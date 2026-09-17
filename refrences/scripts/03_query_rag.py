#!/usr/bin/env python3
"""
03_query_rag.py
High-precision retrieval engine querying the verbatim atomic semantic chunks of CPSA.

Supports:
- Lexical BM25 / keyword scoring with section title & chapter boosting.
- Optional dense semantic vector similarity via embedding models.
- Can be run as a standalone CLI tool or imported as a retrieval module in DSPy pipelines.
"""

import sys
import os
import json
import re
import argparse
import math
from pathlib import Path
from collections import Counter
from dotenv import load_dotenv, find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(usecwd=True))
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

CHUNKS_JSONL_PATH = BASE_DIR / "chunks" / "manual_chunks.jsonl"
CHUNKS_JSON_PATH = BASE_DIR / "chunks" / "manual_chunks.json"

def tokenize(text: str) -> list[str]:
    """Tokenize text preserving technical symbols, hyphens, and S-expression keywords."""
    return re.findall(r'[a-zA-Z0-9_\-\(\)]+', text.lower())

class CPSASemanticRetriever:
    def __init__(self, chunks_path: Path = None):
        self.chunks = []
        self.chunk_map = {}
        self.doc_lengths = []
        self.avg_doc_len = 0.0
        self.term_doc_freqs = Counter()
        self.total_docs = 0

        # Load chunks from jsonl first, then fallback to json
        if chunks_path:
            self._load_from_path(chunks_path)
        elif CHUNKS_JSONL_PATH.exists():
            self._load_from_path(CHUNKS_JSONL_PATH)
        elif CHUNKS_JSON_PATH.exists():
            self._load_from_path(CHUNKS_JSON_PATH)

        self._build_bm25_index()

    def _load_from_path(self, path: Path):
        if path.suffix == ".jsonl":
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            c = json.loads(line)
                            self.chunks.append(c)
                            self.chunk_map[c["chunk_id"]] = c
                        except Exception:
                            pass
        else:
            with open(path, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)
                self.chunk_map = {c["chunk_id"]: c for c in self.chunks}

    def _build_bm25_index(self):
        self.total_docs = len(self.chunks)
        if self.total_docs == 0:
            return

        total_words = 0
        for c in self.chunks:
            # Combined text for indexing with title, breadcrumb, summary, and tags weighted
            breadcrumb = c.get('breadcrumb') or c.get('chapter', '')
            summary = c.get('scenario_summary', '')
            tags_str = " ".join(c.get('tags', []))
            full_text = f"{c.get('title', '')} {c.get('title', '')} {breadcrumb} {summary} {tags_str} {c.get('text', '')}"
            tokens = tokenize(full_text)
            doc_len = len(tokens)
            self.doc_lengths.append(doc_len)
            total_words += doc_len
            unique_terms = set(tokens)
            for t in unique_terms:
                self.term_doc_freqs[t] += 1

        self.avg_doc_len = total_words / self.total_docs if self.total_docs > 0 else 1.0

    def search(self, query: str, top_k: int = 5, source_filter: str = None, chunk_type: str = None) -> list[dict]:
        """BM25 search over verbatim atomic semantic chunks and full code examples."""
        if not self.chunks:
            return []

        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        k1 = 1.5
        b = 0.75
        scores = []

        for idx, chunk in enumerate(self.chunks):
            if chunk_type and chunk.get("chunk_type", "") != chunk_type:
                continue
            if source_filter and source_filter.lower() not in chunk.get("source_file", "").lower():
                continue

            breadcrumb = chunk.get('breadcrumb') or chunk.get('chapter', '')
            summary = chunk.get('scenario_summary', '')
            tags_str = " ".join(chunk.get('tags', []))
            doc_tokens = tokenize(
                f"{chunk.get('title', '')} {chunk.get('title', '')} {breadcrumb} {summary} {tags_str} {chunk.get('text', '')}"
            )
            doc_len = self.doc_lengths[idx] if idx < len(self.doc_lengths) else len(doc_tokens)
            doc_freq = Counter(doc_tokens)

            score = 0.0
            for t in query_tokens:
                if t not in doc_freq:
                    continue
                tf = doc_freq[t]
                df = self.term_doc_freqs.get(t, 0)
                # BM25 IDF
                idf = math.log(1.0 + (self.total_docs - df + 0.5) / (df + 0.5))
                # BM25 term frequency component
                num = tf * (k1 + 1.0)
                denom = tf + k1 * (1.0 - b + b * (doc_len / self.avg_doc_len))
                score += idf * (num / denom)

            # Exact query string bonus in title, summary, or text
            q_lower = query.lower()
            if q_lower in chunk.get("title", "").lower():
                score += 8.0
            if q_lower in breadcrumb.lower():
                score += 4.0
            if summary and q_lower in summary.lower():
                score += 6.0
            if q_lower in chunk.get("text", "").lower():
                score += 3.0

            if score > 0:
                scores.append((score, chunk))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "score": round(score, 3),
                "chunk_id": c["chunk_id"],
                "chunk_type": c.get("chunk_type", "documentation"),
                "title": c.get("title"),
                "breadcrumb": c.get("breadcrumb") or c.get("chapter", ""),
                "chapter": c.get("breadcrumb") or c.get("chapter", ""),
                "source_file": c.get("source_file"),
                "word_count": c.get("word_count"),
                "scenario_summary": c.get("scenario_summary", ""),
                "tags": c.get("tags", []),
                "text": c.get("text")
            }
            for score, c in scores[:top_k]
        ]

    def get_chunk(self, chunk_id: int) -> dict | None:
        return self.chunk_map.get(chunk_id)

def main():
    parser = argparse.ArgumentParser(description="Query CPSA Atomic Semantic Chunks.")
    parser.add_argument("query", type=str, help="Search query or error message.")
    parser.add_argument("--top-k", "-k", type=int, default=3, help="Number of results to return (default: 3).")
    parser.add_argument("--source", "-s", type=str, default=None, help="Filter by source file substring.")
    args = parser.parse_args()

    retriever = CPSASemanticRetriever()
    print(f"\nSearching {len(retriever.chunks)} atomic CPSA semantic chunks for: '{args.query}'...\n")
    results = retriever.search(args.query, top_k=args.top_k, source_filter=args.source)

    if not results:
        print("No matching semantic chunks found.")
        return

    for i, res in enumerate(results, 1):
        print(f"[{i}] Score: {res['score']} | Chunk #{res['chunk_id']} | Source: {res['source_file']}")
        print(f"    Title:      {res['title']}")
        print(f"    Breadcrumb: {res['breadcrumb']} ({res['word_count']} words)")
        print("    " + "-" * 70)
        # Print first 350 chars of verbatim text
        snippet = res['text'][:350].replace("\n", "\n    ")
        print(f"    {snippet}...")
        print("    " + "=" * 70 + "\n")

if __name__ == "__main__":
    main()
