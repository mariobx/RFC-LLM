# Official MITRE CPSA Examples Catalog (Part 4: Hackage cpsa-4.4.9 Additional Examples)

This catalog documents the 3 additional official MITRE CPSA `.scm` example files from `cpsa-4.4.9/tst/` (`chan-mesg.scm`, `dev-subatomic-open-closed.scm`, and `devlocn.scm`). Every declaration, role, variable sort, trace event, macro, rule, goal, and skeleton is extracted directly from the source `.scm` files.

## chan-mesg.scm

- **File Path**: `03_examples_scm/chan-mesg.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Yahalom Protocol Without Forwarding" (bound 15) (comment "Testing channels as arbitrary messages."))` | Flags: `(bound 15)`, `(comment "Testing channels as arbitrary messages.")`
- **Protocol & Purpose**: Models the Yahalom protocol without forwarding while testing CPSA 4.4.9's support for arbitrary compound messages in channel positions. Instead of atomic `chan` variables, trace events use `(cat b c)`, `(cat c a)`, and `(cat c b)` as directional channel terms in `(send <chan-term> <msg>)` and `(recv <chan-term> <msg>)`, and skeletons declare `(auth (cat c b))` and `(conf (cat c b) (cat c a))` so that matching a channel automatically forces agreement on the endpoint names.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (cat c a) (cat a b k n-a n-b))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom`):
    - `vars`: `(b a c name), (n-a n-b text), (k skey), (ch1 ch2 chan)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b c) (cat a b n-a n-b))` -> `(recv (cat c b) (cat a b k))` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey), (ch1 ch2 ch3 chan)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b c) (cat a b n-a n-b))` -> `(send (cat c a) (cat a b k n-a n-b))` -> `(send (cat c b) (cat a b k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `auth`, `bound`, `comment`, `conf`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (8)**:
    - `(defskeleton yahalom (vars (a b c name) (n-b text)) (defstrand resp 4 (a a) (b b) (c c) (n-b n-b)) (auth (cat c b)) (uniq-orig n-b))`
    - `(defskeleton yahalom (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b c name)) (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (c c)) (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (c c) (a a) (b b)) (precedes ((1 2) (0 2))) (uniq-orig k n-b) (auth (cat c b)) (conf (cat c b) (cat c a)))`
    - `(defskeleton yahalom (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b c name)) (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (c c)) (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (c c) (a a) (b b)) (uniq-orig k n-b) (auth (cat c b) (cat b c)) (conf (cat c b) (cat c a)))`
    - `(defskeleton yahalom (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b c name)) (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (c c)) (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (c c) (a a) (b b)) (deflistener k) (uniq-orig k n-b) (auth (cat c b) (cat b c)) (conf (cat c b) (cat c a)))`
    - `(defskeleton yahalom (vars (a b c name) (n-a text) (k skey)) (defstrand init 3 (n-a n-a) (c c) (a a)) (uniq-orig n-a) (auth (cat c a)))`
    - `(defskeleton yahalom (vars (k skey) (n-a n-b text) (a c b c-0 name)) (defstrand init 3 (k k) (n-a n-a) (n-b n-b) (a a) (b b) (c c)) (defstrand serv 2 (k k) (n-a n-a) (n-b n-b) (c c-0) (a a) (b b)) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig k n-a) (auth (cat c a) (cat b c-0)) (conf (cat c-0 a)))`
    - `(defskeleton yahalom (vars (c a b name) (n-a n-b text) (k skey)) (defstrand serv 3 (a a) (b b) (c c)) (auth (cat b c)) (conf (cat c b) (cat c a)))`
    - `(defskeleton yahalom (vars (c a b name) (n-a n-b text) (k skey)) (defstrand serv 3 (k k) (a a) (b b) (c c)) (deflistener k) (auth (cat b c)) (conf (cat c b) (cat c a)))`
- **When to Reference This Example**: Reference this example when modeling point-to-point authenticated or confidential channels parameterized by principal names (`(send (cat a b) msg)`, `(auth (cat a b))`, `(conf (cat a b))`) in CPSA 4.4.9+.
- **Key S-Expression Excerpt**:
```scheme
(herald "Yahalom Protocol Without Forwarding" (bound 15)
	(comment "Testing channels as arbitrary messages."))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey))
    (trace (send (cat a n-a))
	   (recv (cat c a) (cat a b k n-a n-b))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))
    (trace (recv (cat a n-a))
	   (send (cat b c) (cat a b n-a n-b))
	   (recv (cat c b) (cat a b k))
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
    (trace (recv (cat b c) (cat a b n-a n-b))
	   (send (cat c a) (cat a b k n-a n-b))
	   (send (cat c b) (cat a b k)))
    (uniq-orig k))
  (comment "Use (cat x y) as channel from x to y. Matching channel should force matching names."))

;;; How much do we know assuming that the resp had a run with an
;;; authenticated channel ch2?  We also assume the responder's nonce
;;; is freshly chosen.

(defskeleton yahalom
  (vars (a b c name) (n-b text))
  (defstrand resp 4 (a a) (b b) (c c) (n-b n-b))
  (auth (cat c b))
  (uniq-orig n-b))

```

## dev-subatomic-open-closed.scm

- **File Path**: `03_examples_scm/dev-subatomic-open-closed.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald dev-subatomic-open-closed (comment "Version that uses (dev const) pairs for locations"))` | Flags: `(comment "Version that uses (dev const) pairs for locations")`
- **Protocol & Purpose**: Models the stateful `subatomic-open-closed` device access-control protocol in CPSA 4.4.9+ using structured `(cat d "lk")` and `(cat d "ls")` `(dev const)` pairs (where `d` has sort `dev`) in the location position of `(load ...)` and `(stor ...)`. By embedding the device identifier `d` directly into the location term, CPSA automatically associates both state registers with device `d` without needing explicit `(facts (same-dev ls lk))` or `same-dev` rules.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `dev-up` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d dev), (o name), (old old1 mesg), (start-ch chan)` | Role assumptions/annotations: `(auth start-ch)`
    - `trace`: `(recv start-ch (cat "power-up" o k))` -> `(stor (cat d "lk") (dev-key-state o k))` -> `(stor (cat d "ls") (dev-state-closed o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (o name), (start-ch chan)` | Role assumptions/annotations: `(conf start-ch)`
    - `trace`: `(send start-ch (cat "power-up" o k))` -> `(recv (enc "up" k))`
  - Role `owner-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d dev), (o name)` | Role assumptions: none
    - `trace`: `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d dev), (o name)` | Role assumptions: none
    - `trace`: `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d dev), (o name)` | Role assumptions/annotations: `(gen-st (dev-key-state o k) (dev-state-opened o))`
    - `trace`: `(recv (enc "open" d o n k))` -> `(load (cat d "lk") (dev-key-state o k))` -> `(stor (cat d "ls") (dev-state-opened o))` -> `(send n)`
  - Role `dev-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d dev), (o name)` | Role assumptions/annotations: `(gen-st (dev-key-state o k))`
    - `trace`: `(recv (enc "close" d o n k))` -> `(load (cat d "lk") (dev-key-state o k))` -> `(stor (cat d "ls") (dev-state-closed o))` -> `(send n)`
  - Role `dev-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d dev), (o name)` | Role assumptions/annotations: `(uniq-orig n)`, `(gen-st (dev-key-state o k) (dev-state-opened o))`
    - `trace`: `(load (cat d "lk") (dev-key-state o k))` -> `(load (cat d "ls") (dev-state-opened o))` -> `(recv (enc "may I pass" k))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey)` | Role assumptions: none
    - `trace`: `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `=`, `and`, `auth`, `comment`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `facts`, `forall`, `gen-st`, `herald`, `implies`, `load`, `p`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros (6)**: `(dev-key-state o k)` -> `(cat "st-k" o k)`; `(opened o)` -> `(cat o o)`; `(closed o)` -> `o`; `(dev-state-opened o)` -> `(cat "st" (opened o))`; `(dev-state-closed o)` -> `(cat "st" (closed o))`; `(dev-state-any o any)` -> `(cat "st" any)`
  - **Rules & Genrules (1)**:
    - `(defrule power-deliver-once ...)` in `subatomic-open-closed`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (deflistener k) (uniq-orig k) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand dev-pass 4 (k k)) (facts (no-state-split) (useLocName)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (defstrand dev-pass 4 (k k)) (uniq-orig k) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand dev-pass 4 (k k)) (facts (no-state-split)))`
- **When to Reference This Example**: Reference this example when modeling multi-register stateful devices in CPSA 4.4.9+ using `(vars (d dev))` and compound location terms `(load (cat d "reg") ...)` / `(stor (cat d "reg") ...)` instead of separate `locn` variables and `same-dev` rules.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol subatomic-open-closed basic
  (defrole dev-up
    (vars (k skey) (d dev) (o name) (old old1 mesg) (start-ch chan))
    (trace
     (recv start-ch (cat "power-up" o k))
     (stor (cat d "lk") (dev-key-state o k))
     (stor (cat d "ls") (dev-state-closed o))
     (send (enc "up" k)))
    (auth start-ch)
    )

  (defrole owner-power-dev
    (vars (k skey) (o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d dev) (o name))
    (trace
     (send (enc "open" d o n k))
     (recv n)))

  (defrole owner-close
    (vars (k skey) (n text) (d dev) (o name))
    (trace
     (send (enc "close" d o n k))
     (recv n)))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d dev) (o name))
    (trace
     (recv (enc "open" d o n k))
     (load (cat d "lk") (dev-key-state o k))
     (stor (cat d "ls") (dev-state-opened o))
     (send n))
    (gen-st (dev-key-state o k) (dev-state-opened o))
    )
```

