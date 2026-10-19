# MITRE CPSA 4.4.9 Complete Keyword & Grammar Specification

This document provides the authoritative, exhaustive technical reference for every keyword, operator, sort, and construct supported by the MITRE Cryptographic Protocol Shapes Analyzer (CPSA 4.4.9).

Every entry defines:
1. **Grammar Production**: Formal syntax from MITRE Manual Tables 10.1 through 10.6.
2. **Algebra Availability**: Applicable under `basic`, `diffie-hellman`, or both.
3. **Context / Scope**: Where the keyword may appear in a `.scm` file.
4. **Semantics**: Dolev-Yao strand space and order-sorted algebraic interpretation.
5. **Scheme S-Expression**: Concrete `.scm` snippet.
6. **Pydantic Model / Field**: Corresponding Python type in `src/intermediate_representation/protocol_syntax_tree.py`.
7. **Compiler Diagnostic**: Error emitted by `cpsa4`, `cpsa4json`, or `cpsa4roletran` if misused.

---

## Table of Contents

1. [Top-Level Forms (Table 10.1)](#1-top-level-forms-table-101)
2. [Cryptographic Message Algebras (Tables 10.2 & 10.4)](#2-cryptographic-message-algebras-tables-102--104)
3. [Sorts & Types Hierarchy (Tables 10.2, 10.4, 10.5)](#3-sorts--types-hierarchy-tables-102-104-105)
4. [Role Declaration Keywords (Tables 10.1, 10.6 & Roletran)](#4-role-declaration-keywords-tables-101-106--roletran)
5. [Preskeleton Declaration Keywords (Tables 10.1 & 10.6)](#5-preskeleton-declaration-keywords-tables-101--106)
6. [Trace Events & State Actions (Section 10.2)](#6-trace-events--state-actions-section-102)
7. [Cryptographic Term Operators (Tables 10.3 & 10.5)](#7-cryptographic-term-operators-tables-103--105)
8. [First-Order Logic Rules & Goals (Table 7.1)](#8-first-order-logic-rules--goals-table-71)

---

## 1. Top-Level Forms (Table 10.1)

### `herald`
- **Grammar**: `(herald [symbol | string] alist)`
- **Algebra**: All
- **Context**: File header (must be the first form in the file).
- **Semantics**: Identifies the protocol verification suite and sets global analyzer parameters (step limits, strand bounds, default algebra).
- **Scheme Example**:
  ```scheme
  (herald "EDHOC Verification Suite" (bound 20) (algebra diffie-hellman))
  ```
- **Pydantic**: `CPSAProtocolSpecification.herald_comment`
- **Compiler Diagnostic**: `Expecting terms in algebra basic` (emitted if protocol uses `diffie-hellman` but herald omits `(algebra diffie-hellman)`).

### `defprotocol`
- **Grammar**: `(defprotocol id alg role+ rule* prot-alist)`
- **Algebra**: All
- **Context**: Top-level protocol definition.
- **Semantics**: Defines a security protocol with its constituent participant roles, message algebra, and optional rewrite rules.
- **Scheme Example**:
  ```scheme
  (defprotocol tls13 diffie-hellman
    (defrole client ...)
    (defrole server ...))
  ```
- **Pydantic**: `CPSAProtocolSpecification.protocol_name`, `CPSAProtocolSpecification.message_algebra`, `CPSAProtocolSpecification.roles`
- **Compiler Diagnostic**: `defprotocol: bad algebra` or `defprotocol requires at least one role`.

### `defskeleton`
- **Grammar**: `(defskeleton id vars strand+ skel-alist)`
- **Algebra**: All
- **Context**: Top-level problem query.
- **Semantics**: Declares a point-of-view preskeleton to be solved. Defines which strands have run and what initial assumptions (non-origination, unique origination) hold.
- **Scheme Example**:
  ```scheme
  (defskeleton tls13
    (vars (c s name) (cr sr text))
    (defstrandmax client (client_identity c) (server_identity s))
    (non-orig (privk s))
    (uniq-orig cr))
  ```
- **Pydantic**: `CPSAPreskeleton`
- **Compiler Diagnostic**: `Unknown role in defstrand` or `Variable not in skeleton scope`.

### `defmacro`
- **Grammar**: `(defmacro (id id*) body)`
- **Algebra**: All
- **Context**: Top-level S-expression.
- **Semantics**: Defines syntactic replacement macros. In CPSA 4, parameters inside the body are prefixed with `^` (e.g. `^x`). Expanded prior to analysis via `cpsa4 -e`.
- **Scheme Example**:
  ```scheme
  (defmacro (dh-key ^x ^y) (exp (exp (gen) ^x) ^y))
  ```
- **Pydantic**: Preserved via desugaring or compiled via `cpsa4 -e`.

### `defrule`
- **Grammar**: `(defrule id sentence alist)`
- **Algebra**: All
- **Context**: Inside `defprotocol` or at top level.
- **Semantics**: Defines an inference rule that fires during skeleton analysis to augment skeletons when antecedent conditions are satisfied.
- **Scheme Example**:
  ```scheme
  (defrule trust-anchor
    (forall ((a name))
      (implies (fact trusted a)
               (non-orig (privk a)))))
  ```
- **Pydantic**: `CPSAProtocolSpecification.rules`

### `defgenrule`
- **Grammar**: `(defgenrule id sentence alist)`
- **Algebra**: All
- **Context**: Top-level rule form.
- **Semantics**: Generalization of `defrule` supporting compound state transition relations across multiple strand positions.

### `defgoal`
- **Grammar**: `(defgoal id sentence+ alist)`
- **Algebra**: All
- **Context**: Inside `defskeleton` or at top level.
- **Semantics**: Asserts a formal security goal in first-order logic. CPSA evaluates whether all minimal realized shapes satisfy the conclusion.
- **Scheme Example**:
  ```scheme
  (defgoal nsl
    (forall ((n text) (z strd))
      (implies
        (and (p "init" z 2) (p "init" "n" z n) (non-orig (privk "b")))
        (exists ((y strd))
          (and (p "resp" y 2) (p "resp" "n" y n))))))
  ```
- **Pydantic**: `CPSAPreskeleton.goal`

### `deflemma`
- **Grammar**: `(deflemma id sentence alist)`
- **Algebra**: All
- **Context**: Top-level form.
- **Semantics**: Asserts a proven intermediate lemma to prune the search space during shape analysis.

### `comment`
- **Grammar**: `(comment string | any*)`
- **Algebra**: All
- **Context**: Any top-level or alist location.
- **Semantics**: Ignored by solver; preserved in output markup.
- **Pydantic**: `.comment` attributes on roles, skeletons, specifications.

---

## 2. Cryptographic Message Algebras (Tables 10.2 & 10.4)

### `basic`
- **Context**: `(defprotocol <id> basic ...)`
- **Semantics**: Standard Dolev-Yao term algebra over symmetric keys, asymmetric key pairs, hashes, and concatenations. Diffie-Hellman exponentiation operators (`exp`, `gen`, `mul`, `rec`) are strictly forbidden.

### `diffie-hellman`
- **Context**: `(defprotocol <id> diffie-hellman ...)`
- **Semantics**: Extends basic algebra with abelian group exponentiation modulo algebraic equations. Random exponents must be typed as `rndx` and declared under `uniq-gen`.

---

## 3. Sorts & Types Hierarchy (Tables 10.2, 10.4, 10.5)

| Sort Keyword | Super-Sort | Semantics & Usage | Roletran Allowed in `inputs`? |
|---|---|---|---|
| `name` | `mesg` | Principal identity atom (e.g. `client_identity`). Required argument for `(pubk name)`, `(privk name)`, `(ltk name1 name2)`. | Yes |
| `text` | `mesg` | Fresh unguessable nonces and random challenge tokens (e.g. `client_random`). Declared in `uniq-orig`. | No (if fresh) / Yes (if received) |
| `data` | `mesg` | Arbitrary payloads, secrets, premaster secrets, application data. | Yes |
| `skey` | `mesg` | Symmetric encryption keys. Any key variable used in `(enc payload key)` for symmetric crypto **must** have sort `skey`. | Yes |
| `akey` | `mesg` | Asymmetric public or private key variables. Inverted via `(invk k)`. Cannot be wrapped in `(pubk k)`. | Yes |
| `tag` | `mesg` | Constant domain separation strings or tag atoms. | Yes |
| `chan` | `mesg` | Directional communication channel (e.g. `ch`). Required by `cpsa4roletran`. | **Mandatory** |
| `locn` | `mesg` | Stateful memory cell identifier for state protocols using `load` and `stor`. | Yes |
| `rndx` | `expt` | Atomic, randomly generated Diffie-Hellman private exponent. **Must be declared in `uniq-gen`, NEVER `uniq-orig`**. | No |
| `expt` | `mesg` | Compound exponent expression or unconstrained received exponent in Diffie-Hellman groups. | Yes |
| `base` | `mesg` | Group element in Diffie-Hellman algebra (e.g. `(exp (gen) x)`). | Yes |
| `mesg` | Top | Universal top sort. Variables cannot be encrypted with sort `mesg` keys because inversion is undefined on `mesg`. | Yes |
| `fact` | Formula | Logical fact assertion sort used in state rules and facts declarations. | N/A |
| `strd` | Formula | Strand identifier sort in first-order rules and goals. | N/A |
| `indx` | Formula | Node height index sort in first-order rules and goals. | N/A |

---

## 4. Role Declaration Keywords (Tables 10.1, 10.6 & Roletran)

### `defrole`
- **Grammar**: `(defrole id vars trace role-alist)`
- **Semantics**: Defines principal behavior.

### `vars`
- **Grammar**: `(vars (id+ sort)*)`
- **Semantics**: Scope-bound variable type declarations: `(vars (c s name) (cr sr text) (k skey))`.

### `trace`
- **Grammar**: `(trace event+)`
- **Semantics**: Ordered sequence of directional communications.

### `inputs` / `params`
- **Grammar**: `(inputs term*)` (alias: `params`)
- **Semantics**: Procedural roletran formal parameters required to execute the role. Must include all channels. Every variable in `inputs` **must** appear in the trace.

### `outputs` / `returns`
- **Grammar**: `(outputs term*)` (alias: `returns`)
- **Semantics**: Procedural roletran return values yielded on handshake completion. Every variable in `outputs` **must** appear in the trace.

### `uniq-orig`
- **Grammar**: `(uniq-orig term+)`
- **Semantics**: Asserts that terms originate uniquely within this role across all protocol executions (e.g. fresh nonces of sort `text`).
- **Compiler Diagnostic**: `Role not well formed: uniq-orig x doesn't originate` (triggered if `x` is sort `rndx` or never sent in trace).

### `uniq-gen`
- **Grammar**: `(uniq-gen term+)`
- **Semantics**: Asserts unique generation for atomic Diffie-Hellman exponents of sort `rndx`.

### `non-orig`
- **Grammar**: `(non-orig term+)`
- **Semantics**: Asserts that keys (e.g. `(privk s)`, `(ltk a b)`) are never compromised and never originate on any strand.

### `pen-non-orig`
- **Grammar**: `(pen-non-orig term+)`
- **Semantics**: Penetrator non-originating assumption. Similar to `non-orig` but restricts the adversary from obtaining the term while allowing compromised strands.

### `conf`
- **Grammar**: `(conf chan+)`
- **Semantics**: Declares channels confidential; adversary cannot read traffic sent over these channels.

### `auth`
- **Grammar**: `(auth chan+)`
- **Semantics**: Declares channels authenticated; adversary cannot inject messages on these channels.

### `facts`
- **Grammar**: `(facts (id term*)*)`
- **Semantics**: User-defined logical relational assertions recorded upon reaching this role height.

### `priority`
- **Grammar**: `(priority (height integer)+)`
- **Semantics**: Solver heuristics overriding branch search priority.

---

## 5. Preskeleton Declaration Keywords (Tables 10.1 & 10.6)

### `defstrand`
- **Grammar**: `(defstrand role-name height (role-var skel-term)*)`
- **Semantics**: Instantiates a role strand up to a specific height with variable bindings.

### `defstrandmax`
- **Grammar**: `(defstrandmax role-name (role-var skel-term)*)`
- **Semantics**: Instantiates a role strand run to its maximum trace length.

### `deflistener`
- **Grammar**: `(deflistener term)`
- **Semantics**: A 1-node strand that receives `term`. Used to test secrecy. If penetrator cannot derive `term`, the listener is dead and 0 shapes are found.

### `precedes`
- **Grammar**: `(precedes ((s1 n1) (s2 n2))*)`
- **Semantics**: Enforces causal message ordering between strand node pairs.

### `leadsto`
- **Grammar**: `(leadsto ((s1 n1) (s2 n2))*)`
- **Semantics**: State synchronization ordering constraint.

---

## 6. Trace Events & State Actions (Section 10.2)

### `send`
- **Grammar**: `(send ch? term)`
- **Semantics**: Transmission of `term` over optional channel `ch`.

### `recv`
- **Grammar**: `(recv ch? term)`
- **Semantics**: Reception of `term` from optional channel `ch`. Must be destructible.

### `load`
- **Grammar**: `(load locn? term)`
- **Semantics**: Stateful read of `term` from optional memory location `locn` (sort `locn`). Never takes both a `chan` and a `locn`.

### `stor`
- **Grammar**: `(stor locn? term)`
- **Semantics**: Stateful write of `term` to optional memory location `locn` (sort `locn`). Never takes both a `chan` and a `locn`.

### `cheq`
- **Grammar**: `(cheq id term)`
- **Semantics**: Equality check annotation.

---

## 7. Cryptographic Term Operators (Tables 10.3 & 10.5)

### `enc`
- **Grammar**: `(enc term+ term)`
- **Arity**: $\ge 2$.
- **Semantics**: Encryption of 1 or more payload terms under a key. **The key is always the LAST argument**. Per Equation 10.1, the encryption key cannot be a variable declared of sort `mesg`.
- **Scheme**: `(enc m1 m2 k)` $\equiv \{| m_1, m_2 |\}_k$.
- **Pydantic**: `["enc", "m1", "m2", "k"]`.

### `hash`
- **Grammar**: `(hash term+)`
- **Arity**: $\ge 1$.
- **Semantics**: One-way cryptographic hash of terms.
- **Scheme**: `(hash m1 m2)` $\equiv \#(m_1, m_2)$.

### `cat`
- **Grammar**: `(cat term+)`
- **Arity**: $\ge 1$.
- **Semantics**: Concatenation / tuple pairing.
- **Scheme**: `(cat m1 m2)` $\equiv (m_1, m_2)$.

### `pubk`
- **Grammar**: `(pubk name) | (pubk tag_string name)`
- **Arity**: 1 or 2.
- **Semantics**: Public key corresponding to principal `name` (optionally scoped by a leading string `tag_string` per Table 10.3).
- **Compiler Diagnostic**: `Expecting a name` if applied to a key variable rather than a principal identifier, or `Malformed pubk` if the 2-argument order `(pubk tag_string name)` is reversed.

### `privk`
- **Grammar**: `(privk name) | (privk tag_string name)`
- **Arity**: 1 or 2.
- **Semantics**: Private key corresponding to principal `name` (optionally scoped by a leading string `tag_string` per Table 10.3).

### `invk`
- **Grammar**: `(invk akey_var)`
- **Arity**: 1.
- **Semantics**: Multiplicative algebraic inverse of asymmetric key variable $k^{-1}$.

### `ltk`
- **Grammar**: `(ltk name1 name2)`
- **Arity**: 2.
- **Semantics**: Long-term pre-shared symmetric key between principals.

### `bltk`
- **Grammar**: `(bltk name1 name2)`
- **Arity**: 2 (Diffie-Hellman only).
- **Semantics**: Bi-directional long-term key satisfying $bltk(a, b) = bltk(b, a)$.

### `exp`
- **Grammar**: `(exp base expt)`
- **Arity**: 2 (Diffie-Hellman only).
- **Semantics**: Modular exponentiation $h^x$.

### `gen`
- **Grammar**: `(gen)`
- **Arity**: 0 (Diffie-Hellman only).
- **Semantics**: Group generator constant $g$.

### `mul`
- **Grammar**: `(mul expt1 expt2 ...)`
- **Arity**: $\ge 2$ (Diffie-Hellman only).
- **Semantics**: Exponent multiplication $x \cdot y$.

### `rec`
- **Grammar**: `(rec expt)`
- **Arity**: 1 (Diffie-Hellman only).
- **Semantics**: Multiplicative inverse of exponent $x^{-1}$.

### `one`
- **Grammar**: `(one)`
- **Arity**: 0 (Diffie-Hellman only).
- **Semantics**: Multiplicative identity constant $1$.

---

## 8. First-Order Logic Rules & Goals (Table 7.1)

| Keyword | Production | Semantics |
|---|---|---|
| `forall` | `(forall (vdecl*) formula)` | Universal quantification |
| `exists` | `(exists (vdecl*) formula)` | Existential quantification |
| `implies` | `(implies antecedent conclusion)` | Logical implication |
| `and` | `(and formula*)` | Conjunction |
| `or` | `(or formula*)` | Disjunction |
| `not` | `(not formula)` | Negation |
| `equals` | `(equals term1 term2)` | Term syntactic equality |
| `prec` | `(prec strd indx strd indx)` | Precedence assertion between nodes $(s_1, i_1) \prec (s_2, i_2)$ |
| `leads-to` | `(leads-to strd indx strd indx)` | State synchronization constraint |
| `fact` | `(fact id term*)` | Relational fact predicate evaluation |
| `p` | `(p role_name indx [var] [term])` | Position predicate in goal syntax |
