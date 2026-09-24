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
   - Variable Naming & Metadata (STRICT ENFORCEMENT):
     * NEVER use cryptic, single-letter, or abbreviated identifiers (e.g. forbid 'c', 's', 'k', 'prem', 'crand', 'a', 'b', 'n1', 'n2').
     * ALWAYS use full, self-explanatory semantic identifiers directly reflecting the RFC:
       - Principal identities: e.g. "client_identity", "server_identity" (sort: "name")
       - Fresh nonces/tokens: e.g. "client_random", "server_random" (sort: "text")
       - Secrets/payloads: e.g. "premaster_secret", "client_finished_mac" (sort: "data")
       - Symmetric keys: e.g. "session_key", "master_secret_key" (sort: "skey")
       - Asymmetric keys: e.g. "server_public_key", "client_public_key" (sort: "akey")
       - Communication channels: e.g. "handshake_channel" (sort: "chan")
     * ALWAYS populate the 'description' field for every variable explaining its semantic purpose.
     * ALWAYS populate the 'rfc_field' with the exact RFC structure or message name (e.g. "ClientHello.random", "EncryptedPreMasterSecret").
   - Declare all variables with appropriate CPSA sorts:
     * "name": principal identifiers
     * "text": fresh nonces and tokens
     * "data": arbitrary secrets, premaster secrets, or session payloads
     * "skey": symmetric encryption keys (any key used in ["enc", ..., key] for symmetric crypto MUST be sort "skey")
     * "akey": asymmetric key variables
     * "chan": communication channels (always declare a channel variable, e.g. "handshake_channel")
     * "rndx" / "expt": Diffie-Hellman exponents
   - Trace events: Ordered sequence of directional message transmissions:
     * direction: "send" or "recv"
     * channel: e.g. "handshake_channel"
     * description: human-readable explanation of this trace step (e.g. "Client sends ClientHello with client_random")
     * message_term: term tree representation, using operators:
       ["enc", term1, ..., key] for encryption
       ["hash", term1, ...] for one-way digests
       ["cat", term1, term2, ...] for concatenated elements
       ["pubk", name] or ["privk", name] for asymmetric key pairs
       ["invk", key] for the inverse of an asymmetric key variable
       ["ltk", name1, name2] for long-term shared symmetric keys
       ["exp", ["gen"], x] for Diffie-Hellman powers
   - inputs: List of terms known prior to execution required to execute the role (e.g. channel "handshake_channel", held private keys, or pre-shared keys). CRITICAL: In CPSA roletran, every variable in "inputs" MUST actually appear in the role trace! Never include principal names in inputs if they are not sent or received in the trace.
   - outputs: List of terms output or returned upon successful handshake completion (e.g. established nonces, shared secrets). Every variable in outputs must also appear in the trace.
   - unique_originating: Nonces or keys uniquely originated / generated fresh by this role. All fresh terms sent in initial messages must be declared here.

3. Analysis Preskeletons:
   - Always provide a descriptive "herald_comment" summarizing the protocol and analysis goal.
   - For the primary roles, construct point-of-view CPSAPreskeleton instances:
     * description: describe the security goal (e.g. "Verification of premaster_secret secrecy and server authentication from client POV")
     * strands: instantiation of the role strand with variable bindings (the compiler uses "defstrandmax" to instantiate maximal role trace).
     * non_originating: private keys or long-term secrets assumed uncompromised by the penetrator (e.g. ["privk", "server_identity"] or ["invk", "server_public_key"]).
     * unique_originating: fresh nonces or secrets generated in this scenario.

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
            retrieved_meta = []
            for idx, chunk in enumerate(hits, 1):
                chunk_id = chunk.get("chunk_id") or chunk.get("id") or idx
                chunk_title = chunk.get("title") or chunk.get("breadcrumb") or f"Pattern {idx}"
                chunk_source = chunk.get("source_file") or chunk.get("source") or "MITRE Manual"
                chunk_text = chunk.get("text") or chunk.get("content") or ""
                rag_context_blocks.append(f"--- Reference {idx}: {chunk_title} ({chunk_source}) ---\n{chunk_text[:800]}")
                retrieved_meta.append({
                    "chunk_id": str(chunk_id),
                    "title": chunk_title,
                    "source_file": chunk_source,
                    "snippet": chunk_text[:280].strip() + ("..." if len(chunk_text) > 280 else ""),
                })
            from src.pipeline_events import GLOBAL_EVENT_BUS
            GLOBAL_EVENT_BUS.emit(
                "rag_retrieval",
                stage=2,
                purpose="Protocol Extraction Grounding",
                query=rag_query,
                chunks=retrieved_meta,
            )
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

    schema_str = json.dumps(CPSAProtocolSpecification.model_json_schema(), indent=2)
    system_prompt = f"{EXTRACTION_SYSTEM_PROMPT}\n\nRespond strictly with a valid JSON object matching this schema:\n{schema_str}"

    llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(model_name, temperature=0.0)
    response = litellm.completion(
        **llm_kwargs,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
    )

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except Exception:
        import json_repair
        data = json_repair.loads(content)

    spec = CPSAProtocolSpecification.model_validate(data)

    logger.info(
        "Extraction SUCCESS: Extracted protocol '%s' with %d roles and %d preskeletons",
        spec.protocol_name,
        len(spec.roles),
        len(spec.skeletons),
    )
    return spec
