# Official MITRE CPSA Examples Catalog (Part 1: DH_hack.scm to goalsvar.scm)

This catalog documents the first 50 official MITRE CPSA `.scm` example files (`DH_hack.scm` through `goalsvar.scm`, sorted alphabetically) from `03_examples_scm/`. Every declaration, role, sort, trace event, rule, goal, macro, and S-expression excerpt is extracted directly from the source `.scm` files.

---

## DH_hack.scm

- **File Path**: `03_examples_scm/DH_hack.scm`
- **Algebra & Herald**: `(herald "DH Hack" (bound 15))` — `basic` algebra (declared in `(defprotocol DH_hack basic ...)`), with herald flag `(bound 15)`.
- **Protocol & Purpose**: Demonstrates a limited technique for approximating Diffie-Hellman (DH) key agreement inside the `basic` crypto algebra. A DH key pair $(x, g^x)$ is modeled as `((invk x), x)` of sort `akey`, where the owner of `(invk x)` computes `(hash (invk x) y)` and the owner of `(invk y)` computes `(hash x (invk y))`. An auxiliary `commute` role translates encryptions under `(hash (invk x) y)` into encryptions under `(hash x (invk y))`, preventing decryption unless the adversary possesses either `(invk x)` or `(invk y)` while ignoring algebraic DH properties.
- **Roles & Variables**:
  - `init1`:
    - `(vars (gcs name) (cek skey) (x y akey) (d data))`
    - Role-level assumptions: `(uniq-orig cek d x)`
    - Trace: `(send (enc x (enc cek (hash (invk x) y)) (enc d cek) (privk gcs)))`
  - `resp`:
    - `(vars (gcs name) (cek skey) (x y akey) (d data))`
    - Role-level assumptions: `(non-orig (privk gcs))`
    - Trace: `(recv (enc x (enc cek (hash x (invk y))) (enc d cek) (privk gcs)))`
  - `commute`:
    - `(vars (gcs name) (cek skey) (x y akey) (d data))`
    - Role-level assumptions: `(non-orig (privk gcs))`
    - Trace: `(recv (enc x (enc cek (hash (invk x) y)) (enc d cek) (privk gcs)))` followed by `(send (enc x (enc cek (hash x (invk y))) (enc d cek) (privk gcs)))`
- **Skeletons, Goals, Rules & Macros**:
  - Contains 6 `(defskeleton DH_hack ...)` queries testing `resp` of height 1:
    1. `(defstrand resp 1 (x x) (y y))` with `(non-orig (invk x) (invk y))`
    2. `(defstrand resp 1 (cek cek) (x x))` with `(non-orig (invk x))`
    3. `(defstrand resp 1 (cek cek) (y y))` with `(non-orig (invk y))`
    4. `(defstrand resp 1 (cek cek) (x x) (y y))` with `(deflistener cek)` and `(non-orig (invk x) (invk y))`
    5. `(defstrand resp 1 (cek cek) (x x))` with `(deflistener cek)` and `(non-orig (invk x))`
    6. `(defstrand resp 1 (cek cek) (y y))` with `(deflistener cek)` and `(non-orig (invk y))`
  - No rules, lemmas, goals, or macros.
- **When to Reference This Example**: Reference this example when modeling a protocol in the `basic` algebra that requires a lightweight commutativity bridge (via an auxiliary `commute` role and `(hash (invk x) y)` / `(hash x (invk y))`) without switching the entire protocol to the `diffie-hellman` algebra.
- **Key S-Expression Excerpt**:
```scheme
(herald "DH Hack" (bound 15))

(defprotocol DH_hack basic
  (defrole init1
    (vars (gcs name) (cek skey) (x y akey) (d data))
    (trace
     (send (enc x (enc cek (hash (invk x) y)) (enc d cek) (privk gcs))))
    (uniq-orig cek d x))
  (defrole resp
    (vars (gcs name) (cek skey) (x y akey) (d data))
    (trace
     (recv (enc x (enc cek (hash x (invk y))) (enc d cek) (privk gcs))))
    (non-orig (privk gcs)))
  (defrole commute
    (vars (gcs name) (cek skey) (x y akey) (d data) )
    (trace
     (recv (enc x (enc cek (hash (invk x) y)) (enc d cek) (privk gcs)))
     (send (enc x (enc cek (hash x (invk y))) (enc d cek) (privk gcs))))
    (non-orig (privk gcs))))

 (defskeleton DH_hack
  (vars (x y akey))
  (defstrand resp 1 (x x) (y y))
  (non-orig (invk x) (invk y)))
```

---

## ab.scm

- **File Path**: `03_examples_scm/ab.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol ab basic ...)`.
- **Protocol & Purpose**: Models a minimal "A-B cascading" non-termination/dead-skeleton pattern. An initiator sends `(enc x k)` and expects `(enc x x k)`, while roles `A` and `B` each output `(enc x x k)` only after receiving `(enc "A" x k)` or `(enc "B" x k)` respectively. Because nothing can ever produce the `"A"` or `"B"` tagged inputs under secret key `k`, the input skeleton is dead, illustrating how roles that appear to make progress on an encrypted return format fail when their preconditions cannot be satisfied.
- **Roles & Variables**:
  - `init`:
    - `(vars (x text) (k skey))`
    - Role-level assumptions: `(uniq-orig x)` and `(non-orig k)`
    - Trace: `(send (enc x k))`, `(recv (enc x x k))`
  - `A`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "A" x k))`, `(send (enc x x k))`
  - `B`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "B" x k))`, `(send (enc x x k))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton ab (vars (x text) (k skey)) (defstrand init 2 (x x) (k k)))`.
  - Uses `uniq-orig` and `non-orig` at the role level; no rules, goals, or macros.
- **When to Reference This Example**: Reference this example when diagnosing dead skeletons (0 shapes produced) or search cascading where responder roles emit the message pattern expected by an initiator (`(enc x x k)`) but require an unreachable encrypted tag (`(enc "A" x k)`) in their `recv` event.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol ab basic
  (defrole init (vars (x text) (k skey))
    (trace
     (send (enc x k))
     (recv (enc x x k)))
    (uniq-orig x)
    (non-orig k))
  (defrole A (vars (x text) (k skey))
    (trace
     (recv (enc "A" x k))
     (send (enc x x k))))
  (defrole B (vars (x text) (k skey))
    (trace
     (recv (enc "B" x k))
     (send (enc x x k))))
)

(defskeleton ab
  (vars (x text) (k skey))
  (defstrand init 2 (x x) (k k)))
```

---

## abc.scm

- **File Path**: `03_examples_scm/abc.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol abc basic ...)`.
- **Protocol & Purpose**: Extends `ab.scm` to three auxiliary roles (`A`, `B`, and `C`) to demonstrate three-way A-B-C cascading on a dead skeleton. Roles `A`, `B`, and `C` each produce `(enc x x k)` upon receiving `(enc "A" x k)`, `(enc "B" x k)`, or `(enc "C" x k)`, none of which can be constructed from the initiator's `(send (enc x k))` when `k` is `non-orig`.
- **Roles & Variables**:
  - `init`:
    - `(vars (x text) (k skey))`
    - Role-level assumptions: `(uniq-orig x)`, `(non-orig k)`
    - Trace: `(send (enc x k))`, `(recv (enc x x k))`
  - `A`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "A" x k))`, `(send (enc x x k))`
  - `B`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "B" x k))`, `(send (enc x x k))`
  - `C`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "C" x k))`, `(send (enc x x k))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton abc (vars (x text) (k skey)) (defstrand init 2 (x x) (k k)))`.
  - Uses `uniq-orig` and `non-orig` inside `defrole init`.
- **When to Reference This Example**: Reference this example alongside `ab.scm` to understand multi-branch cohort cascading and dead-skeleton termination when multiple roles share identical outgoing ciphertexts but incompatible incoming tags.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol abc basic
  (defrole init (vars (x text) (k skey))
    (trace
     (send (enc x k))
     (recv (enc x x k)))
    (uniq-orig x)
    (non-orig k))
  (defrole A (vars (x text) (k skey))
    (trace
     (recv (enc "A" x k))
     (send (enc x x k))))
  (defrole B (vars (x text) (k skey))
    (trace
     (recv (enc "B" x k))
     (send (enc x x k))))
  (defrole C (vars (x text) (k skey))
    (trace
     (recv (enc "C" x k))
     (send (enc x x k))))
)

(defskeleton abc
  (vars (x text) (k skey))
  (defstrand init 2 (x x) (k k)))
```

---

## aik.scm

- **File Path**: `03_examples_scm/aik.scm`
- **Algebra & Herald**: `(herald "Anonymous identity protocol from TCG")` — `basic` algebra (`(defprotocol aikprot basic ...)`), no extra herald flags.
- **Protocol & Purpose**: Models the Trusted Computing Group (TCG) Anonymous Identity Key (AIK) credential issuance protocol (`aikprot`) involving a manufacturer CA (`ca`), a Trusted Platform Module (`tpm`), and a Privacy CA (`pca`). The CA issues an endorsement key certificate `(enc "ekc" mf ek (privk mf))`, the TPM generates a fresh AIK pair `(k, (invk k))` and requests an anonymous identity certificate `(enc "aic" i k x (privk pc))` encrypted under `ek`, and the TPM subsequently exports `(enc k (invk k) srk)` wrapped under the Storage Root Key `srk`.
- **Roles & Variables**:
  - `ca`:
    - `(vars (mf name) (ek akey))`
    - Role-level assumptions: `(non-orig (invk ek))`
    - Trace: `(send (enc "ekc" mf ek (privk mf)))`
  - `tpm`:
    - `(vars (i x mf pc name) (ek k akey) (srk skey))`
    - Role-level assumptions: `(non-orig srk (invk ek))` and `(uniq-orig k (invk k))`
    - Trace:
      1. `(recv (cat x i (enc "ekc" mf ek (privk mf))))`
      2. `(send (cat i k x (enc "ekc" mf ek (privk mf))))`
      3. `(recv (enc (enc "aic" i k x (privk pc)) ek))`
      4. `(send (cat (enc "aic" i k x (privk pc)) (enc k (invk k) srk)))`
  - `pca`:
    - `(vars (i x mf pc name) (ek k akey))`
    - Role-level assumptions: `(non-orig (privk mf))`
    - Trace:
      1. `(recv (cat i k x (enc "ekc" mf ek (privk mf))))`
      2. `(send (enc (enc "aic" i k x (privk pc)) ek))`
- **Skeletons, Goals, Rules & Macros**:
  - Two `(defskeleton aikprot ...)` blocks:
    1. Full `tpm` strand of height 4 (`(defstrand tpm 4 (mf mf) (pc pc))`) with `(non-orig (privk pc))`.
    2. Listener skeleton (`(deflistener (enc "aic" i k x (privk pc)))`) with `(non-orig (privk pc))`.
- **When to Reference This Example**: Reference this example when modeling PKI certificate enrollment, Privacy CA / TPM AIK issuance, or generating asymmetric key pairs on the fly where both `k` and `(invk k)` are declared `(uniq-orig k (invk k))` and wrapped under a symmetric storage key `srk`.
- **Key S-Expression Excerpt**:
```scheme
(herald "Anonymous identity protocol from TCG")

(defprotocol aikprot basic
  (defrole ca
    (vars (mf name) (ek akey))
    (trace (send (enc "ekc" mf ek (privk mf))))
    (non-orig (invk ek)))
  (defrole tpm
    (vars (i x mf pc name) (ek k akey) (srk skey))
    (trace (recv (cat x i (enc "ekc" mf ek (privk mf))))
      (send (cat i k x (enc "ekc" mf ek (privk mf))))
      (recv (enc (enc "aic" i k x (privk pc)) ek))
      (send (cat (enc "aic" i k x (privk pc)) (enc k (invk k) srk))))
    (non-orig srk (invk ek))
    (uniq-orig k (invk k)))
  (defrole pca
    (vars (i x mf pc name) (ek k akey))
    (trace (recv (cat i k x (enc "ekc" mf ek (privk mf))))
      (send (enc (enc "aic" i k x (privk pc)) ek)))
    (non-orig (privk mf))))

(defskeleton aikprot
  (vars (i x mf pc name) (ek k akey) (srk skey))
  (defstrand tpm 4 (mf mf) (pc pc))
  (non-orig (privk pc)))
```

---

## atomic-open-closed.scm

- **File Path**: `03_examples_scm/atomic-open-closed.scm`
- **Algebra & Herald**: `(herald atomic-open-closed (bound 44))` (with commented-out flags `;; (try-old-strands)`, `;; (check-nonces)`, `;; (reverse-nodes)`) — `basic` algebra (`(defprotocol atomic-open-closed basic ...)`).
- **Protocol & Purpose**: Models a stateful device (`d`) controlled by an owner (`o`) using two mutable state locations (`lk` and `ls` of sort `locn`) and a power-up channel (`start-ch` of sort `chan`). The device transitions between closed (`(dev-state-closed d o)`) and opened (`(dev-state-opened d o)`) states via `load` and `stor` trace events, and only allows a user to pass (`dev-pass`) when `ls` holds `(dev-state-opened d o)`. Extensive `defrule` axioms enforce state-generation (`gen-st`), same-device register pairing (`(fact same-dev ls lk)`), single-threaded register ordering, strand completion, and multi-step `load`/`stor` atomicity.
- **Roles & Variables**:
  - `dev-up`: `(vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))`, `(auth start-ch)`, trace: `(recv start-ch (cat "power-up" d o k))`, `(load lk old)`, `(stor lk (dev-key-state d o k))`, `(load ls old1)`, `(stor ls (dev-state-closed d o))`, `(send (enc "up" k))`
  - `owner-power-dev`: `(vars (k skey) (d o name) (start-ch chan))`, `(conf start-ch)`, trace: `(send start-ch (cat "power-up" d o k))`, `(recv (enc "up" k))`
  - `owner-open`: `(vars (k skey) (n text) (d o name))`, trace: `(send (enc "open" d o n k))`, `(recv n)`
  - `owner-close`: `(vars (k skey) (n text) (d o name))`, trace: `(send (enc "close" d o n k))`, `(recv n)`
  - `dev-open`: `(vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))`, trace: `(recv (enc "open" d o n k))`, `(load lk (dev-key-state d o k))`, `(load ls (dev-state-any d o any))`, `(stor ls (dev-state-opened d o))`, `(send n)`
  - `dev-close`: `(vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))`, trace: `(recv (enc "close" d o n k))`, `(load lk (dev-key-state d o k))`, `(load ls (dev-state-any d o any))`, `(stor ls (dev-state-closed d o))`, `(send n)`
  - `dev-pass`: `(vars (k skey) (n text) (d o name) (lk ls locn))`, `(uniq-orig n)`, trace: `(recv (enc "may I pass" k))`, `(load lk (dev-key-state d o k))`, `(load ls (dev-state-opened d o))`, `(send (enc "you may pass" n k))`
  - `user-pass`: `(vars (k skey) (n text) (d o name) (l locn))`, trace: `(send (enc "may I pass" k))`, `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros** (`defmacro`): `(dev-key-state d o k)`, `(opened o)`, `(closed o)`, `(dev-state-opened d o)`, `(dev-state-closed d o)`, `(dev-state-any d o any)`.
  - **Rules** (`defrule`): 31 active rules covering:
    - `gen-st` state-generation declarations: `gen-state-close`, `gen-state-pass`, `gen-state-open`, `gen-state-close` (for `dev-key-state`), `gen-state-pass` (for `dev-key-state`).
    - Uniqueness & register coupling via `fact`: `power-deliver-once`, `intro-same-dev-up`, `intro-same-dev-open`, `intro-same-dev-close`, `intro-same-dev-pass`, `same-dev-ls-lk`, `same-dev-lk-ls`.
    - Single-threaded location ordering (`prec`): `single-thread-up-up`, `single-thread-up-open`, `single-thread-up-close`, `single-thread-open-open`, `single-thread-ls-open-close`, `single-thread-close-close`, `atomic-up-pass`.
    - Strand completion & atomic load/stor transitions: `dev-up-completes`, `dev-open-completes`, `dev-close-completes`, `dev-pass-completes`, `dev-up-atomic1`, `dev-up-atomic2`, `dev-open-atomic1`, `dev-open-atomic2`, `dev-close-atomic1`, `dev-close-atomic2`, `dev-pass-atomic1`, `dev-pass-atomic2`.
  - **Skeletons**: 3 active `(defskeleton atomic-open-closed ...)` queries testing `owner-power-dev` with `(deflistener k)`, `dev-pass` alone, and `owner-power-dev` + `dev-pass` with `(uniq-orig k)`.
- **When to Reference This Example**: Reference this example whenever modeling mutable device state with `locn`, `load`, and `stor` in CPSA, especially when you need `defrule` patterns for `gen-st`, multi-register coupling (`(fact same-dev ls lk)`), or atomic load-modify-store sequences using `prec` and sort `indx`.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol atomic-open-closed basic
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))
    (trace
     (recv start-ch (cat "power-up" d o k))
     (load lk old)
     (stor lk (dev-key-state d o k))
     (load ls old1)
     (stor ls (dev-state-closed d o))
     (send (enc "up" k)))
    (auth start-ch))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (recv (enc "open" d o n k))
     (load lk (dev-key-state d o k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-opened d o))
     (send n)))

  (defrule dev-open-atomic1
    (forall ((x z strd) (i1 indx))
      (implies
       (and (p "dev-open" z 4)
            (prec x i1 z 3))
       (or (= x z)
           (prec x i1 z 1))))))
```

---

## attest.scm

- **File Path**: `03_examples_scm/attest.scm`
- **Algebra & Herald**: `(herald attest-door)` — `basic` algebra across three protocol variants (`attest-door`, `attest-door-trust`, `attest-door-trust-attest`).
- **Protocol & Purpose**: Models a door entry protocol augmented with remote attestation (`appraise`) and a malicious "fake door" role (`squealer`) that leaks the session key `k`. Progressively refines the trust model across three protocols using `defrule` axioms:
  1. `attest-door`: Includes only rule `yes` (if an uncompromised appraiser `a` completes, the attested door `d` has an uncompromised private key `(non (invk d))`).
  2. `attest-door-trust`: Adds rule `trust` (a door `d` that passes appraisal cannot also act as a `squealer`, deriving `(false)`).
  3. `attest-door-trust-attest`: Adds rule `uncompromised-people-choose-uncompromised-appraisers` (an uncompromised `person` always queries an uncompromised appraiser `(non (invk a))`).
- **Roles & Variables**:
  - Identical across all 3 protocols (`attest-door`, `attest-door-trust`, `attest-door-trust-attest`):
    - `appraise`: `(vars (d p a akey) (n text))`, trace: `(recv (enc (enc d n (invk p)) a))`, `(send (enc n a p))`
    - `person`: `(vars (d p a akey) (k skey) (n t text))`, `(uniq-orig n k)`, trace: `(send (enc (enc d n (invk p)) a))`, `(recv (enc n a p))`, `(send (enc (enc k (invk p)) d))`, `(recv (enc t k))`, `(send t)`
    - `door`: `(vars (d p akey) (k skey) (t text))`, `(uniq-orig t)`, trace: `(recv (enc (enc k (invk p)) d))`, `(send (enc t k))`, `(recv t)`
    - `squealer`: `(vars (d p akey) (k skey) (t text))`, trace: `(recv (enc (enc k (invk p)) d))`, `(send k)`
- **Skeletons, Goals, Rules & Macros**:
  - **Rules**: `yes` (uses `exists` and `(non (invk d))`), `trust` (uses `(false)` to forbid a strand `w` of `squealer` sharing `d` with `appraise` strand `z`), and `uncompromised-people-choose-uncompromised-appraisers`.
  - **Skeletons**: 2 `(defskeleton ...)` blocks per protocol (6 total), analyzing `person` of height 5 with `(non-orig (invk p) (invk a))` and `door` of height 3 with `(non-orig (invk d) (invk p))`.
- **When to Reference This Example**: Reference this example when modeling remote attestation, key compromise / rogue peer exclusion (`squealer`), or writing `defrule` axioms that transfer `(non (invk ...))` trust from an appraiser/authority to a peer or rule out dishonest roles via `(false)`.
- **Key S-Expression Excerpt**:
```scheme
  (defrule yes
    (forall ((z strd) (a akey))
	    (implies
	     (and (p "appraise" z 2)
		  (p "appraise" "a" z a)
		  (non (invk a)))
	     (exists ((d akey))
		     (and (p "appraise" "d" z d)
			  (non (invk d))))))
    (comment "Appraisal succeeded"))
  (defrule trust
    (forall ((z w strd) (d akey))
	    (implies
	     (and (p "appraise" z 2)
		  (p "appraise" "d" z d)
		  (p "squealer" w 2)
		  (p "squealer" "d" w d))
	     (false)))
    (comment "Passing attestation means not a squealer"))
  (defrule uncompromised-people-choose-uncompromised-appraisers
    (forall ((z strd) (a p akey))
	    (implies
	     (and (p "person" z 3)
		  (p "person" "p" z p)
		  (p "person" "a" z a)
		  (non (invk p)))
	     (non (invk a)))))
