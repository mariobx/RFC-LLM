# RFC-LLM

**RFC-LLM** is an automated pipeline that reads IETF RFC documents, identifies real cryptographic handshake protocols, extracts the exact message-exchange sections, and translates them into formally verified **MITRE CPSA 4.4.9** (Cryptographic Protocol Shapes Analyzer) models. It runs CPSA's compiler and strand-space solver (`cpsa4json`, `cpsa4roletran`, and `cpsa4`) in a self-healing repair loop to prove authentication shapes and secrecy properties, and packages the verified runs and `<think>` reasoning traces into training datasets (`sft_train.jsonl` and `dpo_pairs.jsonl`).

---

## 1. Pipeline Overview

[`src/main_pipeline_orchestrator.py`](src/main_pipeline_orchestrator.py) executes a **6-stage compiler-in-the-loop pipeline**:

1. **Stage 1 — Document Intake ([`src/document_ingestion/`](src/document_ingestion/))**:
   - [`rfc_header_filter.py`](src/document_ingestion/rfc_header_filter.py) & [`protocol_applicability_gate.py`](src/document_ingestion/protocol_applicability_gate.py): Rejects non-protocol RFCs (informational memos, MIBs, administrative guidelines, static payload formats, and protocols that merely run over TLS/IPsec without defining their own cryptographic handshake).
   - [`rfc_toc_parser.py`](src/document_ingestion/rfc_toc_parser.py), [`handshake_section_router.py`](src/document_ingestion/handshake_section_router.py), & [`verbatim_section_slicer.py`](src/document_ingestion/verbatim_section_slicer.py): Slices 10,000+ line RFCs down to the verbatim sections defining the cryptographic message exchange (`verbatim_slice.txt`).
2. **Stage 2 — JSON CPSA Generation ([`src/intermediate_representation/`](src/intermediate_representation/), [`src/semantic_extraction/constrained_protocol_extractor.py`](src/semantic_extraction/constrained_protocol_extractor.py))**:
   - Extracts a validated `CPSAProtocolSpecification` Pydantic AST enforcing MITRE CPSA 4.4.9 sort rules, positional keyword scoping, and the Stage 2 Verbatim Slice Bailout Gate (exiting immediately with 0 repair loops if the sliced RFC text defines no cryptographic message exchange).
   - Enforces the **3-POV Preskeleton Architecture**: pure 1-strand `defstrandmax` Point-of-View skeletons for each role (with zero listeners) plus a dedicated `deflistener` secrecy probe skeleton.
3. **Stage 3 — CPSA4json -> scm ([`src/code_generation/`](src/code_generation/))**:
   - [`cpsa_json_serializer.py`](src/code_generation/cpsa_json_serializer.py) & [`cpsa_scheme_emitter.py`](src/code_generation/cpsa_scheme_emitter.py): Runs the deterministic AST pre-normalizer (auto-quoting undeclared constant tags/numbers as `"\"tag\""`, inferring missing `name`/`locn` variables from `ltk`/`bltk`/`pubk`/`privk`/`load`/`stor`, and abstractly interpreting role traces to synthesize `cpsa4roletran` `inputs`), serializes CPSA JSON S-expression arrays, and compiles them into canonical CPSA 4.4.9 `.scm` code via `cpsa4json`.
4. **Stage 4 — Roletran Check ([`src/verification_engine/roletran_executability_gate.py`](src/verification_engine/roletran_executability_gate.py))**:
   - Runs `cpsa4roletran` (for stateless `basic` algebra) or `cpsa4 -l 1` (for `diffie-hellman` or stateful `locn`/`load`/`stor` specifications) under `ROLETRAN_TIMEOUT_SECONDS = 15` to verify role constructibility, destructibility, and variable origination before invoking full strand-space search.
