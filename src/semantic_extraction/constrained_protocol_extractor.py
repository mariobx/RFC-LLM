"""Constrained Protocol Semantic Extractor with RAG Grounding."""

import json
from typing import List, Optional
import litellm

from src.intermediate_representation.protocol_syntax_tree import (
    CPSAProtocolSpecification,
    CPSAPreskeleton,
    CPSAStrandInstance,
    CPSAVariableDeclaration,
)
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

3. Analysis Preskeletons (MANDATORY 3-SKELETON ARCHITECTURE):
   CRITICAL: Never put 'deflistener' in the primary POV skeletons! In CPSA, a skeleton with a listener on an uncompromised secret terminates as dead/unrealized and CANNOT display the realized two-party protocol handshake shape.
   You MUST generate 3 distinct point-of-view CPSAPreskeleton instances:
   - Skeleton 1 (Initiator / Client POV - Shape Realization & Authentication):
     * description: "Client Point of View: verifies server authentication and completes handshake shape"
     * strands: [defstrandmax for initiator/client role]
     * non_originating: uncompromised private/long-term keys (e.g. ["privk", "server_identity"])
     * unique_originating: fresh nonces / secrets generated by client (e.g. "client_random", "premaster_secret")
     * listeners: [] (STRICTLY EMPTY: never include deflistener in pure POV skeletons)
   - Skeleton 2 (Responder / Server POV - Mutual Authentication):
     * description: "Server Point of View: verifies client authentication"
     * strands: [defstrandmax for responder/server role]
     * non_originating: uncompromised private/long-term keys (e.g. ["privk", "server_identity"])
     * unique_originating: fresh nonces generated by server (e.g. "server_random")
     * listeners: [] (STRICTLY EMPTY)
   - Skeleton 3 (Confidentiality / Secrecy POV):
     * description: "Secrecy Verification: tests whether penetrator can learn the established secret"
     * strands: [defstrandmax for client or server role]
     * listeners: [the core established secret/payload, e.g. "premaster_secret"]
     * non_originating: uncompromised private/long-term keys
     * unique_originating: fresh nonces / secrets

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
    spec = ensure_three_point_of_view_skeletons(spec)

    logger.info(
        "Extraction SUCCESS: Extracted protocol '%s' with %d roles and %d preskeletons",
        spec.protocol_name,
        len(spec.roles),
        len(spec.skeletons),
    )
    return spec


def ensure_three_point_of_view_skeletons(spec: CPSAProtocolSpecification) -> CPSAProtocolSpecification:
    """Guarantees the standard CPSA 3-skeleton architecture:
    1. Dedicated pure POV preskeleton for each communicating role with defstrandmax and NO listeners
       (enabling CPSA to compute minimal realized bilateral handshake shapes).
    2. A distinct secrecy preskeleton containing a deflistener for the primary secret.
    """
    if not spec.roles:
        return spec

    # Collect existing secrecy listeners and non-originating assumptions
    existing_listeners = []
    global_non_orig = []
    for skel in spec.skeletons:
        existing_listeners.extend(skel.listeners)
        global_non_orig.extend(skel.non_originating)

    # Dedup non-originating keys preserving order
    seen_no = set()
    dedup_non_orig = []
    for no in global_non_orig:
        s = json.dumps(no, sort_keys=True)
        if s not in seen_no:
            seen_no.add(s)
            dedup_non_orig.append(no)

    # Separate pure POV skeletons (without listeners) and secrecy skeletons (with listeners)
    roles_with_pure_pov = set()
    pure_skeletons = []
    secrecy_skeletons = []

    for skel in spec.skeletons:
        if not skel.listeners:
            pure_skeletons.append(skel)
            for strand in skel.strands:
                roles_with_pure_pov.add(strand.role_name)
        else:
            secrecy_skeletons.append(skel)

    # Build pure POV skeletons for roles that lack them
    new_pure_skeletons = list(pure_skeletons)
    for role in spec.roles:
        if role.role_name not in roles_with_pure_pov:
            bindings = {v.name: v.name for v in role.variables}
            skel_vars = [CPSAVariableDeclaration(name=v.name, sort=v.sort) for v in role.variables]
            new_skel = CPSAPreskeleton(
                protocol_name=spec.protocol_name,
                description=f"{role.role_name.capitalize()} Point of View (Authentication & Shape Realization)",
                variables=skel_vars,
                strands=[
                    CPSAStrandInstance(
                        role_name=role.role_name,
                        variable_bindings=bindings,
                    )
                ],
                non_originating=dedup_non_orig,
                unique_originating=list(role.unique_originating),
                listeners=[],
                comment=f"{role.role_name.capitalize()} Point of View",
            )
            new_pure_skeletons.append(new_skel)

    # Guarantee at least one secrecy verification skeleton if a secret exists
    final_skeletons = new_pure_skeletons
    if secrecy_skeletons:
        final_skeletons.extend(secrecy_skeletons)
    else:
        # Pick secret to listen for
        secret_term = existing_listeners[0] if existing_listeners else None
        if not secret_term:
            for r in spec.roles:
                for v in r.variables:
                    if v.sort.value == "data" and ("secret" in v.name.lower() or "key" in v.name.lower() or "data" in v.name.lower()):
                        secret_term = v.name
                        break
                if secret_term:
                    break

        if secret_term:
            primary_role = spec.roles[0]
            bindings = {v.name: v.name for v in primary_role.variables}
            skel_vars = [CPSAVariableDeclaration(name=v.name, sort=v.sort) for v in primary_role.variables]
            sec_skel = CPSAPreskeleton(
                protocol_name=spec.protocol_name,
                description=f"Secrecy Verification: tests secrecy of {secret_term}",
                variables=skel_vars,
                strands=[
                    CPSAStrandInstance(
                        role_name=primary_role.role_name,
                        variable_bindings=bindings,
                    )
                ],
                non_originating=dedup_non_orig,
                unique_originating=list(primary_role.unique_originating),
                listeners=[secret_term],
                comment=f"Secrecy Point of View: Listener on {secret_term}",
            )
            final_skeletons.append(sec_skel)

    spec.skeletons = final_skeletons
    return spec
