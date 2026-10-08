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
1. "Undeclared variable <var>":
   - A variable is declared in "inputs", "outputs", or "unique_originating", but does NOT occur anywhere in the role's trace events!
   - Fix: Remove the variable from "inputs", "outputs", and "unique_originating". In CPSA roletran, every variable in inputs/outputs/uniq-orig must actually appear in a trace send or recv.
2. "Cannot build <term>":
   - A role attempts to send a term before it has been generated ("unique_originating"), received, or passed as an input ("inputs").
   - Or, a symmetric encryption key in ["enc", payload, key] was mistakenly declared as "data" instead of "skey".
   - Fix: Change key sort to "skey". Add fresh originating terms to "unique_originating". Add known parameters or channels to "inputs".
3. "Received term cannot be fully destructured":
   - A role receives an encrypted message or hash, but lacks the necessary decryption key or preimage in its "inputs".
   - Fix: Ensure the role's "inputs" list includes the required key (e.g. held private key or shared secret) to decrypt the incoming payload.
4. Preskeleton Architecture (MANDATORY 3-SKELETON SEPARATION):
   - CRITICAL: Never put 'deflistener' inside pure POV skeletons! A listener on an uncompromised secret causes CPSA to abort without displaying the completed bilateral protocol handshake shape.
   - Separate into 3 distinct skeletons:
     * Skeleton 1: Initiator / Client POV (defstrandmax initiator, listeners: [])
     * Skeleton 2: Responder / Server POV (defstrandmax responder, listeners: [])
     * Skeleton 3: Secrecy POV (defstrandmax + deflistener for the secret)
   - Preserve uncompromised private keys under "non_originating" and fresh nonces under "unique_originating".
5. "Expecting a name":
   - An asymmetric key constructor like ["pubk", key] or ["privk", key] was passed an asymmetric key variable (sort "akey") instead of a principal identifier (sort "name").
   - Fix: In CPSA, if an asymmetric key variable 'k' is declared with sort "akey", use 'k' and ["invk", 'k'] directly without wrapping in "pubk" or "privk". "pubk" and "privk" only accept variables of sort "name".
6. "Uniquely originating value ... does not originate in trace":
   - A variable declared under "unique_originating" is only transmitted inside a ["hash", ...] one-way digest, or is never transmitted.
   - Fix: Remove the variable from "unique_originating". In CPSA, atoms cannot originate inside a one-way hash.
7. Variable Naming & Metadata Integrity:
   - Preserve all descriptive, domain-specific identifiers (e.g. "client_identity", "server_identity", "client_random", "premaster_secret"). Do NOT downgrade them to single-letter or toy abbreviations like 'a', 'b', 'init', 'resp', 'k'.
   - Preserve and update the 'description' and 'rfc_field' metadata fields.
8. NEVER Emit Foreign Operator "aenc" or "senc":
   - CPSA message algebra has NO "aenc" or "senc" operator!
   - In CPSA, ALL encryption (both symmetric and asymmetric) strictly uses "enc": ["enc", payload, key].
   - If encrypting with a public key, use ["enc", payload, ["pubk", name]] or ["enc", payload, key]. NEVER write "aenc".

Return ONLY the repaired, valid CPSAProtocolSpecification matching the requested JSON schema."""


DIAGNOSTIC_QUERY_SYSTEM_PROMPT = """You are a formal verification compiler diagnostic analyst for MITRE CPSA 4.4.9 (Cryptographic Protocol Shapes Analyzer).
Your task is to analyze a compiler/solver diagnostic error and formulate a concise, targeted search query (3 to 6 words) to retrieve the relevant formal rules from the MITRE CPSA reference manual.

CRITICAL INSTRUCTIONS FOR RETRIEVAL PRECISION:
1. ABSTRACT CONCRETE IDENTIFIERS:
   NEVER include protocol-specific variable names, role names, file paths, line numbers, or literals from the error (e.g. forbid 'client_random', 'session_id', 'tls_1_2', 'premaster_secret', 'server_hello_done', '.scm:72:6').
   Abstract them into formal CPSA grammar, algebra, or roletran concepts (e.g. 'roletran term origination trace inputs', 'defskeleton vars declaration binding', 'order-sorted algebra sort mismatch', 'asymmetric key sort rules').
