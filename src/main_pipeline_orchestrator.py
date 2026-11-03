"""Main Pipeline Orchestrator for RFC-to-CPSA Synthesis.

Coordinates the 6-stage synthesis pipeline for a single RFC document:
- Stage 1 (Document Intake): Tier 0 Header Filter, TOC Parsing, Tier 1 Applicability Gate,
  Exchange Section Routing, and Verbatim Section Slicing.
- Stage 2 (JSON CPSA Generation): Constrained Protocol Extraction with RAG grounding and 1-shot schema correction.
- Stage 3 (CPSA4json -> scm): CPSA JSON Serialization and Scheme S-Expression Emission (`cpsa4json`).
- Stage 4 (Roletran Check): Pre-Flight Executability Check (`cpsa4roletran` / `cpsa4 -l 1`).
- Stage 5 (Self-Healing Loop): Cycle-aware RAG diagnostic repair loop for pre-flight defects.
- Stage 6 (CPSA Compilation): MITRE CPSA compilation and shape realization (`make` / `cpsa4` / `cpsa4shapes` / `cpsa4graph`, 60s hard cap) with RAG self-healing.
"""

import datetime as dt
import hashlib
import json
import time
from pathlib import Path
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

from src.code_generation.cpsa_scheme_emitter import emit_cpsa_scheme
from src.document_ingestion.handshake_section_router import route_handshake_sections
from src.document_ingestion.protocol_applicability_gate import evaluate_protocol_applicability
from src.document_ingestion.rfc_header_filter import filter_rfc_header
from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections
from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import (
    PipelineMetricsCSVLogger,
    configure_pipeline_logging,
    get_pipeline_logger,
)
from src.pipeline_events import GLOBAL_EVENT_BUS
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    PROMPT_COMPILER_REPAIR,
    PROMPT_PROTOCOL_EXTRACTION,
    PROMPT_RAG_QUERY_FORMULATION,
    resolve_prompt_model,
)
from src.semantic_extraction import constrained_protocol_extractor
from src.semantic_extraction.constrained_protocol_extractor import extract_protocol_specification
from src.system_config import SYSTEM_CONFIG
from src.verification_engine import compiler_diagnostic_repair
from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification
from src.verification_engine.mitre_build_orchestrator import (
    CPSABuildArtifacts,
    execute_mitre_make_build,
)
from src.verification_engine.snowball_autopsy import is_snowball_state_error
from src.verification_engine.roletran_executability_gate import (
    RoletranVerificationResult,
    verify_role_executability,
)
from src.verification_engine.trajectory_metadata_exporter import (
    update_run_metadata_index,
    write_trajectory_metadata_bundle,
)

logger = get_pipeline_logger("orchestrator")


class PipelineExecutionSummary(BaseModel):
    """Execution summary of an end-to-end RFC synthesis run."""

    rfc_id: str = Field(..., description="Target RFC identifier")
    protocol_name: Optional[str] = Field(None, description="Identified protocol name")
    is_eligible: bool = Field(..., description="Whether the RFC passed intake filtering")
    selected_sections: List[str] = Field(default_factory=list, description="RFC sections sliced for synthesis")
    sliced_lines_count: int = Field(default=0, description="Number of lines in the verbatim slice")
    roletran_passed: bool = Field(default=False, description="Whether static role executability passed")
    build_successful: bool = Field(default=False, description="Whether MITRE make build succeeded")
    build_artifacts: Optional[CPSABuildArtifacts] = Field(None, description="Generated verification artifacts")
    trajectory_json_path: Optional[Path] = Field(None, description="Path to the generated trajectory metadata JSON")
    quality_tier: Optional[str] = Field(None, description="Programmatic verification quality tier (GOLD/SILVER/BRONZE/REJECTED)")
    duration_seconds: float = Field(default=0.0, description="Total pipeline execution time")
    cost_usd: float = Field(default=0.0, description="Total estimated LLM cost in USD for this RFC")
    cost_telemetry: dict = Field(default_factory=dict, description="Per-role token and USD cost breakdown")
    error_message: Optional[str] = Field(None, description="Diagnostic error if pipeline halted")


def _extract_rfc_abstract(raw_rfc_text: str) -> str:
    """Extracts the abstract section from the top 120 lines of an RFC document."""
    lines = raw_rfc_text.splitlines()
    for line_idx, line in enumerate(lines[:120]):
        if line.strip().lower() == "abstract":
            return "\n".join(lines[line_idx + 1 : line_idx + 35])
    return ""


def _read_scm_safe(scm_path: Optional[Path]) -> Optional[str]:
    if scm_path and scm_path.exists():
        return scm_path.read_text(encoding="utf-8", errors="replace")
    return None


