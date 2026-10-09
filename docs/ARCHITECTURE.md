# RFC-LLM Pipeline Architecture & Lifecycle

## 1. System Overview

RFC-LLM translates raw, unstructured IETF RFC documents into formally verified MITRE CPSA 4.4.9 models (`.scm`).

RFC specifications are full of ambiguities: English prose, ASCII sequence diagrams, and byte-level packet layouts. CPSA requires exact, order-sorted algebraic S-expressions under strict Dolev-Yao strand space semantics. Passing an RFC straight to an LLM produces hallucinated operators, invalid sort assignments, and uncompilable Scheme code.

This system decomposes translation into seven discrete compiler stages:

```
[RFC Text]
   │
   ▼
[Stage 0: Header Filter] ─── (Rejects Non-Protocols via Regex/TOC)
   │
   ▼
[Stage 1: TOC Routing & Slicing] ─── (Extracts Exchange Sections 1480-1915)
   │
   ▼
[Stage 2: Constrained Extraction] ─── (Claude Haiku 5.5 + RAG -> Pydantic AST)
   │
   ▼
[Stage 3: SCM Emission] ─── (Compiles JSON AST -> Scheme via cpsa4json)
   │
   ▼
[Stage 4: Pre-Flight Gate] ─── (cpsa4roletran for Basic / cpsa4 for DH)
   │           │
   │ (Pass)    │ (Fail)
   │           ▼
   │     [Stage 5: Self-Healing Repair] ─── (Gemini Query + DeepSeek AST Patch)
   │           │
   │           └───────► (Re-emit to Stage 3)
   ▼
[Stage 6: MITRE CPSA Analyzer] ─── (cpsa4 computes shapes / secrecy)
   │
   ▼
[Stage 7: Shape Graph Generation] ─── (cpsa4shapes -> XHTML / SVG DAGs)
```

---

## 2. Pipeline Stages

### Stage 0: Tier 0 Header & Frontmatter Filter
- **File**: `src/document_ingestion/rfc_header_filter.py`
- **Execution Cost**: <1ms (No LLM calls).
- **Function**: Inspects the first 100 lines of the RFC using regular expressions.
- **Rules**:
  - Rejects documents under 60 lines (errata, 1-page stubs).
  - Extracts RFC ID (`Request for Comments: (\d+)`) and Category (`Standards Track`, `Informational`, etc.).
  - Rejects categories: `Historic`, `Best Current Practice`.
  - Rejects blacklisted title keywords: `MIB`, `Management Information Base`, `Managed Objects`, `Architecture`, `Applicability Statement`, `Problem Statement`, `Requirements for`, `Guidelines for`, `Meeting Minutes`.

### Stage 1: TOC Parser, Gatekeeper, and Section Slicer
1. **TOC Parser** (`src/document_ingestion/rfc_toc_parser.py`):
   - Locates `Table of Contents` in lines 1–250.
   - Extracts hierarchical sections: dotted identifiers (`5.2`, `A.1`), titles, page numbers, and indentation levels.
   - Falls back to column-0 regex scanning if no formal TOC block exists.
2. **Tier 1 Applicability Gate** (`src/document_ingestion/protocol_applicability_gate.py`):
   - Feeds metadata + entire TOC to `LLM_ROUTER_MODEL` (DeepSeek-Chat).
   - Verifies whether the RFC specifies an interactive protocol with cryptographic mechanisms (keys, nonces, auth, secure channels).
   - Drops static data formats, XML schemas, transport-only specs.
3. **Handshake Section Router** (`src/document_ingestion/handshake_section_router.py`):
   - Scans the TOC to pick the specific sections defining the cryptographic handshake (e.g. `['5.2', '5.3', '5.4', '5.5']` for EDHOC).
   - Filters out non-handshake sections (IANA considerations, security considerations prose, ASN.1 tables).
4. **Verbatim Slicer** (`src/document_ingestion/verbatim_section_slicer.py`):
   - Finds column-0 section headers in the raw text.
   - Slices only the target lines (typically 200–600 lines out of 50,000+).
   - Strips page breaks, form feeds (`\x0c`), and header/footer boilerplate.
   - Saves `verbatim_slice.txt` for extraction grounding and auditing.

### Stage 2: Constrained Semantic Extraction
- **File**: `src/semantic_extraction/constrained_protocol_extractor.py`
- **Model**: `LLM_EXTRACTION_MODEL` (`nous/anthropic/claude-haiku-5.5`).
- **Input**: `verbatim_slice.txt` + RAG reference examples + Pydantic JSON schema.
- **Output**: Validated `CPSAProtocolSpecification` instance.
- **Core Constraints**:
  - Semantic variable identifiers: e.g. `client_random`, `premaster_secret`, `session_key`. No single-letter variables (`a`, `b`, `k`).
  - CPSA Sorts: `name`, `text`, `data`, `skey`, `akey`, `chan`, `rndx`, `expt`.
  - Strict atom terms: Terms in traces must be string atoms or prefix lists. Dictionaries inside terms are illegal.
  - Mandatory 3-skeleton architecture: Initiator POV (pure), Responder POV (pure), Secrecy POV (`deflistener`).
