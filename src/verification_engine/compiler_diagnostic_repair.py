"""Compiler Diagnostic Repair Engine with RAG-Guided Self-Healing.

Analyzes `cpsa4roletran` and `cpsa4` compiler diagnostics, formulates an
abstracted conceptual RAG query using the configured query model, retrieves
authoritative MITRE CPSA 4.4.9 manual chunks, and repairs the failing
`CPSAProtocolSpecification` AST.
"""

import json
import re
import time
from typing import Literal, Optional
import litellm

from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_COMPILER_REPAIR,
    PROMPT_RAG_QUERY_FORMULATION,
    build_schema_system_prompt,
    load_prompt,
)
from src.rag_retriever_client import (
    get_cpsa_manual_retriever,
    retrieve_cpsa_manual_guidance,
)
from src.semantic_extraction.constrained_protocol_extractor import (
    ensure_three_point_of_view_skeletons,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("diagnostic_repair")

# Legacy helper alias preserved for compatibility
_get_retriever = get_cpsa_manual_retriever

# Loaded from .prompts/06_compiler_repair.md and .prompts/05_rag_query_formulation.md
REPAIR_SYSTEM_PROMPT: str = load_prompt(PROMPT_COMPILER_REPAIR)
DIAGNOSTIC_QUERY_SYSTEM_PROMPT: str = load_prompt(PROMPT_RAG_QUERY_FORMULATION)


def fallback_sanitize_diagnostic_query(diagnostic: str, failure_stage: str) -> str:
    """Fallback sanitizer for compiler diagnostics when LLM query formulation is unavailable,
    stripping file paths, line numbers, and Make boilerplate.
    """
    cleaned = re.sub(r"MITRE build failed for [^:]+:\s*", "", diagnostic, flags=re.IGNORECASE)
    cleaned = re.sub(r"make(\[\d+\])?:.*", "", cleaned)
    cleaned = re.sub(r"[a-zA-Z0-9_\-\./]+\.(scm|txt|xhtml|mk|hs|pl)(:\d+:\d+)?:?", "", cleaned)
    cleaned = re.sub(r"\(.*?\)", "", cleaned)
    cleaned = re.sub(r'["\':*#\n\r]', " ", cleaned)
    tokens = [
        token
        for token in cleaned.split()
        if len(token) > 2
        and not token.isdigit()
        and token.lower() not in {"error", "exit", "code", "failed"}
    ]
    concise_tokens = " ".join(tokens[:5])
    if concise_tokens:
        return f"CPSA {failure_stage} {concise_tokens} syntax manual error rule fix"
    return f"CPSA {failure_stage} syntax manual error rule fix"


def formulate_rag_diagnostic_query(
    diagnostic: str,
    failure_stage: str,
    model: Optional[str] = None,
) -> str:
    """Uses a dedicated LLM call to formulate a targeted conceptual query for the MITRE CPSA manual,
    purging concrete variable names and local file paths. Falls back to deterministic sanitization if offline.
    """
    query_model = model or SYSTEM_CONFIG.DEFAULT_QUERY_MODEL
    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(query_model, temperature=0.0)
        system_prompt = load_prompt(PROMPT_RAG_QUERY_FORMULATION)
        user_prompt = f"Failure Stage: {failure_stage}\nCompiler Diagnostic:\n{diagnostic}"
        response = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=10,
        )
        raw_content = response.choices[0].message.content
        if raw_content:
            query = " ".join(raw_content.strip().strip('"').strip("'").split())
            if query:
                return query
    except Exception as exc:
        logger.warning("LLM diagnostic query generation failed (%s), using fallback sanitizer", exc)

    return fallback_sanitize_diagnostic_query(diagnostic, failure_stage)


def clean_rag_diagnostic_query(
    diagnostic: str,
    failure_stage: str,
    model: Optional[str] = None,
) -> str:
    """Legacy alias routing to LLM query formulation."""
    return formulate_rag_diagnostic_query(diagnostic, failure_stage, model=model)


