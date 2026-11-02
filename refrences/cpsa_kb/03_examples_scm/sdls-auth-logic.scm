(herald "SDLSP TC Baseline: Authentication Only (AES-CMAC)")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defprotocol sdls-tc-auth basic
  (defrole ground
    (vars (header text) (frame_data tc) (old_arsn seq_n) (assumed_auth_key skey) (ground spacecraft name))
    (trace
      (send
        (cat (sdl_header spacecraft) header (successor old_arsn) frame_data
             (hash (sdl_header spacecraft) header (successor old_arsn) frame_data assumed_auth_key))
      )
      (recv
        (cat (sdl_header ground) (successor (successor old_arsn)) frame_data
             (hash (sdl_header ground) (successor (successor old_arsn)) frame_data assumed_auth_key))
      )
    )
  )
  (defrole satellite
    (vars (header text) (frame_data tc) (old_arsn seq_n) (assumed_auth_key skey) (ground spacecraft name))
    (trace
      (recv
        (cat (sdl_header spacecraft) header (successor old_arsn) frame_data
             (hash (sdl_header spacecraft) header (successor old_arsn) frame_data assumed_auth_key))
      )
      (send
        (cat (sdl_header ground) (successor (successor old_arsn)) frame_data
             (hash (sdl_header ground) (successor (successor old_arsn)) frame_data assumed_auth_key))
      )
    )
  )
  (lang (seq_n atom) (tc atom) (successor hash))
)

(defgoal sdls-tc-auth
  (forall ((ground spacecraft name) (assumed_auth_key skey) (frame_data tc) (old_arsn seq_n) (z1 eve strd))
    (implies
      (and
        (strand ground z1 2 (ground ground) (spacecraft spacecraft) (old_arsn old_arsn) (frame_data frame_data) (assumed_auth_key assumed_auth_key))
        (pnon assumed_auth_key)
        (ugen old_arsn)
        (uniq frame_data)
        (listener eve frame_data)
      )
      (false)))
  (comment "Confidentiality Goal: Adversary cannot learn telecommand")
)


;; (defgoal sdls-tc-auth
;;   (forall ((ground spacecraft name) (assumed_auth_key skey) (frame_data tc) (old_arsn seq_n) (z1 eve strd))
;;     (implies
;;       (and
;;         (strand satellite z1 2 (ground ground) (spacecraft spacecraft) (old_arsn old_arsn) (frame_data frame_data) (assumed_auth_key assumed_auth_key))
;;         (pnon assumed_auth_key)
;;         (ugen old_arsn)
;;         (uniq frame_data)
;;         (listener eve frame_data)
;;       )
;;       (false)))
;;   (comment "Confidentiality Goal: Adversary cannot learn telecommand")
;; )

(defskeleton sdls-tc-auth
  (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (frame_data tc) (ground spacecraft name))
  (defstrandmax ground (old_arsn old_arsn) (assumed_auth_key assumed_auth_key) (frame_data frame_data) (spacecraft spacecraft))
  (pen-non-orig assumed_auth_key)

  (uniq-gen old_arsn))

(defskeleton sdls-tc-auth
  (vars (header text) (assumed_auth_key skey) (frame_data tc) (old_arsn seq_n) (ground spacecraft name))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key) (frame_data frame_data) (old_arsn old_arsn) (spacecraft spacecraft) (ground ground))
  (pen-non-orig assumed_auth_key)
)
