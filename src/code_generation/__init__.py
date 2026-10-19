"""Code Generation package for Stages 3 & 4 CPSA JSON serialization and Scheme S-expression emission."""

from src.code_generation.cpsa_json_serializer import (
    serialize_to_cpsa_json,
    serialize_to_cpsa_json_string,
    write_cpsa_json_file,
)
from src.code_generation.cpsa_scheme_emitter import (
    CPSAJsonCompilationError,
    emit_cpsa_scheme,
)

__all__ = [
    "serialize_to_cpsa_json",
    "serialize_to_cpsa_json_string",
    "write_cpsa_json_file",
    "CPSAJsonCompilationError",
    "emit_cpsa_scheme",
]
