# Termination, limits, and heap

## Herald options

```lisp
(herald "name"
  (limit 2000)          ; step limit: skeletons processed before aborting. Default 2000.
  (bound 12)            ; strand bound. Default 12.
  (depth 8)             ; max steps from the point of view. No default.
  (goals-sat)           ; stop descending where goals are already satisfied
  (try-old-strands)     ; leftmost unrealized strand first
  (check-nonces)        ; smallest critical term first
  (reverse-nodes))      ; youngest node in a strand first
```

## Which bound to reach for

- **`bound`** limits the modelled world — how many concurrent strands exist.
  "We verified all executions involving at most N regular strands" is a standard,
  defensible claim. Errors with "Strand bound exceeded" rather than degrading.
- **`goals-sat`** is semantic pruning: branches where the goal already holds are
  not pursued, so the run asks *how could this goal fail*. Principled, and often
  a large saving.
- **`depth`** cuts at an arbitrary distance from the point of view and has no
  protocol meaning. It never errors — unanalysed skeletons are marked `(fringe)`
  — which makes it useful for diagnosis but weak as a published bound.
- **`limit`** is a step cap. Raising it does not "explore more of the space" in
  any complete sense; it retains more skeletons and makes heap exhaustion more
  likely. An `(aborted)` result is as much a cutoff as a `depth` result.

There is no unbounded mode. Every run is bounded; choose a bound you can defend
in writing.

## Search-order flags

The manual states that each helps some analyses and hurts others, and that some
analyses terminate **only** with a given option. Test them **individually** first
— a combination can be worse than either alone. Three flags give eight
combinations; scripting the sweep is cheap and each run is informative.

## Heap

`cpsa4 +RTS -M4g -N -RTS -o out.txt model.scm`. The default in many makefiles is
512 MB, which is small for anything with several encrypted components per role.

## Structural causes, in order of impact

1. **State with `gen-st`** — see `state.md`. This causes genuine non-termination,
   not slowness. Suspect it first.
2. **Split keys.** One key in the `enc` position and a different key in the
   `hash` position lets CPSA pair encryption from one strand with authentication
   from another. Using a single key for both collapses that branch entirely. If
   the cipher suite is a combined single-key AEAD, one key is also the more
   faithful model.
3. **Unconstrained passenger variables.** A `text` variable appearing in every
   message but in no goal contributes only search cost.
4. **Long roles.** Cost grows with encrypted components, which is roughly
   messages times layers. Cut backwards to find where it breaks: delete later
   steps, confirm the prefix terminates, add back one at a time.

## Reporting a run that will not converge

"The authenticated-encryption variant exceeded practical search limits while the
authentication-only variant terminated" is a legitimate observation about
analysis cost. Report it as that. Do not present shapes from an `(aborted)` run
as a completed analysis.
