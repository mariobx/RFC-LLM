# Goals and skeletons

## Skeletons — a point of view

```lisp
(defskeleton my-protocol
  (vars (k skey) (a b name))
  (defstrandmax satellite (k k) (a a) (b b))
  (non-orig k))
```

- `defstrandmax role maplet...` — no height field, includes the role's full trace.
- `defstrand role <INT> maplet...` — height `INT` IS REQUIRED; it must satisfy `1 <= INT <= length(role-trace)` or CPSA fails `Bad height` before any further analysis. Use it to model a *prefix* of the role (partial execution, e.g., the responder's point of view after only 2 of 4 events).
- **Arity trap**: `defstrand` and `defstrandmax` are DIFFERENT keywords with DIFFERENT arities. Substituting one for the other, or dropping the height from `(defstrand role N env...)`, produces the misleading error `Malformed defstrand` from `cpsa/src/CPSA/Loader.hs:loadInsts`. That error most often indicates a paren-imbalance EARLIER in the file (the `SExpr` parser fed `loadInsts` a malformed slist), not a typo on the `defstrand` line. Run a full-file paren-depth scan before touching the skeleton (see SKILL.md R4).
- **Maplets may only name parameters that appear in the role's trace.** A
  variable declared in `vars` but never sent or received is not a parameter;
  naming it errors with "Identifier X unknown." This is the most common cause
  of that error — check it first before suspecting parens or missing decls.
- **`defstrandmax` is strictly a list of `(var var)` maplets.** A bare term
  (e.g. `(cat "m" a b c)`) is not a legal maplet → `Malformed maplet`. Use
  `defstrand role <h> ...` for prefix bindings that need term patterns, or a
  `defgoal` for richer queries. A same-name maplet (`(x x)`) is the only
  form that is always safe against both errors.

## Goals — the documented predicate syntax

```lisp
(defgoal my-protocol
  (forall ((responder strd) (k skey) (n text))
    (implies
      (and (p "satellite" responder 2)
           (p "satellite" "sessionkey" responder k)
           (p "satellite" "chal" responder n)
           (non k) (uniq n))
      (exists ((initiator strd))
        (and (p "ground" initiator 2)
             (p "ground" "sessionkey" initiator k)
             (p "ground" "chal" initiator n))))))
```

- `(p "role" strandvar length)` — a strand of that role has run at least `length`
  events.
- `(p "role" "param" strandvar value)` — binds that strand's parameter. The
  parameter string must match the role's `vars` name **exactly**; a mismatch
  binds nothing and the goal silently means something else.
- Every variable in the quantifier must appear in the body, or CPSA errors.
- Available predicates include `non`, `pnon`, `uniq`, `ugen`, `uniq-at`,
  `ugen-at`, `listener`, `gen-st`, `trans`, `same-locn`, `component`, `fact`.

## Secrecy goals

Put a `listener` on the secret and conclude `(false)`:

```lisp
(and ... (uniq k) (listener eve k)) => (false)
```

If the resulting tree terminates with no realized skeleton — typically `(dead)`
with `empty cohort` — no execution puts the secret in the adversary's hands.

## What an authentication goal does *not* say

An `exists` conclusion permits one initiator strand to satisfy many responder
strands. That is replay, and it is allowed unless you add more:

- **Injectivity** — needs a stronger conclusion tying the two strands.
- **Ordering** — add `(prec initiatorstrand i responderstrand j)`.
- **Principal identity** — only if the roles actually carry `name` variables.
- **Full agreement** — each parameter you care about must be named in the
  conclusion; unnamed ones are unconstrained even if they happen to unify.

Say precisely what the goal establishes. "The recipient's binding originates at
an initiator" is not "the recipient received this exactly once from the intended
sender."
