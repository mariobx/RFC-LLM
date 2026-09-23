(herald "SDLSP TC Baseline: Authentication Only (AES-CMAC): full SDLS-EP rekeying sequence")

;; MODELLED
;;   1. OTAR                3.2.3.1   session keys delivered under the master key
;;   2. Key Activation      3.2.3.2   key IDs signalled for activation
;;   3. Rekey SA            3.3.3.3   keys bound to the SA
;;   4. Start SA            3.3.3.1   SA put in service on a channel
;;   5. Key Verification    3.2.3.5   challenge / response under the new key
;;   6. Traffic             355.0-B-2 the new SA protects a frame_data
;;
;; KEYS
;;   assumed_auth_key                     the SA already in service.  4.3.1.1
;;     p.4-5 requires every EP command PDU to ride an already-protected
;;     channel, so steps 1-5 all use it; a key cannot be delivered under
;;     itself.  4.3.1.2 p.4-5 recommends this be an SA other than the one
;;     being affected.
;;   sessionkey1 / sessionkey2            delivered by OTAR, bound to the SA
;;     as Encryption and Authentication Key ID in step 3.  Only sessionkey2
;;     protects step 6 traffic.  sessionkey1 is exercised only by the Key
;;     Verification response, which 5.4.2.5.3.4 p.5-11 encrypts regardless of
;;     the frame transport mode.
;;
;; SEQUENCE NUMBERS
;;   Steps 1-5 run on the old SA and advance one successor per frame.
;;   Step 6 restarts at new_arsn: 5.5.1.4.2.7 p.5-16 makes the Rekey SA ARSN the
;;   NEW value for the new key, like a counter reset instead of an increment.
;;
;; ASSUMPTIONS
;;   keymaster is non-originating: 3.2.3.1.2.2 p.3-4 pre-shares it and no
;;     procedure transmits it. Must be assumed for generic protocol version
;;   the in-service SA keys are non-originating in the point-of-view skeletons.
;;   sessionkey1, sessionkey2, new_arsn, chal and frame_data originate uniquely
;;     at the Initiator.
;;
;;
;; NOT MODELLED
;;   Create SA, Delete SA, Stop SA, Expire SA, Key Deactivation, Key Destruction
;;   3.3.3.1.3.4 d.2, the GVCID authorization check



(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))
(defmacro (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
  (cat keyid1 sessionkey1 keyid2 sessionkey2))
(defmacro (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
  (otar_pdu (keyid_of keymaster)
    (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))

(defmacro (key_activation_pdu keyid)
  (cat "ep-pdu" "tag:00-0010" keyid))

(defmacro (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
  (cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv))

(defmacro (start_sa_pdu spi gvcid)
  (cat "ep-pdu" "tag:01-1011" spi gvcid))

(defmacro (keyver_cmd keyid chal)
  (cat "ep-pdu" "tag:00-0100-cmd" keyid chal))
(defmacro (keyver_reply keyid chal sessionkey)
  (cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey)))

(defprotocol sdls-ep-chain-auth basic

  (defrole ground
    (vars (header text) (old_arsn new_arsn seq_n) (iv text)
          (assumed_auth_key skey) (ground spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid)
          (spi spi) (gvcid gvcid) (chal text) (frame_data tc))
    (trace
        ;; STEP 1 -- OTAR, 3.2.3.1
      (send
        (cat (sdl_header spacecraft) header (successor old_arsn)
             (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
             (hash (sdl_header spacecraft) header (successor old_arsn)
                   (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key))
      )

      ;; STEP 2 -- Key Activation, 3.2.3.2
      (send
        (cat (sdl_header spacecraft) header (successor (successor old_arsn))
             (key_activation_pdu keyid1)
             (hash (sdl_header spacecraft) header (successor (successor old_arsn))
                   (key_activation_pdu keyid1) assumed_auth_key))
      )

      ;; STEP 3 -- Rekey SA, 3.3.3.3
      (send
        (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
             (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv)
             (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
                   (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_auth_key))
      )

      ;; STEP 4 -- Start SA, 3.3.3.1
      (send
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
             (start_sa_pdu spi gvcid)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
                   (start_sa_pdu spi gvcid) assumed_auth_key))
      )

      ;; STEP 5 -- Key Verification, 3.2.3.5
      (send
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
             (keyver_cmd keyid1 chal)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
                   (keyver_cmd keyid1 chal) assumed_auth_key))
      )


      (recv
        (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
             (keyver_reply keyid1 chal sessionkey1)
             (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
                   (keyver_reply keyid1 chal sessionkey1) assumed_auth_key))
      )
   ;; STEP 6 -- new SA carries traffic under the OTAR'd keys
      (send
        (cat (sdl_header spacecraft) header (successor new_arsn)
             frame_data
             (hash (sdl_header spacecraft) header (successor new_arsn)
                   frame_data sessionkey2))
      )

    )
  )

  (defrole satellite
    (vars (header text) (old_arsn new_arsn seq_n) (iv text)
          (assumed_auth_key skey) (ground spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid)
          (spi spi) (gvcid gvcid) (chal text) (frame_data tc))
    (trace
      (recv
        (cat (sdl_header spacecraft) header (successor old_arsn)
             (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
             (hash (sdl_header spacecraft) header (successor old_arsn)
                   (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key))
      )
      ;; STEP 1 -- OTAR, 3.2.3.1

      (recv
        (cat (sdl_header spacecraft) header (successor (successor old_arsn))
             (key_activation_pdu keyid1)
             (hash (sdl_header spacecraft) header (successor (successor old_arsn))
                   (key_activation_pdu keyid1) assumed_auth_key))
      )
      ;; STEP 2 -- Key Activation, 3.2.3.2

      (recv
        (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
             (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv)
             (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
                   (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_auth_key))
      )
      ;; STEP 3 -- Rekey SA, 3.3.3.3

      (recv
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
             (start_sa_pdu spi gvcid)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
                   (start_sa_pdu spi gvcid) assumed_auth_key))
      )
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
  (facts (neq old_arsn new_arsn))
  (non-orig keymaster)
  (comment "Satellite point of view")
)

(defskeleton sdls-ep-chain-auth
  (vars (assumed_auth_key keymaster sessionkey1 sessionkey2 skey)
        (ground spacecraft name) (old_arsn new_arsn seq_n) (chal text) (frame_data tc))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
                       (keymaster keymaster)
                       (sessionkey1 sessionkey1) (sessionkey2 sessionkey2)
                       (old_arsn old_arsn) (new_arsn new_arsn)
                       (ground ground) (spacecraft spacecraft) (chal chal) (frame_data frame_data))
  (non-orig assumed_auth_key keymaster)
  (uniq-orig sessionkey1 sessionkey2)
  (facts (neq old_arsn new_arsn))
  (uniq-gen old_arsn)
  (uniq-orig new_arsn chal frame_data sessionkey1 sessionkey2)
  (non-orig keymaster)
  (comment "Ground-station point of view")
)
