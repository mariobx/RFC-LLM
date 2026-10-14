# Reading CPSA output

## Per-skeleton markers

| Marker | Meaning |
|---|---|
| `(realized)` | Every reception is explained. |
| `(shape)` | A minimal essentially different execution. This is the result. |
| `(dead)` with `empty cohort` | No execution exists. For a listener-based secrecy goal, this is secrecy holding. |
| `(unrealized (s n) ...)` | Node `n` of strand `s` is not yet explained. |
| `(preskeleton)` "Not a skeleton" | Needs conversion; not by itself a failure — check whether the tree yields children. |
| `(fringe)` | Not analysed because of the `depth` limit. |
| `(aborted)` | Step limit hit. **The analysis is incomplete — do not report its shapes as complete.** |

## The verdict line

- `(satisfies yes)` — goal holds in this shape.
- `(satisfies (no CONJUNCT bindings...))` — the named conjunct is the one that
  failed. Read it: it tells you exactly which agreement is missing, which is far
  more informative than "the goal failed."

## Primed variables are the finding

When a shape shows `x` on one strand and `x-0` on another, those are different
values. The two strands disagree on that parameter.

This most often means a **cleartext field sat beside a protected one**. The
encryption test forces the encrypted component to come from a legitimate strand,
but an adjacent plaintext field can be stripped and replaced in transit. Before
"fixing" the model, check the specification: if the field genuinely travels
outside the integrity-protected region, the disagreement is a real property of
the protocol and is worth reporting.

A shape with **no primed variables at all** is full agreement on every parameter
— frequently stronger than the goal asked for, and worth stating.

## The operation line

`(operation encryption-test (added-strand ROLE N) TERM (s n))` shows how CPSA
explained node `(s n)`: it added a strand of `ROLE` to produce `TERM`.
`(displaced ...)` means it unified with an existing strand instead. Reading these
tells you *why* a shape looks the way it does.

## Diagnosing a large or stuck run

Count these before changing anything:

```
grep -c "defskeleton" out.txt      # skeletons explored
grep -c "(realized)"  out.txt      # how many closed
grep -c "(dead)"      out.txt
grep -o "(operation [a-z-]*" out.txt | sort | uniq -c | sort -rn
grep -o "VAR-[0-9]*" out.txt | sed 's/-[0-9]*$//' | sort | uniq -c | sort -rn
```

Many skeletons and few realized means branching without converging. The primed-
variable histogram names the variables driving it — the top entries are where
CPSA is manufacturing strands, and usually point at the term to simplify.
