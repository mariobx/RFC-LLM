# RFC-LLM Pipeline Architecture & Lifecycle

## 1. System Overview

RFC-LLM translates raw, unstructured IETF RFC documents into formally verified MITRE CPSA 4.4.9 models (`.scm`), programmatic verification trajectories (`<protocol>_trajectory.json`), and Phase 3 `<think>` reasoning datasets (`<protocol>_think.json`, `sft_train.jsonl`, `dpo_pairs.jsonl`).

RFC specifications combine English prose, ASCII sequence diagrams, and byte-level packet layouts, whereas CPSA requires order-sorted algebraic S-expressions under strict Dolev-Yao strand space semantics. Passing an RFC straight to an LLM produces hallucinated operators, invalid sort assignments, and uncompilable Scheme code.

RFC-LLM decomposes translation into six discrete compiler stages in `./rfc-llm` ([`src/main_pipeline_orchestrator.py`](../src/main_pipeline_orchestrator.py)) followed by Phase 3 hindsight reasoning synthesis in `./rfc-think` ([`src/generate_think/`](../src/generate_think/)):

```
[RFC Text]
   |
   v
[Stage 1: Document Intake] ──────── (Tier 0 Regex Filter -> TOC -> Gatekeeper -> Section Router -> Verbatim Slicer)
   |
   v
[Stage 2: JSON CPSA Generation] ─── (prompts/03_protocol_extraction.md + Hybrid RAG -> Scoped Pydantic AST)
   |
   v
[Stage 3: CPSA4json -> scm] ─────── (JSON AST -> Native CPSA JSON -> ~/.cabal/bin/cpsa4json -> <protocol>.scm)
   |
   v
[Stage 4: Roletran Check] ───────── (cpsa4roletran for Basic / cpsa4 -l 1 for Diffie-Hellman; 15s Timeout)
   |           |
   | (Pass)    | (Fail)
   |           v
   |     [Stage 5: Self-Healing Loop] ─── (SHA-256 Cycle Check + RAG Query [15s] + AST Repair [180s]; Max 50)
   |           |                                 ^
   |           +────────> (Re-emit Stage 3)      | (Build / 60s Timeout Error)
   v                                             |
[Stage 6: CPSA Compilation] ─────── (Hard 60s Process-Group SIGKILL Cap: make + cpsa4 + cpsa4shapes + cpsa4graph)
   |
   v
[Trajectory & Quality Tier Export] ── (<protocol>.scm Header + <protocol>_trajectory.json + metadata_index.json)
   |
   v
[Phase 3: ./rfc-think Synthesizer] ── (prompts/07_think_token_synthesizer.md -> <protocol>_think.json + SFT/DPO JSONL)
```

---

## 2. Phase 2 Synthesis Pipeline Stages (`./rfc-llm`)

### Stage 1: Document Intake
1. **Stage 1a — Tier 0 Header & Frontmatter Filter** ([`src/document_ingestion/rfc_header_filter.py`](../src/document_ingestion/rfc_header_filter.py)):
   - Inspects the first 100 lines of the RFC using deterministic regular expressions (<1 ms, zero LLM calls).
   - Rejects documents under 60 lines, `Historic` or `Best Current Practice` categories, and administrative/data-definition titles (`MIB`, `Management Information Base`, `Managed Objects`, `Architecture`, `Applicability Statement`, `Problem Statement`, `Requirements for`, `Guidelines for`, `Meeting Minutes`).
2. **Stage 1b — Table of Contents Parser** ([`src/document_ingestion/rfc_toc_parser.py`](../src/document_ingestion/rfc_toc_parser.py)):
   - Parses hierarchical dotted section identifiers (`5.2`, `A.1`), titles, page numbers, and indentation levels from the TOC block, falling back to column-0 header scanning if no formal TOC exists.
