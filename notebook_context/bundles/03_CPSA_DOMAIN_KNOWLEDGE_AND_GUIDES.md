# CPSA 4.4.9 Core Rules, Compiler Diagnostics & Official Manuals

> Tier 1/3 Domain Reference — Zero-hallucination CPSA 4.4.9 core operational rules (`refrences/cpsa_kb/01_core_rules/`), JSON AST to Scheme S-expression mapping, exhaustive compiler/solver diagnostic catalog, and the 5 consolidated official MITRE manuals (`refrences/cpsa_kb/02_manuals/`).

*Generated: 2026-11-03 21:53:56 UTC · Git: `main` @ `8b5b88a14002` · Tier: Tier 1/3 — Domain Reference Documentation & Modeling Guides · Files: 13 · Estimated Tokens: ~175,802*

## Table of Contents

- [`refrences/cpsa_kb/01_core_rules/00_json_ast_to_cpsa_scheme_mapping.md`](#refrencescpsa-kb01-core-rules00-json-ast-to-cpsa-scheme-mappingmd)
- [`refrences/cpsa_kb/01_core_rules/01_algebra_sorts_and_operators.md`](#refrencescpsa-kb01-core-rules01-algebra-sorts-and-operatorsmd)
- [`refrences/cpsa_kb/01_core_rules/02_roletran_and_executability_rules.md`](#refrencescpsa-kb01-core-rules02-roletran-and-executability-rulesmd)
- [`refrences/cpsa_kb/01_core_rules/03_declarations_origination_and_assumptions.md`](#refrencescpsa-kb01-core-rules03-declarations-origination-and-assumptionsmd)
- [`refrences/cpsa_kb/01_core_rules/04_skeletons_3pov_and_security_goals.md`](#refrencescpsa-kb01-core-rules04-skeletons-3pov-and-security-goalsmd)
- [`refrences/cpsa_kb/01_core_rules/05_channels_state_and_macros.md`](#refrencescpsa-kb01-core-rules05-channels-state-and-macrosmd)
- [`refrences/cpsa_kb/01_core_rules/06_termination_and_anti_snowballing.md`](#refrencescpsa-kb01-core-rules06-termination-and-anti-snowballingmd)
- [`refrences/cpsa_kb/01_core_rules/07_compiler_and_solver_error_catalog.md`](#refrencescpsa-kb01-core-rules07-compiler-and-solver-error-catalogmd)
- [`refrences/cpsa_kb/02_manuals/01_CPSA4_User_Manual.md`](#refrencescpsa-kb02-manuals01-cpsa4-user-manualmd)
- [`refrences/cpsa_kb/02_manuals/02_Role_Translations_Manual.md`](#refrencescpsa-kb02-manuals02-role-translations-manualmd)
- [`refrences/cpsa_kb/02_manuals/03_CPSA_Primer.md`](#refrencescpsa-kb02-manuals03-cpsa-primermd)
- [`refrences/cpsa_kb/02_manuals/04_CPSA_Goals_and_Security_Manual.md`](#refrencescpsa-kb02-manuals04-cpsa-goals-and-security-manualmd)
- [`refrences/cpsa_kb/02_manuals/05_CPSA_Specification_and_User_Guide.md`](#refrencescpsa-kb02-manuals05-cpsa-specification-and-user-guidemd)

---

### `refrences/cpsa_kb/01_core_rules/00_json_ast_to_cpsa_scheme_mapping.md`

*sha256:`2f735a9f8ff9` · 379 lines · 22.3 KB (~5,695 tokens) · lang:`markdown`*

````markdown
# CPSA 4.4.9 JSON AST to Scheme S-Expression Mapping Reference

This document defines the exact, bidirectional structural mapping between the strongly-typed Pydantic Intermediate Representation (`CPSAProtocolSpecification` in `src/intermediate_representation/protocol_syntax_tree.py`) and the canonical MITRE CPSA 4.4.9 Scheme S-expressions (`.scm`) emitted by `src/code_generation/cpsa_json_serializer.py` and `src/code_generation/cpsa_scheme_emitter.py` via the official `cpsa4json` compiler.

---

## Compilation Pipeline Architecture: Pydantic AST to MITRE Scheme

The RFC-LLM code generation pipeline translates a validated `CPSAProtocolSpecification` Pydantic model into a formal `.scm` specification through a deterministic 3-step serialization pipeline:

1. **AST Normalization & Scoped Validation (`protocol_syntax_tree.py`)**:
   - Enforces strict keyword scoping across top-level specifications, roles (`CPSAProtocolRole`), trace events (`CPSATraceEvent`), and point-of-view preskeletons (`CPSAPreskeleton`) in accordance with MITRE CPSA 4.4.9 Manual Tables 10.1 through 10.6.
   - Sanitizes all symbolic identifiers via `sanitize_cpsa_symbol()`, converting spaces and periods (`.`) into hyphens (`-`) and stripping characters outside `[a-zA-Z0-9+\-*/<=>!?$:%_&~^]` to prevent `cpsa4json: Bad char in atom` errors.
   - Desugars foreign cryptographic operators (`aenc` $\to$ `enc`, `senc` $\to$ `enc`, `sign` $\to$ `enc`, `mac`/`hmac` $\to$ `hash`) via `desugar_term_tree()`.
   - Normalizes asymmetric key terms via `normalize_cpsa_term()`: unwraps `["pubk", k]` $\to$ `k` and `["privk", k]` $\to$ `["invk", k]` when `k` has sort `akey`, repairs reversed 2-argument `["pubk", name_var, tag_str]` $\to$ `["pubk", "\"tag_str\"", name_var]`, and expands bare `"gen"` / `"one"` inside Diffie-Hellman operators (`exp`, `mul`, `rec`) into `["gen"]` / `["one"]`.
2. **JSON S-Expression Serialization (`cpsa_json_serializer.py`)**:
   - Invokes `spec.to_cpsa_json_payload()`, returning a list of top-level JSON S-expression arrays (`["herald", ...]`, `["defprotocol", ...]`, and `["defskeleton", ...]`).
   - Serializes each top-level JSON array onto a separate double-newline-delimited line via `serialize_to_cpsa_json_string()`.
3. **Native Binary Emission (`cpsa_scheme_emitter.py` + `cpsa4json`)**:
   - Pipes the newline-delimited JSON string into `~/.cabal/bin/cpsa4json`, which parses the JSON AST and emits properly formatted MITRE CPSA 4.4.9 Scheme S-expressions to `<protocol_stem>.scm`.

---

## Dual-Gate Architecture: Raw `cpsa4` vs. RFC-LLM `cpsa4roletran` + `cpsa4` Pipeline

Understanding the structural difference between hand-written `cpsa4`-only `.scm` models and RFC-LLM's dual-gate `.scm` specifications is critical for generating valid `CPSAProtocolSpecification` JSON:

1. **Why Raw `cpsa4` Guides Recommend Empty Roles**:
   - In standalone `cpsa4` shape analysis (e.g., `SKILL.md` and Manual Chapter 6.3), authors often omit `(uniq-orig ...)` and `(non-orig ...)` from `(defrole ...)` and place all assumptions exclusively inside `(defskeleton ...)` so that individual skeletons can vary compromise assumptions.
   - Furthermore, standalone `cpsa4` does not require channel variables (`chan`), `(inputs ...)`, or `(outputs ...)` inside `(defrole ...)`.
2. **Why RFC-LLM Requires Annotated Roles AND Packed Preskeletons**:
   - RFC-LLM enforces a **Pre-Flight Executability Gate** (`src/verification_engine/roletran_executability_gate.py`) prior to running the full `cpsa4` solver.
   - For protocols using the `basic` message algebra, the gate executes `~/.cabal/bin/cpsa4roletran` (`CPSA.Roletran`).
   - `cpsa4roletran` mathematically proves that every role is **procedurally executable** (can be compiled into a real Rust/C procedure `defproc` where every sent message is constructible from known inputs and prior receptions, and every received message is destructible using held decryption keys).
   - **Mandatory `CPSAProtocolRole` Fields for `cpsa4roletran`**:
     * Every `send` and `recv` event in `CPSAProtocolRole.trace` **must** specify a channel variable (`channel`, default `"ch"`, declared with sort `"chan"`).
     * `CPSAProtocolRole.inputs` **must** list all channels used in the trace plus all initial parameters, identities, and pre-shared or private keys required to construct outbound messages or decrypt inbound messages.
     * `CPSAProtocolRole.unique_originating` **must** list all fresh nonces or keys (sorts `text`, `data`, `skey`, `akey`) generated by that role, or `cpsa4roletran` will reject the role with `Cannot build <term>` when the role attempts to transmit the fresh value without receiving it or taking it as an input.
     * `CPSAProtocolRole.outputs` **must** list the return values produced upon completing the role trace (disjoint from `inputs`).
   - **Mandatory `CPSAPreskeleton` Fields for `cpsa4` Shape Analysis**:
     * In addition to the role annotations, each `CPSAPreskeleton` in `CPSAProtocolSpecification.skeletons` **must also** populate `non_originating`, `pen_non_originating`, `unique_originating`, `unique_generated`, and `listeners` (for secrecy skeletons) so that `cpsa4` has explicit scenario-level origination assumptions and `ensure_three_point_of_view_skeletons()` can construct self-contained 3-POV verification queries.

---

## Side-by-Side Schema Mapping Table: Pydantic JSON AST to Scheme S-Expressions

| Pydantic Model & Field | JSON AST Type | Emitted Scheme S-Expression | Scope & Serialization Rules |
|---|---|---|---|
| `CPSAProtocolSpecification.herald_comment` | `Optional[str]` | `(herald "<comment>" [(algebra diffie-hellman)])` | Always emitted as the first top-level form. Automatically appends `["algebra", "diffie-hellman"]` when `message_algebra == "diffie-hellman"`. |
| `CPSAProtocolSpecification.protocol_name` | `str` | `(defprotocol <id> <alg> ...)` | Sanitized via `sanitize_cpsa_symbol()`. |
| `CPSAProtocolSpecification.message_algebra` | `Literal["basic", "diffie-hellman"]` | `basic` or `diffie-hellman` | Second token of `(defprotocol <id> <alg> ...)`. |
| `CPSAProtocolSpecification.roles` | `List[CPSAProtocolRole]` | `(defrole <role_name> ...)` | Nested directly inside `(defprotocol ...)`. |
| `CPSAProtocolSpecification.primary_secrecy_goals` | `List[CPSATerm]` | `(deflistener <term>)` (in Skeleton 3) | Consumed by `ensure_three_point_of_view_skeletons()` to synthesize the dedicated Secrecy POV skeleton. |
| `CPSAProtocolSpecification.skeletons` | `List[CPSAPreskeleton]` | `(defskeleton <proto_id> ...)` | Emitted as top-level sibling forms **after** `(defprotocol ...)` closes. Never nested inside `defprotocol`. |
| `CPSAProtocolRole.role_name` | `str` | `(defrole <role_name> ...)` | Sanitized symbol identifying the role. |
| `CPSAProtocolRole.variables` | `List[CPSAVariableDeclaration]` | `(vars (<id>+ <sort>)*)` | Grouped by `sort.value` in insertion order. Any channel used in `trace` is automatically added to sort `chan` if omitted. |
| `CPSAProtocolRole.trace` | `List[CPSATraceEvent]` | `(trace (<dir> <chan_or_loc>? <term>)+)` | Ordered list of `send`, `recv`, `load`, or `stor` events. |
| `CPSAProtocolRole.unique_originating` | `List[CPSATerm]` | `(uniq-orig <term>+)` | Filtered to terms whose variables appear in `trace`. Variables of sort `rndx`/`expt` are automatically moved to `(uniq-gen ...)`. |
| `CPSAProtocolRole.unique_generated` | `List[CPSATerm]` | `(uniq-gen <term>+)` | Filtered to terms whose variables appear in `trace`. Required for `rndx` Diffie-Hellman exponents. |
| `CPSAProtocolRole.non_originating` | `List[CPSATerm]` | `(non-orig <term>+)` | Normalized via `normalize_cpsa_term()`. |
| `CPSAProtocolRole.pen_non_originating` | `List[CPSATerm]` | `(pen-non-orig <term>+)` | Normalized via `normalize_cpsa_term()`. |
| `CPSAProtocolRole.confidential_channels` | `List[str]` | `(conf <chan>+)` | Declares confidential channels in role scope. |
| `CPSAProtocolRole.authenticated_channels` | `List[str]` | `(auth <chan>+)` | Declares authenticated channels in role scope. |
| `CPSAProtocolRole.gen_st` | `List[CPSATerm]` | `(gen-st <term>+)` | Generated (non-initial) state values in stateful protocols. |
| `CPSAProtocolRole.facts` | `List[List[Any]]` | `(facts (<pred> <term>*)*)` | Logical facts asserted by the role. |
| `CPSAProtocolRole.inputs` | `List[CPSATerm]` | `(inputs <term>+)` | Automatically prepends all trace channels when `inputs` or `outputs` is non-empty. Strips any term in `uniq-orig`/`uniq-gen`, any compound non-key term, and any term whose variables do not appear in `trace`. |
| `CPSAProtocolRole.outputs` | `List[CPSATerm]` | `(outputs <term>+)` | Strips any term present in `inputs` and any term whose variables do not appear in `trace`. |
| `CPSAPreskeleton.protocol_name` | `str` | `(defskeleton <protocol_name> ...)` | Must match `CPSAProtocolSpecification.protocol_name`. |
| `CPSAPreskeleton.variables` | `List[CPSAVariableDeclaration]` | `(vars (<id>+ <sort>)*)` | Skeleton-scoped variable declarations grouped by sort. |
| `CPSAPreskeleton.strands` | `List[CPSAStrandInstance]` | `(defstrandmax <role_name> (<rvar> <svar>)*)` | Emits `defstrandmax` with maplet bindings `[role_var, skel_term]`. |
| `CPSAPreskeleton.listeners` | `List[CPSATerm]` | `(deflistener <term>)` | Emits one `(deflistener <term>)` per item. Must be `[]` in pure POV skeletons (Skeletons 1 & 2) and populated in Secrecy Skeleton 3. |
| `CPSAPreskeleton.non_originating` | `List[CPSATerm]` | `(non-orig <term>+)` | Uncompromised keys carried nowhere in the bundle. |
| `CPSAPreskeleton.pen_non_originating` | `List[CPSATerm]` | `(pen-non-orig <term>+)` | Secrets never originated by the penetrator. |
| `CPSAPreskeleton.unique_originating` | `List[CPSATerm]` | `(uniq-orig <term>+)` | Fresh nonces/keys. Any `rndx`/`expt` variable is automatically redirected to `(uniq-gen ...)`. |
| `CPSAPreskeleton.unique_generated` | `List[CPSATerm]` | `(uniq-gen <term>+)` | Fresh Diffie-Hellman exponents (`rndx`). |
| `CPSAPreskeleton.precedes` | `List[List[List[int]]]` | `(precedes ((<s1> <n1>) (<s2> <n2>))+)` | Causal ordering constraints between strand nodes. |
| `CPSAPreskeleton.leadsto` | `List[List[List[int]]]` | `(leadsto ((<s1> <n1>) (<s2> <n2>))+)` | State transition ordering constraints. |
| `CPSAPreskeleton.priority` | `List[List[Any]]` | `(priority ((<s> <n>) <int>)+)` | Node solving priority overrides. |
| `CPSAPreskeleton.facts` | `List[List[Any]]` | `(facts (<pred> <term>*)*)` | Relational facts (e.g., `[["neq", "client_id", "server_id"]]`). |

---

## Scoped Keyword Separation Invariants (`_FORBIDDEN_IN_*`)

`src/intermediate_representation/protocol_syntax_tree.py` enforces strict grammatical firewalls via Pydantic `@model_validator(mode="before")` hooks so that keywords from one scope can never leak into another:

1. **Forbidden in `CPSAProtocolRole` (`_FORBIDDEN_IN_ROLE`)**:
   - `defskeleton`, `defstrand`, `defstrandmax`, `deflistener`, `precedes`, `leadsto`, `goal`, `goals`, `strands`, `listeners`.
   - Violating this raises `ValueError: Keyword '<key>' is a preskeleton-only keyword (MITRE CPSA 4.4.9 Tables 10.1 & 10.6) and is strictly forbidden inside CPSAProtocolRole (defrole).`
2. **Forbidden in `CPSAPreskeleton` (`_FORBIDDEN_IN_SKELETON`)**:
   - `defrole`, `trace`, `inputs`, `outputs`, `params`, `returns`, `assume`, `ind-zero`, `role_name`.
   - Violating this raises `ValueError: Keyword '<key>' is a role-only keyword (MITRE CPSA 4.4.9 Tables 10.1 & 10.6) and is strictly forbidden inside CPSAPreskeleton (defskeleton).`
3. **Forbidden in `CPSATraceEvent` (`_FORBIDDEN_IN_EVENT`)**:
   - Any role-only or skeleton-only keyword, plus `vars`, `variables`, `strands`, `listeners`, `unique_originating`, `non_originating`.
4. **Forbidden in `CPSATerm` (`CPSA_STRUCTURAL_NON_TERM_KEYWORDS`)**:
   - Structural keywords (`defprotocol`, `defrole`, `defskeleton`, `trace`, `send`, `recv`, `load`, `stor`, `vars`, `inputs`, `outputs`, `uniq-orig`, `non-orig`, etc.) are strictly forbidden as leading operators in a `CPSATerm` list.

---

## Trace Event & Operator Serialization Mapping

Every `CPSATraceEvent` serializes via `to_cpsa_json()` according to its `direction` (`send`, `recv`, `load`, `stor`):

- **Channel Communication Events (`send` / `recv`)**:
  - JSON AST:
    ```json
    {
      "direction": "send",
      "channel": "handshake_channel",
      "message_term": ["enc", "client_random", "client_identity", ["pubk", "server_identity"]],
      "description": "Client sends encrypted nonce and identity to server"
    }
    ```
  - Intermediate JSON Array (`to_cpsa_json()`):
    ```json
    ["send", "handshake_channel", ["enc", "client_random", "client_identity", ["pubk", "server_identity"]]]
    ```
  - Emitted `.scm` via `cpsa4json`:
    ```scheme
    (send handshake_channel (enc client_random client_identity (pubk server_identity)))
    ```

- **Stateful Memory Events (`load` / `stor`)**:
  - Per MITRE CPSA 4.4.9 Table 10.1 (`event <- (dir term? term)`), `load` and `stor` take an optional memory location (`locn`) and a message term—never both a channel and a location.
  - JSON AST:
    ```json
    {
      "direction": "stor",
      "location": "key_registry_loc",
      "message_term": ["cat", "server_identity", "session_key"],
      "description": "Store negotiated session key into device registry"
    }
    ```
  - Emitted `.scm` via `cpsa4json`:
    ```scheme
    (stor key_registry_loc (cat server_identity session_key))
    ```

---

## Complete Side-by-Side Example: `CPSAProtocolSpecification` JSON vs. Emitted `.scm`

### Input Pydantic JSON (`CPSAProtocolSpecification`)

```json
{
  "protocol_name": "nsl_handshake",
  "message_algebra": "basic",
  "herald_comment": "Needham-Schroeder-Lowe Public-Key Handshake Verification Suite",
  "primary_secrecy_goals": ["client_nonce", "server_nonce"],
  "roles": [
    {
      "role_name": "client",
      "description": "Initiator client authenticating with server",
      "variables": [
        {"name": "handshake_channel", "sort": "chan", "description": "Transport channel", "rfc_field": "Transport"},
        {"name": "client_identity", "sort": "name", "description": "Client principal ID", "rfc_field": "ClientID"},
        {"name": "server_identity", "sort": "name", "description": "Server principal ID", "rfc_field": "ServerID"},
        {"name": "client_nonce", "sort": "text", "description": "Fresh client challenge", "rfc_field": "NonceC"},
        {"name": "server_nonce", "sort": "text", "description": "Fresh server challenge", "rfc_field": "NonceS"}
      ],
      "trace": [
        {
          "direction": "send",
          "channel": "handshake_channel",
          "message_term": ["enc", "client_nonce", "client_identity", ["pubk", "server_identity"]]
        },
        {
          "direction": "recv",
          "channel": "handshake_channel",
          "message_term": ["enc", "client_nonce", "server_nonce", "server_identity", ["pubk", "client_identity"]]
        },
        {
          "direction": "send",
          "channel": "handshake_channel",
          "message_term": ["enc", "server_nonce", ["pubk", "server_identity"]]
        }
      ],
      "unique_originating": ["client_nonce"],
      "inputs": [
        "handshake_channel",
        "client_identity",
        "server_identity",
        ["privk", "client_identity"],
        ["pubk", "client_identity"],
        ["pubk", "server_identity"]
      ],
      "outputs": ["client_nonce", "server_nonce"]
    },
    {
      "role_name": "server",
      "description": "Responder server authenticating client",
      "variables": [
        {"name": "handshake_channel", "sort": "chan", "description": "Transport channel", "rfc_field": "Transport"},
        {"name": "client_identity", "sort": "name", "description": "Client principal ID", "rfc_field": "ClientID"},
        {"name": "server_identity", "sort": "name", "description": "Server principal ID", "rfc_field": "ServerID"},
        {"name": "client_nonce", "sort": "text", "description": "Client challenge", "rfc_field": "NonceC"},
        {"name": "server_nonce", "sort": "text", "description": "Fresh server challenge", "rfc_field": "NonceS"}
      ],
      "trace": [
        {
          "direction": "recv",
          "channel": "handshake_channel",
          "message_term": ["enc", "client_nonce", "client_identity", ["pubk", "server_identity"]]
        },
        {
          "direction": "send",
          "channel": "handshake_channel",
          "message_term": ["enc", "client_nonce", "server_nonce", "server_identity", ["pubk", "client_identity"]]
        },
        {
          "direction": "recv",
          "channel": "handshake_channel",
          "message_term": ["enc", "server_nonce", ["pubk", "server_identity"]]
        }
      ],
      "unique_originating": ["server_nonce"],
      "inputs": [
        "handshake_channel",
        "server_identity",
        ["privk", "server_identity"],
        ["pubk", "server_identity"],
        ["pubk", "client_identity"]
      ],
      "outputs": ["client_nonce", "server_nonce"]
    }
  ],
  "skeletons": [
    {
      "protocol_name": "nsl_handshake",
      "variables": [
        {"name": "handshake_channel", "sort": "chan"},
        {"name": "client_identity", "sort": "name"},
        {"name": "server_identity", "sort": "name"},
        {"name": "client_nonce", "sort": "text"},
        {"name": "server_nonce", "sort": "text"}
      ],
      "strands": [
        {
          "role_name": "client",
          "variable_bindings": {
            "handshake_channel": "handshake_channel",
            "client_identity": "client_identity",
            "server_identity": "server_identity",
            "client_nonce": "client_nonce",
            "server_nonce": "server_nonce"
          }
        }
      ],
      "non_originating": [["privk", "client_identity"], ["privk", "server_identity"]],
      "unique_originating": ["client_nonce"],
      "listeners": [],
      "comment": "Client Point of View"
    },
    {
      "protocol_name": "nsl_handshake",
      "variables": [
        {"name": "handshake_channel", "sort": "chan"},
        {"name": "client_identity", "sort": "name"},
        {"name": "server_identity", "sort": "name"},
        {"name": "client_nonce", "sort": "text"},
        {"name": "server_nonce", "sort": "text"}
      ],
      "strands": [
        {
          "role_name": "server",
          "variable_bindings": {
            "handshake_channel": "handshake_channel",
            "client_identity": "client_identity",
            "server_identity": "server_identity",
            "client_nonce": "client_nonce",
            "server_nonce": "server_nonce"
          }
        }
      ],
      "non_originating": [["privk", "client_identity"], ["privk", "server_identity"]],
      "unique_originating": ["server_nonce"],
      "listeners": [],
      "comment": "Server Point of View"
    },
    {
      "protocol_name": "nsl_handshake",
      "variables": [
        {"name": "handshake_channel", "sort": "chan"},
        {"name": "client_identity", "sort": "name"},
        {"name": "server_identity", "sort": "name"},
        {"name": "client_nonce", "sort": "text"},
        {"name": "server_nonce", "sort": "text"}
      ],
      "strands": [
        {
          "role_name": "client",
          "variable_bindings": {
            "handshake_channel": "handshake_channel",
            "client_identity": "client_identity",
            "server_identity": "server_identity",
            "client_nonce": "client_nonce",
            "server_nonce": "server_nonce"
          }
        }
      ],
      "non_originating": [["privk", "client_identity"], ["privk", "server_identity"]],
      "unique_originating": ["client_nonce"],
      "listeners": ["client_nonce"],
      "comment": "Secrecy Point of View: Listener on client_nonce"
    }
  ]
}
```

### Resulting MITRE Scheme Output (`.scm`) Emitted by `cpsa4json`

```scheme
(herald "Needham-Schroeder-Lowe Public-Key Handshake Verification Suite")

(defprotocol nsl_handshake basic
  (defrole client
    (vars (handshake_channel chan) (client_identity server_identity name)
      (client_nonce server_nonce text))
    (trace
      (send handshake_channel
        (enc client_nonce client_identity (pubk server_identity)))
      (recv handshake_channel
        (enc client_nonce server_nonce server_identity
          (pubk client_identity)))
      (send handshake_channel
        (enc server_nonce (pubk server_identity))))
    (uniq-orig client_nonce)
    (inputs handshake_channel client_identity server_identity
      (privk client_identity) (pubk client_identity)
      (pubk server_identity))
    (outputs client_nonce server_nonce))
  (defrole server
    (vars (handshake_channel chan) (client_identity server_identity name)
      (client_nonce server_nonce text))
    (trace
      (recv handshake_channel
        (enc client_nonce client_identity (pubk server_identity)))
      (send handshake_channel
        (enc client_nonce server_nonce server_identity
          (pubk client_identity)))
      (recv handshake_channel
        (enc server_nonce (pubk server_identity))))
    (uniq-orig server_nonce)
    (inputs handshake_channel server_identity (privk server_identity)
      (pubk server_identity) (pubk client_identity))
    (outputs client_nonce server_nonce)))

(defskeleton nsl_handshake
  (vars (handshake_channel chan) (client_identity server_identity name)
    (client_nonce server_nonce text))
  (defstrandmax client (handshake_channel handshake_channel)
    (client_identity client_identity) (server_identity server_identity)
    (client_nonce client_nonce) (server_nonce server_nonce))
  (non-orig (privk client_identity) (privk server_identity))
  (uniq-orig client_nonce)
  (comment "Client Point of View"))

(defskeleton nsl_handshake
  (vars (handshake_channel chan) (client_identity server_identity name)
    (client_nonce server_nonce text))
  (defstrandmax server (handshake_channel handshake_channel)
    (client_identity client_identity) (server_identity server_identity)
    (client_nonce client_nonce) (server_nonce server_nonce))
  (non-orig (privk client_identity) (privk server_identity))
  (uniq-orig server_nonce)
  (comment "Server Point of View"))

(defskeleton nsl_handshake
  (vars (handshake_channel chan) (client_identity server_identity name)
    (client_nonce server_nonce text))
  (defstrandmax client (handshake_channel handshake_channel)
    (client_identity client_identity) (server_identity server_identity)
    (client_nonce client_nonce) (server_nonce server_nonce))
  (deflistener client_nonce)
  (non-orig (privk client_identity) (privk server_identity))
  (uniq-orig client_nonce)
  (comment "Secrecy Point of View: Listener on client_nonce"))
```
````

---

### `refrences/cpsa_kb/01_core_rules/01_algebra_sorts_and_operators.md`

*sha256:`c6f1f795c971` · 135 lines · 14.1 KB (~3,574 tokens) · lang:`markdown`*

````markdown
# CPSA 4.4.9 Order-Sorted Message Algebras, Sorts, and Operators Reference

This document provides the complete formal specification of the MITRE CPSA 4.4.9 order-sorted message algebras (`basic` and `diffie-hellman`), grounded directly in Manual Chapter 4, Chapter 10 (Tables 10.1 through 10.6, Equation 10.1), `src/intermediate_representation/algebraic_sorts.py`, and `src/intermediate_representation/cpsa_grammar.py`.

---

## Order-Sorted Message Algebras: `basic` vs. `diffie-hellman`

CPSA models cryptographic messages using an order-sorted quotient term algebra generated by variable declarations $X$. Every protocol definition `(defprotocol <id> <alg> ...)` and JSON `CPSAProtocolSpecification.message_algebra` selects one of two algebras:

1. **`basic` Algebra (Tables 10.2 & 10.3)**:
   - Free order-sorted algebra over symmetric encryption, asymmetric public/private key pairs, one-way hashes, and pairing/concatenation, modulo the single asymmetric key inversion equation:
     $$(a^{-1})^{-1} = a \quad \text{for } a : \text{akey}$$
   - Supported by **both** `cpsa4roletran` (procedural executability verifier) and `cpsa4` (shape analyzer).
   - Diffie-Hellman sorts (`rndx`, `expt`, `base`) and Diffie-Hellman operators (`bltk`, `exp`, `gen`, `mul`, `rec`, `one`) are **strictly forbidden** under `basic` algebra (`validate_algebra_consistency()` in `protocol_syntax_tree.py`).

2. **`diffie-hellman` Algebra (Tables 10.4 & 10.5)**:
   - Extends the `basic` algebra with an Abelian exponent group and modular exponentiation over a generator `(gen)`, modulo the equational theory:
     $$\begin{aligned}
     (a^{-1})^{-1} &= a \quad (a : \text{akey}) \\
     \text{bltk}(a, b) &= \text{bltk}(b, a) \quad (a, b : \text{name}) \\
     xy &= yx, \quad x(yz) = (xy)z \quad (x, y, z : \text{expt}) \\
     x \cdot 1 &= x, \quad x \cdot i(x) = 1 \quad (x : \text{expt}) \\
     h^1 &= h, \quad (h^x)^y = h^{(xy)} \quad (h : \text{base},\; x, y : \text{expt})
     \end{aligned}$$
   - **Herald Requirement**: Any `.scm` file containing a `diffie-hellman` protocol **must** include `(algebra diffie-hellman)` inside its top-level `(herald ...)` form, or `cpsa4` aborts with `Expecting terms in algebra basic`. (`CPSAProtocolSpecification.to_cpsa_json_payload()` injects `["algebra", "diffie-hellman"]` into the herald automatically).

---

## Complete Order-Sorted Hierarchy (`CPSASortEnum`)

Every variable declared in `(vars ...)` belongs to a sort within the CPSA 4.4.9 subsort lattice:

```
                               mesg (Universal Top Message Sort)
     ┌───────┬───────┬───────┬───┴───┬───────┬───────┬───────┬───────┬───────┐
   name    text    data     tag    skey    akey    expt    chan    locn     dev
                                                     │
                                                   rndx
```

### 1. Basic Message Algebra Sorts (Table 10.2 — `CPSA_BASIC_VARIABLE_SORTS`)

| Sort (`CPSASortEnum`) | Super-Sort | Formal Role & Cryptographic Semantics | Acquisition & Usage Constraints |
|---|---|---|---|
| `name` | `mesg` | Principal identities, agents, servers, authorities (e.g., `client_identity`, `server_identity`). | Required input sort for `(pubk name)`, `(privk name)`, `(ltk n1 n2)`, and `(bltk n1 n2)`. Passing any non-`name` sort triggers `Expecting a name` or `Terms in role not well formed`. |
| `text` | `mesg` | Plaintext nonces, random challenges, timestamps, cleartext fields. | Standard sort for fresh challenges in `uniq-orig`. |
| `data` | `mesg` | Opaque byte payloads, premaster secrets, cookies, session tokens. | Recommended by CPSA Primer (§12) for fresh secrets or random parameters that must never unify with `text` fields. |
| `skey` | `mesg` | Symmetric encryption keys and session keys. | Self-inverse ($k^{-1} = k$). Any standalone variable used as a symmetric encryption key in `(enc ... k)` **must** be declared `skey` (if declared `data` or `text`, `cpsa4roletran` rejects with `Cannot build`). |
| `akey` | `mesg` | Unnamed asymmetric public or private keys. | Inverted via `(invk k)` where `((invk (invk k))) = k`. **Never** pass an `akey` variable to `pubk` or `privk`; use `k` for the public key and `["invk", k]` for the private key. |
| `tag` | `mesg` | Constant protocol tag atoms. | Quoted string literals `"tag"` in terms automatically inhabit `tag < mesg`. |
| `chan` | `mesg` | Communication channels for `(send ch m)` and `(recv ch m)`. | Mandatory in `cpsa4roletran` roles; every channel in `trace` must also appear in `inputs`. Can be annotated with `auth` and `conf`. |
| `locn` | `mesg` | Mutable memory storage cells / registers for `(load loc m)` and `(stor loc m)`. | Used exclusively in stateful protocols (Chapter 8.2). |
| `dev` | `mesg` | Hardware device identifiers. | Used with `locn` (e.g., `(cat d l)`) to bind registers to specific physical devices. |
| `mesg` | Top (`mesg`) | Universal top message sort unifying with any message term. | **Acquisition Rule**: Any variable of sort `mesg` in a role **must** first appear in a carried position of an inbound `recv` event (`Role not well formed: variable [...] not acquired`). **Equation 10.1**: **Never** use a `mesg` variable as the encryption key in `(enc ...)` (`Algebra.inv: Cannot invert a variable of sort mesg`). |

### 2. Diffie-Hellman Message Algebra Sorts (Table 10.4 — `CPSA_DH_ONLY_VARIABLE_SORTS`)

| Sort (`CPSASortEnum`) | Super-Sort | Formal Role & Cryptographic Semantics | Acquisition & Origination Constraints |
|---|---|---|---|
| `rndx` | `expt < mesg` | Atomic, freshly chosen Diffie-Hellman random private exponents. | **Must first appear in a `send` event** (`Expts must first be received, rndxs first sent`). **Must be declared in `uniq-gen` (`unique_generated`), NEVER `uniq-orig`** (`uniq-orig [...] doesn't originate`). Only `rndx` exponents may appear as bare exponents outside `(exp ...)` (`Disallowed bare exponent`). |
| `expt` | `mesg` | Compound exponent expressions or unconstrained received exponents. | **Must first appear in a `recv` event** (`Expts must first be received, rndxs first sent`). Never declare a locally generated fresh exponent as `expt`. |
| `base` | `mesg` | Diffie-Hellman group elements (e.g., `(exp (gen) x)`). | **DEPRECATED in `(vars ...)` in CPSA 4.4.8+**: Declaring `(vars (b base))` in CPSA 4.4.8+ triggers `mkVar: Variables of sort base are now deprecated`. Instead, represent received DH group public values as `(exp (gen) alpha)` where `(alpha expt)` or `(alpha rndx)`. |

### 3. First-Order Logic & Goal Sorts (Table 7.1 — `CPSA_LOGIC_ONLY_SORTS`)

| Sort (`CPSASortEnum`) | Permitted Scope | Forbidden Scope | Semantics |
|---|---|---|---|
| `strd` | `defgoal`, `defrule`, `deflemma` quantifiers `(forall ((z strd)) ...)` | **Forbidden** in `defrole` / `defskeleton` `(vars ...)` | Strand variable indexing a protocol or listener strand in first-order geometric sentences. |
| `indx` | `defgoal`, `defrule`, `deflemma` quantifiers `(forall ((i indx)) ...)` | **Forbidden** in `defrole` / `defskeleton` `(vars ...)` | Node height/index variable along a strand in first-order geometric sentences. |
| `fact` | Internal relational fact sort | **Forbidden** in `defrole` / `defskeleton` `(vars ...)` | Logical relation sort for `(facts ...)` and `(fact ...)`. |

### 4. Forbidden Hallucinated Sorts

CPSA has **no** built-in sorts named `nonce`, `key`, `pubkey`, `privkey`, `symkey`, `cert`, `signature`, `hash`, `int`, `string`, or `bytes`. Declaring any of these in `(vars ...)` without a custom `(lang ...)` definition aborts compilation with `Sort [...] not recognized`.

---

## Complete Cryptographic Operator Signatures (Tables 10.3 & 10.5)

In `CPSAProtocolSpecification`, every compound `CPSATerm` is represented as a prefix JSON array `["<operator>", arg1, arg2, ...]`.

### 1. Basic Algebra Operators (`CPSA_BASIC_OPERATORS` — Table 10.3)

| Operator | Arity | JSON AST Signature | Scheme Syntax | Algebraic Sort Signature & Rules |
|---|---|---|---|---|
| `enc` | $\ge 2$ | `["enc", m1, ..., mN, key]` | `(enc m1 ... mN key)` | $\text{mesg}^+ \times \text{KeySort} \to \text{mesg}$. **The encryption key is ALWAYS the LAST argument.** Implicitly concatenates `m1 ... mN` before encrypting. `key` may be sort `skey`, `akey`, or any compound term (such as `["pubk", a]`, `["privk", a]`, `["ltk", a, b]`, `["hash", ...]`, or `["exp", ...]`), **except** a variable of sort `mesg` (Equation 10.1). |
| `hash` | $\ge 1$ | `["hash", m1, ..., mN]` | `(hash m1 ... mN)` | $\text{mesg}^+ \to \text{mesg}$. One-way cryptographic hash or keyed MAC/HMAC/KDF. Subterms inside `hash` are **not carried** (cannot be extracted by decomposition or decryption). |
| `cat` | $\ge 1$ | `["cat", m1, ..., mN]` | `(cat m1 ... mN)` | $\text{mesg}^+ \to \text{mesg}$. Right-associative tuple pairing $(m_1, (m_2, \dots))$. All components are publicly **carried** and extractable without keys. |
| `pubk` | $1$ or $2$ | `["pubk", name_id]` or `["pubk", "\"tag\"", name_id]` | `(pubk a)` or `(pubk "sig" a)` | $\text{name} \to \text{akey}$ (1-arg) or $\text{tag} \times \text{name} \to \text{akey}$ (2-arg). In 2-argument form, the **string tag MUST be first and the `name` variable MUST be second** (Table 10.3). |
| `privk` | $1$ or $2$ | `["privk", name_id]` or `["privk", "\"tag\"", name_id]` | `(privk a)` or `(privk "sig" a)` | $\text{name} \to \text{akey}$ (1-arg) or $\text{tag} \times \text{name} \to \text{akey}$ (2-arg). Syntactic sugar for `(invk (pubk a))` or `(invk (pubk "tag" a))`. |
| `invk` | $1$ | `["invk", akey_var]` | `(invk k)` | $\text{akey} \to \text{akey}$. Algebraic inverse of an unnamed asymmetric key variable `k : akey`, satisfying `(invk (invk k)) = k`. |
| `ltk` | $2$ | `["ltk", name1, name2]` | `(ltk a b)` | $\text{name} \times \text{name} \to \text{skey}$. Directional long-term symmetric key shared between principals `a` and `b`. Directional: `(ltk a b)` does **not** unify with `(ltk b a)` unless `a = b`. |

### 2. Diffie-Hellman Algebra Operators (`CPSA_DH_OPERATORS` — Table 10.5)

| Operator | Arity | JSON AST Signature | Scheme Syntax | Algebraic Sort Signature & Rules |
|---|---|---|---|---|
| `bltk` | $2$ | `["bltk", name1, name2]` | `(bltk a b)` | $\text{name} \times \text{name} \to \text{skey}$. Bidirectional long-term symmetric key satisfying the commutative equation `(bltk a b) = (bltk b a)`. Only available in `diffie-hellman` algebra (omitted from `CPSA/Roletran/Loader.hs` `loadDispatch`, so using `bltk` in `basic` algebra triggers `cpsa4roletran` `Keyword bltk unknown`). |
| `exp` | $2$ | `["exp", base_term, expt_term]` | `(exp (gen) x)` | $\text{base} \times \text{expt} \to \text{base}$. Modular exponentiation $h^x$. Satisfies `((exp (exp (gen) x) y)) = (exp (gen) (mul x y))`. Note: the exponent `x` is **uncarried** in `(exp (gen) x)`. |
| `gen` | $0$ | `["gen"]` | `(gen)` | $() \to \text{base}$. Constant group generator $g$. Must be written as a 0-ary list `["gen"]` in JSON (`(gen)` in Scheme), never as an unquoted string `"gen"` (unless normalized by `normalize_cpsa_term`). |
| `mul` | $\ge 2$ | `["mul", expt1, expt2, ...]` | `(mul x y)` | $\text{expt} \times \text{expt}^+ \to \text{expt}$. Abelian group multiplication in the exponent group. Associative and commutative. |
| `rec` | $1$ | `["rec", expt_term]` | `(rec x)` | $\text{expt} \to \text{expt}$. Multiplicative inverse $x^{-1}$ of an exponent, satisfying `(mul x (rec x)) = (one)`. |
| `one` | $0$ | `["one"]` | `(one)` | $() \to \text{expt}$. Multiplicative identity constant $1$ in the exponent group, satisfying `(exp h (one)) = h`. |

---

## Equation 10.1: The `mesg` Encryption Key Restriction

In MITRE CPSA 4.4.9 Section 10.3.1 (Equation 10.1), the decryption key inverse operator $\text{inv}(a)$ is defined as:

$$\text{inv}(a) = \begin{cases} a^{-1} & \text{if } a : \text{akey} \\ a & \text{if } a \text{ is not a variable of sort } \text{mesg} \\ \perp \text{ (undefined)} & \text{otherwise (if } a \text{ is a variable of sort } \text{mesg}\text{)} \end{cases}$$

### Why Encrypting with a `mesg` Variable Is Forbidden
Because CPSA uses a single operator `enc` for both symmetric encryption (where $\text{inv}(k) = k$) and asymmetric encryption (where $\text{inv}(k) = k^{-1}$), encrypting a payload with a variable `k` declared of sort `mesg` makes it algebraically ambiguous whether `inv(k)` is `k` or `(invk k)`.
- **Compiler Errors Triggered**:
  - `cpsa4`: `Algebra.inv: Cannot invert a variable of sort mesg`
  - `cpsa4roletran`: `Message variable cannot used as key`
  - `CPSAProtocolSpecification`: `_validate_no_mesg_encryption_key()` raises `ValueError: Variable '<k>' of sort 'mesg' ... cannot be used as an encryption key in (enc ...) per MITRE CPSA 4.4.9 Equation 10.1`.
- **Mandatory Fix**: Always declare encryption key variables with sort `"skey"` (for symmetric keys) or `"akey"` (for asymmetric keys)—never `"mesg"`, `"data"`, or `"text"`.

---

## Forbidden Foreign Operators and Canonical Desugaring (`CPSA_DESUGAR_MAP`)

LLMs trained on ProVerif, Tamarin, or Maude-NPA frequently hallucinate foreign cryptographic operators that do not exist in MITRE CPSA 4.4.9. Passing any of these to `cpsa4` or `cpsa4roletran` triggers `Keyword [...] unknown` or `Malformed term`:

| Forbidden Foreign Operator | Canonical CPSA 4.4.9 Equivalent | Semantic Modeling Rule in CPSA 4.4.9 |
|---|---|---|
| `aenc` / `asym_enc` | `enc` | Asymmetric encryption of `m` for `b` is `["enc", m, ["pubk", "b"]]` (or `["enc", m, "k"]` where `k : akey`). |
| `senc` / `sym_enc` | `enc` | Symmetric encryption of `m` under `k` (`k : skey`) is `["enc", m, "k"]` or `["enc", m, ["ltk", "a", "b"]]`. |
| `sign` / `dsig` | `enc` | Digital signature of `m` by `a` is modeled as encryption under `a`'s private key: `["enc", m, ["privk", "a"]]` (or `["enc", m, ["invk", "k"]]`). If the signed message is also readable in cleartext, send `["cat", m, ["enc", ["hash", m], ["privk", "a"]]]`. |
| `mac` / `hmac` / `kdf` | `hash` | Keyed MAC or KDF over `m` with key `k` is modeled as `["hash", m, "k"]` (or `["hash", "\"label\"", m, "k"]`). |
| `pair` / `tuple` | `cat` | Tuple construction in standard BCA is `["cat", m1, m2, ...]`. |
| `g` (bare string) | `["gen"]` | The Diffie-Hellman generator is a 0-ary operator `(gen)`, never a variable `g`. |
````

---

### `refrences/cpsa_kb/01_core_rules/02_roletran_and_executability_rules.md`

*sha256:`e04343744d5d` · 168 lines · 16.5 KB (~4,227 tokens) · lang:`markdown`*

````markdown
# CPSA 4.4.9 Roletran (`CPSA.Roletran`) and Pre-Flight Executability Rules

This document specifies the formal procedural translation rules enforced by `cpsa4roletran` (`CPSA.Roletran`), the dual-algebra verification gate (`src/verification_engine/roletran_executability_gate.py`), and the serializer invariants in `src/intermediate_representation/protocol_syntax_tree.py`.

---

## Purpose of `cpsa4roletran`: Procedural Executability Semantics

In Strand Space Theory, a CPSA role `(defrole ...)` is a declarative template of message transmissions (`send`) and receptions (`recv`). However, an analyst or LLM can easily write a syntactically valid declarative role that **no real computer program could ever execute**—for example:
- Sending a variable that was neither passed as an input, received in a prior message, nor freshly generated (`uniq-orig`);
- Receiving an encrypted payload `(enc n k)` and immediately transmitting `n` in the next step without possessing the decryption key `inv(k)`;
- Attempting to invert a one-way cryptographic `(hash x)` to recover `x`.

The `cpsa4roletran` compiler (`~/.cabal/bin/cpsa4roletran`, documented in `cpsa4roletran.md` and John D. Ramsdell's *Cryptographic Protocol Analysis and Compilation Using CPSA and Roletran*) bridges declarative strand spaces and real implementations by compiling each `defrole` into a language-independent procedure `(defproc ...)`. In RFC-LLM, `verify_role_executability()` runs `cpsa4roletran` as a $<15\text{ ms}$ pre-flight gate before invoking `cpsa4`.

---

## Formal Definition of a Role in `CPSA.Roletran`

Per `Role_Translations.md` Section 3, a role is a structure $r_X(c, i, o, u)$ over variable declarations $X$ where:
1. **Trace ($c \in (\pm \text{Alg}_X)^+$)**: A non-empty sequence of channeled message transmissions $+[h, t]$ (`(send h t)`) and channeled message receptions $-[h, t]$ (`(recv h t)`).
2. **Trace Variable Coverage**: Every variable declared in $X$ (`vars`), `inputs`, `outputs`, or `uniq-orig` **must occur in the trace $c$**.
3. **Inputs ($i \in (\text{BV}_X \cup \text{Chn}_X)^*$)**: A sequence of basic values and channels specifying the formal parameters known to the procedure at invocation time.
4. **Outputs ($o \in \text{Alg}_X^*$)**: A sequence of terms returned by the procedure upon successful completion of the trace.
5. **Uniquely Originating Fresh Values ($u \subseteq \text{BV}_X$)**: A set of basic values (`uniq-orig`) that are freshly generated via `frsh` at the point of their first outbound transmission in $c$.

---

## The Seven Mandatory `cpsa4roletran` Well-Formedness Constraints

`cpsa4roletran` enforces seven strict syntactic and structural checks on every `(defrole ...)` before checking message constructibility and destructibility:

### 1. Mandatory Channel on Every Trace Event
- **Rule**: Every `send` and `recv` event in the role's trace **must** occur on a declared channel variable of sort `chan`:
  ```scheme
  (send handshake_channel (enc client_nonce (pubk server_identity)))
  (recv handshake_channel client_nonce)
  ```
- **JSON AST Requirement**: Every `CPSATraceEvent` in `CPSAProtocolRole.trace` must set `"channel": "<chan_var>"`, and `<chan_var>` must be declared with `"sort": "chan"` in `CPSAProtocolRole.variables`.
- **Compiler Error if Violated**: `Missing channel` or `Expecting a channel`.

### 2. Mandatory `inputs` and `outputs` Fields (or `params` / `returns`)
- **Rule**: Every role passed to `cpsa4roletran` must include `(inputs ...)` (alias `params`) and, if returning values, `(outputs ...)` (alias `returns`).
- **Channel Inclusion Rule**: **Every channel variable used anywhere in `(trace ...)` MUST be listed in `(inputs ...)`**.
- **Compiler Error if Violated**: `Missing channel` (if a trace channel is omitted from `inputs`) or `Malformed role`.

### 3. Input Terms Restricted to Basic Values and Channels
- **Rule**: Every element of `(inputs ...)` must be either:
  - A channel variable of sort `chan`,
  - An atomic variable of a Basic Value sort (`name`, `text`, `data`, `tag`, `skey`, `akey`, `dev`, `locn`), or
  - A canonical key-constructor term producing a basic key value (`(pubk a)`, `(privk a)`, `( pubk "tag" a)`, `(privk "tag" a)`, `(invk k)`, `(ltk a b)`).
- **Forbidden in `inputs`**: Compound terms constructed with `cat`, `enc`, or `hash` (e.g., `["cat", "a", "b"]` or `["hash", "k"]`) are **never** basic values and cannot appear in `inputs`.
- **Compiler Error if Violated**: `Input is not a basic value or a channel <term>`.
- **Serializer Enforcement**: `_is_valid_roletran_input_term()` in `protocol_syntax_tree.py` automatically filters out compound non-key terms from `inputs`.

### 4. Disjointness of `inputs` and `uniq-orig`
- **Rule**: No term declared in `(uniq-orig ...)` may appear in `(inputs ...)`.
  $$\text{inputs} \cap \text{uniq-orig} = \emptyset$$
- **Semantic Reason**: An input is passed into the procedure from the caller before execution starts, whereas a `uniq-orig` value is freshly generated inside the procedure via `frsh` during execution. A value cannot be both pre-existing caller input and freshly generated mid-run.
- **Compiler Error if Violated**: `Uniquely originating value in input <term>`.
- **Serializer Enforcement**: `CPSAProtocolRole.to_cpsa_json()` strips any `uniq-orig` / `uniq-gen` term from `inputs`.

### 5. Disjointness of `inputs` and `outputs`
- **Rule**: No term declared in `(inputs ...)` may appear in `(outputs ...)`.
  $$\text{inputs} \cap \text{outputs} = \emptyset$$
- **Semantic Reason**: The caller of the generated procedure already possesses all `inputs` parameters; returning an input parameter as an output is redundant and forbidden by `CPSA.Roletran`.
- **Compiler Error if Violated**: `Output contains an input value <term>`.
- **Serializer Enforcement**: `CPSAProtocolRole.to_cpsa_json()` filters out any term from `outputs` that matches a term in `valid_inputs`.

### 6. Trace Occurrence Invariant for All Role Declarations
- **Rule**: Every variable occurring in `(vars ...)`, `(inputs ...)`, `(outputs ...)`, or `(uniq-orig ...)` **must** occur in at least one event inside `(trace ...)`.
- **Compiler Error if Violated**: `Undeclared variable <var>` or `Uniquely originating value <var> does not originate in trace`.
- **Serializer Enforcement**: `CPSAProtocolRole.to_cpsa_json()` extracts `trace_tokens` from the normalized trace and drops any declaration term whose variables are not a subset of `trace_tokens`.

### 7. TrueCarried Origination for `uniq-orig`
- **Rule**: Every basic value in `(uniq-orig ...)` must **originate** in the role's trace—meaning its first occurrence in the trace is in a `send` event, AND it appears in a **carried** position (i.e., outside key positions and outside `(hash ...)` digests).
- **Compiler Error if Violated**:
  - If first seen in a `recv` or only inside `(hash ...)`: `Uniquely originating value <var> does not originate in trace`.
  - If compound term placed in `uniq-orig`: `Expecting a basic value`.

---

## The Three Procedural Executability Rules (Constructibility & Destructibility)

After verifying well-formedness, `cpsa4roletran` simulates the step-by-step execution environment $E$ of the role from trace event $0$ to $n-1$ (`Role_Translations.md` Section 4, Figures 2 & 3):

### Rule 1: Outbound Term Constructibility (`send`)
At every `(send ch t)` event, the transmitted term $t$ must be **constructible** from the current knowledge environment $E$ (which starts with `inputs` and accumulates `uniq-orig` values generated at this step plus subterms extracted from prior `recv` events):
- A basic value is constructible iff it is in `inputs`, was already extracted from an earlier `recv`, or is declared in `uniq-orig` and originates at this `send`.
- `(cat t1 t2)` is constructible iff `t1` and `t2` are constructible (`pair`).
- `(hash t1)` is constructible iff `t1` is constructible (`hash`).
- `(enc t1 k)` is constructible iff `t1` is constructible and the encryption key `k` is constructible (`encr`), where `k` is **not** a variable of sort `mesg` and `k` is declared with a key sort (`skey` or `akey`).
- **Compiler Error on Failure**: `Cannot build <term>`.
- **Common Root Causes of `Cannot build <term>`**:
  1. A fresh nonce/secret sent by the role was omitted from `unique_originating`.
  2. A pre-shared key (`(ltk a b)`), peer public key (`(pubk b)`), own signing key (`(privk a)`), or principal identity (`a`, `b`) used to build the message was omitted from `inputs`.
  3. A symmetric key variable `k` used in `["enc", payload, "k"]` was declared with sort `"data"` or `"text"` instead of `"skey"`, or an asymmetric key was not properly typed.

### Rule 2: Inbound Term Destructibility (`recv`)
At every `(recv ch t)` event, the received term $t$ must be **fully destructurable** into basic values and hashes that can either be bound to new variables or compared for equality (`same` / $v_1 \approx v_2$) against already-known values in $E$:
- Receiving `(cat t1 t2)` projects `frst` (`t1`) and `scnd` (`t2`), recursively destructuring both.
- Receiving `(enc t1 k)` requires that the **inverse decryption key** $k^{-1} = \text{inv}(k)$ is **already constructible in $E$** at the moment the message arrives, AND $k^{-1}$ is **encryption-free** ($\text{enc\_free}(k^{-1})$):
  - If `k` is `(pubk b)`, the receiver must already know `(privk b)` (e.g., via `inputs`).
  - If `k` is `(privk a)` (a signature), the receiver must already know `(pubk a)` (e.g., via `inputs`).
  - If `k` is `k_sym : skey` or `(ltk a b)`, the receiver must already know `k_sym` or `(ltk a b)` (via `inputs` or an earlier decrypted component).
  - **Ordering Trap inside `cat`**: If a single message is `(cat k (enc m k))` where `k` is acquired from the first element, `cpsa4roletran` processes components left-to-right; if the encryption comes before the key is extracted or if the key is inside a hash `(hash s)` where `s` is unknown, decryption fails.
- Receiving `(hash t1)` **cannot** be inverted to learn `t1`! Because hashes are one-way, when a role receives `(hash t1)`, the role must **already** be able to construct `(hash t1)` from its current environment $E$ and compare the received digest against the locally computed digest via `(same v_recv v_computed)`. If any variable inside `(hash t1)` is not yet known to the receiver, `cpsa4roletran` rejects the reception!
- **Compiler Error on Failure**: `Received term cannot be fully destructured` or `Message not receivable <term>`.

### Rule 3: Return Value Constructibility (`outputs`)
At the end of the trace, every term listed in `(outputs ...)` must be constructible from the final environment $E$ (`return(v0, v1, ...)`).
- **Compiler Error on Failure**: `Cannot build <term>`.

---

## Probabilistic Encryption, Message Receivability (`receivable`), and the Encryption-Free Requirement

Per `Role_Translations.md` Section 5–7 (Equations 7, 12, 13 and Lemma 11), real-world encryption is probabilistic (encrypting the same plaintext and key twice with different randomness produces different ciphertexts). To guarantee adequacy (Theorem 14) between abstract Dolev-Yao execution and concrete probabilistic execution, `cpsa4roletran` enforces two levels of restrictions:

### 1. The `receivable` Check in `CPSA.Roletran.Algebra` & `CPSA.Roletran.Derivation`
In `CPSA/Roletran/Algebra.hs` (`receivable`, lines 190–209) and `CPSA/Roletran/Derivation.hs` (`deriveEvent`, lines 88, 104; `deriveOutput`, line 320), `cpsa4roletran` checks **every** message term $t$ in:
- Every outbound `(send ch t)` event,
- Every inbound `(recv ch t)` event, and
- Every return value in `(outputs ...)`!

A term $t$ satisfies `receivable t == Nothing` if and only if:
1. **No Encryption in Key Position**: $t$ contains **no** occurrence of an encryption `(enc ...)` inside the key position $y$ of any encryption `(enc x y)` (`findEnc y == Nothing`); AND
2. **No Encryption Inside Hash**: $t$ contains **no** occurrence of an encryption `(enc ...)` anywhere inside a hash `(hash x)` (`findEnc x == Nothing`).

If a term violates either rule—for instance, hashing a ciphertext `["hash", ["enc", "n", "k"]]` or using an encrypted term as an encryption key `["enc", "m", ["enc", "k1", "k2"]]`—`cpsa4roletran` immediately aborts with:
```
Message not receivable (enc ...)
```
**How to Model Hash-of-Plaintext or Compound Keys Safely**:
- Never wrap `["enc", ...]` inside `["hash", ...]`. Instead, hash the plaintext values `["hash", "n", "id"]` or encrypt the hash `["enc", ["hash", "n"], "k"]`.
- Never use `["enc", ...]` as the key argument of `["enc", ...]`. Instead, use an atomic `skey`/`akey` variable, `(ltk a b)`, `(pubk a)`, `(privk a)`, or a `(hash ...)` of encryption-free values as the key.

### 2. The Encryption-Free (`enc_free`) Requirement on Keys and Equality Checks
Furthermore, `CPSA.Roletran.Derivation` requires three kinds of terms to be **encryption-free** ($\text{enc\_free}$):
1. The decryption key $t_2^{-1}$ synthesized by `synth st (inv y)` in `loopEncr` (`Decr`, Equation 7);
2. Any two terms compared by an equality/sameness check `Same` ($v_1 \approx v_2$, Equation 12)—meaning a role cannot verify a received ciphertext by re-encrypting the plaintext and comparing ciphertexts byte-for-byte (unless it decrypts the ciphertext and compares plaintexts or compares hashes of plaintexts);
3. Terms compared with an inverse key pair check `Invp` (Equation 13).

### 3. Official Haskell Implementation Map (`src/CPSA/Roletran/`)
| Haskell Module | Key Functions | Enforcement Responsibility |
|---|---|---|
| `CPSA.Roletran.Loader` (`Roletran/Loader.hs`) | `loadProt`, `loadRole`, `loadEvt`, `loadVars`, `loadSort`, `loadChan`, `loadBasic`, `loadTerm`, `loadEnc` | Rejects non-`basic` algebra (`Expecting terms in basic algebra `), missing channels (`Missing channel`), channel variables inside message terms (`Not expecting a channel`), non-basic terms in `uniq-orig` (`Expecting a basic value`), and `mesg` variables used as encryption keys (`Message variable cannot used as key`). |
| `CPSA.Roletran.Protocol` (`Roletran/Protocol.hs`) | `mkRole`, `checkInput`, `checkUniq`, `addPos`, `checkOutput`, `originationPos` | Enforces `isBasic input || isChanVar input` (`Input is not a basic value or a channel `), `inputs`/`uniq-orig` disjointness (`Uniquely originating value in input `), `uniq-orig` carried origination (`Uniquely originating value ... does not originate in trace`), and `inputs`/`outputs` disjointness (`Output contains an input value `). |
| `CPSA.Roletran.Algebra` (`Roletran/Algebra.hs`) | `isBasic`, `isMesgVar`, `isChanVar`, `carriedBy`, `receivable`, `findEnc` | Defines the 7-sort Roletran type system (`Text`, `Data`, `Name`, `Skey`, `Akey`, `Ikey`, `Mesg`, `Chan`), carried position check (`carriedBy`), and the encryption-free hash/key check (`receivable`). |
| `CPSA.Roletran.Derivation` (`Roletran/Derivation.hs`) | `derive`, `deriveEvent`, `deriveUniques`, `build`, `synth`, `reduce`, `loop`, `loopPair`, `loopEncr`, `loopHash`, `deriveOutput` | Compiles role traces to procedures (`Proc`), enforcing `receivable` (`Message not receivable `), outbound synthesis (`Cannot build `), and fixed-point inbound destructuring (`Received term cannot be fully destructured`). |

---

## Why `cpsa4roletran` Rejects `diffie-hellman` and How the Dual Gate Works

### 1. The `CPSA.Roletran` Algebra Limitation
In MITRE CPSA 4.4.9, the `cpsa4roletran` binary is hard-wired to `CPSA.Roletran.Algebra`, which implements **only** the `basic` cryptoalgebra. When given a protocol with `(defprotocol <id> diffie-hellman ...)`, `cpsa4roletran` immediately aborts with:
```
Expecting terms in basic algebra
```

### 2. The RFC-LLM Dual Pre-Flight Gate (`roletran_executability_gate.py`)
`verify_role_executability(scm_path)` in `src/verification_engine/roletran_executability_gate.py` inspects the emitted `.scm` file and routes validation based on the algebra:

| Protocol Algebra | Pre-Flight Binary Invoked | Validation Performed (<50 ms) | Pass Condition |
|---|---|---|---|
| `basic` | `~/.cabal/bin/cpsa4roletran` (stdin) | Full procedural compilation to `defproc`: checks channel presence, `inputs`/`outputs`/`uniq-orig` disjointness, sort rules, outbound constructibility, and inbound destructibility. | `returncode == 0` and empty `stderr`. Returns compiled `procedural_defproc_code`. |
| `diffie-hellman` | `~/.cabal/bin/cpsa4 -l 1 <scm_path>` | Runs the full CPSA 4.4.9 Loader and Preskeleton initialization with step limit `-l 1`. Validates S-expression grammar, herald `(algebra diffie-hellman)`, sort hierarchy (`rndx` vs `expt`), exponent acquisition (`Expts must first be received, rndxs first sent`), bare exponent rules, `uniq-gen` origination, and skeleton maplets. | Reaches `"Step limit exceeded"` on `stderr` with no `"Role not well formed"` or `"Expecting"` errors (`is_step_limit_only == True`). |
````

---

### `refrences/cpsa_kb/01_core_rules/03_declarations_origination_and_assumptions.md`

*sha256:`12bf91e3827d` · 139 lines · 12.0 KB (~3,076 tokens) · lang:`markdown`*

````markdown
# CPSA 4.4.9 Declarations, Origination, Carried Positions, and Assumptions Reference

This document provides the exhaustive formal reference for all origination, freshness, secrecy, relational, and state declarations in MITRE CPSA 4.4.9 (Manual Chapter 6, Chapter 7, and Table 10.6).

---

## Carried vs. Uncarried Subterm Positions (Manual §6.2 & Roletran §2)

The distinction between **carried** and **uncarried** occurrences of a term is the foundational concept governing `non-orig`, `pen-non-orig`, `uniq-orig`, and `uniq-gen`.

### Formal Definition of "Carried By" ($t_0 \sqsubseteq t_1$)
A term $t_0$ is **carried by** a message $t_1$ (written $t_0 \sqsubseteq t_1$) iff $t_0$ can be extracted from $t_1$ via tuple decomposition and decryption by an entity who possesses the necessary decryption keys. Formally, $\sqsubseteq$ is the smallest reflexive, transitive relation satisfying:
1. **Reflexivity**: $t \sqsubseteq t$
2. **Pairing / Concatenation (`cat`)**: $t_0 \sqsubseteq (t_0, t_1)$ and $t_1 \sqsubseteq (t_0, t_1)$ (all arguments of `cat` carry their carried subterms)
3. **Encryption (`enc`)**: $t_0 \sqsubseteq \{| t_0 |\}_{t_1}$ (an encryption carries its **plaintext payload** arguments, NOT its key $t_1$)

### What Is Carried vs. Uncarried in Practice

| Enclosing Expression | Subterm Position | Carried or Uncarried? | Formal Reason |
|---|---|---|---|
| `(cat a b c)` | `a`, `b`, `c` | **Carried** | Tuple projection extracts every component directly. |
| `(enc m1 m2 k)` | Plaintexts `m1`, `m2` | **Carried** | Decrypting with $\text{inv}(k)$ recovers `m1` and `m2`. |
| `(enc m1 m2 k)` | Key `k` | **Uncarried** (unless `k` also appears in `m1`/`m2`) | Decrypting $\{|m_1, m_2|\}_k$ does not yield the key $k$; using a key to encrypt does not transmit the key. |
| `(hash m1 m2 k)` | Any argument `m1`, `m2`, `k` | **Uncarried** | Cryptographic hashes are one-way functions; no key or operation can invert `#(m)` to extract `m`. |
| `(exp (gen) x)` | Exponent `x` | **Uncarried** | Discrete logarithm is one-way; knowing $g^x$ never allows extracting the exponent $x$. |

---

## Why Atoms Cannot Originate Inside a `hash`

By definition (Manual §6.2), a term $t$ **originates** at a strand node $n = (s, i)$ iff:
1. Node $n$ is an outbound transmission (`send` / $+$),
2. $t$ is **carried** in the message sent at node $n$ ($t \sqsubseteq \text{msg}(n)$), and
3. $t$ does not occur in a carried position of any earlier node $(s, j)$ for $j < i$.

Because `(hash x)` is a one-way digest, $x$ is **never carried** by `(hash x)`. Consequently:
- If a role's only outbound transmission of `x` is `(send ch (hash x))`, then `x` **never originates** in that trace!
- Declaring `(uniq-orig x)` when `x` only appears inside `(hash ...)` or as the key of `(enc m x)` or as the exponent of `(exp (gen) x)` causes immediate compilation failure:
  - `cpsa4`: `Role not well formed: uniq-orig x doesn't originate` (or `Skeleton not well formed: uniq-orig x doesn't originate`)
  - `cpsa4roletran`: `Uniquely originating value x does not originate in trace`
- **How to Fix**:
  - If `x` is a fresh nonce that must originate, it must be sent in a **carried** position (either in plaintext `(cat x ...)` or inside the plaintext payload of an encryption `(enc x ... k)`).
  - If `x` is only ever used as an uncarried key, MAC secret, or DH exponent, use `uniq-gen` (if freshly generated at an outbound node) or `pen-non-orig` / `non-orig` (if a long-term secret).

---

## The Four Core Secrecy & Freshness Declarations (Manual §6.2 & Table 10.6)

All four declarations (`non-orig`, `pen-non-orig`, `uniq-orig`, `uniq-gen`) apply strictly to **basic values / atomic terms** (`name`, `text`, `data`, `skey`, `akey`, `rndx`, or atomic key constructors `(pubk a)`, `(privk a)`, `(invk k)`, `(ltk a b)`, `(bltk a b)`). Applying them to compound terms like `(cat a b)` or `(hash k)` triggers `Expecting an atom`.

### 1. `non-orig` (Non-Origination — Goal Predicate: `non`)
- **Syntax**: `(non-orig term+)` | JSON AST: `non_originating: List[CPSATerm]`
- **Formal Semantics**: Restricts analysis to bundles in which the declared atom **originates on NO strand whatsoever** (neither regular protocol strands nor penetrator `create` strands).
- **Fundamental Lemma**: A value is `non-orig` in a bundle **only if it is never carried in any message anywhere in the bundle** (even inside an encrypted payload!).
- **When to Use**: Long-term private keys (`["privk", "server_id"]`, `["invk", "k"]`) and pre-shared symmetric keys (`["ltk", "client_id", "server_id"]`) that are **only ever used as encryption/decryption keys or inside `(hash ...)`** and are **never transmitted as payload**.
- **Optional Height Form in Roles (Table 10.6)**: In a role declaration, `(non-orig (t h))` asserts that `t` is non-originating whenever the strand has height at least `h`.
- **Fatal Pitfall (`non-orig [...] carried`)**: If a key `k` is transmitted inside an encryption `(send ch (enc k (pubk b)))` (e.g., key transport / session key distribution), `k` is **carried**! Declaring `(non-orig k)` causes `Role not well formed: non-orig k carried` or `Skeleton not well formed: non-orig k carried` (or silently kills all shapes). Use `pen-non-orig` or `uniq-orig` instead!

### 2. `pen-non-orig` (Penetrator Non-Origination — Goal Predicate: `pnon`)
- **Syntax**: `(pen-non-orig term+)` | JSON AST: `pen_non_originating: List[CPSATerm]`
- **Formal Semantics**: Restricts analysis to bundles in which the declared atom **never originates on a penetrator strand** (cannot be invented by the adversary's `create` role), **but MAY originate and be carried on regular protocol strands**.
- **When to Use**:
  - Pre-shared secrets, passwords, or tickets that are transmitted inside encrypted messages or carried across strands;
  - Session keys or secrets in compromise/leakage experiments where regular roles transmit the key as payload.
- **Compatibility**: Can be combined with `uniq-orig` on the same variable without conflict.

### 3. `uniq-orig` (Unique Origination — Goal Predicate: `uniq`)
- **Syntax**: `(uniq-orig term+)` | JSON AST: `unique_originating: List[CPSATerm]`
- **Formal Semantics**: Asserts that the declared atom originates (has its first **carried** occurrence in an outbound `send` event) at **exactly one node in the entire bundle**. Because it originates at a regular strand node in the skeleton, the penetrator cannot independently invent it in a `create` strand.
- **When to Use**:
  - Freshly generated nonces and challenges (`sort: "text"` or `"data"`);
  - Freshly generated symmetric session keys (`sort: "skey"`) that are transmitted (carried) inside an encrypted key-transport message `(send ch (enc session_key (pubk peer)))`.
- **Mandatory Requirement**: The term **must** appear in a carried position of a `send` event in the role/skeleton where `(uniq-orig ...)` is declared, and must not appear in an earlier `recv` event on that strand.

### 4. `uniq-gen` (Unique Generation — Goal Predicate: `ugen`)
- **Syntax**: `(uniq-gen term+)` | JSON AST: `unique_generated: List[CPSATerm]`
- **Formal Semantics**: Asserts that the declared atom **generates** (has its first occurrence—**whether carried or uncarried**—in an outbound `send` or `stor` event) at **exactly one node in the entire bundle**.
- **When to Use**:
  1. **All Diffie-Hellman random private exponents (`sort: "rndx"`)**: In `(send ch (exp (gen) x))`, `x` is in an uncarried exponent position. Therefore, `x` generates at that node but does not originate there. **Always put `rndx` variables in `uniq-gen` (`unique_generated`), NEVER `uniq-orig`**.
  2. Freshly generated symmetric keys that are immediately used as the encryption key `(send ch (enc payload k))` or inside a hash `(send ch (hash payload k))` without ever being transmitted in a carried position.
  3. Asymmetric key pairs generated dynamically mid-run: an asymmetric key `k` and its inverse `(invk k)` generate together at the first outbound occurrence of either one (Manual §7.2).

---

## Node-Specific & Advanced Declarations (Manual Ch. 6, 7, 8 & Table 10.6)

### 1. `uniq-at` and `ugen-at` (Node-Anchored Freshness Predicates — Table 7.1)
- **Syntax (in `defgoal` / `defrule` atomic formulas)**:
  - `(uniq-at term strdvar index)`
  - `(ugen-at term strdvar index)`
- **Semantics**: Asserts not only that `term` is uniquely originating (`uniq`) or uniquely generated (`ugen`), but pinpoints the exact strand `strdvar` and 0-based event index `index` at which it originates or generates.
- **Compiler Diagnostic**: If `(uniq-at a z i)` is placed in the antecedent of a goal for a node where `a` does not actually originate, `cpsa4` aborts with `Atom not unique at node`.

### 2. `absent` (Diffie-Hellman Exponent Independence — Manual §6.3)
- **Syntax (in `defskeleton` two-term-decl)**:
  ```scheme
  (absent (x y) (x (mul y z)))
  ```
- **Typing Requirement**: Each pair `(rndx_var expt_term)` **must** have an `rndx` variable as its first element and an `expt` term as its second element.
- **Semantics**: Asserts that the atomic random exponent `x` does not occur algebraically inside the exponent expression `y` (even after group cancellations). CPSA automatically adds `(absent (x y))` when `y` is an exponent occurring on a strand before the node where `x` is declared `uniq-gen`.
- **Compiler Diagnostic**: Passing wrong sorts to `absent` triggers `Algebra.absenceSubst: bad absence assertion` or `Algebra.nullifyOne: unexpected pattern`.

### 3. `ind-zero` (Independent of Zero / Exponent Non-Cancellation)
- **Syntax (in `defrole`)**: `(ind-zero expt_term+)`
- **Semantics**: Role-level declaration asserting that an exponent expression cannot reduce to the identity element `(one)`.

### 4. `precur` (Precursor Declaration)
- **Syntax**: `(precur (strd indx))`
- **Semantics**: Internal/advanced skeleton declaration used in Diffie-Hellman exponentiation reduction.

### 5. `neq` and `facts` (Inequality & User-Defined Relational Facts — Manual §7.7.1)
- **Syntax in `defrole` / `defskeleton` (`CPSAProtocolRole.facts` / `CPSAPreskeleton.facts`)**:
  ```scheme
  (facts (neq client_identity server_identity) (trusted ca_identity))
  ```
  - In JSON AST: `"facts": [["neq", "client_identity", "server_identity"]]`
- **Built-in `neq` Rule**: CPSA automatically generates three built-in `defgenrule` axioms (for sorts `mesg`, `strd`, and `indx`):
  ```scheme
  (defrule neq
    (forall ((a mesg))
      (implies (fact neq a a) (false))))
  ```
  Whenever a branch of shape analysis unifies two variables declared in `(facts (neq a b))` (such as a reflection attack where initiator `a` talks to itself `a = b`), the `neq` rule derives `(false)` and prunes that branch immediately.
- **Native Two-Term Inequality (`(neq (t1 t2))`)**: CPSA also supports the native declaration `(neq (t1 t2))` in `skel-decl`; if `t1` and `t2` are already identical in the initial role/skeleton definition, `cpsa4` fails with `[Role / Skeleton] not well formed: inequality conditions violated`.

### 6. `lt` and Subsort Declarations
- **Syntax**: `(lt (t1 t2)+)`
- **Semantics**: Partial order constraint on terms. If a cycle is formed in the role or skeleton definition, `cpsa4` aborts with `[Role / Skeleton] not well formed: lt declarations form a cycle`.

### 7. `gen-st` (Generated State Values — Manual §8.2.3 & Table 10.6)
- **Syntax**: `(gen-st term+)` | JSON AST: `gen_st: List[CPSATerm]`
- **Semantics**: Asserts that a state tuple `term` read by a `(load loc term)` event is **definitely non-initial** (could not have been present in the register at device power-up). Consequently, reading a `gen-st` value from `loc` acts like receiving on an authenticated channel: CPSA requires a regular strand with a prior `(stor loc term)` transition to explain how `term` was written into `loc`.

### 8. `assume` (Role-Level Logical Assumptions — Manual §7.7.3 & Table 10.6)
- **Syntax (in `defrole` only)**:
  ```scheme
  (assume (fact neq (exp (gen) upsilon) (gen)))
  ```
- **Semantics**: Generates an automatic `defgenrule` stating that any strand of the role reaching the height where all free variables of the formula have appeared satisfies the conclusion formula. Note: `assume` is **not** recognized inside `defskeleton` (use `facts` in `defskeleton`).
````

---

### `refrences/cpsa_kb/01_core_rules/04_skeletons_3pov_and_security_goals.md`

*sha256:`69b35f7b4460` · 143 lines · 13.6 KB (~3,469 tokens) · lang:`markdown`*

````markdown
# CPSA 4.4.9 Point-of-View Preskeletons, 3-POV Separation, and Security Goals Reference

This document specifies the formal architecture of CPSA point-of-view preskeletons (`defskeleton`), the mandatory 3-POV separation rule enforced by `ensure_three_point_of_view_skeletons()` in `src/semantic_extraction/constrained_protocol_extractor.py`, and the first-order geometric logic language (`defgoal`, `defrule`, `deflemma`, and Shape Analysis Sentences) from Manual Chapter 7 and Tables 7.1 & 10.1.

---

## Mandatory 3-POV Skeleton Architecture (`ensure_three_point_of_view_skeletons`)

Every protocol specification in RFC-LLM (`CPSAProtocolSpecification.skeletons`) **must** partition its analysis queries into three distinct point-of-view preskeletons (`CPSAPreskeleton`):

1. **Skeleton 1: Pure Initiator / Client Point of View (Authentication & Shape Realization)**:
   - **Strands**: One `defstrandmax` instance of the Initiator/Client role.
   - **Listeners**: `[]` (**STRICTLY EMPTY** — `deflistener` is forbidden here).
   - **Assumptions**: `non_originating` on uncompromised long-term keys (`(privk ...)`, `(ltk ...)`) and `unique_originating` (or `unique_generated` for `rndx`) on fresh values generated by the Initiator.
   - **Expected `cpsa4` Outcome**: Produces **$\ge 1$ realized shape** (`(shape)`) demonstrating that if the Initiator completes its run, a corresponding Responder strand must have executed and agreed on the cryptographic handshake parameters.
2. **Skeleton 2: Pure Responder / Server Point of View (Mutual Authentication)**:
   - **Strands**: One `defstrandmax` instance of the Responder/Server role.
   - **Listeners**: `[]` (**STRICTLY EMPTY** — `deflistener` is forbidden here).
   - **Assumptions**: `non_originating` on uncompromised long-term keys and `unique_originating` / `unique_generated` on fresh values generated by the Responder.
   - **Expected `cpsa4` Outcome**: Produces **$\ge 1$ realized shape** (`(shape)`) verifying what peer behavior the Responder can rely on having occurred when the Responder completes its run.
3. **Skeleton 3: Dedicated Secrecy / Non-Disclosure Point of View (`deflistener`)**:
   - **Strands**: One `defstrandmax` instance of the originating role **plus** `(deflistener <secret_term>)` via `listeners: ["<secret_term>"]` (populated from `CPSAProtocolSpecification.primary_secrecy_goals`).
   - **Assumptions**: Same `non_originating` and `unique_originating` / `unique_generated` assumptions as the pure POV skeleton.
   - **Expected `cpsa4` Outcome**: Produces **0 realized shapes**—terminating in `(dead)` with `empty cohort` or `(comment "Not a skeleton")`. Because the listener strand asks whether the adversary can hear `<secret_term>` in the clear, **0 shapes proves mathematically that the secret cannot be leaked**.

---

## Why Putting `deflistener` Inside a Pure POV Skeleton Kills Bilateral Shape Realization

A frequent modeling bug is placing `"listeners": ["session_key"]` inside the Initiator or Responder POV skeleton without creating separate listener-free POV skeletons.
- **How CPSA Evaluates a Skeleton**: A skeleton represents the conjunction of *all* strands declared inside it. If a skeleton contains both `(defstrandmax client ...)` and `(deflistener session_key)`, CPSA searches for executions where **both** the client completes the handshake **and** the penetrator learns `session_key` in plaintext.
- **Why It Kills Shape Realization**: In any secure protocol where `session_key` is properly protected by `non-orig` and `uniq-orig`, the penetrator **cannot** derive `session_key`. Consequently, the listener reception node `(recv session_key)` can never be explained, the entire skeleton dies (`(dead)`), and CPSA outputs **0 shapes** (`shapes_count == 0`).
- **Verification Consequence**: Because `mitre_build_orchestrator.py` verifies that a protocol model realizes at least 1 bilateral handshake shape (`shapes_count > 0` in `<stem>_shapes.txt`), putting `deflistener` in every skeleton results in 0 total shapes across the file, hiding the bilateral handshake graph and failing shape realization! Separating pure POV skeletons (`listeners: []`) from the Secrecy POV skeleton (`listeners: [secret]`) ensures that Skeletons 1 & 2 realize the bilateral handshake shapes while Skeleton 3 proves secrecy by dying with 0 shapes.

---

## Complete Reference for `defskeleton`, `defstrand`, `defstrandmax`, and `deflistener`

### 1. `defskeleton` (synonym: `defpreskeleton`)
- **Grammar (Table 10.1)**:
  ```bnf
  skeleton   ::= "(" "defskeleton" id vars strand+ skel-alist ")"
  skel-alist ::= skel-decl* (precedes node-pair*)? (leadsto node-pair*)? (goal sentence+)? (facts (id term*)*)?
  ```
- **Top-Level Placement Rule**: Every `(defskeleton ...)` **must** be a top-level S-expression sibling *after* `(defprotocol ...)` has been closed with `)`. Nesting `(defskeleton ...)` inside `(defprotocol ...)` causes CPSA to silently ignore the skeleton as an unrecognized protocol association-list key, causing `cpsa4graph: Empty input`.

### 2. `defstrand` vs. `defstrandmax`
- **`defstrand`**:
  - **Grammar**: `(defstrand role_id height (role_var skel_term)*)`
  - **Height Requirement**: The integer `height` is **mandatory** and must satisfy $1 \le \text{height} \le |\text{trace}(\text{role\_id})|$. Passing `0`, a negative integer, or an integer exceeding the role's trace length triggers `Bad height`, `Bad position in role`, or `Negative position in role`. Omitting the integer triggers `Malformed defstrand`.
- **`defstrandmax`**:
  - **Grammar**: `(defstrandmax role_id (role_var skel_term)*)`
  - **Semantics**: Automatically instantiates `role_id` to its full maximum trace length $|\text{trace}(\text{role\_id})|$. Used by `CPSAStrandInstance.to_cpsa_json()` across RFC-LLM.
- **Maplet Binding Rules (`(role_var skel_term)`)**:
  - The first element `role_var` must be a variable declared in the role's `(vars ...)` that **actually appears in the role's `(trace ...)`**. If a variable was declared in the role's `(vars ...)` but never used in `(trace ...)`, CPSA prunes it from the role's parameters and rejects the maplet with `Identifier <role_var> unknown`.
  - The sort of `skel_term` in the skeleton's `(vars ...)` must be compatible with the sort of `role_var` in the role's `(vars ...)`, or `cpsa4` fails with `Domain does not match range`.
  - Always use simple variable-to-variable maplets `(x x)` in `defstrandmax`.

### 3. `deflistener`
- **Grammar**: `(deflistener term)` | JSON AST: `CPSAPreskeleton.listeners: List[CPSATerm]`
- **Semantics**: Instantiates a 2-event penetrator listener strand that first receives `term` (`(recv term)`) and immediately retransmits `term` (`(send term)`) to test whether `term` can ever become available to the adversary outside encryption.
- **Equation 10.1 Check**: Just like role trace events, `term` inside `deflistener` cannot use a variable of sort `mesg` as an encryption key (`validate_skeleton_invariants()`).

### 4. `precedes` and `leadsto`
- **Grammar**:
  - `(precedes ((s1 i1) (s2 i2))*)` | JSON AST: `precedes: List[List[List[int]]]`
  - `(leadsto ((s1 i1) (s2 i2))*)` | JSON AST: `leadsto: List[List[List[int]]]`
- **Indexing**: `s` is the 0-based strand index in the skeleton (in order of `defstrand`/`defstrandmax`/`deflistener` appearance) and `i` is the 0-based node index along strand `s`.
- **Well-Formedness Constraints**:
  - In `precedes`, `(s1 i1)` and `(s2 i2)` **must belong to different strands** ($s_1 \ne s_2$), or `cpsa4` fails with `Malformed pair -- nodes in same strand`. (Note: `leadsto` allows same-strand pairs).
  - In `precedes`, the earlier node `(s1 i1)` must be an outbound transmission (`send`/`stor`) and the later node `(s2 i2)` must be an inbound reception (`recv`/`load`), or `cpsa4` fails with `Skeleton not well formed: ordered pairs not well formed`.
  - The directed graph formed by strand succession and `precedes` pairs must be acyclic, or `cpsa4` fails with `Skeleton not well formed: cycle found in ordered pairs`.

---

## First-Order Geometric Logic: `defgoal`, `defrule`, `defgenrule`, and `deflemma` (Chapter 7)

### 1. `defgoal` Grammar & Semantics (Table 7.1)
A `defgoal` states a formal security property in first-order geometric logic:
```bnf
goal        ::= "(" "defgoal" prot_id sentence+ alist ")"
sentence    ::= "(" "forall" "(" gvdecl* ")" "(" "implies" conjunction conclusion ")" ")"
gvdecl      ::= "(" id+ (sort | "strd" | "indx") ")"
conjunction ::= conjunct | "(" "and" conjunct+ ")"
conclusion  ::= "(" "false" ")" | existential | "(" "or" existential+ ")"
existential ::= conjunction | "(" "exists" "(" gvdecl* ")" conjunction ")"
```
- **Characteristic Skeleton Extraction**: When `cpsa4` loads a `defgoal`, it extracts the **characteristic skeleton** $k_0$ from the antecedent (`conjunction`), runs standard shape analysis on $k_0$, and checks whether every resulting shape $k_i$ satisfies the `conclusion`.
- **Verdict Annotations**:
  - `(satisfies yes)`: The shape satisfies the goal conclusion.
  - `(satisfies (no (var val)...))`: The shape is a counterexample to the goal; the variable bindings show the exact instantiation of the antecedent for which the conclusion failed.

### 2. Complete Goal & Rule Predicate Reference (Table 7.1)

| Predicate Form | Syntactic Sugar Form | Formal Meaning in Skeleton $k$ |
|---|---|---|
| `(p "role" z h)` | `(strand role z h ...)` | Strand variable `z : strd` is an instance of `"role"` of height at least `h` ($\ge h$ events). |
| `(p "role" "param" z t)` | `(strand role z h (param t))` | Role parameter `"param"` on strand `z` is bound to algebra term `t` (requires `z` to have height past the first appearance of `"param"`). |
| `(p "" z 1)` + `(p "" "x" z t)` | `(listener z t)` | Strand `z : strd` is a listener strand observing message `t`. |
| `(prec z0 i0 z1 i1)` | — | Event `(z0, i0)` causally precedes event `(z1, i1)` ($(z_0, i_0) \prec (z_1, i_1)$). |
| `(leads-to z0 i0 z1 i1)` | — | State transition `(z0, i0)` writes a state value read by `(z1, i1)` with no intervening transition ($(z_0, i_0) \leadsto (z_1, i_1)$). |
| `(non t)` | — | Term `t` is assumed `non-orig`. |
| `(pnon t)` | — | Term `t` is assumed `pen-non-orig`. |
| `(uniq t)` | — | Term `t` is assumed `uniq-orig`. |
| `(uniq-at t z i)` | — | Term `t` uniquely originates at exact node `(z, i)`. |
| `(ugen t)` | — | Term `t` is assumed `uniq-gen`. |
| `(ugen-at t z i)` | — | Term `t` is uniquely generated at exact node `(z, i)`. |
| `(auth ch)` / `(conf ch)` | — | Channel `ch` is declared authenticated (`auth`) or confidential (`conf`). |
| `(gen-st t)` | — | State term `t` is declared a generated (non-initial) state value. |
| `(trans z i)` | — | Node `(z, i)` is a mutable state transition event. |
| `(state-node z i)` | — | Node `(z, i)` is a state event (`load` or `stor`). |
| `(same-locn z0 i0 z1 i1)` | — | State nodes `(z0, i0)` and `(z1, i1)` access the same storage location. |
| `(fact pred t1 ...)` | — | User-defined relational fact `(pred t1 ...)` holds in the skeleton's `(facts ...)` database. |
| `(= x y)` (or `equals`) | — | Syntactic equality between two `strd` variables or two algebra terms. **Allowed in the `conclusion` ONLY** (`Equals not allowed in antecedent`). |
| `(false)` | — | Empty disjunction (unsatisfiable conclusion). Used in secrecy goals (`(listener z k) => (false)`) and pruning rules (`(fact neq x x) => (false)`). |

### 3. `defrule` and `defgenrule` (Manual §7.7)
- **`defrule`**: Placed inside `(defprotocol ...)` after all `(defrole ...)` blocks:
  ```scheme
  (defrule rule_name
    (forall ((z strd) (p d akey))
      (implies
        (and (p "person" z 1) (p "person" "p" z p) (p "person" "d" z d) (non (invk p)))
        (non (invk d)))))
  ```
  Fires automatically as a forward-chaining rewrite axiom after every cohort step.
- **Rule Binding Invariant**: Every `strd` variable in a rule antecedent **must** be bound by a length predicate `(p "role" z h)`, and every algebra variable in the antecedent **must** be bound by a parameter predicate `(p "role" "param" z v)` or `fact` before appearing in an equality or conclusion (`In rule [...], [...] did not get a strand` / `did not get a term`).
- **`defgenrule`**: Rules automatically synthesized by CPSA (for `neq`, state transitions, critical sections, `gen-st`, `assume`, `rely`, and `guar`) and printed in the `.txt` output.

### 4. `deflemma` (Manual §7.8 & Table 10.1)
- **Grammar**: `(deflemma check rule_id prot_id sentence alist)` where `check` $\in \{\text{rule}, \text{goal}, \text{both}\}$.
- **Context**: Top-level form outside `defprotocol`.
  - `goal`: Evaluates `sentence` as a `defgoal` query without adding it as a rewrite rule.
  - `rule`: Injects `sentence` as a `defrule` named `rule_id` into `prot_id` for all subsequent skeletons/goals in the file without proving it first.
  - `both`: First generates a `defgoal` verification query to prove `sentence`, and then injects `sentence` as a `defrule` into `prot_id` to accelerate subsequent queries.

---

## Shape Analysis Sentences (`cpsa4sas` — Manual §7.6)

Running `cpsa4sas < output.txt > sas.txt` extracts a **Shape Analysis Sentence (SAS)** for each solved point-of-view skeleton.
- **Structure**: A universally quantified implication whose antecedent is the characteristic formula of the initial POV skeleton $k_0$ and whose conclusion is the disjunction $\bigvee_{i=1}^m \exists \vec{y}_i.\; \Phi(k_i)$ of the characteristic formulas of all minimal realized shapes $k_1, \dots, k_m$.
- **Completeness Property**: Because every execution compatible with $k_0$ factors through at least one shape $k_i$, the Shape Analysis Sentence is the **strongest first-order geometric theorem** true across all executions of the protocol from that point of view. If a dead secrecy query yields 0 shapes, the SAS conclusion is `(false)`.
````

---

### `refrences/cpsa_kb/01_core_rules/05_channels_state_and_macros.md`

*sha256:`99afb283f0ed` · 139 lines · 11.1 KB (~2,830 tokens) · lang:`markdown`*

````markdown
# CPSA 4.4.9 Channels, Mutable State, Heralds, and Preprocessor Macros Reference

This document provides the complete technical specification for channels (`chan`, `auth`, `conf`), long-term mutable state (`locn`, `dev`, `load`, `stor`, `gen-st`, and the five state transition axioms), file-level `herald` declarations, and preprocessor directives (`defmacro`, `include`) from MITRE CPSA 4.4.9 Manual Chapters 8 & 10.

---

## Abstract & Channeled Communication (`chan`, `auth`, `conf` — Manual §8.1)

In CPSA 4.4.9, message events can occur either over the unauthenticated public network `(send msg)` / `(recv msg)` or over explicit channels `(send ch msg)` / `(recv ch msg)`:

1. **Declaring and Using Channels**:
   - Declare channel variables with sort `chan`: `(vars (ch1 ch2 chan) ...)` (JSON AST: `{"name": "ch1", "sort": "chan"}`).
   - Attach the channel as the first argument of `send` or `recv`:
     ```scheme
     (send ch1 (cat a b n_a))
     (recv ch2 (enc session_key (ltk a b)))
     ```
   - **Mandatory in `cpsa4roletran`**: As documented in `02_roletran_and_executability_rules.md`, `cpsa4roletran` requires **every** `send` and `recv` event to specify a channel variable, and every channel variable must be included in the role's `(inputs ...)`.
   - **Compound Message Terms as Channels (CPSA 4.4.9+)**: In standalone `cpsa4` (version 4.4.9+), the channel argument of `(send ch_term msg)` may also be a compound algebra term such as `(cat a b)` representing a directional channel from `a` to `b`. If a `mesg` variable is used as a channel, it must be acquired in an earlier reception.

2. **Authenticated Channels (`auth`)**:
   - **Syntax**: `(auth ch1 ch2 ...)`
   - **Pydantic AST**: `CPSAProtocolRole.authenticated_channels: List[str]` (or in `defskeleton`).
   - **Formal Semantics**: Guarantees to the recipient of `(recv ch1 m)` that `m` was transmitted on `ch1` by a **regular protocol strand**, never forged or injected by the adversary. Note: `auth` does *not* prevent replay of a legitimate regular transmission unless fresh nonces or state bind the session.

3. **Confidential Channels (`conf`)**:
   - **Syntax**: `(conf ch1 ch2 ...)`
   - **Pydantic AST**: `CPSAProtocolRole.confidential_channels: List[str]` (or in `defskeleton`).
   - **Formal Semantics**: Guarantees to the sender of `(send ch1 m)` that the adversary **cannot eavesdrop or receive `m` directly from `ch1`**. Any reception from `ch1` must occur on a regular protocol strand.

4. **Role-Level vs. Skeleton-Level Channel Assumptions (Manual §8.1.2–8.1.3)**:
   - Placing `(auth ch)` or `(conf ch)` inside `(defrole ...)` asserts that *every* instance of that role across all concurrent sessions uses an authenticated/confidential channel.
   - Placing `(auth ch)` or `(conf ch)` inside `(defskeleton ...)` restricts the assumption to the specific strand session in that query, enabling session-independence proofs.

---

## Stateful Protocols & Mutable Memory Locations (`locn`, `load`, `stor`, `gen-st` — Manual §8.2)

While network channels remember all past messages (allowing replay), device storage registers (`locn`) are **mutable**: writing a new value to a location overwrites and erases the previous value.

### 1. Syntax for State Events (`CPSATraceEvent`)
- **Variable Sorts**:
  - `locn`: Mutable register / memory cell identifier (e.g., `(vars (key_reg door_reg locn))`).
  - `dev`: Hardware device identifier (used in compound location terms `(cat d l)` to bind location `l` to device `d`).
- **Trace Event Forms (Table 10.1)**:
  - `(load loc_term state_value)`: Reads `state_value` from `loc_term`.
  - `(stor loc_term state_value)`: Writes `state_value` into `loc_term`, overwriting its prior contents.
  - **JSON AST Mapping (`CPSATraceEvent.to_cpsa_json()`)**:
    ```json
    {"direction": "load", "location": "key_reg", "message_term": ["cat", "server_id", "k"]}
    {"direction": "stor", "location": "key_reg", "message_term": ["cat", "server_id", "k_new"]}
    ```
    *Critical Rule*: `load` and `stor` take **at most one** location term before `message_term` (`event <- (dir term? term)`). Never pass both a `chan` and a `locn` to `load`/`stor`.

### 2. State Segments, Observations, and Transitions (Manual §8.2.3)
A **state segment** is a contiguous sequence of zero or more `load` events followed by zero or more `stor` events in a role trace, subject to two well-formedness invariants:
1. No two `load` events in the same state segment may read from the same location $\ell$.
2. No two `stor` events in the same state segment may write to the same location $\ell$.
- **Transition vs. Pure Observation**:
  - A state segment is a **transition** for location $\ell$ iff it contains a `(stor l ...)` event (usually preceded by a `(load l ...)` of the old value).
  - A state segment is a **pure observation** for location $\ell$ iff it contains a `(load l ...)` event with no corresponding `(stor l ...)` in that segment.
- **Critical Section Atomicity**: CPSA automatically generates `defgenrule` axioms (`cau-<role>-<idx>` and `eff-<role>-<idx>`, Manual Fig. 8.8) ensuring that all `load` and `stor` events within a single state segment execute atomically without interleaving external events.
- **Same-Device Binding (`same-dev`)**: When a role accesses two locations `lk` and `ls` on the same device, assert `(facts (same-dev ls lk))` (`"facts": [["same-dev", "ls", "lk"]]`).

### 3. Generated State Values (`gen-st`) and the Channels-State Analogy
- Writing to a location `(stor loc v)` is analogous to sending `v` on a **confidential channel** (`conf`): the adversary cannot read `loc`.
- Reading from a location `(load loc v)` has two cases:
  1. If `v` is an unconstrained or initial power-up value, no prior `stor` strand is required to explain it.
  2. If `v` is declared in `(gen-st v)` (`CPSAProtocolRole.gen_st`), `v` is a **generated state value** (definitely non-initial). Reading a `gen-st` value from `loc` acts like receiving on an **authenticated channel** (`auth`): CPSA must find a regular protocol strand with a prior `(stor loc v)` transition that leads to (`leadsto`, $n_0 \leadsto n_1$) this `load`.

---

## The Five State Transition Axioms & Derived Rules (Manual §8.2.1–8.2.2)

When a transition event $n_0$ writes value $v$ into location $\ell$ and a subsequent state event $n_1$ reads $v$ from $\ell$ with no intervening transition on $\ell$, CPSA records the **leads-to** relation $n_0 \leadsto n_1$ (`(leadsto ((s0 i0) (s1 i1)))` in skeletons, `(leads-to z0 i0 z1 i1)` in goals).

To enforce the past-erasing semantics of mutable memory on a single location $\ell$, CPSA enforces two fundamental discreteness axioms and three non-disjunctive derived consequences:

| Rule / Axiom | Formal Condition (on Location $\ell$) | Conclusion | Operational Meaning |
|---|---|---|---|
| **1. Discrete-After Axiom** | Transition $n \leadsto m_0$ (where $m_0$ is a transition) and $n \prec m_1$ (where $m_1$ is a transition) | $m_0 \preceq m_1$ ($m_0 = m_1 \lor m_0 \prec m_1$) | Any other transition $m_1$ following $n$ must occur at or after the transition $m_0$ that directly consumed $n$'s state. |
| **2. Discrete-Before Axiom** | Transition $m_0 \prec n$ and transition $m_1 \leadsto n$ | $m_0 \preceq m_1$ ($m_0 = m_1 \lor m_0 \prec m_1$) | Any transition $m_0$ preceding $n$ must have occurred at or before the transition $m_1$ that directly supplied $n$'s state. |
| **3. Scissors Rule** | Node $n \leadsto m_0$ and $n \leadsto m_1$, where both $m_0$ and $m_1$ are transitions | $m_0 = m_1$ | A single state write $n$ can be overwritten by **at most one** immediate successor transition (the two blades of the scissors snap shut). |
| **4. No Interruption Rule** | Transition $n_0 \leadsto n_1$ and transition $m$ satisfies $n_0 \prec m \prec n_1$ | `(false)` | No transition $m$ on location $\ell$ can occur strictly between $n_0$ and the event $n_1$ to which $n_0$ leads. |
| **5. Cake Rule** | Node $n_0 \leadsto n_1$ (where $n_1$ is a transition), $n_0 \leadsto m$ (observation), and $n_1 \prec m$ | `(false)` | "You cannot eat your cake at transition $n_1$ and still observe it later at $m$": once $n_1$ overwrites $n_0$'s value, no later event $m$ can read $n_0$'s old value. |

---

## Top-Level `herald` Declarations and Options (Manual §10.5.1)

Every `.scm` file should begin with a `(herald ...)` declaration (Table 10.1):
```scheme
(herald "Protocol Title"
  (algebra diffie-hellman)
  (bound 16)
  (limit 2000)
  (depth 10)
  (goals-sat)
  (try-old-strands)
  (reverse-nodes)
  (check-nonces)
  (margin 72))
```

| Herald Option | CLI Equivalent | Default | Semantics |
|---|---|---|---|
| `(algebra <alg>)` | `-a STRING` | `basic` | Sets the file-wide algebra (`basic` or `diffie-hellman`). Mandatory in herald when `defprotocol` uses `diffie-hellman`. |
| `(bound <int>)` | `-b INT` | `12` | Maximum number of strands permitted in any skeleton before aborting with `Strand bound exceeded`. |
| `(limit <int>)` | `-l INT` | `2000` | Maximum number of skeletons processed per query before aborting with `Step limit exceeded`. |
| `(depth <int>)` | `-d INT` | $\infty$ | Maximum derivation tree depth; deeper unrealized skeletons are marked `(fringe)` without error. |
| `(goals-sat)` | `-g` | Off | Stops exploring search branches as soon as the `defgoal` is satisfied on an intermediate skeleton. |
| `(try-old-strands)` | `-t` | Off | Prioritizes unrealized nodes on older (leftmost) strands over newer (rightmost) strands. |
| `(reverse-nodes)` | `-r` | Off | Prioritizes younger (bottom-most) unrealized nodes on a strand over older (topmost) nodes. |
| `(check-nonces)` | `-c` | Off | Prioritizes restricted nonces over encryptions when selecting critical terms at an unrealized node. |
| `(noisochk)` | `-n` | Off | Disables isomorphism pruning (almost never desired; causes non-termination). |
| `(margin <int>)` | `-m INT` | `72` | Output line-wrapping width in characters. |

*Note*: CLI flags override herald options. The CLI flags `output` (`-o`), `help` (`-h`), `version` (`-v`), and `show-algebras` (`-s`) are **not** allowed inside `(herald ...)`.

---

## Preprocessor Directives: `defmacro` and `include` (Manual §10.1)

CPSA runs a textual S-expression preprocessor before parsing protocols and skeletons. You can inspect macro-expanded output without running the solver using `cpsa4 -e input.scm`.

### 1. `defmacro` (Positional Macro Expansion & `^` Splicing)
- **Grammar**: `(defmacro (macro_name arg1 arg2 ...) body)`
- **Semantics**: Replaces every call `(macro_name val1 val2 ...)` in subsequent forms with `body`, substituting `arg_i` $\mapsto$ `val_i`.
- **Example**:
  ```scheme
  (defmacro (signed-hash m signer)
    (cat m (enc (hash m) (privk signer))))
  ```
- **Multi-Event Splicing (`^`)**: If a macro body begins with `(^ event1 event2 ...)`, calling the macro inside a list (such as `(trace (handshake-prefix a b) (send ...))`) splices `event1 event2 ...` directly into the enclosing list!
- **Recursion Limit**: Macro expansion depth is capped at 1000 (`Expansion limit exceeded`).

### 2. `include` (Relative File Inclusion)
- **Grammar**: `(include "relative/path/to/file.scm")`
- **Constraints**: Only **relative paths** are permitted. Inclusion depth is capped at 16 (`Include depth exceeded with file [...]`).
````

---

### `refrences/cpsa_kb/01_core_rules/06_termination_and_anti_snowballing.md`

*sha256:`6a196582c239` · 112 lines · 9.7 KB (~2,489 tokens) · lang:`markdown`*

````markdown
# CPSA 4.4.9 State-Space Termination and Anti-Snowballing Reference

This document details the root causes of 60-second `cpsa4` state-space explosions ("snowballing" / infinite strand loops) in `src/verification_engine/mitre_build_orchestrator.py` and provides exact structural AST fixes and search flag configurations to guarantee rapid termination.

---

## Why `cpsa4` Times Out or Hits `Step limit exceeded` (Snowballing Mechanics)

Because cryptographic protocol verification in an unbounded Dolev-Yao strand space is Turing-undecidable in general (Manual §9.1), `mitre_build_orchestrator.py` enforces a hard **60-second timeout** (`CPSA_TIMEOUT_SECONDS = 60`) and `cpsa4` enforces a default **2,000-skeleton step limit** (`limit = 2000`) and **12-strand bound** (`bound = 12`).

When `cpsa4` hits `MITRE CPSA compilation timed out after 60 seconds (state-space explosion / infinite strand loop)` or `Step limit exceeded`, the solver is almost never "just slow"—it is caught in an **algebraic unification cycle (snowballing)** where solving an authentication test on Strand $k$ spawns an isomorphic unrealized reception on Strand $k+1$ ad infinitum.

---

## Cause 1: Symmetric Request/Response `(enc ...)` Arity & Key Unification

### The Mechanism
Suppose an Initiator sends a Request ciphertext and receives a Response ciphertext encrypted under the same symmetric key (or same key constructor family `(ltk A B)` or `session_key`), and both ciphertexts have the **exact same tuple arity and sort pattern**:
```scheme
;; ANTI-PATTERN: Request and Response have identical 2-element (enc text name skey) structure!
(defrole initiator
  (vars (ch chan) (a b name) (na nb text) (k skey))
  (trace
    (send ch (enc na a k))
    (recv ch (enc nb b k))))

(defrole responder
  (vars (ch chan) (a b name) (na nb text) (k skey))
  (trace
    (recv ch (enc na a k))
    (send ch (enc nb b k))))
```
When CPSA tries to explain the Responder's reception `(recv ch (enc na a k))`, it sees that the Responder's own outbound transmission `(send ch (enc nb b k))` has the **exact same algebraic shape** `(enc <text> <name> <skey>)`! Consequently, CPSA's cohort generator adds a second Responder strand whose output feeds the first Responder's input, which requires a third Responder strand to feed the second Responder's input, branching exponentially until the 60-second timeout or strand bound is exhausted.

### Structural AST Fix
**Always make Request and Response ciphertexts structurally incapable of unifying with each other** by using distinct tuple arities, distinct sort sequences, or explicit string direction tags inside `(enc ...)`:
```json
// FIXED JSON AST: Request has 2 elements + key; Response has 3 elements + key (or explicit tag)
{
  "direction": "send",
  "channel": "handshake_channel",
  "message_term": ["enc", "client_nonce", "client_identity", "session_key"]
},
{
  "direction": "recv",
  "channel": "handshake_channel",
  "message_term": ["enc", "client_nonce", "server_nonce", "server_identity", "session_key"]
}
```
Because a 3-element plaintext tuple `(cat client_nonce server_nonce server_identity)` is right-associated as `(client_nonce, (server_nonce, server_identity))` where the second projection is a pair rather than an atomic `name`, a Response ciphertext can **never** unify with a Request reception `(enc client_nonce client_identity session_key)`.

---

## Cause 2: `(ltk A B)` Self-Unification and Reflection (`A = B`)

### The Mechanism
In protocols using long-term symmetric keys `(ltk client_identity server_identity)` or bidirectional keys `(bltk client_identity server_identity)`:
1. Even though `(ltk a b)` is directional when $a \ne b$, CPSA's unification engine freely considers the substitution $\sigma = \{a \mapsto b\}$ unless explicitly forbidden! Under $a = b$, `(ltk a b)` becomes `(ltk b b)`, making `(ltk a b)` and `(ltk b a)` identical!
2. Furthermore, as documented in the official Hackage CPSA 4.4.9 release notes (`hackage_cpsa_overview.md` line 285):
   > *"KNOWN BUGS: Variable separation in generalization fails to separate variables in terms of the form `(ltk a a)`."*
3. When $a = b$ unifies, any role that receives a message encrypted under `(ltk a b)` and sends a message encrypted under `(ltk b a)` (or `(ltk a b)`) can chain into itself infinitely.

### Structural AST Fix
1. **Enforce Distinct Principal Identities in Preskeletons**: Add `"facts": [["neq", "client_identity", "server_identity"]]` to `CPSAPreskeleton` so CPSA's built-in `neq` rule immediately kills any branch that unifies `client_identity = server_identity`.
2. **Ensure Asymmetric/Directional Inner Structure**: Bind the sender's and receiver's identities or distinct nonces in asymmetric positions inside the encrypted payload so `(enc ... (ltk a b))` cannot unify with a reflection.

---

## Cause 3: Overly Nested `(hash (cat ...))` Inside `(enc ...)` and Split Keys

### The Mechanism
1. **Redundant Nested Hashes Inside `enc`**: In CPSA's Dolev-Yao model, `(enc m1 m2 k)` is already authenticated encryption (unforgeable without `k`). Wrapping multiple nested `(enc (cat a b (hash (cat c d (hash e)))) k)` layers inside a trace forces CPSA to perform multi-way unification across deep term trees at every cohort contraction step.
2. **Split Encryption and MAC Keys**: If a role sends `(cat (enc payload k_enc) (hash payload k_mac))` using two separate keys `k_enc` and `k_mac` that are both derived or distributed across multiple strands, CPSA must independently solve authentication tests for `k_enc` (which could come from Strand $S_1$) and `k_mac` (which could come from Strand $S_2$), squaring the cohort branching factor at every step (`termination.md`).

### Structural AST Fix
1. **Flatten Inner Payloads**: Keep `(enc m1 m2 ... k)` flat—pass the core nonces, identities, and secrets directly as arguments to `enc` rather than wrapping them in redundant `(cat ...)` or nested `(hash (cat ...))` layers inside `enc`.
2. **Keep Role Traces Concise (2 to 4 Handshake Events)**: Model the essential cryptographic handshake flights (typically 2 to 4 `send`/`recv` events per role). Drop decorative plaintext acks or post-handshake data exchanges that do not introduce new cryptographic bindings.
3. **Eliminate Passenger Variables**: Remove any `text` or `data` variable that is carried through messages without being bound to a freshness assumption (`uniq-orig`) or security goal.

---

## Cause 4: The Mutable State `gen-st` Non-Termination Trap (Manual §8.2.4)

### The Mechanism
In stateful protocols using `load` and `stor` (Manual §8.2.4 & `state.md`):
- Suppose an initial state value $v_0$ can only be produced by an initial load, and a state transition role reads a state value and writes a new state value $v_{i+1}$ that is declared `(gen-st ...)`.
- Because `gen-st` forces CPSA to explain every `load` of a `gen-st` value by adding an earlier `stor` transition strand, and runs with $0, 1, 2, \dots, n$ state transitions have **no homomorphisms between them** when the initial value is distinguished from transition values, the protocol has **infinitely many distinct shapes**! CPSA will never terminate regardless of search flags.

### Structural AST Fix
- Restrict `gen-st` strictly to state forms whose predecessors do not distinguish arbitrary-length transition histories, or model single-session protocols using standard `send`/`recv` channels without unnecessary `load`/`stor` state cells.

---

## Search Flags & Herald Tuning (`bound`, `limit`, `depth`, `goals-sat`, Search Order)

When analyzing a complex protocol in standalone `cpsa4`, the following `herald` / CLI options control termination and search order (Manual §9.1 & §10.5):

| Option | Herald Syntax | CLI Flag | Effect on Termination & Completeness |
|---|---|---|---|
| **Strand Bound** | `(bound 10)` | `-b 10` | **Hard cap on concurrent strands per skeleton** (default `12`). Best way to bound the modeled world ("verified for all runs up to $N$ strands"). Aborts with `Strand bound exceeded` if hit. |
| **Step Limit** | `(limit 2000)` | `-l 2000` | **Hard cap on total skeletons analyzed** (default `2000`). Raising it increases memory consumption; hitting it marks output `(aborted)`. |
| **Depth Limit** | `(depth 8)` | `-d 8` | **Soft cap on derivation tree depth** (default $\infty$). Never errors; marks unanalyzed skeletons at depth $D$ as `(fringe)`. Ideal for diagnosing which branch is exploding. |
| **Goals Satisfaction Pruning** | `(goals-sat)` | `-g` | **Semantic branch pruning**: checks `defgoal` at every intermediate skeleton and immediately stops expanding any branch where the goal is already satisfied. Huge speedup when verifying `defgoal` specifications. |
| **Try Old Strands First** | `(try-old-strands)` | `-t` | Solves unrealized receptions on the **leftmost (oldest)** strand instead of the rightmost (newest) strand. Prevents CPSA from chasing newly added responder strands into an infinite chain before closing the POV strand! |
| **Reverse Nodes** | `(reverse-nodes)` | `-r` | Solves the **bottom-most (youngest)** unrealized node on a strand before the topmost (oldest) node. |
| **Check Nonces First** | `(check-nonces)` | `-c` | Selects the smallest critical term (restricted nonce) instead of the largest enclosing encryption when solving an authentication test. |
| **GHC Heap Limit** | N/A (CLI only) | `+RTS -M4g -N -RTS` | Bounds GHC runtime heap to 4 GB and enables multicore parallelism (`-N`) to prevent OS swap thrashing. |

### Diagnosing a Stuck or Large Run (`reading-output.md`)
When inspecting a partial or aborted `.txt` output file to locate the source of snowballing:
1. Count total vs. realized skeletons: `grep -c "defskeleton" out.txt` vs. `grep -c "(realized)" out.txt`.
2. Inspect the primed-variable histogram (`x-0`, `x-1`, `x-2`): the variable with the highest primed count (`VAR-0`, `VAR-1`) is the exact parameter where CPSA is manufacturing new strands at every step.
````

---

### `refrences/cpsa_kb/01_core_rules/07_compiler_and_solver_error_catalog.md`

*sha256:`065ded1b6bde` · 429 lines · 49.5 KB (~12,629 tokens) · lang:`markdown`*

````markdown
# CPSA 4.4.9 Exhaustive Compiler, Roletran, and Solver Error Diagnostic Catalog

This document provides the complete, zero-hallucination reference catalog of every error diagnostic emitted by the official Hackage `cpsa-4.4.9` Haskell modules (`CPSA.Roletran.Protocol`, `CPSA.Roletran.Derivation`, `CPSA.Roletran.Loader`, `CPSA.Loader`, `CPSA.Algebra`, `CPSA.LoadFormulas`, `CPSA.Strand`, `CPSA.Characteristic`, `CPSA.Signature`, `CPSA.JSON.Main`, `CPSA.Lib.SExpr`, `CPSA.Lib.Expand`, `CPSA.Shapes.Shapes`, `CPSA.Graph.Loader`) and the Pydantic AST validators in `src/intermediate_representation/protocol_syntax_tree.py`.

Every entry specifies:
1. **Exact Compiler Error String** (verified directly against the `cpsa-4.4.9/src/CPSA/*.hs` Haskell source code and Manual Chapter 9.2)
2. **Emitting Tool & Haskell Source Location** (`module :: function (File.hs:line)`)
3. **Root Cause in CPSA Semantics**
4. **Exact JSON AST Field to Fix in `CPSAProtocolSpecification`**
5. **Before / After JSON & Scheme Repair Example**

---

## Section 1: `cpsa4roletran` Procedural Executability Diagnostics (`CPSA.Roletran.*`)

## 1.1 `Received term cannot be fully destructured`
- **Emitting Tool & Source**: `cpsa4roletran` — `CPSA.Roletran.Derivation :: loop` (`Roletran/Derivation.hs:217`)
- **Root Cause in CPSA Semantics**: During the fixed-point destructuring loop (`reduce` / `loop`) on a `(recv ch term)` event, at least one subterm remains in the `todo` queue (`loop pos _ False [] (_ : _)`) after a full pass with no progress (`more == False`). This happens when:
  1. The received term contains an encryption `(enc x y)` (`loopEncr`), and `synth st (inv y)` returns `Nothing` because the role does **not** possess the inverse decryption key $\text{inv}(y)$ at that point in the trace; OR
  2. The received term contains a one-way hash `(hash x)` (`loopHash`), and `synth st (Hsh x)` returns `Nothing` because the role cannot locally synthesize `(hash x)` from its compile-time store `compStore` to compare via `Same`.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.inputs` (add the required decryption key, e.g., `["privk", "server_identity"]`, `["pubk", "client_identity"]`, `["ltk", "client_identity", "server_identity"]`, or symmetric key variable `"psk"`, or preimage inputs needed to verify `(hash x)`) or `CPSAProtocolRole.trace` (ensure any dynamically negotiated key is received in an earlier carried position before it is used to decrypt).
- **Before / After Fix Example**:
  - *Failing JSON (`server` role receives message encrypted under `(pubk server_identity)` but lacks `(privk server_identity)` in `inputs`)*:
    ```json
    "trace": [
      {"direction": "recv", "channel": "ch", "message_term": ["enc", "client_nonce", ["pubk", "server_identity"]]}
    ],
    "inputs": ["ch", "server_identity"]
    ```
  - *Repaired JSON*:
    ```json
    "trace": [
      {"direction": "recv", "channel": "ch", "message_term": ["enc", "client_nonce", ["pubk", "server_identity"]]}
    ],
    "inputs": ["ch", "server_identity", ["privk", "server_identity"]]
    ```
  - *Repaired Scheme*:
    ```scheme
    (inputs ch server_identity (privk server_identity))
    ```

## 1.2 `Cannot build <term>`
- **Emitting Tool & Source**: `cpsa4roletran` — `CPSA.Roletran.Derivation :: build` (`Roletran/Derivation.hs:142`)
- **Root Cause in CPSA Semantics**: `synth st t` returned `Nothing` while compiling a `(send ch <term>)` event (`deriveEvent`) or an `(outputs ...)` return value (`deriveOutput`). A role attempts to synthesize `<term>`, but `<term>` (or one of its subterms/encryption keys) is not in `compStore`—meaning it was neither bound from `rinputs` (`inputs`), bound via `Frsh` from `runiques` (`uniq-orig`) at its origination index `i == j`, nor extracted into `compStore` from a prior `recv` event. **Alternative Root Cause**: A symmetric key variable used as the last argument of `["enc", payload, "k"]` was declared with sort `"data"` or `"text"` instead of `"skey"`.
- **Exact JSON AST Field to Fix**:
  1. If `<term>` is a fresh nonce or session key generated by this role at this `send` step: add `"<term>"` to `CPSAProtocolRole.unique_originating`.
  2. If `<term>` is a known identity, channel, peer public key `["pubk", "b"]`, own private signing key `["privk", "a"]`, or long-term key `["ltk", "a", "b"]`: add it to `CPSAProtocolRole.inputs`.
  3. If `<term>` is an `(enc ... k)` expression where `k` is a symmetric key variable: change `k`'s `sort` in `CPSAProtocolRole.variables` to `"skey"`.
- **Before / After Fix Example**:
  - *Failing JSON (`client_nonce` sent without being in `unique_originating`, and `(pubk server_identity)` missing from `inputs`)*:
    ```json
    "trace": [
      {"direction": "send", "channel": "ch", "message_term": ["enc", "client_nonce", ["pubk", "server_identity"]]}
    ],
    "unique_originating": [],
    "inputs": ["ch"]
    ```
  - *Repaired JSON*:
    ```json
    "trace": [
      {"direction": "send", "channel": "ch", "message_term": ["enc", "client_nonce", ["pubk", "server_identity"]]}
    ],
    "unique_originating": ["client_nonce"],
    "inputs": ["ch", ["pubk", "server_identity"]]
    ```

## 1.3 `Message not receivable <term>`
- **Emitting Tool & Source**: `cpsa4roletran` — `CPSA.Roletran.Derivation :: deriveEvent` & `deriveOutput` (`Roletran/Derivation.hs:100, 115, 327`) calling `CPSA.Roletran.Algebra :: receivable` (`Roletran/Algebra.hs:190–209`)
- **Root Cause in CPSA Semantics**: `receivable t` returned `Just <offending_enc_term>` on a `send` event, `recv` event, or `outputs` term. In `Roletran/Algebra.hs`, a message `t` is receivable iff:
  1. `t` contains **no** encryption `(enc ...)` inside the **key position** of an encryption (`receivable (En x y)` checks `findEnc y`), AND
  2. `t` contains **no** encryption `(enc ...)` inside a **hash** (`receivable (Hsh x)` checks `findEnc x`).
  Because real-world encryption is probabilistic, hashing a ciphertext `(hash (enc m k))` or encrypting with a ciphertext `(enc m (enc k1 k2))` breaks adequacy between symbolic and probabilistic execution.
- **Exact JSON AST Field to Fix**: `CPSATraceEvent.message_term` and `CPSAProtocolRole.outputs`. Never nest `["enc", ...]` inside `["hash", ...]` or inside the key slot (last argument) of `["enc", ..., key]`. Hash the plaintext components `["hash", "m"]` or encrypt the hash `["enc", ["hash", "m"], "k"]`.
- **Before / After Fix Example**:
  - *Failing JSON (hashing a ciphertext)*:
    ```json
    "message_term": ["hash", ["enc", "client_nonce", "session_key"]]
    ```
  - *Repaired JSON (encrypting a hash or hashing plaintext with key)*:
    ```json
    "message_term": ["enc", ["hash", "client_nonce"], "session_key"]
    ```

## 1.4 `Input is not a basic value or a channel <term>` / `Expecting a basic value`
- **Emitting Tool & Source**:
  - `Input is not a basic value or a channel <term>`: `cpsa4roletran` — `CPSA.Roletran.Protocol :: checkInput` (`Roletran/Protocol.hs:96`)
  - `Expecting a basic value`: `cpsa4roletran` — `CPSA.Roletran.Loader :: loadBasic` (`Roletran/Loader.hs:169`)
- **Root Cause in CPSA Semantics**:
  - `checkInput` requires `isBasic input || isChanVar input`. In `Roletran/Algebra.hs:100`, `isBasic` is `True` **only** for `Txt`, `Dta`, `Nam`, `Sky` (`skey` var or `(ltk a b)`), `Aky` (`akey` var or `(pubk ...)`), and `Iky` (`(privk ...)` or `(invk ...)`). Compound terms built with `Pr` (`cat`), `En` (`enc`), `Hsh` (`hash`), or `Tag` (`"..."`) return `False`!
  - `loadBasic` requires `isBasic t == True` for every element of `(uniq-orig ...)`.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.inputs` and `CPSAProtocolRole.unique_originating` — replace any compound `cat`/`enc`/`hash` expression or string literal tag with its constituent atomic variables or key constructors (`pubk`, `privk`, `invk`, `ltk`).
- **Before / After Fix Example**:
  - *Failing JSON*: `"inputs": ["ch", ["hash", "shared_secret"]]`
  - *Repaired JSON*: `"inputs": ["ch", "shared_secret"]`

## 1.5 `Uniquely originating value in input <term>`
- **Emitting Tool & Source**: `cpsa4roletran` — `CPSA.Roletran.Protocol :: checkUniq` (`Roletran/Protocol.hs:101`)
- **Root Cause in CPSA Semantics**: `elem unique inputs == True`. The same term is listed in **both** `unique_originating` (`uniq-orig`) and `inputs` (`inputs`/`params`). In `CPSA.Roletran`, `inputs` (caller-supplied parameters) and `uniq-orig` (fresh values generated mid-procedure via `Frsh`) must be strictly disjoint.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.inputs` or `CPSAProtocolRole.unique_originating`. Remove `<term>` from `inputs` if it is a fresh nonce/key generated by this role; remove `<term>` from `unique_originating` if it is a pre-existing parameter passed into this role.
- **Before / After Fix Example**:
  - *Failing JSON*: `"unique_originating": ["client_nonce"], "inputs": ["ch", "client_nonce"]`
  - *Repaired JSON*: `"unique_originating": ["client_nonce"], "inputs": ["ch"]`

## 1.6 `Uniquely originating value <term> does not originate in trace`
- **Emitting Tool & Source**: `cpsa4roletran` — `CPSA.Roletran.Protocol :: addPos` & `originationPos` (`Roletran/Protocol.hs:31–41, 108`)
- **Root Cause in CPSA Semantics**: `originationPos unique trace` returned `Nothing`. Looking at `Roletran/Protocol.hs:31–41` and `Roletran/Algebra.hs:172–178`:
  - `carriedBy t t'` is `True` **only** when `t == t'`, `t` is carried in `Pr x y` (`cat`), or `t` is carried in the **plaintext** `x` of `En x _` (`enc`).
  - `originationPos` returns `Nothing` if `unique` first appears in an `In` (`recv`) event (`t carriedBy t'`), OR if `unique` only appears inside `Hsh _` (`hash`) or in the key slot of `En _ k` (`enc`), OR if `unique` never appears in the trace.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.unique_originating` and `CPSAProtocolRole.inputs`. If `<term>` is received from the peer or is a pre-shared key/secret only used inside `(hash ...)` or as an encryption key, remove `<term>` from `unique_originating` (and add it to `inputs` if known prior to execution). If `<term>` is a fresh nonce that *should* originate, ensure it is transmitted in a carried position (`cat` or plaintext of `enc`) in an outbound `send` before any `recv` carrying it.
- **Before / After Fix Example**:
  - *Failing JSON (`secret_token` only sent inside `["hash", "secret_token"]`)*:
    ```json
    "trace": [{"direction": "send", "channel": "ch", "message_term": ["hash", "secret_token"]}],
    "unique_originating": ["secret_token"],
    "inputs": ["ch"]
    ```
  - *Repaired JSON (if `secret_token` is a pre-shared secret)*:
    ```json
    "trace": [{"direction": "send", "channel": "ch", "message_term": ["hash", "secret_token"]}],
    "unique_originating": [],
    "inputs": ["ch", "secret_token"]
    ```

## 1.7 `Output contains an input value <term>`
- **Emitting Tool & Source**: `cpsa4roletran` — `CPSA.Roletran.Protocol :: checkOutput` (`Roletran/Protocol.hs:114`)
- **Root Cause in CPSA Semantics**: `elem output inputs == True`. A term listed in `outputs` (`(outputs ...)` / `(returns ...)`) is also present in `inputs` (`(inputs ...)` / `(params ...)`). `CPSA.Roletran` forbids returning a caller-supplied input parameter as a procedure return value.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.outputs` — remove any term that already appears in `CPSAProtocolRole.inputs`.
- **Before / After Fix Example**:
  - *Failing JSON*: `"inputs": ["ch", "client_id"], "outputs": ["client_id", "session_key"]`
  - *Repaired JSON*: `"inputs": ["ch", "client_id"], "outputs": ["session_key"]`

## 1.8 `Undeclared variable <v>` / `Malformed terms`
- **Emitting Tool & Source**: `cpsa4roletran` — `CPSA.Roletran.Loader :: loadRole`, `loadChan`, `loadLookup` (`Roletran/Loader.hs:78, 157, 174`)
- **Root Cause in CPSA Semantics**:
  - In `Roletran/Loader.hs:75–86`, `loadRole` first loads `declEnv <- loadVars vars`, then parses the trace `c <- loadTrace declEnv`, and then computes `traceWellFormed c` **starting from `emptyVarEnv`** (`foldM eventWellFormed emptyVarEnv c`)!
  - Consequently, `Just env` returned by `traceWellFormed c` contains **only variables that actually appeared in the trace `c`**! When `u`, `i`, and `o` (`uniq-orig`, `inputs`, `outputs`) are subsequently loaded against `env` (lines 81–85), **any variable declared in `(vars ...)` that did NOT appear in `(trace ...)` is missing from `env` and triggers `Undeclared variable <v>`**!
  - `Malformed terms` (line 78) occurs when `traceWellFormed c` returns `Nothing` (a variable was used with conflicting sorts).
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.variables`, `CPSAProtocolRole.inputs`, `CPSAProtocolRole.outputs`, `CPSAProtocolRole.unique_originating`, and `CPSAProtocolRole.trace`. Ensure every variable in `inputs`, `outputs`, `unique_originating`, and `variables` appears in at least one `send`/`recv` event in `trace`.
- **Before / After Fix Example**:
  - *Failing Scheme*:
    ```scheme
    (defrole client
      (vars (ch chan) (n text) (unused_id name))
      (trace (send ch n))
      (uniq-orig n)
      (inputs ch unused_id))
    ```
  - *Repaired Scheme*:
    ```scheme
    (defrole client
      (vars (ch chan) (n text))
      (trace (send ch n))
      (uniq-orig n)
      (inputs ch))
    ```

## 1.9 `Missing channel` / `Expecting a channel` / `Not expecting a channel` / `Not expecting an ikey`
- **Emitting Tool & Source**: `cpsa4roletran` — `CPSA.Roletran.Loader :: loadEvt`, `loadChan`, `loadLookup` (`Roletran/Loader.hs:109, 159, 161, 180, 182`)
- **Root Cause in CPSA Semantics**:
  - `Missing channel` (`Roletran/Loader.hs:109`): A trace event has only 2 elements `(send <term>)` or `(recv <term>)` instead of 3 elements `(send <chan> <term>)` or `(recv <chan> <term>)`.
  - `Expecting a channel` (`Roletran/Loader.hs:159, 161`): The channel argument in `(send <ch> <term>)` or `(recv <ch> <term>)` is either not a symbol or is declared in `(vars ...)` with a sort other than `chan`.
  - `Not expecting a channel` (`Roletran/Loader.hs:182`): A variable declared with sort `chan` was used inside a message term `t`, `outputs`, or `uniq-orig` (where `loadTerm` calls `loadLookup`). Channels are only allowed in the channel slot of `send`/`recv` and in `inputs` (`loadChanTerm`).
  - `Not expecting an ikey` (`Roletran/Loader.hs:180`): Internal guard against bare `Ikey` sort lookup in `loadLookup`.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.trace`, `CPSAProtocolRole.variables`, `CPSAProtocolRole.inputs`, and `CPSAProtocolRole.outputs`. Every `CPSATraceEvent` must have `"channel": "ch"`, `"ch"` must have `"sort": "chan"` in `variables`, `"ch"` must be in `inputs`, and `"ch"` must never appear inside `message_term` or `outputs`.

## 1.10 `Expecting terms in basic algebra ` / `No protocol found`
- **Emitting Tool & Source**: `cpsa4roletran` — `CPSA.Roletran.Loader :: loadSExprs`, `loadProt` (`Roletran/Loader.hs:38, 43`)
- **Root Cause in CPSA Semantics**:
  - `Expecting terms in basic algebra `: `alg /= "basic"` in `(defprotocol <name> <alg> ...)`. `cpsa4roletran` only supports `basic` algebra.
  - `No protocol found`: Input contained no `(defprotocol ...)` S-expression.
- **Exact JSON AST Field to Fix**: Handled automatically in `roletran_executability_gate.py` by routing `diffie-hellman` protocols to `cpsa4 -l 1`. If the protocol does not use Diffie-Hellman exponentiation, set `CPSAProtocolSpecification.message_algebra` to `"basic"`.

---

## Section 2: Algebra, Sort, and Operator Diagnostics (`CPSA.Algebra`, `CPSA.Roletran.Loader`, `CPSA.Signature`)

## 2.1 `Algebra.inv: Cannot invert a variable of sort mesg` / `Message variable cannot used as key`
- **Emitting Tool & Source**:
  - `Message variable cannot used as key`: `cpsa4roletran` — `CPSA.Roletran.Loader :: loadEnc` (`Roletran/Loader.hs:279`)
  - `Algebra.inv: Cannot invert a variable of sort mesg`: `cpsa4` — `CPSA.Algebra` (Equation 10.1)
- **Root Cause in CPSA Semantics**: Violation of MITRE CPSA 4.4.9 Equation 10.1 (`isMesgVar t' == True` on the last argument of `enc`). A variable declared with `"sort": "mesg"` was used as the encryption key (the last element) of an `["enc", ..., "<mesg_var>"]` term. Because `mesg` is the top sort, CPSA cannot determine whether its inverse is `k` (symmetric) or `(invk k)` (asymmetric).
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.variables` and `CPSAPreskeleton.variables` — change the key variable's `sort` from `"mesg"` to `"skey"` (for symmetric encryption) or `"akey"` (for asymmetric encryption).
- **Before / After Fix Example**:
  - *Failing JSON*: `{"name": "session_key", "sort": "mesg"}` with `["enc", "payload", "session_key"]`
  - *Repaired JSON*: `{"name": "session_key", "sort": "skey"}` with `["enc", "payload", "session_key"]`

## 2.2 `Expecting a name` / `Expecting <name> to be a name` / `Expecting <name> to be an akey` / `Expecting an akey` / `Terms in [role/skeleton] not well formed`
- **Emitting Tool & Source**:
  - `Expecting a name`: `cpsa4roletran` — `CPSA.Roletran.Loader :: loadName` (`Roletran/Loader.hs:196`)
  - `Expecting <name> to be a name`: `cpsa4` — `CPSA.Algebra :: loadLookupName` (`Algebra.hs:2546`)
  - `Expecting <name> to be an akey` / `Expecting an akey`: `cpsa4` — `CPSA.Algebra :: loadLookupAkey`, `loadInvk` (`Algebra.hs:2554, 2689`)
  - `Terms in role not well formed` / `Terms in skeleton not well formed`: `cpsa4` — `CPSA.Loader :: loadRole`, `loadRest` (`Loader.hs:182, 1207`) calling `CPSA.Algebra :: termsWellFormed` (`Algebra.hs:617`)
- **Root Cause in CPSA Semantics**: Sort mismatch in a key constructor call:
  1. `pubk`, `privk`, `ltk`, or `bltk` was passed a variable declared with sort `akey`, `skey`, `text`, `data`, or `mesg` instead of a principal identifier of sort `name`.
  2. `(invk <var>)` in `cpsa4` (`Algebra.hs:2659`) requires `<var>` to be an `akey` variable (or `(pubk ...)` / `(privk ...)` / `(invk ...)`). Passing a `name` or `skey` variable to `invk` triggers `Expecting <var> to be an akey`.
- **Exact JSON AST Field to Fix**:
  - Either change the variable's `sort` in `variables` to `"name"` (if it represents a principal identity in `["pubk", id]`, `["privk", id]`, `["ltk", id1, id2]`),
  - Or if the variable `k` is already declared with `"sort": "akey"`, unwrap `["pubk", "k"]` $\to$ `"k"` and replace `["privk", "k"]` $\to$ `["invk", "k"]`.
- **Before / After Fix Example**:
  - *Failing Scheme*: `(vars (k akey)) ... (send ch (enc n (pubk k)))`
  - *Repaired Scheme*: `(vars (k akey)) ... (send ch (enc n k))` (or `(vars (server_id name)) ... (send ch (enc n (pubk server_id)))`)

## 2.3 `Malformed pubk` / `Malformed privk` / `Malformed invk` / `Malformed ltk` / `Malformed bltk` / `Malformed cat` / `Malformed enc` / `Malformed hash` / `Malformed gen` / `Malformed exponentiation` / `Malformed base` / `Malformed exponent` / `Malformed one` / `Malformed rec`
- **Emitting Tool & Source**: `cpsa4` (`CPSA.Algebra`, `Algebra.hs:2645–2816`) and `cpsa4roletran` (`CPSA.Roletran.Loader`, `Roletran/Loader.hs:233–294`)
- **Root Cause in CPSA Semantics**: Operator arity or argument syntax violation against Tables 10.3 & 10.5:
  - `Malformed pubk` / `Malformed privk`: Must have arity 1 `(pubk <name_sym>)` or arity 2 `(pubk "<tag_str>" <name_sym>)` where the **first** argument in 2-arg form is a quoted string `Q` and the **second** is a `name` symbol `S`. Reversing them `(pubk <name_sym> "<tag_str>")`, passing a compound expression, or passing $\ge 3$ arguments triggers `Malformed pubk`.
  - `Malformed invk`: Must have exact arity 1 `(invk <akey_term>)`.
  - `Malformed ltk` / `Malformed bltk`: Must have exact arity 2 `(ltk <name_sym1> <name_sym2>)` where both arguments are symbols of sort `name`.
  - `Malformed enc`: Must have arity $\ge 2$ `(enc <term>+ <key>)`. Calling `(enc x)` with 1 argument triggers `Malformed enc`.
  - `Malformed cat` / `Malformed hash`: Must have arity $\ge 1$. Calling `(cat)` or `(hash)` with 0 arguments triggers `Malformed cat` / `Malformed hash`.
  - `Malformed gen` / `Malformed one`: Must have arity 0 `(gen)` / `(one)`. Passing arguments `(gen x)` triggers `Malformed gen`.
  - `Malformed exponentiation` / `Malformed base` / `Malformed exponent`: `(exp <base> <expt>)` must have exact arity 2, where the first argument has sort `base` (`(gen)` or `(exp ...)`) and the second argument has sort `expt` or `rndx`. Note: If you write `(exp x y)` without `(gen)`, `x` is not of sort `base`, triggering `Malformed base`!
  - `Malformed rec`: `(rec <expt>)` must have exact arity 1 where `<expt>` has sort `expt` or `rndx`.
- **Exact JSON AST Field to Fix**: `CPSATraceEvent.message_term`, `inputs`, `outputs`, `non_originating` — fix the operator array length, argument order, and ensure `exp` always has `["gen"]` or `["exp", ...]` as its first argument.
- **Before / After Fix Example**:
  - *Failing JSON (`Malformed base` and `Malformed pubk`)*:
    ```json
    ["enc", ["exp", "x", "y"], ["pubk", "server_id", "\"sig\""]]
    ```
  - *Repaired JSON*:
    ```json
    ["enc", ["exp", ["gen"], ["mul", "x", "y"]], ["pubk", "\"sig\"", "server_id"]]
    ```

## 2.4 `Keyword <s> unknown` / `Malformed term`
- **Emitting Tool & Source**: `cpsa4` (`CPSA.Algebra :: loadTerm`, `Algebra.hs:2575, 2578`) and `cpsa4roletran` (`CPSA.Roletran.Loader :: loadTerm`, `Roletran/Loader.hs:205, 207`)
- **Root Cause in CPSA Semantics**: The head symbol `<s>` of a list `(<s> ...)` in a term position is not in `loadDispatch`:
  1. Using a foreign operator like `aenc`, `senc`, `sign`, `mac`, `hmac`, `kdf`, `tuple`, `pair`.
  2. Using `bltk`, `exp`, `gen`, `mul`, `rec`, `one` in a `basic` algebra protocol evaluated by `cpsa4roletran` (`Roletran/Loader.hs:211` `loadDispatch` only knows `pubk`, `privk`, `invk`, `ltk`, `cat`, `enc`, `hash`!).
  3. Omitting `cat` or `enc` at the head of a list, e.g., writing `["client_nonce", "server_nonce"]` (`(client_nonce server_nonce)`), causing CPSA to treat the variable `client_nonce` as an unknown function keyword!
  4. `Malformed term` occurs when a list in a term position does not start with a symbol (e.g., `((cat a b) c)` where the head is a nested list or number) or is an empty list `()`.
- **Exact JSON AST Field to Fix**: `CPSATraceEvent.message_term` — prepend `"cat"`, `"enc"`, or `"hash"` to tuple lists, replace `bltk` with `ltk` in `basic` algebra, and replace foreign operators with canonical CPSA 4.4.9 operators.

## 2.5 `Sort <sort> not recognized` / `mkVar:  Variables of sort base are now deprecated <x>` / `Malformed vars declaration` / `Bad variable declaration` / `Bad variable syntax`
- **Emitting Tool & Source**: `cpsa4` (`CPSA.Algebra :: loadVarPair`, `loadVar`, `mkVar`, `Algebra.hs:2453–2490`) and `cpsa4roletran` (`CPSA.Roletran.Loader :: loadVarPair`, `loadVar`, `loadSort`, `Roletran/Loader.hs:128–150`)
- **Root Cause in CPSA Semantics**:
  1. `Sort <sort> not recognized`: A variable was declared with a non-existent sort (`nonce`, `key`, `cert`, `int`, `string`), OR a `locn`/`rndx`/`expt` sort was passed to `cpsa4roletran` (`Roletran/Loader.hs:141–150` only recognizes `text`, `data`, `name`, `skey`, `akey`, `mesg`, `chan`).
  2. `mkVar:  Variables of sort base are now deprecated <x>` (`Algebra.hs:2481`, because `variablesOfSortBase = False` at line 207): A variable was declared with sort `base` (`(vars (g_a base))`).
  3. `Malformed vars declaration` / `Bad variable declaration` / `Bad variable syntax`: An entry in `(vars ...)` is not a list of $\ge 2$ symbols `(v1 ... vn sort)`.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.variables` and `CPSAPreskeleton.variables`. Use only valid sorts (`name`, `text`, `data`, `tag`, `skey`, `akey`, `chan`, `locn`, `dev`, `mesg`, `rndx`, `expt`). To model a received Diffie-Hellman public group element without sort `base`, declare an exponent `(alpha expt)` and write the group element as `["exp", ["gen"], "alpha"]`.

## 2.6 ` Expts must first be received, rndxs first sent:   at event <i> in role <name>` / ` Var received non-carried in role <name>, then sent carried:  <v> at event <p>`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: loadTrace`, `badGroupMemberOccurrences`, `badOrigNotGen` (`Loader.hs:841–897`)
- **Root Cause in CPSA Semantics**: In `diffie-hellman` algebra, `loadTrace` validates all group variables (`rndx` and `expt`) across the role's trace:
  1. `Expts must first be received, rndxs first sent`: `checkGroupVar (Out _) v = isRndx v` (line 848). If the **first** occurrence of a group variable `v` in a role's trace is in an outbound `send`/`stor` event, `v` **must** have sort `rndx` (if it has sort `expt`, `cpsa4` fails!). Conversely, a peer's DH exponent first seen in an inbound `recv` event should have sort `expt`.
  2. `Var received non-carried in role <name>, then sent carried`: `recvButOrig v c` (`originates v c && not (generates v c)`, line 869). A group variable `v` first occurred **uncarried** in an inbound `recv` event (e.g., `(recv (exp (gen) v))`) and was later sent **carried** in an outbound `send` event (e.g., `(send v)`).
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.variables` and `CPSAProtocolRole.trace` — in each role, set `"sort": "rndx"` for the DH exponent(s) **first sent** by that role, set `"sort": "expt"` for the peer DH exponent(s) **first received** by that role, and never transmit a received peer exponent as a bare carried value!
- **Before / After Fix Example**:
  - *Failing Scheme (`client` declares sent `x` as `expt`)*:
    ```scheme
    (defrole client
      (vars (x expt) (y expt))
      (trace (send (exp (gen) x)) (recv (exp (gen) y))))
    ```
  - *Repaired Scheme (`client` declares sent `x` as `rndx` and received `y` as `expt`)*:
    ```scheme
    (defrole client
      (vars (x rndx) (y expt))
      (trace (send (exp (gen) x)) (recv (exp (gen) y))))
    ```

## 2.7 `Identifier <name> is an expt--must be a rndx` / `Disallowed bare exponent`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Algebra :: loadLookupStrict`, `loadOne`, `loadRec`, `loadMul` (`Algebra.hs:2538, 2746, 2754, 2767`)
- **Root Cause in CPSA Semantics**: In `Algebra.hs`, `loadTerm sig vars strict` is called with `strict = True` when loading:
  - Outbound `(send ...)` and `(stor ...)` messages (`Loader.hs:904, 916, 929`),
  - `(deflistener <term>)` (`Loader.hs:1172`), and
  - Base/atom declarations `(non-orig ...)`, `(pen-non-orig ...)`, `(uniq-orig ...)`, `(uniq-gen ...)`, and the first element of `(absent ...)` (`Loader.hs:1002, 1028, 1053`).
  Inside `loadTerm` with `strict = True`, `loadExp`, `loadHash`, and the key slot of `loadOper (Enc)` switch `strict` to `False`. Therefore:
  1. If an `expt` variable `<name>` appears in a **carried** position of a `send`/`stor`/`deflistener` or in `uniq-orig`/`uniq-gen`/`non-orig` (outside `exp`, `hash`, or `enc` key slot), `loadLookupStrict` fails with `Identifier <name> is an expt--must be a rndx`!
  2. If `(one)`, `(rec ...)`, or `(mul ...)` appears in a **carried** position outside `(exp ...)`, `loadOne`/`loadRec`/`loadMul` fails with `Disallowed bare exponent`!
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.variables`, `CPSAProtocolRole.trace`, `CPSAPreskeleton.listeners`, `CPSAPreskeleton.unique_generated`. Wrap DH exponents in `["exp", ["gen"], ...]` when sending or listening (unless revealing a compromised raw `rndx` scalar), and never place `expt` variables in `uniq-gen` or `deflistener` (use `rndx` or `["exp", ["gen"], ...]` instead).

## 2.8 `Expecting terms in algebra <nom>` / `Bad algebra: <nom>` / `Algebra <name> not one of ...`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: loadProt` (`Loader.hs:87`) and `CPSA.Main :: select`, `interp` (`Main.hs:106, 277`)
- **Root Cause in CPSA Semantics**: Mismatch between the algebra `<nom>` active in the solver (set by `(herald "..." (algebra <nom>))` or CLI `-a`, defaulting to `"basic"`) and `<alg>` in `(defprotocol <name> <alg> ...)`. Most commonly occurs when `defprotocol` specifies `diffie-hellman` but `(herald ...)` omits `(algebra diffie-hellman)`.
- **Exact JSON AST Field to Fix**: `CPSAProtocolSpecification.message_algebra` — set to `"diffie-hellman"`, which causes `to_cpsa_json_payload()` to emit `(herald "..." (algebra diffie-hellman))` automatically.

---

## Section 3: Role & Preskeleton Well-Formedness Diagnostics (`CPSA.Loader` & `CPSA.Strand`)

## 3.1 `Role not well formed: uniq-orig <t> doesn't originate` / `uniq-gen <t> doesn't generate` / `Skeleton not well formed: uniq-orig <t> not carried` / `uniq-gen <t> does not occur` / `an inherited unique doesn't originate in its strand` / `an inherited unique gen doesn't generate in its strand`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: roleWellFormed` (`Loader.hs:318, 321`) and `CPSA.Strand :: verbosePreskelWellFormed` (`Strand.hs:938, 940, 948, 951`)
- **Root Cause in CPSA Semantics**:
  1. `uniq-orig <t> doesn't originate` / `uniq-orig <t> not carried`: `<t>` was declared in `uniq-orig`, but `<t>` is a Diffie-Hellman `rndx` exponent in `(exp (gen) <t>)` (uncarried!), or `<t>` only appears inside `(hash ...)` or as the key of `(enc ... <t>)` (uncarried!), or `<t>`'s first trace appearance is in a `recv` event.
  2. `uniq-gen <t> doesn't generate` / `uniq-gen <t> does not occur`: `<t>` was declared in `uniq-gen`, but its first occurrence in the role trace is in an inbound `recv` event rather than an outbound `send` event, or it does not occur in the skeleton.
  3. `an inherited unique [gen] doesn't originate [generate] in its strand`: A role declared `(uniq-orig u)` or `(uniq-gen u)` at role trace index `pos`, and a skeleton instantiated that role with height `> pos`, mapping `u` to a skeleton term `t'`, but `t'` was already received/carried earlier on that strand (e.g., due to variable aliasing in `variable_bindings`), destroying origination at `pos`!
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.unique_originating` / `CPSAProtocolRole.unique_generated`, `CPSAPreskeleton.unique_originating` / `CPSAPreskeleton.unique_generated`, and `CPSAStrandInstance.variable_bindings`. Move `rndx` variables and uncarried fresh keys to `unique_generated` (`uniq-gen`); remove peer-received variables from `unique_originating`.

## 3.2 `Role not well formed: non-orig <t> carried` / `Skeleton not well formed: non-orig <t> carried`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: roleWellFormed` (`Loader.hs:304`) and `CPSA.Strand :: verbosePreskelWellFormed` (`Strand.hs:945`)
- **Root Cause in CPSA Semantics**: `any (carriedBy t) terms == True`. A term `<t>` declared in `non-orig` (`non_originating`) is transmitted or received in a **carried** position of a message in the role or skeleton (e.g., a session key `k` sent inside `(enc k (pubk b))` or in plaintext `(cat a k)`). By definition, `non-orig` means carried **nowhere** in the bundle.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.non_originating` and `CPSAPreskeleton.non_originating`. Remove the carried key from `non_originating` and place it in `pen_non_originating` (`pen-non-orig`) or, if freshly generated by the sender, in `unique_originating` (`uniq-orig`).

## 3.3 `Role not well formed: a variable in [non-orig/pen-non-orig] is not in trace` / `Skeleton not well formed: a variable in [non-orig/pen-non-orig] is not in some trace`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: roleWellFormed` (`Loader.hs:278, 280`) and `CPSA.Strand :: verbosePreskelWellFormed` (`Strand.hs:925, 927`)
- **Root Cause in CPSA Semantics**: `varSubset (knon k) terms == False`. A variable occurring in a `(non-orig ...)` or `(pen-non-orig ...)` assumption (such as `server_identity` in `(non-orig (privk server_identity))`) does **not** appear in any message term in `kterms k` (the instantiated strands of that skeleton). Usually happens when:
  1. `server_identity` was not bound in `defstrandmax`'s `variable_bindings`, OR
  2. `server_identity` was bound to a role variable that was dropped by `loadRole` because it never appeared in that role's `trace`!
- **Exact JSON AST Field to Fix**: `CPSAPreskeleton.strands[i].variable_bindings`, `CPSAPreskeleton.non_originating`, and `CPSAProtocolRole.trace`. Ensure every variable referenced in `non_originating` / `pen_non_originating` is bound in `variable_bindings` to a role variable that actually appears in that role's `trace`.

## 3.4 `Role not well formed: invalid position <len>` / `<t> appears after position <len>` / `no used position for non-originating atom <t>` / `Expecting a non-negative non-origination position`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: roleWellFormed`, `loadPosBaseTerm` (`Loader.hs:308–316, 1020`)
- **Root Cause in CPSA Semantics**: In a role-level positional `(non-orig (<len> <atom>))` or `(pen-non-orig (<len> <atom>))` declaration:
  - `<len> < 0` (`Expecting a non-negative non-origination position`),
  - `<len> >= length (rtrace role)` (`invalid position <len>`), or
  - `<atom>` is used in the role trace at a step index `> <len>` (`<t> appears after position <len>`).
- **Exact JSON AST Field to Fix**: Omit integer position prefixes in `(non-orig ...)` or move `non-orig` to `CPSAPreskeleton.non_originating`.

## 3.5 `Role not well formed: variable <v> not acquired`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: roleWellFormed` (`Loader.hs:324`)
- **Root Cause in CPSA Semantics**: `isAcquiredVar v` (`v` has sort `mesg`) and `acquiredPos v (rtrace role) == Nothing`. A variable `<v>` declared with `"sort": "mesg"` appeared in a `send` event (or in an uncarried key/hash position of a `recv` event) before first appearing in a **carried** position of an inbound `recv` event.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.variables` — change `<v>`'s `sort` from `"mesg"` to a specific basic sort (`"data"`, `"text"`, `"skey"`, `"name"`), or ensure the `mesg` variable is first acquired in a carried position of an earlier `recv` event.

## 3.6 `Role not well formed: role trace is a prefix of a listener`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: roleWellFormed`, `notListenerPrefix` (`Loader.hs:290, 607–609`)
- **Root Cause in CPSA Semantics**: `notListenerPrefix (In t : Out t' : _) | t == t' = False`. A role's trace begins with `(recv m)` at index 0 followed immediately by `(send m)` at index 1 for the exact same unmodified term `m` (and channel), making a 2-event prefix of the role identical to a listener strand `(deflistener m)`.
- **Exact JSON AST Field to Fix**: `CPSAProtocolRole.trace` — add a distinct tag or cryptographic wrapper to the transmitted or received message, e.g., `["cat", "\"ack\"", "m"]` or `["enc", "m", "k"]`.

## 3.7 `Role not well formed: <ch> declared [conf/auth] but not used in role <r>` / `Bad channel in role` / `Skeleton not well formed: some variable in [confidential/authenticated] channel <c> not in some strand`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: loadRole`, `roleWellFormed`, `loadRest` (`Loader.hs:185, 338–343, 1210`) and `CPSA.Strand :: verbosePreskelWellFormed` (`Strand.hs:963, 967`)
- **Root Cause in CPSA Semantics**: A channel declared in `(conf <ch>)` or `(auth <ch>)` is not of sort `chan`, or is never used in any `(send <ch> ...)` / `(recv <ch> ...)` event of that role or skeleton.
- **Exact JSON AST Field to Fix**: Ensure every channel listed in `conf` or `auth` is declared with `"sort": "chan"` and used in at least one trace event of the role/skeleton.

## 3.8 `Expecting an atom` / `Expecting a pair of terms` / `Expecting an exponent` / `Expecting an exponent variable` / `Skeleton not well formed: absent <x> does not occur`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: loadBaseTerm`, `loadPosBaseTerm`, `loadAbsent`, `loadExprTerm`, `loadVarExprTerm` (`Loader.hs:1005, 1031, 1040, 1048, 1056`) and `CPSA.Strand :: verbosePreskelWellFormed` (`Strand.hs:955, 957`)
- **Root Cause in CPSA Semantics**:
  1. `Expecting an atom`: A term in `non-orig`, `pen-non-orig`, `uniq-orig`, or `uniq-gen` failed `isAtom t` (`Algebra.hs:712`). In `Algebra.hs`, `isAtom` is `True` **only** for variables of sort `name`, `text`, `data`, `skey`, `akey`, `chan`, `locn`, `rndx` (`isBasisVar`), and key atoms `(pubk ...)`, `(privk ...)`, `(invk ...)`, `(ltk ...)`, `(bltk ...)`. It is `False` for `mesg`, `base` (`(exp ...)`), `expt` (`isExprVar`), tags `"..."`, and compound terms `(cat ...)`, `(enc ...)`, `(hash ...)`!
  2. `Expecting a pair of terms` / `Expecting an exponent variable` / `Expecting an exponent`: In `(absent (x y))`, `x` must be an exponent variable (`rndx` or `expt`), `y` must be an exponent term, and both must occur in the skeleton (`absent <x> does not occur`).
- **Exact JSON AST Field to Fix**: `non_originating`, `pen_non_originating`, `unique_originating`, `unique_generated` — remove any `(cat ...)`, `(enc ...)`, `(hash ...)`, `(exp ...)`, `mesg`, or `expt` term and replace with atomic `name`/`text`/`data`/`skey`/`akey`/`rndx` variables or `pubk`/`privk`/`ltk` key terms.

## 3.9 `Role not well formed: role trace has multiple loads or stors on same locn` / `checkForDivergenceInStoreSegments: Roles <r1> and <r2> agree up to step <i> but diverge in a store segment` / `Skeleton not well formed: gen-st <t> not carried` / `Expecting a location`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: loadProt`, `roleWellFormed`, `locnsUnique`, `loadLocn` (`Loader.hs:122, 299, 989`) and `CPSA.Strand :: verbosePreskelWellFormed` (`Strand.hs:960`)
- **Root Cause in CPSA Semantics**:
  1. `multiple loads or stors on same locn`: Within a single contiguous state segment of a role trace, the same `locn` variable was loaded twice or stored twice.
  2. `checkForDivergenceInStoreSegments`: Two roles have identical trace prefixes up to a state segment and diverge inside the store segment without being distinguished prior to the second event in the store segment.
  3. `gen-st <t> not carried`: A state term in `(gen-st <t>)` is not carried in any strand of the skeleton.
  4. `Expecting a location`: First argument of `(load <locn> <term>)` or `(stor <locn> <term>)` is not declared with sort `locn`.

## 3.10 `Identifier <name> unknown` / `Domain does not match range` / `Malformed maplet` / `Bad maplet`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Algebra :: loadLookup` (`Algebra.hs:2528`), `CPSA.Loader :: loadMaplet` (`Loader.hs:1165, 1166`), `CPSA.Graph.Loader :: loadMaplet` (`Graph/Loader.hs:405`)
- **Root Cause in CPSA Semantics**:
  - `Identifier <x> unknown`: Either `<x>` is used in a trace/skeleton without being declared in `(vars ...)`, **OR** `<x>` is the left-hand side (domain) of a `defstrandmax` maplet `(<x> <val>)` where `<x>` was declared in the role's `(vars ...)` but **never used in the role's `(trace ...)`** (`Loader.hs:189` drops unused variables from `rvars role` via `let vs = L.filter f vars`, so `<x>` is no longer in `rvars r` when `loadMaplet` looks it up!).
  - `Domain does not match range`: In a `defstrand` / `defstrandmax` maplet `(<role_var> <skel_term>)`, `match t t' env` returned `[]` because the sort of `<skel_term>` in the skeleton's `(vars ...)` does not match the sort of `<role_var>` in the role's `(vars ...)` (e.g., mapping a role variable of sort `rndx` to a skeleton variable of sort `expt`, or mapping `text` to `data`), or `<role_var>` was mapped to two conflicting terms.
  - `Malformed maplet` / `Bad maplet`: A maplet in `defstrand` / `defstrandmax` is not a 2-element list `(domain range)`.
- **Exact JSON AST Field to Fix**: `CPSAPreskeleton.variables`, `CPSAPreskeleton.strands[i].variable_bindings`, and `CPSAProtocolRole.variables`. Ensure every `role_parameter` in `variable_bindings` appears in that role's `trace` and has the exact same sort as `skeleton_variable` in `CPSAPreskeleton.variables`.

## 3.11 `Role <r> not found in <p>` / `Protocol <p> unknown` / `No strands` / `Duplicate role <r> in protocol <p>` / `Duplicate variable declaration for <v>` / `<key> declaration too late in enclosing form` / `defrole <name> misplaced`
- **Emitting Tool & Source**: `cpsa4` (`CPSA.Loader`, `Loader.hs:131, 762, 820, 1064, 1184`, `CPSA.LoadFormulas :: lookupRole`, `LoadFormulas.hs:122`) and `cpsa4roletran` (`CPSA.Roletran.Loader`, `Roletran/Loader.hs:55, 134`)
- **Root Cause in CPSA Semantics**:
  - `Role <r> not found in <p>`: `CPSAStrandInstance.role_name` in a skeleton does not match any `CPSAProtocolRole.role_name` in `CPSAProtocolSpecification.roles`.
  - `Protocol <p> unknown`: `CPSAPreskeleton.protocol_name` does not match `CPSAProtocolSpecification.protocol_name`.
  - `No strands`: `CPSAPreskeleton.strands` (and `listeners`) is empty `[]`.
  - `Duplicate role`: Two roles in `roles` have the same `role_name`.
  - `Duplicate variable declaration for <v>`: Two entries in `variables` have the same `name`.
  - `<key> declaration too late in enclosing form` / `defrole <name> misplaced`: In `defskeleton`, all `defstrand` / `defstrandmax` / `deflistener` forms **must precede** `non-orig`, `uniq-orig`, `precedes`, etc. (`badKey ["defstrand", "deflistener"] xs`, `Loader.hs:1103`). In `defprotocol`, all `defrole` forms must precede `defrule` forms, which must precede association-list comments (`Loader.hs:762, 765`).
- **Exact JSON AST Field to Fix**: Align `protocol_name`, `role_name`, and deduplicate `variables` / `roles`. (`CPSAProtocolSpecification.to_cpsa_json_payload()` automatically emits strands before origination assumptions).

## 3.12 `Bad height` / `Negative strand in node` / `Negative position in node` / `Bad strand in node` / `Bad position in node` / `Malformed node` / `Malformed pair` / `Skeleton not well formed: ordered pairs not well formed` / `Skeleton not well formed: cycle found in ordered pairs`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: loadInst`, `loadPair`, `loadNode` (`Loader.hs:1138, 1239–1255`) and `CPSA.Strand :: verbosePreskelWellFormed` (`Strand.hs:936, 937`)
- **Root Cause in CPSA Semantics**:
  - `Bad height`: In `(defstrand role h ...)`, `h < 1` or `h > length (rtrace r)`. (`CPSAStrandInstance.to_cpsa_json()` always emits `defstrandmax` to avoid height errors).
  - `Negative/Bad strand/position in node` / `Malformed node` / `Malformed pair`: Invalid node coordinates `((s0 i0) (s1 i1))` in `precedes` or `leads-to`.
  - `ordered pairs not well formed` (`Strand.hs:986`): In `precedes`, for every pair `((s0 i0) (s1 i1))`, event `(s0, i0)` **must** be an `Out` (`send`/`stor`) event and event `(s1, i1)` **must** be an `In` (`recv`/`load`) event!
  - `cycle found in ordered pairs` (`Strand.hs:1043`): `precedes` edges plus strand succession edges contain a directed cycle.
- **Exact JSON AST Field to Fix**: `CPSAPreskeleton.precedes` — remove invalid or cyclic `precedes` pairs (CPSA infers causal precedence automatically from message transmissions).

---

## Section 4: Goal, Rule, Rely/Guarantee, and Characteristic Skeleton Diagnostics (`CPSA.LoadFormulas`, `CPSA.Characteristic`, `CPSA.Loader`)

## 4.1 `Bad goal sentence:  No forall` / `Bad goal implication` / `<v> not used`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.LoadFormulas :: loadSentence`, `loadImplication`, `loadRoleSpecific`, `loadUsedVars` (`LoadFormulas.hs:139, 157, 231, 245`)
- **Root Cause in CPSA Semantics**:
  - `Bad goal sentence:  No forall`: Top-level formula in `defgoal`, `defrule`, or `goals` is not `(forall ((...)) (implies ...))`.
  - `Bad goal implication`: Body of `forall` is not `(implies <antecedent> <conclusion>)`.
  - `<v> not used`: A universally or existentially quantified variable `<v>` in `forall` or `exists` never occurs in any role-specific predicate in the conjunction (or only occurs in non-role-binding predicates).

## 4.2 `Unbound variable in [parameter predicate|prec|non|pnon|uniq|uniq-at|ugen|ugen-at|gen-st|conf|auth|fact|comm-pr|leads-to|state-node|trans|same-locn|equals|component]`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.LoadFormulas :: roleSpecific` (`LoadFormulas.hs:530–605`)
- **Root Cause in CPSA Semantics**: In a `defgoal` (or role-specific conclusion), every universally quantified strand variable `z` must be bound by a role length predicate `(p "role" z h)` (or `(strand "role" z h ...)` / `(listener z t)`), and every message/channel variable `v` must be bound by a parameter predicate `(p "role" "param" z v)` (or `(fact ... v)`) before appearing in `non`, `pnon`, `uniq`, `uniq-at`, `prec`, `=`, etc.

## 4.3 `Bad length` / `Bad parameter -- not a variable <v>` / `parameter <x> not in role <r>` / `Bad protocol specific formula for role <r>` / `Bad formula for predicate <pred>` / `Sort mismatch in equality` / `Type mismatch in [equals/component]` / `Strand variable in component formula` / `Malformed pair -- nodes in same strand`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.LoadFormulas :: loadStrand`, `loadVMaps`, `loadPrimary`, `roleSpecific` (`LoadFormulas.hs:292–450, 591–602`)
- **Root Cause in CPSA Semantics**:
  - `Bad length`: Height `h` in `(p "role" z h)` or `(strand "role" z h ...)` is `<= 0` or `> length (rtrace r)`.
  - `parameter <x> not in role <r>`: `<x>` in `(p "role" "<x>" z val)` does not occur in `<role>`'s trace.
  - `Sort mismatch in equality` / `Type mismatch in equals`: Comparing a `strd` variable against an algebra term in `(= x y)`.
  - `Malformed pair -- nodes in same strand`: `(prec z i z j)` has the same strand variable `z` for both nodes (`LoadFormulas.hs:418`).

## 4.4 `Equals not allowed in antecedent` / `Index is variable, not integer` / `Strand occurs in more than one role length atom` / `Role in parameter pred differs from role position pred` / `Atom not unique at node` / `Atom not uniq gen at node`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Characteristic` (`Characteristic.hs:44, 88, 95, 129, 231, 240`)
- **Root Cause in CPSA Semantics**: When `defgoal` constructs its characteristic preskeleton from the antecedent of `(forall (...) (implies <antec> <concl>))`:
  - `Equals not allowed in antecedent`: `(= x y)` appeared in `<antec>` (substitute `x` for `y` directly instead).
  - `Index is variable, not integer`: Height `h` in `(p "role" z h)` in `<antec>` is an `indx` variable instead of an integer literal.
  - `Strand occurs in more than one role length atom`: The same strand variable `z` was given two different roles `(p "r1" z h1)` and `(p "r2" z h2)`.
  - `Atom not unique at node` / `Atom not uniq gen at node`: `(uniq-at t z i)` or `(ugen-at t z i)` was asserted in `<antec>`, but `t` does not originate/generate at node `(z, i)` of the characteristic skeleton.

## 4.5 `Rely precedes first event in role <r>` / `Rely must follow recv or load in role <r>` / `Guarantee follows last event in role <r>` / `Guarantee must precede send or stor in role <r>` / `cheq must precede some event in role <r>` / `<pos> var <v> not bound by height <bound>` / `<pos> variables not bound until height <ht>`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Loader :: loadTrace`, `varsUsedBy` (`Loader.hs:685, 688, 937–959`)
- **Root Cause in CPSA Semantics**: In a role trace using rely/guarantee/cheq annotations:
  - `(rely <form>)` must immediately follow an inbound `recv` or `load` event.
  - `(guar <form>)` must immediately precede an outbound `send` or `stor` event.
  - Every variable used in `<form>` or `(cheq src tgt)` must be bound in the role's trace at or before that event's height.

---

## Section 5: Lexer, Parser, Macro, JSON, and Graph Pipeline Diagnostics (`CPSA.Lib.SExpr`, `CPSA.Lib.Expand`, `CPSA.JSON.Main`, `CPSA.Graph.Loader`, `CPSA.Shapes.Shapes`)

## 5.1 `Bad char in atom` / `Bad char in string` / `Bad escaped char in string` / `End of input in string` / `Bad char after number` / `Close of unopened list` / `Unexpected end of input in list` / `Quote in symbol` / `Sign not followed by a digit`
- **Emitting Tool & Source**: `cpsa4` S-expression reader (`CPSA.Lib.SExpr`, `Lib/SExpr.hs:175, 197, 273, 282, 290, 299, 305, 320`) and `cpsa4json` JSON reader (`CPSA.JSON.Main`, `JSON/Main.hs:162, 183, 239, 248, 256, 278, 314`)
- **Root Cause in CPSA Semantics**:
  - `Bad char in atom`: An unquoted symbol contains periods (`.`), brackets, or characters outside `[a-zA-Z0-9+\-*/<=>!?$:%_&~^]`, or in `cpsa4json` an unquoted token is neither `[` / `]` / integer / `"..."`.
  - `Bad char in string` / `End of input in string`: A string literal or comment contains a literal newline or unescaped quote.
  - `Quote in symbol` (`JSON/Main.hs:278`): In `cpsa4json`, a string starting with `\"` (representing a CPSA quoted tag `"\"tag\""`) did not end with `\"`.
  - `Bad char after number`: A token starts with digits (or `+/-` followed by digits) and is immediately followed by symbol characters (e.g., `123abc` or `5G_AKA`). **CPSA symbols may never begin with a digit or a sign followed by a digit!**
- **Exact JSON AST Field to Fix**: All identifier fields (`protocol_name`, `role_name`, `variables[i].name`) and string tags/comments. Never start a symbol name with a digit (e.g., use `fiveg_aka` instead of `5g_aka`), keep all strings single-line, and format string literal tags as `"\"tag_value\""` (automatically enforced by `sanitize_cpsa_symbol()` and `normalize_cpsa_term()`).

## 5.2 `Malformed macro` / `Expecting a symbol` / `Expansion limit exceeded` / `Expected argument count for macro <m>` / `Include depth exceeded with file <f>`
- **Emitting Tool & Source**: `cpsa4` — `CPSA.Lib.Expand` (`Lib/Expand.hs:65, 130, 134, 154, 173`)
- **Root Cause in CPSA Semantics**: A `(defmacro (name arg1 ...) body)` form has non-symbol parameter names, is called with the wrong number of arguments, or expands recursively beyond the macro expansion depth limit.

## 5.3 `Empty input` / `Cycle found` / `parent unknown`
- **Emitting Tool & Source**: `cpsa4graph` (`CPSA.Graph.Loader`, `Graph/Loader.hs:154, 285`) and `cpsa4shapes` (`CPSA.Shapes.Shapes`, `Shapes/Shapes.hs:45`)
- **Root Cause in CPSA Semantics**:
  - `Empty input`: `cpsa4` produced no output skeletons (either because `CPSAProtocolSpecification.skeletons` was empty `[]`, or because `cpsa4` aborted with a loader error before emitting any skeletons).
  - `Cycle found`: The skeleton graph contains a causal cycle.
  - `parent unknown`: Broken `(parent <n>)` pointer in corrupted `cpsa4` output passed to `cpsa4shapes`.
- **Exact JSON AST Field to Fix**: `CPSAProtocolSpecification.skeletons` — ensure the 3-POV skeletons are populated (via `ensure_three_point_of_view_skeletons()`) and that `cpsa4` exits with code 0.
````

---

### `refrences/cpsa_kb/02_manuals/01_CPSA4_User_Manual.md`

*sha256:`dfc86b9da5c8` · 3927 lines · 221.8 KB (~56,314 tokens) · lang:`markdown` · 22 control chars sanitized*

````markdown
# CPSA 4 User Manual (Version 4.4.9)

**The Cryptographic Protocol Shapes Analyzer: A Manual for CPSA 4**
*Authors: Moses D. Liskov, John D. Ramsdell, Joshua D. Guttman, Paul D. Rowe (The MITRE Corporation)*

---

## Table of Contents

- **Part I: Basic Use of CPSA**
  - [Chapter 1: Introduction](#chapter-1-introduction) (`1.1 Recommended reading`, `1.2 Tool components`)
  - [Chapter 2: Setup and Installation](#chapter-2-setup-and-installation) (`2.1 Basic Installation`, `2.2 Finding Documentation`, `2.3 Running cpsa`)
  - [Chapter 3: Basic Protocol Modeling and Analysis with CPSA](#chapter-3-basic-protocol-modeling-and-analysis-with-cpsa) (`3.1 Basic CPSA modeling`, `3.2 CPSA input`, `3.3 CPSA output`, `3.4 Interpreting shapes`, `3.5 Blanchet's simple example protocol`)
  - [Chapter 4: Algebra Features of CPSA](#chapter-4-algebra-features-of-cpsa) (`4.1 Generic messages and long-term keys`, `4.2 Modeling Diffie-Hellman`, `4.3 Other Algebra Features`, `4.4 The Lang Field: Declaring new operators`)
- **Part II: Understanding and Guiding CPSA**
  - [Chapter 5: The CPSA Search Algorithm](#chapter-5-the-cpsa-search-algorithm) (`5.1 Solving tests`, `5.2 Flawed Kerberos, revisited`)
  - [Chapter 6: Constraining CPSA's Search](#chapter-6-constraining-cpsas-search) (`6.1 Bundles: A Strand-Based Execution Model`, `6.2 Secrecy assumptions`, `6.3 Diffie-Hellman declarations`, `6.4 Declaring skeletons`, `6.5 A Caution about typos`)
- **Part III: Advanced Features of CPSA**
  - [Chapter 7: Logical Security Goals and Rules](#chapter-7-logical-security-goals-and-rules) (`7.1 Overview`, `7.2 Semantics`, `7.3 Examples`, `7.4 The Rest of the Story`, `7.5 Syntactic Abbreviations`, `7.6 Shape Analysis Sentences`, `7.7 Rules`, `7.8 Lemmas`)
  - [Chapter 8: Channels and State](#chapter-8-channels-and-state) (`8.1 Channels`, `8.2 State`)
- **Part IV: Reference Material**
  - [Chapter 9: Troubleshooting](#chapter-9-troubleshooting) (`9.1 Non-termination`, `9.2 Error messages`)
  - [Chapter 10: CPSA Program Reference](#chapter-10-cpsa-program-reference) (`10.1 CPSA pre-processing`, `10.2 CPSA input syntax`, `10.3 Algebra reference`, `10.4 Declaration syntax`, `10.5 Command-line options`)
  - [Chapter 11: CPSA Tools](#chapter-11-cpsa-tools) (`11.1 cpsa4init` – `11.10 cpsa4diff`)
  - [Bibliography](#bibliography)

---

## Chapter 1: Introduction

cpsa, the Cryptographic Protocol Shapes Analyzer, is a software tool designed to assist in
the design and analysis of cryptographic protocols. A cryptographic protocol is a specific
pattern of interaction between principals. TLS and IKE are some examples of well-known
cryptographic protocols.
    The tool takes as input a protocol definition and a partial description of an execution,
each built within a particular formal model by the user. It attempts to produce descriptions
of all possible executions of the protocol that complete the partial description, consistent
with the presence of a powerful network adversary capable of diverting, altering, replaying,
or dropping network messages. Such an adversary may be able to manipulate honest participants
 into an unexpected execution, breaking a secrecy or authentication property that
the protocol was intended to achieve.
    Naturally, there are infinitely many possible executions of a useful protocol, since different
 participants can run it with varying parameters, and the participants can run it
repeatedly. However, for many naturally occurring protocols, there are only finitely many
of these runs that are essentially different. Indeed, there are frequently very few, often just
one or two, even in cases where the protocol is flawed. We call these minimal, essentially
different executions the shapes of the protocol. Authentication and secrecy properties are
easy to “read off” from the shapes, as are attacks and anomalies.
    The analysis performed by cpsa is done within a pure Dolev-Yao model [3]; as such, the
analysis reveals only structural flaws in the protocols it analyzes. It cannot detect flaws in
underlying cryptographic algorithms or in actual implementations of protocol participants.
    The purpose of this document is to provide the background required to make effective
use of the cpsa software distribution.

### 1.1 Recommended reading

If you are new to cpsa, it is recommended that you first read Part I, which is introductory
in nature and presented as a tutorial. Chapter 2 discusses how to download, install, and
run the tool. Chapter 3 begins the tutorial describing how to use the tool, and Chapter 4
describes some of the more important additional features.
    Readers, especially those without direct access to an experienced user of the tool, are
encouraged to attempt the “explorations” present from Chapter 3 onwards. The purpose of
the explorations is to give the reader experience in the use of the tool and a chance to test
his or her understanding of its features. After reading through the first part, you should be
ready to attempt to use the tool to analyze a protocol that interests you, whether it be an
existing protocol or one you need to design.
    When you are ready for a deeper base of knowledge, read Part II. The chapters in
Part II will be helpful as you cross from trying to understand how to use the tool to trying
to impact your work on protocol design through use of the tool. Chapter 5 will be of
general use as you try to understand the analyses cpsa conducts, and Chapter 6 will help
you narrow the tool’s focus to what interests you.
    Part III deals with special-purpose features of the tool. Chapter 8 deals with stateful
protocols and Chapter 7 deals with logic-based protocol goals. You should read these
chapters if those features seem important to you.
    Part IV is reference material. Chapter 9 contains reference material about dealing with
errors of various sorts that arise during the use of cpsa, while Chapter 10 documents the
complete syntax of the tool.

### 1.2 Tool components

The distribution includes a number of separate executable command-line tools. Of these,
three are key components of the core expected workflow: cpsa4, cpsa4graph, and cpsa4shape.
The other tools are auxiliary utilities most general users will not need to use, although
cpsa4diff is of some use to a general user when updating the tool.
     The cpsa4 program takes as input one or more analysis problems (at least, a protocol
and a partial description of an execution), and analyzes them one at a time. It outputs the
full, step-by-step analysis for each problem, ultimately describing all possible full executions
that complete the partial execution.
     The cpsa4shape program takes an analysis and reduces it to an analysis that skips
directly from analysis input to the set of shapes associated with that input.
     The cpsa4graph program takes an analysis (from either cpsa4 or cpsa4shape) and
formats it into an xhtml file and includes svg(scalable vector graphics) diagrams of each
partial execution as well as the overall branching pattern of the analysis.
     The expected work flow follows. An analysis problem is entered using an ordinary
text editor, preferably one with support for Lisp syntax. The cpsa4 program uses an S-expression
-based syntax for both input and output. S-expression is an abbreviation for a
Symbolic Expression (as in the Lisp programming language).
    The body of the input consists of two forms: defprotocol statements that describe a
protocol, and defskeleton statements that describe a partial execution of a protocol. The
exact details of both forms depend on the message algebra specified by the protocol.
    Assuming there are no errors in the input, the analyzer will produce output as a text
document. The text document contains each step used to derive a shape from a problem
statement. It is common to filter the output using the cpsa4shapes program, and look
only at the computed shapes associated with each problem statement.
    The cpsa4graph program is applied to the output to produce a more readable, hyperlinked
 xhtml document that can be displayed in a standards-compliant web browser. See
Chapter 11 for more information on the programs that come with a cpsa distribution.
---

> **Part I: Basic use of CPSA**

## Chapter 2: Setup and Installation

### 2.1 Basic Installation

The use of cpsa requires Haskell, the programming language in which cpsa is coded. Our
recommendation is to use the Haskell Platform, which is available for Windows, Mac, and
Linux. The “Core” platform is sufficient, but the “Full” platform is also fine. On Linux,
install the haskell-platform package. Otherwise, follow the download and installation
instructions at:

                            http://www.haskell.org/platform/

    To install cpsa, run in a terminal or command prompt:
$ cabal update (to get the latest package list; this may take a while.)
$ cabal install cpsa
    Note that if you are behind a proxy, you may have to set the http proxy for your shell
if you haven’t already. For example, on a mac:
$ export http_proxy=http://proxy.myorg:port
On Windows:
$ set HTTP_PROXY=http://proxy.myorg:port
    Cabal will install cpsa in a directory specified in its config file (usually in /.cabal/config,
unless you’ve installed Haskell in a different directory). Instructions for changing your path
are included in the config file. The final step in the cabal install process should print the
location that cpsa has been installed in.

#### 2.1.1 Getting the Source

If you have trouble with cabal, or if you’d like extra features such as the cpsa test suite
of example protocols, you can download the current source distribution directly at:

                               http://github.com/mitre/cpsa

    There is a directory named cpsa4 at the top-level of the repository. It contains a copy
of the cpsa sources downloaded and compiled using cabal. On all platforms, to install
from this source, change into the cpsa4 directory and type:

$ cabal update
$ cabal install parallel
$ cabal configure
$ cabal build
$ cabal install

    Alternatively, there are other install options described in README.txt in the cpsa4
directory.

### 2.2 Finding Documentation

cpsa comes with documentation, but it can be difficult to locate by hand when the tool
has been installed through cabal. Run
    $ cpsa4 -h
to see the program’s help message, including the documentation directory, where this manual
 should be found.

### 2.3 Running cpsa

To analyze a protocol you have put in prob.scm type:

$ cpsa4 -o prob.txt prob.scm
$ cpsa4shapes -o prob_shapes.txt prob.txt
$ cpsa4graph -o prob_shapes.xhtml prob_shapes.txt

    See Section 10.5 for command-line options.
    The cpsa4shapes command is optional, but recommended; it cuts down cpsa’s output
to only show final results. Unless you’re doing detailed debugging, using it will make the
output much easier to read.
    To analyze a protocol without using the cpsa4shapes command, type:

$ cpsa4 -o prob.txt prob.scm
$ cpsa4graph -o prob.xhtml prob.txt

   The .xhtml results can be opened in a web browser.

#### 2.3.1 cpsa Projects
A cpsa project is a directory containing some cpsa input files and items that orchestrate
the use of the various cpsa tools. To create a project, in a fresh directory, run cpsa4init.

$ mkdir project
$ cd project
$ cpsa4init
Created Makefile
Created cpsa.mk
Created Make.hs
Created cpsa4prolog.pl

   The cpsa4init will not overwrite a file if it is already present in the current directory.
The distribution provides two ways to relieve users of the tedium of issuing individual
commands.

#### 2.3.2 Using the cpsa Makefile

The easiest way to orchestrate cpsa programs is to use GNU make. A cpsa project
contains the files Makefile and cpsa4.mk. To analyze the problems in your project, type
make. Edit the file Makefile to adjust program flags to suit your needs. For example, you
many want to enable the use of multiple processors during protocol analysis as described
in Section 2.3.5.
    The cpsa program is Emacs friendly. If you run the above makefile via M-x compile,
the results will be displayed in a buffer in Compilation Mode. The command C-x ‘ will
visit the locus of the next error message or match (next-error) in your cpsa input file.

#### 2.3.3 Using the Haskell Makefile

This approach is designed to be easy for Windows users, who do not want to bother installing
Cygwin or MSYS.
   Locate Make.hs in your project directory. If using Windows, double-click on the file
and it will open up a new window with a prompt. On a Mac or Linux machine, run $ ghci
Make.hs
   From the Make.hs prompt, you can use the following commands:

   • build: Run cpsa on all protocols (.scm files) in the directory, and produce .xhtml
     output files displaying the results.

   • clean: Remove all cpsa output files, to ensure that any changes to protocol files are
     reflected in the output.

        – Because intermediate files are used for behind-the-scenes processing, it can be
          possible to have the results in the .xhtml output files not reflect the most up-todate
 protocol file contents. If you make changes and don’t see them reflected in
          the output, try running clean. Getting into the habit of running clean before
          build is a good idea.

   • cpsa4 "protocolname ": Run cpsa on just the protocol provided. Note that the file
     extension (.scm) should not be included in the name; if your protocol is in foo.scm,
     you would run cpsa4 "foo". Most useful if you have an exceptionally large number
     of protocols in a single directory.

   • :q Quit.

#### 2.3.4 Memory usage

On large problems, cpsa can consume large amounts of memory. To protect against memory
 exhaustion, run cpsa with the command-line options +RTS -M512m -RTS. The initial
makefile includes these options by default.

#### 2.3.5 Parallelism

CPSA is built so it can make use of multiple processors. To make use of more than one
processor, start CPSA with a runtime flag that specifies the number of processors to be
used, such as +RTS -N4 -RTS. The GHC documentation describes the -N option in detail.

## Chapter 3: Basic Protocol Modeling and Analysis with CPSA

This chapter is designed to be a tutorial for a new user with access to the tool, but totally
unfamiliar with the ideas behind it. We will explain the basics of the tool while stepping
through an example input and its output. Input and output for the examples in this chapter
and in other chapters are included in the distribution. Explorations are included for readers
to build their understanding of the tool through experience. If you are a new user but do
not intend to work through the explorations, we recommend that you at least copy the
input files and run the tool yourself to check that you can produce outputs mirroring those
in the distribution.
    The first protocol we discuss is the Needham-Schroeder protocol for establishing key
transport over insecure networks. The protocol has two participants: an initiator a and a
responder b. The intention is for the following interaction to take place:

  1. a picks a fresh, random nonce n1 and encrypts a message containing n1 and a’s name
     under b’s public encryption key, and sends the result to b.

  2. b, on receiving such a message, picks a fresh random nonce n2 and encrypts a message
     containing n1 and n2 under a’s public encryption key, and sends the result to a.

  3. a, on receiving this reply, encrypts n2 under b’s public encryption key and sends the
     result to b.

    The intention is that a and b should have authenticated each other (that is, that a is
communicating with b and vice versa) and that the pair of nonces establish a unique session
of such authentication. The nonces should also be unreadable by the network adversary, so
that they can be used to create a session key between a and b.
    This protocol has a well known but non-obvious flaw discovered by Lowe [10] that cpsa
can discover automatically.

                      init      / {|n1 , a|}K            {|n1 , a|}Kb       / resp
                                                b

                                                                              
                       •o       {|n1 , n2 |}Ka           {|n1 , n2 |}Ka o     •

                                                                             
                       •         / {|n2 |}K                {|n2 |}Kb         /•
                                           b
**Figure 3.1: Needham-Schroeder initiator and responder roles**

### 3.1 Basic CPSA modeling

In order to use cpsa on this protocol, we must first understand some basics about how
cpsa models protocols and messages.
     Since cpsa’s aim is to analyze protocols in the presence of a powerful network attacker,
we equate the network with the attacker, and do not model the notion of addressing of
messages. The description provided above for Needham-Schroeder describes messages that
(for instance) a sends to b. In cpsa, we ignore the intended recipient because the attacker
is free to ignore it.
     The protocol can be thought of as made up of the roles that entities can play during the
protocol. In the case of Needham-Schroeder, there are two: the initiator and the responder.
These roles describe the sequence of message-related events each party observes during the
protocol. The events are described by giving a formula for the format of each message,
along with an indiciation whether each event is a reception of a message or a transmission
of one.
     Messages in cpsa are represented as formally structured objects, specifically as terms
in an order-sorted algebra [4]. Terms are either variables or functional outputs of simpler
terms. Variables have types called sorts, and function symbols have specific signatures that
specifies the sorts of each input and the sort of the output. The roles of Needham-Schroeder
are given in Figure 3.1.
     The messages in these roles are built from variables (n1 , n2 , a, b) and function symbols;
the three function symbols used in this protocol are encryption, pairing, and the “key of”
function.
     {|m|}k denotes the encryption of message m under encryption key k. In cpsa, encryption
 operators are always regarded as offering authenticated encryption, meaning that a
participant without access to an encryption key is overwhelmingly unlikely to generate a
message that can be successfully decrypted. This property is primarily relevant in symmetric
 (secret-key) kinds of encryption.
     Terms in a pair are represented in comma-separated lists. And Ka denotes the result

of the “key of” function symbol on input a. This represents the public key (either an
encryption key or a signature verification key) of a. The values n1 and n2 are of a different
sort than a and b: the latter are names to which the K(·) function can be applied, while n1
and n2 are simple values.

```scheme
                       (defprotocol ns basic
                         (defrole init
                           (vars (a b name) (n1 n2 text))
                           (trace (send (enc n1 a (pubk b)))
                                  (recv (enc n1 n2 (pubk a)))
                                  (send (enc n2 (pubk b))))
                         (defrole resp . . . ))
```
**Figure 3.2: Needham-Schroeder defprotocol**

    In addition to a description of the protocol, cpsa expects the description of what we
call a skeleton—a partial protocol execution. A skeleton is made up of instances of the
roles, that is, viewpoints of honest parties, along with what values are associated with the
variables in those viewpoints. These viewpoints may be partial, but they always represent
a prefix of a full role.

### 3.2 CPSA input

The ns.scm file in the examples directory contains a protocol description for Needham-
Schroeder and two skeletons: one representing the viewpoint of a completed initiator, and
one representing the viewpoint of a completed responder. The .scm extension used for
cpsa input files refers to the Scheme programming language, which is a language derived
from Lisp. This allows the user to make use of an IDE or text editor that knows about
Scheme syntax, for ease of editing input files. The cpsa tool itself does not require any
particular extension, but auxiliary tools may, including the Make.hs program described in
Section 2.3.
     The input file for Needham-Schroeder contains comments found on lines beginning with
‘;’, and four top-level S-Expressions: a herald, a defprotocol, and two defskeletons. We
will describe heralds in Section 10.5.1; ignore them for now.
     The defprotocol S-expression describes and names a protocol, while the defskeleton
describes a skeleton, referencing a particular protocol. A portion of the Needham-Schroeder
defprotocol is reproduced in Figure 3.2 for ease of reference.
     A defprotocol S-expression starts with a protocol name, ns in this case, followed by
the name of a message algebra. The basic algebra contains enough elements to describe
Needham-Schroeder and most simple examples; the only other algebra contained in the

cpsa distribution is diffie-hellman; see Chapter 4, and specifically Section 4.2, for details
of the Diffie-Hellman algbera.

```scheme
                         (defskeleton ns
                           (vars (b name) (n1 text))
                           (defstrand init 3 (b b) (n1 n1))
                           (non-orig (privk b))
                           (uniq-orig n1))
```
**Figure 3.3: Initiator point of view**

```scheme
                         (defskeleton ns
                           (vars (a name) (n2 text))
                           (defstrand resp 3 (a a) (n2 n2))
                           (non-orig (privk a))
                           (uniq-orig n2))
```
**Figure 3.4: Responder point of view**

    The rest of the defprotocol S-expression is a sequence of roles, each defined by a
defrole S-expression. In our example, there are two roles, and thus two defroles, the first
defining the initiator role (init) and the latter describing the responder role (resp).
    The first input to a defrole is a role name; the second should be a set of variable
declarations (vars), and the third should be a trace declaration which describes the event
sequence of the role. The variable declarations define and give types to the variables used
in the role’s trace. The trace S-expression defines the list of events: a recv S-expression
describes a reception and send describes a transmission.
    Function symbols in the cpsa message algebra have specific S-expressions associated
with them. enc denotes an encryption, cat denotes a pair, and pubk denotes the “key of”
function. You may notice that cat does not occur in the figure: this is because its use is
hidden by “syntactic sugar”—a convenient shortcut in the syntax. The message (enc n1 a
(pubk b)) is more properly the encryption of the pair (n1 , a) under the key Kb , but when
an enc S-expression is given more than two inputs, it is assumed that all but the last are
concatenated together using pairs.
    In Figures 3.3 and 3.4, we reproduce the skeletons described in our example input file. A
defskeleton S-expression includes first of all a protocol name, then variable declarations,
and then a list of instances, most of which are defined by the defstrand S-expression.
A defstrand includes an input specifying the name of the role the strand is an instance
of, as well as a height, that is, a number of the events (send / recv) in the role that
are to be reflected in the instance, starting from the first event. In our example input,
each defskeleton includes one defstrand, which defines an instance of height 3 since that
refers to a full execution of either role in the protocol. A defstrand S-expression may

optionally include maplets that specify values to be used to instantiate variables in the role
specification. A maplet is a parentheses-delimited pair where the first element is the name
of the role variable to be instantiated and the second is the value, which can be any term
formed over the variables declared in the vars portion of the defskeleton.
    A defskeleton will usually have one or more declarations in it that restrict the class
of executions the tool is to explore. Here, each example includes two declarations: one
non-orig declaration and one uniq-orig declaration. Declarations must be made about
expressions that can be parsed given the variables in the defskeleton; it is because of these
declarations that we specify an instantiation of certain variables in a defstrand.
    A non-orig declaration specifies a value (usually a symmetric or private key) as secret
and never sent by honest parties in any potentially decryptable form. A uniq-orig declaration
 specifies a value as being randomly and freshly chosen where it first occurs in a
transmission. Here, the initiator point of view specifies two assumptions: that the initiator
picks her own nonce properly (i.e. randomly), and that the initiator’s intended communication
 partner has an uncompromised private key. Similarly, the responder’s point of view
assumes that the the responder picks his own nonce properly and that his intended partner
has an uncompromised private key.

### 3.3 CPSA output

When we run the cpsa tool on the Needham-Schroeder input file, and then run the
cpsa4graph graphing tool on the result, we obtain a .xhtml file that can be viewed in
a web browser. The ns.xhtml file in the examples directory contains these results.
     The graphing output contains some top matter that includes the herald from the input
file. Below this is a list of trees, each of which represents the analysis of one of the input
defskeletons; in the case of our example, there are two trees.
     The rest of the graph output consists of the search results. The numbers in the list of
trees link to the start of each tree. Each search result starts with an identification (“Tree
0” in the example), followed by a graph of the search, then the defprotocol used in that
search, and then the skeletons considered by cpsa during its analysis. Figure 3.5 illustrates
the list of trees, the tree identification, and that tree’s search graph.
     The search tree diagrams the steps in the search. Each skeleton in the entire graph
file has a label, a number starting from 0. The number associated with a tree is the label
number of the input skeleton. The left edge of the search graph is the root of the tree: in
the case of Figure 3.5, the graph does not look very tree-like because the analysis doesn’t
branch. The numbers in the graph are the labels of the skeletons considered by cpsa during
its analysis, and clicking on a number will direct the browser to display the corresponding
skeleton.
     The process by which cpsa analyzes a skeleton is the repeated use of an operation called
the cohort, which takes an input skeleton and produces a set of more refined skeletons that

cover all the possible executions the input skeleton covered. The relationship between a
parent skeleton and a child is that a child is included in the cohort calculated with the
parent as an input.
**Figure 3.5: Search tree diagram for the initiator point of view in ns.xhtml**

    Numbers are normally displayed in black, but may also be displayed in other colors.
Blue numbers represent shapes, that is, skeletons that represent a minimal execution.1 Red
numbers represent dead skeletons, that is, skeletons that represent partial executions that
are not part of any actual execution—in other words, impossible scenarios.
    Numbers may occur in the tree more than once, because it is possible that cpsa will discover
 a particular skeleton through more than one branch of the analysis. Green, italicized
numbers represent skeletons present in more than one branch that are not dead skeletons,
while orange italicized numbers represent dead skeletons present in more than one branch.
    Each skeleton starts with a line that indicates its label (item) and the labels of its
parent ((parent), if any) and its children ((child), if any) See Fig. 3.6) The parent and
child numbers link to those skeletons, while the “item” number links back to the tree this
skeleton is part of.
    Below the diagram is a defskeleton that fully describes the skeleton. This text is fully
compatible with cpsa input and can be used as a skeleton input for analysis with this
protocol, although some of the fields in it are added by cpsa and would be ignored during
input, for instance, the label and parent fields.
    The diagram shows the skeleton as a graph. Strands are columns, ordered from top
to bottom. The nodes in the graph are events, normally transmissions or receptions of
messages. Nodes may be blue, red, or black; a black node represents a transmission, while
blue and red nodes represent receptions. A blue node represents an explainable reception
while a red node represents an unexplainable one. The left-most strands in a skeleton are
normally the strands from the input defskeleton.
    Note that sometimes cpsa encounters a realized skeleton representing an actual execution before a
shape. It does further analysis once a realized skeleton is reached in order to generalize that skeleton as
much as possible to obtain a minimal execution (i.e., a shape). Realized skeletons that are not shapes are
displayed in gray. See page 33 for more detail on generalization.
**Figure 3.6: Skeleton from the initiator point of view in ns.xhtml**

    The user may hover their mouse cursor over any node and will see a display of the
S-expression describing the message at that event (see Figure 3.6). Here, if we hover over
the red node (as shown) we will see that this is an event where the initiator receives the
message {|n1, n2|}Ka . This occurs after two transmissions: the first event in the init strand
and the second in the resp strand. Those two transmissions are {|n1, a|}Kb and {|n1, n20 |}Ka .
Neither transmission is the expected message, but sometimes a reception can be explained
even if no regular node sends the exact message. Here, it is a question of what the adversary
can build given the messages available. In this skeleton there are non-orig or uniq-orig
assumptions about n1, SKa , and SKb , so since both messages are encrypted under keys
for which we have a secrecy assumption on the decryption key, the adversary is unable to
decrypt them. The adversary is also unable to build the required message: although the
adversary is allowed access to n2 and Ka (since there are no restrictions on those), the
adversary does not have access to n1. Hence, this node is unexplainable.
    Arrows in the diagram represent basic orderings in the skeleton; arrows go from earlier
events to later events. An arrow is solid when it goes from an event transmitting a message
to one receiving the same message. So the blue node in this example is obviously explained
because the exact message was transmitted by the initiator, specifically, at the first node
in the initiator strand. The arrow ending at the red node is dashed because the messages
do not agree, but it still represents that in this skeleton the second node of the responder
strand occurs before the second node of the initiator strand.

### 3.4 Interpreting shapes

Next, we turn our attention to Figure 3.7, which is the one shape found by cpsa during
the search on the initiator point of view.
    Before we get into detail on what is contained in this skeleton, note the graph. All the
arrows are solid, and there are arrows everywhere we expect them to be. This describes
a message being sent by an initiator and received, unaltered, by a responder, who then
sends a message that is received, again unaltered, by the same initiator, who then sends a
message.
    The user can hover their mouse cursor over the name of the role at the top of a strand
in the skeleton diagram to see the variable assignment used in that instance. Here, hovering
over both the instances indicates that they are in agreement about the values of n1, n2, a,
and b: that is, the initiator’s internal value for each variable is the same as the responder’s
internal value for the variable of the same name.
    It may seem slightly odd that the initiator sends a message in its third node that is not
received by anyone, but we know that in general it need not be received. The adversary
completely controls the network, so it does not have to deliver that message.
**Figure 3.7: The only shape from the initiator point of view (ns.xhtml)**

The responder’s point of view. The shape found during the search on the responder’s
point of view, however, includes something unusual. See Figure 3.8.
     The graph of this shape should look less like expected behavior. Two things look odd,
even at first glance. Most noticeable is the dashed arrow from the third initiator node to
the third responder node. Also, there’s the fact that there is a blue node (the one in the
top left) that does not have any arrow coming in.
     Inspection of the instances in this shape reveals that the initiator and responder agree
on all the values except for b. This explains the dashed arrow: the initiator sends {|n2|}Kb0
but the responder receives {|n2|}Kb ; these messages are not the same, which is why the arrow
is not solid. As for how the responder could receive the proper value, note that we only
assumed SKa and SKb are secure, but we did not assume SKb0 was secure. It would have
been hard to do so, since b0 is a value we know nothing about from the responder’s point
of view. The initiator’s transmission of {|n2|}Kb0 thus does not protect n2 from decryption,
so an attacker could have created the responder’s received message by encrypting n2 under
Kb .
     The lack of an incoming arrow for the responder’s first node can be explained because
of the lack of any assumption about the value n1. The value n1 is the initiator’s nonce, but
this analysis does not assume that an initiator, if present, will choose their nonce properly.
So n1 could actually be a value already chosen by the adversary, and the message {|n1, a|}Kb
can be constructed and delivered to the responder before the initiator even starts.
     The fact that the initiator and responder do not agree on b is an interesting feature of
this protocol. We know from the initiator’s point of view that the initiator a, when they
have completed their execution, can infer that b has taken part in the responder role with
a, and that they agree on both nonces.
     The responder’s point of view leads to less information. The responder b knows that a
has taken part in the initiator role, but does not know that a intended to initate communication
 with b. This lets us conclude that the Needham-Schroeder protocol provides less
than an ideal level of authentication.
**Figure 3.8: The only shape in the responder point of view search in ns.xhtml**

**Exploration 3.1.** The attack described above was first identified by Gavin Lowe [10], who
also proposed a fix, namely, to have the second message in the Needham-Schroeder protocol
include the name b of the responder.
    Make a copy of the Needham-Schroeder input file and modify the protocol so that the
second message (in both roles) includes a b. Run the analysis again and graph it. You
should observe that the disagreement on b from the responder’s point of view is no longer
possible, and that the initiator’s point of view is still good.

### 3.5 Blanchet’s simple example protocol
Next we turn our attention to a second protocol, which will help build the reader’s experience
 with cpsa and also introduce some additional features. This protocol is due to

Bruno Blanchet, and has a flaw introduced by design for the purpose of discussing protocol
analysis. In this protocol there are again two participants: an initiator and a responder.
However, in this protocol, we do not use names, just public keys. Specifically, one party
has a public signing key (a), while the other has a public encryption key (b).

```scheme
                     (defprotocol blanchet basic
                       (defrole init
                         (vars (a b akey) (s skey) (d data))
                         (trace (send (enc (enc s (invk a)) b))
                                (recv (enc d s)))
                         (uniq-orig s))
                       (defrole resp
                         (vars (a b akey) (s skey) (d data))
                         (trace (recv (enc (enc s (invk a)) b))
                                (send (enc d s)))
                         (uniq-orig d)))
```
**Figure 3.9: The Blanchet simple example protocol**

   The protocol is as follows, informally:

   • The initiator chooses a fresh, random session key s, signs it with their private signing
     key (corresponding to the public key a), and encrypts it with the responder’s public
     key b and sends the result to the responder.

   • The responder receives and decrypts such a message, confirms the signature, and then
     encrypts a piece of data d under s and sends this back to the initiator.

    The file blanchet.scm in the examples directory contains Blanchet’s simple example
protocol described above. See Figure 3.9 for the protocol declaration.
    There are several elements of this protocol input that are new. First of all, the Needham-
Schroeder protocol used only two types: name and text, while this protocol uses three new
types. The data type is for simple values, much like text. In fact, the two types are
interchangeable, but both are available for cases where an analyst may wish to describe a
protocol in which two types of simple values exist that cannot be confused for each other.
    The akey and skey types are for keys, specifically, asymmetric and symmetric keys,
respectively. The invk function symbol maps an asymmetric key to its inverse.
    Note that we use (enc s (invk a)) to represent the digital signature. A digital signature
 in the cpsa message algebra is represented as an encryption under the signature
key.
    A third feature is the presence of a delcaration such as (uniq-orig s) within a defrole.
Like the uniq-orig declaration that can appear in a skeleton, this declaration indicates
that the value contained inside is freshly chosen. When this declaration appears in the role,

however, the assumption is that the value is freshly chosen by every honest participant
in the protocol who plays that role. Declarations present in a role are inherited by every
skeleton with an instance of that role. See Chapter 6 for more on the declarations supported
by cpsa.

```scheme
                   (defskeleton blanchet
                     (vars (a b akey) (s skey) (d data))
                     (defstrand init 2 (a a) (b b) (s s) (d d))
                     (deflistener d)
                     (non-orig (invk b)))
```

```scheme
                   (defskeleton blanchet
                     (vars (a b akey) (s skey) (d data))
                     (defstrand resp 2 (a a) (b b) (s s) (d d))
                     (deflistener d)
                     (non-orig (invk a) (invk b)))
```
**Figure 3.10: Blanchet points of view**

**Exploration 3.2.** Make a variant of the Needham-Schroeder protocol in which the freshness
 of each party’s nonce is assumed via a uniq-orig declaration in the protocol role. Run
the analysis from each participant’s point of view. What differs in the shapes, and why?
(There should be one difference that’s noticeable in the graph of one of the shapes.)

**Exploration 3.3.** Make a variant of the Needham-Schroeder protocol in which the secrecy
of each party’s partner’s private key is assumed via a non-orig declaration in the protocol
role. Run the analysis from each participant’s point of view.
    You should observe that the authentication failure is no longer present in the shape
from the analysis of the responder’s viewpoint. What conclusion can you draw about this
declaration? Did we fix the protocol? If not, why does the analysis seem to contain no
flaws?

    The blanchet.scm file contains four inputs to the analysis. The first and second are
just the points of view of each participant, under typical assumptions. But the third and
fourth contain another new element. See Figure 3.10 for these two inputs.
    These two inputs are prepared to ask a confidentiality question: specifically, is the
value d exposed to the adversary? A listener is a pseudo-role that is considered part of
all protocols by cpsa. That role consists of receiving some arbitrary message and then
sending that same message. Listeners can show up in cpsa analyses, in order to handle a
case where a certain value is learnable, so that the rest of the case breakdown can assume
that value is not learnable.
**Figure 3.11: The search tree for the privacy of d in the initiator’s point of view in blanchet.xhtml**

    In this protocol, the secret data d remains private in the initiator’s point of view.
Figure 3.11 shows the search tree for the point of view in which the initiator completes the
protocol and in which there is a listener for the same d value the initiator hears. The fact
that all the numbers are red here indicates that all the skeletons in the search are “dead”,
meaning that they are inconsistent with any actual executions. In other words, there are
no executions in which d is revealed given our assumption that the private decryption key
of b is not compromised.
    However, d does not remain private in the responder’s point of view. Figure 3.12 shows
the graph of a shape for the point of view in which the responder completes the protocol
and in which there is a listener for the d value the responder sends. Note that although d
is encrypted under s, and s is freshly chosen by an initiator, the shape shows that s can
leak. We are not guaranteed that the initiator and responder agree on b. Therefore, the
initiator may have sent s encrypted with b0 , and since the private key corresponding to b0
is not necessarily secret, s may leak.
    The blanchet.scm file also contains a second protocol named blanchet-corrected in
which the flaw that allows d to be learned in the responder’s point of view is eliminated.
**Exploration 3.4.** Modify the Blanchet protocol to add a role that is identical to the
initiator role, except that s is not declared uniq-orig. What impact does this have on the
analyses?
**Exploration 3.5.** If you modify the Blanchet protocol to instead add a role that is identical
to the responder role, except that d is not declared uniq-orig, what impact do you believe
this will have on the analyses? Make a prediction, then check your prediction.
**Figure 3.12: The only shape in the analysis for the responder’s point of view with a listener for d in blanchet.xhtml. The second strand, with no role name, is the listener.**

**Exploration 3.6.** Try modifying the Blanchet protocol, removing the uniq-orig declarations
 from the two roles. Replace the defskeletons in the input file with the point of view
skeletons for the un-corrected version of the Blanchet protocol from blanchet.xhtml; these
skeletons will explicitly include declarations that would be inherited but were lost due to
the removal of the role declaration.

## Chapter 4: Algebra Features of CPSA

The cpsa distribution comes equipped with one cryptographic algebra. For reasons of backwards
 compatibility it has two names: the basic cryptoalgebra and the diffie-hellman
cryptoalgebra. Previous versions of cpsa had separate implementations, but since the
Diffie-Hellman algebra was a pure extension of the basic algebra, we have merged them
back into one. Thus, the Diffie-Hellman features are always available, even when the user
specifies the basic algebra.
    In Chapter 3, we introduced basic components of the cryptoalgebra such as the data,
text, name, skey, and akey sorts, and the pubk, privk, invk, enc, and cat function
symbols. In addition to these, there are the sorts tag and mesg, and the ltk, bltk, and
hash function symbols, and string constants. To represent Diffie-Hellman values we include
two further sorts, rndx and expt, and five new function symbols, exp, rec, mul, gen,
and one.
    At one time variables of sort base were also permitted, but a variable b of sort base has
the same meaning as a term (exp (gen) alpha) where alpha is of sort expt. Eliminating
variables of sort base allows us to eliminate some tricky but conceptually unnecessary,
even practically unnecessary, code. Thus, replace these variables with (exp (gen) alpha),
where alpha is a variable of sort expt. We still refer to these terms as having sort base,
since they may be the bases for further exponentiation, but there are no variables of this
sort.
    In this chapter we will explain these additional features with examples. In Section 4.1,
we will discuss the ltk function symbol and the use of the mesg sort, worked with an
example based on the Kerberos protocol. In Section 4.2, we will discuss the tool’s Diffie-
Hellman features. In Section 4.3, we will discuss the remaining features, and note examples
that demonstrate their use. For a more complete reference about the two algebras, see
Section 10.3.

### 4.1 Generic messages and long-term keys

Securing communications purely with symmetric keys faces an inherent scaling problem:
when there are n parties that may wish to communicate, there must be O(n2 ) keys shared
between parties, which gets to be too many in any system with a large number of users.
    The Kerberos protocol is a well-known protocol for the distribution of symmetric keys.
Instead of having the n parties share keys with each other party, the users share a key only
with a central key server (also known as a key distribution center). The key server controls
key distribution within a realm that can be thought of as the set of users that share keys
with the key server.
    Suppose a user wishes to communicate securely with another user in the same realm.
The first user would contact the key server and request a session key for communication
with the other user. The key server could then encrypt the session key twice, once under
each user’s shared key with the server. One encrypted key is sent back to the user that
requested the channel, and the other (called the “ticket”) is also sent to the requesting user,
to be forwarded on to their communication partner.
    We will focus on a flawed protocol similar to the initialization protocol used by Kerberos.
The protocol is described informally as follows. There are three parties, the initiator a, the
responder b, and the key server s.

   • a sends a message (a, b, n) to the key server, where n is a freshly chosen nonce.

   • The key server, on a message (a, b, n), picks a fresh, random session key k, and sends
     two encryptions to a: {|k, n|}SK(a,s) and {|k, a, b|}SK(b,s) . Here, SK(x, s) refers to the
     shared secret between the key server and x.

   • a receives these two messages, decrypts the first to learn k and to check that the
     proper nonce n was included, then sends a message m on to the responder, encrypted
     under k, along with the second message (the ticket).

   • b receives two encrypted messages, decrypts the second to learn k, and decrypts the
     first with k to learn the message.

    The ltk function symbol is used in cpsa to represent long-term shared keys between two
specific parties, when communication of that key is assumed out of scope of the analysis. See
Figure 4.1 for a defprotocol that attempts to describe this flawed version of the Kerberos
initialization protocol. See kerb.scm in the examples directory for the input file discussed
here.
    The actual Kerberos protocol contains several additional elements that we omit for
simplicity, but the key difference is that the message encrypted under SK(a, s) should
include b. The message from the initiator that requests a session key is transmitted in the
clear and can be tampered with, so the initiator needs assurance that the session key k is

being exposed only to the initiator and b. Otherwise, even assuming the long-term keys of
both a and b with the key server are secure, a third party may observe the message m: all
the adversary has to do is block the initial message and substitute b with another name c.

```scheme
      (defprotocol kerb-flawed basic
        (defrole init
          (vars (a b s name) (m n text) (k skey))
          (trace (send (cat a b n))
                 (recv (cat (enc k n (ltk a s)) (enc k a b (ltk b s))))
                 (send (cat (enc m k) (enc k a b (ltk b s)))))
          (uniq-orig n))
        (defrole keyserv
          (vars (a b s name) (n text) (k skey))
          (trace (recv (cat a b n))
                 (send (cat (enc k n (ltk a s)) (enc k a b (ltk b s)))))
          (uniq-orig k))
        (defrole resp
          (vars (a b s name) (m n text) (k skey))
          (trace (recv (cat (enc m k) (enc k a b (ltk b s)))))))
```
**Figure 4.1: A flawed version of Kerberos**

```scheme
                  (defskeleton kerb-flawed
                    (vars (a b s name) (m text))
                    (defstrandmax init (a a) (b b) (s s) (m m))
                    (deflistener m)
                    (non-orig (ltk a s) (ltk b s))
                    (uniq-orig m))
```
**Figure 4.2: Flawed Kerberos point of view**

    Will cpsa find this attack? See kerb.xhtml for the results of the analysis for the point-of
-view skeleton described in Figure 4.2. Note the use of defstrandmax; this is a shortcut
you can use in cpsa to specify a full-height instance of a role.
    Interestingly, the result of the analysis does not indicate any attack is possible! The
analysis gets stuck at a skeleton (see Figure 4.3) where the key server does in fact generate
a session key for a and b, and where that session key is exposed, but it cannot be exposed if
it was generated for a and b and if we are assuming both of their long-term keys are private.
    The reason cpsa gets the wrong result here is that we have inadvertently modeled
our protocol question incorrectly. Specifically, we have described a version of the protocol
where the initiator is able to check the validity of the ticket. The attack we have in mind
is one where the two encrypted keys received by the initiator are prepared by a key server

instance, but one which does not agree with the initiator on b. However, the ticket would
not match what the initiator expects in our expression of the initiator role.1
**Figure 4.3: Flawed Kerberos dead skeleton. The use of the mesg sort provides a fix to this badly modeled version of the protocol.**

```scheme
       (defprotocol kerb-flawed2 basic
         (defrole init
           (vars (a b s name) (m n text) (ticket mesg) (k skey))
           (trace (send (cat a b n))
                  (recv (cat (enc k n (ltk a s)) ticket))
                  (send (cat (enc m k) ticket)))
           (uniq-orig n))
         (defrole keyserv
           (vars (a b s name) (n text) (k skey))
           (trace (recv (cat a b n))
                  (send (cat (enc k n (ltk a s)) (enc k a b (ltk b s)))))
           (uniq-orig k))
         (defrole resp
           (vars (a b s name) (m n text) (k skey))
           (trace (recv (cat (enc m k) (enc k a b (ltk b s)))))))
```
**Figure 4.4: Using a variable of sort mesg in a flawed version of Kerberos**

    We described an initiator that will only proceed onto the third step (sending m) if the
ticket is of the form we specified. In fact, the initiator cannot do this. The initiator cannot
even verify that the ticket is encrypted under the correct key! The solution is to use a
generic variable, one that can stand for any message, even one that a particular participant
cannot parse or understand. The mesg sort is the sort of all possible messages, so a variable
of the mesg sort can stand for any potential value at all. See Figure 4.4 for a version that
models the initiator’s reception properly. Note the ticket variable in the initiator role,
which stands for the ticket value the initiator cannot inspect.
    This version of the flawed Kerberos protocol may also be found in the file kerb.scm, and
its analysis may be found in kerb.xhtml. This time, there is a shape found. See Figure 4.5.

Notes on generic variables. Variables of the mesg sort are constrained in cpsa, and
may only be used when they are received before they are transmitted. So for instance the
m variable in the initiator role of the flawed Kerberos protocol cannot be of the mesg sort,
because it appears first in a transmission. However, if the responder is willing to accept an
encryption of any message m, then m may declared as a variable of the mesg sort within
that role.
     An alert reader may wonder how they could detect such an error of their own when using the tool. We
will return to this example in Chapter 5, when we discuss how the cpsa search process works.
**Figure 4.5: Flawed Kerberos shape. The use of the mesg variable allows us to find the attack illustrated here.**

   Also, variables of the mesg sort should never be used as a key in any encryption. This is
because cpsa uses a single function symbol to represent both symmetric and asymmetric
encryption, and when the key is a variable of sort mesg, it is ambiguous which is meant.

Notes on long-term keys. Long-term keys are uni-directional: (ltk a b) and (ltk b
a) are distinct values. In fact, cpsa believes that they cannot be the same unless a = b.
This is fine for modeling protocols like Kerberos where there is a clear distinction between
client and server behavior. Note that in our protocol example, all long-term keys were
described in all roles with a client name in the first position and a server name in the
second position. See Section 4.3.3 for discussion of the bltk function symbol, which models
bi-directional long-term symmetric keys.
    For another example of the use of long-term symmetric keys in a protocol, see yahalom.scm
in the examples directory.
**Exploration 4.1.** Fix the flawed version of Kerberos so that the initiator can believe their
transmission is private to them and b. Continue to use the ticket variable of sort mesg.
    Construct a defskeleton for the responder’s point of view for your fixed protocol,
analyze it, and explain in English what authentication property this analysis implies.
**Exploration 4.2.** Construct a defskeleton for the initiator’s point of view, without the
listener for m, in the fixed version you created in Exercise 4.1. Run the tool on your
defskeleton. Why are there dashed arrows in the result? Does this represent an insecurity
in the protocol?
    Whether or not you think this is an insecurity, think about how you would alter the
protocol to avoid the dashed arrows, and try out your ideas.
   The Otway-Rees protocol is another example of very similar modeling; see or.scm and
or.xhtml if you wish to explore these issues further on your own.

### 4.2 Modeling Diffie-Hellman

In their seminal 1976 paper, “New Directions in Cryptography”, Diffie and Hellman proposed
the notion of public-key cryptography [1]. They did not have a method for public-key direct
encryption, but they did have a key exchange protocol that has become a crucial building
block in cryptographic protocols.
    The Diffie-Hellman protocol works as follows. A large prime number p is chosen and
agreed upon as a parameter, and g is chosen to be some integer modulo p. In order to enable
secure communication between arbitrary parties, Diffie and Hellman imagined a directory
of public values, like a phone book. Each person who wishes to be able to communicate
securely with others will generate for themselves a private value x, and publicize g x mod p
as their public value. If Alice’s private value is a, and Bob’s private value is b, then the
shared secret between Alice and Bob would be g ab mod p, which each party can calcuate

from their own private value and their partner’s public value. For instance, Alice can
calculate g ab ≡ (g b )a mod p.
    The cryptoalgebra for cpsa includes features to represent values that allow for analysis
of protocols that incorporate Diffie-Hellman techniques. Whether the user asks for the
basic algebra or the Diffie-Hellman algebra, the result is the same: They get an algebra
that includes all the function symbols and sorts available in the original basic algebra, plus
two additional sorts of variable, namely the two sorts rndx and expt for exponents such as
x. The Diffie-Hellman specific function symbols are as follows:

   • exp represents exponentation. For example, hx is encoded as
     (exp h x).

   • mul represents multiplication of exponents. So if x is an exponent,
     (mul x x) would represent the square of x.

   • gen represents the standard generator g. It is probably best to think of gen as a
     constant, i.e. a function symbol with arity 0.

   • one represents the multiplicative identity for the group of exponents. Like gen, one
     is a 0-ary function.
     Important: gen and one are functions, so they must be enclosed in parentheses. So
     (exp (gen) x) represents g x , while (exp gen x) would represent genx where gen is
     expected to be a variable. Similarly, (mul (one) x) represents 1 · x while (mul one
     x) would represent one · x where the tool expects one to be an exponent variable. (In
     fact, using (exp gen x) would result in an error message since cpsa does not allow
     variables of the same sort base as (gen). But (mul one x) would produce no error
     because one can be the name of an expt variable.)

   • rec represents the multiplicative inverse in the group of exponents. So for instance
     (exp (exp (gen) x) (rec x)) = (exp (gen) (one)) = (gen).

    At this time, cpsa does not model addition of exponents, although there are many
examples of protocols that add or subtract exponents. There is no way to take a product
of exponentiated values either (e.g. g x · g y ) since this would be equivalent to including
addition of exponents.
    Several examples of Diffie-Hellman protocols are available in the examples directory
of the distribution. The plaindh.scm example models a simple, unauthenticated Diffie-
Hellman exchange between two parties.
    The initiator and responder perform a Diffie-Hellman exchange, followed by the initiator
choosing a random nonce n and sending it, encrypted with the Diffie-Hellman key, to the
responder, who decrypts n and sends it back.

```scheme
                  (defprotocol plaindh diffie-hellman
                    (defrole init
                      (vars (x rndx) (y expt) (n text))
                      (trace (send (exp (gen) x))
                             (recv (exp (gen) y))
                             (send (enc n (exp (gen) (mul y x))))
                             (recv n))
                      (uniq-orig n)
                      (uniq-gen x))
                   ...)
```
**Figure 4.6: Diffie-Hellman defprotocol**

    The analysis result can be found in plaindh.xhtml. You can see there that a shape is
found where an initiator exists but no responder; the n can be decrypted because g xx0 can
be calculated by the adversary when x0 is not assumed secret.
    Two features of the cpsa model of Diffie-Hellman in this protocol are worth drawing
attention to. See Figure 4.6
    Note that the initiator uses a variable x of the rndx sort to represent its own random
variable, and a variable y of the expt sort to represent the exponent present in the base value
(exp (gen) y) it receives from the initiator. Distinct values of the rndx sort model distinct
independent random choices of exponents, while expt values merely represent arbitrary
exponents which may or may not be calculated as some product of other known values.
Here, since the initiator chooses their own exponent, we model x as an rndx value. But
since the initiator cannot know how the base value g y was calculated, we model y as an
expt value.
    Note that unlike the example in Section 4.1, where receiving a specifically formatted
encryption in a protocol role implied the ability to decrypt and check that structure is
present, the use of a value like g y in a reception does not imply that y is known, only that
y is defined to be the value such that g y is the base value received.
    Second, you may notice that n is declared uniq-orig while x is declared uniq-gen. The
difference between these declarations is rather technical: see Section 6.2 for details. For the
moment, it is sufficient to say that one should use uniq-gen for exponents that first occur
within an exponentiation, rather than uniq-orig.
    It is also instructive to examine the two final skeletons in the analysis that leads to the
shape; see Figure 4.7. The first realized skeleton reached in the branch is skeleton 4, on
the left, which includes an instance of the initiator role and a listener. But this realized
skeleton has a child: skeleton 5. The difference is that skeleton 5 does not include the
listener. This is an example of a step that cpsa takes called generalization: when cpsa
recognizes a realized skeleton (that is, one that has no unexplainable receptions), it attempts
**Figure 4.7: Deletion of strand**

to identify ways to make that skeleton more general without losing coverage. Here, cpsa
has deleted the listener, because that actual explicit reception and re-transmission of g xx0
is not strictly necessary. When a realized skeleton cannot be further generalized, cpsa
declares it a “shape” and stops working in that branch of the analysis.
    You may notice there is another shape in plaindh.xhtml, in which a responder is
present. As it happens, the other shape is strictly less general than the shape shown as
skeleton 5. cpsa does not promise that the set of shapes it outputs is strictly minimal, and
this is one example where the output of cpsa is not minimal.

#### 4.2.1 Other examples

The examples directory also contains the station.scm and station.xhtml examples that
model the station-to-station protocol. This protocol uses digital signatures in order to
authenticate a Diffie-Hellman exchange so that the key established represents a secure and
authenticated channel. Two versions of the protocol are provided; in one, the Diffie-Hellman

exponents are assumed fresh in the roles, while in the other, they are not. The two analyses
produce different results.
    Another example provided can be found in iadh-um.scm and iadh-um.xhtml. These
inputs concern a method of determining Diffie-Hellman session keys using both long-term
and “ephemeral” exponents called the unified method. The “ia” in the example name stands
for implicitly authenticated, because this method of session key creation allows the parties
to be sure that no other party knows the key. One interesting feature of this input is that it
contains an example of an exponent being transmitted outside of an exponentiation. Specifically
, there is a role in which a party generates and signs their long-term Diffie-Hellman
public value, and then compromises it by releasing the key. The explicit compromise allows
us to test the “forward secrecy” property of the unified method.

### 4.3 Other Algebra Features

#### 4.3.1 Hashing

The cpsa cryptoalgebra includes a hash function symbol that can be used to represent the
use of a hash function. The function takes a single input, but (hash t1 t2 ... tn) is
interpreted as shorthand for (hash (cat t1 (cat t2 ( ...tn) ...))).
**Exploration 4.3.** The Needham-Schroeder protocol discussed in Chapter 3 was described
as for key agreement, but no session key is apparent in the protocol. The intention is to
use the hash of the two nonces as the key. Make a copy of the ns.scm example in which
this key is explicitly used to encrypt and transmit a separate fresh value, and make a point
of view testing the confidentiality of the plaintext.

#### 4.3.2 Constants

Numerous cryptographic protocols make use of magic numbers or string constants to disambiguate
 the purpose of various messages that occur during the protocol. cpsa includes
constant strings in the basic cryptoalgebra. Such constants, which we often call tags, always
appear as quoted strings, e.g. "foo". These strings do not need to be declared in a vars
statement because they are not variables. Tags are messages, so that a variable of mesg
sort may be instantiated by a tag.
**Exploration 4.4.** Note that in the Needham-Schroeder protocol, there seems to be no
way for an initiator to accidentally talk to another initiator, even though the initiator both
sends and receives an encrypted message with two components in it. Make a copy of the
Needham-Schroeder protocol in which the nonces are declared to be of sort name instead
of text, so that {|n1 , a|}Kb and {|n1 , n2 |}Ka are modeled as similar enough in format that
confusing the two is possible. What changes?
    Then try adding distinct tag constants to each encrypted message, to avoid the ambiguity
 we just created. Run the analysis to see the effect.

    Constants may also be used to modify the pubk and privk function symbols, to de-scribe
 distinct keys associated with a particular name. For instance, one might use (pubk
"encrypt" a) to describe the public encryption key of a, so as to distinguish it from the
public signature verification key of a. Or, one might wish to describe a certifying authority
’s certificate-signing key but also a key used to sign certificate revocation statements that
might be different.

#### 4.3.3 Bidirectional Long-Term Keys

The ltk function symbol is used to describe the long-term secret key shared between two
parties. However, the names of the two parties are, in the function symbol, presented in a
distinguished order.
    In other words, cpsa regards (ltk a b) and (ltk b a) as distinct from each other;
in fact, they are only considered equal when a = b. The bltk function symbol regards the
two orders of names as equivalent. That is, (bltk a b) = (bltk b a). In the Kerberos
example discussed in Section 4.1, we noted that the server’s name s always appears second
in our ltk expressions. This is fine if participants never can act as both client and server,
but if a participant can act as both, the use of ltk implies that the participant maintains
a strict separation between the keys they share with other servers when acting as a client
(in which their own name appears first), and keys they share with clients when acting as a
server (in which their own name appears second).
    The use of bltk implies that participants can act as both servers and clients, and that
they only share one key with other entities, and use that key both when acting as a server
and when acting as a client.
    See bltk_or.scm and bltk_or.xhtml for modeling of the Otway-Rees protocol with
bi-directional long-term keys rather than uni-directional ones.
**Exploration 4.5.** Make a version of the flawed Kerberos input file kerb.scm that uses
bi-directional long-term keys instead. What differences do you observe?

**Exploration 4.6.** Repeat the Exercise 4.5 but with the Yahalom protocol (yahalom.scm)
instead.

### 4.4 The Lang Field: Declaring new operators
The signature of the message algebra used by cpsa is extensible. There are two forms
of extensibility provided by cpsa. Users can add operations for encryption, tupling, and
hashing; and add sorts for atomic data.
    A common extension is to add tupling operations to message algebras. Previously,
complex protocols often made use of tagged concatenation to encode a tagged sequence of
messages. In cpsa, concatenation is implemented as sequences of pairing operations. Thus,
the expression for a certificate body of the form

      (cat "cert-body" dn serial-no pub-key)
is syntax for
      (cat "cert-body" (cat dn (cat serial-no pub-key)))

**Table 4.1: Lang Field Syntax**

```text
 lang     ←    (lang ldecl∗)
ldecl     ←    (symbol+ kind)
 kind     ←    atom | akey | hash | (tuple integer)
          |    enc | senc | aenc | sign
```

    Algebra extensions are declared using the lang key in the protocol’s association list, at
the end of a protocol. For the certificate body example,
```scheme
      (defprotocol cert basic
        ...
        (lang (cert-body (tuple 3))))
```
adds one tupling operation so that the example above can be written as
      (cert-body dn serial-no pub-key)
cpsa represents this form internally as a sequence of messages with a distinguished mark.
This representation is more efficient as compared with the tagged concatenation representation
.
    The syntax of a lang declaration is given in Table 4.1. There are eight kinds of ways
that cpsa algebras can be extended.

   • An atomic sort is added to the algebra when a symbol is declared to be of kind
     atom. If dollar is declared to be an atomic sort, then (price dollar) in a var form
     declares price to be of sort dollar.

   • An atomic sort is also added to the algebra when a symbol is declared to be of kind
     akey. However, in addition to adding the sort, cpsa adds the equation (x−1 )−1 = x
     for variables of the new sort.

   • A unary operation is added to the algebra when a symbol is declared to be of kind
     hash. As with the default hash operation, the adversary cannot extract the contents
     of the hash.

   • An n-ary operation is added to the algebra when a symbol is declared to be of kind
     (tuple n). As with concatenation, the adversary can construct and extract contents
     of tuples. Constraint: n > 0.

• A binary operation is added to the algebra when a symbol is declared to be of kind
  enc. As with the default encryption operation, the adversary cannot extract contents
  of the encryption without access to the inverse of the key.

• A symbol of kind senc is just like one of kind enc except that the key supplied when
  it is applied must be symmetric, that is, the sort of the key must not be asymmetric.

• A symbol of kind aenc is just like one of kind enc except that the key supplied when
  it is applied must be asymmetric, but not the inverse applied to an asymmetric key.

• A symbol of kind sign is just like one of kind enc except that the key supplied when
  it is applied must be the inverse applied to an asymmetric key.
---

> **Part II: Understanding and Guiding CPSA**

## Chapter 5: The CPSA Search Algorithm

The result of running the cpsa4shape tool is a file that contains only “shapes”, which include
all essential structures possible in executions of the protocol under the conditions input to
the analysis. Although this output contains the most important elements of the results of
an analysis, it can be useful to an analyst to examine the full result.
    Consider analyzing a protocol that has a secrecy property you wish to guarantee. After
modeling the protocol, you model a set of conditions under which you expect the secrecy
property to hold, but you include a listener that would invalidate it. See Section 3.5 for an
instance of the use of this technique.
    Suppose the analysis confirms the secrecy property. This would mean that there are no
shapes at all, because any shape would represent a possible way in which the conditions
were present but the secret is revealed. If you look only at the shapes file, you will see
nothing other than the fact that no shapes are present. The full analysis, however, can
be used to understand the space of attacks that were explored, which gives a much clearer
sense of why the analysis resulted in no shapes.
    It is a complicated and somewhat unnatural process modeling a protocol and setting up
the conditions for an analysis. Human error is possible, and when a human error occurs, it
is difficult for the analyst—most likely, the human that made the error in the first place—to
distinguish a human error from a correct analysis result.
    By examining the full analysis carefully, the analyst may discover errors of two types:
segments of the analysis that seem inconsistent with the intended scenario, or the lack of
analysis that the user expected to be present. The first circumstance indicates an analysis
that was under-constrained, while the latter indicates one that was over-constrained. In
order to detect errors of the second type, however, the analyst needs to understand the
search algorithm.
    Another reason to understand the search algorithm is when the user has obtained an
analysis that describes a genuine attack against a protocol. By stepping through the path
in the analysis that led to the shape in question, a user may gain an understanding of what

features of the protocol allowed this attack to take place. This often leads to insights about
how to repair the protocol and eliminate the attack.

### 5.1 Solving tests

A realized skeleton is one in which every reception is explainable given the assumed re-strictions
 on the attacker. The attacker is capable of producing every basic value (that is,
every possible value of the basic sorts data, text, name, akey, skey, and rndx), except
for those specifically withheld from the adversary. The values withheld are the ones for
which there is one of the following declarations present: uniq-orig, uniq-gen, non-orig,
or pen-non-orig (see Section 6.2 for detail).
     In addition, the attacker observes all of the transmissions made in a skeleton. The
attacker is also capable of manipulating messages in certain specific ways—these are the
derivations present in Table 10.2.
     When a reception message can be constructed by the attacker from the basic values
accessible to the attacker and the transmissions that occur prior to that reception, we say
it is realized, meaning that this reception can be explained.
     When a skeleton to be analyzed contains at least one unrealized node, one of these
nodes is selected as the “test node”, and the subsequent skeletons are determined based on
four distinct strategies for resolving (or at least making progress at resolving) the problem
at the test node. The strategies focus on a critical term, a sub-value of the reception value
that is a specific problem for derivability. The critical term may be a freshly generated
value, which was generated by a regular participant but is subsequently found in a different
message context than any in which it is known to have been transmitted. It may also be
an encrypted (or digitally signed) unit, which must be generated on some regular strand
unless the generating key is compromised. This inference builds in the assumption that
cryptographic operators have an authentication value, as a symmetric encryption may be an
authenticated encryption. cpsa always interprets an encryption operator as guaranteeing
authenticity, unless the key is compromised.
     Only certain kinds of sub-values may be of interest as critical terms, specifically, those
which are carried . The notion of a carried sub-term can be defined recursively: a term
carries itself, a pair carries either of its components, and an encryption carries its plaintext.
     The four strategies are:

   • A regular augmentation, which assumes the presence of an additional transmission
     carrying the critical term, in an entirely new strand,
   • A displacement, which assumes the presence of an additional transmission carrying
     the critical term, but in an already existing strand,
   • A contraction, which assumes that the critical issue can be resolved with some more
     refined version of the current transmissions that carry the critical value, and

   • A listener augmentation, which assumes that some key not known to be derivable is
     in fact derivable.

    When examining a skeleton and one of its children in a full cpsa analysis it is often
simple to determine which sort of strategy was used. If a child has one more strand than its
parent then it was produced by either augmentation (if the extra strand is a role instance)
or listener augmentation (if the extra strand is a listener). If a child has the same number
of strands but additional nodes, it is the result of a displacement. When a child has the
same number of nodes and strands, it may be the result of a displacement or a contraction,
but either way the only thing that has changed is a map of terms.

### 5.2 Flawed Kerberos, revisited

In Section 4.1, we worked through an example—a flawed version of the Kerberos protocol.
The first attempt at modeling the protocol was flawed in a way that would prevent the tool
from discovering the attack against the protocol.
    See Figure 4.1 for the flawed model of the protocol. Recall that the initiator is a, the
server is s, and the responder is b. See Figure 4.4 for the corrected model; the difference
is that in the corrected version, the initiator uses a variable of sort mesg to represent the
ticket the initiator receives, since the initiator is not able to check the internal format of
the ticket.

#### 5.2.1 The operation field

Examining the full cpsa analysis is essential to detecting the mistake. Each skeleton has
an operation field describing how it was derived from its parent, with one exception: when
the input skeleton does not meet all the requirements for a skeleton, the first child will be
the minimal skeleton incorporating the input.
    In kerb.xhtml, tree 0 is the flawed model. Item 0 is the input point of view and Item
1 is the completion of that input into a skeleton; notice that the skeleton below Item 1 has
no S-expression of the form (operation ...) in it.
    Item 2 is a child of Item 1 that adds a key server instance. This was a regular augmentation
, because a new protocol role instance was added. The operation field will include
added-strand whenever the skeleton was produced by regular augmentation. The full
operation field in Item 2 is:

               (operation encryption-test (added-strand keyserv 2)
                                (enc k n (ltk a s)) (0 1))

   The first argument to the operation field is the general type of operation performed.
Typically this will be one of the following four possibilities:

       • encryption-test indicates that the critical term at the test node was an encryption.

       • nonce-test indicates that the critical term at the test node was an atom, not an
         encryption.

       • channel-test indicates that the critical term at the test node was an authenticated
         channel message.

       • generalization indicates that the skeleton was realized and the tool is trying to
         make it more general without making it unrealized.

    The second argument describes the operation; here, the operation is added-strand
(regular augmentation), where the new instance is an instance of keyserv and is of length
2. The third argument is the criticial term; here it was (enc k n (ltk a s)), the portion
of the server’s message intended for the initiator. The last argument is a node, normally
the test node, so in this case, the (0 1) refers to strand 0, node 1—the second node of the
initiator strand in Item 1.
    Returning to our example, Item 2’s critical term is the encryption {|k, n|}SK(a,s) . The
regular augmentation creates a new transmission of that encryption in some carried form;
in this case, it is a transmission by the key server. Note that the key server instance in
Item 2 agrees with the initiator on a but not on b.
    See Figure 5.1 for Item 3 in the analysis. It is this step at which the analyst should
notice there was a mistake of some sort. If the analyst is trying to understand why it should
be impossible for the secret m to leak, thus far the reasoning is that if the initiator proceeds
to its third event, there is a key server that agreed with the initiator on a, s, and n. But
since the second initiator node is red, this indicates there is still something unexplained in
the execution.
    The operation field of Item 3 is telling:

                 (operation encryption-test (displaced 3 2 keyserv 2)
                               (enc k a b-0 (ltk b-0 s)) (0 1))

    The critical term here is the encryption {|k, a, b0|}K(b0,s) . Thus, the ticket portion of the
initiator’s reception is driving this step in the analysis.1 After the displacement (which,
you may notice, adds no new nodes), the key server agrees with the initiator on b.
    In other words, the tool reasons first that the presence of the “authenticator” portion
of the reception guarantees there is a key server instance that believes it is responding to
a request initiated by a, but may or may not believe the request initiated by a was for
communicating with b. The ticket portion makes the guarantee, but that’s strange because

the ticket is for b and not a to examine. To believe this reasoning implies that the initiator
really is checking the format of the ticket, which the analyst should realize is not the way
the protocol is intended to work.

     Note that the specific encryption {|k, a, b0|}K(b0,s) is not actually present in Item 2 or in Item 3, it is
a side effect of the internal way cpsa represents variables and determines how to display them. Still, only
the ticket portion of the node (0 1) is of this kind of format, so the conclusion in the text is correct.
**Figure 5.1: Flawed Kerberos key moment in analysis**

    If you next examine the properly modeled protocol, you will find that Items 5, 6, and
7 follow a very similar path. Item 6 makes Item 5 into a skeleton, while Item 7 adds a key
server instance in which the key server agrees with the initiator on a but not on b. But
Item 7 is a realized skeleton, while Item 2 is not realized.

## Chapter 6: Constraining CPSA's Search

If you have read Chapters 3 and 4, you have seen the uniq-orig and non-orig features,
which are the first representatives of a large class of features called declarations. These
“declare” certain assumed properties about an execution in order to constrain the tool’s
search. In this chapter, we will describe more precisely the notion of execution that motivates
 the cpsa analysis, and precisely define these and other declarations available for use
in the tool.

### 6.1 Bundles: A Strand-Based Execution Model
The cpsa tool is based on strand space theory [2]. A strand is simply a sequence of events,
which are transmissions or receptions of messages.
    A bundle is a set of strands, along with a satisfaction relation → from transmissions to
receptions, where for every reception event e1 of a message m, there is a unique transmission
event e0 of m such that e0 → e1 , and such that the graph formed on the events of the strands
with edges defined by → and strand succession is acyclic.
    Bundles express an explanatory framework in which a set of sequential viewpoints of
transmissions and receptions is self-contained. Although bundles do not totally order the
events, they express the orderings that are essential due to causality.
    The most basic notion of a protocol is simply a set of roles which are each themselves
strands representing a template of behavior. A bundle is a bundle of a protocol P if
every strand in the bundle is either an instance of a role in P or an instance of a penetrator
 role. There are two types of penetrator roles: derivation roles and the “create”
role. The derivation roles are determined by the message model; one matches each derivability
 rule in the algebra used. The create role consists of a one-event strand in which
certain basic values may be transmitted. This always includes all constants (such as tag
constants or the Diffie-Hellman generator g), and also includes all values of basic sorts:
data, text, name, skey, akey, rndx.

### 6.2 Secrecy assumptions

A priori, the analysis of (say) the initiator’s point of view in Needham-Schroeder is tasked
with exploring all bundles of the Needham-Schroeder protocol in which an initiator instance
of sufficient length is included. As it turns out, there is a most general shape, namely, the
full-length initiator instance, alone. However, the bundle this shape describes is not of great
interest, because the nonce chosen by the initiator appears in a “create” instance.
    An assumption of secrecy is, in essence, a statement that the analyst is interested only
in certain bundles. In the case of this nonce, for instance, we assume the nonce is secret
and are thus uninterested in bundles in which that nonce appears in a “create” instance.
    There are four declarations that may be used in cpsa to represent a secrecy assumption,
but these assumptions are distinct from each other and each have a particular semantic and
syntactic meaning.
    To describe these assumptions, we first need some terminology. We use “carried” to refer
to subterms of a term that can potentially be obtained from that term via decomposition.
A pair carries each of its elements, and an encryption carries its plaintext. We extend this
notion transitively, so for instance {|n1, n2|}K(a) carries n1 since it carries the plaintext
(n1, n2) which in turn carries n1.
    We say that a value originates on a strand when its first carried occurrence is in a
transmission. We say that a value generates on a strand when its first occurrence (whether
carried or not) in that strand is in a transmission.

   • A value uniquely originates in a bundle if it originates on exactly one strand. Note
     that if the unique origination point of a value is on a regular strand, then it cannot
     be produced in a “create” instance because that would constitute a second point of
     origination.

   • A value is non-originating in a bundle if it does not originate on any strands. A
     simple lemma can show that a value is non-originating only if it is not carried in any
     message in the bundle.

   • A value is penetrator non-originating in a bundle of a protocol if it does not originate
     on any penetrator strands. Clearly, such a value cannot be produced in a “create”
     instance.

    The presence of a uniq-orig, non-orig, or pen-non-orig declaration of a value is a
statement by the user that they are only interested in bundles in which the declared value
uniquely originates, is non-originating, or is penetrator non-originating, respectively.
    The fourth declaration that imposes a secrecy assumption is the uniq-gen declaration.
The presence of a uniq-gen declaration of a value equates to a restriction to bundles in
which the declared value generates on only one strand. Note that if a value that generates
uniquely generates on a regular strand, it cannot be produced in a “create” instance.

    The uniq-orig (resp. uniq-gen) declaration can only be used in cpsa input for values
that do originate (resp. generate) on the role or in the skeleton in which the declaration
appears. This forces the use of such declarations to create a secrecy assumption.
    Because “generation” covers a wider set of occurrences than “origination,” a value that
originates uniquely on one strand may still generate on a different strand. For instance,
it may be used to encrypt a message on that strand. This means that one can model a
key (for instance) that is distributed from a point of unique origination, and subsequently
used to encrypt messages on other strands, without modeling a particular mechanism for
storing it in the recipient’s device. This property of origination and generation can, however,
cause surprises if the key could surface unexpectedly in other strands. See Chapter 8 to
understand how to store values explicitly, when that is desired.
**Exploration 6.1.** Experiment with variants of your favorite simple protocol in which you
try replacing uniq-orig with uniq-gen and/or non-orig with pen-non-orig. What do
you find?
**Exploration 6.2.** Suppose a protocol you wish to model involves key management, and
includes keys being encrypted and transmitted and received in encrypted form. What
declaration should you use to model a long-term (not recently chosen) key as secret, if you
are concerned about the actual possibility of that key leaking?
    Note: these four declarations (uniq-orig, non-orig, pen-non-orig, and uniq-gen)
may only be applied to basic values. One of the main purposes of such declarations is to
restrict the use of the “create” role in bundles, so such declarations on values that cannot
be produced in the “create” role is undesirable.

### 6.3 Diffie-Hellman declarations

A declaration arises as a part of the algorithm cpsa uses for Diffie-Hellman protocols. Like
other declarations, these may be provided as part of a protocol or skeleton input.

   • The absent declaration specifies that a particular rndx variable does not occur in an
     exponent expression. This declaration is automatically added to specify x is absent
     within y whenever y is an exponent expression that occurs in a strand in which x
     is declared uniq-gen before the point where x is generated. This declaration is also
     added by the algorithm in rare circumstances.

### 6.4 Declaring skeletons

To ask cpsa a query, one uses a defskeleton form. The detailed syntax definition is
in Table 10.1. We give here a summary of the core elements and how to use them. A
defskeleton form such as those in Figs. 3.3–3.4 has the form

```scheme
                                 (defskeleton prot-name
                                   (vars ...)
                                   strand-decls ...
                                   assumptions ...
                                   comments)
```
prot-name is the name of the protocol. The (vars ...) give the names and sorts of the
values appearing in the resulting skeleton, for instance values that may be parameters of one
or more role instances in the skeleton, and may appear in the assumptions. The assumptions
include unique origination and non-origination claims, as well as channel properties and
state annotations (Chapter 8) and facts (Section 7.7.1). Comments are for the convenience
of the specifier. The strand-decls consist of one or more forms

   • (defstrand role height bindings) for an instance of role of the given height,

   • (defstrandmax role bindings) to indicate an instance of role of its full maximum
     height, or

   • (deflistener t) to indicate that the term t is heard transmitted publicly.

Generally, a defskeleton q containing a (deflistener t) declaration is used to see
whether the term t remains confidential in the situation described by the remainder q ′
of the defskeleton. If cpsa determines that there are no shapes for this query, then there
is no extension of q ′ in which the participants emit messages allowing the adversary to
extract t. Typically, this is what the specifier intends to find: These are non-disclosure
queries.
    A defskeleton form most frequently contains a single defstrand or defstrandmax, in
which case cpsa will determine what other behaviors this participant can rely on having
occurred when a run of this role takes this number of steps. Thus, it determines what is
learnt from the point of view of this participant. These are authentication queries from that
participant’s point of view.
    When a single-strand authentication query gives some information about other local
sessions, but we would like also to know whether additional conclusions follow if we assume
unique origination or non-origination for values in those local sessions, then we would use
multiple defstrands.
    The bindings (aka “maplets”) in a strand declaration are pairs (p v) where p is a
parameter of the role being declared and v is a value defined from the variables declared for
this skeleton. Most often v just is one of these variables. These bindings can be confusing,
since the role parameter and the variable in the skeleton may have the same name, so we have
a binding (b b) or (n1 n1), as in Fig. 3.3. However, the two bs are different: The first is
the parameter declared in the init role in Fig. 3.2, while the second is the skeleton variable
declared in the variable form (vars (b name) (n1 text)). A binding must appear in the
strand declaration only if we need to assert something about it. In Fig. 3.3, those two

bindings appear because the skeleton variable n1 is assumed uniquely originating, and b
appears because (privk b) is assumed non-originating. Any other parameters may be
omitted, in which case cpsa supplies an unconstrained value for it.

### 6.5 A Caution about typos

Declarations are typically found syntactically in “association lists” which include declarations
 and may also include other fields, whether in protocol declarations, role declarations
within them, or in skeleton query declarations. For instance, the cpsa tool creates associations
 in its defskeleton outputs specifying things like the algorithmic method used to
produce this skeleton, or the label of the parent, etc. cpsa handles comments in the same
way. Any association list entry (header . . . stuff . . . ) in which the header is unrecognized
is treated as a comment, and preserved in the output. This is convenient not just for documenting
 your specifications, but also for defining material to be used not by cpsa itself
but by downstream tools.
    Be careful when using declarations that you do not mis-spell the keywords! If you do,
they will typically be treated just like a comment and ignored, so they will not have the
effect you intended.
---

> **Part III: Advanced features of CPSA**

## Chapter 7: Logical Security Goals and Rules

How easy is it to read off authentication and secrecy properties? What precisely is it that an
expert sees? This chapter describes cpsa’s support for reasoning about security goals using
first-order logic. With security goals expressed in first-order logic, intuition is replaced by
determining if a formula is true in all executions of the protocol.
     This treatment of security goals relies heavily on a branch of first-order logic called
model theory. It deals with the relationship between descriptions in first-order languages
and the structures that satisfy these descriptions. In our case, the structures are skeletons
that denote a collection of executions of a protocol. This chapter describes the language of
security goals and its structures without requiring the reader to have studied model theory.
     The model theoretical foundation of this approach to security goals appears in [6]. A
practical use of security goals in protocol standardization is described in [8, 14]. The precise
semantics of the goal language is in [13]. The syntax of security goals appears in Table 7.1.
     The cpsa distribution contains, in its examples directory, the input file goals.scm.
The reader is encouraged to run the examples and examine the output while reading this
chapter.
     In this chapter we return to the Needham-Schroeder protocol discussed in Chapter 3.
The roles are displayed in Figure 3.2.
     The protocol is analyzed from the point of view of a complete run of one instance of the
initiator role. The input security goal, followed by the point of view skeleton it generates
and the shape produced by cpsa, are shown in Figure 7.1. The syntax and semantics of the
goal will be explained later. Roughly speaking, it asserts that if a realized skeleton contains
a full length initiator strand, its private key is uncompromised, and it uniquely generates
n1, then the skeleton will contain a responder strand that agrees with the initiator on the
name b. The shape produced by cpsa contains the annotation (satisfies yes). This
indicates that its structure satisfies the description given by the security goal. It will be
explained later why the properties of cpsa allows us to conclude that this goal is true in
all executions of the protocol, and therefore conclude that the Needham-Schroeder protocol

**Table 7.1: Goal syntax. See Tables 10.3 and 10.5 for the algebra syntax, which defines the term and sort symbols.**

```text
               goal     ←    (defgoal id sentence+ alist)
          sentence      ←    (forall (gvdecl∗) implication)
            gvdecl      ←    (id+ sort) | (id+ strd) | (id+ indx)
              vmap      ←    (id id)
        implication     ←    (implies conjunction conclusion)
       conjunction      ←    conjunct | (and conjunct+)

achieves this authentication goal.

          conjunct      ←    atomic | (strand id strdvar integer (vmap∗))
                        |    (listener strdvar id)
         conclusion     ←    (false) | existential
                        |    (or existential+)
        existential     ←    conjunction | (exists (gvdecl∗) conjunction)
             atomic     ←    (p string strdvar integer)
                        |    (p string string strdvar term)
                        |    (prec strdvar index strdvar index)
                        |    (leads-to strdvar index strdvar index)
                        |    (non term) | (pnon term)
                        |    (uniq term) | (uniq-at term strdvar index)
                        |    (ugen term) | (ugen-at term strdvar index)
                        |    (conf term) | (auth term)
                        |    (= strdvar strdvar) | (= term term)
                        |    (gen-st term) | (trans strdvar index)
                        |    (comm-pr strdvar index strdvar index)
                        |    (state-node strdvar index)
                        |    (same-locn strdvar index strdvar index)
                        |    (component term term) | (fact id term*)
            strdvar     ←    symbol
              index     ←    symbol | integer
```

```scheme
(defgoal ns                ; Goal
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and (p "init" z0 3)
      (p "init" "n1" z0 n1) (p "init" "b" z0 b)
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
      (and (p "resp" z1 2) (p "resp" "b" z1 b))))))
```

```scheme
(defskeleton ns            ; Point of view skeleton
  (vars (a b name) (n1 n2 text))
  (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2))
  (non-orig (privk b))
  (uniq-orig n1))
```

        {|N1 , A|}KB                    {|N1 , A|}KB
init                         ≺                           resp
       {|N1 , N2 |}KA                  {|N1 , N2′ |}KA
 •                           ≻                            •
         {|N2 |}KB
 •
```scheme
(defskeleton ns            ; Shape
  (vars (n1 n2 text) (a b name))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))
  (defstrand resp 2 (n2 n2-0) (n1 n1) (b b) (a a))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (non-orig (privk b))
  (uniq-orig n1)
  (satisfies yes))
```
**Figure 7.1: Needham-Schroeder Initiator Point of View**

### 7.1 Overview

In addition to defskeleton S-expressions, a cpsa input file may contain defgoal S-expressions
. Like a defskeleton, a defgoal takes as its first parameter the name of a
protocol which the tool expects has been previously defined in the input file. The second
parameter to a defgoal is a geometric sentence in first-order logic. A geometric sentence
contains one implication. The antecedent is a conjunction of atomic formulas. The free
variables that occur in the antecedent are universally quantified. The conclusion is a disjunction
 of existentially quantified conjunctions of atomic formulas.
    When the tool is run, a defgoal is converted to a defskeleton that represents as
narrowly as possible the left-hand side of the implication and has a goal recorded for the
right-hand side. The tool then analyzes defskeletons as usual, but realized skeletons
found during the course of analysis of a defskeleton with a goal are augmented with a
satisfies S-expression indicating whether the goal is met or not.
    The tool cpsa4goalsat will examine the output from a cpsa run, and, for each goal
formula, will determine whether the analysis ensures that the goal is met. If not, it identifies
the labels of all the skeletons that furnish counterexamples to the goal. See Section 11.
    The remainder of this chapter is devoted to explaining the semantics of this feature in
greater detail.

### 7.2 Semantics

In a defgoal sentence, the antecedent specifies the point of view skeleton. We focus on the
antecedent. In the example,

      (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2))

is extracted from

      (and (p "init" z0 3)
        (p "init" "n1" z0 n1) (p "init" "b" z0 b)).

Notice that cpsa adds a binding for a and n2 just as it does had

      (defstrand init 3 (b b) (n1 n1))

been given as input.
    Our aim now is to specify how to decide if a security goal is true in all possible executions
of a protocol. A skeleton defines a set of executions that contain the skeleton’s structure.
We say a skeleton satisfies a formula if the skeleton contains all of the structure specified

by the formula. To decide if a skeleton satisfies a formula, we decide if it satisfies each of
its atomic formulas, and combine the results using the rules of first-order logic.
    Atomic formula (p "init" z0 3) is called a role strand length formula. A skeleton k
satisfies the formula if z0 maps to a strand s in k such that
  1. the trace of strand s in k has a length greater than 2, and

  2. the trace when truncated to length 3 is an instance of the init role.
Consider the shape in Figure 7.1. It satisfies (p "init" z0 3) when z0 maps to 0.
    Atomic formula (p "init" "n1" z0 n1) is called a role parameter formula. A skeleton
 k satisfies the formula if z0 maps to strand s in k, n1 first occurs in at position i in the
trace of the init role, and n1 maps to a message algebra term t in k such that
  1. the trace of strand s in k has a length greater than i,

  2. the trace truncated to length i + 1 is an instance of the init role, and

  3. the truncated trace is compatible with mapping the init role’s "n1" role variable to t.
The shape in Figure 7.1 satisfies (p "init" "n1" z0 n1) when z0 maps to 0 and n1 maps
to the message algebra term n1.
    Collectively, a skeleton satisfies the formula
      (and (p "init" z0 3)
           (p "init" "a" z0 a) (p "init" "b" z0 b)
           (p "init" "n1" z0 n1) (p "init" "n2" z0 n2))
if the skeleton contains the structure specified by
      (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2)).
   The antecedent in Figure 7.1 contains two origination assertions. The formula (non
(privk b)) is extracted as (non-orig (privk b)). A skeleton k satisfies the formula if b
maps to a message algebra term t in k such that k assumes that t is non-originating. The
unique origination formula for n1 is similarly extracted.
   Putting it all together, the mapping

                         {n1 7→ n1, n2 7→ n2, a 7→ a, b 7→ b, z0 7→ 0}

shows that the shape in Figure 7.1 satisfies the antecedent of the security goal.
    The prec predicate is used to assert a node precedes another node. The conclusion
in Figure 7.1 with (prec z1 2 z0 2) added is satisfied by the shape using the mapping
z0 7→ 0 and z1 7→ 1.
    The uniq-at predicate is used to assert not only that an atom uniquely originates, but
also the node at which it originates. In the Figure 7.1 goal, the (uniq n1) formula could

have been replaced by (uniq-at n1 z0 0). The extracted point of view skeleton is the
same.
    The ugen and ugen-at predicates are similar, except that they refer to an earliest
outbound occurrence, whether carried or not. If an atom is an asymmetric key, it and its
inverse are generated together at the first outbound occurrence of either one.
    Predicates conf and auth hold true of channels, when those channels are assumed to
be confidential or authenticated channels as described in Chapter 8. The gen-st predicate
holds true of a message value that cannot be an unexplained value in a state location, but
can only be the result of a transition caused by a regular role (Section 8.2). The leads-to
predicate relates a pair of nodes when the former creates a state value in a location, and
the latter reads it from that location with no intervening transitions (Section 8.2). The
comm-pr, comm-pr, and state-node predicates are used mainly internally to cpsa.
    Recall that our aim in analyzing a protocol is to find out what security goals are true
in all of its possible executions. When every shape of a cpsa run satisfies the goal specified
in a defgoal query, then that goal is satisfied in every execution.
    When cpsa performs a shape analysis, every shape it generates refines the input skeleton
. Skeleton refinement is defined in Chapter 5. The definition makes precise the notion
of structure containment, as skeleton A refines skeleton B if and only if A contains the
structure of skeleton B.
    The skeleton k0 extracted from the antecedent of a security goal has the property that
a skeleton refines k0 if and only if it satisfies the antecedent. A skeleton with this property
is called the characteristic skeleton of the antecedent.
    Given a goal Φ, consider a shape analysis starting from the characteristic skeleton k0 of
its antecedent. Assume cpsa finds shapes k1 , . . . , kn and that cpsa determines that each ki
satisfies Φ. Consider the executions that contain the structure in k0 . cpsa tells us that
each execution is in the executions that contain the structure of some ki . Furthermore,
because k0 is a characteristic skeleton, each ki satisfies the antecedent of Φ. Executions
that do not contain the structure in k0 do not satisfy the antecedent. Therefore, Φ is true
in all executions of the protocol and maximally informative.

### 7.3 Examples

This section contains examples of both authentication and secrecy goals. The first example
shows the feedback the user receives when a shape does not satisfy a security goal. The
second example shows how to use a listener to state a secrecy goal.

#### 7.3.1 Needham-Schroeder Responder

Figure 7.2 contains an analysis of Needham-Schroeder from the point of view of a complete
run of the responder under the assumption that the responder’s private key is uncompromised
 and the nonce it generates uniquely originates.

```scheme
(defgoal ns                ; Goal
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
      (and (p "resp" z0 3) (p "resp" "n2" z0 n2)
        (p "resp" "a" z0 a) (p "resp" "b" z0 b)
        (non (privk a)) (uniq n2))
      (exists ((z1 strd))
        (and (p "init" z1 2) (p "init" "b" z1 b))))))
```

```scheme
(defskeleton ns            ; Point of view skeleton
  (vars (a b name) (n1 n2 text))
  (defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2))
  (non-orig (privk a))
  (uniq-orig n2))
```

                    {|N1 , A|}KB                   {|N1 , A|}KB′
          resp                                                     init
                    {|N1 , N2 |}KA                {|N1 , N2 |}KA
           •                            ≺                              •
                      {|N2 |}KB                     {|N2 |}KB′
           •                            ≻                              •

```scheme
(defskeleton ns            ; Shape
  (vars (n1 n2 text) (a b b-0 name))
  (defstrand resp 3 (n2 n2) (n1 n1) (b b) (a a))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b-0))
  (precedes ((0 1) (1 1)) ((1 2) (0 2)))
  (non-orig (privk a))
  (uniq-orig n2)
  (satisfies (no (a a) (b b) (n2 n2) (z0 0))))
```
**Figure 7.2: Needham-Schroeder Responder Point of View**

   The conclusion of the goal asserts that in an execution compatible with the point of
view, there must be an initiator strand that agrees with the responder strand on the name
b. The shape produced by cpsa is a counterexample to this assertion. Because of this,
cpsa annotates the shape with
     (satisfies (no (a a) (b b) (n2 n2) (z0 0))).
The annotation includes a variable mapping for the shape that satisfies the antecedent of
the goal but does not satisfy its conclusion. The reason the shape does not satisfy the goal
is because the mapping (b b) maps the initiator’s b parameter to b, not b-0 as is required
to model the shape.
    Gavin Lowe identified this authentication failure in Needham-Schroeder and provided a
fix. In the Needham-Schroeder-Lowe Protocol, the name b is included within the encryption
in second message of both roles. With this modification, the shape found by cpsa satisfies
the security goal in Figure 7.2, so Needham-Schroeder-Lowe achieves this authentication
goal.

#### 7.3.2 A Needham-Schroeder Secrecy Goal

```scheme
     (defgoal ns
       (forall ((a b name) (n1 text) (z0 z1 strd))
         (implies
           (and (p "init" z0 3) (p "init" "n1" z0 n1)
             (p "init" "a" z0 a) (p "init" "b" z0 b)
             (p "" z1 1) (p "" "x" z1 n1) ; Listener
             (non (privk a)) (non (privk b))
             (uniq n1))
           (false))))
```
**Figure 7.3: Needham-Schroeder Secrecy Goal**

Figure 7.3 contains a goal of Needham-Schroeder from the point of view of a complete
run of the initiator under the assumption that the responder’s and its peer’s private keys
are uncompromised and the nonce n1 it generates uniquely originates. Furthermore, the
antecedent of the goal assumes that the nonce is leaked using a listener (represented by the
empty string "").
     (p "" z1 1) (p "" "x" z1 n1)           ; Listener
The conclusion of the goal is false, a predicate that is satisfied by no executions. Essentially
, this goal is saying that any shape found by the analysis is evidence that the nonce
can leak, and therefore a counterexample to the secrecy goal. This is because any shape
found will satisfy the antecedent, but not the conclusion of this goal. In this case, cpsa
finds no shapes, so Needham-Schroeder achieves this secrecy goal and does not leak n1.

### 7.4 The Rest of the Story

The examples in the previous section demonstrate the typical way security goals are analyzed
 with cpsa. However, there are more features that may be useful.
    A defgoal form may contain more than one sentence. See Figure 7.4 for an example.
When presented with more than one sentence, cpsa extracts the point of view skeleton

```scheme
      (defgoal ns
        (forall ((a b name) (n text) (z0 strd))
          (implies
            (and (p "init" z0 2) (p "init" "n1" z0 n)
              (p "init" "a" z0 a) (p "init" "b" z0 b)
              (non (privk a)) (non (privk b)) (uniq n))
            (exists ((z1 strd))
              (and (p "resp" z1 2) (p "resp" "b" z1 b)))))
        (forall ((a b name) (n text) (z0 strd))
          (implies
            (and (p "init" z0 2) (p "init" "n1" z0 n)
              (p "init" "a" z0 a) (p "init" "b" z0 b)
              (non (privk a)) (non (privk b)) (uniq n))
            (exists ((z1 strd))
              (and (p "resp" z1 2) (p "resp" "a" z1 a))))))
```
**Figure 7.4: Two Initiator Authentication Goals**

from the first sentence.
    It is wise to ensure that the antecedent in every sentence is identical. When cpsa
performs satisfaction-checking on sentence Φ, it only determines if each shape satisfies Φ.
If the point of view skeleton is not the characteristic skeleton of the antecedent of Φ, the
fact that all skeletons satisfy Φ cannot be used to conclude that Φ is true in all executions
of the protocol.
    cpsa performs satisfaction-checking when an input skeleton in annotated with one or
more security goals. The annotation uses the goals key.

```scheme
      (defskeleton
         ...
         (goals sent+))
```

   The program cpsa4sas, discussed in the next section, can be used to generate a formula
 with an antecedent such that the input skeleton is the characteristic skeleton of the
antecedent.

### 7.5 Syntactic Abbreviations

Section 7.2 described how cpsa extracts
      (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2))
from the following conjunction of facts
      (and (p "init" z0 3)
        (p "init" "n1" z0 n1) (p "init" "b" z0 b)).
    Using a conjunction of facts to represent a single defstrand is convenient for defining
and implementing a clear semantics, however it can be quite cumbersome and error prone
to specify these conjunctions. We therefore also provide support for syntactic sugar in the
goal language to allow users to represent these conjunctions in a manner much closer to the
defstrand form found in a skeleton. In particular, the user can write
      (strand init z0 3 (n1 n1) (b b))
as a single conjunct in a formula, and cpsa will ingest it with the same interpretation as if
the user had entered
      (and (p "init" z0 3)
        (p "init" "n1" z0 n1) (p "init" "b" z0 b)).
   Thus the goal in Fig. 7.1 could therefore be written as follows instead:
```scheme
      (defgoal ns
        (forall ((b name) (n1 text) (z0 strd))
          (implies
           (and (strand init z0 3 (n1 n1) (b b))
            (non (privk b)) (uniq n1))
           (exists ((z1 strd))
            (strand resp z1 2 (b b)))))).
    This representation has the benefit of being syntactically quite close to the skeleton
```
representation, and therefore the connection is more visually obvious to the user. Notice
the crucial difference that the (strand ...) form includes a strand variable after the name
of the role. While such a variable is not needed for skeletons, it is required in formulas to
allow other facts to reference the strand it represents.
    We also provide a similar abbreviation for listener strands. Instead of writing
      (and (p "" z0 1) (p "" "x" z0 n1))
we can write the following instead
      (listener z0 n1).
    These abbreviations can be used both in goals and in rules (described below in Section
 7.7).

### 7.6 Shape Analysis Sentences

A shape analysis sentence expresses all that can be learned from a run of cpsa as a security
goal. If a security goal can be derived from a shape analysis sentence, then the protocol
achieves the security goal, that is, the goal is true in all executions of the protocol.
   The program cpsa4sas extracts shape analysis sentences from the output of cpsa.
Consider the first example in this paper (Figure 7.1), which is in the sample file goals.scm.

```scheme
(defgoal ns
  (forall ((n1 n2 text) (b a name) (z strd))
    (implies
      (and (p "init" z 3) (p "init" "n1" z n1)
        (p "init" "n2" z n2) (p "init" "a" z a)
        (p "init" "b" z b) (non (privk b)) (uniq-at n1 z 0))
      (exists ((n2-0 text) (z-0 strd))
        (and (p "resp" z-0 2) (p "resp" "n2" z-0 n2-0)
          (p "resp" "n1" z-0 n1) (p "resp" "b" z-0 b)
          (p "resp" "a" z-0 a) (prec z 0 z-0 0)
          (prec z-0 1 z 1))))))
```
**Figure 7.5: Initiator Shape Analysis Sentence**

To generate a maximally informative security goal from the initiator point of view with
ghci and Make.hs, type

      $ ghci Make.hs
      *Make> sas "goals"

When using GNU make, type “make goals_sas.text”. The resulting shape analysis sentence
 is displayed in Figure 7.5.
    A shape analysis sentences asserts that either a realized skeleton does not satisfy its
antecedent or it satisfies one or more of the disjuncts in its conclusion. cpsa has been
designed so that this assertion is true. Therefore, every shape analysis sentence is true in
all executions.
    A security goal is true in all executions if it can be derived from a shape analysis sentence
 [13]. In practice, theorem-proving using shape analysis sentences is rarely employed.
It’s clumsy and it requires too much expertise. The main use of cpsa4sas is for generating
a formula that is edited to become a desired security goal.
    In general, cpsa will not use the syntactic abbreviations of the previous section in its
output, preferring instead the fully elaborated conjunction of facts. So the shape analysis
sentences will not contain these abbreviations.

### 7.7 Rules

Each protocol includes a small collection of rules. A rule is a sentence in the goal language
presented in Table 7.1. Rules are defined after the roles of a protocol are defined. The
syntax of a rule follows.

                   rule    ←    (defrule name sentence comments)

    A rule is an axiom added to a protocol. cpsa uses the axiom as a rewrite rule to
derive zero or more new skeletons from a skeleton produced during a step. An example of
a protocol with a rule is in Figure 7.8 on page 66.
    The trust rule states that when CPSA finds a person strand of length at least one, and
the inverse of it’s p parameter is non-originating, CPSA should assume the inverse of it’s d
parameter is non-originating.

#### 7.7.1 Facts

Each skeleton includes a small database of facts. A fact is a named relation among fact
terms. A fact term is either a strand of the skeleton or an algebra term. A set of facts
is defined anywhere after strands are defined using the facts form. The syntax of facts
follows.
                              facts    ←   (facts fact∗)
                               fact    ←   (symbol fterm∗)
                             fterm     ←   mesg | nat

    For example, in a skeleton, a user may want to note that strand 0 owns the private key
for a by assuming.

                               (facts (owns 0 (privk a)))

    Facts are most useful when combined with rules. Here is an example of their combination
. Suppose a point of view skeleton has two names, a and b, and the problem is modeling
a situation in which the two names are known to differ. To enforce this constraint, add
                                    (facts (neq a b))
to the point of view skeleton. CPSA generates a default rule stating essentially that neq
can never apply to two equal terms:

      (defrule neq
        (forall ((a mesg))
          (implies
            (fact neq a a)
            (false))))

#### 7.7.2 DoorSEP

As a motivating scenario consider the Door Simple Example Protocol (DoorSEP), derived
from an expository protocol that was designed to have a weakness. Despite this, the protocol
achieves the needs of an application, given a trust assumption.

                                 person                           door
                               {|{|K|}P −1 |}D                {|{|K|}P −1 |}D
                      •                          /                              /•
         Fresh: K                 {|T |}K                        {|T |}K           Fresh: T
                      •o                                  o                     •
                                                                                
                      •
                                     T           /                  T           /•
**Figure 7.6: DoorSEP Protocol**

    Imagine a door D which is equipped with a badge reader, and a person P equipped with
a badge. When the person swipes the badge, the protocol executes. Principals such as doors
or persons are identified by the public parts of their key pairs, with D−1 and P −1 being the
corresponding private keys. We write {|M |}K for the encryption of message M with key K.
We represent digital signatures {|M |}P −1 as if they were the result of encrypting with P ’s
private key.
    P initiates the exchange by creating a fresh symmetric key K, signing it, and sending
it to the door D encrypted with the door’s public key. D extracts the symmetric key
after checking the signature, freshly generates a token T , and sends it—encrypted with the
symmetric key—back to P . P demonstrates they are authorized to enter by decrypting
the token and sending it as plaintext to the door. The two roles of DoorSEP are shown in
Fig. 7.6, where each vertical column displays the behavior of one of the roles. The cpsa
encoding of the roles is in Figure 7.8.
    cpsa finds an undesirable execution of DoorSEP. Assume the person’s private key P −1
is uncompromised and the door has received the token it sent out. Then cpsa finds that P
freshly created the symmetric key K. However, nothing ensures that the person meant
to open door D. If P ever initiates a run with a compromised door C, the adversary
can perform a man-in-the-middle attack, decrypting using the compromised key C −1 and
re-encrypting with D’s public key, as elided in the · · · in Fig. 7.7. To verify this result
with cpsa, remove the trust axiom in the doorsep protocol in examples/rules.scm and
run cpsa. Thus, without additional assumptions, the door cannot authenticate the person
requesting entry.
    But possibly we can trust the person to swipe her badge only in front of doors our
organization controls. And we can we ensure that our doors have uncompromised private
keys. If so, then the adversary cannot exercise the flaw.
    We regard this as a trust assumption, and we can express it as an axiom:

Trust Assumption 1. If an uncompromised signing key P −1 is used to prepare an instance

of the first DoorSEP message, then its owning principal has ensured that the selected door
D has an uncompromised private key.

                     person                                                 door
                               {|{|K|}P −1 |}C            {|{|K|}P −1 |}D
                        •                        / ···                      /•
                                                              {|T |}K         
                                                      o                      •
                                                                              
                                                                T           /•

                              Uncompromised: P            Fresh: K, T
**Figure 7.7: DoorSEP Weakness**

    The responsibility for ensuring the truth of this axiom may be split between P and the
organization controlling D. P makes sure to swipe her badge only at legitimate doors of
the organization’s buildings. The organization maintains a security posture that protects
the corresponding private keys.
Is DoorSEP good enough, assuming the trust axiom? Add the trust axiom back to the
doorsep protocol in doc/rules.scm and see. You should find that the protocol does its job;
namely, ensuring that the door opens only when an authorized person requests it to open.

A trick to control rules. Sometimes, one would like to explore two versions of a protocol:
One that contains a particular rule, and another that doesn’t. Some cpsa queries should
be executed with the rule in force, and others without the rule. For instance, one may want
to know which security properties hold even without the assumption made in the rule.
    To do this, one can add a sort of flag to the rule as an additional premise. For instance,
in the DoorSEP case, we could have written the rule as shown in Fig. 7.9, with the additional
premise (fact use-trust-rule).
    Now, a query that should not use the trust-sometimes rule can be stated as usual,
as in Fig. 7.8. A query that should use the rule can add the use-trust-rule fact to the
defskeleton form, as shown in Fig. 7.9. As a consequence, the additional premise will be
satisfied any time that cpsa would apply the rule.
    This also illustrates the way that a fact that is written (fact use-trust-rule) in a
goal or rule is declared (facts (use-trust-rule)) in a defskeleton form.

#### 7.7.3 Generated rules

cpsa generates certain rules either automatically in all cases or else as a consequence of
user inputs. The rules generated for a given protocol input may be found in the printed
output for that protocol; these are the formulas appearing in defgenrule forms in the .txt
and .xhtml files.

```scheme
(defprotocol doorsep basic
  (defrole person
    (vars (d p akey) (k skey) (t text))
    (trace
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t)))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t)))
  (defrule trust
    (forall ((z strd) (p d akey))
            (implies
             (and (p "person" z 1)
                  (p "person" "p" z p)
                  (p "person" "d" z d)
                  (non (invk p)))
             (non (invk d))))
    (comment "The trust rule"))
  (comment "Doorsep protocol using unnamed asymmetric keys"))
```

```scheme
(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (comment "Analyze from the doors’s perspective"))
```
**Figure 7.8: Door Simple Example Protocol**

```scheme
(defrule trust-sometimes
   (forall ((z strd) (p d akey))
           (implies
            (and (fact use-trust-rule)
                 (p "person" z 1)
                 (p "person" "p" z p)
                 (p "person" "d" z d)
                 (non (invk p)))
            (non (invk d))))
   (comment "The trust rule. Assume (fact use-trust-rule) to enable it"))
```

. . .

```scheme
(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (facts (use-trust-rule))
  (comment "Analyze from the doors perspective, with trust rule"))
```
**Figure 7.9: Rule with a flag to control its use**

Negated equalities. Since negated equalities are often needed to express assumptions
users are interested in, cpsa generates three rules with the body:

(implies (fact neq x x)
         (false))

This rule has the effect of terminating a branch of analysis if two expressions that the
user has stipulated should not be equal become unified to the same value. Three rules
are generated since the variable x may be of sort mesg, or of sort strd for a strand in the
skeleton, or of sort indx meaning the index of a node along a strand. To stipulate a negated
equality between two expressions e1 , e2 , the user may write in the input file:

```scheme
(defskeleton protocol
   . . . strand declarations, etc. . . .
   (facts (neq e1 e2 )))
```

Negated equality assertions may also appear in the conclusions of user-defined rules, or
anywhere else that an atomic formula may appear.
    A good number of additional rules are generated to implement cpsa’s model of state
(see Section 8.2, esp. Figs. 8.4–8.5 and pp. 89–90).

“Assume” declarations. A formula may be provided after the trace declaration in a
defprotocol declaration in an assume clause. For instance:1

```scheme
(defrole init
    (vars ...)
    (trace ...)
    ...
    (assume (fact neq (exp (gen) upsilon) (gen))))
```

In this case, the cpsa loader checks that all of the free variables (just upsilon here) appear
in the trace. If i is the first height at which all of the variables have occurred, cpsa
generates a rule stating that any instance of the rule of height ≥ i satisfies this property of
the instances of the role parameters. In this case, i = 4, so the generated formula states:

(defgenrule assume-init-0
    (forall ((z strd) (upsilon expt))
      (implies (and (p "init" z 4) (p "init" "upsilon" z upsilon))
        (fact neq (exp (gen) upsilon) (gen)))))

Here, the assumption is the uninterpreted predicate symbol neq applied to two expressions
. However, the assumption may also involve conjunction and existential quantifiers.
       See the file dhcr_um_expt_assume.scm in the manual examples directory.

cpsa also permits disjunctions, but these typically cause unreasonable branching and bad
performance.
   In case the assumption is a fact, such as the neq assertion above, one can write

```scheme
(defrole init
    (vars ...)
    (trace ...)
    ...
    (facts (neq (gen) (exp (gen) upsilon))))
```

instead of writing the assume annotation above. Many facts may be listed as clauses here,
with the effect of a conjunction. The keyword here is the plural facts, and the singular
fact does not appear in the individual clauses.
    The facts annotation may also appear in a defskeleton query.

```scheme
(defskeleton dhcr-um
  (vars (a b name) (beta expt))
  (defstrand init 5 (a a) (b b) (beta beta))
  (non-orig (privk "sig" b))
  (facts (neq a b) (undisclosed beta)))
```

Currently, cpsa does not recognize the assume keyword in defskeleton queries.

#### 7.7.4 Rules generated for trace annotations

cpsa now allows a few types of annotations to be interspersed within the trace declaration
within a role. These are:

rely, used after a reception to declare a formula containing only free variables appearing
      up to and including this reception. Every instance of the role long enough to include
      a successful instance of this reception must satisfy the formula;

guar, used before a transmission to declare a formula containing only free variables appearing
 up to and including the following transmission. Every instance of the role long
     enough to include an instance of the following transmission must satisfy the formula.

All of these trace annotations will cause similar rules to be generated. Trace annotations
do not add to the height of the trace. They simply express constraints on what happens in
the “real” events around them.

Expressing rely and guarantee statements. In work on trust management, and on
compiling cryptographic protocols [9, 7, 11], we introduced the idea of a rely formula that
expresses what a principal learns when a message is received, possibly assuming that certain
peers are uncompromised. We also introduced the idea of a (dual) guarantee formula that

must be true in order for a principal to transmit a message. In particular, if a message
sent by a principal A has a particular guarantee formula ϕ, and a peer B receives it and
authenticates its origin with A in this step of the protocol, then B may rely on a formula
with the meaning, A says ϕ.
    This example will be sound in the sense that the authentication property ensures that
A really did say (i.e. guarantee) ϕ in any execution in which B relies on the claim. The
soundness of rely statements may be checked by analyzing the protocol with the rely state-ments
 omitted, and querying them as goal statements under the relevant non-compromise
assumptions. We will now assume that this soundness checking has been done, and that
any relevant non-compromise assumptions are made in the protocol definition.
    Thus, a rely formula definitely holds true whenever the principal successfully completes
the preceding receive event. Indeed, the operational interpretation of a rely formula is
that the principal will add an assertion to a database of its knowledge. cpsa transforms
a rely formula after a reception which is at height i in a trace into a rule stating: “long-enough
” instances of the role will satisfy the formula, for that instance’s values of the role
parameters.
    This transformation is similar to what cpsa does for a cheq annotation, except that
instead of an equation, the conclusion may involve other atomic formulas, conjunctions,
and existential quantifiers. Disjunctions are permitted, but will usually lead to intractable
cpsa analysis.
    A guarantee formula has a dual relation with a subsequent transmission. Just as the
received message may determine the instances of parameters appearing in a rely formula,
a guarantee formula may dually select instances of parameters that will appear in the
subsequent transmission. As a rely formula is interpreted operationally as an assert to a
database held by the principal, a guarantee formula is interpreted operationally as a query
against that database. Hence, assertions caused by previous rely formulas may influence
the parameter instances selected by subsequent guarantee formulas.

A rely-guarantee example. Consider a protocol in which a customer will interact with
a merchant and a bank to purchase an item at a cost; the merchant will be paid by a debit
from the customer’s account at the bank. Each participant should obtain evidence that
the expected peers are participating in a corresponding session. Moreover, the merchant
does not need to know the customer’s account number, and therefore should not see this
information. The bank does not need to know what item the customer is buying, and
therefore should not see that. Outsiders should not see the details at all. How best to
achieve this goal?
    Each party will need to generate a digital signature, since in case of dispute a third
party must be able to reconstruct who committed to paying whom, and to sending what
merchandise. Moreover, public key encryption will be needed, at least for a handshake,
since the parties must protect secrets from the outsiders and from the third party. Thus,
there is no way to avoid having three digital signatures generated, along with a similar

number of public key encryptions, with corresponding verification and decryption actions.
A protocol that achieves this goal is found in examples/minipay.scm.
    Each party is making assertions, in effect. The customer asserts his desire to buy the
item for the cost. The bank asserts that it will transfer the funds to the merchant. The
merchant asserts that it will ship the item. Moreover, the protocol should ensure that each
party knows that the others have made these commitments. For instance, the merchant is
willing to ship the goods because it knows that the bank will transfer the payment. Thus,
each party makes a guarantee, and each party learns that it may rely on its peers having
made their guarantee. A fine point is the bank’s rely formula; it learns that the customer
has requested some item in exchange for the cost, but not which one. Thus, the item is
existentially bound in the bank’s rely formula.
    This yields the rely and guarantee formulas displayed in Fig. 7.10; the protocol with
these trust annotations may be found in examples/minipay-rely-guar.scm. The principals
 in a particular session are required not to proceed past a guarantee formula unless the
instances of the variables are known to satisfy the property claimed. The rely formulas
summarize what they have learned in the preceding reception.
    But: How do we know these formulas are in fact true in every execution that includes
the preceding reception, or at least every execution satisfying some reasonable assumptions
about uncompromised keys?
    We can use goal formulas to check this. In a separate file, examples/minipay-guar.scm,
we define the protocol with the same message structure and guarantee formulas, but with
no rely formulas. We now pose goal statements for cpsa to resolve; these are shown in
Fig. 7.11–7.12. In these formulas, the conclusions are the rely statements that must be
justified. The hypotheses say that there is a strand z instantiating the relevant role long
enough to reach the rely statement position. They also connect the variables in the rely
formula with the parameters of z. Moreover, each customer goal assumes only the relevant
peer’s signature key to be non-compromised. The merchant assumes only the bank’s signing
key non-compromised, which is desirable since it may have no long-term association with
the customer. The bank presumably has an association with the customer, established
when the customer opened the account; the customer’s signing key could be established at
that time.
    The goals may be constructed from the generated rules cpsa provides when processing
 examples/minipay-rely-guar.scm, essentially adding the non-compromise assumptions
.
    Since cpsa validates these goal formulas in the minipay-guar protocol that contains
the guarantee formulas but not the rely formulas, the generated rules introduced by the
rely formulas are also sound subject to the stated non-compromise assumptions.
    We regard this rely-guarantee method as a systematic way to formalize the trust assumptions
, and the effects, of protocols that accomplish real-world tasks, in this case purchase
and payment.

```scheme
(defrole cust (vars ...)
  (trace
    (guar (fact buy-via c m b item cost n))
    (send ...)
    (recv ...)           ; from bank
    (rely (fact will-transfer c m b cost n mtr btr))
    (recv ...)           ; from merchant
    (rely (fact will-ship c m b item mtr))))
```

```scheme
(defrole merc (vars ...)
  (trace
    (recv ...)           ; from customer
    (send ...)
    (recv ...)           ; from bank
    (rely (and (fact buy-via c m b item cost n)
               (fact will-transfer c m b cost n mtr btr)))
    (guar (fact will-ship c m b item mtr))
    (send ...)))
```

```scheme
(defrole bank (vars ...)
  (trace
    (recv ...)
    (rely (exists ((item merchandise))
                  (fact buy-via c m b item cost n)))
    ;; Do not proceed unless customer signature trustworthy.
    ;; Given that, now commit to transferring the funds
    (guar (and (non (privk "sig" c))
               (fact will-transfer c m b cost n mtr btr)))
    (send ...)))
```
**Figure 7.10: Rely and gauantee formulas in minipay.scm**

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (cost amount) (n data) (mtr btr text))
   (implies
    (and (p "cust" z 2)
         (p "cust" "c" z c)
         (p "cust" "m" z m)
         (p "cust" "b" z b)
         (p "cust" "cost" z cost)
         (p "cust" "n" z n)
         (p "cust" "mtr" z mtr)
         (p "cust" "btr" z btr)
         (non (privk "sig" b)))
    (fact will-transfer c m b cost n mtr btr))))
```

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (item merchandise) (n data) (mtr btr text))
   (implies
    (and (p "cust" z 3)
         (p "cust" "c" z c)
         (p "cust" "m" z m)
         (p "cust" "b" z b)
         (p "cust" "item" z item)
         (p "cust" "n" z n)
         (p "cust" "mtr" z mtr)
         (p "cust" "btr" z btr)
         (non (privk "sig" m)))
    (fact will-ship c m b item mtr))))
```
**Figure 7.11: Goal statements to validate customer’s rely formulas**

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (item merchandise) (cost amount) (n data) (mtr btr text))
   (implies
    (and (p "merc" z 3)
         (p "merc" "c" z c)
         (p "merc" "m" z m)
         (p "merc" "b" z b)
         (p "merc" "item" z item)
         (p "merc" "cost" z cost)
         (p "merc" "n" z n)
         (p "merc" "mtr" z mtr)
         (p "merc" "btr" z btr)
         (non (privk "sig" b)))
    (and (fact will-transfer c m b cost n mtr btr)
         (fact buy-via c m b item cost n)))))
```

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (cost amount) (n data))
   (implies
    (and (p "bank" z 1)
         (p "bank" "c" z c)
         (p "bank" "m" z m)
         (p "bank" "b" z b)
         (p "bank" "cost" z cost)
         (p "bank" "n" z n)
         (non (privk "sig" c)))
    (exists ((item merchandise))
            (fact buy-via c m b item cost n)))))
```
**Figure 7.12: Goal statements to validate other rely formulas**

### 7.8 Lemmas

One common way in which rules have been used in cpsa is as lemmas. The analyst would
define a goal as a query and run cpsa to check that the goal is satisfied. Then the goal
can be added to the protocol as a rule to help speed up the search for subsequent queries.
One common example is when cpsa repeatedly undergoes a long search to satisfy a listener
for some key that cannot be satisfied. Validating once and for all that the key cannot be
leaked, and then including that fact as a rule can drastically improve performance.
    Unfortunately, the syntax for doing so was not particularly friendly to the user. The
formula stated as a defgoal query resides outside the protocol, while the defrule version
 must be included inside the protocol. Managing these lemmas could become difficult
as there was no built-in management to help determine which rules had previously been
validated as lemmas that hold.
    For this reason, cpsa also includes a deflemma form. It must be place outside the
protocol at the top level, just as a defgoal form. However, the syntax for a lemma differs
slightly from that of a goal in ways that allow cpsa to help manage the complexities that
arise from sometimes wanting to validate a formula as a goal and sometimes wanting to use
it as a rule. The user should look at tst/lemmas.scm for an example of the syntax.
    Compared to a defgoal, a deflemma has two extra arguments that come at the beginning
. The first is a flag that signals to cpsa whether or not it should include a query for
the lemma in order to validate that it is satisfied. There are three valid values: rule, goal,
and both. The second is a name that will be used as the rule name when the lemma is
used as a rule.
    When a lemma uses the rule flag, cpsa will update the protocol identified in the
lemma to include the specified formula as a rule. As a result, all subsequent queries for
that protocol will include the lemma as a rule. cpsa will not generate a query for the
lemma. The result is the same as if a copy of the protocol with the same name had been
added in this location with an extra defrule added to it (hence only subsequent queries
would use the rule).
    The goal flag signals cpsa to treat the lemma as if it were a defgoal. A query will be
added to the analysis, but it will not be included as a rule in any subsequent queries. The
skeletons in the analysis contain a comment indicating the name of the lemma the analysis
is associated with.
    When the both flag is used, the behavior is first to treat the lemma as a goal, and then
as a rule. cpsa will first create a query for the lemma against the specified protocol before
updating the protocol to include the lemma as a rule for subsequent queries.
    Since cpsa updates the protocol with a rule at load time, it cannot know in advance
whether the lemma is satisfied or not. That means that subsequent queries will use the
lemma as a rule, even if the query for the lemma shows that the lemma is not satisfied ! For
this reason, the added rule contains a comment to indicate whether or not an associated
query has been added to check its validity. When the both flag is used for a lemma that is

not satisfied, since a query for the formula is generated as a goal, the output will contain
(satisfies (no ...)) as evidence that some goal was not satisfied.

## Chapter 8: Channels and State

Suppose that we are developing a protocol. We may well want to work out the overall
message flow, and understand the consequences of different choices, before we figure out
how—concretely—to protect particular messages. For instance, we may know that the
sender of a particular message will want to ensure that its contents will remain confidential,
without selecting a particular mechanism for doing so. Having worked out the overall
structure of the protocol, it may later be clear how to discharge the assumption that the
contents remain confidential. Or in other cases, we may know that we will use the same
main message flow in several contexts, and in each of those contexts there may be different
mechanisms that would make sense.
    In those kinds of development, cpsa allows us to assume that messages are transmitted
over channels that are assumed to offer security guarantees to the messages they carry.
The treatment of channels also helped determine an approach to representing long-term,
cross-session mutable state in cpsa. The goal of this chapter is to explain how to use
the cpsa channel mechanism, and to build on that understanding to work with long-term
mutable state.

Channel security guarantees. The most important guarantees are authenticated channels
 and confidential channels. They stipulate actions that must be taken by some instance
of a role of the protocol, rather than by the adversary.
   • An authenticated channel guarantees to the recipient of a message that this message
     was sent by some instance of a role of the protocol.

   • A confidential channel guarantees to the sender that this transmission will not be
     received by the adversary, i.e. that any recipient is an instance of a role of the protocol.
     Hence, any disclosure of not-yet-public parts of the message occur only if the message
     is received and acted on by one or more instances of protocol roles.
A channel that is both authenticated and confidential is sometimes called a secure channel.

    Later, when we have developed an adequate protocol using the channel properties, we
can refine it to one or more protocols that use specific cryptographic mechanisms to achieve
the properties we need. For instance, digital signatures or Message Authentication Codes
can achieve authenticity, public-key encryption can achieve confidentiality, and symmetric
encryption (e.g. an authenticated encryption mode) can implement a secure channel.
    Likewise, specific TLS modes can be used to implement authentic, confidential, and
secure channels. For instance, a typical unilaterally authenticated TLS connection provides
the client an authenticated channel for messages from the server, while it provides a confidential
 channel for messages to the server. In itself, the TLS unilateral handshake provides
no guarantee to the server.
    Other properties of channels are sometimes of interest, but are not directly implemented
by cpsa. For instance, a fair channel ensures that a message transmitted onto it will
eventually be delivered to some instance of a role of the protocol. A deliver-once channel
ensures that a message transmitted onto it will be delivered at most once to any instance
of a role of the protocol. In-order delivery is another possible channel property. Some of
these may be represented indirectly in cpsa specifications [5]. However, authenticated and
confidential channels are often useful in protocol design, and fit smoothly into the cpsa
authentication test method.
    In Section 8.1, we describe how to use the cpsa channel mechanism.

Channels and long-term state. In Section 8.2, we also describe a model of protocols
that rely on long-term, cross-session state, which is based on the channel mechanism. Here
we consider a regular principal that interacts privately with a device containing some registers
 that maintain state.1 The principal may read values out of the state registers and
write back other values, often related values; these actions determine the state transitions
the device can undergo when used in this protocol.
    The connection with channels is this. When a regular protocol participant writes a
value into a state register, this is akin to sending a message to oneself at a future moment.
What one relies on, when using this mechanism, is that the recipient of this message—one’s
future self—is still a regular participant, so that any future disclosure to the adversary will
be due to some other action. That is, writing to a state register is sending a message on a
confidential channel.
    When reading from a state register, there are two possibilities. One is that one’s past
self wrote this value into the state register previously. In this case, reading from the state
register is like receiving a message on an authenticated channel. However, there is another
case also, in which the value read may simply have been an initial state, available from the
state register at power-up, so to speak. We call a state value a generated state value when
the second case cannot apply to it, i.e. it is a value that may have been written into the
     By a regular principal for a protocol Π, we mean a non-adversarial principal, i.e. one that acts only in
accordance with the protocol Π.

register but was definitely not available simply as an initial, power-up value. We summarize
the idea by saying that reading a generated state value from a state register is receiving a
authenticated value from a channel.
    Thus, state registers offer a confidentiality property for written values, and an authenticity
 property for read values, if they are generated values. Thus, for state registers, the
duality of confidentiality and authenticity holds in a limited form, i.e. for generated values.
This is the reason why cpsa implements state via the same ideas as confidential and authenticated
 channels, although state requires some additional properties that will be described
below in Section 8.2.

### 8.1 Channels

The cpsa model of authenticated or confidential channels requires only a small amount of
syntax. First, variables of sort chan may be declared to range over channels, for instance:

```scheme
      (vars ... (ch-name-1 ch-name-2 chan) ...)
```

Second, a transmission event or reception event may have an additional component that is
a variable of sort chan, taking the forms:

      (send ch-name-1 sent-msg)
      (recv ch-name-2 recvd-msg)

Finally, we may assert the authenticated or confidential property of a channel, using the
annotations:

      (auth ch-name-1 ch-name-2)
      (conf ch-name-2)

     As with annotations such as uniq-orig and non-orig, these can appear either within
a defskeleton query form or within a defrole role declaration. As in the previous cases,
the semantics for an annotation in a particular query is that the annotation holds only for
that specific instance. An annotation in a role declaration is a much stronger assumption.
It instructs cpsa to add the instance of the assumption every time it adds an instance of
that role. Since it is a much stronger assumption, it yields less precise analyses.
     Starting with cpsa version 4.4.9, when a send or recv event has two arguments, the
first channel argument can be any algebra term, not just a variable of the chan sort. If a
variable of sort mesg is used, that variable must be acquired (i.e. its first occurrence in the
role must be in a carried position of an inbound event).

#### 8.1.1 Yahalom with Channels

We provide two examples of the channel mechanism, both based on the Yahalom protocol.
They both use channels with annotations to explain the security properties needed for
interaction with the key server. An explicit encryption is present only for the last message,
in which the initiator encrypts and returns the responder’s nonce, establishing that the
session key has been received and accepted, and was indeed requested by the initiator when
starting the session.
    In the first version (Section 8.1.2), we “take the easy way out,” and incorporate the
channel annotations into the role definitions, meaning that cpsa will introduce a new
instance of the assumption for every instance of a role that it considers.
    In the second version, we use the slower mechanism, and introduce each individual
channel property in a declaration in the defskeleton query forms. From the latter we
learn a kind of session-independence: The security properties of a particular session of the
protocol depend only on the channels that should be used in that protocol session, and the
messages cannot leak from one session to undermine the security goals of another session.
    It is perfectly reasonable in a development process to explore the protocol design choices
with the channel annotations as assumptions at the role definition level first. When analysis
shows that a version is acceptable, then one can remove the role definition annotations, and
add assumptions strand-by-strand during a stepwise analysis.
    If this analysis yields an acceptable result, for instance the session-independence property
, one can then further refine the protocol by incorporating cryptographic mechanisms
to ensure the channel properties are met. In the original Yahalom protocol (see e.g. [12]),
the channels are implemented via symmetric cryptography. If the initiator and responder
each share an uncompromised long-term key with the server, then an authenticated encryption
 mode certainly satisfies the channel properties. However, other mechanisms are also
possible, e.g. asymmetric primitives or, indeed, TLS.
    Indeed, a choice of a particular primitive early in the design process obscures what
actual properties are needed for the protocol to achieve its goals.

Yahalom: Protocol idea. In the Yahalom protocol, the initiator A provides a nonce
NA to the responder B, who passes that along with its own nonce NB and both names
A, B to a key server. The server then creates a fresh session key K for A and B, packaging
it separately for A and for B with their names; the package for A also contains NA , NB . A
completes the exchange by encrypting B’s nonce NB with the session key K.

Yahalom: Channel assumptions. In any session, the server needs a confidentiality
guarantee for the packages it sends in order to protect the session key K in that session.
So that requires the channel confidentiality property for the outbound channels from the
server. Moreover, the initiator and responder each need an authentication guarantee for
the packages it receives, so as to know that the key is safe to use.

```scheme
(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey) (ch3 chan))
    (trace (send (cat a n-a))
           (recv ch3 (cat a b k n-a n-b))
           (send (enc n-b k)))
    (auth ch3))
```

```scheme
  (defrole resp
    (vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))
    (trace (recv (cat a n-a))
           (send ch1 (cat a b n-a n-b))
           (recv ch2 (cat a b k))
           (recv (enc n-b k)))
    (auth ch2))
```

```scheme
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
    (trace (recv ch1 (cat a b n-a n-b))
           (send ch3 (cat a b k n-a n-b))
           (send ch2 (cat a b k)))
    (conf ch3 ch2)
    (uniq-orig k)))
```
**Figure 8.1: Yahalom protocol with channel assumptions in role declarations**

#### 8.1.2 Yahalom with Channels, 1: Role-level assumptions
We first codify the confidentiality and authenticity channel properties using annotations in
the role declarations. This corresponds to the stronger assumption that compliant principals
 always use channels that successfully achieve those security properties. Since the
assumption is stronger, any conclusions we reach will be weaker conclusions: they are implications
 that depend on a stronger hypothesis. In Section 8.1.3, we will show how, with
a bit of extra work, we can find the tightest relevant hypotheses.
    In Fig. 8.1 we show the three roles of the protocol with the behavior and channel
assumptions mentioned at the end of Section 8.1.1. cpsa will automatically instantiate the
channel assumptions for each role every time it incorporates an instance of the role.
    We can now ask cpsa a succession of queries about this protocol. First, if the responder
has a complete, four-step local session, then there are corresponding server and initiator
runs (Fig. 8.2). All participants agree on the identities A, B, the responder’s nonce Nb , and
the session key K. Moreover, the server and initiator agree on the initiator’s nonce NA ,
but the responder does not need to. cpsa also validates that the session key K cannot be
disclosed.

                                           (defstrand resp 4 (k k) (n-a n-a)
                                                      (n-b n-b) (b b) (a a) ...)

                                           (defstrand serv 3 (k k) (n-a n-a-0)
                                                      (n-b n-b) (a a) (b b) ...)

                                           (defstrand init 3 (k k) (n-a n-a-0)
                                                      (n-b n-b) (a a) (b b) ...)
**Figure 8.2: The responder’s point of view**

    When we ask what follows if the initiator has a full local session, the result is more
limited. The initiator authenticates a server session of at least length two, agreeing on
the identities A, B, the two nonces, and the session key K. Again, cpsa validates that K
cannot be disclosed.
    Observe that if any initiator and responder have local sessions involving a shared key
K, then at least the result of Fig. 8.2 must hold, and they agree on each other’s identities
A, B.
    The server receives no authentication guarantees from the protocol as defined here, but
is guaranteed that the shared key K will remain undisclosed. This is undesirable from
one point of view, as it may cost resources for the key server to generate a new key and
package it. Thus, an adversary can force this to occur as desired. This is (presumably) the
reason why the original Yahalom protocol encrypts the message from the responder to the
server (the arrow that appears dashed in Fig. 8.2). We may achieve the desired effect by
stipulating that the server’s channel ch1 is authenticated. Our analysis shows that there is
no benefit to confidentiality on that channel.
    One might, however, doubt whether there is much benefit to the (auth ch1) stipulation,
since the adversary can still arrange for messages from legitimate responders to be delivered
repeatedly.
    We can infer from this analysis that a symmetric authenticated long-term encryption
key shared between the key server and each client is a good way to implement the channels
ch2 and ch3, since the key server relies on their confidentiality property and the clients rely
on their authentication property.

```scheme
                        (defskeleton yahalom
                          (vars (k skey) (n-b n-a n-a-0 n-b-0 text)
                                          (a b name) ...)
                          (defstrand resp 4 (k k) (n-a n-a) (n-b n-b)
                                             (b b) (a a) ...)
                          (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0)
                                             (a a) (b b) ...)
                          (precedes ((1 2) (0 2)))
                          (uniq-orig k n-b)
                          (auth ch2) ...)
```
**Figure 8.3: Responder’s first guarantee**

#### 8.1.3 Yahalom with Channels, 2: Per-strand assumptions
We now remove the role definition annotations, i.e. we omit the (conf ch3 ch2) annotation
from the declaration of the server, and we omit the (auth ch2) and (auth ch3) annotations
from the responder and initiator declarations, resp. We will now ask a succession of queries,
each eliciting some more information, and allowing us to add small assumptions at each
stage to identify the individual channel properties that matter. First, we ask:
```scheme
(defskeleton yahalom
  (vars (a b c name) (n-b text) (ch1 ch2 chan))
  (defstrand resp 4 (a a) (b b) (n-b n-b) (ch1 ch1) (ch2 ch2))
  (auth ch2)
  (uniq-orig n-b))
```

This yields the output in Fig. 8.3.
    Now that we have ascertained a server run occurred with the same identities A, B and
session key K, we may resubmit this output to cpsa with the added annotation (conf ch2
ch3), saying that we will assume that this server session successfully used channels with
the confidential property. At this point, cpsa completes the analysis with the same shape
shown in Fig. 8.2.
    This establishes that no other channel assumptions could be relevant to the conclusion.
This was not evident from Fig. 8.2, since other channel assumptions may have led cpsa to
discard some branches of analysis as impossible, which might then never be displayed.
    The analysis from the initiator’s point of view can then follow the same pattern.

Message terms as channels. The test suite has a version of the above channel-based
description of Yahalom (tst/chan-mesg.scm) in which, instead of using arbitrary channel
variables to name the channels, they are given names such as (cat a b) to indicate is a
channel intended to go from a to b. The user should be aware that if channel (cat a b)
is marked as authentic, then when b receives a message on that channel, the sending party

will necessarily agree with the values a and b whether or not those names appear in the
message payload.

### 8.2 State

cpsa models situations in which regular principals control devices with state registers or
storage locations—we will henceforth use the term location for all such pieces of memory—
that allow long-term storage and coordination among different local protocol sessions.2
Each protocol role determines when a regular principal reads from a device location; what
it does with the value read from it, and the parts of the value; and when it writes a new
value into a location.

Locations and channels. As we mentioned at the start of the chapter, cpsa relies on the
analogy between reading from locations and receiving messages from channels, and between
writing to locations and sending messages onto channels. In particular, writing to a location
is like sending to a confidential channel, as we are modeling regular principals in control
of the devices. And reading a state value is partly like receiving from an authenticated
channel: Unless the value read might be the result of device initialization, it must have
been written by a previous write action by a regular principal. We say that a value is
a generated state value when we model it as not a possible result of device initialization.
When cpsa knows of a value read from a location that it is a generated state value, it
treats this as an authenticated channel reception. It then investigates the possible ways
that regular principals may previously have written this state value to the location.

Contrast: Locations are mutable. Channels can deliver the same message more than
once, and, since redelivery is never ruled out, effectively always remember their previous
contents. However, locations are mutable. After a transition event observes the value in a
location and writes a new (possibly related) value into the location, subsequent reads are
guaranteed to deliver the new value, not its predecessor. Although any number of read
events may observe the same value, a transition event ensures that the new value is the
only value available from this location. This fact—that transitions erase the past—is the
essential characteristic of mutable state.

“Leads to.” When a state transition event n0 writes a value v into a state location ℓ,
and a later observation or transition event n1 obtains this value v from ℓ, without any
other transitions having occurred to ℓ in between, we say that n0 leads to n1 , and we write
n0 ⇝ n1 .
    Allowing the Dolev-Yao adversary to have devices does not strengthen its powers, as it can already
remember unbounded numbers of messages and perform all the reasonable operations on them. This is why
our model highlights devices under the control of the regular principals.

   Thus, when n0 ⇝ n1 the following conclusions hold:

   1. n0 and n1 are events on the same location ℓ;

   2. n0 is a transition event;

   3. n0 precedes n1 , also written n0 ≺ n1 ; and

   4. n1 receives the value that n0 has written into ℓ.

The event n1 may just be a state observation rather than a state transition. In the former
case, it is a pure read against ℓ. In the latter case, it is the beginning of a transition event,
which we think of as consisting of a read of the old value in ℓ followed by a write of the
new value into ℓ.
    Internally, cpsa represents a state event as transmitting or receiving a pair t = (p, v).
The second component is the state value v being read or written. The first component is
a special value which is thought of as a spacetime point p. If the event is a write event,
then cpsa assumes p to be uniquely originating. cpsa defines n0 ⇝ n1 to hold iff (i) n0 is
a state node; (ii) n0 ≺ n1 , and (iii) for some message t, n0 transmits t and n1 receives t.
    This cpsa representation lets us add to (1)–(4) another conclusion: When n0 ⇝ n1 ,

   5. if also n2 ⇝ n1 , then n0 = n2 .

#### 8.2.1 The axioms of state

The mutating, past-erasing property of transitions is expressed in two basic properties of
the leads-to relation. They say in essence that leads-to is discrete for transitions events on
any one location.
    We write them diagrammatically in Fig. 8.4, using a boxed variable m to represent
a transition event, and a plain variable m to represent an event that may be either a
transition or a pure observation. We use a wavy arrow to represent leads-to; a dotted arrow
to represent the precedence ordering ≺; and ⪯ to express the weak ordering, i.e. n0 ⪯ n1
holds if and only if n0 ≺ n1 or n0 = n1 .
    In each case, the events n, m0 , m1 are all state events on the same location ℓ.

Axiom (i) states that when n ⇝ m0 and n ≺ m1 , all of these being transition events on
    ℓ, then m0 ⪯ m1 . Thus, the leads-to relation is a discrete step, and if m0 ̸= m1 , then
    the latter comes definitely later.
      We call axiom (i) the discrete-after axiom, since it forces m1 to come after a transition
 that is the target of the ⇝ edge.

Axiom (ii) states that when m0 ≺ n and m1 ⇝ n, each mi being a transition on ℓ, then
    m0 ⪯ m1 . Again, the leads-to relation is a discrete step, and if m0 ̸= m1 , then the
    former comes definitely earlier.

     We call axiom (ii) the discrete-before axiom, since it forces m0 to come before a
     transition that is the source of the ⇝ edge.

The symmetry between these two principles is better brought out if we omit to state, in (i),
that n is a transition. The source of a leads-to edge is always a transition. The common
idea is that a weak ordering holds between m0 and m1 , whenever one is a connected to n
by ⇝ and the other by ≺. They jointly say: a transition ordered with respect to one end
of a leads-to arrow has the corresponding weak ordering with respect to the other end.

                      (i)                  n                                          n
                                                    ≺                                             ≺
                                                                  =⇒
                                                                                               
                                 m0                 m1                 m0             ⪯           m1

                      (ii)       m0                     m1             m0                 ⪯           m1
                                                                  =⇒
                                       ≺                                       ≺           
                                           n                                              n
**Figure 8.4: Two axioms about state events on the same location ℓ**

                      n                                                          n0
                                 =⇒ m0 = m1                                               ≺
                                                                                                =⇒ false
                                                                                         
                m0          m1                                         n1 ≻ m

                                               n0
                                                                  =⇒        false
                                                         

                                  n1           ≺         m
**Figure 8.5: Three derived rules for state: Scissors, no interruption, and cake**

#### 8.2.2 Consequences of the axioms

What is distinctive of state—over and above channel confidentiality and channel authenticity
 for generated state values—is captured in the discrete-after and discrete-before axioms.
However, each of them has a disjunction as its conclusion, namely either m0 = m1 or
m0 ≺ m1 . Disjunctions are logically less convenient than non-disjunctive conclusions, since
separate possibilities must each be explored. Hence, cpsa also formalizes three consequences
 of the discreteness axioms. One of them has the conclusion m0 = m1 , and the

other two have the conclusion false. Again assuming that the state events concern the same
location ℓ, the rules are:

Scissors rule, which says that when a given node n leads to transition nodes m0 , m1 , the
     latter two are equal.
     Equivalently, a single node leads to at most one transition node.

No interruption, which says that a transition node m is never properly between transition
     nodes n0 and n1 when n0 ⇝ n1 .
     Thus, a transition node m cannot “interrupt” the leads-to edge.

Cake rule, which says that if a node n0 leads to two other nodes, and one of them is a
    transition n1 , then the other one m does not follow the transition.
     Thus, it says that a transition n1 caps off the period when other events m (which are
     pure observations by the scissors rule) may result from n0 .

We present these diagrammatically in Fig. 8.5. The two leads-to edges of the scissors rule
are like the blades, which the equation m0 = m1 snaps shut. The cake rule formalizes the
fact that you can’t eat your cake at n1 and have it too at m, at least not if m follows n1 .
    Again, their concrete form may be found in the output of cpsa specifications using
state, such as tst/open-closed.tst.

Why these rules are consequences. Each of these rules is easily justified from the
discrete-after and discrete-before rules, using the facts that n ⇝ m implies n ≺ m and that
⪯ is a (weak) partial order.

Scissors rule: The scissors rule follows by two applications of the discrete-after axiom.
     Specifically, since n ⇝ m1 implies n ≺ m1 , we can apply the discrete-after axiom to
     infer that m0 ⪯ m1 . Symmetrically, observing that n ⇝ m0 implies n ≺ m0 , we can
     again apply the discrete-after axiom to infer that m1 ⪯ m0 .
     The antisymmetry of ⪯ implies that m0 = m1 .

No interruptions rule: For the no interruptions rule, apply discrete-after to infer that
     n1 ⪯ m. But since m ≺ n1 is also assumed, this would yield a cycle.

Cake rule: For the cake rule, apply discrete-before, instantiating its variable m0 as m,
    its m1 as n0 , and its n as n1 . Thus, it follows that m ⪯ n0 , but the leads-to edge
    n0 ⇝ m implies n0 ≺ m, yielding a contradiction.

```scheme
(defrole dev-open
    (vars (k skey) (n nb text) (any mesg) (d o b name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (cat b n (enc (open-req b d o nb n) (hash-dk (cat b nb n k)))))
     (load ls (door-state d any))
     (load lk (dev-key-state d o k))          ; check k unchanged
     (stor ls (door-state d (opened b nb n)))
     (send (hash (open-req b d o nb n))))
    (gen-st (dev-key-state d o k))
    (facts (same-dev ls lk)))
```
**Figure 8.6: Device-open role causing door to open**

#### 8.2.3 Syntax for state

In defining the syntax for modeling state, we first describe state events and the state
segments that they can build up. We then describe how to specify generated state values—
which were mentioned at the beginning of the chapter—and critical sections—which are
atomicity assumptions about state segments.

State events and state segments. In addition to the chan sort discussed in Section 8.1,
there is a sort locn. A variable lv declared of sort locn via a declaration such as (lv locn)
may be used as the target of load and stor events; these events indicate that a value is to
be read from a location or written to it. Thus, Fig. 8.6, which uses a number of operators
from a lang field,3 shows a role that manipulates two variables lk, ls of sort locn. Its
intent is to open a door in response to a suitable encrypted command, conforming its
action. The form (lk ls locn) declares the variables of sort locn. The form (load lk
(dev-key-state d o k)) loads a tuple including a key k from the locn lk, which must
contain a tuple of this kind for the event to occur. After receiving a message that contains
a request to open the door, it loads the current door state from the other location ls, after
which it stores back the “open” value. These events might be implemented by a sensor and
an actuator in a real device. Finally, it confirms success by sending the hash of the open
request.
    Starting with cpsa version 4.4.9, a load or stor event may be followed by any pair of
message terms. The first acts as a name for the location, just like a channel send or recv
(Section 8.1). A particularly useful structure for a channel name is (cat d l) where d is
a variable of sort dev and l is a variable of sort locn. This can help to represent natural
     See Section 4.4. In this example, dev-key-state, open-req, door-state, and opened are tuple operators
, and hash-dk is a hash operator, in essence a key derivation function. This example is found
in examples/open-closed.scm.

assumptions about stateful devices such as the fact that no role will update one location on
one device and another location on another in the same transaction. If the locations can be
viewed as fixed addresses on a device then one can even use (cat d "l") with a constant
to represent the location.
    In general, a state segment consists of zero or more load events followed by zero or
more stor events, subject to the requirements that:

  1. no two load events in this state segment load from the same location;

  2. no two stor events in this state segment store into the same location.

A particular state segment is a transition for a location ℓ iff there is a stor into ℓ in this
state segment. It is a (pure) observation for ℓ iff there is a load from ℓ but no stor into ℓ
in this state segment.
    State segments of length greater than two necessarily represent events that involve
multiple locations (given the constraints above). If a transition for location ℓ1 depends on
the value present in ℓ2 , then a state segment can load v2 from ℓ2 and then store a new
value dependent on v2 into ℓ1 . In this case, the state segment is a transition for ℓ1 but
a pure observation for ℓ2 . If instead new values are stored into both ℓ1 and ℓ2 , then the
state segment is a transition for both. In other cases, a state segment loads from both ℓ1
and ℓ2 , but instead of storing back to either of them, it simply uses those values to control
future message transmissions and receptions. In the latter cases, the state segment is a
pure observation for both ℓ1 and ℓ2 .

Rules for protocols with state. cpsa generates three types of rules for protocols that
manipulate state, in addition to the two axioms of Section 8.2.1 and the three consequences
of Section 8.2.2.4
    The first kind are the transition rules, and these are generated entirely automatically by
cpsa. The axioms and rules of Sections 8.2.1–8.2.2 depend on which events are transition
events, the boxed events in Figs 8.4–8.5. Moreover, the syntax of the state segments
determines which these are. Thus, cpsa generates rules that imply that an event is a
transition event if:

  1. it is a stor event; or

  2. it is a load event, and the strand is long enough also to have a stor event from this
     state segment for the same location ℓ.

These are the transition rules.
   The second kind are the generated state value rules. As we mentioned at the start, a
generated state value is a value v that is definitely non-initial. Thus, if a load event reads
      See Section 7.7 for rules in cpsa.

a generated state value v from a location ℓ, then ℓ is acting like an authenticated channel
for v. In particular cpsa will consider which instances of the roles could previously have
stored v into ℓ; one of those must be present.
    A generated state assumption may be introduced as a per-strand assumption, akin to
the declarations discussed in Section 8.1.3. In that case it is syntactically present in a cpsa
defskeleton query such as:
```scheme
(defskeleton open-closed
  (vars (k skey) (d o name))
  (defstrand dev-pass 4 (k k) (d d) (o o))
  (gen-st (dev-key-state d o k)))
```

This gen-st declaration says that the particular tuple (dev-key-state d o k) using the
values of the variables that appear in this strand forms a generated state value.
    A generated state assumption may be introduced as a role-level assumption, akin to the
declarations discussed in Section 8.1.2. In this case, the specifier wants to tell cpsa that
the declared value is a generated state value whenever an instance of the role is long enough
to furnish values for the variables that appear in it. Fig. 8.6 contains a role-level generated
state assumption, namely (dev-key-state d o k). Since the trace of the dev-open rule
loads a value of this form as its first action, these variables have values in every instance of
height ≥ 1.
    cpsa enforces this role-level assumption by generating a rule stating:
(defgenrule gen-st-dev-open-0
    (forall ((z strd) (k skey) (o d name))
      (implies
        (and (p "dev-open" z 1) (p "dev-open" "k" z k)
             (p "dev-open" "o" z o) (p "dev-open" "d" z d))
        (gen-st (dev-key-state d o k)))))

cpsa uses the defgenrule form to distinguish rules it has generated automatically from
rules that were explicitly written by the specifier, as described in Section 7.7.
    Finally, the third kind of rule concerns critical sections. These are generated automatically
 for each state segment. These generated rules imply that any node that precedes
one of the events in a state segments must precede all of them. Any node that follows one
of the store events must follow all of them. Thus for instance in Fig. 8.7, the load events at
indices 1, 2 and the store events at indices 3, 4 occur with transaction-like atomicity. cpsa
generates the rules in Fig. 8.8. They are of value only when the state segment has multiple
loads or multiple stores. In this particular example, the critical section declaration does
not in fact make a difference to the analysis.

```scheme
(defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (ch chan) (lk ls locn))
    (trace
     (recv ch (cat "power-up" d o k))
     (load lk old)
     (load ls old1)
     (stor lk (dev-key-state d o k))
     (stor ls (door-state d (closed o)))
     (send (enc "up" k)))
    (auth ch)
    (facts (same-dev ls lk)))
```
**Figure 8.7: State segments are critical sections**

```scheme
(defgenrule cau-dev-up-2
   (forall ((z z1 strd) (i indx))
     (implies
       (and (p "dev-up" z 3) (prec z1 i z 2))
       (or (= z z1) (prec z1 i z 1)))))

 (defgenrule eff-dev-up-3
   (forall ((z z1 strd) (i indx))
     (implies
       (and (p "dev-up" z 4) (prec z 3 z1 i))
       (or (= z z1) (and (p "dev-up" z 5) (prec z 4 z1 i))))))
```
**Figure 8.8: Critical section: Generated rules**

#### 8.2.4 Channels and state: Summary
A core idea is that receptions may have authenticity, meaning that the adversary has not
delivered the message; thus, cpsa explores what regular strands may have transmitted it.

Dually, a transmission may have confidentiality, meaning that the adversary will not receive
the message directly. Thus, any parts of the transmitted message that appear in new forms
subsequently will require some regular strand to have received it and transformed these
parts.
    In the channel mechanism, cpsa allows these properties to be directly associated with
channels, providing a useful technique for protocol design. In the state mechanism, cpsa
models the confidentiality of storing a value into a device controlled locally by the regular
principal(s). Moreover, stored state values with the gen-st property satisfy the authenticity
condition also.
    Besides these properties, mutable state also requires modeling the fact that an old state
value can no longer be observed in a location after that location has undergone a transition.
We express these in the two axioms of Fig. 8.4; cpsa also uses their three consequences as
shown in Fig. 8.5 for efficiency.
    The modeling distinguishes between transitions on a location, which are expressed in
state segments that contain a stor to it, and observations, expressed in state segments
that contain a load but no stor to it. cpsa determines which events are transitions on a
location automatically, and generates rules to keep track of this information. Rules are also
available to determine which state values are stored state values, and these are generated
from gen-st declarations.
    cpsa’s job is to enumerate shapes. When a specification distinguishes a kind of value
that can only appear in an initial load, and transitions that do not produce these values, but
always produce stored state values with the gen-st property, then a run can typically have 0,
1, 2, . . . , n transitions, and these will have no homomorphisms between them. Hence there
will be infinitely many distinct shapes to enumerate, and cpsa will not terminate, although
its partial outputs are often informative. The craft of using cpsa to understand state in
protocols is often to restrict the gen-st declarations so that cpsa does not distinguish
among state histories of (irrelevantly) different lengths.
---

> **Part IV: Reference material**

## Chapter 9: Troubleshooting

The cpsa tool is a complicated one and many errors are possible in its use. In this chapter
we discuss these errors, from the simplest to the most complex, and offer suggestions as to
how to resolve them.

### 9.1 Non-termination

The cpsa tool is not guaranteed to complete its search on all well-formed inputs. The
problem space cpsa attempts to perform includes some Turing-undecidable problems.
   Because of this, the tool has two bail-out conditions that users should be aware of:

   • The strand bound causes the tool to abort its analysis if any skeleton it analyzes
     has more strands than the bound. By default, the strand bound is 12.

   • The step limit causes the tool to abort its analysis if during the analysis of a single
     input defskeleton or defgoal, the number of skeletons it processes exceeds the limit.
     By default, the step limit is 2000.

   • The depth limit causes the tool to not analyze skeletons more steps away from the
     initial point of view than the bound. There is no depth limit by default. Skeletons that
     are unrealized and not analyzed due to the depth limit are marked with “(fringe)”.

    If you execute an analysis and the tool says “Strand bound exceeded” or “Step limit
reached,” then that bail-out condition has come into play. This may indicate an analysis
that would never terminate, but it may also be the case that the strand bound or step limit
is too small, and a larger one will enable the analysis to complete.
    Unlike the strand bound and the step limit, the depth limit never triggers an error
condition, and can thus be useful for multi-skeleton analyses in which one of the earlier
skeletons would otherwise have a non-terminating analysis.

    The step limit, depth limit, and strand bound can be adjusted through the limit,
depth, and bound options, respectively. See Section 10.5.
    Note that sometimes, a user may become impatient waiting for an analysis to either
complete or bail out. When this happens, the user should not hesitate to interrupt the
tool; the tool will output a partial result that can be graphed so the user can examing the
analysis done so far.
    An analysis that doesn’t terminate does not necessarily represent an insecure protocol, it
may just indicate a protocol where a more clever analysis is required than cpsa’s automated
one.

#### 9.1.1 Configuring the search

There are cases in which the default cpsa analysis does not terminate, but a non-default
analysis would terminate. The tool has several default settings that influence the search
but can be configured:

   • Node precedence. In a skeleton with multiple unrealized receptions, the tool will,
     by default, focus on the topmost unrealized node of the rightmost strand that contains
     an unrealized node. If you find that an analysis gets into a large search space due
     to exploring those unrealized receptions first, you could alter this order with the
     reverse-nodes or try-old-strands options. The latter will prioritize the leftmost
     strands over the rightmost, while the former will prioritize the bottom-most unrealized
     node in the strand rather than the topmost. These can be used individually or jointly,
     yielding three extra non-default search strategies.

   • Critical term precedence. Occasionally, a reception will arise that is unrealized
     and multiple critical terms are available. In particular, there are cases where a term
     contains both a hard-to-explain encryption and a restricted nonce. For instance, in
     the Kerberos protocol, the ticket {|k, a, b|}SK(b,s) can serve as both a critical encryption
     (because SK(b, s) may be declared non-originating) and a critical term (because k
     is uniquely originating). By default, cpsa will treat the encryption as the critical
     term because this tends to lead to learning more in fewer steps, but this choice can
     be reversed by using the check-nonces option.

   • Priority. The tool contains an ability to declare a priority for certain receptions
     that differs from the default. Priority takes precedence over all other search order-ings
. See Section 10.4 for the format requirements for declaring priorities, and the
     priority_test.scm example in the examples directory.
     Note that the default priority is 5, and priority 0 indicates that the tool should never
     bother solving tests at those nodes. This may be of use, for instance, if solving one
     particular node leads to infinite analysis, but other nodes would result in a quick
     determination that a skeleton is dead.

### 9.2 Error messages

In this section, we provide an alphabetical listing of error messages / failures that may arise
during cpsa execution. If you get an error message not included here, it likely represents
a bug and should be reported to the tool maintainers.

   • “[ASSERT FAILED] [...]”. This kind of error should not occur. If you see this
     happen, please contact the tool maintainers and make a bug report!

   • “Aborting after applying 500 rules and more are applicable”. This most
     likely indicates a circular use of rules.

   • “Algebra.absenceSubst: bad absence assertion” or “Algebra.nullifyOne: unexpected
 pattern” The absent declaration must be declared on a pair where the
     first element is an rndx variable and the second element is an exponent. These errors
     should not occur if you did not give cpsa an input with an absent declaration.

   • “Algebra.inv: Cannot invert a variable of sort mesg”. Variables of the mesg
     sort should never be used as the key in an encryption. cpsa uses a single function
     symbol to represent both symmetric and asymmetric encryption, and when the key
     is a variable of sort mesg, it is ambiguous which is meant. As a result, it is unclear
     what the decryption key would be for such a message. When cpsa tries to calculate
     the decryption key when the encryption key is a variable of sort mesg, this error is
     produced.

   • “Atom not unique at node”. This occurs when a formula has been specified
     including a uniq-at predicate in the antecedent that is untrue.

   • “Bad char [...]”. This error message comes from a low-level parser trying to understand
 S-expressions. When parsing an S-expression, any non-whitespace that isn’t
     a parenthesis is an “atom” but we expect atoms to be symbols, numbers, or quoted
     strings, and only certain characters are allowed in these. An atom that starts with a
     digit is expected to be a number, for instance, so subsequent non-digits will cause an
     error of this kind. The characters allowed in symbols include all alphanumeric characters
 and the following punctuation marks: +, -, *, /, <, =, >, !, ?, :, $,
     %, _, &, ~, ^.

   • “Bad height” / “Bad position in role” / “Negative position in role”. A
     defstrand includes a specification of a height (the length of the instance) but that
     height must be positive and must not exceed the length of the role.

   • “Bad str-prec”. Your goal included a str-prec predicate among node variables
     associated with different roles. In other words, your formula has attempted to make
     a single strand that includes events from distinct roles.

• “Close of unopened list”. Your input has an erroneous close-paren.

• “Disallowed bare exponent”. See Section 4.2. The tool requires that within roles
  and skeletons, any exponent occurring outside an exponentiation function must be of
  sort rndx.

• “Domain does not match range”. This error message occurs when cpsa is trying
  to understand the variable assignment you have specified in a defstrand. You may
  have defined the value of a parameter more than once, or your definition may have
  a type mismatch. For instance if a is a parameter role expected to be of the name
  type, and you declare t to be a text variable, then including (a t) in a defstrand will
  produce this error.

• “Duplicate role [...] in protocol [...]”. The roles in a protocol must have distinct
  names. This error occurs if you have two protocols with the same name.

• “Duplicate variable declaration for [...]”. Within any vars statement, any symbol
 may be used for a variable name, but each variable name can be declared only
  once.

• “End of input in string”. You included a quote-delimited string but didn’t close it
  before the end of the input file.

• “Equals not allowed in antecedent”. The equals predicate may only be used on
  the conclusion side of a defgoal.

• “Expansion limit exceeded”. This most likely indicates a circular use of macros.
  The limit of expansion of a macro within a macro is hard-coded in the tool as depth
  1000.

• “Expecting [...] to be [a/an ...]”. You have a type error in your use of a function
 symbol. For instance if (pubk a) is to be loaded within a particular variable
  declaration scope, the a variable should be of the name sort.

• “Expecting a node variable” / “Expecting an algebra term”. Certain predicates
 within a defgoal expect one of their inputs to be a declared node variable (or
  to be a non-node variable). If a variable used in such an input is declared otherwise,
  this error message is produced.

• “Expecting an atom”. Certain declarations, in particular the uniq-orig, uniq-gen,
  and non-orig ones, are expected to be used on atomic terms rather than compound
  ones.

• “Expecting terms in algebra [...]”. This is a historical artifact resulting from the
  fact that the algebra has two names. If you specify one name as a runtime parameter

  (or in the herald) that is different from the name used in the defprotocol form, this
  error will result.

• “Expts must first be received, rndxs first sent”. If the first occurrence of a
  variables of the expt sort is in a transmission, it could resolve to any multiplication
  of exponents and so is underspecified. When receiving an exponent, there is no way
  to ensure it was not chosen to be some multiplication of other exponents, so we can
  assume its sort is rndx. Hence the rule described by the error.

• “Identifier [...] unknown”. This is a relatively common user-caused error that
  occurs when you try to use a variable not declared in your vars declaration.

• “Include depth exceeded with file [...]”. Most likely, this indicates a circular use
  of the include command. The limit of inclusion within an included file is depth 16.

• “Keyword [...] unknown”. The tool was expecting the symbol to specify an algebra
  function symbol, but it didn’t match any of the available ones. This most commonly
  indicates that the user forgot to include a function symbol name at the beginning
  of a list when describing a term. One of the most common forms of this mistake is
  to include (send (a b)) in a trace of a role, when the user intended to model the
  sending of the pair (a, b). The proper input would be (send (cat a b)).
  Because of this type of mistake, it is recommended to avoid using variables in your
  model that are the same as function symbol names such as “ltk” or “pubk”.

• “In a rule equality check, cannot find a binding for some variable”. An
  equality in a rule is receiving a variable that has not been bound by a length or
  parameter predicate. Try moving the equality to the end of the conjunction in which
  it occurs.

• “In rule [...], parameter predicate for [...] did not get a strand”. This message
  occurs when a strand variable is not bound by a length predicate.

• “In rule [...], [...] did not get a strand”. This message occurs when a strand
  variable is not bound by a length predicate.

• “In rule [...], [...] did not get a term. This message occurs when an algebra
  variable is not bound by a parameter predicate.

• “Malformed [...]”. Generally speaking, this indicates a syntax error. Consult the
  grammar in Chapter 10 for the syntax requirements for the type of object the tool
  claims was malformed. Double-check that you have spelled required keywords correctly
, and that your parentheses are matched.

• “Malformed association list”. This refers to one of the “-alist” symbols in the
  grammar; these may occur in skeletons, goals, protocols, or roles.
  Association lists are lists of S-expressions, each of which is a list that starts with a
  symbol. This error would occur if you had, for instance, a symbol or a number, or an
  S-expression starting with a number as an input to a defrole or defskeleton.

• “Malformed input”. Top level S-expressions in your input file must be one of the
  following: defprotocol, defskeleton, defgoal, comment, or herald. The tool
  also recognizes defpreskeleton as a synonym for defskeleton. If you have an S-expression
 at the top level that is other than one of these, this is the error message
  you will see.

• “Malformed pair – nodes in same strand”. In a defskeleton you are prohibited
  from specifying orderings between nodes in the same strand.
  This is not the case for leadsto relationships.

• “No strands”. Your defskeleton did not include any strands at all; it must include
  at least one.

• “Node occurs in more than one role predicate”. Node variables in a goal must
  occur within a role position predicate, but should not occur within more than one
  within their defined scope.

• “Priority declaration disallowed on [...]”. Prioritization has no effect except on
  events that need an explanation. If you try to change the default priority of a send
  or stor event, this is assumed to be a mistake and the tool produces this error.

• “Protocol [...] unknown”. This error occurs when you have a defskeleton or
  defgoal with a protocol name not matching any defprotocol so far present in the
  file.

• “Role [...] not found in [...]”. You included a defstrand referencing a role that
  does not exist in the protocol definition.

• “Role in parameter pred differs from role position pred”. A node variable
  in a formula should occur in a role position predicate but may also occur in node
  parameter predicates. However, node parameter predicates for a given node variable
  should match the role of the role position predicate the variable occurs in.

• “Role not well formed: role trace is a prefix of a listener”. cpsa disallows the
  use of roles that begin with the reception of some message followed by the transmission
  of that same message, because there is an ambiguity as to whether an instance is a
  listener or an instance of a protocol role. This should not be a problem because

  beginning a role in this manner is quite unusual, but if it is necessary for you to do so
  we recommend the reception be paired with a tag constant such as (cat "regular
  role" [...]).

• “Role not well formed: non-orig [...] carried”. The non-orig declaration
  specifies that a certain atomic value not be carried (see Section 6.2). You have made
  such a declaration but a plain (full-height) instance of your role violates the rule.

• “Role not well formed: uniq-orig/uniq-gen [...] doesn’t originate/generate”.
  The uniq-orig declaration in a role requires the declared value to originate, i.e., its
  first carried occurrence is in a transmission. The role probably has an earlier carried
 reception of the value. Similarly uniq-gen requires the first occurrence (whether
  carried or not) to be in a transmission. See Section 6.2 for an explanation of “carried.”

• “Role not well formed: variable [...] not acquired”. Variables of the mesg sort
  must be “acquired” when used in roles. This means that the first occurrence of the
  variable must be a carried occurrence in a reception event. See Section 6.2 for an
  explanation of “carried.”

• “[Role / Skeleton] not well formed: inequality conditions violated”. A neq
  declaration is false where it is first declared: in a role or skeleton definition.

• “[Role / Skeleton] not well formed: lt declarations form a cycle”. The lt
  declarations present in a role or in a skeleton are already violated in the role or
  skeleton definition.

• “[Role / Skeleton] not well formed: subsort requirements violated”. The
  subsort declarations present in the role or skeleton being defined are already violated.

• “Skeleton not well formed: a variable in [...] is not in some trace”. A
  defskeleton causes this error when a variable used in a declaration does not appear
  in any of the traces.

• “Skeleton not well formed: cycle found in ordered pairs”. The ordering edges
  (strand succession plus ordered pairs) of a skeleton should form an acyclic graph. A
  cycle represents circular causality which should not be possible in any real execution.

• “Skeleton not well formed: non-orig [...] carried”. The non-orig declaration
  specifies that a certain atomic value not be carried (see Section 6.2). You have made
  such a declaration but your defskeleton violates the rule.

• “Skeleton not well formed: ordered pairs not well formed”. This error occurs
  when an ordering is specified between the wrong types of events. In cpsa, an ordering
  must be such that the earlier node has an outgoing type, so for instance an ordering
  directly between two reception events is disallowed.

• “Sort [...] not recognized”. You attempted to declare a variable to be of a sort
  not present in the algebra. There is likely a typo in one of the sorts.

• “Terms in [role/skeleton] not well formed”. This error occurs when you have
  constructed a term using a function symbol that expects inputs of a certain sort,
  but your inputs are not of that sort. For instance, in (ltk a b), a and b must be
  variables of the name sort, or they are not well-formed. To resolve: double-check your
  variable declarations and your use of function symbols.

• “Too many locations in declaration”. You have a native declaration that appears
  to include two or more locations in it. All native declarations allow at most one
  location.

• “Type mismatch in equals”. The equals predicate in a defgoal can be used
  to compare node variables or to compare algebra variables, but cannot be used to
  compare node variables to algebra variables.

• “Unbound variable in [...]”. In a defgoal, variables must meet specific binding
  requirements. See Chapter 7 for details. This error indicates that you have provided
  a formula that the tool rejects for this reason.

• “Unexpected end of input in list”. One of the most frequent user errors—you
  didn’t include close parens for all your S-expressions.

## Chapter 10: CPSA Program Reference

### 10.1 CPSA pre-processing

The cpsa tool performs a pre-processing step before it interprets its input. There are two
important features that take place during pre-processing: macros and file inclusion.

File inclusion. cpsa input files that become large enough become unweildy, and the user
may wish to break them down into logical components and include one file in another. For
instance, one might wish to separate protocol definitions out so they can be reused, or a
user might wish to put together a file of macros they find useful. To include one file in
another, add (include "filename") as a top-level S-expression where you wish that file
to be included. Inclusion recognizes only relative paths.

Macros. The cpsa pre-processor interprets macros.
   To define a macro in a cpsa input file, use the defmacro keyword in an S-expression.
The envelope.scm file in the examples directory uses the following macro:

;; This is the refusal token
(defmacro (refuse n pcr v k aik)
  (enc "quote" (extend "refuse" (extend n pcr)) (enc v k) aik))

    The first input to the defmacro defines the format that will trigger the macro. In
this case, the first macros are defined for an S-expression with keyword refuse and five
additional inputs. The second input to the defmacro describes what the macro should be
replaced with. Symbols that exactly match the subsequent symbols in the first input are
interpreted as standing for the inputs when the macro is used. So for instance (refuse a
b c d e) would be replaced by

(enc "quote" (extend "refuse" (extend a b)) (enc c d) e)

wherever it appears in what follows. Macros can call on other macros, but there is a depth
limit to the amount of recursion that this can entail. In the example, extend is actually
another macro.
    Normally a defmacro will replace a symbol with a single S-expression, but the ˆ (splice)
keyword can be used to indicate that a macro should be replaced with more than one S-expression
. This may be of use, for instance, to describe a portion of a role’s trace, when
defining multiple roles with some behavior in common. For instance:

(defmacro (handshake n a b)
  (^ (send (enc "hello" a b n (pubk b)))
     (recv (enc "hello-received" a n (pubk a))))

   Note that the pre-processor actually handles the splice keyword as a separate pre-processing
 step after macro expansion. For this reason, use of ˆ outside of macros can
produce unanticipated behavior.

### 10.2 CPSA input syntax

The complete syntax for the analyzer using the Basic Crypto Algebra is shown in Table 10.1.
The start grammar symbol is file, and the terminal grammar symbols are: (, ), symbol,
string, integer, and the constants set in typewriter font.
    The alist, prot-alist, role-alist, and skel-alist productions are Lisp style association
 lists, that is, lists of key-value pairs, where every key is a symbol. Key-value pairs
with unrecognized keys are ignored, and are available for use by other tools. On output, unrecognized
 key-value pairs are preserved when printing protocols, but elided when printing
skeletons.
    The contents of a file can be interpreted as a sequence of S-expressions. The S-expressions
 used are restricted so that most dialects of Lisp can read them, and characters
within symbols and strings never need quoting. Every list is proper. An S-expression atom
is either a symbol, an integer, or a string. The characters that make up a symbol are
the letters, the digits, and the special characters in “-*/<=>!?:$%_&~^+”. A symbol may
not begin with a digit or a sign followed by a digit. The characters that make up a string
are the printing characters omitting double quote and backslash, except when double quote
and backslash are escaped using the backslash character. Double quotes delimit a string.
A comment begins with a semicolon, or is an S-expression list at top-level that starts with
the comment symbol.

**Table 10.1: cpsa Input Syntax. See Tables 10.3 and 10.5 for algebra syntax (for the term and sort symbols), Table 10.6 for declaration syntax (for the role-decl and skel-decl symbols), and Table 7.1 for goal syntax (for the sentence and conclusion symbols).**

```text
       file   ←    herald? form+
   herald     ←    (herald [symbol | string] alist)
     form     ←    (comment . . .) | protocol | skeleton | goal
 protocol     ←    (defprotocol id alg role+ rule∗ prot-alist)
         id   ←    symbol
       alg    ←    basic | diffie-hellman
     role     ←    (defrole id vars trace role-alist)
      vars    ←    (vars vdecl∗)
    vdecl     ←    (id+ sort)
    trace     ←    (trace {event | annot}+)
    event     ←    (dir term? term)
        dir   ←    send | recv | load | stor
    annot     ←    (cheq id term) | (rely conclusion) | (guarantee conclusion)
     rule     ←    (defrule id sentence alist)
role-alist    ←    role-decl role-alist | alist role-alist
     alist    ←    (symbol . . .)? alist?
 skeleton     ←    (defskeleton id vars strand+ skel-alist)
   strand     ←    (defstrand id integer maplet∗)
              |    (defstrandmax id integer? maplet∗)
              |    (deflistener term)
   maplet     ←    (term term)
skel-alist    ←    skel-decl skel-alist | alist skel-alist
              |    (precedes node-pair∗) skel-alist
              |    (leadsto node-pair∗) skel-alist
              |    (goal sentence+)| (facts(id term*))
 node-pair    ←    (node node)
     node     ←    (integer integer)
      goal    ←    (defgoal id sentence+ alist)
    check     ←    rule | goal | both
    lemma     ←    (deflemma check id id sentence alist)
```

### 10.3 Algebra reference

#### 10.3.1 Basic crypto algebra

The basic crypto algebra is an order-sorted algebra with signature described in Table 10.2.
Historically it was a distinct subset of the Diffie-Hellman crypto algebra, but they have since
been merged into a single algebra used by all protocols. The presentation here starts with
the basic crypto algebra as the core, then describes the Diffie-Hellman-specific additions.
The basic algebra is the free order-sorted algebra generated by the function symbols, sorts,
and constants given, modulo the one equation.
    Additionally, cpsa reasons about derivability of values from other values, and the basic
derivation rules are given in the table, where inv is defined as follows (with ⊥ indicating
“undefined”):
                                        if a : akey
                                −1
                                a
                    inv(a) =      a     if a is not a variable of sort mesg              (10.1)
                                  ⊥     otherwise.
                               

    Because inv is undefined on variables of sort mesg, cpsa cannot handle protocols or
skeletons in which a value is encrypted with such a variable. This is a consequence of the
choice we made in the design of cpsa to use only one encryption function symbol, despite
there being two forms of encryption (symmetric and asymmetric). When encrypting with
a variable of sort mesg, the type of encryption is ambiguous.
    Table 10.3 describes the grammar for basic crypto algbera messages in the input syntax.
    Each of these function symbols has a specific interpretation in the algebra signature;
for instance, enc refers to the {| · |}· function symbol, and pubk refers to the K(·) function
symbol when it has one input, but to K(·)    s when it has two inputs, where the second is s.

privk refers to the composition of either K(·) or K(·)s with (·)−1 .

**Table 10.2: The Basic Cryptoalgebra**

```text
                                    Sorts
Sorts:                    name, text, data, tag, skey, akey < mesg
                          dev, chan, locn < mesg
                                 Operations
{| · |}(·)                mesg × mesg → mesg Encryption
(·, ·)                    mesg × mesg → mesg Pairing
#(·)                      mesg → mesg           Hashing
K(·)                      name → akey           Public key of name
   s
K(·)                      name → akey           s-Public key of name
(·)−1                     akey → akey           Inverse of key
ltk(·, ·)                 name × name → skey Long-term key
                                 Constants
T ags                     tag                   Tag constants
                                 Equations
(a−1 )−1 = a              a : akey
                                 Derivations
m0 , m1 ⊨ {|m0 |}m1       m0 , m1 : mesg        Encryption
m0 , m1 ⊨ (m0 , m1 )      m0 , m1 : mesg        Pairing
(m0 , m1 ) ⊨ {m0 , m1 }   m0 , m1 : mesg        Destructuring
{|m|}k , inv(k) ⊨ m       m, k : mesg           Decryption
m ⊨ #(m)                  m : mesg              Hashing
```

**Table 10.3: cpsa Basic Algebra Syntax; sorts, operators id from Lang field**

```text
 alg    ←    basic
sort    ←    text | data | name | tag | skey | akey
        |    dev | chan | locn | mesg | id
   id   ←    symbol
term    ←    id | (pubk id) | (privk id) | (invk id)
        |    (pubk string id) | (privk string id)
        |    (ltk id id) | string | (cat term+)
        |    (enc term+ term) | (hash term+)
        |    (id term+)
```

#### 10.3.2 The Diffie-Hellman crypto algebra

The Diffie-Hellman crypto algebra refers to the extra features on top of the basic crypto
algebra. It is an order-sorted algebra with signature described in Table 10.4. The algebra is
the free order-sorted algebra generated by the function symbols, sorts, and constants given,
modulo the equations.
    In Section 4.2 we discussed modeling Diffie-Hellman in cpsa, but we said almost nothing
about the expt sort that features prominently in the algebra signature. Our message model
for Diffie-Hellman has two sorts of exponents. The rndx sort is for exponents that are to
be thought of as atomic values. Randomly chosen exponents should always be of this sort,
which is why rndx appears exclusively in our examples, while expt does not. The expt
sort is for compound expressions involving exponents, or values (exp (gen) alpha) that
are received with unconstrained exponent. There may also be variables of this sort, but
they should not first occur in transmissions in protocol roles.
    Table 10.5 describes the grammar for Diffie-Hellman crypto algbera messages in the
input syntax. Symbols in the grammar appearing in the grammar for the basic crypto
algebra retain their same interpretation. Additionally, the gen and one symbols, used as
0-ary function symbols, specify the g and 1 constants, respectively.

**Table 10.4: The Diffie-Hellman Cryptoalgebra**

```text
                                    Sorts
Sorts:                    name, text, data, tag, skey, akey< mesg
                          rndx < expt < mesg
                          dev, chan, locn < mesg
                                 Operations
{| · |}(·)                mesg × mesg → mesg Encryption
(·, ·)                    mesg × mesg → mesg Pairing
#(·)                      mesg → mesg           Hashing
K(·)                      name → akey           Public key of name
   s
K(·)                      name → akey           s-Public key of name
(·)−1                     akey → akey           Inverse of key
ltk(·, ·)                 name × name → skey Long-term key
bltk(·, ·)                name × name → skey Bi-directional LTK
(·)(·)                    base × expt → base    Exponentiation
(··)                      expt × expt → expt Multiplication
i(·)                      expt → expt           Mult. Inverse
                                  Constants
T ags                     mesg                  Tag constants
g                         base                  Generator
1                         expt                  Mult. Identity
                                  Equations
(a−1 )−1 = a                                    a : akey
bltk(a, b) = bltk(b, a)                         a, b : name
xy = yx                   x(yz) = (xy)z         x, y : expt
x1 = x                    x(i(x)) = 1           x : expt
h1 = h                    (hx )y = h(xy)        h : base, x, y : expt
                                 Derivations
m0 , m1 ⊨ {|m0 |}m1       m0 , m1 : mesg        Encryption
m0 , m1 ⊨ (m0 , m1 )      m0 , m1 : mesg        Pairing
(m0 , m1 ) ⊨ {m0 , m1 }   m0 , m1 : mesg        Destructuring
{|m|}k , inv(k) ⊨ m       m, k : mesg           Decryption
m ⊨ #(m)                  m : mesg              Hashing
x, y ⊨ xy                 x, y : expt           Multiplication
x ⊨ i(x)                  x : expt              Inversion
h, x ⊨ hx                 h : base, x : expt    Exponentiation
```

**Table 10.5: cpsa Diffie-Hellman Algebra Syntax**

```text
 alg      ←   diffie-hellman
sort      ←   text | data | name | tag | skey | akey
          |   rndx | expt | dev | chan | locn | mesg | id
   id     ←   symbol
term      ←   id | (pubk id) | (privk id) | (invk id)
          |   (pubk string id) | (privk string id)
          |   (ltk id id) | string | (cat term+)
          |   (enc term+ term) | (hash term+)
          |   (exp term term ) | (gen) | (mul term term)
          |   (rec term) | (one) | (id term+)
```

### 10.4 Declaration syntax

Table 10.6 gives a grammar for the syntax of native and user-defined declarations. For the
purposes of this table, there are two top-level symbols: role-decl and skel-decl.

**Table 10.6: Declaration syntax. See Tables 10.3 and 10.5 for the algebra syntax, which defines the term symbols. See Table 7.1 for formulas conclusion.**

```text
     role-decl       ←   (one-term-decl ht-term+)
                     |   (priority (height integer)+)
                     |   (facts (id term*)*) | (assume conclusion*)
one-term-decl        ←   non-orig | pen-non-orig | uniq-orig | uniq-gen
                     |   conf | auth | gen-st
        height       ←   integer
      ht-term        ←   term | (term height)
     skel-decl       ←   (one-term-decl term+)
                     |   (two-term-decl (term term)+)
                     |   (facts (id term*)*)
                     |   (priority (node integer)+)
          node       ←   (integer integer)
```

### 10.5 Command-line options

The following command-line options are defined for the cpsa program:

   • ‘o’ (“output”) – specifies a file to which the output will be written. Usage: -o FILE
     or –output=FILE.

   • ‘l’ (“limit”) – specifies a step limit (see Section 9.1). By default, the step limit is 2000.
     Usage: -l INT or –limit=INT.

   • ‘d’ (“depth”) – specifies a depth limit (see Section 9.1). The depth limit is infinite by
     default. Usage: -d INT or –depth=INT.

   • ‘b’ (“bound”) – specifies a strand bound (see Section 9.1). By default, the strand
     bound is 12. Usage: -b INT or –bound=INT.

   • ‘m’ (“margin”) – specifies the number of characters allowed per line in the output. By
     default, the margin is 72. Usage: -m INT or –margin=INT.

• ‘e’ (“expand”) – expands macros only. For use in debugging macros; when run with
  this option, the tool does not analyze its input.
• ‘z’ (“noanalyze”) – loads the input but does not analyze. This could be used for
  checking whether any errors are present in the input.
• ‘n’ (“noisochk”) – disable isomorphism checks. Not recommended except in rare
  circumstances. When the tool produces a new skeleton, it only gets a number in the
  output if no isomorphic skeleton has already been found. With isomorphism checking
  disabled, many analyses that otherwise terminate will not terminate. However, there
  is one advantage. Normally, when a skeleton is found more than once in an analysis,
  its operation field (see Section 5.2) is displayed only for the first time that skeleton is
  found. Other instances are not annotated with an operation field but instead simply
  link to the isomorphic skeleton. This usage is largely unnecessary due to the presence
  of the seen-ops field.
• ‘c’ (“check-nonces”) – check nonces first. Normally, the tool will consider the largest
  possible critical term when attempting to solve an unrealized node. This option flips
  the default behavior. Some analyses terminate only with this option, while others
  perform better with this option.
• ‘t’ (“try-old-strands”) – try old strands first. Normally, when there are unrealized
  nodes on multiple strands, the tool will focus on the highest-numbered (rightmost in
  the diagram) strand with unrealized nodes. This option flips the default behavior.
  Some analyses terminate only with this option, while others perform better with this
  option.
• ‘r’ (“reverse-nodes”) – try younger nodes first. Normally, when a strand containing
  unrealized nodes is chosen for analysis, if there are multiple unrealized nodes, the
  earliest (oldest) node is analyzed. This option flips the default behavior. Some
  analyses terminate only with this option, while others perform better with this option.

• ‘g’ (“goals-sat”) – stop when goals are satisfied. Normally, a defgoal is converted to a
  skeleton and analyzed, and only shapes are compared to the goals. With this option
  enabled, the goals are checked against every intermediate skeleton, and branches of
  the analysis in which the goals are satisfied are not further pursued. The output
  analysis will show the skeletons in which the goals were first satisfied, and any shapes
  in which the goals were not satisfied. In a sense, running cpsa with this option asks
  the question: what are all the ways in which this goal may not be satisfied?
• ‘a’ (“algebra”) – sets the algebra to use for the input. Since the basic and diffie-hellman
  algebras have now been joined into a single algebra, this option should be considered
  deprecated. Usage: -a STRING or –algebra=STRING.

   • ‘s’ (“show-algebras”) – causes the tool to print a list of the allowed algebras, instead
     of performing any analysis.

   • ‘h’ (“help”) – causes the tool to print a list of command-line options, and also to
     print the directory in which the package’s documentation exists. When run with this
     option, the tool will not perform any analysis.

   • ‘v’ (“version”) – causes the tool to simply print its version number rather than per-forming
 any analysis.

   Additionally,

   • To protect cpsa against memory exhaustion, run cpsa with the command-line options
     +RTS -M512m -RTS.

   • To make use use of parallelism on an n-processor machine, start cpsa with the
     command-line options +RTS -Nn -RTS.

   See the GHC User’s Guide [15] for documentation on these and other options.

#### 10.5.1 Heralds

At the top of each cpsa input file is, optionally, a herald that is an alternate way to specify
command-line options. All of the examples in the examples directory contain heralds. The
herald, in addition to setting certain options for the analyzer, is also included in the output
file, which may be useful to the analyst in distinguishing one analysis from a similar, related
one.
     Options are included in the herald by constructing an S-expression with first element
equal to the long name of an option, and the second element (if any) set to be the parameter
for that option. For instance, (bound 20) can be included to increase the strand bound for
every run of the analysis without having to add the flag manually.
     Command-line options override the herald. Also, certain command-line options are not
allowed in the herald, specifically, “output”, “help”, “version”, and “show-algebras”.

## Chapter 11: CPSA Tools

This chapter describes programs that complement the cpsa program. All the tools accept a
–help option that describes the tool’s usage and a –version option that prints the version
of the tool.

### 11.1 `cpsa4init`

Populates a directory with files used to create a cpsa project. See Section 2.3.1.

### 11.2 `cpsa4shape`

Cuts down cpsa’s output to only show final results—the shapes.

### 11.3 `cpsa4graph`

Constructs an xhtml document that visualizes the output of a cpsa run or
     the output of cpsa4shape.

### 11.4 `cpsa4goalsat`

Prints the labels of skeletons that do not satisfy a defgoal. See Section 7.1.
     For each point of view skeleton specified by a goal, the program prints a list. The first
     element of the list is the label of the point of view skeleton. The remaining elements
     of the list are labels of the skeletons that do not satisfy the goal.

### 11.5 `cpsa4prot`

Translates protocols expressed in Alice and Bob notation into cpsa’s defprotocol
     syntax. It translates defprot forms, and passes all else through unchanged. The syntax
 of defprot forms is presented in Table 11.1.
     The basic layout of a defprot is a chronological description of things that happen
     in the intended execution of the protocol. The s-expression (msg A B M) is used to
     indicate that role A sends M, while role B receives it. Other features of cpsa4prot are
     given in Table 11.2.

**Table 11.1: defprot Grammar**

```text
   prot     ←    (defprot id alg vars form∗ rule∗ prot-alist)
    vars    ←    (vars vdecl∗)
   form     ←    (msg role role chmsg)
            |    (msg role role chmsg chmsg)
            |    (from role chmsg)
            |    (to role chmsg)
            |    (assume role role-alist)
            |    (clone role role)
chmmsg      ←    (chmsg id term) | (chmsg term) | term
```

**Table 11.2: defprot commands**

```text
      Form                                       Meaning
  (msg A B M)                                 A sends M to B
(msg A B M N)                        A sends M and B receives it as N
   (from A M)                                   A sends M
    (to A M)                                   A receives M
 (assume A M)                      Add the assumption M to the role A
  (clone A B)    Create a role B which includes all behavior described for A to this point.
```

$ cat blanchet.prot
(defprot blanchet basic
```scheme
  (vars (a b akey) (s skey) (d data))
  (msg init resp (enc (enc s (invk a)) b))
  (msg resp init (enc d s))
  (assume init (uniq-orig s))
  (assume resp (uniq-orig d))
  (comment "Blanchet’s protocol"))
```
$ cpsa4prot blanchet.prot
```scheme
(defprotocol blanchet basic
  (defrole init
    (vars (a b akey) (s skey) (d data))
    (trace (send (enc (enc s (invk a)) b)) (recv (enc d s)))
    (uniq-orig s))
  (defrole resp
    (vars (a b akey) (s skey) (d data))
    (trace (recv (enc (enc s (invk a)) b)) (send (enc d s)))
    (uniq-orig d))
  (comment "Blanchet’s protocol"))
```
$
**Figure 11.1: defprot Example**

     See Figure 11.1 for an example.

### 11.6 `cpsa4sas`

Generates Shape Analysis Sentences from the output of cpsa. See Section 7.6.

### 11.7 `cpsa4pp`

Pretty prints cpsa input. It can also be used to translate S-expression syntax
     into json for use with tools written in other languages such as Python.

### 11.8 `cpsa42latex`

Translates cpsa macros specifying message formats into equivalent LATEX
     macros. Algebra primitives such as enc and pubk are mapped to unspecified LATEX
     macros with the same name and arity (sometimes with an optional tag), allowing the
     user to easily customize how they would like these primitives to be typeset.

### 11.9 `cpsa4json`

Translates cpsa input in json syntax into S-expression syntax.

### 11.10 `cpsa4diff`

Compares the skeletons in two files. If a difference is detected, it prints the
     first difference and exits.

## Bibliography
[1] W. Diffie and M. Hellman. New directions in cryptography. IEEE Transactions on
    Information Theory, 22(6):644–654, November 1976.

[2] Shaddin F. Doghmi, Joshua D. Guttman, and F. Javier Thayer. Searching for shapes
    in cryptographic protocols. In Tools and Algorithms for Construction and Analysis of
    Systems (TACAS), number 4424 in LNCS, pages 523–538, 2007.

[3] Daniel Dolev and Andrew Yao. On the security of public-key protocols. IEEE Transactions
 on Information Theory, 29:198–208, 1983.

[4] Joseph A. Goguen and José Meseguer. Order-sorted algebra I: equational deduction
    for multiple inheritance, overloading, exceptions and partial operations. Theoretical
    Computer Science, 105(2):217–273, 1992.

[5] Joshua D. Guttman. State and progress in strand spaces: Proving fair exchange.
    Journal of Automated Reasoning, 48(2):159–195, 2012.

[6] Joshua D. Guttman. Establishing and preserving protocol security goals. Journal of
    Computer Security, 22(2):201–267, 2014.

[7] Joshua D. Guttman, Jonathan C. Herzog, John D. Ramsdell, and Brian T. Sniffen.
    Programming cryptographic protocols. In Rocco De Nicola and Davide Sangiorgi,
    editors, Trust in Global Computing, number 3705 in LNCS, pages 116–145. Springer,
    2005.

[8] Joshua D Guttman, Moses D Liskov, and Paul D Rowe. Security goals and evolving
    standards. In Security Standardisation Research, pages 93–110. Springer, 2014.

[9] Joshua D. Guttman, F. Javier Thayer, Jay A. Carlson, Jonathan C. Herzog, John D.
    Ramsdell, and Brian T. Sniffen. Trust management in strand spaces: A rely-guarantee
    method. In David Schmidt, editor, Programming Languages and Systems: 13th European
 Symposium on Programming, number 2986 in LNCS, pages 325–339. Springer,
    2004.

[10] Gavin Lowe. Breaking and fixing the Needham-Schroeder public-key protocol using
     FDR. In Proceeedings of tacas, volume 1055 of LNCS, pages 147–166, 1996.

[11] Jay A. McCarthy, Shriram Krishnamurthi, Joshua D. Guttman, and John D. Ramsdell.
     Compiling cryptographic protocols for deployment on the web. In World Wide Web
     Conference, pages 687–696. ACM, 2007.

[12] Lawrence C. Paulson. Relations between secrets: Two formal analyses of the Yahalom
     protocol. Journal of Computer Security, 2001.

[13] John D. Ramsdell. Deducing security goals from shape analysis sentences. The MITRE
     Corporation, April 2012. http://arxiv.org/abs/1204.0480.

[14] Paul D. Rowe, Joshua D. Guttman, and Moses D. Liskov. Measuring protocol
     strength with security goals. International Journal of Information Security, 15(6):575–
     596, November 2016. DOI 10.1007/s10207-016-0319-z, http://web.cs.wpi.edu/
     ~guttman/pubs/ijis_measuring-security.pdf.

[15] The GHC Team. GHC user’s guide documentation, release 8.2.1, July 2017. https:
     //downloads.haskell.org/~ghc/latest/docs/users_guide.pdf.
````

---

### `refrences/cpsa_kb/02_manuals/02_Role_Translations_Manual.md`

*sha256:`e36922f0cd30` · 867 lines · 45.7 KB (~11,590 tokens) · lang:`markdown` · 113 control chars sanitized*

````markdown
# CPSA4 Role Translations Manual (`cpsa4roletran`)

*Author: John D. Ramsdell (The MITRE Corporation)*

---

## Table of Contents

- [1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`)](#1-cpsa4-roletran-compiler-user-guide-cpsa4roletran)
  - [1.1 Overview and Natural Role Semantics](#11-overview-and-natural-role-semantics)
  - [1.2 Roletran Input Syntax and Executability Constraints](#12-roletran-input-syntax-and-executability-constraints)
  - [1.3 Annotated Roletran Input Example (`unilateral`)](#13-annotated-roletran-input-example-unilateral)
  - [1.4 Roletran Procedure Output Syntax (`defproc`)](#14-roletran-procedure-output-syntax-defproc)
  - [1.5 Generated Procedure Example (`init` Role)](#15-generated-procedure-example-init-role)
- [2. Role Translations: Formal Semantics and Compilation](#2-role-translations-formal-semantics-and-compilation)
  - [2.1 Introduction and Procedural Role Semantics](#21-introduction-and-procedural-role-semantics)
  - [2.2 Notation](#22-notation)
- [3. Message Algebras for Role Translation](#3-message-algebras-for-role-translation)
  - [3.1 Example Message Algebra (Simple Crypto Algebra)](#31-example-message-algebra-simple-crypto-algebra)
  - [3.2 Encryption-Free Terms and Carried-By Relation](#32-encryption-free-terms-and-carried-by-relation)
- [4. Strand Spaces with Channels](#4-strand-spaces-with-channels)
  - [4.1 Channeled Messages, Traces, and Roles](#41-channeled-messages-traces-and-roles)
  - [4.2 Role Executions and Runs](#42-role-executions-and-runs)
  - [4.3 Unilateral Protocol Example](#43-unilateral-protocol-example)
  - [4.4 Channel Assumptions](#44-channel-assumptions)
- [5. Abstract Execution Semantics](#5-abstract-execution-semantics)
  - [5.1 Runtime Environment, Randomness, and Channel Traces](#51-runtime-environment-randomness-and-channel-traces)
  - [5.2 Abstract Expression and Statement Semantics](#52-abstract-expression-and-statement-semantics)
  - [5.3 Labeled Transition System and Procedure Execution](#53-labeled-transition-system-and-procedure-execution)
  - [5.4 Correctness: Liveness and Safety](#54-correctness-liveness-and-safety)
- [6. Runtime with Probabilistic Encryption (Concrete Message Algebras)](#6-runtime-with-probabilistic-encryption-concrete-message-algebras)
- [7. Concrete Execution Semantics](#7-concrete-execution-semantics)
- [8. Relating Abstract and Concrete Execution Semantics](#8-relating-abstract-and-concrete-execution-semantics)
- [9. Implementation Notes and Epilogue](#9-implementation-notes-and-epilogue)
- [10. References](#10-references)

---

## 1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`)

### 1.1 Overview and Natural Role Semantics

The Cryptographic Protocol Shapes Analyzer (CPSA) attempts to
enumerate all essentially different executions possible for a
cryptographic protocol.  We call them the shapes of the
protocol. Naturally occurring protocols have only finitely many,
indeed very few shapes.  Authentication and secrecy properties are
easy to determine from them, as are attacks and anomalies.

For each input problem, the CPSA program is given some initial
behavior, and it discovers what shapes are compatible with it.
Normally, the initial behavior is from the point of view of one
participant.  The analysis reveals what the other participants must
have done, given the participant's view.  The search is complete,
i.e. we proved every shape can in fact be found in a finite number of
steps, relative to a procedural semantics of protocol roles.

When we say a role has natural role semantics, we mean that there
exists a program that implements the intent of the specified role.
Until now, establishing the correspondence between a CPSA role and its
implementation has been informal.  It requires a programmer that is
well versed in the semantics of CPSA.  As the messages used in roles
become more complex, the likelihood of errors in the correspondence
increases, even when employing the best programmer/CPSA expert.  The
`cpsa4roletran` compiler automates the translation of a CPSA role into
a language independent procedure.  It uses the same algorithms
implemented in CPSA to ensure a faithful translation.

This document describes the use of the compiler.  It assumes the
reader is experienced with CPSA4, version four of CPSA.  This version
of CPSA is required because channels play an essential part in the
translation.

In typical usage, protocols are analyzed using CPSA4 to ensure they
achieve desired security goals before any attempt is made to construct
programs that implement them.

### 1.2 Roletran Input Syntax and Executability Constraints

`cpsa4roletran` translates an annotated CPSA4 role into a language
independent procedure.  The translator consumes the first protocol
that appears in a CPSA4 input file, and ignores everything else in the
file.  Within the protocol, the translators ignores everything but the
protocol name and the role definitions.

There are two syntactic constraints on roles accepted by `cpsa4roletran`.

 * Every messaging event in the trace of a role must occur on a channel.

 * Every role must include two fields particular to `cpsa4roletran`:
   `inputs` and `outputs`.  The `inputs` specify the terms that become
   the formal parameters of the generated procedure.  The `inputs`
   must include all channel variables that occur in the role's trace.
   The `outputs` contain the terms returned by the generated
   procedure.

The params `field` is an alias for the `inputs` field and the
`returns` field is an alias for the `outputs` field.

The translator ignores all fields in a role definition except its
name, `vars`, `trace`, `uniq-orig`, `inputs`, `params`, `outputs`, and
`returns`.

The translator performs various checks to ensure that each role read
is well formed.  It ensures the each term in the inputs is either a
basic value or a channel.  It ensures that any basic value assumed to
be uniquely originating originates in the role's trace, and that no
uniquely originating value is in the inputs.  It ensures that no input
variable is specified as an output.  It also ensures that every
variable in terms that occur in the inputs, outputs, or are assumed to
be uniquely originating also occur in the role's trace.

Finally, a role must be executable.  A role is *executable* iff

 * each transmitted term can be built from the inputs and previously
   sent and received terms;

 * each received term can be destructured into previously seen basic
   values and hashes; and

 * each output term can be build from the inputs and previously sent
   and received terms.

### 1.3 Annotated Roletran Input Example (`unilateral`)

Here is a protocol that performs unilateral authentication.  Its roles
have been annotated for `cpsa4roletran`.

```scheme
(defprotocol unilateral basic
  (defrole init
    (vars (ch chan) (n text) (k akey))
    (trace
     (send ch (enc n k))
     (recv ch n))
    (uniq-orig n)
    (inputs ch k)
    (outputs n))
  (defrole resp
    (vars (ch chan) (n text) (k akey))
    (trace
     (recv ch (enc n k))
     (send ch n))
    (inputs ch (invk k))
    (outputs n)))
```

The initiator role `init` creates a fresh nonce `n` and sends it on
channel `ch` encrypted with public asymmetric key `k`.  To perform the
encryption, the inputs include the key.  The initiator concludes that
it is communicating with a party that possesses the private companion
key by receiving a nonce unencrypted and ensuring it is what it sent.

The responder role `resp` receives the encrypted nonce, and decrypts
with the private key `(invk k)`.  To do the decryption, the inputs
include that key.  In this example, both roles return the nonce for
use by other parts of the program.

### 1.4 Roletran Procedure Output Syntax (`defproc`)

The compiler generates a language independent procedure for each role
in the input protocol.  A user need not understand the details of the
generated code, but a rough understanding can be helpful when the code
generated is unexpected.  It could mean that the CPSA role specifies
something other that what its author intended.

The structure of a generated procedure is:

```scheme
(comment "Role: NAME (FILE_POSITION)")
(defproc NAME (PARAMS) (OUTPUTS) STMTS)
```

where NAME is the name of the role, FILE_POSITION is the location of
the role's definition in the source file, PARAMS are the input
parameters of the procedure, OUTPUTS is the output types of the
procedure, and STMTS is the statements that make up the body of the
procedure.

There are six kinds of statements.

- `(let (VAR TYPE) EXPR)` binds variable VAR to the results of
  expression EXPR.
- `(let (VAR TYPE) (recv CVAR))` binds variable VAR to the results of
  reading a message on channel CVAR.
- `(send CVAR VAR)` transmits the contents of variable VAR on channel
  CVAR.
- `(same VAR1 VAR2)` ensures the contents of VAR1 agrees with what is
  in VAR2.
- `(return VAR ...)` returns the contents of a sequence of variables
  from the procedure.

Finally, there is a comment statement for each message event that
tells where the event being translated occurs in the source file.

Expressions are self explanatory.  They include pairing, projection,
encryption, decryption, hashing, and nonce generation.  The names of
procedures called in expressions include letters that follow the
underscore character which specify type information.  This part of the
procedure name can be safely ignored.

### 1.5 Generated Procedure Example (`init` Role)

The code generated for the `init` role in the unilateral protocol
follows.  Notice how this code agrees with the description of the
role.

```scheme
(comment "Role: init (rtst/unilateral.scm:6:3)")

(defproc init ((p0 chan) (p1 akey)) (text)
  (comment "Send (rtst/unilateral.scm:9:7)")
  (let (v2 text) (frsh_t))
  (let (v3 aenc) (encr_ta v2 p1))
  (send_m p0 v3)
  (comment "Recv (rtst/unilateral.scm:10:7)")
  (let (v4 text) (recv_t p0))
  (same_t v4 v2)
  (return v2))
```

The initiator role `init` creates a fresh nonce `n` (`v2`) and sends
it on channel `ch` (`p0`) encrypted with public asymmetric key `k`
(`p1`).  To perform the encryption, the inputs include the key.  The
initiator concludes that it is communicating with a party that
possesses the private companion key by receiving a nonce unencrypted
(`v4`) and ensuring it is what it sent `(same_t v4 v2)`.

---

## 2. Role Translations: Formal Semantics and Compilation

### 2.1 Introduction and Procedural Role Semantics

The Cryptographic Protocol Shapes Analyzer (cpsa) [8] attempts to enumerate
all essentially different executions possible for a cryptographic protocol. We call
them the shapes of the protocol. Naturally occurring protocols have only finitely
many, indeed very few shapes. Authentication and secrecy properties are easy
to determine from them, as are attacks and anomalies.
    For each input problem, the cpsa program is given some initial behavior,
and it discovers what shapes are compatible with it. Normally, the initial behavior
 is from the point of view of one participant. The analysis reveals what the
other participants must have done, given the participant’s view. The search is
complete, i.e. we proved every shape can in fact be found in a finite number of
steps, relative to a procedural semantics of protocol roles [7].
When we say a role has procedural semantics, we mean that there exists a
program that implements the intent of the specified role. Until now, establishing
 the correspondence between a cpsa role and its implementation has been
informal. It requires a programmer that is well versed in the semantics of cpsa.
As the messages used in roles become more complex, the likelihood of errors in
the correspondence increases, even when employing the best programmer/cpsa
expert. The Roletran compiler automates the translation of a cpsa role into a
procedure that is easily translated into the source for an existing programming
language, in our case, Rust. It uses the same algorithms implemented in cpsa to
ensure a faithful translation. But how do we know its translations are correct?
    Section 4 presents the abstract semantics of procedures used to guide our
implementation of a runtime system for Roletran generated programs. It includes
a definition of correctness, Definition 8, that precisely defines whether the output
of Roletran correctly implements the role it is given.
    The semantics presented in Sect. 4 has been specified in Coq [1]. An attempt
was made to specify the Roletran compiler as a function in Coq and prove that
every output of Roletran correctly implements the role it is given. However,
the proofs turned out to be too complex and challenging, and the attempt was
abandoned.
    As a fallback, one can present Coq with the runtime semantics, a role, and
procedure, and when the procedure is the output of Roletran, Coq will automatically
 prove it correctly implements the role. The Coq automation succeeds on
protocols of substantial size. Thus for high-assurance applications, we provide a
means to validate compiler input/output pairs in lieu of verifying the compiler
algorithm.
    There is one loose end in what might seem to be a tidy story at this
point. Real implementations of cryptographic functions make use of probabilistic
encryption. This means that there may be several bit patterns that correspond
to one encryption term in cpsa. If the compiler generates code that asserts that
two encryptions are equal, the assertion might fail at runtime if the two encryptions
 differ only because of the randomness used to generate them. To explore
these issues, a more concrete semantics has been defined that models randomness
in encryptions. The paper concludes by showing that
1. the concrete semantics is faithful to the abstract semantics, in that for every
   run of the concrete semantics, there is a corresponding run of the abstract
   semantics, and
2. the concrete semantics is adequate with respect to the abstract semantics,
   in that for every run of the abstract semantics and choice of random values,
   there is a corresponding run of the concrete semantics.
      Therefore, probabilistic encryption is handled correctly.

   The Roletran compiler and supporting Coq proofs were written by the author
and the sources are available on GitHub [8]. The sources contain about 5800 lines
of Coq scripts and the Intro module presents an overview of the work.

    There have been a variety of systems that compile high-level descriptions of
protocols into executable code [2,5]. To our knowledge, this is the first example
of a compiler that uses the input of a cryptographic protocol analyzer as its sole
input and honors its semantics.

### 2.2 Notation

**Notation.** A finite sequence f is a function from an initial segment of the natural
numbers. The length of f is |f |, and f = f (0), . . . , f (n − 1) for n = |f |. The
sequence x::f is x, f (0), . . . , f (n−1). The concatenation of sequences f1 and f2
is f1  f2 .
    If S is a set, then S ∗ is the set of finite sequences over S, and S + is the
                                                                   →
                                                                   −
non-empty finite sequences over S. If S is a finite set, then S is some injective
sequence that is onto S. That is, it is a sequence that contains every element in
S without duplicates.
    Suppose g : X  Y is a finite partial function.
                                             
                                               y    if z = x,
                          g[x → y](z) =
                                               g(z) otherwise.

We use ∅ to denote the finite partial function that has an empty domain.

## 3. Message Algebras for Role Translation

This section describes the formalism on which cpsa message algebras are based.
The parameters to an algebra are:

1. a set of messages Alg. The set of messages Alg is the carrier set (or domain)
   of a term algebra.
2. a set of basic values BV ⊂ Alg. Keys and nonces are examples of basic values.
3. a carried by relation ⊆ Alg × Alg. Intuitively, a message t0 is carried by t1
   if it is possible to extract t0 from t1 by someone who knows the relevant
   decryption keys.

### 3.1 Example Message Algebra (Simple Crypto Algebra)

**Example Message Algebra.** The signature of one possible order-sorted [4] message
algebra is in Fig. 1. The algebra is the simplification of the cpsa message algebra
used by the examples in this paper.
     In an order-sorted algebra, each variable x has a unique sort S. The declaration
 of x is x : S.
     The algebra of interest is the order-sorted quotient term algebra generated by
a set of declarations X. The message algebra AlgX is the carrier set for sort M.
The set of basic values BVX is the union of the carrier sets for sorts A, S, and D.
The carrier set for sort A contains the algebra’s asymmetric key pairs. We write
t : S to say that term t is in the carrier set of sort S.
     A variable has no intrinsic sort associated with it. The declarations that
generate an algebra determine the sort of variables that occur within terms of
the algebra. A variable declared to be of sort M is called a message variable.

**Fig. 1. Simple crypto algebra signature**

```text
                Sorts:      M, A, S, D
                Subsorts: A < M, S < M, D < M
                Operations: (·, ·)          : M × M → M Pairing
                            {| · |}(·) : M × M → M Encryption
                            #               :M→M        Hash
                            (·)−1           :M→M        Key inverse
                            τ0 , τ1 , . . . : M         Tag constants
                Equations: (x−1 )−1 = x for x : A; x−1 = x otherwise
```

    The Simple Crypto Algebra is interesting because like cpsa’s message algebra
, any message can be used as a key when constructing an encryption, with
the exception of a message variable. The reason for the exception is that message
variable x could be unified with any basic value, and so what equation applies
to x−1 ?
    Each element of the message algebra is a set of terms. The canonical representative
 of each element is the term with the fewest number of occurrences of the
                     −1
inverse operation (·) . Thus when x is a variable, the canonical representative
of the algebra element that contains
                                          −1 −1
                                   ((x−1 )   )

is x−1 if x : A, and x otherwise. Message t0 occurs in t1 iff the canonical representative
 of t0 is a subterm of the canonical representative of t1 . In what follows,
we conflate each algebra element with its canonical representative.
### 3.2 Encryption-Free Terms and Carried-By Relation

**Definition 1 (Encryption free terms).** Term t is encryption free, written
enc f ree t, iff no encryption term occurs in t.
    A message t0 is carried by t1 , written t0   t1 , if t0 can be derived from t1
given the right set of keys. That is: is the smallest reflexive, transitive relation
such that
                t0 (t0 , t1 ), t1 (t0 , t1 ),  and t0 {|t0 |}t1 .

## 4. Strand Spaces with Channels

The foundation of this work is a version of strand spaces in which messages are
transmitted over channels. This change facilitates the translation of a role into
code by adding a natural handle for performing input and output in generated
code.
    Recall that a strand space [9] is a finite map from a local session of a protocol,
called a strand, to its behavior, called a trace. The addition of channels changes
the standard definition of a trace, but otherwise leaves the basic definitions of
strand space theory unchanged.

    A channel is a variable of sort C. For h : C and t : M, [h, t] associates message
t with channel h, and is called a channeled message. The additions to a message
signature required to support channels follow.

             Extra Sorts: C, CM
             Operation: [·, ·] : C × M → CM       Channeled messages

The sort associated with a channeled message is CM. The carrier set for that
sort is AlgX . Variables of sort CM are not allowed in X. The carrier set for sort
                 
C is ChnX . Let Alg X = AlgX ∪ ChnX .

### 4.1 Channeled Messages, Traces, and Roles

**Traces and Roles.** The behavior of a strand, its trace, is a finite non-empty
sequence of events. An event is either a channeled message transmission or a
channeled message reception. An event transmitting m ∈ AlgX is written as +m;
and an event receiving channeled message m is written as −m. If e = ±[h, t] is
                                                                       +
an event, then msg(e) = t. The set of traces over AlgX is (±AlgX ) .
    A message t originates in trace c at index i iff c(i) = +[h, t1 ], t t1 , and for
all j < i, t msg(c(j)). A message t uniquely originates in strand space Θ iff
it originates in exactly one trace in Θ. A message t is non-originating in strand
space Θ iff it originates in no trace in Θ.
    Structure rX (c, i, o, u) is a role when
                            +
1. c is a trace in (±AlgX ) ,
2. each variable declared in X occurs in c,
3. i ∈ (BVX ∪ ChnX )∗ is a sequence of basic values and channels that specify
   the inputs to the role,
4. o ∈ Alg∗X is a sequence of terms that specify the outputs of the role, and
5. u ⊆ BVX is a set of basic values that originate in c.
The elements of i and o are a sequence because the order matters when generating
a procedure from the role. Elements of u are freshly generated when the compiled
role executes.

### 4.2 Role Executions and Runs

**Executions.** An execution eY (c, i, o, u) is similar to a role except that its uniquely
originating values are a sequence, not a set. The semantics of an execution
requires that the fresh values be presented in the order in which they are consumed
. Otherwise, the components of an execution must satisfy the same con-
                  
straints. Let φ : Alg     
                      X → AlgY be a homomorphism, and φ̄ be the extension of φ
to traces and sequences of terms in the obvious way.

**Definition 2 (Run of a role).** Execution eY (c , i , o , u ) is a run of role
rX (c, i, o, u) iff there exists a homomorphism φ such that φ̄(c) = c , φ̄(i) = i ,
φ̄(o) = o , φ̄(u) = u , and u is some sequence that contains the elements in u.

   The strand spaces model of a protocol execution is a bundle. A bundle adds
a communication relation to a strand space, and constraints that ensure that
causality is respected in that every received message is transmitted previously

in the bundle. In strand spaces, a Dolev-Yao adversary [3] is modeled by strands
in a bundle along with the strands derived from the protocol being analyzed.
    cpsa does not represent executions using bundles or adversarial behavior
using strands. Instead, it uses a skeleton to represent a collection of bundles. A
skeleton has a strand space, an ordering relation between events, and some origination
 assumptions that must be satisfied by the strand space of the skeleton.
A bundle is modeled by a skeleton if it contains all of the structure specified by
the skeleton, in other words, there is a homomorphism from the skeleton into
the bundle.
    For each input problem, cpsa is given some initial behavior, and it discovers
what shapes are compatible with it. A shape is a special kind of skeleton in that
it contains enough protocol behavior to explain all message receptions in the
presence of adversarial behavior, and it is minimal in that if there is a homomorphism
 from another skeleton to the shape, then there is a homomorphism
from the shape to the other skeleton.
    To describe the executions of a protocol, each strand in a skeleton must be
an instance of some role in the protocol, which is defined to mean there is a
homomorphism from the role to the strand. The definition of a run of a role
codifies that link for procedure execution semantics.

### 4.3 Unilateral Protocol Example

The Unilateral Protocol is a very simple authentication protocol. It consists of
two roles, an initiator and a responder. The initiator encrypts a freshly chosen
nonce using the public key of the responder and sends it. The responder decrypts
the encryption it receives using its private key, and transmits the plaintext. If the
initiator receives the nonce it sent unencrypted, it concludes it is communicating
with a responder that possesses the corresponding private key, assuming the
private key has not been compromised. In the notation presented above, the
protocol is specified as follows.
**Example 3 (Unilateral Protocol)**
             init = rh:C,n:D,k:A (+[h, {|n|}k ], −[h, n], h, k, n, {n})
            resp = rh:C,n:D,k:A (−[h, {|n|}k ], +[h, n], h, k −1 , n, {})
    Both the initiator and the responder use a message algebra generated by
a channel h, a datum n, and an asymmetric key k. The trace of the initiator
contains two events, a channeled message transmission followed by a channeled
message reception. The inputs to the initiator are a channel and the public part
of a key pair. The inputs to the responder are a channel and the private part
of a key pair. The outputs produced by both roles is the single nonce n. The
initiator freshly generates nonce n, and the responder freshly generates nothing.
    cpsa determines that if an instance of an initiator role runs to completion,
and the private part of the key pair is not compromised, i.e. is non-originating,
then there must have been a corresponding run of the responder role that agrees
with the initiator on the values of the nonce and the public key.

### 4.4 Channel Assumptions

With the addition of channels to cpsa, skeletons now include additional kinds of
assumptions besides origination assumptions. A channel can be assumed to be
authenticated and/or confidential. In a bundle, when a channel is authenticated,
the adversary is not allowed to transmit a message on the channel, and when
it is confidential, the adversary is not allowed to received a message on the
channel. The addition of channel assumptions allows interesting new analyses of
protocols, but does not impact Roletran, so it will not be further discussed.

## 5. Abstract Execution Semantics

### 5.1 Runtime Environment, Randomness, and Channel Traces

Roletran generates a procedure for each role in a protocol. To build an executable
program, the procedure is trivially translated into source code for an existing
programming language, in our case Rust. The code is compiled and linked with
a runtime system. The implementer of the program provides a main routine that
invokes the procedure with inputs that must be compatible with inputs of the
translated role. We trust the implementor to do so.
     When the program executes, it goes through state changes associated with
each statement generated by Roletran. The abstract execution semantics specifies
 an abstract view of properties of the states that must be preserved in order
to be in compliance with the execution semantics stated in the previous section.
     When the compiled translation of a role is executing, the runtime system
for the source language maintains a binding between program variables and
binary objects that represent message fragments. The abstract execution semantics
 models these bindings with a map from program variables to terms in the
message algebra. This map is called an environment. The implementor of the
runtime library must ensure that each binary object naturally abstracts into the
corresponding term in the message algebra as specified by the current environment
.
     A runtime system for a program provides two more capabilities, support for
sending and receiving messages on channels, and freshly generating random values
. To model freshly generating random values, the abstract execution semantics
maintains a sequence of basic values that is the source of randomness. Initially
it is the sequence of uniquely originating values in an execution. The implementor
 of the runtime library must ensure each binary object it creates naturally
abstracts into the corresponding term in the message algebra as specified by the
abstract execution semantics.
     To model messaging on channels, the abstract execution semantics maintains
a trace that initially is the trace in the execution. The implementor of the runtime
 library must ensure each binary object transmitted or received naturally
abstracts into the corresponding event over the message algebra as specified by
the abstract execution semantics.

### 5.2 Abstract Expression and Statement Semantics

**Fig. 2. Abstract execution expression semantics**

```text
             ae :       Alg Y environment
                           ∗
                × (±AlgY ) input trace
                      ∗
                × AlgY        input fresh values
                ×E            expression
                × AlgY        value
                           ∗
                × (±AlgY ) output trace
                × Alg∗Y       output fresh values

                  ae(E, c, u, quot(τ ) , τ, c, u)                     (1)

                 E(v1 ) = t1        E(v2 ) = t2
                                                                      (2)
             ae(E, c, u, pair(v1 , v2 ) , (t1 , t2 ), c, u)

                  E(v1 ) = t1       E(v2 ) = t2
                                                                      (3)
             ae(E, c, u, encr(v1 , v2 ) , {|t1 |}t2 , c, u)
                           E(v1 ) = t1
                                                                      (4)
                ae(E, c, u, hash(v1 ) , #t1 , c, u)

                        E(v1 ) = (t1 , t2 )
                                                                      (5)
                  ae(E, c, u, frst(v1 ) , t1 , c, u)
                        E(v1 ) = (t1 , t2 )
                                                                      (6)
                 ae(E, c, u, scnd(v1 ) , t2 , c, u)

        E(v1 ) = {|t1 |}t2 E(v2 ) = t2 −1 enc free t2 −1
                                                                      (7)
               ae(E, c, u, decr(v1 , v2 ) , t1 , c, u)
                            E(v1 ) = h
                                                                      (8)
             ae(E, −[h, t] :: c, u, recv(v1 ) , t, c, u)

                   ae(E, c, t :: u, frsh , t, c, u)                   (9)
```

    The output of the compiler is an executable procedure x(p, s), where p is
a sequence of parameters and s is a sequence of statements. Each parameter
is a program variable and its type, and is associated with an input when the
procedure is invoked. A type is one of M, A, I, S, D, and C.
    The code generated by the compiler is a sequence of statements. Let V be
the syntactic category for program variables. The syntax of a statement is

```text
        S :: = V : T ← E | V ≈ V | invp(V, V) | send(V, V) | return(V ∗ )
        T :: = M | A | I | S | D | C
        E :: = quot(τ ) | pair(V, V) | encr(V, V) | hash(V)
            | frst(V) | scnd(V) | decr(V, V) | recv(V) | frsh
```

**Fig. 3. Abstract execution statement semantics**

```text
                as :      AlgY input environment
                             ∗
                   × (±AlgY ) input trace
                        ∗
                   × AlgY      input fresh values
                   ×S          statement
                   ×      AlgY output environment
                             ∗
                   × (±AlgY ) output trace
                        ∗
                   × AlgY      output fresh values

                ae(E, c1 , u1 , x, t, c2 , u2 ) chk (t, k)
                                                                                     (10)
             as(E, c1 , u1 , v : k ← x , E[v       t], c2 , u2 )

               chk (t, M) always true
               chk (t, A) iff t is a variable of sort A
               chk (t, I) iff t−1 is a variable of sort A
                                                                                     (11)
               chk (t, S) iff t is a variable of sort S
               chk (t, D) iff t is a variable of sort D
               chk (t, C) iff t is a variable of sort C
                   E(v1 ) = E(v2 ) enc free E(v1 )
                                                                                     (12)
                    as(E, c, u, v1 ≈ v2 , E, c, u)

                  E(v1 ) = E(v2 )−1 enc free E(v1 )
                                                                                     (13)
                  as(E, c, u, invp(v1 , v2 ) , E, c, u)
                      E(v1 ) = h E(v2 ) = t
                                                                                     (14)
             as(E, +[h, t] :: c, u, send(v1 , v2 ) , E, c, u)

                            as∗(E, , , , E )                                         (15)

         as(E1 , c1 , u1 , x, E2 , c2 , u2 ) as∗(E2 , c2 , u2 , s, E3 )
                                                                                     (16)
                         as∗(E1 , c1 , u1 , x :: s, E3 )
```

    At runtime, a program variable is associated with an element of a message
algebra. This association is represented by an environment E :V  Alg    Y , a finite
partial function. The semantics of a sequence of statements is specified using the
                                                                                   ∗
relation asret(E, c, u, s, o), where E is an environment, c is a trace in (±AlgY ) ,
u is a sequence of fresh terms in Alg∗Y , s is a sequence of statements, and o is a
sequence of outputs in Alg∗Y .

                 as∗(E, c, u, s, E  ) E  ◦ v0 , v1 , . . . = t0 , t1 , . . .
                                                                                           (17)
                 asret(E, c, u, s return(v0 , v1 , . . .), t0 , t1 , . . .)

The semantics of the remaining statements are given in Fig. 3. The semantics of
expressions are given in Fig. 2. Note that Eq. 7, 12, and 13 make assertions that
some terms must be free of encryptions. the purpose of these restrictions has to do with the correct handling of probabilistic encryption and will be explained in
Sect. 7.
### 5.3 Labeled Transition System and Procedure Execution

The intuition behind the semantics can be gleaned from the statement semantics
 as in Fig. 3. Think of an environment, trace, fresh values triple (E, c, u) as
a state, and a statement as a label. Figure 3 specifies a labeled transition system
. It defines how the states evolve during the course of an execution. For a
sameness test v1 ≈ v2  (Eq. 12), the state does not change. Execution halts
if the test fails. For a send statement send(v1 , v2 ) (Eq. 14), only the trace is
updated. For a bind statement v : k ← x (Eq. 10), all three components of the
state are updated as determined by the expression semantics ae. The trace is
changed only in response to a recv(v1 ) expression (Eq. 8), and a fresh value
is consumed only in response to a frsh expression (Eq. 9). Sequences of state
transitions are tied together in the natural way by as∗ (Eqs. 15 and 16). The
asret predicate (Eq. 17) ensures that the final statement in a procedure is a
return statement, and that the outputs of the procedure are correctly retrieved
from the final environment.
**Definition 4 (Procedure execution).** Let p = (v0 , k0 ), . . . , (vn−1 , kn−1 )
and i = i0 , . . . , in−1 . Execution e = eY (c, i, o, u) is an execution of procedure
x = x(p, s), written exec(x, e), iff
1. for all j < n, chk (ij , kj ), and
2. asret(E, c, u, s, o), where E = ∅[v0 → i0 ] · · · [vn−1 → in−1 ].
See Eq. 11 for the definition of chk .
      Roletran generates the following procedures for the Unilateral Protocol.
**Example 5 (Unilateral Protocol Procedures)**
          initp = x((v0 , C), (v1 , A),      respp = x((v0 , C), (v1 , I),
                    v2 : D ← frsh                        v2 : M ← recv(v0 )
                    v3 : M ← encr(v2 , v1 )              v3 : D ← decr(v2 , v1 )
                    send(v0 , v3 )                       send(v0 , v3 )
                    v4 : D ← recv(v0 )                   return(v3 ))
                    v2 ≈ v4
                    return(v2 ))

   The execution inite = eh:C,n:D,k:A (+[h, {|n|}k ], −[h, n], h, k, n, n) is an
execution of procedure initp. The state transitions caused by this execution of
procedure initp are shown in Fig. 4.

### 5.4 Correctness: Liveness and Safety

**Definition 6 (Liveness).** Procedure x is live for role r, iff there exists an execution
 e such that

1. e is a run of r, and
2. e is an execution of x.

**Definition 7 (Safety).** Procedure x is safe for role r, iff when

1. e is an execution of x, then
2. e is a run of r.

**Definition 8 (Correctness).** Procedure x correctly implements role r, iff x is
live and safe for r.

    The Coq scripts that come with Roletran automatically prove that the Uni-lateral
 Protocol procedures it generates correctly implement their respective
roles.
    Consider the case in which Roletran mistakenly omitted the sameness test
(v2 ≈ v4 ) in the initiator procedure. The Coq scripts would determine that
ec:C,n,n :D,k:A (+[h, {|n|}k ], −[h, n ], h, k, n, n) is an execution of procedure
initp , but note that this execution violates the safety condition. The safety
condition ensures that runs of a collection of procedures that correctly implement
the roles of a protocol achieve the security goals of the protocol.

## 6. Runtime with Probabilistic Encryption (Concrete Message Algebras)

This section presents message algebras, called concrete message algebras, that
are very similar to the ones used by the abstract execution semantics. The only
difference is the way in which they model encryption. The signature used by the
previous algebras has one operation for encryption, {|(·)|}(·) (See Fig. 1), which
suggests that two encryptions are the same if the plaintext and the key used to
construct them are the same. This is not true for implementations of encryption
in actual use. Instead, some randomness is added to an encryption during its
construction in such a way that knowledge of the randomness is not needed to
recover the plaintext by someone in possession of the decryption key.

    Figure 5 shows the signature used for concrete algebras that model probabilistic
 encryption. This signature features a family of encryption operations,
{(·)}i(·) , one for each natural number i. The natural number is meant to represent
 the randomness used while creating the encryption. In concrete algebras,
two encryptions created with the same plaintext and key are equal only if they
were created using the same random value.
    The algebra of interest is the order-sorted quotient term algebra generated by
a set of declarations Y . The message algebra CAlgY is the carrier set for sort M.
The definitions of traces, roles, and executions, extend to concrete algebras in
the obvious ways.

**Definition 9 (Forgetful function).** Let F : CAlgY → AlgY be the obvious
function that forgets the randomness used to create encryptions.

**Lemma 10.** For x ∈ AlgY , if x is encryption free (enc f ree x), then there
exists a unique y ∈ AlgY such that F(y) = x.

Proof. By induction on the structure of y.

      The lemma used in proofs follows.
**Lemma 11.** For x, y ∈ CAlgY , if enc free(F(x)) and F(x) = F(y), then x = y.

## 7. Concrete Execution Semantics

The concrete execution semantics is analogous to the abstract execution semantics
 except that references to message algebras are replaced with references to
concrete message algebras. There is one big exception. When executing an encr
expression, there must be a source of randomness for use in creating an encryption
. To provide a source of fresh basic values, the abstract execution semantics
 threads a sequence of values through state changes. In the concrete execution
 semantics, a sequence of natural numbers γ is also threaded through state
changes and used to create encryptions.

                              E(v1 ) = t1         E(v2 ) = t2
                                                                                 (18)
                   ce(E, c, u, ι :: γ, encr(v1 , v2 ), {t1 }ιt2 , c, u, γ)

                              E(v1 ) = t1        E(v2 ) = t2
                                                                                      (19)
                     ce(E, c, u, , encr(v1 , v2 ), {t1 }0t2 , c, u, )
Equation 19 handles the case in which the source of randomness has been
exhausted.
   Other than the case for the encr expression, the definition of the concrete execution
 semantics follows that of the abstract execution semantics in the obvious
ways.
**Definition 12 (Concrete procedure execution)**
Assume p = (v0 , k0 ), . . . , (vn−1 , kn−1 ) and i = i0 , . . . , in−1 . Execution e =
eY (c , i , o , u ) is a concrete execution of procedure x = x(p, s) with randomness
 γ, written cexec(x, e, γ), iff
1. for all j < n, chk (F(ij ), kj );
2. csret(E, c, u, γ, s, o), where E = ∅[v0 → i0 ] · · · [vn−1 → in−1 ];
3. c is the result of mapping c using F;
4. i = F ◦ i;
5. o = F ◦ o; and
6. u = F ◦ u.

## 8. Relating Abstract and Concrete Execution Semantics

The proofs of the theorems stated in this section were performed using Coq and
the proof scripts are available in the distribution of cpsa [8].
**Theorem 13 (Faithfulness).** cexec(x, e, γ) implies exec(x, e).
    The proof of faithfulness is tedious but straightforward. The forgetful function
 in Definition 9 is used to map items in the concrete semantics to items in
the abstract semantics, and then the proofs go through as expected.
**Theorem 14 (Adequacy).** exec(x, e) implies cexec(x, e, γ).
    The proof of adequacy is tricky. Where there is a sequence of state transitions
in the abstract execution semantics, one must find a corresponding sequence
in the concrete execution semantics. During both sequences, an event in the
trace is consumed when a send statement or a receive expression is encountered.
The case of a receive expression is the easy situation. The received term in the
complex algebra can be any term as long as applying the forgetful function
to it produces the received term in the abstract algebra. However, the case
of a send statement is quite different. The transmitted term in the complex
algebra must agree with what is in the environment associated with the send
statement’s message variable. And the term in the environment depends on the
particular sequence of random values consumed up to this point in the execution.
Engineering a proof that maintains this property is what makes the proof tricky.
    The proof of adequacy makes demands on both the abstract and concrete
execution semantics. The proof depends on the fact that the following terms
must not contain an encryption,

– the key used during a decryption (see Eq. 7),
– the terms compared with a sameness test (see Eq. 12), and
– the terms compared with an inverse key predicate test (see Eq. 13).
The lack of encryptions allow the use of Lemma 11.
   With these checks in place, the means we use to validate compiler
input/output pairs correctly handles probabilistic encryption.

## 9. Implementation Notes and Epilogue

The development of the Roletran compiler is part of a project aimed at addressing
 the fact that there are systems built on aging software components with
questionable security. An approach to protecting such systems is to isolate each
component, and mediate communication between the components using trusted
software that achieves desired security goals. Verified implementations of protocols
 is a key component to our approach. Members of this project include Ian
D. Kretz and Dan J. Dougherty. The project is led by Joshua D. Guttman.
    The project has developed a runtime system in Rust for code generated by
Roletran, and several test protocols have been analyzed and then translated
into running code, the simplest of which is the Unilateral Protocol. The project
has another compiler that compiles protocols that make use of state. Future
work might include the construction of a verified runtime system for Roletran
generated code.
    The addition of channels to cpsa was due to yet another successful collaboration
 between Joshua and the author.

Acknowledgement. Paul D. Rowe provided valuable comments that improved this
paper.

## 10. References
1. The Coq proof assistant reference manual (2021). http://coq.inria.fr
2. Bhargavan, K., Corin, R., Deniélou, P., Fournet, C., Leifer, J.J.: Cryptographic
   protocol synthesis and verification for multiparty sessions. In: Proceedings of the
   22nd IEEE Computer Security Foundations Symposium, CSF 2009, Port Jefferson,
   New York, USA, 8–10 July 2009, pp. 124–140. IEEE Computer Society (2009).
   https://doi.org/10.1109/CSF.2009.26
3. Dolev, D., Yao, A.C.: On the security of public key protocols. IEEE Trans. Inf.
   Theory 29(2), 198–207 (1983). https://doi.org/10.1109/TIT.1983.1056650
4. Goguen, J.A., Meseguer, J.: Order-sorted algebra I: equational deduction for multiple
 inheritance, overloading, exceptions and partial operations. Theor. Comput.
   Sci. 105(2), 217–273 (1992). https://citeseer.ist.psu.edu/goguen92ordersorted.html
5. Guttman, J.D., Herzog, J.C., Ramsdell, J.D., Sniffen, B.T.: Programming cryptographic
 protocols. In: De Nicola, R., Sangiorgi, D. (eds.) TGC 2005. LNCS, vol. 3705,
   pp. 116–145. Springer, Heidelberg (2005). https://doi.org/10.1007/11580850 8
6. Guttman, J.D., Wand, M.: VLISP: a verified implementation of scheme. Lisp Symbolic
 Comput. 8, 5–32 (1995). https://doi.org/10.1007/BF01128406

7. Liskov, M.D., Rowe, P.D., Thayer, F.J.: Completeness of CPSA. Technical
   report, MTR110479, The MITRE Corporation (2011). https://www.mitre.org/
   publications/technical-papers/completeness-of-cpsa
8. Ramsdell, J.D., Guttman, J.D.: CPSA4: A cryptographic protocol shapes analyzer.
   The MITRE Corporation (2018). https://github.com/mitre/cpsaexp
9. Thayer, F.J., Herzog, J.C., Guttman, J.D.: Strand spaces: proving security protocols
 correct. J. Comput. Secur. 7(1), 191–230 (1999). http://content.iospress.com/
   articles/journal-of-computer-security/jcs117
````

---

### `refrences/cpsa_kb/02_manuals/03_CPSA_Primer.md`

*sha256:`3b12073cc9f8` · 1302 lines · 67.7 KB (~17,216 tokens) · lang:`markdown`*

````markdown
# CPSA Primer: Modeling Methodology, Core Concepts, and Foundations

*Authors: John D. Ramsdell, Joshua D. Guttman (The MITRE Corporation, CPSA Version 4.4)*

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Overview and Workflow](#2-overview-and-workflow)
- [3. Basic Crypto Algebra (BCA) Messages](#3-basic-crypto-algebra-bca-messages)
  - [3.1 The Carries Relation (`carries`)](#31-the-carries-relation-carries)
- [4. Protocols and Roles](#4-protocols-and-roles)
- [5. Protocol Executions and Origination Assumptions](#5-protocol-executions-and-origination-assumptions)
  - [5.1 Origination and Channel Assumptions (`non-orig`, `pen-non-orig`, `uniq-orig`, `auth`, `conf`)](#51-origination-and-channel-assumptions-non-orig-pen-non-orig-uniq-orig-auth-conf)
- [6. Skeletons, Homomorphisms, and Refinements](#6-skeletons-homomorphisms-and-refinements)
  - [6.1 Realized Skeletons](#61-realized-skeletons)
  - [6.2 Structural and Message Refinement (Homomorphisms)](#62-structural-and-message-refinement-homomorphisms)
- [7. Listeners](#7-listeners)
- [8. Authentication Tests](#8-authentication-tests)
- [9. Generalization and Shapes](#9-generalization-and-shapes)
- [10. Skeleton Input Syntax (`defskeleton`)](#10-skeleton-input-syntax-defskeleton)
  - [10.1 Semantic Errors and Well-Formedness Checks](#101-semantic-errors-and-well-formedness-checks)
  - [10.2 Needham-Schroeder Input Example](#102-needham-schroeder-input-example)
- [11. Output Format and Annotations](#11-output-format-and-annotations)
  - [11.0.1 Interpreting the `operation` Field](#1101-interpreting-the-operation-field)
  - [11.1 Needham-Schroeder Complete Output Trace](#111-needham-schroeder-complete-output-trace)
- [12. Security Goals and Rules](#12-security-goals-and-rules)
- [13. Macros (`defmacro`)](#13-macros-defmacro)
- [14. File Includes (`include`)](#14-file-includes-include)
- [15. Algebra Signature Extensions (`lang`)](#15-algebra-signature-extensions-lang)
- [16. Modeling Methodology and Advice](#16-modeling-methodology-and-advice)
  - [16.1 Role vs. Skeleton Origination Assumptions](#161-role-vs-skeleton-origination-assumptions)
  - [16.2 Distinguishing `text` vs. `data` Sorts](#162-distinguishing-text-vs-data-sorts)
  - [16.3 Shape Interpretation and Authentication Test Debugging](#163-shape-interpretation-and-authentication-test-debugging)
  - [16.4 Progressive Refinement Analysis Technique](#164-progressive-refinement-analysis-technique)
  - [16.5 Resource Bounds and Handling Non-Termination](#165-resource-bounds-and-handling-non-termination)
- [17. Formula Extraction (`cpsa4sas`)](#17-formula-extraction-cpsa4sas)
- [Appendix A: BCA Syntax Reference](#appendix-a-bca-syntax-reference)
- [Appendix B: Omitted Executions and Natural Role Semantics](#appendix-b-omitted-executions-and-natural-role-semantics)
- [References](#references)

---

## 1. Introduction

Analyzing a cryptographic protocol means finding out what security
properties—essentially, authentication and secrecy properties—are true in
all its possible executions. Protocol analysis is hard because an adversary
can often manipulate the regular, law-abiding participants. The adversary
may be able to manipulate the regular participants into an unexpected execution
, breaking a secrecy or authentication property that the protocol was
intended to ensure.
    cpsa, The Cryptographic Protocol Shapes Analyzer, is a software tool.
Given a protocol definition and some assumptions about executions, it attempts
 to produce descriptions of all possible executions of the protocol compatible
 with the assumptions. Naturally, there are infinitely many possible
executions of a useful protocol, since different participants can run it with
varying parameters, and the participants can run it repeatedly.
    However, for many naturally occurring protocols, there are only finitely
many of these runs that are essentially different. Indeed, there are frequently
very few, often just one or two, even in cases where the protocol is flawed.
We call these essentially different executions the shapes of the protocol. Authentication
 and secrecy properties are easy to “read off” from the shapes,
as are attacks and anomalies.
    The purpose of this document is to provide the background required to
make effective use of a cpsa software distribution. In particular, the advice
in Section 16 is essential reading.
    The cpsa program reads a sequence of problem descriptions, and prints
the steps it used to solve each problem. Each input problem contains some
initial behavior, together with assumptions about some uncompromised keys
and freshly chosen values. cpsa discovers what shapes are compatible with
this problem description. Normally, the initial behavior is a local run of
one participant, so that the problem is to see what possible executions exist
from that participant’s “point of view.” The analysis reveals what the other
participants must have done, given the first participant’s view.
    The shapes analysis is performed within a pure Dolev-Yao model [3].
cpsa’s search is based on a high-level algorithm that was claimed to be complete
, i.e. every shape can in fact be found in a finite number of steps [2, 5].
Further theoretical work showed classes of executions that are not found by
the algorithm, however it also showed that every omitted execution requires
an unnatural interpretation of a protocol’s roles. Hence the algorithm is

complete relative to natural role semantics. Appendix B discusses omitted
executions.

## 2. Overview and Workflow

A cpsa release includes several programs, an analyzer, and various tools used
to interpret the results. The analyzer, cpsa, provides support for several algebras
, one of which is the Basic Crypto Algebra. Programs that assist in
the interpretation of results are cpsashapes and cpsagraph. The analyzer
prints the steps it used to solve each problem. The cpsashapes program
extracts the shapes discovered by an analyzer run. The cpsagraph program
 graphs both forms of output using Scalable Vector Graphics (svg). A
standards-compliant browser such as FireFox or Safari displays the generated
diagrams.
    The expected work flow follows. An analysis problem is entered using an
ordinary text editor, preferably one with support for Lisp syntax. Problem
statement errors in the input are detected by running the analyzer. Many
error reports are of the form that allow editors such as Emacs to move its
cursor to location of the problem.
    There are two classes of problem statement errors: syntax and semantic
errors. Correcting syntax errors is straightforward, but correcting semantic
errors requires an understanding of the core data structures. Section 10.1
describes their correction.
    Once the problem statement errors have been eliminated, the analyzer
should produce useful output as a text document. The text document contains
 each step used to derive a shape from a problem statement. It is
common to filter the output using the cpsashapes program, and look only
at the computed shapes associated with each problem statement.
    The cpsagraph program is applied to the output to produce a more readable
, hyperlinked xhtml document that can be displayed in a standardscompliant
 web browser. The cpsa User Guide contains the up-to-date de-scription
 of cpsagraph generated documents. The guide is also the place to
find command-line usage information for all programs in a release. The user
guide is an xhtml document delivered with the software.
    The cpsa program uses S-expressions for both input and output. Sexpression
 is an abbreviation for a Symbolic Expression of Lisp fame, and is
described in Appendix A.

    The input may optionally start with a herald form. The form contains
a title for the run and an association list. The association list allows options
normally specified on the command line to be specified within an input file.
In the following example, the herald form specifies a strand bound of 12 in a
way that is equivalent to the command line option --bound=12.

      (herald Needham-Schroeder (bound 12))

    The body of the input consists of two forms: protocol definitions and
initial behavior descriptions. The exact details of both forms depend on
the message algebra specified by the protocol. Protocols that specify basic
as their algebra get an implementation of the Basic Crypto Algebra (bca)
described in the next section. A complete grammar for cpsa input with bca
protocols is displayed in Table 2 on Page 33.

## 3. Basic Crypto Algebra (BCA) Messages

Each message exchanged in a protocol is represented by a term. Terms represent
 atomic values such as text objects, principal names, and asymmetric
and symmetric keys. They also represent values composed from other values
via encryption and concatenation.
    A sort system is used to classify terms. A cpsa message algebra is an
order-sorted algebra [4] with restrictions, hence the use of the word sort
instead of type. Other aspects of cpsa’s use of order-sorted algebras is
beyond the scope of this paper.
    The sorts that correspond to the atomic values are the base sorts—for
bca they are text, data, name, akey, and skey. The non-base sort is mesg.
Every term is of sort mesg, and every one of the other sorts is a subsort
of mesg.
    The simplest term is a variable, which syntactically is a symbol as de-scribed
 in Appendix A. Internally, each variable has a sort, so the sort of
each variable in the input must be declared in a vars form, such as:

```scheme
                  (vars (t text) (n name) (k akey)).
```

   Asymmetric keys come in pairs related by the invk operator. If t is a
term of sort akey, so is (invk t). Furthermore, (invk (invk t)) is equated
with t. A name can be used to identify an asymmetric key pair using the

pubk and privk operators, as in (pubk n) and (privk n)—the latter is
interpreted as (invk (pubk n)). A name may be associated with more
than one key using the binary form of pubk, where the first argument is a
quoted constant, as in (pubk "sig" n) and (pubk "enc" n). Two names
can be used to identify a long term symmetric key with the ltk operator.
    Terms formed from base sorted variables, and the operators invk, pubk,
privk, and ltk are called atoms, because each one represents an atomic
value. A key property of an atom is that the receiver of an atom carried in
a message term cannot decompose the atom into parts. For example, the
reception of a message that consists of the atom (invk k) does not allow its
receiver to deduce k. Within this document, S-expression syntax will often,
for the sake of readability, be replaced by the traditional notation for terms.
Thus (invk k) will be written as K −1 , and (pubk n) as KN .
    The terms in this algebra are freely generated from the atoms, tags, concatenation
, encryption, and hashing. A tag is a quoted constant. The concatenation
 of terms t and t′ is t, t′ in traditional infix notation and (cat t t′ )
in S-expression syntax. The comma operator is right associative and (cat a
b c d) is equivalent to (cat a (cat b (cat c d))). Given t, the term to
be protected, and key term k, the encryption of t using k is {|t|}k in traditional
 notation and (enc t k) in S-expression syntax. The term represents
asymmetric encryption when the key is of sort akey, otherwise it represents
symmetric encryption. Additionally, (enc a b c d k) is equivalent to (enc
(cat a b c d) k). Given t, the term to be hashed, its hash is #t in traditional
 notation and (hash t) in S-expression syntax. cpsa treats a hashed
term as if it were an encryption in which the term that is hashed is the
encryption key. As with encryption, (hash a b c d) is equivalent to hash
(cat a b c d)). Figure 2 on Page 8 contains examples of bca message
terms. Also see term in Table 2, Appendix A.
### 3.1 The Carries Relation (`carries`)

A message term carries a subterm of the message if the possession of the
right set of keys allows the extraction of the subterm. The carries relation is
the least relation such that (1) t carries t, (2) {|t0 |}t1 carries t if t0 carries t,
and (3) t0 , t1 carries t if t0 or t1 carries t. As noted above, the message k −1
does not carry k. Also, {|t|}k does not carry k unless (anomalously) t carries k.

## 4. Protocols and Roles

A protocol defines the patterns of allowed behavior for non-adversarial participants
. In other words, the behavior of each participant must be an instance
of some protocol template, called a role. Figure 1 displays the roles that
make up the Needham-Schroeder protocol.

            init     {|N1 , A|}KB             {|N1 , A|}KB    resp

             •       {|N1 , N2 |}KA          {|N1 , N2 |}KA    •

             •       {|N2 |}KB                   {|N2 |}KB     •
**Figure 1: Needham-Schroeder Initiator and Responder Roles**

```scheme
     (defrole resp (vars (b a name) (n2 n1 text))
       (trace (recv (enc n1 a (pubk b)))
              (send (enc n1 n2 (pubk a)))
              (recv (enc n2 (pubk b)))))
```
**Figure 2: Needham-Schroeder Responder Role**

    In S-expression syntax, a protocol is a named set of roles and is defined
by the defprotocol form. See protocol in Table 2, Appendix A.
```scheme
                           (defprotocol ns basic
                             (defrole init . . . )
                             (defrole resp . . . ))
```

    The name of this protocol (id) is ns, and the second identifier (alg)
names the message algebra in use. The identifier for the Basic Crypto Algebra
is basic.
    A role has a name, a declared set of variables, and a trace that provides a
template for the behavior of its instances. A trace is a non-empty sequence
of message events, either a message reception or a transmission. An inbound
message with term t is −t in text and (recv t) in S-expression syntax. An
outbound term is +t in text and (send t) in S-expression syntax. The
Needham-Schroeder responder’s role in S-expression syntax is in Figure 2.

    A message may optionally be transferred on a channel using the syntax
(send c t) and (recv c t), where c is a variable of sort chan. A channel
 may be authenticated or confidential or both. The semantics of using
channels for messaging will be explained in the next section.
    Zero-based indexing is used though out this document and in the source
code it describes. Within the document, a finite sequence is a function from
an initial segment of the natural numbers. Angle brackets are used for sequence
 construction. Thus ⟨3, 2, 99⟩ = {0 7→ 3, 1 7→ 2, 2 7→ 99}, and the
responder’s trace is ⟨−{|N1 , A|}KB , +{|N1 , N2 |}KA , −{|N2 |}KB ⟩. The length of
a sequence x is |x|.
    A term originates in a trace if it is carried in some event and the first
term in which it is carried is an outbound term. A term is acquired by a
trace if it first occurs in an inbound term and is also carried by that term.
    Some atoms in a role have special properties. An atom may be declared
to be non-originating with the non-orig form or the pen-non-orig form
and uniquely originating with the uniq-orig form. A channel variable may
be declared to be authenticated with the auth form, and confidential with
the conf form. The declarations make assertions about instances of a role,
assertions that will be defined after role instantiation is explained.
    Every variable that occurs in each term declared to be non-originating
must occur in some term in the trace, and the term must not be carried by
any term in the trace. Every variable that occurs in each term declared to
be penetrator non-originating must occur in some term in the trace, but the
term may be carried by some term in a trace. Each term declared to be
uniquely originating must originate in the trace. Each variable of sort mesg
must be acquired in the trace.

## 5. Protocol Executions and Origination Assumptions

A protocol analysis problem is specified by a skeleton. Some background
information is presented before details of a problem specification is given.
    A skeleton describes a set of executions of a protocol. They specify the
local behavior of participants and their interactions via message-passing. A
definition of an execution is presented for the case in which protocols declare
no terms to be non-originating or uniquely originating, and then is later
amended. The executions are a representation of the strand space notion of
bundle.

    A strand represents a principal executing a single local session of a protocol
 role. The sequence of events that describes the session is patterned after
a prefix of its role’s trace. In the context of a protocol, a strand’s trace is
represented by an instance, a triple consisting of a role name, a height, and a
map from role variables to terms. The length of the described sequence is the
instance’s height, and must be positive and no greater than the length of the
associated role’s trace. The map is the instance’s environment. The domain
of the map is the set of variables that occur in the events in the prefix of the
role’s trace of the same length as the instance’s height.
    An example of an instance of the Needham-Schroeder responder role is:

           (defstrand resp 2 (b a) (a b) (n1 n1) (n2 n2))

The trace associated with this instance is:

                        ⟨−{|N1 , B|}KA , +{|N1 , N2 |}KB ⟩.

    The position of a event in the instance’s trace is its index in the sequence,
and in this example, the position of −{|N1 , B|}KA is zero.
    In addition to a protocol, a component of an execution is a collection of
local sessions. An instance cannot be used to identify one session, because
two principals may engage in the same pattern of message passing. Instead, a
sequence of instances is used as a component of an execution, and a strand is
represented by an index that selects an instance from the sequence. In other
words, each principal executing a local session is represented by a natural
number less than the length of the sequence of instances, and its behavior is
described by the instance found using its representation.
    A node is a pair of natural numbers that identifies an event within a
sequence of instances. The first integer is the strand, and the second is the
position of the event within the strand’s trace. A node with an inbound term
is a reception node, and one with an outbound term is a transmission node.
Given a sequence i, its nodes are:

                       {(s, p) | s < |i|, p < height(i(s))}.

    The remaining component of an execution is a binary relation between
transmission nodes and reception nodes, where each pair of nodes in the re-lation
 agree on their message term. The relation specifies message transmissions
 between strands. The nodes of the graph associated with an execution

are the nodes in the sequence of instances, and the edges include the ones in
the relation. Additionally, the following strand succession edges are included:

              {((s, p), (s, p + 1)) | s < |i|, p + 1 < height(i(s))}.

Executions with cyclic graphs are omitted from consideration, because they
violate causality. The transitive irreflexive ≺ is the transitive closure of the
graph’s edges, and n0 ≺ n1 asserts that the message event at n0 precedes the
one at n1 .
    The node relation of an execution satisfies one additional property. For
each reception node in its sequence, there exists a unique transmission node,
related to it by the communication ordering. In other words, the relation
must be a function. Informally, this property ensures that every message
reception is accounted for by the activity of a principal that is part of the
execution. Figure 3 shows the intended execution of the Needham-Schroeder
Protocol. The node graph of an execution is a bundle.
    A set of runs of the protocol is associated with each execution. A variable
 is associated with an execution if the variable occurs in the range of an
environment in some instance. To derive a run from an execution, a sub-stitution
 that maps each variable associated with the execution to a ground
term is applied to the execution. cpsa message algebras do not contain the
constants required to name all the ground terms. For most sorts, the identity
of a particular ground term is irrelevant to the analysis. Message tags are
the only exception to this rule. For this reason, cpsa message algebras are
free algebras, but not initial algebras.
    Strands in executions represent both adversarial and non-adversarial behaviors
. A strand that is an instance of a protocol role is non-adversarial,
and is called regular. A strand that represents adversarial behavior is called
a penetrator strand.

                                 {|N1 , A|}KB
                      init                         resp
                                {|N1 , N2 |}KA
                        •                            •
                                  {|N2 |}KB
                        •                            •

```scheme
     (vars (n1 n2 text) (a b name))
     (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))
     (defstrand resp 3 (n2 n2) (n1 n1) (b b) (a a))
     (precedes ((0 0) (1 0)) ((1 1) (0 1)) ((0 2) (1 2)))
```
**Figure 3: Needham-Schroeder Intended Run**

    The roles that define adversary behavior codify the basic abilities that
make up the Dolev-Yao model. They include transmitting an atom such as
a name or a key; transmitting a tag; transmitting an encrypted message after
 receiving its plain text and the key; and transmitting a plain text after
receiving ciphertext and its decryption key. The adversary can also concatenate
 two messages, or separate the pieces of a concatenated message. Since a
penetrator strand that encrypts or decrypts must receive the key as one of its
inputs, keys used by the adversary—compromised keys—have always been
transmitted by some participant. The adversary may transmit a message

on a channel when the channel is not authenticated, and the adversary may
receive a message on a channel when the channel is not confidential.
     Figure 4 shows a penetrated execution of the Needham-Schroeder Protocol
. Strand space theory would decompose the penetrator behavior into
multiple strands; instead the description of the penetrator has been simplified
by the use of an artificially constructed role pen.

                  {|N1 , A|}KP
         A                            P
                                                {|N1 , A|}KB
                                      •                            B
                  {|N1 , N2 |}KA
         •                                                          •
                    {|N2 |}KP
         •                            •
                                                 {|N2 |}KB
                                      •                             •
**Figure 4: Needham-Schroeder Penetrated**

### 5.1 Origination and Channel Assumptions (`non-orig`, `pen-non-orig`, `uniq-orig`, `auth`, `conf`)

A non-originating term is an atom that is carried by no message, and it or
its inverse is the key of an encryption in some message. Each non-originating
term is a key that is not compromised, as the penetrator has no access to
the key.
     A penetrator non-originating term is an atom that is forbidden from being
originated on a penetrator strand in an execution.
     A uniquely originating term is an atom that originates on exactly one
strand in the execution. The correct behavior of some protocols depends
on the fact that its executions include only ones in which some terms are
uniquely originating—each term’s provenance is one node. Implementations
of these protocols can ensure unique origination of a term by freshly generating
 a nonce for the component of the message it represents.
     A channel is authenticated if only regular strands transmit messages on
it. A channel is confidential if only regular strands receive messages on it.
     Occasionally, protocol roles designate some terms to be non-originating
or uniquely originating. Consider the prefix of the trace of a role associated
with some instance. When a uniquely originating role term is carried in the

prefix, the instance’s environment maps it to a term that must originate in
the instance’s strand. Furthermore, when the variables in a non-originating
role term occur in the prefix, the instance’s environment maps that term to
one that must not be carried by any message term in the execution. The
mapping of a non-originating role term can be conditioned on the height of
the instance. A role non-origination assumption of the form (3 a) asserts
that a will not be mapped into an instance unless its height is at least three.
Penetrator non-originating atoms are similar. Section 16 provides advice on
when to add non-origination or unique origination assumptions to roles.

## 6. Skeletons, Homomorphisms, and Refinements

A skeleton represents regular behavior that might make up part of an execution
. The components of a skeleton are similar to an execution. The
components of a skeleton include a protocol, a sequence of instances, and a
binary relation between transmission nodes and reception nodes within the
sequence. Unlike an execution, the strands in a skeleton specify only regular
behavior. Furthermore, the pair of nodes in the relation need not agree on
their message term. Two nodes are related if the transmitting node precedes
the reception node, as an execution it represents may include nodes between
the related transmission and reception nodes.
    The final five additional components of a skeleton are a set of non-originating
 terms, a set of penetrator non-originating terms, a set of uniquely
originating terms, a set of authenticated channels, and a set of confidential

channels. To be a skeleton, each uniquely originating term must originate in
at most one strand in the skeleton, and each non-originating term must never
be carried by some event in the skeleton and every variable that occurs in
the term must occur in some event. For a penetrator non-originating term,
is suffices that every variable that occurs in the term must occur in some
event. Furthermore, for each uniquely originating term that originates in the
skeleton, the node relation must ensure that reception nodes that carry the
term follow the node of its origination. Figure 5 shows the components in
the S-expression representation of a skeleton.

```scheme
     (defskeleton protocol variables
        ...                ; Instance sequence
        (precedes ...)     ; Node orderings
        (non-orig ...)     ; Non-originating terms
        (pen-non-orig ...) ; Penetrator non-originating terms
        (uniq-orig ...))   ; Uniquely originating terms
        (auth ...))        ; Authenticated channels
        (conf ...))        ; Confidential channels
```
**Figure 5: Components of Skeletons**

    Two skeletons are equivalent if there is a permutation of the strands in
one skeleton that when applied to its sequence and its node relation, produces
the other skeleton. Two skeletons are also equivalent if they differ only by
a systematic, sort-preserving renaming of their variables, excluding variables
that occur in the domains of environments—the role variables. The trace of
a strand is used for the comparison, so role names need not match.
    A skeleton is normalized by performing a transitive reduction on its node
relation. The transitive reduction of an ordering is the minimal ordering
such that both orderings have the same transitive closure. Here, communication
 orderings implied by transitive closure are removed. Two skeletons
are equivalent if their normalized forms are equivalent.
    One special skeleton is associated with each execution. It summarizes
the regular behavior of the execution. It is derived from the execution by
enriching its node relation to contain all node orderings implied by transitive
closure, deleting all strands and nodes that refer to penetrator behavior, and
then performing the transitive reduction on the resulting node relation. The
set of uniquely originating terms is the set of terms that originate on exactly

one strand in the execution, and are carried in a term of a regular strand.
The set of non-originating terms is the union of two sets. One set contains
each term that is used as an encryption or decryption key in some term in
the execution, but is not carried by any term. The other set contains the
terms specified by non-origination assumptions in roles. If a realized skeleton
instance maps all of the variables that occur in one of its non-originating role
terms, the mapped term is a member of the skeleton’s set of non-originating
terms. A skeleton is realized if it summarizes the behavior of some execution.
### 6.1 Realized Skeletons

Skeletons are a central concept in the cpsa algorithm because they capture
 the notion that the details of penetrator behavior are irrelevant to the
analysis. From the perspective of regular behavior, all that is needed is a
description of the messages that can be derived by the penetrator at a given
reception node of a regular strand. In a realized skeleton, some combination
of penetrator behavior and regular behavior derives the message at every
reception node. The skeleton’s node relation specifies the transmission nodes
that provide messages available to the penetrator for message derivations.
The rules for message derivation are algebra specific. If the message derivation
 rules imply a message at a reception node in a skeleton is derivable, the
node is realized.
    A skeleton with an unrealized node might be related to another skeleton
with additional regular behavior that makes the original node realized. A
skeleton with additional regular behavior is called a refinement.
### 6.2 Structural and Message Refinement (Homomorphisms)

A skeleton A structurally refines B if the transitive closure of the graph
associated with B is a subgraph of the one associated with A, the event at
corresponding nodes agree, the set of uniquely originating terms of B is a
subset of the ones in A, the set of non-originating terms of B is a subset of
the ones in A, and a uniquely originating term that originates in B originates
at the corresponding node in A. Penetrator non-originating assumptions are
similar to non-originating assumptions.
    A skeleton A message refines B if A and B agree on all but the terms in
the range of each strand’s environment and its non-originating and uniquely
originating terms, and there is a substitution that maps each term in B to its
related term in A. Similar to structural refinement, a uniquely originating
term that originates in B originates at the same node in the image of B.
    A skeleton A refines B if A is equivalent to a skeleton that structurally
or message refines B.1 Each skeleton describes the realized skeletons that

refine it. A skeleton is dead if no realized skeleton refines it. A diagram of a
skeleton is in Figure 6.

      A skeleton A refines B if there is a homomorphism from B to A as defined in [2].

                   {|N1 , A|}KC                       {|N1 , A|}KB
        init                                                             resp
                  {|N1 , N2 |}KA                      {|N1 , N2 |}KA
          •                               ≻                               •
                    {|N2 |}KC                           {|N2 |}KB
          •                               ≺                               •
**Figure 6: Needham-Schroeder Shape (KA−1 uncompromised, N2 fresh)**

    The cpsa algorithm computes realized skeletons from unrealized skeletons
 by identifying an unrealized node, and computing the skeletons that
refine the unrealized skeleton by making the target node realized.

## 7. Listeners

In addition to the roles specified in a protocol, for each term t, a regular
strand may be an instance of the listener role with the trace lsn(t) = ⟨−t, +t⟩.
There are no non-originating or uniquely originating terms associated with
a listener role.
    A listener strand is used in a skeleton to assert that an atom t is available
on its own to the adversary, unprotected by encryption. For example, to
test if the protocol keeps a term t from the adversary, one adds a strand
that listens for t. The term is protected if the resulting skeleton is dead.
Otherwise, the cpsa analyzer program will find a refined realized skeleton
that shows how the adversary accesses t.
    A listener instance in S-expression syntax follows. See strand in Table 2,
Appendix A.
                                (deflistener term)
The cpsa programs generate the associated listener role and hide it on output
. Listener role names are absent in all forms of output, one indication
that a strand is an instance of a listener role.
The implementation avoids the complexities of directly representing homomorphisms by
composing structural and message refinement with equivalence checks, as is done in this
chapter.

## 8. Authentication Tests

Authentication tests [6] guide the search for skeletons that refine one with
an unrealized node into ones in which it is realized. There are three types
of authentication tests, nonce, encryption, and channel tests. In all cases,
an unrealized node is selected, called the test node. A term carried by the
inbound message at the test node is identified as the critical term. A critical
term is one that occurs in a message context, the construction of which cannot
be explained by the regular behavior in the current skeleton or by penetrator
behavior. An authentication test determines the additional regular behavior
required to refine a skeleton into ones in which the test node is realized.
    The critical term in a nonce test is a uniquely originating term, the nonce.
It is freshly generated by one regular participant in each run of the protocol.
A nonce is unguessable by both regular and adversarial participants except
when it is received in an unprotected context.
    A reception node’s outbound predecessors is the set of messages sent by
transmission nodes that precede the reception node, as given by the transitive
closure of its skeleton’s node ordering relation. Suppose every occurrence of
the nonce in the outbound predecessors of the test node is within a context
protected by encryption, but the critical term in the test node occurs outside
of all of those encryptions. Clearly, another participant was able to decrypt
one of the test node’s outbound predecessors. The set of encryptions that
protects a critical term in a test node’s outbound predecessors is called its
escape set.
    There are three ways to refine a skeleton to account for the decryption:
regular augmentation, listener augmentation, and contraction. For regular
augmentation, an instance of a protocol role is added to the skeleton. The final
 transmission node of the strand is called a transforming node. The strand
is selected for augmentation because relative to the test node’s outbound pre-decessors
, the transforming node’s message shows the strand performed the
decryption.
    Sometimes, a regular augmentation is immediately followed by merging
the new strand into another. This is called a displacement. It occurs when
simply adding the strand creates a redundancy.
    The penetrator can expose the critical term if it has access to any of the
decryption keys used to protect it in the escape set. For listener augmentation
, an instance of a listener role listening to one decryption key used to
protect the critical term is added, and the skeleton’s communication ordering

relation is updated to record the fact that the listener’s transmission node
precedes the test node. If the resulting skeleton is not dead, the decryption
can be explained by penetrator behavior.
    For a contraction, a message refining substitution is found that equates
two or more atoms. Sometimes, the key used to protect the critical term can
be equated with one used in previous messages, thus vacuously explaining
the decryption of the critical term.
    The critical term in an encryption test is an encryption. When the encryption
 key is unavailable, the encryption is unguessable. Whenever the
unavailability of the encryption key can be established, the methods used to
refine skeletons with nonce tests apply. Additionally, an instance of a listener
role listening for the critical term’s encryption key is added. If the resulting
skeleton is not dead, the encryption can be explained by penetrator behavior.
    The critical term in a channel test is an authenticated channel and a term.
cpsa uses regular augmentation to create a matching term transmitted on
the channel.

## 9. Generalization and Shapes

Repeated use of authentication tests either produce realized skeletons or
show that a skeleton is dead. The next step in the algorithm is to make each
realized skeleton into a shape, using the process of generalization.
    Realized skeleton A generalizes realized skeleton B if A refines the origin
problem specification, and B refines A. Furthermore, A may not combine
strands in B. The shape associated with a realized skeleton is its maximally
generalized realized skeleton. The shapes of a protocol capture all the essentially
 different executions possible for the protocol consistent with the
initial behavior specification. Figure 6 shows the shape associated with the
Needham-Schroeder Protocol from the point of view of a responder strand.
    A different fixed set of operations is used to transform a realized skeleton
into a shape: deletion, weakening, separation, and forgetting. If an operation
 succeeds, it produces a more general realized skeleton, one that is not
equivalent to the starting skeleton. If no operations succeeds, the skeleton is
a shape.
    For deletion, a node and all nodes that follow it in a strand are deleted,
and the resulting skeleton is checked to see if it generalized the starting
skeleton. The operation is tried for each node in the starting skeleton until

there is a success.
    If deletion fails, a skeleton is weakened by deleting one element of the
communication ordering, then checking the result to see if it generalized the
starting skeleton. The operation is tried for each communication ordering in
the starting skeleton until there is a success.
    If weakening fails, origination assumption forgetting is tried by deleting
each term in the non-originating set that is not specified by a role. This
is followed by deleting each term in the uniquely originating set that is not
specified by a role.
    If origination assumption forgetting fails, variable separation is tried.
Sometimes a more general skeleton can be found by replacing some occurrences
 of one variable by a fresh variable. To separate a variable, the collection
 of places at which the variable occurs in the range of all environments is
generated, and a fresh variable is substituted for the variable at a subset of
these places. All possibilities are tried until a more general skeleton is found.
    Sometimes a shape is derived from another shape by collapsing two strands
in a shape. Collapsing might produce an unrealized skeleton, so authentication
 tests apply.

## 10. Skeleton Input Syntax (`defskeleton`)

With this background, the defskeleton form in Table 2, Appendix A is
explained. The key object in cpsa input and output is a skeleton, but an
object with weaker properties is allowed for the initial problem statement.
A preskeleton is a skeleton except that terms in the uniquely originating set
may originate in more than one strand. Furthermore, the node relation of
a preskeleton need not imply that a node that carries a uniquely originating
 term is after the node of its origination. A preskeleton that cannot be
immediately converted into a skeleton is erroneous, and an error message is
issued.
    Referring to skeleton in Table 2, the id in the skeleton form names a
protocol. It refers to the most recent protocol definition of that name which
precedes the skeleton form. The id in the strand form names a role. The
integer in the strand form gives the height of the strand. The sequence of
pairs of terms in the strand form specify an environment used to construct
the messages in a strand from its role’s trace. The first term is interpreted
using the role’s variables and the second term uses the skeleton’s variables.

The environment used to produce the strand’s trace is derived by matching
the second term using the first term as a pattern.
    The precedes form specifies members of the node relation. The first
integer in a node identifies the strand using the order in which strands are
defined in the defskeleton form.
    A variable may occur in more then one role within a protocol. The reader
performs a renaming so as to ensure these occurrences do not overlap. Furthermore
, the maplets used to specify a strand need not specify how to map
every role variable. The reader inserts missing mappings, and renames every
skeleton variable that also occurs in a role of its protocol. The sort of every
skeleton variable that occurs in the non-orig, pen-non-orig, uniq-orig,
auth, or conf lists or in a maplet must be declared, using the vars form.
    The prot-alist, role-alist, and skel-alist productions are Lisp
style association lists, that is, lists of key-value pairs, where every key is
a symbol. Key-value pairs with unrecognized keys are ignored, and are available
 for use by other tools. On output, unrecognized key-value pairs are
preserved when printing protocols, but elided when printing skeletons, with
the exception of the comment key.

### 10.1 Semantic Errors and Well-Formedness Checks

The error messages generated for syntax errors are informative, however the
ones generated for semantic errors are less so. A role might be rejected
because it is not well-formed. A role is not well-formed if (1) there is a term
declared to be uniquely originating that does not originate in the trace, (2)
there is a term declared to be non-originating that is carried by some term
in the trace, a variable occurs in the term that does not occur in the trace,
or the declaration of the term included a height, and a variable occurs in the
term that does not occur in the prefix of the trace of the given height, or
(3) a variable of sort mesg is not acquired in the trace. The error message
might not indicate which condition caused the rejection.
    Similarly, a skeleton might be rejected because it is not well-formed. A
skeleton is not well-formed if (1) the first node in a node pair refers to an
inbound term, or the second node refers to an outbound term, (2) the node
ordering contains cycles, (3) a term declared to be uniquely originating, is
not carried by any term, (4) an instance maps a uniquely originating role
term to a term that does not originate in the instance’s strand, or (5) a
term declared to be non-originating is carried by a term in some strand, or

a variable occurs in the term that does not occur in any strand. Once again,
the error message might not indicate which condition caused the rejection.

### 10.2 Needham-Schroeder Input Example

This section contains the verbatim input of the running example used
throughout this paper. The use of an editor that pretty-prints S-expressions
is recommended.

```scheme
;;; Hey Emacs, use -*- mode:scheme -*-
(herald "Needham-Schroeder Public-Key Protocol"
        (comment "This protocol contains a man-in-the-middle"
                 "attack discovered by Galvin Lowe."))
```

   An S-expression version of Figure 1 follows.

```scheme
(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 (pubk a)))
     (recv (enc n2 (pubk b))))))
```

    The protocol is analyzed from the point of view of a complete run of one
instance of an initiator role.

```scheme
(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b) (privk a))
  (uniq-orig n1))
```

## 11. Output Format and Annotations

The cpsa output format has been designed so that it can be reused as input
. All skeletons in the output are normalized skeletons, with the possible
exception of an initial preskeleton, the one used to state a problem. If an initial
 preskeleton cannot be converted into a skeleton, an error is immediately
signaled.
    For each skeleton, a cpsa analyzer computes a set of skeletons that refine
it using a fixed set of operations based on authentication tests. The immediate
 descendants of a skeleton are called its cohort. A member of the cohort
that is equivalent to a previously seen skeleton is replaced by that skeleton.
Thus the skeletons in an analysis form a directed acyclic graph. All but one
skeleton has a single parent, and one skeleton can be a member of several
cohorts.
    The operations above either produce realized skeletons or show that a
skeleton is dead. The next step in the algorithm is to make each realized
skeleton into a shape, using the process of generalization. Although the set
of shapes is in some sense the answer to the problem, an understanding of
the operations used to generate the shapes can be very informative. The
remainder of this section describes the annotations in the output that allow
for an understanding of each step of the analysis.
    On output, key-value pairs are added to each skeleton’s association list,
skel-alist. Every skeleton in the output is labeled with a unique identifier
with (label integer). A skeleton has (parent integer) if it is a member
of the cohort of the identified parent. A skeleton has (seen integer+)
when members of its cohort are equivalent to previously seen skeletons. A
skeleton lists its unrealized nodes with (unrealized node∗). The traces
associated with each strand is given by the (traces . . . ) form.
    Figure 7 shows a skeleton generated during an analysis of the Needham-
Schroeder Protocol from the point of view of an initiator strand. It is labeled
as 1. It’s parent is labeled 0. It has one child, and that child has not been
seen before. It is unrealized.

```scheme
(defskeleton ns
  (vars (n1 n2 n2-0 text) (a b name))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))
  (defstrand resp 2 (n2 n2-0) (n1 n1) (b b) (a a))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (non-orig (privk a) (privk b))
  (uniq-orig n1)
  (operation nonce-test (added-strand resp 2) n1 (0 1)
    (enc n1 a (pubk b)))
  (traces
    ((send (enc n1 a (pubk b))) (recv (enc n1 n2 (pubk a)))
      (send (enc n2 (pubk b))))
    ((recv (enc n1 a (pubk b)))
      (send (enc n1 n2-0 (pubk a)))))
  (label 1)
  (parent 0)
  (unrealized (0 1))
  (comment "1 in cohort - 1 not yet seen"))
```
**Figure 7: Annotated cpsa Output**

### 11.0.1 Interpreting the `operation` Field

The operation used to derive a skeleton is recorded with
(operation test kind term node term∗), where test is the authentication
 test encryption-test, nonce-test, or channel-test; kind is
(added-strand id integer), (displaced integer integer id integer),
(contracted maplet∗), or (added-listener term); term is the critical
term; node in the test node; and the remaining terms specify the escape

set. When the operation kind is added strand, the instance’s role name
and height are provided. For kind displaced, the first number is the strand
being merged, the second number is the strand it was merged into, and
the remaining give the new instance’s role name and height. For kind
added-listener, a term is provided. For kind contracted, the substitution
is provided. When a substitution refers to a variable not in the skeleton,
its name is unpredictable. For generalization, the operation is recorded as
(operation generalization method), where method is one of deleted
node, weakened node-pair, separated term, or forgot term. Shapes
can be collapsed leading to new shapes. For shape collapsing, the operation
is recorded as (operation collapsed integer integer), where the two
integers identify the strands merged.
    The skeleton in Figure 7 was generated as a result of a nonce test, by
augmenting the starting skeleton with a responder strand of length two. The
critical term is n1, the test node is (0 1), and the escape set has one element.
    When the operation kind is added strand, it is possible that the number
of strands in the skeleton and its parent are the same. In this case, cpsa
has found a way to produce a more concise representation of the skeleton by
merging two strands.

### 11.1 Needham-Schroeder Complete Output Trace

This section contains the verbatim output of the running example used
throughout this paper. A run starts by displaying the program’s version
number.

(herald "Needham-Schroeder Public-Key Protocol"
  (comment "This protocol contains a man-in-the-middle"
    "attack discovered by Galvin Lowe."))

(comment "CPSA 4.4.8")
(comment "All input read")

   An S-expression version of Figure 1 follows.

```scheme
(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace (send (enc n1 a (pubk b)))
```

      (recv (enc n1 n2 (pubk a))) (send (enc n2 (pubk b)))))
```scheme
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace (recv (enc n1 a (pubk b)))
      (send (enc n1 n2 (pubk a)))
      (recv (enc n2 (pubk b))))))
```

    The protocol is analyzed from the point of view of a complete run of one
instance of an initiator role.

```scheme
(defskeleton ns
  (vars (n1 n2 text) (a b name))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))
  (non-orig (privk a) (privk b))
  (uniq-orig n1)
  (traces
    ((send (enc n1 a (pubk b))) (recv (enc n1 n2 (pubk a)))
      (send (enc n2 (pubk b)))))
  (label 0)
  (unrealized (0 1))
  (comment "1 in cohort - 1 not yet seen"))
```

   A nonce test justifies adding an instance of part of a reponder role.

```scheme
(defskeleton ns
  (vars (n1 n2 n2-0 text) (a b name))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))
  (defstrand resp 2 (n2 n2-0) (n1 n1) (b b) (a a))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (non-orig (privk a) (privk b))
  (uniq-orig n1)
  (operation nonce-test (added-strand resp 2) n1 (0 1)
    (enc n1 a (pubk b)))
  (traces
    ((send (enc n1 a (pubk b))) (recv (enc n1 n2 (pubk a)))
      (send (enc n2 (pubk b))))
    ((recv (enc n1 a (pubk b)))
      (send (enc n1 n2-0 (pubk a)))))

  (label 1)
  (parent 0)
  (unrealized (0 1))
  (comment "1 in cohort - 1 not yet seen"))
```
  A nonce test justifies a contraction that produces the one and only shape.
The shape is also displayed in Figure 8.

                {|N1 , A|}KB                   {|N1 , A|}KB
       init                         ≺                           resp
                {|N1 , N2 |}KA                 {|N1 , N2 |}KA
         •                          ≻                            •
                  {|N2 |}KB
         •
**Figure 8: Needham-Schroeder Shape (Initiator Point of View)**

```scheme
(defskeleton ns
  (vars (n1 n2 text) (a b name))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))
  (defstrand resp 2 (n2 n2) (n1 n1) (b b) (a a))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (non-orig (privk a) (privk b))
  (uniq-orig n1)
  (operation nonce-test (contracted (n2-0 n2)) n1 (0 1)
    (enc n1 n2 (pubk a)) (enc n1 a (pubk b)))
  (traces
    ((send (enc n1 a (pubk b))) (recv (enc n1 n2 (pubk a)))
      (send (enc n2 (pubk b))))
    ((recv (enc n1 a (pubk b)))
      (send (enc n1 n2 (pubk a)))))
  (label 2)
  (parent 1)
  (unrealized)
  (shape))
```

The following phrase means cpsa is finished with this problem—it has exhausted its to do list.

```scheme
(comment "Nothing left to do")
```

## 12. Security Goals and Rules

Another way to specify a problem statement is with a security goal. A
security goal a sentence in first-order logic. It asserts that if some properties
hold for a skeleton, then some other properties must hold for all shapes
computed by CPSA starting with the skeleton. Security goals can be used
to formally state authentication and secrecy goals of a protocol.
    The defgoal form is used to pose an analysis problem with a sentence
instead of a skeleton. CPSA extracts a point of view skeleton from the
antecedent of the formula and then analyzes it. When it prints a shape, it
checks to see if the shape satisfies the conclusion of the security goal. See [8]
for details.
    Each protocol may include a small collection of rules. A rule is a sentence
in the goal language. A rule is an axiom added to a protocol. cpsa uses the
axiom as a rewrite rule to derive zero or more new skeletons from a skeleton
produced during a cohort step. Rules are described in [8]. The grammar of
security goals and rules is in Table 3.

## 13. Macros (`defmacro`)

After reading the input, cpsa expands macros before in analyzing the results.
A macro definition is a top-level form.

      (defmacro (name arg∗ ) body)

    The cpsa program expands all calls to macros in non-macro defining Sexpressions
 using the macros that have been defined previously. A macro
definition can be used to expand a call if the first element of a list matches
the name of the macro, and the length of the remaining elements in the
list matches the length of the macro’s argument list. When two macros
definitions are applicable, the last definition takes precedence. The cpsa
program omits macro definitions from its output.
    After expanding a list, elements of the list of the form (^ · · · ) are
spliced into the output. Thus (a ^(b c) d) becomes (a b c d) after macro
expansion.

## 14. File Includes (`include`)

While performing macro expansion, cpsa includes other source files with the
top-level include form,
      (include file)
where file is a string.

## 15. Algebra Signature Extensions (`lang`)

The signature of the message algebra used by cpsa is extensible. There are
two forms of extensibility provided by cpsa. Users can add operations for
encryption, tupling, and hashing; and add sorts for atomic data.
    A common extension is to add tupling operations to message algebras.
Previously, complex protocols often made use of tagged concatenation to encode
 a tagged sequence of messages. In cpsa, concatenation is implemented
as sequences of pairing operations. Thus, the expression for a certificate body
of the form
      (cat "cert-body" dn serial-no pub-key)
is syntax for
      (cat "cert-body" (cat dn (cat serial-no pub-key)))
   Algebra extensions are declared using the lang key in the protocol’s association
 list, at the end of a protocol. For the certificate body example,
```scheme
      (defprotocol cert basic
        ...
        (lang (cert-body (tupl 3))))
```
adds one tupling operation so that the example above can be written as
      (cert-body dn serial-no pub-key)
cpsa represents this form internally as a sequence of messages with a distinguished
 mark. This representation is more efficient as compared with the
tagged concatenation representation.
    The syntax of a lang declaration is given in Table 1. There are eight
kinds of ways that cpsa algebras can be extended.

**Table 1: Lang Field Syntax**

```text
 lang ← (lang ldecl∗)
ldecl ← (symbol+ kind)
 kind ← atom | akey | hash | (tupl integer)
      | enc | senc | aenc | sign
```

• An atomic sort is added to the algebra when a symbol is declared to
  be of kind atom. If dollar is declared to be an atomic sort, then
  (price dollar) in a var form declares price to be of sort dollar.

• An atomic sort is also added to the algebra when a symbol is declared
  to be of kind akey. However, in addition to adding the sort, cpsa adds
  the equation (x−1 )−1 = x for variables of the new sort.

• A unary operation is added to the algebra when a symbol is declared
  to be of kind hash. As with the default hash operation, the adversary
  cannot extract the contents of the hash.

• An n-ary operation is added to the algebra when a symbol is declared
  to be of kind (tupl n). As with concatenation, the adversary can
  construct and extract contents of tuples. Constraint: n > 0.

• A binary operation is added to the algebra when a symbol is declared to
  be of kind enc. As with the default encryption operation, the adversary
  cannot extract contents of the encryption without access to the inverse
  of the key.

• A symbol of kind senc is just like one of kind enc except that the key
  supplied when it is applied must be symmetric, that is, the sort of the
  key must not be asymmetric.

• A symbol of kind aenc is just like one of kind enc except that the key
  supplied when it is applied must be asymmetric, but not the inverse
  applied to an asymmetric key.

• A symbol of kind sign is just like one of kind enc except that the key
  supplied when it is applied must be the inverse applied to an asymmetric
 key.

## 16. Modeling Methodology and Advice

### 16.1 Role vs. Skeleton Origination Assumptions

This section contains advice derived from using cpsa. When specifying cpsa
input, one must decide when to specify terms as uniquely originating or non-originating
 in a role, and when to specifying them in the initial skeleton. If a
fresh value is generated by all programs that implement a role in a protocol,
the term that represents the fresh value should be assumed to be uniquely
originating in the role. Otherwise, unique origination assumptions should be
specified in the initial skeleton.
    Adding non-origination assumptions to a role can lead to an excessively
weak protocol analysis, i.e. an analysis relative to an unrealistically narrow
assumption. Placing non-origination assumptions in the initial skeleton is
preferred whenever possible.
### 16.2 Distinguishing `text` vs. `data` Sorts

The Basic Crypto Algebra has two text-like sorts, `text` and `data`. For
some protocols, message fields that carry uniquely originating data cannot be
carried by other text-like fields. To ensure cpsa does not explore skeletons
in which uniquely originating data is carried in fields with predictable values,
the convention is to use the sort data for uniquely originating data, and sort
text for the other fields.
### 16.3 Shape Interpretation and Authentication Test Debugging

When looking at the output, try extracting the shapes first. If the shapes
only version of the output does not answer your questions, try studying the
output that contains intermediate skeletons.
    When cpsa generates an unexpected intermediate skeleton, study its
operation field (see Page 11). Usually, the unexpected intermediate skeletons
of interest have been generated as a result of an authentication test. Section 8
explains how to interpret an operation field for an authentication test.
    When using cpsa for protocol design, focus on authentication tests. For
each iteration of the design, search for the most informative unexpected
intermediate skeleton. That skeleton is likely to suggest a missing origination
assumption, or the redesign of some message term included in the operation
field.
### 16.4 Progressive Refinement Analysis Technique

There are situations in which origination assumptions are not justified
for initial segments of runs of a protocol, but are required to show that
complete runs of the protocol have certain expected shapes. In this case, the
progressive refinement analysis technique is used. The initial segments of runs
are analyzed with only the origination assumptions justified initially. A shape
associated with a partial run may justify additional origination assumptions.
For example, a strand in a partial run may send its next message only after a

trust decision is made, and the implication of the decision is that the strand
infers that some key is uncompromised. In this case, the shape with the new
origination assumption and additional regular behavior is supplied as input
to cpsa, thereby refining the original problem.
### 16.5 Resource Bounds and Handling Non-Termination

As there is no guarantee that cpsa is bug free, you may come upon input
that causes non-termination. As a result, whenever you run the program
unattended, you should limit its memory usage. To get output that can be
visualized, specify a step count and/or a strand bound so that cpsa has the
chance to abort the run in a fashion that generates graphable output. Of
course, sending us input that causes erroneous behavior will help us improve
cpsa.

## 17. Formula Extraction (`cpsa4sas`)

The cpsasas program extracts a formula in the language of order-sorted first-order
 logic for each problem and its shapes from a cpsa run. The formula
is called a shape analysis sentence [7]. The formula is satisfied in all realized
skeletons when cpsa finds all the shapes for the problem. The details of
formula extraction are presented in Appendix B of The cpsa Specification [9].

## Acknowledgements
Jonathan K. Millen provided valuable feedback as our first cpsa user and on
a draft of this document.

## Appendix A: BCA Syntax Reference
The complete syntax for the analyzer using the Basic Crypto Algebra is
shown in Tables 2 and 3. The start grammar symbol is file, and the terminal
grammar symbols are: (, ), symbol, string, integer, and the constants
set in typewriter font. The language used for stating security goals is in
Table 3. The goal language adds the sort symbol node.
    The alist, prot-alist, role-alist, skel-alist, and goal-alist productions
 are Lisp style association lists, that is, lists of key-value pairs, where
every key is a symbol. Key-value pairs with unrecognized keys are ignored,
and are available for use by other tools. On output, unrecognized key-value

pairs are preserved when printing protocols, but elided when printing skeletons
.
    The contents of a file can be interpreted as a sequence of S-expressions.
The S-expressions used are restricted so that most dialects of Lisp can read
them, and characters within symbols and strings never need quoting. Every
list is proper. An S-expression atom is either a symbol, an integer, or
a string. The characters that make up a symbol are the letters, the digits
, and the special characters in “-*/<=>!?:$%_&~^+”. A symbol may not
begin with a digit or a sign followed by a digit. The characters that make
up a string are the printing characters omitting double quote and backslash,
except when double quote and backslash are escaped using the backslash
character. Double quotes delimit a string. A comment begins with a semicolon
, or is an S-expression list at top-level that starts with the comment
symbol.

**Table 2: cpsa Syntax**

```text
      file   ←   herald? form+
  herald     ←   (herald title alist)
    title    ←   symbol | string
    form     ←   comment | protocol | skeleton | goal
comment      ←   (comment . . . )
protocol     ←   (defprotocol id alg role+ rule∗ prot-alist)
        id   ←   symbol
      alg    ←   symbol
    role     ←   (defrole id vars trace role-alist)
     vars    ←   (vars decl∗)
    decl     ←   (id+ sort)
     sort    ←   text | data | name | skey | akey | mesg | chan
   trace     ←   (trace event+)
   event     ←   (send id? term) | (recv id? term)
    term     ←   id | akey | (ltk id id) | string | (cat term+)
             |   (enc term+ term) | (hash term+)
     akey    ←   id | (invk id) | (pubk id) | (privk akey)
             |   (pubk id string) | (privk id string)
role-alist   ←   (non-orig ht-term∗) role-alist
             |   (pen-non-orig ht-term∗) role-alist
             |   (uniq-orig term∗) role-alist
             |   (conf id∗) role-alist
             |   (auth id∗) role-alist
  ht-term    ←   term | (integer term)
     rule    ←   (defrule id sentence rule-alist)
rule-alist   ←   ...
prot-alist   ←   (lang ldecl∗) prot-alist | . . .
    ldecl    ←   (symbol+ kind)
      kind   ←   atom | akey | hash | (tupl integer)
                 enc | senc | aenc | sign
```

**Table 3: cpsa Syntax Continued**

```text
  skeleton    ←    (defskeleton id vars
                        strand+ skel-alist)
    strand    ←    (defstrand id integer maplet∗)
              |    (deflistener term)
    maplet    ←    (term term)
 skel-alist   ←    (non-orig term∗) skel-alist
              |    (pen-non-orig term∗) skel-alist
              |    (uniq-orig term∗) skel-alist
              |    (conf id∗) skel-alist
              |    (auth id∗) skel-alist
              |    (facts fact∗) skel-alist
              |    (precedes node-pair∗) skel-alist | . . .
  node-pair   ←    (node node)
      node    ←    (integer integer)
      fact    ←    (id fterm∗)
     fterm    ←    term | integer

       goal   ←    (defgoal id sentence+ goal-alist)
   sentence   ←    (forall (decl∗) implication)
implication   ←    (implies antecedent conclusion)
 conclusion   ←    (false) | existential | (or existential∗)
existential   ←    (exists (decl∗) antecedent) | antecedent
antecedent    ←    atomic | (and atomic∗)
     atomic   ←    (p roleid svar hgt)
              |    (p roleid param svar term)
              |    (prec svar pos svar pos)
              |    (non term) | (pnon term)
              |    (uniq term) | (uniq-at term svar pos)
              |    (conf id) | (auth id)
              |    (fact id term∗) | (= term term)
     roleid   ←    string
        hgt   ←    integer
        pos   ←    integer
       svar   ←    id
     param    ←    string
```

## Appendix B: Omitted Executions and Natural Role Semantics
When given some initial behavior, the cpsa program discovers what shapes
are compatible with it. Early work claimed that the cpsa algorithm would
generate every shape in a finite number of steps [2, 5]. Further theoretical
 work showed classes of executions that are not found by the algorithm,
however it also showed that every omitted execution requires an unnatural
interpretation of a protocol’s roles. Hence the algorithm is complete relative
to natural role semantics. We present an example of a protocol that has a
shape missed by cpsa.
    The protocol has an initiator role and a responder role.

               init    {|N |}K                {|N1 |}K   resp

                •      N                           N2      •

   Observe that a natural interpretation of N2 in the responder role is that
a binding for it is known when an instance of the role begins execution.
   Consider a scenario in which there is an instance of the initiator role
where N is freshly generated and K −1 is uncompromised. cpsa will find no
shapes compatible with the scenario, however what follows is.

                                  {|N |}K
                      init                        resp

                       •             N             •

Yet this shape requires that the message for N2 in an instance the responder
role be obtained from its first message reception—an unnatural interpretation
of the responder role.

## References
[1] Edsger W. Dijkstra. Why numbering should start at zero. http://www.
    cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html,
    August 1982.

[2] Shaddin F. Doghmi, Joshua D. Guttman, and F. Javier Thayer. Searching
 for shapes in cryptographic protocols. In Tools and Algorithms
    for Construction and Analysis of Systems (TACAS), number 4424 in
    LNCS, pages 523–538. Springer, March 2007. Extended version at
    http://eprint.iacr.org/2006/435.

[3] Daniel Dolev and Andrew Yao. On the security of public-key protocols.
    IEEE Transactions on Information Theory, 29:198–208, 1983.

[4] Joseph A. Goguen and Jose Meseguer. Order-sorted algebra I: Equational
    deduction for multiple inheritance, overloading, exceptions and partial
    operations. Theoretical Computer Science, 105(2):217–273, 1992.

[5] Joshua D. Guttman. Shapes: Surveying crypto protocol runs. In
    Veronique Cortier and Steve Kremer, editors, Formal Models and Techniques
 for Analyzing Security Protocols, volume 5 of Cryptology and Information
 Security Series. IOS Press, 2011.

[6] Joshua D. Guttman and F. Javier Thayer. Authentication tests and the
    structure of bundles. Theor. Comput. Sci., 283(2):333–380, 2002.

[7] John D. Ramsdell. Deducing security goals from shape analysis sentences.
    The MITRE Corporation, April 2012. http://arxiv.org/abs/1204.
    0480.

[8] John D. Ramsdell. CPSA Security Goals and Rules. The MITRE Corporation
, 2015. In https://github.com/mitre/cpsaexp source distribution
, doc directory.

[9] John D. Ramsdell, Joshua D. Guttman, Moses D. Liskov, and Paul D.
    Rowe. The CPSA Specification: A Reduction System for Searching for
    Shapes in Cryptographic Protocols. The MITRE Corporation, 2009. In
    https://github.com/mitre/cpsaexp source distribution, doc directory.
````

---

### `refrences/cpsa_kb/02_manuals/04_CPSA_Goals_and_Security_Manual.md`

*sha256:`c785cb712b93` · 1289 lines · 61.5 KB (~15,601 tokens) · lang:`markdown` · 6 control chars sanitized*

````markdown
# CPSA Security Goals, Rules, Lemmas, and Shape Analysis Sentences Manual

*Authors: Joshua D. Guttman, John D. Ramsdell, Moses D. Liskov, Paul D. Rowe (The MITRE Corporation, CPSA Version 4.4)*

---

## Table of Contents

- [1. Introduction to First-Order Security Goals](#1-introduction-to-first-order-security-goals)
- [2. Security Goal Syntax (`defgoal` and Predicates)](#2-security-goal-syntax-defgoal-and-predicates)
  - [2.1 Full CPSA 4.4 Security Goal Grammar](#21-full-cpsa-44-security-goal-grammar)
  - [2.2 Goal Predicates](#22-goal-predicates)
  - [2.3 Syntactic Abbreviations (`strand` and `listener`)](#23-syntactic-abbreviations-strand-and-listener)
- [3. Model-Theoretic Semantics and Characteristic Skeletons](#3-model-theoretic-semantics-and-characteristic-skeletons)
- [4. Authentication and Secrecy Goal Examples](#4-authentication-and-secrecy-goal-examples)
  - [4.1 Counterexample Analysis: Needham-Schroeder Responder (`satisfies no`)](#41-counterexample-analysis-needham-schroeder-responder-satisfies-no)
  - [4.2 Secrecy Goal with Listeners (`(false)` Conclusion)](#42-secrecy-goal-with-listeners-false-conclusion)
- [5. Multi-Sentence Goals, Skeleton `goals` Annotations, and Shape Analysis Sentences](#5-multi-sentence-goals-skeleton-goals-annotations-and-shape-analysis-sentences)
  - [5.1 Shape Analysis Sentences (`cpsa4sas`)](#51-shape-analysis-sentences-cpsa4sas)
- [6. Axiomatic Rewrite Rules (`defrule`) and Facts (`facts`)](#6-axiomatic-rewrite-rules-defrule-and-facts-facts)
  - [6.1 Skeleton Fact Databases (`facts` and `fact`)](#61-skeleton-fact-databases-facts-and-fact)
  - [6.2 Case Study: Door Simple Example Protocol (DoorSEP) and Trust Axioms](#62-case-study-door-simple-example-protocol-doorsep-and-trust-axioms)
- [7. Automatically Generated Rules (`defgenrule`), Built-in Relations, and Trace Annotations](#7-automatically-generated-rules-defgenrule-built-in-relations-and-trace-annotations)
  - [7.1 Built-in Fact Relations (`neq`, `invk`, `lt`, `subsort`) and Generated Rules](#71-built-in-fact-relations-neq-invk-lt-subsort-and-generated-rules)
  - [7.2 Trace Annotations (`cheq`, `assume`, `rely`, `guarantee` / `guar`) and `cpsa4goals`](#72-trace-annotations-cheq-assume-rely-guarantee--guar-and-cpsa4goals)
- [8. Lemmas (`deflemma`)](#8-lemmas-deflemma)
- [9. Formal Specification of Shape Analysis Sentences (Coherent Logic)](#9-formal-specification-of-shape-analysis-sentences-coherent-logic)
  - [9.1 Formal Syntax and Satisfaction Semantics of Skeleton Formulas](#91-formal-syntax-and-satisfaction-semantics-of-skeleton-formulas)
- [10. References](#10-references)

---

## 1. Introduction to First-Order Security Goals

Analyzing a cryptographic protocol means finding out what security
properties—essentially, authentication and secrecy properties—are true in
all its possible executions.
    Given a protocol definition and some assumptions about executions, cpsa
attempts to produce descriptions of all possible executions of the protocol
compatible with the assumptions. Naturally, there are infinitely many possible
 executions of a useful protocol, since different participants can run it
with varying parameters, and the participants can run it repeatedly.
    However, for many naturally occurring protocols, there are only finitely
many of these runs that are essentially different. Indeed, there are frequently
very few, often just one or two, even in cases where the protocol is flawed. We
call these essentially different executions the shapes of the protocol. Authentication
 and secrecy properties are easy to “read off” from the shapes, as are
attacks and anomalies, according to the introduction in the cpsa Primer [4].
    But how easy is it to read off authentication and secrecy properties? What
precisely is it that an expert sees? This paper describes cpsa’s support for
reasoning about security goals using first-order logic. With security goals
expressed in first-order logic, intuition is replaced by determining if a formula
is true in all executions of the protocol.
    This treatment of security goals relies heavily on a branch of first-order
logic called model theory. It deals with the relationship between descriptions
in first-order languages and the structures that satisfy these descriptions. In
our case, the structures are skeletons that denote a collection of executions
of a protocol. This paper attempts to describe the language of security goals
and its structures without requiring the reader to have studied model theory.
    The model theoretical foundation of this approach to security goals appears
 in [1]. A practical use of security goals in protocol standardization is
described in [2]. The precise semantics of the goal language is in [5, Appendix
 C]. The syntax of security goals appears in [4, Table 2].
    The distribution in which this paper is included contains the sample in-put
 cpsa file goals.scm. It contains the examples in this paper. You are
encouraged to run the examples and examine the output while reading this
paper.
    The cpsa Primer [4] is a prerequisite for reading this paper. In particular,
the Needham-Schroeder Protocol in Section 10 is reanalyzed using security
goals here. The roles are displayed in Figure 1.

   init     {|N1 , A|}KB          {|N1 , A|}KB    resp

     •      {|N1 , N2 |}KA       {|N1 , N2 |}KA    •

     •      {|N2 |}KB                {|N2 |}KB     •

```scheme
          (defprotocol ns basic
            (defrole init
              (vars (a b name) (n1 n2 text))
              (trace
               (send (enc n1 a (pubk b)))
               (recv (enc n1 n2 (pubk a)))
               (send (enc n2 (pubk b)))))
            (defrole resp
              (vars (b a name) (n2 n1 text))
              (trace
               (recv (enc n1 a (pubk b)))
               (send (enc n1 n2 (pubk a)))
               (recv (enc n2 (pubk b))))))
```
**Figure 1: Needham-Schroeder Initiator and Responder Roles**

```scheme
(defgoal ns                ; Goal
  (forall ((b name) (n1 text) (z0 strd))
    (implies
      (and (p "init" z0 3) (p "init" "n1" z0 n1)
        (p "init" "b" z0 b) (non (privk b)) (uniq n1))
      (exists ((z1 strd))
        (and (p "resp" z1 2) (p "resp" "b" z1 b))))))
```

```scheme
(defskeleton ns            ; Point of view skeleton
  (vars (a b name) (n1 n2 text))
  (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2))
  (non-orig (privk b))
  (uniq-orig n1))
```

                {|N1 , A|}KB                 {|N1 , A|}KB
      init                         ≺                           resp
               {|N1 , N2 |}KA                {|N1 , N2′ |}KA
       •                           ≻                             •
                 {|N2 |}KB
       •

```scheme
(defskeleton ns            ; Shape
  (vars (n1 n2 text) (a b name))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))
  (defstrand resp 2 (n2 n2-0) (n1 n1) (b b) (a a))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (non-orig (privk b))
  (uniq-orig n1)
  (satisfies yes))
```
**Figure 2: Needham-Schroeder Initiator Point of View**

    The protocol is analyzed from the point of view of a complete run of
one instance of the initiator role. The input security goal, followed by the
point of view skeleton it generates and the shape produced by cpsa, are
shown in Figure 2. The syntax and semantics of the goal will be explained
later. Roughly speaking, it asserts that if a realized skeleton contains a full
length initiator strand, its private key is uncompromised, and it uniquely
generates n1, then the skeleton will contain a responder strand that agrees
with the initiator on the name b. The shape produced by cpsa contains
the annotation (satisfies yes). This indicates that its structure satisfies
the description given by the security goal. It will be explained later why the
properties of cpsa allows us to conclude that this goal is true in all executions
of the protocol, and therefore conclude that the Needham-Schroeder protocol
achieves this authentication goal.

## 2. Security Goal Syntax (`defgoal` and Predicates)

To be precise, a security goal is an order-sorted first-order logic sentence
in a restricted form. The sentence in Figure 2 has the form shared by all
security goals. It is a universally quantified implication. The antecedent is
a conjunction of atomic formulas. For this sentence, the conclusion is an
existentially quantified conjunction of atomic formulas, but in general, the
conclusion is a disjunction of existentially quantified conjunctions of atomic
formulas. In what follows, (false) is a synonym for the empty disjunction,
(or).

```text
         goal     ←    (defgoal prot sent+ comments)
         sent     ←    (forall (decl∗) (implies antec concl))
        concl     ←    (false) | existl | (or existl∗)
        existl    ←    (exists (decl∗) antec) | antec
        antec     ←    atomic | (and atomic+)
```

    Variables are declared as they are for roles and skeletons with one exception
, there is a new sort symbol strd for strands. Notice that in the sentence
in Figure 2, variables z0 and z1 have sort strd. Every universally quantified
variable must occur in the antecedent of the implication.
    The signature as been expanded to include the natural numbers. A natural
 number has sort nat.

### 2.1 Full CPSA 4.4 Security Goal Grammar

**Table 7.1: Goal syntax. See Tables 10.3 and 10.5 for the algebra syntax, which defines the term and sort symbols.**

```text
               goal     ←    (defgoal id sentence+ alist)
          sentence      ←    (forall (gvdecl∗) implication)
            gvdecl      ←    (id+ sort) | (id+ strd) | (id+ indx)
              vmap      ←    (id id)
        implication     ←    (implies conjunction conclusion)
       conjunction      ←    conjunct | (and conjunct+)

achieves this authentication goal.

          conjunct      ←    atomic | (strand id strdvar integer (vmap∗))
                        |    (listener strdvar id)
         conclusion     ←    (false) | existential
                        |    (or existential+)
        existential     ←    conjunction | (exists (gvdecl∗) conjunction)
             atomic     ←    (p string strdvar integer)
                        |    (p string string strdvar term)
                        |    (prec strdvar index strdvar index)
                        |    (leads-to strdvar index strdvar index)
                        |    (non term) | (pnon term)
                        |    (uniq term) | (uniq-at term strdvar index)
                        |    (ugen term) | (ugen-at term strdvar index)
                        |    (conf term) | (auth term)
                        |    (= strdvar strdvar) | (= term term)
                        |    (gen-st term) | (trans strdvar index)
                        |    (comm-pr strdvar index strdvar index)
                        |    (state-node strdvar index)
                        |    (same-locn strdvar index strdvar index)
                        |    (component term term) | (fact id term*)
            strdvar     ←    symbol
              index     ←    symbol | integer
```

### 2.2 Goal Predicates

**Table 1: Predicates**

```text
 Symbol                 Sort          Description
 p role             strd × nat        Role strand length
 p role param      strd × mesg        Role parameter
 prec         strd × nat × strd × nat Precedes
 non                   atom           Non-origination
 pnon                  atom           Penetrator non-origination
 uniq                  atom           Unique origination
 uniq-at        atom × strd × nat     Unique origination on strand
 auth                  chan           Authenticated channel
 conf                  chan           Confidential channel
 =                    all × all       Equality
```

    The predicates used to construct an atomic formula (atomic) are listed in
Table 1. There are two classes of predicates, protocol specific and protocol
independent predicates, and two kinds of protocol specific predicates, role
strand length and role parameter predicates. Protocol specific predicates are
distinguished from protocol independent predicates by beginning with the
symbol p.
    The first line of the table gives the syntax of a role strand length predicate.
It contains two tokens, p and a string that names a role. That is, for role r,
there is a role strand length predicate, p r. Thus (p "init" z0 3) is an
atomic formula using the role strand length predicate for length 3 in the
init role of the protocol in Figure 1.
    The second line gives the syntax of a role parameter predicate. It contains
 three tokens, p, a string that names a role, and a string that names a
role variable. For role r, there is role parameter predicate for each variable
declared by r. Thus (p "init" "n1" z0 n1) is an atomic formula using the
role parameter predicate for parameter n1 in the init role of the protocol.
    The empty string names the listener role of a protocol. The role has the
variable x of sort mesg as its only role variable. There are two positions in
the listener role. Its trace is (trace (recv x) (send x)).
    When a variable of sort strd occurs in a formula, its length must be
specified using a role strand length formula. When an algebra variable occurs
in a formula, its association with the parameter of some role must be specified
using a role parameter formula.

### 2.3 Syntactic Abbreviations (`strand` and `listener`)

Section 7.2 described how cpsa extracts
      (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2))
from the following conjunction of facts
      (and (p "init" z0 3)
        (p "init" "n1" z0 n1) (p "init" "b" z0 b)).
    Using a conjunction of facts to represent a single defstrand is convenient for defining
and implementing a clear semantics, however it can be quite cumbersome and error prone
to specify these conjunctions. We therefore also provide support for syntactic sugar in the
goal language to allow users to represent these conjunctions in a manner much closer to the
defstrand form found in a skeleton. In particular, the user can write
      (strand init z0 3 (n1 n1) (b b))
as a single conjunct in a formula, and cpsa will ingest it with the same interpretation as if
the user had entered
      (and (p "init" z0 3)
        (p "init" "n1" z0 n1) (p "init" "b" z0 b)).
   Thus the goal in Fig. 7.1 could therefore be written as follows instead:
```scheme
      (defgoal ns
        (forall ((b name) (n1 text) (z0 strd))
          (implies
           (and (strand init z0 3 (n1 n1) (b b))
            (non (privk b)) (uniq n1))
           (exists ((z1 strd))
            (strand resp z1 2 (b b)))))).
    This representation has the benefit of being syntactically quite close to the skeleton
```
representation, and therefore the connection is more visually obvious to the user. Notice
the crucial difference that the (strand ...) form includes a strand variable after the name
of the role. While such a variable is not needed for skeletons, it is required in formulas to
allow other facts to reference the strand it represents.
    We also provide a similar abbreviation for listener strands. Instead of writing
      (and (p "" z0 1) (p "" "x" z0 n1))
we can write the following instead
      (listener z0 n1).
    These abbreviations can be used both in goals and in rules (described below in Section
 7.7).

## 3. Model-Theoretic Semantics and Characteristic Skeletons

In a defgoal sentence, the antecedent specifies the point of view skeleton.
We focus on the antecedent. In the example,

       (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2))

is extracted from

       (and (p "init" z0 3)
         (p "init" "n1" z0 n1) (p "init" "b" z0 b)).

Notice that cpsa adds a binding for a and n2 just as it does had

       (defstrand init 3 (b b) (n1 n1))

been given as input.
    Our aim now is to specify how to decide if a security goal is true in all
possible executions of a protocol. A skeleton defines a set of executions that
contain the skeleton’s structure. We say a skeleton satisfies a formula if the
skeleton contains all of the structure specified by the formula. To decide
if a skeleton satisfies a formula, we decide if it satisfies each of its atomic
formulas, and combine the results using the rules of first-order logic.
    Atomic formula (p "init" z0 3) is called a role strand length formula.
A skeleton k satisfies the formula if z0 maps to a strand s in k such that

    1. the trace of strand s in k has a length greater than 2, and

    2. the trace when truncated to length 3 is an instance of the init role.

Consider the shape in Figure 2. It satisfies (p "init" z0 3) when z0 maps
to 0.
    Atomic formula (p "init" "n1" z0 n1) is called a role parameter formula
. A skeleton k satisfies the formula if z0 maps to strand s in k, n1 first
occurs in at position i in the trace of the init role, and n1 maps to a message
algebra term t in k such that

    1. the trace of strand s in k has a length greater than i,

    2. the trace truncated to length i + 1 is an instance of the init role, and

  3. the truncated trace is compatible with mapping the init role’s "n1" role
     variable to t.

The shape in Figure 2 satisfies (p "init" "n1" z0 n1) when z0 maps to 0
and n1 maps to the message algebra term n1.
   Collectively, a skeleton satisfies the formula

     (and (p "init" z0 3)
          (p "init" "a" z0 a) (p "init" "b" z0 b)
          (p "init" "n1" z0 n1) (p "init" "n2" z0 n2))

if the skeleton contains the structure specified by

     (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2)).

   The antecedent in Figure 2 contains two origination assertions. The formula
 (non (privk b)) is extracted as (privk b). A skeleton k satisfies
the formula if b maps to a message algebra term t in k such that k assumes
that t is non-originating. The unique origination formula for n1 is similarly
extracted.
   Putting it all together, the mapping

                 {n1 7→ n1, n2 7→ n2, a 7→ a, b 7→ b, z0 7→ 0}

shows that the shape in Figure 2 satisfies the antecedent of the security goal.
    The prec predicate is used to assert a node precedes another node. The
conclusion in Figure 2 with (prec z1 1 z0 2) added is satisfied by the
shape using the mapping z0 7→ 0 and z1 7→ 1.
    The uniq-at predicate is used to assert not only that an atom uniquely
originates, but also the node at which it originates. In the Figure 2 goal, the
(uniq n1) formula could have been replaced by (uniq-at n1 z0 0). The
extracted point of view skeleton is the same.
    Recall that our aim in analyzing a protocol is to find out what security
goals are true in all of its possible executions. We are interested in runs of
cpsa that show that when every shape satisfies a goal, it is true in every
execution.
    When cpsa performs a shape analysis, every shape it generates refines
the input skeleton. Skeleton refinement is defined in [4, Section 6]. The
definition makes precise the notion of structure containment, as skeleton A
refines skeleton B if and only if A contains the structure of skeleton B.

    The skeleton k0 extracted from the antecedent of a security goal has the
property that a skeleton refines k0 if and only if it satisfies the antecedent.
A skeleton with this property is called the characteristic skeleton of the
antecedent.
    Given a goal Φ, consider a shape analysis starting from the characteristic
 skeleton k0 of its antecedent. Assume cpsa finds shapes k1 , . . . , kn and
that cpsa determines that each ki satisfies Φ. Consider the executions that
contain the structure in k0 . cpsa tells us that each execution is in the executions
 that contain the structure of some ki . Furthermore, because k0 is a
characteristic skeleton, each ki satisfies the antecedent of Φ. Executions that
do not contain the structure in k0 do not satisfy the antecedent. Therefore, Φ
is true in all executions of the protocol and maximally informative.

## 4. Authentication and Secrecy Goal Examples

This section contains examples of both authentication and secrecy goals.
The first example shows the feedback the user receives when a shape does
not satisfy a security goal. The second example shows how to use a listener
to state a secrecy goal.

### 4.1 Counterexample Analysis: Needham-Schroeder Responder (`satisfies no`)

Figure 3 contains an analysis of Needham-Schroeder from the point of view
of a complete run of the responder under the assumption that the responder’s
private key is uncompromised and the nonce it generates uniquely originates.
    The conclusion of the goal asserts that in an execution compatible with
the point of view, there must be an initiator strand that agrees with the
responder strand on the name b. The shape produced by cpsa is a counterexample
 to this assertion. Because of this, cpsa annotates the shape with

      (satisfies (no (a a) (b b) (n2 n2) (z0 0))).

The annotation includes a variable mapping for the shape that satisfies the
antecedent of the goal but does not satisfy its conclusion. The reason the
shape does not satisfy the goal is because the mapping (b b) maps the
initiator’s b parameter to b, not b-0 as is required to model the shape.
    Galvin Lowe identified this authentication failure in Needham-Schroeder
and provided a fix. In the Needham-Schroeder-Lowe Protocol, the name b

is included within the encryption in second message of both roles. With this
modification, the shape found by cpsa satisfies the security goal in Figure 3,
so Needham-Schroeder-Lowe achieves this authentication goal.

```scheme
(defgoal ns                ; Goal
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
      (and (p "resp" z0 3) (p "resp" "n2" z0 n2)
        (p "resp" "a" z0 a) (p "resp" "b" z0 b)
        (non (privk a)) (uniq n2))
      (exists ((z1 strd))
        (and (p "init" z1 2) (p "init" "b" z1 b))))))
```

```scheme
(defskeleton ns            ; Point of view skeleton
  (vars (a b name) (n1 n2 text))
  (defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2))
  (non-orig (privk a))
  (uniq-orig n2))
```

              {|N1 , A|}KB                {|N1 , A|}KB′
      resp                                                 init
             {|N1 , N2 |}KA               {|N1 , N2 |}KA
       •                        ≺                           •
               {|N2 |}KB                   {|N2 |}KB′
       •                        ≻                           •

```scheme
(defskeleton ns            ; Shape
  (vars (n1 n2 text) (a b b-0 name))
  (defstrand resp 3 (n2 n2) (n1 n1) (b b) (a a))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b-0))
  (precedes ((0 1) (1 1)) ((1 2) (0 2)))
  (non-orig (privk a))
  (uniq-orig n2)
  (satisfies (no (a a) (b b) (n2 n2) (z0 0))))
```
**Figure 3: Needham-Schroeder Responder Point of View**

### 4.2 Secrecy Goal with Listeners (`(false)` Conclusion)

Figure 4 contains an analysis of Needham-Schroeder from the point of view
of a complete run of the initiator under the assumption that the responder’s
and its peer’s private keys are uncompromised and the nonce n1 it generates
uniquely originates. Futhermore, the point of view asserts that the nonce is
leaked using a listener.

      (p "" z1 1) (p "" "x" z1 n1)           ; Listener

   cpsa finds no shapes, so Needham-Schroeder achieves this secrecy goal
and does not leak n1.

```scheme
      (defgoal ns
        (forall ((a b name) (n1 text) (z0 z1 strd))
          (implies
            (and (p "init" z0 3) (p "init" "n1" z0 n1)
              (p "init" "a" z0 a) (p "init" "b" z0 b)
              (p "" z1 1) (p "" "x" z1 n1) ; Listener
              (non (privk a)) (non (privk b))
              (uniq n1))
            (false))))
```
**Figure 4: Needham-Schroeder Secrecy Goal**

## 5. Multi-Sentence Goals, Skeleton `goals` Annotations, and Shape Analysis Sentences

The examples in the previous section demonstrate the typical way security
goals are analyzed with cpsa. However, there are more features that may
be useful.
   A defgoal form may contain more than one sentence. See Figure 5 for
an example. When presented with more than one sentence, cpsa extracts
the point of view skeleton from the first sentence.

```scheme
     (defgoal ns
       (forall ((a b name) (n text) (z0 strd))
         (implies
           (and (p "init" z0 2) (p "init" "n1" z0 n)
             (p "init" "a" z0 a) (p "init" "b" z0 b)
             (non (privk a)) (non (privk b)) (uniq n))
           (exists ((z1 strd))
             (and (p "resp" z1 2) (p "resp" "b" z1 b)))))
       (forall ((a b name) (n text) (z0 strd))
         (implies
           (and (p "init" z0 2) (p "init" "n1" z0 n)
             (p "init" "a" z0 a) (p "init" "b" z0 b)
             (non (privk a)) (non (privk b)) (uniq n))
           (exists ((z1 strd))
             (and (p "resp" z1 2) (p "resp" "a" z1 a))))))
```
**Figure 5: Two Initiator Authentication Goals**

    It is wise to ensure that the antecedent in every sentence is identical.
When cpsa performs satisfaction-checking on sentence Φ, it only determines
if each shape it finds is satisfied. If the point of view skeleton is not the
characteristic skeleton of the antecedent of Φ, the fact that all skeletons
satisfy Φ cannot be used to conclude that Φ is true in all executions of the
protocol.
    cpsa performs satisfaction-checking when an input skeleton in annotated
with one or more security goals. The annotation uses the goals key.

```scheme
     (defskeleton
        ...
        (goals sent+))
```

   The program cpsasas, discussed in the next section, can be used to
generate a formula with an antecedent such that the input skeleton is the
characteristic skeleton of the antecedent.

### 5.1 Shape Analysis Sentences (`cpsa4sas`)

A shape analysis sentence expresses all that can be learned from a run of
cpsa as a security goal. If a security goal can be derived from a shape
analysis sentence, then the protocol achieves the security goal, that is, the
goal is true in all executions of the protocol.
    The program cpsasas extracts shape analysis sentences from the output
of cpsa. Consider the first example in this paper (Figure 2), which is in the
sample file goals.scm. To generate a maximally informative security goal
from the initiator point of view with ghci and Make.hs, type
      $ ghci Make.hs
      *Make> sas "goals"
When using GNU make, type “make goals sas.text”. The resulting shape
analysis sentence is displayed in Figure 6.

```scheme
(defgoal ns
  (forall ((n1 n2 text) (b a name) (z strd))
    (implies
      (and (p "init" z 3) (p "init" "n1" z n1)
        (p "init" "n2" z n2) (p "init" "a" z a)
        (p "init" "b" z b) (non (privk b)) (uniq-at n1 z 0))
      (exists ((n2-0 text) (z-0 strd))
        (and (p "resp" z-0 2) (p "resp" "n2" z-0 n2-0)
          (p "resp" "n1" z-0 n1) (p "resp" "b" z-0 b)
          (p "resp" "a" z-0 a) (prec z 0 z-0 0)
          (prec z-0 1 z 1))))))
```
**Figure 6: Initiator Shape Analysis Sentence**

   A shape analysis sentences asserts that either a realized skeleton does
not satisfy its antecedent or it satisfies one or more of the disjuncts in its
conclusion. cpsa has been designed so that this assertion is true. Therefore,
every shape analysis sentence is true in all executions.
   A security goal is true in all executions if it can be derived from a shape
analysis sentence [3]. In practice, theorem-proving using shape analysis sentences
 is rarely employed. It’s clumsy and it requires too much expertise. The
main use of cpsasas is for generating a formula that is edited to become a
desired security goal.

## 6. Axiomatic Rewrite Rules (`defrule`) and Facts (`facts`)

Support for rules was introduced in version 4.1 of cpsa.
   Each protocol includes a small collection of rules. A rule is a sentence in
the goal language presented in Section 2. Rules are defined after the roles of
a protocol are defined. The syntax of a rule follows.

              rule    ←   (defrule name sent comments)

    A rule is an axiom added to a protocol. cpsa uses the axiom as a rewrite
rule to derive zero or more new skeletons from a skeleton produced during a
step. An example of a protocol with a rule is in Figure 9 on Page 18.
    The trust rule states that when CPSA finds a person strand of length
at least one, and the inverse of it’s p parameter is non-originating, CPSA
should assume the inverse of it’s d parameter is non-originating.

### 6.1 Skeleton Fact Databases (`facts` and `fact`)

Each skeleton includes a small database of facts. A fact is a named relation
among fact terms. A fact term is either a strand of the skeleton or an algebra
term. A set of facts is defined anywhere after strands are defined using the
facts form. The syntax of facts follows.

                      facts ← (facts fact∗)
                       fact ← (symbol fterm∗)
                     fterm ← mesg | nat

   For example, in a skeleton, a user may want to note that strand 0 owns
the private key for a by assuming.

                      (facts (owns 0 (privk a)))

    Facts are most useful when combined with rules. Here is an example of
their combination. Suppose a point of view skeleton has two names, a and b,
and the problem is modeling a situation in which the two names are known
to differ. To enforce this constraint, add
                            (facts (neq a b))
to the point of view skeleton and the neq rule below to the protocol.

```scheme
      (defrule neq
        (forall ((a mesg))
          (implies
            (fact neq a a)
            (false))))
```

### 6.2 Case Study: Door Simple Example Protocol (DoorSEP) and Trust Axioms

As a motivating scenario consider the Door Simple Example Protocol
(DoorSEP), derived from an expository protocol that was designed to have
a weakness. Despite this, the protocol achieves the needs of an application,
given a trust assumption.
    Imagine a door D which is equipped with a badge reader, and a person P
equipped with a badge. When the person swipes the badge, the protocol
executes. Principals such as doors or persons are identified by the public
parts of their key pairs, with D−1 and P −1 being the corresponding private
keys. We write {|M |}K for the encryption of message M with key K. We
represent digital signatures {|M |}P −1 as if they were the result of encrypting
with P ’s private key.
    P initiates the exchange by creating a fresh symmetric key K, signing
it, and sending it to the door D encrypted with the door’s public key. D
extracts the symmetric key after checking the signature, freshly generates
a token T , and sends it—encrypted with the symmetric key—back to P .
P demonstrates they are authorized to enter by decrypting the token and
sending it as plaintext to the door. The two roles of DoorSEP are shown in
Fig. 7, where each vertical column displays the behavior of one of the roles.
The cpsa4 encoding of the roles is in Figure 9.

                        person                               door
                      {|{|K|}P −1 |}D                    {|{|K|}P −1 |}D
               •                            /                              /•
                         {|T |}K                            {|T |}K         
  Fresh: K     •o                                    o                      •    Fresh: T
                                                                            
               •
                            T           /                      T           /•
**Figure 7: DoorSEP Protocol**

    cpsa finds an undesirable execution of DoorSEP. Assume the person’s

private key P −1 is uncompromised and the door has received the token it
sent out. Then cpsa finds that P freshly created the symmetric key K.
However, nothing ensures that the person meant to open door D. If P ever
initiates a run with a compromised door C, the adversary can perform a
man-in-the-middle attack, decrypting using the compromised key C −1 and
re-encrypting with D’s public key, as elided in the · · · in Fig. 8. To verify
this result with cpsa4, remove the trust axiom in the doorsep protocol in
doc/rules.scm and run cpsa4. Thus, without additional assumptions, the
door cannot authenticate the person requesting entry.

              person                                                 door
                        {|{|K|}P −1 |}C            {|{|K|}P −1 |}D
                 •                        / ···                      /•
                                                       {|T |}K         
                                               o                      •
                                                                       
                                                         T           /•

                       Uncompromised: P            Fresh: K, T
**Figure 8: DoorSEP Weakness**

    But possibly we can trust the person to swipe her badge only in front of
doors our organization controls. And we can we ensure that our doors have
uncompromised private keys. If so, then the adversary cannot exercise the
flaw.
    We regard this as a trust assumption, and we can express it as an axiom:

Trust Assumption 1 If an uncompromised signing key P −1 is used to pre-pare
 an instance of the first DoorSEP message, then its owning principal has
ensured that the selected door D has an uncompromised private key.

The responsibility for ensuring the truth of this axiom may be split between
P and the organization controlling D. P makes sure to swipe her badge
only at legitimate doors of the organization’s buildings. The organization
maintains a security posture that protects the corresponding private keys.
Is DoorSEP good enough, assuming the trust axiom? Add the trust
axiom back to the doorsep protocol in doc/rules.scm and see. You should
find that the protocol does its job; namely, ensuring that the door opens only
when an authorized person requests it to open.

```scheme
(defprotocol doorsep basic
  (defrole person
    (vars (d p akey) (k skey) (t text))
    (trace
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t)))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t)))
  (defrule trust
    (forall ((z strd) (p d akey))
            (implies
             (and (p "person" z 1)
                  (p "person" "p" z p)
                  (p "person" "d" z d)
                  (non (invk p)))
             (non (invk d))))
    (comment "The trust rule"))
  (comment "Doorsep protocol using unnamed asymmetric keys"))
```

```scheme
(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (comment "Analyze from the doors’s perspective"))
```
**Figure 9: Door Simple Example Protocol**

## 7. Automatically Generated Rules (`defgenrule`), Built-in Relations, and Trace Annotations

### 7.1 Built-in Fact Relations (`neq`, `invk`, `lt`, `subsort`) and Generated Rules

cpsa generates certain rules either automatically in all cases or else as a consequence of
user inputs. The rules generated for a given protocol input may be found in the printed
output for that protocol; these are the formulas appearing in defgenrule forms in the .txt
and .xhtml files.

```scheme
(defprotocol doorsep basic
  (defrole person
    (vars (d p akey) (k skey) (t text))
    (trace
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t)))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t)))
  (defrule trust
    (forall ((z strd) (p d akey))
            (implies
             (and (p "person" z 1)
                  (p "person" "p" z p)
                  (p "person" "d" z d)
                  (non (invk p)))
             (non (invk d))))
    (comment "The trust rule"))
  (comment "Doorsep protocol using unnamed asymmetric keys"))
```

```scheme
(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (comment "Analyze from the doors’s perspective"))
```
**Figure 7.8: Door Simple Example Protocol**

```scheme
(defrule trust-sometimes
   (forall ((z strd) (p d akey))
           (implies
            (and (fact use-trust-rule)
                 (p "person" z 1)
                 (p "person" "p" z p)
                 (p "person" "d" z d)
                 (non (invk p)))
            (non (invk d))))
   (comment "The trust rule. Assume (fact use-trust-rule) to enable it"))
```

. . .

```scheme
(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (facts (use-trust-rule))
  (comment "Analyze from the doors perspective, with trust rule"))
```
**Figure 7.9: Rule with a flag to control its use**

Negated equalities. Since negated equalities are often needed to express assumptions
users are interested in, cpsa generates three rules with the body:

(implies (fact neq x x)
         (false))

This rule has the effect of terminating a branch of analysis if two expressions that the
user has stipulated should not be equal become unified to the same value. Three rules
are generated since the variable x may be of sort mesg, or of sort strd for a strand in the
skeleton, or of sort indx meaning the index of a node along a strand. To stipulate a negated
equality between two expressions e1 , e2 , the user may write in the input file:

```scheme
(defskeleton protocol
   . . . strand declarations, etc. . . .
   (facts (neq e1 e2 )))
```

Negated equality assertions may also appear in the conclusions of user-defined rules, or
anywhere else that an atomic formula may appear.
    A good number of additional rules are generated to implement cpsa’s model of state
(see Section 8.2, esp. Figs. 8.4–8.5 and pp. 89–90).

“Assume” declarations. A formula may be provided after the trace declaration in a
defprotocol declaration in an assume clause. For instance:1

```scheme
(defrole init
    (vars ...)
    (trace ...)
    ...
    (assume (fact neq (exp (gen) upsilon) (gen))))
```

In this case, the cpsa loader checks that all of the free variables (just upsilon here) appear
in the trace. If i is the first height at which all of the variables have occurred, cpsa
generates a rule stating that any instance of the rule of height ≥ i satisfies this property of
the instances of the role parameters. In this case, i = 4, so the generated formula states:

(defgenrule assume-init-0
    (forall ((z strd) (upsilon expt))
      (implies (and (p "init" z 4) (p "init" "upsilon" z upsilon))
        (fact neq (exp (gen) upsilon) (gen)))))

Here, the assumption is the uninterpreted predicate symbol neq applied to two expressions
. However, the assumption may also involve conjunction and existential quantifiers.
       See the file dhcr_um_expt_assume.scm in the manual examples directory.

cpsa also permits disjunctions, but these typically cause unreasonable branching and bad
performance.
   In case the assumption is a fact, such as the neq assertion above, one can write

```scheme
(defrole init
    (vars ...)
    (trace ...)
    ...
    (facts (neq (gen) (exp (gen) upsilon))))
```

instead of writing the assume annotation above. Many facts may be listed as clauses here,
with the effect of a conjunction. The keyword here is the plural facts, and the singular
fact does not appear in the individual clauses.
    The facts annotation may also appear in a defskeleton query.

```scheme
(defskeleton dhcr-um
  (vars (a b name) (beta expt))
  (defstrand init 5 (a a) (b b) (beta beta))
  (non-orig (privk "sig" b))
  (facts (neq a b) (undisclosed beta)))
```

Currently, cpsa does not recognize the assume keyword in defskeleton queries.

### 7.2 Trace Annotations (`cheq`, `assume`, `rely`, `guarantee` / `guar`) and `cpsa4goals`

cpsa now allows a few types of annotations to be interspersed within the trace declaration
within a role. These are:

rely, used after a reception to declare a formula containing only free variables appearing
      up to and including this reception. Every instance of the role long enough to include
      a successful instance of this reception must satisfy the formula;

guar, used before a transmission to declare a formula containing only free variables appearing
 up to and including the following transmission. Every instance of the role long
     enough to include an instance of the following transmission must satisfy the formula.

All of these trace annotations will cause similar rules to be generated. Trace annotations
do not add to the height of the trace. They simply express constraints on what happens in
the “real” events around them.

Expressing rely and guarantee statements. In work on trust management, and on
compiling cryptographic protocols [9, 7, 11], we introduced the idea of a rely formula that
expresses what a principal learns when a message is received, possibly assuming that certain
peers are uncompromised. We also introduced the idea of a (dual) guarantee formula that

must be true in order for a principal to transmit a message. In particular, if a message
sent by a principal A has a particular guarantee formula ϕ, and a peer B receives it and
authenticates its origin with A in this step of the protocol, then B may rely on a formula
with the meaning, A says ϕ.
    This example will be sound in the sense that the authentication property ensures that
A really did say (i.e. guarantee) ϕ in any execution in which B relies on the claim. The
soundness of rely statements may be checked by analyzing the protocol with the rely state-ments
 omitted, and querying them as goal statements under the relevant non-compromise
assumptions. We will now assume that this soundness checking has been done, and that
any relevant non-compromise assumptions are made in the protocol definition.
    Thus, a rely formula definitely holds true whenever the principal successfully completes
the preceding receive event. Indeed, the operational interpretation of a rely formula is
that the principal will add an assertion to a database of its knowledge. cpsa transforms
a rely formula after a reception which is at height i in a trace into a rule stating: “long-enough
” instances of the role will satisfy the formula, for that instance’s values of the role
parameters.
    This transformation is similar to what cpsa does for a cheq annotation, except that
instead of an equation, the conclusion may involve other atomic formulas, conjunctions,
and existential quantifiers. Disjunctions are permitted, but will usually lead to intractable
cpsa analysis.
    A guarantee formula has a dual relation with a subsequent transmission. Just as the
received message may determine the instances of parameters appearing in a rely formula,
a guarantee formula may dually select instances of parameters that will appear in the
subsequent transmission. As a rely formula is interpreted operationally as an assert to a
database held by the principal, a guarantee formula is interpreted operationally as a query
against that database. Hence, assertions caused by previous rely formulas may influence
the parameter instances selected by subsequent guarantee formulas.

A rely-guarantee example. Consider a protocol in which a customer will interact with
a merchant and a bank to purchase an item at a cost; the merchant will be paid by a debit
from the customer’s account at the bank. Each participant should obtain evidence that
the expected peers are participating in a corresponding session. Moreover, the merchant
does not need to know the customer’s account number, and therefore should not see this
information. The bank does not need to know what item the customer is buying, and
therefore should not see that. Outsiders should not see the details at all. How best to
achieve this goal?
    Each party will need to generate a digital signature, since in case of dispute a third
party must be able to reconstruct who committed to paying whom, and to sending what
merchandise. Moreover, public key encryption will be needed, at least for a handshake,
since the parties must protect secrets from the outsiders and from the third party. Thus,
there is no way to avoid having three digital signatures generated, along with a similar

number of public key encryptions, with corresponding verification and decryption actions.
A protocol that achieves this goal is found in examples/minipay.scm.
    Each party is making assertions, in effect. The customer asserts his desire to buy the
item for the cost. The bank asserts that it will transfer the funds to the merchant. The
merchant asserts that it will ship the item. Moreover, the protocol should ensure that each
party knows that the others have made these commitments. For instance, the merchant is
willing to ship the goods because it knows that the bank will transfer the payment. Thus,
each party makes a guarantee, and each party learns that it may rely on its peers having
made their guarantee. A fine point is the bank’s rely formula; it learns that the customer
has requested some item in exchange for the cost, but not which one. Thus, the item is
existentially bound in the bank’s rely formula.
    This yields the rely and guarantee formulas displayed in Fig. 7.10; the protocol with
these trust annotations may be found in examples/minipay-rely-guar.scm. The principals
 in a particular session are required not to proceed past a guarantee formula unless the
instances of the variables are known to satisfy the property claimed. The rely formulas
summarize what they have learned in the preceding reception.
    But: How do we know these formulas are in fact true in every execution that includes
the preceding reception, or at least every execution satisfying some reasonable assumptions
about uncompromised keys?
    We can use goal formulas to check this. In a separate file, examples/minipay-guar.scm,
we define the protocol with the same message structure and guarantee formulas, but with
no rely formulas. We now pose goal statements for cpsa to resolve; these are shown in
Fig. 7.11–7.12. In these formulas, the conclusions are the rely statements that must be
justified. The hypotheses say that there is a strand z instantiating the relevant role long
enough to reach the rely statement position. They also connect the variables in the rely
formula with the parameters of z. Moreover, each customer goal assumes only the relevant
peer’s signature key to be non-compromised. The merchant assumes only the bank’s signing
key non-compromised, which is desirable since it may have no long-term association with
the customer. The bank presumably has an association with the customer, established
when the customer opened the account; the customer’s signing key could be established at
that time.
    The goals may be constructed from the generated rules cpsa provides when processing
 examples/minipay-rely-guar.scm, essentially adding the non-compromise assumptions
.
    Since cpsa validates these goal formulas in the minipay-guar protocol that contains
the guarantee formulas but not the rely formulas, the generated rules introduced by the
rely formulas are also sound subject to the stated non-compromise assumptions.
    We regard this rely-guarantee method as a systematic way to formalize the trust assumptions
, and the effects, of protocols that accomplish real-world tasks, in this case purchase
and payment.

```scheme
(defrole cust (vars ...)
  (trace
    (guar (fact buy-via c m b item cost n))
    (send ...)
    (recv ...)           ; from bank
    (rely (fact will-transfer c m b cost n mtr btr))
    (recv ...)           ; from merchant
    (rely (fact will-ship c m b item mtr))))
```

```scheme
(defrole merc (vars ...)
  (trace
    (recv ...)           ; from customer
    (send ...)
    (recv ...)           ; from bank
    (rely (and (fact buy-via c m b item cost n)
               (fact will-transfer c m b cost n mtr btr)))
    (guar (fact will-ship c m b item mtr))
    (send ...)))
```

```scheme
(defrole bank (vars ...)
  (trace
    (recv ...)
    (rely (exists ((item merchandise))
                  (fact buy-via c m b item cost n)))
    ;; Do not proceed unless customer signature trustworthy.
    ;; Given that, now commit to transferring the funds
    (guar (and (non (privk "sig" c))
               (fact will-transfer c m b cost n mtr btr)))
    (send ...)))
```
**Figure 7.10: Rely and gauantee formulas in minipay.scm**

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (cost amount) (n data) (mtr btr text))
   (implies
    (and (p "cust" z 2)
         (p "cust" "c" z c)
         (p "cust" "m" z m)
         (p "cust" "b" z b)
         (p "cust" "cost" z cost)
         (p "cust" "n" z n)
         (p "cust" "mtr" z mtr)
         (p "cust" "btr" z btr)
         (non (privk "sig" b)))
    (fact will-transfer c m b cost n mtr btr))))
```

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (item merchandise) (n data) (mtr btr text))
   (implies
    (and (p "cust" z 3)
         (p "cust" "c" z c)
         (p "cust" "m" z m)
         (p "cust" "b" z b)
         (p "cust" "item" z item)
         (p "cust" "n" z n)
         (p "cust" "mtr" z mtr)
         (p "cust" "btr" z btr)
         (non (privk "sig" m)))
    (fact will-ship c m b item mtr))))
```
**Figure 7.11: Goal statements to validate customer’s rely formulas**

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (item merchandise) (cost amount) (n data) (mtr btr text))
   (implies
    (and (p "merc" z 3)
         (p "merc" "c" z c)
         (p "merc" "m" z m)
         (p "merc" "b" z b)
         (p "merc" "item" z item)
         (p "merc" "cost" z cost)
         (p "merc" "n" z n)
         (p "merc" "mtr" z mtr)
         (p "merc" "btr" z btr)
         (non (privk "sig" b)))
    (and (fact will-transfer c m b cost n mtr btr)
         (fact buy-via c m b item cost n)))))
```

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (cost amount) (n data))
   (implies
    (and (p "bank" z 1)
         (p "bank" "c" z c)
         (p "bank" "m" z m)
         (p "bank" "b" z b)
         (p "bank" "cost" z cost)
         (p "bank" "n" z n)
         (non (privk "sig" c)))
    (exists ((item merchandise))
            (fact buy-via c m b item cost n)))))
```
**Figure 7.12: Goal statements to validate other rely formulas**

## 8. Lemmas (`deflemma`)

One common way in which rules have been used in cpsa is as lemmas. The analyst would
define a goal as a query and run cpsa to check that the goal is satisfied. Then the goal
can be added to the protocol as a rule to help speed up the search for subsequent queries.
One common example is when cpsa repeatedly undergoes a long search to satisfy a listener
for some key that cannot be satisfied. Validating once and for all that the key cannot be
leaked, and then including that fact as a rule can drastically improve performance.
    Unfortunately, the syntax for doing so was not particularly friendly to the user. The
formula stated as a defgoal query resides outside the protocol, while the defrule version
 must be included inside the protocol. Managing these lemmas could become difficult
as there was no built-in management to help determine which rules had previously been
validated as lemmas that hold.
    For this reason, cpsa also includes a deflemma form. It must be place outside the
protocol at the top level, just as a defgoal form. However, the syntax for a lemma differs
slightly from that of a goal in ways that allow cpsa to help manage the complexities that
arise from sometimes wanting to validate a formula as a goal and sometimes wanting to use
it as a rule. The user should look at tst/lemmas.scm for an example of the syntax.
    Compared to a defgoal, a deflemma has two extra arguments that come at the beginning
. The first is a flag that signals to cpsa whether or not it should include a query for
the lemma in order to validate that it is satisfied. There are three valid values: rule, goal,
and both. The second is a name that will be used as the rule name when the lemma is
used as a rule.
    When a lemma uses the rule flag, cpsa will update the protocol identified in the
lemma to include the specified formula as a rule. As a result, all subsequent queries for
that protocol will include the lemma as a rule. cpsa will not generate a query for the
lemma. The result is the same as if a copy of the protocol with the same name had been
added in this location with an extra defrule added to it (hence only subsequent queries
would use the rule).
    The goal flag signals cpsa to treat the lemma as if it were a defgoal. A query will be
added to the analysis, but it will not be included as a rule in any subsequent queries. The
skeletons in the analysis contain a comment indicating the name of the lemma the analysis
is associated with.
    When the both flag is used, the behavior is first to treat the lemma as a goal, and then
as a rule. cpsa will first create a query for the lemma against the specified protocol before
updating the protocol to include the lemma as a rule for subsequent queries.
    Since cpsa updates the protocol with a rule at load time, it cannot know in advance
whether the lemma is satisfied or not. That means that subsequent queries will use the
lemma as a rule, even if the query for the lemma shows that the lemma is not satisfied ! For
this reason, the added rule contains a comment to indicate whether or not an associated
query has been added to check its validity. When the both flag is used for a lemma that is

not satisfied, since a query for the formula is generated as a goal, the output will contain
(satisfies (no ...)) as evidence that some goal was not satisfied.

## 9. Formal Specification of Shape Analysis Sentences (Coherent Logic)

For each point-of-view skeleton and its shapes found by cpsa, there is a
formula in a language of order-sorted first-order logic called  W a shape analysis
 sentence. The sentence has a special form, ∀X(Ψ ⊃ i ∃Yi (∆i ∧ Φi )),
where Ψ, ∆i , and Φi are conjunctions of atomic formulas and X and Yi are
variable sets. This fragment of first-order logic is called coherent logic. Formula
 Ψ describes the point-of-view skeleton k0 . For each homomorphism to
               δi
a shape, k0 7−→   ki , formula ∆i describes the structure preserving maps δi ,
and the shape ki is described by Φi .
    An interpretation of a shape analysis sentence is a skeleton. If cpsa finds
all of the shapes and the homomorphisms associated with a point-of-view
skeleton, the analysis’ sentence is satisfied in all realized skeletons. Let Σ be
a shape analysis sentence and Ψ be a security goal. If Σ ⊃ Ψ is a theorem in
order-sorted first-order logic, then Ψ is satisfied in all realized skeletons and
its protocol achieves this goal.
    Shape analysis sentences are closely related to security goals in [7], and
were motivated by that work. This material was extracted from [11], the
paper that introduced shape analysis sentences.

### 9.1 Formal Syntax and Satisfaction Semantics of Skeleton Formulas
The signature for security goal terms extends the one used for the underlying
message algebra with sort Z. Variables of this sort denote strands.
   Security goals make use of protocol specific and protocol independent
predicates. For each role rY (C, N, U ) ∈ P , there are strand length predicates

and strand parameter predicates. There are |C| unary length predicates
P [r, h] : Z, with 1 ≤ h ≤ |r|. Relative to skeleton k, P [r, h](z) asserts
that strand z in k is an instance of r and has a length of at least h. For
each variable x : S that occurs in C, there is a binary parameter predicate
P [r, x] : Z × S. Relative to skeleton k, P [r, x](z, t) asserts that strand z in k
is an instance of r in which x is instantiated as t.
    For each base sort B, there are unary predicates non : B and uniq : B.
non(t) asserts t is non-originating in k and uniq(t) asserts t uniquely originates
in k.
    Let m be the length of the longest role in P . There are m2 precedence
predicates prec[i, j] : Z × Z for 0 ≤ i, j < m. prec[i, j](x, y) asserts that node
(x, i) is before node (y, j) in k. There are 3m origin predicates uniq-at[i] :
B ×Z, with 0 ≤ i < m and B as before. uniq-at[i](t, z) asserts that t uniquely
originates in k at node (z, i). The predicate false has arity zero and, of course,
equality is binary.
    To improve the readability of formulas to follow, we write prec(x, i, y, j)
for prec[i, j](x, y) and uniq-at(t, z, i) for uniq-at[i](t, z).
    Let k = kX (P, I, ≺, N, U ) and let ≺− be the transitive reduction of ≺.
Recall that ΘX is the strand space defined by I, see Section 5.4. We de-fine
 F(k) = (Y, Φ), where Φ is k’s skeleton formula, and Y is the formula’s
variable set. For F(k) = (Y, Φ), the variable set Y is X augmented with a
fresh variable of sort Z for each strand in k. Let Z(s) be the strand variable
associated with strand s ∈ Dom(I).
    The formula Φ is a conjunction of atomic formulas composed as follows.
   • For each s ∈ Dom(I), let I(s) = i(r, h, σ) and z = Z(s). Assert
     P [r, h](z). Let r = r(C, N, U ). For each variable x ∈ Vars(C † h) and
     term t = σ(x), assert P [r, x](z, t).
   • For each (s, i) ≺− (s′ , i′ ) such that s ̸= s′ , assert prec(Z(s), i, Z(s′ ), i′ ).
   • For each t ∈ N , assert non(t).
   • For each t ∈ U and (s, i) ∈ Ok (t), assert uniq-at(t, Z(s), i).
   • For each t ∈ U without a point of origination in k, assert uniq(t).
   Given a set of homomorphisms δi : k0 7→ ki , its shape analysis sentence is
                                             _
               S(δi : k0 7→ ki ) = ∀X0 (Φ0 ⊃   ∃Xi (∆i ∧ Φi )),         (C.1)
                                                   i

        ∀a0 , b0 : A, s0 : S, d0 : D, z0 : Z(
          resp 2 (z0 ) ∧ resp a (z0 , a0 ) ∧ resp b (z0 , b0 )
               ∧ resp s (z0 , s0 ) ∧ resp d (z0 , d0 )
               ∧ non(a−1 0 ) ∧ non(b0 )
                                        −1

          ⊃
          ∃a1 , b1 , b2 : A, s1 : S, d1 : D, z1 , z2 : Z(
              z0 = z1 ∧ a0 = a1 ∧ b0 = b1 ∧ s0 = s1 ∧ d0 = d1
                 ∧ resp 2 (z1 ) ∧ resp a (z1 , a1 ) ∧ resp b (z1 , b1 )
                 ∧ resp s (z1 , s1 ) ∧ resp d (z1 , d1 )
                 ∧ init 1 (z2 ) ∧ init a (z2 , a1 ) ∧ init b (z2 , b2 ) ∧ init s (z2 , s1 )
                 ∧ uniq-at(s1 , z2 , 0) ∧ prec(z2 , 0, z1 , 0)
                 ∧ non(a−1                −1
                           1 ) ∧ non(b1 )))

       Figure C.1: Shape Analysis Sentence for Blanchet’s Protocol

where F(k0 ) = (X0 , Φ0 ). The same procedure produces Xi and Φi for
shape ki with one proviso—the variables in Xi that also occur in X0 must be
renamed to avoid trouble while encoding the structure preserving maps δi .
    The structure preserving maps δi = (ϕi , σi ) are encoded in ∆i by a conjunction
 of equalities. Map σi is coded as equalities between a message algebra
 variable in the domain of σi and the term it maps to. Map ϕi is coded as
equalities between strand variables in Φ0 and strand variables in Φi . Let Z0
be the strand variables freshly generated for k0 , and Zi be the ones generated
for ki . The strand mapping part of ∆i is
                             ^
                                   Z0 (s) = Zi (ϕi (s)).
                              s∈Dom(Z0 )

    The shape analysis sentence for the second analysis of Blanchet’s Simple
 Example Protocol in Section 5.1 is displayed in Figure C.1. The strand
length predicate P [r, h](z) is written rh (z), and the strand parameter predicate
 P [r, x](z, t) is written rx (z, t) with the protocol left implicit.

#### 9.1.1 Semantics of Skeleton Formulas (`k, α |= Φ`)

**Semantics of Skeleton Formulas.** Let k = kX (P, I, ≺, N, U ) and ΘX be
its strand space. When formula Φ is satisfied in skeleton k with order-sorted
variable assignment α, we write k, α |= Φ. For x : S ∈ X, α(x) is in the
carrier set of ĀX for sort S. For x : Z, α(x) ∈ Dom(ΘX ). We write ᾱ when α

is extended to terms in the obvious way. When sentence Σ is satisfied in
skeleton k, we write k |= Σ.

   • k, α |= P [r, h](z) iff h ≤ |ΘX (s)|, and for some σ,

                                 ΘX (s) † h = σ ◦ C † h

      where s = α(z) and r = r(C, N, U ).

   • k, α |= P [r, x](y, t) iff for some σ with σ(x) = ᾱ(t),

                                 ΘX (s) † h = σ ◦ C † h

      where s = α(z), r = r(C, N, U ), and h is the smallest ℓ such that x
      occurs in C † ℓ.

   • k, α |= prec(x, i, y, j) iff (α(x), i) ≺ (α(y), j).

   • k, α |= non(t) iff ᾱ(t) ∈ N .

   • k, α |= uniq(t) iff ᾱ(t) ∈ U .

   • k, α |= uniq-at(t, z, i) iff ᾱ(t) ∈ U and (α(z), i) ∈ Ok (ᾱ(t)).

   • k, α |= y = z iff ᾱ(y) = ᾱ(z).

    Let Σ be a shape analysis sentence and Ψ be a security goal. If Σ ⊃ Ψ is
a theorem in order-sorted first-order logic, then Ψ is satisfied in all realized
skeletons and its protocol achieves this goal.

#### 9.1.2 Channel Formulas (`auth` and `conf`)

**Channel Formulas.** This appendix has not been updated to reflect the
inclusion of channels into cpsa, but the changes made are straightforward.
There are two new unary predicate symbols, auth and conf, that are similar
to non except their argument must be a variable of sort chan. For skeleton k
and variable assignment α, auth(c) is satisfied iff α(c) ∈ auth(k), and conf(c)
is satisfied iff α(c) ∈ conf (k).

## 10. References
[1] Joshua D. Guttman. Establishing and preserving protocol security goals.
    Journal of Computer Security, 22(2):201–267, 2014.

[2] Joshua D. Guttman, Moses D. Liskov, and Paul D. Rowe. Security goals
    and evolving standards. In Liqun Chen and Chris Mitchell, editors, Security
 Standardization Research, volume 8839 of LNCS, pages 93–110.
    Springer, December 2014.

[3] John D. Ramsdell. Deducing security goals from shape analysis sentences.
    The MITRE Corporation, April 2012. http://arxiv.org/abs/1204.
    0480.

[4] John D. Ramsdell and Joshua D. Guttman. CPSA Primer. The MITRE
    Corporation, 2009. In https://github.com/mitre/cpsaexp source distribution
, doc directory.

[5] John D. Ramsdell, Joshua D. Guttman, Moses D. Liskov, and Paul D.
    Rowe. The CPSA Specification: A Reduction System for Searching for
    Shapes in Cryptographic Protocols. The MITRE Corporation, 2009. In
    https://github.com/mitre/cpsaexp source distribution, doc directory.
````

---

### `refrences/cpsa_kb/02_manuals/05_CPSA_Specification_and_User_Guide.md`

*sha256:`7c75b7d2f76b` · 3029 lines · 148.0 KB (~37,052 tokens) · lang:`markdown` · 22 control chars sanitized*

````markdown
# CPSA 4.4 Formal Specification and User Guide (`cpsauser` & `cpsaspec`)

*Authors: John D. Ramsdell, Joshua D. Guttman, Moses D. Liskov, Paul D. Rowe (The MITRE Corporation)*

---

## Table of Contents

- **Part I: CPSA 4.4 User Guide and Companion Tools (`cpsauser`)**
  - [1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage](#1-cpsa-44-user-guide-inputoutput-syntax-and-solver-usage)
    - `1.1 Input/Output Syntax Overview`
    - `1.2 Protocols (defprotocol and defrole)` & `1.2.1 Algebra Signature Extensions (lang)`
    - `1.3 Skeletons (defskeleton, defstrand, deflistener)`
    - `1.4 First-Order Logic and Security Goals (defgoal)`
    - `1.5 Rewrite Rules (defrule and facts)`
    - `1.6 Long-Term (Cross-Session) State (locn, load, stor, gen-st, leadsto)`
    - `1.7 Macros (defmacro) and File Includes (include)`
    - `1.8 CPSA Command-Line Usage (cpsa4 Flags and Options)`
    - `1.9 Search Order Options (check-nonces, try-old-strands, reverse-nodes)`
  - [2. CPSA Companion Tools Reference](#2-cpsa-companion-tools-reference)
    - `2.1 cpsa4init` | `2.2 cpsa4graph` | `2.3 cpsa4diff` | `2.4 cpsa4shapes` | `2.5 cpsa4sas` | `2.6 cpsa4goalsat` | `2.7 cpsa4prot` | `2.8 cpsa4pp` | `2.9 cpsa42latex` | `2.10 cpsa4json` | `2.11 cpsa4query` | `2.12 cpsa4db & Prolog` | `2.13 cpsa4dl` | `2.14 S-Expression Syntax`
- **Part II: The CPSA Formal Specification (`cpsaspec`)**
  - [3. The CPSA Formal Specification (`cpsaspec`)](#3-the-cpsa-formal-specification-cpsaspec)
  - [Spec Chapter 1: Introduction to the CPSA Reduction System](#spec-chapter-1-introduction-to-the-cpsa-reduction-system)
  - [Spec Chapter 2: Order-Sorted Message Algebras](#spec-chapter-2-order-sorted-message-algebras)
  - [Spec Chapter 3: Strand Spaces and Bundles](#spec-chapter-3-strand-spaces-and-bundles)
  - [Spec Chapter 4: Adversary Model](#spec-chapter-4-adversary-model)
  - [Spec Chapter 5: Preskeletons, Skeletons, and Homomorphisms](#spec-chapter-5-preskeletons-skeletons-and-homomorphisms)
  - [Spec Chapter 6: Algorithms as Reduction Systems](#spec-chapter-6-algorithms-as-reduction-systems)
  - [Spec Chapter 7: Primitive Preskeleton Operators](#spec-chapter-7-primitive-preskeleton-operators)
  - [Spec Chapter 8: Reductions on Preskeletons (Thinning, Hulling, Compression)](#spec-chapter-8-reductions-on-preskeletons-thinning-hulling-compression)
  - [Spec Chapter 9: Penetrator Derivability (`Tp : Ta |- t`)](#spec-chapter-9-penetrator-derivability-tp--ta---t)
  - [Spec Chapter 10: Carried Only Within (`cows`)](#spec-chapter-10-carried-only-within-cows)
  - [Spec Chapter 11: Solving Authentication Tests and Cohort Augmentation](#spec-chapter-11-solving-authentication-tests-and-cohort-augmentation)
  - [Spec Chapter 12: Collapsing and Preconditioning](#spec-chapter-12-collapsing-and-preconditioning)
  - [Spec Chapter 13: Generalization (Deletion, Weakening, Separation, Forgetting)](#spec-chapter-13-generalization-deletion-weakening-separation-forgetting)
  - [Spec Chapter 14: Complete Skeleton Reduction System (`->>k`)](#spec-chapter-14-complete-skeleton-reduction-system--k)
  - [Appendix A: Penetrator Non-Origination Assumptions (`pen-non-orig`)](#appendix-a-penetrator-non-origination-assumptions-pen-non-orig)
  - [Appendix B: Programs Specified by a Role (Procedural Dataflow Relation)](#appendix-b-programs-specified-by-a-role-procedural-dataflow-relation)
  - [Appendix C: Shape Analysis Sentences](#appendix-c-shape-analysis-sentences)
  - [Appendix D: Facts and Rules](#appendix-d-facts-and-rules)
  - [Bibliography](#bibliography)

---

## 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage

### 1.0 Overview of CPSA Shape Analysis

The Cryptographic Protocol Shapes Analyzer (CPSA) attempts to enumerate all
essentially different executions possible for a cryptographic protocol. We call
them the shapes of the protocol. Naturally occurring protocols have only
finitely many, indeed very few shapes. Authentication and secrecy properties
are easy to determine from them, as are attacks and anomalies.

For each input problem, the CPSA program is given some initial
behavior, and it discovers what shapes are compatible with
it. Normally, the initial behavior is from the point of view of one
participant. The analysis reveals what the other participants must
have done, given the participant's view. The search is based on a
high-level algorithm that was claimed to be complete, i.e. every shape
can in fact be found in a finite number of steps. Further theoretical
work showed classes of executions that are not found by the algorithm,
however it also showed that every omitted execution requires an
unnatural interpretation of a protocol's roles.  Hence the algorithm
is complete relative to natural role semantics.

The analyzer is designed to work well with other
  tools. S-expressions are used for both input and output. The
  analyzer reads all the problems in its input, writes out the
  solution to each problem, and then exits. This release contains nine
  tools.  The  `cpsa4init`  program
  copies a Makefile and a Haskell script for use
  with  `ghci`  into the current directory.  They orchestrate
  the use of the other tools.
  The  `cpsa4graph`  program
  provides a visualization of answers using Scalable Vector Graphics
  (SVG).
  The  `cpsa4shapes`  program
  removes intermediate results from analyzer runs making the shapes
  easy to identify.
  The  `cpsa4diff`  program compares
  CPSA output files S-expression by S-expression, and prints the first
  skeleton that differs.
  The  `cpsa4sas`  program logical
  formula that can be used to ensure security goals are achieved.
  The  `cpsa4goalsat`  program
  prints skeletons that do not satisfy the goal associated with the
  point of view skeleton.  The
   `cpsa4prot`  program translates
  protocols expressed in Alice and Bob notation into
  CPSA's  `defprotocol`  syntax.
   `cpsa4pp`  program pretty prints its
  input using a CPSA specific algorithm.  It also translates
  S-Expressions into JavaScript Object Notation
  (JSON) to ease processing in other
  languages.  The
   `cpsa4json`  program translates
  JSON encoded CPSA into CPSA
  S-Expressions. The  `cpsa4query` 
  program queries CPSA output as derivation trees.
  The  `cpsa4db` 
  and  `cpsa4dbprolog`  programs
  translate CPSA output into Prolog so it can be analyzed using the
  power and flexibility of Prolog.
  The  `cpsa4dl`  program generates
  Prolog queries written in a dynamic logic.
  Finally,
  the  `cpsa42latex`  program
  translates CPSA macros into equivalent LaTeX macros.

The input syntax is essentially the same as the output syntax. A
  Lisp aware editor will pretty print input, and the output is pretty
  printed. We use Emacs' Scheme mode to prepare input. This document
  describes the syntax, but provides little assistance for its
  interpretation. See the CPSA Primer and
  CPSA Security Goals and Rules for more
  information.

The typical pattern of usage is to enter the set of problems to be analyzed
into a file, in this example,  `prob.scm` , analyze the problems, and if
something interesting is produced, visualize the answers.

   `$ cpsa4 +RTS -M512m -RTS -o prob.txt prob.scm
$ cpsa4graph -o prob.xhtml prob.txt
$ firefox -remote "openFile(`pwd`/prob.xhtml)"` 

Often a summary of the analysis is more enlightening.

   `$ cpsa4shapes -o prob_shapes.txt prob.txt
$ cpsa4graph -o prob_shapes.xhtml prob_shapes.txt
$ firefox -remote "openFile(`pwd`/prob_shapes.xhtml)"` 

 The  `cpsa4init` 
  program creates the
  file  `cpsa4.mk`  for inclusion into
  your makefile. A sample makefile is also created.  The
  file  `cpsa4prolog.pl`  is
  also added to facilitate the analysis of outputs using Prolog.

The CPSA program
  is Emacs friendly.
  If you run the above  `makefile`  via "M-x
  compile", the results will be displayed in a buffer in
  Compilation Mode.  The command "C-x `" will visit
  the locus of the next error message or match ( `next-error` )
  in your CPSA input file.

For platforms without GNU  `make` , the Haskell
 program  `make4.hs`  can be loaded
 into a Haskell interpreter and perform a similar function. Users are
 expected to copy the makefile or the Haskell program into the
 directory containing a set of analysis problems
 using  `cpsa4init` , and then modify
 a file so it specifies the command line flags appropriate for the
 problems in the directory.

### 1.1 Input/Output Syntax Overview
The syntax is extensible. Association lists in which the key is always a
symbol are allowed at various points in the grammar. Key-value pairs with
unrecognized keys are ignored, and are available for use by other tools. On
output, unrecognized key-value pairs are preserved when printing protocols, but
elided when printing skeletons, with the exception of the  `comment` 
key.

The input is an option herald form followed by a sequence of
protocol definitions and problem statements.
A herald form allows options normally specified
on the command line to be specified within an input file.  A problem
statement describes the initial behavior as a skeleton or a security
goal.

### 1.2 Protocols (`defprotocol` and `defrole`)
The grammar for a protocol follows.

   `PROTOCOL   ::= (defprotocol ID ALG ROLE+ RULE* PROT-ALIST)
ID         ::= SYMBOL
ALG        ::= SYMBOL
ROLE       ::= (defrole ID VARS TRACE ROLE-ALIST)
VARS       ::= (vars DECL*)
DECL       ::= (ID+ SORT)
TRACE      ::= (trace EVENT+)
EVENT      ::= (send TERM) | (send ID TERM) | (stor ID TERM)
            |  (recv TERM) | (recv ID TERM) | (load ID TERM)
ROLE-ALIST ::= (non-orig POS-TERM*) ROLE-ALIST
            |  (pen-non-orig POS-TERM*) ROLE-ALIST
            |  (uniq-orig TERM*) ROLE-ALIST
            |  (uniq-gen TERM*) ROLE-ALIST
            |  (conf ID*) ROLE-ALIST
            |  (auth ID*) ROLE-ALIST
            |  (priority POS-INT*) ROLE-ALIST
	    |  (gen-st TERM+) ROLE-ALIST
            |  (critical-sections POS-INT+) ROLE-ALIST
	    |  (facts FACTS*) ROLE-ALIST | ...
POS-TERM   ::= TERM | (INT TERM)
POS-INT    ::= (INT INT)
RULE       ::= (defrule ID SENTENCE RULE-ALIST)
RULE-ALIST ::= ...
PROT-ALIST ::= (lang LDECL*) PROT-ALIST | ...
LDECL      ::= (ID+ KIND)
KIND       ::= atom | akey | hash | (tuple INT)
            |  enc | senc | aenc | sign` 

The syntax for  `SORT` ,  `TERM` ,
  and  `SENTENCE`  will be presented later.

The protocol  `ID`  is a symbol that names the protocol, and the role
 `ID`  is a symbol that names the role. The  `ALG` 
symbol identifies the algebra used by the protocol. For the Basic
Cryptographic Algebra, the symbol is  `basic` .
The  `var`  form contains symbols that declare the sort of
the variables used in this role. The set of sort symbols is algebra
specific, but must include  `mesg` 
and  `chan` .

Events specify message transmission ( `send` ) or
  reception ( `recv` ).  A message can be sent on a channel
  using the form  `(send ID TERM)`  where  `ID`  is
  declared to be of sort  `chan` , and similarly for message
  receptions.  A state value may be received or loaded from a location
  using the form  `(stor ID TERM)`  where  `ID`  is
  declared to be of sort  `locn` .  Every store event
  must be in a group consisting of a number of loads followed by a
  number of stores.  Moreover, each  `locn`  in a store
  event must have had a load event earlier in that group.

The protocol association list has no predefined keys, while the
role association list has nine predefined keys. The value associated
with  `non-orig, pen-non-orig, uniq-orig, uniq-gen, conf, auth`  must
be atoms in the algebra. Each  `non-orig`  term must not be
carried by any event in the role's trace, but each of its variables
must occur in some term.  A role non-origination assumption of the
form  `(3 a)`  asserts that atom  `a`  will not be
mapped into an instance unless its height is greater than three.  For
each  `pen-non-orig`  term, each of its variables must occur
in some term, but unlike a non-origination assumption, the term may be
carried.  Each  `uniq-orig`  term must originate in the
role's trace.  Each  `uniq-gen`  term must generate in the
role's trace.  Each  `conf`  term must be a channel variable,
and it asserts the channel is confidential.  Each  `auth` 
term must be a channel variable, and it asserts the channel is
authenticated.  Each  `gen-st`  must be a term loaded in the
role.  It entails that the instances of these terms are not initial
values, and they must be explained by a previous store event on some
strand.  Each  `critical-section`  designates the start and
end of a group of loads and stores that must occur atomically.  It is
not needed when there is only one load and at most one store in the
group of events.  And it is not needed if the events are not assumed
to occur atomically.  Each  `facts`  declaration ensures
that, whenever an instance of the role proceeds long enough to have
chosen parameter values for each parameter that appears in the facts,
the corresponding instance of the fact will be inferred.  Every
variable of sort  `mesg`  must be acquired by the role's
trace.

The structure of sorts and terms in the Basic Cryptographic Algebra
follows.

   `SORT ::= text | data | name | skey | akey | mesg | chan | locn
TERM ::= ID | AKEY | (ltk ID ID) | STRING
      |  (cat TERM+) | (enc TERM+ TERM) | (hash TERM+)
AKEY ::= ID | (invk AKEY) | (pubk ID) | (privk ID)
      |  (pubk STRING ID) | (privk STRING ID)` 

The form ( `cat`  a b c d e) is expands to
  ( `cat`  a ( `cat`  b ( `cat`  c
  ( `cat`  d e)))).  The form ( `enc`  a b c d e) is
  expands to ( `enc`  ( `cat`  a b c d) e).

A term in the Basic Crypto Algebra is an atom if it is a variable
  of a sort other than  `mesg` , or it if formed from one of
  the following
  operations:  `pubk` ,  `privk` ,  `invk` ,
  and  `ltk` .

The Diffie-Hellman algebra adds three
  sorts:  `rndx` ,  `expt` , and  `base` .
  Variables of sort  `rndx`  are considered atoms.  The new
  terms are  `BASE` :

   `BASE ::= ID | (gen) | (exp BASE EXPT)
EXPT ::= ID | (one) | (mul EXPT EXPT) | (rec EXPT)` 

#### 1.2.1 Algebra Signature Extensions (`lang`)
The signature of the message algebra used by CPSA is extensible.
  There are two forms of extensibility provided by CPSA.  Users can add
  operations for encryption, tupling, and hashing; and add sorts for
  atomic data.

A common extension is to add tupling operations to message algebras.
  Previously, complex protocols often made use of tagged concatenation
  to encode a tagged sequence of messages.  In CPSA, concatenation is
  implemented as sequences of pairing operations.  Thus, the expression
  for a certificate body of the form

   `(cat "cert-body" dn serial-no pub-key)` 

is syntax for

   `(cat "cert-body" (cat dn (cat serial-no pub-key)))` 

Algebra extensions are declared using the  `lang`  key in
  the protocol's association list, at the end of a protocol.  For the
  certificate body example,

   `(defprotocol cert basic
  ...
  (lang (cert-body (tuple 3))))` 

adds one tupling operation so that the example above can be written as

   `(cert-body dn serial-no pub-key)` 

CPSA represents this form internally as sequence of messages with a
  distinguished mark.  This representation is more efficient as compared
  with the tagged concatenation representation.

   `LANG  ::= (lang LDECL*)
LDECL ::= (ID+ KIND)
KIND  ::= atom | akey | hash | (tuple INT)
       |  enc | senc | aenc | sign` 

The syntax of a  `lang`  declaration is given above.
There are eight kinds of ways that CPSA algebras can be extended.

* An atomic sort is added to the algebra when a symbol is declared
    to be of kind  `atom` .  If  `dollar`  is
    declared to be an atomic sort, than  `(price dollar)`  in
    a  `var`  form declares  `price`  to be of
    sort  `dollar` .

* An atomic sort is also added to the algebra when a symbol is
    declared to be of kind  `akey` .  However, in addition to
    adding the sort, CPSA adds the equation  `(invk (invk x)) =
    x`  for variables of the new sort.

* A unary operation is added to the algebra when a symbol is
    declared to be of kind  `hash` .  As with the default
    hash operation, the adversary cannot extract the contents of the
    hash.

* An N-ary operation is added to the algebra when a symbol is
    declared to be of kind ( `tuple`  N).  As with
    concatenation, the adversary can construct and extract contents of
    tuples.  N must be positive.

* A binary operation is added to the algebra when a symbol is
    declared to be of kind  `enc` .  As with the default
    encryption operation, the adversary cannot extract contents of the
    encryption without access to the inverse of the key.

* A symbol of kind  `senc`  is just like one of kind
     `enc`  except that the key supplied when it is applied
    must be symmetric.

* A symbol of kind  `aenc`  is just like one of kind
     `enc`  except that the key supplied when it is applied
    must be asymmetric.

* A symbol of kind  `sign`  is just like one of kind
     `enc`  except that the key supplied when it is applied
    must be the inverse applied to an asymmetric key.

### 1.3 Skeletons (`defskeleton`, `defstrand`, `deflistener`)
   `SKELETON   ::= (defskeleton ID VARS STRAND+ SKEL-ALIST)
STRAND     ::= (defstrand ID INT MAPLET*) | (deflistener TERM)
MAPLET     ::= (TERM TERM)
SKEL-ALIST ::= (non-orig TERM*) SKEL-ALIST
            |  (pen-non-orig TERM*) SKEL-ALIST
            |  (uniq-orig TERM*) SKEL-ALIST
            |  (uniq-gen TERM*) SKEL-ALIST
            |  (conf ID*) SKEL-ALIST
            |  (auth ID*) SKEL-ALIST
            |  (precedes NODE-PAIR*) SKEL-ALIST
            |  (facts FACTS*) SKEL-ALIST
            |  (priority NODE-INT*) SKEL-ALIST | ...
NODE-PAIR  ::= (NODE NODE)
NODE       ::= (INT INT)
FACT       ::= (ID FTERM*)
FTERM      ::= TERM | INT` 

The  `ID`  in the skeleton form names a protocol. It refers to the last
protocol definition of that name which precedes the skeleton form. The
 `ID`  in the strand form names a role. The integer in the strand form
gives the height of the strand. The sequence of pairs of terms in the strand
form specify an environment used to construct the messages in a strand from its
role's trace. The first term is interpreted using the role's variables and the
second term uses the skeleton's variables. The environment used to produce the
strand's trace is derived by matching the second term using the first term as a
pattern.

The first integer in a node identifies a strand, and the second one
specifies the position of the node in the strand. Zero-based indexing is used.
Zero identifies the first strand, and the first node in a strand has position
zero.

A variable may occur in more then one role within a protocol. The
reader performs a renaming so as to ensure these occurrences do not
overlap.  Furthermore, the maplets used to specify a strand need not
specify how to map every role variable. The reader inserts missing
mappings, and renames every skeleton variable that also occurs in a
role of its protocol. The sort of every skeleton variable that occurs
in the  `non-orig` ,  `pen-non-orig` ,
 `uniq-orig` ,  `uniq-gen` ,  `conf` ,
or  `auth`  list or in a maplet must be declared.

On output, key-value pairs are added to all skeleton's association list.
Every skeleton in the output is labeled with a unique identifier with
 `(label INT)`  A skeleton has  `(parent INT)`  if it is a member of
the cohort of the identified parent. A skeleton has  `(seen INT+)`  when
members of its cohort are isomorphic to previously seen skeletons. A skeleton
lists its unrealized nodes with  `(unrealized NODE*)` . The traces
associated with each strand is given by the  `(traces ...)`  form.
Finally, the operation used to derive this skeleton from its parent is recorded
with  `(operation TEST KIND TERM NODE TERM*)` , where  `TEST`  is the
authentication test  `encryption-test` ,  `nonce` ,
or  `channel-test` ;  `KIND` 
is  `(added-strand ID INT)` ,
 `(displaced INT INT ID INT)` ,
 `(contracted MAPLET*)` ,
 `(added-listener TERM)` ;
 `TERM`  is the critical term;
 `NODE`  in the test node;
and the remaining terms specify the escape set.
When the operation kind is augmenting, the instance's role name and height are
provided.
For kind displacing, the first number is the strand being merged, the
second number is the strand it was merged into, and the remaining give
the new instance's role name and height.
For kind listening, a term is provided. For kind contracting, the
substitution is provided. When a substitution refers to a variable not in the
skeleton, its name is unpredictable. For generalization, the operation is
recorded as  `(operation generalization METHOD)` , where  `METHOD` 
is one of  `deleted NODE` ,  `weakened NODE-PAIR` ,  `separated
TERM`  and  `forgot TERM` . Generalization is used to find shapes from
realized skeletons. For shape collapsing, the operation is recorded as
 `(operation collapsed INT INT)` , where the two  `INT` s identify
the strands merged. Shape collapsing is used to find related shapes.

### 1.4 First-Order Logic and Security Goals (`defgoal`)
Another way to specify a problem statement is with a security
  goal. A security goal a sentence in first-order logic.  It asserts
  that if some properties hold for a skeleton, then some other
  properties must hold for all shapes computed by CPSA starting with
  the skeleton.  Security goals can be used to formally state
  authentication and secrecy goals of a protocol.

The  `defgoal`  form is used to pose an analysis problem
  with a sentence instead of a skeleton.  CPSA extracts a point of
  view skeleton from the antecedent of the formula and then analyzes
  it.  When a  `defgoal`  form has a sequence of sentences,
  they must all contain the same antecedent.  CPSA will evaluate all
  of the conclusions during the analysis of this shared antecedent.
  When it prints a shape, it checks to see if the shape satisfies the
  conclusions of the security goal sentences.  When invoked with
  the  `goals-sat`  option, CPSA will successfully terminate
  any branch of its analysis as soon as the conclusions of the goals
  are satisfied.  See
  CPSA Security Goals and Rules for
  details.

To be precise, a security goal is an order-sorted first-order logic
  sentence in a restricted form.  The set of sort symbols available
  for use in a  `DECL`  is the ones provided by the message
  algebra augmented with the symbol  `strd` .  The form of a
  sentence is restricted by the syntax that follows.

   `GOAL        ::= (defgoal ID SENTENCE+ GOAL-ALIST)
SENTENCE    ::= (forall (DECL*) (implies ANTECEDENT CONCLUSION))
CONCLUSION  ::= (false) | EXISTENTIAL | (or EXISTENTIAL*)
EXISTENTIAL ::= (exists (DECL*) ANTECEDENT) | ANTECEDENT
ANTECEDENT  ::= ATOMIC | (and ATOMIC+)
ATOMIC      ::= (p ROLEID SVAR HGT) | (p ROLEID PARAM SVAR TERM)
             |  (prec SVAR POS SVAR POS) | (non TERM) | (pnon TERM)
             |  (uniq TERM) | (uniq-at TERM SVAR POS)
             |  (ugen TERM) | (ugen-at TERM SVAR POS)
             |  (conf ID) | (auth ID)
	     |  (gen-st TERM) | (comm-pr SVAR POS SVAR POS)
	     |  (same-locn SVAR POS SVAR POS) | (state-node SVAR POS)
	     |  (trans SVAR POS) | (leads-to SVAR POS SVAR POS)
             |  (fact ID TERM*) | (= TERM TERM)
ROLEID      ::= STRING
HGT         ::= INT
POS         ::= INT | ID
SVAR        ::= ID
PARAM       ::= STRING` 

An atomic formula asserts that a skeleton has some property.  The
  formula  `(p "init" s 3)`  asserts that
  strand  `s`  in the skeleton is an instance of
  an  `init`  role and is of length 3 or greater.  The
  formula  `(p "init" "x" s y)`  asserts that
  strand  `s`  is an instance of an
   `init`  role and is of a length that is great enough so
  that role parameter  `x`  occurs in the role, and the role
  parameter  `x`  is instantiated to become
  term  `y` .  Formula  `(prec (x 2) (y 1))` 
  asserts that for some strands  `x`  and  `y`  in
  the skeleton, the transitive closure of the precedence relation
  contains the mentioned pair of nodes.  Formula  `(non t)` 
  asserts  `t`  is assumed to be non-originating in the
  skeleton.  Predicates  `pnon`  and  `uniq`  have
  similar interpretations. The formula  `(fact foo s (invk
  t))`  asserts the skeleton contains a fact
  called  `foo`  relating a strand to the inverse of some term.
  The formula  `(= s t)`  asserts that  `s` 
  and  `t`  refer to the same object in the skeleton.

The empty string names the listener role of a protocol.  The
  role has the variable  `x`  of sort  `mesg` 
  as its only role variable. There are two positions in the listener
  role.

  `gen-st`  asserts that its argument is a generated state
  value, and cannot be an initial value.   `comm-pr`  asserts
  that the two nodes that follow are a transmission-reception pair
  with the same message.   `same-locn`  asserts that the two
  nodes that follow are state nodes involving the same
  location.   `same-locn`  asserts that the node that follows
  is a state node.   `trans`  asserts that the node that
  follows is a transition node rather than a pure
  observation.   `leads-to`  asserts that the two nodes that
  follow are a transmission and a reception on the same location that
  are immediately related, ie no other transition comes between them.

### 1.5 Rewrite Rules (`defrule` and `facts`)
Each protocol may include a small collection of rules.  A rule is
  written using the language of security goals.

A rule is an axiom added to a protocol.  CPSA uses the axiom as a
  rewrite rule to derive zero or more new skeletons from a skeleton
  produced after each analysis step.  A protocol with a rule
  follows.

 `(defprotocol doorsep basic
  (defrole person
    (vars (d p akey) (k skey) (t text))
    (trace
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t)))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t)))
  (defrule trust
    (forall ((z strd) (p d akey))
            (implies
             (and (p "person" z 1)
                  (p "person" "p" z p)
                  (p "person" "d" z d)
                  (non (invk p)))
             (non (invk d))))
    (comment "The trust rule"))
  (comment "Doorsep protocol using unnamed asymmetric keys"))

(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (comment "Analyze from the doors's perspective"))` 

The trust rule states that when CPSA finds a person strand of
  length at least one, and the inverse of it's  `p` 
  parameter is non-originating, CPSA should assume the inverse of
  it's  `d`  parameter is non-originating.

### 1.6 Long-Term (Cross-Session) State (`locn`, `load`, `stor`, `gen-st`, `leadsto`)
Some protocols manipulate state.  Key management protocols acquire
secrets and certificates, and store them so that subsequent rules can
use them.  Hardware security modules store keys and other data, and
use them in a succession of controlled ways, some of which modifies
the data.  Many other examples arise.

CPSA supports long-term state using two basic event forms,
namely  `(load l term)`  and  `(stor l term)` .
A  `load`  event acquires the piece of state in
location  `l`  of sort  `locn` .  The
term  `term`  in  `(load l term)`  constrains the
value in  `l`  at the time this event occurs.  That value
must have the form of  `term` , and any variables
within  `term`  that are already bound constrain the value
found there.  All remaining variables are newly bound here, and will
constrain the subsequent occurrences.

A  `(stor l term)`  event places the value
of  `term`  into location  `l`  so that
subsequent  `load` s will receive it.  We say that
a  `stor`  event on location  `l`  leads to
a  `load`  event on the same location  `l`  if the
latter happens immediately after; CPSA formalizes this internally by
creating a special value (a "point") that originates uniquely at
each  `stor`  and must match in an immediately
subsequent  `load`  event.  There may be several immediately
subsequent  `load`  events, since several events may observe the
value without causing a transition.  A transition consists of a pair
of adjacent events, one which  `load` s the current value,
followed by another the  `stor` es the subsequent value.
There can be at most one transition to which a
single  `stor`  event leads.

Internally, CPSA regards a location  `l`  of
sort  `locn`  as a kind of channel.  It is a confidential
channel, since the location remains within the device, and the
adversary can obtain the value only via message transmissions.  It is
not a channel with (full) authenticity, since we regard initial values
as always being available.  However, any value that is non-initial
must be generated by a previous transition; i.e. a location offers
authenticity for values known to be non-initial.

We formalize this using a  `gen-st`  predicate in the rule
language.  CPSA uses the formula  `(gen-st term)`  to assert
that  `term`  is definitely non-initial, and requires a
(regular)  `(stor l term)`  event to explain it being
available in location  `l` .  Rules with this kind of
conclusion allow CPSA to infer these formulas when needed.

Within a role definition, a declaration  `(gen-st term-1
... term-i)`  causes CPSA to generate rules that establish that
each of the terms given is  `gen-st`  as long as a role
instance is long enough for the variables in it to be
well-defined.

### 1.7 Macros (`defmacro`) and File Includes (`include`)
After reading the input,  `cpsa4`  expands macros before analyzing
the results. A macro definition is a top-level form.

   `(defmacro (NAME ARG*) BODY)` 

The  `cpsa4`  program expands all calls to macros in
non-macro defining S-expressions using the macros that have been
defined previously. A macro definition can be used to expand a call if
the first element of a list matches the name of the macro, and the
length of the remaining elements in the list matches the length of the
macro's argument list. When two macros definitions are applicable, the
last definition takes precedence. The  `cpsa4`  program omits
macro definitions from its output.

After expanding a list, elements of the list of the
  form  `(^`  ... `)`  are spliced into the output.
  Thus  `(a ^(b c) d)`  becomes
   `(a b c d)`  after macro expansion.

A source file can be included within another with the top-level
include form,

   `(include FILE)` 

where  `FILE`  is a string. The  `cpsa4`  program
includes files while it does macro expansion.

### 1.8 CPSA Command-Line Usage (`cpsa4` Flags and Options)
   `$ cpsa4 -h
Usage: cpsa4 [OPTIONS] [FILE]
  -o FILE    --output=FILE      output FILE
  -l INT     --limit=INT        step count limit (default 2000)
  -b INT     --bound=INT        strand count bound (default 12)
  -d INT     --depth=INT        tree depth bound (default unbounded)
  -m INT     --margin=INT       set output margin (default 72)
  -e         --expand           expand macros only; don't analyze
  -n         --noisochk         disable isomorphism checks
  -c         --check-nonces     check nonces first
  -t         --try-old-strands  try old strands first
  -r         --reverse-nodes    try younger nodes first
  -g         --goals-sat        Stop when goals are satisfied
  -a STRING  --algebra=STRING   algebra (default basic)
  -s         --show-algebras    show algebras
  -h         --help             show help message
  -v         --version          show version number` 

This program will abort if too many steps are taken. A skeleton is
printed for each step taken by the program. The step count limit
option is used to override the default step count limit. It will also
abort when it detects a skeleton with too many strands. The strand
count bound option is used to override the default strand count
bound. The tree depth bound option is used to override the default
tree depth bound.  Another way to limit resources used by the program
is to limit the amount of memory it may use. The command-line
option  `+RTS -M512m -RTS`  limits memory usage to 512m.

The herald form can be used to specify options within a file.  The
  grammar for a herald form follows, where  `ALIST`  is an
  association list with symbols as keys.

   `HERALD ::= (herald TITLE ALIST)
TITLE  ::= SYMBOL | STRING` 

The title is used by  `cpsa4graph`  when generating XHTML.
  In the following example, the herald form specifies a strand bound
  of 12 in a way that is equivalent to the command line
  option  `--bound=12` .

   `(herald "Needham-Schroeder Public-Key Protocol" (bound 12))` 

The herald form is only interpreted by the  `cpsa4`  program,
  and is treated as a comment by all other programs.  In particular,
  specifying a  `margin`  option effects  `cpsa4`  only.

For long running problems, SMP parallelism is available. For example, on a
quad-core machine, we would probably use  `+RTS -N4 -RTS` .

In addition to the options provided on the command line or a herald
  form, one can influence the order in which test nodes are sought.
  When a role includes  `(reverse-search)`  in its association
  list as a comment, the nodes in its instances will be searched in
  reverse order.

When run with isomorphism checks disabled ( `--noisochk` ), CPSA
searches for realized skeletons, not shapes. It attempts to speed up analysis
by not identifying duplicate skeletons or generalizing realized skeletons,
however in many cases, run times increase. It is used when normal analysis
takes too much time on the chance that avoiding the checks makes more progress.

In no isomorphism checking mode output, every realized skeleton is labeled a
shape even when it is not. This allows the extraction of every realized
skeletons from the output using the  `cpsa4shapes`  program.

An error message that begins with "No test for unrealized node" identifies a
severe error that should be reported as a bug.

### 1.9 Search Order Options (`check-nonces`, `try-old-strands`, `reverse-nodes`)
In its analysis, CPSA will attempt to solve unrealized nodes until the
skeleton is realized, and then generalize until a shape is obtained.  When
there are multiple unrealized nodes, by default, CPSA will chose the topmost,
rightmost unrealized node among those unrealized nodes with maximum priority.
The default priority of a node is 5, and higher numbers represent a higher
priority.  When a node has non-positive priority, it is left unsolved.

In a role, in order to specify a priority for an event other than
the default, add a comment of the
form  `(priority (i p))` ,
where i is the index of the event in the trace,
and p is the priority.
Priorities are inherited
from roles, but may be overridden in a skeleton with a
 `priority`  comment of the form
 `(priority (n p))` ,
where n is a node.

## 2. CPSA Companion Tools Reference

### 2.1 Project Initialization (`cpsa4init`)
The  `cpsa4init`  copies the
  files  `Makefile` ,  `cpsa4.mk` ,
  and  `Make4.hs`  into the current directory.  It will not
  overwrite existing files of the same name.  The makefile is for use
  with systems that provide GNU  `make` .  Windows users should
  load  `Make4.hs`  into  `ghci` .  Read the
  comments in the script for usage instructions.

#### Usage
   `$ cpsa4init -h
Usage: cpsa4init [OPTIONS]
  -h       --help          show help message
  -v       --version       show version number` 

### 2.2 Visualization (`cpsa4graph`)
The  `cpsa4graph`  program produces a graphical rendering of the output
or input of an analyzer using SVG. It is viewable only with a
standards-compliant web browser such as FireFox.

When applied to the output of CPSA, the program groups together all the
skeletons related to each problem statement in the input. The program assembles
the related skeletons into a directed acyclic graph using the parent identifier
and renders it as a tree using SVG. Each vertex in the tree is the label added
to the skeleton by the CPSA program. Click the label in the tree to view the
skeleton. Hover over a node in a skeleton drawing to see the term associated
with it. Hover over a role to see the mapping from role variables to skeleton
variables.

A node ordering edge in a skeleton drawing indicates that the message
transmission at the source of the edge happened before message reception at the
destination edge. The edge is solid if the transmitting term is syntactically
identical to the receiving term, otherwise the edge is dashed. Thus in an
algebra with a commutative operation  `*` , the graphing program sometimes
draws a dashed line between  `(send (* a b))`  and  `(recv (* b
a))` .

In the tree drawing, the label of a shape is blue, and the label of
  a realized skeleton that is not a shape is grey. For dead
skeletons, the label is red, unless it has been seen before, in which
case it is orange. Otherwise the label is green for skeletons seen
before. Seen skeleton labels are rendered in an italic font.

By the default,  `cpsa4graph`  generates a view of CPSA S-expressions as
a compound document that contains SVG within XHTML. This view integrates
graphics with the input text.

In compact mode,  `cpsa4graph`  generates an SVG document. The tree is
displayed immediately to the left of skeleton drawings. When there is more than
one tree, the left-hand-side of the drawing contains a vertical listing of the
trees. Compact mode output should never be used as a replacement for studying
the text version of the output. The text version contains strictly more
information, and should be displayed next to its graphical rendition.

In LaTeX mode,  `cpsa4graph`  generates LaTeX source. XY-pic is used for
drawings of skeletons. The margin specified in  `cpsa4.mk`  produces good results. 

#### Usage
   `$ cpsa4graph -h
Usage: cpsa4graph [OPTIONS] [FILE]
  -o FILE  --output=FILE   output FILE
  -x       --expanded      use expanded format (default)
  -z       --zoom          enable diagram scaling
  -t       --treeless      use treeless expanded format
  -c       --compact       use compact format
  -l       --latex         use LaTeX format
  -m INT   --margin=INT    set output margin (default 72)
  -p       --purge-traces  purge traces
  -h       --help          show help message
  -v       --version       show version number` 

### 2.3 Output Comparisons (`cpsa4diff`)
The  `cpsa4diff`  program compares CPSA output files
S-expression by S-expression, and prints the first skeleton that
differs.

#### Usage
   `$ cpsa4diff -h
Usage: cpsa4diff [OPTIONS] OLD-FILE NEW-FILE
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

### 2.4 Shape Extraction (`cpsa4shapes`)
The  `cpsa4shapes`  program extracts the original problems and the
shapes from the output of a CPSA run. The shapes are linked to their problem so
the output can be graphed.

#### Usage
   `$ cpsa4shapes -h
Usage: cpsa4shapes [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

### 2.5 Formula Extraction (`cpsa4sas`)
The  `cpsa4sas`  program extracts a formula in the language
  of order-sorted first-order logic for each problem and its shapes
  from a CPSA run. The formula is called a
  shape analysis
  sentence. The formula is satisfied in all realized skeletons
  when CPSA finds all the shapes for the problem.

#### Usage
   `$ cpsa4sas -h
Usage: cpsa4sas [OPTIONS] [FILE]
  -o FILE    --output=FILE     output FILE
  -m INT     --margin=INT      set output margin (default 72)
  -a STRING  --algebra=STRING  algebra (default basic)
  -s         --show-algebras   show algebras
  -h         --help            show help message
  -v         --version         show version number` 

### 2.6 Goal Satisfaction Checking (`cpsa4goalsat`)
The  `cpsa4goalsat`  program prints the labels of
  skeletons that do not satisfy a  `defgoal` .  For each
  point of view skeleton specified by a goal, the program prints a
  list.  The first element of the list is the label of the point of
  view skeleton.  The remaining elements of the list are labels of the
  skeletons that do not satisfy the goal.

#### Usage
   `$ cpsa4goalsat -h
Usage: cpsa4goalsat [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

### 2.7 Alice and Bob Notation Translator (`cpsa4prot`)
The  `cpsa4prot`  program translates protocols expressed
  in Alice and Bob notation into CPSA's  `defprotocol` 
  syntax.  It translates  `defprot`  forms, and passes all
  else through unchanged.  The syntax of a  `defprot`  form
  is:

   `PROT       ::= (defprot NAME ALGEBRA (vars DECLS) NOTATION* RULE* PROT-ALIST)
NOTATION   ::= (msg ROLE ROLE CHMSG)
            |  (msg ROLE ROLE CHMSG CHMSG)
            |  (from ROLE CHMSG)
            |  (to ROLE CHMSG)
            |  (clone ROLE ROLE)
            |  (assume ROLE ASSUMPTION*)
CHMSG      ::= (chmsg CHAN TERM) | (chmsg TERM) | TERM
ASSUMPTION ::= (uniq-orig ...) | (non-orig ...) | ...
RULE       ::= (defrule ...)` 

The form  `(msg A B M)`  says role  `A` 
  sends  `M` , and role  `B`  receives
   `M` .  The form  `(msg A B M N)`  says
  role  `A`  sends  `M` , and role  `B` 
  receives  `N` .  The form  `(from A M)`  says
  role  `A`  sends  `M` .  The form  `(to A
  M)`  says role  `A`  receives  `M` .
  The form  `(clone A B)`  says make role  `B`  have
  the same messages as  `A`  up to this point in the
  specification.

#### Example
   `$ cat blanchet.prot
(defprot blanchet basic
  (vars (a b akey) (s skey) (d data))
  (msg init resp (enc (enc s (invk a)) b))
  (msg resp init (enc d s))
  (assume init (uniq-orig s))
  (assume resp (uniq-orig d))
  (comment "Blanchet's protocol"))
$ cpsa4prot blanchet.prot
(defprotocol blanchet basic
  (defrole init
    (vars (a b akey) (s skey) (d data))
    (trace (send (enc (enc s (invk a)) b)) (recv (enc d s)))
    (uniq-orig s))
  (defrole resp
    (vars (a b akey) (s skey) (d data))
    (trace (recv (enc (enc s (invk a)) b)) (send (enc d s)))
    (uniq-orig d))
  (comment "Blanchet's protocol"))
$` 

#### Usage
   `$ cpsa4prot -h
Usage: cpsa4prot [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -e       --expand       expand macros first
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

### 2.8 Pretty Printing and JSON Export (`cpsa4pp`)
The  `cpsa4pp`  program program pretty prints its input
using the CPSA specific algorithm.  It also translates S-Expressions
into JavaScript Object Notation (JSON)
to ease processing in other languages.

#### Usage
   `$ cpsa4pp -h
Usage: cpsa4pp [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -j       --json         output uses JSON notation
  -h       --help         show help message
  -v       --version      show version number` 

### 2.9 CPSA to LaTeX Macro Translation (`cpsa42latex`)
The  `cpsa42latex`  program translates CPSA macros
  specifying message formats into equivalent LaTeX macros. CPSA
  algebra primitives are mapped to unspecified LaTeX macros with the
  same name and arity (sometimes with an optional tag), allowing the
  user to easily customize how they would like these primitives to be
  typeset. 

#### Usage
   `$ cpsa42latex -h
Usage: cpsa42latex [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -h       --help         show help message
  -v       --version      show version number` 

### 2.10 JSON to S-Expression Translation (`cpsa4json`)
The  `cpsa4json`  program translates JSON encoded CPSA into
CPSA S-Expressions.

#### Usage
   `$ cpsa4json -h
Usage: cpsa4json [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

### 2.11 Querying CPSA Output as Derivation Trees (`cpsa4query`)
The  `cpsa4query`  program loads CPSA output and a query.
It assembles the skeletons in the output into a forest of derivation
trees.  It then runs the query against the selected trees in the
forest and returns the labels of the skeletons that satisfy the
query.

Each tree vertex is a skeleton represented as a S-Expression.
Information in the skeleton can be accessed by treating it as an
association list.  The query language allows one to ask questions
about the association list, such as if it has a given key.  For
example, you can list the shapes in a tree by asking if the
association list has the symbol "shape" as a key.

#### Usage
   `$ cpsa4query -h
Usage: cpsa4query [OPTIONS] QUERY [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

#### Description
A query is a file containing S-Expressions.  The first S-Expression
contains the query proper, and the remaining S-Expressions are integers
that select which trees in the forest will be the searched by the
query proper.  If there are no integers, the entire forest is
searched.  The syntax of the query proper is:

   `QUERY ::= (has-key SYMBOL)
       |  (null SYMBOL)
       |  (member SEXPR SYMBOL)
       |  (has-children)
       |  (has-duplicates)
       |  (not QUERY)
       |  (and QUERY*)
       |  (or QUERY*)` 

The  `has-key`  predicate asks if  `SYMBOL`  is a
key in a skeleton.  The  `null`  predicate asks
if  `SYMBOL`  is a key and the value is the empty list.  The
 `member`  predicate asks if  `SEXPR`  is a member
of the value associated with key  `SYMBOL` .
The  `has-children`  predicate asks if the current skeleton
has children.  The  `has-duplicates`  predicate asks if the
current skeleton has duplicates as descendents.  The remaining
operations implement the usual way to combine boolean functions.

#### Examples
   `(has-key shape) 0 1` 

finds the skeletons in the first and second tree that have shape as
a key.  If this query is run against the test file output
 `tst/unilateral.txt` , it will find that skeletons 1 and 3
are shapes.

   `(has-key aborted)` 

finds the skeletons in the forest that have aborted as a key.  If
this query is run against the test file output
 `tst/wide-mouth-frog.txt` , it will find that skeleton 18 is
aborted.

   `(and (not (has-children))
     (not (has-duplicates))
     (has-key unrealized))` 

finds the skeletons in the forest that are terminal and unrealized.
If this query is run against the test file output
 `tst/blanchet.txt` , it will produce

   `    2    6    8   16   20   22   30   34   36   42` 

#### Transcript
   `$ cat query.txt
(has-key shape) 0 1
$ cpsa4query query.txt tst/unilateral.txt
    1    3` 

### 2.12 Querying CPSA Output Using Prolog (`cpsa4db` and `cpsa4prolog.pl`)
The  `cpsa4db`  program is used to produce a database of
  facts about the output of CPSA in S-Expression syntax.  The facts
  provide a logical description of a run of CPSA.

The database contains facts about skeletons and facts about how
  skeletons are related to each other in the output.  There are two
  kinds of facts about each skeleton.  The body of a skeleton is
  provided as an association list with the  `skel/2` 
  predicate.  The first argument is the skeleton's label, and the
  second is the association list.  Each skeleton is also described
  using a subset of the goal language, however, the predicate symbol
  used for length predicates is  `l`  to make them easily
  distinguishable from parameter predicates.

The output of CPSA relates skeletons in two ways, by its tree
  structure and its cohort step structure.  Each non-root skeleton has one
  parent.  That information is used to form the tree used to display
  CPSA output.  The  `child/2`  predicate encodes the tree
  structure using skeleton labels.  This predicate is used to visit
  each skeleton once during a search.

A skeleton that is part of a cohort step is either a child of the
  analyzed skeleton or a seen child, meaning it is the child of a
  previously analyzed skeleton.  The  `step/3`  predicate
  specifies the cohort step relation, where its second argument is the
  operation used by CPSA to produce the cohort member from the
  analyzed skeleton.  Thus, the  `step/3`  predicate
  describes a run as a labeled transition system.

For each cohort step not produced by generalization, there is a
  homomorphism from the parent to the cohort member, and when a member
  is produced by generalization, there is a homomorphism from the
  member to the parent.  The homomorphism is available with
  the  `stwa/5`  and  `mtwa/5`  predicates.
  The  `stwa/5`  predicate specifies how strands are mapped,
  and the  `mtwa`  predicate specifies how message variables
  are mapped.  For both of these predicates, the first and forth
  arguments are skeleton labels, and the third argument is the
  operation.

The  `cpsa4dbprolog`  translates a database of facts into
  Prolog syntax so that the database can be queried using all of the
  power and flexibility of Prolog.  To be loadable by Prolog, the
  output must be sorted so that clauses of one predicate are
  colocated.  The sorting program provided in all dialects of Unix
  does the job.

The generated Prolog must be used with a dialect of Prolog in which
  strings are not be atoms, such as SWI Prolog and not GNU Prolog.
  Load the file using  `consult/1` .  Next load your query.
  The file  `cpsa4prolog.pl` 
  contains useful predicates that may help formulate your query.  The
  comments for each predicate are intended help users understand the
  output format.

Most Prolog implementations allow one to use list notation to
  easily consult several files.  If your database is
  called  `db.pl` , and your query is
  called  `query.pl` , you can load all three files with:

   `?- ['db.pl', 'cpsa4prolog.pl', 'query.pl'].` 

#### Usage
   `$ cpsa4db [OPTIONS] [FILE]
  -o FILE    --output=FILE     output FILE
  -m INT     --margin=INT      set output margin (default 72)
  -a STRING  --algebra=STRING  algebra (default basic)
  -s         --show-algebras   show algebras
  -h         --help            show help message
  -v         --version         show version number` 

   `$ cpsa4dbprolog [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

### 2.13 Using Dynamic Logic to Generate Prolog Queries (`cpsa4dl`)
The  `cpsa4dl`  program translates parts of queries
  written in the dynamic logic into Prolog.  Parts of queries that
  make use of the fact that descendents of a skeleton that are related
  to the ancestor by a homomorphism can be produced automatically by
  specifying those parts in the dynamic language and translating the
  result into Prolog.

Each step in a CPSA output contains some direct children and seen
  children.  When a direct descendent in derived using an
  authentication test, there is a homomorphism from the parent to the
  descendent, that is, all of the structure in the parent is contained
  in the descendent.  When a direct descendent is derived using
  generalization, there is a homomorphism from the descendent to the
  parent.

The dynamic logic implemented provides the usual logical operators
  for specifying properties of a skeleton.  Queries that only use
  them might as well be written directly in Prolog.

What is special about the dynamic logic is it includes the diamond
  and box operators that map formulas about descendents of a skeleton
  using homomorphisms.  For example, if the parent contains the
  message variable  `a` , and it is mapped to the
  message variable  `b`  in the descendent by the homomorphism,
  the generated code knows how to honor the mapping.

A diamond operator applied to a formula is satisfied when the
  formula is satisfied by at least one of the current formula's direct
  descendents.  A box operator applied to a formula is satisfied when
  the formula is satisfied by all of the current formula's direct
  descendents.  When the action associated with a dynamic operator
  is  `plus` , then the operator is applied to all of the
  skeleton's descendents.  The syntax of a dynamic logic query is:

   `QUERY ::= (defquery (SYMBOL DECL*) FORM+)
DECL ::= (SYMBOL SORT)
SORT ::= mesg | strd | node | othr
FORM ::= (SYMBOL TERM*)
      |  (and FORM+)
      |  (or FORM+)
      |  (exists (DECL*) FORM)
      |  (forall (DECL*) FORM)
      |  (diamond ACT FORM)
      |  (box ACT FORM)
TERM ::= SYMBOL | STRING | INTEGER | (INTEGER INTEGER)
ACT  ::= one | plus | star` 

The constant "_" is treated specially and is translated as a Prolog
  anonymous variable.

#### Usage
   `$ cpsa4dl [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

### 2.14 Restricted S-Expression Lexical Syntax
The S-expressions used are restricted so that most dialects of Lisp
can read them, and characters within symbols and strings never need
quoting. Every list is proper. An atom is either a symbol, an integer,
or a string. The characters that make up a symbol are the letters, the
digits, and the special characters in
" `+-*/<=>!?:$%_&~^` ". A symbol may not begin with
a digit or a sign followed by a digit. The characters that make up a
string are the printing characters omitting double quote and
backslash, except when double quote and backslash are escaped using
the backslash character. Double quotes delimit a string. A comment
begins with a semicolon, or is an S-expression list at top-level that
starts with the  `comment`  symbol. 

Copyright (c) 2017 The MITRE Corporation. Permission to copy without fee all
or part of this material is granted provided that the copies are not made or
distributed for direct commercial advantage, this copyright notice and the
title of the publication and its date appear, and notice in given that copying
is by permission of The MITRE Corporation.

---

## 3. The CPSA Formal Specification (`cpsaspec`)

### 3.0 Abstract
We describe a term reduction system that enumerates all essentially different
executions possible for a cryptographic protocol. We call them the shapes of
the protocol. Naturally occurring protocols have only finitely many, indeed
very few shapes. Authentication and secrecy properties are easy to determine
 from them, as are attacks and anomalies. Our Cryptographic Protocols
Shapes Analyzer (cpsa) program is a direct implementation of the reduction
system described within, and the form of the reduction system is partially
determined by the implementation.

## Spec Chapter 1: Introduction to the CPSA Reduction System

The Cryptographic Protocol Shapes Analyzer (cpsa) attempts to enumerate
all essentially different executions possible for a cryptographic protocol. We
call them the shapes of the protocol. Naturally occurring protocols have only
finitely many, indeed very few shapes. Authentication and secrecy properties
are easy to determine from them, as are attacks and anomalies.
    The shapes analysis is performed within a pure Dolev-Yao model. The
cpsa program reads a sequence of problem descriptions, and prints the steps
it used to solve each problem. For each input problem, cpsa is given some
initial behavior, and it descovers what shapes are compatible with it. Normally
, the initial behavior is from the point of view of one participant. The
analysis reveals what the other participants must have done, given the participant
’s view.
    This document specifies the cpsa program using a term reduction system.
Chapter 2 describes message algebras as order-sorted quotient term algebras.
Chapter 3 presents an implementation-oriented view of strand spaces. Chapter
 4 details the model of the adversary. The formal definition of a partial
run of a protocol is called a skeleton, and is introduced in Chapter 5.
    The term reduction systems used to specify the algorithm is presented
in Chapter 6, and the primitive reduction rules are in Chapter 7. The rules
used to transform terms called preskeletons into skeletons are in Chapter 8.
    The algorithm used to model adversarial behavior is in Chapter 9. The
algorithms used to infer what else must have happened given a partial de-scription
 of a run of a protocol as skeleton is in Chapters 10 and 11. Chapters
 13 and 12 find most general descriptions of cpsa answers—the shapes.
Finally, Chapter 14 assembles reduction rules into one system that specifies

the cpsa program.
    Appendix A describes an extension to Strand Space theory that models
passwords and related concepts. Appendix B details the sense in which a
protocol role can be viewed as an abstraction of a program. Appendix C
describes a formula in the language of order-sorted first-order logic for each
problem and its shapes found by cpsa. The formula is called a shape analysis
sentence. The formula is modeled by all skeletons that describe full runs of
a protocol when cpsa finds all the shapes for the problem.
    cpsa’s search is based on a high-level algorithm that was claimed to
be complete, i.e. every shape can in fact be found in a finite number of
steps [5, 8]. Further theoretical work [10] showed classes of executions that
are not found by the algorithm, however it also showed that every omitted
execution requires an unnatural interpretation of a protocol’s roles. Hence
the algorithm is complete relative to natural role semantics. See [13, Appendix
 B] for more on omitted executions.
    A cpsa release includes two other documents, the cpsa Design [12] and
the cpsa Primer [13]. The design document describes details of the cpsa
implementation that would clutter this one. It should be read by anyone
interesting in reading and modifying the source code. The cpsa Primer
provides an overview of cpsa, and is worth reading before this document is
approached.

### 1.1 Notation

A finite sequence is a function from an initial segment of the natural numbers.
The length of a sequence X is |X|, and sequence X = ⟨X(0), . . . , X(n − 1)⟩
for n = |X|. Alternatively, ⟨x0 , x1 , . . . , xn−1 ⟩ = x0 :: x1 :: . . . :: xn−1 :: ⟨⟩. If S
is a set, then S ∗ is the set of finite sequences of S, and S + is the non-empty
finite sequences of S. The concatenation of sequences X0 and X1 is X0 ⌢ X1 .
The prefix of sequence X of length n is X † n.
    Generally, when discussing terms, a lowercase Latin letter is used to de-note
 a term, and an uppercase Latin letter is used to denote a set of terms
or a sequence of terms.

## Spec Chapter 2: Order-Sorted Message Algebras

cpsa models a message by an equivalence class of terms over a signature. A
sort system is used to classify messages. cpsa depends on the sort system
to allow it to treat a variable that represents an asymmetric key differently
from a variable that represents an arbitrary message. In particular, cpsa uses
order-sorted quotient term algebras [6] for message algebras. This formalism
enables the use of well-known algorithms for unification and matching in the
presences of equations and sorts [2].
    This paper makes no attempt to provide a general introduction to order-sorted
 quotient term algebras. We use a message algebra called the Basic
Crypto Algebra (bca), which is the main algebra used by cpsa.
    There are six bca sorts: mesg, the sort of all messages, skey, the sort
of symmetric keys, akey, the sort of asymmetric keys, name, the sort of
participant names, and text and data for ordinary values. Sort mesg is
sometimes written as ⊤ and the other sorts are called base sorts. All base
sorts are subsorts of mesg. The function symbols, or operations, used to
form terms are given by the signature in Figure 2.1.
    Each variable x used to form a term has a unique sort s, written x : s.
Variable set X is an indexed set of sets of variables, Xs = {x | x : s}. For
bca, Xmesg , Xskey , Xakey , Xname , Xtext , and Xdata partition the set of
variables in X. By abuse of notation, at times, we write X for the set of
variables in X.
    The Basic Crypto Quotient Term Algebra A generated by variable set X
is displayed in Figure 2.2. The union of the messages in A is set of terms
generated by X, and A partitions the set of terms into a set of equivalence
classes induced by the equations. Terms t0 and t1 are equivalent, written

t0 ≡ t1 , iff t0 ∈ T ∧ t1 ∈ T for some T ∈ A. The canonical representative
of a message is the t in {t′ | t′ ≡ t} with the fewest occurrences of the (·)−1
operation.

**Figure 2.1: Basic Crypto Signature and Equation**

```text
    Sorts: name, text, data, skey, akey < mesg
      Base sorts: name, text, data, skey, akey
     Carried positions: • denotes a carried position.
{| • |}(·) : mesg × mesg → mesg      Encryption
#(·) : mesg → mesg                   Hashing
(•, •) : mesg × mesg → mesg          Pairing
“. . . ” : mesg                      Tag constants
K(·) : name → akey                   Public key of name
(·)−1 : akey → akey                  Inverse of key
ltk(·, ·) : name × name → skey       Long term key
           Equation: (x−1 )−1 ≈ x for x : akey
```

**Figure 2.2: bca Messages A and Atoms B**

```text
    Askey = {{x} | x ∈ Xskey } ∪ {{ltk(a, b)} | a ∈ Xname , b ∈ Xname }
    Aakey = {{x−2n | n ∈ N} | x ∈ Xakey }
               ∪ {{x−2n−1 | n ∈ N} | x ∈ Xakey }
               ∪ {{Kx−2n | n ∈ N} | x ∈ Xname }
               ∪ {{Kx−2n−1 | n ∈ N} | x ∈ Xname }
    Aname = {{x} | x ∈ Xname }
     Atext = {{x} | x ∈ Xtext }
    Adata = {{x} | x ∈ Xdata }
        B = Askey ∪ Aakey ∪ Aname ∪ Atext ∪ Adata
       A0 = B ∪ {{x} | x ∈ Xmesg } ∪ {{x} | x is a tag constant }
      n+1
     A     = An ∪ {{(t0 , t1 ) | t0 ∈ T0 , t1 ∈ T1 } | T0 ∈ An , T1 ∈ An }
                ∪ {{{|t0 |}t1 | t0 ∈ T0 , t1 ∈ T1 } | T0 ∈ An , T1 ∈ An }
             S ∪ {{#t     | t ∈ T } | T ∈ An }
A = Amesg = n∈N An
```

    Keys, names, data, and texts in the algebra are called atoms and are
members of B. We write t : B iff {t′ | t′ ≡ t} ∈ B. Note that encryption
is defined with an encryption key of sort mesg. When the encryption key
is of sort akey this is meant to model asymmetric encryption: otherwise,
this models symmetric encryption. Note that even complex messages such
as encryptions can be used as encryption keys in the symmetric sense.
    To find the decryption key associated with an encryption, one must exclude
 the case in which the key is a variable of sort mesg, as there is no way
to determine if the encryption operation denotes symmetric or asymmetric
encryption. Therefore, the decryption key associated with encryption key t
is inv (t).
                       
                        invk(t)     if t : akey;
             inv (t) =   undefined if t is a variable of sort mesg;
                         t           otherwise.
                       

    An important property possessed by the algebra is that for all T ∈ A, if
there are any encryptions in T then all members of T are encryptions. As
a result, a message can be identified as representing an encryption and if it
is, decomposed into its plaintext and its decryption key. This property is a
consequence of the fact that equations relate atoms, not arbitrary messages.
A similar property holds for pairs and hashes. A hash is treated as a kind of
encryption in which the term that is hashed is the encryption key.
    We write AX when it is important to identify the variable set X that
generates the algebra. Given two variable sets X and Y , a substitution is
an order-sorted map σ : X → AY such that σ(x) ̸= x for only finitely many
elements of X. For a substitution σ, the domain is the set of variables
Dom(σ) = {x | σ(x) ̸= x} and the range is the set Ran(σ) = {σ(x) |
x ∈ Dom(σ)}. Substitution σ0 is more general than σ1 , written σ0 ⊴ σ1 ,
if there exists a substitution σ2 such that ∀x σ1 (x) ≡ σ2 (σ0 (x)). Given a
substitution σ : X → AY , the unique homomorphism σ ∗ : AX → AY induced
by σ is also denoted σ.
    A position p is a finite sequence of natural numbers. The term in t that

occurs at p, written t @ p, is:

                       t @ ⟨⟩ = t;
                       (t0 , t1 ) @ i :: p = ti @ p for i ∈ {0, 1};
                       {|t0 |}t1 @ i :: p = ti @ p for i ∈ {0, 1};
                       t−1 @ 0 :: p = t @ p.

A term t occurs in term t′ if t = t′ @ p for some p. A message T occurs
in message T ′ if the canonical representative of T occurs in the canonical
representative of T ′ .
   A carried term is one that can be extracted from a message reception
assuming plaintext is extractable from encryptions. The positions at which
term t is carried in t′ is carpos(t, t′ ), where

                                {⟨⟩} if t′ ≡ t, else
                             
                             
                             
                                {0 :: p | p ∈ carpos(t, t1 )}
                             
                             
                             
                             
                                        if t′ = {|t0 |}t1 , else
                             
            carpos(t, t′ ) =
                             
                               {i :: p | i ∈ {0, 1}, p ∈ carpos(t, ti )}
                                        if t′ = (t0 , t1 ) else
                             
                             
                             
                             
                                ∅       otherwise.
                             

     Term t carries t′ if carpos(t′ , t) is not empty, and t′ ⊑ t when t′ is carried
 by t. Note that for all terms t0 , t1 , t′0 , t′1 , if t0 ≡ t1 and t′0 ≡ t′1 , then
carpos(t0 , t′0 ) = carpos(t1 , t′1 ). We write t′ ⊑p t when p ∈ carpos(t′ , t) and
t @ p ≡ t′ .
     In what follows, we will often conflate a term with the message of which
it is a member, and use lowercase letters to denote both.

### 2.1 Channel Messages

As of cpsa version 4.2, messages can optionally be transported on a channel.
For t ∈ AX , a plain message is written [t], and when the message is bound
to channel c, it is written [c, t].
    The channel message algebra adds two sorts to the underlying message
algebra, chan and chmsg, and two operations to the signature:

                  [·] : mesg → chmsg        Plain message
               [·, ·] : chan × mesg → chmsg Channel message

Let X be a bca variable set, and X̄ be a variable set that adds channel
variables to X. If AX is the algebra associated with sort mesg, then ĀX̄ is
the algebra associated with sort chmsg, the Basic Crypto Channel Algebra
generated from X̄.
   Positions are extended to channel messages as follows:

                              m @ ⟨⟩ = m;
                              [t] @ 0 :: p = t @ p;
                              [c, t] @ 1 :: p = t @ p.

The set of carried positions is extended to channel messages in the obvious
way. The plain message [t] will often be written as t when the context
disambiguates the reference.

### 2.2 Locations and state messages

The cpsa 4 treatment of state makes two additions to the message algebra.
First, we introduce a new sort of channel, called locations and written locn.
These are handled exactly like chans in building channel messages:

            [·] : mesg → chmsg                 Plain message
         [·, ·] : (chan ∪ locn) × mesg → chmsg Channel message

We also add a new sort to the underlying message sorts, the sort of points
pval, which are a base sort.
            Sorts: pval, name, text, data, skey, akey < mesg
              Base sorts: pval, name, text, data, skey, akey
We leave the operators and equations unchanged. cpsa protocol specifications
 never mention point values explicitly, but the cpsa loader incorporates
them whenever it reads roles that load state values from locations or store
them into locations.
    The state value is a pair (pt, t) consisting of a point pt : pval and the user-specified
 message term t; the point occurring when a state value is stored into
a location is always assumed to be uniquely originating. This ensures that
loads that receive the same value (including the point component) are in fact
observing the same state transition event. This allows cpsa to reconstruct
the state histories of different state registers.

    Thus, when m is a message, it may be a plain message [t] or a channel
message [c, t], where either c : chan or c : locn. In case c : locn, cpsa
always arranges that t is a pair of the form t = (pt, t0 ) where pt : pval and
t0 is a point-free term.

## Spec Chapter 3: Strand Spaces and Bundles

When using strand space theory, one normally hypothesizes the existence of
a single global strand space. This is a very reasonable assumption for theoretical
 analysis, but from the point view of an implementer, it turns out
that it is better to assume there are many local strand spaces and the de-sign
 specification task is to describe the relations between these local spaces.
Our reformulation of strand space notation provides an implementation oriented
 way of describing the concept of a local strand space, and a direct
link between from algorithm specification to the data structures used in the
implementation.
    A run of a protocol is viewed as an exchange of messages by a finite set
of local sessions of the protocol. Each local session is called a strand. The
behavior of a strand, its trace, is a sequence of messaging events. An event
is either a message transmission or a reception.
    An outbound message m ∈ ĀX is written as +m, and a message m is
written as −m.

State events: Stores and loads. When m = [c, (pt, t0 )] for c : locn and
pt : pval, +m is a store event, in which the value t0 is written into the
location c, and −m is a load event, in which the value t0 is read out of the
location c. In the latter case, pt may be the point associated with an earlier
store event e that wrote t0 into c. In this case, our theory will ensure that e
is the most recent store event involving c.

Traces and strand spaces. The set of traces over ĀX is CX = (±ĀX )+ .
A message originates in a trace if it is carried by some event and the first

event in which it is carried is outbound. A message is gained by a trace if it
is carried by some event and the first event in which it is carried is inbound.
A message is acquired by a trace if it first occurs in a reception event and is
also carried by that event.
    Abstractly, a strand space is a multiset of traces, but since we wish to
name each element, a strand space ΘX over algebra ĀX is defined to be a
sequence of traces in CX . A strand s is a member of the domain of ΘX , and
its trace is ΘX (s).
    Message events occur at nodes in a strand space. For each strand s, there
is a node for every event in Θ(s). The nodes of strand space Θ are {(s, i) |
s ∈ Dom(Θ), 0 ≤ i < |Θ(s)|}, the event at a node is evt Θ (s, i) = Θ(s)(i),
and the message at a node is msg Θ (s, i) = m such that evt Θ (s, i) = ±m.
Just as a position names a subterm within another term, a strand names a
trace within a strand space, and a node names an event in a strand space.
The relation ⇒ defined by {(s, i − 1) ⇒ (s, i) | s ∈ Dom(Θ), 1 ≤ i < |Θ(s)|}
is called the strand succession relation.
    A bundle in strand space Θ is a finite directed acyclic graph Υ(Θ, →),
where the vertices are the nodes of Θ, and an edge represents communication
 (→) or strand succession (⇒). For communication, if n0 → n1 , then
there is a channel message m such that evt Θ (n0 ) = +m and evt Θ (n1 ) = −m.
For each reception node n1 , there is a unique transmission node n0 with
n0 → n1 .
    Each acyclic graph has a transitive irreflexive relation ≺ on its vertices.
The relation specifies the causal ordering of nodes in a bundle. An transitive
irreflexive binary relation is also called a strict partial order.

Authentic and confidential channels. An atom uniquely originates in
a bundle if it originates in the trace of exactly one strand. An atom is non-originating
 in a bundle if it originates on no strand, but each of its variables
occurs in some strand’s trace. A channel is authenticated if only regular
strands in a bundle use it to transmit messages. A channel is confidential if
only regular strands in a bundle use it to receive messages.

Channel properties of locations. Every location is regarded as a confidential
 channel. Thus, we are modeling long term state registers that are
associated with devices under the control of regular (i.e. compliant) participants
. The adversary never observes a location directly; the adversary

observes only messages from regular participants that may reflect the contents
 of locations. The adversary may store certain values directly, namely
the possible initial values for a location. Thus, we rely on the adversary
to initialize locations values. Other values that can be produced only by a
state transition cannot be inserted by the adversary; only a regular participant
’s store event can cause them. The protocol specification determines
the sufficient conditions for these non-initial values, or, as we will call them,
generated state values. Naturally, messages the adversary delivers to regular
participants may affect what generated state values they subsequently store.

Roles. In a run of a protocol, the behavior of each strand is constrained by
a role in a protocol. Adversarial strands are constrained by roles as are non-adversarial
 strands. What follows is the definition of a role before channels
and channel messages were introduced into cpsa, followed by a discussion of
the additions caused by channels.
    Given an ĀY , and C ∈ CY , N ⊆ BY , and U ⊆ BY , if:
  1. t ∈ N implies t is not carried in C, and all variables in N occur in C;
  2. t ∈ U implies t originates in C;
  3. if variable x occurs in C then x is an atom or it is acquired in C; and
  4. the trace of a role may not match the pattern ⟨−m, +m, . . .⟩,
then rY (C, N, U ) is a role over ĀY . The trace of rY (C, N, U ) is C, its non-origination
 assumptions are N , and its unique origination assumptions are U .
Item (4) is meant to ensure that listeners, which are introduced on Page 17,
cannot be confused with protocol constrained strands.
     A protocol P is a set of roles. Let Vars(P ) be the set of variables that
occur in the traces of the roles in protocol P .
     A bundle Υ(ΘX , →) is a run of protocol P if there is a role mapping
rl : ΘX → P that satisfies properties for each s ∈ Dom(ΘX ). Assuming
rl (s) = rY (C, N, U ) and X and Y share no variables, and let h = |ΘX (s)|, the
properties are (1) h ≤ |C|, (2) there is a homomorphism σ : ĀY → ĀX such
that σ ◦ C † h = ΘX (s), (3) Dom(σ) is the set of variables that occur in C † h,
(4) if the variables in t ∈ N occur in Dom(σ), then σ(t) is non-originating in
Υ(ΘX , →), and (5) if t ∈ U originates at index i in C, and i < h, then σ(t)
uniquely originates in Υ(ΘX , →) at node (s, i). Origination assumptions in
bundles specified by roles are called inherited origination assumptions.

Roles and channels. The introduction of channels adds two new fields to
a role, a set of channels assumed to be authenticated, and a set of channels
assumed to be confidential. For a bundle to be a run of a protocol, the
inherited channel assumptions must be honored by the bundle. State adds
no other fields to the role data structure, although when c : locn, c will
always be among the confidential channels.

## Spec Chapter 4: Adversary Model

A fixed set of penetrator roles encodes the adversary model associated with
a message algebra. For the Basic Crypto Algebra, there are nine roles. Each
role makes no origination assumptions, and the trace of each role is given
in Figure 4.1. The first line of the figure specifies many traces, one for each
base sort, and a trace for each tag.
    A strand exhibits non-adversarial behavior when its role is not a penetrator
 role. A non-adversarial strand is called a regular strand as is its
role.
    The penetrator cannot use a non-originating atom to encrypt or decrypt a
message, because every key it uses must be carried in a message. Consider a
uniquely originating atom that originates on a regular strand. The penetrator
cannot make the atom using a create role, because the atom would originate
in more than one trace. Therefore, the penetrator can use a uniquely originating
 atom to encrypt or decrypt a message only if it is transmitted by a
regular strand unprotected by encryption.
    When a channel is authenticated, the penetrator cannot send a message

on it. When a channel is confidential, the penetrator cannot receive a message
on it.

**Figure 4.1: Basic Crypto Algebra Penetrator Role Traces**

```text
Create(z : B)         ⟨+z⟩                 ⟨+“. . . ”⟩
Pair(x, y : ⊤)        ⟨−x, −y, +(x, y)⟩    ⟨−(x, y), +x, +y⟩
Encrypt(x, y : ⊤)     ⟨−x, −y, +{|x|}y ⟩   ⟨−{|x|}y , − inv (y), +x⟩
Hash(x : ⊤)           ⟨−x, +#x⟩
Chan(c : Ch, x : ⊤)   ⟨−x, +[c, x]⟩        ⟨−[c, x], +x⟩
```

## Spec Chapter 5: Preskeletons, Skeletons, and Homomorphisms

The details of penetrator behavior are abstracted away when performing
protocol analysis. The abstracted description of a bundle is called a realized
skeleton, which is defined using a protoskeleton. A protoskeleton over ĀX is
kX (rl , P, ΘX , ≺, N, U ), where rl : Dom(ΘX ) → P is a role map, the sets X
and Vars(P ) are disjoint, ΘX is a sequence of traces in CX , ≺ is a relation on
the nodes in ΘX , N ⊆ BX are its non-origination assumptions, and U ⊆ BX
are its unique origination assumptions. Unlike a strand space, the sort of a
variable in X need not be a base sort.
    The introduction of channels adds two new fields to a skeleton, a set of
channels assumed to be authenticated, and a set of channels assumed to be
confidential. The implications of the additions is straightforward, and we
simply retain the original description of skeletons.
    Assume the strands in bundle Υ(ΘX , →) have been permuted so that
regular strands precede penetrator strands in sequence ΘX , and rl demonstrates
 the bundle is a run of protocol P . Let P ′ be P without penetrator
roles. Skeleton kX (rl ′ , P ′ , Θ′X , ≺, N, U ) realizes the bundle if rl ′ and Θ′X are
the truncations of rl and ΘX respectively that omit penetrator strands from
their domains, ≺ is the transitive irreflexive relation associated with the
bundle without penetrator nodes, N is the set of non-originating atoms with
variables that occur in Θ′X , and U is the set of atoms that uniquely originate
and are carried by some regular event.
    A protoskeleton kX (rl , P, ΘX , ≺, N, U ) is a preskeleton if the following
properties hold.
   1. Sequence rl demonstrates that the strands in Dom(ΘX ) satisfy the
      conditions for being a part of a run of protocol P .

   2. Relation ≺ is transitive, irreflexive, and includes the strand succession
      relation (⇒).

   3. If n ≺ n′ , then either n ⇒ n′ , evt ΘX (n) = +t and evt ΘX (n′ ) = −t′ , or
      n ≺ n′′ ≺ n′ for some n′′ .

   4. Each atom in N is carried by no event, and each variable in the atom
      occurs in some event.

   5. Each atom in U is carried by some event.

   6. N includes the non-originating atoms inherited from roles via the role
      map.

   7. U includes the uniquely originating atoms inherited from roles via the
      role map.

    Let Ok (t) be the set of nodes at which t originates in preskeleton k,
and Gk (t) be the set of nodes at which t is gained in k. Preskeleton
kX (rl , P, ΘX , ≺, N, U ) is a skeleton if each atom in U originates on at most
one strand, and the node of origination precedes each node that gains the
atom, i.e. for every t ∈ U , n0 ∈ Ok (t) and n1 ∈ Gk (t) implies n0 ≺ n1 .
    Let k0 = kX (rl0 , P, Θ0 , ≺0 , N0 , U0 ) and k1 = kY (rl1 , P, Θ1 , ≺1 , N1 , U1 ) be
preskeletons. There is a preskeleton homomorphism from k0 to k1 if ϕ and σ
are maps with the following properties:

   1. ϕ maps strands of k0 into those of k1 , and nodes as ϕ((s, i)) = (ϕ(s), i),
      that is ϕ is in Dom(Θ0 ) → Dom(Θ1 );

   2. σ : ĀX → ĀY is a message algebra homomorphism;

   3. n ∈ nodes(Θ0 ) implies σ(evt Θ0 (n)) = evt Θ1 (ϕ(n));

   4. n0 ≺0 n1 implies ϕ(n0 ) ≺1 ϕ(n1 );

   5. σ(N0 ) ⊆ N1 ;

   6. σ(U0 ) ⊆ U1 ;

   7. t ∈ U0 implies ϕ(Ok0 (t)) ⊆ Ok1 (σ(t)).

    A homomorphism is strandwise injective if its strand map is injective.
Two preskeletons are isomorphic if they are related by strandwise injective
homomorphism in both directions. A homomorphism is nodewise isomorphic
if the strand map ϕ implies a bijection on nodes, and n0 ≺1 n1 implies
ϕ−1 (n0 ) ≺0 ϕ−1 (n1 ). A skeleton is realized if there is a nodewise isomorphic
homomorphism from it to a skeleton that realizes a bundle, and message
component of the homomorphism is injective.
    Our formalism requires that every protocol include a listener role of the
form: lsn(x : ⊤) = r(⟨−x, +x⟩, ∅, ∅). Instances of this role are sometimes used
to make penetrator derived messages visible in skeletons. We say skeleton k
realizes modulo listeners bundle Υ(Θ, →) if k realizes Υ(Θ′ , →′ ) and Υ(Θ, →)
is the result of removing listener strands, and adjusting the communication
ordering → appropriately.
    The set of bundles denoted by preskeleton k, [[k]], is:
                          ϕ,σ
           [[k]] = {Υ | k 7−→ k ′ and k ′ realizes modulo listeners Υ}
A cpsa algorithm is complete if when given a preskeleton k, either the algorithm
 diverges, or else it terminates       and produces a finite set of realized
skeletons K, such that [[k]] = k′ ∈K [[k ′ ]].
                              S

### 5.1 Blanchet’s Simple Example Protocol
The following protocol is a simplified version of the Denning-Sacco key distribution
 protocol [4] due to Bruno Blanchet.
                                A → B : {|{|s|}a−1 |}b
                                B → A : {|d|}s
Symmetric key s is freshly generated, asymmetric keys a−1 and b−1 are uncompromised
, and the goal of the protocol is to keep data d secret. The
protocol was constructed with a known flaw for expository purposes.
    This cpsa description of the protocol has an initiator and a responder
role.
           init(a, b : A, s : S, d : D) = r(⟨+{|{|s|}a−1 |}b , −{|d|}s ⟩, ∅, ∅)
          resp(a, b : A, s : S, d : D) = r(⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩, ∅, ∅)
where we use A for sort akey, S for sort skey, and D for sort data to
save space. The algebra for the initiator role is generated from X, where
XA = {a, b}, XS = {s}, XD = {d}, Xtext = ∅, Xname = ∅, and X⊤ = ∅.

    An interesting point of view for analysis is to see if the authentication
goals of the initiator are met. To do so, we assume there was full length run
of an initiator strand, and let cpsa determine what else must have happened.
Let variable set Y = a, b : A, s : S, d : D. The point-of-view skeleton is:
       kY (⟨init(a0 , b0 , s0 , d0 )⟩,                             Role map
           {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )},   Protocol
           ⟨⟨+{|{|s|}a−1 |}b , −{|d|}s ⟩⟩,                         Traces
           ∅,                                                      Node orderings
           {a−1 , b−1 },                                           Non-origination
           {s})                                                    Unique origination
where the variable set that generates the algebra for the initiator and responder
 roles have been renamed so as to avoid conflicts with the variable set Y
used by the skeleton.
    The skeleton produced by cpsa for this problem follows. Notice that the
two strands agree on the key b used in the outermost encryption of their
first message, and indication that the authentication goals of the initiator
are met. See Figure 5.1 to see the structure of the shape.
       kY (⟨init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )⟩,   Role map
           {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )},   Protocol
           ⟨⟨+{|{|s|}a−1 |}b , −{|d|}s ⟩,                          Traces
            ⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩⟩,
           {(0, 0) ≺ (1, 0), (1, 1) ≺ (0, 1)},                     Node orderings
           {a−1 , b−1 },                                           Non-origination
           {s})                                                    Unique origination
The homomorphism from the point-of-view skeleton to the shape is
                         (⟨1⟩, {a 7→ a, b 7→ b, s 7→ s, d 7→ d}).
    An analysis of the authentication goals for the responder shows the flaw
built into the protocol. To do the analysis, assume there was a full length run
of a responder strand, and let cpsa determine what else must have happened.
In this case, the point-of-view skeleton is:
       kY (⟨resp(a0 , b0 , s0 , d0 )⟩,                             Role map
           {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )},   Protocol
           ⟨⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩⟩,                         Traces
           ∅,                                                      Node orderings
           {a−1 , b−1 },                                           Non-origination
           {s})                                                    Unique origination

                            init        resp          resp         init

                             •            /•            •o             •

                                                       
                             •o           •             •
**Figure 5.1: Shapes for Blanchet’s Protocol**

    The shape generated by cpsa follows. An early indication of a problem
is the variable set for the shape has three asymmetric keys. Let variable set
Z = a, b, b′ : A, s : S, d : D. The shape is:

      kZ (⟨resp(a0 , b0 , s0 , d0 ), init(a1 , b1 , s1 , d1 )⟩,   Role map
          {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )},   Protocol
          ⟨⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩,                          Traces
           ⟨+{|{|s|}a−1 |}b′ ⟩⟩,                                  Note key is b′ not b!
          {(1, 0) ≺ (0, 0)},                                      Node orderings
          {a−1 , b−1 },                                           Non-origination
          {s})                                                    Unique origination

   Notice that the two strands do not agree on the key used in the outermost
encryption of their first message—an authentication failure. To see that the
authentication failure leads to the failure to protect the secrecy of data d,
the protocol is analyzed using the following point-of-view:

   kY (⟨resp(a0 , b0 , s0 , d0 ), lsn(x)⟩,                                 Role map
       {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 ), lsn(x)},       Protocol
       ⟨⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩, ⟨−d, +d⟩⟩,                           Traces
       {(0, 1) ≺ (1, 0)},                                                  Node orderings
       {a−1 , b−1 },                                                       Non-origination
       {s, d})                                                             Unique origination

   cpsa finds a shape that shows how data d is revealed to the adversary.

### 5.2 Dolev-Yao Example 1.3
The intended run of the protocol in the Dolev-Yao Example 1.3 is:
                                  A → B : {|{|m|}b , a|}b
                                  B → A : {|{|m|}a , b|}a

assuming text m is freshly generated, and asymmetric keys a−1 and b−1 are
uncompromised.
    The cpsa description of the protocol also has an initiator and a responder
role.
          init(a, b : A, m : D) = r(⟨+{|{|m|}b , a|}b , −{|{|m|}a , b|}a ⟩, ∅, ∅)
         resp(a, b : A, m : ⊤) = r(⟨−{|{|m|}b , a|}b , +{|{|m|}a , b|}a ⟩, ∅, ∅)

    An interesting point of view for analysis is to see if m is kept secret after
the initiator sends its message. Let variable set Z = a, b : A, m : D. The
initial scenario preskeleton is:
      kZ (⟨init(a0 , b0 , m0 ), lsn(x)⟩,                            Role map
          {init(a0 , b0 , m0 ), resp(a1 , b1 , m1 ), lsn(x)},       Protocol
          ⟨⟨+{|{|m|}b , a|}b ⟩, ⟨−m⟩⟩,                              Traces
          ∅,                                                        Node orderings
          {a−1 , b−1 },                                             Non-origination
          {m})                                                      Unique origination

where the variable set that generates the algebra for the initiator role has
been renamed so as to avoid conflicts with the variable set Z used by the
preskeleton.
   cpsa determines m is not kept secret by producing the shape in Figure
 5.2. The added strands in the shape are instances of responder roles.
The strands in the shape are:
                  ⟨+{|{|m|}b , a|}b ⟩
                  ⟨−m⟩
                  ⟨−{|{|m|}b , a′ |}b , +{|{|m|}a′ , b|}a′ ⟩
                  ⟨−{|{|{|m|}b , a|}b , a′′ |}b , +{|{|{|m|}b , a|}a′′ , b|}a′′ ⟩

The non-origination and unique origination assumptions are as they are in
the initial scenario preskeleton. An interesting exercise left for the reader is
to produce a bundle that is realized by the shape.

                        init               resp        resp

                          •                             /•

                                                         
                                              •o         •

                                              
                                   •o         •

                                    
                                   •
**Figure 5.2: Dolev-Yao Example 1.3 Shape**

### 5.3 Exercise

Consider the following roles.

                     init(a, b : A) = r(⟨+(a, b), −(b, a)⟩, ∅, ∅)
                    resp(a, b : A) = r(⟨−(a, b), +(b, a)⟩, ∅, ∅)

Let X = x, y : A and k = kX (⟨init(a, b), resp(a, b), resp(a, b)⟩,
                             {init(a, b), resp(a, b)},
                             ⟨⟨+(x, y), −(y, x)⟩,
                              ⟨−(x, y), +(y, x)⟩,
                              ⟨−(x, y), +(y, x)⟩⟩,
                             Node ordering in Figure 5.3,
                             ∅,
                             ∅)
   What is [[k]]?
   One member is shown in Figure 5.4.

                init       resp      resp

                  •        /•         ,•

                                      
                  • lo      •          •
**Figure 5.3: Exercise Skeleton**

       init   ⟨+(x, y), −(y, x)⟩
       resp   ⟨−(x, y), +(y, x)⟩
       resp   ⟨−(x, y), +(y, x)⟩
       pair   ⟨−(y, x), −(y, x), +((y, x), (y, x))⟩
       sep    ⟨−((y, x), (y, x)), +(y, x)⟩

      init      resp       resp       pair      sep

       •         /•         ,•

                               
                  •         •          /•

                                       - •

                                            
                                        •        /•

                                                 
       •o                                         •
**Figure 5.4: A Bundle Realized by the Example Skeleton**

### 5.4 External Syntax and Instances

The external syntax used by cpsa is a little different than what has been
described here. In the external syntax, the trace and the role associated
with a strand is specified by an instance. An instance is of the form i(r, h, σ),

where r is a role, h specifies the length of a trace instantiated from the role,
and σ specifies how to instantiate the variables in the role to obtain the trace.
Thus when r = rY (C, N, U ), the trace associated with i(r, h, σ) is σ ◦ C † h.
An instance is well-formed if 1 ≤ h ≤ |C|, and Dom(σ) is the set of variables
that occur in C † h.
     In the external syntax, the role map and sequence of traces are replaced
by a sequence of instances. So for preskeleton kX (rl , P, ΘX , ≺, N, U ), the
external syntax is kX (P, I, ≺, N, U ), where for each s ∈ Dom(Θx ), I(s) =
i(r, h, σ), r = rl (s), and the trace of i(r, h, σ) is ΘX (s).

## Spec Chapter 6: Algorithms as Reduction Systems

Systems

Algorithms in this paper are specified as abstract reduction systems [1, Chapter
 2]. A reduction system is a pair (A, →), where reduction → is a binary
relation → ⊆ A × A. Element x ∈ A is a normal form if there is no y such
that x → y. The transitive closure of → is →+ . The reflexive transitive
closure of → is →∗ . A reduction is confluent if x →∗ y0 and x →∗ y1 implies
there is a z such that y0 →∗ z and y1 →∗ z. A reduction is terminating
if there are no infinite descending chains. A reduction is convergent if it is
confluent and terminating.
    Let K be the set of preskeletons. Algorithms are specified as reduction
systems of the form (K, →), which are then used to specify a related setwise
reduction system of the form (2K , ↠). Setwise reduction systems are the
ones with the interesting normal forms and confluence properties. In a setwise
reduction system, reduction rewrites one element of a set to a set of elements.

**Definition 6.1 (Setwise Reduction System).** The setwise reduction system
of binary relation ⇝⊆ K × 2K is a reduction system (2K , ↠), where for each
K0 ∈ 2K , K0 ↠ K1 if for some k0 ∈ K0 , k0 ⇝ K2 , K1 = K2 ∪ (K0 \ {k0 }),
and K1 ̸= K0 .

   The cpsa algorithm will be specified as a setwise term reduction system,
where the initial problem is given a singleton in 2K , and the answers computed
by an implementation of the algorithm are a normal form of the setwise
reduction relation ↠k defined in Chapter 14.

    In what follows the relation k ⇝ K is defined in terms of →⊆ K × K by
specifying {k} ↠ K using →, so the ⇝ relation is not explicitly defined.
    We regard sets of preskeletons as factored by isomorphism, where each
set has at most one representative of the equivalence class of isomorphic
preskeletons. The definition of isomorphic preskeletons is given on Page 17.
    The cpsa Design [12] describes an extension of a message algebra signature
 that models the data structures used in the cpsa program. The terms
over the extended signature include ones that model preskeletons. Sets of
terms of sort preskeleton are the domain of our setwise reduction systems.

## Spec Chapter 7: Primitive Preskeleton Operators

Operators

The are four primitive operators on preskeletons used by cpsa to solve
authentication tests. Each operator is a partial map from preskeletons to
preskeletons.

**Definition 7.1 (Substitution Operator).** For order-sorted substitution σ : X →
AY , the operator Sσ is:

                Sσ (kX (rl , P, ΘX , ≺, N, U )) =
                  kY (rl , P, s 7→ σ ◦ ΘX (s), ≺, σ(N ), σ(U ))

   For k ′ = Sσ (k), there is a homomorphism from k to k ′ only if for all
t ∈ Uk , Ok (t) ⊆ Ok′ (σ(t)). The structure preserving maps associated with
the homomorphism are ϕid and σ.

**Definition 7.2 (Compression Operator).** For distinct strands s and s′ , operator
 Cs,s′ compresses strand s into s′ .

                    Cs,s′ (kX (rl , P, ΘX , ≺, N, U )) =
                      kX (rl ◦ ϕ′s , P, ΘX ◦ ϕ′s , ≺′ , N, U )

where                              
                                       j + 1 if j ≥ s
                       ϕ′s (j) =
                                       j     otherwise,

relation ≺′ is the transitive closure of ϕs,s′ (≺), and

                                      ϕs (s′ ) if j = s
                                    
                        ϕs,s′ (j) =
                                     ϕs (j) otherwise
                                      j − 1 if j > s
                          ϕs (j) =
                                      j        otherwise.

    The compression operator is only used when ΘX (s) is a prefix of ΘX (s′ ),
and when there is a homomorphism from k to Cs,s′ (k). The structure pre-serving
 maps associated with the homomorphism are ϕs,s′ and σid . Note that
the compression operator is defined only when relation ≺′ is asymmetric, and
that ϕs,s′ ◦ ϕ′s = ϕid .

**Definition 7.3 (Ordering Enrichment Operator).** Operator O applied to k
enriches ≺k by adding all elements implied by unique origination. That
is O(k) = kX (rl , P, ΘX , ≺′ , N, U )), where k = kX (rl , P, ΘX , ≺, N, U ) and
≺′ = (≺ ∪{(n0 , n1 ) | n0 ∈ O(k, t) ∧ n1 ∈ G(k, t)})∗ .

   The ordering enrichment operator is total and idempotent. The structure
 preserving maps associated with the operator’s homomorphism are ϕid
and σid , i.e. the homomorphism is an embedding.

**Definition 7.4 (Augmentation Operator).** For node n, role r, and trace C,
operator An,r,C is:

                     An,r,C (kX (rl , P, ΘX , ≺, N, U )) =
                       kX ′ (rl ⌢ r, P, ΘX (s) ⌢ C, ≺′ , N ′ , U ′ )

where X ′ is X extended to include the variables in C, ≺′ is the minimal
extension of ≺ such that (|ΘX | + 1, |C|) ≺′ n, N ′ is N extended with non-origination
 assumptions inherited from r by C, and likewise for U ′ .

    The structure preserving maps associated with the augmentation operator
’s homomorphism are ϕid and σid , i.e. the homomorphism is an embedding.

## Spec Chapter 8: Reductions on Preskeletons (Thinning, Hulling, Compression)

This chapter describes the algorithm used to transform a preskeleton into a
skeleton as a setwise term reduction system (K, ↠). Recall that the relation
k ⇝ K in Chapter 6 is defined in terms of →⊆ K × K by specifying {k} ↠ K
using →. Additionally, when k = k(rl , P, Θ, ≺, N, U ), Uk is used to name U ,
and so forth for other components of k.
    If a preskeleton k is not a skeleton, then it is either because some t ∈ Uk
actually originates at more than one node, or because for some t ∈ Uk ,
there is a node n1 ∈ Gk (t), and a node n0 ∈ Ok (t) such that n0 ⊀k n1 . A
preskeleton in which an atom assumed to be uniquely originating originates
more than once is simply expunged. The second obstruction is resolved by
enriching node orderings. A hulled preskeleton is a preskeleton in which every
uniquely originating atom originates at most once, but it may lack some node
orderings needed to be a skeleton.
    Skeletons may contain “effectively equivalent” strands. After converting
preskeletons to skeletons, a preskeleton reduction system may remove effectively
 equivalent strands using a process called thinning. A skeleton without
any effectively equivalent strands is called a thinned skeleton.

**Definition 8.1 (Hulling Reduction).** A non-hulled preskeleton k is expunged.
                                           H
The setwise hulling reduction rule is {k} −↠ {} when k is not hulled.

**Definition 8.2 (Order Enrichment).** Suppose hulled preskeleton k0 is not a
skeleton. Hulled preskeleton k0 reduces to skeleton k1 by order enrichment,
             O
written k0 −→ k1 , iff k1 is the result of adding node orderings implied by
origination. That is, ≺k1 = (≺k0 ∪ {(n0 , n1 ) | n0 ∈ O(k0 , t) ∧ n1 ∈ G(k0 , t)})∗ .

There is a homomorphism from k0 to k1 that is an embedding. For the
                                           O           O
setwise order enrichment reduction, {k0 } −↠ {k1 | k0 −→ k1 } when k0 is a
hulled preskeleton that is not a skeleton.
   The thinning operator Ts removes an effectively equivalent strand.
**Definition 8.3 (Thinning).** Two strands s and s′ in a skeleton k are effectively
 equivalent if k with s removed and k with s′ removed are isomorphic.
(Page 17 defines isomorphic skeletons.) Skeleton k0 reduces to skeleton k1
                           Ts
by thinning, written k0 −→     k1 , if and only if there exists a strand s′ that
is effectively equivalent to s in k0 and k1 is isomorphic to both k0 with s
                                                     Ts
removed and k0 with s′ removed. In detail, k0 −→         k1 if and only if there
                  ′
exists a strand s such that
  1. strands s and s′ are not in the image of k0 ’s strand map from the
     point-of-view skeleton;
  2. Θk0 (s) is isomorphic to Θk0 (s′ );
  3. let k1 be k0 with strand s removed, along with extraneous origination
     assumptions;
  4. let k2 be k0 with strand s′ removed, along with extraneous origination
     assumptions;
  5. k1 is isomorphic to k2 .
                                              Ts           sT
    For the setwise thinning reduction, {k0 } −↠ {k1 | k0 −→ k1 }, when there
                      Ts
is a k1 such that k0 −→ k1 .
    Thinning in cpsa is also implemented for the case of sets of multiple
strands rather than pairs of individual strands. The correctness of thinning
has yet to be demonstrated.

### 8.1 Reduction Systems

Notice that a setwise hulling reduction may produce the empty set, but a
setwise order enrichment and thinning reduction never does.
   There are two preskeleton reduction systems, one with thinning, and one
                                                S     H      O
without. For the one without, let reduction ↠= s,s′ −↠ ∪ −↠.

**Definition 8.4 (Preskeleton Reduction System).** Preskeleton k0 reduces to
                         skel
skeleton k1 , written k0 −→ k1 , if {k0 } ↠∗ K, k1 ∈ K, and K is a normal
form of ↠.
                         skel
   For each skeleton k, k −→ k.
                                        S      H    O  S Ts
   When using thinning, let reduction ↠= s,s′ −↠ ∪ −↠ ∪ s −↠.

**Definition 8.5 (Preskeleton Reduction System with Thinning).** Preskeletskel

ton k0 reduces to thinned skeleton k1 , written k0 −→ k1 , if {k0 } ↠∗ K,
k1 ∈ K, and K is a normal form of ↠.
                                 tskel
   For each thinned skeleton k, k −→ k.

## Spec Chapter 9: Penetrator Derivability (`Tp : Ta |- t`)

For each algebra, the powers of the adversary are defined by a set of roles.
For the Basic Crypto Signature in Figure 2.1, the traces of the penetrator
roles are in Figure 9.1. Penetrator roles make no origination assumptions.
    The context in which penetrator strands appear determine the messages
the adversary can derive. The context includes previously sent messages
and atoms it is forbidden to originate. An atom that is assumed to be non-originating
 must be avoided as is a uniquely originating atom that is assumed
to originate on a regular strand.
    The ternary relation Tp : Ta ⊢ t states that message t is penetrator
derivable from previously sent messages Tp while avoiding atoms Ta . The
relation is defined by a set of inference rules. Most of the rules are justified by
a penetrator role that when instantiated, derives a message in the conclusion

of the rule. Note there are no rules that pertain to channel messages. Channel
messages are handled elsewhere.

**Figure 9.1: Penetrator Traces**

```text
    base(t) = ⟨+t⟩, where t is an atom
      tag(t) = ⟨+t⟩, where t is a tag
pair (t0 , t1 ) = ⟨−t0 , −t1 , +(t0 , t1 )⟩
 sep(t0 , t1 ) = ⟨−(t0 , t1 ), +t0 , +t1 ⟩
 enc(t0 , t1 ) = ⟨−t0 , −t1 , +{|t0 |}t1 ⟩
 dec(t0 , t1 ) = ⟨−{|t0 |}t1 , −t2 , +t0 ⟩, where t2 = inv (t1 )
    hash(t) = ⟨−t, +#t⟩
   put(c, t) = ⟨−t, +[c, t]⟩
  take(c, t) = ⟨−[c, t], +t⟩
```

    The first rule states that no additional penetrator behavior is required to
derive t if it has been previously sent.
                                    t ∈ Tp
                                                                          (9.1)
                                  Tp : Ta ⊢ t

By base(t):
                            t an atom      t∈/ Ta
                                                                          (9.2)
                                 Tp : Ta ⊢ t
By tag(“. . . ”):
                                Tp : ta ⊢ “. . . ”                        (9.3)
By pair (t0 , t1 ):
                         Tp : Ta ⊢ t0     Tp : Ta ⊢ t1
                                                                          (9.4)
                               Tp : Ta ⊢ (t0 , t1 )
By sep(t0 , t1 ):
                               Tp : Ta ⊢ (t0 , t1 )
                                                                          (9.5)
                                 Tp : Ta ⊢ t0
By sep(t0 , t1 ):
                               Tp : Ta ⊢ (t0 , t1 )
                                                                          (9.6)
                                 Tp : Ta ⊢ t1
By enc(t, k):
                          Tp : Ta ⊢ t     Tp : Ta ⊢ k
                                                                          (9.7)
                                Tp : Ta ⊢ {|t|}k
By dec(t, k):
                      Tp : Ta ⊢ {|t|}k     Tp : Ta ⊢ inv k
                                                                          (9.8)
                                   Tp : Ta ⊢ t
By hash(t):
                          Tp : Ta ⊢ t     Tp : Ta ⊢ k
                                                                          (9.9)
                                 Tp : Ta ⊢ #t
A non-base sorted variable is derivable in a bundle that instantiates it with
any message other than an element of X⊤ .
                                   t ∈ X⊤
                                                                        (9.10)
                                  Tp : Ta ⊢ t

**Definition 9.1 (Sent Channel Messages).** The sent channel messages of
skeleton k at n is sntchmsg(k, n) = {msg k (n0 ) | n0 ≺k n, n0 is transmitting}.

**Definition 9.2 (Public Messages).** The public messages of skeleton k at n
is
       pubmsg(k, n) = {t | [t] ∈ M } ∪ {t | [c, t] ∈ M ∧ c ∈
                                                           / conf (k)},
where M = sntchmsg(k, n), and conf (k) is the set of channels assumed to
be confidential in k.

**Definition 9.3 (Avoidance Set).** The avoidance set of skeleton k is avoid (k) =
Nk ∪ {t | t ∈ Uk ∧ |Ok (t)| = 1}.

   An atom in avoid (k) is not available to the penetrator, except if it is
exposed by a messages transmission. Clearly, only uniquely originating atoms
can be exposed.

**Definition 9.4 (Derivable Before).** A channel message m is derivable before
reception node n in skeleton k, written der (k, n, t), if

  1. m ∈ sntchmsg(k, n),

  2. m = [t] and Tp : Ta ⊢ t, or

  3. m = [c, t], c ∈
                   / auth k, and Tp : Ta ⊢ t,

where Tp = pubmsg(k, n), Ta = avoid (k), and auth(k) is the set of channels
assumed to be authenticated in k.

**Definition 9.5 (Realized Node).** A reception node n is realized in skeleton k
if msg k (n) is derivable before n in k.

   Notice that one can read off penetrator behavior from the proof tree used
to demonstrate that msg k (n) is derivable before n in k. For example, if
a decryption step is required by the proof, an instance of the penetrator’s
decryption role is indicated. In a bundle, for a non-base sorted variable,
there is a substitution that maps the variable to a message that is not a non-base
 sorted variable. The substitution determines the penetrator behavior
associated with the variable.

**Conjecture 9.1 (Realized Skeleton).** A skeleton is realized if and only if all
of its reception nodes are realized.

Partial Proof. Given a skeleton k in which all of its reception nodes are realized
, the combination of the regular behavior in the skeleton, the penetrator
behavior specified by the proof trees used to demonstrate each node is realized
, and a substitution for non-base sorted variables determines a bundle.
The skeleton of the bundle may have more non-originating atoms than is
in Nk , however since the extra non-originating atoms are derivable by the
bundle that realizes k, the proof trees for those atoms specify any additional
penetrator behavior required.
    The “only if” part of this proof has yet to be completed.

### 9.1 Implementation

The derivable before a node predicate is implemented using auxiliary functions
.

**Definition 9.6 (Buildable).** Message t is buildable from previously sent messages
 Tp while avoiding Ta , written bld (t, Tp , Ta ), if Tp : Ta ⊢ t without the
use of Inference Rules 9.5, 9.6, and 9.8.

   Consider the following reduction system based on Inference Rules 9.5,
9.10, 9.6, and 9.8.

                   Tp : Ta → Tp : Ta \ {t}                      if t ∈ Tp and t ∈ Ta
                   Tp : Ta → Tp \ {x} : Ta                      if x ∈ Tp and x ∈ X⊤
    {(t0 , t1 )} ∪ Tp : Ta → {t0 , t1 , (t0 , t1 )} ∪ Tp : Ta   if t0 or t1 ∈/ Tp
    {{|t0 |}t1 } ∪ Tp : Ta → {t0 , {|t0 |}t1 } ∪ Tp : Ta        if t0 ∈
                                                                      / Tp and
                                                                bld (inv (t1 ), Tp , Ta )

**Definition 9.7 (Decompose).** Previously sent messages Tp and avoidance
set Ta decompose to Tp′ , Ta′ , written decompose(Tp , Ta ) = (Tp′ , Ta′ ), if Tp :
Ta →∗ Tp′ : Ta′ and (Tp′ , Ta′ ) is a normal form of reduction →.

   The penetrator derivable predicate Tp : Ta ⊢ t is implemented as

                        Tp : Ta ⊢ t =
                          let Tp′ , Ta′ = decompose(Tp , Ta ) in
                          bld (t, Tp′ , Ta′ )
   The decomposition at a node function is

               dcmp(k, n) =
                 decompose(pubmsg(k, n), avoid (k))
The derivable before a node predicate is implemented as
                   der (k, n, t) =
                     let Tp , Ta = dcmp(k, n) in
                     bld (t, Tp , Ta )

## Spec Chapter 10: Carried Only Within (`cows`)

A set of encryptions Te protects critical message t in message t′ if t is carried
by t′ only within a member of Te . The definition of the carried only within
(cow) relation to follow makes this concept precise. The concept is used
when solving authentication tests (Chapter 11).

**Definition 10.1 (Ancestors).** Let t′ = t @ p. The ancestors of t′ in t at p is
the set anc(t, p) = {t @ p′ | p′ a proper prefix of p}.

**Definition 10.2 (Carried Only Within).** Message t is carried only within
set Te in t′ if for all carried positions p of t in t′ , there exists an ancestor ta ∈
anc(t′ , p) and te ∈ Te such that ta ≡ te .

   The function defines carpos(t, t′ ) is defined on Page 6, the set of positions
at which t′ carries t. The interface to each algebra exports unify 0 , where

               unify 0 (t, t′ , σ) = {σ ′ ◦ σ | σ ′ ∈ unify(σ(t), σ(t′ ))}.

Unification is extended to channel messages as:

             unify0 ([t], [t′ ], σ) = unify0 (t, t′ , σ)
             unify0 ([c, t], [c′ , t′ ], σ) =
                  {σ ′′ | σ ′ ∈ unify0 (c, c′ , σ) ∧ σ ′′ ∈ unify0 (t, t′ , σ ′ )}

   The details of a reduction on skeletons called a augmentation will be
described in Section 11.2. In simplified form, for an augmentation, given t, Te ,
and t′ , one must find all most general unifiers σ such that σ(t) is carried only
within set σ(Te ) in σ(t′ ).

    A carried only within solution cannot be directly computed using Definition
 10.2. Given terms ta and te , the unify 0 function finds substitutions σ
such σ(ta ) ≡ σ(te ), however, the carried positions carpos(σ(t), σ(t′ )), are
used before the unify 0 function computes the substitution σ. Figure 10.1
displays the iterative procedure that breaks the cyclic dependencies. Each
step of the iteration improves an approximation of a solution to the problem.
The correctness of this function is shown in [9], although for a version of the
algorithm with the alternate definition for the function fold in Figure 10.2.

**Figure 10.1: The cows Function**

```text
cows(t, T, t′ ) =
  cows 0 (t, T, t′ , σid )   — σid is the identity subst

cows 0 (t, T, t′ , σ) =
  if σ(t) is cow σ(T ) at σ(t′ ) then
     {σ}
  else
     let S = fold (t, T, t′ , σ) in
                              ′   ′
     S
        σ ′ ∈S cows 0 (t, T, t , σ )

fold (t, T, t′ , σ) =
   {σ ′ ◦ σ | σ ′ ∈ fold 0 (σ(T ), σ(t′ ), {σid }, carpos(σ(t), σ(t′ )))}

fold 0 (T, t′ , S, {}) = S
fold 0 (T, t′ , S, ⟨p⟩ ⌢ P ) =
   fold 0 (T, t′ , solve(anc(t′ , p), T, S), P )

solve(T, T ′ , S) =
  {σ ′ | t ∈ T, t′ ∈ T ′ , σ ∈ S, σ ′ ∈ unify 0 (t, t′ , σ)}
```

**Figure 10.2: The Alternate fold Function**

```text
fold (t, T, t′ , σ) =
   fold 0 (t, T, t′ , σ, {σid }, carpos(σ(t), σ(t′ )))

fold 0 (t, T, t′ , σ, S, {}) = {σ ′ ◦ σ|σ ′ ∈ S}
fold 0 (t, T, t′ , σ, S, ⟨p⟩ ⌢ P ) =
   fold 0 (t, T, t′ , σ, solve(anc(σ(t′ ), p), σ(T ), S), P )
```

## Spec Chapter 11: Solving Authentication Tests and Cohort Augmentation

**Definition 11.1 (Protectors).** The protectors of t are encryptions that carry t
and cannot be decrypted. Function prot(Tp , Ta , t) is undefined if bld (t, Tp , Ta ),
otherwise

    prot(Tp , Ta , t) = {{|t0 |}t1 ∈ Tp | t0 carries t and ¬ bld (inv (t1 ), Tp , Ta )}

**Definition 11.2 (Escape Set).** The escape set for message tc at n in skeleton
 k, esc(k, n, tc ), contains encryptions and channel messages. Function
esc(k, n, tc ) = prot(tc , Tp , Ta ) ∪ M , where (Tp , Ta ) = dcmp(k, n) (See Definition
 9.7), and M is the set of sent channel messages with confidential channels
that carry tc . It is undefined when tc is derivable in k at n.

**Definition 11.3 (Critical Position, Critical Message).** Position p is a critical
position at n in k if for m = msg k (n)

   1. p is a carried position in m,

   2. m @ p is not derivable before n in k,

   3. either

       (a) m @ p ∈ Uk ,
       (b) m @ p = #t1 ,
       (c) m @ p = {|t0 |}t1 and t1 is not derivable before n in k, or
       (d) m = [c, t], p = ⟨⟩, and c ∈ auth(k).

  4. anc(t, p) ∩ esc(k, n, t @ p) = ∅.

The message at a critical position is called a critical message.

**Definition 11.4 (Authentication Test).** The triple (k, n, p) is an authentication
 test iff p is a critical position at reception node n in k.

     An authentication test is a nonce test if the critical message is an atom,
it is a channel test if the critical message is a channel message, otherwise it
is an encryption test. (A hash is treated as a kind of encryption in which
the term that is hashed is the encryption key.) Observe that every critical
message at a node in a skeleton is not derivable at the node.

**Conjecture 11.1.** A reception node is unrealized iff it has a critical position.

**Definition 11.5 (Target Messages).** Let Te be a set of messages, and tc be
a message. The set of target messages is

   targ(tc , Te ) = {tc } ∪ {tt | te ∈ Te , p ∈ carpos(tc , te ), tt ∈ anc(te , p)} \ Te .

**Definition 11.6 (Critical Position Solved).** Suppose p is a critical position
                     ϕ,σ
at n in k0 and k0 7−→ k1 . Let t = msg k0 (n)@p, and T = esc(k0 , n, t). Critical
position p is solved in k1 after k0 at n if:

  1. anc(msg k1 (ϕ(n)), p) ∩ σ(T ) ̸= ∅, or

  2. for some tp ∈ sntchmsg(k1 , ϕ(n)), σ(t) is not carried only within σ(T )
     in tp , or

  3. targ(σ(t), σ(T )) \ σ(targ(t, T )) ̸= ∅ and there are variables in k’s protocol
 that are not atoms, or

  4. the decryption key of a member of σ(T ) is derivable before ϕ(n) in k1 ,
     or

  5. σ(t) is an encryption and its encryption key is derivable before ϕ(n)
     in k1 .

### 11.1 Test Solving Steps

A step used to solve a test is a contraction (Definition 11.7), a regular augmentation
 (Definition 11.8), a displacement (Definition 11.9), or a listener
augmentation (Definition 11.10).
**Definition 11.7 (Contraction).** Let p be a critical position at n in k, t =
msg k (n), and Te = esc(k, n, t@p). Suppose there is a substitution σ such that
for some ta ∈ anc(t, p), te ∈ Te , σ(ta ) = σ(te ). Skeleton k1 is a contraction if
   Sσ      tskel
k −→   k0 −→ k1 .
   cpsa computes a set of substitutions for each critical position, and then
removes some substitutions to form a complete set of most general unifiers.
Only most general unifiers are used for contractions.
**Definition 11.8 (Regular Augmentation).** Suppose substitution σ, non-listener
 role r, and trace C are selected as described in Section 11.2. Skele-
                                       σ             S        An,r,C      tskel
ton k2 is a regular augmentation if k −→ k0 −→ k1 −→ k2 .
**Definition 11.9 (Displacement).** Let substitution σ, non-listener role r, and
trace C be selected as described in Section 11.2, and there be a preskeleton k1
               S       An,r,C
such that k −→   σ
                    k0 −→ k1 . Suppose there are strands s and s′ , where one
of them is the newly created strand, and a most general unifier σ ′ such
that σ ′ (Θk1 (s)(j)) ≡ σ ′ (Θk1 (s′ )(j)) for 0 ≤ j < |Θk1 (s)|. Skeleton k4 is a
                    σ S ′       Cs,s′       tskel
displacement if k1 −→ k2 −→ k3 −→ k4 .
**Definition 11.10 (Listener Augmentation).** Let p be a critical position at n
in k, tc = msg k (n) @ p, and Te = esc(k, n, tc ). For each {|t0 |}t1 ∈ Te , skele-
                                                         An,lsn,C      tskel
ton k1 is a listener augmentation if k −→ k0 −→ k1 and C listens for
inv (t1 ), i.e. C = ⟨− inv (t1 ), + inv (t1 )⟩. If tc = {|t0 |}t1 , then skeleton k1 is a
                                 An,lsn,C       tskel
listener augmentation if k −→ k0 −→ k1 and C = ⟨−t1 , +t1 ⟩.
   For regular augmentation and displacement, cpsa removes solutions that
lead to skeletons that are less general than other solutions, that is, when
there is a homomorphism from a solution to the omitted solution.
**Definition 11.11 (Cohort Member).** For unrealized node n in a skeleton k0 ,
                           n,p
and a position p at n, k0 −→ k1 asserts that k1 is a member of the cohort of k0 ,
where k1 is derived using contraction, regular augmentation, displacement,

or listener augmentation, and p is solved in k1 after k0 at n. For the setwise
                                     n,p       n,p
cohort member reduction, {k0 } −↠ {k1 | k0 −→ k1 }, when n is unrealized
in k0 , and p is a critical position at n.
                                                          n0 ,p0   n1 ,p1   nℓ−1 ,pℓ−1
**Conjecture 11.2 (Critical Message Solved).** If k0 −→ k1 −→ . . . −→ kℓ
is a sequence of cohort member reductions, then for positive ℓ, p0 is solved
in kℓ after k0 at n0 .

### 11.2 Augmentation

Let tc be the critical message that demonstrates n is a test node in skeleton k.
For each triple (σ, r, C) that satisfies some properties, there is a potential
                               tskel   An,r,Cσ   S
regular augmentation with −→ ◦ −→ ◦ −→.          When successful, the message t
in the last event of the added strand is outbound, carries σ(tc ), but σ(tc ) is
not carried only within escape set σ(Te ) in t, where Te = esc(k, n, tc ), the
escape set. Moreover, for every other message t in the strand, σ(tc ) is carried
only within escape set σ(Te ) in t. The last event in the strand is called a
transforming event, as this event no longer protects the critical message, but
events that precede it do.
    cpsa computes the parameters for a set of augmentation steps as follows.
Suppose skeleton k = kX ( , P, , , , ). First, compute the target messages,
Tt = targ(tc , Te ). Next, for each non-listener role r(Cr , Nr , Ur ) ∈ P and each
index h where Cr (h) = +t, a transmission, do the following.

Create fresh variables: Let σr be a sort preserving variable renaming,
    where the domain is the variables that occur in Cr †h, and every variable
    in the range does not occur in X or in P .

Insert critical message: For each message t′ carried by t, and each tt ∈
     targ(tc , Te ), consider most general unifiers σ ′ where, σ ′ (t′ ) = σ ′ (tt ) and
     σr ⊴ σ ′ . (In other words, σ ′ = σ0 ◦ σr for some σ0 .)

Ensure previous events do not transform: For each σ ′ , find most general
 unifiers σ such that for 0 ≤ i < h, σ(tc ) is carried only within
    σ(Te ) at σ(C(i)) and σ ′ ⊴ σ. The function cowt, presented in Figure
 11.1, performs the explorations, producing the substitutions S ′ =
    cowt(tc , Te , Cr † h, S). Function fold is defined in Figure 10.1. Let Sr,h
    be the set S ′ with non-most general unifiers removed.

**Figure 11.1: The cowt Function**

```text
cowt(t,
  S T, C, S) =
    σ∈S cowt 0 (t, T, C, σ)

cowt 0 (t, T, C, σ) =
  if ∀t ±t ∈ C → σ(t) is cow σ(T ) at σ(t′ ) then
     {σ}
  else
     cowt(t, T, C, foldn(t, T, C, {σ}))

foldn(t, T, ⟨⟩, S) = S
foldn(t, T, ⟨±t′ ⟩S
                  ⌢
                    C, S) =
   foldn(t, T, C, σ∈S fold (t, T, t′ , σ))
```

Ensure last event transforms: For each σ ∈ Sr,h , if σ(tc ) is not carried
    only with σ(Te ) at σ(C(h)), try augmenting with parameters n, r,
    σ ◦ C † h, and σ.
    For target terms to be the reasonable set for insertion of the critical message
, one must require that variables of sort message are acquired. This fact
needs to be explained and noted as another reason for the acquired variable
constraint.
    The following example shows the need for Item 3 in the definition of a
solved critical position. The protocol has two roles.

     init(a : N, n1 , n2 : D, k : A) = r(⟨+{|n1 , {|a, n2 |}k |}k , −{|a, n1 |}k ⟩, ∅, ∅)
       resp(n1 : D, m : ⊤, k : A) = r(⟨−{|n1 , m|}k , +m⟩, ∅, ∅)
where we use N for sort name, D for sort data A for sort akey, and ⊤ for
sort mesg to save space. Notice the responder declares m to be of sort mesg.
    The point-of-view skeleton k0 is:
        kY (⟨init(a′ , n′1 , n′2 , k ′ )⟩                              Role map
            {init(a′ , n′1 , n′2 , k ′ ), resp(n′′1 , m′′ , k ′′ )},   Protocol
            ⟨⟨+{|n1 , {|a, n2 |}k |}k , −{|a, n1 |}k ⟩⟩,               Traces
            ∅,                                                         Node orderings
            {k −1 },                                                   Non-origination
            {n1 })                                                     Unique origination

where Y = a : N, n1 , n2 : D, k : A.
    cpsa finds the nonce test (k0 , (0, 1), ⟨0, 1⟩) with critical message n1 . The
escape set E = esc(k0 , (0, 1), n1 ) = {{|n1 , {|a, n2 |}k |}k }.
    cpsa solves this test to produce skeleton k1 with a displacement that
                                          ϕ,σ
simply equates n1 and n2 . Thus, k0 7−→ k1 where ϕ = ⟨0⟩ and σ = {n1 7→
n2 }.
    Consider Definition 11.6, the definition of critical position solved. Item 1
does not apply because an ancestor of the image of the critical position does
not match E. Item 2 does not apply because (k1 , (0, 1), ⟨0, 1⟩) is a nonce
test. Item 4 does not apply because the key that protects the member of
the escape set is non-originating. Finally, Item 5 does not apply because the
critical message is not an encryption.
    Item 3 applies in this example because

                    targs(n1 , E) = {n1 , (n1 , {|a, n2 |}k )}
              targs(σ(n1 ), σ(E)) = {n2 , (n2 , {|a, n2 |}k ), (a, n2 )}.

so targs(σ(n1 ), σ(E)) \ σ(targs(n1 , E)) = {(a, n2 )}.
    Once n1 and n2 have been equated, cpsa easily finds the one shape by
adding a responder instance. The shape corresponds to a rather odd use of
the initiator role. The instance of that role picks a fresh value for n1 and
then makes use of that value for its n2 parameter. See Appendix B for more
on the relation between roles and the programs they specify.

## Spec Chapter 12: Collapsing and Preconditioning

The input preskeleton is preconditioned before it is subjected to authentication
 test solving. The preskeleton is converted to a skeleton and then
collapsing is applied so as to ensure all shapes are found. Collapsing handles
the case in which strands merged in the input lead to shapes.

**Definition 12.1 (Collapsing).** Let k0 and k1 be two skeletons such that
there are two strands, s and s′ , and a most general unifier σ such that
σ(Θk0 (s)(j)) ≡ σ(Θk0 (s′ )(j)) for all 0 ≤ j < |Θk0 (s)|. Then k0 collapses
                  clp          S         Cs,s′   skel
                                  σ
to k1 , written k0 −→ k1 , if k0 −→ k −→ k ′ −→ k1 .

**Definition 12.2 (Preconditioning).** For point-of-view preskeleton k0 , k0 is
                                   pre              skel   clp
preconditioned to k1 , written k0 −→ k1 , if k0 −→ k (−→)∗ k1 .

## Spec Chapter 13: Generalization (Deletion, Weakening, Separation, Forgetting)

The cohort reduction system produces a set of realized skeletons. Generalization
 attempts to convert that set into a set of skeletons. Not all possible
cases are implemented due to performance issues, so it is not uncommon to
find a realized skeleton in the output of a run of cpsa that is not a shape.

**Conjecture 13.1 (Shape Completeness).** Without generalization, cpsa produces
 a complete set of shapes among the realized skeletons in its output.

**Definition 13.1 (Generalize).** A skeleton k0 generalizes skeleton k1 , written
     <
k1 −→k k0 , if both k0 and k1 are realized, k0 and k1 are not isomorphic, there
is a homomorphism from a point-of-view skeleton k to k0 , and a strandwise
injective homomorphism k0 7→ k1 .
                                                             ≤
    If skeletons are allowed to be isomorphic, we write k1 −→k k0 , and note
       ≤
that −→k defines a partial ordering. Therefore, there are maximal elements
in the partial ordering. A shape associated with a preskeleton is a maximally
generalized realized skeleton derived from the preskeleton.
                                                                     pre
**Definition 13.2 (Shape).** Let k0 be a preskeleton such that k0 −→ k for
some skeleton k, and let k1 be a realized skeleton such that k 7→ k1 . Skele-
                               ≤
ton k2 is a shape of k0 if k1 −→k k2 , and k2 is maximal among skeletons that
generalize k1 .

    There are four generalization reductions used to transform a realized
skeleton into its shapes: deletion, weakening, forgetting, and separation.

**Definition 13.3 (Deletion).** Skeleton k0 generalizes by deletion skeleton k1 ,
            Dn               <          skel
written k1 −→  k k0 , if k1 −→k k0 , k2 −→ k0 , and k2 is the result of deleting
node n in k1 and all of the nodes that follow it in its strand.

**Definition 13.4 (Weakening).** Skeleton k0 generalizes by weakening skele-
                    Wn,n′             <            skel
ton k1 , written k1 −→ k k0 , if k1 −→k k0 , k2 −→ k0 , and k2 is k1 except
≺k2 = (≺k1 \ {(n, n′ )})∗ .

**Definition 13.5 (Forgetting).** Skeleton k0 generalizes by origination as-
                                              Ft               <          skel
sumption forgetting skeleton k1 , written k1 −→  k k0 , if k1 −→k k0 , k2 −→ k0 ,
and k2 is k1 except Uk2 = Uk1 \ {t} and Nk2 = Nk1 \ {t}.

    Sometimes a more general skeleton can be found by replacing some occurrences
 of one variable by a fresh variable. For variable separation, the
location of an occurrence of a variable is defined using a skeleton’s instance.
Recall that in the external syntax, strand s in skeleton k is described by an
instance of the form i(r, h, σ). (Instances are introduced in Section 5.4.)

**Definition 13.6 (Location).** Variable x is at location (s, y, p) in k if the
instance at Θk (s) is i(r, h, σ) and x = σ(y) @ p.

**Definition 13.7 (Variable Separation).** Skeleton k0 generalizes by variable
                                      Vt               <          skel
separation skeleton k1 , written k1 −→   k k0 , if k1 −→k k0 , k2 −→ k0 , and k2
is k1 except t is a variable that occurs in multiple locations in k1 , and k2 is
the result of replacing t with a variable t0 of the same sort at a proper subset
of t’s locations, where t0 occurs nowhere in k1 .

    When separating a non-originating term, both the term and its clone are
non-originating. When separating a uniquely originating term, either the
term or its clone is uniquely originating.
    What happens when separating t in k into t and t0 , and ltk(t, t) ∈ Nk ?
Should a skeleton k0 with ltk(t, t0 ) ∈ Nk0 be a candidate separation? Currently
, only skeletons k1 with ltk(t, t) ∈ Nk1 and ltk(t0 , t0 ) ∈ Nk1 are considered
.
                                                     gen      S Dn        S    Wn,n′
**Definition 13.8 (Generalization).** The reduction −→k = n −→            k ∪ n,n′ −→ k
  S Ft        S Vt
∪ t −→    k ∪ t −→k is the generalization relation. For the setwise generalgen
                  gen
ization reduction, {k0 } −↠k {k1 } when k0 −→k k1 .

    The fact that each generalization reduction replaces a singleton with just
a singleton requires explanation. It’s simply a matter of performance. If
all possibilities are considered, cpsa run time would become dominated by
generalization. Since generalization failures do not interfere with producing
a complete description of the input, an approximation of the set of shapes is
okay.
                                                    gen
**Conjecture 13.2 (Generalization).** The relation −↠k is terminating.

Discussion
In [5], the shapes of a point-of-view skeleton are said to be minimal, in
the partial ordering induced by injective homomorphism, among all realized
homomorphic images of the point-of-view skeleton. Minimal corresponds to
maximally generalized. The need for origination assumption forgetting was
not known when [5] was written. Generalization by variable separation uses
non-carried positions, and in particular, positions that traverse an atom edge.
Algebras in previous strand space papers have no concept of a position that
traverses an atom edge, and therefore cannot be used to specify generalization
by variable separation.
    Variable separation can be expensive when there are many possible ways
to separate variables. The implementation simply truncates the search when
it grows too large. The current implementation never attempts to separate
channel variables.

## Spec Chapter 14: Complete Skeleton Reduction System (`->>k`)

                     co    gen
Let reduction ↠k = (−↠ ∪ −↠k )+ . This reduction system specifies the cpsa
program.

**Conjecture 14.1.** The reduction ↠k is confluent.

**Conjecture 14.2 (Soundness).** Let k0 be a preskeleton and k be an unrealpre

ized skeleton such that k0 −→ k. Skeleton k1 is a shape of k0 if {k} ↠k K,
k1 ∈ K, and K is a normal form.

   The set of bundles denoted by preskeleton k, [[k]] is defined on Page 17.

**Conjecture 14.3 (Completeness).** Let k0 be a preskeleton and k be an
                                      pre
unrealized
         S    skeleton   such that k0 −→  k. For all K such that {k} ↠k K,
[[k0 ]] = k1 ∈K [[k1 ]].

## Acknowledgements
Carolyn Talcott and Leonard Monk provided valuable feedback on drafts of
this document.

## Appendix A: Penetrator Non-Origination Assumptions (`pen-non-orig`)

Penetrator non-origination assumptions have been added as an extension to
the basic strand space theory. An atom is penetrator non-originating in a
bundle if it originates on no penetrator strand, but each of its variables occurs
in some strand’s trace.
    Penetrator non-origination assumptions can be used to model passwords.
Several regular participants might know a password and originate it in a run
of a protocol, but an idealized password is one the penetrator cannot guess.
    A penetrator non-originating atom is similar to a non-originating atom,
except in that it can be carried. There are two definitions that require
change. Penetrator non-originating atoms must be added to the avoidance
set of Definition 9.3. When the message at a critical position is an atom (see
**Definition 11.**3, Item 3), instead of being uniquely originating, and can also
be penetrator non-originating.

## Appendix B: Programs Specified by a Role (Procedural Dataflow Relation)

Given the definitions in Chapter 3, a role can be viewed as an abstraction of
a program, and a strand as an abstraction of a run of a program. But what
program is specified by a role?
    Consider a role that contains the event −{|t0 |}t1 . If the program has the
decryption key inv (t1 ) before the message is received, the program could
decrypt the message and extract t0 . Alternatively, if the program has {|t0 |}t1 ,
or has t0 and the encryption key t1 , it might check to see if the received
message is the same as the expected message, and abort the run if not.
    Here is an example of when the second behavior is desired. In cpsa,
before hashing was part of the algebra, an encryption was used to represent
hashing. The hash of t, #t, expanded to {|“hash”, t|}h , where h was an
asymmetric key known to all, but no one knew h−1 . The tag “hash” was
added to the encryption so as to ensure a hash was never confused with
other uses of encryption.
    A role does not specify a valid program if the only possible way of interpreting
 the event −#t is by using h−1 to decrypt {|“hash”, t|}h . The
remainder of this section describes how this class of specification errors is
detected for the Basic Crypto Algebra.
    The behaviors associated with a trace depend on the set of messages
available initially. The behaviors are specified by a data flow relation, T0 , C ▷
T1 . For trace C, the relation T0 , C ▷ T1 asserts that when messages T0 are
available initially, there is a behavior of C that produces messages T1 .
    A derivation tree used to demonstrate T0 , C ▷ T1 shows the steps that
enable the flow of data. The tree can be linearized, and thus specifies a
sequential program that implements the role.

    The data flow relation is defined with the aid of a data flow relation for
a sequence of events, T0 , C ▷ T1 .

                                      T0 , ⟨±t⟩ ▷ T T, C ▷ T1
                  T, ⟨⟩ ▷ T
                                           T0 , ⟨±t⟩ ⌢ C ▷ T1
   The T0 , ⟨±t⟩ ▷ T1 relation is defined using the T0 , C ▷ T1 relation. An
outbound message can be formed if it is available initially
                                         t∈T
                                     T, ⟨+t⟩ ▷ T
or if it can be formed by construction.
                                                                            
                 T, ⟨+t1 , . . . , +tn ⟩ ▷ T          f (t1 , . . . , tn )
                 T, ⟨+f (t1 , . . . , tn )⟩ ▷ T       not an atom
   An inbound message makes atoms and acquired variables available.
                T, ⟨−t⟩ ▷ T ∪ {t} [t an atom or a variable]
When the decryption key is available, the contents of the encryption are
also available. Furthermore, the encryption can be sent in future messages
without access to its encryption key.
                     T0 , ⟨+ inv (t1 )⟩ ▷ T0 T0 , ⟨−t0 ⟩ ▷ T1
                         T0 , ⟨−{|t0 |}t1 ⟩ ▷ T1 ∪ {{|t0 |}t1 }
A received encryption that can be sent ensures the encryption agrees with
currently available terms and makes nothing new available.
                                 T, ⟨+{|t0 |}t1 ⟩ ▷ T
                                 T, ⟨−{|t0 |}t1 ⟩ ▷ T
   Consider an operation f other than the encryption operation. The order
in which messages that occur in a message constructed using f are made
available may determine if the decryption key of an encryption is available.
All possible orderings must be explored. Let πn be a permutation on the
domain of a sequence of length n.
                                                                          
                T0 , ⟨−t1 , . . . , −tn ⟩ ◦ πn ▷ T1   f (t1 , . . . , tn )
                 T0 , ⟨−f (t1 , . . . , tn )⟩ ▷ T1    not an atom
   The data flow relation is used to find initial sets of atoms that are compatible
 with some behavior of a trace that produces messages.

**Figure B.1: Two programs that implement the role ⟨+{|a, n|}Kb , −{|n|}Ka ⟩.**

```text
proc(a, n, Kb , Ka−1 )            proc(a, n, Kb , Ka )
  send({|a, n|}Kb );                send({|a, n|}Kb );
  x0 ← recv();                      x0 ← recv();
  x1 ← decrypt(x0 , Ka−1 );         x1 ← {|n|}Ka ;
  x1 ̸= n → fail;                   x0 ̸= x1 → fail;
end                               end
```

**Definition B.1 (Trace Parameters).** The set of atoms T0 are parameters of
trace C if T0 , C ▷ T1 for some T1 , and T0 is minimal, that is for all T0′ such
that T0′ , C ▷ T1 , T0′ ̸⊂ T0 .

    The role ⟨+{|a, n|}Kb , −{|n|}Ka ⟩ has two sets of parameters, {a, n, Kb , Ka−1 }
and {a, n, Kb , Ka }. See Figure B for two examples of programs that implement
 the role, using distinct parameter sets.
    The cpsa distribution contains a program that computes the set of parameters
 of a role. It was used to find an error in a role’s use of hashing as
described at the beginning of this section. The role in question is the verifier
role that is part of an attestation protocol [3]. In an earlier version of the
role, every set of parameters included the decryption key of the encryption
used as a hash. The role was so complicated that inspection did not reveal
the error.
    Note that this section is specific to the basic crypto algebra in the sense
that all non-atomic operations are assumed to be constructable, and encryption
 has the specific de-construction recipe shown. Although carried positions
were not mentioned in this section, the inference system specifies the same
concept. In fact, in future work we hope to show that the inference system is
all one needs to define, and that which positions are carried, which are protected
, and which sorts are atoms can be defined in terms of the inferences
available.

## Appendix C: Shape Analysis Sentences

For each point-of-view skeleton and its shapes found by cpsa, there is a
formula in a language of order-sorted first-order logic called  W a shape analysis
 sentence. The sentence has a special form, ∀X(Ψ ⊃ i ∃Yi (∆i ∧ Φi )),
where Ψ, ∆i , and Φi are conjunctions of atomic formulas and X and Yi are
variable sets. This fragment of first-order logic is called coherent logic. Formula
 Ψ describes the point-of-view skeleton k0 . For each homomorphism to
               δi
a shape, k0 7−→   ki , formula ∆i describes the structure preserving maps δi ,
and the shape ki is described by Φi .
    An interpretation of a shape analysis sentence is a skeleton. If cpsa finds
all of the shapes and the homomorphisms associated with a point-of-view
skeleton, the analysis’ sentence is satisfied in all realized skeletons. Let Σ be
a shape analysis sentence and Ψ be a security goal. If Σ ⊃ Ψ is a theorem in
order-sorted first-order logic, then Ψ is satisfied in all realized skeletons and
its protocol achieves this goal.
    Shape analysis sentences are closely related to security goals in [7], and
were motivated by that work. This material was extracted from [11], the
paper that introduced shape analysis sentences.

### C.1 Security Goals and Skeleton Formulas
The signature for security goal terms extends the one used for the underlying
message algebra with sort Z. Variables of this sort denote strands.
   Security goals make use of protocol specific and protocol independent
predicates. For each role rY (C, N, U ) ∈ P , there are strand length predicates

and strand parameter predicates. There are |C| unary length predicates
P [r, h] : Z, with 1 ≤ h ≤ |r|. Relative to skeleton k, P [r, h](z) asserts
that strand z in k is an instance of r and has a length of at least h. For
each variable x : S that occurs in C, there is a binary parameter predicate
P [r, x] : Z × S. Relative to skeleton k, P [r, x](z, t) asserts that strand z in k
is an instance of r in which x is instantiated as t.
    For each base sort B, there are unary predicates non : B and uniq : B.
non(t) asserts t is non-originating in k and uniq(t) asserts t uniquely originates
in k.
    Let m be the length of the longest role in P . There are m2 precedence
predicates prec[i, j] : Z × Z for 0 ≤ i, j < m. prec[i, j](x, y) asserts that node
(x, i) is before node (y, j) in k. There are 3m origin predicates uniq-at[i] :
B ×Z, with 0 ≤ i < m and B as before. uniq-at[i](t, z) asserts that t uniquely
originates in k at node (z, i). The predicate false has arity zero and, of course,
equality is binary.
    To improve the readability of formulas to follow, we write prec(x, i, y, j)
for prec[i, j](x, y) and uniq-at(t, z, i) for uniq-at[i](t, z).
    Let k = kX (P, I, ≺, N, U ) and let ≺− be the transitive reduction of ≺.
Recall that ΘX is the strand space defined by I, see Section 5.4. We de-fine
 F(k) = (Y, Φ), where Φ is k’s skeleton formula, and Y is the formula’s
variable set. For F(k) = (Y, Φ), the variable set Y is X augmented with a
fresh variable of sort Z for each strand in k. Let Z(s) be the strand variable
associated with strand s ∈ Dom(I).
    The formula Φ is a conjunction of atomic formulas composed as follows.
   • For each s ∈ Dom(I), let I(s) = i(r, h, σ) and z = Z(s). Assert
     P [r, h](z). Let r = r(C, N, U ). For each variable x ∈ Vars(C † h) and
     term t = σ(x), assert P [r, x](z, t).
   • For each (s, i) ≺− (s′ , i′ ) such that s ̸= s′ , assert prec(Z(s), i, Z(s′ ), i′ ).
   • For each t ∈ N , assert non(t).
   • For each t ∈ U and (s, i) ∈ Ok (t), assert uniq-at(t, Z(s), i).
   • For each t ∈ U without a point of origination in k, assert uniq(t).
   Given a set of homomorphisms δi : k0 7→ ki , its shape analysis sentence is
                                             _
               S(δi : k0 7→ ki ) = ∀X0 (Φ0 ⊃   ∃Xi (∆i ∧ Φi )),         (C.1)
                                                   i

where F(k0 ) = (X0 , Φ0 ). The same procedure produces Xi and Φi for
shape ki with one proviso—the variables in Xi that also occur in X0 must be
renamed to avoid trouble while encoding the structure preserving maps δi .
    The structure preserving maps δi = (ϕi , σi ) are encoded in ∆i by a conjunction
 of equalities. Map σi is coded as equalities between a message algebra
 variable in the domain of σi and the term it maps to. Map ϕi is coded as
equalities between strand variables in Φ0 and strand variables in Φi . Let Z0
be the strand variables freshly generated for k0 , and Zi be the ones generated
for ki . The strand mapping part of ∆i is
                             ^
                                   Z0 (s) = Zi (ϕi (s)).
                              s∈Dom(Z0 )

    The shape analysis sentence for the second analysis of Blanchet’s Simple
 Example Protocol in Section 5.1 is displayed in Figure C.1. The strand
length predicate P [r, h](z) is written rh (z), and the strand parameter predicate
 P [r, x](z, t) is written rx (z, t) with the protocol left implicit.

**Figure C.1: Shape Analysis Sentence for Blanchet’s Protocol**

```text
∀a0 , b0 : A, s0 : S, d0 : D, z0 : Z(
  resp 2 (z0 ) ∧ resp a (z0 , a0 ) ∧ resp b (z0 , b0 )
       ∧ resp s (z0 , s0 ) ∧ resp d (z0 , d0 )
       ∧ non(a−1 0 ) ∧ non(b0 )
                                −1

  ⊃
  ∃a1 , b1 , b2 : A, s1 : S, d1 : D, z1 , z2 : Z(
      z0 = z1 ∧ a0 = a1 ∧ b0 = b1 ∧ s0 = s1 ∧ d0 = d1
         ∧ resp 2 (z1 ) ∧ resp a (z1 , a1 ) ∧ resp b (z1 , b1 )
         ∧ resp s (z1 , s1 ) ∧ resp d (z1 , d1 )
         ∧ init 1 (z2 ) ∧ init a (z2 , a1 ) ∧ init b (z2 , b2 ) ∧ init s (z2 , s1 )
         ∧ uniq-at(s1 , z2 , 0) ∧ prec(z2 , 0, z1 , 0)
         ∧ non(a−1                −1
                   1 ) ∧ non(b1 )))
```

Semantics of Skeleton Formulas. Let k = kX (P, I, ≺, N, U ) and ΘX be
its strand space. When formula Φ is satisfied in skeleton k with order-sorted
variable assignment α, we write k, α |= Φ. For x : S ∈ X, α(x) is in the
carrier set of ĀX for sort S. For x : Z, α(x) ∈ Dom(ΘX ). We write ᾱ when α

is extended to terms in the obvious way. When sentence Σ is satisfied in
skeleton k, we write k |= Σ.

   • k, α |= P [r, h](z) iff h ≤ |ΘX (s)|, and for some σ,

                                 ΘX (s) † h = σ ◦ C † h

      where s = α(z) and r = r(C, N, U ).

   • k, α |= P [r, x](y, t) iff for some σ with σ(x) = ᾱ(t),

                                 ΘX (s) † h = σ ◦ C † h

      where s = α(z), r = r(C, N, U ), and h is the smallest ℓ such that x
      occurs in C † ℓ.

   • k, α |= prec(x, i, y, j) iff (α(x), i) ≺ (α(y), j).

   • k, α |= non(t) iff ᾱ(t) ∈ N .

   • k, α |= uniq(t) iff ᾱ(t) ∈ U .

   • k, α |= uniq-at(t, z, i) iff ᾱ(t) ∈ U and (α(z), i) ∈ Ok (ᾱ(t)).

   • k, α |= y = z iff ᾱ(y) = ᾱ(z).

    Let Σ be a shape analysis sentence and Ψ be a security goal. If Σ ⊃ Ψ is
a theorem in order-sorted first-order logic, then Ψ is satisfied in all realized
skeletons and its protocol achieves this goal.

Channel Formulas. This appendix has not been updated to reflect the
inclusion of channels into cpsa, but the changes made are straightforward.
There are two new unary predicate symbols, auth and conf, that are similar
to non except their argument must be a variable of sort chan. For skeleton k
and variable assignment α, auth(c) is satisfied iff α(c) ∈ auth(k), and conf(c)
is satisfied iff α(c) ∈ conf (k).

## Appendix D: Facts and Rules

Support for facts and rules was introduced in version 4.1 of cpsa.
    Each skeleton includes a small database of facts. A fact is a named
relation among fact terms. A fact term is either a strand of the skeleton or
an algebra term. For example, in skeleton k, a user may want to note that
strand 0 owns the private key for a by asserting fact (owns, ⟨0, a−1 ⟩).
    Each protocol includes a small collection of rules. A rule is a sentence in
the goal language presented in Section C.1. A rule is an axiom added to a
protocol. cpsa uses the axiom as a rewrite rule to derive zero or more new
skeletons from a skeleton produced during a cohort step.

## Bibliography
[1] Franz Baader and Tobias Nipkow. Term Rewriting and All That. Cambridge
 University Press, 1998.
[2] Franz Baader and Wayne Snyder. Unification theory. In Alan Robinson
 and Andrei Voronkov, editors, Handbook of Automated Reasoning,
    volume 1, chapter 8. The MIT Press, 2001. https://www.cs.bu.edu/
    fac/snyder/publications/UnifChapter.pdf.
[3] George Coker, Joshua Guttman, Peter Loscocco, Amy Herzog, Jonathan
    Millen, Brian O’Hanlon, John Ramsdell, Ariel Segall, Justin Sheehy, and
    Brian Sniffen. Principles of remote attestation. International Journal
    of Information Security, 10:63–81, 2011. 10.1007/s10207-011-0124-7.
[4] Dorothy E. Denning and Giovanni M. Sacco. Timestamps in key distribution
 protocols. Communications of the ACM, 24(8):533–536, August
    1981.
[5] Shaddin F. Doghmi, Joshua D. Guttman, and F. Javier Thayer. Searching
 for shapes in cryptographic protocols. In Tools and Algorithms
    for Construction and Analysis of Systems (TACAS), number 4424 in
    LNCS, pages 523–538. Springer, March 2007. Extended version at
    http://eprint.iacr.org/2006/435.
[6] Joseph A. Goguen and Jose Meseguer. Order-sorted algebra I: Equational
 deduction for multiple inheritance, overloading, exceptions and
    partial operations. Theoretical Computer Science, 105(2):217–273, 1992.
[7] Joshua D. Guttman. Security theorems via model theory. In Express
: Expressiveness in Concurrency, Workshop affiliated with Concur
, September 2009. Post-proceedings to appear in EPTCS, http:
    //www.eptcs.org/.

 [8] Joshua D. Guttman. Shapes: Surveying crypto protocol runs. In
     Veronique Cortier and Steve Kremer, editors, Formal Models and Techniques
 for Analyzing Security Protocols, volume 5 of Cryptology and
     Information Security Series. IOS Press, 2011.

 [9] Moses Liskov and John D. Ramsdell. Implementing strand space algebras
. http://www.ccs.neu.edu/home/ramsdell/papers/algimpl.
     pdf, 2011.

[10] Moses D. Liskov, Paul D. Rowe, and F. Javier Thayer. Completeness of
     CPSA. Technical Report MTR110479, The MITRE Corporation, 2011.

[11] John D. Ramsdell. Deducing security goals from shape analysis sentences
. The MITRE Corporation, April 2012. http://arxiv.org/abs/
     1204.0480.

[12] John D. Ramsdell and Joshua D. Guttman. CPSA Design. The MITRE
     Corporation, 2009. In https://github.com/mitre/cpsaexp source distribution
, doc directory.

[13] John D. Ramsdell and Joshua D. Guttman. CPSA Primer. The MITRE
     Corporation, 2009. In https://github.com/mitre/cpsaexp source distribution
, doc directory.
````

---
