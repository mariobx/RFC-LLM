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
                       (assumed_auth_key assumed_auth_key)
                       (keyid1 keyid1)
                       (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_enc_key assumed_auth_key)
  (uniq-orig old_arsn)
  (comment "Ground-station point of view"))
