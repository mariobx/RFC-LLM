(herald "Fordham's GREATEST PROTOCOL GO RAMS🐏🐏🐏🐏🐏🐏🐏🐏🐏🐏 Protocol"
  (algebra diffie-hellman)
  (comment "By: Mario Marku & Luke Shragher"))

;; ==========================================
;; MACRO DEFINITIONS
;; ==========================================
(defmacro (PMS dh_es dh_ew)
  (exp (gen) (mul dh_es dh_ew)))

(defmacro (S_write dh_es dh_ew rs rw)
  (hash (PMS dh_es dh_ew) rs rw "client-write"))

(defmacro (W_write dh_es dh_ew rs rw)
  (hash (PMS dh_es dh_ew) rs rw "server-write"))

; SCEP Tokens
(defmacro (Tok X Y data)
  (cat "Token" X (pubk X) Y (pubk Y) data))

(defmacro (SCEP-Token X Y data)
  (cat (Tok X Y data) (enc (hash (Tok X Y data)) (privk Y))))

; TLS
(defmacro (Cert_W W CA dh_ew)
  (cat W (pubk W) (enc (hash W (exp (gen) dh_ew)) (privk CA))))

(defmacro (W_KE dh_ew rs rw W)
  (cat (exp (gen) dh_ew)
       (enc (hash rs rw (exp (gen) dh_ew)) (privk W))))

(defmacro (S_FMESG rs rw W CA dh_ew)
  (cat rs rw (Cert_W W CA dh_ew) (W_KE dh_ew rs rw W)))

(defmacro (SFIN dh_es dh_ew rs rw W CA)
  (enc (hash (PMS dh_es dh_ew) "client-fin" (S_FMESG rs rw W CA dh_ew))
       (S_write dh_es dh_ew rs rw)))

(defmacro (WFIN dh_es dh_ew rs rw W CA)
  (enc (hash (PMS dh_es dh_ew) "server-fin" (S_FMESG rs rw W CA dh_ew) (SFIN dh_es dh_ew rs rw W CA))
       (W_write dh_es dh_ew rs rw)))


;; ==========================================
;; PROTOCOL DEFINITION
;; ==========================================

(defprotocol dh diffie-hellman
  (defrole client
    (vars (S W M CA name)
          (rS rW rSp rWp w text)
          (dh_eS dh_eW rndx))
    (trace
      ; Trace of TLS for the Client
      (send (enc rSp (pubk W)))
      (recv (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))
      (send (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))
      (recv (WFIN dh_eS dh_eW rSp rWp W CA))

      ; Trace of the SCEP W to S.
      (send (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))
      (recv (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))
      (send (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))
    )
    (uniq-orig rS rSp)
  )

  (defrole server
    (vars (S W M CA name)
          (rS rW rSp rWp w text)
          (dh_eS dh_eW rndx))
    (trace
      ; Trace of TLS for the Server
      (recv (enc rSp (pubk W)))
      (send (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))
      (recv (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))
      (send (WFIN dh_eS dh_eW rSp rWp W CA))

      ; Trace of the SCEP W to S.
      (recv (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))
      (send (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))
      (recv (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))
    )
    (uniq-orig rW rWp w)
  )
)

(defgoal dh
  (forall ((S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx) (z1 eve strd))
    (implies
      (and
        ;; The Client strand runs to full completion
        (p "client" z1 7)
        (p "client" "S" z1 S)
        (p "client" "W" z1 W)
        (p "client" "M" z1 M)
        (p "client" "CA" z1 CA)
        (p "client" "rS" z1 rS)
        (p "client" "rW" z1 rW)
        (p "client" "rSp" z1 rSp)
        (p "client" "rWp" z1 rWp)
        (p "client" "w" z1 w)
        (p "client" "dh_eS" z1 dh_eS)
        (p "client" "dh_eW" z1 dh_eW)

        ; We assume the longterm keys of all involved parties are not compromised
        (non (privk S))
        (non (privk W))
        (non (privk M))
        (non (privk CA))

        ;The adversary listener strand "eve" attempts to intercept the SCEP Token
        (p "" eve 1)
        (p "" "x" eve (SCEP-Token S M rS))
      )
      ;If all the above is true, it implies a logical impossibility (false)
      (false))))
  (comment "Confidentiality goal: The adversary cannot learn the SCEP-Token S M rS")


  ; view client pov, perfect ladder
(defskeleton dh
  (vars (S W M CA name)
        (rS rW rSp rWp w text)
        (dh_eS dh_eW rndx))
  (defstrandmax client
    (S S) (W W) (M M) (CA CA) (rS rS) (rW rW) (rSp rSp) (rWp rWp) (w w) (dh_eS dh_eS) (dh_eW dh_eW))
  (pen-non-orig (privk S) (privk W) (privk CA))
  (comment "Analyze security from the Client's perspective"))

 ; view skeleton pov, will be a straight line
(defskeleton dh
  (vars (S W M CA name)
        (rS rW rSp rWp w text)
        (dh_eS dh_eW rndx))
  (defstrandmax server
    (S S) (W W) (M M) (CA CA) (rS rS) (rW rW) (rSp rSp) (rWp rWp) (w w) (dh_eS dh_eS) (dh_eW dh_eW))
  (pen-non-orig (privk S) (privk W) (privk CA))
  (comment "Analyze security from the Server's perspective"))


