# Official MITRE CPSA Examples Catalog (Part 3: sdls-ep-challenge.scm to yes-or-no.scm)

This catalog documents the 48 official MITRE CPSA `.scm` example files in alphabetical slice `[100:148]` (`sdls-ep-challenge.scm` through `yes-or-no.scm`). Every declaration, role, variable sort, trace event, macro, rule, goal, and skeleton is extracted directly from the source `.scm` files.

## sdls-ep-challenge.scm

- **File Path**: `03_examples_scm/sdls-ep-challenge.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Verification")` | Flags: none | Custom `lang`: `(lang (keyid atom))`
- **Protocol & Purpose**: Models the Space Data Link Security Extended Procedures (SDLS-EP) Key Verification procedure (Command PDU Figure 5-7 p.5-10 and Reply PDU Figure 5-8 p.5-11, Recipient steps 3.2.3.5.3.4 and .3.5 p.3-12). The ground station sends a challenge `chal` paired with a custom-sorted key identifier `keyid1`, and the satellite replies with `chal` encrypted under `sessionkey1`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-key-verification`):
    - `vars`: `(keyid1 keyid), (sessionkey1 skey), (chal text)` | Role assumptions: none
    - `trace`: `(send (keyver_cmd keyid1 chal))` -> `(recv (keyver_reply keyid1 chal sessionkey1))`
  - Role `satellite` (in `sdls-ep-key-verification`):
    - `vars`: `(keyid1 keyid), (sessionkey1 skey), (chal text)` | Role assumptions: none
    - `trace`: `(recv (keyver_cmd keyid1 chal))` -> `(send (keyver_reply keyid1 chal sessionkey1))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `pen-non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(keyver_cmd keyid chal)` -> `(cat "ep-pdu" "tag:00-0100-cmd" keyid chal)`; `(keyver_reply keyid chal sessionkey)` -> `(cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-key-verification (vars (sessionkey1 skey) (keyid1 keyid) (chal text)) (defstrandmax ground (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal)) (pen-non-orig sessionkey1) (uniq-orig chal) (comment "Initiator's view"))`
    - `(defskeleton sdls-ep-key-verification (vars (sessionkey1 skey) (keyid1 keyid)) (defstrandmax satellite (sessionkey1 sessionkey1) (keyid1 keyid1)) (pen-non-orig sessionkey1) (comment "Recipient's view of Key Verification"))`
- **When to Reference This Example**: Reference this example when modeling challenge-response key verification PDUs using `(defmacro ...)` for packet tags, custom atomic sorts via `(lang (keyid atom))`, and `(pen-non-orig ...)` for symmetric session keys.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Key Verification")

;; Key Verification Command PDU, Figure 5-7 p.5-10..
(defmacro (keyver_cmd keyid chal)
  (cat "ep-pdu" "tag:00-0100-cmd" keyid chal))

;; Key Verification Reply PDU, Figure 5-8 p.5-11.
(defmacro (keyver_reply keyid chal sessionkey)
  (cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey)))

(defprotocol sdls-ep-key-verification basic
  (defrole ground
    (vars (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (send (keyver_cmd keyid1 chal))
      (recv (keyver_reply keyid1 chal sessionkey1))))

  ;; Recipient.  3.2.3.5.3.4 and .3.5, p.3-12
  (defrole satellite
    (vars (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (recv (keyver_cmd keyid1 chal))
      (send (keyver_reply keyid1 chal sessionkey1))))

  (lang (keyid atom))
)

;pov skeletons
(defskeleton sdls-ep-key-verification
  (vars (sessionkey1 skey) (keyid1 keyid) (chal text))
  (defstrandmax ground (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal))
  (pen-non-orig sessionkey1)
  (uniq-orig chal)
  (comment "Initiator's view"))

```

## sdls-ep-key-activation-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-key-activation-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Activation: Authentication Only")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (keyid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Key Activation command with Authentication Only protection. The `ground` role sends a frame containing the Space Data Link header (`sdl_header`), sequence number `(successor old_arsn)`, Key Activation PDU (`key_activation_pdu`), and a keyed MAC modeled as `(hash ... assumed_auth_key)` to `satellite`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-key-activation-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (keyid1 keyid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) (hash (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-key-activation-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (keyid1 keyid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) (hash (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len")`; `(key_activation_pdu keyid)` -> `(cat "ep-pdu" "tag:00-0010" keyid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-key-activation-auth (vars (assumed_auth_key skey) (spacecraft name) (keyid1 keyid)) (defstrandmax satellite (assumed_auth_key assumed_auth_key) (keyid1 keyid1) (spacecraft spacecraft)) (non-orig assumed_auth_key) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-key-activation-auth (vars (assumed_auth_key skey) (spacecraft name) (keyid1 keyid) (old_arsn seq_n)) (defstrandmax ground (assumed_auth_key assumed_auth_key) (keyid1 keyid1) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_auth_key) (uniq-gen old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling authenticated unencrypted command frames with anti-replay sequence numbers (`(lang (seq_n atom) (successor hash) (keyid atom))`) and keyed hash MACs.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Key Activation: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (key_activation_pdu keyid)
  (cat "ep-pdu" "tag:00-0010" keyid))

(defprotocol sdls-ep-key-activation-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (keyid1 keyid))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1)
             (hash (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (keyid1 keyid))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1)
             (hash (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom)))

(defskeleton sdls-ep-key-activation-auth
  (vars (assumed_auth_key skey) (spacecraft name) (keyid1 keyid))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (keyid1 keyid1)
                          (spacecraft spacecraft))
  (non-orig assumed_auth_key)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-key-activation-auth
  (vars (assumed_auth_key skey) (spacecraft name) (keyid1 keyid) (old_arsn seq_n))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
```

## sdls-ep-key-activation-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-key-activation-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Activation: Authenticated Encryption")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (keyid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Key Activation command under Authenticated Encryption (Encrypt-then-MAC). The Key Activation PDU is encrypted under `assumed_enc_key`, concatenated with the SDL header and sequence number `old_arsn`, and authenticated with a keyed hash using `assumed_auth_key`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-key-activation-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (keyid1 keyid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-key-activation-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (keyid1 keyid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number")`; `(key_activation_pdu keyid)` -> `(cat "ep-pdu" "tag:00-0010" keyid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-key-activation-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keyid1 keyid)) (defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keyid1 keyid1) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-key-activation-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keyid1 keyid) (old_arsn seq_n)) (defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keyid1 keyid1) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_enc_key assumed_auth_key) (uniq-orig old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling Encrypt-then-MAC authenticated encryption framing with separate encryption and authentication symmetric keys (`assumed_enc_key`, `assumed_auth_key`).
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Key Activation: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (key_activation_pdu keyid)
  (cat "ep-pdu" "tag:00-0010" keyid))

(defprotocol sdls-ep-key-activation-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (keyid1 keyid))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (keyid1 keyid))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom)))

(defskeleton sdls-ep-key-activation-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keyid1 keyid))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (keyid1 keyid1)
                          (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-key-activation-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keyid1 keyid) (old_arsn seq_n))
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
```

## sdls-ep-key-activation.scm

- **File Path**: `03_examples_scm/sdls-ep-key-activation.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Activation")` | Flags: none | Custom `lang`: `(lang (keyid atom))`
- **Protocol & Purpose**: Models the bare SDLS-EP Key Activation Command PDU without link-layer framing or cryptographic wrapping. As noted in the comments, key database state (5.4.1.2 p.5-5) is not modeled and no reply PDU exists for Key Activation (5.4.2.2.1, p.5-7).
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-key-activation`):
    - `vars`: `(keyid1 keyid)` | Role assumptions: none
    - `trace`: `(send (key_activation_pdu keyid1))`
  - Role `satellite` (in `sdls-ep-key-activation`):
    - `vars`: `(keyid1 keyid)` | Role assumptions: none
    - `trace`: `(recv (key_activation_pdu keyid1))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `recv`, `send`, `trace`, `vars`
  - **Macros (1)**: `(key_activation_pdu keyid)` -> `(cat "ep-pdu" "tag:00-0010" keyid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-key-activation (vars (keyid1 keyid)) (defstrandmax satellite (keyid1 keyid1)) (comment "Recipient's view"))`
    - `(defskeleton sdls-ep-key-activation (vars (keyid1 keyid)) (defstrandmax ground (keyid1 keyid1)) (comment "Initiator's view"))`
- **When to Reference This Example**: Reference this example as a minimal baseline for one-way unauthenticated command PDUs using `(defmacro ...)` and `(lang (keyid atom))`.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Key Activation")
;; Key Activation Command PDU
(defmacro (key_activation_pdu keyid)
  (cat "ep-pdu" "tag:00-0010" keyid))
;; Key database state (5.4.1.2 p.5-5) is not modelled and assumed

(defprotocol sdls-ep-key-activation basic
  (defrole ground
    (vars (keyid1 keyid))
    (trace
      (send (key_activation_pdu keyid1))))
  (defrole satellite
    (vars (keyid1 keyid))
    (trace
      (recv (key_activation_pdu keyid1))))
  (lang (keyid atom))
  (comment "No reply PDU exists for Key Activation -- 5.4.2.2.1, p.5-7."))


;pov skeletons
(defskeleton sdls-ep-key-activation
  (vars (keyid1 keyid))
  (defstrandmax satellite (keyid1 keyid1))
  (comment "Recipient's view"))
(defskeleton sdls-ep-key-activation
  (vars (keyid1 keyid))
  (defstrandmax ground (keyid1 keyid1))
  (comment "Initiator's view"))
```

## sdls-ep-otar-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-otar-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP OTAR: Authentication Only")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (keyid atom) (keyid_of hash))`
- **Protocol & Purpose**: Models SDLS-EP Over-the-Air Rekeying (OTAR) with Authentication Only link protection. The OTAR payload encrypts a block of new session keys and their key IDs (`keyid1`, `sessionkey1`, `keyid2`, `sessionkey2`) under `keymaster` (identified by `(keyid_of keymaster)`), while the outer frame is authenticated with `assumed_auth_key` and sequence number `(successor old_arsn)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-otar-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-otar-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros (4)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len")`; `(otar_pdu masterkeyid uploadblock)` -> `(cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock)`; `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)` -> `(cat keyid1 sessionkey1 keyid2 sessionkey2)`; `(otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)` -> `(otar_pdu (keyid_of keymaster) (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-otar-auth (vars (assumed_auth_key skey) (spacecraft name) (keymaster skey)) (defstrandmax satellite (assumed_auth_key assumed_auth_key) (keymaster keymaster) (spacecraft spacecraft)) (non-orig assumed_auth_key keymaster) (non-orig keymaster) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-otar-auth (vars (assumed_auth_key skey) (spacecraft name) (keymaster sessionkey1 sessionkey2 skey) (old_arsn seq_n)) (defstrandmax ground (assumed_auth_key assumed_auth_key) (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_auth_key keymaster) (uniq-orig sessionkey1 sessionkey2) (non-orig keymaster) (uniq-gen old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling key transport / over-the-air rekeying where a master key wraps multiple session keys inside an outer MAC-authenticated frame and key identifiers are functionally bound to keys via `(lang ... (keyid_of hash))`.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP OTAR: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))
(defmacro (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
  (cat keyid1 sessionkey1 keyid2 sessionkey2))
(defmacro (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
  (otar_pdu (keyid_of keymaster)
    (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))

(defprotocol sdls-ep-otar-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
             (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
             (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom) (keyid_of hash)))

(defskeleton sdls-ep-otar-auth
  (vars (assumed_auth_key skey) (spacecraft name) (keymaster skey))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (keymaster keymaster)
                          (spacecraft spacecraft))
  (non-orig assumed_auth_key keymaster)
```

## sdls-ep-otar-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-otar-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP OTAR: Authenticated Encryption")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (keyid atom) (keyid_of hash))`
- **Protocol & Purpose**: Models SDLS-EP Over-the-Air Rekeying (OTAR) with Authenticated Encryption link protection. The OTAR payload (which itself encrypts `keyid1`, `sessionkey1`, `keyid2`, `sessionkey2` under `keymaster`) is nested inside an outer link-layer encryption under `assumed_enc_key` and authenticated with `assumed_auth_key`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-otar-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-otar-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (4)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number")`; `(otar_pdu masterkeyid uploadblock)` -> `(cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock)`; `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)` -> `(cat keyid1 sessionkey1 keyid2 sessionkey2)`; `(otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)` -> `(otar_pdu (keyid_of keymaster) (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-otar-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keymaster skey)) (defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keymaster keymaster) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key keymaster) (non-orig keymaster) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-otar-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keymaster sessionkey1 sessionkey2 skey) (old_arsn seq_n)) (defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_enc_key assumed_auth_key keymaster) (uniq-orig sessionkey1 sessionkey2) (non-orig keymaster) (uniq-orig old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling nested key-wrapping inside an Encrypt-then-MAC link layer with functional key-ID binding `(keyid_of keymaster)`.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP OTAR: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))
(defmacro (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
  (cat keyid1 sessionkey1 keyid2 sessionkey2))
(defmacro (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
  (otar_pdu (keyid_of keymaster)
    (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))

(defprotocol sdls-ep-otar-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom) (keyid_of hash)))

(defskeleton sdls-ep-otar-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keymaster skey))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (keymaster keymaster)
                          (spacecraft spacecraft))