def _compute_ast_hash(spec: CPSAProtocolSpecification) -> str:
    """Computes a canonical SHA-256 hash of a protocol AST excluding cosmetic prose fields
    (`herald_comment`, `ineligibility_reason`, `description`, `comment`) so text variations
    across repair passes never mask an AST cycle.
    """
    payload = spec.model_dump(exclude={"herald_comment", "ineligibility_reason"})
    for role in payload.get("roles", []):
        role.pop("description", None)
    for skel in payload.get("skeletons", []):
        skel.pop("description", None)
        skel.pop("comment", None)
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def _run_roletran_self_healing_loop(
    protocol_ast: CPSAProtocolSpecification,
    scm_path: Path,
    target_output_dir: Path,
    verbatim_slice: str,
    repair_model_override: Optional[str] = None,
    query_model_override: Optional[str] = None,
) -> Tuple[CPSAProtocolSpecification, Path, RoletranVerificationResult, dict]:
    """Executes Stage 4 Roletran Check and Stage 5 Self-Healing Loop with cycle-aware RAG repair."""
    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=4,
        stage_name="Roletran Check",
        model="cpsa4roletran + cpsa4 -l 1",
    )
    roletran_result = verify_role_executability(scm_path)
    initial_passed = roletran_result.is_executable
    if initial_passed:
        GLOBAL_EVENT_BUS.emit("stage_completed", stage=4, status="passed", model="cpsa4roletran + cpsa4 -l 1")
    else:
        live_repair = resolve_prompt_model(PROMPT_COMPILER_REPAIR, repair_model_override)
        live_query = resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION, query_model_override)
        GLOBAL_EVENT_BUS.emit(
            "stage_started",
            stage=5,
            stage_name="Self-Healing Loop",
            model=f"{live_repair} (RAG: {live_query})",
        )
    attempt = 0
    seen_roletran_hashes = set()
    prev_roletran_diag: Optional[str] = None
    max_attempts = SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS
    repair_attempts_log: List[dict] = []
    stable_stem = scm_path.stem

    while not roletran_result.is_executable and attempt < max_attempts:
        attempt += 1
        ast_hash = _compute_ast_hash(protocol_ast)
        cycle_detected = ast_hash in seen_roletran_hashes
        seen_roletran_hashes.add(ast_hash)

        rejected_ast_snapshot = protocol_ast.model_dump()
        rejected_scm_snapshot = _read_scm_safe(scm_path)
        failed_stderr = roletran_result.raw_stderr
        failed_diag = roletran_result.error_diagnostic
        use_searcher = bool(
            attempt >= 3
            or cycle_detected
            or (attempt == 2 and failed_diag and failed_diag == prev_roletran_diag)
        )
        prev_roletran_diag = failed_diag

        live_repair = resolve_prompt_model(PROMPT_COMPILER_REPAIR, repair_model_override)
        live_query = resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION, query_model_override)
        GLOBAL_EVENT_BUS.emit(
            "repair_attempt",
            stage=5,
            attempt=attempt,
            max_attempts=max_attempts,
            diagnostic=roletran_result.error_diagnostic,
            cycle_detected=cycle_detected,
            model=live_repair,
            query_model=live_query if use_searcher else "Pinned CPSA Header (Direct)",
        )

        logger.warning(
            "Roletran check failed on attempt %d/%d (cycle=%s, searcher=%s): %s. Initiating self-healing repair...",
            attempt,
            max_attempts,
            cycle_detected,
            use_searcher,
            roletran_result.error_diagnostic,
        )
        try:
            protocol_ast = repair_protocol_specification(
                failing_spec=protocol_ast,
                error_diagnostic=roletran_result.error_diagnostic or "Executability verification failure",
                verbatim_slice=verbatim_slice,
                failure_stage="roletran",
                model=repair_model_override,
                query_model=query_model_override,
                cycle_detected=cycle_detected,
                use_agentic_searcher=use_searcher,
            )
            scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir, filename_prefix=stable_stem)
            GLOBAL_EVENT_BUS.emit(
                "stage_completed",
                stage=3,
                scm_path=str(scm_path),
                ast=protocol_ast.model_dump(),
            )
            GLOBAL_EVENT_BUS.emit(
                "compiler_check_started",
                stage=4,
                attempt=attempt,
                binary="cpsa4roletran + cpsa4 -l 1",
                timeout_seconds=SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS,
                model="cpsa4roletran + cpsa4 -l 1",
            )
            roletran_result = verify_role_executability(scm_path)
            repair_meta = compiler_diagnostic_repair.LAST_REPAIR_METADATA
            repair_attempts_log.append({
                "attempt_number": attempt,
                "cycle_detected": cycle_detected,
                "rejected_ast": rejected_ast_snapshot,
                "rejected_scm": rejected_scm_snapshot,
                "raw_stderr": failed_stderr,
                "parsed_diagnostic": failed_diag,
                "rag_query": repair_meta.get("rag_query"),
                "retrieved_chunk_ids": list(repair_meta.get("retrieved_chunk_ids", [])),
                "searcher_diagnosis": repair_meta.get("searcher_diagnosis"),
                "searcher_turns": list(repair_meta.get("searcher_turns", [])),
                "repaired_ast": protocol_ast.model_dump(),
                "repaired_scm": _read_scm_safe(scm_path),
                "passed_after_repair": roletran_result.is_executable,
            })
        except Exception as repair_error:
            logger.error("Self-healing repair exception on attempt %d: %s", attempt, repair_error)
            repair_attempts_log.append({
                "attempt_number": attempt,
                "cycle_detected": cycle_detected,
                "rejected_ast": rejected_ast_snapshot,
                "rejected_scm": rejected_scm_snapshot,
                "raw_stderr": failed_stderr,
                "parsed_diagnostic": failed_diag,
                "rag_query": compiler_diagnostic_repair.LAST_REPAIR_METADATA.get("rag_query"),
                "retrieved_chunk_ids": list(compiler_diagnostic_repair.LAST_REPAIR_METADATA.get("retrieved_chunk_ids", [])),
                "repaired_ast": None,
                "repaired_scm": None,
                "repair_exception": str(repair_error),
                "passed_after_repair": False,
            })
            time.sleep(2)
            continue

    if roletran_result.is_executable:
        logger.info("Roletran executability check passed.")
        GLOBAL_EVENT_BUS.emit("stage_completed", stage=5, status="passed", attempts=attempt)
    else:
        logger.warning(
            "Roletran pre-flight executability check unfulfilled (%s). Proceeding directly to MITRE CPSA solver verification...",
            roletran_result.error_diagnostic,
        )
        GLOBAL_EVENT_BUS.emit(
            "stage_completed",
            stage=5,
            status="unfulfilled",
            diagnostic=roletran_result.error_diagnostic,
            attempts=attempt,
        )

    stage5_record = {
        "validator_binary": roletran_result.validator_binary,
        "roletran_algebra_supported": roletran_result.roletran_algebra_supported,
        "initial_passed": initial_passed,
        "final_passed": roletran_result.is_executable,
        "total_attempts": attempt,
        "compiled_defproc_output": roletran_result.procedural_defproc_code,
        "repair_attempts": repair_attempts_log,
    }
    return protocol_ast, scm_path, roletran_result, stage5_record


