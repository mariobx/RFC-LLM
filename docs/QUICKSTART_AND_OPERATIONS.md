# Quickstart & Operations Runbook

## 1. System Requirements & Setup

### 1.1 Prerequisites
- **Operating System**: Linux (Ubuntu 22.04+ or Debian 12 recommended)
- **Python**: 3.10, 3.11, or 3.12 (virtual environment at `.venv/`)
- **Haskell Toolchain**: GHC 9.6+ and Cabal 3.10+
- **Graphviz**: `sudo apt install graphviz` (provides `dot` for SVG shape rendering)
- **MITRE CPSA 4.4.9 Suite** compiled and installed to `~/.cabal/bin/`:
  - `cpsa4`: Core strand space analyzer
  - `cpsa4json`: Scheme <-> JSON AST compiler
  - `cpsa4roletran`: Procedural executability compiler (`basic` algebra)
  - `cpsa4init`: `Makefile` and `cpsa4.mk` project initializer
  - `cpsa4shapes`: Minimal realized shape distiller
  - `cpsa4graph`: Interactive XHTML/SVG graph renderer
  - `cpsa4prot`: Protocol table renderer

Verify binary installation:
```bash
~/.cabal/bin/cpsa4 -v
~/.cabal/bin/cpsa4json -v
~/.cabal/bin/cpsa4roletran -v
```

### 1.2 Python Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1.3 Credentials & Endpoints Configuration (`.env`)
Copy [`.env.example`](../.env.example) to `.env` and populate your API keys and local/Tailscale base URLs:
```bash
cp .env.example .env
```

`.env` holds **only** API credentials and base endpoint URLs:
```bash
# Cloud & Unified Proxy Credentials
GEMINI_API_KEY=your_gemini_api_key_here
NOUS_API_KEY=your_nous_api_key_here
NOUS_API_BASE=https://inference-api.nousresearch.com/v1
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Local & Tailscale Model Base Endpoints
OLLAMA_API_BASE=http://localhost:11434
STRATA_API_BASE=http://localhost:11435/v1
```

Per-stage `model`, HTTP `timeout` (`180s` default; `15s` for `05_rag_query_formulation.md`), and `temperature` are configured directly in the YAML frontmatter at the top of [`prompts/01_applicability_gate.md`](../prompts/01_applicability_gate.md) through [`prompts/07_think_token_synthesizer.md`](../prompts/07_think_token_synthesizer.md) and **hot-reload live mid-batch** without restarting `./rfc-llm`.

### 1.4 Execution Limits & Compiler Caps ([`src/system_config.py`](../src/system_config.py))
- **`CPSA_TIMEOUT_SECONDS = 60`**: Hard 60-second process-group `SIGKILL` cap on MITRE `make` / `cpsa4` compilation to contain state-space explosions.
- **`ROLETRAN_TIMEOUT_SECONDS = 15`**: 15-second cap on Stage 4 `cpsa4roletran` / `cpsa4 -l 1` pre-flight checks.
- **`MAX_REPAIR_ATTEMPTS = 50`**: Maximum Stage 5/6 RAG self-healing iterations per verification loop.
- **Per-Prompt LLM `timeout:`**: Configured in `prompts/*.md` YAML frontmatter (`180s` default, `15s` for `05_rag_query_formulation.md`).

---

## 2. CLI Execution & Commands

The repository root provides two CLI wrappers that automatically configure `PYTHONPATH` and invoke `.venv/bin/python`:
- [`./rfc-llm`](../rfc-llm): Phase 2 RFC-to-CPSA synthesis, formal verification, and `--view` offline visualizer replay ([`src/pipeline.py`](../src/pipeline.py)).
- [`./rfc-think`](../rfc-think): Phase 3 hindsight `<think>` token and SFT/DPO dataset synthesizer ([`src/generate_think/cli.py`](../src/generate_think/cli.py)).

### 2.1 Single RFC Synthesis & Verification
```bash
./rfc-llm refrences/all_RFCs/rfc9528.txt
```
- Creates an isolated timestamped run directory `output/run_YYYY-MM-DD_HH-MM-SS/` containing `metadata_index.json` and `rfc9528/` (`verbatim_slice.txt`, `events.jsonl`, `edhoc.scm`, `edhoc_shapes.xhtml`, `edhoc_trajectory.json`).
- Launches the live web visualizer automatically at `http://127.0.0.1:8080` (pass `--no-visualize` for headless execution, or `--keep-alive 600` to keep the server up for 600 seconds in non-interactive scripts).

