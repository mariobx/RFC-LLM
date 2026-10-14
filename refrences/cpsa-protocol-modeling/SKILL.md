---
name: cpsa-protocol-modeling
description: Comprehensive guide and formal reference for CPSA 4 protocol modeling and RFC batch analysis
version: 3.1.0
metadata:
  hermes:
    tags: [formal-methods, cpsa, security-protocols, strand-spaces, rfc-analysis, cryptography]
    category: security
---

# CPSA 4 Protocol Modeling: The Comprehensive Reference

The Cryptographic Protocol Shapes Analyzer (CPSA 4) is a formal methods tool developed by MITRE that enumerates all minimal essentially different executions (*shapes*) consistent with a protocol run within the Dolev-Yao penetrator model.

> [!IMPORTANT]
> **Complete CPSA 4 Manual Reference Guide Available**:
> An exhaustive, chapter-by-chapter reference guide to the entire official MITRE CPSA 4 manual is maintained in:
> - [`pdf_refrence/CPSA4ManualRefrence.md`](pdf_manual/CPSA4ManualRefrence.md)

>
> Consult `CPSA4ManualRefrence.md` for section citations, complete BNF grammars, error dictionaries, state transition axioms, and search flags across all 11 chapters.

---

## 1. Complete CPSA 4 Language & Keyword Reference (from Manual Ch. 4 & 6)

### A. Sort Hierarchy (Order-Sorted Algebra)
Every variable declared in `(vars ...)` must have an explicit sort:
* `name`: Principals, identities, agents (e.g. `client_id`, `server_id`, `kdc_identity`, `ca_identity`).
* `text`: Nonces, challenges, timestamps, cleartext payloads (e.g. `client_nonce`, `server_challenge`).
* `data`: Opaque payload blocks, cookies, tokens, session IDs (conventionally used for unguessable random values).
* `skey`: Symmetric encryption and MAC keys (e.g. `session_key`, `preshared_key`).
* `akey`: Asymmetric public and private keys (e.g. `(pubk client_id)`, `(privk server_id)`).
* `tag`: Literal string tags used to disambiguate messages (e.g. `"client-hello"`, `"key-confirmation"`).
* `rndx`: **Atomic random Diffie-Hellman private exponents**. Subtype of `expt`. Used for fresh private DH keys chosen by an entity. Must first appear in an outbound transmission (`send`).
* `expt`: Compound exponent expressions or unconstrained exponents. Must first appear in an inbound reception (`recv`).
* `mesg`: Top of the message sort hierarchy. (Warning: do not encrypt with a variable of sort `mesg`).
* `chan`: Communication channels (used with `auth`, `conf`).
* `locn`: Mutable state memory cells (used with `load`, `stor`).
* `dev`: Hardware or device identifiers.

> [!CAUTION]
> **Sort `base` is DEPRECATED in CPSA 4.4.8+**:
> Declaring `(vars (x base))` aborts with `mkVar: Variables of sort base are now deprecated`.
> To represent public DH values, write `(exp (gen) rndx_var)` directly in message terms, with exponents typed `rndx`.

---

### B. Cryptographic Operators & Term Constructors
* `(enc term1 term2 ... key)`: Keyed encryption of message terms.
  * If `key` is sort `skey` $
ightarrow$ Symmetric encryption.
  * If `key` is `(pubk name)` $
ightarrow$ Asymmetric public-key encryption.
  * If `key` is `(privk name)` $
ightarrow$ Asymmetric digital signature.
* `(hash term1 term2 ...)`: Cryptographic one-way hash / digest.
* `(cat term1 term2 ...)`: Explicit concatenation / grouping of terms.
* `(pubk principal)`: Public key of `principal`. (Can also take optional sub-key tag: `(pubk "sig" principal)`).
* `(privk principal)`: Private key of `principal`. (Or `(privk "sig" principal)`).
* `(invk key)`: Algebraic inverse of an asymmetric key (`invk (pubk a) = privk a`).
* `(ltk principal_a principal_b)`: Directional long-term shared symmetric key (`ltk(a,b) != ltk(b,a)`).
* `(bltk principal_a principal_b)`: Bidirectional long-term shared symmetric key (`bltk(a,b) = bltk(b,a)`).
* `(exp base exponent)`: Modular / Diffie-Hellman exponentiation ($g^{xy}$).
* `(gen)`: The constant generator $g$ for Diffie-Hellman.
* `(one)`: The multiplicative identity $1$ for exponents.
* `(mul exp1 exp2 ...)`: Exponent multiplication ($x \cdot y$).
* `(rec exponent)`: Multiplicative inverse of an exponent ($x^{-1}$).

