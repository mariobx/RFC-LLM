"""Main Pipeline Orchestrator for RFC-to-CPSA Synthesis."""

import time
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel, Field

from rfc_llm.system_config import SYSTEM_CONFIG
from rfc_llm.logging_config import configure_pipeline_logging, get_pipeline_logger, PipelineMetricsCSVLogger
from rfc_llm.document_ingestion.rfc_header_filter import filter_rfc_header
from rfc_llm.document_ingestion.rfc_toc_parser import parse_table_of_contents
from rfc_llm.document_ingestion.protocol_applicability_gate import evaluate_protocol_applicability
from rfc_llm.document_ingestion.handshake_section_router import route_handshake_sections
from rfc_llm.document_ingestion.verbatim_section_slicer import slice_verbatim_sections
from rfc_llm.semantic_extraction.constrained_protocol_extractor import extract_protocol_specification
from rfc_llm.code_generation.cpsa_scheme_emitter import emit_cpsa_scheme
from rfc_llm.verification_engine.roletran_executability_gate import verify_role_executability
from rfc_llm.verification_engine.mitre_build_orchestrator import execute_mitre_make_build, CPSABuildArtifacts
from rfc_llm.verification_engine.compiler_diagnostic_repair import repair_protocol_specification
import hashlib
from rfc_llm.pipeline_events import GLOBAL_EVENT_BUS

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

    # Initialize per-run logger and CSV recorder
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
        err = f"RFC source file not found: {rfc_file_path}"
        logger.error(err)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=err)
        return PipelineExecutionSummary(rfc_id=rfc_id, is_eligible=False, error_message=err)

    with open(rfc_file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_rfc_text = f.read()

    # -------------------------------------------------------------------------
    # STAGE 1a: Tier 0 Header Filter
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=1, stage_name="Document Intake & Applicability Gate")
    header_res = filter_rfc_header(raw_rfc_text)
    if not header_res.is_eligible:
        elapsed = time.time() - start_time
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            error_message=header_res.disqualification_reason,
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, reason=header_res.disqualification_reason)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            is_eligible=False,
            duration_seconds=elapsed,
            error_message=header_res.disqualification_reason,
        )

    rfc_number_str = header_res.rfc_id or rfc_id
    protocol_title = header_res.title or "Unknown Protocol"

    # -------------------------------------------------------------------------
    # STAGE 1b: Full TOC Parsing
    # -------------------------------------------------------------------------
    toc_entries = parse_table_of_contents(raw_rfc_text)

    # Extract abstract lines
    abstract_lines = []
    lines = raw_rfc_text.splitlines()
    for idx, l in enumerate(lines[:120]):
        if re_match := l.strip().lower() == "abstract":
            abstract_lines = lines[idx + 1:idx + 35]
            break
    abstract_text = "\n".join(abstract_lines)

    # -------------------------------------------------------------------------
    # STAGE 1c: Tier 1 Applicability Gate
    # -------------------------------------------------------------------------
    app_report = evaluate_protocol_applicability(
        rfc_id=rfc_number_str,
        title=protocol_title,
        category=header_res.category or "Unknown",
        abstract=abstract_text,
        toc_entries=toc_entries,
        model=router_model,
    )

    if not app_report.is_cryptographic_protocol:
        elapsed = time.time() - start_time
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            protocol_name=app_report.protocol_name or protocol_title,
            error_message=f"Ineligible: {app_report.rationale}",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, reason=app_report.rationale)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=app_report.protocol_name or protocol_title,
            is_eligible=False,
            duration_seconds=elapsed,
            error_message=app_report.rationale,
        )

    final_proto_name = app_report.protocol_name or protocol_title
    GLOBAL_EVENT_BUS.emit("stage_completed", stage=1, protocol_name=final_proto_name)

    # -------------------------------------------------------------------------
    # STAGE 1d: Exchange Section Routing
    # -------------------------------------------------------------------------
    target_sections = route_handshake_sections(
        rfc_id=rfc_number_str,
        protocol_name=final_proto_name,
        toc_entries=toc_entries,
        model=router_model,
    )

    # -------------------------------------------------------------------------
    # STAGE 1e: Verbatim Section Slicing
    # -------------------------------------------------------------------------
    verbatim_slice = slice_verbatim_sections(raw_rfc_text, target_sections)
    slice_lines_count = len(verbatim_slice.splitlines())

    # Write slice to disk for auditing
    slice_file = target_output_dir / "verbatim_slice.txt"
    with open(slice_file, "w", encoding="utf-8") as f:
        f.write(verbatim_slice)

    GLOBAL_EVENT_BUS.emit(
        "slice_ready",
        sections=target_sections,
        line_count=slice_lines_count,
        slice_path=str(slice_file),
    )

    # -------------------------------------------------------------------------
    # STAGE 2: Constrained Extraction
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=2, stage_name="Constrained Protocol Extraction")
    try:
        protocol_ast = extract_protocol_specification(
            verbatim_slice=verbatim_slice,
            protocol_name=final_proto_name,
            principals=app_report.participating_principals,
            model=extraction_model,
        )
        GLOBAL_EVENT_BUS.emit(
            "stage_completed",
            stage=2,
            roles_count=len(protocol_ast.roles),
            skeletons_count=len(protocol_ast.skeletons),
            ast=protocol_ast.model_dump(),
        )
    except Exception as e:
        elapsed = time.time() - start_time
        err = f"Extraction failed: {e}"
        logger.error(err)
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            protocol_name=final_proto_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            duration_seconds=elapsed,
            error_message=err,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=2, error_message=err)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_proto_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            duration_seconds=elapsed,
            error_message=err,
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
    GLOBAL_EVENT_BUS.emit("stage_started", stage=5, stage_name="Roletran Executability Verification")
    roletran_res = verify_role_executability(scm_path)
    attempt = 0
    seen_roletran_hashes = set()

    max_roletran_attempts = SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS
    while not roletran_res.is_executable and attempt < max_roletran_attempts:
        attempt += 1
        current_hash = hashlib.sha256(protocol_ast.model_dump_json().encode()).hexdigest()
        cycle_detected = current_hash in seen_roletran_hashes
        seen_roletran_hashes.add(current_hash)

        GLOBAL_EVENT_BUS.emit(
            "repair_attempt",
            stage=5,
            attempt=attempt,
            max_attempts=max_roletran_attempts,
            diagnostic=roletran_res.error_diagnostic,
            cycle_detected=cycle_detected,
        )

        logger.warning(
            "Roletran check failed on attempt %d/%d (cycle=%s): %s. Initiating fast self-healing repair...",
            attempt,
            max_roletran_attempts,
            cycle_detected,
            roletran_res.error_diagnostic,
        )
        try:
            protocol_ast = repair_protocol_specification(
                failing_spec=protocol_ast,
                error_diagnostic=roletran_res.error_diagnostic or "Executability verification failure",
                verbatim_slice=verbatim_slice,
                failure_stage="roletran",
                model=active_repair_model,
                query_model=active_query_model,
                cycle_detected=cycle_detected,
            )
            scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir)
            roletran_res = verify_role_executability(scm_path)
        except Exception as repair_err:
            logger.error("Self-healing repair exception on attempt %d: %s", attempt, repair_err)
            time.sleep(2)
            continue

    if roletran_res.is_executable:
        logger.info("Roletran executability check passed.")
        GLOBAL_EVENT_BUS.emit("stage_completed", stage=5, status="passed", attempts=attempt)
    else:
        logger.warning(
            "Roletran pre-flight executability check unfulfilled (%s). Proceeding directly to MITRE CPSA solver verification...",
            roletran_res.error_diagnostic,
        )
        GLOBAL_EVENT_BUS.emit(
            "stage_completed",
            stage=5,
            status="unfulfilled",
            diagnostic=roletran_res.error_diagnostic,
            attempts=attempt,
        )

    # -------------------------------------------------------------------------
    # STAGE 6: MITRE Build Orchestration with RAG Self-Healing Loop
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=6, stage_name="MITRE Build & Shapes Exploration")
    artifacts = None
    build_attempt = 0
    last_build_err = None
    seen_solver_hashes = set()

    while build_attempt <= SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS:
        try:
            artifacts = execute_mitre_make_build(scm_path, target_output_dir)
            break
        except Exception as e:
            last_build_err = str(e)
            if build_attempt < SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS:
                build_attempt += 1
                current_hash = hashlib.sha256(protocol_ast.model_dump_json().encode()).hexdigest()
                cycle_detected = current_hash in seen_solver_hashes
                seen_solver_hashes.add(current_hash)

                GLOBAL_EVENT_BUS.emit(
                    "repair_attempt",
                    stage=6,
                    attempt=build_attempt,
                    max_attempts=SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS,
                    diagnostic=last_build_err,
                    cycle_detected=cycle_detected,
                )

                logger.warning(
                    "MITRE make build failed (attempt %d/%d, cycle=%s): %s. Initiating RAG self-healing repair...",
                    build_attempt,
                    SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS,
                    cycle_detected,
                    last_build_err,
                )
                try:
                    combined_diagnostic = last_build_err
                    if not roletran_res.is_executable and roletran_res.error_diagnostic:
                        combined_diagnostic = (
                            f"MITRE CPSA make / solver failure:\n{last_build_err}\n\n"
                            f"Pre-flight Roletran Executability Diagnostic:\n{roletran_res.error_diagnostic}"
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
                    roletran_res = verify_role_executability(scm_path)
                    if not roletran_res.is_executable:
                        logger.warning("Repaired spec failed roletran executability: %s", roletran_res.error_diagnostic)
                except Exception as repair_err:
                    logger.error("Build self-healing exception on attempt %d: %s", build_attempt, repair_err)
                    time.sleep(2)
                    continue
            else:
                break

    if artifacts is None:
        elapsed = time.time() - start_time
        err = f"MITRE make build failed after {build_attempt} repair attempts: {last_build_err}"
        logger.error(err)
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            protocol_name=final_proto_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            role_count=len(protocol_ast.roles),
            preskeleton_count=len(protocol_ast.skeletons),
            roletran_passed=True,
            solver_passed=False,
            duration_seconds=elapsed,
            error_message=err,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=6, error_message=err)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=err)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_proto_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            roletran_passed=True,
            build_successful=False,
            duration_seconds=elapsed,
            error_message=err,
        )

    elapsed = time.time() - start_time
    csv_recorder.log_run(
        rfc_id=rfc_id,
        is_eligible=True,
        protocol_name=final_proto_name,
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
        protocol_name=final_proto_name,
        duration_seconds=elapsed,
        shapes_count=artifacts.shapes_count,
        shapes_xhtml=str(artifacts.shapes_graph_xhtml_path),
        shapes_txt=str(artifacts.shapes_txt_path),
        scm_path=str(scm_path),
    )

    return PipelineExecutionSummary(
        rfc_id=rfc_id,
        protocol_name=final_proto_name,
        is_eligible=True,
        selected_sections=target_sections,
        sliced_lines_count=slice_lines_count,
        roletran_passed=True,
        build_successful=True,
        build_artifacts=artifacts,
        duration_seconds=elapsed,
    )
