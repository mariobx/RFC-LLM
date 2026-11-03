"""Comprehensive Structured Logging Subsystem for RFC-LLM Pipeline."""

import csv
import datetime
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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
        # Group B: Protocol, Solver Complexity & Formal CPSA Security Findings Telemetry
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
        "role_executability",
        "dead_roles_count",
        "authentication_profile",
        "parameter_agreement_status",
        "disagreed_parameters_count",
        "disagreed_parameters_summary",
        "role_reflection_status",
        "secrecy_status",
        "protected_secrets",
        "leaked_secrets",
        "defgoal_satisfaction_status",
        "shape_analysis_sentences_count",
        "encryption_tests_count",
        "nonce_tests_count",
        "channel_tests_count",
        "anomalies_count",
        "vulnerabilities_and_anomalies",
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

    def seed_from_source(self, source_path: Path) -> int:
        """Copies rows from an existing CSV file or prior run directory into `self.csv_path`
        without modifying `source_path` (ensuring strict run-to-run isolation).

        Supports:
        1. Direct `.csv` file path (e.g., `output/run_.../pipeline_runs.csv` or `logs/pipeline_runs.csv`)
        2. Run directory containing `pipeline_runs.csv`
        3. Legacy run directory containing `metadata_index.json` (reconstructs rows from `filtered_rfcs` and `runs`)
        """
        resolved = source_path.resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"Seed CSV or run directory does not exist: {source_path}")

        csv_file: Optional[Path] = None
        index_file: Optional[Path] = None
        if resolved.is_file():
            if resolved.name == "metadata_index.json":
                index_file = resolved
            else:
                csv_file = resolved
        elif resolved.is_dir():
            cand_csv = resolved / "pipeline_runs.csv"
            cand_idx = resolved / "metadata_index.json"
            if cand_csv.exists() and cand_csv.stat().st_size > 0:
                csv_file = cand_csv
            elif cand_idx.exists():
                index_file = cand_idx
            else:
                raise FileNotFoundError(
                    f"Directory {source_path} contains neither pipeline_runs.csv nor metadata_index.json"
                )

        if csv_file is not None:
            if csv_file.resolve() == self.csv_path.resolve():
                return len(self._read_existing_rows())
            seeded_rows: Dict[str, dict] = {}
            with open(csv_file, mode="r", newline="", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    norm_id = self.normalize_rfc_id(row.get("rfc_id", ""))
                    if norm_id:
                        row_copy = dict(row)
                        row_copy["rfc_id"] = norm_id
                        seeded_rows[norm_id] = row_copy
            rows_list = list(seeded_rows.values())
            self._write_all_rows(rows_list)
            return len(rows_list)

        if index_file is not None:
            idx_data = json.loads(index_file.read_text(encoding="utf-8", errors="ignore"))
            created_ts = (idx_data.get("created_at_utc") or "").replace("T", " ").replace("Z", "")
            for filt in idx_data.get("filtered_rfcs", []):
                rid = self.normalize_rfc_id(filt.get("rfc_id", ""))
                if not rid:
                    continue
                reason = filt.get("reason") or "Ineligible"
                if not reason.lower().startswith("ineligible"):
                    reason = f"Ineligible: {reason}"
                self.log_run(
                    rfc_id=rid,
                    is_eligible=False,
                    status="INELIGIBLE",
                    quality_tier="INELIGIBLE",
                    rejection_gate=filt.get("gate") or "Intake Gate",
                    protocol_name=filt.get("title") or rid,
                    duration_seconds=float(filt.get("duration_seconds") or 0.0),
                    error_message=reason,
                )
            for run_entry in idx_data.get("runs", []):
                rid = self.normalize_rfc_id(run_entry.get("rfc_id", ""))
                if not rid:
                    continue
                is_elig = bool(run_entry.get("is_eligible", True))
                traj_str = run_entry.get("metadata_json_file")
                traj_path = Path(traj_str) if traj_str else None
                traj_obj: Dict[str, Any] = {}
                if traj_path and traj_path.exists():
                    try:
                        traj_obj = json.loads(traj_path.read_text(encoding="utf-8", errors="ignore"))
                    except Exception:
                        traj_obj = {}
                meta = traj_obj.get("rfc_metadata", {})
                s2 = traj_obj.get("stage2_initial_extraction", {})
                s5 = traj_obj.get("stage5_preflight_gate", {})
                s6 = traj_obj.get("stage6_cpsa4_solver", {})
                qa = traj_obj.get("quality_assessment", {})
                sec_f = traj_obj.get("security_findings") or qa.get("security_findings")
                ast_obj = (traj_obj.get("final_verified_output") or {}).get("final_ast") or {}
                scm_file_str = run_entry.get("scm_file")
                scm_p = Path(scm_file_str) if scm_file_str else None
                xhtml_p: Optional[Path] = None
                if scm_p and scm_p.parent.exists():
                    xhtmls = sorted(scm_p.parent.glob("*_shapes.xhtml"))
                    if xhtmls:
                        xhtml_p = xhtmls[0]
                self.log_run(
                    rfc_id=rid,
                    is_eligible=is_elig,
                    quality_tier=qa.get("quality_tier") or run_entry.get("quality_tier"),
                    protocol_name=meta.get("protocol_name") or run_entry.get("protocol_name"),
                    message_algebra=meta.get("algebra") or ast_obj.get("message_algebra"),
                    selected_sections=meta.get("selected_sections"),
                    sliced_lines_count=int(meta.get("sliced_lines_count") or 0),
                    role_count=len(ast_obj.get("roles") or []),
                    preskeleton_count=len(ast_obj.get("skeletons") or []),
                    roletran_passed=bool(s5.get("final_passed", run_entry.get("build_successful"))),
                    solver_passed=bool(s6.get("final_passed", run_entry.get("build_successful"))),
                    shapes_count=int(
                        (s6.get("shapes_analysis_from_shapes_txt") or {}).get("total_realized_shapes", 0)
                    ),
                    explored_skeletons_count=int(
                        (s6.get("exploration_telemetry_from_txt") or {}).get("total_explored_labels", 0)
                    ),
                    all_povs_multi_strand=qa.get("all_participant_povs_multi_strand"),
                    secrecy_proved=qa.get("all_secrecy_listeners_unrealized"),
                    schema_repairs=1 if s2.get("schema_self_correction_triggered") else 0,
                    roletran_repairs=int(s5.get("total_attempts") or 0),
                    solver_repairs=int(s6.get("total_attempts") or 0),
                    herald_options=ast_obj.get("herald_options"),
                    duration_seconds=float(traj_obj.get("duration_seconds") or 0.0),
                    cost_telemetry=traj_obj.get("cost_telemetry") or run_entry.get("cost_telemetry"),
                    scm_path=scm_p,
                    shapes_xhtml_path=xhtml_p,
                    trajectory_json_path=traj_path,
                    error_message=run_entry.get("error_message"),
                    security_findings=sec_f,
                )
            return len(self._read_existing_rows())

        return 0

    def prune_keep_ineligible_only(self) -> Tuple[int, int]:
        """Deletes all rows in `self.csv_path` EXCEPT ineligible RFCs (`is_eligible=False`).

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
        security_findings: Optional[Dict[str, Any]] = None,
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

        # Auto-hydrate security_findings from trajectory_json_path if not explicitly passed
        eff_sec = security_findings
        if not eff_sec and trajectory_json_path and Path(trajectory_json_path).exists():
            try:
                t_data = json.loads(Path(trajectory_json_path).read_text(encoding="utf-8", errors="ignore"))
                eff_sec = t_data.get("security_findings") or (t_data.get("quality_assessment") or {}).get("security_findings")
                if not eff_sec:
                    from src.verification_engine.trajectory_metadata_exporter import compute_security_findings
                    s6_t = t_data.get("stage6_cpsa4_solver") or {}
                    fin_t = t_data.get("final_verified_output") or {}
                    eff_sec = compute_security_findings(
                        shapes_analysis=s6_t.get("shapes_analysis_from_shapes_txt") or {},
                        exploration_telemetry=s6_t.get("exploration_telemetry_from_txt") or {},
                        sas_formulas=fin_t.get("shape_analysis_sentences") or [],
                    )
            except Exception:
                eff_sec = None
        eff_sec = eff_sec or {}

        disagreed_list = eff_sec.get("parameter_disagreements") or []
        disagreed_summary_parts = []
        for dp in disagreed_list:
            if isinstance(dp, dict):
                disagreed_summary_parts.append(
                    f"{dp.get('pov_role', '?')}->{dp.get('peer_role', '?')}:{dp.get('parameter', '?')}({dp.get('pov_value', '?')}!={dp.get('peer_value', '?')})"
                )
        disagreed_summary_str = ";".join(disagreed_summary_parts)
        protected_str = ";".join(str(x) for x in (eff_sec.get("protected_secrets") or []))
        leaked_str = ";".join(str(x) for x in (eff_sec.get("leaked_secrets") or []))
        anomalies_list = eff_sec.get("vulnerabilities_and_anomalies") or []
        anomalies_str = " | ".join(str(x) for x in anomalies_list)
        auth_tests = eff_sec.get("authentication_tests_summary") or {}

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
            "role_executability": str(eff_sec.get("role_executability") or "") if is_eligible else "",
            "dead_roles_count": str(int(eff_sec.get("dead_roles_count", 0))) if (is_eligible and eff_sec) else ("0" if is_eligible else ""),
            "authentication_profile": str(eff_sec.get("authentication_profile") or "") if is_eligible else "",
            "parameter_agreement_status": str(eff_sec.get("parameter_agreement_status") or "") if is_eligible else "",
            "disagreed_parameters_count": str(len(disagreed_list)) if is_eligible else "0",
            "disagreed_parameters_summary": disagreed_summary_str if is_eligible else "",
            "role_reflection_status": str(eff_sec.get("role_reflection_status") or "") if is_eligible else "",
            "secrecy_status": str(eff_sec.get("secrecy_status") or "") if is_eligible else "",
            "protected_secrets": protected_str if is_eligible else "",
            "leaked_secrets": leaked_str if is_eligible else "",
            "defgoal_satisfaction_status": str(eff_sec.get("defgoal_satisfaction_status") or "") if is_eligible else "",
            "shape_analysis_sentences_count": str(int(eff_sec.get("shape_analysis_sentences_count", 0))) if is_eligible else "0",
            "encryption_tests_count": str(int(auth_tests.get("encryption_tests", 0))) if is_eligible else "0",
            "nonce_tests_count": str(int(auth_tests.get("nonce_tests", 0))) if is_eligible else "0",
            "channel_tests_count": str(int(auth_tests.get("channel_tests", 0))) if is_eligible else "0",
            "anomalies_count": str(len(anomalies_list)) if is_eligible else "0",
            "vulnerabilities_and_anomalies": anomalies_str if is_eligible else "",
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
        try:
            from src.pipeline_events import GLOBAL_EVENT_BUS
            GLOBAL_EVENT_BUS.emit(
                "csv_updated",
                csv_path=str(self.csv_path),
                rfc_id=norm_rfc_id,
                status=resolved_status,
                quality_tier=resolved_tier,
                total_rows=len(updated_rows),
            )
        except Exception:
            pass