---

### C. Role Events (`defrole`)
* `(send term)` / `(recv term)`: Message transmission and reception over the public network.
* `(send chan term)` / `(recv chan term)`: Transmission / reception over a specific channel.
* `(load locn term)` / `(stor locn term)`: Read or update mutable state cells.

> [!IMPORTANT]
> **NO KEYWORDS IN ROLES (AVOID DUPLICATION & OVER-CONSTRAINING)**:
> Do **NOT** declare `uniq-orig`, `uniq-gen`, or `non-orig` inside `defrole`. Keep `defrole` strictly limited to `(vars ...)` and `(trace ...)`.
> **ALL assumption and constraint keywords belong in `defskeleton`!** This eliminates conflicting declarations and allows key compromise experiments.

---

## 2. PACKING SKELETONS WITH KEYWORDS AS MUCH AS POSSIBLE

> [!IMPORTANT]
> **Why Skeletons Must Be Packed with Keywords**:
> A raw skeleton without assumptions represents an unconstrained scenario where the adversary is free to invent keys out of thin air, guess nonces, or reflect messages back to the sender. This produces vacuous or degenerate shapes.
> 
> **Place ALL keywords in `defskeleton` (NOT in `defrole`)**:
> Pack every `defskeleton` with all appropriate keyword declarations to formally model the RFC's security environment:

### The Ten Critical Keywords for Skeletons:

1. **`non-orig` (Non-Origination)**:
   * **Definition**: Term is **carried nowhere** in any bundle. Never emitted in the clear or in carried positions by any honest or penetrator strand.
   * **Usage**: Put this on ALL long-term private keys and shared keys uncompromised in the RFC that are **never transmitted**:
     ```lisp
     (non-orig (privk server_identity) (privk client_identity) (ltk client_identity server_identity))
     ```
2. **`pen-non-orig` (Penetrator Non-Origination)**:
   * **Definition**: Key is carried on regular strands, but **never forged by the penetrator**.
   * **Usage**: Use for session keys, Kerberos tickets, or shared secrets that appear inside transmitted messages (even inside hashes):
     ```lisp
     (pen-non-orig session_encryption_key shared_secret)
     ```
     *(Warning: Using `non-orig` on a key emitted in a trace causes shape realization to fail. Use `pen-non-orig` instead!)*
3. **`uniq-orig` (Unique Origination)**:
   * **Definition**: Fresh value originating at **exactly one carried transmission** node.
   * **Usage**: Put this on every fresh challenge, nonce, or fresh session key:
     ```lisp
     (uniq-orig client_nonce server_challenge fresh_session_key)
     ```
4. **`uniq-gen` (Unique Generation for Diffie-Hellman)**:
   * **Definition**: Fresh value generated uniquely at a transmission node, **whether carried or not**.
   * **Usage**: Put this on all `rndx` private exponents! Because $x$ in $(g^x)$ is in an *uncarried* algebraic position, `uniq-orig` will error with `doesn't originate`. Always use `uniq-gen` for DH exponents:
     ```lisp
     (uniq-gen client_dh_priv_exponent server_dh_priv_exponent)
     ```
5. **`defstrandmax` vs `defstrand`** — *different arities, pick carefully*:
   * **`defstrandmax role maplet ...`** — no height field. Instantiates the role to its full trace length. Use this for a full run of the role.
   * **`defstrand role <INT> maplet ...`** — `INT` IS REQUIRED and must satisfy `1 <= INT <= length(role-trace)`, or CPSA fails with `Bad height`. Use this to analyze only a prefix of the role (e.g., a partial execution for a secrecy query).
   * **Pitfall**: using `defstrand` without a height, OR using `defstrandmax` with a height, produces `Malformed defstrand` — **not** a keyword/arity diagnostic. Because the CPSA `SExpr` parser feeds a malformed slist to `loadInsts` (cpsa/src/CPSA/Loader.hs), you can waste time debugging the wrong line. When this error appears, first check the `.scm` for a missing/extra paren **anywhere earlier in the file** — a malformed slist upstream of the skeleton often shows up as a defstrand error on the line where CPSA tried to bind an environment.
