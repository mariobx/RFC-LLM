(herald "SDLS-EP Key Activation")
;; Key Activation Command PDU
(defmacro (key_activation_pdu keyid)
  (cat "ep-pdu" "tag:00-0010" keyid))
;; Key database state (5.4.1.2 p.5-5) is not modelled and assumed

(defprotocol sdls-ep-key-activation basic
  (defrole ground
    (vars (keyid1 keyid))
    (trace
      (send (key_activation_pdu keyid1))))
  (defrole satellite
    (vars (keyid1 keyid))
    (trace
      (recv (key_activation_pdu keyid1))))
  (lang (keyid atom))
  (comment "No reply PDU exists for Key Activation -- 5.4.2.2.1, p.5-7."))


;pov skeletons
(defskeleton sdls-ep-key-activation
  (vars (keyid1 keyid))
  (defstrandmax satellite (keyid1 keyid1))
  (comment "Recipient's view"))
(defskeleton sdls-ep-key-activation
  (vars (keyid1 keyid))
  (defstrandmax ground (keyid1 keyid1))
  (comment "Initiator's view"))
