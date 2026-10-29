"""Code Generation package for Stage 3 CPSA JSON serialization and Scheme S-expression emission."""

from src.code_generation.cpsa_json_serializer import (
    serialize_to_cpsa_json,
    serialize_to_cpsa_json_string,
)
from src.code_generation.cpsa_scheme_emitter import (
    CPSAJsonCompilationError,
    emit_cpsa_scheme,
)

__all__ = [
    "serialize_to_cpsa_json",
    "serialize_to_cpsa_json_string",
    "CPSAJsonCompilationError",
    "emit_cpsa_scheme",
]
