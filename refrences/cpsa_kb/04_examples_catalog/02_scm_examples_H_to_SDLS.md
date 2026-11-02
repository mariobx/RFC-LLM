# Official MITRE CPSA Examples Catalog (Part 2: hashtest-key-hash.scm to sdls-ep-challenge-authenc.scm)

This catalog documents files `50` through `99` (sorted alphabetically) from `03_examples_scm/`, covering `hashtest-key-hash.scm` through `sdls-ep-challenge-authenc.scm`. Every entry is extracted strictly from the actual `.scm` source file.

## hashtest-key-hash.scm

- **File Path**: `03_examples_scm/hashtest-key-hash.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Hashtest")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `hashtest`. Tests whether keyed hashing modeled via symmetric/asymmetric encryption `(enc "h" n)` using a nonce `n` of sort `data` as an encryption key works properly in CPSA's `basic` algebra. The initiator sends `(enc n k)` under asymmetric key `k` (with `(invk k)` non-originating and `n` uniquely originating) and expects `(enc "h" n)` in return from the responder.
- **Roles & Variables**:
  - Role `init`: Vars: `(n data)`, `(k akey)` | Role Assumptions: `(uniq-orig n)`, `(non-orig (invk k))` | Trace (2 events): `(send (enc n k))` -> `(recv (enc "h" n))`
  - Role `resp`: Vars: `(k akey)`, `(n data)` | Role Assumptions: none | Trace (2 events): `(recv (enc n k))` -> `(send (enc "h" n))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`hashtest`): `(vars)`, `(defstrand init 2)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when comparing ad-hoc hash modeling via `(enc "h" n)` (which allows anyone who learns `n` to both construct and invert/decrypt the term if `n` is a symmetric key or data term) against native `(hash n)` in the `basic` algebra.
- **Key S-Expression Excerpt** (lines 1–25):
```scheme
;;; Hashtest.scm is designed to test if the
;;; hash is working properly.
(herald "Hashtest")

(defprotocol hashtest basic
  (defrole init (vars (n data) (k akey))
     (trace
       (send (enc n k))
       (recv (enc "h" n))
     )
     (uniq-orig n)
     (non-orig (invk k))
   )
   (defrole resp (vars (k akey) (n data))
     (trace
       (recv (enc n k))
       (send (enc "h" n))
     )
   )
)

(defskeleton hashtest
   (vars)
   (defstrand init 2)
)
```

## hashtest.scm

- **File Path**: `03_examples_scm/hashtest.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Hashtest")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `hashtest`. Tests CPSA's built-in one-way `(hash ...)` operator in the `basic` algebra. The initiator sends `(enc n k)` where `n` is fresh (`uniq-orig`) and `(invk k)` is uncompromised (`non-orig`), and receives `(hash n)` from the responder.
- **Roles & Variables**:
  - Role `init`: Vars: `(n data)`, `(k akey)` | Role Assumptions: `(uniq-orig n)`, `(non-orig (invk k))` | Trace (2 events): `(send (enc n k))` -> `(recv (hash n))`
  - Role `resp`: Vars: `(k akey)`, `(n data)` | Role Assumptions: none | Trace (2 events): `(recv (enc n k))` -> `(send (hash n))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`hashtest`): `(vars)`, `(defstrand init 2)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for the minimal canonical syntax of the built-in `(hash ...)` operator in CPSA's `basic` algebra and how CPSA derives authentication when a secret nonce `n` is returned inside a one-way hash.
- **Key S-Expression Excerpt** (lines 1–25):
```scheme
;;; Hashtest.scm is designed to test if the
;;; hash is working properly.
(herald "Hashtest")

(defprotocol hashtest basic
  (defrole init (vars (n data) (k akey))
     (trace
       (send (enc n k))
       (recv (hash n))
     )
     (uniq-orig n)
     (non-orig (invk k))
   )
   (defrole resp (vars (k akey) (n data))
     (trace
       (recv (enc n k))
       (send (hash n))
     )
   )
)

(defskeleton hashtest
   (vars)
   (defstrand init 2)
)
```

## incompleteness_example.scm

- **File Path**: `03_examples_scm/incompleteness_example.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald incompleteness-example (comment "Shows a shape not found by CPSA"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `incompleteness-example`. Demonstrates an intentional incompleteness edge case in CPSA's search algorithm (`"Shows a shape not found by CPSA"`). In `incompleteness-example`, `init` sends `(enc n k)` and receives `n`, while `resp` receives `(enc n1 k)` and sends an independent variable `n2` without linking `n1` and `n2` in the role definition. The second skeleton explicitly exhibits a valid shape where `n1 = n` and `n2 = n` with causal ordering `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`, which CPSA does not discover from the first skeleton because `resp` does not originate or transform `n`.
- **Roles & Variables**:
  - Role `init`: Vars: `(k akey)`, `(n text)` | Role Assumptions: `(uniq-orig n)` | Trace (2 events): `(send (enc n k))` -> `(recv n)`
  - Role `resp`: Vars: `(k akey)`, `(n1 n2 text)` | Role Assumptions: none | Trace (2 events): `(recv (enc n1 k))` -> `(send n2)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`incompleteness-example`): `(vars (k akey))`, `(defstrand init 2 (k k))`, `(non-orig (invk k))` | Skeleton 2 (`incompleteness-example`): `(vars (k akey) (n text))`, `(defstrand init 2 (k k) (n n))`, `(defstrand resp 2 (k k) (n1 n) (n2 n))`, `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when debugging missing shapes or non-termination caused by roles whose `send` terms contain unconstrained variables (like `n2`) that are not bound to received variables (`n1`), violating CPSA's strand transformation expectations.
- **Key S-Expression Excerpt** (lines 1–21):
```scheme
(herald incompleteness-example
  (comment "Shows a shape not found by CPSA"))

(defprotocol incompleteness-example basic
  (defrole init (vars (k akey) (n text))
    (trace (send (enc n k)) (recv n))
    (uniq-orig n))
  (defrole resp (vars (k akey) (n1 n2 text))
    (trace (recv (enc n1 k)) (send n2))))

(defskeleton incompleteness-example
  (vars (k akey))
  (defstrand init 2 (k k))
  (non-orig (invk k)))

(defskeleton incompleteness-example
  (vars (k akey) (n text))
  (defstrand init 2 (k k) (n n))
  (defstrand resp 2 (k k) (n1 n) (n2 n))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (comment "A shape compatible with the first problem in this run"))