2. OUTPUT FORMAT:
   Output strictly the plain text search query (3 to 6 words). Do NOT include quotes, explanations, markdown, or punctuation."""


def fallback_sanitize_diagnostic_query(diagnostic: str, failure_stage: str) -> str:
    """Fallback sanitizer for compiler diagnostics when LLM query formulation is unavailable,
    stripping file paths, line numbers, and Make boilerplate."""
    import re
    cleaned = re.sub(r'MITRE build failed for [^:]+:\s*', '', diagnostic, flags=re.IGNORECASE)
    cleaned = re.sub(r'make(\[\d+\])?:.*', '', cleaned)
    cleaned = re.sub(r'[a-zA-Z0-9_\-\./]+\.(scm|txt|xhtml|mk|hs|pl)(:\d+:\d+)?:?', '', cleaned)
    cleaned = re.sub(r'\(.*?\)', '', cleaned)
    cleaned = re.sub(r'["\':*#\n\r]', ' ', cleaned)
    tokens = [t for t in cleaned.split() if len(t) > 2 and not t.isdigit() and t.lower() not in {"error", "exit", "code", "failed"}]
    concise = " ".join(tokens[:5])
    if concise:
        return f"CPSA {failure_stage} {concise} syntax manual error rule fix"
    return f"CPSA {failure_stage} syntax manual error rule fix"


def formulate_rag_diagnostic_query(diagnostic: str, failure_stage: str, model: Optional[str] = None) -> str:
    """Uses a dedicated LLM call to formulate a targeted conceptual query for the MITRE CPSA manual,
    purging concrete variable names and local file paths. Falls back to deterministic sanitization if offline."""
    query_model = model or SYSTEM_CONFIG.DEFAULT_QUERY_MODEL
    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(query_model, temperature=0.0)
        user_prompt = f"Failure Stage: {failure_stage}\nCompiler Diagnostic:\n{diagnostic}"
        resp = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": DIAGNOSTIC_QUERY_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            timeout=10,
        )
        content = resp.choices[0].message.content
        if content:
            query = " ".join(content.strip().strip('"').strip("'").split())
            if query:
                return query
    except Exception as exc:
        logger.warning("LLM diagnostic query generation failed (%s), using fallback sanitizer", exc)

    return fallback_sanitize_diagnostic_query(diagnostic, failure_stage)


def clean_rag_diagnostic_query(diagnostic: str, failure_stage: str, model: Optional[str] = None) -> str:
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
    logger.info("Executing RAG-guided repair for stage '%s' (cycle_detected=%s) with diagnostic: %s", failure_stage, cycle_detected, error_diagnostic)

    # 1. RAG Retrieval on Compiler Diagnostic
    retrieved_guidance = []
    retriever = _get_retriever()
    if retriever:
        try:
            rag_query = formulate_rag_diagnostic_query(error_diagnostic, failure_stage, model=query_model)
            hits = retriever.search(rag_query, top_k=2, mode="hybrid", rerank=False)
            retrieved_meta = []
            for idx, chunk in enumerate(hits, 1):
                chunk_id = chunk.get("chunk_id") or chunk.get("id") or idx
                chunk_title = chunk.get("title") or chunk.get("breadcrumb") or f"Manual Section {idx}"
                chunk_source = chunk.get("source_file") or chunk.get("source") or "Manual"
                chunk_text = chunk.get("text") or chunk.get("content") or ""
                retrieved_guidance.append(f"--- Retrieved Manual Guidance {idx}: {chunk_title} ({chunk_source}) ---\n{chunk_text[:800]}")
                retrieved_meta.append({
                    "chunk_id": str(chunk_id),
                    "title": chunk_title,
                    "source_file": chunk_source,
                    "snippet": chunk_text[:280].strip() + ("..." if len(chunk_text) > 280 else ""),
                })
            from src.pipeline_events import GLOBAL_EVENT_BUS
            GLOBAL_EVENT_BUS.emit(
                "rag_retrieval",
                stage=5 if failure_stage == "roletran" else 6,
                purpose=f"Diagnostic Repair ({failure_stage})",
                query=rag_query,
                chunks=retrieved_meta,
            )
        except Exception as e:
            logger.warning("RAG retrieval failed during repair: %s", e)

    guidance_text = "\n\n".join(retrieved_guidance) if retrieved_guidance else "Review standard CPSA executability and preskeleton assumption rules."

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

    user_prompt = f"""Failing Protocol: {failing_spec.protocol_name}
Failure Stage: {failure_stage}
Compiler Diagnostic / Error:
{error_diagnostic}

MITRE CPSA Reference Guidance (Helper Only - Explains syntax rules and failure mechanisms):
{guidance_text}

Verbatim RFC Exchange Specification (Excerpt for repair context):
{slice_snippet}

Current Failing CPSA Specification (JSON):
{failing_spec.model_dump_json(indent=2)}{cycle_warning}

Provide the complete repaired CPSAProtocolSpecification resolving the error without inventing fictional protocol terms."""

    # Use higher temperature if cycle detected to break greedy minimum
    temp = 0.4 if cycle_detected else 0.0
    schema_str = json.dumps(CPSAProtocolSpecification.model_json_schema(), indent=2)
    system_prompt = f"{REPAIR_SYSTEM_PROMPT}\n\nRespond strictly with a valid JSON object matching this schema:\n{schema_str}"

    llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(model_name, temperature=temp)
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
            if ("429" in err_msg or "Quota exceeded" in err_msg or "RateLimitError" in err_msg) and retry_idx < 3:
                wait_sec = 30 * (retry_idx + 1)
                logger.warning("Quota rate limit reached during repair pass. Waiting %ds before retry: %s", wait_sec, exc)
                time.sleep(wait_sec)
            else:
                raise

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except Exception:
        import json_repair
        data = json_repair.loads(content)

    repaired_spec = CPSAProtocolSpecification.model_validate(data)
    from src.semantic_extraction.constrained_protocol_extractor import ensure_three_point_of_view_skeletons
    repaired_spec = ensure_three_point_of_view_skeletons(repaired_spec)

    logger.info("Repair pass completed for '%s'", repaired_spec.protocol_name)
    return repaired_spec