6. **`deflistener` (Confidentiality / Secrecy Proof)**:
   * **Definition**: Injects an active adversary listener observing a target secret term.
   * **Usage**:
     ```lisp
     (deflistener session_encryption_key)
     ```
   * **Proof Rule**: If CPSA terminates with `(dead)` or `(comment "Not a skeleton")` and **0 shapes**, secrecy is formally proven!
7. **`facts` (Inequality & Separation Constraints)**:
   * **Definition**: Prevents identity reflection attacks where an initiator mistakenly authenticates to itself.
   * **Usage**:
     ```lisp
     (facts (neq client_identity server_identity))
     ```
8. **`precedes` (Causal Ordering Constraints)**:
   * **Definition**: Explicitly asserts that a specific event on one strand happened before an event on another strand:
     ```lisp
     (precedes ((0 1) (1 0))) ;; Event 1 of strand 0 happened before event 0 of strand 1
     ```
9. **`auth` / `conf` (Channel Security)**:
   * **Definition**: Declares that a channel is authenticated (`auth`) or confidential (`conf`).
10. **`comment`**:
    * **Definition**: Documents the exact formal security query. **Must be on a single physical line!**

---

## 3. Seven Architectural Rules Learned from the Hermes Run

> [!CAUTION]
> **RULE 1: String Literals Must Be Single-Line**:
> CPSA's lexer parses `"` strictly. A line break inside quotes aborts parsing with `Bad char in string`. Keep every `(comment "...")` and string tag on one physical line!

> [!CAUTION]
> **RULE 8: The `defprotocol` Closer Is a STANDALONE LINE — NEVER Merge Into the Last Role's Close**
> Each `defrole` block ends with `)))` (3 closes: last send/recv → trace → role). After the LAST role's `)))`, a **standalone-`)` on its own line** — nothing else — closes the `defprotocol` form. Do NOT write `))))` on the last role's final line to absorb the protocol close — that consumes the one bracket `defrole` itself needs and produces `Unexpected end of input in list` (cpsa4:5:3) or the next role reported as `Role <name> not found`.
>
> The proven pattern (produced `PASS RFC-4252_SSH-Auth-PublicKey shapes=1` and `PASS RFC-4253_SSH-Transport-DH shapes=1`):
>
> ```lisp
> (defprotocol rfcXXXX-name basic
>   (defrole client (vars ...) (trace (send ...)))) ;; 3 closes on last line
> 
>   (defrole server (vars ...) (trace (recv ...)))) ;; 3 closes on last line
> ) ;; STANDALONE — closes defprotocol, nothing else on this line
> ```

> [!CAUTION]
> **RULE 2: `defskeleton` MUST Be a Top-Level Sibling (NEVER Nested in `defprotocol`)**:
> Close `(defprotocol ...)` with a closing `)` FIRST! In Scheme/Lisp, nesting `(defskeleton ...)` inside `defprotocol` is treated as an ignored association list. CPSA analyzes nothing, leading to the fatal error:
> ```
> cpsa4graph: Empty input
> make: *** [cpsa4.mk:24: model.xhtml] Error 1
> ```
> Skeletons must be top-level forms outside `defprotocol`.

> [!IMPORTANT]
> **RULE 3: Name `.scm` Files After the Protocol (NEVER Generic `protocol.scm`)**:
> Always name your `.scm` file after the RFC and protocol (e.g. `rfc4253_ssh_transport.scm`). This generates self-documenting `.txt`, `_shapes.txt`, and `.xhtml` artifacts and allows automated batch processing.