```

## isoreject-corrected.scm

- **File Path**: `03_examples_scm/isoreject-corrected.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald isoreject-corrected)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `isofix`. Models a corrected three-message challenge-response signature protocol (`isofix`, based on ISO/IEC 9798-3 mutual authentication) using explicit message-type tags `"first"` and `"second"` inside signatures `(enc "first" nb na a (privk b))` and `(enc "second" nc nb b (privk a))` to prevent reflection/type-confusion attacks between message 2 and message 3.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(na nb nc text)` | Role Assumptions: none | Trace (3 events): `(send (cat a na))` -> `(recv (enc "first" nb na a (privk b)))` -> `(send (enc "second" nc nb b (privk a)))`
  - Role `resp`: Vars: `(a b name)`, `(na nb nc text)` | Role Assumptions: `(uniq-orig nb)` | Trace (3 events): `(recv (cat a na))` -> `(send (enc "first" nb na a (privk b)))` -> `(recv (enc "second" nc nb b (privk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`isofix`): `(vars (a b name))`, `(defstrand resp 3 (a a) (b b))`, `(non-orig (privk a) (privk b))` | Skeleton 2 (`isofix`): `(vars (b name))`, `(defstrand init 3 (b b))`, `(non-orig (privk b))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when fixing reflection or message-confusion vulnerabilities in multi-message signed challenge-response protocols by adding distinct string literal tags (`"first"`, `"second"`) inside `(enc ... (privk ...))`.
- **Key S-Expression Excerpt** (lines 1–24):
```scheme
(herald isoreject-corrected)

(defprotocol isofix basic
  (defrole init (vars (a b name) (na nb nc text))
    (trace
     (send (cat a na))
     (recv (enc "first" nb na a (privk b)))
     (send (enc "second" nc nb b (privk a)))))
  (defrole resp (vars (a b name) (na nb nc text))
    (trace
     (recv (cat a na))
     (send (enc "first" nb na a (privk b)))
     (recv (enc "second" nc nb b (privk a))))
    (uniq-orig nb)))

(defskeleton isofix
  (vars (a b name))
  (defstrand resp 3 (a a) (b b))
  (non-orig (privk a) (privk b)))

(defskeleton isofix
  (vars (b name))
  (defstrand init 3 (b b))
  (non-orig (privk b)))
```

## isoreject.scm

- **File Path**: `03_examples_scm/isoreject.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `isoreject`. Models the untagged three-message ISO challenge-response signature protocol (`isoreject`) without string tags in the signed messages `(enc nb na a (privk b))` and `(enc nc nb b (privk a))`. Because the two signed messages have identical term structure `(enc <text> <text> <name> (privk <name>))`, a responder's first signature can be reflected or confused with an initiator's second signature.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(na nb nc text)` | Role Assumptions: none | Trace (3 events): `(send (cat a na))` -> `(recv (enc nb na a (privk b)))` -> `(send (enc nc nb b (privk a)))`
  - Role `resp`: Vars: `(a b name)`, `(na nb nc text)` | Role Assumptions: `(uniq-orig nb)` | Trace (3 events): `(recv (cat a na))` -> `(send (enc nb na a (privk b)))` -> `(recv (enc nc nb b (privk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`isoreject`): `(vars (a b name))`, `(defstrand resp 3 (a a) (b b))`, `(non-orig (privk a) (privk b))` | Skeleton 2 (`isoreject`): `(vars (b name))`, `(defstrand init 3 (b b))`, `(non-orig (privk b))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example alongside `isoreject-corrected.scm` to see how structurally identical signed messages in challenge-response protocols enable reflection attacks when domain-separation tags are omitted.
- **Key S-Expression Excerpt** (lines 1–22):
```scheme
(defprotocol isoreject basic
  (defrole init (vars (a b name) (na nb nc text))
    (trace
     (send (cat a na))
     (recv (enc nb na a (privk b)))
     (send (enc nc nb b (privk a)))))
  (defrole resp (vars (a b name) (na nb nc text))
    (trace
     (recv (cat a na))
     (send (enc nb na a (privk b)))
     (recv (enc nc nb b (privk a))))
    (uniq-orig nb)))

(defskeleton isoreject
  (vars (a b name))
  (defstrand resp 3 (a a) (b b))
  (non-orig (privk a) (privk b)))

(defskeleton isoreject
  (vars (b name))
  (defstrand init 3 (b b))
  (non-orig (privk b)))
```

## kelly1.scm

- **File Path**: `03_examples_scm/kelly1.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `kelly1`. Models a three-party remote attestation protocol (`kelly1`) involving a `client`, an `appraiser`, and a `server`. The client requests content from the server (receiving `(enc (cat response Ns) (privk S))`), and asks a trusted appraiser `A` (`(non-orig (privk A))`) to verify the server's public key `(pubk S)` and nonce `Ns`. The appraiser challenges the server with fresh nonce `N`, receives a TPM-style quote signed by `(privk AIK)` binding `(cat Quote measurements N Ns (pubk S))`, and issues a signed policy decision `(enc (cat policy (pubk S) Ns) (privk A))` to the client.
- **Roles & Variables**:
  - Role `client`: Vars: `(C name)`, `(A name)`, `(S name)`, `(Ns text)`, `(request text)`, `(Check text)`, `(policy text)`, `(response text)` | Role Assumptions: none | Trace (4 events): `(send (cat C S request))` -> `(recv (cat S C (enc (cat response Ns) (privk S))))` -> `(send (cat C A Check (pubk S)))` -> `(recv (cat A C (enc (cat policy (pubk S) Ns) (privk A))))`
  - Role `appraiser`: Vars: `(C name)`, `(A name)`, `(S name)`, `(N text)`, `(Ns text)`, `(hello text)`, `(Quote text)`, `(measurements text)`, `(Check text)`, `(policy text)`, `(AIK name)` | Role Assumptions: `(non-orig (privk A) (privk AIK))`, `(uniq-orig N)` | Trace (5 events): `(recv (cat S A hello))` -> `(send (cat A S N))` -> `(recv (cat S A (enc (cat Quote measurements N Ns (pubk S)) (privk AIK)) (pubk S)))` -> `(recv (cat C A Check (pubk S)))` -> `(send (cat A C (enc (cat policy (pubk S) Ns) (privk A))))`
  - Role `server`: Vars: `(C name)`, `(A name)`, `(S name)`, `(N text)`, `(Ns text)`, `(hello text)`, `(Quote text)`, `(measurements text)`, `(request text)`, `(response text)`, `(AIK name)` | Role Assumptions: `(non-orig (privk S) (privk AIK))`, `(uniq-orig Ns)` | Trace (5 events): `(send (cat S A hello))` -> `(recv (cat A S N))` -> `(send (cat S A (enc (cat Quote measurements N Ns (pubk S)) (privk AIK)) (pubk S)))` -> `(recv (cat C S request))` -> `(send (cat S C (enc (cat response Ns) (privk S))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`kelly1`): `(vars (A name))`, `(defstrand client 4 (A A))`, `(non-orig (privk A))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling remote attestation, RATS (RFC 9334), or TPM quote verification protocols where an appraiser/verifier mediates trust between a relying party (client) and an attester (server) using an Attestation Identity Key (`AIK`).
- **Key S-Expression Excerpt** (lines 16–76):
```scheme

(defprotocol kelly1 basic

  (defrole client
    (vars (C name) (A name) (S name) (Ns text) (request text) (Check text)  (policy text) (response text))
    (trace
     (send (cat C S request))
     (recv (cat S C (enc (cat response Ns)
			 (privk S))))
     (send (cat C A Check (pubk S)))
     (recv (cat A C (enc (cat policy (pubk S) Ns)
			 (privk A))))
      )
    )

  (defrole appraiser
    (vars (C name) (A name) (S name) (N text) (Ns text) (hello text)
	  (Quote text) (measurements text) (Check text) (policy text)
	  (AIK name))
    (trace
     (recv (cat S A hello))
     (send (cat A S N))
     (recv (cat S A
		(enc
		 (cat Quote measurements N Ns (pubk S))
		 (privk AIK))
		(pubk S)))
     (recv (cat C A Check (pubk S)))
     (send (cat A C (enc (cat policy (pubk S) Ns)
			 (privk A))))
      )
    (non-orig (privk A) (privk AIK))
    (uniq-orig N)
    )

  (defrole server
    (vars (C name) (A name) (S name) (N text) (Ns text) (hello text)
	  (Quote text) (measurements text) (request text) (response text)
	  (AIK name))
   (trace
      (send (cat S A hello))
      (recv (cat A S N))
      (send (cat S A
		 (enc
		  (cat Quote measurements N Ns (pubk S))
		  (privk AIK))
		 (pubk S)))
      (recv (cat C S request))
      (send (cat S C (enc (cat response Ns)
			  (privk S))))
      )
   (non-orig (privk S) (privk AIK))
   (uniq-orig  Ns)
   )
)

(defskeleton kelly1
  (vars (A name))
  (defstrand client 4 (A A))
  (non-orig (privk A))
  )
```

## kerberos.scm

- **File Path**: `03_examples_scm/kerberos.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `kerberos`. Models a simplified three-party Kerberos authentication exchange (`kerberos`) among `init` (client `a`), `resp` (service `b`), and `keyserver` (`ks`) using shared long-term keys `(ltk a ks)` and `(ltk b ks)`. As noted in the file's comments, because the keyserver's response `(cat (enc (cat t l k b) (ltk a ks)) (enc (cat t l k a) (ltk b ks)))` is symmetric in `a` and `b`, CPSA finds two shapes corresponding to reversing `a` and `b`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a name)`, `(b name)`, `(ks name)`, `(t text)`, `(t-prime text)`, `(l text)`, `(k skey)` | Role Assumptions: none | Trace (4 events): `(send (cat a b))` -> `(recv (cat (enc (cat t l k b) (ltk a ks)) (enc (cat t l k a) (ltk b ks))))` -> `(send (cat (enc (cat a t) k) (enc (cat t l k a) (ltk b ks))))` -> `(recv (enc t-prime k))`
  - Role `resp`: Vars: `(a name)`, `(b name)`, `(ks name)`, `(t text)`, `(t-prime text)`, `(l text)`, `(k skey)` | Role Assumptions: none | Trace (2 events): `(recv (cat (enc (cat a t) k) (enc (cat t l k a) (ltk b ks))))` -> `(send (enc t-prime k))`
  - Role `keyserver`: Vars: `(a name)`, `(b name)`, `(ks name)`, `(t text)`, `(l text)`, `(k skey)` | Role Assumptions: `(uniq-orig k)` | Trace (2 events): `(recv (cat a b))` -> `(send (cat (enc (cat t l k b) (ltk a ks)) (enc (cat t l k a) (ltk b ks))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`kerberos`): `(vars (a name) (b name) (ks name))`, `(defstrand init 4 (a a) (b b) (ks ks))`, `(non-orig (ltk a ks) (ltk b ks))` | Skeleton 2 (`kerberos`): `(vars (a name) (b name) (ks name))`, `(defstrand resp 2 (a a) (b b) (ks ks))`, `(non-orig (ltk a ks) (ltk b ks))` | Skeleton 3 (`kerberos`): `(vars (a name) (b name) (ks name))`, `(defstrand keyserver 2 (a a) (b b) (ks ks))`, `(non-orig (ltk a ks) (ltk b ks))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling Kerberos or KDC-based symmetric ticket distribution protocols using `(ltk a ks)` and understanding why symmetric ticket structures produce multiple shapes unless directional tags distinguish client and server tickets.
- **Key S-Expression Excerpt** (lines 1–37):
```scheme
(defprotocol kerberos basic
  (defrole init
    (vars (a name) (b name) (ks name) (t text) (t-prime text) (l text) (k skey))
    (trace (send (cat a b))
      (recv
        (cat (enc (cat t l k b) (ltk a ks))
          (enc (cat t l k a) (ltk b ks))))
      (send (cat (enc (cat a t) k) (enc (cat t l k a) (ltk b ks))))
      (recv (enc t-prime k))))
  (defrole resp
    (vars (a name) (b name) (ks name) (t text) (t-prime text) (l text) (k skey))
    (trace (recv (cat (enc (cat a t) k) (enc (cat t l k a) (ltk b ks))))
      (send (enc t-prime k))))
  (defrole keyserver
    (vars (a name) (b name) (ks name) (t text) (l text) (k skey))
    (trace (recv (cat a b))
      (send
        (cat (enc (cat t l k b) (ltk a ks))
          (enc (cat t l k a) (ltk b ks))))) (uniq-orig k)))

; we'll observe two shapes resulting from these preskeletons
; because the keyserver can reverse a and b with no change
; in the protocol
(defskeleton kerberos
  (vars (a name) (b name) (ks name))
  (defstrand init 4 (a a) (b b) (ks ks))
  (non-orig (ltk a ks) (ltk b ks)))

(defskeleton kerberos
  (vars (a name) (b name) (ks name))
  (defstrand resp 2 (a a) (b b) (ks ks))
  (non-orig (ltk a ks) (ltk b ks)))

(defskeleton kerberos
  (vars (a name) (b name) (ks name))
  (defstrand keyserver 2 (a a) (b b) (ks ks))
  (non-orig (ltk a ks) (ltk b ks)))
```

## lemmas.scm

- **File Path**: `03_examples_scm/lemmas.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald goalsvar)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. Demonstrates CPSA's `(deflemma ...)` and `(defgoal ...)` security goal declarations on the Needham-Schroeder Public-Key protocol (`ns`, from Section 10 of the CPSA Primer). Illustrates the three `deflemma` modes: `(deflemma rule lemma1 ns ...)` (used only as a rewrite rule), `(deflemma both lemma2 ns ...)` (both proved as a goal and used as a rule), and `(deflemma goal lemma3 ns ...)` (proved as a goal only), alongside `(defgoal ns ...)` using role-variable predicate syntax `(strand init z0 3 (n1 n1) (b b))`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 text)` | Role Assumptions: none | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc n1 n2 (pubk a)))` -> `(send (enc n2 (pubk b)))`
  - Role `resp`: Vars: `(b a name)`, `(n2 n1 text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 (pubk a)))` -> `(recv (enc n2 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Lemmas (3)**: `(deflemma rule lemma1 ns (forall ((b name) (n1 text) (z0 strd)) (implies (and (strand init z0 3 (n1 n1) (b b)) (non (privk b)) (uniq n1)) (exists ((z1 strd)) (strand resp z1 2 (b b))))) (comment "Skeleton 1") (comment "Authentication goal: agreement on name b"))`; `(deflemma both lemma2 ns (forall ((b name) (n1 text) (z0 strd)) (implies (and (strand init z0 3 (n1 n1) (b b)) (non (privk b)) (uniq n1)) (exists ((z1 strd)) (and (strand resp z1 2 (b b)) (prec z1 1 z0 2))))) (comment "Prec example. Skeleton 2"))`; `(deflemma goal lemma3 ns (forall ((a b name) (n2 text) (z0 strd)) (implies (and (strand resp z0 3 (n2 n2) (a a) (b b)) (non (privk a)) (uniq n2)) (exists ((z1 strd)) (strand init z1 2 (b b))))) (comment "Skeleton 3") (comment "Failed authentication goal: agreement on name b"))`
  - **Goals (1)**: `(defgoal ns (forall ((a b name) (n2 text) (z0 strd)) (implies (and (strand resp z0 3 (n2 n2) (a a) (b b)) (non (privk a)) (uniq n2)) (exists ((z1 strd)) (strand init z1 2 (b b))))) (comment "Skeleton 4"))`
  - **Skeletons**: None active (note: `;`-commented `defskeleton` blocks appear at the bottom of `scep-tls-dh-broken.scm`)
  - **Keywords & Predicates Used**: `and`, `defgoal`, `deflemma`, `defprotocol`, `defrole`, `exists`, `forall`, `herald`, `implies`, `non`, `prec`, `recv`, `send`, `strand`, `trace`, `uniq`, `vars`
- **When to Reference This Example**: Reference this example when writing `(deflemma <mode> <name> <prot> ...)` or `(defgoal <prot> ...)` formulas using the high-level `(strand <role> <strd> <height> (<var> <val>)...)`, `(non ...)`, `(uniq ...)`, and `(prec ...)` predicates.
- **Key S-Expression Excerpt** (lines 22–61):
```scheme
(deflemma rule lemma1 ns
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and 
      (strand init z0 3 (n1 n1) (b b))
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
	     (strand resp z1 2 (b b)))))
  (comment "Skeleton 1")
  (comment "Authentication goal: agreement on name b"))

(deflemma both lemma2 ns
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and (strand init z0 3 (n1 n1) (b b))
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
        (and 
          (strand resp z1 2 (b b))
	      (prec z1 1 z0 2)))))
  (comment "Prec example. Skeleton 2"))

(deflemma goal lemma3 ns
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
     (and (strand resp z0 3 (n2 n2) (a a) (b b))
      (non (privk a)) (uniq n2))
     (exists ((z1 strd))
      (strand init z1 2 (b b)))))
  (comment "Skeleton 3")
  (comment "Failed authentication goal: agreement on name b"))

(defgoal ns
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
     (and (strand resp z0 3 (n2 n2) (a a) (b b))
      (non (privk a)) (uniq n2))
     (exists ((z1 strd))
      (strand init z1 2 (b b)))))
  (comment "Skeleton 4"))
```

## locn_envelope.scm

- **File Path**: `03_examples_scm/locn_envelope.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Envelope Protocol, location-based version" (bound 30) (limit 1200))` | Flags: `(bound 30)`, `(limit 1200)`
- **Protocol & Purpose**: Protocol(s): `envelope`, `envelope-plus`, `envelope-plus-2`. Comprehensive model of the TPM Envelope Protocol using stateful locations (`locn`), channels (`chan` with `auth` and `conf`), macros (`defmacro`), and state-generation/ordering rules (`defrule` with `gen-st`). Defines three protocol variants (`envelope`, `envelope-plus`, `envelope-plus-2`) to test three scenarios: listening for the secret `v`, listening for the refusal token `(refuse pcr-id n v k aik)`, and listening for both simultaneously (which should be impossible once PCR state splitting and multi-TPM ambiguity are ruled out by `ordered-extends` and `pcr-id-identifies-pcr`).
- **Roles & Variables**:
  - *(Roles are defined via `(defmacro (roles) (^ ...))` and expanded into `envelope`, `envelope-plus`, and `envelope-plus-2`)*:
  - Role `tpm-power-on`: Vars: `(current-value mesg)`, `(pcr locn)`, `(tpm chan)` | Role Assumptions: none | Trace (3 events): `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc`: Vars: `(value current-value mesg)`, `(pcr-id text)`, `(pcr locn)`, `(tpm chan)` | Role Assumptions: none | Trace (4 events): `(recv tpm (cat "extend" pcr-id value))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote`: Vars: `(nonce current-value mesg)`, `(pcr-id text)`, `(aik akey)`, `(pcr locn)`, `(tpm chan)` | Role Assumptions: none | Trace (3 events): `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key`: Vars: `(k aik akey)`, `(pcr-id text)`, `(pcrval mesg)`, `(tpm chan)` | Role Assumptions: `(uniq-orig k)`, `(non-orig (invk k))`, `(auth tpm)` | Trace (2 events): `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt`: Vars: `(m current-value mesg)`, `(pcr-id text)`, `(k aik akey)`, `(pcr locn)`, `(tpm chan)` | Role Assumptions: `(non-orig aik)` | Trace (4 events): `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice`: Vars: `(n v data)`, `(pcr-id text)`, `(k aik akey)`, `(tpm chan)` | Role Assumptions: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpm)` | Trace (4 events): `(send tpm (cat "extend" pcr-id n))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (3)**: `(refuse pcr-id n v k aik)`, `(roles)`, `(genStV-rules)`
  - **Rules (6)**: `genStV-if-hashed-tpm-power-on`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`; `genStV-if-hashed-tpm-extend-enc`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`; `genStV-if-hashed-tpm-decrypt`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`; `genStV-if-hashed-tpm-quote`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`; `ordered-extends`: `(forall ((y z strd) (pcr locn)) (implies (and (p "tpm-extend-enc" y 3) (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "pcr" y pcr) (p "tpm-extend-enc" "pcr" z pcr)) (or (= y z) (prec y 2 z 1) (prec z 2 y 1))))`; `pcr-id-identifies-pcr`: `(forall ((y z strd) (pcr-id text) (pcr pcr-0 locn)) (implies (and (p "tpm-extend-enc" y 3) (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "pcr-id" y pcr-id) (p "tpm-extend-enc" "pcr-id" z pcr-id) (p "tpm-extend-enc" "pcr" y pcr) (p "tpm-extend-enc" "pcr" z pcr-0)) (= pcr pcr-0)))`
  - **Goals**: None
  - **Skeletons (9)**: Skeleton 1 (`envelope`): `(vars (v data))`, `(deflistener v)`, `(defstrand alice 4 (v v))` | Skeleton 2 (`envelope`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 3 (`envelope`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(deflistener v)`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 4 (`envelope-plus`): `(vars (v data))`, `(deflistener v)`, `(defstrand alice 4 (v v))` | Skeleton 5 (`envelope-plus`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 6 (`envelope-plus`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(deflistener v)`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 7 (`envelope-plus-2`): `(vars (v data))`, `(deflistener v)`, `(defstrand alice 4 (v v))` | Skeleton 8 (`envelope-plus-2`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 9 (`envelope-plus-2`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(deflistener v)`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))`
  - **Keywords & Predicates Used**: `and`, `auth`, `bound`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `forall`, `gen-st`, `herald`, `implies`, `limit`, `load`, `neq`, `non-orig`, `or`, `p`, `prec`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling stateful hardware security modules or TPM PCR `load`/`stor` transitions over authenticated/confidential channels, or when writing `gen-st` and location-equality rules (`defrule`) to prevent state splitting.
- **Key S-Expression Excerpt** (lines 89–124):
```scheme
     (vars (m current-value mesg) (pcr-id text) (k aik akey) (pcr locn) (tpm chan))
     (trace
      (recv tpm (cat "decrypt" (enc m k)))
      (recv (enc "created" k pcr-id current-value aik))
      (load pcr current-value) ;; MSR lhs (not deleted)
      (send m))
     (non-orig aik))

   ;; Alice extends a pcr with a fresh nonce in an encrypted
   ;; session.  She has the TPM create a new key whose use is
   ;; bound to the hash of pcr value she just created with the
   ;; string "obtain".  She then encrypts her fresh secret with
   ;; this newly created key.
   (defrole alice
     (vars (n v data) (pcr-id text) (k aik akey) (tpm chan))
     (trace
      (send tpm (cat "extend" pcr-id n))
      (send tpm (cat "create-req"pcr-id (hash (hash "0" n) "obtain")))
      ;; (enc "create key" (hash (hash "0" n) "obtain") esk)
      (recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))
      (send (enc v k)))
     (neq (k aik))
     (uniq-orig n v)
     (non-orig aik)
     (conf tpm))))

(defmacro (genStV-rules)
  (^
   (defrule genStV-if-hashed-tpm-power-on
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-power-on" z 2)
	(p "tpm-power-on" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))
```

## missing_contraction.scm

- **File Path**: `03_examples_scm/missing_contraction.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `missing-contraction`. Regression and diagnostic test case (`missing-contraction`) illustrating a subtlety in CPSA's cohort generation where solving a test node requires displacement/augmentation rather than ordinary contraction because `(enc a n (pubk b))` is not in the escape set of `(enc a m (pubk a))`.
- **Roles & Variables**:
  - Role `sender`: Vars: `(m n text)`, `(a b name)` | Role Assumptions: none | Trace (2 events): `(send (enc a m (pubk a)))` -> `(send (enc a n (pubk b)))`
  - Role `receiver`: Vars: `(m text)`, `(a b name)` | Role Assumptions: none | Trace (1 events): `(recv (enc a m (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`missing-contraction`): `(vars (m text) (a c name))`, `(defstrand sender 2 (m m) (a a))`, `(defstrand receiver 1 (m m) (a a) (b c))`, `(precedes ((0 1) (1 0)))`, `(uniq-orig m)`, `(non-orig (privk a))` | Skeleton 2 (`missing-contraction`): `(vars (m text) (a c name))`, `(defstrand sender 1 (m m) (a a))`, `(deflistener (enc a m (pubk c)))`, `(uniq-orig m)`, `(non-orig (privk a))` | Skeleton 3 (`missing-contraction`): `(vars (m text) (a b c name))`, `(defstrand sender 2 (m m) (a a) (b b))`, `(defstrand receiver 1 (m m) (a a) (b c))`, `(precedes ((0 1) (1 0)))`, `(uniq-orig m)`, `(non-orig (privk a) (privk b))`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example to understand how CPSA handles multiple encrypted transmissions from the same strand when a nonce `m` originates in one encryption `(enc a m (pubk a))` and is expected in another `(enc a m (pubk b))`.
- **Key S-Expression Excerpt** (lines 21–54):
```scheme

(defprotocol missing-contraction basic
  (defrole sender
    (vars (m n text) (a b name))
    (trace
     (send (enc a m (pubk a)))
     (send (enc a n (pubk b)))))
  (defrole receiver
    (vars (m text) (a b name))
    (trace
     (recv (enc a m (pubk b))))))

(defskeleton missing-contraction
  (vars (m text) (a c name))
  (defstrand sender 2 (m m) (a a))
  (defstrand receiver 1 (m m) (a a) (b c))
  (precedes ((0 1) (1 0)))
  (uniq-orig m)
  (non-orig (privk a)))

(defskeleton missing-contraction
  (vars (m text) (a c name))
  (defstrand sender 1 (m m) (a a))
  (deflistener (enc a m (pubk c)))
  (uniq-orig m)
  (non-orig (privk a)))

(defskeleton missing-contraction
  (vars (m text) (a b c name))
  (defstrand sender 2 (m m) (a a) (b b))
  (defstrand receiver 1 (m m) (a a) (b c))
  (precedes ((0 1) (1 0)))
  (uniq-orig m)
  (non-orig (privk a) (privk b)))
```

## neq_test.scm

- **File Path**: `03_examples_scm/neq_test.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Inequality constraint using facts and rules" (comment "First skeleton should have a shape," "second should be dead."))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `neq-test`. Demonstrates how to enforce an inequality constraint (`n1 != n2`) in CPSA using a custom `(facts (neq n1 n2))` declaration in `defskeleton` paired with a protocol rule `(defrule neq (forall ((a mesg)) (implies (fact neq a a) (false))))`. In the first skeleton (without the inequality fact), CPSA finds a shape by unifying `n1 = n2`; in the second skeleton (with `(facts (neq n1 n2))`), the unification `n1 = n2` triggers `(fact neq a a) -> (false)` and kills the branch, yielding a dead skeleton (no shapes).
- **Roles & Variables**:
  - Role `init`: Vars: `(n1 n2 text)`, `(k skey)` | Role Assumptions: `(non-orig k)`, `(uniq-orig n1 n2)` | Trace (2 events): `(send (cat n1 (enc n1 n2 k)))` -> `(recv n2)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `neq`: `(forall ((a mesg)) (implies (fact neq a a) (false)))`
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`neq-test`): `(vars)`, `(defstrand init 2)` | Skeleton 2 (`neq-test`): `(vars (n1 n2 text))`, `(defstrand init 2 (n1 n1) (n2 n2))`, `(facts (neq n1 n2))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `false`, `forall`, `herald`, `implies`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example whenever you need to assert that two terms or variables are distinct (`x != y`) in a CPSA skeleton using `(facts (neq x y))` and the standard `neq` falsification rule.
- **Key S-Expression Excerpt** (lines 1–30):
```scheme
(herald "Inequality constraint using facts and rules"
	(comment "First skeleton should have a shape,"
		 "second should be dead."))

(defprotocol neq-test basic
  (defrole init
    (vars (n1 n2 text) (k skey))
    (trace
     (send (cat n1 (enc n1 n2 k)))
     (recv n2))
    (non-orig k)
    (uniq-orig n1 n2))
  (defrule neq
    (forall ((a mesg))
	    (implies
	     (fact neq a a)
	     (false)))))

;;; With no inequality fact,
;;; a shape should be found where n1 = n2.
(defskeleton neq-test
  (vars)
  (defstrand init 2))

;;; With an inequality fact,
;;; no shape should exist.
(defskeleton neq-test
   (vars (n1 n2 text))
   (defstrand init 2 (n1 n1) (n2 n2))
   (facts (neq n1 n2)))			;  assert n1 != n2
```

## neuman-stubblebine.scm

- **File Path**: `03_examples_scm/neuman-stubblebine.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `neuman-stubblebine`. Models the initial exchange of the Neuman-Stubblebine authentication and key distribution protocol (`neuman-stubblebine`) with three roles (`init`, `resp`, `keyserver`) using symmetric long-term keys `(ltk a ks)` and `(ltk b ks)` and fresh session key `k`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b ks name)`, `(ra rb text)`, `(k skey)`, `(tb text)` | Role Assumptions: none | Trace (3 events): `(send (cat a ra))` -> `(recv (cat (enc b ra k tb (ltk a ks)) (enc a k tb (ltk b ks)) rb))` -> `(send (cat (enc a k tb (ltk b ks)) (enc rb k)))`
  - Role `resp`: Vars: `(a b ks name)`, `(ra rb text)`, `(k skey)`, `(tb text)` | Role Assumptions: none | Trace (3 events): `(recv (cat a ra))` -> `(send (cat b rb (enc a ra tb (ltk b ks))))` -> `(recv (cat (enc a k tb (ltk b ks)) (enc rb k)))`
  - Role `keyserver`: Vars: `(a b ks name)`, `(ra rb text)`, `(k skey)`, `(tb text)` | Role Assumptions: `(uniq-orig k)` | Trace (2 events): `(recv (cat b rb (enc a ra tb (ltk b ks))))` -> `(send (cat (enc b ra k tb (ltk a ks)) (enc a k tb (ltk b ks)) rb))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`neuman-stubblebine`): `(vars (a b ks name) (ra rb text))`, `(defstrand init 3 (a a) (b b) (ks ks) (ra ra) (rb rb))`, `(uniq-orig ra rb)`, `(non-orig (ltk a ks) (ltk b ks))` | Skeleton 2 (`neuman-stubblebine`): `(vars (a b ks name) (ra rb text))`, `(defstrand resp 3 (a a) (b b) (ks ks) (ra ra) (rb rb))`, `(uniq-orig ra rb)`, `(non-orig (ltk a ks) (ltk b ks))` | Skeleton 3 (`neuman-stubblebine`): `(vars (a b ks name) (ra rb text))`, `(defstrand keyserver 2 (a a) (b b) (ks ks) (ra ra) (rb rb))`, `(uniq-orig ra rb)`, `(non-orig (ltk a ks) (ltk b ks))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling three-party symmetric key distribution protocols with timestamps/lifetimes (`tb`) and dual nonces (`ra`, `rb`) where the responder forwards the initiator's challenge to the key server.
- **Key S-Expression Excerpt** (lines 1–37):
```scheme
(defprotocol neuman-stubblebine basic
  (defrole init (vars (a b ks name) (ra rb text) (k skey) (tb text))
    (trace
     (send (cat a ra))
     (recv (cat (enc b ra k tb (ltk a ks))
		(enc a k tb (ltk b ks)) rb))
     (send (cat (enc a k tb (ltk b ks)) (enc rb k)))))
  (defrole resp (vars (a b ks name) (ra rb text) (k skey) (tb text))
    (trace
     (recv (cat a ra))
     (send (cat b rb (enc a ra tb (ltk b ks))))
     (recv (cat (enc a k tb (ltk b ks)) (enc rb k)))))
  (defrole keyserver
    (vars (a b ks name) (ra rb text) (k skey) (tb text))
    (trace
     (recv (cat b rb (enc a ra tb (ltk b ks))))
     (send (cat (enc b ra k tb (ltk a ks))
		(enc a k tb (ltk b ks)) rb)))
    (uniq-orig k)))

(defskeleton neuman-stubblebine
  (vars (a b ks name) (ra rb text))
  (defstrand init 3 (a a) (b b) (ks ks) (ra ra) (rb rb))
  (uniq-orig ra rb)
  (non-orig (ltk a ks) (ltk b ks)))

(defskeleton neuman-stubblebine
  (vars (a b ks name) (ra rb text))
  (defstrand resp 3 (a a) (b b) (ks ks) (ra ra) (rb rb))
  (uniq-orig ra rb)
  (non-orig (ltk a ks) (ltk b ks)))

(defskeleton neuman-stubblebine
  (vars (a b ks name) (ra rb text))
  (defstrand keyserver 2 (a a) (b b) (ks ks) (ra ra) (rb rb))
  (uniq-orig ra rb)
  (non-orig (ltk a ks) (ltk b ks)))
```

## no_contraction.scm

- **File Path**: `03_examples_scm/no_contraction.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `no-contraction`. Minimal test case (`no-contraction`) where `init` sends a nested signed-then-encrypted term `(enc (enc n (privk a)) (pubk b))` without `b`'s private key being non-originating, while `resp` receives the inner signed term `(enc n (privk a))`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n text)` | Role Assumptions: none | Trace (1 events): `(send (enc (enc n (privk a)) (pubk b)))`
  - Role `resp`: Vars: `(a name)`, `(n text)` | Role Assumptions: none | Trace (1 events): `(recv (enc n (privk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`no-contraction`): `(vars (a b name) (n m text))`, `(defstrand resp 1 (a a) (n n))`, `(defstrand init 1 (n n))`, `(uniq-orig n)`, `(non-orig (privk a))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example as a minimal template for nested sign-then-encrypt (`(enc (enc n (privk a)) (pubk b))`) where the outer encryption key `(pubk b)` is unconstrained so the penetrator can strip the outer layer.
- **Key S-Expression Excerpt** (lines 1–16):
```scheme
(defprotocol no-contraction basic
  (defrole init
    (vars (a b name) (n text))
    (trace
     (send (enc (enc n (privk a))(pubk b)))))
  (defrole resp
    (vars (a name) (n text))
    (trace
     (recv (enc n (privk a))))))

(defskeleton no-contraction
  (vars (a b name) (n m text))
  (defstrand resp 1 (a a) (n n))
  (defstrand init 1 (n n))
  (uniq-orig n)
  (non-orig (privk a)))
```

## non_transforming.scm

- **File Path**: `03_examples_scm/non_transforming.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `non_transforming`. Regression test (`non_transforming`) illustrating a corner case in CPSA's augmentation step: augmenting a skeleton containing `recv` and two `sender` strands with `(breaker 3)` causes unification (`a = b`) such that the 3rd node of `breaker` sends the exact same term `(enc a (pubk B))` as the 2nd node and is therefore no longer a transforming node.
- **Roles & Variables**:
  - Role `sender`: Vars: `(a b text)`, `(B name)` | Role Assumptions: `(uniq-orig a b)`, `(non-orig (privk B))` | Trace (1 events): `(send (enc a b (pubk B)))`
  - Role `recv`: Vars: `(a b text)`, `(B name)` | Role Assumptions: none | Trace (2 events): `(recv (enc a (pubk B)))` -> `(recv (enc b (pubk B)))`
  - Role `breaker`: Vars: `(a b text)`, `(B name)` | Role Assumptions: none | Trace (3 events): `(recv (enc a b (pubk B)))` -> `(send (enc a (pubk B)))` -> `(send (enc b (pubk B)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`non_transforming`): `(vars (a b c d text) (B B0 B1 name))`, `(defstrand recv 2 (a a) (b b) (B B))`, `(defstrand sender 1 (a a) (b d) (B B0))`, `(defstrand sender 1 (a c) (b b) (B B1))`, `(precedes ((1 0) (0 0)) ((2 0) (0 1)))`, `(uniq-orig a b)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when studying how CPSA's augmentation and unification interact when a helper/breaker role decomposes a pair `(enc a b (pubk B))` into separate components `(enc a (pubk B))` and `(enc b (pubk B))`.
- **Key S-Expression Excerpt** (lines 9–42):
```scheme
(defprotocol non_transforming basic
  (defrole sender
    (vars (a b text) (B name))
    (trace
      (send (enc a b (pubk B)))
    )
    (uniq-orig a b)
    (non-orig (privk B))
  )
  (defrole recv
    (vars (a b text) (B name))
    (trace
      (recv (enc a (pubk B)))
      (recv (enc b (pubk B)))
    )
  )
  (defrole breaker
    (vars (a b text) (B name))
    (trace
       (recv (enc a b (pubk B)))
       (send (enc a (pubk B)))
       (send (enc b (pubk B)))
    )
  )
)

(defskeleton non_transforming
  (vars (a b c d text) (B B0 B1 name))
  (defstrand recv 2 (a a) (b b) (B B))
  (defstrand sender 1 (a a) (b d) (B B0))
  (defstrand sender 1 (a c) (b b) (B B1))
  (precedes ((1 0) (0 0)) ((2 0) (0 1)))
  (uniq-orig a b)
)
```

## nonaug-prune.scm

- **File Path**: `03_examples_scm/nonaug-prune.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `nonaug-prune`. Regression test (`nonaug-prune`) demonstrating that CPSA can prune two existing strands (`trans2`) of a parent skeleton after augmenting with a new strand when variable unifications (`A = B`) make one strand redundant.
- **Roles & Variables**:
  - Role `orig`: Vars: `(n text)`, `(A B name)`, `(k akey)` | Role Assumptions: `(uniq-orig n)`, `(non-orig (invk k))` | Trace (3 events): `(send (enc n B B k))` -> `(send (enc n A k))` -> `(recv (enc n A A A k))`
  - Role `trans1`: Vars: `(n text)`, `(A C name)`, `(k akey)` | Role Assumptions: none | Trace (3 events): `(recv (enc n A A k))` -> `(recv (enc n A k))` -> `(send (enc n n C k))`
  - Role `trans2`: Vars: `(n text)`, `(A name)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc n A k))` -> `(send (enc n A A A k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`nonaug-prune`): `(vars (n text) (A B name) (k akey))`, `(defstrand trans2 2 (n n) (A B) (k k))`, `(defstrand trans2 2 (n n) (A A) (k k))`, `(defstrand orig 3 (n n) (A A) (B B) (k k))`, `(precedes ((2 0) (0 0)) ((2 0) (1 0)))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when analyzing strand pruning and generalization behavior in preskeletons with multiple instances of the same role (`trans2`) bound to different role parameters.
- **Key S-Expression Excerpt** (lines 5–42):
```scheme
(defprotocol nonaug-prune basic
  (defrole orig
    (vars (n text) (A B name) (k akey))
    (trace
     (send (enc n B B k))
     (send (enc n A k))
     (recv (enc n A A A k)))
    (uniq-orig n)
    (non-orig (invk k)))
  (defrole trans1
    (vars (n text) (A C name) (k akey))
    (trace
     (recv (enc n A A k))
     (recv (enc n A k))
     (send (enc n n C k))))
  (defrole trans2
    (vars (n text) (A name) (k akey))
    (trace
     (recv (enc n A k))
     (send (enc n A A A k))))
)

;; (defskeleton nonaug-prune
;;   (vars (n text) (A B C name) (k akey))
;;   (defstrand trans1 3 (n n) (A A) (C C) (k k))
;;   (defstrand orig 3 (n n) (A A) (B B) (k k))
;;   (precedes ((1 0) (0 0)) ((0 2) (1 2))))

;; (defskeleton nonaug-prune
;;   (vars (n text) (A B name) (k akey))
;;   (defstrand orig 3 (n n) (A A) (B B) (k k)))

(defskeleton nonaug-prune
  (vars (n text) (A B name) (k akey))
  (defstrand trans2 2 (n n) (A B) (k k))
  (defstrand trans2 2 (n n) (A A) (k k))
  (defstrand orig 3 (n n) (A A)(B B) (k k))
  (precedes ((2 0) (0 0)) ((2 0) (1 0))))
```

## ns-l.scm

- **File Path**: `03_examples_scm/ns-l.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Needham-Schroeder-Low Public-Key Protocol" (comment "With deflistener's"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. Models the Needham-Schroeder-Lowe Public-Key Protocol (`ns`, with Lowe's fix including responder identity `b` in message 2: `(enc b n1 n2 (pubk a))`) and includes `(deflistener n1)` and `(deflistener n2)` in the initiator and responder skeletons to verify nonce secrecy alongside authentication.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 text)` | Role Assumptions: none | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc b n1 n2 (pubk a)))` -> `(send (enc n2 (pubk b)))`
  - Role `resp`: Vars: `(b a name)`, `(n2 n1 text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc b n1 n2 (pubk a)))` -> `(recv (enc n2 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(deflistener n1)`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 2 (`ns`): `(vars (a name) (n2 text))`, `(defstrand resp 3 (a a) (n2 n2))`, `(deflistener n2)`, `(non-orig (privk a))`, `(uniq-orig n2)`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for the canonical Needham-Schroeder-Lowe public-key protocol model and the standard pattern for testing nonce confidentiality using `(deflistener <nonce>)` inside `(defskeleton ...)`.
- **Key S-Expression Excerpt** (lines 1–38):
```scheme
(herald "Needham-Schroeder-Low Public-Key Protocol"
	(comment "With deflistener's"))

;;; Used to generate output for inclusion in the primer.
;;; Use margin = 60 (-m 60) to generate the output.

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc b n1 n2 (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc b n1 n2 (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder"))

;;; The initiator point-of-view
(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (deflistener n1)
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Initiator point-of-view with a listener"))

;;; The responder point-of-view
(defskeleton ns
  (vars (a name) (n2 text))
  (defstrand resp 3 (a a) (n2 n2))
  (deflistener n2)
  (non-orig (privk a))
  (uniq-orig n2)
  (comment "Responder point-of-view with a listener"))
```

## ns-rebinding.scm

- **File Path**: `03_examples_scm/ns-rebinding.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "ALternate Needham-Schroeder Public-Key Protocol Variants")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. Tests variable rebinding and existential quantification in the conclusion of a rule (`rebind-x`: `(forall ((x y text)) (implies (fact rel1 x y) (exists ((x name)) (fact rel2 x y))))`, where `x` is rebound from sort `text` to sort `name`), alongside role-level `(facts (rel1 n1 n2) (rel2 n1 n2))` and double-initiator skeletons on the Needham-Schroeder-Lowe protocol.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 text)` | Role Assumptions: `(facts (rel1 n1 n2) (rel2 n1 n2))` | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc n1 n2 b (pubk a)))` -> `(send (enc n2 (pubk b)))`
  - Role `resp`: Vars: `(b a name)`, `(n2 n1 text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 b (pubk a)))` -> `(recv (enc n2 (pubk b)))`
  - *(Commented-out role)*: Top-level `(comment (defrole keyserver ...))` also illustrates a `guar` event `(guar (and (long-term-key ks a kas) (long-term-key ks b kbs)))`.
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `rebind-x`: `(forall ((x y text)) (implies (fact rel1 x y) (exists ((x name)) (fact rel2 x y))))`
  - **Goals**: None
  - **Skeletons (8)**: Skeleton 1 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 2 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)`, `(facts (rel n1 n1))` | Skeleton 3 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b))`, `(uniq-orig n1)` | Skeleton 4 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(deflistener n1)`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 5 (`ns`): `(vars (a b name) (n1 n1-0 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(defstrand init 3 (a a) (b b) (n1 n1-0))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1 n1-0)` | Skeleton 6 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 7 (`ns`): `(vars (a name) (n2 text))`, `(defstrand resp 3 (a a) (n2 n2))`, `(non-orig (privk a))`, `(uniq-orig n2)` | Skeleton 8 (`ns`): `(vars (x name) (n1 n2 text) (a b name))`, `(defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))`, `(non-orig (privk a) (privk b))`, `(uniq-orig n1)`, `(facts (rel2 x n2) (rel1 n1 n2) (rel2 n1 n2))`
  - **Keywords & Predicates Used**: `comment`, `deflistener`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `exists`, `fact`, `facts`, `forall`, `herald`, `implies`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when attaching custom `(facts ...)` directly inside a `(defrole ...)` definition or when testing variable shadowing/rebinding in `(defrule ...)` existential conclusions.
- **Key S-Expression Excerpt** (lines 15–47):
```scheme
(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 b (pubk a)))
     (send (enc n2 (pubk b))))
    (facts (rel1 n1 n2)
	   (rel2 n1 n2)))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 b (pubk a)))
     (recv (enc n2 (pubk b)))))

  (defrule rebind-x 			; This rule tests rebinding in the conclusion of a rule.
    (forall
     ((x y text))
     (implies
      (fact rel1 x y)
      (exists ((x name)) (fact rel2 x y)))))

  (comment "Needham-Schroeder with no role origination assumptions"))

