"""Verification Engine package for Stages 5 & 6 roletran executability, self-healing repair, and MITRE CPSA build."""

from src.verification_engine.compiler_diagnostic_repair import (
    DIAGNOSTIC_QUERY_SYSTEM_PROMPT,
    REPAIR_SYSTEM_PROMPT,
    clean_rag_diagnostic_query,
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

__all__ = [
    "RoletranVerificationResult",
    "verify_role_executability",
    "CPSABuildArtifacts",
    "CPSABuildError",
    "execute_mitre_make_build",
    "REPAIR_SYSTEM_PROMPT",
    "DIAGNOSTIC_QUERY_SYSTEM_PROMPT",
    "fallback_sanitize_diagnostic_query",
    "formulate_rag_diagnostic_query",
    "clean_rag_diagnostic_query",
    "repair_protocol_specification",
]
