(herald "SDLS-EP Rekey SA")


;; Rekey SA PDU, Figure 5-14 p.5-16
;; Field order per 5.5.1.4.2.2
(defmacro (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
  (cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv))

(defprotocol sdls-ep-rekey-sa basic
  ;; Initiator  3.3.3.3.3.2 then 3.3.3.3.3.3, pp.3-21..3-22.
  ;; Initiator transitions its own SA to Keyed before signalling.
  (defrole ground
    (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (send (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv))))
  ;; Recipient.  3.3.3.3.3.4, p.3-22.
  (defrole satellite
    (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (recv (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv))))
  (lang (spi atom) (keyid atom) (seq_n atom))
  (comment "No reply PDU exists for Rekey SA -- 5.5.1.4.1, p.5-15."))

;;; pov
(defskeleton sdls-ep-rekey-sa
  (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n))
  (defstrandmax satellite (spi spi) (enckeyid enckeyid)
                          (authkeyid authkeyid) (new_arsn new_arsn))
  (comment "Recipient's view"))
(defskeleton sdls-ep-rekey-sa
  (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n))
  (defstrandmax ground (spi spi) (enckeyid enckeyid)
                       (authkeyid authkeyid) (new_arsn new_arsn))
  (uniq-orig new_arsn)
  (comment "Initiator's view.")
  )
