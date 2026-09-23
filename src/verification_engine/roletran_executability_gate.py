"""MITRE CPSA Roletran Pre-Flight Executability Gate (<15 ms)."""

import re
import subprocess
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("roletran_gate")


class RoletranVerificationResult(BaseModel):
    """Result of the static executability verification pass."""
    is_executable: bool = Field(..., description="True if all roles are mathematically constructible and destructible")
    error_diagnostic: Optional[str] = Field(None, description="Concise error diagnostic if executability failed")
    procedural_defproc_code: Optional[str] = Field(None, description="Compiled defproc procedural code if successful")
    raw_stderr: str = Field(default="", description="Complete stderr from roletran execution")


def verify_role_executability(scm_path: Path) -> RoletranVerificationResult:
    """Executes cpsa4roletran on a Scheme model to prove term constructibility and destructibility."""
    logger.info("Executing roletran pre-flight executability gate on %s", scm_path)

    if not SYSTEM_CONFIG.CPSA4ROLETRAN_BIN.exists():
        logger.error("cpsa4roletran binary missing at %s", SYSTEM_CONFIG.CPSA4ROLETRAN_BIN)
        raise FileNotFoundError(f"cpsa4roletran binary missing at {SYSTEM_CONFIG.CPSA4ROLETRAN_BIN}")

    try:
        with open(scm_path, "r", encoding="utf-8") as f:
            scm_content = f.read()

        proc = subprocess.run(
            [str(SYSTEM_CONFIG.CPSA4ROLETRAN_BIN)],
            input=scm_content,
            capture_output=True,
            text=True,
            timeout=SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS,
            check=False,
        )

        stderr_output = proc.stderr.strip()
        stdout_output = proc.stdout.strip()

        if proc.returncode == 0 and not stderr_output:
            logger.info("Roletran PASS: All protocol roles are statically executable")
            return RoletranVerificationResult(
                is_executable=True,
                procedural_defproc_code=stdout_output,
                raw_stderr="",
            )

        # Parse error message: e.g. ":6:6: Received term cannot be fully destructured"
        clean_error = stderr_output
        match = re.search(r":\d+:\d+:\s*(.*)", stderr_output)
        if match:
            clean_error = match.group(1).strip()

        logger.warning("Roletran REJECT: %s", clean_error)
        return RoletranVerificationResult(
            is_executable=False,
            error_diagnostic=clean_error,
            raw_stderr=stderr_output,
        )

    except subprocess.TimeoutExpired:
        logger.error("Roletran check timed out after %d seconds", SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS)
        return RoletranVerificationResult(
            is_executable=False,
            error_diagnostic=f"Roletran verification timed out after {SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS}s",
            raw_stderr="Timeout",
        )
    except Exception as e:
        logger.error("Unexpected failure running roletran: %s", str(e))
        return RoletranVerificationResult(
            is_executable=False,
            error_diagnostic=str(e),
            raw_stderr=str(e),
        )
