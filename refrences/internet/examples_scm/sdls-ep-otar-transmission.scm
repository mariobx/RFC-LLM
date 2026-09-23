(herald "SDLS-EP Over-the-Air Rekeying (OTAR)")
;; OTAR command PDU, Figure 5-3 p.5-6:
;;   tag 00,0001 | length | Master Key ID | IV | { EncKeyID, EncKey } x N | MAC


(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))


(defmacro (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
  (cat keyid1 sessionkey1 keyid2 sessionkey2))

(defprotocol sdls-ep-otar basic
  ;; Initiator.  Steps 3.2.3.1.3.2 and 3.2.3.1.3.3, pp.3-4..3-5
  (defrole ground
    (vars (keymaster sessionkey1 sessionkey2 skey)
          (keyid1 keyid2 keyid))
    (trace
      ;; Key IDs sit in the enc, per 5.4.2.1.2.5 p.5-6.
      (send (otar_pdu (keyid_of keymaster)
              (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
                   keymaster)))))
  ;; Recipient.  Step 3.2.3.1.3.4, p.3-5

  (defrole satellite
    (vars (keymaster sessionkey1 sessionkey2 skey)
          (keyid1 keyid2 keyid))
    (trace
      (recv (otar_pdu (keyid_of keymaster)
              (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
                   keymaster)))))
  (lang (keyid atom)  (keyid_of hash))
  (comment "No reply PDU exists for OTAR (5.4.2.1.1, p.5-5.)"))


;pov skeletons
(defskeleton sdls-ep-otar
  (vars (keymaster skey))
  (defstrandmax satellite (keymaster keymaster))
  (non-orig keymaster)
  (comment "Recipient's view of OTAR"))

(defskeleton sdls-ep-otar
  (vars (keymaster sessionkey1 sessionkey2 skey))
  (defstrandmax ground (keymaster keymaster)
                       (sessionkey1 sessionkey1)
                       (sessionkey2 sessionkey2))
  (non-orig keymaster)
  (uniq-orig sessionkey1 sessionkey2)
  (comment "Initiator's view of OTAR"))