```

## sdls-ep-otar-transmission.scm

- **File Path**: `03_examples_scm/sdls-ep-otar-transmission.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Over-the-Air Rekeying (OTAR)")` | Flags: none | Custom `lang`: `(lang (keyid atom) (keyid_of hash))`
- **Protocol & Purpose**: Models the standalone SDLS-EP Over-the-Air Rekeying (OTAR) command PDU (Figure 5-3 p.5-6; Initiator steps 3.2.3.1.3.2–.3, Recipient step 3.2.3.1.3.4) without outer link-layer framing. The ground station sends `(keyid_of keymaster)` and the encrypted key upload block `(enc (otar_upload_block ...) keymaster)` to the satellite.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-otar`):
    - `vars`: `(keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(send (otar_pdu (keyid_of keymaster) (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))`
  - Role `satellite` (in `sdls-ep-otar`):
    - `vars`: `(keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(recv (otar_pdu (keyid_of keymaster) (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(otar_pdu masterkeyid uploadblock)` -> `(cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock)`; `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)` -> `(cat keyid1 sessionkey1 keyid2 sessionkey2)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-otar (vars (keymaster skey)) (defstrandmax satellite (keymaster keymaster)) (non-orig keymaster) (comment "Recipient's view of OTAR"))`
    - `(defskeleton sdls-ep-otar (vars (keymaster sessionkey1 sessionkey2 skey)) (defstrandmax ground (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2)) (non-orig keymaster) (uniq-orig sessionkey1 sessionkey2) (comment "Initiator's view of OTAR"))`
- **When to Reference This Example**: Reference this example when modeling standalone key-upload PDUs where key identifiers sit inside the encrypted payload and a functional hash `(keyid_of hash)` maps keys to their public identifiers.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Over-the-Air Rekeying (OTAR)")
;; OTAR command PDU, Figure 5-3 p.5-6:
;;   tag 00,0001 | length | Master Key ID | IV | { EncKeyID, EncKey } x N | MAC


(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))


(defmacro (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
  (cat keyid1 sessionkey1 keyid2 sessionkey2))

(defprotocol sdls-ep-otar basic
  ;; Initiator.  Steps 3.2.3.1.3.2 and 3.2.3.1.3.3, pp.3-4..3-5
  (defrole ground
    (vars (keymaster sessionkey1 sessionkey2 skey)
          (keyid1 keyid2 keyid))
    (trace
      ;; Key IDs sit in the enc, per 5.4.2.1.2.5 p.5-6.
      (send (otar_pdu (keyid_of keymaster)
              (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
                   keymaster)))))
  ;; Recipient.  Step 3.2.3.1.3.4, p.3-5

  (defrole satellite
    (vars (keymaster sessionkey1 sessionkey2 skey)
          (keyid1 keyid2 keyid))
    (trace
      (recv (otar_pdu (keyid_of keymaster)
              (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
                   keymaster)))))
  (lang (keyid atom)  (keyid_of hash))
  (comment "No reply PDU exists for OTAR (5.4.2.1.1, p.5-5.)"))


```

## sdls-ep-sa-rekey-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-rekey-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Rekey SA: Authentication Only")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (spi atom) (keyid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Rekey Security Association (SA) command with Authentication Only link protection. The `ground` station sends a frame containing the SDL header, `(successor old_arsn)`, the Rekey SA PDU (`spi`, `enckeyid`, `authkeyid`, `new_arsn`, `iv`), and a keyed hash under `assumed_auth_key`, with `(facts (neq old_arsn new_arsn))` distinguishing the old and new anti-replay sequence numbers.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-rekey-sa-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) (hash (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-rekey-sa-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) (hash (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `facts`, `herald`, `lang`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len")`; `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)` -> `(cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-rekey-sa-auth (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n)) (defstrandmax satellite (assumed_auth_key assumed_auth_key) (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn) (old_arsn old_arsn) (spacecraft spacecraft)) (non-orig assumed_auth_key) (facts (neq old_arsn new_arsn)) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-rekey-sa-auth (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n)) (defstrandmax ground (assumed_auth_key assumed_auth_key) (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn) (old_arsn old_arsn) (spacecraft spacecraft)) (non-orig assumed_auth_key) (uniq-orig new_arsn) (facts (neq old_arsn new_arsn)) (uniq-gen old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling SA rekeying commands with multiple custom atomic sorts (`seq_n`, `spi`, `keyid`) and inequality facts `(facts (neq old_arsn new_arsn))` in skeletons.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Rekey SA: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
  (cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv))

(defprotocol sdls-ep-rekey-sa-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
             (hash (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
             (hash (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (spi atom) (keyid atom)))

(defskeleton sdls-ep-rekey-sa-auth
  (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (spi spi) (enckeyid enckeyid)
                          (authkeyid authkeyid) (new_arsn new_arsn)
                          (old_arsn old_arsn)
                          (spacecraft spacecraft))
  (non-orig assumed_auth_key)
  (facts (neq old_arsn new_arsn))
  (comment "Satellite point of view"))

```

## sdls-ep-sa-rekey-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-rekey-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Rekey SA: Authenticated Encryption")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (spi atom) (keyid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Rekey SA command under Authenticated Encryption. The Rekey SA PDU (`spi`, `enckeyid`, `authkeyid`, `new_arsn`, `iv`) is encrypted under `assumed_enc_key` and MAC-authenticated under `assumed_auth_key`, with `(facts (neq old_arsn new_arsn))` enforced in the skeletons.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-rekey-sa-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-rekey-sa-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `facts`, `herald`, `lang`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number")`; `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)` -> `(cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-rekey-sa-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n)) (defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn) (old_arsn old_arsn) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key) (facts (neq old_arsn new_arsn)) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-rekey-sa-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n)) (defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn) (old_arsn old_arsn) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key) (uniq-orig new_arsn) (facts (neq old_arsn new_arsn)) (uniq-orig old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling encrypted and authenticated SA rekeying frames that update sequence numbers and IVs while enforcing `(facts (neq old_arsn new_arsn))`.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Rekey SA: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
  (cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv))

(defprotocol sdls-ep-rekey-sa-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (spi atom) (keyid atom)))

(defskeleton sdls-ep-rekey-sa-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (spi spi) (enckeyid enckeyid)
                          (authkeyid authkeyid) (new_arsn new_arsn)
                          (old_arsn old_arsn)
                          (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (facts (neq old_arsn new_arsn))
  (comment "Satellite point of view"))
```

## sdls-ep-sa-rekey.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-rekey.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Rekey SA")` | Flags: none | Custom `lang`: `(lang (spi atom) (keyid atom) (seq_n atom))`
- **Protocol & Purpose**: Models the bare SDLS-EP Rekey SA PDU (Figure 5-14 p.5-16, field order per 5.5.1.4.2.2, Initiator 3.3.3.3.3.2–.3, Recipient 3.3.3.3.3.4) without outer link framing. Transmits `spi`, `enckeyid`, `authkeyid`, `new_arsn`, and `iv` in cleartext.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-rekey-sa`):
    - `vars`: `(spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(send (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv))`
  - Role `satellite` (in `sdls-ep-rekey-sa`):
    - `vars`: `(spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(recv (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (1)**: `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)` -> `(cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-rekey-sa (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n)) (defstrandmax satellite (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn)) (comment "Recipient's view"))`
    - `(defskeleton sdls-ep-rekey-sa (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n)) (defstrandmax ground (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn)) (uniq-orig new_arsn) (comment "Initiator's view."))`
- **When to Reference This Example**: Reference this example when defining custom protocol field sorts (`(lang (spi atom) (keyid atom) (seq_n atom))`) for unframed security association management PDUs.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Rekey SA")


;; Rekey SA PDU, Figure 5-14 p.5-16
;; Field order per 5.5.1.4.2.2
(defmacro (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
  (cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv))

(defprotocol sdls-ep-rekey-sa basic
  ;; Initiator  3.3.3.3.3.2 then 3.3.3.3.3.3, pp.3-21..3-22.
  ;; Initiator transitions its own SA to Keyed before signalling.
  (defrole ground
    (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (send (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv))))
  ;; Recipient.  3.3.3.3.3.4, p.3-22.
  (defrole satellite
    (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (recv (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv))))
  (lang (spi atom) (keyid atom) (seq_n atom))
  (comment "No reply PDU exists for Rekey SA -- 5.5.1.4.1, p.5-15."))

;;; pov
(defskeleton sdls-ep-rekey-sa
  (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n))
  (defstrandmax satellite (spi spi) (enckeyid enckeyid)
                          (authkeyid authkeyid) (new_arsn new_arsn))
  (comment "Recipient's view"))
(defskeleton sdls-ep-rekey-sa
  (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n))
  (defstrandmax ground (spi spi) (enckeyid enckeyid)
                       (authkeyid authkeyid) (new_arsn new_arsn))
  (uniq-orig new_arsn)
  (comment "Initiator's view.")
  )
```

## sdls-ep-sa-start-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-start-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Start SA: Authentication Only")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (spi atom) (gvcid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Start SA command with Authentication Only protection. Sends the Start SA PDU (`spi` and Global Virtual Channel ID `gvcid`) alongside `(successor old_arsn)` and a keyed hash MAC under `assumed_auth_key`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-start-sa-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) (hash (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-start-sa-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) (hash (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len")`; `(start_sa_pdu spi gvcid)` -> `(cat "ep-pdu" "tag:01-1011" spi gvcid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-start-sa-auth (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid)) (defstrandmax satellite (assumed_auth_key assumed_auth_key) (spi spi) (gvcid gvcid) (spacecraft spacecraft)) (non-orig assumed_auth_key) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-start-sa-auth (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid) (old_arsn seq_n)) (defstrandmax ground (assumed_auth_key assumed_auth_key) (spi spi) (gvcid gvcid) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_auth_key) (uniq-gen old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling authenticated SA activation/start commands binding a Security Parameter Index (`spi`) to a channel identifier (`gvcid`).
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Start SA: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (start_sa_pdu spi gvcid)
  (cat "ep-pdu" "tag:01-1011" spi gvcid))

(defprotocol sdls-ep-start-sa-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (spi spi) (gvcid gvcid))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid)
             (hash (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (spi spi) (gvcid gvcid))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid)
             (hash (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (spi atom) (gvcid atom)))

(defskeleton sdls-ep-start-sa-auth
  (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (spi spi) (gvcid gvcid)
                          (spacecraft spacecraft))
  (non-orig assumed_auth_key)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-start-sa-auth
  (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid) (old_arsn seq_n))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
```

## sdls-ep-sa-start-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-start-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Start SA: Authenticated Encryption")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (spi atom) (gvcid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Start SA command with Authenticated Encryption. Encrypts `(start_sa_pdu spi gvcid)` under `assumed_enc_key` and authenticates the frame (including `old_arsn`) with a keyed hash under `assumed_auth_key`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-start-sa-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-start-sa-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number")`; `(start_sa_pdu spi gvcid)` -> `(cat "ep-pdu" "tag:01-1011" spi gvcid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-start-sa-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid)) (defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spi spi) (gvcid gvcid) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-start-sa-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid) (old_arsn seq_n)) (defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spi spi) (gvcid gvcid) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_enc_key assumed_auth_key) (uniq-orig old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling Encrypt-then-MAC SA start commands with custom atomic sorts `spi`, `gvcid`, and `seq_n`.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Start SA: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (start_sa_pdu spi gvcid)
  (cat "ep-pdu" "tag:01-1011" spi gvcid))

(defprotocol sdls-ep-start-sa-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (spi spi) (gvcid gvcid))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (spi spi) (gvcid gvcid))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (spi atom) (gvcid atom)))

(defskeleton sdls-ep-start-sa-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (spi spi) (gvcid gvcid)
                          (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-start-sa-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid) (old_arsn seq_n))
```

## sdls-ep-sa-start.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-start.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Start SA")` | Flags: none | Custom `lang`: `(lang (spi atom) (gvcid atom))`
- **Protocol & Purpose**: Models the bare SDLS-EP Start SA PDU (p.5-14, Tag 01,1011, fields per 5.5.1.2.2.2) with one mandatory `spi` and one `gvcid`, assuming the SA precondition (Keyed state) without link-layer framing.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-start-sa`):
    - `vars`: `(spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(send (start_sa_pdu spi gvcid))`
  - Role `satellite` (in `sdls-ep-start-sa`):
    - `vars`: `(spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(recv (start_sa_pdu spi gvcid))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `recv`, `send`, `trace`, `vars`
  - **Macros (1)**: `(start_sa_pdu spi gvcid)` -> `(cat "ep-pdu" "tag:01-1011" spi gvcid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-start-sa (vars (spi spi) (gvcid gvcid)) (defstrandmax satellite (spi spi) (gvcid gvcid)) (comment "Recipient's view"))`
    - `(defskeleton sdls-ep-start-sa (vars (spi spi) (gvcid gvcid)) (defstrandmax ground (spi spi) (gvcid gvcid)) (comment "Initiator's view"))`
- **When to Reference This Example**: Reference this example as a minimal template for unframed SA management PDUs using custom atomic sorts `(lang (spi atom) (gvcid atom))`.
- **Key S-Expression Excerpt**:
```scheme
(herald "SDLS-EP Start SA")

;; Start SA PDU, p.5-14.  Tag 01,1011.

;; Fields per 5.5.1.2.2.2: SPI (16 bits, mandatory) and one or more

;; GVC/GMAP IDs (32 bits each, mandatory).  One GVCID modelled.
(defmacro (start_sa_pdu spi gvcid)
  (cat "ep-pdu" "tag:01-1011" spi gvcid))

;; The 3.3.3.1.2 precondition -- SA in Keyed state --
;; is assumed rather than checked.
(defprotocol sdls-ep-start-sa basic
  ;; Initiator.  3.3.3.1.3.2 then 3.3.3.1.3.3, pp.3-18..3-19
  (defrole ground
    (vars (spi spi) (gvcid gvcid))
    (trace
      (send (start_sa_pdu spi gvcid))))
  ;; Recipient.  3.3.3.1.3.4, p.3-19.
  (defrole satellite
    (vars (spi spi) (gvcid gvcid))
    (trace
      (recv (start_sa_pdu spi gvcid))))
  (lang (spi atom) (gvcid atom))
  (comment "No reply PDU exists for Start SA -- 5.5.1.2.1, p.5-14."))


;;; pov.
(defskeleton sdls-ep-start-sa
  (vars (spi spi) (gvcid gvcid))
  (defstrandmax satellite (spi spi) (gvcid gvcid))
  (comment "Recipient's view"))
(defskeleton sdls-ep-start-sa
  (vars (spi spi) (gvcid gvcid))
  (defstrandmax ground (spi spi) (gvcid gvcid))
  (comment "Initiator's view"
  )
)
```

## sigenc.scm

- **File Path**: `03_examples_scm/sigenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Signed Encrypted Message Example" (comment "Shows examples of key usage of asymmetric keys"))` | Flags: `(comment "Shows examples of key usage of asymmetric keys")`
- **Protocol & Purpose**: Demonstrates asymmetric key separation in a 3-message challenge-response protocol (`mult-keys-sig-enc`) where principals use distinct tagged key pairs for signing (`(privk "sig" a)`) and encryption (`(pubk "enc" b)`). Four skeletons compare the responder's authentication guarantees when trusting only `a`'s signature key, only `a`'s encryption key, or both.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `mult-keys-sig-enc`):
    - `vars`: `(a b name), (n1 n2 text)` | Role assumptions: none
    - `trace`: `(send (enc (enc n1 a (privk "sig" a)) (pubk "enc" b)))` -> `(recv (enc (enc n1 n2 (privk "sig" b)) (pubk "enc" a)))` -> `(send (enc (enc n2 (privk "sig" a)) (pubk "enc" b)))`
  - Role `resp` (in `mult-keys-sig-enc`):
    - `vars`: `(b a name), (n2 n1 text)` | Role assumptions: none
    - `trace`: `(recv (enc (enc n1 a (privk "sig" a)) (pubk "enc" b)))` -> `(send (enc (enc n1 n2 (privk "sig" b)) (pubk "enc" a)))` -> `(recv (enc (enc n2 (privk "sig" a)) (pubk "enc" b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton mult-keys-sig-enc (vars (a b name) (n1 text)) (defstrand init 3 (a a) (b b) (n1 n1)) (non-orig (privk "enc" a) (privk "sig" a) (privk "enc" b)) (uniq-orig n1))`
    - `(defskeleton mult-keys-sig-enc (vars (a b name) (n2 text)) (defstrand resp 3 (a a) (b b) (n2 n2)) (non-orig (privk "sig" a)) (uniq-orig n2))`
    - `(defskeleton mult-keys-sig-enc (vars (a b name) (n2 text)) (defstrand resp 3 (a a) (b b) (n2 n2)) (non-orig (privk "enc" a)) (uniq-orig n2))`
    - `(defskeleton mult-keys-sig-enc (vars (a b name) (n2 text)) (defstrand resp 3 (a a) (b b) (n2 n2)) (non-orig (privk "sig" a) (privk "enc" a)) (uniq-orig n2))`
- **When to Reference This Example**: Reference this example when separating signing and encryption asymmetric keys using string-tagged `(privk "sig" a)` / `(pubk "enc" b)` to prevent cross-key-usage attacks.
- **Key S-Expression Excerpt**:
```scheme
(herald "Signed Encrypted Message Example"
   (comment "Shows examples of key usage of asymmetric keys"))

(defprotocol mult-keys-sig-enc basic
   (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc (enc n1 a (privk "sig" a)) (pubk "enc" b)))
     (recv (enc (enc n1 n2 (privk "sig" b)) (pubk "enc" a)))
     (send (enc (enc n2 (privk "sig" a)) (pubk "enc" b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc (enc n1 a (privk "sig" a)) (pubk "enc" b)))
     (send (enc (enc n1 n2 (privk "sig" b)) (pubk "enc" a)))
     (recv (enc (enc n2 (privk "sig" a)) (pubk "enc" b))))))

;;; The initiator point-of-view
(defskeleton mult-keys-sig-enc
   (vars (a b name) (n1 text))
   (defstrand init 3 (a a) (b b) (n1 n1))
   (non-orig (privk "enc" a) (privk "sig" a) (privk "enc" b))
   (uniq-orig n1))

;;; The responder point-of-view trusting only a's signature key
(defskeleton mult-keys-sig-enc
  (vars (a b name) (n2 text))
  (defstrand resp 3 (a a) (b b) (n2 n2))
  (non-orig (privk "sig" a))
  (uniq-orig n2))

;;; The responder point-of-view trusting only a's encryption key
```

## sorted_epmo_acctnum.scm

- **File Path**: `03_examples_scm/sorted_epmo_acctnum.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Electronic Purchase with Money Order Protocol Variant" (bound 12) (comment "This version includes account numbers in exchanges" "This version uses sorts to avoid confusion" "between a nonce and other data"))` | Flags: `(bound 12)`, `(comment "This version includes account numbers in exchanges" "This version uses sorts to avoid confusion" "between a nonce and other data")`
- **Protocol & Purpose**: Models a variant of the Electronic Purchase with Money Order (EPMO) protocol (`sorted_epmo_acctnum`) between `customer`, `merchant`, and `bank` that includes account numbers (`acctnum`), uses sorts (`data` for nonces `nc`, `nm`, `nb` vs. `text` for `acctnum`, `goods`, `price`) to avoid type confusion, models hashing as `(enc "hash" ... (pubk hash))` with `(non-orig (privk hash))`, and attaches formal trust-management `(annotations ...)` using `says`, `implies`, `forall`, and `exists`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `bank` (in `sorted_epmo_acctnum`):
    - `vars`: `(b c m name), (acctnum price text), (hash name), (nc nm nb data)` | Role assumptions/annotations: `(non-orig (privk hash))`, `(annotations b (1 (forall ((pm name)) (implies (and (authtransfer c acctnum b price pm nm) (reqtransfer pm b price pm nm)) (dotransfer acctnum b price pm nm)))) (2 (and (says c (authtransfer c acctnum b price m nm)) (says m (reqtransfer m b price m nm)))))`
    - `trace`: `(recv (enc c nc nm acctnum price (pubk b)))` -> `(send (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b)) (enc nc nb (pubk c))))` -> `(recv (enc (enc "hash" b m nb nm (pubk hash)) (privk m)))`
  - Role `customer` (in `sorted_epmo_acctnum`):
    - `vars`: `(b c m hash name), (acctnum goods price text), (nc nm nb data)` | Role assumptions/annotations: `(non-orig (privk b) (privk hash))`, `(uniq-orig nc)`, `(annotations c (1 (says m (implies (exists ((acctnum2 text)) (dotransfer acctnum2 b price m nm)) (doship m goods c)))) (3 (says b (forall ((pm name)) (implies (and (authtransfer c acctnum b price m nm) (reqtransfer pm b price pm nm)) (dotransfer acctnum b price pm nm))))) (4 (authtransfer c acctnum b price m nm)))`
    - `trace`: `(send (enc c nc goods (pubk m)))` -> `(recv (enc nc nm m price (pubk c)))` -> `(send (enc c nc nm acctnum price (pubk b)))` -> `(recv (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b)) (enc nc nb (pubk c))))` -> `(send (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b)) nb))`
  - Role `merchant` (in `sorted_epmo_acctnum`):
    - `vars`: `(b c m hash name), (goods price text), (nc nm nb data)` | Role assumptions/annotations: `(non-orig (privk hash))`, `(uniq-orig nm)`, `(annotations m (1 (implies (exists ((acctnum2 text)) (dotransfer acctnum2 b price m nm)) (doship m goods c))) (2 (and (says b (forall ((pm name)) (exists ((acctnum2 text)) (implies (and (authtransfer c acctnum2 b price m nm) (reqtransfer pm b price pm nm)) (dotransfer acctnum2 b price pm nm))))) (says c (exists ((acctnum2 text)) (authtransfer c acctnum2 b price m nm))))) (3 (and (reqtransfer m b price m nm) (doship m goods c))))`
    - `trace`: `(recv (enc c nc goods (pubk m)))` -> `(send (enc nc nm m price (pubk c)))` -> `(recv (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b)) nb))` -> `(send (enc (enc "hash" b m nb nm (pubk hash)) (privk m)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `and`, `annotations`, `bound`, `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `exists`, `forall`, `herald`, `implies`, `non-orig`, `recv`, `says`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sorted_epmo_acctnum (vars (b m c name) (nm nc nb data) (hash name)) (defstrand merchant 4 (b b) (m m) (c c) (nm nm) (nc nc) (nb nb) (hash hash)) (non-orig (privk b) (privk m) (privk c) (privk hash)) (uniq-orig nm nc nb))`
    - `(defskeleton sorted_epmo_acctnum (vars (b m c name) (nm nb nc data) (hash name) (price acctnum text)) (defstrand bank 3 (b b) (m m) (c c) (nm nm) (nb nb) (nc nc) (hash hash)) (non-orig (privk b) (privk m) (privk c) (privk hash)) (uniq-orig nm nc nb))`
- **When to Reference This Example**: Reference this example when using sort separation (`data` vs `text`) to prevent type-flaw attacks in multi-party payment protocols, or when attaching logical `(annotations ...)` to roles.
- **Key S-Expression Excerpt**:
```scheme
(herald "Electronic Purchase with Money Order Protocol Variant"
  (bound 12)
  (comment "This version includes account numbers in exchanges"
	   "This version uses sorts to avoid confusion"
	   "between a nonce and other data"))

(defprotocol sorted_epmo_acctnum basic
  (defrole bank
    (vars (b c m name) (acctnum price text) (hash name) (nc nm nb data))
    (trace
     (recv (enc c nc nm acctnum price (pubk b)))
     (send (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (enc "hash" b m nb nm (pubk hash)) (privk m))))
    (non-orig (privk hash))
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
  (defrole customer
    (vars (b c m hash name) (acctnum goods price text) (nc nm nb data))
    (trace
     (send (enc c nc goods (pubk m)))
     (recv (enc nc nm m price (pubk c)))
     (send (enc c nc nm acctnum price (pubk b)))
     (recv (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b))
		(enc nc nb (pubk c))))
     (send (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b))
		nb)))
    (non-orig (privk b) (privk hash))
```

## sts.scm

- **File Path**: `03_examples_scm/sts.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "Station-to-station protocol" (bound 20) (algebra diffie-hellman))` | Flags: `(bound 20)`, `(algebra diffie-hellman)`
- **Protocol & Purpose**: Models the classic Station-to-Station (STS) authenticated Diffie-Hellman key exchange protocol (`station-to-station`) in the `diffie-hellman` algebra, where both `init` and `resp` include role-level `(uniq-gen x)` / `(uniq-gen y)` assumptions and a fourth event `(send (privk a))` / `(send (privk b))` used in forward-secrecy skeletons.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `station-to-station`):
    - `vars`: `(x rndx), (eta expt), (a b name)` | Role assumptions/annotations: `(uniq-gen x)`
    - `trace`: `(send (exp (gen) x))` -> `(recv (cat (exp (gen) eta) (enc (enc (exp (gen) eta) (exp (gen) x) (privk b)) (exp (exp (gen) eta) x))))` -> `(send (enc (enc (exp (gen) x) (exp (gen) eta) (privk a)) (exp (exp (gen) eta) x)))` -> `(send (privk a))`
  - Role `resp` (in `station-to-station`):
    - `vars`: `(y rndx), (chi expt), (a b name)` | Role assumptions/annotations: `(uniq-gen y)`
    - `trace`: `(recv (exp (gen) chi))` -> `(send (cat (exp (gen) y) (enc (enc (exp (gen) y) (exp (gen) chi) (privk b)) (exp (exp (gen) chi) y))))` -> `(recv (enc (enc (exp (gen) chi) (exp (gen) y) (privk a)) (exp (exp (gen) chi) y)))` -> `(send (privk b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `algebra`, `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (6)**:
    - `(defskeleton station-to-station (vars (a b name)) (defstrand init 3 (a a) (b b)) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station (vars (a b name)) (defstrand resp 3 (a a) (b b)) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-to-station (vars (a b name) (x y rndx) (eta expt)) (defstrand init 3 (a a) (b b) (x x) (eta eta)) (deflistener (exp (exp (gen) eta) x)) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station (vars (a b name) (x y rndx) (chi expt)) (defstrand resp 3 (a a) (b b) (y y) (chi chi)) (deflistener (exp (exp (gen) chi) y)) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-to-station (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (deflistener (exp (gen) (mul x y))) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig (privk b) (privk a)))`
- **When to Reference This Example**: Reference this example when modeling authenticated Diffie-Hellman key exchange (STS) and testing Perfect Forward Secrecy (PFS) by exposing long-term private keys after session completion (`defstrand init 4` with `deflistener (exp (gen) (mul x y))`).
- **Key S-Expression Excerpt**:
```scheme
(herald "Station-to-station protocol" (bound 20) (algebra diffie-hellman))

(defprotocol station-to-station diffie-hellman
  (defrole init
    (vars (x rndx) (eta expt) (a b name))
    (trace
     (send (exp (gen) x))
     (recv (cat (exp (gen) eta)
		(enc (enc (exp (gen) eta)
			  (exp (gen) x) (privk b))
		     (exp (exp (gen) eta) x))))
     (send (enc (enc (exp (gen) x)
		     (exp (gen) eta) (privk a))
		(exp (exp (gen) eta) x)))
     (send (privk a)))
    (uniq-gen x))
  (defrole resp
    (vars (y rndx) (chi expt) (a b name))
    (trace
     (recv (exp (gen) chi))
     (send (cat (exp (gen) y)
		(enc (enc (exp (gen) y)
			  (exp (gen) chi) (privk b))
		     (exp (exp (gen) chi) y))))
     (recv (enc (enc (exp (gen) chi)
		     (exp (gen) y) (privk a))
		(exp (exp (gen) chi) y)))
     (send (privk b)))
    (uniq-gen y)))

(defskeleton station-to-station
  (vars (a b name))
  (defstrand init 3 (a a) (b b))
  (non-orig (privk b) (privk a))
)

```

## sts_non_role.scm

- **File Path**: `03_examples_scm/sts_non_role.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "Station-to-station protocol:  Weakened version" (bound 20) (algebra diffie-hellman))` | Flags: `(bound 20)`, `(algebra diffie-hellman)`
- **Protocol & Purpose**: Models a weakened version of the Station-to-Station protocol (`station-weak`) in the `diffie-hellman` algebra where `(uniq-gen x)` and `(uniq-gen y)` are commented out at the role level and instead asserted only in individual skeletons.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `station-weak`):
    - `vars`: `(x rndx), (eta expt), (a b name)` | Role assumptions: none
    - `trace`: `(send (exp (gen) x))` -> `(recv (cat (exp (gen) eta) (enc (enc (exp (gen) eta) (exp (gen) x) (privk b)) (exp (exp (gen) eta) x))))` -> `(send (enc (enc (exp (gen) x) (exp (gen) eta) (privk a)) (exp (exp (gen) eta) x)))` -> `(send (privk a))`
  - Role `resp` (in `station-weak`):
    - `vars`: `(y rndx), (chi expt), (a b name)` | Role assumptions: none
    - `trace`: `(recv (exp (gen) chi))` -> `(send (cat (exp (gen) y) (enc (enc (exp (gen) y) (exp (gen) chi) (privk b)) (exp (exp (gen) chi) y))))` -> `(recv (enc (enc (exp (gen) chi) (exp (gen) y) (privk a)) (exp (exp (gen) chi) y)))` -> `(send (privk b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `algebra`, `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (7)**:
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand init 3 (a a) (b b) (x x) (eta y)) (uniq-gen x y) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand resp 3 (a a) (b b) (y y) (chi x)) (uniq-gen x y) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand init 3 (a a) (b b) (x x) (eta y)) (deflistener (exp (exp (gen) y) x)) (uniq-gen x y) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-weak (vars (a b name) (x rndx) (eta expt)) (defstrand init 3 (a a) (b b) (x x) (eta eta)) (deflistener (exp (exp (gen) eta) x)) (uniq-gen x) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-weak (vars (a b name) (y rndx) (chi expt)) (defstrand resp 3 (a a) (b b) (y y) (chi chi)) (deflistener (exp (exp (gen) chi) y)) (non-orig (privk a) (privk b)) (uniq-gen y))`
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-gen x y) (uniq-orig (privk b) (privk a)))`
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (deflistener (exp (gen) (mul x y))) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-gen x y) (uniq-orig (privk b) (privk a)))`
- **When to Reference This Example**: Reference this example to understand the difference between role-level `(uniq-gen ...)` (every peer strand generates a fresh DH exponent) and skeleton-level `(uniq-gen ...)` (only the POV/specified strands are guaranteed fresh exponents).
- **Key S-Expression Excerpt**:
```scheme
(herald "Station-to-station protocol:  Weakened version"
	(bound 20)
	(algebra diffie-hellman))

(defprotocol station-weak diffie-hellman
  (defrole init
    (vars (x rndx) (eta expt) (a b name))
    (trace
     (send (exp (gen) x))
     (recv (cat (exp (gen) eta)
		(enc (enc (exp (gen) eta)
			  (exp (gen) x) (privk b))
		     (exp (exp (gen) eta) x))))
     (send (enc (enc (exp (gen) x)
		     (exp (gen) eta) (privk a))
		(exp (exp (gen) eta) x)))
     (send (privk a)))
    ;; (uniq-gen x)
    )
  (defrole resp
    (vars (y rndx) (chi expt) (a b name))
    (trace
     (recv (exp (gen) chi))
     (send (cat (exp (gen) y)
		(enc (enc (exp (gen) y)
			  (exp (gen) chi) (privk b))
		     (exp (exp (gen) chi) y))))
     (recv (enc (enc (exp (gen) chi)
		     (exp (gen) y) (privk a))
		(exp (exp (gen) chi) y)))
     (send (privk b)))
    ;; (uniq-gen y)
    ))

(defskeleton station-weak
  (vars (a b name) (x y rndx))
  (defstrand init 3 (a a) (b b) (x x) (eta y))
  (uniq-gen x y)
```

## sts_weakened_reflect.scm

- **File Path**: `03_examples_scm/sts_weakened_reflect.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "station-to-station-reflect protocol" (bound 20) (algebra diffie-hellman))` | Flags: `(bound 20)`, `(algebra diffie-hellman)`
- **Protocol & Purpose**: Models a weakened Station-to-Station variant (`station-to-station-reflect`) in the `diffie-hellman` algebra that omits the order flip of the Diffie-Hellman exponentials `(exp (gen) eta)` and `(exp (gen) x)` inside the signed component of the second and third messages, enabling a reflection/type-symmetry attack.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `station-to-station-reflect`):
    - `vars`: `(x rndx), (eta expt), (a b name)` | Role assumptions/annotations: `(uniq-gen x)`
    - `trace`: `(send (exp (gen) x))` -> `(recv (cat (exp (gen) eta) (enc (enc (exp (gen) eta) (exp (gen) x) (privk b)) (exp (exp (gen) eta) x))))` -> `(send (enc (enc (exp (gen) eta) (exp (gen) x) (privk a)) (exp (exp (gen) eta) x)))` -> `(send (privk a))`
  - Role `resp` (in `station-to-station-reflect`):
    - `vars`: `(y rndx), (chi expt), (a b name)` | Role assumptions/annotations: `(uniq-gen y)`
    - `trace`: `(recv (exp (gen) chi))` -> `(send (cat (exp (gen) y) (enc (enc (exp (gen) y) (exp (gen) chi) (privk b)) (exp (exp (gen) chi) y))))` -> `(recv (enc (enc (exp (gen) y) (exp (gen) chi) (privk a)) (exp (exp (gen) chi) y)))` -> `(send (privk b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `algebra`, `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (6)**:
    - `(defskeleton station-to-station-reflect (vars (a b name)) (defstrand init 3 (a a) (b b)) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station-reflect (vars (a b name)) (defstrand resp 3 (a a) (b b)) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-to-station-reflect (vars (a b name) (x y rndx) (eta expt)) (defstrand init 3 (a a) (b b) (x x) (eta eta)) (deflistener (exp (exp (gen) eta) x)) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station-reflect (vars (a b name) (x y rndx) (chi expt)) (defstrand resp 3 (a a) (b b) (y y) (chi chi)) (deflistener (exp (exp (gen) chi) y)) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-to-station-reflect (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station-reflect (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (deflistener (exp (gen) (mul x y))) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig (privk b) (privk a)))`
- **When to Reference This Example**: Reference this example when analyzing reflection or role-confusion vulnerabilities in Diffie-Hellman handshake signatures where initiator and responder sign identically ordered transcript terms.
- **Key S-Expression Excerpt**:
```scheme
(herald "station-to-station-reflect protocol" (bound 20) (algebra diffie-hellman))

(defprotocol station-to-station-reflect diffie-hellman
  (defrole init
    (vars (x rndx) (eta expt) (a b name))
    (trace
     (send (exp (gen) x))
     (recv (cat (exp (gen) eta)
		(enc (enc (exp (gen) eta)
			  (exp (gen) x) (privk b))
		     (exp (exp (gen) eta) x))))
     (send (enc (enc (exp (gen) eta)
		     (exp (gen) x) (privk a))
		(exp (exp (gen) eta) x)))
     (send (privk a)))
    (uniq-gen x))
  (defrole resp
    (vars (y rndx) (chi expt) (a b name))
    (trace
     (recv (exp (gen) chi))
     (send (cat (exp (gen) y)
		(enc (enc (exp (gen) y)
			  (exp (gen) chi) (privk b))
		     (exp (exp (gen) chi) y))))
     (recv (enc (enc (exp (gen) y)
		     (exp (gen) chi) (privk a))
		(exp (exp (gen) chi) y)))
     (send (privk b)))
    (uniq-gen y)))

(defskeleton station-to-station-reflect
  (vars (a b name))
  (defstrand init 3 (a a) (b b))
```

## subatomic-open-closed-test-genrule.scm

- **File Path**: `03_examples_scm/subatomic-open-closed-test-genrule.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald subatomic-open-closed-test-genrule (bound 40))` | Flags: `(bound 40)`
- **Protocol & Purpose**: Models a stateful device open/close/pass access-control protocol (`subatomic-open-closed`) with two state locations (`lk` for key state, `ls` for open/closed status), channels (`start-ch`), `(gen-st ...)`, `(facts (same-dev ls lk))`, and explicit `(defgenrule ...)` declarations encoding subatomic state transition semantics (`no-interruption`, `cakeRule`, `scissorsRule`, `shearsRule`, `invShearsRule`, `trans`, `same-locn`, `leads-to`).
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `dev-up` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d o name), (old old1 mesg), (start-ch chan), (lk ls locn)` | Role assumptions/annotations: `(auth start-ch)`, `(facts (same-dev ls lk))`
    - `trace`: `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(load ls old1)` -> `(stor lk (cat "st-k" d o k))` -> `(stor ls (cat "st" d o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d o name), (start-ch chan)` | Role assumptions/annotations: `(conf start-ch)`
    - `trace`: `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name)` | Role assumptions: none
    - `trace`: `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name)` | Role assumptions: none
    - `trace`: `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d o name), (lk ls locn)` | Role assumptions/annotations: `(gen-st (cat "st-k" d o k) (cat "st" d (cat o o)))`, `(facts (same-dev ls lk))`
    - `trace`: `(recv (enc "open" d o n k))` -> `(load ls (cat "st" d any))` -> `(load lk (cat "st-k" d o k))` -> `(stor ls (cat "st" d o o))` -> `(send n)`
  - Role `dev-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d o name), (lk ls locn)` | Role assumptions/annotations: `(gen-st (cat "st-k" d o k))`, `(facts (same-dev ls lk))`
    - `trace`: `(recv (enc "close" d o n k))` -> `(load lk (cat "st-k" d o k))` -> `(load ls (cat "st" d any))` -> `(stor ls (cat "st" d o))` -> `(send n)`
  - Role `dev-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name), (lk ls locn)` | Role assumptions/annotations: `(uniq-orig n)`, `(gen-st (cat "st-k" d o k) (cat "st" d (cat o o)))`, `(facts (same-dev ls lk))`
    - `trace`: `(load lk (cat "st-k" d o k))` -> `(load ls (cat "st" d o o))` -> `(recv (enc "may I pass" k))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey)` | Role assumptions: none
    - `trace`: `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `=`, `and`, `auth`, `bound`, `conf`, `defgenrule`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `false`, `forall`, `gen-st`, `herald`, `implies`, `leads-to`, `load`, `or`, `p`, `prec`, `recv`, `same-locn`, `send`, `stor`, `trace`, `trans`, `uniq-orig`, `vars`
  - **Macros (6)**: `(dev-key-state d o k)` -> `(cat "st-k" d o k)`; `(opened o)` -> `(cat o o)`; `(closed o)` -> `o`; `(dev-state-opened d o)` -> `(cat "st" d (opened o))`; `(dev-state-closed d o)` -> `(cat "st" d (closed o))`; `(dev-state-any d o any)` -> `(cat "st" d any)`
  - **Rules & Genrules (33)**:
    - `(defrule power-deliver-once ...)` in `subatomic-open-closed`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
    - `(defrule same-dev-ls-lk ...)` in `subatomic-open-closed`: `(forall ((ls lk lk-0 locn)) (implies (and (fact same-dev ls lk) (fact same-dev ls lk-0)) (= lk lk-0)))`
    - `(defrule same-dev-lk-ls ...)` in `subatomic-open-closed`: `(forall ((lk ls ls-0 locn)) (implies (and (fact same-dev ls lk) (fact same-dev ls-0 lk)) (= ls ls-0)))`
    - `(defgenrule neqRl_indx ...)` in `subatomic-open-closed`: `(forall ((x indx)) (implies (fact neq x x) (false)))`
    - `(defgenrule neqRl_strd ...)` in `subatomic-open-closed`: `(forall ((x strd)) (implies (fact neq x x) (false)))`
    - `(defgenrule neqRl_mesg ...)` in `subatomic-open-closed`: `(forall ((x mesg)) (implies (fact neq x x) (false)))`
    - `(defgenrule no-interruption ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (leads-to z0 i0 z2 i2) (trans z1 i1) (same-locn z0 i0 z1 i1) (prec z0 i0 z1 i1) (prec z1 i1 z2 i2)) (false)))`
    - `(defgenrule cakeRule ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (trans z0 i0) (trans z1 i1) (leads-to z0 i0 z1 i1) (leads-to z0 i0 z2 i2) (prec z1 i1 z2 i2)) (false)))`
    - `(defgenrule gen-st-dev-pass-0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (o d name)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "o" z o) (p "dev-pass" "d" z d)) (gen-st (cat "st" d o o))))`
    - `(defgenrule gen-st-dev-pass-1 ...)` in `subatomic-open-closed`: `(forall ((z strd) (k skey) (o d name)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "k" z k) (p "dev-pass" "o" z o) (p "dev-pass" "d" z d)) (gen-st (cat "st-k" d o k))))`
    - `(defgenrule fact-dev-pass-same-dev0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (ls lk locn)) (implies (and (p "dev-pass" z 2) (p "dev-pass" "ls" z ls) (p "dev-pass" "lk" z lk)) (fact same-dev ls lk)))`
    - `(defgenrule trRl_dev-close-at-2 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-close" z 3) (trans z 2)))`
    - `(defgenrule trRl_dev-close-at-3 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-close" z 4) (trans z 3)))`
    - `(defgenrule gen-st-dev-close-0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (k skey) (o d name)) (implies (and (p "dev-close" z 1) (p "dev-close" "k" z k) (p "dev-close" "o" z o) (p "dev-close" "d" z d)) (gen-st (cat "st-k" d o k))))`
    - `(defgenrule fact-dev-close-same-dev0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (ls lk locn)) (implies (and (p "dev-close" z 3) (p "dev-close" "ls" z ls) (p "dev-close" "lk" z lk)) (fact same-dev ls lk)))`
    - `(defgenrule trRl_dev-open-at-1 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-open" z 2) (trans z 1)))`
    - `(defgenrule trRl_dev-open-at-3 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-open" z 4) (trans z 3)))`
    - `(defgenrule gen-st-dev-open-0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (o d name)) (implies (and (p "dev-open" z 1) (p "dev-open" "o" z o) (p "dev-open" "d" z d)) (gen-st (cat "st" d o o))))`
    - `(defgenrule gen-st-dev-open-1 ...)` in `subatomic-open-closed`: `(forall ((z strd) (k skey) (o d name)) (implies (and (p "dev-open" z 1) (p "dev-open" "k" z k) (p "dev-open" "o" z o) (p "dev-open" "d" z d)) (gen-st (cat "st-k" d o k))))`
    - `(defgenrule fact-dev-open-same-dev0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (ls lk locn)) (implies (and (p "dev-open" z 3) (p "dev-open" "ls" z ls) (p "dev-open" "lk" z lk)) (fact same-dev ls lk)))`
    - `(defgenrule trRl_dev-up-at-1 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-up" z 2) (trans z 1)))`
    - `(defgenrule trRl_dev-up-at-2 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-up" z 3) (trans z 2)))`
    - `(defgenrule trRl_dev-up-at-3 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-up" z 4) (trans z 3)))`
    - `(defgenrule trRl_dev-up-at-4 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-up" z 5) (trans z 4)))`
    - `(defgenrule fact-dev-up-same-dev0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (ls lk locn)) (implies (and (p "dev-up" z 3) (p "dev-up" "ls" z ls) (p "dev-up" "lk" z lk)) (fact same-dev ls lk)))`
    - `(defgenrule scissorsRule ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (trans z0 i0) (trans z1 i1) (trans z2 i2) (leads-to z0 i0 z1 i1) (leads-to z0 i0 z2 i2)) (and (= z1 z2) (= i1 i2))))`
    - `(defgenrule cau-dev-pass-1 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-pass" z 2) (prec z1 i z 1)) (or (= z z1) (prec z1 i z 0))))`
    - `(defgenrule cau-dev-close-2 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-close" z 3) (prec z1 i z 2)) (or (= z z1) (prec z1 i z 1))))`
    - `(defgenrule cau-dev-open-2 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-open" z 3) (prec z1 i z 2)) (or (= z z1) (prec z1 i z 1))))`
    - `(defgenrule cau-dev-up-2 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-up" z 3) (prec z1 i z 2)) (or (= z z1) (prec z1 i z 1))))`
    - `(defgenrule eff-dev-up-3 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-up" z 4) (prec z 3 z1 i)) (or (= z z1) (and (p "dev-up" z 5) (prec z 4 z1 i)))))`
    - `(defgenrule invShearsRule ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (trans z0 i0) (trans z1 i1) (same-locn z0 i0 z1 i1) (leads-to z1 i1 z2 i2) (prec z0 i0 z2 i2)) (or (and (= z0 z1) (= i0 i1)) (prec z0 i0 z1 i1))))`
    - `(defgenrule shearsRule ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (trans z0 i0) (trans z1 i1) (trans z2 i2) (leads-to z0 i0 z1 i1) (same-locn z0 i0 z2 i2) (prec z0 i0 z2 i2)) (or (and (= z1 z2) (= i1 i2)) (prec z1 i1 z2 i2))))`
  - **Goals**: None.
  - **Skeletons (3)**:
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (deflistener k) (uniq-orig k) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand dev-pass 4 (k k)) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (defstrand dev-pass 4 (k k)) (uniq-orig k) (facts (no-state-split)))`
- **When to Reference This Example**: Reference this example when debugging or writing low-level `(defgenrule ...)` axioms for stateful location (`locn`) transitions, `leads-to`, `trans`, `same-locn`, and `gen-st` without relying on obsolete `critical-sections`.
- **Key S-Expression Excerpt**:
```scheme
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan)
      (lk ls locn))
    (trace (recv start-ch (cat "power-up" d o k)) (load lk old)
      (load ls old1) (stor lk (cat "st-k" d o k))
      (stor ls (cat "st" d o)) (send (enc "up" k)))
    (auth start-ch)
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 4))
    (facts (same-dev ls lk)))
  (defrole owner-power-dev
    (vars (k skey) (d o name) (start-ch chan))
    (trace (send start-ch (cat "power-up" d o k)) (recv (enc "up" k)))
    (conf start-ch))
  (defrole owner-open
    (vars (k skey) (n text) (d o name))
    (trace (send (enc "open" d o n k)) (recv n)))
  (defrole owner-close
    (vars (k skey) (n text) (d o name))
    (trace (send (enc "close" d o n k)) (recv n)))
  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace (recv (enc "open" d o n k)) (load ls (cat "st" d any))
      (load lk (cat "st-k" d o k)) (stor ls (cat "st" d o o)) (send n))
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 3))
    (gen-st (cat "st-k" d o k) (cat "st" d (cat o o)))
    (facts (same-dev ls lk)))
  (defrole dev-close
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace (recv (enc "close" d o n k)) (load lk (cat "st-k" d o k))
      (load ls (cat "st" d any)) (stor ls (cat "st" d o)) (send n))
    (gen-st (cat "st-k" d o k))
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 3))
    (facts (same-dev ls lk)))
