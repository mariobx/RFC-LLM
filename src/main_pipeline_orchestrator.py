"""Main Pipeline Orchestrator for RFC-to-CPSA Synthesis.

Coordinates the 6-stage synthesis pipeline for a single RFC document:
- Stage 1: Tier 0 Header Filter, TOC Parsing, Tier 1 Applicability Gate,
           Exchange Section Routing, and Verbatim Section Slicing.
- Stage 2: Constrained Protocol Extraction (with RAG grounding & 1-shot schema correction).
- Stage 3 & 4: CPSA JSON Serialization and Scheme S-Expression Emission (`cpsa4json`).
- Stage 5: Pre-Flight Roletran Executability Gate (`cpsa4roletran` / `cpsa4 -l 1`) with RAG Self-Healing.
- Stage 6: MITRE CPSA Solver & Shapes Realization (`make` / `cpsa4` / `cpsa4shapes` / `cpsa4graph`) with RAG Self-Healing.
"""

import hashlib
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
from src.semantic_extraction.constrained_protocol_extractor import extract_protocol_specification
from src.system_config import SYSTEM_CONFIG
from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification
from src.verification_engine.mitre_build_orchestrator import (
    CPSABuildArtifacts,
    execute_mitre_make_build,
)
from src.verification_engine.roletran_executability_gate import (
    RoletranVerificationResult,
    verify_role_executability,
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
    duration_seconds: float = Field(default=0.0, description="Total pipeline execution time")
    error_message: Optional[str] = Field(None, description="Diagnostic error if pipeline halted")


def _extract_rfc_abstract(raw_rfc_text: str) -> str:
    """Extracts the abstract section from the top 120 lines of an RFC document."""
    lines = raw_rfc_text.splitlines()
    for line_idx, line in enumerate(lines[:120]):
        if line.strip().lower() == "abstract":
            return "\n".join(lines[line_idx + 1 : line_idx + 35])
    return ""


def _run_roletran_self_healing_loop(
    protocol_ast: CPSAProtocolSpecification,
    scm_path: Path,
    target_output_dir: Path,
    verbatim_slice: str,
    active_repair_model: str,
    active_query_model: str,
) -> Tuple[CPSAProtocolSpecification, Path, RoletranVerificationResult]:
    """Executes Stage 5 Roletran pre-flight executability verification with cycle-aware RAG self-healing."""
    GLOBAL_EVENT_BUS.emit("stage_started", stage=5, stage_name="Roletran Executability Verification")
    roletran_result = verify_role_executability(scm_path)
    attempt = 0
    seen_roletran_hashes = set()
    max_attempts = SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS

    while not roletran_result.is_executable and attempt < max_attempts:
        attempt += 1
        ast_hash = hashlib.sha256(protocol_ast.model_dump_json().encode()).hexdigest()
        cycle_detected = ast_hash in seen_roletran_hashes
        seen_roletran_hashes.add(ast_hash)

        GLOBAL_EVENT_BUS.emit(
            "repair_attempt",
            stage=5,
            attempt=attempt,
            max_attempts=max_attempts,
            diagnostic=roletran_result.error_diagnostic,
            cycle_detected=cycle_detected,
        )

        logger.warning(
            "Roletran check failed on attempt %d/%d (cycle=%s): %s. Initiating fast self-healing repair...",
            attempt,
            max_attempts,
            cycle_detected,
            roletran_result.error_diagnostic,
        )
        try:
            protocol_ast = repair_protocol_specification(
                failing_spec=protocol_ast,
                error_diagnostic=roletran_result.error_diagnostic or "Executability verification failure",
                verbatim_slice=verbatim_slice,
                failure_stage="roletran",
                model=active_repair_model,
                query_model=active_query_model,
                cycle_detected=cycle_detected,
            )
            scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir)
            roletran_result = verify_role_executability(scm_path)
        except Exception as repair_error:
            logger.error("Self-healing repair exception on attempt %d: %s", attempt, repair_error)
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

    return protocol_ast, scm_path, roletran_result


