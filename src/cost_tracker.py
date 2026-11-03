"""Real-Time Token & USD Cost Telemetry Tracker across Pipeline Model Roles.

Tracks per-call, per-RFC, and cumulative batch token usage and USD cost across the
four pipeline model roles:
  1. `router`     — Stage 1b Applicability Gate & Stage 1c Section Router
  2. `extraction` — Stage 2 Constrained Protocol Extraction & Schema Self-Correction
  3. `query`      — Stage 5/6 Agentic CPSA Knowledge Base Searcher
  4. `repair`     — Stage 5/6 Compiler & Solver Diagnostic Self-Healing Repair
"""

from __future__ import annotations

import copy
import json
import threading
import urllib.request
from typing import Any, Dict, Literal, Optional, Tuple

import litellm

from src.logging_config import get_pipeline_logger
from src.pipeline_events import GLOBAL_EVENT_BUS
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("cost_tracker")

ModelRoleLiteral = Literal["router", "extraction", "query", "repair"]
MODEL_ROLES: Tuple[str, ...] = ("router", "extraction", "query", "repair")

# Built-in fallback per-token USD rates (prompt, completion, cache_read) per 1 token
# Derived from live Nous Research / OpenAI / Anthropic / Google / DeepSeek pricing.
_FALLBACK_PRICING_PER_TOKEN: Dict[str, Tuple[float, float, float]] = {
    "openai/gpt-6.1-terra": (1.00e-6, 5.00e-6, 0.05e-6),
    "openai/gpt-6.1-terra-pro": (1.00e-6, 5.00e-6, 0.05e-6),
    "openai/gpt-6.1-sol": (2.00e-6, 10.00e-6, 0.10e-6),
    "openai/gpt-6-luna": (0.10e-6, 0.50e-6, 0.01e-6),
    "openai/gpt-6-luna-pro": (0.10e-6, 0.50e-6, 0.01e-6),
    "anthropic/claude-haiku-5.5": (0.10e-6, 0.50e-6, 0.01e-6),
    "anthropic/claude-sonnet-5.5": (2.00e-6, 10.00e-6, 0.10e-6),
    "anthropic/claude-sonnet-4.6": (3.00e-6, 15.00e-6, 0.30e-6),
    "google/gemini-3.7-flash": (0.75e-6, 3.75e-6, 0.075e-6),
    "google/gemini-3.8-flash": (0.825e-6, 4.125e-6, 0.0825e-6),
    "google/gemini-3.1-flash-lite-preview": (0.25e-6, 1.50e-6, 0.025e-6),
    "google/gemini-3.1-pro-preview": (2.00e-6, 12.00e-6, 0.20e-6),
    "google/gemini-2.5-flash": (0.15e-6, 0.60e-6, 0.0375e-6),
    "google/gemini-2.5-flash-lite": (0.10e-6, 0.40e-6, 0.025e-6),
    "z-ai/glm-5.3": (0.91e-6, 2.86e-6, 0.169e-6),
    "z-ai/glm-5.3-flash": (0.12e-6, 0.40e-6, 0.024e-6),
    "z-ai/glm-5.2": (0.90e-6, 2.83e-6, 0.16e-6),
    "deepseek/deepseek-v4-pro": (0.94e-6, 1.89e-6, 0.08e-6),
    "deepseek/deepseek-v4.1-flash": (0.106e-6, 0.513e-6, 0.004e-6),
    "deepseek/deepseek-v4-flash": (0.091e-6, 0.182e-6, 0.0182e-6),
    "deepseek/deepseek-v4-flash-0731": (0.054e-6, 0.162e-6, 0.0135e-6),
    "deepseek/deepseek-chat": (0.27e-6, 1.10e-6, 0.07e-6),
    "qwen/qwen3.8-flash": (0.15e-6, 0.47e-6, 0.016e-6),
    "qwen/qwen3.6-flash": (0.1875e-6, 1.125e-6, 0.02e-6),
}


def _empty_role_bucket(model_name: str = "") -> Dict[str, Any]:
    return {
        "model": model_name,
        "calls": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "cached_tokens": 0,
        "total_tokens": 0,
        "cost_usd": 0.0,
    }


def make_empty_cost_summary() -> Dict[str, Any]:
    """Creates a clean per-RFC or batch cost telemetry dictionary."""
    return {
        "total_calls": 0,
        "total_prompt_tokens": 0,
        "total_completion_tokens": 0,
        "total_cached_tokens": 0,
        "total_tokens": 0,
        "total_cost_usd": 0.0,
        "roles": {role: _empty_role_bucket() for role in MODEL_ROLES},
    }