5. **Stage 5 — Self-Healing Loop ([`src/verification_engine/compiler_diagnostic_repair.py`](src/verification_engine/compiler_diagnostic_repair.py), [`src/rag_retriever_client.py`](src/rag_retriever_client.py))**:
   - Intercepts Stage 4 (`Roletran Check`) or Stage 6 (`CPSA Compilation`) rejections, tracks canonical SHA-256 AST hashes (stripping cosmetic prose/comments) and prior failed attempt summaries to break `A -> B -> A` repair oscillations, runs the Pinned CPSA Header + Agentic CPSA Knowledge Base Searcher (`refrences/cpsa_kb/`), and patches the Pydantic AST while preserving 1-to-1 fidelity to the verbatim RFC.
6. **Stage 6 — CPSA Compilation & 3-Tier Snowball State Recovery ([`src/verification_engine/mitre_build_orchestrator.py`](src/verification_engine/mitre_build_orchestrator.py), [`src/verification_engine/snowball_autopsy.py`](src/verification_engine/snowball_autopsy.py), [`src/verification_engine/trajectory_metadata_exporter.py`](src/verification_engine/trajectory_metadata_exporter.py))**:
   - Executes `cpsa4init` and `make` (`cpsa4`, `cpsa4shapes`, `cpsa4graph`) under a hard 15-second process-group `SIGKILL` cap (`CPSA_TIMEOUT_SECONDS = 15`) with 3-tier snowball state recovery (Tier 1 herald search-order portfolio, Tier 2 partial `.txt` snowball autopsy, Tier 3 structural anti-unification repair).
   - Scores deterministic verification quality tiers (`GOLD`, `SILVER`, `BRONZE`, `REJECTED`), records per-role and batch USD/token telemetry ([`src/cost_tracker.py`](src/cost_tracker.py)), upserts the master ledger (`logs/pipeline_runs.csv`), and updates `output/run_YYYY-MM-DD_HH-MM-SS/metadata_index.json`.

