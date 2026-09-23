#!/usr/bin/env python3
"""
04_build_embeddings.py
High-Performance Local Dense Vector Embedding Generator for CPSA Corpus.

Architecture:
- Ingests unified chunks from refrences/chunks/manual_chunks.jsonl (docs + code).
- Uses LiteLLM for unified embedding generation across cloud and local providers:
  * Gemini: gemini/text-embedding-004 (768 dimensions)
  * Ollama: ollama/nomic-embed-text (768 dimensions)
- Tailors embedding text representation:
  * Documentation: Title + Breadcrumb + Verbatim Text
  * Code Examples: Title + Breadcrumb + Tags + Scenario Summary + Verbatim SCM Code
- L2-normalizes vectors so dot product equals cosine similarity.
- Persists dense float32 matrix to refrences/chunks/embeddings.npy.
- Persists mapping metadata to refrences/chunks/embeddings_meta.json.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
import numpy as np
import backoff
from dotenv import load_dotenv, find_dotenv
import litellm

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(usecwd=True))
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

DEFAULT_CHUNKS_PATH = BASE_DIR / "chunks" / "manual_chunks.jsonl"
DEFAULT_OUTPUT_NPY = BASE_DIR / "chunks" / "embeddings.npy"
DEFAULT_OUTPUT_META = BASE_DIR / "chunks" / "embeddings_meta.json"

GEMINI_DEFAULT_MODEL = "gemini/gemini-embedding-001"
OLLAMA_DEFAULT_MODEL = "ollama/nomic-embed-text"
DEFAULT_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

# Disable verbose litellm logs
litellm.suppress_debug_info = True

def prepare_chunk_text(chunk: dict, is_nomic: bool = False) -> str:
    """Prepare enriched textual payload for embedding generation."""
    title = chunk.get("title", "").strip()
    breadcrumb = (chunk.get("breadcrumb") or chunk.get("chapter", "")).strip()
    chunk_type = chunk.get("chunk_type", "documentation")

    if chunk_type == "code_example":
        summary = chunk.get("scenario_summary", "").strip()
        tags = ", ".join(chunk.get("tags", []))
        code = chunk.get("text", "").strip()
        meta = chunk.get("formal_metadata", {})

        meta_parts = []
        if meta.get("protocols"):
            prots = ", ".join([f"{p['name']} ({p.get('algebra', 'basic')})" for p in meta["protocols"]])
            meta_parts.append(f"Protocols: {prots}")
        if meta.get("roles"):
            meta_parts.append(f"Roles: {', '.join(meta['roles'])}")
        if meta.get("crypto_primitives"):
            meta_parts.append(f"Primitives: {', '.join(meta['crypto_primitives'])}")
        if meta.get("assumptions"):
            meta_parts.append(f"Assumptions: {', '.join(meta['assumptions'])}")
        if meta.get("channels_and_state"):
            meta_parts.append(f"State/Channels: {', '.join(meta['channels_and_state'])}")

        ast_header = " | ".join(meta_parts)
        if ast_header:
            body = f"{title} | {breadcrumb}\nFormal AST: {ast_header}\nTags: {tags}\nSummary: {summary}\n\n{code}"
        else:
            body = f"{title} | {breadcrumb}\nTags: {tags}\nSummary: {summary}\n\n{code}"
    else:
        text = chunk.get("text", "").strip()
        context = chunk.get("context_header", "").strip()
        if context:
            body = f"{title} | {breadcrumb}\nContext: {context}\n\n{text}"
        else:
            body = f"{title} | {breadcrumb}\n\n{text}"

    # Prepend document instruction prefix for models that support asymmetric retrieval
    if is_nomic:
        return f"search_document: {body}"
    return body

@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=8,
    max_time=180,
    jitter=backoff.full_jitter,
    on_backoff=lambda details: print(
        f"  [RateLimit/Retry] Embedding backoff {details['wait']:.1f}s after try {details['tries']}..."
    )
)
def compute_embedding_batch(texts: list[str], model: str, api_key: str = None, api_base: str = None) -> list[list[float]]:
    """Compute dense embeddings for a batch of texts using LiteLLM."""
    kwargs = {"model": model, "input": texts}
    if api_key:
        kwargs["api_key"] = api_key
    if api_base:
        kwargs["api_base"] = api_base

    response = litellm.embedding(**kwargs)
    return [item["embedding"] for item in response.data]

def build_embeddings(
    chunks_path: Path,
    out_npy: Path,
    out_meta: Path,
    provider: str,
    model: str,
    batch_size: int,
    api_key: str,
    api_base: str
):
    if not chunks_path.exists():
        print(f"Error: Chunks file not found at {chunks_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading chunks from {chunks_path}...")
    chunks = []
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    chunks.append(json.loads(line))
                except Exception:
                    pass

    total_chunks = len(chunks)
    if total_chunks == 0:
        print("Error: No valid chunks found to embed.", file=sys.stderr)
        sys.exit(1)

    is_nomic = "nomic" in model.lower()
    doc_count = sum(1 for c in chunks if c.get("chunk_type") != "code_example")
    code_count = sum(1 for c in chunks if c.get("chunk_type") == "code_example")

    print("\n========================================================")
    print("       CPSA Local Dense Vector Embedding Builder        ")
    print("========================================================")
    print(f"  Total chunks to embed: {total_chunks} ({doc_count} docs, {code_count} code examples)")
    print(f"  Provider:              {provider.upper()}")
    print(f"  Model:                 {model}")
    print(f"  Batch size:            {batch_size}")
    print(f"  Output Matrix:         {out_npy}")
    print(f"  Output Metadata:       {out_meta}")
    print("========================================================\n")

    embeddings_list = []
    meta_entries = []
    t0 = time.time()

    for start_idx in range(0, total_chunks, batch_size):
        end_idx = min(start_idx + batch_size, total_chunks)
        batch = chunks[start_idx:end_idx]
        batch_texts = [prepare_chunk_text(c, is_nomic=is_nomic) for c in batch]

        print(f"  [Embed {start_idx+1:04d}-{end_idx:04d}/{total_chunks:04d}] Batch of {len(batch)} chunks -> {model}...")
        sys.stdout.flush()

        vectors = compute_embedding_batch(
            texts=batch_texts,
            model=model,
            api_key=api_key if provider == "gemini" else None,
            api_base=api_base if provider == "ollama" else None
        )

        embeddings_list.extend(vectors)

        for offset, c in enumerate(batch):
            meta_entries.append({
                "matrix_index": start_idx + offset,
                "chunk_id": c["chunk_id"],
                "chunk_type": c.get("chunk_type", "documentation"),
                "title": c.get("title"),
                "source_file": c.get("source_file"),
                "word_count": c.get("word_count", len(c.get("text", "").split()))
            })

    # Convert to float32 matrix
    raw_matrix = np.array(embeddings_list, dtype=np.float32)
    dim = raw_matrix.shape[1]

    # L2-normalize vectors for fast dot-product cosine similarity
    norms = np.linalg.norm(raw_matrix, axis=1, keepdims=True)
    normalized_matrix = raw_matrix / np.maximum(norms, 1e-12)

    # Save matrix and metadata
    out_npy.parent.mkdir(parents=True, exist_ok=True)
    np.save(out_npy, normalized_matrix)

    with open(out_meta, "w", encoding="utf-8") as mf:
        json.dump({
            "model": model,
            "provider": provider,
            "dimensions": dim,
            "total_chunks": total_chunks,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "chunks": meta_entries
        }, mf, indent=2, ensure_ascii=False)

    elapsed = time.time() - t0
    print("\n========================================================")
    print("Embedding Generation Complete!")
    print(f"  Saved Matrix:   {out_npy} (Shape: {normalized_matrix.shape}, {normalized_matrix.nbytes / (1024*1024):.2f} MB)")
    print(f"  Saved Metadata: {out_meta}")
    print(f"  Time Elapsed:   {elapsed:.1f}s ({total_chunks / max(elapsed, 0.001):.1f} chunks/sec)")
    print("========================================================\n")

def main():
    parser = argparse.ArgumentParser(description="Generate local dense vector embeddings for CPSA chunks.")
    parser.add_argument("--chunks", type=str, default=str(DEFAULT_CHUNKS_PATH),
                        help=f"Path to manual_chunks.jsonl. Default: {DEFAULT_CHUNKS_PATH}")
    parser.add_argument("--out-matrix", type=str, default=str(DEFAULT_OUTPUT_NPY),
                        help=f"Output .npy file path. Default: {DEFAULT_OUTPUT_NPY}")
    parser.add_argument("--out-meta", type=str, default=str(DEFAULT_OUTPUT_META),
                        help=f"Output metadata JSON path. Default: {DEFAULT_OUTPUT_META}")
    parser.add_argument("--provider", "-p", type=str, choices=["gemini", "ollama"], default="gemini",
                        help="Embedding provider ('gemini' or 'ollama'). Default: gemini")
    parser.add_argument("--model", "-m", type=str, default=None,
                        help="Embedding model tag. Default: gemini/text-embedding-004 or ollama/nomic-embed-text")
    parser.add_argument("--batch-size", "-b", type=int, default=32,
                        help="Batch size for embedding generation. Default: 32")
    parser.add_argument("--api-key", type=str, default=None,
                        help="API key for Gemini (defaults to GEMINI_API_KEY from .env)")
    parser.add_argument("--api-base", type=str, default=DEFAULT_API_BASE,
                        help=f"Ollama API base URL. Default: {DEFAULT_API_BASE}")
    args = parser.parse_args()

    provider = args.provider.lower()
    if provider == "gemini":
        model = args.model or GEMINI_DEFAULT_MODEL
        api_key = args.api_key or os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            print("Error: GEMINI_API_KEY is required for Gemini embeddings.", file=sys.stderr)
            sys.exit(1)
    else:
        model = args.model or OLLAMA_DEFAULT_MODEL
        if not model.startswith("ollama/"):
            model = f"ollama/{model}"
        api_key = None

    build_embeddings(
        chunks_path=Path(args.chunks).resolve(),
        out_npy=Path(args.out_matrix).resolve(),
        out_meta=Path(args.out_meta).resolve(),
        provider=provider,
        model=model,
        batch_size=args.batch_size,
        api_key=api_key,
        api_base=args.api_base
    )

if __name__ == "__main__":
    main()