;;; The initiator point-of-view
(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Initiator point-of-view"))

```

## ns.scm

- **File Path**: `03_examples_scm/ns.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Needham-Schroeder Public-Key Protocol" (comment "This protocol contains a man-in-the-middle" "attack discovered by Gavin Lowe."))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. The classic original Needham-Schroeder Public-Key Protocol (`ns`) from the CPSA Primer, where message 2 is `(enc n1 n2 (pubk a))` (omitting `b`'s identity), which exhibits Gavin Lowe's famous man-in-the-middle attack when analyzed from the responder's point of view.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 text)` | Role Assumptions: none | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc n1 n2 (pubk a)))` -> `(send (enc n2 (pubk b)))`
  - Role `resp`: Vars: `(b a name)`, `(n2 n1 text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 (pubk a)))` -> `(recv (enc n2 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 2 (`ns`): `(vars (a name) (n2 text))`, `(defstrand resp 3 (a a) (n2 n2))`, `(non-orig (privk a))`, `(uniq-orig n2)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example as the canonical baseline for public-key challenge-response modeling in CPSA and to see why responder point-of-view analysis fails when the responder's identity `b` is omitted from `(enc n1 n2 (pubk a))`.
- **Key S-Expression Excerpt** (lines 1–37):
```scheme
(herald "Needham-Schroeder Public-Key Protocol"
	(comment "This protocol contains a man-in-the-middle"
		 "attack discovered by Gavin Lowe."))

;;; Used to generate output for inclusion in the primer.
;;; Use margin = 60 (-m 60) to generate the output.

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder"))

;;; The initiator point-of-view
(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Initiator point-of-view"))

;;; The responder point-of-view
(defskeleton ns
  (vars (a name) (n2 text))
  (defstrand resp 3 (a a) (n2 n2))
  (non-orig (privk a))
  (uniq-orig n2)
  (comment "Responder point-of-view"))
```

## nsl3.scm

- **File Path**: `03_examples_scm/nsl3.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Three Party Needham-Schroeder-Lowe Protocol")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `nsl3`. Models a Three-Party Needham-Schroeder-Lowe Protocol (`nsl3`) with roles `init` (`a`), `mid` (`b`), and `resp` (`c`), where each participant originates two fresh nonces (`na0 na1`, `nb0 nb1`, `nc0 nc1`) and forwards nested public-key encrypted tickets to establish mutual authentication across all three parties.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b c name)`, `(na0 na1 nb0 nb1 nc0 nc1 text)` | Role Assumptions: `(uniq-orig na0 na1)` | Trace (3 events): `(send (enc na0 a c (enc na1 a b (pubk c)) (pubk b)))` -> `(recv (enc na1 nc1 c b (enc na0 nb0 b c (pubk a)) (enc nb1 nc0 c a (pubk b)) (pubk a)))` -> `(send (enc nb0 (enc nb1 nc0 c a (pubk b)) (enc nc1 (pubk c)) (pubk b)))`
  - Role `mid`: Vars: `(a b c name)`, `(na0 na1 nb0 nb1 nc0 nc1 text)` | Role Assumptions: `(uniq-orig nb0 nb1)` | Trace (4 events): `(recv (enc na0 a c (enc na1 a b (pubk c)) (pubk b)))` -> `(send (enc nb1 b a (enc na1 a b (pubk c)) (enc na0 nb0 b c (pubk a)) (pubk c)))` -> `(recv (enc nb0 (enc nb1 nc0 c a (pubk b)) (enc nc1 (pubk c)) (pubk b)))` -> `(send (enc nc0 (enc nc1 (pubk c)) (pubk c)))`
  - Role `resp`: Vars: `(a b c name)`, `(na0 na1 nb0 nb1 nc0 nc1 text)` | Role Assumptions: `(uniq-orig nc0 nc1)` | Trace (3 events): `(recv (enc nb1 b a (enc na1 a b (pubk c)) (enc na0 nb0 b c (pubk a)) (pubk c)))` -> `(send (enc na1 nc1 c b (enc na0 nb0 b c (pubk a)) (enc nb1 nc0 c a (pubk b)) (pubk a)))` -> `(recv (enc nc0 (enc nc1 (pubk c)) (pubk c)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`nsl3`): `(vars (a b c name))`, `(defstrand init 3 (a a) (b b) (c c))`, `(non-orig (privk a) (privk b) (privk c))` | Skeleton 2 (`nsl3`): `(vars (a b c name))`, `(defstrand mid 4 (a a) (b b) (c c))`, `(non-orig (privk a) (privk b) (privk c))` | Skeleton 3 (`nsl3`): `(vars (a b c name))`, `(defstrand resp 3 (a a) (b b) (c c))`, `(non-orig (privk a) (privk b) (privk c))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling multi-party (3+ participant) public-key authentication protocols with nested encrypted forwarding tickets (`(enc ... (enc ... (pubk c)) (pubk b))`).
- **Key S-Expression Excerpt** (lines 1–41):
```scheme
(herald "Three Party Needham-Schroeder-Lowe Protocol")

(defprotocol nsl3 basic
  (defrole init (vars (a b c name) (na0 na1 nb0 nb1 nc0 nc1 text))
    (trace
     (send (enc na0 a c (enc na1 a b (pubk c)) (pubk b)))
     (recv (enc na1 nc1 c b
		(enc na0 nb0 b c (pubk a))
		(enc nb1 nc0 c a (pubk b))
		(pubk a)))
     (send (enc nb0
		(enc nb1 nc0 c a (pubk b))
		(enc nc1 (pubk c))
		(pubk b))))
    (uniq-orig na0 na1))
  (defrole mid (vars (a b c name) (na0 na1 nb0 nb1 nc0 nc1 text))
    (trace
     (recv (enc na0 a c (enc na1 a b (pubk c)) (pubk b)))
     (send (enc nb1 b a
		(enc na1 a b (pubk c))
		(enc na0 nb0 b c (pubk a))
		(pubk c)))
     (recv (enc nb0
		(enc nb1 nc0 c a (pubk b))
		(enc nc1 (pubk c))
		(pubk b)))
     (send (enc nc0 (enc nc1 (pubk c)) (pubk c))))
    (uniq-orig nb0 nb1))
  (defrole resp (vars (a b c name) (na0 na1 nb0 nb1 nc0 nc1 text))
    (trace
     (recv (enc nb1 b a
		(enc na1 a b (pubk c))
		(enc na0 nb0 b c (pubk a))
		(pubk c)))
     (send (enc na1 nc1 c b
		(enc na0 nb0 b c (pubk a))
		(enc nb1 nc0 c a (pubk b))
		(pubk a)))
     (recv (enc nc0 (enc nc1 (pubk c)) (pubk c))))
    (uniq-orig nc0 nc1)))

```

## nslsk.scm

- **File Path**: `03_examples_scm/nslsk.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Needham-Schroeder-Lowe Protocol with symmetric encryption")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `nslsk`, `nslsk-tag-term`. Models the Needham-Schroeder-Lowe protocol used to distribute a fresh symmetric session key `(k skey)` (`nslsk`) followed by a confirmation message `(enc t k)`, along with a second protocol variant (`nslsk-tag-term`) where the confirmation payload is a constant string literal tag `(enc "t" k)`.
- **Roles & Variables**:
  - Role `init` (in `nslsk`): Vars: `(a b name)`, `(n text)`, `(k skey)`, `(t text)` | Role Assumptions: none | Trace (3 events): `(send (enc n a (pubk b)))` -> `(recv (enc n k b (pubk a)))` -> `(send (enc t k))`
  - Role `resp` (in `nslsk`): Vars: `(b a name)`, `(n text)`, `(k skey)`, `(t text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n a (pubk b)))` -> `(send (enc n k b (pubk a)))` -> `(recv (enc t k))`
  - Role `init` (in `nslsk-tag-term`): Vars: `(a b name)`, `(n text)`, `(k skey)` | Role Assumptions: none | Trace (3 events): `(send (enc n a (pubk b)))` -> `(recv (enc n k b (pubk a)))` -> `(send (enc "t" k))`
  - Role `resp` (in `nslsk-tag-term`): Vars: `(b a name)`, `(n text)`, `(k skey)` | Role Assumptions: none | Trace (3 events): `(recv (enc n a (pubk b)))` -> `(send (enc n k b (pubk a)))` -> `(recv (enc "t" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (4)**: Skeleton 1 (`nslsk`): `(vars (a name) (k skey))`, `(defstrand resp 3 (a a) (k k))`, `(non-orig (privk a))`, `(uniq-orig k)` | Skeleton 2 (`nslsk`): `(vars (b name) (n text))`, `(defstrand init 3 (b b) (n n))`, `(non-orig (privk b))`, `(uniq-orig n)` | Skeleton 3 (`nslsk-tag-term`): `(vars (a name) (k skey))`, `(defstrand resp 3 (a a) (k k))`, `(non-orig (privk a))`, `(uniq-orig k)` | Skeleton 4 (`nslsk-tag-term`): `(vars (b name) (n text))`, `(defstrand init 3 (b b) (n n))`, `(non-orig (privk b))`, `(uniq-orig n)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling hybrid public-key / symmetric-key handshakes (where an asymmetric exchange establishes a symmetric `skey` `k` used to encrypt subsequent traffic or a constant confirmation tag `"t"`).
- **Key S-Expression Excerpt** (lines 1–40):
```scheme
(herald "Needham-Schroeder-Lowe Protocol with symmetric encryption")

(defprotocol nslsk basic
  (defrole init (vars (a b name) (n text) (k skey) (t text))
    (trace
     (send (enc n a (pubk b)))
     (recv (enc n k b (pubk a)))
     (send (enc t k))))
  (defrole resp (vars (b a name) (n text) (k skey) (t text))
    (trace
     (recv (enc n a (pubk b)))
     (send (enc n k b (pubk a)))
     (recv (enc t k)))))

(defskeleton nslsk
  (vars (a name) (k skey))
  (defstrand resp 3 (a a) (k k))
  (non-orig (privk a))
  (uniq-orig k))

(defskeleton nslsk
  (vars (b name) (n text))
  (defstrand init 3 (b b) (n n))
  (non-orig (privk b))
  (uniq-orig n))

;; Use a tag as a term.

(defprotocol nslsk-tag-term basic
  (defrole init (vars (a b name) (n text) (k skey))
    (trace
     (send (enc n a (pubk b)))
     (recv (enc n k b (pubk a)))
     (send (enc "t" k))))
  (defrole resp (vars (b a name) (n text) (k skey))
    (trace
     (recv (enc n a (pubk b)))
     (send (enc n k b (pubk a)))
     (recv (enc "t" k)))))

```

## open-closed-multiloc.scm

- **File Path**: `03_examples_scm/open-closed-multiloc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald open-closed (bound 44))` | Flags: `(bound 44)` (commented-out flags in source: `(try-old-strands)`, `(check-nonces)`, `(reverse-nodes)`)
- **Protocol & Purpose**: Protocol(s): `open-closed`. Models a stateful device access-control protocol (`open-closed`) using two distinct state locations (`lk` for key state and `ls` for open/closed status), an authenticated/confidential power-up channel (`start-ch` of sort `chan`), macros (`defmacro`) encoding state terms (`(opened o)` as `(cat o o)`, `(closed o)` as `o`), and rules (`gen-state-close`, `gen-state-pass`, `power-deliver-once`) using `(gen-st ...)`.
- **Roles & Variables**:
  - Role `dev-up`: Vars: `(k skey)`, `(d o name)`, `(old old1 mesg)`, `(start-ch chan)`, `(lk ls locn)` | Role Assumptions: `(auth start-ch)` | Trace (6 events): `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(load ls old1)` -> `(stor ls (dev-state-closed d o))` -> `(stor lk (dev-key-state d o k))` -> `(send (enc "up" k))`
  - Role `owner-power-dev`: Vars: `(k skey)`, `(d o name)`, `(start-ch chan)` | Role Assumptions: `(conf start-ch)` | Trace (2 events): `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "open" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-opened d o))` -> `(send n)`
  - Role `dev-close`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "close" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-closed d o))` -> `(send n)`
  - Role `dev-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: `(uniq-orig n)` | Trace (4 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "may I pass" k))` -> `(load ls (dev-state-opened d o))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(l locn)` | Role Assumptions: none | Trace (2 events): `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (6)**: `(dev-key-state d o k)`, `(opened o)`, `(closed o)`, `(dev-state-opened d o)`, `(dev-state-closed d o)`, `(dev-state-any d o any)`
  - **Rules (3)**: `gen-state-close`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-close" z 1) (p "dev-close" "d" z d) (p "dev-close" "o" z o) (p "dev-close" "k" z k) (p "dev-close" "any" z (opened o))) (gen-st (dev-state-opened d o))))`; `gen-state-pass`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "d" z d) (p "dev-pass" "o" z o) (p "dev-pass" "k" z k)) (gen-st (dev-state-opened d o))))`; `power-deliver-once`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(deflistener k)`, `(uniq-orig k)` | Skeleton 2 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand dev-pass 4 (k k))` | Skeleton 3 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(defstrand dev-pass 4 (k k))`, `(uniq-orig k)`
  - **Keywords & Predicates Used**: `and`, `auth`, `bound`, `comment`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `forall`, `gen-st`, `herald`, `implies`, `load`, `p`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling hardware or protocol state machines with multiple `locn` registers (`lk`, `ls`), channel assumptions (`(auth start-ch)`, `(conf start-ch)`), and `(gen-st ...)` rules.
