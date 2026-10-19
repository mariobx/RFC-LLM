"""Dynamic Markdown Prompt Loader for RFC-LLM (.prompts/ directory).

Allows users to inspect, customize, and hot-reload the system prompts driving
all 4 LLM pipeline loops without editing Python source code, while keeping
mandatory Pydantic JSON schema enforcement in Python.
"""

import json
from pathlib import Path
from typing import Dict, Optional, Type
from pydantic import BaseModel

from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("prompt_loader")

# Canonical prompt filenames in .prompts/
PROMPT_APPLICABILITY_GATE = "01_applicability_gate.md"
PROMPT_SECTION_ROUTER = "02_section_router.md"
PROMPT_PROTOCOL_EXTRACTION = "03_protocol_extraction.md"
PROMPT_SCHEMA_SELF_CORRECTION = "04_schema_self_correction.md"
PROMPT_RAG_QUERY_FORMULATION = "05_rag_query_formulation.md"
PROMPT_COMPILER_REPAIR = "06_compiler_repair.md"

# Built-in fallback prompts if a file in .prompts/ is missing or empty
_FALLBACK_PROMPTS: Dict[str, str] = {
    PROMPT_APPLICABILITY_GATE: (
        "You are a formal methods expert in cryptographic protocol verification using MITRE CPSA 4.4.9.\n"
        "Analyze the RFC metadata and Table of Contents to determine if it specifies an interactive "
        "cryptographic security protocol.\n"
        "CRITICAL: Return a populated JSON instance, NOT the schema definition."
    ),
    PROMPT_SECTION_ROUTER: (
        "You are a protocol analyst reading an RFC's Table of Contents.\n"
        "Identify the EXACT section numbers that define the cryptographic message exchange or handshake.\n"
        "Return ONLY a valid JSON object matching the requested schema."
    ),
    PROMPT_PROTOCOL_EXTRACTION: (
        "You are a formal methods expert in cryptographic protocol specification for MITRE CPSA 4.4.9.\n"
        "Analyze the verbatim RFC specification text and extract a complete, mathematically rigorous "
        "CPSAProtocolSpecification.\n"
        "Return ONLY a valid JSON object matching the requested CPSAProtocolSpecification schema."
    ),
    PROMPT_SCHEMA_SELF_CORRECTION: (
        "Your previous JSON output failed MITRE CPSA 4.4.9 schema and scoping validation with the following errors:\n"
        "{validation_error}\n\n"
        "Return ONLY the corrected, fully valid JSON object."
    ),
    PROMPT_RAG_QUERY_FORMULATION: (
        "You are a formal verification compiler diagnostic analyst for MITRE CPSA 4.4.9.\n"
        "Formulate a concise, targeted search query (3 to 6 words) abstracting concrete variable names "
        "into formal CPSA grammar, algebra, or roletran concepts.\n"
        "Output strictly the plain text search query (3 to 6 words)."
    ),
    PROMPT_COMPILER_REPAIR: (
        "You are a formal methods expert in debugging and repairing MITRE CPSA 4.4.9 protocol specifications.\n"
        "Identify the precise defect causing the compiler or solver failure and return a corrected "
        "CPSAProtocolSpecification matching the requested JSON schema."
    ),
}


def load_prompt(prompt_filename: str, prompts_dir: Optional[Path] = None) -> str:
    """Loads a prompt template from `.prompts/<prompt_filename>` on disk.

    Reads dynamically on each invocation so user edits to `.prompts/*.md` take
    effect immediately. Falls back to the built-in default if the file is missing.
    """
    base_dir = prompts_dir or SYSTEM_CONFIG.PROMPTS_DIR
    prompt_path = base_dir / prompt_filename

    if prompt_path.exists() and prompt_path.is_file():
        try:
            content = prompt_path.read_text(encoding="utf-8").strip()
            if content:
                return content
            logger.warning("Prompt file %s is empty; using built-in fallback.", prompt_path)
        except Exception as exc:
            logger.warning("Failed to read prompt file %s (%s); using built-in fallback.", prompt_path, exc)
    else:
        logger.debug("Prompt file %s not found; using built-in fallback.", prompt_path)

    if prompt_filename in _FALLBACK_PROMPTS:
        return _FALLBACK_PROMPTS[prompt_filename]
    raise FileNotFoundError(f"Prompt template '{prompt_filename}' not found in {base_dir}")


def build_schema_system_prompt(
    prompt_filename: str,
    schema_model: Type[BaseModel],
    prompts_dir: Optional[Path] = None,
) -> str:
    """Loads a base system prompt from `.prompts/` and appends the mandatory Pydantic JSON schema."""
    base_prompt = load_prompt(prompt_filename, prompts_dir=prompts_dir)
    schema_json = json.dumps(schema_model.model_json_schema(), indent=2)
    return f"{base_prompt}\n\nRespond strictly with a valid JSON object matching this schema:\n{schema_json}"