```

## subatomic-open-closed.scm

- **File Path**: `03_examples_scm/subatomic-open-closed.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald subatomic-open-closed (bound 40))` | Flags: `(bound 40)`
- **Protocol & Purpose**: Models the stateful `subatomic-open-closed` device protocol using state macros (`dev-key-state`, `dev-state-opened`, `dev-state-closed`, `dev-state-any`), two `locn` variables (`lk`, `ls`), channel `start-ch` (`auth`/`conf`), `(gen-st ...)`, and three user-level `(defrule ...)` axioms (`power-deliver-once`, `same-dev-ls-lk`, `same-dev-lk-ls`) without the auto-generated `defgenrule` boilerplate.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `dev-up` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d o name), (old old1 mesg), (start-ch chan), (lk ls locn)` | Role assumptions/annotations: `(auth start-ch)`, `(facts (same-dev ls lk))`
    - `trace`: `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(load ls old1)` -> `(stor lk (dev-key-state d o k))` -> `(stor ls (dev-state-closed d o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d o name), (start-ch chan)` | Role assumptions/annotations: `(conf start-ch)`
    - `trace`: `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name)` | Role assumptions: none
    - `trace`: `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name)` | Role assumptions: none
    - `trace`: `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d o name), (lk ls locn)` | Role assumptions/annotations: `(gen-st (dev-key-state d o k) (dev-state-opened d o))`, `(facts (same-dev ls lk))`
    - `trace`: `(recv (enc "open" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(load lk (dev-key-state d o k))` -> `(stor ls (dev-state-opened d o))` -> `(send n)`
  - Role `dev-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d o name), (lk ls locn)` | Role assumptions/annotations: `(gen-st (dev-key-state d o k))`, `(facts (same-dev ls lk))`
    - `trace`: `(recv (enc "close" d o n k))` -> `(load lk (dev-key-state d o k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-closed d o))` -> `(send n)`
  - Role `dev-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name), (lk ls locn)` | Role assumptions/annotations: `(uniq-orig n)`, `(gen-st (dev-key-state d o k) (dev-state-opened d o))`, `(facts (same-dev ls lk))`
    - `trace`: `(load lk (dev-key-state d o k))` -> `(load ls (dev-state-opened d o))` -> `(recv (enc "may I pass" k))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name), (l locn)` | Role assumptions: none
    - `trace`: `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `=`, `and`, `auth`, `bound`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `forall`, `gen-st`, `herald`, `implies`, `load`, `p`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros (6)**: `(dev-key-state d o k)` -> `(cat "st-k" d o k)`; `(opened o)` -> `(cat o o)`; `(closed o)` -> `o`; `(dev-state-opened d o)` -> `(cat "st" d (opened o))`; `(dev-state-closed d o)` -> `(cat "st" d (closed o))`; `(dev-state-any d o any)` -> `(cat "st" d any)`
  - **Rules & Genrules (3)**:
    - `(defrule power-deliver-once ...)` in `subatomic-open-closed`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
    - `(defrule same-dev-ls-lk ...)` in `subatomic-open-closed`: `(forall ((ls lk lk-0 locn)) (implies (and (fact same-dev ls lk) (fact same-dev ls lk-0)) (= lk lk-0)))`
    - `(defrule same-dev-lk-ls ...)` in `subatomic-open-closed`: `(forall ((lk ls ls-0 locn)) (implies (and (fact same-dev ls lk) (fact same-dev ls-0 lk)) (= ls ls-0)))`
  - **Goals**: None.
  - **Skeletons (3)**:
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (deflistener k) (uniq-orig k) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand dev-pass 4 (k k)) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (defstrand dev-pass 4 (k k)) (uniq-orig k) (facts (no-state-split)))`
- **When to Reference This Example**: Reference this example as the clean idiom for modeling multi-location device state with `load`/`stor`, `gen-st`, `facts`, and `defrule` functional dependencies between locations on the same device.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol subatomic-open-closed basic
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))
    (trace
     (recv start-ch (cat "power-up" d o k))
     (load lk old)
     (load ls old1)
     (stor lk (dev-key-state d o k))
     (stor ls (dev-state-closed d o))
     (send (enc "up" k)))
    (auth start-ch)
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 4))
    (facts (same-dev ls lk)))

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
```

## sync_locn_envelope.scm

- **File Path**: `03_examples_scm/sync_locn_envelope.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Envelope Protocol, location-based version" (check-nonces) (bound 30) (limit 6000))` | Flags: `(check-nonces)`, `(bound 30)`, `(limit 6000)`
- **Protocol & Purpose**: Models the TPM Envelope Protocol (`envelope`) using location-based state (`pcr` of sort `locn`) and channels (`tpm`, `tpmconf` of sort `chan`), using higher-order macros `(defmacro (roles) (^ ...))` and `(defmacro (genStV-rules) (^ ...))` with splice operator `^` to share roles and `gen-st` rules across protocol variants.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `tpm-power-on` (in `envelope`):
    - `vars`: `(current-value mesg), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc` (in `envelope`):
    - `vars`: `(value current-value mesg), (pcr-id nonce text), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(uniq-orig nonce)`
    - `trace`: `(send tpm (cat "token" nonce))` -> `(recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote` (in `envelope`):
    - `vars`: `(nonce current-value mesg), (pcr-id text), (aik akey), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key` (in `envelope`):
    - `vars`: `(k aik akey), (pcr-id text), (pcrval mesg), (tpm chan)` | Role assumptions/annotations: `(uniq-orig k)`, `(non-orig (invk k))`, `(auth tpm)`
    - `trace`: `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt` (in `envelope`):
    - `vars`: `(m current-value mesg), (pcr-id text), (k aik akey), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(non-orig aik)`
    - `trace`: `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice` (in `envelope`):
    - `vars`: `(n v data), (pcr-id nonce text), (k aik akey), (tpm tpmconf chan)` | Role assumptions/annotations: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpmconf)`
    - `trace`: `(recv tpm (cat "token" nonce))` -> `(send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `^`, `and`, `auth`, `bound`, `check-nonces`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `facts`, `forall`, `gen-st`, `herald`, `implies`, `limit`, `load`, `neq`, `non-orig`, `p`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros (3)**: `(refuse pcr-id n v k aik)` -> `(enc "quote" pcr-id (hash (hash "0" n) "refuse") (enc v k) aik)`; `(roles)` -> `(^ (defrole tpm-power-on (vars (current-value mesg) (pcr locn) (tpm chan)) (trace (recv tpm "power on") (load pcr current-value) (stor pcr "0"))) (defrole tpm-extend-enc (vars (value current-value mesg) (pcr-id nonce text) (pcr locn) (tpm chan)) (trace (send tpm (cat "token" nonce)) (recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce))) (load pcr current-value) (stor pcr (hash current-value value)) (send "ext ok")) (uniq-orig nonce)) (defrole tpm-quote (vars (nonce current-value mesg) (pcr-id text) (aik akey) (pcr locn) (tpm chan)) (trace (recv tpm (cat "quote" pcr-id nonce)) (load pcr current-value) (send (enc "quote" pcr-id current-value nonce aik)))) (defrole tpm-create-key (vars (k aik akey) (pcr-id text) (pcrval mesg) (tpm chan)) (trace (recv tpm (cat "create-req" pcr-id pcrval)) (send (enc "created" k pcr-id pcrval aik))) (uniq-orig k) (non-orig (invk k)) (auth tpm)) (defrole tpm-decrypt (vars (m current-value mesg) (pcr-id text) (k aik akey) (pcr locn) (tpm chan)) (trace (recv tpm (cat "decrypt" (enc m k))) (recv (enc "created" k pcr-id current-value aik)) (load pcr current-value) (send m)) (non-orig aik)) (defrole alice (vars (n v data) (pcr-id nonce text) (k aik akey) (tpm tpmconf chan)) (trace (recv tpm (cat "token" nonce)) (send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce))) (send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain"))) (recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik)) (send (enc v k))) (neq (k aik)) (uniq-orig n v) (non-orig aik) (conf tpmconf)))`; `(genStV-rules)` -> `(^ (defrule genStV-if-hashed-tpm-power-on (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-extend-enc (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-decrypt (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-quote (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))))`
  - **Rules & Genrules (4)**:
    - `(defrule genStV-if-hashed-tpm-power-on ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-extend-enc ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-decrypt ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-quote ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton envelope (vars (v data)) (deflistener v) (defstrand alice 5 (v v)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)) (facts (no-state-split)))`
- **When to Reference This Example**: Reference this example when modeling TPM PCR `load`/`stor` state machines, channel authentication `(auth tpm)` / confidentiality `(conf tpmconf)`, or when using `(defmacro (name) (^ ...))` to splice multiple roles/rules into a `defprotocol`.
- **Key S-Expression Excerpt**:
```scheme
(defmacro (roles)
  (^
   ;; Power on sets the pcr to 0
   (defrole tpm-power-on
     (vars (current-value mesg) (pcr locn) (tpm chan))
     (trace
      (recv tpm "power on")
      (load pcr current-value)
      (stor pcr "0")))

   ;; The extend command takes the value to extend and the current PCR
   ;; value and produces the hash of the two values.
   ;;     (defrole tpm-extend
   ;;        (vars (value current-value mesg) (pcr locn))
   ;;        (trace
   ;;         (recv (cat "extend" value))
   ;;         (recv pcr current-value)		    ;; MSR lhs (deleted)
   ;;         (stor pcr (hash current-value value)) ;; MSR rhs
   ;;         (send "ext ok")))

   ;; The extend command can also occur within an
   ;; encrypted session.  We assume some session key already exists
   (defrole tpm-extend-enc
     (vars (value current-value mesg) (pcr-id nonce text) (pcr locn) (tpm chan))
     (trace
      (send tpm (cat "token" nonce))
      (recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))
      (load pcr current-value)		    ;; MSR lhs (deleted)
      (stor pcr (hash current-value value)) ;; MSR rhs
      (send "ext ok"))
     (uniq-orig nonce))

   ;; The TPM must retrieve the current pcr value.  Notice that
   ;; the nonce is of sort mesg, which allows non-atomic values.
   (defrole tpm-quote
```

## sync_locn_envelope_no_auth.scm

- **File Path**: `03_examples_scm/sync_locn_envelope_no_auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Envelope Protocol, location-based version" (check-nonces) (bound 30) (limit 6000))` | Flags: `(check-nonces)`, `(bound 30)`, `(limit 6000)`
- **Protocol & Purpose**: Variant of the location-based TPM Envelope Protocol that comments out `(auth tpm)` in `tpm-create-key`, activates four `genStV-not-catted-*` rules forbidding catted PCR values, and compares three protocol rule sets (`envelope`, `envelope-plus` with `ordered-extends`, and `envelope-plus-2` with `pcr-id-identifies-pcr`).
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `tpm-power-on` (in `envelope`):
    - `vars`: `(current-value mesg), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc` (in `envelope`):
    - `vars`: `(value current-value mesg), (pcr-id nonce text), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(uniq-orig nonce)`
    - `trace`: `(send tpm (cat "token" nonce))` -> `(recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote` (in `envelope`):
    - `vars`: `(nonce current-value mesg), (pcr-id text), (aik akey), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key` (in `envelope`):
    - `vars`: `(k aik akey), (pcr-id text), (pcrval mesg), (tpm chan)` | Role assumptions/annotations: `(uniq-orig k)`, `(non-orig (invk k))`
    - `trace`: `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt` (in `envelope`):
    - `vars`: `(m current-value mesg), (pcr-id text), (k aik akey), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(non-orig aik)`
    - `trace`: `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice` (in `envelope`):
    - `vars`: `(n v data), (pcr-id nonce text), (k aik akey), (tpm tpmconf chan)` | Role assumptions/annotations: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpmconf)`
    - `trace`: `(recv tpm (cat "token" nonce))` -> `(send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
  - Role `tpm-power-on` (in `envelope-plus`):
    - `vars`: `(current-value mesg), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc` (in `envelope-plus`):
    - `vars`: `(value current-value mesg), (pcr-id nonce text), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(uniq-orig nonce)`
    - `trace`: `(send tpm (cat "token" nonce))` -> `(recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote` (in `envelope-plus`):
    - `vars`: `(nonce current-value mesg), (pcr-id text), (aik akey), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key` (in `envelope-plus`):
    - `vars`: `(k aik akey), (pcr-id text), (pcrval mesg), (tpm chan)` | Role assumptions/annotations: `(uniq-orig k)`, `(non-orig (invk k))`
    - `trace`: `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt` (in `envelope-plus`):
    - `vars`: `(m current-value mesg), (pcr-id text), (k aik akey), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(non-orig aik)`
    - `trace`: `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice` (in `envelope-plus`):
    - `vars`: `(n v data), (pcr-id nonce text), (k aik akey), (tpm tpmconf chan)` | Role assumptions/annotations: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpmconf)`
    - `trace`: `(recv tpm (cat "token" nonce))` -> `(send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
  - Role `tpm-power-on` (in `envelope-plus-2`):
    - `vars`: `(current-value mesg), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc` (in `envelope-plus-2`):
    - `vars`: `(value current-value mesg), (pcr-id nonce text), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(uniq-orig nonce)`
    - `trace`: `(send tpm (cat "token" nonce))` -> `(recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote` (in `envelope-plus-2`):
    - `vars`: `(nonce current-value mesg), (pcr-id text), (aik akey), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key` (in `envelope-plus-2`):
    - `vars`: `(k aik akey), (pcr-id text), (pcrval mesg), (tpm chan)` | Role assumptions/annotations: `(uniq-orig k)`, `(non-orig (invk k))`
    - `trace`: `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt` (in `envelope-plus-2`):
    - `vars`: `(m current-value mesg), (pcr-id text), (k aik akey), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(non-orig aik)`
    - `trace`: `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice` (in `envelope-plus-2`):
    - `vars`: `(n v data), (pcr-id nonce text), (k aik akey), (tpm tpmconf chan)` | Role assumptions/annotations: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpmconf)`
    - `trace`: `(recv tpm (cat "token" nonce))` -> `(send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `=`, `^`, `and`, `bound`, `check-nonces`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `false`, `forall`, `gen-st`, `herald`, `implies`, `limit`, `load`, `neq`, `non-orig`, `or`, `p`, `prec`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros (3)**: `(refuse pcr-id n v k aik)` -> `(enc "quote" pcr-id (hash (hash "0" n) "refuse") (enc v k) aik)`; `(roles)` -> `(^ (defrole tpm-power-on (vars (current-value mesg) (pcr locn) (tpm chan)) (trace (recv tpm "power on") (load pcr current-value) (stor pcr "0"))) (defrole tpm-extend-enc (vars (value current-value mesg) (pcr-id nonce text) (pcr locn) (tpm chan)) (trace (send tpm (cat "token" nonce)) (recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce))) (load pcr current-value) (stor pcr (hash current-value value)) (send "ext ok")) (uniq-orig nonce)) (defrole tpm-quote (vars (nonce current-value mesg) (pcr-id text) (aik akey) (pcr locn) (tpm chan)) (trace (recv tpm (cat "quote" pcr-id nonce)) (load pcr current-value) (send (enc "quote" pcr-id current-value nonce aik)))) (defrole tpm-create-key (vars (k aik akey) (pcr-id text) (pcrval mesg) (tpm chan)) (trace (recv tpm (cat "create-req" pcr-id pcrval)) (send (enc "created" k pcr-id pcrval aik))) (uniq-orig k) (non-orig (invk k))) (defrole tpm-decrypt (vars (m current-value mesg) (pcr-id text) (k aik akey) (pcr locn) (tpm chan)) (trace (recv tpm (cat "decrypt" (enc m k))) (recv (enc "created" k pcr-id current-value aik)) (load pcr current-value) (send m)) (non-orig aik)) (defrole alice (vars (n v data) (pcr-id nonce text) (k aik akey) (tpm tpmconf chan)) (trace (recv tpm (cat "token" nonce)) (send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce))) (send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain"))) (recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik)) (send (enc v k))) (neq (k aik)) (uniq-orig n v) (non-orig aik) (conf tpmconf)))`; `(genStV-rules)` -> `(^ (defrule genStV-if-hashed-tpm-power-on (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-extend-enc (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-decrypt (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-quote (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-not-catted-tpm-power-on (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (cat v1 v2))) (false)))) (defrule genStV-not-catted-tpm-extend-enc (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (cat v1 v2))) (false)))) (defrule genStV-not-catted-tpm-decrypt (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (cat v1 v2))) (false)))) (defrule genStV-not-catted-tpm-quote (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (cat v1 v2))) (false)))))`
  - **Rules & Genrules (26)**:
    - `(defrule genStV-if-hashed-tpm-power-on ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-extend-enc ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-decrypt ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-quote ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-not-catted-tpm-power-on ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-extend-enc ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-decrypt ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-quote ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-if-hashed-tpm-power-on ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-extend-enc ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-decrypt ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-quote ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-not-catted-tpm-power-on ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-extend-enc ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-decrypt ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-quote ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule ordered-extends ...)` in `envelope-plus`: `(forall ((y z strd) (pcr locn)) (implies (and (p "tpm-extend-enc" y 4) (p "tpm-extend-enc" z 4) (p "tpm-extend-enc" "pcr" y pcr) (p "tpm-extend-enc" "pcr" z pcr)) (or (= y z) (prec y 3 z 2) (prec z 3 y 2))))`
    - `(defrule genStV-if-hashed-tpm-power-on ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-extend-enc ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-decrypt ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-quote ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-not-catted-tpm-power-on ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-extend-enc ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-decrypt ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-quote ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule pcr-id-identifies-pcr ...)` in `envelope-plus-2`: `(forall ((y z strd) (pcr-id text) (pcr pcr-0 locn)) (implies (and (p "tpm-extend-enc" y 3) (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "pcr-id" y pcr-id) (p "tpm-extend-enc" "pcr-id" z pcr-id) (p "tpm-extend-enc" "pcr" y pcr) (p "tpm-extend-enc" "pcr" z pcr-0)) (= pcr pcr-0)))`
  - **Goals**: None.
  - **Skeletons (9)**:
    - `(defskeleton envelope (vars (v data)) (deflistener v) (defstrand alice 5 (v v)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope-plus (vars (v data)) (deflistener v) (defstrand alice 5 (v v)))`
    - `(defskeleton envelope-plus (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope-plus (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope-plus-2 (vars (v data)) (deflistener v) (defstrand alice 5 (v v)))`
    - `(defskeleton envelope-plus-2 (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope-plus-2 (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
- **When to Reference This Example**: Reference this example to see how omitting channel authentication `(auth tpm)` affects TPM state shapes and how `defrule` axioms (`ordered-extends`, `pcr-id-identifies-pcr`) prevent state-splitting across multiple protocol variants in one file.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol envelope-plus basic
  (roles)
  (genStV-rules)

  (defrule ordered-extends
    (forall ((y z strd) (pcr locn))
	    (implies
	     (and (p "tpm-extend-enc" y 4)
		  (p "tpm-extend-enc" z 4)
		  (p "tpm-extend-enc" "pcr" y pcr)
		  (p "tpm-extend-enc" "pcr" z pcr))
	     (or (= y z)
		 (prec y 3 z 2)
		 (prec z 3 y 2))))))


(defskeleton envelope-plus
  (vars (v data))
  (deflistener v)
  (defstrand alice 5 (v v)))

(defskeleton envelope-plus
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope-plus
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (deflistener v)
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))


(defprotocol envelope-plus-2 basic
  (roles)
```

## targetterms1.scm

- **File Path**: `03_examples_scm/targetterms1.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Minimal two-role protocol (`targetterms`) testing CPSA's target terms solved filter: `init` sends `(enc n1 (enc a n2 k) k)` and expects `(enc a n1 k)`, while `resp` decrypts `(enc n1 m k)` and sends `m`, forcing `n1 = n2` and `m = (enc a n1 k)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `targetterms`):
    - `vars`: `(a skey), (n1 n2 text), (k akey)` | Role assumptions: none
    - `trace`: `(send (enc n1 (enc a n2 k) k))` -> `(recv (enc a n1 k))`
  - Role `resp` (in `targetterms`):
    - `vars`: `(n1 text), (m mesg), (k akey)` | Role assumptions: none
    - `trace`: `(recv (enc n1 m k))` -> `(send m)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton targetterms (vars (n1 text) (k akey)) (defstrand init 2 (n1 n1) (k k)) (non-orig (invk k)) (uniq-orig n1))`
