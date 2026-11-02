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

(defskeleton sdls-ep-rekey-sa-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n))
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
                       (assumed_auth_key assumed_auth_key)
                       (spi spi) (enckeyid enckeyid)
                       (authkeyid authkeyid) (new_arsn new_arsn)
                       (old_arsn old_arsn)
                       (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (uniq-orig new_arsn)
  (facts (neq old_arsn new_arsn))
  (uniq-orig old_arsn)
  (comment "Ground-station point of view"))