3. **Stage 1c — Protocol Applicability Gate** ([`src/document_ingestion/protocol_applicability_gate.py`](../src/document_ingestion/protocol_applicability_gate.py)):
   - Configured via [`prompts/01_applicability_gate.md`](../prompts/01_applicability_gate.md) (`timeout: 180`).
   - Evaluates RFC metadata, abstract, and TOC to confirm the document defines an interactive cryptographic protocol with principals, keys, or nonces.
   - **Deferred Directory Creation**: Ineligible RFCs rejected at Stage 1a or Stage 1c are recorded in `metadata_index.json` (`filtered_rfcs`) and `logs/pipeline_runs.csv` without creating empty per-RFC directories or allocating visualizer tabs.
4. **Stage 1d — Handshake Section Router** ([`src/document_ingestion/handshake_section_router.py`](../src/document_ingestion/handshake_section_router.py)):
   - Configured via [`prompts/02_section_router.md`](../prompts/02_section_router.md) (`timeout: 180`).
   - Selects the exact section numbers defining the cryptographic message exchange (excluding introductory prose, security considerations, and IANA registries).
5. **Stage 1e — Verbatim Section Slicer** ([`src/document_ingestion/verbatim_section_slicer.py`](../src/document_ingestion/verbatim_section_slicer.py)):
   - Extracts the selected sections verbatim (typically 200-600 lines out of 10,000+ lines), strips form feeds (`\x0c`) and page headers/footers, and writes `<rfc_dir>/verbatim_slice.txt`.

### Stage 2: JSON CPSA Generation
- **Files**: [`src/semantic_extraction/constrained_protocol_extractor.py`](../src/semantic_extraction/constrained_protocol_extractor.py), [`src/intermediate_representation/protocol_syntax_tree.py`](../src/intermediate_representation/protocol_syntax_tree.py)
- **Prompts**: [`prompts/03_protocol_extraction.md`](../prompts/03_protocol_extraction.md) (initial extraction, `timeout: 180`), [`prompts/04_schema_self_correction.md`](../prompts/04_schema_self_correction.md) (1-shot retry, `timeout: 180`).
- **Input**: `verbatim_slice.txt` + top-2 hybrid RAG reference chunks + mandatory `CPSAProtocolSpecification` JSON schema.
- **Core Constraints**:
  - Order-sorted variables (`name`, `text`, `data`, `skey`, `akey`, `chan`, `locn`, `tag`, `mesg`, plus `rndx`, `expt`, `base` under `diffie-hellman`). Logic sorts (`strd`, `indx`, `fact`) are forbidden in `(vars ...)`.
  - Strict atom terms (`term ::= id | integer | [op, ...args]`), Equation 10.1 enforcement (`mesg` forbidden as encryption key in `enc`), and positional keyword scoping between roles and preskeletons.
  - **1-Shot Schema Self-Correction**: If Pydantic validation fails, the exact `ValidationError` is injected into `{validation_error}` in `04_schema_self_correction.md` for an immediate correction turn.
  - **3-POV Preskeleton Enforcement**: `ensure_three_point_of_view_skeletons()` guarantees pure participant POV skeletons (`listeners: []`) alongside a separate secrecy `deflistener` skeleton.

### Stage 3: CPSA4json -> scm
- **Files**: [`src/code_generation/cpsa_json_serializer.py`](../src/code_generation/cpsa_json_serializer.py), [`src/code_generation/cpsa_scheme_emitter.py`](../src/code_generation/cpsa_scheme_emitter.py)
- **Process**:
  1. Serializes `CPSAProtocolSpecification` into native CPSA JSON S-expression arrays (automatically injecting `["algebra", "diffie-hellman"]` into the `herald` form when `message_algebra == "diffie-hellman"`).
  2. Pipes the serialized JSON forms into `~/.cabal/bin/cpsa4json` via `stdin`.
  3. Writes canonical MITRE CPSA 4.4.9 Scheme S-expressions to `<rfc_dir>/<protocol>.scm`.

