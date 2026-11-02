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