- **When to Reference This Example**: Reference this example to understand how CPSA resolves generic `mesg` variables (`m`) in decryptor/responder roles when an initiator's reception requires unifying two distinct nonce variables (`n1` and `n2`).
- **Key S-Expression Excerpt**:
```scheme
;; Solution requires the use of target terms in the solved filter.

;; The protocol is strange because the initiator sends out two texts
;; that turn out must be the same.

(defprotocol targetterms basic
  (defrole init (vars (a skey) (n1 n2 text) (k akey))
    (trace
     (send (enc n1 (enc a n2 k) k))
     (recv (enc a n1 k))))

  (defrole resp (vars (n1 text) (m mesg) (k akey))
    (trace
     (recv (enc n1 m k))
     (send m))))

(defskeleton targetterms
  (vars (n1 text) (k akey))
  (defstrand init 2 (n1 n1) (k k))
  (non-orig (invk k))
  (uniq-orig n1))
```

## targetterms2.scm

- **File Path**: `03_examples_scm/targetterms2.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Models a target-terms experiment (`targetterms2`) where `init` sends `(enc n (pubk a))` and expects triple-nested `(enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a))`, synthesized by chaining instances of a generic transformer role `trans` that receives `(enc n (pubk a))` and `m` and outputs `(enc n m (pubk a))`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `targetterms2`):
    - `vars`: `(a name), (n text)` | Role assumptions/annotations: `(uniq-orig n)`, `(non-orig (privk a))`
    - `trace`: `(send (enc n (pubk a)))` -> `(recv (enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a)))`
  - Role `trans` (in `targetterms2`):
    - `vars`: `(a name), (n text), (m mesg)` | Role assumptions: none
    - `trace`: `(recv (enc n (pubk a)))` -> `(recv m)` -> `(send (enc n m (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton targetterms2 (vars (a name) (n text)) (defstrand init 2 (a a) (n n)))`
- **When to Reference This Example**: Reference this example when analyzing protocols with recursive or chained wrapping/transforming roles that bind a generic `mesg` variable `m` across multiple strands.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol targetterms2 basic
  (defrole init (vars (a name) (n text))
    (trace
	(send (enc n (pubk a)))
      (recv (enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a)))
    )
    (uniq-orig n)
    (non-orig (privk a))
)
  (defrole trans (vars (a name) (n text) (m mesg))
    (trace
     (recv (enc n (pubk a)))
     (recv m)
     (send (enc n m (pubk a)))
    ))
)

(defskeleton targetterms2
  (vars (a name) (n text))
  (defstrand init 2 (a a) (n n))
)
```

## targetterms6.scm

- **File Path**: `03_examples_scm/targetterms6.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Extends `targetterms2` so `init` receives the concatenation of both the triple-wrapped and double-wrapped terms, exposing historical CPSA bugs in single-position critical message contractions and aggressive cohort pruning when multiple `trans` strands have differently bound `mesg` variables.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `targetterms6`):
    - `vars`: `(a name), (n text), (m mesg)` | Role assumptions/annotations: `(uniq-orig n)`, `(non-orig (privk a))`
    - `trace`: `(send (enc n (pubk a)))` -> `(recv (cat (enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a)) (enc n (enc n (pubk a)) (pubk a))))`
  - Role `trans` (in `targetterms6`):
    - `vars`: `(a name), (n text), (m mesg)` | Role assumptions: none
    - `trace`: `(recv (enc n (pubk a)))` -> `(recv m)` -> `(send (enc n m (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton targetterms6 (vars (a name) (n text)) (defstrand init 2 (a a) (n n)))`
    - `(defskeleton targetterms6 (vars (n text) (a name)) (defstrand init 2 (n n) (a a)) (defstrand trans 3 (m (enc n (pubk a))) (n n) (a a)) (defstrand trans 3 (m (enc n (enc n (pubk a)) (pubk a))) (n n) (a a)) (precedes ((0 0) (1 0)) ((0 0) (2 0)) ((1 2) (2 1)) ((2 2) (0 1))))`
- **When to Reference This Example**: Reference this example when debugging non-termination or missing shapes involving multiple instances of a generic forwarding/wrapping role with `mesg` variables.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol targetterms6 basic
  (defrole init (vars (a name) (n text) (m mesg))
    (trace
	(send (enc n (pubk a)))
      (recv (cat (enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a))
         (enc n (enc n (pubk a)) (pubk a)) ))
    )
    (uniq-orig n)
    (non-orig (privk a))
)
  (defrole trans (vars (a name) (n text) (m mesg))
    (trace
     (recv (enc n (pubk a)))
     (recv m)
     (send (enc n m (pubk a)))
    ))
)

(defskeleton targetterms6
  (vars (a name) (n text))
  (defstrand init 2 (a a) (n n))
)

(defskeleton targetterms6
  (vars (n text) (a name))
  (defstrand init 2 (n n) (a a))
  (defstrand trans 3 (m (enc n (pubk a))) (n n) (a a))
  (defstrand trans 3 (m (enc n (enc n (pubk a)) (pubk a))) (n n) (a a))
  (precedes ((0 0) (1 0)) ((0 0) (2 0)) ((1 2) (2 1)) ((2 2) (0 1)))
)
```

## targetterms8.scm

- **File Path**: `03_examples_scm/targetterms8.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Demonstrates the need for condition 2a in CPSA's solved predicate: `init` sends `(enc n1 (enc a n2 k) k)` and receives `(enc a n1 k)`, while `resp` receives `(enc n1 (enc m k) k)` and sends `(enc m k)`. Compares an initial POV with `n1, n2` distinct against a second POV where `n2` is pre-unified with `n1`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `targetterms8`):
    - `vars`: `(a name), (n1 n2 text), (k akey)` | Role assumptions/annotations: `(uniq-orig n1)`, `(non-orig (invk k))`
    - `trace`: `(send (enc n1 (enc a n2 k) k))` -> `(recv (enc a n1 k))`
  - Role `resp` (in `targetterms8`):
    - `vars`: `(n1 text), (m mesg), (k akey)` | Role assumptions: none
    - `trace`: `(recv (enc n1 (enc m k) k))` -> `(send (enc m k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton targetterms8 (vars (a name) (n1 n2 text) (k akey)) (defstrand init 2 (a a) (n1 n1) (n2 n2) (k k)))`
    - `(defskeleton targetterms8 (vars (a name) (n1 text) (k akey)) (defstrand init 2 (a a) (n1 n1) (n2 n1) (k k)))`
- **When to Reference This Example**: Reference this example when a protocol requires an initiator's own terms to unify (`n2 = n1`) via self-augmentation or when testing how nested encryptions `(enc n1 (enc m k) k)` interact with `mesg` variables.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol targetterms8 basic
  (defrole init (vars (a name) (n1 n2 text) (k akey))
    (trace
	(send (enc n1 (enc a n2 k) k))
      (recv (enc a n1 k))
    )
    (uniq-orig n1)
    (non-orig (invk k))
)
  (defrole resp (vars (n1 text) (m mesg) (k akey))
    (trace
     (recv (enc n1 (enc m k) k))
     (send (enc m k))
    ))
)

(comment First POV)
(defskeleton targetterms8
  (vars (a name) (n1 n2 text) (k akey))
  (defstrand init 2 (a a) (n1 n1) (n2 n2) (k k))
)

(comment Second POV)
(defskeleton targetterms8
  (vars (a name) (n1 text) (k akey))
  (defstrand init 2 (a a) (n1 n1) (n2 n1) (k k))
)

(comment "This is the shape.  We don't need it because we find it from the second POV.")
(comment (defskeleton targetterms8
  (vars (a name) (n1 text) (k akey) )
  (defstrand init 2 (a a) (n1 n1) (n2 n1) (k k))
  (defstrand resp 2 (n1 n1) (k k) (m (cat a n1)))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))))
```

## thisthat.scm

- **File Path**: `03_examples_scm/thisthat.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Needham-Schroeder Public-Key Protocol This-That Variant")` | Flags: none
- **Protocol & Purpose**: Models the Needham-Schroeder Public-Key Protocol 'This-That' variant (`thisthat`), where `init` sends one challenge `(enc n1 a (pubk b))` and receives two responses and two tagged confirmations (`"this"` and `"that"`), requiring concurrent participation of both `this` and `that` responder roles.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `thisthat`):
    - `vars`: `(a b name), (n1 n2 n3 text)` | Role assumptions: none
    - `trace`: `(send (enc n1 a (pubk b)))` -> `(recv (cat (enc n1 n2 (pubk a)) (enc n1 n3 (pubk a))))` -> `(recv (cat (enc "this" n2 (pubk b)) (enc "that" n3 (pubk b))))`
  - Role `this` (in `thisthat`):
    - `vars`: `(b a name), (n2 n1 text)` | Role assumptions/annotations: `(uniq-orig n2)`
    - `trace`: `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 (pubk a)))` -> `(send (enc "this" n2 (pubk b)))`
  - Role `that` (in `thisthat`):
    - `vars`: `(b a name), (n3 n1 text)` | Role assumptions/annotations: `(uniq-orig n3)`
    - `trace`: `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n3 (pubk a)))` -> `(send (enc "that" n3 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton thisthat (vars (a b name) (n1 text)) (defstrand init 3 (a a) (b b) (n1 n1)) (non-orig (privk b) (privk a)) (uniq-orig n1) (comment "Initiator point-of-view"))`
- **When to Reference This Example**: Reference this example when modeling protocols where a single initiator session interacts with multiple distinct responder roles (`this` and `that`) distinguished by string tags.
- **Key S-Expression Excerpt**:
```scheme
(herald "Needham-Schroeder Public-Key Protocol This-That Variant")

(defprotocol thisthat basic
  (defrole init
    (vars (a b name) (n1 n2 n3 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (cat (enc n1 n2 (pubk a)) (enc n1 n3 (pubk a))))
     (recv (cat (enc "this" n2 (pubk b)) (enc "that" n3 (pubk b))))))
  (defrole this
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 (pubk a)))
     (send (enc "this" n2 (pubk b))))
    (uniq-orig n2))
  (defrole that
    (vars (b a name) (n3 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n3 (pubk a)))
     (send (enc "that" n3 (pubk b))))
    (uniq-orig n3)))

;;; The initiator point-of-view
(defskeleton thisthat
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Initiator point-of-view"))
```

## tickle-unique.scm

- **File Path**: `03_examples_scm/tickle-unique.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald tickle-unique)` | Flags: none
- **Protocol & Purpose**: Models a public-key challenge-response protocol (`tickle`) equipped with a guarded rule `uniq-tickle` that asserts `(uniq nb0)` whenever `(fact guard-me)` holds and `resp` reaches length 2, contrasting unguarded vs. fact-guarded skeletons.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `tickle`):
    - `vars`: `(a b name), (na nb text)` | Role assumptions/annotations: `(uniq-orig na)`
    - `trace`: `(send (enc a na (pubk b)))` -> `(recv (enc b na na nb (pubk a)))` -> `(send nb)`
  - Role `resp` (in `tickle`):
    - `vars`: `(a b name), (na nb0 nb text)` | Role assumptions: none
    - `trace`: `(recv (enc a na (pubk b)))` -> `(send (enc b na nb0 nb (pubk a)))` -> `(recv nb)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `forall`, `herald`, `implies`, `non-orig`, `p`, `recv`, `send`, `trace`, `uniq`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Genrules (1)**:
    - `(defrule uniq-tickle ...)` in `tickle`: `(forall ((z strd) (nb0 text)) (implies (and (fact guard-me) (p "resp" z 2) (p "resp" "nb0" z nb0)) (uniq nb0)))`
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton tickle (vars (a b name) (na nb0 nb text)) (defstrand resp 3 (a a) (b b) (nb0 nb0) (nb nb)) (non-orig (privk a)) (uniq-orig nb))`
    - `(defskeleton tickle (vars (a b name) (na nb0 nb text)) (defstrand resp 3 (a a) (b b) (nb0 nb0) (nb nb)) (facts (guard-me)) (non-orig (privk a)) (uniq-orig nb))`
- **When to Reference This Example**: Reference this example to learn how to conditionally enable or disable a `(defrule ...)` in specific skeletons using a trigger fact like `(facts (guard-me))`.
- **Key S-Expression Excerpt**:
```scheme
(herald tickle-unique)

(defprotocol tickle basic
  (defrole init
    (vars (a b name) (na nb text))
    (trace
     (send (enc a na (pubk b)))
     (recv (enc b na na nb (pubk a)))
     (send nb))
    (uniq-orig na))

  (defrole resp
    (vars (a b name) (na nb0 nb text))
    (trace
     (recv (enc a na (pubk b)))
     (send (enc b na nb0 nb (pubk a)))
     (recv nb)))

  (defrule uniq-tickle
    (forall
     ((z strd) (nb0 text))
     (implies
      (and (fact guard-me)
	   (p "resp" z 2)
	   (p "resp" "nb0" z nb0))
      (uniq nb0)))))

(defskeleton tickle
  (vars (a b name) (na nb0 nb text))
  (defstrand resp 3 (a a) (b b) (nb0 nb0) (nb nb))
  (non-orig (privk a))
  (uniq-orig nb))

(defskeleton tickle
  (vars (a b name) (na nb0 nb text))
  (defstrand resp 3 (a a) (b b) (nb0 nb0) (nb nb))
  (facts (guard-me))
  (non-orig (privk a))
  (uniq-orig nb))
```

## timestamping.scm

- **File Path**: `03_examples_scm/timestamping.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald timestamping-service)` | Flags: none
- **Protocol & Purpose**: Models Bruce Schneier's linked Timestamping Service (`timestamping-service`, Applied Cryptography 2nd Ed., p.76) with roles `client`, `server`, `origin`, and `big-bang`, using macros `(link)` and `(timestamp l)` and double-wrapping `(enc (enc ... (privk trent)) (pubk trent))` to represent server state across linked timestamps.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `client` (in `timestamping-service`):
    - `vars`: `(alice alice_1 trent name), (n data), (h h_1 text), (t_1 l mesg)` | Role assumptions: none
    - `trace`: `(send (cat h alice))` -> `(recv (timestamp l))`
  - Role `server` (in `timestamping-service`):
    - `vars`: `(alice alice_1 trent name), (n data), (h h_1 text), (t_1 l_1 mesg)` | Role assumptions/annotations: `(uniq-orig n)`
    - `trace`: `(recv (cat (enc (enc (link) (privk trent)) (pubk trent)) h alice))` -> `(send (cat (timestamp (hash (link))) (enc (enc (hash alice h (timestamp (hash (link))) (hash (link))) (privk trent)) (pubk trent))))`
  - Role `origin` (in `timestamping-service`):
    - `vars`: `(alice alice_1 trent name), (n data), (h h_1 text), (t_1 l_1 text)` | Role assumptions: none
    - `trace`: `(recv (enc (enc n (privk trent)) (pubk trent)))` -> `(send (enc (enc alice h (timestamp (hash (link))) (hash (link)) (privk trent)) (pubk trent)))`
  - Role `big-bang` (in `timestamping-service`):
    - `vars`: `(n data), (trent name)` | Role assumptions/annotations: `(uniq-orig n)`
    - `trace`: `(send (enc (enc n (privk trent)) (pubk trent)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(link)` -> `(cat alice_1 h_1 t_1 l_1)`; `(timestamp l)` -> `(enc n alice h alice_1 h_1 t_1 l (privk trent))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton timestamping-service (vars (trent name) (n_0 data)) (defstrand client 2 (trent trent)) (non-orig (privk trent)))`
- **When to Reference This Example**: Reference this example when modeling hash-chain or linked-timestamping protocols, or when encoding server state as self-encrypted signed tokens `(enc (enc state (privk s)) (pubk s))` in message-passing basic algebra.
- **Key S-Expression Excerpt**:
```scheme
(defmacro (link)
  (cat alice_1 h_1 t_1 l_1))

(defmacro (timestamp l)
  (enc n alice h alice_1 h_1 t_1 l (privk trent)))

(defprotocol timestamping-service basic
  (defrole client (vars (alice alice_1 trent name)
  			(n data) (h h_1 text) (t_1 l mesg))
    (trace
     (send (cat h alice))
     (recv (timestamp l))))
  (defrole server (vars (alice alice_1 trent name)
			(n data) (h h_1 text) (t_1 l_1 mesg))
    (trace
     (recv (cat (enc (enc (link) (privk trent)) (pubk trent)) h alice))
     (send (cat (timestamp (hash (link)))
		(enc
		 (enc (hash alice h (timestamp (hash (link))) (hash (link)))
		      (privk trent))
		 (pubk trent)))))
    (uniq-orig n))
  (defrole origin (vars (alice alice_1 trent name)
  			(n data) (h h_1 text) (t_1 l_1 text))
    (trace
     (recv (enc (enc n (privk trent)) (pubk trent)))
     (send (enc
	    (enc alice h (timestamp (hash (link))) (hash (link))
		 (privk trent))
	    (pubk trent)))))
  (defrole big-bang (vars (n data) (trent name))
    (trace (send (enc (enc n (privk trent)) (pubk trent))))
    (uniq-orig n)))

(defskeleton timestamping-service
  (vars (trent name) (n_0 data))
  (defstrand client 2 (trent trent))
  (non-orig (privk trent)))
```

## trust-anchor.scm

- **File Path**: `03_examples_scm/trust-anchor.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald trust-anchor (comment "Tests rule application on initial skeleton"))` | Flags: `(comment "Tests rule application on initial skeleton")`
- **Protocol & Purpose**: Minimal roleless protocol (`trust-anchor`) testing rule application on the initial skeleton: defines `(defrule trust-anchor-inverse-is-non ...)` which deduces `(non (invk k))` from `(fact trust-anchor k)`, and compares a skeleton with explicit `(non-orig (privk ca))` against one with `(facts (trust-anchor (pubk ca)))`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Protocol `trust-anchor` (`basic`): No `(defrole ...)` declarations (roleless rule-testing protocol).
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `deflistener`, `defprotocol`, `defrule`, `defskeleton`, `fact`, `facts`, `forall`, `herald`, `implies`, `non`, `non-orig`, `vars`
  - **Macros**: None.
  - **Rules & Genrules (1)**:
    - `(defrule trust-anchor-inverse-is-non ...)` in `trust-anchor`: `(forall ((k akey)) (implies (fact trust-anchor k) (non (invk k))))`
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton trust-anchor (vars (f ca name)) (deflistener (enc f (pubk f) (privk ca))) (non-orig (privk ca)))`
    - `(defskeleton trust-anchor (vars (f ca name)) (deflistener (enc f (pubk f) (privk ca))) (facts (trust-anchor (pubk ca))))`
- **When to Reference This Example**: Reference this example when modeling PKI trust anchors or custom security assumptions via `(facts ...)` that entail `(non ...)` through a `(defrule ...)`.
- **Key S-Expression Excerpt**:
```scheme
(herald trust-anchor
	(comment "Tests rule application on initial skeleton"))

(defprotocol trust-anchor basic
  ;;; trust-anchor property guarantees non
  (defrule trust-anchor-inverse-is-non
    (forall ((k akey))
	    (implies (fact trust-anchor k)
		     (non (invk k))))))

(defskeleton trust-anchor
  (vars (f ca name))
  (deflistener (enc f (pubk f) (privk ca)))
  (non-orig (privk ca)))

(defskeleton trust-anchor
  (vars (f ca name))
  (deflistener (enc f (pubk f) (privk ca)))
  (facts (trust-anchor (pubk ca))))
```

## ugen-at.scm

- **File Path**: `03_examples_scm/ugen-at.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald uniq-at)` | Flags: none
- **Protocol & Purpose**: Models the Yahalom protocol (`yahalom-plus-uniq-at`) using `(uniq-gen ...)` for keys and nonces and includes two rules (`uniq-at` and `ugen-at`) that match the strand-location predicates `(uniq-at v z i)` and `(ugen-at v z i)` and record them as facts `(fact remember v z)` and `(fact remember-gen v z)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom-plus-uniq-at`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (enc b k n-a n-b (ltk a c)))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom-plus-uniq-at`):
    - `vars`: `(b a c name), (n-a n-b text), (rest mesg), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b c))))` -> `(recv (cat (enc a k (ltk b c)) rest))` -> `(send rest)` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom-plus-uniq-at`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-gen k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b c))))` -> `(send (cat (enc a k (ltk b c)) (enc b k n-a n-b (ltk a c))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `deflistener`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `forall`, `herald`, `implies`, `non-orig`, `recv`, `send`, `trace`, `ugen-at`, `uniq-at`, `uniq-gen`, `vars`
  - **Macros**: None.
  - **Rules & Genrules (2)**:
    - `(defrule uniq-at ...)` in `yahalom-plus-uniq-at`: `(forall ((z strd) (i indx) (v mesg)) (implies (uniq-at v z i) (fact remember v z)))`
    - `(defrule ugen-at ...)` in `yahalom-plus-uniq-at`: `(forall ((z strd) (i indx) (v mesg)) (implies (ugen-at v z i) (fact remember-gen v z)))`
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton yahalom-plus-uniq-at (vars (a b c name) (n-b text) (k skey)) (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk b c) (ltk a c)) (uniq-gen n-b))`
    - `(defskeleton yahalom-plus-uniq-at (vars (a b c name) (n-a text)) (defstrand init 3 (n-a n-a) (a a) (b b) (c c)) (non-orig (ltk b c) (ltk a c)) (uniq-gen n-a))`
