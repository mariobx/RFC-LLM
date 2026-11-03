"""Comprehensive Structured Logging Subsystem for RFC-LLM Pipeline."""

import csv
import datetime
import logging
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from src.system_config import SYSTEM_CONFIG


class PipelineConsoleFormatter(logging.Formatter):
    """ANSI color-coded console formatter for distinct pipeline stages."""

    GREY = "\x1b[38;20m"
    CYAN = "\x1b[36;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    FORMAT_PREFIX = "%(asctime)s | "
    FORMAT_SUFFIX = " | %(name)s - %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + FORMAT_PREFIX + "DEBUG" + FORMAT_SUFFIX + RESET,
        logging.INFO: CYAN + FORMAT_PREFIX + "INFO " + FORMAT_SUFFIX + RESET,
        logging.WARNING: YELLOW + FORMAT_PREFIX + "WARN " + FORMAT_SUFFIX + RESET,
        logging.ERROR: RED + FORMAT_PREFIX + "ERROR" + FORMAT_SUFFIX + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT_PREFIX + "CRIT " + FORMAT_SUFFIX + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.GREY + self.FORMAT_PREFIX + "%(levelname)s" + self.FORMAT_SUFFIX + self.RESET)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def configure_pipeline_logging(
    log_level: int = logging.INFO,
    run_log_file: Optional[Path] = None,
) -> logging.Logger:
    """Configures the root pipeline logger with both console and file handlers."""
    SYSTEM_CONFIG.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger("rfc_llm")
    root_logger.setLevel(log_level)
    root_logger.propagate = False

    # Avoid duplicate handlers and prevent file descriptor leaks on re-entry across batch runs
    if root_logger.hasHandlers():
        for existing_handler in list(root_logger.handlers):
            root_logger.removeHandler(existing_handler)
            try:
                existing_handler.close()
            except Exception:
                pass

    # Silence third-party litellm, HTTP client, and visualizer access loggers
    for _noisy_logger in ("LiteLLM", "litellm", "LiteLLM Proxy", "LiteLLM Router", "aiohttp.access", "openai", "openai._base_client", "httpx", "httpcore"):
        _nl = logging.getLogger(_noisy_logger)
        _nl.setLevel(logging.WARNING if _noisy_logger == "aiohttp.access" else logging.ERROR)
        _nl.propagate = False

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(PipelineConsoleFormatter())
    root_logger.addHandler(console_handler)

    # 2. Global Pipeline File Handler
    global_log_path = SYSTEM_CONFIG.LOGS_DIR / "rfc_llm_pipeline.log"
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    global_file_handler = logging.FileHandler(global_log_path, mode="a", encoding="utf-8")
    global_file_handler.setLevel(logging.DEBUG)  # Always log debug to file
    global_file_handler.setFormatter(file_formatter)
    root_logger.addHandler(global_file_handler)

    # 3. Optional Per-Run File Handler
    if run_log_file:
        run_log_file.parent.mkdir(parents=True, exist_ok=True)
        run_file_handler = logging.FileHandler(run_log_file, mode="w", encoding="utf-8")
        run_file_handler.setLevel(logging.DEBUG)
        run_file_handler.setFormatter(file_formatter)
        root_logger.addHandler(run_file_handler)

    return root_logger


def get_pipeline_logger(subsystem: str) -> logging.Logger:
    """Returns a namespaced child logger for a specific pipeline subsystem."""
    return logging.getLogger(f"rfc_llm.{subsystem}")