- **Key S-Expression Excerpt** (lines 24–59):
```scheme
(defprotocol open-closed basic
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))
    (trace
     (recv start-ch (cat "power-up" d o k))
     (load lk old)
     (load ls old1)
     (stor ls (dev-state-closed d o))
     (stor lk (dev-key-state d o k))
     (send (enc "up" k)))
    (auth start-ch))

  (defrole owner-power-dev
    (vars (k skey) (d o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" d o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "open" d o n k))
     (recv n)))

  (defrole owner-close
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "close" d o n k))
     (recv n)))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "open" d o n k))
```

## open-closed-tag.scm

- **File Path**: `03_examples_scm/open-closed-tag.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald open-closed (bound 44))` | Flags: `(bound 44)` (commented-out flags in source: `(try-old-strands)`, `(check-nonces)`, `(reverse-nodes)`)
- **Protocol & Purpose**: Protocol(s): `open-closed`. Variant of the stateful `open-closed` device protocol where the `opened` and `closed` state macros use string literal tags (`"opened"` and `"closed"`) instead of name-based encodings, and includes an explicit realized 5-strand skeleton showing how `dev-open` and `dev-up` interact across multiple locations (`lk`, `lk-0`, `ls`, `ls-0`).
- **Roles & Variables**:
  - Role `dev-up`: Vars: `(k skey)`, `(d o name)`, `(old old1 mesg)`, `(start-ch chan)`, `(lk ls locn)` | Role Assumptions: `(auth start-ch)` | Trace (6 events): `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(stor lk (dev-key-state d o k))` -> `(load ls old1)` -> `(stor ls (dev-state-closed d o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev`: Vars: `(k skey)`, `(d o name)`, `(start-ch chan)` | Role Assumptions: `(conf start-ch)` | Trace (2 events): `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "open" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-opened d o))` -> `(send n)`
  - Role `dev-close`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "close" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-closed d o))` -> `(send n)`
  - Role `dev-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: `(uniq-orig n)` | Trace (4 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "may I pass" k))` -> `(load ls (dev-state-opened d o))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(l locn)` | Role Assumptions: none | Trace (2 events): `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (6)**: `(dev-key-state d o k)`, `(opened o)`, `(closed o)`, `(dev-state-opened d o)`, `(dev-state-closed d o)`, `(dev-state-any d o any)`
  - **Rules (3)**: `gen-state-close`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-close" z 1) (p "dev-close" "d" z d) (p "dev-close" "o" z o) (p "dev-close" "k" z k) (p "dev-close" "any" z (opened o))) (gen-st (dev-state-opened d o))))`; `gen-state-pass`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "d" z d) (p "dev-pass" "o" z o) (p "dev-pass" "k" z k)) (gen-st (dev-state-opened d o))))`; `power-deliver-once`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
  - **Goals**: None
  - **Skeletons (4)**: Skeleton 1 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(deflistener k)`, `(uniq-orig k)` | Skeleton 2 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand dev-pass 4 (k k))` | Skeleton 3 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(defstrand dev-pass 4 (k k))`, `(uniq-orig k)` | Skeleton 4 (`open-closed`): `(vars (old old1 any mesg) (n n-0 text) (d o name) (k k-0 skey) (start-ch chan) (ls lk ls-0 lk-0 locn))`, `(defstrand owner-power-dev 2 (d d) (o o) (k k) (start-ch start-ch))`, `(defstrand dev-pass 4 (n n) (d d) (o o) (k k) (lk lk) (ls ls))`, `(defstrand dev-up 6 (old old) (old1 old1) (d d) (o o) (k k) (start-ch start-ch) (lk lk) (ls ls-0))`, `(defstrand user-pass 1 (k k))`, `(defstrand dev-open 4 (any any) (n n-0) (d d) (o o) (k k-0) (lk lk-0) (ls ls))`, `(precedes ((0 0) (2 0)) ((2 2) (1 0)) ((2 5) (0 1)) ((3 0) (1 1)) ((4 3) (1 2)))`, `(uniq-orig n k)`
  - **Keywords & Predicates Used**: `and`, `auth`, `bound`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `forall`, `gen-st`, `herald`, `implies`, `load`, `p`, `precedes`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when using string literal tags (`"opened"`, `"closed"`) inside `locn` state macros (`load`/`stor`) and inspecting multi-strand state transition skeletons.
- **Key S-Expression Excerpt** (lines 7–45):
```scheme
(defmacro (dev-key-state d o k)
  (cat "st-k" d o k))

(defmacro (opened o)
  "opened")

(defmacro (closed o) "closed")

(defmacro (dev-state-opened d o)
  (cat "st" d (opened o)))

(defmacro (dev-state-closed d o)
  (cat "st" d (closed o)))

(defmacro (dev-state-any d o any)
  (cat "st" d any))

(defprotocol open-closed basic
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

  (defrole owner-power-dev
    (vars (k skey) (d o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" d o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d o name))
    (trace
```

## open-closed.scm

- **File Path**: `03_examples_scm/open-closed.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald open-closed (bound 44))` | Flags: `(bound 44)` (commented-out flags in source: `(try-old-strands)`, `(check-nonces)`, `(reverse-nodes)`)
- **Protocol & Purpose**: Protocol(s): `open-closed`. Full version of the stateful `open-closed` device protocol that extends `open-closed-multiloc.scm` with two additional rules demonstrating built-in location/state predicates: `(same-locn z1 i1 z2 i2)` (recording `(fact ha z1 i1 z2 i2)`) and `(leads-to z1 i1 z2 i2)` (recording `(fact la z1 i1 z2 i2)`), along with rule-level `(comment ...)` clauses.
- **Roles & Variables**:
  - Role `dev-up`: Vars: `(k skey)`, `(d o name)`, `(old old1 mesg)`, `(start-ch chan)`, `(lk ls locn)` | Role Assumptions: `(auth start-ch)` | Trace (6 events): `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(stor lk (dev-key-state d o k))` -> `(load ls old1)` -> `(stor ls (dev-state-closed d o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev`: Vars: `(k skey)`, `(d o name)`, `(start-ch chan)` | Role Assumptions: `(conf start-ch)` | Trace (2 events): `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "open" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-opened d o))` -> `(send n)`
  - Role `dev-close`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "close" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-closed d o))` -> `(send n)`
  - Role `dev-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: `(uniq-orig n)` | Trace (4 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "may I pass" k))` -> `(load ls (dev-state-opened d o))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(l locn)` | Role Assumptions: none | Trace (2 events): `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (6)**: `(dev-key-state d o k)`, `(opened o)`, `(closed o)`, `(dev-state-opened d o)`, `(dev-state-closed d o)`, `(dev-state-any d o any)`
  - **Rules (5)**: `gen-state-close`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-close" z 1) (p "dev-close" "d" z d) (p "dev-close" "o" z o) (p "dev-close" "k" z k) (p "dev-close" "any" z (opened o))) (gen-st (dev-state-opened d o))))`; `gen-state-pass`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "d" z d) (p "dev-pass" "o" z o) (p "dev-pass" "k" z k)) (gen-st (dev-state-opened d o))))`; `power-deliver-once`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z2 z1)))`; `same-locn`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (same-locn z1 i1 z2 i2) (fact ha z1 i1 z2 i2)))`; `leadsto-la`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (leads-to z1 i1 z2 i2) (fact la z1 i1 z2 i2)))`
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(deflistener k)`, `(uniq-orig k)` | Skeleton 2 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand dev-pass 4 (k k))` | Skeleton 3 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(defstrand dev-pass 4 (k k))`, `(uniq-orig k)`
  - **Keywords & Predicates Used**: `and`, `auth`, `bound`, `comment`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `forall`, `gen-st`, `herald`, `implies`, `leads-to`, `load`, `p`, `recv`, `same-locn`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example to learn the exact syntax of the built-in stateful predicates `(same-locn z1 i1 z2 i2)` and `(leads-to z1 i1 z2 i2)` over strand (`strd`) and node index (`indx`) variables in `(defrule ...)`.
- **Key S-Expression Excerpt** (lines 100–131):
```scheme
	    (implies
	     (and (p "dev-pass" z 1)
		  (p "dev-pass" "d" z d)
		  (p "dev-pass" "o" z o)
		  (p "dev-pass" "k" z k))
	     (gen-st (dev-state-opened d o)))))

   (defrule power-deliver-once
     (forall
      ((z1 z2 strd) (k skey))
      (implies
       (and (p "dev-up" z1 2)
 	   (p "dev-up" z2 2)
 	   (p "dev-up" "k" z1 k)
 	   (p "dev-up" "k" z2 k))
       (= z2 z1))))

   (defrule same-locn
     (forall ((z1 z2 strd) (i1 i2 indx))
  	     (implies
  	      (same-locn z1 i1 z2 i2)
  	      (fact ha z1 i1 z2 i2)))
     (comment this is a rule comment))

   (defrule leadsto-la
     (forall ((z1 z2 strd) (i1 i2 indx))
  	     (implies
  	      (leads-to z1 i1 z2 i2)
  	      (fact la z1 i1 z2 i2)))
     (comment this is a rule comment))
   )

```

## or.scm

- **File Path**: `03_examples_scm/or.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Otway-Rees Protocol" (comment "Standard version using variables of sort mesg"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `or`. Standard version of the Otway-Rees symmetric key distribution protocol (`or`) with roles `init`, `resp`, and `serv`, demonstrating the use of sort `mesg` variables (`x` and `y`) in `resp` to forward opaque encrypted tickets (`x` from `init` to `serv`, and `y` from `serv` to `init`) that `resp` cannot decrypt.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b s name)`, `(na text)`, `(k skey)`, `(m text)` | Role Assumptions: none | Trace (2 events): `(send (cat m a b (enc na m a b (ltk a s))))` -> `(recv (cat m (enc na k (ltk a s))))`
  - Role `resp`: Vars: `(a b s name)`, `(nb text)`, `(k skey)`, `(m text)`, `(x y mesg)` | Role Assumptions: none | Trace (4 events): `(recv (cat m a b x))` -> `(send (cat m a b x (enc nb m a b (ltk b s))))` -> `(recv (cat m y (enc nb k (ltk b s))))` -> `(send y)`
  - Role `serv`: Vars: `(a b s name)`, `(na nb text)`, `(k skey)`, `(m text)` | Role Assumptions: `(uniq-orig k)` | Trace (2 events): `(recv (cat m a b (enc na m a b (ltk a s)) (enc nb m a b (ltk b s))))` -> `(send (cat m (enc na k (ltk a s)) (enc nb k (ltk b s))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`or`): `(vars (nb text) (s a b name))`, `(defstrand resp 4 (a a) (b b) (s s) (nb nb))`, `(non-orig (ltk a s) (ltk b s))`, `(uniq-orig nb)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example whenever an intermediate or responder role must receive and forward an opaque ciphertext or token it cannot decrypt, using variables of sort `mesg` (`(vars ... (x y mesg))`).
- **Key S-Expression Excerpt** (lines 1–27):
```scheme
(herald "Otway-Rees Protocol"
	(comment "Standard version using variables of sort mesg"))

(defprotocol or basic
  (defrole init (vars (a b s name) (na text) (k skey) (m text))
    (trace
     (send (cat m a b (enc na m a b (ltk a s))))
     (recv (cat m (enc na k (ltk a s))))))
  (defrole resp
    (vars (a b s name) (nb text) (k skey) (m text) (x y mesg))
    (trace
     (recv (cat m a b x))
     (send (cat m a b x (enc nb m a b (ltk b s))))
     (recv (cat m y (enc nb k (ltk b s))))
     (send y)))
  (defrole serv (vars (a b s name) (na nb text) (k skey) (m text))
    (trace
     (recv (cat m a b (enc na m a b (ltk a s))
		(enc nb m a b (ltk b s))))
     (send (cat m (enc na k (ltk a s)) (enc nb k (ltk b s)))))
    (uniq-orig k)))

(defskeleton or
  (vars (nb text) (s a b name))
  (defstrand resp 4 (a a) (b b) (s s) (nb nb))
  (non-orig (ltk a s) (ltk b s))
  (uniq-orig nb))
```

## ordered.scm

- **File Path**: `03_examples_scm/ordered.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald ordered)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ordered`. Demonstrates a linear ordering rule (`order`) over decryption strands (`dec`) using the low-level role predicate syntax `(p "dec" y 2)` and `(p "dec" z 2)`, concluding `(or (prec y 1 z 0) (prec z 1 y 0) (= y z))`. Also illustrates how CPSA records rule-application output annotations (`(rule order)`, `(traces ...)`, `(label 3)`, `(parent 0)`, `(unrealized)`, `(shape)`, `(maps ...)`, `(origs)`) in an output skeleton.
- **Roles & Variables**:
  - Role `dec`: Vars: `(t text)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc t k))` -> `(send t)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `order`: `(forall ((y z strd)) (implies (and (p "dec" y 2) (p "dec" z 2)) (or (prec y 1 z 0) (prec z 1 y 0) (= y z))))`
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`ordered`): `(vars (a b text))`, `(defstrand dec 2 (t a))`, `(defstrand dec 2 (t b))`, `(facts (neq a b))` | Skeleton 2 (`ordered`): `(vars (b text) (k akey))`, `(defstrand dec 2 (t b) (k k))`, `(facts (neq b b))`, `(rule order)`, `(traces ((recv (enc b k)) (send b)))`, `(label 3)`, `(parent 0)`, `(unrealized)`, `(shape)`, `(maps ((0 0) ((a b) (b b) (k k) (k-0 k))))`, `(origs)`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `facts`, `forall`, `herald`, `implies`, `label`, `maps`, `neq`, `or`, `origs`, `p`, `parent`, `prec`, `recv`, `rule`, `send`, `shape`, `trace`, `traces`, `unrealized`, `vars`
- **When to Reference This Example**: Reference this example when writing a rule (`defrule`) that forces all instances of a role to execute sequentially (linear ordering via `(or (prec y 1 z 0) (prec z 1 y 0) (= y z))`) using the `(p "<role>" <strd> <height>)` predicate syntax.
- **Key S-Expression Excerpt** (lines 1–39):
```scheme
(herald ordered)

(defprotocol ordered basic

  (defrole dec
    (vars (t text) (k akey))
    (trace (recv (enc t k)) (send t)))

;;     (defrule neq
;;       (forall ((x mesg))
;;   	    (implies (fact neq x x) (false))))

  (defrule order
    (forall ((y z strd))
	    (implies
	     (and (p "dec" y 2)
		  (p "dec" z 2))
	     (or (prec y 1 z 0)
		 (prec z 1 y 0)
		 (= y z))))))

(defskeleton ordered
  (vars (a b text))
  (defstrand dec 2 (t a))
  (defstrand dec 2 (t b))
  (facts (neq a b)))

(defskeleton ordered
  (vars (b text) (k akey))
  (defstrand dec 2 (t b) (k k))
  (facts (neq b b))
  (rule order)
  (traces ((recv (enc b k)) (send b)))
  (label 3)
  (parent 0)
  (unrealized)
  (shape)
  (maps ((0 0) ((a b) (b b) (k k) (k-0 k))))
  (origs))
```

## orderedvar.scm

- **File Path**: `03_examples_scm/orderedvar.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald ordered)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ordered`. Identical to `ordered.scm` except that the `order` rule is written using CPSA's role-variable predicate syntax `(strand dec y 2)` and `(strand dec z 2)` instead of string-quoted `(p "dec" y 2)`.
- **Roles & Variables**:
  - Role `dec`: Vars: `(t text)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc t k))` -> `(send t)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `order`: `(forall ((y z strd)) (implies (and (strand dec y 2) (strand dec z 2)) (or (prec y 1 z 0) (prec z 1 y 0) (= y z))))`
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`ordered`): `(vars (a b text))`, `(defstrand dec 2 (t a))`, `(defstrand dec 2 (t b))`, `(facts (neq a b))` | Skeleton 2 (`ordered`): `(vars (b text) (k akey))`, `(defstrand dec 2 (t b) (k k))`, `(facts (neq b b))`, `(rule order)`, `(traces ((recv (enc b k)) (send b)))`, `(label 3)`, `(parent 0)`, `(unrealized)`, `(shape)`, `(maps ((0 0) ((a b) (b b) (k k) (k-0 k))))`, `(origs)`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `facts`, `forall`, `herald`, `implies`, `label`, `maps`, `neq`, `or`, `origs`, `parent`, `prec`, `recv`, `rule`, `send`, `shape`, `strand`, `trace`, `traces`, `unrealized`, `vars`
- **When to Reference This Example**: Reference this example to compare the cleaner `(strand <role> <strd> <height>)` syntax against `(p "<role>" <strd> <height>)` inside `(defrule ...)`.
- **Key S-Expression Excerpt** (lines 1–39):
```scheme
(herald ordered)

(defprotocol ordered basic

  (defrole dec
    (vars (t text) (k akey))
    (trace (recv (enc t k)) (send t)))

;;     (defrule neq
;;       (forall ((x mesg))
;;   	    (implies (fact neq x x) (false))))

  (defrule order
    (forall ((y z strd))
	    (implies
	     (and (strand dec y 2)
		  (strand dec z 2))
	     (or (prec y 1 z 0)
		 (prec z 1 y 0)
		 (= y z))))))

(defskeleton ordered
  (vars (a b text))
  (defstrand dec 2 (t a))
  (defstrand dec 2 (t b))
  (facts (neq a b)))

(defskeleton ordered
  (vars (b text) (k akey))
  (defstrand dec 2 (t b) (k k))
  (facts (neq b b))
  (rule order)
  (traces ((recv (enc b k)) (send b)))
  (label 3)
  (parent 0)
  (unrealized)
  (shape)
  (maps ((0 0) ((a b) (b b) (k k) (k-0 k))))
  (origs))
```