- **1-Shot Self-Correction**:
  - If `CPSAProtocolSpecification.model_validate()` fails, the raw validation error string is piped back into a fast correction turn.

### Stage 3: SCM Emission & cpsa4json Compilation
- **Files**: `src/code_generation/cpsa_json_serializer.py`, `src/code_generation/cpsa_scheme_emitter.py`
- **Process**:
  1. AST serializes to native CPSA JSON S-expression arrays:
     ```json
     ["defprotocol", "edhoc", "diffie-hellman",
       ["defrole", "initiator",
         ["vars", ["initiator_dh_exponent", "rndx"], ["connection_id_i", "text"]],
         ["trace", ["send", "ch", ["cat", "method", ["exp", ["gen"], "initiator_dh_exponent"]]]]
       ]
     ]
     ```
  2. Pipes serialized JSON into `~/.cabal/bin/cpsa4json` via stdin.
  3. Emits clean Scheme S-expressions to `<output_dir>/<stem>.scm`.

### Stage 4: Pre-Flight Executability Gate
- **File**: `src/verification_engine/roletran_executability_gate.py`
- **Execution Cost**: 15–40ms.
- **Dual Verification Path**:
  - **Basic Algebra**: Runs `~/.cabal/bin/cpsa4roletran <stem>.scm`. Verifies that roles are statically constructible and destructible. Produces procedural `defproc` code.
  - **Diffie-Hellman Algebra**: `cpsa4roletran` does not support Diffie-Hellman exponentiation (`exp`, `gen`, `mul`). The gate branches to `~/.cabal/bin/cpsa4 -l 1 <stem>.scm`, validating role well-formedness, variable scopes, and sort rules directly.

### Stage 5: Self-Healing Diagnostic Repair
- **File**: `src/verification_engine/compiler_diagnostic_repair.py`
- **Trigger**: Any failure in Stage 4 (roletran) or Stage 6 (CPSA build).
- **Mechanism**:
  1. **Cycle Detection**: MD5 hashes candidate ASTs. If an identical AST was previously generated, flags an oscillation and boosts temperature to 0.4.
  2. **RAG Query Formulation**: `LLM_QUERY_MODEL` (Gemini Flash Lite) abstracts concrete variable names from the error string into formal CPSA manual concepts.
  3. **Corpus Search**: Queries `manual_chunks.jsonl` using hybrid BM25 + dense retrieval for authoritative rule snippets.
  4. **AST Mutation**: `LLM_REPAIR_MODEL` (DeepSeek-Chat) modifies the AST to fix the defect.
  5. **Loop**: Re-emits to Stage 3 and re-tests. Allowed up to 50 attempts before halting.

### Stage 6 & 7: Formal Verification & Shape Derivation
- **File**: `src/verification_engine/mitre_build_orchestrator.py`
- **Process**:
  1. Initializes build directory using `cpsa4init` (generates `Makefile` and `cpsa4.mk`).
  2. Executes `make <stem>_shapes.xhtml`.
  3. GNU Make invokes:
     - `cpsa4 <stem>.scm -o <stem>.txt`: Computes the strand space search tree.
     - `cpsa4shapes <stem>.txt -o <stem>_shapes.txt`: Filters unrealized skeletons down to minimal shapes.
     - `cpsa4graph <stem>_shapes.txt -o <stem>_shapes.xhtml`: Renders interactive SVG graphs of realized bilateral authentication shapes.
  4. Parses `shapes_count` to verify that at least one shape was realized.

---

## 3. Real-Time Event Bus & Web Visualizer

### Global Event Bus (`src/pipeline_events.py`)
- Thread-safe singleton `GLOBAL_EVENT_BUS`.
- Events carry: `event_id`, `timestamp`, `event_type`, `stage`, `data`.
- Core event types:
  - `pipeline_started`, `pipeline_completed`
  - `stage_started`, `stage_completed`, `stage_failed`
  - `slice_ready` (metadata, line counts, section IDs)
  - `rag_retrieval` (queries, hits, snippet previews)
  - `repair_attempt` (attempt index, cycle flag, diagnostic text)
  - `build_completed` (shape count, links to XHTML artifacts)

### Asynchronous Server (`src/visualizer/server.py`)
- Built on `aiohttp`. Runs in a background thread during pipeline execution.
- Default port: `8080`.
- Endpoints:
  - `GET /`: Serves single-page dashboard (`static/index.html`).
  - `GET /api/events`: Live Server-Sent Events (SSE) feed.
  - `GET /api/history`: Full replay of past events for clients connecting mid-run.
  - `GET /api/artifact?path=...`: Serves emitted Scheme files and rendered SVG/XHTML shape graphs.
