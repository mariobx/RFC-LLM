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
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
                       (assumed_auth_key assumed_auth_key)
                       (spi spi) (gvcid gvcid)
                      (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_enc_key assumed_auth_key)
  (uniq-orig old_arsn)
  (comment "Ground-station point of view"))
