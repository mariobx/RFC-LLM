# Operational RAG Scripts, Evaluation Harnesses & Test Suites

> Tier 3 — Operational RAG chunking/embedding/enrichment pipeline scripts (`refrences/scripts/`), shell pipeline runner (`refrences/run_rag_pipeline.sh`), retrieval evaluation and clustering scripts (`refrences/reports/`), LaTeX report source, and the complete pytest unit and integration test suite (`tests/`).

*Generated: 2026-10-19 21:48:59 UTC · Git: `main` @ `9d27f26fb814` · Tier: Tier 3 — Operational Scripts, Pipelines & Test Suites · Files: 14 · Estimated Tokens: ~51,906*

## Table of Contents

- [`refrences/reports/evaluate_rag.py`](#refrencesreportsevaluate-ragpy)
- [`refrences/reports/plot_clusters.py`](#refrencesreportsplot-clusterspy)
- [`refrences/reports/rag_evaluation_report.tex`](#refrencesreportsrag-evaluation-reporttex)
- [`refrences/run_rag_pipeline.sh`](#refrencesrun-rag-pipelinesh)
- [`refrences/scripts/01_extract_chunks.py`](#refrencesscripts01-extract-chunkspy)
- [`refrences/scripts/02_extract_code_examples.py`](#refrencesscripts02-extract-code-examplespy)
- [`refrences/scripts/03_query_rag.py`](#refrencesscripts03-query-ragpy)
- [`refrences/scripts/04_build_embeddings.py`](#refrencesscripts04-build-embeddingspy)
- [`refrences/scripts/05_enrich_doc_chunks.py`](#refrencesscripts05-enrich-doc-chunkspy)
- [`tests/test_code_generation_and_verification.py`](#teststest-code-generation-and-verificationpy)
- [`tests/test_cpsa_scoping_and_prompts.py`](#teststest-cpsa-scoping-and-promptspy)
- [`tests/test_document_ingestion.py`](#teststest-document-ingestionpy)
- [`tests/test_main_pipeline_orchestrator.py`](#teststest-main-pipeline-orchestratorpy)
- [`tests/test_visualizer_and_events.py`](#teststest-visualizer-and-eventspy)

---

### `refrences/reports/evaluate_rag.py`

*sha256:`43ff894da40f` · 590 lines · 25.8 KB (~6,596 tokens) · lang:`python`*

```python
#!/usr/bin/env python3
"""
evaluate_rag.py
Comprehensive 300-Query Benchmark Harness across Non-SDLS CPSA Knowledge Corpus.
Evaluates:
  1. Sparse BM25
  2. Dense Vector (Nomic 768-D)
  3. Hybrid RRF-20 (Steep reciprocal rank decay, k=20)
  4. Hybrid Convex-AST (Normalized Score Fusion: 0.55 Dense + 0.45 BM25 + AST Exact Boost)
  5. Two-Stage Cross-Encoder Rerank (Convex-AST Candidate Pool + FlashRank MiniLM-L-12)

Generates 5 publication-grade comparative figures for the Visual LaTeX Dashboard:
  - fig1_recall_progression.png: Hit@K progression across K in [1, 10]
  - fig2_category_mrr.png: MRR across the 4 query domains
  - fig3_latency_pareto.png: Latency vs. Retrieval Quality Pareto Frontier
  - fig4_rank_distribution.png: Target chunk rank position distributions (Rank 1 vs 2-3 vs 4-10 vs Miss)
  - fig5_complementarity.png: Lexical vs. Semantic Complementarity & Query Recovery Analysis
"""

import sys
import os
import time
import json
import math
import logging
from pathlib import Path
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

# Suppress noisy LiteLLM logs
os.environ["LITELLM_LOG"] = "ERROR"
logging.getLogger("LiteLLM").setLevel(logging.ERROR)

REPORTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = REPORTS_DIR.parent.parent

import importlib.util
query_rag_path = REPORTS_DIR.parent / "scripts" / "03_query_rag.py"
spec = importlib.util.spec_from_file_location("query_rag_module", str(query_rag_path))
query_rag_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(query_rag_mod)
CPSASemanticRetriever = query_rag_mod.CPSASemanticRetriever
import litellm

BENCHMARK_PATH = REPORTS_DIR / "golden_benchmark.jsonl"
OUT_JSON_PATH = REPORTS_DIR / "benchmark_results.json"
FIG_DIR = REPORTS_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def compute_ndcg(retrieved_ids: list[int], target_ids: set[int], k: int) -> float:
    rel = [1 if cid in target_ids else 0 for cid in retrieved_ids[:k]]
    dcg = sum(r / math.log2(idx + 2) for idx, r in enumerate(rel))
    num_possible = min(k, len(target_ids))
    if num_possible == 0:
        return 0.0
    idcg = sum(1.0 / math.log2(idx + 2) for idx in range(num_possible))
    return dcg / idcg if idcg > 0 else 0.0

def evaluate_retriever(
    benchmark_path: Path = BENCHMARK_PATH,
    out_json_path: Path = OUT_JSON_PATH,
    fig_dir: Path = FIG_DIR,
    generate_figs: bool = True
):
    print("=" * 80)
    print(f"CPSA RETRIEVAL EVALUATION: 5-ARCHITECTURE COMPARISON")
    print(f"Benchmark Dataset: {benchmark_path.name}")
    print("=" * 80)

    with open(benchmark_path, "r", encoding="utf-8") as f:
        queries = [json.loads(line) for line in f if line.strip()]
    num_queries = len(queries)
    print(f"Loaded {num_queries} verified non-SDLS benchmark queries.")

    print("Initializing CPSASemanticRetriever...")
    retriever = CPSASemanticRetriever()
    print(f"Corpus initialized: {len(retriever.chunks)} chunks, matrix shape: {retriever.embeddings.shape}\n")

    # Batch pre-embed all queries in batches of 50
    print(f"Pre-computing dense embeddings for {num_queries} queries via Ollama (batch size 50)...")
    batch_size = 50
    all_q_vecs = []
    embed_latencies = []
    for b_start in range(0, num_queries, batch_size):
        b_queries = [f"search_query: {q['query']}" for q in queries[b_start : b_start + batch_size]]
        t0 = time.perf_counter()
        res = litellm.embedding(
            model=retriever.embed_model,
            api_base=retriever.api_base,
            input=b_queries
        )
        t1 = time.perf_counter()
        b_lat_ms = (t1 - t0) * 1000.0 / len(b_queries)
        for item in res.data:
            vec = np.array(item["embedding"], dtype=np.float32)
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            all_q_vecs.append(vec)
            embed_latencies.append(b_lat_ms)
        print(f"  Embedded queries {b_start+1} to {min(b_start+batch_size, num_queries)} ({b_lat_ms:.1f}ms/query)")
    print("All query embeddings generated.\n")

    methods = ["bm25", "dense", "hybrid_rrf20", "convex_ast", "two_stage_rerank"]
    results = {m: [] for m in methods}
    latencies = {m: [] for m in methods}

    ast_syntax_tokens = [
        "defprotocol", "defrole", "defskeleton", "deflistener", "defmacro", "defrule", "defgenrule",
        "non-orig", "uniq-orig", "pen-non-orig", "uniq-gen", "role_uniq",
        "skey", "akey", "name", "text", "data", "mesg", "chan", "locn",
        "prec", "subsort", "auth-test", "trace", "invk", "pubk", "privk"
    ]

    print("Running multi-architecture retrieval evaluation across 300 queries...")
    for idx, q in enumerate(queries):
        qid = q["query_id"]
        cat = q["category"]
        query_text = q["query"]
        target_ids = set(q["target_chunk_ids"])
        q_vec = all_q_vecs[idx]
        base_embed_lat = embed_latencies[idx]

        # 1. BM25 Search
        t0_bm = time.perf_counter()
        bm25_hits = retriever._bm25_search(query_text)
        t1_bm = time.perf_counter()
        bm_lat = (t1_bm - t0_bm) * 1000.0

        # 2. Dense Cosine Search
        t0_d = time.perf_counter()
        sims = np.dot(retriever.embeddings, q_vec)
        dense_hits = [(float(sims[c_idx]), c) for c_idx, c in enumerate(retriever.chunks)]
        dense_hits.sort(key=lambda x: x[0], reverse=True)
        t1_d = time.perf_counter()
        dense_lat = base_embed_lat + (t1_d - t0_d) * 1000.0

        # Method 1: BM25
        m1_ids = [c["chunk_id"] for _, c in bm25_hits[:10]]
        latencies["bm25"].append(bm_lat)

        # Method 2: Dense
        m2_ids = [c["chunk_id"] for _, c in dense_hits[:10]]
        latencies["dense"].append(dense_lat)

        # Method 3: Hybrid RRF-20
        t0_rrf20 = time.perf_counter()
        rrf20_scores = Counter()
        for rank, (_, c) in enumerate(bm25_hits[:40], 1):
            rrf20_scores[c["chunk_id"]] += 1.0 / (20.0 + rank)
        for rank, (_, c) in enumerate(dense_hits[:40], 1):
            rrf20_scores[c["chunk_id"]] += 1.0 / (20.0 + rank)
        m3_ids = [cid for cid, _ in rrf20_scores.most_common(10)]
        t1_rrf20 = time.perf_counter()
        latencies["hybrid_rrf20"].append(bm_lat + dense_lat + (t1_rrf20 - t0_rrf20) * 1000.0)

        # Method 4: Convex MinMax + AST Boost
        t0_cvx = time.perf_counter()
        bm25_dict = {c["chunk_id"]: s for s, c in bm25_hits[:60]}
        dense_dict = {c["chunk_id"]: s for s, c in dense_hits[:60]}
        all_cids = set(bm25_dict.keys()) | set(dense_dict.keys())

        if bm25_dict:
            max_bm, min_bm = max(bm25_dict.values()), min(bm25_dict.values())
            rng_bm = max_bm - min_bm if max_bm > min_bm else 1.0
            norm_bm = {cid: (s - min_bm) / rng_bm for cid, s in bm25_dict.items()}
        else:
            norm_bm = {}

        if dense_dict:
            max_d, min_d = max(dense_dict.values()), min(dense_dict.values())
            rng_d = max_d - min_d if max_d > min_d else 1.0
            norm_d = {cid: (s - min_d) / rng_d for cid, s in dense_dict.items()}
        else:
            norm_d = {}

        ql = query_text.lower()
        matched_tokens = [t for t in ast_syntax_tokens if t in ql]
        alpha = 0.55
        cvx_scores = {}
        for cid in all_cids:
            base = alpha * norm_d.get(cid, 0.0) + (1.0 - alpha) * norm_bm.get(cid, 0.0)
            if matched_tokens and cid in retriever.chunk_map:
                c = retriever.chunk_map[cid]
                c_tokens = set()
                c_ast = c.get("ast_features", {})
                if isinstance(c_ast, dict):
                    for sl in c_ast.values():
                        if isinstance(sl, list):
                            c_tokens.update(sl)
                c_meta = c.get("formal_metadata", {})
                if isinstance(c_meta, dict):
                    for sl in c_meta.values():
                        if isinstance(sl, list):
                            for it in sl:
                                if isinstance(it, str):
                                    c_tokens.add(it)
                                elif isinstance(it, dict) and "name" in it:
                                    c_tokens.add(it["name"])
                if c_tokens.intersection(matched_tokens):
                    base *= 1.40
            cvx_scores[cid] = base

        sorted_cvx = sorted(cvx_scores.items(), key=lambda x: x[1], reverse=True)
        m4_ids = [cid for cid, _ in sorted_cvx[:10]]
        t1_cvx = time.perf_counter()
        latencies["convex_ast"].append(bm_lat + dense_lat + (t1_cvx - t0_cvx) * 1000.0)

        # Method 5: Two-Stage Rerank (Convex-AST top 25 -> FlashRank MiniLM-L-12)
        t0_ce = time.perf_counter()
        top_candidates = [retriever.chunk_map[cid] for cid, _ in sorted_cvx[:25] if cid in retriever.chunk_map]
        try:
            from flashrank import RerankRequest
            passages = [
                {
                    "id": p_idx,
                    "text": f"{c.get('title', '')}. {c.get('context_header', '')} {c.get('scenario_summary', '')} {c.get('breadcrumb', '')} {c.get('text', '')[:2500]}"
                }
                for p_idx, c in enumerate(top_candidates)
            ]
            rerank_req = RerankRequest(query=query_text, passages=passages)
            ce_res = retriever.ranker.rerank(rerank_req)
            m5_ids = [top_candidates[item["id"]]["chunk_id"] for item in ce_res[:10]]
        except Exception:
            m5_ids = m4_ids
        t1_ce = time.perf_counter()
        latencies["two_stage_rerank"].append(bm_lat + dense_lat + (t1_ce - t0_ce) * 1000.0)

        method_id_map = {
            "bm25": m1_ids,
            "dense": m2_ids,
            "hybrid_rrf20": m3_ids,
            "convex_ast": m4_ids,
            "two_stage_rerank": m5_ids
        }

        for m in methods:
            retrieved_ids = method_id_map[m]
            hit_k = {k: (1.0 if any(cid in target_ids for cid in retrieved_ids[:k]) else 0.0) for k in range(1, 11)}

            first_rank = None
            rr = 0.0
            for rank_pos, cid in enumerate(retrieved_ids[:10], 1):
                if cid in target_ids:
                    first_rank = rank_pos
                    rr = 1.0 / rank_pos
                    break

            results[m].append({
                "query_id": qid,
                "category": cat,
                "hit_k": hit_k,
                "first_rank": first_rank,
                "rr": rr,
                "ndcg5": compute_ndcg(retrieved_ids, target_ids, 5),
                "ndcg10": compute_ndcg(retrieved_ids, target_ids, 10),
                "retrieved": retrieved_ids,
                "targets": list(target_ids)
            })

        if (idx + 1) % 50 == 0 or (idx + 1) == num_queries:
            print(f"Evaluated {idx+1:3d}/{num_queries} queries...")

    # 3. Aggregate Global and Category Metrics
    summary = {}
    for m in methods:
        recs = results[m]
        summary[m] = {
            "hit1": float(np.mean([r["hit_k"][1] for r in recs])),
            "hit2": float(np.mean([r["hit_k"][2] for r in recs])),
            "hit3": float(np.mean([r["hit_k"][3] for r in recs])),
            "hit5": float(np.mean([r["hit_k"][5] for r in recs])),
            "hit10": float(np.mean([r["hit_k"][10] for r in recs])),
            "hit_k_progression": [float(np.mean([r["hit_k"][k] for r in recs])) for k in range(1, 11)],
            "mrr": float(np.mean([r["rr"] for r in recs])),
            "ndcg5": float(np.mean([r["ndcg5"] for r in recs])),
            "ndcg10": float(np.mean([r["ndcg10"] for r in recs])),
            "avg_latency_ms": float(np.mean(latencies[m])),
            "rank_distribution": {
                "rank_1": float(np.mean([1 if r["first_rank"] == 1 else 0 for r in recs])),
                "rank_2_3": float(np.mean([1 if r["first_rank"] in (2, 3) else 0 for r in recs])),
                "rank_4_5": float(np.mean([1 if r["first_rank"] in (4, 5) else 0 for r in recs])),
                "rank_6_10": float(np.mean([1 if r["first_rank"] is not None and 6 <= r["first_rank"] <= 10 else 0 for r in recs])),
                "miss": float(np.mean([1 if r["first_rank"] is None else 0 for r in recs]))
            }
        }

    categories = sorted(list({q["category"] for q in queries}))
    cat_breakdown = {m: {} for m in methods}
    for m in methods:
        for cat in categories:
            cat_recs = [r for r in results[m] if r["category"] == cat]
            cat_breakdown[m][cat] = {
                "count": len(cat_recs),
                "hit1": float(np.mean([r["hit_k"][1] for r in cat_recs])),
                "hit3": float(np.mean([r["hit_k"][3] for r in cat_recs])),
                "hit5": float(np.mean([r["hit_k"][5] for r in cat_recs])),
                "mrr": float(np.mean([r["rr"] for r in cat_recs])),
                "ndcg5": float(np.mean([r["ndcg5"] for r in cat_recs]))
            }

    # Complementarity Analysis between BM25, Dense, and Two-Stage Rerank (Top-3)
    num_q = len(queries)
    both_hit = 0
    dense_only = 0
    bm25_only = 0
    rerank_rescued = 0
    all_miss = 0

    for i in range(num_q):
        bm_hit = results["bm25"][i]["hit_k"][3] > 0
        dn_hit = results["dense"][i]["hit_k"][3] > 0
        re_hit = results["two_stage_rerank"][i]["hit_k"][3] > 0

        if bm_hit and dn_hit:
            both_hit += 1
        elif dn_hit and not bm_hit:
            dense_only += 1
        elif bm_hit and not dn_hit:
            bm25_only += 1
        elif re_hit and not dn_hit and not bm_hit:
            rerank_rescued += 1
        else:
            all_miss += 1

    complementarity = {
        "both_top3": both_hit,
        "dense_only_top3": dense_only,
        "bm25_only_top3": bm25_only,
        "rerank_rescued_top3": rerank_rescued,
        "all_missed_top3": all_miss,
        "total_queries": num_q
    }

    print("\n" + "=" * 96)
    print(f"{'Method':<18} | {'Hit@1':<8} | {'Hit@3':<8} | {'Hit@5':<8} | {'Hit@10':<8} | {'MRR':<8} | {'NDCG@5':<8} | {'Lat (ms)':<8}")
    print("-" * 96)
    for m in methods:
        s = summary[m]
        print(f"{m.upper():<18} | {s['hit1']*100:6.1f}%  | {s['hit3']*100:6.1f}%  | {s['hit5']*100:6.1f}%  | {s['hit10']*100:6.1f}%  | {s['mrr']:6.3f}   | {s['ndcg5']:6.3f}   | {s['avg_latency_ms']:6.1f}ms")
    print("=" * 96)
    print(f"Top-3 Complementarity: Both={both_hit}, Dense-Only={dense_only}, BM25-Only={bm25_only}, Rerank-Rescued={rerank_rescued}, Miss={all_miss}\n")

    # Save JSON results
    export_payload = {
        "benchmark_meta": {
            "num_queries": len(queries),
            "corpus_chunks": len(retriever.chunks),
            "categories": categories
        },
        "summary": summary,
        "category_breakdown": cat_breakdown,
        "complementarity": complementarity
    }
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(export_payload, f, indent=2)
    print(f"Saved complete evaluation payload to: {out_json_path}\n")

    # 4. Generate 5 Dashboard Figures
    if generate_figs:
        generate_figures(summary, cat_breakdown, categories, complementarity, fig_dir)
    return export_payload

def generate_figures(summary, cat_breakdown, categories, complementarity, fig_dir: Path = FIG_DIR):
    fig_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        'font.size': 10,
        'font.family': 'sans-serif',
        'axes.labelsize': 10.5,
        'axes.titlesize': 11.5,
        'xtick.labelsize': 9.0,
        'ytick.labelsize': 9.0,
        'figure.autolayout': True,
        'figure.dpi': 300
    })

    methods = ["bm25", "dense", "hybrid_rrf20", "convex_ast", "two_stage_rerank"]
    method_labels = ["Sparse BM25", "Dense (768-D)", "Hybrid (RRF-20)", "Convex-AST", "Two-Stage Rerank"]
    palette = ["#2563EB", "#D97706", "#059669", "#7C3AED", "#DC2626"]
    markers = ["o", "^", "s", "D", "*"]

    # -------------------------------------------------------------
    # Figure 1: Cumulative Recall Progression (Hit@K, K=1..10)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ks = np.arange(1, 11)
    for m, label, col, mark in zip(methods, method_labels, palette, markers):
        curve = summary[m]["hit_k_progression"]
        lw = 2.4 if m == "two_stage_rerank" else 1.6
        ms = 9 if m == "two_stage_rerank" else 5.5
        ax.plot(ks, [v * 100 for v in curve], label=label, color=col, marker=mark, linewidth=lw, markersize=ms, alpha=0.92)

    ax.set_xlabel("Retrieval Cutoff (K)", fontweight="bold")
    ax.set_ylabel("Cumulative Hit Rate (%)", fontweight="bold")
    ax.set_title("Recall Progression Across Cutoffs (Hit@1 to Hit@10)", fontweight="bold", pad=10)
    ax.set_xticks(ks)
    ax.set_ylim(60, 102)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", loc="lower right", fontsize=8.0)
    plt.savefig(fig_dir / "fig1_recall_progression.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Figure 2: Category MRR Breakdown Across 4 Domains
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    x_cats = np.arange(len(categories))
    width = 0.16

    for idx, (m, label, col) in enumerate(zip(methods, method_labels, palette)):
        cat_mrrs = [cat_breakdown[m][c]["mrr"] for c in categories]
        rects = ax.bar(x_cats + (idx - 2) * width, cat_mrrs, width, label=label, color=col, alpha=0.92, edgecolor="#1E293B", linewidth=0.6)
        for rect in rects:
            h = rect.get_height()
            ax.annotate(f"{h:.2f}",
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 2),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=6.8, fontweight='bold')

    ax.set_ylabel("Mean Reciprocal Rank (MRR)", fontweight="bold")
    ax.set_title("Domain Performance Breakdown (MRR Across 4 Categories)", fontweight="bold", pad=10)
    ax.set_xticks(x_cats)
    ax.set_xticklabels([c.replace(" ", "\n") for c in categories], fontweight="bold")
    ax.set_ylim(0, 1.15)
    ax.grid(axis='y', linestyle='--', alpha=0.35)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", loc="upper left", ncol=3, fontsize=7.5)
    plt.savefig(fig_dir / "fig2_category_mrr.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Figure 3: Latency vs. Retrieval Quality (MRR) Pareto Frontier
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    
    lat_pts = [summary[m]["avg_latency_ms"] for m in methods]
    mrr_pts = [summary[m]["mrr"] for m in methods]
    
    for m, label, col, mark, lat, mrr in zip(methods, method_labels, palette, markers, lat_pts, mrr_pts):
        ax.scatter(lat, mrr, color=col, s=140, marker=mark, edgecolor="#0F172A", linewidth=1.2, zorder=4, label=label)
        offset_y = 0.007 if m != "hybrid_rrf20" else -0.013
        offset_x = 2.0 if m != "two_stage_rerank" else -14.0
        ax.annotate(f"{label}\n({lat:.1f}ms, {mrr:.3f})",
                    xy=(lat, mrr),
                    xytext=(lat + offset_x, mrr + offset_y),
                    fontsize=7.8, fontweight="bold", color=col,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="#F8FAFC", edgecolor=col, alpha=0.85))

    # Connect Pareto frontier points
    pareto_idx = [0, 1, 3, 4]
    p_lats = [lat_pts[i] for i in pareto_idx]
    p_mrrs = [mrr_pts[i] for i in pareto_idx]
    ax.plot(p_lats, p_mrrs, linestyle="--", color="#0F172A", linewidth=1.5, alpha=0.6, label="Pareto Frontier", zorder=3)
    ax.fill_between(p_lats, p_mrrs, 0.70, color="#E2E8F0", alpha=0.4, zorder=1)

    ax.set_xlabel("Mean Query Latency (ms)", fontweight="bold")
    ax.set_ylabel("Mean Reciprocal Rank (MRR)", fontweight="bold")
    ax.set_title("Latency vs. Retrieval Quality (Pareto Efficiency)", fontweight="bold", pad=10)
    ax.set_ylim(0.72, 0.92)
    ax.set_xlim(0, max(lat_pts) * 1.15)
    ax.grid(True, linestyle="--", alpha=0.35)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", loc="lower right", fontsize=8.0)
    plt.savefig(fig_dir / "fig3_latency_pareto.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Figure 4: Target Rank Position Distribution (Concentration)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    y_pos = np.arange(len(methods))
    
    r1 = [summary[m]["rank_distribution"]["rank_1"] * 100 for m in methods]
    r23 = [summary[m]["rank_distribution"]["rank_2_3"] * 100 for m in methods]
    r45 = [summary[m]["rank_distribution"]["rank_4_5"] * 100 for m in methods]
    r610 = [summary[m]["rank_distribution"]["rank_6_10"] * 100 for m in methods]
    miss = [summary[m]["rank_distribution"]["miss"] * 100 for m in methods]

    c_r1 = "#10B981"   # Emerald
    c_r23 = "#3B82F6"  # Blue
    c_r45 = "#F59E0B"  # Amber
    c_r610 = "#8B5CF6" # Violet
    c_miss = "#EF4444" # Crimson

    p1 = ax.barh(y_pos, r1, color=c_r1, edgecolor="#1E293B", linewidth=0.5, label="Rank 1 (Immediate Hit)")
    p2 = ax.barh(y_pos, r23, left=r1, color=c_r23, edgecolor="#1E293B", linewidth=0.5, label="Rank 2–3")
    left_45 = [a + b for a, b in zip(r1, r23)]
    p3 = ax.barh(y_pos, r45, left=left_45, color=c_r45, edgecolor="#1E293B", linewidth=0.5, label="Rank 4–5")
    left_610 = [a + b for a, b in zip(left_45, r45)]
    p4 = ax.barh(y_pos, r610, left=left_610, color=c_r610, edgecolor="#1E293B", linewidth=0.5, label="Rank 6–10")
    left_miss = [a + b for a, b in zip(left_610, r610)]
    p5 = ax.barh(y_pos, miss, left=left_miss, color=c_miss, edgecolor="#1E293B", linewidth=0.5, label="Miss (>10)")

    for idx in range(len(methods)):
        val_r1 = r1[idx]
        if val_r1 > 20:
            ax.text(val_r1 / 2, idx, f"{val_r1:.1f}%", ha='center', va='center', color="#FFFFFF", fontweight="bold", fontsize=8.0)
        val_miss = miss[idx]
        if val_miss > 1.5:
            ax.text(99.0, idx, f"{val_miss:.1f}%", ha='right', va='center', color="#FFFFFF", fontweight="bold", fontsize=7.2)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(method_labels, fontweight="bold")
    ax.set_xlabel("Proportion of Queries (%)", fontweight="bold")
    ax.set_title("Target Chunk Rank Position Distribution", fontweight="bold", pad=10)
    ax.set_xlim(0, 100)
    ax.grid(axis='x', linestyle='--', alpha=0.35)
    ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#CBD5E1", loc="lower left", bbox_to_anchor=(0.0, 1.02), ncol=3, fontsize=7.5)
    plt.savefig(fig_dir / "fig4_rank_distribution.png", dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # Figure 5: Complementarity & Query Recovery Analysis
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    comp_labels = [
        "Dual Top-3 Hits\n(Dense + BM25)",
        "Dense-Only Top-3\n(Semantic)",
        "BM25-Only Top-3\n(Exact Keyword)",
        "Rerank Rescued\n(Elevated to Top-3)",
        "All Missed\n(>Rank 3)"
    ]
    counts = [
        complementarity["both_top3"],
        complementarity["dense_only_top3"],
        complementarity["bm25_only_top3"],
        complementarity["rerank_rescued_top3"],
        complementarity["all_missed_top3"]
    ]
    pcts = [c / complementarity["total_queries"] * 100 for c in counts]
    comp_colors = ["#10B981", "#3B82F6", "#F59E0B", "#8B5CF6", "#EF4444"]

    bars = ax.bar(comp_labels, pcts, color=comp_colors, alpha=0.92, edgecolor="#1E293B", linewidth=0.7, width=0.55)
    for bar, c, p in zip(bars, counts, pcts):
        h = bar.get_height()
        ax.annotate(f"{c} q ({p:.1f}%)",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8.0, fontweight='bold')

    ax.set_ylabel("Proportion of Queries (%)", fontweight="bold")
    ax.set_title("Lexical vs. Semantic Complementarity & Query Recovery", fontweight="bold", pad=10)
    ax.set_ylim(0, max(pcts) * 1.18)
    ax.grid(axis='y', linestyle='--', alpha=0.35)
    plt.savefig(fig_dir / "fig5_complementarity.png", dpi=300)
    plt.close()

    print(f"Generated 5 publication-grade figures in {fig_dir}:")
    print("  - fig1_recall_progression.png")
    print("  - fig2_category_mrr.png")
    print("  - fig3_latency_pareto.png")
    print("  - fig4_rank_distribution.png")
    print("  - fig5_complementarity.png\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate CPSA RAG Retrieval Architectures.")
    parser.add_argument("--benchmark", "-b", type=str, default=str(BENCHMARK_PATH),
                        help="Path to benchmark JSON/JSONL file.")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Path to output JSON results.")
    parser.add_argument("--fig-dir", "-f", type=str, default=None,
                        help="Directory to save generated figures.")
    parser.add_argument("--no-figs", action="store_true",
                        help="Skip generating figure PNGs.")
    args = parser.parse_args()

    bench_path = Path(args.benchmark).resolve()
    if args.output:
        out_path = Path(args.output).resolve()
    elif bench_path.name != "golden_benchmark.jsonl":
        stem = bench_path.stem
        out_path = REPORTS_DIR / f"benchmark_results_{stem}.json"
    else:
        out_path = OUT_JSON_PATH

    if args.fig_dir:
        target_fig_dir = Path(args.fig_dir).resolve()
    elif bench_path.name != "golden_benchmark.jsonl":
        target_fig_dir = REPORTS_DIR / f"figures_{bench_path.stem}"
    else:
        target_fig_dir = FIG_DIR

    evaluate_retriever(
        benchmark_path=bench_path,
        out_json_path=out_path,
        fig_dir=target_fig_dir,
        generate_figs=not args.no_figs
    )
```

---

### `refrences/reports/plot_clusters.py`

*sha256:`8ef9166c5e29` · 1278 lines · 49.0 KB (~12,553 tokens) · lang:`python`*

```python
#!/usr/bin/env python3
"""
plot_clusters.py
High-Dimensional Dense Vector Embedding Multi-Projection Cluster Visualizer with Real-Time RAG Search Engine.

Features:
- Solid Engineering Dark Mode (zero glassmorphism, zero blur textures, high contrast).
- Mathematically Optimal Color Palette:
  Uniformly sampled in HCL/CIELAB space with maximum chroma (0.95), constant luminance (0.62),
  and a 150-degree chromatic jump stride so no two adjacent categories share a hue.
- Distinct geometric marker symbols for every category.
- Physical White Outline on all Code Models (.scm) for immediate visual identification.
- Clean category names (removed [CODE] and [DOCS] prefixes).
- 7 Projections Switchable via Flat Control Header:
  1. UMAP (Balanced Topology): n_neighbors=25, min_dist=0.3
  2. UMAP (Clustered Islands): n_neighbors=15, min_dist=0.05
  3. UMAP (Global Spread): n_neighbors=50, min_dist=0.5
  4. t-SNE (Standard Perplexity=35)
  5. t-SNE (Macro Perplexity=65)
  6. PCA (Linear Variance / Unwarped)
  7. Truncated SVD / LSA (Semantic Axes)
- Strict Top-10 Highlight Search Engine:
  Highlights strictly the Top 10 matching points for any question.
  Preserves EXACT shape and EXACT category color for all points.
  Highlights with an increased marker size and crisp white stroke outline.
  All background points softly dimmed to 15% opacity.
  Zero emojis, zero decorative glass/AI styling.
"""

import os
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
import umap
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_DIR = BASE_DIR / "chunks"
REPORTS_DIR = BASE_DIR / "reports"
REPO_ROOT = BASE_DIR.parent
DOWNLOADS_DIR = Path("/home/mario/Downloads")

NPY_PATH = CHUNKS_DIR / "embeddings.npy"
META_PATH = CHUNKS_DIR / "embeddings_meta.json"
JSONL_PATH = CHUNKS_DIR / "manual_chunks.jsonl"
OUT_HTML_PATH = REPORTS_DIR / "embedding_clusters.html"
ROOT_HTML_PATH = REPO_ROOT / "embedding_clusters.html"
DL_HTML_PATH = DOWNLOADS_DIR / "embedding_clusters.html"

# Mathematically optimal 12-color palette: 150° chromatic stride in HCL space + distinct glyphs
CATEGORY_CONFIG = {
    "Space Link Protocols (SDLS/OTAR)": {
        "color": "#FA4242",  # Vivid Red
        "symbol": "circle",
        "order": 1,
        "is_code": True
    },
    "Modern Protocols (TLS/DH/SCEP)": {
        "color": "#42FA9E",  # Aquamarine / Mint
        "symbol": "diamond",
        "order": 2,
        "is_code": True
    },
    "Classical Protocols (Kerberos/NS/Yahalom)": {
        "color": "#FA42FA",  # Vivid Magenta / Fuchsia
        "symbol": "square",
        "order": 3,
        "is_code": True
    },
    "Theoretical Tests & Edge Cases": {
        "color": "#9EFA42",  # Electric Lime
        "symbol": "triangle-up",
        "order": 4,
        "is_code": True
    },
    "Other Code Examples": {
        "color": "#4242FA",  # Royal Blue
        "symbol": "star",
        "order": 5,
        "is_code": True
    },
    "Official CPSA Manual": {
        "color": "#FA9E42",  # Vivid Coral Orange
        "symbol": "circle",
        "order": 6,
        "is_code": False
    },
    "Syntax Guides & Crib Sheet": {
        "color": "#42FAFA",  # Electric Cyan
        "symbol": "hexagon",
        "order": 7,
        "is_code": False
    },
    "Strand Space Theory & Algorithms": {
        "color": "#FA429E",  # Deep Rose / Ruby
        "symbol": "diamond",
        "order": 8,
        "is_code": False
    },
    "Protocols with State & Channels": {
        "color": "#42FA42",  # Vivid Emerald
        "symbol": "square",
        "order": 9,
        "is_code": False
    },
    "Hardware Attestation & Trust Roots": {
        "color": "#9E42FA",  # Electric Violet / Purple
        "symbol": "triangle-down",
        "order": 10,
        "is_code": False
    },
    "Authentication Tests & Invariants": {
        "color": "#FAFA42",  # Pure Canary Yellow
        "symbol": "cross",
        "order": 11,
        "is_code": False
    },
    "Formal Logic, Goals & Tooling": {
        "color": "#429EFA",  # Vivid Sky Blue
        "symbol": "pentagon",
        "order": 12,
        "is_code": False
    }
}

def assign_functional_category(chunk: dict) -> str:
    """Classify chunk into clean fine-grained domain taxonomy without prefixes."""
    src = chunk.get("source_file", "").lower()
    title = chunk.get("title", "").lower()
    c_type = chunk.get("chunk_type", "documentation")

    if c_type == "code_example" or src.endswith(".scm"):
        if any(k in src or k in title for k in ["sdls", "otar", "350.5"]):
            return "Space Link Protocols (SDLS/OTAR)"
        if any(k in src or k in title for k in ["scep", "tls", "dh", "sts"]):
            return "Modern Protocols (TLS/DH/SCEP)"
        if any(k in src or k in title for k in ["ns", "nsl", "kerberos", "yahalom", "blanchet", "woolam", "denning-sacco", "dass"]):
            return "Classical Protocols (Kerberos/NS/Yahalom)"
        if any(k in src or k in title for k in ["crushing", "weird", "non_transforming", "nonaug", "wonthull", "facts", "rule", "ordered", "deorig"]):
            return "Theoretical Tests & Edge Cases"
        return "Other Code Examples"
    else:
        if "cpsa4manual" in src:
            return "Official CPSA Manual"
        if any(k in src for k in ["cpsa_cribsheet", "cpsa_index", "cpsaprimer", "cpsaspec", "cpsauser"]):
            return "Syntax Guides & Crib Sheet"
        if any(k in src for k in ["doghmi", "cpsadesign", "cpsafoundation"]):
            return "Strand Space Theory & Algorithms"
        if any(k in src for k in ["state", "hybrid_analysis"]):
            return "Protocols with State & Channels"
        if "attestation" in src or "caves" in src:
            return "Hardware Attestation & Trust Roots"
        if any(k in src for k in ["composition", "auth_tests", "deducing_security_goals"]):
            return "Authentication Tests & Invariants"
        return "Formal Logic, Goals & Tooling"

def main():
    if not NPY_PATH.exists() or not JSONL_PATH.exists():
        print(f"Error: Missing embeddings {NPY_PATH} or chunks {JSONL_PATH}", file=sys.stderr)
        sys.exit(1)

    print("Loading embeddings and chunks...")
    embeddings = np.load(NPY_PATH)
    total_vectors = len(embeddings)
    dim = embeddings.shape[1]
    print(f"Loaded matrix: {total_vectors} vectors, {dim} dimensions.")

    chunks = []
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    chunks.append(json.loads(line))
                except Exception:
                    pass

    # 1. Unsupervised K-Means Clustering on High-Dimensional Vectors
    n_clusters = 7
    print(f"Running K-Means (k={n_clusters}) on {dim}-D embeddings...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(embeddings)

    # Extract top keywords per cluster using TF-IDF
    corpus_texts = [c.get("text", "")[:600] for c in chunks]
    tfidf = TfidfVectorizer(max_features=500, stop_words="english", token_pattern=r"[a-zA-Z0-9_\-]+")
    try:
        tfidf_mat = tfidf.fit_transform(corpus_texts)
        feature_names = np.array(tfidf.get_feature_names_out())
        cluster_keywords = {}
        for k in range(n_clusters):
            k_indices = np.where(cluster_labels == k)[0]
            if len(k_indices) > 0:
                k_mean_tfidf = np.asarray(tfidf_mat[k_indices].mean(axis=0)).flatten()
                top_word_indices = k_mean_tfidf.argsort()[-3:][::-1]
                cluster_keywords[k] = ", ".join(feature_names[top_word_indices])
            else:
                cluster_keywords[k] = "general"
    except Exception:
        cluster_keywords = {k: f"Cluster {k}" for k in range(n_clusters)}

    # 2. Compute 7 Multi-Projection Coordinates
    print("Computing 1/7: UMAP Balanced (n_neighbors=25, min_dist=0.3, metric='cosine')...")
    umap_bal = umap.UMAP(n_neighbors=25, min_dist=0.3, metric="cosine", random_state=42).fit_transform(embeddings)

    print("Computing 2/7: UMAP Dense Islands (n_neighbors=15, min_dist=0.05, metric='cosine')...")
    umap_dense = umap.UMAP(n_neighbors=15, min_dist=0.05, metric="cosine", random_state=42).fit_transform(embeddings)

    print("Computing 3/7: UMAP Global Spread (n_neighbors=50, min_dist=0.5, metric='cosine')...")
    umap_macro = umap.UMAP(n_neighbors=50, min_dist=0.5, metric="cosine", random_state=42).fit_transform(embeddings)

    print("Computing 4/7: t-SNE Standard (perplexity=35, metric='cosine')...")
    tsne_std = TSNE(n_components=2, perplexity=35, metric="cosine", random_state=42, init="pca", learning_rate="auto").fit_transform(embeddings)

    print("Computing 5/7: t-SNE Macro (perplexity=65, metric='cosine')...")
    tsne_macro = TSNE(n_components=2, perplexity=65, metric="cosine", random_state=42, init="pca", learning_rate="auto").fit_transform(embeddings)

    print("Computing 6/7: PCA (Linear Variance Decomposition)...")
    pca_coords = PCA(n_components=2, random_state=42).fit_transform(embeddings)

    print("Computing 7/7: Truncated SVD / LSA...")
    svd_coords = TruncatedSVD(n_components=2, random_state=42).fit_transform(embeddings)

    # 3. Assemble Master DataFrame
    rows = []
    for idx, c in enumerate(chunks):
        k_id = cluster_labels[idx]
        category = assign_functional_category(c)
        is_code = CATEGORY_CONFIG.get(category, {}).get("is_code", False) or c.get("source_file", "").endswith(".scm")
        raw_text = c.get("text", "")
        clean_preview = raw_text.replace("\n", " ").replace("\"", "'").replace("<", "[").replace(">", "]")[:160] + "..."
        clean_title = c.get("title", "Untitled").replace("<", "[").replace(">", "]").replace("\"", "'")
        clean_source = c.get("source_file", "").replace("<", "[").replace(">", "]").replace("\"", "'")

        rows.append({
            "u_bal_x": float(umap_bal[idx, 0]),
            "u_bal_y": float(umap_bal[idx, 1]),
            "u_dense_x": float(umap_dense[idx, 0]),
            "u_dense_y": float(umap_dense[idx, 1]),
            "u_macro_x": float(umap_macro[idx, 0]),
            "u_macro_y": float(umap_macro[idx, 1]),
            "tsne_s_x": float(tsne_std[idx, 0]),
            "tsne_s_y": float(tsne_std[idx, 1]),
            "tsne_m_x": float(tsne_macro[idx, 0]),
            "tsne_m_y": float(tsne_macro[idx, 1]),
            "pca_x": float(pca_coords[idx, 0]),
            "pca_y": float(pca_coords[idx, 1]),
            "svd_x": float(svd_coords[idx, 0]),
            "svd_y": float(svd_coords[idx, 1]),
            "chunk_id": c.get("chunk_id", idx + 1),
            "title": clean_title,
            "category": category,
            "is_code": is_code,
            "cluster_id": k_id,
            "cluster_name": f"K{k_id}: {cluster_keywords.get(k_id, '')}".replace("<", "[").replace(">", "]"),
            "source_file": clean_source,
            "word_count": c.get("word_count", len(raw_text.split())),
            "snippet": clean_preview
        })

    df = pd.DataFrame(rows)

    # 4. Construct Plotly Multi-Trace Figure
    print("Constructing multi-projection interactive visualization with optimal palette...")
    fig = go.Figure()

    sorted_categories = sorted(CATEGORY_CONFIG.keys(), key=lambda k: CATEGORY_CONFIG[k]["order"])
    category_counts = df["category"].value_counts().to_dict()
    active_cats = [cat for cat in sorted_categories if not df[df["category"] == cat].empty]

    search_corpus = []

    for trace_idx, cat in enumerate(active_cats):
        cat_df = df[df["category"] == cat]
        cfg = CATEGORY_CONFIG.get(cat, {"color": "#9E9E9E", "symbol": "circle", "is_code": False})
        count = category_counts.get(cat, len(cat_df))
        is_code = cfg.get("is_code", False)
        # Clean display name without [CODE] or [DOCS] prefixes
        display_name = f"{cat} ({count})"

        hovertemplate = (
            "<b style='font-size:13px; color:#FFFFFF;'>%{customdata[0]}</b><br>"
            "<span style='color:#94A3B8;'>Chunk ID:</span> #%{customdata[1]} | "
            "<span style='color:#94A3B8;'>Words:</span> %{customdata[2]}<br>"
            "<span style='color:#94A3B8;'>Category:</span> " + cat + "<br>"
            "<span style='color:#94A3B8;'>K-Means Cluster:</span> %{customdata[3]}<br>"
            "<span style='color:#94A3B8;'>Source:</span> %{customdata[4]}<br>"
            "--------------------------------------------------<br>"
            "<span style='color:#E2E8F0;'>%{customdata[5]}</span>"
            "<extra></extra>"
        )

        customdata = np.stack((
            cat_df["title"].values,
            cat_df["chunk_id"].values,
            cat_df["word_count"].values,
            cat_df["cluster_name"].values,
            cat_df["source_file"].values,
            cat_df["snippet"].values
        ), axis=-1)

        hoverlabel = dict(
            bgcolor="#0B0F19",
            bordercolor=cfg["color"],
            font=dict(
                color="#FFFFFF",
                size=12,
                family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
            )
        )

        fig.add_trace(go.Scatter(
            x=cat_df["u_bal_x"],
            y=cat_df["u_bal_y"],
            mode="markers",
            name=display_name,
            marker=dict(
                size=11.5 if is_code else 8.5,
                color=cfg["color"],
                symbol=cfg["symbol"],
                opacity=0.92 if is_code else 0.86,
                # Crisp white outline around all code files, subtle dark border for documentation
                line=dict(
                    width=2.5 if is_code else 1.0,
                    color="#FFFFFF" if is_code else "#05070D"
                )
            ),
            customdata=customdata,
            hovertemplate=hovertemplate,
            hoverlabel=hoverlabel
        ))

        # Index points for real-time in-browser RAG search engine
        for point_idx, (_, row) in enumerate(cat_df.iterrows()):
            c_id = int(row["chunk_id"])
            chunk_obj = chunks[c_id - 1] if 0 <= c_id - 1 < len(chunks) else {}
            ast_feats = []
            ast_dict = chunk_obj.get("ast_features", {})
            if isinstance(ast_dict, dict):
                for sublist in ast_dict.values():
                    if isinstance(sublist, list):
                        ast_feats.extend(sublist)
            meta_dict = chunk_obj.get("formal_metadata", {})
            if isinstance(meta_dict, dict):
                for sublist in meta_dict.values():
                    if isinstance(sublist, list):
                        for it in sublist:
                            if isinstance(it, str):
                                ast_feats.append(it)
                            elif isinstance(it, dict) and "name" in it:
                                ast_feats.append(it["name"])

            search_corpus.append({
                "id": c_id,
                "t_idx": trace_idx,
                "p_idx": point_idx,
                "title": row["title"],
                "cat": cat,
                "src": row["source_file"],
                "text": row["snippet"],
                "ast": list(set(ast_feats))[:20],
                "is_code": bool(row["is_code"]),
                "symbol": cfg["symbol"],
                "color": cfg["color"],
                "words": int(row["word_count"]),
                "cluster_name": row["cluster_name"]
            })

    # Add Dedicated Spotlight Glow Halo Trace (Trace Index: len(active_cats))
    fig.add_trace(go.Scatter(
        x=[],
        y=[],
        mode="markers",
        name="Search Spotlight Halo",
        showlegend=False,
        marker=dict(
            size=10,
            color="rgba(255, 255, 255, 0.3)",
            symbol="circle",
            opacity=0.35,
            line=dict(width=0)
        ),
        hoverinfo="skip"
    ))

    # Add Dedicated Spotlight Core Markers Trace (Trace Index: len(active_cats) + 1)
    fig.add_trace(go.Scatter(
        x=[],
        y=[],
        mode="markers",
        name="Search Spotlight Core",
        showlegend=False,
        marker=dict(
            size=16,
            color="#FFFFFF",
            symbol="circle",
            opacity=1.0,
            line=dict(
                width=3.0,
                color="#FFFFFF"
            )
        ),
        customdata=[],
        hovertemplate=(
            "<b style='font-size:13px; color:#FFFFFF;'>Rank #%{customdata[6]} Match</b><br>"
            "<b style='font-size:13px; color:#FFFFFF;'>%{customdata[0]}</b><br>"
            "<span style='color:#94A3B8;'>Chunk ID:</span> #%{customdata[1]} | "
            "<span style='color:#94A3B8;'>Words:</span> %{customdata[2]}<br>"
            "<span style='color:#94A3B8;'>Category:</span> %{customdata[7]}<br>"
            "<span style='color:#94A3B8;'>K-Means Cluster:</span> %{customdata[3]}<br>"
            "<span style='color:#94A3B8;'>Source:</span> %{customdata[4]}<br>"
            "--------------------------------------------------<br>"
            "<span style='color:#E2E8F0;'>%{customdata[5]}</span>"
            "<extra></extra>"
        ),
        hoverlabel=dict(
            bgcolor="#0B0F19",
            bordercolor="#FFFFFF",
            font=dict(
                color="#FFFFFF",
                size=12,
                family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
            )
        )
    ))

    # Projections dictionary for real-time coordinate switching (targeting background traces 0..11)
    projections_dict = {
        "0": {
            "name": "UMAP (Balanced Topology)",
            "x": [df[df["category"] == cat]["u_bal_x"].tolist() for cat in active_cats],
            "y": [df[df["category"] == cat]["u_bal_y"].tolist() for cat in active_cats]
        },
        "1": {
            "name": "UMAP (Clustered Islands)",
            "x": [df[df["category"] == cat]["u_dense_x"].tolist() for cat in active_cats],
            "y": [df[df["category"] == cat]["u_dense_y"].tolist() for cat in active_cats]
        },
        "2": {
            "name": "UMAP (Global Spread)",
            "x": [df[df["category"] == cat]["u_macro_x"].tolist() for cat in active_cats],
            "y": [df[df["category"] == cat]["u_macro_y"].tolist() for cat in active_cats]
        },
        "3": {
            "name": "t-SNE (Standard Perplexity=35)",
            "x": [df[df["category"] == cat]["tsne_s_x"].tolist() for cat in active_cats],
            "y": [df[df["category"] == cat]["tsne_s_y"].tolist() for cat in active_cats]
        },
        "4": {
            "name": "t-SNE (Macro Perplexity=65)",
            "x": [df[df["category"] == cat]["tsne_m_x"].tolist() for cat in active_cats],
            "y": [df[df["category"] == cat]["tsne_m_y"].tolist() for cat in active_cats]
        },
        "5": {
            "name": "PCA (Linear Variance / Unwarped)",
            "x": [df[df["category"] == cat]["pca_x"].tolist() for cat in active_cats],
            "y": [df[df["category"] == cat]["pca_y"].tolist() for cat in active_cats]
        },
        "6": {
            "name": "Truncated SVD / LSA (Semantic Axes)",
            "x": [df[df["category"] == cat]["svd_x"].tolist() for cat in active_cats],
            "y": [df[df["category"] == cat]["svd_y"].tolist() for cat in active_cats]
        }
    }

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B0F19",
        plot_bgcolor="#0F172A",
        autosize=True,
        hovermode="closest",
        margin=dict(l=30, r=360, t=30, b=30),
        legend=dict(
            title=dict(
                text="<b>Domain Taxonomy</b><br><span style='font-size:10px; color:#94A3B8;'>Click items to isolate</span>",
                font=dict(size=12, color="#FFFFFF")
            ),
            orientation="v",
            yanchor="top",
            y=0.97,
            xanchor="left",
            x=1.02,
            bgcolor="#111827",
            bordercolor="#334155",
            borderwidth=1,
            font=dict(size=11, color="#E2E8F0"),
            itemsizing="constant"
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            title=""
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            title=""
        ),
        hoverlabel=dict(
            bgcolor="#0B0F19",
            bordercolor="#38BDF8",
            font=dict(size=12, color="#FFFFFF", family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif")
        )
    )

    raw_html = fig.to_html(include_plotlyjs="cdn", full_html=False)
    projections_json = json.dumps(projections_dict)
    search_corpus_json = json.dumps(search_corpus)
    active_cats_count = len(active_cats)

    full_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CPSA Corpus Embedding Topology & Real-Time RAG Search</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        html, body {{
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            background-color: #0B0F19;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        #plotly-container {{
            width: 100vw;
            height: 100vh;
            position: relative;
        }}
        /* Solid Flat Technical Control Header (Zero Glassmorphism) */
        .tech-header {{
            position: absolute;
            top: 16px;
            left: 20px;
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 12px;
            background: #111827;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 7px 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        }}
        .control-group {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .control-label {{
            color: #94A3B8;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .projection-select {{
            background: #0B0F19;
            color: #F8FAFC;
            border: 1px solid #475569;
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            outline: none;
            transition: border-color 0.15s ease;
        }}
        .projection-select:hover, .projection-select:focus {{
            border-color: #38BDF8;
            background: #0B0F19;
        }}
        .projection-select option {{
            background: #0B0F19;
            color: #F8FAFC;
            padding: 8px;
        }}
        /* Search Box Input */
        .search-box-wrapper {{
            position: relative;
            display: flex;
            align-items: center;
            border-left: 1px solid #334155;
            padding-left: 12px;
        }}
        .search-icon {{
            width: 14px;
            height: 14px;
            color: #38BDF8;
            position: absolute;
            left: 20px;
            pointer-events: none;
        }}
        .search-input {{
            width: 330px;
            background: #0B0F19;
            color: #F8FAFC;
            border: 1px solid #475569;
            border-radius: 4px;
            padding: 6px 28px 6px 28px;
            font-size: 12px;
            outline: none;
            transition: border-color 0.15s ease;
        }}
        .search-input:focus {{
            width: 420px;
            border-color: #38BDF8;
            background: #0B0F19;
        }}
        .search-clear-btn {{
            position: absolute;
            right: 8px;
            background: transparent;
            border: none;
            color: #94A3B8;
            font-size: 13px;
            cursor: pointer;
            display: none;
            padding: 2px 6px;
        }}
        .search-clear-btn:hover {{
            color: #FFFFFF;
        }}
        /* Reset View Button */
        .reset-view-btn {{
            display: flex;
            align-items: center;
            gap: 5px;
            background: #0B0F19;
            border: 1px solid #475569;
            color: #E2E8F0;
            padding: 5px 9px;
            border-radius: 4px;
            font-size: 11.5px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .reset-view-btn:hover {{
            background: #1F2937;
            border-color: #38BDF8;
            color: #38BDF8;
        }}
        /* Legend Indicator */
        .legend-indicator {{
            display: flex;
            align-items: center;
            gap: 8px;
            border-left: 1px solid #334155;
            padding-left: 12px;
            font-size: 11px;
            color: #94A3B8;
        }}
        .legend-badge-code {{
            display: inline-block;
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: #FA42FA;
            border: 2px solid #FFFFFF;
        }}
        .legend-badge-doc {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #42FAFA;
            border: 1.2px solid #05070D;
        }}
        /* Minimized Drawer Floating Pill */
        .drawer-pill {{
            position: absolute;
            top: 68px;
            left: 20px;
            z-index: 999;
            display: none;
            align-items: center;
            gap: 8px;
            background: #111827;
            border: 1px solid #38BDF8;
            border-radius: 4px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 600;
            color: #38BDF8;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            transition: background 0.15s ease;
        }}
        .drawer-pill:hover {{
            background: #1F2937;
        }}
        /* Solid Flat Ranked Results Drawer */
        .results-drawer {{
            position: absolute;
            top: 68px;
            left: 20px;
            width: 480px;
            max-height: calc(100vh - 90px);
            background: #111827;
            border: 1px solid #334155;
            border-radius: 6px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
            z-index: 1000;
            display: none;
            flex-direction: column;
            overflow: hidden;
        }}
        .results-drawer-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 9px 13px;
            background: #1E293B;
            border-bottom: 1px solid #334155;
        }}
        .results-count {{
            font-size: 12px;
            font-weight: 700;
            color: #38BDF8;
        }}
        .drawer-toggle-btn {{
            background: #0B0F19;
            border: 1px solid #475569;
            color: #94A3B8;
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .drawer-toggle-btn:hover {{
            color: #FFFFFF;
            border-color: #38BDF8;
            background: #1F2937;
        }}
        .results-list {{
            overflow-y: auto;
            padding: 8px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .result-card {{
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 4px;
            padding: 8px 10px;
            cursor: pointer;
            transition: border-color 0.15s ease, background 0.15s ease;
        }}
        .result-card:hover, .result-card.active-card {{
            background: #273549;
            border-color: #38BDF8;
        }}
        .result-card-header {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 4px;
        }}
        .rank-badge {{
            font-size: 10px;
            font-weight: 700;
            padding: 1px 6px;
            border-radius: 3px;
            background: #334155;
            color: #F8FAFC;
            border: 1px solid #475569;
        }}
        .result-title {{
            font-size: 12px;
            font-weight: 600;
            color: #FFFFFF;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            flex: 1;
        }}
        .score-pill {{
            font-size: 9.5px;
            color: #94A3B8;
            background: #0F172A;
            border: 1px solid #334155;
            padding: 1px 5px;
            border-radius: 3px;
        }}
        .result-meta {{
            display: flex;
            gap: 8px;
            font-size: 10px;
            color: #94A3B8;
            margin-bottom: 4px;
        }}
        .meta-chunk {{
            color: #38BDF8;
            font-weight: 600;
        }}
        .meta-cat {{
            color: #CBD5E1;
        }}
        .result-snippet {{
            font-size: 11px;
            color: #94A3B8;
            line-height: 1.35;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .js-plotly-plot .plotly .modebar {{
            top: 15px !important;
            right: 370px !important;
        }}
        /* Strict hoverlayer overrides (Solid Dark) */
        .hoverlayer .hovertext rect {{
            fill: #0B0F19 !important;
            fill-opacity: 1.0 !important;
            rx: 4px !important;
            ry: 4px !important;
            stroke: #38BDF8 !important;
            stroke-width: 1.5px !important;
        }}
        .hoverlayer .hovertext text, .hoverlayer .hovertext tspan {{
            fill: #FFFFFF !important;
        }}
    </style>
</head>
<body>
    <div id="plotly-container">
        <div class="tech-header">
            <div class="control-group">
                <label for="proj-select" class="control-label">Projection:</label>
                <select id="proj-select" class="projection-select" onchange="switchProjection(this.value)">
                    <option value="0">1. UMAP (Balanced Topology - Default)</option>
                    <option value="1">2. UMAP (Clustered Islands - High Density)</option>
                    <option value="2">3. UMAP (Global Spread - Macro Distances)</option>
                    <option value="3">4. t-SNE (Standard Perplexity=35)</option>
                    <option value="4">5. t-SNE (Macro Perplexity=65)</option>
                    <option value="5">6. PCA (Linear Variance / Unwarped)</option>
                    <option value="6">7. Truncated SVD / LSA (Semantic Axes)</option>
                </select>
            </div>

            <div class="search-box-wrapper">
                <svg class="search-icon" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                </svg>
                <input type="text" id="rag-query-input" class="search-input" placeholder="Query CPSA RAG (e.g. pen-non-orig, defrole trace, auth-test, envelope)..." oninput="onSearchInput(this.value)" autocomplete="off">
                <button id="clear-search-btn" class="search-clear-btn" onclick="clearSearch()">✕</button>
            </div>

            <button class="reset-view-btn" onclick="resetPlotView()" title="Reset Zoom & Pan">
                <svg viewBox="0 0 20 20" fill="currentColor" width="13" height="13">
                    <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
                </svg>
                Reset View
            </button>

            <div class="legend-indicator">
                <span class="legend-badge-code"></span>
                <span style="color:#FFFFFF;">White Ring: Code (.scm)</span>
                <span class="legend-badge-doc" style="margin-left:6px;"></span>
                <span>Dark Border: Docs</span>
            </div>
        </div>

        <!-- Minimized Floating Pill -->
        <button id="drawer-pill" class="drawer-pill" onclick="toggleDrawer()">
            <span id="pill-count">0</span> Matches (Expand)
        </button>

        <!-- Solid Ranked Results Drawer -->
        <div id="search-results-drawer" class="results-drawer">
            <div class="results-drawer-header">
                <span id="results-count" class="results-count">Top 10 Matches</span>
                <button class="drawer-toggle-btn" onclick="toggleDrawer()" title="Minimize Drawer">◀ Minimize</button>
            </div>
            <div id="results-list" class="results-list"></div>
        </div>

        {raw_html}
    </div>

    <script>
        const PROJECTIONS = {projections_json};
        const SEARCH_CORPUS = {search_corpus_json};
        const ACTIVE_CATS_COUNT = {active_cats_count};
        const BG_TRACE_INDICES = Array.from({{length: ACTIVE_CATS_COUNT}}, (_, i) => i);
        const HALO_TRACE_INDEX = ACTIVE_CATS_COUNT;
        const CORE_TRACE_INDEX = ACTIVE_CATS_COUNT + 1;

        let currentProjKey = "0";
        let debounceTimer = null;
        let activeQuery = "";
        let currentTopMatches = [];

        // Comprehensive Stopwords (Filter Query Framing Noise)
        const STOP_WORDS = new Set([
            "what", "is", "a", "an", "the", "and", "or", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "up", "about", "into", "through", "after", "before",
            "does", "do", "did", "how", "why", "where", "which", "who", "when", "can", "could",
            "would", "should", "will", "shall", "are", "were", "be", "been", "being", "have",
            "has", "had", "it", "its", "they", "their", "this", "that", "these", "those",
            "used", "use", "using", "uses", "work", "works", "mean", "means", "make", "makes",
            "show", "shows", "tell", "give", "find", "chunk", "protocol", "example"
        ]);

        // Precompute Corpus Document Frequency (DF) for BM25/IDF
        const DF = {{}};
        const CORPUS_SIZE = SEARCH_CORPUS.length;
        SEARCH_CORPUS.forEach(doc => {{
            const seen = new Set();
            const addTokens = (str) => {{
                if (!str) return;
                const tokens = str.toLowerCase().replace(/[^a-z0-9_\\-]/g, ' ').split(/\\s+/);
                tokens.forEach(t => {{
                    if (t.length > 1 && !STOP_WORDS.has(t) && !seen.has(t)) {{
                        seen.add(t);
                        DF[t] = (DF[t] || 0) + 1;
                    }}
                }});
            }};
            addTokens(doc.title);
            addTokens(doc.text);
            addTokens(doc.src);
            if (doc.ast) doc.ast.forEach(a => addTokens(a));
        }});

        function escapeHtml(str) {{
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
        }}

        function extractTokens(qStr) {{
            const rawTokens = qStr.toLowerCase().replace(/[^a-z0-9_\\-]/g, ' ').split(/\\s+/).filter(Boolean);
            const substantive = rawTokens.filter(t => !STOP_WORDS.has(t));
            return {{
                raw: rawTokens,
                substantive: substantive.length > 0 ? substantive : rawTokens
            }};
        }}

        function onSearchInput(val) {{
            const clearBtn = document.getElementById('clear-search-btn');
            clearBtn.style.display = val.trim() ? 'block' : 'none';

            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {{
                executeSearch(val);
            }}, 110);
        }}

        function clearSearch() {{
            clearTimeout(debounceTimer);
            const input = document.getElementById('rag-query-input');
            input.value = '';
            executeSearch('');
            input.focus();
        }}

        function resetPlotView() {{
            const plotDiv = document.querySelector('.js-plotly-plot');
            if (!plotDiv) return;
            Plotly.relayout(plotDiv, {{
                'xaxis.autorange': true,
                'yaxis.autorange': true
            }});
        }}

        function toggleDrawer() {{
            const drawer = document.getElementById('search-results-drawer');
            const pill = document.getElementById('drawer-pill');
            if (drawer.style.display === 'none') {{
                drawer.style.display = 'flex';
                pill.style.display = 'none';
            }} else {{
                drawer.style.display = 'none';
                if (activeQuery) pill.style.display = 'flex';
            }}
        }}

        function switchProjection(key) {{
            currentProjKey = key;
            const proj = PROJECTIONS[key];
            if (!proj) return;
            const plotDiv = document.querySelector('.js-plotly-plot');
            if (!plotDiv) return;

            // Restyle background traces 0..11 with new projection coordinates
            Plotly.restyle(plotDiv, {{
                x: proj.x,
                y: proj.y
            }}, BG_TRACE_INDICES);

            // Re-sync spotlight points if query is active
            if (activeQuery) {{
                executeSearch(activeQuery);
            }}
        }}

        function executeSearch(query) {{
            activeQuery = (query || '').trim();
            const drawer = document.getElementById('search-results-drawer');
            const pill = document.getElementById('drawer-pill');
            const clearBtn = document.getElementById('clear-search-btn');
            const countEl = document.getElementById('results-count');
            const pillCountEl = document.getElementById('pill-count');
            const listEl = document.getElementById('results-list');
            const plotDiv = document.querySelector('.js-plotly-plot');
            if (!plotDiv || !plotDiv.data) return;

            if (!activeQuery) {{
                clearBtn.style.display = 'none';
                drawer.style.display = 'none';
                pill.style.display = 'none';
                currentTopMatches = [];

                // 1. Clear spotlight halo and core traces
                Plotly.restyle(plotDiv, {{
                    x: [[]],
                    y: [[]]
                }}, [HALO_TRACE_INDEX, CORE_TRACE_INDEX]);

                // 2. Restore background traces to full opacity (0.92)
                Plotly.restyle(plotDiv, {{
                    opacity: 0.92
                }}, BG_TRACE_INDICES);
                return;
            }}

            clearBtn.style.display = 'block';
            drawer.style.display = 'flex';
            pill.style.display = 'none';

            const {{ raw, substantive }} = extractTokens(activeQuery);
            const qLower = activeQuery.toLowerCase();

            // BM25-Weighted Lexical & AST Feature Scoring
            const scored = [];
            for (let i = 0; i < SEARCH_CORPUS.length; i++) {{
                const doc = SEARCH_CORPUS[i];
                let score = 0;
                const titleL = doc.title.toLowerCase();
                const textL = doc.text.toLowerCase();
                const srcL = doc.src.toLowerCase();
                const catL = doc.cat.toLowerCase();

                // Exact phrase bonus
                if (titleL.includes(qLower)) score += 80;
                if (textL.includes(qLower)) score += 40;
                if (srcL.includes(qLower)) score += 35;

                // Substantive keyword scoring with IDF weighting
                for (let j = 0; j < substantive.length; j++) {{
                    const t = substantive[j];
                    const idf = DF[t] ? Math.log(1 + (CORPUS_SIZE - DF[t] + 0.5) / (DF[t] + 0.5)) : 3.0;

                    if (doc.ast && doc.ast.some(a => a.toLowerCase().includes(t))) score += idf * 25.0;
                    if (titleL.includes(t)) score += idf * 18.0;
                    if (srcL.includes(t)) score += idf * 14.0;
                    if (textL.includes(t)) score += idf * 6.0;
                    if (catL.includes(t)) score += idf * 3.0;
                }}

                if (score > 0) {{
                    scored.push({{ doc, score }});
                }}
            }}

            scored.sort((a, b) => b.score - a.score);
            
            // STRICTLY HIGHLIGHT ONLY THE TOP 10 MATCHES
            currentTopMatches = scored.slice(0, 10);

            const matchCount = scored.length;
            countEl.innerText = matchCount > 10 ? `Top 10 of ${{matchCount}} matches` : `${{matchCount}} matching chunk${{matchCount === 1 ? '' : 's'}}`;
            pillCountEl.innerText = currentTopMatches.length;

            // 1. Dim background traces to 15% in a single instantaneous call
            Plotly.restyle(plotDiv, {{ opacity: 0.15 }}, BG_TRACE_INDICES);

            // 2. Populate Spotlight Overlay Traces with accurate PROJECTIONS coordinates
            const currentCoords = PROJECTIONS[currentProjKey];
            const haloX = [], haloY = [], haloSizes = [], haloColors = [];
            const coreX = [], coreY = [], coreSizes = [], coreColors = [], coreSymbols = [], coreLineWidths = [], coreCustomData = [];

            for (let r = 0; r < currentTopMatches.length; r++) {{
                const item = currentTopMatches[r];
                const d = item.doc;
                const px = currentCoords.x[d.t_idx][d.p_idx];
                const py = currentCoords.y[d.t_idx][d.p_idx];
                if (px === undefined || py === undefined) continue;

                haloX.push(px);
                haloY.push(py);
                coreX.push(px);
                coreY.push(py);

                const rank = r + 1;
                // Highlight: Keep EXACT category shape and EXACT category color
                haloSizes.push(30);
                haloColors.push(d.color); // Exact category color for subtle halo

                coreSizes.push(16); // Prominent highlighted marker size
                coreColors.push(d.color); // EXACT category color preserved
                coreSymbols.push(d.symbol); // EXACT category symbol preserved
                coreLineWidths.push(3.0); // Thick crisp white outline

                coreCustomData.push([
                    d.title,
                    d.id,
                    d.words,
                    d.cluster_name,
                    d.src,
                    d.text,
                    rank,
                    d.cat
                ]);
            }}

            // Update Halo overlay trace
            Plotly.restyle(plotDiv, {{
                x: [haloX],
                y: [haloY],
                'marker.size': [haloSizes],
                'marker.color': [haloColors]
            }}, [HALO_TRACE_INDEX]);

            // Update Core overlay trace
            Plotly.restyle(plotDiv, {{
                x: [coreX],
                y: [coreY],
                'marker.size': [coreSizes],
                'marker.color': [coreColors],
                'marker.symbol': [coreSymbols],
                'marker.line.width': [coreLineWidths],
                customdata: [coreCustomData]
            }}, [CORE_TRACE_INDEX]);

            // Populate Results List (strictly top 10)
            let listHtml = '';
            currentTopMatches.forEach((item, rIdx) => {{
                const d = item.doc;
                const rank = rIdx + 1;
                listHtml += `
                    <div id="card-${{d.id}}" class="result-card" onclick="focusCard(${{rIdx}}, ${{d.id}})" onmouseenter="previewCard(${{rIdx}})" onmouseleave="unpreviewCard()">
                        <div class="result-card-header">
                            <span class="rank-badge">#${{rank}}</span>
                            <span class="result-title">${{escapeHtml(d.title)}}</span>
                            <span class="score-pill">${{Math.round(item.score)}} pts</span>
                        </div>
                        <div class="result-meta">
                            <span class="meta-chunk">#${{d.id}}</span>
                            <span class="meta-cat" style="color:${{d.color}}; font-weight:600;">${{escapeHtml(d.cat)}}</span>
                            <span class="meta-src">${{escapeHtml(d.src)}}</span>
                        </div>
                        <div class="result-snippet">${{escapeHtml(d.text)}}</div>
                    </div>
                `;
            }});
            listEl.innerHTML = listHtml || '<div style="color:#94A3B8; font-size:12px; padding:12px;">No matching chunks found.</div>';
        }}

        function focusCard(rankIndex, chunkId) {{
            const plotDiv = document.querySelector('.js-plotly-plot');
            if (!plotDiv || !currentTopMatches[rankIndex]) return;
            const item = currentTopMatches[rankIndex];
            const d = item.doc;
            const currentCoords = PROJECTIONS[currentProjKey];
            const px = currentCoords.x[d.t_idx][d.p_idx];
            const py = currentCoords.y[d.t_idx][d.p_idx];

            if (px !== undefined && py !== undefined) {{
                Plotly.relayout(plotDiv, {{
                    'xaxis.range': [px - 2.5, px + 2.5],
                    'yaxis.range': [py - 2.5, py + 2.5]
                }});
                // Hover directly on the glowing spotlight point
                Plotly.Fx.hover(plotDiv, [{{ curveNumber: CORE_TRACE_INDEX, pointNumber: rankIndex }}]);
            }}

            // Highlight card
            document.querySelectorAll('.result-card').forEach(c => c.classList.remove('active-card'));
            const activeCard = document.getElementById('card-' + chunkId);
            if (activeCard) activeCard.classList.add('active-card');
        }}

        function previewCard(rankIndex) {{
            const plotDiv = document.querySelector('.js-plotly-plot');
            if (!plotDiv || rankIndex >= currentTopMatches.length) return;
            // Highlight the glowing spotlight point directly
            Plotly.Fx.hover(plotDiv, [{{ curveNumber: CORE_TRACE_INDEX, pointNumber: rankIndex }}]);
        }}

        function unpreviewCard() {{
            const plotDiv = document.querySelector('.js-plotly-plot');
            if (!plotDiv) return;
            Plotly.Fx.unhover(plotDiv);
        }}

        window.addEventListener('DOMContentLoaded', () => {{
            const plotDiv = document.querySelector('.js-plotly-plot');
            if (!plotDiv) return;

            // Bind Enter key on search input
            const input = document.getElementById('rag-query-input');
            input.addEventListener('keydown', (e) => {{
                if (e.key === 'Enter') {{
                    clearTimeout(debounceTimer);
                    executeSearch(e.target.value);
                }}
            }});

            // Bidirectional: Click canvas point -> scroll to and highlight drawer card
            plotDiv.on('plotly_click', function(data) {{
                if (!data.points || !data.points.length) return;
                const pt = data.points[0];
                const custom = pt.customdata;
                if (custom && custom[1]) {{
                    const chunkId = custom[1];
                    const card = document.getElementById('card-' + chunkId);
                    if (card) {{
                        card.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
                        document.querySelectorAll('.result-card').forEach(c => c.classList.remove('active-card'));
                        card.classList.add('active-card');
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>
"""

    # Write to canonical reports location
    with open(OUT_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(full_html_content)

    # Copy to repo root and downloads folder
    try:
        with open(ROOT_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(full_html_content)
    except Exception as e:
        print(f"Warning: Could not copy to root: {e}", file=sys.stderr)

    try:
        with open(DL_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(full_html_content)
    except Exception as e:
        print(f"Warning: Could not copy to downloads: {e}", file=sys.stderr)

    print(f"\n========================================================")
    print(f"Strict Top-10 Highlight Visualizer Generated Successfully!")
    print(f"Primary File: {OUT_HTML_PATH}")
    print(f"Root Workspace File: {ROOT_HTML_PATH}")
    print(f"User Downloads: {DL_HTML_PATH}")
    print(f"Total Points Indexed: {len(search_corpus)}")
    print(f"========================================================\n")

if __name__ == "__main__":
    main()
```

---

### `refrences/reports/rag_evaluation_report.tex`

*sha256:`8a0c8f6ee076` · 103 lines · 6.4 KB (~1,627 tokens) · lang:`latex`*

```latex
\documentclass[10pt,twocolumn]{article}

\usepackage[margin=0.48in,top=0.50in,bottom=0.50in]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{microtype}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage{caption}

\captionsetup{font=small,labelfont=bf,skip=3pt}

\definecolor{navyblue}{RGB}{15, 44, 89}
\definecolor{darkslate}{RGB}{30, 41, 59}

\hypersetup{colorlinks=true, linkcolor=navyblue, citecolor=navyblue, urlcolor=navyblue}

\title{
    \vspace{-0.9cm}
    \fontsize{13pt}{15pt}\selectfont \textbf{CPSA Protocol RAG: Architecture Evaluation \& Figure Dashboard} \\[0.2em]
    \normalsize \textit{Visualizing 300 Non-SDLS Golden Queries Across BM25, Dense Vectors, Hybrid Fusion, and Reranking}
}
\author{\small \textbf{RFC-LLM Systems Research} \quad | \quad Empirical Technical Dashboard \quad | \quad September 18, 2026}
\date{\vspace{-0.65cm}}

\begin{document}

\maketitle

\begin{table}[htbp]
\centering
\fontsize{7.0pt}{8.8pt}\selectfont
\begin{tabular*}{\columnwidth}{@{\extracolsep{\fill}} l cccc r}
\toprule
\textbf{Retriever Architecture} & \textbf{Hit@1} & \textbf{Hit@3} & \textbf{Hit@10} & \textbf{MRR} & \textbf{NDCG@5} \\
\midrule
Sparse BM25 (DSL Tokenized)          & 68.3\% & 83.3\% & 94.7\% & 0.771 & 0.462 \\
Dense Vectors (Nomic 768-D)          & 75.0\% & 89.0\% & 96.7\% & 0.829 & 0.508 \\
Hybrid RRF-20 (Steep Decay)          & 73.7\% & 92.3\% & 97.3\% & 0.830 & 0.523 \\
Hybrid Convex-AST (Score Fusion)     & 76.0\% & 93.0\% & 97.7\% & 0.845 & 0.539 \\
\textbf{Two-Stage Cross-Encoder}     & \textbf{80.7\%} & \textbf{92.3\%} & \textbf{97.7\%} & \textbf{0.871} & \textbf{0.533} \\
\bottomrule
\end{tabular*}
\vspace{-0.15cm}
\caption{\textbf{Global Empirical Performance Across 300 Golden Benchmark Queries (Non-SDLS).} Evaluated against 1,426 corpus chunks (1,278 contextualized documentation sections + 148 formal Scheme protocol models) across all 5 MITRE manual sources.}
\label{tab:global_summary}
\vspace{-0.25cm}
\end{table}

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{figures/fig1_recall_progression.png}
\caption{\textbf{Cumulative Recall Progression Across Cutoffs ($K=1 \dots 10$).} Comparison of Hit@K across retrieval architectures. While single-stage methods (BM25, Dense, RRF-20, Convex-AST) eventually converge to $\sim$95--97\% recall at $K=10$, Two-Stage Cross-Encoder Reranking creates an immediate step-function increase at $K=1$ (\textbf{80.7\%} vs. 73.7\% for RRF-20 and 68.3\% for BM25). This steep initial trajectory is critical for agentic LLM synthesis: an agent prompting an LLM with only the top-1 or top-2 chunks avoids context window bloat and eliminates distractor hallucinations.}
\label{fig:recall_progression}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{figures/fig2_category_mrr.png}
\caption{\textbf{Domain Performance Breakdown (MRR Across 4 Core Categories).} Mean Reciprocal Rank decomposed by query domain. Two-Stage Reranking achieves its most dramatic performance leaps on symbolic, syntax-sensitive categories: \textbf{Advanced State \& Channels} (+10.1 MRR points over RRF-20) and \textbf{Grammar \& Syntax} (+5.6 MRR points over RRF-20). Full cross-attention pairs exact CPSA keywords (\texttt{pen-non-orig}, \texttt{defgenrule}, memory envelopes) with formal BNF grammar, where bi-encoder vector embeddings collapse fine-grained algebraic distinctions.}
\label{fig:category_mrr}
\end{figure}

\newpage

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{figures/fig3_latency_pareto.png}
\caption{\textbf{Latency vs. Retrieval Quality (MRR) Pareto Frontier.} Trade-off between mean query latency (ms) and Mean Reciprocal Rank (MRR). The dashed line marks the Pareto efficiency boundary. Sparse BM25 offers ultra-low latency (1.4\,ms) but insufficient accuracy (0.771 MRR). Two-Stage Reranking (74.2\,ms, \textbf{0.871 MRR}) dominates the high-accuracy frontier. Heavy multi-vector architectures (e.g. ColBERT at $\sim$120\,ms, 180\,MB index) and full-corpus cross-encoders ($>$1,800\,ms) fall far outside the acceptable envelope for real-time 10-turn DSPy agent loops.}
\label{fig:latency_pareto}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{figures/fig4_rank_distribution.png}
\caption{\textbf{Target Chunk Rank Position Distribution.} Stacked breakdown showing where target chunks surface across the top-10 result positions. Two-Stage Cross-Encoder concentrates \textbf{80.7\%} of all target chunks directly at Rank 1 (green bar), with only 11.6\% at Ranks 2--3 and a mere 2.3\% miss rate ($>10$). In contrast, BM25 leaves 31.7\% of queries dispersed across Ranks 2--10 or missed entirely. Rank-1 concentration allows downstream DSPy generators to operate with compact prompt budgets ($<$1,500 tokens).}
\label{fig:rank_distribution}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=\columnwidth]{figures/fig5_complementarity.png}
\caption{\textbf{Lexical vs. Semantic Complementarity \& Cross-Encoder Query Recovery.} Analysis of top-3 query resolution overlap across modalities. While 79.0\% of queries are resolved jointly by Dense and BM25, 10.0\% are captured \textit{exclusively} by Dense vectors (semantic generalizations) and 4.3\% \textit{exclusively} by BM25 (exact OOV tokens). Crucially, the Cross-Encoder rescues an additional 2.7\% of queries where neither Dense nor BM25 placed the target in the top-3, validating the necessity of a unified hybrid-rerank stack.}
\label{fig:complementarity}
\end{figure}

\vspace{-0.25cm}
\noindent\fbox{%
\parbox{0.96\columnwidth}{%
\fontsize{7.2pt}{8.8pt}\selectfont
\textbf{Operational Recommendations for Autonomous DSPy Agent Loops:}
\begin{itemize}[leftmargin=*,itemsep=1pt,topsep=1pt]
    \item \textbf{Stage 1 Candidate Sizing:} Set candidate pool size to $K=25$. This captures 97.7\% of all ground truth targets while keeping cross-encoder scoring under 52\,ms.
    \item \textbf{Convex-AST Prefilter:} MinMax score normalization with $1.4\times$ exact AST terminal boosting bridges the gap between natural language RFC descriptions and Scheme syntax.
    \item \textbf{Rank-1 Prompt Budget:} Because Top-1 precision is 80.7\%, pass only the single highest-scoring chunk directly into the initial generator prompt; fall back to Chunks 2--3 only if the CPSA binary compiler flags a verification error.
\end{itemize}
}%
}

\end{document}
```

---

### `refrences/run_rag_pipeline.sh`

*sha256:`1c48f0d10d91` · 74 lines · 2.3 KB (~584 tokens) · lang:`bash`*

```bash
#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$DIR/../.venv/bin/python"

if [ ! -f "$PYTHON" ]; then
    echo "Error: Python environment not found at $DIR/../.venv"
    exit 1
fi

# Load environment variables if .env exists
if [ -f "$DIR/.env" ]; then
    set -a
    source "$DIR/.env"
    set +a
elif [ -f "$DIR/../.env" ]; then
    set -a
    source "$DIR/../.env"
    set +a
fi

# Model and Target Directory selection
if [[ "$1" == --* ]]; then
    MODEL="${MODEL_NAME:-gemini/gemini-3.5-flash-lite}"
    TARGET_DIR=""
else
    MODEL="${1:-${MODEL_NAME:-gemini/gemini-3.5-flash-lite}}"
    TARGET_DIR="${2:-}"
fi

echo "============================================================"
echo "    CPSA Atomic Semantic Decomposition & RAG Pipeline       "
echo "============================================================"
echo "Target Model: $MODEL"

if [[ "$MODEL" == gemini* ]]; then
    if [ -z "$GEMINI_API_KEY" ]; then
        echo "Error: GEMINI_API_KEY is not set. Add it to .env or export it."
        exit 1
    fi
    echo "[1/2] Cloud Provider: Google Gemini ($MODEL)"
else
    echo "[1/2] Local Provider: Ollama"
fi

# Check for reprocess-all flag
EXTRA_ARGS=()
for arg in "$@"; do
    if [ "$arg" == "--reprocess-all" ]; then
        EXTRA_ARGS+=("--reprocess-all")
    fi
done

# Step 1: Documentation Semantic Component Chunking
echo "[1/2] Processing technical documentation into atomic semantic chunks..."
if [ -n "$TARGET_DIR" ] && [ "$TARGET_DIR" != "--reprocess-all" ]; then
    "$PYTHON" -u "$DIR/scripts/01_extract_chunks.py" --dir "$TARGET_DIR" -m "$MODEL" "${EXTRA_ARGS[@]}"
else
    "$PYTHON" -u "$DIR/scripts/01_extract_chunks.py" -m "$MODEL" "${EXTRA_ARGS[@]}"
fi

# Step 2: SCM Code Examples Extraction
echo ""
echo "[2/2] Extracting SCM code examples with formal AST features and scenario summaries..."
"$PYTHON" -u "$DIR/scripts/02_extract_code_examples.py" -m "$MODEL" "${EXTRA_ARGS[@]}"

echo ""
echo "============================================================"
echo "CPSA Full RAG Corpus Pipeline Complete!"
echo "Documentation Chunks: $DIR/chunks/manual_chunks.jsonl"
echo "Code Examples:        $DIR/chunks/code_examples.jsonl"
echo "To query: $PYTHON $DIR/scripts/03_query_rag.py '<query>'"
echo "============================================================"
```

---

### `refrences/scripts/01_extract_chunks.py`

*sha256:`8f2e9bcd7fa7` · 624 lines · 26.0 KB (~6,655 tokens) · lang:`python`*

```python
#!/usr/bin/env python3
"""
01_extract_chunks.py
Uniform 1000-Word Block Semantic Decomposer for the CPSA Corpus.

Architecture:
- Ingests all scannable files (.pdf, .md, .txt, .scm) across refrences/ (manual & internet).
- Slices documents into cohesive ~1,000-word blocks at natural paragraph boundaries.
- Blocks <= 150 words (e.g. small .scm protocols) are preserved as atomic units.
- Blocks > 150 words are passed to Gemini 3.1 Flash Lite, which identifies natural
  thematic inflection points and returns exact verbatim first-sentence anchors.
- Python slices the text at exact line numbers matching those verbatim anchors,
  preserving 100% source text integrity without dropping or hallucinating words.
- Enriches every chunk with hierarchical context breadcrumbs.
- Real-time streaming persistence: writes immediately to manual_chunks.jsonl.
- Append-only history logging: updates processing_history.log on file completion.
- Re-run verification: checks processing_history.log and checkpoint.json to skip finished files.
"""

import os
import sys
import time
import json
import re
import argparse
import logging
import warnings
from pathlib import Path
from pydantic import BaseModel, Field
import pymupdf
import dspy
import backoff
from dotenv import load_dotenv, find_dotenv
import litellm

# Silence LiteLLM log spam and deprecation warnings
litellm.suppress_debug_info = True
litellm.set_verbose = False
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning)

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(usecwd=True))
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

DEFAULT_SEARCH_DIRS = [BASE_DIR / "manual", BASE_DIR / "internet"]
CHUNKS_DIR = BASE_DIR / "chunks"
CHUNKS_JSONL_PATH = CHUNKS_DIR / "manual_chunks.jsonl"
CHUNKS_JSON_PATH = CHUNKS_DIR / "manual_chunks.json"
CHECKPOINT_PATH = CHUNKS_DIR / "checkpoint.json"
HISTORY_LOG_PATH = CHUNKS_DIR / "processing_history.log"
CLEAN_MD_PATH = CHUNKS_DIR / "all_references_clean.md"

TARGET_BLOCK_WORDS = 1000
MIN_SPLIT_WORDS = 150
DEFAULT_MODEL = os.environ.get("MODEL_NAME", "gemini/gemini-3.1-flash-lite")
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt"}
EXCLUDE_FILENAMES = {
    "cpsa4manual.txt",       # Duplicate text of cpsa4manual.pdf
    "cpsa4manual_clean.md",  # Duplicate markdown
    "cpsa.cabal.txt",        # Packaging metadata
    "readme.md",             # Empty placeholder
    "manifest.json",         # Download manifest
}

class SemanticBoundary(BaseModel):
    concept_title: str = Field(
        description="Concise, descriptive title defining the specific formal concept, grammar rule, or protocol mechanism."
    )
    first_sentence_verbatim: str = Field(
        description="The exact character-for-character opening sentence where this concept begins in the source text."
    )

class SemanticBlockSplitter(dspy.Signature):
    """You are a formal methods expert and cryptographic protocol analyst specializing in CPSA.
Deconstruct the provided text block into atomic, self-contained semantic units.

Requirements:
1. Sequential Ordering: Identify inflection points strictly in the chronological order they appear in the text from top to bottom.
2. Conceptual Independence: Each boundary must isolate a single distinct topic—such as a specific syntactic rule, algebraic property, protocol role, security goal, operational algorithm, or analysis technique.
3. Verbatim Fidelity: The first_sentence_verbatim MUST match the exact opening characters of the sentence as printed in the text, including punctuation and capitalization. Do not paraphrase or alter tokens.
4. Grounding: Base boundaries strictly on the provided text. Do not hallucinate external concepts or create redundant sub-divisions for brief continuous explanations.
5. Determinism: Maintain strict low-variance deterministic extraction. Adhere purely to factual syntactic boundaries without creative interpolation."""
    source_context: str = dspy.InputField(desc="File and block breadcrumb hierarchy")
    block_text: str = dspy.InputField(desc="Verbatim source text to partition")
    boundaries: list[SemanticBoundary] = dspy.OutputField(desc="Chronologically ordered semantic boundaries with exact verbatim text anchors")

def clean_page_text(text: str) -> str:
    """Clean recurring PDF headers/footers."""
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if "MITRE Corporation" in stripped or stripped.isdigit():
            continue
        if stripped.startswith("The Cryptographic Protocol Shapes Analyzer:"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()

def partition_into_paragraph_blocks(text: str, target_words: int = TARGET_BLOCK_WORDS, max_single_words: int = 1400) -> list[str]:
    """
    Split text into balanced ~1000-word blocks respecting clean paragraph boundaries.
    - If text <= max_single_words (e.g. 1200-1400 words), preserves as 1 unified block
      to give the LLM full document context and avoid awkward runt tails.
    - For larger texts, divides dynamically into k balanced blocks (e.g. 2300w -> 2 x 1150w).
    """
    raw_paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not raw_paras:
        return []

    words = text.split()
    total_words = len(words)
    if total_words <= max_single_words:
        return ["\n\n".join(raw_paras)]

    k = max(2, round(total_words / target_words))
    target_per_block = total_words // k

    blocks = []
    curr_paras = []
    curr_words = 0

    for p in raw_paras:
        p_words = len(p.split())
        if len(blocks) < k - 1 and curr_words + p_words > target_per_block and curr_paras:
            blocks.append("\n\n".join(curr_paras))
            curr_paras = [p]
            curr_words = p_words
        else:
            curr_paras.append(p)
            curr_words += p_words

    if curr_paras:
        blocks.append("\n\n".join(curr_paras))

    return blocks

def clip_block_by_anchors(block_text: str, boundaries: list[SemanticBoundary], base_title: str) -> list[dict]:
    """Clip a text block at exact line numbers matching the verbatim anchors."""
    if not boundaries:
        return [{"title": base_title, "text": block_text}]

    lines = block_text.splitlines()
    split_indices = []
    titles = []

    for b in boundaries:
        anchor = b.first_sentence_verbatim.strip().lower()
        if not anchor:
            continue
        anchor_sub = anchor[:35] if len(anchor) >= 35 else anchor
        found_idx = -1
        for idx, line in enumerate(lines):
            line_clean = line.strip().lower()
            if not line_clean:
                continue
            # Avoid false positives: require minimum length before checking line_clean in anchor
            if anchor in line_clean or (len(anchor) >= 20 and anchor[:30] in line_clean) or (len(line_clean) >= 25 and line_clean in anchor):
                found_idx = idx
                break

        if found_idx != -1 and (not split_indices or found_idx > split_indices[-1]):
            split_indices.append(found_idx)
            titles.append(b.concept_title)

    if not split_indices:
        return [{"title": base_title, "text": block_text}]

    slices = []
    prepend_to_first = ""

    # Handle text preceding the first boundary
    if split_indices[0] > 0:
        head_text = "\n".join(lines[0:split_indices[0]]).strip()
        if len(head_text.split()) < 25:
            # Prepend small header to the first slice instead of creating an orphan chunk
            prepend_to_first = head_text + "\n\n"
        else:
            slices.append({"title": f"{base_title} (Intro)", "text": head_text})

    for i in range(len(split_indices)):
        start = split_indices[i]
        end = split_indices[i + 1] if i + 1 < len(split_indices) else len(lines)
        slice_text = "\n".join(lines[start:end]).strip()
        if i == 0 and prepend_to_first:
            slice_text = prepend_to_first + slice_text
        slices.append({"title": titles[i], "text": slice_text})
    raw_slices = slices if slices else [{"title": base_title, "text": block_text}]
    return ensure_minimum_chunk_floor(raw_slices, min_words=35)

def ensure_minimum_chunk_floor(slices: list[dict], min_words: int = 35) -> list[dict]:
    """
    Merge undersized runt slices (< 35 words) into adjacent slices to prevent fragmentation,
    while preserving semantic purity of titles instead of blindly concatenating with ' / '.
    """
    if len(slices) <= 1:
        return slices

    merged = []
    curr = None
    for s in slices:
        w_count = len(s["text"].split())
        if curr is None:
            curr = dict(s)
        elif len(curr["text"].split()) < min_words:
            # Current accumulator is a runt intro/bridge; merge it into the incoming concept
            curr_title = curr["title"]
            incoming_title = s["title"]
            if "(intro)" in curr_title.lower() or len(curr["text"].split()) < 20:
                final_title = incoming_title
            else:
                final_title = f"{curr_title}: {incoming_title}" if curr_title != incoming_title else curr_title
            curr["title"] = final_title
            curr["text"] = f"{curr['text']}\n\n{s['text']}"
        elif w_count < min_words:
            # Incoming slice is a runt trailing remark/note; fold it into current
            curr["text"] = f"{curr['text']}\n\n{s['text']}"
        else:
            merged.append(curr)
            curr = dict(s)

    if curr:
        if merged and len(curr["text"].split()) < min_words:
            merged[-1]["text"] = f"{merged[-1]['text']}\n\n{curr['text']}"
        else:
            merged.append(curr)

    return merged

@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=8,
    max_time=180,
    jitter=backoff.full_jitter,
    on_backoff=lambda details: print(
        f"  [RateLimit/Retry] Backing off {details['wait']:.1f}s after try {details['tries']}..."
    )
)
def run_splitter_with_backoff(splitter, **kwargs):
    return splitter(**kwargs)

class ChunkStreamManager:
    """Manages streaming append of chunks, history logging, and checkpoint tracking."""
    def __init__(self, jsonl_path: Path, json_path: Path, checkpoint_path: Path,
                 history_log_path: Path, reprocess_all: bool = False):
        self.jsonl_path = jsonl_path
        self.json_path = json_path
        self.checkpoint_path = checkpoint_path
        self.history_log_path = history_log_path
        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)
        self.current_file_chunks = []

        if reprocess_all:
            if self.jsonl_path.exists():
                self.jsonl_path.unlink()
            if self.json_path.exists():
                self.json_path.unlink()
            if self.checkpoint_path.exists():
                self.checkpoint_path.unlink()
            if self.history_log_path.exists():
                self.history_log_path.unlink()
            self.completed_files = set()
            self.current_chunk_id = 0
            self.all_chunks = []
        else:
            ckpt_files = self._load_checkpoint()
            hist_files = self._load_completed_from_history()
            self.completed_files = ckpt_files.union(hist_files)
            self.all_chunks = self._load_existing_chunks()
            self.current_chunk_id = max((c["chunk_id"] for c in self.all_chunks), default=0)

        self._out_f = open(self.jsonl_path, "a", encoding="utf-8")

    def _load_completed_from_history(self) -> set[str]:
        completed = set()
        if self.history_log_path.exists():
            with open(self.history_log_path, "r", encoding="utf-8") as f:
                for line in f:
                    m = re.search(r"COMPLETED:\s*([^\s|]+)", line)
                    if m:
                        completed.add(m.group(1).strip())
        return completed

    def _load_checkpoint(self) -> set[str]:
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return set(data.get("completed_files", []))
            except Exception:
                pass
        return set()

    def _save_checkpoint(self):
        with open(self.checkpoint_path, "w", encoding="utf-8") as f:
            json.dump({
                "completed_files": sorted(list(self.completed_files)),
                "total_chunks": self.current_chunk_id,
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=2)

    def _load_existing_chunks(self) -> list[dict]:
        chunks = []
        if self.jsonl_path.exists():
            with open(self.jsonl_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            chunks.append(json.loads(line))
                        except Exception:
                            pass
        return chunks

    def is_file_completed(self, file_key: str) -> bool:
        return file_key in self.completed_files

    def mark_file_completed(self, file_key: str):
        self.completed_files.add(file_key)
        self._save_checkpoint()
        self.sync_to_json()

        # Append to processing history log
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        chunk_count = len(self.current_file_chunks)
        if chunk_count > 0:
            first_id = self.current_file_chunks[0]["chunk_id"]
            last_id = self.current_file_chunks[-1]["chunk_id"]
            total_words = sum(c["word_count"] for c in self.current_file_chunks)
            log_line = f"[{timestamp}] COMPLETED: {file_key:<55} | Chunks: {chunk_count:3d} (IDs: #{first_id:04d}-#{last_id:04d}) | Words: {total_words:6,d}\n"
        else:
            log_line = f"[{timestamp}] COMPLETED: {file_key:<55} | Chunks:   0 | Words:      0\n"

        with open(self.history_log_path, "a", encoding="utf-8") as hf:
            hf.write(log_line)
            hf.flush()

        self.current_file_chunks = []

    def add_chunk(self, source_file: str, breadcrumb: str, title: str, text: str) -> dict:
        self.current_chunk_id += 1
        words = text.split()
        chunk = {
            "chunk_id": self.current_chunk_id,
            "chunk_type": "documentation",
            "source_file": source_file,
            "breadcrumb": breadcrumb,
            "title": title,
            "word_count": len(words),
            "text": text
        }
        self.all_chunks.append(chunk)
        self.current_file_chunks.append(chunk)
        self._out_f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        self._out_f.flush()
        os.fsync(self._out_f.fileno())
        return chunk

    def sync_to_json(self):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.all_chunks, f, indent=2, ensure_ascii=False)

    def close(self):
        if not self._out_f.closed:
            self._out_f.close()
        self.sync_to_json()
        self._save_checkpoint()

def process_document_text(full_text: str, source_file: str, splitter, delay: float,
                          stream_mgr: ChunkStreamManager, full_md_lines: list[str] = None):
    words = full_text.split()
    total_words = len(words)
    if total_words < 15:
        return

    file_title = Path(source_file).stem.replace("_", " ").title()
    is_scm = Path(source_file).suffix.lower() == ".scm"

    # For .scm code files <= 1000 words, preserve as 1 complete atomic protocol model
    # For prose/guides, preserve <= 150 words directly as 1 atomic chunk
    if (is_scm and total_words <= TARGET_BLOCK_WORDS) or total_words <= MIN_SPLIT_WORDS or not splitter:
        breadcrumb = f"{file_title} > Complete Protocol" if is_scm else f"{file_title} > Overview"
        chunk = stream_mgr.add_chunk(
            source_file=source_file,
            breadcrumb=breadcrumb,
            title=file_title,
            text=full_text
        )
        print(f"  [Chunk {chunk['chunk_id']:04d}] Saved atomic ({total_words} words): '{file_title}'")
        if full_md_lines is not None:
            full_md_lines.append(f"\n## {file_title}\n*({breadcrumb})*\n\n{full_text}\n")
        return

    # Slices document into cohesive ~1000-word paragraph blocks
    blocks = partition_into_paragraph_blocks(full_text, target_words=TARGET_BLOCK_WORDS)
    total_blocks = len(blocks)

    for b_idx, block_text in enumerate(blocks, 1):
        b_words = len(block_text.split())
        block_breadcrumb = f"{file_title} > Block {b_idx}/{total_blocks}"

        # If block is small, keep as-is
        if b_words <= MIN_SPLIT_WORDS:
            chunk = stream_mgr.add_chunk(
                source_file=source_file,
                breadcrumb=block_breadcrumb,
                title=f"{file_title} (Part {b_idx})",
                text=block_text
            )
            print(f"  [Chunk {chunk['chunk_id']:04d}] Saved atomic ({b_words} words): '{chunk['title']}'")
            continue

        # Send ~1000-word block to Gemini 3.1 Flash Lite for semantic boundary detection
        boundaries = []
        try:
            print(f"  [Semantic Split] Block {b_idx}/{total_blocks} ({b_words} words) -> Gemini 3.1 Flash Lite...")
            sys.stdout.flush()
            pred = run_splitter_with_backoff(
                splitter,
                source_context=block_breadcrumb,
                block_text=block_text
            )
            boundaries = pred.boundaries or []
            if boundaries:
                print(f"    -> Detected {len(boundaries)} semantic concepts:")
                for b in boundaries:
                    print(f"       * [{b.concept_title}]")
                sys.stdout.flush()
            if delay > 0:
                time.sleep(delay)
        except Exception as e:
            print(f"    -> Splitter warning for {block_breadcrumb}: {e}", file=sys.stderr)
            sys.stdout.flush()

        # Clip the block text at exact line numbers matching verbatim anchors
        slices = clip_block_by_anchors(block_text, boundaries, base_title=f"{file_title} (Part {b_idx})")

        for s in slices:
            sub_title = s["title"]
            sub_text = s["text"]
            sub_words = len(sub_text.split())
            chunk_breadcrumb = f"{file_title} > {sub_title}"

            chunk = stream_mgr.add_chunk(
                source_file=source_file,
                breadcrumb=chunk_breadcrumb,
                title=sub_title,
                text=sub_text
            )
            print(f"  [Chunk {chunk['chunk_id']:04d}] Saved slice ({sub_words} words): '{sub_title}'")

            if full_md_lines is not None:
                full_md_lines.append(f"\n### {sub_title}\n*({chunk_breadcrumb})*\n\n{sub_text}\n")

def read_file_content(file_path: Path) -> str:
    """Read content according to file type."""
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        doc = pymupdf.open(file_path)
        pages_text = [clean_page_text(p.get_text()) for p in doc]
        return "\n\n".join([t for t in pages_text if t]).strip()
    else:
        return file_path.read_text(encoding="utf-8", errors="ignore").strip()

def discover_corpus_files(search_dirs: list[Path]) -> list[Path]:
    """Recursively discover all scannable files in search directories."""
    discovered = []
    for d in search_dirs:
        if not d.exists():
            continue
        for p in sorted(d.rglob("*")):
            if not p.is_file():
                continue
            if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if p.name in EXCLUDE_FILENAMES:
                continue
            # Skip papers_pdf because we already converted papers to text in guides_markdown
            if "papers_pdf" in p.parts and p.suffix.lower() == ".pdf":
                continue
            discovered.append(p)
    return discovered

def process_file(file_path: Path, splitter, delay: float,
                 stream_mgr: ChunkStreamManager, full_md_lines: list[str]):
    try:
        rel_path = str(file_path.relative_to(BASE_DIR))
    except ValueError:
        rel_path = file_path.name

    if stream_mgr.is_file_completed(rel_path):
        print(f"[Skip] Already completed in history/checkpoint: '{rel_path}'")
        return

    print(f"\n========================================================")
    print(f"[Processing] {rel_path}")
    print(f"========================================================")
    sys.stdout.flush()

    content = read_file_content(file_path)
    process_document_text(
        full_text=content,
        source_file=rel_path,
        splitter=splitter,
        delay=delay,
        stream_mgr=stream_mgr,
        full_md_lines=full_md_lines
    )

    stream_mgr.mark_file_completed(rel_path)
    print(f"[Completed] '{rel_path}' -> Total chunks in DB: {stream_mgr.current_chunk_id}")

def main():
    parser = argparse.ArgumentParser(description="Uniform 1000-word block semantic chunker for CPSA.")
    parser.add_argument("--dir", "-d", type=str, default=None,
                        help="Target directory to scan (defaults to refrences/manual and refrences/internet).")
    parser.add_argument("--file", "-f", type=str, default=None,
                        help="Process a single specific file path.")
    parser.add_argument("--no-llm", action="store_true",
                        help="Disable Gemini LLM; slice strictly at 1000-word paragraph boundaries.")
    parser.add_argument("--semantic-split", action="store_true", default=True,
                        help="Enable semantic line-break splitting (default: True, kept for compatibility).")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL,
                        help=f"Model identifier (e.g. gemini/gemini-3.1-flash-lite). Default: {DEFAULT_MODEL}")
    parser.add_argument("--api-key", type=str, default=DEFAULT_API_KEY,
                        help="Gemini API key (defaults to GEMINI_API_KEY from .env).")
    parser.add_argument("--api-base", type=str, default=DEFAULT_API_BASE,
                        help=f"Ollama API base URL. Default: {DEFAULT_API_BASE}")
    parser.add_argument("--delay", type=float, default=None,
                        help="Pacing delay (seconds) between LLM calls. Default: 3.5s for Gemini, 0.0s for local.")
    parser.add_argument("--reprocess-all", action="store_true",
                        help="Clear checkpoint and history log to reprocess all chunks from scratch.")
    args = parser.parse_args()

    splitter = None
    is_gemini = args.model.startswith("gemini") or "gemini" in args.model.lower()
    delay = args.delay if args.delay is not None else (3.5 if is_gemini else 0.0)

    if not args.no_llm:
        if is_gemini:
            model_tag = args.model if args.model.startswith("gemini/") else f"gemini/{args.model}"
            api_key = args.api_key or os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                print("Error: GEMINI_API_KEY is required for Gemini models. Set it in .env or pass --api-key.", file=sys.stderr)
                sys.exit(1)
            os.environ["GEMINI_API_KEY"] = api_key
            print(f"Configuring Gemini ('{model_tag}', delay: {delay}s) for 1000-word block splitting...")
            lm = dspy.LM(model_tag, api_key=api_key)
        else:
            clean_model = args.model
            for prefix in ["ollama_chat/", "ollama/"]:
                if clean_model.startswith(prefix):
                    clean_model = clean_model[len(prefix):]
            print(f"Connecting to Ollama at {args.api_base} with model '{clean_model}'...")
            lm = dspy.LM(f"ollama_chat/{clean_model}", api_base=args.api_base, api_key="", temperature=0.1)

        dspy.configure(lm=lm)
        splitter = dspy.Predict(SemanticBlockSplitter)

    stream_mgr = ChunkStreamManager(
        jsonl_path=CHUNKS_JSONL_PATH,
        json_path=CHUNKS_JSON_PATH,
        checkpoint_path=CHECKPOINT_PATH,
        history_log_path=HISTORY_LOG_PATH,
        reprocess_all=args.reprocess_all
    )

    full_md_lines = ["# Complete CPSA Reference Corpus (Clean Markdown)\n"]

    if args.file:
        target_path = Path(args.file).resolve()
        if not target_path.exists():
            print(f"Error: Target file '{target_path}' not found.", file=sys.stderr)
            sys.exit(1)
        all_files = [target_path]
    elif args.dir:
        search_dir = Path(args.dir).resolve()
        all_files = discover_corpus_files([search_dir])
    else:
        all_files = discover_corpus_files(DEFAULT_SEARCH_DIRS)

    print(f"\n========================================================")
    print(f"CPSA 1000-Word Block Semantic Decomposer")
    print(f"  Discovered scannable files:    {len(all_files)}")
    print(f"  Existing chunks in database:   {len(stream_mgr.all_chunks)}")
    print(f"  Completed files recognized:    {len(stream_mgr.completed_files)}")
    print(f"  Target block size:             ~{TARGET_BLOCK_WORDS} words")
    print(f"  Semantic line-break splitting: {'ENABLED (Gemini 3.1 Flash Lite)' if splitter else 'DISABLED'}")
    print(f"========================================================\n")

    for f_path in all_files:
        process_file(
            file_path=f_path,
            splitter=splitter,
            delay=delay,
            stream_mgr=stream_mgr,
            full_md_lines=full_md_lines
        )

    stream_mgr.close()

    if len(full_md_lines) > 1:
        with open(CLEAN_MD_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(full_md_lines))
        print(f"\n[Saved] Consolidated clean markdown to {CLEAN_MD_PATH}")

    total = len(stream_mgr.all_chunks)
    print(f"\nFinished processing.")
    print(f"Total atomic semantic chunks: {total}")
    if total > 0:
        words = [c["word_count"] for c in stream_mgr.all_chunks]
        print(f"Word count: min={min(words)}, max={max(words)}, median={sorted(words)[total // 2]}")
    print(f"Chunks saved to:\n  - {CHUNKS_JSONL_PATH}\n  - {CHUNKS_JSON_PATH}")
    print(f"History log saved to:\n  - {HISTORY_LOG_PATH}")
    print(f"Checkpoint saved to:\n  - {CHECKPOINT_PATH}")

if __name__ == "__main__":
    main()
```

---

### `refrences/scripts/02_extract_code_examples.py`

*sha256:`15d8adabeeb7` · 513 lines · 22.9 KB (~5,858 tokens) · lang:`python`*

```python
#!/usr/bin/env python3
"""
02_extract_code_examples.py
Extracts CPSA SCM Code Examples with Full Formal Grammar Features and Semantic Scenario Summaries.

Architecture:
- Ingests all .scm files across refrences/internet/examples_scm/
- 100% Intact Code: Never splits S-expressions; every .scm file is preserved as an atomic executable model.
- Option C (Static AST Extraction): Extracts heralds, protocols, algebras, roles, cryptographic primitives,
  channels, state locations, assumptions (non-orig, uniq-orig, pen-non-orig), rules, and comments.
- Option B (Gemini 3.1 Flash Lite Summary): Generates a natural, short, and informative overview of what protocol
  is modeled, security properties/attacks analyzed (MITM, replay, secrecy), and key modeling mechanisms.
- Streaming Persistence: Writes immediately to code_examples.jsonl and syncs to code_examples.json.
- Also appends to manual_chunks.jsonl so the retriever can search documentation and code examples simultaneously.
- Checkpointing & History Logging: Skips completed files on reruns.
"""

import os
import sys
import time
import json
import re
import argparse
import logging
import warnings
from pathlib import Path
from pydantic import BaseModel, Field
import dspy
import backoff
from dotenv import load_dotenv, find_dotenv
import litellm

# Silence LiteLLM log spam and deprecation warnings
litellm.suppress_debug_info = True
litellm.set_verbose = False
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning)

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(usecwd=True))
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

EXAMPLES_DIR = BASE_DIR / "internet" / "examples_scm"
CHUNKS_DIR = BASE_DIR / "chunks"
CODE_JSONL_PATH = CHUNKS_DIR / "code_examples.jsonl"
CODE_JSON_PATH = CHUNKS_DIR / "code_examples.json"
MANUAL_JSONL_PATH = CHUNKS_DIR / "manual_chunks.jsonl"
MANUAL_JSON_PATH = CHUNKS_DIR / "manual_chunks.json"
CHECKPOINT_PATH = CHUNKS_DIR / "code_examples_checkpoint.json"
HISTORY_LOG_PATH = CHUNKS_DIR / "code_examples_history.log"

DEFAULT_MODEL = os.environ.get("MODEL_NAME", "gemini/gemini-3.1-flash-lite")
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

# =====================================================================
# Option C: Static Formal CPSA Grammar Feature Extractor
# =====================================================================

def strip_scheme_comments(content: str) -> str:
    """Strip line comments (;...) and block comments (#|...|#) while preserving string literals."""
    strings = []
    def save_str(m):
        strings.append(m.group(0))
        return f"__STR_LITERAL_{len(strings)-1}__"

    # Protect string literals from semicolon stripping
    protected = re.sub(r'"(?:\\.|[^"\\])*"', save_str, content)
    # Strip block comments #| ... |#
    protected = re.sub(r'#\|.*?\|#', ' ', protected, flags=re.DOTALL)
    # Strip line comments ; ...
    protected = re.sub(r';.*$', ' ', protected, flags=re.MULTILINE)
    # Restore string literals
    for idx, s in enumerate(strings):
        protected = protected.replace(f"__STR_LITERAL_{idx}__", s)
    return protected

def parse_cpsa_scm(content: str, file_name: str) -> dict:
    """Extract complete formal CPSA 4.4 grammar AST features from an S-expression file."""
    # 1. Developer Intent Comments (extracted from raw content before stripping)
    dev_comments = [line.strip("; \t") for line in re.findall(r";;;+(.+)", content) if line.strip("; \t")]

    # 2. Strip comments to analyze only active syntax forms
    clean_code = strip_scheme_comments(content)

    # 3. Herald Title and Comment
    m_herald = re.search(r"\(herald\s+[\"\x27]([^\"]+)[\"\x27](.*?)\)", clean_code, re.DOTALL)
    herald_title = m_herald.group(1).strip() if m_herald else ""
    herald_comment = ""
    if m_herald:
        m_c = re.search(r"\(comment\s+[\"\x27]([^\"]+)[\"\x27]", m_herald.group(2))
        if m_c:
            herald_comment = m_c.group(1).strip()

    # 4. Protocols and Algebras
    protocols = []
    for pm in re.finditer(r"\(defprotocol\s+([^\s\(\)]+)\s+([^\s\(\)]+)", clean_code):
        protocols.append({"name": pm.group(1), "algebra": pm.group(2)})
    algebras = list(dict.fromkeys([p["algebra"] for p in protocols]))
    if re.search(r"\bdiffie-hellman\b", clean_code) and "diffie-hellman" not in algebras:
        algebras.append("diffie-hellman")

    # 5. Roles
    roles = list(dict.fromkeys(re.findall(r"\(defrole\s+([^\s\(\)]+)", clean_code)))

    # 6. Sorts
    all_sorts = ["text", "data", "name", "skey", "akey", "mesg", "chan", "locn", "rndx", "expt", "base", "strd"]
    sorts_used = [s for s in all_sorts if re.search(r"\b" + s + r"\b", clean_code)]

    # 7. Cryptographic Primitives
    all_crypto = ["pubk", "privk", "invk", "ltk", "cat", "enc", "senc", "aenc", "sign", "hash", "exp", "gen", "mul", "rec"]
    crypto_used = [c for c in all_crypto if re.search(r"\b" + c + r"\b", clean_code)]

    # 8. Channels and State Operations
    all_state_chan = ["auth", "conf", "stor", "load", "gen-st", "critical-sections"]
    state_chan_used = [sc for sc in all_state_chan if re.search(r"\b" + sc + r"\b", clean_code)]

    # 9. Assumptions and Constraints
    all_assumptions = ["non-orig", "pen-non-orig", "uniq-orig", "uniq-gen", "precedes", "priority", "facts"]
    assumptions_used = [a for a in all_assumptions if re.search(r"\b" + a + r"\b", clean_code)]

    # 10. Top-Level Entity Counts
    skel_count = len(re.findall(r"\(defskeleton\b", clean_code))
    listener_count = len(re.findall(r"\(deflistener\b", clean_code))
    goal_count = len(re.findall(r"\(defgoal\b", clean_code))
    rule_count = len(re.findall(r"\(defrule\b|\(rule\b", clean_code))

    title = herald_title or Path(file_name).stem.replace("_", " ").title()

    return {
        "file": file_name,
        "title": title,
        "herald_title": herald_title,
        "herald_comment": herald_comment,
        "protocols": protocols,
        "algebras": algebras,
        "roles": roles,
        "sorts": sorts_used,
        "crypto_primitives": crypto_used,
        "channels_and_state": state_chan_used,
        "assumptions": assumptions_used,
        "counts": {
            "skeletons": skel_count,
            "listeners": listener_count,
            "goals": goal_count,
            "rules": rule_count
        },
        "dev_comments": dev_comments[:4]
    }

# =====================================================================
# Option B: Gemini 3.1 Flash Lite Scenario Summarizer
# =====================================================================

class SCMExampleSummarizer(dspy.Signature):
    """You are a formal methods expert and cryptographic protocol analyst specializing in CPSA.
Analyze the provided CPSA Scheme (.scm) source code and its extracted AST metadata.
Synthesize a concise, rigorous technical summary of the protocol model.

Requirements:
1. Scenario & Classification: Identify the specific protocol or cryptographic interaction being modeled. If the file is a theoretical benchmark, regression test, minimal counterexample, or sanity check rather than an RFC protocol, explicitly state its theoretical purpose. Do not force-map abstract models to named real-world protocols.
2. Security Properties & Goals: State the exact security invariants, shapes, or adversarial behaviors under verification, as evidenced by the skeletons, listeners, and goal declarations.
3. Formal Modeling Constructs: Detail the key CPSA primitives actually declared in formal_metadata and the code (algebras, sorts, channel abstractions, state operations, origination assumptions, and custom rewrite rules). Never reference primitives that are absent from the model.
4. Grounding: Base the summary strictly on the source code, comments, and formal AST. Avoid generic boilerplate.
5. Determinism: Maintain strict factual precision and low variance. State only verifiable AST constructs and explicit security goals."""
    file_name: str = dspy.InputField(desc="Filename of the CPSA Scheme model")
    formal_metadata: str = dspy.InputField(desc="Extracted formal AST features (herald, protocols, roles, primitives, assumptions)")
    scm_code: str = dspy.InputField(desc="Verbatim Scheme source code")
    scenario_summary: str = dspy.OutputField(desc="Accurate, factual 2-4 sentence summary of the model's protocol scenario, security properties, and modeling mechanics")
    tags: list[str] = dspy.OutputField(desc="List of 3 to 6 lowercase kebab-case tags capturing the protocol name, algebra, key primitives, and verified properties")

@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=8,
    max_time=180,
    jitter=backoff.full_jitter,
    on_backoff=lambda details: print(
        f"  [RateLimit/Retry] Backing off {details['wait']:.1f}s after try {details['tries']}..."
    )
)
def run_summarizer_with_backoff(summarizer, **kwargs):
    return summarizer(**kwargs)

# =====================================================================
# Stream and Checkpoint Manager
# =====================================================================

class CodeExampleStreamManager:
    def __init__(self, code_jsonl_path: Path, code_json_path: Path,
                 manual_jsonl_path: Path, manual_json_path: Path,
                 checkpoint_path: Path, history_log_path: Path,
                 reprocess_all: bool = False):
        self.code_jsonl_path = code_jsonl_path
        self.code_json_path = code_json_path
        self.manual_jsonl_path = manual_jsonl_path
        self.manual_json_path = manual_json_path
        self.checkpoint_path = checkpoint_path
        self.history_log_path = history_log_path

        self.code_jsonl_path.parent.mkdir(parents=True, exist_ok=True)

        if reprocess_all:
            if self.code_jsonl_path.exists():
                self.code_jsonl_path.unlink()
            if self.code_json_path.exists():
                self.code_json_path.unlink()
            if self.checkpoint_path.exists():
                self.checkpoint_path.unlink()
            if self.history_log_path.exists():
                self.history_log_path.unlink()
            # Strip previous code_example records from manual_chunks.jsonl to avoid duplicates
            if self.manual_jsonl_path.exists():
                doc_lines = []
                with open(self.manual_jsonl_path, "r", encoding="utf-8") as mf:
                    for line in mf:
                        if line.strip():
                            try:
                                rec = json.loads(line)
                                if rec.get("chunk_type") != "code_example":
                                    doc_lines.append(line)
                            except Exception:
                                doc_lines.append(line)
                with open(self.manual_jsonl_path, "w", encoding="utf-8") as mf:
                    mf.writelines(doc_lines)
            self.completed_files = set()
            self.all_examples = []
            self.current_chunk_id = self._get_next_manual_chunk_id()
        else:
            self.completed_files = self._load_completed()
            self.all_examples = self._load_existing_examples()
            self.current_chunk_id = self._get_next_manual_chunk_id()

        self._code_f = open(self.code_jsonl_path, "a", encoding="utf-8")
        self._manual_f = open(self.manual_jsonl_path, "a", encoding="utf-8") if self.manual_jsonl_path.exists() else None

    def _get_next_manual_chunk_id(self) -> int:
        max_id = 0
        if self.manual_jsonl_path.exists():
            with open(self.manual_jsonl_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            c = json.loads(line)
                            if c.get("chunk_type") != "code_example":
                                max_id = max(max_id, c.get("chunk_id", 0))
                        except Exception:
                            pass
        return max_id

    def _load_completed(self) -> set[str]:
        completed = set()
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    completed.update(data.get("completed_files", []))
            except Exception:
                pass
        if self.history_log_path.exists():
            with open(self.history_log_path, "r", encoding="utf-8") as f:
                for line in f:
                    m = re.search(r"COMPLETED:\s*([^\s|]+)", line)
                    if m:
                        completed.add(m.group(1).strip())
        return completed

    def _load_existing_examples(self) -> list[dict]:
        examples = []
        if self.code_jsonl_path.exists():
            with open(self.code_jsonl_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            examples.append(json.loads(line))
                        except Exception:
                            pass
        return examples

    def is_file_completed(self, file_key: str) -> bool:
        return file_key in self.completed_files

    def add_example(self, source_file: str, meta: dict, scenario_summary: str, tags: list[str], code: str) -> dict:
        self.current_chunk_id += 1
        prot_names = ", ".join([p["name"] for p in meta.get("protocols", [])]) or "protocol"
        breadcrumb = f"Code Examples > {prot_names} > {meta['title']}"

        chunk = {
            "chunk_id": self.current_chunk_id,
            "chunk_type": "code_example",
            "source_file": source_file,
            "breadcrumb": breadcrumb,
            "title": meta["title"],
            "word_count": len(code.split()),
            "scenario_summary": scenario_summary,
            "tags": tags,
            "formal_metadata": meta,
            "text": code
        }

        self.all_examples.append(chunk)

        # Write to code_examples.jsonl
        self._code_f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        self._code_f.flush()
        os.fsync(self._code_f.fileno())

        # Also append to manual_chunks.jsonl for unified RAG search (check deduplication)
        if self._manual_f:
            already_in_manual = False
            if self.manual_jsonl_path.exists():
                with open(self.manual_jsonl_path, "r", encoding="utf-8") as mf:
                    for line in mf:
                        if f'"{source_file}"' in line:
                            already_in_manual = True
                            break
            if not already_in_manual:
                self._manual_f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                self._manual_f.flush()
                os.fsync(self._manual_f.fileno())

        return chunk

    def mark_completed(self, file_key: str, words: int):
        self.completed_files.add(file_key)
        self._save_checkpoint()
        self.sync_to_json()

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] COMPLETED: {file_key:<55} | Words: {words:6,d}\n"
        with open(self.history_log_path, "a", encoding="utf-8") as hf:
            hf.write(log_line)
            hf.flush()

    def _save_checkpoint(self):
        with open(self.checkpoint_path, "w", encoding="utf-8") as f:
            json.dump({
                "completed_files": sorted(list(self.completed_files)),
                "total_examples": len(self.all_examples),
                "last_chunk_id": self.current_chunk_id,
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=2)

    def sync_to_json(self):
        with open(self.code_json_path, "w", encoding="utf-8") as f:
            json.dump(self.all_examples, f, indent=2, ensure_ascii=False)

    def close(self):
        if not self._code_f.closed:
            self._code_f.close()
        if self._manual_f and not self._manual_f.closed:
            self._manual_f.close()
        self.sync_to_json()
        self._save_checkpoint()

# =====================================================================
# Processing Logic
# =====================================================================

def process_scm_file(scm_path: Path, summarizer, delay: float, stream_mgr: CodeExampleStreamManager):
    file_key = f"internet/examples_scm/{scm_path.name}"
    if stream_mgr.is_file_completed(file_key):
        print(f"[Skip] Already completed: {file_key}")
        return

    code = scm_path.read_text(encoding="utf-8", errors="ignore").strip()
    words = len(code.split())
    if words < 10:
        return

    print(f"\n========================================================")
    print(f"[Processing SCM Example] {file_key} ({words} words)")
    print(f"========================================================")

    # 1. Option C: Static Formal CPSA Grammar Extraction
    meta = parse_cpsa_scm(code, scm_path.name)
    print(f"  Title:      {meta['title']}")
    if meta['herald_comment']:
        print(f"  Comment:    {meta['herald_comment']}")
    print(f"  Protocols:  {meta['protocols']}")
    print(f"  Roles:      {meta['roles']}")
    print(f"  Primitives: {meta['crypto_primitives']}")
    print(f"  Assumptions:{meta['assumptions']}")

    # 2. Option B: Gemini 3.1 Flash Lite Scenario Summarization
    scenario_summary = ""
    tags = []
    if summarizer:
        meta_str = json.dumps(meta, indent=2)
        try:
            print(f"  -> Generating scenario summary via Gemini 3.1 Flash Lite...")
            sys.stdout.flush()
            pred = run_summarizer_with_backoff(
                summarizer,
                file_name=scm_path.name,
                formal_metadata=meta_str,
                scm_code=code
            )
            scenario_summary = getattr(pred, "scenario_summary", "").strip()
            tags = getattr(pred, "tags", []) or []
            print(f"  -> Summary: {scenario_summary}")
            print(f"  -> Tags:    {tags}")
            if delay > 0:
                time.sleep(delay)
        except Exception as e:
            print(f"  -> Summarizer warning for {scm_path.name}: {e}", file=sys.stderr)
            scenario_summary = meta.get("herald_comment", "") or f"Example CPSA protocol model for {meta['title']}."
            tags = [p["name"] for p in meta.get("protocols", [])]
    else:
        scenario_summary = meta.get("herald_comment", "") or f"Example CPSA protocol model for {meta['title']}."
        tags = [p["name"] for p in meta.get("protocols", [])]

    chunk = stream_mgr.add_example(
        source_file=file_key,
        meta=meta,
        scenario_summary=scenario_summary,
        tags=tags,
        code=code
    )
    print(f"  [Chunk #{chunk['chunk_id']:04d}] Saved un-split SCM example: '{chunk['title']}'")

    stream_mgr.mark_completed(file_key, words)

# =====================================================================
# Main CLI
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description="Extract CPSA SCM Code Examples with Formal AST and Scenario Summaries.")
    parser.add_argument("--file", "-f", type=str, default=None, help="Process a single specific .scm file.")
    parser.add_argument("--no-llm", action="store_true", help="Disable Gemini LLM; use static AST metadata and comments only.")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help=f"Model identifier. Default: {DEFAULT_MODEL}")
    parser.add_argument("--api-key", type=str, default=DEFAULT_API_KEY, help="Gemini API key.")
    parser.add_argument("--api-base", type=str, default=DEFAULT_API_BASE, help="Ollama API base URL.")
    parser.add_argument("--delay", type=float, default=None, help="Pacing delay between LLM calls. Default: 3.5s for Gemini.")
    parser.add_argument("--reprocess-all", action="store_true", help="Clear checkpoint and reprocess all files.")
    args = parser.parse_args()

    summarizer = None
    is_gemini = args.model.startswith("gemini") or "gemini" in args.model.lower()
    delay = args.delay if args.delay is not None else (3.5 if is_gemini else 0.0)

    if not args.no_llm:
        if is_gemini:
            model_tag = args.model if args.model.startswith("gemini/") else f"gemini/{args.model}"
            api_key = args.api_key or os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                print("Error: GEMINI_API_KEY is required for Gemini models.", file=sys.stderr)
                sys.exit(1)
            os.environ["GEMINI_API_KEY"] = api_key
            print(f"Configuring Gemini ('{model_tag}', delay: {delay}s) for SCM scenario summarization...")
            lm = dspy.LM(model_tag, api_key=api_key)
        else:
            clean_model = args.model
            for prefix in ["ollama_chat/", "ollama/"]:
                if clean_model.startswith(prefix):
                    clean_model = clean_model[len(prefix):]
            print(f"Connecting to Ollama at {args.api_base} with model '{clean_model}'...")
            lm = dspy.LM(f"ollama_chat/{clean_model}", api_base=args.api_base, api_key="", temperature=0.2)

        dspy.configure(lm=lm)
        summarizer = dspy.Predict(SCMExampleSummarizer)

    stream_mgr = CodeExampleStreamManager(
        code_jsonl_path=CODE_JSONL_PATH,
        code_json_path=CODE_JSON_PATH,
        manual_jsonl_path=MANUAL_JSONL_PATH,
        manual_json_path=MANUAL_JSON_PATH,
        checkpoint_path=CHECKPOINT_PATH,
        history_log_path=HISTORY_LOG_PATH,
        reprocess_all=args.reprocess_all
    )

    if args.file:
        target_path = Path(args.file).resolve()
        if not target_path.exists():
            print(f"Error: Target file '{target_path}' not found.", file=sys.stderr)
            sys.exit(1)
        all_files = [target_path]
    else:
        all_files = sorted(list(EXAMPLES_DIR.glob("*.scm")))

    print(f"\n========================================================")
    print(f"CPSA SCM Code Examples Pipeline")
    print(f"  Discovered SCM files:        {len(all_files)}")
    print(f"  Existing SCM examples in DB: {len(stream_mgr.all_examples)}")
    print(f"  Completed files recognized:  {len(stream_mgr.completed_files)}")
    print(f"  Summarization:               {'ENABLED (Gemini 3.1 Flash Lite)' if summarizer else 'DISABLED (Static AST Only)'}")
    print(f"========================================================\n")

    for f_path in all_files:
        process_scm_file(
            scm_path=f_path,
            summarizer=summarizer,
            delay=delay,
            stream_mgr=stream_mgr
        )

    stream_mgr.close()

    total = len(stream_mgr.all_examples)
    print(f"\nFinished SCM processing.")
    print(f"Total SCM code examples in catalog: {total}")
    print(f"Catalog saved to:\n  - {CODE_JSONL_PATH}\n  - {CODE_JSON_PATH}")
    print(f"Also appended to:\n  - {MANUAL_JSONL_PATH}")
    print(f"History log: {HISTORY_LOG_PATH}")
    print(f"Checkpoint:  {CHECKPOINT_PATH}")

if __name__ == "__main__":
    main()
```

---

### `refrences/scripts/03_query_rag.py`

*sha256:`108c13835a78` · 438 lines · 18.5 KB (~4,740 tokens) · lang:`python`*

```python
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
```

---

### `refrences/scripts/04_build_embeddings.py`

*sha256:`4ddfc900a6ae` · 260 lines · 10.4 KB (~2,672 tokens) · lang:`python`*

```python
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
```

---

### `refrences/scripts/05_enrich_doc_chunks.py`

*sha256:`741a60e69395` · 207 lines · 7.9 KB (~2,021 tokens) · lang:`python`*

```python
#!/usr/bin/env python3
"""
Contextual Enrichment Engine for CPSA Technical Documentation Chunks.
Implements the Anthropic Contextual Retrieval technique combined with 
deterministic AST feature extraction for the 1,278 documentation chunks.
"""

import os
import sys
import json
import re
import asyncio
import time
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CHUNKS_PATH = ROOT_DIR / "refrences" / "chunks" / "manual_chunks.jsonl"
CACHE_PATH = ROOT_DIR / "refrences" / "chunks" / "context_headers_cache.json"
ENRICHED_PATH = ROOT_DIR / "refrences" / "chunks" / "manual_chunks_enriched.jsonl"
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(ENV_PATH)
import litellm

# Silence excessive LiteLLM logging
litellm.suppress_debug_info = True

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment or .env", file=sys.stderr)
    sys.exit(1)

MODEL_NAME = "gemini/gemini-3.1-flash-lite"
CONCURRENCY_LIMIT = 12

# Deterministic CPSA AST patterns
AST_PATTERNS = {
    "Forms": re.compile(r"\b(defprotocol|defrole|defskeleton|deflistener|defmacro|defrule|defgenrule)\b"),
    "Assumptions": re.compile(r"\b(non-orig|uniq-orig|pen-non-orig|uniq-gen|role_uniq)\b"),
    "Algebra Sorts": re.compile(r"\b(name|text|data|skey|akey|mesg|chan|locn)\b"),
    "Crypto Terms": re.compile(r"\b(enc|cat|hash|pubk|privk|invk|ltk)\b"),
    "Relations": re.compile(r"\b(send|recv|trace|prec|subsort|auth-test)\b")
}

def extract_ast_features(text: str) -> dict[str, list[str]]:
    """Deterministically extracts Scheme and CPSA syntax primitives from text."""
    features = {}
    for cat, pat in AST_PATTERNS.items():
        matches = sorted(list(set(pat.findall(text))))
        if matches:
            features[cat] = matches
    return features

def build_ast_summary(features: dict[str, list[str]]) -> str:
    if not features:
        return "None detected (prose/derivation)"
    parts = []
    for cat, items in features.items():
        parts.append(f"{cat}: {', '.join(items[:6])}")
    return " | ".join(parts)

SYSTEM_PROMPT = """You are a formal methods expert indexing the MITRE CPSA (Cryptographic Protocol Shapes Analyzer) documentation corpus.
Given the document metadata, detected syntax features, and chunk text, write strictly 1 to 2 concise sentences providing the global orienting context for this chunk.
State:
1. The exact document and structural section this chunk belongs to.
2. The specific protocol, algebraic sort, S-expression syntax rule, or formal verification theorem it defines.

Do NOT summarize the chunk. Output ONLY the 1-2 sentence orienting header."""

PROMPT_TEMPLATE = """Document: {source_file}
Breadcrumb: {breadcrumb}
Section Title: {title}
Detected Syntax Primitives: {ast_summary}

Chunk Text:
{text_snippet}

Context Header:"""

async def generate_header_with_retry(chunk: dict, sem: asyncio.Semaphore, max_retries: int = 5) -> str:
    source_file = chunk.get("source_file", chunk.get("doc_id", "Unknown Document"))
    breadcrumb = chunk.get("breadcrumb", "") or chunk.get("chapter", "")
    title = chunk.get("title", "")
    text = chunk.get("text", "")
    
    ast_features = extract_ast_features(text)
    ast_summary = build_ast_summary(ast_features)
    
    prompt = PROMPT_TEMPLATE.format(
        source_file=source_file,
        breadcrumb=breadcrumb,
        title=title,
        ast_summary=ast_summary,
        text_snippet=text[:1600]
    )
    
    for attempt in range(1, max_retries + 1):
        try:
            async with sem:
                resp = await litellm.acompletion(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    api_key=GEMINI_API_KEY
                )
                header = resp.choices[0].message.content.strip()
                # Clean up any quotes or markdown artifacts
                header = header.replace('"', '').strip()
                return header
        except Exception as e:
            wait_time = 2.0 ** attempt
            if attempt == max_retries:
                # Fallback to deterministic AST header on exhaustion
                return f"This chunk from {source_file} ({title}) details formal verification semantics involving {ast_summary}."
            await asyncio.sleep(wait_time)

async def main():
    print("=" * 80)
    print("CPSA DOCUMENTATION CHUNK CONTEXTUAL ENRICHMENT PIPELINE")
    print("Model: Gemini 3.1 Flash Lite | Concurrency: 12")
    print("=" * 80)
    
    # 1. Load chunks
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        all_chunks = [json.loads(line) for line in f if line.strip()]
    
    doc_chunks = [c for c in all_chunks if c.get("chunk_type") != "code_example" and not c.get("is_code", False)]
    code_chunks = [c for c in all_chunks if c.get("chunk_type") == "code_example" or c.get("is_code", False)]
    
    print(f"Loaded {len(all_chunks)} total chunks:")
    print(f"  • Documentation chunks to enrich: {len(doc_chunks)}")
    print(f"  • Code model chunks (already enriched): {len(code_chunks)}")
    
    # 2. Load Cache if exists
    cache = {}
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                cache = json.load(f)
            print(f"Loaded {len(cache)} cached headers from {CACHE_PATH.name}")
        except Exception:
            cache = {}
            
    # 3. Filter chunks needing generation
    to_process = [c for c in doc_chunks if str(c["chunk_id"]) not in cache]
    print(f"Chunks requiring LLM generation: {len(to_process)}")
    
    sem = asyncio.Semaphore(CONCURRENCY_LIMIT)
    t0 = time.perf_counter()
    
    if to_process:
        async def worker(chunk):
            cid = str(chunk["chunk_id"])
            header = await generate_header_with_retry(chunk, sem)
            cache[cid] = header
            return cid, header

        # Run in batches of 50 to periodically persist cache
        batch_size = 50
        for i in range(0, len(to_process), batch_size):
            batch = to_process[i:i + batch_size]
            tasks = [worker(c) for c in batch]
            await asyncio.gather(*tasks)
            # Save cache checkpoint
            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=2)
            processed_so_far = min(i + batch_size, len(to_process))
            elapsed = time.perf_counter() - t0
            rate = processed_so_far / elapsed if elapsed > 0 else 0.0
            print(f"Progress: {processed_so_far:4d}/{len(to_process)} ({processed_so_far/len(to_process)*100:5.1f}%) | Rate: {rate:4.1f} chunks/sec | Elapsed: {elapsed:5.1f}s")

    t1 = time.perf_counter()
    print(f"\nContext generation completed in {t1 - t0:.2f}s.")
    
    # 4. Assemble Enriched Chunks
    enriched_chunks = []
    for c in all_chunks:
        cid = str(c["chunk_id"])
        c_copy = dict(c)
        if cid in cache:
            c_copy["context_header"] = cache[cid]
            # Attach deterministic AST features as structured metadata
            c_copy["ast_features"] = extract_ast_features(c.get("text", ""))
        enriched_chunks.append(c_copy)
        
    # Write enriched output
    with open(ENRICHED_PATH, "w", encoding="utf-8") as f:
        for c in enriched_chunks:
            f.write(json.dumps(c) + "\n")
    print(f"Wrote {len(enriched_chunks)} enriched chunks to {ENRICHED_PATH}")
    
    # Backup original and swap
    backup_path = CHUNKS_PATH.with_suffix(".jsonl.bak")
    if not backup_path.exists():
        import shutil
        shutil.copyfile(CHUNKS_PATH, backup_path)
        print(f"Created corpus backup at {backup_path.name}")
    
    import shutil
    shutil.copyfile(ENRICHED_PATH, CHUNKS_PATH)
    print(f"Updated primary corpus: {CHUNKS_PATH.name}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

### `tests/test_code_generation_and_verification.py`

*sha256:`827647dc908b` · 332 lines · 14.2 KB (~3,631 tokens) · lang:`python`*

```python
"""Unit and Integration Tests for Code Generation and Verification Engine."""

import pytest
import shutil
from pathlib import Path

from src.system_config import SYSTEM_CONFIG
from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAVariableDeclaration,
    CPSATraceEvent,
    CPSAProtocolRole,
    CPSAStrandInstance,
    CPSAPreskeleton,
    CPSAProtocolSpecification,
)
from src.code_generation.cpsa_scheme_emitter import emit_cpsa_scheme
from src.verification_engine.roletran_executability_gate import verify_role_executability
from src.verification_engine.mitre_build_orchestrator import execute_mitre_make_build


@pytest.fixture
def valid_unilateral_spec() -> CPSAProtocolSpecification:
    """A valid, executable unilateral authentication protocol with channels and inputs/outputs."""
    return CPSAProtocolSpecification(
        protocol_name="unilateral_auth",
        herald_comment="Unilateral Authentication Test Suite",
        roles=[
            CPSAProtocolRole(
                role_name="init",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="send", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="recv", channel="ch", message_term="n"),
                ],
                inputs=["ch", "k"],
                outputs=["n"],
                unique_originating=["n"],
            ),
            CPSAProtocolRole(
                role_name="resp",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="recv", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="send", channel="ch", message_term="n"),
                ],
                inputs=["ch", ["invk", "k"]],
                outputs=["n"],
            ),
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="unilateral_auth",
                variables=[
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                strands=[
                    CPSAStrandInstance(role_name="init", trace_length=2, variable_bindings={"k": "k", "n": "n"}),
                ],
                non_originating=[["invk", "k"]],
                unique_originating=["n"],
                comment="Initiator Point of View",
            ),
        ],
    )


@pytest.fixture
def unexecutable_spec() -> CPSAProtocolSpecification:
    """An unexecutable protocol where the responder tries to send a nonce it cannot decrypt."""
    return CPSAProtocolSpecification(
        protocol_name="broken_protocol",
        roles=[
            CPSAProtocolRole(
                role_name="resp",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="recv", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="send", channel="ch", message_term="n"),
                ],
                inputs=["ch"],  # Missing decryption key (invk k)
                outputs=["n"],
            ),
        ],
    )


def test_scheme_emitter_generates_valid_scm(tmp_path: Path, valid_unilateral_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(valid_unilateral_spec, tmp_path)
    assert scm_path.exists()
    assert scm_path.suffix == ".scm"

    with open(scm_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "(defprotocol unilateral_auth basic" in content
    assert "(defrole init" in content
    assert "(defskeleton unilateral_auth" in content


def test_roletran_gate_accepts_valid_protocol(tmp_path: Path, valid_unilateral_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(valid_unilateral_spec, tmp_path)
    result = verify_role_executability(scm_path)

    assert result.is_executable is True
    assert result.error_diagnostic is None
    assert result.procedural_defproc_code is not None
    assert "(defproc init" in result.procedural_defproc_code


def test_roletran_gate_rejects_unexecutable_protocol(tmp_path: Path, unexecutable_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(unexecutable_spec, tmp_path)
    result = verify_role_executability(scm_path)

    assert result.is_executable is False
    assert result.error_diagnostic is not None
    assert "Received term cannot be fully destructured" in result.error_diagnostic


def test_mitre_build_orchestrator_compiles_artifacts(tmp_path: Path, valid_unilateral_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(valid_unilateral_spec, tmp_path)
    artifacts = execute_mitre_make_build(scm_path, tmp_path)

    assert artifacts.trace_txt_path.exists()
    assert artifacts.shapes_txt_path.exists()
    assert artifacts.full_graph_xhtml_path.exists()
    assert artifacts.shapes_graph_xhtml_path.exists()
    assert artifacts.shapes_count >= 1


def test_compiler_diagnostic_repair_patches_spec(monkeypatch, tmp_path: Path, unexecutable_spec: CPSAProtocolSpecification):
    """Test that repair engine retrieves manual guidance and returns an executable specification."""
    import copy
    from unittest.mock import MagicMock
    from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification

    # Fix the missing decryption key in the role inputs
    repaired = copy.deepcopy(unexecutable_spec)
    repaired.roles[0].inputs.append(["invk", "k"])

    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock(message=MagicMock(content=repaired.model_dump_json()))]
    monkeypatch.setattr("litellm.completion", lambda **kwargs: mock_resp)

    repaired_spec = repair_protocol_specification(
        failing_spec=unexecutable_spec,
        error_diagnostic="Received term cannot be fully destructured: (enc n k)",
        verbatim_slice="Initiator sends {n}_k to responder. Responder decrypts with invk(k).",
        failure_stage="roletran",
        model="mock_model",
    )

    assert ["invk", "k"] in repaired_spec.roles[0].inputs
    scm_path = emit_cpsa_scheme(repaired_spec, tmp_path)
    res = verify_role_executability(scm_path)
    assert res.is_executable is True


def test_cpsa_term_desugaring_and_validation():
    """Verify that foreign operators are desugared and unknown operators are strictly rejected."""
    # 1. Foreign operator desugaring: aenc, senc, sign -> enc; mac, hmac -> hash
    event = CPSATraceEvent(
        direction="send",
        channel="ch",
        message_term=["aenc", ["mac", "secret", "tag"], "pubkey"],
    )
    assert event.message_term == ["enc", ["hash", "secret", "tag"], "pubkey"]

    # 2. Unknown operator rejection
    with pytest.raises(ValueError, match="Unknown operator keyword 'foreign_op'"):
        CPSATraceEvent(
            direction="send",
            channel="ch",
            message_term=["foreign_op", "payload"],
        )


def test_cpsa_operator_arity_enforcement():
    """Verify that operator arities from MITRE CPSA Tables 10.3 and 10.5 are strictly enforced."""
    # (enc) requires at least 2 arguments: payload + key
    with pytest.raises(ValueError, match="Operator 'enc' at 'term' expects at least 2 arguments"):
        from src.intermediate_representation.cpsa_grammar import validate_cpsa_term_syntax
        validate_cpsa_term_syntax(["enc", "payload_only"])

    # (invk) requires exactly 1 argument
    with pytest.raises(ValueError, match="Operator 'invk' at 'term' expects exactly 1 arguments"):
        from src.intermediate_representation.cpsa_grammar import validate_cpsa_term_syntax
        validate_cpsa_term_syntax(["invk", "key1", "key2"])

    # (ltk) requires exactly 2 arguments
    with pytest.raises(ValueError, match="Operator 'ltk' at 'term' expects exactly 2 arguments"):
        from src.intermediate_representation.cpsa_grammar import validate_cpsa_term_syntax
        validate_cpsa_term_syntax(["ltk", "key1"])


def test_basic_algebra_forbids_diffie_hellman_operators():
    """Verify that protocol with 'basic' algebra rejects Diffie-Hellman operators in trace or declarations."""
    # exp operator under basic algebra must fail
    with pytest.raises(ValueError, match="Diffie-Hellman operator 'exp'"):
        CPSAProtocolSpecification(
            protocol_name="dh_in_basic",
            message_algebra="basic",
            roles=[
                CPSAProtocolRole(
                    role_name="client",
                    variables=[
                        CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                        CPSAVariableDeclaration(name="x", sort=CPSASortEnum.DATA),
                    ],
                    trace=[
                        CPSATraceEvent(
                            direction="send",
                            channel="ch",
                            message_term=["exp", "gen", "x"],
                        ),
                    ],
                )
            ],
        )


def test_ensure_three_point_of_view_skeletons():
    """Verify that ensure_three_point_of_view_skeletons guarantees distinct pure POV and secrecy skeletons."""
    from src.semantic_extraction.constrained_protocol_extractor import ensure_three_point_of_view_skeletons

    spec = CPSAProtocolSpecification(
        protocol_name="test_proto",
        roles=[
            CPSAProtocolRole(
                role_name="client",
                variables=[CPSAVariableDeclaration(name="s", sort=CPSASortEnum.DATA)],
                trace=[CPSATraceEvent(direction="send", message_term="s")],
                unique_originating=["s"],
            ),
            CPSAProtocolRole(
                role_name="server",
                variables=[CPSAVariableDeclaration(name="s", sort=CPSASortEnum.DATA)],
                trace=[CPSATraceEvent(direction="recv", message_term="s")],
            ),
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="test_proto",
                strands=[CPSAStrandInstance(role_name="client", variable_bindings={"s": "s"})],
                listeners=["s"],
            )
        ],
    )

    updated = ensure_three_point_of_view_skeletons(spec)
    assert len(updated.skeletons) == 3
    # Skeletons 1 & 2 must be pure POV skeletons without listeners
    assert updated.skeletons[0].strands[0].role_name == "client"
    assert updated.skeletons[0].listeners == []
    assert updated.skeletons[1].strands[0].role_name == "server"
    assert updated.skeletons[1].listeners == []
    # Skeleton 3 must be a secrecy listener skeleton
    assert updated.skeletons[2].listeners == ["s"]

    # Test case 2: LLM specifies primary_secrecy_goals with an arbitrary name not matching any keywords/regex
    spec_semantic = CPSAProtocolSpecification(
        protocol_name="test_proto_semantic",
        primary_secrecy_goals=["arbitrary_token"],
        roles=[
            CPSAProtocolRole(
                role_name="alice",
                variables=[CPSAVariableDeclaration(name="arbitrary_token", sort=CPSASortEnum.DATA)],
                trace=[CPSATraceEvent(direction="send", message_term="arbitrary_token")],
                unique_originating=["arbitrary_token"],
            ),
            CPSAProtocolRole(
                role_name="bob",
                variables=[CPSAVariableDeclaration(name="arbitrary_token", sort=CPSASortEnum.DATA)],
                trace=[CPSATraceEvent(direction="recv", message_term="arbitrary_token")],
            ),
        ],
        skeletons=[],
    )
    updated_semantic = ensure_three_point_of_view_skeletons(spec_semantic)
    assert len(updated_semantic.skeletons) == 3
    assert updated_semantic.skeletons[0].strands[0].role_name == "alice"
    assert updated_semantic.skeletons[0].listeners == []
    assert updated_semantic.skeletons[1].strands[0].role_name == "bob"
    assert updated_semantic.skeletons[1].listeners == []
    assert updated_semantic.skeletons[2].listeners == ["arbitrary_token"]
    assert updated_semantic.skeletons[2].strands[0].role_name == "alice"


def test_nous_portal_llm_kwargs_routing():
    """Verify that nous/ prefixed models are mapped to OpenAI-compatible Nous inference endpoints."""
    from src.system_config import SYSTEM_CONFIG

    kwargs_claude = SYSTEM_CONFIG.get_llm_kwargs("nous/anthropic/claude-3.5-sonnet")
    assert kwargs_claude["model"] == "openai/anthropic/claude-3.5-sonnet"
    assert kwargs_claude["api_base"] == "https://inference-api.nousresearch.com/v1"

    kwargs_deepseek = SYSTEM_CONFIG.get_llm_kwargs("nous/deepseek/deepseek-chat")
    assert kwargs_deepseek["model"] == "openai/deepseek/deepseek-chat"
    assert kwargs_deepseek["api_base"] == "https://inference-api.nousresearch.com/v1"


def test_clean_rag_diagnostic_query_sanitization():
    """Verify that compiler error messages strip local paths, line numbers, and output clean domain queries."""
    from src.verification_engine.compiler_diagnostic_repair import fallback_sanitize_diagnostic_query

    # Test solver unbound identifier error from make output
    make_err = "MITRE build failed for tls_1_2_shapes.xhtml: tls_1_2.scm:72:6: Identifier server_hello_done unknown\nmake: *** [cpsa4.mk:8: tls_1_2.txt] Error 1"
    q1 = fallback_sanitize_diagnostic_query(make_err, "solver")
    assert "tls_1_2" not in q1
    assert "shapes.xhtml" not in q1
    assert ".scm" not in q1

    # Test roletran Cannot build error
    roletran_err = "Cannot build (cat client_random session_id)"
    q2 = fallback_sanitize_diagnostic_query(roletran_err, "roletran")
    assert "Cannot build" in q2
    assert "client_random" not in q2
```

---

### `tests/test_cpsa_scoping_and_prompts.py`

*sha256:`e5bd0e9a7fec` · 160 lines · 6.8 KB (~1,732 tokens) · lang:`python`*

```python
"""Unit Tests for MITRE CPSA 4.4.9 Keyword/Sort Scoping and Externalized .prompts/ Loader."""

from pathlib import Path
import pytest

from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.cpsa_grammar import validate_cpsa_term_syntax
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAPreskeleton,
    CPSAProtocolRole,
    CPSAProtocolSpecification,
    CPSAStrandInstance,
    CPSATraceEvent,
    CPSAVariableDeclaration,
)
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    PROMPT_COMPILER_REPAIR,
    PROMPT_PROTOCOL_EXTRACTION,
    PROMPT_RAG_QUERY_FORMULATION,
    PROMPT_SCHEMA_SELF_CORRECTION,
    PROMPT_SECTION_ROUTER,
    build_schema_system_prompt,
    load_prompt,
)


def test_externalized_prompts_load_from_disk_and_fallback(tmp_path: Path):
    """Verify all 6 prompt templates in .prompts/ exist, load cleanly, and support fallback."""
    for prompt_filename in (
        PROMPT_APPLICABILITY_GATE,
        PROMPT_SECTION_ROUTER,
        PROMPT_PROTOCOL_EXTRACTION,
        PROMPT_SCHEMA_SELF_CORRECTION,
        PROMPT_RAG_QUERY_FORMULATION,
        PROMPT_COMPILER_REPAIR,
    ):
        text = load_prompt(prompt_filename)
        assert len(text) > 100

    # Verify schema attachment helper
    schema_prompt = build_schema_system_prompt(PROMPT_PROTOCOL_EXTRACTION, CPSAProtocolSpecification)
    assert "Respond strictly with a valid JSON object matching this schema:" in schema_prompt
    assert '"CPSAProtocolSpecification"' in schema_prompt

    # Verify fallback when directory has no files
    fallback_text = load_prompt(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert "MITRE CPSA 4.4.9" in fallback_text


def test_logic_only_sorts_forbidden_in_role_and_skeleton_vars():
    """Tables 10.2 & 10.4 vs Table 7.1: strd, indx, and fact are forbidden in role/skeleton vars."""
    for bad_sort in (CPSASortEnum.STRD, CPSASortEnum.INDX, CPSASortEnum.FACT):
        with pytest.raises(ValueError, match="first-order logic sort"):
            CPSAVariableDeclaration(name="node_idx", sort=bad_sort)


def test_diffie_hellman_sorts_forbidden_under_basic_algebra():
    """Table 10.2: rndx, expt, and base sorts are forbidden when protocol message_algebra is 'basic'."""
    with pytest.raises(ValueError, match="Diffie-Hellman variable sort 'rndx'"):
        CPSAProtocolSpecification(
            protocol_name="dh_sort_in_basic",
            message_algebra="basic",
            roles=[
                CPSAProtocolRole(
                    role_name="initiator",
                    variables=[
                        CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                        CPSAVariableDeclaration(name="x", sort=CPSASortEnum.RNDX),
                    ],
                    trace=[
                        CPSATraceEvent(direction="send", channel="ch", message_term="x"),
                    ],
                )
            ],
        )


def test_structural_keywords_forbidden_inside_message_terms():
    """Tables 10.1, 10.3, 10.5: structural keywords (defrole, send, vars, etc.) cannot be term operators."""
    for bad_kw in ("defrole", "defskeleton", "send", "recv", "vars", "trace", "uniq-orig", "deflistener"):
        with pytest.raises(ValueError, match=f"Structural CPSA keyword '{bad_kw}'"):
            validate_cpsa_term_syntax([bad_kw, "x"])


def test_role_and_skeleton_keyword_scoping_separation():
    """Tables 10.1 & 10.6: skeleton keywords cannot appear in defrole and role keywords cannot appear in defskeleton."""
    # 1. Skeleton keyword 'listeners' or 'strands' inside CPSAProtocolRole must fail
    with pytest.raises(ValueError, match="preskeleton-only keyword"):
        CPSAProtocolRole.model_validate({
            "role_name": "client",
            "variables": [{"name": "x", "sort": "text"}],
            "trace": [{"direction": "send", "message_term": "x"}],
            "listeners": ["x"],
        })

    # 2. Role keyword 'trace' or 'inputs' inside CPSAPreskeleton must fail
    with pytest.raises(ValueError, match="role-only keyword"):
        CPSAPreskeleton.model_validate({
            "protocol_name": "proto",
            "strands": [{"role_name": "client"}],
            "trace": [{"direction": "send", "message_term": "x"}],
        })


def test_equation_10_1_forbids_mesg_sort_as_encryption_key():
    """Equation 10.1: variables declared with sort 'mesg' cannot be used as encryption keys in (enc ...)."""
    with pytest.raises(ValueError, match="Equation 10.1"):
        CPSAProtocolRole(
            role_name="sender",
            variables=[
                CPSAVariableDeclaration(name="payload", sort=CPSASortEnum.TEXT),
                CPSAVariableDeclaration(name="generic_key", sort=CPSASortEnum.MESG),
            ],
            trace=[
                CPSATraceEvent(
                    direction="send",
                    channel="ch",
                    message_term=["enc", "payload", "generic_key"],
                )
            ],
        )


def test_stateful_load_stor_event_serialization_and_roletran_invariants():
    """Verify Table 10.1 load/stor 2-arg serialization, 2-arg pubk ordering, and cpsa4roletran input/output sanitization."""
    # 1. load/stor must emit 2 arguments after direction: [load, locn, term]
    load_evt = CPSATraceEvent(direction="load", location="state_cell", message_term="secret_val")
    assert load_evt.to_cpsa_json() == ["load", "state_cell", "secret_val"]

    # 2. Role serialization enforces roletran invariants and 2-arg pubk argument order
    role = CPSAProtocolRole(
        role_name="initiator",
        variables=[
            CPSAVariableDeclaration(name="server_id", sort=CPSASortEnum.NAME),
            CPSAVariableDeclaration(name="fresh_nonce", sort=CPSASortEnum.TEXT),
        ],
        trace=[
            CPSATraceEvent(
                direction="send",
                channel="ch",
                message_term=["enc", "fresh_nonce", ["pubk", "server_id", "enc_tag"]],
            )
        ],
        unique_originating=["fresh_nonce"],
        # Intentionally include fresh_nonce and a compound cat in inputs, and repeat server_id in outputs
        inputs=["server_id", "fresh_nonce", ["cat", "server_id", "fresh_nonce"]],
        outputs=["fresh_nonce", "server_id"],
    )
    role_json = role.to_cpsa_json()
    role_str = str(role_json)

    # Channel 'ch' auto-declared in vars and auto-added to inputs
    assert "['ch', 'chan']" in role_str
    # 2-arg pubk normalized to ['pubk', '"enc_tag"', 'server_id']
    assert "['pubk', '\"enc_tag\"', 'server_id']" in role_str
    # 'fresh_nonce' (uniq-orig) and ['cat', ...] stripped from inputs
    assert "['inputs', 'ch', 'server_id']" in role_str
    # 'server_id' (an input) stripped from outputs, leaving only 'fresh_nonce'
    assert "['outputs', 'fresh_nonce']" in role_str
```

---

### `tests/test_document_ingestion.py`

*sha256:`38caae01f6fb` · 98 lines · 3.3 KB (~844 tokens) · lang:`python`*

```python
"""Unit & Integration Tests for Document Ingestion Subsystem (Stage 1)."""

import pytest
from pathlib import Path

from src.system_config import SYSTEM_CONFIG
from src.document_ingestion.rfc_header_filter import filter_rfc_header
from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections
from src.document_ingestion.handshake_section_router import _heuristic_section_router


@pytest.fixture
def tls_rfc_text() -> str:
    path = SYSTEM_CONFIG.RFCS_DIR / "rfc5246.txt"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


@pytest.fixture
def kerberos_rfc_text() -> str:
    path = SYSTEM_CONFIG.RFCS_DIR / "rfc4120.txt"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


@pytest.fixture
def mib_rfc_text() -> str:
    path = SYSTEM_CONFIG.RFCS_DIR / "rfc2358.txt"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def test_header_filter_accepts_tls(tls_rfc_text: str):
    res = filter_rfc_header(tls_rfc_text)
    assert res.is_eligible is True
    assert res.rfc_id == "RFC 5246"
    assert "Transport Layer Security" in (res.title or "")
    assert res.category == "Standards Track"


def test_header_filter_accepts_kerberos(kerberos_rfc_text: str):
    res = filter_rfc_header(kerberos_rfc_text)
    assert res.is_eligible is True
    assert res.rfc_id == "RFC 4120"
    assert "Kerberos" in (res.title or "")


def test_header_filter_rejects_mib(mib_rfc_text: str):
    res = filter_rfc_header(mib_rfc_text)
    assert res.is_eligible is False
    assert any(term in res.disqualification_reason.lower() for term in ["mib", "managed objects"])


def test_header_filter_rejects_short_stub():
    res = filter_rfc_header("Short administrative stub.\n" * 10)
    assert res.is_eligible is False
    assert "too short" in res.disqualification_reason.lower()


def test_toc_parser_tls5246(tls_rfc_text: str):
    entries = parse_table_of_contents(tls_rfc_text)
    assert len(entries) >= 70
    section_map = {e.section_id: e.title for e in entries}

    assert "7.3" in section_map
    assert "Handshake Protocol Overview" in section_map["7.3"]
    assert "7.4" in section_map
    assert "Handshake Protocol" in section_map["7.4"]


def test_toc_parser_kerberos4120(kerberos_rfc_text: str):
    entries = parse_table_of_contents(kerberos_rfc_text)
    assert len(entries) >= 100
    section_map = {e.section_id: e.title for e in entries}

    assert "3.1" in section_map
    assert "The Authentication Service Exchange" in section_map["3.1"]


def test_verbatim_slicer_tls_handshake(tls_rfc_text: str):
    slice_text = slice_verbatim_sections(tls_rfc_text, ["7.3"])
    lines = slice_text.splitlines()

    # Starts with section header
    assert lines[0].startswith("7.3.  Handshake Protocol Overview")
    # Contains client hello ladder diagram
    assert "ClientHello" in slice_text
    assert "ServerHello" in slice_text
    # Does not contain page break markers
    assert "\x0c" not in slice_text
    assert "[Page 33]" not in slice_text


def test_heuristic_section_router_tls(tls_rfc_text: str):
    entries = parse_table_of_contents(tls_rfc_text)
    selected = _heuristic_section_router(entries)
    assert "7.3" in selected or "7.4" in selected
```

---

### `tests/test_main_pipeline_orchestrator.py`

*sha256:`e585514ba572` · 131 lines · 5.6 KB (~1,441 tokens) · lang:`python`*

```python
"""Integration tests for Main Pipeline Orchestrator."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.system_config import SYSTEM_CONFIG
from src.main_pipeline_orchestrator import run_rfc_translation_pipeline
from src.document_ingestion.protocol_applicability_gate import ProtocolApplicabilityReport
from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAVariableDeclaration,
    CPSATraceEvent,
    CPSAProtocolRole,
    CPSAStrandInstance,
    CPSAPreskeleton,
    CPSAProtocolSpecification,
)


@pytest.fixture
def mock_valid_spec() -> CPSAProtocolSpecification:
    return CPSAProtocolSpecification(
        protocol_name="orch_test_proto",
        herald_comment="Pipeline Orchestrator Verification Spec",
        roles=[
            CPSAProtocolRole(
                role_name="init",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="send", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="recv", channel="ch", message_term="n"),
                ],
                inputs=["ch", "k"],
                outputs=["n"],
                unique_originating=["n"],
            ),
            CPSAProtocolRole(
                role_name="resp",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="recv", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="send", channel="ch", message_term="n"),
                ],
                inputs=["ch", ["invk", "k"]],
                outputs=["n"],
            ),
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="orch_test_proto",
                variables=[
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                strands=[
                    CPSAStrandInstance(role_name="init", trace_length=2, variable_bindings={"k": "k", "n": "n"}),
                ],
                non_originating=[["invk", "k"]],
                unique_originating=["n"],
                comment="Initiator Point of View",
            ),
        ],
    )


def test_pipeline_rejects_ineligible_rfc(tmp_path: Path):
    """Pipeline immediately halts on administrative or MIB documents at Stage 1a."""
    mib_rfc_path = SYSTEM_CONFIG.RFCS_DIR / "rfc2358.txt"
    summary = run_rfc_translation_pipeline(
        rfc_file_path=mib_rfc_path,
        output_dir=tmp_path / "rfc2358_out",
    )
    assert summary.is_eligible is False
    assert summary.build_successful is False
    assert any(k in (summary.error_message or "").lower() for k in ["mib", "managed objects"])


def test_pipeline_e2e_successful_synthesis_and_build(tmp_path: Path, mock_valid_spec: CPSAProtocolSpecification):
    """Pipeline successfully synthesizes and verifies all MITRE shapes when given an eligible RFC."""
    rfc_source = tmp_path / "rfc9999.txt"
    rfc_source.write_text(
        "Network Working Group                                          J. Doe\n"
        "Request for Comments: 9999                                        MITRE\n"
        "Category: Standards Track                                September 2026\n\n\n"
        "                    A Secure Protocol Specification\n\n"
        "Abstract\n\n"
        "   This document specifies an interactive cryptographic protocol.\n\n"
        "Table of Contents\n\n"
        "   1. Introduction .................................................... 2\n"
        "   2. Protocol Handshake ............................................. 3\n\n"
        "1. Introduction\n\n"
        + "   Detailed protocol background and security model.\n" * 40 +
        "\n2. Protocol Handshake\n\n"
        "   Alice sends an encrypted nonce to Bob. Bob decrypts and returns it.\n"
        + "   Additional protocol details.\n" * 40,
        encoding="utf-8",
    )

    mock_app_report = ProtocolApplicabilityReport(
        is_cryptographic_protocol=True,
        protocol_name="orch_test_proto",
        participating_principals=["init", "resp"],
        has_keys_or_nonces=True,
        rationale="Clear cryptographic authentication handshake.",
    )

    with patch("src.main_pipeline_orchestrator.evaluate_protocol_applicability", return_value=mock_app_report), \
         patch("src.main_pipeline_orchestrator.route_handshake_sections", return_value=["2"]), \
         patch("src.main_pipeline_orchestrator.extract_protocol_specification", return_value=mock_valid_spec):

        summary = run_rfc_translation_pipeline(
            rfc_file_path=rfc_source,
            output_dir=tmp_path / "rfc9999_out",
        )

        assert summary.is_eligible is True
        assert summary.roletran_passed is True
        assert summary.build_successful is True
        assert summary.build_artifacts is not None
        assert summary.build_artifacts.shapes_graph_xhtml_path.exists()
        assert summary.build_artifacts.shapes_txt_path.exists()
        assert summary.build_artifacts.shapes_count >= 1
```

---

### `tests/test_visualizer_and_events.py`

*sha256:`9833d4b0fe7a` · 110 lines · 3.7 KB (~952 tokens) · lang:`python`*

```python
"""Unit and integration tests for Pipeline Event Bus, Cycle Detection, and Visualizer Server."""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import MagicMock
from aiohttp import web

from src.pipeline_events import GLOBAL_EVENT_BUS, PipelineEvent
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAVariableDeclaration,
    CPSATraceEvent,
    CPSAProtocolRole,
    CPSAProtocolSpecification,
)
from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification
from src.visualizer.server import VisualizerServer


@pytest.fixture
def sample_spec() -> CPSAProtocolSpecification:
    return CPSAProtocolSpecification(
        protocol_name="cycle_proto",
        roles=[
            CPSAProtocolRole(
                role_name="r",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="x", sort=CPSASortEnum.TEXT),
                ],
                trace=[
                    CPSATraceEvent(direction="send", channel="ch", message_term="x"),
                ],
                inputs=["ch"],
                outputs=["x"],
            )
        ],
    )


def test_pipeline_event_bus_emission_and_subscription():
    """Event bus properly broadcasts events to listeners and maintains history."""
    received_events = []

    def listener(event: PipelineEvent):
        received_events.append(event)

    GLOBAL_EVENT_BUS.subscribe(listener)
    try:
        GLOBAL_EVENT_BUS.emit("stage_started", stage=1, test_key="test_value")

        assert len(received_events) >= 1
        last = received_events[-1]
        assert last.event_type == "stage_started"
        assert last.stage == 1
        assert last.data["test_key"] == "test_value"

        # Verify SSE message formatting
        sse = last.to_sse_message()
        assert "event: stage_started" in sse
        assert '"test_key": "test_value"' in sse
    finally:
        GLOBAL_EVENT_BUS.unsubscribe(listener)


def test_compiler_repair_cycle_detection_triggers_warning_and_jitter(monkeypatch, sample_spec: CPSAProtocolSpecification):
    """When cycle_detected=True, prompt receives oscillation warning and litellm receives higher temperature."""
    captured_kwargs = {}

    def mock_completion(**kwargs):
        captured_kwargs.update(kwargs)
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock(message=MagicMock(content=sample_spec.model_dump_json()))]
        return mock_resp

    monkeypatch.setattr("litellm.completion", mock_completion)

    repaired = repair_protocol_specification(
        failing_spec=sample_spec,
        error_diagnostic="Repeated syntax error",
        verbatim_slice="Sample RFC text",
        failure_stage="roletran",
        model="dummy_model",
        cycle_detected=True,
    )

    assert repaired is not None
    assert captured_kwargs.get("temperature") == 0.4
    prompt_content = captured_kwargs["messages"][1]["content"]
    assert "CRITICAL WARNING: An oscillation/cycle was detected" in prompt_content


def test_visualizer_server_endpoints(tmp_path: Path):
    """Visualizer web server serves history and artifact content."""
    async def _run():
        server = VisualizerServer(host="127.0.0.1", port=8089)

        # Emit test event
        GLOBAL_EVENT_BUS.emit("test_event", stage=4, detail="unit test")

        # Test history endpoint
        req = MagicMock(spec=web.Request)
        resp = await server.handle_history(req)
        assert resp.status == 200
        import json
        history = json.loads(resp.text)
        assert any(e["event_type"] == "test_event" for e in history)

    asyncio.run(_run())
```

---