> [!IMPORTANT]
> **RULE 4: Run AST-Aware Paren Checking Before Compiling**:
> LLM context compaction often damages parenthesis balance. Run the upgraded AST paren checker:
> ```bash
> python3 /root/.hermes/profiles/work/skills/cpsa-protocol-modeling/scripts/check_parens.py --fix rfcNNNN_proto.scm
> ```
> It ignores comments and string escapes, identifies exact line-and-column mismatches, and can automatically repair missing closing brackets.
>
> **When CPSA emits `Malformed <keyword>` (defstrand, defstrandmax, deflistener, defrole, defprotocol, ...)** — the most common root cause is **imbalanced s-expressions EARLIER in the file**, not the keyword itself.
> Run a full-file depth scan before touching anything CPSA reported:
> ```python
> # Depth scan: prints final depth and any line where depth goes negative
> depth = 0
> for i, ln in enumerate(open(path, encoding='utf8').read().splitlines(), 1):
>     depth += ln.count('(') - ln.count(')')
>     if depth < 0:
>         print(f'NEG at L{i}: {ln.strip()[:80]}')
> print('final depth =', depth, '(must be 0)')
> ```
> If the final depth is non-zero, find the structural form that never closed (per-line trace back to the first line where the expected top-level boundary did NOT land). Fixing the paren will usually make the `Malformed ...` error disappear — that error was a downstream symptom, not the cause.

> [!IMPORTANT]
> **RULE 5: Carried vs Uncarried Keys (`non-orig` vs `pen-non-orig`)**:
> If a key appears *inside* any emitted term (e.g. a shared secret hashed into a response, or a distributed session key), CPSA treats it as carried. Declaring `non-orig` on it produces a contradiction and causes shape realization to fail. Use **`pen-non-orig`** for carried/emitted keys; reserve `non-orig` for keys that are never transmitted.

> [!IMPORTANT]
> **RULE 6: Symmetrical Message Pairing Across Roles**:
> Every `(send term)` in Role A must have a matching `(recv term)` in Role B. If an initiator sends a packet that no responder role ever receives (or receives with mismatched encryption), the protocol cannot advance and CPSA will treat the strand as dead.

> [!TIP]
> **RULE 7: Interpreting Secrecy Queries (`deflistener`)**:
> When testing secrecy via `(deflistener secret_term)`, deriving 0 shapes where the listener strand terminates as `(dead)` or `(comment "Not a skeleton")` is the formal mathematical proof that the adversary cannot derive the secret. Do NOT attempt to "fix" a dead listener—that is the exact desired outcome!

> [!IMPORTANT]
> **RULE 8: Strict CPSA Sorts (Never Invent Sorts)**:
> CPSA basic algebra only recognizes: `name`, `text`, `skey`, `atom`, `data`, `akey`.
> CPSA has **NO** sort named `key`, `nonce`, `cert`, `sign`, or `hash`. Declaring `(vars (n nonce))` causes compilation aborts. For nonces and challenges, always declare sort `text` or `data`.

> [!IMPORTANT]
> **RULE 9: Exact Role Identifier Alignment**:
> The role name in `(defstrand role-name ...)` and `(defstrandmax role-name ...)` must **EXACTLY** match the identifier in `(defrole role-name ...)`. A typo like `(defstrand ssh-server ...)` when the role was `(defrole server ...)` produces `Role <name> not found`.

> [!TIP]
> **RULE 10: Watch for Stale Duplicate Model Directories**:
> If the project tree contains BOTH `RFC-Models/` (plural, live) AND `RFC-Model/` (singular, legacy), or any other parallel directory with the same RFC sub-directory, `build_one.sh` will happily run against whichever path you pass. A stale duplicate `.scm` (often from a prior write that went to the wrong directory) will silently shadow the file you meant to build.
> Before diagnosing a `FAIL`: `ls <dir>/*.scm` for every plausible directory AND `grep -lrn '<defprotocol name>' <projectRoot> --include='*.scm'` to confirm you are debugging the right file.

> [!TIP]
> **RULE 11: Syntax Templates & Reference Guidelines**:
> Use `templates/single-procedure.scm` and `references/cpsa-4.4.9-keyword-and-grammar-spec.md` as reference templates for protocol construction.

> [!IMPORTANT]
> **RULE 12: The 20-Attempt Perseverance Protocol (Get Every Model to Compile)**:
> Do NOT give up or bail out after 1 compilation error. The mission is to get 100% of cryptographic protocol models to compile cleanly into realized shapes.
> Spend **up to 20 real fix attempts and iterative model adjustments** per protocol.
> Only after 20 real, distinct model edits that still fail compilation may you mark `failed_compilation`.