## pca.scm

- **File Path**: `03_examples_scm/pca.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Privacy Certificate Authority" (bound 15) (comment "Generation of an Attestation Identity Certificate"))` | Flags: `(bound 15)`
- **Protocol & Purpose**: Protocol(s): `pca`. Models a simplified Privacy Certificate Authority (`pca`) protocol for generating a TPM Attestation Identity Certificate (AIC), with roles `tpm`, `pca`, and `appr` (appraiser) and herald flag `(bound 15)`. The TPM sends a self-signed identity key `(enc ki a (invk ki))` and manufacturer-certified endorsement key `(enc t ke (invk km))` to the PCA, receives the signed AIC `(enc ki a t (invk kp))` encrypted under `ke`, and forwards the AIC to the appraiser.
- **Roles & Variables**:
  - Role `tpm`: Vars: `(ke ki km kp akey)`, `(t a text)` | Role Assumptions: `(non-orig (invk ke) (invk ki) (invk km) (invk kp))`, `(uniq-orig ki)` | Trace (3 events): `(send (cat (enc ki a (invk ki)) (enc t ke (invk km))))` -> `(recv (enc (enc ki a t (invk kp)) ke))` -> `(send (enc ki a t (invk kp)))`
  - Role `pca`: Vars: `(ke ki km kp akey)`, `(t a text)` | Role Assumptions: `(non-orig (invk ke) (invk ki) (invk km) (invk kp))` | Trace (2 events): `(recv (cat (enc ki a (invk ki)) (enc t ke (invk km))))` -> `(send (enc (enc ki a t (invk kp)) ke))`
  - Role `appr`: Vars: `(ki kp akey)`, `(t a text)` | Role Assumptions: `(non-orig (invk ki) (invk kp))` | Trace (1 events): `(recv (enc ki a t (invk kp)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`pca`): `(vars (ki kp akey))`, `(defstrand appr 1 (ki ki) (kp kp))`, `(non-orig (invk ki) (invk kp))`
  - **Keywords & Predicates Used**: `bound`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling PKI certificate issuance or TPM Attestation Identity Certificate (AIC) enrollment where a CA wraps a newly signed certificate `(enc ki a t (invk kp))` inside an encryption key `ke`.
- **Key S-Expression Excerpt** (lines 1–36):
```scheme
(herald "Privacy Certificate Authority" (bound 15)
  (comment "Generation of an Attestation Identity Certificate"))

;;; PCA generation of AIC, simplified

;;; ki = identity key
;;; a = identity label
;;; t = TPM type/platform
;;; ke = endorsement key
;;; kp = PCA key
;;; km = manufacturer key
;;; (enc (cat ki a t) (invk kp)) is the signed AIC

(defprotocol pca basic
  (defrole tpm (vars (ke ki km kp akey) (t a text))
    (trace
     (send (cat (enc ki a (invk ki)) (enc t ke (invk km))))
     (recv (enc (enc ki a t (invk kp)) ke))
     (send (enc ki a t (invk kp))))
    (non-orig (invk ke) (invk ki) (invk km) (invk kp))
    (uniq-orig ki))
  (defrole pca (vars (ke ki km kp akey) (t a text))
    (trace
     (recv (cat (enc ki a (invk ki)) (enc t ke (invk km))))
     (send (enc (enc ki a t (invk kp)) ke)))
    (non-orig (invk ke) (invk ki) (invk km) (invk kp)))
  (defrole appr (vars (ki kp akey) (t a text))
    (trace
     (recv (enc ki a t (invk kp))))
    (non-orig (invk ki) (invk kp))))

;;; normal run

(defskeleton pca (vars (ki kp akey))
  (defstrand appr 1 (ki ki) (kp kp))
  (non-orig (invk ki) (invk kp)))
```

## pen-non-orig-test.scm

- **File Path**: `03_examples_scm/pen-non-orig-test.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "pen-non-orig test")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `pennonorigtest`. Minimal test case (`pennonorigtest`) illustrating the exact semantics of `(pen-non-orig pwd)`. Because `pwd` is declared `(pen-non-orig pwd)` in `server`, the penetrator does not know `pwd` initially (so `server` receiving `(cat userid pwd)` in cleartext must still be explained by a legitimate `client` strand), even though the penetrator learns `pwd` once `client` transmits it in the clear (so the second skeleton with `(deflistener pwd)` is also realized).
- **Roles & Variables**:
  - Role `client`: Vars: `(userid name)`, `(pwd text)` | Role Assumptions: none | Trace (1 events): `(send (cat userid pwd))`
  - Role `server`: Vars: `(userid name)`, `(pwd text)` | Role Assumptions: `(pen-non-orig pwd)` | Trace (1 events): `(recv (cat userid pwd))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`pennonorigtest`): `(vars (pwd text))`, `(defstrand server 1 (pwd pwd))` | Skeleton 2 (`pennonorigtest`): `(vars (pwd text))`, `(defstrand server 1 (pwd pwd))`, `(deflistener pwd)`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `pen-non-orig`, `recv`, `send`, `trace`, `vars`
- **When to Reference This Example**: Reference this example to understand the difference between `(non-orig x)` (never sent in the clear or learned by the penetrator) and `(pen-non-orig x)` (not initially known to or originated by the penetrator, even if later exposed on the network, such as passwords or pre-shared session keys).
- **Key S-Expression Excerpt** (lines 1–29):
```scheme
;; This is to test the pen-non-orig declaration.
;; The password, pwd, should not be known to the
;; penetrator at the outset.  Thus, even over an
;; unencrypted channel, the server should infer
;; a good client.  However, the password is
;; learned in the process, hence the skeleton
;; with a listener will also be realized.

(herald "pen-non-orig test")

(defprotocol pennonorigtest basic
  (defrole client
    (vars (userid name) (pwd text))
    (trace
     (send (cat userid pwd))))
  (defrole server
    (vars (userid name) (pwd text))
    (trace
     (recv (cat userid pwd)))
    (pen-non-orig pwd)))

(defskeleton pennonorigtest
  (vars (pwd text))
  (defstrand server 1 (pwd pwd)))

(defskeleton pennonorigtest
  (vars (pwd text))
  (defstrand server 1 (pwd pwd))
  (deflistener pwd))
```

## pfs-via-pubkey.scm

- **File Path**: `03_examples_scm/pfs-via-pubkey.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald pfs-via-pubkey)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `pfs-easy`. Demonstrates how to model Perfect Forward Secrecy (PFS) in CPSA (`pfs-easy`) by having `init` generate an ephemeral asymmetric key `new-akey`, sign it with long-term signing key `(privk "sgn" a)`, receive a secret `s` encrypted under `new-akey`, and then explicitly transmit the long-term private key `(send (privk "sgn" a))` at the end of the trace to model subsequent key compromise (requiring `(uniq-orig (privk "sgn" a))` instead of `(non-orig (privk "sgn" a))`).
- **Roles & Variables**:
  - Role `init`: Vars: `(new-akey akey)`, `(a b name)`, `(n data)`, `(s text)` | Role Assumptions: none | Trace (3 events): `(send (enc a b new-akey n (privk "sgn" a)))` -> `(recv (enc (enc a n s (privk "sgn" b)) new-akey))` -> `(send (privk "sgn" a))`
  - Role `resp`: Vars: `(new-akey akey)`, `(a b name)`, `(n data)`, `(s text)` | Role Assumptions: none | Trace (2 events): `(recv (enc a b new-akey n (privk "sgn" a)))` -> `(send (enc (enc a n s (privk "sgn" b)) new-akey))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`pfs-easy`): `(vars (new-akey akey) (a b name) (n data) (s text))`, `(defstrand init 3 (a a) (b b) (new-akey new-akey) (n n))`, `(non-orig (privk "sgn" b) (invk new-akey))`, `(uniq-orig (privk "sgn" a) new-akey n)` | Skeleton 2 (`pfs-easy`): `(vars (new-akey akey) (a b name) (n data) (s text))`, `(defstrand resp 2 (a a) (new-akey new-akey))`, `(non-orig (privk "sgn" a))` | Skeleton 3 (`pfs-easy`): `(vars (s text) (n data) (a b name) (new-akey akey))`, `(defstrand resp 2 (s s) (n n) (a a) (b b) (new-akey new-akey))`, `(defstrand init 3 (n n) (a a) (b b) (new-akey new-akey))`, `(deflistener s)`, `(precedes ((1 0) (0 0)))`, `(non-orig (invk new-akey))`, `(uniq-orig (privk "sgn" a) s)`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example whenever you need to model Perfect Forward Secrecy (PFS) or post-compromise security by transmitting a long-term key `(send (privk ...))` at the end of a role and declaring it `uniq-orig` rather than `non-orig`.
- **Key S-Expression Excerpt** (lines 1–35):
```scheme
(herald pfs-via-pubkey)

(defprotocol pfs-easy basic
  (defrole init
    (vars (new-akey akey) (a b name) (n data) (s text))
    (trace
     (send (enc a b new-akey n (privk "sgn" a)))
     (recv (enc (enc a n s (privk "sgn" b)) new-akey))
     (send (privk "sgn" a))))		; compromise signing key subsequently

  (defrole resp
    (vars (new-akey akey) (a b name) (n data) (s text))
    (trace
     (recv (enc a b new-akey n (privk "sgn" a)))
     (send (enc (enc a n s (privk "sgn" b)) new-akey)))))

(defskeleton pfs-easy
  (vars (new-akey akey) (a b name) (n data) (s text))
  (defstrand init 3 (a a) (b b) (new-akey new-akey) (n n))
  (non-orig (privk "sgn" b) (invk new-akey))
  (uniq-orig (privk "sgn" a) new-akey n))

(defskeleton pfs-easy
  (vars (new-akey akey) (a b name) (n data) (s text))
  (defstrand resp 2 (a a) (new-akey new-akey))
  (non-orig (privk "sgn" a)))

(defskeleton pfs-easy
  (vars (s text) (n data) (a b name) (new-akey akey))
  (defstrand resp 2 (s s) (n n) (a a) (b b) (new-akey new-akey))
  (defstrand init 3 (n n) (a a) (b b) (new-akey new-akey))
  (deflistener s)
  (precedes ((1 0) (0 0)))
  (non-orig (invk new-akey))
  (uniq-orig (privk "sgn" a) s))
```

## pkinit.scm

- **File Path**: `03_examples_scm/pkinit.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Kerberos PK init")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `pkinit`. Models the Kerberos PKINIT (Public Key Cryptography for Initial Authentication in Kerberos, RFC 4556) exchange (`pkinit`) between `client` (`c`) and authentication server `auth` (`as`), combining public-key signatures/encryption (`(privk c)`, `(privk as)`, `(pubk c)`) with symmetric session keys (`k`, `ak` of sort `skey`).
- **Roles & Variables**:
  - Role `client`: Vars: `(c t as name)`, `(n2 n1 text)`, `(tc tk tgt data)`, `(k ak skey)` | Role Assumptions: `(uniq-orig n1 n2)` | Trace (2 events): `(send (cat (enc tc n2 (privk c)) c t n1))` -> `(recv (cat (enc (enc k n2 (privk as)) (pubk c)) c tgt (enc ak n1 tk t k)))`
  - Role `auth`: Vars: `(c t as name)`, `(n2 n1 text)`, `(tc tk tgt data)`, `(k ak skey)` | Role Assumptions: `(uniq-orig k ak)` | Trace (2 events): `(recv (cat (enc tc n2 (privk c)) c t n1))` -> `(send (cat (enc (enc k n2 (privk as)) (pubk c)) c tgt (enc ak n1 tk t k)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`pkinit`): `(vars (c as name))`, `(defstrand client 2 (c c) (as as))`, `(non-orig (privk c) (privk as))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling RFC 4556 (Kerberos PKINIT) or protocols that bootstrap symmetric Kerberos tickets (`tgt`) and session keys (`k`, `ak`) from an initial public-key signed request.
- **Key S-Expression Excerpt** (lines 1–22):
```scheme
(herald "Kerberos PK init")

(defprotocol pkinit basic
  (defrole client
    (vars (c t as name) (n2 n1 text) (tc tk tgt data) (k ak skey))
    (trace (send (cat (enc tc n2 (privk c)) c t n1))
      (recv
        (cat (enc (enc k n2 (privk as)) (pubk c)) c tgt
          (enc ak n1 tk t k))))
    (uniq-orig n1 n2))
  (defrole auth
    (vars (c t as name) (n2 n1 text) (tc tk tgt data) (k ak skey))
    (trace (recv (cat (enc tc n2 (privk c)) c t n1))
      (send
        (cat (enc (enc k n2 (privk as)) (pubk c)) c tgt
          (enc ak n1 tk t k))))
    (uniq-orig k ak)))

(defskeleton pkinit
  (vars (c as name))
  (defstrand client 2 (c c) (as as))
  (non-orig (privk c) (privk as)))
```

## preprocess.scm

- **File Path**: `03_examples_scm/preprocess.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Pre-processing test example: modified NS with two responders")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. Tests CPSA's preskeleton preprocessing on a modified Needham-Schroeder protocol (`ns`) where the responder originates two nonces (`n2`, `n3`) and the initial skeleton entangles one initiator strand (`(n2 n2) (n3 n3)`) with two responder strands (`(n2 n2) (n3 n3p)` and `(n2 n2p) (n3 n3)`).
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 n3 text)` | Role Assumptions: `(uniq-orig n1)` | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc n1 n2 n3 (pubk a)))` -> `(send (enc n2 n3 (pubk b)))`
  - Role `resp`: Vars: `(a b name)`, `(n1 n2 n3 text)` | Role Assumptions: `(uniq-orig n2 n3)` | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 n3 (pubk a)))` -> `(recv (enc n2 n3 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`ns`): `(vars (a b name) (n1 n2 n3 n2p n3p text))`, `(defstrand init 3 (a a) (b b) (n1 n1) (n2 n2) (n3 n3))`, `(defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2) (n3 n3p))`, `(defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2p) (n3 n3))`, `(non-orig (privk b) (privk a))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when constructing multi-strand preskeletons that test whether entangled responder sessions must collapse into a single session due to `uniq-orig` constraints.
- **Key S-Expression Excerpt** (lines 1–27):
```scheme
(herald "Pre-processing test example: modified NS with two responders")

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 n3 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 n3 (pubk a)))
     (send (enc n2 n3 (pubk b))))
	(uniq-orig n1))
  (defrole resp
    (vars (a b name) (n1 n2 n3 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 n3 (pubk a)))
     (recv (enc n2 n3 (pubk b))))
	(uniq-orig n2 n3))
  (comment "modified Needham-Schroeder with role origination assumptions"))

;;; The initiator and two entangled responders POV
(defskeleton ns
  (vars (a b name) (n1 n2 n3 n2p n3p text))
  (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2) (n3 n3))
  (defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2) (n3 n3p))
  (defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2p) (n3 n3))
  (non-orig (privk b) (privk a))
)
```

## print.scm

- **File Path**: `03_examples_scm/print.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Print Test" (comment "See if read forms look like printed ones"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `print-test`. Minimal test (`print-test`) verifying the canonical order in which CPSA prints variables of different sorts (`akey`, `skey`, `data`) in `vars` declarations and strand mappings.
- **Roles & Variables**:
  - Role `role`: Vars: `(a b akey)`, `(f g skey)`, `(x y data)` | Role Assumptions: none | Trace (1 events): `(recv (cat a b f g x y))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`print-test`): `(vars (a b akey) (f g skey) (x y data))`, `(defstrand role 1 (a a) (b b) (f f) (g g) (x x) (y y))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `recv`, `trace`, `vars`
- **When to Reference This Example**: Reference this example as a minimal 13-line syntax check for grouping multiple variables per sort `(vars (a b akey) (f g skey) (x y data))` in `defrole` and `defskeleton`.
- **Key S-Expression Excerpt** (lines 1–13):
```scheme
(herald "Print Test"
  (comment "See if read forms look like printed ones"))

(defprotocol print-test basic
  (defrole role
    (vars (a b akey) (f g skey) (x y data))
    (trace (recv (cat a b f g x y)))
    (comment "Check the order in which variables are printed")))

(defskeleton print-test
  (vars (a b akey) (f g skey) (x y data))
  (defstrand role 1 (a a) (b b) (f f) (g g) (x x) (y y))
  (comment "Check the order in which variables are printed"))
```

## prottrans.scm

- **File Path**: `03_examples_scm/prottrans.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Protocol Transformations With Rules")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`, `unilateral`, `ns-with-rule`. Demonstrates protocol transformations with rules (`Protocol Transformations With Rules`). Defines three protocols: standard `ns` (with `akey` principals), a 2-message `unilateral` challenge-response protocol (with its Shape Analysis Sentence shown as a commented `defgoal`), and `ns-with-rule`, which embeds the image of the `unilateral` shape analysis sentence as a `(defrule unilateral ...)` inside Needham-Schroeder.
- **Roles & Variables**:
  - Role `init` (in `ns`): Vars: `(a b akey)`, `(na nb text)` | Role Assumptions: none | Trace (3 events): `(send (enc na a b))` -> `(recv (enc na nb a))` -> `(send (enc nb b))`
  - Role `resp` (in `ns`): Vars: `(b a akey)`, `(nb na text)` | Role Assumptions: none | Trace (3 events): `(recv (enc na a b))` -> `(send (enc na nb a))` -> `(recv (enc nb b))`
  - Role `init` (in `unilateral`): Vars: `(n text)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(send (enc n k))` -> `(recv n)`
  - Role `resp` (in `unilateral`): Vars: `(n text)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc n k))` -> `(send n)`
  - Role `init` (in `ns-with-rule`): Vars: `(a b akey)`, `(na nb text)` | Role Assumptions: none | Trace (3 events): `(send (enc na a b))` -> `(recv (enc na nb a))` -> `(send (enc nb b))`
  - Role `resp` (in `ns-with-rule`): Vars: `(b a akey)`, `(nb na text)` | Role Assumptions: none | Trace (3 events): `(recv (enc na a b))` -> `(send (enc na nb a))` -> `(recv (enc nb b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `unilateral`: `(forall ((r strd) (a akey) (nb text)) (implies (and (p "resp" r 3) (p "resp" "a" r a) (p "resp" "nb" r nb) (non (invk a)) (uniq nb)) (exists ((i strd)) (and (p "init" i 3) (p "init" "a" i a) (p "init" "nb" i nb) (prec r 1 i 1) (prec i 2 r 2)))))`
  - **Goals**: None active (contains a commented-out `(defgoal unilateral ...)` inside `(comment ...)` showing the Shape Analysis Sentence before rule translation)
  - **Skeletons (4)**: Skeleton 1 (`ns`): `(vars (a b akey) (na text))`, `(defstrand init 3 (a a) (b b) (na na))`, `(non-orig (invk a) (invk b))`, `(uniq-orig na)` | Skeleton 2 (`ns`): `(vars (a akey) (nb text))`, `(defstrand resp 3 (a a) (nb nb))`, `(non-orig (invk a))`, `(uniq-orig nb)` | Skeleton 3 (`unilateral`): `(vars (k akey) (n text))`, `(defstrand init 2 (n n) (k k))`, `(non-orig (invk k))`, `(uniq-orig n)` | Skeleton 4 (`ns-with-rule`): `(vars (a akey) (nb text))`, `(defstrand resp 3 (a a) (nb nb))`, `(non-orig (invk a))`, `(uniq-orig nb)`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `exists`, `forall`, `herald`, `implies`, `non`, `non-orig`, `p`, `prec`, `recv`, `send`, `trace`, `uniq`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when translating a proved shape analysis sentence (`defgoal`) from a sub-protocol (`unilateral`) into a lemma/rule (`defrule`) inside a larger protocol (`ns-with-rule`).
- **Key S-Expression Excerpt** (lines 65–107):
```scheme
(defprotocol ns-with-rule basic
  (defrole init
    (vars (a b akey) (na nb text))
    (trace
     (send (enc na a b))
     (recv (enc na nb a))
     (send (enc nb b))))
  (defrole resp
    (vars (b a akey) (nb na text))
    (trace
     (recv (enc na a b))
     (send (enc na nb a))
     (recv (enc nb b))))
  (defrule unilateral
    (forall ((r strd) (a akey) (nb text))
	    (implies
	     (and (p "resp" r 3)
		  (p "resp" "a" r a)
		  (p "resp" "nb" r nb)
		  (non (invk a))
		  (uniq nb))
	     (exists ((i strd))
		     (and (p "init" i 3)
			  (p "init" "a" i a)
			  (p "init" "nb" i nb)
			  (prec r 1 i 1)
			  (prec i 2 r 2)))))
    (comment "Unilateral sas under the predicate mapping:")
    (comment (p "init" 2) "->" (p "resp" 3) "and")
    (comment (p "init" "n") "->" (p "resp" "nb") "and")
    (comment (p "init" "k") "->" (p "resp" "a") "and")
    (comment (p "resp" 2) "->" (p "init" 3) "and")
    (comment (p "resp" "n") "->" (p "init" "nb"))
    (comment (p "resp" "k") "->" (p "init" "a")))
  (comment "Needham-Schroeder with rule"))

