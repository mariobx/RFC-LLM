# Origination and Freshness Declarations

## The Four Fundamental Declarations

| Declaration | Goal Predicate | Definition | Usage Context |
|-------------|----------------|------------|---------------|
| `non-orig` | `non` | Originates on **no** strand (honest or penetrator). The value is carried in no message in the entire bundle. | Long-term private keys (`(privk A)`), un-emitted shared LTKs (`(ltk A B)`). |
| `pen-non-orig` | `pnon` | Originates on no **penetrator** strand. Regular strands may originate/transmit it. | Keys transported in messages, Kerberos tickets, shared secrets hashed in replies. |
| `uniq-orig` | `uniq` | Originates at exactly one node, and appears in a **carried** message position there. | Freshly generated nonces, challenges, random session keys. |
| `uniq-gen` | `ugen` | Generated uniquely at exactly one node, **whether carried or not**. | Diffie-Hellman private exponents (`rndx`), uncarried sequence numbers. |

In goal formulas the corresponding predicates are `non`, `pnon`, `uniq`, `ugen`.

---

## Critical Rules for Choosing Declarations

1. **A pre-shared long-term key that no procedure transmits** $	o$ `non-orig`.  
   Example: `(non-orig (privk server_id) (privk client_id))`
2. **A key or secret delivered or emitted inside a message** $	o$ `pen-non-orig`.  
   `non-orig` here is contradictory: because the key is carried in a message (even inside a hash or ciphertext), declaring `non-orig` voids the bundle and prevents shape realization. Use `pen-non-orig`!
3. **A freshly generated nonce, challenge, or session key** $	o$ `uniq-orig`.
4. **Diffie-Hellman random private exponents (`rndx`)** $	o$ **`uniq-gen`**!  
   In modular exponentiation `(exp (gen) x)`, the exponent $x$ is in an **uncarried** algebraic position. If you declare `(uniq-orig x)`, CPSA fails with `uniq-orig doesn't originate`. Always declare `(uniq-gen x)` for `rndx` variables!
5. **Compatibility**: `uniq-orig` and `pen-non-orig` on the same value are not in conflict: one constrains *where* it originates (freshness), the other constrains *who* originates it (adversary cannot forge it).

---

## Where to Put Declarations: Skeletons vs Roles

> [!IMPORTANT]
> **Always prefer placing declarations in `defskeleton` rather than `defrole`.**
> - A declaration inside a `defrole` applies globally to *every* strand of that role in every analysis, which makes it impossible to ask what happens when that key is compromised.
> - Assumptions stated in the `defskeleton` or `defgoal` can be varied per experiment.
> - The compromise experiment is the payoff: leave one key unconstrained and constrain the other, then swap.

---

## Running CPSA Models

Use this standard workflow for modeling RFC protocols:

1. **Check Parentheses**: `python3 check_parens.py --fix model.scm`
2. **Initialize**: `cpsa4init` (run with no arguments) - generates Makefile and cpsa4.mk
3. **Build**: `make` - runs analysis with sensible defaults
4. **Clean**: `make clean` - wipes compiled output (*.txt, *.xhtml)
5. **View**: Open the generated `.xhtml` file or use `cpsa4graph` for visualization

This generates:
- `model.txt` - CPSA analysis output
- `model_shapes.txt` - extracted protocol shapes
- `model.xhtml` - interactive visualization