```

---

## auth-enc.scm

- **File Path**: `03_examples_scm/auth-enc.scm`
- **Algebra & Herald**: `(herald auth-enc)` — `basic` algebra (`(defprotocol auth-enc basic ...)`).
- **Protocol & Purpose**: Minimal roletran-annotated protocol demonstrating transmission of an encrypted nonce `(enc n k)` followed by the plaintext nonce and key `(cat n k)` over an authenticated channel `ch`. Uses `(inputs ...)` and `(outputs ...)` declarations inside `defrole`.
- **Roles & Variables**:
  - `init`:
    - `(vars (n text) (k skey) (ch chan))`
    - Role-level assumptions & I/O: `(uniq-orig n k)`, `(inputs ch)`
    - Trace: `(send ch (enc n k))`, `(send ch (cat n k))`
  - `resp`:
    - `(vars (n text) (k skey) (ch chan))`
    - Role-level I/O: `(inputs ch)`, `(outputs n)`
    - Trace: `(recv ch (enc n k))`, `(recv ch (cat n k))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton auth-enc (vars (ch chan)) (defstrand resp 2 (ch ch)) (auth ch))`.
- **When to Reference This Example**: Reference this example for the exact syntax of `(inputs ...)` and `(outputs ...)` role declarations (used by `cpsa4roletran`) combined with channel-authenticated `(send ch ...)` / `(recv ch ...)` events and `(auth ch)`.
- **Key S-Expression Excerpt**:
```scheme
(herald auth-enc)

(defprotocol auth-enc basic
  (defrole init
    (vars (n text) (k skey) (ch chan))
    (trace (send ch (enc n k)) (send ch (cat n k)))
    (uniq-orig n k)
    (inputs ch))
  (defrole resp
    (vars (n text) (k skey) (ch chan))
    (trace (recv ch (enc n k)) (recv ch (cat n k)))
    (inputs ch)
    (outputs n)))

(defskeleton auth-enc
  (vars (ch chan))
  (defstrand resp 2 (ch ch))
  (auth ch))
```

---

## auth-hash.scm

- **File Path**: `03_examples_scm/auth-hash.scm`
- **Algebra & Herald**: `(herald auth-hash)` — `basic` algebra (`(defprotocol auth-hash basic ...)`).
- **Protocol & Purpose**: Companion to `auth-enc.scm` that sends a hash commitment `(hash n)` followed by `n` over an authenticated channel `ch`, with `(inputs ch)` and `(outputs n)` declarations for `cpsa4roletran` translation.
- **Roles & Variables**:
  - `init`:
    - `(vars (n text) (ch chan))`
    - Role-level assumptions & I/O: `(uniq-orig n)`, `(inputs ch)`
    - Trace: `(send ch (hash n))`, `(send ch n)`
  - `resp`:
    - `(vars (n text) (ch chan))`
    - Role-level I/O: `(inputs ch)`, `(outputs n)`
    - Trace: `(recv ch (hash n))`, `(recv ch n)`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton auth-hash (vars (ch chan)) (defstrand resp 2 (ch ch)) (auth ch))`.
- **When to Reference This Example**: Reference this example when using `(hash n)` commitments over an authenticated channel `(auth ch)` with `inputs`/`outputs` roletran annotations.
- **Key S-Expression Excerpt**:
```scheme
(herald auth-hash)

(defprotocol auth-hash basic
  (defrole init
    (vars (n text) (ch chan))
    (trace (send ch (hash n)) (send ch n))
    (uniq-orig n)
    (inputs ch))
  (defrole resp
    (vars (n text) (ch chan))
    (trace (recv ch (hash n)) (recv ch n))
    (inputs ch)
    (outputs n)))

(defskeleton auth-hash
  (vars (ch chan))
  (defstrand resp 2 (ch ch))
  (auth ch))
```

---

## blanchet-strandmax.scm

- **File Path**: `03_examples_scm/blanchet-strandmax.scm`
- **Algebra & Herald**: `(herald "Blanchet's Simple Example Protocol (strand max)" (comment "There is a flaw in this protocol by design"))` — `basic` algebra across three protocols (`blanchet-max`, `blanchet-max-akey`, `blanchet-max-fixed`).
- **Protocol & Purpose**: Models Bruno Blanchet's classic flawed two-message signed-then-encrypted session key exchange (`init` sends `(enc (enc s (privk a)) (pubk b))`, `resp` replies with `(enc d s)`) and its fixed variant (`(enc (enc s b (privk a)) (pubk b))`, which binds the responder's identity `b` inside the signature). Demonstrates `(defstrandmax role ...)` syntax (which automatically specifies the full height of a role) as well as both named asymmetric keys (`pubk`/`privk`) and unnamed asymmetric keys (`akey`/`invk`).
- **Roles & Variables**:
  - In `blanchet-max` (named asymmetric keys):
    - `init`: `(vars (a b name) (s skey) (d data))`, trace: `(send (enc (enc s (privk a)) (pubk b)))`, `(recv (enc d s))`
    - `resp`: `(vars (a b name) (s skey) (d data))`, trace: `(recv (enc (enc s (privk a)) (pubk b)))`, `(send (enc d s))`
  - In `blanchet-max-akey` (unnamed asymmetric keys `akey`):
    - `init`: `(vars (a b akey) (s skey) (d data))`, trace: `(send (enc (enc s (invk a)) b))`, `(recv (enc d s))`
    - `resp`: `(vars (a b akey) (s skey) (d data))`, trace: `(recv (enc (enc s (invk a)) b))`, `(send (enc d s))`
  - In `blanchet-max-fixed` (fixed with `b` inside signature):
    - `init`: `(vars (a b name) (s skey) (d data))`, trace: `(send (enc (enc s b (privk a)) (pubk b)))`, `(recv (enc d s))`
    - `resp`: `(vars (a b name) (s skey) (d data))`, trace: `(recv (enc (enc s b (privk a)) (pubk b)))`, `(send (enc d s))`
- **Skeletons, Goals, Rules & Macros**:
  - 12 `(defskeleton ...)` blocks (4 per protocol: initiator perspective, initiator secrecy with `(deflistener d)`, responder perspective, responder secrecy with `(deflistener d)`).
  - The first 4 skeletons in `blanchet-max` use `(defstrandmax init ...)` and `(defstrandmax resp ...)` instead of explicit numeric strand heights.
- **When to Reference This Example**: Reference this example to see how `(defstrandmax <role> ...)` avoids hardcoding strand lengths in `defskeleton`, how to compare named (`(pubk b)`/`(privk a)`) vs. unnamed (`b`/`(invk a)`) asymmetric keys, and how omitting the recipient's identity inside a signed key transport message causes an authentication/secrecy flaw.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol blanchet-max basic
  (defrole init
    (vars (a b name) (s skey) (d data))
    (trace
     (send (enc (enc s (privk a)) (pubk b)))
     (recv (enc d s))))
  (defrole resp
    (vars (a b name) (s skey) (d data))
    (trace
     (recv (enc (enc s (privk a)) (pubk b)))
     (send (enc d s))))
  (comment "Blanchet's protocol using named asymmetric keys"))

(defskeleton blanchet-max
  (vars (a b name) (s skey) (d data))
  (defstrandmax init (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk b))
  (uniq-orig s d)
  (comment "From the initiator's perspective, is the secret leaked?"))
```

---

## blanchet.scm

- **File Path**: `03_examples_scm/blanchet.scm`
- **Algebra & Herald**: `(herald "Blanchet's Simple Example Protocol" (comment "There is a flaw in this protocol by design"))` — `basic` algebra across two protocols (`blanchet` and `blanchet-fixed`).
- **Protocol & Purpose**: Standard version of Blanchet's flawed signed-then-encrypted key exchange (`blanchet`) and its recipient-bound fix (`blanchet-fixed`) using explicit strand heights `(defstrand init 2 ...)` and `(defstrand resp 2 ...)`. In `blanchet`, an initiator `a` signing `s` without `b`'s name allows a dishonest recipient to forward `(enc s (privk a))` re-encrypted under an honest responder `b`'s public key, whereas `blanchet-fixed` signs `(enc s b (privk a))`.
- **Roles & Variables**:
  - In `blanchet`:
    - `init`: `(vars (a b name) (s skey) (d data))`, trace: `(send (enc (enc s (privk a)) (pubk b)))`, `(recv (enc d s))`
    - `resp`: `(vars (a b name) (s skey) (d data))`, trace: `(recv (enc (enc s (privk a)) (pubk b)))`, `(send (enc d s))`
  - In `blanchet-fixed`:
    - `init`: `(vars (a b name) (s skey) (d data))`, trace: `(send (enc (enc s b (privk a)) (pubk b)))`, `(recv (enc d s))`
    - `resp`: `(vars (a b name) (s skey) (d data))`, trace: `(recv (enc (enc s b (privk a)) (pubk b)))`, `(send (enc d s))`
- **Skeletons, Goals, Rules & Macros**:
  - 8 `(defskeleton ...)` blocks (4 for `blanchet`, 4 for `blanchet-fixed`) testing initiator and responder perspectives with and without `(deflistener d)`, using `(non-orig (privk b))`, `(non-orig (privk a) (privk b))`, `(uniq-orig s)`, and `(uniq-orig s d)`.
- **When to Reference This Example**: Reference this example as the canonical template for analyzing both authentication and payload secrecy (`(deflistener d)` with `(uniq-orig s d)`) from initiator and responder perspectives in a public-key session key transport protocol.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol blanchet-fixed basic
  (defrole init
    (vars (a b name) (s skey) (d data))
    (trace
     (send (enc (enc s b (privk a)) (pubk b)))
     (recv (enc d s))))
  (defrole resp
    (vars (a b name) (s skey) (d data))
    (trace
     (recv (enc (enc s b (privk a)) (pubk b)))
     (send (enc d s))))
  (comment "Fixed Blanchet's protocol using named asymmetric keys"))

(defskeleton blanchet-fixed
  (vars (a b name) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk b))
  (uniq-orig s d)
  (comment "From the initiator's perspective, is the secret leaked?"))
```

---

## bug_example.scm

- **File Path**: `03_examples_scm/bug_example.scm`
- **Algebra & Herald**: `(herald bug_example (bound 20))` — `basic` algebra (`(defprotocol bug_example basic ...)`), with herald flag `(bound 20)`.
- **Protocol & Purpose**: Contains two definitions of `bug_example` that test inverse-key (`invk`) flipping inside hashed encryption keys `(hash x (invk y))` vs. `(hash (invk x) y)`. In the first protocol definition, a single `flip` role receives `(enc k (hash k1 k2))` and sends `(enc k (hash (invk k1) (invk k2)))` (relying on `(invk (invk k)) = k` unification). In the second definition, two roles `flip1` and `flip2` explicitly match `(hash (invk k1) k2)` and `(hash k1 (invk k2))` respectively.
- **Roles & Variables**:
  - First `(defprotocol bug_example basic ...)`:
    - `init`: `(vars (x y akey))`, `(non-orig (invk y) (invk x))`, trace: `(send (enc y (hash x (invk y))))`
    - `resp`: `(vars (x y akey))`, `(non-orig (invk x) (invk y))`, trace: `(recv (enc y (hash (invk x) y)))`
    - `flip`: `(vars (k k1 k2 akey))`, trace: `(recv (enc k (hash k1 k2)))`, `(send (enc k (hash (invk k1) (invk k2))))`
  - Second `(defprotocol bug_example basic ...)`:
    - `init`: `(vars (x y akey))`, `(non-orig (invk y) (invk x))`, trace: `(send (enc y (hash x (invk y))))`
    - `resp`: `(vars (x y akey))`, `(non-orig (invk x) (invk y))`, trace: `(recv (enc y (hash (invk x) y)))`
    - `flip1`: `(vars (k k1 k2 akey))`, trace: `(recv (enc k (hash (invk k1) k2)))`, `(send (enc k (hash k1 (invk k2))))`
    - `flip2`: `(vars (k k1 k2 akey))`, trace: `(recv (enc k (hash k1 (invk k2))))`, `(send (enc k (hash (invk k1) k2)))`
- **Skeletons, Goals, Rules & Macros**:
  - Two identical `(defskeleton bug_example (vars (x y akey)) (defstrand resp 1 (x x) (y y)))` queries, one after each `defprotocol`.
- **When to Reference This Example**: Reference this example when testing how CPSA unifies involutive `(invk ...)` terms inside compound keys `(hash k1 k2)` versus explicit pattern-matched `(invk k1)` / `(invk k2)` transformer roles.
- **Key S-Expression Excerpt**:
```scheme
(herald bug_example (bound 20))

(defprotocol bug_example basic
  (defrole init (vars (x y akey))
    (trace
     (send (enc y (hash x (invk y)))))
    (non-orig (invk y) (invk x)))
  (defrole resp (vars (x y akey))
    (trace
     (recv (enc y (hash (invk x) y))))
    (non-orig (invk x) (invk y)))
  (defrole flip (vars (k k1 k2 akey))
    (trace
     (recv (enc k (hash k1 k2)))
     (send (enc k (hash (invk k1) (invk k2)))))))

(defskeleton bug_example
  (vars (x y akey))
  (defstrand resp 1 (x x) (y y)))
```

---

## cert_lang.scm

- **File Path**: `03_examples_scm/cert_lang.scm`
- **Algebra & Herald**: `(herald cert-lang)` — `basic` algebra (`(defprotocol cert-uni basic ...)`).
- **Protocol & Purpose**: Demonstrates custom protocol-specific message constructors via `(lang (cert sign) (cert-body (tupl 3)))` in a certificate-based unilateral challenge-response protocol (`cert-uni`). A certificate authority (`certify`) sends a signed certificate `(cert (cert-body subj serial pk) (privk "cert" ca))` over channel `ch`. An initiator (`init`) receives the certificate on `ch-ca`, sends an encrypted challenge `(enc "challenge" chal pk)` on `ch-r`, and receives `chal` back. Includes a `defrule` (`certified-keys-uncompromised`) stating that any public key certified by an uncompromised CA has an uncompromised inverse `(non (invk pk))`.
- **Roles & Variables**:
  - `certify`:
    - `(vars (ch chan) (subj ca name) (pk akey) (serial data))`
    - Role-level I/O: `(inputs ch subj pk serial (privk "cert" ca))`
    - Trace: `(send ch (cert (cert-body subj serial pk) (privk "cert" ca)))`
  - `init`:
    - `(vars (ch-ca ch-r chan) (subj ca name) (pk akey) (serial data) (chal text))`
    - Role-level assumptions & I/O: `(uniq-orig chal)`, `(inputs ch-ca ch-r subj (pubk "cert" ca))`, `(outputs chal)`
    - Trace: `(recv ch-ca (cert (cert-body subj serial pk) (privk "cert" ca)))`, `(send ch-r (enc "challenge" chal pk))`, `(recv ch-r chal)`
  - `resp`:
    - `(vars (ch-ca ch-i chan) (subj ca name) (pk akey) (serial data) (chal text))`
    - Role-level I/O: `(inputs ch-ca ch-i subj (pubk "cert" ca) (invk pk))`, `(outputs chal)`
    - Trace: `(recv ch-ca (cert (cert-body subj serial pk) (privk "cert" ca)))`, `(recv ch-i (enc "challenge" chal pk))`, `(send ch-i chal)`
- **Skeletons, Goals, Rules & Macros**:
  - **Custom Language Declarations**: `(lang (cert sign) (cert-body (tupl 3)))` at the end of `defprotocol`.
  - **Rule**: `certified-keys-uncompromised` transferring `(non (privk "cert" ca))` on a `certify` strand to `(non (invk pk))`.
  - **Skeleton**: `(defskeleton cert-uni (vars (subj ca name) (pk akey) (serial data) (chal text)) (defstrand init 3 (ca ca) (chal chal)) (non-orig (privk "cert" ca)))`.
- **When to Reference This Example**: Reference this example when defining custom cryptographic or tuple operators via `(lang (<op> sign) (<op2> (tupl <n>)))`, when modeling PKI certificate validation rules (`certified-keys-uncompromised`), or when using `cpsa4roletran` `(inputs ...)` and `(outputs ...)` with channels and asymmetric keys.
- **Key S-Expression Excerpt**:
```scheme
  (defrole init
    (vars (ch-ca ch-r chan) (subj ca name) (pk akey)
      (serial data) (chal text))
    (trace
      (recv ch-ca
        (cert (cert-body subj serial pk) (privk "cert" ca)))
      (send ch-r (enc "challenge" chal pk))
      (recv ch-r chal))
    (uniq-orig chal)
    (inputs ch-ca ch-r subj (pubk "cert" ca))
    (outputs chal))
  (defrule certified-keys-uncompromised
    (forall ((zca strd) (subj ca name) (pk akey))
      (implies
        (and (p "certify" zca 1)
          (p "certify" "subj" zca subj)
          (p "certify" "ca" zca ca)
          (p "certify" "pk" zca pk) (non (privk "cert" ca)))
        (non (invk pk)))))
   (lang (cert sign) (cert-body (tupl 3))))
```

---

## chan-envelope.scm

- **File Path**: `03_examples_scm/chan-envelope.scm`
- **Algebra & Herald**: `(herald "Envelope Protocol With Channels" (bound 15))` — `basic` algebra (`(defprotocol envelope basic ...)` repeated 3 times with progressively stronger rule sets), with `(bound 15)`.
- **Protocol & Purpose**: Models the TPM Envelope Protocol where PCR state is carried over an authenticated and confidential channel `c` (`(conf c)` and `(auth c)`). Evaluates three rule sets across three scenarios each (listening for the secret `v`, listening for the refusal token `(refuse n v k aik)`, and listening for both simultaneously):
  1. Empty rule set: allows the TPM's PCR state on channel `c` to split.
  2. Adds rule `ordered-extends`: forces `tpm-extend` strands sharing channel `c` to be linearly ordered, though Alice's single encrypted session key `esk` can still talk to two different TPM channels.
  3. Adds rule `esk-same-as-chan`: enforces that `tpm-extend-enc` strands sharing `esk` must use the same state channel `(= c c-0)`, making the third scenario (both obtain and refuse tokens leaked) impossible as required.
