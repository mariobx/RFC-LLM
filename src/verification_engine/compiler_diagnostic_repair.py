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
import json_repair
import litellm

from src import rag_retriever_client
from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_COMPILER_REPAIR,
    PROMPT_RAG_QUERY_FORMULATION,
    build_schema_system_prompt,
    load_prompt_spec,
)
from src.rag_retriever_client import (
    get_cpsa_manual_retriever,
    retrieve_cpsa_manual_guidance,
    run_agentic_cpsa_searcher,
)
from src.semantic_extraction.constrained_protocol_extractor import (
    ensure_three_point_of_view_skeletons,
)
from src.system_config import SYSTEM_CONFIG
from src.verification_engine.snowball_autopsy import is_snowball_state_error

logger = get_pipeline_logger("diagnostic_repair")

LAST_REPAIR_METADATA: dict = {
    "rag_query": None,
    "retrieved_chunk_ids": [],
}


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
    query_spec = load_prompt_spec(PROMPT_RAG_QUERY_FORMULATION)
    query_model = model or query_spec.model
    sampling_temp = query_spec.temperature if query_spec.temperature is not None else 0.0
    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(query_model, temperature=sampling_temp)
        system_prompt = query_spec.body
        user_prompt = f"Failure Stage: {failure_stage}\nCompiler Diagnostic:\n{diagnostic}"
        response = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=query_spec.timeout,
        )
        from src.cost_tracker import GLOBAL_COST_TRACKER
        GLOBAL_COST_TRACKER.record_llm_call(
            response,
            role="query",
            model_name=query_model,
            stage=5 if failure_stage == "roletran" else 6,
        )
        raw_content = response.choices[0].message.content
        if raw_content:
            query = " ".join(raw_content.strip().strip('"').strip("'").split())
            if query:
                return query
    except Exception as exc:
        logger.warning("LLM diagnostic query generation failed (%s), using fallback sanitizer", exc)

    return fallback_sanitize_diagnostic_query(diagnostic, failure_stage)