### Stage 4: Roletran Check
- **File**: [`src/verification_engine/roletran_executability_gate.py`](../src/verification_engine/roletran_executability_gate.py)
- **Timeout**: `ROLETRAN_TIMEOUT_SECONDS = 15` ([`src/system_config.py`](../src/system_config.py)).
- **Dual Pre-Flight Path**:
  - **Basic Algebra**: Runs `~/.cabal/bin/cpsa4roletran` to prove static constructibility of sent terms, destructibility of received terms, and procedural `defproc` compilation.
  - **Diffie-Hellman Algebra**: Because `cpsa4roletran` only supports `basic` algebra, Diffie-Hellman models run `~/.cabal/bin/cpsa4 -l 1 <protocol>.scm` to validate syntax, sorts, role well-formedness, and `(uniq-gen ...)` exponent scoping in milliseconds before full search.

### Stage 5: Self-Healing Loop
- **Files**: [`src/verification_engine/compiler_diagnostic_repair.py`](../src/verification_engine/compiler_diagnostic_repair.py), [`src/rag_retriever_client.py`](../src/rag_retriever_client.py), [`src/prompt_loader.py`](../src/prompt_loader.py)
- **Prompts**: [`prompts/05_rag_query_formulation.md`](../prompts/05_rag_query_formulation.md) (`timeout: 15`), [`prompts/06_compiler_repair.md`](../prompts/06_compiler_repair.md) (`timeout: 180`).
- **Iteration Budget**: `MAX_REPAIR_ATTEMPTS = 50` per verification loop (Stage 4 Roletran loop and Stage 6 CPSA Compilation loop).
- **Mechanism**:
  1. **SHA-256 Cycle Detection**: Hashes `protocol_ast.model_dump_json()` via `hashlib.sha256`. Repeating a previously seen AST sets `cycle_detected = True`, appends an explicit anti-oscillation directive, and raises sampling temperature to at least `0.4`.
  2. **Conceptual RAG Query Formulation**: Strips concrete protocol variable names, line numbers, and file paths into a 3-6 word CPSA concept query (`15s` timeout, with deterministic regex fallback if offline).
  3. **Hybrid Manual Retrieval**: Queries `refrences/chunks/manual_chunks.jsonl` via `CPSASemanticRetriever` (BM25 + `ollama/nomic-embed-text` dense embeddings + RRF) for top-2 authoritative MITRE manual excerpts.
  4. **AST Repair & Re-Emission**: Produces a corrected `CPSAProtocolSpecification`, re-enforces 3-POV skeleton separation, and re-emits `.scm` through Stage 3.

### Stage 6: CPSA Compilation & Trajectory Export
- **Files**: [`src/verification_engine/mitre_build_orchestrator.py`](../src/verification_engine/mitre_build_orchestrator.py), [`src/verification_engine/trajectory_metadata_exporter.py`](../src/verification_engine/trajectory_metadata_exporter.py)
- **Hard 60-Second Compilation Cap (`CPSA_TIMEOUT_SECONDS = 60`)**:
  1. Initializes `Makefile` and `cpsa4.mk` in `<rfc_dir>` via `~/.cabal/bin/cpsa4init`.
  2. Executes `make -B <stem>_shapes.xhtml` (`cpsa4` -> `cpsa4shapes` -> `cpsa4graph`) inside a dedicated process session (`start_new_session=True`). If strand search exceeds `60` seconds, `_run_make_with_hard_timeout` terminates the entire process group via `os.killpg(..., signal.SIGKILL)` and raises `CPSABuildError` so the Stage 5/6 self-healing loop can repair the state-space explosion.
  3. Renders the full derivation search graph (`make <stem>.xhtml`) within any remaining time of the 60-second budget.