def repair_protocol_specification(
    failing_spec: CPSAProtocolSpecification,
    error_diagnostic: str,
    verbatim_slice: str,
    failure_stage: Literal["roletran", "solver"],
    model: Optional[str] = None,
    query_model: Optional[str] = None,
    cycle_detected: bool = False,
) -> CPSAProtocolSpecification:
    """Uses RAG-guided diagnostic repair to patch a failing CPSAProtocolSpecification."""
    model_name = model or SYSTEM_CONFIG.DEFAULT_REPAIR_MODEL
    logger.info(
        "Executing RAG-guided repair for stage '%s' (cycle_detected=%s) with diagnostic: %s",
        failure_stage,
        cycle_detected,
        error_diagnostic,
    )

    # 1. Formulate RAG query and retrieve manual guidance only when a retriever is available
    retriever = _get_retriever()
    if retriever:
        rag_query = formulate_rag_diagnostic_query(
            error_diagnostic,
            failure_stage,
            model=query_model,
        )
        guidance_text = retrieve_cpsa_manual_guidance(
            query=rag_query,
            stage=5 if failure_stage == "roletran" else 6,
            purpose=f"Diagnostic Repair ({failure_stage})",
            header_prefix="Retrieved Manual Guidance",
            top_k=2,
            fallback_message="Review standard CPSA executability and preskeleton assumption rules.",
        )
    else:
        guidance_text = "Review standard CPSA executability and preskeleton assumption rules."

    cycle_warning = ""
    if cycle_detected:
        cycle_warning = (
            "\n\nCRITICAL WARNING: An oscillation/cycle was detected. You previously generated a specification "
            "identical or near-identical to this one that already failed. Do NOT repeat the previous edits. "
            "You MUST apply an alternative repair strategy (e.g. check sort declarations, add missing variables to role inputs, "
            "or adjust preskeleton non-originating/unique-originating assumptions) to escape this cycle."
        )

    # Truncate verbatim slice to concise context to preserve token quota across multiple repair passes
    slice_snippet = verbatim_slice[:3000]
    if len(verbatim_slice) > 3000:
        slice_snippet += "\n... [Remaining RFC specification text truncated for compiler repair pass] ..."

    user_prompt = (
        f"Failing Protocol: {failing_spec.protocol_name}\n"
        f"Failure Stage: {failure_stage}\n"
        f"Compiler Diagnostic / Error:\n{error_diagnostic}\n\n"
        "MITRE CPSA Reference Guidance (Helper Only - Explains syntax rules and failure mechanisms):\n"
        f"{guidance_text}\n\n"
        "Verbatim RFC Exchange Specification (Excerpt for repair context):\n"
        f"{slice_snippet}\n\n"
        "Current Failing CPSA Specification (JSON):\n"
        f"{failing_spec.model_dump_json(indent=2)}{cycle_warning}\n\n"
        "Provide the complete repaired CPSAProtocolSpecification resolving the error without inventing fictional protocol terms."
    )

    # Use higher temperature if cycle detected to break greedy minimum
    sampling_temperature = 0.4 if cycle_detected else 0.0
    system_prompt = build_schema_system_prompt(
        PROMPT_COMPILER_REPAIR,
        CPSAProtocolSpecification,
    )

    llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(model_name, temperature=sampling_temperature)
    response = None
    for retry_idx in range(4):
        try:
            response = litellm.completion(
                **llm_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
            )
            break
        except Exception as exc:
            err_msg = str(exc)
            if (
                any(token in err_msg for token in ("429", "Quota exceeded", "RateLimitError"))
                and retry_idx < 3
            ):
                wait_seconds = 30 * (retry_idx + 1)
                logger.warning(
                    "Quota rate limit reached during repair pass. Waiting %ds before retry: %s",
                    wait_seconds,
                    exc,
                )
                time.sleep(wait_seconds)
            else:
                raise

    raw_content = response.choices[0].message.content
    try:
        parsed_data = json.loads(raw_content)
    except Exception:
        import json_repair
        parsed_data = json_repair.loads(raw_content)

    repaired_spec = CPSAProtocolSpecification.model_validate(parsed_data)
    repaired_spec = ensure_three_point_of_view_skeletons(repaired_spec)

    logger.info("Repair pass completed for '%s'", repaired_spec.protocol_name)
    return repaired_spec