- **When to Reference This Example**: Reference this example when writing `(defrule ...)` formulas that inspect the exact strand and node index where a value is uniquely generated (`(ugen-at v z i)`) or uniquely originated (`(uniq-at v z i)`).
- **Key S-Expression Excerpt**:
```scheme
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey))
    (trace (recv (cat b (enc a n-a n-b (ltk b c))))
	   (send (cat (enc a k (ltk b c))
		      (enc b k n-a n-b (ltk a c)))))
    (uniq-gen k))

  (defrule uniq-at
    (forall
     ((z strd) (i indx) (v mesg))
     (implies (uniq-at v z i)
	      (fact remember v z))))

  (defrule ugen-at
    (forall
     ((z strd) (i indx) (v mesg))
     (implies (ugen-at v z i)
	      (fact remember-gen v z)))))

(defskeleton yahalom-plus-uniq-at
  (vars (a b c name) (n-b text) (k skey))
  (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk b c) (ltk a c))
  (uniq-gen n-b))

(defskeleton yahalom-plus-uniq-at
  (vars (a b c name) (n-a text))
  (defstrand init 3 (n-a n-a) (a a) (b b) (c c))
  (non-orig (ltk b c) (ltk a c))
  (uniq-gen n-a))

```

## ugo.scm

- **File Path**: `03_examples_scm/ugo.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald uniq-gen-and-orig-example (comment "Non-executable role examples"))` | Flags: `(comment "Non-executable role examples")`
- **Protocol & Purpose**: Defines three diagnostic protocols (`uniq-gen-example`, `uniq-gen-example-alt`, `uniq-orig-example`) illustrating non-executable role specifications where an asymmetric key `u` and its inverse `(invk u)` are generated or originated across strands in ways that require a responder to magically compute `(invk u)` from `u`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `uniq-gen-example`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(uniq-gen u)`, `(non-orig k)`
    - `trace`: `(send (enc u k))` -> `(recv (invk u))` -> `(send u)`
  - Role `resp` (in `uniq-gen-example`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc u k))` -> `(send (invk u))` -> `(recv u)`
  - Role `init` (in `uniq-gen-example-alt`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(uniq-gen (invk u))`, `(non-orig k)`
    - `trace`: `(send (enc (invk u) k))` -> `(recv u)` -> `(send u)`
  - Role `resp` (in `uniq-gen-example-alt`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc (invk u) k))` -> `(send u)` -> `(recv u)`
  - Role `init` (in `uniq-orig-example`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(uniq-orig u)`, `(non-orig k)`
    - `trace`: `(send (enc u k))` -> `(recv (invk u))` -> `(send u)`
  - Role `resp` (in `uniq-orig-example`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc u k))` -> `(send (invk u))` -> `(recv u)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (6)**:
    - `(defskeleton uniq-gen-example (vars) (defstrandmax resp) (comment "How is the responder able to send (invk u)?"))`
    - `(defskeleton uniq-gen-example (vars (u akey)) (defstrandmax resp (u u)) (uniq-gen (invk u)) (comment "How is the responder able to send (invk u)?"))`
    - `(defskeleton uniq-gen-example-alt (vars) (defstrandmax resp) (comment "How is the responder able to send (invk u)?"))`
    - `(defskeleton uniq-gen-example-alt (vars (u akey)) (defstrandmax resp (u u)) (uniq-gen (invk u)) (comment "How is the responder able to send (invk u)?"))`
    - `(defskeleton uniq-orig-example (vars) (defstrandmax resp))`
    - `(defskeleton uniq-orig-example (vars (u akey)) (defstrandmax resp (u u)) (uniq-orig (invk u)))`
- **When to Reference This Example**: Reference this example to understand CPSA's semantics for asymmetric key pair generation (`uniq-gen` vs `uniq-orig` on `u` and `(invk u)`) and why specifiers must ensure roles do not use unreceived private keys.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol uniq-gen-example basic
  (defrole init
    (vars (u akey) (k skey))
    (trace
     (send (enc u k))
     (recv (invk u))
     (send u))
    (uniq-gen u)
    (non-orig k)
    (comment
     "Instances of this role generate u and (invk u)"
     "at their first event."))
  (defrole resp
    (vars (u akey) (k skey))
    (trace
     (recv (enc u k))
     (send (invk u))
     (recv u))
    (non-orig k)
    (comment
     "Instances of this role appear to generate (invk u)"
     "at their second event.")))

(defskeleton uniq-gen-example
  (vars)
  (defstrandmax resp)
  (comment "How is the responder able to send (invk u)?"))

(defskeleton uniq-gen-example
  (vars (u akey))
  (defstrandmax resp (u u))
  (uniq-gen (invk u))
  (comment "How is the responder able to send (invk u)?"))

```

## uncarried_keys.scm

- **File Path**: `03_examples_scm/uncarried_keys.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Illustrates a subtlety of `uniq-orig` vs. fresh generation (`uncarried-keys`): `init` declares `(uniq-orig a K)` and sends `K` in its 3rd event (node index 2), yet `resp` can use `K` in a non-carried encryption key position before `K` is ever transmitted if `K` is only `uniq-orig` rather than `uniq-gen`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `uncarried-keys`):
    - `vars`: `(a text), (A B name), (K akey)` | Role assumptions/annotations: `(non-orig (privk B) (invk K))`, `(uniq-orig a K)`
    - `trace`: `(send (enc "start" a A B (pubk B)))` -> `(recv (enc a A B (pubk A)))` -> `(send (enc a K (pubk B)))` -> `(recv (enc a A B K))`
  - Role `resp` (in `uncarried-keys`):
    - `vars`: `(a text), (A B name), (K akey)` | Role assumptions: none
    - `trace`: `(recv (enc "start" a A B (pubk B)))` -> `(send (enc a A B (pubk A)))` -> `(recv (enc a K (pubk B)))` -> `(send (enc a A B K))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton uncarried-keys (vars (a text) (A B name) (K akey)) (defstrand init 4 (a a) (A A) (B B) (K K)))`
- **When to Reference This Example**: Reference this example to understand why keys generated during a protocol run should be declared `uniq-gen` (or why `uniq-orig` alone allows a key to be used in encryption-key position prior to its first carried transmission).
- **Key S-Expression Excerpt**:
```scheme
; uncarried-keys
;   Shows that our notion of uniquely-originating
; does not necessarily correspond to the notion of
; a freshly-generated nonce, because such values can
; be used in non-carried positions before they are
; received.  Here, the initiator originates K in its
; 4th message but receives (earlier) a message
; encrypted with K from the responder.

(defprotocol uncarried-keys basic
  (defrole init
    (vars (a text) (A B name) (K akey))
    (trace
     (send (enc "start" a A B (pubk B)))
     (recv (enc a A B (pubk A)))
     (send (enc a K (pubk B)))
     (recv (enc a A B K)))
    (non-orig (privk B) (invk K))
    (uniq-orig a K))
  (defrole resp
    (vars (a text) (A B name) (K akey))
    (trace
     (recv (enc "start" a A B (pubk B)))
     (send (enc a A B (pubk A)))
     (recv (enc a K (pubk B)))
     (send (enc a A B K)))))

(defskeleton uncarried-keys
  (vars (a text) (A B name) (K akey))
  (defstrand init 4 (a a) (A A) (B B) (K K)))
```

## unilateral.scm

- **File Path**: `03_examples_scm/unilateral.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald unilateral)` | Flags: none
- **Protocol & Purpose**: Presents two unilateral authentication protocols (`unilateral` and `iso-unilateral` from ISO/IEC JTC 1/SC 27/WG 2 N1050) and formulates their security properties both as POV skeletons (`defskeleton`) and as explicit first-order security goals (`defgoal`), including a deliberately false goal to demonstrate counterexample shape generation.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `unilateral`):
    - `vars`: `(n text), (k akey)` | Role assumptions/annotations: `(uniq-orig n)`
    - `trace`: `(send (enc n k))` -> `(recv n)`
  - Role `resp` (in `unilateral`):
    - `vars`: `(n text), (k akey)` | Role assumptions: none
    - `trace`: `(recv (enc n k))` -> `(send n)`
  - Role `resp` (in `iso-unilateral`):
    - `vars`: `(na nb t1 t2 t3 text), (b name)` | Role assumptions/annotations: `(uniq-orig na)`
    - `trace`: `(recv (cat nb t1))` -> `(send (cat na nb b t3 (enc na nb b t2 (privk b))))`
  - Role `init` (in `iso-unilateral`):
    - `vars`: `(na nb t1 t2 t3 text), (b name)` | Role assumptions/annotations: `(uniq-orig nb)`
    - `trace`: `(send (cat nb t1))` -> `(recv (cat na nb b t3 (enc na nb b t2 (privk b))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `and`, `comment`, `defgoal`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `exists`, `false`, `forall`, `herald`, `implies`, `non`, `non-orig`, `p`, `pen-non-orig`, `pnon`, `prec`, `recv`, `send`, `trace`, `uniq-at`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals (4)**:
    - `(defgoal unilateral (forall ((n text) (k akey) (z strd)) (implies (and (p "init" z 2) (p "init" "n" z n) (p "init" "k" z k) (non (invk k)) (uniq-at n z 0)) (exists ((z-0 strd)) (and (p "resp" z-0 2) (p "resp" "n" z-0 n) (p "resp" "k" z-0 k) (prec z 0 z-0 0) (prec z-0 1 z 1))))))`
    - `(defgoal unilateral (forall ((n text) (k akey) (z strd)) (implies (and (p "resp" z 2) (p "resp" "n" z n) (p "resp" "k" z k) (non (invk k)) (pnon n)) (exists ((k-0 akey) (z-0 strd)) (and (p "init" z-0 1) (p "init" "n" z-0 n) (p "init" "k" z-0 k-0) (prec z-0 0 z 0) (uniq-at n z-0 0))))))`
    - `(defgoal iso-unilateral (forall ((b name) (z strd)) (implies (and (p "init" z 2) (p "init" "b" z b) (non (privk b))) (exists ((y strd)) (and (p "resp" y 2) (p "resp" "b" y b))))))`
    - `(defgoal iso-unilateral (forall ((b name) (z strd)) (implies (and (p "init" z 2) (p "init" "b" z b) (non (privk b))) (false))))`
  - **Skeletons (3)**:
    - `(defskeleton unilateral (vars (k akey)) (defstrand init 2 (k k)) (non-orig (invk k)))`
    - `(defskeleton unilateral (vars (n text) (k akey)) (defstrand resp 2 (n n) (k k)) (pen-non-orig n) (non-orig (invk k)))`
    - `(defskeleton iso-unilateral (vars (b name)) (defstrand init 2 (b b)) (non-orig (privk b)))`
- **When to Reference This Example**: Reference this example when writing `(defgoal ...)` authentication and secrecy theorems using `forall`, `implies`, `exists`, `p`, `prec`, `non`, `pnon`, and `uniq-at`.
- **Key S-Expression Excerpt**:
```scheme
;;; The same two problems posed using security goals.  The goals were
;;; taken from the output of cpsasas.

(defgoal unilateral
  (forall ((n text) (k akey) (z strd))
    (implies
      (and (p "init" z 2) (p "init" "n" z n) (p "init" "k" z k)
        (non (invk k)) (uniq-at n z 0))
      (exists ((z-0 strd))
        (and (p "resp" z-0 2) (p "resp" "n" z-0 n) (p "resp" "k" z-0 k)
          (prec z 0 z-0 0) (prec z-0 1 z 1))))))

(defgoal unilateral
  (forall ((n text) (k akey) (z strd))
    (implies
      (and (p "resp" z 2) (p "resp" "n" z n) (p "resp" "k" z k)
        (non (invk k)) (pnon n))
      (exists ((k-0 akey) (z-0 strd))
        (and (p "init" z-0 1) (p "init" "n" z-0 n)
          (p "init" "k" z-0 k-0) (prec z-0 0 z 0) (uniq-at n z-0 0))))))

;;; Unilateral authentication from ISO/IEC JTC 1/SC 27/WG 2 N1050

(defprotocol iso-unilateral basic
  (defrole resp
    (vars (na nb t1 t2 t3 text) (b name))
    (trace
     (recv (cat nb t1))
     (send (cat na nb b t3 (enc na nb b t2 (privk b)))))
    (uniq-orig na))
  (defrole init
    (vars (na nb t1 t2 t3 text) (b name))
    (trace
     (send (cat nb t1))
     (recv (cat na nb b t3 (enc na nb b t2 (privk b)))))
    (uniq-orig nb))
  (comment "Two pass authentication"))

(defskeleton iso-unilateral
```

## uniq-at.scm

- **File Path**: `03_examples_scm/uniq-at.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald uniq-at)` | Flags: none
- **Protocol & Purpose**: Companion to `ugen-at.scm` that models `yahalom-plus-uniq-at` using `(uniq-orig ...)` instead of `(uniq-gen ...)` on the server key `k` and skeleton nonces `n-b`, `n-a`, firing the `uniq-at` rule to record `(fact remember v z)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom-plus-uniq-at`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (enc b k n-a n-b (ltk a c)))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom-plus-uniq-at`):
    - `vars`: `(b a c name), (n-a n-b text), (rest mesg), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b c))))` -> `(recv (cat (enc a k (ltk b c)) rest))` -> `(send rest)` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom-plus-uniq-at`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b c))))` -> `(send (cat (enc a k (ltk b c)) (enc b k n-a n-b (ltk a c))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `deflistener`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `forall`, `herald`, `implies`, `non-orig`, `recv`, `send`, `trace`, `ugen-at`, `uniq-at`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Genrules (2)**:
    - `(defrule uniq-at ...)` in `yahalom-plus-uniq-at`: `(forall ((z strd) (i indx) (v mesg)) (implies (uniq-at v z i) (fact remember v z)))`
    - `(defrule ugen-at ...)` in `yahalom-plus-uniq-at`: `(forall ((z strd) (i indx) (v mesg)) (implies (ugen-at v z i) (fact remember-gen v z)))`
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton yahalom-plus-uniq-at (vars (a b c name) (n-b text) (k skey)) (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
    - `(defskeleton yahalom-plus-uniq-at (vars (a b c name) (n-a text)) (defstrand init 3 (n-a n-a) (a a) (b b) (c c)) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-a))`
- **When to Reference This Example**: Reference this example alongside `ugen-at.scm` to compare how `(uniq-at v z i)` and `(ugen-at v z i)` behave in `defrule` triggers under `uniq-orig` vs. `uniq-gen`.
- **Key S-Expression Excerpt**:
```scheme
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey))
    (trace (recv (cat b (enc a n-a n-b (ltk b c))))
	   (send (cat (enc a k (ltk b c))
		      (enc b k n-a n-b (ltk a c)))))
    (uniq-orig k))

  (defrule uniq-at
    (forall
     ((z strd) (i indx) (v mesg))
     (implies (uniq-at v z i)
	      (fact remember v z))))

  (defrule ugen-at
    (forall
     ((z strd) (i indx) (v mesg))
     (implies (ugen-at v z i)
	      (fact remember-gen v z)))))

(defskeleton yahalom-plus-uniq-at
  (vars (a b c name) (n-b text) (k skey))
  (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))

(defskeleton yahalom-plus-uniq-at
  (vars (a b c name) (n-a text))
  (defstrand init 3 (n-a n-a) (a a) (b b) (c c))
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-a))

```

## uniq-gen-test.scm

- **File Path**: `03_examples_scm/uniq-gen-test.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Unique generation test protocols." (comment "Skeletons 2, 4, and 7 should have no shapes."))` | Flags: `(comment "Skeletons 2, 4, and 7 should have no shapes.")`
- **Protocol & Purpose**: Tests `uniq-gen` vs. `non-orig` on a symmetric key `k` in `uniqgentest` with roles `init`, `doubler`, and `resp`. When `k` is `uniq-gen` in the `init` skeleton, `doubler` cannot participate because `doubler` would also generate `k` (yielding a dead skeleton); when `k` is merely `non-orig`, `doubler` can supply `(enc a a k)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `uniqgentest`):
    - `vars`: `(a name), (k skey)` | Role assumptions: none
    - `trace`: `(send (enc a k))` -> `(recv (enc a a k))`
  - Role `doubler` (in `uniqgentest`):
    - `vars`: `(a name), (k skey)` | Role assumptions: none
    - `trace`: `(send (enc a a k))`
  - Role `resp` (in `uniqgentest`):
    - `vars`: `(a name), (k skey)` | Role assumptions: none
    - `trace`: `(recv (enc a k))` -> `(send (enc a a k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton uniqgentest (vars (k skey)) (defstrand init 2 (k k)) (uniq-gen k))`
    - `(defskeleton uniqgentest (vars (k skey)) (defstrand init 2 (k k)) (non-orig k))`
- **When to Reference This Example**: Reference this example to understand how `(uniq-gen k)` prevents key-generating helper roles from independently using `k` without receiving it, whereas `(non-orig k)` permits pre-shared key usage across roles.
- **Key S-Expression Excerpt**:
```scheme
(herald "Unique generation test protocols."
	(comment "Skeletons 2, 4, and 7 should have no shapes."))

(defprotocol uniqgentest basic
  (defrole init
    (vars (a name) (k skey))
    (trace
     (send (enc a k))
     (recv (enc a a k))))
  (defrole doubler
    (vars (a name) (k skey))
    (trace
     (send (enc a a k))))
  (defrole resp
    (vars (a name) (k skey))
    (trace
     (recv (enc a k))
     (send (enc a a k)))))

;; This input should have no shape, because
;; declaring k to be uniq-gen does not allow
;; a doubler strand: the doubler strand generates
;; its key.
(defskeleton uniqgentest
  (vars (k skey))
  (defstrand init 2 (k k))
  (uniq-gen k))

;; This input should have a shape in which a
;; doubler produces the message needed by the
;; initiator.
(defskeleton uniqgentest
  (vars (k skey))
  (defstrand init 2 (k k))
  (non-orig k))
```

## uo.scm

- **File Path**: `03_examples_scm/uo.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Minimal two-role protocol (`uniq-orig`) showing that declaring `(uniq-orig n)` in `init` (which sends `n`) does not prevent `resp` from sending `(enc m n)` before receiving `n`, because `n` appears only in the non-carried key position of `(enc m n)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `uniq-orig`):
    - `vars`: `(n text)` | Role assumptions/annotations: `(uniq-orig n)`
    - `trace`: `(send n)`
  - Role `resp` (in `uniq-orig`):
    - `vars`: `(m n text)` | Role assumptions: none
    - `trace`: `(send (enc m n))` -> `(recv n)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton uniq-orig (vars (n text)) (defstrand init 1 (n n)) (defstrand resp 2 (n n)))`
- **When to Reference This Example**: Reference this example for the simplest possible demonstration of why `uniq-orig` only constrains where a term is first *carried* (not where it is first used as an encryption key).
- **Key S-Expression Excerpt**:
```scheme
; uniq-orig
;   Shows that our notion of uniquely-originating
; does not necessarily correspond to the notion of
; a freshly-generated nonce, because such values can
; be used in non-carried positions before they are
; received.  Here, the initiator originates n in its
; message but no problem is detected with a responder
; that sends a message encrypted under n as its first
; message, before receiving n.

(defprotocol uniq-orig basic
  (defrole init
    (vars (n text))
    (trace (send n))
    (uniq-orig n))
  (defrole resp
    (vars (m n text))
    (trace
     (send (enc m n))
     (recv n))))

(defskeleton uniq-orig
  (vars (n text))
  (defstrand init 1 (n n))
  (defstrand resp 2 (n n)))
```

## wang-hash.scm

- **File Path**: `03_examples_scm/wang-hash.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Wang's Fair Exchange Protocol" (bound 10))` | Flags: `(bound 10)`
- **Protocol & Purpose**: Models Wang's Fair Exchange Protocol (`wang`) with 14 roles (`init1`–`init5`, `resp1`–`resp3`, `ttp-ab1`–`ttp-ab2`, `ttp-rc1`–`ttp-rc2`, `ttp-cf1`–`ttp-cf2`), 14 macros (`em`, `l-prime`, `l-star`, `eoo-star`, `eor-star`, `rr-star`, `at-star`, `ek`, `l`, `l-prime-prime`, `eoo-prime-prime`, `eor-prime-prime`, `rr-prime-prime`, `cf-prime-prime`), and 12 skeletons proving Lemmas 4.1, 4.2, and 4.3 using built-in `(hash ...)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init1` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (cat k r))`
  - Role `init2` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (enc "abcf" (enc "abrq" (l) (privk "sign" a)) (privk "sign" t)))`
  - Role `init3` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))`
  - Role `init4` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (enc "abcf" (enc "abrq" (l) (privk "sign" a)) (privk "sign" t)))`
  - Role `init5` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))`
  - Role `resp1` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (eor-star (hash k) (enc m k) (ek (l))))` -> `(recv (cat k r))`
  - Role `resp2` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l))) (eor-star (hash k) (enc m k) (ek (l)))))` -> `(send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l))) (eor-star (hash k) (enc m k) (ek (l))) (enc "rcrq" (l) (ek (l)) (privk "sign" b))))` -> `(recv (cat k r))`
  - Role `resp3` (in `wang`):
    - `vars`: `(a b t hash_id name), (e1 e2 x mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l-star e1 x) e1 e2 (eoo-star x e1 e2)))` -> `(send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2)))` -> `(send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2) (enc "rcrq" (l-star e1 x) e2 (privk "sign" b))))` -> `(recv (enc "abcf" (enc "abrq" (l-star e1 x) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-ab1` (in `wang`):
    - `vars`: `(a b t hash_id name), (y x mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (enc "abrq" (l-prime y x) (privk "sign" a)))` -> `(send (cat "sync-abrq" (enc "abrq" (l-prime y x) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-ab2` (in `wang`):
    - `vars`: `(a b t hash_id name), (y x e mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (enc "abrq" (l-prime y x) (privk "sign" a)))` -> `(recv (cat "sync-abrq" (enc "eortag" (hash (l-prime y x)) e (privk "sign" b))))` -> `(send (enc "eortag" (hash (l-prime y x)) e (privk "sign" b)))`
  - Role `ttp-rc1` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (rr-prime-prime y))` -> `(send (cat "sync-rc-req" (rr-prime-prime y)))` -> `(send (cat k r))`
  - Role `ttp-rc2` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (rr-prime-prime y))` -> `(recv (cat "sync-rc-req" (enc "abrq" (l-prime-prime y) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime-prime y) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-cf1` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cf-prime-prime y))` -> `(send (cat "sync-cf-req" (cf-prime-prime y)))` -> `(send (enc (cf-prime-prime y) (privk "sign" t)))`
  - Role `ttp-cf2` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cf-prime-prime y))` -> `(recv (cat "sync-cf-req" (enc "abrq" (l-prime-prime y) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime-prime y) (privk "sign" a)) (privk "sign" t)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `comment`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (14)**: `(em)` -> `(enc m k)`; `(l-prime y x)` -> `(cat a b t y x)`; `(l-star e1 x)` -> `(l-prime (hash e1) x)`; `(eoo-star x e1 e2)` -> `(enc (cat "eootag" (hash (l-star e1 x)) e2) (privk "sign" a))`; `(eor-star x e1 e2)` -> `(enc (cat "eortag" (hash (l-star e1 x)) e2) (privk "sign" b))`; `(rr-star x e1 e2)` -> `(cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2) (enc (cat "rcrq" (l-star e1 x) e2) (privk "sign" b)))`; `(at-star e1 x)` -> `(enc (enc "abrq" (l-star e1 x) (privk "sign" a)) (privk "sign" t))`; `(ek l)` -> `(enc (cat "keytag" (hash l) k r) (pubk "encr" t))`; `(l)` -> `(l-prime (hash (enc m k)) (hash k))`; `(l-prime-prime y)` -> `(cat a b t y (hash k))`; `(eoo-prime-prime y)` -> `(enc (cat "eootag" (hash (l-prime-prime y)) (ek (l-prime-prime y))) (privk "sign" a))`; `(eor-prime-prime y)` -> `(enc (cat "eortag" (hash (l-prime-prime y)) (ek (l-prime-prime y))) (privk "sign" b))`; `(rr-prime-prime y)` -> `(cat (l-prime-prime y) (ek (l-prime-prime y)) (eoo-prime-prime y) (eor-prime-prime y) (enc "rcrq" (l-prime-prime y) (ek (l-prime-prime y)) (privk "sign" b)))`; `(cf-prime-prime y)` -> `(cat (l-prime-prime y) (ek (l-prime-prime y)) (eoo-prime-prime y) (eor-prime-prime y) (enc "cfrq" (l-prime-prime y) (ek (l-prime-prime y)) (privk "sign" b)))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (12)**:
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 1 (b b) (t t) (m m) (r r) (k k)) (deflistener m) (non-orig (privk "encr" t)) (uniq-orig m k) (comment "Experiment 1 to prove Lemma 4.1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 1 (b b) (t t) (m m) (r r) (k k)) (deflistener k) (non-orig (privk "encr" t)) (uniq-orig m k) (comment "Experiment 2 to prove Lemma 4.1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 3 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "First of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init3 3 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "Second of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init5 4 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "Third of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand resp1 3 (a a) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" a)) (comment "First of two experiments to prove Lemma 4.2, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand resp2 4 (a a) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" a)) (comment "Second of two experiments to prove Lemma 4.2, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (e1 e2 x mesg)) (defstrand resp3 4 (a a) (t t)) (non-orig (privk "sign" a)) (comment "Experiments to prove Lemma 4.2, clause 3."))`
    - `(defskeleton wang (vars (a b t hash_id name) (y x mesg)) (deflistener (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a)) (privk "sign" t))) (non-orig (privk "sign" t)) (comment "Experiments to prove Lemma 4.3, clause 1."))`
    - `(defskeleton wang (vars (y x mesg) (a b t name)) (defstrand ttp-ab1 3 (y y) (x x) (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 1 to prove Lemma 4.3, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (r text) (k skey) (y mesg)) (defstrand ttp-rc2 3 (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 2 to prove Lemma 4.3, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (r text) (k skey) (y mesg)) (defstrand ttp-cf2 3 (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 3 to prove Lemma 4.3, clause 2."))`
- **When to Reference This Example**: Reference this example when modeling complex optimistic fair-exchange protocols with a Trusted Third Party (TTP), abort/recovery/confirmation subprotocols, and deep macro composition.
- **Key S-Expression Excerpt**:
```scheme

  ;; Successful initiator run with no TTP involvement

  (defrole init1
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (recv (eor-star (hash k) (enc m k) (ek (l))))
     (send (cat k r)))
    (non-orig (privk hash_id)))

  ;; Aborted initiator run

  (defrole init2
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (enc "abcf"
                (enc "abrq" (l) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; Initiator run with abort request and forced recovery

  (defrole init3
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (eor-star (hash k) (enc m k) (ek (l)))))
    (non-orig (privk hash_id)))

```

## wang-key-hash.scm

- **File Path**: `03_examples_scm/wang-key-hash.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Wang's Fair Exchange Protocol" (bound 10))` | Flags: `(bound 10)`
- **Protocol & Purpose**: Variant of `wang-hash.scm` for Wang's Fair Exchange Protocol that overrides `(hash x)` via `(defmacro (hash x) (enc "h" (cat "h" x)))` to model hashing as symmetric encryption under literal tag `"h"` instead of the built-in `hash` constructor.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init1` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (cat k r))`
  - Role `init2` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (enc "abcf" (enc "abrq" (l) (privk "sign" a)) (privk "sign" t)))`
  - Role `init3` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))`
  - Role `init4` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (enc "abcf" (enc "abrq" (l) (privk "sign" a)) (privk "sign" t)))`
  - Role `init5` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))`
  - Role `resp1` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (eor-star (hash k) (enc m k) (ek (l))))` -> `(recv (cat k r))`
  - Role `resp2` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l))) (eor-star (hash k) (enc m k) (ek (l)))))` -> `(send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l))) (eor-star (hash k) (enc m k) (ek (l))) (enc "rcrq" (l) (ek (l)) (privk "sign" b))))` -> `(recv (cat k r))`
  - Role `resp3` (in `wang`):
    - `vars`: `(a b t hash_id name), (e1 e2 x mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l-star e1 x) e1 e2 (eoo-star x e1 e2)))` -> `(send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2)))` -> `(send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2) (enc "rcrq" (l-star e1 x) e2 (privk "sign" b))))` -> `(recv (enc "abcf" (enc "abrq" (l-star e1 x) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-ab1` (in `wang`):
    - `vars`: `(a b t hash_id name), (y x mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (enc "abrq" (l-prime y x) (privk "sign" a)))` -> `(send (cat "sync-abrq" (enc "abrq" (l-prime y x) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-ab2` (in `wang`):
    - `vars`: `(a b t hash_id name), (y x e mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (enc "abrq" (l-prime y x) (privk "sign" a)))` -> `(recv (cat "sync-abrq" (enc "eortag" (hash (l-prime y x)) e (privk "sign" b))))` -> `(send (enc "eortag" (hash (l-prime y x)) e (privk "sign" b)))`
  - Role `ttp-rc1` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (rr-prime-prime y))` -> `(send (cat "sync-rc-req" (rr-prime-prime y)))` -> `(send (cat k r))`
  - Role `ttp-rc2` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (rr-prime-prime y))` -> `(recv (cat "sync-rc-req" (enc "abrq" (l-prime-prime y) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime-prime y) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-cf1` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cf-prime-prime y))` -> `(send (cat "sync-cf-req" (cf-prime-prime y)))` -> `(send (enc (cf-prime-prime y) (privk "sign" t)))`
  - Role `ttp-cf2` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cf-prime-prime y))` -> `(recv (cat "sync-cf-req" (enc "abrq" (l-prime-prime y) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime-prime y) (privk "sign" a)) (privk "sign" t)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `comment`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (15)**: `(hash x)` -> `(enc "h" (cat "h" x))`; `(em)` -> `(enc m k)`; `(l-prime y x)` -> `(cat a b t y x)`; `(l-star e1 x)` -> `(l-prime (hash e1) x)`; `(eoo-star x e1 e2)` -> `(enc (cat "eootag" (hash (l-star e1 x)) e2) (privk "sign" a))`; `(eor-star x e1 e2)` -> `(enc (cat "eortag" (hash (l-star e1 x)) e2) (privk "sign" b))`; `(rr-star x e1 e2)` -> `(cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2) (enc (cat "rcrq" (l-star e1 x) e2) (privk "sign" b)))`; `(at-star e1 x)` -> `(enc (enc "abrq" (l-star e1 x) (privk "sign" a)) (privk "sign" t))`; `(ek l)` -> `(enc (cat "keytag" (hash l) k r) (pubk "encr" t))`; `(l)` -> `(l-prime (hash (enc m k)) (hash k))`; `(l-prime-prime y)` -> `(cat a b t y (hash k))`; `(eoo-prime-prime y)` -> `(enc (cat "eootag" (hash (l-prime-prime y)) (ek (l-prime-prime y))) (privk "sign" a))`; `(eor-prime-prime y)` -> `(enc (cat "eortag" (hash (l-prime-prime y)) (ek (l-prime-prime y))) (privk "sign" b))`; `(rr-prime-prime y)` -> `(cat (l-prime-prime y) (ek (l-prime-prime y)) (eoo-prime-prime y) (eor-prime-prime y) (enc "rcrq" (l-prime-prime y) (ek (l-prime-prime y)) (privk "sign" b)))`; `(cf-prime-prime y)` -> `(cat (l-prime-prime y) (ek (l-prime-prime y)) (eoo-prime-prime y) (eor-prime-prime y) (enc "cfrq" (l-prime-prime y) (ek (l-prime-prime y)) (privk "sign" b)))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (12)**:
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 1 (b b) (t t) (m m) (r r) (k k)) (deflistener m) (non-orig (privk "encr" t)) (uniq-orig m k) (comment "Experiment 1 to prove Lemma 4.1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 1 (b b) (t t) (m m) (r r) (k k)) (deflistener k) (non-orig (privk "encr" t)) (uniq-orig m k) (comment "Experiment 2 to prove Lemma 4.1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 3 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "First of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init3 3 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "Second of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init5 4 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "Third of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand resp1 3 (a a) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" a)) (comment "First of two experiments to prove Lemma 4.2, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand resp2 4 (a a) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" a)) (comment "Second of two experiments to prove Lemma 4.2, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (e1 e2 x mesg)) (defstrand resp3 4 (a a) (t t)) (non-orig (privk "sign" a)) (comment "Experiments to prove Lemma 4.2, clause 3."))`
    - `(defskeleton wang (vars (a b t hash_id name) (y x mesg)) (deflistener (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a)) (privk "sign" t))) (non-orig (privk "sign" t)) (comment "Experiments to prove Lemma 4.3, clause 1."))`
    - `(defskeleton wang (vars (y x mesg) (a b t name)) (defstrand ttp-ab1 3 (y y) (x x) (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 1 to prove Lemma 4.3, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (r text) (k skey) (y mesg)) (defstrand ttp-rc2 3 (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 2 to prove Lemma 4.3, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (r text) (k skey) (y mesg)) (defstrand ttp-cf2 3 (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 3 to prove Lemma 4.3, clause 2."))`
- **When to Reference This Example**: Reference this example to compare built-in `(hash ...)` against macro-encoded tagged encryption `(defmacro (hash x) (enc "h" (cat "h" x)))` in large fair-exchange protocols.
- **Key S-Expression Excerpt**:
```scheme
(herald "Wang's Fair Exchange Protocol" (bound 10))

;; CPSA input file to represent
;; Wang's Fair Exchange Protocol

;; This macro implements the CPSA
;; convention of regarding a hash as
;; an asymmetric encryption.  The
;; decryption key inverse to (pubk
;; hash) is assumed non-originating
;; in roles using hashing.

(defmacro (hash x)
  (enc "h" (cat "h" x)))

;; Wang's encrypted format for the
;; message payload.  Observe that m,
;; k get their values from the
;; like-named messages in the context
;; where the macro is expanded.

(defmacro (em)
  (enc m k))

;; The session label L as a fn of
;; the values that *should be* the
;; hashes of the encrypted message EM
;; and the session key K.

(defmacro (l-prime y x)
  (cat a b t y x))

;; The recipient can check that a
;; session label has an l-prime where
;; y is the hash of another parameter.
```

## weird.scm

- **File Path**: `03_examples_scm/weird.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Contrasts two protocols (`weird` using `(uniq-orig k)` and `weird-gen` using `(uniq-gen k)`) with roles `originator`, `guesser`, and `encryptor` to demonstrate why `uniq-orig` allows a `guesser` or `encryptor` to use key `k` without causal precedence, whereas `uniq-gen` enforces proper key generation ordering.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `originator` (in `weird`):
    - `vars`: `(k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(send k)`
  - Role `guesser` (in `weird`):
    - `vars`: `(k skey), (a name)` | Role assumptions: none
    - `trace`: `(send (enc a k))`
  - Role `encryptor` (in `weird`):
    - `vars`: `(k skey), (a name)` | Role assumptions: none
    - `trace`: `(recv (enc a k))`
  - Role `originator` (in `weird-gen`):
    - `vars`: `(k skey)` | Role assumptions/annotations: `(uniq-gen k)`
    - `trace`: `(send k)`
  - Role `guesser` (in `weird-gen`):
    - `vars`: `(k skey), (a name)` | Role assumptions: none
    - `trace`: `(send (enc a k))`
  - Role `encryptor` (in `weird-gen`):
    - `vars`: `(k skey), (a name)` | Role assumptions: none
    - `trace`: `(recv (enc a k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `precedes`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (6)**:
    - `(defskeleton weird (vars (k skey)) (defstrand originator 1 (k k)) (defstrand guesser 1 (k k)))`
    - `(defskeleton weird (vars (k skey)) (defstrand originator 1 (k k)) (defstrand encryptor 1 (k k)))`
    - `(defskeleton weird (vars (k skey)) (defstrand originator 1 (k k)) (defstrand encryptor 1 (k k)) (precedes ((0 0) (1 0))))`
    - `(defskeleton weird-gen (vars (k skey)) (defstrand originator 1 (k k)) (defstrand guesser 1 (k k)))`
    - `(defskeleton weird-gen (vars (k skey)) (defstrand originator 1 (k k)) (defstrand encryptor 1 (k k)))`
    - `(defskeleton weird-gen (vars (k skey)) (defstrand originator 1 (k k)) (defstrand encryptor 1 (k k)) (precedes ((0 0) (1 0))))`
- **When to Reference This Example**: Reference this example when deciding between `uniq-orig` and `uniq-gen` for dynamically generated symmetric keys.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol weird basic
  (defrole originator
    (vars (k skey))
    (trace (send k))
    (uniq-orig k))
  (defrole guesser
    (vars (k skey) (a name))
    (trace (send (enc a k))))
  (defrole encryptor
    (vars (k skey) (a name))
    (trace (recv (enc a k)))))

;;; CPSA mistakenly concludes this is a skeleton.
(defskeleton weird
  (vars (k skey))
  (defstrand originator 1 (k k))
  (defstrand guesser 1 (k k)))

;;; CPSA mistakenly concludes it is possible for the encryptor to
;;; acquire k.
(defskeleton weird
  (vars (k skey))
  (defstrand originator 1 (k k))
  (defstrand encryptor 1 (k k)))

(defskeleton weird
  (vars (k skey))
  (defstrand originator 1 (k k))
  (defstrand encryptor 1 (k k))
  (precedes ((0 0) (1 0))))

(defprotocol weird-gen basic
  (defrole originator
    (vars (k skey))
    (trace (send k))
    (uniq-gen k))
  (defrole guesser
    (vars (k skey) (a name))
```

## wonthull.scm

- **File Path**: `03_examples_scm/wonthull.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald wonthull (bound 9))` | Flags: `(bound 9)`
- **Protocol & Purpose**: Demonstrates a subtle incompleteness in CPSA's augmentation/hulling mechanism (`wonthull`, bound 9) where `init` sends `(cat (enc x1 x2 (pubk a)) (enc x3 x2 (pubk a)))` with `(uniq-orig x1 x2 x3)` and `resp` swaps components in `(enc "okay" y3 y1 (pubk a))`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `wonthull`):
    - `vars`: `(a name), (x1 x2 x3 x4 text)` | Role assumptions/annotations: `(uniq-orig x1 x2 x3)`, `(non-orig (privk a))`
    - `trace`: `(send (cat (enc x1 x2 (pubk a)) (enc x3 x2 (pubk a))))` -> `(recv (enc "okay" x3 x4 (pubk a)))`
  - Role `resp` (in `wonthull`):
    - `vars`: `(a name), (y1 y2 y3 text)` | Role assumptions: none
    - `trace`: `(recv (enc y1 y2 (pubk a)))` -> `(send (enc "okay" y3 y1 (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton wonthull (vars) (defstrand init 2))`
    - `(defskeleton wonthull (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 2 (a a) (x1 x1) (x2 x3) (x3 x3) (x4 x1)) (defstrand resp 2 (a a) (y1 x1) (y2 x3) (y3 x3)) (precedes ((0 0) (1 0)) ((1 1) (0 1))))`
- **When to Reference This Example**: Reference this example when studying CPSA's completeness boundaries regarding augmentation, deorigination, and hulling when multiple uniquely originating nonces can unify.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol wonthull basic
  (defrole init (vars (a name) (x1 x2 x3 x4 text))
    (trace
     (send (cat (enc x1 x2 (pubk a))
		(enc x3 x2 (pubk a))))
     (recv (enc "okay" x3 x4 (pubk a)))
     )
    (uniq-orig x1 x2 x3)
    (non-orig (privk a))
    )
  (defrole resp (vars (a name) (y1 y2 y3 text))
    (trace
     (recv (enc y1 y2 (pubk a)) )
     (send (enc "okay" y3 y1 (pubk a)) )
     )
    )
  )

(defskeleton wonthull
  (vars)
  (defstrand init 2)
)

(defskeleton wonthull
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 2 (a a) (x1 x1) (x2 x3) (x3 x3) (x4 x1))
  (defstrand resp 2 (a a) (y1 x1) (y2 x3) (y3 x3))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
)
```

## wonthull2.scm

- **File Path**: `03_examples_scm/wonthull2.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald wonthull2 (bound 9))` | Flags: `(bound 9)`
- **Protocol & Purpose**: Variant of `wonthull.scm` (`wonthull2`, bound 9) where `init` sends `(cat (enc x1 x3 (pubk a)) (enc x3 x2 (pubk a)))` with only `(uniq-orig x3)`, allowing CPSA to find the shape via variable separation.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `wonthull2`):
    - `vars`: `(a name), (x1 x2 x3 x4 text)` | Role assumptions/annotations: `(uniq-orig x3)`, `(non-orig (privk a))`
    - `trace`: `(send (cat (enc x1 x3 (pubk a)) (enc x3 x2 (pubk a))))` -> `(recv (enc "okay" x3 x4 (pubk a)))`
  - Role `resp` (in `wonthull2`):
    - `vars`: `(a name), (y1 y2 y3 text)` | Role assumptions: none
    - `trace`: `(recv (enc y1 y2 (pubk a)))` -> `(send (enc "okay" y3 y1 (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton wonthull2 (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 2))`
    - `(defskeleton wonthull2 (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 2 (x2 x3) (x4 x1)) (defstrand resp 2 (y1 x1) (y2 x3) (y3 x3)) (precedes ((0 0) (1 0)) ((1 1) (0 1))))`
- **When to Reference This Example**: Reference this example alongside `wonthull.scm` and `wonthull3.scm` when analyzing how deorigination and variable separation interact during CPSA search.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol wonthull2 basic
  (defrole init (vars (a name) (x1 x2 x3 x4 text))
    (trace
     (send (cat (enc x1 x3 (pubk a)) (enc x3 x2 (pubk a))))
     (recv (enc "okay" x3 x4 (pubk a)))
     )
    (uniq-orig x3)
    (non-orig (privk a))
  )
  (defrole resp (vars (a name) (y1 y2 y3 text))
     (trace
       (recv (enc y1 y2 (pubk a)) )
       (send (enc "okay" y3 y1 (pubk a)) )
     )
  )
)

(defskeleton wonthull2
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 2)
)

(defskeleton wonthull2
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 2 (x2 x3) (x4 x1))
  (defstrand resp 2 (y1 x1) (y2 x3) (y3 x3))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
)
```

## wonthull3.scm

- **File Path**: `03_examples_scm/wonthull3.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Third variant in the `wonthull` series (`wonthull3`) where `init` first sends `(enc x3 (pubk a))` before sending `(cat (enc x1 x2 (pubk a)) (enc x3 x2 (pubk a)))`, showing that deorigination behavior is not tied to the initial node of origination.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `wonthull3`):
    - `vars`: `(a name), (x1 x2 x3 x4 text)` | Role assumptions/annotations: `(uniq-orig x3)`, `(non-orig (privk a))`
    - `trace`: `(send (enc x3 (pubk a)))` -> `(send (cat (enc x1 x2 (pubk a)) (enc x3 x2 (pubk a))))` -> `(recv (enc "okay" x3 x4 (pubk a)))`
  - Role `resp` (in `wonthull3`):
    - `vars`: `(a name), (y1 y2 y3 text)` | Role assumptions: none
    - `trace`: `(recv (enc y1 y2 (pubk a)))` -> `(send (enc "okay" y3 y1 (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton wonthull3 (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 3))`
    - `(defskeleton wonthull3 (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 3 (x2 x3) (x4 x1)) (defstrand resp 2 (y1 x1) (y2 x3) (y3 x3)) (precedes ((0 1) (1 0)) ((1 1) (0 2))))`
- **When to Reference This Example**: Reference this example when investigating how earlier origination nodes (`(send (enc x3 (pubk a)))`) affect deorigination in subsequent protocol steps.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol wonthull3 basic
  (defrole init (vars (a name) (x1 x2 x3 x4 text))
    (trace
     (send (enc x3 (pubk a)))
     (send (cat (enc x1 x2 (pubk a))
		(enc x3 x2 (pubk a))))
     (recv (enc "okay" x3 x4 (pubk a)))
     )
    (uniq-orig x3)
    (non-orig (privk a))
    )
  (defrole resp (vars (a name) (y1 y2 y3 text))
    (trace
     (recv (enc y1 y2 (pubk a)) )
     (send (enc "okay" y3 y1 (pubk a)) )
     )
    )
  )