> [!IMPORTANT]
> **RULE 13: The Role Trace Invariant (`Identifier <name> unknown`)**:
> If CPSA fails with `Identifier <name> unknown` in `defstrand` or `defstrandmax`:
> Variable `<name>` is declared in `(vars ...)` but NEVER appears in `(trace ...)`.
> CPSA prunes unused variables from the role signature, so `defstrand` cannot bind it!
> **Fix**: Either include `<name>` in the message trace (e.g. in `cat` or `hash`), or remove `(<name> <name>)` from `defstrandmax`.

> [!IMPORTANT]
> **RULE 14: defstrandmax Maplets Must Be Simple Identifiers**:
> Maplets in `defstrand` and `defstrandmax` MUST be simple variable-to-variable bindings: `(role_var skel_var)`.
> Never put complex terms like `(cat ...)` or `(enc ...)` inside `defstrandmax` maplets. That triggers `Malformed maplet`.

> [!CAUTION]
> **RULE 15: Avoid Dynamic Shell Scripts / Heredocs (Tirith Security Scanner Stall)**:
> Never execute inline bash heredocs or dynamic Python one-liners in terminal. They get flagged by Tirith security scanner and time out waiting for interactive approval.
> Strictly use standard project tools: `bash build_one.sh <dir>`, `python3 update_progress.py ...`, and `python3 sync_checkpoint.py`.

> [!IMPORTANT]
> **RULE 16: The Roletran Algebra Boundary (`cpsa4roletran` vs `diffie-hellman`)**:
> `cpsa4roletran` implements procedural executability (constructibility and destructibility of messages) for the **`basic` algebra only**. It does NOT support Diffie-Hellman algebra and fails with `Expecting terms in basic algebra`.
> For `diffie-hellman` protocols, use `cpsa4 -l 1 <protocol>.scm` (step limit 1) as the pre-flight gate. It validates loader syntax, algebraic well-formedness, and scope in under 50ms without executing full search.

> [!IMPORTANT]
> **RULE 17: Role Declarations for Executability (Inputs, Outputs, Exports)**:
> In addition to `(trace ...)`, `cpsa4roletran` supports role-level declarations:
> - `(inputs var ...)`: Parameters known to the role prior to message reception. Decryption keys, identity credentials, and initial nonces must be declared in `inputs`.
> - `(outputs var ...)`: Values produced by the role that must be constructible from inputs and received messages.
> - `(exports var ...)`: Exported channel/interface variables.

> [!IMPORTANT]
> **RULE 18: Top-Level Forms Mastery (`deflemma`, `defrule`, `defgenrule`)**:
> - `deflemma`: Used to prove intermediate lemmas outside the protocol. Takes flags `rule`, `goal`, or `both` to automatically inject proven theorems into subsequent query searches.
> - `defrule`: Inference rule firing during preskeleton reduction when antecedent conditions are met.
> - `defgenrule`: Multi-strand relational state transition and causal precedence inference.

---

## 4. Standard CPSA Model Template

```
; Each defrole ends with )))  (3 closes: last send/recv + trace + role)
; A standalone-`)` on its own line after the last role closes defprotocol.
; Do NOT write `))))` on the last role's final line.
```

