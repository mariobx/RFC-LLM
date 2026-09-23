(herald "SDLSP Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defprotocol sdls-enc basic
  ;; Ground station sends an encrypted SDLS frame
  (defrole ground
    (vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))
    (trace
      (send (cat (sdl_header spacecraft) (enc frame_data assumed_enc_key)))
      (recv (cat (sdl_header ground) (enc frame_data assumed_enc_key)))))
  ;; Satellite receives the encrypted SDLS frame

  (defrole satellite
    (vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))
    (trace
      (recv (cat (sdl_header spacecraft) (enc frame_data assumed_enc_key)))
      (send (cat (sdl_header ground) (enc frame_data assumed_enc_key)))))
)

;; Ground-station point of view
(defskeleton sdls-enc
  (vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))
  (defstrandmax ground (frame_data frame_data) (assumed_enc_key assumed_enc_key) (spacecraft spacecraft) (ground ground))

  (non-orig assumed_enc_key))

;;Satellite point of view
(defskeleton sdls-enc
  (vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))
  (defstrandmax satellite (frame_data frame_data) (assumed_enc_key assumed_enc_key) (ground ground) (spacecraft spacecraft))
  (uniq-orig frame_data)

  (non-orig assumed_enc_key))



;(defgoal sdls-enc
;  (forall ((frame_data text) (assumed_enc_key skey) (ground spacecraft name) (z1 eve strd))
;    (implies
;      (and
;        (strand ground z1 2 (ground ground) (spacecraft spacecraft) (frame_data frame_data) (assumed_enc_key assumed_enc_key))
;        (pnon assumed_enc_key)
;        (pnon frame_data)
;        (listener eve frame_data)
;      )
;      (false)))
;  (comment "Confidentiality Goal: Adversary cannot learn frame_data (ground POV)")
;)

;; (defgoal sdls-enc
;;   (forall ((frame_data text) (ground spacecraft name) (z1 eve strd))
;;     (implies
;;       (and
;;         (strand satellite z1 2 (ground ground) (spacecraft spacecraft) (frame_data frame_data))
;;         (uniq frame_data)
;;         (non assumed_enc_key)
;;         (listener eve frame_data)
;;       )
;;       (false)))
;;   (comment "Confidentiality Goal: Adversary cannot learn frame_data (satellite POV)")
;; )
;;
;;
;;
;; (defgoal sdls-enc
;;   (forall ((frame_data text) (ground spacecraft name) (z1 eve strd))
;;     (implies
;;       (and
;;         (strand satellite z1 2 (ground ground) (spacecraft spacecraft) (frame_data frame_data))
;;         (uniq frame_data)
;;         (non assumed_enc_key)
;;         (listener eve (enc frame_data assumed_enc_key))
;;       )
;;       (false)))
;;   (comment "Confidentiality Goal: Adversary cannot learn frame_data (satellite POV)")
;; )
;;
