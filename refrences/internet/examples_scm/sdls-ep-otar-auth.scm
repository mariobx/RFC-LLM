(herald "SDLS-EP OTAR: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))
(defmacro (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
  (cat keyid1 sessionkey1 keyid2 sessionkey2))
(defmacro (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
  (otar_pdu (keyid_of keymaster)
    (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))

(defprotocol sdls-ep-otar-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
             (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
             (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom) (keyid_of hash)))

(defskeleton sdls-ep-otar-auth
  (vars (assumed_auth_key skey) (spacecraft name) (keymaster skey))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (keymaster keymaster)
                          (spacecraft spacecraft))
  (non-orig assumed_auth_key keymaster)
  (non-orig keymaster)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-otar-auth
  (vars (assumed_auth_key skey) (spacecraft name) (keymaster sessionkey1 sessionkey2 skey) (old_arsn seq_n))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
                       (keymaster keymaster)
                       (sessionkey1 sessionkey1) (sessionkey2 sessionkey2)
                       (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_auth_key keymaster)
  (uniq-orig sessionkey1 sessionkey2)
  (non-orig keymaster)
  (uniq-gen old_arsn)
  (comment "Ground-station point of view"))
