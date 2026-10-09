# Quickstart & Operations Runbook

## 1. System Requirements & Setup

### 1.1 Prerequisites
- **Operating System**: Linux (Ubuntu 22.04+ or Debian 12 recommended)
- **Python**: 3.10, 3.11, or 3.12 (Virtual environment at `.venv/`)
- **Haskell Toolchain**: GHC 9.6+ and Cabal 3.10+
- **Graphviz**: `sudo apt install graphviz` (provides `dot` for SVG generation)
- **MITRE CPSA 4.4.9 Suite**:
  Must be compiled and installed to `~/.cabal/bin/`:
  - `cpsa4`: Core strand space analyzer
  - `cpsa4json`: Scheme $\leftrightarrow$ JSON AST compiler
  - `cpsa4roletran`: Procedural executability compiler
  - `cpsa4init`: Makefile and project scaffolding tool
  - `cpsa4shapes`: Shape extraction and distillation tool
  - `cpsa4graph`: SVG graph generator
  - `cpsa4prot`: Protocol table renderer

Verify binary installation:
```bash
~/.cabal/bin/cpsa4 -v
~/.cabal/bin/cpsa4json --version
~/.cabal/bin/cpsa4roletran
```

### 1.2 Python Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1.3 API Keys Configuration (`.env`)
Create `.env` in the repository root:
```bash
# Nous Research Portal Credentials
NOUS_API_KEY=sk-nous-...
NOUS_API_BASE=https://inference-api.nousresearch.com/v1

# Google Gemini Credentials (Free Tier)
GEMINI_API_KEY=AIzaSy...

# Decoupled Model Routing
LLM_QUERY_MODEL=gemini/gemini-3.5-flash-lite
LLM_ROUTER_MODEL=nous/deepseek/deepseek-chat
LLM_EXTRACTION_MODEL=nous/anthropic/claude-haiku-5.5
LLM_REPAIR_MODEL=nous/deepseek/deepseek-chat

# Subprocess & HTTP Timeouts (Seconds)
SUBPROCESS_TIMEOUT_SECONDS=180
ROLETRAN_TIMEOUT_SECONDS=30
```

---

## 2. CLI Execution & Commands

The project root contains the executable wrapper `./rfc-llm` which automatically configures `PYTHONPATH` and activates `.venv`.

### 2.1 Single RFC Synthesis & Verification
Run on a single RFC text file with live visualization:
```bash
./rfc-llm refrences/all_RFCs/rfc9528.txt --output-dir output/run_rfc9528 --visualize
```
- Open `http://127.0.0.1:8080` in your browser to view the real-time pipeline execution DAG, logs, and generated shapes.
- When running non-interactively in scripts, add `--keep-alive 600` to keep the visualizer running for 10 minutes post-completion.

### 2.2 Directory Batch Processing
Process an entire directory of RFCs:
```bash
./rfc-llm refrences/all_RFCs/ --pattern "rfc*.txt" --output-dir output/batch_runs --limit 50 --skip-completed
```
- `--pattern "rfc*.txt"`: Glob pattern for selecting RFC text files.
- `--limit 50`: Restricts processing to the first 50 discovered files.
- `--skip-completed`: Checks `logs/pipeline_runs.csv` and skips RFCs that already have completed execution entries.

### 2.3 Model Overrides via CLI
Override any model assignment without editing `.env`:
```bash
./rfc-llm refrences/all_RFCs/rfc5246.txt \
  --extraction-model nous/anthropic/claude-haiku-5.5 \
  --router-model nous/deepseek/deepseek-chat \
  --repair-model nous/deepseek/deepseek-chat \
  --query-model gemini/gemini-3.5-flash-lite
```

---

## 3. Web Visualizer Dashboard

The visualizer starts automatically when `--visualize` is active (default).

- **URL**: `http://127.0.0.1:8080`
- **Port Override**: `./rfc-llm ... --port 8888`
- **Headless Mode**: Pass `--no-visualize` to disable the visualizer server entirely.

