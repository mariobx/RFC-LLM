(herald "SDLS-EP Key Verification")

;; Key Verification Command PDU, Figure 5-7 p.5-10..
(defmacro (keyver_cmd keyid chal)
  (cat "ep-pdu" "tag:00-0100-cmd" keyid chal))

;; Key Verification Reply PDU, Figure 5-8 p.5-11.
(defmacro (keyver_reply keyid chal sessionkey)
  (cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey)))

(defprotocol sdls-ep-key-verification basic
  (defrole ground
    (vars (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (send (keyver_cmd keyid1 chal))
      (recv (keyver_reply keyid1 chal sessionkey1))))

  ;; Recipient.  3.2.3.5.3.4 and .3.5, p.3-12
  (defrole satellite
    (vars (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (recv (keyver_cmd keyid1 chal))
      (send (keyver_reply keyid1 chal sessionkey1))))

  (lang (keyid atom))
)

;pov skeletons
(defskeleton sdls-ep-key-verification
  (vars (sessionkey1 skey) (keyid1 keyid) (chal text))
  (defstrandmax ground (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal))
  (pen-non-orig sessionkey1)
  (uniq-orig chal)
  (comment "Initiator's view"))

(defskeleton sdls-ep-key-verification
  (vars (sessionkey1 skey) (keyid1 keyid))
  (defstrandmax satellite (sessionkey1 sessionkey1) (keyid1 keyid1))
  (pen-non-orig sessionkey1)
  (comment "Recipient's view of Key Verification"))
