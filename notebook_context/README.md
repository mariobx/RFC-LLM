# notebook_context — Agnostic Repository → Markdown Context Bundler

Self-contained, zero-dependency system that packages the RFC-LLM repository
(source code, CLI executables, tests, domain knowledge, documentation) into
clean plain-text Markdown bundles under `bundles/`, optimized for uploading to
an LLM Notebook knowledge base.

Contents of this directory:

| Path | Role |
|---|---|
| `bundle_config.json` | Declarative, file-agnostic map of repo → bundles (the only file you edit) |
| `sync_context.py` | The bundler / state-tracker CLI (Python 3.8+, stdlib only) |
| `manifest_state.json` | Persisted SHA-256 state of the last sync (generated; do not edit) |
| `bundles/*.md` | Generated Markdown bundles for Notebook upload (generated; do not edit) |
| `README.md` | This document |

---

## 1. System Overview & Architecture

The pipeline runs in five stages on every sync:

```
git ls-files (tracked + untracked, .gitignore-honoring)
        │
        ▼
[1] DISCOVERY ──── global_excludes filter (.git, .venv, __pycache__, .env, output/, logs …)
        │
        ▼
[2] CLASSIFICATION
        ├─ binary sniff (NUL byte in first 8 KB)  ─────────────┐
        ├─ size guard (> settings.max_file_size_kb = 100 KB) ──┤──► Tier 4: SUMMARIZED
        ├─ declared summarized_assets patterns ────────────────┘    (metadata + schema preview,
        ├─ bundle include_globs / explicit_files match ──► Tier 1–3: FULL TEXT    never raw bytes)
        └─ unmatched but shebang/executable ──► auto-routed to fallback bundle (02)
        │
        ▼
[3] STATE & DELTA ── SHA-256 of every discovered file → manifest_state.json
        │             diff vs previous run → "Changes Since Last Sync" section
        ▼             (Added / Modified / Deleted + git branch & commit) prepended
        │             to the master index bundle (00_…)
        ▼
[4] INTROSPECTION ── stdlib `ast` scan of every bundled .py file: module docstring,
        │             classes, top-level functions, argparse CLI flags
        ▼             → "Symbol & Script Registry" table in the master index
        ▼
[5] MARKDOWN RENDER ─ per bundle: header, TOC with anchors, then every file with
                      relative path, sha256 (12-char), line count, size, and a
                      syntax-tagged code fence. Fences auto-lengthen (```` ````+ ````)
                      when embedded content itself contains ``` runs, and
                      PDF-to-text control-char garbage (\x0c, \x1a, …) is sanitized
                      (noted per file). Master index additionally carries the
                      Bundle Catalog, Symbol Registry, and the
                      "Excluded & Heavy Assets Inventory".