- **Roles & Variables**:
  - Defined inside `(defmacro (roles) (^ ...))` and expanded into all three `envelope` protocol definitions:
    - `tpm-power-on`: `(vars (c chan))`, `(conf c)`, `(auth c)`, trace: `(recv "power on")`, `(send c "0")`
    - `tpm-extend`: `(vars (value current-value mesg) (c chan))`, `(conf c)`, `(auth c)`, trace: `(recv (cat "extend" value))`, `(recv c current-value)`, `(send c (hash current-value value))`, `(send "ext ok")`
    - `tpm-extend-enc`: `(vars (value current-value mesg) (esk skey) (c chan))`, `(non-orig esk)`, `(conf c)`, `(auth c)`, trace: `(recv (enc "extend" value esk))`, `(recv c current-value)`, `(send c (hash current-value value))`, `(send "ext ok")`
    - `tpm-quote`: `(vars (nonce current-value mesg) (c chan) (aik akey))`, `(non-orig aik)`, `(conf c)`, `(auth c)`, trace: `(recv (cat "quote" nonce))`, `(recv c current-value)`, `(send (enc "quote" current-value nonce aik))`
    - `tpm-create-key`: `(vars (k aik akey) (pcrval mesg) (esk skey))`, `(uniq-orig k)`, `(non-orig (invk k) aik esk)`, trace: `(recv (enc "create key" pcrval esk))`, `(send (enc "created" k pcrval aik))`
    - `tpm-decrypt`: `(vars (m pcrvals mesg) (k aik akey) (c chan))`, `(non-orig aik)`, `(conf c)`, `(auth c)`, trace: `(recv (cat "decrypt" (enc m k)))`, `(recv (enc "created" k pcrvals aik))`, `(recv c pcrvals)`, `(send m)`
    - `alice`: `(vars (n v data) (esk skey) (k aik akey))`, `(uniq-orig n v)`, `(non-orig aik esk)`, trace: `(send (enc "extend" n esk))`, `(send (enc "create key" (hash (hash "0" n) "obtain") esk))`, `(recv (enc "created" k (hash (hash "0" n) "obtain") aik))`, `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: `(defmacro (refuse n v k aik) (enc "quote" (hash (hash "0" n) "refuse") (enc v k) aik))` and `(defmacro (roles) (^ ...))` using the splice operator `^`.
  - **Rules**: `ordered-extends` and `esk-same-as-chan`.
  - **Skeletons**: 9 `(defskeleton envelope ...)` blocks (3 per protocol variant).
- **When to Reference This Example**: Reference this example to learn how to splice multiple `defrole` declarations into multiple `defprotocol` variants using `(defmacro (roles) (^ ...))`, and how to model linear state transitions over confidential/authenticated channels (`(conf c)`, `(auth c)`) using `prec` ordering rules.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol envelope basic
  (roles)

  (defrule ordered-extends
    (forall ((y z strd) (c chan))
	    (implies
	     (and (p "tpm-extend" y 3)
		  (p "tpm-extend" z 3)
		  (p "tpm-extend" "c" y c)
		  (p "tpm-extend" "c" z c))
	     (or (= y z)
		 (prec y 2 z 3)
		 (prec z 2 y 3)))))

  (defrule esk-same-as-chan
    (forall ((y z strd) (esk skey) (c c-0 chan))
	    (implies
	     (and (p "tpm-extend-enc" y 3)
		  (p "tpm-extend-enc" z 3)
		  (p "tpm-extend-enc" "esk" y esk)
		  (p "tpm-extend-enc" "esk" z esk)
		  (p "tpm-extend-enc" "c" y c)
		  (p "tpm-extend-enc" "c" z c-0))
	     (= c c-0)))))
```

---

## chan-perrig-song.scm

- **File Path**: `03_examples_scm/chan-perrig-song.scm`
- **Algebra & Herald**: `(herald perrig-song)` — `basic` algebra (`(defprotocol perrig-song basic ...)`).
- **Protocol & Purpose**: Models a two-party challenge-response protocol (`perrig-song`) where the middle message `(cat na nb a b)` is transmitted over a channel `c` while `na` and `nb` are sent in the clear. Tests four combinations of `(auth c)` and `(conf c)` on `init` and `resp` skeletons to show when CPSA must introduce a peer strand versus when the skeleton is already realized as-is.
- **Roles & Variables**:
  - `init`:
    - `(vars (na nb text) (a b name) (c chan))`
    - Trace: `(send na)`, `(recv c (cat na nb a b))`, `(send nb)`
  - `resp`:
    - `(vars (na nb text) (a b name) (c chan))`
    - Trace: `(recv na)`, `(send c (cat na nb a b))`, `(recv nb)`
- **Skeletons, Goals, Rules & Macros**:
  - 4 `(defskeleton perrig-song ...)` blocks:
    1. `(defstrand init 2 (na na) (c c))` with `(uniq-orig na)` and `(auth c)` (brings in a matching `resp` strand of height 2).
    2. `(defstrand resp 3 (nb nb) (c c))` with `(uniq-orig nb)` and `(conf c)` (brings in a matching `init` strand of height 3).
    3. `(defstrand init 2 (na na) (c c))` with `(uniq-orig na)` and `(conf c)` (realized as-is, since `conf` does not prevent adversary injection into `c`).
    4. `(defstrand resp 3 (nb nb) (c c))` with `(uniq-orig nb)` and `(auth c)` (realized as-is, since `auth` does not prevent adversary eavesdropping on `c`).
- **When to Reference This Example**: Reference this example as a clear contrast between `(auth c)` (only an honest role can send on `c`) and `(conf c)` (only an honest role can receive from `c`) on channel messages.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol perrig-song basic
  (defrole init
    (vars (na nb text) (a b name) (c chan))
    (trace
     (send na)
     (recv c (cat na nb a b))
     (send nb)))

  (defrole resp
    (vars (na nb text) (a b name) (c chan))
    (trace
     (recv na)
     (send c (cat na nb a b))
     (recv nb))))

(defskeleton perrig-song
  (vars (na nb text) (a b name) (c chan))
  (defstrand init 2 (na na) (c c))
  (uniq-orig na)
  (auth c))

(defskeleton perrig-song
  (vars (na nb text) (a b name) (c chan))
  (defstrand resp 3 (nb nb) (c c))
  (uniq-orig nb)
  (conf c))
```

---

## chan-unilateral.scm

- **File Path**: `03_examples_scm/chan-unilateral.scm`
- **Algebra & Herald**: `(herald chan-unilateral)` — `basic` algebra (`(defprotocol unilateral basic ...)`).
- **Protocol & Purpose**: Models unilateral authentication over a channel `ch` (`init` sends `n` over `ch` and receives `n` in the clear; `resp` receives `n` over `ch` and sends `n` in the clear). Systematically tests all 4 combinations of channel assumptions (none, `(auth ch)`, `(conf ch)`, and both `(auth ch)` + `(conf ch)`) from both the `init` perspective (using role-level `(uniq-orig n)`) and the `resp` perspective (using skeleton-level `(pen-non-orig n)`).
- **Roles & Variables**:
  - `init`:
    - `(vars (n text) (ch chan))`
    - Role-level assumptions: `(uniq-orig n)`
    - Trace: `(send ch n)`, `(recv n)`
  - `resp`:
    - `(vars (n text) (ch chan))`
    - Trace: `(recv ch n)`, `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - 8 `(defskeleton unilateral ...)` blocks:
    - First 4 test `(defstrand init 2 (ch ch))` with: no channel assumption, `(auth ch)`, `(conf ch)`, and `(auth ch)` + `(conf ch)`.
    - Next 4 test `(defstrand resp 2 (n n) (ch ch))` with `(pen-non-orig n)` and: no channel assumption, `(auth ch)`, `(conf ch)`, and `(auth ch)` + `(conf ch)`.
- **When to Reference This Example**: Reference this example when using `(pen-non-orig n)` (penetrator non-origination, meaning the adversary cannot guess/originate `n` on its own, though honest strands may originate it) together with `(auth ch)` and `(conf ch)` channel properties.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol unilateral basic
  (defrole init
     (vars (n text) (ch chan))
     (trace
      (send ch n)
      (recv n))
     (uniq-orig n))
  (defrole resp
     (vars (n text) (ch chan))
     (trace
      (recv ch n)			; bogus version was:  (cat ch n)
      (send n)))
  (comment "Unilateral protocol using channels with differing assumptions"))

(defskeleton unilateral
  (vars (n text) (ch chan))
  (defstrand resp 2 (n n) (ch ch))
  (pen-non-orig n)
  (auth ch)
  (conf ch))
```

---

## chan-yahalom-role-decl.scm

- **File Path**: `03_examples_scm/chan-yahalom-role-decl.scm`
- **Algebra & Herald**: `(herald "Yahalom Protocol Without Forwarding" (bound 15))` — `basic` algebra (`(defprotocol yahalom basic ...)`), with `(bound 15)`.
- **Protocol & Purpose**: Models the Yahalom key distribution protocol without key forwarding by replacing shared long-term symmetric keys with channels (`ch1`, `ch2`, `ch3` of sort `chan`) whose security properties (`(auth ch3)`, `(auth ch2)`, `(conf ch3 ch2)`) are declared directly inside the `defrole` definitions rather than in each `defskeleton`.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b c name) (n-a n-b text) (k skey) (ch3 chan))`
    - Role-level assumptions: `(auth ch3)`
    - Trace: `(send (cat a n-a))`, `(recv ch3 (cat a b k n-a n-b))`, `(send (enc n-b k))`
  - `resp`:
    - `(vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))`
    - Role-level assumptions: `(auth ch2)`
    - Trace: `(recv (cat a n-a))`, `(send ch1 (cat a b n-a n-b))`, `(recv ch2 (cat a b k))`, `(recv (enc n-b k))`
  - `serv`:
    - `(vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))`
    - Role-level assumptions: `(conf ch3 ch2)`, `(uniq-orig k)`
    - Trace: `(recv ch1 (cat a b n-a n-b))`, `(send ch3 (cat a b k n-a n-b))`, `(send ch2 (cat a b k))`
- **Skeletons, Goals, Rules & Macros**:
  - 8 `(defskeleton yahalom ...)` queries:
    1. `resp` height 4 with `(uniq-orig n-b)`
    2. `resp` height 4 with `(deflistener k)` and `(uniq-orig n-b)`
    3. `init` height 3 with `(uniq-orig n-a)`
    4. `init` height 3 with `(deflistener k)`
    5. `init` height 3 + `resp` height 3 sharing `k` with `(uniq-orig n-a)`
    6. `init` height 3 + `resp` height 4 sharing `k` with `(uniq-orig n-a)`
    7. `serv` height 3
    8. `serv` height 3 with `(deflistener k)`
- **When to Reference This Example**: Reference this example when you want channel trust properties (`(auth ...)` and `(conf ...)`) to apply automatically to every instance of a role by declaring them inside `(defrole ...)` rather than repeating them in every `(defskeleton ...)`.
- **Key S-Expression Excerpt**:
```scheme
(herald "Yahalom Protocol Without Forwarding" (bound 15))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey) (ch3 chan))
    (trace (send (cat a n-a))
	   (recv ch3 (cat a b k n-a n-b))
	   (send (enc n-b k)))
    (auth ch3))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))
    (trace (recv (cat a n-a))
	   (send ch1 (cat a b n-a n-b))
	   (recv ch2 (cat a b k))
	   (recv (enc n-b k)))
    (auth ch2))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
    (trace (recv ch1 (cat a b n-a n-b))
	   (send ch3 (cat a b k n-a n-b))
	   (send ch2 (cat a b k)))
    (conf ch3 ch2)
    (uniq-orig k)))
```

---

## chan-yahalom.scm

- **File Path**: `03_examples_scm/chan-yahalom.scm`
- **Algebra & Herald**: `(herald "Yahalom Protocol Without Forwarding" (bound 15))` — `basic` algebra (`(defprotocol yahalom basic ...)`), with `(bound 15)`.
- **Protocol & Purpose**: Companion to `chan-yahalom-role-decl.scm` modeling the same channel-based Yahalom protocol, but omitting `(auth ...)` and `(conf ...)` from the `defrole` definitions so they can be added incrementally in individual `defskeleton` queries to explore exactly which channel assumptions are needed at each step.
- **Roles & Variables**:
  - `init`: `(vars (a b c name) (n-a n-b text) (k skey) (ch3 chan))`, trace: `(send (cat a n-a))`, `(recv ch3 (cat a b k n-a n-b))`, `(send (enc n-b k))`
  - `resp`: `(vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))`, trace: `(recv (cat a n-a))`, `(send ch1 (cat a b n-a n-b))`, `(recv ch2 (cat a b k))`, `(recv (enc n-b k))`
  - `serv`: `(vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))`, `(uniq-orig k)`, trace: `(recv ch1 (cat a b n-a n-b))`, `(send ch3 (cat a b k n-a n-b))`, `(send ch2 (cat a b k))`
- **Skeletons, Goals, Rules & Macros**:
  - 8 `(defskeleton yahalom ...)` blocks demonstrating iterative analysis:
    1. `resp` height 4 with `(auth ch2)` and `(uniq-orig n-b)`
    2. `resp` height 4 + `serv` height 3 with `(precedes ((1 2) (0 2)))`, `(uniq-orig k n-b)`, `(auth ch2)`, `(conf ch2 ch3)`
    3. Adds `(auth ch2 ch1-0)` to unify `ch1-0 = ch1`
    4. Adds `(deflistener k)` to verify session key secrecy
    5. `init` height 3 with `(uniq-orig n-a)` and `(auth ch3)`
    6. `init` height 3 + `serv` height 2 with `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`, `(uniq-orig k n-a)`, `(auth ch3 ch1)`, `(conf ch3-0)`
    7. `serv` height 3 with `(auth ch1)` and `(conf ch2 ch3)`
    8. `serv` height 3 with `(deflistener k)`, `(auth ch1)`, and `(conf ch2 ch3)`
- **When to Reference This Example**: Reference this example when performing step-by-step interactive hypothesis refinement in CPSA—taking a shape output from one skeleton (with `(precedes ...)` and distinct channel variables `ch1`, `ch1-0`) and adding `(auth ...)` / `(conf ...)` assumptions in the next skeleton.
- **Key S-Expression Excerpt**:
```scheme
(defskeleton yahalom
  (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b name)
    (ch1 ch2 ch1-0 ch3 chan))
  (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (ch1 ch1)
    (ch2 ch2))
  (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (a a) (b b)
    (ch1 ch1-0) (ch2 ch2) (ch3 ch3))
  (deflistener k)
  (uniq-orig k n-b)
  (auth ch2 ch1-0)
  (conf ch2 ch3))
```

---

## commitment.scm

- **File Path**: `03_examples_scm/commitment.scm`
- **Algebra & Herald**: `(herald commitment)` — `basic` algebra (`(defprotocol commit basic ...)`).
- **Protocol & Purpose**: Models a cryptographic commitment auction protocol (`commit`) with a `bidder`, a malformed/alternative `bid-trash` role, and an `auctioneer`. Demonstrates the `(cheq sealed (hash a b n quote))` trace event inside `auctioneer`: the auctioneer first receives an opaque `sealed` value of sort `mesg` inside a signed bid `(recv (enc "bid" sealed (privk "sig" a)))`, issues a receipt, later receives the opening `(recv (cat n quote))`, and checks equality `(cheq sealed (hash a b n quote))` before signing the result. Note the inline comment explaining that `cheq` does not count as a separate node toward strand height (`auctioneer` has 4 `recv`/`send` events and full height 4).
- **Roles & Variables**:
  - `bidder`:
    - `(vars (a b name) (n data) (quote outcome text))`
    - Trace: `(send (enc "bid" (hash a b n quote) (privk "sig" a)))`, `(recv (enc "receipt" (hash a b n quote) (privk "sig" b)))`, `(send (cat n quote))`, `(recv (enc "result" a b n quote outcome (privk "sig" b)))`
  - `bid-trash`:
    - `(vars (a b name) (n data) (outcome trash text))`
    - Trace: `(send (enc "bid" (hash n trash) (privk "sig" a)))`, `(recv (enc "receipt" (hash n trash) (privk "sig" b)))`
  - `auctioneer`:
    - `(vars (a b name) (n data) (quote outcome text) (sealed mesg))`
    - Trace: `(recv (enc "bid" sealed (privk "sig" a)))`, `(send (enc "receipt" sealed (privk "sig" b)))`, `(recv (cat n quote))`, `(cheq sealed (hash a b n quote))`, `(send (enc "result" a b n quote outcome (privk "sig" b)))`
- **Skeletons, Goals, Rules & Macros**:
  - 3 `(defskeleton commit ...)` blocks:
    1. `(defstrand auctioneer 4 (a a))` (full height 4) with `(non-orig (privk "sig" a))`
    2. `(defstrand auctioneer 2 (a a))` (up to receipt send, before `sealed` is opened) with `(non-orig (privk "sig" a))`
    3. `(defstrand auctioneer 4 (sealed (hash a b n quote)) ...)` + `(defstrand bidder 1 ...)` with `(uniq-gen n)` and `(non-orig (privk "sig" a))`
- **When to Reference This Example**: Reference this example when modeling hash commitment / reveal protocols where a party receives an opaque commitment `sealed` (`mesg`), acts on it before knowing its preimage, and later verifies `(cheq sealed (hash ...))` after receiving the opening; also note that `cheq` does not increment strand height.
- **Key S-Expression Excerpt**:
```scheme
  (defrole auctioneer
    (vars (a b name) (n data) (quote outcome text) (sealed mesg))
    (trace
     (recv (enc "bid" sealed (privk "sig" a)))
     (send (enc "receipt" sealed (privk "sig" b)))
     (recv (cat n quote))
     (cheq sealed (hash a b n quote))
     (send (enc "result" a b n quote outcome (privk "sig" b))))))

(defskeleton commit
  (vars (a b name) (n data) (quote outcome text) (sealed mesg))
  (defstrand auctioneer 4 (a a))	; full height:  cheq doesn't
					; count separately
  (non-orig (privk "sig" a)))

(defskeleton commit
  (vars (a b name) (n data) (quote outcome text) (sealed mesg))
  (defstrand auctioneer 2 (a a))	; up to last recv
  (non-orig (privk "sig" a)))
```

---

## comp_test.scm

- **File Path**: `03_examples_scm/comp_test.scm`
- **Algebra & Herald**: `(herald "Main Example")` — `basic` algebra across three protocols (`main-ex-src`, `main-ex-tgt`, `main-ex-tgt-rule`).
- **Protocol & Purpose**: Models protocol refinement / composition across three protocol versions:
  - `main-ex-src`: A query-answer protocol where queriers (`qn`, `qy`) send a compound request `(cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c))` and responders (`an`, `ay`) treat the fourth component as an opaque `x` (`mesg`) and reply with `(enc "sorry" a b k)` or `(enc "data" d k)`.
  - `main-ex-tgt`: Refines `an` and `ay` so they forward `(enc y n i a x c)` to a backend server (`sn` or `sy`) that decrypts `(enc a b i ssn c)` and returns `n` (no) or `y` (yes) before `an`/`ay` reply to the querier.
  - `main-ex-tgt-rule`: Adds a `defrule src` encoding the shape analysis guarantee of `main-ex-src` directly as an axiom on `qn` and `an`.
- **Roles & Variables**:
  - In `main-ex-src`:
    - `qn`: `(vars (a b c akey) (i ssn text) (k skey))`, `(uniq-orig k)`, trace: `(send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))`, `(recv (enc "sorry" a b k))`
    - `qy`: `(vars (a b c akey) (i ssn d text) (k skey))`, `(uniq-orig k)`, trace: `(send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))`, `(recv (enc "data" d k))`
    - `an`: `(vars (a b c akey) (i text) (k skey) (x mesg))`, trace: `(recv (cat i a (enc (enc k b c i (invk a)) b) x))`, `(send (enc "sorry" a b k))`
    - `ay`: `(vars (a b c akey) (i d text) (k skey) (x mesg))`, `(uniq-orig d)`, trace: `(recv (cat i a (enc (enc k b c i (invk a)) b) x))`, `(send (enc "data" d k))`
  - In `main-ex-tgt` and `main-ex-tgt-rule`:
    - `qn`, `qy` (same as above)
    - `an`: `(vars (a b c akey) (i y n text) (k skey) (x mesg))`, `(uniq-orig y n)`, height 4 (adds sub-exchange `(send (enc y n i a x c))`, `(recv n)`)
    - `ay`: `(vars (a b c akey) (i y n d text) (k skey) (x mesg))`, `(uniq-orig d y n)`, height 4 (adds sub-exchange `(send (enc y n i a x c))`, `(recv y)`)
    - `sn`: `(vars (a b c akey) (i ssn y n text))`, trace: `(recv (enc y n i a (enc a b i ssn c) c))`, `(send n)`
    - `sy`: `(vars (a b c akey) (i ssn y n text))`, trace: `(recv (enc y n i a (enc a b i ssn c) c))`, `(send y)`
