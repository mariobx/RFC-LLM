"""Constrained Protocol Semantic Extractor with RAG Grounding."""

import json
from typing import List, Optional
import litellm
from pydantic import ValidationError

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

CRITICAL MITRE CPSA 4.4.9 MANUAL GROUNDING (Chapters 2, 3, 4, 10 - Tables 10.1 through 10.6):
Every extracted construct must strictly obey the MITRE CPSA formal syntax:

1. Cryptographic Message Algebra (Tables 10.2, 10.4, 10.5):
   - Select "basic" for symmetric/asymmetric protocols, or "diffie-hellman" if modular exponentiation or Diffie-Hellman groups are used.
   - Diffie-Hellman Sorts (Section 4.2 & 10.3.2): Fresh randomly generated private exponents MUST be declared with sort "rndx" (atomic exponents). Sort "expt" is reserved for compound expressions or unconstrained received values. NEVER declare fresh originating exponents as "expt".

2. Term Syntax & Structure (Tables 10.3 & 10.5):
   - Formal Term Grammar:
     term ::= id | integer | (op term+)
   - STRICT ATOM ENFORCEMENT: A term is strictly an atom string (variable identifier e.g. "client_random", "session_key"), an integer constant (e.g. 1), or a prefix operator list [op, ...args].
   - ABSOLUTE NEGATIVE CONSTRAINT: A term is NEVER a dictionary or object (e.g. NEVER {"name": "...", "description": "..."}).
     Variables MUST BE DECLARED in the role's 'variables' list. In 'message_term', 'inputs', 'outputs', and 'unique_originating', variables are referenced ONLY by their plain string name atom (e.g. "session_key", "client_random").
   - Authorized Operator Signatures:
     * ["enc", term1, ..., termN, encryption_key] (Table 10.3): One or more payload terms followed by the encryption key as the LAST element.
     * ["hash", term1, ...] (Table 10.3): One-way hash digest.
     * ["cat", term1, term2, ...] (Table 10.3): Concatenation of terms.
     * ["pubk", principal_name] or ["privk", principal_name] (Table 10.3): Asymmetric key pairs.
     * ["invk", akey_var] (Table 10.3): Inverse of an asymmetric key variable.
     * ["ltk", principal1, principal2] (Table 10.3): Long-term shared symmetric key.
     * ["exp", base, expt] (Table 10.5): Exponentiation, e.g. ["exp", ["gen"], x].
     * ["gen"] (Table 10.5): 0-ary generator constant.
     * ["mul", expt1, expt2] (Table 10.5): Multiplication of exponents.
     * ["rec", expt] (Table 10.5): Multiplicative inverse of exponent.

3. Principal Roles & Executability Invariants (Tables 10.1 & 10.6, cpsa4roletran):
   - Variable Naming: Full self-explanatory semantic identifiers from the RFC (e.g. "client_identity", "client_random", "server_random", "session_key", "handshake_channel"). Never use single-letter abbreviations.
   - Populated Metadata: 'description' and 'rfc_field' must be populated for every variable.
   - Sort Mapping:
     * "name": principal identifiers
     * "text": fresh nonces and tokens
     * "data": arbitrary secrets, premaster secrets, or session payloads
     * "skey": symmetric encryption keys (keys used in ["enc", ..., key] for symmetric encryption MUST be sort "skey")
     * "akey": asymmetric keys
     * "chan": communication channels (every role must declare a channel variable, e.g. "handshake_channel")
     * "rndx": fresh Diffie-Hellman private exponents
   - Trace Events:
     * direction: "send" or "recv"
     * channel: e.g. "handshake_channel"
     * message_term: prefix term tree using valid operators or plain identifier atoms.
   - ROLETRAN EXECUTABILITY RULE: Every variable in "inputs", "outputs", and "unique_originating" MUST appear in that role's trace events!
     * "inputs": Terms known prior to execution (e.g. "handshake_channel", pre-shared keys).
     * "outputs": Established return terms (e.g. negotiated session tokens).
     * "unique_originating": Fresh nonces or secrets generated and first sent by this role.

4. Primary Secrecy & Confidentiality Goals:
   - Identify the primary confidential terms negotiated by the protocol (e.g. ["session_key"] or ["premaster_secret"]).

