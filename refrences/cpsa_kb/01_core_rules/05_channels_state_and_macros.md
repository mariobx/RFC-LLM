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