def _run_mitre_solver_self_healing_loop(
    protocol_ast: CPSAProtocolSpecification,
    scm_path: Path,
    target_output_dir: Path,
    verbatim_slice: str,
    roletran_result: RoletranVerificationResult,
    active_repair_model: str,
    active_query_model: str,
) -> Tuple[CPSAProtocolSpecification, Path, Optional[CPSABuildArtifacts], int, Optional[str]]:
    """Executes Stage 6 MITRE CPSA make build and shape realization with cycle-aware RAG self-healing."""
    GLOBAL_EVENT_BUS.emit("stage_started", stage=6, stage_name="MITRE Build & Shapes Exploration")
    artifacts: Optional[CPSABuildArtifacts] = None
    build_attempt = 0
    last_build_error: Optional[str] = None
    seen_solver_hashes = set()
    max_attempts = SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS

    while build_attempt <= max_attempts:
        try:
            artifacts = execute_mitre_make_build(scm_path, target_output_dir)
            break
        except Exception as build_exc:
            last_build_error = str(build_exc)
            if build_attempt < max_attempts:
                build_attempt += 1
                ast_hash = hashlib.sha256(protocol_ast.model_dump_json().encode()).hexdigest()
                cycle_detected = ast_hash in seen_solver_hashes
                seen_solver_hashes.add(ast_hash)

                GLOBAL_EVENT_BUS.emit(
                    "repair_attempt",
                    stage=6,
                    attempt=build_attempt,
                    max_attempts=max_attempts,
                    diagnostic=last_build_error,
                    cycle_detected=cycle_detected,
                )

                logger.warning(
                    "MITRE make build failed (attempt %d/%d, cycle=%s): %s. Initiating RAG self-healing repair...",
                    build_attempt,
                    max_attempts,
                    cycle_detected,
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
                        model=active_repair_model,
                        query_model=active_query_model,
                        cycle_detected=cycle_detected,
                    )
                    scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir)
                    roletran_result = verify_role_executability(scm_path)
                    if not roletran_result.is_executable:
                        logger.warning(
                            "Repaired spec failed roletran executability: %s",
                            roletran_result.error_diagnostic,
                        )
                except Exception as repair_error:
                    logger.error("Build self-healing exception on attempt %d: %s", build_attempt, repair_error)
                    time.sleep(2)
                    continue
            else:
                break

    return protocol_ast, scm_path, artifacts, build_attempt, last_build_error


