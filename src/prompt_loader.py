"""Dynamic Markdown & YAML-Frontmatter Prompt Loader for RFC-LLM (prompts/ directory).

Each `prompts/*.md` file begins with an optional YAML frontmatter block configuring
its target LLM (`model`), request `timeout`, and optional `temperature`, followed by
the system prompt body:

    ---
    model: strata/unsloth-iq4_xs
    timeout: 180
    temperature: 0.0
    ---
    You are a formal methods expert...

Files are read dynamically on every invocation so prompt and model edits hot-reload
live mid-batch without restarting the pipeline.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Type
import yaml
from pydantic import BaseModel

from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("prompt_loader")

# Canonical prompt filenames in prompts/
PROMPT_APPLICABILITY_GATE = "01_applicability_gate.md"
PROMPT_SECTION_ROUTER = "02_section_router.md"
PROMPT_PROTOCOL_EXTRACTION = "03_protocol_extraction.md"
PROMPT_SCHEMA_SELF_CORRECTION = "04_schema_self_correction.md"
PROMPT_RAG_QUERY_FORMULATION = "05_rag_query_formulation.md"
PROMPT_COMPILER_REPAIR = "06_compiler_repair.md"
PROMPT_THINK_SYNTHESIZER = "07_think_token_synthesizer.md"

GLOBAL_FALLBACK_MODEL = "gemini/gemini-3.5-flash-lite"

# Built-in fallback models & timeouts when a `prompts/*.md` file omits frontmatter or is missing
_FALLBACK_METADATA: Dict[str, Dict[str, Any]] = {
    PROMPT_APPLICABILITY_GATE: {"model": "strata/unsloth-iq4_xs", "timeout": 1500, "max_tokens": 65536, "temperature": 0.0},
    PROMPT_SECTION_ROUTER: {"model": "strata/unsloth-iq4_xs", "timeout": 1500, "max_tokens": 65536, "temperature": 0.0},
    PROMPT_PROTOCOL_EXTRACTION: {"model": "strata/unsloth-iq4_xs", "timeout": 1500, "max_tokens": 65536, "temperature": 0.0},
    PROMPT_SCHEMA_SELF_CORRECTION: {"model": "strata/unsloth-iq4_xs", "timeout": 1500, "max_tokens": 65536, "temperature": 0.0},
    PROMPT_RAG_QUERY_FORMULATION: {"model": "strata/unsloth-iq4_xs", "timeout": 1500, "max_tokens": 65536, "temperature": 0.0},
    PROMPT_COMPILER_REPAIR: {"model": "strata/unsloth-iq4_xs", "timeout": 1500, "max_tokens": 65536, "temperature": 0.0},
    PROMPT_THINK_SYNTHESIZER: {"model": "strata/unsloth-iq4_xs", "timeout": 1500, "max_tokens": 65536, "temperature": 0.2},
}

# Built-in fallback prompt bodies if a file in prompts/ is missing or empty
_FALLBACK_PROMPTS: Dict[str, str] = {
    PROMPT_APPLICABILITY_GATE: (
        "You are a formal methods expert in cryptographic protocol verification using MITRE CPSA 4.4.9.\n"
        "Analyze the RFC metadata and Table of Contents to determine if it specifies an interactive "
        "cryptographic security protocol.\n"
        "CRITICAL: Return a populated JSON instance, NOT the schema definition."
    ),
    PROMPT_SECTION_ROUTER: (
        "You are a protocol analyst reading an RFC's Table of Contents.\n"
        "Identify the EXACT section numbers that define the cryptographic message exchange or handshake.\n"
        "Return ONLY a valid JSON object matching the requested schema."
    ),
    PROMPT_PROTOCOL_EXTRACTION: (
        "You are a formal methods expert in cryptographic protocol specification for MITRE CPSA 4.4.9.\n"
        "Analyze the verbatim RFC specification text and extract a complete, mathematically rigorous "
        "CPSAProtocolSpecification.\n"
        "Return ONLY a valid JSON object matching the requested CPSAProtocolSpecification schema."
    ),
    PROMPT_SCHEMA_SELF_CORRECTION: (
        "Your previous JSON output failed MITRE CPSA 4.4.9 schema and scoping validation with the following errors:\n"
        "{validation_error}\n\n"
        "Return ONLY the corrected, fully valid JSON object."
    ),
    PROMPT_RAG_QUERY_FORMULATION: (
        "You are a formal verification compiler diagnostic analyst for MITRE CPSA 4.4.9.\n"
        "Formulate a concise, targeted search query (3 to 6 words) abstracting concrete variable names "
        "into formal CPSA grammar, algebra, or roletran concepts.\n"
        "Output strictly the plain text search query (3 to 6 words)."
    ),
    PROMPT_COMPILER_REPAIR: (
        "You are a formal methods expert in debugging and repairing MITRE CPSA 4.4.9 protocol specifications.\n"
        "Identify the precise defect causing the compiler or solver failure and return a corrected "
        "CPSAProtocolSpecification matching the requested JSON schema."
    ),
    PROMPT_THINK_SYNTHESIZER: (
        "You are a formal methods expert in MITRE CPSA 4.4.9 synthesizing a first-person reasoning monologue "
        "(<think>...</think>) that derives a formally verified CPSA specification from verbatim IETF RFC prose.\n"
        "Never mention that you were provided the final AST or .scm output in advance; write strictly from a "
        "forward-looking, first-principles deduction perspective, incorporating compiler self-correction and "
        "backtracking steps where applicable."
    ),
}

_FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", re.DOTALL)


class PromptSpec(BaseModel):
    """Parsed prompt template and LLM execution parameters loaded from `prompts/<filename>`."""

    filename: str
    body: str
    model: str
    timeout: int = 1500
    max_tokens: int = 65536
    temperature: Optional[float] = None


def parse_prompt_frontmatter(raw_text: str) -> Tuple[Dict[str, Any], str]:
    """Splits optional leading `--- ... ---` YAML frontmatter from the Markdown prompt body."""
    stripped = raw_text.lstrip("\ufeff")
    match = _FRONTMATTER_RE.match(stripped)
    if not match:
        return {}, stripped.strip()

    yaml_block = match.group(1)
    body = stripped[match.end():].strip()
    try:
        parsed = yaml.safe_load(yaml_block)
        meta = parsed if isinstance(parsed, dict) else {}
    except Exception as exc:
        logger.warning("Invalid YAML frontmatter in prompt (%s); ignoring frontmatter block.", exc)
        meta = {}
    return meta, body


def load_prompt_spec(prompt_filename: str, prompts_dir: Optional[Path] = None) -> PromptSpec:
    """Loads a `PromptSpec` (model, timeout, temperature, stripped prompt body) dynamically from `prompts/`."""
    base_dir = prompts_dir or SYSTEM_CONFIG.PROMPTS_DIR
    prompt_path = base_dir / prompt_filename
    defaults = _FALLBACK_METADATA.get(prompt_filename, {})
    default_model = str(defaults.get("model") or GLOBAL_FALLBACK_MODEL)
    default_timeout = int(defaults.get("timeout") or SYSTEM_CONFIG.LLM_TIMEOUT_SECONDS)
    default_max_tokens = int(defaults.get("max_tokens") or 65536)
    default_temp = defaults.get("temperature")

    meta: Dict[str, Any] = {}
    body: str = ""

    if prompt_path.exists() and prompt_path.is_file():
        try:
            raw_content = prompt_path.read_text(encoding="utf-8")
            meta, body = parse_prompt_frontmatter(raw_content)
            if not body:
                logger.warning("Prompt body in %s is empty; using built-in fallback body.", prompt_path)
        except Exception as exc:
            logger.warning("Failed to read prompt file %s (%s); using built-in fallback.", prompt_path, exc)
    else:
        logger.debug("Prompt file %s not found; using built-in fallback.", prompt_path)

    if not body:
        if prompt_filename in _FALLBACK_PROMPTS:
            body = _FALLBACK_PROMPTS[prompt_filename]
        else:
            raise FileNotFoundError(f"Prompt template '{prompt_filename}' not found in {base_dir}")

    raw_model = meta.get("model")
    resolved_model = str(raw_model).strip() if raw_model and str(raw_model).strip() else default_model

    raw_timeout = meta.get("timeout")
    try:
        resolved_timeout = int(raw_timeout) if raw_timeout is not None else default_timeout
    except (TypeError, ValueError):
        resolved_timeout = default_timeout

    raw_max_tokens = meta.get("max_tokens")
    try:
        resolved_max_tokens = int(raw_max_tokens) if raw_max_tokens is not None else default_max_tokens
    except (TypeError, ValueError):
        resolved_max_tokens = default_max_tokens

    raw_temp = meta.get("temperature", default_temp)
    try:
        resolved_temp = float(raw_temp) if raw_temp is not None else None
    except (TypeError, ValueError):
        resolved_temp = default_temp

    return PromptSpec(
        filename=prompt_filename,
        body=body,
        model=resolved_model,
        timeout=resolved_timeout,
        max_tokens=resolved_max_tokens,
        temperature=resolved_temp,
    )


def resolve_prompt_model(
    prompt_filename: str,
    override_model: Optional[str] = None,
    prompts_dir: Optional[Path] = None,
) -> str:
    """Returns `override_model` if explicitly provided (e.g., via CLI flag), else the frontmatter `model`."""
    if override_model and override_model.strip():
        return override_model.strip()
    return load_prompt_spec(prompt_filename, prompts_dir=prompts_dir).model


def load_prompt(prompt_filename: str, prompts_dir: Optional[Path] = None) -> str:
    """Loads the Markdown prompt body (with YAML frontmatter stripped) from `prompts/<prompt_filename>`."""
    return load_prompt_spec(prompt_filename, prompts_dir=prompts_dir).body


def build_schema_system_prompt(
    prompt_filename: str,
    schema_model: Type[BaseModel],
    prompts_dir: Optional[Path] = None,
) -> str:
    """Loads a stripped base system prompt from `prompts/` and appends the mandatory Pydantic JSON schema."""
    base_prompt = load_prompt(prompt_filename, prompts_dir=prompts_dir)
    schema_json = json.dumps(schema_model.model_json_schema(), indent=2)
    return f"{base_prompt}\n\nRespond strictly with a valid JSON object matching this schema:\n{schema_json}"


_THINK_TAG_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def parse_llm_json(raw_content: Optional[str]) -> Any:
    """Strips `<think>...</think>` reasoning blocks and markdown fences, then parses or repairs JSON."""
    import json_repair

    text = (raw_content or "").strip()
    if not text:
        return {}

    # 1. Strip complete <think>...</think> blocks
    cleaned = _THINK_TAG_RE.sub("", text).strip()
    # If an unclosed <think> tag preceded a JSON block, jump to the last `</think>` or first `{` after it
    if "</think>" in cleaned.lower():
        idx = cleaned.lower().rfind("</think>")
        cleaned = cleaned[idx + len("</think>") :].strip()
    elif cleaned.lower().startswith("<think>"):
        brace_idx = cleaned.find("{")
        if brace_idx != -1:
            cleaned = cleaned[brace_idx:].strip()

    # 2. Strip markdown ```json ... ``` fences if present
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except Exception:
        # Extract from first '{' to last '}' if surrounded by prose
        first_brace = cleaned.find("{")
        last_brace = cleaned.rfind("}")
        if first_brace != -1 and last_brace > first_brace:
            candidate = cleaned[first_brace : last_brace + 1]
            try:
                return json.loads(candidate)
            except Exception:
                return json_repair.loads(candidate)
        return json_repair.loads(cleaned)