;;; The responder point-of-view
(defskeleton ns-with-rule
  (vars (a akey) (nb text))
  (defstrand resp 3 (a a) (nb nb))
  (non-orig (invk a))
  (uniq-orig nb)
  (comment "Responder point-of-view"))
```

## pruning1.scm

- **File Path**: `03_examples_scm/pruning1.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `prune`. Regression test (`prune`) demonstrating a subtle case of strand pruning where `init` sends `(enc n (pubk a))` and expects both `(enc n (pubk b) (pubk a))` and `(enc n (privk b) (pubk a))`, requiring two separate instances of the transformer role `trans` (one with `k = (pubk b)` and one with `k = (privk b)`).
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n text)` | Role Assumptions: `(uniq-orig n)`, `(non-orig (privk a))` | Trace (3 events): `(send (enc n (pubk a)))` -> `(recv (enc n (pubk b) (pubk a)))` -> `(recv (enc n (privk b) (pubk a)))`
  - Role `trans`: Vars: `(a name)`, `(n text)`, `(k akey)` | Role Assumptions: none | Trace (3 events): `(recv (enc n (pubk a)))` -> `(recv k)` -> `(send (enc n k (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`prune`): `(vars (a name) (n text) (k akey))`, `(defstrand init 3)` | Skeleton 2 (`prune`): `(vars (n text) (a b name))`, `(defstrand init 3 (n n) (a a) (b b))`, `(defstrand trans 3 (n n) (a a) (k (pubk b)))`, `(defstrand trans 3 (n n) (a a) (k (privk b)))`, `(precedes ((0 0) (1 0)) ((0 0) (2 0)) ((1 2) (0 1)) ((2 2) (0 2)))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when a protocol role (`trans`) takes a generic key variable `(k akey)` that must be instantiated with both `(pubk b)` and `(privk b)` across distinct strands in the same shape.
- **Key S-Expression Excerpt** (lines 12–42):
```scheme
(defprotocol prune basic
  (defrole init (vars (a b name) (n text))
    (trace
	(send (enc n (pubk a)))
      (recv (enc n (pubk b) (pubk a)))
      (recv (enc n (privk b) (pubk a)))
	)
    (uniq-orig n)
    (non-orig (privk a))
  )
  (defrole trans (vars (a name) (n text) (k akey))
     (trace
        (recv (enc n (pubk a)))
	(recv k )
        (send (enc n k (pubk a)))
     )
  )
  (comment "Shows a failure with generalization"
	   "Run this with a step count of 4"))

(defskeleton prune
  (vars (a name) (n text) (k akey))
  (defstrand init 3))

(defskeleton prune
  (vars (n text) (a b name))
  (defstrand init 3 (n n) (a a) (b b))
  (defstrand trans 3 (n n) (a a) (k (pubk b)))
  (defstrand trans 3 (n n) (a a) (k (privk b)))
  (precedes ((0 0) (1 0)) ((0 0) (2 0)) ((1 2) (0 1)) ((2 2) (0 2)))
)
```

## puzzle_example.scm

- **File Path**: `03_examples_scm/puzzle_example.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald puzzle_example)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `puzzle`. Models a symmetric-key challenge-response and payload encryption protocol (`puzzle`) using `(ltk a b)` and fresh session key `(s skey)`, followed by 7 different `(defskeleton ...)` queries exploring initiator POV, responder POV, and confidentiality of `s` and `payload` with `(deflistener ...)` and explicit `(precedes ...)` constraints.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(na payload text)`, `(s skey)` | Role Assumptions: none | Trace (3 events): `(send na)` -> `(recv (enc na s (ltk a b)))` -> `(send (enc payload s))`
  - Role `resp`: Vars: `(a b name)`, `(na payload text)`, `(s skey)` | Role Assumptions: none | Trace (3 events): `(recv na)` -> `(send (enc na s (ltk a b)))` -> `(recv (enc payload s))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (7)**: Skeleton 1 (`puzzle`): `(vars (a b name) (na payload text) (s skey))`, `(defstrand init 3 (a a) (b b) (na na) (payload payload))`, `(uniq-orig na payload)`, `(non-orig (ltk a b))` | Skeleton 2 (`puzzle`): `(vars (a b name) (na payload text) (s skey))`, `(defstrand init 3 (a a) (b b) (na na) (payload payload))`, `(deflistener payload)`, `(uniq-orig na payload)`, `(non-orig (ltk a b))` | Skeleton 3 (`puzzle`): `(vars (na payload text) (a b name) (s skey))`, `(defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))`, `(defstrand resp 2 (na na) (a a) (b b) (s s))`, `(deflistener s)`, `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`, `(non-orig (ltk a b))`, `(uniq-orig s na payload)` | Skeleton 4 (`puzzle`): `(vars (na payload text) (a b name) (s skey))`, `(defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))`, `(defstrand resp 2 (na na) (a a) (b b) (s s))`, `(deflistener payload)`, `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`, `(non-orig (ltk a b))`, `(uniq-orig s na payload)` | Skeleton 5 (`puzzle`): `(vars (a b name) (na payload text) (s skey))`, `(defstrand resp 3 (a a) (b b) (s s) (payload payload))`, `(uniq-orig s)`, `(non-orig (ltk a b))` | Skeleton 6 (`puzzle`): `(vars (a b name) (na payload text) (s skey))`, `(defstrand resp 3 (a a) (b b) (s s) (payload payload))`, `(deflistener s)`, `(uniq-orig s)`, `(non-orig (ltk a b))` | Skeleton 7 (`puzzle`): `(vars (payload na text) (a b name) (s skey))`, `(defstrand resp 3 (na na) (payload payload) (a a) (b b) (s s))`, `(defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))`, `(deflistener payload)`, `(precedes ((0 1) (1 1)) ((1 2) (0 2)))`, `(non-orig (ltk a b))`, `(uniq-orig s payload)`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for a complete set of `defskeleton` patterns testing initiator POV, responder POV, session-key secrecy (`(deflistener s)`), and payload secrecy (`(deflistener payload)`) on a single protocol.
- **Key S-Expression Excerpt** (lines 1–37):
```scheme
(herald puzzle_example)

;; Note that (ltk a b) \not= (ltk b a).  If we have a shared key with
;; this symmetry, then we need a lttle more structure in the middle
;; msg.

(defprotocol puzzle basic
  (defrole init
    (vars (a b name) (na payload text) (s skey))
    (trace
     (send na)
     (recv (enc na s (ltk a b)))
     (send (enc payload s))))

  (defrole resp
    (vars (a b name) (na payload text) (s skey))
    (trace
     (recv na)
     (send (enc na s (ltk a b)))
     (recv (enc payload s)))))

(defskeleton puzzle
  (vars (a b name) (na payload text) (s skey))
  (defstrand init 3 (a a) (b b) (na na) (payload payload))
  (uniq-orig na payload)
  (non-orig (ltk a b)))

(defskeleton puzzle
  (vars (a b name) (na payload text) (s skey))
  (defstrand init 3 (a a) (b b) (na na) (payload payload))
  (deflistener payload)
  (uniq-orig na payload)
  (non-orig (ltk a b)))

(defskeleton puzzle
  (vars (na payload text) (a b name) (s skey))
  (defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))
```

## reflect.scm

- **File Path**: `03_examples_scm/reflect.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald reflect)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `reflect`. Models a 2-message asymmetric signature protocol (`reflect`) where `init` sends `(enc b (invk a))` and receives `(enc a (invk b))`. Also demonstrates passing an inverted key `(b (invk b))` as a role parameter in the third skeleton and declaring `(non-orig (invk a) b)`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b akey)` | Role Assumptions: none | Trace (2 events): `(send (enc b (invk a)))` -> `(recv (enc a (invk b)))`
  - Role `resp`: Vars: `(a b akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc b (invk a)))` -> `(send (enc a (invk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`reflect`): `(vars (a b akey))`, `(defstrand resp 1 (a a) (b b))`, `(non-orig (invk a) (invk b))` | Skeleton 2 (`reflect`): `(vars (a b akey))`, `(defstrand init 2 (a a) (b b))`, `(non-orig (invk a) (invk b))` | Skeleton 3 (`reflect`): `(vars (a b akey))`, `(defstrand resp 1 (a a) (b (invk b)))`, `(non-orig (invk a) b)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `vars`
- **When to Reference This Example**: Reference this example when testing reflection attacks on two-message signature protocols or when instantiating an `akey` role parameter with an inverse key `(invk b)` in `defstrand`.
- **Key S-Expression Excerpt** (lines 1–32):
```scheme
(herald reflect)

;; A simple protocol vulnerable to a reflection attack

(defprotocol reflect basic
  (defrole init
    (vars (a b akey))
    (trace
     (send (enc b (invk a)))
     (recv (enc a (invk b)))))
  (defrole resp
    (vars (a b akey))
    (trace
     (recv (enc b (invk a)))
     (send (enc a (invk b))))))

;; Expect two shapes

(defskeleton reflect
  (vars (a b akey))
  (defstrand resp 1 (a a) (b b))
  (non-orig (invk a) (invk b)))

(defskeleton reflect
  (vars (a b akey))
  (defstrand init 2 (a a) (b b))
  (non-orig (invk a) (invk b)))

(defskeleton reflect
  (vars (a b akey))
  (defstrand resp 1 (a a) (b (invk b)))
  (non-orig (invk a) b))
```

## renamings.scm

- **File Path**: `03_examples_scm/renamings.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Blanchet's Simple Example Protocol" (comment "There is a flaw in this protocol by design") (comment "It also shows how variable renaming works"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `blanchet`. Models Bruno Blanchet's simple sign-then-encrypt protocol (`blanchet`) using intentionally permuted variable names across `init` (`a b name`, `s skey`, `d data`), `resp` (`d a name`, `b skey`, `s data`), and the `defskeleton` declarations (`(defstrand resp 2 (d s) (a d) (b a) (s b))`) to test CPSA's key-value variable renaming and binding logic.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(s skey)`, `(d data)` | Role Assumptions: none | Trace (2 events): `(send (enc (enc s (privk a)) (pubk b)))` -> `(recv (enc d s))`
  - Role `resp`: Vars: `(d a name)`, `(b skey)`, `(s data)` | Role Assumptions: none | Trace (2 events): `(recv (enc (enc b (privk d)) (pubk a)))` -> `(send (enc s b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`blanchet`): `(vars (s d name) (a skey) (b data))`, `(defstrand resp 2 (d s) (a d) (b a) (s b))`, `(non-orig (privk s) (privk d))`, `(uniq-orig a)` | Skeleton 2 (`blanchet`): `(vars (s d name) (a skey) (b data))`, `(defstrand init 2 (a s) (b d) (s a) (d b))`, `(non-orig (privk d))`, `(uniq-orig a)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example to understand how `(defstrand <role> <height> (<role-var> <skel-var>)...)` maps role-local variable names (left) to skeleton-level variable names (right) even when their identifiers overlap.
- **Key S-Expression Excerpt** (lines 1–30):
```scheme
(herald "Blanchet's Simple Example Protocol"
	(comment "There is a flaw in this protocol by design")
	(comment "It also shows how variable renaming works"))

(defprotocol blanchet basic
  (defrole init
    (vars (a b name) (s skey) (d data))
    (trace
     (send (enc (enc s (privk a)) (pubk b)))
     (recv (enc d s))))
  (defrole resp
    (vars (d a name) (b skey) (s data))
    (trace
     (recv (enc (enc b (privk d)) (pubk a)))
     (send (enc s b))))
  (comment "Blanchet's protocol using named asymmetric keys"))

(defskeleton blanchet
  (vars (s d name) (a skey) (b data))
  (defstrand resp 2 (d s) (a d) (b a) (s b))
  (non-orig (privk s) (privk d))
  (uniq-orig a)
  (comment "Analyze from the responder's perspective"))

(defskeleton blanchet
  (vars (s d name) (a skey) (b data))
  (defstrand init 2 (a s) (b d) (s a) (d b))
  (non-orig (privk d))
  (uniq-orig a)
  (comment "Analyze from the initiator's perspective"))
```

## role_uniq.scm

- **File Path**: `03_examples_scm/role_uniq.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Role Unique Origination")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `blanchet`. Demonstrates that a role-level `(uniq-orig s)` assumption in `init` of Blanchet's protocol (`blanchet`) is equivalent to omitting `(uniq-orig s)` from the role and instead adding a protocol rule `(defrule role-uniq (forall ((z strd) (s skey)) (implies (p "init" "s" z s) (uniq s))))`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b akey)`, `(s skey)`, `(d data)` | Role Assumptions: `(uniq-orig s)` | Trace (2 events): `(send (enc (enc s (invk a)) b))` -> `(recv (enc d s))`
  - Role `resp`: Vars: `(a b akey)`, `(s skey)`, `(d data)` | Role Assumptions: none | Trace (2 events): `(recv (enc (enc s (invk a)) b))` -> `(send (enc d s))`
  - Role `init`: Vars: `(a b akey)`, `(s skey)`, `(d data)` | Role Assumptions: none | Trace (2 events): `(send (enc (enc s (invk a)) b))` -> `(recv (enc d s))`
  - Role `resp`: Vars: `(a b akey)`, `(s skey)`, `(d data)` | Role Assumptions: none | Trace (2 events): `(recv (enc (enc s (invk a)) b))` -> `(send (enc d s))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `role-uniq`: `(forall ((z strd) (s skey)) (implies (p "init" "s" z s) (uniq s)))`
  - **Goals**: None
  - **Skeletons (4)**: Skeleton 1 (`blanchet`): `(vars (a b akey) (s skey) (d data))`, `(defstrand init 2 (a a) (b b) (s s) (d d))`, `(non-orig (invk b))` | Skeleton 2 (`blanchet`): `(vars (a b akey) (s skey) (d data))`, `(defstrand resp 2 (a a) (b b) (s s) (d d))`, `(non-orig (invk a) (invk b))` | Skeleton 3 (`blanchet`): `(vars (a b akey) (s skey) (d data))`, `(defstrand init 2 (a a) (b b) (s s) (d d))`, `(non-orig (invk b))` | Skeleton 4 (`blanchet`): `(vars (a b akey) (s skey) (d data))`, `(defstrand resp 2 (a a) (b b) (s s) (d d))`, `(non-orig (invk a) (invk b))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `forall`, `herald`, `implies`, `non-orig`, `p`, `recv`, `send`, `trace`, `uniq`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example to see how role-level `(uniq-orig ...)` declarations work and how they can be expressed equivalently as logical rules (`(defrule ... (implies (p "init" "s" z s) (uniq s)))`).
- **Key S-Expression Excerpt** (lines 29–56):
```scheme
(defprotocol blanchet basic
  (defrole init
    (vars (a b akey) (s skey) (d data))
    (trace
     (send (enc (enc s (invk a)) b))
     (recv (enc d s))))
  (defrole resp
    (vars (a b akey) (s skey) (d data))
    (trace
     (recv (enc (enc s (invk a)) b))
     (send (enc d s))))
  (defrule role-uniq
    (forall ((z strd) (s skey))
	    (implies (p "init" "s" z s)
		     (uniq s))))
  (comment "Blanchet's protocol using unnamed asymmetric keys"))

(defskeleton blanchet
  (vars (a b akey) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (non-orig (invk b))
  (comment "Analyze from the initiator's perspective"))

(defskeleton blanchet
  (vars (a b akey) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (non-orig (invk a) (invk b))
  (comment "Analyze from the responder's perspective"))
```

## rule-node.scm

- **File Path**: `03_examples_scm/rule-node.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald rule-node)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `rule-order`, `rule-order-prec`. Tests rules and facts over strand (`strd`) and node index (`indx`) variables in two protocols (`rule-order` and `rule-order-prec`), demonstrating the `(idx 0)` and `(idx 1)` index literal constructors inside skeleton `(facts (le 0 (idx 0) 0 (idx 1)))` as well as `(prec z1 i1 z2 i2)` and `(neq (s t))`.
- **Roles & Variables**:
  - Role `init` (in `rule-order`): Vars: `(s t text)` | Role Assumptions: none | Trace (2 events): `(send (cat s t))` -> `(recv (cat t s))`
  - Role `init` (in `rule-order-prec`): Vars: `(s t text)` | Role Assumptions: none | Trace (2 events): `(send (cat s t))` -> `(recv (cat t s))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (5)**: `le-lt`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (fact le z1 i1 z2 i2) (or (and (= z1 z2) (= i1 i2)) (fact lt z1 i1 z2 i2))))`; `lt-le`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (fact lt z1 i1 z2 i2) (fact le z1 i1 z2 i2)))`; `prec-lt`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (prec z1 i1 z2 i2) (or (fact lt z1 i1 z2 i2))))`; `neq-false`: `(forall ((s mesg)) (implies (fact neq s s) (false)))`; `prec-tell-me`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (prec z1 i1 z2 i2) (fact tell-me z1 i1 z2 i2)))`
  - **Goals**: None
  - **Skeletons (5)**: Skeleton 1 (`rule-order`): `(vars (s t s1 t1 text))`, `(defstrand init 2 (s s) (t t))`, `(defstrand init 2 (s t) (t s))`, `(precedes ((1 0) (0 1)))`, `(facts (neq s t))`, `(facts (le 0 (idx 0) 0 (idx 1)))` | Skeleton 2 (`rule-order`): `(vars (s t text))`, `(defstrand init 2 (s s) (t t))`, `(defstrand init 2 (s t) (t s))`, `(precedes ((1 0) (0 1)))`, `(facts (le 1 (idx 0) 0 (idx 1)) (le 0 (idx 0) 0 (idx 1)))` | Skeleton 3 (`rule-order-prec`): `(vars (s t text))`, `(defstrand init 2 (s s) (t t))` | Skeleton 4 (`rule-order-prec`): `(vars (s t text))`, `(defstrand init 2 (s s) (t t))`, `(defstrand init 2 (s t) (t s))`, `(precedes ((1 0) (0 1)))` | Skeleton 5 (`rule-order-prec`): `(vars (s t text))`, `(defstrand init 2 (s s) (t t))`, `(defstrand init 2 (s s) (t t))`, `(precedes ((1 0) (0 1)))`, `(neq (s t))`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `false`, `forall`, `herald`, `implies`, `le`, `neq`, `or`, `prec`, `precedes`, `recv`, `send`, `trace`, `vars`
- **When to Reference This Example**: Reference this example whenever you need to write rules or skeleton `facts` that reference specific strand node indices (`indx` sort and `(idx <int>)` literals) alongside `(prec z1 i1 z2 i2)`.
- **Key S-Expression Excerpt** (lines 1–36):
```scheme
(herald rule-node)

(defprotocol rule-order basic
  (defrole init
    (vars (s t text))
    (trace
     (send (cat s t))
     (recv (cat t s))))

  (defrule le-lt
    (forall ((z1 z2 strd)(i1 i2 indx))
    	    (implies
    	     (fact le z1 i1 z2 i2)
    	     (or
    	      (and (= z1 z2) (= i1 i2))
    	      (fact lt z1 i1 z2 i2)))))

  (defrule lt-le
    (forall ((z1 z2 strd)(i1 i2 indx))
    	    (implies
    	     (fact lt z1 i1 z2 i2)
    	     (fact le z1 i1 z2 i2))))

  (defrule prec-lt
    (forall ((z1 z2 strd)(i1 i2 indx))
	    (implies
	     (prec z1 i1 z2 i2)
	     (or
	      (fact lt z1 i1 z2 i2)))))

  (defrule neq-false
    (forall ((s mesg))
	    (implies (fact neq s s)
		     (false))))
  )

```

## rule-order.scm

