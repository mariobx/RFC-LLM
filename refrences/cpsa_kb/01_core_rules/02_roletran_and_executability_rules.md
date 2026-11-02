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
