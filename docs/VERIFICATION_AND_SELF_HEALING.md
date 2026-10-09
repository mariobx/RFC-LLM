# Verification Engine & Closed-Loop Self-Healing

## 1. Pre-Flight Executability Gate (`src/verification_engine/roletran_executability_gate.py`)

Running the full CPSA solver (`cpsa4`) on a broken model is computationally expensive (can take seconds or minutes depending on search depth). The pre-flight executability gate catches syntactic and structural defects in under 40 milliseconds before solver invocation.

### 1.1 The Basic Algebra Path (`cpsa4roletran`)
For protocols declared under `basic` message algebra:
- Runs `~/.cabal/bin/cpsa4roletran <protocol>.scm`.
- **Procedural Executability Semantics**: `cpsa4roletran` verifies that a protocol role corresponds to a real, executable program:
  1. **Constructibility**: Every transmitted term can be assembled from the role's declared inputs and previously received messages.
  2. **Destructibility**: Every received term can be parsed and decrypted using known or previously received keys.
  3. **Output Validity**: Every term in `outputs` can be built from known parameters.
- **Output**: Compiles the role into language-independent procedural code (`defproc`).

### 1.2 The Diffie-Hellman Algebra Path (`cpsa4 -l 1`)
- **Crucial Architecture Fact**: In MITRE CPSA 4.4.9, `cpsa4roletran` only implements `CPSA.Roletran.Algebra` (the basic cryptoalgebra). It **does not support Diffie-Hellman exponentiation**. Passing a `diffie-hellman` protocol to `cpsa4roletran` unconditionally outputs: `Expecting terms in basic algebra`.
- **The Dual Strategy**:
  When `diffie-hellman` is detected in the Scheme file:
  - The gate branches to `~/.cabal/bin/cpsa4 -l 1 <protocol>.scm`.
  - Runs with step limit 1 to execute loader parsing, variable scope checking, and sort validation without performing full strand search.
  - Verifies that all exponents are declared as `rndx`, all exponent origination uses `uniq-gen`, and all DH terms (`exp`, `gen`, `mul`) are algebraically well-formed.

---

## 2. Closed-Loop Self-Healing Diagnostic Repair (`src/verification_engine/compiler_diagnostic_repair.py`)

When the pre-flight gate or solver rejects a specification, the orchestrator triggers an automated repair cycle (up to 50 attempts).

```
[Failing Scheme File] ──► [Compiler Diagnostic: ":6:6: Received term cannot be fully destructured"]
                                │
                                ▼
                       [MD5 AST Cycle Detection]
                                │
                                ▼
                    [Gemini 3.5 Flash Lite Query Formulation]
                    (Abstracts to: "roletran trace reception term destructuring")
                                │
                                ▼
                    [Hybrid RAG Search: manual_chunks.jsonl]
                    (Retrieves Chapter 6 / Table 10.6 rule chunks)
                                │
                                ▼
                    [DeepSeek-Chat Surgical AST Patch]
                    (Adds decryption key to role inputs)
                                │
                                ▼
                    [Pydantic Re-Validation & Scheme Re-Emission]
```

### 2.1 Error Diagnostic Extraction
The gate parses standard error streams into clean error strings:
- Strips file paths, line numbers, and Make boilerplate.
- Isolates the root compiler diagnostic: e.g. `Received term cannot be fully destructured`, `Uniquely originating value x does not originate in trace`, `Expecting a name`.

### 2.2 Oscillation & Cycle Detection
LLMs frequently fall into greedy minimum oscillations (e.g. adding variable `k` to `inputs`, then removing it next turn because of an unused variable warning).
- The engine hashes each serialized AST: `hashlib.md5(spec.model_dump_json().encode()).hexdigest()`.
- Hashed ASTs are stored in an execution cache `seen_spec_hashes`.
- If an AST hash is seen again:
  - `cycle_detected = True`.
  - Injects a strict cycle warning into the prompt instructing the model to discard previous edits.
  - Jitters sampling temperature from `0.0` to `0.4` to break greedy determinism.

