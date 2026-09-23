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
  (non-orig assumed_auth_key)
  (pen-non-orig sessionkey1)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-key-verification-auth
  (vars (assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid) (chal text) (old_arsn seq_n))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
                       (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal)
                       (ground ground) (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_auth_key)
  (pen-non-orig sessionkey1)
  (uniq-orig chal)
  (uniq-gen old_arsn)
  (comment "Ground-station point of view"))