```

Key properties:

- **Agnostic**: nothing is hardcoded about filenames. `sync_context.py` reads
  every rule from `bundle_config.json`; globs use `**` (any depth), `*`
  (within a segment), `?`. New files in covered directories are picked up
  automatically on the next sync.
- **Safe**: binary content can never reach a bundle. Three independent guards
  (NUL sniff, strict UTF-8 decode, size threshold) route offenders to the
  summarized inventory instead of failing or corrupting the context window.
- **Stateful**: `manifest_state.json` records each file's SHA-256, size,
  status (`included`/`summarized`) and bundle assignment, plus git branch /
  commit at sync time. The delta engine gives the Notebook LLM an explicit
  changelog of what moved between syncs.

## 2. Repository Map & Bundle Breakdown

Reconnaissance (Phase 1 audit) found **283 git-visible files** in these
functional zones, classified into four tiers:

### Tier 1 — Architecture, Documentation & Project Configs → `00_ARCHITECTURE_AND_INDEX.md`
- `docs/` — 8 architecture/spec documents (MASTER_BLUEPRINT, ARCHITECTURE,
  INTERMEDIATE_REPRESENTATION, CPSA_KEYWORD_REFERENCE, TIERED_MODEL_ROUTING,
  VERIFICATION_AND_SELF_HEALING, QUICKSTART_AND_OPERATIONS, index)
- Root manifests: `README.md`, `LICENSE`, `requirements.txt`, `pytest.ini`,
  `.gitignore`, `logs/.gitignore`
- Plus generated sections: delta changelog, bundle catalog, AST symbol
  registry, heavy-asset inventory.

### Tier 2 — Core Source & CLI → `01_CORE_SOURCE_AND_CLI.md`
- `src/` — 23 files: `document_ingestion/` (RFC header filter, TOC parser,
  section slicer, applicability gate, handshake router),
  `intermediate_representation/` (CPSA 4.4.9 grammar, algebraic sorts,
  protocol syntax tree), `semantic_extraction/` (RAG-grounded constrained
  extractor), `code_generation/` (CPSA JSON serializer, Scheme emitter),
  `verification_engine/` (roletran gate, MITRE make orchestrator, compiler
  diagnostic self-heal), `visualizer/` (async web server + dashboard HTML),
  `main_pipeline_orchestrator.py`, `pipeline.py` (argparse CLI),
  `pipeline_events.py`, `logging_config.py`, `system_config.py`
- `rfc-llm` — extensionless root CLI launcher (bash, detected via explicit
  file rule + shebang auto-detection).

### Tier 3 — Operational Scripts, Pipelines & Tests → `02_RAG_SCRIPTS_AND_TESTS.md`
- `refrences/scripts/` — numbered RAG pipeline (`01_extract_chunks.py` …
  `05_enrich_doc_chunks.py`)
- `refrences/run_rag_pipeline.sh` — shell pipeline runner
- `refrences/reports/` — `evaluate_rag.py` (retrieval benchmark harness),
  `plot_clusters.py`, `rag_evaluation_report.tex` (LaTeX source)
- `tests/` — 4 pytest modules (ingestion, codegen/verification, orchestrator,
  visualizer/events)

### Tier 1/3 — Domain knowledge → `03_CPSA_DOMAIN_KNOWLEDGE_AND_GUIDES.md`
- `refrences/cpsa-protocol-modeling/` — SKILL.md, curated `references/`
  (grammar, declarations, goals, state, termination, roletran diagnostics),
  templates, pdf_manual transcription, and complete official MITRE User Manual and Specification (`CPSA4_User_Manual.md`, `CPSA_Comprehensive_Guide.md`, `CPSA_Specification.md`) under the upgraded 600 KB file limit.
- `refrences/internet/guides_markdown/` — CPSA guides and Guttman/Ramsdell
  theoretical foundation papers.

### Tier 3 — Reference corpus → `04_CPSA_SCM_EXAMPLES_CORPUS.md`
- `refrences/internet/examples_scm/` — all 148 official MITRE CPSA `.scm`
  protocol examples (few-shot grounding corpus).

### Tier 4 — Heavy / binary / generated (summarized, never dumped)
44 assets ≈ 20 MB: `refrences/chunks/` (embeddings.npy 4.2 MB,
manual_chunks.jsonl 2.4 MB, all_references_clean.md 1.3 MB, …), 17 PDFs under
`papers_pdf/` + `manual/`, 10 PNG figures, `embedding_clusters.html` (1.6 MB
rendered artifact), raw text duplicate manuals, benchmark JSON/JSONL, and
`logs/pipeline_runs.csv`. Each appears in the
**Excluded & Heavy Assets Inventory** with size, line/record counts and a
schema preview (CSV header + sample rows, JSON/JSONL keys, NPY shape/dtype,
heading outlines).

### Why these split points?
Bundle sizes target the sweet spot for Gemini / NotebookLM ingestion:
- Splitting code (`01`), test harnesses (`02`), CPSA formal semantics (`03`), and `.scm` examples (`04`) allows modular uploads into NotebookLM sources or a unified single-prompt upload into Google AI Studio / Gemini Advanced.

## 3. Agnostic Evolution Guide

### Things that need NO config edit
- **New Python module anywhere under `src/`** → auto-included in bundle 01
  (`src/**/*.py`).
- **New test under `tests/`** → bundle 02 (`tests/**/*.py`).
- **New `.scm` example** → bundle 04.
- **New doc under `docs/`** → bundle 00 (`docs/**/*.md`).
- **New extensionless executable or shebang script anywhere** (e.g. a future
  root-level `rfc-llm-eval` launcher): shebang + exec-bit auto-detection
  routes it to the fallback Tier-3 bundle (02) and logs it under
  "Auto-Detected Executables" in the index. No JSON edit required.
- **New huge/binary artifact under a summarized pattern** (e.g. another PDF in
  `refrences/internet/papers_pdf/`) → auto-summarized.
- Any file over `max_file_size_kb` or failing UTF-8 decode is auto-demoted to
  the inventory regardless of which glob claimed it.

### Things that DO need a config edit
- **New top-level directory** with source code (e.g. `tools/`): add a glob to
  an existing bundle's `include_globs` (e.g. `"tools/**/*.py"` in bundle 02),
  or create a new bundle object.
- **New bundle group**: append an object to `bundles` with `name`, `title`,
  `description`, `tier`, `include_globs`, `explicit_files`. First-match wins —
  order bundles so more specific rules come first. Exactly one bundle should
  keep `"is_master_index": true`.
- **Change the size threshold**: `settings.max_file_size_kb` (currently 100).
  Raising it pulls oversized manuals/guides into full text; lowering it pushes
  more into summaries.
- **Exclude something new**: add a glob to `global_excludes` (hard exclusion,
  invisible to the Notebook) or to `summarized_assets.patterns` (soft
  exclusion — still inventoried with metadata).
- **Summarize despite matching a bundle**: `summarized_assets.patterns` wins
  over bundle globs.

After any config edit run `python3 notebook_context/sync_context.py --rebuild`
so the delta baseline reflects the new rules cleanly.

## 4. Operational Workflow

```bash
# Full sync (normal use) — regenerates all bundles + state, prints report
python3 notebook_context/sync_context.py

