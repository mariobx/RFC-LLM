(herald "SDLS-EP Start SA")

;; Start SA PDU, p.5-14.  Tag 01,1011.

;; Fields per 5.5.1.2.2.2: SPI (16 bits, mandatory) and one or more

;; GVC/GMAP IDs (32 bits each, mandatory).  One GVCID modelled.
(defmacro (start_sa_pdu spi gvcid)
  (cat "ep-pdu" "tag:01-1011" spi gvcid))

;; The 3.3.3.1.2 precondition -- SA in Keyed state --
;; is assumed rather than checked.
(defprotocol sdls-ep-start-sa basic
  ;; Initiator.  3.3.3.1.3.2 then 3.3.3.1.3.3, pp.3-18..3-19
  (defrole ground
    (vars (spi spi) (gvcid gvcid))
    (trace
      (send (start_sa_pdu spi gvcid))))
  ;; Recipient.  3.3.3.1.3.4, p.3-19.
  (defrole satellite
    (vars (spi spi) (gvcid gvcid))
    (trace
      (recv (start_sa_pdu spi gvcid))))
  (lang (spi atom) (gvcid atom))
  (comment "No reply PDU exists for Start SA -- 5.5.1.2.1, p.5-14."))


;;; pov.
(defskeleton sdls-ep-start-sa
  (vars (spi spi) (gvcid gvcid))
  (defstrandmax satellite (spi spi) (gvcid gvcid))
  (comment "Recipient's view"))
(defskeleton sdls-ep-start-sa
  (vars (spi spi) (gvcid gvcid))
  (defstrandmax ground (spi spi) (gvcid gvcid))
  (comment "Initiator's view"
  )
)
