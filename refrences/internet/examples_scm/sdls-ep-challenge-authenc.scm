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
                          (ground ground) (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (pen-non-orig sessionkey1)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-key-verification-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid) (chal text) (old_arsn seq_n))
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
                       (assumed_auth_key assumed_auth_key)
                       (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal)
                       (ground ground) (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_enc_key assumed_auth_key)
  (pen-non-orig sessionkey1)
  (uniq-orig chal)
  (uniq-orig old_arsn)
  (comment "Ground-station point of view"))