(defskeleton wonthull3
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 3)
)

(defskeleton wonthull3
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 3 (x2 x3) (x4 x1))
  (defstrand resp 2 (y1 x1) (y2 x3) (y3 x3))
  (precedes ((0 1) (1 0)) ((1 1) (0 2)))
)
```

## woolam.scm

- **File Path**: `03_examples_scm/woolam.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Woo-Lam Protocol")` | Flags: none
- **Protocol & Purpose**: Models the classic Woo-Lam unilateral authentication protocol (`woolam`) among initiator `a`, responder `b`, and server `s` using long-term symmetric keys `(ltk a s)` and `(ltk b s)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `woolam`):
    - `vars`: `(a s name), (n text)` | Role assumptions/annotations: `(non-orig (ltk a s))`
    - `trace`: `(send a)` -> `(recv n)` -> `(send (enc n (ltk a s)))`
  - Role `resp` (in `woolam`):
    - `vars`: `(a s b name), (n text)` | Role assumptions/annotations: `(non-orig (ltk b s))`, `(uniq-orig n)`
    - `trace`: `(recv a)` -> `(send n)` -> `(recv (enc n (ltk a s)))` -> `(send (enc a (enc n (ltk a s)) (ltk b s)))` -> `(recv (enc a n (ltk b s)))`
  - Role `serv` (in `woolam`):
    - `vars`: `(a s b name), (n text)` | Role assumptions: none
    - `trace`: `(recv (enc a (enc n (ltk a s)) (ltk b s)))` -> `(send (enc a n (ltk b s)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton woolam (vars (n text) (a s name)) (defstrand resp 5 (a a) (s s)) (non-orig (ltk a s)))`
- **When to Reference This Example**: Reference this example when modeling symmetric-key server-mediated unilateral authentication protocols using `(ltk a s)`.
- **Key S-Expression Excerpt**:
```scheme
(herald "Woo-Lam Protocol")

(defprotocol woolam basic
  (defrole init (vars (a s name) (n text))
    (trace
     (send a)
     (recv n)
     (send (enc n (ltk a s))))
    (non-orig (ltk a s)))
  (defrole resp (vars (a s b name) (n text))
    (trace
     (recv a)
     (send n)
     (recv (enc n (ltk a s)))
     (send (enc a (enc n (ltk a s)) (ltk b s)))
     (recv (enc a n (ltk b s))))
    (non-orig (ltk b s))
    (uniq-orig n))
  (defrole serv (vars (a s b name) (n text))
    (trace
     (recv (enc a (enc n (ltk a s)) (ltk b s)))
     (send (enc a n (ltk b s))))))

(defskeleton woolam (vars (n text) (a s name))
  (defstrand resp 5 (a a) (s s))
  (non-orig (ltk a s)))
```

## yahalom-6.3.6.scm

- **File Path**: `03_examples_scm/yahalom-6.3.6.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Yahalom Protocol" (comment "A Survey of Authentication Protocol Literature:" "Version 1.0, John Clark and Jeremy Jacob," "Yahalom Protocol, Section 6.3.6, Page 49") (url "http://www.eecs.umich.edu/acal/swerve/docs/49-1.pdf") (bound 15))` | Flags: `(comment "A Survey of Authentication Protocol Literature:" "Version 1.0, John Clark and Jeremy Jacob," "Yahalom Protocol, Section 6.3.6, Page 49")`, `(url "http://www.eecs.umich.edu/acal/swerve/docs/49-1.pdf")`, `(bound 15)`
- **Protocol & Purpose**: Models the Yahalom protocol as specified in Clark & Jacob's 'A Survey of Authentication Protocol Literature' Section 6.3.6, Page 49, where `init` receives `(cat (enc b k n-a n-b (ltk a s)) blob)` from `serv` and forwards `blob` (which is `(enc a k (ltk b s))`) alongside `(enc n-b k)` to `resp`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom`):
    - `vars`: `(a b s name), (n-a n-b text), (k skey), (blob mesg)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (cat (enc b k n-a n-b (ltk a s)) blob))` -> `(send (cat blob (enc n-b k)))`
  - Role `resp` (in `yahalom`):
    - `vars`: `(a b s name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b s))))` -> `(recv (cat (enc a k (ltk b s)) (enc n-b k)))`
  - Role `serv` (in `yahalom`):
    - `vars`: `(a b s name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b s))))` -> `(send (cat (enc b k n-a n-b (ltk a s)) (enc a k (ltk b s))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `comment`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `url`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton yahalom (vars (a b s name) (n-a n-b text)) (defstrand init 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b)) (non-orig (ltk a s) (ltk b s)) (uniq-orig n-a n-b))`
    - `(defskeleton yahalom (vars (a b s name) (n-a n-b text) (k skey)) (defstrand resp 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk a s) (ltk b s)) (uniq-orig n-a n-b))`
    - `(defskeleton yahalom (vars (a b s name) (n-a n-b text)) (defstrand resp 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b)) (non-orig (ltk a s) (ltk b s)) (uniq-orig n-a n-b))`
    - `(defskeleton yahalom (vars (a b s name) (n-a n-b text)) (defstrand serv 2 (a a) (b b) (s s) (n-a n-a) (n-b n-b)) (non-orig (ltk a s) (ltk b s)) (uniq-orig n-a n-b))`
- **When to Reference This Example**: Reference this example when modeling ticket-forwarding symmetric-key distribution protocols where an untyped `mesg` variable (`blob`) represents an opaque encrypted ticket forwarded by a principal who cannot decrypt it.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol yahalom basic
  (defrole init
    (vars (a b s name) (n-a n-b text) (k skey) (blob mesg))
    (trace
     (send (cat a n-a))
     (recv (cat (enc b k n-a n-b (ltk a s)) blob))
     (send (cat blob (enc n-b k)))))
  (defrole resp
    (vars (a b s name) (n-a n-b text) (k skey))
    (trace
     (recv (cat a n-a))
     (send (cat b (enc a n-a n-b (ltk b s))))
     (recv (cat (enc a k (ltk b s)) (enc n-b k)))))
  (defrole serv
    (vars (a b s name) (n-a n-b text) (k skey))
    (trace
     (recv (cat b (enc a n-a n-b (ltk b s))))
     (send (cat (enc b k n-a n-b (ltk a s)) (enc a k (ltk b s)))))
    (uniq-orig k))
  (comment "Yahalom protocol, Section 6.3.6, Page 49")
  (url "http://www.eecs.umich.edu/acal/swerve/docs/49-1.pdf"))