class PipelineMetricsCSVLogger:
    """Logs tabular run-level experiment metrics to a persistent deduplicated CSV master ledger.

    Performs atomic in-place upserts keyed by normalized `rfc_id` (`RFC4285`), overwriting older
    entries when an RFC is re-evaluated while incrementing `run_count`, and automatically
    migrating legacy CSV headers to the expanded 50-column telemetry schema.
    """

    CSV_HEADER = [
        # Group A: Identity, Status, Step Counts & Intake
        "timestamp",
        "rfc_id",
        "run_count",
        "is_eligible",
        "status",
        "quality_tier",
        "total_completion_steps",
        "zero_shot_passed",
        "schema_repairs",
        "roletran_repairs",
        "solver_repairs",
        "total_repairs",
        "rejection_gate",
        "protocol_name",
        # Group B: Protocol & Solver Complexity Telemetry
        "message_algebra",
        "selected_sections",
        "sliced_lines_count",
        "role_count",
        "preskeleton_count",
        "scm_lines_count",
        "shapes_count",
        "explored_skeletons_count",
        "all_povs_multi_strand",
        "secrecy_proved",
        # Group C: Self-Healing Searcher & Snowball Telemetry
        "searcher_invocations",
        "herald_options",
        # Group D: Runtime & Per-Role Model Telemetry (Dedicated columns per model role)
        "duration_seconds",
        "router_model",
        "router_calls",
        "router_tokens",
        "router_cost_usd",
        "extraction_model",
        "extraction_calls",
        "extraction_tokens",
        "extraction_cost_usd",
        "query_model",
        "query_calls",
        "query_tokens",
        "query_cost_usd",
        "repair_model",
        "repair_calls",
        "repair_tokens",
        "repair_cost_usd",
        "total_calls",
        "total_tokens",
        "total_cost_usd",
        # Group E: Persistent Artifact File Paths & Diagnostics
        "scm_path",
        "shapes_xhtml_path",
        "trajectory_json_path",
        "error_message",
    ]

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or (SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv")
        self._ensure_header()

    @staticmethod
    def normalize_rfc_id(rfc_id: str) -> str:
        """Normalizes 'rfc4285', 'RFC 4285', or 'RFC_4285' to canonical 'RFC4285'."""
        return (rfc_id or "").strip().upper().replace(" ", "").replace("_", "")

    def _read_existing_rows(self) -> List[dict]:
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            return []
        try:
            with open(self.csv_path, mode="r", newline="", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                return [dict(row) for row in reader if row.get("rfc_id")]
        except Exception:
            return []

    def _write_all_rows(self, rows: List[dict]) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.csv_path.with_suffix(".csv.tmp")
        with open(tmp_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER, extrasaction="ignore")
            writer.writeheader()
            for r in rows:
                clean_row = {col: r.get(col, "") for col in self.CSV_HEADER}
                writer.writerow(clean_row)
        tmp_path.replace(self.csv_path)

    def _ensure_header(self) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            self._write_all_rows([])
            return
        # Automatically migrate legacy CSV headers if columns changed
        try:
            with open(self.csv_path, mode="r", newline="", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                first_row = next(reader, None)
            if first_row != self.CSV_HEADER:
                existing = self._read_existing_rows()
                # Deduplicate any legacy duplicate rows on migration, keeping latest & counting runs
                deduped: dict = {}
                counts: dict = {}
                for r in existing:
                    norm_id = self.normalize_rfc_id(r.get("rfc_id", ""))
                    if not norm_id:
                        continue
                    counts[norm_id] = counts.get(norm_id, 0) + 1
                    r["rfc_id"] = norm_id
                    if not r.get("run_count"):
                        r["run_count"] = str(counts[norm_id])
                    deduped[norm_id] = r
                self._write_all_rows(list(deduped.values()))
        except Exception:
            pass

    def prune_keep_ineligible_only(self) -> Tuple[int, int]:
        """Deletes all rows in `logs/pipeline_runs.csv` EXCEPT ineligible RFCs (`is_eligible=False`).

        Allows starting a fresh synthesis run over eligible protocols while preserving cached
        Tier 0 / Stage 1 / Stage 2 ineligibility decisions so non-protocol RFCs are skipped in 0ms.

        Returns:
            Tuple of `(removed_eligible_rows_count, kept_ineligible_rows_count)`.
        """
        existing_rows = self._read_existing_rows()
        kept_rows: List[dict] = []
        removed_count = 0
        seen_ids = set()
        for row in existing_rows:
            is_elig_str = (row.get("is_eligible") or "").strip().lower()
            status_str = (row.get("status") or "").strip().upper()
            if is_elig_str == "false" or status_str == "INELIGIBLE":
                norm_id = self.normalize_rfc_id(row.get("rfc_id", ""))
                if norm_id and norm_id not in seen_ids:
                    seen_ids.add(norm_id)
                    row["rfc_id"] = norm_id
                    kept_rows.append(row)
            else:
                removed_count += 1
        self._write_all_rows(kept_rows)
        return removed_count, len(kept_rows)

    def log_run(
        self,
        rfc_id: str,
        is_eligible: bool,
        status: Optional[str] = None,
        quality_tier: Optional[str] = None,
        rejection_gate: Optional[str] = None,
        protocol_name: Optional[str] = None,
        message_algebra: Optional[str] = None,
        selected_sections: Optional[List[str]] = None,
        sliced_lines_count: int = 0,
        role_count: int = 0,
        preskeleton_count: int = 0,
        scm_lines_count: int = 0,
        roletran_passed: Optional[bool] = None,
        solver_passed: Optional[bool] = None,
        shapes_count: int = 0,
        explored_skeletons_count: int = 0,
        all_povs_multi_strand: Optional[bool] = None,
        secrecy_proved: Optional[bool] = None,
        zero_shot_passed: Optional[bool] = None,
        schema_repairs: int = 0,
        roletran_repairs: int = 0,
        solver_repairs: int = 0,
        total_repairs: Optional[int] = None,
        total_completion_steps: Optional[int] = None,
        searcher_invocations: int = 0,
        herald_options: Optional[List[str]] = None,
        duration_seconds: float = 0.0,
        cost_telemetry: Optional[dict] = None,
        router_model: Optional[str] = None,
        extraction_model: Optional[str] = None,
        query_model: Optional[str] = None,
        repair_model: Optional[str] = None,
        scm_path: Optional[Path] = None,
        shapes_xhtml_path: Optional[Path] = None,
        trajectory_json_path: Optional[Path] = None,
        error_message: Optional[str] = None,
    ) -> None:
        now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        norm_rfc_id = self.normalize_rfc_id(rfc_id)
        sec_str = ";".join(selected_sections) if selected_sections else ""
        herald_str = ";".join(herald_options) if herald_options else ""

        # Resolve high-level status if not explicitly passed
        resolved_status = status
        if not resolved_status:
            if not is_eligible:
                resolved_status = "INELIGIBLE"
            elif solver_passed:
                resolved_status = "VERIFIED"
            elif roletran_passed:
                resolved_status = "PARTIAL"
            else:
                resolved_status = "FAILED"

        resolved_tier = quality_tier or ("INELIGIBLE" if not is_eligible else "REJECTED")
        computed_total_repairs = (
            total_repairs
            if total_repairs is not None
            else (int(schema_repairs) + int(roletran_repairs) + int(solver_repairs))
        )
        computed_total_steps = (
            total_completion_steps
            if total_completion_steps is not None
            else ((1 + int(schema_repairs) + int(roletran_repairs) + int(solver_repairs)) if is_eligible else 0)
        )
        resolved_zero_shot = (
            zero_shot_passed
            if zero_shot_passed is not None
            else (bool(solver_passed) and computed_total_repairs == 0)
        )

        # Auto-compute scm_lines_count if scm_path exists and wasn't explicitly passed
        effective_scm_lines = scm_lines_count
        if effective_scm_lines == 0 and scm_path and Path(scm_path).exists():
            try:
                effective_scm_lines = len(
                    Path(scm_path).read_text(encoding="utf-8", errors="ignore").splitlines()
                )
            except Exception:
                effective_scm_lines = 0

        # Extract per-role model telemetry from cost_telemetry (or GLOBAL_COST_TRACKER)
        roles_data = (cost_telemetry or {}).get("roles", {})
        r_info = roles_data.get("router", {})
        e_info = roles_data.get("extraction", {})
        q_info = roles_data.get("query", {})
        p_info = roles_data.get("repair", {})

        tot_calls = int((cost_telemetry or {}).get("total_calls", 0))
        tot_tokens = int((cost_telemetry or {}).get("total_tokens", 0))
        tot_cost = float((cost_telemetry or {}).get("total_cost_usd", 0.0))

        new_row = {
            "timestamp": now_iso,
            "rfc_id": norm_rfc_id,
            "run_count": "1",
            "is_eligible": str(bool(is_eligible)),
            "status": resolved_status,
            "quality_tier": resolved_tier,
            "total_completion_steps": str(computed_total_steps),
            "zero_shot_passed": "" if not is_eligible else str(bool(resolved_zero_shot)),
            "schema_repairs": str(schema_repairs) if is_eligible else "0",
            "roletran_repairs": str(roletran_repairs) if is_eligible else "0",
            "solver_repairs": str(solver_repairs) if is_eligible else "0",
            "total_repairs": str(computed_total_repairs) if is_eligible else "0",
            "rejection_gate": rejection_gate or "",
            "protocol_name": protocol_name or "",
            "message_algebra": message_algebra or "",
            "selected_sections": sec_str,
            "sliced_lines_count": str(sliced_lines_count) if is_eligible else "0",
            "role_count": str(role_count) if is_eligible else "0",
            "preskeleton_count": str(preskeleton_count) if is_eligible else "0",
            "scm_lines_count": str(effective_scm_lines) if is_eligible else "0",
            "shapes_count": str(shapes_count) if is_eligible else "0",
            "explored_skeletons_count": str(explored_skeletons_count) if is_eligible else "0",
            "all_povs_multi_strand": "" if all_povs_multi_strand is None else str(bool(all_povs_multi_strand)),
            "secrecy_proved": "" if secrecy_proved is None else str(bool(secrecy_proved)),
            "searcher_invocations": str(searcher_invocations) if is_eligible else "0",
            "herald_options": herald_str,
            "duration_seconds": str(round(duration_seconds, 3)),
            "router_model": router_model or r_info.get("model") or "",
            "router_calls": str(int(r_info.get("calls", 0))),
            "router_tokens": str(int(r_info.get("total_tokens", 0))),
            "router_cost_usd": f"{float(r_info.get('cost_usd', 0.0)):.6f}",
            "extraction_model": extraction_model or e_info.get("model") or "",
            "extraction_calls": str(int(e_info.get("calls", 0))),
            "extraction_tokens": str(int(e_info.get("total_tokens", 0))),
            "extraction_cost_usd": f"{float(e_info.get('cost_usd', 0.0)):.6f}",
            "query_model": query_model or q_info.get("model") or "",
            "query_calls": str(int(q_info.get("calls", 0))),
            "query_tokens": str(int(q_info.get("total_tokens", 0))),
            "query_cost_usd": f"{float(q_info.get('cost_usd', 0.0)):.6f}",
            "repair_model": repair_model or p_info.get("model") or "",
            "repair_calls": str(int(p_info.get("calls", 0))),
            "repair_tokens": str(int(p_info.get("total_tokens", 0))),
            "repair_cost_usd": f"{float(p_info.get('cost_usd', 0.0)):.6f}",
            "total_calls": str(tot_calls),
            "total_tokens": str(tot_tokens),
            "total_cost_usd": f"{tot_cost:.6f}",
            "scm_path": str(scm_path) if scm_path else "",
            "shapes_xhtml_path": str(shapes_xhtml_path) if shapes_xhtml_path else "",
            "trajectory_json_path": str(trajectory_json_path) if trajectory_json_path else "",
            "error_message": error_message or "",
        }

        existing_rows = self._read_existing_rows()
        replaced = False
        updated_rows: List[dict] = []
        for row in existing_rows:
            row_id = self.normalize_rfc_id(row.get("rfc_id", ""))
            if row_id == norm_rfc_id:
                if not replaced:
                    try:
                        prev_count = int(row.get("run_count") or 1)
                    except (TypeError, ValueError):
                        prev_count = 1
                    new_row["run_count"] = str(prev_count + 1)
                    updated_rows.append(new_row)
                    replaced = True
                # Skip any older duplicate rows for this same rfc_id
            else:
                updated_rows.append(row)

        if not replaced:
            updated_rows.append(new_row)

        self._write_all_rows(updated_rows)
