"""CPSA Scheme S-Expression Emitter using cpsa4json."""

import re
import subprocess
from pathlib import Path
from typing import Optional

from src.code_generation.cpsa_json_serializer import serialize_to_cpsa_json_string
from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("scheme_emitter")


class CPSAJsonCompilationError(Exception):
    """Raised when cpsa4json fails to compile a JSON tree into Scheme S-expressions."""
    pass


def sanitize_protocol_stem(raw_name: str) -> str:
    """Sanitizes a protocol name or filename prefix into a filesystem-safe `.scm` stem."""
    sanitized = re.sub(r"[^a-z0-9_-]+", "_", (raw_name or "").lower()).strip("_")
    return sanitized or "protocol"


def emit_cpsa_scheme(
    spec: CPSAProtocolSpecification,
    output_directory: Path,
    filename_prefix: Optional[str] = None,
) -> Path:
    """Compiles a CPSAProtocolSpecification into a verified MITRE Scheme (.scm) file via cpsa4json."""
    output_directory.mkdir(parents=True, exist_ok=True)
    stem = sanitize_protocol_stem(filename_prefix or spec.protocol_name)
    target_scm_path = output_directory / f"{stem}.scm"

    logger.info("Emitting CPSA Scheme S-expressions for '%s' to %s", spec.protocol_name, target_scm_path)

    json_input_str = serialize_to_cpsa_json_string(spec)

    if not SYSTEM_CONFIG.CPSA4JSON_BIN.exists():
        logger.error("cpsa4json binary not found at %s", SYSTEM_CONFIG.CPSA4JSON_BIN)
        raise FileNotFoundError(f"cpsa4json binary missing at {SYSTEM_CONFIG.CPSA4JSON_BIN}")

    try:
        proc = subprocess.run(
            [str(SYSTEM_CONFIG.CPSA4JSON_BIN)],
            input=json_input_str,
            capture_output=True,
            text=True,
            timeout=SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS,
            check=False,
        )

        if proc.returncode != 0 or "Bad char in atom" in proc.stdout or "Error" in proc.stderr:
            err_msg = proc.stderr.strip() or proc.stdout.strip() or f"Exited with code {proc.returncode}"
            logger.error("cpsa4json compilation failed: %s", err_msg)
            raise CPSAJsonCompilationError(f"cpsa4json compilation error: {err_msg}")

        scm_content = proc.stdout

        with open(target_scm_path, "w", encoding="utf-8") as f:
            f.write(scm_content)

        logger.info("Successfully emitted %d lines of Scheme code to %s", len(scm_content.splitlines()), target_scm_path)
        return target_scm_path

    except subprocess.TimeoutExpired as e:
        logger.error("cpsa4json subprocess timed out after %d seconds", SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS)
        raise CPSAJsonCompilationError(f"cpsa4json compilation timed out: {e}") from e
