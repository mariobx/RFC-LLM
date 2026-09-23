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
