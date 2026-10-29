"""Verification Engine package for Stages 4, 5 & 6 roletran check, self-healing repair, and MITRE CPSA compilation."""

from src.verification_engine.compiler_diagnostic_repair import (
    fallback_sanitize_diagnostic_query,
    formulate_rag_diagnostic_query,
    repair_protocol_specification,
)
from src.verification_engine.mitre_build_orchestrator import (
    CPSABuildArtifacts,
    CPSABuildError,
    execute_mitre_make_build,
)
from src.verification_engine.roletran_executability_gate import (
    RoletranVerificationResult,
    verify_role_executability,
)
from src.verification_engine.trajectory_metadata_exporter import (
    analyze_exploration_txt,
    analyze_shapes_txt,
    build_scm_metadata_header,
    compute_quality_assessment,
    write_trajectory_metadata_bundle,
)

__all__ = [
    "RoletranVerificationResult",
    "verify_role_executability",
    "CPSABuildArtifacts",
    "CPSABuildError",
    "execute_mitre_make_build",
    "fallback_sanitize_diagnostic_query",
    "formulate_rag_diagnostic_query",
    "repair_protocol_specification",
    "analyze_exploration_txt",
    "analyze_shapes_txt",
    "build_scm_metadata_header",
    "compute_quality_assessment",
    "write_trajectory_metadata_bundle",
]
