# Official MITRE CPSA Scheme (.scm) Protocol Examples Corpus

> Tier 3 Reference Corpus — Complete collection of 148 official MITRE CPSA `.scm` protocol specifications, heralds, macros, defroles, and security goals used for few-shot RAG grounding and grammar verification.

*Generated: 2026-10-14 16:18:38 UTC · Git: `main` @ `f572f106cef2` · Tier: Tier 3 — Domain Reference Code Corpus (.scm) · Files: 148*

## Table of Contents

- [`refrences/internet/examples_scm/DH_hack.scm`](#refrencesinternetexamples-scmdh-hackscm)
- [`refrences/internet/examples_scm/ab.scm`](#refrencesinternetexamples-scmabscm)
- [`refrences/internet/examples_scm/abc.scm`](#refrencesinternetexamples-scmabcscm)
- [`refrences/internet/examples_scm/aik.scm`](#refrencesinternetexamples-scmaikscm)
- [`refrences/internet/examples_scm/atomic-open-closed.scm`](#refrencesinternetexamples-scmatomic-open-closedscm)
- [`refrences/internet/examples_scm/attest.scm`](#refrencesinternetexamples-scmattestscm)
- [`refrences/internet/examples_scm/auth-enc.scm`](#refrencesinternetexamples-scmauth-encscm)
- [`refrences/internet/examples_scm/auth-hash.scm`](#refrencesinternetexamples-scmauth-hashscm)
- [`refrences/internet/examples_scm/blanchet-strandmax.scm`](#refrencesinternetexamples-scmblanchet-strandmaxscm)
- [`refrences/internet/examples_scm/blanchet.scm`](#refrencesinternetexamples-scmblanchetscm)
- [`refrences/internet/examples_scm/bug_example.scm`](#refrencesinternetexamples-scmbug-examplescm)
- [`refrences/internet/examples_scm/cert_lang.scm`](#refrencesinternetexamples-scmcert-langscm)
- [`refrences/internet/examples_scm/chan-envelope.scm`](#refrencesinternetexamples-scmchan-envelopescm)
- [`refrences/internet/examples_scm/chan-perrig-song.scm`](#refrencesinternetexamples-scmchan-perrig-songscm)
- [`refrences/internet/examples_scm/chan-unilateral.scm`](#refrencesinternetexamples-scmchan-unilateralscm)
- [`refrences/internet/examples_scm/chan-yahalom-role-decl.scm`](#refrencesinternetexamples-scmchan-yahalom-role-declscm)
- [`refrences/internet/examples_scm/chan-yahalom.scm`](#refrencesinternetexamples-scmchan-yahalomscm)
- [`refrences/internet/examples_scm/commitment.scm`](#refrencesinternetexamples-scmcommitmentscm)
- [`refrences/internet/examples_scm/comp_test.scm`](#refrencesinternetexamples-scmcomp-testscm)
- [`refrences/internet/examples_scm/completeness-test.scm`](#refrencesinternetexamples-scmcompleteness-testscm)
- [`refrences/internet/examples_scm/crushing.scm`](#refrencesinternetexamples-scmcrushingscm)
- [`refrences/internet/examples_scm/dass_simple.scm`](#refrencesinternetexamples-scmdass-simplescm)
- [`refrences/internet/examples_scm/denning-sacco.scm`](#refrencesinternetexamples-scmdenning-saccoscm)
- [`refrences/internet/examples_scm/deorig_contract.scm`](#refrencesinternetexamples-scmdeorig-contractscm)
- [`refrences/internet/examples_scm/deorig_mesg.scm`](#refrencesinternetexamples-scmdeorig-mesgscm)
- [`refrences/internet/examples_scm/deorig_simple.scm`](#refrencesinternetexamples-scmdeorig-simplescm)
- [`refrences/internet/examples_scm/dh-ca_hack.scm`](#refrencesinternetexamples-scmdh-ca-hackscm)
- [`refrences/internet/examples_scm/dh_encrypt_hack.scm`](#refrencesinternetexamples-scmdh-encrypt-hackscm)
- [`refrences/internet/examples_scm/dh_group_sig.scm`](#refrencesinternetexamples-scmdh-group-sigscm)
- [`refrences/internet/examples_scm/dh_group_sig_auth_failure.scm`](#refrencesinternetexamples-scmdh-group-sig-auth-failurescm)
- [`refrences/internet/examples_scm/dh_mim_hack.scm`](#refrencesinternetexamples-scmdh-mim-hackscm)
- [`refrences/internet/examples_scm/dhnsl_hack.scm`](#refrencesinternetexamples-scmdhnsl-hackscm)
- [`refrences/internet/examples_scm/dhstatic-state.scm`](#refrencesinternetexamples-scmdhstatic-statescm)
- [`refrences/internet/examples_scm/disclosure.scm`](#refrencesinternetexamples-scmdisclosurescm)
- [`refrences/internet/examples_scm/doorsep.scm`](#refrencesinternetexamples-scmdoorsepscm)
- [`refrences/internet/examples_scm/doorsep2invk.scm`](#refrencesinternetexamples-scmdoorsep2invkscm)
- [`refrences/internet/examples_scm/encsig.scm`](#refrencesinternetexamples-scmencsigscm)
- [`refrences/internet/examples_scm/envelope.scm`](#refrencesinternetexamples-scmenvelopescm)
- [`refrences/internet/examples_scm/epmo-hash.scm`](#refrencesinternetexamples-scmepmo-hashscm)
- [`refrences/internet/examples_scm/epmo-key-hash.scm`](#refrencesinternetexamples-scmepmo-key-hashscm)
- [`refrences/internet/examples_scm/epmo.scm`](#refrencesinternetexamples-scmepmoscm)
- [`refrences/internet/examples_scm/epmo_acctnum-key-hash.scm`](#refrencesinternetexamples-scmepmo-acctnum-key-hashscm)
- [`refrences/internet/examples_scm/expand.scm`](#refrencesinternetexamples-scmexpandscm)
- [`refrences/internet/examples_scm/facts.scm`](#refrencesinternetexamples-scmfactsscm)
- [`refrences/internet/examples_scm/factvar.scm`](#refrencesinternetexamples-scmfactvarscm)
- [`refrences/internet/examples_scm/ffgg.scm`](#refrencesinternetexamples-scmffggscm)
- [`refrences/internet/examples_scm/fluffy_draft03_gske.scm`](#refrencesinternetexamples-scmfluffy-draft03-gskescm)
- [`refrences/internet/examples_scm/fragile_pruning.scm`](#refrencesinternetexamples-scmfragile-pruningscm)
- [`refrences/internet/examples_scm/goals.scm`](#refrencesinternetexamples-scmgoalsscm)
- [`refrences/internet/examples_scm/goalsvar.scm`](#refrencesinternetexamples-scmgoalsvarscm)
- [`refrences/internet/examples_scm/hashtest-key-hash.scm`](#refrencesinternetexamples-scmhashtest-key-hashscm)
- [`refrences/internet/examples_scm/hashtest.scm`](#refrencesinternetexamples-scmhashtestscm)
- [`refrences/internet/examples_scm/incompleteness_example.scm`](#refrencesinternetexamples-scmincompleteness-examplescm)
- [`refrences/internet/examples_scm/isoreject-corrected.scm`](#refrencesinternetexamples-scmisoreject-correctedscm)
- [`refrences/internet/examples_scm/isoreject.scm`](#refrencesinternetexamples-scmisorejectscm)
- [`refrences/internet/examples_scm/kelly1.scm`](#refrencesinternetexamples-scmkelly1scm)
- [`refrences/internet/examples_scm/kerberos.scm`](#refrencesinternetexamples-scmkerberosscm)
- [`refrences/internet/examples_scm/lemmas.scm`](#refrencesinternetexamples-scmlemmasscm)
- [`refrences/internet/examples_scm/locn_envelope.scm`](#refrencesinternetexamples-scmlocn-envelopescm)
- [`refrences/internet/examples_scm/missing_contraction.scm`](#refrencesinternetexamples-scmmissing-contractionscm)
- [`refrences/internet/examples_scm/neq_test.scm`](#refrencesinternetexamples-scmneq-testscm)
- [`refrences/internet/examples_scm/neuman-stubblebine.scm`](#refrencesinternetexamples-scmneuman-stubblebinescm)
- [`refrences/internet/examples_scm/no_contraction.scm`](#refrencesinternetexamples-scmno-contractionscm)
- [`refrences/internet/examples_scm/non_transforming.scm`](#refrencesinternetexamples-scmnon-transformingscm)
- [`refrences/internet/examples_scm/nonaug-prune.scm`](#refrencesinternetexamples-scmnonaug-prunescm)
- [`refrences/internet/examples_scm/ns-l.scm`](#refrencesinternetexamples-scmns-lscm)
- [`refrences/internet/examples_scm/ns-rebinding.scm`](#refrencesinternetexamples-scmns-rebindingscm)
- [`refrences/internet/examples_scm/ns.scm`](#refrencesinternetexamples-scmnsscm)
- [`refrences/internet/examples_scm/nsl3.scm`](#refrencesinternetexamples-scmnsl3scm)
- [`refrences/internet/examples_scm/nslsk.scm`](#refrencesinternetexamples-scmnslskscm)
- [`refrences/internet/examples_scm/open-closed-multiloc.scm`](#refrencesinternetexamples-scmopen-closed-multilocscm)
- [`refrences/internet/examples_scm/open-closed-tag.scm`](#refrencesinternetexamples-scmopen-closed-tagscm)
- [`refrences/internet/examples_scm/open-closed.scm`](#refrencesinternetexamples-scmopen-closedscm)
- [`refrences/internet/examples_scm/or.scm`](#refrencesinternetexamples-scmorscm)
- [`refrences/internet/examples_scm/ordered.scm`](#refrencesinternetexamples-scmorderedscm)
- [`refrences/internet/examples_scm/orderedvar.scm`](#refrencesinternetexamples-scmorderedvarscm)
- [`refrences/internet/examples_scm/pca.scm`](#refrencesinternetexamples-scmpcascm)
- [`refrences/internet/examples_scm/pen-non-orig-test.scm`](#refrencesinternetexamples-scmpen-non-orig-testscm)
- [`refrences/internet/examples_scm/pfs-via-pubkey.scm`](#refrencesinternetexamples-scmpfs-via-pubkeyscm)
- [`refrences/internet/examples_scm/pkinit.scm`](#refrencesinternetexamples-scmpkinitscm)
- [`refrences/internet/examples_scm/preprocess.scm`](#refrencesinternetexamples-scmpreprocessscm)
- [`refrences/internet/examples_scm/print.scm`](#refrencesinternetexamples-scmprintscm)
- [`refrences/internet/examples_scm/prottrans.scm`](#refrencesinternetexamples-scmprottransscm)
- [`refrences/internet/examples_scm/pruning1.scm`](#refrencesinternetexamples-scmpruning1scm)
- [`refrences/internet/examples_scm/puzzle_example.scm`](#refrencesinternetexamples-scmpuzzle-examplescm)
- [`refrences/internet/examples_scm/reflect.scm`](#refrencesinternetexamples-scmreflectscm)
- [`refrences/internet/examples_scm/renamings.scm`](#refrencesinternetexamples-scmrenamingsscm)
- [`refrences/internet/examples_scm/role_uniq.scm`](#refrencesinternetexamples-scmrole-uniqscm)
- [`refrences/internet/examples_scm/rule-node.scm`](#refrencesinternetexamples-scmrule-nodescm)
- [`refrences/internet/examples_scm/rule-order.scm`](#refrencesinternetexamples-scmrule-orderscm)
- [`refrences/internet/examples_scm/rules.scm`](#refrencesinternetexamples-scmrulesscm)
- [`refrences/internet/examples_scm/scep-tls-dh-broken.scm`](#refrencesinternetexamples-scmscep-tls-dh-brokenscm)
- [`refrences/internet/examples_scm/scep-tls-dh-fixed.scm`](#refrencesinternetexamples-scmscep-tls-dh-fixedscm)
- [`refrences/internet/examples_scm/sdls-auth-enc-full-payload.scm`](#refrencesinternetexamples-scmsdls-auth-enc-full-payloadscm)
- [`refrences/internet/examples_scm/sdls-auth-enc-logic.scm`](#refrencesinternetexamples-scmsdls-auth-enc-logicscm)
- [`refrences/internet/examples_scm/sdls-auth-full-payload.scm`](#refrencesinternetexamples-scmsdls-auth-full-payloadscm)
- [`refrences/internet/examples_scm/sdls-auth-logic.scm`](#refrencesinternetexamples-scmsdls-auth-logicscm)
- [`refrences/internet/examples_scm/sdls-enc-logic.scm`](#refrencesinternetexamples-scmsdls-enc-logicscm)
- [`refrences/internet/examples_scm/sdls-ep-challenge-auth.scm`](#refrencesinternetexamples-scmsdls-ep-challenge-authscm)
- [`refrences/internet/examples_scm/sdls-ep-challenge-authenc.scm`](#refrencesinternetexamples-scmsdls-ep-challenge-authencscm)
- [`refrences/internet/examples_scm/sdls-ep-challenge.scm`](#refrencesinternetexamples-scmsdls-ep-challengescm)
- [`refrences/internet/examples_scm/sdls-ep-key-activation-auth.scm`](#refrencesinternetexamples-scmsdls-ep-key-activation-authscm)
- [`refrences/internet/examples_scm/sdls-ep-key-activation-authenc.scm`](#refrencesinternetexamples-scmsdls-ep-key-activation-authencscm)
- [`refrences/internet/examples_scm/sdls-ep-key-activation.scm`](#refrencesinternetexamples-scmsdls-ep-key-activationscm)
- [`refrences/internet/examples_scm/sdls-ep-otar-auth.scm`](#refrencesinternetexamples-scmsdls-ep-otar-authscm)
- [`refrences/internet/examples_scm/sdls-ep-otar-authenc.scm`](#refrencesinternetexamples-scmsdls-ep-otar-authencscm)
- [`refrences/internet/examples_scm/sdls-ep-otar-transmission.scm`](#refrencesinternetexamples-scmsdls-ep-otar-transmissionscm)
- [`refrences/internet/examples_scm/sdls-ep-sa-rekey-auth.scm`](#refrencesinternetexamples-scmsdls-ep-sa-rekey-authscm)
- [`refrences/internet/examples_scm/sdls-ep-sa-rekey-authenc.scm`](#refrencesinternetexamples-scmsdls-ep-sa-rekey-authencscm)
- [`refrences/internet/examples_scm/sdls-ep-sa-rekey.scm`](#refrencesinternetexamples-scmsdls-ep-sa-rekeyscm)
- [`refrences/internet/examples_scm/sdls-ep-sa-start-auth.scm`](#refrencesinternetexamples-scmsdls-ep-sa-start-authscm)
- [`refrences/internet/examples_scm/sdls-ep-sa-start-authenc.scm`](#refrencesinternetexamples-scmsdls-ep-sa-start-authencscm)
- [`refrences/internet/examples_scm/sdls-ep-sa-start.scm`](#refrencesinternetexamples-scmsdls-ep-sa-startscm)
- [`refrences/internet/examples_scm/sigenc.scm`](#refrencesinternetexamples-scmsigencscm)
- [`refrences/internet/examples_scm/sorted_epmo_acctnum.scm`](#refrencesinternetexamples-scmsorted-epmo-acctnumscm)
- [`refrences/internet/examples_scm/sts.scm`](#refrencesinternetexamples-scmstsscm)
- [`refrences/internet/examples_scm/sts_non_role.scm`](#refrencesinternetexamples-scmsts-non-rolescm)
- [`refrences/internet/examples_scm/sts_weakened_reflect.scm`](#refrencesinternetexamples-scmsts-weakened-reflectscm)
- [`refrences/internet/examples_scm/subatomic-open-closed-test-genrule.scm`](#refrencesinternetexamples-scmsubatomic-open-closed-test-genrulescm)
- [`refrences/internet/examples_scm/subatomic-open-closed.scm`](#refrencesinternetexamples-scmsubatomic-open-closedscm)
- [`refrences/internet/examples_scm/sync_locn_envelope.scm`](#refrencesinternetexamples-scmsync-locn-envelopescm)
- [`refrences/internet/examples_scm/sync_locn_envelope_no_auth.scm`](#refrencesinternetexamples-scmsync-locn-envelope-no-authscm)
- [`refrences/internet/examples_scm/targetterms1.scm`](#refrencesinternetexamples-scmtargetterms1scm)
- [`refrences/internet/examples_scm/targetterms2.scm`](#refrencesinternetexamples-scmtargetterms2scm)
- [`refrences/internet/examples_scm/targetterms6.scm`](#refrencesinternetexamples-scmtargetterms6scm)
- [`refrences/internet/examples_scm/targetterms8.scm`](#refrencesinternetexamples-scmtargetterms8scm)
- [`refrences/internet/examples_scm/thisthat.scm`](#refrencesinternetexamples-scmthisthatscm)
- [`refrences/internet/examples_scm/tickle-unique.scm`](#refrencesinternetexamples-scmtickle-uniquescm)
- [`refrences/internet/examples_scm/timestamping.scm`](#refrencesinternetexamples-scmtimestampingscm)
- [`refrences/internet/examples_scm/trust-anchor.scm`](#refrencesinternetexamples-scmtrust-anchorscm)
- [`refrences/internet/examples_scm/ugen-at.scm`](#refrencesinternetexamples-scmugen-atscm)
- [`refrences/internet/examples_scm/ugo.scm`](#refrencesinternetexamples-scmugoscm)
- [`refrences/internet/examples_scm/uncarried_keys.scm`](#refrencesinternetexamples-scmuncarried-keysscm)
- [`refrences/internet/examples_scm/unilateral.scm`](#refrencesinternetexamples-scmunilateralscm)
- [`refrences/internet/examples_scm/uniq-at.scm`](#refrencesinternetexamples-scmuniq-atscm)
- [`refrences/internet/examples_scm/uniq-gen-test.scm`](#refrencesinternetexamples-scmuniq-gen-testscm)
- [`refrences/internet/examples_scm/uo.scm`](#refrencesinternetexamples-scmuoscm)
- [`refrences/internet/examples_scm/wang-hash.scm`](#refrencesinternetexamples-scmwang-hashscm)
- [`refrences/internet/examples_scm/wang-key-hash.scm`](#refrencesinternetexamples-scmwang-key-hashscm)
- [`refrences/internet/examples_scm/weird.scm`](#refrencesinternetexamples-scmweirdscm)
- [`refrences/internet/examples_scm/wonthull.scm`](#refrencesinternetexamples-scmwonthullscm)
- [`refrences/internet/examples_scm/wonthull2.scm`](#refrencesinternetexamples-scmwonthull2scm)
- [`refrences/internet/examples_scm/wonthull3.scm`](#refrencesinternetexamples-scmwonthull3scm)
- [`refrences/internet/examples_scm/woolam.scm`](#refrencesinternetexamples-scmwoolamscm)
- [`refrences/internet/examples_scm/yahalom-6.3.6.scm`](#refrencesinternetexamples-scmyahalom-636scm)
- [`refrences/internet/examples_scm/yahalom-forward.scm`](#refrencesinternetexamples-scmyahalom-forwardscm)
- [`refrences/internet/examples_scm/yahalom.scm`](#refrencesinternetexamples-scmyahalomscm)
- [`refrences/internet/examples_scm/yes-or-no.scm`](#refrencesinternetexamples-scmyes-or-noscm)

---

### `refrences/internet/examples_scm/DH_hack.scm`

*sha256:`1dd27362fe4b` · 72 lines · 2.4 KB · lang:`scheme`*

```scheme
;; This file demonstrates a way to model DH keys in a limited way
;; within the Basic Crypto Algebra.  The idea is the following:
;; the pair (x, g^x) is represented as ((invk x), x), and similarly
;; for (y, g^y).  The owner of (invk x) computes (hash (invk x) y) and
;; the owner of (invk y) computes (hash x (invk y)).  We add an auxiliary
;; role (other protocols may need more auxiliary roles) that serves
;; to transform encryptions using (hash (invk x) y) into encryptions
;; using (hash x (invk y)).

;; This has the advantage that the adversary cannot decrypt these
;; messages if he does not have either (invk x) or (invk y).  However,
;; the presence of the auxiliary role makes it possible for the
;; adversary to decrypt the message by knowing either (invk x) or
;; (invk y).

;; It is currently unclear how well this solution will scale to larger
;; protocols which may need more auxiliary roles.  This also completely
;; ignores algebraic properties of DH and hence it excludes algebraic
;; attacks from consideration.

(herald "DH Hack" (bound 15))

(defprotocol DH_hack basic
  (defrole init1
    (vars (gcs name) (cek skey) (x y akey) (d data))
    (trace
     (send (enc x (enc cek (hash (invk x) y)) (enc d cek) (privk gcs))))
    (uniq-orig cek d x))
  (defrole resp
    (vars (gcs name) (cek skey) (x y akey) (d data))
    (trace
     (recv (enc x (enc cek (hash x (invk y))) (enc d cek) (privk gcs))))
    (non-orig (privk gcs)))
  (defrole commute
    (vars (gcs name) (cek skey) (x y akey) (d data) )
    (trace
     (recv (enc x (enc cek (hash (invk x) y)) (enc d cek) (privk gcs)))
     (send (enc x (enc cek (hash x (invk y))) (enc d cek) (privk gcs))))
    (non-orig (privk gcs))))

 (defskeleton DH_hack
  (vars (x y akey))
  (defstrand resp 1 (x x) (y y))
  (non-orig (invk x) (invk y)))

 (defskeleton DH_hack
  (vars (cek skey) (x y akey))
  (defstrand resp 1 (cek cek) (x x))
  (non-orig (invk x)))

(defskeleton DH_hack
  (vars (cek skey) (x y akey))
  (defstrand resp 1 (cek cek) (y y))
  (non-orig (invk y)))

(defskeleton DH_hack
  (vars (cek skey) (x y akey))
  (defstrand resp 1 (cek cek) (x x) (y y))
  (deflistener cek)
  (non-orig (invk x) (invk y)))

 (defskeleton DH_hack
  (vars (cek skey) (x y akey))
  (defstrand resp 1 (cek cek) (x x))
  (deflistener cek)
  (non-orig (invk x)))

(defskeleton DH_hack
  (vars (cek skey) (x y akey))
  (defstrand resp 1 (cek cek) (y y))
  (deflistener cek)
  (non-orig (invk y)))
```

---

### `refrences/internet/examples_scm/ab.scm`

*sha256:`1e3d93f7a82d` · 26 lines · 0.6 KB · lang:`scheme`*

```scheme
;;  Simple example of A-B cascading.
;;  Input should be a dead skeleton.
;;  Cascading occurs because roles A and B both seem to
;;  create progress, but nothing can ever produce their input in the
;;  correct form.

(defprotocol ab basic
  (defrole init (vars (x text) (k skey))
    (trace
     (send (enc x k))
     (recv (enc x x k)))
    (uniq-orig x)
    (non-orig k))
  (defrole A (vars (x text) (k skey))
    (trace
     (recv (enc "A" x k))
     (send (enc x x k))))
  (defrole B (vars (x text) (k skey))
    (trace
     (recv (enc "B" x k))
     (send (enc x x k))))
)

(defskeleton ab
  (vars (x text) (k skey))
  (defstrand init 2 (x x) (k k)))
```

---

### `refrences/internet/examples_scm/abc.scm`

*sha256:`67394bb26109` · 30 lines · 0.7 KB · lang:`scheme`*

```scheme
;;  Simple example of A-B-C cascading.
;;  Input should be a dead skeleton.
;;  Cascading occurs because roles A, B, and C seem to
;;  create progress, but nothing can ever produce their input in the
;;  correct form.

(defprotocol abc basic
  (defrole init (vars (x text) (k skey))
    (trace
     (send (enc x k))
     (recv (enc x x k)))
    (uniq-orig x)
    (non-orig k))
  (defrole A (vars (x text) (k skey))
    (trace
     (recv (enc "A" x k))
     (send (enc x x k))))
  (defrole B (vars (x text) (k skey))
    (trace
     (recv (enc "B" x k))
     (send (enc x x k))))
  (defrole C (vars (x text) (k skey))
    (trace
     (recv (enc "C" x k))
     (send (enc x x k))))
)

(defskeleton abc
  (vars (x text) (k skey))
  (defstrand init 2 (x x) (k k)))
```

---

### `refrences/internet/examples_scm/aik.scm`

*sha256:`de3554177295` · 30 lines · 1.0 KB · lang:`scheme`*

```scheme
(herald "Anonymous identity protocol from TCG")

(defprotocol aikprot basic
  (defrole ca
    (vars (mf name) (ek akey))
    (trace (send (enc "ekc" mf ek (privk mf))))
    (non-orig (invk ek)))
  (defrole tpm
    (vars (i x mf pc name) (ek k akey) (srk skey))
    (trace (recv (cat x i (enc "ekc" mf ek (privk mf))))
      (send (cat i k x (enc "ekc" mf ek (privk mf))))
      (recv (enc (enc "aic" i k x (privk pc)) ek))
      (send (cat (enc "aic" i k x (privk pc)) (enc k (invk k) srk))))
    (non-orig srk (invk ek))
    (uniq-orig k (invk k)))
  (defrole pca
    (vars (i x mf pc name) (ek k akey))
    (trace (recv (cat i k x (enc "ekc" mf ek (privk mf))))
      (send (enc (enc "aic" i k x (privk pc)) ek)))
    (non-orig (privk mf))))

(defskeleton aikprot
  (vars (i x mf pc name) (ek k akey) (srk skey))
  (defstrand tpm 4 (mf mf) (pc pc))
  (non-orig (privk pc)))

(defskeleton aikprot
  (vars (i x mf pc name) (ek k akey) (srk skey))
  (deflistener (enc "aic" i k x (privk pc)))
  (non-orig (privk pc)))
```

---

### `refrences/internet/examples_scm/atomic-open-closed.scm`

*sha256:`0aca95d4c358` · 416 lines · 10.4 KB · lang:`scheme`*

```scheme
(herald atomic-open-closed
	;; (try-old-strands)
	;; 	(check-nonces)
	;; 	(reverse-nodes)
	(bound 44))

(defmacro (dev-key-state d o k)
  (cat "st-k" d o k))

(defmacro (opened o)
  (cat o o))

(defmacro (closed o) o)

(defmacro (dev-state-opened d o)
  (cat "st" d (opened o)))

(defmacro (dev-state-closed d o)
  (cat "st" d (closed o)))

(defmacro (dev-state-any d o any)
  (cat "st" d any))

(defprotocol atomic-open-closed basic
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))
    (trace
     (recv start-ch (cat "power-up" d o k))
     (load lk old)
     (stor lk (dev-key-state d o k))
     (load ls old1)
     (stor ls (dev-state-closed d o))
     (send (enc "up" k)))
    (auth start-ch))

  (defrole owner-power-dev
    (vars (k skey) (d o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" d o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "open" d o n k))
     (recv n)))

  (defrole owner-close
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "close" d o n k))
     (recv n)))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (recv (enc "open" d o n k))
     (load lk (dev-key-state d o k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-opened d o))
     (send n)))

  (defrole dev-close
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (recv (enc "close" d o n k))
     (load lk (dev-key-state d o k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-closed d o))
     (send n)))

  (defrole dev-pass
    (vars (k skey) (n text) (d o name) (lk ls locn))
    (trace
     (recv (enc "may I pass" k))
     (load lk (dev-key-state d o k))
     (load ls (dev-state-opened d o))
     (send (enc "you may pass" n k)))
    (uniq-orig n))

  (defrole user-pass
    (vars (k skey) (n text) (d o name) (l locn))
    (trace
     (send (enc "may I pass" k))
     (recv (enc "you may pass" k))))

  (defrule gen-state-close
    (forall ((z strd) (d o name) (k skey))
	    (implies
	     (and (p "dev-close" z 1)
		  (p "dev-close" "d" z d)
		  (p "dev-close" "o" z o)
		  (p "dev-close" "k" z k)
		  (p "dev-close" "any" z (opened o)))
	     (gen-st (dev-state-opened d o)))))

  (defrule gen-state-pass
    (forall ((z strd) (d o name) (k skey))
	    (implies
	     (and (p "dev-pass" z 1)
		  (p "dev-pass" "d" z d)
		  (p "dev-pass" "o" z o)
		  (p "dev-pass" "k" z k))
	     (gen-st (dev-state-opened d o)))))

  (defrule gen-state-open
    (forall ((z strd) (d o k mesg))
	    (implies
	     (and (p "dev-open" "d" z d)
		  (p "dev-open" "o" z o)
		  (p "dev-open" "k" z k))
	     (gen-st (dev-key-state d o k)))))

  (defrule gen-state-close
    (forall ((z strd) (d o k mesg))
	    (implies
	     (and (p "dev-close" "d" z d)
		  (p "dev-close" "o" z o)
		  (p "dev-close" "k" z k))
	     (gen-st (dev-key-state d o k)))))

  (defrule gen-state-pass
    (forall ((z strd) (d o k mesg))
	    (implies
	     (and (p "dev-pass" "d" z d)
		  (p "dev-pass" "o" z o)
		  (p "dev-pass" "k" z k))
	     (and (gen-st (dev-key-state d o k))))))

   (defrule power-deliver-once
     (forall
      ((z1 z2 strd) (k skey))
      (implies
       (and (p "dev-up" z1 2)
 	   (p "dev-up" z2 2)
 	   (p "dev-up" "k" z1 k)
 	   (p "dev-up" "k" z2 k))
       (= z1 z2))))

   (defrule intro-same-dev-up
     (forall ((z strd) (lk ls locn))
	     (implies
	      (and (p "dev-up" "lk" z lk)
		   (p "dev-up" "ls" z ls))
	      (fact same-dev ls lk))))

   (defrule intro-same-dev-open
     (forall ((z strd) (lk ls locn))
	     (implies
	      (and (p "dev-open" "lk" z lk)
		   (p "dev-open" "ls" z ls))
	      (fact same-dev ls lk))))

   (defrule intro-same-dev-close
     (forall ((z strd) (lk ls locn))
	     (implies
	      (and (p "dev-close" "lk" z lk)
		   (p "dev-close" "ls" z ls))
	      (fact same-dev ls lk))))

   (defrule intro-same-dev-pass
     (forall ((z strd) (lk ls locn))
	     (implies
	      (and (p "dev-pass" "lk" z lk)
		   (p "dev-pass" "ls" z ls))
	      (fact same-dev ls lk))))

   (defrule same-dev-ls-lk
     (forall ((ls lk lk-0 locn))
	     (implies
	      (and (fact same-dev ls lk)
		   (fact same-dev ls lk-0))
	      (= lk lk-0))))

   (defrule same-dev-lk-ls
     (forall ((lk ls ls-0 locn))
	     (implies
	      (and (fact same-dev ls lk)
		   (fact same-dev ls-0 lk))
	      (= ls ls-0))))

   ;; Single-threaded registers
   (defrule single-thread-up-up
     (forall ((x y strd) (lk locn))
   	     (implies
   	      (and (p "dev-up" x 5)
   		   (p "dev-up" y 5)
   		   (p "dev-up" "lk" x lk)
   		   (p "dev-up" "lk" y lk))
   	      (or (= x y)
		  (prec x 4 y 1)
   		  (prec y 4 x 1)))))

   (defrule single-thread-up-open
     (forall ((x y strd) (ls locn))
   	     (implies
   	      (and (p "dev-up" x 5)
   		   (p "dev-open" y 4)
   		   (p "dev-up" "ls" x ls)
   		   (p "dev-open" "ls" y ls))
   	      (or (prec x 4 y 1)
   		  (prec y 3 x 1)))))

   (defrule single-thread-up-close
     (forall ((x y strd) (ls locn))
   	     (implies
   	      (and (p "dev-up" x 5)
   		   (p "dev-close" y 4)
   		   (p "dev-up" "ls" x ls)
   		   (p "dev-close" "ls" y ls))
   	      (or (prec x 4 y 1)
   		  (prec y 3 x 1)))))

   (defrule single-thread-open-open
     (forall ((x y strd) (ls locn))
   	     (implies
   	      (and (p "dev-open" x 4)
   		   (p "dev-open" y 4)
   		   (p "dev-open" "ls" x ls)
   		   (p "dev-open" "ls" y ls))
   	      (or (= x y)
   		  (prec x 3 y 1)
   		  (prec y 3 x 1)))))

   (defrule single-thread-ls-open-close
     (forall ((x y strd) (ls locn))
   	     (implies
   	      (and (p "dev-open" x 4)
   		   (p "dev-close" y 4)
   		   (p "dev-open" "ls" x ls)
   		   (p "dev-close" "ls" y ls))
   	      (or (prec x 3 y 1)
   		  (prec y 3 x 1)))))

   (defrule single-thread-close-close
     (forall ((x y strd) (ls locn))
   	     (implies
   	      (and (p "dev-close" x 4)
   		   (p "dev-close" y 4)
   		   (p "dev-close" "ls" x ls)
   		   (p "dev-close" "ls" y ls))
   	      (or (= x y)
   		  (prec x 3 y 1)
   		  (prec y 3 x 1)))))

   (defrule atomic-up-pass
     (forall ((x y strd) (lk locn))
   	     (implies
   	      (and (p "dev-up" x 5)
   		   (p "dev-pass" y 3)
   		   (p "dev-up" "lk" x lk)
   		   (p "dev-pass" "lk" y lk)
   		   (prec x 2 y 1))
   	      (prec x 4 y 1))))

   (defrule dev-up-completes
     (forall ((x strd))
	     (implies
	      (p "dev-up" x 2)
	      (p "dev-up" x 5))))

   (defrule dev-open-completes
     (forall ((x strd))
	     (implies
	      (p "dev-open" x 2)
	      (p "dev-open" x 4))))

   (defrule dev-close-completes
     (forall ((x strd))
	     (implies
	      (p "dev-close" x 2)
	      (p "dev-close" x 4))))

   (defrule dev-pass-completes
     (forall ((x strd))
	     (implies
	      (p "dev-pass" x 2)
	      (p "dev-pass" x 3))))

   (defrule dev-up-atomic1
     (forall ((x z strd) (i1 indx))
	     (implies
	      (and (p "dev-up" z 5)
		   (prec x i1 z 4))
	      (or (= x z)
		  (prec x i1 z 1)))))

   (defrule dev-up-atomic2
     (forall ((x z strd) (i1 indx))
	     (implies
	      (and (p "dev-up" z 5)
		   (prec z 1 x i1))
	      (or (= x z)
		  (prec z 4 x i1)))))

   (defrule dev-open-atomic1
     (forall ((x z strd) (i1 indx))
	     (implies
	      (and (p "dev-open" z 4)
		   (prec x i1 z 3))
	      (or (= x z)
		  (prec x i1 z 1)))))

   (defrule dev-open-atomic2
     (forall ((x z strd) (i1 indx))
	     (implies
	      (and (p "dev-open" z 4)
		   (prec z 1 x i1))
	      (or (= x z)
		  (prec z 3 x i1)))))

   (defrule dev-close-atomic1
     (forall ((x z strd) (i1 indx))
	     (implies
	      (and (p "dev-close" z 4)
		   (prec x i1 z 3))
	      (or (= x z)
		  (prec x i1 z 1)))))

   (defrule dev-close-atomic2
     (forall ((x z strd) (i1 indx))
	     (implies
	      (and (p "dev-close" z 4)
		   (prec z 1 x i1))
	      (or (= x z)
		  (prec z 3 x i1)))))

   (defrule dev-pass-atomic1
     (forall ((x z strd) (i1 indx))
	     (implies
	      (and (p "dev-pass" z 3)
		   (prec x i1 z 2))
	      (or (= x z)
		  (prec x i1 z 1)))))

   (defrule dev-pass-atomic2
     (forall ((x z strd) (i1 indx))
	     (implies
	      (and (p "dev-pass" z 3)
		   (prec z 1 x i1))
	      (or (= x z)
		  (prec z 2 x i1)))))

;;      (defrule leadsto-la
;;        (forall ((z1 z2 strd) (i1 i2 indx))
;;     	     (implies
;;     	      (leads-to z1 i1 z2 i2)
;;     	      (fact la z1 i1 z2 i2)))
;;        (comment this is a rule comment))
;;
;;      (defrule commpair-cp
;;        (forall ((z1 z2 strd) (i1 i2 indx))
;;     	     (implies
;;     	      (comm-pr z1 i1 z2 i2)
;;     	      (fact cp z1 i1 z2 i2)))
;;        (comment this is a rule comment))
;;
;;      (defrule prec-pr
;;        (forall ((z1 z2 strd) (i1 i2 indx))
;;     	     (implies
;;     	      (prec z1 i1 z2 i2)
;;     	      (fact pr z1 i1 z2 i2)))
;;        (comment this is a rule comment))

   ;; (defrule atomic-simpl
   ;;   (forall ((x z strd) (i1 i2 i3 indx))
   ;; 	     (implies
   ;; 	      (and (fact atomic z i1 i2)
   ;; 		   (prec x i3 z i1))
   ;; 	      (or (= x z)
   ;; 		  (prec x i3 z i1)))))

   ;; (defrule atomic-simpl2
   ;;   (forall ((x z strd) (i1 i2 i3 indx))
   ;; 	     (implies
   ;; 	      (and (fact atomic z i1 i2)
   ;; 		   (prec z i1 x i3))
   ;; 	      (or
   ;; 	       (= x z)
   ;; 	       (prec z i1 x i3)))))

  )

(defskeleton atomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (deflistener k)
  (uniq-orig k))

(defskeleton atomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  ;; (defstrand owner-power-dev 2 (k k))
  (defstrand dev-pass 4 (k k))
  ;; (uniq-orig k)
  )

(defskeleton atomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (defstrand dev-pass 4 (k k))
  (uniq-orig k))

;; (defskeleton atomic-open-closed
;;   (vars (old old1 any mesg) (n n-0 text) (d o name) (k k-0 skey)
;;     (start-ch chan) (ls lk ls-0 lk-0 locn))
;;   (defstrand owner-power-dev 2 (d d) (o o) (k k) (start-ch start-ch))
;;   (defstrand dev-pass 4 (n n) (d d) (o o) (k k) (lk lk) (ls ls))
;;   (defstrand dev-up 6 (old old) (old1 old1) (d d) (o o) (k k)
;;     (start-ch start-ch) (lk lk) (ls ls-0))
;;   (defstrand user-pass 1 (k k))
;;   (defstrand dev-open 4 (any any) (n n-0) (d d) (o o) (k k-0) (lk lk-0)
;;     (ls ls))
;;   (precedes ((0 0) (2 0)) ((2 2) (1 0)) ((2 5) (0 1)) ((3 0) (1 1))
;;     ((4 3) (1 2)))
;;   (uniq-orig n k))
```

---

### `refrences/internet/examples_scm/attest.scm`

*sha256:`fc0ffff10b77` · 190 lines · 5.0 KB · lang:`scheme`*

```scheme
(herald attest-door)

(defprotocol attest-door basic
  (defrole appraise
    (vars (d p a akey) (n text))
    (trace
     (recv (enc (enc d n (invk p)) a))
     (send (enc n a p)))
    (comment "The appraiser for the door"))
  (defrole person
    (vars (d p a akey) (k skey) (n t text))
    (trace
     (send (enc (enc d n (invk p)) a))
     (recv (enc n a p))
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t))
    (uniq-orig n k)
    (comment "Person requesting door entry"))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t))
    (uniq-orig t))
  (defrole squealer
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send k))
    (comment "Fake door"))
  (defrule yes
    (forall ((z strd) (a akey))
	    (implies
	     (and (p "appraise" z 2)
		  (p "appraise" "a" z a)
		  (non (invk a)))
	     (exists ((d akey))
		     (and (p "appraise" "d" z d)
			  (non (invk d))))))
    (comment "Appraisal succeeded"))
  (comment "Door attestations protocol"))

(defskeleton attest-door
  (vars (p a akey))
  (defstrand person 5 (p p) (a a))
  (non-orig (invk p) (invk a))
  (comment "Analyze from the person's perspective"))

(defskeleton attest-door
  (vars (p d a akey))
  (defstrand door 3 (p p) (d d))
  (non-orig (invk d) (invk p))
  (comment "Analyze from the door's perspective"))

(defprotocol attest-door-trust basic
  (defrole appraise
    (vars (d p a akey) (n text))
    (trace
     (recv (enc (enc d n (invk p)) a))
     (send (enc n a p)))
    (comment "The appraiser for the door"))
  (defrole person
    (vars (d p a akey) (k skey) (n t text))
    (trace
     (send (enc (enc d n (invk p)) a))
     (recv (enc n a p))
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t))
    (uniq-orig n k)
    (comment "Person requesting door entry"))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t))
    (uniq-orig t))
  (defrole squealer
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send k))
    (comment "Fake door"))
  (defrule yes
    (forall ((z strd) (a akey))
	    (implies
	     (and (p "appraise" z 2)
		  (p "appraise" "a" z a)
		  (non (invk a)))
	     (exists ((d akey))
		     (and (p "appraise" "d" z d)
			  (non (invk d))))))
    (comment "Appraisal succeeded"))
  (defrule trust
    (forall ((z w strd) (d akey))
	    (implies
	     (and (p "appraise" z 2)
		  (p "appraise" "d" z d)
		  (p "squealer" w 2)
		  (p "squealer" "d" w d))
	     (false)))
    (comment "Passing attestation means not a squealer"))
  (comment "Door attestations protocol with attestation"))

(defskeleton attest-door-trust
  (vars (p a akey))
  (defstrand person 5 (p p) (a a))
  (non-orig (invk p) (invk a))
  (comment "Analyze from the person's perspective"))

(defskeleton attest-door-trust
  (vars (p d akey))
  (defstrand door 3 (p p) (d d))
  (non-orig (invk d) (invk p))
  (comment "Analyze from the door's perspective"))

(defprotocol attest-door-trust-attest basic
  (defrole appraise
    (vars (d p a akey) (n text))
    (trace
     (recv (enc (enc d n (invk p)) a))
     (send (enc n a p)))
    (comment "The appraiser for the door"))
  (defrole person
    (vars (d p a akey) (k skey) (n t text))
    (trace
     (send (enc (enc d n (invk p)) a))
     (recv (enc n a p))
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t))
    (uniq-orig n k)
    (comment "Person requesting door entry"))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t))
    (uniq-orig t))
  (defrole squealer
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send k))
    (comment "Fake door"))
  (defrule yes
    (forall ((z strd) (a akey))
	    (implies
	     (and (p "appraise" z 2)
		  (p "appraise" "a" z a)
		  (non (invk a)))
	     (exists ((d akey))
		     (and (p "appraise" "d" z d)
			  (non (invk d))))))
    (comment "Appraisal succeeded"))
  (defrule trust
    (forall ((z w strd) (d akey))
	    (implies
	     (and (p "appraise" z 2)
		  (p "appraise" "d" z d)
		  (p "squealer" w 2)
		  (p "squealer" "d" w d))
	     (false)))
    (comment "Passing attestation means not a squealer"))
  (defrule uncompromised-people-choose-uncompromised-appraisers
    (forall ((z strd) (a p akey))
	    (implies
	     (and (p "person" z 3)
		  (p "person" "p" z p)
		  (p "person" "a" z a)
		  (non (invk p)))
	     (non (invk a)))))

  (comment "Door attestations protocol with attestation and reliable persons"))

(defskeleton attest-door-trust-attest
  (vars (p a akey))
  (defstrand person 5 (p p) (a a))
  (non-orig (invk p) (invk a))
  (comment "Analyze from the person's perspective"))

(defskeleton attest-door-trust-attest
  (vars (p d akey))
  (defstrand door 3 (p p) (d d))
  (non-orig (invk d) (invk p))
  (comment "Analyze from the door's perspective"))
```

---

### `refrences/internet/examples_scm/auth-enc.scm`

*sha256:`f2ddbb62150b` · 18 lines · 0.4 KB · lang:`scheme`*

```scheme
(herald auth-enc)

(defprotocol auth-enc basic
  (defrole init
    (vars (n text) (k skey) (ch chan))
    (trace (send ch (enc n k)) (send ch (cat n k)))
    (uniq-orig n k)
    (inputs ch))
  (defrole resp
    (vars (n text) (k skey) (ch chan))
    (trace (recv ch (enc n k)) (recv ch (cat n k)))
    (inputs ch)
    (outputs n)))

(defskeleton auth-enc
  (vars (ch chan))
  (defstrand resp 2 (ch ch))
  (auth ch))
```

---

### `refrences/internet/examples_scm/auth-hash.scm`

*sha256:`58e88956cdec` · 18 lines · 0.4 KB · lang:`scheme`*

```scheme
(herald auth-hash)

(defprotocol auth-hash basic
  (defrole init
    (vars (n text) (ch chan))
    (trace (send ch (hash n)) (send ch n))
    (uniq-orig n)
    (inputs ch))
  (defrole resp
    (vars (n text) (ch chan))
    (trace (recv ch (hash n)) (recv ch n))
    (inputs ch)
    (outputs n)))

(defskeleton auth-hash
  (vars (ch chan))
  (defstrand resp 2 (ch ch))
  (auth ch))
```

---

### `refrences/internet/examples_scm/blanchet-strandmax.scm`

*sha256:`5caa67bbda5b` · 131 lines · 3.9 KB · lang:`scheme`*

```scheme
(herald "Blanchet's Simple Example Protocol (strand max)"
  (comment "There is a flaw in this protocol by design"))

(defprotocol blanchet-max basic
  (defrole init
    (vars (a b name) (s skey) (d data))
    (trace
     (send (enc (enc s (privk a)) (pubk b)))
     (recv (enc d s))))
  (defrole resp
    (vars (a b name) (s skey) (d data))
    (trace
     (recv (enc (enc s (privk a)) (pubk b)))
     (send (enc d s))))
  (comment "Blanchet's protocol using named asymmetric keys"))

(defskeleton blanchet-max
  (vars (a b name) (s skey) (d data))
  (defstrandmax init (a a) (b b) (s s) (d d))
  (non-orig (privk b))
  (uniq-orig s)
  (comment "Analyze from the initiator's perspective"))

(defskeleton blanchet-max
  (vars (a b name) (s skey) (d data))
  (defstrandmax init (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk b))
  (uniq-orig s d)
  (comment "From the initiator's perspective, is the secret leaked?"))

(defskeleton blanchet-max
  (vars (a b name) (s skey) (d data))
  (defstrandmax resp (a a) (b b) (s s) (d d))
  (non-orig (privk a) (privk b))
  (uniq-orig s)
  (comment "Analyze from the responder's perspective"))

(defskeleton blanchet-max
  (vars (a b name) (s skey) (d data))
  (defstrandmax resp (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk a) (privk b))
  (uniq-orig s d)
  (comment "From the responders's perspective, is the secret leaked?"))

(defprotocol blanchet-max-akey basic
  (defrole init
    (vars (a b akey) (s skey) (d data))
    (trace
     (send (enc (enc s (invk a)) b))
     (recv (enc d s))))
  (defrole resp
    (vars (a b akey) (s skey) (d data))
    (trace
     (recv (enc (enc s (invk a)) b))
     (send (enc d s))))
  (comment "Blanchet's protocol using unnamed asymmetric keys"))

(defskeleton blanchet-max-akey
  (vars (a b akey) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (non-orig (invk b))
  (uniq-orig s)
  (comment "Analyze from the initiator's perspective"))

(defskeleton blanchet-max-akey
  (vars (a b akey) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (invk b))
  (uniq-orig s d)
  (comment "From the initiator's perspective, is the secret leaked?"))

(defskeleton blanchet-max-akey
  (vars (a b akey) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (non-orig (invk a) (invk b))
  (uniq-orig s)
  (comment "Analyze from the responder's perspective"))

(defskeleton blanchet-max-akey
  (vars (a b akey) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (invk a) (invk b))
  (uniq-orig s d)
  (comment "From the responders's perspective, is the secret leaked?"))

(defprotocol blanchet-max-fixed basic
  (defrole init
    (vars (a b name) (s skey) (d data))
    (trace
     (send (enc (enc s b (privk a)) (pubk b)))
     (recv (enc d s))))
  (defrole resp
    (vars (a b name) (s skey) (d data))
    (trace
     (recv (enc (enc s b (privk a)) (pubk b)))
     (send (enc d s))))
  (comment "Fixed Blanchet's protocol using named asymmetric keys"))

(defskeleton blanchet-max-fixed
  (vars (a b name) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (non-orig (privk b))
  (uniq-orig s)
  (comment "Analyze from the initiator's perspective"))

(defskeleton blanchet-max-fixed
  (vars (a b name) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk b))
  (uniq-orig s d)
  (comment "From the initiator's perspective, is the secret leaked?"))

(defskeleton blanchet-max-fixed
  (vars (a b name) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (non-orig (privk a) (privk b))
  (uniq-orig s)
  (comment "Analyze from the responder's perspective"))

(defskeleton blanchet-max-fixed
  (vars (a b name) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk a) (privk b))
  (uniq-orig s d)
  (comment "From the responders's perspective, is the secret leaked?"))
```

---

### `refrences/internet/examples_scm/blanchet.scm`

*sha256:`2f16c32a28d3` · 88 lines · 2.6 KB · lang:`scheme`*

```scheme
(herald "Blanchet's Simple Example Protocol"
  (comment "There is a flaw in this protocol by design"))

(defprotocol blanchet basic
  (defrole init
    (vars (a b name) (s skey) (d data))
    (trace
     (send (enc (enc s (privk a)) (pubk b)))
     (recv (enc d s))))
  (defrole resp
    (vars (a b name) (s skey) (d data))
    (trace
     (recv (enc (enc s (privk a)) (pubk b)))
     (send (enc d s))))
  (comment "Blanchet's protocol using named asymmetric keys"))

(defskeleton blanchet
  (vars (a b name) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (non-orig (privk b))
  (uniq-orig s)
  (comment "Analyze from the initiator's perspective"))

(defskeleton blanchet
  (vars (a b name) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk b))
  (uniq-orig s d)
  (comment "From the initiator's perspective, is the secret leaked?"))

(defskeleton blanchet
  (vars (a b name) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (non-orig (privk a) (privk b))
  (uniq-orig s)
  (comment "Analyze from the responder's perspective"))

(defskeleton blanchet
  (vars (a b name) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk a) (privk b))
  (uniq-orig s d)
  (comment "From the responders's perspective, is the secret leaked?"))

(defprotocol blanchet-fixed basic
  (defrole init
    (vars (a b name) (s skey) (d data))
    (trace
     (send (enc (enc s b (privk a)) (pubk b)))
     (recv (enc d s))))
  (defrole resp
    (vars (a b name) (s skey) (d data))
    (trace
     (recv (enc (enc s b (privk a)) (pubk b)))
     (send (enc d s))))
  (comment "Fixed Blanchet's protocol using named asymmetric keys"))

(defskeleton blanchet-fixed
  (vars (a b name) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (non-orig (privk b))
  (uniq-orig s)
  (comment "Analyze from the initiator's perspective"))

(defskeleton blanchet-fixed
  (vars (a b name) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk b))
  (uniq-orig s d)
  (comment "From the initiator's perspective, is the secret leaked?"))

(defskeleton blanchet-fixed
  (vars (a b name) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (non-orig (privk a) (privk b))
  (uniq-orig s)
  (comment "Analyze from the responder's perspective"))

(defskeleton blanchet-fixed
  (vars (a b name) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (deflistener d)
  (non-orig (privk a) (privk b))
  (uniq-orig s d)
  (comment "From the responders's perspective, is the secret leaked?"))
```

---

### `refrences/internet/examples_scm/bug_example.scm`

*sha256:`68f92ca2c76a` · 43 lines · 1.1 KB · lang:`scheme`*

```scheme
(herald bug_example (bound 20))

(defprotocol bug_example basic
  (defrole init (vars (x y akey))
    (trace
     (send (enc y (hash x (invk y)))))
    (non-orig (invk y) (invk x)))
  (defrole resp (vars (x y akey))
    (trace
     (recv (enc y (hash (invk x) y))))
    (non-orig (invk x) (invk y)))
  (defrole flip (vars (k k1 k2 akey))
    (trace
     (recv (enc k (hash k1 k2)))
     (send (enc k (hash (invk k1) (invk k2)))))))

(defskeleton bug_example
  (vars (x y akey))
  (defstrand resp 1 (x x) (y y)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defprotocol bug_example basic
  (defrole init (vars (x y akey))
    (trace
     (send (enc y (hash x (invk y)))))
    (non-orig (invk y) (invk x)))
  (defrole resp (vars (x y akey))
    (trace
     (recv (enc y (hash (invk x) y))))
    (non-orig (invk x) (invk y)))
  (defrole flip1 (vars (k k1 k2 akey))
    (trace
     (recv (enc k (hash (invk k1) k2)))
     (send (enc k (hash k1 (invk k2))))))
  (defrole flip2 (vars (k k1 k2 akey))
    (trace
     (recv (enc k (hash k1 (invk k2))))
     (send (enc k (hash (invk k1) k2))))))

(defskeleton bug_example
  (vars (x y akey))
  (defstrand resp 1 (x x) (y y)))
```

---

### `refrences/internet/examples_scm/cert_lang.scm`

*sha256:`f2199b4592dc` · 44 lines · 1.4 KB · lang:`scheme`*

```scheme
(herald cert-lang)

(defprotocol cert-uni basic
  (defrole certify
    (vars (ch chan) (subj ca name) (pk akey) (serial data))
    (trace
      (send ch
        (cert (cert-body subj serial pk) (privk "cert" ca))))
    (inputs ch subj pk serial (privk "cert" ca)))
  (defrole init
    (vars (ch-ca ch-r chan) (subj ca name) (pk akey)
      (serial data) (chal text))
    (trace
      (recv ch-ca
        (cert (cert-body subj serial pk) (privk "cert" ca)))
      (send ch-r (enc "challenge" chal pk))
      (recv ch-r chal))
    (uniq-orig chal)
    (inputs ch-ca ch-r subj (pubk "cert" ca))
    (outputs chal))
  (defrole resp
    (vars (ch-ca ch-i chan) (subj ca name) (pk akey)
      (serial data) (chal text))
    (trace
      (recv ch-ca
        (cert (cert-body subj serial pk) (privk "cert" ca)))
      (recv ch-i (enc "challenge" chal pk))
      (send ch-i chal))
    (inputs ch-ca ch-i subj (pubk "cert" ca) (invk pk))
    (outputs chal))
  (defrule certified-keys-uncompromised
    (forall ((zca strd) (subj ca name) (pk akey))
      (implies
        (and (p "certify" zca 1)
          (p "certify" "subj" zca subj)
          (p "certify" "ca" zca ca)
          (p "certify" "pk" zca pk) (non (privk "cert" ca)))
        (non (invk pk)))))
   (lang (cert sign) (cert-body (tupl 3))))

(defskeleton cert-uni
  (vars (subj ca name) (pk akey) (serial data) (chal text))
  (defstrand init 3 (ca ca) (chal chal))
  (non-orig (privk "cert" ca)))
```

---

### `refrences/internet/examples_scm/chan-envelope.scm`

*sha256:`34a633cf224a` · 212 lines · 6.5 KB · lang:`scheme`*

```scheme
(herald "Envelope Protocol With Channels" (bound 15))

;;; This file analyzes the Envelope Protocol using three rules sets.
;;; For each rule set, it checks three scenarios.  In every scenario,
;;; an Alice strand runs to completion.  In the first scenario, the
;;; obtain token is listened for.  In the second, a listener for the
;;; refusal token is included.  In the third scenario, both listeners
;;; are included.  The third scenario should be impossible, but rules
;;; are required to accurately model state.
;;;
;;; The first rule set is empty and the answer to the third scenario
;;; shows a case is which the TPM's PCR state splits.  The second rule
;;; set forces TPM extends to be linearly ordered.  However, in this
;;; case, there are two TPMs when there should be one as Alice uses
;;; one TPM storage key to communicate with both TPMs.  The final rule
;;; set includes a rule about storage keys and thus accurately models
;;; state.
;;;
;;; Macros are used to avoid copying roles and scenarios.

;; This is the refusal token
(defmacro (refuse n v k aik)
  (enc "quote" (hash (hash "0" n) "refuse") (enc v k) aik))

;;; This protocol tracks the TPM's PCR state
;;; by sending a message with the current PCR
;;; value encrypted by a hashed secret key.
;;; The hash is used to prevent a confusion with
;;; the key for an encrypted session.

(defmacro (roles)
  (^
   ;; Power on sets the pcr to 0
   (defrole tpm-power-on
     (vars (c chan))
     (trace
      (recv "power on")
      (send c "0"))
     (conf c)
     (auth c))

   ;; The extend command takes the value to
   ;; extend and the current PCR value (in the
   ;; form of a message encrypted with the special
   ;; PCR state key) and produces the hash of the
   ;; two values (by sending it encrypted in the
   ;; special PCR state key).
   (defrole tpm-extend
     (vars (value current-value mesg) (c chan))
     (trace
      (recv (cat "extend" value))
      (recv c current-value)		  ;; MSR lhs (deleted)
      (send c (hash current-value value)) ;; MSR rhs
      (send "ext ok"))
     (conf c)
     (auth c))

   ;; The extend command can also occur within an
   ;; encrypted session.  We assume some session key already exists
   (defrole tpm-extend-enc
     (vars (value current-value mesg) (esk skey) (c chan))
     (trace
      (recv (enc "extend" value esk))
      (recv c current-value)		  ;; MSR lhs (deleted)
      (send c (hash current-value value)) ;; MSR rhs
      (send "ext ok"))
     (non-orig esk)
     (conf c)
     (auth c))

   ;; The TPM must retrieve the current pcr value.  Notice that
   ;; the nonce is of sort mesg, which allows non-atomic values.
   (defrole tpm-quote
     (vars (nonce current-value mesg) (c chan) (aik akey))
     (trace
      (recv (cat "quote" nonce))
      (recv c current-value) ;; MSR lhs (not deleted)
      (send (enc "quote" current-value nonce aik)))
     (non-orig aik)
     (conf c)
     (auth c))

   ;; This role creates a key whose use is restricted to a
   ;; requested pcr value (since we only model one pcr).
   ;; It doesn't create or change any TPM state.
   (defrole tpm-create-key
     (vars (k aik akey) (pcrval mesg) (esk skey))
     (trace
      (recv (enc "create key" pcrval esk)) ;; encryption prevents weird shapes
      (send (enc "created" k pcrval aik)));; no tpm state is set
     (uniq-orig k)
     (non-orig (invk k) aik esk))

   ;; This role receives an encryption and a previously
   ;; made key structure that restricts the decryption key
   ;; to be used with a certain pcr value.  It retrieves the
   ;; current value and checks that it matches before decrypting.
   (defrole tpm-decrypt
     (vars (m pcrvals mesg) (k aik akey) (c chan))
     (trace
      (recv (cat "decrypt" (enc m k)))
      (recv (enc "created" k pcrvals aik))
      (recv c pcrvals) ;; MSR lhs (not deleted)
      (send m))
     (non-orig aik)
     (conf c)
     (auth c))

   ;; Alice extends a pcr with a fresh nonce in an encrypted
   ;; session.  She has the TPM create a new key whose use is
   ;; bound to the hash of pcr value she just created with the
   ;; string "obtain".  She then encrypts her fresh secret with
   ;; this newly created key.
   (defrole alice
     (vars (n v data) (esk skey) (k aik akey))
     (trace
      (send (enc "extend" n esk))
      (send (enc "create key" (hash (hash "0" n) "obtain") esk))
      (recv (enc "created" k (hash (hash "0" n) "obtain") aik))
      (send (enc v k)))
     (uniq-orig n v)
     (non-orig aik esk))))

(defprotocol envelope basic
  (roles))

(defskeleton envelope
  (vars (v data))
  (deflistener v)
  (defstrand alice 4 (v v)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (deflistener v)
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defprotocol envelope basic
  (roles)

  (defrule ordered-extends
    (forall ((y z strd) (c chan))
	    (implies
	     (and (p "tpm-extend" y 3)
		  (p "tpm-extend" z 3)
		  (p "tpm-extend" "c" y c)
		  (p "tpm-extend" "c" z c))
	     (or (= y z)
		 (prec y 2 z 3)
		 (prec z 2 y 3))))))

(defskeleton envelope
  (vars (v data))
  (deflistener v)
  (defstrand alice 4 (v v)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (deflistener v)
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defprotocol envelope basic
  (roles)

  (defrule ordered-extends
    (forall ((y z strd) (c chan))
	    (implies
	     (and (p "tpm-extend" y 3)
		  (p "tpm-extend" z 3)
		  (p "tpm-extend" "c" y c)
		  (p "tpm-extend" "c" z c))
	     (or (= y z)
		 (prec y 2 z 3)
		 (prec z 2 y 3)))))

  (defrule esk-same-as-chan
    (forall ((y z strd) (esk skey) (c c-0 chan))
	    (implies
	     (and (p "tpm-extend-enc" y 3)
		  (p "tpm-extend-enc" z 3)
		  (p "tpm-extend-enc" "esk" y esk)
		  (p "tpm-extend-enc" "esk" z esk)
		  (p "tpm-extend-enc" "c" y c)
		  (p "tpm-extend-enc" "c" z c-0))
	     (= c c-0)))))

(defskeleton envelope
  (vars (v data))
  (deflistener v)
  (defstrand alice 4 (v v)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (deflistener v)
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))
```

---

### `refrences/internet/examples_scm/chan-perrig-song.scm`

*sha256:`28d099dc459d` · 48 lines · 1.0 KB · lang:`scheme`*

```scheme
(herald perrig-song)

(defprotocol perrig-song basic
  (defrole init
    (vars (na nb text) (a b name) (c chan))
    (trace
     (send na)
     (recv c (cat na nb a b))
     (send nb)))

  (defrole resp
    (vars (na nb text) (a b name) (c chan))
    (trace
     (recv na)
     (send c (cat na nb a b))
     (recv nb))))

;;; this query should bring in a matching
;;; run of resp of height 2.

(defskeleton perrig-song
  (vars (na nb text) (a b name) (c chan))
  (defstrand init 2 (na na) (c c))
  (uniq-orig na)
  (auth c))

;;; this query should bring in a matching
;;; run of init of height 3.

(defskeleton perrig-song
  (vars (na nb text) (a b name) (c chan))
  (defstrand resp 3 (nb nb) (c c))
  (uniq-orig nb)
  (conf c))

;;; these two should be realized as-is.

(defskeleton perrig-song
  (vars (na nb text) (a b name) (c chan))
  (defstrand init 2 (na na) (c c))
  (uniq-orig na)
  (conf c))

(defskeleton perrig-song
  (vars (na nb text) (a b name) (c chan))
  (defstrand resp 3 (nb nb) (c c))
  (uniq-orig nb)
  (auth c))
```

---

### `refrences/internet/examples_scm/chan-unilateral.scm`

*sha256:`65050edbf09c` · 61 lines · 1.3 KB · lang:`scheme`*

```scheme
(herald chan-unilateral)

;; Unilateral authentication using channels with differing assumptions.

(defprotocol unilateral basic
  (defrole init
     (vars (n text) (ch chan))
     (trace
      (send ch n)
      (recv n))
     (uniq-orig n))
  (defrole resp
     (vars (n text) (ch chan))
     (trace
      (recv ch n)			; bogus version was:  (cat ch n)
      (send n)))
  (comment "Unilateral protocol using channels with differing assumptions"))

(defskeleton unilateral
   (vars (ch chan))
   (defstrand init 2 (ch ch)))

(defskeleton unilateral
   (vars (ch chan))
   (defstrand init 2 (ch ch))
   (auth ch))

(defskeleton unilateral
   (vars (ch chan))
   (defstrand init 2 (ch ch))
   (conf ch))

(defskeleton unilateral
   (vars (ch chan))
   (defstrand init 2 (ch ch))
   (auth ch)
   (conf ch))

(defskeleton unilateral
  (vars (n text) (ch chan))
  (defstrand resp 2 (n n) (ch ch))
  (pen-non-orig n))

(defskeleton unilateral
  (vars (n text) (ch chan))
  (defstrand resp 2 (n n) (ch ch))
  (pen-non-orig n)
  (auth ch))

(defskeleton unilateral
  (vars (n text) (ch chan))
  (defstrand resp 2 (n n) (ch ch))
  (pen-non-orig n)
  (conf ch))

(defskeleton unilateral
  (vars (n text) (ch chan))
  (defstrand resp 2 (n n) (ch ch))
  (pen-non-orig n)
  (auth ch)
  (conf ch))
```

---

### `refrences/internet/examples_scm/chan-yahalom-role-decl.scm`

*sha256:`01f7233171d9` · 78 lines · 2.2 KB · lang:`scheme`*

```scheme
(herald "Yahalom Protocol Without Forwarding" (bound 15))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey) (ch3 chan))
    (trace (send (cat a n-a))
	   (recv ch3 (cat a b k n-a n-b))
	   (send (enc n-b k)))
    (auth ch3))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))
    (trace (recv (cat a n-a))
	   (send ch1 (cat a b n-a n-b))
	   (recv ch2 (cat a b k))
	   (recv (enc n-b k)))
    (auth ch2))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
    (trace (recv ch1 (cat a b n-a n-b))
	   (send ch3 (cat a b k n-a n-b))
	   (send ch2 (cat a b k)))
    (conf ch3 ch2)
    (uniq-orig k)))

;;; How much do we know assuming that the resp had a run, which
;;; because of the role declaration is necessarily using an
;;; authenticated channel ch2?  We also assume the responder's nonce
;;; is freshly chosen.

(defskeleton yahalom
  (vars (a b c name) (n-b text) (ch1 ch2 chan))
  (defstrand resp 4 (n-b n-b))
  (uniq-orig n-b))

(defskeleton yahalom
  (vars (a b c name) (k skey) (n-b text) (ch1 ch2 chan))
  (defstrand resp 4 (k k) (n-b n-b))
  (deflistener k)
  (uniq-orig n-b))

;;; Let's turn now to the initiator's point of view:

(defskeleton yahalom
  (vars (a b c name) (n-a text) (k skey) (ch3 chan))
  (defstrand init 3 (n-a n-a))
  (uniq-orig n-a))

(defskeleton yahalom
  (vars (a b c name) (n-a text) (k skey) (ch3 chan))
  (defstrand init 3 (k k))
  (deflistener k))

(defskeleton yahalom
  (vars (a b c name) (n-a text) (k skey) (ch3 chan))
  (defstrand init 3 (k k) (n-a n-a))
  (defstrand resp 3 (k k))
  (uniq-orig n-a))

(defskeleton yahalom
  (vars (a b c name) (n-a text) (k skey) (ch3 chan))
  (defstrand init 3 (k k) (n-a n-a))
  (defstrand resp 4 (k k))
  (uniq-orig n-a))

;;; Finally, the server knows only that the responder has requested a
;;; session key.

(defskeleton yahalom
  (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
  (defstrand serv 3))

;;; However, the server can be sure that the session key will not be
;;; disclosed.

(defskeleton yahalom
  (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
  (defstrand serv 3 (k k))
  (deflistener k))
```

---

### `refrences/internet/examples_scm/chan-yahalom.scm`

*sha256:`e3d108aed772` · 129 lines · 4.3 KB · lang:`scheme`*

```scheme
(herald "Yahalom Protocol Without Forwarding" (bound 15))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey) (ch3 chan))
    (trace (send (cat a n-a))
	   (recv ch3 (cat a b k n-a n-b))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))
    (trace (recv (cat a n-a))
	   (send ch1 (cat a b n-a n-b))
	   (recv ch2 (cat a b k))
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
    (trace (recv ch1 (cat a b n-a n-b))
	   (send ch3 (cat a b k n-a n-b))
	   (send ch2 (cat a b k)))
    (uniq-orig k)))

;;; How much do we know assuming that the resp had a run with an
;;; authenticated channel ch2?  We also assume the responder's nonce
;;; is freshly chosen.

(defskeleton yahalom
  (vars (a b c name) (n-b text) (ch1 ch2 chan))
  (defstrand resp 4 (a a) (b b) (n-b n-b) (ch1 ch1) (ch2 ch2))
  (auth ch2)
  (uniq-orig n-b))

;;; This is the answer to the previous question, to which we have
;;; added the assumptions that ch2 and ch3, used by the key server to
;;; distribute the key, are confidential channels.  In this case, we
;;; find *almost* all we would expect.

(defskeleton yahalom
  (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b name)
    (ch1 ch2 ch1-0 ch3 chan))
  (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (ch1 ch1)
    (ch2 ch2))
  (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (a a) (b b)
    (ch1 ch1-0) (ch2 ch2) (ch3 ch3))
  (precedes ((1 2) (0 2)))
  (uniq-orig k n-b)
  (auth ch2)
  (conf ch2 ch3))

;;; This is the answer to the previous question, together with the
;;; assumption that the server's request channel is an authenticated
;;; channel.  This yields all of the desired result, including the
;;; fact that the channels used by the server and the responder agree:
;;; ch1-0 = ch1.

(defskeleton yahalom
  (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b name)
    (ch1 ch2 ch1-0 ch3 chan))
  (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (ch1 ch1)
    (ch2 ch2))
  (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (a a) (b b)
    (ch1 ch1-0) (ch2 ch2) (ch3 ch3))
  (uniq-orig k n-b)
  (auth ch2 ch1-0)
  (conf ch2 ch3))

;;; In particular, we can now check that the session key cannot be
;;; compromised, subject to the assumptions we have imposed, using
;;; (deflistener k).

(defskeleton yahalom
  (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b name)
    (ch1 ch2 ch1-0 ch3 chan))
  (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (ch1 ch1)
    (ch2 ch2))
  (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (a a) (b b)
    (ch1 ch1-0) (ch2 ch2) (ch3 ch3))
  (deflistener k)
  (uniq-orig k n-b)
  (auth ch2 ch1-0)
  (conf ch2 ch3))

;;; Let's turn now to the initiator's point of view:

(defskeleton yahalom
  (vars (a b c name) (n-a text) (k skey) (ch3 chan))
  (defstrand init 3 (ch3 ch3) (n-a n-a))
  (uniq-orig n-a)
  (auth ch3))

;;; The initiator infers the presence of the server.  We can now add
;;; the assumptions that the server's channels -- ch1 and ch, here --
;;; have the same trust properties as before, ie ch1 is auth and ch is
;;; conf, in addition to the auth previously assumed:

(defskeleton yahalom
  (vars (k skey) (n-a n-b text) (a b name) (ch3 ch3-0 ch1 chan))
  (defstrand init 3 (k k) (n-a n-a) (n-b n-b) (a a) (b b) (ch3 ch3))
  (defstrand serv 2 (k k) (n-a n-a) (n-b n-b) (a a) (b b) (ch1 ch1)
    (ch3 ch3-0))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (uniq-orig k n-a)
  (auth ch3 ch1)
  (conf ch3-0))

;;; This now authenticates the presence of the responder for the first
;;; two nodes, and its agreement on all of the values present there.

;;; Finally, let us consider the server's point of view, with an
;;; authenticated channel for the request, and confidential channels
;;; over which to transmit the session key.

(defskeleton yahalom
  (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
  (defstrand serv 3 (ch1 ch1) (ch2 ch2) (ch3 ch3))
  (auth ch1)
  (conf ch2 ch3))

;;; This query confirms that the server has authenticated the first
;;; two nodes of the responder, but has not authenticated the
;;; initiator at all.

;;; However, the session key is safe:

(defskeleton yahalom
  (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
  (defstrand serv 3 (k k) (ch1 ch1) (ch2 ch2) (ch3 ch3))
  (deflistener k)
  (auth ch1)
  (conf ch2 ch3))
```

---

### `refrences/internet/examples_scm/commitment.scm`

*sha256:`505c140833d9` · 44 lines · 1.5 KB · lang:`scheme`*

```scheme
(herald commitment)

(defprotocol commit basic
  (defrole bidder
    (vars (a b name) (n data) (quote outcome text))
    (trace
     (send (enc "bid" (hash a b n quote) (privk "sig" a)))
     (recv (enc "receipt" (hash a b n quote) (privk "sig" b)))
     (send (cat n quote))
     (recv (enc "result" a b n quote outcome (privk "sig" b)))))

  (defrole bid-trash
    (vars (a b name) (n data) (outcome trash text))
    (trace
     (send (enc "bid" (hash n trash) (privk "sig" a)))
     (recv (enc "receipt" (hash n trash) (privk "sig" b)))))

  (defrole auctioneer
    (vars (a b name) (n data) (quote outcome text) (sealed mesg))
    (trace
     (recv (enc "bid" sealed (privk "sig" a)))
     (send (enc "receipt" sealed (privk "sig" b)))
     (recv (cat n quote))
     (cheq sealed (hash a b n quote))
     (send (enc "result" a b n quote outcome (privk "sig" b))))))

(defskeleton commit
  (vars (a b name) (n data) (quote outcome text) (sealed mesg))
  (defstrand auctioneer 4 (a a))	; full height:  cheq doesn't
					; count separately
  (non-orig (privk "sig" a)))

(defskeleton commit
  (vars (a b name) (n data) (quote outcome text) (sealed mesg))
  (defstrand auctioneer 2 (a a))	; up to last recv
  (non-orig (privk "sig" a)))

(defskeleton commit
  (vars (n data) (quote outcome text) (a b name))
  (defstrand auctioneer 4 (sealed (hash a b n quote)) (n n)
    (quote quote) (outcome outcome) (a a) (b b))
  (defstrand bidder 1 (n n) (quote quote) (a a) (b b))
  (uniq-gen n)
  (non-orig (privk "sig" a)))
```

---

### `refrences/internet/examples_scm/comp_test.scm`

*sha256:`6fb561c2b579` · 156 lines · 4.7 KB · lang:`scheme`*

```scheme
(herald "Main Example")

(defprotocol main-ex-src basic
  (defrole qn
    (vars (a b c akey) (i ssn text) (k skey))
    (trace
     (send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))
     (recv (enc "sorry" a b k)))
    (uniq-orig k))
  (defrole qy
    (vars (a b c akey) (i ssn d text) (k skey))
    (trace
     (send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))
     (recv (enc "data" d k)))
    (uniq-orig k))
  (defrole an
    (vars (a b c akey) (i text) (k skey) (x mesg))
    (trace
     (recv (cat i a (enc (enc k b c i (invk a)) b) x))
     (send (enc "sorry" a b k))))
  (defrole ay
    (vars (a b c akey) (i d text) (k skey) (x mesg))
    (trace
     (recv (cat i a (enc (enc k b c i (invk a)) b) x))
     (send (enc "data" d k)))
    (uniq-orig d)))

(defprotocol main-ex-tgt basic
  (defrole qn
    (vars (a b c akey) (i ssn text) (k skey))
    (trace
     (send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))
     (recv (enc "sorry" a b k)))
    (uniq-orig k))
  (defrole qy
    (vars (a b c akey) (i ssn d text) (k skey))
    (trace
     (send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))
     (recv (enc "data" d k)))
    (uniq-orig k))
  (defrole an
    (vars (a b c akey) (i y n text) (k skey) (x mesg))
    (trace
     (recv (cat i a (enc (enc k b c i (invk a)) b) x))
     (send (enc y n i a x c))
     (recv n)
     (send (enc "sorry" a b k)))
    (uniq-orig y n))
  (defrole ay
    (vars (a b c akey) (i y n d text) (k skey) (x mesg))
    (trace
     (recv (cat i a (enc (enc k b c i (invk a)) b) x))
     (send (enc y n i a x c))
     (recv y)
     (send (enc "data" d k)))
    (uniq-orig d y n))
  (defrole sn
    (vars (a b c akey) (i ssn y n text))
    (trace
     (recv (enc y n i a (enc a b i ssn c) c))
     (send n)))
  (defrole sy
    (vars (a b c akey) (i ssn y n text))
    (trace
     (recv (enc y n i a (enc a b i ssn c) c))
     (send y))))

(defprotocol main-ex-tgt-rule basic
  (defrole qn
    (vars (a b c akey) (i ssn text) (k skey))
    (trace
     (send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))
     (recv (enc "sorry" a b k)))
    (uniq-orig k))
  (defrole qy
    (vars (a b c akey) (i ssn d text) (k skey))
    (trace
     (send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))
     (recv (enc "data" d k)))
    (uniq-orig k))
  (defrole an
    (vars (a b c akey) (i y n text) (k skey) (x mesg))
    (trace
     (recv (cat i a (enc (enc k b c i (invk a)) b) x))
     (send (enc y n i a x c))
     (recv n)
     (send (enc "sorry" a b k)))
    (uniq-orig y n))
  (defrole ay
    (vars (a b c akey) (i y n d text) (k skey) (x mesg))
    (trace
     (recv (cat i a (enc (enc k b c i (invk a)) b) x))
     (send (enc y n i a x c))
     (recv y)
     (send (enc "data" d k)))
    (uniq-orig d y n))
  (defrole sn
    (vars (a b c akey) (i ssn y n text))
    (trace
     (recv (enc y n i a (enc a b i ssn c) c))
     (send n)))
  (defrole sy
    (vars (a b c akey) (i ssn y n text))
    (trace
     (recv (enc y n i a (enc a b i ssn c) c))
     (send y)))
  (defrule src
    (forall ((z strd) (i ssn text) (k skey) (a b c akey))
	    (implies
	     (and (p "qn" z 2) (p "qn" "i" z i) (p "qn" "ssn" z ssn)
		  (p "qn" "k" z k) (p "qn" "a" z a) (p "qn" "b" z b)
		  (p "qn" "c" z c) (non (invk a)) (non (invk b)) (non (invk c))
		  (uniq k))
	     (exists ((z-0 strd) (x mesg))
		     (and (p "an" z-0 4) (p "an" "x" z-0 x)
			  (p "an" "i" z-0 i) (p "an" "k" z-0 k)
			  (p "an" "a" z-0 a) (p "an" "b" z-0 b)
			  (p "an" "c" z-0 c) (prec z 0 z-0 0)
			  (prec z-0 3 z 1)))))))

(defskeleton main-ex-src
  (vars (a b c akey))
  (defstrand qn 2 (a a) (b b) (c c))
  (non-orig (invk a) (invk b) (invk c))
  (comment
   (defgoal main-ex-src
     (forall ((i ssn text) (k skey) (a b c akey) (z strd))
	     (implies
	      (and (p "qn" z 2) (p "qn" "i" z i) (p "qn" "ssn" z ssn)
		   (p "qn" "k" z k) (p "qn" "a" z a) (p "qn" "b" z b)
		   (p "qn" "c" z c) (non (invk a)) (non (invk b)) (non (invk c))
		   (uniq-at k z 0))
	      (exists ((x mesg) (z-0 strd))
		      (and (p "an" z-0 2) (p "an" "x" z-0 x) (p "an" "i" z-0 i)
			   (p "an" "k" z-0 k) (p "an" "a" z-0 a) (p "an" "b" z-0 b)
			   (p "an" "c" z-0 c) (prec z 0 z-0 0) (prec z-0 1 z 1))))))))

(defskeleton main-ex-src
  (vars (a b c akey))
  (defstrand qy 2 (a a) (b b) (c c))
  (non-orig (invk a) (invk b) (invk c)))

(defskeleton main-ex-tgt
  (vars (a b c akey))
  (defstrand qn 2 (a a) (b b) (c c))
  (non-orig (invk a) (invk b) (invk c)))

(defskeleton main-ex-tgt
  (vars (a b c akey))
  (defstrand qy 2 (a a) (b b) (c c))
  (non-orig (invk a) (invk b) (invk c)))

(defskeleton main-ex-tgt-rule
  (vars (a b c akey))
  (defstrand qn 2 (a a) (b b) (c c))
  (non-orig (invk a) (invk b) (invk c)))
```

---

### `refrences/internet/examples_scm/completeness-test.scm`

*sha256:`32ffa577d5f7` · 56 lines · 1.5 KB · lang:`scheme`*

```scheme
;; In this protocol an initiator verifies the liveness
;; of a responder via the first two messages of a
;; Needham-Schroeder exchange.  The initiator then
;; sends an ok message to a probe who is waiting
;; to hear if the responder is live.

(defprotocol completeness-test basic
 (defrole init
   (vars (a b name) (n text) (s skey))
   (trace
    (send (enc a n (pubk b)))
    (recv (enc n (pubk a)))
    (send (enc "ok" s))))
 (defrole resp
   (vars (a b name) (n text))
   (trace
    (recv (enc a n (pubk b)))
    (send (enc n (pubk a)))))
 (defrole probe
   (vars (s skey))
   (trace
    (recv (enc "ok" s)))))

;; These first two skeletons should be compared to
;; each other.  They only differ in the order in which
;; the strands are listed.  CPSA should find the same
;; shapes for both of them.  However, CPSA 1.5.3
;; only finds one shape for the first one.

(defskeleton completeness-test
  (vars (b name) (n text) (s skey))
  (defstrand init 3 (b b) (n n))
  (defstrand probe 1 (s s))
  (non-orig s (privk b))
  (uniq-orig n))

(defskeleton completeness-test
  (vars (b name) (n text) (s skey))
  (defstrand probe 1 (s s))
  (defstrand init 3 (b b) (n n))
  (non-orig s (privk b))
  (uniq-orig n))

(defskeleton completeness-test
  (vars (b name) (n text) (s skey))
  (defstrand init 2 (b b) (n n))
  (defstrand probe 1 (s s))
  (non-orig s (privk b))
  (uniq-orig n))

(defskeleton completeness-test
  (vars (b name) (n text) (s skey))
  (defstrand probe 1 (s s))
  (defstrand init 2 (b b) (n n))
  (non-orig s (privk b))
  (uniq-orig n))
```

---

### `refrences/internet/examples_scm/crushing.scm`

*sha256:`9c7657aaef79` · 35 lines · 0.8 KB · lang:`scheme`*

```scheme
;;; Attempt to make a protocol that reduces several strands by hulling at once

(defprotocol crushing basic
  (defrole init (vars (k akey) (n n1 n2 n3 text))
    (trace
	(send (enc n k))
      (recv (enc n n1 (invk k)))
      (recv (enc n n2 (invk k)))
      (recv (enc n n3 (invk k)))
      (send (enc n n1 n2 n3 (invk k)))
      (recv (enc n n1 n2 n3 n (invk k)))
    )
    (uniq-orig n)
    (non-orig (invk k))
  )
  (defrole adder (vars (k akey) (n new text))
    (trace
      (recv (enc n k))
      (send (enc n new (invk k)))
    )
    (uniq-orig new)
  )
  (defrole twister (vars (k akey) (n n1 n2 n3 text))
    (trace
       (recv (enc n n1 n2 n3 (invk k)))
       (send (enc n n2 n3 n1 n (invk k)))
    )
  )
)

(defskeleton crushing
  (vars (k akey) (n n1 n2 n3  text))
  (defstrand init 6 (k k) (n n) (n1 n1) (n2 n2) (n3 n3))
  (uniq-orig n1 n2 n3)
)
```

---

### `refrences/internet/examples_scm/dass_simple.scm`

*sha256:`48d05f30a4f4` · 57 lines · 2.1 KB · lang:`scheme`*

```scheme
(herald "Distributed Authentication Security Service Protocol Variants")

(defprotocol dass-simple basic
  (defrole init (vars (a b name) (k skey) (ta text) (kp akey) (tb text))
    (trace (send (cat (enc "init" ta k)
		      (enc a kp (privk a))
		      (enc (enc k (pubk b)) (invk kp))))
	   (recv (enc "resp" tb k))))
  (defrole resp (vars (a b name) (k skey) (ta text) (kp akey) (tb text))
    (trace (recv (cat (enc "init" ta k)
		      (enc a kp (privk a))
		      (enc (enc k (pubk b)) (invk kp))))
	   (send (enc "resp" tb k))))
  (comment "In this version of the protocol ")
  (comment "b might interact with a compromised initiator.")
  (comment "That is why a is not authenticated to b."))

(defprotocol dass+ basic
  (defrole init (vars (a b name) (k skey) (ta text) (kp akey) (tb text))
    (trace (send (cat (enc "init" ta k)
		      (enc a kp (privk a))
		      (enc (enc k (pubk b)) (invk kp))))
	   (recv (enc "resp" tb k))))
  (defrole resp (vars (a b name) (k skey) (ta text) (kp akey) (tb text))
    (trace (recv (cat (enc "init" ta k)
		      (enc a kp (privk a))
		      (enc (enc k (pubk b)) (invk kp))))
	   (send (enc "resp" tb k)))
    (non-orig (privk a)))
  (comment "In this version of the protocol ")
  (comment "b never interacts with a compromised initiator.")
  (comment "That is why a is properly authenticated to b."))

(defskeleton dass-simple
  (vars (a name) (b name) (k skey) (kp akey) (ta text)(tb text))
  (defstrand init 2 (a a) (b b) (k k) (kp kp) (ta ta) (tb tb))
  (non-orig (privk a) (privk b) (invk kp))
  (uniq-orig k kp))

(defskeleton dass+
  (vars (a name) (b name) (k skey) (kp akey) (ta text)(tb text))
  (defstrand init 2 (a a) (b b) (k k) (kp kp) (ta ta) (tb tb))
  (non-orig (privk a) (privk b) (invk kp))
  (uniq-orig k kp))

(comment
 (defskeleton dass
   (vars (a name) (b name) (ks name) (k skey) (kp akey))
   (defstrand init 4 (a a) (b b) (ks ks) (k k) (kp kp))
   (non-orig (privk a) (privk b) (privk ks))
   (uniq-orig k kp))

 (defskeleton dass
   (vars (a name) (b name) (ks name) (k skey) (kp akey))
   (defstrand resp 4 (a a) (b b) (ks ks) (k k) (kp kp))
   (non-orig (privk a) (privk b) (privk ks))
   (uniq-orig k kp)))
```

---

### `refrences/internet/examples_scm/denning-sacco.scm`

*sha256:`5550b730f87a` · 27 lines · 0.8 KB · lang:`scheme`*

```scheme
(herald "Denning-Sacco Protocol")

(defprotocol denning-sacco basic
  (defrole init (vars (a b ks name) (k skey) (ta text))
    (trace
     (send (cat a b))
     (recv (cat (enc b (pubk b) (privk ks))
		(enc a (pubk a) (privk ks))))
     (send (enc (enc a b k ta (privk a))
		(enc b (pubk b) (privk ks))
		(enc a (pubk a) (privk ks)) (pubk b)))))
  (defrole resp (vars (a b ks name) (k skey) (ta text))
    (trace
     (recv (enc (enc a b k ta (privk a))
		(enc b (pubk b) (privk ks))
		(enc a (pubk a) (privk ks)) (pubk b)))))
  (defrole keyserver (vars (a b ks name))
    (trace
     (recv (cat a b))
     (send (cat (enc b (pubk b) (privk ks))
		(enc a (pubk a) (privk ks)))))))

(defskeleton denning-sacco
  (vars (a b ks name) (k skey))
  (defstrand resp 1 (a a) (b b) (ks ks) (k k))
  (non-orig (privk b) (privk a) (privk ks))
  (uniq-orig k))
```

---

### `refrences/internet/examples_scm/deorig_contract.scm`

*sha256:`d2b82fe71e94` · 40 lines · 1.1 KB · lang:`scheme`*

```scheme
;;;  Deorig_contract:  Demonstrates a subtle incompleteness.
;;;
;;;  Attempts to show that deorigination may be necessary
;;; even during non-augmentation steps, such as in a contraction.
;;;  The idea is to make for a situation in which a value will
;;; be originated on a strand but later a contraction will force
;;; that value to be one that is restricted, where deorigination
;;; can solve the problem but CPSA will probably eliminate the
;;; contraction from the cohort.

(defprotocol deorig-contract basic
  (defrole init (vars (k akey) (x1 x2 text))
     (trace
       (send (enc x1 k))
       (send (enc x2 k))
       (recv (enc x1 x2 k))
     )
     (uniq-orig x1 x2)
     (non-orig (invk k))
   )
   (defrole resp (vars (k akey) (y1 y2 y3 text))
     (trace
       (recv (enc y1 k))
       (recv (enc y2 k))
       (send (enc y1 y3 k))
     )
   )
)

(defskeleton deorig-contract
   (vars)
   (defstrand init 3)
)

(defskeleton deorig-contract
   (vars (k akey) (x1 x2 text))
   (defstrand init 3 (k k) (x1 x1) (x2 x2))
   (defstrand resp 3 (k k) (y1 x1) (y2 x2) (y3 x2))
   (precedes ((0 0) (1 0)) ((0 1) (1 1)) ((1 2) (0 2)))
)
```

---

### `refrences/internet/examples_scm/deorig_mesg.scm`

*sha256:`9455450b46ca` · 19 lines · 0.5 KB · lang:`scheme`*

```scheme
(herald deorig-mesg)

(defprotocol deorig-mesg basic
  (defrole init
    (vars (k akey) (x text))
    (trace (send (enc x k)) (recv x))
    (uniq-orig x)
    (non-orig (invk k)))
  (defrole resp
    (vars (x mesg) (y text))
    (trace (recv x) (send y))))

(defskeleton deorig-mesg (vars) (defstrand init 2))

(defskeleton deorig-mesg
  (vars (k akey) (z text))
  (defstrand init 2 (k k) (x z))
  (defstrand resp 2 (x (enc z k)) (y z))
  (precedes ((0 0) (1 0)) ((1 1) (0 1))))
```

---

### `refrences/internet/examples_scm/deorig_simple.scm`

*sha256:`61d250e40a22` · 30 lines · 0.9 KB · lang:`scheme`*

```scheme
(herald deorig-simple)

;;;  Deorig_simple:     Demonstrates the same incompleteness as
;;;                     deorig_contract, but with fewer messages.
;;;
;;;  This simply sets up the archetypal nonce test for an init strand
;;;  but the resp role is only a partial match for the test.  In particular,
;;;  it sends a different value than it receives.  The obvious shape is one
;;;  in which the resp strand sends the same value it receives, but this
;;;  shape is not found.

(defprotocol deorig-simple basic
  (defrole init
    (vars (k akey) (x text))
    (trace (send (enc x k)) (recv x))
    (uniq-orig x)
    (non-orig (invk k)))
  (defrole resp
    (vars (k akey) (x y text))
    (trace (recv (enc x k)) (send y))))

(defskeleton deorig-simple
  (vars)
  (defstrand init 2))

(defskeleton deorig-simple
  (vars (k akey) (z text))
  (defstrand init 2 (k k) (x z))
  (defstrand resp 2 (k k) (x z) (y z))
  (precedes ((0 0) (1 0)) ((1 1) (0 1))))
```

---

### `refrences/internet/examples_scm/dh-ca_hack.scm`

*sha256:`f94fc6424084` · 66 lines · 2.0 KB · lang:`scheme`*

```scheme
(herald dhca (algebra basic) (bound 12))

(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))

(defprotocol dhca basic
  (defrole init (vars (gx h akey) (dhkey skey) (a b ca name) (n text))
    (trace
     (recv (enc gx a (privk ca)))
     (send (cat gx (enc gx a (privk ca))))
     (recv (cat h (enc h b (privk ca)) (enc n (CDH gx h dhkey))))
     (send (enc "check" n (CDH gx h dhkey))))
    (non-orig (privk ca) dhkey))
  (defrole resp (vars (gy h akey) (dhkey skey) (a b ca name) (n text))
    (trace
     (recv (enc gy b (privk ca)))
     (recv (cat h (enc h a (privk ca))))
     (send (cat gy (enc gy b (privk ca))
		(enc n (CDH h gy dhkey))))
     (recv (enc "check" n (CDH h gy dhkey))))
    (non-orig (privk ca) dhkey))
  (defrole ca (vars (subject ca name) (gz akey))
    (trace
     (send (enc gz subject (privk ca)) ))
    (non-orig (invk gz)))
  (defrole CDHcalc1 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gx (invk gy)))
    (send (CDH gx gy dhkey))
  ))
  (defrole CDHcalc2 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gy (invk gx)))
    (send (CDH gx gy dhkey))
  ))
;  (comment "A diffie-hellman exchange which uses a certificate
;    authority to certify long-term DH values.")
)

(defskeleton dhca
  (vars )
  (defstrand init 4 )
(comment "Full initiator point-of-view.  No need to make extra assumptions."))

(defskeleton dhca
  (vars (n text))
  (defstrand resp 4 (n n))
  (uniq-orig n)
  (comment "Full responder point of view with freshly chosen n")
)

(defskeleton dhca
  (vars (n text))
  (defstrand resp 4 (n n))
  (deflistener n)
  (uniq-orig n)
  (comment "Full responder point of view with freshly chosen n")
)

(defskeleton dhca
  (vars (a b ca name) (gx gy akey) (n text) (dhkey skey))
  (defstrand init 4 (gx gx) (h gy) (ca ca) (a a) (b b) (n n) (dhkey dhkey))
  (defstrand resp 4 (h gx) (gy gy) (ca ca) (a a) (b b) (n n) (dhkey dhkey))
(uniq-orig n)
;(comment "point of view in which init and resp each complete and
;    they agree on the relevant parameters.")
)
```

---

### `refrences/internet/examples_scm/dh_encrypt_hack.scm`

*sha256:`7cc99c4130f6` · 53 lines · 1.4 KB · lang:`scheme`*

```scheme
(herald dhencrypt (algebra basic))

(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))

(defprotocol dhencrypt basic
  (defrole init (vars (gx h akey) (dhkey skey) (n text))
    (trace
     (send gx)
     (recv (cat h (enc n (CDH gx h dhkey))))
     (send (enc "check" n (CDH gx h dhkey)))
    )
    (non-orig (invk gx) dhkey)
  )
  (defrole resp (vars (h gy akey) (dhkey skey) (n text))
    (trace
     (recv h)
     (send (cat gy (enc n (CDH h gy dhkey))))
     (recv (enc "check" n (CDH h gy dhkey)))
    )
    (non-orig (invk gy) dhkey)
    (uniq-orig gy n)
  )
  (defrole CDHcalc1 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gx (invk gy)))
    (send (CDH gx gy dhkey))
  ))
  (defrole CDHcalc2 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gy (invk gx)))
    (send (CDH gx gy dhkey))
  ))
  (comment "Diffie-hellman key exchange followed by an encrypted-nonce challenge/response")
)

(defskeleton dhencrypt
   (vars (gx h akey) (dhkey skey) (n text))
   (defstrand init 3 (gx gx) (h h) (dhkey dhkey) (n n))
   (comment "Initiator full point of view")
)

(defskeleton dhencrypt
   (vars (gy h akey) (dhkey skey) (n text))
   (defstrand resp 3 (gy gy) (h h) (dhkey dhkey) (n n))
   (comment "Responder full point of view")
)

(defskeleton dhencrypt
   (vars (gx gy akey) (n text))
   (defstrand init 2 (gx gx) (h gy) (n n))
   (defstrand resp 3 (h gx) (gy gy) (n n))
   (comment "Point of view where the natural result should be the only shape")
)
```

---

### `refrences/internet/examples_scm/dh_group_sig.scm`

*sha256:`27fb57e12cbf` · 70 lines · 1.6 KB · lang:`scheme`*

```scheme
(herald "Signed group DH exchange (improved version)"
	(algebra diffie-hellman)
	(limit 100))



(defprotocol dh_sig diffie-hellman
  (defrole group-init
    (vars (alpha rndx) (group text) (group-dist chan))
    (trace
     (send group-dist (cat "Group id" group
			   (exp (gen) alpha))))
    (uniq-gen alpha)
    (conf group-dist))
  
  (defrole init
    (vars (x rndx) (y expt) (alpha expt) (group na nb text)
	  (a b name) (group-dist chan))
    (trace
     (recv group-dist (cat "Group id" group
			   (exp (gen) alpha)))
     (send (enc (exp (exp (gen) alpha) x)
		(privk a)))
     (recv (enc a (exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk b)))
     (send (enc "final" b na
		(exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk a)))
     (recv (enc na nb
		(exp (exp (exp (gen) alpha) y)
		     x)))
     (send nb))
    (uniq-gen na x)
    (auth group-dist))

  (defrole resp
    (vars (y rndx) (x expt) (alpha expt) (group na nb text)
	  (a b name) (group-dist chan))
    (trace
     (recv group-dist (cat "Group id" group
			   (exp (gen) alpha)))
     (recv (enc (exp (exp (gen) alpha) x)
		(privk a)))
     (send (enc a (exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk b)))
     (recv (enc "final" b na
		(exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk a)))
     (send (enc na nb
		(exp (exp (exp (gen) alpha) x)
		     y)))
     (recv nb))
    (uniq-gen nb y)
    (auth group-dist)))

(defskeleton dh_sig
  (vars (a b name))
  (defstrand init 6 (a a) (b b))
  (non-orig (privk b) (privk a)))

(defskeleton dh_sig
  (vars (a b name))
  (defstrand resp 6 (a a) (b b))
  (non-orig (privk a) (privk b)))
```

---

### `refrences/internet/examples_scm/dh_group_sig_auth_failure.scm`

*sha256:`7aef504be50e` · 59 lines · 1.4 KB · lang:`scheme`*

```scheme
(herald "Signed group DH exchange (version with auth failure)"
	(algebra diffie-hellman)
	(limit 100))

(defprotocol dh_sig diffie-hellman
  (defrole group-init
    (vars (alpha rndx) (group text) (group-dist chan))
    (trace
     (send group-dist (cat "Group id" group
			   (exp (gen) alpha))))
    (uniq-gen alpha)
    (conf group-dist))
  
  (defrole init
    (vars (x rndx) (y expt) (alpha expt) (group text)
	  (a b name) (group-dist chan))
    (trace
     (recv group-dist (cat "Group id" group
			   (exp (gen) alpha)))
     (send (enc (exp (exp (gen) alpha) x)
		(privk a)))
     (recv (enc (exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk b)))
     (send (enc "final" (exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk a))))
    (uniq-gen x)
    (auth group-dist))

  (defrole resp
    (vars (y rndx) (x expt) (alpha expt) (group text)
	  (a b name) (group-dist chan))
    (trace
     (recv group-dist (cat "Group id" group
			   (exp (gen) alpha)))
     (recv (enc (exp (exp (gen) alpha) x)
		(privk a)))
     (send (enc (exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk b)))
     (recv (enc "final" (exp (exp (gen) alpha) y)
		(exp (exp (gen) alpha) x)
		(privk a))))
    (uniq-gen y)
    (auth group-dist)))

(defskeleton dh_sig
  (vars (a b name))
  (defstrand init 4 (a a) (b b))
  (non-orig (privk b) (privk a))
)

(defskeleton dh_sig
  (vars (a b name))
  (defstrand resp 4 (a a) (b b))
  (non-orig (privk a) (privk b))
)
```

---

### `refrences/internet/examples_scm/dh_mim_hack.scm`

*sha256:`40710e381d87` · 31 lines · 1.0 KB · lang:`scheme`*

```scheme
(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))

(defprotocol dh_mim basic
  (defrole init
    (vars (gx gy akey) (n text) (dhkey skey))
    (trace (send gx) (recv gy) (send (enc n (CDH gx gy dhkey))))
    (uniq-orig n gx)
    (non-orig (invk gx) dhkey))
  (defrole resp
    (vars (gx gy akey) (n text) (dhkey skey))
    (trace (recv gx) (send gy) (recv (enc n (CDH gx gy dhkey))))
    (uniq-orig gy)
    (non-orig (invk gy) dhkey))
  (defrole CDHcalc1 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gx (invk gy)))
    (send (CDH gx gy dhkey))
  ))
  (defrole CDHcalc2 (vars (gx gy akey) (dhkey skey))
   (trace
    (recv (cat gy (invk gx)))
    (send (CDH gx gy dhkey))
  ))
  (comment "Diffie-hellman key exchange followed by an encryption"))

(defskeleton dh_mim
  (vars (n text) (gx gy akey) (dhkey skey))
  (defstrand init 3 (n n) (gx gx) (dhkey dhkey))
  (defstrand resp 3 (n n) (gy gy) (dhkey dhkey))
  (precedes ((0 2) (1 2)))
  (comment "Agreement on the encrypted text only"))
```

---

### `refrences/internet/examples_scm/dhnsl_hack.scm`

*sha256:`1988a950f6f8` · 44 lines · 1.3 KB · lang:`scheme`*

```scheme
(herald "Diffie-Hellman enhanced Needham-Schroeder-Lowe Protocol"
  (algebra basic))

(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))

(defprotocol dhnsl basic
  (defrole init
    (vars (a b name) (h2 h3 gx akey) (dhkey skey))
    (trace
     (send (enc gx a (pubk b)))
     (recv (enc h2 (CDH h2 gx dhkey) h3 b (pubk a)))
     (send (enc (CDH h3 gx dhkey) (pubk b)))
    )
    (uniq-orig gx)
    (non-orig (invk gx) dhkey)
    (comment "X should be assumed to be freshly chosen per role")
  )
  (defrole resp
    (vars (b a name) (h1 gy gz akey) (dhkey skey))
    (trace
     (recv (enc h1 a (pubk b)))
     (send (enc gy (CDH gy h1 dhkey) gz b (pubk a)))
     (recv (enc (CDH gz h1 dhkey) (pubk b)))
    )
    (uniq-orig gy gz)
    (non-orig (invk gy) (invk gz) dhkey)
    (comment "Y and Z should be assumed to be freshly chosen per role")
  )
  (comment "Needham-Schroeder-Lowe DH challenge/responses in place of nonces")
)

;;; The initiator point-of-view
(defskeleton dhnsl
  (vars (a b name) (gx gy gz akey))
  (defstrand init 3 (a a) (b b) (h2 gy) (h3 gz) (gx gx))
  (non-orig (privk b) (privk a))
  (comment "Initiator point-of-view"))

;;; The responder point-of-view
(defskeleton dhnsl
  (vars (a b name) (gx gy gz akey))
  (defstrand resp 3 (a a) (b b) (h1 gx) (gy gy) (gz gz))
  (non-orig (privk a))
  (comment "Responder point-of-view"))
```

---

### `refrences/internet/examples_scm/dhstatic-state.scm`

*sha256:`a49573f51e24` · 67 lines · 2.0 KB · lang:`scheme`*

```scheme
(herald dhstatic-state
	(algebra diffie-hellman)
	(bound 16))

(defprotocol dhstatic-state diffie-hellman
  (defrole cert
    (vars (subj ca name) (serial data) (galpha mesg))
    (trace
     (recv (sig (cert-req subj galpha ca) (privk "sig" subj)))
     (send (sig (cert subj galpha ca serial)
		(privk "sig" ca))))
    (uniq-orig serial)
    (comment "Certificate Authority"))

  (defrole get-cert
    (vars (self ca name) (serial data) (ra rndx)
	  (static-key locn) (ignore mesg))
    (trace
     (send (sig (cert-req self (exp (gen) ra) ca) (privk "sig" self)))
     (recv (sig (cert self (exp (gen) ra) ca serial)
		(privk "sig" ca)))
     (load static-key ignore)
     (stor static-key (cat "privkey" self ra serial ca)))

    (uniq-gen ra)
    (comment "Get certified"))

  (defrole init
    (vars (a b ca name) (ra rndx) (serial-a serial-b data)
	  (alpha expt) (n text) (static-key locn))
    (trace
     (load static-key (cat "privkey" a ra serial-a ca))
     (recv (sig (cert b (exp (gen) alpha) ca serial-b)
		(privk "sig" ca)))
     (send (enc n a b serial-a serial-b (exp (exp (gen) alpha) ra)))
     (recv n))
    (uniq-orig n)
    (gen-st (cat "privkey" a ra serial-a ca))
    (facts (neq a b))
    (comment "Initiator is A"))

  (defrole resp
    (vars (a b ca name) (rb rndx) (serial-b serial-a data)
	  (alpha expt) (n text) (static-key locn))
    (trace
     (load static-key (cat "privkey" b rb serial-b ca))
     (recv (sig (cert a (exp (gen) alpha) ca serial-a)
		(privk "sig" ca)))
     (recv (enc n a b serial-a serial-b (exp (exp (gen) alpha) rb)))
     (send n))
    (facts (neq a b))
    (gen-st (cat "privkey" b rb serial-b ca))
    (comment "Responder is B"))

  (lang (cert-req (tupl 3))
	(cert (tupl 4))
	(sig sign)))

(defskeleton dhstatic-state
  (vars (ca b name))
  (defstrand init 4 (ca ca) (b b))
  (non-orig (privk "sig" ca) (privk "sig" b)))

(defskeleton dhstatic-state
  (vars (ca a name))
  (defstrand resp 4 (ca ca) (a a))
  (non-orig (privk "sig" ca) (privk "sig" a)))
```

---

### `refrences/internet/examples_scm/disclosure.scm`

*sha256:`03f8b49cc6eb` · 33 lines · 1.0 KB · lang:`scheme`*

```scheme
;;; Here's a protocol where there are two ways for the init strand to
;;; be satisfied.  The responder can use the key to extract that
;;; nonce.  Or else the adversary can get the key from the init's last
;;; send, and use that in *the next* session to extract the nonce
;;; without the responder's help.

;;; This is a simplest example in which CPSA needs to introduce a
;;; listener to explore the possibility that the adversary can do the
;;; decryption.  It certainly illustrates that the generalization
;;; steps that discard listeners are a natural part of finding the
;;; minimal shapes.

(herald disclosure)

(defprotocol disc basic
  (defrole init
    (vars (a b name) (k skey) (n text))
    (trace
     (send (enc a b n k))
     (recv n)
     (send k))
    (pen-non-orig k))

  (defrole resp
    (vars (a b name) (k skey) (n text))
    (trace
     (recv (enc a b n k))
     (send n))))

(defskeleton disc
  (vars (n text))
  (defstrand init 2 (n n))
  (uniq-orig n))
```

---

### `refrences/internet/examples_scm/doorsep.scm`

*sha256:`b727325455f4` · 33 lines · 0.8 KB · lang:`scheme`*

```scheme
(herald doorsep (comment "Door Simple Example Protocol"))

(defprotocol doorsep basic
  (defrole person
    (vars (d p akey) (k skey) (t text))
    (trace
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t))
    (uniq-orig k))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t))
    (uniq-orig t))
  (defrule trust
    (forall ((z strd) (p d akey))
	    (implies
	     (and (p "person" z 1)
		  (p "person" "p" z p)
		  (p "person" "d" z d)
		  (non (invk p)))
	     (non (invk d))))
    (comment "The trust rule"))
  (comment "Doorsep protocol using unnamed asymmetric keys"))

(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (comment "Analyze from the doors's perspective"))
```

---

### `refrences/internet/examples_scm/doorsep2invk.scm`

*sha256:`7fe92d6d7c55` · 27 lines · 1.0 KB · lang:`scheme`*

```scheme
(herald doorsep2invk (comment "Door Simple Example Protocol"))

(defprotocol doorsep basic
  (defrole init
    (vars (self peer akey) (skey skey) (data text))
    (trace (send (enc (enc skey (invk self)) peer))
      (recv (enc data skey)) (send data))
    (uniq-orig skey))
  (defrole resp
    (vars (self peer akey) (skey skey) (data text))
    (trace (recv (enc (enc skey (invk peer)) self))
      (send (enc data skey)) (recv data))
    (uniq-orig data))
  (comment "Doorsep's protocol using unnamed asymmetric keys"))

(defgoal doorsep
  (forall
    ((text+0 text) (skey+0 skey) (akey+1 akey+0 akey+3 akey)
     (z z-0 strd))
    (implies
      (and (p "resp" z 3) (p "init" z-0 1) (p "resp" "data" z text+0)
        (p "resp" "skey" z skey+0) (p "resp" "self" z akey+1)
        (p "resp" "peer" z (invk akey+3)) (p "init" "skey" z-0 skey+0)
        (p "init" "self" z-0 (invk akey+3)) (p "init" "peer" z-0 akey+0)
        (prec z-0 0 z 0) (non akey+3) (non (invk akey+0))
        (uniq-at skey+0 z-0 0) (uniq-at text+0 z 1))
      (and))))
```

---

### `refrences/internet/examples_scm/encsig.scm`

*sha256:`480f80c2eea1` · 44 lines · 1.5 KB · lang:`scheme`*

```scheme
(herald "Encrypted Signed Message Example"
   (comment "Shows examples of key usage of asymmetric keys"))

(defprotocol mult-keys-enc-sig basic
   (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc (enc n1 a (pubk "enc" b)) (privk "sig" a)))
     (recv (enc (enc n1 n2 (pubk "enc" a)) (privk "sig" b)))
     (send (enc (enc n2 (pubk "enc" b)) (privk "sig" a)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc (enc n1 a (pubk "enc" b)) (privk "sig" a)))
     (send (enc (enc n1 n2 (pubk "enc" a)) (privk "sig" b)))
     (recv (enc (enc n2 (pubk "enc" b)) (privk "sig" a))))))

;;; The initiator point-of-view
(defskeleton mult-keys-enc-sig
   (vars (a b name) (n1 text))
   (defstrand init 3 (a a) (b b) (n1 n1))
   (non-orig (privk "enc" a) (privk "sig" a) (privk "sig" b))
   (uniq-orig n1))

;;; The responder point-of-view trusting only a's signature key
(defskeleton mult-keys-enc-sig
  (vars (a b name) (n2 text))
  (defstrand resp 3 (a a) (b b) (n2 n2))
  (non-orig (privk "sig" a))
  (uniq-orig n2))

;;; The responder point-of-view trusting only a's encryption key
(defskeleton mult-keys-enc-sig
  (vars (a b name) (n2 text))
  (defstrand resp 3 (a a) (b b) (n2 n2))
  (non-orig (privk "enc" a))
  (uniq-orig n2))

;;; The responder point-of-view trusting both of a's keys
(defskeleton mult-keys-enc-sig
  (vars (a b name) (n2 text))
  (defstrand resp 3 (a a) (b b) (n2 n2))
  (non-orig (privk "sig" a) (privk "enc" a))
  (uniq-orig n2))
```

---

### `refrences/internet/examples_scm/envelope.scm`

*sha256:`0c2f85eb6f6b` · 204 lines · 6.6 KB · lang:`scheme`*

```scheme
(herald "Envelope Protocol" (bound 15))

;;; This file analyzes the Envelope Protocol using three rules sets.
;;; For each rule set, it checks three scenarios.  In every scenario,
;;; an Alice strand runs to completion.  In the first scenario, the
;;; obtain token is listened for.  In the second, a listener for the
;;; refusal token is included.  In the third scenario, both listeners
;;; are included.  The third scenario should be impossible, but rules
;;; are required to accurately model state.
;;;
;;; The first rule set is empty and the answer to the third scenario
;;; shows a case is which the TPM's PCR state splits.  The second rule
;;; set forces TPM extends to be linearly ordered.  However, in this
;;; case, there are two TPMs when there should be one as Alice uses
;;; one TPM storage key to communicate with both TPMs.  The final rule
;;; set includes a rule about storage keys and thus accurately models
;;; state.
;;;
;;; Macros are used to avoid copying roles and scenarios.

;; This is the refusal token
(defmacro (refuse n v k aik)
  (enc "quote" (hash (hash "0" n) "refuse") (enc v k) aik))

;;; This protocol tracks the TPM's PCR state
;;; by sending a message with the current PCR
;;; value encrypted by a hashed secret key.
;;; The hash is used to prevent a confusion with
;;; the key for an encrypted session.

(defmacro (roles)
  (^
   ;; Power on sets the pcr to 0
   (defrole tpm-power-on
     (vars (pcrkey skey))
     (trace
      (recv "power on")
      (send (enc "0" (hash pcrkey))))
     (non-orig pcrkey))

   ;; The extend command takes the value to
   ;; extend and the current PCR value (in the
   ;; form of a message encrypted with the special
   ;; PCR state key) and produces the hash of the
   ;; two values (by sending it encrypted in the
   ;; special PCR state key).
   (defrole tpm-extend
     (vars (value current-value mesg) (pcrkey skey))
     (trace
      (recv (cat "extend" value))
      (recv (enc current-value (hash pcrkey))) ;; MSR lhs (deleted)
      (send (enc (hash current-value value) (hash pcrkey))) ;; MSR rhs
      (send "ext ok"))
     (non-orig pcrkey))

   ;; The extend command can also occur within an
   ;; encrypted session.  We assume some session key already exists
   (defrole tpm-extend-enc
     (vars (value current-value mesg) (pcrkey esk skey))
     (trace
      (recv (enc "extend" value esk))
      (recv (enc current-value (hash pcrkey))) ;; MSR lhs (deleted)
      (send (enc (hash current-value value) (hash pcrkey))) ;; MSR rhs
      (send "ext ok"))
     (non-orig pcrkey esk))

   ;; The TPM must retrieve the current pcr value.  Notice that
   ;; the nonce is of sort mesg, which allows non-atomic values.
   (defrole tpm-quote
     (vars (nonce current-value mesg) (pcrkey skey) (aik akey))
     (trace
      (recv (cat "quote" nonce))
      (recv (enc current-value (hash pcrkey))) ;; MSR lhs (not deleted)
      (send (enc "quote" current-value nonce aik)))
     (non-orig aik pcrkey))

   ;; This role creates a key whose use is restricted to a
   ;; requested pcr value (since we only model one pcr).
   ;; It doesn't create or change any TPM state.
   (defrole tpm-create-key
     (vars (k aik akey) (pcrval mesg) (esk skey))
     (trace
      (recv (enc "create key" pcrval esk)) ;; encryption prevents weird shapes
      (send (enc "created" k pcrval aik)));; no tpm state is set
     (uniq-orig k)
     (non-orig (invk k) aik esk))

   ;; This role receives an encryption and a previously
   ;; made key structure that restricts the decryption key
   ;; to be used with a certain pcr value.  It retrieves the
   ;; current value and checks that it matches before decrypting.
   (defrole tpm-decrypt
     (vars (m pcrvals mesg) (k aik akey) (pcrkey skey))
     (trace
      (recv (cat "decrypt" (enc m k)))
      (recv (enc "created" k pcrvals aik))
      (recv (enc pcrvals (hash pcrkey))) ;; MSR lhs (not deleted)
      (send m))
     (non-orig aik pcrkey))

   ;; Alice extends a pcr with a fresh nonce in an encrypted
   ;; session.  She has the TPM create a new key whose use is
   ;; bound to the hash of pcr value she just created with the
   ;; string "obtain".  She then encrypts her fresh secret with
   ;; this newly created key.
   (defrole alice
     (vars (n v data) (esk skey) (k aik akey))
     (trace
      (send (enc "extend" n esk))
      (send (enc "create key" (hash (hash "0" n) "obtain") esk))
      (recv (enc "created" k (hash (hash "0" n) "obtain") aik))
      (send (enc v k)))
     (uniq-orig n v)
     (non-orig aik esk))))

(defprotocol envelope basic
  (roles))

(defskeleton envelope
  (vars (v data))
  (deflistener v)
  (defstrand alice 4 (v v)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (deflistener v)
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defprotocol envelope basic
  (roles)

  (defrule ordered-extends
    (forall ((y z strd) (pcrkey skey))
	    (implies
	     (and (p "tpm-extend" y 3)
		  (p "tpm-extend" z 3)
		  (p "tpm-extend" "pcrkey" y pcrkey)
		  (p "tpm-extend" "pcrkey" z pcrkey))
	     (or (= y z)
		 (prec y 2 z 3)
		 (prec z 2 y 3))))))

(defskeleton envelope
  (vars (v data))
  (deflistener v)
  (defstrand alice 4 (v v)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (deflistener v)
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defprotocol envelope basic
  (roles)

  (defrule ordered-extends
    (forall ((y z strd) (pcrkey skey))
	    (implies
	     (and (p "tpm-extend" y 3)
		  (p "tpm-extend" z 3)
		  (p "tpm-extend" "pcrkey" y pcrkey)
		  (p "tpm-extend" "pcrkey" z pcrkey))
	     (or (= y z)
		 (prec y 2 z 3)
		 (prec z 2 y 3)))))

  (defrule esk-same-as-pcrkey
    (forall ((y z strd) (esk pcrkey pcrkey-0 skey))
	    (implies
	     (and (p "tpm-extend-enc" y 3)
		  (p "tpm-extend-enc" z 3)
		  (p "tpm-extend-enc" "esk" y esk)
		  (p "tpm-extend-enc" "esk" z esk)
		  (p "tpm-extend-enc" "pcrkey" y pcrkey)
		  (p "tpm-extend-enc" "pcrkey" z pcrkey-0))
	     (= pcrkey pcrkey-0)))))

(defskeleton envelope
  (vars (v data))
  (deflistener v)
  (defstrand alice 4 (v v)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey))
  (deflistener (refuse n v k aik))
  (deflistener v)
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))
```

---

### `refrences/internet/examples_scm/epmo-hash.scm`

*sha256:`57d5e38dc720` · 77 lines · 2.7 KB · lang:`scheme`*

```scheme
(herald "Electronic Purchase with Money Order Protocol with Key Hashing"
  (comment "Annotated with trust management formulas"))

(defprotocol epmo basic
  (defrole bank
    (vars (b c m name) (nc nm nb data) (price text))
    (trace
     (recv (enc c nc nm price (pubk b)))
     (send (cat (enc (hash c nc nb nm price) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (hash b nb nm) (privk m))))
    (uniq-orig nb)
    (annotations b
      (1
        (implies
          (and (forall ((pm name)) (says c (transfer b price pm nm)))
            (forall ((pm name)) (says pm (transfer b price pm nm))))
          (forall ((pm name)) (transfer b price pm nm))))
      (2
        (and (says c (transfer b price m nm))
          (says m (transfer b price m nm))))))
  (defrole customer
    (vars (b c m name) (nb nc nm data) (goods price text))
    (trace
     (send (enc c nc goods price (pubk m)))
     (recv (enc nc nm m goods price (pubk c)))
     (send (enc c nc nm price (pubk b)))
     (recv (cat (enc (hash c nc nb nm price) (privk b))
		(enc nc nb (pubk c))))
     (send (cat (enc (hash c nc nb nm price) (privk b)) nb)))
    (uniq-orig nc)
    (annotations c
      (1
        (says m
          (forall ((pb name))
            (implies (transfer pb price m nm) (ship m goods c)))))
      (3
        (says b
          (implies
            (and (forall ((pm name)) (says c (transfer b price pm nm)))
              (forall ((pm name)) (says m (transfer b price pm nm))))
            (transfer b price m nm))))
      (4 (transfer b price m nm))))
  (defrole merchant
    (vars (b c m name) (nb nc nm data) (goods price text))
    (trace
     (recv (enc c nc goods price (pubk m)))
     (send (enc nc nm m goods price (pubk c)))
     (recv (cat (enc (hash c nc nb nm price) (privk b)) nb))
     (send (enc (hash b nb nm) (privk m))))
    (uniq-orig nm)
    (annotations m
      (1
        (forall ((pb name))
          (implies (transfer pb price m nm) (ship m goods c))))
      (2
        (and
          (says b
            (implies
              (and
                (forall ((pm name)) (says c (transfer b price pm nm)))
                (forall ((pm name)) (says m (transfer b price pm nm))))
              (transfer b price m nm)))
          (says c (transfer b price m nm))))
      (3 (and (transfer b price m nm) (ship m goods c))))))

(defskeleton epmo (vars (b c m name))
  (defstrand customer 5 (b b) (c c) (m m))
  (non-orig (privk b) (privk c) (privk m)))

(defskeleton epmo (vars (b c m name) (goods name))
  (defstrand bank 3 (b b) (c c) (m m))
  (non-orig (privk b) (privk c) (privk m)))

(defskeleton epmo (vars (b c m name))
  (defstrand merchant 4 (b b) (c c) (m m))
  (non-orig (privk b) (privk c) (privk m)))
```

---

### `refrences/internet/examples_scm/epmo-key-hash.scm`

*sha256:`f779124fc6fe` · 77 lines · 2.7 KB · lang:`scheme`*

```scheme
(herald "Electronic Purchase with Money Order Protocol with Key Hashing"
  (comment "Annotated with trust management formulas"))

(defprotocol epmo basic
  (defrole bank
    (vars (b c m name) (nc nm nb data) (price text))
    (trace
     (recv (enc c nc nm price (pubk b)))
     (send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (enc "hash" (cat b nb nm)) (privk m))))
    (uniq-orig nb)
    (annotations b
      (1
        (implies
          (and (forall ((pm name)) (says c (transfer b price pm nm)))
            (forall ((pm name)) (says pm (transfer b price pm nm))))
          (forall ((pm name)) (transfer b price pm nm))))
      (2
        (and (says c (transfer b price m nm))
          (says m (transfer b price m nm))))))
  (defrole customer
    (vars (b c m name) (nb nc nm data) (goods price text))
    (trace
     (send (enc c nc goods price (pubk m)))
     (recv (enc nc nm m goods price (pubk c)))
     (send (enc c nc nm price (pubk b)))
     (recv (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b))
		(enc nc nb (pubk c))))
     (send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) nb)))
    (uniq-orig nc)
    (annotations c
      (1
        (says m
          (forall ((pb name))
            (implies (transfer pb price m nm) (ship m goods c)))))
      (3
        (says b
          (implies
            (and (forall ((pm name)) (says c (transfer b price pm nm)))
              (forall ((pm name)) (says m (transfer b price pm nm))))
            (transfer b price m nm))))
      (4 (transfer b price m nm))))
  (defrole merchant
    (vars (b c m name) (nb nc nm data) (goods price text))
    (trace
     (recv (enc c nc goods price (pubk m)))
     (send (enc nc nm m goods price (pubk c)))
     (recv (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) nb))
     (send (enc (enc "hash" (cat b nb nm)) (privk m))))
    (uniq-orig nm)
    (annotations m
      (1
        (forall ((pb name))
          (implies (transfer pb price m nm) (ship m goods c))))
      (2
        (and
          (says b
            (implies
              (and
                (forall ((pm name)) (says c (transfer b price pm nm)))
                (forall ((pm name)) (says m (transfer b price pm nm))))
              (transfer b price m nm)))
          (says c (transfer b price m nm))))
      (3 (and (transfer b price m nm) (ship m goods c))))))

(defskeleton epmo (vars (b c m name))
  (defstrand customer 5 (b b) (c c) (m m))
  (non-orig (privk b) (privk c) (privk m)))

(defskeleton epmo (vars (b c m name) (goods name))
  (defstrand bank 3 (b b) (c c) (m m))
  (non-orig (privk b) (privk c) (privk m)))

(defskeleton epmo (vars (b c m name))
  (defstrand merchant 4 (b b) (c c) (m m))
  (non-orig (privk b) (privk c) (privk m)))
```

---

### `refrences/internet/examples_scm/epmo.scm`

*sha256:`619a6b134674` · 80 lines · 2.8 KB · lang:`scheme`*

```scheme
(herald "Electronic Purchase with Money Order Protocol"
  (comment "Annotated with trust management formulas"))

(defprotocol epmo basic
  (defrole bank
    (vars (b c m name) (hash akey) (nc nm nb data) (price text))
    (trace
     (recv (enc c nc nm price (pubk b)))
     (send (cat (enc (enc c nc nb nm price hash) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (enc b nb nm hash) (privk m))))
    (non-orig (invk hash))
    (uniq-orig nb)
    (annotations b
      (1
        (implies
          (and (forall ((pm name)) (says c (transfer b price pm nm)))
            (forall ((pm name)) (says pm (transfer b price pm nm))))
          (forall ((pm name)) (transfer b price pm nm))))
      (2
        (and (says c (transfer b price m nm))
          (says m (transfer b price m nm))))))
  (defrole customer
    (vars (b c m name) (hash akey) (nb nc nm data) (goods price text))
    (trace
     (send (enc c nc goods price (pubk m)))
     (recv (enc nc nm m goods price (pubk c)))
     (send (enc c nc nm price (pubk b)))
     (recv (cat (enc (enc c nc nb nm price hash) (privk b))
		(enc nc nb (pubk c))))
     (send (cat (enc (enc c nc nb nm price hash) (privk b)) nb)))
    (non-orig (invk hash))
    (uniq-orig nc)
    (annotations c
      (1
        (says m
          (forall ((pb name))
            (implies (transfer pb price m nm) (ship m goods c)))))
      (3
        (says b
          (implies
            (and (forall ((pm name)) (says c (transfer b price pm nm)))
              (forall ((pm name)) (says m (transfer b price pm nm))))
            (transfer b price m nm))))
      (4 (transfer b price m nm))))
  (defrole merchant
    (vars (b c m name) (hash akey) (nb nc nm data) (goods price text))
    (trace
     (recv (enc c nc goods price (pubk m)))
     (send (enc nc nm m goods price (pubk c)))
     (recv (cat (enc (enc c nc nb nm price hash) (privk b)) nb))
     (send (enc (enc b nb nm hash) (privk m))))
    (non-orig (invk hash))
    (uniq-orig nm)
    (annotations m
      (1
        (forall ((pb name))
          (implies (transfer pb price m nm) (ship m goods c))))
      (2
        (and
          (says b
            (implies
              (and
                (forall ((pm name)) (says c (transfer b price pm nm)))
                (forall ((pm name)) (says m (transfer b price pm nm))))
              (transfer b price m nm)))
          (says c (transfer b price m nm))))
      (3 (and (transfer b price m nm) (ship m goods c))))))

(defskeleton epmo (vars (b c m name))
  (defstrand customer 5 (b b) (c c) (m m))
  (non-orig (privk b) (privk c) (privk m)))

(defskeleton epmo (vars (b c m name) (goods name))
  (defstrand bank 3 (b b) (c c) (m m))
  (non-orig (privk b) (privk c) (privk m)))

(defskeleton epmo (vars (b c m name))
  (defstrand merchant 4 (b b) (c c) (m m))
  (non-orig (privk b) (privk c) (privk m)))
```

---

### `refrences/internet/examples_scm/epmo_acctnum-key-hash.scm`

*sha256:`9590f59d5844` · 100 lines · 3.8 KB · lang:`scheme`*

```scheme
(herald "Electronic Purchase with Money Order Protocol Variant with Key Hashing"
  (comment "This version includes account numbers in exchanges"))

;; The results of running CPSA on this input produces interesting
;; output.  One of the shapes is produced only as a result of
;; generalization, not cohort reduction.  It is a counterexample to
;; the hypthesis that all shapes are produced by cohort reduction, and
;; the purpose of generalization is to distinguish the shapes from the
;; other realized skeletons produced by cohort reduction.

;; The shape in question identifies the bank's nonce with price of the
;; goods.  The variable cannot be separated because the uniquely
;; originating variable originates on the merchant strand, but after
;; separation, it would originate on the bank's strand.

;; Adding a role unique origination assumption to the bank role for
;; its nonce eliminates the undesired shape.

(defprotocol epmo_acctnum basic
  (defrole bank
    (vars (b c m name) (acctnum text) (nc nm nb price text))
    (trace
     (recv (enc c nc nm acctnum price (pubk b)))
     (send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (enc "hash" (cat b m nb nm)) (privk m))))
    (annotations b
      (1
        (forall ((pm name))
          (implies
            (and (authtransfer c acctnum b price pm nm)
              (reqtransfer pm b price pm nm))
            (dotransfer acctnum b price pm nm))))
      (2
        (and (says c (authtransfer c acctnum b price m nm))
          (says m (reqtransfer m b price m nm))))))
  (defrole customer
    (vars (b c m name) (acctnum nb nc nm goods price text))
    (trace
     (send (enc c nc goods (pubk m)))
     (recv (enc nc nm m price (pubk c)))
     (send (enc c nc nm acctnum price (pubk b)))
     (recv (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b))
		(enc nc nb (pubk c))))
     (send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b))
		nb)))
    (non-orig (privk b))
    (uniq-orig nc)
    (annotations c
      (1
        (says m
          (implies
            (exists ((acctnum2 text))
              (dotransfer acctnum2 b price m nm)) (doship m goods c))))
      (3
        (says b
          (forall ((pm name))
            (implies
              (and (authtransfer c acctnum b price m nm)
                (reqtransfer pm b price pm nm))
              (dotransfer acctnum b price pm nm)))))
      (4 (authtransfer c acctnum b price m nm))))
  (defrole merchant (vars (b c m name) (nb nc nm goods price text))
    (trace
     (recv (enc c nc goods (pubk m)))
     (send (enc nc nm m price (pubk c)))
     (recv (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b))
		nb))
     (send (enc (enc "hash" (cat b m nb nm)) (privk m))))
    (uniq-orig nm)
    (annotations m
      (1
        (implies
          (exists ((acctnum2 text)) (dotransfer acctnum2 b price m nm))
          (doship m goods c)))
      (2
        (and
          (says b
            (forall ((pm name))
              (exists ((acctnum2 text))
                (implies
                  (and (authtransfer c acctnum2 b price m nm)
                    (reqtransfer pm b price pm nm))
                  (dotransfer acctnum2 b price pm nm)))))
          (says c
            (exists ((acctnum2 text))
              (authtransfer c acctnum2 b price m nm)))))
      (3 (and (reqtransfer m b price m nm) (doship m goods c))))))

(defskeleton epmo_acctnum
  (vars (b m c name) (nm nc nb text))
  (defstrand merchant 4 (b b) (m m) (c c) (nm nm) (nc nc) (nb nb))
  (non-orig (privk b) (privk m) (privk c))
  (uniq-orig nm nc nb))

(defskeleton epmo_acctnum
  (vars (b m c name) (nm nb nc text) (price acctnum text))
  (defstrand bank 3 (b b) (m m) (c c) (nm nm) (nb nb) (nc nc))
  (non-orig (privk b) (privk m) (privk c))
  (uniq-orig nm nc nb))
```

---

### `refrences/internet/examples_scm/expand.scm`

*sha256:`80a54a16b03e` · 18 lines · 0.3 KB · lang:`scheme`*

```scheme
(herald expand (expand) (comment "test macro expansion"))

(defmacro (altenc t k)
  (enc t k))

(defmacro (altcat a b)
  (^ a b))

(defprotocol expand basic
  (defrole init
    (vars (t text) (k skey))
    (trace
     (send (altenc t k))
     (recv (cat (altcat t k))))))

(defskeleton expand
  (vars)
  (defstrand init 2))
```

---

### `refrences/internet/examples_scm/facts.scm`

*sha256:`e6a2686168e7` · 95 lines · 2.4 KB · lang:`scheme`*

```scheme
(herald facts)

;;; Testing facts

(defprotocol unilateral basic
  (defrole init
     (vars (n text) (k akey))
     (trace
      (send (enc n k))
      (recv n))
     (uniq-orig n))
  (defrole resp
     (vars (n text) (k akey))
     (trace
      (recv (enc n k))
      (send n))))

(defskeleton unilateral
   (vars (k akey))
   (defstrand init 2 (k k))
   (non-orig (invk k))
   (facts (foo 0 k)
	  (bar 0 (invk k))))

(defskeleton unilateral
   (vars (n text) (k akey))
   (defstrand resp 2 (n n) (k k))
   (pen-non-orig n)
   (non-orig (invk k)))

;;; The same two problems posed using security goals.  The goals were
;;; taken from the output of cpsasas.

(defgoal unilateral
  (forall ((n text) (k akey) (z strd))
    (implies
      (and (p "init" z 2) (p "init" "n" z n) (p "init" "k" z k)
        (non (invk k)) (uniq-at n z 0)
	(fact foo z k)
	(fact bar z (invk k)))
      (exists ((z-0 strd))
        (and (p "resp" z-0 2) (p "resp" "n" z-0 n) (p "resp" "k" z-0 k)
          (prec z 0 z-0 0) (prec z-0 1 z 1))))))

(defgoal unilateral
  (forall ((n text) (k akey) (z strd))
    (implies
      (and (p "resp" z 2) (p "resp" "n" z n) (p "resp" "k" z k)
        (non (invk k)) (pnon n))
      (exists ((k-0 akey) (z-0 strd))
        (and (p "init" z-0 1) (p "init" "n" z-0 n)
          (p "init" "k" z-0 k-0) (prec z-0 0 z 0) (uniq-at n z-0 0))))))

;;; Unilateral authentication from ISO/IEC JTC 1/SC 27/WG 2 N1050

(defprotocol iso-unilateral basic
  (defrole resp
    (vars (na nb t1 t2 t3 text) (b name))
    (trace
     (recv (cat nb t1))
     (send (cat na nb b t3 (enc na nb b t2 (privk b)))))
    (uniq-orig na))
  (defrole init
    (vars (na nb t1 t2 t3 text) (b name))
    (trace
     (send (cat nb t1))
     (recv (cat na nb b t3 (enc na nb b t2 (privk b)))))
    (uniq-orig nb))
  (comment "Two pass authentication"))

(defskeleton iso-unilateral
  (vars (b name))
  (defstrand init 2 (b b))
  (non-orig (privk b)))

;;; Same as above, but also checking to see if there was agreement.
(defgoal iso-unilateral
  (forall ((b name) (z strd))
    (implies
     (and (p "init" z 2)
	  (p "init" "b" z b)
	  (non (privk b)))
      (exists ((y strd))
	      (and (p "resp" y 2)
		   (p "resp" "b" y b))))))

;;; Silly example.  Of course the shape produced does not satisfy this
;;; goal!
(defgoal iso-unilateral
  (forall ((b name) (z strd))
    (implies
     (and (p "init" z 2)
	  (p "init" "b" z b)
	  (non (privk b)))
     (false))))
```

---

### `refrences/internet/examples_scm/factvar.scm`

*sha256:`fb9d3f74d9e3` · 32 lines · 0.7 KB · lang:`scheme`*

```scheme
(herald factvar)

;; An example of a rule that creates a variable that is
;; used in a fact but does not occur in a strand.

(defprotocol free-fact-var basic
  (defrole resp
    (vars (n text) (k akey))
    (trace
     (recv (enc n k))
     (send n)))

  (defrule add
    (forall ((z strd))
	    (implies
	     (p "resp" z 1)
	     (exists ((m text))
		     (fact thing m))))
    (comment "This rule adds a text variable")
    (comment "that does not appear in a strand"))
  )

(defskeleton free-fact-var
  (vars (k akey))
  (defstrand resp 1 (k k))
  (non-orig (invk k)))

(defskeleton free-fact-var
  (vars (n text) (k akey))
  (defstrand resp 1 (n n) (k k))
  (non-orig (invk k))
  (pen-non-orig n))
```

---

### `refrences/internet/examples_scm/ffgg.scm`

*sha256:`5b0ba3591e9d` · 24 lines · 0.7 KB · lang:`scheme`*

```scheme
(herald "The ffgg Protocol"
	(comment "From A Necessarily Parallel Attack by Jon K. Millen"))

(defprotocol ffgg basic
  (defrole init (vars (a b name) (n1 n2 m x y text))
    (trace
     (send a)
     (recv (cat b n1 n2))
     (send (cat a (enc n1 n2 m (pubk b))))
     (recv (cat n1 x (enc x y n1 (pubk b))))))
  (defrole resp (vars (b a name) (n1 n2 x y text))
    (trace
     (recv a)
     (send (cat b n1 n2))
     (recv (cat a (enc n1 x y (pubk b))))
     (send (cat n1 x (enc x y n1 (pubk b)))))
    (uniq-orig n1 n2)))

(defskeleton ffgg
  (vars (b name) (n1 n2 m text))
  (defstrand init 4 (b b) (m m))
  (deflistener m)
  (uniq-orig m)
  (non-orig (privk b)))
```

---

### `refrences/internet/examples_scm/fluffy_draft03_gske.scm`

*sha256:`c6039262563d` · 114 lines · 3.5 KB · lang:`scheme`*

```scheme
(herald "GSKE, part of Fluffy: Simplified Key Exchange for Constrained Environments draft-hardjono-ace-fluffy-03"
 (comment "Based on the Internet-Draft: https://www.ietf.org/archive/id/draft-hardjono-ace-fluffy-03.txt"))

;; This model does not include timestamps or optional fields.
(defprotocol fluffy basic
 (defrole sp
  (vars (b s name) (nb g text) (gk skey))
  (trace
   (send (cat "req" s g (enc b nb (ltk s b))))
   (recv (cat "resp" b (enc s g nb gk (ltk s b))))))
 (defrole keyserv
  (vars (a b s name) (nb na g text) (gk skey))
  (trace
   (recv (cat "req" s g (enc b nb (ltk s b))))
   (send (cat "resp" b (enc s g nb gk (ltk s b))))
   (recv (cat "fetch" s g (enc a na (ltk s a))))
   (send (cat "deliver" a (enc s g na gk (ltk s a)))))
  (uniq-gen gk))
 (defrole client
  (vars (a b s name) (na g text) (gk skey))
  (trace
   (send (cat "fetch" s g (enc a na (ltk s a))))
   (recv (cat "deliver" a (enc s g na gk (ltk s a)))))))

;; Service principal's (sp) point-of-view
(defskeleton fluffy
 (vars (b s name) (nb text) (gk skey))
 (defstrand sp 2 (b b) (s s) (nb nb) (gk gk))
 (non-orig (ltk s b))
 (uniq-orig nb)
 (comment "Service Principal's point-of-view"))

;; Simple key distribution center's (skdc) point-of-view
(defskeleton fluffy
 (vars (a b s name) (nb na text) (gk skey))
 (defstrand keyserv 4 (a a) (b b) (s s) (nb nb) (na na) (gk gk))
 (non-orig (ltk s b) (ltk s a))
 (uniq-gen gk)
 (comment "SKDC's point-of-view"))

;; Client's point-of-view
(defskeleton fluffy
 (vars (a s name) (na text) (gk skey))
 (defstrand client 2 (a a) (s s) (na na) (gk gk))
 (non-orig (ltk s a))
 (uniq-orig na)
 (comment "Clients's point-of-view"))

(defprotocol fluffy-rule basic
  (defrole sp
    (vars (b s name) (nb g text) (gk skey))
    (trace
     (send (cat "req" s g (enc b nb (ltk s b))))
     (recv (cat "resp" b (enc s g nb gk (ltk s b))))))
  (defrole keyserv
    (vars (a b s name) (nb na g text) (gk skey))
    (trace
     (recv (cat "req" s g (enc b nb (ltk s b))))
     (send (cat "resp" b (enc s g nb gk (ltk s b))))
     (recv (cat "fetch" s g (enc a na (ltk s a))))
     (send (cat "deliver" a (enc s g na gk (ltk s a)))))
    (uniq-gen gk))
  (defrole client
    (vars (a b s name) (na g text) (gk skey))
    (trace
     (send (cat "fetch" s g (enc a na (ltk s a))))
     (recv (cat "deliver" a (enc s g na gk (ltk s a))))))
  (defrule client-no-request
    (forall ((a s name) (y z strd))
	    (implies
	     (and
	      (p "client" z 1)
	      (p "client" "s" z s)
	      (p "client" "a" z a)
	      (p "keyserv" y 1)
	      (p "keyserv" "s" y s)
	      (p "keyserv" "b" y a))
	     (false))))
  (defrule sp-no-fetch
    (forall ((b s name) (y z strd))
	    (implies
	     (and
	      (p "sp" z 1)
	      (p "sp" "s" z s)
	      (p "sp" "b" z b)
	      (p "keyserv" y 3)
	      (p "keyserv" "s" y s)
	      (p "keyserv" "a" y b))
	     (false))))
  )

;; Service principal's (sp) point-of-view
(defskeleton fluffy-rule
 (vars (b s name) (nb text) (gk skey))
 (defstrand sp 2 (b b) (s s) (nb nb) (gk gk))
 (non-orig (ltk s b))
 (uniq-orig nb)
 (comment "Service Principal's point-of-view"))

;; Simple key distribution center's (skdc) point-of-view
(defskeleton fluffy-rule
 (vars (a b s name) (nb na text) (gk skey))
 (defstrand keyserv 4 (a a) (b b) (s s) (nb nb) (na na) (gk gk))
 (non-orig (ltk s b) (ltk s a))
 (uniq-gen gk)
 (comment "SKDC's point-of-view"))

;; Client's point-of-view
(defskeleton fluffy-rule
 (vars (a s name) (na text) (gk skey))
 (defstrand client 2 (a a) (s s) (na na) (gk gk))
 (non-orig (ltk s a))
 (uniq-orig na)
 (comment "Clients's point-of-view"))
```

---

### `refrences/internet/examples_scm/fragile_pruning.scm`

*sha256:`5c19c39ed044` · 45 lines · 1.2 KB · lang:`scheme`*

```scheme
;;; Illustrates how delicate pruning must be:
;;; to find a shape we must allow 3 almost
;;; identical instances of "adder", without
;;; pruning them even though they are renamings of
;;; each other.
;;; This goes to show that pruning is not justified
;;; in some cases even when the two strands are
;;; isomorphic.  What is lost by pruning here is merely
;;; the ability for a fresh variable of sort text to
;;; unify with a different already-existing variable of
;;; sort text without unifying the two existing ones.

(defprotocol fragile_pruning basic
  (defrole init (vars (k akey) (n n1 n2 n3 text))
    (trace
	(send (enc n k))
      (recv (enc n n1 k))
      (recv (enc n n2 k))
      (recv (enc n n3 k))
      (send (enc n n1 n2 n3 k))
      (recv (enc n n1 n2 n3 n k))
    )
    (uniq-orig n)
    (non-orig (invk k))
  )
  (defrole adder (vars (k akey) (n new text))
    (trace
      (recv (enc n k))
      (send (enc n new k))
    )
    (uniq-orig new)
  )
  (defrole final (vars (k akey) (n n1 n2 n3 text))
    (trace
       (recv (enc n n1 n2 n3 k))
       (send (enc n n1 n2 n3 n k))
    )
  )
)

(defskeleton fragile_pruning
  (vars (k akey) (n n1 n2 n3  text))
  (defstrand init 6 (k k) (n n) (n1 n1) (n2 n2) (n3 n3))
  (uniq-orig n1 n2 n3)
)
```

---

### `refrences/internet/examples_scm/goals.scm`

*sha256:`b1ae1766178a` · 240 lines · 7.5 KB · lang:`scheme`*

```scheme
(herald goals)

;;; Section 1 --- Examples from CPSA Security Goals and Rules

;;; Needham-Schroeder from Section 10 of the CPSA Primer

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder with no role origination assumptions"))

(defgoal ns
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and (p "init" z0 3)
      (p "init" "n1" z0 n1) (p "init" "b" z0 b)
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
	     (and (p "resp" z1 2) (p "resp" "b" z1 b)))))
  (comment "Initiator point of view")
  (comment "Authentication goal: agreement on name b"))

(defgoal ns
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and (p "init" z0 3)
      (p "init" "n1" z0 n1) (p "init" "b" z0 b)
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
	     (and (p "resp" z1 2) (p "resp" "b" z1 b)
	      (prec z1 1 z0 2)))))
  (comment "Prec example"))

(defgoal ns
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
     (and (p "resp" z0 3) (p "resp" "n2" z0 n2)
      (p "resp" "a" z0 a) (p "resp" "b" z0 b)
      (non (privk a)) (uniq n2))
     (exists ((z1 strd))
      (and (p "init" z1 2) (p "init" "b" z1 b)))))
  (comment "Responder point of view")
  (comment "Failed authentication goal: agreement on name b"))

(defprotocol nsl basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 b (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 b (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder-Lowe with no role origination assumptions"))

(defgoal nsl
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
     (and (p "resp" z0 3) (p "resp" "n2" z0 n2)
      (p "resp" "a" z0 a) (p "resp" "b" z0 b)
      (non (privk a)) (uniq n2))
     (exists ((z1 strd))
      (and (p "init" z1 2) (p "init" "b" z1 b)))))
  (comment "Responder point of view")
  (comment "Authentication goal: agreement on name b"))

(defgoal ns
  (forall ((a b name) (n1 text) (z0 z1 strd))
    (implies
     (and (p "init" z0 3) (p "init" "n1" z0 n1)
      (p "init" "a" z0 a) (p "init" "b" z0 b)
      (p "" z1 1) (p "" "x" z1 n1)
      (non (privk a)) (non (privk b)) (uniq n1))
     (false)))
  (comment "Initiator point of view")
  (comment "Secrecy goal: nonce n1 not revealed"))

(defprotocol unilateral basic
  (defrole init
    (vars (a name) (n text))
    (trace
     (send (enc n (pubk a)))
     (recv n)))
  (defrole resp
    (vars (a name) (n text))
    (trace
     (recv (enc n (pubk a)))
     (send n)))
  (comment "Unilateral authentication"))

(defgoal unilateral
  (forall ((a name) (n text)
           (z0 strd))
   (implies
    (and (p "init" z0 2)
     (p "init" "n" z0 n)
     (p "init" "a" z0 a)
     (non (privk a)) (uniq n))
    (exists ((z1 strd))
     (and (p "resp" z1 2)
      (p "resp" "a" z1 a)))))
  (comment "Unilateral authentication goal"))

;;; Does initiator satisfy the unilateral authentication goal?

;;; Note that the goal requires translation of some of the role
;;; specific predicates.
(defgoal ns
  (forall ((a name) (n text) (z0 strd))
   (implies
    (and (p "init" z0 2) (p "init" "n1" z0 n)
     (p "init" "b" z0 a) (non (privk a)) (uniq n))
    (exists ((z1 strd))
     (and (p "resp" z1 2) (p "resp" "b" z1 a)))))
  (comment "Initiator authentication goal")
  (comment "Same as unilateral goal under the predicate mapping:")
  (comment (p "init" "n") "->" (p "init" "n1") "and")
  (comment (p "init" "a") "->" (p "init" "b") "and")
  (comment (p "resp" "a") "->" (p "resp" "b")))

;;; Does responder satisfy the unilateral authentication goal?

(defgoal ns
  (forall ((a name) (n text) (z0 strd))
   (implies
    (and (p "resp" z0 3) (p "resp" "n2" z0 n)
     (p "resp" "a" z0 a) (non (privk a)) (uniq n))
    (exists ((z1 strd))
     (and (p "init" z1 3) (p "init" "a" z1 a)))))
  (comment "Responder authentication goal")
  (comment "Same as unilateral goal under the predicate mapping:")
  (comment (p "init" 1) "->" (p "resp" 2) "and")
  (comment (p "init" "n") "->" (p "resp" "n2") "and")
  (comment (p "init" "a") "->" (p "resp" "a") "and")
  (comment (p "resp" 1) "->" (p "init" 2) "and")
  (comment (p "resp" "a") "->" (p "init" "a")))

(defgoal ns
  (forall ((a b name) (n text) (z0 strd))
    (implies
     (and
      (p "init" z0 2) (p "init" "n1" z0 n)
      (p "init" "a" z0 a) (p "init" "b" z0 b)
      (non (privk a)) (non (privk b)) (uniq n))
     (exists ((z1 strd))
      (and (p "resp" z1 2) (p "resp" "b" z1 b)))))
  (forall ((a b name) (n text) (z0 strd))
   (implies
     (and
      (p "init" z0 2) (p "init" "n1" z0 n)
      (p "init" "a" z0 a) (p "init" "b" z0 b)
      (non (privk a)) (non (privk b)) (uniq n))
     (exists ((z1 strd))
      (and (p "resp" z1 2) (p "resp" "a" z1 a)))))
  (comment "Two initiator authentication goals"))

;;; The shape analysis sentence as input (kind of useless)

(defgoal ns
  (forall ((n1 n2 text) (b a name) (z strd))
    (implies
      (and (p "init" z 3) (p "init" "n1" z n1) (p "init" "n2" z n2)
        (p "init" "a" z a) (p "init" "b" z b) (non (privk b))
        (uniq-at n1 z 0))
      (exists ((n2-0 text) (z-0 strd))
        (and (p "resp" z-0 2) (p "resp" "n2" z-0 n2-0)
          (p "resp" "n1" z-0 n1) (p "resp" "b" z-0 b)
          (p "resp" "a" z-0 a) (prec z 0 z-0 0) (prec z-0 1 z 1)))))
  (comment "Shape analysis sentence"))

;;; Section 2 --- Additional Examples

(defgoal ns
  (forall ((a b name) (n2 text) (z0 z1 strd))
    (implies
     (and
      (p "resp" z0 3) (p "resp" "n2" z0 n2)
      (p "resp" "a" z0 a) (p "resp" "b" z0 b)
      (p "" z1 1) (p "" "x" z1 n2)
      (non (privk a)) (non (privk b)) (uniq n2))
     (false)))
  (comment "Responder point of view")
  (comment "Failed secrecy goal: nonce n2 not revealed"))

;;; Double initiator point of view
(defskeleton ns
  (vars (a b name) (n1 n1-0 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (defstrand init 3 (a a) (b b) (n1 n1-0))
  (non-orig (privk b) (privk a))
  (uniq-orig n1 n1-0)
  (goals
  (forall ((n1 n1-0 n2 n2-0 text) (a b name) (z z-0 strd))
    (implies
      (and (p "init" z 3) (p "init" z-0 3) (p "init" "n1" z n1)
        (p "init" "n2" z n2) (p "init" "a" z a) (p "init" "b" z b)
        (p "init" "n1" z-0 n1-0) (p "init" "n2" z-0 n2-0)
        (p "init" "a" z-0 a) (p "init" "b" z-0 b) (non (privk a))
        (non (privk b)) (uniq-at n1 z 0) (uniq-at n1-0 z-0 0))
      (= z z-0))))
  (comment "Double initiator point of view"))

(defprotocol nsl-typeless basic
  (defrole init
    (vars (a b name) (n1 text) (n2 mesg))
    (trace
     (send (enc a n1 (pubk b)))
     (recv (enc n1 n2 b (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 text) (n1 mesg))
    (trace
     (recv (enc a n1 (pubk b)))
     (send (enc n1 n2 b (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder-Lowe with untyped nonces"))

;;; The responder point of view
(defgoal nsl-typeless
  (forall ((n2 text) (a b name) (z z-0 strd))
    (implies
      (and (p "resp" z 2) (p "" z-0 1)
        (p "resp" "n2" z n2) (p "resp" "b" z b) (p "resp" "a" z a)
        (p "" "x" z-0 n2) (non (privk a)) (non (privk b)) (uniq n2))
      (false)))
  (comment "Shows typeflaw in typeless NSL"))
```

---

### `refrences/internet/examples_scm/goalsvar.scm`

*sha256:`0d26a1fa46e2` · 229 lines · 6.7 KB · lang:`scheme`*

```scheme
(herald goalsvar)

;;; Section 1 --- Examples from CPSA and Formal Security Goals

;;; Needham-Schroeder from Section 10 of the CPSA Primer

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder with no role origination assumptions"))

(defgoal ns
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and 
      (strand init z0 3 (n1 n1) (b b))
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
	     (strand resp z1 2 (b b)))))
  (comment "Initiator point of view")
  (comment "Authentication goal: agreement on name b"))

(defgoal ns
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and (strand init z0 3 (n1 n1) (b b))
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
        (and 
          (strand resp z1 2 (b b))
	      (prec z1 1 z0 2)))))
  (comment "Prec example"))

(defgoal ns
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
     (and (strand resp z0 3 (n2 n2) (a a) (b b))
      (non (privk a)) (uniq n2))
     (exists ((z1 strd))
      (strand init z1 2 (b b)))))
  (comment "Responder point of view")
  (comment "Failed authentication goal: agreement on name b"))

(defprotocol nsl basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 b (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 b (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder-Lowe with no role origination assumptions"))

(defgoal nsl
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
     (and (strand resp z0 3 (n2 n2) (a a) (b b))
      (non (privk a)) (uniq n2))
     (exists ((z1 strd))
      (strand init z1 2 (b b)))))
  (comment "Responder point of view")
  (comment "Authentication goal: agreement on name b"))

(defgoal ns
  (forall ((a b name) (n1 text) (z0 z1 strd))
    (implies
     (and (strand init z0 3 (n1 n1) (a a) (b b))
      (listener z1 n1)
      (non (privk a)) (non (privk b)) (uniq n1))
     (false)))
  (comment "Initiator point of view")
  (comment "Secrecy goal: nonce n1 not revealed"))

(defprotocol unilateral basic
  (defrole init
    (vars (a name) (n text))
    (trace
     (send (enc n (pubk a)))
     (recv n)))
  (defrole resp
    (vars (a name) (n text))
    (trace
     (recv (enc n (pubk a)))
     (send n)))
  (comment "Unilateral authentication"))

(defgoal unilateral
  (forall ((a name) (n text)
           (z0 strd))
   (implies
    (and (strand init z0 2 (n n) (a a))
     (non (privk a)) (uniq n))
    (exists ((z1 strd))
     (strand resp z1 2 (a a)))))
  (comment "Unilateral authentication goal"))

;;; Does initiator satisfy the unilateral authentication goal?

;;; Note that the goal requires translation of some of the role
;;; specific predicates.
(defgoal ns
  (forall ((a name) (n text) (z0 strd))
   (implies
    (and (strand init z0 2 (n1 n) (b a))
      (non (privk a)) (uniq n))
    (exists ((z1 strd))
     (strand resp z1 2 (b a)))))
  (comment "Initiator authentication goal")
  (comment "Same as unilateral goal under the predicate mapping:")
  (comment (p "init" "n") "->" (p "init" "n1") "and")
  (comment (p "init" "a") "->" (p "init" "b") "and")
  (comment (p "resp" "a") "->" (p "resp" "b")))

;;; Does responder satisfy the unilateral authentication goal?

(defgoal ns
  (forall ((a name) (n text) (z0 strd))
   (implies
    (and (strand resp z0 3 (n2 n) (a a))
     (non (privk a)) (uniq n))
    (exists ((z1 strd))
     (strand init z1 3 (a a)))))
  (comment "Responder authentication goal")
  (comment "Same as unilateral goal under the predicate mapping:")
  (comment (p "init" 1) "->" (p "resp" 2) "and")
  (comment (p "init" "n") "->" (p "resp" "n2") "and")
  (comment (p "init" "a") "->" (p "resp" "a") "and")
  (comment (p "resp" 1) "->" (p "init" 2) "and")
  (comment (p "resp" "a") "->" (p "init" "a")))

(defgoal ns
  (forall ((a b name) (n text) (z0 strd))
    (implies
     (and (strand init z0 2 (n1 n) (a a) (b b))
      (non (privk a)) (non (privk b)) (uniq n))
     (exists ((z1 strd))
      (strand resp z1 2 (b b)))))
  (forall ((a b name) (n text) (z0 strd))
   (implies
     (and (strand init z0 2 (n1 n) (a a) (b b))
      (non (privk a)) (non (privk b)) (uniq n))
     (exists ((z1 strd))
      (strand resp z1 2 (a a)))))
  (comment "Two initiator authentication goals"))

;;; The shape analysis sentence as input (kind of useless)

(defgoal ns
  (forall ((n1 n2 text) (b a name) (z strd))
    (implies
      (and (strand init z 3 (n1 n1) (n2 n2) (a a) (b b))
        (non (privk b))
        (uniq-at n1 z 0))
      (exists ((n2-0 text) (z-0 strd))
        (and (strand resp z-0 2 (n2 n2-0) (n1 n1) (b b) (a a))
          (prec z 0 z-0 0) (prec z-0 1 z 1)))))
  (comment "Shape analysis sentence"))

;;; Section 2 --- Additional Examples

(defgoal ns
  (forall ((a b name) (n2 text) (z0 z1 strd))
    (implies
     (and
      (strand resp z0 3 (n2 n2) (a a) (b b))
      ;; Still have to add support for a listener formula: 
      (listener z1 n2)
      (non (privk a)) (non (privk b)) (uniq n2))
     (false)))
  (comment "Responder point of view")
  (comment "Failed secrecy goal: nonce n2 not revealed"))

;;; Double initiator point of view
(defskeleton ns
  (vars (a b name) (n1 n1-0 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (defstrand init 3 (a a) (b b) (n1 n1-0))
  (non-orig (privk b) (privk a))
  (uniq-orig n1 n1-0)
  (goals
  (forall ((n1 n1-0 n2 n2-0 text) (a b name) (z z-0 strd))
    (implies
      (and 
        (strand init z 3 (n1 n1) (n2 n2) (a a) (b b))
        (strand init z-0 3 (n1 n1-0) (n2 n2-0) (a a) (b b))
        (non (privk a))
        (non (privk b)) (uniq-at n1 z 0) (uniq-at n1-0 z-0 0))
      (= z z-0))))
  (comment "Double initiator point of view"))

(defprotocol nsl-typeless basic
  (defrole init
    (vars (a b name) (n1 text) (n2 mesg))
    (trace
     (send (enc a n1 (pubk b)))
     (recv (enc n1 n2 b (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 text) (n1 mesg))
    (trace
     (recv (enc a n1 (pubk b)))
     (send (enc n1 n2 b (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder-Lowe with untyped nonces"))

;;; The responder point of view
(defgoal nsl-typeless
  (forall ((n2 text) (a b name) (z z-0 strd))
    (implies
      (and (strand resp z 2 (n2 n2) (b b) (a a))
        (listener z-0 n2)
        (non (privk a)) (non (privk b)) (uniq n2))
      (false)))
  (comment "Shows typeflaw in typeless NSL"))
```

---

### `refrences/internet/examples_scm/hashtest-key-hash.scm`

*sha256:`a9914930ffa5` · 25 lines · 0.4 KB · lang:`scheme`*

```scheme
;;; Hashtest.scm is designed to test if the
;;; hash is working properly.
(herald "Hashtest")

(defprotocol hashtest basic
  (defrole init (vars (n data) (k akey))
     (trace
       (send (enc n k))
       (recv (enc "h" n))
     )
     (uniq-orig n)
     (non-orig (invk k))
   )
   (defrole resp (vars (k akey) (n data))
     (trace
       (recv (enc n k))
       (send (enc "h" n))
     )
   )
)

(defskeleton hashtest
   (vars)
   (defstrand init 2)
)
```

---

### `refrences/internet/examples_scm/hashtest.scm`

*sha256:`3ff3a8f0d1cc` · 25 lines · 0.4 KB · lang:`scheme`*

```scheme
;;; Hashtest.scm is designed to test if the
;;; hash is working properly.
(herald "Hashtest")

(defprotocol hashtest basic
  (defrole init (vars (n data) (k akey))
     (trace
       (send (enc n k))
       (recv (hash n))
     )
     (uniq-orig n)
     (non-orig (invk k))
   )
   (defrole resp (vars (k akey) (n data))
     (trace
       (recv (enc n k))
       (send (hash n))
     )
   )
)

(defskeleton hashtest
   (vars)
   (defstrand init 2)
)
```

---

### `refrences/internet/examples_scm/incompleteness_example.scm`

*sha256:`d6fcb0502d3d` · 21 lines · 0.6 KB · lang:`scheme`*

```scheme
(herald incompleteness-example
  (comment "Shows a shape not found by CPSA"))

(defprotocol incompleteness-example basic
  (defrole init (vars (k akey) (n text))
    (trace (send (enc n k)) (recv n))
    (uniq-orig n))
  (defrole resp (vars (k akey) (n1 n2 text))
    (trace (recv (enc n1 k)) (send n2))))

(defskeleton incompleteness-example
  (vars (k akey))
  (defstrand init 2 (k k))
  (non-orig (invk k)))

(defskeleton incompleteness-example
  (vars (k akey) (n text))
  (defstrand init 2 (k k) (n n))
  (defstrand resp 2 (k k) (n1 n) (n2 n))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (comment "A shape compatible with the first problem in this run"))
```

---

### `refrences/internet/examples_scm/isoreject-corrected.scm`

*sha256:`caf4ace8ece3` · 24 lines · 0.6 KB · lang:`scheme`*

```scheme
(herald isoreject-corrected)

(defprotocol isofix basic
  (defrole init (vars (a b name) (na nb nc text))
    (trace
     (send (cat a na))
     (recv (enc "first" nb na a (privk b)))
     (send (enc "second" nc nb b (privk a)))))
  (defrole resp (vars (a b name) (na nb nc text))
    (trace
     (recv (cat a na))
     (send (enc "first" nb na a (privk b)))
     (recv (enc "second" nc nb b (privk a))))
    (uniq-orig nb)))

(defskeleton isofix
  (vars (a b name))
  (defstrand resp 3 (a a) (b b))
  (non-orig (privk a) (privk b)))

(defskeleton isofix
  (vars (b name))
  (defstrand init 3 (b b))
  (non-orig (privk b)))
```

---

### `refrences/internet/examples_scm/isoreject.scm`

*sha256:`9280d47d1adc` · 22 lines · 0.6 KB · lang:`scheme`*

```scheme
(defprotocol isoreject basic
  (defrole init (vars (a b name) (na nb nc text))
    (trace
     (send (cat a na))
     (recv (enc nb na a (privk b)))
     (send (enc nc nb b (privk a)))))
  (defrole resp (vars (a b name) (na nb nc text))
    (trace
     (recv (cat a na))
     (send (enc nb na a (privk b)))
     (recv (enc nc nb b (privk a))))
    (uniq-orig nb)))

(defskeleton isoreject
  (vars (a b name))
  (defstrand resp 3 (a a) (b b))
  (non-orig (privk a) (privk b)))

(defskeleton isoreject
  (vars (b name))
  (defstrand init 3 (b b))
  (non-orig (privk b)))
```

---

### `refrences/internet/examples_scm/kelly1.scm`

*sha256:`757b6d34a380` · 76 lines · 2.1 KB · lang:`scheme`*

```scheme
;;An attestation protocol containing a client, a server, and an appraiser.

;;The client is attempting to verify that the server he receives his
;;content from is the server he wishes to communicate with, and that the
;;server meets some policy.

;;The appraiser acquires measurements from the server to determine the
;;policy, and passes the resulting policy on to the client. The server's
;;public key is used to identify the server.

;;The server is verifying nothing about his surroundings, and will
;;answer both measurement and content inquiries from anyone.

;;When analyzing this protocol, it is assumes that the client knows some
;;appraiser he trusts; the client analysis should contain non privk(A).

(defprotocol kelly1 basic

  (defrole client
    (vars (C name) (A name) (S name) (Ns text) (request text) (Check text)  (policy text) (response text))
    (trace
     (send (cat C S request))
     (recv (cat S C (enc (cat response Ns)
			 (privk S))))
     (send (cat C A Check (pubk S)))
     (recv (cat A C (enc (cat policy (pubk S) Ns)
			 (privk A))))
      )
    )

  (defrole appraiser
    (vars (C name) (A name) (S name) (N text) (Ns text) (hello text)
	  (Quote text) (measurements text) (Check text) (policy text)
	  (AIK name))
    (trace
     (recv (cat S A hello))
     (send (cat A S N))
     (recv (cat S A
		(enc
		 (cat Quote measurements N Ns (pubk S))
		 (privk AIK))
		(pubk S)))
     (recv (cat C A Check (pubk S)))
     (send (cat A C (enc (cat policy (pubk S) Ns)
			 (privk A))))
      )
    (non-orig (privk A) (privk AIK))
    (uniq-orig N)
    )

  (defrole server
    (vars (C name) (A name) (S name) (N text) (Ns text) (hello text)
	  (Quote text) (measurements text) (request text) (response text)
	  (AIK name))
   (trace
      (send (cat S A hello))
      (recv (cat A S N))
      (send (cat S A
		 (enc
		  (cat Quote measurements N Ns (pubk S))
		  (privk AIK))
		 (pubk S)))
      (recv (cat C S request))
      (send (cat S C (enc (cat response Ns)
			  (privk S))))
      )
   (non-orig (privk S) (privk AIK))
   (uniq-orig  Ns)
   )
)

(defskeleton kelly1
  (vars (A name))
  (defstrand client 4 (A A))
  (non-orig (privk A))
  )
```

---

### `refrences/internet/examples_scm/kerberos.scm`

*sha256:`63adf8e0bcea` · 37 lines · 1.3 KB · lang:`scheme`*

```scheme
(defprotocol kerberos basic
  (defrole init
    (vars (a name) (b name) (ks name) (t text) (t-prime text) (l text) (k skey))
    (trace (send (cat a b))
      (recv
        (cat (enc (cat t l k b) (ltk a ks))
          (enc (cat t l k a) (ltk b ks))))
      (send (cat (enc (cat a t) k) (enc (cat t l k a) (ltk b ks))))
      (recv (enc t-prime k))))
  (defrole resp
    (vars (a name) (b name) (ks name) (t text) (t-prime text) (l text) (k skey))
    (trace (recv (cat (enc (cat a t) k) (enc (cat t l k a) (ltk b ks))))
      (send (enc t-prime k))))
  (defrole keyserver
    (vars (a name) (b name) (ks name) (t text) (l text) (k skey))
    (trace (recv (cat a b))
      (send
        (cat (enc (cat t l k b) (ltk a ks))
          (enc (cat t l k a) (ltk b ks))))) (uniq-orig k)))

; we'll observe two shapes resulting from these preskeletons
; because the keyserver can reverse a and b with no change
; in the protocol
(defskeleton kerberos
  (vars (a name) (b name) (ks name))
  (defstrand init 4 (a a) (b b) (ks ks))
  (non-orig (ltk a ks) (ltk b ks)))

(defskeleton kerberos
  (vars (a name) (b name) (ks name))
  (defstrand resp 2 (a a) (b b) (ks ks))
  (non-orig (ltk a ks) (ltk b ks)))

(defskeleton kerberos
  (vars (a name) (b name) (ks name))
  (defstrand keyserver 2 (a a) (b b) (ks ks))
  (non-orig (ltk a ks) (ltk b ks)))
```

---

### `refrences/internet/examples_scm/lemmas.scm`

*sha256:`c815266aaa57` · 61 lines · 1.7 KB · lang:`scheme`*

```scheme
(herald goalsvar)

;;; Section 1 --- Examples from CPSA and Formal Security Goals

;;; Needham-Schroeder from Section 10 of the CPSA Primer

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder with no role origination assumptions"))

(deflemma rule lemma1 ns
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and 
      (strand init z0 3 (n1 n1) (b b))
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
	     (strand resp z1 2 (b b)))))
  (comment "Skeleton 1")
  (comment "Authentication goal: agreement on name b"))

(deflemma both lemma2 ns
  (forall ((b name) (n1 text) (z0 strd))
    (implies
     (and (strand init z0 3 (n1 n1) (b b))
      (non (privk b)) (uniq n1))
     (exists ((z1 strd))
        (and 
          (strand resp z1 2 (b b))
	      (prec z1 1 z0 2)))))
  (comment "Prec example. Skeleton 2"))

(deflemma goal lemma3 ns
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
     (and (strand resp z0 3 (n2 n2) (a a) (b b))
      (non (privk a)) (uniq n2))
     (exists ((z1 strd))
      (strand init z1 2 (b b)))))
  (comment "Skeleton 3")
  (comment "Failed authentication goal: agreement on name b"))

(defgoal ns
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
     (and (strand resp z0 3 (n2 n2) (a a) (b b))
      (non (privk a)) (uniq n2))
     (exists ((z1 strd))
      (strand init z1 2 (b b)))))
  (comment "Skeleton 4"))
```

---

### `refrences/internet/examples_scm/locn_envelope.scm`

*sha256:`b76bdb322e9d` · 254 lines · 8.1 KB · lang:`scheme`*

```scheme
(herald "Envelope Protocol, location-based version"
	(bound 30)
	(limit 1200))

;;; This file analyzes the Envelope Protocol using three rules sets.
;;; For each rule set, it checks three scenarios.  In every scenario,
;;; an Alice strand runs to completion.  In the first scenario, the
;;; obtain token is listened for.  In the second, a listener for the
;;; refusal token is included.  In the third scenario, both listeners
;;; are included.  The third scenario should be impossible, but rules
;;; are required to accurately model state.
;;;
;;; The first rule set is empty and the answer to the third scenario
;;; shows a case is which the TPM's PCR state splits.  The second rule
;;; set forces TPM extends to be linearly ordered.  However, in this
;;; case, there are two TPMs when there should be one as Alice uses
;;; one TPM storage key to communicate with both TPMs.  The final rule
;;; set includes a rule about storage keys and thus accurately models
;;; state.
;;;
;;; Macros are used to avoid copying roles and scenarios.

;; This is the refusal token
(defmacro (refuse pcr-id n v k aik)
  (enc "quote" pcr-id (hash (hash "0" n) "refuse") (enc v k) aik))

;;; This protocol tracks the TPM's PCR state
;;; by sending a message with the current PCR
;;; value encrypted by a hashed secret key.
;;; The hash is used to prevent a confusion with
;;; the key for an encrypted session.

(defmacro (roles)
  (^
   ;; Power on sets the pcr to 0
   (defrole tpm-power-on
     (vars (current-value mesg) (pcr locn) (tpm chan))
     (trace
      (recv tpm "power on")
      (load pcr current-value)
      (stor pcr "0")))

   ;; The extend command takes the value to extend and the current PCR
   ;; value and produces the hash of the two values.
   ;;     (defrole tpm-extend
   ;;        (vars (value current-value mesg) (pcr locn))
   ;;        (trace
   ;;         (recv (cat "extend" value))
   ;;         (recv pcr current-value)		    ;; MSR lhs (deleted)
   ;;         (stor pcr (hash current-value value)) ;; MSR rhs
   ;;         (send "ext ok")))

   ;; The extend command can also occur within an
   ;; encrypted session.  We assume some session key already exists
   (defrole tpm-extend-enc
     (vars (value current-value mesg) (pcr-id text) (pcr locn) (tpm chan))
     (trace
      (recv tpm (cat "extend" pcr-id value))
      (load pcr current-value)		    ;; MSR lhs (deleted)
      (stor pcr (hash current-value value)) ;; MSR rhs
      (send "ext ok")))

   ;; The TPM must retrieve the current pcr value.  Notice that
   ;; the nonce is of sort mesg, which allows non-atomic values.
   (defrole tpm-quote
     (vars (nonce current-value mesg) (pcr-id text) (aik akey) (pcr locn) (tpm chan))
     (trace
      (recv tpm (cat "quote" pcr-id nonce))
      (load pcr current-value) ;; MSR lhs (not deleted)
      (send (enc "quote" pcr-id current-value nonce aik))))

   ;; This role creates a key whose use is restricted to a
   ;; requested pcr value (since we only model one pcr).
   ;; It doesn't create or change any TPM state.
   (defrole tpm-create-key
     (vars (k aik akey) (pcr-id text) (pcrval mesg) (tpm chan))
     (trace
      (recv tpm (cat "create-req" pcr-id pcrval))
      (send (enc "created" k pcr-id pcrval aik))) ;; no tpm state is set
     (uniq-orig k)
     (non-orig (invk k))
     (auth tpm))

   ;; This role receives an encryption and a previously
   ;; made key structure that restricts the decryption key
   ;; to be used with a certain pcr value.  It retrieves the
   ;; current value and checks that it matches before decrypting.
   (defrole tpm-decrypt
     (vars (m current-value mesg) (pcr-id text) (k aik akey) (pcr locn) (tpm chan))
     (trace
      (recv tpm (cat "decrypt" (enc m k)))
      (recv (enc "created" k pcr-id current-value aik))
      (load pcr current-value) ;; MSR lhs (not deleted)
      (send m))
     (non-orig aik))

   ;; Alice extends a pcr with a fresh nonce in an encrypted
   ;; session.  She has the TPM create a new key whose use is
   ;; bound to the hash of pcr value she just created with the
   ;; string "obtain".  She then encrypts her fresh secret with
   ;; this newly created key.
   (defrole alice
     (vars (n v data) (pcr-id text) (k aik akey) (tpm chan))
     (trace
      (send tpm (cat "extend" pcr-id n))
      (send tpm (cat "create-req"pcr-id (hash (hash "0" n) "obtain")))
      ;; (enc "create key" (hash (hash "0" n) "obtain") esk)
      (recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))
      (send (enc v k)))
     (neq (k aik))
     (uniq-orig n v)
     (non-orig aik)
     (conf tpm))))

(defmacro (genStV-rules)
  (^
   (defrule genStV-if-hashed-tpm-power-on
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-power-on" z 2)
	(p "tpm-power-on" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

;;      (defrule genStV-if-hashed-tpm-extend
;;        (forall
;;         ((z strd) (v1 v2 mesg))
;;         (implies
;;          (and
;;   	(p "tpm-extend" z 2)
;;   	(p "tpm-extend" "current-value" z (hash v1 v2)))
;;          (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-extend-enc
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-extend-enc" z 2)
	(p "tpm-extend-enc" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-decrypt
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-decrypt" z 3)
	(p "tpm-decrypt" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-quote
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-quote" z 2)
	(p "tpm-quote" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))))

(defprotocol envelope basic
  (roles)
  (genStV-rules)
  )

(defskeleton envelope
  (vars (v data))
  (deflistener v)
  (defstrand alice 4 (v v)))

(defskeleton envelope
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (deflistener v)
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defprotocol envelope-plus basic
  (roles)
  (genStV-rules)

  (defrule ordered-extends
    (forall ((y z strd) (pcr locn))
	    (implies
	     (and (p "tpm-extend-enc" y 3)
		  (p "tpm-extend-enc" z 3)
		  (p "tpm-extend-enc" "pcr" y pcr)
		  (p "tpm-extend-enc" "pcr" z pcr))
	     (or (= y z)
		 (prec y 2 z 1)
		 (prec z 2 y 1))))))

(defskeleton envelope-plus
  (vars (v data))
  (deflistener v)
  (defstrand alice 4 (v v)))

(defskeleton envelope-plus
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope-plus
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (deflistener v)
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defprotocol envelope-plus-2 basic
  (roles)
  (genStV-rules)

  ;;   (defrule ordered-extends
;;       (forall ((y z strd) (pcr locn))
;;   	    (implies
;;   	     (and (p "tpm-extend-enc" y 3)
;;   		  (p "tpm-extend-enc" z 3)
;;   		  (p "tpm-extend-enc" "pcr" y pcr)
;;   		  (p "tpm-extend-enc" "pcr" z pcr))
;;   	     (or (= y z)
;;   		 (prec y 2 z 1)
;;   		 (prec z 2 y 1)))))

  (defrule pcr-id-identifies-pcr
    (forall ((y z strd) (pcr-id text) (pcr pcr-0 locn))
	    (implies
	     (and (p "tpm-extend-enc" y 3)
		  (p "tpm-extend-enc" z 3)
		  (p "tpm-extend-enc" "pcr-id" y pcr-id)
		  (p "tpm-extend-enc" "pcr-id" z pcr-id)
		  (p "tpm-extend-enc" "pcr" y pcr)
		  (p "tpm-extend-enc" "pcr" z pcr-0))
	     (= pcr pcr-0)))))

(defskeleton envelope-plus-2
  (vars (v data))
  (deflistener v)
  (defstrand alice 4 (v v)))

(defskeleton envelope-plus-2
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope-plus-2
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (deflistener v)
  (defstrand alice 4 (n n) (v v) (k k) (aik aik)))
```

---

### `refrences/internet/examples_scm/missing_contraction.scm`

*sha256:`327190aada48` · 54 lines · 1.8 KB · lang:`scheme`*

```scheme
; missing-contraction
;   The purpose in creating this example was to see if
; CPSA would stubmle when it should find a substitution to
; solve a test node that ultimately unifies the reception
; with something *not* in the escape set.  In this case,
; the receiver's reception is unexplained.  Ordinary
; contraction finds the map that unifies the names a and b
; but (enc a n (pubk b)) is not part of the escape set so
; contraction does not find the substitution that unifies
; n and m.
;   Contraction doesn't work that way but CPSA does have
; another route to finding that shape, but it involves
; augmentation, or more correctly, displacement.  A
; displacement will create a sender that uses m as its n,
; and will unify this with the existing sender, resulting
; effectively in the substitution we were looking for.
;   At the time, CPSA failed to do this, because the map
; that collapses the two sender strands is not a homomorphism
; because it changes the origination point of m on the new
; strand.

(defprotocol missing-contraction basic
  (defrole sender
    (vars (m n text) (a b name))
    (trace
     (send (enc a m (pubk a)))
     (send (enc a n (pubk b)))))
  (defrole receiver
    (vars (m text) (a b name))
    (trace
     (recv (enc a m (pubk b))))))

(defskeleton missing-contraction
  (vars (m text) (a c name))
  (defstrand sender 2 (m m) (a a))
  (defstrand receiver 1 (m m) (a a) (b c))
  (precedes ((0 1) (1 0)))
  (uniq-orig m)
  (non-orig (privk a)))

(defskeleton missing-contraction
  (vars (m text) (a c name))
  (defstrand sender 1 (m m) (a a))
  (deflistener (enc a m (pubk c)))
  (uniq-orig m)
  (non-orig (privk a)))

(defskeleton missing-contraction
  (vars (m text) (a b c name))
  (defstrand sender 2 (m m) (a a) (b b))
  (defstrand receiver 1 (m m) (a a) (b c))
  (precedes ((0 1) (1 0)))
  (uniq-orig m)
  (non-orig (privk a) (privk b)))
```

---

### `refrences/internet/examples_scm/neq_test.scm`

*sha256:`0602413ce18e` · 30 lines · 0.7 KB · lang:`scheme`*

```scheme
(herald "Inequality constraint using facts and rules"
	(comment "First skeleton should have a shape,"
		 "second should be dead."))

(defprotocol neq-test basic
  (defrole init
    (vars (n1 n2 text) (k skey))
    (trace
     (send (cat n1 (enc n1 n2 k)))
     (recv n2))
    (non-orig k)
    (uniq-orig n1 n2))
  (defrule neq
    (forall ((a mesg))
	    (implies
	     (fact neq a a)
	     (false)))))

;;; With no inequality fact,
;;; a shape should be found where n1 = n2.
(defskeleton neq-test
  (vars)
  (defstrand init 2))

;;; With an inequality fact,
;;; no shape should exist.
(defskeleton neq-test
   (vars (n1 n2 text))
   (defstrand init 2 (n1 n1) (n2 n2))
   (facts (neq n1 n2)))			;  assert n1 != n2
```

---

### `refrences/internet/examples_scm/neuman-stubblebine.scm`

*sha256:`c2208789c13a` · 37 lines · 1.2 KB · lang:`scheme`*

```scheme
(defprotocol neuman-stubblebine basic
  (defrole init (vars (a b ks name) (ra rb text) (k skey) (tb text))
    (trace
     (send (cat a ra))
     (recv (cat (enc b ra k tb (ltk a ks))
		(enc a k tb (ltk b ks)) rb))
     (send (cat (enc a k tb (ltk b ks)) (enc rb k)))))
  (defrole resp (vars (a b ks name) (ra rb text) (k skey) (tb text))
    (trace
     (recv (cat a ra))
     (send (cat b rb (enc a ra tb (ltk b ks))))
     (recv (cat (enc a k tb (ltk b ks)) (enc rb k)))))
  (defrole keyserver
    (vars (a b ks name) (ra rb text) (k skey) (tb text))
    (trace
     (recv (cat b rb (enc a ra tb (ltk b ks))))
     (send (cat (enc b ra k tb (ltk a ks))
		(enc a k tb (ltk b ks)) rb)))
    (uniq-orig k)))

(defskeleton neuman-stubblebine
  (vars (a b ks name) (ra rb text))
  (defstrand init 3 (a a) (b b) (ks ks) (ra ra) (rb rb))
  (uniq-orig ra rb)
  (non-orig (ltk a ks) (ltk b ks)))

(defskeleton neuman-stubblebine
  (vars (a b ks name) (ra rb text))
  (defstrand resp 3 (a a) (b b) (ks ks) (ra ra) (rb rb))
  (uniq-orig ra rb)
  (non-orig (ltk a ks) (ltk b ks)))

(defskeleton neuman-stubblebine
  (vars (a b ks name) (ra rb text))
  (defstrand keyserver 2 (a a) (b b) (ks ks) (ra ra) (rb rb))
  (uniq-orig ra rb)
  (non-orig (ltk a ks) (ltk b ks)))
```

---

### `refrences/internet/examples_scm/no_contraction.scm`

*sha256:`160793310026` · 16 lines · 0.4 KB · lang:`scheme`*

```scheme
(defprotocol no-contraction basic
  (defrole init
    (vars (a b name) (n text))
    (trace
     (send (enc (enc n (privk a))(pubk b)))))
  (defrole resp
    (vars (a name) (n text))
    (trace
     (recv (enc n (privk a))))))

(defskeleton no-contraction
  (vars (a b name) (n m text))
  (defstrand resp 1 (a a) (n n))
  (defstrand init 1 (n n))
  (uniq-orig n)
  (non-orig (privk a)))
```

---

### `refrences/internet/examples_scm/non_transforming.scm`

*sha256:`ec45277f12c7` · 42 lines · 1.0 KB · lang:`scheme`*

```scheme
; non_transforming.scm --
;  Illustrates a bug.  In the given
; POV, if we try an augmentation with
; (breaker 3), cowt causes a unification
; that makes the 3rd node no longer a
; transforming node, because the same
; message is sent at the 2nd node.

(defprotocol non_transforming basic
  (defrole sender
    (vars (a b text) (B name))
    (trace
      (send (enc a b (pubk B)))
    )
    (uniq-orig a b)
    (non-orig (privk B))
  )
  (defrole recv
    (vars (a b text) (B name))
    (trace
      (recv (enc a (pubk B)))
      (recv (enc b (pubk B)))
    )
  )
  (defrole breaker
    (vars (a b text) (B name))
    (trace
       (recv (enc a b (pubk B)))
       (send (enc a (pubk B)))
       (send (enc b (pubk B)))
    )
  )
)

(defskeleton non_transforming
  (vars (a b c d text) (B B0 B1 name))
  (defstrand recv 2 (a a) (b b) (B B))
  (defstrand sender 1 (a a) (b d) (B B0))
  (defstrand sender 1 (a c) (b b) (B B1))
  (precedes ((1 0) (0 0)) ((2 0) (0 1)))
  (uniq-orig a b)
)
```

---

### `refrences/internet/examples_scm/nonaug-prune.scm`

*sha256:`5274cf847e16` · 42 lines · 1.2 KB · lang:`scheme`*

```scheme
;; This protocol shows that it is possible to prune
;; two strands of a parent skeleton after augmenting
;; with a new strand.

(defprotocol nonaug-prune basic
  (defrole orig
    (vars (n text) (A B name) (k akey))
    (trace
     (send (enc n B B k))
     (send (enc n A k))
     (recv (enc n A A A k)))
    (uniq-orig n)
    (non-orig (invk k)))
  (defrole trans1
    (vars (n text) (A C name) (k akey))
    (trace
     (recv (enc n A A k))
     (recv (enc n A k))
     (send (enc n n C k))))
  (defrole trans2
    (vars (n text) (A name) (k akey))
    (trace
     (recv (enc n A k))
     (send (enc n A A A k))))
)

;; (defskeleton nonaug-prune
;;   (vars (n text) (A B C name) (k akey))
;;   (defstrand trans1 3 (n n) (A A) (C C) (k k))
;;   (defstrand orig 3 (n n) (A A) (B B) (k k))
;;   (precedes ((1 0) (0 0)) ((0 2) (1 2))))

;; (defskeleton nonaug-prune
;;   (vars (n text) (A B name) (k akey))
;;   (defstrand orig 3 (n n) (A A) (B B) (k k)))

(defskeleton nonaug-prune
  (vars (n text) (A B name) (k akey))
  (defstrand trans2 2 (n n) (A B) (k k))
  (defstrand trans2 2 (n n) (A A) (k k))
  (defstrand orig 3 (n n) (A A)(B B) (k k))
  (precedes ((2 0) (0 0)) ((2 0) (1 0))))
```

---

### `refrences/internet/examples_scm/ns-l.scm`

*sha256:`1eebc4fe0c3f` · 38 lines · 1.0 KB · lang:`scheme`*

```scheme
(herald "Needham-Schroeder-Low Public-Key Protocol"
	(comment "With deflistener's"))

;;; Used to generate output for inclusion in the primer.
;;; Use margin = 60 (-m 60) to generate the output.

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc b n1 n2 (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc b n1 n2 (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder"))

;;; The initiator point-of-view
(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (deflistener n1)
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Initiator point-of-view with a listener"))

;;; The responder point-of-view
(defskeleton ns
  (vars (a name) (n2 text))
  (defstrand resp 3 (a a) (n2 n2))
  (deflistener n2)
  (non-orig (privk a))
  (uniq-orig n2)
  (comment "Responder point-of-view with a listener"))
```

---

### `refrences/internet/examples_scm/ns-rebinding.scm`

*sha256:`f9af085a3c0b` · 103 lines · 2.7 KB · lang:`scheme`*

```scheme
(comment
 (defrole keyserver
   (vars (a name) (b name) (ks name) (t text) (l text) (sk kas kbs skey))
   (trace
    (recv (cat a b))
    (guar (and (long-term-key ks a kas)
	       (long-term-key ks b kbs)))
    (send
     (cat (enc (cat t l sk b) kas)
	  (enc (cat t l sk a) kbs))))
   (uniq-orig sk)))

(herald "ALternate Needham-Schroeder Public-Key Protocol Variants")

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 b (pubk a)))
     (send (enc n2 (pubk b))))
    (facts (rel1 n1 n2)
	   (rel2 n1 n2)))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 b (pubk a)))
     (recv (enc n2 (pubk b)))))

  (defrule rebind-x 			; This rule tests rebinding in the conclusion of a rule.
    (forall
     ((x y text))
     (implies
      (fact rel1 x y)
      (exists ((x name)) (fact rel2 x y)))))

  (comment "Needham-Schroeder with no role origination assumptions"))

;;; The initiator point-of-view
(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Initiator point-of-view"))

(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (facts (rel n1 n1))
  (comment "Initiator point-of-view"))

(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b))
  (uniq-orig n1)
  (comment "Initiator point-of-view"))

(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (deflistener n1)
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Initiator point-of-view"))

;;; Double initiator point-of-view
(defskeleton ns
  (vars (a b name) (n1 n1-0 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (defstrand init 3 (a a) (b b) (n1 n1-0))
  (non-orig (privk b) (privk a))
  (uniq-orig n1 n1-0)
  (comment "Double initiator point-of-view"))

;;; Double initiator point-of-view, same nonce
(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Double initiator point-of-view, same nonce"))

;;; The responder point-of-view
(defskeleton ns
  (vars (a name) (n2 text))
  (defstrand resp 3 (a a) (n2 n2))
  (non-orig (privk a))
  (uniq-orig n2)
  (comment "Responder point-of-view"))

(defskeleton ns
  (vars (x name) (n1 n2 text) (a b name))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))
  (non-orig (privk a) (privk b))
  (uniq-orig n1)
  (facts (rel2 x n2) (rel1 n1 n2) (rel2 n1 n2))
  (comment "Double initiator point-of-view, same nonce"))
```

---

### `refrences/internet/examples_scm/ns.scm`

*sha256:`436649066c0e` · 37 lines · 1.0 KB · lang:`scheme`*

```scheme
(herald "Needham-Schroeder Public-Key Protocol"
	(comment "This protocol contains a man-in-the-middle"
		 "attack discovered by Gavin Lowe."))

;;; Used to generate output for inclusion in the primer.
;;; Use margin = 60 (-m 60) to generate the output.

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 (pubk a)))
     (send (enc n2 (pubk b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 (pubk a)))
     (recv (enc n2 (pubk b)))))
  (comment "Needham-Schroeder"))

;;; The initiator point-of-view
(defskeleton ns
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Initiator point-of-view"))

;;; The responder point-of-view
(defskeleton ns
  (vars (a name) (n2 text))
  (defstrand resp 3 (a a) (n2 n2))
  (non-orig (privk a))
  (uniq-orig n2)
  (comment "Responder point-of-view"))
```

---

### `refrences/internet/examples_scm/nsl3.scm`

*sha256:`8bc8612a71fd` · 55 lines · 1.5 KB · lang:`scheme`*

```scheme
(herald "Three Party Needham-Schroeder-Lowe Protocol")

(defprotocol nsl3 basic
  (defrole init (vars (a b c name) (na0 na1 nb0 nb1 nc0 nc1 text))
    (trace
     (send (enc na0 a c (enc na1 a b (pubk c)) (pubk b)))
     (recv (enc na1 nc1 c b
		(enc na0 nb0 b c (pubk a))
		(enc nb1 nc0 c a (pubk b))
		(pubk a)))
     (send (enc nb0
		(enc nb1 nc0 c a (pubk b))
		(enc nc1 (pubk c))
		(pubk b))))
    (uniq-orig na0 na1))
  (defrole mid (vars (a b c name) (na0 na1 nb0 nb1 nc0 nc1 text))
    (trace
     (recv (enc na0 a c (enc na1 a b (pubk c)) (pubk b)))
     (send (enc nb1 b a
		(enc na1 a b (pubk c))
		(enc na0 nb0 b c (pubk a))
		(pubk c)))
     (recv (enc nb0
		(enc nb1 nc0 c a (pubk b))
		(enc nc1 (pubk c))
		(pubk b)))
     (send (enc nc0 (enc nc1 (pubk c)) (pubk c))))
    (uniq-orig nb0 nb1))
  (defrole resp (vars (a b c name) (na0 na1 nb0 nb1 nc0 nc1 text))
    (trace
     (recv (enc nb1 b a
		(enc na1 a b (pubk c))
		(enc na0 nb0 b c (pubk a))
		(pubk c)))
     (send (enc na1 nc1 c b
		(enc na0 nb0 b c (pubk a))
		(enc nb1 nc0 c a (pubk b))
		(pubk a)))
     (recv (enc nc0 (enc nc1 (pubk c)) (pubk c))))
    (uniq-orig nc0 nc1)))

(defskeleton nsl3
  (vars (a b c name))
  (defstrand init 3 (a a) (b b) (c c))
  (non-orig (privk a) (privk b) (privk c)))

(defskeleton nsl3
  (vars (a b c name))
  (defstrand mid 4 (a a) (b b) (c c))
  (non-orig (privk a) (privk b) (privk c)))

(defskeleton nsl3
  (vars (a b c name))
  (defstrand resp 3 (a a) (b b) (c c))
  (non-orig (privk a) (privk b) (privk c)))
```

---

### `refrences/internet/examples_scm/nslsk.scm`

*sha256:`139b149a6a68` · 51 lines · 1.3 KB · lang:`scheme`*

```scheme
(herald "Needham-Schroeder-Lowe Protocol with symmetric encryption")

(defprotocol nslsk basic
  (defrole init (vars (a b name) (n text) (k skey) (t text))
    (trace
     (send (enc n a (pubk b)))
     (recv (enc n k b (pubk a)))
     (send (enc t k))))
  (defrole resp (vars (b a name) (n text) (k skey) (t text))
    (trace
     (recv (enc n a (pubk b)))
     (send (enc n k b (pubk a)))
     (recv (enc t k)))))

(defskeleton nslsk
  (vars (a name) (k skey))
  (defstrand resp 3 (a a) (k k))
  (non-orig (privk a))
  (uniq-orig k))

(defskeleton nslsk
  (vars (b name) (n text))
  (defstrand init 3 (b b) (n n))
  (non-orig (privk b))
  (uniq-orig n))

;; Use a tag as a term.

(defprotocol nslsk-tag-term basic
  (defrole init (vars (a b name) (n text) (k skey))
    (trace
     (send (enc n a (pubk b)))
     (recv (enc n k b (pubk a)))
     (send (enc "t" k))))
  (defrole resp (vars (b a name) (n text) (k skey))
    (trace
     (recv (enc n a (pubk b)))
     (send (enc n k b (pubk a)))
     (recv (enc "t" k)))))

(defskeleton nslsk-tag-term
  (vars (a name) (k skey))
  (defstrand resp 3 (a a) (k k))
  (non-orig (privk a))
  (uniq-orig k))

(defskeleton nslsk-tag-term
  (vars (b name) (n text))
  (defstrand init 3 (b b) (n n))
  (non-orig (privk b))
  (uniq-orig n))
```

---

### `refrences/internet/examples_scm/open-closed-multiloc.scm`

*sha256:`06aac6425c95` · 166 lines · 4.5 KB · lang:`scheme`*

```scheme
(herald open-closed
	;; (try-old-strands)
	;; 	(check-nonces)
	;; 	(reverse-nodes)
	(bound 44))

(defmacro (dev-key-state d o k)
  (cat "st-k" d o k))

(defmacro (opened o)
  (cat o o))

(defmacro (closed o) o)

(defmacro (dev-state-opened d o)
  (cat "st" d (opened o)))

(defmacro (dev-state-closed d o)
  (cat "st" d (closed o)))

(defmacro (dev-state-any d o any)
  (cat "st" d any))

(defprotocol open-closed basic
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))
    (trace
     (recv start-ch (cat "power-up" d o k))
     (load lk old)
     (load ls old1)
     (stor ls (dev-state-closed d o))
     (stor lk (dev-key-state d o k))
     (send (enc "up" k)))
    (auth start-ch))

  (defrole owner-power-dev
    (vars (k skey) (d o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" d o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "open" d o n k))
     (recv n)))

  (defrole owner-close
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "close" d o n k))
     (recv n)))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "open" d o n k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-opened d o))
     (send n)))

  (defrole dev-close
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "close" d o n k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-closed d o))
     (send n)))

  (defrole dev-pass
    (vars (k skey) (n text) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "may I pass" k))
     (load ls (dev-state-opened d o))
     (send (enc "you may pass" n k)))
    (uniq-orig n))

  (defrole user-pass
    (vars (k skey) (n text) (d o name) (l locn))
    (trace
     (send (enc "may I pass" k))
     (recv (enc "you may pass" k))))

  (defrule gen-state-close
    (forall ((z strd) (d o name) (k skey))
	    (implies
	     (and (p "dev-close" z 1)
		  (p "dev-close" "d" z d)
		  (p "dev-close" "o" z o)
		  (p "dev-close" "k" z k)
		  (p "dev-close" "any" z (opened o)))
	     (gen-st (dev-state-opened d o)))))

  (defrule gen-state-pass
    (forall ((z strd) (d o name) (k skey))
	    (implies
	     (and (p "dev-pass" z 1)
		  (p "dev-pass" "d" z d)
		  (p "dev-pass" "o" z o)
		  (p "dev-pass" "k" z k))
	     (gen-st (dev-state-opened d o)))))

   (defrule power-deliver-once
     (forall
      ((z1 z2 strd) (k skey))
      (implies
       (and (p "dev-up" z1 2)
 	   (p "dev-up" z2 2)
 	   (p "dev-up" "k" z1 k)
 	   (p "dev-up" "k" z2 k))
       (= z1 z2))))
  )

(defskeleton open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (deflistener k)
  (uniq-orig k))

(defskeleton open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  ;; (defstrand owner-power-dev 2 (k k))
  (defstrand dev-pass 4 (k k))
  ;; (uniq-orig k)
  )

(defskeleton open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (defstrand dev-pass 4 (k k))
  (uniq-orig k))

(comment
 (defskeleton open-closed
   (vars (any old old1 mesg) (n n-0 text) (d o name) (k k-0 skey)
	 (start-ch chan) (ls lk lk-0 ls-0 locn))
   (defstrand owner-power-dev 2 (d d) (o o) (k k) (start-ch start-ch))
   (defstrand dev-pass 4 (n n) (d d) (o o) (k k) (lk lk ;-0
						     ) (ls ls))
   (defstrand user-pass 1 (k k))
   (defstrand dev-open 4 (any any) (n n-0) (d d) (o o) (k k-0) (lk lk)
     (ls ls))
   (defstrand dev-up 6 (old old) (old1 old1) (d d) (o o) (k k)
     (start-ch start-ch) (lk lk-0) (ls ls-0))
   (precedes ((0 0) (4 0)) ((2 0) (1 1)) ((3 3) (1 2)) ((4 2) (1 0))
	     ((4 5) (0 1)))
   (uniq-orig n k))

 (defskeleton open-closed
   (vars (any old old1 mesg) (n n-0 text) (d o name) (k k-0 skey)
	 (start-ch chan) (ls lk ls-0 locn))
   (defstrand owner-power-dev 2 (d d) (o o) (k k) (start-ch start-ch))
   (defstrand dev-pass 4 (n n) (d d) (o o) (k k) (lk lk) (ls ls))
   (defstrand user-pass 1 (k k))
   (defstrand dev-open 4 (any any) (n n-0) (d d) (o o) (k k-0) (lk lk)
     (ls ls))
   (defstrand dev-up 6 (old old) (old1 old1) (d d) (o o) (k k)
     (start-ch start-ch) (lk lk) (ls ls	; -0
				     ))
   (precedes ((0 0) (4 0)) ((2 0) (1 1)) ((3 3) (1 2)) ((4 2) (1 0))
	     ((4 5) (0 1)))
   (uniq-orig n k)))
```

---

### `refrences/internet/examples_scm/open-closed-tag.scm`

*sha256:`077b13ff8584` · 149 lines · 3.8 KB · lang:`scheme`*

```scheme
(herald open-closed
	;; (try-old-strands)
	;; 	(check-nonces)
	;; 	(reverse-nodes)
	(bound 44))

(defmacro (dev-key-state d o k)
  (cat "st-k" d o k))

(defmacro (opened o)
  "opened")

(defmacro (closed o) "closed")

(defmacro (dev-state-opened d o)
  (cat "st" d (opened o)))

(defmacro (dev-state-closed d o)
  (cat "st" d (closed o)))

(defmacro (dev-state-any d o any)
  (cat "st" d any))

(defprotocol open-closed basic
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))
    (trace
     (recv start-ch (cat "power-up" d o k))
     (load lk old)
     (stor lk (dev-key-state d o k))
     (load ls old1)
     (stor ls (dev-state-closed d o))
     (send (enc "up" k)))
    (auth start-ch))

  (defrole owner-power-dev
    (vars (k skey) (d o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" d o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "open" d o n k))
     (recv n)))

  (defrole owner-close
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "close" d o n k))
     (recv n)))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "open" d o n k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-opened d o))
     (send n)))

  (defrole dev-close
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "close" d o n k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-closed d o))
     (send n)))

  (defrole dev-pass
    (vars (k skey) (n text) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "may I pass" k))
     (load ls (dev-state-opened d o))
     (send (enc "you may pass" n k)))
    (uniq-orig n))

  (defrole user-pass
    (vars (k skey) (n text) (d o name) (l locn))
    (trace
     (send (enc "may I pass" k))
     (recv (enc "you may pass" k))))

  (defrule gen-state-close
    (forall ((z strd) (d o name) (k skey))
	    (implies
	     (and (p "dev-close" z 1)
		  (p "dev-close" "d" z d)
		  (p "dev-close" "o" z o)
		  (p "dev-close" "k" z k)
		  (p "dev-close" "any" z (opened o)))
	     (gen-st (dev-state-opened d o)))))

  (defrule gen-state-pass
    (forall ((z strd) (d o name) (k skey))
	    (implies
	     (and (p "dev-pass" z 1)
		  (p "dev-pass" "d" z d)
		  (p "dev-pass" "o" z o)
		  (p "dev-pass" "k" z k))
	     (gen-st (dev-state-opened d o)))))

   (defrule power-deliver-once
     (forall
      ((z1 z2 strd) (k skey))
      (implies
       (and (p "dev-up" z1 2)
 	   (p "dev-up" z2 2)
 	   (p "dev-up" "k" z1 k)
 	   (p "dev-up" "k" z2 k))
       (= z1 z2))))
  )

(defskeleton open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (deflistener k)
  (uniq-orig k))

(defskeleton open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  ;; (defstrand owner-power-dev 2 (k k))
  (defstrand dev-pass 4 (k k))
  ;; (uniq-orig k)
  )

(defskeleton open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (defstrand dev-pass 4 (k k))
  (uniq-orig k))

(defskeleton open-closed
  (vars (old old1 any mesg) (n n-0 text) (d o name) (k k-0 skey)
    (start-ch chan) (ls lk ls-0 lk-0 locn))
  (defstrand owner-power-dev 2 (d d) (o o) (k k) (start-ch start-ch))
  (defstrand dev-pass 4 (n n) (d d) (o o) (k k) (lk lk) (ls ls))
  (defstrand dev-up 6 (old old) (old1 old1) (d d) (o o) (k k)
    (start-ch start-ch) (lk lk) (ls ls-0))
  (defstrand user-pass 1 (k k))
  (defstrand dev-open 4 (any any) (n n-0) (d d) (o o) (k k-0) (lk lk-0)
    (ls ls))
  (precedes ((0 0) (2 0)) ((2 2) (1 0)) ((2 5) (0 1)) ((3 0) (1 1))
    ((4 3) (1 2)))
  (uniq-orig n k))
```

---

### `refrences/internet/examples_scm/open-closed.scm`

*sha256:`ffb860449ac3` · 180 lines · 4.8 KB · lang:`scheme`*

```scheme
(herald open-closed
	;; (try-old-strands)
	;; 	(check-nonces)
	;; 	(reverse-nodes)
	(bound 44))

(defmacro (dev-key-state d o k)
  (cat "st-k" d o k))

(defmacro (opened o)
  (cat o o))

(defmacro (closed o) o)

(defmacro (dev-state-opened d o)
  (cat "st" d (opened o)))

(defmacro (dev-state-closed d o)
  (cat "st" d (closed o)))

(defmacro (dev-state-any d o any)
  (cat "st" d any))

(defprotocol open-closed basic
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))
    (trace
     (recv start-ch (cat "power-up" d o k))
     (load lk old)
     (stor lk (dev-key-state d o k))
     (load ls old1)
     (stor ls (dev-state-closed d o))
     (send (enc "up" k)))
    (auth start-ch))

  (defrole owner-power-dev
    (vars (k skey) (d o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" d o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "open" d o n k))
     (recv n)))

  (defrole owner-close
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "close" d o n k))
     (recv n)))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "open" d o n k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-opened d o))
     (send n)))

  (defrole dev-close
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "close" d o n k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-closed d o))
     (send n)))

  (defrole dev-pass
    (vars (k skey) (n text) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (recv (enc "may I pass" k))
     (load ls (dev-state-opened d o))
     (send (enc "you may pass" n k)))
    (uniq-orig n))

  (defrole user-pass
    (vars (k skey) (n text) (d o name) (l locn))
    (trace
     (send (enc "may I pass" k))
     (recv (enc "you may pass" k))))

  (defrule gen-state-close
    (forall ((z strd) (d o name) (k skey))
	    (implies
	     (and (p "dev-close" z 1)
		  (p "dev-close" "d" z d)
		  (p "dev-close" "o" z o)
		  (p "dev-close" "k" z k)
		  (p "dev-close" "any" z (opened o)))
	     (gen-st (dev-state-opened d o)))))

  (defrule gen-state-pass
    (forall ((z strd) (d o name) (k skey))
	    (implies
	     (and (p "dev-pass" z 1)
		  (p "dev-pass" "d" z d)
		  (p "dev-pass" "o" z o)
		  (p "dev-pass" "k" z k))
	     (gen-st (dev-state-opened d o)))))

   (defrule power-deliver-once
     (forall
      ((z1 z2 strd) (k skey))
      (implies
       (and (p "dev-up" z1 2)
 	   (p "dev-up" z2 2)
 	   (p "dev-up" "k" z1 k)
 	   (p "dev-up" "k" z2 k))
       (= z2 z1))))

   (defrule same-locn
     (forall ((z1 z2 strd) (i1 i2 indx))
  	     (implies
  	      (same-locn z1 i1 z2 i2)
  	      (fact ha z1 i1 z2 i2)))
     (comment this is a rule comment))

   (defrule leadsto-la
     (forall ((z1 z2 strd) (i1 i2 indx))
  	     (implies
  	      (leads-to z1 i1 z2 i2)
  	      (fact la z1 i1 z2 i2)))
     (comment this is a rule comment))
   )

(defskeleton open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (deflistener k)
  (uniq-orig k))

(defskeleton open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  ;; (defstrand owner-power-dev 2 (k k))
  (defstrand dev-pass 4 (k k))
  ;; (uniq-orig k)
  )

(defskeleton open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (defstrand dev-pass 4 (k k))
  (uniq-orig k))

(comment
 (defskeleton open-closed
   (vars (any old old1 mesg) (n n-0 text) (d o name) (k k-0 skey)
	 (start-ch chan) (ls lk lk-0 ls-0 locn))
   (defstrand owner-power-dev 2 (d d) (o o) (k k) (start-ch start-ch))
   (defstrand dev-pass 4 (n n) (d d) (o o) (k k) (lk lk ;-0
						     ) (ls ls))
   (defstrand user-pass 1 (k k))
   (defstrand dev-open 4 (any any) (n n-0) (d d) (o o) (k k-0) (lk lk)
     (ls ls))
   (defstrand dev-up 6 (old old) (old1 old1) (d d) (o o) (k k)
     (start-ch start-ch) (lk lk-0) (ls ls-0))
   (precedes ((0 0) (4 0)) ((2 0) (1 1)) ((3 3) (1 2)) ((4 2) (1 0))
	     ((4 5) (0 1)))
   (uniq-orig n k))

 (defskeleton open-closed
   (vars (any old old1 mesg) (n n-0 text) (d o name) (k k-0 skey)
	 (start-ch chan) (ls lk ls-0 locn))
   (defstrand owner-power-dev 2 (d d) (o o) (k k) (start-ch start-ch))
   (defstrand dev-pass 4 (n n) (d d) (o o) (k k) (lk lk) (ls ls))
   (defstrand user-pass 1 (k k))
   (defstrand dev-open 4 (any any) (n n-0) (d d) (o o) (k k-0) (lk lk)
     (ls ls))
   (defstrand dev-up 6 (old old) (old1 old1) (d d) (o o) (k k)
     (start-ch start-ch) (lk lk) (ls ls	; -0
				     ))
   (precedes ((0 0) (4 0)) ((2 0) (1 1)) ((3 3) (1 2)) ((4 2) (1 0))
	     ((4 5) (0 1)))
   (uniq-orig n k)))
```

---

### `refrences/internet/examples_scm/or.scm`

*sha256:`8bdc4e82cc5e` · 27 lines · 0.9 KB · lang:`scheme`*

```scheme
(herald "Otway-Rees Protocol"
	(comment "Standard version using variables of sort mesg"))

(defprotocol or basic
  (defrole init (vars (a b s name) (na text) (k skey) (m text))
    (trace
     (send (cat m a b (enc na m a b (ltk a s))))
     (recv (cat m (enc na k (ltk a s))))))
  (defrole resp
    (vars (a b s name) (nb text) (k skey) (m text) (x y mesg))
    (trace
     (recv (cat m a b x))
     (send (cat m a b x (enc nb m a b (ltk b s))))
     (recv (cat m y (enc nb k (ltk b s))))
     (send y)))
  (defrole serv (vars (a b s name) (na nb text) (k skey) (m text))
    (trace
     (recv (cat m a b (enc na m a b (ltk a s))
		(enc nb m a b (ltk b s))))
     (send (cat m (enc na k (ltk a s)) (enc nb k (ltk b s)))))
    (uniq-orig k)))

(defskeleton or
  (vars (nb text) (s a b name))
  (defstrand resp 4 (a a) (b b) (s s) (nb nb))
  (non-orig (ltk a s) (ltk b s))
  (uniq-orig nb))
```

---

### `refrences/internet/examples_scm/ordered.scm`

*sha256:`c0c9185c45bf` · 39 lines · 0.7 KB · lang:`scheme`*

```scheme
(herald ordered)

(defprotocol ordered basic

  (defrole dec
    (vars (t text) (k akey))
    (trace (recv (enc t k)) (send t)))

;;     (defrule neq
;;       (forall ((x mesg))
;;   	    (implies (fact neq x x) (false))))

  (defrule order
    (forall ((y z strd))
	    (implies
	     (and (p "dec" y 2)
		  (p "dec" z 2))
	     (or (prec y 1 z 0)
		 (prec z 1 y 0)
		 (= y z))))))

(defskeleton ordered
  (vars (a b text))
  (defstrand dec 2 (t a))
  (defstrand dec 2 (t b))
  (facts (neq a b)))

(defskeleton ordered
  (vars (b text) (k akey))
  (defstrand dec 2 (t b) (k k))
  (facts (neq b b))
  (rule order)
  (traces ((recv (enc b k)) (send b)))
  (label 3)
  (parent 0)
  (unrealized)
  (shape)
  (maps ((0 0) ((a b) (b b) (k k) (k-0 k))))
  (origs))
```

---

### `refrences/internet/examples_scm/orderedvar.scm`

*sha256:`aa7cdc6a6107` · 39 lines · 0.7 KB · lang:`scheme`*

```scheme
(herald ordered)

(defprotocol ordered basic

  (defrole dec
    (vars (t text) (k akey))
    (trace (recv (enc t k)) (send t)))

;;     (defrule neq
;;       (forall ((x mesg))
;;   	    (implies (fact neq x x) (false))))

  (defrule order
    (forall ((y z strd))
	    (implies
	     (and (strand dec y 2)
		  (strand dec z 2))
	     (or (prec y 1 z 0)
		 (prec z 1 y 0)
		 (= y z))))))

(defskeleton ordered
  (vars (a b text))
  (defstrand dec 2 (t a))
  (defstrand dec 2 (t b))
  (facts (neq a b)))

(defskeleton ordered
  (vars (b text) (k akey))
  (defstrand dec 2 (t b) (k k))
  (facts (neq b b))
  (rule order)
  (traces ((recv (enc b k)) (send b)))
  (label 3)
  (parent 0)
  (unrealized)
  (shape)
  (maps ((0 0) ((a b) (b b) (k k) (k-0 k))))
  (origs))
```

---

### `refrences/internet/examples_scm/pca.scm`

*sha256:`298053fef263` · 36 lines · 1.1 KB · lang:`scheme`*

```scheme
(herald "Privacy Certificate Authority" (bound 15)
  (comment "Generation of an Attestation Identity Certificate"))

;;; PCA generation of AIC, simplified

;;; ki = identity key
;;; a = identity label
;;; t = TPM type/platform
;;; ke = endorsement key
;;; kp = PCA key
;;; km = manufacturer key
;;; (enc (cat ki a t) (invk kp)) is the signed AIC

(defprotocol pca basic
  (defrole tpm (vars (ke ki km kp akey) (t a text))
    (trace
     (send (cat (enc ki a (invk ki)) (enc t ke (invk km))))
     (recv (enc (enc ki a t (invk kp)) ke))
     (send (enc ki a t (invk kp))))
    (non-orig (invk ke) (invk ki) (invk km) (invk kp))
    (uniq-orig ki))
  (defrole pca (vars (ke ki km kp akey) (t a text))
    (trace
     (recv (cat (enc ki a (invk ki)) (enc t ke (invk km))))
     (send (enc (enc ki a t (invk kp)) ke)))
    (non-orig (invk ke) (invk ki) (invk km) (invk kp)))
  (defrole appr (vars (ki kp akey) (t a text))
    (trace
     (recv (enc ki a t (invk kp))))
    (non-orig (invk ki) (invk kp))))

;;; normal run

(defskeleton pca (vars (ki kp akey))
  (defstrand appr 1 (ki ki) (kp kp))
  (non-orig (invk ki) (invk kp)))
```

---

### `refrences/internet/examples_scm/pen-non-orig-test.scm`

*sha256:`43ea68bd790c` · 29 lines · 0.8 KB · lang:`scheme`*

```scheme
;; This is to test the pen-non-orig declaration.
;; The password, pwd, should not be known to the
;; penetrator at the outset.  Thus, even over an
;; unencrypted channel, the server should infer
;; a good client.  However, the password is
;; learned in the process, hence the skeleton
;; with a listener will also be realized.

(herald "pen-non-orig test")

(defprotocol pennonorigtest basic
  (defrole client
    (vars (userid name) (pwd text))
    (trace
     (send (cat userid pwd))))
  (defrole server
    (vars (userid name) (pwd text))
    (trace
     (recv (cat userid pwd)))
    (pen-non-orig pwd)))

(defskeleton pennonorigtest
  (vars (pwd text))
  (defstrand server 1 (pwd pwd)))

(defskeleton pennonorigtest
  (vars (pwd text))
  (defstrand server 1 (pwd pwd))
  (deflistener pwd))
```

---

### `refrences/internet/examples_scm/pfs-via-pubkey.scm`

*sha256:`49b7b5024629` · 35 lines · 1.2 KB · lang:`scheme`*

```scheme
(herald pfs-via-pubkey)

(defprotocol pfs-easy basic
  (defrole init
    (vars (new-akey akey) (a b name) (n data) (s text))
    (trace
     (send (enc a b new-akey n (privk "sgn" a)))
     (recv (enc (enc a n s (privk "sgn" b)) new-akey))
     (send (privk "sgn" a))))		; compromise signing key subsequently

  (defrole resp
    (vars (new-akey akey) (a b name) (n data) (s text))
    (trace
     (recv (enc a b new-akey n (privk "sgn" a)))
     (send (enc (enc a n s (privk "sgn" b)) new-akey)))))

(defskeleton pfs-easy
  (vars (new-akey akey) (a b name) (n data) (s text))
  (defstrand init 3 (a a) (b b) (new-akey new-akey) (n n))
  (non-orig (privk "sgn" b) (invk new-akey))
  (uniq-orig (privk "sgn" a) new-akey n))

(defskeleton pfs-easy
  (vars (new-akey akey) (a b name) (n data) (s text))
  (defstrand resp 2 (a a) (new-akey new-akey))
  (non-orig (privk "sgn" a)))

(defskeleton pfs-easy
  (vars (s text) (n data) (a b name) (new-akey akey))
  (defstrand resp 2 (s s) (n n) (a a) (b b) (new-akey new-akey))
  (defstrand init 3 (n n) (a a) (b b) (new-akey new-akey))
  (deflistener s)
  (precedes ((1 0) (0 0)))
  (non-orig (invk new-akey))
  (uniq-orig (privk "sgn" a) s))
```

---

### `refrences/internet/examples_scm/pkinit.scm`

*sha256:`424045fb7b6f` · 22 lines · 0.7 KB · lang:`scheme`*

```scheme
(herald "Kerberos PK init")

(defprotocol pkinit basic
  (defrole client
    (vars (c t as name) (n2 n1 text) (tc tk tgt data) (k ak skey))
    (trace (send (cat (enc tc n2 (privk c)) c t n1))
      (recv
        (cat (enc (enc k n2 (privk as)) (pubk c)) c tgt
          (enc ak n1 tk t k))))
    (uniq-orig n1 n2))
  (defrole auth
    (vars (c t as name) (n2 n1 text) (tc tk tgt data) (k ak skey))
    (trace (recv (cat (enc tc n2 (privk c)) c t n1))
      (send
        (cat (enc (enc k n2 (privk as)) (pubk c)) c tgt
          (enc ak n1 tk t k))))
    (uniq-orig k ak)))

(defskeleton pkinit
  (vars (c as name))
  (defstrand client 2 (c c) (as as))
  (non-orig (privk c) (privk as)))
```

---

### `refrences/internet/examples_scm/preprocess.scm`

*sha256:`85f407700b4e` · 27 lines · 0.8 KB · lang:`scheme`*

```scheme
(herald "Pre-processing test example: modified NS with two responders")

(defprotocol ns basic
  (defrole init
    (vars (a b name) (n1 n2 n3 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (enc n1 n2 n3 (pubk a)))
     (send (enc n2 n3 (pubk b))))
	(uniq-orig n1))
  (defrole resp
    (vars (a b name) (n1 n2 n3 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 n3 (pubk a)))
     (recv (enc n2 n3 (pubk b))))
	(uniq-orig n2 n3))
  (comment "modified Needham-Schroeder with role origination assumptions"))

;;; The initiator and two entangled responders POV
(defskeleton ns
  (vars (a b name) (n1 n2 n3 n2p n3p text))
  (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2) (n3 n3))
  (defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2) (n3 n3p))
  (defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2p) (n3 n3))
  (non-orig (privk b) (privk a))
)
```

---

### `refrences/internet/examples_scm/print.scm`

*sha256:`5461454e4b17` · 13 lines · 0.4 KB · lang:`scheme`*

```scheme
(herald "Print Test"
  (comment "See if read forms look like printed ones"))

(defprotocol print-test basic
  (defrole role
    (vars (a b akey) (f g skey) (x y data))
    (trace (recv (cat a b f g x y)))
    (comment "Check the order in which variables are printed")))

(defskeleton print-test
  (vars (a b akey) (f g skey) (x y data))
  (defstrand role 1 (a a) (b b) (f f) (g g) (x x) (y y))
  (comment "Check the order in which variables are printed"))
```

---

### `refrences/internet/examples_scm/prottrans.scm`

*sha256:`506c69f72936` · 107 lines · 2.8 KB · lang:`scheme`*

```scheme
(herald "Protocol Transformations With Rules")

;; Basic Needham-Schroeder using asymmetric keys

(defprotocol ns basic
  (defrole init
    (vars (a b akey) (na nb text))
    (trace
     (send (enc na a b))
     (recv (enc na nb a))
     (send (enc nb b))))
  (defrole resp
    (vars (b a akey) (nb na text))
    (trace
     (recv (enc na a b))
     (send (enc na nb a))
     (recv (enc nb b))))
  (comment "Needham-Schroeder without rules"))

;;; The initiator point-of-view
(defskeleton ns
  (vars (a b akey) (na text))
  (defstrand init 3 (a a) (b b) (na na))
  (non-orig (invk a) (invk b))
  (uniq-orig na)
  (comment "Initiator point-of-view"))

;;; The responder point-of-view
(defskeleton ns
  (vars (a akey) (nb text))
  (defstrand resp 3 (a a) (nb nb))
  (non-orig (invk a))
  (uniq-orig nb)
  (comment "Responder point-of-view"))

;;; Unilateral protocol
(defprotocol unilateral basic
  (defrole init
     (vars (n text) (k akey))
     (trace
      (send (enc n k))
      (recv n)))
  (defrole resp
     (vars (n text) (k akey))
     (trace
      (recv (enc n k))
      (send n))))

(defskeleton unilateral
  (vars (k akey) (n text))
  (defstrand init 2 (n n) (k k))
  (non-orig (invk k))
  (uniq-orig n)
  (comment "The shape analysis sentence for this problem:"
    (defgoal unilateral
      (forall ((n text) (k akey) (z strd))
        (implies
          (and (p "init" z 2) (p "init" "n" z n) (p "init" "k" z k)
            (non (invk k)) (uniq-at n z 0))
          (exists ((z-0 strd))
            (and (p "resp" z-0 2) (p "resp" "n" z-0 n)
              (p "resp" "k" z-0 k) (prec z 0 z-0 0)
              (prec z-0 1 z 1))))))))

(defprotocol ns-with-rule basic
  (defrole init
    (vars (a b akey) (na nb text))
    (trace
     (send (enc na a b))
     (recv (enc na nb a))
     (send (enc nb b))))
  (defrole resp
    (vars (b a akey) (nb na text))
    (trace
     (recv (enc na a b))
     (send (enc na nb a))
     (recv (enc nb b))))
  (defrule unilateral
    (forall ((r strd) (a akey) (nb text))
	    (implies
	     (and (p "resp" r 3)
		  (p "resp" "a" r a)
		  (p "resp" "nb" r nb)
		  (non (invk a))
		  (uniq nb))
	     (exists ((i strd))
		     (and (p "init" i 3)
			  (p "init" "a" i a)
			  (p "init" "nb" i nb)
			  (prec r 1 i 1)
			  (prec i 2 r 2)))))
    (comment "Unilateral sas under the predicate mapping:")
    (comment (p "init" 2) "->" (p "resp" 3) "and")
    (comment (p "init" "n") "->" (p "resp" "nb") "and")
    (comment (p "init" "k") "->" (p "resp" "a") "and")
    (comment (p "resp" 2) "->" (p "init" 3) "and")
    (comment (p "resp" "n") "->" (p "init" "nb"))
    (comment (p "resp" "k") "->" (p "init" "a")))
  (comment "Needham-Schroeder with rule"))

;;; The responder point-of-view
(defskeleton ns-with-rule
  (vars (a akey) (nb text))
  (defstrand resp 3 (a a) (nb nb))
  (non-orig (invk a))
  (uniq-orig nb)
  (comment "Responder point-of-view"))
```

---

### `refrences/internet/examples_scm/pruning1.scm`

*sha256:`6c32b763e3f2` · 42 lines · 1.4 KB · lang:`scheme`*

```scheme
; pruning1
;   Demonstrates a flaw in CPSA due to overly aggressive pruning.
; Specifically, the shape requires two instances of trans, one
; with k = pubk b and the other with k = privk b.  CPSA would
; form one of these instances and then refuse to augment with another
; because the new one would prune.  This pruning was overly aggressive
; because leaving k unbound gives the new strand greater freedom.
;   This flaw was discovered previously in targetterms6, but
; this example illustrates that the flaw does not depend on variables
; of sort mesg; here it is done with a variable of sort akey.

(defprotocol prune basic
  (defrole init (vars (a b name) (n text))
    (trace
	(send (enc n (pubk a)))
      (recv (enc n (pubk b) (pubk a)))
      (recv (enc n (privk b) (pubk a)))
	)
    (uniq-orig n)
    (non-orig (privk a))
  )
  (defrole trans (vars (a name) (n text) (k akey))
     (trace
        (recv (enc n (pubk a)))
	(recv k )
        (send (enc n k (pubk a)))
     )
  )
  (comment "Shows a failure with generalization"
	   "Run this with a step count of 4"))

(defskeleton prune
  (vars (a name) (n text) (k akey))
  (defstrand init 3))

(defskeleton prune
  (vars (n text) (a b name))
  (defstrand init 3 (n n) (a a) (b b))
  (defstrand trans 3 (n n) (a a) (k (pubk b)))
  (defstrand trans 3 (n n) (a a) (k (privk b)))
  (precedes ((0 0) (1 0)) ((0 0) (2 0)) ((1 2) (0 1)) ((2 2) (0 2)))
)
```

---

### `refrences/internet/examples_scm/puzzle_example.scm`

*sha256:`9786d9060676` · 73 lines · 2.1 KB · lang:`scheme`*

```scheme
(herald puzzle_example)

;; Note that (ltk a b) \not= (ltk b a).  If we have a shared key with
;; this symmetry, then we need a lttle more structure in the middle
;; msg.

(defprotocol puzzle basic
  (defrole init
    (vars (a b name) (na payload text) (s skey))
    (trace
     (send na)
     (recv (enc na s (ltk a b)))
     (send (enc payload s))))

  (defrole resp
    (vars (a b name) (na payload text) (s skey))
    (trace
     (recv na)
     (send (enc na s (ltk a b)))
     (recv (enc payload s)))))

(defskeleton puzzle
  (vars (a b name) (na payload text) (s skey))
  (defstrand init 3 (a a) (b b) (na na) (payload payload))
  (uniq-orig na payload)
  (non-orig (ltk a b)))

(defskeleton puzzle
  (vars (a b name) (na payload text) (s skey))
  (defstrand init 3 (a a) (b b) (na na) (payload payload))
  (deflistener payload)
  (uniq-orig na payload)
  (non-orig (ltk a b)))

(defskeleton puzzle
  (vars (na payload text) (a b name) (s skey))
  (defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))
  (defstrand resp 2 (na na) (a a) (b b) (s s))
  (deflistener s)
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (non-orig (ltk a b))
  (uniq-orig s na payload))

(defskeleton puzzle
  (vars (na payload text) (a b name) (s skey))
  (defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))
  (defstrand resp 2 (na na) (a a) (b b) (s s))
  (deflistener payload)
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (non-orig (ltk a b))
  (uniq-orig s na payload))

(defskeleton puzzle
  (vars (a b name) (na payload text) (s skey))
  (defstrand resp 3 (a a) (b b) (s s) (payload payload))
  (uniq-orig s)
  (non-orig (ltk a b)))

(defskeleton puzzle
  (vars (a b name) (na payload text) (s skey))
  (defstrand resp 3 (a a) (b b) (s s) (payload payload))
  (deflistener s)
  (uniq-orig s)
  (non-orig (ltk a b)))

(defskeleton puzzle
  (vars (payload na text) (a b name) (s skey))
  (defstrand resp 3 (na na) (payload payload) (a a) (b b) (s s))
  (defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))
  (deflistener payload)
  (precedes ((0 1) (1 1)) ((1 2) (0 2)))
  (non-orig (ltk a b))
  (uniq-orig s payload))
```

---

### `refrences/internet/examples_scm/reflect.scm`

*sha256:`d28cf4717229` · 32 lines · 0.6 KB · lang:`scheme`*

```scheme
(herald reflect)

;; A simple protocol vulnerable to a reflection attack

(defprotocol reflect basic
  (defrole init
    (vars (a b akey))
    (trace
     (send (enc b (invk a)))
     (recv (enc a (invk b)))))
  (defrole resp
    (vars (a b akey))
    (trace
     (recv (enc b (invk a)))
     (send (enc a (invk b))))))

;; Expect two shapes

(defskeleton reflect
  (vars (a b akey))
  (defstrand resp 1 (a a) (b b))
  (non-orig (invk a) (invk b)))

(defskeleton reflect
  (vars (a b akey))
  (defstrand init 2 (a a) (b b))
  (non-orig (invk a) (invk b)))

(defskeleton reflect
  (vars (a b akey))
  (defstrand resp 1 (a a) (b (invk b)))
  (non-orig (invk a) b))
```

---

### `refrences/internet/examples_scm/renamings.scm`

*sha256:`26877988b9f1` · 30 lines · 0.9 KB · lang:`scheme`*

```scheme
(herald "Blanchet's Simple Example Protocol"
	(comment "There is a flaw in this protocol by design")
	(comment "It also shows how variable renaming works"))

(defprotocol blanchet basic
  (defrole init
    (vars (a b name) (s skey) (d data))
    (trace
     (send (enc (enc s (privk a)) (pubk b)))
     (recv (enc d s))))
  (defrole resp
    (vars (d a name) (b skey) (s data))
    (trace
     (recv (enc (enc b (privk d)) (pubk a)))
     (send (enc s b))))
  (comment "Blanchet's protocol using named asymmetric keys"))

(defskeleton blanchet
  (vars (s d name) (a skey) (b data))
  (defstrand resp 2 (d s) (a d) (b a) (s b))
  (non-orig (privk s) (privk d))
  (uniq-orig a)
  (comment "Analyze from the responder's perspective"))

(defskeleton blanchet
  (vars (s d name) (a skey) (b data))
  (defstrand init 2 (a s) (b d) (s a) (d b))
  (non-orig (privk d))
  (uniq-orig a)
  (comment "Analyze from the initiator's perspective"))
```

---

### `refrences/internet/examples_scm/role_uniq.scm`

*sha256:`44cb41cd7701` · 56 lines · 1.6 KB · lang:`scheme`*

```scheme
(herald "Role Unique Origination")

(defprotocol blanchet basic
  (defrole init
    (vars (a b akey) (s skey) (d data))
    (trace
     (send (enc (enc s (invk a)) b))
     (recv (enc d s)))
    (uniq-orig s))
  (defrole resp
    (vars (a b akey) (s skey) (d data))
    (trace
     (recv (enc (enc s (invk a)) b))
     (send (enc d s))))
  (comment "Blanchet's protocol using unnamed asymmetric keys"))

(defskeleton blanchet
  (vars (a b akey) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (non-orig (invk b))
  (comment "Analyze from the initiator's perspective"))

(defskeleton blanchet
  (vars (a b akey) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (non-orig (invk a) (invk b))
  (comment "Analyze from the responder's perspective"))

(defprotocol blanchet basic
  (defrole init
    (vars (a b akey) (s skey) (d data))
    (trace
     (send (enc (enc s (invk a)) b))
     (recv (enc d s))))
  (defrole resp
    (vars (a b akey) (s skey) (d data))
    (trace
     (recv (enc (enc s (invk a)) b))
     (send (enc d s))))
  (defrule role-uniq
    (forall ((z strd) (s skey))
	    (implies (p "init" "s" z s)
		     (uniq s))))
  (comment "Blanchet's protocol using unnamed asymmetric keys"))

(defskeleton blanchet
  (vars (a b akey) (s skey) (d data))
  (defstrand init 2 (a a) (b b) (s s) (d d))
  (non-orig (invk b))
  (comment "Analyze from the initiator's perspective"))

(defskeleton blanchet
  (vars (a b akey) (s skey) (d data))
  (defstrand resp 2 (a a) (b b) (s s) (d d))
  (non-orig (invk a) (invk b))
  (comment "Analyze from the responder's perspective"))
```

---

### `refrences/internet/examples_scm/rule-node.scm`

*sha256:`d623459ea1e4` · 88 lines · 1.8 KB · lang:`scheme`*

```scheme
(herald rule-node)

(defprotocol rule-order basic
  (defrole init
    (vars (s t text))
    (trace
     (send (cat s t))
     (recv (cat t s))))

  (defrule le-lt
    (forall ((z1 z2 strd)(i1 i2 indx))
    	    (implies
    	     (fact le z1 i1 z2 i2)
    	     (or
    	      (and (= z1 z2) (= i1 i2))
    	      (fact lt z1 i1 z2 i2)))))

  (defrule lt-le
    (forall ((z1 z2 strd)(i1 i2 indx))
    	    (implies
    	     (fact lt z1 i1 z2 i2)
    	     (fact le z1 i1 z2 i2))))

  (defrule prec-lt
    (forall ((z1 z2 strd)(i1 i2 indx))
	    (implies
	     (prec z1 i1 z2 i2)
	     (or
	      (fact lt z1 i1 z2 i2)))))

  (defrule neq-false
    (forall ((s mesg))
	    (implies (fact neq s s)
		     (false))))
  )

(defskeleton rule-order
  (vars (s t s1 t1 text))
  (defstrand init 2 (s s) (t t))
  (defstrand init 2 (s t) (t s))
  ;;  (defstrand init 2 (s s1) (t t1))
  (precedes ((1 0) (0 1))
	    ;; ((2 0) (0 1))
	    )
  (facts (neq s t)
	 ;; (neq s s1)
	 )
  (facts (le 0 (idx 0) 0 (idx 1)))
  )

(defskeleton rule-order
  (vars (s t text))
  (defstrand init 2 (s s) (t t))
  (defstrand init 2 (s t) (t s))
  (precedes ((1 0) (0 1)))
  (facts (le 1 (idx 0) 0 (idx 1)) (le 0 (idx 0) 0 (idx 1))))

(defprotocol rule-order-prec basic
  (defrole init
    (vars (s t text))
    (trace
     (send (cat s t))
     (recv (cat t s))))

  (defrule prec-tell-me
    (forall ((z1 z2 strd) (i1 i2 indx))
	    (implies
	     (prec z1 i1 z2 i2)
	     (fact tell-me z1 i1 z2 i2))))
  )

(defskeleton rule-order-prec
  (vars (s t text))
  (defstrand init 2 (s s) (t t)))

(defskeleton rule-order-prec
  (vars (s t text))
  (defstrand init 2 (s s) (t t))
  (defstrand init 2 (s t) (t s))
  (precedes ((1 0) (0 1)))
  )

(defskeleton rule-order-prec
  (vars (s t text))
  (defstrand init 2 (s s) (t t))
  (defstrand init 2 (s s) (t t))
  (precedes ((1 0) (0 1)))
  (neq (s t)))
```

---

### `refrences/internet/examples_scm/rule-order.scm`

*sha256:`02735c6e55ef` · 21 lines · 0.3 KB · lang:`scheme`*

```scheme
(herald rule-order)

(defprotocol rule-order basic
  (defrole init
    (vars (s t text))
    (trace
     (send (cat s t))))

  (defrule ge
    (forall ((x y text))
	    (implies
	     (fact le x y)
	     (or
	      (= x y)
	      (fact lt x y)))))
  )

(defskeleton rule-order
  (vars (s t text))
  (defstrand init 1 (s s) (t t))
  (facts (le s t)))
```

---

### `refrences/internet/examples_scm/rules.scm`

*sha256:`2761f75fd5bd` · 67 lines · 1.6 KB · lang:`scheme`*

```scheme
(herald "Rules and Facts")

(defprotocol neq-test basic
  (defrole init
    (vars (n1 n2 text) (k skey))
    (trace
     (send (cat n1 (enc n1 n2 k)))
     (recv n2))
    (non-orig k)
    (uniq-orig n1 n2))
  (defrule neq
    (forall ((a mesg))
	    (implies
	     (fact neq a a)
	     (false))))
  (comment "Impose an nequality constraint using facts and rules"))

;;; With no inequality fact,
;;; a shape should be found where n1 = n2.
(defskeleton neq-test
  (vars)
  (defstrand init 2)
  (comment "This skeleton should have a shape"))

;;; With an inequality fact,
;;; no shape should exist.
(defskeleton neq-test
  (vars (n1 n2 text))
  (defstrand init 2 (n1 n1) (n2 n2))
  (facts (neq n1 n2))			;  assert n1 != n2
  (comment "This skeleton should have no shapes"))

;;;

(herald doorsep (comment "Door Simple Example Protocol"))

(defprotocol doorsep basic
  (defrole person
    (vars (d p akey) (k skey) (t text))
    (trace
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t))
    (uniq-orig k))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t))
    (uniq-orig t))
  (defrule trust
    (forall ((z strd) (p d akey))
	    (implies
	     (and (p "person" z 1)
		  (p "person" "p" z p)
		  (p "person" "d" z d)
		  (non (invk p)))
	     (non (invk d))))
    (comment "The trust rule"))
  (comment "Doorsep protocol using unnamed asymmetric keys"))

(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (comment "Analyze from the doors's perspective"))
```

---

### `refrences/internet/examples_scm/scep-tls-dh-broken.scm`

*sha256:`b1818bb80bb3` · 140 lines · 4.7 KB · lang:`scheme`*

```scheme
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

;; SCEP Tokens
(defmacro (Tok X Y data)
  (cat "Token" X (pubk X) Y (pubk Y) data))

(defmacro (SCEP-Token X Y data)
  (cat (Tok X Y data) (enc (hash (Tok X Y data)) (privk Y))))

;; TLS Components
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
      ;; Tr_TLS-C (S acts as Client)
      (send rSp)
      (recv (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))
      (send (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))
      (recv (WFIN dh_eS dh_eW rSp rWp W CA))

      ;; Tr_SCEP-SW
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
      ;; Tr_TLS-S (W acts as Server)
      (recv rSp)
      (send (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))
      (recv (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))
      (send (WFIN dh_eS dh_eW rSp rWp W CA))

      ;; Tr_SCEP-WS
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
        ;; 1. The Client strand runs to full completion (depth 7)
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

        ;; 2. We assume the long-term keys of all involved parties are not compromised
        (non (privk S))
        (non (privk W))
        (non (privk M))
        (non (privk CA))

        ;; 3. The adversary listener strand "eve" attempts to intercept the SCEP Token
        (p "" eve 1)
        (p "" "x" eve (SCEP-Token S M rS))
      )
      ;; 4. If all the above is true, it implies a logical impossibility (false)
      (false))))
  (comment "Confidentiality goal: The adversary cannot learn the SCEP-Token S M rS")


;(defskeleton dh
;  (vars (S W M CA name)
;        (rS rW rSp rWp w text)
;        (dh_eS dh_eW rndx))
;  (defstrandmax client
;    (S S) (W W) (M M) (CA CA) (rS rS) (rW rW) (rSp rSp) (rWp rWp) (w w) (dh_eS dh_eS) (dh_eW dh_eW))
;  (pen-non-orig (privk S) (privk W) (privk CA))
;  (comment "Analyze security from the Client's perspective"))


;(defskeleton dh
;  (vars (S W M CA name)
;        (rS rW rSp rWp w text)
;        (dh_eS dh_eW rndx))
;  (defstrandmax server
;    (S S) (W W) (M M) (CA CA) (rS rS) (rW rW) (rSp rSp) (rWp rWp) (w w) (dh_eS dh_eS) (dh_eW dh_eW))
;  (pen-non-orig (privk S) (privk W) (privk CA))
;  (comment "Analyze security from the Server's perspective"))
```

---

### `refrences/internet/examples_scm/scep-tls-dh-fixed.scm`

*sha256:`f58ff6535265` · 141 lines · 4.8 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sdls-auth-enc-full-payload.scm`

*sha256:`ca74511ed9c2` · 226 lines · 10.5 KB · lang:`scheme`*

```scheme
(herald "SDLSP Authenticated Encryption: full SDLS-EP rekeying sequence")

;; MODELLED
;;   1. OTAR                3.2.3.1   session keys delivered under the master key
;;   2. Key Activation      3.2.3.2   key IDs signalled for activation
;;   3. Rekey SA            3.3.3.3   keys bound to the SA
;;   4. Start SA            3.3.3.1   SA put in service on a channel
;;   5. Key Verification    3.2.3.5   challenge / response under the new key
;;   6. Traffic             355.0-B-2 the new SA protects a frame_data
;;
;; KEYS
;;   assumed_enc_key / assumed_auth_key   the SA already in service.  4.3.1.1
;;     p.4-5 requires every EP command PDU to ride an already-protected
;;     channel, so steps 1-5 all use it. a key cannot be delivered under
;;     itself.  4.3.1.2 p.4-5 recommends this be an SA other than the one
;;     being affected.
;;   sessionkey1 / sessionkey2            delivered by OTAR, activated in
;;     step 2, bound to the SA as Encryption and Authentication Key ID in
;;     step 3, put in service in step 4, and first used in step 6.
;;
;; SEQUENCE NUMBERS
;;   Steps 1-5 run on the old SA and advance one successor per frame.
;;   Step 6 restarts at new_arsn: 5.5.1.4.2.7 p.5-16 makes the Rekey SA ARSN the
;;   NEW value for the new key, i.e. a counter reset, not an increment.
;;
;; ASSUMPTIONS
;;   keymaster is non-originating: 3.2.3.1.2.2 p.3-4 pre-shares it and no
;;     procedure transmits it.
;;   the in service SA keys are non originating in the skeletons.
;;   sessionkey1, sessionkey2, new_arsn, chal and frame_data originate uniquely
;;     at the Initiator.
;;
;; NOT MODELLED
;;   Create SA, Delete SA, Stop SA, Expire SA, Key Deactivation, Key Destruction
;;   3.3.3.1.3.4 d.2, the GVCID authorization check

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))
(defmacro (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
  (cat keyid1 sessionkey1 keyid2 sessionkey2))
(defmacro (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
  (otar_pdu (keyid_of keymaster)
    (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))

(defmacro (key_activation_pdu keyid)
  (cat "ep-pdu" "tag:00-0010" keyid))

(defmacro (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
  (cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv))

(defmacro (start_sa_pdu spi gvcid)
  (cat "ep-pdu" "tag:01-1011" spi gvcid))

(defmacro (keyver_cmd keyid chal)
  (cat "ep-pdu" "tag:00-0100-cmd" keyid chal))
(defmacro (keyver_reply keyid chal sessionkey)
  (cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey)))

(defprotocol sdls-ep-chain-auth-enc basic

  (defrole ground
    (vars (header text) (old_arsn new_arsn seq_n) (iv text)
          (assumed_enc_key assumed_auth_key skey) (ground spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid)
          (spi spi) (gvcid gvcid) (chal text) (frame_data tc))
    (trace
      ;; STEP 1 -- OTAR, 3.2.3.1
      (send
        (cat (sdl_header spacecraft) header (successor old_arsn)
             (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor old_arsn)
                   (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key))
      )

      ;; STEP 2 -- Key Activation, 3.2.3.2
      (send
        (cat (sdl_header spacecraft) header (successor (successor old_arsn))
             (enc (key_activation_pdu keyid1) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor (successor old_arsn))
                   (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key))
      )

      ;; STEP 3 -- Rekey SA, 3.3.3.3
      (send
        (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
             (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
                   (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) assumed_auth_key))
      )

      ;; STEP 4 -- Start SA, 3.3.3.1
      (send
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
             (enc (start_sa_pdu spi gvcid) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
                   (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key))
      )


      (send
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
             (enc (keyver_cmd keyid1 chal) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
                   (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key))
      )

      ;; STEP 5 -- Key Verification, 3.2.3.5
      (recv
        (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
             (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key)
             (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
                   (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key))
      )
  ;; STEP 6 -- new SA carries traffic under the OTAR'd keys
      (send
        (cat (sdl_header spacecraft) header (successor new_arsn)
             (enc frame_data sessionkey1)
             (hash (sdl_header spacecraft) header (successor new_arsn)
                   (enc frame_data sessionkey1) sessionkey2))
      )

    )
    (uniq-gen assumed_enc_key assumed_auth_key old_arsn)
    (uniq-orig new_arsn chal frame_data sessionkey1 sessionkey2)
    (non-orig keymaster)
  )

  (defrole satellite
    (vars (header text) (old_arsn new_arsn seq_n) (iv text)
          (assumed_enc_key assumed_auth_key skey) (ground spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid)
          (spi spi) (gvcid gvcid) (chal text) (frame_data tc))
    (trace
            ;; STEP 1 -- OTAR, 3.2.3.1
      (recv
        (cat (sdl_header spacecraft) header (successor old_arsn)
             (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor old_arsn)
                   (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key))
      )

      ;; STEP 2 -- Key Activation, 3.2.3.2
      (recv
        (cat (sdl_header spacecraft) header (successor (successor old_arsn))
             (enc (key_activation_pdu keyid1) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor (successor old_arsn))
                   (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key))
      )

      ;; STEP 3 -- Rekey SA, 3.3.3.3
      (recv
        (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
             (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
                   (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) assumed_auth_key))
      )
    ;; STEP 4 -- Start SA, 3.3.3.1
      (recv
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
             (enc (start_sa_pdu spi gvcid) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
                   (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key))
      )

      ;; STEP 5 -- Key Verification, 3.2.3.5
      (recv
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
             (enc (keyver_cmd keyid1 chal) assumed_enc_key)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
                   (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key))
      )


      (send
        (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
             (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key)
             (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
                   (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key))
      )

      ;; STEP 6 -- new SA carries traffic under the OTAR'd keys
      (recv
        (cat (sdl_header spacecraft) header (successor new_arsn)
             (enc frame_data sessionkey1)
             (hash (sdl_header spacecraft) header (successor new_arsn)
                   (enc frame_data sessionkey1) sessionkey2))
      )

    )
    (non-orig keymaster)
  )

  (lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash)
        (spi atom) (gvcid atom))
)


(defskeleton sdls-ep-chain-auth-enc
  (vars (assumed_enc_key assumed_auth_key keymaster skey) (ground spacecraft name)
        (old_arsn new_arsn seq_n))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (keymaster keymaster)
                          (old_arsn old_arsn) (new_arsn new_arsn)
                          (ground ground) (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key keymaster)
  (facts (neq old_arsn new_arsn))
  (comment "Satellite point of view")
)

(defskeleton sdls-ep-chain-auth-enc
  (vars (assumed_enc_key assumed_auth_key keymaster sessionkey1 sessionkey2 skey)
        (ground spacecraft name) (old_arsn new_arsn seq_n))
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
                       (assumed_auth_key assumed_auth_key)
                       (keymaster keymaster)
                       (sessionkey1 sessionkey1) (sessionkey2 sessionkey2)
                       (old_arsn old_arsn) (new_arsn new_arsn)
                       (ground ground) (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key keymaster)
  (uniq-orig sessionkey1 sessionkey2)
  (facts (neq old_arsn new_arsn))
  (comment "Ground-station point of view")
)
```

---

### `refrences/internet/examples_scm/sdls-auth-enc-logic.scm`

*sha256:`8f15c79e0913` · 55 lines · 2.5 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sdls-auth-full-payload.scm`

*sha256:`3a36093acaf5` · 226 lines · 9.8 KB · lang:`scheme`*

```scheme
(herald "SDLSP TC Baseline: Authentication Only (AES-CMAC): full SDLS-EP rekeying sequence")

;; MODELLED
;;   1. OTAR                3.2.3.1   session keys delivered under the master key
;;   2. Key Activation      3.2.3.2   key IDs signalled for activation
;;   3. Rekey SA            3.3.3.3   keys bound to the SA
;;   4. Start SA            3.3.3.1   SA put in service on a channel
;;   5. Key Verification    3.2.3.5   challenge / response under the new key
;;   6. Traffic             355.0-B-2 the new SA protects a frame_data
;;
;; KEYS
;;   assumed_auth_key                     the SA already in service.  4.3.1.1
;;     p.4-5 requires every EP command PDU to ride an already-protected
;;     channel, so steps 1-5 all use it; a key cannot be delivered under
;;     itself.  4.3.1.2 p.4-5 recommends this be an SA other than the one
;;     being affected.
;;   sessionkey1 / sessionkey2            delivered by OTAR, bound to the SA
;;     as Encryption and Authentication Key ID in step 3.  Only sessionkey2
;;     protects step 6 traffic.  sessionkey1 is exercised only by the Key
;;     Verification response, which 5.4.2.5.3.4 p.5-11 encrypts regardless of
;;     the frame transport mode.
;;
;; SEQUENCE NUMBERS
;;   Steps 1-5 run on the old SA and advance one successor per frame.
;;   Step 6 restarts at new_arsn: 5.5.1.4.2.7 p.5-16 makes the Rekey SA ARSN the
;;   NEW value for the new key, like a counter reset instead of an increment.
;;
;; ASSUMPTIONS
;;   keymaster is non-originating: 3.2.3.1.2.2 p.3-4 pre-shares it and no
;;     procedure transmits it. Must be assumed for generic protocol version
;;   the in-service SA keys are non-originating in the point-of-view skeletons.
;;   sessionkey1, sessionkey2, new_arsn, chal and frame_data originate uniquely
;;     at the Initiator.
;;
;;
;; NOT MODELLED
;;   Create SA, Delete SA, Stop SA, Expire SA, Key Deactivation, Key Destruction
;;   3.3.3.1.3.4 d.2, the GVCID authorization check



(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))
(defmacro (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
  (cat keyid1 sessionkey1 keyid2 sessionkey2))
(defmacro (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
  (otar_pdu (keyid_of keymaster)
    (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))

(defmacro (key_activation_pdu keyid)
  (cat "ep-pdu" "tag:00-0010" keyid))

(defmacro (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
  (cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv))

(defmacro (start_sa_pdu spi gvcid)
  (cat "ep-pdu" "tag:01-1011" spi gvcid))

(defmacro (keyver_cmd keyid chal)
  (cat "ep-pdu" "tag:00-0100-cmd" keyid chal))
(defmacro (keyver_reply keyid chal sessionkey)
  (cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey)))

(defprotocol sdls-ep-chain-auth basic

  (defrole ground
    (vars (header text) (old_arsn new_arsn seq_n) (iv text)
          (assumed_auth_key skey) (ground spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid)
          (spi spi) (gvcid gvcid) (chal text) (frame_data tc))
    (trace
        ;; STEP 1 -- OTAR, 3.2.3.1
      (send
        (cat (sdl_header spacecraft) header (successor old_arsn)
             (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
             (hash (sdl_header spacecraft) header (successor old_arsn)
                   (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key))
      )

      ;; STEP 2 -- Key Activation, 3.2.3.2
      (send
        (cat (sdl_header spacecraft) header (successor (successor old_arsn))
             (key_activation_pdu keyid1)
             (hash (sdl_header spacecraft) header (successor (successor old_arsn))
                   (key_activation_pdu keyid1) assumed_auth_key))
      )

      ;; STEP 3 -- Rekey SA, 3.3.3.3
      (send
        (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
             (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv)
             (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
                   (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_auth_key))
      )

      ;; STEP 4 -- Start SA, 3.3.3.1
      (send
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
             (start_sa_pdu spi gvcid)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
                   (start_sa_pdu spi gvcid) assumed_auth_key))
      )

      ;; STEP 5 -- Key Verification, 3.2.3.5
      (send
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
             (keyver_cmd keyid1 chal)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
                   (keyver_cmd keyid1 chal) assumed_auth_key))
      )


      (recv
        (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
             (keyver_reply keyid1 chal sessionkey1)
             (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
                   (keyver_reply keyid1 chal sessionkey1) assumed_auth_key))
      )
   ;; STEP 6 -- new SA carries traffic under the OTAR'd keys
      (send
        (cat (sdl_header spacecraft) header (successor new_arsn)
             frame_data
             (hash (sdl_header spacecraft) header (successor new_arsn)
                   frame_data sessionkey2))
      )

    )
  )

  (defrole satellite
    (vars (header text) (old_arsn new_arsn seq_n) (iv text)
          (assumed_auth_key skey) (ground spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid)
          (spi spi) (gvcid gvcid) (chal text) (frame_data tc))
    (trace
      (recv
        (cat (sdl_header spacecraft) header (successor old_arsn)
             (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
             (hash (sdl_header spacecraft) header (successor old_arsn)
                   (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key))
      )
      ;; STEP 1 -- OTAR, 3.2.3.1

      (recv
        (cat (sdl_header spacecraft) header (successor (successor old_arsn))
             (key_activation_pdu keyid1)
             (hash (sdl_header spacecraft) header (successor (successor old_arsn))
                   (key_activation_pdu keyid1) assumed_auth_key))
      )
      ;; STEP 2 -- Key Activation, 3.2.3.2

      (recv
        (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
             (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv)
             (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn)))
                   (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_auth_key))
      )
      ;; STEP 3 -- Rekey SA, 3.3.3.3

      (recv
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
             (start_sa_pdu spi gvcid)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn))))
                   (start_sa_pdu spi gvcid) assumed_auth_key))
      )
      ;; STEP 4 -- Start SA, 3.3.3.1

      (recv
        (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
             (keyver_cmd keyid1 chal)
             (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn)))))
                   (keyver_cmd keyid1 chal) assumed_auth_key))
      )
      (send
        (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
             (keyver_reply keyid1 chal sessionkey1)
             (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn))))))
                   (keyver_reply keyid1 chal sessionkey1) assumed_auth_key))
      )
      ;; STEP 5 -- Key Verification, 3.2.3.5

      (recv
        (cat (sdl_header spacecraft) header (successor new_arsn)
             frame_data
             (hash (sdl_header spacecraft) header (successor new_arsn)
                   frame_data sessionkey2))
      )
      ;; STEP 6 -- new SA carries traffic under the OTAR'd keys
    )
  )

  (lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash)
        (spi atom) (gvcid atom))
)

(defskeleton sdls-ep-chain-auth
  (vars (assumed_auth_key keymaster skey) (ground spacecraft name)
        (old_arsn new_arsn seq_n))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (keymaster keymaster)
                          (old_arsn old_arsn) (new_arsn new_arsn)
                          (ground ground) (spacecraft spacecraft))
  (non-orig assumed_auth_key keymaster)
  (facts (neq old_arsn new_arsn))
  (non-orig keymaster)
  (comment "Satellite point of view")
)

(defskeleton sdls-ep-chain-auth
  (vars (assumed_auth_key keymaster sessionkey1 sessionkey2 skey)
        (ground spacecraft name) (old_arsn new_arsn seq_n) (chal text) (frame_data tc))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
                       (keymaster keymaster)
                       (sessionkey1 sessionkey1) (sessionkey2 sessionkey2)
                       (old_arsn old_arsn) (new_arsn new_arsn)
                       (ground ground) (spacecraft spacecraft) (chal chal) (frame_data frame_data))
  (non-orig assumed_auth_key keymaster)
  (uniq-orig sessionkey1 sessionkey2)
  (facts (neq old_arsn new_arsn))
  (uniq-gen old_arsn)
  (uniq-orig new_arsn chal frame_data sessionkey1 sessionkey2)
  (non-orig keymaster)
  (comment "Ground-station point of view")
)
```

---

### `refrences/internet/examples_scm/sdls-auth-logic.scm`

*sha256:`69e52ed30db5` · 75 lines · 3.0 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sdls-enc-logic.scm`

*sha256:`ab76741609f5` · 78 lines · 2.7 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sdls-ep-challenge-auth.scm`

*sha256:`350ed2a1d1d9` · 49 lines · 2.7 KB · lang:`scheme`*

```scheme
(herald "SDLS-EP Key Verification: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (keyver_cmd keyid chal)
  (cat "ep-pdu" "tag:00-0100-cmd" keyid chal))
(defmacro (keyver_reply keyid chal sessionkey)
  (cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey)))

(defprotocol sdls-ep-key-verification-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (ground spacecraft name)
          (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal)
             (hash (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) assumed_auth_key)))
      (recv (cat (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1)
             (hash (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (ground spacecraft name)
          (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal)
             (hash (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) assumed_auth_key)))
      (send (cat (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1)
             (hash (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom)))

(defskeleton sdls-ep-key-verification-auth
  (vars (assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (sessionkey1 sessionkey1) (keyid1 keyid1)
                          (ground ground) (spacecraft spacecraft))
  (non-orig assumed_auth_key)
  (pen-non-orig sessionkey1)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-key-verification-auth
  (vars (assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid) (chal text) (old_arsn seq_n))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
                       (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal)
                       (ground ground) (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_auth_key)
  (pen-non-orig sessionkey1)
  (uniq-orig chal)
  (uniq-gen old_arsn)
  (comment "Ground-station point of view"))
```

---

### `refrences/internet/examples_scm/sdls-ep-challenge-authenc.scm`

*sha256:`d4e5673b3ddc` · 51 lines · 3.0 KB · lang:`scheme`*

```scheme
(herald "SDLS-EP Key Verification: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (keyver_cmd keyid chal)
  (cat "ep-pdu" "tag:00-0100-cmd" keyid chal))
(defmacro (keyver_reply keyid chal sessionkey)
  (cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey)))

(defprotocol sdls-ep-key-verification-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (ground spacecraft name)
          (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))
      (recv (cat (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key)
             (hash (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (ground spacecraft name)
          (keyid1 keyid) (sessionkey1 skey) (chal text))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))
      (send (cat (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key)
             (hash (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom)))

(defskeleton sdls-ep-key-verification-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (sessionkey1 sessionkey1) (keyid1 keyid1)
                          (ground ground) (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (pen-non-orig sessionkey1)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-key-verification-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid) (chal text) (old_arsn seq_n))
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
                       (assumed_auth_key assumed_auth_key)
                       (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal)
                       (ground ground) (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_enc_key assumed_auth_key)
  (pen-non-orig sessionkey1)
  (uniq-orig chal)
  (uniq-orig old_arsn)
  (comment "Ground-station point of view"))
```

---

### `refrences/internet/examples_scm/sdls-ep-challenge.scm`

*sha256:`312adef361d9` · 40 lines · 1.3 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sdls-ep-key-activation-auth.scm`

*sha256:`a6bc99dd2efc` · 40 lines · 1.7 KB · lang:`scheme`*

```scheme
(herald "SDLS-EP Key Activation: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (key_activation_pdu keyid)
  (cat "ep-pdu" "tag:00-0010" keyid))

(defprotocol sdls-ep-key-activation-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (keyid1 keyid))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1)
             (hash (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (keyid1 keyid))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1)
             (hash (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom)))

(defskeleton sdls-ep-key-activation-auth
  (vars (assumed_auth_key skey) (spacecraft name) (keyid1 keyid))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (keyid1 keyid1)
                          (spacecraft spacecraft))
  (non-orig assumed_auth_key)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-key-activation-auth
  (vars (assumed_auth_key skey) (spacecraft name) (keyid1 keyid) (old_arsn seq_n))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
                       (keyid1 keyid1)
                       (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_auth_key)
  (uniq-gen old_arsn)
  (comment "Ground-station point of view"))
```

---

### `refrences/internet/examples_scm/sdls-ep-key-activation-authenc.scm`

*sha256:`6367eb4a2d12` · 42 lines · 2.0 KB · lang:`scheme`*

```scheme
(herald "SDLS-EP Key Activation: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (key_activation_pdu keyid)
  (cat "ep-pdu" "tag:00-0010" keyid))

(defprotocol sdls-ep-key-activation-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (keyid1 keyid))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (keyid1 keyid))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom)))

(defskeleton sdls-ep-key-activation-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keyid1 keyid))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (keyid1 keyid1)
                          (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-key-activation-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keyid1 keyid) (old_arsn seq_n))
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
                       (assumed_auth_key assumed_auth_key)
                       (keyid1 keyid1)
                       (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_enc_key assumed_auth_key)
  (uniq-orig old_arsn)
  (comment "Ground-station point of view"))
```

---

### `refrences/internet/examples_scm/sdls-ep-key-activation.scm`

*sha256:`8e5407169d35` · 28 lines · 0.8 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sdls-ep-otar-auth.scm`

*sha256:`3361496cd892` · 49 lines · 2.5 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sdls-ep-otar-authenc.scm`

*sha256:`9c21a336cca3` · 51 lines · 2.8 KB · lang:`scheme`*

```scheme
(herald "SDLS-EP OTAR: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (otar_pdu masterkeyid uploadblock)
  (cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock))
(defmacro (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)
  (cat keyid1 sessionkey1 keyid2 sessionkey2))
(defmacro (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)
  (otar_pdu (keyid_of keymaster)
    (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))

(defprotocol sdls-ep-otar-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (keymaster sessionkey1 sessionkey2 skey) (keyid1 keyid2 keyid))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (keyid atom) (keyid_of hash)))

(defskeleton sdls-ep-otar-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keymaster skey))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (keymaster keymaster)
                          (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key keymaster)
  (non-orig keymaster)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-otar-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keymaster sessionkey1 sessionkey2 skey) (old_arsn seq_n))
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
                       (assumed_auth_key assumed_auth_key)
                       (keymaster keymaster)
                       (sessionkey1 sessionkey1) (sessionkey2 sessionkey2)
                       (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_enc_key assumed_auth_key keymaster)
  (uniq-orig sessionkey1 sessionkey2)
  (non-orig keymaster)
  (uniq-orig old_arsn)
  (comment "Ground-station point of view"))
```

---

### `refrences/internet/examples_scm/sdls-ep-otar-transmission.scm`

*sha256:`c6cab6fa329e` · 50 lines · 1.7 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sdls-ep-sa-rekey-auth.scm`

*sha256:`efa36900f119` · 47 lines · 2.4 KB · lang:`scheme`*

```scheme
(herald "SDLS-EP Rekey SA: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
  (cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv))

(defprotocol sdls-ep-rekey-sa-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
             (hash (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
             (hash (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (spi atom) (keyid atom)))

(defskeleton sdls-ep-rekey-sa-auth
  (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (spi spi) (enckeyid enckeyid)
                          (authkeyid authkeyid) (new_arsn new_arsn)
                          (old_arsn old_arsn)
                          (spacecraft spacecraft))
  (non-orig assumed_auth_key)
  (facts (neq old_arsn new_arsn))
  (comment "Satellite point of view"))

(defskeleton sdls-ep-rekey-sa-auth
  (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
                       (spi spi) (enckeyid enckeyid)
                       (authkeyid authkeyid) (new_arsn new_arsn)
                       (old_arsn old_arsn)
                       (spacecraft spacecraft))
  (non-orig assumed_auth_key)
  (uniq-orig new_arsn)
  (facts (neq old_arsn new_arsn))
  (uniq-gen old_arsn)
  (comment "Ground-station point of view"))
```

---

### `refrences/internet/examples_scm/sdls-ep-sa-rekey-authenc.scm`

*sha256:`161329f435d8` · 49 lines · 2.6 KB · lang:`scheme`*

```scheme
(herald "SDLS-EP Rekey SA: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)
  (cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv))

(defprotocol sdls-ep-rekey-sa-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n) (iv text))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (spi atom) (keyid atom)))

(defskeleton sdls-ep-rekey-sa-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (spi spi) (enckeyid enckeyid)
                          (authkeyid authkeyid) (new_arsn new_arsn)
                          (old_arsn old_arsn)
                          (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (facts (neq old_arsn new_arsn))
  (comment "Satellite point of view"))

(defskeleton sdls-ep-rekey-sa-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n))
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
                       (assumed_auth_key assumed_auth_key)
                       (spi spi) (enckeyid enckeyid)
                       (authkeyid authkeyid) (new_arsn new_arsn)
                       (old_arsn old_arsn)
                       (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (uniq-orig new_arsn)
  (facts (neq old_arsn new_arsn))
  (uniq-orig old_arsn)
  (comment "Ground-station point of view"))
```

---

### `refrences/internet/examples_scm/sdls-ep-sa-rekey.scm`

*sha256:`f4d29e1126d6` · 36 lines · 1.4 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sdls-ep-sa-start-auth.scm`

*sha256:`176085a6c5c2` · 40 lines · 1.8 KB · lang:`scheme`*

```scheme
(herald "SDLS-EP Start SA: Authentication Only")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len"))

(defmacro (start_sa_pdu spi gvcid)
  (cat "ep-pdu" "tag:01-1011" spi gvcid))

(defprotocol sdls-ep-start-sa-auth basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (spi spi) (gvcid gvcid))
    (trace
      (send (cat (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid)
             (hash (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (spacecraft name)
          (spi spi) (gvcid gvcid))
    (trace
      (recv (cat (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid)
             (hash (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (spi atom) (gvcid atom)))

(defskeleton sdls-ep-start-sa-auth
  (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid))
  (defstrandmax satellite (assumed_auth_key assumed_auth_key)
                          (spi spi) (gvcid gvcid)
                          (spacecraft spacecraft))
  (non-orig assumed_auth_key)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-start-sa-auth
  (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid) (old_arsn seq_n))
  (defstrandmax ground (assumed_auth_key assumed_auth_key)
                       (spi spi) (gvcid gvcid)
                       (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_auth_key)
  (uniq-gen old_arsn)
  (comment "Ground-station point of view"))
```

---

### `refrences/internet/examples_scm/sdls-ep-sa-start-authenc.scm`

*sha256:`61c0b0266d5c` · 42 lines · 2.1 KB · lang:`scheme`*

```scheme
(herald "SDLS-EP Start SA: Authenticated Encryption")

(defmacro (sdl_header dest) (cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number"))

(defmacro (start_sa_pdu spi gvcid)
  (cat "ep-pdu" "tag:01-1011" spi gvcid))

(defprotocol sdls-ep-start-sa-auth-enc basic
  (defrole ground
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (spi spi) (gvcid gvcid))
    (trace
      (send (cat (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))))

  (defrole satellite
    (vars (header text) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (spacecraft name)
          (spi spi) (gvcid gvcid))
    (trace
      (recv (cat (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key)
             (hash (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))))

  (lang (seq_n atom) (successor hash) (spi atom) (gvcid atom)))

(defskeleton sdls-ep-start-sa-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid))
  (defstrandmax satellite (assumed_enc_key assumed_enc_key)
                          (assumed_auth_key assumed_auth_key)
                          (spi spi) (gvcid gvcid)
                          (spacecraft spacecraft))
  (non-orig assumed_enc_key assumed_auth_key)
  (comment "Satellite point of view"))

(defskeleton sdls-ep-start-sa-auth-enc
  (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid) (old_arsn seq_n))
  (defstrandmax ground (assumed_enc_key assumed_enc_key)
                       (assumed_auth_key assumed_auth_key)
                       (spi spi) (gvcid gvcid)
                      (spacecraft spacecraft) (old_arsn old_arsn))
  (non-orig assumed_enc_key assumed_auth_key)
  (uniq-orig old_arsn)
  (comment "Ground-station point of view"))
```

---

### `refrences/internet/examples_scm/sdls-ep-sa-start.scm`

*sha256:`db963aab66d9` · 38 lines · 1.1 KB · lang:`scheme`*

```scheme
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
```

---

### `refrences/internet/examples_scm/sigenc.scm`

*sha256:`7de7f622deba` · 44 lines · 1.5 KB · lang:`scheme`*

```scheme
(herald "Signed Encrypted Message Example"
   (comment "Shows examples of key usage of asymmetric keys"))

(defprotocol mult-keys-sig-enc basic
   (defrole init
    (vars (a b name) (n1 n2 text))
    (trace
     (send (enc (enc n1 a (privk "sig" a)) (pubk "enc" b)))
     (recv (enc (enc n1 n2 (privk "sig" b)) (pubk "enc" a)))
     (send (enc (enc n2 (privk "sig" a)) (pubk "enc" b)))))
  (defrole resp
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc (enc n1 a (privk "sig" a)) (pubk "enc" b)))
     (send (enc (enc n1 n2 (privk "sig" b)) (pubk "enc" a)))
     (recv (enc (enc n2 (privk "sig" a)) (pubk "enc" b))))))

;;; The initiator point-of-view
(defskeleton mult-keys-sig-enc
   (vars (a b name) (n1 text))
   (defstrand init 3 (a a) (b b) (n1 n1))
   (non-orig (privk "enc" a) (privk "sig" a) (privk "enc" b))
   (uniq-orig n1))

;;; The responder point-of-view trusting only a's signature key
(defskeleton mult-keys-sig-enc
  (vars (a b name) (n2 text))
  (defstrand resp 3 (a a) (b b) (n2 n2))
  (non-orig (privk "sig" a))
  (uniq-orig n2))

;;; The responder point-of-view trusting only a's encryption key
(defskeleton mult-keys-sig-enc
  (vars (a b name) (n2 text))
  (defstrand resp 3 (a a) (b b) (n2 n2))
  (non-orig (privk "enc" a))
  (uniq-orig n2))

;;; The responder point-of-view trusting both of a's keys
(defskeleton mult-keys-sig-enc
  (vars (a b name) (n2 text))
  (defstrand resp 3 (a a) (b b) (n2 n2))
  (non-orig (privk "sig" a) (privk "enc" a))
  (uniq-orig n2))
```

---

### `refrences/internet/examples_scm/sorted_epmo_acctnum.scm`

*sha256:`3e81474246f0` · 90 lines · 3.3 KB · lang:`scheme`*

```scheme
(herald "Electronic Purchase with Money Order Protocol Variant"
  (bound 12)
  (comment "This version includes account numbers in exchanges"
	   "This version uses sorts to avoid confusion"
	   "between a nonce and other data"))

(defprotocol sorted_epmo_acctnum basic
  (defrole bank
    (vars (b c m name) (acctnum price text) (hash name) (nc nm nb data))
    (trace
     (recv (enc c nc nm acctnum price (pubk b)))
     (send (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b))
		(enc nc nb (pubk c))))
     (recv (enc (enc "hash" b m nb nm (pubk hash)) (privk m))))
    (non-orig (privk hash))
    (annotations b
      (1
        (forall ((pm name))
          (implies
            (and (authtransfer c acctnum b price pm nm)
              (reqtransfer pm b price pm nm))
            (dotransfer acctnum b price pm nm))))
      (2
        (and (says c (authtransfer c acctnum b price m nm))
          (says m (reqtransfer m b price m nm))))))
  (defrole customer
    (vars (b c m hash name) (acctnum goods price text) (nc nm nb data))
    (trace
     (send (enc c nc goods (pubk m)))
     (recv (enc nc nm m price (pubk c)))
     (send (enc c nc nm acctnum price (pubk b)))
     (recv (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b))
		(enc nc nb (pubk c))))
     (send (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b))
		nb)))
    (non-orig (privk b) (privk hash))
    (uniq-orig nc)
    (annotations c
      (1
        (says m
          (implies
            (exists ((acctnum2 text))
              (dotransfer acctnum2 b price m nm)) (doship m goods c))))
      (3
        (says b
          (forall ((pm name))
            (implies
              (and (authtransfer c acctnum b price m nm)
                (reqtransfer pm b price pm nm))
              (dotransfer acctnum b price pm nm)))))
      (4 (authtransfer c acctnum b price m nm))))
  (defrole merchant (vars (b c m hash name) (goods price text) (nc nm nb data))
    (trace
     (recv (enc c nc goods (pubk m)))
     (send (enc nc nm m price (pubk c)))
     (recv (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b))
		nb))
     (send (enc (enc "hash" b m nb nm (pubk hash)) (privk m))))
    (non-orig (privk hash))
    (uniq-orig nm)
    (annotations m
      (1
        (implies
          (exists ((acctnum2 text)) (dotransfer acctnum2 b price m nm))
          (doship m goods c)))
      (2
        (and
          (says b
            (forall ((pm name))
              (exists ((acctnum2 text))
                (implies
                  (and (authtransfer c acctnum2 b price m nm)
                    (reqtransfer pm b price pm nm))
                  (dotransfer acctnum2 b price pm nm)))))
          (says c
            (exists ((acctnum2 text))
              (authtransfer c acctnum2 b price m nm)))))
      (3 (and (reqtransfer m b price m nm) (doship m goods c))))))

(defskeleton sorted_epmo_acctnum
  (vars (b m c name) (nm nc nb data) (hash name))
  (defstrand merchant 4 (b b) (m m) (c c) (nm nm) (nc nc) (nb nb) (hash hash))
  (non-orig (privk b) (privk m) (privk c) (privk hash))
  (uniq-orig nm nc nb))

(defskeleton sorted_epmo_acctnum
  (vars (b m c name) (nm nb nc data) (hash name) (price acctnum text))
  (defstrand bank 3 (b b) (m m) (c c) (nm nm) (nb nb) (nc nc) (hash hash))
  (non-orig (privk b) (privk m) (privk c) (privk hash))
  (uniq-orig nm nc nb))
```

---

### `refrences/internet/examples_scm/sts.scm`

*sha256:`f4cba59e4388` · 81 lines · 2.2 KB · lang:`scheme`*

```scheme
;;; Station-to-station

;;; This is an authenticated form of a Diffie-Hellman key exchange.

;;; The file contains one model of the station-to-station protocol.
;;; An assumption is made that *any* initiator or responder properly
;;; picks a fresh random exponent and does not allow it to be obtained
;;; by the adversary.

(herald "Station-to-station protocol" (bound 20) (algebra diffie-hellman))

(defprotocol station-to-station diffie-hellman
  (defrole init
    (vars (x rndx) (eta expt) (a b name))
    (trace
     (send (exp (gen) x))
     (recv (cat (exp (gen) eta)
		(enc (enc (exp (gen) eta)
			  (exp (gen) x) (privk b))
		     (exp (exp (gen) eta) x))))
     (send (enc (enc (exp (gen) x)
		     (exp (gen) eta) (privk a))
		(exp (exp (gen) eta) x)))
     (send (privk a)))
    (uniq-gen x))
  (defrole resp
    (vars (y rndx) (chi expt) (a b name))
    (trace
     (recv (exp (gen) chi))
     (send (cat (exp (gen) y)
		(enc (enc (exp (gen) y)
			  (exp (gen) chi) (privk b))
		     (exp (exp (gen) chi) y))))
     (recv (enc (enc (exp (gen) chi)
		     (exp (gen) y) (privk a))
		(exp (exp (gen) chi) y)))
     (send (privk b)))
    (uniq-gen y)))

(defskeleton station-to-station
  (vars (a b name))
  (defstrand init 3 (a a) (b b))
  (non-orig (privk b) (privk a))
)

(defskeleton station-to-station
  (vars (a b name))
  (defstrand resp 3 (a a) (b b))
  (non-orig (privk a) (privk b))
  )

(defskeleton station-to-station
  (vars (a b name)(x y rndx) (eta expt))
  (defstrand init 3 (a a) (b b) (x x) (eta eta))
  (deflistener (exp (exp (gen) eta) x))
  (non-orig (privk b) (privk a))
)

(defskeleton station-to-station
  (vars (a b name) (x y rndx)(chi expt))
  (defstrand resp 3 (a a) (b b) (y y) (chi chi))
  (deflistener (exp (exp (gen) chi) y))
  (non-orig (privk a) (privk b))
)

(defskeleton station-to-station
  (vars (a b name) (x y rndx))
  (defstrand init 4 (a a) (b b) (eta y) (x x))
  (defstrand resp 4 (b b) (chi x) (y y))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (uniq-orig (privk b) (privk a))
  )

(defskeleton station-to-station
  (vars (a b name) (x y rndx))
  (defstrand init 4 (a a) (b b) (eta y) (x x))
  (defstrand resp 4 (b b) (chi x) (y y))
  (deflistener (exp (gen) (mul x y)))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (uniq-orig (privk b) (privk a))
  )
```

---

### `refrences/internet/examples_scm/sts_non_role.scm`

*sha256:`1b34a75f590e` · 98 lines · 2.6 KB · lang:`scheme`*

```scheme
;;; Station-to-station

;;; This is an authenticated form of a Diffie-Hellman key exchange.

;;; The file contains one model of the station-to-station protocol.
;;; An assumption is made that *any* initiator or responder properly
;;; picks a fresh random exponent and does not allow it to be obtained
;;; by the adversary.

(herald "Station-to-station protocol:  Weakened version"
	(bound 20)
	(algebra diffie-hellman))

(defprotocol station-weak diffie-hellman
  (defrole init
    (vars (x rndx) (eta expt) (a b name))
    (trace
     (send (exp (gen) x))
     (recv (cat (exp (gen) eta)
		(enc (enc (exp (gen) eta)
			  (exp (gen) x) (privk b))
		     (exp (exp (gen) eta) x))))
     (send (enc (enc (exp (gen) x)
		     (exp (gen) eta) (privk a))
		(exp (exp (gen) eta) x)))
     (send (privk a)))
    ;; (uniq-gen x)
    )
  (defrole resp
    (vars (y rndx) (chi expt) (a b name))
    (trace
     (recv (exp (gen) chi))
     (send (cat (exp (gen) y)
		(enc (enc (exp (gen) y)
			  (exp (gen) chi) (privk b))
		     (exp (exp (gen) chi) y))))
     (recv (enc (enc (exp (gen) chi)
		     (exp (gen) y) (privk a))
		(exp (exp (gen) chi) y)))
     (send (privk b)))
    ;; (uniq-gen y)
    ))

(defskeleton station-weak
  (vars (a b name) (x y rndx))
  (defstrand init 3 (a a) (b b) (x x) (eta y))
  (uniq-gen x y)
  (non-orig (privk b) (privk a))
)

(defskeleton station-weak
  (vars (a b name) (x y rndx))
  (defstrand resp 3 (a a) (b b) (y y) (chi x))
  (uniq-gen x y)
  (non-orig (privk a) (privk b))
  )

(defskeleton station-weak
  (vars (a b name) (x y rndx))
  (defstrand init 3 (a a) (b b) (x x) (eta y))
  (deflistener (exp (exp (gen) y) x))
  (uniq-gen x y)
  (non-orig (privk b) (privk a)))

(defskeleton station-weak
  (vars (a b name) (x rndx) (eta expt))
  (defstrand init 3 (a a) (b b) (x x) (eta eta))
  (deflistener (exp (exp (gen) eta) x))
  (uniq-gen x)
  (non-orig (privk b) (privk a)))


(defskeleton station-weak
  (vars (a b name) (y rndx) (chi expt))
  (defstrand resp 3 (a a) (b b) (y y) (chi chi))
  (deflistener (exp (exp (gen) chi) y))
  (non-orig (privk a) (privk b))
  (uniq-gen y)
)

(defskeleton station-weak
  (vars (a b name) (x y rndx))
  (defstrand init 4 (a a) (b b) (eta y) (x x))
  (defstrand resp 4 (b b) (chi x) (y y))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (uniq-gen x y)
  (uniq-orig (privk b) (privk a))
  )

(defskeleton station-weak 
  (vars (a b name) (x y rndx))
  (defstrand init 4 (a a) (b b) (eta y) (x x))
  (defstrand resp 4 (b b) (chi x) (y y))
  (deflistener (exp (gen) (mul x y)))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (uniq-gen x y)
  (uniq-orig (privk b) (privk a))
  )
```

---

### `refrences/internet/examples_scm/sts_weakened_reflect.scm`

*sha256:`c639a40306a4` · 80 lines · 2.3 KB · lang:`scheme`*

```scheme
;;; Station-to-station

;;; This is an authenticated form of a Diffie-Hellman key exchange.

;;; The file contains one model of the station-to-station protocol.
;;; We weaken it here by omitting the flip in the order of components
;;; in the second and third msgs.

(herald "station-to-station-reflect protocol" (bound 20) (algebra diffie-hellman))

(defprotocol station-to-station-reflect diffie-hellman
  (defrole init
    (vars (x rndx) (eta expt) (a b name))
    (trace
     (send (exp (gen) x))
     (recv (cat (exp (gen) eta)
		(enc (enc (exp (gen) eta)
			  (exp (gen) x) (privk b))
		     (exp (exp (gen) eta) x))))
     (send (enc (enc (exp (gen) eta)
		     (exp (gen) x) (privk a))
		(exp (exp (gen) eta) x)))
     (send (privk a)))
    (uniq-gen x))
  (defrole resp
    (vars (y rndx) (chi expt) (a b name))
    (trace
     (recv (exp (gen) chi))
     (send (cat (exp (gen) y)
		(enc (enc (exp (gen) y)
			  (exp (gen) chi) (privk b))
		     (exp (exp (gen) chi) y))))
     (recv (enc (enc (exp (gen) y)
		     (exp (gen) chi) (privk a))
		(exp (exp (gen) chi) y)))
     (send (privk b)))
    (uniq-gen y)))

(defskeleton station-to-station-reflect
  (vars (a b name))
  (defstrand init 3 (a a) (b b))
  (non-orig (privk b) (privk a))
)

(defskeleton station-to-station-reflect
  (vars (a b name))
  (defstrand resp 3 (a a) (b b))
  (non-orig (privk a) (privk b))
  )

(defskeleton station-to-station-reflect
  (vars (a b name)(x y rndx) (eta expt))
  (defstrand init 3 (a a) (b b) (x x) (eta eta))
  (deflistener (exp (exp (gen) eta) x))
  (non-orig (privk b) (privk a))
)

(defskeleton station-to-station-reflect
  (vars (a b name) (x y rndx)(chi expt))
  (defstrand resp 3 (a a) (b b) (y y) (chi chi))
  (deflistener (exp (exp (gen) chi) y))
  (non-orig (privk a) (privk b))
)

(defskeleton station-to-station-reflect
  (vars (a b name) (x y rndx))
  (defstrand init 4 (a a) (b b) (eta y) (x x))
  (defstrand resp 4 (b b) (chi x) (y y))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (uniq-orig (privk b) (privk a))
  )

(defskeleton station-to-station-reflect
  (vars (a b name) (x y rndx))
  (defstrand init 4 (a a) (b b) (eta y) (x x))
  (defstrand resp 4 (b b) (chi x) (y y))
  (deflistener (exp (gen) (mul x y)))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (uniq-orig (privk b) (privk a))
  )
```

---

### `refrences/internet/examples_scm/subatomic-open-closed-test-genrule.scm`

*sha256:`819efab85760` · 227 lines · 8.4 KB · lang:`scheme`*

```scheme
(herald subatomic-open-closed-test-genrule
	;; (try-old-strands)
	;; 	(check-nonces)
	;; 	(reverse-nodes)
	(bound 40))

(defmacro (dev-key-state d o k)
  (cat "st-k" d o k))

(defmacro (opened o)
  (cat o o))

(defmacro (closed o) o)

(defmacro (dev-state-opened d o)
  (cat "st" d (opened o)))

(defmacro (dev-state-closed d o)
  (cat "st" d (closed o)))

(defmacro (dev-state-any d o any)
  (cat "st" d any))

(defprotocol subatomic-open-closed basic
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan)
      (lk ls locn))
    (trace (recv start-ch (cat "power-up" d o k)) (load lk old)
      (load ls old1) (stor lk (cat "st-k" d o k))
      (stor ls (cat "st" d o)) (send (enc "up" k)))
    (auth start-ch)
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 4))
    (facts (same-dev ls lk)))
  (defrole owner-power-dev
    (vars (k skey) (d o name) (start-ch chan))
    (trace (send start-ch (cat "power-up" d o k)) (recv (enc "up" k)))
    (conf start-ch))
  (defrole owner-open
    (vars (k skey) (n text) (d o name))
    (trace (send (enc "open" d o n k)) (recv n)))
  (defrole owner-close
    (vars (k skey) (n text) (d o name))
    (trace (send (enc "close" d o n k)) (recv n)))
  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace (recv (enc "open" d o n k)) (load ls (cat "st" d any))
      (load lk (cat "st-k" d o k)) (stor ls (cat "st" d o o)) (send n))
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 3))
    (gen-st (cat "st-k" d o k) (cat "st" d (cat o o)))
    (facts (same-dev ls lk)))
  (defrole dev-close
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace (recv (enc "close" d o n k)) (load lk (cat "st-k" d o k))
      (load ls (cat "st" d any)) (stor ls (cat "st" d o)) (send n))
    (gen-st (cat "st-k" d o k))
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 3))
    (facts (same-dev ls lk)))
  (defrole dev-pass
    (vars (k skey) (n text) (d o name) (lk ls locn))
    (trace (load lk (cat "st-k" d o k)) (load ls (cat "st" d o o))
      (recv (enc "may I pass" k)) (send (enc "you may pass" n k)))
    (uniq-orig n)
    (gen-st (cat "st-k" d o k) (cat "st" d (cat o o)))
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (0 1))
    (facts (same-dev ls lk)))
  (defrole user-pass
    (vars (k skey))
    (trace (send (enc "may I pass" k)) (recv (enc "you may pass" k))))
  (defrule power-deliver-once
    (forall ((z1 z2 strd) (k skey))
      (implies
        (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k)
          (p "dev-up" "k" z2 k))
        (= z1 z2))))
  (defrule same-dev-ls-lk
    (forall ((ls lk lk-0 locn))
      (implies
        (and (fact same-dev ls lk) (fact same-dev ls lk-0))
        (= lk lk-0))))
  (defrule same-dev-lk-ls
    (forall ((lk ls ls-0 locn))
      (implies
        (and (fact same-dev ls lk) (fact same-dev ls-0 lk))
        (= ls ls-0))))
  (defgenrule neqRl_indx
    (forall ((x indx)) (implies (fact neq x x) (false))))
  (defgenrule neqRl_strd
    (forall ((x strd)) (implies (fact neq x x) (false))))
  (defgenrule neqRl_mesg
    (forall ((x mesg)) (implies (fact neq x x) (false))))
  (defgenrule no-interruption
    (forall ((z0 z1 z2 strd) (i0 i1 i2 indx))
      (implies
        (and (leads-to z0 i0 z2 i2) (trans z1 i1)
          (same-locn z0 i0 z1 i1) (prec z0 i0 z1 i1) (prec z1 i1 z2 i2))
        (false))))
  (defgenrule cakeRule
    (forall ((z0 z1 z2 strd) (i0 i1 i2 indx))
      (implies
        (and (trans z0 i0) (trans z1 i1) (leads-to z0 i0 z1 i1)
          (leads-to z0 i0 z2 i2) (prec z1 i1 z2 i2)) (false))))
  (defgenrule gen-st-dev-pass-0
    (forall ((z strd) (o d name))
      (implies
        (and (p "dev-pass" z 1) (p "dev-pass" "o" z o)
          (p "dev-pass" "d" z d)) (gen-st (cat "st" d o o)))))
  (defgenrule gen-st-dev-pass-1
    (forall ((z strd) (k skey) (o d name))
      (implies
        (and (p "dev-pass" z 1) (p "dev-pass" "k" z k)
          (p "dev-pass" "o" z o) (p "dev-pass" "d" z d))
        (gen-st (cat "st-k" d o k)))))
  (defgenrule fact-dev-pass-same-dev0
    (forall ((z strd) (ls lk locn))
      (implies
        (and (p "dev-pass" z 2) (p "dev-pass" "ls" z ls)
          (p "dev-pass" "lk" z lk)) (fact same-dev ls lk))))
  (defgenrule trRl_dev-close-at-2
    (forall ((z strd)) (implies (p "dev-close" z 3) (trans z 2))))
  (defgenrule trRl_dev-close-at-3
    (forall ((z strd)) (implies (p "dev-close" z 4) (trans z 3))))
  (defgenrule gen-st-dev-close-0
    (forall ((z strd) (k skey) (o d name))
      (implies
        (and (p "dev-close" z 1) (p "dev-close" "k" z k)
          (p "dev-close" "o" z o) (p "dev-close" "d" z d))
        (gen-st (cat "st-k" d o k)))))
  (defgenrule fact-dev-close-same-dev0
    (forall ((z strd) (ls lk locn))
      (implies
        (and (p "dev-close" z 3) (p "dev-close" "ls" z ls)
          (p "dev-close" "lk" z lk)) (fact same-dev ls lk))))
  (defgenrule trRl_dev-open-at-1
    (forall ((z strd)) (implies (p "dev-open" z 2) (trans z 1))))
  (defgenrule trRl_dev-open-at-3
    (forall ((z strd)) (implies (p "dev-open" z 4) (trans z 3))))
  (defgenrule gen-st-dev-open-0
    (forall ((z strd) (o d name))
      (implies
        (and (p "dev-open" z 1) (p "dev-open" "o" z o)
          (p "dev-open" "d" z d)) (gen-st (cat "st" d o o)))))
  (defgenrule gen-st-dev-open-1
    (forall ((z strd) (k skey) (o d name))
      (implies
        (and (p "dev-open" z 1) (p "dev-open" "k" z k)
          (p "dev-open" "o" z o) (p "dev-open" "d" z d))
        (gen-st (cat "st-k" d o k)))))
  (defgenrule fact-dev-open-same-dev0
    (forall ((z strd) (ls lk locn))
      (implies
        (and (p "dev-open" z 3) (p "dev-open" "ls" z ls)
          (p "dev-open" "lk" z lk)) (fact same-dev ls lk))))
  (defgenrule trRl_dev-up-at-1
    (forall ((z strd)) (implies (p "dev-up" z 2) (trans z 1))))
  (defgenrule trRl_dev-up-at-2
    (forall ((z strd)) (implies (p "dev-up" z 3) (trans z 2))))
  (defgenrule trRl_dev-up-at-3
    (forall ((z strd)) (implies (p "dev-up" z 4) (trans z 3))))
  (defgenrule trRl_dev-up-at-4
    (forall ((z strd)) (implies (p "dev-up" z 5) (trans z 4))))
  (defgenrule fact-dev-up-same-dev0
    (forall ((z strd) (ls lk locn))
      (implies
        (and (p "dev-up" z 3) (p "dev-up" "ls" z ls)
          (p "dev-up" "lk" z lk)) (fact same-dev ls lk))))
  (defgenrule scissorsRule
    (forall ((z0 z1 z2 strd) (i0 i1 i2 indx))
      (implies
        (and (trans z0 i0) (trans z1 i1) (trans z2 i2)
          (leads-to z0 i0 z1 i1) (leads-to z0 i0 z2 i2))
        (and (= z1 z2) (= i1 i2)))))
  (defgenrule cau-dev-pass-1
    (forall ((z z1 strd) (i indx))
      (implies (and (p "dev-pass" z 2) (prec z1 i z 1))
        (or (= z z1) (prec z1 i z 0)))))
  (defgenrule cau-dev-close-2
    (forall ((z z1 strd) (i indx))
      (implies (and (p "dev-close" z 3) (prec z1 i z 2))
        (or (= z z1) (prec z1 i z 1)))))
  (defgenrule cau-dev-open-2
    (forall ((z z1 strd) (i indx))
      (implies (and (p "dev-open" z 3) (prec z1 i z 2))
        (or (= z z1) (prec z1 i z 1)))))
  (defgenrule cau-dev-up-2
    (forall ((z z1 strd) (i indx))
      (implies (and (p "dev-up" z 3) (prec z1 i z 2))
        (or (= z z1) (prec z1 i z 1)))))
  (defgenrule eff-dev-up-3
    (forall ((z z1 strd) (i indx))
      (implies (and (p "dev-up" z 4) (prec z 3 z1 i))
        (or (= z z1) (and (p "dev-up" z 5) (prec z 4 z1 i))))))
  (defgenrule invShearsRule
    (forall ((z0 z1 z2 strd) (i0 i1 i2 indx))
      (implies
        (and (trans z0 i0) (trans z1 i1) (same-locn z0 i0 z1 i1)
          (leads-to z1 i1 z2 i2) (prec z0 i0 z2 i2))
        (or (and (= z0 z1) (= i0 i1)) (prec z0 i0 z1 i1)))))
  (defgenrule shearsRule
    (forall ((z0 z1 z2 strd) (i0 i1 i2 indx))
      (implies
        (and (trans z0 i0) (trans z1 i1) (trans z2 i2)
          (leads-to z0 i0 z1 i1) (same-locn z0 i0 z2 i2)
          (prec z0 i0 z2 i2))
        (or (and (= z1 z2) (= i1 i2)) (prec z1 i1 z2 i2))))))

(defskeleton subatomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (deflistener k)
  (uniq-orig k)
  (facts (no-state-split)))

(defskeleton subatomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand dev-pass 4 (k k))
  (facts (no-state-split)))

(defskeleton subatomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (defstrand dev-pass 4 (k k))
  (uniq-orig k)
  (facts (no-state-split)))
```

---

### `refrences/internet/examples_scm/subatomic-open-closed.scm`

*sha256:`eae2ff6d0a48` · 165 lines · 4.6 KB · lang:`scheme`*

```scheme
(herald subatomic-open-closed
	;; (try-old-strands)
	;; 	(check-nonces)
	;; 	(reverse-nodes)
	(bound 40))

(defmacro (dev-key-state d o k)
  (cat "st-k" d o k))

(defmacro (opened o)
  (cat o o))

(defmacro (closed o) o)

(defmacro (dev-state-opened d o)
  (cat "st" d (opened o)))

(defmacro (dev-state-closed d o)
  (cat "st" d (closed o)))

(defmacro (dev-state-any d o any)
  (cat "st" d any))

(defprotocol subatomic-open-closed basic
  (defrole dev-up
    (vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))
    (trace
     (recv start-ch (cat "power-up" d o k))
     (load lk old)
     (load ls old1)
     (stor lk (dev-key-state d o k))
     (stor ls (dev-state-closed d o))
     (send (enc "up" k)))
    (auth start-ch)
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 4))
    (facts (same-dev ls lk)))

  (defrole owner-power-dev
    (vars (k skey) (d o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" d o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "open" d o n k))
     (recv n)))

  (defrole owner-close
    (vars (k skey) (n text) (d o name))
    (trace
     (send (enc "close" d o n k))
     (recv n)))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (recv (enc "open" d o n k))
     (load ls (dev-state-any d o any))
     (load lk (dev-key-state d o k))
     (stor ls (dev-state-opened d o))
     (send n))
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 3))
    (gen-st (dev-key-state d o k) (dev-state-opened d o))
    (facts (same-dev ls lk)))

  (defrole dev-close
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (recv (enc "close" d o n k))
     (load lk (dev-key-state d o k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-closed d o))
     (send n))
    (gen-st (dev-key-state d o k))
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (1 3))
    (facts (same-dev ls lk)))

  (defrole dev-pass
    (vars (k skey) (n text) (d o name) (lk ls locn))
    (trace
     (load lk (dev-key-state d o k))
     (load ls (dev-state-opened d o))
     (recv (enc "may I pass" k))
     (send (enc "you may pass" n k)))
    (uniq-orig n)
    (gen-st (dev-key-state d o k) (dev-state-opened d o))
    ;; Critical section declarations are now obsolete.  
    ;; (critical-sections (0 1))
    (facts (same-dev ls lk)))

  (defrole user-pass
    (vars (k skey) (n text) (d o name) (l locn))
    (trace
     (send (enc "may I pass" k))
     (recv (enc "you may pass" k))))

   (defrule power-deliver-once
     (forall
      ((z1 z2 strd) (k skey))
      (implies
       (and (p "dev-up" z1 2)
 	   (p "dev-up" z2 2)
 	   (p "dev-up" "k" z1 k)
 	   (p "dev-up" "k" z2 k))
       (= z1 z2))))

   (defrule same-dev-ls-lk
     (forall ((ls lk lk-0 locn))
  	     (implies
  	      (and (fact same-dev ls lk)
  		   (fact same-dev ls lk-0))
  	      (= lk lk-0))))

   (defrule same-dev-lk-ls
     (forall ((lk ls ls-0 locn))
  	     (implies
  	      (and (fact same-dev ls lk)
  		   (fact same-dev ls-0 lk))
     	      (= ls ls-0)))))

(defskeleton subatomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (deflistener k)
  (uniq-orig k)
  (facts (no-state-split)))

(defskeleton subatomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand dev-pass 4 (k k))
  (facts (no-state-split)))

(defskeleton subatomic-open-closed
	   (vars (k skey) (d o name) (n text) (start-ch chan))
	   (defstrand owner-power-dev 2 (k k))
	   (defstrand dev-pass 4 (k k))
	   (uniq-orig k)
	   (facts (no-state-split)))

(comment
 (defskeleton subatomic-open-closed
   (vars (any old old1 mesg) (k skey) (n n-0 text) (d o name)
	 (pt pt-0 pt-1 pt-2 pt-3 pt-4 pval) (start-ch chan) (lk ls locn))
   (defstrand owner-power-dev 2 (k k) (d d) (o o) (start-ch start-ch))
   (defstrand dev-pass 4 (k k) (n n) (d d) (o o) (lk lk) (ls ls))
   (defstrand dev-open 4 (any any) (k k) (n n-0) (d d) (o o) (lk lk)
     (ls ls))
   (defstrand owner-open 1 (k k) (n n-0) (d d) (o o))
   (defstrand user-pass 1 (k k))
   (defstrand dev-up 6 (old old) (old1 old1) (k k) (d d) (o o)
     (start-ch start-ch) (lk lk) (ls ls))
   (precedes ((0 0) (5 0)) ((2 3) (1 0)) ((3 0) (2 0)) ((4 0) (1 2))
	     ((5 4) (2 1)) ((5 5) (0 1)))
   (uniq-orig k n)
   (gen-st (cat "st" d o o) (cat "st-k" d o k))
   (conf start-ch)
   (auth start-ch)
   ;;  (facts (same-dev ls lk) (no-state-split))
   (leads-to ((2 3) (1 1)) ((5 3) (1 0)) ((5 3) (2 2)))))
```

---

### `refrences/internet/examples_scm/sync_locn_envelope.scm`

*sha256:`c0dfe134ad6c` · 303 lines · 9.6 KB · lang:`scheme`*

```scheme
(herald "Envelope Protocol, location-based version"
   	;;   (reverse-nodes)
	;; (try-old-strands)
	(check-nonces)
	(bound 30)
	(limit 6000))

;;; This file analyzes the Envelope Protocol using three rules sets.
;;; For each rule set, it checks three scenarios.  In every scenario,
;;; an Alice strand runs to completion.  In the first scenario, the
;;; obtain token is listened for.  In the second, a listener for the
;;; refusal token is included.  In the third scenario, both listeners
;;; are included.  The third scenario should be impossible, but rules
;;; are required to accurately model state.
;;;
;;; The first rule set is empty and the answer to the third scenario
;;; shows a case is which the TPM's PCR state splits.  The second rule
;;; set forces TPM extends to be linearly ordered.  However, in this
;;; case, there are two TPMs when there should be one as Alice uses
;;; one TPM storage key to communicate with both TPMs.  The final rule
;;; set includes a rule about storage keys and thus accurately models
;;; state.
;;;
;;; Macros are used to avoid copying roles and scenarios.

;; This is the refusal token
(defmacro (refuse pcr-id n v k aik)
  (enc "quote" pcr-id (hash (hash "0" n) "refuse") (enc v k) aik))

;;; This protocol tracks the TPM's PCR state
;;; by sending a message with the current PCR
;;; value encrypted by a hashed secret key.
;;; The hash is used to prevent a confusion with
;;; the key for an encrypted session.

(defmacro (roles)
  (^
   ;; Power on sets the pcr to 0
   (defrole tpm-power-on
     (vars (current-value mesg) (pcr locn) (tpm chan))
     (trace
      (recv tpm "power on")
      (load pcr current-value)
      (stor pcr "0")))

   ;; The extend command takes the value to extend and the current PCR
   ;; value and produces the hash of the two values.
   ;;     (defrole tpm-extend
   ;;        (vars (value current-value mesg) (pcr locn))
   ;;        (trace
   ;;         (recv (cat "extend" value))
   ;;         (recv pcr current-value)		    ;; MSR lhs (deleted)
   ;;         (stor pcr (hash current-value value)) ;; MSR rhs
   ;;         (send "ext ok")))

   ;; The extend command can also occur within an
   ;; encrypted session.  We assume some session key already exists
   (defrole tpm-extend-enc
     (vars (value current-value mesg) (pcr-id nonce text) (pcr locn) (tpm chan))
     (trace
      (send tpm (cat "token" nonce))
      (recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))
      (load pcr current-value)		    ;; MSR lhs (deleted)
      (stor pcr (hash current-value value)) ;; MSR rhs
      (send "ext ok"))
     (uniq-orig nonce))

   ;; The TPM must retrieve the current pcr value.  Notice that
   ;; the nonce is of sort mesg, which allows non-atomic values.
   (defrole tpm-quote
     (vars (nonce current-value mesg) (pcr-id text) (aik akey) (pcr locn) (tpm chan))
     (trace
      (recv tpm (cat "quote" pcr-id nonce))
      (load pcr current-value) ;; MSR lhs (not deleted)
      (send (enc "quote" pcr-id current-value nonce aik))))

   ;; This role creates a key whose use is restricted to a
   ;; requested pcr value (since we only model one pcr).
   ;; It doesn't create or change any TPM state.
   (defrole tpm-create-key
     (vars (k aik akey) (pcr-id text) (pcrval mesg) (tpm chan))
     (trace
      (recv tpm (cat "create-req" pcr-id pcrval))
      (send (enc "created" k pcr-id pcrval aik))) ;; no tpm state is set
     (uniq-orig k)
     (non-orig (invk k))
     (auth tpm)			; Weird shapes without auth
     )

   ;; This role receives an encryption and a previously
   ;; made key structure that restricts the decryption key
   ;; to be used with a certain pcr value.  It retrieves the
   ;; current value and checks that it matches before decrypting.
   (defrole tpm-decrypt
     (vars (m current-value mesg) (pcr-id text) (k aik akey) (pcr locn) (tpm chan))
     (trace
      (recv tpm (cat "decrypt" (enc m k)))
      (recv (enc "created" k pcr-id current-value aik))
      (load pcr current-value) ;; MSR lhs (not deleted)
      (send m))
     (non-orig aik))

   ;; Alice extends a pcr with a fresh nonce in an encrypted
   ;; session.  She has the TPM create a new key whose use is
   ;; bound to the hash of pcr value she just created with the
   ;; string "obtain".  She then encrypts her fresh secret with
   ;; this newly created key.
   (defrole alice
     (vars (n v data) (pcr-id nonce text) (k aik akey) (tpm tpmconf chan))
     (trace
      (recv tpm (cat "token" nonce))
      (send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))
      (send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))
      ;; (enc "create key" (hash (hash "0" n) "obtain") esk)
      (recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))
      (send (enc v k)))
     (neq (k aik))
     (uniq-orig n v)
     (non-orig aik)
     (conf tpmconf))))

(defmacro (genStV-rules)
  (^

;;      (defrule genStV-if-hashed-tpm-extend
;;        (forall
;;         ((z strd) (v1 v2 mesg))
;;         (implies
;;          (and
;;   	(p "tpm-extend" z 2)
;;   	(p "tpm-extend" "current-value" z (hash v1 v2)))
;;          (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-power-on
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-power-on" z 2)
	(p "tpm-power-on" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-extend-enc
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-extend-enc" z 3)
	(p "tpm-extend-enc" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-decrypt
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-decrypt" z 3)
	(p "tpm-decrypt" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-quote
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-quote" z 2)
	(p "tpm-quote" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

;;      (defrule genStV-not-catted-tpm-power-on
;;        (forall
;;         ((z strd) (v1 v2 mesg))
;;         (implies
;;          (and
;;   	(p "tpm-power-on" z 2)
;;   	(p "tpm-power-on" "current-value" z (cat v1 v2)))
;;          (false))))
;;
;;      (defrule genStV-not-catted-tpm-extend-enc
;;        (forall
;;         ((z strd) (v1 v2 mesg))
;;         (implies
;;          (and
;;   	(p "tpm-extend-enc" z 2)
;;   	(p "tpm-extend-enc" "current-value" z (cat v1 v2)))
;;          (false))))
;;
;;      (defrule genStV-not-catted-tpm-decrypt
;;        (forall
;;         ((z strd) (v1 v2 mesg))
;;         (implies
;;          (and
;;   	(p "tpm-decrypt" z 3)
;;   	(p "tpm-decrypt" "current-value" z (cat v1 v2)))
;;          (false))))
;;
;;      (defrule genStV-not-catted-tpm-quote
;;        (forall
;;         ((z strd) (v1 v2 mesg))
;;         (implies
;;          (and
;;   	(p "tpm-quote" z 2)
;;   	(p "tpm-quote" "current-value" z (cat v1 v2)))
   ;;          (false))))
   ))

(defprotocol envelope basic
  (roles)
  (genStV-rules)
  )

(defskeleton envelope
  (vars (v data))
  (deflistener v)
  (defstrand alice 5 (v v)))

(defskeleton envelope
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (deflistener v)
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (deflistener v)
  (defstrand alice 5 (n n) (v v) (k k) (aik aik))
  (facts (no-state-split)))

;;   (defprotocol envelope-plus basic
;;     (roles)
;;     (genStV-rules)
;;
;;     (defrule ordered-extends
;;       (forall ((y z strd) (pcr locn))
;;   	    (implies
;;   	     (and (p "tpm-extend-enc" y 4)
;;   		  (p "tpm-extend-enc" z 4)
;;   		  (p "tpm-extend-enc" "pcr" y pcr)
;;   		  (p "tpm-extend-enc" "pcr" z pcr))
;;   	     (or (= y z)
;;   		 (prec y 3 z 2)
;;   		 (prec z 3 y 2))))))
;;
;;
;;   (defskeleton envelope-plus
;;     (vars (v data))
;;     (deflistener v)
;;     (defstrand alice 5 (v v)))
;;
;;   (defskeleton envelope-plus
;;     (vars (n v data) (k aik akey) (pcr-id text))
;;     (deflistener (refuse pcr-id n v k aik))
;;     (defstrand alice 5 (n n) (v v) (k k) (aik aik)))
;;
;;   (defskeleton envelope-plus
;;     (vars (n v data) (k aik akey) (pcr-id text))
;;     (deflistener (refuse pcr-id n v k aik))
;;     (deflistener v)
;;     (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

(comment (defprotocol envelope-plus-2 basic
	   (roles)
	   (genStV-rules)

	   (defrule pcr-id-identifies-pcr
	     (forall ((y z strd) (pcr-id text) (pcr pcr-0 locn))
		     (implies
		      (and (p "tpm-extend-enc" y 3)
			   (p "tpm-extend-enc" z 3)
			   (p "tpm-extend-enc" "pcr-id" y pcr-id)
			   (p "tpm-extend-enc" "pcr-id" z pcr-id)
			   (p "tpm-extend-enc" "pcr" y pcr)
			   (p "tpm-extend-enc" "pcr" z pcr-0))
		      (= pcr pcr-0)))))

	 (defskeleton envelope-plus-2
	   (vars (v data))
	   (deflistener v)
	   (defstrand alice 5 (v v)))

	 (defskeleton envelope-plus-2
	   (vars (n v data) (k aik akey) (pcr-id text))
	   (deflistener (refuse pcr-id n v k aik))
	   (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

	 (defskeleton envelope-plus-2
	   (vars (n v data) (k aik akey) (pcr-id text))
	   (deflistener (refuse pcr-id n v k aik))
	   (deflistener v)
	   (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

	 (defskeleton envelope-plus-2
	   (vars (n v data) (k aik akey) (pcr-id text))
	   (deflistener (refuse pcr-id n v k aik))
	   (deflistener v)
	   (defstrand alice 5 (n n) (v v) (k k) (aik aik))
	   (facts (no-state-split))))
```

---

### `refrences/internet/examples_scm/sync_locn_envelope_no_auth.scm`

*sha256:`e234dfddd0b0` · 299 lines · 9.2 KB · lang:`scheme`*

```scheme
(herald "Envelope Protocol, location-based version"
   	;;   (reverse-nodes)
	;;   (try-old-strands)
	(check-nonces)
	(bound 30)
	(limit 6000)) 

;;; This file analyzes the Envelope Protocol using three rules sets.
;;; For each rule set, it checks three scenarios.  In every scenario,
;;; an Alice strand runs to completion.  In the first scenario, the
;;; obtain token is listened for.  In the second, a listener for the
;;; refusal token is included.  In the third scenario, both listeners
;;; are included.  The third scenario should be impossible, but rules
;;; are required to accurately model state.
;;;
;;; The first rule set is empty and the answer to the third scenario
;;; shows a case is which the TPM's PCR state splits.  The second rule
;;; set forces TPM extends to be linearly ordered.  However, in this
;;; case, there are two TPMs when there should be one as Alice uses
;;; one TPM storage key to communicate with both TPMs.  The final rule
;;; set includes a rule about storage keys and thus accurately models
;;; state.
;;;
;;; Macros are used to avoid copying roles and scenarios.

;; This is the refusal token
(defmacro (refuse pcr-id n v k aik)
  (enc "quote" pcr-id (hash (hash "0" n) "refuse") (enc v k) aik))

;;; This protocol tracks the TPM's PCR state
;;; by sending a message with the current PCR
;;; value encrypted by a hashed secret key.
;;; The hash is used to prevent a confusion with
;;; the key for an encrypted session.

(defmacro (roles)
  (^
   ;; Power on sets the pcr to 0
   (defrole tpm-power-on 
     (vars (current-value mesg) (pcr locn) (tpm chan)) 
     (trace
      (recv tpm "power on")
      (load pcr current-value) 
      (stor pcr "0")))

   ;; The extend command takes the value to extend and the current PCR
   ;; value and produces the hash of the two values.
   ;;     (defrole tpm-extend
   ;;        (vars (value current-value mesg) (pcr locn))
   ;;        (trace
   ;;         (recv (cat "extend" value))
   ;;         (recv pcr current-value)		    ;; MSR lhs (deleted)
   ;;         (stor pcr (hash current-value value)) ;; MSR rhs
   ;;         (send "ext ok")))

   ;; The extend command can also occur within an
   ;; encrypted session.  We assume some session key already exists
   (defrole tpm-extend-enc
     (vars (value current-value mesg) (pcr-id nonce text) (pcr locn) (tpm chan))
     (trace
      (send tpm (cat "token" nonce))
      (recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))
      (load pcr current-value)		    ;; MSR lhs (deleted)
      (stor pcr (hash current-value value)) ;; MSR rhs
      (send "ext ok"))
     (uniq-orig nonce))

   ;; The TPM must retrieve the current pcr value.  Notice that
   ;; the nonce is of sort mesg, which allows non-atomic values.
   (defrole tpm-quote
     (vars (nonce current-value mesg) (pcr-id text) (aik akey) (pcr locn) (tpm chan))
     (trace
      (recv tpm (cat "quote" pcr-id nonce))
      (load pcr current-value) ;; MSR lhs (not deleted)
      (send (enc "quote" pcr-id current-value nonce aik))))

   ;; This role creates a key whose use is restricted to a
   ;; requested pcr value (since we only model one pcr).
   ;; It doesn't create or change any TPM state.
   (defrole tpm-create-key
     (vars (k aik akey) (pcr-id text) (pcrval mesg) (tpm chan))
     (trace
      (recv tpm (cat "create-req" pcr-id pcrval))
      (send (enc "created" k pcr-id pcrval aik))) ;; no tpm state is set
     (uniq-orig k)
     (non-orig (invk k))
     ;; (auth tpm)			; Weird shapes without auth 
     )
   
   ;; This role receives an encryption and a previously
   ;; made key structure that restricts the decryption key
   ;; to be used with a certain pcr value.  It retrieves the
   ;; current value and checks that it matches before decrypting.
   (defrole tpm-decrypt
     (vars (m current-value mesg) (pcr-id text) (k aik akey) (pcr locn) (tpm chan))
     (trace
      (recv tpm (cat "decrypt" (enc m k)))
      (recv (enc "created" k pcr-id current-value aik))
      (load pcr current-value) ;; MSR lhs (not deleted)
      (send m))
     (non-orig aik))

   ;; Alice extends a pcr with a fresh nonce in an encrypted
   ;; session.  She has the TPM create a new key whose use is
   ;; bound to the hash of pcr value she just created with the
   ;; string "obtain".  She then encrypts her fresh secret with
   ;; this newly created key.
   (defrole alice
     (vars (n v data) (pcr-id nonce text) (k aik akey) (tpm tpmconf chan))
     (trace
      (recv tpm (cat "token" nonce))
      (send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))
      (send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))
      ;; (enc "create key" (hash (hash "0" n) "obtain") esk)
      (recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))
      (send (enc v k)))
     (neq (k aik))
     (uniq-orig n v)
     (non-orig aik)
     (conf tpmconf))))

(defmacro (genStV-rules)
  (^
   
;;      (defrule genStV-if-hashed-tpm-extend 
;;        (forall
;;         ((z strd) (v1 v2 mesg))
;;         (implies
;;          (and
;;   	(p "tpm-extend" z 2)
;;   	(p "tpm-extend" "current-value" z (hash v1 v2)))
;;          (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-power-on
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-power-on" z 2)
	(p "tpm-power-on" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-extend-enc 
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-extend-enc" z 3)
	(p "tpm-extend-enc" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-decrypt
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-decrypt" z 3)
	(p "tpm-decrypt" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

   (defrule genStV-if-hashed-tpm-quote
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-quote" z 2)
	(p "tpm-quote" "current-value" z (hash v1 v2)))
       (gen-st (hash v1 v2)))))

   (defrule genStV-not-catted-tpm-power-on
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-power-on" z 2)
	(p "tpm-power-on" "current-value" z (cat v1 v2)))
       (false))))

   (defrule genStV-not-catted-tpm-extend-enc 
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-extend-enc" z 2)
	(p "tpm-extend-enc" "current-value" z (cat v1 v2)))
       (false))))

   (defrule genStV-not-catted-tpm-decrypt
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-decrypt" z 3)
	(p "tpm-decrypt" "current-value" z (cat v1 v2)))
       (false))))

   (defrule genStV-not-catted-tpm-quote
     (forall
      ((z strd) (v1 v2 mesg))
      (implies
       (and
	(p "tpm-quote" z 2)
	(p "tpm-quote" "current-value" z (cat v1 v2)))
       (false))))))


(defprotocol envelope basic
  (roles)
  (genStV-rules)
  )


(defskeleton envelope
  (vars (v data))
  (deflistener v)
  (defstrand alice 5 (v v)))

(defskeleton envelope
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (deflistener v)
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

(defprotocol envelope-plus basic
  (roles)
  (genStV-rules)

  (defrule ordered-extends
    (forall ((y z strd) (pcr locn))
	    (implies
	     (and (p "tpm-extend-enc" y 4)
		  (p "tpm-extend-enc" z 4)
		  (p "tpm-extend-enc" "pcr" y pcr)
		  (p "tpm-extend-enc" "pcr" z pcr))
	     (or (= y z)
		 (prec y 3 z 2)
		 (prec z 3 y 2))))))


(defskeleton envelope-plus
  (vars (v data))
  (deflistener v)
  (defstrand alice 5 (v v)))

(defskeleton envelope-plus
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope-plus
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (deflistener v)
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))


(defprotocol envelope-plus-2 basic
  (roles)
  (genStV-rules)

  (defrule pcr-id-identifies-pcr 
    (forall ((y z strd) (pcr-id text) (pcr pcr-0 locn))
	    (implies
	     (and (p "tpm-extend-enc" y 3)
		  (p "tpm-extend-enc" z 3)
		  (p "tpm-extend-enc" "pcr-id" y pcr-id) 
		  (p "tpm-extend-enc" "pcr-id" z pcr-id)
		  (p "tpm-extend-enc" "pcr" y pcr)
		  (p "tpm-extend-enc" "pcr" z pcr-0))
	     (= pcr pcr-0))))) 

(defskeleton envelope-plus-2
  (vars (v data))
  (deflistener v)
  (defstrand alice 5 (v v)))

(defskeleton envelope-plus-2
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

(defskeleton envelope-plus-2
  (vars (n v data) (k aik akey) (pcr-id text))
  (deflistener (refuse pcr-id n v k aik))
  (deflistener v)
  (defstrand alice 5 (n n) (v v) (k k) (aik aik)))

;;   
;;   make -k sync_locn_envelope_no_auth.xhtml 
;;   time  cpsa4 +RTS -M512m -N -RTS -o sync_locn_envelope_no_auth.txt sync_locn_envelope_no_auth.scm
;;       15598.90 real     42296.24 user       173.50 sys
;;   cpsa4graph  -o sync_locn_envelope_no_auth.xhtml sync_locn_envelope_no_auth.txt
;;   
;;   Compilation finished at Wed Apr 22 18:19:28
```

---

### `refrences/internet/examples_scm/targetterms1.scm`

*sha256:`c2c1a27820ba` · 21 lines · 0.6 KB · lang:`scheme`*

```scheme
;; Solution requires the use of target terms in the solved filter.

;; The protocol is strange because the initiator sends out two texts
;; that turn out must be the same.

(defprotocol targetterms basic
  (defrole init (vars (a skey) (n1 n2 text) (k akey))
    (trace
     (send (enc n1 (enc a n2 k) k))
     (recv (enc a n1 k))))

  (defrole resp (vars (n1 text) (m mesg) (k akey))
    (trace
     (recv (enc n1 m k))
     (send m))))

(defskeleton targetterms
  (vars (n1 text) (k akey))
  (defstrand init 2 (n1 n1) (k k))
  (non-orig (invk k))
  (uniq-orig n1))
```

---

### `refrences/internet/examples_scm/targetterms2.scm`

*sha256:`1910a7315f43` · 36 lines · 1.3 KB · lang:`scheme`*

```scheme
;;; Target terms experiment
;  The aim of this "experiment" was to try to create an instance
; where we would want to do an augmentation where (1) the critical
; term is to appear in a variable of sort mesg in the transforming
; node and moreover (2) the target term we'd like to use is a
; subterm of what is currently a variable of sort mesg in the
; escape set.
;  This was not wholly successful.  However, targetterms2 did
; illustrate something interesting: a lack of factoring all homomorphisms
; through members of the cohort.  We could have the init2 strand and a
; mostly generic trans strand, and there are two trans strands in the
; shape.  There are two homomorphisms, then, but only one factored through
; what happened next, because the only next step was a contraction that
; effectively fixed our idea of which trans strand we had.

(defprotocol targetterms2 basic
  (defrole init (vars (a name) (n text))
    (trace
	(send (enc n (pubk a)))
      (recv (enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a)))
    )
    (uniq-orig n)
    (non-orig (privk a))
)
  (defrole trans (vars (a name) (n text) (m mesg))
    (trace
     (recv (enc n (pubk a)))
     (recv m)
     (send (enc n m (pubk a)))
    ))
)

(defskeleton targetterms2
  (vars (a name) (n text))
  (defstrand init 2 (a a) (n n))
)
```

---

### `refrences/internet/examples_scm/targetterms6.scm`

*sha256:`4a93026b8f2e` · 56 lines · 2.2 KB · lang:`scheme`*

```scheme
;;; Target terms experiment
;
;  After a series of other experiments on target terms
; this example arose, and it demonstrated two serious bugs
; in CPSA.
;  First, before this example, CPSA was looking for contractions
; that would completely realize a test node (at least, with respect
; to one critical message).  In this example, the unrealized node
; is the second node of the init strand, and the only critical
; message is the nonce n.  Only if TWO instances of trans were
; available, both with variable m unbound, could we completely
; solve the reception with a single substitution.  However, we can't
; have two instances of trans that are so generic, if we are
; to terminate in circumstances like these (similar to the pruning
; necessary to make Needham-Schroeder terminate).  The fix is to
; make contractions solve only one *position* of the critical
; message at a time.
;  The other problem arose when we added that fix - CPSA was still
; unable to find the shape.  This time, the problem was that pruning
; was overly aggressive: we had an instance of trans in which m had
; been bound, and another version in which m had not.  There was a
; homomorphism and all other conditions were satisfied but the pruning
; was not justified, because the new copy of the trans strand retained
; the freedom to have m map to something not unifiable with the binding
; of m in the other strand.

(defprotocol targetterms6 basic
  (defrole init (vars (a name) (n text) (m mesg))
    (trace
	(send (enc n (pubk a)))
      (recv (cat (enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a))
         (enc n (enc n (pubk a)) (pubk a)) ))
    )
    (uniq-orig n)
    (non-orig (privk a))
)
  (defrole trans (vars (a name) (n text) (m mesg))
    (trace
     (recv (enc n (pubk a)))
     (recv m)
     (send (enc n m (pubk a)))
    ))
)

(defskeleton targetterms6
  (vars (a name) (n text))
  (defstrand init 2 (a a) (n n))
)

(defskeleton targetterms6
  (vars (n text) (a name))
  (defstrand init 2 (n n) (a a))
  (defstrand trans 3 (m (enc n (pubk a))) (n n) (a a))
  (defstrand trans 3 (m (enc n (enc n (pubk a)) (pubk a))) (n n) (a a))
  (precedes ((0 0) (1 0)) ((0 0) (2 0)) ((1 2) (2 1)) ((2 2) (0 1)))
)
```

---

### `refrences/internet/examples_scm/targetterms8.scm`

*sha256:`25e015e83177` · 64 lines · 2.2 KB · lang:`scheme`*

```scheme
;;; Target terms experiment
;
;  This example demonstrates the need for the solved filter condition "2a",
; which we had suspected was necessary for months but until now we were not
; sure.
;
;
;  The initiator sends out an encryption {|n1 {|a n2|} |}, with both levels
; of encryption being under an asymmetric key whose inverse is assumed to be
; non-originating.  n1 is freshly chosen.  The initiator expects to receive
; {|a n1|}.
;
;  The responder takes {|n1 {|m|} |} and outputs {|m|}.
;
;  The initial POV (which is just the init 2 role) is dead because we don't
; have condition 2a in the solved predicate.  If we did, we could try an
; augmentation or displacement for a length-1 init strand with n1 being
; used as the value for n2.  Hulling would require that this unify with the
; existing init strand, and the result would be an init strand in which n1
; and n2 are unified.  (Our second POV is this skeleton).
;
;  However, the escape set after this map is no bigger than it was; it consists
; of only {|n1 {|a n1|} |}, which is in the image of the old escape set, so
; we don't meet condition 2.  We do meet condition 2a, since the target term
; (a n1) is not an image of any old target term (the old target terms were only
; n1 and (n1 {|a n2|}).
;
;  Note that the first POV is dead (in CPSA 2.2.2) but the second POV is not,
; and leads to a shape.

(defprotocol targetterms8 basic
  (defrole init (vars (a name) (n1 n2 text) (k akey))
    (trace
	(send (enc n1 (enc a n2 k) k))
      (recv (enc a n1 k))
    )
    (uniq-orig n1)
    (non-orig (invk k))
)
  (defrole resp (vars (n1 text) (m mesg) (k akey))
    (trace
     (recv (enc n1 (enc m k) k))
     (send (enc m k))
    ))
)

(comment First POV)
(defskeleton targetterms8
  (vars (a name) (n1 n2 text) (k akey))
  (defstrand init 2 (a a) (n1 n1) (n2 n2) (k k))
)

(comment Second POV)
(defskeleton targetterms8
  (vars (a name) (n1 text) (k akey))
  (defstrand init 2 (a a) (n1 n1) (n2 n1) (k k))
)

(comment "This is the shape.  We don't need it because we find it from the second POV.")
(comment (defskeleton targetterms8
  (vars (a name) (n1 text) (k akey) )
  (defstrand init 2 (a a) (n1 n1) (n2 n1) (k k))
  (defstrand resp 2 (n1 n1) (k k) (m (cat a n1)))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))))
```

---

### `refrences/internet/examples_scm/thisthat.scm`

*sha256:`ff8fb574f088` · 31 lines · 0.9 KB · lang:`scheme`*

```scheme
(herald "Needham-Schroeder Public-Key Protocol This-That Variant")

(defprotocol thisthat basic
  (defrole init
    (vars (a b name) (n1 n2 n3 text))
    (trace
     (send (enc n1 a (pubk b)))
     (recv (cat (enc n1 n2 (pubk a)) (enc n1 n3 (pubk a))))
     (recv (cat (enc "this" n2 (pubk b)) (enc "that" n3 (pubk b))))))
  (defrole this
    (vars (b a name) (n2 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n2 (pubk a)))
     (send (enc "this" n2 (pubk b))))
    (uniq-orig n2))
  (defrole that
    (vars (b a name) (n3 n1 text))
    (trace
     (recv (enc n1 a (pubk b)))
     (send (enc n1 n3 (pubk a)))
     (send (enc "that" n3 (pubk b))))
    (uniq-orig n3)))

;;; The initiator point-of-view
(defskeleton thisthat
  (vars (a b name) (n1 text))
  (defstrand init 3 (a a) (b b) (n1 n1))
  (non-orig (privk b) (privk a))
  (uniq-orig n1)
  (comment "Initiator point-of-view"))
```

---

### `refrences/internet/examples_scm/tickle-unique.scm`

*sha256:`7a2222c13440` · 39 lines · 0.8 KB · lang:`scheme`*

```scheme
(herald tickle-unique)

(defprotocol tickle basic
  (defrole init
    (vars (a b name) (na nb text))
    (trace
     (send (enc a na (pubk b)))
     (recv (enc b na na nb (pubk a)))
     (send nb))
    (uniq-orig na))

  (defrole resp
    (vars (a b name) (na nb0 nb text))
    (trace
     (recv (enc a na (pubk b)))
     (send (enc b na nb0 nb (pubk a)))
     (recv nb)))

  (defrule uniq-tickle
    (forall
     ((z strd) (nb0 text))
     (implies
      (and (fact guard-me)
	   (p "resp" z 2)
	   (p "resp" "nb0" z nb0))
      (uniq nb0)))))

(defskeleton tickle
  (vars (a b name) (na nb0 nb text))
  (defstrand resp 3 (a a) (b b) (nb0 nb0) (nb nb))
  (non-orig (privk a))
  (uniq-orig nb))

(defskeleton tickle
  (vars (a b name) (na nb0 nb text))
  (defstrand resp 3 (a a) (b b) (nb0 nb0) (nb nb))
  (facts (guard-me))
  (non-orig (privk a))
  (uniq-orig nb))
```

---

### `refrences/internet/examples_scm/timestamping.scm`

*sha256:`82003a7aeb20` · 46 lines · 1.4 KB · lang:`scheme`*

```scheme
(herald timestamping-service)

;; Timestamping service as described on Page 76 in Applied
;; Cryptography, Second Edition by Bruce Schneier.

;; This version DOES NOT send the identity of timestamp holder that
;; follows the one sent to the client.  It's a to do.

(defmacro (link)
  (cat alice_1 h_1 t_1 l_1))

(defmacro (timestamp l)
  (enc n alice h alice_1 h_1 t_1 l (privk trent)))

(defprotocol timestamping-service basic
  (defrole client (vars (alice alice_1 trent name)
  			(n data) (h h_1 text) (t_1 l mesg))
    (trace
     (send (cat h alice))
     (recv (timestamp l))))
  (defrole server (vars (alice alice_1 trent name)
			(n data) (h h_1 text) (t_1 l_1 mesg))
    (trace
     (recv (cat (enc (enc (link) (privk trent)) (pubk trent)) h alice))
     (send (cat (timestamp (hash (link)))
		(enc
		 (enc (hash alice h (timestamp (hash (link))) (hash (link)))
		      (privk trent))
		 (pubk trent)))))
    (uniq-orig n))
  (defrole origin (vars (alice alice_1 trent name)
  			(n data) (h h_1 text) (t_1 l_1 text))
    (trace
     (recv (enc (enc n (privk trent)) (pubk trent)))
     (send (enc
	    (enc alice h (timestamp (hash (link))) (hash (link))
		 (privk trent))
	    (pubk trent)))))
  (defrole big-bang (vars (n data) (trent name))
    (trace (send (enc (enc n (privk trent)) (pubk trent))))
    (uniq-orig n)))

(defskeleton timestamping-service
  (vars (trent name) (n_0 data))
  (defstrand client 2 (trent trent))
  (non-orig (privk trent)))
```

---

### `refrences/internet/examples_scm/trust-anchor.scm`

*sha256:`29e459309918` · 19 lines · 0.5 KB · lang:`scheme`*

```scheme
(herald trust-anchor
	(comment "Tests rule application on initial skeleton"))

(defprotocol trust-anchor basic
  ;;; trust-anchor property guarantees non
  (defrule trust-anchor-inverse-is-non
    (forall ((k akey))
	    (implies (fact trust-anchor k)
		     (non (invk k))))))

(defskeleton trust-anchor
  (vars (f ca name))
  (deflistener (enc f (pubk f) (privk ca)))
  (non-orig (privk ca)))

(defskeleton trust-anchor
  (vars (f ca name))
  (deflistener (enc f (pubk f) (privk ca)))
  (facts (trust-anchor (pubk ca))))
```

---

### `refrences/internet/examples_scm/ugen-at.scm`

*sha256:`b5797b5eddf5` · 53 lines · 1.3 KB · lang:`scheme`*

```scheme
(herald uniq-at)

(defprotocol yahalom-plus-uniq-at basic 

  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey))
    (trace (send (cat a n-a))
	   (recv (enc b k n-a n-b (ltk a c)))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (rest mesg) (k skey))
    (trace (recv (cat a n-a))
	   (send (cat b (enc a n-a n-b (ltk b c))))
	   (recv (cat (enc a k (ltk b c)) rest))
	   (send rest) 
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey))
    (trace (recv (cat b (enc a n-a n-b (ltk b c))))
	   (send (cat (enc a k (ltk b c))
		      (enc b k n-a n-b (ltk a c)))))
    (uniq-gen k))

  (defrule uniq-at
    (forall
     ((z strd) (i indx) (v mesg))
     (implies (uniq-at v z i)
	      (fact remember v z))))

  (defrule ugen-at
    (forall
     ((z strd) (i indx) (v mesg))
     (implies (ugen-at v z i)
	      (fact remember-gen v z)))))

(defskeleton yahalom-plus-uniq-at
  (vars (a b c name) (n-b text) (k skey))
  (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk b c) (ltk a c))
  (uniq-gen n-b))

(defskeleton yahalom-plus-uniq-at
  (vars (a b c name) (n-a text))
  (defstrand init 3 (n-a n-a) (a a) (b b) (c c))
  (non-orig (ltk b c) (ltk a c))
  (uniq-gen n-a))





  
```

---

### `refrences/internet/examples_scm/ugo.scm`

*sha256:`a9bb4281d911` · 110 lines · 2.8 KB · lang:`scheme`*

```scheme
(herald uniq-gen-and-orig-example
	(comment "Non-executable role examples"))

;;; These two protocols show examples where generation and origination
;;; of asymmetric key pairs lead to shapes that cannot be
;;; implemented.  Note that key pairs must generate or originate at
;;; the same node in a skeleton.

;;; CPSA computes the shapes that would be possible, assuming that the
;;; responder, given u, could magically determine (invk u).
;;; Presumably, the specifier who writes a protocol like this is
;;; committed to this possibility.  I.e. we consider this the
;;; specifier's responsibility to avoid, not CPSA's responsibility to
;;; detect.  

(defprotocol uniq-gen-example basic
  (defrole init
    (vars (u akey) (k skey))
    (trace
     (send (enc u k))
     (recv (invk u))
     (send u))
    (uniq-gen u)
    (non-orig k)
    (comment
     "Instances of this role generate u and (invk u)"
     "at their first event."))
  (defrole resp
    (vars (u akey) (k skey))
    (trace
     (recv (enc u k))
     (send (invk u))
     (recv u))
    (non-orig k)
    (comment
     "Instances of this role appear to generate (invk u)"
     "at their second event.")))

(defskeleton uniq-gen-example
  (vars)
  (defstrandmax resp)
  (comment "How is the responder able to send (invk u)?"))

(defskeleton uniq-gen-example
  (vars (u akey))
  (defstrandmax resp (u u))
  (uniq-gen (invk u))
  (comment "How is the responder able to send (invk u)?"))


(defprotocol uniq-gen-example-alt basic
  (defrole init
    (vars (u akey) (k skey))
    (trace
     (send (enc (invk u) k))
     (recv u)
     (send u))
    (uniq-gen (invk u))
    (non-orig k)
    (comment
     "Instances of this role generate u and (invk u)"
     "at their first event."))
  (defrole resp
    (vars (u akey) (k skey))
    (trace
     (recv (enc (invk u) k))
     (send u)
     (recv u))
    (non-orig k)
    (comment
     "Instances of this role appear to generate (invk u)"
     "at their second event.")))

(defskeleton uniq-gen-example-alt 
  (vars)
  (defstrandmax resp)
  (comment "How is the responder able to send (invk u)?"))

(defskeleton uniq-gen-example-alt 
  (vars (u akey))
  (defstrandmax resp (u u))
  (uniq-gen (invk u))
  (comment "How is the responder able to send (invk u)?"))

(defprotocol uniq-orig-example basic
  (defrole init
    (vars (u akey) (k skey))
    (trace
     (send (enc u k))
     (recv (invk u))
     (send u))
    (uniq-orig u)
    (non-orig k))
  (defrole resp
    (vars (u akey) (k skey))
    (trace
     (recv (enc u k))
     (send (invk u))
     (recv u))
    (non-orig k))
  (comment "Similar to the above, but with uniq-orig instead of uniq-gen."))

(defskeleton uniq-orig-example
  (vars)
  (defstrandmax resp))

(defskeleton uniq-orig-example
  (vars (u akey))
  (defstrandmax resp (u u))
  (uniq-orig (invk u)))
```

---

### `refrences/internet/examples_scm/uncarried_keys.scm`

*sha256:`f8f5a1fac5e9` · 30 lines · 0.9 KB · lang:`scheme`*

```scheme
; uncarried-keys
;   Shows that our notion of uniquely-originating
; does not necessarily correspond to the notion of
; a freshly-generated nonce, because such values can
; be used in non-carried positions before they are
; received.  Here, the initiator originates K in its
; 4th message but receives (earlier) a message
; encrypted with K from the responder.

(defprotocol uncarried-keys basic
  (defrole init
    (vars (a text) (A B name) (K akey))
    (trace
     (send (enc "start" a A B (pubk B)))
     (recv (enc a A B (pubk A)))
     (send (enc a K (pubk B)))
     (recv (enc a A B K)))
    (non-orig (privk B) (invk K))
    (uniq-orig a K))
  (defrole resp
    (vars (a text) (A B name) (K akey))
    (trace
     (recv (enc "start" a A B (pubk B)))
     (send (enc a A B (pubk A)))
     (recv (enc a K (pubk B)))
     (send (enc a A B K)))))

(defskeleton uncarried-keys
  (vars (a text) (A B name) (K akey))
  (defstrand init 4 (a a) (A A) (B B) (K K)))
```

---

### `refrences/internet/examples_scm/unilateral.scm`

*sha256:`3f30672cadd0` · 89 lines · 2.3 KB · lang:`scheme`*

```scheme
(herald unilateral)

(defprotocol unilateral basic
  (defrole init
     (vars (n text) (k akey))
     (trace
      (send (enc n k))
      (recv n))
     (uniq-orig n))
  (defrole resp
     (vars (n text) (k akey))
     (trace
      (recv (enc n k))
      (send n))))

(defskeleton unilateral
   (vars (k akey))
   (defstrand init 2 (k k))
   (non-orig (invk k)))

(defskeleton unilateral
   (vars (n text) (k akey))
   (defstrand resp 2 (n n) (k k))
   (pen-non-orig n)
   (non-orig (invk k)))

;;; The same two problems posed using security goals.  The goals were
;;; taken from the output of cpsasas.

(defgoal unilateral
  (forall ((n text) (k akey) (z strd))
    (implies
      (and (p "init" z 2) (p "init" "n" z n) (p "init" "k" z k)
        (non (invk k)) (uniq-at n z 0))
      (exists ((z-0 strd))
        (and (p "resp" z-0 2) (p "resp" "n" z-0 n) (p "resp" "k" z-0 k)
          (prec z 0 z-0 0) (prec z-0 1 z 1))))))

(defgoal unilateral
  (forall ((n text) (k akey) (z strd))
    (implies
      (and (p "resp" z 2) (p "resp" "n" z n) (p "resp" "k" z k)
        (non (invk k)) (pnon n))
      (exists ((k-0 akey) (z-0 strd))
        (and (p "init" z-0 1) (p "init" "n" z-0 n)
          (p "init" "k" z-0 k-0) (prec z-0 0 z 0) (uniq-at n z-0 0))))))

;;; Unilateral authentication from ISO/IEC JTC 1/SC 27/WG 2 N1050

(defprotocol iso-unilateral basic
  (defrole resp
    (vars (na nb t1 t2 t3 text) (b name))
    (trace
     (recv (cat nb t1))
     (send (cat na nb b t3 (enc na nb b t2 (privk b)))))
    (uniq-orig na))
  (defrole init
    (vars (na nb t1 t2 t3 text) (b name))
    (trace
     (send (cat nb t1))
     (recv (cat na nb b t3 (enc na nb b t2 (privk b)))))
    (uniq-orig nb))
  (comment "Two pass authentication"))

(defskeleton iso-unilateral
  (vars (b name))
  (defstrand init 2 (b b))
  (non-orig (privk b)))

;;; Same as above, but also checking to see if there was agreement.
(defgoal iso-unilateral
  (forall ((b name) (z strd))
    (implies
     (and (p "init" z 2)
	  (p "init" "b" z b)
	  (non (privk b)))
      (exists ((y strd))
	      (and (p "resp" y 2)
		   (p "resp" "b" y b))))))

;;; Silly example.  Of course the shape produced does not satisfy this
;;; goal!
(defgoal iso-unilateral
  (forall ((b name) (z strd))
    (implies
     (and (p "init" z 2)
	  (p "init" "b" z b)
	  (non (privk b)))
     (false))))
```

---

### `refrences/internet/examples_scm/uniq-at.scm`

*sha256:`d8ec10d3158a` · 53 lines · 1.3 KB · lang:`scheme`*

```scheme
(herald uniq-at)

(defprotocol yahalom-plus-uniq-at basic 

  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey))
    (trace (send (cat a n-a))
	   (recv (enc b k n-a n-b (ltk a c)))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (rest mesg) (k skey))
    (trace (recv (cat a n-a))
	   (send (cat b (enc a n-a n-b (ltk b c))))
	   (recv (cat (enc a k (ltk b c)) rest))
	   (send rest) 
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey))
    (trace (recv (cat b (enc a n-a n-b (ltk b c))))
	   (send (cat (enc a k (ltk b c))
		      (enc b k n-a n-b (ltk a c)))))
    (uniq-orig k))

  (defrule uniq-at
    (forall
     ((z strd) (i indx) (v mesg))
     (implies (uniq-at v z i)
	      (fact remember v z))))

  (defrule ugen-at
    (forall
     ((z strd) (i indx) (v mesg))
     (implies (ugen-at v z i)
	      (fact remember-gen v z)))))

(defskeleton yahalom-plus-uniq-at
  (vars (a b c name) (n-b text) (k skey))
  (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))

(defskeleton yahalom-plus-uniq-at
  (vars (a b c name) (n-a text))
  (defstrand init 3 (n-a n-a) (a a) (b b) (c c))
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-a))





  
```

---

### `refrences/internet/examples_scm/uniq-gen-test.scm`

*sha256:`863bc5bd5cfd` · 35 lines · 0.8 KB · lang:`scheme`*

```scheme
(herald "Unique generation test protocols."
	(comment "Skeletons 2, 4, and 7 should have no shapes."))

(defprotocol uniqgentest basic
  (defrole init
    (vars (a name) (k skey))
    (trace
     (send (enc a k))
     (recv (enc a a k))))
  (defrole doubler
    (vars (a name) (k skey))
    (trace
     (send (enc a a k))))
  (defrole resp
    (vars (a name) (k skey))
    (trace
     (recv (enc a k))
     (send (enc a a k)))))

;; This input should have no shape, because
;; declaring k to be uniq-gen does not allow
;; a doubler strand: the doubler strand generates
;; its key.
(defskeleton uniqgentest
  (vars (k skey))
  (defstrand init 2 (k k))
  (uniq-gen k))

;; This input should have a shape in which a
;; doubler produces the message needed by the
;; initiator.
(defskeleton uniqgentest
  (vars (k skey))
  (defstrand init 2 (k k))
  (non-orig k))
```

---

### `refrences/internet/examples_scm/uo.scm`

*sha256:`4e212592b42d` · 25 lines · 0.7 KB · lang:`scheme`*

```scheme
; uniq-orig
;   Shows that our notion of uniquely-originating
; does not necessarily correspond to the notion of
; a freshly-generated nonce, because such values can
; be used in non-carried positions before they are
; received.  Here, the initiator originates n in its
; message but no problem is detected with a responder
; that sends a message encrypted under n as its first
; message, before receiving n.

(defprotocol uniq-orig basic
  (defrole init
    (vars (n text))
    (trace (send n))
    (uniq-orig n))
  (defrole resp
    (vars (m n text))
    (trace
     (send (enc m n))
     (recv n))))

(defskeleton uniq-orig
  (vars (n text))
  (defstrand init 1 (n n))
  (defstrand resp 2 (n n)))
```

---

### `refrences/internet/examples_scm/wang-hash.scm`

*sha256:`e49573e42a15` · 434 lines · 12.2 KB · lang:`scheme`*

```scheme
(herald "Wang's Fair Exchange Protocol" (bound 10))

;; CPSA input file to represent
;; Wang's Fair Exchange Protocol

;; This macro implements the CPSA
;; convention of regarding a hash as
;; an asymmetric encryption.  The
;; decryption key inverse to (pubk
;; hash) is assumed non-originating
;; in roles using hashing.

;; (defmacro (hash x)
;;  (enc "h" (cat "h" x)))

;; Wang's encrypted format for the
;; message payload.  Observe that m,
;; k get their values from the
;; like-named messages in the context
;; where the macro is expanded.

(defmacro (em)
  (enc m k))

;; The session label L as a fn of
;; the values that *should be* the
;; hashes of the encrypted message EM
;; and the session key K.

(defmacro (l-prime y x)
  (cat a b t y x))

;; The recipient can check that a
;; session label has an l-prime where
;; y is the hash of another parameter.
;; Hence recipient roles use l-star.

(defmacro (l-star e1 x)
  (l-prime (hash e1) x))

;; The Evidence of Origin is checked
;; to be this fn of other parameters
;; available to the recipient.

(defmacro (eoo-star x e1 e2)
  (enc (cat "eootag"
	    (hash (l-star e1 x)) e2)
       (privk "sign" a)))

;; The Evidence of Receipt is computed
;; as this fn of other parameters
;; available to the recipient.

(defmacro (eor-star x e1 e2)
  (enc (cat "eortag"
	    (hash (l-star e1 x)) e2)
       (privk "sign" b)))

;; The Recovery Request as computed by
;; the recipient.

(defmacro (rr-star x e1 e2)
  (cat (l-star e1 x) e2
       (eoo-star x e1 e2)
       (eor-star x e1 e2)
       (enc (cat "rcrq" (l-star e1 x) e2)
            (privk "sign" b))))

;; The Abort Token is checked
;; to be this fn of other parameters
;; available to the recipient.

(defmacro (at-star e1 x)
  (enc (enc "abrq" (l-star e1 x)
            (privk "sign" a))
       (privk "sign" t)))

;; How the initiator computes the
;; encrypted key package:

(defmacro (ek l)
  (enc (cat "keytag" (hash l) k r)
       (pubk "encr" t)))

;; The Initiator's computed
;; version of L.

(defmacro (l)
  (l-prime (hash (enc m k)) (hash k)))

;; The TTP can check that the session
;; label L is this fn of other
;; parameters available to the TTP.

(defmacro (l-prime-prime y)
  (cat a b t y (hash k)))

;; The TTP can check that the EOO
;; is this fn of other parameters
;; available to the TTP.

(defmacro (eoo-prime-prime y)
  (enc (cat "eootag"
            (hash (l-prime-prime y))
	    (ek (l-prime-prime y)))
       (privk "sign" a)))

;; The TTP can check that the EOR
;; is this fn of other parameters
;; available to the TTP.

(defmacro (eor-prime-prime y)
  (enc (cat "eortag"
	    (hash (l-prime-prime y))
	    (ek (l-prime-prime y)))
       (privk "sign" b)))

;; The TTP can check that the RR
;; is this fn of other parameters
;; available to the TTP.

(defmacro (rr-prime-prime y)
  (cat (l-prime-prime y)
       (ek (l-prime-prime y))
       (eoo-prime-prime y)
       (eor-prime-prime y)
       (enc "rcrq" (l-prime-prime y)
	    (ek (l-prime-prime y))
            (privk "sign" b))))

;; The TTP can check that the Confirmation
;; Request is this fn of other parameters
;; available to the TTP.

(defmacro (cf-prime-prime y)
  (cat (l-prime-prime y) (ek (l-prime-prime y))
       (eoo-prime-prime y) (eor-prime-prime y)
       (enc "cfrq" (l-prime-prime y)
	    (ek (l-prime-prime y))
            (privk "sign" b))))

;; Defn of Wang's Fair Exchange Protocol.
;; Closely follows the presentation in the
;; figures in Section 3.  In the TTP roles,
;; we have put a dummy send or receive in place
;; of the state synchronization event to keep
;; the indices matching the spec.

(defprotocol wang basic

  ;; Successful initiator run with no TTP involvement

  (defrole init1
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (recv (eor-star (hash k) (enc m k) (ek (l))))
     (send (cat k r)))
    (non-orig (privk hash_id)))

  ;; Aborted initiator run

  (defrole init2
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (enc "abcf"
                (enc "abrq" (l) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; Initiator run with abort request and forced recovery

  (defrole init3
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (eor-star (hash k) (enc m k) (ek (l)))))
    (non-orig (privk hash_id)))

  ;; Aborted initiator run, but with EOR received

  (defrole init4
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (recv (eor-star (hash k) (enc m k) (ek (l))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (enc "abcf"
                (enc "abrq" (l) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; Initiator run with abort requested after EOR received,
  ;; but recovery forced

  (defrole init5
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (recv (eor-star (hash k) (enc m k) (ek (l))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (eor-star (hash k) (enc m k) (ek (l)))))
    (non-orig (privk hash_id)))

  ;; Successful responder run with no TTP involvement

  (defrole resp1
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (recv (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (eor-star (hash k) (enc m k) (ek (l))))
     (recv (cat k r)))
    (non-orig (privk hash_id)))

  ;;Responder run with recovery via TTP

  (defrole resp2
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (recv (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))
                (eor-star (hash k) (enc m k) (ek (l)))))
     (send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))
                (eor-star (hash k) (enc m k) (ek (l)))
                (enc "rcrq" (l) (ek (l)) (privk "sign" b))))
     (recv (cat k r)))
    (non-orig (privk hash_id)))

  ;; Responder run with recovery request and forced abort

  (defrole resp3
    (vars (a b t hash_id name) (e1 e2 x mesg))
    (trace
     (recv (cat (l-star e1 x) e1 e2 (eoo-star x e1 e2)))
     (send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2)))
     (send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2)
                (enc "rcrq" (l-star e1 x) e2 (privk "sign" b))))
     (recv (enc "abcf"
                (enc "abrq" (l-star e1 x) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; TTP handles an abort

  (defrole ttp-ab1
    (vars (a b t hash_id name) (y x mesg))
    (trace
     (recv (enc "abrq" (l-prime y x) (privk "sign" a)))
     (send (cat "sync-abrq"
                (enc "abrq" (l-prime y x) (privk "sign" a))))
     (send (enc "abcf"
                (enc "abrq" (l-prime y x) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; TTP forces recovery in response to an abort request

  (defrole ttp-ab2
    (vars (a b t hash_id name) (y x e mesg))
    (trace
     (recv (enc "abrq" (l-prime y x) (privk "sign" a)))
     (recv (cat "sync-abrq"
                (enc "eortag" (hash (l-prime y x)) e
                     (privk "sign" b))))
     (send (enc "eortag" (hash (l-prime y x)) e
                (privk "sign" b))))
    (non-orig (privk hash_id)))

  ;; TTP handles a recovery

  (defrole ttp-rc1
    (vars (a b t hash_id name) (r text) (k skey) (y mesg))
    (trace
     (recv (rr-prime-prime y))
     (send (cat "sync-rc-req"
                (rr-prime-prime y)))
     (send (cat k r)))
    (non-orig (privk hash_id)))

  ;; TTP forces abort in response to a recovery request

  (defrole ttp-rc2
    (vars (a b t hash_id name) (r text) (k skey) (y mesg))
    (trace
     (recv (rr-prime-prime y))
     (recv (cat "sync-rc-req"
		(enc "abrq" (l-prime-prime y) (privk "sign" a))))
     (send (enc "abcf"
                (enc "abrq" (l-prime-prime y) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; TTP handles a confirm request

  (defrole ttp-cf1
    (vars (a b t hash_id name) (r text) (k skey) (y mesg))
    (trace
     (recv (cf-prime-prime y))
     (send (cat "sync-cf-req"
                (cf-prime-prime y)))
     (send (enc (cf-prime-prime y) (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; TTP replies with abort token given confirm request

  (defrole ttp-cf2
    (vars (a b t hash_id name) (r text) (k skey) (y mesg))
    (trace
     (recv (cf-prime-prime y))
     (recv (cat "sync-cf-req"
                (enc "abrq"(l-prime-prime y) (privk "sign" a))))
     (send (enc "abcf"
                (enc "abrq"(l-prime-prime y) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id))))

;; End of Wang's protocol defn.

;; Two experiments to prove Lemma 4.1

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init1 1 (b b) (t t) (m m) (r r) (k k))
  (deflistener m)
  (non-orig
   (privk "encr" t))
  (uniq-orig m k)
  (comment "Experiment 1 to prove Lemma 4.1."))

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init1 1 (b b) (t t) (m m) (r r) (k k))
  (deflistener k)
  (non-orig
   (privk "encr" t))
  (uniq-orig m k)
  (comment "Experiment 2 to prove Lemma 4.1."))

;; We now have three experiments
;; to prove Lemma 4.2, clause 1.

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init1 3 (b b) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" b))
  (comment "First of three experiments to prove Lemma 4.2, clause 1."))

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init3 3 (b b) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" b))
  (comment "Second of three experiments to prove Lemma 4.2, clause 1."))

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init5 4 (b b) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" b))
  (comment "Third of three experiments to prove Lemma 4.2, clause 1."))

;; Two experiments to prove 4.2, Clause 2.

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand resp1 3 (a a) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" a))
  (comment
   "First of two experiments to prove Lemma 4.2, clause 2."))

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand resp2 4 (a a) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" a))
  (comment
   "Second of two experiments to prove Lemma 4.2, clause 2."))

;; Experiment to prove Lemma 4.2, clause 3.

(defskeleton wang
  (vars (a b t hash_id name) (e1 e2 x mesg))
  (defstrand resp3 4 (a a) (t t))
  (non-orig
   (privk "sign" a))
  (comment
   "Experiments to prove Lemma 4.2, clause 3."))

;; One experiment to prove Lemma 4.3, Clause 1.

(defskeleton wang
  (vars (a b t hash_id name) (y x mesg))
  (deflistener
    (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a))
	 (privk "sign" t)))
  (non-orig
   (privk "sign" t))
  (comment
   "Experiments to prove Lemma 4.3, clause 1."))

;; Three experiments to prove Lemma 4.3, Clause 2.

(defskeleton wang
  (vars (y x mesg) (a b t name))
  (defstrand ttp-ab1 3 (y y) (x x) (a a) (b b) (t t))
  (non-orig (privk "sign" a)  (privk "encr" t))
  (comment
   "Experiment 1 to prove Lemma 4.3, clause 2."))

(defskeleton wang
  (vars (a b t hash_id name) (r text) (k skey) (y mesg))
  (defstrand ttp-rc2 3 (a a) (b b) (t t))
  (non-orig (privk "sign" a)  (privk "encr" t))
  (comment
   "Experiment 2 to prove Lemma 4.3, clause 2."))

(defskeleton wang
  (vars (a b t hash_id name) (r text) (k skey) (y mesg))
  (defstrand ttp-cf2 3 (a a) (b b) (t t))
  (non-orig (privk "sign" a)  (privk "encr" t))
  (comment
   "Experiment 3 to prove Lemma 4.3, clause 2."))
```

---

### `refrences/internet/examples_scm/wang-key-hash.scm`

*sha256:`362536a1eb34` · 434 lines · 12.2 KB · lang:`scheme`*

```scheme
(herald "Wang's Fair Exchange Protocol" (bound 10))

;; CPSA input file to represent
;; Wang's Fair Exchange Protocol

;; This macro implements the CPSA
;; convention of regarding a hash as
;; an asymmetric encryption.  The
;; decryption key inverse to (pubk
;; hash) is assumed non-originating
;; in roles using hashing.

(defmacro (hash x)
  (enc "h" (cat "h" x)))

;; Wang's encrypted format for the
;; message payload.  Observe that m,
;; k get their values from the
;; like-named messages in the context
;; where the macro is expanded.

(defmacro (em)
  (enc m k))

;; The session label L as a fn of
;; the values that *should be* the
;; hashes of the encrypted message EM
;; and the session key K.

(defmacro (l-prime y x)
  (cat a b t y x))

;; The recipient can check that a
;; session label has an l-prime where
;; y is the hash of another parameter.
;; Hence recipient roles use l-star.

(defmacro (l-star e1 x)
  (l-prime (hash e1) x))

;; The Evidence of Origin is checked
;; to be this fn of other parameters
;; available to the recipient.

(defmacro (eoo-star x e1 e2)
  (enc (cat "eootag"
	    (hash (l-star e1 x)) e2)
       (privk "sign" a)))

;; The Evidence of Receipt is computed
;; as this fn of other parameters
;; available to the recipient.

(defmacro (eor-star x e1 e2)
  (enc (cat "eortag"
	    (hash (l-star e1 x)) e2)
       (privk "sign" b)))

;; The Recovery Request as computed by
;; the recipient.

(defmacro (rr-star x e1 e2)
  (cat (l-star e1 x) e2
       (eoo-star x e1 e2)
       (eor-star x e1 e2)
       (enc (cat "rcrq" (l-star e1 x) e2)
            (privk "sign" b))))

;; The Abort Token is checked
;; to be this fn of other parameters
;; available to the recipient.

(defmacro (at-star e1 x)
  (enc (enc "abrq" (l-star e1 x)
            (privk "sign" a))
       (privk "sign" t)))

;; How the initiator computes the
;; encrypted key package:

(defmacro (ek l)
  (enc (cat "keytag" (hash l) k r)
       (pubk "encr" t)))

;; The Initiator's computed
;; version of L.

(defmacro (l)
  (l-prime (hash (enc m k)) (hash k)))

;; The TTP can check that the session
;; label L is this fn of other
;; parameters available to the TTP.

(defmacro (l-prime-prime y)
  (cat a b t y (hash k)))

;; The TTP can check that the EOO
;; is this fn of other parameters
;; available to the TTP.

(defmacro (eoo-prime-prime y)
  (enc (cat "eootag"
            (hash (l-prime-prime y))
	    (ek (l-prime-prime y)))
       (privk "sign" a)))

;; The TTP can check that the EOR
;; is this fn of other parameters
;; available to the TTP.

(defmacro (eor-prime-prime y)
  (enc (cat "eortag"
	    (hash (l-prime-prime y))
	    (ek (l-prime-prime y)))
       (privk "sign" b)))

;; The TTP can check that the RR
;; is this fn of other parameters
;; available to the TTP.

(defmacro (rr-prime-prime y)
  (cat (l-prime-prime y)
       (ek (l-prime-prime y))
       (eoo-prime-prime y)
       (eor-prime-prime y)
       (enc "rcrq" (l-prime-prime y)
	    (ek (l-prime-prime y))
            (privk "sign" b))))

;; The TTP can check that the Confirmation
;; Request is this fn of other parameters
;; available to the TTP.

(defmacro (cf-prime-prime y)
  (cat (l-prime-prime y) (ek (l-prime-prime y))
       (eoo-prime-prime y) (eor-prime-prime y)
       (enc "cfrq" (l-prime-prime y)
	    (ek (l-prime-prime y))
            (privk "sign" b))))

;; Defn of Wang's Fair Exchange Protocol.
;; Closely follows the presentation in the
;; figures in Section 3.  In the TTP roles,
;; we have put a dummy send or receive in place
;; of the state synchronization event to keep
;; the indices matching the spec.

(defprotocol wang basic

  ;; Successful initiator run with no TTP involvement

  (defrole init1
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (recv (eor-star (hash k) (enc m k) (ek (l))))
     (send (cat k r)))
    (non-orig (privk hash_id)))

  ;; Aborted initiator run

  (defrole init2
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (enc "abcf"
                (enc "abrq" (l) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; Initiator run with abort request and forced recovery

  (defrole init3
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (eor-star (hash k) (enc m k) (ek (l)))))
    (non-orig (privk hash_id)))

  ;; Aborted initiator run, but with EOR received

  (defrole init4
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (recv (eor-star (hash k) (enc m k) (ek (l))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (enc "abcf"
                (enc "abrq" (l) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; Initiator run with abort requested after EOR received,
  ;; but recovery forced

  (defrole init5
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (send (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (recv (eor-star (hash k) (enc m k) (ek (l))))
     (send (enc "abrq" (l) (privk "sign" a)))
     (recv (eor-star (hash k) (enc m k) (ek (l)))))
    (non-orig (privk hash_id)))

  ;; Successful responder run with no TTP involvement

  (defrole resp1
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (recv (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (eor-star (hash k) (enc m k) (ek (l))))
     (recv (cat k r)))
    (non-orig (privk hash_id)))

  ;;Responder run with recovery via TTP

  (defrole resp2
    (vars (a b t hash_id name) (m data) (r text) (k skey))
    (trace
     (recv (cat (l) (enc m k) (ek (l))
                (eoo-star (hash k) (enc m k) (ek (l)))))
     (send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))
                (eor-star (hash k) (enc m k) (ek (l)))))
     (send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))
                (eor-star (hash k) (enc m k) (ek (l)))
                (enc "rcrq" (l) (ek (l)) (privk "sign" b))))
     (recv (cat k r)))
    (non-orig (privk hash_id)))

  ;; Responder run with recovery request and forced abort

  (defrole resp3
    (vars (a b t hash_id name) (e1 e2 x mesg))
    (trace
     (recv (cat (l-star e1 x) e1 e2 (eoo-star x e1 e2)))
     (send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2)))
     (send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2)
                (enc "rcrq" (l-star e1 x) e2 (privk "sign" b))))
     (recv (enc "abcf"
                (enc "abrq" (l-star e1 x) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; TTP handles an abort

  (defrole ttp-ab1
    (vars (a b t hash_id name) (y x mesg))
    (trace
     (recv (enc "abrq" (l-prime y x) (privk "sign" a)))
     (send (cat "sync-abrq"
                (enc "abrq" (l-prime y x) (privk "sign" a))))
     (send (enc "abcf"
                (enc "abrq" (l-prime y x) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; TTP forces recovery in response to an abort request

  (defrole ttp-ab2
    (vars (a b t hash_id name) (y x e mesg))
    (trace
     (recv (enc "abrq" (l-prime y x) (privk "sign" a)))
     (recv (cat "sync-abrq"
                (enc "eortag" (hash (l-prime y x)) e
                     (privk "sign" b))))
     (send (enc "eortag" (hash (l-prime y x)) e
                (privk "sign" b))))
    (non-orig (privk hash_id)))

  ;; TTP handles a recovery

  (defrole ttp-rc1
    (vars (a b t hash_id name) (r text) (k skey) (y mesg))
    (trace
     (recv (rr-prime-prime y))
     (send (cat "sync-rc-req"
                (rr-prime-prime y)))
     (send (cat k r)))
    (non-orig (privk hash_id)))

  ;; TTP forces abort in response to a recovery request

  (defrole ttp-rc2
    (vars (a b t hash_id name) (r text) (k skey) (y mesg))
    (trace
     (recv (rr-prime-prime y))
     (recv (cat "sync-rc-req"
		(enc "abrq" (l-prime-prime y) (privk "sign" a))))
     (send (enc "abcf"
                (enc "abrq" (l-prime-prime y) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; TTP handles a confirm request

  (defrole ttp-cf1
    (vars (a b t hash_id name) (r text) (k skey) (y mesg))
    (trace
     (recv (cf-prime-prime y))
     (send (cat "sync-cf-req"
                (cf-prime-prime y)))
     (send (enc (cf-prime-prime y) (privk "sign" t))))
    (non-orig (privk hash_id)))

  ;; TTP replies with abort token given confirm request

  (defrole ttp-cf2
    (vars (a b t hash_id name) (r text) (k skey) (y mesg))
    (trace
     (recv (cf-prime-prime y))
     (recv (cat "sync-cf-req"
                (enc "abrq"(l-prime-prime y) (privk "sign" a))))
     (send (enc "abcf"
                (enc "abrq"(l-prime-prime y) (privk "sign" a))
                (privk "sign" t))))
    (non-orig (privk hash_id))))

;; End of Wang's protocol defn.

;; Two experiments to prove Lemma 4.1

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init1 1 (b b) (t t) (m m) (r r) (k k))
  (deflistener m)
  (non-orig
   (privk "encr" t))
  (uniq-orig m k)
  (comment "Experiment 1 to prove Lemma 4.1."))

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init1 1 (b b) (t t) (m m) (r r) (k k))
  (deflistener k)
  (non-orig
   (privk "encr" t))
  (uniq-orig m k)
  (comment "Experiment 2 to prove Lemma 4.1."))

;; We now have three experiments
;; to prove Lemma 4.2, clause 1.

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init1 3 (b b) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" b))
  (comment "First of three experiments to prove Lemma 4.2, clause 1."))

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init3 3 (b b) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" b))
  (comment "Second of three experiments to prove Lemma 4.2, clause 1."))

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand init5 4 (b b) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" b))
  (comment "Third of three experiments to prove Lemma 4.2, clause 1."))

;; Two experiments to prove 4.2, Clause 2.

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand resp1 3 (a a) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" a))
  (comment
   "First of two experiments to prove Lemma 4.2, clause 2."))

(defskeleton wang
  (vars (a b t hash_id name) (m data) (r text) (k skey))
  (defstrand resp2 4 (a a) (t t) (m m) (r r) (k k))
  (non-orig
   (privk "sign" a))
  (comment
   "Second of two experiments to prove Lemma 4.2, clause 2."))

;; Experiment to prove Lemma 4.2, clause 3.

(defskeleton wang
  (vars (a b t hash_id name) (e1 e2 x mesg))
  (defstrand resp3 4 (a a) (t t))
  (non-orig
   (privk "sign" a))
  (comment
   "Experiments to prove Lemma 4.2, clause 3."))

;; One experiment to prove Lemma 4.3, Clause 1.

(defskeleton wang
  (vars (a b t hash_id name) (y x mesg))
  (deflistener
    (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a))
	 (privk "sign" t)))
  (non-orig
   (privk "sign" t))
  (comment
   "Experiments to prove Lemma 4.3, clause 1."))

;; Three experiments to prove Lemma 4.3, Clause 2.

(defskeleton wang
  (vars (y x mesg) (a b t name))
  (defstrand ttp-ab1 3 (y y) (x x) (a a) (b b) (t t))
  (non-orig (privk "sign" a)  (privk "encr" t))
  (comment
   "Experiment 1 to prove Lemma 4.3, clause 2."))

(defskeleton wang
  (vars (a b t hash_id name) (r text) (k skey) (y mesg))
  (defstrand ttp-rc2 3 (a a) (b b) (t t))
  (non-orig (privk "sign" a)  (privk "encr" t))
  (comment
   "Experiment 2 to prove Lemma 4.3, clause 2."))

(defskeleton wang
  (vars (a b t hash_id name) (r text) (k skey) (y mesg))
  (defstrand ttp-cf2 3 (a a) (b b) (t t))
  (non-orig (privk "sign" a)  (privk "encr" t))
  (comment
   "Experiment 3 to prove Lemma 4.3, clause 2."))
```

---

### `refrences/internet/examples_scm/weird.scm`

*sha256:`c90e3b9beb58` · 58 lines · 1.3 KB · lang:`scheme`*

```scheme
(defprotocol weird basic
  (defrole originator
    (vars (k skey))
    (trace (send k))
    (uniq-orig k))
  (defrole guesser
    (vars (k skey) (a name))
    (trace (send (enc a k))))
  (defrole encryptor
    (vars (k skey) (a name))
    (trace (recv (enc a k)))))

;;; CPSA mistakenly concludes this is a skeleton.
(defskeleton weird
  (vars (k skey))
  (defstrand originator 1 (k k))
  (defstrand guesser 1 (k k)))

;;; CPSA mistakenly concludes it is possible for the encryptor to
;;; acquire k.
(defskeleton weird
  (vars (k skey))
  (defstrand originator 1 (k k))
  (defstrand encryptor 1 (k k)))

(defskeleton weird
  (vars (k skey))
  (defstrand originator 1 (k k))
  (defstrand encryptor 1 (k k))
  (precedes ((0 0) (1 0))))

(defprotocol weird-gen basic
  (defrole originator
    (vars (k skey))
    (trace (send k))
    (uniq-gen k))
  (defrole guesser
    (vars (k skey) (a name))
    (trace (send (enc a k))))
  (defrole encryptor
    (vars (k skey) (a name))
    (trace (recv (enc a k)))))

(defskeleton weird-gen
  (vars (k skey))
  (defstrand originator 1 (k k))
  (defstrand guesser 1 (k k)))

(defskeleton weird-gen
  (vars (k skey))
  (defstrand originator 1 (k k))
  (defstrand encryptor 1 (k k)))

(defskeleton weird-gen
  (vars (k skey))
  (defstrand originator 1 (k k))
  (defstrand encryptor 1 (k k))
  (precedes ((0 0) (1 0))))
```

---

### `refrences/internet/examples_scm/wonthull.scm`

*sha256:`2e7e04acefd5` · 40 lines · 1.1 KB · lang:`scheme`*

```scheme
(herald wonthull (bound 9))

;;;  Wonthull:  Demonstrates a subtle incompleteness.
;;;
;;;  The second POV skeleton given is a shape not produced
;;;   or covered in the first search.  The problem is that an
;;;   augmentation is attempted only with the most general
;;;   version of the responder strand that uses x3 as y1, not
;;;   the more specific version in which this does not lead to
;;;   x3 being originated in more than one place.)

(defprotocol wonthull basic
  (defrole init (vars (a name) (x1 x2 x3 x4 text))
    (trace
     (send (cat (enc x1 x2 (pubk a))
		(enc x3 x2 (pubk a))))
     (recv (enc "okay" x3 x4 (pubk a)))
     )
    (uniq-orig x1 x2 x3)
    (non-orig (privk a))
    )
  (defrole resp (vars (a name) (y1 y2 y3 text))
    (trace
     (recv (enc y1 y2 (pubk a)) )
     (send (enc "okay" y3 y1 (pubk a)) )
     )
    )
  )

(defskeleton wonthull
  (vars)
  (defstrand init 2)
)

(defskeleton wonthull
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 2 (a a) (x1 x1) (x2 x3) (x3 x3) (x4 x1))
  (defstrand resp 2 (a a) (y1 x1) (y2 x3) (y3 x3))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
)
```

---

### `refrences/internet/examples_scm/wonthull2.scm`

*sha256:`ec51d8d163d6` · 38 lines · 1.0 KB · lang:`scheme`*

```scheme
(herald wonthull2 (bound 9))
;;;  Wonthull 2:  Demonstrates a subtle incompleteness.
;;;
;;;  From Wonthull 1, the difference here is that
;;; Wonthull 2 should be able to do augmentation with
;;; non-trivial deorigination immediately after the POV.
;;;  Interestingly, Wonthull 2 (without deorigination)
;;; actually finds the missing shape, but via variable
;;; separation.

(defprotocol wonthull2 basic
  (defrole init (vars (a name) (x1 x2 x3 x4 text))
    (trace
     (send (cat (enc x1 x3 (pubk a)) (enc x3 x2 (pubk a))))
     (recv (enc "okay" x3 x4 (pubk a)))
     )
    (uniq-orig x3)
    (non-orig (privk a))
  )
  (defrole resp (vars (a name) (y1 y2 y3 text))
     (trace
       (recv (enc y1 y2 (pubk a)) )
       (send (enc "okay" y3 y1 (pubk a)) )
     )
  )
)

(defskeleton wonthull2
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 2)
)

(defskeleton wonthull2
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 2 (x2 x3) (x4 x1))
  (defstrand resp 2 (y1 x1) (y2 x3) (y3 x3))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
)
```

---

### `refrences/internet/examples_scm/wonthull3.scm`

*sha256:`37101d7ff334` · 36 lines · 0.9 KB · lang:`scheme`*

```scheme
;;;  Wonthull 3:  Demonstrates a subtle incompleteness.
;;;
;;;  Demonstrates that the deorigination incompleteness
;;; is not inherently linked to point and position of
;;; origination.

(defprotocol wonthull3 basic
  (defrole init (vars (a name) (x1 x2 x3 x4 text))
    (trace
     (send (enc x3 (pubk a)))
     (send (cat (enc x1 x2 (pubk a))
		(enc x3 x2 (pubk a))))
     (recv (enc "okay" x3 x4 (pubk a)))
     )
    (uniq-orig x3)
    (non-orig (privk a))
    )
  (defrole resp (vars (a name) (y1 y2 y3 text))
    (trace
     (recv (enc y1 y2 (pubk a)) )
     (send (enc "okay" y3 y1 (pubk a)) )
     )
    )
  )

(defskeleton wonthull3
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 3)
)

(defskeleton wonthull3
  (vars (a name) (n text) (x1 x2 x3 x4 text))
  (defstrand init 3 (x2 x3) (x4 x1))
  (defstrand resp 2 (y1 x1) (y2 x3) (y3 x3))
  (precedes ((0 1) (1 0)) ((1 1) (0 2)))
)
```

---

### `refrences/internet/examples_scm/woolam.scm`

*sha256:`9b5ddc1d5e38` · 26 lines · 0.7 KB · lang:`scheme`*

```scheme
(herald "Woo-Lam Protocol")

(defprotocol woolam basic
  (defrole init (vars (a s name) (n text))
    (trace
     (send a)
     (recv n)
     (send (enc n (ltk a s))))
    (non-orig (ltk a s)))
  (defrole resp (vars (a s b name) (n text))
    (trace
     (recv a)
     (send n)
     (recv (enc n (ltk a s)))
     (send (enc a (enc n (ltk a s)) (ltk b s)))
     (recv (enc a n (ltk b s))))
    (non-orig (ltk b s))
    (uniq-orig n))
  (defrole serv (vars (a s b name) (n text))
    (trace
     (recv (enc a (enc n (ltk a s)) (ltk b s)))
     (send (enc a n (ltk b s))))))

(defskeleton woolam (vars (n text) (a s name))
  (defstrand resp 5 (a a) (s s))
  (non-orig (ltk a s)))
```

---

### `refrences/internet/examples_scm/yahalom-6.3.6.scm`

*sha256:`6ad926c80e47` · 53 lines · 1.7 KB · lang:`scheme`*

```scheme
(herald "Yahalom Protocol"
  (comment "A Survey of Authentication Protocol Literature:"
	   "Version 1.0, John Clark and Jeremy Jacob,"
	   "Yahalom Protocol, Section 6.3.6, Page 49")
  (url "http://www.eecs.umich.edu/acal/swerve/docs/49-1.pdf")
  (bound 15))

(defprotocol yahalom basic
  (defrole init
    (vars (a b s name) (n-a n-b text) (k skey) (blob mesg))
    (trace
     (send (cat a n-a))
     (recv (cat (enc b k n-a n-b (ltk a s)) blob))
     (send (cat blob (enc n-b k)))))
  (defrole resp
    (vars (a b s name) (n-a n-b text) (k skey))
    (trace
     (recv (cat a n-a))
     (send (cat b (enc a n-a n-b (ltk b s))))
     (recv (cat (enc a k (ltk b s)) (enc n-b k)))))
  (defrole serv
    (vars (a b s name) (n-a n-b text) (k skey))
    (trace
     (recv (cat b (enc a n-a n-b (ltk b s))))
     (send (cat (enc b k n-a n-b (ltk a s)) (enc a k (ltk b s)))))
    (uniq-orig k))
  (comment "Yahalom protocol, Section 6.3.6, Page 49")
  (url "http://www.eecs.umich.edu/acal/swerve/docs/49-1.pdf"))

(defskeleton yahalom
  (vars (a b s name) (n-a n-b text))
  (defstrand init 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b))
  (non-orig (ltk a s) (ltk b s))
  (uniq-orig n-a n-b))

(defskeleton yahalom
  (vars (a b s name) (n-a n-b text) (k skey))
  (defstrand resp 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk a s) (ltk b s))
  (uniq-orig n-a n-b))

(defskeleton yahalom
  (vars (a b s name) (n-a n-b text))
  (defstrand resp 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b))
  (non-orig (ltk a s) (ltk b s))
  (uniq-orig n-a n-b))

(defskeleton yahalom
  (vars (a b s name) (n-a n-b text))
  (defstrand serv 2 (a a) (b b) (s s) (n-a n-a) (n-b n-b))
  (non-orig (ltk a s) (ltk b s))
  (uniq-orig n-a n-b))
```

---

### `refrences/internet/examples_scm/yahalom-forward.scm`

*sha256:`06698f095963` · 41 lines · 1.2 KB · lang:`scheme`*

```scheme
(herald "Yahalom Protocol With Forwarding" (bound 15))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey))
    (trace (send (cat a n-a))
	   (recv (enc b k n-a n-b (ltk a c)))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (rest mesg) (k skey))
    (trace (recv (cat a n-a))
	   (send (cat b (enc a n-a n-b (ltk b c))))
	   (recv (cat (enc a k (ltk b c)) rest))
	   (send rest) 
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey))
    (trace (recv (cat b (enc a n-a n-b (ltk b c))))
	   (send (cat (enc a k (ltk b c))
		      (enc b k n-a n-b (ltk a c)))))
    (uniq-orig k)))

(defskeleton yahalom
  (vars (a b c name) (n-b text))
  (defstrand resp 5 (a a) (b b) (c c) (n-b n-b))
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))

;;; Ensure encryption key remains secret.
(defskeleton yahalom
  (vars (a b c name) (n-b text) (k skey))
  (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))

(defskeleton yahalom
  (vars (a b c name) (n-a text))
  (defstrand init 3 (n-a n-a) (a a) (b b) (c c))
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-a))
```

---

### `refrences/internet/examples_scm/yahalom.scm`

*sha256:`e403b0a15ffb` · 34 lines · 1.0 KB · lang:`scheme`*

```scheme
(herald "Yahalom Protocol with Forwarding Removed" (bound 10))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey))
    (trace (send (cat a n-a))
	   (recv (enc b k n-a n-b (ltk a c)))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (k skey))
    (trace (recv (cat a n-a))
	   (send (cat b (enc a n-a n-b (ltk b c))))
	   (recv (enc a k (ltk b c)))
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey))
    (trace (recv (cat b (enc a n-a n-b (ltk b c))))
	   (send (enc b k n-a n-b (ltk a c)))
	   (send (enc a k (ltk b c))))
    (uniq-orig k)))

(defskeleton yahalom
  (vars (a b c name) (n-b text))
  (defstrand resp 4 (a a) (b b) (c c) (n-b n-b))
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))

;;; Ensure encryption key remains secret.
(defskeleton yahalom
  (vars (a b c name) (n-b text) (k skey))
  (defstrand resp 4 (a a) (b b) (c c) (n-b n-b) (k k))
  (deflistener k)
  (non-orig (ltk b c) (ltk a c))
  (uniq-orig n-b))
```

---

### `refrences/internet/examples_scm/yes-or-no.scm`

*sha256:`44271b6e83a9` · 52 lines · 1.3 KB · lang:`scheme`*

```scheme
(herald yes-or-no)

(defprotocol yes-or-no basic
  (defrole init-positive
    (vars (y n data) (question text) (ans name) (ans-key akey))
    (trace
     (send (enc question y n ans-key))
     (recv y)))

  (defrole init-negative
    (vars (y n data) (question text) (ans name) (ans-key akey))
    (trace
     (send (enc question y n ans-key))
     (recv n)))

  (defrole resp-positive
    (vars (y n data) (question text) (ans name) (ans-key akey))
    (trace
     (recv (enc question y n ans-key))
     (send y)))

  (defrole resp-negative
    (vars (y n data) (question text) (ans name) (ans-key akey))
    (trace
     (recv (enc question y n ans-key))
     (send n))))

(defskeleton yes-or-no
  (vars (y data) (ans-key akey))
  (defstrand init-positive 2 (y y) (ans-key ans-key))
  (uniq-orig y)
  (non-orig (invk ans-key)))

(defskeleton yes-or-no
  (vars (ans-key akey) (n data))
  (defstrand init-negative 2 (n n) (ans-key ans-key))
  (uniq-orig n) 
  (non-orig (invk ans-key)))

(defskeleton yes-or-no
  (vars (y data) (ans-key akey))
  (defstrand init-positive 1 (y y) (ans-key ans-key))
  (deflistener y)
  (uniq-orig y)
  (non-orig (invk ans-key)))

(defskeleton yes-or-no
  (vars (n data) (ans-key akey))
  (defstrand init-positive 1 (n n) (ans-key ans-key))
  (deflistener n) 
  (uniq-orig n)
  (non-orig (invk ans-key)))
```

---