### 2.2 Directory Batch Processing
```bash
./rfc-llm refrences/all_RFCs/ \
  --tier0-eligible-only \
  --skip-completed \
  --target-eligible 25
```
Key batch flags:
- `--limit N` (`-n N`): Scan at most `N` candidate RFC files.
- `--target-eligible E` (`-e E`): Stop batch processing once `E` eligible cryptographic protocols have been synthesized.
- `--tier0-eligible-only`: Pre-filter directory candidates using the deterministic <1ms Tier 0 header check before applying `--limit`.
- `--skip-completed`: Skip RFC IDs already recorded in `logs/pipeline_runs.csv`.
- `--random`: Shuffle candidate RFCs randomly before applying `--limit`.
- `--pattern "rfc*.txt"`: Custom glob pattern when scanning a directory.
- `--output-dir <dir>` (`-o <dir>`): Custom parent output directory (or explicit `run_*` folder).

### 2.3 Offline Visualizer Replay (`--view`)
Open any previously completed run directory (or `metadata_index.json`) in the web visualizer without running synthesis:
```bash
./rfc-llm --view output/run_2026-10-28_16-03-11 --port 8080
```

### 2.4 One-Off CLI Model Overrides
For persistent routing changes (including live mid-batch updates), edit `model:` in `prompts/01_*.md` .. `07_*.md`. For temporary single-run overrides, pass CLI flags:
```bash
./rfc-llm refrences/all_RFCs/rfc5246.txt \
  --router-model nous/z-ai/glm-5.3 \
  --extraction-model nous/google/gemini-4-argon \
  --repair-model nous/google/gemini-3.8-flash \
  --query-model nous/anthropic/claude-haiku-5.5
```
(Or pass `--model <provider>/<slug>` to override all stages simultaneously.)

### 2.5 Phase 3 Hindsight Reasoning (`<think>`) Synthesis (`./rfc-think`)
Generate `<protocol>_think.json` artifacts alongside `<protocol>_trajectory.json`, plus consolidated `sft_train.jsonl` and `dpo_pairs.jsonl` files in the run root directory:
```bash
# Default ('auto' mode: DSPy/LLM using prompts/07_think_token_synthesizer.md with deterministic fallback)
./rfc-think output/run_2026-10-28_16-03-11

# Filter to strictly GOLD-verified protocols and override the synthesizer model
./rfc-think output/run_2026-10-28_16-03-11 --min-tier GOLD --model strata/unsloth-iq4_xs

# Zero-LLM programmatic synthesis directly from AST + compiler backtracking history
./rfc-think output/run_2026-10-28_16-03-11 --mode deterministic
```
Flags:
- `--mode {auto,llm,deterministic}`: Synthesis strategy (default: `auto`).
- `--min-tier {GOLD,SILVER,BRONZE,REJECTED}`: Minimum verification quality tier to include (default: `BRONZE`).
- `--model <slug>` (`-m`): Override `model:` from `prompts/07_think_token_synthesizer.md`.
- `--no-jsonl`: Write per-RFC `<protocol>_think.json` bundles without exporting run-level `sft_train.jsonl` and `dpo_pairs.jsonl`.

#### Programmatic Verification Quality Tiers
- **`GOLD`**: `cpsa4` succeeded, every participant POV skeleton realized multi-strand authenticated shapes (`max_strands >= 2`), and every secrecy `deflistener` skeleton remained unrealized (`0` shapes, proving secret confidentiality).
- **`SILVER`**: `cpsa4` succeeded and every participant POV skeleton realized at least one shape, with single-strand realization or realized listener shapes.
- **`BRONZE`**: `cpsa4` succeeded, but one or more participant POV skeletons failed to realize (`DEAD_HANDSHAKE`).
- **`REJECTED`**: `cpsa4` build failed or produced zero preskeleton outcomes.

---

## 3. Multi-RFC Virtualized Web Visualizer

Enabled by default during `./rfc-llm` runs and in offline `./rfc-llm --view <run_dir>` replay mode:
- **URL**: `http://127.0.0.1:8080` (configurable via `--port`; disable via `--no-visualize`).
- **Virtualized `#1..#N` Tab Bar**: Accepted RFCs receive sequential `#1..#N` tabs displaying tab number, RFC ID, quality tier (`GOLD`/`SILVER`/`BRONZE`/`REJECTED`), and protocol name. Virtual scrolling and on-demand disk hydration (`events.jsonl` + `<protocol>_trajectory.json`) maintain `O(1)` browser DOM nodes and `O(1)` server RAM across 5,000+ tabs.
- **Collapsible `Filtered / Skipped` Drawer**: Displays Tier 0 and Stage 1c rejected RFCs with search and 100-row pagination without polluting the accepted tab strip.
- **6-Stage Horizontal Stepper**: Live per-stage timers, active model slugs, and status across `Document Intake`, `JSON CPSA Generation`, `CPSA4JSON -> .scm`, `Roletran Check`, `Self-Healing Loop`, and `CPSA Compilation`.
- **Per-Attempt Time-Travel Stepper**: Step across `Attempt 0 | Initial` -> `Attempt 1..K` -> `Final`, toggle between rejected input `.scm` and repaired `.scm`, and inspect the Pydantic JSON AST, sliced RFC text, compiler diagnostics, retrieved MITRE manual chunks, and SVG shape graphs.