### YAML Frontmatter Model Routing & Live Hot-Reload (`prompts/*.md`)
All 7 LLM prompt templates ([`prompts/01_applicability_gate.md`](prompts/01_applicability_gate.md) through [`prompts/07_think_token_synthesizer.md`](prompts/07_think_token_synthesizer.md)) define their per-stage `model`, HTTP `timeout`, `max_tokens`, and `temperature` directly in leading YAML frontmatter via [`src/prompt_loader.py`](src/prompt_loader.py):
- **Zero-Restart Live Hot-Reload**: Edits to `model:`, `timeout:`, `temperature:`, or prompt text take effect on the very next LLM call—even mid-batch—without restarting `./rfc-llm`.
- **Clean `.env`**: `.env` ([`.env.example`](.env.example)) holds **only** API credentials (`GEMINI_API_KEY`, `NOUS_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) and base endpoint URLs (`NOUS_API_BASE`, `OLLAMA_API_BASE`, `STRATA_API_BASE`).
- **Provider Prefixes & CLI Overrides**: Supports `nous/<model>`, `strata/<model>`, `ollama/<model>`, `gemini/<model>`, `openai/<model>`, and `anthropic/<model>`, plus optional one-off CLI overrides (`--model`, `--router-model`, `--extraction-model`, `--repair-model`, `--query-model`).

### Multi-RFC Web Visualizer & Offline Replay (`--view`)
[`src/visualizer/server.py`](src/visualizer/server.py), [`src/visualizer/static/index.html`](src/visualizer/static/index.html), and [`src/pipeline_events.py`](src/pipeline_events.py) provide real-time and offline multi-RFC inspection at `http://127.0.0.1:8080`:
- **Virtualized `#1..#N` Tab Strip**: Allocates sequential `#1..#N` tabs for accepted RFCs showing tab number, RFC ID, quality tier, and protocol name.
- **Collapsible `Filtered / Skipped` Drawer**: Paginated, searchable drawer recording Tier 0, Stage 1c, and Stage 2 rejected RFCs.
- **Per-Attempt Time-Travel Stepper**: Inspect `Attempt 0 | Initial` -> `Attempt 1..K` -> `Final` with a rejected/repaired `.scm` toggle, Pydantic JSON AST, compiler diagnostics, KB rules, and SVG shape graphs.
- **Offline Replay Mode**: Inspect any completed run folder without re-running synthesis via `./rfc-llm --view output/run_<timestamp>`.

### Hindsight Reasoning (`<think>`) Synthesizer (`./rfc-think`)
Implemented in [`./rfc-think`](rfc-think) ([`src/generate_think/`](src/generate_think/) and [`prompts/07_think_token_synthesizer.md`](prompts/07_think_token_synthesizer.md)), `./rfc-think` converts verification trajectories into post-training datasets (`<protocol>_think.json`, `sft_train.jsonl`, and `dpo_pairs.jsonl`).

---

## 2. Repository Structure & Documentation Map

| Directory / File | Purpose |
| :--- | :--- |
| [`rfc-llm`](rfc-llm) | Synthesis & offline replay CLI (`./rfc-llm <rfc_or_dir>` / `./rfc-llm --view <run_dir>`) |
| [`rfc-think`](rfc-think) | `<think>` reasoning & SFT/DPO dataset synthesizer CLI (`./rfc-think <run_dir>`) |
| [`.env.example`](.env.example) | Credentials & base endpoint URLs template (`*_API_KEY`, `NOUS_API_BASE`, `OLLAMA_API_BASE`, `STRATA_API_BASE`) |
| [`prompts/`](prompts/README.md) | 7 YAML-frontmatter prompt templates (`model`, `timeout`, `temperature`) with live mid-batch hot-reload |
| [`src/`](src/) | Core 6-stage synthesis pipeline, Pydantic IR, verification engine, `<think>` synthesizer, and web visualizer |
| [`docs/`](docs/README.md) | Architecture specifications, CPSA 4.4.9 keyword reference, model routing, and operational runbooks |
| [`tests/`](tests/) | Unit and integration test suite enforcing CPSA 4.4.9 scoping, visualizer tabs, and `<think>` synthesis |
| [`refrences/`](refrences/) | MITRE CPSA 4.4.9 Knowledge Base (`cpsa_kb/`), 151 `.scm` examples, and manuals |
| [`notebook_context/`](notebook_context/README.md) | Automated repository-to-Markdown context bundler for LLM Notebook ingestion |

### Core Technical Documentation (`docs/`)
- **[System Architecture & Lifecycle](docs/ARCHITECTURE.md)**
- **[Formal Grammar & Intermediate Representation](docs/INTERMEDIATE_REPRESENTATION.md)**
- **[Complete CPSA 4.4.9 Keyword & Grammar Reference](docs/CPSA_KEYWORD_REFERENCE.md)**
- **[Tiered Model Routing & YAML Frontmatter Configuration](docs/TIERED_MODEL_ROUTING.md)**
- **[Verification Engine & Self-Healing Loop](docs/VERIFICATION_AND_SELF_HEALING.md)**
- **[Master Clean-Room Blueprint](docs/MASTER_BLUEPRINT.md)**
- **[Quickstart & Operational Runbook](docs/QUICKSTART_AND_OPERATIONS.md)**

---

## 3. Quickstart

```bash
# 1. Copy the credentials & endpoints template and populate your API keys
cp .env.example .env

# 2. Run the full test suite
.venv/bin/pytest tests/

# 3. Synthesize & formally verify a CPSA model from an RFC (live visualizer on http://127.0.0.1:8080)
./rfc-llm refrences/all_RFCs/rfc9528.txt

# 4. Replay any completed run directory offline in the virtualized multi-RFC visualizer
./rfc-llm --view output/run_YYYY-MM-DD_HH-MM-SS

# 5. Synthesize <think> traces plus sft_train.jsonl and dpo_pairs.jsonl
./rfc-think output/run_YYYY-MM-DD_HH-MM-SS

# 6. Rebuild NotebookLM / Gemini markdown context bundles after edits
python3 notebook_context/sync_context.py
```
