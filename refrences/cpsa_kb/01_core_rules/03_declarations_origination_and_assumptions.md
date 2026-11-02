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
