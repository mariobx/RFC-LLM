"""CPSA JSON AST Serializer."""

import json
from pathlib import Path
from typing import Any, List, Union

from rfc_llm.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from rfc_llm.logging_config import get_pipeline_logger

logger = get_pipeline_logger("json_serializer")


def serialize_to_cpsa_json(spec: CPSAProtocolSpecification) -> List[List[Any]]:
    """Serializes a CPSAProtocolSpecification into a list of top-level CPSA JSON forms."""
    logger.debug("Serializing CPSAProtocolSpecification for '%s' to native JSON forms", spec.protocol_name)
    payload = spec.to_cpsa_json_payload()
    logger.debug("Serialized %d top-level S-expression forms", len(payload))
    return payload


def serialize_to_cpsa_json_string(spec: CPSAProtocolSpecification) -> str:
    """Serializes the protocol specification into a newline-delimited JSON string for cpsa4json."""
    forms = serialize_to_cpsa_json(spec)
    # Each top-level form is written on its own line / separated by double newlines
    return "\n\n".join(json.dumps(form) for form in forms) + "\n"


def write_cpsa_json_file(spec: CPSAProtocolSpecification, target_path: Path) -> Path:
    """Writes the serialized JSON specification to disk."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    json_content = serialize_to_cpsa_json_string(spec)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(json_content)
    logger.info("Wrote CPSA JSON specification to %s", target_path)
    return target_path