(defskeleton yahalom
  (vars (a b s name) (n-a n-b text))
  (defstrand init 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b))
  (non-orig (ltk a s) (ltk b s))
  (uniq-orig n-a n-b))

(defskeleton yahalom
  (vars (a b s name) (n-a n-b text) (k skey))
  (defstrand resp 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk a s) (ltk b s))
  (uniq-orig n-a n-b))

(defskeleton yahalom
```

## yahalom-forward.scm

- **File Path**: `03_examples_scm/yahalom-forward.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Yahalom Protocol With Forwarding" (bound 15))` | Flags: `(bound 15)`
- **Protocol & Purpose**: Models the Yahalom protocol with forwarding where `resp` receives `(cat (enc a k (ltk b c)) rest)` from `serv` and forwards the opaque `mesg` variable `rest` (containing `(enc b k n-a n-b (ltk a c))`) to `init`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (enc b k n-a n-b (ltk a c)))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom`):
    - `vars`: `(b a c name), (n-a n-b text), (rest mesg), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b c))))` -> `(recv (cat (enc a k (ltk b c)) rest))` -> `(send rest)` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b c))))` -> `(send (cat (enc a k (ltk b c)) (enc b k n-a n-b (ltk a c))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (3)**:
    - `(defskeleton yahalom (vars (a b c name) (n-b text)) (defstrand resp 5 (a a) (b b) (c c) (n-b n-b)) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
    - `(defskeleton yahalom (vars (a b c name) (n-b text) (k skey)) (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
    - `(defskeleton yahalom (vars (a b c name) (n-a text)) (defstrand init 3 (n-a n-a) (a a) (b b) (c c)) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-a))`
- **When to Reference This Example**: Reference this example when the responder (rather than the initiator) acts as the conduit forwarding an opaque server-encrypted ticket (`rest` of sort `mesg`) to the initiator.
- **Key S-Expression Excerpt**:
```scheme
(herald "Yahalom Protocol With Forwarding" (bound 15))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey))
    (trace (send (cat a n-a))
	   (recv (enc b k n-a n-b (ltk a c)))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (rest mesg) (k skey))
    (trace (recv (cat a n-a))
	   (send (cat b (enc a n-a n-b (ltk b c))))
	   (recv (cat (enc a k (ltk b c)) rest))
	   (send rest) 
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey))
    (trace (recv (cat b (enc a n-a n-b (ltk b c))))
	   (send (cat (enc a k (ltk b c))
		      (enc b k n-a n-b (ltk a c)))))
    (uniq-orig k)))