- **Skeletons, Goals, Rules & Macros**:
  - **Rule**: `src` in `main-ex-tgt-rule` using `forall`, `implies`, `exists`, `(non (invk ...))`, `(uniq k)`, and `(prec ...)`.
  - **Skeletons**: 5 `(defskeleton ...)` blocks (2 for `main-ex-src`, 2 for `main-ex-tgt`, 1 for `main-ex-tgt-rule`); the first skeleton embeds a commented `(comment (defgoal main-ex-src ...))` showing the shape analysis sentence from `cpsasas`.
- **When to Reference This Example**: Reference this example when modeling multi-tier protocol composition (where a middle tier forwards an encrypted blob `x` of sort `mesg` to a backend verifier) or when converting a shape analysis sentence (`defgoal`) into a compositional `defrule`.
- **Key S-Expression Excerpt**:
```scheme
  (defrule src
    (forall ((z strd) (i ssn text) (k skey) (a b c akey))
	    (implies
	     (and (p "qn" z 2) (p "qn" "i" z i) (p "qn" "ssn" z ssn)
		  (p "qn" "k" z k) (p "qn" "a" z a) (p "qn" "b" z b)
		  (p "qn" "c" z c) (non (invk a)) (non (invk b)) (non (invk c))
		  (uniq k))
	     (exists ((z-0 strd) (x mesg))
		     (and (p "an" z-0 4) (p "an" "x" z-0 x)
			  (p "an" "i" z-0 i) (p "an" "k" z-0 k)
			  (p "an" "a" z-0 a) (p "an" "b" z-0 b)
			  (p "an" "c" z-0 c) (prec z 0 z-0 0)
			  (prec z-0 3 z 1)))))))
```

---

## completeness-test.scm

- **File Path**: `03_examples_scm/completeness-test.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol completeness-test basic ...)`.
- **Protocol & Purpose**: Regression test for strand-ordering completeness in CPSA. An initiator (`init`) verifies the liveness of a responder (`resp`) via a two-message public-key challenge-response (`(send (enc a n (pubk b)))`, `(recv (enc n (pubk a)))`) and then sends `(enc "ok" s)` to a `probe` role waiting to hear `(recv (enc "ok" s))`. Compares skeletons that differ only in the order in which `defstrand init` and `defstrand probe` are listed.
- **Roles & Variables**:
  - `init`: `(vars (a b name) (n text) (s skey))`, trace: `(send (enc a n (pubk b)))`, `(recv (enc n (pubk a)))`, `(send (enc "ok" s))`
  - `resp`: `(vars (a b name) (n text))`, trace: `(recv (enc a n (pubk b)))`, `(send (enc n (pubk a)))`
  - `probe`: `(vars (s skey))`, trace: `(recv (enc "ok" s))`
- **Skeletons, Goals, Rules & Macros**:
  - 4 `(defskeleton completeness-test ...)` blocks, all with `(non-orig s (privk b))` and `(uniq-orig n)`:
    1. `(defstrand init 3 (b b) (n n))` then `(defstrand probe 1 (s s))`
    2. `(defstrand probe 1 (s s))` then `(defstrand init 3 (b b) (n n))`
    3. `(defstrand init 2 (b b) (n n))` then `(defstrand probe 1 (s s))`
    4. `(defstrand probe 1 (s s))` then `(defstrand init 2 (b b) (n n))`
- **When to Reference This Example**: Reference this example when testing multi-strand point-of-view skeletons (where one role signals completion to a secondary `probe` or observer role) or verifying that strand declaration order in `defskeleton` does not alter discovered shapes.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol completeness-test basic
 (defrole init
   (vars (a b name) (n text) (s skey))
   (trace
    (send (enc a n (pubk b)))
    (recv (enc n (pubk a)))
    (send (enc "ok" s))))
 (defrole resp
   (vars (a b name) (n text))
   (trace
    (recv (enc a n (pubk b)))
    (send (enc n (pubk a)))))
 (defrole probe
   (vars (s skey))
   (trace
    (recv (enc "ok" s)))))

(defskeleton completeness-test
  (vars (b name) (n text) (s skey))
  (defstrand init 3 (b b) (n n))
  (defstrand probe 1 (s s))
  (non-orig s (privk b))
  (uniq-orig n))
```

---

## crushing.scm

- **File Path**: `03_examples_scm/crushing.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol crushing basic ...)`.
- **Protocol & Purpose**: Designed to force CPSA to reduce ("crush") several strands simultaneously via hulling. An `init` strand sends `(enc n k)`, receives three signed/encrypted pairs `(enc n n1 (invk k))`, `(enc n n2 (invk k))`, `(enc n n3 (invk k))` from `adder` strands, sends `(enc n n1 n2 n3 (invk k))`, and receives `(enc n n1 n2 n3 n (invk k))` after cyclic permutation by `twister` strands (which map `(n1, n2, n3)` to `(n2, n3, n1)`).
- **Roles & Variables**:
  - `init`:
    - `(vars (k akey) (n n1 n2 n3 text))`
    - Role-level assumptions: `(uniq-orig n)`, `(non-orig (invk k))`
    - Trace: `(send (enc n k))`, `(recv (enc n n1 (invk k)))`, `(recv (enc n n2 (invk k)))`, `(recv (enc n n3 (invk k)))`, `(send (enc n n1 n2 n3 (invk k)))`, `(recv (enc n n1 n2 n3 n (invk k)))`
  - `adder`:
    - `(vars (k akey) (n new text))`
    - Role-level assumptions: `(uniq-orig new)`
    - Trace: `(recv (enc n k))`, `(send (enc n new (invk k)))`
  - `twister`:
    - `(vars (k akey) (n n1 n2 n3 text))`
    - Trace: `(recv (enc n n1 n2 n3 (invk k)))`, `(send (enc n n2 n3 n1 n (invk k)))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton crushing (vars (k akey) (n n1 n2 n3 text)) (defstrand init 6 (k k) (n n) (n1 n1) (n2 n2) (n3 n3)) (uniq-orig n1 n2 n3))`.
- **When to Reference This Example**: Reference this example when studying strand hulling, variable unification across cyclic permutations (`twister`), and how CPSA collapses multiple isomorphic `adder` strands when `n1`, `n2`, `n3` are forced equal.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol crushing basic
  (defrole init (vars (k akey) (n n1 n2 n3 text))
    (trace
	(send (enc n k))
      (recv (enc n n1 (invk k)))
      (recv (enc n n2 (invk k)))
      (recv (enc n n3 (invk k)))
      (send (enc n n1 n2 n3 (invk k)))
      (recv (enc n n1 n2 n3 n (invk k)))
    )
    (uniq-orig n)
    (non-orig (invk k))
  )
  (defrole adder (vars (k akey) (n new text))
    (trace
      (recv (enc n k))
      (send (enc n new (invk k)))
    )
    (uniq-orig new)
  )
  (defrole twister (vars (k akey) (n n1 n2 n3 text))
    (trace
       (recv (enc n n1 n2 n3 (invk k)))
       (send (enc n n2 n3 n1 n (invk k)))
    )
  )
)

(defskeleton crushing
  (vars (k akey) (n n1 n2 n3  text))
  (defstrand init 6 (k k) (n n) (n1 n1) (n2 n2) (n3 n3))
  (uniq-orig n1 n2 n3)
)
```

---

## dass_simple.scm

- **File Path**: `03_examples_scm/dass_simple.scm`
- **Algebra & Herald**: `(herald "Distributed Authentication Security Service Protocol Variants")` — `basic` algebra across two protocol variants (`dass-simple` and `dass+`).
- **Protocol & Purpose**: Models two simplified variants of the Distributed Authentication Security Service (DASS) protocol (`dass-simple` and `dass+`) where an initiator `a` certifies an ephemeral public key `kp` via `(enc a kp (privk a))` and signs the encrypted session key `(enc (enc k (pubk b)) (invk kp))`. Demonstrates the critical difference between placing `(non-orig (privk a))` only in the `defskeleton` (`dass-simple`, where responder `b` might interact with a compromised initiator in another session, failing to authenticate `a` to `b`) versus placing `(non-orig (privk a))` directly inside `(defrole resp ...)` (`dass+`, which constrains every responder instance to interact only with uncompromised initiators).
- **Roles & Variables**:
  - In `dass-simple`:
    - `init`: `(vars (a b name) (k skey) (ta text) (kp akey) (tb text))`, trace: `(send (cat (enc "init" ta k) (enc a kp (privk a)) (enc (enc k (pubk b)) (invk kp))))`, `(recv (enc "resp" tb k))`
    - `resp`: `(vars (a b name) (k skey) (ta text) (kp akey) (tb text))`, trace: `(recv (cat (enc "init" ta k) (enc a kp (privk a)) (enc (enc k (pubk b)) (invk kp))))`, `(send (enc "resp" tb k))`
  - In `dass+`:
    - `init`: identical to `dass-simple`
    - `resp`: identical to `dass-simple`, plus role-level `(non-orig (privk a))`
- **Skeletons, Goals, Rules & Macros**:
  - 2 active `(defskeleton ...)` blocks (one for `dass-simple`, one for `dass+`), both testing `(defstrand init 2 (a a) (b b) (k k) (kp kp) (ta ta) (tb tb))` with `(non-orig (privk a) (privk b) (invk kp))` and `(uniq-orig k kp)`.
  - Contains a trailing `(comment ...)` block with two legacy skeletons for `dass`.
- **When to Reference This Example**: Reference this example to understand the exact semantic difference between role-level `(non-orig ...)` and skeleton-level `(non-orig ...)`, or when modeling ephemeral signing keys `kp` certified by a long-term key `(privk a)`.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol dass+ basic
  (defrole init (vars (a b name) (k skey) (ta text) (kp akey) (tb text))
    (trace (send (cat (enc "init" ta k)
		      (enc a kp (privk a))
		      (enc (enc k (pubk b)) (invk kp))))
	   (recv (enc "resp" tb k))))
  (defrole resp (vars (a b name) (k skey) (ta text) (kp akey) (tb text))
    (trace (recv (cat (enc "init" ta k)
		      (enc a kp (privk a))
		      (enc (enc k (pubk b)) (invk kp))))
	   (send (enc "resp" tb k)))
    (non-orig (privk a)))
  (comment "In this version of the protocol ")
  (comment "b never interacts with a compromised initiator.")
  (comment "That is why a is properly authenticated to b."))

(defskeleton dass+
  (vars (a name) (b name) (k skey) (kp akey) (ta text)(tb text))
  (defstrand init 2 (a a) (b b) (k k) (kp kp) (ta ta) (tb tb))
  (non-orig (privk a) (privk b) (invk kp))
  (uniq-orig k kp))
```

---

## denning-sacco.scm

- **File Path**: `03_examples_scm/denning-sacco.scm`
- **Algebra & Herald**: `(herald "Denning-Sacco Protocol")` — `basic` algebra (`(defprotocol denning-sacco basic ...)`).
- **Protocol & Purpose**: Models the classic Denning-Sacco public-key key distribution protocol with a `keyserver` (`ks`). The initiator `a` requests certificates for `a` and `b` from `ks`, receives `(cat (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks)))`, and forwards those certificates together with the signed session key and timestamp `(enc a b k ta (privk a))` encrypted under `(pubk b)`.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b ks name) (k skey) (ta text))`
    - Trace:
      1. `(send (cat a b))`
      2. `(recv (cat (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks))))`
      3. `(send (enc (enc a b k ta (privk a)) (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks)) (pubk b)))`
  - `resp`:
    - `(vars (a b ks name) (k skey) (ta text))`
    - Trace: `(recv (enc (enc a b k ta (privk a)) (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks)) (pubk b)))`
  - `keyserver`:
    - `(vars (a b ks name))`
    - Trace: `(recv (cat a b))`, `(send (cat (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks))))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton denning-sacco (vars (a b ks name) (k skey)) (defstrand resp 1 (a a) (b b) (ks ks) (k k)) (non-orig (privk b) (privk a) (privk ks)) (uniq-orig k))`.
- **When to Reference This Example**: Reference this example when modeling three-party certificate directory / keyserver protocols where public key certificates `(enc a (pubk a) (privk ks))` are fetched and bundled into an encrypted session key transport message.
- **Key S-Expression Excerpt**:
```scheme
(herald "Denning-Sacco Protocol")

(defprotocol denning-sacco basic
  (defrole init (vars (a b ks name) (k skey) (ta text))
    (trace
     (send (cat a b))
     (recv (cat (enc b (pubk b) (privk ks))
		(enc a (pubk a) (privk ks))))
     (send (enc (enc a b k ta (privk a))
		(enc b (pubk b) (privk ks))
		(enc a (pubk a) (privk ks)) (pubk b)))))
  (defrole resp (vars (a b ks name) (k skey) (ta text))
    (trace
     (recv (enc (enc a b k ta (privk a))
		(enc b (pubk b) (privk ks))
		(enc a (pubk a) (privk ks)) (pubk b)))))
  (defrole keyserver (vars (a b ks name))
    (trace
     (recv (cat a b))
     (send (cat (enc b (pubk b) (privk ks))
		(enc a (pubk a) (privk ks)))))))

(defskeleton denning-sacco
  (vars (a b ks name) (k skey))
  (defstrand resp 1 (a a) (b b) (ks ks) (k k))
  (non-orig (privk b) (privk a) (privk ks))
  (uniq-orig k))
```

---

## deorig_contract.scm

- **File Path**: `03_examples_scm/deorig_contract.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol deorig-contract basic ...)`.
- **Protocol & Purpose**: Demonstrates a subtle incompleteness in CPSA related to "deorigination" during contraction steps. The `init` role originates two fresh values `(uniq-orig x1 x2)`, sends `(enc x1 k)` and `(enc x2 k)`, and expects `(enc x1 x2 k)`. However, `resp` receives `(enc y1 k)` and `(enc y2 k)` and sends `(enc y1 y3 k)` where `y3` appears for the first time in `resp`'s send event. For `resp` to satisfy `init`, a contraction must unify `y3 = y2 = x2`, which requires `y3` on `resp` to cease being an origination point ("deorigination") because `x2` already uniquely originates on `init` prior to `resp`'s second `recv`.
- **Roles & Variables**:
  - `init`:
    - `(vars (k akey) (x1 x2 text))`
    - Role-level assumptions: `(uniq-orig x1 x2)`, `(non-orig (invk k))`
    - Trace: `(send (enc x1 k))`, `(send (enc x2 k))`, `(recv (enc x1 x2 k))`
  - `resp`:
    - `(vars (k akey) (y1 y2 y3 text))`
    - Trace: `(recv (enc y1 k))`, `(recv (enc y2 k))`, `(send (enc y1 y3 k))`
- **Skeletons, Goals, Rules & Macros**:
  - Two `(defskeleton deorig-contract ...)` blocks:
    1. `(defskeleton deorig-contract (vars) (defstrand init 3))` (the initial point of view).
    2. `(defskeleton deorig-contract (vars (k akey) (x1 x2 text)) (defstrand init 3 (k k) (x1 x1) (x2 x2)) (defstrand resp 3 (k k) (y1 x1) (y2 x2) (y3 x2)) (precedes ((0 0) (1 0)) ((0 1) (1 1)) ((1 2) (0 2))))` (the expected realized skeleton where `y3` and `y2` are unified with `x2`).
- **When to Reference This Example**: Reference this example when debugging unexpected dead skeletons caused by unbound variables in a responder's `send` event (`y3`) that must unify with a previously received `uniq-orig` variable (`x2`) during cohort contraction.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol deorig-contract basic
  (defrole init (vars (k akey) (x1 x2 text))
     (trace
       (send (enc x1 k))
       (send (enc x2 k))
       (recv (enc x1 x2 k))
     )
     (uniq-orig x1 x2)
     (non-orig (invk k))
   )
   (defrole resp (vars (k akey) (y1 y2 y3 text))
     (trace
       (recv (enc y1 k))
       (recv (enc y2 k))
       (send (enc y1 y3 k))
     )
   )
)

(defskeleton deorig-contract
   (vars (k akey) (x1 x2 text))
   (defstrand init 3 (k k) (x1 x1) (x2 x2))
   (defstrand resp 3 (k k) (y1 x1) (y2 x2) (y3 x2))
   (precedes ((0 0) (1 0)) ((0 1) (1 1)) ((1 2) (0 2)))
)
```

---

## deorig_mesg.scm

- **File Path**: `03_examples_scm/deorig_mesg.scm`
- **Algebra & Herald**: `(herald deorig-mesg)` — `basic` algebra (`(defprotocol deorig-mesg basic ...)`).
- **Protocol & Purpose**: Minimal two-message demonstration of deorigination involving sort `mesg`. `init` sends `(enc x k)` and receives `x` (with `(uniq-orig x)` and `(non-orig (invk k))`), while `resp` receives an untyped `(x mesg)` and sends `(y text)`. For `resp` to satisfy `init`, `resp`'s received `x` must instantiate to `(enc z k)` and its sent `y` must instantiate to `z`, changing `z` from originating at `resp`'s send node to being received inside `(enc z k)` at `resp`'s recv node.
- **Roles & Variables**:
  - `init`: `(vars (k akey) (x text))`, `(uniq-orig x)`, `(non-orig (invk k))`, trace: `(send (enc x k))`, `(recv x)`
  - `resp`: `(vars (x mesg) (y text))`, trace: `(recv x)`, `(send y)`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton deorig-mesg ...)` blocks:
    1. `(defskeleton deorig-mesg (vars) (defstrand init 2))`
    2. `(defskeleton deorig-mesg (vars (k akey) (z text)) (defstrand init 2 (k k) (x z)) (defstrand resp 2 (x (enc z k)) (y z)) (precedes ((0 0) (1 0)) ((1 1) (0 1))))`
- **When to Reference This Example**: Reference this example to understand why a role that receives an unparsed `(x mesg)` and sends a separate variable `(y text)` cannot act as a general decryption oracle in CPSA without explicit variable binding between the received ciphertext and sent plaintext.
- **Key S-Expression Excerpt**:
```scheme
(herald deorig-mesg)

(defprotocol deorig-mesg basic
  (defrole init
    (vars (k akey) (x text))
    (trace (send (enc x k)) (recv x))
    (uniq-orig x)
    (non-orig (invk k)))
  (defrole resp
    (vars (x mesg) (y text))
    (trace (recv x) (send y))))

(defskeleton deorig-mesg (vars) (defstrand init 2))

(defskeleton deorig-mesg
  (vars (k akey) (z text))
  (defstrand init 2 (k k) (x z))
  (defstrand resp 2 (x (enc z k)) (y z))
  (precedes ((0 0) (1 0)) ((1 1) (0 1))))
```

---

## deorig_simple.scm

