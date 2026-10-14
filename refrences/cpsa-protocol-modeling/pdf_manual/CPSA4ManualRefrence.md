# Cryptographic Protocol Shapes Analyzer (CPSA 4)
# Comprehensive Manual Reference & Technical Index

**Authoritative Technical Reference for MITRE CPSA Version 4.x**  
*Source Document:* `The Cryptographic Protocol Shapes Analyzer: A Manual for CPSA 4`  
*LaTeX Source Repository:* `/root/.hermes/profiles/work/skills/cpsa-protocol-modeling/manuals/`  
*Authors:* Moses D. Liskov, John D. Ramsdell, Joshua D. Guttman, Paul D. Rowe (The MITRE Corporation)

---

## Master Architecture & Document Map

The complete CPSA 4 manual is structured into four major parts across eleven chapters, supplemented by the CPSA Primer and formal syntax specifications. This index provides an exhaustive chapter-by-chapter mapping detailing where to find every concept, keyword, algebra sort, declaration, rule, goal syntax, channel, memory cell, algorithm phase, error message, and tool flag.

```
cpsa4manual/
├── intro.tex               ── Ch. 1: Introduction (Dolev-Yao model, bundles, shapes)
├── setup.tex               ── Ch. 2: Setup & Environment (cpsa4init, Makefiles, RTS flags)
├── basic.tex               ── Ch. 3: Basic Use of CPSA (Needham-Schroeder, Blanchet, graphs)
├── algebra.tex             ── Ch. 4: Cryptographic Algebra (BCA, Diffie-Hellman, lang field)
├── algorithm.tex           ── Ch. 5: The CPSA Algorithm (Cohorts, critical terms, 4 operations)
├── declarations.tex        ── Ch. 6: Declarations (non-orig, pen-non-orig, uniq-orig, uniq-gen)
├── goals.tex               ── Ch. 7: Security Goals & Rules (defgoal, defrule, deflemma, SAS)
├── channels_state.tex      ── Ch. 8: Channels and State (auth, conf, load, stor, state axioms)
├── troubleshooting.tex     ── Ch. 9: Troubleshooting & Error Reference (30+ error catalog)
├── input.tex               ── Ch. 10: CPSA Program & BNF Grammar (macros, include, heralds)
├── tools.tex               ── Ch. 11: CPSA Tools Ecosystem (all 12 companion utilities)
├── cpsaprimer.tex          ── Primer & Author Advice (Text vs data, progressive refinement)
├── bcasyntax.tex           ── Formal BCA Grammar Reference
├── macros.tex              ── TeX typesetting definitions
└── secureprotocols.bib     ── Complete bibliography of foundational literature
```

---

## Chapter 1: Introduction (`intro.tex`)

### 1.1 The Dolev-Yao Penetrator Model (§1.1)
* **The Adversary**: Modeled strictly within the Dolev-Yao framework. The penetrator controls the network: it can intercept, delay, duplicate, decompose, synthesize, and inject any message.
* **Ideal Cryptography**: The penetrator cannot break cryptography by guessing or brute-force. Keys must be learned legitimately or compromised. Hashes cannot be inverted. Encryptions cannot be decrypted without knowledge of the corresponding decryption key.
* **Strand Space Theory**:
  - **Strand**: A linearly ordered sequence of causal message events representing a local execution by a single participant or penetrator primitive.
  - **Node**: An individual transmission (`send` / `+`), reception (`recv` / `-`), memory store (`stor`), or memory load (`load`) on a strand, denoted `(s, i)` where `s` is the strand index and `i` is the zero-based step index.
  - **Bundle**: A finite, causally closed, acyclic directed graph of events representing a complete, physically realizable execution of the network. In a bundle:
    1. Every reception node is preceded by a matching transmission node.
    2. Within each strand, events occur in strictly increasing chronological order.
    3. The graph contains no causal directed cycles.

