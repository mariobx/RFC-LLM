# Verification Engine & Closed-Loop Self-Healing

## 1. Stage 4: Roletran Check ([`src/verification_engine/roletran_executability_gate.py`](../src/verification_engine/roletran_executability_gate.py))

Invoking the full CPSA strand-space solver (`cpsa4`) on an ill-formed model wastes compute on unexecutable roles. Stage 4 runs a pre-flight static executability check bounded by `ROLETRAN_TIMEOUT_SECONDS = 15` ([`src/system_config.py`](../src/system_config.py)), catching structural, scoping, and destructibility defects in milliseconds before full compilation.

### 1.1 Basic Algebra Path (`cpsa4roletran`)
For protocols declared under `basic` message algebra:
- Pipes `<protocol>.scm` into `~/.cabal/bin/cpsa4roletran`.
- **Procedural Executability Semantics**: Verifies that every protocol role compiles cleanly into an executable procedure (`defproc`):
  1. **Constructibility**: Every transmitted term can be built from the role's declared `inputs`, freshly originating values (`uniq-orig`), and previously received terms.
  2. **Destructibility**: Every received term can be parsed and decrypted using keys already held in `inputs` or extracted from earlier receptions.
  3. **Input/Output Disjointness & Trace Occurrence**: Every parameter in `inputs`, `outputs`, and `uniq-orig` appears in the role's trace, and no `inputs` variable is repeated in `outputs` or `uniq-orig`.

### 1.2 Diffie-Hellman Algebra Path (`cpsa4 -l 1`)
- **MITRE CPSA 4.4.9 Binary Constraint**: `cpsa4roletran` implements only `CPSA.Roletran.Algebra` (`basic` algebra) and rejects `diffie-hellman` protocols unconditionally with `Expecting terms in basic algebra`.
- **Dual Pre-Flight Strategy**:
  When `diffie-hellman` is present in `<protocol>.scm`, `verify_role_executability()` automatically executes `~/.cabal/bin/cpsa4 -l 1 <protocol>.scm` (`15s` timeout):
  - Executes the CPSA S-expression loader, sort checker, role well-formedness validator, and `(uniq-gen ...)` exponent checks before stopping after 1 search step (`Step limit exceeded`).
  - Rejects any syntax, sort, or origination error (`Role not well formed`, `Expecting ...`) while passing well-formed Diffie-Hellman specifications directly to Stage 6.

---

## 2. Stage 5: Self-Healing Loop ([`src/verification_engine/compiler_diagnostic_repair.py`](../src/verification_engine/compiler_diagnostic_repair.py))

Whenever Stage 4 (`Roletran Check`) or Stage 6 (`CPSA Compilation`) rejects a candidate specification, the orchestrator enters an automated RAG-guided repair loop bounded by `MAX_REPAIR_ATTEMPTS = 50`:

```
[Rejected .scm] ──> [Compiler / Timeout Diagnostic]
                            |
                            v
               [SHA-256 AST Cycle Detection]
                            |
                            v
      [RAG Query Formulation (prompts/05_rag_query_formulation.md, 15s)]
      (Abstracts error into 3-6 CPSA manual keywords)
                            |
                            v
      [Hybrid RAG Search: refrences/chunks/manual_chunks.jsonl]
      (BM25 + ollama/nomic-embed-text Dense Vectors + RRF)
                            |
                            v
      [AST Repair (prompts/06_compiler_repair.md, 180s)]
      (Patches CPSAProtocolSpecification + enforces 3-POV skeletons)
                            |
                            v
               [Stage 3: CPSA4json -> scm Re-Emission]
```

### 2.1 Error Diagnostic Extraction
`verify_role_executability()` and `execute_mitre_make_build()` isolate actionable compiler diagnostics from `stderr`/`stdout` (such as `Received term cannot be fully destructured`, `Role not well formed: uniq-orig x doesn't originate`, `Expecting a name`, or `MITRE CPSA compilation timed out after 60 seconds`).