(defskeleton yahalom
  (vars (a b c name) (n-b text))
  (defstrand resp 5 (a a) (b b) (c c) (n-b n-b))
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))

;;; Ensure encryption key remains secret.
(defskeleton yahalom
  (vars (a b c name) (n-b text) (k skey))
  (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))

(defskeleton yahalom
  (vars (a b c name) (n-a text))
  (defstrand init 3 (n-a n-a) (a a) (b b) (c c))
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-a))
```

## yahalom.scm

- **File Path**: `03_examples_scm/yahalom.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Yahalom Protocol with Forwarding Removed" (bound 10))` | Flags: `(bound 10)`
- **Protocol & Purpose**: Models the Yahalom protocol with ticket forwarding removed: `serv` sends `(enc b k n-a n-b (ltk a c))` and `(enc a k (ltk b c))` as two separate messages directly to `init` and `resp` without an opaque `mesg` forwarding variable.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (enc b k n-a n-b (ltk a c)))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom`):
    - `vars`: `(b a c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b c))))` -> `(recv (enc a k (ltk b c)))` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b c))))` -> `(send (enc b k n-a n-b (ltk a c)))` -> `(send (enc a k (ltk b c)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton yahalom (vars (a b c name) (n-b text)) (defstrand resp 4 (a a) (b b) (c c) (n-b n-b)) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
    - `(defskeleton yahalom (vars (a b c name) (n-b text) (k skey)) (defstrand resp 4 (a a) (b b) (c c) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
- **When to Reference This Example**: Reference this example to see how removing opaque ticket forwarding (`mesg` variables) simplifies state-space bounds (`(bound 10)`) and avoids state-space explosion in KDC protocols.
- **Key S-Expression Excerpt**:
```scheme
(herald "Yahalom Protocol with Forwarding Removed" (bound 10))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey))
    (trace (send (cat a n-a))
	   (recv (enc b k n-a n-b (ltk a c)))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (k skey))
    (trace (recv (cat a n-a))
	   (send (cat b (enc a n-a n-b (ltk b c))))
	   (recv (enc a k (ltk b c)))
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey))
    (trace (recv (cat b (enc a n-a n-b (ltk b c))))
	   (send (enc b k n-a n-b (ltk a c)))
	   (send (enc a k (ltk b c))))
    (uniq-orig k)))

(defskeleton yahalom
  (vars (a b c name) (n-b text))
  (defstrand resp 4 (a a) (b b) (c c) (n-b n-b))
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))

;;; Ensure encryption key remains secret.
(defskeleton yahalom
  (vars (a b c name) (n-b text) (k skey))
  (defstrand resp 4 (a a) (b b) (c c) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))
```

## yes-or-no.scm

- **File Path**: `03_examples_scm/yes-or-no.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald yes-or-no)` | Flags: none
- **Protocol & Purpose**: Models a polarized query-response protocol (`yes-or-no`) where an initiator sends an encrypted question alongside two fresh `data` tokens `y` (yes) and `n` (no) under `ans-key`, and separate positive/negative roles (`init-positive`, `init-negative`, `resp-positive`, `resp-negative`) send or receive `y` or `n`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init-positive` (in `yes-or-no`):
    - `vars`: `(y n data), (question text), (ans name), (ans-key akey)` | Role assumptions: none
    - `trace`: `(send (enc question y n ans-key))` -> `(recv y)`
  - Role `init-negative` (in `yes-or-no`):
    - `vars`: `(y n data), (question text), (ans name), (ans-key akey)` | Role assumptions: none
    - `trace`: `(send (enc question y n ans-key))` -> `(recv n)`
  - Role `resp-positive` (in `yes-or-no`):
    - `vars`: `(y n data), (question text), (ans name), (ans-key akey)` | Role assumptions: none
    - `trace`: `(recv (enc question y n ans-key))` -> `(send y)`
  - Role `resp-negative` (in `yes-or-no`):
    - `vars`: `(y n data), (question text), (ans name), (ans-key akey)` | Role assumptions: none
    - `trace`: `(recv (enc question y n ans-key))` -> `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton yes-or-no (vars (y data) (ans-key akey)) (defstrand init-positive 2 (y y) (ans-key ans-key)) (uniq-orig y) (non-orig (invk ans-key)))`
    - `(defskeleton yes-or-no (vars (ans-key akey) (n data)) (defstrand init-negative 2 (n n) (ans-key ans-key)) (uniq-orig n) (non-orig (invk ans-key)))`
    - `(defskeleton yes-or-no (vars (y data) (ans-key akey)) (defstrand init-positive 1 (y y) (ans-key ans-key)) (deflistener y) (uniq-orig y) (non-orig (invk ans-key)))`
    - `(defskeleton yes-or-no (vars (n data) (ans-key akey)) (defstrand init-positive 1 (n n) (ans-key ans-key)) (deflistener n) (uniq-orig n) (non-orig (invk ans-key)))`
- **When to Reference This Example**: Reference this example when modeling branching or boolean choice responses (accept/reject, yes/no) by splitting choices into distinct roles (`*-positive`, `*-negative`) and fresh capability tokens.
- **Key S-Expression Excerpt**:
```scheme
(herald yes-or-no)

(defprotocol yes-or-no basic
  (defrole init-positive
    (vars (y n data) (question text) (ans name) (ans-key akey))
    (trace
     (send (enc question y n ans-key))
     (recv y)))

  (defrole init-negative
    (vars (y n data) (question text) (ans name) (ans-key akey))
    (trace
     (send (enc question y n ans-key))
     (recv n)))

  (defrole resp-positive
    (vars (y n data) (question text) (ans name) (ans-key akey))
    (trace
     (recv (enc question y n ans-key))
     (send y)))

  (defrole resp-negative
    (vars (y n data) (question text) (ans name) (ans-key akey))
    (trace
     (recv (enc question y n ans-key))
     (send n))))

(defskeleton yes-or-no
  (vars (y data) (ans-key akey))
  (defstrand init-positive 2 (y y) (ans-key ans-key))
  (uniq-orig y)
  (non-orig (invk ans-key)))

(defskeleton yes-or-no
  (vars (ans-key akey) (n data))
```