- **Deterministic Quality Tiers & Trajectory Bundle**:
  - `trajectory_metadata_exporter.py` parses `<stem>.txt` and `<stem>_shapes.txt` to assign a deterministic quality tier:
    - **`GOLD`**: Solver passed, all participant POV skeletons realized multi-strand authenticated shapes (`max_strands >= 2`), and all secrecy `deflistener` skeletons remained unrealized (`realized_shapes_count == 0`).
    - **`SILVER`**: Solver passed and all participant POV skeletons realized shapes (`realized_shapes_count > 0`), with single-strand realization or non-empty listener shapes.
    - **`BRONZE`**: Solver passed, but one or more participant POV skeletons failed to realize (`DEAD_HANDSHAKE`).
    - **`REJECTED`**: Solver failed or produced zero preskeleton outcomes.
  - Prepends structured MoE conditioning comment headers (`;;; [RFC-ID: ...]`, `;;; [QUALITY-TIER: ...]`) to `<protocol>.scm`, writes `<protocol>_trajectory.json`, and updates `metadata_index.json`.

---

## 3. Phase 3: Hindsight Reasoning Synthesizer (`./rfc-think`)

- **Files**: [`src/generate_think/cli.py`](../src/generate_think/cli.py), [`src/generate_think/dspy_think_synthesizer.py`](../src/generate_think/dspy_think_synthesizer.py), [`src/generate_think/think_schema.py`](../src/generate_think/think_schema.py)
- **Prompt**: [`prompts/07_think_token_synthesizer.md`](../prompts/07_think_token_synthesizer.md) (`timeout: 180`, `temperature: 0.2`).
- **Process**:
  1. Accepts a timestamped run directory (`output/run_YYYY-MM-DD_HH-MM-SS`), `metadata_index.json`, RFC folder, or single `<protocol>_trajectory.json` and filters protocols by `--min-tier` (default: `BRONZE`).
  2. Synthesizes structured 5-step forward-looking deduction traces (`step1_protocol_and_algebra` through `step5_preskeleton_verdicts_and_goals` + `full_thinking_monologue`) in `auto` (DSPy/LLM with deterministic fallback), `llm`, or zero-LLM `deterministic` mode.
  3. Weaves any Stage 4/5/6 compiler diagnostics into `step4_compiler_backtracking_and_invariants` as natural first-person self-checks without leaking post-hoc references to `final_ast` or `final_scm`.
  4. Writes `<protocol>_think.json` (`ThinkArtifactBundle`) inside each RFC directory and exports consolidated `sft_train.jsonl` and compiler-rejected contrastive `dpo_pairs.jsonl` at the root of the run directory.

---

## 4. Timestamped Run Directory Structure

Every `./rfc-llm` invocation writes artifacts under an isolated timestamped run folder `output/run_YYYY-MM-DD_HH-MM-SS/`:

```
output/run_YYYY-MM-DD_HH-MM-SS/
├── metadata_index.json               # Master run manifest (accepted tab runs[] + filtered_rfcs[])
├── sft_train.jsonl                   # Consolidated Phase 3 SFT chat dataset (written by ./rfc-think)
├── dpo_pairs.jsonl                   # Consolidated Phase 3 contrastive DPO pairs (written by ./rfc-think)
└── rfc9528/                          # Created ONLY for eligible RFCs passing Stage 1a & 1c
    ├── verbatim_slice.txt            # Sliced RFC handshake specification text
    ├── events.jsonl                  # Compact per-RFC telemetry stream for O(1)-RAM visualizer hydration
    ├── run.log                       # Per-RFC execution log
    ├── Makefile & cpsa4.mk           # Initialized by cpsa4init
    ├── edhoc.scm                     # Final verified CPSA model with ;;; [QUALITY-TIER: ...] header
    ├── edhoc.txt                     # Raw cpsa4 strand-space derivation tree
    ├── edhoc_shapes.txt              # Distilled minimal realized shapes from cpsa4shapes
    ├── edhoc_shapes.xhtml            # Interactive SVG graph of realized shapes from cpsa4graph
    ├── edhoc.xhtml                   # Interactive SVG graph of full derivation tree
    ├── edhoc_trajectory.json         # Complete AST, Stage 5/6 repair history, & formal quality assessment
    └── edhoc_think.json              # Phase 3 5-step <think> trace, SFT messages, & DPO pairs (./rfc-think)
```