- **File Path**: `03_examples_scm/rule-order.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald rule-order)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `rule-order`. Minimal test (`rule-order`) of a disjunctive rule (`ge`: `(forall ((x y text)) (implies (fact le x y) (or (= x y) (fact lt x y))))`) triggered by `(facts (le s t))` in a skeleton, splitting the search into two branches (`s = t` and `(fact lt s t)`).
- **Roles & Variables**:
  - Role `init`: Vars: `(s t text)` | Role Assumptions: none | Trace (1 events): `(send (cat s t))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `ge`: `(forall ((x y text)) (implies (fact le x y) (or (= x y) (fact lt x y))))`
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`rule-order`): `(vars (s t text))`, `(defstrand init 1 (s s) (t t))`, `(facts (le s t))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `forall`, `herald`, `implies`, `le`, `or`, `send`, `trace`, `vars`
- **When to Reference This Example**: Reference this example for a minimal template of a disjunctive `(defrule ...)` using `(or (= x y) (fact lt x y))` to split CPSA's analysis into equality and strict-inequality cases.
- **Key S-Expression Excerpt** (lines 1–21):
```scheme
(herald rule-order)

(defprotocol rule-order basic
  (defrole init
    (vars (s t text))
    (trace
     (send (cat s t))))

  (defrule ge
    (forall ((x y text))
	    (implies
	     (fact le x y)
	     (or
	      (= x y)
	      (fact lt x y)))))
  )

(defskeleton rule-order
  (vars (s t text))
  (defstrand init 1 (s s) (t t))
  (facts (le s t)))
```

## rules.scm

- **File Path**: `03_examples_scm/rules.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Rules and Facts")`; `(herald doorsep (comment "Door Simple Example Protocol"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `neq-test`, `doorsep`. Contains two complete rule-based protocol examples in one file (each with its own `herald`): `neq-test` (enforcing `n1 != n2` via `(facts (neq n1 n2))` and `(defrule neq ...)`) and `doorsep` (the Door Simple Example Protocol, using `(defrule trust ...)` to express that if an uncompromised person `(non (invk p))` initiates a session with door `d`, then the door's private key is also uncompromised `(non (invk d))`).
- **Roles & Variables**:
  - Role `init` (in `neq-test`): Vars: `(n1 n2 text)`, `(k skey)` | Role Assumptions: `(non-orig k)`, `(uniq-orig n1 n2)` | Trace (2 events): `(send (cat n1 (enc n1 n2 k)))` -> `(recv n2)`
  - Role `person` (in `doorsep`): Vars: `(d p akey)`, `(k skey)`, `(t text)` | Role Assumptions: `(uniq-orig k)` | Trace (3 events): `(send (enc (enc k (invk p)) d))` -> `(recv (enc t k))` -> `(send t)`
  - Role `door` (in `doorsep`): Vars: `(d p akey)`, `(k skey)`, `(t text)` | Role Assumptions: `(uniq-orig t)` | Trace (3 events): `(recv (enc (enc k (invk p)) d))` -> `(send (enc t k))` -> `(recv t)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (2)**: `neq`: `(forall ((a mesg)) (implies (fact neq a a) (false)))`; `trust`: `(forall ((z strd) (p d akey)) (implies (and (p "person" z 1) (p "person" "p" z p) (p "person" "d" z d) (non (invk p))) (non (invk d))))`
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`neq-test`): `(vars)`, `(defstrand init 2)` | Skeleton 2 (`neq-test`): `(vars (n1 n2 text))`, `(defstrand init 2 (n1 n1) (n2 n2))`, `(facts (neq n1 n2))` | Skeleton 3 (`doorsep`): `(vars (p akey))`, `(defstrand door 3 (p p))`, `(non-orig (invk p))`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `false`, `forall`, `herald`, `implies`, `neq`, `non`, `non-orig`, `p`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for the canonical `trust` rule pattern (`(implies (and (p "person" z 1) ... (non (invk p))) (non (invk d)))`), which dynamically derives `(non (invk d))` for whatever peer `d` an honest principal `p` chooses to trust.
- **Key S-Expression Excerpt** (lines 35–67):
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

## scep-tls-dh-broken.scm

- **File Path**: `03_examples_scm/scep-tls-dh-broken.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "Fordham's GREATEST PROTOCOL GO RAMS🐏🐏🐏🐏🐏🐏🐏🐏🐏🐏 Protocol" (algebra diffie-hellman) (comment "By: Mario Marku & Luke Shragher"))` | Flags: `(algebra diffie-hellman)`
- **Protocol & Purpose**: Protocol(s): `dh`. Models a combined TLS + SCEP (Simple Certificate Enrollment Protocol) handshake (`dh`) in the `diffie-hellman` algebra using extensive `(defmacro ...)` definitions (`PMS`, `S_write`, `W_write`, `Tok`, `SCEP-Token`, `Cert_W`, `W_KE`, `S_FMESG`, `SFIN`, `WFIN`) and a confidentiality `(defgoal dh ...)` testing whether an adversary listener `eve` (`(p "" eve 1) (p "" "x" eve (SCEP-Token S M rS))`) can learn the client's SCEP token when `rSp` is sent in the clear.
- **Roles & Variables**:
  - Role `client`: Vars: `(S W M CA name)`, `(rS rW rSp rWp w text)`, `(dh_eS dh_eW rndx)` | Role Assumptions: `(uniq-orig rS rSp)` | Trace (7 events): `(send rSp)` -> `(recv (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))` -> `(send (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))` -> `(recv (WFIN dh_eS dh_eW rSp rWp W CA))` -> `(send (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))` -> `(recv (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))` -> `(send (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))`
  - Role `server`: Vars: `(S W M CA name)`, `(rS rW rSp rWp w text)`, `(dh_eS dh_eW rndx)` | Role Assumptions: `(uniq-orig rW rWp w)` | Trace (7 events): `(recv rSp)` -> `(send (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))` -> `(recv (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))` -> `(send (WFIN dh_eS dh_eW rSp rWp W CA))` -> `(recv (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))` -> `(send (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))` -> `(recv (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (10)**: `(PMS dh_es dh_ew)`, `(S_write dh_es dh_ew rs rw)`, `(W_write dh_es dh_ew rs rw)`, `(Tok X Y data)`, `(SCEP-Token X Y data)`, `(Cert_W W CA dh_ew)`, `(W_KE dh_ew rs rw W)`, `(S_FMESG rs rw W CA dh_ew)`, `(SFIN dh_es dh_ew rs rw W CA)`, `(WFIN dh_es dh_ew rs rw W CA)`
  - **Rules & Lemmas**: None
  - **Goals (1)**: `(defgoal dh (forall ((S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx) (z1 eve strd)) (implies (and (p "client" z1 7) (p "client" "S" z1 S) (p "client" "W" z1 W) (p "client" "M" z1 M) (p "client" "CA" z1 CA) (p "client" "rS" z1 rS) (p "client" "rW" z1 rW) (p "client" "rSp" z1 rSp) (p "client" "rWp" z1 rWp) (p "client" "w" z1 w) (p "client" "dh_eS" z1 dh_eS) (p "client" "dh_eW" z1 dh_eW) (non (privk S)) (non (privk W)) (non (privk M)) (non (privk CA)) (p "" eve 1) (p "" "x" eve (SCEP-Token S M rS))) (false))))`
  - **Skeletons**: None active (note: `;`-commented `defskeleton` blocks appear at the bottom of `scep-tls-dh-broken.scm`)
  - **Keywords & Predicates Used**: `algebra`, `and`, `comment`, `defgoal`, `defmacro`, `defprotocol`, `defrole`, `false`, `forall`, `herald`, `implies`, `non`, `p`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling complex layered protocols (like SCEP over TLS with Diffie-Hellman ephemeral key exchange `(exp (gen) (mul dh_es dh_ew))`) using modular `(defmacro ...)` definitions and low-level `(p ...)` confidentiality goals.
- **Key S-Expression Excerpt** (lines 1–35):
```scheme
(herald "Fordham's GREATEST PROTOCOL GO RAMS🐏🐏🐏🐏🐏🐏🐏🐏🐏🐏 Protocol"
  (algebra diffie-hellman)
  (comment "By: Mario Marku & Luke Shragher"))

;; ==========================================
;; MACRO DEFINITIONS
;; ==========================================
(defmacro (PMS dh_es dh_ew)
  (exp (gen) (mul dh_es dh_ew)))

(defmacro (S_write dh_es dh_ew rs rw)
  (hash (PMS dh_es dh_ew) rs rw "client-write"))

(defmacro (W_write dh_es dh_ew rs rw)
  (hash (PMS dh_es dh_ew) rs rw "server-write"))

;; SCEP Tokens
(defmacro (Tok X Y data)
  (cat "Token" X (pubk X) Y (pubk Y) data))

(defmacro (SCEP-Token X Y data)
  (cat (Tok X Y data) (enc (hash (Tok X Y data)) (privk Y))))

;; TLS Components
(defmacro (Cert_W W CA dh_ew)
  (cat W (pubk W) (enc (hash W (exp (gen) dh_ew)) (privk CA))))

(defmacro (W_KE dh_ew rs rw W)
  (cat (exp (gen) dh_ew)
       (enc (hash rs rw (exp (gen) dh_ew)) (privk W))))

(defmacro (S_FMESG rs rw W CA dh_ew)
  (cat rs rw (Cert_W W CA dh_ew) (W_KE dh_ew rs rw W)))

(defmacro (SFIN dh_es dh_ew rs rw W CA)
```

## scep-tls-dh-fixed.scm

- **File Path**: `03_examples_scm/scep-tls-dh-fixed.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "Fordham's GREATEST PROTOCOL GO RAMS🐏🐏🐏🐏🐏🐏🐏🐏🐏🐏 Protocol" (algebra diffie-hellman) (comment "By: Mario Marku & Luke Shragher"))` | Flags: `(algebra diffie-hellman)`
- **Protocol & Purpose**: Protocol(s): `dh`. Fixed version of `scep-tls-dh-broken.scm` in the `diffie-hellman` algebra where the client encrypts its initial nonce `(send (enc rSp (pubk W)))` under the server's public key, alongside both a confidentiality `(defgoal dh ...)` and two active `(defskeleton dh ...)` declarations using `(defstrandmax client ...)` and `(defstrandmax server ...)` with `(pen-non-orig (privk S) (privk W) (privk CA))`.
- **Roles & Variables**:
  - Role `client`: Vars: `(S W M CA name)`, `(rS rW rSp rWp w text)`, `(dh_eS dh_eW rndx)` | Role Assumptions: `(uniq-orig rS rSp)` | Trace (7 events): `(send (enc rSp (pubk W)))` -> `(recv (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))` -> `(send (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))` -> `(recv (WFIN dh_eS dh_eW rSp rWp W CA))` -> `(send (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))` -> `(recv (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))` -> `(send (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))`
  - Role `server`: Vars: `(S W M CA name)`, `(rS rW rSp rWp w text)`, `(dh_eS dh_eW rndx)` | Role Assumptions: `(uniq-orig rW rWp w)` | Trace (7 events): `(recv (enc rSp (pubk W)))` -> `(send (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))` -> `(recv (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))` -> `(send (WFIN dh_eS dh_eW rSp rWp W CA))` -> `(recv (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))` -> `(send (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))` -> `(recv (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (10)**: `(PMS dh_es dh_ew)`, `(S_write dh_es dh_ew rs rw)`, `(W_write dh_es dh_ew rs rw)`, `(Tok X Y data)`, `(SCEP-Token X Y data)`, `(Cert_W W CA dh_ew)`, `(W_KE dh_ew rs rw W)`, `(S_FMESG rs rw W CA dh_ew)`, `(SFIN dh_es dh_ew rs rw W CA)`, `(WFIN dh_es dh_ew rs rw W CA)`
  - **Rules & Lemmas**: None
  - **Goals (1)**: `(defgoal dh (forall ((S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx) (z1 eve strd)) (implies (and (p "client" z1 7) (p "client" "S" z1 S) (p "client" "W" z1 W) (p "client" "M" z1 M) (p "client" "CA" z1 CA) (p "client" "rS" z1 rS) (p "client" "rW" z1 rW) (p "client" "rSp" z1 rSp) (p "client" "rWp" z1 rWp) (p "client" "w" z1 w) (p "client" "dh_eS" z1 dh_eS) (p "client" "dh_eW" z1 dh_eW) (non (privk S)) (non (privk W)) (non (privk M)) (non (privk CA)) (p "" eve 1) (p "" "x" eve (SCEP-Token S M rS))) (false))))`
  - **Skeletons (2)**: Skeleton 1 (`dh`): `(vars (S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx))`, `(defstrandmax client (S S) (W W) (M M) (CA CA) (rS rS) (rW rW) (rSp rSp) (rWp rWp) (w w) (dh_eS dh_eS) (dh_eW dh_eW))`, `(pen-non-orig (privk S) (privk W) (privk CA))` | Skeleton 2 (`dh`): `(vars (S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx))`, `(defstrandmax server (S S) (W W) (M M) (CA CA) (rS rS) (rW rW) (rSp rSp) (rWp rWp) (w w) (dh_eS dh_eS) (dh_eW dh_eW))`, `(pen-non-orig (privk S) (privk W) (privk CA))`
  - **Keywords & Predicates Used**: `algebra`, `and`, `comment`, `defgoal`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `false`, `forall`, `herald`, `implies`, `non`, `p`, `pen-non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for combining `diffie-hellman` algebra macros, a confidentiality `(defgoal ...)`, and `(defstrandmax <role> ...)` skeletons in a full TLS + application-layer protocol model.
- **Key S-Expression Excerpt** (lines 88–122):
```scheme
(defgoal dh
  (forall ((S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx) (z1 eve strd))
    (implies
      (and
        ;; The Client strand runs to full completion
        (p "client" z1 7)
        (p "client" "S" z1 S)
        (p "client" "W" z1 W)
        (p "client" "M" z1 M)
        (p "client" "CA" z1 CA)
        (p "client" "rS" z1 rS)
        (p "client" "rW" z1 rW)
        (p "client" "rSp" z1 rSp)
        (p "client" "rWp" z1 rWp)
        (p "client" "w" z1 w)
        (p "client" "dh_eS" z1 dh_eS)
        (p "client" "dh_eW" z1 dh_eW)

        ; We assume the longterm keys of all involved parties are not compromised
        (non (privk S))
        (non (privk W))
        (non (privk M))
        (non (privk CA))

        ;The adversary listener strand "eve" attempts to intercept the SCEP Token
        (p "" eve 1)
        (p "" "x" eve (SCEP-Token S M rS))
      )
      ;If all the above is true, it implies a logical impossibility (false)
      (false))))
  (comment "Confidentiality goal: The adversary cannot learn the SCEP-Token S M rS")


  ; view client pov, perfect ladder
(defskeleton dh
```

## sdls-auth-enc-full-payload.scm

- **File Path**: `03_examples_scm/sdls-auth-enc-full-payload.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP Authenticated Encryption: full SDLS-EP rekeying sequence")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-ep-chain-auth-enc`. Full 6-step Space Data Link Security Extended Procedures (CCSDS SDLS-EP, 355.0-B-2 / 355.1-B-1) rekeying chain (`sdls-ep-chain-auth-enc`) in Authenticated Encryption mode between `ground` and `satellite`. Models (1) OTAR key upload under `keymaster`, (2) Key Activation, (3) Rekey SA, (4) Start SA, (5) Key Verification challenge/reply, and (6) Frame Data traffic under the new session keys (`sessionkey1`, `sessionkey2`) and reset sequence number `(successor new_arsn)`, using custom language sorts and hash constructors `(lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash) (spi atom) (gvcid atom))`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(old_arsn new_arsn seq_n)`, `(iv text)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)`, `(keymaster sessionkey1 sessionkey2 skey)`, `(keyid1 keyid2 keyid)`, `(spi spi)`, `(gvcid gvcid)`, `(chal text)`, `(frame_data tc)` | Role Assumptions: `(uniq-gen assumed_enc_key assumed_auth_key old_arsn)`, `(uniq-orig new_arsn chal frame_data sessionkey1 sessionkey2)`, `(non-orig keymaster)` | Trace (7 events): `(send (cat (sdl_header spacecraft) header (successor old_arsn) (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) (hash (sdl_header spacecraft) header (successor old_arsn) (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor old_arsn)) (enc (key_activation_pdu keyid1) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor old_arsn)) (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (enc (start_sa_pdu spi gvcid) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (enc (keyver_cmd keyid1 chal) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor new_arsn) (enc frame_data sessionkey1) (hash (sdl_header spacecraft) header (successor new_arsn) (enc frame_data sessionkey1) sessionkey2)))`
  - Role `satellite`: Vars: `(header text)`, `(old_arsn new_arsn seq_n)`, `(iv text)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)`, `(keymaster sessionkey1 sessionkey2 skey)`, `(keyid1 keyid2 keyid)`, `(spi spi)`, `(gvcid gvcid)`, `(chal text)`, `(frame_data tc)` | Role Assumptions: `(non-orig keymaster)` | Trace (7 events): `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) (hash (sdl_header spacecraft) header (successor old_arsn) (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor old_arsn)) (enc (key_activation_pdu keyid1) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor old_arsn)) (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (enc (start_sa_pdu spi gvcid) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (enc (keyver_cmd keyid1 chal) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor new_arsn) (enc frame_data sessionkey1) (hash (sdl_header spacecraft) header (successor new_arsn) (enc frame_data sessionkey1) sessionkey2)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (9)**: `(sdl_header dest)`, `(otar_pdu masterkeyid uploadblock)`, `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)`, `(otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)`, `(key_activation_pdu keyid)`, `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)`, `(start_sa_pdu spi gvcid)`, `(keyver_cmd keyid chal)`, `(keyver_reply keyid chal sessionkey)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash) (spi atom) (gvcid atom))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-ep-chain-auth-enc`): `(vars (assumed_enc_key assumed_auth_key keymaster skey) (ground spacecraft name) (old_arsn new_arsn seq_n))`, `(defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keymaster keymaster) (old_arsn old_arsn) (new_arsn new_arsn) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_enc_key assumed_auth_key keymaster)`, `(facts (neq old_arsn new_arsn))` | Skeleton 2 (`sdls-ep-chain-auth-enc`): `(vars (assumed_enc_key assumed_auth_key keymaster sessionkey1 sessionkey2 skey) (ground spacecraft name) (old_arsn new_arsn seq_n))`, `(defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2) (old_arsn old_arsn) (new_arsn new_arsn) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_enc_key assumed_auth_key keymaster)`, `(uniq-orig sessionkey1 sessionkey2)`, `(facts (neq old_arsn new_arsn))`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `facts`, `herald`, `lang`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling multi-step key management and rekeying protocols (such as CCSDS SDLS-EP, IPsec/IKEv2 SA rekeying, or counter/sequence-number progression) using custom `(lang (<sort> atom) (<op> hash))` declarations.
- **Key S-Expression Excerpt** (lines 171–206):
```scheme
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
                   (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key))
      )


      (send
        (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
             (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key)
             (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
                   (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key))
      )

      ;; STEP 6 -- new SA carries traffic under the OTAR'd keys
      (recv
        (cat (sdl_header spacecraft) header (successor new_arsn)
             (enc frame_data sessionkey1)
             (hash (sdl_header spacecraft) header (successor new_arsn)
                   (enc frame_data sessionkey1) sessionkey2))
      )

    )
    (non-orig keymaster)
  )

  (lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash)
        (spi atom) (gvcid atom))
)


(defskeleton sdls-ep-chain-auth-enc
  (vars (assumed_enc_key assumed_auth_key keymaster skey) (ground spacecraft name)
        (old_arsn new_arsn seq_n))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (keymaster keymaster)
                          (old_arsn old_arsn) (new_arsn new_arsn)
```

## sdls-auth-enc-logic.scm

- **File Path**: `03_examples_scm/sdls-auth-enc-logic.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP Authenticated Encryption")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-auth-enc`. Core framing logic of CCSDS Space Data Link Security Protocol (`sdls-auth-enc`) in Authenticated Encryption mode (encrypt-then-MAC), where `ground` and `satellite` exchange frames containing `(cat (sdl_header ...) header old_arsn (enc frame_data assumed_enc_key) (hash ... assumed_auth_key))` and advance the anti-replay sequence number via `(successor old_arsn)`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(frame_data tc)`, `(old_arsn seq_n)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) (hash (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) assumed_auth_key)))`
  - Role `satellite`: Vars: `(header text)`, `(frame_data tc)`, `(old_arsn seq_n)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) (hash (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (1)**: `(sdl_header dest)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (tc atom) (successor hash))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-auth-enc`): `(vars (header text) (frame_data tc) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (ground spacecraft name))`, `(defstrandmax ground (header header) (frame_data frame_data) (old_arsn old_arsn) (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spacecraft spacecraft) (ground ground))`, `(non-orig assumed_enc_key assumed_auth_key)`, `(uniq-orig old_arsn)` | Skeleton 2 (`sdls-auth-enc`): `(vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name))`, `(defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_enc_key assumed_auth_key)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for a clean, minimal pattern of Encrypt-then-MAC framing with monotonic sequence numbers `(successor old_arsn)` declared via `(lang (seq_n atom) (tc atom) (successor hash))`.
- **Key S-Expression Excerpt** (lines 1–38):
```scheme
(herald "SDLSP Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defprotocol sdls-auth-enc basic

  ;; Ground station sends an authenticated + encrypted SDLS frame
  (defrole ground
    (vars (header text) (frame_data tc) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (ground spacecraft name))
    (trace
      (send
        (cat (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) assumed_auth_key))
      )
      (recv
        (cat (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key)
             (hash (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) assumed_auth_key))
      )
    )
  )

  ;; Satellite receives the authenticated + encrypted SDLS frame
  (defrole satellite
    (vars (header text) (frame_data tc) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (ground spacecraft name))
    (trace
      (recv
        (cat (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) assumed_auth_key))
      )
      (send
        (cat (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key)
             (hash (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) assumed_auth_key))
      )
    )
  )

  (lang (seq_n atom) (tc atom) (successor hash))
)
```

## sdls-auth-full-payload.scm

- **File Path**: `03_examples_scm/sdls-auth-full-payload.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP TC Baseline: Authentication Only (AES-CMAC): full SDLS-EP rekeying sequence")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-ep-chain-auth`. Full 6-step CCSDS SDLS-EP rekeying sequence (`sdls-ep-chain-auth`) in Authentication-Only (AES-CMAC) baseline mode, where PDUs and frame payloads are sent in cleartext accompanied by keyed MACs `(hash ... assumed_auth_key)` (except OTAR key upload encrypted under `keymaster` and the Key Verification challenge encryption `(enc chal sessionkey1)`).
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(old_arsn new_arsn seq_n)`, `(iv text)`, `(assumed_auth_key skey)`, `(ground spacecraft name)`, `(keymaster sessionkey1 sessionkey2 skey)`, `(keyid1 keyid2 keyid)`, `(spi spi)`, `(gvcid gvcid)`, `(chal text)`, `(frame_data tc)` | Role Assumptions: none | Trace (7 events): `(send (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor old_arsn)) (key_activation_pdu keyid1) (hash (sdl_header spacecraft) header (successor (successor old_arsn)) (key_activation_pdu keyid1) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (start_sa_pdu spi gvcid) (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (start_sa_pdu spi gvcid) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (keyver_cmd keyid1 chal) (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (keyver_cmd keyid1 chal) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (keyver_reply keyid1 chal sessionkey1) (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor new_arsn) frame_data (hash (sdl_header spacecraft) header (successor new_arsn) frame_data sessionkey2)))`
  - Role `satellite`: Vars: `(header text)`, `(old_arsn new_arsn seq_n)`, `(iv text)`, `(assumed_auth_key skey)`, `(ground spacecraft name)`, `(keymaster sessionkey1 sessionkey2 skey)`, `(keyid1 keyid2 keyid)`, `(spi spi)`, `(gvcid gvcid)`, `(chal text)`, `(frame_data tc)` | Role Assumptions: none | Trace (7 events): `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor old_arsn)) (key_activation_pdu keyid1) (hash (sdl_header spacecraft) header (successor (successor old_arsn)) (key_activation_pdu keyid1) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (start_sa_pdu spi gvcid) (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (start_sa_pdu spi gvcid) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (keyver_cmd keyid1 chal) (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (keyver_cmd keyid1 chal) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (keyver_reply keyid1 chal sessionkey1) (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor new_arsn) frame_data (hash (sdl_header spacecraft) header (successor new_arsn) frame_data sessionkey2)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (9)**: `(sdl_header dest)`, `(otar_pdu masterkeyid uploadblock)`, `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)`, `(otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)`, `(key_activation_pdu keyid)`, `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)`, `(start_sa_pdu spi gvcid)`, `(keyver_cmd keyid chal)`, `(keyver_reply keyid chal sessionkey)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash) (spi atom) (gvcid atom))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-ep-chain-auth`): `(vars (assumed_auth_key keymaster skey) (ground spacecraft name) (old_arsn new_arsn seq_n))`, `(defstrandmax satellite (assumed_auth_key assumed_auth_key) (keymaster keymaster) (old_arsn old_arsn) (new_arsn new_arsn) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_auth_key keymaster)`, `(facts (neq old_arsn new_arsn))`, `(non-orig keymaster)` | Skeleton 2 (`sdls-ep-chain-auth`): `(vars (assumed_auth_key keymaster sessionkey1 sessionkey2 skey) (ground spacecraft name) (old_arsn new_arsn seq_n) (chal text) (frame_data tc))`, `(defstrandmax ground (assumed_auth_key assumed_auth_key) (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2) (old_arsn old_arsn) (new_arsn new_arsn) (ground ground) (spacecraft spacecraft) (chal chal) (frame_data frame_data))`, `(non-orig assumed_auth_key keymaster)`, `(uniq-orig sessionkey1 sessionkey2)`, `(facts (neq old_arsn new_arsn))`, `(uniq-gen old_arsn)`, `(uniq-orig new_arsn chal frame_data sessionkey1 sessionkey2)`, `(non-orig keymaster)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `facts`, `herald`, `lang`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling authenticated-only (MAC/CMAC/HMAC) protocol framing and key rollovers where control headers and payloads are integrity-protected via `(hash ... auth_key)` while key transport remains encrypted.
- **Key S-Expression Excerpt** (lines 168–205):
```scheme
      ;; STEP 4 -- Start SA, 3.3.3.1

      (recv
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
             (keyver_cmd keyid1 chal)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
                   (keyver_cmd keyid1 chal) assumed_auth_key))
      )
      (send
        (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
             (keyver_reply keyid1 chal sessionkey1)
             (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
                   (keyver_reply keyid1 chal sessionkey1) assumed_auth_key))
      )
      ;; STEP 5 -- Key Verification, 3.2.3.5

      (recv
        (cat (sdl_header spacecraft) header (successor new_arsn)
             frame_data
             (hash (sdl_header spacecraft) header (successor new_arsn)
                   frame_data sessionkey2))
      )
      ;; STEP 6 -- new SA carries traffic under the OTAR'd keys
    )
  )

  (lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash)
        (spi atom) (gvcid atom))
)

