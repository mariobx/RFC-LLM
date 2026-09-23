"""Compiler Diagnostic Repair Engine with RAG-Guided Self-Healing."""

import json
from typing import Literal, Optional
import litellm

from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("diagnostic_repair")

_GLOBAL_RETRIEVER = None


def _get_retriever():
    global _GLOBAL_RETRIEVER
    if _GLOBAL_RETRIEVER is None:
        try:
            import importlib
            rag_module = importlib.import_module("refrences.scripts.03_query_rag")
            CPSASemanticRetriever = getattr(rag_module, "CPSASemanticRetriever")
            _GLOBAL_RETRIEVER = CPSASemanticRetriever()
        except Exception as e:
            logger.warning("Could not initialize CPSASemanticRetriever for repair: %s", e)
            _GLOBAL_RETRIEVER = None
    return _GLOBAL_RETRIEVER


REPAIR_SYSTEM_PROMPT = """You are a formal methods expert in debugging and repairing MITRE CPSA 4.4.9 protocol specifications.
You are given a failing CPSAProtocolSpecification, the verbatim RFC exchange text, the compiler error diagnostic, and retrieved guidance from the MITRE CPSA reference manual.

Your task is to identify the precise defect causing the compiler or solver failure and return a corrected CPSAProtocolSpecification.

Common Diagnostics & Fixes:
1. "Received term cannot be fully destructured":
   - A role receives an encrypted message or hash, but lacks the necessary decryption key or preimage in its "inputs".
   - Fix: Ensure the role's "inputs" list includes the required key (e.g. held private key or shared secret) to decrypt the incoming payload.
2. "Transmitted term cannot be built from inputs and previous terms":
   - A role attempts to send a variable, nonce, or key before it has been generated, passed as an input, or received.
   - Fix: Add the variable to "inputs", declare it as "uniq-orig", or adjust event sequence.
3. Unprovable / Unrealized Preskeleton Skeletons:
   - Preskeleton is missing necessary secrecy assumptions ("non-orig" for uncompromised private keys).
   - Nonces lack freshness assumptions ("uniq-orig").
   - Fix: Declare uncompromised keys under "non_originating" and fresh nonces under "unique_originating".

Return ONLY the repaired, valid CPSAProtocolSpecification matching the requested JSON schema."""


def repair_protocol_specification(
    failing_spec: CPSAProtocolSpecification,
    error_diagnostic: str,
    verbatim_slice: str,
    failure_stage: Literal["roletran", "solver"],
    model: Optional[str] = None,
) -> CPSAProtocolSpecification:
    """Uses RAG-guided diagnostic repair to patch a failing CPSAProtocolSpecification."""
    model_name = model or SYSTEM_CONFIG.DEFAULT_REPAIR_MODEL
    logger.info("Executing RAG-guided repair for stage '%s' with diagnostic: %s", failure_stage, error_diagnostic)

    # 1. RAG Retrieval on Compiler Diagnostic
    retrieved_guidance = []
    retriever = _get_retriever()
    if retriever:
        try:
            rag_query = f"{error_diagnostic} CPSA manual syntax error rule fix"
            hits = retriever.search(rag_query, top_k=2, mode="hybrid", rerank=False)
            for idx, chunk in enumerate(hits, 1):
                chunk_title = chunk.get("title") or chunk.get("breadcrumb") or f"Manual Section {idx}"
                chunk_source = chunk.get("source_file") or chunk.get("source") or "Manual"
                chunk_text = chunk.get("text") or chunk.get("content") or ""
                retrieved_guidance.append(f"--- Retrieved Manual Guidance {idx}: {chunk_title} ({chunk_source}) ---\n{chunk_text[:800]}")
        except Exception as e:
            logger.warning("RAG retrieval failed during repair: %s", e)

    guidance_text = "\n\n".join(retrieved_guidance) if retrieved_guidance else "Review standard CPSA executability and preskeleton assumption rules."

    user_prompt = f"""Failing Protocol: {failing_spec.protocol_name}
Failure Stage: {failure_stage}
Compiler Diagnostic / Error:
{error_diagnostic}

MITRE CPSA Reference Guidance (Helper Only - Explains syntax rules and failure mechanisms):
{guidance_text}

Verbatim RFC Exchange Specification (SOLE GROUND TRUTH for protocol messages and keys):
{verbatim_slice}

Current Failing CPSA Specification (JSON):
{failing_spec.model_dump_json(indent=2)}

Provide the complete repaired CPSAProtocolSpecification resolving the error without inventing fictional protocol terms."""

    response = litellm.completion(
        model=model_name,
        api_base=SYSTEM_CONFIG.OLLAMA_API_BASE if model_name.startswith("ollama/") else None,
        messages=[
            {"role": "system", "content": REPAIR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object", "schema": CPSAProtocolSpecification.model_json_schema()},
        temperature=0.0,
        timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    repaired_spec = CPSAProtocolSpecification.model_validate(data)

    logger.info("Repair pass completed for '%s'", repaired_spec.protocol_name)
    return repaired_spec