---

## 5. Bounded Event Bus & Multi-RFC Virtualized Web Visualizer

### Bounded `O(1)`-RAM Event Bus ([`src/pipeline_events.py`](../src/pipeline_events.py))
- Thread-safe singleton `GLOBAL_EVENT_BUS` (`PipelineEventBus`).
- **Bounded Active Buffer**: Keeps **only** the currently executing RFC's events in RAM (`_active_events`), flushing slimmed event records (large AST blobs stripped because full snapshots reside in `<protocol>_trajectory.json`) directly to `<rfc_dir>/events.jsonl` on disk.
- **Sequential Tab & Filtered Registries**:
  - `register_accepted_tab()`: Allocates sequential 1-based tab numbers (`#1..#N`) exclusively for RFCs passing intake gates (~150 bytes per summary entry, <1 MB RAM for 5,000+ RFCs).
  - `register_filtered_rfc()`: Records Tier 0 and Stage 1c disqualifications in a compact list without allocating numbered tabs.
  - `load_run_from_disk()`: Reconstructs the tab bar and filtered registry from `metadata_index.json` (or legacy run folders) for offline `--view` replay.

### Live & Offline Web Visualizer ([`src/visualizer/server.py`](../src/visualizer/server.py), [`src/visualizer/static/index.html`](../src/visualizer/static/index.html))
- Asynchronous `aiohttp` server running on `http://127.0.0.1:8080` (auto-increments if port 8080 is busy) during live runs or via `./rfc-llm --view output/run_<timestamp>`.
- **UI Capabilities**:
  - **Virtualized `#1..#N` Tab Bar**: Renders only visible tab buttons inside the horizontal scroll viewport (`O(1)` browser DOM nodes across 5,000+ tabs), displaying tab `#`, RFC ID, quality tier badge, and protocol name, plus live search and status filtering (`ALL`, `VERIFIED`, `PARTIAL`, `FAILED`).
  - **Collapsible `Filtered / Skipped` Drawer**: Paginated (`100` entries/page) and searchable table inspecting Tier 0 and Stage 1c rejected RFCs and disqualification rationales.
  - **6-Stage Horizontal Stepper**: Tracks live timing, active model slugs, and status across `01 Document Intake`, `02 JSON CPSA Generation`, `03 CPSA4JSON -> .scm`, `04 Roletran Check`, `05 Self-Healing Loop`, and `06 CPSA Compilation`.
  - **Per-Attempt Time-Travel Stepper**: Hydrates any tab on demand from `events.jsonl` + `<protocol>_trajectory.json` to step through `Attempt 0 | Initial` -> `Attempt 1..K` -> `Final`, complete with a `Show Rejected Input .scm` toggle, Pydantic JSON AST viewer, compiler diagnostic banner, retrieved MITRE manual RAG chunks, and interactive SVG shape diagrams.
- **HTTP & SSE Endpoints**:
  - `GET /`: Serves the single-page dashboard (`src/visualizer/static/index.html`).
  - `GET /api/events`: Live Server-Sent Events (SSE) stream.
  - `GET /api/tabs`: Compact `#1..#N` accepted-tab summaries and `filtered_total`.
  - `GET /api/active` & `GET /api/history`: Bounded in-memory events for the currently active RFC.
  - `GET /api/tab/{tab_index}`: Lazy on-demand disk hydration for tab `#{tab_index}` (`attempts`, `events`, `verbatim_slice`, `quality_assessment`, `shapes_xhtml`).
  - `GET /api/filtered?offset=0&limit=100&q=...`: Paginated/searchable disqualified RFC records.
  - `GET /api/models`: Live per-stage model slugs resolved from `prompts/*.md` frontmatter and `cpsa_timeout_seconds`.
  - `GET /api/artifact?path=...`: Serves `.scm`, `.json`, `.svg`, and `.xhtml` verification artifacts.