(defskeleton sdls-ep-chain-auth
  (vars (assumed_auth_key keymaster skey) (ground spacecraft name)
        (old_arsn new_arsn seq_n))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (keymaster keymaster)
                          (old_arsn old_arsn) (new_arsn new_arsn)
                          (ground ground) (spacecraft spacecraft))
  (non-orig assumed_auth_key keymaster)
```

## sdls-auth-logic.scm

- **File Path**: `03_examples_scm/sdls-auth-logic.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP TC Baseline: Authentication Only (AES-CMAC)")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-tc-auth`. Models CCSDS SDLS Telecommand Baseline Authentication-Only mode (`sdls-tc-auth`) and includes a confidentiality `(defgoal sdls-tc-auth ...)` demonstrating the high-level goal predicates `(strand ground z1 2 ...)`, `(pnon assumed_auth_key)`, `(ugen old_arsn)`, `(uniq frame_data)`, and `(listener eve frame_data)`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(frame_data tc)`, `(old_arsn seq_n)`, `(assumed_auth_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) header (successor old_arsn) frame_data (hash (sdl_header spacecraft) header (successor old_arsn) frame_data assumed_auth_key)))` -> `(recv (cat (sdl_header ground) (successor (successor old_arsn)) frame_data (hash (sdl_header ground) (successor (successor old_arsn)) frame_data assumed_auth_key)))`
  - Role `satellite`: Vars: `(header text)`, `(frame_data tc)`, `(old_arsn seq_n)`, `(assumed_auth_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) header (successor old_arsn) frame_data (hash (sdl_header spacecraft) header (successor old_arsn) frame_data assumed_auth_key)))` -> `(send (cat (sdl_header ground) (successor (successor old_arsn)) frame_data (hash (sdl_header ground) (successor (successor old_arsn)) frame_data assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (1)**: `(sdl_header dest)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (tc atom) (successor hash))`
  - **Rules & Lemmas**: None
  - **Goals (1)**: `(defgoal sdls-tc-auth (forall ((ground spacecraft name) (assumed_auth_key skey) (frame_data tc) (old_arsn seq_n) (z1 eve strd)) (implies (and (strand ground z1 2 (ground ground) (spacecraft spacecraft) (old_arsn old_arsn) (frame_data frame_data) (assumed_auth_key assumed_auth_key)) (pnon assumed_auth_key) (ugen old_arsn) (uniq frame_data) (listener eve frame_data)) (false))) (comment "Confidentiality Goal: Adversary cannot learn telecommand"))`
  - **Skeletons (2)**: Skeleton 1 (`sdls-tc-auth`): `(vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (frame_data tc) (ground spacecraft name))`, `(defstrandmax ground (old_arsn old_arsn) (assumed_auth_key assumed_auth_key) (frame_data frame_data) (spacecraft spacecraft))`, `(pen-non-orig assumed_auth_key)`, `(uniq-gen old_arsn)` | Skeleton 2 (`sdls-tc-auth`): `(vars (header text) (assumed_auth_key skey) (frame_data tc) (old_arsn seq_n) (ground spacecraft name))`, `(defstrandmax satellite (assumed_auth_key assumed_auth_key) (frame_data frame_data) (old_arsn old_arsn) (spacecraft spacecraft) (ground ground))`, `(pen-non-orig assumed_auth_key)`
  - **Keywords & Predicates Used**: `and`, `defgoal`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `false`, `forall`, `herald`, `implies`, `lang`, `listener`, `pen-non-orig`, `pnon`, `recv`, `send`, `strand`, `trace`, `ugen`, `uniq`, `uniq-gen`, `vars`
- **When to Reference This Example**: Reference this example to see the exact syntax of high-level security goal predicates (`strand`, `pnon`, `ugen`, `uniq`, `listener`) inside `(defgoal ...)` when testing whether an authentication-only protocol leaks `frame_data`.
- **Key S-Expression Excerpt** (lines 1–47):
```scheme
(herald "SDLSP TC Baseline: Authentication Only (AES-CMAC)")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defprotocol sdls-tc-auth basic
  (defrole ground
    (vars (header text) (frame_data tc) (old_arsn seq_n) (assumed_auth_key skey) (ground spacecraft name))
    (trace
      (send
        (cat (sdl_header spacecraft) header (successor old_arsn) frame_data
             (hash (sdl_header spacecraft) header (successor old_arsn) frame_data assumed_auth_key))
      )
      (recv
        (cat (sdl_header ground) (successor (successor old_arsn)) frame_data
             (hash (sdl_header ground) (successor (successor old_arsn)) frame_data assumed_auth_key))
      )
    )
  )
  (defrole satellite
    (vars (header text) (frame_data tc) (old_arsn seq_n) (assumed_auth_key skey) (ground spacecraft name))
    (trace
      (recv
        (cat (sdl_header spacecraft) header (successor old_arsn) frame_data
             (hash (sdl_header spacecraft) header (successor old_arsn) frame_data assumed_auth_key))
      )
      (send
        (cat (sdl_header ground) (successor (successor old_arsn)) frame_data
             (hash (sdl_header ground) (successor (successor old_arsn)) frame_data assumed_auth_key))
      )
    )
  )
  (lang (seq_n atom) (tc atom) (successor hash))
)

(defgoal sdls-tc-auth
  (forall ((ground spacecraft name) (assumed_auth_key skey) (frame_data tc) (old_arsn seq_n) (z1 eve strd))
    (implies
      (and
        (strand ground z1 2 (ground ground) (spacecraft spacecraft) (old_arsn old_arsn) (frame_data frame_data) (assumed_auth_key assumed_auth_key))
        (pnon assumed_auth_key)
        (ugen old_arsn)
        (uniq frame_data)
        (listener eve frame_data)
      )
      (false)))
  (comment "Confidentiality Goal: Adversary cannot learn telecommand")
)
```

## sdls-enc-logic.scm

- **File Path**: `03_examples_scm/sdls-enc-logic.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP Encryption")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-enc`. Models CCSDS SDLS Encryption-Only mode (`sdls-enc`) where `ground` and `satellite` exchange `(cat (sdl_header ...) (enc frame_data assumed_enc_key))` without a MAC or sequence number, using `(defstrandmax ground ...)` and `(defstrandmax satellite ...)` in the skeletons (with commented-out `defgoal` examples at the bottom).
- **Roles & Variables**:
  - Role `ground`: Vars: `(frame_data text)`, `(assumed_enc_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) (enc frame_data assumed_enc_key)))` -> `(recv (cat (sdl_header ground) (enc frame_data assumed_enc_key)))`
  - Role `satellite`: Vars: `(frame_data text)`, `(assumed_enc_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) (enc frame_data assumed_enc_key)))` -> `(send (cat (sdl_header ground) (enc frame_data assumed_enc_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (1)**: `(sdl_header dest)`
  - **Rules & Lemmas**: None
  - **Goals**: None active (contains `;`-commented `(defgoal ...)` templates at the bottom of the file)
  - **Skeletons (2)**: Skeleton 1 (`sdls-enc`): `(vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))`, `(defstrandmax ground (frame_data frame_data) (assumed_enc_key assumed_enc_key) (spacecraft spacecraft) (ground ground))`, `(non-orig assumed_enc_key)` | Skeleton 2 (`sdls-enc`): `(vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))`, `(defstrandmax satellite (frame_data frame_data) (assumed_enc_key assumed_enc_key) (ground ground) (spacecraft spacecraft))`, `(uniq-orig frame_data)`, `(non-orig assumed_enc_key)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling basic symmetric payload encryption framing with header macros (`(defmacro (sdl_header dest) ...)`) and `(defstrandmax ...)` skeletons.
- **Key S-Expression Excerpt** (lines 1–35):
```scheme
(herald "SDLSP Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defprotocol sdls-enc basic
  ;; Ground station sends an encrypted SDLS frame
  (defrole ground
    (vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))
    (trace
      (send (cat (sdl_header spacecraft) (enc frame_data assumed_enc_key)))
      (recv (cat (sdl_header ground) (enc frame_data assumed_enc_key)))))
  ;; Satellite receives the encrypted SDLS frame

  (defrole satellite
    (vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))
    (trace
      (recv (cat (sdl_header spacecraft) (enc frame_data assumed_enc_key)))
      (send (cat (sdl_header ground) (enc frame_data assumed_enc_key)))))
)

;; Ground-station point of view
(defskeleton sdls-enc
  (vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))
  (defstrandmax ground (frame_data frame_data) (assumed_enc_key assumed_enc_key) (spacecraft spacecraft) (ground ground))

  (non-orig assumed_enc_key))

;;Satellite point of view
(defskeleton sdls-enc
  (vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))
  (defstrandmax satellite (frame_data frame_data) (assumed_enc_key assumed_enc_key) (ground ground) (spacecraft spacecraft))
  (uniq-orig frame_data)

  (non-orig assumed_enc_key))

```

## sdls-ep-challenge-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-challenge-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Verification: Authentication Only")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-ep-key-verification-auth`. Models the standalone CCSDS SDLS-EP Key Verification challenge-response procedure in Authentication-Only mode (`sdls-ep-key-verification-auth`), where `ground` sends a signed/MACed challenge `(keyver_cmd keyid1 chal)` at `(successor old_arsn)` and `satellite` replies with `(keyver_reply keyid1 chal sessionkey1)` (containing `(enc chal sessionkey1)`) at `(successor (successor old_arsn))`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(old_arsn seq_n)`, `(assumed_auth_key skey)`, `(ground spacecraft name)`, `(keyid1 keyid)`, `(sessionkey1 skey)`, `(chal text)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) (hash (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) (hash (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))`
  - Role `satellite`: Vars: `(header text)`, `(old_arsn seq_n)`, `(assumed_auth_key skey)`, `(ground spacecraft name)`, `(keyid1 keyid)`, `(sessionkey1 skey)`, `(chal text)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) (hash (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) (hash (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (3)**: `(sdl_header dest)`, `(keyver_cmd keyid chal)`, `(keyver_reply keyid chal sessionkey)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (successor hash) (keyid atom))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-ep-key-verification-auth`): `(vars (assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid))`, `(defstrandmax satellite (assumed_auth_key assumed_auth_key) (sessionkey1 sessionkey1) (keyid1 keyid1) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_auth_key)`, `(pen-non-orig sessionkey1)` | Skeleton 2 (`sdls-ep-key-verification-auth`): `(vars (assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid) (chal text) (old_arsn seq_n))`, `(defstrandmax ground (assumed_auth_key assumed_auth_key) (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal) (ground ground) (spacecraft spacecraft) (old_arsn old_arsn))`, `(non-orig assumed_auth_key)`, `(pen-non-orig sessionkey1)`, `(uniq-orig chal)`, `(uniq-gen old_arsn)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `pen-non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling key-confirmation / challenge-response sub-protocols with sequence-number increments `(successor old_arsn)` and `(pen-non-orig sessionkey1)`.
- **Key S-Expression Excerpt** (lines 1–35):
```scheme
(herald "SDLS-EP Key Verification: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (keyver_cmd keyid chal)
  (cat "ep-pdu" "tag:00-0100-cmd" keyid chal))
(defmacro (keyver_reply keyid chal sessionkey)
  (cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey)))

(defprotocol sdls-ep-key-verification-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (ground spacecraft name)
          (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal)
             (hash (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) assumed_auth_key)))
      (recv (cat (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1)
             (hash (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (ground spacecraft name)
          (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal)
             (hash (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) assumed_auth_key)))
      (send (cat (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1)
             (hash (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom)))

(defskeleton sdls-ep-key-verification-auth
  (vars (assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (sessionkey1 sessionkey1) (keyid1 keyid1)
                          (ground ground) (spacecraft spacecraft))
```

## sdls-ep-challenge-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-challenge-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Verification: Authenticated Encryption")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-ep-key-verification-auth-enc`. Models the standalone CCSDS SDLS-EP Key Verification challenge-response procedure in Authenticated Encryption mode (`sdls-ep-key-verification-auth-enc`), where the key verification command and reply PDUs are both encrypted under `assumed_enc_key` and MACed under `assumed_auth_key`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(old_arsn seq_n)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)`, `(keyid1 keyid)`, `(sessionkey1 skey)`, `(chal text)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) (hash (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite`: Vars: `(header text)`, `(old_arsn seq_n)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)`, `(keyid1 keyid)`, `(sessionkey1 skey)`, `(chal text)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) (hash (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (3)**: `(sdl_header dest)`, `(keyver_cmd keyid chal)`, `(keyver_reply keyid chal sessionkey)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (successor hash) (keyid atom))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-ep-key-verification-auth-enc`): `(vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid))`, `(defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (sessionkey1 sessionkey1) (keyid1 keyid1) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_enc_key assumed_auth_key)`, `(pen-non-orig sessionkey1)` | Skeleton 2 (`sdls-ep-key-verification-auth-enc`): `(vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid) (chal text) (old_arsn seq_n))`, `(defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal) (ground ground) (spacecraft spacecraft) (old_arsn old_arsn))`, `(non-orig assumed_enc_key assumed_auth_key)`, `(pen-non-orig sessionkey1)`, `(uniq-orig chal)`, `(uniq-orig old_arsn)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `pen-non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling nested key confirmation inside an already-established authenticated encryption tunnel (`assumed_enc_key` + `assumed_auth_key`).
- **Key S-Expression Excerpt** (lines 1–35):
```scheme
(herald "SDLS-EP Key Verification: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (keyver_cmd keyid chal)
  (cat "ep-pdu" "tag:00-0100-cmd" keyid chal))
(defmacro (keyver_reply keyid chal sessionkey)
  (cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey)))

(defprotocol sdls-ep-key-verification-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (ground spacecraft name)
          (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))
      (recv (cat (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key)
             (hash (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (ground spacecraft name)
          (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))
      (send (cat (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key)
             (hash (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom)))

(defskeleton sdls-ep-key-verification-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (sessionkey1 sessionkey1) (keyid1 keyid1)
```