### 2.2 SHA-256 Oscillation & Cycle Detection
LLMs repairing compiler errors can oscillate between two invalid states (for example, adding a key to `inputs` and removing it on the next pass).
- Both `_run_roletran_self_healing_loop()` and `_run_mitre_solver_self_healing_loop()` in [`src/main_pipeline_orchestrator.py`](../src/main_pipeline_orchestrator.py) hash every candidate AST via `hashlib.sha256(protocol_ast.model_dump_json().encode()).hexdigest()`.
- If a SHA-256 hash reappears in `seen_roletran_hashes` or `seen_solver_hashes`:
  1. `cycle_detected = True` is logged and emitted to the visualizer.
  2. An explicit anti-oscillation directive is appended to the repair prompt instructing the model to abandon prior edits.
  3. Sampling temperature is raised to `max(0.4, base_temp)` to break greedy repetition.

### 2.3 Dynamic RAG Query Formulation ([`prompts/05_rag_query_formulation.md`](../prompts/05_rag_query_formulation.md))
Raw compiler errors contain protocol-specific identifiers (`edhoc.scm:72:6`, `client_random`, `connection_id_i`) that do not exist in the MITRE manual.
1. **Conceptual Abstraction Pass**: Configured via `prompts/05_rag_query_formulation.md` (`timeout: 15`, overridable via `--query-model`), abstracting concrete error strings into 3-6 formal CPSA keywords (e.g., `"roletran term origination trace inputs"` or `"asymmetric key sort rules"`).
2. **Deterministic Fallback (`fallback_sanitize_diagnostic_query`)**: If the query model times out or is unreachable, regex sanitization strips file paths, line numbers, and `make` boilerplate automatically.

### 2.4 Hybrid RAG Retrieval ([`src/rag_retriever_client.py`](../src/rag_retriever_client.py), [`refrences/scripts/03_query_rag.py`](../refrences/scripts/03_query_rag.py))
Queries the 1,426 enriched chunks in `refrences/chunks/manual_chunks.jsonl`:
- **DSL-Aware Lexical BM25**: Preserves hyphenated CPSA S-expression atoms (`defprotocol`, `non-orig`, `uniq-orig`, `uniq-gen`, `defstrandmax`).
- **Dense Vector Similarity**: 768-dimensional embeddings (`ollama/nomic-embed-text`, stored in `refrences/chunks/embeddings.npy`).
- **Reciprocal Rank Fusion (RRF)**: Fuses lexical and semantic rankings and injects the top-2 MITRE manual excerpts into the repair prompt while emitting `rag_retrieval` cards to the web visualizer.

### 2.5 Surgical AST Repair ([`prompts/06_compiler_repair.md`](../prompts/06_compiler_repair.md))
Configured via `prompts/06_compiler_repair.md` (`timeout: 180`, overridable via `--repair-model`):
- Consumes the failing `CPSAProtocolSpecification` JSON, the compiler diagnostic, retrieved MITRE manual guidance, and the verbatim RFC exchange excerpt.
- Validates the repaired JSON against `CPSAProtocolSpecification`, enforces `ensure_three_point_of_view_skeletons()`, re-emits `<protocol>.scm` via `cpsa4json`, and records `(rejected_scm, parsed_diagnostic, rag_query, retrieved_chunk_ids, repaired_scm)` in `<protocol>_trajectory.json` for Phase 3 DPO pair extraction.

---

## 3. Stage 6: CPSA Compilation & Quality Grading

