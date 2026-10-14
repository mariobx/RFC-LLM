# Message algebra, macros, and lang

## defmacro — preprocessing

Expanded textually before the analyser sees the file. By the time CPSA runs, the
macro does not exist. Purely for readability and for keeping repeated terms
identical.

```lisp
(defmacro (sdl_header dest)
  (cat "ver" "bypass flag" dest "VCID" "Frame len"))
```

Parameters are positional; names are local to the definition. Use a macro when:
- literals are baked in (a macro can hold `"tag:00-0001"`; a lang operator cannot)
- the expansion spans multiple trace events (use the `^` splice)
- the same term must appear byte-identically in several places, e.g. a payload
  that appears once inside `enc` and again inside the `hash` covering it

## lang — extends the algebra

Goes in the protocol's association list, after the roles.

```lisp
(lang (keyid atom) (seq_n atom) (successor hash) (keyid_of hash)
      (upload_block (tuple 4)))
```

Two kinds of extension:

- **new atomic sorts** — `(keyid atom)`. Needed if you want `non-orig` or
  `uniq-orig` on the value, since those require atoms. Also stops adversary-
  supplied values of other sorts from unifying with it.
- **new operations** — `tuple`, `hash`, `enc`.

## tuple vs hash — the decision that matters

- `tuple` behaves like concatenation: **the adversary can construct it and
  extract its contents.** Correct for plain field concatenation.
- `hash` is opaque: the adversary can neither invert it nor construct it without
  the arguments. Correct for one-way functions.

Choosing `tuple` for something that should be opaque leaks its contents.
Choosing `hash` for something public overstates protection — it makes a
guessable public label behave like an unforgeable token. State which you chose
and why.

## Tagged concatenation

A leading string literal keeps a `cat` from unifying with an unrelated one:

```lisp
(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))
```

This is the older idiom; declared tuples are the modern replacement and the
manual describes them as the more efficient representation. Either is defensible;
be consistent within a project.

## Modelling cryptography

- `(enc m k)` — authenticated encryption, symmetric or asymmetric. Unforgeable
  without `k`. Keys used for encryption are **not** part of the ciphertext, so
  `(enc m k)` does not transmit `k`.
- `(hash a b k)` — a MAC keyed on `k`.
- IV and MAC tag are normally folded into `enc`; CPSA cannot say anything useful
  about IV reuse. Say so rather than implying coverage.
- Encrypt-then-MAC is modelled by putting the ciphertext inside the hash:
  `(hash hdr sn (enc payload ke) ka)`. This also lets the MAC cover cleartext
  header fields, which is usually the reason the hash earns its place — without
  it, `(enc m k)` is already unforgeable and a separate MAC over only the
  ciphertext tells the analyser nothing new.
- AEAD with associated data flattens: `enc` does not distinguish authenticated-
  but-not-encrypted inputs. Note the limitation.

## What CPSA cannot express

- Counters and windows. `successor` chains give ordering, not arithmetic; an
  anti-replay window is receiver state, not a message property.
- Failed decryption. There is no "tried the wrong key" event, so a key-lookup
  step must be modelled explicitly (as state, or by making the identifier a
  function of the key) or not at all.
- Chosen-plaintext oracles. An encryption oracle is invisible in a Dolev-Yao
  model even when it is a real weakness.