def _run_mitre_solver_self_healing_loop(
    protocol_ast: CPSAProtocolSpecification,
    scm_path: Path,
    target_output_dir: Path,
    verbatim_slice: str,
    roletran_result: RoletranVerificationResult,
    repair_model_override: Optional[str] = None,
    query_model_override: Optional[str] = None,
) -> Tuple[CPSAProtocolSpecification, Path, Optional[CPSABuildArtifacts], int, Optional[str], dict]:
    """Executes Stage 6 CPSA Compilation and shape realization with cycle-aware RAG self-healing."""
    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=6,
        stage_name="CPSA Compilation",
        model="cpsa4 + cpsa4graph",
    )
    artifacts: Optional[CPSABuildArtifacts] = None
    build_attempt = 0
    last_build_error: Optional[str] = None
    prev_solver_diag: Optional[str] = None
    seen_solver_hashes = set()
    # If Stage 5 already exhausted its full repair budget (`not roletran_result.is_executable`),
    # try `execute_mitre_make_build` once on `build_attempt == 0` (since `cpsa4` is more permissive
    # than `cpsa4roletran`), and do not run another 10 redundant LLM repair attempts if `cpsa4` also fails.
    max_attempts = SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS if roletran_result.is_executable else 0
    solver_attempts_log: List[dict] = []
    stable_stem = scm_path.stem

    while build_attempt <= max_attempts:
        try:
            if build_attempt > 0 and not roletran_result.is_executable and roletran_result.roletran_algebra_supported:
                raise RuntimeError(
                    f"Pre-flight roletran check rejected repaired model (<15ms syntax/executability gate): "
                    f"{roletran_result.error_diagnostic}"
                )
            GLOBAL_EVENT_BUS.emit(
                "compiler_check_started",
                stage=6,
                attempt=build_attempt,
                binary="cpsa4 + cpsa4graph",
                timeout_seconds=SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS,
                model="cpsa4 + cpsa4graph",
            )
            artifacts = execute_mitre_make_build(scm_path, target_output_dir)
            if artifacts.winning_herald_options:
                protocol_ast.herald_options = list(artifacts.winning_herald_options)
            if solver_attempts_log:
                solver_attempts_log[-1]["passed_after_repair"] = True
            break
        except Exception as build_exc:
            last_build_error = str(build_exc)
            if build_attempt < max_attempts:
                build_attempt += 1
                ast_hash = _compute_ast_hash(protocol_ast)
                cycle_detected = ast_hash in seen_solver_hashes
                seen_solver_hashes.add(ast_hash)

                rejected_ast_snapshot = protocol_ast.model_dump()
                rejected_scm_snapshot = _read_scm_safe(scm_path)
                snowball_detected = is_snowball_state_error(last_build_error)
                use_searcher = bool(
                    snowball_detected
                    or build_attempt >= 3
                    or cycle_detected
                    or (build_attempt == 2 and last_build_error and last_build_error == prev_solver_diag)
                )
                prev_solver_diag = last_build_error

                live_repair = resolve_prompt_model(PROMPT_COMPILER_REPAIR, repair_model_override)
                live_query = resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION, query_model_override)
                GLOBAL_EVENT_BUS.emit(
                    "repair_attempt",
                    stage=6,
                    attempt=build_attempt,
                    max_attempts=max_attempts,
                    diagnostic=last_build_error,
                    cycle_detected=cycle_detected,
                    model=live_repair,
                    query_model=live_query if use_searcher else "Pinned CPSA Header (Direct)",
                )

                logger.warning(
                    "MITRE make build failed (attempt %d/%d, cycle=%s, searcher=%s): %s. Initiating self-healing repair...",
                    build_attempt,
                    max_attempts,
                    cycle_detected,
                    use_searcher,
                    last_build_error,
                )
                try:
                    combined_diagnostic = last_build_error
                    if not roletran_result.is_executable and roletran_result.error_diagnostic:
                        combined_diagnostic = (
                            f"MITRE CPSA make / solver failure:\n{last_build_error}\n\n"
                            f"Pre-flight Roletran Executability Diagnostic:\n{roletran_result.error_diagnostic}"
                        )

                    protocol_ast = repair_protocol_specification(
                        failing_spec=protocol_ast,
                        error_diagnostic=combined_diagnostic,
                        verbatim_slice=verbatim_slice,
                        failure_stage="solver",
                        model=repair_model_override,
                        query_model=query_model_override,
                        cycle_detected=cycle_detected,
                        use_agentic_searcher=use_searcher,
                    )
                    scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir, filename_prefix=stable_stem)
                    GLOBAL_EVENT_BUS.emit(
                        "stage_completed",
                        stage=3,
                        scm_path=str(scm_path),
                        ast=protocol_ast.model_dump(),
                    )
                    roletran_result = verify_role_executability(scm_path)
                    if not roletran_result.is_executable:
                        logger.warning(
                            "Repaired spec failed roletran executability: %s",
                            roletran_result.error_diagnostic,
                        )
                    repair_meta = compiler_diagnostic_repair.LAST_REPAIR_METADATA
                    solver_attempts_log.append({
                        "attempt_number": build_attempt,
                        "cycle_detected": cycle_detected,
                        "rejected_ast": rejected_ast_snapshot,
                        "rejected_scm": rejected_scm_snapshot,
                        "raw_stderr": last_build_error,
                        "parsed_diagnostic": combined_diagnostic,
                        "rag_query": repair_meta.get("rag_query"),
                        "retrieved_chunk_ids": list(repair_meta.get("retrieved_chunk_ids", [])),
                        "repaired_ast": protocol_ast.model_dump(),
                        "repaired_scm": _read_scm_safe(scm_path),
                        "passed_after_repair": False,
                    })
                except Exception as repair_error:
                    logger.error("Build self-healing exception on attempt %d: %s", build_attempt, repair_error)
                    solver_attempts_log.append({
                        "attempt_number": build_attempt,
                        "cycle_detected": cycle_detected,
                        "rejected_ast": rejected_ast_snapshot,
                        "rejected_scm": rejected_scm_snapshot,
                        "raw_stderr": last_build_error,
                        "parsed_diagnostic": last_build_error,
                        "rag_query": compiler_diagnostic_repair.LAST_REPAIR_METADATA.get("rag_query"),
                        "retrieved_chunk_ids": list(compiler_diagnostic_repair.LAST_REPAIR_METADATA.get("retrieved_chunk_ids", [])),
                        "repaired_ast": None,
                        "repaired_scm": None,
                        "repair_exception": str(repair_error),
                        "passed_after_repair": False,
                    })
                    time.sleep(2)
                    continue
            else:
                break

    stage6_record = {
        "validator_binary": "cpsa4",
        "initial_passed": build_attempt == 0 and artifacts is not None,
        "final_passed": artifacts is not None,
        "total_attempts": build_attempt,
        "repair_attempts": solver_attempts_log,
    }
    return protocol_ast, scm_path, artifacts, build_attempt, last_build_error, stage6_record


