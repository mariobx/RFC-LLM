#!/usr/bin/env python3
"""
03_query_rag.py
High-precision hybrid retrieval engine querying the verbatim atomic semantic chunks of CPSA.

Supports:
- Lexical BM25 keyword scoring with title, breadcrumb, summary, and tag weighting.
- Exact phrase boosting for titles, breadcrumbs, scenario summaries, and body text.
- Dense semantic vector similarity via local embeddings.npy.
- Reciprocal Rank Fusion (RRF) combining BM25 lexical precision and dense semantic intent.
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
import numpy as np
from dotenv import load_dotenv, find_dotenv
import litellm

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(usecwd=True))
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

CHUNKS_JSONL_PATH = BASE_DIR / "chunks" / "manual_chunks.jsonl"
CHUNKS_JSON_PATH = BASE_DIR / "chunks" / "manual_chunks.json"
NPY_PATH = BASE_DIR / "chunks" / "embeddings.npy"
META_PATH = BASE_DIR / "chunks" / "embeddings_meta.json"

litellm.suppress_debug_info = True

def tokenize(text: str) -> list[str]:
    """
    DSL-aware tokenizer preserving Scheme S-expression atoms, hyphenated keywords,
    and structural markers (e.g. defprotocol, non-orig, pen-non-orig, uniq-orig, defstrand).
    """
    text_lower = text.lower()
    tokens = re.findall(r'[a-zA-Z0-9_\-]+', text_lower)
    # Capture leading Scheme operator forms like (defrole, (send, (recv, (enc, (pubk
    scheme_ops = re.findall(r'\(([a-zA-Z0-9_\-]+)', text_lower)
    tokens.extend(scheme_ops)
    return tokens

class CPSASemanticRetriever:
    def __init__(self, chunks_path: Path = None, npy_path: Path = None, meta_path: Path = None):
        self.chunks = []
        self.chunk_map = {}
        self.doc_lengths = []
        self.avg_doc_len = 0.0
        self.term_doc_freqs = Counter()
        self.total_docs = 0

        # Dense vector state
        self.embeddings = None
        self.embed_meta = {}
        self.embed_model = "ollama/nomic-embed-text"
        self.api_base = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
        self.api_key = os.environ.get("GEMINI_API_KEY", "")

        # Cross-Encoder Reranker state (FlashRank ONNX)
        self.ranker = None
        try:
            from flashrank import Ranker
            self.ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")
        except Exception:
            pass

        # 1. Load chunks
        target_chunks_path = chunks_path or (CHUNKS_JSONL_PATH if CHUNKS_JSONL_PATH.exists() else CHUNKS_JSON_PATH)
        if target_chunks_path and target_chunks_path.exists():
            self._load_from_path(target_chunks_path)

        # 2. Build BM25 Index
        self._build_bm25_index()

        # 3. Load Vector Embeddings if available
        target_npy = npy_path or NPY_PATH
        target_meta = meta_path or META_PATH
        if target_npy.exists() and target_meta.exists():
            try:
                self.embeddings = np.load(target_npy)
                with open(target_meta, "r", encoding="utf-8") as mf:
                    self.embed_meta = json.load(mf)
                self.embed_model = self.embed_meta.get("model", self.embed_model)
            except Exception as e:
                print(f"[Warning] Failed to load dense embeddings: {e}", file=sys.stderr)

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
            breadcrumb = c.get('breadcrumb') or c.get('chapter', '')
            summary = c.get('scenario_summary', '')
            ctx_hdr = c.get('context_header', '')
            tags_str = " ".join(c.get('tags', []))
            full_text = f"{c.get('title', '')} {c.get('title', '')} {breadcrumb} {ctx_hdr} {summary} {tags_str} {c.get('text', '')}"
            tokens = tokenize(full_text)
            doc_len = len(tokens)
            self.doc_lengths.append(doc_len)
            total_words += doc_len
            unique_terms = set(tokens)
            for t in unique_terms:
                self.term_doc_freqs[t] += 1

        self.avg_doc_len = total_words / self.total_docs if self.total_docs > 0 else 1.0

    def _bm25_search(self, query: str, source_filter: str = None, chunk_type: str = None) -> list[tuple[float, dict]]:
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
                idf = math.log(1.0 + (self.total_docs - df + 0.5) / (df + 0.5))
                num = tf * (k1 + 1.0)
                denom = tf + k1 * (1.0 - b + b * (doc_len / self.avg_doc_len))
                score += idf * (num / denom)

            # Exact phrase bonus
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
        return scores

    def _dense_search(self, query: str, source_filter: str = None, chunk_type: str = None) -> list[tuple[float, dict]]:
        if self.embeddings is None:
            return []

        is_nomic = "nomic" in self.embed_model.lower()
        formatted_query = f"search_query: {query}" if is_nomic else query

        try:
            kwargs = {"model": self.embed_model, "input": [formatted_query]}
            if "gemini" in self.embed_model.lower():
                kwargs["api_key"] = self.api_key
            else:
                kwargs["api_base"] = self.api_base

            res = litellm.embedding(**kwargs)
            q_vec = np.array(res.data[0]["embedding"], dtype=np.float32)
            q_norm = np.linalg.norm(q_vec)
            if q_norm > 0:
                q_vec = q_vec / q_norm

            sims = np.dot(self.embeddings, q_vec)
            scores = []
            for idx, chunk in enumerate(self.chunks):
                if chunk_type and chunk.get("chunk_type", "") != chunk_type:
                    continue
                if source_filter and source_filter.lower() not in chunk.get("source_file", "").lower():
                    continue
                if idx < len(sims):
                    scores.append((float(sims[idx]), chunk))

            scores.sort(key=lambda x: x[0], reverse=True)
            return scores
        except Exception as e:
            print(f"[Warning] Dense embedding query failed: {e}", file=sys.stderr)
            return []

    def search(self, query: str, top_k: int = 5, mode: str = "hybrid",
               source_filter: str = None, chunk_type: str = None,
               rerank: bool = True) -> list[dict]:
        """
        Unified search supporting:
        - 'bm25': pure lexical keyword search
        - 'dense': pure vector cosine similarity
        - 'hybrid': Steep RRF (k=20) combining BM25 and dense similarity
        - rerank=True: Cross-Encoder full token attention reranking via FlashRank ONNX.
        """
        if not self.chunks:
            return []

        # Fallback to BM25 if dense vectors are not available
        if mode in ["dense", "hybrid"] and self.embeddings is None:
            mode = "bm25"

        # Fetch candidate pool (top 25-30) for Stage 2 Cross-Encoder reranking
        candidate_k = max(top_k * 5, 25) if (rerank and self.ranker) else top_k

        if mode == "bm25":
            bm25_hits = self._bm25_search(query, source_filter=source_filter, chunk_type=chunk_type)
            candidates = [(s, c, "BM25") for s, c in bm25_hits[:candidate_k]]
        elif mode == "dense":
            dense_hits = self._dense_search(query, source_filter=source_filter, chunk_type=chunk_type)
            candidates = [(s, c, "Cosine") for s, c in dense_hits[:candidate_k]]
        else:
            # Stage 1: Convex MinMax Score Normalization with AST Syntax Boosting
            bm25_hits = self._bm25_search(query, source_filter=source_filter, chunk_type=chunk_type)
            dense_hits = self._dense_search(query, source_filter=source_filter, chunk_type=chunk_type)

            bm25_dict = {c["chunk_id"]: s for s, c in bm25_hits[:60]}
            dense_dict = {c["chunk_id"]: s for s, c in dense_hits[:60]}
            all_candidate_cids = set(bm25_dict.keys()) | set(dense_dict.keys())

            if bm25_dict:
                max_bm = max(bm25_dict.values())
                min_bm = min(bm25_dict.values())
                range_bm = max_bm - min_bm if max_bm > min_bm else 1.0
                norm_bm = {cid: (s - min_bm) / range_bm for cid, s in bm25_dict.items()}
            else:
                norm_bm = {}

            if dense_dict:
                max_d = max(dense_dict.values())
                min_d = min(dense_dict.values())
                range_d = max_d - min_d if max_d > min_d else 1.0
                norm_d = {cid: (s - min_d) / range_d for cid, s in dense_dict.items()}
            else:
                norm_d = {}

            # Detect exact Scheme AST tokens in query
            query_lower = query.lower()
            ast_tokens = [
                "defprotocol", "defrole", "defskeleton", "deflistener", "defmacro", "defrule", "defgenrule",
                "non-orig", "uniq-orig", "pen-non-orig", "uniq-gen", "role_uniq",
                "skey", "akey", "name", "text", "data", "mesg", "chan", "locn",
                "prec", "subsort", "auth-test", "trace", "invk", "pubk", "privk"
            ]
            matched_query_tokens = [t for t in ast_tokens if t in query_lower]

            alpha = 0.55
            fused_scores = {}
            for cid in all_candidate_cids:
                s_d = norm_d.get(cid, 0.0)
                s_b = norm_bm.get(cid, 0.0)
                base = alpha * s_d + (1.0 - alpha) * s_b

                # AST Boost: If query contains exact CPSA syntax keywords, boost chunks with matching ast_features
                if matched_query_tokens:
                    c = self.chunk_map[cid]
                    c_ast = c.get("ast_features", {})
                    c_tokens = set()
                    if isinstance(c_ast, dict):
                        for sublist in c_ast.values():
                            if isinstance(sublist, list):
                                c_tokens.update(sublist)
                    # Also check formal_metadata for .scm code chunks
                    c_meta = c.get("formal_metadata", {})
                    if isinstance(c_meta, dict):
                        for sublist in c_meta.values():
                            if isinstance(sublist, list):
                                for item in sublist:
                                    if isinstance(item, str):
                                        c_tokens.add(item)
                                    elif isinstance(item, dict) and "name" in item:
                                        c_tokens.add(item["name"])

                    overlap = c_tokens.intersection(matched_query_tokens)
                    if overlap:
                        base *= (1.0 + 0.3 * len(overlap))

                fused_scores[cid] = base

            top_ranked = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)[:candidate_k]
            candidates = [(score, self.chunk_map[cid], "Convex-AST") for cid, score in top_ranked]

        # Stage 2: Cross-Encoder Deep Token-to-Token Attention Reranking
        if rerank and self.ranker and len(candidates) > 1:
            try:
                from flashrank import RerankRequest
                passages = [
                    {
                        "id": idx,
                        "text": f"{c.get('title', '')}. {c.get('context_header', '')} {c.get('scenario_summary', '')} {c.get('breadcrumb', '')} {c.get('text', '')[:2500]}"
                    }
                    for idx, (_, c, _) in enumerate(candidates)
                ]
                rerank_req = RerankRequest(query=query, passages=passages)
                reranked_res = self.ranker.rerank(rerank_req)
                final_scored = []
                for item in reranked_res[:top_k]:
                    idx = item["id"]
                    ce_score = float(item["score"])
                    _, orig_chunk, _ = candidates[idx]
                    final_scored.append((ce_score, orig_chunk, "CrossEncoder"))
            except Exception:
                final_scored = candidates[:top_k]
        else:
            final_scored = candidates[:top_k]

        return [
            {
                "score": round(score, 4),
                "metric": metric,
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
            for score, c, metric in final_scored
        ]

    def as_dspy_tool(self):
        """
        Returns a callable tool function formatted specifically for DSPy ReAct agents.
        The agent can call this tool during RFC-to-SCM synthesis to retrieve formal models and syntax.
        """
        def search_cpsa_knowledge(query: str) -> str:
            """
            Search the CPSA formal verification knowledge base for syntax rules,
            S-expression macros, protocol models, and security goal declarations.
            Args:
                query: Natural language question, RFC section summary, or Scheme syntax query.
            Returns:
                Formatted string of top matching CPSA documentation chunks and code examples.
            """
            results = self.search(query, top_k=3, rerank=True)
            if not results:
                return "No relevant CPSA documents found."

            output = []
            for idx, r in enumerate(results, 1):
                output.append(
                    f"--- Result {idx} | {r['title']} ({r['source_file']}) [Score: {r['score']}] ---\n"
                    f"Summary: {r.get('scenario_summary', 'N/A')}\n"
                    f"Content:\n{r['text']}\n"
                )
            return "\n".join(output)

        return search_cpsa_knowledge

    def get_chunk(self, chunk_id: int) -> dict | None:
        return self.chunk_map.get(chunk_id)

def main():
    parser = argparse.ArgumentParser(description="Query CPSA Atomic Semantic Chunks.")
    parser.add_argument("query", type=str, help="Search query, technical phrase, or error message.")
    parser.add_argument("--top-k", "-k", type=int, default=3, help="Number of results to return (default: 3).")
    parser.add_argument("--mode", "-m", type=str, choices=["hybrid", "bm25", "dense"], default="hybrid",
                        help="Retrieval mode: 'hybrid' (RRF, default), 'bm25', or 'dense'.")
    parser.add_argument("--source", "-s", type=str, default=None, help="Filter by source file substring.")
    parser.add_argument("--type", "-t", type=str, default=None, help="Filter by chunk_type ('documentation' or 'code_example').")
    args = parser.parse_args()

    retriever = CPSASemanticRetriever()
    dense_status = f"ENABLED ({retriever.embeddings.shape[0]} vectors, model: {retriever.embed_model})" if retriever.embeddings is not None else "DISABLED"

    print(f"\n========================================================")
    print(f"CPSA Semantic Retriever")
    print(f"  Query:       '{args.query}'")
    print(f"  Mode:        {args.mode.upper()}")
    print(f"  Corpus:      {len(retriever.chunks)} chunks")
    print(f"  Dense Index: {dense_status}")
    print(f"========================================================\n")

    results = retriever.search(
        args.query,
        top_k=args.top_k,
        mode=args.mode,
        source_filter=args.source,
        chunk_type=args.type
    )

    if not results:
        print("No matching chunks found.")
        return

    for i, res in enumerate(results, 1):
        print(f"[{i}] {res['metric']} Score: {res['score']} | Chunk #{res['chunk_id']} | Type: {res['chunk_type']}")
        print(f"    Title:      {res['title']}")
        print(f"    Source:     {res['source_file']}")
        print(f"    Breadcrumb: {res['breadcrumb']} ({res['word_count']} words)")
        if res.get("scenario_summary"):
            print(f"    Summary:    {res['scenario_summary'][:180]}...")
        print("    " + "-" * 70)
        snippet = res['text'][:300].replace("\n", "\n    ")
        print(f"    {snippet}...")
        print("    " + "=" * 70 + "\n")

if __name__ == "__main__":
    main()
