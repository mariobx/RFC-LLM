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
                       (keyid1 keyid1)
                       (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_auth_key)
  (uniq-gen old_arsn)
  (comment "Ground-station point of view"))