```lisp
(herald "RFC <NNNN> <Protocol_Name> Model"
  (algebra basic)) ;; or (algebra diffie-hellman) if using exp/gen/rndx

;; PROTOCOL DEFINITION
;; Each defrole ends with )))  (3 closes: last send/recv + trace + role)
;; A standalone ) on its own line after the last role closes defprotocol (RULE 8)
(defprotocol rfc<NNNN>-<proto-name> basic

  ;; ROLES: Define message structure only. NO uniq-orig or non-orig here!
  (defrole client_role
    (vars
      (client_id server_id name)
      (client_nonce server_challenge text)
      (session_key skey))
    (trace
      (send (enc client_nonce client_id (pubk server_id)))
      (recv (enc client_nonce server_challenge session_key (pubk client_id)))
      (send (enc server_challenge session_key)))) ;; 3 closes: send/recv + trace + role

  (defrole server_role
    (vars
      (client_id server_id name)
      (client_nonce server_challenge text)
      (session_key skey))
    (trace
      (recv (enc client_nonce client_id (pubk server_id)))
      (send (enc client_nonce server_challenge session_key (pubk client_id)))
      (recv (enc server_challenge session_key)))) ;; 3 closes: send/recv + trace + role
) ;; STANDALONE line — closes defprotocol

;; ====================================================================
;; SKELETON 1: Client Point of View (Authentication & Integrity)
;; ALL KEYWORDS AND ASSUMPTIONS GO HERE (NO DUPLICATES, NO DUPLICATES IN THE SAME SKELETON)
;; ====================================================================
(defskeleton rfc<NNNN>-<proto-name>
  (vars
    (client_id server_id name)
    (client_nonce server_challenge text)
    (session_key skey))
  (defstrandmax client_role
    (client_id client_id) (server_id server_id)
    (client_nonce client_nonce) (server_challenge server_challenge)
    (session_key session_key))
  ;; PACK KEYWORDS INTO SKELETON:
  ;; non-orig: NEVER on emitted/carried keys → use pen-non-orig instead!
  (non-orig (privk server_id) (privk client_id))
  (uniq-orig client_nonce session_key)
  (facts (neq client_id server_id))
  (comment "Client point of view: verify server authentication"))

;; ====================================================================
;; SKELETON 2: Confidentiality / Secrecy Query (Non-Disclosure)
;; ====================================================================
(defskeleton rfc<NNNN>-<proto-name>
  (vars
    (client_id server_id name)
    (client_nonce server_challenge text)
    (session_key skey))
  (defstrandmax client_role
    (client_id client_id) (server_id server_id)
    (client_nonce client_nonce) (server_challenge server_challenge)
    (session_key session_key))
  ;; Injects adversary listener to test if session_key is leaked:
  (deflistener session_key)
  (non-orig (privk server_id) (privk client_id))
  (uniq-orig client_nonce session_key)
  (facts (neq client_id server_id))
  (comment "Secrecy query: verify session_key cannot be derived by adversary"))
```

---

## 4.5 Debugging Loop: When a Model Refuses to Build

> [!CAUTION]
> **RULE 13: `Identifier <x> unknown` at a `defskeleton` boundary = unbalanced paren EARLIER, not a missing declaration.**
> CPSA reports the *first identifier after the boundary where balance broke*, not where the paren leaked. If defprotocol's closer absorbs one bracket too many (or too few), every `defstrandmax` maplet in the next skeleton resolves against a dead environment and dies with `Identifier <name> unknown` — the name cited is often a variable declared in the skeleton's own `(vars ...)`, which makes the error look like a missing declaration. It is not. Never "fix" by re-declaring the variable. Count the closer after the last role's final event: trace closes, role closes, defprotocol closes — one bracket each, exactly 3 after the last `send`/`recv` term's own closes. The canonical completed models (rfc4252, rfc4253) all obey this; diffing against them is the fastest verification.

> [!CAUTION]
> **RULE 14: `cat` is not a legal `defstrandmax` maplet → `Malformed maplet`.**
> A `defstrandmax` block is a list of `(var var)` maplets only. A bare term like `(cat "m" a b c)` as one of the maplets is rejected with `Malformed maplet`. Use `(defstrand role <height> ...)` for prefix bindings that need term patterns, or restructure to same-name maplets. If you need the role instantiated with a constructed term, use `defgoal` with `forall`/`implies` instead.

> [!IMPORTANT]
> **RULE 15: Debug loop — three moves that beat rewriting the model.
> (a) `make` without piping** — `build_one.sh` and `tail`/`head` pipes swallow the diagnostic. Run `make` raw; the `file.scm:L:COL: <diagnostic>` line is the ONLY signal you need.
> (b) Binary-search invariants — when the whole model fails, write a 10–20 line minimal variant in `/tmp/`, preserving only the suspect form (same-name maplets, `cat` maplet, `non-orig`+`enc` pairing, multi-name vars line). A minimal variant that FAILS pins the rule in seconds. A minimal variant that PASSES and the full model still fails means the interaction (not either form) is the cause — look for the boundary between them.
> (c) **Diff against reference templates** — `diff <(norm <(rfcNNNN.scm)) <(norm <(templates/single-procedure.scm))` where `norm` strips comments/whitespace.
> If all three fail, re-read `CPSA4_User_Manual.md` Chapter 4 for the exact keyword you're using — the manual is authoritative over memory. Don't write a new rule to your memory before it's reproduced in a minimal variant.

