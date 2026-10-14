# State: load, stor, gen-st

## What state is for

Exactly one thing nothing else can do: **link two strands on the same device
when no message passes between them.** If two procedures run as separate roles
and the only connection is a database record, state is the only channel.

## What it is not for

If both procedures live in one long role, trace order already enforces sequence
and shared variables already enforce agreement. State there is decorative.

## The non-termination trap

CPSA manual §8.2.4: when a specification distinguishes a kind of value that can
only appear in an initial load, and transitions produce different values, a run
can have 0, 1, 2, … n transitions with **no homomorphisms between them** — so
there are infinitely many shapes and cpsa will not terminate, though partial
output is often informative. The manual says the craft of using cpsa with state
is largely restricting `gen-st` so it does not distinguish state histories of
irrelevantly different lengths.

The pattern that triggers it: `gen-st` on an initial-only value, with
transitions producing values that are not themselves declared.

## When a load actually does work

A `load` earns its place only if one of these holds:

1. **Another strand could have written that location** — then the write explains
   the read, and `gen-st` can be dropped from that role.
2. **A second strand competes for the same location** — the scissors rule (a
   state node leads to at most one transition node) then rules out concurrent
   transitions, giving idempotence for free.
3. **A goal asks about state** — via `gen-st`, `trans`, `same-locn`,
   `state-node`.

If none holds, the `load`/`stor` pair is documentation with no analytical
consequence. That is a legitimate choice, but say so rather than implying the
precondition was verified.

## Syntax

```lisp
(defrole device
  (vars (k skey) (loc locn))
  (trace
    (load loc (record k "state-a"))
    (stor loc (record k "state-b"))
    (send (msg k)))
  (gen-st (record k "state-a")))
```

Give locations names that identify the registry (`ground_key_db`, not `lk`) —
with two registries in one role, the names are what make the two state machines
distinguishable on sight. `(facts (same-dev loc1 loc2))` ties two locations to
one device; needed only when one role touches more than one.

## The honest disclosure

Dropping state means preconditions are **assumed by construction rather than
verified**. Name the clauses this affects. That sentence is short, true, and
much better than a reader assuming they were checked.