### 3.1 Hard 60-Second Process-Group Compilation Cap ([`src/verification_engine/mitre_build_orchestrator.py`](../src/verification_engine/mitre_build_orchestrator.py))
Under-constrained preskeletons or unbounded Diffie-Hellman cohorts can trigger state-space explosions in `cpsa4`. Stage 6 enforces a strict 60-second compilation budget (`CPSA_TIMEOUT_SECONDS = 60`):
1. `_ensure_cpsa_makefile()` runs `~/.cabal/bin/cpsa4init` to initialize `Makefile` and `cpsa4.mk` in the RFC output directory and removes stale `.txt`/`.xhtml` artifacts prior to each attempt.
2. `_run_make_with_hard_timeout()` launches `make -B <stem>_shapes.xhtml` (`cpsa4` -> `cpsa4shapes` -> `cpsa4graph`) in an isolated process group (`start_new_session=True`).
3. If compilation exceeds `60` seconds, `os.killpg(os.getpgid(proc.pid), signal.SIGKILL)` immediately terminates `make` and all child `cpsa4` processes and raises `CPSABuildError`, feeding the timeout diagnostic back into Stage 5/6 self-healing.
4. Any remaining budget within the 60-second window is used to render the full search tree graph (`make <stem>.xhtml`).

### 3.2 Deterministic Verification Quality Tiers ([`src/verification_engine/trajectory_metadata_exporter.py`](../src/verification_engine/trajectory_metadata_exporter.py))
After `cpsa4shapes` finishes, `analyze_shapes_txt()` and `compute_quality_assessment()` inspect every preskeleton outcome in `<stem>_shapes.txt` and `<stem>.txt` to assign a deterministic quality tier:

| Quality Tier | Formal Verification Criteria | Post-Training Eligibility |
|---|---|---|
| **`GOLD`** | `cpsa4` passed, **all** participant POV skeletons realized multi-strand authenticated shapes (`max_strands >= 2`), and **all** secrecy `deflistener` skeletons remained unrealized (`realized_shapes_count == 0`, proving confidentiality). | Positive SFT (`sft_train.jsonl`) + Contrastive DPO (`dpo_pairs.jsonl`) |
| **`SILVER`** | `cpsa4` passed and **all** participant POV skeletons realized shapes (`realized_shapes_count > 0`), but at least one POV shape was single-strand (`TRIVIAL_SINGLE_STRAND`) or a `deflistener` realized a leak shape. | Contrastive DPO (`dpo_pairs.jsonl`) + Optional SFT (`--min-tier SILVER`) |
| **`BRONZE`** | `cpsa4` passed and produced preskeleton outcomes, but one or more participant POV skeletons failed to realize (`DEAD_HANDSHAKE`). | Trajectory inspection + Optional `<think>` (`--min-tier BRONZE`) |
| **`REJECTED`** | `cpsa4` failed to compile or produced zero preskeleton outcomes after exhausting `MAX_REPAIR_ATTEMPTS = 50`. | Excluded from positive SFT/DPO |

`write_trajectory_metadata_bundle()` prepends the structured MoE conditioning header (`;;; [RFC-ID: ...]`, `;;; [QUALITY-TIER: ...]`) to `<protocol>.scm` and writes `<protocol>_trajectory.json`.

---

## 4. The 300-Query Golden Retrieval Benchmark

The hybrid retrieval engine is evaluated against [`refrences/reports/golden_benchmark.jsonl`](../refrences/reports/golden_benchmark.jsonl) (300 ground-truth CPSA queries spanning 4 categories):
- **SYN-001 to SYN-075**: BNF syntax, sort hierarchies, Equation 10.1, and channel rules.
- **PROT-001 to PROT-085**: Official MITRE `.scm` protocol models (Kerberos, Needham-Schroeder-Lowe, Otway-Rees, Yahalom, Diffie-Hellman).
- **TH-001 to TH-075**: Strand space shape analysis, skeleton homomorphisms, and cohort pruning.
- **ADV-001 to ADV-065**: Stateful protocols (`load`/`stor`, `locn`), envelopes, and first-order `defrule`/`defgoal` logic.

Run the benchmark suite:
```bash
.venv/bin/python refrences/reports/evaluate_rag.py
```
