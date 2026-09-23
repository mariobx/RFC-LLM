"""Constrained Protocol Semantic Extractor with RAG Grounding."""

import json
from typing import List, Optional
import litellm

from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("protocol_extractor")

# Lazy-loaded singleton retriever
_GLOBAL_RETRIEVER = None


def _get_retriever():
    global _GLOBAL_RETRIEVER
    if _GLOBAL_RETRIEVER is None:
        try:
            import importlib
            rag_module = importlib.import_module("refrences.scripts.03_query_rag")
            CPSASemanticRetriever = getattr(rag_module, "CPSASemanticRetriever")
            _GLOBAL_RETRIEVER = CPSASemanticRetriever()
            logger.info("Initialized CPSASemanticRetriever for extraction grounding")
        except Exception as e:
            logger.warning("Could not initialize CPSASemanticRetriever: %s", e)
            _GLOBAL_RETRIEVER = None
    return _GLOBAL_RETRIEVER


EXTRACTION_SYSTEM_PROMPT = """You are a formal methods expert in cryptographic protocol specification for MITRE CPSA 4.4.9.
Your task is to analyze the provided verbatim RFC specification text and extract a complete, mathematically rigorous CPSAProtocolSpecification.

CPSA Model Architecture Requirements:
1. Message Algebra: Select "basic" for symmetric/asymmetric protocols, or "diffie-hellman" if modular exponentiation or Diffie-Hellman groups are used.
2. Roles: For every communicating principal, create a CPSAProtocolRole:
   - Declare all variables with appropriate CPSA sorts:
     * "name": principal identifiers
     * "text": fresh nonces and tokens
     * "data": arbitrary secrets, premaster secrets, or session payloads
     * "skey": symmetric encryption keys
     * "akey": asymmetric key variables
     * "chan": communication channels (always declare a channel variable, such as "ch")
     * "rndx" / "expt": Diffie-Hellman exponents
   - Trace events: Ordered sequence of directional message transmissions:
     * direction: "send" or "recv"
     * channel: "ch"
     * message_term: term tree representation, using operators:
       ["enc", term1, ..., key] for encryption
       ["hash", term1, ...] for one-way digests
       ["cat", term1, term2, ...] for concatenated elements
       ["pubk", name] or ["privk", name] for asymmetric key pairs
       ["invk", key] for the inverse of an asymmetric key variable
       ["ltk", name1, name2] for long-term shared symmetric keys
       ["exp", ["gen"], x] for Diffie-Hellman powers
   - inputs: List of terms known prior to execution required to execute the role (e.g. channel "ch", principal names, held private keys or pre-shared keys).
   - outputs: List of terms output or returned upon successful handshake completion (e.g. established nonces, shared secrets).
   - unique_originating: Nonces or keys uniquely originated / generated fresh by this role.

3. Analysis Preskeletons:
   - For the primary roles, construct point-of-view CPSAPreskeleton instances:
     * strands: instantiation of the role strand with full trace height.
     * non_originating: private keys or long-term secrets assumed uncompromised by the penetrator (e.g. ["privk", "Principal_Name"] or ["invk", "key_var"]).
     * unique_originating: fresh terms generated in this scenario.

Return ONLY a valid JSON object matching the requested CPSAProtocolSpecification schema."""


def extract_protocol_specification(
    verbatim_slice: str,
    protocol_name: str,
    principals: Optional[List[str]] = None,
    model: Optional[str] = None,
) -> CPSAProtocolSpecification:
    """Extracts a validated CPSAProtocolSpecification from verbatim RFC text."""
    model_name = model or SYSTEM_CONFIG.DEFAULT_EXTRACTION_MODEL
    logger.info("Extracting CPSAProtocolSpecification for '%s' using %s", protocol_name, model_name)

    # 1. Retrieve RAG Grounding Context
    rag_context_blocks = []
    retriever = _get_retriever()
    if retriever:
        try:
            rag_query = f"{protocol_name} protocol message exchange encryption keys nonces"
            hits = retriever.search(rag_query, top_k=2, mode="hybrid", rerank=False)
            for idx, chunk in enumerate(hits, 1):
                chunk_title = chunk.get("title") or chunk.get("breadcrumb") or f"Pattern {idx}"
                chunk_source = chunk.get("source_file") or chunk.get("source") or "MITRE Manual"
                chunk_text = chunk.get("text") or chunk.get("content") or ""
                rag_context_blocks.append(f"--- Reference {idx}: {chunk_title} ({chunk_source}) ---\n{chunk_text[:800]}")
        except Exception as e:
            logger.warning("RAG retrieval failed during extraction: %s", e)

    rag_grounding_text = "\n\n".join(rag_context_blocks) if rag_context_blocks else "Use standard MITRE CPSA 4.4.9 syntax conventions."

    principals_hint = f"Expected Principals: {', '.join(principals)}" if principals else ""

    user_prompt = f"""Protocol Identifier: {protocol_name}
{principals_hint}

MITRE CPSA Reference Syntax Examples (Helper Only - Use strictly for syntax and algebraic structure, NEVER as ground truth for protocol facts):
{rag_grounding_text}

Verbatim RFC Exchange Specification (SOLE GROUND TRUTH):
{verbatim_slice}

Extract the complete CPSAProtocolSpecification adhering to all executability and sort constraints.
Do NOT copy protocol elements, names, or messages from the reference examples; extract strictly what is defined in the Verbatim RFC Exchange Specification."""

    response = litellm.completion(
        model=model_name,
        api_base=SYSTEM_CONFIG.OLLAMA_API_BASE if model_name.startswith("ollama/") else None,
        messages=[
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object", "schema": CPSAProtocolSpecification.model_json_schema()},
        temperature=0.0,
        timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    spec = CPSAProtocolSpecification.model_validate(data)

    logger.info(
        "Extraction SUCCESS: Extracted protocol '%s' with %d roles and %d preskeletons",
        spec.protocol_name,
        len(spec.roles),
        len(spec.skeletons),
    )
    return spec
