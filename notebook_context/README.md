# notebook_context — Agnostic Repository to Markdown Context Bundler

Self-contained, zero-dependency system that packages the RFC-LLM repository
(source code, prompt templates, CLI executables, tests, domain knowledge, and
documentation) into plain-text Markdown bundles under `bundles/`, optimized for
uploading to an LLM Notebook knowledge base.

Contents of this directory:

| Path | Role |
|---|---|
| `bundle_config.json` | Declarative, file-agnostic map of repo -> bundles (the only file you edit) |
| `sync_context.py` | Bundler and SHA-256 state-tracker CLI (Python 3.8+, stdlib only) |
| `manifest_state.json` | Persisted SHA-256 state of the last sync (generated; do not edit) |
| `bundles/*.md` | Generated Markdown bundles for Notebook upload (generated; do not edit) |
| `README.md` | This document |

---

## 1. System Overview & Architecture

The pipeline runs in five stages on every sync:

```
git ls-files (tracked + untracked, .gitignore-honoring)
        |
        v
[1] DISCOVERY ──── global_excludes filter (.git, .venv, __pycache__, .env, output/, all_RFCs/ ...)
        |
        v
[2] CLASSIFICATION
        ├─ binary sniff (NUL byte in first 8 KB)  ─────────────┐
        ├─ size guard (> settings.max_file_size_kb = 600 KB) ──┤──> Tier 4: SUMMARIZED
        ├─ declared summarized_assets patterns ────────────────┘    (metadata + schema preview,
        ├─ bundle include_globs / explicit_files match ──> Tier 1-3: FULL TEXT    never raw bytes)
        └─ unmatched but shebang/executable ──> auto-routed to fallback bundle (02)
        |
        v
[3] STATE & DELTA ── SHA-256 of every discovered file -> manifest_state.json
        |             diff vs previous run -> "Changes Since Last Sync" section
        v             (Added / Modified / Deleted + git branch & commit) prepended
        |             to the master index bundle (00_...)
        v
[4] INTROSPECTION ── stdlib `ast` scan of every bundled .py file: module docstring,
        |             classes, top-level functions, argparse CLI flags
        v             -> "Symbol & Script Registry" table in the master index
        v
[5] MARKDOWN RENDER ─ per bundle: header, TOC with anchors, then every file with
                      relative path, sha256 (12-char), line count, size, and a
                      syntax-tagged code fence. Fences auto-lengthen (````+ )
                      when embedded content itself contains ``` runs, and
                      PDF-to-text control-char garbage (\x0c, \x1a, ...) is sanitized
                      (noted per file). Master index additionally carries the
                      Bundle Catalog, Symbol Registry, and the
                      "Excluded & Heavy Assets Inventory".
```

Key properties:

- **Agnostic**: Nothing is hardcoded about filenames in `sync_context.py`. Every
  inclusion/exclusion rule comes from `bundle_config.json`; globs support `**`
  (any depth), `*` (within a segment), and `?`. New files in covered directories
  are picked up automatically on the next sync.
- **Safe**: Binary content never reaches a bundle. Three independent guards
  (NUL sniff, strict UTF-8 decode, size threshold) route binary or oversized
  files to the summarized inventory instead of corrupting the context window.
- **Stateful**: `manifest_state.json` records each file's SHA-256, size, status
  (`included`/`summarized`), and bundle assignment, plus git branch and commit
  at sync time.

---

## 2. Repository Map & Bundle Breakdown

### Tier 1 — Architecture, Documentation & Project Configs -> `00_ARCHITECTURE_AND_INDEX.md`
- `docs/` — 8 technical documents (`MASTER_BLUEPRINT.md`, `ARCHITECTURE.md`,
  `INTERMEDIATE_REPRESENTATION.md`, `CPSA_KEYWORD_REFERENCE.md`,
  `TIERED_MODEL_ROUTING.md`, `VERIFICATION_AND_SELF_HEALING.md`,
  `QUICKSTART_AND_OPERATIONS.md`, `README.md`)
- Root manifests: `README.md`, `LICENSE`, `requirements.txt`, `pytest.ini`,
  `.env.example`, `.gitignore`, `logs/.gitignore`
- Generated sections: delta changelog, executive grounding guide, bundle
  catalog, AST symbol registry, and heavy-asset inventory.

### Tier 2 — Core Source, Prompts & CLI -> `01_CORE_SOURCE_AND_CLI.md`
- `prompts/` — `01_applicability_gate.md` through
  `07_think_token_synthesizer.md` (with YAML frontmatter `model`, `timeout`,
  `temperature`) and `prompts/README.md`
- `src/` — complete Phase 2 & Phase 3 implementation:
  - `document_ingestion/` (Tier 0 header filter, TOC parser, applicability gate,
    handshake section router, verbatim section slicer)
  - `intermediate_representation/` (CPSA 4.4.9 grammar, algebraic sorts,
    order-sorted Pydantic syntax tree)
  - `semantic_extraction/` (RAG-grounded constrained protocol extractor)
  - `code_generation/` (CPSA JSON serializer, `cpsa4json` Scheme emitter)
  - `verification_engine/` (`Roletran Check` gate, hard-60s MITRE `make`
    orchestrator, SHA-256 cycle-aware RAG diagnostic repair, trajectory and
    `GOLD`/`SILVER`/`BRONZE`/`REJECTED` quality-tier exporter)
  - `generate_think/` (Phase 3 DSPy/deterministic `<think>` synthesizer and
    `sft_train.jsonl` / `dpo_pairs.jsonl` dataset exporter)
  - `visualizer/` (async `aiohttp` SSE/REST server + virtualized `#1..#N` tab
    dashboard HTML supporting offline `--view` replay)
  - Root `src/` modules: `main_pipeline_orchestrator.py`, `pipeline.py`,
    `pipeline_events.py`, `prompt_loader.py`, `rag_retriever_client.py`,
    `logging_config.py`, `system_config.py`
