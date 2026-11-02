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

;;Ground-station point of view
(defskeleton sdls-auth-enc
  (vars (header text) (frame_data tc) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (ground spacecraft name))
  (defstrandmax ground (header header) (frame_data frame_data) (old_arsn old_arsn) (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spacecraft spacecraft) (ground ground))
  ;; The adversary does not initially possess the encryption key.
  (non-orig assumed_enc_key assumed_auth_key)
  (uniq-orig old_arsn)
)

;; Satellite point of view
(defskeleton sdls-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (ground ground) (spacecraft spacecraft))
  ;; The adversary does not initially possess the decryption key.
  (non-orig assumed_enc_key assumed_auth_key)
)