## 5. Compilation & Running Workflow

In every protocol directory `RFC-Models/RFC-<NNNN>_<ShortName>/`:

1. **Verify Parentheses**:
   ```bash
   python3 /root/.hermes/profiles/work/skills/cpsa-protocol-modeling/scripts/check_parens.py --fix rfcNNNN_proto.scm
   ```
2. **Initialize Makefile**:
   ```bash
   ~/.local/bin/cpsa4init
   ```
   *Run `cpsa4init` with no arguments*. This generates `Makefile` and `cpsa4.mk`.
3. **Compile**:
   ```bash
   make
   ```
   Compiles all `.scm` files into `.txt`, `_shapes.txt`, and `.xhtml`.
4. **Clean**:
   ```bash
   make clean
   ```

### Batch Helpers & Universal Storage:
* `CHECKPOINT.md` & `rfc_progress.csv`: Kept safely at project root (`HermesRunAndScripts/`) with backward-compatible symlinks in `RFC-Models/`.
* `get_next_rfc.py`: Queries next unworked RFC.
* `build_one.sh <dir> [name] [scm_base]`: Automates paren check, `cpsa4init`, and `make` (auto-detects the `.scm` file if omitted).
* `update_progress.py <RFC> <status> [dir] [notes]`: Updates CSV status.
* `sync_checkpoint.py [--log "note"]`: Syncs live status table in `CHECKPOINT.md`.

---

## 6. Companion Reference Guides

This skill includes specialized deep-dive reference documents:

| Guide | File Path | Focus & Core Insights |
|---|---|---|
| **CPSA 4 Manual Master Reference** | [`pdf_refrence/CPSA4ManualRefrence.md`](pdf_refrence/CPSA4ManualRefrence.md) | Exhaustive chapter-by-chapter mapping of all 11 chapters of the official MITRE CPSA 4 manual. |
| **CPSA 4.4.9 Complete Grammar & Keyword Spec** | [`references/cpsa-4.4.9-keyword-and-grammar-spec.md`](references/cpsa-4.4.9-keyword-and-grammar-spec.md) | Exhaustive syntax, Pydantic AST mapping, compiler diagnostics, and algebraic rules from MITRE manual Tables 10.1–10.6. |
| **Roletran & Verification Gate Guide** | [`references/roletran-and-compiler-diagnostics.md`](references/roletran-and-compiler-diagnostics.md) | Procedural executability (`cpsa4roletran`), constructibility/destructibility semantics, DH gate handling, and automated closed-loop diagnostic repair. |
| **Declarations & Freshness** | [`references/declarations.md`](references/declarations.md) | `non-orig` vs `pen-non-orig` vs `uniq-orig` vs `uniq-gen`. Why keywords belong in skeletons/goals rather than roles to enable compromise experiments. |
| **Goals & Skeletons** | [`references/goals-and-skeletons.md`](references/goals-and-skeletons.md) | First-order logic `defgoal` syntax (`forall`, `implies`, `exists`, `p`, `listener`, `prec`), maplet rules, injectivity, and agreement properties. |
| **Algebra, Macros & Lang** | [`references/algebra-and-macros.md`](references/algebra-and-macros.md) | `defmacro` preprocessing, `(lang ...)` algebra extensions, `tuple` vs `hash`, modeling encrypt-then-MAC, and limitations (counters/AEAD). |
| **Reading CPSA Output** | [`references/reading-output.md`](references/reading-output.md) | Decoding markers (`(realized)`, `(shape)`, `(dead)`, `(unrealized)`, `(aborted)`), interpreting primed variables (`x` vs `x-0`), diagnosing stuck runs. |
| **Channels & State** | [`references/state.md`](references/state.md) | Mutable memory cells (`load`, `stor`), `gen-st`, `trans`, scissors rule, `same-dev`, and the non-termination trap with initial-only state values. |
| **Termination & Search Flags** | [`references/termination.md`](references/termination.md) | Search bounds (`bound`, `limit`, `depth`), search order flags (`try-old-strands`, `check-nonces`, `reverse-nodes`), heap sizing (`+RTS -M4g -RTS`). |