- `rfc-llm` & `rfc-think` — extensionless root CLI launchers, plus
  `refrences/all_RFCs/rfc9528.txt` (benchmark EDHOC input RFC).

### Tier 3 — Operational Scripts, Pipelines & Tests -> `02_RAG_SCRIPTS_AND_TESTS.md`
- `refrences/scripts/` — numbered RAG corpus pipeline (`01_extract_chunks.py`
  through `05_enrich_doc_chunks.py`)
- `refrences/run_rag_pipeline.sh` — shell pipeline runner
- `refrences/reports/` — `evaluate_rag.py` (300-query retrieval benchmark),
  `plot_clusters.py`, `rag_evaluation_report.tex`
- `tests/` — `conftest.py` and 8 pytest modules (`test_document_ingestion.py`,
  `test_cpsa_scoping_and_prompts.py`,
  `test_code_generation_and_verification.py`,
  `test_main_pipeline_orchestrator.py`,
  `test_trajectory_and_hardening.py`,
  `test_visualizer_and_events.py`,
  `test_visualizer_tabs.py`, `test_generate_think.py`).

### Tier 1/3 — Domain Knowledge -> `03_CPSA_DOMAIN_KNOWLEDGE_AND_GUIDES.md`
- `refrences/cpsa-protocol-modeling/` — `SKILL.md`, curated `references/`
  (grammar, declarations, goals, state, termination, roletran diagnostics),
  templates, `pdf_manual` transcription, and official MITRE manuals
  (`CPSA4_User_Manual.md`, `CPSA_Comprehensive_Guide.md`,
  `CPSA_Specification.md`) under the 600 KB file size threshold.
- `refrences/internet/guides_markdown/` — CPSA guides and theoretical papers.

### Tier 3 — Reference Corpus -> `04_CPSA_SCM_EXAMPLES_CORPUS.md`
- `refrences/internet/examples_scm/` — 148 official MITRE CPSA `.scm` protocol
  specifications used for few-shot grounding and grammar verification.

### Tier 4 — Heavy / Binary / Generated Assets (Summarized, Never Dumped)
`refrences/chunks/` (`embeddings.npy`, `manual_chunks.jsonl`,
`all_references_clean.md`, `embeddings_meta.json`), PDFs under `papers_pdf/` and
`manual/`, PNG benchmark figures, `embedding_clusters.html`, benchmark
JSON/JSONL files, and `logs/pipeline_runs.csv`. Each appears in the **Excluded &
Heavy Assets Inventory** with size, line/record counts, and a schema preview.

---

## 3. Agnostic Evolution Guide

### Changes Requiring No Config Edit
- **New Python module under `src/`** -> auto-included in bundle `01` (`src/**/*.py`).
- **New prompt template under `prompts/`** -> auto-included in bundle `01` (`prompts/**/*.md`).
- **New test under `tests/`** -> auto-included in bundle `02` (`tests/**/*.py`).
- **New `.scm` example** -> auto-included in bundle `04`.
- **New doc under `docs/`** -> auto-included in bundle `00` (`docs/**/*.md`).
- **New extensionless executable or shebang script** -> auto-detected and routed
  to the fallback Tier-3 bundle (`02`) if not listed in `explicit_files`.

### Changes Requiring a `bundle_config.json` Edit
- **New top-level directory** with source code: add a glob to an existing
  bundle's `include_globs` or create a new bundle entry.
- **Adjust size threshold**: edit `settings.max_file_size_kb` (currently `600`).
- **Exclude or summarize new artifacts**: add patterns to `global_excludes`
  (hard exclusion) or `summarized_assets.patterns` (inventoried with preview).

After editing `bundle_config.json`, run
`python3 notebook_context/sync_context.py --rebuild` to reset the delta baseline.

---

## 4. Operational Workflow

```bash
# Full sync (normal use) — regenerates all bundles + state, prints report
python3 notebook_context/sync_context.py

# Dry run — show drift since last sync (exit 0 = in sync, 1 = drift)
python3 notebook_context/sync_context.py --check

# Force full regeneration and reset delta baseline (after config edits)
python3 notebook_context/sync_context.py --rebuild

# Auto-sync bundles after every git commit (installs .git/hooks/post-commit)
python3 notebook_context/sync_context.py --install-hook
```

Hygiene guarantees:
- `notebook_context/**` is listed in `global_excludes`, preventing recursive
  self-bundling.
- `.env`, `output/**`, `all_RFCs/**`, caches, and `.venv/**` are hard-excluded
  so secrets and runtime artifacts never leak into generated bundles (while
  `.env.example` is explicitly included in `00_ARCHITECTURE_AND_INDEX.md`).