def run_rfc_translation_pipeline(
    rfc_file_path: Path,
    output_dir: Optional[Path] = None,
    router_model: Optional[str] = None,
    extraction_model: Optional[str] = None,
    repair_model: Optional[str] = None,
    query_model: Optional[str] = None,
) -> PipelineExecutionSummary:
    """Executes the end-to-end RFC to formally verified MITRE CPSA synthesis pipeline."""
    start_time = time.time()
    rfc_id = rfc_file_path.stem.upper()

    target_output_dir = output_dir or (SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR / rfc_file_path.stem.lower())
    target_output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize per-run logger and CSV metrics recorder
    run_log_path = target_output_dir / "run.log"
    configure_pipeline_logging(run_log_file=run_log_path)
    csv_recorder = PipelineMetricsCSVLogger()
    active_repair_model = repair_model or extraction_model or SYSTEM_CONFIG.DEFAULT_REPAIR_MODEL
    active_query_model = query_model or SYSTEM_CONFIG.DEFAULT_QUERY_MODEL

    logger.info("================================================================")
    logger.info("Starting RFC-LLM Synthesis Pipeline for: %s", rfc_file_path.name)
    logger.info("Output Directory: %s", target_output_dir)
    logger.info("================================================================")

    GLOBAL_EVENT_BUS.emit("pipeline_started", rfc_id=rfc_id, rfc_file=rfc_file_path.name)

    if not rfc_file_path.exists():
        error_msg = f"RFC source file not found: {rfc_file_path}"
        logger.error(error_msg)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=error_msg)
        return PipelineExecutionSummary(rfc_id=rfc_id, is_eligible=False, error_message=error_msg)

    with open(rfc_file_path, "r", encoding="utf-8", errors="ignore") as rfc_file:
        raw_rfc_text = rfc_file.read()

    # -------------------------------------------------------------------------
    # STAGE 1a: Tier 0 Header Filter
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=1, stage_name="Document Intake & Applicability Gate")
    header_filter_result = filter_rfc_header(raw_rfc_text)
    if not header_filter_result.is_eligible:
        elapsed = time.time() - start_time
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            error_message=header_filter_result.disqualification_reason,
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
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            protocol_name=applicability_report.protocol_name or protocol_title,
            error_message=f"Ineligible: {applicability_report.rationale}",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, reason=applicability_report.rationale)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=applicability_report.protocol_name or protocol_title,
            is_eligible=False,
            duration_seconds=elapsed,
            error_message=applicability_report.rationale,
        )

    final_protocol_name = applicability_report.protocol_name or protocol_title
    GLOBAL_EVENT_BUS.emit("stage_completed", stage=1, protocol_name=final_protocol_name)

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

    GLOBAL_EVENT_BUS.emit(
        "slice_ready",
        sections=target_sections,
        line_count=slice_lines_count,
        slice_path=str(slice_file),
    )

    # -------------------------------------------------------------------------
    # STAGE 2: Constrained Protocol Extraction
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=2, stage_name="Constrained Protocol Extraction")
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
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            protocol_name=final_protocol_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            duration_seconds=elapsed,
            error_message=error_msg,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=2, error_message=error_msg)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_protocol_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            duration_seconds=elapsed,
            error_message=error_msg,
        )

    # -------------------------------------------------------------------------
    # STAGE 3 & 4: Scheme SCM Emission
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=3, stage_name="CPSA Scheme Code Generation")
    scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir)
    GLOBAL_EVENT_BUS.emit("stage_completed", stage=3, scm_path=str(scm_path))

    # -------------------------------------------------------------------------
    # STAGE 5: Roletran Executability Gate (<15 ms) with RAG Self-Healing Loop
    # -------------------------------------------------------------------------
    protocol_ast, scm_path, roletran_result = _run_roletran_self_healing_loop(
        protocol_ast=protocol_ast,
        scm_path=scm_path,
        target_output_dir=target_output_dir,
        verbatim_slice=verbatim_slice,
        active_repair_model=active_repair_model,
        active_query_model=active_query_model,
    )

    # -------------------------------------------------------------------------
    # STAGE 6: MITRE Build Orchestration with RAG Self-Healing Loop
    # -------------------------------------------------------------------------
    protocol_ast, scm_path, artifacts, build_attempt, last_build_error = _run_mitre_solver_self_healing_loop(
        protocol_ast=protocol_ast,
        scm_path=scm_path,
        target_output_dir=target_output_dir,
        verbatim_slice=verbatim_slice,
        roletran_result=roletran_result,
        active_repair_model=active_repair_model,
        active_query_model=active_query_model,
    )

    if artifacts is None:
        elapsed = time.time() - start_time
        error_msg = f"MITRE make build failed after {build_attempt} repair attempts: {last_build_error}"
        logger.error(error_msg)
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            protocol_name=final_protocol_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            role_count=len(protocol_ast.roles),
            preskeleton_count=len(protocol_ast.skeletons),
            roletran_passed=True,
            solver_passed=False,
            duration_seconds=elapsed,
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
            roletran_passed=True,
            build_successful=False,
            duration_seconds=elapsed,
            error_message=error_msg,
        )

    elapsed = time.time() - start_time
    csv_recorder.log_run(
        rfc_id=rfc_id,
        is_eligible=True,
        protocol_name=final_protocol_name,
        selected_sections=target_sections,
        sliced_lines_count=slice_lines_count,
        role_count=len(protocol_ast.roles),
        preskeleton_count=len(protocol_ast.skeletons),
        roletran_passed=True,
        solver_passed=True,
        shapes_count=artifacts.shapes_count,
        duration_seconds=elapsed,
        error_message=None,
    )

    logger.info("================================================================")
    logger.info("Pipeline Complete for %s in %.2fs!", rfc_id, elapsed)
    logger.info("Generated: %s", artifacts.shapes_graph_xhtml_path)
    logger.info("================================================================")

    GLOBAL_EVENT_BUS.emit(
        "pipeline_completed",
        success=True,
        protocol_name=final_protocol_name,
        duration_seconds=elapsed,
        shapes_count=artifacts.shapes_count,
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
        roletran_passed=True,
        build_successful=True,
        build_artifacts=artifacts,
        duration_seconds=elapsed,
    )