### 1.2 Shapes & The Shape Analysis Method (§1.2)
* **What is a Shape?** Given an initial scenario (a *skeleton* expressing a participant's point of view and trust assumptions), a *shape* is a minimal, fully-realized bundle compatible with the initial skeleton.
* **Homomorphism & Minimality**: Every concrete execution that could ever occur containing the initial skeleton is a homomorphic extension of at least one shape. Shapes capture the *essential*, non-redundant structural possibilities.
* **Authentication Test Method**: CPSA reasons backwards from an unexplained reception containing a fresh or secret component (*critical term*) to determine what honest strand must have created and sent it.

---

## Chapter 2: Setup & Environment (`setup.tex`)

### 2.1 Project Initialization (`cpsa4init`) (§2.1)
Running `cpsa4init` with **no arguments** sets up a standard CPSA project in the current working directory:
```bash
cpsa4init
```
It extracts the following core files:
1. `Makefile`: The top-level driver for GNU Make.
2. `cpsa4.mk`: Standard target definitions linking `.scm` source files to `.txt`, `_shapes.txt`, and `.xhtml` outputs.
3. `Make4.hs`: A Haskell implementation of the build driver.
4. `cpsa4prolog.pl`: Prolog bridge for exporting strand space graphs.

### 2.2 Standard Build Pipeline (§2.2)
```
[ protocol.scm ] 
      │
      ▼  (cpsa4)
 [ protocol.txt ]  ─── Full intermediate search tree (all steps)
      │
      ├────────────────────────┐
      ▼ (cpsa4shapes)          ▼ (cpsa4graph)
[ protocol_shapes.txt ]   [ protocol.xhtml ] ── Interactive SVG graph
      │
      ▼ (cpsa4graph)
[ protocol_shapes.xhtml ]
```
* `make`: Compiles all `.scm` files into `.txt` and `.xhtml`.
* `make clean`: Cleans generated `.txt`, `_shapes.txt`, and `.xhtml` artifacts.

### 2.3 Haskell GHC Runtime System Flags (§2.3)
To safeguard CPSA against memory thrashing or to leverage multithreading on multicore CPUs:
```bash
cpsa4 +RTS -M512m -N4 -RTS -o output.txt input.scm
```
* `+RTS -M<size> -RTS`: Sets maximum heap size limit (e.g. `-M512m`, `-M4g`). If CPSA exhausts this memory, it aborts gracefully with a clean backtrace rather than locking the operating system.
* `+RTS -N<cores> -RTS`: Enables parallel search across $N$ CPU cores.

---

## Chapter 3: Basic Use of CPSA (`basic.tex`)

### 3.1 Anatomy of a Protocol Definition (§3.1)
A protocol is declared with `defprotocol`, specifying the protocol name, the underlying algebra (`basic` or `diffie-hellman`), and one or more roles (`defrole`):
```lisp
(herald "Needham-Schroeder" (algebra basic))

(defprotocol ns basic
  (defrole init
    (vars (a b name) (na nb text))
    (trace
      (send (enc na a (pubk b)))
      (recv (enc na nb (pubk a)))
      (send (enc nb (pubk b)))))

  (defrole resp
    (vars (a b name) (na nb text))
    (trace
      (recv (enc na a (pubk b)))
      (send (enc na nb (pubk a)))
      (recv (enc nb (pubk b))))))
```

### 3.2 Anatomy of a Skeleton Query (Point of View) (§3.2)
A `defskeleton` specifies the scenario from a specific participant's point of view:
```lisp
(defskeleton ns
  (vars (a b name) (na nb text))
  (defstrandmax init (a a) (b b) (na na) (nb nb))
  (non-orig (privk a) (privk b))
  (uniq-orig na)
  (comment "Initiator point of view"))
```
* `defstrandmax`: Instantiates a role to its full maximum height automatically.
* `defstrand`: Instantiates a role up to a specific step index: `(defstrand role height maplets...)`.
* `maplet`: Maps role variables to skeleton variables: `(role_var skel_var)`.

### 3.3 Visualizing Graphs (`cpsa4graph`) (§3.3)
Generated `.xhtml` files render interactive SVG diagrams with color-coded nodes:
* **Red Nodes**: Unrealized reception events (unexplained transmissions requiring authentication tests).
* **Blue Nodes**: Realized reception events (explained by an earlier transmission).
* **Black Nodes**: Message transmission events (`send`).
* **Orange Nodes**: State write events (`stor`).
* **Cyan Nodes**: State read events (`load`).
* **Solid Arrows**: Intra-strand causal succession (local chronological order).
* **Dashed / Dotted Arrows**: Inter-strand message transmission or causal precedence (`prec`).

### 3.4 Proving Secrecy via Listeners (`deflistener`) (§3.4)
To formally verify whether a secret value $K$ remains confidential:
```lisp
(defskeleton ns
  (vars (a b name) (na nb text))
  (defstrandmax init (a a) (b b) (na na) (nb nb))
  (deflistener na)
  (non-orig (privk a) (privk b))
  (uniq-orig na)
  (comment "Secrecy query for initiator nonce"))
```
* **Proof Interpretation**: If CPSA terminates with `(dead)` or `(comment "Not a skeleton")` and **0 shapes**, the listener strand cannot be realized. This is the **formal mathematical proof of secrecy**.

---

## Chapter 4: Cryptographic Algebra (`algebra.tex` & `input.tex`)

### 4.1 Sort Hierarchy (Order-Sorted Algebra) (§4.1)
Every variable declared in `(vars ...)` belongs to a sort within the order-sorted hierarchy:

```
                      mesg
     ┌───────┬───────┬──┴────┬───────┬───────┬───────┬───────┐
    name    text    data    tag    skey    akey    expt    chan
                                                    │       │
                                                   rndx    locn
                                                            │
                                                           dev
```

* `name`: Principals, identities, network addresses.
* `text`: Nonces, challenges, plaintext messages, timestamps.
* `data`: Payloads, cookies, opaque byte streams.
* `tag`: String literal tags used for message disambiguation (`"client-hello"`).
* `skey`: Symmetric encryption keys and HMAC keys.
* `akey`: Asymmetric public/private key pairs.
* `rndx`: **Fresh random Diffie-Hellman private exponents** (subtype of `expt`).
* `expt`: Arbitrary algebraic exponent expressions.
* `chan`: Communication channels (used with `auth` and `conf`).
* `locn`: Memory cells / hardware register locations (used with `load` and `stor`).
* `dev`: Device identifiers.
* `mesg`: Root sort of all transferable messages.

> [!CAUTION]
> **Sort `base` Deprecation (CPSA 4.4.8+)**:
> Declaring `(vars (x base))` aborts with `mkVar: Variables of sort base are now deprecated`.
> To represent public Diffie-Hellman values, write `(exp (gen) x)` directly in message terms, where `x` is declared `rndx`.

### 4.2 Cryptographic Function Symbols (§4.2)
* `(enc term1 term2 ... key)`: Keyed encryption.
  * If `key` is sort `skey` $	o$ Symmetric encryption.
  * If `key` is `(pubk a)` $	o$ Asymmetric public-key encryption.
  * If `key` is `(privk a)` $	o$ Asymmetric digital signature.
* `(hash term1 term2 ...)`: Cryptographic one-way hash / digest.
* `(cat term1 term2 ...)`: Explicit concatenation / grouping.
* `(pubk principal)`: Public key of principal ($K_a$). Sub-key variant: `(pubk "tag" principal)`.
* `(privk principal)`: Private key of principal ($K_a^{-1}$). Sub-key variant: `(privk "tag" principal)`.
* `(invk key)`: Algebraic inverse of an asymmetric key (`invk (pubk a) = privk a`).
* `(ltk a b)`: Directional long-term shared symmetric key (`ltk(a,b) != ltk(b,a)`).
* `(bltk a b)`: Bidirectional long-term shared symmetric key (`bltk(a,b) = bltk(b,a)`).

### 4.3 Diffie-Hellman Algebra (§4.3)
* `(exp base exponent)`: Modular / DH exponentiation ($g^{xy}$).
* `(gen)`: The constant generator $g$ for Diffie-Hellman.
* `(one)`: Multiplicative identity $1$ for exponents.
* `(mul exp1 exp2 ...)`: Exponent multiplication ($x \cdot y$).
* `(rec exponent)`: Exponent multiplicative inverse ($x^{-1}$).
* **Syntactic Exponent Rules**:
  - `rndx` variables **must first occur in an outbound transmission** (`send`).
  - Generic `expt` variables **must first occur in an inbound reception** (`recv`).
  - Bare exponents outside an `exp` term are disallowed unless typed `rndx`.

### 4.4 Custom Algebra Extensions (`(lang ...)`) (§4.4)
Custom sorts and constructors can be defined in a protocol's association list:
```lisp
(defprotocol custom-p basic
  ...
  (lang
    (my_atom atom)
    (my_tuple (tuple 3))
    (my_hash hash)
    (my_enc enc)))
```
* `atom`: Declares an atomic sort eligible for `non-orig` or `uniq-orig`.
* `tuple`: Publicly constructible and invertible tuple (like `cat`).
* `hash`: Opaque one-way function.
* `enc`: Keyed encryption function.

---

## Chapter 5: The CPSA Algorithm (§5)

### 5.1 Cohorts & Search Trees (§5.1)
The analyzer operates by iterative cohort reduction:
1. It selects an unrealized node from the skeleton.
2. It identifies the critical term within the node's received message.
3. It computes the **cohort**: all minimal ways to resolve the critical term.
4. Each child skeleton is queued for subsequent exploration.

### 5.2 The Four Solving Operations (§5.2)
1. **Regular Augmentation**: Adding a new strand of an existing protocol role whose transmission could supply the critical term.
2. **Displacement**: Unifying the needed transmission with an existing strand already in the skeleton.
3. **Contraction**: Applying a variable substitution that unifies message terms or keys.
4. **Listener Augmentation**: Inverting or decrypting a term by querying whether the decryption key is derivable.

### 5.3 Pruning & Isomorphism Checks (§5.3)
* **Homomorphic Subsumption**: If skeleton $S_1$ can be mapped into skeleton $S_2$ preserving all structure and orderings, $S_2$ is redundant and pruned.
* **Seen Children (`seen-ops`)**: Skeletons identical to previously visited nodes are linked rather than re-explored.

---

## Chapter 6: Declarations & Assumptions (`declarations.tex`)

### 6.1 The Four Origination & Freshness Declarations (§6.1)

| Declaration | Goal Predicate | Definition | Usage Context |
|---|---|---|---|
| `non-orig` | `non` | **Carried nowhere** in any bundle. Never emitted by any honest or penetrator strand. | Long-term private keys (`privk`), shared symmetric LTKs (`ltk`). |
| `pen-non-orig` | `pnon` | Carried on regular strands, but **never originated by penetrator**. | Transported session keys, Kerberos tickets, hashed shared secrets. |
| `uniq-orig` | `uniq` | Originates uniquely at **exactly one carried transmission** node. | Fresh nonces, random challenges, freshly generated session keys. |
| `uniq-gen` | `ugen` | Generated uniquely at **exactly one transmission node, whether carried or not**. | Diffie-Hellman private exponents (`rndx`), uncarried sequence numbers. |

> [!IMPORTANT]
> **Carried vs Uncarried Terms**:
> A subterm $t$ is *carried* in $m$ if $t$ can be extracted from $m$ without decrypting using unknown keys.
> - In `(enc (cat k n) k2)`, $k$ and $n$ are carried.
> - In `(exp (gen) x)`, the exponent $x$ is **NOT carried**!
> - In `(hash x)`, $x$ is **NOT carried**!
> - Therefore: DH exponents must use **`uniq-gen`**, NEVER `uniq-orig`!
> - Shared secrets emitted inside hashes must use **`pen-non-orig`**, NEVER `non-orig`!

### 6.2 Relational & Inequality Constraints (§6.2)
* `(absent (rndx_var expt_term))`: Asserts that an exponent does not occur algebraically within another term.
* `(neq (term1 term2) ...)` / `(facts (neq var1 var2))`: Asserts that two variables cannot unify (e.g. preventing identity reflection $A 
e B$).
* `(priority ((strand node) integer))`: Adjusts search order priority for specific nodes (0 = never solve, 5 = default, 10 = high priority).

### 6.3 Placement Rule: Skeletons vs Roles (§6.3)
* **In `defrole`**: Assumptions apply globally to *every* instance of that role across all sessions. This over-constrains the model and prevents analyzing key compromise scenarios.
* **In `defskeleton`**: Assumptions apply strictly to the scenario under test.
* **Best Practice**: Keep `defrole` completely free of assumptions; pack all `non-orig`, `pen-non-orig`, `uniq-orig`, and `uniq-gen` into `defskeleton`.

---

## Chapter 7: Security Goals & Rules (`goals.tex`)

### 7.1 First-Order Geometric Logic (`defgoal`) (§7.1)
CPSA allows formalizing security guarantees as first-order sentences:
```lisp
(defgoal ns
  (forall ((init_s strd) (a b name) (na text))
    (implies
      (and (p "init" init_s 3)
           (p "init" "a" init_s a)
           (p "init" "b" init_s b)
           (p "init" "na" init_s na)
           (non (privk a)) (non (privk b))
           (uniq na))
      (exists ((resp_s strd) (nb text))
        (and (p "resp" resp_s 2)
             (p "resp" "a" resp_s a)
             (p "resp" "b" resp_s b)
             (p "resp" "na" resp_s na)
             (prec init_s 0 resp_s 0)
             (prec resp_s 1 init_s 1))))))
```

### 7.2 Goal Predicate Reference (§7.2)
* `(p "role" strand_var height)`: Strand has executed at least `height` events.
* `(p "role" "param_name" strand_var term)`: Parameter binding for `param_name`.
* `(prec s1 i1 s2 i2)`: Node `(s1, i1)` causally precedes node `(s2, i2)`.
* `(non term)`: Non-origination assumption.
* `(pnon term)`: Penetrator non-origination assumption.
* `(uniq term)`: Unique origination assumption.
* `(ugen term)`: Unique generation assumption.
* `(listener strand_var term)`: Strand is a listener observing `term`.
* `(= term1 term2)`: Term equality (conclusion only).
* `(false)`: Disproves scenario (used for secrecy goals: `(and (listener s k) ...) => (false)`).

### 7.3 Rules & Lemmas (`defrule`, `deflemma`) (§7.3)
* `(defrule name sentence alist)`: User-defined inference rule evaluated during cohort expansion.
* `(deflemma check id proto sentence alist)`: Intermediate lemma. Flag `check` can be `rule`, `goal`, or `both`.
* `rely` / `guarantee`: Step-by-step trust management annotations.

---

## Chapter 8: Channels and State (`channels_state.tex`)

### 8.1 Secure Channels (§8.1)
Communication can occur over abstract channels with intrinsic security guarantees:
```lisp
(vars (ch chan))
(send ch msg)
(recv ch msg)
(auth ch)  ;; Guarantees authenticity: recipient knows msg came from regular strand
(conf ch)  ;; Guarantees confidentiality: adversary cannot intercept msg
```

### 8.2 Stateful Protocols & Mutable Memory Cells (§8.2)
* Sort: `locn` (storage register).
* Events:
  - `(load locn term)`: Read value from location.
  - `(stor locn term)`: Write value to location.
* `(gen-st term)`: Declares that a stored state value is non-initial (*generated state value*). A `load` of a generated state value acts like an authenticated reception.

### 8.3 State Axioms & Consequences (§8.3)
1. **Discrete-After Axiom**: A state transition step is discrete: transitions following a write are weakly ordered.
2. **Discrete-Before Axiom**: Transitions preceding a read are weakly ordered.
3. **Scissors Rule**: A single state event leads to at most one subsequent transition event ($m_0 = m_1$).
4. **No Interruption Rule**: A transition cannot be inserted between a state event and its direct successor.
5. **Cake Rule**: You cannot observe an old state value after a state transition has already overwritten it.

> [!WARNING]
> **The Non-Termination State Trap (§8.4)**:
> Declaring `gen-st` on an initial-only state value while transitions produce unbounded sequences of intermediate values generates infinite shapes with no homomorphisms between them. Ensure `gen-st` is applied only to non-initial values that bound the state history.

---

## Chapter 9: Troubleshooting & Error Reference (`troubleshooting.tex`)

### 9.1 Non-Termination Bail-outs & Search Flags (§9.1)

| Option | Flag | Default | Description |
|---|---|---|---|
| `bound` | `-b INT` | 12 | Aborts if any skeleton exceeds $N$ strands. |
| `limit` | `-l INT` | 2000 | Aborts if skeleton analysis count exceeds $N$ steps. |
| `depth` | `-d INT` | $\infty$ | Skeletons beyond depth $N$ are marked `(fringe)` without error. |
| `goals-sat` | `-g` | Off | Prunes search branches once the security goal is satisfied. |
| `try-old-strands` | `-t` | Off | Prioritizes leftmost strands over rightmost strands. |
| `reverse-nodes` | `-r` | Off | Prioritizes youngest nodes on a strand over oldest nodes. |
| `check-nonces` | `-c` | Off | Prioritizes nonces over encryptions when selecting critical terms. |

### 9.2 Complete Error Message Index & Solutions (§9.2)

* **`Bad char in string`**: A quote-delimited string contains an unescaped newline or illegal character. Keep all strings and `(comment "...")` on a single physical line.
* **`Close of unopened list`**: Erroneous closing parenthesis `)`.
* **`Unexpected end of input in list`**: Missing closing parenthesis `)`. Run `check_parens.py --fix`.
* **`cpsa4graph: Empty input`**: Skeletons were omitted or accidentally nested inside `(defprotocol ...)`. Close `defprotocol` first; `defskeleton` must be a top-level sibling!
* **`Disallowed bare exponent`**: An exponent variable appears outside `exp` without sort `rndx`.
* **`Domain does not match range`**: Parameter type mismatch in `defstrand` maplets (e.g. mapping `name` to `text`).
* **`Duplicate variable declaration for [...]`**: A variable name is declared more than once in `(vars ...)`.
* **`Expts must first be received, rndxs first sent`**: An `expt` variable appeared first in a `send`, or an `rndx` variable appeared first in a `recv`.
* **`Identifier [...] unknown`**: Variable referenced in trace or maplet was not declared in the local `(vars ...)` block.
* **`Keyword [...] unknown`**: A term list omitted its function constructor (e.g. `(send (a b))` instead of `(send (cat a b))`).
* **`Role not well formed: non-orig [...] carried`**: A key declared `non-orig` is emitted in the clear or inside a carried position. Change to `pen-non-orig`.
* **`Role not well formed: uniq-orig [...] doesn't originate`**: Declared `uniq-orig` on a term whose first appearance is in a `recv` or uncarried position (such as a DH exponent). Use `uniq-gen` for DH exponents.
* **`Role not well formed: variable [...] not acquired`**: A variable of sort `mesg` first appeared in a transmission without being acquired in a previous reception.
* **`Skeleton not well formed: cycle found in ordered pairs`**: Contradictory `precedes` declarations created a causal time-travel loop.

---

## Chapter 10: Formal BNF Grammar (`input.tex`)

### 10.1 Complete Grammar Summary (§10.2)
```bnf
<file>         ::= [<herald>] <form>+
<herald>       ::= "(" "herald" (<symbol> | <string>) <alist> ")"
<form>         ::= <comment> | <protocol> | <skeleton> | <goal> | <lemma>
<comment>      ::= "(" "comment" <any>* ")"

<protocol>     ::= "(" "defprotocol" <id> <alg> <role>+ <rule>* <prot-alist> ")"
<alg>          ::= "basic" | "diffie-hellman"

<role>         ::= "(" "defrole" <id> <vars> <trace> <role-alist> ")"
<vars>         ::= "(" "vars" <vdecl>* ")"
<vdecl>        ::= "(" <id>+ <sort> ")"
<trace>        ::= "(" "trace" <event>+ ")"
<event>        ::= "(" <dir> [<term>] <term> ")"
<dir>          ::= "send" | "recv" | "load" | "stor"

<skeleton>     ::= "(" "defskeleton" <id> <vars> <strand>+ <skel-alist> ")"
<strand>       ::= "(" "defstrand" <id> <integer> <maplet>* ")"
                 | "(" "defstrandmax" <id> [<integer>] <maplet>* ")"
                 | "(" "deflistener" <term> ")"
<maplet>       ::= "(" <term> <term> ")"

<goal>         ::= "(" "defgoal" <id> <sentence>+ <alist> ")"
<lemma>        ::= "(" "deflemma" ("rule" | "goal" | "both") <id> <id> <sentence> <alist> ")"
```

### 10.2 Preprocessor Directives (§10.1)
* `(include "filename.scm")`: Textual file inclusion (relative paths only).
* `(defmacro (name arg1 arg2) expansion)`: Positional macro expansion.
* `(^ event1 event2 ...)`: Macro splicing (allows a macro to expand into multiple trace events).

---

## Chapter 11: Tool Ecosystem (`tools.tex`)

* **`cpsa4`**: Core shape analysis solver.
* **`cpsa4init`**: Creates standard project structure and Makefile.
* **`cpsa4shapes`**: Strips intermediate skeletons from output, retaining only solved shapes.
* **`cpsa4graph`**: Generates interactive XHTML diagrams featuring SVG strand graphs.
* **`cpsa4goalsat`**: Evaluates `defgoal` formulas against analysis output, returning unsatisfied skeleton IDs.
* **`cpsa4prot`**: Converts intuitive Alice-and-Bob notation (`(msg A B M)`) into full `defprotocol` forms.
* **`cpsa4sas`**: Extracts Shape Analysis Sentences (first-order logic theorems proved by the run).
* **`cpsa4pp`**: Scheme pretty-printer and JSON converter.
* **`cpsa4json`**: Translates JSON representations back into CPSA S-expressions.
* **`cpsa42latex`**: Typesets CPSA macro definitions into publication-ready LaTeX.
* **`cpsa4diff`**: Performs semantic structural comparison between skeletons in two output files.

---

## Primer Wisdom & Expert Modeling Guidance (`cpsaprimer.tex`)

1. **Sort `text` vs Sort `data` (§12)**:
   - Use `data` for uniquely originating secrets, random cookies, and fresh parameters that must never unify with predictable protocol fields.
   - Use `text` for unconstrained fields, general payloads, and plain messages.
2. **Progressive Refinement Analysis (§12)**:
   - Begin analysis with minimal assumptions. Inspect unexpected intermediate skeletons to reveal missing authenticity assumptions or design flaws.
3. **Interpreting Primed Variables (`x-0`, `x-1`)**:
   - If a shape contains `x` on one strand and `x-0` on another, the parties **failed to achieve agreement** on that parameter! This commonly happens when a cleartext field sits adjacent to an encrypted block without being integrity-bound.