- **File Path**: `03_examples_scm/deorig_simple.scm`
- **Algebra & Herald**: `(herald deorig-simple)` — `basic` algebra (`(defprotocol deorig-simple basic ...)`).
- **Protocol & Purpose**: Demonstrates the same deorigination incompleteness as `deorig_contract.scm` in a simpler two-message exchange. `init` sends `(enc x k)` and expects `x` back, whereas `resp` receives `(enc x k)` and sends a distinct variable `y` (both of sort `text`). Although unifying `x = y = z` on `resp` produces a valid shape (shown in the second skeleton), `y` originates on `resp` until unified with `x`, causing standard augmentation to miss the shape.
- **Roles & Variables**:
  - `init`: `(vars (k akey) (x text))`, `(uniq-orig x)`, `(non-orig (invk k))`, trace: `(send (enc x k))`, `(recv x)`
  - `resp`: `(vars (k akey) (x y text))`, trace: `(recv (enc x k))`, `(send y)`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton deorig-simple ...)` blocks:
    1. `(defskeleton deorig-simple (vars) (defstrand init 2))`
    2. `(defskeleton deorig-simple (vars (k akey) (z text)) (defstrand init 2 (k k) (x z)) (defstrand resp 2 (k k) (x z) (y z)) (precedes ((0 0) (1 0)) ((1 1) (0 1))))`
- **When to Reference This Example**: Reference this example when diagnosing why a role must use the same variable name (e.g., `x` in both `(recv (enc x k))` and `(send x)`) if it is meant to forward or decrypt-and-return a received nonce, rather than declaring two distinct variables `x` and `y`.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol deorig-simple basic
  (defrole init
    (vars (k akey) (x text))
    (trace (send (enc x k)) (recv x))
    (uniq-orig x)
    (non-orig (invk k)))
  (defrole resp
    (vars (k akey) (x y text))
    (trace (recv (enc x k)) (send y))))

(defskeleton deorig-simple
  (vars)
  (defstrand init 2))

(defskeleton deorig-simple
  (vars (k akey) (z text))
  (defstrand init 2 (k k) (x z))
  (defstrand resp 2 (k k) (x z) (y z))
  (precedes ((0 0) (1 0)) ((1 1) (0 1))))
```

---

## dh-ca_hack.scm

- **File Path**: `03_examples_scm/dh-ca_hack.scm`
- **Algebra & Herald**: `(herald dhca (algebra basic) (bound 12))` — `basic` algebra (`(defprotocol dhca basic ...)`), with herald flags `(algebra basic)` and `(bound 12)`.
- **Protocol & Purpose**: Models a static Diffie-Hellman exchange with CA-certified long-term DH public values inside the `basic` crypto algebra using the `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))` encoding and two adversary computation roles (`CDHcalc1` and `CDHcalc2`). The `ca` role certifies a long-term DH public key `gz` (`akey`) while assuming `(non-orig (invk gz))` for the private exponent. If the adversary learns either `(invk gy)` or `(invk gx)`, it can invoke `CDHcalc1` or `CDHcalc2` to compute `(CDH gx gy dhkey)`.
- **Roles & Variables**:
  - `init`:
    - `(vars (gx h akey) (dhkey skey) (a b ca name) (n text))`
    - Role-level assumptions: `(non-orig (privk ca) dhkey)`
    - Trace: `(recv (enc gx a (privk ca)))`, `(send (cat gx (enc gx a (privk ca))))`, `(recv (cat h (enc h b (privk ca)) (enc n (CDH gx h dhkey))))`, `(send (enc "check" n (CDH gx h dhkey)))`
  - `resp`:
    - `(vars (gy h akey) (dhkey skey) (a b ca name) (n text))`
    - Role-level assumptions: `(non-orig (privk ca) dhkey)`
    - Trace: `(recv (enc gy b (privk ca)))`, `(recv (cat h (enc h a (privk ca))))`, `(send (cat gy (enc gy b (privk ca)) (enc n (CDH h gy dhkey))))`, `(recv (enc "check" n (CDH h gy dhkey)))`
  - `ca`:
    - `(vars (subject ca name) (gz akey))`
    - Role-level assumptions: `(non-orig (invk gz))`
    - Trace: `(send (enc gz subject (privk ca)))`
  - `CDHcalc1`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gx (invk gy)))`, `(send (CDH gx gy dhkey))`
  - `CDHcalc2`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gy (invk gx)))`, `(send (CDH gx gy dhkey))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macro**: `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))`
  - **Skeletons**: 4 `(defskeleton dhca ...)` queries:
    1. `(defstrand init 4)`
    2. `(defstrand resp 4 (n n))` with `(uniq-orig n)`
    3. `(defstrand resp 4 (n n))` with `(deflistener n)` and `(uniq-orig n)`
    4. Joint `init` height 4 + `resp` height 4 agreeing on `(gx, gy, ca, a, b, n, dhkey)` with `(uniq-orig n)`.
- **When to Reference This Example**: Reference this example when encoding Computational Diffie-Hellman (`CDH`) inside the `basic` algebra using `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))` and calculator roles `CDHcalc1`/`CDHcalc2` alongside CA-issued certificates.
- **Key S-Expression Excerpt**:
```scheme
(herald dhca (algebra basic) (bound 12))

(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))

(defprotocol dhca basic
  (defrole init (vars (gx h akey) (dhkey skey) (a b ca name) (n text))
    (trace
     (recv (enc gx a (privk ca)))
     (send (cat gx (enc gx a (privk ca))))
     (recv (cat h (enc h b (privk ca)) (enc n (CDH gx h dhkey))))
     (send (enc "check" n (CDH gx h dhkey))))
    (non-orig (privk ca) dhkey))
  (defrole ca (vars (subject ca name) (gz akey))
    (trace
     (send (enc gz subject (privk ca)) ))
    (non-orig (invk gz)))
  (defrole CDHcalc1 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gx (invk gy)))
    (send (CDH gx gy dhkey))
  ))
  (defrole CDHcalc2 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gy (invk gx)))
    (send (CDH gx gy dhkey))
  )))
```

---

## dh_encrypt_hack.scm

- **File Path**: `03_examples_scm/dh_encrypt_hack.scm`
- **Algebra & Herald**: `(herald dhencrypt (algebra basic))` — `basic` algebra (`(defprotocol dhencrypt basic ...)`), with herald flag `(algebra basic)`.
- **Protocol & Purpose**: Models an unauthenticated Diffie-Hellman key exchange followed by an encrypted-nonce challenge/response in the `basic` algebra using the `(CDH gx gy dhkey)` macro and calculator roles `CDHcalc1`/`CDHcalc2`. Shows how an unauthenticated DH exchange without certificates is vulnerable unless both `init` and `resp` are explicitly assumed to agree on `(gx, gy)` in the point-of-view skeleton.
- **Roles & Variables**:
  - `init`:
    - `(vars (gx h akey) (dhkey skey) (n text))`
    - Role-level assumptions: `(non-orig (invk gx) dhkey)`
    - Trace: `(send gx)`, `(recv (cat h (enc n (CDH gx h dhkey))))`, `(send (enc "check" n (CDH gx h dhkey)))`
  - `resp`:
    - `(vars (h gy akey) (dhkey skey) (n text))`
    - Role-level assumptions: `(non-orig (invk gy) dhkey)`, `(uniq-orig gy n)`
    - Trace: `(recv h)`, `(send (cat gy (enc n (CDH h gy dhkey))))`, `(recv (enc "check" n (CDH h gy dhkey)))`
  - `CDHcalc1`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gx (invk gy)))`, `(send (CDH gx gy dhkey))`
  - `CDHcalc2`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gy (invk gx)))`, `(send (CDH gx gy dhkey))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macro**: `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))`
  - **Skeletons**: 3 `(defskeleton dhencrypt ...)` queries:
    1. `init` height 3
    2. `resp` height 3
    3. `init` height 2 + `resp` height 3 sharing `(gx, gy, n)`
- **When to Reference This Example**: Reference this example as the minimal template for the `(CDH gx gy dhkey)` macro + `CDHcalc1`/`CDHcalc2` pattern in the `basic` algebra without CA certificates.
- **Key S-Expression Excerpt**:
```scheme
(herald dhencrypt (algebra basic))

(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))

(defprotocol dhencrypt basic
  (defrole init (vars (gx h akey) (dhkey skey) (n text))
    (trace
     (send gx)
     (recv (cat h (enc n (CDH gx h dhkey))))
     (send (enc "check" n (CDH gx h dhkey)))
    )
    (non-orig (invk gx) dhkey)
  )
  (defrole resp (vars (h gy akey) (dhkey skey) (n text))
    (trace
     (recv h)
     (send (cat gy (enc n (CDH h gy dhkey))))
     (recv (enc "check" n (CDH h gy dhkey)))
    )
    (non-orig (invk gy) dhkey)
    (uniq-orig gy n)
  )
  (defrole CDHcalc1 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gx (invk gy)))
    (send (CDH gx gy dhkey))
  ))
  (defrole CDHcalc2 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gy (invk gx)))
    (send (CDH gx gy dhkey))
  )))
```

---

## dh_group_sig.scm

- **File Path**: `03_examples_scm/dh_group_sig.scm`
- **Algebra & Herald**: `(herald "Signed group DH exchange (improved version)" (algebra diffie-hellman) (limit 100))` — `diffie-hellman` algebra (`(defprotocol dh_sig diffie-hellman ...)`), with herald flags `(algebra diffie-hellman)` and `(limit 100)`.
- **Protocol & Purpose**: Models an authenticated Diffie-Hellman exchange over a dynamically distributed DH subgroup generator `(exp (gen) alpha)`. A `group-init` role generates a fresh random exponent `(alpha rndx)` (`(uniq-gen alpha)`) and distributes `(cat "Group id" group (exp (gen) alpha))` over a confidential channel `group-dist`. The initiator (`init`) and responder (`resp`) receive the group generator over `(auth group-dist)` (modeling `alpha` as `(alpha expt)`), perform a signed DH exchange binding peer identities `a` and `b` and nonces `na`, `nb`, and verify possession of the shared secret `(exp (exp (exp (gen) alpha) y) x)` via a nonce challenge-response `(enc na nb (exp (exp (exp (gen) alpha) y) x))`.
- **Roles & Variables**:
  - `group-init`:
    - `(vars (alpha rndx) (group text) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen alpha)`, `(conf group-dist)`
    - Trace: `(send group-dist (cat "Group id" group (exp (gen) alpha)))`
  - `init`:
    - `(vars (x rndx) (y expt) (alpha expt) (group na nb text) (a b name) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen na x)`, `(auth group-dist)`
    - Trace:
      1. `(recv group-dist (cat "Group id" group (exp (gen) alpha)))`
      2. `(send (enc (exp (exp (gen) alpha) x) (privk a)))`
      3. `(recv (enc a (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b)))`
      4. `(send (enc "final" b na (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a)))`
      5. `(recv (enc na nb (exp (exp (exp (gen) alpha) y) x)))`
      6. `(send nb)`
  - `resp`:
    - `(vars (y rndx) (x expt) (alpha expt) (group na nb text) (a b name) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen nb y)`, `(auth group-dist)`
    - Trace:
      1. `(recv group-dist (cat "Group id" group (exp (gen) alpha)))`
      2. `(recv (enc (exp (exp (gen) alpha) x) (privk a)))`
      3. `(send (enc a (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b)))`
      4. `(recv (enc "final" b na (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a)))`
      5. `(send (enc na nb (exp (exp (exp (gen) alpha) x) y)))`
      6. `(recv nb)`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton dh_sig ...)` blocks:
    1. `(defstrand init 6 (a a) (b b))` with `(non-orig (privk b) (privk a))`
    2. `(defstrand resp 6 (a a) (b b))` with `(non-orig (privk a) (privk b))`
- **When to Reference This Example**: Reference this example when modeling Diffie-Hellman exchanges in the `diffie-hellman` algebra, especially when distinguishing own exponents (`rndx` with `uniq-gen`) from received peer/group exponents (`expt`), or when using nested exponentiation `(exp (exp (gen) alpha) x)` for custom DH groups.
- **Key S-Expression Excerpt**:
```scheme
(herald "Signed group DH exchange (improved version)"
	(algebra diffie-hellman)
	(limit 100))

(defprotocol dh_sig diffie-hellman
  (defrole group-init
    (vars (alpha rndx) (group text) (group-dist chan))
    (trace
     (send group-dist (cat "Group id" group
			   (exp (gen) alpha))))
    (uniq-gen alpha)
    (conf group-dist))
  
  (defrole init
    (vars (x rndx) (y expt) (alpha expt) (group na nb text)
	  (a b name) (group-dist chan))
    (trace
     (recv group-dist (cat "Group id" group
			   (exp (gen) alpha)))
     (send (enc (exp (exp (gen) alpha) x)
		(privk a)))
     (recv (enc a (exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk b)))
     (send (enc "final" b na
		(exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk a)))
     (recv (enc na nb
		(exp (exp (exp (gen) alpha) y)
		     x)))
     (send nb))
    (uniq-gen na x)
    (auth group-dist)))
```

---

## dh_group_sig_auth_failure.scm

- **File Path**: `03_examples_scm/dh_group_sig_auth_failure.scm`
- **Algebra & Herald**: `(herald "Signed group DH exchange (version with auth failure)" (algebra diffie-hellman) (limit 100))` — `diffie-hellman` algebra (`(defprotocol dh_sig diffie-hellman ...)`), with herald flags `(algebra diffie-hellman)` and `(limit 100)`.
- **Protocol & Purpose**: Vulnerable predecessor to `dh_group_sig.scm` that omits the peer identities `a` and `b` inside the signed DH messages (`(enc (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b))` and `(enc "final" (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a))`) and omits the subsequent shared-secret challenge-response. Demonstrates an authentication failure (unknown key-share / man-in-the-middle forwarding of signed DH shares) in the `diffie-hellman` algebra.
- **Roles & Variables**:
  - `group-init`:
    - `(vars (alpha rndx) (group text) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen alpha)`, `(conf group-dist)`
    - Trace: `(send group-dist (cat "Group id" group (exp (gen) alpha)))`
  - `init`:
    - `(vars (x rndx) (y expt) (alpha expt) (group text) (a b name) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen x)`, `(auth group-dist)`
    - Trace:
      1. `(recv group-dist (cat "Group id" group (exp (gen) alpha)))`
      2. `(send (enc (exp (exp (gen) alpha) x) (privk a)))`
      3. `(recv (enc (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b)))`
      4. `(send (enc "final" (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a)))`
  - `resp`:
    - `(vars (y rndx) (x expt) (alpha expt) (group text) (a b name) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen y)`, `(auth group-dist)`
    - Trace:
      1. `(recv group-dist (cat "Group id" group (exp (gen) alpha)))`
      2. `(recv (enc (exp (exp (gen) alpha) x) (privk a)))`
      3. `(send (enc (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b)))`
      4. `(recv (enc "final" (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton dh_sig ...)` blocks:
    1. `(defstrand init 4 (a a) (b b))` with `(non-orig (privk b) (privk a))`
    2. `(defstrand resp 4 (a a) (b b))` with `(non-orig (privk a) (privk b))`
- **When to Reference This Example**: Reference this example alongside `dh_group_sig.scm` to see how omitting peer identities (`a`, `b`) inside signed Diffie-Hellman transcripts leads to authentication failure in CPSA's `diffie-hellman` algebra.
- **Key S-Expression Excerpt**:
```scheme
  (defrole init
    (vars (x rndx) (y expt) (alpha expt) (group text)
	  (a b name) (group-dist chan))
    (trace
     (recv group-dist (cat "Group id" group
			   (exp (gen) alpha)))
     (send (enc (exp (exp (gen) alpha) x)
		(privk a)))
     (recv (enc (exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk b)))
     (send (enc "final" (exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk a))))
    (uniq-gen x)
    (auth group-dist))

(defskeleton dh_sig
  (vars (a b name))
  (defstrand init 4 (a a) (b b))
  (non-orig (privk b) (privk a))
)
```

---

## dh_mim_hack.scm

- **File Path**: `03_examples_scm/dh_mim_hack.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol dh_mim basic ...)`.
- **Protocol & Purpose**: Models an unauthenticated Diffie-Hellman key exchange followed by sending an encrypted nonce `(enc n (CDH gx gy dhkey))` in the `basic` algebra using the `(CDH gx gy dhkey)` macro and calculator roles `CDHcalc1`/`CDHcalc2`. Demonstrates a classic man-in-the-middle attack when the point-of-view skeleton requires agreement only on the encrypted plaintext `n` (`(precedes ((0 2) (1 2)))`) without binding `gx` and `gy` across `init` and `resp`.
- **Roles & Variables**:
  - `init`: `(vars (gx gy akey) (n text) (dhkey skey))`, `(uniq-orig n gx)`, `(non-orig (invk gx) dhkey)`, trace: `(send gx)`, `(recv gy)`, `(send (enc n (CDH gx gy dhkey)))`
  - `resp`: `(vars (gx gy akey) (n text) (dhkey skey))`, `(uniq-orig gy)`, `(non-orig (invk gy) dhkey)`, trace: `(recv gx)`, `(send gy)`, `(recv (enc n (CDH gx gy dhkey)))`
  - `CDHcalc1`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gx (invk gy)))`, `(send (CDH gx gy dhkey))`
  - `CDHcalc2`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gy (invk gx)))`, `(send (CDH gx gy dhkey))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macro**: `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))`
  - **Skeleton**: `(defskeleton dh_mim (vars (n text) (gx gy akey) (dhkey skey)) (defstrand init 3 (n n) (gx gx) (dhkey dhkey)) (defstrand resp 3 (n n) (gy gy) (dhkey dhkey)) (precedes ((0 2) (1 2))) (comment "Agreement on the encrypted text only"))`.
- **When to Reference This Example**: Reference this example when demonstrating a Diffie-Hellman man-in-the-middle attack in the `basic` algebra where `init` and `resp` agree on the payload `n` (`(precedes ((0 2) (1 2)))`) while the adversary substitutes its own DH half-keys via `CDHcalc1` and `CDHcalc2`.
- **Key S-Expression Excerpt**:
```scheme
(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))

(defprotocol dh_mim basic
  (defrole init
    (vars (gx gy akey) (n text) (dhkey skey))
    (trace (send gx) (recv gy) (send (enc n (CDH gx gy dhkey))))
    (uniq-orig n gx)
    (non-orig (invk gx) dhkey))
  (defrole resp
    (vars (gx gy akey) (n text) (dhkey skey))
    (trace (recv gx) (send gy) (recv (enc n (CDH gx gy dhkey))))
    (uniq-orig gy)
    (non-orig (invk gy) dhkey))
  (defrole CDHcalc1 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gx (invk gy)))
    (send (CDH gx gy dhkey))
  ))
  (defrole CDHcalc2 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gy (invk gx)))
    (send (CDH gx gy dhkey))
  ))
  (comment "Diffie-hellman key exchange followed by an encryption"))

(defskeleton dh_mim
  (vars (n text) (gx gy akey) (dhkey skey))
  (defstrand init 3 (n n) (gx gx) (dhkey dhkey))
  (defstrand resp 3 (n n) (gy gy) (dhkey dhkey))
  (precedes ((0 2) (1 2)))
  (comment "Agreement on the encrypted text only"))
```

---

## dhnsl_hack.scm

