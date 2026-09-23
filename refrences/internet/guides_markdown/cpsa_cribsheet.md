# CPSA Official Quick Reference & Syntax Cribsheet

## 1. Top-Level Forms and Execution Limits
CPSA analysis inputs are structured as S-expressions.
```scheme
(herald "Protocol Title"
  (limit 200)               ;; Maximum number of skeletons to analyze
  (bound 10)                ;; Maximum number of strands in a skeleton
  ;; (algebra diffie-hellman) ;; Include when using Diffie-Hellman algebra
)
```

## 2. Basic Cryptoalgebra
### Sorts / Types:
- Base atomic sorts: `text`, `data`, `name`, `skey`, `akey`, `tag` (all subsorts of `mesg`)
- Compound message sort: `mesg`
- Invariants:
  - Cannot use a variable of sort `mesg` as the key in an encryption.
  - Variables of sort `mesg` must be acquired (received before sent).

### Functions and Operators:
- `pubk`: `name -> akey` (Public key of principal)
- `privk`: `name -> akey` (Private key of principal)
- `invk`: `akey -> akey` (Inverse of asymmetric key)
- `ltk`: `name x name -> skey` (Long-term symmetric key shared between principals)
- `cat`: `mesg x mesg -> mesg` (Concatenation / pairing)
- `enc`: `mesg x mesg -> mesg` (Encryption; symmetric or asymmetric depending on key sort)
- `hash`: `mesg -> mesg` (One-way cryptographic hash)

## 3. Diffie-Hellman Cryptoalgebra
### Additional Sorts / Types:
- `rndx` < `expt` < `mesg` (Random exponents and general exponents)
- `base` < `mesg` (Diffie-Hellman group elements)

### Additional Functions:
- `gen`: `() -> base` (Generator of the Diffie-Hellman group)
- `exp`: `base x expt -> base` (Exponentiation $g^x$)
- `one`: `() -> expt` (Multiplicative identity exponent 1)
- `rec`: `expt -> expt` (Reciprocal exponent $x^{-1}$)
- `mul`: `expt x expt -> expt` (Multiplication of exponents in $\mathbb{Z}_q$)
- `bltk`: `name x name -> skey` (Bidirectional long-term key)
- Invariant: Variables of sort `expt` must be acquired (received before sent).

## 4. Origination and Variable Declarations (Atoms Only)
- `(non-orig x)`: $x$ is secret and uncompromised (never carried by any network transmission).
- `(uniq-orig x)`: $x$ is fresh and uniquely originates at the first event where it is carried.
- `(uniq-gen x)`: $x$ is freshly generated at the first point where it appears (even if not carried, e.g. state or DH exponent).
- `(pen-non-orig x)`: Penetration non-originating; $x$ is secret unless explicitly exposed.

## 5. Equality and Algebraic Constraints
- `(neq (x y))`: Inequality constraint ($x \neq y$).
- `(eq (x y))`: Equality constraint ($x = y$).
- `(fn-of (function (x y)))`: Functional dependency ($x = f(y)$).

## 6. Rule and Goal Atomic Formulae
- `(p "role" z 2)`: Strand $z$ executes role "role" through index 2 (height 3).
- `(p "role" "v" z v)`: Strand parameter $v$ in strand $z$ is bound to value $v$.
- `(non a)`: Term $a$ satisfies non-originating assumption.
- `(pnon a)`: Term $a$ satisfies penetrator non-originating assumption.
- `(uniq a)`: Term $a$ satisfies unique origination assumption.
- `(uniq-at a z 2)`: Term $a$ uniquely originates at node $(z, 2)$.
- `(= v1 v2)`: Equality predicate.
- `(prec z0 2 z1 3)`: Precedence relation; event $(z_0, 2)$ happens before $(z_1, 3)$.
- `(leads-to z0 2 z1 3)`: Leads-to relation across state nodes.
- `(fact pred params)`: User-defined state relation or relational fact.

## 7. Rule and Goal First-Order Logic Grammar
```
SENTENCE     <- (forall (GVDECL*) IMPLICATION)
GVDECL       <- (ID+ SORT) | (ID+ strd)
IMPLICATION  <- (implies CONJUNCTION CONCLUSION)
CONJUNCTION  <- ATOMIC | (and ATOMIC*)
CONCLUSION   <- (false) | EXISTENTIAL | (or EXISTENTIAL*)
EXISTENTIAL  <- CONJUNCTION | (exists (GVDECL*) CONJUNCTION)
```

## 8. Output Interpretation and Visualization
- Shapes: Minimal, fully realized protocol executions satisfying the point of view.
- Realized Skeleton: A skeleton in which every receive event is explained by a prior send event or initial knowledge.
- Dead Skeleton: An unrealizable partial execution branch pruned by the search algorithm.
- Event Nodes:
  - `(send m)`: Message transmission event.
  - `(recv m)`: Message reception event.
  - `(load s v)`: State observation/load from state cell $s$.
  - `(stor s v)`: State transition/store to state cell $s$.