# Dry run — what changed since the last sync? (exit 0 = in sync, 1 = drift)
python3 notebook_context/sync_context.py --check

# Force full regeneration and reset the delta baseline (after config edits)
python3 notebook_context/sync_context.py --rebuild

# Auto-sync bundles after every git commit (installs .git/hooks/post-commit)
python3 notebook_context/sync_context.py --install-hook
#   remove again with:  rm .git/hooks/post-commit
```

Checking drift between two commits: commit A → `sync_context.py`, later at
commit B → `sync_context.py --check` lists exactly which files were
added/modified/deleted between the two sync points (hash-based, not
mtime-based).

Uploading to the Notebook:

1. Run a sync (or let the post-commit hook do it).
2. Upload every file in `notebook_context/bundles/` as Notebook sources:
   - `00_ARCHITECTURE_AND_INDEX.md` — always upload first; it is the map
     (changelog, symbol registry, heavy-asset inventory).
   - `01`–`04` — upload all, or selectively refresh only the bundles whose
     files appear in the delta changelog.
3. Re-upload only bundles whose content changed (compare the "Changes Since
   Last Sync" section in `00_…`, or `git diff --stat notebook_context/bundles/`
   if you commit them).

Hygiene notes:

- `notebook_context/**` is in `global_excludes`, so generated bundles never
  bundle themselves (no recursion).
- `.env` files, `output/`, `all_RFCs/`, caches and `.venv/` are hard-excluded —
  secrets and runtime artifacts can never leak into a bundle.
- Bundles are deterministic given the same repo state, so committing them is
  safe and diffs stay reviewable (only the generated-at timestamp and delta
  section churn on no-op syncs).