- **File Path**: `03_examples_scm/dhnsl_hack.scm`
- **Algebra & Herald**: `(herald "Diffie-Hellman enhanced Needham-Schroeder-Lowe Protocol" (algebra basic))` — `basic` algebra (`(defprotocol dhnsl basic ...)`), with herald flag `(algebra basic)`.
- **Protocol & Purpose**: Models a Diffie-Hellman enhanced Needham-Schroeder-Lowe (NSL) protocol in the `basic` algebra where DH public values (`gx`, `gy`, `gz` of sort `akey`) and CDH tokens `(CDH gy gx dhkey)` and `(CDH gz gx dhkey)` replace traditional nonces inside public-key encrypted messages.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b name) (h2 h3 gx akey) (dhkey skey))`
    - Role-level assumptions: `(uniq-orig gx)`, `(non-orig (invk gx) dhkey)`
    - Trace:
      1. `(send (enc gx a (pubk b)))`
      2. `(recv (enc h2 (CDH h2 gx dhkey) h3 b (pubk a)))`
      3. `(send (enc (CDH h3 gx dhkey) (pubk b)))`
  - `resp`:
    - `(vars (b a name) (h1 gy gz akey) (dhkey skey))`
    - Role-level assumptions: `(uniq-orig gy gz)`, `(non-orig (invk gy) (invk gz) dhkey)`
    - Trace:
      1. `(recv (enc h1 a (pubk b)))`
      2. `(send (enc gy (CDH gy h1 dhkey) gz b (pubk a)))`
      3. `(recv (enc (CDH gz h1 dhkey) (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macro**: `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))`
  - **Skeletons**: 2 `(defskeleton dhnsl ...)` queries:
    1. `(defstrand init 3 (a a) (b b) (h2 gy) (h3 gz) (gx gx))` with `(non-orig (privk b) (privk a))`
    2. `(defstrand resp 3 (a a) (b b) (h1 gx) (gy gy) (gz gz))` with `(non-orig (privk a))`
- **When to Reference This Example**: Reference this example when modeling hybrid public-key / Diffie-Hellman challenge-response protocols (such as DH-enhanced NSL) using the `(CDH ...)` macro in the `basic` algebra.
- **Key S-Expression Excerpt**:
```scheme
(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))

(defprotocol dhnsl basic
  (defrole init
    (vars (a b name) (h2 h3 gx akey) (dhkey skey))
    (trace
     (send (enc gx a (pubk b)))
     (recv (enc h2 (CDH h2 gx dhkey) h3 b (pubk a)))
     (send (enc (CDH h3 gx dhkey) (pubk b)))
    )
    (uniq-orig gx)
    (non-orig (invk gx) dhkey)
    (comment "X should be assumed to be freshly chosen per role")
  )
  (defrole resp
    (vars (b a name) (h1 gy gz akey) (dhkey skey))
    (trace
     (recv (enc h1 a (pubk b)))
     (send (enc gy (CDH gy h1 dhkey) gz b (pubk a)))
     (recv (enc (CDH gz h1 dhkey) (pubk b)))
    )
    (uniq-orig gy gz)
    (non-orig (invk gy) (invk gz) dhkey)
    (comment "Y and Z should be assumed to be freshly chosen per role")
  )
  (comment "Needham-Schroeder-Lowe DH challenge/responses in place of nonces")
)
```

---

## dhstatic-state.scm

- **File Path**: `03_examples_scm/dhstatic-state.scm`
- **Algebra & Herald**: `(herald dhstatic-state (algebra diffie-hellman) (bound 16))` — `diffie-hellman` algebra (`(defprotocol dhstatic-state diffie-hellman ...)`), with herald flags `(algebra diffie-hellman)` and `(bound 16)`.
- **Protocol & Purpose**: Models a static Diffie-Hellman key agreement protocol with PKI enrollment (`cert` and `get-cert`) where a principal's static DH private key `(ra rndx)` and certificate metadata are stored in a local state location `(static-key locn)` via `(stor static-key (cat "privkey" self ra serial ca))` and later retrieved via `(load static-key ...)` in `init` and `resp`. Also demonstrates role-level `(gen-st ...)`, role-level inequality facts `(facts (neq a b))`, and custom `(lang ...)` operators (`cert-req`, `cert`, `sig`) inside the `diffie-hellman` algebra.
- **Roles & Variables**:
  - `cert`:
    - `(vars (subj ca name) (serial data) (galpha mesg))`
    - Role-level assumptions: `(uniq-orig serial)`
    - Trace: `(recv (sig (cert-req subj galpha ca) (privk "sig" subj)))`, `(send (sig (cert subj galpha ca serial) (privk "sig" ca)))`
  - `get-cert`:
    - `(vars (self ca name) (serial data) (ra rndx) (static-key locn) (ignore mesg))`
    - Role-level assumptions: `(uniq-gen ra)`
    - Trace: `(send (sig (cert-req self (exp (gen) ra) ca) (privk "sig" self)))`, `(recv (sig (cert self (exp (gen) ra) ca serial) (privk "sig" ca)))`, `(load static-key ignore)`, `(stor static-key (cat "privkey" self ra serial ca))`
  - `init`:
    - `(vars (a b ca name) (ra rndx) (serial-a serial-b data) (alpha expt) (n text) (static-key locn))`
    - Role-level assumptions: `(uniq-orig n)`, `(gen-st (cat "privkey" a ra serial-a ca))`, `(facts (neq a b))`
    - Trace: `(load static-key (cat "privkey" a ra serial-a ca))`, `(recv (sig (cert b (exp (gen) alpha) ca serial-b) (privk "sig" ca)))`, `(send (enc n a b serial-a serial-b (exp (exp (gen) alpha) ra)))`, `(recv n)`
  - `resp`:
    - `(vars (a b ca name) (rb rndx) (serial-b serial-a data) (alpha expt) (n text) (static-key locn))`
    - Role-level assumptions: `(facts (neq a b))`, `(gen-st (cat "privkey" b rb serial-b ca))`
    - Trace: `(load static-key (cat "privkey" b rb serial-b ca))`, `(recv (sig (cert a (exp (gen) alpha) ca serial-a) (privk "sig" ca)))`, `(recv (enc n a b serial-a serial-b (exp (exp (gen) alpha) rb)))`, `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - **Language Declarations**: `(lang (cert-req (tupl 3)) (cert (tupl 4)) (sig sign))`
  - **Skeletons**: 2 `(defskeleton dhstatic-state ...)` queries:
    1. `(defstrand init 4 (ca ca) (b b))` with `(non-orig (privk "sig" ca) (privk "sig" b))`
    2. `(defstrand resp 4 (ca ca) (a a))` with `(non-orig (privk "sig" ca) (privk "sig" a))`
- **When to Reference This Example**: Reference this example when combining the `diffie-hellman` algebra with stateful `locn` storage (`load`/`stor` and role-level `(gen-st ...)`), role-level inequality constraints `(facts (neq a b))` (to prevent self-communication reflections in static DH), and custom `(lang ...)` operators.
- **Key S-Expression Excerpt**:
```scheme
  (defrole get-cert
    (vars (self ca name) (serial data) (ra rndx)
	  (static-key locn) (ignore mesg))
    (trace
     (send (sig (cert-req self (exp (gen) ra) ca) (privk "sig" self)))
     (recv (sig (cert self (exp (gen) ra) ca serial)
		(privk "sig" ca)))
     (load static-key ignore)
     (stor static-key (cat "privkey" self ra serial ca)))
    (uniq-gen ra)
    (comment "Get certified"))

  (defrole init
    (vars (a b ca name) (ra rndx) (serial-a serial-b data)
	  (alpha expt) (n text) (static-key locn))
    (trace
     (load static-key (cat "privkey" a ra serial-a ca))
     (recv (sig (cert b (exp (gen) alpha) ca serial-b)
		(privk "sig" ca)))
     (send (enc n a b serial-a serial-b (exp (exp (gen) alpha) ra)))
     (recv n))
    (uniq-orig n)
    (gen-st (cat "privkey" a ra serial-a ca))
    (facts (neq a b))
    (comment "Initiator is A"))

  (lang (cert-req (tupl 3))
	(cert (tupl 4))
	(sig sign)))
```

---

## disclosure.scm

- **File Path**: `03_examples_scm/disclosure.scm`
- **Algebra & Herald**: `(herald disclosure)` — `basic` algebra (`(defprotocol disc basic ...)`).
- **Protocol & Purpose**: Illustrates a protocol (`disc`) where an initiator (`init`) uses a key `k` declared `(pen-non-orig k)` to encrypt `(enc a b n k)`, receives `n` back, and then discloses `k` in its third step `(send k)`. Because `k` is only `pen-non-orig` (not `non-orig`, since `init` itself originates `k` at step 3), an `init` strand of height 2 can be satisfied in two distinct ways: either by an honest `resp` strand, or by the adversary obtaining `k` from a completed height-3 `init` strand in another session. Demonstrates how CPSA introduces and generalizes listeners during shape analysis.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b name) (k skey) (n text))`
    - Role-level assumptions: `(pen-non-orig k)`
    - Trace: `(send (enc a b n k))`, `(recv n)`, `(send k)`
  - `resp`:
    - `(vars (a b name) (k skey) (n text))`
    - Trace: `(recv (enc a b n k))`, `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton disc (vars (n text)) (defstrand init 2 (n n)) (uniq-orig n))`.
- **When to Reference This Example**: Reference this example when modeling deliberate key disclosure (e.g., TESLA or delayed key release protocols) where a symmetric key `k` is eventually transmitted in plaintext by an honest role (`(send k)`), requiring `(pen-non-orig k)` instead of `(non-orig k)` so the role's own key emission does not violate non-origination.
- **Key S-Expression Excerpt**:
```scheme
(herald disclosure)

(defprotocol disc basic
  (defrole init
    (vars (a b name) (k skey) (n text))
    (trace
     (send (enc a b n k))
     (recv n)
     (send k))
    (pen-non-orig k))

  (defrole resp
    (vars (a b name) (k skey) (n text))
    (trace
     (recv (enc a b n k))
     (send n))))

(defskeleton disc
  (vars (n text))
  (defstrand init 2 (n n))
  (uniq-orig n))
```

---

## doorsep.scm

- **File Path**: `03_examples_scm/doorsep.scm`
- **Algebra & Herald**: `(herald doorsep (comment "Door Simple Example Protocol"))` — `basic` algebra (`(defprotocol doorsep basic ...)`).
- **Protocol & Purpose**: Models the Door Simple Example Protocol (`doorsep`) from the CPSA Primer using unnamed asymmetric keys (`d p akey`). A `person` sends a fresh session key `k` signed with `(invk p)` and encrypted under `d` (`(enc (enc k (invk p)) d)`), the `door` replies with a fresh token `t` encrypted under `k` (`(enc t k)`), and the `person` returns `t` in the clear. Includes a `defrule trust` stating that if an uncompromised `person` (`(non (invk p))`) initiates a session with door key `d`, then `d`'s private key is also uncompromised (`(non (invk d))`).
- **Roles & Variables**:
  - `person`:
    - `(vars (d p akey) (k skey) (t text))`
    - Role-level assumptions: `(uniq-orig k)`
    - Trace: `(send (enc (enc k (invk p)) d))`, `(recv (enc t k))`, `(send t)`
  - `door`:
    - `(vars (d p akey) (k skey) (t text))`
    - Role-level assumptions: `(uniq-orig t)`
    - Trace: `(recv (enc (enc k (invk p)) d))`, `(send (enc t k))`, `(recv t)`
- **Skeletons, Goals, Rules & Macros**:
  - **Rule**: `trust` (`(forall ((z strd) (p d akey)) (implies (and (p "person" z 1) (p "person" "p" z p) (p "person" "d" z d) (non (invk p))) (non (invk d))))`).
  - **Skeleton**: `(defskeleton doorsep (vars (p akey)) (defstrand door 3 (p p)) (non-orig (invk p)) (comment "Analyze from the doors's perspective"))`.
- **When to Reference This Example**: Reference this example as the canonical, minimal introduction to writing a `defrule` trust axiom (`(implies (and (p "person" z 1) ... (non (invk p))) (non (invk d)))`) that prevents man-in-the-middle key substitution in a two-party protocol.
- **Key S-Expression Excerpt**:
```scheme
(herald doorsep (comment "Door Simple Example Protocol"))

(defprotocol doorsep basic
  (defrole person
    (vars (d p akey) (k skey) (t text))
    (trace
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t))
    (uniq-orig k))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t))
    (uniq-orig t))
  (defrule trust
    (forall ((z strd) (p d akey))
	    (implies
	     (and (p "person" z 1)
		  (p "person" "p" z p)
		  (p "person" "d" z d)
		  (non (invk p)))
	     (non (invk d))))
    (comment "The trust rule"))
  (comment "Doorsep protocol using unnamed asymmetric keys"))

(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (comment "Analyze from the doors's perspective"))
```

---

## doorsep2invk.scm

- **File Path**: `03_examples_scm/doorsep2invk.scm`
- **Algebra & Herald**: `(herald doorsep2invk (comment "Door Simple Example Protocol"))` — `basic` algebra (`(defprotocol doorsep basic ...)`).
- **Protocol & Purpose**: Variant of `doorsep` with roles named `init` and `resp` and a single `(defgoal doorsep ...)` testing a formula where the `peer` / `self` parameter is instantiated with an inverted key `(invk akey+3)` (`(p "resp" "peer" z (invk akey+3))` and `(non akey+3)`) and trivial conclusion `(and)`.
- **Roles & Variables**:
  - `init`:
    - `(vars (self peer akey) (skey skey) (data text))`
    - Role-level assumptions: `(uniq-orig skey)`
    - Trace: `(send (enc (enc skey (invk self)) peer))`, `(recv (enc data skey))`, `(send data)`
  - `resp`:
    - `(vars (self peer akey) (skey skey) (data text))`
    - Role-level assumptions: `(uniq-orig data)`
    - Trace: `(recv (enc (enc skey (invk peer)) self))`, `(send (enc data skey))`, `(recv data)`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defgoal doorsep ...)` using `forall`, `implies`, `and`, `p`, `prec`, `non`, and `uniq-at`, with empty conjunction `(and)` as conclusion.
- **When to Reference This Example**: Reference this example when examining how `defgoal` handles involutive `akey` expressions where `(invk akey+3)` is bound to a role parameter and `(non akey+3)` asserts non-origination of its inverse.
- **Key S-Expression Excerpt**:
```scheme
(herald doorsep2invk (comment "Door Simple Example Protocol"))

(defprotocol doorsep basic
  (defrole init
    (vars (self peer akey) (skey skey) (data text))
    (trace (send (enc (enc skey (invk self)) peer))
      (recv (enc data skey)) (send data))
    (uniq-orig skey))
  (defrole resp
    (vars (self peer akey) (skey skey) (data text))
    (trace (recv (enc (enc skey (invk peer)) self))
      (send (enc data skey)) (recv data))
    (uniq-orig data))
  (comment "Doorsep's protocol using unnamed asymmetric keys"))

(defgoal doorsep
  (forall
    ((text+0 text) (skey+0 skey) (akey+1 akey+0 akey+3 akey)
     (z z-0 strd))
    (implies
      (and (p "resp" z 3) (p "init" z-0 1) (p "resp" "data" z text+0)
        (p "resp" "skey" z skey+0) (p "resp" "self" z akey+1)
        (p "resp" "peer" z (invk akey+3)) (p "init" "skey" z-0 skey+0)
        (p "init" "self" z-0 (invk akey+3)) (p "init" "peer" z-0 akey+0)
        (prec z-0 0 z 0) (non akey+3) (non (invk akey+0))
        (uniq-at skey+0 z-0 0) (uniq-at text+0 z 1))
      (and))))
```

---

## encsig.scm

- **File Path**: `03_examples_scm/encsig.scm`
- **Algebra & Herald**: `(herald "Encrypted Signed Message Example" (comment "Shows examples of key usage of asymmetric keys"))` — `basic` algebra (`(defprotocol mult-keys-enc-sig basic ...)`).
- **Protocol & Purpose**: Demonstrates how to separate encryption key pairs from signature key pairs for the same principal using string-tagged `(pubk "enc" b)` / `(privk "enc" b)` and `(pubk "sig" a)` / `(privk "sig" a)` in an encrypt-then-sign challenge-response protocol (`mult-keys-enc-sig`). Explores how responder authentication depends on whether `a`'s signature key `(privk "sig" a)`, encryption key `(privk "enc" a)`, or both are assumed `non-orig`.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b name) (n1 n2 text))`
    - Trace:
      1. `(send (enc (enc n1 a (pubk "enc" b)) (privk "sig" a)))`
      2. `(recv (enc (enc n1 n2 (pubk "enc" a)) (privk "sig" b)))`
      3. `(send (enc (enc n2 (pubk "enc" b)) (privk "sig" a)))`
  - `resp`:
    - `(vars (b a name) (n2 n1 text))`
    - Trace:
      1. `(recv (enc (enc n1 a (pubk "enc" b)) (privk "sig" a)))`
      2. `(send (enc (enc n1 n2 (pubk "enc" a)) (privk "sig" b)))`
      3. `(recv (enc (enc n2 (pubk "enc" b)) (privk "sig" a)))`
- **Skeletons, Goals, Rules & Macros**:
  - 4 `(defskeleton mult-keys-enc-sig ...)` queries:
    1. `init` height 3 with `(non-orig (privk "enc" a) (privk "sig" a) (privk "sig" b))` and `(uniq-orig n1)`
    2. `resp` height 3 trusting only `a`'s signature key: `(non-orig (privk "sig" a))` and `(uniq-orig n2)`
    3. `resp` height 3 trusting only `a`'s encryption key: `(non-orig (privk "enc" a))` and `(uniq-orig n2)`
    4. `resp` height 3 trusting both of `a`'s keys: `(non-orig (privk "sig" a) (privk "enc" a))` and `(uniq-orig n2)`
- **When to Reference This Example**: Reference this example whenever an RFC or protocol uses distinct public/private key pairs per principal for encryption vs. signing—modeled in CPSA via two-argument `(pubk "enc" a)` / `(privk "enc" a)` and `(pubk "sig" a)` / `(privk "sig" a)`.
- **Key S-Expression Excerpt**:
```scheme
(herald "Encrypted Signed Message Example"
   (comment "Shows examples of key usage of asymmetric keys"))

(defprotocol mult-keys-enc-sig basic
   (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc (enc n1 a (pubk "enc" b)) (privk "sig" a)))
     (recv (enc (enc n1 n2 (pubk "enc" a)) (privk "sig" b)))
     (send (enc (enc n2 (pubk "enc" b)) (privk "sig" a)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc (enc n1 a (pubk "enc" b)) (privk "sig" a)))
     (send (enc (enc n1 n2 (pubk "enc" a)) (privk "sig" b)))
     (recv (enc (enc n2 (pubk "enc" b)) (privk "sig" a))))))

;;; The responder point-of-view trusting both of a's keys
(defskeleton mult-keys-enc-sig
  (vars (a b name) (n2 text))
  (defstrand resp 3 (a a) (b b) (n2 n2))
  (non-orig (privk "sig" a) (privk "enc" a))
  (uniq-orig n2))
```

---

## envelope.scm

- **File Path**: `03_examples_scm/envelope.scm`
- **Algebra & Herald**: `(herald "Envelope Protocol" (bound 15))` — `basic` algebra (`(defprotocol envelope basic ...)` repeated 3 times with progressively stronger rule sets), with `(bound 15)`.
- **Protocol & Purpose**: Non-channel counterpart to `chan-envelope.scm`. Models the TPM Envelope Protocol by encoding the TPM's current PCR register value as a message encrypted under a hashed secret key `(enc current-value (hash pcrkey))` with `(non-orig pcrkey)` (where hashing `pcrkey` prevents key confusion with the encrypted session key `esk`). Evaluates three rule sets (empty, `ordered-extends`, and `ordered-extends` + `esk-same-as-pcrkey`) across the same three listener scenarios (`v`, `(refuse n v k aik)`, and both).
- **Roles & Variables**:
  - Defined inside `(defmacro (roles) (^ ...))`:
    - `tpm-power-on`: `(vars (pcrkey skey))`, `(non-orig pcrkey)`, trace: `(recv "power on")`, `(send (enc "0" (hash pcrkey)))`
    - `tpm-extend`: `(vars (value current-value mesg) (pcrkey skey))`, `(non-orig pcrkey)`, trace: `(recv (cat "extend" value))`, `(recv (enc current-value (hash pcrkey)))`, `(send (enc (hash current-value value) (hash pcrkey)))`, `(send "ext ok")`
    - `tpm-extend-enc`: `(vars (value current-value mesg) (pcrkey esk skey))`, `(non-orig pcrkey esk)`, trace: `(recv (enc "extend" value esk))`, `(recv (enc current-value (hash pcrkey)))`, `(send (enc (hash current-value value) (hash pcrkey)))`, `(send "ext ok")`
    - `tpm-quote`: `(vars (nonce current-value mesg) (pcrkey skey) (aik akey))`, `(non-orig aik pcrkey)`, trace: `(recv (cat "quote" nonce))`, `(recv (enc current-value (hash pcrkey)))`, `(send (enc "quote" current-value nonce aik))`
    - `tpm-create-key`: `(vars (k aik akey) (pcrval mesg) (esk skey))`, `(uniq-orig k)`, `(non-orig (invk k) aik esk)`, trace: `(recv (enc "create key" pcrval esk))`, `(send (enc "created" k pcrval aik))`
    - `tpm-decrypt`: `(vars (m pcrvals mesg) (k aik akey) (pcrkey skey))`, `(non-orig aik pcrkey)`, trace: `(recv (cat "decrypt" (enc m k)))`, `(recv (enc "created" k pcrvals aik))`, `(recv (enc pcrvals (hash pcrkey)))`, `(send m)`
    - `alice`: `(vars (n v data) (esk skey) (k aik akey))`, `(uniq-orig n v)`, `(non-orig aik esk)`, trace: `(send (enc "extend" n esk))`, `(send (enc "create key" (hash (hash "0" n) "obtain") esk))`, `(recv (enc "created" k (hash (hash "0" n) "obtain") aik))`, `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: `(defmacro (refuse n v k aik) ...)` and `(defmacro (roles) (^ ...))`.
  - **Rules**: `ordered-extends` (forces linear ordering on `tpm-extend` strands sharing `pcrkey`) and `esk-same-as-pcrkey` (forces `(= pcrkey pcrkey-0)` when two `tpm-extend-enc` strands share `esk`).
  - **Skeletons**: 9 `(defskeleton envelope ...)` queries (3 per protocol block).
- **When to Reference This Example**: Reference this example when modeling state-carrying encrypted tokens `(enc current-value (hash pcrkey))` without `locn` or `chan`, using `defrule` axioms to enforce linear state updates (`(or (= y z) (prec y 2 z 3) (prec z 2 y 3))`).
- **Key S-Expression Excerpt**:
```scheme
(defprotocol envelope basic
  (roles)

  (defrule ordered-extends
    (forall ((y z strd) (pcrkey skey))
	    (implies
	     (and (p "tpm-extend" y 3)
		  (p "tpm-extend" z 3)
		  (p "tpm-extend" "pcrkey" y pcrkey)
		  (p "tpm-extend" "pcrkey" z pcrkey))
	     (or (= y z)
		 (prec y 2 z 3)
		 (prec z 2 y 3)))))

  (defrule esk-same-as-pcrkey
    (forall ((y z strd) (esk pcrkey pcrkey-0 skey))
	    (implies
	     (and (p "tpm-extend-enc" y 3)
		  (p "tpm-extend-enc" z 3)
		  (p "tpm-extend-enc" "esk" y esk)
		  (p "tpm-extend-enc" "esk" z esk)
		  (p "tpm-extend-enc" "pcrkey" y pcrkey)
		  (p "tpm-extend-enc" "pcrkey" z pcrkey-0))
	     (= pcrkey pcrkey-0)))))
```

---

## epmo-hash.scm

- **File Path**: `03_examples_scm/epmo-hash.scm`
- **Algebra & Herald**: `(herald "Electronic Purchase with Money Order Protocol with Key Hashing" (comment "Annotated with trust management formulas"))` — `basic` algebra (`(defprotocol epmo basic ...)`).
- **Protocol & Purpose**: Models the Electronic Purchase with Money Order (`epmo`) protocol between a `bank` (`b`), `customer` (`c`), and `merchant` (`m`), using CPSA's built-in `(hash ...)` operator inside signed money orders `(enc (hash c nc nb nm price) (privk b))` and merchant endorsements `(enc (hash b nb nm) (privk m))`. Includes role-level `(annotations ...)` with trust-management formulas (`says`, `transfer`, `ship`) attached to specific node indices.
- **Roles & Variables**:
  - `bank`:
    - `(vars (b c m name) (nc nm nb data) (price text))`
    - Role-level assumptions & annotations: `(uniq-orig nb)`, `(annotations b (1 ...) (2 ...))`
    - Trace:
      1. `(recv (enc c nc nm price (pubk b)))`
      2. `(send (cat (enc (hash c nc nb nm price) (privk b)) (enc nc nb (pubk c))))`
      3. `(recv (enc (hash b nb nm) (privk m)))`
  - `customer`:
    - `(vars (b c m name) (nb nc nm data) (goods price text))`
    - Role-level assumptions & annotations: `(uniq-orig nc)`, `(annotations c (1 ...) (3 ...) (4 ...))`
    - Trace:
      1. `(send (enc c nc goods price (pubk m)))`
      2. `(recv (enc nc nm m goods price (pubk c)))`
      3. `(send (enc c nc nm price (pubk b)))`
      4. `(recv (cat (enc (hash c nc nb nm price) (privk b)) (enc nc nb (pubk c))))`
      5. `(send (cat (enc (hash c nc nb nm price) (privk b)) nb))`
  - `merchant`:
    - `(vars (b c m name) (nb nc nm data) (goods price text))`
    - Role-level assumptions & annotations: `(uniq-orig nm)`, `(annotations m (1 ...) (2 ...) (3 ...))`
    - Trace:
      1. `(recv (enc c nc goods price (pubk m)))`
      2. `(send (enc nc nm m goods price (pubk c)))`
      3. `(recv (cat (enc (hash c nc nb nm price) (privk b)) nb))`
      4. `(send (enc (hash b nb nm) (privk m)))`
- **Skeletons, Goals, Rules & Macros**:
  - 3 `(defskeleton epmo ...)` queries testing `customer` height 5, `bank` height 3, and `merchant` height 4, each with `(non-orig (privk b) (privk c) (privk m))`.
- **When to Reference This Example**: Reference this example when modeling three-party e-commerce / payment protocols using `(hash ...)` inside digital signatures or when attaching trust-management `(annotations <principal> (<node-index> <formula>) ...)` to roles.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol epmo basic
  (defrole bank
    (vars (b c m name) (nc nm nb data) (price text))
    (trace
     (recv (enc c nc nm price (pubk b)))
     (send (cat (enc (hash c nc nb nm price) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (hash b nb nm) (privk m))))
    (uniq-orig nb)
    (annotations b
      (1
        (implies
          (and (forall ((pm name)) (says c (transfer b price pm nm)))
            (forall ((pm name)) (says pm (transfer b price pm nm))))
          (forall ((pm name)) (transfer b price pm nm))))
      (2
        (and (says c (transfer b price m nm))
          (says m (transfer b price m nm))))))
```

---

## epmo-key-hash.scm

- **File Path**: `03_examples_scm/epmo-key-hash.scm`
- **Algebra & Herald**: `(herald "Electronic Purchase with Money Order Protocol with Key Hashing" (comment "Annotated with trust management formulas"))` — `basic` algebra (`(defprotocol epmo basic ...)`).
- **Protocol & Purpose**: Variant of `epmo-hash.scm` that models hashing via two-argument `enc` with a string literal `"hash"` (`(enc "hash" (cat c nc nb nm price))` and `(enc "hash" (cat b nb nm))`) instead of the unary `(hash ...)` operator, while preserving the same `bank`, `customer`, and `merchant` roles and trust-management `(annotations ...)`.
- **Roles & Variables**:
  - `bank`: `(vars (b c m name) (nc nm nb data) (price text))`, `(uniq-orig nb)`, `(annotations b (1 ...) (2 ...))`, trace uses `(enc (enc "hash" (cat c nc nb nm price)) (privk b))` and `(enc (enc "hash" (cat b nb nm)) (privk m))`
  - `customer`: `(vars (b c m name) (nb nc nm data) (goods price text))`, `(uniq-orig nc)`, `(annotations c (1 ...) (3 ...) (4 ...))`
  - `merchant`: `(vars (b c m name) (nb nc nm data) (goods price text))`, `(uniq-orig nm)`, `(annotations m (1 ...) (2 ...) (3 ...))`
- **Skeletons, Goals, Rules & Macros**:
  - 3 `(defskeleton epmo ...)` queries testing `customer` height 5, `bank` height 3, and `merchant` height 4 with `(non-orig (privk b) (privk c) (privk m))`.
- **When to Reference This Example**: Reference this example alongside `epmo-hash.scm` and `epmo.scm` to compare older/alternative CPSA idioms for hashing (`(enc "hash" (cat ...))` vs. `(hash ...)`).
- **Key S-Expression Excerpt**:
```scheme
(defprotocol epmo basic
  (defrole bank
    (vars (b c m name) (nc nm nb data) (price text))
    (trace
     (recv (enc c nc nm price (pubk b)))
     (send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (enc "hash" (cat b nb nm)) (privk m))))
    (uniq-orig nb)
    (annotations b
      (1
        (implies
          (and (forall ((pm name)) (says c (transfer b price pm nm)))
            (forall ((pm name)) (says pm (transfer b price pm nm))))
          (forall ((pm name)) (transfer b price pm nm))))
      (2
        (and (says c (transfer b price m nm))
          (says m (transfer b price m nm))))))
```

---

## epmo.scm

- **File Path**: `03_examples_scm/epmo.scm`
- **Algebra & Herald**: `(herald "Electronic Purchase with Money Order Protocol" (comment "Annotated with trust management formulas"))` — `basic` algebra (`(defprotocol epmo basic ...)`).
- **Protocol & Purpose**: Original formulation of the Electronic Purchase with Money Order (`epmo`) protocol that models cryptographic hashing as encryption under a public key variable `(hash akey)` whose inverse is uncompromised (`(non-orig (invk hash))`). Each role (`bank`, `customer`, `merchant`) declares `(hash akey)` in `(vars ...)` and `(non-orig (invk hash))` in the role body, writing `(enc c nc nb nm price hash)` and `(enc b nb nm hash)`.
- **Roles & Variables**:
  - `bank`:
    - `(vars (b c m name) (hash akey) (nc nm nb data) (price text))`
    - Role-level assumptions & annotations: `(non-orig (invk hash))`, `(uniq-orig nb)`, `(annotations b (1 ...) (2 ...))`
    - Trace: `(recv (enc c nc nm price (pubk b)))`, `(send (cat (enc (enc c nc nb nm price hash) (privk b)) (enc nc nb (pubk c))))`, `(recv (enc (enc b nb nm hash) (privk m)))`
  - `customer`:
    - `(vars (b c m name) (hash akey) (nb nc nm data) (goods price text))`
    - Role-level assumptions & annotations: `(non-orig (invk hash))`, `(uniq-orig nc)`, `(annotations c (1 ...) (3 ...) (4 ...))`
    - Trace: `(send (enc c nc goods price (pubk m)))`, `(recv (enc nc nm m goods price (pubk c)))`, `(send (enc c nc nm price (pubk b)))`, `(recv (cat (enc (enc c nc nb nm price hash) (privk b)) (enc nc nb (pubk c))))`, `(send (cat (enc (enc c nc nb nm price hash) (privk b)) nb))`
  - `merchant`:
    - `(vars (b c m name) (hash akey) (nb nc nm data) (goods price text))`
    - Role-level assumptions & annotations: `(non-orig (invk hash))`, `(uniq-orig nm)`, `(annotations m (1 ...) (2 ...) (3 ...))`
    - Trace: `(recv (enc c nc goods price (pubk m)))`, `(send (enc nc nm m goods price (pubk c)))`, `(recv (cat (enc (enc c nc nb nm price hash) (privk b)) nb))`, `(send (enc (enc b nb nm hash) (privk m)))`
- **Skeletons, Goals, Rules & Macros**:
  - 3 `(defskeleton epmo ...)` queries testing `customer` height 5, `bank` height 3, and `merchant` height 4 with `(non-orig (privk b) (privk c) (privk m))`.
- **When to Reference This Example**: Reference this example to recognize legacy CPSA models where a one-way hash function is modeled as an asymmetric key variable `(hash akey)` with `(non-orig (invk hash))` (and note that modern CPSA provides the built-in unary `(hash ...)` operator used in `epmo-hash.scm`).
- **Key S-Expression Excerpt**:
```scheme
(defprotocol epmo basic
  (defrole bank
    (vars (b c m name) (hash akey) (nc nm nb data) (price text))
    (trace
     (recv (enc c nc nm price (pubk b)))
     (send (cat (enc (enc c nc nb nm price hash) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (enc b nb nm hash) (privk m))))
    (non-orig (invk hash))
    (uniq-orig nb)
    (annotations b
      (1
        (implies
          (and (forall ((pm name)) (says c (transfer b price pm nm)))
            (forall ((pm name)) (says pm (transfer b price pm nm))))
          (forall ((pm name)) (transfer b price pm nm))))
      (2
        (and (says c (transfer b price m nm))
          (says m (transfer b price m nm))))))
```

---

## epmo_acctnum-key-hash.scm

- **File Path**: `03_examples_scm/epmo_acctnum-key-hash.scm`
- **Algebra & Herald**: `(herald "Electronic Purchase with Money Order Protocol Variant with Key Hashing" (comment "This version includes account numbers in exchanges"))` — `basic` algebra (`(defprotocol epmo_acctnum basic ...)`).
- **Protocol & Purpose**: Variant of the EPMO protocol (`epmo_acctnum`) that adds an account number `(acctnum text)` to the customer-to-bank request and declares all nonces (`nb`, `nc`, `nm`) and `price` as sort `text` (instead of separating `data` and `text`), while omitting `(uniq-orig nb)` from the `bank` role. As documented in the file's comments, this produces an interesting counterexample shape during generalization where the bank's nonce `nb` becomes unified with `price` (which originates on the `merchant` strand) and cannot be separated during generalization unless `(uniq-orig nb)` is declared at the role level on `bank`.
- **Roles & Variables**:
  - `bank`:
    - `(vars (b c m name) (acctnum text) (nc nm nb price text))`
    - Role-level annotations: `(annotations b (1 ...) (2 ...))` (no `uniq-orig nb` in role)
    - Trace: `(recv (enc c nc nm acctnum price (pubk b)))`, `(send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) (enc nc nb (pubk c))))`, `(recv (enc (enc "hash" (cat b m nb nm)) (privk m)))`
  - `customer`:
    - `(vars (b c m name) (acctnum nb nc nm goods price text))`
    - Role-level assumptions & annotations: `(non-orig (privk b))`, `(uniq-orig nc)`, `(annotations c (1 ...) (3 ...) (4 ...))`
    - Trace: `(send (enc c nc goods (pubk m)))`, `(recv (enc nc nm m price (pubk c)))`, `(send (enc c nc nm acctnum price (pubk b)))`, `(recv (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) (enc nc nb (pubk c))))`, `(send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) nb))`
  - `merchant`:
    - `(vars (b c m name) (nb nc nm goods price text))`
    - Role-level assumptions & annotations: `(uniq-orig nm)`, `(annotations m (1 ...) (2 ...) (3 ...))`
    - Trace: `(recv (enc c nc goods (pubk m)))`, `(send (enc nc nm m price (pubk c)))`, `(recv (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) nb))`, `(send (enc (enc "hash" (cat b m nb nm)) (privk m)))`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton epmo_acctnum ...)` queries testing `merchant` height 4 and `bank` height 3 with `(non-orig (privk b) (privk m) (privk c))` and `(uniq-orig nm nc nb)`.
- **When to Reference This Example**: Reference this example to understand why declaring `(uniq-orig ...)` inside a `defrole` (role-level unique origination) is stronger than declaring `(uniq-orig ...)` only in `defskeleton`, and how giving nonces (`nb`) and protocol fields (`price`) the same sort (`text`) can cause unexpected variable identification (`nb = price`) if role-level `uniq-orig` is omitted.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol epmo_acctnum basic
  (defrole bank
    (vars (b c m name) (acctnum text) (nc nm nb price text))
    (trace
     (recv (enc c nc nm acctnum price (pubk b)))
     (send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (enc "hash" (cat b m nb nm)) (privk m))))
    (annotations b
      (1
        (forall ((pm name))
          (implies
            (and (authtransfer c acctnum b price pm nm)
              (reqtransfer pm b price pm nm))
            (dotransfer acctnum b price pm nm))))
      (2
        (and (says c (authtransfer c acctnum b price m nm))
          (says m (reqtransfer m b price m nm))))))
```