### Dashboard Capabilities
1. **Live Stepper**: Displays real-time status (Idle, Running, Passed, Failed) for all 5 stages.
2. **Execution Logs**: Real-time log stream over Server-Sent Events (SSE).
3. **Artifact Inspector Tabs**:
   - `Verbatim Slice`: Shows lines sliced from the RFC.
   - `Extracted AST`: Live JSON representation of the Pydantic spec.
   - `Emitted Scheme`: The compiled `.scm` source code.
   - `Shape Graph`: Interactive SVG showing realized shapes and secrecy proofs.
   - `RAG Retrieval`: Queries, scores, and chunk snippets used for grounding.

---

## 4. Running Tests & Benchmarks

### 4.1 Unit & Integration Test Suite
```bash
.venv/bin/pytest tests/
```
The test suite contains 24 tests across:
- `test_document_ingestion.py`: Header filter regexes, TOC parsing, and section slicing.
- `test_code_generation_and_verification.py`: Pydantic AST validation, operator arity enforcement, `cpsa4json` emission, roletran gates, and build orchestrator.
- `test_main_pipeline_orchestrator.py`: End-to-end synthesis pipeline on sample RFCs.
- `test_visualizer_and_events.py`: Global event bus thread-safety, SSE endpoints, and cycle jitter.

### 4.2 RAG Information Retrieval Benchmark
Run evaluation across 300 ground-truth queries:
```bash
.venv/bin/python refrences/reports/evaluate_rag.py
```
Outputs MRR, Recall@1, Recall@5, and Mean NDCG across BM25, Dense, Hybrid RRF-60, and Hybrid RRF-20.

---

## 5. Troubleshooting Runbook

| Diagnostic / Symptom | Root Cause | Solution |
|---|---|---|
| `Roletran REJECT: Expecting terms in basic algebra` | Protocol uses `diffie-hellman` algebra, but `cpsa4roletran` only supports `basic`. | Handled automatically: `roletran_executability_gate.py` branches to `cpsa4 -l 1` for Diffie-Hellman files. |
| `Expecting terms in algebra basic` (from `cpsa4`) | Herald S-expression missing `(algebra diffie-hellman)`. | `to_cpsa_json_payload()` now injects `["algebra", "diffie-hellman"]` into herald whenever protocol uses Diffie-Hellman. |
| `Role not well formed: uniq-orig x doesn't originate` | Random exponent of sort `rndx` was placed in `uniq-orig`. | Exponents in $(g)^x$ cannot originate as carried terms. Sort `rndx` variables must be declared in `uniq-gen`. AST serializer automatically migrates `rndx` to `uniq-gen`. |
| `Value error, Invalid term node at 'term[...]'. Expected string atom, integer, or nested operator list, got dict` | LLM embedded a variable metadata dictionary inside a message term. | `desugar_term_tree` unpacks `term["name"]` automatically, and 1-shot self-healing repairs any remaining syntax defects. |
| `Received term cannot be fully destructured` | Role receives an encrypted payload but lacks the corresponding decryption key in its inputs. | Ensure the principal's private key or shared symmetric key is declared in `inputs`. |
| `Undeclared variable <var> in inputs` | Variable declared in `inputs` or `outputs` never appears in the trace. | In CPSA roletran, every parameter in `inputs`/`outputs` must be transmitted or received in a trace event. Remove unused variables from inputs. |
| `APITimeoutError` / `429 RateLimitError` | Proxy rate-limit or network latency to Nous Research Portal. | `constrained_protocol_extractor.py` and `compiler_diagnostic_repair.py` include exponential backoff retries with `SUBPROCESS_TIMEOUT_SECONDS=180`. |
| `cpsa4json binary missing at ~/.cabal/bin/cpsa4json` | Cabal binaries not installed or wrong path. | Recompile CPSA with `cabal install --installdir=$HOME/.cabal/bin`. |