### 2.3 Two-Phase Dynamic RAG Query Formulation
Querying vector databases with raw compiler diagnostics yields poor retrieval because compiler errors contain local file paths and concrete protocol variables (`edhoc.scm:14:1`, `connection_id_i`) that never appear in the MITRE manual.
1. **Abstraction Pass (`LLM_QUERY_MODEL` / Gemini 3.5 Flash Lite)**:
   - Takes: `Failure Stage: roletran` + `Compiler Diagnostic: Expecting a name`.
   - Produces 3–6 word conceptual query: `"asymmetric key constructor pubk name sort"`.
   - Completely removes protocol-specific variables and line numbers.
2. **Fallback Sanitizer (`fallback_sanitize_diagnostic_query`)**:
   - If the LLM call fails or times out, deterministic regex purges numbers, paths, and punctuation, preserving compiler keywords.

### 2.4 Hybrid RAG Retrieval (`refrences/scripts/03_query_rag.py`)
Queries the 1,426 chunks in `manual_chunks.jsonl`:
- **Lexical BM25**: Preserves hyphenated Scheme S-expression atoms (`defprotocol`, `non-orig`, `uniq-orig`).
- **Dense Vectors**: `embeddings.npy` semantic vector similarity.
- **Reciprocal Rank Fusion (RRF-60)**:
  $$RRF\_Score(d) = \sum_{m \in \{BM25, Dense\}} \frac{1}{60 + Rank_m(d)}$$
- Injects the top 2 relevant manual excerpts directly into the repair prompt.

### 2.5 Surgical AST Mutation (`LLM_REPAIR_MODEL` / DeepSeek-Chat)
- DeepSeek receives: failing AST JSON + exact diagnostic + manual guidance + verbatim RFC excerpt.
- Emits the repaired JSON matching `CPSAProtocolSpecification`.
- Pydantic validates the patched AST and passes it back to Stage 3 for re-emission.

---

## 3. MITRE CPSA Build Orchestrator (`src/verification_engine/mitre_build_orchestrator.py`)

When pre-flight verification succeeds, the orchestrator triggers GNU Make to generate formal shapes.

### 3.1 Build Lifecycle
1. `_ensure_cpsa_makefile()`: Invokes `~/.cabal/bin/cpsa4init` in the target directory to create the official `Makefile` and `cpsa4.mk`.
2. Sets `PATH` to include `~/.cabal/bin`.
3. Executes `make <stem>_shapes.xhtml`:
   - `cpsa4 <stem>.scm -o <stem>.txt`: Derives all strand space skeletons.
   - `cpsa4shapes <stem>.txt -o <stem>_shapes.txt`: Filters unrealized search nodes down to minimal shapes.
   - `cpsa4graph <stem>_shapes.txt -o <stem>_shapes.xhtml`: Generates interactive SVG graphs embedded in XHTML.
4. Executes `make <stem>.xhtml` to render the full search tree DAG.

### 3.2 Realized Shape Counting
Parses `_shapes.txt` for `(defskeleton` occurrences:
- If `shapes_count > 0`: Formal verification succeeded. Bilateral shapes are realized.
- If `shapes_count == 0`: Skeletons are unrealized / dead (expected only for Secrecy Skeletons where the secret was protected from the adversary).

---

## 4. The 300-Query Golden Benchmark

The retrieval engine is benchmarked using `refrences/reports/golden_benchmark.jsonl` (300 verified ground-truth queries partitioned across 4 MITRE manuals):
- **SYN-001 to SYN-075**: Grammar, BNF syntax, sort hierarchies, channel rules.
- **PROT-001 to PROT-085**: Authoritative Scheme protocol models (Kerberos, NSL, Otway-Rees, Yahalom, Diffie-Hellman hacks).
- **TH-001 to TH-075**: Shape analysis theorems, skeleton quotienting, augmentation theorems.
- **ADV-001 to ADV-065**: State envelopes, door separators, fact rules.

Benchmark runner:
```bash
.venv/bin/python refrences/reports/evaluate_rag.py
```
Evaluates BM25, Dense, Hybrid RRF-60, Hybrid RRF-20, and Two-Stage Rerank. Hybrid RRF-60 achieves >0.85 Mean Reciprocal Rank (MRR) and >0.92 Recall@5 across specialized Scheme DSL tokens.