---

## 4. Running Tests & Benchmarks

### 4.1 Unit & Integration Test Suite
```bash
.venv/bin/pytest tests/
```
Test modules under [`tests/`](../tests/):
- `test_document_ingestion.py`: Tier 0 header filter regexes, TOC parsing, and verbatim section slicing.
- `test_cpsa_scoping_and_prompts.py`: CPSA 4.4.9 positional keyword scoping, Equation 10.1 enforcement, and `prompts/*.md` YAML frontmatter loader / live hot-reload tests.
- `test_code_generation_and_verification.py`: Pydantic AST validation, `cpsa4json` Scheme emission, `Roletran Check`, and hard-timeout `CPSA Compilation`.
- `test_main_pipeline_orchestrator.py`: End-to-end 6-stage synthesis and timestamped run directory / `metadata_index.json` tests.
- `test_trajectory_and_hardening.py`: Programmatic quality-tier grading (`GOLD`/`SILVER`/`BRONZE`/`REJECTED`), trajectory export, and compiler timeout hardening.
- `test_visualizer_and_events.py` & `test_visualizer_tabs.py`: Bounded `O(1)`-RAM event bus, sequential `#1..#N` tab hydration, filtered RFC drawer pagination, and offline `--view` replay.
- `test_generate_think.py`: Phase 3 `<think>` hindsight rationalization, no-leakage invariants, and SFT/DPO JSONL export.

### 4.2 RAG Information Retrieval Benchmark
```bash
.venv/bin/python refrences/reports/evaluate_rag.py
```
Evaluates MRR, Recall@1, Recall@5, and Mean NDCG across 300 ground-truth CPSA queries for BM25, Dense (`ollama/nomic-embed-text`), and Hybrid RRF retrieval.

---

## 5. Troubleshooting Runbook

| Diagnostic / Symptom | Root Cause | Solution |
|---|---|---|
| `MITRE CPSA compilation timed out after 60 seconds` | Unbounded strand search / state-space explosion in `cpsa4`. | `_run_make_with_hard_timeout` automatically `SIGKILL`s the `make`/`cpsa4` process group at `CPSA_TIMEOUT_SECONDS = 60` and routes the timeout diagnostic into Stage 5/6 self-healing to tighten role/skeleton constraints. |
| `Roletran REJECT: Expecting terms in basic algebra` | Protocol uses `diffie-hellman` algebra, while `cpsa4roletran` only supports `basic`. | Handled automatically: `roletran_executability_gate.py` branches to `cpsa4 -l 1` (`15s` timeout) whenever `diffie-hellman` is present. |
| `Expecting terms in algebra basic` (from `cpsa4`) | Herald S-expression missing `(algebra diffie-hellman)`. | `to_cpsa_json_payload()` automatically injects `["algebra", "diffie-hellman"]` into the `herald` form for Diffie-Hellman specs. |
| `Role not well formed: uniq-orig x doesn't originate` | Fresh exponent of sort `rndx` placed in `uniq-orig`. | Exponents in `(exp (gen) x)` must use `rndx` + `(uniq-gen x)`. `CPSAProtocolRole.to_cpsa_json()` automatically migrates `rndx`/`expt` variables from `unique_originating` to `unique_generated`. |
| `Received term cannot be fully destructured` | Role receives an encrypted message without holding the decryption key in `inputs`. | Declare the principal's private key or shared key in the role's `inputs` list (automatically patched by Stage 5 `Self-Healing Loop`). |
| `Undeclared variable <var> in inputs` | Variable listed in `inputs`, `outputs`, or `uniq-orig` never appears in `trace`. | Every parameter in `inputs`/`outputs`/`uniq-orig` must appear in at least one `send` or `recv` event. |
| `APITimeoutError` / `429 RateLimitError` | Endpoint latency or provider rate limit. | Adjust `timeout:` or switch `model:` directly in the relevant `prompts/0*.md` frontmatter (hot-reloads live on the next call without restarting). |
| `cpsa4json binary missing at ~/.cabal/bin/cpsa4json` | MITRE CPSA 4.4.9 binaries not installed to `~/.cabal/bin`. | Install CPSA via Cabal (`cabal install cpsa --installdir=$HOME/.cabal/bin`). |