5. Point-of-View Preskeletons (Chapters 3 & 6):
   - POV Skeleton 1 (Initiator POV - Realized Handshake Shape):
     * strands: [defstrandmax for initiator role]
     * non_originating: uncompromised long-term/private keys (e.g. ["privk", "server_identity"])
     * unique_originating: fresh nonces generated by initiator (e.g. "client_random")
     * listeners: [] (STRICTLY EMPTY: never include deflistener in pure POV skeletons, or CPSA cannot realize the 2-party shape)
   - POV Skeleton 2 (Responder POV - Mutual Authentication):
     * strands: [defstrandmax for responder role]
     * non_originating: uncompromised long-term/private keys
     * unique_originating: fresh nonces generated by responder (e.g. "server_random")
     * listeners: [] (STRICTLY EMPTY)
   - Secrecy Skeleton 3 (Confidentiality Proof):
     * strands: [defstrandmax for initiator or responder]
     * listeners: [primary confidential term]
     * non_originating: uncompromised keys
     * unique_originating: fresh nonces

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
    response = None
    import time
    for retry_idx in range(3):
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
            if ("Timeout" in err_msg or "timed out" in err_msg or "429" in err_msg or "RateLimit" in err_msg) and retry_idx < 2:
                wait_sec = 10 * (retry_idx + 1)
                logger.warning("Extraction attempt %d failed (%s). Retrying in %ds...", retry_idx + 1, exc, wait_sec)
                time.sleep(wait_sec)
            else:
                raise

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except Exception:
        import json_repair
        data = json_repair.loads(content)

    try:
        spec = CPSAProtocolSpecification.model_validate(data)
    except ValidationError as val_err:
        logger.warning("Stage 2 schema validation error encountered: %s. Initiating 1-shot self-healing correction...", val_err)
        correction_prompt = f"""Your previous JSON output failed MITRE CPSA schema validation with the following errors:
{val_err}

CRITICAL MITRE CPSA MANUAL GROUNDING RULES (Chapter 10, Tables 10.1 - 10.6):
1. In 'message_term', terms MUST be plain string identifier atoms (e.g. 'client_random', 'session_key'), integers, or prefix lists like ['enc', payload, key].
   NEVER place variable objects or dictionaries inside message_term!
2. In ['enc', ...], the encryption key is ALWAYS the LAST element in the list.
3. Every variable in 'inputs', 'outputs', and 'unique_originating' MUST be sent or received in the role's trace!
4. Diffie-Hellman fresh exponents must be sort 'rndx'.

Return ONLY the corrected, fully valid JSON object."""
        try:
            corr_resp = litellm.completion(
                **llm_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": content},
                    {"role": "user", "content": correction_prompt},
                ],
                response_format={"type": "json_object"},
                timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
            )
            corr_content = corr_resp.choices[0].message.content
            try:
                corr_data = json.loads(corr_content)
            except Exception:
                import json_repair
                corr_data = json_repair.loads(corr_content)
            spec = CPSAProtocolSpecification.model_validate(corr_data)
            logger.info("Stage 2 self-healing correction SUCCEEDED")
        except Exception as retry_err:
            logger.error("Self-healing correction failed: %s. Raising validation error.", retry_err)
            raise val_err from retry_err

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

    # Guarantee at least one secrecy verification skeleton if a secret was semantically identified by the LLM
    final_skeletons = new_pure_skeletons
    if secrecy_skeletons:
        final_skeletons.extend(secrecy_skeletons)
    else:
        # Determine the secrecy target strictly from the LLM's semantic output:
        # Priority 1: Listeners chosen by the LLM in existing skeletons
        # Priority 2: Terms designated in spec.primary_secrecy_goals by the LLM
        secret_targets = existing_listeners or spec.primary_secrecy_goals
        if secret_targets:
            chosen_secret = secret_targets[0]
            # Bind to the principal that originates or establishes this secret
            originating_role = spec.roles[0]
            for r in spec.roles:
                if any(chosen_secret == uo or (isinstance(uo, str) and uo == chosen_secret) for uo in r.unique_originating):
                    originating_role = r
                    break

            bindings = {v.name: v.name for v in originating_role.variables}
            skel_vars = [CPSAVariableDeclaration(name=v.name, sort=v.sort) for v in originating_role.variables]
            sec_skel = CPSAPreskeleton(
                protocol_name=spec.protocol_name,
                description=f"Secrecy Verification: tests confidentiality of {chosen_secret}",
                variables=skel_vars,
                strands=[
                    CPSAStrandInstance(
                        role_name=originating_role.role_name,
                        variable_bindings=bindings,
                    )
                ],
                non_originating=dedup_non_orig,
                unique_originating=list(originating_role.unique_originating),
                listeners=[chosen_secret],
                comment=f"Secrecy Point of View: Listener on {chosen_secret}",
            )
            final_skeletons.append(sec_skel)

    spec.skeletons = final_skeletons
    return spec