---

## expand.scm

- **File Path**: `03_examples_scm/expand.scm`
- **Algebra & Herald**: `(herald expand (expand) (comment "test macro expansion"))` — `basic` algebra (`(defprotocol expand basic ...)`), with herald flag `(expand)`.
- **Protocol & Purpose**: Minimal regression test demonstrating CPSA's `(defmacro ...)` facility, the splice marker `^` inside macros, and the `(expand)` herald option (which instructs CPSA to stop after macro expansion and output the expanded S-expressions).
- **Roles & Variables**:
  - `init`:
    - `(vars (t text) (k skey))`
    - Trace: `(send (altenc t k))`, `(recv (cat (altcat t k)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: `(defmacro (altenc t k) (enc t k))` and `(defmacro (altcat a b) (^ a b))` (where `^` splices `a` and `b` directly into the surrounding `(cat ...)` form).
  - **Skeleton**: `(defskeleton expand (vars) (defstrand init 2))`.
- **When to Reference This Example**: Reference this example for the exact syntax of `(defmacro (<name> <args>...) <body>)`, the splice operator `(^ ...)` for flattening macro arguments into a parent list, and the `(expand)` herald flag.
- **Key S-Expression Excerpt**:
```scheme
(herald expand (expand) (comment "test macro expansion"))

(defmacro (altenc t k)
  (enc t k))

(defmacro (altcat a b)
  (^ a b))

(defprotocol expand basic
  (defrole init
    (vars (t text) (k skey))
    (trace
     (send (altenc t k))
     (recv (cat (altcat t k))))))

(defskeleton expand
  (vars)
  (defstrand init 2))