## devlocn.scm

- **File Path**: `03_examples_scm/devlocn.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Dev and Locn" (comment "This tests the feature that allows loads and stors to have any message in their location position."))` | Flags: `(comment "This tests the feature that allows loads and stors to have any message in their location position.")`
- **Protocol & Purpose**: Tests CPSA 4.4.9's generalized location terms across three `devlocn` protocol definitions: (1) storing and loading at `(cat d l1)` / `(cat d l2)` where `d` is `dev` and `l1, l2` are `locn`; (2) testing state isolation across skeletons with `(facts (neq d1 d2))` vs. `(facts (neq l1 l2))`; and (3) loading from a generic `mesg` variable `dl` (`(load dl m)`) after acquiring `dl` in `(recv (enc dl k))`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `devlocn` (definition 1)):
    - `vars`: `(d dev), (l1 l2 locn), (n1 n2 data), (k skey)` | Role assumptions/annotations: `(uniq-orig n1 n2 d)`
    - `trace`: `(stor (cat d l1) n1)` -> `(stor (cat d l2) n2)` -> `(send (enc d l1 k))` -> `(send (enc d l2 k))`
  - Role `resp` (in `devlocn` (definition 1)):
    - `vars`: `(d dev), (l locn), (m mesg), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc d l k))` -> `(load (cat d l) m)` -> `(send m)`
  - Role `init` (in `devlocn` (definition 2)):
    - `vars`: `(d dev), (l1 l2 locn), (n1 n2 data), (k skey)` | Role assumptions/annotations: `(uniq-orig n1 l1)`
    - `trace`: `(stor (cat d l1) n1)` -> `(send (enc d l1 k))`
  - Role `resp` (in `devlocn` (definition 2)):
    - `vars`: `(d dev), (l locn), (m mesg), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc d l k))` -> `(load (cat d l) m)` -> `(send m)`
  - Role `init` (in `devlocn` (definition 3)):
    - `vars`: `(d dev), (l1 l2 locn), (n1 n2 data), (k skey)` | Role assumptions/annotations: `(uniq-orig n1 l1)`
    - `trace`: `(stor (cat d l1) n1)` -> `(send (enc d l1 k))`
  - Role `resp` (in `devlocn` (definition 3)):
    - `vars`: `(d dev), (l locn), (dl m mesg), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc dl k))` -> `(load dl m)` -> `(send m)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `facts`, `gen-st`, `herald`, `load`, `neq`, `non-orig`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (8)**:
    - `(defskeleton devlocn (vars (n1 n2 data)) (defstrand init 2 (n1 n1) (n2 n2)) (deflistener n1) (deflistener n2))`
    - `(defskeleton devlocn (vars (n1 n2 data)) (defstrand init 1 (n1 n1)) (defstrand init 1 (n1 n2)) (deflistener n1) (deflistener n2))`
    - `(defskeleton devlocn (vars (n1 n2 data) (d1 d2 dev)) (defstrand init 1 (n1 n1) (d d1)) (defstrand init 1 (n1 n2) (d d2)) (deflistener n1) (deflistener n2) (facts (neq d1 d2)) (comment "With different devices they cannot have the same source."))`
    - `(defskeleton devlocn (vars (n1 n2 data) (l1 l2 locn)) (defstrand init 1 (n1 n1) (l1 l1)) (defstrand init 1 (n1 n2) (l1 l2)) (deflistener n1) (deflistener n2) (facts (neq l1 l2)) (comment "With different locns they cannot have the same source."))`
    - `(defskeleton devlocn (vars (n1 n2 data) (l1 l2 locn) (d dev)) (defstrand init 1 (n1 n1) (l1 l1) (d d)) (defstrand init 1 (n1 n2) (l1 l2) (d d)) (deflistener n1) (deflistener n2) (facts (neq l1 l2)) (comment "With different locns they cannot have the same source even if the devs are the same."))`
    - `(defskeleton devlocn (vars (m mesg)) (defstrand resp 2 (m m)) (gen-st m))`
    - `(defskeleton devlocn (vars (m mesg)) (defstrand resp 2 (m m)) (comment "Possibly strange interpretation. Init has uniq-orig n1 and l1. Resp doesn't necessarily retrieve n1, even though nobody but Init should know l1, so nobody else could stor into it."))`
    - `(defskeleton devlocn (vars (n data)) (defstrand resp 2 (m n)) (defstrand init 2 (n1 n)) (comment "Even if loaded value is not gen-st, since it's uniq-orig, nonce-test still applies."))`
- **When to Reference This Example**: Reference this example when using compound `(cat d l)` or dynamically received `mesg` variables in the location slot of `(load <locn-mesg> <val>)` and `(stor <locn-mesg> <val>)`, or when reasoning about `dev` and `locn` inequality facts.
- **Key S-Expression Excerpt**:
```scheme
(herald "Dev and Locn" 
  (comment "This tests the feature that allows loads and stors to have any message in their location position."))

(defprotocol devlocn basic
  (defrole init
    (vars (d dev) (l1 l2 locn) (n1 n2 data) (k skey))
    (trace
     (stor (cat d l1) n1)
     (stor (cat d l2) n2)
     (send (enc d l1 k))
     (send (enc d l2 k)))
    (uniq-orig n1 n2 d))
  (defrole resp
    (vars (d dev) (l locn) (m mesg) (k skey))
    (trace
     (recv (enc d l k))
     (load (cat d l) m)
     (send m))
    (non-orig k))) 

(defskeleton devlocn
  (vars (n1 n2 data))
  (defstrand init 2 (n1 n1) (n2 n2))
  (deflistener n1)
  (deflistener n2))

(defprotocol devlocn basic
  (defrole init
    (vars (d dev) (l1 l2 locn) (n1 n2 data) (k skey))
    (trace
     (stor (cat d l1) n1)
     (send (enc d l1 k)))
    (uniq-orig n1 l1))
  (defrole resp
    (vars (d dev) (l locn) (m mesg) (k skey))
```

