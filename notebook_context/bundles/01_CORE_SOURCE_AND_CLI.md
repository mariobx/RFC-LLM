# RFC-LLM Core Source Code, Compilers, IR & CLI Entrypoints

> Tier 2 — Complete core synthesis and Phase 3 <think> curation pipeline (`src/` and `prompts/`), including YAML-frontmatter prompt templates, RFC document ingestion, order-sorted message algebra intermediate representation (IR), constrained protocol extraction, CPSA 4.4.9 JSON/Scheme code generation, roletran & compiler self-healing verification engine, trajectory & quality-tier exporter, DSPy hindsight `<think>` synthesizer (`src/generate_think/`), virtualized multi-RFC web visualizer, root `rfc-llm` and `rfc-think` CLI entrypoints, and the benchmark EDHOC input RFC.

*Generated: 2026-11-05 18:27:58 UTC · Git: `main` @ `955b498002b7` · Tier: Tier 2 — Core Source Code & CLI Entrypoints · Files: 48 · Estimated Tokens: ~242,120*

## Table of Contents

- [`prompts/01_applicability_gate.md`](#prompts01-applicability-gatemd)
- [`prompts/02_section_router.md`](#prompts02-section-routermd)
- [`prompts/03_protocol_extraction.md`](#prompts03-protocol-extractionmd)
- [`prompts/04_schema_self_correction.md`](#prompts04-schema-self-correctionmd)
- [`prompts/05_rag_query_formulation.md`](#prompts05-rag-query-formulationmd)
- [`prompts/06_compiler_repair.md`](#prompts06-compiler-repairmd)
- [`prompts/07_think_token_synthesizer.md`](#prompts07-think-token-synthesizermd)
- [`prompts/README.md`](#promptsreadmemd)
- [`refrences/all_RFCs/rfc9528.txt`](#refrencesall-rfcsrfc9528txt)
- [`rfc-llm`](#rfc-llm)
- [`rfc-think`](#rfc-think)
- [`src/__init__.py`](#src-init-py)
- [`src/code_generation/__init__.py`](#srccode-generation-init-py)
- [`src/code_generation/cpsa_json_serializer.py`](#srccode-generationcpsa-json-serializerpy)
- [`src/code_generation/cpsa_scheme_emitter.py`](#srccode-generationcpsa-scheme-emitterpy)
- [`src/cost_tracker.py`](#srccost-trackerpy)
- [`src/document_ingestion/__init__.py`](#srcdocument-ingestion-init-py)
- [`src/document_ingestion/handshake_section_router.py`](#srcdocument-ingestionhandshake-section-routerpy)
- [`src/document_ingestion/protocol_applicability_gate.py`](#srcdocument-ingestionprotocol-applicability-gatepy)
- [`src/document_ingestion/rfc_header_filter.py`](#srcdocument-ingestionrfc-header-filterpy)
- [`src/document_ingestion/rfc_toc_parser.py`](#srcdocument-ingestionrfc-toc-parserpy)
- [`src/document_ingestion/verbatim_section_slicer.py`](#srcdocument-ingestionverbatim-section-slicerpy)
- [`src/generate_think/__init__.py`](#srcgenerate-think-init-py)
- [`src/generate_think/cli.py`](#srcgenerate-thinkclipy)
- [`src/generate_think/dspy_think_synthesizer.py`](#srcgenerate-thinkdspy-think-synthesizerpy)
- [`src/generate_think/think_schema.py`](#srcgenerate-thinkthink-schemapy)
- [`src/intermediate_representation/__init__.py`](#srcintermediate-representation-init-py)
- [`src/intermediate_representation/algebraic_sorts.py`](#srcintermediate-representationalgebraic-sortspy)
- [`src/intermediate_representation/cpsa_grammar.py`](#srcintermediate-representationcpsa-grammarpy)
- [`src/intermediate_representation/protocol_syntax_tree.py`](#srcintermediate-representationprotocol-syntax-treepy)
- [`src/logging_config.py`](#srclogging-configpy)
- [`src/main_pipeline_orchestrator.py`](#srcmain-pipeline-orchestratorpy)
- [`src/pipeline.py`](#srcpipelinepy)
- [`src/pipeline_events.py`](#srcpipeline-eventspy)
- [`src/prompt_loader.py`](#srcprompt-loaderpy)
- [`src/rag_retriever_client.py`](#srcrag-retriever-clientpy)
- [`src/semantic_extraction/__init__.py`](#srcsemantic-extraction-init-py)
- [`src/semantic_extraction/constrained_protocol_extractor.py`](#srcsemantic-extractionconstrained-protocol-extractorpy)
- [`src/system_config.py`](#srcsystem-configpy)
- [`src/verification_engine/__init__.py`](#srcverification-engine-init-py)
- [`src/verification_engine/compiler_diagnostic_repair.py`](#srcverification-enginecompiler-diagnostic-repairpy)
- [`src/verification_engine/mitre_build_orchestrator.py`](#srcverification-enginemitre-build-orchestratorpy)
- [`src/verification_engine/roletran_executability_gate.py`](#srcverification-engineroletran-executability-gatepy)
- [`src/verification_engine/snowball_autopsy.py`](#srcverification-enginesnowball-autopsypy)
- [`src/verification_engine/trajectory_metadata_exporter.py`](#srcverification-enginetrajectory-metadata-exporterpy)
- [`src/visualizer/__init__.py`](#srcvisualizer-init-py)
- [`src/visualizer/server.py`](#srcvisualizerserverpy)
- [`src/visualizer/static/index.html`](#srcvisualizerstaticindexhtml)

---

### `prompts/01_applicability_gate.md`

*sha256:`9f63d4594e6d` · 32 lines · 2.7 KB (~680 tokens) · lang:`markdown`*

```markdown
---
# Stage 1c: Protocol Applicability Gatekeeper
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: strata/unsloth-iq4_xs
timeout: 900
max_tokens: 16384
---
You are a formal methods expert in cryptographic protocol verification using MITRE CPSA 4.4.9.
Your task is to analyze an IETF RFC's metadata and Table of Contents to determine if it specifies an interactive cryptographic security protocol.

ELIGIBLE for CPSA:
- Self-contained interactive protocols between two or more principals that define their own multi-message cryptographic exchange or handshake in this RFC.
- Employs cryptographic primitives directly in the protocol flights defined by this document: keys (symmetric or asymmetric), nonces, digital signatures, MACs/hashes, or Diffie-Hellman exponent groups.
- Focuses on authentication, secrecy, key establishment, or secure channel setup.

INELIGIBLE for CPSA (Reject with `"is_cryptographic_protocol": false`):
- Network transport, routing, mobility, or NAT/relay protocols (e.g., TURN/STUN TCP allocations, NEMO basic support, MIPv4 VPN traversal) with no cryptographic handshake defined in this document.
- Application, conferencing, media, or HTTP-API protocols (e.g., BFCP floor control, HELD location dereference, HTTP SET polling) that merely rely on lower-layer TLS/DTLS/HTTPS/IPsec for transport security without defining their own cryptographic handshake.
- Link/frame encryption formats or deployment profiles (e.g., radio link frame encryption, IPsec/IKE cipher profiles) that delegate interactive key management to an external specification (such as IKE [RFC2409] or TLS) without specifying the interactive handshake messages in this document.
- Incremental parameter, flag, PRF/KDF-input tweaks, or declarative HTTP headers (e.g., TCP-AO NAT traversal flags, additional TLS master-secret inputs, HTTP Public Key Pinning headers) that modify local computation or caching without defining an interactive cryptographic exchange.
- Cleartext password / UI prompt framing protocols (e.g., NNTP `AUTHINFO USER/PASS`, SSH `keyboard-interactive` prompt framing) that define zero cryptographic operations of their own.
- Static data formats, ASN.1 management information bases, XML schemas, database definitions, administrative memos, requirements catalogs, problem statements, or surveys without self-contained cryptographic message flows.

CRITICAL: Return a populated JSON instance, NOT the schema definition.
Example output format:
{
  "is_cryptographic_protocol": true,
  "protocol_name": "Protocol Name",
  "participating_principals": ["Alice", "Bob"],
  "has_keys_or_nonces": true,
  "rationale": "Clear concise justification"
}
```

---

### `prompts/02_section_router.md`

*sha256:`918d738d3659` · 23 lines · 1.8 KB (~464 tokens) · lang:`markdown`*

```markdown
---
# Stage 1d: Handshake & Exchange TOC Section Router
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: strata/unsloth-iq4_xs
timeout: 900
max_tokens: 16384
---
You are a protocol analyst reading an RFC's Table of Contents.
Your task is to identify the EXACT section numbers that define the complete cryptographic message exchange, handshake flights, and cryptographic payload/key/MAC structures between principals.

Guidelines:
- Prefer selecting top-level or parent exchange sections (e.g. `"2"`, `"3"`, `"4"`) rather than cherry-picking 1 or 2 isolated leaf subsections—selecting a parent section automatically includes its introductory ladder diagram plus all nested subsections (`3.1`, `3.2`, etc.).
- If a multi-party or multi-phase protocol splits its message flows across multiple sections (e.g., `3. Client-AS Communication` and `4. Client-RS Communication`, or `2. Operation` and `4. Packet Types`), include ALL sections that define the exchange flights!
- ALWAYS include sections that define the cryptographic key derivation, signature/MAC calculation, or encrypted payload structure alongside the message flow sections.
- Do NOT select introductory terminology, conventions, IANA registries, or acknowledgements.
- Output ONLY bare numerical and dotted section IDs (e.g., `"3"`, `"4.1"`, `"7.1.2"`, or `"App-A"` for appendices). NEVER prefix section IDs with `#`, `Section`, or `Sec.`, and NEVER include section titles inside `selected_section_ids`.

CRITICAL: Return a populated JSON instance object, NOT the JSON Schema definition and NOT wrapped inside a `"properties"` key.
Example output format:
{
  "selected_section_ids": ["3", "4"],
  "rationale": "Section 3 defines the Client-to-AS token exchange and Section 4 defines the Client-to-RS nonce and OSCORE setup exchange."
}
```

---

### `prompts/03_protocol_extraction.md`

*sha256:`0dbebc786f8f` · 109 lines · 12.7 KB (~3,256 tokens) · lang:`markdown`*

```markdown
---
# Stage 2: JSON CPSA Generation (Constrained Protocol Semantic Extraction)
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: strata/unsloth-iq4_xs
timeout: 3600
max_tokens: 65536
---
You are a formal methods expert in cryptographic protocol specification for MITRE CPSA 4.4.9.
Your task is to analyze the provided verbatim RFC specification text and extract a complete, mathematically rigorous CPSAProtocolSpecification that is strictly 1-to-1 with the RFC.

ABSOLUTE 1-TO-1 VERBATIM RFC GROUNDING MANDATE (ZERO HALLUCINATION):
- STAGE 2 FALSE-POSITIVE / UNVERIFIABLE PROTOCOL BAILOUT (`"is_verifiable_protocol": false`):
  Before extracting any roles, verify that the provided Verbatim RFC Exchange Specification actually defines a self-contained, interactive multi-message cryptographic or authenticated exchange between two or more principals.
  If the provided RFC excerpt:
  (a) contains NO interactive message flights (e.g., only terminology/scope, local flag/KDF tweaks like TCP-AO-NAT or TLS master-secret input tweaks, static HTTP response headers like HPKP, `[see PostScript]` figure placeholders, or 1-way link-layer frame bit layouts), OR
  (b) delegates the entire key exchange / authentication handshake to an external specification (e.g., "use IKE [RFC2409]" or "use TLS [RFC5246]") without defining the interactive cryptographic flights in this excerpt, OR
  (c) is a plaintext application, conferencing, relay, or UI-prompt protocol (e.g., BFCP floor control, TURN TCP allocations, HELD HTTP GET, HTTP SET polling, NNTP cleartext `AUTHINFO USER/PASS`, or SSH `keyboard-interactive` prompt framing) that defines zero cryptographic operations of its own,
  then DO NOT invent or force a protocol! Immediately return:
  `"is_verifiable_protocol": false`, `"ineligibility_reason": "<concise explanation>"`, `"roles": []`, `"skeletons": []`.
- Every role (`defrole`), message flight (`send`/`recv`), variable (`vars`), and cryptographic operation (`enc`, `hash`, `ltk`, `pubk`, `privk`, `exp`) MUST correspond 1-to-1 to the provided Verbatim RFC Exchange Specification.
- NEVER invent, assume, or hallucinate roles, message flights, nonces, keys, or secrets that are not explicitly specified in the provided RFC excerpt.
- NEVER substitute generic textbook terms (do NOT inject `client_random`, `server_random`, or `premaster_secret` unless the RFC is literally TLS). Name every variable after the exact field, attribute, header, or key terminology used in the RFC text, and cite the exact RFC field name in `rfc_field`.
- If the RFC specifies a 2-message exchange, model 2 messages; if it specifies 4 messages, model 4 messages. Do NOT add or remove protocol flights.
- MANDATORY CRYPTOGRAPHIC STRUCTURE (NO DEGENERATE PLAINTEXT-ONLY PROTOCOLS): Whenever `"is_verifiable_protocol": true`, your specification MUST model the RFC's cryptographic flights (such as `CertificateVerify`, `Finished`, `ClientKeyExchange`, `Signature`, `MAC`, `HMAC`, `AUTH`, encrypted payloads, or Diffie-Hellman key agreement) using CPSA cryptographic operators (`["enc", ..., ["privk", ...]]`, `["enc", ..., ["pubk", ...]]`, `["enc", ..., ["ltk", ...]]`, `["hash", ...]`, `["exp", ...]`) and declare the corresponding uncompromised keys in `non_originating`. NEVER flatten cryptographic handshake flights into bare plaintext `data` variables—doing so allows the Dolev-Yao adversary to forge every flight by itself in a degenerate 1-strand shape!
- If the RFC exchange only performs authentication (e.g., via keyed hash/MAC or digital signature) and does NOT transmit or establish a confidential secret or session key, set `primary_secrecy_goals: []` and do NOT create a `deflistener` skeleton. NEVER invent a fake secret variable or place a pre-shared `non-orig` key inside `deflistener`.

CRITICAL MITRE CPSA 4.4.9 MANUAL GROUNDING (Chapters 2, 3, 4, 10 - Tables 10.1 through 10.6):
Every extracted construct must strictly obey the MITRE CPSA formal syntax:

1. Cryptographic Message Algebra (Tables 10.2, 10.4, 10.5):
   - Select "basic" for symmetric/asymmetric protocols, or "diffie-hellman" if modular exponentiation or Diffie-Hellman groups are used.
   - Diffie-Hellman Sorts (Section 4.2 & 10.3.2): Fresh randomly generated private exponents MUST be declared with sort "rndx" (atomic exponents) and placed in "unique_generated" (uniq-gen). Sort "expt" is reserved for compound expressions or unconstrained received values. NEVER declare fresh originating exponents as "expt" or place them in "unique_originating".
   - Under "basic" algebra, Diffie-Hellman sorts ("rndx", "expt", "base") and operators ("exp", "gen", "mul", "rec", "one", "bltk") are strictly forbidden.

2. Term Syntax & Structure (Tables 10.3 & 10.5):
   - Formal Term Grammar:
     term ::= id | "\"tag_literal\"" | (op term+)
   - STRICT ATOM ENFORCEMENT: A term is strictly a declared variable identifier string (e.g. "client_random", "session_key"), a quoted string constant tag literal (e.g. "\"SAKE_CHALLENGE\"") for fixed protocol message types/opcodes/labels, or a prefix operator list [op, ...args]. Do NOT use bare JSON integers for message types.
   - ABSOLUTE NEGATIVE CONSTRAINT: A term is NEVER a dictionary or object (e.g. NEVER {"name": "...", "description": "..."}).
     Variables MUST BE DECLARED in the role's 'variables' list. In 'message_term', 'inputs', 'outputs', and 'unique_originating', variables are referenced ONLY by their plain string name atom (e.g. "session_key", "client_random").
   - OPAQUE FORWARDING & SIGNATURE VERIFICATION IN `recv` (`cpsa4roletran` Rule):
     * In `cpsa4roletran`, any role that receives an explicit `["enc", payload, key]` MUST possess the inverse decryption key `inv(key)` in its `inputs` or prior receptions!
     * Therefore, a role must NEVER place `["enc", ..., ["pubk", "peer_name"]]` inside a `recv` event if it does not hold `["privk", "peer_name"]` (e.g., an intermediate router forwarding a blob encrypted for a core/initiator, or a client receiving a token encrypted under an issuer's public key). Instead, model any encrypted subtree that a role cannot decrypt as an opaque variable of sort `"mesg"` in that role's `variables` and `recv`/`send` events!
   - COMPLETE BIDIRECTIONAL TRACES & KDF TRANSCRIPT BINDING:
     * Every initiator role that sends a request in a request/response protocol MUST also include the `recv` event for the responder's reply (never leave an initiator role as a 1-event `send`-only stub when the responder sends a reply).
     * When the RFC derives a session key or MAC from negotiated handshake fields (cipher suites, nonces, identities), bind those fields inside `["hash", ...]` rather than replacing the derived key with an unbound static `skey` variable.
   - Authorized Operator Signatures:
     * ["enc", term1, ..., termN, encryption_key] (Table 10.3): One or more payload terms followed by the encryption key as the LAST element. By Equation 10.1, the encryption_key must NEVER be a variable of sort "mesg".
     * ["hash", term1, ...] (Table 10.3): One-way hash digest.
     * ["cat", term1, term2, ...] (Table 10.3): Concatenation of terms.
     * ["pubk", principal_name] or ["pubk", tag_string, principal_name] (Table 10.3): Public key of a principal (sort "name").
     * ["privk", principal_name] or ["privk", tag_string, principal_name] (Table 10.3): Private key of a principal (sort "name").
     * ["invk", akey_var] (Table 10.3): Inverse of an asymmetric key variable (sort "akey").
     * ["ltk", principal1, principal2] (Table 10.3): Long-term shared symmetric key between two principals (sort "name").
     * ["bltk", principal1, principal2] (Table 10.5): Bidirectional long-term key (diffie-hellman only).
     * ["exp", base, expt] (Table 10.5): Exponentiation, e.g. ["exp", ["gen"], "x"] (diffie-hellman only).
     * ["gen"] (Table 10.5): 0-ary generator constant (diffie-hellman only).
     * ["mul", expt1, expt2] (Table 10.5): Multiplication of exponents (diffie-hellman only).
     * ["rec", expt] (Table 10.5): Multiplicative inverse of exponent (diffie-hellman only).
     * ["one"] (Table 10.5): 0-ary unit exponent constant (diffie-hellman only).

3. Principal Roles & Executability Invariants (Tables 10.1 & 10.6, cpsa4roletran):
   - Variable Naming: Full self-explanatory semantic identifiers from the RFC (e.g. "client_identity", "client_random", "server_random", "session_key", "handshake_channel"). Never use single-letter abbreviations.
   - Populated Metadata: 'description' and 'rfc_field' must be populated for every variable.
   - Sort Mapping (Allowed role/skeleton variable sorts):
     * "name": principal identifiers
     * "text": fresh nonces and tokens
     * "data": arbitrary secrets, premaster secrets, or session payloads
     * "skey": symmetric encryption keys (keys used in ["enc", ..., key] for symmetric encryption MUST be sort "skey")
     * "akey": asymmetric keys
     * "chan": communication channels (every role must declare a channel variable, e.g. "handshake_channel")
     * "rndx": fresh Diffie-Hellman private exponents (diffie-hellman algebra only)
     * First-order logic sorts ("strd", "indx", "fact") are strictly forbidden in role or skeleton 'variables'.
   - Trace Events:
     * direction: "send" or "recv" (or "load"/"stor" for stateful memory locations)
     * channel: e.g. "handshake_channel"
     * message_term: prefix term tree using valid operators or plain identifier atoms.
   - ROLETRAN EXECUTABILITY RULES:
     * Every variable in "inputs", "outputs", and "unique_originating" MUST appear in that role's trace events.
     * "inputs": Basic values and channels known prior to execution (e.g. "handshake_channel", pre-shared keys). Must include all channel variables used in the trace. Must NEVER contain any "unique_originating" value.
     * "outputs": Established return terms (e.g. negotiated session tokens). Must NEVER repeat an "inputs" variable.
     * "unique_originating": Fresh nonces or secrets (sort "text", "data", "skey", "akey") generated and first sent by this role.

4. Primary Secrecy & Confidentiality Goals (1-to-1 with RFC):
   - If and ONLY if the RFC exchange transmits or establishes a confidential secret or session key, list that RFC variable in `primary_secrecy_goals`.
   - If the RFC exchange is authentication-only and does NOT establish or transmit a confidential secret, set `primary_secrecy_goals: []`. NEVER place a pre-shared/long-term `non_originating` key into `primary_secrecy_goals` or `listeners` (in CPSA, placing a `non-orig` key in `deflistener` is a fatal compiler error: `Skeleton not well formed: non-orig <key> carried`).

5. Point-of-View Preskeletons (Chapters 3 & 6):
   - POV Skeleton 1 (Initiator POV - Realized Handshake Shape):
     * strands: [defstrandmax for initiator role, with `variable_bindings` explicitly mapping every role variable `(var -> var)`]
     * non_originating: uncompromised long-term/private keys from the RFC
     * unique_originating: ONLY unencrypted fresh nonces (do NOT repeat `unique_originating` atoms already declared in the role's `defrole`, or CPSA will reject encrypted secrets with `uniq-orig <var> not carried`)
     * listeners: [] (STRICTLY EMPTY: never include deflistener in pure POV skeletons, or CPSA cannot realize the bilateral shape)
   - POV Skeleton 2 (Responder POV - Mutual Authentication):
     * strands: [defstrandmax for responder role, with `variable_bindings` explicitly mapping every role variable `(var -> var)`]
     * non_originating: uncompromised long-term/private keys from the RFC
     * unique_originating: [] (rely on the role's `unique_originating` declarations)
     * listeners: [] (STRICTLY EMPTY)
   - Secrecy Skeleton 3 (Confidentiality Proof — ONLY when the RFC establishes/transmits a confidential secret):
     * strands: [defstrandmax for the role that originates or holds the secret, with `variable_bindings` mapping every role variable `(var -> var)`]
     * listeners: [the confidential secret established/transmitted in the RFC] (Yes: in MITRE CPSA, `(deflistener <secret>)` MUST reside inside the same Secrecy `defskeleton` alongside `(defstrandmax <Role> ...)` so that an honest strand originates the secret while CPSA tests whether the adversary can learn it!)
     * non_originating: uncompromised long-term/private keys (must NEVER overlap with `listeners`)
     * unique_originating: [] (rely on the role's `unique_originating` declarations)

6. State-Space Termination & Directional Separation (15s CPSA4 Limit):
   - NEVER give a Request `(enc ...)` / `(hash ...)` and a Response `(enc ...)` / `(hash ...)` the exact same untagged tuple arity and key structure!
   - Include the actual RFC message type, header, or opcode field (or distinct RFC message header sort `data` vs `text`) inside each flight so CPSA4 cannot unify a Response with a Request in an infinite loop.

Return ONLY a valid JSON object matching the requested CPSAProtocolSpecification schema.
```

---

### `prompts/04_schema_self_correction.md`

*sha256:`46077c8e92f4` · 20 lines · 1.6 KB (~418 tokens) · lang:`markdown`*

```markdown
---
# Stage 2 (Retry): 1-Shot Schema & Grammar Self-Correction
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: strata/unsloth-iq4_xs
timeout: 3600
max_tokens: 65536
---
Your previous JSON output failed MITRE CPSA 4.4.9 schema and scoping validation with the following errors:
{validation_error}

CRITICAL MITRE CPSA MANUAL GROUNDING RULES (Chapter 10, Tables 10.1 - 10.6):
1. In 'message_term', terms MUST be plain string identifier atoms (e.g. 'client_random', 'session_key'), quoted string tag literals (e.g. '"\"MSG_TYPE\""'), or prefix lists like ['enc', payload, key].
   NEVER place variable objects or dictionaries inside message_term!
2. In ['enc', ...], the encryption key is ALWAYS the LAST element in the list, and must NEVER have sort 'mesg' (Equation 10.1).
3. In ['pubk', ...] and ['privk', ...], 1-arg form is ['pubk', principal_name] and 2-arg form is ['pubk', tag_string, principal_name].
4. Every variable in 'inputs', 'outputs', and 'unique_originating' MUST be sent or received in the role's trace! No 'unique_originating' term may appear in 'inputs', and no 'inputs' variable may appear in 'outputs'.
5. Diffie-Hellman fresh exponents must be sort 'rndx' and placed in 'unique_generated' (uniq-gen). Under 'basic' algebra, Diffie-Hellman sorts ('rndx', 'expt', 'base') and operators ('exp', 'gen', 'mul', 'rec', 'one', 'bltk') are strictly forbidden.
6. Keep role-only keywords ('trace', 'inputs', 'outputs') strictly inside roles and preskeleton-only keywords ('strands', 'listeners', 'precedes', 'leadsto') strictly inside skeletons.

Return ONLY the corrected, fully valid JSON object.
```

---

### `prompts/05_rag_query_formulation.md`

*sha256:`893fc10d2a84` · 36 lines · 2.8 KB (~705 tokens) · lang:`markdown`*

````markdown
---
# Stage 5 & 6: Agentic CPSA Knowledge Base Investigator & Diagnostic Searcher
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: strata/unsloth-iq4_xs
timeout: 900
max_tokens: 16384
---
You are the Agentic CPSA 4.4.9 Knowledge Base Investigator for RFC-LLM.
Your task is to inspect a failing `CPSAProtocolSpecification` AST summary, the compiler/solver diagnostic (`cpsa4roletran` or `cpsa4`), and the Master Table of Contents of the CPSA Knowledge Base (`refrences/cpsa_kb/`), then invoke the available Knowledge Base tools to retrieve the exact formal CPSA rules and working `.scm` examples needed by the Repair Model.

AVAILABLE KNOWLEDGE BASE TOOLS:
1. `read_section`: Open any section directly by `section_id` from `01_core_rules/`, `02_manuals/`, or `04_examples_catalog/`.
   Example: `{"tool": "read_section", "section_id": "01_core_rules/07_compiler_and_solver_error_catalog#..."}`
2. `search_cpsa_docs`: Run a DSL-BM25 + neural Cross-Encoder search over all CPSA rules and manuals.
   Important: Abstract away protocol-specific variable names or file paths (never include concrete RFC identifiers like `client_random` or `.scm:72:6`). Use formal CPSA keywords (`uniq-orig`, `uniq-gen`, `rndx`, `expt`, `inputs`, `outputs`, `destructured`, `non-orig`, `deflistener`, `chan`, `locn`, `pubk`, `invk`, `ltk`).
   Example: `{"tool": "search_cpsa_docs", "query": "Received term cannot be fully destructured roletran inputs decryption key", "category": "all"}`
3. `find_scm_examples`: Filter the 151 official MITRE `.scm` protocol files by algebra, operators, and keywords.
   Example: `{"tool": "find_scm_examples", "algebra": "diffie-hellman", "operators": ["exp", "gen"], "keywords": ["uniq-gen"]}`
4. `read_scm_example`: Read a specific `.scm` example file verbatim.
   Example: `{"tool": "read_scm_example", "filename": "uniq-gen-test.scm"}`

OUTPUT FORMAT (Respond strictly with a valid JSON object):
```json
{
  "thought": "Brief analysis of why the AST failed the compiler check.",
  "ast_root_cause": "Pinpoint the exact role, variable, trace event, or skeleton field in the failing AST causing the diagnostic.",
  "actionable_fix": "Exact JSON AST field edit required in CPSAProtocolSpecification.",
  "tool_calls": [
    {"tool": "read_section", "section_id": "01_core_rules/07_compiler_and_solver_error_catalog"},
    {"tool": "search_cpsa_docs", "query": "roletran Received term cannot be fully destructured inputs key"},
    {"tool": "find_scm_examples", "algebra": "basic", "operators": ["enc", "invk"]}
  ],
  "is_final": false
}
```
If you are only given a single compiler diagnostic without a TOC map (legacy single-query mode), output a 3-to-6 word plain text CPSA search query abstracting away concrete variable names and file paths.
````

---

### `prompts/06_compiler_repair.md`

*sha256:`29fa722cf12e` · 66 lines · 10.1 KB (~2,571 tokens) · lang:`markdown`*

```markdown
---
# Stage 5 & 6: RAG-Guided Compiler Self-Healing Repair
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: strata/unsloth-iq4_xs
timeout: 3600
max_tokens: 65536
---
You are a formal methods expert in debugging and repairing MITRE CPSA 4.4.9 protocol specifications.
You are given a failing CPSAProtocolSpecification, the verbatim RFC exchange text, the compiler error diagnostic, and retrieved guidance from the MITRE CPSA reference manual.

Your task is to identify the precise defect causing the compiler or solver failure and return a corrected CPSAProtocolSpecification that remains strictly 1-to-1 with the Verbatim RFC Exchange Specification.

STRICT 1-TO-1 RFC FIDELITY DURING REPAIR (ZERO HALLUCINATION):
- NEVER invent fictional protocol messages, fake nonces, fake keys, or non-RFC roles to silence a compiler error.
- NEVER delete real RFC handshake flights or collapse a multi-message RFC exchange into a 1-line stub.
- NEVER strip out `non_originating` keys, `["enc", ...]` encryption wrappers, or legitimate `deflistener` secrecy skeletons just to silence a `Skeleton not well formed` error! Stripping `non_originating` or `["enc", ...]` allows the Dolev-Yao adversary to forge the entire protocol in a trivial 1-strand shape (`TRIVIAL_SINGLE_STRAND`).
- Every variable, role, and trace event in your repaired specification MUST remain grounded 1-to-1 in the provided Verbatim RFC Exchange Specification.

Common Diagnostics & Fixes:
1. "Undeclared variable <var>" or "Malformed term":
   - Either `<var>` is declared in `inputs`, `outputs`, or `unique_originating` without appearing in the role's `trace`, OR `<var>` is used in `trace` without being declared in `variables`.
   - Fix: If `<var>` is a genuine protocol variable (nonce, key, identity, parameter), declare it in `variables` with its proper CPSA sort (`name`, `text`, `data`, `skey`, `akey`, `mesg`). If `<var>` is a fixed message-type constant or domain-separation label, keep it as a quoted tag literal `"\"<var>\""`—NEVER delete domain-separation labels and NEVER convert distinct message-type constants (like `CHALLENGE` vs `CONFIRM`) into unconstrained `text` variables (which allows CPSA to unify them and create false replay shapes!).
2. "Cannot build <term>":
   - A role attempts to send a term before it has been generated ("unique_originating"), received, or passed as an input ("inputs").
   - Or, a symmetric encryption key in ["enc", payload, key] was mistakenly declared as "data" instead of "skey".
   - Fix: Change key sort to "skey". Add fresh originating terms to "unique_originating". Add known parameters, keys (`["ltk", ...]`, `["pubk", ...]`, `["privk", ...]`), or channels to "inputs".
3. "Received term cannot be fully destructured":
   - A role receives an encrypted message or hash, but lacks the necessary decryption key or preimage in its "inputs", OR a role is trying to pattern-match inside `["enc", ..., ["pubk", "peer_name"]]` / `["enc", ..., ["ltk", "a", "b"]]` without owning the decryption key!
   - Fix:
     * If the receiving role is the intended verifier/recipient of the encrypted message or MAC, ensure its `inputs` list includes the required key (e.g., `["ltk", "client_name", "server_name"]`, `["pubk", "signer_name"]` to verify `["enc", ..., ["privk", "signer_name"]]`, `["privk", "recipient_name"]` to decrypt `["enc", ..., ["pubk", "recipient_name"]]`, or symmetric `skey` variable) and any public parameters needed to reconstruct a received `["hash", ...]`.
     * CRITICAL (`cpsa4roletran` `loopEncr` Rule): If a role (such as a `Client` or an `IntermediateRouter` in a multi-hop protocol) receives an encrypted subterm `["enc", ..., ["pubk", "other_principal"]]` or `["enc", ..., ["ltk", "a", "b"]]` for which it does NOT possess `["privk", "other_principal"]` or `["ltk", "a", "b"]`, `cpsa4roletran` CANNOT equality-check or open that `["enc", ...]` inside `recv`! Replace that undecryptable encrypted subterm in that role's `recv` (and subsequent forwarding `send`) with an opaque variable of sort `"mesg"` (e.g. `encrypted_token: mesg`), while keeping the full `["enc", ...]` term in the originating and final decrypting roles!
     * NEVER replace the final verifier's encrypted term or MAC with an unchecked bare `mesg` variable (such as `["recv", "tesla_mac"]` where `tesla_mac` is sort `mesg`), and NEVER model an Authorization Server token to a Resource Server using only public-key encryption `["enc", ..., ["pubk", "rs_name"]]` without an authenticating key `["ltk", "as_name", "rs_name"]` or signature `["privk", "as_name"]`—anyone (including the adversary) knows `["pubk", "rs_name"]` and can forge an unsigned public-key encryption in 1 strand!
4. Preskeleton Architecture & "Skeleton not well formed: non-orig <key> carried":
   - CRITICAL: Never put 'deflistener' inside pure POV skeletons! A listener on an uncompromised secret causes CPSA to abort without displaying the completed bilateral protocol handshake shape.
   - Separate into pure POV skeletons + (only if the RFC establishes/transmits a confidential secret) a Secrecy POV skeleton:
     * Skeleton 1: Initiator / Client POV (defstrandmax initiator, listeners: [])
     * Skeleton 2: Responder / Server POV (defstrandmax responder, listeners: [])
     * Skeleton 3 (ONLY if the RFC transmits/establishes a confidential secret): Secrecy POV (defstrandmax + deflistener for that transmitted secret)
   - If CPSA reports `Skeleton not well formed: non-orig <key> carried`, it means `<key>` is listed in BOTH `non_originating` (or `pen_non_originating`) AND `listeners` (`deflistener <key>`), or `<key>` is transmitted in the clear! A pre-shared/long-term key in `non_originating` can NEVER be placed in `listeners`. Remove `<key>` from `listeners` and `primary_secrecy_goals` (and if the RFC has no other transmitted confidential session key, omit the listener skeleton altogether—never remove `non_originating` from a long-term key!).
   - If CPSA reports `Skeleton not well formed: a variable in non-orig is not in some trace` or `uniq-orig <var> not carried`:
     * Every `CPSAStrandInstance` in `strands` MUST bind all role variables in `variable_bindings` (`{"client_identity": "client_identity", ...}`) so skeleton-level `non_originating` keys (`["ltk", "client_identity", "server_identity"]`, `["privk", "client_identity"]`) map to variables that actually appear in the strand's trace!
     * Do NOT repeat role-level `unique_originating` secrets inside the `defskeleton`'s `unique_originating` list when those secrets are transmitted under encryption—leave `unique_originating` on the `defrole` and set the `defskeleton`'s `unique_originating: []`. NEVER delete `non_originating` or `deflistener` to work around this error!
5. "Expecting a name" or "Malformed pubk":
   - An asymmetric key constructor like ["pubk", key] or ["privk", key] was passed an asymmetric key variable (sort "akey") instead of a principal identifier (sort "name"), or 2-argument ["pubk", tag, name] had its arguments reversed.
   - Fix: In CPSA, if an asymmetric key variable 'k' is declared with sort "akey", use 'k' and ["invk", 'k'] directly without wrapping in "pubk" or "privk". "pubk" and "privk" only accept variables of sort "name" (or ["pubk", "tag", "name"]).
6. "Uniquely originating value ... does not originate in trace" or "Uniquely originating value in input":
   - A variable declared under "unique_originating" is only transmitted inside a ["hash", ...] one-way digest, is never transmitted, or is also listed in "inputs".
   - Fix: Remove the variable from "unique_originating" (or remove it from "inputs" if it is genuinely fresh). In CPSA, atoms cannot originate inside a one-way hash, and uniquely originating values cannot be inputs.
7. Variable Naming & Metadata Integrity:
   - Preserve all descriptive, domain-specific identifiers (e.g. "client_identity", "server_identity", "client_random", "premaster_secret"). Do NOT downgrade them to single-letter or toy abbreviations like 'a', 'b', 'init', 'resp', 'k'.
   - Preserve and update the 'description' and 'rfc_field' metadata fields.
8. NEVER Emit Foreign Operator "aenc" or "senc":
   - CPSA message algebra has NO "aenc" or "senc" operator!
   - In CPSA, ALL encryption (both symmetric and asymmetric) strictly uses "enc": ["enc", payload, key].
   - If encrypting with a public key, use ["enc", payload, ["pubk", name]] or ["enc", payload, key]. NEVER write "aenc".
9. "timed out after 15 seconds", "Step limit exceeded", or "Strand bound exceeded" (CPSA4 State-Space Explosion / Snowballing):
   - Cause: Tier 1 non-default search orders (`--try-old-strands`, `--check-nonces`, `--reverse-nodes`) already failed to terminate, meaning CPSA's unification engine (`unify_0`) is trapped in an algebraic strand-augmentation loop (shown in the `CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT`).
   - Fix (1-to-1 with the RFC):
     * Inspect the `Top Looping Authentication Test Operations` (`(added-strand <Role> <Height>) <critical-term>`) and `Cloned Unconstrained Variables` in the Snowball Autopsy Report.
     * Distinguish request vs. response `["enc", ...]` and `["hash", ...]` terms using the actual RFC message type, header, opcode, or label fields defined in the RFC (or distinct RFC message header sorts `data` vs `text` and distinct tuple structure from the RFC) so outgoing terms cannot unify with incoming receptions of the same key sort.
     * Add `["neq", "<principal_a>", "<principal_b>"]` to `facts` in every `CPSAPreskeleton` declaring two or more `name` variables to block `A = B` symmetric reflection on `(ltk A B)`.
     * Separate fresh `uniq-orig` nonces (`"sort": "data"`) from predictable RFC identifiers/headers/labels (`"sort": "text"`), and include both communicating `name` variables inside encrypted flights so augmented strands bind to existing principals.
10. "Missing channel" or Channel Omission:
   - Every trace event in `CPSAProtocolRole.trace` MUST include `"channel": "<chan_var>"` where `<chan_var>` is declared with `"sort": "chan"` in `variables` and listed in `inputs`. NEVER drop the channel variable when repairing a trace.

Return ONLY the repaired, valid CPSAProtocolSpecification matching the requested JSON schema.
```

---

### `prompts/07_think_token_synthesizer.md`

*sha256:`3035af57c8c4` · 36 lines · 3.7 KB (~957 tokens) · lang:`markdown`*

```markdown
---
# Phase 3: Hindsight Reasoning (<think>) Synthesizer
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: strata/unsloth-iq4_xs
timeout: 3600
max_tokens: 65536
temperature: 0.2
---
You are a formal methods expert in cryptographic protocol verification using MITRE CPSA 4.4.9.
Your task is to perform **Hindsight Rationalization with Compiler-Feedback Backtracking** (following the STaR, OpenThoughts, and Stanford *s1* reasoning-trace curation paradigms).

You are given:
1. The **Verbatim IETF RFC Exchange Slice** (the exact input a student model will see).
2. The **Verified CPSA Ground-Truth Scaffold** (the verified `final_ast` containing variable/role descriptions and RFC field mappings, any Stage 5 `cpsa4roletran` or Stage 6 `cpsa4` compiler repair trajectories, the formal shape analysis verdicts, and the final `.scm` code).

Your goal is to synthesize the structured internal reasoning steps and a cohesive, first-person `<think>...</think>` monologue that derives the exact verified `.scm` specification from the RFC text.

### CRITICAL RULES FOR SYNTHETIC REASONING TRACES (DO NOT VIOLATE)

1. **STRICT NO-HINDSIGHT-LEAKAGE INVARIANT**:
   - Write strictly from a **forward-looking, first-person problem-solving perspective** starting from the RFC text.
   - **NEVER** mention or imply that you were given `final_ast`, `final_scm`, a reference solution, or compiler logs in advance (e.g., NEVER write *"Looking at the provided AST..."*, *"In the given target .scm..."*, or *"According to the trajectory metadata..."*).
   - Instead, use the ground-truth variable names, sorts, message terms, and skeleton structures as the conclusions you arrive at through your own step-by-step deduction from the RFC prose.

2. **INCORPORATE STRUGGLE, BACKTRACKING, AND COMPILER SELF-CORRECTION**:
   - High-quality reasoning traces do not just state final answers; they check formal CPSA 4.4.9 invariants and catch subtle traps before emitting code.
   - If the Ground-Truth Scaffold includes failed **Stage 5 (`cpsa4roletran`) or Stage 6 (`cpsa4`) repair attempts**, weave those exact pitfalls into `step4_compiler_backtracking_and_invariants` and `full_thinking_monologue` as natural internal self-corrections using explicit cognitive transition markers (`"Wait—let me verify..."`, `"Hold on, if I model X as..."`, `"Let me double-check CPSA's executability rules..."`).
   - Even if the run passed on Attempt 0 with zero repairs, explicitly verify:
     - **Algebra & Sort Rules**: Why `basic` vs `diffie-hellman` algebra is required; why fresh DH exponents sent in `(exp (gen) x)` must be `rndx` with `(uniq-gen x)` while received exponents must be `expt`; why encryption keys in `(enc ...)` cannot have sort `mesg` (Equation 10.1); and why logic sorts (`strd`, `indx`, `fact`) are forbidden in `(vars ...)`.
     - **Role Executability (`cpsa4roletran`)**: Why every received variable must be destructible from keys/terms already known or in `(inputs ...)`, and why `(uniq-orig ...)` / `(uniq-gen ...)` variables must never appear in `(inputs ...)`.
     - **3-POV Skeleton Separation**: Why Participant Point-of-View skeletons (`defstrandmax`) must omit `(deflistener ...)` to test multi-strand authentication cleanly, while confidentiality is tested in a separate secrecy skeleton using `(deflistener ...)` alongside the required `(non-orig ...)` long-term key assumptions.

3. **EXACT IDENTIFIER FIDELITY**:
   - Every role name, variable name, sort, channel name, and S-expression term mentioned in your reasoning MUST match the exact identifiers in the verified `.scm` output so the `<think>...</think>` block transitions seamlessly into the emitted `.scm` code.

Return ONLY a valid JSON object matching the requested `SynthesizedReasoningSteps` schema.
```

---

### `prompts/README.md`

*sha256:`ea819aeb4293` · 39 lines · 4.6 KB (~1,188 tokens) · lang:`markdown`*

````markdown
# RFC-LLM Customizable Prompt Templates & Model Routing (`prompts/`)

This directory contains the externalized system prompts **and per-stage LLM routing configuration** driving every LLM step of the RFC-to-CPSA synthesis and Phase 3 `<think>` generation pipelines.

Each `.md` file starts with a YAML frontmatter block defining its `model`, HTTP `timeout` (seconds), and `temperature`. Environment configuration in `.env` (template: [`.env.example`](../.env.example)) holds **only** API credentials (`GEMINI_API_KEY`, `NOUS_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) and base endpoint URLs (`NOUS_API_BASE`, `OLLAMA_API_BASE`, `STRATA_API_BASE`).

```markdown
---
model: strata/unsloth-iq4_xs
timeout: 180
temperature: 0.0
---
You are a formal methods expert...
```

---

## Prompt Catalog & Pipeline Mapping

| Prompt File | Pipeline Stage | Calling Module | Default Timeout / Temp | Supported Provider Prefixes | Uses RAG? |
|---|---|---|---|---|---|
| [`01_applicability_gate.md`](01_applicability_gate.md) | **Stage 1c**: Document Intake (Applicability Gate) | [`src/document_ingestion/protocol_applicability_gate.py`](../src/document_ingestion/protocol_applicability_gate.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | No |
| [`02_section_router.md`](02_section_router.md) | **Stage 1d**: Document Intake (Handshake Section Router) | [`src/document_ingestion/handshake_section_router.py`](../src/document_ingestion/handshake_section_router.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | No |
| [`03_protocol_extraction.md`](03_protocol_extraction.md) | **Stage 2**: JSON CPSA Generation | [`src/semantic_extraction/constrained_protocol_extractor.py`](../src/semantic_extraction/constrained_protocol_extractor.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | **Yes** (Hybrid RRF) |
| [`04_schema_self_correction.md`](04_schema_self_correction.md) | **Stage 2 (Retry)**: 1-Shot Schema & Grammar Self-Correction | [`src/semantic_extraction/constrained_protocol_extractor.py`](../src/semantic_extraction/constrained_protocol_extractor.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | Via Stage 2 context |
| [`05_rag_query_formulation.md`](05_rag_query_formulation.md) | **Stage 5 & 6**: Self-Healing Loop (RAG Query Formulation) | [`src/verification_engine/compiler_diagnostic_repair.py`](../src/verification_engine/compiler_diagnostic_repair.py) | `15s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | **Yes** (Formulates query) |
| [`06_compiler_repair.md`](06_compiler_repair.md) | **Stage 5 & 6**: Self-Healing Loop (Compiler Diagnostic Repair) | [`src/verification_engine/compiler_diagnostic_repair.py`](../src/verification_engine/compiler_diagnostic_repair.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | **Yes** (Consumes chunks) |
| [`07_think_token_synthesizer.md`](07_think_token_synthesizer.md) | **Phase 3**: Hindsight Reasoning (`<think>`) Synthesizer | [`src/generate_think/dspy_think_synthesizer.py`](../src/generate_think/dspy_think_synthesizer.py) | `180s` / `0.2` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | Trajectory-backed |

---

## Architecture & Live Hot-Reload Guarantees

Prompts and frontmatter metadata are loaded dynamically on every invocation via [`src/prompt_loader.py`](../src/prompt_loader.py):
1. **Zero-Restart Live Hot-Reload**: Editing `model:`, `timeout:`, `temperature:`, or prompt instructions in any `prompts/*.md` file takes effect on the **next LLM call**—even mid-batch—without restarting `./rfc-llm`.
2. **One-Off CLI Overrides**: Passing `--model`, `--router-model`, `--extraction-model`, `--repair-model`, or `--query-model` to `./rfc-llm` (or `--model` to `./rfc-think`) overrides the frontmatter `model:` for that CLI session without modifying `prompts/*.md` on disk.
3. **Frontmatter Stripping & Schema Safety**: [`load_prompt`](../src/prompt_loader.py) strips the `--- ... ---` YAML block before sending the system prompt to LiteLLM, and mandatory Pydantic JSON schemas (`ProtocolApplicabilityReport`, `SectionRoutingDecision`, `CPSAProtocolSpecification`, `SynthesizedReasoningSteps`) are appended automatically in Python.
4. **Template Placeholders**: [`04_schema_self_correction.md`](04_schema_self_correction.md) supports the `{validation_error}` placeholder for 1-shot retry diagnostics.
5. **Resilient Fallback**: If frontmatter fields or `.md` files are missing, [`src/prompt_loader.py`](../src/prompt_loader.py) falls back cleanly to built-in defaults (`GLOBAL_FALLBACK_MODEL = "gemini/gemini-3.5-flash-lite"`).
````

---

### `refrences/all_RFCs/rfc9528.txt`

*sha256:`16b0959ee791` · 4671 lines · 214.1 KB (~54,783 tokens) · lang:`text`*

```text
﻿



Internet Engineering Task Force (IETF)                       G. Selander
Request for Comments: 9528                             J. Preuß Mattsson
Category: Standards Track                                   F. Palombini
ISSN: 2070-1721                                                 Ericsson
                                                              March 2024


               Ephemeral Diffie-Hellman Over COSE (EDHOC)

Abstract

   This document specifies Ephemeral Diffie-Hellman Over COSE (EDHOC), a
   very compact and lightweight authenticated Diffie-Hellman key
   exchange with ephemeral keys.  EDHOC provides mutual authentication,
   forward secrecy, and identity protection.  EDHOC is intended for
   usage in constrained scenarios, and a main use case is to establish
   an Object Security for Constrained RESTful Environments (OSCORE)
   security context.  By reusing CBOR Object Signing and Encryption
   (COSE) for cryptography, Concise Binary Object Representation (CBOR)
   for encoding, and Constrained Application Protocol (CoAP) for
   transport, the additional code size can be kept very low.

Status of This Memo

   This is an Internet Standards Track document.

   This document is a product of the Internet Engineering Task Force
   (IETF).  It represents the consensus of the IETF community.  It has
   received public review and has been approved for publication by the
   Internet Engineering Steering Group (IESG).  Further information on
   Internet Standards is available in Section 2 of RFC 7841.

   Information about the current status of this document, any errata,
   and how to provide feedback on it may be obtained at
   https://www.rfc-editor.org/info/rfc9528.

Copyright Notice

   Copyright (c) 2024 IETF Trust and the persons identified as the
   document authors.  All rights reserved.

   This document is subject to BCP 78 and the IETF Trust's Legal
   Provisions Relating to IETF Documents
   (https://trustee.ietf.org/license-info) in effect on the date of
   publication of this document.  Please review these documents
   carefully, as they describe your rights and restrictions with respect
   to this document.  Code Components extracted from this document must
   include Revised BSD License text as described in Section 4.e of the
   Trust Legal Provisions and are provided without warranty as described
   in the Revised BSD License.

Table of Contents

   1.  Introduction
     1.1.  Motivation
     1.2.  Message Size Examples
     1.3.  Document Structure
     1.4.  Terminology and Requirements Language
   2.  EDHOC Outline
   3.  Protocol Elements
     3.1.  General
     3.2.  Method
     3.3.  Connection Identifiers
     3.4.  Transport
     3.5.  Authentication Parameters
     3.6.  Cipher Suites
     3.7.  Ephemeral Public Keys
     3.8.  External Authorization Data (EAD)
     3.9.  Application Profile
   4.  Key Derivation
     4.1.  Keys for EDHOC Message Processing
     4.2.  Keys for EDHOC Applications
   5.  Message Formatting and Processing
     5.1.  EDHOC Message Processing Outline
     5.2.  EDHOC Message 1
     5.3.  EDHOC Message 2
     5.4.  EDHOC Message 3
     5.5.  EDHOC Message 4
   6.  Error Handling
     6.1.  Success
     6.2.  Unspecified Error
     6.3.  Wrong Selected Cipher Suite
     6.4.  Unknown Credential Referenced
   7.  EDHOC Message Deduplication
   8.  Compliance Requirements
   9.  Security Considerations
     9.1.  Security Properties
     9.2.  Cryptographic Considerations
     9.3.  Cipher Suites and Cryptographic Algorithms
     9.4.  Post-Quantum Considerations
     9.5.  Unprotected Data and Privacy
     9.6.  Updated Internet Threat Model Considerations
     9.7.  Denial of Service
     9.8.  Implementation Considerations
   10. IANA Considerations
     10.1.  EDHOC Exporter Label Registry
     10.2.  EDHOC Cipher Suites Registry
     10.3.  EDHOC Method Type Registry
     10.4.  EDHOC Error Codes Registry
     10.5.  EDHOC External Authorization Data Registry
     10.6.  COSE Header Parameters Registry
     10.7.  Well-Known URI Registry
     10.8.  Media Types Registry
     10.9.  CoAP Content-Formats Registry
     10.10. Resource Type (rt=) Link Target Attribute Values Registry
     10.11. Expert Review Instructions
   11. References
     11.1.  Normative References
     11.2.  Informative References
   Appendix A.  Use with OSCORE and Transfer over CoAP
     A.1.  Deriving the OSCORE Security Context
     A.2.  Transferring EDHOC over CoAP
   Appendix B.  Compact Representation
   Appendix C.  Use of CBOR, CDDL, and COSE in EDHOC
     C.1.  CBOR and CDDL
     C.2.  CDDL Definitions
     C.3.  COSE
   Appendix D.  Authentication-Related Verifications
     D.1.  Validating the Authentication Credential
     D.2.  Identities
     D.3.  Certification Path and Trust Anchors
     D.4.  Revocation Status
     D.5.  Unauthenticated Operation
   Appendix E.  Use of External Authorization Data
   Appendix F.  Application Profile Example
   Appendix G.  Long PLAINTEXT_2
   Appendix H.  EDHOC_KeyUpdate
   Appendix I.  Example Protocol State Machine
     I.1.  Initiator State Machine
     I.2.  Responder State Machine
   Acknowledgments
   Authors' Addresses

1.  Introduction

1.1.  Motivation

   Many Internet of Things (IoT) deployments require technologies that
   are highly performant in constrained environments [RFC7228].  IoT
   devices may be constrained in various ways, including memory,
   storage, processing capacity, and power.  The connectivity for these
   settings may also exhibit constraints, such as unreliable and lossy
   channels, highly restricted bandwidth, and dynamic topology.  The
   IETF has acknowledged this problem by standardizing a range of
   lightweight protocols and enablers designed for the IoT, including
   CoAP [RFC7252], CBOR [RFC8949], and Static Context Header Compression
   (SCHC) [RFC8724].

   The need for special protocols targeting constrained IoT deployments
   extends also to the security domain [LAKE-REQS].  Important
   characteristics in constrained environments are the number of round
   trips and protocol message sizes, which (if kept low) can contribute
   to good performance by enabling transport over a small number of
   radio frames, reducing latency due to fragmentation, duty cycles,
   etc.  Another important criterion is code size, which may be
   prohibitively large for certain deployments due to device
   capabilities or network load during firmware updates.  Some IoT
   deployments also need to support a variety of underlying transport
   technologies, potentially even with a single connection.

   Some security solutions for such settings exist already.  COSE
   [RFC9052] specifies basic application-layer security services
   efficiently encoded in CBOR.  Another example is OSCORE [RFC8613],
   which is a lightweight communication security extension to CoAP using
   CBOR and COSE.  In order to establish good quality cryptographic keys
   for security protocols such as COSE and OSCORE, the two endpoints may
   run an authenticated Diffie-Hellman key exchange protocol, from which
   shared secret keying material can be derived.  Such a key exchange
   protocol should also be lightweight to prevent bad performance in
   case of repeated use, e.g., due to device rebooting or frequent
   rekeying for security reasons or to avoid latencies in a network
   formation setting with many devices authenticating at the same time.

   This document specifies Ephemeral Diffie-Hellman Over COSE (EDHOC), a
   lightweight authenticated key exchange protocol providing good
   security properties including forward secrecy, identity protection,
   and cipher suite negotiation.  Authentication can be based on raw
   public keys (RPKs) or public key certificates and requires the
   application to provide input on how to verify that endpoints are
   trusted.  This specification supports the referencing of credentials
   in order to reduce message overhead, but credentials may
   alternatively be embedded in the messages.  EDHOC does not currently
   support Pre-Shared Key (PSK) authentication as authentication with
   static Diffie-Hellman (DH) public keys by reference produces equally
   small message sizes but with much simpler key distribution and
   identity protection.

   EDHOC makes use of known protocol constructions, such as SIGn-and-MAc
   [SIGMA], the Noise XX pattern [Noise], and Extract-and-Expand
   [RFC5869].  EDHOC uses COSE for cryptography and identification of
   credentials (including COSE_Key, CBOR Web Token (CWT), CWT Claims Set
   (CCS), X.509, and CBOR-encoded X.509 (C509) certificates; see
   Section 3.5.2).  COSE provides crypto agility and enables the use of
   future algorithms and credential types targeting IoT.

   EDHOC is designed for highly constrained settings, making it
   especially suitable for low-power networks [RFC8376] such as Cellular
   IoT, IPv6 over the TSCH mode of IEEE 802.15.4e (6TiSCH), and LoRaWAN.
   A main objective for EDHOC is to be a lightweight authenticated key
   exchange for OSCORE, i.e., to provide authentication and session key
   establishment for IoT use cases such as those built on CoAP [RFC7252]
   involving 'things' with embedded microcontrollers, sensors, and
   actuators.  By reusing the same lightweight primitives as OSCORE
   (CBOR, COSE, and CoAP), the additional code size can be kept very
   low.  Note that while CBOR and COSE primitives are built into the
   protocol messages, EDHOC is not bound to a particular transport.

   A typical setting is when one of the endpoints is constrained or in a
   constrained network and the other endpoint is a node on the Internet
   (such as a mobile phone).  Thing-to-thing interactions over
   constrained networks are also relevant since both endpoints would
   then benefit from the lightweight properties of the protocol.  EDHOC
   could, e.g., be run when a device connects for the first time or to
   establish fresh keys that are not revealed by a later compromise of
   the long-term keys.

1.2.  Message Size Examples

   Examples of EDHOC message sizes are shown in Table 1, which use
   different kinds of authentication keys and COSE header parameters for
   identification, including static Diffie-Hellman keys or signature
   keys, either in CWT/CCS [RFC8392] identified by a key identifier
   using 'kid' [RFC9052] or in X.509 certificates identified by a hash
   value using 'x5t' [RFC9360].  EDHOC always uses ephemeral-ephemeral
   key exchange.  As a comparison, in the case of RPK authentication and
   when transferred in CoAP, the EDHOC message size can be less than 1/7
   of the DTLS 1.3 handshake [RFC9147] with Ephemeral Elliptic Curve
   Diffie-Hellman (ECDHE) and connection ID; see [CoAP-SEC-PROT].

              +===========+================+================+
              |           | Static DH Keys | Signature Keys |
              +===========+==========+=====+==========+=====+
              |           |      kid | x5t |      kid | x5t |
              +===========+==========+=====+==========+=====+
              | message_1 |       37 |  37 |       37 |  37 |
              +-----------+----------+-----+----------+-----+
              | message_2 |       45 |  58 |      102 | 115 |
              +-----------+----------+-----+----------+-----+
              | message_3 |       19 |  33 |       77 |  90 |
              +-----------+----------+-----+----------+-----+
              | Total     |      101 | 128 |      216 | 242 |
              +-----------+----------+-----+----------+-----+

                Table 1: Examples of EDHOC Message Sizes in
                                   Bytes

1.3.  Document Structure

   The remainder of the document is organized as follows: Section 2
   outlines EDHOC authenticated with signature keys; Section 3 describes
   the protocol elements of EDHOC, including formatting of the ephemeral
   public keys; Section 4 specifies the key derivation; Section 5
   specifies message processing for EDHOC authenticated with signature
   keys or static Diffie-Hellman keys; Section 6 describes the error
   messages; Section 7 describes EDHOC support for transport that does
   not handle message duplication; and Section 8 lists compliance
   requirements.  Note that normative text is also used in appendices,
   in particular Appendix A.

1.4.  Terminology and Requirements Language

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
   "OPTIONAL" in this document are to be interpreted as described in
   BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all
   capitals, as shown here.

   Readers are expected to be familiar with the terms and concepts
   described in CBOR [RFC8949], CBOR Sequences [RFC8742], COSE
   Structures and Processing [RFC9052], COSE Algorithms [RFC9053], CWT
   and CCS [RFC8392], and the Concise Data Definition Language (CDDL)
   [RFC8610], which is used to express CBOR data structures.  Examples
   of CBOR and CDDL are provided in Appendix C.1.  When referring to
   CBOR, this specification always refers to Deterministically Encoded
   CBOR, as specified in Sections 4.2.1 and 4.2.2 of [RFC8949].  The
   single output from authenticated encryption (including the
   authentication tag) is called "ciphertext", following [RFC5116].

2.  EDHOC Outline

   EDHOC supports different authentication methods of the ephemeral-
   ephemeral Diffie-Hellman key exchange.  This document specifies
   authentication methods based on signature keys and static Diffie-
   Hellman keys.  This section outlines the signature-key-based method.
   Further details of protocol elements and other authentication methods
   are provided in the remainder of this document.

   SIGn-and-MAc (SIGMA) is a family of theoretical protocols with a
   number of variants [SIGMA].  Like in Internet Key Exchange Protocol
   Version 2 (IKEv2) [RFC7296] and (D)TLS 1.3 [RFC8446] [RFC9147], EDHOC
   authenticated with signature keys is built on a variant of the SIGMA
   protocol, SIGMA-I, which provides identity protection against active
   attacks on the party initiating the protocol.  Also like IKEv2, EDHOC
   implements the MAC-then-Sign variant of the SIGMA-I protocol.  The
   message flow (excluding an optional fourth message) is shown in
   Figure 1.

   Initiator                                                   Responder
   |                                G_X                                |
   +------------------------------------------------------------------>|
   |                                                                   |
   |      G_Y, Enc( ID_CRED_R, Sig( R; MAC( CRED_R, G_X, G_Y ) ) )     |
   |<------------------------------------------------------------------+
   |                                                                   |
   |        AEAD( ID_CRED_I, Sig( I; MAC( CRED_I, G_Y, G_X ) ) )       |
   +------------------------------------------------------------------>|
   |                                                                   |

      Figure 1: MAC-then-Sign Variant of the SIGMA-I Protocol Used by
                             the EDHOC Method 0

   The parties exchanging messages in an EDHOC session are called the
   Initiator (I) and the Responder (R), where the Initiator sends
   message_1 (see Section 3).  They exchange ephemeral public keys,
   compute a shared secret session key PRK_out, and derive symmetric
   application keys used to protect application data.

   *  G_X and G_Y are the Elliptic Curve Diffie-Hellman (ECDH) ephemeral
      public keys of I and R, respectively.

   *  CRED_I and CRED_R are the authentication credentials containing
      the public authentication keys of I and R, respectively.

   *  ID_CRED_I and ID_CRED_R are used to identify and optionally
      transport the credentials of I and R, respectively.

   *  Sig(I; . ) and Sig(R; . ) denote signatures made with the private
      authentication key of I and R, respectively.

   *  Enc(), AEAD(), and MAC() denote encryption, Authenticated
      Encryption with Associated Data, and Message Authentication Code
      -- crypto algorithms applied with keys derived from one or more
      shared secrets calculated during the protocol.

   In order to create a "full-fledged" protocol, some additional
   protocol elements are needed.  This specification adds:

   *  transcript hashes (hashes of message data), TH_2, TH_3, and TH_4,
      used for key derivation and as additional authenticated data,

   *  computationally independent keys derived from the ECDH shared
      secret and used for authenticated encryption of different
      messages,

   *  an optional fourth message giving key confirmation to I in
      deployments where no protected application data is sent from R to
      I,

   *  a keying material exporter and a key update function with forward
      secrecy,

   *  secure negotiation of the cipher suite,

   *  method types, error handling, and padding,

   *  the selection of connection identifiers, C_I and C_R, which may be
      used in EDHOC to identify the protocol state, and

   *  transport of external authorization data.

   EDHOC is designed to encrypt and integrity protect as much
   information as possible.  Symmetric keys and random material used in
   EDHOC are derived using EDHOC_KDF with as much previous information
   as possible; see Figure 6.  EDHOC is furthermore designed to be as
   compact and lightweight as possible, in terms of message sizes,
   processing, and the ability to reuse already existing CBOR, COSE, and
   CoAP libraries.  Like in (D)TLS, authentication is the responsibility
   of the application.  EDHOC identifies (and optionally transports)
   authentication credentials and provides proof-of-possession of the
   private authentication key.

   To simplify for implementors, the use of CBOR, CDDL, and COSE in
   EDHOC is summarized in Appendix C.  Test vectors, including CBOR
   diagnostic notation, are provided in [RFC9529].

3.  Protocol Elements

3.1.  General

   The EDHOC protocol consists of three mandatory messages (message_1,
   message_2, and message_3), an optional fourth message (message_4),
   and an error message, between an Initiator (I) and a Responder (R).
   The odd messages are sent by I, the even by R.  Both I and R can send
   error messages.  The roles have slightly different security
   properties that should be considered when the roles are assigned; see
   Section 9.1.  All EDHOC messages are CBOR Sequences [RFC8742] and are
   defined to be deterministically encoded CBOR as specified in
   Section 4.2.1 of [RFC8949].  Figure 2 illustrates an EDHOC message
   flow with the optional fourth message as well as the content of each
   message.  The protocol elements in the figure are introduced in
   Sections 3 and 5.  Message formatting and processing are specified in
   Sections 5 and 6.

   Application data may be protected using the agreed application
   algorithms (AEAD, hash) in the selected cipher suite (see
   Section 3.6), and the application can make use of the established
   connection identifiers C_I and C_R (see Section 3.3).  Media types
   that may be used for EDHOC are defined in Section 10.8.

   The Initiator can derive symmetric application keys after creating
   EDHOC message_3; see Section 4.2.1.  Protected application data can
   therefore be sent in parallel or together with EDHOC message_3.
   EDHOC message_4 is typically not sent.

   Initiator                                                   Responder
   |                 METHOD, SUITES_I, G_X, C_I, EAD_1                 |
   +------------------------------------------------------------------>|
   |                             message_1                             |
   |                                                                   |
   |       G_Y, Enc( C_R, ID_CRED_R, Signature_or_MAC_2, EAD_2 )       |
   |<------------------------------------------------------------------+
   |                             message_2                             |
   |                                                                   |
   |            AEAD( ID_CRED_I, Signature_or_MAC_3, EAD_3 )           |
   +------------------------------------------------------------------>|
   |                             message_3                             |
   |                                                                   |
   |                           AEAD( EAD_4 )                           |
   |<- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
   |                             message_4                             |

     Figure 2: EDHOC Message Flow Including the Optional Fourth Message

3.2.  Method

   The data item METHOD in message_1 (see Section 5.2.1) is an integer
   specifying the authentication method.  EDHOC currently supports
   authentication with signature or static Diffie-Hellman keys, as
   defined in the four authentication methods: 0, 1, 2, and 3; see
   Table 2.  When using a static Diffie-Hellman key, the authentication
   is provided by a Message Authentication Code (MAC) computed from an
   ephemeral-static ECDH shared secret that enables significant
   reductions in message sizes.  Note that, also in the static Diffie-
   Hellman-based authentication methods, there is an ephemeral-ephemeral
   Diffie-Hellman key exchange.

   The Initiator and Responder need to have agreed on a single method to
   be used for EDHOC; see Section 3.9.

      +===================+====================+====================+
      | Method Type Value | Initiator          | Responder          |
      |                   | Authentication Key | Authentication Key |
      +===================+====================+====================+
      |                 0 | Signature Key      | Signature Key      |
      +-------------------+--------------------+--------------------+
      |                 1 | Signature Key      | Static DH Key      |
      +-------------------+--------------------+--------------------+
      |                 2 | Static DH Key      | Signature Key      |
      +-------------------+--------------------+--------------------+
      |                 3 | Static DH Key      | Static DH Key      |
      +-------------------+--------------------+--------------------+
      |                23 | Reserved           | Reserved           |
      +-------------------+--------------------+--------------------+

               Table 2: Authentication Keys for Method Types

   EDHOC does not have a dedicated message field to indicate the
   protocol version.  Breaking changes to EDHOC can be introduced by
   specifying and registering new methods.

3.3.  Connection Identifiers

   EDHOC includes the selection of connection identifiers (C_I and C_R)
   identifying a connection for which keys are agreed.

   Connection identifiers may be used to correlate EDHOC messages and
   facilitate the retrieval of protocol state during an EDHOC session
   (see Section 3.4) or may be used in applications of EDHOC, e.g., in
   OSCORE (see Section 3.3.3).  The connection identifiers do not have
   any cryptographic purpose in EDHOC and only facilitate the retrieval
   of security data associated with the protocol state.

   Connection identifiers in EDHOC are intrinsically byte strings.  Most
   constrained devices only have a few connections for which short
   identifiers may be sufficient.  In some cases, minimum length
   identifiers are necessary to comply with overhead requirements.
   However, CBOR byte strings -- with the exception of the empty byte
   string h'', which encodes as one byte (0x40) -- are encoded as two or
   more bytes.  To enable one-byte encoding of certain byte strings
   while maintaining CBOR encoding, EDHOC represents certain identifiers
   as CBOR integers on the wire; see Section 3.3.2.

3.3.1.  Selection of Connection Identifiers

   C_I and C_R are chosen by I and R, respectively.  The Initiator
   selects C_I and sends it in message_1 for the Responder to use as a
   reference to the connection in communications with the Initiator.
   The Responder selects C_R and sends it in message_2 for the Initiator
   to use as a reference to the connection in communications with the
   Responder.

   If connection identifiers are used by an application protocol for
   which EDHOC establishes keys, then the selected connection
   identifiers SHALL adhere to the requirements for that protocol; see
   Section 3.3.3 for an example.

3.3.2.  Representation of Byte String Identifiers

   To allow identifiers with minimal overhead on the wire, certain byte
   strings used in connection identifiers and credential identifiers
   (see Section 3.5.3) are defined to have integer representations.

   The integers with one-byte CBOR encoding are -24, ..., 23; see
   Figure 3.

   Integer:  -24  -23  ... -11  ...  -2   -1    0    1  ...  15  ...  23
   Encoding:  37   36  ...  2A  ...  21   20   00   01  ...  0F  ...  17

                  Figure 3: One-Byte CBOR-Encoded Integers

   The byte strings that coincide with a one-byte CBOR encoding of an
   integer MUST be represented by the CBOR encoding of that integer.
   Other byte strings are simply encoded as CBOR byte strings.

   For example:

   *  0x21 is represented by 0x21 (CBOR encoding of the integer -2), not
      by 0x4121 (CBOR encoding of the byte string 0x21).

   *  0x0D is represented by 0x0D (CBOR encoding of the integer 13), not
      by 0x410D (CBOR encoding of the byte string 0x0D).

   *  0x18 is represented by 0x4118 (CBOR encoding of the byte string
      0x18).

   *  0x38 is represented by 0x4138 (CBOR encoding of the byte string
      0x38).

   *  0xABCD is represented by 0x42ABCD (CBOR encoding of the byte
      string 0xABCD).

   One may view this representation of byte strings as a transport
   encoding, i.e., a byte string that parses as the one-byte CBOR
   encoding of an integer (i.e., integer in the interval -24, ..., 23)
   is just copied directly into the message, and a byte string that does
   not is encoded as a CBOR byte string during transport.

      |  Implementation Note: When implementing the byte string
      |  identifier representation, in some programming languages, it
      |  can help to define a new type or other data structure, which
      |  (in its user-facing API) behaves like a byte string but when
      |  serializing to CBOR produces a CBOR byte string or a CBOR
      |  integer depending on its value.

3.3.3.  Use of Connection Identifiers with OSCORE

   For OSCORE, the choice of connection identifier results in the
   endpoint selecting its Recipient ID (see Section 3.1 of [RFC8613])
   for which certain uniqueness requirements apply (see Section 3.3 of
   [RFC8613]).  Therefore, the Initiator and Responder MUST NOT select
   connection identifiers such that it results in the same OSCORE
   Recipient ID.  Since the connection identifier is a byte string, it
   is converted to an OSCORE Recipient ID equal to the byte string.

   Examples:

   *  A connection identifier 0xFF (represented in the EDHOC message as
      0x41FF; see Section 3.3.2) is converted to the OSCORE Recipient ID
      0xFF.

   *  A connection identifier 0x21 (represented in the EDHOC message as
      0x21; see Section 3.3.2) is converted to the OSCORE Recipient ID
      0x21.

3.4.  Transport

   Cryptographically, EDHOC does not put requirements on the underlying
   layers.  Received messages are processed as the expected next message
   according to the protocol state; see Section 5.  If processing fails
   for any reason, then typically an error message is attempted to be
   sent and the EDHOC session is aborted.

   EDHOC is not bound to a particular transport layer and can even be
   used in environments without IP.  Ultimately, the application is free
   to choose how to transport EDHOC messages including errors.  In order
   to avoid unnecessary message processing or protocol termination, it
   is RECOMMENDED to use reliable transport, such as CoAP in reliable
   mode, which is the default transport; see Appendix A.2.  In general,
   the transport SHOULD handle:

   *  message loss,

   *  message duplication (see Section 7 for an alternative),

   *  flow control,

   *  congestion control,

   *  fragmentation and reassembly,

   *  demultiplexing EDHOC messages from other types of messages,

   *  denial-of-service mitigation, and

   *  message correlation (see Section 3.4.1).

   EDHOC does not require error-free transport since a change in message
   content is detected through the transcript hashes in a subsequent
   integrity verification; see Section 5.  The transport does not
   require additional means to handle message reordering because of the
   lockstep processing of EDHOC.

   EDHOC is designed to enable an authenticated key exchange with small
   messages, where the minimum message sizes are of the order
   illustrated in the first column of Table 1.  There is no maximum
   message size specified by the protocol; for example, this is
   dependent on the size of the authentication credentials (if they are
   transported, see Section 3.5).  The encryption of very large content
   in message_2 when using certain hash algorithms is described in
   Appendix G.

   The use of transport is specified in the application profile, which
   in particular, may specify limitations in message sizes; see
   Section 3.9.

3.4.1.  EDHOC Message Correlation

   Correlation between EDHOC messages is needed to facilitate the
   retrieval of the protocol state and security context during an EDHOC
   session.  It is also helpful for the Responder to get an indication
   that a received EDHOC message is the beginning of a new EDHOC
   session, such that no existing protocol state or security context
   needs to be retrieved.

   Correlation may be based on existing mechanisms in the transport
   protocol; for example, the CoAP Token may be used to correlate EDHOC
   messages in a CoAP response and in an associated CoAP request.  The
   connection identifiers may also be used to correlate EDHOC messages.

   If correlation between consecutive messages is not provided by other
   means, then the transport binding SHOULD mandate prepending of an
   appropriate connection identifier (when available from the EDHOC
   protocol) to the EDHOC message.  If message_1 indication is not
   provided by other means, then the transport binding SHOULD mandate
   prepending of message_1 with the CBOR simple value true (0xf5).

   Transport of EDHOC in CoAP payloads is described in Appendix A.2,
   including how to use connection identifiers and message_1 indication
   with CoAP.  A similar construction is possible for other client-
   server protocols.  Protocols that do not provide any correlation at
   all can prescribe prepending of the peer's connection identifier to
   all messages.

   Note that correlation between EDHOC messages may be obtained without
   transport support or connection identifiers, for example, if the
   endpoints only accept a single instance of the protocol at a time and
   execute conditionally on a correct sequence of messages.

3.5.  Authentication Parameters

   EDHOC supports various settings for how the other endpoint's public
   key for authentication may be transported, identified, and trusted.
   We shall use the term "authentication key" to mean key used for
   authentication in general, or specifically, the public key, when
   there is no risk for confusion.

   EDHOC performs the following authentication-related operations:

   *  EDHOC transports information about credentials in ID_CRED_I and
      ID_CRED_R (described in Section 3.5.3).  Based on this
      information, the authentication credentials CRED_I and CRED_R
      (described in Section 3.5.2) can be obtained.  EDHOC may also
      transport certain authentication-related information as external
      authorization data (see Section 3.8).

   *  EDHOC uses the authentication credentials in two ways (see
      Sections 5.3.2 and 5.4.2):

      -  The authentication credential is input to the integrity
         verification using the MAC fields.

      -  The authentication key of the authentication credential is used
         with the Signature_or_MAC field to verify proof-of-possession
         of the private key.

   Other authentication-related verifications are out of scope for EDHOC
   and are the responsibility of the application.  In particular, the
   authentication credential needs to be validated in the context of the
   connection for which EDHOC is used; see Appendix D.  EDHOC MUST allow
   the application to read received information about credentials in
   ID_CRED_R and ID_CRED_I.  EDHOC MUST have access to the
   authentication key and the authentication credential.

   Note that the type of authentication key, the type of authentication
   credential, and the identification of the credential have a large
   impact on the message size.  For example, the Signature_or_MAC field
   is much smaller with a static DH key than with a signature key.  A
   CWT Claims Set (CCS) is much smaller than a self-signed certificate /
   CWT, but if it is possible to reference the credential with a COSE
   header like 'kid', then that is in turn much smaller than a CCS.

3.5.1.  Authentication Keys

   The authentication key MUST be a signature key or a static Diffie-
   Hellman key.  The Initiator and Responder MAY use different types of
   authentication keys, e.g., one uses a signature key and the other
   uses a static Diffie-Hellman key.

   The authentication key algorithm needs to be compatible with the
   method and the selected cipher suite (see Section 3.6).  The
   authentication key algorithm needs to be compatible with the EDHOC
   key exchange algorithm when static Diffie-Hellman authentication is
   used and compatible with the EDHOC signature algorithm when signature
   authentication is used.

   Note that for most signature algorithms, the signature is determined
   jointly by the signature algorithm and the authentication key
   algorithm.  When using static Diffie-Hellman keys, the Initiator's
   and the Responder's private authentication keys are denoted as I and
   R, respectively, and the public authentication keys are denoted G_I
   and G_R, respectively.

   For X.509 certificates, the authentication key is represented by a
   SubjectPublicKeyInfo field, which also contains information about
   authentication key algorithm.  For CWT and CCS (see Section 3.5.2),
   the authentication key is represented by a 'cnf' claim [RFC8747]
   containing a COSE_Key [RFC9052], which contains information about
   authentication key algorithm.  In EDHOC, a raw public key (RPK) is an
   authentication key encoded as a COSE_Key wrapped in a CCS, an example
   is given in Figure 4.

3.5.2.  Authentication Credentials

   The authentication credentials, CRED_I and CRED_R, contain the public
   authentication key of the Initiator and Responder, respectively.  We
   use the notation CRED_x to refer to CRED_I or CRED_R.  Requirements
   on CRED_x applies both to CRED_I and to CRED_R.  The authentication
   credential typically also contains other parameters that needs to be
   verified by the application (see Appendix D) and in particular
   information about the identity ("subject") of the endpoint to prevent
   misbinding attacks (see Appendix D.2).

   EDHOC relies on COSE for identification of credentials (see
   Section 3.5.3), for example, X.509 certificates [RFC9360], C509
   certificates [C509-CERTS], CWTs [RFC8392], and CCSs [RFC8392].  When
   the identified credential is a chain or a bag, the authentication
   credential CRED_x is just the end entity X.509 or C509 certificate /
   CWT.  In the choice between a chain or a bag, it is RECOMMENDED to
   use a chain, since the certificates in a bag are unordered and may
   contain self-signed and extraneous certificates, which can add
   complexity to the process of extracting the end entity certificate.
   The Initiator and Responder MAY use different types of authentication
   credentials, e.g., one uses an RPK and the other uses a public key
   certificate.

   Since CRED_R is used in the integrity verification (see
   Section 5.3.2), it needs to be specified such that it is identical
   when used by the Initiator or Responder.  Similarly for CRED_I, see
   Section 5.4.2.  The Initiator and Responder are expected to agree on
   the specific encoding of the authentication credentials; see
   Section 3.9.  It is RECOMMENDED that the COSE 'kid' parameter, when
   used to identify the authentication credential, refers to such a
   specific encoding of the authentication credential.  The Initiator
   and Responder SHOULD use an available authentication credential
   without re-encoding, i.e. an authentication credential transported in
   EDHOC by value, or otherwise provisioned, SHOULD be used as is.  If
   for some reason re-encoding of an authentication credential passed by
   reference may occur, then a potential common encoding for CBOR-based
   credentials is deterministically encoded CBOR, as specified in
   Sections 4.2.1 and 4.2.2 of [RFC8949].

   *  When the authentication credential is an X.509 certificate, CRED_x
      SHALL be the DER-encoded certificate, encoded as a bstr [RFC9360].

   *  When the authentication credential is a C509 certificate, CRED_x
      SHALL be the C509 certificate [C509-CERTS].

   *  When the authentication credential is a CWT including a COSE_Key,
      CRED_x SHALL be the untagged CWT.

   *  When the authentication credential includes a COSE_Key but is not
      in a CWT, CRED_x SHALL be an untagged CCS.  This is how RPKs are
      encoded, see Figure 4 for an example.

      -  Naked COSE_Keys are thus dressed as CCS when used in EDHOC, in
         its simplest form by prefixing the COSE_Key with 0xA108A101 (a
         map with a 'cnf' claim).  In that case, the resulting
         authentication credential contains no other identity than the
         public key itself; see Appendix D.2.

   An example of CRED_x is shown below:

   {                                              /CCS/
     2 : "42-50-31-FF-EF-37-32-39",               /sub/
     8 : {                                        /cnf/
       1 : {                                      /COSE_Key/
         1 : 1,                                   /kty/
         2 : h'00',                               /kid/
        -1 : 4,                                   /crv/
        -2 : h'b1a3e89460e88d3a8d54211dc95f0b90   /x/
               3ff205eb71912d6db8f4af980d2db83a'
       }
     }
   }

      Figure 4: CCS Containing an X25519 Static Diffie-Hellman Key and
                             an EUI-64 Identity

3.5.3.  Identification of Credentials

   The ID_CRED fields, ID_CRED_R and ID_CRED_I, are transported in
   message_2 and message_3, respectively; see Sections 5.3.2 and 5.4.2.
   We use the notation ID_CRED_x to refer to ID_CRED_I or ID_CRED_R.
   Requirements on ID_CRED_x applies both to ID_CRED_I and to ID_CRED_R.
   The ID_CRED fields are used to identify and optionally transport
   credentials:

   *  ID_CRED_R is intended to facilitate for the Initiator retrieving
      the authentication credential CRED_R and the authentication key of
      R.

   *  ID_CRED_I is intended to facilitate for the Responder retrieving
      the authentication credential CRED_I and the authentication key of
      I.

   ID_CRED_x may contain the authentication credential CRED_x, for x = I
   or R, but for many settings, it is not necessary to transport the
   authentication credential within EDHOC.  For example, it may be pre-
   provisioned or acquired out-of-band over less constrained links.
   ID_CRED_I and ID_CRED_R do not have any cryptographic purpose in
   EDHOC since the authentication credentials are integrity protected by
   the Signature_or_MAC field.

   EDHOC relies on COSE for identification of credentials and supports
   all credential types for which COSE header parameters are defined,
   including X.509 certificates [RFC9360], C509 certificates
   [C509-CERTS], CWTs (Section 3.5.3.1) and CCSs (Section 3.5.3.1).

   ID_CRED_I and ID_CRED_R are of type COSE header_map, as defined in
   Section 3 of [RFC9052], and contain one or more COSE header
   parameters.  If a map contains several header parameters, the labels
   do not need to be sorted in bytewise lexicographic order.  ID_CRED_I
   and ID_CRED_R MAY contain different header parameters.  The header
   parameters typically provide some information about the format of the
   credential.

   Example: X.509 certificates can be identified by a hash value using
   the 'x5t' parameter; see Section 2 of [RFC9360]:

   *  ID_CRED_x = { 34 : COSE_CertHash }, for x = I or R

   Example: CWT or CCS can be identified by a key identifier using the
   'kid' parameter; see Section 3.1 of [RFC9052]:

   *  ID_CRED_x = { 4 : kid_x }, where kid_x : kid, for x = I or R

   Note that COSE header parameters in ID_CRED_x are used to identify
   the message sender's credential.  Therefore, there is no reason to
   use the "-sender" header parameters, such as x5t-sender, defined in
   Section 3 of [RFC9360].  Instead, the corresponding parameter without
   "-sender", such as x5t, SHOULD be used.

   As stated in Section 3.1 of [RFC9052], applications MUST NOT assume
   that 'kid' values are unique and several keys associated with a 'kid'
   may need to be checked before the correct one is found.  Applications
   might use additional information such as 'kid context' or lower
   layers to determine which key to try first.  Applications should
   strive to make ID_CRED_x as unique as possible, since the recipient
   may otherwise have to try several keys.

   See Appendix C.3 for more examples.

3.5.3.1.  COSE Header Parameters for CWT and CWT Claims Set

   This document registers two new COSE header parameters, 'kcwt' and
   'kccs', for use with CBOR Web Token (CWT) [RFC8392] and CWT Claims
   Set (CCS) [RFC8392], respectively.  The CWT/CCS MUST contain a
   COSE_Key in a 'cnf' claim [RFC8747].  There may be any number of
   additional claims present in the CWT/CCS.

   CWTs sent in 'kcwt' are protected using a MAC or a signature and are
   similar to a certificate (when used with public key cryptography) or
   a Kerberos ticket (when used with symmetric key cryptography).  CCSs
   sent in 'kccs' are not protected and are therefore similar to raw
   public keys or self-signed certificates.

   Security considerations for 'kcwt' and 'kccs' are made in
   Section 9.8.

3.5.3.2.  Compact Encoding of ID_CRED Fields for 'kid'

   To comply with the Lightweight Authenticated Key Exchange (LAKE)
   message size requirements (see [LAKE-REQS]), two optimizations are
   made for the case when ID_CRED_x, for x = I or R, contains a single
   'kid' parameter.

   1.  The CBOR map { 4 : kid_x } is replaced by the byte string kid_x.

   2.  The representation of identifiers specified in Section 3.3.2 is
       applied to kid_x.

   These optimizations MUST be applied if and only if ID_CRED_x = { 4 :
   kid_x } and ID_CRED_x in PLAINTEXT_y of message_y, y = 2 or 3; see
   Sections 5.3.2 and 5.4.2.  Note that these optimizations are not
   applied to instances of ID_CRED_x that have no impact on message
   size, e.g., context_y, or the COSE protected header.  For example:

   *  For ID_CRED_x = { 4 : h'FF' }, the encoding in PLAINTEXT_y is not
      the CBOR map 0xA10441FF but the CBOR byte string h'FF', i.e.,
      0x41FF.

   *  For ID_CRED_x = { 4 : h'21' }, the encoding in PLAINTEXT_y is
      neither the CBOR map 0xA1044121 nor the CBOR byte string h'21',
      i.e., 0x4121, but the CBOR integer 0x21.

3.6.  Cipher Suites

   An EDHOC cipher suite consists of an ordered set of algorithms from
   the "COSE Algorithms" and "COSE Elliptic Curves" registries as well
   as the EDHOC MAC length.  All algorithm names and definitions follow
   COSE Algorithms [RFC9053].  Note that COSE sometimes uses peculiar
   names such as ES256 for Elliptic Curve Digital Signature Algorithm
   (ECDSA) with SHA-256, A128 for AES-128, and Ed25519 for the curve
   edwards25519.  Algorithms need to be specified with enough parameters
   to make them completely determined.  The EDHOC MAC length MUST be at
   least 8 bytes.  Any cryptographic algorithm used in the COSE header
   parameters in ID_CRED fields is selected independently of the
   selected cipher suite.  EDHOC is currently only specified for use
   with key exchange algorithms of type ECDH curves, but any Key
   Encapsulation Mechanism (KEM), including Post-Quantum Cryptography
   (PQC) KEMs, can be used in method 0; see Section 9.4.  Use of other
   types of key exchange algorithms to replace static DH authentication
   (methods 1, 2, and 3) would likely require a specification updating
   EDHOC with new methods.

   EDHOC supports all signature algorithms defined by COSE.  Just like
   in (D)TLS 1.3 [RFC8446] [RFC9147] and IKEv2 [RFC7296], a signature in
   COSE is determined jointly by the signature algorithm and the
   authentication key algorithm; see Section 3.5.1.  The exact details
   of the authentication key algorithm depend on the type of
   authentication credential.  COSE supports different formats for
   storing the public authentication keys including COSE_Key and X.509,
   which use different names and ways to represent the authentication
   key and the authentication key algorithm.

   An EDHOC cipher suite consists of the following parameters:

   *  EDHOC AEAD algorithm,

   *  EDHOC hash algorithm,

   *  EDHOC MAC length in bytes (Static DH),

   *  EDHOC key exchange algorithm (ECDH curve),

   *  EDHOC signature algorithm,

   *  application AEAD algorithm, and

   *  application hash algorithm.

   Each cipher suite is identified with a predefined integer label.

   EDHOC can be used with all algorithms and curves defined for COSE.
   Implementations can either use any combination of COSE algorithms and
   parameters to define their own private cipher suite or use one of the
   predefined cipher suites.  Private cipher suites can be identified
   with any of the four values: -24, -23, -22, and -21.  The predefined
   cipher suites are listed in the IANA registry (Section 10.2) with the
   initial content outlined here:

   *  Cipher suites 0-3, based on AES-CCM, are intended for constrained
      IoT where message overhead is a very important factor.  Note that
      AES-CCM-16-64-128 and AES-CCM-16-128-128 are compatible with the
      IEEE AES-CCM* mode of operation defined in Annex B of
      [IEEE.802.15.4-2015].

      -  Cipher suites 1 and 3 use a larger tag length (128 bits) in
         EDHOC than in the application AEAD algorithm (64 bits).

   *  Cipher suites 4 and 5, based on ChaCha20, are intended for less
      constrained applications and only use 128-bit tag lengths.

   *  Cipher suite 6, based on AES-GCM, is for general non-constrained
      applications.  It consists of high-performance algorithms that are
      widely used in non-constrained applications.

   *  Cipher suites 24 and 25 are intended for high security
      applications such as government use and financial applications.
      These cipher suites do not share any algorithms.  Cipher suite 24
      consists of algorithms from the Commercial National Security
      Algorithm (CNSA) 1.0 suite [CNSA].

   The different methods (Section 3.2) use the same cipher suites, but
   some algorithms are not used in some methods.  The EDHOC signature
   algorithm is not used in methods without signature authentication.

   The Initiator needs to have a list of cipher suites it supports in
   order of preference.  The Responder needs to have a list of cipher
   suites it supports.  SUITES_I contains cipher suites supported by the
   Initiator and formatted and processed as detailed in Section 5.2.1 to
   secure the cipher suite negotiation.  Examples of cipher suite
   negotiation are given in Section 6.3.2.

3.7.  Ephemeral Public Keys

   The ephemeral public keys in EDHOC (G_X and G_Y) use compact
   representation of elliptic curve points; see Appendix B.  In COSE,
   compact representation is achieved by formatting the ECDH ephemeral
   public keys as COSE_Keys of type EC2 or Octet Key Pair (OKP)
   according to Sections 7.1 and 7.2 of [RFC9053] but only including the
   'x' parameter in G_X and G_Y.  For Elliptic Curve Keys of type EC2,
   compact representation MAY be used also in the COSE_Key.  COSE always
   uses compact output for Elliptic Curve Keys of type EC2.  If the COSE
   implementation requires a 'y' parameter, the value y = false or a
   calculated y-coordinate can be used; see Appendix B.

3.8.  External Authorization Data (EAD)

   In order to reduce round trips and the number of messages or to
   simplify processing, external security applications may be integrated
   into EDHOC by transporting authorization-related data in the
   messages.

   EDHOC allows processing of external authorization data (EAD) to be
   defined in a separate specification and sent in dedicated fields of
   the four EDHOC messages: EAD_1, EAD_2, EAD_3, and EAD_4.  EAD is
   opaque data to EDHOC.

   Each EAD field, EAD_x, for x = 1, 2, 3, or 4, is a CBOR sequence (see
   Appendix C.1) consisting of one or more EAD items.  EAD item ead is a
   CBOR sequence of an ead_label and an optional ead_value; see Figure 5
   and Appendix C.2 for the CDDL definitions.

   ead = (
     ead_label : int,
     ? ead_value : bstr,
   )

                             Figure 5: EAD Item

   A security application may register one or more EAD labels (see
   Section 10.5) and specify the associated processing and security
   considerations.  The IANA registry contains the absolute value of the
   ead_label, |ead_label|; the same ead_value applies independently of
   the sign of the ead_label.

   An EAD item can be either critical or non-critical, determined by the
   sign of the ead_label in the EAD item transported in the EAD field.
   A negative value indicates that the EAD item is critical, and a
   nonnegative value indicates that the EAD item is non-critical.

   If an endpoint receives a critical EAD item it does not recognize or
   a critical EAD item that contains information that it cannot process,
   then the endpoint MUST send an EDHOC error message back as defined in
   Section 6, and the EDHOC session MUST be aborted.  The EAD item
   specification defines the error processing.  A non-critical EAD item
   can be ignored.

   The security application registering a new EAD item needs to describe
   under what conditions the EAD item is critical or non-critical, and
   thus whether the ead_label is used with a negative or positive sign.
   ead_label = 0 is used for padding; see Section 3.8.1.

   The security application may define multiple uses of certain EAD
   items, e.g., the same EAD item may be used in different EDHOC
   messages.  Multiple occurrences of an EAD item in one EAD field may
   also be specified, but the criticality of the repeated EAD item is
   expected to be the same.

   The EAD fields of EDHOC MUST only be used with registered EAD items;
   see Section 10.5.  Examples of the use of EAD are provided in
   Appendix E.

3.8.1.  Padding

   EDHOC message_1 and the plaintext of message_2, message_3, and
   message_4 can be padded with the use of the corresponding EAD_x
   field, for x = 1, 2, 3, or 4.  Padding in EAD_1 mitigates
   amplification attacks (see Section 9.7), and padding in EAD_2, EAD_3,
   and EAD_4 hides the true length of the plaintext (see Section 9.6).
   Padding MUST be ignored and discarded by the receiving application.

   Padding is obtained by using an EAD item with ead_label = 0 and a
   (pseudo)randomly generated byte string of appropriate length as
   ead_value, noting that the ead_label and the CBOR encoding of
   ead_value also add bytes.  For example:

   *  One-byte padding (optional ead_value omitted):

      EAD_x = 0x00

   *  Two-byte padding, using the empty byte string (0x40) as ead_value:

      EAD_x = 0x0040

   *  Three-byte padding, constructed from the pseudorandomly generated
      ead_value 0xe9 encoded as byte string:

      EAD_x = 0x0041e9

   Multiple occurrences of EAD items with ead_label = 0 are allowed.
   Certain padding lengths require the use of at least two such EAD
   items.

   Note that padding is non-critical because the intended behavior when
   receiving is to ignore it.

3.9.  Application Profile

   EDHOC requires certain parameters to be agreed upon between the
   Initiator and Responder.  Some parameters can be negotiated through
   the protocol execution (specifically, cipher suite; see Section 3.6),
   but other parameters are only communicated and may not be negotiated
   (e.g., which authentication method is used; see Section 3.2).  Yet,
   other parameters need to be known out-of-band to ensure successful
   completion, e.g., whether message_4 is used or not.  The application
   decides which endpoint is the Initiator and which is the Responder.

   The purpose of an application profile is to describe the intended use
   of EDHOC to allow for the relevant processing and verifications to be
   made, including things like the following:

   1.  How the endpoint detects that an EDHOC message is received.  This
       includes how EDHOC messages are transported, for example, in the
       payload of a CoAP message with a certain Uri-Path or Content-
       Format; see Appendix A.2.

       The method of transporting EDHOC messages may also describe data
       carried along with the messages that are needed for the transport
       to satisfy the requirements of Section 3.4, e.g., connection
       identifiers used with certain messages; see Appendix A.2.

   2.  Authentication method (METHOD; see Section 3.2).

   3.  Profile for authentication credentials (CRED_I and CRED_R; see
       Section 3.5.2), e.g., profile for certificate or CCS, including
       supported authentication key algorithms (subject public key
       algorithm in X.509 or C509 certificate).

   4.  Type used to identify credentials (ID_CRED_I and ID_CRED_R; see
       Section 3.5.3).

   5.  Use and type of external authorization data (EAD_1, EAD_2, EAD_3,
       and EAD_4; see Section 3.8).

   6.  Identifier used as the identity of the endpoint; see
       Appendix D.2.

   7.  If message_4 shall be sent/expected, and if not, how to ensure a
       protected application message is sent from the Responder to the
       Initiator; see Section 5.5.

   The application profile may also contain information about supported
   cipher suites.  The procedure for selecting and verifying a cipher
   suite is still performed as described in Sections 5.2.1 and 6.3, but
   it may become simplified by this knowledge.  EDHOC messages can be
   processed without the application profile, i.e., the EDHOC messages
   include information about the type and length of all fields.

   An example of an application profile is shown in Appendix F.

   For some parameters, like METHOD, the type of the ID_CRED field, or
   EAD, the receiver of an EDHOC message is able to verify compliance
   with the application profile and, if it needs to fail because of the
   lack of compliance, to infer the reason why the EDHOC session failed.

   For other encodings, like the profiling of CRED_x in the case that it
   is not transported, it may not be possible to verify that the lack of
   compliance with the application profile was the reason for failure.
   For example, integrity verification in message_2 or message_3 may
   fail not only because of a wrong credential.  For example, in case
   the Initiator uses a public key certificate by reference (i.e., not
   transported within the protocol), then both endpoints need to use an
   identical data structure as CRED_I or else the integrity verification
   will fail.

   Note that it is not necessary for the endpoints to specify a single
   transport for the EDHOC messages.  For example, a mix of CoAP and
   HTTP may be used along the path, and this may still allow correlation
   between messages.

   The application profile may be dependent on the identity of the other
   endpoint or other information carried in an EDHOC message, but it
   then applies only to the later phases of the protocol when such
   information is known.  (The Initiator does not know the identity of
   the Responder before having verified message_2, and the Responder
   does not know the identity of the Initiator before having verified
   message_3.)

   Other conditions may be part of the application profile, such as what
   is the target application or use (if there is more than one
   application/use) to the extent that EDHOC can distinguish between
   them.  In case multiple application profiles are used, the receiver
   needs to be able to determine which is applicable for a given EDHOC
   session, for example, based on the URI to which the EDHOC message is
   sent, or external authorization data type.

4.  Key Derivation

4.1.  Keys for EDHOC Message Processing

   EDHOC uses Extract-and-Expand [RFC5869] with the EDHOC hash algorithm
   in the selected cipher suite to derive keys used in message
   processing.  This section defines EDHOC_Extract (Section 4.1.1) and
   EDHOC_Expand (Section 4.1.2) and how to use them to derive PRK_out
   (Section 4.1.3), which is the shared secret session key resulting
   from a completed EDHOC session.

   EDHOC_Extract is used to derive fixed-length uniformly pseudorandom
   keys (PRKs) from ECDH shared secrets.  EDHOC_Expand is used to define
   EDHOC_KDF for generating MACs and for deriving output keying material
   (OKM) from PRKs.

   In EDHOC, a specific message is protected with a certain PRK, but how
   the key is derived depends on the authentication method
   (Section 3.2), as detailed in Section 5.

4.1.1.  EDHOC_Extract

   The pseudorandom keys (PRKs) used for EDHOC message processing are
   derived using EDHOC_Extract:

      PRK = EDHOC_Extract( salt, IKM )

   where the input keying material (IKM) and salt are defined for each
   PRK below.

   The definition of EDHOC_Extract depends on the EDHOC hash algorithm
   of the selected cipher suite:

   *  If the EDHOC hash algorithm is SHA-2, then EDHOC_Extract( salt,
      IKM ) = HKDF-Extract( salt, IKM ) [RFC5869].

   *  If the EDHOC hash algorithm is SHAKE128, then EDHOC_Extract( salt,
      IKM ) = KMAC128( salt, IKM, 256, "" ).

   *  If the EDHOC hash algorithm is SHAKE256, then EDHOC_Extract( salt,
      IKM ) = KMAC256( salt, IKM, 512, "" ).

   where the Keccak Message Authentication Code (KMAC) is specified in
   [SP800-185].

   The rest of the section defines the pseudorandom keys PRK_2e,
   PRK_3e2m, and PRK_4e3m; their use is shown in Figure 6.  The index of
   a PRK indicates its use or in what message protection operation it is
   involved.  For example, PRK_3e2m is involved in the encryption of
   message 3 and in calculating the MAC of message 2.

4.1.1.1.  PRK_2e

   The pseudorandom key PRK_2e is derived with the following input:

   *  The salt SHALL be TH_2.

   *  The IKM SHALL be the ephemeral-ephemeral ECDH shared secret G_XY
      (calculated from G_X and Y or G_Y and X) as defined in
      Section 6.3.1 of [RFC9053].  The use of G_XY gives forward secrecy
      in the sense that compromise of the private authentication keys
      does not compromise past session keys.

   Example: Assuming the use of curve25519, the ECDH shared secret G_XY
   is the output of the X25519 function [RFC7748]:

      G_XY = X25519( Y, G_X ) = X25519( X, G_Y )

   Example: Assuming the use of SHA-256, the extract phase of the key
   derivation function is HKDF-Extract, which produces PRK_2e as
   follows:

      PRK_2e = HMAC-SHA-256( TH_2, G_XY )

4.1.1.2.  PRK_3e2m

   The pseudorandom key PRK_3e2m is derived as follows:

   If the Responder authenticates with a static Diffie-Hellman key, then
   PRK_3e2m = EDHOC_Extract( SALT_3e2m, G_RX ), where

   *  SALT_3e2m is derived from PRK_2e (see Section 4.1.2) and

   *  G_RX is the ECDH shared secret calculated from G_R and X, or G_X
      and R (the Responder's private authentication key; see
      Section 3.5.1),

   else PRK_3e2m = PRK_2e.

4.1.1.3.  PRK_4e3m

   The pseudorandom key PRK_4e3m is derived as follows:

   If the Initiator authenticates with a static Diffie-Hellman key, then
   PRK_4e3m = EDHOC_Extract( SALT_4e3m, G_IY ), where

   *  SALT_4e3m is derived from PRK_3e2m (see Section 4.1.2) and

   *  G_IY is the ECDH shared secret calculated from G_I and Y, or G_Y
      and I (the Initiator's private authentication key; see
      Section 3.5.1),

   else PRK_4e3m = PRK_3e2m.

4.1.2.  EDHOC_Expand and EDHOC_KDF

   The output keying material (OKM) -- including keys, initialization
   vectors (IVs), and salts -- are derived from the PRKs using the
   EDHOC_KDF, which is defined through EDHOC_Expand:

      OKM = EDHOC_KDF( PRK, info_label, context, length )
          = EDHOC_Expand( PRK, info, length )

   where info is encoded as the CBOR sequence:

   info = (
     info_label : int,
     context : bstr,
     length : uint,
   )

   where:

   *  info_label is an int,

   *  context is a bstr, and

   *  length is the length of OKM in bytes.

   When EDHOC_KDF is used to derive OKM for EDHOC message processing,
   then the context includes one of the transcript hashes, TH_2, TH_3,
   or TH_4, defined in Sections 5.3.2 and 5.4.2.

   The definition of EDHOC_Expand depends on the EDHOC hash algorithm of
   the selected cipher suite:

   *  If the EDHOC hash algorithm is SHA-2, then EDHOC_Expand( PRK,
      info, length ) = HKDF-Expand( PRK, info, length ) [RFC5869].

   *  If the EDHOC hash algorithm is SHAKE128, then EDHOC_Expand( PRK,
      info, length ) = KMAC128( PRK, info, L, "" ).

   *  If the EDHOC hash algorithm is SHAKE256, then EDHOC_Expand( PRK,
      info, length ) = KMAC256( PRK, info, L, "" ).

   where L = 8 ⋅ length, the output length in bits.

   Figure 6 lists derivations made with EDHOC_KDF, where:

   *  hash_length is the length of output size of the EDHOC hash
      algorithm of the selected cipher suite,

   *  key_length is the length of the encryption key of the EDHOC AEAD
      algorithm of the selected cipher suite, and

   *  iv_length is the length of the initialization vector of the EDHOC
      AEAD algorithm of the selected cipher suite

   Further details of the key derivation and how the output keying
   material is used are specified in Section 5.

   KEYSTREAM_2   = EDHOC_KDF( PRK_2e,   0, TH_2,      plaintext_length )
   SALT_3e2m     = EDHOC_KDF( PRK_2e,   1, TH_2,      hash_length )
   MAC_2         = EDHOC_KDF( PRK_3e2m, 2, context_2, mac_length_2 )
   K_3           = EDHOC_KDF( PRK_3e2m, 3, TH_3,      key_length )
   IV_3          = EDHOC_KDF( PRK_3e2m, 4, TH_3,      iv_length )
   SALT_4e3m     = EDHOC_KDF( PRK_3e2m, 5, TH_3,      hash_length )
   MAC_3         = EDHOC_KDF( PRK_4e3m, 6, context_3, mac_length_3 )
   PRK_out       = EDHOC_KDF( PRK_4e3m, 7, TH_4,      hash_length )
   K_4           = EDHOC_KDF( PRK_4e3m, 8, TH_4,      key_length )
   IV_4          = EDHOC_KDF( PRK_4e3m, 9, TH_4,      iv_length )
   PRK_exporter  = EDHOC_KDF( PRK_out, 10, h'',       hash_length )

                 Figure 6: Key Derivations Using EDHOC_KDF

   h'' is CBOR diagnostic notation for the empty byte string, 0x40.

4.1.3.  PRK_out

   The pseudorandom key PRK_out, derived as shown in Figure 6, is the
   output session key of a completed EDHOC session.

   Keys for applications are derived using EDHOC_Exporter (see
   Section 4.2.1) from PRK_exporter, which in turn is derived from
   PRK_out as shown in Figure 6.  For the purpose of generating
   application keys, it is sufficient to store PRK_out or PRK_exporter.
   (Note that the word "store" used here does not imply that the
   application has access to the plaintext PRK_out since that may be
   reserved for code within a Trusted Execution Environment (TEE); see
   Section 9.8.)

4.2.  Keys for EDHOC Applications

   This section defines EDHOC_Exporter in terms of EDHOC_KDF and
   PRK_exporter.  A key update function is defined in Appendix H.

4.2.1.  EDHOC_Exporter

   Keying material for the application can be derived using the
   EDHOC_Exporter interface defined as:

      EDHOC_Exporter(exporter_label, context, length)
        = EDHOC_KDF(PRK_exporter, exporter_label, context, length)

   where:

   *  exporter_label is a registered uint from the "EDHOC Exporter
      Labels" registry (Section 10.1),

   *  context is a bstr defined by the application, and

   *  length is a uint defined by the application.

   The (exporter_label, context) pair used in EDHOC_Exporter must be
   unique, i.e., an (exporter_label, context) MUST NOT be used for two
   different purposes.  However, an application can re-derive the same
   key several times as long as it is done securely.  For example, in
   most encryption algorithms, the same key can be reused with different
   nonces.  The context can, for example, be the empty CBOR byte string.

   Examples of use of the EDHOC_Exporter are given in Appendix A.

5.  Message Formatting and Processing

   This section specifies formatting of the messages and processing
   steps.  Error messages are specified in Section 6.  Annotated traces
   of EDHOC sessions are provided in [RFC9529].

   An EDHOC message is encoded as a sequence of CBOR data items (CBOR
   Sequence [RFC8742]).  Additional optimizations are made to reduce
   message overhead.

   While EDHOC uses the COSE_Key, COSE_Sign1, and COSE_Encrypt0
   structures, only a subset of the parameters is included in the EDHOC
   messages; see Appendix C.3.  In order to recreate the COSE object,
   the recipient endpoint may need to add parameters to the COSE headers
   not included in the EDHOC message, for example, the parameter 'alg'
   to COSE_Sign1 or COSE_Encrypt0.

5.1.  EDHOC Message Processing Outline

   For each new/ongoing EDHOC session, the endpoints are assumed to keep
   an associated protocol state containing identifiers, keying material,
   etc. used for subsequent processing of protocol-related data.  The
   protocol state is assumed to be associated with an application
   profile (Section 3.9) that provides the context for how messages are
   transported, identified, and processed.

   EDHOC messages SHALL be processed according to the current protocol
   state.  The following steps are expected to be performed at reception
   of an EDHOC message:

   1.  Detect that an EDHOC message has been received, for example, by
       means of a port number, URI, or media type (Section 3.9).

   2.  Retrieve the protocol state according to the message correlation;
       see Section 3.4.1.  If there is no protocol state, in the case of
       message_1, a new protocol state is created.  The Responder
       endpoint needs to make use of available denial-of-service
       mitigation (Section 9.7).

   3.  If the message received is an error message, then process it
       according to Section 6, else process it as the expected next
       message according to the protocol state.

   The message processing steps SHALL be processed in order, unless
   otherwise stated.  If the processing fails for some reason, then
   typically an error message is sent, the EDHOC session is aborted, and
   the protocol state is erased.  When the composition and sending of
   one message is completed and before the next message is received,
   error messages SHALL NOT be sent.

   After having successfully processed the last message (message_3 or
   message_4 depending on application profile), the EDHOC session is
   completed; after which, no error messages are sent and EDHOC session
   output MAY be maintained even if error messages are received.
   Further details are provided in the following subsections and in
   Section 6.

   Different instances of the same message MUST NOT be processed in one
   EDHOC session.  Note that processing will fail if the same message
   appears a second time for EDHOC processing in the same EDHOC session
   because the state of the protocol has moved on and now expects
   something else.  Message deduplication MUST be done by the transport
   protocol (see Section 3.4) or, if not supported by the transport, as
   described in Section 7.

5.2.  EDHOC Message 1

5.2.1.  Formatting of Message 1

   message_1 SHALL be a CBOR Sequence (see Appendix C.1), as defined
   below.

   message_1 = (
     METHOD : int,
     SUITES_I : suites,
     G_X : bstr,
     C_I : bstr / -24..23,
     ? EAD_1,
   )

   suites = [ 2* int ] / int
   EAD_1 = 1* ead

   where:

   *  METHOD is an authentication method; see Section 3.2,

   *  SUITES_I is an array of cipher suites that the Initiator supports
      constructed as specified in Section 5.2.2,

   *  G_X is the ephemeral public key of the Initiator, and

   *  C_I is a variable-length connection identifier (note that
      connection identifiers are byte strings but certain values are
      represented as integers in the message; see Section 3.3.2), and

   *  EAD_1 is external authorization data; see Section 3.8.

5.2.2.  Initiator Composition of Message 1

   The processing steps are detailed below and in Section 6.3.

   The Initiator SHALL compose message_1 as follows:

   *  Construct SUITES_I as an array of cipher suites supported by I in
      order of preference by I with the first cipher suite in the array
      being the most preferred by I and the last being the one selected
      by I for this EDHOC session.  If the cipher suite most preferred
      by I is selected, then SUITES_I contains only that cipher suite
      and is encoded as an int.  All cipher suites, if any, preferred by
      I over the selected one MUST be included.  (See also Section 6.3.)

      -  The selected suite is based on what the Initiator can assume to
         be supported by the Responder; if the Initiator previously
         received from the Responder an error message with error code 2
         containing SUITES_R (see Section 6.3) indicating cipher suites
         supported by the Responder, then the Initiator SHOULD select
         its most preferred supported cipher suite among those (bearing
         in mind that error messages may be forged).

      -  The Initiator MUST NOT change its order of preference for
         cipher suites and MUST NOT omit a cipher suite preferred to the
         selected one because of previous error messages received from
         the Responder.

   *  Generate an ephemeral ECDH key pair using the curve in the
      selected cipher suite and format it as a COSE_Key.  Let G_X be the
      'x' parameter of the COSE_Key.

   *  Choose a connection identifier C_I and store it during the EDHOC
      session.

   *  Encode message_1 as a sequence of CBOR-encoded data items as
      specified in Section 5.2.1

5.2.3.  Responder Processing of Message 1

   The Responder SHALL process message_1 in the following order:

   1.  Decode message_1 (see Appendix C.1).

   2.  Process message_1.  In particular, verify that the selected
       cipher suite is supported and that no prior cipher suite as
       ordered in SUITES_I is supported.

   3.  If all processing completed successfully, and if EAD_1 is
       present, then make it available to the application for EAD
       processing.

   If any processing step fails, then the Responder MUST send an EDHOC
   error message back as defined in Section 6, and the EDHOC session
   MUST be aborted.

5.3.  EDHOC Message 2

5.3.1.  Formatting of Message 2

   message_2 SHALL be a CBOR Sequence (see Appendix C.1), as defined
   below.

   message_2 = (
     G_Y_CIPHERTEXT_2 : bstr,
   )

   where:

   *  G_Y_CIPHERTEXT_2 is the concatenation of G_Y (i.e., the ephemeral
      public key of the Responder) and CIPHERTEXT_2.

5.3.2.  Responder Composition of Message 2

   The Responder SHALL compose message_2 as follows:

   *  Generate an ephemeral ECDH key pair using the curve in the
      selected cipher suite and format it as a COSE_Key.  Let G_Y be the
      'x' parameter of the COSE_Key.

   *  Choose a connection identifier C_R and store it for the length of
      the EDHOC session.

   *  Compute the transcript hash TH_2 = H( G_Y, H(message_1) ), where
      H() is the EDHOC hash algorithm of the selected cipher suite.  The
      input to the hash function is a CBOR Sequence.  Note that
      H(message_1) can be computed and cached already in the processing
      of message_1.

   *  Compute MAC_2 as in Section 4.1.2 with context_2 = << C_R,
      ID_CRED_R, TH_2, CRED_R, ? EAD_2 >> (see Appendix C.1 for
      notation).

      -  If the Responder authenticates with a static Diffie-Hellman key
         (method equals 1 or 3), then mac_length_2 is the EDHOC MAC
         length of the selected cipher suite.  If the Responder
         authenticates with a signature key (method equals 0 or 2), then
         mac_length_2 is equal to hash_length.

      -  C_R is a variable-length connection identifier.  Note that
         connection identifiers are byte strings but certain values are
         represented as integers in the message; see Section 3.3.2.

      -  ID_CRED_R is an identifier to facilitate the retrieval of
         CRED_R; see Section 3.5.3.

      -  CRED_R is a CBOR item containing the authentication credential
         of the Responder; see Section 3.5.2.

      -  EAD_2 is external authorization data; see Section 3.8.

   *  If the Responder authenticates with a static Diffie-Hellman key
      (method equals 1 or 3), then Signature_or_MAC_2 is MAC_2.  If the
      Responder authenticates with a signature key (method equals 0 or
      2), then Signature_or_MAC_2 is the 'signature' field of a
      COSE_Sign1 object, computed as specified in Section 4.4 of
      [RFC9052] using the signature algorithm of the selected cipher
      suite, the private authentication key of the Responder, and the
      following parameters as input (see Appendix C.3 for an overview of
      COSE and Appendix C.1 for notation):

      -  protected = << ID_CRED_R >>

      -  external_aad = << TH_2, CRED_R, ? EAD_2 >>

      -  payload = MAC_2

   *  CIPHERTEXT_2 is calculated with a binary additive stream cipher,
      using a keystream generated with EDHOC_Expand and the following
      plaintext:

      -  PLAINTEXT_2 = ( C_R, ID_CRED_R / bstr / -24..23,
         Signature_or_MAC_2, ? EAD_2 )

         o  If ID_CRED_R contains a single 'kid' parameter, i.e.,
            ID_CRED_R = { 4 : kid_R }, then the compact encoding is
            applied; see Section 3.5.3.2.

         o  C_R is the variable-length connection identifier.  Note that
            connection identifiers are byte strings, but certain values
            are represented as integers in the message; see
            Section 3.3.2.

      -  Compute KEYSTREAM_2 as in Section 4.1.2, where plaintext_length
         is the length of PLAINTEXT_2.  For the case of plaintext_length
         exceeding the EDHOC_KDF output size, see Appendix G.

      -  CIPHERTEXT_2 = PLAINTEXT_2 XOR KEYSTREAM_2

   *  Encode message_2 as a sequence of CBOR-encoded data items as
      specified in Section 5.3.1.

5.3.3.  Initiator Processing of Message 2

   The Initiator SHALL process message_2 in the following order:

   1.  Decode message_2 (see Appendix C.1).

   2.  Retrieve the protocol state using available message correlation
       (e.g., the CoAP Token, the 5-tuple, or the prepended C_I; see
       Section 3.4.1).

   3.  Decrypt CIPHERTEXT_2; see Section 5.3.2.

   4.  If all processing is completed successfully, then make ID_CRED_R
       and (if present) EAD_2 available to the application for
       authentication and EAD processing.  When and how to perform
       authentication is up to the application.

   5.  Obtain the authentication credential (CRED_R) and the
       authentication key of R from the application (or by other means).

   6.  Verify Signature_or_MAC_2 using the algorithm in the selected
       cipher suite.  The verification process depends on the method;
       see Section 5.3.2.  Make the result of the verification available
       to the application.

   If any processing step fails, then the Initiator MUST send an EDHOC
   error message back as defined in Section 6, and the EDHOC session
   MUST be aborted.

5.4.  EDHOC Message 3

5.4.1.  Formatting of Message 3

   message_3 SHALL be a CBOR Sequence (see Appendix C.1), as defined
   below.

   message_3 = (
     CIPHERTEXT_3 : bstr,
   )

5.4.2.  Initiator Composition of Message 3

   The Initiator SHALL compose message_3 as follows:

   *  Compute the transcript hash TH_3 = H(TH_2, PLAINTEXT_2, CRED_R),
      where H() is the EDHOC hash algorithm of the selected cipher
      suite.  The input to the hash function is a CBOR Sequence.  Note
      that TH_3 can be computed and cached already in the processing of
      message_2.

   *  Compute MAC_3 as in Section 4.1.2, with context_3 = << ID_CRED_I,
      TH_3, CRED_I, ? EAD_3 >>

      -  If the Initiator authenticates with a static Diffie-Hellman key
         (method equals 2 or 3), then mac_length_3 is the EDHOC MAC
         length of the selected cipher suite.  If the Initiator
         authenticates with a signature key (method equals 0 or 1), then
         mac_length_3 is equal to hash_length.

      -  ID_CRED_I is an identifier to facilitate the retrieval of
         CRED_I; see Section 3.5.3.

      -  CRED_I is a CBOR item containing the authentication credential
         of the Initiator; see Section 3.5.2.

      -  EAD_3 is external authorization data; see Section 3.8.

   *  If the Initiator authenticates with a static Diffie-Hellman key
      (method equals 2 or 3), then Signature_or_MAC_3 is MAC_3.  If the
      Initiator authenticates with a signature key (method equals 0 or
      1), then Signature_or_MAC_3 is the 'signature' field of a
      COSE_Sign1 object, computed as specified in Section 4.4 of
      [RFC9052] using the signature algorithm of the selected cipher
      suite, the private authentication key of the Initiator, and the
      following parameters as input (see Appendix C.3):

      -  protected = << ID_CRED_I >>

      -  external_aad = << TH_3, CRED_I, ? EAD_3 >>

      -  payload = MAC_3

   *  Compute a COSE_Encrypt0 object as defined in Sections 5.2 and 5.3
      of [RFC9052], with the EDHOC AEAD algorithm of the selected cipher
      suite, using the encryption key K_3, the initialization vector
      IV_3 (if used by the AEAD algorithm), the plaintext PLAINTEXT_3,
      and the following parameters as input (see Appendix C.3):

      -  protected = h''

      -  external_aad = TH_3

      -  K_3 and IV_3 are defined in Section 4.1.2

      -  PLAINTEXT_3 = ( ID_CRED_I / bstr / -24..23, Signature_or_MAC_3,
         ? EAD_3 )

         o  If ID_CRED_I contains a single 'kid' parameter, i.e.,
            ID_CRED_I = { 4 : kid_I }, then the compact encoding is
            applied; see Section 3.5.3.2.

      CIPHERTEXT_3 is the 'ciphertext' of COSE_Encrypt0.

   *  Compute the transcript hash TH_4 = H(TH_3, PLAINTEXT_3, CRED_I),
      where H() is the EDHOC hash algorithm of the selected cipher
      suite.  The input to the hash function is a CBOR Sequence.

   *  Calculate PRK_out as defined in Figure 6.  The Initiator can now
      derive application keys using the EDHOC_Exporter interface; see
      Section 4.2.1.

   *  Encode message_3 as a CBOR data item as specified in
      Section 5.4.1.

   *  Make the connection identifiers (C_I and C_R) and the application
      algorithms in the selected cipher suite available to the
      application.

   After creating message_3, the Initiator can compute PRK_out (see
   Section 4.1.3) and derive application keys using the EDHOC_Exporter
   interface (see Section 4.2.1).  The Initiator SHOULD NOT persistently
   store PRK_out or application keys until the Initiator has verified
   message_4 or a message protected with a derived application key, such
   as an OSCORE message, from the Responder and the application has
   authenticated the Responder.  This is similar to waiting for an
   acknowledgment (ACK) in a transport protocol.  The Initiator SHOULD
   NOT send protected application data until the application has
   authenticated the Responder.

5.4.3.  Responder Processing of Message 3

   The Responder SHALL process message_3 in the following order:

   1.  Decode message_3 (see Appendix C.1).

   2.  Retrieve the protocol state using available message correlation
       (e.g., the CoAP Token, the 5-tuple, or the prepended C_R; see
       Section 3.4.1).

   3.  Decrypt and verify the COSE_Encrypt0 as defined in Sections 5.2
       and 5.3 of [RFC9052], with the EDHOC AEAD algorithm in the
       selected cipher suite and the parameters defined in
       Section 5.4.2.

   4.  If all processing completed successfully, then make ID_CRED_I and
       (if present) EAD_3 available to the application for
       authentication and EAD processing.  When and how to perform
       authentication is up to the application.

   5.  Obtain the authentication credential (CRED_I) and the
       authentication key of I from the application (or by other means).

   6.  Verify Signature_or_MAC_3 using the algorithm in the selected
       cipher suite.  The verification process depends on the method;
       see Section 5.4.2.  Make the result of the verification available
       to the application.

   7.  Make the connection identifiers (C_I and C_R) and the application
       algorithms in the selected cipher suite available to the
       application.

   After processing message_3, the Responder can compute PRK_out (see
   Section 4.1.3) and derive application keys using the EDHOC_Exporter
   interface (see Section 4.2.1).  The Responder SHOULD NOT persistently
   store PRK_out or application keys until the application has
   authenticated the Initiator.  The Responder SHOULD NOT send protected
   application data until the application has authenticated the
   Initiator.

   If any processing step fails, then the Responder MUST send an EDHOC
   error message back as defined in Section 6, and the EDHOC session
   MUST be aborted.

5.5.  EDHOC Message 4

   This section specifies message_4, which is OPTIONAL to support.  Key
   confirmation is normally provided by sending an application message
   from the Responder to the Initiator protected with a key derived with
   the EDHOC_Exporter, e.g., using OSCORE (see Appendix A).  In
   deployments where no protected application message is sent from the
   Responder to the Initiator, message_4 MUST be supported and MUST be
   used.  Two examples of such deployments are:

   1.  when EDHOC is only used for authentication and no application
       data is sent and

   2.  when application data is only sent from the Initiator to the
       Responder.

   Further considerations about when to use message_4 are provided in
   Sections 3.9 and 9.1.

5.5.1.  Formatting of Message 4

   message_4 SHALL be a CBOR Sequence (see Appendix C.1), as defined
   below.

   message_4 = (
     CIPHERTEXT_4 : bstr,

   )

5.5.2.  Responder Composition of Message 4

   The Responder SHALL compose message_4 as follows:

   *  Compute a COSE_Encrypt0 as defined in Sections 5.2 and 5.3 of
      [RFC9052], with the EDHOC AEAD algorithm of the selected cipher
      suite, using the encryption key K_4, the initialization vector
      IV_4 (if used by the AEAD algorithm), the plaintext PLAINTEXT_4,
      and the following parameters as input (see Appendix C.3):

      -  protected = h''

      -  external_aad = TH_4

      -  K_4 and IV_4 are defined in Section 4.1.2

      -  PLAINTEXT_4 = ( ? EAD_4 )

         o  EAD_4 is external authorization data; see Section 3.8.

      CIPHERTEXT_4 is the 'ciphertext' of COSE_Encrypt0.

   *  Encode message_4 as a CBOR data item as specified in
      Section 5.5.1.

5.5.3.  Initiator Processing of Message 4

   The Initiator SHALL process message_4 as follows:

   *  Decode message_4 (see Appendix C.1).

   *  Retrieve the protocol state using available message correlation
      (e.g., the CoAP Token, the 5-tuple, or the prepended C_I; see
      Section 3.4.1).

   *  Decrypt and verify the COSE_Encrypt0 as defined in Sections 5.2
      and 5.3 of [RFC9052], with the EDHOC AEAD algorithm in the
      selected cipher suite and the parameters defined in Section 5.5.2.

   *  Make (if present) EAD_4 available to the application for EAD
      processing.

   If any processing step fails, then the Initiator MUST send an EDHOC
   error message back as defined in Section 6, and the EDHOC session
   MUST be aborted.

   After verifying message_4, the Initiator is assured that the
   Responder has calculated the key PRK_out (key confirmation) and that
   no other party can derive the key.

6.  Error Handling

   This section defines the format for error messages and the processing
   associated with the currently defined error codes.  Additional error
   codes may be registered; see Section 10.4.

   Many kinds of errors can occur during EDHOC processing.  As in CoAP,
   an error can be triggered by errors in the received message or
   internal errors in the receiving endpoint.  Except for processing and
   formatting errors, it is up to the application when to send an error
   message.  Sending error messages is essential for debugging but MAY
   be skipped if, for example, an EDHOC session cannot be found or due
   to denial-of-service reasons; see Section 9.7.  Error messages in
   EDHOC are always fatal.  After sending an error message, the sender
   MUST abort the EDHOC session.  The receiver SHOULD treat an error
   message as an indication that the other party likely has aborted the
   EDHOC session.  But since error messages might be forged, the
   receiver MAY try to continue the EDHOC session.

   An EDHOC error message can be sent by either endpoint as a reply to
   any non-error EDHOC message.  How errors at the EDHOC layer are
   transported depends on lower layers, which need to enable error
   messages to be sent and processed as intended.

   error SHALL be a CBOR Sequence (see Appendix C.1), as defined below.

   error = (
     ERR_CODE : int,
     ERR_INFO : any,
   )

                       Figure 7: EDHOC Error Message

   where:

   *  ERR_CODE is an error code encoded as an integer.  The value 0 is
      reserved for success and can only be used internally; all other
      values (negative or positive) indicate errors.

   *  ERR_INFO is error information.  Content and encoding depend on the
      error code.

   The remainder of this section specifies the currently defined error
   codes; see Table 3.  Additional error codes and corresponding error
   information may be specified.

       +==========+===============+===============================+
       | ERR_CODE | ERR_INFO Type | Description                   |
       +==========+===============+===============================+
       |        0 |               | Reserved for success          |
       +----------+---------------+-------------------------------+
       |        1 | tstr          | Unspecified error             |
       +----------+---------------+-------------------------------+
       |        2 | suites        | Wrong selected cipher suite   |
       +----------+---------------+-------------------------------+
       |        3 | true          | Unknown credential referenced |
       +----------+---------------+-------------------------------+
       |       23 |               | Reserved                      |
       +----------+---------------+-------------------------------+

             Table 3: EDHOC Error Codes and Error Information

6.1.  Success

   Error code 0 MAY be used internally in an application to indicate
   success, i.e., as a standard value in case of no error, e.g., in
   status reporting or log files.  Error code 0 MUST NOT be used as part
   of the EDHOC message exchange.  If an endpoint receives an error
   message with error code 0, then it MUST abort the EDHOC session and
   MUST NOT send an error message.

6.2.  Unspecified Error

   Error code 1 is used for errors that do not have a specific error
   code defined.  ERR_INFO MUST be a text string containing a human-
   readable diagnostic message that SHOULD be written in English, for
   example, "Method not supported".  The diagnostic text message is
   mainly intended for software engineers who during debugging need to
   interpret it in the context of the EDHOC specification.  The
   diagnostic message SHOULD be provided to the calling application
   where it SHOULD be logged.

6.3.  Wrong Selected Cipher Suite

   Error code 2 MUST only be used when replying to message_1 in case the
   cipher suite selected by the Initiator is not supported by the
   Responder or if the Responder supports a cipher suite more preferred
   by the Initiator than the selected cipher suite; see Section 5.2.3.
   In this case, ERR_INFO = SUITES_R and is of type suites; see
   Section 5.2.1.  If the Responder does not support the selected cipher
   suite, then SUITES_R MUST include one or more supported cipher
   suites.  If the Responder supports a cipher suite in SUITES_I other
   than the selected cipher suite (independently of if the selected
   cipher suite is supported or not), then SUITES_R MUST include the
   supported cipher suite in SUITES_I, which is most preferred by the
   Initiator.  SUITES_R MAY include a single cipher suite; in which
   case, it is encoded as an int.  If the Responder does not support any
   cipher suite in SUITES_I, then it SHOULD include all its supported
   cipher suites in SUITES_R.

   In contrast to SUITES_I, the order of the cipher suites in SUITES_R
   has no significance.

6.3.1.  Cipher Suite Negotiation

   After receiving SUITES_R, the Initiator can determine which cipher
   suite to select (if any) for the next EDHOC run with the Responder.
   The Initiator SHOULD remember which selected cipher suite to use
   until the next message_1 has been sent; otherwise, the Initiator and
   Responder will run into an infinite loop where the Initiator selects
   its most preferred cipher suite and the Responder sends an error with
   supported cipher suites.

   After a completed EDHOC session, the Initiator MAY remember the
   selected cipher suite to use in future EDHOC sessions with this
   Responder.  Note that if the Initiator or Responder is updated with
   new cipher suite policies, any cached information may be outdated.

   Note that the Initiator's list of supported cipher suites and order
   of preference is fixed (see Sections 5.2.1 and 5.2.2).  Furthermore,
   the Responder SHALL only accept message_1 if the selected cipher
   suite is the first cipher suite in SUITES_I that the Responder also
   supports (see Section 5.2.3).  Following this procedure ensures that
   the selected cipher suite is the most preferred (by the Initiator)
   cipher suite supported by both parties.  For examples, see
   Section 6.3.2.

   If the selected cipher suite is not the first cipher suite that the
   Responder supports in SUITES_I received in message_1, then the
   Responder MUST abort the EDHOC session; see Section 5.2.3.  If
   SUITES_I in message_1 is manipulated, then the integrity verification
   of message_2 containing the transcript hash TH_2 will fail and the
   Initiator will abort the EDHOC session.

6.3.2.  Examples

   Assume that the Initiator supports the five cipher suites, 5, 6, 7,
   8, and 9, in decreasing order of preference.  Figures 8 and 9 show
   two examples of how the Initiator can format SUITES_I and how
   SUITES_R is used by Responders to give the Initiator information
   about the cipher suites that the Responder supports.

   In Example 1 (Figure 8), the Responder supports cipher suite 6 but
   not the initially selected cipher suite 5.  The Responder rejects the
   first message_1 with an error indicating support for suite 6 in
   SUITES_R.  The Initiator also supports suite 6 and therefore selects
   suite 6 in the second message_1.  The Initiator prepends in SUITES_I
   the selected suite 6 with the more preferred suites, in this case
   suite 5, to mitigate a potential attack on the cipher suite
   negotiation.

   Initiator                                                   Responder
   |              METHOD, SUITES_I = 5, G_X, C_I, EAD_1                |
   +------------------------------------------------------------------>|
   |                             message_1                             |
   |                                                                   |
   |                   ERR_CODE = 2, SUITES_R = 6                      |
   |<------------------------------------------------------------------+
   |                               error                               |
   |                                                                   |
   |             METHOD, SUITES_I = [5, 6], G_X, C_I, EAD_1            |
   +------------------------------------------------------------------>|
   |                             message_1                             |

                Figure 8: Cipher Suite Negotiation Example 1

   In Example 2 (Figure 9), the Responder supports cipher suites 8 and 9
   but not the more preferred (by the Initiator) cipher suites 5, 6 or
   7.  To illustrate the negotiation mechanics, we let the Initiator
   first make a guess that the Responder supports suite 6 but not suite
   5.  Since the Responder supports neither 5 nor 6, it rejects the
   first message_1 with an error indicating support for suites 8 and 9
   in SUITES_R (in any order).  The Initiator also supports suites 8 and
   9, and prefers suite 8, so it selects suite 8 in the second
   message_1.  The Initiator prepends in SUITES_I the selected suite 8
   with the more preferred suites in order of preference, in this case,
   suites 5, 6 and 7, to mitigate a potential attack on the cipher suite
   negotiation.

   Note 1.  If the Responder had supported suite 5, then the first
            message_1 would not have been accepted either, since the
            Responder observes that suite 5 is more preferred by the
            Initiator than the selected suite 6.  In that case, the
            Responder would have included suite 5 in SUITES_R of the
            response, and it would then have become the selected and
            only suite in the second message_1.

   Note 2.  For each message_1, the Initiator MUST generate a new
            ephemeral ECDH key pair matching the selected cipher suite.

   Initiator                                                   Responder
   |            METHOD, SUITES_I = [5, 6], G_X, C_I, EAD_1             |
   +------------------------------------------------------------------>|
   |                             message_1                             |
   |                                                                   |
   |                  ERR_CODE = 2, SUITES_R = [9, 8]                  |
   |<------------------------------------------------------------------+
   |                               error                               |
   |                                                                   |
   |           METHOD, SUITES_I = [5, 6, 7, 8], G_X, C_I, EAD_1        |
   +------------------------------------------------------------------>|
   |                             message_1                             |

                Figure 9: Cipher Suite Negotiation Example 2

6.4.  Unknown Credential Referenced

   Error code 3 is used for errors due to a received credential
   identifier (ID_CRED_R in message_2 or ID_CRED_I message_3) containing
   a reference to a credential that the receiving endpoint does not have
   access to.  The intent with this error code is that the endpoint who
   sent the credential identifier should, for the next EDHOC session,
   try another credential identifier supported according to the
   application profile.

   For example, an application profile could list x5t and x5chain as
   supported credential identifiers and state that x5t should be used if
   it can be assumed that the X.509 certificate is available at the
   receiving side.  This error code thus enables the certificate chain
   to be sent only when needed, bearing in mind that error messages are
   not protected so an adversary can try to cause unnecessary, large
   credential identifiers.

   For the error code 3, the error information SHALL be the CBOR simple
   value true (0xf5).  Error code 3 MUST NOT be used when the received
   credential identifier type is not supported.

7.  EDHOC Message Deduplication

   By default, EDHOC assumes that message duplication is handled by the
   transport (which is exemplified by CoAP in this section); see
   Appendix A.2.

   Deduplication of CoAP messages is described in Section 4.5 of
   [RFC7252].  This handles the case when the same Confirmable (CON)
   message is received multiple times due to missing acknowledgment on
   the CoAP messaging layer.  The recommended processing in [RFC7252] is
   that the duplicate message is acknowledged, but the received message
   is only processed once by the CoAP stack.

   Message deduplication is resource demanding and therefore not
   supported in all CoAP implementations.  Since EDHOC is targeting
   constrained environments, it is desirable that EDHOC can optionally
   support transport layers that do not handle message duplication.
   Special care is needed to avoid issues with duplicate messages; see
   Section 5.1.

   The guiding principle here is similar to the deduplication processing
   on the CoAP messaging layer, i.e., a received duplicate EDHOC message
   SHALL NOT result in another instance of the next EDHOC message.  The
   result MAY be that a duplicate next EDHOC message is sent, provided
   it is still relevant with respect to the current protocol state.  In
   any case, the received message MUST NOT be processed more than once
   in the same EDHOC session.  This is called "EDHOC message
   deduplication".

   An EDHOC implementation MAY store the previously sent EDHOC message
   to be able to resend it.

   In principle, if the EDHOC implementation would deterministically
   regenerate the identical EDHOC message previously sent, it would be
   possible to instead store the protocol state to be able to recreate
   and resend the previously sent EDHOC message.  However, even if the
   protocol state is fixed, the message generation may introduce
   differences that compromise security.  For example, in the generation
   of message_3, if I is performing a (non-deterministic) ECDSA
   signature (say, method 0 or 1 and cipher suite 2 or 3), then
   PLAINTEXT_3 is randomized, but K_3 and IV_3 are the same, leading to
   a key and nonce reuse.

   The EDHOC implementation MUST NOT store the previous protocol state
   and regenerate an EDHOC message if there is a risk that the same key
   and IV are used for two (or more) distinct messages.

   The previous message or protocol state MUST NOT be kept longer than
   what is required for retransmission, for example, in the case of CoAP
   transport, no longer than the EXCHANGE_LIFETIME (see Section 4.8.2 of
   [RFC7252]).

8.  Compliance Requirements

   In the absence of an application profile specifying otherwise:

   *  An implementation MAY support only an Initiator or only a
      Responder.

   *  An implementation MAY support only a single method.  None of the
      methods are mandatory to implement.

   *  Implementations MUST support 'kid' parameters.  None of the other
      COSE header parameters are mandatory to implement.

   *  An implementation MAY support only a single credential type (CCS,
      CWT, X.509, or C509).  None of the credential types are mandatory
      to implement.

   *  Implementations MUST support the EDHOC_Exporter.

   *  Implementations MAY support message_4.  Error codes (ERR_CODE) 1
      and 2 MUST be supported.

   *  Implementations MUST support EAD.

   *  Implementations MUST support cipher suites 2 and 3.  Cipher suites
      2 (AES-CCM-16-64-128, SHA-256, 8, P-256, ES256, AES-CCM-16-64-128,
      SHA-256) and 3 (AES-CCM-16-128-128, SHA-256, 16, P-256, ES256,
      AES-CCM-16-64-128, SHA-256) only differ in the size of the MAC
      length, so supporting one or both of these is not significantly
      different.  Implementations only need to implement the algorithms
      needed for their supported methods.

9.  Security Considerations

9.1.  Security Properties

   EDHOC has similar security properties as can be expected from the
   theoretical SIGMA-I protocol [SIGMA] and the Noise XX pattern
   [Noise], which are similar to methods 0 and 3, respectively.  Proven
   security properties are detailed in the security analysis
   publications referenced at the end of this section.

   Using the terminology from [SIGMA], EDHOC provides forward secrecy,
   mutual authentication with aliveness, consistency, and peer
   awareness.  As described in [SIGMA], message_3 provides peer
   awareness to the Responder, while message_4 provides peer awareness
   to the Initiator.  By including the authentication credentials in the
   transcript hash, EDHOC protects against an identity misbinding attack
   like the Duplicate Signature Key Selection (DSKS) that the MAC-then-
   Sign variant of SIGMA-I is otherwise vulnerable to.

   As described in [SIGMA], different levels of identity protection are
   provided to the Initiator and Responder.  EDHOC provides identity
   protection of the Initiator against active attacks and identity
   protection of the Responder against passive attacks.  An active
   attacker can get the credential identifier of the Responder by
   eavesdropping on the destination address used for transporting
   message_1 and then sending its own message_1 to the same address.
   The roles should be assigned to protect the most sensitive identity/
   identifier, typically that which is not possible to infer from
   routing information in the lower layers.

   EDHOC messages might change in transit due to a noisy channel or
   through modification by an attacker.  Changes in message_1 and
   message_2 (except Signature_or_MAC_2 when the signature scheme is not
   strongly unforgeable) are detected when verifying Signature_or_MAC_2.
   Changes to not strongly unforgeable Signature_or_MAC_2 and message_3
   are detected when verifying CIPHERTEXT_3.  Changes to message_4 are
   detected when verifying CIPHERTEXT_4.

   Compared to [SIGMA], EDHOC adds an explicit method type and expands
   the message authentication coverage to additional elements such as
   algorithms, external authorization data, and previous plaintext
   messages.  This protects against an attacker replaying messages or
   injecting messages from another EDHOC session.

   EDHOC also adds the selection of connection identifiers and
   downgrade-protected negotiation of cryptographic parameters, i.e., an
   attacker cannot affect the negotiated parameters.  A single session
   of EDHOC does not include negotiation of cipher suites, but it
   enables the Responder to verify that the selected cipher suite is the
   most preferred cipher suite by the Initiator that is supported by
   both the Initiator and Responder and to abort the EDHOC session if
   not.

   As required by [RFC7258], IETF protocols need to mitigate pervasive
   monitoring when possible.  Therefore, EDHOC only supports methods
   with ephemeral Diffie-Hellman and provides a key update function (see
   Appendix H) for lightweight application protocol rekeying.  Either of
   these provides forward secrecy, in the sense that compromise of the
   private authentication keys does not compromise past session keys
   (PRK_out) and compromise of a session key does not compromise past
   session keys.  Frequently re-running EDHOC with ephemeral Diffie-
   Hellman forces attackers to perform dynamic key exfiltration where
   the attacker must have continuous interactions with the collaborator,
   which is a significant sustained attack.

   To limit the effect of breaches, it is important to limit the use of
   symmetric group keys for bootstrapping.  Therefore, EDHOC strives to
   make the additional cost of using raw public keys and self-signed
   certificates as small as possible.  Raw public keys and self-signed
   certificates are not a replacement for a public key infrastructure
   but SHOULD be used instead of symmetric group keys for bootstrapping.

   Compromise of the long-term keys (private signature or static DH
   keys) does not compromise the security of completed EDHOC sessions.
   Compromising the private authentication keys of one party lets an
   active attacker impersonate that compromised party in EDHOC sessions
   with other parties but does not let the attacker impersonate other
   parties in EDHOC sessions with the compromised party.  Compromise of
   the long-term keys does not enable a passive attacker to compromise
   future session keys (PRK_out).  Compromise of the HKDF input
   parameters (ECDH shared secret) leads to compromise of all session
   keys derived from that compromised shared secret.  Compromise of one
   session key does not compromise other session keys.  Compromise of
   PRK_out leads to compromise of all keying material derived with the
   EDHOC_Exporter.

   Based on the cryptographic algorithm requirements (Section 9.3),
   EDHOC provides a minimum of 64-bit security against online brute
   force attacks and a minimum of 128-bit security against offline brute
   force attacks.  To break 64-bit security against online brute force,
   an attacker would on average have to send 4.3 billion messages per
   second for 68 years, which is infeasible in constrained IoT radio
   technologies.  A forgery against a 64-bit MAC in EDHOC breaks the
   security of all future application data, while a forgery against a
   64-bit MAC in the subsequent application protocol (e.g., OSCORE
   [RFC8613]) typically only breaks the security of the data in the
   forged packet.

   As the EDHOC session is aborted when verification fails, the security
   against online attacks is given by the sum of the strength of the
   verified signatures and MACs (including MAC in AEAD).  As an example,
   if EDHOC is used with method 3, cipher suite 2, and message_4, the
   Responder is authenticated with 128-bit security against online
   attacks (the sum of the 64-bit MACs in message_2 and message_4).  The
   same principle applies for MACs in an application protocol keyed by
   EDHOC as long as EDHOC is re-run when verification of the first MACs
   in the application protocol fails.  As an example, if EDHOC with
   method 3 and cipher suite 2 is used as in Figure 2 of
   [EDHOC-CoAP-OSCORE], 128-bit mutual authentication against online
   attacks can be achieved after completion of the first OSCORE request
   and response.

   After sending message_3, the Initiator is assured that no other party
   than the Responder can compute the key PRK_out.  While the Initiator
   can securely send protected application data, the Initiator SHOULD
   NOT persistently store the keying material PRK_out until the
   Initiator has verified message_4 or a message protected with a
   derived application key, such as an OSCORE message, from the
   Responder.  After verifying message_3, the Responder is assured that
   an honest Initiator has computed the key PRK_out.  The Responder can
   securely derive and store the keying material PRK_out and send
   protected application data.

   External authorization data sent in message_1 (EAD_1) or message_2
   (EAD_2) should be considered unprotected by EDHOC; see Section 9.5.
   EAD_2 is encrypted, but the Responder has not yet authenticated the
   Initiator and the encryption does not provide confidentiality against
   active attacks.

   External authorization data sent in message_3 (EAD_3) or message_4
   (EAD_4) is protected between the Initiator and Responder by the
   protocol, but note that EAD fields may be used by the application
   before the message verification is completed; see Section 3.8.
   Designing a secure mechanism that uses EAD is not necessarily
   straightforward.  This document only provides the EAD transport
   mechanism, but the problem of agreeing on the surrounding context and
   the meaning of the information passed to and from the application
   remains.  Any new uses of EAD should be subject to careful review.

   Key Compromise Impersonation (KCI):  In EDHOC authenticated with
      signature keys, EDHOC provides KCI protection against an attacker
      having access to the long-term key or the ephemeral secret key.
      With static Diffie-Hellman key authentication, KCI protection
      would be provided against an attacker having access to the long-
      term Diffie-Hellman key but not to an attacker having access to
      the ephemeral secret key.  Note that the term KCI has typically
      been used for compromise of long-term keys and that an attacker
      with access to the ephemeral secret key can only attack that
      specific EDHOC session.

   Repudiation:  If an endpoint authenticates with a signature, the
      other endpoint can prove that the endpoint performed a run of the
      protocol by presenting the data being signed as well as the
      signature itself.  With static Diffie-Hellman key authentication,
      the authenticating endpoint can deny having participated in the
      protocol.

   Earlier versions of EDHOC have been formally analyzed [Bruni18]
   [Norrman20] [CottierPointcheval22] [Jacomme23] [GuentherIlunga22],
   and the specification has been updated based on the analysis.

9.2.  Cryptographic Considerations

   The SIGMA protocol requires that the encryption of message_3 provides
   confidentiality against active attackers and EDHOC message_4 relies
   on the use of authenticated encryption.  Hence, the message
   authenticating functionality of the authenticated encryption in EDHOC
   is critical, i.e., authenticated encryption MUST NOT be replaced by
   plain encryption only, even if authentication is provided at another
   level or through a different mechanism.

   To reduce message overhead, EDHOC does not use explicit nonces and
   instead relies on the ephemeral public keys to provide randomness to
   each EDHOC session.  A good amount of randomness is important for the
   key generation to provide liveness and to protect against
   interleaving attacks.  For this reason, the ephemeral keys MUST NOT
   be used in more than one EDHOC message, and both parties SHALL
   generate fresh, random ephemeral key pairs.  Note that an ephemeral
   key may be used to calculate several ECDH shared secrets.  When
   static Diffie-Hellman authentication is used, the same ephemeral key
   is used in both ephemeral-ephemeral and ephemeral-static ECDH.

   As discussed in [SIGMA], the encryption of message_2 only needs to
   protect against a passive attacker since active attackers can always
   get the Responder's identity by sending their own message_1.  EDHOC
   uses the EDHOC_Expand function (typically HKDF-Expand) as a binary
   additive stream cipher that is proven secure as long as the expand
   function is a Pseudorandom Function (PRF).  HKDF-Expand is not often
   used as a stream cipher as it is slow on long messages, and most
   applications require both confidentiality with indistinguishability
   under adaptive chosen ciphertext attack (IND-CCA2) as well as
   integrity protection.  For the encryption of message_2, any speed
   difference is negligible, IND-CCA2 does not increase security, and
   integrity is provided by the inner MAC (and signature depending on
   method).

   Requirements for how to securely generate, validate, and process the
   public keys depend on the elliptic curve.  For X25519 and X448, the
   requirements are defined in [RFC7748].  For X25519 and X448, the
   check for all-zero output as specified in Section 6 of [RFC7748] MUST
   be done.  For secp256r1, secp384r1, and secp521r1, the requirements
   are defined in Section 5 of [SP-800-56A].  For secp256r1, secp384r1,
   and secp521r1, at least partial public key validation MUST be done.

   The same authentication credential MAY be used for both the Initiator
   and Responder roles.  As noted in Section 12 of [RFC9052], the use of
   a single key for multiple algorithms is strongly discouraged unless
   proven secure by a dedicated cryptographic analysis.  In particular,
   this recommendation applies to using the same private key for static
   Diffie-Hellman authentication and digital signature authentication.
   A preliminary conjecture is that a minor change to EDHOC may be
   sufficient to fit the analysis of a secure shared signature and ECDH
   key usage in [Degabriele11] and [Thormarker21].  Note that
   Section 5.6.3.2 of [SP-800-56A] allows a key agreement key pair to be
   used with a signature algorithm in certificate requests.

   The property that a completed EDHOC session implies that another
   identity has been active is upheld as long as the Initiator does not
   have its own identity in the set of Responder identities it is
   allowed to communicate with.  In trust-on-first-use (TOFU) use cases
   (see Appendix D.5), the Initiator should verify that the Responder's
   identity is not equal to its own.  Any future EDHOC methods using,
   e.g., PSKs might need to mitigate this in other ways.  However, an
   active attacker can gain information about the set of identities an
   Initiator is willing to communicate with.  If the Initiator is
   willing to communicate with all identities except its own, an
   attacker can determine that a guessed Initiator identity is correct.
   To not leak any long-term identifiers, using a freshly generated
   authentication key as an identity in each initial TOFU session is
   RECOMMENDED.

   NIST SP 800-56A [SP-800-56A] forbids deriving secret and non-secret
   randomness from the same Key Derivation Function (KDF) instance, but
   this decision has been criticized by Krawczyk in [HKDFpaper] and
   doing so is common practice.  In addition to IVs, other examples are
   the challenge in Extensible Authentication Protocol Tunneled
   Transport Layer Security (EAP-TTLS), the RAND in 3GPP Authentication
   and Key Agreement (AKA), and the Session-Id in EAP-TLS 1.3.  Note
   that part of KEYSTREAM_2 is also non-secret randomness, as it is
   known or predictable to an attacker.  The more recent NIST SP 800-108
   [SP-800-108] aligns with [HKDFpaper] and states that, for a secure
   KDF, the revelation of one portion of the derived keying material
   must not degrade the security of any other portion of that keying
   material.

9.3.  Cipher Suites and Cryptographic Algorithms

   When using a private cipher suite or registering new cipher suites,
   the choice of the key length used in the different algorithms needs
   to be harmonized so that a sufficient security level is maintained
   for authentication credentials, the EDHOC session, and the protection
   of application data.  The Initiator and Responder should enforce a
   minimum security level.

   The output size of the EDHOC hash algorithm MUST be at least 256
   bits.  In particular, the hash algorithms SHA-1 and SHA-256/64
   (SHA-256 truncated to 64 bits) SHALL NOT be supported for use in
   EDHOC except for certificate identification with x5t and c5t.  For
   security considerations of SHA-1, see [RFC6194].  As EDHOC integrity
   protects all the authentication credentials, the choice of hash
   algorithm in x5t and c5t does not affect security and using the same
   hash algorithm as in the cipher suite, but with as much truncation as
   possible, is RECOMMENDED.  That is, when the EDHOC hash algorithm is
   SHA-256, using SHA-256/64 in x5t and c5t is RECOMMENDED.  The EDHOC
   MAC length MUST be at least 8 bytes and the tag length of the EDHOC
   AEAD algorithm MUST be at least 64 bits.  Note that secp256k1 is only
   defined for use with ECDSA and not for ECDH.  Note that some COSE
   algorithms are marked as not recommended in the COSE IANA registry.

9.4.  Post-Quantum Considerations

   As of the publication of this specification, it is unclear when or
   even if a quantum computer of sufficient size and power to exploit
   public key cryptography will exist.  Deployments that need to
   consider risks decades into the future should transition to Post-
   Quantum Cryptography (PQC) in the not-too-distant future.  Many other
   systems should take a slower wait-and-see approach where PQC is
   phased in when the quantum threat is more imminent.  Current PQC
   algorithms have limitations compared to Elliptic Curve Cryptography
   (ECC), and the data sizes would be problematic in many constrained
   IoT systems.

   Symmetric algorithms used in EDHOC, such as SHA-256 and AES-CCM-
   16-64-128, are practically secure against even large quantum
   computers.  Two of NIST's security levels for quantum-resistant
   public key cryptography are based on AES-128 and SHA-256.  A quantum
   computer will likely be expensive and slow due to heavy error
   correction.  Grover's algorithm, which is proven to be optimal,
   cannot effectively be parallelized.  It will provide little or no
   advantage in attacking AES, and AES-128 will remain secure for
   decades to come [NISTPQC].

   EDHOC supports all signature algorithms defined by COSE, including
   PQC signature algorithms such as HSS-LMS.  EDHOC is currently only
   specified for use with key exchange algorithms of type ECDH curves,
   but any Key Encapsulation Method (KEM), including PQC KEMs, can be
   used in method 0.  While the key exchange in method 0 is specified
   with the terms of the Diffie-Hellman protocol, the key exchange
   adheres to a KEM interface: G_X is then the public key of the
   Initiator, G_Y is the encapsulation, and G_XY is the shared secret.
   Use of PQC KEMs to replace static DH authentication would likely
   require a specification updating EDHOC with new methods.

9.5.  Unprotected Data and Privacy

   The Initiator and Responder must make sure that unprotected data and
   metadata do not reveal any sensitive information.  This also applies
   for encrypted data sent to an unauthenticated party.  In particular,
   it applies to EAD_1, ID_CRED_R, EAD_2, and error messages.  Using the
   same EAD_1 in several EDHOC sessions allows passive eavesdroppers to
   correlate the different sessions.  Note that even if ead_value is
   encrypted outside of EDHOC, the ead_labels in EAD_1 are revealed to
   passive attackers and the ead_labels in EAD_2 are revealed to active
   attackers.  Another consideration is that the list of supported
   cipher suites may potentially be used to identify the application.
   The Initiator and Responder must also make sure that unauthenticated
   data does not trigger any harmful actions.  In particular, this
   applies to EAD_1 and error messages.

   An attacker observing network traffic may use connection identifiers
   sent in clear in EDHOC or the subsequent application protocol to
   correlate packets sent on different paths or at different times.  The
   attacker may use this information for traffic flow analysis or to
   track an endpoint.  Application protocols using connection
   identifiers from EDHOC SHOULD provide mechanisms to update the
   connection identifiers and MAY provide mechanisms to issue several
   simultaneously active connection identifiers.  See [RFC9000] for a
   non-constrained example of such mechanisms.  Connection identifiers
   can, e.g., be chosen randomly among the set of unused 1-byte
   connection identifiers.  Connection identity privacy mechanisms are
   only useful when there are not fixed identifiers, such as IP address
   or MAC address in the lower layers.

9.6.  Updated Internet Threat Model Considerations

   Since the publication of [RFC3552], there has been an increased
   awareness of the need to protect against endpoints that are
   compromised or malicious or whose interests simply do not align with
   the interests of users [THREAT-MODEL-GUIDANCE].  [RFC7624] describes
   an updated threat model for Internet confidentiality; see
   Section 9.1.  [THREAT-MODEL-GUIDANCE] further expands the threat
   model.  Implementations and users should take these threat models
   into account and consider actions to reduce the risk of tracking by
   other endpoints.  In particular, even data sent protected to the
   other endpoint, such as ID_CRED fields and EAD fields, can be used
   for tracking; see Section 2.7 of [THREAT-MODEL-GUIDANCE].

   The fields ID_CRED_I, ID_CRED_R, EAD_2, EAD_3, and EAD_4 have
   variable length, and information regarding the length may leak to an
   attacker.  A passive attacker may, e.g., be able to differentiate
   endpoints using identifiers of different length.  To mitigate this
   information leakage, an implementation may ensure that the fields
   have a fixed length or use padding.  An implementation may, e.g.,
   only use fixed length identifiers like 'kid' of length 1.
   Alternatively, padding may be used (see Section 3.8.1) to hide the
   true length of, e.g., certificates by value in 'x5chain' or 'c5c'.

9.7.  Denial of Service

   EDHOC itself does not provide countermeasures against denial-of-
   service attacks.  In particular, by sending a number of new or
   replayed message_1, an attacker may cause the Responder to allocate
   the state, perform cryptographic operations, and amplify messages.
   To mitigate such attacks, an implementation SHOULD make use of
   available lower layer mechanisms.  For instance, when EDHOC is
   transferred as an exchange of CoAP messages, the CoAP server can use
   the Echo option defined in [RFC9175], which forces the CoAP client to
   demonstrate reachability at its apparent network address.  To avoid
   an additional round trip, the Initiator can reduce the amplification
   factor by padding message_1, i.e., using EAD_1; see Section 3.8.1.
   Note that while the Echo option mitigates some resource exhaustion
   aspects of spoofing, it does not protect against a distributed
   denial-of-service attack made by real, potentially compromised,
   clients.  Similarly, limiting amplification only reduces the impact,
   which still may be significant because of a large number of clients
   engaged in the attack.

   An attacker can also send a faked message_2, message_3, message_4, or
   error in an attempt to trick the receiving party to send an error
   message and abort the EDHOC session.  EDHOC implementations MAY
   evaluate if a received message is likely to have been forged by an
   attacker and ignore it without sending an error message or aborting
   the EDHOC session.

9.8.  Implementation Considerations

   The availability of a secure random number generator is essential for
   the security of EDHOC.  If no true random number generator is
   available, a random seed MUST be provided from an external source and
   used with a cryptographically secure pseudorandom number generator.
   As each pseudorandom number must only be used once, an implementation
   needs to get a unique input to the pseudorandom number generator
   after reboot or continuously store state in nonvolatile memory.
   Appendix B.1.1 of [RFC8613] describes issues and solution approaches
   for writing to nonvolatile memory.  Intentionally or unintentionally
   weak or predictable pseudorandom number generators can be abused or
   exploited for malicious purposes.  [RFC8937] describes a way for
   security protocol implementations to augment their (pseudo)random
   number generators using a long-term private key and a deterministic
   signature function.  This improves randomness from broken or
   otherwise subverted random number generators.  The same idea can be
   used with other secrets and functions, such as a Diffie-Hellman
   function or a symmetric secret, and a PRF like HMAC or KMAC.  It is
   RECOMMENDED to not trust a single source of randomness and to not put
   unaugmented random numbers on the wire.

   For many constrained IoT devices, it is problematic to support
   several crypto primitives.  Existing devices can be expected to
   support either ECDSA or Edwards-curve Digital Signature Algorithm
   (EdDSA).  If ECDSA is supported, "deterministic ECDSA", as specified
   in [RFC6979], MAY be used.  Pure deterministic elliptic-curve
   signatures, such as deterministic ECDSA and EdDSA, have gained
   popularity over randomized ECDSA as their security does not depend on
   a source of high-quality randomness.  Recent research has however
   found that implementations of these signature algorithms may be
   vulnerable to certain side-channel and fault injection attacks due to
   their determinism.  For example, see Section 1 of [HEDGED-ECC-SIGS]
   for a list of attack papers.  As suggested in Section 2.1.1 of
   [RFC9053], this can be addressed by combining randomness and
   determinism.

   Appendix D of [CURVE-REPR] describes how Montgomery curves, such as
   X25519 and X448, and (twisted) Edwards curves, such as Ed25519 and
   Ed448, can be mapped to and from short-Weierstrass form for
   implementations on platforms that accelerate elliptic curve group
   operations in short-Weierstrass form.

   All private keys, symmetric keys, and IVs MUST be secret.  Only the
   Responder SHALL have access to the Responder's private authentication
   key, and only the Initiator SHALL have access to the Initiator's
   private authentication key.  Implementations should provide
   countermeasures to side-channel attacks, such as timing attacks.
   Intermediate computed values, such as ephemeral ECDH keys and ECDH
   shared secrets, MUST be deleted after key derivation is completed.

   The Initiator and Responder are responsible for verifying the
   integrity and validity of certificates.  Verification of validity may
   require the use of a Real-Time Clock (RTC).  The selection of trusted
   certification authorities (CAs) should be done very carefully and
   certificate revocation should be supported.  The choice of revocation
   mechanism is left to the application.  For example, in case of X.509
   certificates, Certificate Revocation Lists [RFC5280] or the Online
   Certificate Status Protocol (OCSP) [RFC6960] may be used.

   Similar considerations as for certificates are needed for CWT/CCS.
   The endpoints are responsible for verifying the integrity and
   validity of CWT/CCS and to handle revocation.  The application needs
   to determine what trust anchors are relevant and have a well-defined
   trust-establishment process.  A self-signed certificate / CWT or CCS
   appearing in the protocol cannot be a trigger to modify the set of
   trust anchors.  One common way for a new trust anchor to be added to
   (or removed from) a device is by means firmware upgrade.  See
   [RFC9360] for a longer discussion on trust and validation in
   constrained devices.

   Just like for certificates, the contents of the COSE header
   parameters 'kcwt' and 'kccs' defined in Section 10.6 must be
   processed as untrusted inputs.  Endpoints that intend to rely on the
   assertions made by a CWT/CCS obtained from any of these methods need
   to validate the contents.  For 'kccs', which enables transport of raw
   public keys, the data structure used does not include any protection
   or verification data. 'kccs' may be used for unauthenticated
   operations, e.g., trust on first use, with the limitations and
   caveats entailed; see Appendix D.5.

   The Initiator and Responder are allowed to select connection
   identifiers C_I and C_R, respectively, for the other party to use in
   the ongoing EDHOC session as well as in a subsequent application
   protocol (e.g., OSCORE [RFC8613]).  The choice of the connection
   identifier is not security critical in EDHOC but intended to simplify
   the retrieval of the right security context in combination with using
   short identifiers.  If the wrong connection identifier of the other
   party is used in a protocol message, it will result in the receiving
   party not being able to retrieve a security context (which will abort
   the EDHOC session) or retrieve the wrong security context (which also
   aborts the EDHOC session as the message cannot be verified).

   If two nodes unintentionally initiate two simultaneous EDHOC sessions
   with each other, even if they only want to complete a single EDHOC
   session, they MAY abort the EDHOC session with the lexicographically
   smallest G_X.  Note that in cases where several EDHOC sessions with
   different parameter sets (method, COSE headers, etc.) are used, an
   attacker can affect which parameter set will be used by blocking some
   of the parameter sets.

   If supported by the device, it is RECOMMENDED that at least the long-
   term private keys are stored in a Trusted Execution Environment (TEE)
   (for example, see [RFC9397]) and that sensitive operations using
   these keys are performed inside the TEE.  To achieve even higher
   security, it is RECOMMENDED that additional operations such as
   ephemeral key generation, all computations of shared secrets, and
   storage of the PRK keys can be done inside the TEE.  The use of a TEE
   aims at preventing code within that environment to be tampered with
   and preventing data used by such code to be read or tampered with by
   code outside that environment.

   Note that HKDF-Expand has a relatively small maximum output length of
   255 ⋅ hash_length, where hash_length is the output size in bytes of
   the EDHOC hash algorithm of the selected cipher suite.  This means
   that when SHA-256 is used as a hash algorithm, PLAINTEXT_2 cannot be
   longer than 8160 bytes.  This is probably not a limitation for most
   intended applications, but to be able to support, for example, long
   certificate chains or large external authorization data, there is a
   backwards compatible method specified in Appendix G.

   The sequence of transcript hashes in EDHOC (TH_2, TH_3, and TH_4)
   does not make use of a so-called running hash.  This is a design
   choice, as running hashes are often not supported on constrained
   platforms.

   When parsing a received EDHOC message, implementations MUST abort the
   EDHOC session if the message does not comply with the CDDL for that
   message.  Implementations are not required to support non-
   deterministic encodings and MAY abort the EDHOC session if the
   received EDHOC message is not encoded using deterministic CBOR.
   Implementations MUST abort the EDHOC session if validation of a
   received public key fails or if any cryptographic field has the wrong
   length.  It is RECOMMENDED to abort the EDHOC session if the received
   EDHOC message is not encoded using deterministic CBOR.

10.  IANA Considerations

   This section gives IANA considerations and, unless otherwise noted,
   conforms with [RFC8126].

10.1.  EDHOC Exporter Label Registry

   IANA has created a new registry under the new registry group
   "Ephemeral Diffie-Hellman Over COSE (EDHOC)" as follows:

   Registry Name:  EDHOC Exporter Labels

   Reference:  RFC 9528

        +=============+==============================+===========+
        | Label       | Description                  | Reference |
        +=============+==============================+===========+
        | 0           | Derived OSCORE Master Secret | RFC 9528  |
        +-------------+------------------------------+-----------+
        | 1           | Derived OSCORE Master Salt   | RFC 9528  |
        +-------------+------------------------------+-----------+
        | 2-22        | Unassigned                   |           |
        +-------------+------------------------------+-----------+
        | 23          | Reserved                     | RFC 9528  |
        +-------------+------------------------------+-----------+
        | 24-32767    | Unassigned                   |           |
        +-------------+------------------------------+-----------+
        | 32768-65535 | Reserved for Private Use     |           |
        +-------------+------------------------------+-----------+

                      Table 4: EDHOC Exporter Labels

   This registry also has a "Change Controller" field.  For
   registrations made by IETF documents, the IETF is listed.

                 +=============+=========================+
                 | Range       | Registration Procedures |
                 +=============+=========================+
                 | 0-23        | Standards Action        |
                 +-------------+-------------------------+
                 | 24-32767    | Expert Review           |
                 +-------------+-------------------------+
                 | 32768-65535 | Private Use             |
                 +-------------+-------------------------+

                    Table 5: Registration Procedures for
                           EDHOC Exporter Labels

10.2.  EDHOC Cipher Suites Registry

   IANA has created a new registry under the new registry group
   "Ephemeral Diffie-Hellman Over COSE (EDHOC)" as follows:

   Registry Name:  EDHOC Cipher Suites

   Reference:  RFC 9528

   The columns of the registry are Value, Array, Description, and
   Reference, where Value is an integer and the other columns are text
   strings.  The initial contents of the registry are:

   +=======+================+=============================+===========+
   | Value | Array          | Description                 | Reference |
   +=======+================+=============================+===========+
   | -24   | N/A            | Private Use                 | RFC 9528  |
   +-------+----------------+-----------------------------+-----------+
   | -23   | N/A            | Private Use                 | RFC 9528  |
   +-------+----------------+-----------------------------+-----------+
   | -22   | N/A            | Private Use                 | RFC 9528  |
   +-------+----------------+-----------------------------+-----------+
   | -21   | N/A            | Private Use                 | RFC 9528  |
   +-------+----------------+-----------------------------+-----------+
   | 0     | 10, -16, 8, 4, | AES-CCM-16-64-128, SHA-256, | RFC 9528  |
   |       | -8, 10, -16    | 8, X25519, EdDSA,           |           |
   |       |                | AES-CCM-16-64-128, SHA-256  |           |
   +-------+----------------+-----------------------------+-----------+
   | 1     | 30, -16, 16,   | AES-CCM-16-128-128,         | RFC 9528  |
   |       | 4, -8, 10, -16 | SHA-256, 16, X25519, EdDSA, |           |
   |       |                | AES-CCM-16-64-128, SHA-256  |           |
   +-------+----------------+-----------------------------+-----------+
   | 2     | 10, -16, 8, 1, | AES-CCM-16-64-128, SHA-256, | RFC 9528  |
   |       | -7, 10, -16    | 8, P-256, ES256,            |           |
   |       |                | AES-CCM-16-64-128, SHA-256  |           |
   +-------+----------------+-----------------------------+-----------+
   | 3     | 30, -16, 16,   | AES-CCM-16-128-128,         | RFC 9528  |
   |       | 1, -7, 10, -16 | SHA-256, 16, P-256, ES256,  |           |
   |       |                | AES-CCM-16-64-128, SHA-256  |           |
   +-------+----------------+-----------------------------+-----------+
   | 4     | 24, -16, 16,   | ChaCha20/Poly1305, SHA-256, | RFC 9528  |
   |       | 4, -8, 24, -16 | 16, X25519, EdDSA,          |           |
   |       |                | ChaCha20/Poly1305, SHA-256  |           |
   +-------+----------------+-----------------------------+-----------+
   | 5     | 24, -16, 16,   | ChaCha20/Poly1305, SHA-256, | RFC 9528  |
   |       | 1, -7, 24, -16 | 16, P-256, ES256,           |           |
   |       |                | ChaCha20/Poly1305, SHA-256  |           |
   +-------+----------------+-----------------------------+-----------+
   | 6     | 1, -16, 16, 4, | A128GCM, SHA-256, 16,       | RFC 9528  |
   |       | -7, 1, -16     | X25519, ES256, A128GCM,     |           |
   |       |                | SHA-256                     |           |
   +-------+----------------+-----------------------------+-----------+
   | 23    |                | Reserved                    | RFC 9528  |
   +-------+----------------+-----------------------------+-----------+
   | 24    | 3, -43, 16, 2, | A256GCM, SHA-384, 16,       | RFC 9528  |
   |       | -35, 3, -43    | P-384, ES384, A256GCM,      |           |
   |       |                | SHA-384                     |           |
   +-------+----------------+-----------------------------+-----------+
   | 25    | 24, -45, 16,   | ChaCha20/Poly1305,          | RFC 9528  |
   |       | 5, -8, 24, -45 | SHAKE256, 16, X448, EdDSA,  |           |
   |       |                | ChaCha20/Poly1305, SHAKE256 |           |
   +-------+----------------+-----------------------------+-----------+

                       Table 6: EDHOC Cipher Suites

          +===============+=====================================+
          | Range         | Registration Procedures             |
          +===============+=====================================+
          | -65536 to -25 | Specification Required              |
          +---------------+-------------------------------------+
          | -24 to -21    | Private Use                         |
          +---------------+-------------------------------------+
          | -20 to 23     | Standards Action with Expert Review |
          +---------------+-------------------------------------+
          | 24 to 65535   | Specification Required              |
          +---------------+-------------------------------------+

             Table 7: Registration Procedures for EDHOC Cipher
                                   Suites

10.3.  EDHOC Method Type Registry

   IANA has created a new registry under the new registry group
   "Ephemeral Diffie-Hellman Over COSE (EDHOC)" as follows:

   Registry Name:  EDHOC Method Types

   Reference:  RFC 9528

   The columns of the registry are Value, Initiator Authentication Key,
   Responder Authentication Key, and Reference, where Value is an
   integer and the key columns are text strings describing the
   authentication keys.

   The initial contents of the registry are shown in Table 2.  Method 23
   is Reserved.

          +===============+=====================================+
          | Range         | Registration Procedures             |
          +===============+=====================================+
          | -65536 to -25 | Specification Required              |
          +---------------+-------------------------------------+
          | -24 to 23     | Standards Action with Expert Review |
          +---------------+-------------------------------------+
          | 24 to 65535   | Specification Required              |
          +---------------+-------------------------------------+

          Table 8: Registration Procedures for EDHOC Method Types

10.4.  EDHOC Error Codes Registry

   IANA has created a new registry under the new registry group
   "Ephemeral Diffie-Hellman Over COSE (EDHOC)" as follows:

   Registry Name:  EDHOC Error Codes

   Reference:  RFC 9528

   The columns of the registry are ERR_CODE, ERR_INFO Type, Description,
   Change Controller, and Reference, where ERR_CODE is an integer,
   ERR_INFO is a CDDL defined type, and Description is a text string.
   The initial contents of the registry are shown in Table 3.  Error
   code 23 is Reserved.  This registry also has a "Change Controller"
   field.  For registrations made by IETF documents, the IETF is listed.

                +===============+=========================+
                | Range         | Registration Procedures |
                +===============+=========================+
                | -65536 to -25 | Expert Review           |
                +---------------+-------------------------+
                | -24 to 23     | Standards Action        |
                +---------------+-------------------------+
                | 24 to 65535   | Expert Review           |
                +---------------+-------------------------+

                    Table 9: Registration Procedures for
                             EDHOC Error Codes

10.5.  EDHOC External Authorization Data Registry

   IANA has created a new registry under the new registry group
   "Ephemeral Diffie-Hellman Over COSE (EDHOC)" as follows:

   Registry Name:  EDHOC External Authorization Data

   Reference:  RFC 9528

   The columns of the registry are Name, Label, Description, and
   Reference, where Label is a nonnegative integer and the other columns
   are text strings.  The initial contents of the registry are shown in
   Table 10.  EAD label 23 is Reserved.

         +=========+=======+====================+===============+
         | Name    | Label | Description        | Reference     |
         +=========+=======+====================+===============+
         | Padding | 0     | Randomly generated | RFC 9528,     |
         |         |       | CBOR byte string   | Section 3.8.1 |
         +---------+-------+--------------------+---------------+
         |         | 23    | Reserved           | RFC 9528      |
         +---------+-------+--------------------+---------------+

                        Table 10: EDHOC EAD Labels

           +=============+=====================================+
           | Range       | Registration Procedures             |
           +=============+=====================================+
           | 0 to 23     | Standards Action with Expert Review |
           +-------------+-------------------------------------+
           | 24 to 65535 | Specification Required              |
           +-------------+-------------------------------------+

              Table 11: Registration Procedures for EDHOC EAD
                                   Labels

10.6.  COSE Header Parameters Registry

   IANA has registered the following entries in the "COSE Header
   Parameters" registry under the registry group "CBOR Object Signing
   and Encryption (COSE)" (see Table 12).  The value of the 'kcwt'
   header parameter is a COSE Web Token (CWT) [RFC8392], and the value
   of the 'kccs' header parameter is a CWT Claims Set (CCS); see
   Section 1.4.  The CWT/CCS must contain a COSE_Key in a 'cnf' claim
   [RFC8747].  The Value Registry column for this item is empty and
   omitted from the table below.

     +======+=======+===============+===============================+
     | Name | Label | Value Type    | Description                   |
     +======+=======+===============+===============================+
     | kcwt | 13    | COSE_Messages | A CBOR Web Token (CWT)        |
     |      |       |               | containing a COSE_Key in a    |
     |      |       |               | 'cnf' claim and possibly      |
     |      |       |               | other claims.  CWT is defined |
     |      |       |               | in RFC 8392.  COSE_Messages   |
     |      |       |               | is defined in RFC 9052.       |
     +------+-------+---------------+-------------------------------+
     | kccs | 14    | map           | A CWT Claims Set (CCS)        |
     |      |       |               | containing a COSE_Key in a    |
     |      |       |               | 'cnf' claim and possibly      |
     |      |       |               | other claims.  CCS is defined |
     |      |       |               | in RFC 8392.                  |
     +------+-------+---------------+-------------------------------+

                  Table 12: COSE Header Parameter Labels

10.7.  Well-Known URI Registry

   IANA has added the well-known URI "edhoc" to the "Well-Known URIs"
   registry.

   URI Suffix:  edhoc

   Change Controller:  IETF

   Reference:  RFC 9528

   Related Information:  None

10.8.  Media Types Registry

   IANA has added the media types "application/edhoc+cbor-seq" and
   "application/cid-edhoc+cbor-seq" to the "Media Types" registry.

10.8.1.  application/edhoc+cbor-seq Media Type Registration

   Type name:  application

   Subtype name:  edhoc+cbor-seq

   Required parameters:  N/A

   Optional parameters:  N/A

   Encoding considerations:  binary

   Security considerations:  See Section 7 of RFC 9528.

   Interoperability considerations:  N/A

   Published specification:  RFC 9528

   Applications that use this media type:  To be identified

   Fragment identifier considerations:  N/A

   Additional information:

      Magic number(s):  N/A

      File extension(s):  N/A

      Macintosh file type code(s):  N/A

   Person & email address to contact for further information:  See
      "Authors' Addresses" section in RFC 9528.

   Intended usage:  COMMON

   Restrictions on usage:  N/A

   Author:  See "Authors' Addresses" section.

   Change Controller:  IETF

10.8.2.  application/cid-edhoc+cbor-seq Media Type Registration

   Type name:  application

   Subtype name:  cid-edhoc+cbor-seq

   Required parameters:  N/A

   Optional parameters:  N/A

   Encoding considerations:  binary

   Security considerations:  See Section 7 of RFC 9528.

   Interoperability considerations:  N/A

   Published specification:  RFC 9528

   Applications that use this media type:  To be identified

   Fragment identifier considerations:  N/A

   Additional information:

      Magic number(s):  N/A

      File extension(s):  N/A

      Macintosh file type code(s):  N/A

   Person & email address to contact for further information:  See
      "Authors' Addresses" section in RFC 9528.

   Intended usage:  COMMON

   Restrictions on usage:  N/A

   Author:  See "Authors' Addresses" section.

   Change Controller:  IETF

10.9.  CoAP Content-Formats Registry

   IANA has added the media types "application/edhoc+cbor-seq" and
   "application/cid-edhoc+cbor-seq" to the "CoAP Content-Formats"
   registry under the registry group "Constrained RESTful Environments
   (CoRE) Parameters".

   +================================+================+====+===========+
   | Content Type                   | Content Coding | ID | Reference |
   +================================+================+====+===========+
   | application/edhoc+cbor-seq     | -              | 64 | RFC 9528  |
   +--------------------------------+----------------+----+-----------+
   | application/cid-edhoc+cbor-seq | -              | 65 | RFC 9528  |
   +--------------------------------+----------------+----+-----------+

                    Table 13: CoAP Content-Format IDs

10.10.  Resource Type (rt=) Link Target Attribute Values Registry

   IANA has added the resource type "core.edhoc" to the "Resource Type
   (rt=) Link Target Attribute Values" registry under the registry group
   "Constrained RESTful Environments (CoRE) Parameters".

   Value:  core.edhoc

   Description:  EDHOC resource

   Reference:  RFC 9528

10.11.  Expert Review Instructions

   The IANA registries established in this document are defined as
   "Expert Review", "Specification Required", or "Standards Action with
   Expert Review".  This section gives some general guidelines for what
   the experts should be looking for, but they are being designated as
   experts for a reason so they should be given substantial latitude.

   Expert reviewers should take into consideration the following points:

   *  The clarity and correctness of registrations.  Experts are
      expected to check the clarity of purpose and use of the requested
      entries.  Expert needs to make sure the values of algorithms are
      taken from the right registry when that is required.  Experts
      should consider requesting an opinion on the correctness of
      registered parameters from relevant IETF working groups.
      Encodings that do not meet these objectives of clarity and
      completeness should not be registered.

   *  The expected usage of fields when approving code point assignment.
      The length of the encoded value should be weighed against how many
      code points of that length are left, the size of device it will be
      used on, and the number of code points left that encode to that
      size.

   *  It is recommended to have a specification even if the registration
      procedure is "Expert Review".  When specifications are not
      provided for a request where Expert Review is the assignment
      policy, the description provided needs to have sufficient
      information to verify the code points as above.

11.  References

11.1.  Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119,
              DOI 10.17487/RFC2119, March 1997,
              <https://www.rfc-editor.org/info/rfc2119>.

   [RFC3279]  Bassham, L., Polk, W., and R. Housley, "Algorithms and
              Identifiers for the Internet X.509 Public Key
              Infrastructure Certificate and Certificate Revocation List
              (CRL) Profile", RFC 3279, DOI 10.17487/RFC3279, April
              2002, <https://www.rfc-editor.org/info/rfc3279>.

   [RFC3552]  Rescorla, E. and B. Korver, "Guidelines for Writing RFC
              Text on Security Considerations", BCP 72, RFC 3552,
              DOI 10.17487/RFC3552, July 2003,
              <https://www.rfc-editor.org/info/rfc3552>.

   [RFC5116]  McGrew, D., "An Interface and Algorithms for Authenticated
              Encryption", RFC 5116, DOI 10.17487/RFC5116, January 2008,
              <https://www.rfc-editor.org/info/rfc5116>.

   [RFC5869]  Krawczyk, H. and P. Eronen, "HMAC-based Extract-and-Expand
              Key Derivation Function (HKDF)", RFC 5869,
              DOI 10.17487/RFC5869, May 2010,
              <https://www.rfc-editor.org/info/rfc5869>.

   [RFC6090]  McGrew, D., Igoe, K., and M. Salter, "Fundamental Elliptic
              Curve Cryptography Algorithms", RFC 6090,
              DOI 10.17487/RFC6090, February 2011,
              <https://www.rfc-editor.org/info/rfc6090>.

   [RFC6960]  Santesson, S., Myers, M., Ankney, R., Malpani, A.,
              Galperin, S., and C. Adams, "X.509 Internet Public Key
              Infrastructure Online Certificate Status Protocol - OCSP",
              RFC 6960, DOI 10.17487/RFC6960, June 2013,
              <https://www.rfc-editor.org/info/rfc6960>.

   [RFC6979]  Pornin, T., "Deterministic Usage of the Digital Signature
              Algorithm (DSA) and Elliptic Curve Digital Signature
              Algorithm (ECDSA)", RFC 6979, DOI 10.17487/RFC6979, August
              2013, <https://www.rfc-editor.org/info/rfc6979>.

   [RFC7252]  Shelby, Z., Hartke, K., and C. Bormann, "The Constrained
              Application Protocol (CoAP)", RFC 7252,
              DOI 10.17487/RFC7252, June 2014,
              <https://www.rfc-editor.org/info/rfc7252>.

   [RFC7748]  Langley, A., Hamburg, M., and S. Turner, "Elliptic Curves
              for Security", RFC 7748, DOI 10.17487/RFC7748, January
              2016, <https://www.rfc-editor.org/info/rfc7748>.

   [RFC7959]  Bormann, C. and Z. Shelby, Ed., "Block-Wise Transfers in
              the Constrained Application Protocol (CoAP)", RFC 7959,
              DOI 10.17487/RFC7959, August 2016,
              <https://www.rfc-editor.org/info/rfc7959>.

   [RFC8126]  Cotton, M., Leiba, B., and T. Narten, "Guidelines for
              Writing an IANA Considerations Section in RFCs", BCP 26,
              RFC 8126, DOI 10.17487/RFC8126, June 2017,
              <https://www.rfc-editor.org/info/rfc8126>.

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC
              2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174,
              May 2017, <https://www.rfc-editor.org/info/rfc8174>.

   [RFC8392]  Jones, M., Wahlstroem, E., Erdtman, S., and H. Tschofenig,
              "CBOR Web Token (CWT)", RFC 8392, DOI 10.17487/RFC8392,
              May 2018, <https://www.rfc-editor.org/info/rfc8392>.

   [RFC8410]  Josefsson, S. and J. Schaad, "Algorithm Identifiers for
              Ed25519, Ed448, X25519, and X448 for Use in the Internet
              X.509 Public Key Infrastructure", RFC 8410,
              DOI 10.17487/RFC8410, August 2018,
              <https://www.rfc-editor.org/info/rfc8410>.

   [RFC8610]  Birkholz, H., Vigano, C., and C. Bormann, "Concise Data
              Definition Language (CDDL): A Notational Convention to
              Express Concise Binary Object Representation (CBOR) and
              JSON Data Structures", RFC 8610, DOI 10.17487/RFC8610,
              June 2019, <https://www.rfc-editor.org/info/rfc8610>.

   [RFC8613]  Selander, G., Mattsson, J., Palombini, F., and L. Seitz,
              "Object Security for Constrained RESTful Environments
              (OSCORE)", RFC 8613, DOI 10.17487/RFC8613, July 2019,
              <https://www.rfc-editor.org/info/rfc8613>.

   [RFC8724]  Minaburo, A., Toutain, L., Gomez, C., Barthel, D., and JC.
              Zuniga, "SCHC: Generic Framework for Static Context Header
              Compression and Fragmentation", RFC 8724,
              DOI 10.17487/RFC8724, April 2020,
              <https://www.rfc-editor.org/info/rfc8724>.

   [RFC8742]  Bormann, C., "Concise Binary Object Representation (CBOR)
              Sequences", RFC 8742, DOI 10.17487/RFC8742, February 2020,
              <https://www.rfc-editor.org/info/rfc8742>.

   [RFC8747]  Jones, M., Seitz, L., Selander, G., Erdtman, S., and H.
              Tschofenig, "Proof-of-Possession Key Semantics for CBOR
              Web Tokens (CWTs)", RFC 8747, DOI 10.17487/RFC8747, March
              2020, <https://www.rfc-editor.org/info/rfc8747>.

   [RFC8949]  Bormann, C. and P. Hoffman, "Concise Binary Object
              Representation (CBOR)", STD 94, RFC 8949,
              DOI 10.17487/RFC8949, December 2020,
              <https://www.rfc-editor.org/info/rfc8949>.

   [RFC9052]  Schaad, J., "CBOR Object Signing and Encryption (COSE):
              Structures and Process", STD 96, RFC 9052,
              DOI 10.17487/RFC9052, August 2022,
              <https://www.rfc-editor.org/info/rfc9052>.

   [RFC9053]  Schaad, J., "CBOR Object Signing and Encryption (COSE):
              Initial Algorithms", RFC 9053, DOI 10.17487/RFC9053,
              August 2022, <https://www.rfc-editor.org/info/rfc9053>.

   [RFC9175]  Amsüss, C., Preuß Mattsson, J., and G. Selander,
              "Constrained Application Protocol (CoAP): Echo, Request-
              Tag, and Token Processing", RFC 9175,
              DOI 10.17487/RFC9175, February 2022,
              <https://www.rfc-editor.org/info/rfc9175>.

   [RFC9360]  Schaad, J., "CBOR Object Signing and Encryption (COSE):
              Header Parameters for Carrying and Referencing X.509
              Certificates", RFC 9360, DOI 10.17487/RFC9360, February
              2023, <https://www.rfc-editor.org/info/rfc9360>.

11.2.  Informative References

   [Bruni18]  Bruni, A., Sahl Jørgensen, T., Grønbech Petersen, T., and
              C. Schürmann, "Formal Verification of Ephemeral Diffie-
              Hellman Over COSE (EDHOC)", November 2018,
              <https://www.springerprofessional.de/en/formal-
              verification-of-ephemeral-diffie-hellman-over-cose-
              edhoc/16284348>.

   [C509-CERTS]
              Preuß Mattsson, J., Selander, G., Raza, S., Höglund, J.,
              and M. Furuhed, "CBOR Encoded X.509 Certificates (C509
              Certificates)", Work in Progress, Internet-Draft, draft-
              ietf-cose-cbor-encoded-cert-09, 4 March 2024,
              <https://datatracker.ietf.org/doc/html/draft-ietf-cose-
              cbor-encoded-cert-09>.

   [CborMe]   Bormann, C., "CBOR Playground", <https://cbor.me/>.

   [CNSA]     Wikipedia, "Commercial National Security Algorithm Suite",
              October 2023, <https://en.wikipedia.org/w/index.php?title=
              Commercial_National_Security_Algorithm_Suite&oldid=1181333
              611>.

   [CoAP-SEC-PROT]
              Mattsson, J. P., Palombini, F., and M. Vučinić,
              "Comparison of CoAP Security Protocols", Work in Progress,
              Internet-Draft, draft-ietf-iotops-security-protocol-
              comparison-04, 4 March 2024,
              <https://datatracker.ietf.org/doc/html/draft-ietf-iotops-
              security-protocol-comparison-04>.

   [CottierPointcheval22]
              Cottier, B. and D. Pointcheval, "Security Analysis of the
              EDHOC protocol", September 2022,
              <https://arxiv.org/abs/2209.03599>.

   [CURVE-REPR]
              Struik, R., "Alternative Elliptic Curve Representations",
              Work in Progress, Internet-Draft, draft-ietf-lwig-curve-
              representations-23, 21 January 2022,
              <https://datatracker.ietf.org/doc/html/draft-ietf-lwig-
              curve-representations-23>.

   [Degabriele11]
              Degabriele, J., Lehmann, A., Paterson, K., Smart, N., and
              M. Strefler, "On the Joint Security of Encryption and
              Signature in EMV", December 2011,
              <https://eprint.iacr.org/2011/615>.

   [EAT]      Lundblade, L., Mandyam, G., O'Donoghue, J., and C.
              Wallace, "The Entity Attestation Token (EAT)", Work in
              Progress, Internet-Draft, draft-ietf-rats-eat-25, 15
              January 2024, <https://datatracker.ietf.org/doc/html/
              draft-ietf-rats-eat-25>.

   [EDHOC-CoAP-OSCORE]
              Palombini, F., Tiloca, M., Höglund, R., Hristozov, S., and
              G. Selander, "Using Ephemeral Diffie-Hellman Over COSE
              (EDHOC) with the Constrained Application Protocol (CoAP)
              and Object Security for Constrained RESTful Environments
              (OSCORE)", Work in Progress, Internet-Draft, draft-ietf-
              core-oscore-edhoc-10, 29 November 2023,
              <https://datatracker.ietf.org/doc/html/draft-ietf-core-
              oscore-edhoc-10>.

   [GuentherIlunga22]
              Günther, F. and M. Mukendi, "Careful with MAc-then-SIGn: A
              Computational Analysis of the EDHOC Lightweight
              Authenticated Key Exchange Protocol", December 2022,
              <https://eprint.iacr.org/2022/1705>.

   [HEDGED-ECC-SIGS]
              Preuß Mattsson, J., Thormarker, E., and S. Ruohomaa,
              "Hedged ECDSA and EdDSA Signatures", Work in Progress,
              Internet-Draft, draft-irtf-cfrg-det-sigs-with-noise-02, 1
              March 2024, <https://datatracker.ietf.org/doc/html/draft-
              irtf-cfrg-det-sigs-with-noise-02>.

   [HKDFpaper]
              Krawczyk, H., "Cryptographic Extraction and Key
              Derivation: The HKDF Scheme", May 2010,
              <https://eprint.iacr.org/2010/264.pdf>.

   [IEEE.802.15.4-2015]
              IEEE, "IEEE Standard for Low-Rate Wireless Networks",
              DOI 10.1109/IEEESTD.2016.7460875, April 2016,
              <https://ieeexplore.ieee.org/document/7460875>.

   [Jacomme23]
              Jacomme, C., Klein, E., Kremer, S., and M. Racouchot, "A
              comprehensive, formal and automated analysis of the EDHOC
              protocol", October 2022,
              <https://hal.inria.fr/hal-03810102/>.

   [KUDOS]    Höglund, R. and M. Tiloca, "Key Update for OSCORE
              (KUDOS)", Work in Progress, Internet-Draft, draft-ietf-
              core-oscore-key-update-07, 4 March 2024,
              <https://datatracker.ietf.org/doc/html/draft-ietf-core-
              oscore-key-update-07>.

   [LAKE-AUTHZ]
              Selander, G., Mattsson, J. P., Vučinić, M., Fedrecheski,
              G., and M. Richardson, "Lightweight Authorization using
              Ephemeral Diffie-Hellman Over COSE", Work in Progress,
              Internet-Draft, draft-ietf-lake-authz-01, 4 March 2024,
              <https://datatracker.ietf.org/doc/html/draft-ietf-lake-
              authz-01>.

   [LAKE-REQS]
              Vučinić, M., Selander, G., Preuß Mattsson, J., and D.
              Garcia-Carillo, "Requirements for a Lightweight AKE for
              OSCORE", Work in Progress, Internet-Draft, draft-ietf-
              lake-reqs-04, 8 June 2020,
              <https://datatracker.ietf.org/doc/html/draft-ietf-lake-
              reqs-04>.

   [NISTPQC]  National Institute Standards and Technology (NIST), "Post-
              Quantum Cryptography FAQs",
              <https://csrc.nist.gov/Projects/post-quantum-cryptography/
              faqs>.

   [Noise]    Perrin, T., "The Noise Protocol Framework", Revision 34,
              July 2018, <https://noiseprotocol.org/noise.html>.

   [Norrman20]
              Norrman, K., Sundararajan, V., and A. Bruni, "Formal
              Analysis of EDHOC Key Establishment for Constrained IoT
              Devices", September 2020,
              <https://arxiv.org/abs/2007.11427>.

   [RFC2986]  Nystrom, M. and B. Kaliski, "PKCS #10: Certification
              Request Syntax Specification Version 1.7", RFC 2986,
              DOI 10.17487/RFC2986, November 2000,
              <https://www.rfc-editor.org/info/rfc2986>.

   [RFC5280]  Cooper, D., Santesson, S., Farrell, S., Boeyen, S.,
              Housley, R., and W. Polk, "Internet X.509 Public Key
              Infrastructure Certificate and Certificate Revocation List
              (CRL) Profile", RFC 5280, DOI 10.17487/RFC5280, May 2008,
              <https://www.rfc-editor.org/info/rfc5280>.

   [RFC6194]  Polk, T., Chen, L., Turner, S., and P. Hoffman, "Security
              Considerations for the SHA-0 and SHA-1 Message-Digest
              Algorithms", RFC 6194, DOI 10.17487/RFC6194, March 2011,
              <https://www.rfc-editor.org/info/rfc6194>.

   [RFC7228]  Bormann, C., Ersue, M., and A. Keranen, "Terminology for
              Constrained-Node Networks", RFC 7228,
              DOI 10.17487/RFC7228, May 2014,
              <https://www.rfc-editor.org/info/rfc7228>.

   [RFC7258]  Farrell, S. and H. Tschofenig, "Pervasive Monitoring Is an
              Attack", BCP 188, RFC 7258, DOI 10.17487/RFC7258, May
              2014, <https://www.rfc-editor.org/info/rfc7258>.

   [RFC7296]  Kaufman, C., Hoffman, P., Nir, Y., Eronen, P., and T.
              Kivinen, "Internet Key Exchange Protocol Version 2
              (IKEv2)", STD 79, RFC 7296, DOI 10.17487/RFC7296, October
              2014, <https://www.rfc-editor.org/info/rfc7296>.

   [RFC7624]  Barnes, R., Schneier, B., Jennings, C., Hardie, T.,
              Trammell, B., Huitema, C., and D. Borkmann,
              "Confidentiality in the Face of Pervasive Surveillance: A
              Threat Model and Problem Statement", RFC 7624,
              DOI 10.17487/RFC7624, August 2015,
              <https://www.rfc-editor.org/info/rfc7624>.

   [RFC8366]  Watsen, K., Richardson, M., Pritikin, M., and T. Eckert,
              "A Voucher Artifact for Bootstrapping Protocols",
              RFC 8366, DOI 10.17487/RFC8366, May 2018,
              <https://www.rfc-editor.org/info/rfc8366>.

   [RFC8376]  Farrell, S., Ed., "Low-Power Wide Area Network (LPWAN)
              Overview", RFC 8376, DOI 10.17487/RFC8376, May 2018,
              <https://www.rfc-editor.org/info/rfc8376>.

   [RFC8446]  Rescorla, E., "The Transport Layer Security (TLS) Protocol
              Version 1.3", RFC 8446, DOI 10.17487/RFC8446, August 2018,
              <https://www.rfc-editor.org/info/rfc8446>.

   [RFC8937]  Cremers, C., Garratt, L., Smyshlyaev, S., Sullivan, N.,
              and C. Wood, "Randomness Improvements for Security
              Protocols", RFC 8937, DOI 10.17487/RFC8937, October 2020,
              <https://www.rfc-editor.org/info/rfc8937>.

   [RFC9000]  Iyengar, J., Ed. and M. Thomson, Ed., "QUIC: A UDP-Based
              Multiplexed and Secure Transport", RFC 9000,
              DOI 10.17487/RFC9000, May 2021,
              <https://www.rfc-editor.org/info/rfc9000>.

   [RFC9147]  Rescorla, E., Tschofenig, H., and N. Modadugu, "The
              Datagram Transport Layer Security (DTLS) Protocol Version
              1.3", RFC 9147, DOI 10.17487/RFC9147, April 2022,
              <https://www.rfc-editor.org/info/rfc9147>.

   [RFC9176]  Amsüss, C., Ed., Shelby, Z., Koster, M., Bormann, C., and
              P. van der Stok, "Constrained RESTful Environments (CoRE)
              Resource Directory", RFC 9176, DOI 10.17487/RFC9176, April
              2022, <https://www.rfc-editor.org/info/rfc9176>.

   [RFC9397]  Pei, M., Tschofenig, H., Thaler, D., and D. Wheeler,
              "Trusted Execution Environment Provisioning (TEEP)
              Architecture", RFC 9397, DOI 10.17487/RFC9397, July 2023,
              <https://www.rfc-editor.org/info/rfc9397>.

   [RFC9529]  Selander, G., Preuß Mattsson, J., Serafin, M., Tiloca, M.,
              and M. Vučinić, "Traces of Ephemeral Diffie-Hellman Over
              COSE (EDHOC)", RFC 9529, DOI 10.17487/RFC9529, March 2024,
              <https://www.rfc-editor.org/info/rfc9529>.

   [SECG]     Certicom Research, "SEC 1: Elliptic Curve Cryptography",
              Standards for Efficient Cryptography, May 2009,
              <https://www.secg.org/sec1-v2.pdf>.

   [SIGMA]    Krawczyk, H., "SIGMA: the 'SIGn-and-MAc' Approach to
              Authenticated Diffie-Hellman and Its Use in the IKE-
              Protocols", June 2003,
              <https://www.iacr.org/cryptodb/archive/2003/
              CRYPTO/1495/1495.pdf>.

   [SP-800-108]
              Chen, L., "Recommendation for Key Derivation Using
              Pseudorandom Functions", NIST Special Publication 800-108
              Revision 1, DOI 10.6028/NIST.SP.800-108r1-upd1, August
              2022, <https://doi.org/10.6028/NIST.SP.800-108r1-upd1>.

   [SP-800-56A]
              Barker, E., Chen, L., Roginsky, A., Vassilev, A., and R.
              Davis, "Recommendation for Pair-Wise Key-Establishment
              Schemes Using Discrete Logarithm Cryptography",
              NIST Special Publication 800-56A Revision 3,
              DOI 10.6028/NIST.SP.800-56Ar3, April 2018,
              <https://doi.org/10.6028/NIST.SP.800-56Ar3>.

   [SP800-185]
              Kelsey, J., Chang, S., and R. Perlner, "SHA-3 Derived
              Functions cSHAKE, KMAC, TupleHash and ParallelHash",
              NIST Special Publication 800-185,
              DOI 10.6028/NIST.SP.800-185, December 2016,
              <https://doi.org/10.6028/NIST.SP.800-185>.

   [Thormarker21]
              Thormarker, E., "On using the same key pair for Ed25519
              and an X25519 based KEM", April 2021,
              <https://eprint.iacr.org/2021/509.pdf>.

   [THREAT-MODEL-GUIDANCE]
              Arkko, J. and S. Farrell, "Internet Threat Model
              Guidance", Work in Progress, Internet-Draft, draft-arkko-
              arch-internet-threat-model-guidance-00, 12 July 2021,
              <https://datatracker.ietf.org/doc/html/draft-arkko-arch-
              internet-threat-model-guidance-00>.

Appendix A.  Use with OSCORE and Transfer over CoAP

   This appendix describes how to derive an OSCORE security context when
   EDHOC is used to key OSCORE and how to transfer EDHOC messages over
   CoAP.  The use of CoAP or OSCORE with EDHOC is optional, but if you
   are using CoAP or OSCORE, then certain normative requirements apply
   as detailed in the subsections.

A.1.  Deriving the OSCORE Security Context

   This section specifies how to use EDHOC output to derive the OSCORE
   security context.

   After successful processing of EDHOC message_3, the Client and Server
   derive Security Context parameters for OSCORE as follows (see
   Section 3.2 of [RFC8613]):

   *  The Master Secret and Master Salt SHALL be derived by using the
      EDHOC_Exporter interface (see Section 4.2.1):

      -  The EDHOC Exporter Labels for deriving the OSCORE Master Secret
         and OSCORE Master Salt are the uints 0 and 1, respectively.

      -  The context parameter is h'' (0x40), the empty CBOR byte
         string.

      -  By default, oscore_key_length is the key length (in bytes) of
         the application AEAD Algorithm of the selected cipher suite for
         the EDHOC session.  Also by default, oscore_salt_length has
         value 8.  The Initiator and Responder MAY agree out-of-band on
         a longer oscore_key_length than the default and on shorter or
         longer than the default oscore_salt_length.

      Master Secret = EDHOC_Exporter( 0, h'', oscore_key_length )
      Master Salt   = EDHOC_Exporter( 1, h'', oscore_salt_length )

   *  The AEAD Algorithm SHALL be the application AEAD algorithm of the
      selected cipher suite for the EDHOC session.

   *  The HKDF Algorithm SHALL be the one based on the application hash
      algorithm of the selected cipher suite for the EDHOC session.  For
      example, if SHA-256 is the application hash algorithm of the
      selected cipher suite, HKDF SHA-256 is used as the HKDF Algorithm
      in the OSCORE Security Context.

   *  The relationship between identifiers in OSCORE and EDHOC is
      specified in Section 3.3.3.  The OSCORE Sender ID and Recipient ID
      SHALL be determined by EDHOC connection identifiers C_R and C_I
      for the EDHOC session as shown in Table 14.

       +=================+==================+=====================+
       |                 | OSCORE Sender ID | OSCORE Recipient ID |
       +=================+==================+=====================+
       | EDHOC Initiator |       C_R        |         C_I         |
       +-----------------+------------------+---------------------+
       | EDHOC Responder |       C_I        |         C_R         |
       +-----------------+------------------+---------------------+

           Table 14: Usage of Connection Identifiers in OSCORE

   The Client and Server SHALL use the parameters above to establish an
   OSCORE Security Context, as per Section 3.2.1 of [RFC8613].

   From then on, the Client and Server retrieve the OSCORE protocol
   state using the Recipient ID and optionally other transport
   information such as the 5-tuple.

A.2.  Transferring EDHOC over CoAP

   This section specifies how EDHOC can be transferred as an exchange of
   CoAP [RFC7252] messages.  CoAP provides a reliable transport that can
   preserve packet ordering, provides flow and congestion control, and
   handles message duplication.  CoAP can also perform fragmentation and
   mitigate certain denial-of-service attacks.  The underlying CoAP
   transport should be used in reliable mode, in particular, when
   fragmentation is used, to avoid, e.g., situations with hanging
   endpoints waiting for each other.

   EDHOC may run with the Initiator either being a CoAP client or CoAP
   server.  We denote the former by the "forward message flow" (see
   Appendix A.2.1) and the latter by the "reverse message flow" (see
   Appendix A.2.2).  By default, we assume the forward message flow, but
   the roles SHOULD be chosen to protect the most sensitive identity;
   see Section 9.

   According to this specification, EDHOC is transferred in POST
   requests to the Uri-Path: "/.well-known/edhoc" (see Section 10.7) and
   2.04 (Changed) responses.  An application may define its own path
   that can be discovered, e.g., using a resource directory [RFC9176].
   Client applications can use the resource type "core.edhoc" to
   discover a server's EDHOC resource, i.e., where to send a request for
   executing the EDHOC protocol; see Section 10.10.  An alternative
   transfer of the forward message flow is specified in
   [EDHOC-CoAP-OSCORE].

   In order for the server to correlate a message received from a client
   to a message previously sent in the same EDHOC session over CoAP,
   messages sent by the client SHALL be prepended with the CBOR
   serialization of the connection identifier that the server has
   selected; see Section 3.4.1.  This applies both to the forward and
   the reverse message flows.  To indicate a new EDHOC session in the
   forward message flow, message_1 SHALL be prepended with the CBOR
   simple value true (0xf5).  Even if CoAP is carried over a reliable
   transport protocol, such as TCP, the prepending of identifiers
   specified here SHALL be practiced to enable interoperability
   independent of how CoAP is transported.

   The prepended identifiers are encoded in CBOR and thus self-
   delimiting.  The representation of identifiers described in
   Section 3.3.2 SHALL be used.  They are sent in front of the actual
   EDHOC message to keep track of messages in an EDHOC session, and only
   the part of the body following the identifier is used for EDHOC
   processing.  In particular, the connection identifiers within the
   EDHOC messages are not impacted by the prepended identifiers.

   An EDHOC message has media type "application/edhoc+cbor-seq", whereas
   an EDHOC message prepended by a connection identifier has media type
   "application/cid-edhoc+cbor-seq"; see Section 10.9.

   To mitigate certain denial-of-service attacks, the CoAP server MAY
   respond to the first POST request with a 4.01 (Unauthorized)
   containing an Echo option [RFC9175].  This forces the Initiator to
   demonstrate reachability at its apparent network address.  If message
   fragmentation is needed, the EDHOC messages may be fragmented using
   the CoAP Block-Wise Transfer mechanism [RFC7959].

   EDHOC error messages need to be transported in response to a message
   that failed (see Section 6).  EDHOC error messages transported with
   CoAP are carried in the payload.

   Note that the transport over CoAP can serve as a blueprint for other
   client-server protocols:

   *  The client prepends the connection identifier selected by the
      server (or, for message_1, the CBOR simple value true) to any
      request message it sends.

   *  The server does not send any such indicator, as responses are
      matched to request by the client-server protocol design.

A.2.1.  The Forward Message Flow

   In the forward message flow, the CoAP client is the Initiator and the
   CoAP server is the Responder.  This flow protects the client identity
   against active attackers and the server identity against passive
   attackers.

   In the forward message flow, the CoAP Token enables correlation on
   the Initiator (client) side, and the prepended C_R enables
   correlation on the Responder (server) side.

   *  EDHOC message_1 is sent in the payload of a POST request from the
      client to the server's resource for EDHOC, prepended with the
      identifier true (0xf5), indicating a new EDHOC session.

   *  EDHOC message_2 or the EDHOC error message is sent from the server
      to the client in the payload of the response, in the former case
      with response code 2.04 (Changed) and in the latter with response
      code as specified in Appendix A.2.3.

   *  EDHOC message_3 or the EDHOC error message is sent from the client
      to the server's resource in the payload of a POST request,
      prepended with connection identifier C_R.

   *  If EDHOC message_4 is used, or in case of an error message, it is
      sent from the server to the client in the payload of the response,
      with response codes analogously to message_2.  In case of an error
      message sent in response to message_4, it is sent analogously to
      the error message sent in response to message_2.

   An example of a completed EDHOC session over CoAP in the forward
   message flow is shown in Figure 10.

       Client    Server
         |          |
         +--------->| Header: POST (Code=0.02)
         |   POST   | Uri-Path: "/.well-known/edhoc"
         |          | Content-Format: application/cid-edhoc+cbor-seq
         |          | Payload: true, EDHOC message_1
         |          |
         |<---------+ Header: 2.04 Changed
         |   2.04   | Content-Format: application/edhoc+cbor-seq
         |          | Payload: EDHOC message_2
         |          |
         +--------->| Header: POST (Code=0.02)
         |   POST   | Uri-Path: "/.well-known/edhoc"
         |          | Content-Format: application/cid-edhoc+cbor-seq
         |          | Payload: C_R, EDHOC message_3
         |          |
         |<---------+ Header: 2.04 Changed
         |   2.04   | Content-Format: application/edhoc+cbor-seq
         |          | Payload: EDHOC message_4
         |          |

               Figure 10: Example of the Forward Message Flow

   The forward message flow of EDHOC can be combined with an OSCORE
   exchange in a total of two round trips; see [EDHOC-CoAP-OSCORE].

A.2.2.  The Reverse Message Flow

   In the reverse message flow, the CoAP client is the Responder and the
   CoAP server is the Initiator.  This flow protects the server identity
   against active attackers and the client identity against passive
   attackers.

   In the reverse message flow, the CoAP Token enables correlation on
   the Responder (client) side, and the prepended C_I enables
   correlation on the Initiator (server) side.

   *  To trigger a new EDHOC session, the client makes an empty POST
      request to the server's resource for EDHOC.

   *  EDHOC message_1 is sent from the server to the client in the
      payload of the response with response code 2.04 (Changed).

   *  EDHOC message_2 or the EDHOC error message is sent from the client
      to the server's resource in the payload of a POST request,
      prepended with connection identifier C_I.

   *  EDHOC message_3 or the EDHOC error message is sent from the server
      to the client in the payload of the response, in the former case
      with response code 2.04 (Changed) and in the latter with response
      code as specified in Appendix A.2.3.

   *  If EDHOC message_4 is used, or in case of an error message, it is
      sent from the client to the server's resource in the payload of a
      POST request, prepended with connection identifier C_I.  In case
      of an error message sent in response to message_4, it is sent
      analogously to an error message sent in response to message_2.

   An example of a completed EDHOC session over CoAP in the reverse
   message flow is shown in Figure 11.

       Client    Server
         |          |
         +--------->| Header: POST (Code=0.02)
         |   POST   | Uri-Path: "/.well-known/edhoc"
         |          |
         |<---------+ Header: 2.04 Changed
         |   2.04   | Content-Format: application/edhoc+cbor-seq
         |          | Payload: EDHOC message_1
         |          |
         +--------->| Header: POST (Code=0.02)
         |   POST   | Uri-Path: "/.well-known/edhoc"
         |          | Content-Format: application/cid-edhoc+cbor-seq
         |          | Payload: C_I, EDHOC message_2
         |          |
         |<---------+ Header: 2.04 Changed
         |   2.04   | Content-Format: application/edhoc+cbor-seq
         |          | Payload: EDHOC message_3
         |          |

               Figure 11: Example of the Reverse Message Flow

A.2.3.  Errors in EDHOC over CoAP

   When using EDHOC over CoAP, EDHOC error messages sent as CoAP
   responses MUST be sent in the payload of error responses, i.e., they
   MUST specify a CoAP error response code.  In particular, it is
   RECOMMENDED that such error responses have response code either 4.00
   (Bad Request) in case of client error (e.g., due to a malformed EDHOC
   message) or 5.00 (Internal Server Error) in case of server error
   (e.g., due to failure in deriving EDHOC keying material).  The
   Content-Format of the error response MUST be set to "application/
   edhoc+cbor-seq"; see Section 10.9.

Appendix B.  Compact Representation

   This section defines a format for compact representation based on the
   Elliptic-Curve-Point-to-Octet-String Conversion defined in
   Section 2.3.3 of [SECG].

   As described in Section 4.2 of [RFC6090], the x-coordinate of an
   elliptic curve public key is a suitable representative for the entire
   point whenever scalar multiplication is used as a one-way function.
   One example is ECDH with compact output, where only the x-coordinate
   of the computed value is used as the shared secret.

   In EDHOC, compact representation is used for the ephemeral public
   keys (G_X and G_Y); see Section 3.7.  Using the notation from [SECG],
   the output is an octet string of length ceil( (log2 q) / 8 ), where
   ceil(x) is the smallest integer not less than x.  See [SECG] for a
   definition of q, M, X, xp, and ~yp.  The steps in Section 2.3.3 of
   [SECG] are replaced with the following steps:

   1.  Convert the field element xp to an octet string X of length ceil(
       (log2 q) / 8 ) octets using the conversion routine specified in
       Section 2.3.5 of [SECG].

   2.  Output M = X.

   The encoding of the point at infinity is not supported.

   Compact representation does not change any requirements on
   validation; see Section 9.2.  Using compact representation has some
   security benefits.  An implementation does not need to check that the
   point is not the point at infinity (the identity element).
   Similarly, as not even the sign of the y-coordinate is encoded,
   compact representation trivially avoids so-called "benign
   malleability" attacks where an attacker changes the sign; see [SECG].

   The following may be needed for validation or compatibility with APIs
   that do not support compact representation or do not support the full
   [SECG] format:

   *  If a compressed y-coordinate is required, then the value ~yp set
      to zero can be used.  In such a case, the compact representation
      described above can be transformed into the Standards for
      Efficient Cryptography Group (SECG) point-compressed format by
      prepending it with the single byte 0x02 (i.e., M = 0x02 || X).

   *  If an uncompressed y-coordinate is required, then a y-coordinate
      has to be calculated following Section 2.3.4 of [SECG] or
      Appendix C of [RFC6090].  Any of the square roots (see [SECG] or
      [RFC6090]) can be used.  The uncompressed SECG format is M =
      0x04 || X || Y.

   For example: The curve P-256 has the parameters (using the notation
   in [RFC6090]):

   *  p = 2^256 - 2^224 + 2^192 + 2^96 - 1

   *  a = -3

   *  b = 410583637251521421293261297800472684091144410159937255
      54835256314039467401291

   Given an example x:

   *  x = 115792089183396302095546807154740558443406795108653336
      398970697772788799766525

   We can calculate y as the square root w = (x^3 + a ⋅ x + b)^((p +
   1)/4) (mod p).

   *  y = 834387180070192806820075864918626005281451259964015754
      16632522940595860276856

   Note that this does not guarantee that (x, y) is on the correct
   elliptic curve.  A full validation according to Section 5.6.2.3.3 of
   [SP-800-56A] is done by also checking that 0 ≤ x < p and that y^2 ≡
   x^3 + a ⋅ x + b (mod p).

Appendix C.  Use of CBOR, CDDL, and COSE in EDHOC

   This appendix is intended to help implementors not familiar with CBOR
   [RFC8949], CDDL [RFC8610], COSE [RFC9052], and HKDF [RFC5869].

C.1.  CBOR and CDDL

   The Concise Binary Object Representation (CBOR) [RFC8949] is a data
   format designed for small code size and small message size.  CBOR
   builds on the JSON data model but extends it by, e.g., encoding
   binary data directly without base64 conversion.  In addition to the
   binary CBOR encoding, CBOR also has a diagnostic notation that is
   readable and editable by humans.  The Concise Data Definition
   Language (CDDL) [RFC8610] provides a way to express structures for
   protocol messages and APIs that use CBOR.  [RFC8610] also extends the
   diagnostic notation.

   CBOR data items are encoded to or decoded from byte strings using a
   type-length-value encoding scheme, where the three highest order bits
   of the initial byte contain information about the major type.  CBOR
   supports several types of data items, integers (int, uint), simple
   values, byte strings (bstr), and text strings (tstr).  CBOR also
   supports arrays [] of data items, maps {} of pairs of data items, and
   sequences [RFC8742] of data items.  Some examples are given below.

   The EDHOC specification sometimes use CDDL names in CBOR diagnostic
   notation as in, e.g., << ID_CRED_R, ? EAD_2 >>.  This means that
   EAD_2 is optional and that ID_CRED_R and EAD_2 should be substituted
   with their values before evaluation.  That is, if ID_CRED_R = { 4 :
   h'' } and EAD_2 is omitted, then << ID_CRED_R, ? EAD_2 >> = << { 4 :
   h'' } >>, which encodes to 0x43a10440.  We also make use of the
   occurrence symbol "*", like in, e.g., 2* int, meaning two or more
   CBOR integers.

   For a complete specification and more examples, see [RFC8949] and
   [RFC8610].  We recommend implementors get used to CBOR by using the
   CBOR playground [CborMe].

          +==================+==============+==================+
          | Diagnostic       | Encoded      | Type             |
          +==================+==============+==================+
          | 1                | 0x01         | unsigned integer |
          +------------------+--------------+------------------+
          | 24               | 0x1818       | unsigned integer |
          +------------------+--------------+------------------+
          | -24              | 0x37         | negative integer |
          +------------------+--------------+------------------+
          | -25              | 0x3818       | negative integer |
          +------------------+--------------+------------------+
          | true             | 0xf5         | simple value     |
          +------------------+--------------+------------------+
          | h''              | 0x40         | byte string      |
          +------------------+--------------+------------------+
          | h'12cd'          | 0x4212cd     | byte string      |
          +------------------+--------------+------------------+
          | '12cd'           | 0x4431326364 | byte string      |
          +------------------+--------------+------------------+
          | "12cd"           | 0x6431326364 | text string      |
          +------------------+--------------+------------------+
          | { 4 : h'cd' }    | 0xa10441cd   | map              |
          +------------------+--------------+------------------+
          | << 1, 2, true >> | 0x430102f5   | byte string      |
          +------------------+--------------+------------------+
          | [ 1, 2, true ]   | 0x830102f5   | array            |
          +------------------+--------------+------------------+
          | ( 1, 2, true )   | 0x0102f5     | sequence         |
          +------------------+--------------+------------------+
          | 1, 2, true       | 0x0102f5     | sequence         |
          +------------------+--------------+------------------+

                Table 15: Examples of Use of CBOR and CDDL

C.2.  CDDL Definitions

   This section compiles the CDDL definitions for ease of reference.

   suites = [ 2* int ] / int

   ead = (
     ead_label : int,
     ? ead_value : bstr,
   )

   EAD_1 = 1* ead
   EAD_2 = 1* ead
   EAD_3 = 1* ead
   EAD_4 = 1* ead

   message_1 = (
     METHOD : int,
     SUITES_I : suites,
     G_X : bstr,
     C_I : bstr / -24..23,
     ? EAD_1,
   )

   message_2 = (
     G_Y_CIPHERTEXT_2 : bstr,
   )

   PLAINTEXT_2 = (
     C_R,
     ID_CRED_R : map / bstr / -24..23,
     Signature_or_MAC_2 : bstr,
     ? EAD_2,
   )

   message_3 = (
     CIPHERTEXT_3 : bstr,
   )

   PLAINTEXT_3 = (
     ID_CRED_I : map / bstr / -24..23,
     Signature_or_MAC_3 : bstr,
     ? EAD_3,
   )

   message_4 = (
     CIPHERTEXT_4 : bstr,
   )

   PLAINTEXT_4 = (
     ? EAD_4,
   )

   error = (
     ERR_CODE : int,
     ERR_INFO : any,
   )

   info = (
     info_label : int,
     context : bstr,
     length : uint,
   )

C.3.  COSE

   CBOR Object Signing and Encryption (COSE) [RFC9052] describes how to
   create and process signatures, MACs, and encryptions using CBOR.
   COSE builds on JSON Object Signing and Encryption (JOSE) but is
   adapted to allow more efficient processing in constrained devices.
   EDHOC makes use of COSE_Key, COSE_Encrypt0, and COSE_Sign1 objects in
   the message processing:

   *  ECDH ephemeral public keys of type EC2 or OKP in message_1 and
      message_2 consist of the COSE_Key parameter named 'x'; see
      Sections 7.1 and 7.2 of [RFC9053].

   *  The ciphertexts in message_3 and message_4 consist of a subset of
      the single recipient encrypted data object COSE_Encrypt0, which is
      described in Sections 5.2 and 5.3 of [RFC9052].  The ciphertext is
      computed over the plaintext and associated data, using an
      encryption key and an initialization vector.  The associated data
      is an Enc_structure consisting of protected headers and externally
      supplied data (external_aad).  COSE constructs the input to the
      AEAD [RFC5116] for message_i (i = 3 or 4; see Sections 5.4 and
      5.5, respectively) as follows:

      -  Secret key K = K_i

      -  Nonce N = IV_i

      -  Plaintext P for message_i

      -  Associated Data A = [ "Encrypt0", h'', TH_i ]

   *  Signatures in message_2 of method 0 and 2, and in message_3 of
      method 0 and 1, consist of a subset of the single signer data
      object COSE_Sign1, which is described in Sections 4.2 and 4.4 of
      [RFC9052].  The signature is computed over a Sig_structure
      containing payload, protected headers and externally supplied data
      (external_aad) using a private signature key, and verified using
      the corresponding public signature key.  For COSE_Sign1, the
      message to be signed is:

       [ "Signature1", protected, external_aad, payload ]

      where protected, external_aad, and payload are specified in
      Sections 5.3 and 5.4.

   Different header parameters to identify X.509 or C509 certificates by
   reference are defined in [RFC9360] and [C509-CERTS]:

   *  by a hash value with the 'x5t' or 'c5t' parameters, respectively:

      -  ID_CRED_x = { 34 : COSE_CertHash }, for x = I or R and

      -  ID_CRED_x = { 22 : COSE_CertHash }, for x = I or R,

   *  or by a URI with the 'x5u' or 'c5u' parameters, respectively:

      -  ID_CRED_x = { 35 : uri }, for x = I or R, and

      -  ID_CRED_x = { 23 : uri }, for x = I or R.

   When ID_CRED_x does not contain the actual credential, it may be very
   short, e.g., if the endpoints have agreed to use a key identifier
   parameter 'kid':

   *  ID_CRED_x = { 4 : kid_x }, where kid_x : kid, for x = I or R.  For
      further optimization, see Section 3.5.3.

   Note that ID_CRED_x can contain several header parameters, for
   example, { x5u, x5t } or { kid, kid_context }.

   ID_CRED_x MAY also identify the credential by value.  For example, a
   certificate chain can be transported in an ID_CRED field with COSE
   header parameter c5c or x5chain, as defined in [C509-CERTS] and
   [RFC9360].  Credentials of type CWT and CCS can be transported with
   the COSE header parameters registered in Section 10.6.

Appendix D.  Authentication-Related Verifications

   EDHOC performs certain authentication-related operations (see
   Section 3.5), but in general, it is necessary to make additional
   verifications beyond EDHOC message processing.  Which verifications
   that are needed depend on the deployment, in particular, the trust
   model and the security policies, but most commonly, it can be
   expressed in terms of verifications of credential content.

   EDHOC assumes the existence of mechanisms (certification authority or
   other trusted third party, pre-provisioning, etc.) for generating and
   distributing authentication credentials and other credentials, as
   well as the existence of trust anchors (CA certificates, trusted
   public keys, etc.).  For example, a public key certificate or CWT may
   rely on a trusted third party whose public key is pre-provisioned,
   whereas a CCS or a self-signed certificate / CWT may be used when
   trust in the public key can be achieved by other means, or in the
   case of trust on first use, see Appendix D.5.

   In this section, we provide some examples of such verifications.
   These verifications are the responsibility of the application but may
   be implemented as part of an EDHOC library.

D.1.  Validating the Authentication Credential

   In addition to the authentication key, the authentication credential
   may contain other parameters that need to be verified.  For example:

   *  In X.509 and C509 certificates, signature keys typically have key
      usage "digitalSignature", and Diffie-Hellman public keys typically
      have key usage "keyAgreement" [RFC3279] [RFC8410].

   *  In X.509 and C509 certificates, validity is expressed using Not
      After and Not Before.  In CWT and CCS, the "exp" and "nbf" claims
      have similar meanings.

D.2.  Identities

   The application must decide on allowing a connection or not,
   depending on the intended endpoint, and in particular whether it is a
   specific identity or in a set of identities.  To prevent misbinding
   attacks, the identity of the endpoint is included in a MAC verified
   through the protocol.  More details and examples are provided in this
   section.

   Policies for what connections to allow are typically set based on the
   identity of the other endpoint, and endpoints typically only allow
   connections from a specific identity or a small restricted set of
   identities.  For example, in the case of a device connecting to a
   network, the network may only allow connections from devices that
   authenticate with certificates having a particular range of serial
   numbers and signed by a particular CA.  Conversely, a device may only
   be allowed to connect to a network that authenticates with a
   particular public key.

   *  When a Public Key Infrastructure (PKI) is used with certificates,
      the identity is the subject whose unique name, e.g., a domain
      name, a Network Access Identifier (NAI), or an Extended Unique
      Identifier (EUI), is included in the endpoint's certificate.

   *  Similarly, when a PKI is used with CWTs, the identity is the
      subject identified by the relevant claim(s), such as 'sub'
      (subject).

   *  When PKI is not used (e.g., CCS, self-signed certificate / CWT),
      the identity is typically directly associated with the
      authentication key of the other party.  For example, if identities
      can be expressed in the form of unique subject names assigned to
      public keys, then a binding to identity is achieved by including
      both the public key and associated subject name in the
      authentication credential.  CRED_I or CRED_R may be a self-signed
      certificate / CWT or CCS containing the authentication key and the
      subject name; see Section 3.5.2.  Thus, each endpoint needs to
      know the specific authentication key / unique associated subject
      name or set of public authentication keys / unique associated
      subject names, which it is allowed to communicate with.

   To prevent misbinding attacks in systems where an attacker can
   register public keys without proving knowledge of the private key,
   SIGMA [SIGMA] enforces a MAC to be calculated over the "identity".
   EDHOC follows SIGMA by calculating a MAC over the whole
   authentication credential, which in case of an X.509 or C509
   certificate, includes the "subject" and "subjectAltName" fields and,
   in the case of CWT or CCS, includes the "sub" claim.

   (While the SIGMA paper only focuses on the identity, the same
   principle is true for other information such as policies associated
   with the public key.)

D.3.  Certification Path and Trust Anchors

   When a Public Key Infrastructure (PKI) is used with certificates, the
   trust anchor is a certification authority (CA) certificate.  Each
   party needs at least one CA public key certificate or just the CA
   public key.  The certification path contains proof that the subject
   of the certificate owns the public key in the certificate.  Only
   validated public key certificates are to be accepted.

   Similarly, when a PKI is used with CWTs, each party needs to have at
   least one trusted third-party public key as a trust anchor to verify
   the end entity CWTs.  The trusted third-party public key can, e.g.,
   be stored in a self-signed CWT or in a CCS.

   The signature of the authentication credential needs to be verified
   with the public key of the issuer.  X.509 and C509 certificates
   includes the "Issuer" field.  In CWT and CCS, the "iss" claim has a
   similar meaning.  The public key is either a trust anchor or the
   public key in another valid and trusted credential in a certification
   path from the trust anchor to the authentication credential.

   Similar verifications as made with the authentication credential (see
   Appendix D.1) are also needed for the other credentials in the
   certification path.

   When PKI is not used (CCS and self-signed certificate / CWT), the
   trust anchor is the authentication key of the other party; in which
   case, there is no certification path.

D.4.  Revocation Status

   The application may need to verify that the credentials are not
   revoked; see Section 9.8.  Some use cases may be served by short-
   lived credentials, for example, where the validity of the credential
   is on par with the interval between revocation checks.  But, in
   general, credential lifetime and revocation checking are
   complementary measures to control credential status.  Revocation
   information may be transported as External Authorization Data (EAD);
   see Appendix E.

D.5.  Unauthenticated Operation

   EDHOC might be used without authentication by allowing the Initiator
   or Responder to communicate with any identity except its own.  Note
   that EDHOC without mutual authentication is vulnerable to active on-
   path attacks and therefore unsafe for general use.  However, it is
   possible to later establish a trust relationship with an unknown or
   not-yet-trusted endpoint.  Some examples are listed below:

   *  The EDHOC authentication credential can be verified out-of-band at
      a later stage.

   *  The EDHOC session key can be bound to an identity out-of-band at a
      later stage.

   *  Trust on first use (TOFU) can be used to verify that several EDHOC
      connections are made to the same identity.  TOFU combined with
      proximity is a common IoT deployment model that provides good
      security if done correctly.  Note that secure proximity based on
      short range wireless technology requires very low signal strength
      or very low latency.

Appendix E.  Use of External Authorization Data

   In order to reduce the number of messages and round trips, or to
   simplify processing, external security applications may be integrated
   into EDHOC by transporting related external authorization data (EAD)
   in the messages.

   The EAD format is specified in Section 3.8.  This section contains
   examples and further details of how EAD may be used with an
   appropriate accompanying specification.

   *  One example is third-party-assisted authorization, requested with
      EAD_1, and an authorization artifact ("voucher", cf. [RFC8366])
      returned in EAD_2; see [LAKE-AUTHZ].

   *  Another example is remote attestation, requested in EAD_2, and an
      Entity Attestation Token (EAT) [EAT] returned in EAD_3.

   *  A third example is certificate enrollment, where a Certificate
      Signing Request (CSR) [RFC2986] is included in EAD_3, and the
      issued public key certificate (X.509 [RFC5280] and C509
      [C509-CERTS]) or a reference thereof is returned in EAD_4.

   External authorization data should be considered unprotected by
   EDHOC, and the protection of EAD is the responsibility of the
   security application (third-party authorization, remote attestation,
   certificate enrollment, etc.).  The security properties of the EAD
   fields (after EDHOC processing) are discussed in Section 9.1.

   The content of the EAD field may be used in the EDHOC processing of
   the message in which they are contained.  For example,
   authentication-related information, like assertions and revocation
   information, transported in EAD fields may provide input about trust
   anchors or validity of credentials relevant to the authentication
   processing.  The EAD fields (like ID_CRED fields) are therefore made
   available to the application before the message is verified; see
   details of message processing in Section 5.  In the first example
   above, a voucher in EAD_2 made available to the application can
   enable the Initiator to verify the identity or the public key of the
   Responder before verifying the signature.  An application allowing
   EAD fields containing authentication information thus may need to
   handle authentication-related verifications associated with EAD
   processing.

   Conversely, the security application may need to wait for EDHOC
   message verification to complete.  In the third example above, the
   validation of a CSR carried in EAD_3 is not started by the Responder
   before EDHOC has successfully verified message_3 and proven the
   possession of the private key of the Initiator.

   The security application may reuse EDHOC protocol fields that
   therefore need to be available to the application.  For example, the
   security application may use the same crypto algorithms as in the
   EDHOC session and therefore needs access to the selected cipher suite
   (or the whole SUITES_I).  The application may use the ephemeral
   public keys G_X and G_Y as ephemeral keys or as nonces; see
   [LAKE-AUTHZ].

   The processing of the EAD item (ead_label, ? ead_value) by the
   security application needs to be described in the specification where
   the ead_label is registered (see Section 10.5), including the
   optional ead_value for each message and actions in case of errors.
   An application may support multiple security applications that make
   use of EAD, which may result in multiple EAD items in one EAD field;
   see Section 3.8.  Any dependencies on security applications with
   previously registered EAD items need to be documented, and the
   processing needs to consider their simultaneous use.

   Since data carried in EAD may not be protected, or processed by the
   application before the EDHOC message is verified, special
   considerations need to be made such that it does not violate security
   and privacy requirements of the service that uses this data; see
   Section 9.5.  The content in an EAD item may impact the security
   properties provided by EDHOC.  Security applications making use of
   the EAD items must perform the necessary security analysis.

Appendix F.  Application Profile Example

   This appendix contains a rudimentary example of an application
   profile; see Section 3.9.

   For use of EDHOC with application X, the following assumptions are
   made:

   1.  Transfer in CoAP as specified in Appendix A.2 with requests
       expected by the CoAP server (= Responder) at /app1-edh, no
       Content-Format needed.

   2.  METHOD = 1 (I uses signature key; R uses static DH key.)

   3.  CRED_I is an IEEE 802.1AR Initial Device Identifier (IDevID)
       encoded as a C509 certificate of type 0 [C509-CERTS].

       *  R acquires CRED_I out-of-band, indicated in EAD_1.

       *  ID_CRED_I = {4: h''} is a 'kid' with the value of the empty
          CBOR byte string.

   4.  CRED_R is a CCS of type OKP as specified in Section 3.5.2.

       *  The CBOR map has parameters 1 (kty), -1 (crv), and -2
          (x-coordinate).

       *  ID_CRED_R is {14 : CCS}.

   5.  External authorization data is defined and processed as specified
       in [LAKE-AUTHZ].

   6.  EUI-64 is used as the identity of the endpoint (see an example in
       Section 3.5.2).

   7.  No use of message_4.  The application sends protected messages
       from R to I.

Appendix G.  Long PLAINTEXT_2

   By the definition of encryption of PLAINTEXT_2 with KEYSTREAM_2, it
   is limited to lengths of PLAINTEXT_2 not exceeding the output of
   EDHOC_KDF; see Section 4.1.2.  If the EDHOC hash algorithm is SHA-2,
   then HKDF-Expand is used, which limits the length of the EDHOC_KDF
   output to 255 ⋅ hash_length, where hash_length is the length of the
   output of the EDHOC hash algorithm given by the cipher suite.  For
   example, with SHA-256 as the EDHOC hash algorithm, the length of the
   hash output is 32 bytes and the maximum length of PLAINTEXT_2 is 255
   ⋅ 32 = 8160 bytes.

   While PLAINTEXT_2 is expected to be much shorter than 8 kB for the
   intended use cases, it seems nevertheless prudent to specify a
   solution for the event that this should turn out to be a limitation.

   A potential work-around is to use a cipher suite with a different
   hash function.  In particular, the use of KMAC removes all practical
   limitations in this respect.

   This section specifies a solution that works with any hash function
   by making use of multiple invocations of HKDF-Expand and negative
   values of info_label.

   Consider the PLAINTEXT_2 partitioned in parts P(i) of length equal to
   M = 255 ⋅ hash_length, except possibly the last part P(last), which
   has 0 < length ≤ M.

   PLAINTEXT_2 = P(0) | P(1) | ... | P(last)

   where "|" indicates concatenation.

   The object is to define a matching KEYSTREAM_2 of the same length and
   perform the encryption in the same way as defined in Section 5.3.2:

   CIPHERTEXT_2 = PLAINTEXT_2 XOR KEYSTREAM_2

   Define the keystream as:

   KEYSTREAM_2 = OKM(0) | OKM(1)  | ... | OKM(last)

   where:

   OKM(i) = EDHOC_KDF( PRK_2e, -i, TH_2, length(P(i)) )

   Note that if length(PLAINTEXT_2) ≤ M, then P(0) = PLAINTEXT_2 and the
   definition of KEYSTREAM_2 = OKM(0) coincides with Figure 6.

   This describes the processing of the Responder when sending
   message_2.  The Initiator makes the same calculations when receiving
   message_2 but interchanging PLAINTEXT_2 and CIPHERTEXT_2.

   An application profile may specify if it supports or does not support
   the method described in this appendix.

Appendix H.  EDHOC_KeyUpdate

   To provide forward secrecy in an even more efficient way than re-
   running EDHOC, this section specifies the optional function
   EDHOC_KeyUpdate in terms of EDHOC_KDF and PRK_out.

   When EDHOC_KeyUpdate is called, a new PRK_out is calculated as the
   output of the EDHOC_Expand function with the old PRK_out as input.
   The change of PRK_out causes a change to PRK_exporter, which enables
   the derivation of new application keys superseding the old ones,
   using EDHOC_Exporter; see Section 4.2.1.  The process is illustrated
   by the following pseudocode.

   EDHOC_KeyUpdate( context ):
      new PRK_out = EDHOC_KDF( old PRK_out, 11, context, hash_length )
      new PRK_exporter = EDHOC_KDF( new PRK_out, 10, h'', hash_length )

   where hash_length denotes the output size in bytes of the EDHOC hash
   algorithm of the selected cipher suite.

   The EDHOC_KeyUpdate takes a context as input to enable binding of the
   updated PRK_out to some event that triggered the key update.  The
   Initiator and Responder need to agree on the context, which can,
   e.g., be a counter, a pseudorandom number, or a hash.  To provide
   forward secrecy, the old PRK_out and keys derived from it (old
   PRK_exporter and old application keys) must be deleted as soon as
   they are not needed.  When to delete the old keys and how to verify
   that they are not needed is up to the application.  Note that the
   security properties depend on the type of context and the number of
   KeyUpdate iterations.

   An application using EDHOC_KeyUpdate needs to store PRK_out.
   Compromise of PRK_out leads to compromise of all keying material
   derived with the EDHOC_Exporter since the last invocation of the
   EDHOC_KeyUpdate function.

   While this key update method provides forward secrecy, it does not
   give as strong security properties as re-running EDHOC.
   EDHOC_KeyUpdate can be used to meet cryptographic limits and provide
   partial protection against key leakage, but it provides significantly
   weaker security properties than re-running EDHOC with ephemeral
   Diffie-Hellman.  Even with frequent use of EDHOC_KeyUpdate,
   compromise of one session key compromises all future session keys,
   and an attacker therefore only needs to perform static key
   exfiltration [RFC7624], which is less complicated and has a lower
   risk profile than the dynamic case; see Section 9.1.

   A similar method to do a key update for OSCORE is KUDOS; see [KUDOS].

Appendix I.  Example Protocol State Machine

   This appendix describes an example protocol state machine for the
   Initiator and Responder.  States are denoted in all capitals, and
   parentheses denote actions taken only in some circumstances.

   Note that this state machine is just an example, and that details of
   processing are omitted.  For example:

   *  when error messages are being sent (with one exception);

   *  how credentials and EAD are processed by EDHOC and the application
      in the RCVD state; and

   *  what verifications are made, which includes not only MACs and
      signatures.

I.1.  Initiator State Machine

   The Initiator sends message_1, triggering the state machine to
   transition from START to WAIT_M2, and waits for message_2.

   If the incoming message is an error message, then the Initiator
   transitions from WAIT_M2 to ABORTED.  In case of error code 2 (Wrong
   Selected Cipher Suite), the Initiator remembers the supported cipher
   suites for this particular Responder and transitions from ABORTED to
   START.  The message_1 that the Initiator subsequently sends takes
   into account the cipher suites supported by the Responder.

   Upon receiving a non-error message, the Initiator transitions from
   WAIT_M2 to RCVD_M2 and processes the message.  If a processing error
   occurs on message_2, then the Initiator transitions from RCVD_M2 to
   ABORTED.  In case of successful processing of message_2, the
   Initiator transitions from RCVD_M2 to VRFD_M2.

   The Initiator prepares and processes message_3 for sending.  If any
   processing error is encountered, the Initiator transitions from
   VRFD_M2 to ABORTED.  If message_3 is successfully sent, the Initiator
   transitions from VRFD_M2 to COMPLETED.

   If the application profile includes message_4, then the Initiator
   waits for message_4.  If the incoming message is an error message,
   then the Initiator transitions from COMPLETED to ABORTED.  Upon
   receiving a non-error message, the Initiator transitions from
   COMPLETED (="WAIT_M4") to RCVD_M4 and processes the message.  If a
   processing error occurs on message_4, then the Initiator transitions
   from RCVD_M4 to ABORTED.  In case of successful processing of
   message_4, the Initiator transitions from RCVD_M4 to PERSISTED
   (="VRFD_M4").

   If the application profile does not include message_4, then the
   Initiator waits for an incoming application message.  If the
   decryption and verification of the application message is successful,
   then the Initiator transitions from COMPLETED to PERSISTED.

        +- - - - - - - - - -> START
        |                       |
                                | Send message_1
        |                       |
              Receive error     v
    ABORTED <---------------- WAIT_M2
        ^                       |
        |                       | Receive message_2
        |                       |
        |    Processing error   v
        +-------------------- RCVD_M2
        ^                       |
        |                       | Verify message_2
        |                       |
        |    Processing error   v
        +-------------------- VRFD_M2
        ^                       |
        |                       | Send message_3
        |                       |
        |    (Receive error)    v
        +-------------------- COMPLETED ----------------+
        ^                       |                       |
        |                       | (Receive message_4)   |
        |                       |                       |
        |   (Processing error)  v                       | (Verify
        +------------------- (RCVD_M4)                  |  application
                                |                       |  message)
                                | (Verify message_4)    |
                                |                       |
                                v                       |
                              PERSISTED <---------------+

                     Figure 12: Initiator State Machine

I.2.  Responder State Machine

   Upon receiving message_1, the Responder transitions from START to
   RCVD_M1.

   If a processing error occurs on message_1, the Responder transitions
   from RCVD_M1 to ABORTED.  This includes sending an error message with
   error code 2 (Wrong Selected Cipher Suite) if the selected cipher
   suite in message_1 is not supported.  In case of successful
   processing of message_1, the Responder transitions from RCVD_M1 to
   VRFD_M1.

   The Responder prepares and processes message_2 for sending.  If any
   processing error is encountered, the Responder transitions from
   VRFD_M1 to ABORTED.  If message_2 is successfully sent, the Initiator
   transitions from VRFD_M2 to WAIT_M3 and waits for message_3.

   If the incoming message is an error message, then the Responder
   transitions from WAIT_M3 to ABORTED.

   Upon receiving message_3, the Responder transitions from WAIT_M3 to
   RCVD_M3.  If a processing error occurs on message_3, the Responder
   transitions from RCVD_M3 to ABORTED.  In case of successful
   processing of message_3, the Responder transitions from RCVD_M3 to
   COMPLETED (="VRFD_M3").

   If the application profile includes message_4, the Responder prepares
   and processes message_4 for sending.  If any processing error is
   encountered, the Responder transitions from COMPLETED to ABORTED.

   If message_4 is successfully sent, or if the application profile does
   not include message_4, the Responder transitions from COMPLETED to
   PERSISTED.

                                        START
                                          |
                                          | Receive message_1
                                          |
                       Processing error   v
              ABORTED <---------------- RCVD_M1
                  ^                       |
                  |                       | Verify message_1
                  |                       |
                  |    Processing error   v
                  +-------------------- VRFD_M1
                  ^                       |
                  |                       | Send message_2
                  |                       |
                  |     Receive error     v
                  +-------------------- WAIT_M3
                  ^                       |
                  |                       | Receive message_3
                  |                       |
                  |    Processing error   v
                  +-------------------- RCVD_M3
                  ^                       |
                  |                       | Verify message_3
                  |                       |
                  |   (Processing error)  v
                  +------------------- COMPLETED
                                          |
                                          | (Send message_4)
                                          |
                                          v
                                       PERSISTED

                     Figure 13: Responder State Machine

Acknowledgments

   The authors want to thank Christian Amsüss, Karthikeyan Bhargavan,
   Carsten Bormann, Alessandro Bruni, Timothy Claeys, Baptiste Cottier,
   Roman Danyliw, Martin Disch, Martin Duke, Donald Eastlake 3rd, Lars
   Eggert, Stephen Farrell, Loïc Ferreira, Theis Grønbech Petersen,
   Felix Günther, Dan Harkins, Klaus Hartke, Russ Housley, Stefan
   Hristozov, Marc Ilunga, Charlie Jacomme, Elise Klein, Erik Kline,
   Steve Kremer, Alexandros Krontiris, Ilari Liusvaara, Rafa Marín-
   López, Kathleen Moriarty, David Navarro, Karl Norrman, Salvador
   Pérez, Radia Perlman, David Pointcheval, Maïwenn Racouchot, Eric
   Rescorla, Michael Richardson, Thorvald Sahl Jørgensen, Zaheduzzaman
   Sarker, Jim Schaad, Michael Scharf, Carsten Schürmann, John Scudder,
   Ludwig Seitz, Brian Sipos, Stanislav Smyshlyaev, Valery Smyslov,
   Peter van der Stok, Rene Struik, Vaishnavi Sundararajan, Erik
   Thormarker, Marco Tiloca, Sean Turner, Michel Veillette, Mališa
   Vučinić, Paul Wouters, and Lei Yan for reviewing and commenting on
   intermediate draft versions of this document.

   We are especially indebted to the late Jim Schaad for his continuous
   review and implementation of draft versions of this document, as well
   as his work on other technologies such as COSE and OSCORE without
   which EDHOC would not have been.

   Work on this document has in part been supported by the H2020 project
   SIFIS-Home (grant agreement 952652).

Authors' Addresses

   Göran Selander
   Ericsson AB
   SE-164 80 Stockholm
   Sweden
   Email: goran.selander@ericsson.com


   John Preuß Mattsson
   Ericsson AB
   SE-164 80 Stockholm
   Sweden
   Email: john.mattsson@ericsson.com


   Francesca Palombini
   Ericsson AB
   SE-164 80 Stockholm
   Sweden
   Email: francesca.palombini@ericsson.com
```

---

### `rfc-llm`

*sha256:`54ff40ef4c3c` · 15 lines · 0.5 KB (~123 tokens) · lang:`bash`*

```bash
#!/usr/bin/env bash
# RFC-LLM Command-line Runner
# Automatically configures PYTHONPATH and invokes the project virtual environment.

set -e

REPO_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PYTHONPATH="${REPO_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

if [ ! -f "${REPO_ROOT}/.venv/bin/python" ]; then
    echo "Error: Virtual environment not found at ${REPO_ROOT}/.venv" >&2
    exit 1
fi

exec "${REPO_ROOT}/.venv/bin/python" "${REPO_ROOT}/src/pipeline.py" "$@"
```

---

### `rfc-think`

*sha256:`8396df53b458` · 15 lines · 0.5 KB (~130 tokens) · lang:`bash`*

```bash
#!/usr/bin/env bash
# RFC-LLM Phase 3 (<think> Token Synthesizer) Runner
# Automatically configures PYTHONPATH and invokes src/generate_think/cli.py.

set -e

REPO_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PYTHONPATH="${REPO_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"

if [ ! -f "${REPO_ROOT}/.venv/bin/python" ]; then
    echo "Error: Virtual environment not found at ${REPO_ROOT}/.venv" >&2
    exit 1
fi

exec "${REPO_ROOT}/.venv/bin/python" "${REPO_ROOT}/src/generate_think/cli.py" "$@"
```

---

### `src/__init__.py`

*sha256:`5304a7d0e9d5` · 3 lines · 0.1 KB (~30 tokens) · lang:`python`*

```python
"""RFC-LLM: End-to-End Synthesis of Formally Verified MITRE CPSA Scheme Models from IETF RFCs."""

__version__ = "0.1.0"
```

---

### `src/code_generation/__init__.py`

*sha256:`466c2e70bf95` · 17 lines · 0.5 KB (~116 tokens) · lang:`python`*

```python
"""Code Generation package for Stage 3 CPSA JSON serialization and Scheme S-expression emission."""

from src.code_generation.cpsa_json_serializer import (
    serialize_to_cpsa_json,
    serialize_to_cpsa_json_string,
)
from src.code_generation.cpsa_scheme_emitter import (
    CPSAJsonCompilationError,
    emit_cpsa_scheme,
)

__all__ = [
    "serialize_to_cpsa_json",
    "serialize_to_cpsa_json_string",
    "CPSAJsonCompilationError",
    "emit_cpsa_scheme",
]
```

---

### `src/code_generation/cpsa_json_serializer.py`

*sha256:`6a87f1a09db8` · 24 lines · 1.0 KB (~263 tokens) · lang:`python`*

```python
"""CPSA JSON AST Serializer."""

import json
from typing import Any, List

from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("json_serializer")


def serialize_to_cpsa_json(spec: CPSAProtocolSpecification) -> List[List[Any]]:
    """Serializes a CPSAProtocolSpecification into a list of top-level CPSA JSON forms."""
    logger.debug("Serializing CPSAProtocolSpecification for '%s' to native JSON forms", spec.protocol_name)
    payload = spec.to_cpsa_json_payload()
    logger.debug("Serialized %d top-level S-expression forms", len(payload))
    return payload


def serialize_to_cpsa_json_string(spec: CPSAProtocolSpecification) -> str:
    """Serializes the protocol specification into a newline-delimited JSON string for cpsa4json."""
    forms = serialize_to_cpsa_json(spec)
    # Each top-level form is written on its own line / separated by double newlines
    return "\n\n".join(json.dumps(form) for form in forms) + "\n"
```

---

### `src/code_generation/cpsa_scheme_emitter.py`

*sha256:`295e0a2becb0` · 70 lines · 2.8 KB (~709 tokens) · lang:`python`*

```python
"""CPSA Scheme S-Expression Emitter using cpsa4json."""

import re
import subprocess
from pathlib import Path
from typing import Optional

from src.code_generation.cpsa_json_serializer import serialize_to_cpsa_json_string
from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("scheme_emitter")


class CPSAJsonCompilationError(Exception):
    """Raised when cpsa4json fails to compile a JSON tree into Scheme S-expressions."""
    pass


def sanitize_protocol_stem(raw_name: str) -> str:
    """Sanitizes a protocol name or filename prefix into a filesystem-safe `.scm` stem."""
    sanitized = re.sub(r"[^a-z0-9_-]+", "_", (raw_name or "").lower()).strip("_")
    return sanitized or "protocol"


def emit_cpsa_scheme(
    spec: CPSAProtocolSpecification,
    output_directory: Path,
    filename_prefix: Optional[str] = None,
) -> Path:
    """Compiles a CPSAProtocolSpecification into a verified MITRE Scheme (.scm) file via cpsa4json."""
    output_directory.mkdir(parents=True, exist_ok=True)
    stem = sanitize_protocol_stem(filename_prefix or spec.protocol_name)
    target_scm_path = output_directory / f"{stem}.scm"

    logger.info("Emitting CPSA Scheme S-expressions for '%s' to %s", spec.protocol_name, target_scm_path)

    json_input_str = serialize_to_cpsa_json_string(spec)

    if not SYSTEM_CONFIG.CPSA4JSON_BIN.exists():
        logger.error("cpsa4json binary not found at %s", SYSTEM_CONFIG.CPSA4JSON_BIN)
        raise FileNotFoundError(f"cpsa4json binary missing at {SYSTEM_CONFIG.CPSA4JSON_BIN}")

    try:
        proc = subprocess.run(
            [str(SYSTEM_CONFIG.CPSA4JSON_BIN)],
            input=json_input_str,
            capture_output=True,
            text=True,
            timeout=SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS,
            check=False,
        )

        if proc.returncode != 0 or "Bad char in atom" in proc.stdout or "Error" in proc.stderr:
            err_msg = proc.stderr.strip() or proc.stdout.strip() or f"Exited with code {proc.returncode}"
            logger.error("cpsa4json compilation failed: %s", err_msg)
            raise CPSAJsonCompilationError(f"cpsa4json compilation error: {err_msg}")

        scm_content = proc.stdout

        with open(target_scm_path, "w", encoding="utf-8") as f:
            f.write(scm_content)

        logger.info("Successfully emitted %d lines of Scheme code to %s", len(scm_content.splitlines()), target_scm_path)
        return target_scm_path

    except subprocess.TimeoutExpired as e:
        logger.error("cpsa4json subprocess timed out after %d seconds", SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS)
        raise CPSAJsonCompilationError(f"cpsa4json compilation timed out: {e}") from e
```

---

### `src/cost_tracker.py`

*sha256:`7e821742be5b` · 309 lines · 12.6 KB (~3,224 tokens) · lang:`python`*

```python
"""Real-Time Token & USD Cost Telemetry Tracker across Pipeline Model Roles.

Tracks per-call, per-RFC, and cumulative batch token usage and USD cost across the
four pipeline model roles:
  1. `router`     — Stage 1b Applicability Gate & Stage 1c Section Router
  2. `extraction` — Stage 2 Constrained Protocol Extraction & Schema Self-Correction
  3. `query`      — Stage 5/6 Agentic CPSA Knowledge Base Searcher
  4. `repair`     — Stage 5/6 Compiler & Solver Diagnostic Self-Healing Repair
"""

from __future__ import annotations

import copy
import json
import threading
import urllib.request
from typing import Any, Dict, Literal, Optional, Tuple

import litellm

from src.logging_config import get_pipeline_logger
from src.pipeline_events import GLOBAL_EVENT_BUS
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("cost_tracker")

ModelRoleLiteral = Literal["router", "extraction", "query", "repair"]
MODEL_ROLES: Tuple[str, ...] = ("router", "extraction", "query", "repair")

# Built-in fallback per-token USD rates (prompt, completion, cache_read) per 1 token
# Derived from live Nous Research / OpenAI / Anthropic / Google / DeepSeek pricing.
_FALLBACK_PRICING_PER_TOKEN: Dict[str, Tuple[float, float, float]] = {
    "openai/gpt-6.1-terra": (1.00e-6, 5.00e-6, 0.05e-6),
    "openai/gpt-6.1-terra-pro": (1.00e-6, 5.00e-6, 0.05e-6),
    "openai/gpt-6.1-sol": (2.00e-6, 10.00e-6, 0.10e-6),
    "openai/gpt-6-luna": (0.10e-6, 0.50e-6, 0.01e-6),
    "openai/gpt-6-luna-pro": (0.10e-6, 0.50e-6, 0.01e-6),
    "anthropic/claude-haiku-5.5": (0.10e-6, 0.50e-6, 0.01e-6),
    "anthropic/claude-sonnet-5.5": (2.00e-6, 10.00e-6, 0.10e-6),
    "anthropic/claude-sonnet-4.6": (3.00e-6, 15.00e-6, 0.30e-6),
    "google/gemini-3.7-flash": (0.75e-6, 3.75e-6, 0.075e-6),
    "google/gemini-3.8-flash": (0.825e-6, 4.125e-6, 0.0825e-6),
    "google/gemini-3.1-flash-lite-preview": (0.25e-6, 1.50e-6, 0.025e-6),
    "google/gemini-3.1-pro-preview": (2.00e-6, 12.00e-6, 0.20e-6),
    "google/gemini-2.5-flash": (0.15e-6, 0.60e-6, 0.0375e-6),
    "google/gemini-2.5-flash-lite": (0.10e-6, 0.40e-6, 0.025e-6),
    "z-ai/glm-5.3": (0.91e-6, 2.86e-6, 0.169e-6),
    "z-ai/glm-5.3-flash": (0.12e-6, 0.40e-6, 0.024e-6),
    "z-ai/glm-5.2": (0.90e-6, 2.83e-6, 0.16e-6),
    "deepseek/deepseek-v4-pro": (0.94e-6, 1.89e-6, 0.08e-6),
    "deepseek/deepseek-v4.1-flash": (0.106e-6, 0.513e-6, 0.004e-6),
    "deepseek/deepseek-v4-flash": (0.091e-6, 0.182e-6, 0.0182e-6),
    "deepseek/deepseek-v4-flash-0731": (0.054e-6, 0.162e-6, 0.0135e-6),
    "deepseek/deepseek-chat": (0.27e-6, 1.10e-6, 0.07e-6),
    "qwen/qwen3.8-flash": (0.15e-6, 0.47e-6, 0.016e-6),
    "qwen/qwen3.6-flash": (0.1875e-6, 1.125e-6, 0.02e-6),
}


def _empty_role_bucket(model_name: str = "") -> Dict[str, Any]:
    return {
        "model": model_name,
        "calls": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "cached_tokens": 0,
        "total_tokens": 0,
        "cost_usd": 0.0,
    }


def make_empty_cost_summary() -> Dict[str, Any]:
    """Creates a clean per-RFC or batch cost telemetry dictionary."""
    return {
        "total_calls": 0,
        "total_prompt_tokens": 0,
        "total_completion_tokens": 0,
        "total_cached_tokens": 0,
        "total_tokens": 0,
        "total_cost_usd": 0.0,
        "roles": {role: _empty_role_bucket() for role in MODEL_ROLES},
    }


def _normalize_model_key(model_name: str) -> str:
    """Normalizes `nous/openai/gpt-6.1-terra` or `openai/gpt-6.1-terra` to `openai/gpt-6.1-terra`."""
    cleaned = (model_name or "").strip()
    for prefix in ("nous/", "nousresearch/"):
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
    if cleaned.startswith("openai/") and cleaned.count("/") >= 2:
        cleaned = cleaned.split("/", 1)[1]
    return cleaned


def _safe_int(val: Any) -> int:
    """Extracts an integer token count, returning 0 for None or unit-test MagicMocks."""
    if isinstance(val, bool):
        return 0
    if isinstance(val, int):
        return max(0, val)
    if isinstance(val, float):
        return max(0, int(val))
    return 0


class PipelineCostTracker:
    """Thread-safe tracker for per-RFC and cumulative batch token usage and USD costs."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._live_pricing: Dict[str, Tuple[float, float, float]] = dict(_FALLBACK_PRICING_PER_TOKEN)
        self._catalog_fetched = False
        self.current_rfc_id: Optional[str] = None
        self.current_rfc: Dict[str, Any] = make_empty_cost_summary()
        self.batch_total: Dict[str, Any] = make_empty_cost_summary()
        self.rfc_history: Dict[str, Dict[str, Any]] = {}

    def _ensure_live_pricing_loaded(self) -> None:
        if self._catalog_fetched:
            return
        self._catalog_fetched = True
        if not SYSTEM_CONFIG.NOUS_API_KEY:
            return
        try:
            req = urllib.request.Request(
                f"{SYSTEM_CONFIG.NOUS_API_BASE.rstrip('/')}/models",
                headers={
                    "Authorization": f"Bearer {SYSTEM_CONFIG.NOUS_API_KEY}",
                    "User-Agent": "RFC-LLM-CostTracker/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                payload = json.loads(resp.read().decode("utf-8", errors="ignore"))
                for item in payload.get("data", []):
                    mid = item.get("id")
                    pricing = item.get("pricing")
                    if mid and isinstance(pricing, dict):
                        p_rate = float(pricing.get("prompt") or 0.0)
                        c_rate = float(pricing.get("completion") or 0.0)
                        cache_rate = float(pricing.get("input_cache_read") or p_rate)
                        self._live_pricing[mid] = (p_rate, c_rate, cache_rate)
        except Exception as exc:
            logger.debug("Using fallback pricing table (live catalog fetch skipped: %s)", exc)

    def get_model_rates(self, model_name: str) -> Tuple[float, float, float]:
        """Returns `(prompt_rate, completion_rate, cache_read_rate)` in USD per single token."""
        if model_name.startswith(("ollama/", "strata/")):
            return (0.0, 0.0, 0.0)
        self._ensure_live_pricing_loaded()
        norm = _normalize_model_key(model_name)
        if norm in self._live_pricing:
            return self._live_pricing[norm]
        # Try suffix match (e.g. `gemini-2.5-flash` -> `google/gemini-2.5-flash`)
        short = norm.split("/")[-1]
        for k, rates in self._live_pricing.items():
            if k.endswith(f"/{short}") or k == short:
                return rates
        return (0.0, 0.0, 0.0)

    def start_rfc(
        self,
        rfc_id: str,
        router_model: str = "",
        extraction_model: str = "",
        query_model: str = "",
        repair_model: str = "",
    ) -> None:
        """Resets the active per-RFC cost bucket when starting a new RFC run."""
        with self._lock:
            self.current_rfc_id = rfc_id
            self.current_rfc = make_empty_cost_summary()
            role_models = {
                "router": router_model,
                "extraction": extraction_model,
                "query": query_model,
                "repair": repair_model,
            }
            for role, mod in role_models.items():
                if mod:
                    self.current_rfc["roles"][role]["model"] = mod
                    if not self.batch_total["roles"][role]["model"]:
                        self.batch_total["roles"][role]["model"] = mod
            self.rfc_history[rfc_id] = copy.deepcopy(self.current_rfc)

    def record_llm_call(
        self,
        response: Any,
        role: ModelRoleLiteral,
        model_name: str,
        stage: int = 0,
    ) -> Dict[str, Any]:
        """Extracts token usage and USD cost from a LiteLLM response, updates both the
        per-RFC and batch totals, and emits a `cost_updated` visualizer event.
        """
        usage = getattr(response, "usage", None)
        if usage is None and isinstance(response, dict):
            usage = response.get("usage")

        prompt_tok = 0
        comp_tok = 0
        cached_tok = 0

        if usage is not None:
            prompt_tok = _safe_int(
                getattr(usage, "prompt_tokens", None)
                if not isinstance(usage, dict)
                else usage.get("prompt_tokens")
            )
            comp_tok = _safe_int(
                getattr(usage, "completion_tokens", None)
                if not isinstance(usage, dict)
                else usage.get("completion_tokens")
            )
            details = (
                getattr(usage, "prompt_tokens_details", None)
                if not isinstance(usage, dict)
                else usage.get("prompt_tokens_details")
            )
            if details is not None:
                cached_tok = _safe_int(
                    getattr(details, "cached_tokens", None)
                    if not isinstance(details, dict)
                    else details.get("cached_tokens")
                )

        # Estimate cost from live/fallback rates first
        p_rate, c_rate, cache_rate = self.get_model_rates(model_name)
        uncached_prompt = max(0, prompt_tok - cached_tok)
        call_cost = (uncached_prompt * p_rate) + (cached_tok * cache_rate) + (comp_tok * c_rate)

        # If rates were 0 (unknown external model), check LiteLLM response_cost
        if call_cost == 0.0 and (prompt_tok > 0 or comp_tok > 0) and not model_name.startswith(("ollama/", "strata/")):
            try:
                hidden = getattr(response, "_hidden_params", None) or {}
                if isinstance(hidden, dict) and isinstance(hidden.get("response_cost"), (int, float)):
                    call_cost = float(hidden["response_cost"])
                else:
                    litellm_cost = litellm.completion_cost(completion_response=response)
                    if isinstance(litellm_cost, (int, float)):
                        call_cost = float(litellm_cost)
            except Exception:
                pass

        total_tok = prompt_tok + comp_tok
        role_key = role if role in MODEL_ROLES else "repair"

        with self._lock:
            for target in (self.current_rfc, self.batch_total):
                target["total_calls"] += 1
                target["total_prompt_tokens"] += prompt_tok
                target["total_completion_tokens"] += comp_tok
                target["total_cached_tokens"] += cached_tok
                target["total_tokens"] += total_tok
                target["total_cost_usd"] = round(target["total_cost_usd"] + call_cost, 8)

                rb = target["roles"][role_key]
                if model_name:
                    rb["model"] = model_name
                rb["calls"] += 1
                rb["prompt_tokens"] += prompt_tok
                rb["completion_tokens"] += comp_tok
                rb["cached_tokens"] += cached_tok
                rb["total_tokens"] += total_tok
                rb["cost_usd"] = round(rb["cost_usd"] + call_cost, 8)

            rfc_snap = copy.deepcopy(self.current_rfc)
            batch_snap = copy.deepcopy(self.batch_total)
            if self.current_rfc_id:
                self.rfc_history[self.current_rfc_id] = rfc_snap

        GLOBAL_EVENT_BUS.emit(
            "cost_updated",
            stage=stage,
            role=role_key,
            model=model_name,
            call_tokens=total_tok,
            call_cost_usd=round(call_cost, 8),
            rfc_cost=rfc_snap,
            batch_cost=batch_snap,
        )
        return rfc_snap

    def get_current_rfc_summary(self) -> Dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self.current_rfc)

    def get_batch_summary(self) -> Dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self.batch_total)

    @staticmethod
    def format_cli_summary(summary: Dict[str, Any], prefix: str = "Run Cost") -> str:
        """Formats a single-line human-readable summary of total and per-role costs."""
        roles = summary.get("roles", {})
        total_usd = float(summary.get("total_cost_usd", 0.0))
        total_tok = int(summary.get("total_tokens", 0))
        r_usd = float(roles.get("router", {}).get("cost_usd", 0.0))
        e_usd = float(roles.get("extraction", {}).get("cost_usd", 0.0))
        q_usd = float(roles.get("query", {}).get("cost_usd", 0.0))
        rep_usd = float(roles.get("repair", {}).get("cost_usd", 0.0))
        return (
            f"{prefix}: ${total_usd:.4f} ({total_tok:,} tok) | "
            f"Router: ${r_usd:.4f} | Extraction: ${e_usd:.4f} | "
            f"Query/Searcher: ${q_usd:.4f} | Repair: ${rep_usd:.4f}"
        )


GLOBAL_COST_TRACKER = PipelineCostTracker()
```

---

### `src/document_ingestion/__init__.py`

*sha256:`9332eee6bcf3` · 31 lines · 0.9 KB (~235 tokens) · lang:`python`*

```python
"""Document Ingestion package for Stage 1 RFC filtering, TOC parsing, section routing, and slicing."""

from src.document_ingestion.handshake_section_router import (
    SectionRoutingDecision,
    route_handshake_sections,
)
from src.document_ingestion.protocol_applicability_gate import (
    ProtocolApplicabilityReport,
    evaluate_protocol_applicability,
)
from src.document_ingestion.rfc_header_filter import (
    HeaderFilterResult,
    filter_rfc_header,
)
from src.document_ingestion.rfc_toc_parser import (
    TOCSectionEntry,
    parse_table_of_contents,
)
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections

__all__ = [
    "HeaderFilterResult",
    "filter_rfc_header",
    "TOCSectionEntry",
    "parse_table_of_contents",
    "ProtocolApplicabilityReport",
    "evaluate_protocol_applicability",
    "SectionRoutingDecision",
    "route_handshake_sections",
    "slice_verbatim_sections",
]
```

---

### `src/document_ingestion/handshake_section_router.py`

*sha256:`9d6c18dd3001` · 217 lines · 7.9 KB (~2,031 tokens) · lang:`python`*

```python
"""Handshake Section Router for Navigating RFC Table of Contents.

Selects the exact RFC section numbers from the Table of Contents that contain
the cryptographic message exchange or handshake flow.
"""

import json
import re
from typing import List, Optional, Set
import json_repair
import litellm
from pydantic import BaseModel, Field

from src.document_ingestion.rfc_toc_parser import TOCSectionEntry
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_SECTION_ROUTER,
    build_schema_system_prompt,
    load_prompt_spec,
    parse_llm_json,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("section_router")


class SectionRoutingDecision(BaseModel):
    """Decision indicating which RFC sections contain the cryptographic message exchange."""

    selected_section_ids: List[str] = Field(
        ...,
        description=(
            "List of bare numerical and dotted section IDs from the Table of Contents "
            "containing the protocol message traces (e.g., ['3', '4'] or ['7.1.1', '7.2.2', 'App-A']). "
            "Use ONLY digits and dots (or 'App-X' for appendices)—NEVER include '#', 'Section', or section titles."
        ),
    )
    rationale: str = Field(..., description="Explanation of why these sections were selected")


def normalize_section_id_token(raw_id: str) -> str:
    """Normalizes a section ID string into a bare numerical/dotted token (e.g. '#7.1.1.' -> '7.1.1')."""
    if not raw_id:
        return ""
    s = str(raw_id).strip().strip("`'\"")
    # Strip leading '#' or '§' or 'Section' / 'Sec.'
    s = re.sub(r"^[#§]+\s*", "", s)
    s = re.sub(r"^(?:Section|Sec\.?)\s+", "", s, flags=re.IGNORECASE)
    # Normalize 'Appendix A' -> 'App-A'
    s = re.sub(r"^Appendix\s+([A-Za-z0-9]+(?:\.[0-9]+)*)", r"App-\1", s, flags=re.IGNORECASE)
    # If the model included a title after the section number (e.g. "7.1.1 Handshake"), keep only the leading ID token
    token_match = re.match(r"^((?:App-[A-Za-z0-9]+(?:\.[0-9]+)*)|(?:[A-Za-z]\.[0-9]+(?:\.[0-9]+)*)|(?:\d+(?:\.\d+)*))", s, flags=re.IGNORECASE)
    if token_match:
        s = token_match.group(1)
    return s.rstrip(".")


def _match_valid_toc_id(raw_id: str, valid_toc_ids: Set[str]) -> Optional[str]:
    """Matches a raw LLM section ID against `valid_toc_ids` after normalization."""
    if raw_id in valid_toc_ids:
        return raw_id
    norm = normalize_section_id_token(raw_id)
    if not norm:
        return None
    if norm in valid_toc_ids:
        return norm
    norm_lower = norm.lower()
    for valid_id in valid_toc_ids:
        if valid_id.lower() == norm_lower or valid_id.rstrip(".").lower() == norm_lower:
            return valid_id
    return None


def route_handshake_sections(
    rfc_id: str,
    protocol_name: str,
    toc_entries: List[TOCSectionEntry],
    model: Optional[str] = None,
) -> List[str]:
    """Uses a structured LLM call to select the exchange section IDs from the TOC."""
    if not toc_entries:
        logger.info("No numbered TOC entries found for %s; routing to full body fallback.", rfc_id)
        return ["FULL_BODY"]

    prompt_spec = load_prompt_spec(PROMPT_SECTION_ROUTER)
    model_name = model or prompt_spec.model
    sampling_temp = prompt_spec.temperature
    logger.info("Routing exchange sections for %s ('%s') using %s", rfc_id, protocol_name, model_name)

    toc_formatted = "\n".join(f"{entry.section_id} {entry.title}" for entry in toc_entries)

    user_prompt = (
        f"Protocol Name: {protocol_name}\n"
        f"RFC: {rfc_id}\n\n"
        f"Table of Contents:\n{toc_formatted}\n\n"
        "Select the section IDs containing the primary cryptographic message exchange or handshake. "
        "Output ONLY bare numerical and dotted section IDs (e.g., \"3\", \"4.1\", \"7.1.2\") without '#' or 'Section'."
    )

    system_prompt = build_schema_system_prompt(
        PROMPT_SECTION_ROUTER,
        SectionRoutingDecision,
    )

    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=sampling_temp,
            max_tokens=prompt_spec.max_tokens,
            json_mode=True,
        )
        response = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=prompt_spec.timeout,
        )
        from src.cost_tracker import GLOBAL_COST_TRACKER
        GLOBAL_COST_TRACKER.record_llm_call(response, role="router", model_name=model_name, stage=1)

        raw_content = response.choices[0].message.content
        decision_data = parse_llm_json(raw_content)

        decision = SectionRoutingDecision.model_validate(decision_data)

        valid_toc_ids = {entry.section_id for entry in toc_entries}
        filtered_section_ids: List[str] = []
        for raw_sec_id in decision.selected_section_ids:
            matched_id = _match_valid_toc_id(raw_sec_id, valid_toc_ids)
            if matched_id and matched_id not in filtered_section_ids:
                filtered_section_ids.append(matched_id)

        if not filtered_section_ids:
            logger.warning(
                "Model suggested sections %s not in TOC. Falling back to heuristic.",
                decision.selected_section_ids,
            )
            return _heuristic_section_router(toc_entries)

        logger.info("Router selected sections %s: %s", filtered_section_ids, decision.rationale)
        return filtered_section_ids

    except Exception as exc:
        logger.error("LLM section router failed: %s. Using heuristic fallback.", str(exc))
        return _heuristic_section_router(toc_entries)


def _heuristic_section_router(toc_entries: List[TOCSectionEntry]) -> List[str]:
    """Deterministic keyword fallback for selecting exchange sections from TOC."""
    excluded_titles = (
        "introduction",
        "terminology",
        "conventions",
        "requirements language",
        "notation",
        "definitions",
        "scope",
        "background",
        "iana considerations",
        "security considerations",
        "references",
        "normative references",
        "informative references",
        "acknowledgements",
        "acknowledgments",
        "full copyright statement",
        "copyright notice",
        "intellectual property",
        "author's address",
        "authors' addresses",
        "editor's address",
        "status of this memo",
        "abstract",
        "table of contents",
    )

    exchange_keywords = [
        "handshake",
        "message exchange",
        "protocol exchange",
        "authentication",
        "key exchange",
        "key agreement",
        "protocol overview",
        "protocol description",
        "protocol operation",
        "overview of operation",
        "operation",
        "communication",
        "transactions",
        "packet types",
        "message format",
    ]

    selected_sections: List[str] = []
    for entry in toc_entries:
        title_lower = entry.title.lower().strip()
        if any(title_lower == ex or title_lower.startswith(ex + " ") for ex in excluded_titles):
            continue
        # Prefer top-level or second-level sections matching exchange/crypto keywords
        if entry.section_id.count(".") <= 1 and any(keyword in title_lower for keyword in exchange_keywords):
            selected_sections.append(entry.section_id)

    if not selected_sections:
        for entry in toc_entries:
            title_lower = entry.title.lower().strip()
            if any(title_lower == ex or title_lower.startswith(ex + " ") for ex in excluded_titles):
                continue
            if entry.section_id.count(".") == 0 and entry.section_id not in ("1",):
                selected_sections.append(entry.section_id)
                if len(selected_sections) >= 3:
                    break

    logger.info("Heuristic router selected sections: %s", selected_sections)
    return selected_sections or (["2"] if toc_entries else [])
```

---

### `src/document_ingestion/protocol_applicability_gate.py`

*sha256:`bc190bacc005` · 142 lines · 5.3 KB (~1,358 tokens) · lang:`python`*

```python
"""Protocol Applicability Gate (Tier 1 Gatekeeper).

Evaluates an RFC's frontmatter, abstract, and complete Table of Contents to
determine whether it specifies an interactive cryptographic security protocol
eligible for MITRE CPSA 4.4.9 formal verification.
"""

import json
from typing import List, Optional
import json_repair
import litellm
from pydantic import BaseModel, Field

from src.document_ingestion.rfc_toc_parser import TOCSectionEntry
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    build_schema_system_prompt,
    load_prompt_spec,
    parse_llm_json,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("applicability_gate")


class ProtocolApplicabilityReport(BaseModel):
    """Assessment of whether an RFC specifies an interactive cryptographic protocol eligible for CPSA."""

    is_cryptographic_protocol: bool = Field(
        ...,
        description="True if the document specifies an interactive protocol with cryptographic terms (keys, nonces, auth)",
    )
    protocol_name: Optional[str] = Field(None, description="Standard protocol name extracted from title")
    participating_principals: List[str] = Field(
        default_factory=list,
        description="Identified roles or principals",
    )
    has_keys_or_nonces: bool = Field(
        ...,
        description="True if the protocol uses encryption keys, certificates, nonces, or digital signatures",
    )
    rationale: str = Field(..., description="Justification for acceptance or rejection")


def evaluate_protocol_applicability(
    rfc_id: str,
    title: str,
    category: str,
    abstract: str,
    toc_entries: List[TOCSectionEntry],
    model: Optional[str] = None,
) -> ProtocolApplicabilityReport:
    """Evaluates an RFC using its frontmatter and entire TOC to determine CPSA eligibility."""
    prompt_spec = load_prompt_spec(PROMPT_APPLICABILITY_GATE)
    model_name = model or prompt_spec.model
    sampling_temp = prompt_spec.temperature
    logger.info("Evaluating protocol applicability for %s: '%s' using model %s", rfc_id, title, model_name)

    toc_summary = "\n".join(f"{entry.section_id} {entry.title}" for entry in toc_entries)

    user_prompt = (
        f"RFC Identifier: {rfc_id}\n"
        f"Title: {title}\n"
        f"Category: {category}\n\n"
        f"Abstract:\n{abstract}\n\n"
        f"Complete Table of Contents:\n{toc_summary}\n\n"
        "Determine if this RFC is an eligible interactive cryptographic protocol for MITRE CPSA formal verification."
    )

    system_prompt = build_schema_system_prompt(
        PROMPT_APPLICABILITY_GATE,
        ProtocolApplicabilityReport,
    )

    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=sampling_temp,
            max_tokens=prompt_spec.max_tokens,
            json_mode=True,
        )
        response = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=prompt_spec.timeout,
        )
        from src.cost_tracker import GLOBAL_COST_TRACKER
        GLOBAL_COST_TRACKER.record_llm_call(response, role="router", model_name=model_name, stage=1)

        raw_content = response.choices[0].message.content
        report_data = parse_llm_json(raw_content)

        report = ProtocolApplicabilityReport.model_validate(report_data)

        if report.is_cryptographic_protocol and (
            not report.has_keys_or_nonces or len(report.participating_principals) < 2
        ):
            logger.info(
                "Tier 1 REJECT (Incomplete Crypto/Principals): %s had is_cryptographic_protocol=True "
                "but has_keys_or_nonces=%s, principals=%s",
                rfc_id,
                report.has_keys_or_nonces,
                report.participating_principals,
            )
            report.is_cryptographic_protocol = False

        if report.is_cryptographic_protocol:
            logger.info(
                "Tier 1 ACCEPT: %s is eligible (Protocol: '%s', Principals: %s). Reason: %s",
                rfc_id,
                report.protocol_name,
                report.participating_principals,
                report.rationale,
            )
        else:
            logger.info("Tier 1 REJECT: %s is ineligible. Reason: %s", rfc_id, report.rationale)

        return report

    except Exception as exc:
        logger.error("LLM gatekeeper evaluation failed: %s. Falling back to heuristic check.", str(exc))
        combined_text = f"{title} {abstract} {toc_summary}".lower()
        has_crypto = any(
            term in combined_text
            for term in ["cryptographic", "handshake", "cipher", "secret", "nonce", "authentication service"]
        )
        is_protocol = any(
            term in combined_text
            for term in ["protocol", "exchange", "message format", "handshake"]
        )

        return ProtocolApplicabilityReport(
            is_cryptographic_protocol=has_crypto and is_protocol,
            protocol_name=title,
            participating_principals=["initiator", "responder"] if has_crypto else [],
            has_keys_or_nonces=has_crypto,
            rationale=f"Heuristic determination: crypto_terms={has_crypto}, protocol_terms={is_protocol}",
        )
```

---

### `src/document_ingestion/rfc_header_filter.py`

*sha256:`ee1e8df89d04` · 183 lines · 7.2 KB (~1,855 tokens) · lang:`python`*

```python
"""RFC Header and Frontmatter Metadata Filter (Tier 0 Filter)."""

import re
from typing import Optional
from pydantic import BaseModel, Field

from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("header_filter")


class HeaderFilterResult(BaseModel):
    """Result of Tier 0 RFC frontmatter analysis."""
    is_eligible: bool = Field(..., description="Whether the RFC is potentially an eligible protocol")
    rfc_id: Optional[str] = Field(None, description="RFC identifier (e.g. 'RFC ####')")
    title: Optional[str] = Field(None, description="Extracted document title")
    category: Optional[str] = Field(None, description="Category (Standards Track, Informational, etc.)")
    disqualification_reason: Optional[str] = Field(None, description="Reason if disqualified")


DISQUALIFIED_TITLE_KEYWORDS = [
    "management information base",
    "managed objects",
    "definitions of managed objects",
    " mib",
    " mib-",
    "architecture",
    "applicability statement",
    "problem statement",
    "requirements for",
    "iana considerations",
    "registry",
    "guidelines for",
    "guidance for",
    "use cases",
    "threat model",
    "framework for",
    "dhcp option",
    "dhcpv6 option",
    "header extension",
    "padding option",
    "security mechanisms",
    "data model",
    "yang",
    "meeting",
    "minutes",
    "equipment purchase",
    "millennium problem",
]

DISQUALIFIED_CATEGORIES = [
    "historic",
    "best current practice",
]

FRONTMATTER_CRYPTO_REGEX = re.compile(
    r"\b(cryptograph|cipher|encrypt|decrypt|diffie-hellman|ecdh|dh\b|hmac|mac\b|signature|"
    r"shared\s+secret|key\s+exchange|key\s+agreement|key\s+establishment|key\s+derivation|"
    r"handshake|nonce|public\s+key|private\s+key|symmetric\s+key|session\s+key|"
    r"authentication|authenticated|authenticator|certificate|x\.509|pkix|"
    r"tls|dtls|ipsec|ike|ikev2|isakmp|oakley|kerberos|edhoc|oscore|wireguard|ssh|secsh|"
    r"sasl|gss-api|gssapi|eap|pana|hip\b|mls\b|acme|ntpsec|nts\b|dnscurve|dnssec|rpki|"
    r"s/mime|openpgp|cms\b|cose|jose|jwt|jws|jwe|oauth|openid|spake|pake|srp\b|ake\b)\b",
    re.IGNORECASE,
)

FRONTMATTER_PROTOCOL_REGEX = re.compile(
    r"\b(protocol|handshake|exchange|authentication|key\s+agreement|key\s+establishment|"
    r"session|message|client|server|initiator|responder|peer)\b",
    re.IGNORECASE,
)


def filter_rfc_header(raw_rfc_text: str) -> HeaderFilterResult:
    """Evaluates the top 100 lines of an RFC for eligibility before invoking any LLM."""
    lines = raw_rfc_text.splitlines()[:100]
    header_text = "\n".join(lines)

    logger.debug("Executing Tier 0 frontmatter filter on top %d lines", len(lines))

    # 1. Line count check (trivial errata / 1-page stubs)
    total_lines = len(raw_rfc_text.splitlines())
    if total_lines < 60:
        logger.info("Tier 0 REJECT: File has only %d lines (trivial stub)", total_lines)
        return HeaderFilterResult(
            is_eligible=False,
            disqualification_reason=f"Document is too short to be a protocol ({total_lines} lines)",
        )

    # 2. Extract RFC ID
    rfc_match = re.search(r"Request for Comments:\s*#?(\d+)", header_text, re.IGNORECASE)
    rfc_id = f"RFC {rfc_match.group(1)}" if rfc_match else None

    # 3. Extract Category (stop at multiple spaces before right-column date)
    category_match = re.search(r"Category:\s*([A-Za-z\s]+?)(?:\s{2,}|\n|$)", header_text, re.IGNORECASE)
    category = category_match.group(1).strip() if category_match else "Unknown"

    for dis_cat in DISQUALIFIED_CATEGORIES:
        if dis_cat.lower() in category.lower():
            logger.info("Tier 0 REJECT: Disqualified category '%s'", category)
            return HeaderFilterResult(
                is_eligible=False,
                rfc_id=rfc_id,
                category=category,
                disqualification_reason=f"Category '{category}' is not a protocol specification",
            )

    # 4. Extract Title: lines between author/category block and "Status of This Memo" (or top header fallback for pre-RFC-2223 RFCs)
    title: Optional[str] = None
    status_idx = next(
        (i for i, l in enumerate(lines) if re.search(r"^\s*(Status of [Tt]his Memo|Abstract)\b", l, re.IGNORECASE)),
        None,
    )

    title_candidate_lines = []
    if status_idx is not None:
        # Search backwards from Status of This Memo for consecutive non-empty lines
        idx = status_idx - 1
        while idx >= 0 and not lines[idx].strip():
            idx -= 1
        while idx >= 0 and lines[idx].strip():
            line_str = lines[idx].strip()
            if re.search(r"(Category:|Updates:|Obsoletes:|Request for Comments|Network Working Group|ISSN:)", line_str, re.IGNORECASE):
                break
            title_candidate_lines.insert(0, line_str)
            idx -= 1
    else:
        # Legacy pre-RFC-2223 format (no "Status of This Memo" or "Abstract"):
        # Find the end of the top header block within the first 30 lines, then take the first centered/indented title block.
        header_end_idx = 0
        for i, l in enumerate(lines[:25]):
            if re.search(r"(Request for Comments|Network Working Group|RFC\s*#?\s*\d+|NIC\s*#?\s*\d+|Category:|Obsoletes:|Updates:)", l, re.IGNORECASE):
                header_end_idx = i + 1
        idx = header_end_idx
        while idx < min(len(lines), 45) and not lines[idx].strip():
            idx += 1
        while idx < min(len(lines), 45) and lines[idx].strip():
            line_str = lines[idx].strip()
            if re.match(r"^(?:1(?:\.|\s+-)?\s+|Introduction\b)", line_str, re.IGNORECASE):
                break
            title_candidate_lines.append(line_str)
            idx += 1

    if title_candidate_lines:
        title = " ".join(title_candidate_lines)

    # 5. Check Title Keywords
    if title:
        title_lower = title.lower()
        for kw in DISQUALIFIED_TITLE_KEYWORDS:
            if kw in title_lower:
                logger.info("Tier 0 REJECT: Title '%s' matches blacklist keyword '%s'", title, kw)
                return HeaderFilterResult(
                    is_eligible=False,
                    rfc_id=rfc_id,
                    title=title,
                    category=category,
                    disqualification_reason=f"Title keyword '{kw}' indicates non-protocol document",
                )

    # 6. Fast Frontmatter / Abstract / TOC Cryptographic & Protocol Vocabulary Gate
    frontmatter_slice = "\n".join(raw_rfc_text.splitlines()[:350])
    if not FRONTMATTER_CRYPTO_REGEX.search(frontmatter_slice) or not FRONTMATTER_PROTOCOL_REGEX.search(frontmatter_slice):
        logger.info(
            "Tier 0 REJECT: %s ('%s') lacks cryptographic/authentication protocol vocabulary in frontmatter/TOC",
            rfc_id or "Unknown RFC",
            title or "Unknown Title",
        )
        return HeaderFilterResult(
            is_eligible=False,
            rfc_id=rfc_id,
            title=title,
            category=category,
            disqualification_reason="Frontmatter, abstract, and TOC lack cryptographic security protocol terminology",
        )

    logger.info("Tier 0 PASS: %s - '%s' (%s)", rfc_id or "Unknown RFC", title or "Unknown Title", category)
    return HeaderFilterResult(
        is_eligible=True,
        rfc_id=rfc_id,
        title=title,
        category=category,
    )
```

---

### `src/document_ingestion/rfc_toc_parser.py`

*sha256:`4920983a2cc9` · 127 lines · 5.8 KB (~1,495 tokens) · lang:`python`*

```python
"""RFC Table of Contents (TOC) Parser."""

import re
from typing import List, Optional
from pydantic import BaseModel, Field

from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("toc_parser")


class TOCSectionEntry(BaseModel):
    """A single section entry parsed from an RFC Table of Contents."""
    section_id: str = Field(..., description="Dotted section number or identifier (e.g. '7.3', 'A.1')")
    title: str = Field(..., description="Section title")
    page_number: Optional[int] = Field(None, description="Page number if present in TOC")
    indent_level: int = Field(default=0, description="Nesting level derived from leading indentation")

    def __str__(self) -> str:
        page_str = f" (p. {self.page_number})" if self.page_number else ""
        return f"{self.section_id} {self.title}{page_str}"


TOC_HEADER_PATTERN = re.compile(r"^\s*(Table of Contents|CONTENTS)\s*$", re.IGNORECASE)

# Matches lines like:
# "   7.3. Handshake Protocol Overview ...............................33"
# "     5.1.  Updated Section "Location Attributes" . . . . . . . . . .   8"
# "   Appendix A.  Protocol Structures ..................................68"
# "   1.  Introduction"
TOC_LINE_PATTERN = re.compile(
    r"^(?P<indent>\s*)(?P<sec_id>(?:(?:[0-9]+(?:\.[0-9]+)*)|(?:Appendix\s+[A-Z](?:\.[0-9]+)*)|(?:[A-Z]\.[0-9]+)|(?:[A-Z](?=\.\s+\S+.*(?:\.{2,}|\.\s+\.)))))(?:\.|\s+-)?\s+"
    r"(?P<title>.+?)"
    r"(?:\s*(?:\.{2,}|(?:\.\s+){2,}|\.\s+)\s*(?P<page>[0-9]+))?\s*$",
    re.IGNORECASE,
)


def parse_table_of_contents(raw_rfc_text: str) -> List[TOCSectionEntry]:
    """Extracts the complete Table of Contents hierarchy from an RFC text document."""
    lines = raw_rfc_text.splitlines()
    toc_start_idx: Optional[int] = None

    # Step 1: Find the TOC Header within the first 250 lines
    for idx, line in enumerate(lines[:250]):
        if TOC_HEADER_PATTERN.match(line):
            toc_start_idx = idx + 1
            break

    entries: List[TOCSectionEntry] = []

    if toc_start_idx is not None:
        logger.debug("Found TOC header at line %d", toc_start_idx)
        current_entry: Optional[TOCSectionEntry] = None

        # Scan forward until the first section begins at column 0 (e.g. "1.  Introduction")
        for line in lines[toc_start_idx:]:
            # If we hit the actual start of Section 1 at column 0, TOC has ended
            if re.match(r"^1(?:\.|\s+-)?\s+[A-Z]", line):
                break
            # Or if we hit 500 entries without stopping
            if len(entries) > 500:
                break

            match = TOC_LINE_PATTERN.match(line)
            if match:
                sec_id = match.group("sec_id").strip()
                # Clean up "Appendix A" -> "App-A"
                sec_id = re.sub(r"Appendix\s+", "App-", sec_id, flags=re.IGNORECASE)
                title = match.group("title").strip()
                page = int(match.group("page")) if match.group("page") else None
                indent = len(match.group("indent"))

                current_entry = TOCSectionEntry(
                    section_id=sec_id,
                    title=title,
                    page_number=page,
                    indent_level=indent,
                )
                entries.append(current_entry)
            elif current_entry and line.strip():
                stripped_line = line.strip()
                # Skip form feeds, page headers, footers
                if (
                    "\x0c" in line
                    or re.search(r"\[Page\s+\d+\]", stripped_line, re.IGNORECASE)
                    or re.search(r"\b(Standards Track|Informational|Experimental)\b", stripped_line, re.IGNORECASE)
                    or re.search(r"^RFC\s+\d+", stripped_line, re.IGNORECASE)
                ):
                    continue

                # Strip trailing dots or page numbers if on second line
                dots_match = re.search(r"^(.*?)(?:\s*(?:\.{2,}|(?:\.\s+){2,})\s*([0-9]+))?$", stripped_line)
                if dots_match:
                    sub_title = dots_match.group(1).strip()
                    # Do not append if sub_title looks like a new unnumbered back-matter section
                    if re.search(
                        r"^(Security Considerations|IANA Considerations|References|Normative References|"
                        r"Informative References|Acknowledg(?:e)?ments|(?:Author|Editor|Chair)[s']*\s*Address(?:es)?|"
                        r"Full Copyright Statement|Intellectual Property|Appendix\b)",
                        sub_title,
                        re.IGNORECASE,
                    ):
                        current_entry = None
                        continue
                    if sub_title:
                        current_entry.title += f" {sub_title}"
                    if dots_match.group(2) and current_entry.page_number is None:
                        current_entry.page_number = int(dots_match.group(2))

    # Step 2: Fallback if no explicit TOC header exists: scan column-0 headings in body
    if not entries:
        logger.info("No explicit TOC block found. Scanning body headings for synthetic TOC...")
        body_heading_pattern = re.compile(
            r"^(?P<sec_id>(?:[0-9]+\.[0-9]+(?:\.[0-9]+)*(?:\.|\s+-)?)|(?:[0-9]+(?:\.|\s+-))|(?:Appendix\s+[A-Z](?:\.[0-9]+)*\.?)|(?:[A-Z]\.[0-9]+\.?))\s+"
            r"(?P<title>[A-Za-z0-9][A-Za-z0-9\s\-_,:()'\"/]{2,70})$"
        )
        for line in lines:
            match = body_heading_pattern.match(line)
            if match:
                sec_id = re.sub(r"\s+-$", "", match.group("sec_id").strip()).rstrip(".")
                sec_id = re.sub(r"^Appendix\s+", "App-", sec_id, flags=re.IGNORECASE)
                title = match.group("title").strip()
                entries.append(TOCSectionEntry(section_id=sec_id, title=title, page_number=None, indent_level=0))

    logger.info("Parsed %d TOC section entries", len(entries))
    return entries
```

---

### `src/document_ingestion/verbatim_section_slicer.py`

*sha256:`ebee5f9bcfae` · 217 lines · 9.2 KB (~2,349 tokens) · lang:`python`*

```python
"""Verbatim RFC Section Boundary Slicer."""

import re
from typing import List, Optional, Tuple

from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("section_slicer")

_ANY_SECTION_HEADING_RE = re.compile(
    r"^(?:(\d+(?:\.\d+)+)(?:\.|\s+-)?|(\d+)(?:\.|\s+-)|(\d+)|Appendix\s+([A-Z](?:\.\d+)*)\.?|([A-Z](?:\.\d+)+)\.?|([A-Z])\.)\s+"
    r"(?=[A-Za-z0-9\"'\(\[])"
)
_TOC_DOT_LEADER_RE = re.compile(r"(?:\.{3,}|(?:\.\s+){3,})\s*\d+\s*$")


def _is_rfc_page_break(line: str) -> bool:
    """Detects RFC pagination artifacts (form feeds, header/footer lines)."""
    stripped = line.strip()
    if "\x0c" in line:
        return True
    if re.search(r"\[Page\s+\d+\]$", stripped, re.IGNORECASE):
        return True
    if re.search(r"^RFC\s+\d+", stripped, re.IGNORECASE):
        return True
    return False


def _clean_requested_sec_id(section_id: str) -> str:
    """Normalizes a section identifier for body heading lookup."""
    s = section_id.strip().strip("`'\"")
    s = re.sub(r"^[#§]+\s*", "", s)
    s = re.sub(r"^(?:Section|Sec\.?)\s+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^(?:Appendix\s+|App-)", "", s, flags=re.IGNORECASE)
    return s.rstrip(".")


def _find_section_start(lines: List[str], section_id: str, search_from_line: int = 0) -> Optional[int]:
    """Finds the line index where a section heading starts at column 0 in the body text."""
    clean_id = _clean_requested_sec_id(section_id)
    if not clean_id:
        return None
    escaped_id = re.escape(clean_id)
    # Match "^7.3.  Title", "^2 - Authentication", "^6.7.2.  0x0002 - AUTHENTICATION_TYPE", or "^Appendix A.  Title"
    if "." in clean_id:
        pattern = re.compile(
            rf"^(?:{escaped_id}(?:\.|\s+-)?|Appendix\s+{escaped_id}\.?)\s+[A-Za-z0-9\"'\(\[]",
            re.IGNORECASE,
        )
    else:
        pattern = re.compile(
            rf"^(?:{escaped_id}(?:\.|\s+-)\s+[A-Za-z0-9\"'\(\[]|{escaped_id}\s+[A-Za-z]|Appendix\s+{escaped_id}\.?\s+[A-Za-z0-9\"'\(\[])",
            re.IGNORECASE,
        )

    for idx in range(search_from_line, len(lines)):
        line = lines[idx]
        if pattern.match(line) and not _TOC_DOT_LEADER_RE.search(line):
            return idx
    return None


def _find_section_end(lines: List[str], section_id: str, start_line_idx: int) -> int:
    """Finds the line index where `section_id` (and any of its nested subsections) ends."""
    norm_id = _clean_requested_sec_id(section_id)
    sub_prefix = f"{norm_id}."

    for idx in range(start_line_idx + 1, len(lines)):
        line = lines[idx]
        if _TOC_DOT_LEADER_RE.search(line):
            continue
        match = _ANY_SECTION_HEADING_RE.match(line)
        if match:
            # If matched group(3) (bare integer without dot), require uppercase letter start for title
            if match.group(3) and not re.match(r"^\d+\s+[A-Z]", line):
                continue
            found_id = (
                match.group(1)
                or match.group(2)
                or match.group(3)
                or match.group(4)
                or match.group(5)
                or match.group(6)
                or ""
            ).rstrip(".")
            if found_id and found_id.lower() != norm_id.lower() and not found_id.lower().startswith(sub_prefix.lower()):
                return idx

    return min(start_line_idx + 600, len(lines))


def _slice_unnumbered_rfc_body(lines: List[str], clean_page_breaks: bool = True) -> str:
    """Fallback slicer for short RFCs with unnumbered section headings (e.g., RFC 3268)."""
    start_idx = 0
    for idx, line in enumerate(lines[:150]):
        if re.match(r"^(?:Overview|Introduction|1\.?\s+Introduction)\s*$", line.strip(), re.IGNORECASE):
            start_idx = idx
            break
        if re.match(r"^Abstract\s*$", line.strip(), re.IGNORECASE):
            start_idx = idx
    end_idx = len(lines)
    for idx in range(start_idx + 1, len(lines)):
        if re.match(
            r"^(?:References|Normative References|Informative References|"
            r"Author(?:'s|s')?\s+Address(?:es)?|Full Copyright Statement)\s*$",
            lines[idx].strip(),
            re.IGNORECASE,
        ):
            end_idx = idx
            break
    end_idx = min(end_idx, start_idx + 600)
    sliced = lines[start_idx:end_idx]
    if clean_page_breaks:
        sliced = [line for line in sliced if not _is_rfc_page_break(line)]
    return "\n".join(sliced).strip()


def slice_verbatim_sections(
    raw_rfc_text: str,
    target_section_ids: List[str],
    clean_page_breaks: bool = True,
) -> str:
    """Extracts the verbatim text for the specified section IDs from an RFC document,
    slicing each requested section individually and merging overlapping/contiguous spans.
    """
    lines = raw_rfc_text.splitlines()
    if not target_section_ids or target_section_ids == ["FULL_BODY"]:
        if len(lines) <= 1000 or target_section_ids == ["FULL_BODY"]:
            logger.info("Using unnumbered/full-body fallback slicer (%d document lines)", len(lines))
            return _slice_unnumbered_rfc_body(lines, clean_page_breaks=clean_page_breaks)
        logger.warning("No target section IDs provided for slicing")
        return ""

    # Step 1: Skip past the Table of Contents to avoid matching TOC entries as section starts
    toc_end_idx = 100
    for idx, line in enumerate(lines[:800]):
        if re.match(r"^1(?:\.0)?\.?\s+[A-Z]", line) and not _TOC_DOT_LEADER_RE.search(line):
            toc_end_idx = idx
            break

    # Step 2: Resolve [start, end) line intervals for each requested section
    intervals: List[Tuple[int, int]] = []
    seen_parent_preambles = set()
    for raw_sec_id in target_section_ids:
        sec_id = _clean_requested_sec_id(raw_sec_id) or raw_sec_id.strip()
        # If a first subsection (e.g. "3.1") is requested without its parent ("3"),
        # also include the parent section's introductory preamble ("3" -> "3.1")
        if sec_id.endswith(".1") and sec_id.count(".") == 1:
            parent_id = sec_id.split(".")[0]
            if parent_id not in target_section_ids and parent_id not in seen_parent_preambles:
                seen_parent_preambles.add(parent_id)
                p_start = _find_section_start(lines, parent_id, search_from_line=toc_end_idx)
                if p_start is not None:
                    first_sub = _find_section_start(lines, f"{parent_id}.1", search_from_line=p_start + 1)
                    if first_sub is not None and first_sub > p_start and (first_sub - p_start) <= 120:
                        intervals.append((p_start, first_sub))

        start_idx = _find_section_start(lines, sec_id, search_from_line=toc_end_idx)
        if start_idx is None:
            start_idx = _find_section_start(lines, sec_id, search_from_line=0)
        resolved_sec_id = sec_id
        # Parent-section fallback if a deeply nested subsection (e.g. "6.7.2") has a malformed body heading
        while start_idx is None and "." in resolved_sec_id:
            parent_candidate = resolved_sec_id.rsplit(".", 1)[0]
            logger.warning(
                "Section '%s' not found directly; attempting parent section fallback '%s'",
                resolved_sec_id,
                parent_candidate,
            )
            resolved_sec_id = parent_candidate
            start_idx = _find_section_start(lines, resolved_sec_id, search_from_line=toc_end_idx)
            if start_idx is None:
                start_idx = _find_section_start(lines, resolved_sec_id, search_from_line=0)

        if start_idx is None:
            if not intervals and raw_sec_id == target_section_ids[0] and len(target_section_ids) == 1:
                logger.error("Could not locate starting section '%s' in document", sec_id)
                raise ValueError(f"Section '{sec_id}' not found in document")
            logger.warning("Requested section '%s' not found in document; skipping", sec_id)
            continue
        end_idx = _find_section_end(lines, resolved_sec_id, start_idx)
        intervals.append((start_idx, end_idx))

    if not intervals:
        raise ValueError(f"None of the requested sections {target_section_ids} were found in document")

    # Step 3: Sort and merge overlapping or adjacent intervals
    intervals.sort(key=lambda pair: pair[0])
    merged: List[Tuple[int, int]] = [intervals[0]]
    for cur_start, cur_end in intervals[1:]:
        prev_start, prev_end = merged[-1]
        if cur_start <= prev_end:
            merged[-1] = (prev_start, max(prev_end, cur_end))
        else:
            merged.append((cur_start, cur_end))

    total_raw_lines = sum(end - start for start, end in merged)
    span_desc = ", ".join(f"{s + 1}..{e}" for s, e in merged)
    logger.info(
        "Slicing sections %s: spans [%s] (%d raw lines)",
        target_section_ids,
        span_desc,
        total_raw_lines,
    )

    sliced_lines: List[str] = []
    for idx, (s_idx, e_idx) in enumerate(merged):
        if idx > 0 and sliced_lines:
            sliced_lines.append("")
        sliced_lines.extend(lines[s_idx:e_idx])

    if clean_page_breaks:
        cleaned = [line for line in sliced_lines if not _is_rfc_page_break(line)]
        logger.debug("Cleaned %d page break lines from slice", len(sliced_lines) - len(cleaned))
        sliced_lines = cleaned

    return "\n".join(sliced_lines)
```

---

### `src/generate_think/__init__.py`

*sha256:`0b7690b5089c` · 27 lines · 0.8 KB (~201 tokens) · lang:`python`*

```python
"""Phase 3 Hindsight Reasoning (<think>) Synthesizer Package."""

from src.generate_think.think_schema import (
    DPOContrastivePair,
    SynthesizedReasoningSteps,
    ThinkArtifactBundle,
)
from src.generate_think.dspy_think_synthesizer import (
    CPSAHindsightReasoningSignature,
    CPSAHindsightThinkModule,
    compile_deterministic_reasoning_steps,
    generate_think_for_trajectory,
    process_run_directory,
    synthesize_reasoning_steps_via_dspy_or_llm,
)

__all__ = [
    "DPOContrastivePair",
    "SynthesizedReasoningSteps",
    "ThinkArtifactBundle",
    "CPSAHindsightReasoningSignature",
    "CPSAHindsightThinkModule",
    "compile_deterministic_reasoning_steps",
    "generate_think_for_trajectory",
    "process_run_directory",
    "synthesize_reasoning_steps_via_dspy_or_llm",
]
```

---

### `src/generate_think/cli.py`

*sha256:`1c3edd0a8eb8` · 96 lines · 3.2 KB (~819 tokens) · lang:`python`*

```python
"""Command-line interface for Phase 3 Hindsight Reasoning (<think>) Synthesis."""

import argparse
import sys
from pathlib import Path

from src.logging_config import configure_pipeline_logging
from src.system_config import SYSTEM_CONFIG
from src.generate_think.dspy_think_synthesizer import process_run_directory


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "RFC-LLM Phase 3 (<think> Synthesizer): Generates <protocol>_think.json alongside "
            "<protocol>_trajectory.json using DSPy Hindsight Rationalization + Compiler Backtracking."
        ),
    )
    parser.add_argument(
        "target_path",
        type=str,
        help=(
            "Path to a timestamped run directory (e.g. output/run_2026-10-19_19-17-33), "
            "a metadata_index.json file, an RFC directory, or a specific <protocol>_trajectory.json file."
        ),
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help=(
            "Provider-agnostic model identifier (e.g. 'strata/unsloth-iq4_xs', 'ollama/qwq:32b', 'nous/deepseek/deepseek-chat', "
            "'gemini/gemini-2.5-flash'). Defaults to `model:` in prompts/07_think_token_synthesizer.md."
        ),
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "llm", "deterministic"],
        default="auto",
        help=(
            "Synthesis mode: 'auto' (DSPy/LLM hindsight rationalization with deterministic fallback), "
            "'llm' (DSPy/LLM hindsight rationalization), or 'deterministic' (100%% programmatic AST + "
            "compiler trajectory rendering with zero LLM calls)."
        ),
    )
    parser.add_argument(
        "--min-tier",
        choices=["GOLD", "SILVER", "BRONZE", "REJECTED"],
        default="BRONZE",
        help="Minimum verification quality tier to synthesize <think> tokens for (default: BRONZE).",
    )
    parser.add_argument(
        "--no-jsonl",
        action="store_true",
        help="Do not export consolidated sft_train.jsonl and dpo_pairs.jsonl in the run directory.",
    )

    args = parser.parse_args()
    target = Path(args.target_path)

    if not target.exists():
        print(f"Error: Target path does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    configure_pipeline_logging()
    active_model = args.model or SYSTEM_CONFIG.DEFAULT_THINK_MODEL

    print(f"\n{'=' * 70}")
    print(" RFC-LLM PHASE 3: HINDSIGHT REASONING (<think>) SYNTHESIZER")
    print(f"{'=' * 70}")
    print(f"- Target Path : {target.resolve()}")
    print(f"- Mode        : {args.mode}")
    if args.mode != "deterministic":
        print(f"- Model       : {active_model}")
    print(f"- Min Tier    : {args.min_tier}")
    print(f"{'=' * 70}\n")

    generated_files = process_run_directory(
        target_path=target,
        model=active_model,
        mode=args.mode,
        min_tier=args.min_tier,
        export_jsonl=not args.no_jsonl,
    )

    print(f"\n{'=' * 70}")
    print(f" PHASE 3 COMPLETE: Generated {len(generated_files)} <protocol>_think.json artifact(s)")
    print(f"{'=' * 70}")
    for path in generated_files:
        print(f"  -> {path}")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()
```

---

### `src/generate_think/dspy_think_synthesizer.py`

*sha256:`3c6700ca4133` · 758 lines · 35.3 KB (~9,039 tokens) · lang:`python`*

```python
"""Phase 3 Agentic DSPy Hindsight Reasoning (<think>) Synthesizer.

Implements state-of-the-art Hindsight Rationalization (STaR) + Compiler-Feedback
Backtracking (Stanford s1 / OpenThoughts) to generate `<protocol>_think.json`
inside each RFC directory alongside `<protocol>_trajectory.json` and `<protocol>.scm`.
"""

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import dspy
import json_repair
import litellm

from src.generate_think.think_schema import (
    DPOContrastivePair,
    SynthesizedReasoningSteps,
    ThinkArtifactBundle,
)
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_THINK_SYNTHESIZER,
    build_schema_system_prompt,
    load_prompt,
    load_prompt_spec,
    parse_llm_json,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("think_synthesizer")

# Quality tier ranking for filtering
TIER_RANK: Dict[str, int] = {
    "GOLD": 4,
    "SILVER": 3,
    "BRONZE": 2,
    "REJECTED": 1,
    "INELIGIBLE": 0,
}

SFT_SYSTEM_PROMPT: str = (
    "You are a formal methods expert specializing in MITRE CPSA 4.4.9. "
    "Given an IETF RFC protocol specification, reason step-by-step inside <think>...</think> tags "
    "about the participating principals, message algebra sorts, role traces, origination and "
    "executability invariants, and 3-Point-of-View security preskeletons, then emit a formally "
    "verifiable CPSA Scheme (.scm) specification."
)


class CPSAHindsightReasoningSignature(dspy.Signature):
    """Synthesize a forward-looking, first-person MITRE CPSA 4.4.9 <think> deduction trace from an RFC slice.
    Write strictly as if you are designing the CPSA model from scratch while reading the RFC.
    NEVER mention 'compiler backtracking history', 'preskeleton verdicts', 'provided AST', or any post-hoc verification results;
    instead, use exact CPSA variable names, sorts (name, text, data, skey, akey, rndx, expt, chan), S-expression terms,
    and natural self-checks ('Wait—let me verify CPSA's executability rules...').
    """

    rfc_context_and_slice: str = dspy.InputField(
        desc="RFC ID, Title, Participating Principals, Selected Sections, and Verbatim RFC Specification Slice"
    )
    target_cpsa_identifiers_and_terms: str = dspy.InputField(
        desc="Exact CPSA variable names, sorts, role traces, and skeleton structures that your forward-looking reasoning must derive"
    )
    cpsa_invariants_and_self_checks: str = dspy.InputField(
        desc="CPSA 4.4.9 sort, roletran executability, and origination pitfalls to weave in as 'Wait—let me verify...' self-correction thoughts"
    )
    step1_protocol_and_algebra: str = dspy.OutputField(
        desc="Step 1: First-person deduction of protocol scope, principals, and why basic or diffie-hellman algebra is required"
    )
    step2_principals_and_variables: str = dspy.OutputField(
        desc="Step 2: First-person mapping of RFC fields to every exact CPSA variable identifier and sort (rndx vs expt, text, data, skey, akey, name, chan)"
    )
    step3_message_flow_and_terms: str = dspy.OutputField(
        desc="Step 3: First-person derivation of each role's ordered send/recv events with exact S-expression terms ((cat ...), (enc ...), (exp (gen) ...))"
    )
    step4_compiler_backtracking_and_invariants: str = dspy.OutputField(
        desc="Step 4: First-person self-check ('Wait—let me check CPSA's rules...') verifying uniq-orig, uniq-gen, non-orig, and roletran (inputs ...) destructibility"
    )
    step5_preskeleton_verdicts_and_goals: str = dspy.OutputField(
        desc="Step 5: First-person construction of the 3 defskeleton blocks (Initiator POV without deflistener, Responder POV without deflistener, and Secrecy POV with deflistener)"
    )
    full_thinking_monologue: str = dspy.OutputField(
        desc="Complete, detailed first-person reasoning monologue integrating all exact variable names, sorts, S-expressions, and 'Wait—let me check...' self-corrections from Steps 1-5"
    )


class CPSAHindsightThinkModule(dspy.Module):
    """DSPy Module wrapping CPSAHindsightReasoningSignature for provider-agnostic <think> generation."""

    def __init__(self) -> None:
        super().__init__()
        # Dynamically bind the externalized prompts/07_think_token_synthesizer.md instructions
        CPSAHindsightReasoningSignature.__doc__ = load_prompt(PROMPT_THINK_SYNTHESIZER)
        self.synthesize = dspy.Predict(CPSAHindsightReasoningSignature)

    def forward(
        self,
        rfc_context_and_slice: str,
        target_cpsa_identifiers_and_terms: str,
        cpsa_invariants_and_self_checks: str,
    ) -> dspy.Prediction:
        return self.synthesize(
            rfc_context_and_slice=rfc_context_and_slice,
            target_cpsa_identifiers_and_terms=target_cpsa_identifiers_and_terms,
            cpsa_invariants_and_self_checks=cpsa_invariants_and_self_checks,
        )


def _format_sexpr(term: Any) -> str:
    """Renders a Python list/str term into a compact CPSA S-expression string."""
    if isinstance(term, list):
        return "(" + " ".join(_format_sexpr(t) for t in term) + ")"
    return str(term)


def _extract_compiler_backtracking_summary(trajectory_data: Dict[str, Any]) -> str:
    """Extracts Stage 2, Stage 5, and Stage 6 pitfalls as forward-looking CPSA design self-checks."""
    lines: List[str] = []
    algebra = trajectory_data.get("rfc_metadata", {}).get("algebra", "basic")

    stage2 = trajectory_data.get("stage2_initial_extraction", {})
    if stage2.get("schema_self_correction_triggered") and stage2.get("schema_validation_error"):
        lines.append(
            f"- Self-check on CPSA AST scoping: avoid `{stage2['schema_validation_error']}`."
        )

    stage5 = trajectory_data.get("stage5_preflight_gate", {})
    for att in stage5.get("repair_attempts", []):
        diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or "roletran executability failure"
        lines.append(
            f"- Backtracking self-check ('Wait—let me check role executability...'): if we are not careful, "
            f"`{stage5.get('validator_binary', 'cpsa4roletran')}` would reject with `{diag.splitlines()[0]}`. "
            f"Explain how the role's `(inputs ...)` and key declarations avoid this error."
        )

    stage6 = trajectory_data.get("stage6_cpsa4_solver", {})
    for att in stage6.get("repair_attempts", []):
        diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or "cpsa4 solver failure"
        lines.append(
            f"- Backtracking self-check ('Hold on—let me check CPSA sort and origination rules...'): "
            f"avoid `{diag.splitlines()[0]}` by ensuring sort and origination consistency across roles and skeletons."
        )

    if algebra == "diffie-hellman":
        lines.append(
            "- Proactive DH self-check ('Wait—let me verify CPSA's Diffie-Hellman exponent rules...'): "
            "any fresh private exponent sent in `(exp (gen) x)` must have sort `rndx` with `(uniq-gen x)`, "
            "while the peer receiving that public share must type the received exponent variable as `expt` "
            "(because CPSA requires `rndx` to be sent first and `expt` to be received first)."
        )
    else:
        lines.append(
            "- Proactive basic-algebra self-check ('Wait—let me verify CPSA Equation 10.1 and roletran rules...'): "
            "encryption keys in `(enc ...)` must have sort `skey` or `akey` (never `mesg`), and `(inputs ...)` "
            "must include trace channels and pre-known keys without overlapping `(uniq-orig ...)`."
        )

    lines.append(
        "- Proactive 3-POV Skeleton self-check: construct separate participant POV skeletons (`defstrandmax` with "
        "NO `deflistener`) to test multi-strand authentication, and a dedicated secrecy skeleton with "
        "`(deflistener ...)` and `(non-orig ...)` to test confidentiality."
    )
    return "\n".join(lines)


def compile_deterministic_reasoning_steps(trajectory_data: Dict[str, Any]) -> SynthesizedReasoningSteps:
    """Deterministically compiles a rich 5-step <think> trace directly from the AST and compiler trajectory.

    Requires zero LLM calls while preserving 100% identifier fidelity and compiler backtracking checks.
    """
    rfc_meta = trajectory_data.get("rfc_metadata", {})
    rfc_id = rfc_meta.get("rfc_id", "Unknown RFC")
    rfc_title = rfc_meta.get("rfc_title", "Unknown Protocol")
    algebra = rfc_meta.get("algebra", "basic")
    principals = rfc_meta.get("participating_principals", [])
    sections = rfc_meta.get("selected_sections", [])

    final_out = trajectory_data.get("final_verified_output", {})
    final_ast = final_out.get("final_ast") or trajectory_data.get("stage2_initial_extraction", {}).get("initial_ast") or {}
    herald_comment = final_ast.get("herald_comment", "")
    roles = final_ast.get("roles", [])
    skeletons = final_ast.get("skeletons", [])

    # Step 1: Protocol & Algebra
    algebra_rationale = (
        "Because the handshake employs ephemeral Diffie-Hellman exponentiation `(exp (gen) ...)` to establish "
        "shared session keys, we must select the MITRE CPSA `diffie-hellman` message algebra rather than `basic`."
        if algebra == "diffie-hellman"
        else "Because the protocol relies on symmetric/asymmetric encryption, nonces, hashes, and signatures without "
        "Diffie-Hellman group exponentiation, we select the MITRE CPSA `basic` message algebra."
    )
    step1 = (
        f"Let's analyze {rfc_id} ({rfc_title}), focusing on sections {', '.join(sections) or 'describing the core exchange'}. "
        f"The interactive cryptographic exchange involves {len(roles)} primary roles ({', '.join(r.get('role_name', '') for r in roles) or ', '.join(principals)}). "
        f"{algebra_rationale} "
        f"Scope note: {herald_comment}"
    ).strip()

    # Step 2: Principals & Variables
    role_var_paragraphs: List[str] = []
    for role in roles:
        r_name = role.get("role_name", "role")
        r_desc = role.get("description") or f"Participant role `{r_name}`"
        var_items: List[str] = []
        for var in role.get("variables", []):
            v_name = var.get("name")
            v_sort = var.get("sort")
            v_rfc = var.get("rfc_field")
            v_desc = var.get("description")
            mapping_str = f"`{v_name}` (sort `{v_sort}`)"
            if v_rfc:
                mapping_str += f" [RFC: {v_rfc}]"
            if v_desc:
                mapping_str += f": {v_desc}"
            var_items.append(mapping_str)
        role_var_paragraphs.append(
            f"For role `{r_name}` ({r_desc}), we declare the following typed variables in `(vars ...)`: "
            + "; ".join(var_items)
            + "."
        )
    step2 = "\n".join(role_var_paragraphs) if role_var_paragraphs else "We map each principal's variables to strict CPSA 4.4.9 sorts."

    # Step 3: Message Flow & Terms
    trace_paragraphs: List[str] = []
    for role in roles:
        r_name = role.get("role_name", "role")
        ev_lines: List[str] = []
        for idx, ev in enumerate(role.get("trace", [])):
            direction = ev.get("direction", "send")
            chan = ev.get("channel") or ev.get("location") or ""
            term_str = _format_sexpr(ev.get("message_term", ""))
            ev_desc = ev.get("description") or f"Event {idx}"
            if chan:
                sexpr_ev = f"({direction} {chan} {term_str})"
            else:
                sexpr_ev = f"({direction} {term_str})"
            ev_lines.append(f"Event {idx} ({ev_desc}) -> `{sexpr_ev}`")
        trace_paragraphs.append(
            f"In role `{r_name}`, the ordered `(trace ...)` sequence is: " + "; ".join(ev_lines) + "."
        )
    step3 = "\n".join(trace_paragraphs) if trace_paragraphs else "We construct the ordered send/recv trace events for each role."

    # Step 4: Compiler Backtracking & Invariants
    backtrack_notes: List[str] = []
    stage5 = trajectory_data.get("stage5_preflight_gate", {})
    stage6 = trajectory_data.get("stage6_cpsa4_solver", {})
    for att in stage5.get("repair_attempts", []):
        diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or ""
        backtrack_notes.append(
            f"Wait—let me check pre-flight role executability (`{stage5.get('validator_binary', 'cpsa4roletran')}`): "
            f"an initial formulation would trigger `{diag.splitlines()[0] if diag else 'an executability error'}`. "
            f"We must ensure every received term can be destructured using keys already in scope or declared in `(inputs ...)`."
        )
    for att in stage6.get("repair_attempts", []):
        diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or ""
        backtrack_notes.append(
            f"Hold on—when `cpsa4` evaluates the search space, we must avoid `{diag.splitlines()[0] if diag else 'solver rejection'}` "
            f"by aligning sort declarations and origination assumptions across roles and skeletons."
        )

    for role in roles:
        r_name = role.get("role_name", "role")
        uo = [_format_sexpr(x) for x in role.get("unique_originating", [])]
        ug = [_format_sexpr(x) for x in role.get("unique_generated", [])]
        no = [_format_sexpr(x) for x in role.get("non_originating", [])]
        ins = [_format_sexpr(x) for x in role.get("inputs", [])]
        outs = [_format_sexpr(x) for x in role.get("outputs", [])]
        inv_parts: List[str] = []
        if uo:
            inv_parts.append(f"`(uniq-orig {' '.join(uo)})` for freshly originated nonces/identifiers")
        if ug:
            inv_parts.append(f"`(uniq-gen {' '.join(ug)})` for fresh DH exponents of sort `rndx`")
        if no:
            inv_parts.append(f"`(non-orig {' '.join(no)})` for uncompromised long-term keys")
        if ins:
            inv_parts.append(f"`(inputs {' '.join(ins)})` (excluding any `uniq-orig`/`uniq-gen` terms per cpsa4roletran rules)")
        if outs:
            inv_parts.append(f"`(outputs {' '.join(outs)})`")
        if inv_parts:
            backtrack_notes.append(f"For role `{r_name}`, we enforce: " + ", ".join(inv_parts) + ".")

    if algebra == "diffie-hellman":
        backtrack_notes.append(
            "Wait—let me verify CPSA's Diffie-Hellman exponent discipline: any exponent chosen freshly by a role "
            "and sent first in `(exp (gen) x)` must have sort `rndx` and `(uniq-gen x)`, whereas the peer role "
            "receiving that public share must declare its corresponding exponent variable with sort `expt` "
            "(since CPSA requires `expt` variables to be received first and `rndx` variables to be sent first)."
        )
    else:
        backtrack_notes.append(
            "Wait—let me verify MITRE CPSA Equation 10.1 and `cpsa4roletran` invariants: no variable of sort `mesg` "
            "is used as an encryption key in `(enc ...)`, and every role's `(inputs ...)` contains its trace channels "
            "and initial keys without overlapping `(uniq-orig ...)`."
        )
    step4 = " ".join(backtrack_notes)

    # Step 5: Preskeletons
    skel_notes: List[str] = []
    for idx, skel in enumerate(skeletons):
        s_desc = skel.get("description") or skel.get("comment") or f"Preskeleton {idx + 1}"
        strands_str = ", ".join(f"`(defstrandmax {s.get('role_name')})`" for s in skel.get("strands", []))
        listeners = [_format_sexpr(l) for l in skel.get("listeners", [])]
        non_orig = [_format_sexpr(n) for n in skel.get("non_originating", [])]
        if listeners:
            skel_notes.append(
                f"Skeleton {idx + 1} ({s_desc}): instantiates {strands_str} with `(deflistener {' '.join(listeners)})` "
                f"and `(non-orig {' '.join(non_orig)})` to test whether the penetrator can learn the secret."
            )
        else:
            skel_notes.append(
                f"Skeleton {idx + 1} ({s_desc}): pure participant POV instantiating {strands_str} with NO `deflistener` "
                f"and `(non-orig {' '.join(non_orig)})` so `cpsa4` can realize multi-strand authenticated shapes."
            )
    step5 = " ".join(skel_notes) if skel_notes else "We construct participant POV and secrecy preskeletons."

    full_monologue = (
        f"1. Protocol Scope & Message Algebra:\n{step1}\n\n"
        f"2. Principal Roles & Variable Sort Mapping:\n{step2}\n\n"
        f"3. Message Exchange Trace & Term Construction:\n{step3}\n\n"
        f"4. Compiler Invariants & Self-Correction Checks:\n{step4}\n\n"
        f"5. Point-of-View & Secrecy Preskeleton Formulation:\n{step5}"
    )

    return SynthesizedReasoningSteps(
        step1_protocol_and_algebra=step1,
        step2_principals_and_variables=step2,
        step3_message_flow_and_terms=step3,
        step4_compiler_backtracking_and_invariants=step4,
        step5_preskeleton_verdicts_and_goals=step5,
        full_thinking_monologue=full_monologue,
    )


def _sanitize_hindsight_leakage(text: str) -> str:
    """Removes any accidental references to pre-supplied AST/trajectory artifacts."""
    banned_patterns = [
        (
            r"(?i)\bin the (?:provided|given|supplied) (?:final_ast|initial_ast|final_scm|initial_scm|ast|scm|trajectory|scaffold)\b",
            "in our CPSA model",
        ),
        (
            r"(?i)\blooking at the (?:provided|given|supplied) (?:final_ast|initial_ast|final_scm|initial_scm|ast|scm|code|solution)\b",
            "analyzing the protocol structure",
        ),
        (r"(?i)\baccording to the trajectory metadata\b", "by CPSA's strand-space semantics"),
        (r"(?i)\bthe compiler backtracking history (?:indicates|shows) that\b", "Wait—let me verify CPSA's compiler invariants:"),
        (r"(?i)\bthe preskeleton verdicts confirm that\b", "To verify our security goals in CPSA,"),
    ]
    cleaned = text.strip()
    for pat, repl in banned_patterns:
        cleaned = re.sub(pat, repl, cleaned)
    # Strip any outer <think> or </think> tags if the model included them inside full_thinking_monologue
    cleaned = re.sub(r"^\s*<think>\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*</think>\s*$", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def _compose_comprehensive_monologue(steps: SynthesizedReasoningSteps) -> str:
    """Ensures full_thinking_monologue preserves all concrete variable mappings, sorts, and S-expression terms."""
    if "(cat" in steps.full_thinking_monologue or "(enc" in steps.full_thinking_monologue or "(exp" in steps.full_thinking_monologue:
        return steps.full_thinking_monologue
    return (
        f"1. Protocol Scope & Message Algebra:\n{steps.step1_protocol_and_algebra}\n\n"
        f"2. Principal Roles & Variable Sort Mapping:\n{steps.step2_principals_and_variables}\n\n"
        f"3. Message Exchange Trace & Term Construction:\n{steps.step3_message_flow_and_terms}\n\n"
        f"4. Compiler Invariants & Self-Correction Checks:\n{steps.step4_compiler_backtracking_and_invariants}\n\n"
        f"5. Point-of-View & Secrecy Preskeleton Formulation:\n{steps.step5_preskeleton_verdicts_and_goals}"
    )


def synthesize_reasoning_steps_via_dspy_or_llm(
    trajectory_data: Dict[str, Any],
    model: Optional[str] = None,
) -> Tuple[SynthesizedReasoningSteps, str]:
    """Synthesizes `<think>` steps using DSPy / LiteLLM provider-agnostic routing, with deterministic fallback."""
    think_spec = load_prompt_spec(PROMPT_THINK_SYNTHESIZER)
    model_name = model or think_spec.model
    sampling_temp = think_spec.temperature if think_spec.temperature is not None else 0.2
    rfc_meta = trajectory_data.get("rfc_metadata", {})
    rfc_id = rfc_meta.get("rfc_id", "Unknown RFC")
    rfc_title = rfc_meta.get("rfc_title", "Unknown Protocol")
    principals = rfc_meta.get("participating_principals", [])
    sections = rfc_meta.get("selected_sections", [])
    verbatim_slice = rfc_meta.get("verbatim_rfc_slice", "")

    final_out = trajectory_data.get("final_verified_output", {})
    final_ast = final_out.get("final_ast") or trajectory_data.get("stage2_initial_extraction", {}).get("initial_ast")
    final_scm = final_out.get("final_scm_with_header") or trajectory_data.get("stage2_initial_extraction", {}).get("initial_scm") or ""

    rfc_context_and_slice = (
        f"RFC ID: {rfc_id}\n"
        f"Title: {rfc_title}\n"
        f"Participating Principals: {', '.join(principals)}\n"
        f"Selected Sections: {', '.join(sections)}\n\n"
        f"Verbatim RFC Specification Slice:\n{verbatim_slice}"
    )
    verified_scaffold = (
        f"Verified CPSA AST (JSON):\n{json.dumps(final_ast, indent=2)}\n\n"
        f"Verified CPSA Scheme (.scm):\n{final_scm}"
    )
    backtracking_history = _extract_compiler_backtracking_summary(trajectory_data)

    llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
        model_name,
        temperature=sampling_temp,
        max_tokens=think_spec.max_tokens,
    )

    # First attempt: DSPy CPSAHindsightThinkModule configured with provider-agnostic LM
    try:
        logger.info("Synthesizing <think> reasoning trace for %s using DSPy module (%s)", rfc_id, model_name)
        lm_params = {k: v for k, v in llm_kwargs.items() if k != "model"}
        dspy_lm = dspy.LM(model=llm_kwargs["model"], **lm_params)
        module = CPSAHindsightThinkModule()
        with dspy.context(lm=dspy_lm):
            pred = module(
                rfc_context_and_slice=rfc_context_and_slice,
                target_cpsa_identifiers_and_terms=verified_scaffold,
                cpsa_invariants_and_self_checks=backtracking_history,
            )
        steps = SynthesizedReasoningSteps(
            step1_protocol_and_algebra=_sanitize_hindsight_leakage(str(pred.step1_protocol_and_algebra)),
            step2_principals_and_variables=_sanitize_hindsight_leakage(str(pred.step2_principals_and_variables)),
            step3_message_flow_and_terms=_sanitize_hindsight_leakage(str(pred.step3_message_flow_and_terms)),
            step4_compiler_backtracking_and_invariants=_sanitize_hindsight_leakage(
                str(pred.step4_compiler_backtracking_and_invariants)
            ),
            step5_preskeleton_verdicts_and_goals=_sanitize_hindsight_leakage(
                str(pred.step5_preskeleton_verdicts_and_goals)
            ),
            full_thinking_monologue=_sanitize_hindsight_leakage(str(pred.full_thinking_monologue)),
        )
        steps.full_thinking_monologue = _compose_comprehensive_monologue(steps)
        if len(steps.full_thinking_monologue) >= 120:
            return steps, "dspy_hindsight_llm"
    except Exception as dspy_exc:
        logger.warning(
            "DSPy adapter call for %s encountered (%s); attempting direct JSON-schema completion via LiteLLM...",
            rfc_id,
            dspy_exc,
        )

    # Second attempt: Direct LiteLLM JSON-schema completion using prompts/07_think_token_synthesizer.md
    try:
        system_prompt = build_schema_system_prompt(
            PROMPT_THINK_SYNTHESIZER,
            SynthesizedReasoningSteps,
        )
        user_prompt = (
            f"{rfc_context_and_slice}\n\n"
            f"Compiler & Solver Backtracking Points to Include as Internal Self-Checks:\n{backtracking_history}\n\n"
            f"Target Ground-Truth Scaffold (Arrive at these exact identifiers/terms via first-principles deduction "
            f"without ever mentioning they were provided):\n{verified_scaffold}"
        )
        direct_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=sampling_temp,
            max_tokens=think_spec.max_tokens,
            json_mode=True,
        )
        response = litellm.completion(
            **direct_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=think_spec.timeout,
        )
        raw_content = response.choices[0].message.content
        parsed = parse_llm_json(raw_content)

        steps = SynthesizedReasoningSteps.model_validate(parsed)
        steps.step1_protocol_and_algebra = _sanitize_hindsight_leakage(steps.step1_protocol_and_algebra)
        steps.step2_principals_and_variables = _sanitize_hindsight_leakage(steps.step2_principals_and_variables)
        steps.step3_message_flow_and_terms = _sanitize_hindsight_leakage(steps.step3_message_flow_and_terms)
        steps.step4_compiler_backtracking_and_invariants = _sanitize_hindsight_leakage(
            steps.step4_compiler_backtracking_and_invariants
        )
        steps.step5_preskeleton_verdicts_and_goals = _sanitize_hindsight_leakage(
            steps.step5_preskeleton_verdicts_and_goals
        )
        steps.full_thinking_monologue = _sanitize_hindsight_leakage(steps.full_thinking_monologue)
        steps.full_thinking_monologue = _compose_comprehensive_monologue(steps)
        return steps, "dspy_hindsight_llm"
    except Exception as llm_exc:
        logger.warning(
            "LLM synthesis failed for %s (%s); falling back to deterministic AST + compiler trajectory compiler.",
            rfc_id,
            llm_exc,
        )
        return compile_deterministic_reasoning_steps(trajectory_data), "deterministic_ast_compiler"


def _build_sft_and_dpo_records(
    trajectory_data: Dict[str, Any],
    thinking_block: str,
) -> Tuple[List[Dict[str, str]], List[DPOContrastivePair]]:
    """Constructs the 3-turn SFT chat payload and extracts any compiler-rejected DPO contrastive pairs."""
    rfc_meta = trajectory_data.get("rfc_metadata", {})
    rfc_id = rfc_meta.get("rfc_id", "Unknown RFC")
    rfc_title = rfc_meta.get("rfc_title", "Unknown Protocol")
    verbatim_slice = rfc_meta.get("verbatim_rfc_slice", "")

    final_out = trajectory_data.get("final_verified_output", {})
    final_scm = (
        final_out.get("final_scm_with_header")
        or trajectory_data.get("stage2_initial_extraction", {}).get("initial_scm")
        or ""
    ).strip()

    user_message = (
        f"Synthesize a formally verified MITRE CPSA 4.4.9 specification for {rfc_id} ({rfc_title}) "
        f"from the following verbatim RFC specification sections:\n\n{verbatim_slice}"
    )
    chosen_completion = f"{thinking_block}\n\n{final_scm}"

    prompt_messages = [
        {"role": "system", "content": SFT_SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
    sft_messages = prompt_messages + [
        {"role": "assistant", "content": chosen_completion},
    ]

    dpo_pairs: List[DPOContrastivePair] = []
    for stage_key, stage_label in (
        ("stage5_preflight_gate", "stage5_roletran"),
        ("stage6_cpsa4_solver", "stage6_cpsa4"),
    ):
        stage_obj = trajectory_data.get(stage_key, {})
        for att in stage_obj.get("repair_attempts", []):
            rejected_scm = (att.get("rejected_scm") or "").strip()
            if not rejected_scm or rejected_scm == final_scm:
                continue
            diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or "Compiler verification failure"
            dpo_pairs.append(
                DPOContrastivePair(
                    stage=stage_label,
                    attempt_number=int(att.get("attempt_number", 1)),
                    compiler_diagnostic=diag,
                    rag_query=att.get("rag_query"),
                    retrieved_chunk_ids=list(att.get("retrieved_chunk_ids", [])),
                    prompt_messages=prompt_messages,
                    chosen_response=chosen_completion,
                    rejected_response=rejected_scm,
                )
            )

    return sft_messages, dpo_pairs


def update_metadata_index_with_think_file(
    run_root_dir: Path,
    trajectory_json_path: Path,
    think_json_path: Path,
) -> Optional[Path]:
    """Updates `metadata_index.json` in `run_root_dir` to register the generated `<protocol>_think.json`."""
    index_path = run_root_dir / "metadata_index.json"
    if not index_path.exists():
        return None

    try:
        index_data = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    index_data["updated_at_utc"] = now_utc

    if "think_json_files" not in index_data:
        index_data["think_json_files"] = []

    think_abs = str(think_json_path.resolve())
    traj_abs = str(trajectory_json_path.resolve())

    if think_abs not in index_data["think_json_files"]:
        index_data["think_json_files"].append(think_abs)

    for run_entry in index_data.get("runs", []):
        if run_entry.get("metadata_json_file") == traj_abs:
            run_entry["think_json_file"] = think_abs

    index_path.write_text(json.dumps(index_data, indent=2), encoding="utf-8")
    return index_path


def generate_think_for_trajectory(
    trajectory_json_path: Path,
    model: Optional[str] = None,
    mode: str = "auto",
    run_root_dir: Optional[Path] = None,
) -> Path:
    """Reads `<protocol>_trajectory.json`, synthesizes `<think>` tokens, writes `<protocol>_think.json`
    in the same RFC directory, and updates `metadata_index.json` if present.
    """
    trajectory_json_path = trajectory_json_path.resolve()
    if not trajectory_json_path.exists():
        raise FileNotFoundError(f"Trajectory JSON not found: {trajectory_json_path}")

    trajectory_data = json.loads(trajectory_json_path.read_text(encoding="utf-8"))
    rfc_dir = trajectory_json_path.parent
    stem = re.sub(r"_trajectory$", "", trajectory_json_path.stem)
    think_json_path = rfc_dir / f"{stem}_think.json"
    scm_filename = f"{stem}.scm"

    if mode == "deterministic":
        reasoning_steps = compile_deterministic_reasoning_steps(trajectory_data)
        synthesis_mode = "deterministic_ast_compiler"
    else:
        reasoning_steps, synthesis_mode = synthesize_reasoning_steps_via_dspy_or_llm(
            trajectory_data=trajectory_data,
            model=model,
        )

    thinking_block = f"<think>\n{reasoning_steps.full_thinking_monologue.strip()}\n</think>"
    sft_messages, dpo_pairs = _build_sft_and_dpo_records(trajectory_data, thinking_block)

    rfc_meta = trajectory_data.get("rfc_metadata", {})
    quality_tier = trajectory_data.get("quality_assessment", {}).get("quality_tier", "REJECTED")
    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    bundle = ThinkArtifactBundle(
        schema_version="1.0.0",
        run_id=trajectory_data.get("run_id", f"{stem}_{now_utc}"),
        timestamp_utc=now_utc,
        rfc_id=rfc_meta.get("rfc_id", "Unknown RFC"),
        rfc_title=rfc_meta.get("rfc_title", "Unknown Protocol"),
        protocol_name=rfc_meta.get("protocol_name", stem),
        algebra=rfc_meta.get("algebra", "basic"),
        quality_tier=quality_tier,
        synthesis_mode=synthesis_mode,
        source_trajectory_file=trajectory_json_path.name,
        target_scm_file=scm_filename,
        reasoning_steps=reasoning_steps,
        thinking_block=thinking_block,
        sft_messages=sft_messages,
        dpo_contrastive_pairs=dpo_pairs,
    )

    think_json_path.write_text(
        json.dumps(bundle.model_dump(), indent=2),
        encoding="utf-8",
    )
    logger.info(
        "Wrote <think> artifact (%s, mode=%s, dpo_pairs=%d) to %s",
        quality_tier,
        synthesis_mode,
        len(dpo_pairs),
        think_json_path,
    )

    effective_run_root = run_root_dir or rfc_dir.parent
    update_metadata_index_with_think_file(
        run_root_dir=effective_run_root,
        trajectory_json_path=trajectory_json_path,
        think_json_path=think_json_path,
    )
    return think_json_path


def process_run_directory(
    target_path: Path,
    model: Optional[str] = None,
    mode: str = "auto",
    min_tier: str = "BRONZE",
    export_jsonl: bool = True,
) -> List[Path]:
    """Processes a timestamped run directory (via `metadata_index.json`), an RFC directory,
    or a single `<protocol>_trajectory.json` file, generating `<protocol>_think.json` files
    and optional consolidated `sft_train.jsonl` / `dpo_pairs.jsonl` datasets.
    """
    target_path = target_path.resolve()
    min_rank = TIER_RANK.get(min_tier.upper(), 2)
    trajectory_files: List[Path] = []
    run_root_dir: Optional[Path] = None

    if target_path.is_file():
        if target_path.name == "metadata_index.json":
            run_root_dir = target_path.parent
            idx_data = json.loads(target_path.read_text(encoding="utf-8"))
            trajectory_files = [Path(p) for p in idx_data.get("metadata_json_files", []) if Path(p).exists()]
        elif target_path.name.endswith("_trajectory.json"):
            trajectory_files = [target_path]
            run_root_dir = target_path.parent.parent
        else:
            raise ValueError(f"Unsupported file target: {target_path}. Provide a *_trajectory.json or metadata_index.json.")
    elif target_path.is_dir():
        index_candidate = target_path / "metadata_index.json"
        if index_candidate.exists():
            run_root_dir = target_path
            idx_data = json.loads(index_candidate.read_text(encoding="utf-8"))
            trajectory_files = [Path(p) for p in idx_data.get("metadata_json_files", []) if Path(p).exists()]
        else:
            trajectory_files = sorted(target_path.rglob("*_trajectory.json"))
            run_root_dir = target_path
    else:
        raise FileNotFoundError(f"Target path does not exist: {target_path}")

    generated_think_files: List[Path] = []
    sft_records: List[Dict[str, Any]] = []
    dpo_records: List[Dict[str, Any]] = []

    for traj_path in trajectory_files:
        try:
            traj_data = json.loads(traj_path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("Skipping unreadable trajectory file %s: %s", traj_path, exc)
            continue

        tier = traj_data.get("quality_assessment", {}).get("quality_tier", "REJECTED")
        if TIER_RANK.get(tier.upper(), 0) < min_rank:
            logger.info("Skipping %s (quality_tier=%s < min_tier=%s)", traj_path.name, tier, min_tier)
            continue

        think_path = generate_think_for_trajectory(
            trajectory_json_path=traj_path,
            model=model,
            mode=mode,
            run_root_dir=run_root_dir,
        )
        generated_think_files.append(think_path)

        think_data = json.loads(think_path.read_text(encoding="utf-8"))
        sft_records.append({
            "run_id": think_data["run_id"],
            "rfc_id": think_data["rfc_id"],
            "protocol_name": think_data["protocol_name"],
            "algebra": think_data["algebra"],
            "quality_tier": think_data["quality_tier"],
            "messages": think_data["sft_messages"],
        })
        for pair in think_data.get("dpo_contrastive_pairs", []):
            dpo_records.append({
                "run_id": think_data["run_id"],
                "rfc_id": think_data["rfc_id"],
                "protocol_name": think_data["protocol_name"],
                "quality_tier": think_data["quality_tier"],
                **pair,
            })

    if export_jsonl and run_root_dir and generated_think_files:
        sft_jsonl_path = run_root_dir / "sft_train.jsonl"
        with open(sft_jsonl_path, "w", encoding="utf-8") as sft_f:
            for rec in sft_records:
                sft_f.write(json.dumps(rec) + "\n")
        logger.info("Exported %d SFT records to %s", len(sft_records), sft_jsonl_path)

        if dpo_records:
            dpo_jsonl_path = run_root_dir / "dpo_pairs.jsonl"
            with open(dpo_jsonl_path, "w", encoding="utf-8") as dpo_f:
                for rec in dpo_records:
                    dpo_f.write(json.dumps(rec) + "\n")
            logger.info("Exported %d DPO contrastive pairs to %s", len(dpo_records), dpo_jsonl_path)

    return generated_think_files
```

---

### `src/generate_think/think_schema.py`

*sha256:`bd1ebe2938b4` · 112 lines · 5.5 KB (~1,403 tokens) · lang:`python`*

```python
"""Pydantic Schemas for Phase 3 Hindsight Reasoning (<think>) Synthesis and SFT/DPO Curation."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SynthesizedReasoningSteps(BaseModel):
    """Structured 5-phase hindsight reasoning steps with compiler-feedback backtracking."""

    step1_protocol_and_algebra: str = Field(
        ...,
        description=(
            "First-person deduction of the protocol scope, participating principals, "
            "and why 'basic' or 'diffie-hellman' message algebra is required by the RFC text."
        ),
    )
    step2_principals_and_variables: str = Field(
        ...,
        description=(
            "First-person mapping of RFC message fields to CPSA variable identifiers and sorts "
            "(name, text, data, skey, akey, rndx, expt, chan, locn, mesg), justifying sort rules."
        ),
    )
    step3_message_flow_and_terms: str = Field(
        ...,
        description=(
            "Step-by-step derivation of each role's ordered trace events (send/recv/load/stor) "
            "and nested S-expression cryptographic terms (cat, enc, hash, pubk, privk, invk, ltk, exp, gen)."
        ),
    )
    step4_compiler_backtracking_and_invariants: str = Field(
        ...,
        description=(
            "Explicit self-correction, backtracking ('Wait—let me check...'), and formal verification "
            "of CPSA 4.4.9 compiler invariants: cpsa4roletran term destructibility, inputs/outputs "
            "disjointness from uniq-orig/uniq-gen, Equation 10.1 encryption key sort rules, and "
            "avoidance/resolution of any Stage 5 or Stage 6 compiler diagnostics."
        ),
    )
    step5_preskeleton_verdicts_and_goals: str = Field(
        ...,
        description=(
            "Derivation of the 3-Point-of-View defskeleton blocks: why participant POV skeletons "
            "omit deflistener to realize multi-strand authentication shapes, and how the secrecy "
            "skeleton uses deflistener alongside non-orig/uniq-orig/uniq-gen assumptions."
        ),
    )
    full_thinking_monologue: str = Field(
        ...,
        description=(
            "Cohesive, natural first-person reasoning monologue integrating Steps 1-5 (including "
            "backtracking and compiler invariant checks) without <think> wrapper tags. Never mention "
            "that a ground-truth AST or .scm was provided in advance."
        ),
    )


class DPOContrastivePair(BaseModel):
    """Compiler-verified Direct Preference Optimization (DPO) contrastive pair."""

    stage: str = Field(..., description="Verification stage where rejection occurred ('stage5_roletran' or 'stage6_cpsa4')")
    attempt_number: int = Field(..., description="1-based repair attempt index")
    compiler_diagnostic: str = Field(..., description="Exact compiler or solver error diagnostic that rejected the candidate")
    rag_query: Optional[str] = Field(default=None, description="RAG query used to retrieve MITRE CPSA manual guidance")
    retrieved_chunk_ids: List[int] = Field(default_factory=list, description="MITRE CPSA manual chunk IDs retrieved")
    prompt_messages: List[Dict[str, str]] = Field(
        ...,
        description="Input conversation messages ([system, user]) shared by chosen and rejected completions",
    )
    chosen_response: str = Field(
        ...,
        description="Verified completion containing <think>...</think> followed by the final verified .scm code",
    )
    rejected_response: str = Field(
        ...,
        description="Compiler-rejected .scm specification from this failed attempt",
    )


class ThinkArtifactBundle(BaseModel):
    """Complete `<protocol>_think.json` artifact saved alongside `<protocol>_trajectory.json`."""

    schema_version: str = Field(default="1.0.0", description="Schema version for <protocol>_think.json")
    run_id: str = Field(..., description="Run identifier matching <protocol>_trajectory.json")
    timestamp_utc: str = Field(..., description="UTC ISO-8601 timestamp when thinking tokens were synthesized")
    rfc_id: str = Field(..., description="RFC identifier (e.g. 'RFC 9528')")
    rfc_title: str = Field(..., description="RFC document title")
    protocol_name: str = Field(..., description="Synthesized CPSA protocol name")
    algebra: str = Field(..., description="CPSA message algebra ('basic' or 'diffie-hellman')")
    quality_tier: str = Field(..., description="Programmatic verification quality tier (GOLD, SILVER, BRONZE, REJECTED)")
    synthesis_mode: str = Field(
        ...,
        description="Method used to synthesize thinking tokens ('dspy_hindsight_llm' or 'deterministic_ast_compiler')",
    )
    source_trajectory_file: str = Field(..., description="Filename of the source <protocol>_trajectory.json")
    target_scm_file: str = Field(..., description="Filename of the target <protocol>.scm")
    reasoning_steps: SynthesizedReasoningSteps = Field(
        ...,
        description="Structured 5-step reasoning breakdown and full monologue",
    )
    thinking_block: str = Field(
        ...,
        description="Complete <think>\\n...\\n</think> block ready for SFT injection",
    )
    sft_messages: List[Dict[str, str]] = Field(
        ...,
        description="Ready-to-train 3-turn chat messages ([system, user, assistant]) where assistant combines <think> + .scm",
    )
    dpo_contrastive_pairs: List[DPOContrastivePair] = Field(
        default_factory=list,
        description="Contrastive (chosen vs. compiler-rejected) pairs extracted from Stage 5 and Stage 6 repair attempts",
    )
```

---

### `src/intermediate_representation/__init__.py`

*sha256:`c3058f848b2c` · 73 lines · 1.9 KB (~493 tokens) · lang:`python`*

```python
"""Intermediate Representation (IR) package for MITRE CPSA 4.4.9 formal specifications."""

from src.intermediate_representation.algebraic_sorts import (
    CPSA_ALL_VARIABLE_SORTS,
    CPSA_BASIC_VALUE_SORTS,
    CPSA_BASIC_VARIABLE_SORTS,
    CPSA_DH_ONLY_VARIABLE_SORTS,
    CPSA_LOGIC_ONLY_SORTS,
    CPSASortEnum,
)
from src.intermediate_representation.cpsa_grammar import (
    CPSA_ALGEBRAS,
    CPSA_ALL_OPERATORS,
    CPSA_BASIC_OPERATORS,
    CPSA_DH_OPERATORS,
    CPSA_OPERATOR_ARITY,
    CPSA_ROLE_KEYWORDS,
    CPSA_ROLE_ONLY_KEYWORDS,
    CPSA_SHARED_DECLARATION_KEYWORDS,
    CPSA_SKELETON_KEYWORDS,
    CPSA_SKELETON_ONLY_KEYWORDS,
    CPSA_TOP_LEVEL_KEYWORDS,
    CPSA_TRACE_ACTIONS,
    CPSA_TRACE_ANNOTATIONS,
    CPSAMessageAlgebra,
    desugar_term_tree,
    validate_cpsa_term_syntax,
)
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAPreskeleton,
    CPSAProtocolRole,
    CPSAProtocolSpecification,
    CPSAStrandInstance,
    CPSATerm,
    CPSATraceEvent,
    CPSAVariableDeclaration,
    normalize_cpsa_term,
    sanitize_cpsa_symbol,
)

__all__ = [
    "CPSASortEnum",
    "CPSA_BASIC_VARIABLE_SORTS",
    "CPSA_DH_ONLY_VARIABLE_SORTS",
    "CPSA_ALL_VARIABLE_SORTS",
    "CPSA_LOGIC_ONLY_SORTS",
    "CPSA_BASIC_VALUE_SORTS",
    "CPSAMessageAlgebra",
    "CPSA_TOP_LEVEL_KEYWORDS",
    "CPSA_ALGEBRAS",
    "CPSA_SHARED_DECLARATION_KEYWORDS",
    "CPSA_ROLE_ONLY_KEYWORDS",
    "CPSA_ROLE_KEYWORDS",
    "CPSA_SKELETON_ONLY_KEYWORDS",
    "CPSA_SKELETON_KEYWORDS",
    "CPSA_TRACE_ACTIONS",
    "CPSA_TRACE_ANNOTATIONS",
    "CPSA_BASIC_OPERATORS",
    "CPSA_DH_OPERATORS",
    "CPSA_ALL_OPERATORS",
    "CPSA_OPERATOR_ARITY",
    "desugar_term_tree",
    "validate_cpsa_term_syntax",
    "CPSATerm",
    "CPSAVariableDeclaration",
    "CPSATraceEvent",
    "CPSAProtocolRole",
    "CPSAStrandInstance",
    "CPSAPreskeleton",
    "CPSAProtocolSpecification",
    "sanitize_cpsa_symbol",
    "normalize_cpsa_term",
]
```

---

### `src/intermediate_representation/algebraic_sorts.py`

*sha256:`19264144bc10` · 78 lines · 3.0 KB (~764 tokens) · lang:`python`*

```python
"""Order-Sorted Message Algebra Sort Definitions for MITRE CPSA 4.4.9.

Grounded directly in MITRE CPSA 4.4.9 User Manual Tables 7.1, 10.2, 10.4, and 10.6,
and CPSA4 Roletran (`Role_Translations.md` Section 2).
"""

from enum import Enum
from typing import Set


class CPSASortEnum(str, Enum):
    """Supported sorts in MITRE CPSA 4.4.9 order-sorted algebras and logic rules."""

    # Basic Message Algebra Sorts (Table 10.2)
    NAME = "name"      # Principal identifiers (required by pubk, privk, ltk, bltk)
    TEXT = "text"      # Fresh nonces and plain text tokens
    DATA = "data"      # Arbitrary payload / secrets
    TAG = "tag"        # Constant tag atoms
    SKEY = "skey"      # Symmetric encryption keys
    AKEY = "akey"      # Asymmetric keys (public or private)
    DEV = "dev"        # Hardware device identifiers
    CHAN = "chan"      # Communication channels (required by cpsa4roletran)
    LOCN = "locn"      # State memory locations (load / stor events)
    MESG = "mesg"      # Universal top sort (cannot be an encryption key per Eq. 10.1)

    # Diffie-Hellman Message Algebra Sorts (Table 10.4)
    RNDX = "rndx"      # Atomic random exponents (must be uniq-gen, never uniq-orig)
    EXPT = "expt"      # Compound exponent expressions (rndx < expt < mesg)
    BASE = "base"      # Diffie-Hellman group base elements

    # First-Order Logic & Goal Sorts (Table 7.1 — forbidden in role/skeleton vars)
    FACT = "fact"      # User-defined relational facts
    STRD = "strd"      # Strand variable sort in defrule/defgoal quantifiers
    INDX = "indx"      # Node index sort in defrule/defgoal quantifiers


# Sorts permitted inside (vars ...) of defrole and defskeleton under 'basic' algebra (Table 10.2)
CPSA_BASIC_VARIABLE_SORTS: Set[str] = {
    CPSASortEnum.NAME.value,
    CPSASortEnum.TEXT.value,
    CPSASortEnum.DATA.value,
    CPSASortEnum.TAG.value,
    CPSASortEnum.SKEY.value,
    CPSASortEnum.AKEY.value,
    CPSASortEnum.DEV.value,
    CPSASortEnum.CHAN.value,
    CPSASortEnum.LOCN.value,
    CPSASortEnum.MESG.value,
}

# Additional sorts permitted inside (vars ...) only under 'diffie-hellman' algebra (Table 10.4)
CPSA_DH_ONLY_VARIABLE_SORTS: Set[str] = {
    CPSASortEnum.RNDX.value,
    CPSASortEnum.EXPT.value,
    CPSASortEnum.BASE.value,
}

# Complete set of sorts permitted in (vars ...) declarations of defrole and defskeleton
CPSA_ALL_VARIABLE_SORTS: Set[str] = CPSA_BASIC_VARIABLE_SORTS | CPSA_DH_ONLY_VARIABLE_SORTS

# First-order logic sorts restricted exclusively to defrule / defgoal quantifiers (Table 7.1)
CPSA_LOGIC_ONLY_SORTS: Set[str] = {
    CPSASortEnum.FACT.value,
    CPSASortEnum.STRD.value,
    CPSASortEnum.INDX.value,
}

# Basic Value sorts (BV_X) permitted in cpsa4roletran (inputs ...) declarations alongside channels
CPSA_BASIC_VALUE_SORTS: Set[str] = {
    CPSASortEnum.NAME.value,
    CPSASortEnum.TEXT.value,
    CPSASortEnum.DATA.value,
    CPSASortEnum.TAG.value,
    CPSASortEnum.SKEY.value,
    CPSASortEnum.AKEY.value,
    CPSASortEnum.DEV.value,
    CPSASortEnum.LOCN.value,
}
```

---

### `src/intermediate_representation/cpsa_grammar.py`

*sha256:`90cc41d7d8cc` · 399 lines · 14.0 KB (~3,586 tokens) · lang:`python`*

```python
"""MITRE CPSA 4.4.9 Formal Grammar, Scoped Keywords, and Arity Specifications.

Derived directly from the authoritative MITRE CPSA 4.4.9 User Manual:
- Chapters 2, 3, 4, 7, 10 (Tables 7.1, 10.1 – 10.6, Equation 10.1)
- CPSA4 Roletran Specification (`cpsa4roletran.md` & `Role_Translations.md`)

Enforces strict syntactic and positional scoping so every CPSA keyword, sort,
and operator can only appear in the exact grammatical production where the
MITRE CPSA 4.4.9 specification allows it.
"""

from typing import Any, Dict, Literal, Optional, Set, Tuple, Union, get_args


# =============================================================================
# STAGE 1: Top-Level Scheme S-Expression Forms (Table 10.1)
# =============================================================================
CPSATopLevelKeyword = Literal[
    "herald",
    "defprotocol",
    "defskeleton",
    "defmacro",
    "defrule",
    "defgenrule",
    "defgoal",
    "deflemma",
    "comment",
]
CPSA_TOP_LEVEL_KEYWORDS: Set[str] = set(get_args(CPSATopLevelKeyword))


# =============================================================================
# STAGE 2: Cryptographic Message Algebras (Tables 10.2 & 10.4)
# =============================================================================
CPSAMessageAlgebra = Literal[
    "basic",
    "diffie-hellman",
]
CPSA_ALGEBRAS: Set[str] = set(get_args(CPSAMessageAlgebra))


# =============================================================================
# STAGE 3: Scoped Declaration Keywords (Table 10.1, Table 10.6 & Roletran)
# =============================================================================

# Declaration keywords valid in BOTH defrole and defskeleton (Table 10.6)
CPSASharedDeclarationKeyword = Literal[
    "vars",
    "non-orig",
    "pen-non-orig",
    "uniq-orig",
    "uniq-gen",
    "conf",
    "auth",
    "gen-st",
    "priority",
    "facts",
    "comment",
]
CPSA_SHARED_DECLARATION_KEYWORDS: Set[str] = set(get_args(CPSASharedDeclarationKeyword))

# Keywords valid EXCLUSIVELY inside defrole (Table 10.1, Table 10.6, cpsa4roletran)
CPSARoleOnlyKeyword = Literal[
    "defrole",
    "trace",
    "inputs",
    "outputs",
    "params",
    "returns",
    "assume",
    "ind-zero",
]
CPSA_ROLE_ONLY_KEYWORDS: Set[str] = set(get_args(CPSARoleOnlyKeyword))

# Complete set of authorized keywords inside a (defrole ...) form
CPSARoleKeyword = Literal[
    "defrole",
    "vars",
    "trace",
    "inputs",
    "outputs",
    "params",
    "returns",
    "non-orig",
    "pen-non-orig",
    "uniq-orig",
    "uniq-gen",
    "conf",
    "auth",
    "gen-st",
    "priority",
    "facts",
    "assume",
    "ind-zero",
    "comment",
]
CPSA_ROLE_KEYWORDS: Set[str] = set(get_args(CPSARoleKeyword))

# Keywords valid EXCLUSIVELY inside defskeleton (Table 10.1 & Table 10.6)
CPSASkeletonOnlyKeyword = Literal[
    "defskeleton",
    "defstrand",
    "defstrandmax",
    "deflistener",
    "precedes",
    "leadsto",
    "goal",
    "goals",
]
CPSA_SKELETON_ONLY_KEYWORDS: Set[str] = set(get_args(CPSASkeletonOnlyKeyword))

# Complete set of authorized keywords inside a (defskeleton ...) form
CPSASkeletonKeyword = Literal[
    "defskeleton",
    "vars",
    "defstrand",
    "defstrandmax",
    "deflistener",
    "non-orig",
    "pen-non-orig",
    "uniq-orig",
    "uniq-gen",
    "conf",
    "auth",
    "gen-st",
    "precedes",
    "leadsto",
    "priority",
    "facts",
    "goal",
    "goals",
    "comment",
]
CPSA_SKELETON_KEYWORDS: Set[str] = set(get_args(CPSASkeletonKeyword))


# =============================================================================
# STAGE 4: Trace Event Actions & Annotations (Section 10.2, Table 10.1)
# =============================================================================
CPSATraceAction = Literal[
    "send",
    "recv",
    "load",
    "stor",
]
CPSA_TRACE_ACTIONS: Set[str] = set(get_args(CPSATraceAction))

CPSATraceAnnotation = Literal[
    "cheq",
    "rely",
    "guarantee",
]
CPSA_TRACE_ANNOTATIONS: Set[str] = set(get_args(CPSATraceAnnotation))


# =============================================================================
# STAGE 5: Message Term Operators (Tables 10.3 & 10.5)
# =============================================================================

# Basic Crypto Algebra Operators (Table 10.3)
CPSABasicOperator = Literal[
    "enc",     # (enc term+ key)             (arity >= 2; key is last arg)
    "hash",    # (hash term+)                (arity >= 1)
    "cat",     # (cat term+)                 (arity >= 1)
    "pubk",    # (pubk name) | (pubk str id) (arity 1 or 2)
    "privk",   # (privk name)| (privk str id)(arity 1 or 2)
    "invk",    # (invk akey_var)             (arity 1)
    "ltk",     # (ltk name1 name2)           (arity 2)
]
CPSA_BASIC_OPERATORS: Set[str] = set(get_args(CPSABasicOperator))

# Diffie-Hellman Crypto Algebra Operators (Table 10.5)
CPSADHOperator = Literal[
    "bltk",    # (bltk name1 name2)          (arity 2)
    "exp",     # (exp base expt)             (arity 2)
    "gen",     # (gen)                       (arity 0)
    "mul",     # (mul expt1 expt2 ...)       (arity >= 2)
    "rec",     # (rec expt)                  (arity 1)
    "one",     # (one)                       (arity 0)
]
CPSA_DH_OPERATORS: Set[str] = set(get_args(CPSADHOperator))

# All Authorized Term Operators
CPSAAllOperator = Literal[
    "enc",
    "hash",
    "cat",
    "pubk",
    "privk",
    "invk",
    "ltk",
    "bltk",
    "exp",
    "gen",
    "mul",
    "rec",
    "one",
]
CPSA_ALL_OPERATORS: Set[str] = set(get_args(CPSAAllOperator))

# Key-constructing operators whose result is a basic value (akey or skey) allowed in roletran inputs
CPSA_KEY_CONSTRUCTOR_OPERATORS: Set[str] = {"pubk", "privk", "invk", "ltk", "bltk"}

# Structural keywords that must NEVER appear as operators inside a message term
CPSA_STRUCTURAL_NON_TERM_KEYWORDS: Set[str] = (
    CPSA_TOP_LEVEL_KEYWORDS
    | CPSA_ROLE_KEYWORDS
    | CPSA_SKELETON_KEYWORDS
    | CPSA_TRACE_ACTIONS
    | CPSA_TRACE_ANNOTATIONS
    | CPSA_ALGEBRAS
)


# =============================================================================
# STAGE 6: Operator Arity Constraints (Tables 10.3 & 10.5)
# =============================================================================
# Format: int (exact), set (one of allowed integers), tuple (min, max or None)
CPSA_OPERATOR_ARITY: Dict[str, Union[int, Set[int], Tuple[int, Optional[int]]]] = {
    "enc": (2, None),       # at least 1 payload + 1 encryption key (last argument)
    "hash": (1, None),      # at least 1 payload term
    "cat": (1, None),       # at least 1 component term
    "pubk": {1, 2},         # (pubk name_id) or (pubk tag_string name_id) per Table 10.3
    "privk": {1, 2},        # (privk name_id) or (privk tag_string name_id) per Table 10.3
    "invk": 1,              # (invk akey_var)
    "ltk": 2,               # (ltk name1 name2)
    "bltk": 2,              # (bltk name1 name2)
    "exp": 2,               # (exp base expt)
    "gen": 0,               # (gen)
    "mul": (2, None),       # at least 2 exponent factors
    "rec": 1,               # (rec expt)
    "one": 0,               # (one)
}


# =============================================================================
# STAGE 7: JSON Schema Specification for Strongly-Typed Term AST
# =============================================================================
CPSA_TERM_JSON_SCHEMA: Dict[str, Any] = {
    "title": "CPSATerm",
    "description": (
        "A CPSA 4.4.9 message term: an identifier atom string (e.g. client_random, K_ab), "
        "a quoted constant tag literal (e.g. '\"tag_v1\"'), or a prefix S-expression list [operator, ...args] where operator "
        "is strictly one of: enc, hash, cat, pubk, privk, invk, ltk, bltk, exp, gen, mul, rec, one."
    ),
    "anyOf": [
        {"type": "string", "description": "Declared variable identifier or constant tag string"},
        {
            "type": "array",
            "description": "Prefix operator expression: [operator, ...subterms]",
            "items": {
                "anyOf": [
                    {
                        "type": "string",
                        "enum": sorted(list(CPSA_ALL_OPERATORS)),
                        "description": "Leading CPSA 4.4.9 operator keyword",
                    },
                    {"type": "string", "description": "Subterm variable or constant tag string"},
                    {"type": "array", "description": "Nested subterm expression"},
                ]
            },
            "minItems": 1,
        },
    ],
}


# =============================================================================
# STAGE 8: Canonical Desugaring Mappings (Frontend Compiler Normalizer)
# =============================================================================
# Maps foreign cryptographic operators (from ProVerif, Tamarin, or LLM hallucinations)
# to their canonical MITRE CPSA 4.4.9 equivalents.
CPSA_DESUGAR_MAP: Dict[str, str] = {
    "aenc": "enc",
    "senc": "enc",
    "asym_enc": "enc",
    "sym_enc": "enc",
    "sign": "enc",
    "mac": "hash",
    "hmac": "hash",
}


def desugar_term_tree(term: Any) -> Any:
    """Recursively desugars foreign/hallucinated crypto operators and dictionary nodes to canonical CPSA primitives."""
    if isinstance(term, list):
        if not term:
            return term
        normalized_list = list(term)
        operator = normalized_list[0]
        if isinstance(operator, str) and operator in CPSA_DESUGAR_MAP:
            normalized_list[0] = CPSA_DESUGAR_MAP[operator]
        return [desugar_term_tree(subterm) for subterm in normalized_list]

    if isinstance(term, int) and not isinstance(term, bool):
        return f'"{term}"'

    if isinstance(term, dict):
        # Extract atomic identifier name from dictionary variable representation
        for key in ("name", "variable", "identifier", "var", "id", "atom", "field", "val", "value"):
            if key in term and isinstance(term[key], (str, int)):
                val = term[key]
                return f'"{val}"' if isinstance(val, int) and not isinstance(val, bool) else val
        if "term" in term:
            return desugar_term_tree(term["term"])
        if "args" in term and isinstance(term.get("op"), str):
            return desugar_term_tree([term["op"]] + term["args"])
        for val in term.values():
            if isinstance(val, str):
                return val

    return term


def validate_cpsa_term_syntax(
    term: Any,
    algebra: CPSAMessageAlgebra = "basic",
    path: str = "term",
) -> None:
    """Statically validates that a term tree conforms strictly to MITRE CPSA 4.4.9 grammar.

    Enforces:
    1. Rejection of structural keywords (defrole, defskeleton, send, recv, vars, etc.) inside terms.
    2. Operator existence in the authorized CPSA 4.4.9 signature (Tables 10.3 & 10.5).
    3. Message algebra compatibility (forbidding DH operators under 'basic' algebra).
    4. Strict operator arity matching Tables 10.3 & 10.5.
    5. Inductive validation of all subterms.

    Raises:
        ValueError: If an unrecognized keyword, structural keyword leak, algebra incompatibility,
                    or arity defect is found.
    """
    if isinstance(term, (str, int)):
        return

    if isinstance(term, list):
        if not term:
            raise ValueError(f"Empty term expression at '{path}'. Expected atom or operator form.")

        operator = term[0]
        if not isinstance(operator, str):
            raise ValueError(
                f"First element of expression at '{path}' must be an operator string, got {type(operator).__name__}."
            )

        # 1. Check for misplaced structural CPSA keywords inside message terms
        if operator in CPSA_STRUCTURAL_NON_TERM_KEYWORDS and operator not in CPSA_ALL_OPERATORS:
            raise ValueError(
                f"Structural CPSA keyword '{operator}' at '{path}' cannot be used as a message term operator. "
                f"Valid CPSA 4.4.9 term operators: {sorted(list(CPSA_ALL_OPERATORS))}"
            )

        # 2. Operator Keyword Authorization
        if operator not in CPSA_ALL_OPERATORS:
            raise ValueError(
                f"Unknown operator keyword '{operator}' at '{path}'. "
                f"Valid CPSA 4.4.9 operators: {sorted(list(CPSA_ALL_OPERATORS))}"
            )

        # 3. Algebra Compatibility Check
        if algebra == "basic" and operator in CPSA_DH_OPERATORS:
            raise ValueError(
                f"Diffie-Hellman operator '{operator}' at '{path}' is forbidden under 'basic' message algebra. "
                "Change protocol message_algebra to 'diffie-hellman' to use exponentiation/DH features."
            )

        # 4. Arity Validation
        arguments = term[1:]
        arity = len(arguments)
        expected_arity = CPSA_OPERATOR_ARITY.get(operator)

        if isinstance(expected_arity, int):
            if arity != expected_arity:
                raise ValueError(
                    f"Operator '{operator}' at '{path}' expects exactly {expected_arity} arguments, got {arity}: {term}"
                )
        elif isinstance(expected_arity, set):
            if arity not in expected_arity:
                raise ValueError(
                    f"Operator '{operator}' at '{path}' expects arity in {sorted(list(expected_arity))}, got {arity}: {term}"
                )
        elif isinstance(expected_arity, tuple):
            min_args, max_args = expected_arity
            if arity < min_args:
                raise ValueError(
                    f"Operator '{operator}' at '{path}' expects at least {min_args} arguments, got {arity}: {term}"
                )
            if max_args is not None and arity > max_args:
                raise ValueError(
                    f"Operator '{operator}' at '{path}' expects at most {max_args} arguments, got {arity}: {term}"
                )

        # 5. Inductive Recursive Subterm Validation
        for idx, subterm in enumerate(arguments, 1):
            validate_cpsa_term_syntax(subterm, algebra=algebra, path=f"{path}[{idx}]")
    else:
        raise ValueError(
            f"Invalid term node at '{path}'. Expected string atom, integer, or nested operator list, got {type(term).__name__}."
        )
```

---

### `src/intermediate_representation/protocol_syntax_tree.py`

*sha256:`26d26dec0630` · 1252 lines · 55.1 KB (~14,110 tokens) · lang:`python`*

```python
"""Strongly-Typed Intermediate Representation (AST) for MITRE CPSA 4.4.9 Protocols.

Enforces strict syntactic, algebraic, and positional keyword scoping across all
CPSA 4.4.9 constructs (Tables 10.1 – 10.6, Equation 10.1, and CPSA4 Roletran).
"""

import re
from typing import Annotated, Any, Dict, List, Optional, Set, Union
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    Field,
    WithJsonSchema,
    field_validator,
    model_validator,
)

from src.intermediate_representation.algebraic_sorts import (
    CPSA_ALL_VARIABLE_SORTS,
    CPSA_DH_ONLY_VARIABLE_SORTS,
    CPSA_LOGIC_ONLY_SORTS,
    CPSASortEnum,
)
from src.intermediate_representation.cpsa_grammar import (
    CPSA_ALL_OPERATORS,
    CPSA_KEY_CONSTRUCTOR_OPERATORS,
    CPSA_ROLE_ONLY_KEYWORDS,
    CPSA_SKELETON_ONLY_KEYWORDS,
    CPSA_TERM_JSON_SCHEMA,
    CPSAMessageAlgebra,
    CPSATraceAction,
    desugar_term_tree,
    validate_cpsa_term_syntax,
)


def _validate_cpsa_term(value: Any) -> Any:
    validate_cpsa_term_syntax(value, algebra="diffie-hellman")
    return value


# Strongly-typed CPSA term AST: enforces canonical syntax, algebra compatibility,
# and operator arity while providing an explicit enum/grammar JSON schema to LLMs.
CPSATerm = Annotated[
    Union[str, int, List[Any]],
    BeforeValidator(desugar_term_tree),
    AfterValidator(_validate_cpsa_term),
    WithJsonSchema(CPSA_TERM_JSON_SCHEMA),
]


# Forbidden misplaced keys per Pydantic model scope (Tables 10.1 & 10.6)
_FORBIDDEN_IN_ROLE: Set[str] = CPSA_SKELETON_ONLY_KEYWORDS | {"strands", "listeners"}
_FORBIDDEN_IN_SKELETON: Set[str] = CPSA_ROLE_ONLY_KEYWORDS | {"role_name"}
_FORBIDDEN_IN_EVENT: Set[str] = (
    CPSA_ROLE_ONLY_KEYWORDS
    | CPSA_SKELETON_ONLY_KEYWORDS
    | {"vars", "variables", "strands", "listeners", "unique_originating", "non_originating"}
) - {"trace"}
_FORBIDDEN_AT_TOP_LEVEL: Set[str] = (
    CPSA_ROLE_ONLY_KEYWORDS
    | CPSA_SKELETON_ONLY_KEYWORDS
    | {"strands", "listeners"}
) - {"defskeleton"}


def sanitize_cpsa_symbol(symbol: str) -> str:
    """Sanitizes an identifier to conform strictly to CPSA S-expression symbol grammar.

    CPSA allows alphanumeric characters and +-*/<=>!?$:%_&~^.
    Periods (.), spaces, and other punctuation are forbidden in unquoted atoms.
    """
    if not symbol:
        return "prot"
    sanitized = re.sub(r"[\.\s]+", "-", symbol)
    sanitized = re.sub(r"[^a-zA-Z0-9+\-*/<=>!?$:%_&~^]", "", sanitized)
    return sanitized.strip("-") or "prot"


def _quote_cpsa_tag_literal(val: str) -> str:
    """Formats an undeclared constant atom or number as a quoted CPSA 4.4.9 tag literal."""
    inner = val.strip()
    if len(inner) >= 2 and inner.startswith('"') and inner.endswith('"'):
        inner = inner[1:-1]
    inner = inner.replace("\\", "/").replace('"', "'")
    return f'"{inner}"'


def _is_quoted_tag_literal(term: Any) -> bool:
    """Returns True if `term` is a quoted CPSA string tag literal (`\"...\"`)."""
    return isinstance(term, str) and len(term) >= 2 and term.startswith('"') and term.endswith('"')


def _collect_implied_variable_sorts(
    term: Any,
    implied_sorts: Dict[str, str],
    akey_vars: Set[str],
    name_vars: Set[str],
) -> None:
    """Infers mandatory CPSA 4.4.9 variable sorts from operator positions (e.g. `ltk`/`pubk`/`privk` -> `name`)."""
    desugared = desugar_term_tree(term)
    if not isinstance(desugared, list) or not desugared:
        return
    op = desugared[0]
    if op in ("ltk", "bltk") and len(desugared) == 3:
        for arg in desugared[1:]:
            if isinstance(arg, str) and not _is_quoted_tag_literal(arg) and arg not in CPSA_ALL_OPERATORS:
                implied_sorts.setdefault(arg, CPSASortEnum.NAME.value)
    elif op in ("pubk", "privk"):
        if len(desugared) == 2:
            arg = desugared[1]
            if (
                isinstance(arg, str)
                and not _is_quoted_tag_literal(arg)
                and arg not in akey_vars
                and arg not in CPSA_ALL_OPERATORS
            ):
                implied_sorts.setdefault(arg, CPSASortEnum.NAME.value)
        elif len(desugared) == 3:
            a1, a2 = desugared[1], desugared[2]
            if isinstance(a1, str) and isinstance(a2, str):
                if a1 in name_vars and a2 not in name_vars:
                    pass
                elif not _is_quoted_tag_literal(a2) and a2 not in CPSA_ALL_OPERATORS:
                    implied_sorts.setdefault(a2, CPSASortEnum.NAME.value)
    elif op == "invk" and len(desugared) == 2:
        arg = desugared[1]
        if isinstance(arg, str) and not _is_quoted_tag_literal(arg) and arg not in CPSA_ALL_OPERATORS:
            implied_sorts.setdefault(arg, CPSASortEnum.AKEY.value)
    elif op == "enc" and len(desugared) >= 2:
        key_arg = desugared[-1]
        if isinstance(key_arg, str) and not _is_quoted_tag_literal(key_arg) and key_arg not in CPSA_ALL_OPERATORS:
            implied_sorts.setdefault(key_arg, CPSASortEnum.SKEY.value)

    for sub in desugared[1:]:
        _collect_implied_variable_sorts(sub, implied_sorts, akey_vars, name_vars)


def _invert_cpsa_key(key_term: Any, akey_vars: Set[str]) -> Any:
    """Returns the inverse key term required to decrypt/verify `(enc ... key_term)` in `cpsa4roletran`."""
    if isinstance(key_term, list) and key_term:
        op = key_term[0]
        if op == "pubk":
            return ["privk"] + key_term[1:]
        if op == "privk":
            return ["pubk"] + key_term[1:]
        if op == "invk" and len(key_term) == 2:
            return key_term[1]
        return key_term
    if isinstance(key_term, str) and key_term in akey_vars:
        return ["invk", key_term]
    return key_term


def extract_term_tokens(item: Any, token_set: Set[str]) -> None:
    """Recursively extracts all string tokens from an S-expression tree."""
    if isinstance(item, str):
        token_set.add(item)
    elif isinstance(item, (list, tuple)):
        for subitem in item:
            extract_term_tokens(subitem, token_set)
    elif isinstance(item, dict):
        for subitem in item.values():
            extract_term_tokens(subitem, token_set)


def normalize_cpsa_term(
    term: Any,
    akey_vars: Optional[Set[str]] = None,
    name_vars: Optional[Set[str]] = None,
    declared_vars: Optional[Set[str]] = None,
    quote_undeclared: bool = False,
) -> Any:
    """Recursively validates and normalizes message terms into valid CPSA 4.4.9 forms.

    Handles:
    1. Unwrapping (pubk k) -> k and (privk k) -> (invk k) when k has sort 'akey'.
    2. Repairing reversed 2-arg (pubk name tag) -> (pubk "tag" name) and quoting 2-arg tags per Table 10.3.
    3. Expanding bare 'gen' or 'one' in DH expressions to ['gen'] / ['one'] when not declared as variables.
    4. Auto-quoting undeclared constant atoms/numbers as CPSA string tag literals when `quote_undeclared=True`.
    """
    desugared = desugar_term_tree(term)
    if isinstance(desugared, list):
        if not desugared:
            return desugared
        normalized_list = list(desugared)
        operator = normalized_list[0]

        # 1. 1-argument pubk/privk applied to an 'akey' variable instead of 'name'
        if (
            akey_vars
            and len(normalized_list) == 2
            and isinstance(normalized_list[1], str)
            and (normalized_list[1] in akey_vars or sanitize_cpsa_symbol(normalized_list[1]) in akey_vars)
        ):
            clean_k = sanitize_cpsa_symbol(normalized_list[1]) if quote_undeclared else normalized_list[1]
            if operator == "pubk":
                return clean_k
            if operator == "privk":
                return ["invk", clean_k]

        # 2. 2-argument pubk/privk: Table 10.3 requires (pubk string_tag name_id)
        if (
            operator in ("pubk", "privk")
            and len(normalized_list) == 3
            and isinstance(normalized_list[1], str)
            and isinstance(normalized_list[2], str)
        ):
            first_arg, second_arg = normalized_list[1], normalized_list[2]
            if name_vars and (first_arg in name_vars or sanitize_cpsa_symbol(first_arg) in name_vars) and second_arg not in name_vars:
                tag_str = _quote_cpsa_tag_literal(second_arg)
                clean_name = sanitize_cpsa_symbol(first_arg) if quote_undeclared else first_arg
                return [operator, tag_str, clean_name]
            tag_str = _quote_cpsa_tag_literal(first_arg)
            clean_name = sanitize_cpsa_symbol(second_arg) if quote_undeclared else second_arg
            return [operator, tag_str, clean_name]

        # 3. Bare 'gen' or 'one' inside Diffie-Hellman operators (exp, mul, rec)
        if operator in ("exp", "mul", "rec"):
            for idx in range(1, len(normalized_list)):
                arg = normalized_list[idx]
                if arg == "gen" and (not declared_vars or "gen" not in declared_vars):
                    normalized_list[idx] = ["gen"]
                elif arg == "one" and (not declared_vars or "one" not in declared_vars):
                    normalized_list[idx] = ["one"]

        return [normalized_list[0]] + [
            normalize_cpsa_term(
                subterm,
                akey_vars=akey_vars,
                name_vars=name_vars,
                declared_vars=declared_vars,
                quote_undeclared=quote_undeclared,
            )
            for subterm in normalized_list[1:]
        ]

    if isinstance(desugared, str):
        if _is_quoted_tag_literal(desugared):
            return _quote_cpsa_tag_literal(desugared)
        if quote_undeclared and declared_vars is not None:
            clean_sym = sanitize_cpsa_symbol(desugared)
            if desugared in declared_vars or clean_sym in declared_vars:
                return clean_sym
            if desugared in ("gen", "one"):
                return desugared
            return _quote_cpsa_tag_literal(desugared)
    return desugared


def _validate_no_mesg_encryption_key(term: Any, mesg_vars: Set[str], path: str) -> None:
    """Enforces MITRE CPSA 4.4.9 Equation 10.1: encryption keys in (enc ...) cannot be variables of sort 'mesg'."""
    if not mesg_vars or not isinstance(term, list) or not term:
        return
    operator = term[0]
    if operator == "enc" and len(term) >= 2:
        key_term = term[-1]
        if isinstance(key_term, str) and key_term in mesg_vars:
            raise ValueError(
                f"Variable '{key_term}' of sort 'mesg' at '{path}' cannot be used as an encryption key in (enc ...) "
                "per MITRE CPSA 4.4.9 Equation 10.1 (sort 'mesg' lacks a well-defined key inverse). "
                "Declare the key with sort 'skey' or 'akey'."
            )
    for idx, subterm in enumerate(term[1:], 1):
        _validate_no_mesg_encryption_key(subterm, mesg_vars, f"{path}[{idx}]")


def _is_valid_roletran_input_term(term: Any) -> bool:
    """Checks whether a term is a basic value or channel allowed in cpsa4roletran (inputs ...)."""
    if isinstance(term, str):
        return True
    if isinstance(term, list) and term:
        op = term[0]
        if op in ("pubk", "privk", "invk"):
            return len(term) == 2
        if op in ("ltk", "bltk"):
            return len(term) == 3
    return False


class CPSAVariableDeclaration(BaseModel):
    """Declaration of a typed variable in a role or skeleton (Tables 10.2 & 10.4)."""

    name: str = Field(..., description="Semantic alphanumeric identifier (e.g. client_random, server_identity)")
    sort: CPSASortEnum = Field(..., description="Declared CPSA message algebra sort")
    description: Optional[str] = Field(
        default=None,
        description="Detailed explanation of what this variable represents in the RFC",
    )
    rfc_field: Optional[str] = Field(
        default=None,
        description="Exact RFC field name or section mapping (e.g. ClientHello.random)",
    )

    @field_validator("sort")
    @classmethod
    def validate_variable_sort_scope(cls, sort_val: CPSASortEnum) -> CPSASortEnum:
        """Forbids first-order logic sorts (strd, indx, fact) in role/skeleton (vars ...) declarations."""
        if sort_val.value in CPSA_LOGIC_ONLY_SORTS:
            raise ValueError(
                f"Sort '{sort_val.value}' is a first-order logic sort (Table 7.1) restricted to defrule/defgoal "
                f"quantifiers and is forbidden in role or skeleton (vars ...) declarations (Tables 10.2 & 10.4). "
                f"Valid variable sorts: {sorted(list(CPSA_ALL_VARIABLE_SORTS))}"
            )
        return sort_val

    def to_cpsa_json(self) -> List[str]:
        return [sanitize_cpsa_symbol(self.name), self.sort.value]


class CPSATraceEvent(BaseModel):
    """A directional communication or state event over an optional channel or location (Table 10.1)."""

    direction: CPSATraceAction = Field(..., description="Trace event action: send, recv, load, stor")
    channel: Optional[str] = Field(default="ch", description="Channel variable identifier for send/recv")
    location: Optional[str] = Field(default=None, description="Memory location variable for stateful load/stor events")
    message_term: CPSATerm = Field(
        ...,
        description="Term payload: atom string, integer, or nested operator tree conforming strictly to CPSA 4.4.9 grammar",
    )
    description: Optional[str] = Field(
        default=None,
        description="Semantic description of the message event (e.g. Client sends ClientHello)",
    )

    @model_validator(mode="before")
    @classmethod
    def forbid_non_event_keywords(cls, data: Any) -> Any:
        if isinstance(data, dict):
            misplaced = set(data.keys()) & _FORBIDDEN_IN_EVENT
            if misplaced:
                bad_key = sorted(list(misplaced))[0]
                raise ValueError(
                    f"Keyword '{bad_key}' is not allowed inside CPSATraceEvent (Table 10.1 event <- (dir term? term))."
                )
        return data

    def to_cpsa_json(self) -> List[Any]:
        # Per MITRE CPSA 4.4.9 Table 10.1: event <- (dir term? term)
        # load/stor take an optional location (locn) and a message_term (never both channel and location).
        if self.direction in ("load", "stor"):
            loc_var = self.location or (self.channel if self.channel and self.channel != "ch" else None)
            if loc_var:
                return [self.direction, sanitize_cpsa_symbol(loc_var), self.message_term]
            return [self.direction, self.message_term]

        if self.channel:
            return [self.direction, sanitize_cpsa_symbol(self.channel), self.message_term]
        return [self.direction, self.message_term]


class CPSAProtocolRole(BaseModel):
    """Specification of a principal's behavior in a protocol (defrole, Tables 10.1 & 10.6)."""

    role_name: str = Field(..., description="Identifier for the participant role")
    description: Optional[str] = Field(
        default=None,
        description="Detailed explanation of the principal's role in the protocol",
    )
    variables: List[CPSAVariableDeclaration] = Field(..., description="Variables declared within the role scope")
    trace: List[CPSATraceEvent] = Field(..., description="Ordered sequence of message events")
    inputs: List[CPSATerm] = Field(
        default_factory=list,
        description="Input parameters required for execution (channels, pre-shared keys, initial parameters)",
    )
    outputs: List[CPSATerm] = Field(
        default_factory=list,
        description="Return parameters yielded upon successful execution",
    )
    unique_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Terms originating uniquely in this role (uniq-orig)",
    )
    unique_generated: List[CPSATerm] = Field(
        default_factory=list,
        description="Terms generated uniquely in this role (uniq-gen)",
    )
    non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Keys assumed never compromised/originating in this role (non-orig)",
    )
    pen_non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Penetrator non-originating terms (pen-non-orig)",
    )
    confidential_channels: List[str] = Field(
        default_factory=list,
        description="Channels declared confidential (conf)",
    )
    authenticated_channels: List[str] = Field(
        default_factory=list,
        description="Channels declared authenticated (auth)",
    )
    gen_st: List[CPSATerm] = Field(
        default_factory=list,
        description="Stored state values with authenticity property (gen-st, Table 10.6)",
    )
    facts: List[List[Any]] = Field(
        default_factory=list,
        description="User-defined logical facts asserted by this role",
    )
    comment: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def forbid_skeleton_keywords_in_role(cls, data: Any) -> Any:
        if isinstance(data, dict):
            misplaced = set(data.keys()) & _FORBIDDEN_IN_ROLE
            if misplaced:
                bad_key = sorted(list(misplaced))[0]
                raise ValueError(
                    f"Keyword '{bad_key}' is a preskeleton-only keyword (MITRE CPSA 4.4.9 Tables 10.1 & 10.6) "
                    "and is strictly forbidden inside CPSAProtocolRole (defrole)."
                )
        return data

    @model_validator(mode="after")
    def validate_role_invariants(self) -> "CPSAProtocolRole":
        mesg_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.MESG}
        if mesg_vars:
            for idx, event in enumerate(self.trace):
                _validate_no_mesg_encryption_key(
                    event.message_term,
                    mesg_vars,
                    f"role[{self.role_name}].trace[{idx}]",
                )
        return self

    def get_sanitized_var_sorts(self) -> Dict[str, str]:
        """Returns the complete map of sanitized variable names to CPSA sort strings for this role,
        including variables implied by key constructors (`ltk`, `bltk`, `pubk`, `privk`, `invk`),
        channels (`chan`), and memory locations (`locn`).
        """
        akey_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.AKEY} | {
            sanitize_cpsa_symbol(var.name) for var in self.variables if var.sort == CPSASortEnum.AKEY
        }
        name_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.NAME} | {
            sanitize_cpsa_symbol(var.name) for var in self.variables if var.sort == CPSASortEnum.NAME
        }
        implied_sorts: Dict[str, str] = {}
        for event in self.trace:
            _collect_implied_variable_sorts(event.message_term, implied_sorts, akey_vars, name_vars)
        for term in (
            self.unique_originating
            + self.unique_generated
            + self.non_originating
            + self.pen_non_originating
            + self.inputs
            + self.outputs
            + self.gen_st
        ):
            _collect_implied_variable_sorts(term, implied_sorts, akey_vars, name_vars)
        for fact in self.facts:
            for ft in fact[1:] if isinstance(fact, list) and len(fact) > 1 else []:
                _collect_implied_variable_sorts(ft, implied_sorts, akey_vars, name_vars)

        var_sorts: Dict[str, str] = {}
        for var_decl in self.variables:
            clean_name = sanitize_cpsa_symbol(var_decl.name)
            if clean_name not in var_sorts:
                var_sorts[clean_name] = var_decl.sort.value

        for raw_name, sort_val in implied_sorts.items():
            clean_name = sanitize_cpsa_symbol(raw_name)
            if clean_name not in var_sorts:
                var_sorts[clean_name] = sort_val

        for event in self.trace:
            if event.direction in ("send", "recv") and event.channel:
                clean_chan = sanitize_cpsa_symbol(event.channel)
                var_sorts.setdefault(clean_chan, CPSASortEnum.CHAN.value)
            elif event.direction in ("load", "stor"):
                loc_var = event.location or (event.channel if event.channel and event.channel != "ch" else None)
                if loc_var:
                    clean_loc = sanitize_cpsa_symbol(loc_var)
                    var_sorts.setdefault(clean_loc, CPSASortEnum.LOCN.value)
        return var_sorts

    def to_cpsa_json(self) -> List[Any]:
        var_sorts_map = self.get_sanitized_var_sorts()
        akey_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.AKEY.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.AKEY
        }
        name_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.NAME.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.NAME
        }
        declared_vars = set(var_sorts_map.keys()) | {var.name for var in self.variables}

        # Normalize trace events and collect all channels and locations used in trace events
        normalized_events: List[List[Any]] = []
        used_channels: List[str] = []
        used_locations: List[str] = []
        for event in self.trace:
            event_sexpr = event.to_cpsa_json()
            if len(event_sexpr) >= 2:
                event_sexpr[-1] = normalize_cpsa_term(
                    event_sexpr[-1],
                    akey_vars=akey_vars,
                    name_vars=name_vars,
                    declared_vars=declared_vars,
                    quote_undeclared=True,
                )
            if event.direction in ("send", "recv") and event.channel:
                clean_chan = sanitize_cpsa_symbol(event.channel)
                if clean_chan not in used_channels:
                    used_channels.append(clean_chan)
            elif event.direction in ("load", "stor"):
                loc_var = event.location or (event.channel if event.channel and event.channel != "ch" else None)
                if loc_var:
                    clean_loc = sanitize_cpsa_symbol(loc_var)
                    if clean_loc not in used_locations:
                        used_locations.append(clean_loc)
            normalized_events.append(event_sexpr)

        trace_form = ["trace"] + normalized_events

        trace_tokens: Set[str] = set()
        extract_term_tokens(trace_form, trace_tokens)
        reserved_operators = {
            "pubk", "privk", "invk", "ltk", "cat", "enc", "hash", "trace", "send", "recv", "load", "stor"
        } | CPSA_ALL_OPERATORS

        # Group declared variables by sort, keeping all declared variables and any implied variables that occur in trace
        sort_to_vars: Dict[str, List[str]] = {}
        declared_sanitized: Set[str] = set()
        explicit_sanitized = {sanitize_cpsa_symbol(v.name) for v in self.variables}
        for clean_var_name, sort_val in var_sorts_map.items():
            if clean_var_name not in explicit_sanitized and clean_var_name not in trace_tokens:
                continue
            if clean_var_name not in declared_sanitized:
                declared_sanitized.add(clean_var_name)
                sort_to_vars.setdefault(sort_val, []).append(clean_var_name)

        vars_form: List[Any] = ["vars"]
        for sort_value, var_names in sort_to_vars.items():
            vars_form.append(var_names + [sort_value])

        def _term_vars_in_trace(term: Any) -> bool:
            if _is_quoted_tag_literal(term):
                return False
            if isinstance(term, str):
                return term in trace_tokens and term in declared_sanitized
            if isinstance(term, (list, tuple)):
                term_tokens: Set[str] = set()
                extract_term_tokens(term, term_tokens)
                var_tokens = {
                    t for t in (term_tokens - reserved_operators) if not _is_quoted_tag_literal(t)
                }
                return bool(var_tokens and var_tokens.issubset(trace_tokens) and var_tokens.issubset(declared_sanitized))
            return False

        role_form: List[Any] = ["defrole", sanitize_cpsa_symbol(self.role_name), vars_form, trace_form]

        # Enforce Section 4.2 & Table 10.6: rndx/expt variables must be in uniq-gen, never uniq-orig
        dh_exponent_vars = {k for k, v in var_sorts_map.items() if v in ("rndx", "expt")}
        effective_uniq_orig: List[Any] = []
        effective_uniq_gen: List[Any] = [
            normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True)
            for t in self.unique_generated
        ]
        for raw_term in self.unique_originating:
            term = normalize_cpsa_term(
                raw_term, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
            )
            if isinstance(term, str) and term in dh_exponent_vars:
                if term not in effective_uniq_gen:
                    effective_uniq_gen.append(term)
            else:
                effective_uniq_orig.append(term)

        valid_uniq_orig = [term for term in effective_uniq_orig if _term_vars_in_trace(term)]
        if valid_uniq_orig:
            role_form.append(["uniq-orig"] + valid_uniq_orig)

        valid_uniq_gen = [term for term in effective_uniq_gen if _term_vars_in_trace(term)]
        if valid_uniq_gen:
            role_form.append(["uniq-gen"] + valid_uniq_gen)

        normalized_non_orig = [
            normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True)
            for t in self.non_originating
        ]
        valid_non_orig = [t for t in normalized_non_orig if _term_vars_in_trace(t)]
        if valid_non_orig:
            role_form.append(["non-orig"] + valid_non_orig)

        normalized_pen_non_orig = [
            normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True)
            for t in self.pen_non_originating
        ]
        valid_pen_non_orig = [t for t in normalized_pen_non_orig if _term_vars_in_trace(t)]
        if valid_pen_non_orig:
            role_form.append(["pen-non-orig"] + valid_pen_non_orig)

        if self.confidential_channels:
            role_form.append(["conf"] + [sanitize_cpsa_symbol(c) for c in self.confidential_channels])
        if self.authenticated_channels:
            role_form.append(["auth"] + [sanitize_cpsa_symbol(c) for c in self.authenticated_channels])
        if self.gen_st:
            valid_gen_st = [
                normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True)
                for t in self.gen_st
            ]
            valid_gen_st = [t for t in valid_gen_st if _term_vars_in_trace(t)]
            if valid_gen_st:
                role_form.append(["gen-st"] + valid_gen_st)
        if self.facts:
            role_form.append(["facts"] + self.facts)

        # Deterministic cpsa4roletran procedural inputs synthesis:
        # 1. Every input/output variable must occur in trace.
        # 2. All trace channels and locations must be included in inputs.
        # 3. No uniq-orig or uniq-gen value may appear in inputs (cpsa4roletran.md).
        # 4. Each input must be a basic value or channel/locn (no compound cat/enc/hash).
        # 5. Any variable or key constructor needed before being bound by recv/load must be in inputs.
        orig_set = {str(t) for t in (valid_uniq_orig + valid_uniq_gen)}
        non_orig_set = {str(t) for t in (valid_non_orig + valid_pen_non_orig)}

        valid_inputs: List[Any] = []
        known_vars: Set[str] = {
            t for t in (valid_uniq_orig + valid_uniq_gen) if isinstance(t, str)
        } | set(used_channels) | set(used_locations)

        for chan_name in used_channels:
            if chan_name not in valid_inputs:
                valid_inputs.append(chan_name)
        for loc_name in used_locations:
            if loc_name not in valid_inputs and loc_name not in orig_set:
                valid_inputs.append(loc_name)

        def _add_required_input(candidate: Any) -> None:
            if _is_quoted_tag_literal(candidate):
                return
            if str(candidate) in orig_set:
                return
            if not _is_valid_roletran_input_term(candidate):
                return
            if not _term_vars_in_trace(candidate):
                return
            if candidate not in valid_inputs:
                valid_inputs.append(candidate)
            if isinstance(candidate, str):
                known_vars.add(candidate)

        for input_term in self.inputs:
            normalized_input = normalize_cpsa_term(
                input_term,
                akey_vars=akey_vars,
                name_vars=name_vars,
                declared_vars=declared_vars,
                quote_undeclared=True,
            )
            _add_required_input(normalized_input)

        def _require_buildable(term: Any) -> None:
            if isinstance(term, str):
                if not _is_quoted_tag_literal(term) and term in declared_sanitized and term not in known_vars:
                    _add_required_input(term)
            elif isinstance(term, list) and term:
                op = term[0]
                if op in CPSA_KEY_CONSTRUCTOR_OPERATORS:
                    _add_required_input(term)
                else:
                    for sub in term[1:]:
                        _require_buildable(sub)

        def _process_recv_term(term: Any) -> None:
            if isinstance(term, str):
                if not _is_quoted_tag_literal(term) and term in declared_sanitized:
                    known_vars.add(term)
            elif isinstance(term, list) and term:
                op = term[0]
                if op == "cat":
                    for sub in term[1:]:
                        _process_recv_term(sub)
                elif op == "enc" and len(term) >= 2:
                    key_term = term[-1]
                    dec_key = _invert_cpsa_key(key_term, akey_vars)
                    payload_tokens: Set[str] = set()
                    for p in term[1:-1]:
                        extract_term_tokens(p, payload_tokens)
                    payload_vars = {
                        t
                        for t in (payload_tokens - reserved_operators)
                        if not _is_quoted_tag_literal(t) and t in declared_sanitized
                    }
                    has_unbound_payload = bool(payload_vars - known_vars)
                    if _is_valid_roletran_input_term(dec_key):
                        is_unprovided_invk = isinstance(dec_key, list) and dec_key and dec_key[0] == "invk"
                        is_peer_secret_key = (
                            isinstance(dec_key, list)
                            and dec_key
                            and dec_key[0] in ("privk", "invk")
                            and str(dec_key) in non_orig_set
                            and not has_unbound_payload
                        )
                        if not is_peer_secret_key and not is_unprovided_invk:
                            if isinstance(dec_key, str):
                                if dec_key not in known_vars:
                                    _add_required_input(dec_key)
                            else:
                                _add_required_input(dec_key)
                    else:
                        _require_buildable(dec_key)
                    for p in term[1:-1]:
                        _process_recv_term(p)
                elif op in CPSA_KEY_CONSTRUCTOR_OPERATORS:
                    _add_required_input(term)
                else:
                    for sub in term[1:]:
                        _require_buildable(sub)

        for event_sexpr in normalized_events:
            if len(event_sexpr) < 2:
                continue
            ev_dir = event_sexpr[0]
            ev_msg = event_sexpr[-1]
            if ev_dir in ("send", "stor"):
                _require_buildable(ev_msg)
            elif ev_dir in ("recv", "load"):
                _process_recv_term(ev_msg)

        if valid_inputs:
            role_form.append(["inputs"] + valid_inputs)

        input_set = {str(t) for t in valid_inputs}
        if self.outputs:
            valid_outputs: List[Any] = []
            for output_term in self.outputs:
                normalized_output = normalize_cpsa_term(
                    output_term,
                    akey_vars=akey_vars,
                    name_vars=name_vars,
                    declared_vars=declared_vars,
                    quote_undeclared=True,
                )
                if str(normalized_output) in input_set:
                    continue
                if not _term_vars_in_trace(normalized_output):
                    continue
                if normalized_output not in valid_outputs:
                    valid_outputs.append(normalized_output)
            if valid_outputs:
                role_form.append(["outputs"] + valid_outputs)

        if self.comment:
            role_form.append(["comment", f'"{self.comment}"'])

        return role_form


class CPSAStrandInstance(BaseModel):
    """Instantiation of a role strand within a preskeleton (defstrandmax, Table 10.1)."""

    role_name: str = Field(..., description="Name of the instantiated role")
    trace_length: Optional[int] = Field(
        default=None,
        description="Trace height (optional; defstrandmax is always used to evaluate full strand)",
    )
    variable_bindings: Dict[str, CPSATerm] = Field(
        default_factory=dict,
        description="Mapping from role variable identifier to instantiated skeleton term conforming to CPSA grammar",
    )

    def to_cpsa_json(
        self,
        akey_vars: Optional[Set[str]] = None,
        name_vars: Optional[Set[str]] = None,
        declared_vars: Optional[Set[str]] = None,
        valid_role_vars: Optional[Set[str]] = None,
        auto_bind_vars: Optional[Set[str]] = None,
    ) -> List[Any]:
        strand_form: List[Any] = ["defstrandmax", sanitize_cpsa_symbol(self.role_name)]
        bound_role_vars: Set[str] = set()
        for role_var, term_val in self.variable_bindings.items():
            clean_role_var = sanitize_cpsa_symbol(role_var)
            if valid_role_vars is not None and clean_role_var not in valid_role_vars:
                continue
            norm_val = normalize_cpsa_term(
                term_val,
                akey_vars=akey_vars,
                name_vars=name_vars,
                declared_vars=declared_vars,
                quote_undeclared=declared_vars is not None,
            )
            strand_form.append([clean_role_var, norm_val])
            bound_role_vars.add(clean_role_var)

        if valid_role_vars and auto_bind_vars:
            for extra_var in sorted(valid_role_vars & auto_bind_vars):
                if extra_var not in bound_role_vars:
                    strand_form.append([extra_var, extra_var])
                    bound_role_vars.add(extra_var)

        return strand_form


class CPSAPreskeleton(BaseModel):
    """Point-of-view preskeleton to be formally analyzed by CPSA (defskeleton, Tables 10.1 & 10.6)."""

    protocol_name: str = Field(..., description="Target protocol identifier matching a declared defprotocol")
    description: Optional[str] = Field(
        default=None,
        description="Formal security objective or point-of-view scenario being verified",
    )
    variables: List[CPSAVariableDeclaration] = Field(
        default_factory=list,
        description="Variables appearing across strands in the skeleton",
    )
    strands: List[CPSAStrandInstance] = Field(..., description="Role strands active in this execution scenario")
    non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Keys or secrets assumed never compromised/originating (non-orig)",
    )
    pen_non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Penetrator non-originating terms (pen-non-orig)",
    )
    unique_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Nonces or secrets assumed fresh and unique across strands (uniq-orig)",
    )
    unique_generated: List[CPSATerm] = Field(
        default_factory=list,
        description="Uniquely generated terms (uniq-gen)",
    )
    listeners: List[CPSATerm] = Field(
        default_factory=list,
        description="Terms to verify secrecy for via listener strands (deflistener)",
    )
    precedes: List[List[List[int]]] = Field(
        default_factory=list,
        description="Causal message ordering constraints between node pairs: [((s1, n1), (s2, n2))]",
    )
    leadsto: List[List[List[int]]] = Field(
        default_factory=list,
        description="State synchronization ordering constraints between node pairs: [((s1, n1), (s2, n2))]",
    )
    priority: List[List[Any]] = Field(
        default_factory=list,
        description="Solver priority overrides for specific nodes: [((s, n), int_priority)]",
    )
    facts: List[List[Any]] = Field(
        default_factory=list,
        description="Logical facts asserted in this skeleton",
    )
    comment: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def forbid_role_keywords_in_skeleton(cls, data: Any) -> Any:
        if isinstance(data, dict):
            misplaced = set(data.keys()) & _FORBIDDEN_IN_SKELETON
            if misplaced:
                bad_key = sorted(list(misplaced))[0]
                raise ValueError(
                    f"Keyword '{bad_key}' is a role-only keyword (MITRE CPSA 4.4.9 Tables 10.1 & 10.6) "
                    "and is strictly forbidden inside CPSAPreskeleton (defskeleton)."
                )
        return data

    @model_validator(mode="after")
    def validate_skeleton_invariants(self) -> "CPSAPreskeleton":
        mesg_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.MESG}
        if mesg_vars:
            for listener in self.listeners:
                _validate_no_mesg_encryption_key(
                    listener,
                    mesg_vars,
                    f"skeleton[{self.protocol_name}].listeners",
                )
        return self

    def to_cpsa_json(
        self,
        role_var_sorts_by_role: Optional[Dict[str, Dict[str, str]]] = None,
    ) -> List[Any]:
        skel_form: List[Any] = ["defskeleton", sanitize_cpsa_symbol(self.protocol_name)]

        var_sorts_map: Dict[str, str] = {}
        for var_decl in self.variables:
            clean_var_name = sanitize_cpsa_symbol(var_decl.name)
            if clean_var_name not in var_sorts_map:
                var_sorts_map[clean_var_name] = var_decl.sort.value

        # Infer sorts from strand variable bindings if role_var_sorts_by_role is provided
        if role_var_sorts_by_role:
            for strand in self.strands:
                clean_role = sanitize_cpsa_symbol(strand.role_name)
                role_sorts = role_var_sorts_by_role.get(clean_role, {})
                for role_var, bound_val in strand.variable_bindings.items():
                    clean_rv = sanitize_cpsa_symbol(role_var)
                    rv_sort = role_sorts.get(clean_rv)
                    if rv_sort and isinstance(bound_val, str) and not _is_quoted_tag_literal(bound_val):
                        clean_bv = sanitize_cpsa_symbol(bound_val)
                        var_sorts_map.setdefault(clean_bv, rv_sort)

        akey_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.AKEY.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.AKEY
        }
        name_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.NAME.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.NAME
        }

        implied_sorts: Dict[str, str] = {}
        for strand in self.strands:
            for bound_val in strand.variable_bindings.values():
                _collect_implied_variable_sorts(bound_val, implied_sorts, akey_vars, name_vars)
        for term in (
            self.listeners
            + self.non_originating
            + self.pen_non_originating
            + self.unique_originating
            + self.unique_generated
        ):
            _collect_implied_variable_sorts(term, implied_sorts, akey_vars, name_vars)
        for fact in self.facts:
            for ft in fact[1:] if isinstance(fact, list) and len(fact) > 1 else []:
                _collect_implied_variable_sorts(ft, implied_sorts, akey_vars, name_vars)

        for raw_name, sort_val in implied_sorts.items():
            clean_name = sanitize_cpsa_symbol(raw_name)
            var_sorts_map.setdefault(clean_name, sort_val)

        akey_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.AKEY.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.AKEY
        }
        name_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.NAME.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.NAME
        }
        declared_vars = set(var_sorts_map.keys()) | {var.name for var in self.variables}

        if var_sorts_map:
            sort_to_vars: Dict[str, List[str]] = {}
            for clean_var_name, sort_val in var_sorts_map.items():
                sort_to_vars.setdefault(sort_val, []).append(clean_var_name)
            vars_form: List[Any] = ["vars"]
            for sort_value, var_names in sort_to_vars.items():
                vars_form.append(var_names + [sort_value])
            skel_form.append(vars_form)

        strand_forms: List[List[Any]] = []
        skel_trace_tokens: Set[str] = set()
        for strand in self.strands:
            clean_role = sanitize_cpsa_symbol(strand.role_name)
            valid_role_vars = (
                set(role_var_sorts_by_role[clean_role].keys())
                if role_var_sorts_by_role and clean_role in role_var_sorts_by_role
                else None
            )
            s_form = strand.to_cpsa_json(
                akey_vars=akey_vars,
                name_vars=name_vars,
                declared_vars=declared_vars,
                valid_role_vars=valid_role_vars,
                auto_bind_vars=set(var_sorts_map.keys()) if valid_role_vars is not None else None,
            )
            strand_forms.append(s_form)
            for maplet in s_form[2:]:
                if isinstance(maplet, list) and len(maplet) == 2:
                    extract_term_tokens(maplet[1], skel_trace_tokens)

        skel_form.extend(strand_forms)

        for listener in self.listeners:
            norm_listener = normalize_cpsa_term(
                listener, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
            )
            extract_term_tokens(norm_listener, skel_trace_tokens)
            skel_form.append(["deflistener", norm_listener])

        reserved_operators = {
            "pubk", "privk", "invk", "ltk", "cat", "enc", "hash", "trace", "send", "recv", "load", "stor"
        } | CPSA_ALL_OPERATORS

        def _skel_term_in_trace(term: Any) -> bool:
            if _is_quoted_tag_literal(term):
                return False
            if not skel_trace_tokens:
                return True
            if isinstance(term, str):
                return term in skel_trace_tokens
            if isinstance(term, (list, tuple)):
                toks: Set[str] = set()
                extract_term_tokens(term, toks)
                var_toks = {t for t in (toks - reserved_operators) if not _is_quoted_tag_literal(t)}
                return bool(var_toks and var_toks.issubset(skel_trace_tokens))
            return False

        if self.non_originating:
            norm_non_orig = [
                normalize_cpsa_term(
                    t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
                )
                for t in self.non_originating
            ]
            norm_non_orig = [t for t in norm_non_orig if _skel_term_in_trace(t)]
            if norm_non_orig:
                skel_form.append(["non-orig"] + norm_non_orig)
        if self.pen_non_originating:
            norm_pen_non_orig = [
                normalize_cpsa_term(
                    t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
                )
                for t in self.pen_non_originating
            ]
            norm_pen_non_orig = [t for t in norm_pen_non_orig if _skel_term_in_trace(t)]
            if norm_pen_non_orig:
                skel_form.append(["pen-non-orig"] + norm_pen_non_orig)

        skel_dh_vars = {k for k, v in var_sorts_map.items() if v in ("rndx", "expt")}
        effective_skel_uniq_orig: List[Any] = []
        effective_skel_uniq_gen: List[Any] = [
            normalize_cpsa_term(
                t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
            )
            for t in self.unique_generated
        ]
        effective_skel_uniq_gen = [t for t in effective_skel_uniq_gen if _skel_term_in_trace(t)]
        for raw_term in self.unique_originating:
            term = normalize_cpsa_term(
                raw_term, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
            )
            if not _skel_term_in_trace(term):
                continue
            if isinstance(term, str) and (
                term in skel_dh_vars
                or "exponent" in term.lower()
                or term.endswith("_dh")
                or term.endswith("_exp")
            ):
                if term not in effective_skel_uniq_gen:
                    effective_skel_uniq_gen.append(term)
            else:
                effective_skel_uniq_orig.append(term)

        if effective_skel_uniq_orig:
            skel_form.append(["uniq-orig"] + effective_skel_uniq_orig)
        if effective_skel_uniq_gen:
            skel_form.append(["uniq-gen"] + effective_skel_uniq_gen)
        if self.precedes:
            skel_form.append(["precedes"] + self.precedes)
        if self.leadsto:
            skel_form.append(["leadsto"] + self.leadsto)
        if self.priority:
            skel_form.append(["priority"] + self.priority)
        if self.facts:
            skel_form.append(["facts"] + self.facts)

        if self.comment:
            skel_form.append(["comment", f'"{self.comment}"'])

        return skel_form


class CPSAProtocolSpecification(BaseModel):
    """Complete protocol specification and verification suite (defprotocol + defskeletons, Table 10.1)."""

    protocol_name: str = Field(..., description="Unique protocol identifier")
    is_verifiable_protocol: bool = Field(
        default=True,
        description=(
            "True if the provided RFC excerpt specifies an interactive multi-message cryptographic or "
            "authenticated exchange that can be modeled in CPSA; False if this RFC is a false positive "
            "(e.g., no message flights, delegates key exchange to an external RFC, only defines packet/frame "
            "formats or local flags, or is a plaintext application protocol)."
        ),
    )
    ineligibility_reason: Optional[str] = Field(
        default=None,
        description="If is_verifiable_protocol is False, concise explanation of why the RFC excerpt cannot be modeled as an interactive cryptographic protocol.",
    )
    message_algebra: CPSAMessageAlgebra = Field(
        default="basic",
        description="CPSA message algebra selection: basic or diffie-hellman",
    )
    roles: List[CPSAProtocolRole] = Field(
        default_factory=list,
        description="Protocol participant role specifications (empty ONLY when is_verifiable_protocol is False)",
    )
    primary_secrecy_goals: List[CPSATerm] = Field(
        default_factory=list,
        description=(
            "Primary confidential terms (e.g. established session keys, premaster secrets, shared tokens) "
            "semantically identified by the LLM from the RFC whose confidentiality must be verified via listener strands."
        ),
    )
    skeletons: List[CPSAPreskeleton] = Field(
        default_factory=list,
        description="Analysis preskeletons / points of view",
    )
    herald_comment: Optional[str] = None
    herald_options: List[str] = Field(
        default_factory=list,
        description=(
            "Optional CPSA 4.4.9 search-order herald flags persisted when non-default search order "
            "resolves state-space snowballing (allowed: 'try-old-strands', 'check-nonces', 'reverse-nodes')."
        ),
    )

    def has_cryptographic_primitives(self) -> bool:
        """Returns True if the specification uses at least one CPSA cryptographic operator, key sort, or secure channel."""
        crypto_ops = {"enc", "hash", "ltk", "pubk", "privk", "invk", "bltk", "exp", "gen", "mul", "rec"}
        crypto_sorts = {"skey", "akey", "rndx", "expt", "base"}

        def _term_has_crypto(term: Any) -> bool:
            if isinstance(term, list) and term:
                if isinstance(term[0], str) and term[0] in crypto_ops:
                    return True
                return any(_term_has_crypto(sub) for sub in term[1:])
            return False

        for role in self.roles:
            if role.confidential_channels or role.authenticated_channels:
                return True
            if role.non_originating or role.pen_non_originating or role.unique_generated:
                return True
            for v in role.variables:
                if v.sort.value in crypto_sorts:
                    return True
            for ev in role.trace:
                if _term_has_crypto(ev.message_term):
                    return True
            for t in role.inputs + role.outputs + role.unique_originating:
                if _term_has_crypto(t):
                    return True
        for skel in self.skeletons:
            if skel.non_originating or skel.pen_non_originating or skel.unique_generated:
                return True
        return False

    @model_validator(mode="before")
    @classmethod
    def forbid_scoped_keywords_at_top_level(cls, data: Any) -> Any:
        if isinstance(data, dict):
            misplaced = set(data.keys()) & _FORBIDDEN_AT_TOP_LEVEL
            if misplaced:
                bad_key = sorted(list(misplaced))[0]
                raise ValueError(
                    f"Keyword '{bad_key}' is scoped to defrole or defskeleton (MITRE CPSA 4.4.9 Table 10.1) "
                    "and is forbidden directly on the top-level CPSAProtocolSpecification."
                )
        return data

    @model_validator(mode="after")
    def validate_algebra_consistency(self) -> "CPSAProtocolSpecification":
        """Ensures role traces are non-empty and Diffie-Hellman sorts/operators are forbidden under 'basic' algebra."""
        if not self.roles:
            self.is_verifiable_protocol = False
            if not self.ineligibility_reason:
                self.ineligibility_reason = (
                    self.herald_comment
                    or "No interactive cryptographic protocol roles could be extracted from the provided RFC slice."
                )
        else:
            for role in self.roles:
                if not role.trace:
                    raise ValueError(
                        f"Role '{role.role_name}' has an empty trace: []. Every CPSA defrole must contain at least "
                        "one send/recv trace event (or if this RFC does not specify a message exchange, set "
                        "is_verifiable_protocol=False and roles=[])."
                    )
        if self.message_algebra == "basic":
            for term in self.primary_secrecy_goals:
                validate_cpsa_term_syntax(
                    term,
                    algebra="basic",
                    path="primary_secrecy_goals",
                )
            for role in self.roles:
                for var_decl in role.variables:
                    if var_decl.sort.value in CPSA_DH_ONLY_VARIABLE_SORTS:
                        raise ValueError(
                            f"Diffie-Hellman variable sort '{var_decl.sort.value}' on variable '{var_decl.name}' "
                            f"in role '{role.role_name}' is forbidden under 'basic' message algebra (Table 10.2). "
                            "Change protocol message_algebra to 'diffie-hellman' or use a basic algebra sort."
                        )
                for event in role.trace:
                    validate_cpsa_term_syntax(
                        event.message_term,
                        algebra="basic",
                        path=f"role[{role.role_name}].trace",
                    )
                for term in (
                    role.inputs
                    + role.outputs
                    + role.non_originating
                    + role.pen_non_originating
                    + role.unique_originating
                    + role.unique_generated
                ):
                    validate_cpsa_term_syntax(
                        term,
                        algebra="basic",
                        path=f"role[{role.role_name}].declarations",
                    )
            for skel in self.skeletons:
                for var_decl in skel.variables:
                    if var_decl.sort.value in CPSA_DH_ONLY_VARIABLE_SORTS:
                        raise ValueError(
                            f"Diffie-Hellman variable sort '{var_decl.sort.value}' on variable '{var_decl.name}' "
                            f"in skeleton '{skel.protocol_name}' is forbidden under 'basic' message algebra (Table 10.2)."
                        )
                for strand in skel.strands:
                    for bound_var, bound_term in strand.variable_bindings.items():
                        validate_cpsa_term_syntax(
                            bound_term,
                            algebra="basic",
                            path=f"skeleton[{skel.protocol_name}].strand[{strand.role_name}].{bound_var}",
                        )
                for term in (
                    skel.listeners
                    + skel.non_originating
                    + skel.pen_non_originating
                    + skel.unique_originating
                    + skel.unique_generated
                ):
                    validate_cpsa_term_syntax(
                        term,
                        algebra="basic",
                        path=f"skeleton[{skel.protocol_name}].declarations",
                    )
        return self

    def to_cpsa_json_payload(self) -> List[List[Any]]:
        """Converts the specification into a sequence of top-level CPSA JSON forms."""
        payload: List[List[Any]] = []

        # Every SCM file MUST have a herald declaration as the first form per MITRE CPSA Table 10.1
        herald_text = self.herald_comment or f"{self.protocol_name} Protocol Verification Suite"
        herald_form: List[Any] = ["herald", f'"{herald_text}"']
        if self.message_algebra == "diffie-hellman":
            herald_form.append(["algebra", "diffie-hellman"])
        for opt in self.herald_options:
            if opt in {"try-old-strands", "check-nonces", "reverse-nodes"}:
                herald_form.append([opt])
        payload.append(herald_form)

        clean_proto_name = sanitize_cpsa_symbol(self.protocol_name)
        protocol_form: List[Any] = ["defprotocol", clean_proto_name, self.message_algebra]
        role_var_sorts_by_role: Dict[str, Dict[str, str]] = {}
        for role in self.roles:
            clean_role_name = sanitize_cpsa_symbol(role.role_name)
            role_var_sorts_by_role[clean_role_name] = role.get_sanitized_var_sorts()
            protocol_form.append(role.to_cpsa_json())
        payload.append(protocol_form)

        for skel in self.skeletons:
            payload.append(skel.to_cpsa_json(role_var_sorts_by_role=role_var_sorts_by_role))

        return payload
```

---

### `src/logging_config.py`

*sha256:`f27629aeabb1` · 682 lines · 33.8 KB (~8,649 tokens) · lang:`python`*

```python
"""Comprehensive Structured Logging Subsystem for RFC-LLM Pipeline."""

import csv
import datetime
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from src.system_config import SYSTEM_CONFIG


class PipelineConsoleFormatter(logging.Formatter):
    """ANSI color-coded console formatter for distinct pipeline stages."""

    GREY = "\x1b[38;20m"
    CYAN = "\x1b[36;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    FORMAT_PREFIX = "%(asctime)s | "
    FORMAT_SUFFIX = " | %(name)s - %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + FORMAT_PREFIX + "DEBUG" + FORMAT_SUFFIX + RESET,
        logging.INFO: CYAN + FORMAT_PREFIX + "INFO " + FORMAT_SUFFIX + RESET,
        logging.WARNING: YELLOW + FORMAT_PREFIX + "WARN " + FORMAT_SUFFIX + RESET,
        logging.ERROR: RED + FORMAT_PREFIX + "ERROR" + FORMAT_SUFFIX + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT_PREFIX + "CRIT " + FORMAT_SUFFIX + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.GREY + self.FORMAT_PREFIX + "%(levelname)s" + self.FORMAT_SUFFIX + self.RESET)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def configure_pipeline_logging(
    log_level: int = logging.INFO,
    run_log_file: Optional[Path] = None,
) -> logging.Logger:
    """Configures the root pipeline logger with both console and file handlers."""
    SYSTEM_CONFIG.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger("rfc_llm")
    root_logger.setLevel(log_level)
    root_logger.propagate = False

    # Avoid duplicate handlers and prevent file descriptor leaks on re-entry across batch runs
    if root_logger.hasHandlers():
        for existing_handler in list(root_logger.handlers):
            root_logger.removeHandler(existing_handler)
            try:
                existing_handler.close()
            except Exception:
                pass

    # Silence third-party litellm, HTTP client, and visualizer access loggers
    for _noisy_logger in ("LiteLLM", "litellm", "LiteLLM Proxy", "LiteLLM Router", "aiohttp.access", "openai", "openai._base_client", "httpx", "httpcore"):
        _nl = logging.getLogger(_noisy_logger)
        _nl.setLevel(logging.WARNING if _noisy_logger == "aiohttp.access" else logging.ERROR)
        _nl.propagate = False

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(PipelineConsoleFormatter())
    root_logger.addHandler(console_handler)

    # 2. Global Pipeline File Handler
    global_log_path = SYSTEM_CONFIG.LOGS_DIR / "rfc_llm_pipeline.log"
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    global_file_handler = logging.FileHandler(global_log_path, mode="a", encoding="utf-8")
    global_file_handler.setLevel(logging.DEBUG)  # Always log debug to file
    global_file_handler.setFormatter(file_formatter)
    root_logger.addHandler(global_file_handler)

    # 3. Optional Per-Run File Handler
    if run_log_file:
        run_log_file.parent.mkdir(parents=True, exist_ok=True)
        run_file_handler = logging.FileHandler(run_log_file, mode="w", encoding="utf-8")
        run_file_handler.setLevel(logging.DEBUG)
        run_file_handler.setFormatter(file_formatter)
        root_logger.addHandler(run_file_handler)

    return root_logger


def get_pipeline_logger(subsystem: str) -> logging.Logger:
    """Returns a namespaced child logger for a specific pipeline subsystem."""
    return logging.getLogger(f"rfc_llm.{subsystem}")


class PipelineMetricsCSVLogger:
    """Logs tabular run-level experiment metrics to a persistent deduplicated CSV master ledger.

    Performs atomic in-place upserts keyed by normalized `rfc_id` (`RFC4285`), overwriting older
    entries when an RFC is re-evaluated while incrementing `run_count`, and automatically
    migrating legacy CSV headers to the expanded 50-column telemetry schema.
    """

    CSV_HEADER = [
        # Group A: Identity, Status, Step Counts & Intake
        "timestamp",
        "rfc_id",
        "run_count",
        "is_eligible",
        "status",
        "quality_tier",
        "total_completion_steps",
        "zero_shot_passed",
        "schema_repairs",
        "roletran_repairs",
        "solver_repairs",
        "total_repairs",
        "rejection_gate",
        "protocol_name",
        # Group B: Protocol, Solver Complexity & Formal CPSA Security Findings Telemetry
        "message_algebra",
        "selected_sections",
        "sliced_lines_count",
        "role_count",
        "preskeleton_count",
        "scm_lines_count",
        "shapes_count",
        "explored_skeletons_count",
        "all_povs_multi_strand",
        "secrecy_proved",
        "role_executability",
        "dead_roles_count",
        "authentication_profile",
        "parameter_agreement_status",
        "disagreed_parameters_count",
        "disagreed_parameters_summary",
        "role_reflection_status",
        "secrecy_status",
        "protected_secrets",
        "leaked_secrets",
        "defgoal_satisfaction_status",
        "shape_analysis_sentences_count",
        "encryption_tests_count",
        "nonce_tests_count",
        "channel_tests_count",
        "anomalies_count",
        "vulnerabilities_and_anomalies",
        # Group C: Self-Healing Searcher & Snowball Telemetry
        "searcher_invocations",
        "herald_options",
        # Group D: Runtime & Per-Role Model Telemetry (Dedicated columns per model role)
        "duration_seconds",
        "router_model",
        "router_calls",
        "router_tokens",
        "router_cost_usd",
        "extraction_model",
        "extraction_calls",
        "extraction_tokens",
        "extraction_cost_usd",
        "query_model",
        "query_calls",
        "query_tokens",
        "query_cost_usd",
        "repair_model",
        "repair_calls",
        "repair_tokens",
        "repair_cost_usd",
        "total_calls",
        "total_tokens",
        "total_cost_usd",
        # Group E: Persistent Artifact File Paths & Diagnostics
        "scm_path",
        "shapes_xhtml_path",
        "trajectory_json_path",
        "error_message",
    ]

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or (SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv")
        self._ensure_header()

    @staticmethod
    def normalize_rfc_id(rfc_id: str) -> str:
        """Normalizes 'rfc4285', 'RFC 4285', or 'RFC_4285' to canonical 'RFC4285'."""
        return (rfc_id or "").strip().upper().replace(" ", "").replace("_", "")

    def _read_existing_rows(self) -> List[dict]:
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            return []
        try:
            with open(self.csv_path, mode="r", newline="", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                return [dict(row) for row in reader if row.get("rfc_id")]
        except Exception:
            return []

    def _write_all_rows(self, rows: List[dict]) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.csv_path.with_suffix(".csv.tmp")
        with open(tmp_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER, extrasaction="ignore")
            writer.writeheader()
            for r in rows:
                clean_row = {col: r.get(col, "") for col in self.CSV_HEADER}
                writer.writerow(clean_row)
        tmp_path.replace(self.csv_path)

    def _ensure_header(self) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            self._write_all_rows([])
            return
        # Automatically migrate legacy CSV headers if columns changed
        try:
            with open(self.csv_path, mode="r", newline="", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                first_row = next(reader, None)
            if first_row != self.CSV_HEADER:
                existing = self._read_existing_rows()
                # Deduplicate any legacy duplicate rows on migration, keeping latest & counting runs
                deduped: dict = {}
                counts: dict = {}
                for r in existing:
                    norm_id = self.normalize_rfc_id(r.get("rfc_id", ""))
                    if not norm_id:
                        continue
                    counts[norm_id] = counts.get(norm_id, 0) + 1
                    r["rfc_id"] = norm_id
                    if not r.get("run_count"):
                        r["run_count"] = str(counts[norm_id])
                    deduped[norm_id] = r
                self._write_all_rows(list(deduped.values()))
        except Exception:
            pass

    def seed_from_source(self, source_path: Path) -> int:
        """Copies rows from an existing CSV file or prior run directory into `self.csv_path`
        without modifying `source_path` (ensuring strict run-to-run isolation).

        Supports:
        1. Direct `.csv` file path (e.g., `output/run_.../pipeline_runs.csv` or `logs/pipeline_runs.csv`)
        2. Run directory containing `pipeline_runs.csv`
        3. Legacy run directory containing `metadata_index.json` (reconstructs rows from `filtered_rfcs` and `runs`)
        """
        resolved = source_path.resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"Seed CSV or run directory does not exist: {source_path}")

        csv_file: Optional[Path] = None
        index_file: Optional[Path] = None
        if resolved.is_file():
            if resolved.name == "metadata_index.json":
                index_file = resolved
            else:
                csv_file = resolved
        elif resolved.is_dir():
            cand_csv = resolved / "pipeline_runs.csv"
            cand_idx = resolved / "metadata_index.json"
            if cand_csv.exists() and cand_csv.stat().st_size > 0:
                csv_file = cand_csv
            elif cand_idx.exists():
                index_file = cand_idx
            else:
                raise FileNotFoundError(
                    f"Directory {source_path} contains neither pipeline_runs.csv nor metadata_index.json"
                )

        if csv_file is not None:
            if csv_file.resolve() == self.csv_path.resolve():
                return len(self._read_existing_rows())
            seeded_rows: Dict[str, dict] = {}
            with open(csv_file, mode="r", newline="", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    norm_id = self.normalize_rfc_id(row.get("rfc_id", ""))
                    if norm_id:
                        row_copy = {col: str(row.get(col) or "") for col in self.CSV_HEADER}
                        row_copy["rfc_id"] = norm_id
                        # Backfill the 17 CPSA security_findings columns if seeding from an older 50-column CSV
                        if (
                            row_copy.get("is_eligible", "").strip().lower() == "true"
                            and not row_copy.get("role_executability")
                            and row_copy.get("trajectory_json_path")
                        ):
                            t_path = Path(row_copy["trajectory_json_path"])
                            if t_path.exists():
                                try:
                                    t_obj = json.loads(t_path.read_text(encoding="utf-8", errors="ignore"))
                                    qa_t = t_obj.get("quality_assessment") or {}
                                    s6_t = t_obj.get("stage6_cpsa4_solver") or {}
                                    fin_t = t_obj.get("final_verified_output") or {}
                                    sf = t_obj.get("security_findings") or qa_t.get("security_findings")
                                    if not sf and s6_t.get("shapes_analysis_from_shapes_txt"):
                                        from src.verification_engine.trajectory_metadata_exporter import (
                                            compute_security_findings,
                                        )
                                        sf = compute_security_findings(
                                            shapes_analysis=s6_t.get("shapes_analysis_from_shapes_txt") or {},
                                            exploration_telemetry=s6_t.get("exploration_telemetry_from_txt") or {},
                                            sas_formulas=fin_t.get("shape_analysis_sentences") or [],
                                        )
                                    if isinstance(sf, dict) and sf:
                                        dis_list = sf.get("parameter_disagreements") or []
                                        dis_str = ";".join(
                                            f"{d.get('pov_role', '?')}->{d.get('peer_role', '?')}:{d.get('parameter', '?')}({d.get('pov_value', '?')}!={d.get('peer_value', '?')})"
                                            for d in dis_list
                                            if isinstance(d, dict)
                                        )
                                        at = sf.get("authentication_tests_summary") or {}
                                        anom_list = sf.get("vulnerabilities_and_anomalies") or []
                                        row_copy["role_executability"] = str(sf.get("role_executability") or "")
                                        row_copy["dead_roles_count"] = str(int(sf.get("dead_roles_count", 0)))
                                        row_copy["authentication_profile"] = str(sf.get("authentication_profile") or "")
                                        row_copy["parameter_agreement_status"] = str(sf.get("parameter_agreement_status") or "")
                                        row_copy["disagreed_parameters_count"] = str(len(dis_list))
                                        row_copy["disagreed_parameters_summary"] = dis_str
                                        row_copy["role_reflection_status"] = str(sf.get("role_reflection_status") or "")
                                        row_copy["secrecy_status"] = str(sf.get("secrecy_status") or "")
                                        row_copy["protected_secrets"] = ";".join(str(x) for x in (sf.get("protected_secrets") or []))
                                        row_copy["leaked_secrets"] = ";".join(str(x) for x in (sf.get("leaked_secrets") or []))
                                        row_copy["defgoal_satisfaction_status"] = str(sf.get("defgoal_satisfaction_status") or "")
                                        row_copy["shape_analysis_sentences_count"] = str(int(sf.get("shape_analysis_sentences_count", 0)))
                                        row_copy["encryption_tests_count"] = str(int(at.get("encryption_tests", 0)))
                                        row_copy["nonce_tests_count"] = str(int(at.get("nonce_tests", 0)))
                                        row_copy["channel_tests_count"] = str(int(at.get("channel_tests", 0)))
                                        row_copy["anomalies_count"] = str(len(anom_list))
                                        row_copy["vulnerabilities_and_anomalies"] = " | ".join(str(x) for x in anom_list)
                                except Exception:
                                    pass
                        seeded_rows[norm_id] = row_copy
            rows_list = list(seeded_rows.values())
            self._write_all_rows(rows_list)
            return len(rows_list)

        if index_file is not None:
            idx_data = json.loads(index_file.read_text(encoding="utf-8", errors="ignore"))
            created_ts = (idx_data.get("created_at_utc") or "").replace("T", " ").replace("Z", "")
            for filt in idx_data.get("filtered_rfcs", []):
                rid = self.normalize_rfc_id(filt.get("rfc_id", ""))
                if not rid:
                    continue
                reason = filt.get("reason") or "Ineligible"
                if not reason.lower().startswith("ineligible"):
                    reason = f"Ineligible: {reason}"
                self.log_run(
                    rfc_id=rid,
                    is_eligible=False,
                    status="INELIGIBLE",
                    quality_tier="INELIGIBLE",
                    rejection_gate=filt.get("gate") or "Intake Gate",
                    protocol_name=filt.get("title") or rid,
                    duration_seconds=float(filt.get("duration_seconds") or 0.0),
                    error_message=reason,
                )
            for run_entry in idx_data.get("runs", []):
                rid = self.normalize_rfc_id(run_entry.get("rfc_id", ""))
                if not rid:
                    continue
                is_elig = bool(run_entry.get("is_eligible", True))
                traj_str = run_entry.get("metadata_json_file")
                traj_path = Path(traj_str) if traj_str else None
                traj_obj: Dict[str, Any] = {}
                if traj_path and traj_path.exists():
                    try:
                        traj_obj = json.loads(traj_path.read_text(encoding="utf-8", errors="ignore"))
                    except Exception:
                        traj_obj = {}
                meta = traj_obj.get("rfc_metadata", {})
                s2 = traj_obj.get("stage2_initial_extraction", {})
                s5 = traj_obj.get("stage5_preflight_gate", {})
                s6 = traj_obj.get("stage6_cpsa4_solver", {})
                qa = traj_obj.get("quality_assessment", {})
                sec_f = traj_obj.get("security_findings") or qa.get("security_findings")
                ast_obj = (traj_obj.get("final_verified_output") or {}).get("final_ast") or {}
                scm_file_str = run_entry.get("scm_file")
                scm_p = Path(scm_file_str) if scm_file_str else None
                xhtml_p: Optional[Path] = None
                if scm_p and scm_p.parent.exists():
                    xhtmls = sorted(scm_p.parent.glob("*_shapes.xhtml"))
                    if xhtmls:
                        xhtml_p = xhtmls[0]
                self.log_run(
                    rfc_id=rid,
                    is_eligible=is_elig,
                    quality_tier=qa.get("quality_tier") or run_entry.get("quality_tier"),
                    protocol_name=meta.get("protocol_name") or run_entry.get("protocol_name"),
                    message_algebra=meta.get("algebra") or ast_obj.get("message_algebra"),
                    selected_sections=meta.get("selected_sections"),
                    sliced_lines_count=int(meta.get("sliced_lines_count") or 0),
                    role_count=len(ast_obj.get("roles") or []),
                    preskeleton_count=len(ast_obj.get("skeletons") or []),
                    roletran_passed=bool(s5.get("final_passed", run_entry.get("build_successful"))),
                    solver_passed=bool(s6.get("final_passed", run_entry.get("build_successful"))),
                    shapes_count=int(
                        (s6.get("shapes_analysis_from_shapes_txt") or {}).get("total_realized_shapes", 0)
                    ),
                    explored_skeletons_count=int(
                        (s6.get("exploration_telemetry_from_txt") or {}).get("total_explored_labels", 0)
                    ),
                    all_povs_multi_strand=qa.get("all_participant_povs_multi_strand"),
                    secrecy_proved=qa.get("all_secrecy_listeners_unrealized"),
                    schema_repairs=1 if s2.get("schema_self_correction_triggered") else 0,
                    roletran_repairs=int(s5.get("total_attempts") or 0),
                    solver_repairs=int(s6.get("total_attempts") or 0),
                    herald_options=ast_obj.get("herald_options"),
                    duration_seconds=float(traj_obj.get("duration_seconds") or 0.0),
                    cost_telemetry=traj_obj.get("cost_telemetry") or run_entry.get("cost_telemetry"),
                    scm_path=scm_p,
                    shapes_xhtml_path=xhtml_p,
                    trajectory_json_path=traj_path,
                    error_message=run_entry.get("error_message"),
                    security_findings=sec_f,
                )
            return len(self._read_existing_rows())

        return 0

    def prune_keep_ineligible_only(self) -> Tuple[int, int]:
        """Deletes all rows in `self.csv_path` EXCEPT ineligible RFCs (`is_eligible=False`).

        Allows starting a fresh synthesis run over eligible protocols while preserving cached
        Tier 0 / Stage 1 / Stage 2 ineligibility decisions so non-protocol RFCs are skipped in 0ms.

        Returns:
            Tuple of `(removed_eligible_rows_count, kept_ineligible_rows_count)`.
        """
        existing_rows = self._read_existing_rows()
        kept_rows: List[dict] = []
        removed_count = 0
        seen_ids = set()
        for row in existing_rows:
            is_elig_str = (row.get("is_eligible") or "").strip().lower()
            status_str = (row.get("status") or "").strip().upper()
            if is_elig_str == "false" or status_str == "INELIGIBLE":
                norm_id = self.normalize_rfc_id(row.get("rfc_id", ""))
                if norm_id and norm_id not in seen_ids:
                    seen_ids.add(norm_id)
                    row["rfc_id"] = norm_id
                    kept_rows.append(row)
            else:
                removed_count += 1
        self._write_all_rows(kept_rows)
        return removed_count, len(kept_rows)

    def log_run(
        self,
        rfc_id: str,
        is_eligible: bool,
        status: Optional[str] = None,
        quality_tier: Optional[str] = None,
        rejection_gate: Optional[str] = None,
        protocol_name: Optional[str] = None,
        message_algebra: Optional[str] = None,
        selected_sections: Optional[List[str]] = None,
        sliced_lines_count: int = 0,
        role_count: int = 0,
        preskeleton_count: int = 0,
        scm_lines_count: int = 0,
        roletran_passed: Optional[bool] = None,
        solver_passed: Optional[bool] = None,
        shapes_count: int = 0,
        explored_skeletons_count: int = 0,
        all_povs_multi_strand: Optional[bool] = None,
        secrecy_proved: Optional[bool] = None,
        zero_shot_passed: Optional[bool] = None,
        schema_repairs: int = 0,
        roletran_repairs: int = 0,
        solver_repairs: int = 0,
        total_repairs: Optional[int] = None,
        total_completion_steps: Optional[int] = None,
        searcher_invocations: int = 0,
        herald_options: Optional[List[str]] = None,
        duration_seconds: float = 0.0,
        cost_telemetry: Optional[dict] = None,
        router_model: Optional[str] = None,
        extraction_model: Optional[str] = None,
        query_model: Optional[str] = None,
        repair_model: Optional[str] = None,
        scm_path: Optional[Path] = None,
        shapes_xhtml_path: Optional[Path] = None,
        trajectory_json_path: Optional[Path] = None,
        error_message: Optional[str] = None,
        security_findings: Optional[Dict[str, Any]] = None,
    ) -> None:
        now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        norm_rfc_id = self.normalize_rfc_id(rfc_id)
        sec_str = ";".join(selected_sections) if selected_sections else ""
        herald_str = ";".join(herald_options) if herald_options else ""

        # Resolve high-level status if not explicitly passed
        resolved_status = status
        if not resolved_status:
            if not is_eligible:
                resolved_status = "INELIGIBLE"
            elif solver_passed:
                resolved_status = "VERIFIED"
            elif roletran_passed:
                resolved_status = "PARTIAL"
            else:
                resolved_status = "FAILED"

        resolved_tier = quality_tier or ("INELIGIBLE" if not is_eligible else "REJECTED")
        computed_total_repairs = (
            total_repairs
            if total_repairs is not None
            else (int(schema_repairs) + int(roletran_repairs) + int(solver_repairs))
        )
        computed_total_steps = (
            total_completion_steps
            if total_completion_steps is not None
            else ((1 + int(schema_repairs) + int(roletran_repairs) + int(solver_repairs)) if is_eligible else 0)
        )
        resolved_zero_shot = (
            zero_shot_passed
            if zero_shot_passed is not None
            else (bool(solver_passed) and computed_total_repairs == 0)
        )

        # Auto-compute scm_lines_count if scm_path exists and wasn't explicitly passed
        effective_scm_lines = scm_lines_count
        if effective_scm_lines == 0 and scm_path and Path(scm_path).exists():
            try:
                effective_scm_lines = len(
                    Path(scm_path).read_text(encoding="utf-8", errors="ignore").splitlines()
                )
            except Exception:
                effective_scm_lines = 0

        # Auto-hydrate security_findings from trajectory_json_path if not explicitly passed
        eff_sec = security_findings
        if not eff_sec and trajectory_json_path and Path(trajectory_json_path).exists():
            try:
                t_data = json.loads(Path(trajectory_json_path).read_text(encoding="utf-8", errors="ignore"))
                eff_sec = t_data.get("security_findings") or (t_data.get("quality_assessment") or {}).get("security_findings")
                if not eff_sec:
                    from src.verification_engine.trajectory_metadata_exporter import compute_security_findings
                    s6_t = t_data.get("stage6_cpsa4_solver") or {}
                    fin_t = t_data.get("final_verified_output") or {}
                    eff_sec = compute_security_findings(
                        shapes_analysis=s6_t.get("shapes_analysis_from_shapes_txt") or {},
                        exploration_telemetry=s6_t.get("exploration_telemetry_from_txt") or {},
                        sas_formulas=fin_t.get("shape_analysis_sentences") or [],
                    )
            except Exception:
                eff_sec = None
        eff_sec = eff_sec or {}

        disagreed_list = eff_sec.get("parameter_disagreements") or []
        disagreed_summary_parts = []
        for dp in disagreed_list:
            if isinstance(dp, dict):
                disagreed_summary_parts.append(
                    f"{dp.get('pov_role', '?')}->{dp.get('peer_role', '?')}:{dp.get('parameter', '?')}({dp.get('pov_value', '?')}!={dp.get('peer_value', '?')})"
                )
        disagreed_summary_str = ";".join(disagreed_summary_parts)
        protected_str = ";".join(str(x) for x in (eff_sec.get("protected_secrets") or []))
        leaked_str = ";".join(str(x) for x in (eff_sec.get("leaked_secrets") or []))
        anomalies_list = eff_sec.get("vulnerabilities_and_anomalies") or []
        anomalies_str = " | ".join(str(x) for x in anomalies_list)
        auth_tests = eff_sec.get("authentication_tests_summary") or {}

        # Extract per-role model telemetry from cost_telemetry (or GLOBAL_COST_TRACKER)
        roles_data = (cost_telemetry or {}).get("roles", {})
        r_info = roles_data.get("router", {})
        e_info = roles_data.get("extraction", {})
        q_info = roles_data.get("query", {})
        p_info = roles_data.get("repair", {})

        tot_calls = int((cost_telemetry or {}).get("total_calls", 0))
        tot_tokens = int((cost_telemetry or {}).get("total_tokens", 0))
        tot_cost = float((cost_telemetry or {}).get("total_cost_usd", 0.0))

        new_row = {
            "timestamp": now_iso,
            "rfc_id": norm_rfc_id,
            "run_count": "1",
            "is_eligible": str(bool(is_eligible)),
            "status": resolved_status,
            "quality_tier": resolved_tier,
            "total_completion_steps": str(computed_total_steps),
            "zero_shot_passed": "" if not is_eligible else str(bool(resolved_zero_shot)),
            "schema_repairs": str(schema_repairs) if is_eligible else "0",
            "roletran_repairs": str(roletran_repairs) if is_eligible else "0",
            "solver_repairs": str(solver_repairs) if is_eligible else "0",
            "total_repairs": str(computed_total_repairs) if is_eligible else "0",
            "rejection_gate": rejection_gate or "",
            "protocol_name": protocol_name or "",
            "message_algebra": message_algebra or "",
            "selected_sections": sec_str,
            "sliced_lines_count": str(sliced_lines_count) if is_eligible else "0",
            "role_count": str(role_count) if is_eligible else "0",
            "preskeleton_count": str(preskeleton_count) if is_eligible else "0",
            "scm_lines_count": str(effective_scm_lines) if is_eligible else "0",
            "shapes_count": str(shapes_count) if is_eligible else "0",
            "explored_skeletons_count": str(explored_skeletons_count) if is_eligible else "0",
            "all_povs_multi_strand": "" if all_povs_multi_strand is None else str(bool(all_povs_multi_strand)),
            "secrecy_proved": "" if secrecy_proved is None else str(bool(secrecy_proved)),
            "role_executability": str(eff_sec.get("role_executability") or "") if is_eligible else "",
            "dead_roles_count": str(int(eff_sec.get("dead_roles_count", 0))) if (is_eligible and eff_sec) else ("0" if is_eligible else ""),
            "authentication_profile": str(eff_sec.get("authentication_profile") or "") if is_eligible else "",
            "parameter_agreement_status": str(eff_sec.get("parameter_agreement_status") or "") if is_eligible else "",
            "disagreed_parameters_count": str(len(disagreed_list)) if is_eligible else "0",
            "disagreed_parameters_summary": disagreed_summary_str if is_eligible else "",
            "role_reflection_status": str(eff_sec.get("role_reflection_status") or "") if is_eligible else "",
            "secrecy_status": str(eff_sec.get("secrecy_status") or "") if is_eligible else "",
            "protected_secrets": protected_str if is_eligible else "",
            "leaked_secrets": leaked_str if is_eligible else "",
            "defgoal_satisfaction_status": str(eff_sec.get("defgoal_satisfaction_status") or "") if is_eligible else "",
            "shape_analysis_sentences_count": str(int(eff_sec.get("shape_analysis_sentences_count", 0))) if is_eligible else "0",
            "encryption_tests_count": str(int(auth_tests.get("encryption_tests", 0))) if is_eligible else "0",
            "nonce_tests_count": str(int(auth_tests.get("nonce_tests", 0))) if is_eligible else "0",
            "channel_tests_count": str(int(auth_tests.get("channel_tests", 0))) if is_eligible else "0",
            "anomalies_count": str(len(anomalies_list)) if is_eligible else "0",
            "vulnerabilities_and_anomalies": anomalies_str if is_eligible else "",
            "searcher_invocations": str(searcher_invocations) if is_eligible else "0",
            "herald_options": herald_str,
            "duration_seconds": str(round(duration_seconds, 3)),
            "router_model": router_model or r_info.get("model") or "",
            "router_calls": str(int(r_info.get("calls", 0))),
            "router_tokens": str(int(r_info.get("total_tokens", 0))),
            "router_cost_usd": f"{float(r_info.get('cost_usd', 0.0)):.6f}",
            "extraction_model": extraction_model or e_info.get("model") or "",
            "extraction_calls": str(int(e_info.get("calls", 0))),
            "extraction_tokens": str(int(e_info.get("total_tokens", 0))),
            "extraction_cost_usd": f"{float(e_info.get('cost_usd', 0.0)):.6f}",
            "query_model": query_model or q_info.get("model") or "",
            "query_calls": str(int(q_info.get("calls", 0))),
            "query_tokens": str(int(q_info.get("total_tokens", 0))),
            "query_cost_usd": f"{float(q_info.get('cost_usd', 0.0)):.6f}",
            "repair_model": repair_model or p_info.get("model") or "",
            "repair_calls": str(int(p_info.get("calls", 0))),
            "repair_tokens": str(int(p_info.get("total_tokens", 0))),
            "repair_cost_usd": f"{float(p_info.get('cost_usd', 0.0)):.6f}",
            "total_calls": str(tot_calls),
            "total_tokens": str(tot_tokens),
            "total_cost_usd": f"{tot_cost:.6f}",
            "scm_path": str(scm_path) if scm_path else "",
            "shapes_xhtml_path": str(shapes_xhtml_path) if shapes_xhtml_path else "",
            "trajectory_json_path": str(trajectory_json_path) if trajectory_json_path else "",
            "error_message": error_message or "",
        }

        existing_rows = self._read_existing_rows()
        replaced = False
        updated_rows: List[dict] = []
        for row in existing_rows:
            row_id = self.normalize_rfc_id(row.get("rfc_id", ""))
            if row_id == norm_rfc_id:
                if not replaced:
                    try:
                        prev_count = int(row.get("run_count") or 1)
                    except (TypeError, ValueError):
                        prev_count = 1
                    new_row["run_count"] = str(prev_count + 1)
                    updated_rows.append(new_row)
                    replaced = True
                # Skip any older duplicate rows for this same rfc_id
            else:
                updated_rows.append(row)

        if not replaced:
            updated_rows.append(new_row)

        self._write_all_rows(updated_rows)
        try:
            from src.pipeline_events import GLOBAL_EVENT_BUS
            GLOBAL_EVENT_BUS.emit(
                "csv_updated",
                csv_path=str(self.csv_path),
                rfc_id=norm_rfc_id,
                status=resolved_status,
                quality_tier=resolved_tier,
                total_rows=len(updated_rows),
            )
        except Exception:
            pass
```

---

### `src/main_pipeline_orchestrator.py`

*sha256:`d896b2c29551` · 1404 lines · 62.3 KB (~15,958 tokens) · lang:`python`*

```python
"""Main Pipeline Orchestrator for RFC-to-CPSA Synthesis.

Coordinates the 6-stage synthesis pipeline for a single RFC document:
- Stage 1 (Document Intake): Tier 0 Header Filter, TOC Parsing, Tier 1 Applicability Gate,
  Exchange Section Routing, and Verbatim Section Slicing.
- Stage 2 (JSON CPSA Generation): Constrained Protocol Extraction with RAG grounding and 1-shot schema correction.
- Stage 3 (CPSA4json -> scm): CPSA JSON Serialization and Scheme S-Expression Emission (`cpsa4json`).
- Stage 4 (Roletran Check): Pre-Flight Executability Check (`cpsa4roletran` / `cpsa4 -l 1`).
- Stage 5 (Self-Healing Loop): Cycle-aware RAG diagnostic repair loop for pre-flight defects.
- Stage 6 (CPSA Compilation): MITRE CPSA compilation and shape realization (`make` / `cpsa4` / `cpsa4shapes` / `cpsa4graph`, 60s hard cap) with RAG self-healing.
"""

import datetime as dt
import hashlib
import json
import time
from pathlib import Path
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field

from src.code_generation.cpsa_scheme_emitter import emit_cpsa_scheme, sanitize_protocol_stem
from src.document_ingestion.handshake_section_router import route_handshake_sections
from src.document_ingestion.protocol_applicability_gate import evaluate_protocol_applicability
from src.document_ingestion.rfc_header_filter import filter_rfc_header
from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections
from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import (
    PipelineMetricsCSVLogger,
    configure_pipeline_logging,
    get_pipeline_logger,
)
from src.pipeline_events import GLOBAL_EVENT_BUS
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    PROMPT_COMPILER_REPAIR,
    PROMPT_PROTOCOL_EXTRACTION,
    PROMPT_RAG_QUERY_FORMULATION,
    resolve_prompt_model,
)
from src.semantic_extraction import constrained_protocol_extractor
from src.semantic_extraction.constrained_protocol_extractor import extract_protocol_specification
from src.system_config import SYSTEM_CONFIG
from src.verification_engine import compiler_diagnostic_repair
from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification
from src.verification_engine.mitre_build_orchestrator import (
    CPSABuildArtifacts,
    execute_mitre_make_build,
)
from src.verification_engine.snowball_autopsy import is_snowball_state_error
from src.verification_engine.roletran_executability_gate import (
    RoletranVerificationResult,
    verify_role_executability,
)
from src.verification_engine.trajectory_metadata_exporter import (
    update_run_metadata_index,
    write_trajectory_metadata_bundle,
)

logger = get_pipeline_logger("orchestrator")


class PipelineExecutionSummary(BaseModel):
    """Execution summary of an end-to-end RFC synthesis run."""

    rfc_id: str = Field(..., description="Target RFC identifier")
    protocol_name: Optional[str] = Field(None, description="Identified protocol name")
    is_eligible: bool = Field(..., description="Whether the RFC passed intake filtering")
    selected_sections: List[str] = Field(default_factory=list, description="RFC sections sliced for synthesis")
    sliced_lines_count: int = Field(default=0, description="Number of lines in the verbatim slice")
    roletran_passed: bool = Field(default=False, description="Whether static role executability passed")
    build_successful: bool = Field(default=False, description="Whether MITRE make build succeeded")
    build_artifacts: Optional[CPSABuildArtifacts] = Field(None, description="Generated verification artifacts")
    trajectory_json_path: Optional[Path] = Field(None, description="Path to the generated trajectory metadata JSON")
    quality_tier: Optional[str] = Field(None, description="Programmatic verification quality tier (GOLD/SILVER/BRONZE/REJECTED)")
    security_findings: Optional[dict] = Field(None, description="Formal CPSA security findings report")
    intake_rationale: Optional[str] = Field(None, description="Stage 1c applicability gate rationale")
    duration_seconds: float = Field(default=0.0, description="Total pipeline execution time")
    cost_usd: float = Field(default=0.0, description="Total estimated LLM cost in USD for this RFC")
    cost_telemetry: dict = Field(default_factory=dict, description="Per-role token and USD cost breakdown")
    error_message: Optional[str] = Field(None, description="Diagnostic error if pipeline halted")


def _compact_diagnostic_headline(diag: Optional[str]) -> str:
    """Strips multi-line Snowball Autopsy blocks for concise console/CSV summaries while preserving the primary error."""
    if not diag:
        return ""
    marker = "=== CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT"
    if marker in diag:
        head = diag.split(marker, 1)[0].strip()
        first_line = head.splitlines()[0].strip() if head else "CPSA state-space snowball timeout"
        return f"{first_line} [Snowball Autopsy attached in trajectory/RAG tab]"
    return diag


def _extract_rfc_abstract(raw_rfc_text: str) -> str:
    """Extracts the abstract section from the top 120 lines of an RFC document."""
    lines = raw_rfc_text.splitlines()
    for line_idx, line in enumerate(lines[:120]):
        if line.strip().lower() == "abstract":
            return "\n".join(lines[line_idx + 1 : line_idx + 35])
    return ""


def _read_scm_safe(scm_path: Optional[Path]) -> Optional[str]:
    if scm_path and scm_path.exists():
        return scm_path.read_text(encoding="utf-8", errors="replace")
    return None


def _compute_ast_hash(spec: CPSAProtocolSpecification) -> str:
    """Computes a canonical SHA-256 hash of a protocol AST excluding cosmetic prose fields
    (`herald_comment`, `ineligibility_reason`, `description`, `comment`, `rfc_field`) so text variations
    across repair passes never mask an AST cycle.
    """
    payload = spec.model_dump(exclude={"herald_comment", "ineligibility_reason"})
    for role in payload.get("roles", []):
        role.pop("description", None)
        role.pop("comment", None)
        for v in role.get("variables", []):
            v.pop("description", None)
            v.pop("rfc_field", None)
        for ev in role.get("trace", []):
            ev.pop("description", None)
    for skel in payload.get("skeletons", []):
        skel.pop("description", None)
        skel.pop("comment", None)
        for v in skel.get("variables", []):
            v.pop("description", None)
            v.pop("rfc_field", None)
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def _run_roletran_self_healing_loop(
    protocol_ast: CPSAProtocolSpecification,
    scm_path: Path,
    target_output_dir: Path,
    verbatim_slice: str,
    repair_model_override: Optional[str] = None,
    query_model_override: Optional[str] = None,
) -> Tuple[CPSAProtocolSpecification, Path, RoletranVerificationResult, dict]:
    """Executes Stage 4 Roletran Check and Stage 5 Self-Healing Loop with cycle-aware RAG repair."""
    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=4,
        stage_name="Roletran Check",
        model="cpsa4roletran + cpsa4 -l 1",
    )
    roletran_result = verify_role_executability(scm_path)
    initial_passed = roletran_result.is_executable
    if initial_passed:
        GLOBAL_EVENT_BUS.emit("stage_completed", stage=4, status="passed", model="cpsa4roletran + cpsa4 -l 1")
    else:
        live_repair = resolve_prompt_model(PROMPT_COMPILER_REPAIR, repair_model_override)
        live_query = resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION, query_model_override)
        GLOBAL_EVENT_BUS.emit(
            "stage_started",
            stage=5,
            stage_name="Self-Healing Loop",
            model=f"{live_repair} (RAG: {live_query})",
        )
    attempt = 0
    seen_roletran_hashes = set()
    prev_roletran_diag: Optional[str] = None
    max_attempts = SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS
    repair_attempts_log: List[dict] = []
    stable_stem = scm_path.stem

    while not roletran_result.is_executable and attempt < max_attempts:
        attempt += 1
        ast_hash = _compute_ast_hash(protocol_ast)
        cycle_detected = ast_hash in seen_roletran_hashes
        seen_roletran_hashes.add(ast_hash)

        rejected_ast_snapshot = protocol_ast.model_dump()
        rejected_scm_snapshot = _read_scm_safe(scm_path)
        failed_stderr = roletran_result.raw_stderr
        failed_diag = roletran_result.error_diagnostic
        use_searcher = bool(
            attempt >= 3
            or cycle_detected
            or (attempt == 2 and failed_diag and failed_diag == prev_roletran_diag)
        )
        prev_roletran_diag = failed_diag

        live_repair = resolve_prompt_model(PROMPT_COMPILER_REPAIR, repair_model_override)
        live_query = resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION, query_model_override)
        GLOBAL_EVENT_BUS.emit(
            "repair_attempt",
            stage=5,
            attempt=attempt,
            max_attempts=max_attempts,
            diagnostic=roletran_result.error_diagnostic,
            cycle_detected=cycle_detected,
            model=live_repair,
            query_model=live_query if use_searcher else "Pinned CPSA Header (Direct)",
        )

        logger.warning(
            "Roletran check failed on attempt %d/%d (cycle=%s, searcher=%s): %s. Initiating self-healing repair...",
            attempt,
            max_attempts,
            cycle_detected,
            use_searcher,
            roletran_result.error_diagnostic,
        )
        try:
            prior_summaries = [
                f"Attempt #{entry.get('attempt_number')}: {entry.get('parsed_diagnostic') or entry.get('repair_exception')}"
                for entry in repair_attempts_log[-4:]
            ]
            protocol_ast = repair_protocol_specification(
                failing_spec=protocol_ast,
                error_diagnostic=roletran_result.error_diagnostic or "Executability verification failure",
                verbatim_slice=verbatim_slice,
                failure_stage="roletran",
                model=repair_model_override,
                query_model=query_model_override,
                cycle_detected=cycle_detected,
                use_agentic_searcher=use_searcher,
                prior_attempts=prior_summaries,
            )
            scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir, filename_prefix=stable_stem)
            GLOBAL_EVENT_BUS.emit(
                "stage_completed",
                stage=3,
                scm_path=str(scm_path),
                ast=protocol_ast.model_dump(),
            )
            GLOBAL_EVENT_BUS.emit(
                "compiler_check_started",
                stage=4,
                attempt=attempt,
                binary="cpsa4roletran + cpsa4 -l 1",
                timeout_seconds=SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS,
                model="cpsa4roletran + cpsa4 -l 1",
            )
            roletran_result = verify_role_executability(scm_path)
            repair_meta = compiler_diagnostic_repair.LAST_REPAIR_METADATA
            repair_attempts_log.append({
                "attempt_number": attempt,
                "cycle_detected": cycle_detected,
                "rejected_ast": rejected_ast_snapshot,
                "rejected_scm": rejected_scm_snapshot,
                "raw_stderr": failed_stderr,
                "parsed_diagnostic": failed_diag,
                "rag_query": repair_meta.get("rag_query"),
                "retrieved_chunk_ids": list(repair_meta.get("retrieved_chunk_ids", [])),
                "searcher_diagnosis": repair_meta.get("searcher_diagnosis"),
                "searcher_turns": list(repair_meta.get("searcher_turns", [])),
                "repaired_ast": protocol_ast.model_dump(),
                "repaired_scm": _read_scm_safe(scm_path),
                "passed_after_repair": roletran_result.is_executable,
            })
        except Exception as repair_error:
            logger.error("Self-healing repair exception on attempt %d: %s", attempt, repair_error)
            repair_attempts_log.append({
                "attempt_number": attempt,
                "cycle_detected": cycle_detected,
                "rejected_ast": rejected_ast_snapshot,
                "rejected_scm": rejected_scm_snapshot,
                "raw_stderr": failed_stderr,
                "parsed_diagnostic": failed_diag,
                "rag_query": compiler_diagnostic_repair.LAST_REPAIR_METADATA.get("rag_query"),
                "retrieved_chunk_ids": list(compiler_diagnostic_repair.LAST_REPAIR_METADATA.get("retrieved_chunk_ids", [])),
                "repaired_ast": None,
                "repaired_scm": None,
                "repair_exception": str(repair_error),
                "passed_after_repair": False,
            })
            time.sleep(2)
            continue

    if roletran_result.is_executable:
        logger.info("Roletran executability check passed.")
        GLOBAL_EVENT_BUS.emit("stage_completed", stage=5, status="passed", attempts=attempt)
    else:
        logger.warning(
            "Roletran pre-flight executability check unfulfilled (%s). Proceeding directly to MITRE CPSA solver verification...",
            roletran_result.error_diagnostic,
        )
        GLOBAL_EVENT_BUS.emit(
            "stage_completed",
            stage=5,
            status="unfulfilled",
            diagnostic=roletran_result.error_diagnostic,
            attempts=attempt,
        )

    stage5_record = {
        "validator_binary": roletran_result.validator_binary,
        "roletran_algebra_supported": roletran_result.roletran_algebra_supported,
        "initial_passed": initial_passed,
        "final_passed": roletran_result.is_executable,
        "total_attempts": attempt,
        "compiled_defproc_output": roletran_result.procedural_defproc_code,
        "repair_attempts": repair_attempts_log,
    }
    return protocol_ast, scm_path, roletran_result, stage5_record


def _run_mitre_solver_self_healing_loop(
    protocol_ast: CPSAProtocolSpecification,
    scm_path: Path,
    target_output_dir: Path,
    verbatim_slice: str,
    roletran_result: RoletranVerificationResult,
    repair_model_override: Optional[str] = None,
    query_model_override: Optional[str] = None,
) -> Tuple[CPSAProtocolSpecification, Path, Optional[CPSABuildArtifacts], int, Optional[str], dict]:
    """Executes Stage 6 CPSA Compilation and shape realization with cycle-aware RAG self-healing."""
    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=6,
        stage_name="CPSA Compilation",
        model="cpsa4 + cpsa4graph",
    )
    artifacts: Optional[CPSABuildArtifacts] = None
    build_attempt = 0
    last_build_error: Optional[str] = None
    prev_solver_diag: Optional[str] = None
    seen_solver_hashes = set()
    # If Stage 5 already exhausted its full repair budget (`not roletran_result.is_executable`),
    # try `execute_mitre_make_build` once on `build_attempt == 0` (since `cpsa4` is more permissive
    # than `cpsa4roletran`), and do not run another 10 redundant LLM repair attempts if `cpsa4` also fails.
    max_attempts = SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS if roletran_result.is_executable else 0
    solver_attempts_log: List[dict] = []
    stable_stem = scm_path.stem

    while build_attempt <= max_attempts:
        try:
            if build_attempt > 0 and not roletran_result.is_executable and roletran_result.roletran_algebra_supported:
                raise RuntimeError(
                    f"Pre-flight roletran check rejected repaired model (<15ms syntax/executability gate): "
                    f"{roletran_result.error_diagnostic}"
                )
            GLOBAL_EVENT_BUS.emit(
                "compiler_check_started",
                stage=6,
                attempt=build_attempt,
                binary="cpsa4 + cpsa4graph",
                timeout_seconds=SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS,
                model="cpsa4 + cpsa4graph",
            )
            artifacts = execute_mitre_make_build(scm_path, target_output_dir)
            if artifacts.winning_herald_options:
                protocol_ast.herald_options = list(artifacts.winning_herald_options)
            if solver_attempts_log:
                solver_attempts_log[-1]["passed_after_repair"] = True
            break
        except Exception as build_exc:
            last_build_error = str(build_exc)
            if build_attempt < max_attempts:
                build_attempt += 1
                ast_hash = _compute_ast_hash(protocol_ast)
                cycle_detected = ast_hash in seen_solver_hashes
                seen_solver_hashes.add(ast_hash)

                rejected_ast_snapshot = protocol_ast.model_dump()
                rejected_scm_snapshot = _read_scm_safe(scm_path)
                snowball_detected = is_snowball_state_error(last_build_error)
                use_searcher = bool(
                    snowball_detected
                    or build_attempt >= 3
                    or cycle_detected
                    or (build_attempt == 2 and last_build_error and last_build_error == prev_solver_diag)
                )
                prev_solver_diag = last_build_error

                live_repair = resolve_prompt_model(PROMPT_COMPILER_REPAIR, repair_model_override)
                live_query = resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION, query_model_override)
                GLOBAL_EVENT_BUS.emit(
                    "repair_attempt",
                    stage=6,
                    attempt=build_attempt,
                    max_attempts=max_attempts,
                    diagnostic=last_build_error,
                    cycle_detected=cycle_detected,
                    model=live_repair,
                    query_model=live_query if use_searcher else "Pinned CPSA Header (Direct)",
                )

                logger.warning(
                    "MITRE make build failed (attempt %d/%d, cycle=%s, searcher=%s): %s. Initiating self-healing repair...",
                    build_attempt,
                    max_attempts,
                    cycle_detected,
                    use_searcher,
                    _compact_diagnostic_headline(last_build_error),
                )
                try:
                    combined_diagnostic = last_build_error
                    if not roletran_result.is_executable and roletran_result.error_diagnostic:
                        combined_diagnostic = (
                            f"MITRE CPSA make / solver failure:\n{last_build_error}\n\n"
                            f"Pre-flight Roletran Executability Diagnostic:\n{roletran_result.error_diagnostic}"
                        )

                    prior_solver_summaries = [
                        f"Attempt #{entry.get('attempt_number')}: {_compact_diagnostic_headline(entry.get('parsed_diagnostic') or entry.get('repair_exception') or '')}"
                        for entry in solver_attempts_log[-4:]
                    ]
                    protocol_ast = repair_protocol_specification(
                        failing_spec=protocol_ast,
                        error_diagnostic=combined_diagnostic,
                        verbatim_slice=verbatim_slice,
                        failure_stage="solver",
                        model=repair_model_override,
                        query_model=query_model_override,
                        cycle_detected=cycle_detected,
                        use_agentic_searcher=use_searcher,
                        prior_attempts=prior_solver_summaries,
                    )
                    scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir, filename_prefix=stable_stem)
                    GLOBAL_EVENT_BUS.emit(
                        "stage_completed",
                        stage=3,
                        scm_path=str(scm_path),
                        ast=protocol_ast.model_dump(),
                    )
                    roletran_result = verify_role_executability(scm_path)
                    if not roletran_result.is_executable:
                        logger.warning(
                            "Repaired spec failed roletran executability: %s",
                            roletran_result.error_diagnostic,
                        )
                    repair_meta = compiler_diagnostic_repair.LAST_REPAIR_METADATA
                    solver_attempts_log.append({
                        "attempt_number": build_attempt,
                        "cycle_detected": cycle_detected,
                        "rejected_ast": rejected_ast_snapshot,
                        "rejected_scm": rejected_scm_snapshot,
                        "raw_stderr": last_build_error,
                        "parsed_diagnostic": combined_diagnostic,
                        "rag_query": repair_meta.get("rag_query"),
                        "retrieved_chunk_ids": list(repair_meta.get("retrieved_chunk_ids", [])),
                        "repaired_ast": protocol_ast.model_dump(),
                        "repaired_scm": _read_scm_safe(scm_path),
                        "passed_after_repair": False,
                    })
                except Exception as repair_error:
                    logger.error("Build self-healing exception on attempt %d: %s", build_attempt, repair_error)
                    solver_attempts_log.append({
                        "attempt_number": build_attempt,
                        "cycle_detected": cycle_detected,
                        "rejected_ast": rejected_ast_snapshot,
                        "rejected_scm": rejected_scm_snapshot,
                        "raw_stderr": last_build_error,
                        "parsed_diagnostic": last_build_error,
                        "rag_query": compiler_diagnostic_repair.LAST_REPAIR_METADATA.get("rag_query"),
                        "retrieved_chunk_ids": list(compiler_diagnostic_repair.LAST_REPAIR_METADATA.get("retrieved_chunk_ids", [])),
                        "repaired_ast": None,
                        "repaired_scm": None,
                        "repair_exception": str(repair_error),
                        "passed_after_repair": False,
                    })
                    time.sleep(2)
                    continue
            else:
                break

    stage6_record = {
        "validator_binary": "cpsa4",
        "initial_passed": build_attempt == 0 and artifacts is not None,
        "final_passed": artifacts is not None,
        "total_attempts": build_attempt,
        "repair_attempts": solver_attempts_log,
    }
    return protocol_ast, scm_path, artifacts, build_attempt, last_build_error, stage6_record


def run_rfc_translation_pipeline(
    rfc_file_path: Path,
    output_dir: Optional[Path] = None,
    router_model: Optional[str] = None,
    extraction_model: Optional[str] = None,
    repair_model: Optional[str] = None,
    query_model: Optional[str] = None,
    run_root_dir: Optional[Path] = None,
    csv_path: Optional[Path] = None,
) -> PipelineExecutionSummary:
    """Executes the end-to-end RFC to formally verified MITRE CPSA synthesis pipeline."""
    start_time = time.time()
    rfc_id = rfc_file_path.stem.upper()

    if output_dir is not None:
        target_output_dir = output_dir
        effective_run_root = run_root_dir or output_dir.parent
    else:
        run_ts = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        effective_run_root = run_root_dir or (SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR / f"run_{run_ts}")
        target_output_dir = effective_run_root / rfc_file_path.stem.lower()

    # Configure console/global logger first; defer creating per-RFC output directory and run.log
    # until the RFC passes Stage 1a/1c eligibility so batch runs don't create 9,400+ empty folders.
    configure_pipeline_logging(run_log_file=None)
    effective_csv_path = csv_path or (effective_run_root / "pipeline_runs.csv")
    csv_recorder = PipelineMetricsCSVLogger(csv_path=effective_csv_path)
    repair_override = repair_model or extraction_model
    active_router_model = resolve_prompt_model(PROMPT_APPLICABILITY_GATE, router_model)
    active_extraction_model = resolve_prompt_model(PROMPT_PROTOCOL_EXTRACTION, extraction_model)
    active_repair_model = resolve_prompt_model(PROMPT_COMPILER_REPAIR, repair_override)
    active_query_model = resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION, query_model)

    logger.info("================================================================")
    logger.info("Starting RFC-LLM Synthesis Pipeline for: %s", rfc_file_path.name)
    logger.info("================================================================")

    from src.cost_tracker import GLOBAL_COST_TRACKER
    GLOBAL_COST_TRACKER.start_rfc(
        rfc_id=rfc_id,
        router_model=active_router_model,
        extraction_model=active_extraction_model,
        query_model=active_query_model,
        repair_model=active_repair_model,
    )
    GLOBAL_EVENT_BUS.set_run_directory(effective_run_root, is_live=True, csv_path=effective_csv_path)
    GLOBAL_EVENT_BUS.start_rfc(rfc_id=rfc_id, rfc_file=rfc_file_path.name)
    GLOBAL_EVENT_BUS.emit(
        "pipeline_started",
        rfc_id=rfc_id,
        rfc_file=rfc_file_path.name,
        router_model=active_router_model,
        extraction_model=active_extraction_model,
        repair_model=active_repair_model,
        query_model=active_query_model,
    )

    if not rfc_file_path.exists():
        error_msg = f"RFC source file not found: {rfc_file_path}"
        logger.error(error_msg)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=error_msg)
        return PipelineExecutionSummary(rfc_id=rfc_id, is_eligible=False, error_message=error_msg)

    with open(rfc_file_path, "r", encoding="utf-8", errors="ignore") as rfc_file:
        raw_rfc_text = rfc_file.read()

    # -------------------------------------------------------------------------
    # STAGE 1a: Tier 0 Header Filter (Document Intake)
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=1,
        stage_name="Document Intake",
        model=active_router_model,
    )
    header_filter_result = filter_rfc_header(raw_rfc_text)
    if not header_filter_result.is_eligible:
        elapsed = time.time() - start_time
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            status="INELIGIBLE",
            quality_tier="INELIGIBLE",
            rejection_gate="Tier 0 Header Filter",
            protocol_name=header_filter_result.title,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            error_message=header_filter_result.disqualification_reason,
        )
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=header_filter_result.rfc_id or rfc_id,
            protocol_name=header_filter_result.title,
            rfc_dir=target_output_dir,
            scm_path=None,
            trajectory_json_path=None,
            quality_tier="INELIGIBLE",
            is_eligible=False,
            build_successful=False,
            error_message=header_filter_result.disqualification_reason,
            rejection_gate="Tier 0 Header Filter",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.register_filtered_rfc(
            rfc_id=header_filter_result.rfc_id or rfc_id,
            title=header_filter_result.title or rfc_file_path.name,
            gate="Tier 0 Header Filter",
            reason=header_filter_result.disqualification_reason or "Disqualified by Tier 0 header filter",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, reason=header_filter_result.disqualification_reason)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            is_eligible=False,
            duration_seconds=elapsed,
            error_message=header_filter_result.disqualification_reason,
        )

    rfc_number_str = header_filter_result.rfc_id or rfc_id
    protocol_title = header_filter_result.title or "Unknown Protocol"

    # -------------------------------------------------------------------------
    # STAGE 1b: Full TOC Parsing & Abstract Extraction
    # -------------------------------------------------------------------------
    toc_entries = parse_table_of_contents(raw_rfc_text)
    abstract_text = _extract_rfc_abstract(raw_rfc_text)

    # -------------------------------------------------------------------------
    # STAGE 1c: Tier 1 Applicability Gate
    # -------------------------------------------------------------------------
    applicability_report = evaluate_protocol_applicability(
        rfc_id=rfc_number_str,
        title=protocol_title,
        category=header_filter_result.category or "Unknown",
        abstract=abstract_text,
        toc_entries=toc_entries,
        model=router_model,
    )

    if not applicability_report.is_cryptographic_protocol:
        elapsed = time.time() - start_time
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            status="INELIGIBLE",
            quality_tier="INELIGIBLE",
            rejection_gate="Stage 1c Applicability Gate",
            protocol_name=applicability_report.protocol_name or protocol_title,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            error_message=f"Ineligible: {applicability_report.rationale}",
        )
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=rfc_number_str,
            protocol_name=applicability_report.protocol_name or protocol_title,
            rfc_dir=target_output_dir,
            scm_path=None,
            trajectory_json_path=None,
            quality_tier="INELIGIBLE",
            is_eligible=False,
            build_successful=False,
            error_message=applicability_report.rationale,
            rejection_gate="Stage 1c Applicability Gate",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.register_filtered_rfc(
            rfc_id=rfc_number_str,
            title=applicability_report.protocol_name or protocol_title,
            gate="Stage 1c Applicability Gate",
            reason=applicability_report.rationale or "Disqualified by Stage 1c applicability gate",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, reason=applicability_report.rationale)
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix="Ineligible RFC Cost"))
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=applicability_report.protocol_name or protocol_title,
            is_eligible=False,
            duration_seconds=elapsed,
            cost_usd=float(rfc_cost_summary.get("total_cost_usd", 0.0)),
            cost_telemetry=rfc_cost_summary,
            error_message=applicability_report.rationale,
        )

    # Eligible cryptographic protocol confirmed: create per-RFC output directory, run.log, and numbered tab
    target_output_dir.mkdir(parents=True, exist_ok=True)
    run_log_path = target_output_dir / "run.log"
    configure_pipeline_logging(run_log_file=run_log_path)
    final_protocol_name = applicability_report.protocol_name or protocol_title
    intake_rationale = applicability_report.rationale
    eligible_rationale_msg = f"Eligible: {intake_rationale}" if intake_rationale else None
    tab_index = GLOBAL_EVENT_BUS.register_accepted_tab(
        rfc_id=rfc_number_str,
        protocol_name=final_protocol_name,
        rfc_dir=target_output_dir,
        rfc_title=protocol_title,
        intake_rationale=intake_rationale,
    )
    logger.info("Eligible Cryptographic Protocol Confirmed [Tab #%d]: %s (%s)", tab_index, rfc_number_str, final_protocol_name)
    logger.info("Output Directory: %s", target_output_dir)

    GLOBAL_EVENT_BUS.emit("stage_completed", stage=1, protocol_name=final_protocol_name, rfc_id=rfc_number_str, tab_index=tab_index)

    # -------------------------------------------------------------------------
    # STAGE 1d & 1e: Exchange Section Routing & Verbatim Slicing
    # -------------------------------------------------------------------------
    target_sections = route_handshake_sections(
        rfc_id=rfc_number_str,
        protocol_name=final_protocol_name,
        toc_entries=toc_entries,
        model=router_model,
    )

    try:
        verbatim_slice = slice_verbatim_sections(raw_rfc_text, target_sections)
        if not verbatim_slice.strip():
            raise ValueError(f"Verbatim section slice for {target_sections} produced 0 non-empty lines")
    except Exception as slice_exc:
        elapsed = time.time() - start_time
        error_msg = f"Section slicing failed: {slice_exc}"
        csv_error_msg = f"{error_msg} | {eligible_rationale_msg}" if eligible_rationale_msg else error_msg
        logger.error(error_msg)
        empty_stage2 = {
            "schema_self_correction_triggered": False,
            "schema_validation_error": error_msg,
            "initial_ast": None,
            "initial_scm": None,
        }
        empty_stage5 = {
            "validator_binary": "cpsa4roletran",
            "roletran_algebra_supported": True,
            "initial_passed": False,
            "final_passed": False,
            "total_attempts": 0,
            "compiled_defproc_output": None,
            "repair_attempts": [],
        }
        empty_stage6 = {
            "validator_binary": "cpsa4",
            "initial_passed": False,
            "final_passed": False,
            "total_attempts": 0,
            "repair_attempts": [],
        }
        trajectory_path = write_trajectory_metadata_bundle(
            output_dir=target_output_dir,
            rfc_id=rfc_number_str,
            rfc_title=protocol_title,
            protocol_name=final_protocol_name,
            participating_principals=applicability_report.participating_principals,
            selected_sections=target_sections,
            verbatim_slice="",
            duration_seconds=elapsed,
            stage2_record=empty_stage2,
            stage5_record=empty_stage5,
            stage6_record=empty_stage6,
            final_spec=None,
            final_scm_path=None,
            trace_txt_path=None,
            shapes_txt_path=None,
            solver_passed=False,
            intake_rationale=intake_rationale,
        )
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=rfc_number_str,
            protocol_name=final_protocol_name,
            rfc_dir=target_output_dir,
            scm_path=None,
            trajectory_json_path=trajectory_path,
            quality_tier="REJECTED",
            is_eligible=True,
            build_successful=False,
            error_message=csv_error_msg,
            tab_index=tab_index,
            intake_rationale=intake_rationale,
        )
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            status="FAILED",
            quality_tier="REJECTED",
            protocol_name=final_protocol_name,
            selected_sections=target_sections,
            sliced_lines_count=0,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            trajectory_json_path=trajectory_path,
            error_message=csv_error_msg,
        )
        GLOBAL_EVENT_BUS.update_accepted_tab(
            tab_index,
            status="FAILED",
            quality_tier="REJECTED",
            duration_seconds=round(elapsed, 2),
            cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
            cost_telemetry=rfc_cost_summary,
            trajectory_path=str(trajectory_path),
            error_message=error_msg,
            intake_rationale=intake_rationale,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, error_message=error_msg)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=error_msg)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_protocol_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=0,
            trajectory_json_path=trajectory_path,
            quality_tier="REJECTED",
            intake_rationale=intake_rationale,
            duration_seconds=elapsed,
            cost_usd=float(rfc_cost_summary.get("total_cost_usd", 0.0)),
            cost_telemetry=rfc_cost_summary,
            error_message=error_msg,
        )

    slice_lines_count = len(verbatim_slice.splitlines())

    slice_file = target_output_dir / "verbatim_slice.txt"
    with open(slice_file, "w", encoding="utf-8") as slice_handle:
        slice_handle.write(verbatim_slice)

    GLOBAL_EVENT_BUS.update_accepted_tab(tab_index, slice_path=str(slice_file))
    GLOBAL_EVENT_BUS.emit(
        "slice_ready",
        sections=target_sections,
        line_count=slice_lines_count,
        slice_path=str(slice_file),
    )

    # -------------------------------------------------------------------------
    # STAGE 2: JSON CPSA Generation
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=2,
        stage_name="JSON CPSA Generation",
        model=resolve_prompt_model(PROMPT_PROTOCOL_EXTRACTION, extraction_model),
    )
    try:
        protocol_ast = extract_protocol_specification(
            verbatim_slice=verbatim_slice,
            protocol_name=final_protocol_name,
            principals=applicability_report.participating_principals,
            model=extraction_model,
        )
        # Immediately persist Stage 2 AST checkpoint to disk before Stage 3 (cpsa4json) runs
        initial_ast_path = target_output_dir / "initial_ast.json"
        initial_ast_path.write_text(protocol_ast.model_dump_json(indent=2), encoding="utf-8")
        GLOBAL_EVENT_BUS.emit(
            "stage_completed",
            stage=2,
            roles_count=len(protocol_ast.roles),
            skeletons_count=len(protocol_ast.skeletons),
            ast=protocol_ast.model_dump(),
        )
    except Exception as extraction_exc:
        elapsed = time.time() - start_time
        error_msg = f"Extraction failed: {extraction_exc}"
        csv_error_msg = f"{error_msg} | {eligible_rationale_msg}" if eligible_rationale_msg else error_msg
        logger.error(error_msg)
        extraction_meta = constrained_protocol_extractor.LAST_EXTRACTION_METADATA
        failed_stage2_record = {
            "schema_self_correction_triggered": bool(extraction_meta.get("schema_self_correction_triggered", False)),
            "schema_validation_error": extraction_meta.get("schema_validation_error") or str(extraction_exc),
            "initial_ast": None,
            "initial_scm": None,
        }
        empty_stage5 = {
            "validator_binary": "cpsa4roletran",
            "roletran_algebra_supported": True,
            "initial_passed": False,
            "final_passed": False,
            "total_attempts": 0,
            "compiled_defproc_output": None,
            "repair_attempts": [],
        }
        empty_stage6 = {
            "validator_binary": "cpsa4",
            "initial_passed": False,
            "final_passed": False,
            "total_attempts": 0,
            "repair_attempts": [],
        }
        trajectory_path = write_trajectory_metadata_bundle(
            output_dir=target_output_dir,
            rfc_id=rfc_number_str,
            rfc_title=protocol_title,
            protocol_name=final_protocol_name,
            participating_principals=applicability_report.participating_principals,
            selected_sections=target_sections,
            verbatim_slice=verbatim_slice,
            duration_seconds=elapsed,
            stage2_record=failed_stage2_record,
            stage5_record=empty_stage5,
            stage6_record=empty_stage6,
            final_spec=None,
            final_scm_path=None,
            trace_txt_path=None,
            shapes_txt_path=None,
            solver_passed=False,
            intake_rationale=intake_rationale,
        )
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=rfc_number_str,
            protocol_name=final_protocol_name,
            rfc_dir=target_output_dir,
            scm_path=None,
            trajectory_json_path=trajectory_path,
            quality_tier="REJECTED",
            is_eligible=True,
            build_successful=False,
            error_message=csv_error_msg,
            tab_index=tab_index,
            intake_rationale=intake_rationale,
        )
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        schema_repairs_stage2 = 1 if failed_stage2_record["schema_self_correction_triggered"] else 0
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            status="FAILED",
            quality_tier="REJECTED",
            protocol_name=final_protocol_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            schema_repairs=schema_repairs_stage2,
            total_repairs=schema_repairs_stage2,
            total_completion_steps=1 + schema_repairs_stage2,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            trajectory_json_path=trajectory_path,
            error_message=csv_error_msg,
        )
        logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix="RFC Run Cost"))
        GLOBAL_EVENT_BUS.update_accepted_tab(
            tab_index,
            status="FAILED",
            quality_tier="REJECTED",
            duration_seconds=round(elapsed, 2),
            cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
            cost_telemetry=rfc_cost_summary,
            trajectory_path=str(trajectory_path),
            error_message=error_msg,
            intake_rationale=intake_rationale,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=2, error_message=error_msg)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=error_msg)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_protocol_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            trajectory_json_path=trajectory_path,
            quality_tier="REJECTED",
            intake_rationale=intake_rationale,
            duration_seconds=elapsed,
            cost_usd=float(rfc_cost_summary.get("total_cost_usd", 0.0)),
            cost_telemetry=rfc_cost_summary,
            error_message=error_msg,
        )

    # -------------------------------------------------------------------------
    # STAGE 2b: Verbatim Slice Verification Gate (False-Positive Bailout)
    # -------------------------------------------------------------------------
    if (
        not protocol_ast.is_verifiable_protocol
        or not protocol_ast.roles
        or not protocol_ast.has_cryptographic_primitives()
    ):
        elapsed = time.time() - start_time
        raw_ineligible_reason = (
            protocol_ast.ineligibility_reason
            or "Stage 2 Verbatim Slice Gate: RFC slice contains no verifiable cryptographic message exchange."
        )
        ineligible_reason = (
            raw_ineligible_reason
            if raw_ineligible_reason.startswith("Ineligible:")
            else f"Ineligible: {raw_ineligible_reason}"
        )
        logger.warning(
            "Stage 2 Verbatim Slice Gate rejected '%s' (%s) with 0 repair loops: %s",
            rfc_number_str,
            final_protocol_name,
            ineligible_reason,
        )
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        extraction_meta = constrained_protocol_extractor.LAST_EXTRACTION_METADATA
        schema_repairs_stage2 = 1 if extraction_meta.get("schema_self_correction_triggered") else 0
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            status="INELIGIBLE",
            quality_tier="INELIGIBLE",
            rejection_gate="Stage 2 Verbatim Slice Gate",
            protocol_name=final_protocol_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            schema_repairs=schema_repairs_stage2,
            total_repairs=schema_repairs_stage2,
            total_completion_steps=1 + schema_repairs_stage2,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            error_message=ineligible_reason,
        )
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=rfc_number_str,
            protocol_name=final_protocol_name,
            rfc_dir=target_output_dir,
            scm_path=None,
            trajectory_json_path=None,
            quality_tier="INELIGIBLE",
            is_eligible=False,
            build_successful=False,
            error_message=ineligible_reason,
            tab_index=tab_index,
            rejection_gate="Stage 2 Verbatim Slice Gate",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.register_filtered_rfc(
            rfc_id=rfc_number_str,
            title=final_protocol_name,
            gate="Stage 2 Verbatim Slice Gate",
            reason=ineligible_reason,
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.update_accepted_tab(
            tab_index,
            status="INELIGIBLE",
            quality_tier="INELIGIBLE",
            duration_seconds=round(elapsed, 2),
            cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
            cost_telemetry=rfc_cost_summary,
            error_message=ineligible_reason,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=2, reason=ineligible_reason)
        logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix="Stage 2 Filtered RFC Cost"))
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_protocol_name,
            is_eligible=False,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            quality_tier="INELIGIBLE",
            duration_seconds=elapsed,
            cost_usd=float(rfc_cost_summary.get("total_cost_usd", 0.0)),
            cost_telemetry=rfc_cost_summary,
            error_message=ineligible_reason,
        )

    # -------------------------------------------------------------------------
    # STAGE 3: CPSA4json -> scm
    # -------------------------------------------------------------------------
    extraction_meta = constrained_protocol_extractor.LAST_EXTRACTION_METADATA
    stage2_record = {
        "schema_self_correction_triggered": bool(extraction_meta.get("schema_self_correction_triggered", False)),
        "schema_validation_error": extraction_meta.get("schema_validation_error"),
        "initial_ast": protocol_ast.model_dump(),
        "initial_scm": None,
    }
    stage5_record = {
        "validator_binary": "cpsa4roletran",
        "roletran_algebra_supported": True,
        "initial_passed": False,
        "final_passed": False,
        "total_attempts": 0,
        "compiled_defproc_output": None,
        "repair_attempts": [],
    }
    stage6_record = {
        "validator_binary": "cpsa4",
        "initial_passed": False,
        "final_passed": False,
        "total_attempts": 0,
        "repair_attempts": [],
    }
    scm_path: Optional[Path] = None
    artifacts: Optional[CPSABuildArtifacts] = None
    build_attempt = 0
    last_build_error = "Unknown compilation failure"

    GLOBAL_EVENT_BUS.emit(
        "stage_started",
        stage=3,
        stage_name="CPSA4json -> scm",
        model="cpsa_scheme_emitter.py",
    )
    try:
        scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir)
        stage2_record["initial_scm"] = _read_scm_safe(scm_path)
        GLOBAL_EVENT_BUS.update_accepted_tab(
            tab_index,
            protocol_name=protocol_ast.protocol_name or final_protocol_name,
            scm_path=str(scm_path),
        )
        GLOBAL_EVENT_BUS.emit("stage_completed", stage=3, scm_path=str(scm_path))

        # -------------------------------------------------------------------------
        # STAGE 4 & 5: Roletran Check (<15 ms) & Self-Healing Loop
        # -------------------------------------------------------------------------
        protocol_ast, scm_path, roletran_result, stage5_record = _run_roletran_self_healing_loop(
            protocol_ast=protocol_ast,
            scm_path=scm_path,
            target_output_dir=target_output_dir,
            verbatim_slice=verbatim_slice,
            repair_model_override=repair_override,
            query_model_override=query_model,
        )

        # -------------------------------------------------------------------------
        # STAGE 6: CPSA Compilation (60s cap) with RAG Self-Healing Loop
        # -------------------------------------------------------------------------
        protocol_ast, scm_path, artifacts, build_attempt, last_build_error, stage6_record = _run_mitre_solver_self_healing_loop(
            protocol_ast=protocol_ast,
            scm_path=scm_path,
            target_output_dir=target_output_dir,
            verbatim_slice=verbatim_slice,
            roletran_result=roletran_result,
            repair_model_override=repair_override,
            query_model_override=query_model,
        )
    except Exception as downstream_exc:
        last_build_error = f"Stage 3-6 toolchain error: {downstream_exc}"
        logger.error("Unhandled Stage 3-6 error for %s (%s): %s", rfc_number_str, final_protocol_name, downstream_exc)
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=3, error_message=last_build_error)

    elapsed = time.time() - start_time
    stem = scm_path.stem if scm_path is not None else sanitize_protocol_stem(protocol_ast.protocol_name or final_protocol_name)
    trace_txt_candidate = artifacts.trace_txt_path if artifacts else (target_output_dir / f"{stem}.txt")
    shapes_txt_candidate = artifacts.shapes_txt_path if artifacts else (target_output_dir / f"{stem}_shapes.txt")

    trajectory_path = write_trajectory_metadata_bundle(
        output_dir=target_output_dir,
        rfc_id=rfc_number_str,
        rfc_title=protocol_title,
        protocol_name=final_protocol_name,
        participating_principals=applicability_report.participating_principals,
        selected_sections=target_sections,
        verbatim_slice=verbatim_slice,
        duration_seconds=elapsed,
        stage2_record=stage2_record,
        stage5_record=stage5_record,
        stage6_record=stage6_record,
        final_spec=protocol_ast,
        final_scm_path=scm_path,
        trace_txt_path=trace_txt_candidate if trace_txt_candidate.exists() else None,
        shapes_txt_path=shapes_txt_candidate if shapes_txt_candidate.exists() else None,
        solver_passed=artifacts is not None,
        intake_rationale=intake_rationale,
    )

    quality_tier = "REJECTED"
    all_povs_multi_strand: Optional[bool] = None
    secrecy_proved: Optional[bool] = None
    explored_skeletons_count = 0
    sec_findings: dict = {}
    try:
        traj_data = json.loads(trajectory_path.read_text(encoding="utf-8"))
        qa = traj_data.get("quality_assessment", {})
        quality_tier = qa.get("quality_tier", "REJECTED")
        all_povs_multi_strand = qa.get("all_participant_povs_multi_strand")
        secrecy_proved = qa.get("all_secrecy_listeners_unrealized")
        sec_findings = traj_data.get("security_findings") or qa.get("security_findings") or {}
        explored_skeletons_count = int(
            traj_data.get("stage6_cpsa4_solver", {})
            .get("exploration_telemetry_from_txt", {})
            .get("total_explored_labels", 0)
        )
    except Exception:
        pass

    schema_repairs = 1 if stage2_record.get("schema_self_correction_triggered") else 0
    roletran_repairs = int(stage5_record.get("total_attempts", 0))
    solver_repairs = int(stage6_record.get("total_attempts", 0))
    total_repairs = schema_repairs + roletran_repairs + solver_repairs
    total_completion_steps = 1 + total_repairs
    all_repair_attempts = list(stage5_record.get("repair_attempts", [])) + list(
        stage6_record.get("repair_attempts", [])
    )
    searcher_invocations = sum(
        1
        for att in all_repair_attempts
        if att.get("rag_query") or att.get("retrieved_chunk_ids")
    )

    if artifacts is None:
        compact_err = _compact_diagnostic_headline(last_build_error)
        error_msg = f"MITRE make build failed after {build_attempt} repair attempts: {compact_err}"
        csv_error_msg = f"{error_msg} | {eligible_rationale_msg}" if eligible_rationale_msg else error_msg
        logger.error(error_msg)
        update_run_metadata_index(
            run_root_dir=effective_run_root,
            rfc_id=rfc_number_str,
            protocol_name=final_protocol_name,
            rfc_dir=target_output_dir,
            scm_path=scm_path,
            trajectory_json_path=trajectory_path,
            quality_tier=quality_tier,
            is_eligible=True,
            build_successful=False,
            error_message=csv_error_msg,
            tab_index=tab_index,
            security_findings=sec_findings,
            intake_rationale=intake_rationale,
        )
        rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            status="PARTIAL" if roletran_result.is_executable else "FAILED",
            quality_tier=quality_tier,
            protocol_name=final_protocol_name,
            message_algebra=protocol_ast.message_algebra,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            role_count=len(protocol_ast.roles),
            preskeleton_count=len(protocol_ast.skeletons),
            roletran_passed=roletran_result.is_executable,
            solver_passed=False,
            shapes_count=0,
            explored_skeletons_count=explored_skeletons_count,
            all_povs_multi_strand=all_povs_multi_strand,
            secrecy_proved=secrecy_proved,
            zero_shot_passed=False,
            schema_repairs=schema_repairs,
            roletran_repairs=roletran_repairs,
            solver_repairs=solver_repairs,
            total_repairs=total_repairs,
            total_completion_steps=total_completion_steps,
            searcher_invocations=searcher_invocations,
            herald_options=protocol_ast.herald_options,
            duration_seconds=elapsed,
            cost_telemetry=rfc_cost_summary,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            query_model=active_query_model,
            repair_model=active_repair_model,
            scm_path=scm_path,
            shapes_xhtml_path=None,
            trajectory_json_path=trajectory_path,
            error_message=csv_error_msg,
            security_findings=sec_findings,
        )
        logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix=f"Cost Summary ({rfc_id})"))
        GLOBAL_EVENT_BUS.update_accepted_tab(
            tab_index,
            protocol_name=protocol_ast.protocol_name or final_protocol_name,
            status="PARTIAL" if roletran_result.is_executable else "FAILED",
            quality_tier=quality_tier,
            total_attempts=total_repairs,
            duration_seconds=round(elapsed, 2),
            cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
            cost_telemetry=rfc_cost_summary,
            scm_path=str(scm_path),
            trajectory_path=str(trajectory_path),
            error_message=error_msg,
            security_findings=sec_findings,
            intake_rationale=intake_rationale,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=6, error_message=error_msg)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=error_msg)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_protocol_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            roletran_passed=roletran_result.is_executable,
            build_successful=False,
            trajectory_json_path=trajectory_path,
            quality_tier=quality_tier,
            security_findings=sec_findings,
            intake_rationale=intake_rationale,
            duration_seconds=elapsed,
            cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
            cost_telemetry=rfc_cost_summary,
            error_message=error_msg,
        )

    update_run_metadata_index(
        run_root_dir=effective_run_root,
        rfc_id=rfc_number_str,
        protocol_name=final_protocol_name,
        rfc_dir=target_output_dir,
        scm_path=scm_path,
        trajectory_json_path=trajectory_path,
        quality_tier=quality_tier,
        is_eligible=True,
        build_successful=True,
        error_message=eligible_rationale_msg,
        tab_index=tab_index,
        security_findings=sec_findings,
        intake_rationale=intake_rationale,
    )

    rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()
    GLOBAL_EVENT_BUS.update_accepted_tab(
        tab_index,
        protocol_name=protocol_ast.protocol_name or final_protocol_name,
        status="VERIFIED",
        quality_tier=quality_tier,
        total_attempts=total_repairs,
        shapes_count=artifacts.shapes_count,
        duration_seconds=round(elapsed, 2),
        cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
        cost_telemetry=rfc_cost_summary,
        scm_path=str(scm_path),
        trajectory_path=str(trajectory_path),
        shapes_xhtml=str(artifacts.shapes_graph_xhtml_path),
        error_message=eligible_rationale_msg,
        security_findings=sec_findings,
        intake_rationale=intake_rationale,
    )

    csv_recorder.log_run(
        rfc_id=rfc_id,
        is_eligible=True,
        status="VERIFIED",
        quality_tier=quality_tier,
        protocol_name=final_protocol_name,
        message_algebra=protocol_ast.message_algebra,
        selected_sections=target_sections,
        sliced_lines_count=slice_lines_count,
        role_count=len(protocol_ast.roles),
        preskeleton_count=len(protocol_ast.skeletons),
        roletran_passed=roletran_result.is_executable,
        solver_passed=True,
        shapes_count=artifacts.shapes_count,
        explored_skeletons_count=explored_skeletons_count,
        all_povs_multi_strand=all_povs_multi_strand,
        secrecy_proved=secrecy_proved,
        zero_shot_passed=(total_repairs == 0),
        schema_repairs=schema_repairs,
        roletran_repairs=roletran_repairs,
        solver_repairs=solver_repairs,
        total_repairs=total_repairs,
        total_completion_steps=total_completion_steps,
        searcher_invocations=searcher_invocations,
        herald_options=protocol_ast.herald_options,
        duration_seconds=elapsed,
        cost_telemetry=rfc_cost_summary,
        router_model=active_router_model,
        extraction_model=active_extraction_model,
        query_model=active_query_model,
        repair_model=active_repair_model,
        scm_path=scm_path,
        shapes_xhtml_path=artifacts.shapes_graph_xhtml_path,
        trajectory_json_path=trajectory_path,
        error_message=eligible_rationale_msg,
        security_findings=sec_findings,
    )

    logger.info("================================================================")
    logger.info("Pipeline Complete for %s in %.2fs! (Quality Tier: %s)", rfc_id, elapsed, quality_tier)
    if sec_findings:
        logger.info(
            "Security Findings: Auth=%s | Agreement=%s | Secrecy=%s | Anomalies=%s",
            sec_findings.get("authentication_profile", "N/A"),
            sec_findings.get("parameter_agreement_status", "N/A"),
            sec_findings.get("secrecy_status", "N/A"),
            sec_findings.get("anomalies_count", 0),
        )
    logger.info(GLOBAL_COST_TRACKER.format_cli_summary(rfc_cost_summary, prefix=f"Cost Summary ({rfc_id})"))
    logger.info("Generated: %s", artifacts.shapes_graph_xhtml_path)
    logger.info("Trajectory Metadata: %s", trajectory_path)
    logger.info("Master Run Index: %s", effective_run_root / "metadata_index.json")
    logger.info("================================================================")

    GLOBAL_EVENT_BUS.emit(
        "pipeline_completed",
        success=True,
        protocol_name=final_protocol_name,
        duration_seconds=elapsed,
        shapes_count=artifacts.shapes_count,
        quality_tier=quality_tier,
        security_findings=sec_findings,
        intake_rationale=intake_rationale,
        cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
        cost_telemetry=rfc_cost_summary,
        trajectory_json=str(trajectory_path),
        shapes_xhtml=str(artifacts.shapes_graph_xhtml_path),
        shapes_txt=str(artifacts.shapes_txt_path),
        scm_path=str(scm_path),
    )

    return PipelineExecutionSummary(
        rfc_id=rfc_id,
        protocol_name=final_protocol_name,
        is_eligible=True,
        selected_sections=target_sections,
        sliced_lines_count=slice_lines_count,
        roletran_passed=roletran_result.is_executable,
        build_successful=True,
        build_artifacts=artifacts,
        trajectory_json_path=trajectory_path,
        quality_tier=quality_tier,
        security_findings=sec_findings,
        intake_rationale=intake_rationale,
        duration_seconds=elapsed,
        cost_usd=round(float(rfc_cost_summary.get("total_cost_usd", 0.0)), 6),
        cost_telemetry=rfc_cost_summary,
        error_message=eligible_rationale_msg,
    )
```

---

### `src/pipeline.py`

*sha256:`59ac888002a9` · 593 lines · 24.5 KB (~6,269 tokens) · lang:`python`*

```python
"""Command-line interface for RFC-LLM synthesis pipeline supporting single RFCs and directory batching."""

import argparse
import csv
import datetime as dt
import json
import random
import re
import sys
import time
import webbrowser
from pathlib import Path
from typing import List, Optional, Set

from src.cost_tracker import GLOBAL_COST_TRACKER
from src.document_ingestion.rfc_header_filter import filter_rfc_header
from src.logging_config import PipelineMetricsCSVLogger
from src.main_pipeline_orchestrator import PipelineExecutionSummary, run_rfc_translation_pipeline
from src.pipeline_events import GLOBAL_EVENT_BUS
from src.system_config import SYSTEM_CONFIG
from src.visualizer.server import run_visualizer_in_background


def _print_cost_breakdown(cost_summary: dict, title: str = "COST & TOKEN TELEMETRY") -> None:
    """Prints a formatted breakdown of USD cost and tokens by model role."""
    roles = cost_summary.get("roles", {})
    role_labels = [
        ("router", "Router Model"),
        ("extraction", "Extraction Model"),
        ("query", "Query/Searcher Model"),
        ("repair", "Repair Model"),
    ]
    print(f"\n[{title}]")
    for role_key, label in role_labels:
        rb = roles.get(role_key, {})
        mod = rb.get("model") or "n/a"
        usd = float(rb.get("cost_usd", 0.0))
        calls = int(rb.get("calls", 0))
        toks = int(rb.get("total_tokens", 0))
        print(f" - {label:<20}: ${usd:.4f} ({calls} calls, {toks:,} tokens) [{mod}]")
    tot_usd = float(cost_summary.get("total_cost_usd", 0.0))
    tot_calls = int(cost_summary.get("total_calls", 0))
    tot_toks = int(cost_summary.get("total_tokens", 0))
    print(f" - {'Total Run Cost':<20}: ${tot_usd:.4f} ({tot_calls} calls, {tot_toks:,} tokens)")


def natural_rfc_sort_key(file_path: Path):
    """Sorts RFC files by integer number if present (e.g. rfc10 before rfc100)."""
    match = re.search(r"rfc(\d+)", file_path.stem.lower())
    if match:
        return (0, int(match.group(1)))
    return (1, file_path.name)


def get_completed_rfc_ids(csv_path: Optional[Path] = None) -> Set[str]:
    """Reads a pipeline_runs.csv ledger to retrieve RFC IDs that were already evaluated."""
    target_csv = csv_path or (SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv")
    if not target_csv.exists():
        return set()

    completed = set()
    try:
        with open(target_csv, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rfc_val = row.get("rfc_id", "").strip()
                if rfc_val:
                    # Normalize 'RFC 5246' or 'RFC5246' to 'RFC5246'
                    clean_id = rfc_val.upper().replace(" ", "").replace("_", "")
                    completed.add(clean_id)
    except Exception:
        pass
    return completed


def get_failed_rfc_ids(csv_path: Optional[Path] = None) -> Set[str]:
    """Reads a pipeline_runs.csv ledger to retrieve RFC IDs whose latest status is FAILED or PARTIAL."""
    target_csv = csv_path or (SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv")
    if not target_csv.exists():
        return set()

    failed = set()
    try:
        with open(target_csv, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rfc_val = row.get("rfc_id", "").strip()
                status_val = (row.get("status") or "").strip().upper()
                if rfc_val and status_val in {"FAILED", "PARTIAL"}:
                    clean_id = rfc_val.upper().replace(" ", "").replace("_", "")
                    failed.add(clean_id)
    except Exception:
        pass
    return failed


def main():
    parser = argparse.ArgumentParser(
        description="RFC-LLM: End-to-End Synthesis of Verified MITRE CPSA Models from IETF RFCs",
    )
    parser.add_argument(
        "target_path",
        type=str,
        nargs="*",
        help="One or more RFC text files (such as refrences/all_RFCs/rfc5246.txt) OR a directory containing RFCs",
    )
    parser.add_argument(
        "--view",
        type=str,
        default=None,
        help="Open an existing run directory (e.g. output/run_2026-10-28_16-03-11) or metadata_index.json in offline visualizer replay mode",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default=None,
        help="Directory to place synthesized models and build artifacts",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help="Global model identifier for all pipeline stages (e.g. 'gemini/gemini-3.5-flash-lite', 'ollama/qwen2.5:7b-instruct')",
    )
    parser.add_argument(
        "--router-model",
        type=str,
        default=None,
        help="Model identifier for document gatekeeper and TOC router",
    )
    parser.add_argument(
        "--extraction-model",
        type=str,
        default=None,
        help="Model identifier for Pydantic constrained semantic extraction",
    )
    parser.add_argument(
        "--repair-model",
        type=str,
        default=None,
        help="Model identifier for RAG self-healing compiler diagnostic repair",
    )
    parser.add_argument(
        "--query-model",
        type=str,
        default=None,
        help="Model identifier for RAG query formulation / conceptual abstraction",
    )
    parser.add_argument(
        "--no-visualize",
        action="store_true",
        help="Disable the live web dashboard visualizer (enabled by default)",
    )
    parser.add_argument(
        "--visualize",
        "-v",
        action="store_true",
        help="Ensure live web dashboard visualizer is enabled",
    )
    parser.add_argument(
        "--keep-alive",
        type=int,
        default=0,
        help="Seconds to keep visualizer server running after completion in non-interactive mode",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Web port for the live visualizer dashboard (default: 8080)",
    )
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=None,
        help="Maximum number of RFC files to scan when pointing to a directory",
    )
    parser.add_argument(
        "--target-eligible",
        "-e",
        type=int,
        default=None,
        help="Stop batch processing once N eligible cryptographic protocols have been synthesized",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="rfc*.txt",
        help="Glob pattern for discovering RFC files when scanning a directory (default: 'rfc*.txt')",
    )
    parser.add_argument(
        "--skip-completed",
        action="store_true",
        help="Skip RFCs that already have completed run entries in logs/pipeline_runs.csv",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Run only RFCs recorded in logs/pipeline_runs.csv with status FAILED or PARTIAL (overwriting their rows in-place)",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Randomly sample RFC files when pointing to a directory (useful with --limit)",
    )
    parser.add_argument(
        "--tier0-eligible-only",
        action="store_true",
        help="Pre-filter directory candidates using deterministic Tier 0 frontmatter check before applying --limit",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Path to an existing pipeline_runs.csv or older run directory to copy/seed into this new run's pipeline_runs.csv (source CSV is never modified)",
    )
    parser.add_argument(
        "--keep-ineligible",
        "--reset-eligible",
        dest="keep_ineligible",
        action="store_true",
        help="Prune the active run's pipeline_runs.csv by deleting all rows EXCEPT ineligible RFCs (is_eligible=False), and skip those ineligible RFCs when starting a new batch run",
    )

    args = parser.parse_args()

    # Offline Replay Mode (--view <run_dir>)
    if args.view:
        view_path = Path(args.view)
        if not view_path.exists():
            print(f"Error: Run directory or index does not exist: {view_path}", file=sys.stderr)
            sys.exit(1)

        overview = GLOBAL_EVENT_BUS.load_run_from_disk(view_path)
        if args.csv:
            src_csv = Path(args.csv)
            if src_csv.is_dir():
                src_csv = src_csv / "pipeline_runs.csv"
            if src_csv.exists():
                GLOBAL_EVENT_BUS.set_run_directory(
                    Path(overview.get("run_directory") or view_path),
                    is_live=False,
                    csv_path=src_csv,
                )
        server = run_visualizer_in_background(port=args.port)
        monitor_url = f"http://127.0.0.1:{server.port}"

        print(f"\n{'='*70}")
        print(f" [OFFLINE REPLAY MONITOR] Active at: {monitor_url}")
        print(f" - Run Directory   : {overview.get('run_directory')}")
        print(f" - Run Metrics CSV : {GLOBAL_EVENT_BUS.get_csv_path()}")
        print(f" - Accepted Tabs   : {len(overview.get('accepted_tabs', []))}")
        print(f" - Filtered / Skips: {overview.get('filtered_total', 0)}")
        print(f"{'='*70}\n")

        if not args.no_visualize:
            try:
                webbrowser.open(monitor_url)
            except Exception:
                pass

        if sys.stdin.isatty() and args.keep_alive <= 0:
            try:
                input("[OFFLINE REPLAY MONITOR] Press Enter to exit (server remains live until keypress)... ")
            except (EOFError, KeyboardInterrupt):
                pass
        else:
            wait_sec = args.keep_alive if args.keep_alive > 0 else 60
            print(f"[OFFLINE REPLAY MONITOR] Keeping server active for {wait_sec}s...")
            time.sleep(wait_sec)
        sys.exit(0)

    # Require --csv whenever --keep-ineligible, --skip-completed, or --retry-failed is used
    if (args.keep_ineligible or args.skip_completed or args.retry_failed) and not args.csv:
        active_flags = [
            flag
            for flag, enabled in (
                ("--keep-ineligible", args.keep_ineligible),
                ("--skip-completed", args.skip_completed),
                ("--retry-failed", args.retry_failed),
            )
            if enabled
        ]
        parser.error(
            f"{', '.join(active_flags)} requires --csv <path_to_existing_csv_or_run_dir>. "
            "Pass --csv pointing to the existing CSV ledger (or run directory) these flags should apply to, "
            "or remove those flags to start a fresh run."
        )

    # Standalone --keep-ineligible --csv <path> prune mode (no target_path passed)
    if args.keep_ineligible and not args.target_path:
        cand = Path(args.csv)
        if not cand.exists():
            print(f"Error: Source --csv path does not exist: {cand}", file=sys.stderr)
            sys.exit(1)
        standalone_csv_path = (cand / "pipeline_runs.csv") if cand.is_dir() else cand
        csv_logger = PipelineMetricsCSVLogger(csv_path=standalone_csv_path)
        removed_cnt, kept_cnt = csv_logger.prune_keep_ineligible_only()
        print(
            f"[CSV PRUNE] Updated {csv_logger.csv_path}: removed {removed_cnt} eligible row(s), "
            f"retained {kept_cnt} INELIGIBLE row(s) (is_eligible=False)."
        )
        sys.exit(0)

    if not args.target_path:
        parser.error("the following arguments are required: target_path (or pass --view <run_dir>)")

    targets = [Path(p) for p in args.target_path]
    for t in targets:
        if not t.exists():
            print(f"Error: Target path does not exist: {t}", file=sys.stderr)
            sys.exit(1)

    if args.csv and not Path(args.csv).exists():
        print(f"Error: Source --csv path does not exist: {args.csv}", file=sys.stderr)
        sys.exit(1)

    # Pre-flight verification of MITRE CPSA 4.4.9 compiler binaries before starting LLM synthesis
    missing_cpsa_bins = SYSTEM_CONFIG.verify_cpsa_toolchain()
    if missing_cpsa_bins:
        print(
            "Error: MITRE CPSA 4.4.9 compiler toolchain is missing required binaries:\n"
            + "\n".join(f"  - {b}" for b in missing_cpsa_bins)
            + "\nInstall CPSA 4.4.9 (`cabal update && cabal install cpsa`) or ensure ~/.cabal/bin is populated before running synthesis.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 1. Create Unique Timestamped Run Directory & Per-Run CSV Ledger
    run_timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_dir = Path(args.output_dir) if args.output_dir else SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR
    if base_dir.name.startswith("run_"):
        run_root_dir = base_dir
    else:
        run_root_dir = base_dir / f"run_{run_timestamp}"
    run_root_dir.mkdir(parents=True, exist_ok=True)
    run_csv_path = run_root_dir / "pipeline_runs.csv"
    csv_logger = PipelineMetricsCSVLogger(csv_path=run_csv_path)

    # Seed new run's CSV from --csv <source> (source CSV is never mutated)
    if args.csv:
        src_csv_path = Path(args.csv)
        seeded_count = csv_logger.seed_from_source(src_csv_path)
        print(
            f"[CSV SEED] Copied {seeded_count} row(s) from {src_csv_path} -> {run_csv_path} "
            f"(source left untouched)."
        )

    if args.keep_ineligible:
        removed_cnt, kept_cnt = csv_logger.prune_keep_ineligible_only()
        print(
            f"[CSV PRUNE] Pruned {run_csv_path}: removed {removed_cnt} eligible row(s), "
            f"retained {kept_cnt} INELIGIBLE row(s) (is_eligible=False)."
        )
        args.skip_completed = True

    GLOBAL_EVENT_BUS.set_run_directory(run_root_dir, is_live=True, csv_path=run_csv_path)

    # 2. Resolve Target Files (Single File, Multiple Files, or Directory Batch)
    if len(targets) > 1 or targets[0].is_file():
        rfc_files = [t for t in targets if t.is_file()]
    elif targets[0].is_dir():
        target = targets[0]
        raw_candidates = [f for f in target.glob(args.pattern) if f.is_file()]
        if args.pattern == "rfc*.txt":
            # Exclude non-numeric index/reference files such as rfc-index-latest.txt or rfc-ref-old.txt
            numeric_candidates = [f for f in raw_candidates if re.fullmatch(r"rfc\d+\.txt", f.name.lower())]
            rfc_files = sorted(numeric_candidates or raw_candidates, key=natural_rfc_sort_key)
        else:
            rfc_files = sorted(raw_candidates, key=natural_rfc_sort_key)
        if not rfc_files:
            # Fallback to all existing txt files if pattern yielded zero
            rfc_files = sorted([f for f in target.glob("*.txt") if f.is_file()], key=natural_rfc_sort_key)
        if not rfc_files:
            print(f"Error: No RFC text files found in directory {target}", file=sys.stderr)
            sys.exit(1)

        if args.retry_failed:
            failed_ids = get_failed_rfc_ids(csv_path=run_csv_path)
            rfc_files = [
                f for f in rfc_files
                if f.stem.upper().replace(" ", "").replace("_", "") in failed_ids
            ]
            print(f"[BATCH] Filtered to {len(rfc_files)} previously FAILED/PARTIAL RFCs from {run_csv_path}")
        elif args.skip_completed:
            completed_ids = get_completed_rfc_ids(csv_path=run_csv_path)
            initial_count = len(rfc_files)
            rfc_files = [
                f for f in rfc_files
                if f.stem.upper().replace(" ", "").replace("_", "") not in completed_ids
            ]
            print(f"[BATCH] Filtered out {initial_count - len(rfc_files)} previously evaluated RFCs ({len(rfc_files)} remaining)")

        if args.tier0_eligible_only:
            before_t0 = len(rfc_files)
            rfc_files = [
                f for f in rfc_files
                if filter_rfc_header(f.read_text(encoding="utf-8", errors="ignore")).is_eligible
            ]
            print(f"[BATCH] Tier 0 pre-filter retained {len(rfc_files)}/{before_t0} candidate RFCs")

        if args.random:
            random.shuffle(rfc_files)
            print("[BATCH] Shuffled candidate RFC list randomly")

        if args.limit and args.limit > 0:
            rfc_files = rfc_files[:args.limit]
            print(f"[BATCH] Processing limited to {len(rfc_files)} RFCs: {[f.name for f in rfc_files]}")
    else:
        print(f"Error: Invalid target path: {targets[0]}", file=sys.stderr)
        sys.exit(1)

    # 3. Launch Visualizer (Default Enabled)
    enable_visualizer = not args.no_visualize
    monitor_url = None
    if enable_visualizer:
        try:
            server = run_visualizer_in_background(port=args.port)
            monitor_url = f"http://127.0.0.1:{server.port}"
            print(f"\n{'='*70}")
            print(f" [LIVE MONITOR] Active at: {monitor_url}")
            print(f"{'='*70}\n")
            try:
                webbrowser.open(monitor_url)
            except Exception:
                pass
        except Exception as e:
            print(f"[WARN] Could not launch live monitor: {e}")

    master_index_path = run_root_dir / "metadata_index.json"
    if not master_index_path.exists():
        now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        master_index_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0.0",
                    "run_directory": str(run_root_dir.resolve()),
                    "csv_file": str(run_csv_path.resolve()),
                    "created_at_utc": now_utc,
                    "updated_at_utc": now_utc,
                    "total_rfcs_processed": 0,
                    "total_ineligible_filtered": 0,
                    "total_eligible_protocols": 0,
                    "metadata_json_files": [],
                    "rfc_directories": [],
                    "runs": [],
                    "filtered_rfcs": [],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    print(f"[RUN] Created timestamped run directory: {run_root_dir}")
    print(f"[RUN] Master Metadata Index           : {master_index_path}")
    print(f"[RUN] Run CSV Ledger                  : {run_csv_path}")

    # 4. Execution Loop (Models resolve dynamically from prompts/*.md unless CLI overrides are passed)
    results: List[PipelineExecutionSummary] = []
    total_files = len(rfc_files)
    cli_router_model = args.router_model or args.model
    cli_extraction_model = args.extraction_model or args.model
    cli_repair_model = args.repair_model or args.model
    cli_query_model = args.query_model or args.model

    for idx, rfc_file in enumerate(rfc_files, 1):
        if total_files > 1:
            print(f"\n{'='*70}")
            print(f"[{idx}/{total_files}] Processing RFC: {rfc_file.name}")
            print(f"{'='*70}")

        rfc_output_dir = run_root_dir / rfc_file.stem.lower()
        try:
            summary = run_rfc_translation_pipeline(
                rfc_file_path=rfc_file,
                output_dir=rfc_output_dir,
                router_model=cli_router_model,
                extraction_model=cli_extraction_model,
                repair_model=cli_repair_model,
                query_model=cli_query_model,
                run_root_dir=run_root_dir,
                csv_path=run_csv_path,
            )
        except Exception as exc:
            print(f"[ERROR] Unhandled exception on {rfc_file.name}: {exc}", file=sys.stderr)
            summary = PipelineExecutionSummary(
                rfc_id=rfc_file.stem.upper(),
                is_eligible=False,
                error_message=f"Unhandled pipeline exception: {exc}",
            )
        results.append(summary)

        if args.target_eligible and args.target_eligible > 0:
            eligible_so_far = sum(1 for r in results if r.is_eligible)
            if eligible_so_far >= args.target_eligible:
                print(
                    f"\n[BATCH] Reached target of {eligible_so_far}/{args.target_eligible} "
                    f"eligible cryptographic protocols after scanning {idx} RFC(s)."
                )
                break

        if total_files == 1:
            # Single-file reporting and exit code
            if summary.build_successful:
                print("\n[SUCCESS] Synthesis & Formal Verification Completed!")
                print(f"Protocol             : {summary.protocol_name}")
                print(f"Quality Tier         : {summary.quality_tier}")
                if summary.intake_rationale:
                    print(f"Intake Rationale     : Eligible: {summary.intake_rationale}")
                if summary.security_findings:
                    sf = summary.security_findings
                    print(
                        f"Security Findings    : Auth={sf.get('authentication_profile', 'N/A')} | "
                        f"Agreement={sf.get('parameter_agreement_status', 'N/A')} | "
                        f"Secrecy={sf.get('secrecy_status', 'N/A')} | "
                        f"Anomalies={sf.get('anomalies_count', 0)}"
                    )
                print(f"Run Directory        : {run_root_dir}")
                print(f"Master Metadata Index: {master_index_path}")
                print(f"Run Metrics Logged   : {run_csv_path}")
                print(f"RFC Directory        : {rfc_output_dir}")
                print(f"RFC Trajectory JSON  : {summary.trajectory_json_path}")
                print(f"Verified Shapes XHTML: {summary.build_artifacts.shapes_graph_xhtml_path}")
            elif summary.roletran_passed:
                print(f"\n[PARTIAL] Roletran passed, but MITRE build failed: {summary.error_message}")
                print(f"Run Directory        : {run_root_dir}")
                print(f"Master Metadata Index: {master_index_path}")
                print(f"Run Metrics Logged   : {run_csv_path}")
                print(f"RFC Trajectory JSON  : {summary.trajectory_json_path}")
            else:
                print(f"\n[HALTED] Pipeline stopped: {summary.error_message}")
                print(f"Run Directory        : {run_root_dir}")
                print(f"Master Metadata Index: {master_index_path}")
                print(f"Run Metrics Logged   : {run_csv_path}")
                if summary.trajectory_json_path:
                    print(f"RFC Trajectory JSON  : {summary.trajectory_json_path}")

            _print_cost_breakdown(GLOBAL_COST_TRACKER.get_current_rfc_summary(), "RFC RUN COST & TOKEN TELEMETRY")

            if enable_visualizer and monitor_url:
                print(f"\n[LIVE MONITOR] View execution trace and shapes at: {monitor_url}")
                if sys.stdin.isatty():
                    try:
                        input("[LIVE MONITOR] Press Enter to exit (server remains live until keypress)... ")
                    except (EOFError, KeyboardInterrupt):
                        pass
                elif args.keep_alive > 0:
                    print(f"[LIVE MONITOR] Keeping server active for {args.keep_alive}s...")
                    time.sleep(args.keep_alive)

            sys.exit(0 if summary.build_successful else (1 if summary.roletran_passed else 2))

    # 5. Batch Summary Report
    print(f"\n{'='*70}")
    print(f"RFC-LLM BATCH SYNTHESIS REPORT ({total_files} RFCs Processed)")
    print(f"{'='*70}")
    verified_count = sum(1 for r in results if r.build_successful)
    eligible_count = sum(1 for r in results if r.is_eligible)
    ineligible_count = sum(1 for r in results if not r.is_eligible)
    roletran_failed = sum(1 for r in results if r.is_eligible and not r.roletran_passed)
    solver_failed = sum(1 for r in results if r.roletran_passed and not r.build_successful)

    print(f"- Total Processed      : {total_files}")
    print(f"- Ineligible (Filtered): {ineligible_count}")
    print(f"- Eligible Protocols   : {eligible_count}")
    print(f"- Formally Verified    : {verified_count}")
    if roletran_failed:
        print(f"- Roletran Failed      : {roletran_failed}")
    if solver_failed:
        print(f"- Solver Failed        : {solver_failed}")
    print(f"- Run Directory        : {run_root_dir}")
    print(f"- Master Metadata Index: {master_index_path}")
    print(f"- Run Metrics Logged   : {run_csv_path}")
    _print_cost_breakdown(GLOBAL_COST_TRACKER.get_batch_summary(), "BATCH COST & TOKEN TELEMETRY BY MODEL ROLE")
    print(f"{'='*70}\n")

    if enable_visualizer and monitor_url:
        print(f"[LIVE MONITOR] Batch dashboard active at: {monitor_url}")
        if sys.stdin.isatty():
            try:
                input("[LIVE MONITOR] Press Enter to exit (server remains live until keypress)... ")
            except (EOFError, KeyboardInterrupt):
                pass
        elif args.keep_alive > 0:
            print(f"[LIVE MONITOR] Keeping server active for {args.keep_alive}s...")
            time.sleep(args.keep_alive)


if __name__ == "__main__":
    main()
```

---

### `src/pipeline_events.py`

*sha256:`0207791836c5` · 609 lines · 26.5 KB (~6,792 tokens) · lang:`python`*

```python
"""Bounded event bus, sequential tab registry, and disk telemetry sink for pipeline visualization."""

import json
import re
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class PipelineEvent(BaseModel):
    """Structured event emitted across pipeline execution stages."""
    timestamp: float = Field(default_factory=time.time)
    event_type: str = Field(..., description="Type of event (e.g. stage_started, repair_attempt, tab_accepted)")
    stage: Optional[int] = Field(None, description="Stage index (1 to 6)")
    stage_name: Optional[str] = Field(None, description="Human readable stage name")
    rfc_id: Optional[str] = Field(None, description="RFC identifier associated with this event")
    tab_index: Optional[int] = Field(None, description="Sequential 1-based tab number if RFC was accepted")
    data: Dict[str, Any] = Field(default_factory=dict, description="Payload data")

    def to_sse_message(self) -> str:
        """Formats the event as a standard Server-Sent Event (SSE) frame."""
        payload = json.dumps(self.model_dump())
        return f"event: {self.event_type}\ndata: {payload}\n\n"


def _strip_bulky_event_fields(event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Strips large AST blobs before writing compact event lines to events.jsonl
    (full per-attempt ASTs and .scm snapshots are already stored in <stem>_trajectory.json).
    """
    data = event_dict.get("data")
    if not isinstance(data, dict) or "ast" not in data:
        return event_dict
    slim_copy = dict(event_dict)
    slim_data = dict(data)
    ast_obj = slim_data.pop("ast", None)
    if isinstance(ast_obj, dict):
        slim_data["ast_protocol_name"] = ast_obj.get("protocol_name")
    slim_copy["data"] = slim_data
    return slim_copy


class PipelineEventBus:
    """Thread-safe, O(1)-RAM event dispatcher with sequential accepted-RFC tab indexing."""

    def __init__(self):
        self._lock = threading.RLock()
        self._listeners: List[Callable[[PipelineEvent], None]] = []
        # Bounded buffer: holds ONLY the currently executing RFC's events in RAM
        self._active_events: List[PipelineEvent] = []
        self._current_rfc_id: Optional[str] = None
        self._current_tab_index: Optional[int] = None
        self._current_events_jsonl: Optional[Path] = None

        # Run-level compact registries (~150 bytes per entry -> <1 MB for 5,000 RFCs)
        self._run_root_dir: Optional[Path] = None
        self._csv_path: Optional[Path] = None
        self._is_live: bool = True
        self._next_tab_index: int = 0
        self._accepted_tabs: Dict[int, Dict[str, Any]] = {}
        self._tab_order: List[int] = []
        self._filtered_rfcs: List[Dict[str, Any]] = []
        self._batch_cost_telemetry: Dict[str, Any] = {}

    def subscribe(self, callback: Callable[[PipelineEvent], None]):
        """Registers a listener callback."""
        with self._lock:
            if callback not in self._listeners:
                self._listeners.append(callback)

    def unsubscribe(self, callback: Callable[[PipelineEvent], None]):
        """Removes a listener callback."""
        with self._lock:
            if callback in self._listeners:
                self._listeners.remove(callback)

    def set_run_directory(
        self,
        run_root_dir: Path,
        is_live: bool = True,
        csv_path: Optional[Path] = None,
    ) -> None:
        """Binds the current run root directory and active CSV ledger path."""
        with self._lock:
            self._run_root_dir = run_root_dir.resolve()
            self._csv_path = (csv_path or (self._run_root_dir / "pipeline_runs.csv")).resolve()
            self._is_live = is_live

    def get_csv_path(self) -> Optional[Path]:
        """Returns the bound CSV path for the active or replayed run."""
        with self._lock:
            return self._csv_path

    def get_run_root_dir(self) -> Optional[Path]:
        """Returns the bound run root directory."""
        with self._lock:
            return self._run_root_dir

    def start_rfc(self, rfc_id: str, rfc_file: Optional[str] = None) -> None:
        """Evicts the completed RFC's in-memory event buffer and prepares for the next RFC."""
        with self._lock:
            self._active_events.clear()
            self._current_rfc_id = rfc_id
            self._current_tab_index = None
            self._current_events_jsonl = None
            self._is_live = True

    def register_accepted_tab(
        self,
        rfc_id: str,
        protocol_name: str,
        rfc_dir: Path,
        rfc_title: Optional[str] = None,
        intake_rationale: Optional[str] = None,
    ) -> int:
        """Allocates the next sequential 1-based tab number (#1, #2, ...) for an accepted RFC,
        binds its per-RFC events.jsonl sink, and flushes buffered Stage 1 events to disk.
        """
        with self._lock:
            self._next_tab_index += 1
            tab_idx = self._next_tab_index
            self._current_tab_index = tab_idx
            self._current_rfc_id = rfc_id

            resolved_dir = rfc_dir.resolve()
            resolved_dir.mkdir(parents=True, exist_ok=True)
            jsonl_path = resolved_dir / "events.jsonl"
            self._current_events_jsonl = jsonl_path

            tab_summary: Dict[str, Any] = {
                "tab_index": tab_idx,
                "rfc_id": rfc_id,
                "protocol_name": protocol_name,
                "rfc_title": rfc_title or protocol_name,
                "status": "RUNNING",
                "quality_tier": "PENDING",
                "total_attempts": 0,
                "shapes_count": 0,
                "duration_seconds": 0.0,
                "cost_usd": 0.0,
                "cost_telemetry": {},
                "rfc_dir": str(resolved_dir),
                "events_jsonl": str(jsonl_path),
                "slice_path": None,
                "scm_path": None,
                "trajectory_path": None,
                "shapes_xhtml": None,
                "error_message": None,
                "intake_rationale": intake_rationale,
                "security_findings": {},
            }
            self._accepted_tabs[tab_idx] = tab_summary
            self._tab_order.append(tab_idx)

            # Backfill tab_index onto buffered intake events and flush them to events.jsonl
            try:
                with open(jsonl_path, "w", encoding="utf-8") as handle:
                    for buffered_evt in self._active_events:
                        buffered_evt.tab_index = tab_idx
                        if not buffered_evt.rfc_id:
                            buffered_evt.rfc_id = rfc_id
                        slim = _strip_bulky_event_fields(buffered_evt.model_dump())
                        handle.write(json.dumps(slim) + "\n")
            except Exception:
                pass

        self.emit("tab_accepted", stage=1, tab=tab_summary)
        return tab_idx

    def update_accepted_tab(self, tab_index: int, **updates: Any) -> Optional[Dict[str, Any]]:
        """Updates metadata on an existing numbered tab and notifies connected clients."""
        with self._lock:
            tab = self._accepted_tabs.get(tab_index)
            if not tab:
                return None
            for k, v in updates.items():
                if v is not None or k in ("error_message",):
                    tab[k] = v
            snapshot = dict(tab)

        self.emit("tab_updated", tab=snapshot)
        return snapshot

    def register_filtered_rfc(
        self,
        rfc_id: str,
        title: str,
        gate: str,
        reason: str,
        duration_seconds: float = 0.0,
    ) -> Dict[str, Any]:
        """Records a disqualified/non-cryptographic RFC without allocating a numbered tab."""
        with self._lock:
            entry = {
                "index": len(self._filtered_rfcs) + 1,
                "rfc_id": rfc_id,
                "title": title or rfc_id,
                "gate": gate,
                "reason": reason,
                "duration_seconds": round(duration_seconds, 2),
                "timestamp": time.time(),
            }
            self._filtered_rfcs.append(entry)
            total = len(self._filtered_rfcs)

        self.emit("rfc_filtered", stage=1, filtered_total=total, entry=entry)
        return entry

    def emit(
        self,
        event_type: str,
        stage: Optional[int] = None,
        stage_name: Optional[str] = None,
        **kwargs,
    ) -> PipelineEvent:
        """Emits an event to all subscribers, stores it in the bounded active buffer, and appends to events.jsonl."""
        with self._lock:
            rfc_id = kwargs.get("rfc_id") or self._current_rfc_id
            tab_index = kwargs.get("tab_index") or self._current_tab_index
            event = PipelineEvent(
                event_type=event_type,
                stage=stage,
                stage_name=stage_name,
                rfc_id=rfc_id,
                tab_index=tab_index,
                data=kwargs,
            )
            if event_type == "cost_updated":
                if isinstance(kwargs.get("batch_cost"), dict):
                    self._batch_cost_telemetry = kwargs["batch_cost"]
                if tab_index and tab_index in self._accepted_tabs and isinstance(kwargs.get("rfc_cost"), dict):
                    self._accepted_tabs[tab_index]["cost_telemetry"] = kwargs["rfc_cost"]
                    self._accepted_tabs[tab_index]["cost_usd"] = round(
                        float(kwargs["rfc_cost"].get("total_cost_usd", 0.0)), 6
                    )

            # Meta-events for filtered RFCs don't need to bloat an accepted tab's buffer,
            # while active RFC progress events stay in the bounded buffer.
            if event_type != "rfc_filtered":
                self._active_events.append(event)

            jsonl_target = self._current_events_jsonl
            if jsonl_target and event_type not in ("rfc_filtered",):
                try:
                    slim = _strip_bulky_event_fields(event.model_dump())
                    with open(jsonl_target, "a", encoding="utf-8") as handle:
                        handle.write(json.dumps(slim) + "\n")
                except Exception:
                    pass

            listeners_snapshot = list(self._listeners)

        for listener in listeners_snapshot:
            try:
                listener(event)
            except Exception:
                pass
        return event

    def get_history(self) -> List[PipelineEvent]:
        """Returns the bounded event log for the currently active RFC."""
        with self._lock:
            return list(self._active_events)

    def get_active_state(self) -> Dict[str, Any]:
        """Returns active RFC identification and its bounded in-memory event stream."""
        with self._lock:
            return {
                "is_live": self._is_live,
                "rfc_id": self._current_rfc_id,
                "tab_index": self._current_tab_index,
                "events": [e.model_dump() for e in self._active_events],
            }

    def get_tabs_overview(self) -> Dict[str, Any]:
        """Returns the compact O(N) summary array (~150B/tab) for the virtualized tab strip."""
        with self._lock:
            tabs = [dict(self._accepted_tabs[idx]) for idx in self._tab_order if idx in self._accepted_tabs]
            return {
                "is_live": self._is_live,
                "run_directory": str(self._run_root_dir) if self._run_root_dir else None,
                "csv_path": str(self._csv_path) if self._csv_path else None,
                "active_rfc_id": self._current_rfc_id,
                "active_tab_index": self._current_tab_index,
                "accepted_tabs": tabs,
                "filtered_total": len(self._filtered_rfcs),
                "batch_cost_telemetry": self._batch_cost_telemetry,
            }

    def get_tab_summary(self, tab_index: int) -> Optional[Dict[str, Any]]:
        """Returns a single tab summary by 1-based index."""
        with self._lock:
            tab = self._accepted_tabs.get(tab_index)
            return dict(tab) if tab else None

    def get_filtered_slice(self, offset: int = 0, limit: int = 100, query: str = "") -> Dict[str, Any]:
        """Returns a paginated, optionally filtered slice of disqualified RFCs."""
        with self._lock:
            items = self._filtered_rfcs
            if query:
                q_low = query.lower().strip()
                items = [
                    it for it in items
                    if q_low in it.get("rfc_id", "").lower()
                    or q_low in it.get("title", "").lower()
                    or q_low in it.get("reason", "").lower()
                    or q_low in it.get("gate", "").lower()
                ]
            total_matching = len(items)
            sliced = items[max(0, offset) : max(0, offset) + max(1, min(limit, 500))]
            return {
                "total": len(self._filtered_rfcs),
                "matching": total_matching,
                "offset": offset,
                "limit": limit,
                "items": sliced,
            }

    def clear(self):
        """Resets all active and run-scoped event bus state."""
        with self._lock:
            self._active_events.clear()
            self._current_rfc_id = None
            self._current_tab_index = None
            self._current_events_jsonl = None
            self._run_root_dir = None
            self._csv_path = None
            self._is_live = True
            self._next_tab_index = 0
            self._accepted_tabs.clear()
            self._tab_order.clear()
            self._filtered_rfcs.clear()
            self._batch_cost_telemetry = {}

    def load_run_from_disk(self, target_path: Path) -> Dict[str, Any]:
        """Reconstructs numbered accepted tabs and filtered RFCs from an existing run directory,
        metadata_index.json, or single <protocol>_trajectory.json for offline `--view` replay.
        """
        resolved = target_path.resolve()
        with self._lock:
            self.clear()
            self._is_live = False

            index_file: Optional[Path] = None
            run_dir: Path = resolved

            if resolved.is_file():
                if resolved.name == "metadata_index.json":
                    index_file = resolved
                    run_dir = resolved.parent
                elif resolved.suffix.lower() == ".csv":
                    self._csv_path = resolved
                    run_dir = resolved.parent
                    if (run_dir / "metadata_index.json").exists():
                        index_file = run_dir / "metadata_index.json"
                elif resolved.name.endswith("_trajectory.json"):
                    run_dir = resolved.parent.parent
                    self._run_root_dir = run_dir
                    self._csv_path = (run_dir / "pipeline_runs.csv").resolve()
                    self._ingest_trajectory_as_tab(resolved, explicit_index=1)
                    return self.get_tabs_overview()
            elif resolved.is_dir():
                if (resolved / "metadata_index.json").exists():
                    index_file = resolved / "metadata_index.json"
                    run_dir = resolved
                else:
                    # Check if pointed directly at a single RFC output folder
                    trajs = sorted(resolved.glob("*_trajectory.json"))
                    if trajs:
                        self._run_root_dir = resolved.parent
                        self._csv_path = (resolved.parent / "pipeline_runs.csv").resolve()
                        for t_path in trajs:
                            self._ingest_trajectory_as_tab(t_path)
                        return self.get_tabs_overview()

            self._run_root_dir = run_dir
            if self._csv_path is None:
                self._csv_path = (run_dir / "pipeline_runs.csv").resolve()

            if index_file and index_file.exists():
                try:
                    idx_data = json.loads(index_file.read_text(encoding="utf-8"))
                except Exception:
                    idx_data = {}

                if isinstance(idx_data.get("batch_cost_telemetry"), dict):
                    self._batch_cost_telemetry = idx_data["batch_cost_telemetry"]

                # 1. Restore filtered/rejected RFC list if persisted
                for filt in idx_data.get("filtered_rfcs", []):
                    self._filtered_rfcs.append({
                        "index": len(self._filtered_rfcs) + 1,
                        "rfc_id": filt.get("rfc_id", "UNKNOWN"),
                        "title": filt.get("title") or filt.get("protocol_name") or filt.get("rfc_id", "Unknown"),
                        "gate": filt.get("gate", "Intake Gate"),
                        "reason": filt.get("reason") or filt.get("error_message") or "Filtered",
                        "duration_seconds": float(filt.get("duration_seconds", 0.0)),
                        "timestamp": 0.0,
                    })

                # Backward-compat: if older metadata_index.json only stored total_ineligible_filtered count
                persisted_ineligible_count = int(idx_data.get("total_ineligible_filtered", 0))
                if not self._filtered_rfcs and persisted_ineligible_count > 0:
                    self._filtered_rfcs.append({
                        "index": 1,
                        "rfc_id": f"{persisted_ineligible_count} RFCs",
                        "title": "Legacy Run Filtered Summary",
                        "gate": "Stage 1a / Stage 1c",
                        "reason": (
                            f"{persisted_ineligible_count} non-cryptographic RFC(s) were filtered prior to "
                            "detailed per-RFC filtered logging."
                        ),
                        "duration_seconds": 0.0,
                        "timestamp": 0.0,
                    })

                # 2. Restore accepted protocol tabs in exact run order
                runs_list = idx_data.get("runs", [])
                seen_dirs = set()
                for run_entry in runs_list:
                    if not run_entry.get("is_eligible", True):
                        self._filtered_rfcs.append({
                            "index": len(self._filtered_rfcs) + 1,
                            "rfc_id": run_entry.get("rfc_id", "UNKNOWN"),
                            "title": run_entry.get("protocol_name") or run_entry.get("rfc_id", "Unknown"),
                            "gate": "Intake Gate",
                            "reason": run_entry.get("error_message") or "Ineligible",
                            "duration_seconds": 0.0,
                            "timestamp": 0.0,
                        })
                        continue

                    rfc_dir_str = run_entry.get("rfc_directory")
                    traj_str = run_entry.get("metadata_json_file")
                    rfc_dir_path = Path(rfc_dir_str) if rfc_dir_str else None
                    if rfc_dir_path:
                        seen_dirs.add(str(rfc_dir_path.resolve()))
                    traj_path = Path(traj_str) if traj_str else None
                    if (not traj_path or not traj_path.exists()) and rfc_dir_path and rfc_dir_path.exists():
                        candidates = sorted(rfc_dir_path.glob("*_trajectory.json"))
                        if candidates:
                            traj_path = candidates[0]

                    if traj_path and traj_path.exists():
                        self._ingest_trajectory_as_tab(traj_path, fallback_entry=run_entry)
                    elif rfc_dir_path and rfc_dir_path.exists():
                        self._ingest_folder_without_trajectory(rfc_dir_path, fallback_entry=run_entry)

                # Also pick up any accepted RFC directories in run_dir that weren't flushed to metadata_index.json
                # (for example, if a batch run was interrupted with Ctrl+C mid-RFC)
                if run_dir.is_dir():
                    for child in sorted(run_dir.iterdir()):
                        if child.is_dir() and str(child.resolve()) not in seen_dirs:
                            trajs = sorted(child.glob("*_trajectory.json"))
                            if trajs:
                                self._ingest_trajectory_as_tab(trajs[0])
                            elif any(child.iterdir()):
                                self._ingest_folder_without_trajectory(child)
            elif run_dir.is_dir():
                for child in sorted(run_dir.iterdir()):
                    if child.is_dir():
                        trajs = sorted(child.glob("*_trajectory.json"))
                        if trajs:
                            self._ingest_trajectory_as_tab(trajs[0])

            return self.get_tabs_overview()

    def _ingest_trajectory_as_tab(
        self,
        traj_path: Path,
        fallback_entry: Optional[Dict[str, Any]] = None,
        explicit_index: Optional[int] = None,
    ) -> int:
        """Populates a numbered tab entry from a saved <stem>_trajectory.json file."""
        fallback_entry = fallback_entry or {}
        try:
            traj = json.loads(traj_path.read_text(encoding="utf-8"))
        except Exception:
            traj = {}

        rfc_dir = traj_path.parent.resolve()
        meta = traj.get("rfc_metadata", {})
        s5 = traj.get("stage5_preflight_gate", {})
        s6 = traj.get("stage6_cpsa4_solver", {})
        qa = traj.get("quality_assessment", {})

        self._next_tab_index = explicit_index if explicit_index else (self._next_tab_index + 1)
        tab_idx = self._next_tab_index

        rfc_id = meta.get("rfc_id") or fallback_entry.get("rfc_id") or rfc_dir.name.upper()
        proto_name = (
            meta.get("protocol_name")
            or fallback_entry.get("protocol_name")
            or traj_path.stem.replace("_trajectory", "")
        )
        rfc_title = meta.get("rfc_title") or fallback_entry.get("protocol_name") or proto_name
        quality_tier = qa.get("quality_tier") or fallback_entry.get("quality_tier") or "REJECTED"
        solver_passed = bool(s6.get("final_passed") or fallback_entry.get("build_successful"))
        roletran_passed = bool(s5.get("final_passed"))
        total_attempts = int(s5.get("total_attempts", 0)) + int(s6.get("total_attempts", 0))
        shapes_count = int(
            s6.get("shapes_analysis_from_shapes_txt", {}).get("total_realized_shapes", 0)
        )
        duration_sec = float(traj.get("duration_seconds", 0.0))

        scm_candidates = sorted(rfc_dir.glob("*.scm"))
        scm_path = str(scm_candidates[0]) if scm_candidates else fallback_entry.get("scm_file")
        shapes_candidates = sorted(rfc_dir.glob("*_shapes.xhtml"))
        shapes_xhtml = str(shapes_candidates[0]) if shapes_candidates else None
        slice_file = rfc_dir / "verbatim_slice.txt"
        events_jsonl = rfc_dir / "events.jsonl"

        if solver_passed:
            status = "VERIFIED"
        elif roletran_passed:
            status = "PARTIAL"
        else:
            status = "FAILED"

        cost_tel = traj.get("cost_telemetry") or fallback_entry.get("cost_telemetry") or {}
        cost_usd = round(
            float(cost_tel.get("total_cost_usd", fallback_entry.get("cost_usd", 0.0))), 6
        )
        if not self._batch_cost_telemetry and cost_tel:
            self._batch_cost_telemetry = cost_tel

        sec_findings = (
            traj.get("security_findings")
            or qa.get("security_findings")
            or fallback_entry.get("security_findings")
            or {}
        )
        intake_rationale = meta.get("intake_rationale") or fallback_entry.get("intake_rationale")

        tab_summary = {
            "tab_index": tab_idx,
            "rfc_id": rfc_id,
            "protocol_name": proto_name,
            "rfc_title": rfc_title,
            "status": status,
            "quality_tier": quality_tier,
            "total_attempts": total_attempts,
            "shapes_count": shapes_count,
            "duration_seconds": round(duration_sec, 2),
            "cost_usd": cost_usd,
            "cost_telemetry": cost_tel,
            "rfc_dir": str(rfc_dir),
            "events_jsonl": str(events_jsonl) if events_jsonl.exists() else None,
            "slice_path": str(slice_file) if slice_file.exists() else None,
            "scm_path": scm_path,
            "trajectory_path": str(traj_path.resolve()),
            "shapes_xhtml": shapes_xhtml,
            "error_message": fallback_entry.get("error_message"),
            "intake_rationale": intake_rationale,
            "security_findings": sec_findings,
        }
        self._accepted_tabs[tab_idx] = tab_summary
        self._tab_order.append(tab_idx)
        return tab_idx

    def _ingest_folder_without_trajectory(
        self,
        rfc_dir: Path,
        fallback_entry: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Handles an interrupted accepted RFC directory (e.g. Ctrl+C mid-extraction)."""
        fallback_entry = fallback_entry or {}
        resolved_dir = rfc_dir.resolve()
        self._next_tab_index += 1
        tab_idx = self._next_tab_index

        m = re.match(r"rfc(\d+)", resolved_dir.name.lower())
        inferred_rfc = f"RFC {m.group(1)}" if m else resolved_dir.name.upper()
        rfc_id = fallback_entry.get("rfc_id") or inferred_rfc
        proto_name = fallback_entry.get("protocol_name") or resolved_dir.name

        scm_candidates = sorted(resolved_dir.glob("*.scm"))
        shapes_candidates = sorted(resolved_dir.glob("*_shapes.xhtml"))
        slice_file = resolved_dir / "verbatim_slice.txt"
        events_jsonl = resolved_dir / "events.jsonl"

        tab_summary = {
            "tab_index": tab_idx,
            "rfc_id": rfc_id,
            "protocol_name": proto_name,
            "rfc_title": proto_name,
            "status": "VERIFIED" if shapes_candidates else "INTERRUPTED",
            "quality_tier": fallback_entry.get("quality_tier") or "INCOMPLETE",
            "total_attempts": 0,
            "shapes_count": 0,
            "duration_seconds": 0.0,
            "rfc_dir": str(resolved_dir),
            "events_jsonl": str(events_jsonl) if events_jsonl.exists() else None,
            "slice_path": str(slice_file) if slice_file.exists() else None,
            "scm_path": str(scm_candidates[0]) if scm_candidates else None,
            "trajectory_path": None,
            "shapes_xhtml": str(shapes_candidates[0]) if shapes_candidates else None,
            "error_message": fallback_entry.get("error_message") or "Interrupted before trajectory export",
            "intake_rationale": fallback_entry.get("intake_rationale"),
            "security_findings": fallback_entry.get("security_findings") or {},
        }
        self._accepted_tabs[tab_idx] = tab_summary
        self._tab_order.append(tab_idx)
        return tab_idx


# Global event bus singleton
GLOBAL_EVENT_BUS = PipelineEventBus()
```

---

### `src/prompt_loader.py`

*sha256:`9934cc0348f8` · 292 lines · 12.7 KB (~3,251 tokens) · lang:`python`*

````python
"""Dynamic Markdown & YAML-Frontmatter Prompt Loader for RFC-LLM (prompts/ directory).

Each `prompts/*.md` file begins with an optional YAML frontmatter block configuring
its target LLM (`model`), request `timeout`, and optional `temperature`, followed by
the system prompt body:

    ---
    model: strata/unsloth-iq4_xs
    timeout: 180
    temperature: 0.0
    ---
    You are a formal methods expert...

Files are read dynamically on every invocation so prompt and model edits hot-reload
live mid-batch without restarting the pipeline.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Type
import yaml
from pydantic import BaseModel

from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("prompt_loader")

# Canonical prompt filenames in prompts/
PROMPT_APPLICABILITY_GATE = "01_applicability_gate.md"
PROMPT_SECTION_ROUTER = "02_section_router.md"
PROMPT_PROTOCOL_EXTRACTION = "03_protocol_extraction.md"
PROMPT_SCHEMA_SELF_CORRECTION = "04_schema_self_correction.md"
PROMPT_RAG_QUERY_FORMULATION = "05_rag_query_formulation.md"
PROMPT_COMPILER_REPAIR = "06_compiler_repair.md"
PROMPT_THINK_SYNTHESIZER = "07_think_token_synthesizer.md"

GLOBAL_FALLBACK_MODEL = "gemini/gemini-3.5-flash-lite"

# Built-in fallback models & timeouts when a `prompts/*.md` file omits frontmatter or is missing
_FALLBACK_METADATA: Dict[str, Dict[str, Any]] = {
    PROMPT_APPLICABILITY_GATE: {"model": "strata/unsloth-iq4_xs", "timeout": 900, "max_tokens": 16384, "temperature": None},
    PROMPT_SECTION_ROUTER: {"model": "strata/unsloth-iq4_xs", "timeout": 900, "max_tokens": 16384, "temperature": None},
    PROMPT_PROTOCOL_EXTRACTION: {"model": "strata/unsloth-iq4_xs", "timeout": 3600, "max_tokens": 65536, "temperature": None},
    PROMPT_SCHEMA_SELF_CORRECTION: {"model": "strata/unsloth-iq4_xs", "timeout": 3600, "max_tokens": 65536, "temperature": None},
    PROMPT_RAG_QUERY_FORMULATION: {"model": "strata/unsloth-iq4_xs", "timeout": 900, "max_tokens": 16384, "temperature": None},
    PROMPT_COMPILER_REPAIR: {"model": "strata/unsloth-iq4_xs", "timeout": 3600, "max_tokens": 65536, "temperature": None},
    PROMPT_THINK_SYNTHESIZER: {"model": "strata/unsloth-iq4_xs", "timeout": 3600, "max_tokens": 65536, "temperature": 0.2},
}

# Built-in fallback prompt bodies if a file in prompts/ is missing or empty
_FALLBACK_PROMPTS: Dict[str, str] = {
    PROMPT_APPLICABILITY_GATE: (
        "You are a formal methods expert in cryptographic protocol verification using MITRE CPSA 4.4.9.\n"
        "Analyze the RFC metadata and Table of Contents to determine if it specifies an interactive "
        "cryptographic security protocol.\n"
        "CRITICAL: Return a populated JSON instance, NOT the schema definition."
    ),
    PROMPT_SECTION_ROUTER: (
        "You are a protocol analyst reading an RFC's Table of Contents.\n"
        "Identify the EXACT section numbers that define the cryptographic message exchange or handshake.\n"
        "Return ONLY a valid JSON object matching the requested schema."
    ),
    PROMPT_PROTOCOL_EXTRACTION: (
        "You are a formal methods expert in cryptographic protocol specification for MITRE CPSA 4.4.9.\n"
        "Analyze the verbatim RFC specification text and extract a complete, mathematically rigorous "
        "CPSAProtocolSpecification.\n"
        "Return ONLY a valid JSON object matching the requested CPSAProtocolSpecification schema."
    ),
    PROMPT_SCHEMA_SELF_CORRECTION: (
        "Your previous JSON output failed MITRE CPSA 4.4.9 schema and scoping validation with the following errors:\n"
        "{validation_error}\n\n"
        "Return ONLY the corrected, fully valid JSON object."
    ),
    PROMPT_RAG_QUERY_FORMULATION: (
        "You are a formal verification compiler diagnostic analyst for MITRE CPSA 4.4.9.\n"
        "Formulate a concise, targeted search query (3 to 6 words) abstracting concrete variable names "
        "into formal CPSA grammar, algebra, or roletran concepts.\n"
        "Output strictly the plain text search query (3 to 6 words)."
    ),
    PROMPT_COMPILER_REPAIR: (
        "You are a formal methods expert in debugging and repairing MITRE CPSA 4.4.9 protocol specifications.\n"
        "Identify the precise defect causing the compiler or solver failure and return a corrected "
        "CPSAProtocolSpecification matching the requested JSON schema."
    ),
    PROMPT_THINK_SYNTHESIZER: (
        "You are a formal methods expert in MITRE CPSA 4.4.9 synthesizing a first-person reasoning monologue "
        "(<think>...</think>) that derives a formally verified CPSA specification from verbatim IETF RFC prose.\n"
        "Never mention that you were provided the final AST or .scm output in advance; write strictly from a "
        "forward-looking, first-principles deduction perspective, incorporating compiler self-correction and "
        "backtracking steps where applicable."
    ),
}

_FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", re.DOTALL)


class PromptSpec(BaseModel):
    """Parsed prompt template and LLM execution parameters loaded from `prompts/<filename>`."""

    filename: str
    body: str
    model: str
    timeout: int = 1500
    max_tokens: int = 65536
    temperature: Optional[float] = None


def parse_prompt_frontmatter(raw_text: str) -> Tuple[Dict[str, Any], str]:
    """Splits optional leading `--- ... ---` YAML frontmatter from the Markdown prompt body."""
    stripped = raw_text.lstrip("\ufeff")
    match = _FRONTMATTER_RE.match(stripped)
    if not match:
        return {}, stripped.strip()

    yaml_block = match.group(1)
    body = stripped[match.end():].strip()
    try:
        parsed = yaml.safe_load(yaml_block)
        meta = parsed if isinstance(parsed, dict) else {}
    except Exception as exc:
        logger.warning("Invalid YAML frontmatter in prompt (%s); ignoring frontmatter block.", exc)
        meta = {}
    return meta, body


def load_prompt_spec(prompt_filename: str, prompts_dir: Optional[Path] = None) -> PromptSpec:
    """Loads a `PromptSpec` (model, timeout, temperature, stripped prompt body) dynamically from `prompts/`."""
    base_dir = prompts_dir or SYSTEM_CONFIG.PROMPTS_DIR
    prompt_path = base_dir / prompt_filename
    defaults = _FALLBACK_METADATA.get(prompt_filename, {})
    default_model = str(defaults.get("model") or GLOBAL_FALLBACK_MODEL)
    default_timeout = int(defaults.get("timeout") or SYSTEM_CONFIG.LLM_TIMEOUT_SECONDS)
    default_max_tokens = int(defaults.get("max_tokens") or 65536)
    default_temp = defaults.get("temperature")

    meta: Dict[str, Any] = {}
    body: str = ""

    if prompt_path.exists() and prompt_path.is_file():
        try:
            raw_content = prompt_path.read_text(encoding="utf-8")
            meta, body = parse_prompt_frontmatter(raw_content)
            if not body:
                logger.warning("Prompt body in %s is empty; using built-in fallback body.", prompt_path)
        except Exception as exc:
            logger.warning("Failed to read prompt file %s (%s); using built-in fallback.", prompt_path, exc)
    else:
        logger.debug("Prompt file %s not found; using built-in fallback.", prompt_path)

    if not body:
        if prompt_filename in _FALLBACK_PROMPTS:
            body = _FALLBACK_PROMPTS[prompt_filename]
        else:
            raise FileNotFoundError(f"Prompt template '{prompt_filename}' not found in {base_dir}")

    raw_model = meta.get("model")
    resolved_model = str(raw_model).strip() if raw_model and str(raw_model).strip() else default_model

    raw_timeout = meta.get("timeout")
    try:
        resolved_timeout = int(raw_timeout) if raw_timeout is not None else default_timeout
    except (TypeError, ValueError):
        resolved_timeout = default_timeout

    raw_max_tokens = meta.get("max_tokens")
    try:
        resolved_max_tokens = int(raw_max_tokens) if raw_max_tokens is not None else default_max_tokens
    except (TypeError, ValueError):
        resolved_max_tokens = default_max_tokens

    raw_temp = meta.get("temperature", default_temp)
    try:
        resolved_temp = float(raw_temp) if raw_temp is not None else None
    except (TypeError, ValueError):
        resolved_temp = default_temp

    return PromptSpec(
        filename=prompt_filename,
        body=body,
        model=resolved_model,
        timeout=resolved_timeout,
        max_tokens=resolved_max_tokens,
        temperature=resolved_temp,
    )


def resolve_prompt_model(
    prompt_filename: str,
    override_model: Optional[str] = None,
    prompts_dir: Optional[Path] = None,
) -> str:
    """Returns `override_model` if explicitly provided (e.g., via CLI flag), else the frontmatter `model`."""
    if override_model and override_model.strip():
        return override_model.strip()
    return load_prompt_spec(prompt_filename, prompts_dir=prompts_dir).model


def load_prompt(prompt_filename: str, prompts_dir: Optional[Path] = None) -> str:
    """Loads the Markdown prompt body (with YAML frontmatter stripped) from `prompts/<prompt_filename>`."""
    return load_prompt_spec(prompt_filename, prompts_dir=prompts_dir).body


def build_schema_system_prompt(
    prompt_filename: str,
    schema_model: Type[BaseModel],
    prompts_dir: Optional[Path] = None,
) -> str:
    """Loads a stripped base system prompt from `prompts/` and appends the mandatory Pydantic JSON schema."""
    base_prompt = load_prompt(prompt_filename, prompts_dir=prompts_dir)
    schema_json = json.dumps(schema_model.model_json_schema(), indent=2)
    return (
        f"{base_prompt}\n\n"
        "CRITICAL: Return a populated JSON instance object with the actual field values at the top level. "
        "Do NOT return the JSON Schema definition itself, and do NOT wrap your answer inside a 'properties' key.\n"
        f"Respond strictly with a valid JSON object matching this schema:\n{schema_json}"
    )


_THINK_TAG_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def _unwrap_schema_envelope(parsed: Any) -> Any:
    """Unwraps 1-element list wrappers or JSON-Schema `'properties'` envelopes if an LLM echoes schema structure."""
    if isinstance(parsed, list) and len(parsed) == 1 and isinstance(parsed[0], dict):
        parsed = parsed[0]

    if (
        isinstance(parsed, dict)
        and isinstance(parsed.get("properties"), dict)
        and any(k in parsed for k in ("type", "title", "description", "required", "$defs"))
        and "protocol_name" not in parsed
        and "is_cryptographic_protocol" not in parsed
        and "selected_section_ids" not in parsed
    ):
        props = parsed["properties"]
        unwrapped = {}
        for k, v in props.items():
            if isinstance(v, dict) and set(v.keys()).issubset({"type", "description", "title", "items", "default", "value", "const", "anyOf"}):
                if "value" in v:
                    unwrapped[k] = v["value"]
                elif "default" in v and v["default"] is not None:
                    unwrapped[k] = v["default"]
                elif "const" in v:
                    unwrapped[k] = v["const"]
                else:
                    unwrapped[k] = v
            else:
                unwrapped[k] = v
        return unwrapped

    return parsed


def parse_llm_json(raw_content: Optional[str]) -> Any:
    """Strips `<think>...</think>` reasoning blocks and markdown fences, then parses or repairs JSON."""
    import json_repair

    text = (raw_content or "").strip()
    if not text:
        return {}

    # 1. Strip complete <think>...</think> blocks
    cleaned = _THINK_TAG_RE.sub("", text).strip()
    # If an unclosed <think> tag preceded a JSON block, jump to the last `</think>` or first `{` after it
    if "</think>" in cleaned.lower():
        idx = cleaned.lower().rfind("</think>")
        cleaned = cleaned[idx + len("</think>") :].strip()
    elif cleaned.lower().startswith("<think>"):
        brace_idx = cleaned.find("{")
        if brace_idx != -1:
            cleaned = cleaned[brace_idx:].strip()

    # 2. Strip markdown ```json ... ``` fences if present
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    try:
        return _unwrap_schema_envelope(json.loads(cleaned))
    except Exception:
        # Extract from first '{' to last '}' if surrounded by prose
        first_brace = cleaned.find("{")
        last_brace = cleaned.rfind("}")
        if first_brace != -1 and last_brace > first_brace:
            candidate = cleaned[first_brace : last_brace + 1]
            try:
                return _unwrap_schema_envelope(json.loads(candidate))
            except Exception:
                return _unwrap_schema_envelope(json_repair.loads(candidate))
        return _unwrap_schema_envelope(json_repair.loads(cleaned))
````

---

### `src/rag_retriever_client.py`

*sha256:`681a399d2a50` · 1124 lines · 49.2 KB (~12,591 tokens) · lang:`python`*

```python
"""CPSA 4.4.9 Knowledge Base Indexer, `TOC.md` Flag Manager, and Agentic Searcher Client.

Replaces static vector-chunk RAG with a structured, zero-hallucination CPSA 4.4.9
Knowledge Base (`refrences/cpsa_kb/`) backed by:
1. `TOC.md` with a YAML frontmatter `rebuild_toc: true | false` flag that controls
   whether `TOC.md` and `kb_index.json` are rebuilt from disk on load (and automatically
   resets `rebuild_toc: false` after rebuilding).
2. Concept-split Markdown sections across `01_core_rules/`, `02_manuals/`, and
   `04_examples_catalog/` plus all 151 official MITRE `.scm` protocol files in
   `03_examples_scm/`.
3. In-memory DSL-aware BM25 + exact compiler-error phrase matching + optional in-process
   `FlashRank` ONNX cross-encoder reranking (zero external Ollama embedding dependency).
4. An Agentic Searcher LLM loop (`run_agentic_cpsa_searcher`) that inspects the failing
   `CPSAProtocolSpecification` AST + compiler diagnostic, invokes deterministic tools
   (`read_section`, `search_cpsa_docs`, `find_scm_examples`, `read_scm_example`), and
   returns verified manual rules, working `.scm` examples, and pinpointed AST fixes.
"""

from __future__ import annotations

from collections import Counter
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple
import json_repair
import litellm
import yaml

from src.logging_config import get_pipeline_logger
from src.pipeline_events import GLOBAL_EVENT_BUS
from src.prompt_loader import PROMPT_RAG_QUERY_FORMULATION, load_prompt_spec
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("rag_retriever")

CPSA_KB_DIR: Path = SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "cpsa_kb"
TOC_MD_PATH: Path = CPSA_KB_DIR / "TOC.md"
KB_INDEX_JSON_PATH: Path = CPSA_KB_DIR / "kb_index.json"

_GLOBAL_RETRIEVER: Optional["CPSAKnowledgeBase"] = None
LAST_RETRIEVED_CHUNK_IDS: List[str] = []
LAST_SEARCHER_QUERY: Optional[str] = None
LAST_SEARCHER_DIAGNOSIS: Optional[str] = None
LAST_SEARCHER_TRACE: List[Dict[str, Any]] = []
_SEARCH_CACHE: Dict[str, Tuple[str, str, List[str], Optional[str], List[Dict[str, Any]]]] = {}

_KNOWN_SORTS = {
    "name", "text", "data", "skey", "akey", "mesg", "chan", "locn",
    "rndx", "expt", "base", "tag", "dev", "strd", "indx", "fact",
}
_KNOWN_OPERATORS = {
    "enc", "hash", "cat", "pubk", "privk", "invk", "ltk", "bltk",
    "exp", "gen", "mul", "rec", "one", "send", "recv", "load", "stor",
}
_KNOWN_KEYWORDS = {
    "defprotocol", "defrole", "defskeleton", "defstrand", "defstrandmax",
    "deflistener", "defgoal", "defrule", "defgenrule", "deflemma", "defmacro",
    "herald", "vars", "trace", "inputs", "outputs", "non-orig", "pen-non-orig",
    "uniq-orig", "uniq-gen", "ugen-at", "uniq-at", "auth", "conf", "gen-st",
    "facts", "neq", "lt", "leads-to", "same-locn", "state-node", "trans",
    "ind-zero", "absent", "precur", "priority", "critical-sections", "lang",
}


def tokenize_cpsa_dsl(text: str) -> List[str]:
    """DSL-aware tokenizer preserving Scheme S-expression atoms, hyphenated keywords,
    and structural markers (e.g. defprotocol, non-orig, uniq-gen, cpsa4roletran).
    """
    text_lower = text.lower()
    tokens = re.findall(r"[a-zA-Z0-9_\-]+", text_lower)
    scheme_ops = re.findall(r"\(([a-zA-Z0-9_\-]+)", text_lower)
    tokens.extend(scheme_ops)
    return [t for t in tokens if len(t) > 1]


def _slugify_heading(heading: str) -> str:
    """Converts a Markdown heading string into a clean anchor slug."""
    cleaned = re.sub(r"[`*_~]", "", heading.strip())
    slug = re.sub(r"[^a-zA-Z0-9.\-_]+", "-", cleaned.lower()).strip("-")
    return slug[:64] or "section"


def parse_toc_rebuild_flag(toc_path: Path = TOC_MD_PATH) -> bool:
    """Reads `TOC.md` YAML frontmatter and returns True if `rebuild_toc` is True
    (or if `TOC.md` does not exist yet).
    """
    if not toc_path.exists():
        return True
    try:
        raw = toc_path.read_text(encoding="utf-8", errors="ignore")
        if not raw.startswith("---"):
            return True
        parts = raw.split("---", 2)
        if len(parts) < 3:
            return True
        meta = yaml.safe_load(parts[1])
        if not isinstance(meta, dict):
            return True
        flag = meta.get("rebuild_toc", False)
        if isinstance(flag, bool):
            return flag
        if isinstance(flag, str):
            return flag.strip().lower() in {"true", "yes", "1"}
        return bool(flag)
    except Exception as exc:
        logger.warning("Failed to parse rebuild_toc flag from %s (%s); defaulting to rebuild", toc_path, exc)
        return True


def _split_markdown_file_into_sections(
    md_path: Path,
    kb_dir: Path,
    category: str,
) -> List[Dict[str, Any]]:
    """Splits a Markdown file into self-contained conceptual sections at `## ` headings
    (and `### ` headings when a `## ` chapter exceeds 3,200 characters).
    """
    rel_path = md_path.relative_to(kb_dir).as_posix()
    file_stem = f"{category}/{md_path.stem}"
    raw_text = md_path.read_text(encoding="utf-8", errors="ignore").strip()
    if not raw_text:
        return []

    # Strip optional YAML frontmatter if present
    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)
        if len(parts) >= 3:
            raw_text = parts[2].strip()

    lines = raw_text.splitlines()
    doc_title = md_path.stem.replace("_", " ")
    for line in lines[:15]:
        if line.startswith("# "):
            doc_title = line[2:].strip()
            break

    # Split at top-level `## ` headings first
    h2_blocks: List[Tuple[str, List[str]]] = []
    cur_h2_title = "Overview"
    cur_h2_lines: List[str] = []

    for line in lines:
        if line.startswith("## "):
            if cur_h2_lines:
                h2_blocks.append((cur_h2_title, cur_h2_lines))
            cur_h2_title = line[3:].strip()
            cur_h2_lines = [line]
        else:
            cur_h2_lines.append(line)
    if cur_h2_lines:
        h2_blocks.append((cur_h2_title, cur_h2_lines))

    sections: List[Dict[str, Any]] = []
    seen_ids: Counter = Counter()

    for h2_title, h2_lines in h2_blocks:
        block_text = "\n".join(h2_lines).strip()
        if not block_text or len(block_text) < 40:
            continue

        # If a manual chapter is large (>3,200 chars) and has `### ` sub-headings, split by `### `
        has_h3 = any(l.startswith("### ") for l in h2_lines)
        if category == "02_manuals" and len(block_text) > 3200 and has_h3:
            cur_h3_title = h2_title
            cur_h3_lines: List[str] = []
            h3_blocks: List[Tuple[str, List[str]]] = []
            for l in h2_lines:
                if l.startswith("### "):
                    if cur_h3_lines:
                        h3_blocks.append((cur_h3_title, cur_h3_lines))
                    cur_h3_title = f"{h2_title} > {l[4:].strip()}"
                    cur_h3_lines = [f"## {h2_title}", l]
                else:
                    cur_h3_lines.append(l)
            if cur_h3_lines:
                h3_blocks.append((cur_h3_title, cur_h3_lines))

            for sub_title, sub_lines in h3_blocks:
                sub_text = "\n".join(sub_lines).strip()
                if len(sub_text) < 40:
                    continue
                slug = _slugify_heading(sub_title.split(">")[-1])
                base_id = f"{file_stem}#{slug}"
                seen_ids[base_id] += 1
                sec_id = base_id if seen_ids[base_id] == 1 else f"{base_id}-{seen_ids[base_id]}"
                sections.append({
                    "section_id": sec_id,
                    "category": category,
                    "source_file": rel_path,
                    "doc_title": doc_title,
                    "title": sub_title,
                    "content": sub_text,
                })
        else:
            slug = _slugify_heading(h2_title)
            base_id = f"{file_stem}#{slug}"
            seen_ids[base_id] += 1
            sec_id = base_id if seen_ids[base_id] == 1 else f"{base_id}-{seen_ids[base_id]}"
            sections.append({
                "section_id": sec_id,
                "category": category,
                "source_file": rel_path,
                "doc_title": doc_title,
                "title": h2_title,
                "content": block_text,
            })

    return sections


def _extract_scm_metadata_from_source(scm_path: Path, kb_dir: Path) -> Dict[str, Any]:
    """Deterministically parses a `.scm` file to extract algebra, herald flags, protocols,
    roles, sorts, operators, keywords, and header comment summary.
    """
    raw = scm_path.read_text(encoding="utf-8", errors="ignore")
    rel_path = scm_path.relative_to(kb_dir).as_posix()

    # Extract leading `;` comments for summary
    comment_lines: List[str] = []
    for line in raw.splitlines()[:25]:
        stripped = line.strip()
        if stripped.startswith(";"):
            cleaned = stripped.lstrip(";").strip()
            if cleaned and not cleaned.lower().startswith("copyright"):
                comment_lines.append(cleaned)
        elif stripped and not stripped.startswith("(herald"):
            break

    algebra = "diffie-hellman" if "diffie-hellman" in raw else "basic"
    protocols = re.findall(r"\(\s*defprotocol\s+([a-zA-Z0-9_\-]+)", raw)
    roles = list(dict.fromkeys(re.findall(r"\(\s*defrole\s+([a-zA-Z0-9_\-]+)", raw)))

    tokens_set = set(tokenize_cpsa_dsl(raw))
    sorts_used = sorted(tokens_set & _KNOWN_SORTS)
    operators_used = sorted(tokens_set & _KNOWN_OPERATORS)
    keywords_used = sorted(tokens_set & _KNOWN_KEYWORDS)

    herald_flags: List[str] = []
    for flag in ("bound", "limit", "depth", "goals-sat", "try-old-strands", "reverse-nodes", "check-nonces", "algebra"):
        if re.search(rf"\(\s*{flag}\b", raw):
            herald_flags.append(flag)

    summary = " ".join(comment_lines[:3])[:260] or f"Official MITRE CPSA {algebra} example ({scm_path.name})"
    return {
        "example_id": rel_path,
        "filename": scm_path.name,
        "protocol_names": protocols,
        "algebra": algebra,
        "herald_flags": herald_flags,
        "roles": roles,
        "sorts_used": sorts_used,
        "operators_used": operators_used,
        "keywords_used": keywords_used,
        "uses_channels": bool({"chan", "auth", "conf"} & tokens_set),
        "uses_state_locn": bool({"locn", "load", "stor", "gen-st"} & tokens_set),
        "uses_goals": "defgoal" in tokens_set,
        "uses_rules_or_lemmas": bool({"defrule", "defgenrule", "deflemma"} & tokens_set),
        "uses_macros": "defmacro" in tokens_set,
        "has_roletran_declarations": bool({"inputs", "outputs"} & tokens_set),
        "summary": summary,
    }


def build_cpsa_kb_index(kb_dir: Path = CPSA_KB_DIR) -> Dict[str, Any]:
    """Scans all Markdown guides/manuals/catalogs and `.scm` examples in `kb_dir`,
    writes `kb_index.json`, and writes `TOC.md` with `rebuild_toc: false`.
    """
    kb_dir.mkdir(parents=True, exist_ok=True)
    sections: List[Dict[str, Any]] = []

    for category in ("01_core_rules", "02_manuals", "04_examples_catalog"):
        cat_dir = kb_dir / category
        if not cat_dir.exists():
            continue
        for md_file in sorted(cat_dir.glob("*.md")):
            sections.extend(_split_markdown_file_into_sections(md_file, kb_dir, category))

    # Load curated batch*_meta.json if available, then merge with all .scm files in 03_examples_scm/
    curated_scm_meta: Dict[str, Dict[str, Any]] = {}
    catalog_dir = kb_dir / "04_examples_catalog"
    if catalog_dir.exists():
        for meta_file in sorted(catalog_dir.glob("batch*_meta.json")):
            try:
                items = json.loads(meta_file.read_text(encoding="utf-8", errors="ignore"))
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict) and item.get("filename"):
                            curated_scm_meta[item["filename"]] = item
            except Exception as exc:
                logger.warning("Could not parse %s: %s", meta_file, exc)

    scm_examples: List[Dict[str, Any]] = []
    scm_dir = kb_dir / "03_examples_scm"
    if scm_dir.exists():
        for scm_file in sorted(scm_dir.glob("*.scm")):
            auto_meta = _extract_scm_metadata_from_source(scm_file, kb_dir)
            if scm_file.name in curated_scm_meta:
                merged = {**auto_meta, **curated_scm_meta[scm_file.name]}
                merged["example_id"] = auto_meta["example_id"]
                merged["filename"] = scm_file.name
            else:
                merged = auto_meta
            scm_examples.append(merged)

    built_iso = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    index_payload = {
        "schema_version": "2.0.0",
        "built_at": built_iso,
        "total_sections": len(sections),
        "total_scm_examples": len(scm_examples),
        "sections": sections,
        "scm_examples": scm_examples,
    }

    index_path = kb_dir / "kb_index.json"
    index_path.write_text(json.dumps(index_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Build human- and LLM-readable TOC.md with rebuild_toc: false frontmatter flag
    toc_lines: List[str] = [
        "---",
        "# CPSA 4.4.9 Knowledge Base Master Table of Contents",
        "# Flip `rebuild_toc: true` whenever you add or edit .md or .scm files in refrences/cpsa_kb/.",
        "# On the next run, the loader will automatically rebuild TOC.md + kb_index.json and reset `rebuild_toc: false`.",
        "rebuild_toc: false",
        f'last_built: "{built_iso}"',
        f"total_sections: {len(sections)}",
        f"total_scm_examples: {len(scm_examples)}",
        "---",
        "",
        "# MITRE CPSA 4.4.9 Knowledge Base — Master Table of Contents",
        "",
    ]

    for cat_key, cat_header in (
        ("01_core_rules", "## 1. Core Operational Rules & Schema Mapping (`01_core_rules/`)"),
        ("02_manuals", "## 2. Official MITRE CPSA 4.4.9 Manuals (`02_manuals/`)"),
        ("04_examples_catalog", "## 3. Official `.scm` Examples Catalog (`04_examples_catalog/`)"),
    ):
        cat_secs = [s for s in sections if s["category"] == cat_key]
        if not cat_secs:
            continue
        toc_lines.append(cat_header)
        by_file: Dict[str, List[Dict[str, Any]]] = {}
        for s in cat_secs:
            by_file.setdefault(s["source_file"], []).append(s)
        for src_file, file_secs in by_file.items():
            toc_lines.append(f"\n### `{src_file}` ({file_secs[0]['doc_title']})")
            for s in file_secs:
                toc_lines.append(f"- `{s['section_id']}` — {s['title']}")
        toc_lines.append("")

    if scm_examples:
        dh_ex = [e["filename"] for e in scm_examples if e.get("algebra") == "diffie-hellman"]
        chan_ex = [e["filename"] for e in scm_examples if e.get("uses_channels")]
        state_ex = [e["filename"] for e in scm_examples if e.get("uses_state_locn")]
        goal_ex = [e["filename"] for e in scm_examples if e.get("uses_goals")]
        rule_ex = [e["filename"] for e in scm_examples if e.get("uses_rules_or_lemmas")]
        roletran_ex = [e["filename"] for e in scm_examples if e.get("has_roletran_declarations")]
        toc_lines.extend([
            "## 4. Indexed `.scm` Protocol Examples by Feature (`03_examples_scm/`)",
            f"- **Diffie-Hellman (`diffie-hellman`, `rndx`, `uniq-gen`, `exp`) [{len(dh_ex)} files]**: {', '.join(dh_ex)}",
            f"- **Roletran Procedural Inputs/Outputs (`inputs`, `outputs`, `chan`) [{len(roletran_ex)} files]**: {', '.join(roletran_ex)}",
            f"- **Channels (`chan`, `auth`, `conf`) [{len(chan_ex)} files]**: {', '.join(chan_ex)}",
            f"- **Stateful Memory Locations (`locn`, `load`, `stor`, `gen-st`) [{len(state_ex)} files]**: {', '.join(state_ex)}",
            f"- **Security Goals (`defgoal`) [{len(goal_ex)} files]**: {', '.join(goal_ex)}",
            f"- **Axiom Rules & Lemmas (`defrule`, `defgenrule`, `deflemma`) [{len(rule_ex)} files]**: {', '.join(rule_ex)}",
            "",
        ])

    toc_path = kb_dir / "TOC.md"
    toc_path.write_text("\n".join(toc_lines), encoding="utf-8")
    logger.info(
        "Built CPSA Knowledge Base index (%d sections, %d .scm examples) and set rebuild_toc=false in %s",
        len(sections),
        len(scm_examples),
        toc_path,
    )
    return index_payload


class CPSAKnowledgeBase:
    """In-memory CPSA 4.4.9 Knowledge Base supporting TOC section lookup, DSL-aware BM25 +
    exact compiler-error substring boost + optional FlashRank ONNX cross-encoder reranking,
    and operator-indexed `.scm` example retrieval.
    """

    def __init__(self, kb_dir: Path = CPSA_KB_DIR):
        self.kb_dir = Path(kb_dir)
        self.toc_path = self.kb_dir / "TOC.md"
        self.index_path = self.kb_dir / "kb_index.json"

        if parse_toc_rebuild_flag(self.toc_path) or not self.index_path.exists():
            payload = build_cpsa_kb_index(self.kb_dir)
        else:
            try:
                payload = json.loads(self.index_path.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                payload = build_cpsa_kb_index(self.kb_dir)

        self.sections: List[Dict[str, Any]] = payload.get("sections", [])
        self.scm_examples: List[Dict[str, Any]] = payload.get("scm_examples", [])
        self.section_by_id: Dict[str, Dict[str, Any]] = {
            s["section_id"]: s for s in self.sections if s.get("section_id")
        }
        self.scm_by_name: Dict[str, Dict[str, Any]] = {}
        for ex in self.scm_examples:
            self.scm_by_name[ex["filename"]] = ex
            self.scm_by_name[ex["example_id"]] = ex

        # Build compact navigator map for the Agentic Searcher LLM prompt
        self.compact_toc_map: str = self._build_compact_searcher_map()

        # Build DSL-BM25 lexical index over all sections
        self.doc_tokens: List[List[str]] = []
        self.doc_term_freqs: List[Counter] = []
        self.term_doc_freqs: Counter = Counter()
        self.doc_lengths: List[int] = []
        for sec in self.sections:
            combined = f"{sec.get('section_id', '')} {sec.get('title', '')} {sec.get('doc_title', '')} {sec.get('content', '')}"
            toks = tokenize_cpsa_dsl(combined)
            tf = Counter(toks)
            self.doc_tokens.append(toks)
            self.doc_term_freqs.append(tf)
            self.doc_lengths.append(len(toks))
            for term in tf:
                self.term_doc_freqs[term] += 1

        self.total_docs = len(self.sections)
        self.avg_doc_len = (sum(self.doc_lengths) / self.total_docs) if self.total_docs else 1.0

        # Lazy-loaded local in-process ONNX cross-encoder reranker (FlashRank)
        self._ranker = None
        self._ranker_initialized = False

    def _get_ranker(self):
        if not self._ranker_initialized:
            self._ranker_initialized = True
            try:
                from flashrank import Ranker
                self._ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")
            except Exception:
                self._ranker = None
        return self._ranker

    def _build_compact_searcher_map(self) -> str:
        """Builds a compact (~700-token) directory of `01_core_rules/`, `02_manuals/`,
        and `.scm` categories for the Agentic Searcher LLM's system prompt.
        """
        lines: List[str] = ["AVAILABLE CPSA 4.4.9 KNOWLEDGE BASE SECTIONS:"]
        core_secs = [s for s in self.sections if s.get("category") == "01_core_rules"]
        for s in core_secs:
            lines.append(f"  - {s['section_id']} : {s['title']}")

        manual_files: Dict[str, List[str]] = {}
        for s in self.sections:
            if s.get("category") == "02_manuals":
                manual_files.setdefault(s["source_file"], []).append(s["section_id"])
        if manual_files:
            lines.append("\nOFFICIAL MANUAL CHAPTERS (`02_manuals/`):")
            for src, sids in manual_files.items():
                sample_ids = ", ".join(sids[:5])
                more = f" (+{len(sids) - 5} more)" if len(sids) > 5 else ""
                lines.append(f"  - {src}: {sample_ids}{more}")

        dh_files = [e["filename"] for e in self.scm_examples if e.get("algebra") == "diffie-hellman"]
        roletran_files = [e["filename"] for e in self.scm_examples if e.get("has_roletran_declarations")]
        chan_files = [e["filename"] for e in self.scm_examples if e.get("uses_channels")]
        state_files = [e["filename"] for e in self.scm_examples if e.get("uses_state_locn")]
        lines.extend([
            f"\nINDEXED OFFICIAL .SCM EXAMPLES ({len(self.scm_examples)} files in `03_examples_scm/` & `04_examples_catalog/`):",
            f"  - Diffie-Hellman examples: {', '.join(dh_files[:12])}",
            f"  - Roletran (inputs/outputs/chan) examples: {', '.join(roletran_files[:12])}",
            f"  - Channel (auth/conf) examples: {', '.join(chan_files[:10])}",
            f"  - Stateful (locn/load/stor/gen-st) examples: {', '.join(state_files[:10])}",
        ])
        return "\n".join(lines)

    def read_section(self, section_id: str) -> Optional[Dict[str, Any]]:
        """Tool 1: Looks up a Markdown section by exact or partial `section_id`."""
        if not section_id:
            return None
        target = section_id.strip().strip("`'\"")
        if target in self.section_by_id:
            return self.section_by_id[target]

        # Fuzzy suffix or substring match
        target_low = target.lower()
        for sid, sec in self.section_by_id.items():
            if sid.lower() == target_low or sid.lower().endswith(target_low) or target_low in sid.lower():
                return sec
        return None

    def search_cpsa_docs(
        self,
        query: str,
        category: str = "all",
        top_k: int = 3,
        rerank: bool = True,
    ) -> List[Dict[str, Any]]:
        """Tool 2: Searches Markdown sections using DSL-BM25 + exact error phrase boosting
        + optional in-process FlashRank ONNX cross-encoder reranking.
        """
        if not self.sections:
            return []

        q_tokens = tokenize_cpsa_dsl(query)
        q_lower = query.lower().strip()
        k1 = 1.5
        b = 0.75

        scored: List[Tuple[float, int]] = []
        for idx, sec in enumerate(self.sections):
            if category != "all" and sec.get("category") != category:
                continue

            tf_map = self.doc_term_freqs[idx]
            doc_len = self.doc_lengths[idx] or 1
            score = 0.0

            for tok in q_tokens:
                df = self.term_doc_freqs.get(tok, 0)
                if df == 0:
                    continue
                idf = math.log(1.0 + (self.total_docs - df + 0.5) / (df + 0.5))
                tf = tf_map.get(tok, 0)
                if tf > 0:
                    score += idf * ((tf * (k1 + 1.0)) / (tf + k1 * (1.0 - b + b * (doc_len / self.avg_doc_len))))

            title_low = sec.get("title", "").lower()
            content_low = sec.get("content", "").lower()

            # Boost core rules and exact title/phrase matches
            if sec.get("category") == "01_core_rules":
                score *= 1.35
            for tok in q_tokens:
                if tok in title_low:
                    score += 3.5
            if len(q_lower) >= 6 and q_lower in content_low:
                score += 12.0

            if score > 0:
                scored.append((score, idx))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        candidate_indices = [idx for _, idx in scored[: max(top_k * 4, 12)]]
        if not candidate_indices:
            candidate_indices = list(range(min(top_k, len(self.sections))))

        ranker = self._get_ranker() if rerank else None
        if ranker is not None and len(candidate_indices) > top_k:
            try:
                from flashrank import RerankRequest
                passages = [
                    {
                        "id": idx,
                        "text": f"{self.sections[idx]['title']}\n{self.sections[idx]['content'][:1500]}",
                    }
                    for idx in candidate_indices
                ]
                reranked = ranker.rerank(RerankRequest(query=query, passages=passages))
                bm25_ranks = {idx: rank for rank, idx in enumerate(candidate_indices, 1)}
                ce_ranks = {int(item["id"]): rank for rank, item in enumerate(reranked, 1)}
                fused = sorted(
                    candidate_indices,
                    key=lambda i: (1.0 / (20 + bm25_ranks.get(i, 50))) + (1.0 / (20 + ce_ranks.get(i, 50))),
                    reverse=True,
                )
                return [self.sections[i] for i in fused[:top_k]]
            except Exception:
                pass

        return [self.sections[i] for i in candidate_indices[:top_k]]

    def find_scm_examples(
        self,
        algebra: Optional[str] = None,
        operators: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        query: Optional[str] = None,
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """Tool 3: Filters and ranks the 151 official MITRE `.scm` examples by algebra,
        operators, assumption/goal keywords, and free-text query.
        """
        q_tokens = set(tokenize_cpsa_dsl(query or ""))
        req_ops = {op.lower().strip() for op in (operators or []) if op}
        req_kws = {kw.lower().strip() for kw in (keywords or []) if kw}
        req_alg = algebra.lower().strip() if algebra else None

        scored: List[Tuple[float, Dict[str, Any]]] = []
        for ex in self.scm_examples:
            score = 0.0
            ex_alg = (ex.get("algebra") or "basic").lower()
            if req_alg and req_alg in {"basic", "diffie-hellman"}:
                if ex_alg == req_alg:
                    score += 5.0
                else:
                    continue

            ex_ops = set(ex.get("operators_used") or [])
            ex_kws = set(ex.get("keywords_used") or [])
            ex_sorts = set(ex.get("sorts_used") or [])
            all_tags = ex_ops | ex_kws | ex_sorts

            for op in req_ops:
                if op in all_tags:
                    score += 4.0
            for kw in req_kws:
                if kw in all_tags:
                    score += 4.0

            haystack = f"{ex.get('filename', '')} {' '.join(ex.get('protocol_names') or [])} {ex.get('summary', '')}".lower()
            for qt in q_tokens:
                if qt in all_tags:
                    score += 3.0
                if qt in haystack:
                    score += 2.5

            if ex.get("has_roletran_declarations"):
                score += 0.5

            if score > 0 or not (req_ops or req_kws or q_tokens):
                scored.append((score, ex))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [ex for _, ex in scored[:top_k]]

    def read_scm_example(self, filename_or_id: str) -> Optional[Dict[str, Any]]:
        """Tool 4: Reads the full verbatim `.scm` code and catalog entry for a MITRE `.scm` example."""
        if not filename_or_id:
            return None
        key = Path(filename_or_id.strip().strip("`'\"")).name
        ex = self.scm_by_name.get(key) or self.scm_by_name.get(filename_or_id.strip())
        if not ex:
            for cand_name, cand_ex in self.scm_by_name.items():
                if key.lower() in cand_name.lower():
                    ex = cand_ex
                    break
        if not ex:
            return None

        scm_file = self.kb_dir / ex["example_id"]
        scm_code = scm_file.read_text(encoding="utf-8", errors="ignore") if scm_file.exists() else ""
        return {
            **ex,
            "scm_code": scm_code,
        }

    def search(
        self,
        query: str,
        top_k: int = 2,
        mode: str = "hybrid",
        rerank: bool = True,
    ) -> List[Dict[str, Any]]:
        """Backward-compatible `.search()` interface returning standard chunk dicts."""
        hits = self.search_cpsa_docs(query=query, category="all", top_k=top_k, rerank=rerank)
        results: List[Dict[str, Any]] = []
        for sec in hits:
            results.append({
                "chunk_id": sec["section_id"],
                "title": sec["title"],
                "source_file": sec["source_file"],
                "text": sec["content"],
            })
        return results


def get_cpsa_manual_retriever(force_reload: bool = False) -> Optional[CPSAKnowledgeBase]:
    """Returns the lazy-loaded singleton `CPSAKnowledgeBase` instance, automatically rebuilding
    `TOC.md` and `kb_index.json` if `rebuild_toc: true` is set in `TOC.md`.
    """
    global _GLOBAL_RETRIEVER
    if _GLOBAL_RETRIEVER is None or force_reload or parse_toc_rebuild_flag(TOC_MD_PATH):
        try:
            _GLOBAL_RETRIEVER = CPSAKnowledgeBase(CPSA_KB_DIR)
            logger.info(
                "Initialized CPSAKnowledgeBase (%d sections, %d .scm examples)",
                len(_GLOBAL_RETRIEVER.sections),
                len(_GLOBAL_RETRIEVER.scm_examples),
            )
        except Exception as exc:
            logger.warning("Could not initialize CPSAKnowledgeBase: %s", exc)
            _GLOBAL_RETRIEVER = None
    return _GLOBAL_RETRIEVER


def retrieve_cpsa_manual_guidance(
    query: str,
    stage: int,
    purpose: str,
    header_prefix: str = "Reference",
    top_k: int = 2,
    fallback_message: str = "Use standard MITRE CPSA 4.4.9 syntax conventions.",
) -> str:
    """Executes a search over `CPSAKnowledgeBase`, emits a `rag_retrieval` telemetry event,
    and returns formatted reference blocks.
    """
    global LAST_RETRIEVED_CHUNK_IDS, LAST_SEARCHER_QUERY
    LAST_RETRIEVED_CHUNK_IDS = []
    LAST_SEARCHER_QUERY = query
    kb = get_cpsa_manual_retriever()
    if not kb:
        return fallback_message

    try:
        search_hits = kb.search(query, top_k=top_k, rerank=True)
        formatted_blocks: List[str] = []
        telemetry_chunks: List[dict] = []

        for idx, chunk in enumerate(search_hits, 1):
            chunk_id = str(chunk.get("chunk_id") or idx)
            chunk_title = chunk.get("title") or f"Section {idx}"
            chunk_source = chunk.get("source_file") or "CPSA Knowledge Base"
            chunk_text = chunk.get("text") or ""

            LAST_RETRIEVED_CHUNK_IDS.append(chunk_id)
            formatted_blocks.append(
                f"--- {header_prefix} {idx}: {chunk_title} ({chunk_source}) ---\n{chunk_text[:1800]}"
            )
            telemetry_chunks.append({
                "chunk_id": chunk_id,
                "title": chunk_title,
                "source_file": chunk_source,
                "snippet": chunk_text[:280].strip() + ("..." if len(chunk_text) > 280 else ""),
            })

        GLOBAL_EVENT_BUS.emit(
            "rag_retrieval",
            stage=stage,
            purpose=purpose,
            query=query,
            chunks=telemetry_chunks,
        )
        if formatted_blocks:
            return "\n\n".join(formatted_blocks)
    except Exception as exc:
        logger.warning("Knowledge base retrieval failed during %s: %s", purpose, exc)

    return fallback_message


def _term_to_compact_sexpr(term: Any) -> str:
    """Formats a JSON prefix term tree as a compact S-expression string for Searcher inspection."""
    if isinstance(term, list):
        return "(" + " ".join(_term_to_compact_sexpr(sub) for sub in term) + ")"
    return str(term)


def _summarize_failing_ast_for_searcher(failing_spec: Any) -> str:
    """Produces a compact structural summary of the failing `CPSAProtocolSpecification`
    so the Searcher LLM can inspect role variables, sorts, trace events (`send`/`recv`),
    inputs/outputs/origination, and skeleton declarations without raw JSON noise.
    """
    try:
        data = failing_spec.model_dump() if hasattr(failing_spec, "model_dump") else dict(failing_spec)
        lines = [
            f"Protocol: {data.get('protocol_name')} | Algebra: {data.get('message_algebra', 'basic')}",
        ]
        for r in data.get("roles", []):
            vars_str = ", ".join(f"{v['name']}:{v['sort']}" for v in r.get("variables", []))
            trace_events = []
            for ev in r.get("trace", []):
                direction = ev.get("direction", "?")
                ch = ev.get("channel")
                msg_str = _term_to_compact_sexpr(ev.get("message_term"))
                if len(msg_str) > 600:
                    msg_str = msg_str[:597] + "..."
                trace_events.append(f"({direction}{f' {ch}' if ch else ''} {msg_str})")
            lines.append(
                f"  Role '{r.get('role_name')}': vars=[{vars_str}] | "
                f"roletran_inputs={r.get('inputs', [])} | procedural_outputs={r.get('outputs', [])} | "
                f"uniq_orig={r.get('unique_originating', [])} | uniq_gen={r.get('unique_generated', [])} | "
                f"non_orig={r.get('non_originating', [])} | trace=[{'; '.join(trace_events)}]"
            )
        for idx, sk in enumerate(data.get("skeletons", []), 1):
            strands_str = ", ".join(s.get("role_name", "?") for s in sk.get("strands", []))
            lines.append(
                f"  Skeleton #{idx}: strands=[{strands_str}] | listeners={sk.get('listeners', [])} | "
                f"non_orig={sk.get('non_originating', [])} | uniq_orig={sk.get('unique_originating', [])} | "
                f"uniq_gen={sk.get('unique_generated', [])} | facts={sk.get('facts', [])}"
            )
        return "\n".join(lines)
    except Exception:
        return "AST summary unavailable."


def run_agentic_cpsa_searcher(
    error_diagnostic: str,
    failure_stage: str,
    failing_spec: Optional[Any] = None,
    model: Optional[str] = None,
    cycle_detected: bool = False,
    fallback_query_fn: Optional[Any] = None,
) -> str:
    """Runs the Agentic CPSA Knowledge Base Searcher (`05_rag_query_formulation.md`).

    The Searcher LLM inspects the Master TOC map, the failing AST summary, and the
    compiler diagnostic, invokes deterministic KB tools (`read_section`, `search_cpsa_docs`,
    `find_scm_examples`, `read_scm_example`), and returns verified CPSA rules, working
    `.scm` examples, and a pinpointed AST fix brief for the Stage 5/6 Repair LLM.
    """
    global LAST_RETRIEVED_CHUNK_IDS, LAST_SEARCHER_QUERY, LAST_SEARCHER_DIAGNOSIS, LAST_SEARCHER_TRACE
    LAST_RETRIEVED_CHUNK_IDS = []
    LAST_SEARCHER_DIAGNOSIS = None
    LAST_SEARCHER_TRACE = []
    kb = get_cpsa_manual_retriever()
    if not kb:
        return "Review standard MITRE CPSA 4.4.9 executability and preskeleton assumption rules."

    ast_summary = _summarize_failing_ast_for_searcher(failing_spec) if failing_spec is not None else ""
    proto_name = getattr(failing_spec, "protocol_name", "") if failing_spec is not None else ""
    diag_for_key = re.sub(r"\(at \.scm line.*?\)", "", error_diagnostic[:220]).strip()
    diag_for_key = re.sub(r"Undeclared variable\s+\S+", "Undeclared variable <VAR>", diag_for_key)
    diag_for_key = re.sub(r"[0-9]+", "#", diag_for_key)
    ast_hash = (
        hashlib.sha256(proto_name.encode("utf-8")).hexdigest()[:16]
        if "Undeclared variable <VAR>" in diag_for_key
        else hashlib.sha256(ast_summary.encode("utf-8")).hexdigest()[:16]
    )

    # Normalize error signature AND include AST hash so AST-specific diagnoses never bleed across RFCs
    norm_sig = f"{failure_stage}:{ast_hash}:{diag_for_key}"
    if not cycle_detected and norm_sig in _SEARCH_CACHE:
        cached_query, cached_guidance, cached_ids, cached_diag, cached_trace = _SEARCH_CACHE[norm_sig]
        LAST_SEARCHER_QUERY = cached_query
        LAST_RETRIEVED_CHUNK_IDS = list(cached_ids)
        LAST_SEARCHER_DIAGNOSIS = cached_diag
        LAST_SEARCHER_TRACE = list(cached_trace)
        return cached_guidance

    searcher_spec = load_prompt_spec(PROMPT_RAG_QUERY_FORMULATION)
    searcher_model = model or searcher_spec.model
    sampling_temp = searcher_spec.temperature

    algebra_hint = getattr(failing_spec, "message_algebra", "basic") if failing_spec is not None else "basic"

    collected_sections: Dict[str, Dict[str, Any]] = {}
    collected_examples: Dict[str, Dict[str, Any]] = {}
    searcher_diagnosis: Optional[str] = None
    executed_queries: List[str] = []
    searcher_turns: List[Dict[str, Any]] = []

    # Step 1: Ask the Searcher LLM which KB tools/sections to inspect (up to 2 turns)
    user_context = (
        f"{kb.compact_toc_map}\n\n"
        f"FAILURE STAGE: {failure_stage}\n"
        f"CYCLE DETECTED: {cycle_detected}\n"
        f"COMPILER DIAGNOSTIC:\n{error_diagnostic}\n\n"
        f"FAILING PROTOCOL AST SUMMARY:\n{ast_summary}\n"
    )

    messages = [
        {"role": "system", "content": searcher_spec.body},
        {"role": "user", "content": user_context},
    ]

    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            searcher_model,
            temperature=sampling_temp,
            max_tokens=searcher_spec.max_tokens,
        )
        for turn_idx in range(2):
            resp = litellm.completion(
                **llm_kwargs,
                messages=messages,
                timeout=searcher_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(
                resp,
                role="query",
                model_name=searcher_model,
                stage=5 if failure_stage == "roletran" else 6,
            )
            raw_reply = (resp.choices[0].message.content or "").strip()
            if not raw_reply:
                break

            # Support both structured JSON tool-action replies and plain search query replies
            parsed_json = None
            if "{" in raw_reply and "}" in raw_reply:
                try:
                    parsed_json = json.loads(raw_reply)
                except Exception:
                    try:
                        parsed_json = json_repair.loads(raw_reply)
                    except Exception:
                        parsed_json = None

            if isinstance(parsed_json, dict) and (
                "tool_calls" in parsed_json or "actions" in parsed_json or "ast_root_cause" in parsed_json
            ):
                root_cause_str = parsed_json.get("ast_root_cause") or parsed_json.get("diagnosis") or ""
                fix_str = parsed_json.get("actionable_fix") or parsed_json.get("fix_instructions") or ""
                if root_cause_str or fix_str:
                    searcher_diagnosis = (
                        f"Root Cause in AST: {root_cause_str}\n"
                        f"Recommended AST Fix: {fix_str}"
                    ).strip()

                tool_calls = parsed_json.get("tool_calls") or parsed_json.get("actions") or []
                tool_feedback_blocks: List[str] = []
                turn_tool_log: List[Dict[str, Any]] = []

                for call in tool_calls[:4]:
                    if not isinstance(call, dict):
                        continue
                    t_name = (call.get("tool") or call.get("action") or "").strip()
                    if t_name == "read_section":
                        sec_id = call.get("section_id") or call.get("id") or ""
                        executed_queries.append(f"read_section({sec_id})")
                        sec = kb.read_section(sec_id)
                        if sec:
                            collected_sections[sec["section_id"]] = sec
                            tool_feedback_blocks.append(
                                f"[Section {sec['section_id']}: {sec['title']}]\n{sec['content'][:1600]}"
                            )
                            turn_tool_log.append({
                                "tool": "read_section",
                                "args": sec_id,
                                "retrieved": f"{sec['section_id']} ({sec['title']})",
                            })
                        else:
                            turn_tool_log.append({
                                "tool": "read_section",
                                "args": sec_id,
                                "retrieved": "No matching section found",
                            })
                    elif t_name == "search_cpsa_docs":
                        q = call.get("query") or ""
                        cat = call.get("category") or "all"
                        if q:
                            executed_queries.append(q)
                            hits = kb.search_cpsa_docs(q, category=cat, top_k=2)
                            hit_labels: List[str] = []
                            for sec in hits:
                                collected_sections[sec["section_id"]] = sec
                                hit_labels.append(f"{sec['section_id']} ({sec['title']})")
                                tool_feedback_blocks.append(
                                    f"[Section {sec['section_id']}: {sec['title']}]\n{sec['content'][:1400]}"
                                )
                            turn_tool_log.append({
                                "tool": "search_cpsa_docs",
                                "args": f"query='{q}', category='{cat}'",
                                "retrieved": ", ".join(hit_labels) or "0 hits",
                            })
                    elif t_name in {"find_scm_examples", "read_scm_example"}:
                        fname = call.get("filename") or call.get("example_id")
                        if fname:
                            ex = kb.read_scm_example(fname)
                            if ex:
                                executed_queries.append(f"read_scm_example({ex['filename']})")
                                collected_examples[ex["example_id"]] = ex
                                tool_feedback_blocks.append(
                                    f"[Example {ex['filename']} ({ex['algebra']})]\n{ex.get('scm_code', '')[:1400]}"
                                )
                                turn_tool_log.append({
                                    "tool": "read_scm_example",
                                    "args": fname,
                                    "retrieved": f"{ex['filename']} ({ex['algebra']}): {ex.get('summary', '')[:120]}",
                                })
                        else:
                            alg = call.get("algebra") or algebra_hint
                            ops = call.get("operators") or []
                            kws = call.get("keywords") or []
                            q = call.get("query") or ""
                            executed_queries.append(f"find_scm({alg}, ops={ops}, kws={kws})")
                            matches = kb.find_scm_examples(algebra=alg, operators=ops, keywords=kws, query=q, top_k=2)
                            match_names: List[str] = []
                            for match_ex in matches:
                                full_ex = kb.read_scm_example(match_ex["filename"])
                                if full_ex:
                                    collected_examples[full_ex["example_id"]] = full_ex
                                    match_names.append(f"{full_ex['filename']} ({full_ex['algebra']})")
                                    tool_feedback_blocks.append(
                                        f"[Example {full_ex['filename']} ({full_ex['algebra']})]\n{full_ex.get('scm_code', '')[:1400]}"
                                    )
                            turn_tool_log.append({
                                "tool": "find_scm_examples",
                                "args": f"algebra={alg}, ops={ops}, kws={kws}",
                                "retrieved": ", ".join(match_names) or "0 examples",
                            })

                is_final_turn = bool(parsed_json.get("is_final") or not tool_feedback_blocks or turn_idx == 1)
                searcher_turns.append({
                    "turn": turn_idx + 1,
                    "is_final": is_final_turn,
                    "status": "Final Diagnosis & Evidence Ready" if is_final_turn else "Ingested Tool Results -> Requesting Follow-up Synthesis",
                    "ast_root_cause": root_cause_str,
                    "actionable_fix": fix_str,
                    "tool_calls": turn_tool_log,
                })

                if is_final_turn:
                    break

                messages.append({"role": "assistant", "content": raw_reply})
                messages.append({
                    "role": "user",
                    "content": (
                        "TOOL RESULTS:\n"
                        + "\n\n".join(tool_feedback_blocks[:3])
                        + "\n\nNow output your final JSON with `is_final: true`, `ast_root_cause`, and `actionable_fix`."
                    ),
                })
            else:
                # Plain query string returned (e.g. lightweight model or unit test mock)
                clean_q = " ".join(raw_reply.strip().strip('"').strip("'").split())
                if clean_q:
                    executed_queries.append(clean_q)
                    hits = kb.search_cpsa_docs(clean_q, top_k=2)
                    for sec in hits:
                        collected_sections[sec["section_id"]] = sec
                    searcher_turns.append({
                        "turn": turn_idx + 1,
                        "is_final": True,
                        "status": "Direct Query Search Completed",
                        "ast_root_cause": "",
                        "actionable_fix": "",
                        "tool_calls": [{
                            "tool": "search_cpsa_docs",
                            "args": clean_q,
                            "retrieved": ", ".join(s["section_id"] for s in hits),
                        }],
                    })
                break
    except Exception as exc:
        logger.warning("Agentic CPSA searcher LLM step encountered exception (%s); using deterministic KB lookup", exc)

    # Step 2: If this is a Snowball State Error, always pin the authoritative CPSA 4.4.9
    # Anti-Snowballing & Termination core rule section so the Repair LLM has exact mathematical guidance.
    from src.verification_engine.snowball_autopsy import is_snowball_state_error
    if is_snowball_state_error(error_diagnostic):
        for sec in kb.search_cpsa_docs(
            "state space snowballing non-termination encryption-test try-old-strands check-nonces domain separation tags neq",
            category="01_core_rules",
            top_k=2,
        ):
            if "06_termination_and_anti_snowballing" in sec.get("source_file", "") or not collected_sections:
                collected_sections[sec["section_id"]] = sec

    # Step 3: Always guarantee high-precision deterministic fallback / enrichment from the error string
    if not collected_sections:
        fallback_q = (
            fallback_query_fn(error_diagnostic, failure_stage)
            if callable(fallback_query_fn)
            else f"CPSA {failure_stage} {error_diagnostic[:120]}"
        )
        executed_queries.append(fallback_q)
        for sec in kb.search_cpsa_docs(fallback_q, top_k=2):
            collected_sections[sec["section_id"]] = sec

    # Also pull 1 working .scm example matching the protocol's algebra if none was pulled yet
    if not collected_examples:
        for match_ex in kb.find_scm_examples(algebra=algebra_hint, query=error_diagnostic[:100], top_k=1):
            full_ex = kb.read_scm_example(match_ex["filename"])
            if full_ex:
                collected_examples[full_ex["example_id"]] = full_ex

    # Assemble final reference package and emit telemetry
    formatted_blocks: List[str] = []
    telemetry_chunks: List[Dict[str, Any]] = []

    if searcher_diagnosis:
        formatted_blocks.append(f"--- Agentic Searcher AST Diagnosis ---\n{searcher_diagnosis}")

    for idx, (sec_id, sec) in enumerate(list(collected_sections.items())[:3], 1):
        LAST_RETRIEVED_CHUNK_IDS.append(sec_id)
        formatted_blocks.append(
            f"--- Retrieved CPSA Rule {idx}: {sec['title']} ({sec['source_file']}) ---\n{sec['content'][:2200]}"
        )
        telemetry_chunks.append({
            "chunk_id": sec_id,
            "title": sec["title"],
            "source_file": sec["source_file"],
            "snippet": sec["content"][:280].strip() + ("..." if len(sec["content"]) > 280 else ""),
        })

    for idx, (ex_id, ex) in enumerate(list(collected_examples.items())[:1], 1):
        LAST_RETRIEVED_CHUNK_IDS.append(ex_id)
        scm_snippet = (ex.get("scm_code") or "")[:1600]
        formatted_blocks.append(
            f"--- Official MITRE .scm Example: {ex['filename']} (algebra: {ex.get('algebra')}) ---\n"
            f"Summary: {ex.get('summary', '')}\n{scm_snippet}"
        )
        telemetry_chunks.append({
            "chunk_id": ex_id,
            "title": f"MITRE Example: {ex['filename']} ({ex.get('algebra')})",
            "source_file": ex_id,
            "snippet": f"{ex.get('summary', '')}\n{scm_snippet[:200]}",
        })

    summary_query_str = " | ".join(executed_queries[:3]) or f"KB Search ({failure_stage})"
    LAST_SEARCHER_QUERY = summary_query_str
    LAST_SEARCHER_DIAGNOSIS = searcher_diagnosis
    LAST_SEARCHER_TRACE = list(searcher_turns)

    stage_num = 5 if failure_stage == "roletran" else 6
    GLOBAL_EVENT_BUS.emit(
        "rag_retrieval",
        stage=stage_num,
        purpose=f"Agentic KB Search ({failure_stage})",
        query=summary_query_str,
        searcher_diagnosis=searcher_diagnosis,
        searcher_turns=searcher_turns,
        chunks=telemetry_chunks,
    )

    final_guidance = "\n\n".join(formatted_blocks)
    _SEARCH_CACHE[norm_sig] = (
        summary_query_str,
        final_guidance,
        list(LAST_RETRIEVED_CHUNK_IDS),
        searcher_diagnosis,
        list(searcher_turns),
    )
    return final_guidance
```

---

### `src/semantic_extraction/__init__.py`

*sha256:`d74f89ac1ac5` · 11 lines · 0.3 KB (~82 tokens) · lang:`python`*

```python
"""Semantic Extraction package for Stage 2 constrained CPSA protocol synthesis."""

from src.semantic_extraction.constrained_protocol_extractor import (
    ensure_three_point_of_view_skeletons,
    extract_protocol_specification,
)

__all__ = [
    "extract_protocol_specification",
    "ensure_three_point_of_view_skeletons",
]
```

---

### `src/semantic_extraction/constrained_protocol_extractor.py`

*sha256:`d20398caaa8f` · 448 lines · 19.5 KB (~4,998 tokens) · lang:`python`*

```python
"""Constrained Protocol Semantic Extractor with RAG Grounding.

Translates verbatim RFC message-exchange sections into a validated
`CPSAProtocolSpecification` AST using Hybrid BM25 + Dense RRF reference
grounding, 1-shot self-healing schema correction, and the mandatory
3-Point-of-View preskeleton architecture.
"""

import json
import time
from typing import List, Optional
import json_repair
import litellm
from pydantic import ValidationError

from src.intermediate_representation.protocol_syntax_tree import (
    CPSAPreskeleton,
    CPSAProtocolSpecification,
    CPSAStrandInstance,
    CPSAVariableDeclaration,
)
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_PROTOCOL_EXTRACTION,
    PROMPT_SCHEMA_SELF_CORRECTION,
    build_schema_system_prompt,
    load_prompt_spec,
    parse_llm_json,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("protocol_extractor")

LAST_EXTRACTION_METADATA: dict = {
    "schema_self_correction_triggered": False,
    "schema_validation_error": None,
}


def extract_protocol_specification(
    verbatim_slice: str,
    protocol_name: str,
    principals: Optional[List[str]] = None,
    model: Optional[str] = None,
) -> CPSAProtocolSpecification:
    """Extracts a validated CPSAProtocolSpecification from verbatim RFC text."""
    global LAST_EXTRACTION_METADATA
    LAST_EXTRACTION_METADATA = {
        "schema_self_correction_triggered": False,
        "schema_validation_error": None,
    }
    extraction_spec = load_prompt_spec(PROMPT_PROTOCOL_EXTRACTION)
    model_name = model or extraction_spec.model
    sampling_temp = extraction_spec.temperature
    logger.info("Extracting CPSAProtocolSpecification for '%s' using %s", protocol_name, model_name)

    principals_hint = f"Expected Principals: {', '.join(principals)}" if principals else ""

    user_prompt = (
        f"Protocol Identifier: {protocol_name}\n"
        f"{principals_hint}\n\n"
        "Verbatim RFC Exchange Specification (SOLE GROUND TRUTH — STRICT 1-TO-1 FIDELITY REQUIRED):\n"
        f"{verbatim_slice}\n\n"
        "Extract the complete CPSAProtocolSpecification adhering to all MITRE CPSA 4.4.9 executability and sort constraints.\n"
        "CRITICAL ZERO-HALLUCINATION RULE: Model strictly the roles, message flights, fields, and cryptographic "
        "operations defined in the Verbatim RFC Exchange Specification above. Do NOT invent fictional messages, "
        "non-RFC variables, or textbook protocol fields that do not appear in the RFC text."
    )

    system_prompt = build_schema_system_prompt(
        PROMPT_PROTOCOL_EXTRACTION,
        CPSAProtocolSpecification,
    )

    response = None
    for retry_idx in range(3):
        effective_temp = (
            max(0.5, sampling_temp or 0.0)
            if retry_idx > 0
            else sampling_temp
        )
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=effective_temp,
            max_tokens=extraction_spec.max_tokens,
            json_mode=True,
        )
        try:
            response = litellm.completion(
                **llm_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                timeout=extraction_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(response, role="extraction", model_name=model_name, stage=2)
            break
        except Exception as exc:
            err_msg = str(exc)
            if (
                any(
                    token in err_msg
                    for token in (
                        "Timeout",
                        "timed out",
                        "429",
                        "RateLimit",
                        "BadGateway",
                        "502",
                        "503",
                        "504",
                        "incomplete",
                        "output budget",
                    )
                )
                and retry_idx < 2
            ):
                wait_seconds = 10 * (retry_idx + 1)
                logger.warning(
                    "Extraction attempt %d failed (%s). Retrying in %ds...",
                    retry_idx + 1,
                    exc,
                    wait_seconds,
                )
                time.sleep(wait_seconds)
            else:
                raise

    raw_content = response.choices[0].message.content
    parsed_data = parse_llm_json(raw_content)

    try:
        specification = CPSAProtocolSpecification.model_validate(parsed_data)
    except ValidationError as validation_error:
        LAST_EXTRACTION_METADATA["schema_self_correction_triggered"] = True
        LAST_EXTRACTION_METADATA["schema_validation_error"] = str(validation_error)
        logger.warning(
            "Stage 2 schema validation error encountered: %s. Initiating 1-shot self-healing correction...",
            validation_error,
        )
        corr_spec = load_prompt_spec(PROMPT_SCHEMA_SELF_CORRECTION)
        correction_template = corr_spec.body
        if "{validation_error}" in correction_template:
            correction_prompt = correction_template.replace("{validation_error}", str(validation_error))
        else:
            correction_prompt = f"{correction_template}\n\nValidation Errors:\n{validation_error}"

        corr_model = model or corr_spec.model
        corr_temp = corr_spec.temperature
        corr_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            corr_model,
            temperature=corr_temp,
            max_tokens=corr_spec.max_tokens,
            json_mode=True,
        )

        try:
            correction_response = litellm.completion(
                **corr_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": raw_content},
                    {"role": "user", "content": correction_prompt},
                ],
                timeout=corr_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(correction_response, role="extraction", model_name=corr_model, stage=2)
            corrected_content = correction_response.choices[0].message.content
            corrected_data = parse_llm_json(corrected_content)
            specification = CPSAProtocolSpecification.model_validate(corrected_data)
            logger.info("Stage 2 self-healing correction SUCCEEDED")
        except Exception as retry_error:
            logger.error("Self-healing correction failed: %s. Raising validation error.", retry_error)
            raise validation_error from retry_error

    # Stage 2 Cryptographic Primitive Gate: if the LLM extracted roles with zero CPSA cryptographic
    # primitives (e.g., cleartext messages or bare variables), give it 1 self-correction pass to either
    # bail out with `is_verifiable_protocol=False` or model the RFC's actual cryptographic operations.
    if (
        specification.is_verifiable_protocol
        and specification.roles
        and not specification.has_cryptographic_primitives()
    ):
        crypto_error = (
            "Extracted specification contains zero CPSA cryptographic operators (`enc`, `hash`, `ltk`, `pubk`, "
            "`privk`, `invk`, `akey`, `skey`, `exp`, `gen`) across all role traces and assumptions. "
            "Either (a) the Verbatim RFC Exchange Specification defines a cleartext, transport-delegated, or "
            "non-cryptographic exchange — in which case you MUST set `\"is_verifiable_protocol\": false`, "
            "populate `\"ineligibility_reason\"`, and set `\"roles\": []` and `\"skeletons\": []`; OR "
            "(b) you omitted the RFC's cryptographic operations — in which case you MUST model the RFC's "
            "encryption, MAC/PRF (`hash`), signature (`enc` with `privk`), or Diffie-Hellman (`exp`/`gen`) "
            "operations explicitly in the role traces."
        )
        LAST_EXTRACTION_METADATA["schema_self_correction_triggered"] = True
        LAST_EXTRACTION_METADATA["schema_validation_error"] = crypto_error
        logger.warning(
            "Stage 2 extracted protocol '%s' has zero cryptographic primitives. Triggering 1-shot verification gate...",
            protocol_name,
        )
        corr_spec = load_prompt_spec(PROMPT_SCHEMA_SELF_CORRECTION)
        corr_model = model or corr_spec.model
        corr_temp = corr_spec.temperature
        corr_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            corr_model,
            temperature=corr_temp,
            max_tokens=corr_spec.max_tokens,
            json_mode=True,
        )
        try:
            correction_response = litellm.completion(
                **corr_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": specification.model_dump_json()},
                    {"role": "user", "content": crypto_error},
                ],
                timeout=corr_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(correction_response, role="extraction", model_name=corr_model, stage=2)
            corrected_content = correction_response.choices[0].message.content
            corrected_data = parse_llm_json(corrected_content)
            specification = CPSAProtocolSpecification.model_validate(corrected_data)
        except Exception as exc:
            logger.warning("Cryptographic primitive self-correction call failed (%s); marking unverifiable.", exc)

        if specification.is_verifiable_protocol and not specification.has_cryptographic_primitives():
            specification.is_verifiable_protocol = False
            specification.ineligibility_reason = (
                specification.ineligibility_reason
                or "Extracted specification contains zero cryptographic primitives (cleartext or transport-delegated protocol)."
            )

    if not specification.is_verifiable_protocol or not specification.roles:
        logger.info(
            "Stage 2 determined '%s' is not a verifiable cryptographic protocol: %s",
            protocol_name,
            specification.ineligibility_reason,
        )
        return specification

    specification = ensure_three_point_of_view_skeletons(specification)

    logger.info(
        "Extraction SUCCESS: Extracted protocol '%s' with %d roles and %d preskeletons",
        specification.protocol_name,
        len(specification.roles),
        len(specification.skeletons),
    )
    return specification


def ensure_three_point_of_view_skeletons(spec: CPSAProtocolSpecification) -> CPSAProtocolSpecification:
    """Guarantees the standard MITRE CPSA 3-skeleton architecture:
    1. Dedicated pure POV preskeleton for each communicating role with a single defstrandmax and NO listeners
       (enabling CPSA to compute minimal realized bilateral handshake shapes without pre-seeded strands).
    2. A distinct secrecy preskeleton containing a deflistener for the primary confidential term.
    """
    if not spec.is_verifiable_protocol or not spec.roles:
        return spec

    # Collect existing secrecy listeners and non-originating assumptions
    existing_listeners = []
    global_non_originating = []
    for skel in spec.skeletons:
        existing_listeners.extend(skel.listeners)
        global_non_originating.extend(skel.non_originating)

    # Deduplicate non-originating keys while preserving insertion order
    seen_non_orig_keys = set()
    deduplicated_non_orig = []
    for non_orig_term in global_non_originating:
        serialized_term = json.dumps(non_orig_term, sort_keys=True)
        if serialized_term not in seen_non_orig_keys:
            seen_non_orig_keys.add(serialized_term)
            deduplicated_non_orig.append(non_orig_term)

    # Separate pure POV skeletons (without listeners) and secrecy skeletons (with listeners)
    # CRITICAL: Filter out any invalid listener term that is also declared in non_originating
    # or pen_non_originating (which causes CPSA fatal error: `non-orig <key> carried`).
    non_orig_set = {json.dumps(t, sort_keys=True) for t in deduplicated_non_orig}
    for skel in spec.skeletons:
        for pno in skel.pen_non_originating:
            non_orig_set.add(json.dumps(pno, sort_keys=True))
    for role in spec.roles:
        for no_t in role.non_originating + role.pen_non_originating:
            non_orig_set.add(json.dumps(no_t, sort_keys=True))

    spec.primary_secrecy_goals = [
        t for t in spec.primary_secrecy_goals if json.dumps(t, sort_keys=True) not in non_orig_set
    ]

    roles_with_pure_pov = set()
    pure_pov_skeletons = []
    secrecy_skeletons = []

    for skel in spec.skeletons:
        valid_listeners = [
            l for l in skel.listeners if json.dumps(l, sort_keys=True) not in non_orig_set
        ]
        skel.listeners = valid_listeners
        if not skel.listeners:
            if len(skel.strands) == 1:
                role_name = skel.strands[0].role_name
                if role_name not in roles_with_pure_pov:
                    roles_with_pure_pov.add(role_name)
                    pure_pov_skeletons.append(skel)
        else:
            if len(skel.strands) > 1:
                skel.strands = [skel.strands[0]]
            secrecy_skeletons.append(skel)

    # Build pure POV skeletons for any roles that lack them
    final_skeletons = list(pure_pov_skeletons)
    for role in spec.roles:
        if role.role_name not in roles_with_pure_pov:
            variable_bindings = {var.name: var.name for var in role.variables}
            skeleton_variables = [
                CPSAVariableDeclaration(name=var.name, sort=var.sort)
                for var in role.variables
            ]
            pure_role_skeleton = CPSAPreskeleton(
                protocol_name=spec.protocol_name,
                description=f"{role.role_name.capitalize()} Point of View (Authentication & Shape Realization)",
                variables=skeleton_variables,
                strands=[
                    CPSAStrandInstance(
                        role_name=role.role_name,
                        variable_bindings=variable_bindings,
                    )
                ],
                non_originating=deduplicated_non_orig,
                unique_originating=list(role.unique_originating),
                listeners=[],
                comment=f"{role.role_name.capitalize()} Point of View",
            )
            final_skeletons.append(pure_role_skeleton)

    # Guarantee at least one secrecy verification skeleton if a valid transmitted secret was identified
    if secrecy_skeletons:
        final_skeletons.extend(secrecy_skeletons)
    else:
        valid_existing_listeners = [
            l for l in existing_listeners if json.dumps(l, sort_keys=True) not in non_orig_set
        ]
        secret_targets = valid_existing_listeners or spec.primary_secrecy_goals
        if secret_targets:
            chosen_secret = secret_targets[0]
            originating_role = spec.roles[0]
            for role in spec.roles:
                if any(
                    chosen_secret == uo or (isinstance(uo, str) and uo == chosen_secret)
                    for uo in role.unique_originating
                ):
                    originating_role = role
                    break

            variable_bindings = {var.name: var.name for var in originating_role.variables}
            skeleton_variables = [
                CPSAVariableDeclaration(name=var.name, sort=var.sort)
                for var in originating_role.variables
            ]
            secrecy_skeleton = CPSAPreskeleton(
                protocol_name=spec.protocol_name,
                description=f"Secrecy Verification: tests confidentiality of {chosen_secret}",
                variables=skeleton_variables,
                strands=[
                    CPSAStrandInstance(
                        role_name=originating_role.role_name,
                        variable_bindings=variable_bindings,
                    )
                ],
                non_originating=deduplicated_non_orig,
                unique_originating=list(originating_role.unique_originating),
                listeners=[chosen_secret],
                comment=f"Secrecy Point of View: Listener on {chosen_secret}",
            )
            final_skeletons.append(secrecy_skeleton)

    spec.skeletons = final_skeletons

    # Ensure every skeleton's strands explicitly bind role variables to skeleton variables
    # (preventing `Skeleton not well formed: a variable in non-orig is not in some trace`),
    # strip redundant skeleton-level `uniq-orig` atoms already declared in the strand's `defrole`
    # (preventing `Skeleton not well formed: uniq-orig <var> not carried` when encrypted under a non-orig key),
    # and add sort-disjointness `(neq secret other_var)` facts in secrecy skeletons so CPSA cannot
    # alias a secret `data` variable with a cleartext `data` header/identifier in the same strand.
    role_map = {r.role_name: r for r in spec.roles}
    secret_atom_set = {
        s for s in spec.primary_secrecy_goals if isinstance(s, str)
    }
    for skel in spec.skeletons:
        existing_var_names = {v.name for v in skel.variables}
        role_level_uniq_orig = set()
        for strand in skel.strands:
            matched_role = role_map.get(strand.role_name)
            if not matched_role:
                continue
            for r_var in matched_role.variables:
                if r_var.name not in existing_var_names:
                    skel.variables.append(CPSAVariableDeclaration(name=r_var.name, sort=r_var.sort))
                    existing_var_names.add(r_var.name)
                if r_var.name not in strand.variable_bindings:
                    strand.variable_bindings[r_var.name] = r_var.name
            for uo in matched_role.unique_originating:
                if isinstance(uo, str):
                    role_level_uniq_orig.add(uo)
        if role_level_uniq_orig and skel.unique_originating:
            skel.unique_originating = [
                uo for uo in skel.unique_originating
                if not (isinstance(uo, str) and uo in role_level_uniq_orig)
            ]
        if skel.listeners:
            var_sort_map = {v.name: v.sort for v in skel.variables}
            existing_facts = {
                (f[1], f[2])
                for f in skel.facts
                if isinstance(f, list) and len(f) == 3 and f[0] == "neq"
            } | {
                (f[2], f[1])
                for f in skel.facts
                if isinstance(f, list) and len(f) == 3 and f[0] == "neq"
            }
            listener_atoms = [l for l in skel.listeners if isinstance(l, str)]
            for secret_var in listener_atoms:
                secret_sort = var_sort_map.get(secret_var)
                if not secret_sort:
                    continue
                for v in skel.variables:
                    if (
                        v.name != secret_var
                        and v.sort == secret_sort
                        and v.name not in secret_atom_set
                        and v.name not in listener_atoms
                        and (secret_var, v.name) not in existing_facts
                    ):
                        skel.facts.append(["neq", secret_var, v.name])
                        existing_facts.add((secret_var, v.name))

    return spec
```

---

### `src/system_config.py`

*sha256:`590f02a01d64` · 175 lines · 7.6 KB (~1,935 tokens) · lang:`python`*

```python
"""Global environment, binary paths, execution limits, and provider configuration."""

import os
import shutil
import warnings
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import litellm
from pydantic_settings import BaseSettings

# Suppress third-party LiteLLM verbosity, debug info, and deprecation warnings
litellm.suppress_debug_info = True
litellm.set_verbose = False
litellm.drop_params = True
litellm.request_timeout = 3600
for _logger_name in ("LiteLLM", "litellm", "LiteLLM Proxy", "LiteLLM Router"):
    logging.getLogger(_logger_name).setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning, module=".*litellm.*")
warnings.filterwarnings("ignore", category=UserWarning, module=".*litellm.*")
warnings.filterwarnings("ignore", message=".*temperature.*")

# Load .env file eagerly from project root (credentials & base URLs only)
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)


class SystemEnvironmentConfig(BaseSettings):
    """Global system file paths, external tool binaries, API credentials, and endpoints."""

    # Project Directories
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    PROMPTS_DIR: Path = PROJECT_ROOT / "prompts"
    RFCS_DIR: Path = PROJECT_ROOT / "refrences" / "all_RFCs"
    CPSA_KB_DIR: Path = PROJECT_ROOT / "refrences" / "cpsa_kb"
    CHUNKS_DIR: Path = PROJECT_ROOT / "refrences" / "legacy_rag_archive" / "chunks"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    DEFAULT_OUTPUT_DIR: Path = PROJECT_ROOT / "output"

    # MITRE CPSA 4.4.9 Binary Paths
    CABAL_BIN_DIR: Path = Path.home() / ".cabal" / "bin"
    CPSA4_BIN: Path = CABAL_BIN_DIR / "cpsa4"
    CPSA4JSON_BIN: Path = CABAL_BIN_DIR / "cpsa4json"
    CPSA4ROLETRAN_BIN: Path = CABAL_BIN_DIR / "cpsa4roletran"
    CPSA4INIT_BIN: Path = CABAL_BIN_DIR / "cpsa4init"
    CPSA4SHAPES_BIN: Path = CABAL_BIN_DIR / "cpsa4shapes"
    CPSA4GRAPH_BIN: Path = CABAL_BIN_DIR / "cpsa4graph"
    CPSA4PROT_BIN: Path = CABAL_BIN_DIR / "cpsa4prot"
    CPSA4SAS_BIN: Path = CABAL_BIN_DIR / "cpsa4sas"
    CPSA4GOALSAT_BIN: Path = CABAL_BIN_DIR / "cpsa4goalsat"

    # API Keys & Base Endpoints (Loaded from .env)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    NOUS_API_KEY: Optional[str] = os.getenv("NOUS_API_KEY")
    NOUS_API_BASE: str = os.getenv("NOUS_API_BASE", "https://inference-api.nousresearch.com/v1")
    OLLAMA_API_BASE: str = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
    STRATA_API_BASE: str = os.getenv("STRATA_API_BASE", "http://localhost:11435/v1")
    STRATA_API_KEY: str = os.getenv("STRATA_API_KEY", "local-strata")

    # Compiler & Harness Execution Limits
    LLM_TIMEOUT_SECONDS: int = 3600
    CPSA_TIMEOUT_SECONDS: int = 15
    ROLETRAN_TIMEOUT_SECONDS: int = 15
    MAX_REPAIR_ATTEMPTS: int = 10

    model_config = {"env_file": ".env", "extra": "ignore"}

    def verify_cpsa_toolchain(self) -> List[str]:
        """Verifies that required MITRE CPSA 4.4.9 binaries exist on disk or PATH.
        Returns a list of missing binary names (empty list if all are present).
        """
        required_bins = [
            ("cpsa4", self.CPSA4_BIN),
            ("cpsa4json", self.CPSA4JSON_BIN),
            ("cpsa4roletran", self.CPSA4ROLETRAN_BIN),
            ("cpsa4shapes", self.CPSA4SHAPES_BIN),
            ("cpsa4graph", self.CPSA4GRAPH_BIN),
        ]
        missing: List[str] = []
        for bin_name, bin_path in required_bins:
            if bin_path.exists() and os.access(bin_path, os.X_OK):
                continue
            found_on_path = shutil.which(bin_name)
            if found_on_path:
                continue
            missing.append(f"{bin_name} (expected at {bin_path})")
        return missing

    # Live model properties backed directly by `prompts/*.md` YAML frontmatter
    @property
    def DEFAULT_ROUTER_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_APPLICABILITY_GATE, resolve_prompt_model
        return resolve_prompt_model(PROMPT_APPLICABILITY_GATE)

    @property
    def DEFAULT_SECTION_ROUTER_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_SECTION_ROUTER, resolve_prompt_model
        return resolve_prompt_model(PROMPT_SECTION_ROUTER)

    @property
    def DEFAULT_EXTRACTION_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_PROTOCOL_EXTRACTION, resolve_prompt_model
        return resolve_prompt_model(PROMPT_PROTOCOL_EXTRACTION)

    @property
    def DEFAULT_CORRECTION_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_SCHEMA_SELF_CORRECTION, resolve_prompt_model
        return resolve_prompt_model(PROMPT_SCHEMA_SELF_CORRECTION)

    @property
    def DEFAULT_QUERY_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_RAG_QUERY_FORMULATION, resolve_prompt_model
        return resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION)

    @property
    def DEFAULT_REPAIR_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_COMPILER_REPAIR, resolve_prompt_model
        return resolve_prompt_model(PROMPT_COMPILER_REPAIR)

    @property
    def DEFAULT_THINK_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_THINK_SYNTHESIZER, resolve_prompt_model
        return resolve_prompt_model(PROMPT_THINK_SYNTHESIZER)

    def get_llm_kwargs(
        self,
        model_name: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
    ) -> Dict[str, Any]:
        """Returns provider-specific arguments (API keys, base URLs, sampling) for LiteLLM."""
        kwargs: Dict[str, Any] = {"model": model_name}
        effective_max_tokens = int(max_tokens) if (max_tokens is not None and max_tokens > 0) else 65536
        kwargs["max_tokens"] = effective_max_tokens
        if temperature is not None:
            kwargs["temperature"] = float(temperature)

        is_local_provider = model_name.startswith("strata/") or model_name.startswith("ollama/")
        if json_mode and not is_local_provider:
            kwargs["response_format"] = {"type": "json_object"}
        if model_name.startswith("nous/") or model_name.startswith("nousresearch/"):
            target_model = model_name.split("/", 1)[1]
            kwargs["model"] = f"openai/{target_model}"
            kwargs["api_base"] = self.NOUS_API_BASE
            if self.NOUS_API_KEY:
                kwargs["api_key"] = self.NOUS_API_KEY
        elif model_name.startswith("strata/"):
            kwargs["model"] = f"openai/{model_name}"
            kwargs["api_base"] = self.STRATA_API_BASE
            kwargs["api_key"] = self.STRATA_API_KEY
        elif model_name.startswith("ollama/"):
            ollama_base = os.getenv("OLLAMA_API_BASE") or os.getenv("OLLAMA_HOST") or self.OLLAMA_API_BASE
            if ollama_base and not ollama_base.startswith("http"):
                ollama_base = f"http://{ollama_base}"
            kwargs["api_base"] = ollama_base.rstrip("/")
        elif model_name.startswith("gemini/"):
            if self.GEMINI_API_KEY:
                kwargs["api_key"] = self.GEMINI_API_KEY
        elif model_name.startswith("openai/"):
            if self.OPENAI_API_KEY:
                kwargs["api_key"] = self.OPENAI_API_KEY
        elif model_name.startswith("anthropic/"):
            if self.ANTHROPIC_API_KEY:
                kwargs["api_key"] = self.ANTHROPIC_API_KEY

        return kwargs


# Global singleton instance
SYSTEM_CONFIG = SystemEnvironmentConfig()
```

---

### `src/verification_engine/__init__.py`

*sha256:`bfcbde4ba078` · 39 lines · 1.2 KB (~308 tokens) · lang:`python`*

```python
"""Verification Engine package for Stages 4, 5 & 6 roletran check, self-healing repair, and MITRE CPSA compilation."""

from src.verification_engine.compiler_diagnostic_repair import (
    fallback_sanitize_diagnostic_query,
    formulate_rag_diagnostic_query,
    repair_protocol_specification,
)
from src.verification_engine.mitre_build_orchestrator import (
    CPSABuildArtifacts,
    CPSABuildError,
    execute_mitre_make_build,
)
from src.verification_engine.roletran_executability_gate import (
    RoletranVerificationResult,
    verify_role_executability,
)
from src.verification_engine.trajectory_metadata_exporter import (
    analyze_exploration_txt,
    analyze_shapes_txt,
    build_scm_metadata_header,
    compute_quality_assessment,
    write_trajectory_metadata_bundle,
)

__all__ = [
    "RoletranVerificationResult",
    "verify_role_executability",
    "CPSABuildArtifacts",
    "CPSABuildError",
    "execute_mitre_make_build",
    "fallback_sanitize_diagnostic_query",
    "formulate_rag_diagnostic_query",
    "repair_protocol_specification",
    "analyze_exploration_txt",
    "analyze_shapes_txt",
    "build_scm_metadata_header",
    "compute_quality_assessment",
    "write_trajectory_metadata_bundle",
]
```

---

### `src/verification_engine/compiler_diagnostic_repair.py`

*sha256:`d2483d873015` · 295 lines · 12.6 KB (~3,232 tokens) · lang:`python`*

```python
"""Compiler Diagnostic Repair Engine with RAG-Guided Self-Healing.

Analyzes `cpsa4roletran` and `cpsa4` compiler diagnostics, formulates an
abstracted conceptual RAG query using the configured query model, retrieves
authoritative MITRE CPSA 4.4.9 manual chunks, and repairs the failing
`CPSAProtocolSpecification` AST.
"""

import json
import re
import time
from typing import Literal, Optional
import json_repair
import litellm

from src import rag_retriever_client
from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_COMPILER_REPAIR,
    PROMPT_RAG_QUERY_FORMULATION,
    build_schema_system_prompt,
    load_prompt_spec,
    parse_llm_json,
)
from src.rag_retriever_client import (
    get_cpsa_manual_retriever,
    retrieve_cpsa_manual_guidance,
    run_agentic_cpsa_searcher,
)
from src.semantic_extraction.constrained_protocol_extractor import (
    ensure_three_point_of_view_skeletons,
)
from src.system_config import SYSTEM_CONFIG
from src.verification_engine.snowball_autopsy import is_snowball_state_error

logger = get_pipeline_logger("diagnostic_repair")

LAST_REPAIR_METADATA: dict = {
    "rag_query": None,
    "retrieved_chunk_ids": [],
}


def fallback_sanitize_diagnostic_query(diagnostic: str, failure_stage: str) -> str:
    """Fallback sanitizer for compiler diagnostics when LLM query formulation is unavailable,
    stripping file paths, line numbers, and Make boilerplate.
    """
    cleaned = re.sub(r"MITRE build failed for [^:]+:\s*", "", diagnostic, flags=re.IGNORECASE)
    cleaned = re.sub(r"make(\[\d+\])?:.*", "", cleaned)
    cleaned = re.sub(r"[a-zA-Z0-9_\-\./]+\.(scm|txt|xhtml|mk|hs|pl)(:\d+:\d+)?:?", "", cleaned)
    cleaned = re.sub(r"\(.*?\)", "", cleaned)
    cleaned = re.sub(r'["\':*#\n\r]', " ", cleaned)
    tokens = [
        token
        for token in cleaned.split()
        if len(token) > 2
        and not token.isdigit()
        and token.lower() not in {"error", "exit", "code", "failed"}
    ]
    concise_tokens = " ".join(tokens[:5])
    if concise_tokens:
        return f"CPSA {failure_stage} {concise_tokens} syntax manual error rule fix"
    return f"CPSA {failure_stage} syntax manual error rule fix"


def formulate_rag_diagnostic_query(
    diagnostic: str,
    failure_stage: str,
    model: Optional[str] = None,
) -> str:
    """Uses a dedicated LLM call to formulate a targeted conceptual query for the MITRE CPSA manual,
    purging concrete variable names and local file paths. Falls back to deterministic sanitization if offline.
    """
    query_spec = load_prompt_spec(PROMPT_RAG_QUERY_FORMULATION)
    query_model = model or query_spec.model
    sampling_temp = query_spec.temperature if query_spec.temperature is not None else 0.0
    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(query_model, temperature=sampling_temp)
        system_prompt = query_spec.body
        user_prompt = f"Failure Stage: {failure_stage}\nCompiler Diagnostic:\n{diagnostic}"
        response = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=query_spec.timeout,
        )
        from src.cost_tracker import GLOBAL_COST_TRACKER
        GLOBAL_COST_TRACKER.record_llm_call(
            response,
            role="query",
            model_name=query_model,
            stage=5 if failure_stage == "roletran" else 6,
        )
        raw_content = response.choices[0].message.content
        if raw_content:
            query = " ".join(raw_content.strip().strip('"').strip("'").split())
            if query:
                return query
    except Exception as exc:
        logger.warning("LLM diagnostic query generation failed (%s), using fallback sanitizer", exc)

    return fallback_sanitize_diagnostic_query(diagnostic, failure_stage)


def repair_protocol_specification(
    failing_spec: CPSAProtocolSpecification,
    error_diagnostic: str,
    verbatim_slice: str,
    failure_stage: Literal["roletran", "solver"],
    model: Optional[str] = None,
    query_model: Optional[str] = None,
    cycle_detected: bool = False,
    use_agentic_searcher: bool = True,
    prior_attempts: Optional[list] = None,
) -> CPSAProtocolSpecification:
    """Uses Two-Speed Pinned Header + Agentic CPSA Knowledge Base Searcher to patch a failing CPSAProtocolSpecification."""
    repair_spec = load_prompt_spec(PROMPT_COMPILER_REPAIR)
    model_name = model or repair_spec.model
    logger.info(
        "Executing repair for stage '%s' using %s (cycle_detected=%s, use_agentic_searcher=%s) with diagnostic: %s",
        failure_stage,
        model_name,
        cycle_detected,
        use_agentic_searcher,
        error_diagnostic,
    )

    # 1. Run Agentic CPSA Knowledge Base Searcher when triggered (Attempt #3+, repeated diagnostic, or cycle)
    global LAST_REPAIR_METADATA
    retriever = get_cpsa_manual_retriever() if use_agentic_searcher else None
    if retriever and use_agentic_searcher:
        guidance_text = run_agentic_cpsa_searcher(
            error_diagnostic=error_diagnostic,
            failure_stage=failure_stage,
            failing_spec=failing_spec,
            model=query_model,
            cycle_detected=cycle_detected,
            fallback_query_fn=fallback_sanitize_diagnostic_query,
        )
        LAST_REPAIR_METADATA = {
            "rag_query": rag_retriever_client.LAST_SEARCHER_QUERY,
            "retrieved_chunk_ids": list(rag_retriever_client.LAST_RETRIEVED_CHUNK_IDS),
            "searcher_diagnosis": rag_retriever_client.LAST_SEARCHER_DIAGNOSIS,
            "searcher_turns": list(rag_retriever_client.LAST_SEARCHER_TRACE),
        }
    else:
        LAST_REPAIR_METADATA = {
            "rag_query": None,
            "retrieved_chunk_ids": [],
            "searcher_diagnosis": None,
            "searcher_turns": [],
        }
        guidance_text = (
            "Fast Direct Repair Pass: Apply the Pinned MITRE CPSA 4.4.9 Core Rules & Common Diagnostics "
            "in the system prompt to resolve the compiler diagnostic directly."
        )

    cycle_warning = ""
    if cycle_detected:
        cycle_warning = (
            "\n\nCRITICAL WARNING: An oscillation/cycle was detected. You previously generated a specification "
            "identical or near-identical to this one that already failed. Do NOT repeat the previous edits. "
            "You MUST apply an alternative repair strategy (e.g. check sort declarations, add missing variables to role inputs, "
            "or adjust preskeleton non-originating/unique-originating assumptions) to escape this cycle."
        )

    snowball_directive = ""
    if is_snowball_state_error(error_diagnostic):
        snowball_directive = (
            "\n\nMANDATORY TIER-3 SNOWBALL STATE RECOVERY PROTOCOL (Applies ONLY to State-Space Snowballing):\n"
            "Tier 1 non-default search orders (`--try-old-strands`, `--check-nonces`, `--reverse-nodes`) already "
            "failed to terminate on this specification, proving a structural unification cycle (`unify_0` / `cows` loop). "
            "Inspect the `CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT` in the diagnostic above and apply ALL of the following "
            "structural fixes while preserving strict 1-to-1 fidelity to the RFC:\n"
            "1. DOMAIN-SEPARATE EVERY `enc` AND `hash` TERM USING RFC MESSAGE HEADERS/TYPES: Distinguish request vs. "
            "response `[\"enc\", ...]` and `[\"hash\", ...]` terms using the actual RFC message type, header, opcode, "
            "or label fields from the Verbatim RFC Exchange Specification (and distinct prefix sorts `data` vs `text`) "
            "so outgoing ciphertexts/hashes cannot unify with incoming receptions of the same key sort.\n"
            "2. ADD PRINCIPAL INEQUALITY FACTS (`neq`): In every `CPSAPreskeleton` declaring two or more `name` variables "
            "(e.g. `client_id`, `server_id`), add `[\"neq\", \"<name_a>\", \"<name_b>\"]` to `facts` to block `A = B` "
            "symmetric key reflection.\n"
            "3. ENFORCE `data` vs `text` SORT SEPARATION (CPSA Primer §16.2): Declare fresh `uniq-orig` nonces/challenges/secrets "
            "with `\"sort\": \"data\"` and predictable RFC identifiers/headers/labels with `\"sort\": \"text\"`.\n"
            "4. BIND PRINCIPAL IDENTITIES INSIDE ENCRYPTED FLIGHTS: Include the communicating `name` variables inside the "
            "`[\"enc\", ...]` terms of the looping role identified in the autopsy so regular augmentation binds to existing "
            "principals instead of spawning unbounded `*-0, *-1` strands."
        )

    # Truncate verbatim slice to concise context to preserve token quota across multiple repair passes
    slice_snippet = verbatim_slice[:3000]
    if len(verbatim_slice) > 3000:
        slice_snippet += "\n... [Remaining RFC specification text truncated for compiler repair pass] ..."

    prior_history_block = ""
    if prior_attempts:
        joined_history = "\n".join(f"- {item}" for item in prior_attempts)
        prior_history_block = (
            f"\n\nPrior Failed Repair Attempts on This Specification (Do NOT repeat edits that caused these errors):\n"
            f"{joined_history}"
        )

    user_prompt = (
        f"Failing Protocol: {failing_spec.protocol_name}\n"
        f"Failure Stage: {failure_stage}\n"
        f"Compiler Diagnostic / Error:\n{error_diagnostic}{prior_history_block}\n\n"
        "MITRE CPSA Reference Guidance (Helper Only - Explains syntax rules and failure mechanisms):\n"
        f"{guidance_text}\n\n"
        "Verbatim RFC Exchange Specification (Excerpt for repair context):\n"
        f"{slice_snippet}\n\n"
        "Current Failing CPSA Specification (JSON):\n"
        f"{failing_spec.model_dump_json(indent=2)}{cycle_warning}{snowball_directive}\n\n"
        "Provide the complete repaired CPSAProtocolSpecification resolving the error without inventing fictional protocol terms."
    )

    # Use higher temperature if cycle detected or on timeout retry to break out of repetitive token loops
    base_temp = repair_spec.temperature
    sampling_temperature = max(0.5, base_temp or 0.0) if cycle_detected else base_temp
    system_prompt = build_schema_system_prompt(
        PROMPT_COMPILER_REPAIR,
        CPSAProtocolSpecification,
    )

    response = None
    for retry_idx in range(4):
        effective_temp = (
            max(0.5, sampling_temperature or 0.0)
            if retry_idx > 0
            else sampling_temperature
        )
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=effective_temp,
            max_tokens=repair_spec.max_tokens,
            json_mode=True,
        )
        try:
            response = litellm.completion(
                **llm_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                timeout=repair_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(
                response,
                role="repair",
                model_name=model_name,
                stage=5 if failure_stage == "roletran" else 6,
            )
            break
        except Exception as exc:
            err_msg = str(exc)
            if (
                any(
                    token in err_msg
                    for token in (
                        "429",
                        "Quota exceeded",
                        "RateLimitError",
                        "Timeout",
                        "timed out",
                        "BadGateway",
                        "502",
                        "503",
                        "504",
                        "incomplete",
                        "output budget",
                    )
                )
                and retry_idx < 3
            ):
                wait_seconds = 15 * (retry_idx + 1)
                logger.warning(
                    "Transient error during repair pass. Waiting %ds before retry: %s",
                    wait_seconds,
                    exc,
                )
                time.sleep(wait_seconds)
            else:
                raise

    raw_content = response.choices[0].message.content
    parsed_data = parse_llm_json(raw_content)

    repaired_spec = CPSAProtocolSpecification.model_validate(parsed_data)
    repaired_spec = ensure_three_point_of_view_skeletons(repaired_spec)

    logger.info("Repair pass completed for '%s'", repaired_spec.protocol_name)
    return repaired_spec
```

---

### `src/verification_engine/mitre_build_orchestrator.py`

*sha256:`0f74f410fcab` · 314 lines · 12.9 KB (~3,304 tokens) · lang:`python`*

```python
"""MITRE Build Orchestrator for CPSA Verification and Visualization."""

import os
import re
import shutil
import signal
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger
from src.verification_engine.snowball_autopsy import (
    SNOWBALL_HERALD_PORTFOLIO,
    generate_snowball_autopsy_report,
    inject_herald_options_into_scm,
    is_snowball_state_error,
)

logger = get_pipeline_logger("build_orchestrator")


def _run_make_with_hard_timeout(
    cmd: List[str],
    cwd: Path,
    env: Dict[str, str],
    timeout_seconds: float,
) -> Tuple[int, str, str]:
    """Runs a command in its own process group and hard-kills all child processes (e.g. cpsa4) on timeout."""
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout_str, stderr_str = proc.communicate(timeout=timeout_seconds)
        return proc.returncode, stdout_str or "", stderr_str or ""
    except subprocess.TimeoutExpired as exc:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            proc.kill()
            proc.communicate(timeout=2.0)
        except Exception:
            pass
        raise CPSABuildError(
            f"MITRE CPSA compilation timed out after {timeout_seconds:.0f} seconds "
            f"(state-space explosion / infinite strand loop in {' '.join(cmd)})."
        ) from exc


class CPSABuildArtifacts(BaseModel):
    """Paths to all artifacts emitted by the MITRE CPSA build system."""
    protocol_stem: str = Field(..., description="Base identifier stem for protocol outputs")
    scm_path: Path = Field(..., description="Source MITRE Scheme model file")
    trace_txt_path: Path = Field(..., description="Raw strand space solver derivations (.txt)")
    shapes_txt_path: Path = Field(..., description="Distilled minimal realized shapes (.txt)")
    full_graph_xhtml_path: Path = Field(..., description="Interactive SVG graph of all search steps (.xhtml)")
    shapes_graph_xhtml_path: Path = Field(..., description="Interactive SVG graph of proved shapes (.xhtml)")
    shapes_count: int = Field(default=0, description="Total number of realized shapes discovered")
    winning_herald_options: List[str] = Field(
        default_factory=list,
        description="Search-order herald flags that deterministically resolved a state-space snowball in Tier 1",
    )


class CPSABuildError(Exception):
    """Raised when the MITRE make build process fails."""
    pass


def _ensure_cpsa_makefile(target_dir: Path) -> None:
    """Ensures cpsa4init has initialized the official Makefile and cpsa4.mk in target_dir."""
    makefile = target_dir / "Makefile"
    cpsa_mk = target_dir / "cpsa4.mk"

    if makefile.exists() and cpsa_mk.exists():
        return

    logger.info("Initializing MITRE CPSA Makefile in %s via cpsa4init", target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    if not SYSTEM_CONFIG.CPSA4INIT_BIN.exists():
        raise FileNotFoundError(f"cpsa4init binary missing at {SYSTEM_CONFIG.CPSA4INIT_BIN}")

    proc = subprocess.run(
        [str(SYSTEM_CONFIG.CPSA4INIT_BIN)],
        cwd=target_dir,
        capture_output=True,
        text=True,
        check=False,
    )

    if proc.returncode != 0:
        logger.error("cpsa4init failed in %s: %s", target_dir, proc.stderr)
        raise CPSABuildError(f"cpsa4init initialization failed: {proc.stderr}")


def _count_shapes_in_file(shapes_txt_path: Path) -> int:
    """Counts the number of distinct realized shape skeletons in the shape summary file."""
    if not shapes_txt_path.exists():
        return 0
    try:
        with open(shapes_txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        shape_flags = re.findall(r"\(\s*shape\s*\)", content)
        if shape_flags:
            return len(shape_flags)
        matches = re.findall(r"\(defskeleton\s+", content)
        return len(matches)
    except Exception as e:
        logger.warning("Could not count shapes in %s: %s", shapes_txt_path, e)
        return 0


def execute_mitre_make_build(
    scm_path: Path,
    output_directory: Optional[Path] = None,
    build_full_graph: bool = True,
) -> CPSABuildArtifacts:
    """Orchestrates GNU Make to compile a Scheme model through cpsa4, cpsa4shapes, and cpsa4graph."""
    build_dir = output_directory or scm_path.parent
    build_dir.mkdir(parents=True, exist_ok=True)

    _ensure_cpsa_makefile(build_dir)

    stem = scm_path.stem
    target_scm_in_build = build_dir / f"{stem}.scm"

    # Ensure scm file is located in build_dir
    if scm_path.resolve() != target_scm_in_build.resolve():
        shutil.copy(scm_path, target_scm_in_build)

    logger.info("Executing MITRE make build for '%s' in %s", stem, build_dir)

    # Inject ~/.cabal/bin into subprocess PATH so GNU make resolves cpsa4, cpsa4shapes, cpsa4graph
    env = os.environ.copy()
    cabal_bin_str = str(SYSTEM_CONFIG.CABAL_BIN_DIR)
    env["PATH"] = f"{cabal_bin_str}:{env.get('PATH', '')}"

    # Remove stale derived artifacts before running make so each attempt is fresh
    def _clean_derived_artifacts() -> None:
        for stale_name in (f"{stem}.txt", f"{stem}_shapes.txt", f"{stem}_shapes.xhtml", f"{stem}.xhtml"):
            stale_file = build_dir / stale_name
            if stale_file.exists():
                stale_file.unlink()

    _clean_derived_artifacts()

    max_budget_sec = min(15.0, float(getattr(SYSTEM_CONFIG, "CPSA_TIMEOUT_SECONDS", 15)))
    start_ts = time.monotonic()
    trace_txt = build_dir / f"{stem}.txt"
    winning_herald_options: List[str] = []

    # Target 1: Minimal shapes graph (triggers cpsa4, cpsa4shapes, and cpsa4graph)
    target_shapes_xhtml = f"{stem}_shapes.xhtml"
    initial_snowball_msg: Optional[str] = None
    try:
        rc_shapes, out_shapes, err_shapes = _run_make_with_hard_timeout(
            ["make", "-B", target_shapes_xhtml],
            cwd=build_dir,
            env=env,
            timeout_seconds=max_budget_sec,
        )
        if rc_shapes != 0:
            err_msg = err_shapes.strip() or out_shapes.strip()
            full_err = f"MITRE build failed for {target_shapes_xhtml}: {err_msg}"
            if is_snowball_state_error(full_err):
                initial_snowball_msg = full_err
            else:
                logger.error("Make build failed for %s: %s", target_shapes_xhtml, err_msg)
                raise CPSABuildError(full_err)
    except CPSABuildError as exc:
        if is_snowball_state_error(str(exc)):
            initial_snowball_msg = str(exc)
        else:
            raise

    # -------------------------------------------------------------------------
    # SNOWBALL-ONLY RECOVERY PATH (Tier 1 Search-Order Portfolio -> Tier 2 Autopsy)
    # Every non-snowball error already raised above and follows the normal route.
    # -------------------------------------------------------------------------
    if initial_snowball_msg is not None:
        partial_trace_snapshot = ""
        if trace_txt.exists():
            try:
                partial_trace_snapshot = trace_txt.read_text(encoding="utf-8", errors="replace")
            except Exception:
                partial_trace_snapshot = ""

        logger.warning(
            "Snowball state detected on default cpsa4 search for '%s' (%s). "
            "Launching Tier 1 Deterministic Herald Search-Order Portfolio (0 LLM tokens)...",
            stem,
            initial_snowball_msg,
        )

        tier1_resolved = False
        last_snowball_msg = initial_snowball_msg

        for strategy_label, cli_flags, herald_opts in SNOWBALL_HERALD_PORTFOLIO:
            _clean_derived_artifacts()
            cpsa_flags_arg = f"CPSAFLAGS=+RTS -M512m -N -RTS {' '.join(cli_flags)}"
            logger.info("Tier 1 Portfolio trying strategy [%s]: %s", strategy_label, cpsa_flags_arg)
            try:
                rc_strat, out_strat, err_strat = _run_make_with_hard_timeout(
                    ["make", "-B", target_shapes_xhtml, cpsa_flags_arg],
                    cwd=build_dir,
                    env=env,
                    timeout_seconds=max_budget_sec,
                )
                if rc_strat == 0:
                    logger.info(
                        "Tier 1 Search-Order Portfolio RESOLVED snowball for '%s' using [%s] (0 LLM tokens)!",
                        stem,
                        strategy_label,
                    )
                    winning_herald_options = list(herald_opts)
                    tier1_resolved = True
                    try:
                        raw_scm = target_scm_in_build.read_text(encoding="utf-8")
                        updated_scm = inject_herald_options_into_scm(raw_scm, winning_herald_options)
                        target_scm_in_build.write_text(updated_scm, encoding="utf-8")
                        if scm_path.exists() and scm_path.resolve() != target_scm_in_build.resolve():
                            scm_path.write_text(updated_scm, encoding="utf-8")
                        for built_name in (f"{stem}.txt", f"{stem}_shapes.txt", target_shapes_xhtml):
                            built_file = build_dir / built_name
                            if built_file.exists():
                                os.utime(built_file, None)
                    except Exception as inject_exc:
                        logger.warning("Could not persist winning herald options into %s: %s", target_scm_in_build, inject_exc)
                    break

                strat_err = err_strat.strip() or out_strat.strip()
                last_snowball_msg = f"MITRE build failed for {target_shapes_xhtml} [{strategy_label}]: {strat_err}"
            except CPSABuildError as strat_exc:
                last_snowball_msg = str(strat_exc)

            if trace_txt.exists():
                try:
                    candidate_snap = trace_txt.read_text(encoding="utf-8", errors="replace")
                    if candidate_snap.count("(defskeleton") > partial_trace_snapshot.count("(defskeleton"):
                        partial_trace_snapshot = candidate_snap
                except Exception:
                    pass

        if not tier1_resolved:
            logger.warning(
                "All Tier 1 search-order strategies snowballed for '%s'. "
                "Running Tier 2 Partial .txt Snowball Autopsy...",
                stem,
            )
            autopsy_report = generate_snowball_autopsy_report(
                scm_path=target_scm_in_build,
                build_dir=build_dir,
                env=env,
                partial_trace_text=partial_trace_snapshot,
            )
            portfolio_note = (
                "Tier 1 Search-Order Portfolio (`--try-old-strands`, `--check-nonces`, `--reverse-nodes`) "
                "also failed to terminate, confirming a true algebraic unification loop in the protocol roles."
            )
            if autopsy_report:
                raise CPSABuildError(f"{initial_snowball_msg}\n{portfolio_note}\n\n{autopsy_report}")
            raise CPSABuildError(f"{last_snowball_msg}\n{portfolio_note}")

    # Target 2 (Optional): Full derivation search graph (capped within remaining 15s budget)
    if build_full_graph:
        remaining_sec = max(1.0, max_budget_sec - (time.monotonic() - start_ts))
        target_full_xhtml = f"{stem}.xhtml"
        try:
            full_cmd = ["make", target_full_xhtml]
            if winning_herald_options:
                cli_flags = [f"--{opt}" for opt in winning_herald_options]
                full_cmd.append(f"CPSAFLAGS=+RTS -M512m -N -RTS {' '.join(cli_flags)}")
            _run_make_with_hard_timeout(
                full_cmd,
                cwd=build_dir,
                env=env,
                timeout_seconds=remaining_sec,
            )
        except CPSABuildError:
            logger.warning("Full derivation graph %s exceeded remaining budget; keeping shapes graph.", target_full_xhtml)

    # Verify generated artifact paths
    shapes_txt = build_dir / f"{stem}_shapes.txt"
    full_xhtml = build_dir / f"{stem}.xhtml"
    shapes_xhtml = build_dir / f"{stem}_shapes.xhtml"

    for artifact in [trace_txt, shapes_txt, shapes_xhtml]:
        if not artifact.exists():
            raise CPSABuildError(f"Expected build artifact {artifact} was not produced by make")

    shapes_count = _count_shapes_in_file(shapes_txt)
    logger.info("Build SUCCESS: Generated %s with %d realized shapes", shapes_xhtml.name, shapes_count)

    return CPSABuildArtifacts(
        protocol_stem=stem,
        scm_path=target_scm_in_build,
        trace_txt_path=trace_txt,
        shapes_txt_path=shapes_txt,
        full_graph_xhtml_path=full_xhtml if full_xhtml.exists() else shapes_xhtml,
        shapes_graph_xhtml_path=shapes_xhtml,
        shapes_count=shapes_count,
        winning_herald_options=winning_herald_options,
    )
```

---

### `src/verification_engine/roletran_executability_gate.py`

*sha256:`a32baef5a33b` · 151 lines · 7.2 KB (~1,837 tokens) · lang:`python`*

```python
"""MITRE CPSA Roletran Pre-Flight Executability Gate (<15 ms)."""

import re
import subprocess
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("roletran_gate")


class RoletranVerificationResult(BaseModel):
    """Result of the static executability verification pass."""
    is_executable: bool = Field(..., description="True if all roles are mathematically constructible and destructible")
    error_diagnostic: Optional[str] = Field(None, description="Concise error diagnostic if executability failed")
    procedural_defproc_code: Optional[str] = Field(None, description="Compiled defproc procedural code if successful")
    raw_stderr: str = Field(default="", description="Complete stderr from roletran execution")
    validator_binary: str = Field(default="cpsa4roletran", description="Exact binary executed ('cpsa4roletran' or 'cpsa4 -l 1')")
    roletran_algebra_supported: bool = Field(default=True, description="True if protocol uses basic algebra supported by cpsa4roletran")


def verify_role_executability(scm_path: Path) -> RoletranVerificationResult:
    """Executes cpsa4roletran on a Scheme model to prove term constructibility and destructibility."""
    logger.info("Executing roletran pre-flight executability gate on %s", scm_path)

    if not SYSTEM_CONFIG.CPSA4ROLETRAN_BIN.exists():
        logger.error("cpsa4roletran binary missing at %s", SYSTEM_CONFIG.CPSA4ROLETRAN_BIN)
        raise FileNotFoundError(f"cpsa4roletran binary missing at {SYSTEM_CONFIG.CPSA4ROLETRAN_BIN}")

    try:
        with open(scm_path, "r", encoding="utf-8") as f:
            scm_content = f.read()

        is_dh = "diffie-hellman" in scm_content
        has_stateful_locn = bool(re.search(r"\(\s*(?:load|stor)\b|\blocn\s*\)", scm_content))
        if is_dh or has_stateful_locn:
            # MITRE CPSA 4.4.9 cpsa4roletran only supports stateless basic algebra (send/recv over chan).
            # For Diffie-Hellman or stateful locn/load/stor protocols, validate pre-flight syntax and role well-formedness using cpsa4.
            feature_label = "diffie-hellman" if is_dh else "stateful locn/load/stor"
            logger.info("Protocol uses %s; executing cpsa4 -l 1 pre-flight validation gate", feature_label)
            proc = subprocess.run(
                [str(SYSTEM_CONFIG.CPSA4_BIN), "-l", "1", str(scm_path)],
                capture_output=True,
                text=True,
                timeout=SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS,
                check=False,
            )
            stderr_output = proc.stderr.strip()
            stdout_output = proc.stdout.strip()
            combined = (stderr_output + "\n" + stdout_output).strip()
            # Note: When invoked with '-l 1', cpsa4 validates all defprotocol, defrole,
            # and defskeleton blocks before taking 1 search step and exiting with
            # 'Step limit exceeded' on stderr. Reaching 'Step limit exceeded' proves
            # the specification passed all pre-flight syntax, sort, and role checks.
            is_step_limit_only = (
                "Step limit exceeded" in stderr_output
                and "Role not well formed" not in combined
                and "Expecting" not in combined
            )
            has_real_error = (
                "Role not well formed" in combined
                or ("error" in stderr_output.lower() and not is_step_limit_only)
                or (proc.returncode != 0 and not is_step_limit_only)
            )
            if has_real_error:
                error_msg = ""
                for line in stderr_output.splitlines():
                    if line.strip() and "Step limit exceeded" not in line:
                        error_msg = line.strip()
                        break
                if not error_msg:
                    for line in combined.splitlines():
                        if "Role not well formed" in line or "error" in line.lower() or "Expecting" in line:
                            error_msg = line.strip()
                            break
                error_msg = error_msg or stderr_output[:300] or combined[:300]
                logger.warning("Pre-flight cpsa4 -l 1 validation REJECT: %s", error_msg)
                return RoletranVerificationResult(
                    is_executable=False,
                    error_diagnostic=error_msg,
                    raw_stderr=stderr_output or combined,
                    validator_binary="cpsa4 -l 1",
                    roletran_algebra_supported=False,
                )
            logger.info("Pre-flight cpsa4 -l 1 validation PASS: All roles are algebraically well-formed")
            return RoletranVerificationResult(
                is_executable=True,
                procedural_defproc_code=None,
                raw_stderr="",
                validator_binary="cpsa4 -l 1",
                roletran_algebra_supported=False,
            )

        proc = subprocess.run(
            [str(SYSTEM_CONFIG.CPSA4ROLETRAN_BIN)],
            input=scm_content,
            capture_output=True,
            text=True,
            timeout=SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS,
            check=False,
        )

        stderr_output = proc.stderr.strip()
        stdout_output = proc.stdout.strip()

        if proc.returncode == 0 and not stderr_output:
            logger.info("Roletran PASS: All protocol roles are statically executable")
            return RoletranVerificationResult(
                is_executable=True,
                procedural_defproc_code=stdout_output,
                raw_stderr="",
            )

        # Parse error message and preserve line/col context: e.g. ":6:6: Received term cannot be fully destructured"
        clean_error = stderr_output
        match = re.search(r":(\d+):(\d+):\s*(.*)", stderr_output)
        if match:
            line_no = int(match.group(1))
            col_no = int(match.group(2))
            core_msg = match.group(3).strip()
            scm_lines = scm_content.splitlines()
            offending_line = scm_lines[line_no - 1].strip() if 1 <= line_no <= len(scm_lines) else ""
            if offending_line:
                clean_error = f"{core_msg} (at .scm line {line_no}, col {col_no}: `{offending_line[:160]}`)"
            else:
                clean_error = f"{core_msg} (at .scm line {line_no}, col {col_no})"

        logger.warning("Roletran REJECT: %s", clean_error)
        return RoletranVerificationResult(
            is_executable=False,
            error_diagnostic=clean_error,
            raw_stderr=stderr_output,
        )

    except subprocess.TimeoutExpired:
        logger.error("Roletran check timed out after %d seconds", SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS)
        return RoletranVerificationResult(
            is_executable=False,
            error_diagnostic=f"Roletran verification timed out after {SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS}s",
            raw_stderr="Timeout",
        )
    except Exception as e:
        logger.error("Unexpected failure running roletran: %s", str(e))
        return RoletranVerificationResult(
            is_executable=False,
            error_diagnostic=str(e),
            raw_stderr=str(e),
        )
```

---

### `src/verification_engine/snowball_autopsy.py`

*sha256:`a293af53c0ec` · 451 lines · 17.7 KB (~4,532 tokens) · lang:`python`*

```python
"""CPSA 4.4.9 State-Space Snowball Classifier, Herald Injector, and Partial `.txt` Trace Autopsy.

Strictly isolates state-space explosion / non-termination failures (`timed out`, `Step limit exceeded`,
`Strand bound exceeded`, `Heap exhausted`) from ordinary compiler/syntax errors, and extracts a
surgical derivation autopsy from partial `cpsa4` `.txt` output when deterministic search-order
strategies (`--try-old-strands`, `--check-nonces`, `--reverse-nodes`) cannot resolve an
algebraic unification loop.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple

from src.logging_config import get_pipeline_logger
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("snowball_autopsy")

# Ordered portfolio of CPSA 4.4.9 search-order configurations (Manual §9.1.1 & §10.5)
# Tried deterministically (0 LLM tokens) ONLY when the default cpsa4 search snowballs.
SNOWBALL_HERALD_PORTFOLIO: List[Tuple[str, List[str], List[str]]] = [
    (
        "oldest-strand-first (try-old-strands)",
        ["--try-old-strands"],
        ["try-old-strands"],
    ),
    (
        "oldest-strand + nonce-first (try-old-strands + check-nonces)",
        ["--try-old-strands", "--check-nonces"],
        ["try-old-strands", "check-nonces"],
    ),
    (
        "oldest-strand + nonce-first + youngest-node (try-old-strands + check-nonces + reverse-nodes)",
        ["--try-old-strands", "--check-nonces", "--reverse-nodes"],
        ["try-old-strands", "check-nonces", "reverse-nodes"],
    ),
]

_SNOWBALL_ERROR_MARKERS: Tuple[str, ...] = (
    "timed out after",
    "state-space explosion",
    "infinite strand loop",
    "step limit exceeded",
    "step limit reached",
    "strand bound exceeded",
    "heap exhausted",
    "out of memory",
    "aborting after applying 500 rules",
)


def is_snowball_state_error(error_msg: Optional[str]) -> bool:
    """Returns True strictly when `error_msg` is a CPSA 4.4.9 state-space snowball / non-termination error.

    All other errors (syntax errors, undeclared variables, malformed terms, sort mismatches,
    roletran executability errors, or 0-shape dead skeletons) return False and follow the
    normal pipeline route.
    """
    if not error_msg:
        return False
    lowered = error_msg.lower()
    return any(marker in lowered for marker in _SNOWBALL_ERROR_MARKERS)


def inject_herald_options_into_scm(scm_text: str, herald_options: List[str]) -> str:
    """Injects winning search-order options (e.g. `(try-old-strands)`, `(check-nonces)`)
    into the top-level `(herald ...)` form of a `.scm` file without duplicating existing flags.
    """
    valid_opts = [
        opt for opt in herald_options
        if opt in {"try-old-strands", "check-nonces", "reverse-nodes"}
    ]
    if not valid_opts:
        return scm_text

    herald_match = re.search(r"\(\s*herald\b", scm_text)
    if not herald_match:
        opts_str = " ".join(f"({opt})" for opt in valid_opts)
        return f'(herald "Protocol Verification Suite" {opts_str})\n\n{scm_text}'

    start_idx = herald_match.start()
    depth = 0
    in_string = False
    escape = False
    end_idx = -1

    for idx in range(start_idx, len(scm_text)):
        ch = scm_text[idx]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if not in_string:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end_idx = idx
                    break

    if end_idx == -1:
        return scm_text

    herald_block = scm_text[start_idx:end_idx]
    additions: List[str] = []
    for opt in valid_opts:
        if not re.search(rf"\(\s*{re.escape(opt)}\s*\)", herald_block):
            additions.append(f"({opt})")

    if not additions:
        return scm_text

    updated_herald = f"{herald_block} {' '.join(additions)})"
    return scm_text[:start_idx] + updated_herald + scm_text[end_idx + 1 :]


def _extract_balanced_sexp(text: str, start_pos: int) -> Tuple[str, int]:
    """Extracts a balanced parenthesized S-expression starting at or after `start_pos`."""
    open_idx = text.find("(", start_pos)
    if open_idx == -1:
        return "", len(text)
    depth = 0
    in_string = False
    escape = False
    for idx in range(open_idx, len(text)):
        ch = text[idx]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if not in_string:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return text[open_idx : idx + 1], idx + 1
    return text[open_idx:], len(text)


def _normalize_primed_identifiers(sexp_str: str) -> str:
    """Collapses CPSA primed variable suffixes (`var-0`, `var-1`, `var-12`) to `var-*`
    so repeating augmentation operations across generations group together cleanly.
    """
    collapsed_ws = " ".join(sexp_str.split())
    return re.sub(r"\b([a-zA-Z_][a-zA-Z0-9_\-]*)-\d+\b", r"\1-*", collapsed_ws)


def _parse_skeleton_records(raw_txt: str) -> Tuple[int, Optional[str], List[Dict[str, Any]]]:
    """Parses `(defskeleton ...)` blocks from a partial or bounded `cpsa4` `.txt` file.

    Returns:
        (exploding_pov_index, exploding_pov_desc, parsed_skeleton_records)
    """
    # CPSA emits `(defprotocol ...)` before each top-level POV skeleton search tree,
    # and emits `(comment "Nothing left to do")` when a POV search tree finishes.
    chunks = re.split(r"(?=\(\s*defprotocol\b)", raw_txt)
    protocol_sections = [c for c in chunks if re.match(r"\A\(\s*defprotocol\b", c.strip())]

    target_section = raw_txt
    exploding_pov_idx = 1
    if protocol_sections:
        for idx, sec in enumerate(protocol_sections, 1):
            if '(comment "Nothing left to do")' not in sec:
                target_section = sec
                exploding_pov_idx = idx
                break
        else:
            # If all sections completed or `-l` stopped inside the last section
            target_section = protocol_sections[-1]
            exploding_pov_idx = len(protocol_sections)

    records: List[Dict[str, Any]] = []
    pos = 0
    skel_pattern = re.compile(r"\(\s*defskeleton\b")

    while True:
        match = skel_pattern.search(target_section, pos)
        if not match:
            break
        block, next_pos = _extract_balanced_sexp(target_section, match.start())
        if not block:
            break
        pos = next_pos

        label_m = re.search(r"\(\s*label\s+(\d+)\s*\)", block)
        parent_m = re.search(r"\(\s*parent\s+(\d+)\s*\)", block)
        comment_m = re.search(r'\(\s*comment\s+"([^"]+)"\s*\)', block)
        unrealized_m = re.search(r"\(\s*unrealized\s+([^)]*)\)", block)
        strands = re.findall(r"\(\s*defstrand(?:max)?\s+([^\s()]+)\s+(\d+)", block)

        op_match = re.search(r"\(\s*operation\b", block)
        op_raw = ""
        op_type = ""
        op_action = ""
        op_term = ""
        op_node = ""
        if op_match:
            op_raw, _ = _extract_balanced_sexp(block, op_match.start())
            # Format: (operation <test-type> (<action> ...) <critical-term> (<strand> <node>))
            header_m = re.match(
                r"\(\s*operation\s+([^\s()]+)\s+(\([^)]+\)|[^\s()]+)\s*(.*)\)\Z",
                " ".join(op_raw.split()),
            )
            if header_m:
                op_type = header_m.group(1)
                op_action = header_m.group(2)
                remainder = header_m.group(3).strip()
                node_m = re.search(r"\(\s*(\d+\s+\d+)\s*\)\s*(?:\(\s*seen-ops\b.*\))?\Z", remainder)
                if node_m:
                    op_node = f"({node_m.group(1)})"
                    op_term = remainder[: node_m.start()].strip()
                else:
                    op_term = remainder

        # Parse (vars ...) declarations to inspect primed variable explosion
        vars_match = re.search(r"\(\s*vars\b", block)
        vars_block = ""
        if vars_match:
            vars_block, _ = _extract_balanced_sexp(block, vars_match.start())

        records.append({
            "label": int(label_m.group(1)) if label_m else len(records),
            "parent": int(parent_m.group(1)) if parent_m else None,
            "comment": comment_m.group(1) if comment_m else None,
            "unrealized": " ".join(unrealized_m.group(1).split()) if unrealized_m else "",
            "strands": strands,
            "strand_count": len(strands),
            "op_raw": " ".join(op_raw.split()) if op_raw else "",
            "op_type": op_type,
            "op_action": op_action,
            "op_term": op_term,
            "op_node": op_node,
            "vars_block": vars_block,
        })

    pov_desc = None
    if records:
        first_rec = records[0]
        first_strands = ", ".join(f"{r}(h={h})" for r, h in first_rec["strands"])
        pov_desc = f"POV Skeleton #{exploding_pov_idx}"
        if first_rec.get("comment"):
            pov_desc += f' ("{first_rec["comment"]}")'
        if first_strands:
            pov_desc += f" [Initial strands: {first_strands}]"

    return exploding_pov_idx, pov_desc, records


def _extract_primed_variable_stats(vars_block: str) -> List[Tuple[str, str, int]]:
    """Extracts `(base_var_name, sort, clone_count)` for primed variables (`x-0`, `x-1`, ...)
    inside a skeleton's `(vars ...)` block.
    """
    if not vars_block:
        return []
    decl_groups = re.findall(r"\(([^()]+)\)", vars_block)
    base_counts: Counter[Tuple[str, str]] = Counter()
    for grp in decl_groups:
        tokens = grp.strip().split()
        if len(tokens) < 2 or tokens[0] == "vars":
            continue
        sort_name = tokens[-1]
        for var_tok in tokens[:-1]:
            m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_\-]*)-\d+$", var_tok)
            if m:
                base_counts[(m.group(1), sort_name)] += 1
    ranked = sorted(base_counts.items(), key=lambda kv: (-kv[1], kv[0][0]))
    return [(base, sort_name, count) for (base, sort_name), count in ranked]


def analyze_snowball_trace_text(raw_txt: str) -> str:
    """Analyzes a partial or step-bounded `cpsa4` `.txt` derivation file and returns a
    concise, actionable Snowball Autopsy Report pinpointing the exact looping role,
    authentication test, critical term, and cloned variables.
    """
    if not raw_txt or "(defskeleton" not in raw_txt:
        return ""

    _, pov_desc, records = _parse_skeleton_records(raw_txt)
    if not records:
        return ""

    by_label: Dict[int, Dict[str, Any]] = {r["label"]: r for r in records}
    depth_map: Dict[int, int] = {}
    for r in records:
        lbl = r["label"]
        parent = r["parent"]
        depth_map[lbl] = (depth_map.get(parent, 0) + 1) if parent is not None else 0

    deepest_rec = max(records, key=lambda r: (depth_map.get(r["label"], 0), r["strand_count"]))
    max_depth = depth_map.get(deepest_rec["label"], 0)
    max_strands = max(r["strand_count"] for r in records)

    # Reconstruct the deepest parent -> child derivation chain
    deepest_chain: List[Dict[str, Any]] = []
    curr: Optional[Dict[str, Any]] = deepest_rec
    visited = set()
    while curr is not None and curr["label"] not in visited:
        visited.add(curr["label"])
        deepest_chain.append(curr)
        curr = by_label.get(curr["parent"]) if curr["parent"] is not None else None
    deepest_chain.reverse()

    # Count normalized operations across all skeletons and along the deepest chain
    op_counter: Counter[Tuple[str, str, str]] = Counter()
    chain_op_counter: Counter[Tuple[str, str, str]] = Counter()
    role_spawn_counter: Counter[str] = Counter()

    for r in records:
        if r["op_type"] and r["op_action"]:
            norm_action = _normalize_primed_identifiers(r["op_action"])
            norm_term = _normalize_primed_identifiers(r["op_term"])
            op_counter[(r["op_type"], norm_action, norm_term)] += 1
            added_m = re.match(r"\(\s*added-strand\s+([^\s()]+)\s+(\d+)\s*\)", norm_action)
            if added_m:
                role_spawn_counter[f"{added_m.group(1)} (height {added_m.group(2)})"] += 1

    for r in deepest_chain:
        if r["op_type"] and r["op_action"]:
            norm_action = _normalize_primed_identifiers(r["op_action"])
            norm_term = _normalize_primed_identifiers(r["op_term"])
            chain_op_counter[(r["op_type"], norm_action, norm_term)] += 1

    primed_stats = _extract_primed_variable_stats(deepest_rec.get("vars_block", ""))

    # Build the structured autopsy report
    lines: List[str] = [
        "=== CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT (Tier 2 Trace Analysis) ===",
        f"Exploding Query: {pov_desc or 'POV Skeleton'}",
        (
            f"Derivation Stats: {len(records)} skeletons inspected | "
            f"Max derivation depth: {max_depth} | Max concurrent strands in a skeleton: {max_strands}"
        ),
    ]

    if role_spawn_counter:
        top_roles = ", ".join(f"{role}: {cnt}x" for role, cnt in role_spawn_counter.most_common(4))
        lines.append(f"Repeatedly Augmented Roles (`added-strand`): {top_roles}")

    if op_counter:
        lines.append("Top Looping Authentication Test Operations Across Derivation Tree:")
        for (op_type, norm_action, norm_term), count in op_counter.most_common(3):
            chain_cnt = chain_op_counter.get((op_type, norm_action, norm_term), 0)
            lines.append(
                f"  - [{count}x total, {chain_cnt}x in deepest chain] "
                f"Test: `{op_type}` | Action: `{norm_action}` | Unifying Critical Term: `{norm_term[:220]}`"
            )

    if primed_stats:
        cloned_summary = ", ".join(
            f"{base}:{sort_name} (cloned {cnt}x as {base}-0..{base}-{cnt - 1})"
            for base, sort_name, cnt in primed_stats[:6]
        )
        lines.append(f"Cloned Unconstrained Variables in Deepest Skeleton: {cloned_summary}")

    if deepest_rec.get("unrealized"):
        lines.append(f"Remaining Unrealized Reception Nodes in Deepest Skeleton: ({deepest_rec['unrealized']})")

    # Synthesize targeted Tier 3 structural repair directives from the autopsy findings
    lines.append("Targeted Structural Anti-Snowballing Fixes Required (Tier 3):")
    full_ops_str = " ".join(
        f"{t} {a} {term}" for (t, a, term) in op_counter.keys()
    )
    if "encryption-test" in full_ops_str or "(enc " in full_ops_str:
        lines.append(
            "  1. DOMAIN-SEPARATE EVERY `(enc ...)` AND `(hash ...)` TERM: The solver is unifying an outgoing "
            "role encryption with an incoming reception (`encryption-test` loop). Distinguish request vs. response "
            "`[\"enc\", ...]` and `[\"hash\", ...]` terms using the actual RFC message type, header, opcode, or "
            "direction label fields from the RFC (and distinct prefix sorts `data` vs `text`) so order-sorted "
            "unification (`unify_0`) fails immediately between different protocol flights."
        )
    if "(ltk " in full_ops_str or any(s == "name" for _, s, _ in primed_stats):
        lines.append(
            "  2. PRINCIPAL INEQUALITY FACTS & IDENTITY BINDING: Add `[\"neq\", \"<principal_a>\", \"<principal_b>\"]` "
            "to `facts` in every `CPSAPreskeleton` to block `A = B` symmetric reflection, and include both "
            "communicating `name` variables inside encrypted flights so augmented strands bind to existing "
            "principals instead of spawning unconstrained `name-0`, `name-1` peers."
        )
    lines.append(
        "  3. SORT SEPARATION (`data` vs `text`): Declare fresh `uniq-orig` nonces/secrets as sort `\"data\"` "
        "and predictable identifiers/headers/labels as sort `\"text\"` (CPSA Primer §16.2) so CPSA's order-sorted "
        "unifier cannot cross-unify a fresh nonce slot with a metadata/identifier slot."
    )

    return "\n".join(lines)


def generate_snowball_autopsy_report(
    scm_path: Path,
    build_dir: Path,
    env: Dict[str, str],
    partial_trace_text: Optional[str] = None,
    step_limit: int = 120,
) -> str:
    """Generates a deterministic Snowball Autopsy Report from `<stem>.txt` or by running a
    fast (<0.4s) step-bounded `cpsa4 -l <step_limit>` probe when `<stem>.txt` was buffered.
    """
    raw_txt = partial_trace_text or ""
    if raw_txt.count("(defskeleton") < 4 and SYSTEM_CONFIG.CPSA4_BIN.exists():
        autopsy_txt_path = build_dir / f"{scm_path.stem}_autopsy.txt"
        try:
            cmd = [
                str(SYSTEM_CONFIG.CPSA4_BIN),
                "+RTS",
                "-M512m",
                "-N",
                "-RTS",
                "-l",
                str(step_limit),
                "-o",
                str(autopsy_txt_path),
                str(scm_path),
            ]
            subprocess.run(
                cmd,
                cwd=build_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=4.0,
                check=False,
            )
            if autopsy_txt_path.exists():
                probed = autopsy_txt_path.read_text(encoding="utf-8", errors="replace")
                if probed.count("(defskeleton") > raw_txt.count("(defskeleton"):
                    raw_txt = probed
        except Exception as exc:
            logger.debug("Bounded cpsa4 autopsy probe encountered exception: %s", exc)
        finally:
            if autopsy_txt_path.exists():
                try:
                    autopsy_txt_path.unlink()
                except Exception:
                    pass

    return analyze_snowball_trace_text(raw_txt)
```

---

### `src/verification_engine/trajectory_metadata_exporter.py`

*sha256:`62a363878d5b` · 1114 lines · 45.7 KB (~11,707 tokens) · lang:`python`*

```python
"""Programmatic Trajectory & Formal Verification Metadata Exporter.

Parses MITRE CPSA 4.4.9 solver outputs (`<stem>.txt` and `<stem>_shapes.txt`),
computes deterministic quality tiers (`GOLD`, `SILVER`, `BRONZE`, `REJECTED`),
prepends structured MoE router conditioning headers to `.scm` files, and writes
the separated `<stem>_trajectory.json` artifact for ROCm Megatron-LM post-training.
"""

import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import get_pipeline_logger
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("trajectory_exporter")


def split_top_level_sexprs(content: str) -> List[str]:
    """Splits a CPSA Scheme/text file into top-level balanced S-expressions."""
    blocks: List[str] = []
    depth = 0
    in_string = False
    escape = False
    in_comment = False
    start_idx: Optional[int] = None

    for idx, ch in enumerate(content):
        if in_comment:
            if ch == "\n":
                in_comment = False
            continue

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == ";":
            in_comment = True
            continue
        if ch == '"':
            in_string = True
            continue

        if ch == "(":
            if depth == 0:
                start_idx = idx
            depth += 1
        elif ch == ")":
            if depth > 0:
                depth -= 1
                if depth == 0 and start_idx is not None:
                    blocks.append(content[start_idx : idx + 1])
                    start_idx = None

    return blocks


def _extract_int_clause(sexpr: str, keyword: str) -> Optional[int]:
    match = re.search(rf"\(\s*{re.escape(keyword)}\s+(\d+)\s*\)", sexpr)
    return int(match.group(1)) if match else None


def _has_flag_clause(sexpr: str, keyword: str) -> bool:
    return bool(re.search(rf"\(\s*{re.escape(keyword)}\s*\)", sexpr))


def _extract_clause_block(sexpr: str, keyword: str) -> Optional[str]:
    """Extracts a complete balanced sub-expression starting with `(<keyword>`."""
    pattern = re.compile(rf"\(\s*{re.escape(keyword)}\b")
    match = pattern.search(sexpr)
    if not match:
        return None
    sub = sexpr[match.start() :]
    blocks = split_top_level_sexprs(sub)
    return blocks[0] if blocks else None


def _extract_root_deflisteners(sexpr: str) -> List[str]:
    """Extracts all listener terms from a root preskeleton if `(deflistener ...)` clauses are present outside `(operation ...)`."""
    op_block = _extract_clause_block(sexpr, "operation")
    cleaned = sexpr.replace(op_block, "") if op_block else sexpr
    stripped = cleaned.strip()
    inner_body = (
        stripped[1:-1]
        if (stripped.startswith("(") and stripped.endswith(")"))
        else stripped
    )
    terms: List[str] = []
    for sub in split_top_level_sexprs(inner_body):
        if re.match(r"^\(\s*deflistener\b", sub):
            inner = re.sub(r"^\(\s*deflistener\s+", "", sub[:-1]).strip()
            if inner:
                terms.append(inner)
    return terms


def _extract_root_deflistener(sexpr: str) -> Optional[str]:
    """Extracts the first listener term from a root preskeleton if `(deflistener ...)` is present outside `(operation ...)`."""
    terms = _extract_root_deflisteners(sexpr)
    return terms[0] if terms else None


def _extract_skeleton_vars_sorts(sexpr: str) -> Dict[str, str]:
    """Extracts a mapping from skeleton variable name to CPSA sort from `(vars ...)`."""
    vb = _extract_clause_block(sexpr, "vars")
    if not vb:
        return {}
    s = vb.strip()
    inner = re.sub(r"^\(\s*vars\b", "", s[:-1]).strip()
    sorts: Dict[str, str] = {}
    for decl in split_top_level_sexprs(inner):
        toks = decl[1:-1].split()
        if len(toks) >= 2:
            sort_name = toks[-1]
            for v in toks[:-1]:
                sorts[v] = sort_name
    return sorts


def _extract_defstrands(sexpr: str) -> List[Dict[str, Any]]:
    """Extracts all `(defstrand <role> <height> (<role_var> <skel_term>)*)` instances from a skeleton block."""
    # Exclude any `(defstrand ...)` inside `(operation ...)`
    op_block = _extract_clause_block(sexpr, "operation")
    cleaned = sexpr.replace(op_block, "") if op_block else sexpr
    stripped = cleaned.strip()
    inner_body = (
        stripped[1:-1]
        if (stripped.startswith("(") and stripped.endswith(")"))
        else stripped
    )
    strands: List[Dict[str, Any]] = []
    for sub in split_top_level_sexprs(inner_body):
        match = re.match(r"^\(\s*defstrand(?:max)?\s+([^\s\(\)]+)(?:\s+(\d+))?(.*)\)$", sub, flags=re.DOTALL)
        if not match:
            continue
        role_name = match.group(1)
        height = int(match.group(2)) if match.group(2) else None
        tail = match.group(3) or ""
        maplets: Dict[str, str] = {}
        for mp in split_top_level_sexprs(tail):
            inner = mp[1:-1].strip()
            parts = inner.split(None, 1)
            if len(parts) == 2:
                maplets[parts[0].strip()] = " ".join(parts[1].split())
        strand_entry: Dict[str, Any] = {"role": role_name, "height": height}
        if maplets:
            strand_entry["maplets"] = maplets
        strands.append(strand_entry)
    return strands


def _analyze_shape_agreement_and_reflection(
    strands: List[Dict[str, Any]],
    shape_label: Optional[int],
    vars_sorts: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Inspects multi-strand realized shapes for CPSA parameter agreement/disagreement
    (Lowe MITM / Unknown Key Share, CPSA Goals Manual §4.1) and role self-reflection.
    """
    if len(strands) < 2:
        return {
            "same_role_reflection": False,
            "disagreed_parameters": [],
            "agreed_parameters": [],
        }

    sorts_lookup = vars_sorts or {}
    pov_strand = strands[0]
    pov_role = pov_strand.get("role")
    pov_maplets: Dict[str, str] = pov_strand.get("maplets") or {}
    pov_values = set(pov_maplets.values())

    peer_strands = strands[1:]
    peer_roles = [s.get("role") for s in peer_strands if s.get("role")]
    same_role_reflection = bool(peer_roles and all(r == pov_role for r in peer_roles))

    disagreed: List[Dict[str, Any]] = []
    agreed: List[str] = []

    for ps in peer_strands:
        p_role = ps.get("role")
        # Compare parameter agreement across distinct counterparty roles (unless all strands share pov_role)
        if p_role == pov_role and not same_role_reflection:
            continue
        p_maplets: Dict[str, str] = ps.get("maplets") or {}
        for param, p_val in p_maplets.items():
            if param in pov_maplets:
                pov_val = pov_maplets[param]
                var_sort = sorts_lookup.get(pov_val) or sorts_lookup.get(p_val) or "unknown"
                if var_sort == "chan":
                    continue
                if p_val == pov_val:
                    if param not in agreed:
                        agreed.append(param)
                else:
                    disagreed.append({
                        "shape_label": shape_label,
                        "pov_role": pov_role,
                        "peer_role": p_role,
                        "parameter": param,
                        "sort": var_sort,
                        "pov_value": pov_val,
                        "peer_value": p_val,
                    })
            else:
                m = re.match(r"^([a-zA-Z0-9_]+)-\d+$", p_val)
                if m and m.group(1) in pov_values:
                    base_val = m.group(1)
                    var_sort = sorts_lookup.get(base_val) or sorts_lookup.get(p_val) or "unknown"
                    if var_sort == "chan":
                        continue
                    disagreed.append({
                        "shape_label": shape_label,
                        "pov_role": pov_role,
                        "peer_role": p_role,
                        "parameter": param,
                        "sort": var_sort,
                        "pov_value": base_val,
                        "peer_value": p_val,
                    })

    return {
        "same_role_reflection": same_role_reflection,
        "disagreed_parameters": disagreed,
        "agreed_parameters": agreed,
    }


def extract_shape_analysis_sentences(txt_path: Optional[Path]) -> List[str]:
    """Runs `cpsa4sas` on `<stem>.txt` (CPSA Primer §17, Spec Appendix C) to extract
    first-order coherent logic `(defgoal ...)` Shape Analysis Sentences for each POV.
    """
    if not txt_path or not txt_path.exists():
        return []
    sas_bin = getattr(SYSTEM_CONFIG, "CPSA4SAS_BIN", None)
    if not sas_bin or not Path(sas_bin).exists():
        return []
    try:
        raw_txt = txt_path.read_text(encoding="utf-8", errors="replace")
        proc = subprocess.run(
            [str(sas_bin)],
            input=raw_txt,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if proc.returncode != 0 or not proc.stdout:
            return []
        goals: List[str] = []
        for block in split_top_level_sexprs(proc.stdout):
            if block.startswith("(defgoal"):
                goals.append(block)
        return goals
    except Exception:
        return []


def _extract_comment_string(sexpr: str) -> Optional[str]:
    """Extracts the first descriptive user comment from a skeleton block."""
    for match in re.finditer(r'\(\s*comment\s+"([^"]+)"\s*\)', sexpr):
        text = match.group(1)
        if not text.startswith("Not a skeleton") and "in cohort" not in text and "empty cohort" not in text:
            return text
    return None


def _extract_goal_satisfaction(sexpr: str) -> Optional[str]:
    sat_block = _extract_clause_block(sexpr, "satisfies")
    if not sat_block:
        return None
    if re.search(r"\(\s*satisfies\s+yes\s*\)", sat_block):
        return "yes"
    if re.search(r"\(\s*no\b", sat_block):
        return "no"
    return sat_block


def analyze_exploration_txt(
    txt_path: Optional[Path],
    dead_root_labels: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """Extracts compact search telemetry, cohort operation counts, and dead-branch diagnostics from `<stem>.txt`."""
    empty_ops = {
        "encryption_tests": 0,
        "nonce_tests": 0,
        "channel_tests": 0,
        "generalizations": 0,
        "collapsed_shapes": 0,
        "added_strands": 0,
        "contractions": 0,
        "displacements": 0,
        "added_listeners": 0,
    }
    if not txt_path or not txt_path.exists():
        return {
            "source_file": txt_path.name if txt_path else None,
            "txt_file_size_bytes": 0,
            "total_explored_labels": 0,
            "dead_branch_nodes_count": 0,
            "step_limit_or_bound_hit": False,
            "state_explosion_detected": False,
            "authentication_tests_summary": empty_ops,
            "dead_preskeleton_diagnostics": [],
        }

    content = txt_path.read_text(encoding="utf-8", errors="replace")
    file_size = txt_path.stat().st_size
    labels = [int(m.group(1)) for m in re.finditer(r"\(\s*label\s+(\d+)\s*\)", content)]
    total_explored = len(labels)
    dead_count = len(re.findall(r"\(\s*dead\s*\)", content))
    limit_hit = any(
        marker in content
        for marker in (
            "Step count limited",
            "Strand count bounded",
            "Cohort limit",
            "aborted",
        )
    )

    ops_summary = dict(empty_ops)
    blocks = split_top_level_sexprs(content)
    target_roots = set(dead_root_labels) if dead_root_labels else set()
    parent_to_root: Dict[int, int] = {}
    deepest_dead_per_root: Dict[int, Dict[str, Any]] = {}

    for block in blocks:
        if not block.startswith("(defskeleton"):
            continue
        op_block = _extract_clause_block(block, "operation")
        if op_block:
            flat_op = " ".join(op_block.split())
            if "encryption-test" in flat_op:
                ops_summary["encryption_tests"] += 1
            elif "nonce-test" in flat_op:
                ops_summary["nonce_tests"] += 1
            elif "channel-test" in flat_op:
                ops_summary["channel_tests"] += 1
            elif "generalization" in flat_op:
                ops_summary["generalizations"] += 1
            elif "collapsed" in flat_op:
                ops_summary["collapsed_shapes"] += 1

            if "(added-strand" in flat_op:
                ops_summary["added_strands"] += 1
            elif "(contracted" in flat_op:
                ops_summary["contractions"] += 1
            elif "(displaced" in flat_op:
                ops_summary["displacements"] += 1
            elif "(added-listener" in flat_op:
                ops_summary["added_listeners"] += 1

        if not target_roots:
            continue
        lbl = _extract_int_clause(block, "label")
        if lbl is None:
            continue
        parent = _extract_int_clause(block, "parent")
        if parent is None:
            parent_to_root[lbl] = lbl
            root_lbl = lbl
        else:
            root_lbl = parent_to_root.get(parent, parent)
            parent_to_root[lbl] = root_lbl

        if root_lbl in target_roots:
            unrealized = _extract_clause_block(block, "unrealized")
            is_dead_node = _has_flag_clause(block, "dead") or "empty cohort" in block
            if is_dead_node or lbl == root_lbl:
                deepest_dead_per_root[root_lbl] = {
                    "root_label": root_lbl,
                    "deepest_dead_label": lbl,
                    "parent_label": parent,
                    "last_operation": " ".join(op_block.split()) if op_block else None,
                    "stuck_unrealized_nodes": " ".join(unrealized.split()) if unrealized else None,
                }

    dead_diagnostics = list(deepest_dead_per_root.values())

    return {
        "source_file": txt_path.name,
        "txt_file_size_bytes": file_size,
        "total_explored_labels": total_explored,
        "dead_branch_nodes_count": dead_count,
        "step_limit_or_bound_hit": limit_hit,
        "state_explosion_detected": total_explored > 500,
        "authentication_tests_summary": ops_summary,
        "dead_preskeleton_diagnostics": dead_diagnostics,
    }


def analyze_shapes_txt(shapes_txt_path: Optional[Path]) -> Dict[str, Any]:
    """Programmatically parses `<stem>_shapes.txt` into per-preskeleton formal verification verdicts."""
    if not shapes_txt_path or not shapes_txt_path.exists():
        return {
            "source_file": shapes_txt_path.name if shapes_txt_path else None,
            "shapes_file_size_bytes": 0,
            "total_preskeletons": 0,
            "total_realized_shapes": 0,
            "per_preskeleton_outcomes": [],
        }

    content = shapes_txt_path.read_text(encoding="utf-8", errors="replace")
    file_size = shapes_txt_path.stat().st_size
    blocks = split_top_level_sexprs(content)

    preskeleton_groups: List[Dict[str, Any]] = []
    label_to_group_idx: Dict[int, int] = {}

    for block in blocks:
        if not block.startswith("(defskeleton"):
            continue
        lbl = _extract_int_clause(block, "label")
        parent = _extract_int_clause(block, "parent")
        is_shape = _has_flag_clause(block, "shape")

        if parent is None:
            listener_terms = _extract_root_deflisteners(block)
            listener_term = listener_terms[0] if listener_terms else None
            has_listener = bool(listener_terms)
            initial_strands = _extract_defstrands(block)
            group_idx = len(preskeleton_groups)
            if lbl is not None:
                label_to_group_idx[lbl] = group_idx

            group: Dict[str, Any] = {
                "skeleton_index": group_idx,
                "root_label": lbl,
                "skeleton_type": "secrecy_listener_pov" if has_listener else "participant_pov",
                "comment": _extract_comment_string(block),
                "has_deflistener": has_listener,
                "listener_term": listener_term,
                "listener_terms": listener_terms,
                "initial_strand_count": len(initial_strands),
                "realized_shape_labels": [],
                "realized_shapes_count": 0,
                "min_strands_in_realized_shape": 0,
                "max_strands_in_realized_shape": 0,
                "instantiated_roles_in_shape": [],
                "is_trivial_single_strand_shape": False,
                "has_self_reflection_split": False,
                "has_same_role_reflection": False,
                "disagreed_parameters": [],
                "agreed_parameters": [],
                "goal_satisfied": _extract_goal_satisfaction(block),
                "verdict": "UNREALIZED",
            }
            if is_shape:
                strands = _extract_defstrands(block)
                vars_sorts = _extract_skeleton_vars_sorts(block)
                ag = _analyze_shape_agreement_and_reflection(strands, lbl, vars_sorts)
                group["realized_shape_labels"].append(lbl)
                group["realized_shapes_count"] = 1
                group["min_strands_in_realized_shape"] = len(strands)
                group["max_strands_in_realized_shape"] = len(strands)
                group["instantiated_roles_in_shape"] = strands
                group["has_same_role_reflection"] = bool(ag["same_role_reflection"])
                group["disagreed_parameters"].extend(ag["disagreed_parameters"])
                group["agreed_parameters"] = list(ag["agreed_parameters"])
            preskeleton_groups.append(group)
        else:
            group_idx = label_to_group_idx.get(parent, len(preskeleton_groups) - 1)
            if lbl is not None and group_idx >= 0:
                label_to_group_idx[lbl] = group_idx
            if is_shape and 0 <= group_idx < len(preskeleton_groups):
                group = preskeleton_groups[group_idx]
                strands = _extract_defstrands(block)
                vars_sorts = _extract_skeleton_vars_sorts(block)
                ag = _analyze_shape_agreement_and_reflection(strands, lbl, vars_sorts)
                group["realized_shape_labels"].append(lbl)
                group["realized_shapes_count"] += 1
                if group["min_strands_in_realized_shape"] == 0 or len(strands) < group["min_strands_in_realized_shape"]:
                    group["min_strands_in_realized_shape"] = len(strands)
                if len(strands) >= group["max_strands_in_realized_shape"]:
                    group["max_strands_in_realized_shape"] = len(strands)
                    group["instantiated_roles_in_shape"] = strands
                if ag["same_role_reflection"]:
                    group["has_same_role_reflection"] = True
                for dp in ag["disagreed_parameters"]:
                    if dp not in group["disagreed_parameters"]:
                        group["disagreed_parameters"].append(dp)
                for ap in ag["agreed_parameters"]:
                    if ap not in group["agreed_parameters"]:
                        group["agreed_parameters"].append(ap)
                sat = _extract_goal_satisfaction(block)
                if sat is not None:
                    group["goal_satisfied"] = sat

    total_shapes = 0
    for group in preskeleton_groups:
        shapes_cnt = group["realized_shapes_count"]
        total_shapes += shapes_cnt
        init_strands = group.get("initial_strand_count", 1)
        min_strands = group.get("min_strands_in_realized_shape", group["max_strands_in_realized_shape"])
        max_strands = group["max_strands_in_realized_shape"]
        if group["skeleton_type"] == "participant_pov":
            if shapes_cnt == 0:
                group["verdict"] = "DEAD_HANDSHAKE"
                group["is_trivial_single_strand_shape"] = False
                group["has_self_reflection_split"] = False
            elif min_strands >= 2 and max_strands > init_strands:
                group["verdict"] = "AUTHENTICATED_MULTI_STRAND"
                group["is_trivial_single_strand_shape"] = False
                group["has_self_reflection_split"] = False
            else:
                group["verdict"] = "TRIVIAL_SINGLE_STRAND"
                group["is_trivial_single_strand_shape"] = True
                group["has_self_reflection_split"] = bool(min_strands == 1 and max_strands >= 2)
        else:
            if shapes_cnt == 0:
                group["verdict"] = "SECRECY_PROVED_UNREALIZED"
                group["is_trivial_single_strand_shape"] = False
            else:
                group["verdict"] = "SECRECY_LEAKED_SHAPE_FOUND"
                group["is_trivial_single_strand_shape"] = max_strands == 1

    return {
        "source_file": shapes_txt_path.name,
        "shapes_file_size_bytes": file_size,
        "total_preskeletons": len(preskeleton_groups),
        "total_realized_shapes": total_shapes,
        "per_preskeleton_outcomes": preskeleton_groups,
    }


def compute_security_findings(
    shapes_analysis: Dict[str, Any],
    exploration_telemetry: Optional[Dict[str, Any]] = None,
    sas_formulas: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Produces an exhaustive, CPSA-4.4.9-manual-grounded formal security verdict report
    orthogonal to `quality_tier` (which grades translation & compilation fidelity).

    Covers all 7 formal dimensions from MITRE's CPSA Primer and Goals & Security Manual:
    1. Role Executability (`ALL_ROLES_EXECUTABLE`, `PARTIAL_DEAD_ROLES`, `NO_ROLES_EXECUTABLE`)
    2. Authentication Profile (`MUTUAL_MULTI_STRAND`, `UNILATERAL_AUTHENTICATED`,
       `CONDITIONAL_BRANCHED_AUTHENTICATION`, `UNAUTHENTICATED_OR_CLEARTEXT_EXECUTABLE`, `NON_EXECUTABLE`)
    3. Parameter Agreement / Lowe MITM (`FULL_PARAMETER_AGREEMENT`, `PRINCIPAL_DISAGREEMENT_MITM_OR_UKS`,
       `PARAMETER_DISAGREEMENT_DETECTED`, `NOT_APPLICABLE_SINGLE_STRAND`)
    4. Role Self-Reflection (`SAME_ROLE_REFLECTION_DETECTED`, `NO_REFLECTION`)
    5. Secrecy Analysis (`SECRECY_PROVED`, `SECRECY_LEAK_DETECTED`, `PARTIAL_SECRECY`, `NOT_APPLICABLE_NO_LISTENER`)
    6. Explicit `defgoal` Satisfaction (`ALL_SATISFIED`, `COUNTEREXAMPLE_FOUND`, `NO_EXPLICIT_DEFGOALS`)
    7. Coherent-Logic Shape Analysis Sentences (`cpsa4sas`) & Authentication Test Telemetry (`encryption-test`, `nonce-test`, `channel-test`).
    """
    outcomes = shapes_analysis.get("per_preskeleton_outcomes", [])
    participant_povs = [o for o in outcomes if o.get("skeleton_type") == "participant_pov"]
    listener_povs = [o for o in outcomes if o.get("skeleton_type") == "secrecy_listener_pov"]

    # 1. Role Executability
    realized_povs = [o for o in participant_povs if o.get("realized_shapes_count", 0) > 0]
    dead_povs = [o for o in participant_povs if o.get("realized_shapes_count", 0) == 0]
    if not participant_povs or not realized_povs:
        role_executability = "NO_ROLES_EXECUTABLE"
    elif dead_povs:
        role_executability = "PARTIAL_DEAD_ROLES"
    else:
        role_executability = "ALL_ROLES_EXECUTABLE"

    # 2. Authentication Profile
    def _is_strictly_multi_strand(pov: Dict[str, Any]) -> bool:
        max_s = pov.get("max_strands_in_realized_shape", 0)
        min_s = pov.get("min_strands_in_realized_shape", max_s)
        init_s = pov.get("initial_strand_count", 1)
        return bool(pov.get("realized_shapes_count", 0) > 0 and min_s >= 2 and max_s > init_s)

    strictly_multi_count = sum(1 for o in participant_povs if _is_strictly_multi_strand(o))
    any_branched_split = any(
        bool(o.get("has_self_reflection_split"))
        or (
            o.get("min_strands_in_realized_shape", o.get("max_strands_in_realized_shape", 0)) == 1
            and o.get("max_strands_in_realized_shape", 0) >= 2
        )
        for o in participant_povs
    )
    any_multi_shape = any(
        o.get("max_strands_in_realized_shape", 0) >= 2
        and o.get("max_strands_in_realized_shape", 0) > o.get("initial_strand_count", 1)
        for o in participant_povs
    )

    if role_executability == "NO_ROLES_EXECUTABLE":
        auth_profile = "NON_EXECUTABLE"
    elif any_branched_split:
        auth_profile = "CONDITIONAL_BRANCHED_AUTHENTICATION"
    elif participant_povs and strictly_multi_count == len(participant_povs):
        auth_profile = "MUTUAL_MULTI_STRAND"
    elif strictly_multi_count >= 1:
        auth_profile = "UNILATERAL_AUTHENTICATED"
    else:
        auth_profile = "UNAUTHENTICATED_OR_CLEARTEXT_EXECUTABLE"

    # 3. Parameter Agreement / Lowe MITM / Malleable Parameter Detection
    all_disagreements: List[Dict[str, Any]] = []
    for o in participant_povs:
        for dp in o.get("disagreed_parameters") or []:
            if dp not in all_disagreements:
                all_disagreements.append(dp)

    if not any_multi_shape:
        param_agreement_status = "NOT_APPLICABLE_SINGLE_STRAND"
    elif not all_disagreements:
        param_agreement_status = "FULL_PARAMETER_AGREEMENT"
    elif any(d.get("sort") in ("name", "akey") for d in all_disagreements):
        param_agreement_status = "PRINCIPAL_DISAGREEMENT_MITM_OR_UKS"
    else:
        param_agreement_status = "PARAMETER_DISAGREEMENT_DETECTED"

    # 4. Same-Role Reflection
    any_same_role_refl = any(bool(o.get("has_same_role_reflection")) for o in participant_povs)
    reflection_status = "SAME_ROLE_REFLECTION_DETECTED" if any_same_role_refl else "NO_REFLECTION"

    # 5. Secrecy Analysis
    protected_secrets: List[str] = []
    leaked_secrets: List[str] = []
    for l_pov in listener_povs:
        terms = l_pov.get("listener_terms") or (
            [l_pov["listener_term"]]
            if l_pov.get("listener_term")
            else [f"listener_label_{l_pov.get('root_label')}"]
        )
        if l_pov.get("realized_shapes_count", 0) == 0:
            for term in terms:
                if term not in protected_secrets:
                    protected_secrets.append(term)
        else:
            for term in terms:
                if term not in leaked_secrets:
                    leaked_secrets.append(term)

    if not listener_povs:
        secrecy_status = "NOT_APPLICABLE_NO_LISTENER"
    elif protected_secrets and not leaked_secrets:
        secrecy_status = "SECRECY_PROVED"
    elif leaked_secrets and not protected_secrets:
        secrecy_status = "SECRECY_LEAK_DETECTED"
    else:
        secrecy_status = "PARTIAL_SECRECY"

    # 6. Explicit `defgoal` Satisfaction
    goal_verdicts = [o.get("goal_satisfied") for o in outcomes if o.get("goal_satisfied") is not None]
    if not goal_verdicts:
        defgoal_status = "NO_EXPLICIT_DEFGOALS"
    elif all(v == "yes" for v in goal_verdicts):
        defgoal_status = "ALL_SATISFIED"
    else:
        defgoal_status = "COUNTEREXAMPLE_FOUND"

    # 7. Vulnerabilities & Anomalies Summary
    anomalies: List[str] = []
    if leaked_secrets:
        anomalies.append(
            f"SECRECY_LEAK: Listener skeleton(s) realized shape(s) exposing {leaked_secrets}."
        )
    if param_agreement_status == "PRINCIPAL_DISAGREEMENT_MITM_OR_UKS":
        params_str = ", ".join(
            sorted({f"{d['parameter']} ({d['pov_value']} vs {d['peer_value']})" for d in all_disagreements if d.get("sort") in ("name", "akey")})
        )
        anomalies.append(
            f"PRINCIPAL_DISAGREEMENT_MITM: Counterparty strand disagrees on principal/key parameter(s): {params_str}."
        )
    elif param_agreement_status == "PARAMETER_DISAGREEMENT_DETECTED":
        params_str = ", ".join(
            sorted({f"{d['parameter']} ({d['pov_value']} vs {d['peer_value']})" for d in all_disagreements})
        )
        anomalies.append(
            f"PARAMETER_DISAGREEMENT: Counterparty strand disagrees on session/header parameter(s): {params_str}."
        )
    if any_same_role_refl:
        anomalies.append(
            "SAME_ROLE_REFLECTION: At least one realized shape satisfies a role's reception edges using another instance of the same role."
        )
    if any_branched_split:
        anomalies.append(
            "CONDITIONAL_BRANCHED_SHAPES: At least one POV admits both a 1-strand unauthenticated shape and a >=2-strand authenticated shape."
        )

    auth_tests = (exploration_telemetry or {}).get("authentication_tests_summary") or {
        "encryption_tests": 0,
        "nonce_tests": 0,
        "channel_tests": 0,
        "generalizations": 0,
        "collapsed_shapes": 0,
        "added_strands": 0,
        "contractions": 0,
        "displacements": 0,
        "added_listeners": 0,
    }
    sas_list = sas_formulas or []

    return {
        "role_executability": role_executability,
        "dead_roles_count": len(dead_povs),
        "authentication_profile": auth_profile,
        "parameter_agreement_status": param_agreement_status,
        "parameter_disagreements": all_disagreements,
        "role_reflection_status": reflection_status,
        "secrecy_status": secrecy_status,
        "protected_secrets": protected_secrets,
        "leaked_secrets": leaked_secrets,
        "defgoal_satisfaction_status": defgoal_status,
        "authentication_tests_summary": auth_tests,
        "shape_analysis_sentences_count": len(sas_list),
        "shape_analysis_sentences": sas_list,
        "anomalies_count": len(anomalies),
        "vulnerabilities_and_anomalies": anomalies,
    }


def compute_quality_assessment(
    solver_passed: bool,
    shapes_analysis: Dict[str, Any],
    stage5_attempts_count: int,
    stage6_attempts_count: int,
    roletran_passed: bool = True,
    has_cryptographic_primitives: bool = True,
    security_findings: Optional[Dict[str, Any]] = None,
    final_spec: Optional[CPSAProtocolSpecification] = None,
) -> Dict[str, Any]:
    """Computes the deterministic 4-tier translation & modeling quality grade (`GOLD`, `SILVER`, `BRONZE`, `REJECTED`).

    Crucially decoupled from protocol security properties: a faithful, executable CPSA specification
    of an RFC protocol is NEVER penalized in `quality_tier` if the RFC protocol itself is unilateral,
    authentication-only (no `deflistener`), or has a formal vulnerability (secrecy leak, reflection,
    or parameter disagreement) discovered by CPSA. Formal security properties are reported in
    `security_findings`.
    """
    outcomes = shapes_analysis.get("per_preskeleton_outcomes", [])
    participant_povs = [o for o in outcomes if o.get("skeleton_type") == "participant_pov"]
    listener_povs = [o for o in outcomes if o.get("skeleton_type") == "secrecy_listener_pov"]
    sec_report = security_findings or compute_security_findings(shapes_analysis)

    if not solver_passed or not outcomes:
        return {
            "quality_tier": "REJECTED",
            "all_participant_povs_realized": False,
            "all_participant_povs_multi_strand": False,
            "all_secrecy_listeners_unrealized": False,
            "security_findings": sec_report,
            "post_training_routing": {
                "eligible_for_sft_positive": False,
                "dpo_contrastive_pairs_available": 0,
                "compiler_repair_trajectories_available": stage5_attempts_count + stage6_attempts_count,
            },
        }

    all_povs_realized = bool(participant_povs) and all(
        o.get("realized_shapes_count", 0) > 0 for o in participant_povs
    )

    # Detect malformed pre-seeded multi-strand root skeletons where CPSA added 0 partner strands
    any_preseeded_no_progress = any(
        o.get("initial_strand_count", 1) >= 2
        and o.get("max_strands_in_realized_shape", 0) <= o.get("initial_strand_count", 1)
        for o in participant_povs
    )

    def _has_causal_partner_strand(pov: Dict[str, Any]) -> bool:
        max_s = pov.get("max_strands_in_realized_shape", 0)
        init_s = pov.get("initial_strand_count", 1)
        return bool(pov.get("realized_shapes_count", 0) > 0 and max_s >= 2 and max_s > init_s)

    causal_multi_pov_count = sum(1 for o in participant_povs if _has_causal_partner_strand(o))
    all_povs_multi_strand = all_povs_realized and (
        sum(
            1
            for o in participant_povs
            if o.get("min_strands_in_realized_shape", 0) >= 2
            and o.get("max_strands_in_realized_shape", 0) > o.get("initial_strand_count", 1)
        )
        == len(participant_povs)
    )
    all_listeners_unrealized = bool(listener_povs) and all(
        o.get("realized_shapes_count", 0) == 0 for o in listener_povs
    )

    # Detect truncated initiator trace where responder sends a reply that no role ever receives (e.g. RFC 3971)
    has_dangling_response_flight = False
    if final_spec and len(final_spec.roles) >= 2:
        total_sends = sum(1 for r in final_spec.roles for ev in r.trace if ev.direction == "send")
        total_recvs = sum(1 for r in final_spec.roles for ev in r.trace if ev.direction == "recv")
        has_send_only_role = any(
            len(r.trace) == 1 and r.trace[0].direction == "send" for r in final_spec.roles
        )
        has_recv_and_send_role = any(
            any(ev.direction == "recv" for ev in r.trace) and any(ev.direction == "send" for ev in r.trace)
            for r in final_spec.roles
        )
        any_trivial_pov = any(bool(o.get("is_trivial_single_strand_shape")) for o in participant_povs)
        if has_send_only_role and has_recv_and_send_role and total_sends > total_recvs and any_trivial_pov:
            has_dangling_response_flight = True
            anomaly_msg = (
                "INCOMPLETE_INITIATOR_TRACE: Responder sends a reply flight that no role receives, "
                "leaving the initiator POV as a 1-strand trivial shape."
            )
            if anomaly_msg not in sec_report.get("vulnerabilities_and_anomalies", []):
                sec_report.setdefault("vulnerabilities_and_anomalies", []).append(anomaly_msg)
                sec_report["anomalies_count"] = len(sec_report["vulnerabilities_and_anomalies"])

    if not all_povs_realized or not has_cryptographic_primitives or any_preseeded_no_progress:
        tier = "BRONZE"
    elif roletran_passed and causal_multi_pov_count >= 1 and not has_dangling_response_flight:
        tier = "GOLD"
    else:
        tier = "SILVER"

    total_repairs = stage5_attempts_count + stage6_attempts_count
    return {
        "quality_tier": tier,
        "all_participant_povs_realized": all_povs_realized,
        "all_participant_povs_multi_strand": all_povs_multi_strand,
        "all_secrecy_listeners_unrealized": all_listeners_unrealized,
        "security_findings": sec_report,
        "post_training_routing": {
            "eligible_for_sft_positive": tier in ("GOLD", "SILVER"),
            "dpo_contrastive_pairs_available": total_repairs if tier in ("GOLD", "SILVER") else 0,
            "compiler_repair_trajectories_available": total_repairs,
        },
    }


def build_scm_metadata_header(
    rfc_id: str,
    protocol_name: str,
    selected_sections: List[str],
    algebra: str,
    roles: List[str],
    quality_tier: str,
    realized_shapes: int,
    secrecy_proved: bool,
    auth_profile: Optional[str] = None,
    secrecy_status: Optional[str] = None,
) -> str:
    """Formats the structured Scheme comment header for MoE router conditioning."""
    sections_str = ", ".join(selected_sections) if selected_sections else "all"
    roles_str = ", ".join(roles) if roles else "none"
    effective_secrecy = secrecy_status or ("PROVED" if secrecy_proved else "UNVERIFIED")
    auth_suffix = f" | AUTH-PROFILE: {auth_profile}" if auth_profile else ""
    lines = [
        f";;; [RFC-ID: {rfc_id}]",
        f";;; [PROTOCOL: {protocol_name}]",
        f";;; [SECTIONS: {sections_str}]",
        f";;; [ALGEBRA: {algebra}]",
        f";;; [ROLES: {roles_str}]",
        f";;; [QUALITY-TIER: {quality_tier} | REALIZED-SHAPES: {realized_shapes} | SECRECY: {effective_secrecy}{auth_suffix}]",
        "",
    ]
    return "\n".join(lines)


def write_trajectory_metadata_bundle(
    output_dir: Path,
    rfc_id: str,
    rfc_title: str,
    protocol_name: str,
    participating_principals: List[str],
    selected_sections: List[str],
    verbatim_slice: str,
    duration_seconds: float,
    stage2_record: Dict[str, Any],
    stage5_record: Dict[str, Any],
    stage6_record: Dict[str, Any],
    final_spec: Optional[CPSAProtocolSpecification],
    final_scm_path: Optional[Path],
    trace_txt_path: Optional[Path],
    shapes_txt_path: Optional[Path],
    solver_passed: bool,
    intake_rationale: Optional[str] = None,
) -> Path:
    """Computes programmatic CPSA verification metrics, prepends `.scm` metadata headers,
    and writes `<protocol_stem>_trajectory.json` into `output_dir`.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    compact_ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    shapes_analysis = analyze_shapes_txt(shapes_txt_path)
    dead_root_labels = [
        o["root_label"]
        for o in shapes_analysis.get("per_preskeleton_outcomes", [])
        if o.get("skeleton_type") == "participant_pov"
        and o.get("realized_shapes_count", 0) == 0
        and o.get("root_label") is not None
    ]
    exploration_telemetry = analyze_exploration_txt(trace_txt_path, dead_root_labels=dead_root_labels)
    sas_formulas = extract_shape_analysis_sentences(trace_txt_path) if solver_passed else []
    security_findings = compute_security_findings(
        shapes_analysis=shapes_analysis,
        exploration_telemetry=exploration_telemetry,
        sas_formulas=sas_formulas,
    )

    stage5_attempts = stage5_record.get("repair_attempts", [])
    stage6_attempts = stage6_record.get("repair_attempts", [])
    roletran_passed = bool(stage5_record.get("final_passed", True))
    has_crypto = final_spec.has_cryptographic_primitives() if final_spec else True
    quality_assessment = compute_quality_assessment(
        solver_passed=solver_passed,
        shapes_analysis=shapes_analysis,
        stage5_attempts_count=len(stage5_attempts),
        stage6_attempts_count=len(stage6_attempts),
        roletran_passed=roletran_passed,
        has_cryptographic_primitives=has_crypto,
        security_findings=security_findings,
        final_spec=final_spec,
    )

    stage6_full = {
        **stage6_record,
        "exploration_telemetry_from_txt": exploration_telemetry,
        "shapes_analysis_from_shapes_txt": shapes_analysis,
    }

    final_scm_with_header = ""
    algebra_str = final_spec.message_algebra if final_spec else "basic"
    role_names = [r.role_name for r in final_spec.roles] if final_spec else []

    if final_scm_path and final_scm_path.exists():
        raw_scm = final_scm_path.read_text(encoding="utf-8", errors="replace")
        # Strip any previously prepended metadata header lines before writing fresh header
        cleaned_lines = [
            line for line in raw_scm.splitlines() if not line.startswith(";;; [")
        ]
        clean_scm_body = "\n".join(cleaned_lines).lstrip("\n") + "\n"
        header = build_scm_metadata_header(
            rfc_id=rfc_id,
            protocol_name=final_spec.protocol_name if final_spec else protocol_name,
            selected_sections=selected_sections,
            algebra=algebra_str,
            roles=role_names,
            quality_tier=quality_assessment["quality_tier"],
            realized_shapes=shapes_analysis["total_realized_shapes"],
            secrecy_proved=quality_assessment["all_secrecy_listeners_unrealized"],
            auth_profile=security_findings.get("authentication_profile"),
            secrecy_status=security_findings.get("secrecy_status"),
        )
        final_scm_with_header = header + clean_scm_body
        final_scm_path.write_text(final_scm_with_header, encoding="utf-8")

    distilled_shapes_content = None
    if shapes_txt_path and shapes_txt_path.exists():
        distilled_shapes_content = shapes_txt_path.read_text(encoding="utf-8", errors="replace")

    raw_stem = (
        final_scm_path.stem
        if final_scm_path
        else (final_spec.protocol_name if final_spec else rfc_id)
    )
    stem = re.sub(r"[^a-z0-9_-]+", "_", (raw_stem or rfc_id).lower()).strip("_") or "protocol"
    trajectory_path = output_dir / f"{stem}_trajectory.json"

    from src.cost_tracker import GLOBAL_COST_TRACKER
    rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()

    payload: Dict[str, Any] = {
        "schema_version": "1.1.0",
        "run_id": f"{rfc_id.lower()}_{compact_ts}",
        "timestamp_utc": now_utc,
        "duration_seconds": round(duration_seconds, 2),
        "cost_telemetry": rfc_cost_summary,
        "rfc_metadata": {
            "rfc_id": rfc_id,
            "rfc_title": rfc_title,
            "protocol_name": final_spec.protocol_name if final_spec else protocol_name,
            "algebra": algebra_str,
            "participating_principals": participating_principals,
            "selected_sections": selected_sections,
            "sliced_lines_count": len(verbatim_slice.splitlines()),
            "verbatim_rfc_slice": verbatim_slice,
            "intake_rationale": intake_rationale,
        },
        "stage2_initial_extraction": stage2_record,
        "stage5_preflight_gate": stage5_record,
        "stage6_cpsa4_solver": stage6_full,
        "quality_assessment": quality_assessment,
        "security_findings": security_findings,
        "final_verified_output": {
            "final_ast": final_spec.model_dump() if final_spec else None,
            "final_scm_with_header": final_scm_with_header or None,
            "distilled_shapes_txt": distilled_shapes_content,
        },
    }

    with open(trajectory_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    logger.info(
        "Wrote trajectory metadata (%s, auth=%s, secrecy=%s, shapes=%d) to %s",
        quality_assessment["quality_tier"],
        security_findings["authentication_profile"],
        security_findings["secrecy_status"],
        shapes_analysis["total_realized_shapes"],
        trajectory_path,
    )
    return trajectory_path


def update_run_metadata_index(
    run_root_dir: Path,
    rfc_id: str,
    protocol_name: Optional[str],
    rfc_dir: Path,
    scm_path: Optional[Path],
    trajectory_json_path: Optional[Path],
    quality_tier: Optional[str],
    is_eligible: bool,
    build_successful: bool,
    error_message: Optional[str] = None,
    tab_index: Optional[int] = None,
    rejection_gate: Optional[str] = None,
    duration_seconds: float = 0.0,
    security_findings: Optional[Dict[str, Any]] = None,
    intake_rationale: Optional[str] = None,
) -> Path:
    """Updates the master `metadata_index.json` in the timestamped run directory
    with the locations of all generated RFC directories and JSON metadata files.
    """
    run_root_dir.mkdir(parents=True, exist_ok=True)
    index_path = run_root_dir / "metadata_index.json"

    if index_path.exists():
        try:
            index_data = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception:
            index_data = {}
    else:
        index_data = {}

    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not index_data:
        index_data = {
            "schema_version": "1.0.0",
            "run_directory": str(run_root_dir.resolve()),
            "created_at_utc": now_utc,
            "updated_at_utc": now_utc,
            "total_rfcs_processed": 0,
            "total_ineligible_filtered": 0,
            "total_eligible_protocols": 0,
            "metadata_json_files": [],
            "rfc_directories": [],
            "runs": [],
            "filtered_rfcs": [],
        }

    from src.cost_tracker import GLOBAL_COST_TRACKER
    rfc_cost = GLOBAL_COST_TRACKER.get_current_rfc_summary()
    batch_cost = GLOBAL_COST_TRACKER.get_batch_summary()

    index_data["updated_at_utc"] = now_utc
    index_data["total_rfcs_processed"] = int(index_data.get("total_rfcs_processed", 0)) + 1
    index_data["batch_cost_telemetry"] = batch_cost
    index_data.setdefault("filtered_rfcs", [])

    if not is_eligible:
        index_data["total_ineligible_filtered"] = int(index_data.get("total_ineligible_filtered", 0)) + 1
        index_data["filtered_rfcs"].append({
            "rfc_id": rfc_id,
            "title": protocol_name or rfc_id,
            "gate": rejection_gate or "Intake Gate",
            "reason": error_message or "Ineligible",
            "duration_seconds": round(float(duration_seconds), 2),
            "cost_usd": round(float(rfc_cost.get("total_cost_usd", 0.0)), 6),
        })
        with open(index_path, "w", encoding="utf-8") as handle:
            json.dump(index_data, handle, indent=2)
        return index_path

    index_data["total_eligible_protocols"] = int(index_data.get("total_eligible_protocols", 0)) + 1
    rfc_dir_str = str(rfc_dir.resolve())
    if rfc_dir_str not in index_data["rfc_directories"]:
        index_data["rfc_directories"].append(rfc_dir_str)

    if trajectory_json_path and trajectory_json_path.exists():
        traj_str = str(trajectory_json_path.resolve())
        if traj_str not in index_data["metadata_json_files"]:
            index_data["metadata_json_files"].append(traj_str)
    else:
        traj_str = None

    scm_str = str(scm_path.resolve()) if (scm_path and scm_path.exists()) else None
    effective_tab_idx = tab_index if tab_index is not None else (len(index_data.get("runs", [])) + 1)

    index_data["runs"].append({
        "tab_index": effective_tab_idx,
        "rfc_id": rfc_id,
        "protocol_name": protocol_name,
        "is_eligible": is_eligible,
        "build_successful": build_successful,
        "quality_tier": quality_tier or ("REJECTED" if is_eligible else "INELIGIBLE"),
        "rfc_directory": rfc_dir_str,
        "scm_file": scm_str,
        "metadata_json_file": traj_str,
        "error_message": error_message,
        "intake_rationale": intake_rationale,
        "security_findings": security_findings,
        "cost_usd": round(float(rfc_cost.get("total_cost_usd", 0.0)), 6),
        "cost_telemetry": rfc_cost,
    })

    with open(index_path, "w", encoding="utf-8") as handle:
        json.dump(index_data, handle, indent=2)

    return index_path
```

---

### `src/visualizer/__init__.py`

*sha256:`b5ef0fe4ac5a` · 1 lines · 0.1 KB (~16 tokens) · lang:`python`*

```python
"""RFC-LLM Live Visualization and Interactive Dashboard Module."""
```

---

### `src/visualizer/server.py`

*sha256:`8aafb7c40a7f` · 733 lines · 31.7 KB (~8,125 tokens) · lang:`python`*

```python
"""Asynchronous web server for live and offline multi-RFC synthesis visualization."""

import asyncio
import csv
import json
import logging
import socket
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from aiohttp import web

from src.logging_config import PipelineMetricsCSVLogger
from src.pipeline_events import GLOBAL_EVENT_BUS, PipelineEvent
from src.system_config import SYSTEM_CONFIG
from src.verification_engine.trajectory_metadata_exporter import compute_security_findings

logger = logging.getLogger("rfc_llm.visualizer")

HTML_TEMPLATE_PATH = Path(__file__).parent / "static" / "index.html"

# Lazy lightweight chunk-id -> {title, source_file, snippet} lookup cache for offline hydration
_MANUAL_CHUNK_LOOKUP: Optional[Dict[str, Dict[str, str]]] = None


def _get_manual_chunk_lookup() -> Dict[str, Dict[str, str]]:
    """Loads compact section/example metadata from `refrences/cpsa_kb/kb_index.json`
    (plus legacy `manual_chunks.jsonl` if present) for offline RAG card hydration.
    """
    global _MANUAL_CHUNK_LOOKUP
    if _MANUAL_CHUNK_LOOKUP is not None:
        return _MANUAL_CHUNK_LOOKUP

    lookup: Dict[str, Dict[str, str]] = {}
    kb_index_path = SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "cpsa_kb" / "kb_index.json"
    if kb_index_path.exists():
        try:
            kb_data = json.loads(kb_index_path.read_text(encoding="utf-8", errors="ignore"))
            for sec in kb_data.get("sections", []):
                sid = str(sec.get("section_id") or "")
                if sid:
                    txt = sec.get("content") or ""
                    lookup[sid] = {
                        "chunk_id": sid,
                        "title": sec.get("title") or sid,
                        "source_file": sec.get("source_file") or "CPSA Knowledge Base",
                        "snippet": txt[:280].strip() + ("..." if len(txt) > 280 else ""),
                    }
            for ex in kb_data.get("scm_examples", []):
                ex_id = str(ex.get("example_id") or "")
                if ex_id:
                    lookup[ex_id] = {
                        "chunk_id": ex_id,
                        "title": f"MITRE Example: {ex.get('filename')} ({ex.get('algebra', 'basic')})",
                        "source_file": ex_id,
                        "snippet": ex.get("summary") or "",
                    }
        except Exception:
            pass

    jsonl_path = SYSTEM_CONFIG.CHUNKS_DIR / "manual_chunks.jsonl"
    if jsonl_path.exists():
        try:
            with open(jsonl_path, "r", encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    cid = str(obj.get("chunk_id") or obj.get("id") or "")
                    if cid and cid not in lookup:
                        txt = obj.get("text") or obj.get("content") or ""
                        lookup[cid] = {
                            "chunk_id": cid,
                            "title": obj.get("title") or obj.get("breadcrumb") or f"Chunk #{cid}",
                            "source_file": obj.get("source_file") or "MITRE Manual",
                            "snippet": txt[:280].strip() + ("..." if len(txt) > 280 else ""),
                        }
        except Exception:
            pass
    _MANUAL_CHUNK_LOOKUP = lookup
    return lookup


def _resolve_chunks_by_ids(chunk_ids: List[Any]) -> List[Dict[str, str]]:
    lookup = _get_manual_chunk_lookup()
    resolved = []
    for raw_id in chunk_ids or []:
        cid = str(raw_id)
        if cid in lookup:
            resolved.append(lookup[cid])
        else:
            resolved.append({
                "chunk_id": cid,
                "title": f"MITRE CPSA Manual Chunk #{cid}",
                "source_file": "manual_chunks.jsonl",
                "snippet": "",
            })
    return resolved


def hydrate_tab_payload(tab_summary: Dict[str, Any]) -> Dict[str, Any]:
    """Hydrates a single numbered RFC tab on demand from disk (<rfc_dir>/events.jsonl + <stem>_trajectory.json)."""
    rfc_dir = Path(tab_summary["rfc_dir"]) if tab_summary.get("rfc_dir") else None
    traj_path = Path(tab_summary["trajectory_path"]) if tab_summary.get("trajectory_path") else None
    if (not traj_path or not traj_path.exists()) and rfc_dir and rfc_dir.exists():
        candidates = sorted(rfc_dir.glob("*_trajectory.json"))
        if candidates:
            traj_path = candidates[0]

    traj: Dict[str, Any] = {}
    if traj_path and traj_path.exists():
        try:
            traj = json.loads(traj_path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            traj = {}

    meta = traj.get("rfc_metadata", {})
    s2 = traj.get("stage2_initial_extraction", {})
    s5 = traj.get("stage5_preflight_gate", {})
    s6 = traj.get("stage6_cpsa4_solver", {})
    qa = traj.get("quality_assessment", {})
    final_out = traj.get("final_verified_output", {})

    # 1. Verbatim RFC Slice
    verbatim_slice = meta.get("verbatim_rfc_slice") or ""
    if not verbatim_slice and rfc_dir and (rfc_dir / "verbatim_slice.txt").exists():
        verbatim_slice = (rfc_dir / "verbatim_slice.txt").read_text(encoding="utf-8", errors="ignore")

    # Load Chronological Events early so we can reconstruct in-flight attempts for RUNNING tabs
    events: List[Dict[str, Any]] = []
    events_jsonl_path = (
        Path(tab_summary["events_jsonl"])
        if tab_summary.get("events_jsonl")
        else (rfc_dir / "events.jsonl" if rfc_dir else None)
    )
    if events_jsonl_path and events_jsonl_path.exists():
        try:
            with open(events_jsonl_path, "r", encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    line = line.strip()
                    if line:
                        events.append(json.loads(line))
        except Exception:
            events = []

    active_state = GLOBAL_EVENT_BUS.get_active_state()
    if active_state.get("tab_index") == tab_summary.get("tab_index") and active_state.get("events"):
        if not events:
            events = active_state["events"]

    # 2. Build Ordered Per-Attempt Time-Travel Snapshots
    attempts: List[Dict[str, Any]] = []
    s5_repairs = s5.get("repair_attempts") or []
    s6_repairs = s6.get("repair_attempts") or []

    initial_ast = s2.get("initial_ast")
    initial_scm = s2.get("initial_scm")
    if not initial_scm and s5_repairs:
        initial_scm = s5_repairs[0].get("rejected_scm")
    if not initial_scm and s6_repairs:
        initial_scm = s6_repairs[0].get("rejected_scm")

    # If trajectory.json is not written yet (e.g. tab is RUNNING), recover latest AST/.scm from live events
    is_running_tab = (tab_summary.get("status") == "RUNNING") and not traj
    if not initial_ast and events:
        for evt in events:
            if evt.get("event_type") == "stage_completed" and evt.get("stage") == 2:
                initial_ast = (evt.get("data") or {}).get("ast")
                break
    if not initial_scm and tab_summary.get("scm_path") and Path(tab_summary["scm_path"]).exists():
        initial_scm = Path(tab_summary["scm_path"]).read_text(encoding="utf-8", errors="ignore")

    # Determine whether Attempt 0 passed directly or what diagnostic rejected it
    attempt0_diag: Optional[str] = None
    if s5_repairs:
        attempt0_diag = s5_repairs[0].get("parsed_diagnostic") or s5_repairs[0].get("raw_stderr")
        attempt0_status = "REJECTED"
    elif s6_repairs:
        attempt0_diag = s6_repairs[0].get("parsed_diagnostic") or s6_repairs[0].get("raw_stderr")
        attempt0_status = "REJECTED"
    elif s2.get("schema_validation_error") and not initial_ast:
        attempt0_diag = s2.get("schema_validation_error")
        attempt0_status = "FAILED"
    elif s6.get("final_passed"):
        attempt0_status = "PASSED"
    elif initial_ast or initial_scm:
        attempt0_diag = tab_summary.get("error_message")
        attempt0_status = "GENERATED"
    elif is_running_tab:
        attempt0_diag = "Stage 2 JSON CPSA synthesis currently in progress..."
        attempt0_status = "GENERATED"
    else:
        attempt0_diag = tab_summary.get("error_message") or "Initial JSON extraction did not complete."
        attempt0_status = "FAILED"

    attempts.append({
        "attempt_number": 0,
        "attempt_id": "attempt_0",
        "label": "Attempt 0 | Initial",
        "stage": "Stage 2/3: Initial JSON & .scm Synthesis",
        "status": attempt0_status,
        "cycle_detected": False,
        "scm": initial_scm or "; Synthesizing initial .scm model...",
        "ast": initial_ast,
        "diagnostic": attempt0_diag,
        "rag_query": None,
        "retrieved_chunks": [],
    })

    seq_num = 0
    for idx, rep in enumerate(s5_repairs):
        seq_num += 1
        # Diagnostic that this repair produced on the NEXT check (if another repair followed)
        next_diag = None
        if not rep.get("passed_after_repair"):
            if idx + 1 < len(s5_repairs):
                next_diag = s5_repairs[idx + 1].get("parsed_diagnostic")
            elif rep.get("repair_exception"):
                next_diag = rep.get("repair_exception")
        attempts.append({
            "attempt_number": seq_num,
            "attempt_id": f"roletran_{rep.get('attempt_number', idx + 1)}",
            "label": f"Attempt {seq_num} | Roletran Repair",
            "stage": f"Stage 5: Roletran Self-Healing (#{rep.get('attempt_number', idx + 1)})",
            "status": "PASSED" if rep.get("passed_after_repair") else "REJECTED",
            "cycle_detected": bool(rep.get("cycle_detected", False)),
            "scm": rep.get("repaired_scm") or rep.get("rejected_scm") or "; Repair failed to emit .scm",
            "rejected_scm": rep.get("rejected_scm"),
            "ast": rep.get("repaired_ast") or rep.get("rejected_ast"),
            "trigger_diagnostic": rep.get("parsed_diagnostic") or rep.get("raw_stderr"),
            "diagnostic": rep.get("parsed_diagnostic") or rep.get("repair_exception") or next_diag,
            "rag_query": rep.get("rag_query"),
            "searcher_diagnosis": rep.get("searcher_diagnosis"),
            "searcher_turns": rep.get("searcher_turns") or [],
            "retrieved_chunks": _resolve_chunks_by_ids(rep.get("retrieved_chunk_ids", [])),
        })

    for idx, rep in enumerate(s6_repairs):
        seq_num += 1
        attempts.append({
            "attempt_number": seq_num,
            "attempt_id": f"solver_{rep.get('attempt_number', idx + 1)}",
            "label": f"Attempt {seq_num} | CPSA Repair",
            "stage": f"Stage 6: CPSA Compilation Self-Healing (#{rep.get('attempt_number', idx + 1)})",
            "status": "PASSED" if rep.get("passed_after_repair") else "REJECTED",
            "cycle_detected": bool(rep.get("cycle_detected", False)),
            "scm": rep.get("repaired_scm") or rep.get("rejected_scm") or "; Repair failed to emit .scm",
            "rejected_scm": rep.get("rejected_scm"),
            "ast": rep.get("repaired_ast") or rep.get("rejected_ast"),
            "trigger_diagnostic": rep.get("parsed_diagnostic") or rep.get("raw_stderr"),
            "diagnostic": rep.get("parsed_diagnostic") or rep.get("repair_exception") or rep.get("raw_stderr"),
            "rag_query": rep.get("rag_query"),
            "searcher_diagnosis": rep.get("searcher_diagnosis"),
            "searcher_turns": rep.get("searcher_turns") or [],
            "retrieved_chunks": _resolve_chunks_by_ids(rep.get("retrieved_chunk_ids", [])),
        })

    # Reconstruct in-progress repair attempts from live events if trajectory.json is not finalized yet
    if is_running_tab and events:
        latest_ast = initial_ast
        for evt in events:
            et = evt.get("event_type")
            ed = evt.get("data") or {}
            if et == "stage_completed" and evt.get("stage") == 3 and ed.get("ast"):
                latest_ast = ed.get("ast")
            elif et == "repair_attempt":
                seq_num += 1
                stg = evt.get("stage", 5)
                att_n = ed.get("attempt", seq_num)
                attempts.append({
                    "attempt_number": seq_num,
                    "attempt_id": f"live_repair_{seq_num}",
                    "label": f"Attempt {seq_num} | {'Roletran' if stg == 5 else 'CPSA'} Repair",
                    "stage": f"Stage {stg}: Live Self-Healing (#{att_n})",
                    "status": "GENERATED",
                    "cycle_detected": bool(ed.get("cycle_detected", False)),
                    "scm": initial_scm or "; Repair in progress...",
                    "ast": latest_ast,
                    "diagnostic": ed.get("diagnostic"),
                    "rag_query": None,
                    "retrieved_chunks": [],
                })

    final_scm = final_out.get("final_scm_with_header")
    final_ast = final_out.get("final_ast")
    if not is_running_tab and not final_scm and tab_summary.get("scm_path") and Path(tab_summary["scm_path"]).exists():
        final_scm = Path(tab_summary["scm_path"]).read_text(encoding="utf-8", errors="ignore")

    if not is_running_tab and (final_scm or final_ast):
        tier = qa.get("quality_tier") or tab_summary.get("quality_tier") or "REJECTED"
        shapes_n = int(
            s6.get("shapes_analysis_from_shapes_txt", {}).get(
                "total_realized_shapes", tab_summary.get("shapes_count", 0)
            )
        )
        solver_ok = bool(s6.get("final_passed") or tab_summary.get("status") == "VERIFIED")
        final_label = f"Final | {tier} ({shapes_n} Shapes)" if solver_ok else f"Final | {tier}"
        attempts.append({
            "attempt_number": seq_num + 1,
            "attempt_id": "final",
            "label": final_label,
            "stage": "Final Synthesized Artifact",
            "status": "VERIFIED" if solver_ok else "FAILED",
            "cycle_detected": False,
            "scm": final_scm or "; No final .scm file.",
            "ast": final_ast,
            "diagnostic": None if solver_ok else tab_summary.get("error_message"),
            "rag_query": None,
            "retrieved_chunks": [],
        })

    if not events:
        events = _synthesize_events_from_trajectory(tab_summary, traj, attempts)

    shapes_xhtml = tab_summary.get("shapes_xhtml")
    if not shapes_xhtml and rfc_dir and rfc_dir.exists():
        xhtmls = sorted(rfc_dir.glob("*_shapes.xhtml"))
        if xhtmls:
            shapes_xhtml = str(xhtmls[0])

    cost_telemetry = traj.get("cost_telemetry") or tab_summary.get("cost_telemetry") or {}
    if not cost_telemetry and events:
        for evt in reversed(events):
            if evt.get("event_type") == "cost_updated":
                rc = (evt.get("data") or {}).get("rfc_cost")
                if isinstance(rc, dict):
                    cost_telemetry = rc
                    break

    sec_findings = (
        traj.get("security_findings")
        or qa.get("security_findings")
        or tab_summary.get("security_findings")
        or {}
    )
    if not sec_findings and traj:
        try:
            sec_findings = compute_security_findings(
                shapes_analysis=s6.get("shapes_analysis_from_shapes_txt") or {},
                exploration_telemetry=s6.get("exploration_telemetry_from_txt") or {},
                sas_formulas=final_out.get("shape_analysis_sentences") or [],
            )
        except Exception:
            sec_findings = {}

    intake_rationale = (
        meta.get("intake_rationale")
        or tab_summary.get("intake_rationale")
        or None
    )
    if not intake_rationale:
        err_msg = tab_summary.get("error_message") or ""
        if "Eligible:" in err_msg:
            intake_rationale = err_msg.split("Eligible:", 1)[1].strip()

    return {
        "tab": {
            **tab_summary,
            "shapes_xhtml": shapes_xhtml,
            "security_findings": sec_findings,
            "intake_rationale": intake_rationale,
        },
        "rfc_metadata": meta,
        "intake_rationale": intake_rationale,
        "quality_assessment": qa,
        "security_findings": sec_findings,
        "shapes_analysis": s6.get("shapes_analysis_from_shapes_txt") or {},
        "exploration_telemetry": s6.get("exploration_telemetry_from_txt") or {},
        "cost_telemetry": cost_telemetry,
        "verbatim_slice": verbatim_slice,
        "shapes_xhtml": shapes_xhtml,
        "attempts": attempts,
        "events": events,
    }


def _synthesize_events_from_trajectory(
    tab_summary: Dict[str, Any],
    traj: Dict[str, Any],
    attempts: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Synthesizes clean replay events and RAG cards for legacy runs created prior to events.jsonl."""
    base_ts = time.time()
    evts: List[Dict[str, Any]] = []
    meta = traj.get("rfc_metadata", {})
    s2 = traj.get("stage2_initial_extraction", {})
    s5 = traj.get("stage5_preflight_gate", {})
    s6 = traj.get("stage6_cpsa4_solver", {})
    tab_idx = tab_summary.get("tab_index")
    rfc_id = tab_summary.get("rfc_id")

    def _push(offset: float, etype: str, stage: Optional[int], data: Dict[str, Any]):
        evts.append({
            "timestamp": base_ts + offset,
            "event_type": etype,
            "stage": stage,
            "stage_name": None,
            "rfc_id": rfc_id,
            "tab_index": tab_idx,
            "data": data,
        })

    _push(0.0, "pipeline_started", 1, {"rfc_id": rfc_id, "rfc_file": rfc_id})
    _push(0.1, "stage_completed", 1, {"protocol_name": tab_summary.get("protocol_name")})
    if meta.get("selected_sections"):
        _push(0.2, "slice_ready", 1, {
            "sections": meta.get("selected_sections", []),
            "line_count": meta.get("sliced_lines_count", 0),
        })

    if s2.get("initial_ast"):
        _push(0.3, "stage_completed", 2, {
            "roles_count": len(s2["initial_ast"].get("roles", [])),
            "skeletons_count": len(s2["initial_ast"].get("skeletons", [])),
        })
        _push(0.4, "stage_completed", 3, {"scm_path": tab_summary.get("scm_path")})
    else:
        err = s2.get("schema_validation_error") or tab_summary.get("error_message") or "Extraction failed"
        _push(0.3, "stage_failed", 2, {"error_message": err})
        _push(0.4, "pipeline_failed", 2, {"error_message": err})
        return evts

    t_off = 0.5
    for att in attempts:
        if att["attempt_id"] in ("attempt_0", "final"):
            continue
        is_roletran = att["attempt_id"].startswith("roletran_")
        st_num = 5 if is_roletran else 6
        if att.get("rag_query") or att.get("retrieved_chunks") or att.get("searcher_turns"):
            _push(t_off, "rag_retrieval", st_num, {
                "purpose": att["stage"],
                "query": att.get("rag_query") or "",
                "searcher_diagnosis": att.get("searcher_diagnosis"),
                "searcher_turns": att.get("searcher_turns") or [],
                "chunks": att.get("retrieved_chunks") or [],
            })
            t_off += 0.05
        _push(t_off, "repair_attempt", st_num, {
            "attempt": att["attempt_number"],
            "max_attempts": SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS,
            "diagnostic": att.get("diagnostic") or "",
            "cycle_detected": att.get("cycle_detected", False),
        })
        t_off += 0.05

    if s5.get("final_passed"):
        _push(t_off, "stage_completed", 4, {"status": "passed"})
        _push(t_off + 0.02, "stage_completed", 5, {"status": "passed", "attempts": s5.get("total_attempts", 0)})
    else:
        _push(t_off, "stage_failed", 5, {"reason": "Roletran executability unfulfilled"})

    if s6.get("final_passed") or tab_summary.get("status") == "VERIFIED":
        _push(t_off + 0.1, "pipeline_completed", 6, {
            "success": True,
            "protocol_name": tab_summary.get("protocol_name"),
            "shapes_count": tab_summary.get("shapes_count", 0),
            "quality_tier": tab_summary.get("quality_tier"),
            "shapes_xhtml": tab_summary.get("shapes_xhtml"),
        })
    else:
        _push(t_off + 0.1, "stage_failed", 6, {"error_message": tab_summary.get("error_message")})
        _push(t_off + 0.12, "pipeline_failed", 6, {"error_message": tab_summary.get("error_message")})

    return evts


def _load_csv_analytics_payload() -> Dict[str, Any]:
    """Reads and normalizes the active run's 67-column pipeline_runs.csv off the main thread.
    If viewing a legacy run directory that only has metadata_index.json (no pipeline_runs.csv yet),
    reconstructs the 67-column rows from metadata_index.json + trajectory JSONs.
    """
    headers = list(PipelineMetricsCSVLogger.CSV_HEADER)
    csv_path = GLOBAL_EVENT_BUS.get_csv_path()
    run_dir = GLOBAL_EVENT_BUS.get_run_root_dir()

    target_csv: Optional[Path] = None
    if csv_path and csv_path.exists() and csv_path.stat().st_size > 0:
        target_csv = csv_path
    elif run_dir and (run_dir / "pipeline_runs.csv").exists() and (run_dir / "pipeline_runs.csv").stat().st_size > 0:
        target_csv = run_dir / "pipeline_runs.csv"

    rows: List[Dict[str, str]] = []
    if target_csv and target_csv.exists():
        try:
            with open(target_csv, mode="r", newline="", encoding="utf-8", errors="ignore") as handle:
                reader = csv.DictReader(handle)
                for raw_row in reader:
                    normalized = {col: str(raw_row.get(col) or "") for col in headers}
                    rows.append(normalized)
        except Exception:
            rows = []

    # If CSV has 0 rows (e.g., offline --view on a legacy run folder with metadata_index.json),
    # reconstruct rows from metadata_index.json into run_dir/pipeline_runs.csv
    if not rows and run_dir and (run_dir / "metadata_index.json").exists():
        try:
            generated_csv = run_dir / "pipeline_runs.csv"
            temp_logger = PipelineMetricsCSVLogger(csv_path=generated_csv)
            temp_logger.seed_from_source(run_dir / "metadata_index.json")
            target_csv = generated_csv
            with open(generated_csv, mode="r", newline="", encoding="utf-8", errors="ignore") as handle:
                reader = csv.DictReader(handle)
                for raw_row in reader:
                    normalized = {col: str(raw_row.get(col) or "") for col in headers}
                    rows.append(normalized)
        except Exception:
            rows = []

    return {
        "csv_path": str(target_csv or csv_path or ""),
        "headers": headers,
        "row_count": len(rows),
        "rows": rows,
    }


class VisualizerServer:
    """Manages SSE streaming, lazy per-tab hydration, and dashboard state."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self._sse_clients: Set[asyncio.Queue] = set()
        self._setup_routes()

        # Connect event bus to SSE clients
        GLOBAL_EVENT_BUS.subscribe(self._on_bus_event)

    def _setup_routes(self):
        self.app.router.add_get("/", self.handle_index)
        self.app.router.add_get("/api/events", self.handle_sse)
        self.app.router.add_get("/api/history", self.handle_history)
        self.app.router.add_get("/api/tabs", self.handle_tabs)
        self.app.router.add_get("/api/active", self.handle_active)
        self.app.router.add_get("/api/tab/{tab_index}", self.handle_tab_detail)
        self.app.router.add_get("/api/filtered", self.handle_filtered)
        self.app.router.add_get("/api/csv", self.handle_csv)
        self.app.router.add_get("/api/models", self.handle_models)
        self.app.router.add_get("/api/artifact", self.handle_artifact)
        if SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR.exists():
            self.app.router.add_static("/output", SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR, show_index=True)

    async def handle_csv(self, request: web.Request) -> web.Response:
        """Reads and parses the active run's 67-column CSV ledger in a worker thread off the main event loop."""
        payload = await asyncio.to_thread(_load_csv_analytics_payload)
        return web.json_response(payload)

    async def handle_models(self, request: web.Request) -> web.Response:
        """Returns the live stage-specific models resolved from prompts/*.md frontmatter."""
        return web.json_response({
            "router_model": SYSTEM_CONFIG.DEFAULT_ROUTER_MODEL,
            "section_router_model": SYSTEM_CONFIG.DEFAULT_SECTION_ROUTER_MODEL,
            "extraction_model": SYSTEM_CONFIG.DEFAULT_EXTRACTION_MODEL,
            "correction_model": SYSTEM_CONFIG.DEFAULT_CORRECTION_MODEL,
            "repair_model": SYSTEM_CONFIG.DEFAULT_REPAIR_MODEL,
            "query_model": SYSTEM_CONFIG.DEFAULT_QUERY_MODEL,
            "think_model": SYSTEM_CONFIG.DEFAULT_THINK_MODEL,
            "cpsa_timeout_seconds": SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS,
        })

    async def handle_tabs(self, request: web.Request) -> web.Response:
        """Returns the compact O(N) tab summary list and filtered count."""
        return web.json_response(GLOBAL_EVENT_BUS.get_tabs_overview())

    async def handle_active(self, request: web.Request) -> web.Response:
        """Returns the bounded in-memory event stream for the currently running RFC only."""
        return web.json_response(GLOBAL_EVENT_BUS.get_active_state())

    async def handle_tab_detail(self, request: web.Request) -> web.Response:
        """Hydrates a numbered tab (#1..#N) on demand from disk JSON artifacts."""
        raw_idx = request.match_info.get("tab_index", "")
        try:
            tab_idx = int(raw_idx)
        except ValueError:
            return web.json_response({"error": f"Invalid tab_index: {raw_idx}"}, status=400)

        tab_summary = GLOBAL_EVENT_BUS.get_tab_summary(tab_idx)
        if not tab_summary:
            return web.json_response({"error": f"Tab #{tab_idx} not found"}, status=404)

        payload = hydrate_tab_payload(tab_summary)
        return web.json_response(payload)

    async def handle_filtered(self, request: web.Request) -> web.Response:
        """Returns paginated disqualified/filtered RFCs for the collapsible drawer."""
        try:
            offset = int(request.query.get("offset", "0"))
        except ValueError:
            offset = 0
        try:
            limit = int(request.query.get("limit", "100"))
        except ValueError:
            limit = 100
        query = request.query.get("q", "")
        return web.json_response(GLOBAL_EVENT_BUS.get_filtered_slice(offset=offset, limit=limit, query=query))

    def _on_bus_event(self, event: PipelineEvent):
        """Dispatches an event from the pipeline event bus to all connected web clients thread-safely."""
        if hasattr(self, "loop") and self.loop and self.loop.is_running():
            for q in list(self._sse_clients):
                try:
                    self.loop.call_soon_threadsafe(q.put_nowait, event)
                except Exception:
                    pass
        else:
            for q in list(self._sse_clients):
                try:
                    q.put_nowait(event)
                except Exception:
                    pass

    async def handle_index(self, request: web.Request) -> web.Response:
        """Serves the main single-page visualizer dashboard."""
        if not HTML_TEMPLATE_PATH.exists():
            return web.Response(text="Dashboard template not found.", status=404)
        with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return web.Response(text=content, content_type="text/html")

    async def handle_history(self, request: web.Request) -> web.Response:
        """Returns JSON array of active RFC events (bounded)."""
        history = [e.model_dump() for e in GLOBAL_EVENT_BUS.get_history()]
        return web.json_response(history)

    def _is_allowed_artifact_path(self, resolved_path: Path) -> bool:
        """Restricts /api/artifact reads strictly to pipeline output directories and rejects dotfiles."""
        if resolved_path.name.startswith("."):
            return False
        allowed_roots = [SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR.resolve()]
        overview = GLOBAL_EVENT_BUS.get_tabs_overview()
        run_dir = overview.get("run_directory")
        if run_dir:
            allowed_roots.append(Path(run_dir).resolve())
        for tab in overview.get("accepted_tabs", []):
            rfc_dir = tab.get("rfc_dir")
            if rfc_dir:
                allowed_roots.append(Path(rfc_dir).resolve())
        return any(resolved_path.is_relative_to(root) for root in allowed_roots)

    async def handle_artifact(self, request: web.Request) -> web.Response:
        """Serves synthesized code or MITRE verification output files within authorized run directories."""
        filepath_str = request.query.get("path")
        if not filepath_str:
            return web.Response(text="Missing 'path' parameter", status=400)

        path = Path(filepath_str).resolve()
        if not self._is_allowed_artifact_path(path):
            return web.Response(text="Forbidden: path outside authorized output directories", status=403)
        if not path.exists() or not path.is_file():
            return web.Response(text=f"Artifact not found: {path.name}", status=404)

        content_type = "text/plain"
        if path.suffix in (".xhtml", ".html"):
            content_type = "application/xhtml+xml"
        elif path.suffix == ".svg":
            content_type = "image/svg+xml"
        elif path.suffix == ".json":
            content_type = "application/json"
        elif path.suffix == ".scm":
            content_type = "text/plain"

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            body = f.read()

        return web.Response(text=body, content_type=content_type)

    async def handle_sse(self, request: web.Request) -> web.StreamResponse:
        """Streams live Server-Sent Events to dashboard clients."""
        response = web.StreamResponse(
            status=200,
            reason="OK",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            },
        )
        await response.prepare(request)

        client_queue: asyncio.Queue = asyncio.Queue()
        self._sse_clients.add(client_queue)

        await response.write(b": ping\n\n")

        try:
            while True:
                try:
                    event: PipelineEvent = await asyncio.wait_for(client_queue.get(), timeout=15.0)
                    sse_msg = event.to_sse_message().encode("utf-8")
                    await response.write(sse_msg)
                except asyncio.TimeoutError:
                    await response.write(b": heartbeat\n\n")
        except (asyncio.CancelledError, ConnectionResetError):
            pass
        finally:
            self._sse_clients.discard(client_queue)

        return response


def run_visualizer_in_background(host: str = "127.0.0.1", port: int = 8080):
    """Starts the visualizer server in a background daemon thread with access_log disabled."""

    def _is_port_available(p: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, p)) != 0

    actual_port = port
    while not _is_port_available(actual_port) and actual_port < port + 20:
        actual_port += 1

    server = VisualizerServer(host=host, port=actual_port)
    server.port = actual_port

    def _target():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server.loop = loop
        runner = web.AppRunner(server.app, access_log=None)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, host, actual_port)
        loop.run_until_complete(site.start())
        logger.info("Visualizer server active at http://%s:%d", host, actual_port)
        loop.run_forever()

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    time.sleep(0.15)
    return server
```

---

### `src/visualizer/static/index.html`

*sha256:`15754b1924be` · 3649 lines · 153.1 KB (~39,179 tokens) · lang:`html`*

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RFC-LLM Pipeline Monitor</title>
  <style>
    :root {
      --bg-base: #0d1117;
      --bg-surface: #161b22;
      --bg-panel: #1b2129;
      --bg-code: #0b0e14;
      --border-color: #30363d;
      --border-focus: #58a6ff;
      --text-main: #e6edf3;
      --text-muted: #8b949e;
      --color-blue: #58a6ff;
      --color-green: #3fb950;
      --color-yellow: #d29922;
      --color-red: #f85149;
      --color-purple: #bc8cff;
      --mono: "JetBrains Mono", Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg-base);
      color: var(--text-main);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      font-size: 13px;
    }

    /* Top Utility Bar */
    header {
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      padding: 7px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      gap: 12px;
    }
    .header-left {
      display: flex;
      align-items: center;
      gap: 10px;
      white-space: nowrap;
    }
    .header-title {
      font-weight: 700;
      font-size: 14px;
      letter-spacing: -0.01em;
    }
    .run-dir-label {
      font-family: var(--mono);
      font-size: 10px;
      color: var(--text-muted);
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      padding: 2px 6px;
      max-width: 280px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .header-right {
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--mono);
      font-size: 11px;
      flex-wrap: nowrap;
    }
    .status-badge {
      display: inline-block;
      padding: 2px 8px;
      font-weight: 700;
      font-size: 11px;
      border: 1px solid var(--border-color);
      text-transform: uppercase;
    }
    .status-badge.idle { background: #21262d; color: var(--text-muted); }
    .status-badge.running { background: #0c2d6b; color: #58a6ff; border-color: #1f6feb; }
    .status-badge.success { background: #0e4429; color: #3fb950; border-color: #238636; }
    .status-badge.partial { background: #3b2300; color: #d29922; border-color: #9e6a03; }
    .status-badge.failed { background: #490202; color: #f85149; border-color: #da3633; }

    /* Virtualized Numbered RFC Tab Bar */
    .rfc-tabbar {
      display: flex;
      align-items: stretch;
      background: #10141b;
      border-bottom: 1px solid var(--border-color);
      height: 44px;
      flex-shrink: 0;
      user-select: none;
    }
    .live-pin-btn {
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 4px 12px;
      min-width: 145px;
      max-width: 185px;
      background: var(--bg-surface);
      border: none;
      border-right: 1px solid var(--border-color);
      color: var(--text-muted);
      font-family: var(--mono);
      cursor: pointer;
      text-align: left;
      flex-shrink: 0;
    }
    .live-pin-btn:hover {
      background: #1c222d;
      color: var(--text-main);
    }
    .live-pin-btn.active {
      background: #0d2149;
      color: var(--text-main);
      border-bottom: 2px solid var(--color-blue);
    }
    .live-pin-btn.replay-mode {
      cursor: default;
      background: #161b22;
    }
    .live-pin-top {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
    }
    .live-pin-sub {
      font-size: 11px;
      font-weight: 600;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-top: 1px;
    }
    .dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      display: inline-block;
      flex-shrink: 0;
    }
    .dot.running { background: var(--color-blue); box-shadow: 0 0 6px var(--color-blue); }
    .dot.verified { background: var(--color-green); }
    .dot.partial { background: var(--color-yellow); }
    .dot.failed { background: var(--color-red); }
    .dot.idle { background: var(--text-muted); }

    /* Virtual Scroll Viewport */
    .vtab-scroll {
      flex: 1;
      overflow-x: auto;
      overflow-y: hidden;
      position: relative;
      scrollbar-width: thin;
      scrollbar-color: #30363d #10141b;
    }
    .vtab-scroll::-webkit-scrollbar { height: 5px; }
    .vtab-scroll::-webkit-scrollbar-track { background: #10141b; }
    .vtab-scroll::-webkit-scrollbar-thumb { background: #30363d; }
    .vtab-spacer {
      position: relative;
      height: 100%;
    }
    .vtab-empty {
      height: 100%;
      display: flex;
      align-items: center;
      padding: 0 14px;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--text-muted);
    }
    .rfc-vtab {
      position: absolute;
      top: 0;
      height: 100%;
      width: 230px;
      padding: 4px 10px;
      background: #121720;
      border: none;
      border-right: 1px solid var(--border-color);
      color: var(--text-muted);
      font-family: var(--mono);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      justify-content: center;
      text-align: left;
    }
    .rfc-vtab:hover {
      background: #1b2230;
      color: var(--text-main);
    }
    .rfc-vtab.active {
      background: var(--bg-panel);
      color: var(--text-main);
      border-bottom: 2px solid var(--color-blue);
    }
    .rfc-vtab-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 6px;
      width: 100%;
    }
    .rfc-vtab-id {
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      font-weight: 700;
      color: var(--text-main);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .rfc-vtab-num {
      color: var(--color-blue);
    }
    .rfc-vtab-tier {
      font-size: 9px;
      font-weight: 700;
      padding: 0 4px;
      border: 1px solid var(--border-color);
      flex-shrink: 0;
    }
    .rfc-vtab-tier.GOLD, .rfc-vtab-tier.VERIFIED { color: #3fb950; border-color: #238636; background: #0e442966; }
    .rfc-vtab-tier.SILVER { color: #58a6ff; border-color: #1f6feb; background: #0c2d6b66; }
    .rfc-vtab-tier.BRONZE, .rfc-vtab-tier.PARTIAL { color: #d29922; border-color: #9e6a03; background: #3b230066; }
    .rfc-vtab-tier.REJECTED, .rfc-vtab-tier.FAILED, .rfc-vtab-tier.INTERRUPTED { color: #f85149; border-color: #da3633; background: #49020266; }
    .rfc-vtab-tier.PENDING, .rfc-vtab-tier.RUNNING { color: #bc8cff; border-color: #8957e5; background: #bc8cff18; }
    .rfc-vtab-proto {
      font-size: 10px;
      color: var(--text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-top: 2px;
      width: 100%;
    }
    .rfc-vtab.active .rfc-vtab-proto {
      color: #c9d1d9;
    }

    /* Right Controls on Tab Bar */
    .tabbar-controls {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 0 10px;
      background: var(--bg-surface);
      border-left: 1px solid var(--border-color);
      flex-shrink: 0;
    }
    .ctrl-input, .ctrl-select {
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      font-family: var(--mono);
      font-size: 11px;
      padding: 4px 7px;
      outline: none;
    }
    .ctrl-input:focus, .ctrl-select:focus {
      border-color: var(--border-focus);
    }
    .ctrl-input { width: 165px; }
    .ctrl-btn {
      background: #21262d;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 600;
      padding: 4px 9px;
      cursor: pointer;
      white-space: nowrap;
    }
    .ctrl-btn:hover {
      background: #2d333b;
      border-color: #484f58;
    }
    .ctrl-btn.active {
      background: #0c2d6b;
      border-color: var(--color-blue);
      color: var(--color-blue);
    }

    /* Collapsible Filtered / Rejected Drawer */
    .filtered-drawer {
      display: none;
      flex-direction: column;
      background: #11161d;
      border-bottom: 2px solid var(--color-blue);
      max-height: 290px;
      flex-shrink: 0;
    }
    .filtered-drawer.open {
      display: flex;
    }
    .drawer-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 14px;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      font-family: var(--mono);
      font-size: 11px;
    }
    .drawer-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .drawer-table-wrap {
      overflow-y: auto;
      flex: 1;
    }
    .drawer-table {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--mono);
      font-size: 11px;
    }
    .drawer-table th {
      position: sticky;
      top: 0;
      background: #161b22;
      color: var(--text-muted);
      text-align: left;
      padding: 5px 10px;
      border-bottom: 1px solid var(--border-color);
      font-size: 10px;
      text-transform: uppercase;
    }
    .drawer-table td {
      padding: 5px 10px;
      border-bottom: 1px solid #21262d;
      color: #c9d1d9;
      vertical-align: top;
    }
    .drawer-table tr:hover td {
      background: #1b2129;
    }

    /* Pipeline Stages Strip */
    .stepper {
      display: flex;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      flex-shrink: 0;
    }
    .step-item {
      flex: 1;
      padding: 7px 12px;
      border-right: 1px solid var(--border-color);
      background: var(--bg-surface);
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
    }
    .step-item:last-child { border-right: none; }
    .step-item.active {
      background: #111a2c;
      border-bottom: 2px solid var(--color-blue);
    }
    .step-item.passed {
      border-bottom: 2px solid var(--color-green);
    }
    .step-item.failed {
      background: #231215;
      border-bottom: 2px solid var(--color-red);
    }
    .step-header {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-family: var(--mono);
      color: var(--text-muted);
    }
    .step-name {
      font-weight: 600;
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .step-status {
      font-size: 11px;
      color: var(--text-muted);
      font-family: var(--mono);
    }
    .step-model {
      font-size: 10px;
      color: var(--color-purple);
      font-family: var(--mono);
      background: #bc8cff14;
      border: 1px solid #bc8cff33;
      padding: 1px 5px;
      margin-top: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .model-badge {
      display: inline-block;
      padding: 2px 8px;
      font-weight: 600;
      font-size: 11px;
      color: var(--color-purple);
      background: #bc8cff18;
      border: 1px solid #bc8cff44;
      font-family: var(--mono);
      max-width: 240px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      vertical-align: middle;
    }
    .timer-badge {
      display: inline-block;
      padding: 2px 8px;
      font-weight: 700;
      font-size: 11px;
      color: var(--color-blue);
      background: #58a6ff18;
      border: 1px solid #58a6ff44;
      font-family: var(--mono);
      min-width: 68px;
      text-align: center;
    }
    .diag-badge {
      display: inline-block;
      padding: 2px 8px;
      font-weight: 600;
      font-size: 11px;
      font-family: var(--mono);
      border: 1px solid var(--border-color);
      background: #21262d;
      color: var(--text-muted);
    }
    .diag-badge.normal { color: #58a6ff; background: #0c2d6b88; border-color: #1f6feb; }
    .diag-badge.syntax { color: #d29922; background: #3b2300aa; border-color: #d29922; }
    .diag-badge.snowball { color: #f85149; background: #490202cc; border-color: #f85149; animation: pulse-warn 1.2s infinite; }
    @keyframes pulse-warn {
      0%, 100% { opacity: 1.0; }
      50% { opacity: 0.65; }
    }

    /* Cost & Token Telemetry Strip */
    .cost-strip {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 4px 14px;
      background: #11161e;
      border-bottom: 1px solid var(--border-color);
      font-family: var(--mono);
      font-size: 10.5px;
      flex-shrink: 0;
      overflow-x: auto;
    }
    .cost-roles {
      display: flex;
      align-items: center;
      gap: 12px;
      white-space: nowrap;
    }
    .cost-totals {
      display: flex;
      align-items: center;
      gap: 10px;
      white-space: nowrap;
    }
    .cost-item {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      color: var(--text-muted);
    }
    .cost-val {
      color: var(--text-main);
      font-weight: 700;
    }
    .cost-val.highlight {
      color: var(--color-green);
      background: #0e442955;
      border: 1px solid #23863688;
      padding: 1px 6px;
    }
    .cost-val.batch {
      color: var(--color-blue);
      background: #0c2d6b55;
      border: 1px solid #1f6feb88;
      padding: 1px 6px;
    }
    .cost-tok {
      color: var(--text-muted);
      font-size: 10px;
    }

    /* Main Grid */
    .main-grid {
      display: flex;
      flex: 1;
      overflow: hidden;
    }

    /* Left: Live Terminal & Diagnostics */
    .log-panel {
      width: 42%;
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      background: var(--bg-panel);
    }
    .panel-heading {
      padding: 6px 12px;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      font-size: 11px;
      font-weight: 700;
      font-family: var(--mono);
      text-transform: uppercase;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .log-feed {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-family: var(--mono);
      font-size: 11px;
    }
    .log-entry {
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      padding: 6px 8px;
      line-height: 1.45;
    }
    .log-entry.repair { border-left: 3px solid var(--color-yellow); }
    .log-entry.cycle { border-left: 3px solid var(--color-purple); }
    .log-entry.error { border-left: 3px solid var(--color-red); }
    .log-entry.success { border-left: 3px solid var(--color-green); }
    .log-meta {
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
      font-size: 10px;
      margin-bottom: 4px;
    }
    .log-type {
      font-weight: 700;
      color: var(--color-blue);
    }
    .log-data {
      white-space: pre-wrap;
      word-break: break-word;
      color: #c9d1d9;
    }

    /* Right: Code & Model Inspection */
    .viewer-panel {
      width: 58%;
      display: flex;
      flex-direction: column;
      background: var(--bg-code);
      min-width: 0;
    }
    .tab-strip {
      display: flex;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      flex-shrink: 0;
    }
    .tab {
      padding: 8px 13px;
      background: transparent;
      border: none;
      border-right: 1px solid var(--border-color);
      color: var(--text-muted);
      font-family: var(--mono);
      font-size: 11px;
      cursor: pointer;
      font-weight: 600;
    }
    .tab.active {
      color: var(--text-main);
      background: var(--bg-code);
      border-top: 2px solid var(--color-blue);
      margin-top: -1px;
    }

    /* Per-Attempt Time-Travel Stepper Bar */
    .attempt-stepper {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 10px;
      background: #121720;
      border-bottom: 1px solid var(--border-color);
      overflow-x: auto;
      flex-shrink: 0;
      scrollbar-width: thin;
    }
    .attempt-stepper-label {
      font-family: var(--mono);
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-right: 4px;
      flex-shrink: 0;
    }
    .attempt-pill {
      padding: 3px 9px;
      background: #1b2129;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      font-family: var(--mono);
      font-size: 10px;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .attempt-pill:hover {
      color: var(--text-main);
      border-color: #484f58;
    }
    .attempt-pill.passed, .attempt-pill.verified {
      border-left: 3px solid var(--color-green);
    }
    .attempt-pill.rejected, .attempt-pill.failed {
      border-left: 3px solid var(--color-red);
    }
    .attempt-pill.cycle {
      border-left: 3px solid var(--color-purple);
    }
    .attempt-pill.active {
      background: #0c2d6b;
      color: #ffffff;
      border-color: var(--color-blue);
    }

    /* Per-Attempt Context & Diagnostic Banner */
    .attempt-banner {
      display: none;
      padding: 7px 12px;
      background: #151b24;
      border-bottom: 1px solid var(--border-color);
      font-family: var(--mono);
      font-size: 11px;
      line-height: 1.45;
      flex-shrink: 0;
    }
    .attempt-banner.visible {
      display: block;
    }
    .attempt-banner-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      margin-bottom: 3px;
    }
    .attempt-banner-diag {
      color: #f0883e;
      white-space: pre-wrap;
      word-break: break-word;
      max-height: 85px;
      overflow-y: auto;
    }
    .attempt-banner-rag {
      color: var(--color-purple);
      font-size: 10px;
      margin-top: 3px;
    }

    .tab-viewport {
      flex: 1;
      overflow: auto;
      padding: 12px;
      position: relative;
    }
    pre code {
      font-family: var(--mono);
      font-size: 12px;
      line-height: 1.55;
      color: #e6edf3;
      white-space: pre;
    }
    .svg-frame {
      width: 100%;
      height: 100%;
      border: none;
      background: #ffffff;
    }

    /* RAG Tab Styles */
    .rag-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 10px 12px;
      margin-bottom: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .rag-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: var(--text-muted);
    }
    .rag-purpose {
      font-weight: 700;
      color: var(--color-purple);
      text-transform: uppercase;
      font-family: var(--mono);
      font-size: 10px;
      border: 1px solid var(--border-color);
      padding: 1px 6px;
      background: var(--bg-base);
    }
    .rag-query-box {
      background: var(--bg-code);
      border: 1px solid var(--border-color);
      padding: 8px 10px;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--color-blue);
      line-height: 1.45;
      word-break: break-word;
    }
    .rag-chunks-container {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-top: 4px;
    }
    .rag-chunk-card {
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      padding: 8px 10px;
      font-size: 11px;
    }
    .rag-chunk-meta {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
      font-family: var(--mono);
      font-size: 10px;
    }
    .rag-chunk-id {
      background: #1f6feb22;
      color: var(--color-blue);
      border: 1px solid #1f6feb66;
      padding: 1px 5px;
      font-weight: 700;
    }
    .rag-chunk-source { color: var(--text-muted); }
    .rag-chunk-title {
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 4px;
    }
    .rag-chunk-snippet {
      font-family: var(--mono);
      font-size: 11px;
      color: #8b949e;
      background: #06090e;
      padding: 6px 8px;
      border: 1px solid #21262d;
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.4;
    }

    /* Floating ~300ms Hover Tooltip Popover */
    .rating-tooltip {
      position: fixed;
      z-index: 99999;
      max-width: 390px;
      background: #0d1117f2;
      border: 1px solid #58a6ff;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.75);
      padding: 9px 11px;
      font-family: var(--mono);
      font-size: 11px;
      line-height: 1.45;
      color: var(--text-main);
      pointer-events: none;
      display: none;
    }
    .rating-tooltip-title {
      font-weight: 700;
      font-size: 11.5px;
      color: var(--color-blue);
      margin-bottom: 4px;
      border-bottom: 1px solid #30363d;
      padding-bottom: 3px;
    }
    .rating-tooltip-desc {
      color: #c9d1d9;
      white-space: pre-wrap;
    }

    /* Always-Visible Compact Security Verdict Strip */
    .security-verdict-strip {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 5px 12px;
      background: #0e131a;
      border-bottom: 1px solid var(--border-color);
      font-family: var(--mono);
      font-size: 10.5px;
      flex-shrink: 0;
      overflow-x: auto;
      white-space: nowrap;
    }
    .sec-strip-item {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      color: var(--text-muted);
    }
    .sec-pill {
      display: inline-block;
      padding: 1px 6px;
      font-size: 10px;
      font-weight: 700;
      border: 1px solid var(--border-color);
      background: #21262d;
      color: var(--text-muted);
      cursor: help;
    }
    .sec-pill.ok { color: #3fb950; border-color: #238636; background: #0e442955; }
    .sec-pill.info { color: #58a6ff; border-color: #1f6feb; background: #0c2d6b55; }
    .sec-pill.warn { color: #d29922; border-color: #9e6a03; background: #3b230066; }
    .sec-pill.bad { color: #f85149; border-color: #da3633; background: #49020266; }

    /* Collapsible Snowball Autopsy Details */
    details.snowball-details {
      margin-top: 5px;
      background: #0b0e14;
      border: 1px solid #30363d;
      padding: 4px 8px;
      font-family: var(--mono);
      font-size: 10.5px;
    }
    details.snowball-details summary {
      cursor: pointer;
      color: var(--color-purple);
      font-weight: 600;
      user-select: none;
    }
    details.snowball-details pre {
      margin-top: 6px;
      white-space: pre-wrap;
      word-break: break-word;
      color: #8b949e;
      max-height: 220px;
      overflow-y: auto;
    }

    /* Security Findings (CPSA) Sub-Tab */
    .sec-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 10px;
      margin-bottom: 12px;
    }
    .sec-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .sec-card-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
    }
    .sec-card-body {
      font-family: var(--mono);
      font-size: 11px;
      color: #c9d1d9;
      line-height: 1.45;
    }
    .sec-banner-box {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-left: 3px solid var(--color-blue);
      padding: 9px 12px;
      margin-bottom: 12px;
      font-family: var(--mono);
      font-size: 11px;
      line-height: 1.45;
    }
    .sec-table {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--mono);
      font-size: 11px;
      margin-top: 6px;
    }
    .sec-table th {
      background: #161b22;
      color: var(--text-muted);
      text-align: left;
      padding: 6px 8px;
      border: 1px solid var(--border-color);
      font-size: 10px;
      text-transform: uppercase;
    }
    .sec-table td {
      padding: 6px 8px;
      border: 1px solid #21262d;
      color: #c9d1d9;
      vertical-align: top;
    }

    /* CSV Analytics (Live) Sub-Tab */
    .analytics-kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
      gap: 8px;
      margin-bottom: 12px;
    }
    .kpi-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 8px 10px;
      font-family: var(--mono);
    }
    .kpi-label {
      font-size: 10px;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-bottom: 3px;
    }
    .kpi-val {
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
    }
    .kpi-sub {
      font-size: 10px;
      color: var(--text-muted);
      margin-top: 2px;
    }
    .charts-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }
    .chart-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      min-height: 235px;
    }
    .chart-title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--mono);
      font-size: 11px;
      font-weight: 700;
      color: var(--text-main);
      border-bottom: 1px solid #21262d;
      padding-bottom: 5px;
    }
    .chart-sub {
      font-size: 10px;
      color: var(--text-muted);
      font-weight: 400;
    }
    .chart-svg-wrap {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 180px;
      width: 100%;
    }
  </style>
</head>
<body>
  <!-- Floating ~300ms Hover Tooltip Popover -->
  <div id="rating-tooltip" class="rating-tooltip">
    <div id="rating-tooltip-title" class="rating-tooltip-title"></div>
    <div id="rating-tooltip-desc" class="rating-tooltip-desc"></div>
  </div>

  <!-- Top Utility Bar -->
  <header>
    <div class="header-left">
      <span class="header-title">RFC-LLM Pipeline Monitor</span>
      <span class="run-dir-label" id="run-dir-badge" title="Active Run Directory">Initializing...</span>
    </div>
    <div class="header-right">
      <div>Stage Diagnosis: <span id="stage-diagnosis" class="diag-badge">Idle</span></div>
      <div>Attempt Timer: <span id="attempt-timer" class="timer-badge">0.0s</span></div>
      <div>Active Model: <span id="active-model" class="model-badge">nous/z-ai/glm-5.3</span></div>
      <div>RFC: <span id="rfc-name" style="color:var(--text-main); font-weight:700;">Waiting...</span></div>
      <div id="pipeline-status" class="status-badge idle">IDLE</div>
    </div>
  </header>

  <!-- Live & Per-RFC Cost & Token Telemetry Strip -->
  <div class="cost-strip" id="cost-strip">
    <div class="cost-roles">
      <span class="cost-item" title="Stage 1b/1c Router & Applicability Gate Cost">
        Router: <span class="cost-val" id="cost-router">$0.0000</span><span class="cost-tok" id="tok-router">(0 tok)</span>
      </span>
      <span class="cost-item" title="Stage 2 Initial Extraction & Schema Correction Cost">
        Extraction: <span class="cost-val" id="cost-extraction">$0.0000</span><span class="cost-tok" id="tok-extraction">(0 tok)</span>
      </span>
      <span class="cost-item" title="Stage 5/6 Agentic CPSA KB Searcher Cost">
        Query/Searcher: <span class="cost-val" id="cost-query">$0.0000</span><span class="cost-tok" id="tok-query">(0 tok)</span>
      </span>
      <span class="cost-item" title="Stage 5/6 Compiler & Solver Diagnostic Repair Cost">
        Repair: <span class="cost-val" id="cost-repair">$0.0000</span><span class="cost-tok" id="tok-repair">(0 tok)</span>
      </span>
    </div>
    <div class="cost-totals">
      <span class="cost-item" title="Total USD Cost & Tokens for Currently Viewed RFC">
        RFC Run Total: <span class="cost-val highlight" id="cost-rfc-total">$0.0000</span><span class="cost-tok" id="tok-rfc-total">(0 tok)</span>
      </span>
      <span class="cost-item" title="Cumulative USD Cost & Tokens Across Entire Batch">
        Batch Total: <span class="cost-val batch" id="cost-batch-total">$0.0000</span><span class="cost-tok" id="tok-batch-total">(0 tok)</span>
      </span>
    </div>
  </div>

  <!-- Virtualized Numbered Accepted-RFC Tab Strip (#1..#N) -->
  <div class="rfc-tabbar">
    <button class="live-pin-btn active" id="btn-live-follow" onclick="selectLiveFollow()">
      <div class="live-pin-top">
        <span class="dot idle" id="live-pin-dot"></span>
        <span id="live-pin-label">LIVE STREAM</span>
      </div>
      <div class="live-pin-sub" id="live-pin-rfc">Waiting for RFC...</div>
    </button>

    <div class="vtab-scroll" id="vtab-scroll">
      <div class="vtab-spacer" id="vtab-spacer">
        <div class="vtab-empty" id="vtab-empty">No accepted cryptographic protocol tabs yet.</div>
      </div>
    </div>

    <div class="tabbar-controls">
      <input
        type="text"
        id="tab-search-input"
        class="ctrl-input"
        placeholder="Jump # or filter RFC/proto..."
        oninput="onTabFilterChange()"
        onkeydown="onTabSearchKeydown(event)"
      />
      <select id="tab-status-filter" class="ctrl-select" onchange="onTabFilterChange()">
        <option value="ALL">ALL TABS (0)</option>
        <option value="GOLD">GOLD</option>
        <option value="SILVER">SILVER</option>
        <option value="BRONZE">BRONZE</option>
        <option value="VERIFIED">VERIFIED</option>
        <option value="PARTIAL">PARTIAL</option>
        <option value="FAILED">FAILED</option>
      </select>
      <button class="ctrl-btn" id="btn-filtered-toggle" onclick="toggleFilteredDrawer()">
        Filtered / Skipped (0)
      </button>
    </div>
  </div>

  <!-- Collapsible Filtered / Disqualified RFC Drawer -->
  <div class="filtered-drawer" id="filtered-drawer">
    <div class="drawer-header">
      <div>
        <strong>FILTERED / DISQUALIFIED RFCS</strong>
        <span id="filtered-range-label" style="color:var(--text-muted); margin-left:8px;">0 entries</span>
      </div>
      <div class="drawer-controls">
        <input
          type="text"
          id="filtered-search-input"
          class="ctrl-input"
          placeholder="Search filtered RFCs..."
          oninput="onFilteredSearchInput()"
        />
        <button class="ctrl-btn" onclick="pageFiltered(-100)">Prev 100</button>
        <button class="ctrl-btn" onclick="pageFiltered(100)">Next 100</button>
        <button class="ctrl-btn" onclick="toggleFilteredDrawer()">Close</button>
      </div>
    </div>
    <div class="drawer-table-wrap">
      <table class="drawer-table">
        <thead>
          <tr>
            <th style="width:55px;">#</th>
            <th style="width:110px;">RFC ID</th>
            <th style="width:260px;">Title</th>
            <th style="width:190px;">Rejection Gate</th>
            <th>Disqualification Rationale</th>
          </tr>
        </thead>
        <tbody id="filtered-tbody">
          <tr><td colspan="5" style="color:var(--text-muted);">No filtered RFCs recorded yet.</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Horizontal Pipeline Stepper -->
  <div class="stepper">
    <div class="step-item" id="step-1">
      <div class="step-header"><span>01</span><span id="step-1-time">--:--</span></div>
      <div class="step-name">Document Intake</div>
      <div class="step-model" id="step-1-model" title="Router & Gatekeeper Model">nous/z-ai/glm-5.3</div>
      <div class="step-status" id="step-1-status">Pending</div>
    </div>
    <div class="step-item" id="step-2">
      <div class="step-header"><span>02</span><span id="step-2-time">--:--</span></div>
      <div class="step-name">JSON CPSA Generation</div>
      <div class="step-model" id="step-2-model" title="JSON CPSA Generation Model">nous/google/gemini-4-argon</div>
      <div class="step-status" id="step-2-status">Pending</div>
    </div>
    <div class="step-item" id="step-3">
      <div class="step-header"><span>03</span><span id="step-3-time">--:--</span></div>
      <div class="step-name">CPSA4json -> scm</div>
      <div class="step-model" id="step-3-model" title="Deterministic Code Emitter">cpsa_scheme_emitter.py</div>
      <div class="step-status" id="step-3-status">Pending</div>
    </div>
    <div class="step-item" id="step-4">
      <div class="step-header"><span>04</span><span id="step-4-time">--:--</span></div>
      <div class="step-name">Roletran Check</div>
      <div class="step-model" id="step-4-model" title="Pre-flight Executability Binary">cpsa4roletran + cpsa4 -l 1</div>
      <div class="step-status" id="step-4-status">Pending</div>
    </div>
    <div class="step-item" id="step-5">
      <div class="step-header"><span>05</span><span id="step-5-time">--:--</span></div>
      <div class="step-name">Self-Healing Loop</div>
      <div class="step-model" id="step-5-model" title="Repair + RAG Query Models">gemini-3.8-flash + haiku-5.5</div>
      <div class="step-status" id="step-5-status">Pending</div>
    </div>
    <div class="step-item" id="step-6">
      <div class="step-header"><span>06</span><span id="step-6-time">--:--</span></div>
      <div class="step-name">CPSA Compilation</div>
      <div class="step-model" id="step-6-model" title="CPSA4 Compiler + Graph Builder">cpsa4 + cpsa4graph</div>
      <div class="step-status" id="step-6-status">Pending</div>
    </div>
  </div>

  <!-- Main Single Shared Viewport (O(1) DOM Nodes regardless of 5 or 5,000 RFC tabs) -->
  <div class="main-grid">
    <!-- Left: Event Stream -->
    <div class="log-panel">
      <div class="panel-heading">
        <span id="log-panel-title" style="display:inline-flex; align-items:center; gap:6px;"><span class="dot failed" style="box-shadow:0 0 6px var(--color-red);"></span>LIVE</span>
        <span id="event-counter" style="color:var(--text-muted); font-size:10px;">0 Events</span>
      </div>
      <div class="log-feed" id="log-feed"></div>
    </div>

    <!-- Right: Code, Per-Attempt Stepper, and Proof Inspection -->
    <div class="viewer-panel">
      <div class="tab-strip">
        <button class="tab active" data-subtab="scm" onclick="switchTab('scm')">CPSA Scheme (.scm)</button>
        <button class="tab" data-subtab="ast" onclick="switchTab('ast')">Pydantic AST (JSON)</button>
        <button class="tab" data-subtab="slice" onclick="switchTab('slice')">RFC Sliced Text</button>
        <button class="tab" data-subtab="rag" id="tab-btn-rag" onclick="switchTab('rag')">RAG Knowledge</button>
        <button class="tab" data-subtab="graph" onclick="switchTab('graph')">Verified Shapes (SVG)</button>
        <button class="tab" data-subtab="security" id="tab-btn-security" onclick="switchTab('security')">Security Findings (CPSA)</button>
        <button class="tab" data-subtab="analytics" id="tab-btn-analytics" onclick="switchTab('analytics')">CSV Analytics (Live)</button>
      </div>

      <!-- Always-Visible Compact Security & Quality Verdict Strip -->
      <div class="security-verdict-strip" id="security-verdict-strip">
        <span class="sec-strip-item">Quality: <span class="sec-pill" id="strip-quality" data-tooltip-key="PENDING">PENDING</span></span>
        <span class="sec-strip-item">Auth Profile: <span class="sec-pill" id="strip-auth" data-tooltip-key="PENDING">PENDING</span></span>
        <span class="sec-strip-item">Param Agreement: <span class="sec-pill" id="strip-agreement" data-tooltip-key="PENDING">PENDING</span></span>
        <span class="sec-strip-item">Secrecy: <span class="sec-pill" id="strip-secrecy" data-tooltip-key="PENDING">PENDING</span></span>
        <span class="sec-strip-item">Anomalies: <span class="sec-pill" id="strip-anomalies" style="cursor:pointer;" onclick="switchTab('security')">--</span></span>
      </div>

      <!-- Per-Attempt Time-Travel Stepper -->
      <div class="attempt-stepper" id="attempt-stepper">
        <span class="attempt-stepper-label">Attempts:</span>
        <span style="color:var(--text-muted); font-family:var(--mono); font-size:10px;">Waiting for synthesis...</span>
      </div>

      <!-- Per-Attempt Diagnostic & RAG Context Banner -->
      <div class="attempt-banner" id="attempt-banner">
        <div class="attempt-banner-head">
          <strong id="attempt-banner-stage">Attempt</strong>
          <div style="display:flex; gap:6px; align-items:center;">
            <button class="ctrl-btn" id="btn-toggle-rejected-scm" style="display:none; padding:1px 6px; font-size:10px;" onclick="toggleRejectedScmView()">
              Show Rejected Input .scm
            </button>
            <span id="attempt-banner-status" class="status-badge idle">PENDING</span>
          </div>
        </div>
        <div class="attempt-banner-diag" id="attempt-banner-diag"></div>
        <div class="attempt-banner-rag" id="attempt-banner-rag"></div>
      </div>

      <div class="tab-viewport" id="tab-scm">
        <pre><code id="code-scm">; CPSA Scheme model output will appear here...</code></pre>
      </div>
      <div class="tab-viewport" id="tab-ast" style="display:none;">
        <pre><code id="code-ast">// Pydantic JSON AST will appear here...</code></pre>
      </div>
      <div class="tab-viewport" id="tab-slice" style="display:none;">
        <pre><code id="code-slice">Verbatim RFC section slice will appear here...</code></pre>
      </div>
      <div class="tab-viewport" id="tab-rag" style="display:none; padding:12px; overflow-y:auto;">
        <div id="rag-feed" style="display:flex; flex-direction:column; gap:10px;">
          <div style="color:var(--text-muted); font-family:var(--mono); font-size:11px;">
            RAG queries and retrieved manual chunks will appear here...
          </div>
        </div>
      </div>
      <div class="tab-viewport" id="tab-graph" style="display:none; padding:0; height:100%;">
        <div id="graph-container" style="height:100%; display:flex; align-items:center; justify-content:center; color:var(--text-muted); font-family:var(--mono); font-size:11px;">
          MITRE CPSA shapes graph will render here upon successful verification.
        </div>
      </div>
      <div class="tab-viewport" id="tab-security" style="display:none; padding:12px; overflow-y:auto;">
        <div id="security-findings-container" style="color:var(--text-muted); font-family:var(--mono); font-size:11px;">
          Formal CPSA 4.4.9 security findings, Stage 1 intake rationale, parameter agreement maplets, and shape analysis sentences (`cpsa4sas`) will appear here upon protocol verification.
        </div>
      </div>
      <div class="tab-viewport" id="tab-analytics" style="display:none; padding:12px; overflow-y:auto;">
        <div id="analytics-container">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; font-family:var(--mono); font-size:11px;">
            <div>
              <strong style="color:var(--text-main);">LIVE CSV ANALYTICS &amp; GRAPH SUITE (OFF-MAIN-THREAD WEB WORKER)</strong>
              <span id="analytics-csv-label" style="color:var(--text-muted); margin-left:8px;">Loading CSV...</span>
            </div>
            <button class="ctrl-btn" onclick="refreshCsvAnalytics(true)">Refresh CSV Graphs</button>
          </div>
          <div id="analytics-kpis" class="analytics-kpi-grid"></div>
          <div id="analytics-charts" class="charts-grid"></div>
          <div id="analytics-custom-explorer" style="margin-bottom:14px;"></div>
          <div id="analytics-table-section"></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    // =========================================================================
    // Global State (Bounded O(1) DOM & 20-entry LRU Tab Cache)
    // =========================================================================
    const VTAB_WIDTH = 230;
    const LRU_MAX_TABS = 20;

    let viewMode = 'live';           // 'live' | 'tab'
    let isServerLive = true;
    let selectedTabIndex = null;
    let liveActiveTabIndex = null;
    let liveActiveRfcId = null;

    // Compact summary array of all accepted tabs (~150 bytes each -> 5,000 tabs = ~750 KB)
    let acceptedTabs = [];
    const acceptedTabsByIndex = new Map();
    let visibleFilteredTabs = [];
    let filteredTotalCount = 0;

    // 20-entry LRU cache mapping tab_index -> hydrated /api/tab/:idx payload
    const tabLruCache = new Map();

    // Active viewport state
    const seenEventKeys = new Set();
    let eventCount = 0;
    let pipelineRunning = false;
    let currentStageNum = 1;
    let activeAttemptEpoch = null;
    let currentActivityMode = 'idle';
    let currentRepairAttempt = 0;
    const stageStartEpochs = {};
    let ragFirstEvent = true;

    // Attempt time-travel state for currently displayed tab
    let currentAttemptsList = [];
    let selectedAttemptIdx = -1;
    let showingRejectedScm = false;

    let defaultModelCfg = {
      router_model: 'nous/z-ai/glm-5.3',
      extraction_model: 'nous/google/gemini-4-argon',
      repair_model: 'nous/google/gemini-3.8-flash',
      query_model: 'nous/anthropic/claude-haiku-5.5'
    };
    let latestBatchCostTelemetry = null;

    function formatUsd(val) {
      const n = Number(val || 0);
      return `$${n.toFixed(4)}`;
    }

    function formatTok(val) {
      const n = Number(val || 0);
      return `(${n.toLocaleString()} tok)`;
    }

    function renderCostTelemetry(rfcCost, batchCost) {
      if (batchCost && typeof batchCost === 'object') {
        latestBatchCostTelemetry = batchCost;
      }
      if (rfcCost && typeof rfcCost === 'object') {
        const roles = rfcCost.roles || {};
        ['router', 'extraction', 'query', 'repair'].forEach(roleKey => {
          const rb = roles[roleKey] || {};
          const costEl = document.getElementById(`cost-${roleKey}`);
          const tokEl = document.getElementById(`tok-${roleKey}`);
          if (costEl) costEl.innerText = formatUsd(rb.cost_usd);
          if (tokEl) tokEl.innerText = formatTok(rb.total_tokens);
        });
        const rfcTotEl = document.getElementById('cost-rfc-total');
        const rfcTokEl = document.getElementById('tok-rfc-total');
        if (rfcTotEl) rfcTotEl.innerText = formatUsd(rfcCost.total_cost_usd);
        if (rfcTokEl) rfcTokEl.innerText = formatTok(rfcCost.total_tokens);
      }
      const effBatch = latestBatchCostTelemetry || rfcCost;
      if (effBatch && typeof effBatch === 'object') {
        const bTotEl = document.getElementById('cost-batch-total');
        const bTokEl = document.getElementById('tok-batch-total');
        if (bTotEl) bTotEl.innerText = formatUsd(effBatch.total_cost_usd);
        if (bTokEl) bTokEl.innerText = formatTok(effBatch.total_tokens);
      }
    }

    function lruGet(tabIdx) {
      if (!tabLruCache.has(tabIdx)) return null;
      const val = tabLruCache.get(tabIdx);
      tabLruCache.delete(tabIdx);
      tabLruCache.set(tabIdx, val);
      return val;
    }

    function lruSet(tabIdx, payload) {
      if (tabLruCache.has(tabIdx)) tabLruCache.delete(tabIdx);
      tabLruCache.set(tabIdx, payload);
      if (tabLruCache.size > LRU_MAX_TABS) {
        const oldestKey = tabLruCache.keys().next().value;
        tabLruCache.delete(oldestKey);
      }
    }

    // =========================================================================
    // Virtualized Horizontal Tab Bar (Handles 5,000+ Tabs with ~25 DOM Nodes)
    // =========================================================================
    function recomputeVisibleTabs() {
      const q = (document.getElementById('tab-search-input')?.value || '').trim().toLowerCase();
      const statusFilter = document.getElementById('tab-status-filter')?.value || 'ALL';

      const allOption = document.querySelector('#tab-status-filter option[value="ALL"]');
      if (allOption) allOption.innerText = `ALL TABS (${acceptedTabs.length})`;

      visibleFilteredTabs = acceptedTabs.filter(t => {
        if (statusFilter !== 'ALL') {
          if (['GOLD', 'SILVER', 'BRONZE'].includes(statusFilter)) {
            if ((t.quality_tier || '') !== statusFilter) return false;
          } else if (t.status !== statusFilter) {
            return false;
          }
        }
        if (!q) return true;
        const numMatch = `#${t.tab_index}` === q || `${t.tab_index}` === q;
        return (
          numMatch ||
          (t.rfc_id || '').toLowerCase().includes(q) ||
          (t.protocol_name || '').toLowerCase().includes(q) ||
          (t.rfc_title || '').toLowerCase().includes(q) ||
          (t.quality_tier || '').toLowerCase().includes(q)
        );
      });

      renderVirtualTabs();
    }

    function renderVirtualTabs() {
      const scrollEl = document.getElementById('vtab-scroll');
      const spacerEl = document.getElementById('vtab-spacer');
      if (!scrollEl || !spacerEl) return;

      const total = visibleFilteredTabs.length;
      if (total === 0) {
        spacerEl.style.width = '100%';
        const msg = acceptedTabs.length === 0
          ? 'No accepted cryptographic protocol tabs yet.'
          : 'No tabs match current filter.';
        spacerEl.innerHTML = `<div class="vtab-empty">${msg}</div>`;
        return;
      }

      const totalWidth = total * VTAB_WIDTH;
      spacerEl.style.width = `${totalWidth}px`;

      const scrollLeft = scrollEl.scrollLeft;
      const viewportW = scrollEl.clientWidth || 1200;
      const firstIdx = Math.max(0, Math.floor(scrollLeft / VTAB_WIDTH) - 4);
      const lastIdx = Math.min(total - 1, Math.ceil((scrollLeft + viewportW) / VTAB_WIDTH) + 4);

      const frag = document.createDocumentFragment();
      for (let i = firstIdx; i <= lastIdx; i++) {
        const t = visibleFilteredTabs[i];
        const btn = document.createElement('button');
        const isSelected = (viewMode === 'tab' && selectedTabIndex === t.tab_index)
          || (viewMode === 'live' && liveActiveTabIndex === t.tab_index);
        btn.className = `rfc-vtab${isSelected ? ' active' : ''}`;
        btn.style.left = `${i * VTAB_WIDTH}px`;
        btn.onclick = () => selectNumberedTab(t.tab_index);

        const dotClass = t.status === 'VERIFIED' ? 'verified'
          : (t.status === 'PARTIAL' ? 'partial'
          : (t.status === 'RUNNING' ? 'running' : 'failed'));
        const badgeText = (t.status === 'RUNNING') ? 'LIVE' : (t.quality_tier || t.status || '');
        const badgeClass = (t.status === 'RUNNING') ? 'RUNNING' : (t.quality_tier || t.status || '');
        const protoDisplay = t.protocol_name || t.rfc_title || t.rfc_id;
        const tabCostStr = (typeof t.cost_usd === 'number' && t.cost_usd > 0) ? ` | $${t.cost_usd.toFixed(4)}` : '';

        btn.title = [
          `Tab #${t.tab_index} | ${t.rfc_id}`,
          `Protocol: ${protoDisplay}`,
          t.rfc_title && t.rfc_title !== protoDisplay ? `Title: ${t.rfc_title}` : null,
          `Status: ${t.status} | Tier: ${t.quality_tier}`,
          `Repairs: ${t.total_attempts || 0} | Shapes: ${t.shapes_count || 0} | Time: ${t.duration_seconds || 0}s${tabCostStr}`
        ].filter(Boolean).join('\n');

        const topDiv = document.createElement('div');
        topDiv.className = 'rfc-vtab-top';

        const idSpan = document.createElement('div');
        idSpan.className = 'rfc-vtab-id';
        idSpan.innerHTML = `<span class="dot ${dotClass}"></span><span class="rfc-vtab-num">#${t.tab_index}</span><span>${escapeHtml(t.rfc_id)}</span>`;

        const tierSpan = document.createElement('span');
        tierSpan.className = `rfc-vtab-tier ${badgeClass}`;
        tierSpan.setAttribute('data-tooltip-key', badgeClass);
        tierSpan.innerText = badgeText;

        topDiv.appendChild(idSpan);
        topDiv.appendChild(tierSpan);

        const protoDiv = document.createElement('div');
        protoDiv.className = 'rfc-vtab-proto';
        protoDiv.innerText = `${protoDisplay}${tabCostStr}`;

        btn.appendChild(topDiv);
        btn.appendChild(protoDiv);
        frag.appendChild(btn);
      }

      spacerEl.innerHTML = '';
      spacerEl.appendChild(frag);
    }

    document.getElementById('vtab-scroll').addEventListener('scroll', () => {
      window.requestAnimationFrame(renderVirtualTabs);
    });
    window.addEventListener('resize', () => {
      window.requestAnimationFrame(renderVirtualTabs);
    });

    function onTabFilterChange() {
      recomputeVisibleTabs();
    }

    function onTabSearchKeydown(e) {
      if (e.key === 'Enter') {
        const raw = e.target.value.trim().replace(/^#/, '');
        const num = parseInt(raw, 10);
        if (!isNaN(num) && acceptedTabsByIndex.has(num)) {
          selectNumberedTab(num);
          scrollTabIntoView(num);
        } else if (visibleFilteredTabs.length > 0) {
          selectNumberedTab(visibleFilteredTabs[0].tab_index);
        }
      }
    }

    function scrollTabIntoView(tabIndex) {
      const pos = visibleFilteredTabs.findIndex(t => t.tab_index === tabIndex);
      if (pos < 0) return;
      const scrollEl = document.getElementById('vtab-scroll');
      const targetLeft = pos * VTAB_WIDTH;
      if (targetLeft < scrollEl.scrollLeft || targetLeft + VTAB_WIDTH > scrollEl.scrollLeft + scrollEl.clientWidth) {
        scrollEl.scrollLeft = Math.max(0, targetLeft - VTAB_WIDTH);
      }
    }

    function upsertTabSummary(tabObj) {
      if (!tabObj || !tabObj.tab_index) return;
      if (acceptedTabsByIndex.has(tabObj.tab_index)) {
        const existing = acceptedTabsByIndex.get(tabObj.tab_index);
        Object.assign(existing, tabObj);
      } else {
        acceptedTabs.push(tabObj);
        acceptedTabs.sort((a, b) => a.tab_index - b.tab_index);
        acceptedTabsByIndex.set(tabObj.tab_index, tabObj);
      }
      tabLruCache.delete(tabObj.tab_index);
      recomputeVisibleTabs();
    }

    function updateFilteredButtonCount(count) {
      filteredTotalCount = count;
      const btn = document.getElementById('btn-filtered-toggle');
      if (btn) btn.innerText = `Filtered / Skipped (${count})`;
    }

    function updateLivePinButton() {
      const btn = document.getElementById('btn-live-follow');
      const dot = document.getElementById('live-pin-dot');
      const lbl = document.getElementById('live-pin-label');
      const sub = document.getElementById('live-pin-rfc');
      if (!btn) return;

      btn.classList.toggle('active', viewMode === 'live');
      if (!isServerLive) {
        btn.classList.add('replay-mode');
        dot.className = 'dot idle';
        lbl.innerText = 'OFFLINE REPLAY';
        sub.innerText = `${acceptedTabs.length} Accepted Tabs`;
      } else {
        btn.classList.remove('replay-mode');
        dot.className = pipelineRunning ? 'dot running' : 'dot idle';
        lbl.innerText = liveActiveTabIndex ? `LIVE | TAB #${liveActiveTabIndex}` : 'LIVE STREAM';
        sub.innerText = liveActiveRfcId || 'Waiting...';
      }
    }

    // =========================================================================
    // Viewport Reset & Switching Between [LIVE] and Historical Tab #1..#N
    // =========================================================================
    function resetViewportDom(headerTitle) {
      seenEventKeys.clear();
      eventCount = 0;
      ragFirstEvent = true;
      currentAttemptsList = [];
      selectedAttemptIdx = -1;
      showingRejectedScm = false;

      document.getElementById('event-counter').innerText = '0 Events';
      const titleEl = document.getElementById('log-panel-title');
      if (!headerTitle || headerTitle === 'LIVE') {
        titleEl.innerHTML = '<span class="dot failed" style="box-shadow:0 0 6px var(--color-red);"></span>LIVE';
      } else {
        titleEl.innerText = headerTitle;
      }
      document.getElementById('log-feed').innerHTML = '';
      document.getElementById('rag-feed').innerHTML = `
        <div style="color:var(--text-muted); font-family:var(--mono); font-size:11px;">
          No RAG manual retrievals recorded for this protocol yet.
        </div>`;
      document.getElementById('code-scm').innerText = '; CPSA Scheme model output will appear here...';
      document.getElementById('code-ast').innerText = '// Pydantic JSON AST will appear here...';
      document.getElementById('code-slice').innerText = 'Verbatim RFC section slice will appear here...';
      document.getElementById('graph-container').innerHTML =
        'MITRE CPSA shapes graph will render here upon successful verification.';
      document.getElementById('security-findings-container').innerHTML =
        '<div style="color:var(--text-muted); font-family:var(--mono); font-size:11px;">Formal CPSA 4.4.9 security findings, Stage 1 intake rationale, parameter agreement maplets, and shape analysis sentences (`cpsa4sas`) will appear here upon protocol verification.</div>';
      renderSecurityVerdictStrip('PENDING', null);
      document.getElementById('attempt-banner').classList.remove('visible');
      document.getElementById('attempt-stepper').innerHTML =
        '<span class="attempt-stepper-label">Attempts:</span><span style="color:var(--text-muted); font-family:var(--mono); font-size:10px;">Live synthesis...</span>';

      for (let s = 1; s <= 6; s++) {
        const el = document.getElementById(`step-${s}`);
        if (el) el.classList.remove('active', 'passed', 'failed');
        const st = document.getElementById(`step-${s}-status`);
        if (st) st.innerText = 'Pending';
        const tm = document.getElementById(`step-${s}-time`);
        if (tm) tm.innerText = '--:--';
      }
    }

    function selectLiveFollow() {
      if (!isServerLive) {
        if (acceptedTabs.length > 0) selectNumberedTab(acceptedTabs[0].tab_index);
        return;
      }
      viewMode = 'live';
      selectedTabIndex = null;
      updateLivePinButton();
      renderVirtualTabs();
      resetViewportDom('LIVE');

      fetch('/api/active')
        .then(r => r.json())
        .then(state => {
          if (state && Array.isArray(state.events)) {
            state.events.forEach(evt => renderEventIntoViewport(evt, true));
          }
        })
        .catch(() => {});
    }

    function selectNumberedTab(tabIndex) {
      const summary = acceptedTabsByIndex.get(tabIndex);
      if (isServerLive && tabIndex === liveActiveTabIndex && summary && summary.status === 'RUNNING') {
        selectLiveFollow();
        return;
      }
      viewMode = 'tab';
      selectedTabIndex = tabIndex;
      pipelineRunning = false;
      updateLivePinButton();
      renderVirtualTabs();

      resetViewportDom(summary ? `Tab #${tabIndex} | ${summary.rfc_id} (${summary.protocol_name})` : `Tab #${tabIndex}`);

      const cached = lruGet(tabIndex);
      if (cached) {
        applyHydratedTabPayload(cached);
        return;
      }

      document.getElementById('stage-diagnosis').innerText = `Loading Tab #${tabIndex}...`;
      fetch(`/api/tab/${tabIndex}`)
        .then(r => r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`)))
        .then(payload => {
          if (payload.tab && payload.tab.status !== 'RUNNING') {
            lruSet(tabIndex, payload);
          }
          if (viewMode === 'tab' && selectedTabIndex === tabIndex) {
            applyHydratedTabPayload(payload);
          }
        })
        .catch(err => {
          document.getElementById('code-scm').innerText = `; Failed to load Tab #${tabIndex}: ${err}`;
        });
    }

    function applyHydratedTabPayload(payload) {
      const tab = payload.tab || {};
      document.getElementById('rfc-name').innerText = `#${tab.tab_index} ${tab.rfc_id} (${tab.protocol_name || ''})`;
      document.getElementById('attempt-timer').innerText = `${(tab.duration_seconds || 0).toFixed(1)}s`;

      const pill = document.getElementById('pipeline-status');
      if (tab.status === 'VERIFIED') {
        pill.className = 'status-badge success';
        pill.innerText = `${tab.quality_tier || 'VERIFIED'}`;
        pill.setAttribute('data-tooltip-key', tab.quality_tier || 'VERIFIED');
        setDiagnosisBadge(`Verified (${tab.shapes_count || 0} Realized Shapes)`, 'normal');
      } else if (tab.status === 'PARTIAL') {
        pill.className = 'status-badge partial';
        pill.innerText = 'PARTIAL';
        pill.setAttribute('data-tooltip-key', 'PARTIAL');
        setDiagnosisBadge('Roletran Passed | CPSA Failed', 'syntax');
      } else if (tab.status === 'RUNNING') {
        pill.className = 'status-badge running';
        pill.innerText = 'RUNNING';
        pill.setAttribute('data-tooltip-key', 'RUNNING');
        setDiagnosisBadge('Active Synthesis...', 'normal');
      } else {
        pill.className = 'status-badge failed';
        pill.innerText = tab.status || 'FAILED';
        pill.setAttribute('data-tooltip-key', tab.quality_tier || tab.status || 'FAILED');
        setDiagnosisBadge(tab.error_message ? 'Failed (See Attempt Banner)' : 'Halted', 'syntax');
      }

      if (payload.verbatim_slice) {
        document.getElementById('code-slice').innerText = payload.verbatim_slice;
      }

      if (payload.cost_telemetry || tab.cost_telemetry) {
        renderCostTelemetry(payload.cost_telemetry || tab.cost_telemetry, latestBatchCostTelemetry);
      }

      if (Array.isArray(payload.events)) {
        payload.events.forEach(evt => renderEventIntoViewport(evt, false));
      }

      if (payload.shapes_xhtml) {
        document.getElementById('graph-container').innerHTML =
          `<iframe class="svg-frame" src="/api/artifact?path=${encodeURIComponent(payload.shapes_xhtml)}"></iframe>`;
      }

      const secFindings = payload.security_findings || (payload.quality_assessment || {}).security_findings || tab.security_findings || {};
      const qTier = (payload.quality_assessment || {}).quality_tier || tab.quality_tier || tab.status || 'REJECTED';
      renderSecurityVerdictStrip(qTier, secFindings);
      renderSecurityFindingsTab(payload);

      currentAttemptsList = Array.isArray(payload.attempts) ? payload.attempts : [];
      renderAttemptStepper();
      if (currentAttemptsList.length > 0) {
        selectAttemptSnapshot(currentAttemptsList.length - 1);
      }
    }

    // =========================================================================
    // Per-Attempt Time-Travel Stepper (#0 Initial -> #1..#K Repairs -> Final)
    // =========================================================================
    function renderAttemptStepper() {
      const bar = document.getElementById('attempt-stepper');
      if (!bar) return;
      if (!currentAttemptsList.length) {
        bar.innerHTML = '<span class="attempt-stepper-label">Attempts:</span><span style="color:var(--text-muted); font-family:var(--mono); font-size:10px;">No attempt snapshots recorded.</span>';
        return;
      }

      const frag = document.createDocumentFragment();
      const lbl = document.createElement('span');
      lbl.className = 'attempt-stepper-label';
      lbl.innerText = `Attempts (${currentAttemptsList.length}):`;
      frag.appendChild(lbl);

      currentAttemptsList.forEach((att, idx) => {
        const btn = document.createElement('button');
        const stLow = (att.status || '').toLowerCase();
        const cyc = att.cycle_detected ? ' cycle' : '';
        const act = (idx === selectedAttemptIdx) ? ' active' : '';
        btn.className = `attempt-pill ${stLow}${cyc}${act}`;
        btn.innerText = att.label || `Attempt ${idx}`;
        btn.title = `${att.stage}\nStatus: ${att.status}${att.cycle_detected ? ' (Cycle Perturbation)' : ''}`;
        btn.onclick = () => selectAttemptSnapshot(idx);
        frag.appendChild(btn);
      });

      bar.innerHTML = '';
      bar.appendChild(frag);
    }

    function splitSnowballDiagnostic(diagStr) {
      if (!diagStr) return { headline: '', autopsy: null };
      const marker = '=== CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT';
      const idx = diagStr.indexOf(marker);
      if (idx >= 0) {
        const head = diagStr.slice(0, idx).trim();
        const autopsy = diagStr.slice(idx).trim();
        return { headline: head || 'CPSA state-space snowball timeout', autopsy };
      }
      return { headline: diagStr, autopsy: null };
    }

    function selectAttemptSnapshot(idx) {
      if (idx < 0 || idx >= currentAttemptsList.length) return;
      selectedAttemptIdx = idx;
      showingRejectedScm = false;
      renderAttemptStepper();

      const att = currentAttemptsList[idx];
      document.getElementById('code-scm').innerText = att.scm || '; No .scm recorded for this attempt.';
      document.getElementById('code-ast').innerText = att.ast
        ? JSON.stringify(att.ast, null, 2)
        : '// No JSON AST recorded for this attempt.';

      const banner = document.getElementById('attempt-banner');
      const stageEl = document.getElementById('attempt-banner-stage');
      const statusEl = document.getElementById('attempt-banner-status');
      const diagEl = document.getElementById('attempt-banner-diag');
      const ragEl = document.getElementById('attempt-banner-rag');
      const toggleBtn = document.getElementById('btn-toggle-rejected-scm');

      banner.classList.add('visible');
      stageEl.innerText = `${att.label} — ${att.stage}${att.cycle_detected ? ' [CYCLE PERTURBATION]' : ''}`;

      if (att.status === 'VERIFIED' || att.status === 'PASSED') {
        statusEl.className = 'status-badge success';
      } else if (att.status === 'GENERATED') {
        statusEl.className = 'status-badge running';
      } else {
        statusEl.className = 'status-badge failed';
      }
      statusEl.innerText = att.status || 'INFO';

      if (att.rejected_scm && att.rejected_scm !== att.scm) {
        toggleBtn.style.display = 'inline-block';
        toggleBtn.innerText = 'Show Rejected Input .scm';
      } else {
        toggleBtn.style.display = 'none';
      }

      if (att.diagnostic) {
        const sp = splitSnowballDiagnostic(att.diagnostic);
        diagEl.style.color = '#f0883e';
        if (sp.autopsy) {
          diagEl.innerHTML = `<div>Diagnostic: ${escapeHtml(sp.headline)}</div>` +
            `<details class="snowball-details"><summary>▸ Show CPSA 4.4.9 Snowball State Autopsy Report</summary><pre>${escapeHtml(sp.autopsy)}</pre></details>`;
        } else {
          diagEl.innerText = `Diagnostic: ${att.diagnostic}`;
        }
      } else {
        diagEl.style.color = '#3fb950';
        diagEl.innerText = 'No compiler errors on this snapshot.';
      }

      if (att.rag_query || (att.retrieved_chunks && att.retrieved_chunks.length) || att.searcher_diagnosis) {
        const cids = (att.retrieved_chunks || []).map(c => `${c.chunk_id}`).join(', ');
        const diagLine = att.searcher_diagnosis ? `\nSearcher Fix Brief: ${att.searcher_diagnosis}` : '';
        ragEl.innerText = `Agentic KB Tools: ${att.rag_query || 'direct'} | Retrieved: ${cids || 'none'}${diagLine}`;
      } else if (att.attempt_number >= 1 && att.attempt_id !== 'final') {
        ragEl.innerText = 'Fast Direct Repair Pass (Pinned CPSA System Header — Agentic Searcher skipped)';
      } else {
        ragEl.innerText = '';
      }
    }

    function toggleRejectedScmView() {
      if (selectedAttemptIdx < 0 || selectedAttemptIdx >= currentAttemptsList.length) return;
      const att = currentAttemptsList[selectedAttemptIdx];
      if (!att.rejected_scm) return;
      showingRejectedScm = !showingRejectedScm;
      const toggleBtn = document.getElementById('btn-toggle-rejected-scm');
      if (showingRejectedScm) {
        document.getElementById('code-scm').innerText = att.rejected_scm;
        toggleBtn.innerText = 'Show Repaired Output .scm';
      } else {
        document.getElementById('code-scm').innerText = att.scm;
        toggleBtn.innerText = 'Show Rejected Input .scm';
      }
    }

    // =========================================================================
    // Collapsible Filtered / Disqualified RFC Drawer
    // =========================================================================
    let filteredOffset = 0;
    let filteredDebounce = null;

    function toggleFilteredDrawer() {
      const drawer = document.getElementById('filtered-drawer');
      const btn = document.getElementById('btn-filtered-toggle');
      const isOpen = drawer.classList.toggle('open');
      btn.classList.toggle('active', isOpen);
      if (isOpen) {
        filteredOffset = 0;
        fetchFilteredPage();
      }
    }

    function onFilteredSearchInput() {
      clearTimeout(filteredDebounce);
      filteredDebounce = setTimeout(() => {
        filteredOffset = 0;
        fetchFilteredPage();
      }, 200);
    }

    function pageFiltered(delta) {
      filteredOffset = Math.max(0, filteredOffset + delta);
      fetchFilteredPage();
    }

    function fetchFilteredPage() {
      const q = encodeURIComponent(document.getElementById('filtered-search-input')?.value || '');
      fetch(`/api/filtered?offset=${filteredOffset}&limit=100&q=${q}`)
        .then(r => r.json())
        .then(data => {
          updateFilteredButtonCount(data.total || 0);
          const items = data.items || [];
          const endIdx = Math.min(data.matching || 0, filteredOffset + items.length);
          const startIdx = items.length ? filteredOffset + 1 : 0;
          document.getElementById('filtered-range-label').innerText =
            `Showing ${startIdx}-${endIdx} of ${data.matching || 0} matching (${data.total || 0} total)`;

          const tbody = document.getElementById('filtered-tbody');
          if (!items.length) {
            tbody.innerHTML = '<tr><td colspan="5" style="color:var(--text-muted);">No matching filtered RFCs.</td></tr>';
            return;
          }
          tbody.innerHTML = items.map(it => `
            <tr>
              <td>${it.index || ''}</td>
              <td style="color:var(--color-blue); font-weight:700;">${escapeHtml(it.rfc_id || '')}</td>
              <td>${escapeHtml(it.title || '')}</td>
              <td style="color:var(--color-yellow);">${escapeHtml(it.gate || '')}</td>
              <td style="color:var(--text-muted);">${escapeHtml(it.reason || '')}</td>
            </tr>
          `).join('');
        })
        .catch(() => {});
    }

    // =========================================================================
    // Live Timer, Stepper, and Real-Time SSE Event Dispatcher
    // =========================================================================
    function setDiagnosisBadge(text, styleClass) {
      const el = document.getElementById('stage-diagnosis');
      if (!el) return;
      el.innerText = text;
      el.className = `diag-badge ${styleClass || ''}`;
    }

    function updateLiveTimers() {
      if (viewMode !== 'live' || !pipelineRunning || !activeAttemptEpoch) return;
      const nowSec = Date.now() / 1000;
      const elapsed = Math.max(0, nowSec - activeAttemptEpoch);
      const timerEl = document.getElementById('attempt-timer');

      if (currentActivityMode === 'solver' || (currentActivityMode === 'repair_timeout' && elapsed > 20)) {
        if (timerEl) timerEl.innerText = `${elapsed.toFixed(1)}s / 60s`;
        if (elapsed > 30) {
          setDiagnosisBadge(`STATE-SPACE SNOWBALLING (${elapsed.toFixed(0)}s / 60s cap)`, 'snowball');
        } else if (elapsed > 10) {
          setDiagnosisBadge(`Deep CPSA4 Strand Search (${elapsed.toFixed(0)}s / 60s)`, 'syntax');
        } else {
          setDiagnosisBadge('CPSA4 Compiling & Solving...', 'normal');
        }
      } else if (currentActivityMode === 'repair_syntax') {
        if (timerEl) timerEl.innerText = `${elapsed.toFixed(1)}s`;
        setDiagnosisBadge(`Fast Syntax/Roletran Reject -> LLM Repair #${currentRepairAttempt}`, 'syntax');
      } else if (currentActivityMode === 'repair_timeout') {
        if (timerEl) timerEl.innerText = `${elapsed.toFixed(1)}s`;
        setDiagnosisBadge(`60s Timeout (Snowball) -> LLM Repair #${currentRepairAttempt}`, 'snowball');
      } else if (currentActivityMode === 'extraction') {
        if (timerEl) timerEl.innerText = `${elapsed.toFixed(1)}s`;
        setDiagnosisBadge('Generating CPSA JSON...', 'normal');
      } else {
        if (timerEl) timerEl.innerText = `${elapsed.toFixed(1)}s`;
      }

      if (currentStageNum) {
        const stepTimeEl = document.getElementById(`step-${currentStageNum}-time`);
        const stageStart = stageStartEpochs[currentStageNum] || activeAttemptEpoch;
        const stageElapsed = Math.max(0, nowSec - stageStart);
        if (stepTimeEl) stepTimeEl.innerText = `${stageElapsed.toFixed(1)}s`;
      }
    }
    setInterval(updateLiveTimers, 100);

    function switchTab(tabId) {
      document.querySelectorAll('.tab').forEach(b => {
        b.classList.toggle('active', b.getAttribute('data-subtab') === tabId);
      });
      document.querySelectorAll('.tab-viewport').forEach(v => v.style.display = 'none');
      const targetView = document.getElementById(`tab-${tabId}`);
      if (targetView) targetView.style.display = 'block';
      if (tabId === 'analytics') {
        refreshCsvAnalytics(false);
      }
    }

    function setStepState(stageNum, state, label) {
      const step = document.getElementById(`step-${stageNum}`);
      if (!step) return;
      step.classList.remove('active', 'passed', 'failed');
      if (state === 'active') step.classList.add('active');
      else if (state === 'passed') step.classList.add('passed');
      else if (state === 'failed') step.classList.add('failed');

      if (label) {
        const statEl = document.getElementById(`step-${stageNum}-status`);
        if (statEl) statEl.innerText = label;
      }
    }

    function handleIncomingBusEvent(evt) {
      if (!evt || !evt.event_type) return;

      if (evt.event_type === 'csv_updated') {
        scheduleCsvAnalyticsRefresh();
        return;
      }

      // Global tab & filtered registry updates ALWAYS apply regardless of whether viewing [LIVE] or Tab #k
      if (evt.event_type === 'tab_accepted' && evt.data && evt.data.tab) {
        liveActiveTabIndex = evt.data.tab.tab_index;
        liveActiveRfcId = evt.data.tab.rfc_id;
        upsertTabSummary(evt.data.tab);
        updateLivePinButton();
        return;
      }
      if (evt.event_type === 'tab_updated' && evt.data && evt.data.tab) {
        upsertTabSummary(evt.data.tab);
        updateLivePinButton();
        return;
      }
      if (evt.event_type === 'rfc_filtered' && evt.data) {
        updateFilteredButtonCount(evt.data.filtered_total || (filteredTotalCount + 1));
        if (document.getElementById('filtered-drawer').classList.contains('open')) {
          fetchFilteredPage();
        }
        scheduleCsvAnalyticsRefresh();
        return;
      }
      if (evt.event_type === 'cost_updated' && evt.data) {
        if (evt.data.batch_cost) {
          latestBatchCostTelemetry = evt.data.batch_cost;
        }
        if (evt.tab_index && acceptedTabsByIndex.has(evt.tab_index) && evt.data.rfc_cost) {
          const existing = acceptedTabsByIndex.get(evt.tab_index);
          existing.cost_usd = Number(evt.data.rfc_cost.total_cost_usd || 0);
          existing.cost_telemetry = evt.data.rfc_cost;
          renderVirtualTabs();
        }
        if (viewMode === 'live') {
          renderCostTelemetry(evt.data.rfc_cost, evt.data.batch_cost);
        } else if (evt.data.batch_cost) {
          renderCostTelemetry(null, evt.data.batch_cost);
        }
        return;
      }
      if (evt.event_type === 'pipeline_started') {
        liveActiveRfcId = (evt.data && (evt.data.rfc_id || evt.data.rfc_file)) || evt.rfc_id;
        liveActiveTabIndex = null;
        pipelineRunning = true;
        updateLivePinButton();
        if (viewMode === 'live') {
          resetViewportDom('LIVE');
          renderCostTelemetry({ total_cost_usd: 0, total_tokens: 0, roles: {} }, latestBatchCostTelemetry);
        }
      }
      if (evt.event_type === 'pipeline_completed' || evt.event_type === 'pipeline_failed') {
        pipelineRunning = false;
        updateLivePinButton();
        scheduleCsvAnalyticsRefresh();
      }

      // Only mutate the shared DOM viewport if following [LIVE]
      if (viewMode === 'live') {
        renderEventIntoViewport(evt, true);
      }
    }

    function renderSnowballAutopsyCard(timestamp, attemptNum, autopsyText) {
      if (!autopsyText) return;
      const feed = document.getElementById('rag-feed');
      if (!feed) return;
      if (ragFirstEvent) {
        feed.innerHTML = '';
        ragFirstEvent = false;
      }
      const timeStr = new Date((timestamp || (Date.now() / 1000)) * 1000).toLocaleTimeString([], { hour12: false });
      const card = document.createElement('div');
      card.className = 'rag-card';
      card.style.borderLeft = '3px solid var(--color-red)';
      card.innerHTML = `
        <div class="rag-card-header">
          <span class="rag-purpose" style="color:var(--color-red); border-color:var(--color-red);">CPSA 4.4.9 SNOWBALL AUTOPSY (REPAIR #${escapeHtml(String(attemptNum || 1))})</span>
          <span>${escapeHtml(timeStr)}</span>
        </div>
        <details class="snowball-details" open>
          <summary>▸ Snowball State-Space Unification Autopsy Report</summary>
          <pre>${escapeHtml(autopsyText)}</pre>
        </details>
      `;
      feed.prepend(card);
    }

    function renderEventIntoViewport(evt, fetchLiveArtifacts) {
      if (
        evt.event_type === 'tab_accepted' ||
        evt.event_type === 'tab_updated' ||
        evt.event_type === 'rfc_filtered' ||
        evt.event_type === 'cost_updated' ||
        evt.event_type === 'csv_updated'
      ) {
        if (evt.event_type === 'cost_updated' && evt.data && evt.data.rfc_cost) {
          renderCostTelemetry(evt.data.rfc_cost, evt.data.batch_cost || latestBatchCostTelemetry);
        }
        return;
      }
      const key = `${evt.timestamp}_${evt.event_type}_${evt.stage || 0}`;
      if (seenEventKeys.has(key)) return;
      seenEventKeys.add(key);

      // Route Agentic KB Search strictly to the RAG Knowledge tab (never into the LIVE feed)
      if (evt.event_type === 'rag_retrieval') {
        activeAttemptEpoch = evt.timestamp;
        const ragMod = `${defaultModelCfg.query_model} (Agentic KB Searcher)`;
        const badge = document.getElementById('active-model');
        if (badge) badge.innerText = ragMod;
        renderRagEvent(evt);
        return;
      }

      eventCount++;
      document.getElementById('event-counter').innerText = `${eventCount} Events`;

      const feed = document.getElementById('log-feed');
      const item = document.createElement('div');
      item.className = 'log-entry';

      const timeStr = new Date(evt.timestamp * 1000).toLocaleTimeString([], { hour12: false });
      let typeLabel = evt.event_type;
      const safeData = Object.assign({}, evt.data || {});
      delete safeData.ast;
      let bodyText = Object.keys(safeData).length ? JSON.stringify(safeData) : '';
      let extraAutopsyHtml = '';

      const stageDefaultModels = {
        1: document.getElementById('step-1-model')?.innerText || defaultModelCfg.router_model,
        2: document.getElementById('step-2-model')?.innerText || defaultModelCfg.extraction_model,
        3: 'cpsa_scheme_emitter.py',
        4: 'cpsa4roletran + cpsa4 -l 1',
        5: document.getElementById('step-5-model')?.innerText || `${defaultModelCfg.repair_model}`,
        6: document.getElementById('step-6-model')?.innerText || 'cpsa4 + cpsa4graph'
      };

      function updateActiveModel(modelStr, stageNum) {
        if (!modelStr) return;
        const badge = document.getElementById('active-model');
        if (badge) badge.innerText = modelStr;
        if (stageNum) {
          const stepModelEl = document.getElementById(`step-${stageNum}-model`);
          if (stepModelEl) stepModelEl.innerText = modelStr;
        }
      }

      if (evt.event_type === 'pipeline_started') {
        typeLabel = 'PIPELINE_INIT';
        bodyText = `Target: ${evt.data.rfc_file || evt.data.rfc_id || ''}`;
        if (fetchLiveArtifacts) pipelineRunning = true;
        currentStageNum = 1;
        currentRepairAttempt = 0;
        activeAttemptEpoch = evt.timestamp;
        stageStartEpochs[1] = evt.timestamp;
        currentActivityMode = 'intake';
        if (fetchLiveArtifacts) {
          setDiagnosisBadge('Screening RFC & TOC...', 'normal');
          document.getElementById('rfc-name').innerText = evt.data.rfc_file || evt.data.rfc_id;
          const pill = document.getElementById('pipeline-status');
          pill.className = 'status-badge running';
          pill.innerText = 'RUNNING';
          pill.setAttribute('data-tooltip-key', 'RUNNING');
        }
        if (evt.data.router_model) document.getElementById('step-1-model').innerText = evt.data.router_model;
        if (evt.data.extraction_model) document.getElementById('step-2-model').innerText = evt.data.extraction_model;
        if (evt.data.repair_model) {
          const qm = evt.data.query_model ? ` + ${evt.data.query_model.split('/').pop()}` : '';
          document.getElementById('step-5-model').innerText = `${evt.data.repair_model}${qm}`;
          document.getElementById('step-6-model').innerText = `cpsa4 + ${evt.data.repair_model}`;
        }
        updateActiveModel(evt.data.router_model || stageDefaultModels[1], 1);
        setStepState(1, 'active', 'Started');
      } else if (evt.event_type === 'stage_started') {
        typeLabel = `STAGE_${evt.stage}_START`;
        const stgModel = (evt.data && evt.data.model) || stageDefaultModels[evt.stage] || '';
        bodyText = `${evt.stage_name || (evt.data && evt.data.stage_name) || `Stage ${evt.stage}`} | Model: ${stgModel}`;
        currentStageNum = evt.stage;
        activeAttemptEpoch = evt.timestamp;
        stageStartEpochs[evt.stage] = evt.timestamp;
        if (fetchLiveArtifacts) {
          if (evt.stage === 1) { currentActivityMode = 'intake'; setDiagnosisBadge('Screening RFC & TOC...', 'normal'); }
          else if (evt.stage === 2) { currentActivityMode = 'extraction'; setDiagnosisBadge('Generating CPSA JSON...', 'normal'); }
          else if (evt.stage === 4 || evt.stage === 5) { currentActivityMode = 'roletran'; setDiagnosisBadge('Roletran Check...', 'normal'); }
          else if (evt.stage === 6) { currentActivityMode = 'solver'; setDiagnosisBadge('CPSA4 Compiling & Solving...', 'normal'); }
        }
        setStepState(evt.stage, 'active', 'Processing');
        updateActiveModel(stgModel, evt.stage);
      } else if (evt.event_type === 'compiler_check_started') {
        typeLabel = `COMPILER_RUN_${evt.data.attempt || 0}`;
        bodyText = `Validator: ${evt.data.model || 'cpsa4'} | Attempt #${evt.data.attempt || 0}`;
        currentStageNum = evt.stage || 6;
        activeAttemptEpoch = evt.timestamp;
        currentActivityMode = (evt.stage === 6) ? 'solver' : 'roletran';
        updateActiveModel(evt.data.model || 'cpsa4 + cpsa4graph', evt.stage || 6);
        setStepState(evt.stage || 6, 'active', `Testing #${evt.data.attempt || 0}`);
      } else if (evt.event_type === 'stage_completed') {
        typeLabel = `STAGE_${evt.stage}_OK`;
        setStepState(evt.stage, 'passed', 'Passed');
        if (evt.stage === 1) {
          bodyText = `Confirmed Protocol: ${evt.data.protocol_name || ''} (${evt.data.rfc_id || ''})`;
        } else if (evt.stage === 2) {
          const rCount = evt.data.roles_count ?? (evt.data.ast?.roles?.length || 0);
          const sCount = evt.data.skeletons_count ?? (evt.data.ast?.skeletons?.length || 0);
          bodyText = `Synthesized Pydantic AST (${rCount} roles, ${sCount} skeletons)`;
        } else if (evt.stage === 3) {
          const scmName = (evt.data.scm_path || '').split('/').pop() || 'protocol.scm';
          const repTag = evt.data.repair_attempt ? ` (Repair #${evt.data.repair_attempt})` : '';
          bodyText = `Emitted CPSA Scheme: ${scmName}${repTag}`;
        } else if (evt.stage === 4 || evt.stage === 5) {
          bodyText = `Roletran Executability Passed${evt.data.attempts !== undefined ? ` (${evt.data.attempts} repair attempts)` : ''}`;
        }
        if (stageStartEpochs[evt.stage]) {
          const dur = Math.max(0, evt.timestamp - stageStartEpochs[evt.stage]);
          const timeEl = document.getElementById(`step-${evt.stage}-time`);
          if (timeEl) timeEl.innerText = `${dur.toFixed(1)}s`;
        }
        if (fetchLiveArtifacts && evt.data && evt.data.ast) {
          document.getElementById('code-ast').innerText = JSON.stringify(evt.data.ast, null, 2);
        }
        if (fetchLiveArtifacts && evt.data && evt.data.scm_path) {
          fetch(`/api/artifact?path=${encodeURIComponent(evt.data.scm_path)}`)
            .then(r => r.text())
            .then(txt => { document.getElementById('code-scm').innerText = txt; })
            .catch(() => {});
        }
      } else if (evt.event_type === 'slice_ready') {
        typeLabel = 'SLICE_EXTRACTED';
        bodyText = `Sections: ${JSON.stringify(evt.data.sections)}\nLine count: ${evt.data.line_count}`;
        if (fetchLiveArtifacts && evt.data && evt.data.slice_path) {
          fetch(`/api/artifact?path=${encodeURIComponent(evt.data.slice_path)}`)
            .then(r => r.text())
            .then(txt => { document.getElementById('code-slice').innerText = txt; })
            .catch(() => {});
        }
      } else if (evt.event_type === 'repair_attempt') {
        item.classList.add('repair');
        if (evt.data.cycle_detected) item.classList.add('cycle');
        typeLabel = `REPAIR_${evt.data.attempt}_OF_${evt.data.max_attempts}`;
        currentStageNum = evt.stage || 5;
        currentRepairAttempt = evt.data.attempt || 1;
        activeAttemptEpoch = evt.timestamp;
        const rawDiag = evt.data.diagnostic || '';
        const sp = splitSnowballDiagnostic(rawDiag);
        const diagStr = rawDiag.toLowerCase();
        const isTimeout = diagStr.includes('timed out') || diagStr.includes('step limit');
        currentActivityMode = isTimeout ? 'repair_timeout' : 'repair_syntax';
        const failureTag = isTimeout ? '[60s TIMEOUT / STATE-SPACE SNOWBALL]' : '[FAST SYNTAX / ROLETRAN ERROR]';
        const repMod = evt.data.model || defaultModelCfg.repair_model;
        const qMod = evt.data.query_model || defaultModelCfg.query_model;
        updateActiveModel(`${repMod} (RAG: ${qMod.split('/').pop()})`, evt.stage || 5);
        bodyText = `${failureTag}\nRepair Model: ${repMod} | Query Model: ${qMod}\nDiagnostic: ${sp.headline}\nCycle Detected: ${evt.data.cycle_detected ? 'YES (Perturbation active)' : 'NO'}`;
        if (sp.autopsy) {
          renderSnowballAutopsyCard(evt.timestamp, evt.data.attempt, sp.autopsy);
          extraAutopsyHtml = `<details class="snowball-details"><summary>▸ View Snowball State Autopsy Report (also in RAG Knowledge tab)</summary><pre>${escapeHtml(sp.autopsy)}</pre></details>`;
        }
        setStepState(evt.stage || 5, 'active', `Attempt ${evt.data.attempt}/${evt.data.max_attempts || 50}`);
      } else if (evt.event_type === 'stage_failed') {
        item.classList.add('error');
        typeLabel = `STAGE_${evt.stage}_FAIL`;
        const sp = splitSnowballDiagnostic(evt.data.error_message || evt.data.reason || 'Stage failed');
        bodyText = sp.headline;
        if (sp.autopsy) {
          extraAutopsyHtml = `<details class="snowball-details"><summary>▸ View Snowball State Autopsy Report</summary><pre>${escapeHtml(sp.autopsy)}</pre></details>`;
        }
        setStepState(evt.stage, 'failed', 'Failed');
      } else if (evt.event_type === 'pipeline_completed') {
        item.classList.add('success');
        if (fetchLiveArtifacts) {
          pipelineRunning = false;
          setDiagnosisBadge(`Verified (${evt.data.shapes_count} Realized Shapes)`, 'normal');
          const pill = document.getElementById('pipeline-status');
          pill.className = 'status-badge success';
          pill.innerText = evt.data.quality_tier || 'VERIFIED';
          pill.setAttribute('data-tooltip-key', evt.data.quality_tier || 'VERIFIED');
          if (evt.data.shapes_xhtml) {
            document.getElementById('graph-container').innerHTML =
              `<iframe class="svg-frame" src="/api/artifact?path=${encodeURIComponent(evt.data.shapes_xhtml)}"></iframe>`;
          }
          if (evt.data.security_findings) {
            renderSecurityVerdictStrip(evt.data.quality_tier || 'VERIFIED', evt.data.security_findings);
            renderSecurityFindingsTab({
              tab: { rfc_id: evt.rfc_id, protocol_name: evt.data.protocol_name, quality_tier: evt.data.quality_tier, status: 'VERIFIED', shapes_count: evt.data.shapes_count },
              intake_rationale: evt.data.intake_rationale,
              security_findings: evt.data.security_findings,
              quality_assessment: { quality_tier: evt.data.quality_tier, security_findings: evt.data.security_findings }
            });
          }
        }
        typeLabel = 'SYNTHESIS_VERIFIED';
        bodyText = `Protocol: ${evt.data.protocol_name || ''} | Tier: ${evt.data.quality_tier || 'VERIFIED'} | Shapes: ${evt.data.shapes_count ?? 0}`;
        setStepState(6, 'passed', `Shapes: ${evt.data.shapes_count}`);
      } else if (evt.event_type === 'pipeline_failed') {
        item.classList.add('error');
        if (fetchLiveArtifacts) {
          pipelineRunning = false;
          setDiagnosisBadge('Halted / Max Attempts Reached', 'snowball');
          const pill = document.getElementById('pipeline-status');
          pill.className = 'status-badge failed';
          pill.innerText = 'FAILED';
          pill.setAttribute('data-tooltip-key', 'REJECTED');
        }
        typeLabel = 'PIPELINE_HALTED';
        const sp = splitSnowballDiagnostic(evt.data.error_message || evt.data.reason || 'Pipeline halted');
        bodyText = sp.headline;
        if (sp.autopsy) {
          extraAutopsyHtml = `<details class="snowball-details"><summary>▸ View Snowball State Autopsy Report</summary><pre>${escapeHtml(sp.autopsy)}</pre></details>`;
        }
      }

      item.innerHTML = `
        <div class="log-meta">
          <span class="log-type">${escapeHtml(typeLabel)}</span>
          <span>${escapeHtml(timeStr)}</span>
        </div>
        <div class="log-data">${escapeHtml(bodyText)}</div>
        ${extraAutopsyHtml}
      `;

      feed.appendChild(item);
      feed.scrollTop = feed.scrollHeight;
    }

    function renderRagEvent(evt) {
      const feed = document.getElementById('rag-feed');
      if (!feed) return;
      if (ragFirstEvent) {
        feed.innerHTML = '';
        ragFirstEvent = false;
      }

      const card = document.createElement('div');
      card.className = 'rag-card';

      const timeStr = new Date(evt.timestamp * 1000).toLocaleTimeString([], { hour12: false });
      const purpose = (evt.data && evt.data.purpose) || 'Agentic KB Search';
      const query = (evt.data && evt.data.query) || '';
      const searcherDiagnosis = (evt.data && evt.data.searcher_diagnosis) || '';
      const searcherTurns = (evt.data && evt.data.searcher_turns) || [];
      const chunks = (evt.data && evt.data.chunks) || [];

      let turnsHtml = '';
      if (searcherTurns.length > 0) {
        let turnItems = '';
        searcherTurns.forEach((t) => {
          let toolsList = '';
          (t.tool_calls || []).forEach((tc) => {
            toolsList += `
              <div style="margin-top:4px; padding:4px 6px; background:rgba(88,166,255,0.08); border-left:2px solid #58a6ff; font-family:var(--mono); font-size:11px;">
                <span style="color:#58a6ff; font-weight:600;">${escapeHtml(tc.tool || 'tool')}</span>(${escapeHtml(tc.args || '')})
                <div style="color:var(--text-muted); margin-top:2px;">↳ Retrieved: ${escapeHtml(tc.retrieved || '')}</div>
              </div>
            `;
          });
          turnItems += `
            <div style="padding:6px 8px; background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:4px; margin-top:6px;">
              <div style="display:flex; justify-content:space-between; font-size:11px; font-family:var(--mono);">
                <strong style="color:#d2a8ff;">Searcher Turn #${escapeHtml(String(t.turn || 1))}</strong>
                <span style="color:${t.is_final ? '#3fb950' : '#f0883e'};">${escapeHtml(t.status || '')}</span>
              </div>
              ${toolsList}
              ${t.ast_root_cause ? `<div style="margin-top:4px; font-size:11px; color:var(--text-main);"><strong>Thought / Cause:</strong> ${escapeHtml(t.ast_root_cause)}</div>` : ''}
            </div>
          `;
        });
        turnsHtml = `
          <div style="margin-bottom:8px;">
            <div style="font-size:10px; color:var(--text-muted); font-family:var(--mono);">Agentic Searcher Tool-Use Trace (${searcherTurns.length} Turn${searcherTurns.length > 1 ? 's' : ''}):</div>
            ${turnItems}
          </div>
        `;
      }

      const diagnosisHtml = searcherDiagnosis ? `
        <div class="rag-query-box" style="border-left:3px solid #3fb950; background:rgba(63,185,80,0.08); white-space:pre-wrap; margin-bottom:8px;">
          <strong style="color:#3fb950;">Compiled Fix Brief Passed to Repair LLM:</strong>\n${escapeHtml(searcherDiagnosis)}
        </div>
      ` : '';

      let chunksHtml = '';
      chunks.forEach((chk) => {
        const cidStr = String(chk.chunk_id || '');
        const isScm = cidStr.endsWith('.scm');
        const badgeLabel = isScm ? `MITRE .scm Example` : `KB Section: ${cidStr}`;
        chunksHtml += `
          <div class="rag-chunk-card">
            <div class="rag-chunk-meta">
              <span class="rag-chunk-id">${escapeHtml(badgeLabel)}</span>
              <span class="rag-chunk-source">${escapeHtml(chk.source_file || 'CPSA Knowledge Base')}</span>
            </div>
            <div class="rag-chunk-title">${escapeHtml(chk.title || '')}</div>
            ${chk.snippet ? `<div class="rag-chunk-snippet">${escapeHtml(chk.snippet)}</div>` : ''}
          </div>
        `;
      });

      card.innerHTML = `
        <div class="rag-card-header">
          <span class="rag-purpose">${escapeHtml(purpose)}</span>
          <span>${escapeHtml(timeStr)}</span>
        </div>
        <div class="rag-query-box"><strong>Executed Tool Calls / Queries:</strong> ${escapeHtml(query)}</div>
        ${turnsHtml}
        ${diagnosisHtml}
        <div class="rag-chunks-container">
          <div style="font-size:10px; color:var(--text-muted); font-family:var(--mono);">Retrieved CPSA Rules &amp; .scm Examples (${chunks.length}):</div>
          ${chunksHtml}
        </div>
      `;

      feed.prepend(card);
    }

    function escapeHtml(str) {
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    // =========================================================================
    // Plain-English Hover Tooltips (~300ms Delay) for Quality Tiers & CPSA Verdicts
    // =========================================================================
    const RATING_TOOLTIPS = {
      GOLD: {
        title: 'GOLD — Full Multi-Party Interaction (Structural Quality)',
        desc: 'Every participant role in the protocol compiled in CPSA, realized at least one valid execution shape, and interacted with at least one peer strand (>=2 strands in every point-of-view shape). Graded purely on structural fidelity — independent of whether the RFC protocol has security weaknesses.'
      },
      SILVER: {
        title: 'SILVER — Partial Interaction / Local Execution',
        desc: 'CPSA compiled the model and realized >=1 execution shape, and all defined roles are executable, but at least one point-of-view skeleton completed locally (single-strand) without requiring a peer response.'
      },
      BRONZE: {
        title: 'BRONZE — Vacuous or Dead-Role Model',
        desc: 'CPSA exited 0, but either 0 shapes were realized (contradictory assumptions), or the model contains dead/unused roles that were never instantiated in any skeleton.'
      },
      REJECTED: {
        title: 'REJECTED — Uncompilable Model',
        desc: 'The model failed CPSA syntax/executability checks or exhausted the 60s solver budget without compiling.'
      },
      PARTIAL: {
        title: 'PARTIAL — Pre-Flight Passed, Solver Failed',
        desc: 'Static role executability (cpsa4roletran / cpsa4 -l 1) succeeded, but full CPSA4 shape search failed or timed out.'
      },
      VERIFIED: {
        title: 'VERIFIED — Formally Analyzed by CPSA4',
        desc: 'MITRE CPSA4 completed shape analysis and generated formal execution shapes.'
      },
      FAILED: {
        title: 'FAILED — Pipeline Halted',
        desc: 'Synthesis or formal verification halted before producing a compiled CPSA shape graph.'
      },
      RUNNING: {
        title: 'RUNNING — Live Synthesis in Progress',
        desc: 'Currently executing synthesis and formal verification stages for this RFC.'
      },
      PENDING: {
        title: 'PENDING — Awaiting CPSA Verification',
        desc: 'Formal verification results have not been finalized yet.'
      },
      ALL_ROLES_EXECUTABLE: {
        title: 'ALL_ROLES_EXECUTABLE (CPSA Role Executability)',
        desc: 'Every defined role passed cpsa4roletran / cpsa4 -l 1 static executability and is instantiated in at least one preskeleton.'
      },
      PARTIAL_DEAD_ROLES: {
        title: 'PARTIAL_DEAD_ROLES (CPSA Role Executability)',
        desc: 'One or more defined roles were never instantiated in any preskeleton or realized shape.'
      },
      DEAD_ROLES_PRESENT: {
        title: 'DEAD_ROLES_PRESENT (CPSA Role Executability)',
        desc: 'One or more defined roles were never instantiated in any preskeleton or realized shape.'
      },
      NO_ROLES_EXECUTABLE: {
        title: 'NO_ROLES_EXECUTABLE (CPSA Role Executability)',
        desc: 'No participant roles realized an executable shape or static roletran failed.'
      },
      ROLETRAN_FAILED: {
        title: 'ROLETRAN_FAILED (CPSA Role Executability)',
        desc: 'At least one role failed static executability (e.g. sends a variable before receiving or originating it).'
      },
      MUTUAL_MULTI_STRAND: {
        title: 'MUTUAL_MULTI_STRAND (CPSA Authentication Profile)',
        desc: 'Every participant point-of-view skeleton realized >=1 shape and every realized shape required >=2 interacting strands (mutual peer authentication).'
      },
      MUTUAL_PEER_INTERACTION: {
        title: 'MUTUAL_PEER_INTERACTION (CPSA Authentication Profile)',
        desc: 'Every participant point-of-view skeleton realized >=1 shape and every realized shape required >=2 interacting strands (peer authentication).'
      },
      UNILATERAL_AUTHENTICATED: {
        title: 'UNILATERAL_AUTHENTICATED (CPSA Authentication Profile)',
        desc: 'At least one participant POV strictly required peer interaction (>=2 strands), while another POV completed locally (e.g. unilateral server-authenticated key exchange).'
      },
      UNILATERAL_PARTIAL: {
        title: 'UNILATERAL_PARTIAL (CPSA Authentication Profile)',
        desc: 'Some participant POVs required peer interaction (>=2 strands), while at least one POV completed locally (single-strand).'
      },
      CONDITIONAL_BRANCHED_AUTHENTICATION: {
        title: 'CONDITIONAL_BRANCHED_AUTHENTICATION (Branched 1-Strand / 2-Strand Shapes)',
        desc: 'A participant POV split into both a 2-strand peer-authenticated shape and a 1-strand self-communication/unauthenticated shape (e.g. missing principal inequality fact).'
      },
      UNAUTHENTICATED_OR_CLEARTEXT_EXECUTABLE: {
        title: 'UNAUTHENTICATED_OR_CLEARTEXT_EXECUTABLE (Single-Strand Execution Only)',
        desc: 'All realized shapes contained only a single strand — the POV role completed without CPSA proving any peer strand participated.'
      },
      LOCAL_ONLY: {
        title: 'LOCAL_ONLY (CPSA Authentication Profile)',
        desc: 'All realized shapes contained only a single strand (the POV role completed without proving any peer strand existed).'
      },
      NON_EXECUTABLE: {
        title: 'NON_EXECUTABLE (0 Realized Shapes)',
        desc: 'CPSA realized 0 shapes (preskeleton assumptions were contradictory or solver failed).'
      },
      NO_REALIZED_SHAPES: {
        title: 'NO_REALIZED_SHAPES (CPSA Authentication Profile)',
        desc: 'CPSA realized 0 shapes (preskeleton assumptions were contradictory or solver failed).'
      },
      FULL_PARAMETER_AGREEMENT: {
        title: 'FULL_PARAMETER_AGREEMENT (Injective Parameter Agreement)',
        desc: 'In every realized multi-strand shape, peer strands mapped identical values onto all shared protocol parameters (no MITM principal mismatch or parameter substitution).'
      },
      FULL_AGREEMENT: {
        title: 'FULL_AGREEMENT (Injective Parameter Agreement)',
        desc: 'In every realized shape, peer strands mapped identical values onto all shared protocol parameters (no parameter substitution or MITM mismatch).'
      },
      PRINCIPAL_DISAGREEMENT_MITM_OR_UKS: {
        title: 'PRINCIPAL_DISAGREEMENT_MITM_OR_UKS (Lowe MITM / Unknown Key-Share)',
        desc: 'CPSA realized a shape where the POV strand and a peer strand disagreed on a principal identity parameter (e.g. b vs b-0 in Needham-Schroeder Lowe MITM).'
      },
      PARAMETER_DISAGREEMENT_DETECTED: {
        title: 'PARAMETER_DISAGREEMENT_DETECTED (Data/Key Parameter Substitution)',
        desc: 'CPSA realized a shape where the POV strand and a peer strand bound different values (e.g. x vs x-0) to a shared non-principal parameter.'
      },
      DISAGREEMENT_DETECTED: {
        title: 'DISAGREEMENT_DETECTED (Parameter Substitution / Mismatch)',
        desc: 'CPSA realized a shape where the POV strand and a peer strand bound different values (e.g. n != n-0) to the same role parameter.'
      },
      NOT_APPLICABLE_SINGLE_STRAND: {
        title: 'NOT_APPLICABLE_SINGLE_STRAND (Parameter Agreement)',
        desc: 'No multi-strand shapes were realized, so cross-strand parameter agreement could not be evaluated.'
      },
      NO_PEER_STRANDS: {
        title: 'NO_PEER_STRANDS (Parameter Agreement)',
        desc: 'No multi-strand shapes were realized, so cross-strand parameter agreement could not be established.'
      },
      NO_REFLECTION: {
        title: 'NO_REFLECTION (Role Reflection Check)',
        desc: 'Principals and roles are properly separated; no POV shape instantiated multiple strands of the same role or collapsed distinct principals.'
      },
      DISTINCT_PEERS: {
        title: 'DISTINCT_PEERS (Role Reflection Check)',
        desc: 'Principals are properly separated; no peer strand collapsed its own sender/receiver principal variables onto the same identity.'
      },
      SAME_ROLE_REFLECTION_DETECTED: {
        title: 'SAME_ROLE_REFLECTION_DETECTED (Same-Role / Symmetric Reflection)',
        desc: 'CPSA satisfied a POV query by instantiating multiple strands of the same role (symmetric reflection attack where an initiator talks to another initiator).'
      },
      ROLE_REFLECTION_POSSIBLE: {
        title: 'ROLE_REFLECTION_POSSIBLE (Self-Communication / Reflection)',
        desc: 'A realized shape unified two distinct principal variables inside a strand onto the same identity (A = B reflection attack).'
      },
      SECRECY_PROVED: {
        title: 'SECRECY_PROVED (Listener Secrecy Analysis)',
        desc: 'Every (deflistener secret) query realized 0 shapes (dead tree), proving the Dolev-Yao adversary cannot derive any protected secret.'
      },
      ALL_SECRETS_PROTECTED: {
        title: 'ALL_SECRETS_PROTECTED (Listener Secrecy Analysis)',
        desc: 'Every (deflistener secret) query realized 0 shapes (dead tree), proving the Dolev-Yao adversary cannot derive the protected secret.'
      },
      PARTIAL_SECRECY: {
        title: 'PARTIAL_SECRECY (Mixed Secrecy Verdict)',
        desc: 'Some (deflistener ...) queries realized 0 shapes (secret protected), while at least one listener realized >=1 shape (secret leaked).'
      },
      SECRECY_LEAK_DETECTED: {
        title: 'SECRECY_LEAK_DETECTED (Secrecy Breach)',
        desc: 'A (deflistener secret) query realized >=1 shape, meaning the adversary learned the secret in a valid protocol execution.'
      },
      NOT_APPLICABLE_NO_LISTENER: {
        title: 'NOT_APPLICABLE_NO_LISTENER (Secrecy Analysis)',
        desc: 'The protocol model did not include any (deflistener ...) secrecy queries (e.g. pure authentication or integrity protocol).'
      },
      NO_SECRECY_CLAIMS_TESTED: {
        title: 'NO_SECRECY_CLAIMS_TESTED (Secrecy Analysis)',
        desc: 'The protocol model did not include any (deflistener ...) secrecy queries (e.g. pure authentication or integrity protocol).'
      },
      ALL_SATISFIED: {
        title: 'ALL_SATISFIED (CPSA Security Goals)',
        desc: 'All declared (defgoal ...) security sentences were satisfied with 0 counterexamples.'
      },
      ALL_DEFGOALS_SATISFIED: {
        title: 'ALL_DEFGOALS_SATISFIED (CPSA Security Goals)',
        desc: 'All (defgoal ...) security sentences were satisfied with 0 counterexamples.'
      },
      COUNTEREXAMPLE_FOUND: {
        title: 'COUNTEREXAMPLE_FOUND (CPSA Security Goals)',
        desc: 'CPSA found at least one shape violating a declared (defgoal ...) security sentence.'
      },
      NO_EXPLICIT_DEFGOALS: {
        title: 'NO_EXPLICIT_DEFGOALS (Standard defskeleton Exploration)',
        desc: 'Model used standard (defskeleton ...) point-of-view queries; cpsa4sas extracted the strongest satisfied (defgoal ...) shape analysis sentences automatically.'
      },
      NO_DEFGOALS: {
        title: 'NO_DEFGOALS (Standard defskeleton Exploration)',
        desc: 'Model used standard (defskeleton ...) point-of-view queries; cpsa4sas extracted the strongest satisfied (defgoal ...) shape analysis sentences automatically.'
      }
    };

    let tooltipTimer = null;
    let activeTooltipTarget = null;

    function initHoverTooltips() {
      const tipEl = document.getElementById('rating-tooltip');
      const titleEl = document.getElementById('rating-tooltip-title');
      const descEl = document.getElementById('rating-tooltip-desc');
      if (!tipEl) return;

      function positionTooltip(clientX, clientY) {
        const pad = 14;
        const rect = tipEl.getBoundingClientRect();
        let left = clientX + pad;
        let top = clientY + pad;
        if (left + rect.width > window.innerWidth - 10) {
          left = Math.max(8, clientX - rect.width - pad);
        }
        if (top + rect.height > window.innerHeight - 10) {
          top = Math.max(8, clientY - rect.height - pad);
        }
        tipEl.style.left = `${left}px`;
        tipEl.style.top = `${top}px`;
      }

      document.addEventListener('mouseover', (e) => {
        const target = e.target.closest('[data-tooltip-key]');
        if (!target) return;
        const key = target.getAttribute('data-tooltip-key');
        const info = RATING_TOOLTIPS[key];
        if (!info) return;
        activeTooltipTarget = target;
        const startX = e.clientX;
        const startY = e.clientY;
        clearTimeout(tooltipTimer);
        tooltipTimer = setTimeout(() => {
          if (activeTooltipTarget !== target) return;
          titleEl.innerText = info.title;
          descEl.innerText = info.desc;
          tipEl.style.display = 'block';
          positionTooltip(startX, startY);
        }, 280);
      });

      document.addEventListener('mousemove', (e) => {
        if (tipEl.style.display === 'block') {
          positionTooltip(e.clientX, e.clientY);
        }
      });

      document.addEventListener('mouseout', (e) => {
        const target = e.target.closest('[data-tooltip-key]');
        if (target && target === activeTooltipTarget) {
          const related = e.relatedTarget ? e.relatedTarget.closest('[data-tooltip-key]') : null;
          if (related !== target) {
            clearTimeout(tooltipTimer);
            activeTooltipTarget = null;
            tipEl.style.display = 'none';
          }
        }
      });
    }
    initHoverTooltips();

    // =========================================================================
    // Part C: Compact Security Verdict Strip & Security Findings (CPSA) Sub-Tab
    // =========================================================================
    function verdictPillClass(val) {
      const v = String(val || '').toUpperCase();
      if ([
        'GOLD', 'VERIFIED', 'ALL_ROLES_EXECUTABLE', 'MUTUAL_MULTI_STRAND', 'MUTUAL_PEER_INTERACTION',
        'FULL_PARAMETER_AGREEMENT', 'FULL_AGREEMENT', 'NO_REFLECTION', 'DISTINCT_PEERS',
        'SECRECY_PROVED', 'ALL_SECRETS_PROTECTED', 'ALL_SATISFIED', 'ALL_DEFGOALS_SATISFIED'
      ].includes(v)) {
        return 'ok';
      }
      if ([
        'SILVER', 'UNILATERAL_AUTHENTICATED', 'NOT_APPLICABLE_NO_LISTENER', 'NO_SECRECY_CLAIMS_TESTED',
        'NO_EXPLICIT_DEFGOALS', 'NO_DEFGOALS'
      ].includes(v)) {
        return 'info';
      }
      if ([
        'BRONZE', 'PARTIAL', 'UNILATERAL_PARTIAL', 'CONDITIONAL_BRANCHED_AUTHENTICATION',
        'UNAUTHENTICATED_OR_CLEARTEXT_EXECUTABLE', 'LOCAL_ONLY', 'NOT_APPLICABLE_SINGLE_STRAND',
        'NO_PEER_STRANDS', 'PARTIAL_DEAD_ROLES', 'DEAD_ROLES_PRESENT', 'PARTIAL_SECRECY'
      ].includes(v)) {
        return 'warn';
      }
      if ([
        'REJECTED', 'FAILED', 'NO_ROLES_EXECUTABLE', 'ROLETRAN_FAILED', 'NON_EXECUTABLE',
        'NO_REALIZED_SHAPES', 'PRINCIPAL_DISAGREEMENT_MITM_OR_UKS', 'PARAMETER_DISAGREEMENT_DETECTED',
        'DISAGREEMENT_DETECTED', 'SAME_ROLE_REFLECTION_DETECTED', 'ROLE_REFLECTION_POSSIBLE',
        'SECRECY_LEAK_DETECTED', 'COUNTEREXAMPLE_FOUND'
      ].includes(v)) {
        return 'bad';
      }
      return '';
    }

    function setStripPill(elId, val) {
      const el = document.getElementById(elId);
      if (!el) return;
      const text = val || 'PENDING';
      el.innerText = text;
      el.className = `sec-pill ${verdictPillClass(text)}`;
      el.setAttribute('data-tooltip-key', text);
    }

    function renderSecurityVerdictStrip(qualityTier, secFindings) {
      const sf = secFindings || {};
      setStripPill('strip-quality', qualityTier || 'PENDING');
      setStripPill('strip-auth', sf.authentication_profile || 'PENDING');
      setStripPill('strip-agreement', sf.parameter_agreement_status || 'PENDING');
      setStripPill('strip-secrecy', sf.secrecy_status || 'PENDING');

      const anomEl = document.getElementById('strip-anomalies');
      if (anomEl) {
        if (!secFindings || Object.keys(sf).length === 0) {
          anomEl.innerText = '--';
          anomEl.className = 'sec-pill';
        } else {
          const cnt = Number(sf.anomalies_count ?? (sf.vulnerabilities_and_anomalies || []).length ?? 0);
          anomEl.innerText = `${cnt} Anomal${cnt === 1 ? 'y' : 'ies'}`;
          anomEl.className = `sec-pill ${cnt === 0 ? 'ok' : 'warn'}`;
        }
      }
    }

    function renderSecurityFindingsTab(payload) {
      const container = document.getElementById('security-findings-container');
      if (!container) return;
      const tab = payload.tab || {};
      const meta = payload.rfc_metadata || {};
      const qa = payload.quality_assessment || {};
      const sf = payload.security_findings || qa.security_findings || tab.security_findings || {};
      const shapesAnalysis = payload.shapes_analysis || {};
      const expTel = payload.exploration_telemetry || {};
      const rationale = payload.intake_rationale || meta.intake_rationale || tab.intake_rationale || '';
      const qTier = qa.quality_tier || tab.quality_tier || tab.status || 'PENDING';

      if (!sf || Object.keys(sf).length === 0) {
        container.innerHTML = `
          ${rationale ? `<div class="sec-banner-box"><strong style="color:var(--color-green);">Stage 1 Intake Rationale:</strong> Eligible: ${escapeHtml(rationale)}</div>` : ''}
          <div style="color:var(--text-muted);">No formal CPSA security findings recorded for this tab yet.</div>
        `;
        return;
      }

      const deadRoles = (sf.dead_roles || []).join(', ') || 'None';
      const multiPovs = (sf.multi_strand_pov_roles || []).join(', ') || 'None';
      const singlePovs = (sf.single_strand_pov_roles || []).join(', ') || 'None';
      const zeroPovs = (sf.unrealized_pov_roles || []).join(', ') || 'None';
      const protSecrets = (sf.protected_secrets || []).join(', ') || 'None';
      const leakSecrets = (sf.leaked_secrets || []).join(', ') || 'None';
      const anomalies = sf.vulnerabilities_and_anomalies || [];
      const disagreements = sf.disagreed_parameters || sf.parameter_disagreements || [];
      const reflections = sf.role_reflections || [];
      const authTests = sf.authentication_tests_summary || {};
      const sasList = sf.shape_analysis_sentences || sf.shape_analysis_sentences_defgoals || [];
      const perSkel = shapesAnalysis.per_preskeleton_outcomes || shapesAnalysis.per_preskeleton || [];

      const anomaliesHtml = anomalies.length === 0
        ? `<div class="sec-banner-box" style="border-left-color:var(--color-green);"><strong style="color:var(--color-green);">0 Formal Anomalies Detected:</strong> All POV roles interacted with distinct peer strands in full parameter agreement with no secrecy leaks.</div>`
        : `<div class="sec-banner-box" style="border-left-color:var(--color-yellow);">
             <strong style="color:var(--color-yellow);">Detected Protocol Vulnerabilities &amp; CPSA Anomalies (${anomalies.length}):</strong>
             <ul style="margin-top:5px; padding-left:18px; color:#e6edf3;">
               ${anomalies.map(a => `<li>${escapeHtml(a)}</li>`).join('')}
             </ul>
           </div>`;

      const skelRowsHtml = perSkel.length === 0
        ? `<tr><td colspan="7" style="color:var(--text-muted);">No per-preskeleton shape breakdown available.</td></tr>`
        : perSkel.map(sk => {
            const rawDis = sk.disagreed_parameters || sk.parameter_disagreements || [];
            const disList = rawDis.map(d =>
              `${d.pov_role || ''}->${d.peer_role || ''}:${d.param || d.parameter || ''}(${d.pov_val || d.pov_value || ''}!=${d.peer_val || d.peer_value || ''})`
            ).join('; ') || 'Full Agreement';
            const isSecList = Boolean(sk.is_secrecy_listener || sk.query_type === 'SECRECY_LISTENER' || (sk.listener_vars || sk.listener_terms || []).length > 0);
            const listVars = sk.listener_vars || sk.listener_terms || [];
            const realCount = sk.shapes_realized ?? sk.realized_shapes_count ?? 0;
            const hasMulti = Boolean(sk.has_multi_strand_shape || (sk.max_strands_in_any_shape || 0) >= 2);
            const hasSingle = Boolean(sk.has_single_strand_shape || (realCount > 0 && !hasMulti));
            const hasRefl = Boolean(sk.has_same_role_reflection || sk.has_self_reflection_split || (sk.role_reflections || []).length > 0);
            const refList = hasRefl
              ? (sk.has_same_role_reflection ? 'Same-Role Reflection' : 'Branched 1-Strand Split')
              : 'Distinct Peers';
            return `
              <tr>
                <td>#${escapeHtml(String(sk.root_label ?? sk.skeleton_label ?? ''))}</td>
                <td style="font-weight:700; color:var(--color-blue);">${escapeHtml(sk.pov_role || (isSecList ? 'Secrecy Listener' : 'POV'))}</td>
                <td>${isSecList ? `Listener (${escapeHtml(listVars.join(', '))})` : 'Participant POV'}</td>
                <td>${escapeHtml(String(realCount))}</td>
                <td>${hasMulti ? '<span style="color:var(--color-green);">YES (>=2 strands)</span>' : (hasSingle ? '<span style="color:var(--color-yellow);">Single-Strand Only</span>' : '<span style="color:var(--text-muted);">0 Shapes</span>')}</td>
                <td style="color:${rawDis.length ? 'var(--color-red)' : 'var(--color-green)'};">${escapeHtml(disList)}</td>
                <td style="color:${hasRefl ? 'var(--color-yellow)' : 'var(--color-green)'};">${escapeHtml(refList)}</td>
              </tr>
            `;
          }).join('');

      const sasBlockHtml = sasList.length > 0
        ? `<details class="snowball-details" style="margin-top:10px;" open>
             <summary>▸ CPSA4SAS Extracted Shape Analysis Sentences — (defgoal ...) (${sasList.length})</summary>
             <pre>${escapeHtml(sasList.join('\n\n'))}</pre>
           </details>`
        : '';

      container.innerHTML = `
        <div class="sec-banner-box">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <strong>${escapeHtml(tab.rfc_id || meta.rfc_id || '')} — ${escapeHtml(tab.protocol_name || meta.protocol_name || '')}</strong>
            <span class="sec-pill ${verdictPillClass(qTier)}" data-tooltip-key="${escapeHtml(qTier)}">Structural Quality: ${escapeHtml(qTier)}</span>
          </div>
          ${rationale ? `<div><strong style="color:var(--color-green);">Stage 1 Intake Rationale:</strong> Eligible: ${escapeHtml(rationale)}</div>` : ''}
          ${qa.tier_rationale ? `<div style="margin-top:3px; color:var(--text-muted);"><strong>Quality Tier Rationale:</strong> ${escapeHtml(qa.tier_rationale)}</div>` : ''}
        </div>

        ${anomaliesHtml}

        <div class="sec-grid">
          <div class="sec-card">
            <div class="sec-card-head">
              <span>1. Role Executability</span>
              <span class="sec-pill ${verdictPillClass(sf.role_executability)}" data-tooltip-key="${escapeHtml(sf.role_executability || '')}">${escapeHtml(sf.role_executability || 'N/A')}</span>
            </div>
            <div class="sec-card-body">
              <div>Dead / Uninstantiated Roles (${escapeHtml(String(sf.dead_roles_count ?? 0))}): <span style="color:var(--text-main);">${escapeHtml(deadRoles)}</span></div>
            </div>
          </div>

          <div class="sec-card">
            <div class="sec-card-head">
              <span>2. Authentication Profile</span>
              <span class="sec-pill ${verdictPillClass(sf.authentication_profile)}" data-tooltip-key="${escapeHtml(sf.authentication_profile || '')}">${escapeHtml(sf.authentication_profile || 'N/A')}</span>
            </div>
            <div class="sec-card-body">
              <div>Multi-Strand POVs: <span style="color:var(--color-green);">${escapeHtml(multiPovs)}</span></div>
              <div>Single-Strand POVs: <span style="color:var(--color-yellow);">${escapeHtml(singlePovs)}</span></div>
              <div>Unrealized POVs: <span style="color:var(--text-muted);">${escapeHtml(zeroPovs)}</span></div>
            </div>
          </div>

          <div class="sec-card">
            <div class="sec-card-head">
              <span>3. Parameter Agreement</span>
              <span class="sec-pill ${verdictPillClass(sf.parameter_agreement_status)}" data-tooltip-key="${escapeHtml(sf.parameter_agreement_status || '')}">${escapeHtml(sf.parameter_agreement_status || 'N/A')}</span>
            </div>
            <div class="sec-card-body">
              <div>Disagreed Parameters: <span style="color:${disagreements.length ? 'var(--color-red)' : 'var(--color-green)'};">${disagreements.length}</span></div>
              <div style="font-size:10px; color:var(--text-muted);">Hover badge for CPSA maplet agreement definition.</div>
            </div>
          </div>

          <div class="sec-card">
            <div class="sec-card-head">
              <span>4. Role Reflection Check</span>
              <span class="sec-pill ${verdictPillClass(sf.role_reflection_status)}" data-tooltip-key="${escapeHtml(sf.role_reflection_status || '')}">${escapeHtml(sf.role_reflection_status || 'N/A')}</span>
            </div>
            <div class="sec-card-body">
              <div>Self-Communication Instances: <span style="color:${reflections.length ? 'var(--color-yellow)' : 'var(--color-green)'};">${reflections.length}</span></div>
            </div>
          </div>

          <div class="sec-card">
            <div class="sec-card-head">
              <span>5. Secrecy &amp; Listeners</span>
              <span class="sec-pill ${verdictPillClass(sf.secrecy_status)}" data-tooltip-key="${escapeHtml(sf.secrecy_status || '')}">${escapeHtml(sf.secrecy_status || 'N/A')}</span>
            </div>
            <div class="sec-card-body">
              <div>Protected Secrets: <span style="color:var(--color-green);">${escapeHtml(protSecrets)}</span></div>
              <div>Leaked Secrets: <span style="color:${(sf.leaked_secrets || []).length ? 'var(--color-red)' : 'var(--text-muted)'};">${escapeHtml(leakSecrets)}</span></div>
            </div>
          </div>

          <div class="sec-card">
            <div class="sec-card-head">
              <span>6. Security Goals &amp; SAS</span>
              <span class="sec-pill ${verdictPillClass(sf.defgoal_satisfaction_status)}" data-tooltip-key="${escapeHtml(sf.defgoal_satisfaction_status || '')}">${escapeHtml(sf.defgoal_satisfaction_status || 'N/A')}</span>
            </div>
            <div class="sec-card-body">
              <div>Extracted cpsa4sas defgoals: <span style="color:var(--color-blue); font-weight:700;">${escapeHtml(String(sf.shape_analysis_sentences_count ?? sasList.length))}</span></div>
              <div>Cohort Tests: enc=${escapeHtml(String(authTests.encryption_tests ?? 0))} | nonce=${escapeHtml(String(authTests.nonce_tests ?? 0))} | chan=${escapeHtml(String(authTests.channel_tests ?? 0))}</div>
            </div>
          </div>
        </div>

        <div style="font-family:var(--mono); font-size:11px; font-weight:700; color:var(--text-main); margin-top:6px;">
          PER-PRESKELETON SHAPE &amp; AGREEMENT BREAKDOWN (FROM *_shapes.txt)
        </div>
        <table class="sec-table">
          <thead>
            <tr>
              <th>Skeleton</th>
              <th>POV Role</th>
              <th>Query Type</th>
              <th>Realized Shapes</th>
              <th>Peer Interaction</th>
              <th>Parameter Agreement</th>
              <th>Role Reflection</th>
            </tr>
          </thead>
          <tbody>${skelRowsHtml}</tbody>
        </table>
        ${sasBlockHtml}
      `;
    }

    // =========================================================================
    // Part D: Off-Main-Thread CSV Analytics (Live) via Inline Web Worker
    // =========================================================================
    let analyticsWorker = null;
    let latestCsvRows = [];
    let latestCsvHeaders = [];
    let latestCsvPath = '';
    let csvRefreshTimer = null;

    const WORKER_SOURCE = `
      function toNum(v) {
        const n = parseFloat(v);
        return isNaN(n) ? 0 : n;
      }
      function isTrue(v) {
        return String(v || '').trim().toLowerCase() === 'true';
      }
      self.onmessage = function(e) {
        const rows = (e.data && e.data.rows) || [];
        const totalRows = rows.length;
        const eligibleRows = rows.filter(r => isTrue(r.is_eligible));
        const ineligibleRows = rows.filter(r => !isTrue(r.is_eligible));
        const verifiedRows = eligibleRows.filter(r => (r.status || '').toUpperCase() === 'VERIFIED');
        const partialRows = eligibleRows.filter(r => (r.status || '').toUpperCase() === 'PARTIAL');
        const failedRows = eligibleRows.filter(r => (r.status || '').toUpperCase() === 'FAILED');
        const zeroShotRows = verifiedRows.filter(r => isTrue(r.zero_shot_passed));

        // Tier counts
        const tierCounts = { GOLD: 0, SILVER: 0, BRONZE: 0, REJECTED: 0 };
        eligibleRows.forEach(r => {
          const t = (r.quality_tier || 'REJECTED').toUpperCase();
          if (tierCounts[t] !== undefined) tierCounts[t]++;
          else tierCounts.REJECTED++;
        });

        // Intake Funnel
        const gateCounts = {
          'Tier 0 Header Filter': 0,
          'Stage 1c Applicability Gate': 0,
          'Stage 2 Verbatim Slice Gate': 0,
          'Eligible -> FAILED': failedRows.length,
          'Eligible -> PARTIAL': partialRows.length,
          'Eligible -> VERIFIED': verifiedRows.length
        };
        ineligibleRows.forEach(r => {
          const g = r.rejection_gate || 'Stage 1c Applicability Gate';
          if (gateCounts[g] !== undefined) gateCounts[g]++;
          else gateCounts['Stage 1c Applicability Gate']++;
        });

        // Security Findings counts on Verified/Eligible
        const authCounts = { MUTUAL_PEER_INTERACTION: 0, UNILATERAL_PARTIAL: 0, LOCAL_ONLY: 0, NO_REALIZED_SHAPES: 0 };
        const agreeCounts = { FULL_AGREEMENT: 0, DISAGREEMENT_DETECTED: 0, NO_PEER_STRANDS: 0 };
        const secCounts = { ALL_SECRETS_PROTECTED: 0, SECRECY_LEAK_DETECTED: 0, NO_SECRECY_CLAIMS_TESTED: 0 };
        const reflCounts = { DISTINCT_PEERS: 0, ROLE_REFLECTION_POSSIBLE: 0 };
        let anomalyProtocols = 0;

        eligibleRows.forEach(r => {
          const ap = (r.authentication_profile || '').toUpperCase();
          if (ap === 'MUTUAL_MULTI_STRAND' || ap === 'MUTUAL_PEER_INTERACTION') authCounts.MUTUAL_PEER_INTERACTION++;
          else if (ap === 'UNILATERAL_AUTHENTICATED' || ap === 'UNILATERAL_PARTIAL' || ap === 'CONDITIONAL_BRANCHED_AUTHENTICATION') authCounts.UNILATERAL_PARTIAL++;
          else if (ap === 'UNAUTHENTICATED_OR_CLEARTEXT_EXECUTABLE' || ap === 'LOCAL_ONLY') authCounts.LOCAL_ONLY++;
          else if (ap === 'NON_EXECUTABLE' || ap === 'NO_REALIZED_SHAPES') authCounts.NO_REALIZED_SHAPES++;

          const ag = (r.parameter_agreement_status || '').toUpperCase();
          if (ag === 'FULL_PARAMETER_AGREEMENT' || ag === 'FULL_AGREEMENT') agreeCounts.FULL_AGREEMENT++;
          else if (ag === 'PRINCIPAL_DISAGREEMENT_MITM_OR_UKS' || ag === 'PARAMETER_DISAGREEMENT_DETECTED' || ag === 'DISAGREEMENT_DETECTED') agreeCounts.DISAGREEMENT_DETECTED++;
          else if (ag === 'NOT_APPLICABLE_SINGLE_STRAND' || ag === 'NO_PEER_STRANDS') agreeCounts.NO_PEER_STRANDS++;

          const sc = (r.secrecy_status || '').toUpperCase();
          if (sc === 'SECRECY_PROVED' || sc === 'ALL_SECRETS_PROTECTED') secCounts.ALL_SECRETS_PROTECTED++;
          else if (sc === 'SECRECY_LEAK_DETECTED' || sc === 'PARTIAL_SECRECY') secCounts.SECRECY_LEAK_DETECTED++;
          else if (sc === 'NOT_APPLICABLE_NO_LISTENER' || sc === 'NO_SECRECY_CLAIMS_TESTED') secCounts.NO_SECRECY_CLAIMS_TESTED++;

          const rf = (r.role_reflection_status || '').toUpperCase();
          if (rf === 'NO_REFLECTION' || rf === 'DISTINCT_PEERS') reflCounts.DISTINCT_PEERS++;
          else if (rf === 'SAME_ROLE_REFLECTION_DETECTED' || rf === 'ROLE_REFLECTION_POSSIBLE') reflCounts.ROLE_REFLECTION_POSSIBLE++;

          if (toNum(r.anomalies_count) > 0) anomalyProtocols++;
        });

        // Completion steps histogram
        const stepBins = { '1 (Zero-Shot)': 0, '2-3 Steps': 0, '4-6 Steps': 0, '7-10 Steps': 0, '11+ Steps': 0, 'Unverified': 0 };
        eligibleRows.forEach(r => {
          if ((r.status || '').toUpperCase() !== 'VERIFIED') {
            stepBins['Unverified']++;
            return;
          }
          const st = toNum(r.total_completion_steps);
          if (st <= 1) stepBins['1 (Zero-Shot)']++;
          else if (st <= 3) stepBins['2-3 Steps']++;
          else if (st <= 6) stepBins['4-6 Steps']++;
          else if (st <= 10) stepBins['7-10 Steps']++;
          else stepBins['11+ Steps']++;
        });

        // Per-eligible protocol repair breakdown & cohort tests & scale
        const repairSeries = eligibleRows.slice(-25).map(r => ({
          label: r.rfc_id,
          protocol: r.protocol_name || r.rfc_id,
          schema: toNum(r.schema_repairs),
          roletran: toNum(r.roletran_repairs),
          solver: toNum(r.solver_repairs),
          searcher: toNum(r.searcher_invocations)
        }));

        const cohortSeries = eligibleRows.slice(-25).map(r => ({
          label: r.rfc_id,
          protocol: r.protocol_name || r.rfc_id,
          enc: toNum(r.encryption_tests_count),
          nonce: toNum(r.nonce_tests_count),
          chan: toNum(r.channel_tests_count)
        }));

        const scaleSeries = eligibleRows.slice(-25).map(r => ({
          label: r.rfc_id,
          protocol: r.protocol_name || r.rfc_id,
          roles: toNum(r.role_count),
          skeletons: toNum(r.preskeleton_count),
          anomalies: toNum(r.anomalies_count),
          sas: toNum(r.shape_analysis_sentences_count)
        }));

        // State-space scatter
        const stateScatter = eligibleRows.map(r => ({
          rfc_id: r.rfc_id,
          protocol: r.protocol_name || r.rfc_id,
          x: toNum(r.explored_skeletons_count),
          y: toNum(r.shapes_count),
          size: Math.max(4, Math.min(11, 3 + toNum(r.preskeleton_count) * 1.5)),
          tier: (r.quality_tier || 'REJECTED').toUpperCase()
        }));

        // Duration vs Slice Lines scatter
        const durationScatter = eligibleRows.map(r => ({
          rfc_id: r.rfc_id,
          protocol: r.protocol_name || r.rfc_id,
          x: toNum(r.sliced_lines_count),
          y: toNum(r.duration_seconds),
          tier: (r.quality_tier || 'REJECTED').toUpperCase()
        }));

        // Cost & Token breakdown by role
        const roleTotals = {
          Router: { cost: 0, tokens: 0 },
          Extraction: { cost: 0, tokens: 0 },
          Searcher: { cost: 0, tokens: 0 },
          Repair: { cost: 0, tokens: 0 }
        };
        let totalCostUsd = 0;
        let totalTokens = 0;
        rows.forEach(r => {
          roleTotals.Router.cost += toNum(r.router_cost_usd);
          roleTotals.Router.tokens += toNum(r.router_total_tokens);
          roleTotals.Extraction.cost += toNum(r.extraction_cost_usd);
          roleTotals.Extraction.tokens += toNum(r.extraction_total_tokens);
          roleTotals.Searcher.cost += toNum(r.query_cost_usd);
          roleTotals.Searcher.tokens += toNum(r.query_total_tokens);
          roleTotals.Repair.cost += toNum(r.repair_cost_usd);
          roleTotals.Repair.tokens += toNum(r.repair_total_tokens);
          totalCostUsd += toNum(r.total_cost_usd);
          totalTokens += toNum(r.total_tokens);
        });

        // Cumulative timeline over rows
        let cumVerified = 0;
        let cumGold = 0;
        let cumCost = 0;
        const timeline = rows.map((r, idx) => {
          if ((r.status || '').toUpperCase() === 'VERIFIED') cumVerified++;
          if ((r.quality_tier || '').toUpperCase() === 'GOLD') cumGold++;
          cumCost += toNum(r.total_cost_usd);
          return {
            index: idx + 1,
            rfc_id: r.rfc_id,
            verified: cumVerified,
            gold: cumGold,
            cost: cumCost
          };
        });

        const avgSteps = eligibleRows.length
          ? (eligibleRows.reduce((a, r) => a + toNum(r.total_completion_steps), 0) / eligibleRows.length)
          : 0;
        const avgRepairs = eligibleRows.length
          ? (eligibleRows.reduce((a, r) => a + toNum(r.total_repairs), 0) / eligibleRows.length)
          : 0;
        const avgEligDur = eligibleRows.length
          ? (eligibleRows.reduce((a, r) => a + toNum(r.duration_seconds), 0) / eligibleRows.length)
          : 0;
        const avgIneligDur = ineligibleRows.length
          ? (ineligibleRows.reduce((a, r) => a + toNum(r.duration_seconds), 0) / ineligibleRows.length)
          : 0;

        self.postMessage({
          kpis: {
            totalRows,
            eligibleCount: eligibleRows.length,
            ineligibleCount: ineligibleRows.length,
            verifiedCount: verifiedRows.length,
            zeroShotCount: zeroShotRows.length,
            passRate: eligibleRows.length ? ((verifiedRows.length / eligibleRows.length) * 100).toFixed(1) : '0.0',
            zeroShotRate: eligibleRows.length ? ((zeroShotRows.length / eligibleRows.length) * 100).toFixed(1) : '0.0',
            tierCounts,
            fullAgreeCount: agreeCounts.FULL_AGREEMENT,
            secretsProtectedCount: secCounts.ALL_SECRETS_PROTECTED,
            anomalyProtocols,
            avgSteps: avgSteps.toFixed(2),
            avgRepairs: avgRepairs.toFixed(2),
            totalCostUsd: totalCostUsd.toFixed(4),
            avgVerifiedCost: verifiedRows.length ? (totalCostUsd / verifiedRows.length).toFixed(4) : '0.0000',
            totalTokens,
            avgEligDur: avgEligDur.toFixed(1),
            avgIneligDur: avgIneligDur.toFixed(2)
          },
          gateCounts,
          tierCounts,
          securityMatrix: { authCounts, agreeCounts, secCounts, reflCounts },
          stepBins,
          repairSeries,
          cohortSeries,
          scaleSeries,
          stateScatter,
          durationScatter,
          roleTotals,
          timeline
        });
      };
    `;

    function initAnalyticsWorker() {
      if (analyticsWorker) return;
      try {
        const blob = new Blob([WORKER_SOURCE], { type: 'application/javascript' });
        analyticsWorker = new Worker(URL.createObjectURL(blob));
        analyticsWorker.onmessage = (e) => {
          renderCsvAnalyticsResult(e.data);
        };
      } catch (err) {
        analyticsWorker = null;
      }
    }
    initAnalyticsWorker();

    function scheduleCsvAnalyticsRefresh() {
      clearTimeout(csvRefreshTimer);
      csvRefreshTimer = setTimeout(() => {
        const analyticsTab = document.getElementById('tab-analytics');
        if (analyticsTab && analyticsTab.style.display !== 'none') {
          refreshCsvAnalytics(false);
        }
      }, 280);
    }

    function refreshCsvAnalytics(force) {
      fetch('/api/csv')
        .then(r => r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`)))
        .then(data => {
          latestCsvRows = data.rows || [];
          latestCsvHeaders = data.headers || [];
          latestCsvPath = data.csv_path || '';
          const lbl = document.getElementById('analytics-csv-label');
          if (lbl) {
            const shortPath = latestCsvPath ? latestCsvPath.split('/').slice(-2).join('/') : 'pipeline_runs.csv';
            lbl.innerText = `${shortPath} (${latestCsvRows.length} rows, ${latestCsvHeaders.length} columns)`;
            lbl.title = latestCsvPath;
          }
          if (analyticsWorker) {
            analyticsWorker.postMessage({ rows: latestCsvRows });
          }
          renderCustomExplorerUI();
          renderCsvTableUI();
        })
        .catch(() => {});
    }

    function svgHorizontalBars(entries, colors) {
      const vals = entries.map(e => e[1]);
      const maxVal = Math.max(1, ...vals);
      const w = 360;
      const rowH = 24;
      const h = Math.max(150, entries.length * rowH + 16);
      let rowsSvg = '';
      entries.forEach(([label, count], i) => {
        const y = 10 + i * rowH;
        const barW = Math.round((count / maxVal) * 165);
        const col = (colors && colors[i % colors.length]) || '#58a6ff';
        rowsSvg += `
          <text x="4" y="${y + 13}" fill="#c9d1d9" font-family="monospace" font-size="10">${escapeHtml(String(label).slice(0, 24))}</text>
          <rect x="158" y="${y + 3}" width="${Math.max(2, barW)}" height="13" fill="${col}" rx="2" />
          <text x="${164 + Math.max(2, barW)}" y="${y + 13}" fill="#8b949e" font-family="monospace" font-size="10">${count}</text>
        `;
      });
      return `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}">${rowsSvg}</svg>`;
    }

    function svgStackedVerticalBars(items, keys, colors, legendLabels) {
      if (!items || !items.length) {
        return `<div style="color:var(--text-muted); font-family:var(--mono); font-size:11px;">Waiting for eligible RFC runs...</div>`;
      }
      const w = 380;
      const h = 185;
      const plotH = 130;
      const baseY = 145;
      const totals = items.map(it => keys.reduce((s, k) => s + (Number(it[k]) || 0), 0));
      const maxTot = Math.max(1, ...totals);
      const slotW = Math.max(10, Math.min(34, Math.floor((w - 40) / items.length)));

      let barsSvg = `<line x1="28" y1="${baseY}" x2="${w - 8}" y2="${baseY}" stroke="#30363d" />`;
      items.forEach((it, idx) => {
        const x = 32 + idx * slotW;
        let curY = baseY;
        keys.forEach((k, kIdx) => {
          const v = Number(it[k]) || 0;
          if (v <= 0) return;
          const bh = Math.max(2, Math.round((v / maxTot) * plotH));
          curY -= bh;
          barsSvg += `<rect x="${x}" y="${curY}" width="${Math.max(6, slotW - 4)}" height="${bh}" fill="${colors[kIdx]}"><title>${escapeHtml(it.label)} (${escapeHtml(it.protocol || '')}) - ${legendLabels[kIdx]}: ${v}</title></rect>`;
        });
        barsSvg += `<text x="${x + 3}" y="${baseY + 11}" fill="#8b949e" font-family="monospace" font-size="8.5" transform="rotate(28 ${x + 3} ${baseY + 11})">${escapeHtml(String(it.label).replace('RFC', ''))}</text>`;
      });

      let legSvg = '';
      legendLabels.forEach((lbl, i) => {
        const lx = 8 + i * 92;
        legSvg += `<rect x="${lx}" y="4" width="8" height="8" fill="${colors[i]}" /><text x="${lx + 11}" y="11" fill="#8b949e" font-family="monospace" font-size="9">${escapeHtml(lbl)}</text>`;
      });
      return `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}">${legSvg}${barsSvg}</svg>`;
    }

    function svgScatterPlot(points, xLabel, yLabel) {
      if (!points || !points.length) {
        return `<div style="color:var(--text-muted); font-family:var(--mono); font-size:11px;">Waiting for eligible RFC runs...</div>`;
      }
      const w = 380;
      const h = 185;
      const padL = 38, padR = 14, padT = 14, padB = 28;
      const plotW = w - padL - padR;
      const plotH = h - padT - padB;
      const maxX = Math.max(1, ...points.map(p => Number(p.x) || 0));
      const maxY = Math.max(1, ...points.map(p => Number(p.y) || 0));
      const tierCol = { GOLD: '#3fb950', SILVER: '#58a6ff', BRONZE: '#d29922', REJECTED: '#f85149', VERIFIED: '#3fb950', PARTIAL: '#d29922', FAILED: '#f85149' };

      let dots = `
        <line x1="${padL}" y1="${padT}" x2="${padL}" y2="${padT + plotH}" stroke="#30363d" />
        <line x1="${padL}" y1="${padT + plotH}" x2="${padL + plotW}" y2="${padT + plotH}" stroke="#30363d" />
        <text x="${padL + plotW / 2}" y="${h - 4}" fill="#8b949e" font-family="monospace" font-size="9.5" text-anchor="middle">${escapeHtml(xLabel)} (max ${maxX.toFixed(0)})</text>
        <text x="10" y="${padT + plotH / 2}" fill="#8b949e" font-family="monospace" font-size="9.5" text-anchor="middle" transform="rotate(-90 10 ${padT + plotH / 2})">${escapeHtml(yLabel)}</text>
      `;
      points.forEach(p => {
        const cx = padL + ((Number(p.x) || 0) / maxX) * plotW;
        const cy = padT + plotH - ((Number(p.y) || 0) / maxY) * plotH;
        const r = p.size || 5;
        const c = tierCol[p.tier] || '#58a6ff';
        dots += `<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${r}" fill="${c}" fill-opacity="0.82" stroke="#0d1117" stroke-width="1"><title>${escapeHtml(p.rfc_id)} (${escapeHtml(p.protocol || '')})\n${xLabel}: ${p.x} | ${yLabel}: ${p.y} | Tier: ${p.tier}</title></circle>`;
      });
      return `<svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}">${dots}</svg>`;
    }

    function svgTimelineChart(timeline) {
      if (!timeline || !timeline.length) {
        return `<div style="color:var(--text-muted); font-family:var(--mono); font-size:11px;">No CSV rows recorded yet.</div>`;
      }
      const w = 380, h = 185, padL = 34, padR = 14, padT = 18, padB = 24;
      const plotW = w - padL - padR;
      const plotH = h - padT - padB;
      const n = Math.max(1, timeline.length - 1);
      const maxV = Math.max(1, timeline[timeline.length - 1].verified, timeline[timeline.length - 1].gold);

      const verPts = timeline.map((pt, i) => {
        const x = padL + (i / n) * plotW;
        const y = padT + plotH - (pt.verified / maxV) * plotH;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      }).join(' ');
      const goldPts = timeline.map((pt, i) => {
        const x = padL + (i / n) * plotW;
        const y = padT + plotH - (pt.gold / maxV) * plotH;
        return `${x.toFixed(1)},${y.toFixed(1)}`;
      }).join(' ');

      return `
        <svg viewBox="0 0 ${w} ${h}" width="100%" height="${h}">
          <rect x="8" y="3" width="8" height="8" fill="#58a6ff" /><text x="20" y="10" fill="#8b949e" font-family="monospace" font-size="9">Cumulative Verified (${timeline[timeline.length - 1].verified})</text>
          <rect x="180" y="3" width="8" height="8" fill="#3fb950" /><text x="192" y="10" fill="#8b949e" font-family="monospace" font-size="9">Cumulative GOLD (${timeline[timeline.length - 1].gold})</text>
          <line x1="${padL}" y1="${padT}" x2="${padL}" y2="${padT + plotH}" stroke="#30363d" />
          <line x1="${padL}" y1="${padT + plotH}" x2="${padL + plotW}" y2="${padT + plotH}" stroke="#30363d" />
          <polyline fill="none" stroke="#58a6ff" stroke-width="2" points="${verPts}" />
          <polyline fill="none" stroke="#3fb950" stroke-width="2" points="${goldPts}" />
          <text x="${padL + plotW / 2}" y="${h - 4}" fill="#8b949e" font-family="monospace" font-size="9.5" text-anchor="middle">RFC Run Sequence (1 .. ${timeline.length})</text>
        </svg>
      `;
    }

    function renderCsvAnalyticsResult(d) {
      if (!d || !d.kpis) return;
      const k = d.kpis;
      const kpiEl = document.getElementById('analytics-kpis');
      if (kpiEl) {
        kpiEl.innerHTML = `
          <div class="kpi-card">
            <div class="kpi-label">Total RFCs in CSV</div>
            <div class="kpi-val">${k.totalRows}</div>
            <div class="kpi-sub"><span style="color:var(--color-green);">${k.eligibleCount} Eligible</span> | ${k.ineligibleCount} Filtered</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Verification Pass Rate</div>
            <div class="kpi-val" style="color:var(--color-green);">${k.passRate}%</div>
            <div class="kpi-sub">${k.verifiedCount}/${k.eligibleCount} Verified | ${k.zeroShotRate}% Zero-Shot</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Quality Tiers (Structural)</div>
            <div class="kpi-val"><span style="color:#3fb950;" data-tooltip-key="GOLD">${k.tierCounts.GOLD}G</span> / <span style="color:#58a6ff;" data-tooltip-key="SILVER">${k.tierCounts.SILVER}S</span> / <span style="color:#d29922;" data-tooltip-key="BRONZE">${k.tierCounts.BRONZE}B</span></div>
            <div class="kpi-sub">${k.tierCounts.REJECTED} Rejected</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">CPSA Security Verdicts</div>
            <div class="kpi-val" style="color:var(--color-blue);">${k.fullAgreeCount} Agree</div>
            <div class="kpi-sub">${k.secretsProtectedCount} Secrecy OK | ${k.anomalyProtocols} w/ Anomalies</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Avg Steps / Repairs</div>
            <div class="kpi-val">${k.avgSteps} steps</div>
            <div class="kpi-sub">Avg ${k.avgRepairs} repairs per eligible RFC</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Cumulative CSV Cost</div>
            <div class="kpi-val" style="color:var(--color-green);">$${k.totalCostUsd}</div>
            <div class="kpi-sub">$${k.avgVerifiedCost} / verified protocol</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Total Tokens Consumed</div>
            <div class="kpi-val">${Number(k.totalTokens || 0).toLocaleString()}</div>
            <div class="kpi-sub">Across Router, Extraction, Searcher, Repair</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Avg Synthesis Time</div>
            <div class="kpi-val">${k.avgEligDur}s</div>
            <div class="kpi-sub">Eligible avg (${k.avgIneligDur}s Ineligible avg)</div>
          </div>
        `;
      }

      const chartsEl = document.getElementById('analytics-charts');
      if (!chartsEl) return;

      const sm = d.securityMatrix;
      const secEntries = [
        ['Auth: Mutual Peer', sm.authCounts.MUTUAL_PEER_INTERACTION],
        ['Auth: Unilateral/Local', sm.authCounts.UNILATERAL_PARTIAL + sm.authCounts.LOCAL_ONLY],
        ['Agree: Full Agreement', sm.agreeCounts.FULL_AGREEMENT],
        ['Agree: Disagreement', sm.agreeCounts.DISAGREEMENT_DETECTED],
        ['Secrecy: Protected', sm.secCounts.ALL_SECRETS_PROTECTED],
        ['Secrecy: Leak Found', sm.secCounts.SECRECY_LEAK_DETECTED],
        ['Peers: Distinct', sm.reflCounts.DISTINCT_PEERS],
        ['Peers: Reflection', sm.reflCounts.ROLE_REFLECTION_POSSIBLE]
      ];

      const roleCostEntries = Object.entries(d.roleTotals || {}).map(([role, obj]) => [
        `${role} ($${obj.cost.toFixed(4)})`,
        Math.round(obj.tokens / 1000)
      ]);

      chartsEl.innerHTML = `
        <div class="chart-card">
          <div class="chart-title"><span>1. Intake Funnel &amp; Gate Breakdown</span><span class="chart-sub">All CSV Rows</span></div>
          <div class="chart-svg-wrap">${svgHorizontalBars(Object.entries(d.gateCounts), ['#8b949e', '#d29922', '#bc8cff', '#f85149', '#d29922', '#3fb950'])}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>2. Structural Quality Tier Distribution</span><span class="chart-sub">Decoupled from Flaws</span></div>
          <div class="chart-svg-wrap">${svgHorizontalBars(Object.entries(d.tierCounts), ['#3fb950', '#58a6ff', '#d29922', '#f85149'])}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>3. CPSA 4.4.9 Formal Security Verdicts</span><span class="chart-sub">Agreement / Secrecy / Reflection</span></div>
          <div class="chart-svg-wrap">${svgHorizontalBars(secEntries, ['#3fb950', '#d29922', '#3fb950', '#f85149', '#3fb950', '#f85149', '#58a6ff', '#d29922'])}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>4. Self-Healing Convergence Steps</span><span class="chart-sub">total_completion_steps</span></div>
          <div class="chart-svg-wrap">${svgHorizontalBars(Object.entries(d.stepBins), ['#3fb950', '#58a6ff', '#bc8cff', '#d29922', '#f0883e', '#f85149'])}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>5. Repair Effort by Stage (Per Protocol)</span><span class="chart-sub">Schema / Roletran / Solver / RAG</span></div>
          <div class="chart-svg-wrap">${svgStackedVerticalBars(d.repairSeries, ['schema', 'roletran', 'solver', 'searcher'], ['#bc8cff', '#d29922', '#f85149', '#58a6ff'], ['Schema', 'Roletran', 'Solver', 'RAG'])}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>6. State-Space Complexity Scatter</span><span class="chart-sub">Explored Skeletons vs Shapes</span></div>
          <div class="chart-svg-wrap">${svgScatterPlot(d.stateScatter, 'Explored Skeletons', 'Realized Shapes')}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>7. CPSA Cohort Authentication Tests</span><span class="chart-sub">enc-test / nonce-test / chan-test</span></div>
          <div class="chart-svg-wrap">${svgStackedVerticalBars(d.cohortSeries, ['enc', 'nonce', 'chan'], ['#58a6ff', '#3fb950', '#bc8cff'], ['enc-test', 'nonce-test', 'chan-test'])}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>8. LLM Role Cost &amp; Token Share (kTok)</span><span class="chart-sub">Router / Extract / Search / Repair</span></div>
          <div class="chart-svg-wrap">${svgHorizontalBars(roleCostEntries, ['#bc8cff', '#58a6ff', '#d29922', '#3fb950'])}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>9. Synthesis Duration vs RFC Slice Lines</span><span class="chart-sub">Sliced Lines vs Seconds</span></div>
          <div class="chart-svg-wrap">${svgScatterPlot(d.durationScatter, 'Sliced Lines', 'Duration (s)')}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>10. Live Cumulative Verification Timeline</span><span class="chart-sub">Verified &amp; GOLD Growth</span></div>
          <div class="chart-svg-wrap">${svgTimelineChart(d.timeline)}</div>
        </div>

        <div class="chart-card">
          <div class="chart-title"><span>11. Protocol Scale &amp; Extracted SAS Goals</span><span class="chart-sub">Roles / Skeletons / SAS / Anomalies</span></div>
          <div class="chart-svg-wrap">${svgStackedVerticalBars(d.scaleSeries, ['roles', 'skeletons', 'sas', 'anomalies'], ['#58a6ff', '#3fb950', '#bc8cff', '#f85149'], ['Roles', 'Skeletons', 'SAS Goals', 'Anomalies'])}</div>
        </div>
      `;
    }

    const NUMERIC_CSV_COLS = [
      'sliced_lines_count', 'role_count', 'preskeleton_count', 'scm_lines_count',
      'shapes_count', 'explored_skeletons_count', 'total_completion_steps', 'total_repairs',
      'roletran_repairs', 'solver_repairs', 'searcher_invocations', 'encryption_tests_count',
      'nonce_tests_count', 'channel_tests_count', 'shape_analysis_sentences_count',
      'anomalies_count', 'disagreed_parameters_count', 'duration_seconds', 'total_cost_usd', 'total_tokens'
    ];

    function renderCustomExplorerUI() {
      const wrap = document.getElementById('analytics-custom-explorer');
      if (!wrap) return;
      const xSel = document.getElementById('custom-x-col')?.value || 'scm_lines_count';
      const ySel = document.getElementById('custom-y-col')?.value || 'duration_seconds';
      const eligOnly = document.getElementById('custom-elig-only') ? document.getElementById('custom-elig-only').checked : true;

      const sourceRows = eligOnly
        ? latestCsvRows.filter(r => String(r.is_eligible || '').toLowerCase() === 'true')
        : latestCsvRows;

      const pts = sourceRows.map(r => ({
        rfc_id: r.rfc_id,
        protocol: r.protocol_name || r.rfc_id,
        x: parseFloat(r[xSel] || 0) || 0,
        y: parseFloat(r[ySel] || 0) || 0,
        tier: (r.quality_tier || r.status || 'REJECTED').toUpperCase()
      }));

      wrap.innerHTML = `
        <div class="chart-card">
          <div class="chart-title">
            <span>12. Custom 67-Column X/Y Scatter Explorer</span>
            <div style="display:flex; gap:6px; align-items:center;">
              <span class="chart-sub">X:</span>
              <select id="custom-x-col" class="ctrl-select" onchange="renderCustomExplorerUI()">
                ${NUMERIC_CSV_COLS.map(c => `<option value="${c}" ${c === xSel ? 'selected' : ''}>${c}</option>`).join('')}
              </select>
              <span class="chart-sub">Y:</span>
              <select id="custom-y-col" class="ctrl-select" onchange="renderCustomExplorerUI()">
                ${NUMERIC_CSV_COLS.map(c => `<option value="${c}" ${c === ySel ? 'selected' : ''}>${c}</option>`).join('')}
              </select>
              <label style="font-size:10px; color:var(--text-muted); display:inline-flex; align-items:center; gap:3px;">
                <input type="checkbox" id="custom-elig-only" ${eligOnly ? 'checked' : ''} onchange="renderCustomExplorerUI()" /> Eligible Only
              </label>
            </div>
          </div>
          <div class="chart-svg-wrap">${svgScatterPlot(pts, xSel, ySel)}</div>
        </div>
      `;
    }

    function renderCsvTableUI() {
      const sec = document.getElementById('analytics-table-section');
      if (!sec) return;
      const q = (document.getElementById('csv-table-search')?.value || '').trim().toLowerCase();
      const filtered = latestCsvRows.filter(r => {
        if (!q) return true;
        return (
          (r.rfc_id || '').toLowerCase().includes(q) ||
          (r.protocol_name || '').toLowerCase().includes(q) ||
          (r.quality_tier || '').toLowerCase().includes(q) ||
          (r.status || '').toLowerCase().includes(q) ||
          (r.authentication_profile || '').toLowerCase().includes(q) ||
          (r.parameter_agreement_status || '').toLowerCase().includes(q) ||
          (r.secrecy_status || '').toLowerCase().includes(q) ||
          (r.error_message || '').toLowerCase().includes(q)
        );
      });

      const keyCols = [
        'rfc_id', 'is_eligible', 'status', 'quality_tier', 'protocol_name',
        'total_completion_steps', 'shapes_count', 'authentication_profile',
        'parameter_agreement_status', 'secrecy_status', 'anomalies_count',
        'duration_seconds', 'total_cost_usd', 'error_message'
      ];

      const bodyHtml = filtered.slice(0, 200).map(r => `
        <tr>
          <td style="font-weight:700; color:var(--color-blue);">${escapeHtml(r.rfc_id || '')}</td>
          <td>${escapeHtml(r.is_eligible || '')}</td>
          <td>${escapeHtml(r.status || '')}</td>
          <td><span class="sec-pill ${verdictPillClass(r.quality_tier)}" data-tooltip-key="${escapeHtml(r.quality_tier || '')}">${escapeHtml(r.quality_tier || '')}</span></td>
          <td>${escapeHtml(r.protocol_name || '')}</td>
          <td>${escapeHtml(r.total_completion_steps || '')}</td>
          <td>${escapeHtml(r.shapes_count || '')}</td>
          <td><span class="sec-pill ${verdictPillClass(r.authentication_profile)}" data-tooltip-key="${escapeHtml(r.authentication_profile || '')}">${escapeHtml(r.authentication_profile || '-')}</span></td>
          <td><span class="sec-pill ${verdictPillClass(r.parameter_agreement_status)}" data-tooltip-key="${escapeHtml(r.parameter_agreement_status || '')}">${escapeHtml(r.parameter_agreement_status || '-')}</span></td>
          <td><span class="sec-pill ${verdictPillClass(r.secrecy_status)}" data-tooltip-key="${escapeHtml(r.secrecy_status || '')}">${escapeHtml(r.secrecy_status || '-')}</span></td>
          <td>${escapeHtml(r.anomalies_count || '0')}</td>
          <td>${escapeHtml(r.duration_seconds || '')}s</td>
          <td>$${escapeHtml(r.total_cost_usd || '0')}</td>
          <td style="max-width:340px; white-space:normal; word-break:break-word; color:var(--text-muted);">${escapeHtml(r.error_message || '')}</td>
        </tr>
      `).join('');

      sec.innerHTML = `
        <div class="chart-card">
          <div class="chart-title">
            <span>LIVE CSV LEDGER EXPLORER (${filtered.length} matching / ${latestCsvRows.length} total rows)</span>
            <input type="text" id="csv-table-search" class="ctrl-input" style="width:240px;" placeholder="Filter CSV rows (RFC, tier, verdict, rationale)..." value="${escapeHtml(q)}" oninput="renderCsvTableUI()" />
          </div>
          <div style="overflow-x:auto; max-height:340px;">
            <table class="sec-table">
              <thead>
                <tr>${keyCols.map(c => `<th>${escapeHtml(c)}</th>`).join('')}</tr>
              </thead>
              <tbody>${bodyHtml || '<tr><td colspan="14" style="color:var(--text-muted);">No matching CSV rows.</td></tr>'}</tbody>
            </table>
          </div>
        </div>
      `;
    }

    // =========================================================================
    // Initial Bootstrap & Named-Event SSE Subscription (Zero Polling Spam!)
    // =========================================================================
    fetch('/api/models')
      .then(r => r.ok ? r.json() : null)
      .then(cfg => {
        if (!cfg) return;
        defaultModelCfg = Object.assign(defaultModelCfg, cfg);
        if (cfg.router_model) document.getElementById('step-1-model').innerText = cfg.router_model;
        if (cfg.extraction_model) document.getElementById('step-2-model').innerText = cfg.extraction_model;
        if (cfg.repair_model) {
          const qm = cfg.query_model ? ` + ${cfg.query_model.split('/').pop()}` : '';
          document.getElementById('step-5-model').innerText = `${cfg.repair_model}${qm}`;
          document.getElementById('step-6-model').innerText = `cpsa4 + ${cfg.repair_model}`;
        }
      })
      .catch(() => {});

    function syncInitialState() {
      fetch('/api/tabs')
        .then(r => {
          if (!r.ok) throw new Error('legacy server');
          return r.json();
        })
        .then(overview => {
          isServerLive = Boolean(overview.is_live);
          liveActiveRfcId = overview.active_rfc_id;
          liveActiveTabIndex = overview.active_tab_index;

          const runDirEl = document.getElementById('run-dir-badge');
          if (runDirEl) {
            const rd = overview.run_directory || (isServerLive ? 'Live Session' : 'Offline Replay');
            runDirEl.innerText = rd.split('/').slice(-2).join('/');
            runDirEl.title = rd;
          }

          acceptedTabs = [];
          acceptedTabsByIndex.clear();
          (overview.accepted_tabs || []).forEach(t => {
            acceptedTabs.push(t);
            acceptedTabsByIndex.set(t.tab_index, t);
          });
          acceptedTabs.sort((a, b) => a.tab_index - b.tab_index);
          if (overview.batch_cost_telemetry && Object.keys(overview.batch_cost_telemetry).length > 0) {
            renderCostTelemetry(null, overview.batch_cost_telemetry);
          }
          updateFilteredButtonCount(overview.filtered_total || 0);
          recomputeVisibleTabs();
          updateLivePinButton();

          refreshCsvAnalytics(false);
          if (!isServerLive) {
            if (acceptedTabs.length > 0) {
              selectNumberedTab(acceptedTabs[0].tab_index);
            } else {
              setDiagnosisBadge('Replay Loaded (0 Accepted Tabs)', 'normal');
            }
          } else if (viewMode === 'live') {
            return fetch('/api/active')
              .then(r => r.json())
              .then(state => {
                if (state && Array.isArray(state.events)) {
                  state.events.forEach(evt => renderEventIntoViewport(evt, true));
                }
              });
          }
        })
        .catch(() => {
          // Graceful fallback if connected to an older in-memory server without /api/tabs
          fetch('/api/history')
            .then(r => r.json())
            .then(events => {
              if (Array.isArray(events)) events.forEach(e => renderEventIntoViewport(e, true));
            })
            .catch(() => {});
        });
    }

    syncInitialState();

    // Real-time Server-Sent Events: listen on all named event types so frames fire in <1ms
    const sse = new EventSource('/api/events');
    const SSE_EVENT_TYPES = [
      'pipeline_started',
      'stage_started',
      'compiler_check_started',
      'stage_completed',
      'slice_ready',
      'rag_retrieval',
      'repair_attempt',
      'stage_failed',
      'pipeline_completed',
      'pipeline_failed',
      'tab_accepted',
      'tab_updated',
      'rfc_filtered',
      'cost_updated',
      'csv_updated',
      'message'
    ];
    SSE_EVENT_TYPES.forEach(evtName => {
      sse.addEventListener(evtName, function(e) {
        try {
          const evt = JSON.parse(e.data);
          handleIncomingBusEvent(evt);
        } catch (err) {}
      });
    });
  </script>
</body>
</html>
```

---