def _normalize_model_key(model_name: str) -> str:
    """Normalizes `nous/openai/gpt-6.1-terra` or `openai/gpt-6.1-terra` to `openai/gpt-6.1-terra`."""
    cleaned = (model_name or "").strip()
    for prefix in ("nous/", "nousresearch/"):
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
    if cleaned.startswith("openai/") and cleaned.count("/") >= 2:
        cleaned = cleaned.split("/", 1)[1]
    return cleaned


def _safe_int(val: Any) -> int:
    """Extracts an integer token count, returning 0 for None or unit-test MagicMocks."""
    if isinstance(val, bool):
        return 0
    if isinstance(val, int):
        return max(0, val)
    if isinstance(val, float):
        return max(0, int(val))
    return 0


class PipelineCostTracker:
    """Thread-safe tracker for per-RFC and cumulative batch token usage and USD costs."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._live_pricing: Dict[str, Tuple[float, float, float]] = dict(_FALLBACK_PRICING_PER_TOKEN)
        self._catalog_fetched = False
        self.current_rfc_id: Optional[str] = None
        self.current_rfc: Dict[str, Any] = make_empty_cost_summary()
        self.batch_total: Dict[str, Any] = make_empty_cost_summary()
        self.rfc_history: Dict[str, Dict[str, Any]] = {}

    def _ensure_live_pricing_loaded(self) -> None:
        if self._catalog_fetched:
            return
        self._catalog_fetched = True
        if not SYSTEM_CONFIG.NOUS_API_KEY:
            return
        try:
            req = urllib.request.Request(
                f"{SYSTEM_CONFIG.NOUS_API_BASE.rstrip('/')}/models",
                headers={
                    "Authorization": f"Bearer {SYSTEM_CONFIG.NOUS_API_KEY}",
                    "User-Agent": "RFC-LLM-CostTracker/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
                for item in payload.get("data", []):
                    mid = item.get("id")
                    pricing = item.get("pricing")
                    if mid and isinstance(pricing, dict):
                        p_rate = float(pricing.get("prompt") or 0.0)
                        c_rate = float(pricing.get("completion") or 0.0)
                        cache_rate = float(pricing.get("input_cache_read") or p_rate)
                        self._live_pricing[mid] = (p_rate, c_rate, cache_rate)
        except Exception as exc:
            logger.debug("Using fallback pricing table (live catalog fetch skipped: %s)", exc)

    def get_model_rates(self, model_name: str) -> Tuple[float, float, float]:
        """Returns `(prompt_rate, completion_rate, cache_read_rate)` in USD per single token."""
        if model_name.startswith(("ollama/", "strata/")):
            return (0.0, 0.0, 0.0)
        self._ensure_live_pricing_loaded()
        norm = _normalize_model_key(model_name)
        if norm in self._live_pricing:
            return self._live_pricing[norm]
        # Try suffix match (e.g. `gemini-2.5-flash` -> `google/gemini-2.5-flash`)
        short = norm.split("/")[-1]
        for k, rates in self._live_pricing.items():
            if k.endswith(f"/{short}") or k == short:
                return rates
        return (0.0, 0.0, 0.0)

    def start_rfc(
        self,
        rfc_id: str,
        router_model: str = "",
        extraction_model: str = "",
        query_model: str = "",
        repair_model: str = "",
    ) -> None:
        """Resets the active per-RFC cost bucket when starting a new RFC run."""
        with self._lock:
            self.current_rfc_id = rfc_id
            self.current_rfc = make_empty_cost_summary()
            role_models = {
                "router": router_model,
                "extraction": extraction_model,
                "query": query_model,
                "repair": repair_model,
            }
            for role, mod in role_models.items():
                if mod:
                    self.current_rfc["roles"][role]["model"] = mod
                    if not self.batch_total["roles"][role]["model"]:
                        self.batch_total["roles"][role]["model"] = mod
            self.rfc_history[rfc_id] = copy.deepcopy(self.current_rfc)

    def record_llm_call(
        self,
        response: Any,
        role: ModelRoleLiteral,
        model_name: str,
        stage: int = 0,
    ) -> Dict[str, Any]:
        """Extracts token usage and USD cost from a LiteLLM response, updates both the
        per-RFC and batch totals, and emits a `cost_updated` visualizer event.
        """
        usage = getattr(response, "usage", None)
        if usage is None and isinstance(response, dict):
            usage = response.get("usage")

        prompt_tok = 0
        comp_tok = 0
        cached_tok = 0

        if usage is not None:
            prompt_tok = _safe_int(
                getattr(usage, "prompt_tokens", None)
                if not isinstance(usage, dict)
                else usage.get("prompt_tokens")
            )
            comp_tok = _safe_int(
                getattr(usage, "completion_tokens", None)
                if not isinstance(usage, dict)
                else usage.get("completion_tokens")
            )
            details = (
                getattr(usage, "prompt_tokens_details", None)
                if not isinstance(usage, dict)
                else usage.get("prompt_tokens_details")
            )
            if details is not None:
                cached_tok = _safe_int(
                    getattr(details, "cached_tokens", None)
                    if not isinstance(details, dict)
                    else details.get("cached_tokens")
                )

        # Estimate cost from live/fallback rates first
        p_rate, c_rate, cache_rate = self.get_model_rates(model_name)
        uncached_prompt = max(0, prompt_tok - cached_tok)
        call_cost = (uncached_prompt * p_rate) + (cached_tok * cache_rate) + (comp_tok * c_rate)

        # If rates were 0 (unknown external model), check LiteLLM response_cost
        if call_cost == 0.0 and (prompt_tok > 0 or comp_tok > 0) and not model_name.startswith(("ollama/", "strata/")):
            try:
                hidden = getattr(response, "_hidden_params", None) or {}
                if isinstance(hidden, dict) and isinstance(hidden.get("response_cost"), (int, float)):
                    call_cost = float(hidden["response_cost"])
                else:
                    litellm_cost = litellm.completion_cost(completion_response=response)
                    if isinstance(litellm_cost, (int, float)):
                        call_cost = float(litellm_cost)
            except Exception:
                pass

        total_tok = prompt_tok + comp_tok
        role_key = role if role in MODEL_ROLES else "repair"

        with self._lock:
            for target in (self.current_rfc, self.batch_total):
                target["total_calls"] += 1
                target["total_prompt_tokens"] += prompt_tok
                target["total_completion_tokens"] += comp_tok
                target["total_cached_tokens"] += cached_tok
                target["total_tokens"] += total_tok
                target["total_cost_usd"] = round(target["total_cost_usd"] + call_cost, 8)

                rb = target["roles"][role_key]
                if model_name:
                    rb["model"] = model_name
                rb["calls"] += 1
                rb["prompt_tokens"] += prompt_tok
                rb["completion_tokens"] += comp_tok
                rb["cached_tokens"] += cached_tok
                rb["total_tokens"] += total_tok
                rb["cost_usd"] = round(rb["cost_usd"] + call_cost, 8)

            rfc_snap = copy.deepcopy(self.current_rfc)
            batch_snap = copy.deepcopy(self.batch_total)
            if self.current_rfc_id:
                self.rfc_history[self.current_rfc_id] = rfc_snap

        GLOBAL_EVENT_BUS.emit(
            "cost_updated",
            stage=stage,
            role=role_key,
            model=model_name,
            call_tokens=total_tok,
            call_cost_usd=round(call_cost, 8),
            rfc_cost=rfc_snap,
            batch_cost=batch_snap,
        )
        return rfc_snap

    def get_current_rfc_summary(self) -> Dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self.current_rfc)

    def get_batch_summary(self) -> Dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self.batch_total)

    @staticmethod
    def format_cli_summary(summary: Dict[str, Any], prefix: str = "Run Cost") -> str:
        """Formats a single-line human-readable summary of total and per-role costs."""
        roles = summary.get("roles", {})
        total_usd = float(summary.get("total_cost_usd", 0.0))
        total_tok = int(summary.get("total_tokens", 0))
        r_usd = float(roles.get("router", {}).get("cost_usd", 0.0))
        e_usd = float(roles.get("extraction", {}).get("cost_usd", 0.0))
        q_usd = float(roles.get("query", {}).get("cost_usd", 0.0))
        rep_usd = float(roles.get("repair", {}).get("cost_usd", 0.0))
        return (
            f"{prefix}: ${total_usd:.4f} ({total_tok:,} tok) | "
            f"Router: ${r_usd:.4f} | Extraction: ${e_usd:.4f} | "
            f"Query/Searcher: ${q_usd:.4f} | Repair: ${rep_usd:.4f}"
        )


GLOBAL_COST_TRACKER = PipelineCostTracker()