```

---

## facts.scm

- **File Path**: `03_examples_scm/facts.scm`
- **Algebra & Herald**: `(herald facts)` — `basic` algebra across two protocols (`unilateral` and `iso-unilateral`).
- **Protocol & Purpose**: Demonstrates how user-defined relational facts (`(facts (foo 0 k) (bar 0 (invk k)))` in `defskeleton` and `(fact foo z k)` in `defgoal`) and security goals (`defgoal`) work in CPSA. Also models the two-pass unilateral authentication protocol from ISO/IEC JTC 1/SC 27/WG 2 N1050 (`iso-unilateral`) and tests both satisfied and intentionally falsified (`(false)`) `defgoal` assertions.
- **Roles & Variables**:
  - In `unilateral`:
    - `init`: `(vars (n text) (k akey))`, `(uniq-orig n)`, trace: `(send (enc n k))`, `(recv n)`
    - `resp`: `(vars (n text) (k akey))`, trace: `(recv (enc n k))`, `(send n)`
  - In `iso-unilateral`:
    - `resp`: `(vars (na nb t1 t2 t3 text) (b name))`, `(uniq-orig na)`, trace: `(recv (cat nb t1))`, `(send (cat na nb b t3 (enc na nb b t2 (privk b))))`
    - `init`: `(vars (na nb t1 t2 t3 text) (b name))`, `(uniq-orig nb)`, trace: `(send (cat nb t1))`, `(recv (cat na nb b t3 (enc na nb b t2 (privk b))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Skeletons**:
    1. `unilateral` `init` height 2 with `(non-orig (invk k))` and `(facts (foo 0 k) (bar 0 (invk k)))` (where `0` is strand index 0).
    2. `unilateral` `resp` height 2 with `(pen-non-orig n)` and `(non-orig (invk k))`.
    3. `iso-unilateral` `init` height 2 with `(non-orig (privk b))`.
  - **Goals** (`defgoal`):
    1. `unilateral` goal from `init` perspective incorporating `(fact foo z k)`, `(fact bar z (invk k))`, `(uniq-at n z 0)`, and `(prec ...)`.
    2. `unilateral` goal from `resp` perspective using `(pnon n)` (the formula predicate for `pen-non-orig`).
    3. `iso-unilateral` authentication goal concluding `(exists ((y strd)) (and (p "resp" y 2) (p "resp" "b" y b)))`.
    4. `iso-unilateral` intentionally false goal concluding `(false)`.
- **When to Reference This Example**: Reference this example when attaching custom `(facts (<pred> <strand-idx-or-term> ...))` to a `defskeleton` and referencing them via `(fact <pred> <strd-var> ...)` in a `defgoal` or `defrule`, or when using `(pnon n)` and `(uniq-at n z 0)` in `defgoal` formulas.
- **Key S-Expression Excerpt**:
```scheme
(defskeleton unilateral
   (vars (k akey))
   (defstrand init 2 (k k))
   (non-orig (invk k))
   (facts (foo 0 k)
	  (bar 0 (invk k))))

(defgoal unilateral
  (forall ((n text) (k akey) (z strd))
    (implies
      (and (p "init" z 2) (p "init" "n" z n) (p "init" "k" z k)
        (non (invk k)) (uniq-at n z 0)
	(fact foo z k)
	(fact bar z (invk k)))
      (exists ((z-0 strd))
        (and (p "resp" z-0 2) (p "resp" "n" z-0 n) (p "resp" "k" z-0 k)
          (prec z 0 z-0 0) (prec z-0 1 z 1))))))
```

---

## factvar.scm

- **File Path**: `03_examples_scm/factvar.scm`
- **Algebra & Herald**: `(herald factvar)` — `basic` algebra (`(defprotocol free-fact-var basic ...)`).
- **Protocol & Purpose**: Demonstrates a `defrule` (`add`) whose existential conclusion `(exists ((m text)) (fact thing m))` introduces a fresh variable `m` of sort `text` that appears only inside a `fact` and does not occur in any strand.
- **Roles & Variables**:
  - `resp`:
    - `(vars (n text) (k akey))`
    - Trace: `(recv (enc n k))`, `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - **Rule**: `add` (`(forall ((z strd)) (implies (p "resp" z 1) (exists ((m text)) (fact thing m))))`).
  - **Skeletons**: 2 `(defskeleton free-fact-var ...)` blocks:
    1. `(defstrand resp 1 (k k))` with `(non-orig (invk k))`
    2. `(defstrand resp 1 (n n) (k k))` with `(non-orig (invk k))` and `(pen-non-orig n)`
- **When to Reference This Example**: Reference this example when writing a `defrule` that existentially quantifies a ghost/auxiliary variable (`(exists ((m text)) (fact thing m))`) used solely inside `fact` relations rather than protocol messages.
- **Key S-Expression Excerpt**:
```scheme
(herald factvar)

;; An example of a rule that creates a variable that is
;; used in a fact but does not occur in a strand.

(defprotocol free-fact-var basic
  (defrole resp
    (vars (n text) (k akey))
    (trace
     (recv (enc n k))
     (send n)))

  (defrule add
    (forall ((z strd))
	    (implies
	     (p "resp" z 1)
	     (exists ((m text))
		     (fact thing m))))
    (comment "This rule adds a text variable")
    (comment "that does not appear in a strand"))
  )

(defskeleton free-fact-var
  (vars (n text) (k akey))
  (defstrand resp 1 (n n) (k k))
  (non-orig (invk k))
  (pen-non-orig n))
```

---

## ffgg.scm

- **File Path**: `03_examples_scm/ffgg.scm`
- **Algebra & Herald**: `(herald "The ffgg Protocol" (comment "From A Necessarily Parallel Attack by Jon K. Millen"))` — `basic` algebra (`(defprotocol ffgg basic ...)`).
- **Protocol & Purpose**: Models Jon K. Millen's `ffgg` protocol from "A Necessarily Parallel Attack", designed to exhibit a secrecy attack on the secret `(m text)` that requires two parallel responder runs (`resp`). The responder generates two nonces `(uniq-orig n1 n2)`, sends `(cat b n1 n2)`, receives `(cat a (enc n1 x y (pubk b)))`, and replies with `(cat n1 x (enc x y n1 (pubk b)))`—exposing the first inner component `x` in plaintext and shifting `(x, y, n1)` inside the encryption, which allows an attacker running two parallel sessions to extract `m` from `(enc n1 n2 m (pubk b))`.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b name) (n1 n2 m x y text))`
    - Trace: `(send a)`, `(recv (cat b n1 n2))`, `(send (cat a (enc n1 n2 m (pubk b))))`, `(recv (cat n1 x (enc x y n1 (pubk b))))`
  - `resp`:
    - `(vars (b a name) (n1 n2 x y text))`
    - Role-level assumptions: `(uniq-orig n1 n2)`
    - Trace: `(recv a)`, `(send (cat b n1 n2))`, `(recv (cat a (enc n1 x y (pubk b))))`, `(send (cat n1 x (enc x y n1 (pubk b))))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton ffgg (vars (b name) (n1 n2 m text)) (defstrand init 4 (b b) (m m)) (deflistener m) (uniq-orig m) (non-orig (privk b)))`.
- **When to Reference This Example**: Reference this example when studying multi-session / parallel-session oracle attacks in CPSA where an encryption oracle shifts positional fields inside `(enc ... (pubk b))` and leaks `m` to `(deflistener m)`.
- **Key S-Expression Excerpt**:
```scheme
(herald "The ffgg Protocol"
	(comment "From A Necessarily Parallel Attack by Jon K. Millen"))

(defprotocol ffgg basic
  (defrole init (vars (a b name) (n1 n2 m x y text))
    (trace
     (send a)
     (recv (cat b n1 n2))
     (send (cat a (enc n1 n2 m (pubk b))))
     (recv (cat n1 x (enc x y n1 (pubk b))))))
  (defrole resp (vars (b a name) (n1 n2 x y text))
    (trace
     (recv a)
     (send (cat b n1 n2))
     (recv (cat a (enc n1 x y (pubk b))))
     (send (cat n1 x (enc x y n1 (pubk b)))))
    (uniq-orig n1 n2)))

(defskeleton ffgg
  (vars (b name) (n1 n2 m text))
  (defstrand init 4 (b b) (m m))
  (deflistener m)
  (uniq-orig m)
  (non-orig (privk b)))
```

---

## fluffy_draft03_gske.scm

- **File Path**: `03_examples_scm/fluffy_draft03_gske.scm`
- **Algebra & Herald**: `(herald "GSKE, part of Fluffy: Simplified Key Exchange for Constrained Environments draft-hardjono-ace-fluffy-03" (comment "Based on the Internet-Draft: https://www.ietf.org/archive/id/draft-hardjono-ace-fluffy-03.txt"))` — `basic` algebra across two protocol definitions (`fluffy` and `fluffy-rule`).
- **Protocol & Purpose**: Models the Group Symmetric Key Establishment (GSKE) sub-protocol of the IETF ACE Fluffy Internet-Draft (`draft-hardjono-ace-fluffy-03`), involving a service principal (`sp`), a simple key distribution center (`keyserv`), and a `client` sharing long-term symmetric keys `(ltk s b)` and `(ltk s a)`. Because `"req"`/`"fetch"` and `"resp"`/`"deliver"` encryptions under `(ltk s ...)` have identical ciphertext structures `(enc s g nb gk (ltk s b))` and `(enc s g na gk (ltk s a))`, `fluffy` allows role confusion where a client acts as a service principal or vice versa; `fluffy-rule` adds two `defrule` axioms (`client-no-request` and `sp-no-fetch`) that forbid `a` and `b` from playing both roles with the same key server `s`.
- **Roles & Variables**:
  - Identical in `fluffy` and `fluffy-rule`:
    - `sp`: `(vars (b s name) (nb g text) (gk skey))`, trace: `(send (cat "req" s g (enc b nb (ltk s b))))`, `(recv (cat "resp" b (enc s g nb gk (ltk s b))))`
    - `keyserv`: `(vars (a b s name) (nb na g text) (gk skey))`, `(uniq-gen gk)`, trace: `(recv (cat "req" s g (enc b nb (ltk s b))))`, `(send (cat "resp" b (enc s g nb gk (ltk s b))))`, `(recv (cat "fetch" s g (enc a na (ltk s a))))`, `(send (cat "deliver" a (enc s g na gk (ltk s a))))`
    - `client`: `(vars (a b s name) (na g text) (gk skey))`, trace: `(send (cat "fetch" s g (enc a na (ltk s a))))`, `(recv (cat "deliver" a (enc s g na gk (ltk s a))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Rules** (in `fluffy-rule`): `client-no-request` and `sp-no-fetch` (using `(false)` to enforce disjoint principal sets for `client` and `sp`).
  - **Skeletons**: 6 `(defskeleton ...)` queries (3 for `fluffy`, 3 for `fluffy-rule`) testing `sp` height 2, `keyserv` height 4, and `client` height 2 using `(non-orig (ltk s b))`, `(non-orig (ltk s a))`, `(uniq-orig nb)`, `(uniq-orig na)`, and `(uniq-gen gk)`.
- **When to Reference This Example**: Reference this example when modeling IETF symmetric-key KDC protocols using `(ltk s a)` / `(ltk s b)` where outer message tags (`"req"`, `"resp"`, `"fetch"`, `"deliver"`) are in the clear outside `(enc ...)` and you need `defrule` role-separation constraints to prevent principal role confusion.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol fluffy-rule basic
  (defrole sp
    (vars (b s name) (nb g text) (gk skey))
    (trace
     (send (cat "req" s g (enc b nb (ltk s b))))
     (recv (cat "resp" b (enc s g nb gk (ltk s b))))))
  (defrole keyserv
    (vars (a b s name) (nb na g text) (gk skey))
    (trace
     (recv (cat "req" s g (enc b nb (ltk s b))))
     (send (cat "resp" b (enc s g nb gk (ltk s b))))
     (recv (cat "fetch" s g (enc a na (ltk s a))))
     (send (cat "deliver" a (enc s g na gk (ltk s a)))))
    (uniq-gen gk))
  (defrole client
    (vars (a b s name) (na g text) (gk skey))
    (trace
     (send (cat "fetch" s g (enc a na (ltk s a))))
     (recv (cat "deliver" a (enc s g na gk (ltk s a))))))
  (defrule client-no-request
    (forall ((a s name) (y z strd))
	    (implies
	     (and
	      (p "client" z 1)
	      (p "client" "s" z s)
	      (p "client" "a" z a)
	      (p "keyserv" y 1)
	      (p "keyserv" "s" y s)
	      (p "keyserv" "b" y a))
	     (false)))))
```

---

## fragile_pruning.scm

- **File Path**: `03_examples_scm/fragile_pruning.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol fragile_pruning basic ...)`.
- **Protocol & Purpose**: Illustrates why CPSA's strand pruning must be conservative even when multiple strands of the same role appear isomorphic up to renaming. An `init` strand sends `(enc n k)`, receives three encrypted pairs `(enc n n1 k)`, `(enc n n2 k)`, `(enc n n3 k)` from three separate `adder` strands, sends `(enc n n1 n2 n3 k)`, and receives `(enc n n1 n2 n3 n k)` from a `final` strand. If CPSA prematurely pruned two of the three `adder` strands as renamings of each other before `n1`, `n2`, and `n3` were kept distinct, it would fail to find the shape where `n1`, `n2`, `n3` remain distinct `uniq-orig` values.
- **Roles & Variables**:
  - `init`:
    - `(vars (k akey) (n n1 n2 n3 text))`
    - Role-level assumptions: `(uniq-orig n)`, `(non-orig (invk k))`
    - Trace: `(send (enc n k))`, `(recv (enc n n1 k))`, `(recv (enc n n2 k))`, `(recv (enc n n3 k))`, `(send (enc n n1 n2 n3 k))`, `(recv (enc n n1 n2 n3 n k))`
  - `adder`:
    - `(vars (k akey) (n new text))`
    - Role-level assumptions: `(uniq-orig new)`
    - Trace: `(recv (enc n k))`, `(send (enc n new k))`
  - `final`:
    - `(vars (k akey) (n n1 n2 n3 text))`
    - Trace: `(recv (enc n n1 n2 n3 k))`, `(send (enc n n1 n2 n3 n k))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton fragile_pruning (vars (k akey) (n n1 n2 n3 text)) (defstrand init 6 (k k) (n n) (n1 n1) (n2 n2) (n3 n3)) (uniq-orig n1 n2 n3))`.
- **When to Reference This Example**: Reference this example when analyzing protocols where a single initiator aggregates multiple fresh tokens (`n1`, `n2`, `n3`) from multiple parallel responder (`adder`) instances and combines them in a single message (`(enc n n1 n2 n3 k)`).
- **Key S-Expression Excerpt**:
```scheme
(defprotocol fragile_pruning basic
  (defrole init (vars (k akey) (n n1 n2 n3 text))
    (trace
	(send (enc n k))
      (recv (enc n n1 k))
      (recv (enc n n2 k))
      (recv (enc n n3 k))
      (send (enc n n1 n2 n3 k))
      (recv (enc n n1 n2 n3 n k))
    )
    (uniq-orig n)
    (non-orig (invk k))
  )
  (defrole adder (vars (k akey) (n new text))
    (trace
      (recv (enc n k))
      (send (enc n new k))
    )
    (uniq-orig new)
  )
  (defrole final (vars (k akey) (n n1 n2 n3 text))
    (trace
       (recv (enc n n1 n2 n3 k))
       (send (enc n n1 n2 n3 n k))
    )
  )
)

(defskeleton fragile_pruning
  (vars (k akey) (n n1 n2 n3  text))
  (defstrand init 6 (k k) (n n) (n1 n1) (n2 n2) (n3 n3))
  (uniq-orig n1 n2 n3)
)
```

---

## goals.scm

- **File Path**: `03_examples_scm/goals.scm`
- **Algebra & Herald**: `(herald goals)` — `basic` algebra across four protocol definitions (`ns`, `nsl`, `unilateral`, `nsl-typeless`).
- **Protocol & Purpose**: Comprehensive reference for CPSA's formal security goals (`defgoal` and skeleton-embedded `(goals ...)`), using standard role-specific predicates `(p "<role>" <strd> <height>)`, `(p "<role>" "<param>" <strd> <val>)`, listener predicates `(p "" <strd> 1)` and `(p "" "x" <strd> <val>)`, `(non ...)`, `(uniq ...)`, `(uniq-at ...)`, and `(prec ...)`. Covers:
  - Needham-Schroeder (`ns`): initiator authentication, precedence ordering, Lowe's responder authentication failure, initiator nonce secrecy, and predicate-mapped unilateral authentication goals.
  - Needham-Schroeder-Lowe (`nsl`): responder authentication success.
  - Unilateral authentication (`unilateral`): basic authentication goal.
  - Double initiator point-of-view skeleton (`(defskeleton ns ... (goals ...))`) concluding strand equality `(= z z-0)`.
  - Untyped Needham-Schroeder-Lowe (`nsl-typeless`): where `n2` in `init` and `n1` in `resp` have sort `mesg` instead of `text`, exposing a type-flaw secrecy failure on `n2`.
- **Roles & Variables**:
  - In `ns`: `init` (`(vars (a b name) (n1 n2 text))`), `resp` (`(vars (b a name) (n2 n1 text))`)
  - In `nsl`: `init` (`(vars (a b name) (n1 n2 text))`), `resp` (`(vars (b a name) (n2 n1 text))`) with `b` included in message 2 `(enc n1 n2 b (pubk a))`
  - In `unilateral`: `init` (`(vars (a name) (n text))`), `resp` (`(vars (a name) (n text))`)
  - In `nsl-typeless`: `init` (`(vars (a b name) (n1 text) (n2 mesg))`) with message 1 `(send (enc a n1 (pubk b)))`, `resp` (`(vars (b a name) (n2 text) (n1 mesg))`)
- **Skeletons, Goals, Rules & Macros**:
  - 12 `(defgoal ...)` declarations (including a multi-sentence `defgoal ns` containing two `forall` formulas) and 1 `(defskeleton ns ...)` containing an embedded `(goals (forall ...))` clause.
- **When to Reference This Example**: Reference this example as the primary template for writing `(defgoal <prot> (forall ...))` and skeleton-level `(goals (forall ...))` using the classic `(p "<role>" ...)` and listener `(p "" z1 1) (p "" "x" z1 n1)` predicate syntax, as well as modeling type-flaw attacks via sort `mesg` (`nsl-typeless`).
- **Key S-Expression Excerpt**:
```scheme
(defgoal ns
  (forall ((a b name) (n1 text) (z0 z1 strd))
    (implies
     (and (p "init" z0 3) (p "init" "n1" z0 n1)
      (p "init" "a" z0 a) (p "init" "b" z0 b)
      (p "" z1 1) (p "" "x" z1 n1)
      (non (privk a)) (non (privk b)) (uniq n1))
     (false)))
  (comment "Initiator point of view")
  (comment "Secrecy goal: nonce n1 not revealed"))

(defskeleton ns
  (vars (a b name) (n1 n1-0 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (defstrand init 3 (a a) (b b) (n1 n1-0))
  (non-orig (privk b) (privk a))
  (uniq-orig n1 n1-0)
  (goals
  (forall ((n1 n1-0 n2 n2-0 text) (a b name) (z z-0 strd))
    (implies
      (and (p "init" z 3) (p "init" z-0 3) (p "init" "n1" z n1)
        (p "init" "n2" z n2) (p "init" "a" z a) (p "init" "b" z b)
        (p "init" "n1" z-0 n1-0) (p "init" "n2" z-0 n2-0)
        (p "init" "a" z-0 a) (p "init" "b" z-0 b) (non (privk a))
        (non (privk b)) (uniq-at n1 z 0) (uniq-at n1-0 z-0 0))
      (= z z-0))))
  (comment "Double initiator point of view"))
```

---

## goalsvar.scm

- **File Path**: `03_examples_scm/goalsvar.scm`
- **Algebra & Herald**: `(herald goalsvar)` — `basic` algebra across four protocol definitions (`ns`, `nsl`, `unilateral`, `nsl-typeless`).
- **Protocol & Purpose**: Exact counterpart to `goals.scm` demonstrating CPSA's concise `strand` and `listener` goal syntax (`(strand <role> <strd-var> <height> (<param> <val>) ...)` and `(listener <strd-var> <term>)`) in place of verbose `(p "<role>" ...)` and `(p "" ...)` predicates across all 12 `defgoal` declarations and the `defskeleton` `(goals ...)` block.
- **Roles & Variables**:
  - Identical to `goals.scm` across all 4 protocols (`ns`, `nsl`, `unilateral`, `nsl-typeless`):
    - `ns`: `init` (`(vars (a b name) (n1 n2 text))`), `resp` (`(vars (b a name) (n2 n1 text))`)
    - `nsl`: `init` (`(vars (a b name) (n1 n2 text))`), `resp` (`(vars (b a name) (n2 n1 text))`)
    - `unilateral`: `init` (`(vars (a name) (n text))`), `resp` (`(vars (a name) (n text))`)
    - `nsl-typeless`: `init` (`(vars (a b name) (n1 text) (n2 mesg))`), `resp` (`(vars (b a name) (n2 text) (n1 mesg))`)
- **Skeletons, Goals, Rules & Macros**:
  - 12 `(defgoal ...)` declarations and 1 `(defskeleton ns ... (goals ...))` block using `(strand ...)` and `(listener ...)` predicates.
- **When to Reference This Example**: Reference this example when writing readable `(defgoal ...)` or `(goals ...)` specifications using the compact `(strand <role> <z> <h> (<var> <val>) ...)` and `(listener <z> <term>)` syntax instead of `(p "<role>" ...)`.
- **Key S-Expression Excerpt**:
```scheme
(defgoal ns
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and (strand init z0 3 (n1 n1) (b b))
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
        (and 
          (strand resp z1 2 (b b))
	      (prec z1 1 z0 2)))))
  (comment "Prec example"))

(defgoal ns
  (forall ((a b name) (n1 text) (z0 z1 strd))
    (implies
     (and (strand init z0 3 (n1 n1) (a a) (b b))
      (listener z1 n1)
      (non (privk a)) (non (privk b)) (uniq n1))
     (false)))
  (comment "Initiator point of view")
  (comment "Secrecy goal: nonce n1 not revealed"))
```