def run_rfc_translation_pipeline(
    rfc_file_path: Path,
    output_dir: Optional[Path] = None,
    router_model: Optional[str] = None,
    extraction_model: Optional[str] = None,
    repair_model: Optional[str] = None,
    query_model: Optional[str] = None,
    run_root_dir: Optional[Path] = None,
) -> PipelineExecutionSummary:
    """Executes the end-to-end RFC to formally verified MITRE CPSA synthesis pipeline."""
    start_time = time.time()
    rfc_id = rfc_file_path.stem.upper()

    if output_dir is not None:
        target_output_dir = output_dir
        effective_run_root = run_root_dir or output_dir.parent
    else:
        run_ts = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        effective_run_root = run_root_dir or (SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR / f"run_{run_ts}")
        target_output_dir = effective_run_root / rfc_file_path.stem.lower()

    # Configure console/global logger first; defer creating per-RFC output directory and run.log
    # until the RFC passes Stage 1a/1c eligibility so batch runs don't create 9,400+ empty folders.
    configure_pipeline_logging(run_log_file=None)
    csv_recorder = PipelineMetricsCSVLogger()
    repair_override = repair_model or extraction_model
    active_router_model = resolve_prompt_model(PROMPT_APPLICABILITY_GATE, router_model)
    active_extraction_model = resolve_prompt_model(PROMPT_PROTOCOL_EXTRACTION, extraction_model)
    active_repair_model = resolve_prompt_model(PROMPT_COMPILER_REPAIR, repair_override)
    active_query_model = resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION, query_model)

    logger.info("================================================================")
    logger.info("Starting RFC-LLM Synthesis Pipeline for: %s", rfc_file_path.name)
    logger.info("================================================================")

    from src.cost_tracker import GLOBAL_COST_TRACKER
    GLOBAL_COST_TRACKER.start_rfc(
        rfc_id=rfc_id,
        router_model=active_router_model,
        extraction_model=active_extraction_model,
        query_model=active_query_model,
        repair_model=active_repair_model,
    )
    GLOBAL_EVENT_BUS.set_run_directory(effective_run_root, is_live=True)
    GLOBAL_EVENT_BUS.start_rfc(rfc_id=rfc_id, rfc_file=rfc_file_path.name)
    GLOBAL_EVENT_BUS.emit(
        "pipeline_started",
        rfc_id=rfc_id,
        rfc_file=rfc_file_path.name,
        router_model=active_router_model,
        extraction_model=active_extraction_model,
        repair_model=active_repair_model,
        query_model=active_query_model,
    )

    if not rfc_file_path.exists():
        error_msg = f"RFC source file not found: {rfc_file_path}"
        logger.error(error_msg)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=error_msg)
        return PipelineExecutionSummary(rfc_id=rfc_id, is_eligible=False, error_message=error_msg)

    with open(rfc_file_path, "r", encoding="utf-8", errors="ignore") as rfc_file:
        raw_rfc_text = rfc_file.read()

    # -------------------------------------------------------------------------
    # STAGE 1a: Tier 0 Header Filter (Document Intake)
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=1,
        stage_name="Document Intake",
        model=active_router_model,
    )
    header_filter_result = filter_rfc_header(raw_rfc_text)
    if not header_filter_result.is_eligible:
        elapsed = time.time() - start_time
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            status="INELIGIBLE",
            quality_tier="INELIGIBLE",
            rejection_gate="Tier 0 Header Filter",
            protocol_name=header_filter_result.title,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            error_message=header_filter_result.disqualification_reason,
        )
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=header_filter_result.rfc_id or rfc_id,
            protocol_name=header_filter_result.title,
            rfc_dir=target_output_dir,
            scm_path=None,
            trajectory_json_path=None,
            quality_tier="INELIGIBLE",
            is_eligible=False,
            build_successful=False,
            error_message=header_filter_result.disqualification_reason,
            rejection_gate="Tier 0 Header Filter",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.register_filtered_rfc(
            rfc_id=header_filter_result.rfc_id or rfc_id,
            title=header_filter_result.title or rfc_file_path.name,
            gate="Tier 0 Header Filter",
            reason=header_filter_result.disqualification_reason or "Disqualified by Tier 0 header filter",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, reason=header_filter_result.disqualification_reason)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            is_eligible=False,
            duration_seconds=elapsed,
            error_message=header_filter_result.disqualification_reason,
        )

    rfc_number_str = header_filter_result.rfc_id or rfc_id
    protocol_title = header_filter_result.title or "Unknown Protocol"

    # -------------------------------------------------------------------------
    # STAGE 1b: Full TOC Parsing & Abstract Extraction
    # -------------------------------------------------------------------------
    toc_entries = parse_table_of_contents(raw_rfc_text)
    abstract_text = _extract_rfc_abstract(raw_rfc_text)

    # -------------------------------------------------------------------------
    # STAGE 1c: Tier 1 Applicability Gate
    # -------------------------------------------------------------------------
    applicability_report = evaluate_protocol_applicability(
        rfc_id=rfc_number_str,
        title=protocol_title,
        category=header_filter_result.category or "Unknown",
        abstract=abstract_text,
        toc_entries=toc_entries,
        model=router_model,
    )

    if not applicability_report.is_cryptographic_protocol:
        elapsed = time.time() - start_time
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            status="INELIGIBLE",
            quality_tier="INELIGIBLE",
            rejection_gate="Stage 1c Applicability Gate",
            protocol_name=applicability_report.protocol_name or protocol_title,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            error_message=f"Ineligible: {applicability_report.rationale}",
        )
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=rfc_number_str,
            protocol_name=applicability_report.protocol_name or protocol_title,
            rfc_dir=target_output_dir,
            scm_path=None,
            trajectory_json_path=None,
            quality_tier="INELIGIBLE",
            is_eligible=False,
            build_successful=False,
            error_message=applicability_report.rationale,
            rejection_gate="Stage 1c Applicability Gate",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.register_filtered_rfc(
            rfc_id=rfc_number_str,
            title=applicability_report.protocol_name or protocol_title,
            gate="Stage 1c Applicability Gate",
            reason=applicability_report.rationale or "Disqualified by Stage 1c applicability gate",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, reason=applicability_report.rationale)
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix="Ineligible RFC Cost"))
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=applicability_report.protocol_name or protocol_title,
            is_eligible=False,
            duration_seconds=elapsed,
            cost_usd=float(rfc_cost_summary.get("total_cost_usd", 0.0)),
            cost_telemetry=rfc_cost_summary,
            error_message=applicability_report.rationale,
        )

    # Eligible cryptographic protocol confirmed: create per-RFC output directory, run.log, and numbered tab
    target_output_dir.mkdir(parents=True, exist_ok=True)
    run_log_path = target_output_dir / "run.log"
    configure_pipeline_logging(run_log_file=run_log_path)
    final_protocol_name = applicability_report.protocol_name or protocol_title
    tab_index = GLOBAL_EVENT_BUS.register_accepted_tab(
        rfc_id=rfc_number_str,
        protocol_name=final_protocol_name,
        rfc_dir=target_output_dir,
        rfc_title=protocol_title,
    )
    logger.info("Eligible Cryptographic Protocol Confirmed [Tab #%d]: %s (%s)", tab_index, rfc_number_str, final_protocol_name)
    logger.info("Output Directory: %s", target_output_dir)

    GLOBAL_EVENT_BUS.emit("stage_completed", stage=1, protocol_name=final_protocol_name, rfc_id=rfc_number_str, tab_index=tab_index)

    # -------------------------------------------------------------------------
    # STAGE 1d & 1e: Exchange Section Routing & Verbatim Slicing
    # -------------------------------------------------------------------------
    target_sections = route_handshake_sections(
        rfc_id=rfc_number_str,
        protocol_name=final_protocol_name,
        toc_entries=toc_entries,
        model=router_model,
    )

    verbatim_slice = slice_verbatim_sections(raw_rfc_text, target_sections)
    slice_lines_count = len(verbatim_slice.splitlines())

    slice_file = target_output_dir / "verbatim_slice.txt"
    with open(slice_file, "w", encoding="utf-8") as slice_handle:
        slice_handle.write(verbatim_slice)

    GLOBAL_EVENT_BUS.update_accepted_tab(tab_index, slice_path=str(slice_file))
    GLOBAL_EVENT_BUS.emit(
        "slice_ready",
        sections=target_sections,
        line_count=slice_lines_count,
        slice_path=str(slice_file),
    )

    # -------------------------------------------------------------------------
    # STAGE 2: JSON CPSA Generation
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=2,
        stage_name="JSON CPSA Generation",
        model=resolve_prompt_model(PROMPT_PROTOCOL_EXTRACTION, extraction_model),
    )
    try:
        protocol_ast = extract_protocol_specification(
            verbatim_slice=verbatim_slice,
            protocol_name=final_protocol_name,
            principals=applicability_report.participating_principals,
            model=extraction_model,
        )
        GLOBAL_EVENT_BUS.emit(
            "stage_completed",
            stage=2,
            roles_count=len(protocol_ast.roles),
            skeletons_count=len(protocol_ast.skeletons),
            ast=protocol_ast.model_dump(),
        )
    except Exception as extraction_exc:
        elapsed = time.time() - start_time
        error_msg = f"Extraction failed: {extraction_exc}"
        logger.error(error_msg)
        extraction_meta = constrained_protocol_extractor.LAST_EXTRACTION_METADATA
        failed_stage2_record = {
            "schema_self_correction_triggered": bool(extraction_meta.get("schema_self_correction_triggered", False)),
            "schema_validation_error": extraction_meta.get("schema_validation_error") or str(extraction_exc),
            "initial_ast": None,
            "initial_scm": None,
        }
        empty_stage5 = {
            "validator_binary": "cpsa4roletran",
            "roletran_algebra_supported": True,
            "initial_passed": False,
            "final_passed": False,
            "total_attempts": 0,
            "compiled_defproc_output": None,
            "repair_attempts": [],
        }
        empty_stage6 = {
            "validator_binary": "cpsa4",
            "initial_passed": False,
            "final_passed": False,
            "total_attempts": 0,
            "repair_attempts": [],
        }
        trajectory_path = write_trajectory_metadata_bundle(
            output_dir=target_output_dir,
            rfc_id=rfc_number_str,
            rfc_title=protocol_title,
            protocol_name=final_protocol_name,
            participating_principals=applicability_report.participating_principals,
            selected_sections=target_sections,
            verbatim_slice=verbatim_slice,
            duration_seconds=elapsed,
            stage2_record=failed_stage2_record,
            stage5_record=empty_stage5,
            stage6_record=empty_stage6,
            final_spec=None,
            final_scm_path=None,
            trace_txt_path=None,
            shapes_txt_path=None,
            solver_passed=False,
        )
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=rfc_number_str,
            protocol_name=final_protocol_name,
            rfc_dir=target_output_dir,
            scm_path=None,
            trajectory_json_path=trajectory_path,
            quality_tier="REJECTED",
            is_eligible=True,
            build_successful=False,
            error_message=error_msg,
            tab_index=tab_index,
        )
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        schema_repairs_stage2 = 1 if failed_stage2_record["schema_self_correction_triggered"] else 0
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            status="FAILED",
            quality_tier="REJECTED",
            protocol_name=final_protocol_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            schema_repairs=schema_repairs_stage2,
            total_repairs=schema_repairs_stage2,
            total_completion_steps=1 + schema_repairs_stage2,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            trajectory_json_path=trajectory_path,
            error_message=error_msg,
        )
        logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix="RFC Run Cost"))
        GLOBAL_EVENT_BUS.update_accepted_tab(
            tab_index,
            status="FAILED",
            quality_tier="REJECTED",
            duration_seconds=round(elapsed, 2),
            cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
            cost_telemetry=rfc_cost_summary,
            trajectory_path=str(trajectory_path),
            error_message=error_msg,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=2, error_message=error_msg)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=error_msg)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_protocol_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            trajectory_json_path=trajectory_path,
            quality_tier="REJECTED",
            duration_seconds=elapsed,
            cost_usd=float(rfc_cost_summary.get("total_cost_usd", 0.0)),
            cost_telemetry=rfc_cost_summary,
            error_message=error_msg,
        )

    # -------------------------------------------------------------------------
    # STAGE 2b: Verbatim Slice Verification Gate (False-Positive Bailout)
    # -------------------------------------------------------------------------
    if (
        not protocol_ast.is_verifiable_protocol
        or not protocol_ast.roles
        or not protocol_ast.has_cryptographic_primitives()
    ):
        elapsed = time.time() - start_time
        ineligible_reason = (
            protocol_ast.ineligibility_reason
            or "Stage 2 Verbatim Slice Gate: RFC slice contains no verifiable cryptographic message exchange."
        )
        logger.warning(
            "Stage 2 Verbatim Slice Gate rejected '%s' (%s) with 0 repair loops: %s",
            rfc_number_str,
            final_protocol_name,
            ineligible_reason,
        )
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        extraction_meta = constrained_protocol_extractor.LAST_EXTRACTION_METADATA
        schema_repairs_stage2 = 1 if extraction_meta.get("schema_self_correction_triggered") else 0
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            status="INELIGIBLE",
            quality_tier="INELIGIBLE",
            rejection_gate="Stage 2 Verbatim Slice Gate",
            protocol_name=final_protocol_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            schema_repairs=schema_repairs_stage2,
            total_repairs=schema_repairs_stage2,
            total_completion_steps=1 + schema_repairs_stage2,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            error_message=ineligible_reason,
        )
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=rfc_number_str,
            protocol_name=final_protocol_name,
            rfc_dir=target_output_dir,
            scm_path=None,
            trajectory_json_path=None,
            quality_tier="INELIGIBLE",
            is_eligible=False,
            build_successful=False,
            error_message=ineligible_reason,
            tab_index=tab_index,
            rejection_gate="Stage 2 Verbatim Slice Gate",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.register_filtered_rfc(
            rfc_id=rfc_number_str,
            title=final_protocol_name,
            gate="Stage 2 Verbatim Slice Gate",
            reason=ineligible_reason,
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.update_accepted_tab(
            tab_index,
            status="INELIGIBLE",
            quality_tier="INELIGIBLE",
            duration_seconds=round(elapsed, 2),
            cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
            cost_telemetry=rfc_cost_summary,
            error_message=ineligible_reason,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=2, reason=ineligible_reason)
        logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix="Stage 2 Filtered RFC Cost"))
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_protocol_name,
            is_eligible=False,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            quality_tier="INELIGIBLE",
            duration_seconds=elapsed,
            cost_usd=float(rfc_cost_summary.get("total_cost_usd", 0.0)),
            cost_telemetry=rfc_cost_summary,
            error_message=ineligible_reason,
        )

    # -------------------------------------------------------------------------
    # STAGE 3: CPSA4json -> scm
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=3,
        stage_name="CPSA4json -> scm",
        model="cpsa_scheme_emitter.py",
    )
    scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir)
    GLOBAL_EVENT_BUS.update_accepted_tab(
        tab_index,
        protocol_name=protocol_ast.protocol_name or final_protocol_name,
        scm_path=str(scm_path),
    )
    GLOBAL_EVENT_BUS.emit("stage_completed", stage=3, scm_path=str(scm_path))

    extraction_meta = constrained_protocol_extractor.LAST_EXTRACTION_METADATA
    stage2_record = {
        "schema_self_correction_triggered": bool(extraction_meta.get("schema_self_correction_triggered", False)),
        "schema_validation_error": extraction_meta.get("schema_validation_error"),
        "initial_ast": protocol_ast.model_dump(),
        "initial_scm": _read_scm_safe(scm_path),
    }

    # -------------------------------------------------------------------------
    # STAGE 4 & 5: Roletran Check (<15 ms) & Self-Healing Loop
    # -------------------------------------------------------------------------
    protocol_ast, scm_path, roletran_result, stage5_record = _run_roletran_self_healing_loop(
        protocol_ast=protocol_ast,
        scm_path=scm_path,
        target_output_dir=target_output_dir,
        verbatim_slice=verbatim_slice,
        repair_model_override=repair_override,
        query_model_override=query_model,
    )

    # -------------------------------------------------------------------------
    # STAGE 6: CPSA Compilation (60s cap) with RAG Self-Healing Loop
    # -------------------------------------------------------------------------
    protocol_ast, scm_path, artifacts, build_attempt, last_build_error, stage6_record = _run_mitre_solver_self_healing_loop(
        protocol_ast=protocol_ast,
        scm_path=scm_path,
        target_output_dir=target_output_dir,
        verbatim_slice=verbatim_slice,
        roletran_result=roletran_result,
        repair_model_override=repair_override,
        query_model_override=query_model,
    )

    elapsed = time.time() - start_time
    stem = scm_path.stem
    trace_txt_candidate = artifacts.trace_txt_path if artifacts else (target_output_dir / f"{stem}.txt")
    shapes_txt_candidate = artifacts.shapes_txt_path if artifacts else (target_output_dir / f"{stem}_shapes.txt")

    trajectory_path = write_trajectory_metadata_bundle(
        output_dir=target_output_dir,
        rfc_id=rfc_number_str,
        rfc_title=protocol_title,
        protocol_name=final_protocol_name,
        participating_principals=applicability_report.participating_principals,
        selected_sections=target_sections,
        verbatim_slice=verbatim_slice,
        duration_seconds=elapsed,
        stage2_record=stage2_record,
        stage5_record=stage5_record,
        stage6_record=stage6_record,
        final_spec=protocol_ast,
        final_scm_path=scm_path,
        trace_txt_path=trace_txt_candidate if trace_txt_candidate.exists() else None,
        shapes_txt_path=shapes_txt_candidate if shapes_txt_candidate.exists() else None,
        solver_passed=artifacts is not None,
    )

    quality_tier = "REJECTED"
    all_povs_multi_strand: Optional[bool] = None
    secrecy_proved: Optional[bool] = None
    explored_skeletons_count = 0
    try:
        traj_data = json.loads(trajectory_path.read_text(encoding="utf-8"))
        qa = traj_data.get("quality_assessment", {})
        quality_tier = qa.get("quality_tier", "REJECTED")
        all_povs_multi_strand = qa.get("all_participant_povs_multi_strand")
        secrecy_proved = qa.get("all_secrecy_listeners_unrealized")
        explored_skeletons_count = int(
            traj_data.get("stage6_cpsa4_solver", {})
            .get("exploration_telemetry_from_txt", {})
            .get("total_explored_labels", 0)
        )
    except Exception:
        pass

    schema_repairs = 1 if stage2_record.get("schema_self_correction_triggered") else 0
    roletran_repairs = int(stage5_record.get("total_attempts", 0))
    solver_repairs = int(stage6_record.get("total_attempts", 0))
    total_repairs = schema_repairs + roletran_repairs + solver_repairs
    total_completion_steps = 1 + total_repairs
    all_repair_attempts = list(stage5_record.get("repair_attempts", [])) + list(
        stage6_record.get("repair_attempts", [])
    )
    searcher_invocations = sum(
        1
        for att in all_repair_attempts
        if att.get("rag_query") or att.get("retrieved_chunk_ids")
    )

    if artifacts is None:
        error_msg = f"MITRE make build failed after {build_attempt} repair attempts: {last_build_error}"
        logger.error(error_msg)
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=rfc_number_str,
            protocol_name=final_protocol_name,
            rfc_dir=target_output_dir,
            scm_path=scm_path,
            trajectory_json_path=trajectory_path,
            quality_tier=quality_tier,
            is_eligible=True,
            build_successful=False,
            error_message=error_msg,
            tab_index=tab_index,
        )
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            status="PARTIAL" if roletran_result.is_executable else "FAILED",
            quality_tier=quality_tier,
            protocol_name=final_protocol_name,
            message_algebra=protocol_ast.message_algebra,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            role_count=len(protocol_ast.roles),
            preskeleton_count=len(protocol_ast.skeletons),
            roletran_passed=roletran_result.is_executable,
            solver_passed=False,
            shapes_count=0,
            explored_skeletons_count=explored_skeletons_count,
            all_povs_multi_strand=all_povs_multi_strand,
            secrecy_proved=secrecy_proved,
            zero_shot_passed=False,
            schema_repairs=schema_repairs,
            roletran_repairs=roletran_repairs,
            solver_repairs=solver_repairs,
            total_repairs=total_repairs,
            total_completion_steps=total_completion_steps,
            searcher_invocations=searcher_invocations,
            herald_options=protocol_ast.herald_options,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            scm_path=scm_path,
            shapes_xhtml_path=None,
            trajectory_json_path=trajectory_path,
            error_message=error_msg,
        )
        logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix=f"Cost Summary ({rfc_id})"))
        GLOBAL_EVENT_BUS.update_accepted_tab(
            tab_index,
            protocol_name=protocol_ast.protocol_name or final_protocol_name,
            status="PARTIAL" if roletran_result.is_executable else "FAILED",
            quality_tier=quality_tier,
            total_attempts=total_repairs,
            duration_seconds=round(elapsed, 2),
            cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
            cost_telemetry=rfc_cost_summary,
            scm_path=str(scm_path),
            trajectory_path=str(trajectory_path),
            error_message=error_msg,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=6, error_message=error_msg)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=error_msg)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_protocol_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            roletran_passed=roletran_result.is_executable,
            build_successful=False,
            trajectory_json_path=trajectory_path,
            quality_tier=quality_tier,
            duration_seconds=elapsed,
            cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
            cost_telemetry=rfc_cost_summary,
            error_message=error_msg,
        )

    update_run_metadata_index(
        run_root_dir=effective_run_root,
        rfc_id=rfc_number_str,
        protocol_name=final_protocol_name,
        rfc_dir=target_output_dir,
        scm_path=scm_path,
        trajectory_json_path=trajectory_path,
        quality_tier=quality_tier,
        is_eligible=True,
        build_successful=True,
        error_message=None,
        tab_index=tab_index,
    )

    rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
    GLOBAL_EVENT_BUS.update_accepted_tab(
        tab_index,
        protocol_name=protocol_ast.protocol_name or final_protocol_name,
        status="VERIFIED",
        quality_tier=quality_tier,
        total_attempts=total_repairs,
        shapes_count=artifacts.shapes_count,
        duration_seconds=round(elapsed, 2),
        cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
        cost_telemetry=rfc_cost_summary,
        scm_path=str(scm_path),
        trajectory_path=str(trajectory_path),
        shapes_xhtml=str(artifacts.shapes_graph_xhtml_path),
        error_message=None,
    )

    csv_recorder.log_run(
        rfc_id=rfc_id,
        is_eligible=True,
        status="VERIFIED",
        quality_tier=quality_tier,
        protocol_name=final_protocol_name,
        message_algebra=protocol_ast.message_algebra,
        selected_sections=target_sections,
        sliced_lines_count=slice_lines_count,
        role_count=len(protocol_ast.roles),
        preskeleton_count=len(protocol_ast.skeletons),
        roletran_passed=roletran_result.is_executable,
        solver_passed=True,
        shapes_count=artifacts.shapes_count,
        explored_skeletons_count=explored_skeletons_count,
        all_povs_multi_strand=all_povs_multi_strand,
        secrecy_proved=secrecy_proved,
        zero_shot_passed=(total_repairs == 0),
        schema_repairs=schema_repairs,
        roletran_repairs=roletran_repairs,
        solver_repairs=solver_repairs,
        total_repairs=total_repairs,
        total_completion_steps=total_completion_steps,
        searcher_invocations=searcher_invocations,
        herald_options=protocol_ast.herald_options,
        duration_seconds=elapsed,
        cost_telemetry=rfc_cost_summary,
        router_model=active_router_model,
        extraction_model=active_extraction_model,
        query_model=active_query_model,
        repair_model=active_repair_model,
        scm_path=scm_path,
        shapes_xhtml_path=artifacts.shapes_graph_xhtml_path,
        trajectory_json_path=trajectory_path,
        error_message=None,
    )

    logger.info("================================================================")
    logger.info("Pipeline Complete for %s in %.2fs! (Quality Tier: %s)", rfc_id, elapsed, quality_tier)
    logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix=f"Cost Summary ({rfc_id})"))
    logger.info("Generated: %s", artifacts.shapes_graph_xhtml_path)
    logger.info("Trajectory Metadata: %s", trajectory_path)
    logger.info("Master Run Index: %s", effective_run_root / "metadata_index.json")
    logger.info("================================================================")

    GLOBAL_EVENT_BUS.emit(
        "pipeline_completed",
        success=True,
        protocol_name=final_protocol_name,
        duration_seconds=elapsed,
        shapes_count=artifacts.shapes_count,
        quality_tier=quality_tier,
        cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
        cost_telemetry=rfc_cost_summary,
        trajectory_json=str(trajectory_path),
        shapes_xhtml=str(artifacts.shapes_graph_xhtml_path),
        shapes_txt=str(artifacts.shapes_txt_path),
        scm_path=str(scm_path),
    )

    return PipelineExecutionSummary(
        rfc_id=rfc_id,
        protocol_name=final_protocol_name,
        is_eligible=True,
        selected_sections=target_sections,
        sliced_lines_count=slice_lines_count,
        roletran_passed=roletran_result.is_executable,
        build_successful=True,
        build_artifacts=artifacts,
        trajectory_json_path=trajectory_path,
        quality_tier=quality_tier,
        duration_seconds=elapsed,
        cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
        cost_telemetry=rfc_cost_summary,
    )