def repair_protocol_specification(
    failing_spec: CPSAProtocolSpecification,
    error_diagnostic: str,
    verbatim_slice: str,
    failure_stage: Literal["roletran", "solver"],
    model: Optional[str] = None,
    query_model: Optional[str] = None,
    cycle_detected: bool = False,
    use_agentic_searcher: bool = True,
) -> CPSAProtocolSpecification:
    """Uses Two-Speed Pinned Header + Agentic CPSA Knowledge Base Searcher to patch a failing CPSAProtocolSpecification."""
    repair_spec = load_prompt_spec(PROMPT_COMPILER_REPAIR)
    model_name = model or repair_spec.model
    logger.info(
        "Executing repair for stage '%s' using %s (cycle_detected=%s, use_agentic_searcher=%s) with diagnostic: %s",
        failure_stage,
        model_name,
        cycle_detected,
        use_agentic_searcher,
        error_diagnostic,
    )

    # 1. Run Agentic CPSA Knowledge Base Searcher when triggered (Attempt #3+, repeated diagnostic, or cycle)
    global LAST_REPAIR_METADATA
    retriever = get_cpsa_manual_retriever() if use_agentic_searcher else None
    if retriever and use_agentic_searcher:
        guidance_text = run_agentic_cpsa_searcher(
            error_diagnostic=error_diagnostic,
            failure_stage=failure_stage,
            failing_spec=failing_spec,
            model=query_model,
            cycle_detected=cycle_detected,
            fallback_query_fn=fallback_sanitize_diagnostic_query,
        )
        LAST_REPAIR_METADATA = {
            "rag_query": rag_retriever_client.LAST_SEARCHER_QUERY,
            "retrieved_chunk_ids": list(rag_retriever_client.LAST_RETRIEVED_CHUNK_IDS),
            "searcher_diagnosis": rag_retriever_client.LAST_SEARCHER_DIAGNOSIS,
            "searcher_turns": list(rag_retriever_client.LAST_SEARCHER_TRACE),
        }
    else:
        LAST_REPAIR_METADATA = {
            "rag_query": None,
            "retrieved_chunk_ids": [],
            "searcher_diagnosis": None,
            "searcher_turns": [],
        }
        guidance_text = (
            "Fast Direct Repair Pass: Apply the Pinned MITRE CPSA 4.4.9 Core Rules & Common Diagnostics "
            "in the system prompt to resolve the compiler diagnostic directly."
        )

    cycle_warning = ""
    if cycle_detected:
        cycle_warning = (
            "\n\nCRITICAL WARNING: An oscillation/cycle was detected. You previously generated a specification "
            "identical or near-identical to this one that already failed. Do NOT repeat the previous edits. "
            "You MUST apply an alternative repair strategy (e.g. check sort declarations, add missing variables to role inputs, "
            "or adjust preskeleton non-originating/unique-originating assumptions) to escape this cycle."
        )

    snowball_directive = ""
    if is_snowball_state_error(error_diagnostic):
        snowball_directive = (
            "\n\nMANDATORY TIER-3 SNOWBALL STATE RECOVERY PROTOCOL (Applies ONLY to State-Space Snowballing):\n"
            "Tier 1 non-default search orders (`--try-old-strands`, `--check-nonces`, `--reverse-nodes`) already "
            "failed to terminate on this specification, proving a structural unification cycle (`unify_0` / `cows` loop). "
            "Inspect the `CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT` in the diagnostic above and apply ALL of the following "
            "structural fixes while preserving strict 1-to-1 fidelity to the RFC:\n"
            "1. DOMAIN-SEPARATE EVERY `enc` AND `hash` TERM USING RFC MESSAGE HEADERS/TYPES: Distinguish request vs. "
            "response `[\"enc\", ...]` and `[\"hash\", ...]` terms using the actual RFC message type, header, opcode, "
            "or label fields from the Verbatim RFC Exchange Specification (and distinct prefix sorts `data` vs `text`) "
            "so outgoing ciphertexts/hashes cannot unify with incoming receptions of the same key sort.\n"
            "2. ADD PRINCIPAL INEQUALITY FACTS (`neq`): In every `CPSAPreskeleton` declaring two or more `name` variables "
            "(e.g. `client_id`, `server_id`), add `[\"neq\", \"<name_a>\", \"<name_b>\"]` to `facts` to block `A = B` "
            "symmetric key reflection.\n"
            "3. ENFORCE `data` vs `text` SORT SEPARATION (CPSA Primer §16.2): Declare fresh `uniq-orig` nonces/challenges/secrets "
            "with `\"sort\": \"data\"` and predictable RFC identifiers/headers/labels with `\"sort\": \"text\"`.\n"
            "4. BIND PRINCIPAL IDENTITIES INSIDE ENCRYPTED FLIGHTS: Include the communicating `name` variables inside the "
            "`[\"enc\", ...]` terms of the looping role identified in the autopsy so regular augmentation binds to existing "
            "principals instead of spawning unbounded `*-0, *-1` strands."
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
        f"{failing_spec.model_dump_json(indent=2)}{cycle_warning}{snowball_directive}\n\n"
        "Provide the complete repaired CPSAProtocolSpecification resolving the error without inventing fictional protocol terms."
    )

    # Use higher temperature if cycle detected to break greedy minimum
    base_temp = repair_spec.temperature if repair_spec.temperature is not None else 0.0
    sampling_temperature = max(0.4, base_temp) if cycle_detected else base_temp
    system_prompt = build_schema_system_prompt(
        PROMPT_COMPILER_REPAIR,
        CPSAProtocolSpecification,
    )

    llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
        model_name,
        temperature=sampling_temperature,
        max_tokens=repair_spec.max_tokens,
    )
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
                timeout=repair_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(
                response,
                role="repair",
                model_name=model_name,
                stage=5 if failure_stage == "roletran" else 6,
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
        parsed_data = json_repair.loads(raw_content)

    repaired_spec = CPSAProtocolSpecification.model_validate(parsed_data)
    repaired_spec = ensure_three_point_of_view_skeletons(repaired_spec)

    logger.info("Repair pass completed for '%s'", repaired_spec.protocol_name)
    return repaired_spec
