"""Shared RAG Retriever Client for MITRE CPSA 4.4.9 Reference Grounding.

Provides lazy-loaded singleton access to `CPSASemanticRetriever` (Hybrid BM25 + Dense RRF)
and standardized chunk formatting with real-time event bus telemetry for Stage 2
(Protocol Extraction) and Stages 5 & 6 (Compiler Diagnostic Self-Healing Repair).
"""

import importlib
from typing import Any, List, Optional

from src.logging_config import get_pipeline_logger
from src.pipeline_events import GLOBAL_EVENT_BUS

logger = get_pipeline_logger("rag_retriever")

_GLOBAL_RETRIEVER: Optional[Any] = None


def get_cpsa_manual_retriever() -> Optional[Any]:
    """Returns the lazy-loaded singleton `CPSASemanticRetriever` instance."""
    global _GLOBAL_RETRIEVER
    if _GLOBAL_RETRIEVER is None:
        try:
            rag_module = importlib.import_module("refrences.scripts.03_query_rag")
            retriever_cls = getattr(rag_module, "CPSASemanticRetriever")
            _GLOBAL_RETRIEVER = retriever_cls()
            logger.info("Initialized CPSASemanticRetriever for MITRE CPSA 4.4.9 manual grounding")
        except Exception as exc:
            logger.warning("Could not initialize CPSASemanticRetriever: %s", exc)
            _GLOBAL_RETRIEVER = None
    return _GLOBAL_RETRIEVER


def retrieve_cpsa_manual_guidance(
    query: str,
    stage: int,
    purpose: str,
    header_prefix: str = "Reference",
    top_k: int = 2,
    fallback_message: str = "Use standard MITRE CPSA 4.4.9 syntax conventions.",
) -> str:
    """Executes a hybrid BM25 + Dense RRF search over the MITRE CPSA 4.4.9 corpus,
    emits a `rag_retrieval` telemetry event, and returns formatted reference blocks.
    """
    retriever = get_cpsa_manual_retriever()
    if not retriever:
        return fallback_message

    try:
        search_hits = retriever.search(query, top_k=top_k, mode="hybrid", rerank=False)
        formatted_blocks: List[str] = []
        telemetry_chunks: List[dict] = []

        for idx, chunk in enumerate(search_hits, 1):
            chunk_id = chunk.get("chunk_id") or chunk.get("id") or idx
            chunk_title = chunk.get("title") or chunk.get("breadcrumb") or f"Section {idx}"
            chunk_source = chunk.get("source_file") or chunk.get("source") or "MITRE Manual"
            chunk_text = chunk.get("text") or chunk.get("content") or ""

            formatted_blocks.append(
                f"--- {header_prefix} {idx}: {chunk_title} ({chunk_source}) ---\n{chunk_text[:800]}"
            )
            telemetry_chunks.append({
                "chunk_id": str(chunk_id),
                "title": chunk_title,
                "source_file": chunk_source,
                "snippet": chunk_text[:280].strip() + ("..." if len(chunk_text) > 280 else ""),
            })

        GLOBAL_EVENT_BUS.emit(
            "rag_retrieval",
            stage=stage,
            purpose=purpose,
            query=query,
            chunks=telemetry_chunks,
        )
        if formatted_blocks:
            return "\n\n".join(formatted_blocks)
    except Exception as exc:
        logger.warning("RAG retrieval failed during %s: %s", purpose, exc)

    return fallback_message
