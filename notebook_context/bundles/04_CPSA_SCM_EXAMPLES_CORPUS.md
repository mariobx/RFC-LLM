# Official MITRE CPSA Scheme (.scm) Protocol Examples & Catalog (151 Files)

> Tier 3 Reference Corpus — Complete collection of all 151 official MITRE CPSA 4.4.9 `.scm` protocol specifications (`refrences/cpsa_kb/03_examples_scm/`) and their structured A-to-Z concept catalogs (`refrences/cpsa_kb/04_examples_catalog/*.md`).

*Generated: 2026-11-03 15:36:27 UTC · Git: `main` @ `59dd1b43aaa5` · Tier: Tier 3 — Domain Reference Code Corpus (.scm) · Files: 155 · Estimated Tokens: ~234,169*

## Table of Contents

- [`refrences/cpsa_kb/03_examples_scm/DH_hack.scm`](#refrencescpsa-kb03-examples-scmdh-hackscm)
- [`refrences/cpsa_kb/03_examples_scm/ab.scm`](#refrencescpsa-kb03-examples-scmabscm)
- [`refrences/cpsa_kb/03_examples_scm/abc.scm`](#refrencescpsa-kb03-examples-scmabcscm)
- [`refrences/cpsa_kb/03_examples_scm/aik.scm`](#refrencescpsa-kb03-examples-scmaikscm)
- [`refrences/cpsa_kb/03_examples_scm/atomic-open-closed.scm`](#refrencescpsa-kb03-examples-scmatomic-open-closedscm)
- [`refrences/cpsa_kb/03_examples_scm/attest.scm`](#refrencescpsa-kb03-examples-scmattestscm)
- [`refrences/cpsa_kb/03_examples_scm/auth-enc.scm`](#refrencescpsa-kb03-examples-scmauth-encscm)
- [`refrences/cpsa_kb/03_examples_scm/auth-hash.scm`](#refrencescpsa-kb03-examples-scmauth-hashscm)
- [`refrences/cpsa_kb/03_examples_scm/blanchet-strandmax.scm`](#refrencescpsa-kb03-examples-scmblanchet-strandmaxscm)
- [`refrences/cpsa_kb/03_examples_scm/blanchet.scm`](#refrencescpsa-kb03-examples-scmblanchetscm)
- [`refrences/cpsa_kb/03_examples_scm/bug_example.scm`](#refrencescpsa-kb03-examples-scmbug-examplescm)
- [`refrences/cpsa_kb/03_examples_scm/cert_lang.scm`](#refrencescpsa-kb03-examples-scmcert-langscm)
- [`refrences/cpsa_kb/03_examples_scm/chan-envelope.scm`](#refrencescpsa-kb03-examples-scmchan-envelopescm)
- [`refrences/cpsa_kb/03_examples_scm/chan-mesg.scm`](#refrencescpsa-kb03-examples-scmchan-mesgscm)
- [`refrences/cpsa_kb/03_examples_scm/chan-perrig-song.scm`](#refrencescpsa-kb03-examples-scmchan-perrig-songscm)
- [`refrences/cpsa_kb/03_examples_scm/chan-unilateral.scm`](#refrencescpsa-kb03-examples-scmchan-unilateralscm)
- [`refrences/cpsa_kb/03_examples_scm/chan-yahalom-role-decl.scm`](#refrencescpsa-kb03-examples-scmchan-yahalom-role-declscm)
- [`refrences/cpsa_kb/03_examples_scm/chan-yahalom.scm`](#refrencescpsa-kb03-examples-scmchan-yahalomscm)
- [`refrences/cpsa_kb/03_examples_scm/commitment.scm`](#refrencescpsa-kb03-examples-scmcommitmentscm)
- [`refrences/cpsa_kb/03_examples_scm/comp_test.scm`](#refrencescpsa-kb03-examples-scmcomp-testscm)
- [`refrences/cpsa_kb/03_examples_scm/completeness-test.scm`](#refrencescpsa-kb03-examples-scmcompleteness-testscm)
- [`refrences/cpsa_kb/03_examples_scm/crushing.scm`](#refrencescpsa-kb03-examples-scmcrushingscm)
- [`refrences/cpsa_kb/03_examples_scm/dass_simple.scm`](#refrencescpsa-kb03-examples-scmdass-simplescm)
- [`refrences/cpsa_kb/03_examples_scm/denning-sacco.scm`](#refrencescpsa-kb03-examples-scmdenning-saccoscm)
- [`refrences/cpsa_kb/03_examples_scm/deorig_contract.scm`](#refrencescpsa-kb03-examples-scmdeorig-contractscm)
- [`refrences/cpsa_kb/03_examples_scm/deorig_mesg.scm`](#refrencescpsa-kb03-examples-scmdeorig-mesgscm)
- [`refrences/cpsa_kb/03_examples_scm/deorig_simple.scm`](#refrencescpsa-kb03-examples-scmdeorig-simplescm)
- [`refrences/cpsa_kb/03_examples_scm/dev-subatomic-open-closed.scm`](#refrencescpsa-kb03-examples-scmdev-subatomic-open-closedscm)
- [`refrences/cpsa_kb/03_examples_scm/devlocn.scm`](#refrencescpsa-kb03-examples-scmdevlocnscm)
- [`refrences/cpsa_kb/03_examples_scm/dh-ca_hack.scm`](#refrencescpsa-kb03-examples-scmdh-ca-hackscm)
- [`refrences/cpsa_kb/03_examples_scm/dh_encrypt_hack.scm`](#refrencescpsa-kb03-examples-scmdh-encrypt-hackscm)
- [`refrences/cpsa_kb/03_examples_scm/dh_group_sig.scm`](#refrencescpsa-kb03-examples-scmdh-group-sigscm)
- [`refrences/cpsa_kb/03_examples_scm/dh_group_sig_auth_failure.scm`](#refrencescpsa-kb03-examples-scmdh-group-sig-auth-failurescm)
- [`refrences/cpsa_kb/03_examples_scm/dh_mim_hack.scm`](#refrencescpsa-kb03-examples-scmdh-mim-hackscm)
- [`refrences/cpsa_kb/03_examples_scm/dhnsl_hack.scm`](#refrencescpsa-kb03-examples-scmdhnsl-hackscm)
- [`refrences/cpsa_kb/03_examples_scm/dhstatic-state.scm`](#refrencescpsa-kb03-examples-scmdhstatic-statescm)
- [`refrences/cpsa_kb/03_examples_scm/disclosure.scm`](#refrencescpsa-kb03-examples-scmdisclosurescm)
- [`refrences/cpsa_kb/03_examples_scm/doorsep.scm`](#refrencescpsa-kb03-examples-scmdoorsepscm)
- [`refrences/cpsa_kb/03_examples_scm/doorsep2invk.scm`](#refrencescpsa-kb03-examples-scmdoorsep2invkscm)
- [`refrences/cpsa_kb/03_examples_scm/encsig.scm`](#refrencescpsa-kb03-examples-scmencsigscm)
- [`refrences/cpsa_kb/03_examples_scm/envelope.scm`](#refrencescpsa-kb03-examples-scmenvelopescm)
- [`refrences/cpsa_kb/03_examples_scm/epmo-hash.scm`](#refrencescpsa-kb03-examples-scmepmo-hashscm)
- [`refrences/cpsa_kb/03_examples_scm/epmo-key-hash.scm`](#refrencescpsa-kb03-examples-scmepmo-key-hashscm)
- [`refrences/cpsa_kb/03_examples_scm/epmo.scm`](#refrencescpsa-kb03-examples-scmepmoscm)
- [`refrences/cpsa_kb/03_examples_scm/epmo_acctnum-key-hash.scm`](#refrencescpsa-kb03-examples-scmepmo-acctnum-key-hashscm)
- [`refrences/cpsa_kb/03_examples_scm/expand.scm`](#refrencescpsa-kb03-examples-scmexpandscm)
- [`refrences/cpsa_kb/03_examples_scm/facts.scm`](#refrencescpsa-kb03-examples-scmfactsscm)
- [`refrences/cpsa_kb/03_examples_scm/factvar.scm`](#refrencescpsa-kb03-examples-scmfactvarscm)
- [`refrences/cpsa_kb/03_examples_scm/ffgg.scm`](#refrencescpsa-kb03-examples-scmffggscm)
- [`refrences/cpsa_kb/03_examples_scm/fluffy_draft03_gske.scm`](#refrencescpsa-kb03-examples-scmfluffy-draft03-gskescm)
- [`refrences/cpsa_kb/03_examples_scm/fragile_pruning.scm`](#refrencescpsa-kb03-examples-scmfragile-pruningscm)
- [`refrences/cpsa_kb/03_examples_scm/goals.scm`](#refrencescpsa-kb03-examples-scmgoalsscm)
- [`refrences/cpsa_kb/03_examples_scm/goalsvar.scm`](#refrencescpsa-kb03-examples-scmgoalsvarscm)
- [`refrences/cpsa_kb/03_examples_scm/hashtest-key-hash.scm`](#refrencescpsa-kb03-examples-scmhashtest-key-hashscm)
- [`refrences/cpsa_kb/03_examples_scm/hashtest.scm`](#refrencescpsa-kb03-examples-scmhashtestscm)
- [`refrences/cpsa_kb/03_examples_scm/incompleteness_example.scm`](#refrencescpsa-kb03-examples-scmincompleteness-examplescm)
- [`refrences/cpsa_kb/03_examples_scm/isoreject-corrected.scm`](#refrencescpsa-kb03-examples-scmisoreject-correctedscm)
- [`refrences/cpsa_kb/03_examples_scm/isoreject.scm`](#refrencescpsa-kb03-examples-scmisorejectscm)
- [`refrences/cpsa_kb/03_examples_scm/kelly1.scm`](#refrencescpsa-kb03-examples-scmkelly1scm)
- [`refrences/cpsa_kb/03_examples_scm/kerberos.scm`](#refrencescpsa-kb03-examples-scmkerberosscm)
- [`refrences/cpsa_kb/03_examples_scm/lemmas.scm`](#refrencescpsa-kb03-examples-scmlemmasscm)
- [`refrences/cpsa_kb/03_examples_scm/locn_envelope.scm`](#refrencescpsa-kb03-examples-scmlocn-envelopescm)
- [`refrences/cpsa_kb/03_examples_scm/missing_contraction.scm`](#refrencescpsa-kb03-examples-scmmissing-contractionscm)
- [`refrences/cpsa_kb/03_examples_scm/neq_test.scm`](#refrencescpsa-kb03-examples-scmneq-testscm)
- [`refrences/cpsa_kb/03_examples_scm/neuman-stubblebine.scm`](#refrencescpsa-kb03-examples-scmneuman-stubblebinescm)
- [`refrences/cpsa_kb/03_examples_scm/no_contraction.scm`](#refrencescpsa-kb03-examples-scmno-contractionscm)
- [`refrences/cpsa_kb/03_examples_scm/non_transforming.scm`](#refrencescpsa-kb03-examples-scmnon-transformingscm)
- [`refrences/cpsa_kb/03_examples_scm/nonaug-prune.scm`](#refrencescpsa-kb03-examples-scmnonaug-prunescm)
- [`refrences/cpsa_kb/03_examples_scm/ns-l.scm`](#refrencescpsa-kb03-examples-scmns-lscm)
- [`refrences/cpsa_kb/03_examples_scm/ns-rebinding.scm`](#refrencescpsa-kb03-examples-scmns-rebindingscm)
- [`refrences/cpsa_kb/03_examples_scm/ns.scm`](#refrencescpsa-kb03-examples-scmnsscm)
- [`refrences/cpsa_kb/03_examples_scm/nsl3.scm`](#refrencescpsa-kb03-examples-scmnsl3scm)
- [`refrences/cpsa_kb/03_examples_scm/nslsk.scm`](#refrencescpsa-kb03-examples-scmnslskscm)
- [`refrences/cpsa_kb/03_examples_scm/open-closed-multiloc.scm`](#refrencescpsa-kb03-examples-scmopen-closed-multilocscm)
- [`refrences/cpsa_kb/03_examples_scm/open-closed-tag.scm`](#refrencescpsa-kb03-examples-scmopen-closed-tagscm)
- [`refrences/cpsa_kb/03_examples_scm/open-closed.scm`](#refrencescpsa-kb03-examples-scmopen-closedscm)
- [`refrences/cpsa_kb/03_examples_scm/or.scm`](#refrencescpsa-kb03-examples-scmorscm)
- [`refrences/cpsa_kb/03_examples_scm/ordered.scm`](#refrencescpsa-kb03-examples-scmorderedscm)
- [`refrences/cpsa_kb/03_examples_scm/orderedvar.scm`](#refrencescpsa-kb03-examples-scmorderedvarscm)
- [`refrences/cpsa_kb/03_examples_scm/pca.scm`](#refrencescpsa-kb03-examples-scmpcascm)
- [`refrences/cpsa_kb/03_examples_scm/pen-non-orig-test.scm`](#refrencescpsa-kb03-examples-scmpen-non-orig-testscm)
- [`refrences/cpsa_kb/03_examples_scm/pfs-via-pubkey.scm`](#refrencescpsa-kb03-examples-scmpfs-via-pubkeyscm)
- [`refrences/cpsa_kb/03_examples_scm/pkinit.scm`](#refrencescpsa-kb03-examples-scmpkinitscm)
- [`refrences/cpsa_kb/03_examples_scm/preprocess.scm`](#refrencescpsa-kb03-examples-scmpreprocessscm)
- [`refrences/cpsa_kb/03_examples_scm/print.scm`](#refrencescpsa-kb03-examples-scmprintscm)
- [`refrences/cpsa_kb/03_examples_scm/prottrans.scm`](#refrencescpsa-kb03-examples-scmprottransscm)
- [`refrences/cpsa_kb/03_examples_scm/pruning1.scm`](#refrencescpsa-kb03-examples-scmpruning1scm)
- [`refrences/cpsa_kb/03_examples_scm/puzzle_example.scm`](#refrencescpsa-kb03-examples-scmpuzzle-examplescm)
- [`refrences/cpsa_kb/03_examples_scm/reflect.scm`](#refrencescpsa-kb03-examples-scmreflectscm)
- [`refrences/cpsa_kb/03_examples_scm/renamings.scm`](#refrencescpsa-kb03-examples-scmrenamingsscm)
- [`refrences/cpsa_kb/03_examples_scm/role_uniq.scm`](#refrencescpsa-kb03-examples-scmrole-uniqscm)
- [`refrences/cpsa_kb/03_examples_scm/rule-node.scm`](#refrencescpsa-kb03-examples-scmrule-nodescm)
- [`refrences/cpsa_kb/03_examples_scm/rule-order.scm`](#refrencescpsa-kb03-examples-scmrule-orderscm)
- [`refrences/cpsa_kb/03_examples_scm/rules.scm`](#refrencescpsa-kb03-examples-scmrulesscm)
- [`refrences/cpsa_kb/03_examples_scm/scep-tls-dh-broken.scm`](#refrencescpsa-kb03-examples-scmscep-tls-dh-brokenscm)
- [`refrences/cpsa_kb/03_examples_scm/scep-tls-dh-fixed.scm`](#refrencescpsa-kb03-examples-scmscep-tls-dh-fixedscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-auth-enc-full-payload.scm`](#refrencescpsa-kb03-examples-scmsdls-auth-enc-full-payloadscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-auth-enc-logic.scm`](#refrencescpsa-kb03-examples-scmsdls-auth-enc-logicscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-auth-full-payload.scm`](#refrencescpsa-kb03-examples-scmsdls-auth-full-payloadscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-auth-logic.scm`](#refrencescpsa-kb03-examples-scmsdls-auth-logicscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-enc-logic.scm`](#refrencescpsa-kb03-examples-scmsdls-enc-logicscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-challenge-auth.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-challenge-authscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-challenge-authenc.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-challenge-authencscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-challenge.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-challengescm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-key-activation-auth.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-key-activation-authscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-key-activation-authenc.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-key-activation-authencscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-key-activation.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-key-activationscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-otar-auth.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-otar-authscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-otar-authenc.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-otar-authencscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-otar-transmission.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-otar-transmissionscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-rekey-auth.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-sa-rekey-authscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-rekey-authenc.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-sa-rekey-authencscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-rekey.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-sa-rekeyscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-start-auth.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-sa-start-authscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-start-authenc.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-sa-start-authencscm)
- [`refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-start.scm`](#refrencescpsa-kb03-examples-scmsdls-ep-sa-startscm)
- [`refrences/cpsa_kb/03_examples_scm/sigenc.scm`](#refrencescpsa-kb03-examples-scmsigencscm)
- [`refrences/cpsa_kb/03_examples_scm/sorted_epmo_acctnum.scm`](#refrencescpsa-kb03-examples-scmsorted-epmo-acctnumscm)
- [`refrences/cpsa_kb/03_examples_scm/sts.scm`](#refrencescpsa-kb03-examples-scmstsscm)
- [`refrences/cpsa_kb/03_examples_scm/sts_non_role.scm`](#refrencescpsa-kb03-examples-scmsts-non-rolescm)
- [`refrences/cpsa_kb/03_examples_scm/sts_weakened_reflect.scm`](#refrencescpsa-kb03-examples-scmsts-weakened-reflectscm)
- [`refrences/cpsa_kb/03_examples_scm/subatomic-open-closed-test-genrule.scm`](#refrencescpsa-kb03-examples-scmsubatomic-open-closed-test-genrulescm)
- [`refrences/cpsa_kb/03_examples_scm/subatomic-open-closed.scm`](#refrencescpsa-kb03-examples-scmsubatomic-open-closedscm)
- [`refrences/cpsa_kb/03_examples_scm/sync_locn_envelope.scm`](#refrencescpsa-kb03-examples-scmsync-locn-envelopescm)
- [`refrences/cpsa_kb/03_examples_scm/sync_locn_envelope_no_auth.scm`](#refrencescpsa-kb03-examples-scmsync-locn-envelope-no-authscm)
- [`refrences/cpsa_kb/03_examples_scm/targetterms1.scm`](#refrencescpsa-kb03-examples-scmtargetterms1scm)
- [`refrences/cpsa_kb/03_examples_scm/targetterms2.scm`](#refrencescpsa-kb03-examples-scmtargetterms2scm)
- [`refrences/cpsa_kb/03_examples_scm/targetterms6.scm`](#refrencescpsa-kb03-examples-scmtargetterms6scm)
- [`refrences/cpsa_kb/03_examples_scm/targetterms8.scm`](#refrencescpsa-kb03-examples-scmtargetterms8scm)
- [`refrences/cpsa_kb/03_examples_scm/thisthat.scm`](#refrencescpsa-kb03-examples-scmthisthatscm)
- [`refrences/cpsa_kb/03_examples_scm/tickle-unique.scm`](#refrencescpsa-kb03-examples-scmtickle-uniquescm)
- [`refrences/cpsa_kb/03_examples_scm/timestamping.scm`](#refrencescpsa-kb03-examples-scmtimestampingscm)
- [`refrences/cpsa_kb/03_examples_scm/trust-anchor.scm`](#refrencescpsa-kb03-examples-scmtrust-anchorscm)
- [`refrences/cpsa_kb/03_examples_scm/ugen-at.scm`](#refrencescpsa-kb03-examples-scmugen-atscm)
- [`refrences/cpsa_kb/03_examples_scm/ugo.scm`](#refrencescpsa-kb03-examples-scmugoscm)
- [`refrences/cpsa_kb/03_examples_scm/uncarried_keys.scm`](#refrencescpsa-kb03-examples-scmuncarried-keysscm)
- [`refrences/cpsa_kb/03_examples_scm/unilateral.scm`](#refrencescpsa-kb03-examples-scmunilateralscm)
- [`refrences/cpsa_kb/03_examples_scm/uniq-at.scm`](#refrencescpsa-kb03-examples-scmuniq-atscm)
- [`refrences/cpsa_kb/03_examples_scm/uniq-gen-test.scm`](#refrencescpsa-kb03-examples-scmuniq-gen-testscm)
- [`refrences/cpsa_kb/03_examples_scm/uo.scm`](#refrencescpsa-kb03-examples-scmuoscm)
- [`refrences/cpsa_kb/03_examples_scm/wang-hash.scm`](#refrencescpsa-kb03-examples-scmwang-hashscm)
- [`refrences/cpsa_kb/03_examples_scm/wang-key-hash.scm`](#refrencescpsa-kb03-examples-scmwang-key-hashscm)
- [`refrences/cpsa_kb/03_examples_scm/weird.scm`](#refrencescpsa-kb03-examples-scmweirdscm)
- [`refrences/cpsa_kb/03_examples_scm/wonthull.scm`](#refrencescpsa-kb03-examples-scmwonthullscm)
- [`refrences/cpsa_kb/03_examples_scm/wonthull2.scm`](#refrencescpsa-kb03-examples-scmwonthull2scm)
- [`refrences/cpsa_kb/03_examples_scm/wonthull3.scm`](#refrencescpsa-kb03-examples-scmwonthull3scm)
- [`refrences/cpsa_kb/03_examples_scm/woolam.scm`](#refrencescpsa-kb03-examples-scmwoolamscm)
- [`refrences/cpsa_kb/03_examples_scm/yahalom-6.3.6.scm`](#refrencescpsa-kb03-examples-scmyahalom-636scm)
- [`refrences/cpsa_kb/03_examples_scm/yahalom-forward.scm`](#refrencescpsa-kb03-examples-scmyahalom-forwardscm)
- [`refrences/cpsa_kb/03_examples_scm/yahalom.scm`](#refrencescpsa-kb03-examples-scmyahalomscm)
- [`refrences/cpsa_kb/03_examples_scm/yes-or-no.scm`](#refrencescpsa-kb03-examples-scmyes-or-noscm)
- [`refrences/cpsa_kb/04_examples_catalog/01_scm_examples_A_to_G.md`](#refrencescpsa-kb04-examples-catalog01-scm-examples-a-to-gmd)
- [`refrences/cpsa_kb/04_examples_catalog/02_scm_examples_H_to_SDLS.md`](#refrencescpsa-kb04-examples-catalog02-scm-examples-h-to-sdlsmd)
- [`refrences/cpsa_kb/04_examples_catalog/03_scm_examples_SDLS_to_Z.md`](#refrencescpsa-kb04-examples-catalog03-scm-examples-sdls-to-zmd)
- [`refrences/cpsa_kb/04_examples_catalog/04_scm_examples_hackage_4_4_9.md`](#refrencescpsa-kb04-examples-catalog04-scm-examples-hackage-4-4-9md)

---

### `refrences/cpsa_kb/03_examples_scm/DH_hack.scm`

*sha256:`1dd27362fe4b` · 72 lines · 2.4 KB (~615 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/ab.scm`

*sha256:`1e3d93f7a82d` · 26 lines · 0.6 KB (~164 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/abc.scm`

*sha256:`67394bb26109` · 30 lines · 0.7 KB (~190 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/aik.scm`

*sha256:`de3554177295` · 30 lines · 1.0 KB (~254 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/atomic-open-closed.scm`

*sha256:`0aca95d4c358` · 416 lines · 10.4 KB (~2,665 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/attest.scm`

*sha256:`fc0ffff10b77` · 190 lines · 5.0 KB (~1,278 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/auth-enc.scm`

*sha256:`f2ddbb62150b` · 18 lines · 0.4 KB (~104 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/auth-hash.scm`

*sha256:`58e88956cdec` · 18 lines · 0.4 KB (~95 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/blanchet-strandmax.scm`

*sha256:`5caa67bbda5b` · 131 lines · 3.9 KB (~1,000 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/blanchet.scm`

*sha256:`2f16c32a28d3` · 88 lines · 2.6 KB (~665 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/bug_example.scm`

*sha256:`68f92ca2c76a` · 43 lines · 1.1 KB (~294 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/cert_lang.scm`

*sha256:`f2199b4592dc` · 44 lines · 1.4 KB (~362 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/chan-envelope.scm`

*sha256:`34a633cf224a` · 212 lines · 6.5 KB (~1,652 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/chan-mesg.scm`

*sha256:`03a8ba975e93` · 114 lines · 3.8 KB (~980 tokens) · lang:`scheme`*

```scheme
(herald "Yahalom Protocol Without Forwarding" (bound 15)
	(comment "Testing channels as arbitrary messages."))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey))
    (trace (send (cat a n-a))
	   (recv (cat c a) (cat a b k n-a n-b))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))
    (trace (recv (cat a n-a))
	   (send (cat b c) (cat a b n-a n-b))
	   (recv (cat c b) (cat a b k))
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
    (trace (recv (cat b c) (cat a b n-a n-b))
	   (send (cat c a) (cat a b k n-a n-b))
	   (send (cat c b) (cat a b k)))
    (uniq-orig k))
  (comment "Use (cat x y) as channel from x to y. Matching channel should force matching names."))

;;; How much do we know assuming that the resp had a run with an
;;; authenticated channel ch2?  We also assume the responder's nonce
;;; is freshly chosen.

(defskeleton yahalom
  (vars (a b c name) (n-b text))
  (defstrand resp 4 (a a) (b b) (c c) (n-b n-b))
  (auth (cat c b))
  (uniq-orig n-b))

;;; This is the answer to the previous question, to which we have
;;; added the assumptions ...

(defskeleton yahalom
  (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b c name))
  (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (c c))
  (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (c c) (a a) (b b))
  (precedes ((1 2) (0 2)))
  (uniq-orig k n-b)
  (auth (cat c b))
  (conf (cat c b) (cat c a)))


;;; This is the ...
(defskeleton yahalom
  (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b c name))
  (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (c c))
  (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (c c) (a a) (b b))
  (uniq-orig k n-b)
  (auth (cat c b) (cat b c))
  (conf (cat c b) (cat c a)))

;;; In particular, we can now check that the session key cannot be
;;; compromised, subject to the assumptions we have imposed, using
;;; (deflistener k).

(defskeleton yahalom
  (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b c name))
  (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (c c))
  (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (c c) (a a) (b b))
  (deflistener k)
  (uniq-orig k n-b)
  (auth (cat c b) (cat b c))
  (conf (cat c b) (cat c a)))

;;; Let's turn now to the initiator's point of view:

(defskeleton yahalom
  (vars (a b c name) (n-a text) (k skey))
  (defstrand init 3 (n-a n-a) (c c) (a a))
  (uniq-orig n-a)
  (auth (cat c a)))

;;; The initiator infers the presence of the server.  We can now add
;;; the assumptions that the server's channels
;;; have the same trust properties as before, ie ch1 is auth and ch is
;;; conf, in addition to the auth previously assumed:
(defskeleton yahalom
  (vars (k skey) (n-a n-b text) (a c b c-0 name))
  (defstrand init 3 (k k) (n-a n-a) (n-b n-b) (a a) (b b) (c c))
  (defstrand serv 2 (k k) (n-a n-a) (n-b n-b) (c c-0) (a a) (b b))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (uniq-orig k n-a)
  (auth (cat c a) (cat b c-0))
  (conf (cat c-0 a)))

;;; This now authenticates the presence of the responder for the first
;;; two nodes, and its agreement on all of the values present there.

;;; Finally, let us consider the server's point of view, with an
;;; authenticated channel for the request, and confidential channels
;;; over which to transmit the session key.

(defskeleton yahalom
  (vars (c a b name) (n-a n-b text) (k skey))
  (defstrand serv 3 (a a) (b b) (c c))
  (auth (cat b c))
  (conf (cat c b) (cat c a)))

;;; This query confirms that the server has authenticated the first
;;; two nodes of the responder, but has not authenticated the
;;; initiator at all.

;;; However, the session key is safe:

(defskeleton yahalom
  (vars (c a b name) (n-a n-b text) (k skey))
  (defstrand serv 3 (k k) (a a) (b b) (c c))
  (deflistener k)
  (auth (cat b c))
  (conf (cat c b) (cat c a)))
```

---

### `refrences/cpsa_kb/03_examples_scm/chan-perrig-song.scm`

*sha256:`28d099dc459d` · 48 lines · 1.0 KB (~258 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/chan-unilateral.scm`

*sha256:`65050edbf09c` · 61 lines · 1.3 KB (~321 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/chan-yahalom-role-decl.scm`

*sha256:`01f7233171d9` · 78 lines · 2.2 KB (~555 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/chan-yahalom.scm`

*sha256:`e3d108aed772` · 129 lines · 4.3 KB (~1,105 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/commitment.scm`

*sha256:`505c140833d9` · 44 lines · 1.5 KB (~379 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/comp_test.scm`

*sha256:`6fb561c2b579` · 156 lines · 4.7 KB (~1,196 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/completeness-test.scm`

*sha256:`32ffa577d5f7` · 56 lines · 1.5 KB (~388 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/crushing.scm`

*sha256:`9c7657aaef79` · 35 lines · 0.8 KB (~215 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/dass_simple.scm`

*sha256:`48d05f30a4f4` · 57 lines · 2.1 KB (~547 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/denning-sacco.scm`

*sha256:`5550b730f87a` · 27 lines · 0.8 KB (~212 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/deorig_contract.scm`

*sha256:`d2b82fe71e94` · 40 lines · 1.1 KB (~285 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/deorig_mesg.scm`

*sha256:`9455450b46ca` · 19 lines · 0.5 KB (~119 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/deorig_simple.scm`

*sha256:`61d250e40a22` · 30 lines · 0.9 KB (~238 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/dev-subatomic-open-closed.scm`

*sha256:`8c0adb757856` · 158 lines · 4.4 KB (~1,119 tokens) · lang:`scheme`*

```scheme
(herald
 dev-subatomic-open-closed
 (comment "Version that uses (dev const) pairs for locations"))

(defmacro (dev-key-state o k)
  (cat "st-k" o k))

(defmacro (opened o)
  (cat o o))

(defmacro (closed o) o)

(defmacro (dev-state-opened o)
  (cat "st" (opened o)))

(defmacro (dev-state-closed o)
  (cat "st" (closed o)))

(defmacro (dev-state-any o any)
  (cat "st" any))

(defprotocol subatomic-open-closed basic
  (defrole dev-up
    (vars (k skey) (d dev) (o name) (old old1 mesg) (start-ch chan))
    (trace
     (recv start-ch (cat "power-up" o k))
     (stor (cat d "lk") (dev-key-state o k))
     (stor (cat d "ls") (dev-state-closed o))
     (send (enc "up" k)))
    (auth start-ch)
    )

  (defrole owner-power-dev
    (vars (k skey) (o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d dev) (o name))
    (trace
     (send (enc "open" d o n k))
     (recv n)))

  (defrole owner-close
    (vars (k skey) (n text) (d dev) (o name))
    (trace
     (send (enc "close" d o n k))
     (recv n)))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d dev) (o name))
    (trace
     (recv (enc "open" d o n k))
     (load (cat d "lk") (dev-key-state o k))
     (stor (cat d "ls") (dev-state-opened o))
     (send n))
    (gen-st (dev-key-state o k) (dev-state-opened o))
    )

  (defrole dev-close
    (vars (k skey) (n text) (any mesg) (d dev) (o name))
    (trace
     (recv (enc "close" d o n k))
     (load (cat d "lk") (dev-key-state o k))
     (stor (cat d "ls") (dev-state-closed o))
     (send n))
    (gen-st (dev-key-state o k))
    )

  (defrole dev-pass
    (vars (k skey) (n text) (d dev) (o name))
    (trace
     (load (cat d "lk") (dev-key-state o k))
     (load (cat d "ls") (dev-state-opened o))
     (recv (enc "may I pass" k))
     (send (enc "you may pass" n k)))
    (uniq-orig n)
    (gen-st (dev-key-state o k) (dev-state-opened o))
    )

  (defrole user-pass
    (vars (k skey))
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

   ;; (defrule locName
   ;;   (forall
   ;;    ((l1 l2 locn) (m mesg))
   ;;    (implies
   ;;     (and (fact useLocName)
   ;; 	    (fact locName l1 m)
   ;; 	    (fact locName l2 m))
   ;;     (= l1 l2))))
)

(defskeleton subatomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand owner-power-dev 2 (k k))
  (deflistener k)
  (uniq-orig k)
  (facts (no-state-split)))

(defskeleton subatomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand dev-pass 4 (k k))
  (facts (no-state-split) (useLocName)))

(defskeleton subatomic-open-closed
	   (vars (k skey) (d o name) (n text) (start-ch chan))
	   (defstrand owner-power-dev 2 (k k))
	   (defstrand dev-pass 4 (k k))
	   (uniq-orig k)
	   (facts (no-state-split)))

;; When the locName rule is disabled CPSA considers it
;; possible that a given device may have several key-state
;; locations and several door-state locations. These wires
;; can get crossed. The locName fact and rule allow us to
;; treat ls and lk as fixed constant addresses on each
;; device d. 
(defskeleton subatomic-open-closed
  (vars (k skey) (d o name) (n text) (start-ch chan))
  (defstrand dev-pass 4 (k k))
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

### `refrences/cpsa_kb/03_examples_scm/devlocn.scm`

*sha256:`4042cb1ac22f` · 108 lines · 2.9 KB (~734 tokens) · lang:`scheme`*

```scheme
(herald "Dev and Locn" 
  (comment "This tests the feature that allows loads and stors to have any message in their location position."))

(defprotocol devlocn basic
  (defrole init
    (vars (d dev) (l1 l2 locn) (n1 n2 data) (k skey))
    (trace
     (stor (cat d l1) n1)
     (stor (cat d l2) n2)
     (send (enc d l1 k))
     (send (enc d l2 k)))
    (uniq-orig n1 n2 d))
  (defrole resp
    (vars (d dev) (l locn) (m mesg) (k skey))
    (trace
     (recv (enc d l k))
     (load (cat d l) m)
     (send m))
    (non-orig k))) 

(defskeleton devlocn
  (vars (n1 n2 data))
  (defstrand init 2 (n1 n1) (n2 n2))
  (deflistener n1)
  (deflistener n2))

(defprotocol devlocn basic
  (defrole init
    (vars (d dev) (l1 l2 locn) (n1 n2 data) (k skey))
    (trace
     (stor (cat d l1) n1)
     (send (enc d l1 k)))
    (uniq-orig n1 l1))
  (defrole resp
    (vars (d dev) (l locn) (m mesg) (k skey))
    (trace
     (recv (enc d l k))
     (load (cat d l) m)
     (send m))
    (non-orig k))) 

(defskeleton devlocn
  (vars (n1 n2 data))
  (defstrand init 1 (n1 n1))
  (defstrand init 1 (n1 n2))
  (deflistener n1)
  (deflistener n2))

(defskeleton devlocn
  (vars (n1 n2 data) (d1 d2 dev))
  (defstrand init 1 (n1 n1) (d d1))
  (defstrand init 1 (n1 n2) (d d2))
  (deflistener n1)
  (deflistener n2)
  (facts (neq d1 d2))
  (comment "With different devices they cannot have the same source."))

(defskeleton devlocn
  (vars (n1 n2 data) (l1 l2 locn))
  (defstrand init 1 (n1 n1) (l1 l1))
  (defstrand init 1 (n1 n2) (l1 l2))
  (deflistener n1)
  (deflistener n2)
  (facts (neq l1 l2))
  (comment "With different locns they cannot have the same source."))

(defskeleton devlocn
  (vars (n1 n2 data) (l1 l2 locn) (d dev))
  (defstrand init 1 (n1 n1) (l1 l1) (d d))
  (defstrand init 1 (n1 n2) (l1 l2) (d d))
  (deflistener n1)
  (deflistener n2)
  (facts (neq l1 l2))
  (comment "With different locns they cannot have the same source even if the devs are the same."))


(defprotocol devlocn basic
  (defrole init
    (vars (d dev) (l1 l2 locn) (n1 n2 data) (k skey))
    (trace
     (stor (cat d l1) n1)
     (send (enc d l1 k)))
    (uniq-orig n1 l1))
  (defrole resp
    (vars (d dev) (l locn) (dl m mesg) (k skey))
    (trace
     (recv (enc dl k))
     (load dl m)
     (send m)
     )
    (non-orig k))
  (comment "Notice the mesg var dl as location for load. Only allowed because it is acquired."))

(defskeleton devlocn
  (vars (m mesg))
  (defstrand resp 2 (m m))
  (gen-st m))

(defskeleton devlocn
  (vars (m mesg))
  (defstrand resp 2 (m m))
  (comment "Possibly strange interpretation. Init has uniq-orig n1 and l1. Resp doesn't necessarily retrieve n1, even though nobody but Init should know l1, so nobody else could stor into it."))

(defskeleton devlocn
  (vars (n data))
  (defstrand resp 2 (m n))
  (defstrand init 2 (n1 n))
  (comment "Even if loaded value is not gen-st, since it's uniq-orig, nonce-test still applies."))
```

---

### `refrences/cpsa_kb/03_examples_scm/dh-ca_hack.scm`

*sha256:`f94fc6424084` · 66 lines · 2.0 KB (~506 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/dh_encrypt_hack.scm`

*sha256:`7cc99c4130f6` · 53 lines · 1.4 KB (~369 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/dh_group_sig.scm`

*sha256:`27fb57e12cbf` · 70 lines · 1.6 KB (~418 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/dh_group_sig_auth_failure.scm`

*sha256:`7aef504be50e` · 59 lines · 1.4 KB (~370 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/dh_mim_hack.scm`

*sha256:`40710e381d87` · 31 lines · 1.0 KB (~250 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/dhnsl_hack.scm`

*sha256:`1988a950f6f8` · 44 lines · 1.3 KB (~339 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/dhstatic-state.scm`

*sha256:`a49573f51e24` · 67 lines · 2.0 KB (~503 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/disclosure.scm`

*sha256:`03f8b49cc6eb` · 33 lines · 1.0 KB (~244 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/doorsep.scm`

*sha256:`b727325455f4` · 33 lines · 0.8 KB (~207 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/doorsep2invk.scm`

*sha256:`7fe92d6d7c55` · 27 lines · 1.0 KB (~261 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/encsig.scm`

*sha256:`480f80c2eea1` · 44 lines · 1.5 KB (~375 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/envelope.scm`

*sha256:`0c2f85eb6f6b` · 204 lines · 6.6 KB (~1,686 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/epmo-hash.scm`

*sha256:`57d5e38dc720` · 77 lines · 2.7 KB (~682 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/epmo-key-hash.scm`

*sha256:`f779124fc6fe` · 77 lines · 2.7 KB (~700 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/epmo.scm`

*sha256:`619a6b134674` · 80 lines · 2.8 KB (~713 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/epmo_acctnum-key-hash.scm`

*sha256:`9590f59d5844` · 100 lines · 3.8 KB (~960 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/expand.scm`

*sha256:`80a54a16b03e` · 18 lines · 0.3 KB (~81 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/facts.scm`

*sha256:`e6a2686168e7` · 95 lines · 2.4 KB (~612 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/factvar.scm`

*sha256:`fb9d3f74d9e3` · 32 lines · 0.7 KB (~175 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/ffgg.scm`

*sha256:`5b0ba3591e9d` · 24 lines · 0.7 KB (~167 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/fluffy_draft03_gske.scm`

*sha256:`c6039262563d` · 114 lines · 3.5 KB (~903 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/fragile_pruning.scm`

*sha256:`5c19c39ed044` · 45 lines · 1.2 KB (~314 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/goals.scm`

*sha256:`b1ae1766178a` · 240 lines · 7.5 KB (~1,913 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/goalsvar.scm`

*sha256:`0d26a1fa46e2` · 229 lines · 6.7 KB (~1,715 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/hashtest-key-hash.scm`

*sha256:`a9914930ffa5` · 25 lines · 0.4 KB (~114 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/hashtest.scm`

*sha256:`3ff3a8f0d1cc` · 25 lines · 0.4 KB (~112 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/incompleteness_example.scm`

*sha256:`d6fcb0502d3d` · 21 lines · 0.6 KB (~164 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/isoreject-corrected.scm`

*sha256:`caf4ace8ece3` · 24 lines · 0.6 KB (~156 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/isoreject.scm`

*sha256:`9280d47d1adc` · 22 lines · 0.6 KB (~142 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/kelly1.scm`

*sha256:`757b6d34a380` · 76 lines · 2.1 KB (~545 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/kerberos.scm`

*sha256:`63adf8e0bcea` · 37 lines · 1.3 KB (~334 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/lemmas.scm`

*sha256:`c815266aaa57` · 61 lines · 1.7 KB (~424 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/locn_envelope.scm`

*sha256:`b76bdb322e9d` · 254 lines · 8.1 KB (~2,062 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/missing_contraction.scm`

*sha256:`327190aada48` · 54 lines · 1.8 KB (~470 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/neq_test.scm`

*sha256:`0602413ce18e` · 30 lines · 0.7 KB (~178 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/neuman-stubblebine.scm`

*sha256:`c2208789c13a` · 37 lines · 1.2 KB (~314 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/no_contraction.scm`

*sha256:`160793310026` · 16 lines · 0.4 KB (~96 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/non_transforming.scm`

*sha256:`ec45277f12c7` · 42 lines · 1.0 KB (~246 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/nonaug-prune.scm`

*sha256:`5274cf847e16` · 42 lines · 1.2 KB (~297 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/ns-l.scm`

*sha256:`1eebc4fe0c3f` · 38 lines · 1.0 KB (~260 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/ns-rebinding.scm`

*sha256:`f9af085a3c0b` · 103 lines · 2.7 KB (~701 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/ns.scm`

*sha256:`436649066c0e` · 37 lines · 1.0 KB (~256 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/nsl3.scm`

*sha256:`8bc8612a71fd` · 55 lines · 1.5 KB (~381 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/nslsk.scm`

*sha256:`139b149a6a68` · 51 lines · 1.3 KB (~320 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/open-closed-multiloc.scm`

*sha256:`06aac6425c95` · 166 lines · 4.5 KB (~1,140 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/open-closed-tag.scm`

*sha256:`077b13ff8584` · 149 lines · 3.8 KB (~978 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/open-closed.scm`

*sha256:`ffb860449ac3` · 180 lines · 4.8 KB (~1,233 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/or.scm`

*sha256:`8bdc4e82cc5e` · 27 lines · 0.9 KB (~222 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/ordered.scm`

*sha256:`c0c9185c45bf` · 39 lines · 0.7 KB (~189 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/orderedvar.scm`

*sha256:`aa7cdc6a6107` · 39 lines · 0.7 KB (~191 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/pca.scm`

*sha256:`298053fef263` · 36 lines · 1.1 KB (~282 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/pen-non-orig-test.scm`

*sha256:`43ea68bd790c` · 29 lines · 0.8 KB (~198 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/pfs-via-pubkey.scm`

*sha256:`49b7b5024629` · 35 lines · 1.2 KB (~296 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/pkinit.scm`

*sha256:`424045fb7b6f` · 22 lines · 0.7 KB (~172 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/preprocess.scm`

*sha256:`85f407700b4e` · 27 lines · 0.8 KB (~215 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/print.scm`

*sha256:`5461454e4b17` · 13 lines · 0.4 KB (~114 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/prottrans.scm`

*sha256:`506c69f72936` · 107 lines · 2.8 KB (~725 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/pruning1.scm`

*sha256:`6c32b763e3f2` · 42 lines · 1.4 KB (~352 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/puzzle_example.scm`

*sha256:`9786d9060676` · 73 lines · 2.1 KB (~532 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/reflect.scm`

*sha256:`d28cf4717229` · 32 lines · 0.6 KB (~165 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/renamings.scm`

*sha256:`26877988b9f1` · 30 lines · 0.9 KB (~233 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/role_uniq.scm`

*sha256:`44cb41cd7701` · 56 lines · 1.6 KB (~403 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/rule-node.scm`

*sha256:`d623459ea1e4` · 88 lines · 1.8 KB (~467 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/rule-order.scm`

*sha256:`02735c6e55ef` · 21 lines · 0.3 KB (~87 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/rules.scm`

*sha256:`2761f75fd5bd` · 67 lines · 1.6 KB (~401 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/scep-tls-dh-broken.scm`

*sha256:`b1818bb80bb3` · 140 lines · 4.7 KB (~1,191 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/scep-tls-dh-fixed.scm`

*sha256:`f58ff6535265` · 141 lines · 4.8 KB (~1,211 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-auth-enc-full-payload.scm`

*sha256:`ca74511ed9c2` · 226 lines · 10.5 KB (~2,675 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-auth-enc-logic.scm`

*sha256:`8f15c79e0913` · 55 lines · 2.5 KB (~630 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-auth-full-payload.scm`

*sha256:`3a36093acaf5` · 226 lines · 9.8 KB (~2,521 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-auth-logic.scm`

*sha256:`69e52ed30db5` · 75 lines · 3.0 KB (~765 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-enc-logic.scm`

*sha256:`ab76741609f5` · 78 lines · 2.7 KB (~701 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-challenge-auth.scm`

*sha256:`350ed2a1d1d9` · 49 lines · 2.7 KB (~681 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-challenge-authenc.scm`

*sha256:`d4e5673b3ddc` · 51 lines · 3.0 KB (~764 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-challenge.scm`

*sha256:`312adef361d9` · 40 lines · 1.3 KB (~327 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-key-activation-auth.scm`

*sha256:`a6bc99dd2efc` · 40 lines · 1.7 KB (~447 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-key-activation-authenc.scm`

*sha256:`6367eb4a2d12` · 42 lines · 2.0 KB (~520 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-key-activation.scm`

*sha256:`8e5407169d35` · 28 lines · 0.8 KB (~207 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-otar-auth.scm`

*sha256:`3361496cd892` · 49 lines · 2.5 KB (~636 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-otar-authenc.scm`

*sha256:`9c21a336cca3` · 51 lines · 2.8 KB (~710 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-otar-transmission.scm`

*sha256:`c6cab6fa329e` · 50 lines · 1.7 KB (~431 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-rekey-auth.scm`

*sha256:`efa36900f119` · 47 lines · 2.4 KB (~603 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-rekey-authenc.scm`

*sha256:`161329f435d8` · 49 lines · 2.6 KB (~677 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-rekey.scm`

*sha256:`f4d29e1126d6` · 36 lines · 1.4 KB (~353 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-start-auth.scm`

*sha256:`176085a6c5c2` · 40 lines · 1.8 KB (~454 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-start-authenc.scm`

*sha256:`61c0b0266d5c` · 42 lines · 2.1 KB (~527 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sdls-ep-sa-start.scm`

*sha256:`db963aab66d9` · 38 lines · 1.1 KB (~280 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sigenc.scm`

*sha256:`7de7f622deba` · 44 lines · 1.5 KB (~375 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sorted_epmo_acctnum.scm`

*sha256:`3e81474246f0` · 90 lines · 3.3 KB (~846 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sts.scm`

*sha256:`f4cba59e4388` · 81 lines · 2.2 KB (~575 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sts_non_role.scm`

*sha256:`1b34a75f590e` · 98 lines · 2.6 KB (~659 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sts_weakened_reflect.scm`

*sha256:`c639a40306a4` · 80 lines · 2.3 KB (~577 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/subatomic-open-closed-test-genrule.scm`

*sha256:`819efab85760` · 227 lines · 8.4 KB (~2,158 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/subatomic-open-closed.scm`

*sha256:`eae2ff6d0a48` · 165 lines · 4.6 KB (~1,185 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sync_locn_envelope.scm`

*sha256:`c0dfe134ad6c` · 303 lines · 9.6 KB (~2,456 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/sync_locn_envelope_no_auth.scm`

*sha256:`e234dfddd0b0` · 299 lines · 9.2 KB (~2,349 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/targetterms1.scm`

*sha256:`c2c1a27820ba` · 21 lines · 0.6 KB (~141 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/targetterms2.scm`

*sha256:`1910a7315f43` · 36 lines · 1.3 KB (~326 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/targetterms6.scm`

*sha256:`4a93026b8f2e` · 56 lines · 2.2 KB (~551 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/targetterms8.scm`

*sha256:`25e015e83177` · 64 lines · 2.2 KB (~570 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/thisthat.scm`

*sha256:`ff8fb574f088` · 31 lines · 0.9 KB (~227 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/tickle-unique.scm`

*sha256:`7a2222c13440` · 39 lines · 0.8 KB (~216 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/timestamping.scm`

*sha256:`82003a7aeb20` · 46 lines · 1.4 KB (~367 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/trust-anchor.scm`

*sha256:`29e459309918` · 19 lines · 0.5 KB (~130 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/ugen-at.scm`

*sha256:`b5797b5eddf5` · 53 lines · 1.3 KB (~323 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/ugo.scm`

*sha256:`a9bb4281d911` · 110 lines · 2.8 KB (~707 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/uncarried_keys.scm`

*sha256:`f8f5a1fac5e9` · 30 lines · 0.9 KB (~241 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/unilateral.scm`

*sha256:`3f30672cadd0` · 89 lines · 2.3 KB (~588 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/uniq-at.scm`

*sha256:`d8ec10d3158a` · 53 lines · 1.3 KB (~324 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/uniq-gen-test.scm`

*sha256:`863bc5bd5cfd` · 35 lines · 0.8 KB (~214 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/uo.scm`

*sha256:`4e212592b42d` · 25 lines · 0.7 KB (~175 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/wang-hash.scm`

*sha256:`e49573e42a15` · 434 lines · 12.2 KB (~3,129 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/wang-key-hash.scm`

*sha256:`362536a1eb34` · 434 lines · 12.2 KB (~3,128 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/weird.scm`

*sha256:`c90e3b9beb58` · 58 lines · 1.3 KB (~338 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/wonthull.scm`

*sha256:`2e7e04acefd5` · 40 lines · 1.1 KB (~281 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/wonthull2.scm`

*sha256:`ec51d8d163d6` · 38 lines · 1.0 KB (~265 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/wonthull3.scm`

*sha256:`37101d7ff334` · 36 lines · 0.9 KB (~226 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/woolam.scm`

*sha256:`9b5ddc1d5e38` · 26 lines · 0.7 KB (~169 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/yahalom-6.3.6.scm`

*sha256:`6ad926c80e47` · 53 lines · 1.7 KB (~434 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/yahalom-forward.scm`

*sha256:`06698f095963` · 41 lines · 1.2 KB (~307 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/yahalom.scm`

*sha256:`e403b0a15ffb` · 34 lines · 1.0 KB (~259 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/03_examples_scm/yes-or-no.scm`

*sha256:`44271b6e83a9` · 52 lines · 1.3 KB (~333 tokens) · lang:`scheme`*

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

### `refrences/cpsa_kb/04_examples_catalog/01_scm_examples_A_to_G.md`

*sha256:`e8ca58d30ce2` · 2487 lines · 138.6 KB (~35,455 tokens) · lang:`markdown`*

````markdown
# Official MITRE CPSA Examples Catalog (Part 1: DH_hack.scm to goalsvar.scm)

This catalog documents the first 50 official MITRE CPSA `.scm` example files (`DH_hack.scm` through `goalsvar.scm`, sorted alphabetically) from `03_examples_scm/`. Every declaration, role, sort, trace event, rule, goal, macro, and S-expression excerpt is extracted directly from the source `.scm` files.

---

## DH_hack.scm

- **File Path**: `03_examples_scm/DH_hack.scm`
- **Algebra & Herald**: `(herald "DH Hack" (bound 15))` — `basic` algebra (declared in `(defprotocol DH_hack basic ...)`), with herald flag `(bound 15)`.
- **Protocol & Purpose**: Demonstrates a limited technique for approximating Diffie-Hellman (DH) key agreement inside the `basic` crypto algebra. A DH key pair $(x, g^x)$ is modeled as `((invk x), x)` of sort `akey`, where the owner of `(invk x)` computes `(hash (invk x) y)` and the owner of `(invk y)` computes `(hash x (invk y))`. An auxiliary `commute` role translates encryptions under `(hash (invk x) y)` into encryptions under `(hash x (invk y))`, preventing decryption unless the adversary possesses either `(invk x)` or `(invk y)` while ignoring algebraic DH properties.
- **Roles & Variables**:
  - `init1`:
    - `(vars (gcs name) (cek skey) (x y akey) (d data))`
    - Role-level assumptions: `(uniq-orig cek d x)`
    - Trace: `(send (enc x (enc cek (hash (invk x) y)) (enc d cek) (privk gcs)))`
  - `resp`:
    - `(vars (gcs name) (cek skey) (x y akey) (d data))`
    - Role-level assumptions: `(non-orig (privk gcs))`
    - Trace: `(recv (enc x (enc cek (hash x (invk y))) (enc d cek) (privk gcs)))`
  - `commute`:
    - `(vars (gcs name) (cek skey) (x y akey) (d data))`
    - Role-level assumptions: `(non-orig (privk gcs))`
    - Trace: `(recv (enc x (enc cek (hash (invk x) y)) (enc d cek) (privk gcs)))` followed by `(send (enc x (enc cek (hash x (invk y))) (enc d cek) (privk gcs)))`
- **Skeletons, Goals, Rules & Macros**:
  - Contains 6 `(defskeleton DH_hack ...)` queries testing `resp` of height 1:
    1. `(defstrand resp 1 (x x) (y y))` with `(non-orig (invk x) (invk y))`
    2. `(defstrand resp 1 (cek cek) (x x))` with `(non-orig (invk x))`
    3. `(defstrand resp 1 (cek cek) (y y))` with `(non-orig (invk y))`
    4. `(defstrand resp 1 (cek cek) (x x) (y y))` with `(deflistener cek)` and `(non-orig (invk x) (invk y))`
    5. `(defstrand resp 1 (cek cek) (x x))` with `(deflistener cek)` and `(non-orig (invk x))`
    6. `(defstrand resp 1 (cek cek) (y y))` with `(deflistener cek)` and `(non-orig (invk y))`
  - No rules, lemmas, goals, or macros.
- **When to Reference This Example**: Reference this example when modeling a protocol in the `basic` algebra that requires a lightweight commutativity bridge (via an auxiliary `commute` role and `(hash (invk x) y)` / `(hash x (invk y))`) without switching the entire protocol to the `diffie-hellman` algebra.
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## ab.scm

- **File Path**: `03_examples_scm/ab.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol ab basic ...)`.
- **Protocol & Purpose**: Models a minimal "A-B cascading" non-termination/dead-skeleton pattern. An initiator sends `(enc x k)` and expects `(enc x x k)`, while roles `A` and `B` each output `(enc x x k)` only after receiving `(enc "A" x k)` or `(enc "B" x k)` respectively. Because nothing can ever produce the `"A"` or `"B"` tagged inputs under secret key `k`, the input skeleton is dead, illustrating how roles that appear to make progress on an encrypted return format fail when their preconditions cannot be satisfied.
- **Roles & Variables**:
  - `init`:
    - `(vars (x text) (k skey))`
    - Role-level assumptions: `(uniq-orig x)` and `(non-orig k)`
    - Trace: `(send (enc x k))`, `(recv (enc x x k))`
  - `A`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "A" x k))`, `(send (enc x x k))`
  - `B`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "B" x k))`, `(send (enc x x k))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton ab (vars (x text) (k skey)) (defstrand init 2 (x x) (k k)))`.
  - Uses `uniq-orig` and `non-orig` at the role level; no rules, goals, or macros.
- **When to Reference This Example**: Reference this example when diagnosing dead skeletons (0 shapes produced) or search cascading where responder roles emit the message pattern expected by an initiator (`(enc x x k)`) but require an unreachable encrypted tag (`(enc "A" x k)`) in their `recv` event.
- **Key S-Expression Excerpt**:
```scheme
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

## abc.scm

- **File Path**: `03_examples_scm/abc.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol abc basic ...)`.
- **Protocol & Purpose**: Extends `ab.scm` to three auxiliary roles (`A`, `B`, and `C`) to demonstrate three-way A-B-C cascading on a dead skeleton. Roles `A`, `B`, and `C` each produce `(enc x x k)` upon receiving `(enc "A" x k)`, `(enc "B" x k)`, or `(enc "C" x k)`, none of which can be constructed from the initiator's `(send (enc x k))` when `k` is `non-orig`.
- **Roles & Variables**:
  - `init`:
    - `(vars (x text) (k skey))`
    - Role-level assumptions: `(uniq-orig x)`, `(non-orig k)`
    - Trace: `(send (enc x k))`, `(recv (enc x x k))`
  - `A`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "A" x k))`, `(send (enc x x k))`
  - `B`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "B" x k))`, `(send (enc x x k))`
  - `C`:
    - `(vars (x text) (k skey))`
    - Trace: `(recv (enc "C" x k))`, `(send (enc x x k))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton abc (vars (x text) (k skey)) (defstrand init 2 (x x) (k k)))`.
  - Uses `uniq-orig` and `non-orig` inside `defrole init`.
- **When to Reference This Example**: Reference this example alongside `ab.scm` to understand multi-branch cohort cascading and dead-skeleton termination when multiple roles share identical outgoing ciphertexts but incompatible incoming tags.
- **Key S-Expression Excerpt**:
```scheme
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

## aik.scm

- **File Path**: `03_examples_scm/aik.scm`
- **Algebra & Herald**: `(herald "Anonymous identity protocol from TCG")` — `basic` algebra (`(defprotocol aikprot basic ...)`), no extra herald flags.
- **Protocol & Purpose**: Models the Trusted Computing Group (TCG) Anonymous Identity Key (AIK) credential issuance protocol (`aikprot`) involving a manufacturer CA (`ca`), a Trusted Platform Module (`tpm`), and a Privacy CA (`pca`). The CA issues an endorsement key certificate `(enc "ekc" mf ek (privk mf))`, the TPM generates a fresh AIK pair `(k, (invk k))` and requests an anonymous identity certificate `(enc "aic" i k x (privk pc))` encrypted under `ek`, and the TPM subsequently exports `(enc k (invk k) srk)` wrapped under the Storage Root Key `srk`.
- **Roles & Variables**:
  - `ca`:
    - `(vars (mf name) (ek akey))`
    - Role-level assumptions: `(non-orig (invk ek))`
    - Trace: `(send (enc "ekc" mf ek (privk mf)))`
  - `tpm`:
    - `(vars (i x mf pc name) (ek k akey) (srk skey))`
    - Role-level assumptions: `(non-orig srk (invk ek))` and `(uniq-orig k (invk k))`
    - Trace:
      1. `(recv (cat x i (enc "ekc" mf ek (privk mf))))`
      2. `(send (cat i k x (enc "ekc" mf ek (privk mf))))`
      3. `(recv (enc (enc "aic" i k x (privk pc)) ek))`
      4. `(send (cat (enc "aic" i k x (privk pc)) (enc k (invk k) srk)))`
  - `pca`:
    - `(vars (i x mf pc name) (ek k akey))`
    - Role-level assumptions: `(non-orig (privk mf))`
    - Trace:
      1. `(recv (cat i k x (enc "ekc" mf ek (privk mf))))`
      2. `(send (enc (enc "aic" i k x (privk pc)) ek))`
- **Skeletons, Goals, Rules & Macros**:
  - Two `(defskeleton aikprot ...)` blocks:
    1. Full `tpm` strand of height 4 (`(defstrand tpm 4 (mf mf) (pc pc))`) with `(non-orig (privk pc))`.
    2. Listener skeleton (`(deflistener (enc "aic" i k x (privk pc)))`) with `(non-orig (privk pc))`.
- **When to Reference This Example**: Reference this example when modeling PKI certificate enrollment, Privacy CA / TPM AIK issuance, or generating asymmetric key pairs on the fly where both `k` and `(invk k)` are declared `(uniq-orig k (invk k))` and wrapped under a symmetric storage key `srk`.
- **Key S-Expression Excerpt**:
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
```

---

## atomic-open-closed.scm

- **File Path**: `03_examples_scm/atomic-open-closed.scm`
- **Algebra & Herald**: `(herald atomic-open-closed (bound 44))` (with commented-out flags `;; (try-old-strands)`, `;; (check-nonces)`, `;; (reverse-nodes)`) — `basic` algebra (`(defprotocol atomic-open-closed basic ...)`).
- **Protocol & Purpose**: Models a stateful device (`d`) controlled by an owner (`o`) using two mutable state locations (`lk` and `ls` of sort `locn`) and a power-up channel (`start-ch` of sort `chan`). The device transitions between closed (`(dev-state-closed d o)`) and opened (`(dev-state-opened d o)`) states via `load` and `stor` trace events, and only allows a user to pass (`dev-pass`) when `ls` holds `(dev-state-opened d o)`. Extensive `defrule` axioms enforce state-generation (`gen-st`), same-device register pairing (`(fact same-dev ls lk)`), single-threaded register ordering, strand completion, and multi-step `load`/`stor` atomicity.
- **Roles & Variables**:
  - `dev-up`: `(vars (k skey) (d o name) (old old1 mesg) (start-ch chan) (lk ls locn))`, `(auth start-ch)`, trace: `(recv start-ch (cat "power-up" d o k))`, `(load lk old)`, `(stor lk (dev-key-state d o k))`, `(load ls old1)`, `(stor ls (dev-state-closed d o))`, `(send (enc "up" k))`
  - `owner-power-dev`: `(vars (k skey) (d o name) (start-ch chan))`, `(conf start-ch)`, trace: `(send start-ch (cat "power-up" d o k))`, `(recv (enc "up" k))`
  - `owner-open`: `(vars (k skey) (n text) (d o name))`, trace: `(send (enc "open" d o n k))`, `(recv n)`
  - `owner-close`: `(vars (k skey) (n text) (d o name))`, trace: `(send (enc "close" d o n k))`, `(recv n)`
  - `dev-open`: `(vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))`, trace: `(recv (enc "open" d o n k))`, `(load lk (dev-key-state d o k))`, `(load ls (dev-state-any d o any))`, `(stor ls (dev-state-opened d o))`, `(send n)`
  - `dev-close`: `(vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))`, trace: `(recv (enc "close" d o n k))`, `(load lk (dev-key-state d o k))`, `(load ls (dev-state-any d o any))`, `(stor ls (dev-state-closed d o))`, `(send n)`
  - `dev-pass`: `(vars (k skey) (n text) (d o name) (lk ls locn))`, `(uniq-orig n)`, trace: `(recv (enc "may I pass" k))`, `(load lk (dev-key-state d o k))`, `(load ls (dev-state-opened d o))`, `(send (enc "you may pass" n k))`
  - `user-pass`: `(vars (k skey) (n text) (d o name) (l locn))`, trace: `(send (enc "may I pass" k))`, `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros** (`defmacro`): `(dev-key-state d o k)`, `(opened o)`, `(closed o)`, `(dev-state-opened d o)`, `(dev-state-closed d o)`, `(dev-state-any d o any)`.
  - **Rules** (`defrule`): 31 active rules covering:
    - `gen-st` state-generation declarations: `gen-state-close`, `gen-state-pass`, `gen-state-open`, `gen-state-close` (for `dev-key-state`), `gen-state-pass` (for `dev-key-state`).
    - Uniqueness & register coupling via `fact`: `power-deliver-once`, `intro-same-dev-up`, `intro-same-dev-open`, `intro-same-dev-close`, `intro-same-dev-pass`, `same-dev-ls-lk`, `same-dev-lk-ls`.
    - Single-threaded location ordering (`prec`): `single-thread-up-up`, `single-thread-up-open`, `single-thread-up-close`, `single-thread-open-open`, `single-thread-ls-open-close`, `single-thread-close-close`, `atomic-up-pass`.
    - Strand completion & atomic load/stor transitions: `dev-up-completes`, `dev-open-completes`, `dev-close-completes`, `dev-pass-completes`, `dev-up-atomic1`, `dev-up-atomic2`, `dev-open-atomic1`, `dev-open-atomic2`, `dev-close-atomic1`, `dev-close-atomic2`, `dev-pass-atomic1`, `dev-pass-atomic2`.
  - **Skeletons**: 3 active `(defskeleton atomic-open-closed ...)` queries testing `owner-power-dev` with `(deflistener k)`, `dev-pass` alone, and `owner-power-dev` + `dev-pass` with `(uniq-orig k)`.
- **When to Reference This Example**: Reference this example whenever modeling mutable device state with `locn`, `load`, and `stor` in CPSA, especially when you need `defrule` patterns for `gen-st`, multi-register coupling (`(fact same-dev ls lk)`), or atomic load-modify-store sequences using `prec` and sort `indx`.
- **Key S-Expression Excerpt**:
```scheme
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

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d o name) (lk ls locn))
    (trace
     (recv (enc "open" d o n k))
     (load lk (dev-key-state d o k))
     (load ls (dev-state-any d o any))
     (stor ls (dev-state-opened d o))
     (send n)))

  (defrule dev-open-atomic1
    (forall ((x z strd) (i1 indx))
      (implies
       (and (p "dev-open" z 4)
            (prec x i1 z 3))
       (or (= x z)
           (prec x i1 z 1))))))
```

---

## attest.scm

- **File Path**: `03_examples_scm/attest.scm`
- **Algebra & Herald**: `(herald attest-door)` — `basic` algebra across three protocol variants (`attest-door`, `attest-door-trust`, `attest-door-trust-attest`).
- **Protocol & Purpose**: Models a door entry protocol augmented with remote attestation (`appraise`) and a malicious "fake door" role (`squealer`) that leaks the session key `k`. Progressively refines the trust model across three protocols using `defrule` axioms:
  1. `attest-door`: Includes only rule `yes` (if an uncompromised appraiser `a` completes, the attested door `d` has an uncompromised private key `(non (invk d))`).
  2. `attest-door-trust`: Adds rule `trust` (a door `d` that passes appraisal cannot also act as a `squealer`, deriving `(false)`).
  3. `attest-door-trust-attest`: Adds rule `uncompromised-people-choose-uncompromised-appraisers` (an uncompromised `person` always queries an uncompromised appraiser `(non (invk a))`).
- **Roles & Variables**:
  - Identical across all 3 protocols (`attest-door`, `attest-door-trust`, `attest-door-trust-attest`):
    - `appraise`: `(vars (d p a akey) (n text))`, trace: `(recv (enc (enc d n (invk p)) a))`, `(send (enc n a p))`
    - `person`: `(vars (d p a akey) (k skey) (n t text))`, `(uniq-orig n k)`, trace: `(send (enc (enc d n (invk p)) a))`, `(recv (enc n a p))`, `(send (enc (enc k (invk p)) d))`, `(recv (enc t k))`, `(send t)`
    - `door`: `(vars (d p akey) (k skey) (t text))`, `(uniq-orig t)`, trace: `(recv (enc (enc k (invk p)) d))`, `(send (enc t k))`, `(recv t)`
    - `squealer`: `(vars (d p akey) (k skey) (t text))`, trace: `(recv (enc (enc k (invk p)) d))`, `(send k)`
- **Skeletons, Goals, Rules & Macros**:
  - **Rules**: `yes` (uses `exists` and `(non (invk d))`), `trust` (uses `(false)` to forbid a strand `w` of `squealer` sharing `d` with `appraise` strand `z`), and `uncompromised-people-choose-uncompromised-appraisers`.
  - **Skeletons**: 2 `(defskeleton ...)` blocks per protocol (6 total), analyzing `person` of height 5 with `(non-orig (invk p) (invk a))` and `door` of height 3 with `(non-orig (invk d) (invk p))`.
- **When to Reference This Example**: Reference this example when modeling remote attestation, key compromise / rogue peer exclusion (`squealer`), or writing `defrule` axioms that transfer `(non (invk ...))` trust from an appraiser/authority to a peer or rule out dishonest roles via `(false)`.
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## auth-enc.scm

- **File Path**: `03_examples_scm/auth-enc.scm`
- **Algebra & Herald**: `(herald auth-enc)` — `basic` algebra (`(defprotocol auth-enc basic ...)`).
- **Protocol & Purpose**: Minimal roletran-annotated protocol demonstrating transmission of an encrypted nonce `(enc n k)` followed by the plaintext nonce and key `(cat n k)` over an authenticated channel `ch`. Uses `(inputs ...)` and `(outputs ...)` declarations inside `defrole`.
- **Roles & Variables**:
  - `init`:
    - `(vars (n text) (k skey) (ch chan))`
    - Role-level assumptions & I/O: `(uniq-orig n k)`, `(inputs ch)`
    - Trace: `(send ch (enc n k))`, `(send ch (cat n k))`
  - `resp`:
    - `(vars (n text) (k skey) (ch chan))`
    - Role-level I/O: `(inputs ch)`, `(outputs n)`
    - Trace: `(recv ch (enc n k))`, `(recv ch (cat n k))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton auth-enc (vars (ch chan)) (defstrand resp 2 (ch ch)) (auth ch))`.
- **When to Reference This Example**: Reference this example for the exact syntax of `(inputs ...)` and `(outputs ...)` role declarations (used by `cpsa4roletran`) combined with channel-authenticated `(send ch ...)` / `(recv ch ...)` events and `(auth ch)`.
- **Key S-Expression Excerpt**:
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

## auth-hash.scm

- **File Path**: `03_examples_scm/auth-hash.scm`
- **Algebra & Herald**: `(herald auth-hash)` — `basic` algebra (`(defprotocol auth-hash basic ...)`).
- **Protocol & Purpose**: Companion to `auth-enc.scm` that sends a hash commitment `(hash n)` followed by `n` over an authenticated channel `ch`, with `(inputs ch)` and `(outputs n)` declarations for `cpsa4roletran` translation.
- **Roles & Variables**:
  - `init`:
    - `(vars (n text) (ch chan))`
    - Role-level assumptions & I/O: `(uniq-orig n)`, `(inputs ch)`
    - Trace: `(send ch (hash n))`, `(send ch n)`
  - `resp`:
    - `(vars (n text) (ch chan))`
    - Role-level I/O: `(inputs ch)`, `(outputs n)`
    - Trace: `(recv ch (hash n))`, `(recv ch n)`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton auth-hash (vars (ch chan)) (defstrand resp 2 (ch ch)) (auth ch))`.
- **When to Reference This Example**: Reference this example when using `(hash n)` commitments over an authenticated channel `(auth ch)` with `inputs`/`outputs` roletran annotations.
- **Key S-Expression Excerpt**:
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

## blanchet-strandmax.scm

- **File Path**: `03_examples_scm/blanchet-strandmax.scm`
- **Algebra & Herald**: `(herald "Blanchet's Simple Example Protocol (strand max)" (comment "There is a flaw in this protocol by design"))` — `basic` algebra across three protocols (`blanchet-max`, `blanchet-max-akey`, `blanchet-max-fixed`).
- **Protocol & Purpose**: Models Bruno Blanchet's classic flawed two-message signed-then-encrypted session key exchange (`init` sends `(enc (enc s (privk a)) (pubk b))`, `resp` replies with `(enc d s)`) and its fixed variant (`(enc (enc s b (privk a)) (pubk b))`, which binds the responder's identity `b` inside the signature). Demonstrates `(defstrandmax role ...)` syntax (which automatically specifies the full height of a role) as well as both named asymmetric keys (`pubk`/`privk`) and unnamed asymmetric keys (`akey`/`invk`).
- **Roles & Variables**:
  - In `blanchet-max` (named asymmetric keys):
    - `init`: `(vars (a b name) (s skey) (d data))`, trace: `(send (enc (enc s (privk a)) (pubk b)))`, `(recv (enc d s))`
    - `resp`: `(vars (a b name) (s skey) (d data))`, trace: `(recv (enc (enc s (privk a)) (pubk b)))`, `(send (enc d s))`
  - In `blanchet-max-akey` (unnamed asymmetric keys `akey`):
    - `init`: `(vars (a b akey) (s skey) (d data))`, trace: `(send (enc (enc s (invk a)) b))`, `(recv (enc d s))`
    - `resp`: `(vars (a b akey) (s skey) (d data))`, trace: `(recv (enc (enc s (invk a)) b))`, `(send (enc d s))`
  - In `blanchet-max-fixed` (fixed with `b` inside signature):
    - `init`: `(vars (a b name) (s skey) (d data))`, trace: `(send (enc (enc s b (privk a)) (pubk b)))`, `(recv (enc d s))`
    - `resp`: `(vars (a b name) (s skey) (d data))`, trace: `(recv (enc (enc s b (privk a)) (pubk b)))`, `(send (enc d s))`
- **Skeletons, Goals, Rules & Macros**:
  - 12 `(defskeleton ...)` blocks (4 per protocol: initiator perspective, initiator secrecy with `(deflistener d)`, responder perspective, responder secrecy with `(deflistener d)`).
  - The first 4 skeletons in `blanchet-max` use `(defstrandmax init ...)` and `(defstrandmax resp ...)` instead of explicit numeric strand heights.
- **When to Reference This Example**: Reference this example to see how `(defstrandmax <role> ...)` avoids hardcoding strand lengths in `defskeleton`, how to compare named (`(pubk b)`/`(privk a)`) vs. unnamed (`b`/`(invk a)`) asymmetric keys, and how omitting the recipient's identity inside a signed key transport message causes an authentication/secrecy flaw.
- **Key S-Expression Excerpt**:
```scheme
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
  (deflistener d)
  (non-orig (privk b))
  (uniq-orig s d)
  (comment "From the initiator's perspective, is the secret leaked?"))
```

---

## blanchet.scm

- **File Path**: `03_examples_scm/blanchet.scm`
- **Algebra & Herald**: `(herald "Blanchet's Simple Example Protocol" (comment "There is a flaw in this protocol by design"))` — `basic` algebra across two protocols (`blanchet` and `blanchet-fixed`).
- **Protocol & Purpose**: Standard version of Blanchet's flawed signed-then-encrypted key exchange (`blanchet`) and its recipient-bound fix (`blanchet-fixed`) using explicit strand heights `(defstrand init 2 ...)` and `(defstrand resp 2 ...)`. In `blanchet`, an initiator `a` signing `s` without `b`'s name allows a dishonest recipient to forward `(enc s (privk a))` re-encrypted under an honest responder `b`'s public key, whereas `blanchet-fixed` signs `(enc s b (privk a))`.
- **Roles & Variables**:
  - In `blanchet`:
    - `init`: `(vars (a b name) (s skey) (d data))`, trace: `(send (enc (enc s (privk a)) (pubk b)))`, `(recv (enc d s))`
    - `resp`: `(vars (a b name) (s skey) (d data))`, trace: `(recv (enc (enc s (privk a)) (pubk b)))`, `(send (enc d s))`
  - In `blanchet-fixed`:
    - `init`: `(vars (a b name) (s skey) (d data))`, trace: `(send (enc (enc s b (privk a)) (pubk b)))`, `(recv (enc d s))`
    - `resp`: `(vars (a b name) (s skey) (d data))`, trace: `(recv (enc (enc s b (privk a)) (pubk b)))`, `(send (enc d s))`
- **Skeletons, Goals, Rules & Macros**:
  - 8 `(defskeleton ...)` blocks (4 for `blanchet`, 4 for `blanchet-fixed`) testing initiator and responder perspectives with and without `(deflistener d)`, using `(non-orig (privk b))`, `(non-orig (privk a) (privk b))`, `(uniq-orig s)`, and `(uniq-orig s d)`.
- **When to Reference This Example**: Reference this example as the canonical template for analyzing both authentication and payload secrecy (`(deflistener d)` with `(uniq-orig s d)`) from initiator and responder perspectives in a public-key session key transport protocol.
- **Key S-Expression Excerpt**:
```scheme
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
  (deflistener d)
  (non-orig (privk b))
  (uniq-orig s d)
  (comment "From the initiator's perspective, is the secret leaked?"))
```

---

## bug_example.scm

- **File Path**: `03_examples_scm/bug_example.scm`
- **Algebra & Herald**: `(herald bug_example (bound 20))` — `basic` algebra (`(defprotocol bug_example basic ...)`), with herald flag `(bound 20)`.
- **Protocol & Purpose**: Contains two definitions of `bug_example` that test inverse-key (`invk`) flipping inside hashed encryption keys `(hash x (invk y))` vs. `(hash (invk x) y)`. In the first protocol definition, a single `flip` role receives `(enc k (hash k1 k2))` and sends `(enc k (hash (invk k1) (invk k2)))` (relying on `(invk (invk k)) = k` unification). In the second definition, two roles `flip1` and `flip2` explicitly match `(hash (invk k1) k2)` and `(hash k1 (invk k2))` respectively.
- **Roles & Variables**:
  - First `(defprotocol bug_example basic ...)`:
    - `init`: `(vars (x y akey))`, `(non-orig (invk y) (invk x))`, trace: `(send (enc y (hash x (invk y))))`
    - `resp`: `(vars (x y akey))`, `(non-orig (invk x) (invk y))`, trace: `(recv (enc y (hash (invk x) y)))`
    - `flip`: `(vars (k k1 k2 akey))`, trace: `(recv (enc k (hash k1 k2)))`, `(send (enc k (hash (invk k1) (invk k2))))`
  - Second `(defprotocol bug_example basic ...)`:
    - `init`: `(vars (x y akey))`, `(non-orig (invk y) (invk x))`, trace: `(send (enc y (hash x (invk y))))`
    - `resp`: `(vars (x y akey))`, `(non-orig (invk x) (invk y))`, trace: `(recv (enc y (hash (invk x) y)))`
    - `flip1`: `(vars (k k1 k2 akey))`, trace: `(recv (enc k (hash (invk k1) k2)))`, `(send (enc k (hash k1 (invk k2))))`
    - `flip2`: `(vars (k k1 k2 akey))`, trace: `(recv (enc k (hash k1 (invk k2))))`, `(send (enc k (hash (invk k1) k2)))`
- **Skeletons, Goals, Rules & Macros**:
  - Two identical `(defskeleton bug_example (vars (x y akey)) (defstrand resp 1 (x x) (y y)))` queries, one after each `defprotocol`.
- **When to Reference This Example**: Reference this example when testing how CPSA unifies involutive `(invk ...)` terms inside compound keys `(hash k1 k2)` versus explicit pattern-matched `(invk k1)` / `(invk k2)` transformer roles.
- **Key S-Expression Excerpt**:
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
```

---

## cert_lang.scm

- **File Path**: `03_examples_scm/cert_lang.scm`
- **Algebra & Herald**: `(herald cert-lang)` — `basic` algebra (`(defprotocol cert-uni basic ...)`).
- **Protocol & Purpose**: Demonstrates custom protocol-specific message constructors via `(lang (cert sign) (cert-body (tupl 3)))` in a certificate-based unilateral challenge-response protocol (`cert-uni`). A certificate authority (`certify`) sends a signed certificate `(cert (cert-body subj serial pk) (privk "cert" ca))` over channel `ch`. An initiator (`init`) receives the certificate on `ch-ca`, sends an encrypted challenge `(enc "challenge" chal pk)` on `ch-r`, and receives `chal` back. Includes a `defrule` (`certified-keys-uncompromised`) stating that any public key certified by an uncompromised CA has an uncompromised inverse `(non (invk pk))`.
- **Roles & Variables**:
  - `certify`:
    - `(vars (ch chan) (subj ca name) (pk akey) (serial data))`
    - Role-level I/O: `(inputs ch subj pk serial (privk "cert" ca))`
    - Trace: `(send ch (cert (cert-body subj serial pk) (privk "cert" ca)))`
  - `init`:
    - `(vars (ch-ca ch-r chan) (subj ca name) (pk akey) (serial data) (chal text))`
    - Role-level assumptions & I/O: `(uniq-orig chal)`, `(inputs ch-ca ch-r subj (pubk "cert" ca))`, `(outputs chal)`
    - Trace: `(recv ch-ca (cert (cert-body subj serial pk) (privk "cert" ca)))`, `(send ch-r (enc "challenge" chal pk))`, `(recv ch-r chal)`
  - `resp`:
    - `(vars (ch-ca ch-i chan) (subj ca name) (pk akey) (serial data) (chal text))`
    - Role-level I/O: `(inputs ch-ca ch-i subj (pubk "cert" ca) (invk pk))`, `(outputs chal)`
    - Trace: `(recv ch-ca (cert (cert-body subj serial pk) (privk "cert" ca)))`, `(recv ch-i (enc "challenge" chal pk))`, `(send ch-i chal)`
- **Skeletons, Goals, Rules & Macros**:
  - **Custom Language Declarations**: `(lang (cert sign) (cert-body (tupl 3)))` at the end of `defprotocol`.
  - **Rule**: `certified-keys-uncompromised` transferring `(non (privk "cert" ca))` on a `certify` strand to `(non (invk pk))`.
  - **Skeleton**: `(defskeleton cert-uni (vars (subj ca name) (pk akey) (serial data) (chal text)) (defstrand init 3 (ca ca) (chal chal)) (non-orig (privk "cert" ca)))`.
- **When to Reference This Example**: Reference this example when defining custom cryptographic or tuple operators via `(lang (<op> sign) (<op2> (tupl <n>)))`, when modeling PKI certificate validation rules (`certified-keys-uncompromised`), or when using `cpsa4roletran` `(inputs ...)` and `(outputs ...)` with channels and asymmetric keys.
- **Key S-Expression Excerpt**:
```scheme
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
  (defrule certified-keys-uncompromised
    (forall ((zca strd) (subj ca name) (pk akey))
      (implies
        (and (p "certify" zca 1)
          (p "certify" "subj" zca subj)
          (p "certify" "ca" zca ca)
          (p "certify" "pk" zca pk) (non (privk "cert" ca)))
        (non (invk pk)))))
   (lang (cert sign) (cert-body (tupl 3))))
```

---

## chan-envelope.scm

- **File Path**: `03_examples_scm/chan-envelope.scm`
- **Algebra & Herald**: `(herald "Envelope Protocol With Channels" (bound 15))` — `basic` algebra (`(defprotocol envelope basic ...)` repeated 3 times with progressively stronger rule sets), with `(bound 15)`.
- **Protocol & Purpose**: Models the TPM Envelope Protocol where PCR state is carried over an authenticated and confidential channel `c` (`(conf c)` and `(auth c)`). Evaluates three rule sets across three scenarios each (listening for the secret `v`, listening for the refusal token `(refuse n v k aik)`, and listening for both simultaneously):
  1. Empty rule set: allows the TPM's PCR state on channel `c` to split.
  2. Adds rule `ordered-extends`: forces `tpm-extend` strands sharing channel `c` to be linearly ordered, though Alice's single encrypted session key `esk` can still talk to two different TPM channels.
  3. Adds rule `esk-same-as-chan`: enforces that `tpm-extend-enc` strands sharing `esk` must use the same state channel `(= c c-0)`, making the third scenario (both obtain and refuse tokens leaked) impossible as required.
- **Roles & Variables**:
  - Defined inside `(defmacro (roles) (^ ...))` and expanded into all three `envelope` protocol definitions:
    - `tpm-power-on`: `(vars (c chan))`, `(conf c)`, `(auth c)`, trace: `(recv "power on")`, `(send c "0")`
    - `tpm-extend`: `(vars (value current-value mesg) (c chan))`, `(conf c)`, `(auth c)`, trace: `(recv (cat "extend" value))`, `(recv c current-value)`, `(send c (hash current-value value))`, `(send "ext ok")`
    - `tpm-extend-enc`: `(vars (value current-value mesg) (esk skey) (c chan))`, `(non-orig esk)`, `(conf c)`, `(auth c)`, trace: `(recv (enc "extend" value esk))`, `(recv c current-value)`, `(send c (hash current-value value))`, `(send "ext ok")`
    - `tpm-quote`: `(vars (nonce current-value mesg) (c chan) (aik akey))`, `(non-orig aik)`, `(conf c)`, `(auth c)`, trace: `(recv (cat "quote" nonce))`, `(recv c current-value)`, `(send (enc "quote" current-value nonce aik))`
    - `tpm-create-key`: `(vars (k aik akey) (pcrval mesg) (esk skey))`, `(uniq-orig k)`, `(non-orig (invk k) aik esk)`, trace: `(recv (enc "create key" pcrval esk))`, `(send (enc "created" k pcrval aik))`
    - `tpm-decrypt`: `(vars (m pcrvals mesg) (k aik akey) (c chan))`, `(non-orig aik)`, `(conf c)`, `(auth c)`, trace: `(recv (cat "decrypt" (enc m k)))`, `(recv (enc "created" k pcrvals aik))`, `(recv c pcrvals)`, `(send m)`
    - `alice`: `(vars (n v data) (esk skey) (k aik akey))`, `(uniq-orig n v)`, `(non-orig aik esk)`, trace: `(send (enc "extend" n esk))`, `(send (enc "create key" (hash (hash "0" n) "obtain") esk))`, `(recv (enc "created" k (hash (hash "0" n) "obtain") aik))`, `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: `(defmacro (refuse n v k aik) (enc "quote" (hash (hash "0" n) "refuse") (enc v k) aik))` and `(defmacro (roles) (^ ...))` using the splice operator `^`.
  - **Rules**: `ordered-extends` and `esk-same-as-chan`.
  - **Skeletons**: 9 `(defskeleton envelope ...)` blocks (3 per protocol variant).
- **When to Reference This Example**: Reference this example to learn how to splice multiple `defrole` declarations into multiple `defprotocol` variants using `(defmacro (roles) (^ ...))`, and how to model linear state transitions over confidential/authenticated channels (`(conf c)`, `(auth c)`) using `prec` ordering rules.
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## chan-perrig-song.scm

- **File Path**: `03_examples_scm/chan-perrig-song.scm`
- **Algebra & Herald**: `(herald perrig-song)` — `basic` algebra (`(defprotocol perrig-song basic ...)`).
- **Protocol & Purpose**: Models a two-party challenge-response protocol (`perrig-song`) where the middle message `(cat na nb a b)` is transmitted over a channel `c` while `na` and `nb` are sent in the clear. Tests four combinations of `(auth c)` and `(conf c)` on `init` and `resp` skeletons to show when CPSA must introduce a peer strand versus when the skeleton is already realized as-is.
- **Roles & Variables**:
  - `init`:
    - `(vars (na nb text) (a b name) (c chan))`
    - Trace: `(send na)`, `(recv c (cat na nb a b))`, `(send nb)`
  - `resp`:
    - `(vars (na nb text) (a b name) (c chan))`
    - Trace: `(recv na)`, `(send c (cat na nb a b))`, `(recv nb)`
- **Skeletons, Goals, Rules & Macros**:
  - 4 `(defskeleton perrig-song ...)` blocks:
    1. `(defstrand init 2 (na na) (c c))` with `(uniq-orig na)` and `(auth c)` (brings in a matching `resp` strand of height 2).
    2. `(defstrand resp 3 (nb nb) (c c))` with `(uniq-orig nb)` and `(conf c)` (brings in a matching `init` strand of height 3).
    3. `(defstrand init 2 (na na) (c c))` with `(uniq-orig na)` and `(conf c)` (realized as-is, since `conf` does not prevent adversary injection into `c`).
    4. `(defstrand resp 3 (nb nb) (c c))` with `(uniq-orig nb)` and `(auth c)` (realized as-is, since `auth` does not prevent adversary eavesdropping on `c`).
- **When to Reference This Example**: Reference this example as a clear contrast between `(auth c)` (only an honest role can send on `c`) and `(conf c)` (only an honest role can receive from `c`) on channel messages.
- **Key S-Expression Excerpt**:
```scheme
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

(defskeleton perrig-song
  (vars (na nb text) (a b name) (c chan))
  (defstrand init 2 (na na) (c c))
  (uniq-orig na)
  (auth c))

(defskeleton perrig-song
  (vars (na nb text) (a b name) (c chan))
  (defstrand resp 3 (nb nb) (c c))
  (uniq-orig nb)
  (conf c))
```

---

## chan-unilateral.scm

- **File Path**: `03_examples_scm/chan-unilateral.scm`
- **Algebra & Herald**: `(herald chan-unilateral)` — `basic` algebra (`(defprotocol unilateral basic ...)`).
- **Protocol & Purpose**: Models unilateral authentication over a channel `ch` (`init` sends `n` over `ch` and receives `n` in the clear; `resp` receives `n` over `ch` and sends `n` in the clear). Systematically tests all 4 combinations of channel assumptions (none, `(auth ch)`, `(conf ch)`, and both `(auth ch)` + `(conf ch)`) from both the `init` perspective (using role-level `(uniq-orig n)`) and the `resp` perspective (using skeleton-level `(pen-non-orig n)`).
- **Roles & Variables**:
  - `init`:
    - `(vars (n text) (ch chan))`
    - Role-level assumptions: `(uniq-orig n)`
    - Trace: `(send ch n)`, `(recv n)`
  - `resp`:
    - `(vars (n text) (ch chan))`
    - Trace: `(recv ch n)`, `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - 8 `(defskeleton unilateral ...)` blocks:
    - First 4 test `(defstrand init 2 (ch ch))` with: no channel assumption, `(auth ch)`, `(conf ch)`, and `(auth ch)` + `(conf ch)`.
    - Next 4 test `(defstrand resp 2 (n n) (ch ch))` with `(pen-non-orig n)` and: no channel assumption, `(auth ch)`, `(conf ch)`, and `(auth ch)` + `(conf ch)`.
- **When to Reference This Example**: Reference this example when using `(pen-non-orig n)` (penetrator non-origination, meaning the adversary cannot guess/originate `n` on its own, though honest strands may originate it) together with `(auth ch)` and `(conf ch)` channel properties.
- **Key S-Expression Excerpt**:
```scheme
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
  (vars (n text) (ch chan))
  (defstrand resp 2 (n n) (ch ch))
  (pen-non-orig n)
  (auth ch)
  (conf ch))
```

---

## chan-yahalom-role-decl.scm

- **File Path**: `03_examples_scm/chan-yahalom-role-decl.scm`
- **Algebra & Herald**: `(herald "Yahalom Protocol Without Forwarding" (bound 15))` — `basic` algebra (`(defprotocol yahalom basic ...)`), with `(bound 15)`.
- **Protocol & Purpose**: Models the Yahalom key distribution protocol without key forwarding by replacing shared long-term symmetric keys with channels (`ch1`, `ch2`, `ch3` of sort `chan`) whose security properties (`(auth ch3)`, `(auth ch2)`, `(conf ch3 ch2)`) are declared directly inside the `defrole` definitions rather than in each `defskeleton`.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b c name) (n-a n-b text) (k skey) (ch3 chan))`
    - Role-level assumptions: `(auth ch3)`
    - Trace: `(send (cat a n-a))`, `(recv ch3 (cat a b k n-a n-b))`, `(send (enc n-b k))`
  - `resp`:
    - `(vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))`
    - Role-level assumptions: `(auth ch2)`
    - Trace: `(recv (cat a n-a))`, `(send ch1 (cat a b n-a n-b))`, `(recv ch2 (cat a b k))`, `(recv (enc n-b k))`
  - `serv`:
    - `(vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))`
    - Role-level assumptions: `(conf ch3 ch2)`, `(uniq-orig k)`
    - Trace: `(recv ch1 (cat a b n-a n-b))`, `(send ch3 (cat a b k n-a n-b))`, `(send ch2 (cat a b k))`
- **Skeletons, Goals, Rules & Macros**:
  - 8 `(defskeleton yahalom ...)` queries:
    1. `resp` height 4 with `(uniq-orig n-b)`
    2. `resp` height 4 with `(deflistener k)` and `(uniq-orig n-b)`
    3. `init` height 3 with `(uniq-orig n-a)`
    4. `init` height 3 with `(deflistener k)`
    5. `init` height 3 + `resp` height 3 sharing `k` with `(uniq-orig n-a)`
    6. `init` height 3 + `resp` height 4 sharing `k` with `(uniq-orig n-a)`
    7. `serv` height 3
    8. `serv` height 3 with `(deflistener k)`
- **When to Reference This Example**: Reference this example when you want channel trust properties (`(auth ...)` and `(conf ...)`) to apply automatically to every instance of a role by declaring them inside `(defrole ...)` rather than repeating them in every `(defskeleton ...)`.
- **Key S-Expression Excerpt**:
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
```

---

## chan-yahalom.scm

- **File Path**: `03_examples_scm/chan-yahalom.scm`
- **Algebra & Herald**: `(herald "Yahalom Protocol Without Forwarding" (bound 15))` — `basic` algebra (`(defprotocol yahalom basic ...)`), with `(bound 15)`.
- **Protocol & Purpose**: Companion to `chan-yahalom-role-decl.scm` modeling the same channel-based Yahalom protocol, but omitting `(auth ...)` and `(conf ...)` from the `defrole` definitions so they can be added incrementally in individual `defskeleton` queries to explore exactly which channel assumptions are needed at each step.
- **Roles & Variables**:
  - `init`: `(vars (a b c name) (n-a n-b text) (k skey) (ch3 chan))`, trace: `(send (cat a n-a))`, `(recv ch3 (cat a b k n-a n-b))`, `(send (enc n-b k))`
  - `resp`: `(vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))`, trace: `(recv (cat a n-a))`, `(send ch1 (cat a b n-a n-b))`, `(recv ch2 (cat a b k))`, `(recv (enc n-b k))`
  - `serv`: `(vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))`, `(uniq-orig k)`, trace: `(recv ch1 (cat a b n-a n-b))`, `(send ch3 (cat a b k n-a n-b))`, `(send ch2 (cat a b k))`
- **Skeletons, Goals, Rules & Macros**:
  - 8 `(defskeleton yahalom ...)` blocks demonstrating iterative analysis:
    1. `resp` height 4 with `(auth ch2)` and `(uniq-orig n-b)`
    2. `resp` height 4 + `serv` height 3 with `(precedes ((1 2) (0 2)))`, `(uniq-orig k n-b)`, `(auth ch2)`, `(conf ch2 ch3)`
    3. Adds `(auth ch2 ch1-0)` to unify `ch1-0 = ch1`
    4. Adds `(deflistener k)` to verify session key secrecy
    5. `init` height 3 with `(uniq-orig n-a)` and `(auth ch3)`
    6. `init` height 3 + `serv` height 2 with `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`, `(uniq-orig k n-a)`, `(auth ch3 ch1)`, `(conf ch3-0)`
    7. `serv` height 3 with `(auth ch1)` and `(conf ch2 ch3)`
    8. `serv` height 3 with `(deflistener k)`, `(auth ch1)`, and `(conf ch2 ch3)`
- **When to Reference This Example**: Reference this example when performing step-by-step interactive hypothesis refinement in CPSA—taking a shape output from one skeleton (with `(precedes ...)` and distinct channel variables `ch1`, `ch1-0`) and adding `(auth ...)` / `(conf ...)` assumptions in the next skeleton.
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## commitment.scm

- **File Path**: `03_examples_scm/commitment.scm`
- **Algebra & Herald**: `(herald commitment)` — `basic` algebra (`(defprotocol commit basic ...)`).
- **Protocol & Purpose**: Models a cryptographic commitment auction protocol (`commit`) with a `bidder`, a malformed/alternative `bid-trash` role, and an `auctioneer`. Demonstrates the `(cheq sealed (hash a b n quote))` trace event inside `auctioneer`: the auctioneer first receives an opaque `sealed` value of sort `mesg` inside a signed bid `(recv (enc "bid" sealed (privk "sig" a)))`, issues a receipt, later receives the opening `(recv (cat n quote))`, and checks equality `(cheq sealed (hash a b n quote))` before signing the result. Note the inline comment explaining that `cheq` does not count as a separate node toward strand height (`auctioneer` has 4 `recv`/`send` events and full height 4).
- **Roles & Variables**:
  - `bidder`:
    - `(vars (a b name) (n data) (quote outcome text))`
    - Trace: `(send (enc "bid" (hash a b n quote) (privk "sig" a)))`, `(recv (enc "receipt" (hash a b n quote) (privk "sig" b)))`, `(send (cat n quote))`, `(recv (enc "result" a b n quote outcome (privk "sig" b)))`
  - `bid-trash`:
    - `(vars (a b name) (n data) (outcome trash text))`
    - Trace: `(send (enc "bid" (hash n trash) (privk "sig" a)))`, `(recv (enc "receipt" (hash n trash) (privk "sig" b)))`
  - `auctioneer`:
    - `(vars (a b name) (n data) (quote outcome text) (sealed mesg))`
    - Trace: `(recv (enc "bid" sealed (privk "sig" a)))`, `(send (enc "receipt" sealed (privk "sig" b)))`, `(recv (cat n quote))`, `(cheq sealed (hash a b n quote))`, `(send (enc "result" a b n quote outcome (privk "sig" b)))`
- **Skeletons, Goals, Rules & Macros**:
  - 3 `(defskeleton commit ...)` blocks:
    1. `(defstrand auctioneer 4 (a a))` (full height 4) with `(non-orig (privk "sig" a))`
    2. `(defstrand auctioneer 2 (a a))` (up to receipt send, before `sealed` is opened) with `(non-orig (privk "sig" a))`
    3. `(defstrand auctioneer 4 (sealed (hash a b n quote)) ...)` + `(defstrand bidder 1 ...)` with `(uniq-gen n)` and `(non-orig (privk "sig" a))`
- **When to Reference This Example**: Reference this example when modeling hash commitment / reveal protocols where a party receives an opaque commitment `sealed` (`mesg`), acts on it before knowing its preimage, and later verifies `(cheq sealed (hash ...))` after receiving the opening; also note that `cheq` does not increment strand height.
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## comp_test.scm

- **File Path**: `03_examples_scm/comp_test.scm`
- **Algebra & Herald**: `(herald "Main Example")` — `basic` algebra across three protocols (`main-ex-src`, `main-ex-tgt`, `main-ex-tgt-rule`).
- **Protocol & Purpose**: Models protocol refinement / composition across three protocol versions:
  - `main-ex-src`: A query-answer protocol where queriers (`qn`, `qy`) send a compound request `(cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c))` and responders (`an`, `ay`) treat the fourth component as an opaque `x` (`mesg`) and reply with `(enc "sorry" a b k)` or `(enc "data" d k)`.
  - `main-ex-tgt`: Refines `an` and `ay` so they forward `(enc y n i a x c)` to a backend server (`sn` or `sy`) that decrypts `(enc a b i ssn c)` and returns `n` (no) or `y` (yes) before `an`/`ay` reply to the querier.
  - `main-ex-tgt-rule`: Adds a `defrule src` encoding the shape analysis guarantee of `main-ex-src` directly as an axiom on `qn` and `an`.
- **Roles & Variables**:
  - In `main-ex-src`:
    - `qn`: `(vars (a b c akey) (i ssn text) (k skey))`, `(uniq-orig k)`, trace: `(send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))`, `(recv (enc "sorry" a b k))`
    - `qy`: `(vars (a b c akey) (i ssn d text) (k skey))`, `(uniq-orig k)`, trace: `(send (cat i a (enc (enc k b c i (invk a)) b) (enc a b i ssn c)))`, `(recv (enc "data" d k))`
    - `an`: `(vars (a b c akey) (i text) (k skey) (x mesg))`, trace: `(recv (cat i a (enc (enc k b c i (invk a)) b) x))`, `(send (enc "sorry" a b k))`
    - `ay`: `(vars (a b c akey) (i d text) (k skey) (x mesg))`, `(uniq-orig d)`, trace: `(recv (cat i a (enc (enc k b c i (invk a)) b) x))`, `(send (enc "data" d k))`
  - In `main-ex-tgt` and `main-ex-tgt-rule`:
    - `qn`, `qy` (same as above)
    - `an`: `(vars (a b c akey) (i y n text) (k skey) (x mesg))`, `(uniq-orig y n)`, height 4 (adds sub-exchange `(send (enc y n i a x c))`, `(recv n)`)
    - `ay`: `(vars (a b c akey) (i y n d text) (k skey) (x mesg))`, `(uniq-orig d y n)`, height 4 (adds sub-exchange `(send (enc y n i a x c))`, `(recv y)`)
    - `sn`: `(vars (a b c akey) (i ssn y n text))`, trace: `(recv (enc y n i a (enc a b i ssn c) c))`, `(send n)`
    - `sy`: `(vars (a b c akey) (i ssn y n text))`, trace: `(recv (enc y n i a (enc a b i ssn c) c))`, `(send y)`
- **Skeletons, Goals, Rules & Macros**:
  - **Rule**: `src` in `main-ex-tgt-rule` using `forall`, `implies`, `exists`, `(non (invk ...))`, `(uniq k)`, and `(prec ...)`.
  - **Skeletons**: 5 `(defskeleton ...)` blocks (2 for `main-ex-src`, 2 for `main-ex-tgt`, 1 for `main-ex-tgt-rule`); the first skeleton embeds a commented `(comment (defgoal main-ex-src ...))` showing the shape analysis sentence from `cpsasas`.
- **When to Reference This Example**: Reference this example when modeling multi-tier protocol composition (where a middle tier forwards an encrypted blob `x` of sort `mesg` to a backend verifier) or when converting a shape analysis sentence (`defgoal`) into a compositional `defrule`.
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## completeness-test.scm

- **File Path**: `03_examples_scm/completeness-test.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol completeness-test basic ...)`.
- **Protocol & Purpose**: Regression test for strand-ordering completeness in CPSA. An initiator (`init`) verifies the liveness of a responder (`resp`) via a two-message public-key challenge-response (`(send (enc a n (pubk b)))`, `(recv (enc n (pubk a)))`) and then sends `(enc "ok" s)` to a `probe` role waiting to hear `(recv (enc "ok" s))`. Compares skeletons that differ only in the order in which `defstrand init` and `defstrand probe` are listed.
- **Roles & Variables**:
  - `init`: `(vars (a b name) (n text) (s skey))`, trace: `(send (enc a n (pubk b)))`, `(recv (enc n (pubk a)))`, `(send (enc "ok" s))`
  - `resp`: `(vars (a b name) (n text))`, trace: `(recv (enc a n (pubk b)))`, `(send (enc n (pubk a)))`
  - `probe`: `(vars (s skey))`, trace: `(recv (enc "ok" s))`
- **Skeletons, Goals, Rules & Macros**:
  - 4 `(defskeleton completeness-test ...)` blocks, all with `(non-orig s (privk b))` and `(uniq-orig n)`:
    1. `(defstrand init 3 (b b) (n n))` then `(defstrand probe 1 (s s))`
    2. `(defstrand probe 1 (s s))` then `(defstrand init 3 (b b) (n n))`
    3. `(defstrand init 2 (b b) (n n))` then `(defstrand probe 1 (s s))`
    4. `(defstrand probe 1 (s s))` then `(defstrand init 2 (b b) (n n))`
- **When to Reference This Example**: Reference this example when testing multi-strand point-of-view skeletons (where one role signals completion to a secondary `probe` or observer role) or verifying that strand declaration order in `defskeleton` does not alter discovered shapes.
- **Key S-Expression Excerpt**:
```scheme
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

(defskeleton completeness-test
  (vars (b name) (n text) (s skey))
  (defstrand init 3 (b b) (n n))
  (defstrand probe 1 (s s))
  (non-orig s (privk b))
  (uniq-orig n))
```

---

## crushing.scm

- **File Path**: `03_examples_scm/crushing.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol crushing basic ...)`.
- **Protocol & Purpose**: Designed to force CPSA to reduce ("crush") several strands simultaneously via hulling. An `init` strand sends `(enc n k)`, receives three signed/encrypted pairs `(enc n n1 (invk k))`, `(enc n n2 (invk k))`, `(enc n n3 (invk k))` from `adder` strands, sends `(enc n n1 n2 n3 (invk k))`, and receives `(enc n n1 n2 n3 n (invk k))` after cyclic permutation by `twister` strands (which map `(n1, n2, n3)` to `(n2, n3, n1)`).
- **Roles & Variables**:
  - `init`:
    - `(vars (k akey) (n n1 n2 n3 text))`
    - Role-level assumptions: `(uniq-orig n)`, `(non-orig (invk k))`
    - Trace: `(send (enc n k))`, `(recv (enc n n1 (invk k)))`, `(recv (enc n n2 (invk k)))`, `(recv (enc n n3 (invk k)))`, `(send (enc n n1 n2 n3 (invk k)))`, `(recv (enc n n1 n2 n3 n (invk k)))`
  - `adder`:
    - `(vars (k akey) (n new text))`
    - Role-level assumptions: `(uniq-orig new)`
    - Trace: `(recv (enc n k))`, `(send (enc n new (invk k)))`
  - `twister`:
    - `(vars (k akey) (n n1 n2 n3 text))`
    - Trace: `(recv (enc n n1 n2 n3 (invk k)))`, `(send (enc n n2 n3 n1 n (invk k)))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton crushing (vars (k akey) (n n1 n2 n3 text)) (defstrand init 6 (k k) (n n) (n1 n1) (n2 n2) (n3 n3)) (uniq-orig n1 n2 n3))`.
- **When to Reference This Example**: Reference this example when studying strand hulling, variable unification across cyclic permutations (`twister`), and how CPSA collapses multiple isomorphic `adder` strands when `n1`, `n2`, `n3` are forced equal.
- **Key S-Expression Excerpt**:
```scheme
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

## dass_simple.scm

- **File Path**: `03_examples_scm/dass_simple.scm`
- **Algebra & Herald**: `(herald "Distributed Authentication Security Service Protocol Variants")` — `basic` algebra across two protocol variants (`dass-simple` and `dass+`).
- **Protocol & Purpose**: Models two simplified variants of the Distributed Authentication Security Service (DASS) protocol (`dass-simple` and `dass+`) where an initiator `a` certifies an ephemeral public key `kp` via `(enc a kp (privk a))` and signs the encrypted session key `(enc (enc k (pubk b)) (invk kp))`. Demonstrates the critical difference between placing `(non-orig (privk a))` only in the `defskeleton` (`dass-simple`, where responder `b` might interact with a compromised initiator in another session, failing to authenticate `a` to `b`) versus placing `(non-orig (privk a))` directly inside `(defrole resp ...)` (`dass+`, which constrains every responder instance to interact only with uncompromised initiators).
- **Roles & Variables**:
  - In `dass-simple`:
    - `init`: `(vars (a b name) (k skey) (ta text) (kp akey) (tb text))`, trace: `(send (cat (enc "init" ta k) (enc a kp (privk a)) (enc (enc k (pubk b)) (invk kp))))`, `(recv (enc "resp" tb k))`
    - `resp`: `(vars (a b name) (k skey) (ta text) (kp akey) (tb text))`, trace: `(recv (cat (enc "init" ta k) (enc a kp (privk a)) (enc (enc k (pubk b)) (invk kp))))`, `(send (enc "resp" tb k))`
  - In `dass+`:
    - `init`: identical to `dass-simple`
    - `resp`: identical to `dass-simple`, plus role-level `(non-orig (privk a))`
- **Skeletons, Goals, Rules & Macros**:
  - 2 active `(defskeleton ...)` blocks (one for `dass-simple`, one for `dass+`), both testing `(defstrand init 2 (a a) (b b) (k k) (kp kp) (ta ta) (tb tb))` with `(non-orig (privk a) (privk b) (invk kp))` and `(uniq-orig k kp)`.
  - Contains a trailing `(comment ...)` block with two legacy skeletons for `dass`.
- **When to Reference This Example**: Reference this example to understand the exact semantic difference between role-level `(non-orig ...)` and skeleton-level `(non-orig ...)`, or when modeling ephemeral signing keys `kp` certified by a long-term key `(privk a)`.
- **Key S-Expression Excerpt**:
```scheme
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

(defskeleton dass+
  (vars (a name) (b name) (k skey) (kp akey) (ta text)(tb text))
  (defstrand init 2 (a a) (b b) (k k) (kp kp) (ta ta) (tb tb))
  (non-orig (privk a) (privk b) (invk kp))
  (uniq-orig k kp))
```

---

## denning-sacco.scm

- **File Path**: `03_examples_scm/denning-sacco.scm`
- **Algebra & Herald**: `(herald "Denning-Sacco Protocol")` — `basic` algebra (`(defprotocol denning-sacco basic ...)`).
- **Protocol & Purpose**: Models the classic Denning-Sacco public-key key distribution protocol with a `keyserver` (`ks`). The initiator `a` requests certificates for `a` and `b` from `ks`, receives `(cat (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks)))`, and forwards those certificates together with the signed session key and timestamp `(enc a b k ta (privk a))` encrypted under `(pubk b)`.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b ks name) (k skey) (ta text))`
    - Trace:
      1. `(send (cat a b))`
      2. `(recv (cat (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks))))`
      3. `(send (enc (enc a b k ta (privk a)) (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks)) (pubk b)))`
  - `resp`:
    - `(vars (a b ks name) (k skey) (ta text))`
    - Trace: `(recv (enc (enc a b k ta (privk a)) (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks)) (pubk b)))`
  - `keyserver`:
    - `(vars (a b ks name))`
    - Trace: `(recv (cat a b))`, `(send (cat (enc b (pubk b) (privk ks)) (enc a (pubk a) (privk ks))))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton denning-sacco (vars (a b ks name) (k skey)) (defstrand resp 1 (a a) (b b) (ks ks) (k k)) (non-orig (privk b) (privk a) (privk ks)) (uniq-orig k))`.
- **When to Reference This Example**: Reference this example when modeling three-party certificate directory / keyserver protocols where public key certificates `(enc a (pubk a) (privk ks))` are fetched and bundled into an encrypted session key transport message.
- **Key S-Expression Excerpt**:
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

## deorig_contract.scm

- **File Path**: `03_examples_scm/deorig_contract.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol deorig-contract basic ...)`.
- **Protocol & Purpose**: Demonstrates a subtle incompleteness in CPSA related to "deorigination" during contraction steps. The `init` role originates two fresh values `(uniq-orig x1 x2)`, sends `(enc x1 k)` and `(enc x2 k)`, and expects `(enc x1 x2 k)`. However, `resp` receives `(enc y1 k)` and `(enc y2 k)` and sends `(enc y1 y3 k)` where `y3` appears for the first time in `resp`'s send event. For `resp` to satisfy `init`, a contraction must unify `y3 = y2 = x2`, which requires `y3` on `resp` to cease being an origination point ("deorigination") because `x2` already uniquely originates on `init` prior to `resp`'s second `recv`.
- **Roles & Variables**:
  - `init`:
    - `(vars (k akey) (x1 x2 text))`
    - Role-level assumptions: `(uniq-orig x1 x2)`, `(non-orig (invk k))`
    - Trace: `(send (enc x1 k))`, `(send (enc x2 k))`, `(recv (enc x1 x2 k))`
  - `resp`:
    - `(vars (k akey) (y1 y2 y3 text))`
    - Trace: `(recv (enc y1 k))`, `(recv (enc y2 k))`, `(send (enc y1 y3 k))`
- **Skeletons, Goals, Rules & Macros**:
  - Two `(defskeleton deorig-contract ...)` blocks:
    1. `(defskeleton deorig-contract (vars) (defstrand init 3))` (the initial point of view).
    2. `(defskeleton deorig-contract (vars (k akey) (x1 x2 text)) (defstrand init 3 (k k) (x1 x1) (x2 x2)) (defstrand resp 3 (k k) (y1 x1) (y2 x2) (y3 x2)) (precedes ((0 0) (1 0)) ((0 1) (1 1)) ((1 2) (0 2))))` (the expected realized skeleton where `y3` and `y2` are unified with `x2`).
- **When to Reference This Example**: Reference this example when debugging unexpected dead skeletons caused by unbound variables in a responder's `send` event (`y3`) that must unify with a previously received `uniq-orig` variable (`x2`) during cohort contraction.
- **Key S-Expression Excerpt**:
```scheme
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
   (vars (k akey) (x1 x2 text))
   (defstrand init 3 (k k) (x1 x1) (x2 x2))
   (defstrand resp 3 (k k) (y1 x1) (y2 x2) (y3 x2))
   (precedes ((0 0) (1 0)) ((0 1) (1 1)) ((1 2) (0 2)))
)
```

---

## deorig_mesg.scm

- **File Path**: `03_examples_scm/deorig_mesg.scm`
- **Algebra & Herald**: `(herald deorig-mesg)` — `basic` algebra (`(defprotocol deorig-mesg basic ...)`).
- **Protocol & Purpose**: Minimal two-message demonstration of deorigination involving sort `mesg`. `init` sends `(enc x k)` and receives `x` (with `(uniq-orig x)` and `(non-orig (invk k))`), while `resp` receives an untyped `(x mesg)` and sends `(y text)`. For `resp` to satisfy `init`, `resp`'s received `x` must instantiate to `(enc z k)` and its sent `y` must instantiate to `z`, changing `z` from originating at `resp`'s send node to being received inside `(enc z k)` at `resp`'s recv node.
- **Roles & Variables**:
  - `init`: `(vars (k akey) (x text))`, `(uniq-orig x)`, `(non-orig (invk k))`, trace: `(send (enc x k))`, `(recv x)`
  - `resp`: `(vars (x mesg) (y text))`, trace: `(recv x)`, `(send y)`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton deorig-mesg ...)` blocks:
    1. `(defskeleton deorig-mesg (vars) (defstrand init 2))`
    2. `(defskeleton deorig-mesg (vars (k akey) (z text)) (defstrand init 2 (k k) (x z)) (defstrand resp 2 (x (enc z k)) (y z)) (precedes ((0 0) (1 0)) ((1 1) (0 1))))`
- **When to Reference This Example**: Reference this example to understand why a role that receives an unparsed `(x mesg)` and sends a separate variable `(y text)` cannot act as a general decryption oracle in CPSA without explicit variable binding between the received ciphertext and sent plaintext.
- **Key S-Expression Excerpt**:
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

## deorig_simple.scm

- **File Path**: `03_examples_scm/deorig_simple.scm`
- **Algebra & Herald**: `(herald deorig-simple)` — `basic` algebra (`(defprotocol deorig-simple basic ...)`).
- **Protocol & Purpose**: Demonstrates the same deorigination incompleteness as `deorig_contract.scm` in a simpler two-message exchange. `init` sends `(enc x k)` and expects `x` back, whereas `resp` receives `(enc x k)` and sends a distinct variable `y` (both of sort `text`). Although unifying `x = y = z` on `resp` produces a valid shape (shown in the second skeleton), `y` originates on `resp` until unified with `x`, causing standard augmentation to miss the shape.
- **Roles & Variables**:
  - `init`: `(vars (k akey) (x text))`, `(uniq-orig x)`, `(non-orig (invk k))`, trace: `(send (enc x k))`, `(recv x)`
  - `resp`: `(vars (k akey) (x y text))`, trace: `(recv (enc x k))`, `(send y)`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton deorig-simple ...)` blocks:
    1. `(defskeleton deorig-simple (vars) (defstrand init 2))`
    2. `(defskeleton deorig-simple (vars (k akey) (z text)) (defstrand init 2 (k k) (x z)) (defstrand resp 2 (k k) (x z) (y z)) (precedes ((0 0) (1 0)) ((1 1) (0 1))))`
- **When to Reference This Example**: Reference this example when diagnosing why a role must use the same variable name (e.g., `x` in both `(recv (enc x k))` and `(send x)`) if it is meant to forward or decrypt-and-return a received nonce, rather than declaring two distinct variables `x` and `y`.
- **Key S-Expression Excerpt**:
```scheme
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

## dh-ca_hack.scm

- **File Path**: `03_examples_scm/dh-ca_hack.scm`
- **Algebra & Herald**: `(herald dhca (algebra basic) (bound 12))` — `basic` algebra (`(defprotocol dhca basic ...)`), with herald flags `(algebra basic)` and `(bound 12)`.
- **Protocol & Purpose**: Models a static Diffie-Hellman exchange with CA-certified long-term DH public values inside the `basic` crypto algebra using the `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))` encoding and two adversary computation roles (`CDHcalc1` and `CDHcalc2`). The `ca` role certifies a long-term DH public key `gz` (`akey`) while assuming `(non-orig (invk gz))` for the private exponent. If the adversary learns either `(invk gy)` or `(invk gx)`, it can invoke `CDHcalc1` or `CDHcalc2` to compute `(CDH gx gy dhkey)`.
- **Roles & Variables**:
  - `init`:
    - `(vars (gx h akey) (dhkey skey) (a b ca name) (n text))`
    - Role-level assumptions: `(non-orig (privk ca) dhkey)`
    - Trace: `(recv (enc gx a (privk ca)))`, `(send (cat gx (enc gx a (privk ca))))`, `(recv (cat h (enc h b (privk ca)) (enc n (CDH gx h dhkey))))`, `(send (enc "check" n (CDH gx h dhkey)))`
  - `resp`:
    - `(vars (gy h akey) (dhkey skey) (a b ca name) (n text))`
    - Role-level assumptions: `(non-orig (privk ca) dhkey)`
    - Trace: `(recv (enc gy b (privk ca)))`, `(recv (cat h (enc h a (privk ca))))`, `(send (cat gy (enc gy b (privk ca)) (enc n (CDH h gy dhkey))))`, `(recv (enc "check" n (CDH h gy dhkey)))`
  - `ca`:
    - `(vars (subject ca name) (gz akey))`
    - Role-level assumptions: `(non-orig (invk gz))`
    - Trace: `(send (enc gz subject (privk ca)))`
  - `CDHcalc1`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gx (invk gy)))`, `(send (CDH gx gy dhkey))`
  - `CDHcalc2`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gy (invk gx)))`, `(send (CDH gx gy dhkey))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macro**: `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))`
  - **Skeletons**: 4 `(defskeleton dhca ...)` queries:
    1. `(defstrand init 4)`
    2. `(defstrand resp 4 (n n))` with `(uniq-orig n)`
    3. `(defstrand resp 4 (n n))` with `(deflistener n)` and `(uniq-orig n)`
    4. Joint `init` height 4 + `resp` height 4 agreeing on `(gx, gy, ca, a, b, n, dhkey)` with `(uniq-orig n)`.
- **When to Reference This Example**: Reference this example when encoding Computational Diffie-Hellman (`CDH`) inside the `basic` algebra using `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))` and calculator roles `CDHcalc1`/`CDHcalc2` alongside CA-issued certificates.
- **Key S-Expression Excerpt**:
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
  )))
```

---

## dh_encrypt_hack.scm

- **File Path**: `03_examples_scm/dh_encrypt_hack.scm`
- **Algebra & Herald**: `(herald dhencrypt (algebra basic))` — `basic` algebra (`(defprotocol dhencrypt basic ...)`), with herald flag `(algebra basic)`.
- **Protocol & Purpose**: Models an unauthenticated Diffie-Hellman key exchange followed by an encrypted-nonce challenge/response in the `basic` algebra using the `(CDH gx gy dhkey)` macro and calculator roles `CDHcalc1`/`CDHcalc2`. Shows how an unauthenticated DH exchange without certificates is vulnerable unless both `init` and `resp` are explicitly assumed to agree on `(gx, gy)` in the point-of-view skeleton.
- **Roles & Variables**:
  - `init`:
    - `(vars (gx h akey) (dhkey skey) (n text))`
    - Role-level assumptions: `(non-orig (invk gx) dhkey)`
    - Trace: `(send gx)`, `(recv (cat h (enc n (CDH gx h dhkey))))`, `(send (enc "check" n (CDH gx h dhkey)))`
  - `resp`:
    - `(vars (h gy akey) (dhkey skey) (n text))`
    - Role-level assumptions: `(non-orig (invk gy) dhkey)`, `(uniq-orig gy n)`
    - Trace: `(recv h)`, `(send (cat gy (enc n (CDH h gy dhkey))))`, `(recv (enc "check" n (CDH h gy dhkey)))`
  - `CDHcalc1`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gx (invk gy)))`, `(send (CDH gx gy dhkey))`
  - `CDHcalc2`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gy (invk gx)))`, `(send (CDH gx gy dhkey))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macro**: `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))`
  - **Skeletons**: 3 `(defskeleton dhencrypt ...)` queries:
    1. `init` height 3
    2. `resp` height 3
    3. `init` height 2 + `resp` height 3 sharing `(gx, gy, n)`
- **When to Reference This Example**: Reference this example as the minimal template for the `(CDH gx gy dhkey)` macro + `CDHcalc1`/`CDHcalc2` pattern in the `basic` algebra without CA certificates.
- **Key S-Expression Excerpt**:
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
  )))
```

---

## dh_group_sig.scm

- **File Path**: `03_examples_scm/dh_group_sig.scm`
- **Algebra & Herald**: `(herald "Signed group DH exchange (improved version)" (algebra diffie-hellman) (limit 100))` — `diffie-hellman` algebra (`(defprotocol dh_sig diffie-hellman ...)`), with herald flags `(algebra diffie-hellman)` and `(limit 100)`.
- **Protocol & Purpose**: Models an authenticated Diffie-Hellman exchange over a dynamically distributed DH subgroup generator `(exp (gen) alpha)`. A `group-init` role generates a fresh random exponent `(alpha rndx)` (`(uniq-gen alpha)`) and distributes `(cat "Group id" group (exp (gen) alpha))` over a confidential channel `group-dist`. The initiator (`init`) and responder (`resp`) receive the group generator over `(auth group-dist)` (modeling `alpha` as `(alpha expt)`), perform a signed DH exchange binding peer identities `a` and `b` and nonces `na`, `nb`, and verify possession of the shared secret `(exp (exp (exp (gen) alpha) y) x)` via a nonce challenge-response `(enc na nb (exp (exp (exp (gen) alpha) y) x))`.
- **Roles & Variables**:
  - `group-init`:
    - `(vars (alpha rndx) (group text) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen alpha)`, `(conf group-dist)`
    - Trace: `(send group-dist (cat "Group id" group (exp (gen) alpha)))`
  - `init`:
    - `(vars (x rndx) (y expt) (alpha expt) (group na nb text) (a b name) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen na x)`, `(auth group-dist)`
    - Trace:
      1. `(recv group-dist (cat "Group id" group (exp (gen) alpha)))`
      2. `(send (enc (exp (exp (gen) alpha) x) (privk a)))`
      3. `(recv (enc a (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b)))`
      4. `(send (enc "final" b na (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a)))`
      5. `(recv (enc na nb (exp (exp (exp (gen) alpha) y) x)))`
      6. `(send nb)`
  - `resp`:
    - `(vars (y rndx) (x expt) (alpha expt) (group na nb text) (a b name) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen nb y)`, `(auth group-dist)`
    - Trace:
      1. `(recv group-dist (cat "Group id" group (exp (gen) alpha)))`
      2. `(recv (enc (exp (exp (gen) alpha) x) (privk a)))`
      3. `(send (enc a (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b)))`
      4. `(recv (enc "final" b na (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a)))`
      5. `(send (enc na nb (exp (exp (exp (gen) alpha) x) y)))`
      6. `(recv nb)`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton dh_sig ...)` blocks:
    1. `(defstrand init 6 (a a) (b b))` with `(non-orig (privk b) (privk a))`
    2. `(defstrand resp 6 (a a) (b b))` with `(non-orig (privk a) (privk b))`
- **When to Reference This Example**: Reference this example when modeling Diffie-Hellman exchanges in the `diffie-hellman` algebra, especially when distinguishing own exponents (`rndx` with `uniq-gen`) from received peer/group exponents (`expt`), or when using nested exponentiation `(exp (exp (gen) alpha) x)` for custom DH groups.
- **Key S-Expression Excerpt**:
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
    (auth group-dist)))
```

---

## dh_group_sig_auth_failure.scm

- **File Path**: `03_examples_scm/dh_group_sig_auth_failure.scm`
- **Algebra & Herald**: `(herald "Signed group DH exchange (version with auth failure)" (algebra diffie-hellman) (limit 100))` — `diffie-hellman` algebra (`(defprotocol dh_sig diffie-hellman ...)`), with herald flags `(algebra diffie-hellman)` and `(limit 100)`.
- **Protocol & Purpose**: Vulnerable predecessor to `dh_group_sig.scm` that omits the peer identities `a` and `b` inside the signed DH messages (`(enc (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b))` and `(enc "final" (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a))`) and omits the subsequent shared-secret challenge-response. Demonstrates an authentication failure (unknown key-share / man-in-the-middle forwarding of signed DH shares) in the `diffie-hellman` algebra.
- **Roles & Variables**:
  - `group-init`:
    - `(vars (alpha rndx) (group text) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen alpha)`, `(conf group-dist)`
    - Trace: `(send group-dist (cat "Group id" group (exp (gen) alpha)))`
  - `init`:
    - `(vars (x rndx) (y expt) (alpha expt) (group text) (a b name) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen x)`, `(auth group-dist)`
    - Trace:
      1. `(recv group-dist (cat "Group id" group (exp (gen) alpha)))`
      2. `(send (enc (exp (exp (gen) alpha) x) (privk a)))`
      3. `(recv (enc (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b)))`
      4. `(send (enc "final" (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a)))`
  - `resp`:
    - `(vars (y rndx) (x expt) (alpha expt) (group text) (a b name) (group-dist chan))`
    - Role-level assumptions: `(uniq-gen y)`, `(auth group-dist)`
    - Trace:
      1. `(recv group-dist (cat "Group id" group (exp (gen) alpha)))`
      2. `(recv (enc (exp (exp (gen) alpha) x) (privk a)))`
      3. `(send (enc (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk b)))`
      4. `(recv (enc "final" (exp (exp (gen) alpha) y) (exp (exp (gen) alpha) x) (privk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton dh_sig ...)` blocks:
    1. `(defstrand init 4 (a a) (b b))` with `(non-orig (privk b) (privk a))`
    2. `(defstrand resp 4 (a a) (b b))` with `(non-orig (privk a) (privk b))`
- **When to Reference This Example**: Reference this example alongside `dh_group_sig.scm` to see how omitting peer identities (`a`, `b`) inside signed Diffie-Hellman transcripts leads to authentication failure in CPSA's `diffie-hellman` algebra.
- **Key S-Expression Excerpt**:
```scheme
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

(defskeleton dh_sig
  (vars (a b name))
  (defstrand init 4 (a a) (b b))
  (non-orig (privk b) (privk a))
)
```

---

## dh_mim_hack.scm

- **File Path**: `03_examples_scm/dh_mim_hack.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol dh_mim basic ...)`.
- **Protocol & Purpose**: Models an unauthenticated Diffie-Hellman key exchange followed by sending an encrypted nonce `(enc n (CDH gx gy dhkey))` in the `basic` algebra using the `(CDH gx gy dhkey)` macro and calculator roles `CDHcalc1`/`CDHcalc2`. Demonstrates a classic man-in-the-middle attack when the point-of-view skeleton requires agreement only on the encrypted plaintext `n` (`(precedes ((0 2) (1 2)))`) without binding `gx` and `gy` across `init` and `resp`.
- **Roles & Variables**:
  - `init`: `(vars (gx gy akey) (n text) (dhkey skey))`, `(uniq-orig n gx)`, `(non-orig (invk gx) dhkey)`, trace: `(send gx)`, `(recv gy)`, `(send (enc n (CDH gx gy dhkey)))`
  - `resp`: `(vars (gx gy akey) (n text) (dhkey skey))`, `(uniq-orig gy)`, `(non-orig (invk gy) dhkey)`, trace: `(recv gx)`, `(send gy)`, `(recv (enc n (CDH gx gy dhkey)))`
  - `CDHcalc1`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gx (invk gy)))`, `(send (CDH gx gy dhkey))`
  - `CDHcalc2`: `(vars (gx gy akey) (dhkey skey))`, trace: `(recv (cat gy (invk gx)))`, `(send (CDH gx gy dhkey))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macro**: `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))`
  - **Skeleton**: `(defskeleton dh_mim (vars (n text) (gx gy akey) (dhkey skey)) (defstrand init 3 (n n) (gx gx) (dhkey dhkey)) (defstrand resp 3 (n n) (gy gy) (dhkey dhkey)) (precedes ((0 2) (1 2))) (comment "Agreement on the encrypted text only"))`.
- **When to Reference This Example**: Reference this example when demonstrating a Diffie-Hellman man-in-the-middle attack in the `basic` algebra where `init` and `resp` agree on the payload `n` (`(precedes ((0 2) (1 2)))`) while the adversary substitutes its own DH half-keys via `CDHcalc1` and `CDHcalc2`.
- **Key S-Expression Excerpt**:
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

## dhnsl_hack.scm

- **File Path**: `03_examples_scm/dhnsl_hack.scm`
- **Algebra & Herald**: `(herald "Diffie-Hellman enhanced Needham-Schroeder-Lowe Protocol" (algebra basic))` — `basic` algebra (`(defprotocol dhnsl basic ...)`), with herald flag `(algebra basic)`.
- **Protocol & Purpose**: Models a Diffie-Hellman enhanced Needham-Schroeder-Lowe (NSL) protocol in the `basic` algebra where DH public values (`gx`, `gy`, `gz` of sort `akey`) and CDH tokens `(CDH gy gx dhkey)` and `(CDH gz gx dhkey)` replace traditional nonces inside public-key encrypted messages.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b name) (h2 h3 gx akey) (dhkey skey))`
    - Role-level assumptions: `(uniq-orig gx)`, `(non-orig (invk gx) dhkey)`
    - Trace:
      1. `(send (enc gx a (pubk b)))`
      2. `(recv (enc h2 (CDH h2 gx dhkey) h3 b (pubk a)))`
      3. `(send (enc (CDH h3 gx dhkey) (pubk b)))`
  - `resp`:
    - `(vars (b a name) (h1 gy gz akey) (dhkey skey))`
    - Role-level assumptions: `(uniq-orig gy gz)`, `(non-orig (invk gy) (invk gz) dhkey)`
    - Trace:
      1. `(recv (enc h1 a (pubk b)))`
      2. `(send (enc gy (CDH gy h1 dhkey) gz b (pubk a)))`
      3. `(recv (enc (CDH gz h1 dhkey) (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macro**: `(defmacro (CDH gx gy dhkey) (enc "dh" gx gy dhkey))`
  - **Skeletons**: 2 `(defskeleton dhnsl ...)` queries:
    1. `(defstrand init 3 (a a) (b b) (h2 gy) (h3 gz) (gx gx))` with `(non-orig (privk b) (privk a))`
    2. `(defstrand resp 3 (a a) (b b) (h1 gx) (gy gy) (gz gz))` with `(non-orig (privk a))`
- **When to Reference This Example**: Reference this example when modeling hybrid public-key / Diffie-Hellman challenge-response protocols (such as DH-enhanced NSL) using the `(CDH ...)` macro in the `basic` algebra.
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## dhstatic-state.scm

- **File Path**: `03_examples_scm/dhstatic-state.scm`
- **Algebra & Herald**: `(herald dhstatic-state (algebra diffie-hellman) (bound 16))` — `diffie-hellman` algebra (`(defprotocol dhstatic-state diffie-hellman ...)`), with herald flags `(algebra diffie-hellman)` and `(bound 16)`.
- **Protocol & Purpose**: Models a static Diffie-Hellman key agreement protocol with PKI enrollment (`cert` and `get-cert`) where a principal's static DH private key `(ra rndx)` and certificate metadata are stored in a local state location `(static-key locn)` via `(stor static-key (cat "privkey" self ra serial ca))` and later retrieved via `(load static-key ...)` in `init` and `resp`. Also demonstrates role-level `(gen-st ...)`, role-level inequality facts `(facts (neq a b))`, and custom `(lang ...)` operators (`cert-req`, `cert`, `sig`) inside the `diffie-hellman` algebra.
- **Roles & Variables**:
  - `cert`:
    - `(vars (subj ca name) (serial data) (galpha mesg))`
    - Role-level assumptions: `(uniq-orig serial)`
    - Trace: `(recv (sig (cert-req subj galpha ca) (privk "sig" subj)))`, `(send (sig (cert subj galpha ca serial) (privk "sig" ca)))`
  - `get-cert`:
    - `(vars (self ca name) (serial data) (ra rndx) (static-key locn) (ignore mesg))`
    - Role-level assumptions: `(uniq-gen ra)`
    - Trace: `(send (sig (cert-req self (exp (gen) ra) ca) (privk "sig" self)))`, `(recv (sig (cert self (exp (gen) ra) ca serial) (privk "sig" ca)))`, `(load static-key ignore)`, `(stor static-key (cat "privkey" self ra serial ca))`
  - `init`:
    - `(vars (a b ca name) (ra rndx) (serial-a serial-b data) (alpha expt) (n text) (static-key locn))`
    - Role-level assumptions: `(uniq-orig n)`, `(gen-st (cat "privkey" a ra serial-a ca))`, `(facts (neq a b))`
    - Trace: `(load static-key (cat "privkey" a ra serial-a ca))`, `(recv (sig (cert b (exp (gen) alpha) ca serial-b) (privk "sig" ca)))`, `(send (enc n a b serial-a serial-b (exp (exp (gen) alpha) ra)))`, `(recv n)`
  - `resp`:
    - `(vars (a b ca name) (rb rndx) (serial-b serial-a data) (alpha expt) (n text) (static-key locn))`
    - Role-level assumptions: `(facts (neq a b))`, `(gen-st (cat "privkey" b rb serial-b ca))`
    - Trace: `(load static-key (cat "privkey" b rb serial-b ca))`, `(recv (sig (cert a (exp (gen) alpha) ca serial-a) (privk "sig" ca)))`, `(recv (enc n a b serial-a serial-b (exp (exp (gen) alpha) rb)))`, `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - **Language Declarations**: `(lang (cert-req (tupl 3)) (cert (tupl 4)) (sig sign))`
  - **Skeletons**: 2 `(defskeleton dhstatic-state ...)` queries:
    1. `(defstrand init 4 (ca ca) (b b))` with `(non-orig (privk "sig" ca) (privk "sig" b))`
    2. `(defstrand resp 4 (ca ca) (a a))` with `(non-orig (privk "sig" ca) (privk "sig" a))`
- **When to Reference This Example**: Reference this example when combining the `diffie-hellman` algebra with stateful `locn` storage (`load`/`stor` and role-level `(gen-st ...)`), role-level inequality constraints `(facts (neq a b))` (to prevent self-communication reflections in static DH), and custom `(lang ...)` operators.
- **Key S-Expression Excerpt**:
```scheme
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

  (lang (cert-req (tupl 3))
	(cert (tupl 4))
	(sig sign)))
```

---

## disclosure.scm

- **File Path**: `03_examples_scm/disclosure.scm`
- **Algebra & Herald**: `(herald disclosure)` — `basic` algebra (`(defprotocol disc basic ...)`).
- **Protocol & Purpose**: Illustrates a protocol (`disc`) where an initiator (`init`) uses a key `k` declared `(pen-non-orig k)` to encrypt `(enc a b n k)`, receives `n` back, and then discloses `k` in its third step `(send k)`. Because `k` is only `pen-non-orig` (not `non-orig`, since `init` itself originates `k` at step 3), an `init` strand of height 2 can be satisfied in two distinct ways: either by an honest `resp` strand, or by the adversary obtaining `k` from a completed height-3 `init` strand in another session. Demonstrates how CPSA introduces and generalizes listeners during shape analysis.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b name) (k skey) (n text))`
    - Role-level assumptions: `(pen-non-orig k)`
    - Trace: `(send (enc a b n k))`, `(recv n)`, `(send k)`
  - `resp`:
    - `(vars (a b name) (k skey) (n text))`
    - Trace: `(recv (enc a b n k))`, `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton disc (vars (n text)) (defstrand init 2 (n n)) (uniq-orig n))`.
- **When to Reference This Example**: Reference this example when modeling deliberate key disclosure (e.g., TESLA or delayed key release protocols) where a symmetric key `k` is eventually transmitted in plaintext by an honest role (`(send k)`), requiring `(pen-non-orig k)` instead of `(non-orig k)` so the role's own key emission does not violate non-origination.
- **Key S-Expression Excerpt**:
```scheme
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

## doorsep.scm

- **File Path**: `03_examples_scm/doorsep.scm`
- **Algebra & Herald**: `(herald doorsep (comment "Door Simple Example Protocol"))` — `basic` algebra (`(defprotocol doorsep basic ...)`).
- **Protocol & Purpose**: Models the Door Simple Example Protocol (`doorsep`) from the CPSA Primer using unnamed asymmetric keys (`d p akey`). A `person` sends a fresh session key `k` signed with `(invk p)` and encrypted under `d` (`(enc (enc k (invk p)) d)`), the `door` replies with a fresh token `t` encrypted under `k` (`(enc t k)`), and the `person` returns `t` in the clear. Includes a `defrule trust` stating that if an uncompromised `person` (`(non (invk p))`) initiates a session with door key `d`, then `d`'s private key is also uncompromised (`(non (invk d))`).
- **Roles & Variables**:
  - `person`:
    - `(vars (d p akey) (k skey) (t text))`
    - Role-level assumptions: `(uniq-orig k)`
    - Trace: `(send (enc (enc k (invk p)) d))`, `(recv (enc t k))`, `(send t)`
  - `door`:
    - `(vars (d p akey) (k skey) (t text))`
    - Role-level assumptions: `(uniq-orig t)`
    - Trace: `(recv (enc (enc k (invk p)) d))`, `(send (enc t k))`, `(recv t)`
- **Skeletons, Goals, Rules & Macros**:
  - **Rule**: `trust` (`(forall ((z strd) (p d akey)) (implies (and (p "person" z 1) (p "person" "p" z p) (p "person" "d" z d) (non (invk p))) (non (invk d))))`).
  - **Skeleton**: `(defskeleton doorsep (vars (p akey)) (defstrand door 3 (p p)) (non-orig (invk p)) (comment "Analyze from the doors's perspective"))`.
- **When to Reference This Example**: Reference this example as the canonical, minimal introduction to writing a `defrule` trust axiom (`(implies (and (p "person" z 1) ... (non (invk p))) (non (invk d)))`) that prevents man-in-the-middle key substitution in a two-party protocol.
- **Key S-Expression Excerpt**:
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

## doorsep2invk.scm

- **File Path**: `03_examples_scm/doorsep2invk.scm`
- **Algebra & Herald**: `(herald doorsep2invk (comment "Door Simple Example Protocol"))` — `basic` algebra (`(defprotocol doorsep basic ...)`).
- **Protocol & Purpose**: Variant of `doorsep` with roles named `init` and `resp` and a single `(defgoal doorsep ...)` testing a formula where the `peer` / `self` parameter is instantiated with an inverted key `(invk akey+3)` (`(p "resp" "peer" z (invk akey+3))` and `(non akey+3)`) and trivial conclusion `(and)`.
- **Roles & Variables**:
  - `init`:
    - `(vars (self peer akey) (skey skey) (data text))`
    - Role-level assumptions: `(uniq-orig skey)`
    - Trace: `(send (enc (enc skey (invk self)) peer))`, `(recv (enc data skey))`, `(send data)`
  - `resp`:
    - `(vars (self peer akey) (skey skey) (data text))`
    - Role-level assumptions: `(uniq-orig data)`
    - Trace: `(recv (enc (enc skey (invk peer)) self))`, `(send (enc data skey))`, `(recv data)`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defgoal doorsep ...)` using `forall`, `implies`, `and`, `p`, `prec`, `non`, and `uniq-at`, with empty conjunction `(and)` as conclusion.
- **When to Reference This Example**: Reference this example when examining how `defgoal` handles involutive `akey` expressions where `(invk akey+3)` is bound to a role parameter and `(non akey+3)` asserts non-origination of its inverse.
- **Key S-Expression Excerpt**:
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

## encsig.scm

- **File Path**: `03_examples_scm/encsig.scm`
- **Algebra & Herald**: `(herald "Encrypted Signed Message Example" (comment "Shows examples of key usage of asymmetric keys"))` — `basic` algebra (`(defprotocol mult-keys-enc-sig basic ...)`).
- **Protocol & Purpose**: Demonstrates how to separate encryption key pairs from signature key pairs for the same principal using string-tagged `(pubk "enc" b)` / `(privk "enc" b)` and `(pubk "sig" a)` / `(privk "sig" a)` in an encrypt-then-sign challenge-response protocol (`mult-keys-enc-sig`). Explores how responder authentication depends on whether `a`'s signature key `(privk "sig" a)`, encryption key `(privk "enc" a)`, or both are assumed `non-orig`.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b name) (n1 n2 text))`
    - Trace:
      1. `(send (enc (enc n1 a (pubk "enc" b)) (privk "sig" a)))`
      2. `(recv (enc (enc n1 n2 (pubk "enc" a)) (privk "sig" b)))`
      3. `(send (enc (enc n2 (pubk "enc" b)) (privk "sig" a)))`
  - `resp`:
    - `(vars (b a name) (n2 n1 text))`
    - Trace:
      1. `(recv (enc (enc n1 a (pubk "enc" b)) (privk "sig" a)))`
      2. `(send (enc (enc n1 n2 (pubk "enc" a)) (privk "sig" b)))`
      3. `(recv (enc (enc n2 (pubk "enc" b)) (privk "sig" a)))`
- **Skeletons, Goals, Rules & Macros**:
  - 4 `(defskeleton mult-keys-enc-sig ...)` queries:
    1. `init` height 3 with `(non-orig (privk "enc" a) (privk "sig" a) (privk "sig" b))` and `(uniq-orig n1)`
    2. `resp` height 3 trusting only `a`'s signature key: `(non-orig (privk "sig" a))` and `(uniq-orig n2)`
    3. `resp` height 3 trusting only `a`'s encryption key: `(non-orig (privk "enc" a))` and `(uniq-orig n2)`
    4. `resp` height 3 trusting both of `a`'s keys: `(non-orig (privk "sig" a) (privk "enc" a))` and `(uniq-orig n2)`
- **When to Reference This Example**: Reference this example whenever an RFC or protocol uses distinct public/private key pairs per principal for encryption vs. signing—modeled in CPSA via two-argument `(pubk "enc" a)` / `(privk "enc" a)` and `(pubk "sig" a)` / `(privk "sig" a)`.
- **Key S-Expression Excerpt**:
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

;;; The responder point-of-view trusting both of a's keys
(defskeleton mult-keys-enc-sig
  (vars (a b name) (n2 text))
  (defstrand resp 3 (a a) (b b) (n2 n2))
  (non-orig (privk "sig" a) (privk "enc" a))
  (uniq-orig n2))
```

---

## envelope.scm

- **File Path**: `03_examples_scm/envelope.scm`
- **Algebra & Herald**: `(herald "Envelope Protocol" (bound 15))` — `basic` algebra (`(defprotocol envelope basic ...)` repeated 3 times with progressively stronger rule sets), with `(bound 15)`.
- **Protocol & Purpose**: Non-channel counterpart to `chan-envelope.scm`. Models the TPM Envelope Protocol by encoding the TPM's current PCR register value as a message encrypted under a hashed secret key `(enc current-value (hash pcrkey))` with `(non-orig pcrkey)` (where hashing `pcrkey` prevents key confusion with the encrypted session key `esk`). Evaluates three rule sets (empty, `ordered-extends`, and `ordered-extends` + `esk-same-as-pcrkey`) across the same three listener scenarios (`v`, `(refuse n v k aik)`, and both).
- **Roles & Variables**:
  - Defined inside `(defmacro (roles) (^ ...))`:
    - `tpm-power-on`: `(vars (pcrkey skey))`, `(non-orig pcrkey)`, trace: `(recv "power on")`, `(send (enc "0" (hash pcrkey)))`
    - `tpm-extend`: `(vars (value current-value mesg) (pcrkey skey))`, `(non-orig pcrkey)`, trace: `(recv (cat "extend" value))`, `(recv (enc current-value (hash pcrkey)))`, `(send (enc (hash current-value value) (hash pcrkey)))`, `(send "ext ok")`
    - `tpm-extend-enc`: `(vars (value current-value mesg) (pcrkey esk skey))`, `(non-orig pcrkey esk)`, trace: `(recv (enc "extend" value esk))`, `(recv (enc current-value (hash pcrkey)))`, `(send (enc (hash current-value value) (hash pcrkey)))`, `(send "ext ok")`
    - `tpm-quote`: `(vars (nonce current-value mesg) (pcrkey skey) (aik akey))`, `(non-orig aik pcrkey)`, trace: `(recv (cat "quote" nonce))`, `(recv (enc current-value (hash pcrkey)))`, `(send (enc "quote" current-value nonce aik))`
    - `tpm-create-key`: `(vars (k aik akey) (pcrval mesg) (esk skey))`, `(uniq-orig k)`, `(non-orig (invk k) aik esk)`, trace: `(recv (enc "create key" pcrval esk))`, `(send (enc "created" k pcrval aik))`
    - `tpm-decrypt`: `(vars (m pcrvals mesg) (k aik akey) (pcrkey skey))`, `(non-orig aik pcrkey)`, trace: `(recv (cat "decrypt" (enc m k)))`, `(recv (enc "created" k pcrvals aik))`, `(recv (enc pcrvals (hash pcrkey)))`, `(send m)`
    - `alice`: `(vars (n v data) (esk skey) (k aik akey))`, `(uniq-orig n v)`, `(non-orig aik esk)`, trace: `(send (enc "extend" n esk))`, `(send (enc "create key" (hash (hash "0" n) "obtain") esk))`, `(recv (enc "created" k (hash (hash "0" n) "obtain") aik))`, `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: `(defmacro (refuse n v k aik) ...)` and `(defmacro (roles) (^ ...))`.
  - **Rules**: `ordered-extends` (forces linear ordering on `tpm-extend` strands sharing `pcrkey`) and `esk-same-as-pcrkey` (forces `(= pcrkey pcrkey-0)` when two `tpm-extend-enc` strands share `esk`).
  - **Skeletons**: 9 `(defskeleton envelope ...)` queries (3 per protocol block).
- **When to Reference This Example**: Reference this example when modeling state-carrying encrypted tokens `(enc current-value (hash pcrkey))` without `locn` or `chan`, using `defrule` axioms to enforce linear state updates (`(or (= y z) (prec y 2 z 3) (prec z 2 y 3))`).
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## epmo-hash.scm

- **File Path**: `03_examples_scm/epmo-hash.scm`
- **Algebra & Herald**: `(herald "Electronic Purchase with Money Order Protocol with Key Hashing" (comment "Annotated with trust management formulas"))` — `basic` algebra (`(defprotocol epmo basic ...)`).
- **Protocol & Purpose**: Models the Electronic Purchase with Money Order (`epmo`) protocol between a `bank` (`b`), `customer` (`c`), and `merchant` (`m`), using CPSA's built-in `(hash ...)` operator inside signed money orders `(enc (hash c nc nb nm price) (privk b))` and merchant endorsements `(enc (hash b nb nm) (privk m))`. Includes role-level `(annotations ...)` with trust-management formulas (`says`, `transfer`, `ship`) attached to specific node indices.
- **Roles & Variables**:
  - `bank`:
    - `(vars (b c m name) (nc nm nb data) (price text))`
    - Role-level assumptions & annotations: `(uniq-orig nb)`, `(annotations b (1 ...) (2 ...))`
    - Trace:
      1. `(recv (enc c nc nm price (pubk b)))`
      2. `(send (cat (enc (hash c nc nb nm price) (privk b)) (enc nc nb (pubk c))))`
      3. `(recv (enc (hash b nb nm) (privk m)))`
  - `customer`:
    - `(vars (b c m name) (nb nc nm data) (goods price text))`
    - Role-level assumptions & annotations: `(uniq-orig nc)`, `(annotations c (1 ...) (3 ...) (4 ...))`
    - Trace:
      1. `(send (enc c nc goods price (pubk m)))`
      2. `(recv (enc nc nm m goods price (pubk c)))`
      3. `(send (enc c nc nm price (pubk b)))`
      4. `(recv (cat (enc (hash c nc nb nm price) (privk b)) (enc nc nb (pubk c))))`
      5. `(send (cat (enc (hash c nc nb nm price) (privk b)) nb))`
  - `merchant`:
    - `(vars (b c m name) (nb nc nm data) (goods price text))`
    - Role-level assumptions & annotations: `(uniq-orig nm)`, `(annotations m (1 ...) (2 ...) (3 ...))`
    - Trace:
      1. `(recv (enc c nc goods price (pubk m)))`
      2. `(send (enc nc nm m goods price (pubk c)))`
      3. `(recv (cat (enc (hash c nc nb nm price) (privk b)) nb))`
      4. `(send (enc (hash b nb nm) (privk m)))`
- **Skeletons, Goals, Rules & Macros**:
  - 3 `(defskeleton epmo ...)` queries testing `customer` height 5, `bank` height 3, and `merchant` height 4, each with `(non-orig (privk b) (privk c) (privk m))`.
- **When to Reference This Example**: Reference this example when modeling three-party e-commerce / payment protocols using `(hash ...)` inside digital signatures or when attaching trust-management `(annotations <principal> (<node-index> <formula>) ...)` to roles.
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## epmo-key-hash.scm

- **File Path**: `03_examples_scm/epmo-key-hash.scm`
- **Algebra & Herald**: `(herald "Electronic Purchase with Money Order Protocol with Key Hashing" (comment "Annotated with trust management formulas"))` — `basic` algebra (`(defprotocol epmo basic ...)`).
- **Protocol & Purpose**: Variant of `epmo-hash.scm` that models hashing via two-argument `enc` with a string literal `"hash"` (`(enc "hash" (cat c nc nb nm price))` and `(enc "hash" (cat b nb nm))`) instead of the unary `(hash ...)` operator, while preserving the same `bank`, `customer`, and `merchant` roles and trust-management `(annotations ...)`.
- **Roles & Variables**:
  - `bank`: `(vars (b c m name) (nc nm nb data) (price text))`, `(uniq-orig nb)`, `(annotations b (1 ...) (2 ...))`, trace uses `(enc (enc "hash" (cat c nc nb nm price)) (privk b))` and `(enc (enc "hash" (cat b nb nm)) (privk m))`
  - `customer`: `(vars (b c m name) (nb nc nm data) (goods price text))`, `(uniq-orig nc)`, `(annotations c (1 ...) (3 ...) (4 ...))`
  - `merchant`: `(vars (b c m name) (nb nc nm data) (goods price text))`, `(uniq-orig nm)`, `(annotations m (1 ...) (2 ...) (3 ...))`
- **Skeletons, Goals, Rules & Macros**:
  - 3 `(defskeleton epmo ...)` queries testing `customer` height 5, `bank` height 3, and `merchant` height 4 with `(non-orig (privk b) (privk c) (privk m))`.
- **When to Reference This Example**: Reference this example alongside `epmo-hash.scm` and `epmo.scm` to compare older/alternative CPSA idioms for hashing (`(enc "hash" (cat ...))` vs. `(hash ...)`).
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## epmo.scm

- **File Path**: `03_examples_scm/epmo.scm`
- **Algebra & Herald**: `(herald "Electronic Purchase with Money Order Protocol" (comment "Annotated with trust management formulas"))` — `basic` algebra (`(defprotocol epmo basic ...)`).
- **Protocol & Purpose**: Original formulation of the Electronic Purchase with Money Order (`epmo`) protocol that models cryptographic hashing as encryption under a public key variable `(hash akey)` whose inverse is uncompromised (`(non-orig (invk hash))`). Each role (`bank`, `customer`, `merchant`) declares `(hash akey)` in `(vars ...)` and `(non-orig (invk hash))` in the role body, writing `(enc c nc nb nm price hash)` and `(enc b nb nm hash)`.
- **Roles & Variables**:
  - `bank`:
    - `(vars (b c m name) (hash akey) (nc nm nb data) (price text))`
    - Role-level assumptions & annotations: `(non-orig (invk hash))`, `(uniq-orig nb)`, `(annotations b (1 ...) (2 ...))`
    - Trace: `(recv (enc c nc nm price (pubk b)))`, `(send (cat (enc (enc c nc nb nm price hash) (privk b)) (enc nc nb (pubk c))))`, `(recv (enc (enc b nb nm hash) (privk m)))`
  - `customer`:
    - `(vars (b c m name) (hash akey) (nb nc nm data) (goods price text))`
    - Role-level assumptions & annotations: `(non-orig (invk hash))`, `(uniq-orig nc)`, `(annotations c (1 ...) (3 ...) (4 ...))`
    - Trace: `(send (enc c nc goods price (pubk m)))`, `(recv (enc nc nm m goods price (pubk c)))`, `(send (enc c nc nm price (pubk b)))`, `(recv (cat (enc (enc c nc nb nm price hash) (privk b)) (enc nc nb (pubk c))))`, `(send (cat (enc (enc c nc nb nm price hash) (privk b)) nb))`
  - `merchant`:
    - `(vars (b c m name) (hash akey) (nb nc nm data) (goods price text))`
    - Role-level assumptions & annotations: `(non-orig (invk hash))`, `(uniq-orig nm)`, `(annotations m (1 ...) (2 ...) (3 ...))`
    - Trace: `(recv (enc c nc goods price (pubk m)))`, `(send (enc nc nm m goods price (pubk c)))`, `(recv (cat (enc (enc c nc nb nm price hash) (privk b)) nb))`, `(send (enc (enc b nb nm hash) (privk m)))`
- **Skeletons, Goals, Rules & Macros**:
  - 3 `(defskeleton epmo ...)` queries testing `customer` height 5, `bank` height 3, and `merchant` height 4 with `(non-orig (privk b) (privk c) (privk m))`.
- **When to Reference This Example**: Reference this example to recognize legacy CPSA models where a one-way hash function is modeled as an asymmetric key variable `(hash akey)` with `(non-orig (invk hash))` (and note that modern CPSA provides the built-in unary `(hash ...)` operator used in `epmo-hash.scm`).
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## epmo_acctnum-key-hash.scm

- **File Path**: `03_examples_scm/epmo_acctnum-key-hash.scm`
- **Algebra & Herald**: `(herald "Electronic Purchase with Money Order Protocol Variant with Key Hashing" (comment "This version includes account numbers in exchanges"))` — `basic` algebra (`(defprotocol epmo_acctnum basic ...)`).
- **Protocol & Purpose**: Variant of the EPMO protocol (`epmo_acctnum`) that adds an account number `(acctnum text)` to the customer-to-bank request and declares all nonces (`nb`, `nc`, `nm`) and `price` as sort `text` (instead of separating `data` and `text`), while omitting `(uniq-orig nb)` from the `bank` role. As documented in the file's comments, this produces an interesting counterexample shape during generalization where the bank's nonce `nb` becomes unified with `price` (which originates on the `merchant` strand) and cannot be separated during generalization unless `(uniq-orig nb)` is declared at the role level on `bank`.
- **Roles & Variables**:
  - `bank`:
    - `(vars (b c m name) (acctnum text) (nc nm nb price text))`
    - Role-level annotations: `(annotations b (1 ...) (2 ...))` (no `uniq-orig nb` in role)
    - Trace: `(recv (enc c nc nm acctnum price (pubk b)))`, `(send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) (enc nc nb (pubk c))))`, `(recv (enc (enc "hash" (cat b m nb nm)) (privk m)))`
  - `customer`:
    - `(vars (b c m name) (acctnum nb nc nm goods price text))`
    - Role-level assumptions & annotations: `(non-orig (privk b))`, `(uniq-orig nc)`, `(annotations c (1 ...) (3 ...) (4 ...))`
    - Trace: `(send (enc c nc goods (pubk m)))`, `(recv (enc nc nm m price (pubk c)))`, `(send (enc c nc nm acctnum price (pubk b)))`, `(recv (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) (enc nc nb (pubk c))))`, `(send (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) nb))`
  - `merchant`:
    - `(vars (b c m name) (nb nc nm goods price text))`
    - Role-level assumptions & annotations: `(uniq-orig nm)`, `(annotations m (1 ...) (2 ...) (3 ...))`
    - Trace: `(recv (enc c nc goods (pubk m)))`, `(send (enc nc nm m price (pubk c)))`, `(recv (cat (enc (enc "hash" (cat c nc nb nm price)) (privk b)) nb))`, `(send (enc (enc "hash" (cat b m nb nm)) (privk m)))`
- **Skeletons, Goals, Rules & Macros**:
  - 2 `(defskeleton epmo_acctnum ...)` queries testing `merchant` height 4 and `bank` height 3 with `(non-orig (privk b) (privk m) (privk c))` and `(uniq-orig nm nc nb)`.
- **When to Reference This Example**: Reference this example to understand why declaring `(uniq-orig ...)` inside a `defrole` (role-level unique origination) is stronger than declaring `(uniq-orig ...)` only in `defskeleton`, and how giving nonces (`nb`) and protocol fields (`price`) the same sort (`text`) can cause unexpected variable identification (`nb = price`) if role-level `uniq-orig` is omitted.
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## expand.scm

- **File Path**: `03_examples_scm/expand.scm`
- **Algebra & Herald**: `(herald expand (expand) (comment "test macro expansion"))` — `basic` algebra (`(defprotocol expand basic ...)`), with herald flag `(expand)`.
- **Protocol & Purpose**: Minimal regression test demonstrating CPSA's `(defmacro ...)` facility, the splice marker `^` inside macros, and the `(expand)` herald option (which instructs CPSA to stop after macro expansion and output the expanded S-expressions).
- **Roles & Variables**:
  - `init`:
    - `(vars (t text) (k skey))`
    - Trace: `(send (altenc t k))`, `(recv (cat (altcat t k)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: `(defmacro (altenc t k) (enc t k))` and `(defmacro (altcat a b) (^ a b))` (where `^` splices `a` and `b` directly into the surrounding `(cat ...)` form).
  - **Skeleton**: `(defskeleton expand (vars) (defstrand init 2))`.
- **When to Reference This Example**: Reference this example for the exact syntax of `(defmacro (<name> <args>...) <body>)`, the splice operator `(^ ...)` for flattening macro arguments into a parent list, and the `(expand)` herald flag.
- **Key S-Expression Excerpt**:
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

## facts.scm

- **File Path**: `03_examples_scm/facts.scm`
- **Algebra & Herald**: `(herald facts)` — `basic` algebra across two protocols (`unilateral` and `iso-unilateral`).
- **Protocol & Purpose**: Demonstrates how user-defined relational facts (`(facts (foo 0 k) (bar 0 (invk k)))` in `defskeleton` and `(fact foo z k)` in `defgoal`) and security goals (`defgoal`) work in CPSA. Also models the two-pass unilateral authentication protocol from ISO/IEC JTC 1/SC 27/WG 2 N1050 (`iso-unilateral`) and tests both satisfied and intentionally falsified (`(false)`) `defgoal` assertions.
- **Roles & Variables**:
  - In `unilateral`:
    - `init`: `(vars (n text) (k akey))`, `(uniq-orig n)`, trace: `(send (enc n k))`, `(recv n)`
    - `resp`: `(vars (n text) (k akey))`, trace: `(recv (enc n k))`, `(send n)`
  - In `iso-unilateral`:
    - `resp`: `(vars (na nb t1 t2 t3 text) (b name))`, `(uniq-orig na)`, trace: `(recv (cat nb t1))`, `(send (cat na nb b t3 (enc na nb b t2 (privk b))))`
    - `init`: `(vars (na nb t1 t2 t3 text) (b name))`, `(uniq-orig nb)`, trace: `(send (cat nb t1))`, `(recv (cat na nb b t3 (enc na nb b t2 (privk b))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Skeletons**:
    1. `unilateral` `init` height 2 with `(non-orig (invk k))` and `(facts (foo 0 k) (bar 0 (invk k)))` (where `0` is strand index 0).
    2. `unilateral` `resp` height 2 with `(pen-non-orig n)` and `(non-orig (invk k))`.
    3. `iso-unilateral` `init` height 2 with `(non-orig (privk b))`.
  - **Goals** (`defgoal`):
    1. `unilateral` goal from `init` perspective incorporating `(fact foo z k)`, `(fact bar z (invk k))`, `(uniq-at n z 0)`, and `(prec ...)`.
    2. `unilateral` goal from `resp` perspective using `(pnon n)` (the formula predicate for `pen-non-orig`).
    3. `iso-unilateral` authentication goal concluding `(exists ((y strd)) (and (p "resp" y 2) (p "resp" "b" y b)))`.
    4. `iso-unilateral` intentionally false goal concluding `(false)`.
- **When to Reference This Example**: Reference this example when attaching custom `(facts (<pred> <strand-idx-or-term> ...))` to a `defskeleton` and referencing them via `(fact <pred> <strd-var> ...)` in a `defgoal` or `defrule`, or when using `(pnon n)` and `(uniq-at n z 0)` in `defgoal` formulas.
- **Key S-Expression Excerpt**:
```scheme
(defskeleton unilateral
   (vars (k akey))
   (defstrand init 2 (k k))
   (non-orig (invk k))
   (facts (foo 0 k)
	  (bar 0 (invk k))))

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
```

---

## factvar.scm

- **File Path**: `03_examples_scm/factvar.scm`
- **Algebra & Herald**: `(herald factvar)` — `basic` algebra (`(defprotocol free-fact-var basic ...)`).
- **Protocol & Purpose**: Demonstrates a `defrule` (`add`) whose existential conclusion `(exists ((m text)) (fact thing m))` introduces a fresh variable `m` of sort `text` that appears only inside a `fact` and does not occur in any strand.
- **Roles & Variables**:
  - `resp`:
    - `(vars (n text) (k akey))`
    - Trace: `(recv (enc n k))`, `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - **Rule**: `add` (`(forall ((z strd)) (implies (p "resp" z 1) (exists ((m text)) (fact thing m))))`).
  - **Skeletons**: 2 `(defskeleton free-fact-var ...)` blocks:
    1. `(defstrand resp 1 (k k))` with `(non-orig (invk k))`
    2. `(defstrand resp 1 (n n) (k k))` with `(non-orig (invk k))` and `(pen-non-orig n)`
- **When to Reference This Example**: Reference this example when writing a `defrule` that existentially quantifies a ghost/auxiliary variable (`(exists ((m text)) (fact thing m))`) used solely inside `fact` relations rather than protocol messages.
- **Key S-Expression Excerpt**:
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
  (vars (n text) (k akey))
  (defstrand resp 1 (n n) (k k))
  (non-orig (invk k))
  (pen-non-orig n))
```

---

## ffgg.scm

- **File Path**: `03_examples_scm/ffgg.scm`
- **Algebra & Herald**: `(herald "The ffgg Protocol" (comment "From A Necessarily Parallel Attack by Jon K. Millen"))` — `basic` algebra (`(defprotocol ffgg basic ...)`).
- **Protocol & Purpose**: Models Jon K. Millen's `ffgg` protocol from "A Necessarily Parallel Attack", designed to exhibit a secrecy attack on the secret `(m text)` that requires two parallel responder runs (`resp`). The responder generates two nonces `(uniq-orig n1 n2)`, sends `(cat b n1 n2)`, receives `(cat a (enc n1 x y (pubk b)))`, and replies with `(cat n1 x (enc x y n1 (pubk b)))`—exposing the first inner component `x` in plaintext and shifting `(x, y, n1)` inside the encryption, which allows an attacker running two parallel sessions to extract `m` from `(enc n1 n2 m (pubk b))`.
- **Roles & Variables**:
  - `init`:
    - `(vars (a b name) (n1 n2 m x y text))`
    - Trace: `(send a)`, `(recv (cat b n1 n2))`, `(send (cat a (enc n1 n2 m (pubk b))))`, `(recv (cat n1 x (enc x y n1 (pubk b))))`
  - `resp`:
    - `(vars (b a name) (n1 n2 x y text))`
    - Role-level assumptions: `(uniq-orig n1 n2)`
    - Trace: `(recv a)`, `(send (cat b n1 n2))`, `(recv (cat a (enc n1 x y (pubk b))))`, `(send (cat n1 x (enc x y n1 (pubk b))))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton ffgg (vars (b name) (n1 n2 m text)) (defstrand init 4 (b b) (m m)) (deflistener m) (uniq-orig m) (non-orig (privk b)))`.
- **When to Reference This Example**: Reference this example when studying multi-session / parallel-session oracle attacks in CPSA where an encryption oracle shifts positional fields inside `(enc ... (pubk b))` and leaks `m` to `(deflistener m)`.
- **Key S-Expression Excerpt**:
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

## fluffy_draft03_gske.scm

- **File Path**: `03_examples_scm/fluffy_draft03_gske.scm`
- **Algebra & Herald**: `(herald "GSKE, part of Fluffy: Simplified Key Exchange for Constrained Environments draft-hardjono-ace-fluffy-03" (comment "Based on the Internet-Draft: https://www.ietf.org/archive/id/draft-hardjono-ace-fluffy-03.txt"))` — `basic` algebra across two protocol definitions (`fluffy` and `fluffy-rule`).
- **Protocol & Purpose**: Models the Group Symmetric Key Establishment (GSKE) sub-protocol of the IETF ACE Fluffy Internet-Draft (`draft-hardjono-ace-fluffy-03`), involving a service principal (`sp`), a simple key distribution center (`keyserv`), and a `client` sharing long-term symmetric keys `(ltk s b)` and `(ltk s a)`. Because `"req"`/`"fetch"` and `"resp"`/`"deliver"` encryptions under `(ltk s ...)` have identical ciphertext structures `(enc s g nb gk (ltk s b))` and `(enc s g na gk (ltk s a))`, `fluffy` allows role confusion where a client acts as a service principal or vice versa; `fluffy-rule` adds two `defrule` axioms (`client-no-request` and `sp-no-fetch`) that forbid `a` and `b` from playing both roles with the same key server `s`.
- **Roles & Variables**:
  - Identical in `fluffy` and `fluffy-rule`:
    - `sp`: `(vars (b s name) (nb g text) (gk skey))`, trace: `(send (cat "req" s g (enc b nb (ltk s b))))`, `(recv (cat "resp" b (enc s g nb gk (ltk s b))))`
    - `keyserv`: `(vars (a b s name) (nb na g text) (gk skey))`, `(uniq-gen gk)`, trace: `(recv (cat "req" s g (enc b nb (ltk s b))))`, `(send (cat "resp" b (enc s g nb gk (ltk s b))))`, `(recv (cat "fetch" s g (enc a na (ltk s a))))`, `(send (cat "deliver" a (enc s g na gk (ltk s a))))`
    - `client`: `(vars (a b s name) (na g text) (gk skey))`, trace: `(send (cat "fetch" s g (enc a na (ltk s a))))`, `(recv (cat "deliver" a (enc s g na gk (ltk s a))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Rules** (in `fluffy-rule`): `client-no-request` and `sp-no-fetch` (using `(false)` to enforce disjoint principal sets for `client` and `sp`).
  - **Skeletons**: 6 `(defskeleton ...)` queries (3 for `fluffy`, 3 for `fluffy-rule`) testing `sp` height 2, `keyserv` height 4, and `client` height 2 using `(non-orig (ltk s b))`, `(non-orig (ltk s a))`, `(uniq-orig nb)`, `(uniq-orig na)`, and `(uniq-gen gk)`.
- **When to Reference This Example**: Reference this example when modeling IETF symmetric-key KDC protocols using `(ltk s a)` / `(ltk s b)` where outer message tags (`"req"`, `"resp"`, `"fetch"`, `"deliver"`) are in the clear outside `(enc ...)` and you need `defrule` role-separation constraints to prevent principal role confusion.
- **Key S-Expression Excerpt**:
```scheme
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
	     (false)))))
```

---

## fragile_pruning.scm

- **File Path**: `03_examples_scm/fragile_pruning.scm`
- **Algebra & Herald**: No `(herald ...)` form; uses `basic` algebra in `(defprotocol fragile_pruning basic ...)`.
- **Protocol & Purpose**: Illustrates why CPSA's strand pruning must be conservative even when multiple strands of the same role appear isomorphic up to renaming. An `init` strand sends `(enc n k)`, receives three encrypted pairs `(enc n n1 k)`, `(enc n n2 k)`, `(enc n n3 k)` from three separate `adder` strands, sends `(enc n n1 n2 n3 k)`, and receives `(enc n n1 n2 n3 n k)` from a `final` strand. If CPSA prematurely pruned two of the three `adder` strands as renamings of each other before `n1`, `n2`, and `n3` were kept distinct, it would fail to find the shape where `n1`, `n2`, `n3` remain distinct `uniq-orig` values.
- **Roles & Variables**:
  - `init`:
    - `(vars (k akey) (n n1 n2 n3 text))`
    - Role-level assumptions: `(uniq-orig n)`, `(non-orig (invk k))`
    - Trace: `(send (enc n k))`, `(recv (enc n n1 k))`, `(recv (enc n n2 k))`, `(recv (enc n n3 k))`, `(send (enc n n1 n2 n3 k))`, `(recv (enc n n1 n2 n3 n k))`
  - `adder`:
    - `(vars (k akey) (n new text))`
    - Role-level assumptions: `(uniq-orig new)`
    - Trace: `(recv (enc n k))`, `(send (enc n new k))`
  - `final`:
    - `(vars (k akey) (n n1 n2 n3 text))`
    - Trace: `(recv (enc n n1 n2 n3 k))`, `(send (enc n n1 n2 n3 n k))`
- **Skeletons, Goals, Rules & Macros**:
  - Single `(defskeleton fragile_pruning (vars (k akey) (n n1 n2 n3 text)) (defstrand init 6 (k k) (n n) (n1 n1) (n2 n2) (n3 n3)) (uniq-orig n1 n2 n3))`.
- **When to Reference This Example**: Reference this example when analyzing protocols where a single initiator aggregates multiple fresh tokens (`n1`, `n2`, `n3`) from multiple parallel responder (`adder`) instances and combines them in a single message (`(enc n n1 n2 n3 k)`).
- **Key S-Expression Excerpt**:
```scheme
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

## goals.scm

- **File Path**: `03_examples_scm/goals.scm`
- **Algebra & Herald**: `(herald goals)` — `basic` algebra across four protocol definitions (`ns`, `nsl`, `unilateral`, `nsl-typeless`).
- **Protocol & Purpose**: Comprehensive reference for CPSA's formal security goals (`defgoal` and skeleton-embedded `(goals ...)`), using standard role-specific predicates `(p "<role>" <strd> <height>)`, `(p "<role>" "<param>" <strd> <val>)`, listener predicates `(p "" <strd> 1)` and `(p "" "x" <strd> <val>)`, `(non ...)`, `(uniq ...)`, `(uniq-at ...)`, and `(prec ...)`. Covers:
  - Needham-Schroeder (`ns`): initiator authentication, precedence ordering, Lowe's responder authentication failure, initiator nonce secrecy, and predicate-mapped unilateral authentication goals.
  - Needham-Schroeder-Lowe (`nsl`): responder authentication success.
  - Unilateral authentication (`unilateral`): basic authentication goal.
  - Double initiator point-of-view skeleton (`(defskeleton ns ... (goals ...))`) concluding strand equality `(= z z-0)`.
  - Untyped Needham-Schroeder-Lowe (`nsl-typeless`): where `n2` in `init` and `n1` in `resp` have sort `mesg` instead of `text`, exposing a type-flaw secrecy failure on `n2`.
- **Roles & Variables**:
  - In `ns`: `init` (`(vars (a b name) (n1 n2 text))`), `resp` (`(vars (b a name) (n2 n1 text))`)
  - In `nsl`: `init` (`(vars (a b name) (n1 n2 text))`), `resp` (`(vars (b a name) (n2 n1 text))`) with `b` included in message 2 `(enc n1 n2 b (pubk a))`
  - In `unilateral`: `init` (`(vars (a name) (n text))`), `resp` (`(vars (a name) (n text))`)
  - In `nsl-typeless`: `init` (`(vars (a b name) (n1 text) (n2 mesg))`) with message 1 `(send (enc a n1 (pubk b)))`, `resp` (`(vars (b a name) (n2 text) (n1 mesg))`)
- **Skeletons, Goals, Rules & Macros**:
  - 12 `(defgoal ...)` declarations (including a multi-sentence `defgoal ns` containing two `forall` formulas) and 1 `(defskeleton ns ...)` containing an embedded `(goals (forall ...))` clause.
- **When to Reference This Example**: Reference this example as the primary template for writing `(defgoal <prot> (forall ...))` and skeleton-level `(goals (forall ...))` using the classic `(p "<role>" ...)` and listener `(p "" z1 1) (p "" "x" z1 n1)` predicate syntax, as well as modeling type-flaw attacks via sort `mesg` (`nsl-typeless`).
- **Key S-Expression Excerpt**:
```scheme
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
```

---

## goalsvar.scm

- **File Path**: `03_examples_scm/goalsvar.scm`
- **Algebra & Herald**: `(herald goalsvar)` — `basic` algebra across four protocol definitions (`ns`, `nsl`, `unilateral`, `nsl-typeless`).
- **Protocol & Purpose**: Exact counterpart to `goals.scm` demonstrating CPSA's concise `strand` and `listener` goal syntax (`(strand <role> <strd-var> <height> (<param> <val>) ...)` and `(listener <strd-var> <term>)`) in place of verbose `(p "<role>" ...)` and `(p "" ...)` predicates across all 12 `defgoal` declarations and the `defskeleton` `(goals ...)` block.
- **Roles & Variables**:
  - Identical to `goals.scm` across all 4 protocols (`ns`, `nsl`, `unilateral`, `nsl-typeless`):
    - `ns`: `init` (`(vars (a b name) (n1 n2 text))`), `resp` (`(vars (b a name) (n2 n1 text))`)
    - `nsl`: `init` (`(vars (a b name) (n1 n2 text))`), `resp` (`(vars (b a name) (n2 n1 text))`)
    - `unilateral`: `init` (`(vars (a name) (n text))`), `resp` (`(vars (a name) (n text))`)
    - `nsl-typeless`: `init` (`(vars (a b name) (n1 text) (n2 mesg))`), `resp` (`(vars (b a name) (n2 text) (n1 mesg))`)
- **Skeletons, Goals, Rules & Macros**:
  - 12 `(defgoal ...)` declarations and 1 `(defskeleton ns ... (goals ...))` block using `(strand ...)` and `(listener ...)` predicates.
- **When to Reference This Example**: Reference this example when writing readable `(defgoal ...)` or `(goals ...)` specifications using the compact `(strand <role> <z> <h> (<var> <val>) ...)` and `(listener <z> <term>)` syntax instead of `(p "<role>" ...)`.
- **Key S-Expression Excerpt**:
```scheme
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
  (forall ((a b name) (n1 text) (z0 z1 strd))
    (implies
     (and (strand init z0 3 (n1 n1) (a a) (b b))
      (listener z1 n1)
      (non (privk a)) (non (privk b)) (uniq n1))
     (false)))
  (comment "Initiator point of view")
  (comment "Secrecy goal: nonce n1 not revealed"))
```
````

---

### `refrences/cpsa_kb/04_examples_catalog/02_scm_examples_H_to_SDLS.md`

*sha256:`c54f6fc5d4ae` · 2664 lines · 187.0 KB (~47,818 tokens) · lang:`markdown`*

````markdown
# Official MITRE CPSA Examples Catalog (Part 2: hashtest-key-hash.scm to sdls-ep-challenge-authenc.scm)

This catalog documents files `50` through `99` (sorted alphabetically) from `03_examples_scm/`, covering `hashtest-key-hash.scm` through `sdls-ep-challenge-authenc.scm`. Every entry is extracted strictly from the actual `.scm` source file.

## hashtest-key-hash.scm

- **File Path**: `03_examples_scm/hashtest-key-hash.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Hashtest")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `hashtest`. Tests whether keyed hashing modeled via symmetric/asymmetric encryption `(enc "h" n)` using a nonce `n` of sort `data` as an encryption key works properly in CPSA's `basic` algebra. The initiator sends `(enc n k)` under asymmetric key `k` (with `(invk k)` non-originating and `n` uniquely originating) and expects `(enc "h" n)` in return from the responder.
- **Roles & Variables**:
  - Role `init`: Vars: `(n data)`, `(k akey)` | Role Assumptions: `(uniq-orig n)`, `(non-orig (invk k))` | Trace (2 events): `(send (enc n k))` -> `(recv (enc "h" n))`
  - Role `resp`: Vars: `(k akey)`, `(n data)` | Role Assumptions: none | Trace (2 events): `(recv (enc n k))` -> `(send (enc "h" n))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`hashtest`): `(vars)`, `(defstrand init 2)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when comparing ad-hoc hash modeling via `(enc "h" n)` (which allows anyone who learns `n` to both construct and invert/decrypt the term if `n` is a symmetric key or data term) against native `(hash n)` in the `basic` algebra.
- **Key S-Expression Excerpt** (lines 1–25):
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

## hashtest.scm

- **File Path**: `03_examples_scm/hashtest.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Hashtest")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `hashtest`. Tests CPSA's built-in one-way `(hash ...)` operator in the `basic` algebra. The initiator sends `(enc n k)` where `n` is fresh (`uniq-orig`) and `(invk k)` is uncompromised (`non-orig`), and receives `(hash n)` from the responder.
- **Roles & Variables**:
  - Role `init`: Vars: `(n data)`, `(k akey)` | Role Assumptions: `(uniq-orig n)`, `(non-orig (invk k))` | Trace (2 events): `(send (enc n k))` -> `(recv (hash n))`
  - Role `resp`: Vars: `(k akey)`, `(n data)` | Role Assumptions: none | Trace (2 events): `(recv (enc n k))` -> `(send (hash n))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`hashtest`): `(vars)`, `(defstrand init 2)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for the minimal canonical syntax of the built-in `(hash ...)` operator in CPSA's `basic` algebra and how CPSA derives authentication when a secret nonce `n` is returned inside a one-way hash.
- **Key S-Expression Excerpt** (lines 1–25):
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

## incompleteness_example.scm

- **File Path**: `03_examples_scm/incompleteness_example.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald incompleteness-example (comment "Shows a shape not found by CPSA"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `incompleteness-example`. Demonstrates an intentional incompleteness edge case in CPSA's search algorithm (`"Shows a shape not found by CPSA"`). In `incompleteness-example`, `init` sends `(enc n k)` and receives `n`, while `resp` receives `(enc n1 k)` and sends an independent variable `n2` without linking `n1` and `n2` in the role definition. The second skeleton explicitly exhibits a valid shape where `n1 = n` and `n2 = n` with causal ordering `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`, which CPSA does not discover from the first skeleton because `resp` does not originate or transform `n`.
- **Roles & Variables**:
  - Role `init`: Vars: `(k akey)`, `(n text)` | Role Assumptions: `(uniq-orig n)` | Trace (2 events): `(send (enc n k))` -> `(recv n)`
  - Role `resp`: Vars: `(k akey)`, `(n1 n2 text)` | Role Assumptions: none | Trace (2 events): `(recv (enc n1 k))` -> `(send n2)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`incompleteness-example`): `(vars (k akey))`, `(defstrand init 2 (k k))`, `(non-orig (invk k))` | Skeleton 2 (`incompleteness-example`): `(vars (k akey) (n text))`, `(defstrand init 2 (k k) (n n))`, `(defstrand resp 2 (k k) (n1 n) (n2 n))`, `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when debugging missing shapes or non-termination caused by roles whose `send` terms contain unconstrained variables (like `n2`) that are not bound to received variables (`n1`), violating CPSA's strand transformation expectations.
- **Key S-Expression Excerpt** (lines 1–21):
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

## isoreject-corrected.scm

- **File Path**: `03_examples_scm/isoreject-corrected.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald isoreject-corrected)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `isofix`. Models a corrected three-message challenge-response signature protocol (`isofix`, based on ISO/IEC 9798-3 mutual authentication) using explicit message-type tags `"first"` and `"second"` inside signatures `(enc "first" nb na a (privk b))` and `(enc "second" nc nb b (privk a))` to prevent reflection/type-confusion attacks between message 2 and message 3.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(na nb nc text)` | Role Assumptions: none | Trace (3 events): `(send (cat a na))` -> `(recv (enc "first" nb na a (privk b)))` -> `(send (enc "second" nc nb b (privk a)))`
  - Role `resp`: Vars: `(a b name)`, `(na nb nc text)` | Role Assumptions: `(uniq-orig nb)` | Trace (3 events): `(recv (cat a na))` -> `(send (enc "first" nb na a (privk b)))` -> `(recv (enc "second" nc nb b (privk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`isofix`): `(vars (a b name))`, `(defstrand resp 3 (a a) (b b))`, `(non-orig (privk a) (privk b))` | Skeleton 2 (`isofix`): `(vars (b name))`, `(defstrand init 3 (b b))`, `(non-orig (privk b))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when fixing reflection or message-confusion vulnerabilities in multi-message signed challenge-response protocols by adding distinct string literal tags (`"first"`, `"second"`) inside `(enc ... (privk ...))`.
- **Key S-Expression Excerpt** (lines 1–24):
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

## isoreject.scm

- **File Path**: `03_examples_scm/isoreject.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `isoreject`. Models the untagged three-message ISO challenge-response signature protocol (`isoreject`) without string tags in the signed messages `(enc nb na a (privk b))` and `(enc nc nb b (privk a))`. Because the two signed messages have identical term structure `(enc <text> <text> <name> (privk <name>))`, a responder's first signature can be reflected or confused with an initiator's second signature.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(na nb nc text)` | Role Assumptions: none | Trace (3 events): `(send (cat a na))` -> `(recv (enc nb na a (privk b)))` -> `(send (enc nc nb b (privk a)))`
  - Role `resp`: Vars: `(a b name)`, `(na nb nc text)` | Role Assumptions: `(uniq-orig nb)` | Trace (3 events): `(recv (cat a na))` -> `(send (enc nb na a (privk b)))` -> `(recv (enc nc nb b (privk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`isoreject`): `(vars (a b name))`, `(defstrand resp 3 (a a) (b b))`, `(non-orig (privk a) (privk b))` | Skeleton 2 (`isoreject`): `(vars (b name))`, `(defstrand init 3 (b b))`, `(non-orig (privk b))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example alongside `isoreject-corrected.scm` to see how structurally identical signed messages in challenge-response protocols enable reflection attacks when domain-separation tags are omitted.
- **Key S-Expression Excerpt** (lines 1–22):
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

## kelly1.scm

- **File Path**: `03_examples_scm/kelly1.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `kelly1`. Models a three-party remote attestation protocol (`kelly1`) involving a `client`, an `appraiser`, and a `server`. The client requests content from the server (receiving `(enc (cat response Ns) (privk S))`), and asks a trusted appraiser `A` (`(non-orig (privk A))`) to verify the server's public key `(pubk S)` and nonce `Ns`. The appraiser challenges the server with fresh nonce `N`, receives a TPM-style quote signed by `(privk AIK)` binding `(cat Quote measurements N Ns (pubk S))`, and issues a signed policy decision `(enc (cat policy (pubk S) Ns) (privk A))` to the client.
- **Roles & Variables**:
  - Role `client`: Vars: `(C name)`, `(A name)`, `(S name)`, `(Ns text)`, `(request text)`, `(Check text)`, `(policy text)`, `(response text)` | Role Assumptions: none | Trace (4 events): `(send (cat C S request))` -> `(recv (cat S C (enc (cat response Ns) (privk S))))` -> `(send (cat C A Check (pubk S)))` -> `(recv (cat A C (enc (cat policy (pubk S) Ns) (privk A))))`
  - Role `appraiser`: Vars: `(C name)`, `(A name)`, `(S name)`, `(N text)`, `(Ns text)`, `(hello text)`, `(Quote text)`, `(measurements text)`, `(Check text)`, `(policy text)`, `(AIK name)` | Role Assumptions: `(non-orig (privk A) (privk AIK))`, `(uniq-orig N)` | Trace (5 events): `(recv (cat S A hello))` -> `(send (cat A S N))` -> `(recv (cat S A (enc (cat Quote measurements N Ns (pubk S)) (privk AIK)) (pubk S)))` -> `(recv (cat C A Check (pubk S)))` -> `(send (cat A C (enc (cat policy (pubk S) Ns) (privk A))))`
  - Role `server`: Vars: `(C name)`, `(A name)`, `(S name)`, `(N text)`, `(Ns text)`, `(hello text)`, `(Quote text)`, `(measurements text)`, `(request text)`, `(response text)`, `(AIK name)` | Role Assumptions: `(non-orig (privk S) (privk AIK))`, `(uniq-orig Ns)` | Trace (5 events): `(send (cat S A hello))` -> `(recv (cat A S N))` -> `(send (cat S A (enc (cat Quote measurements N Ns (pubk S)) (privk AIK)) (pubk S)))` -> `(recv (cat C S request))` -> `(send (cat S C (enc (cat response Ns) (privk S))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`kelly1`): `(vars (A name))`, `(defstrand client 4 (A A))`, `(non-orig (privk A))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling remote attestation, RATS (RFC 9334), or TPM quote verification protocols where an appraiser/verifier mediates trust between a relying party (client) and an attester (server) using an Attestation Identity Key (`AIK`).
- **Key S-Expression Excerpt** (lines 16–76):
```scheme

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

## kerberos.scm

- **File Path**: `03_examples_scm/kerberos.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `kerberos`. Models a simplified three-party Kerberos authentication exchange (`kerberos`) among `init` (client `a`), `resp` (service `b`), and `keyserver` (`ks`) using shared long-term keys `(ltk a ks)` and `(ltk b ks)`. As noted in the file's comments, because the keyserver's response `(cat (enc (cat t l k b) (ltk a ks)) (enc (cat t l k a) (ltk b ks)))` is symmetric in `a` and `b`, CPSA finds two shapes corresponding to reversing `a` and `b`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a name)`, `(b name)`, `(ks name)`, `(t text)`, `(t-prime text)`, `(l text)`, `(k skey)` | Role Assumptions: none | Trace (4 events): `(send (cat a b))` -> `(recv (cat (enc (cat t l k b) (ltk a ks)) (enc (cat t l k a) (ltk b ks))))` -> `(send (cat (enc (cat a t) k) (enc (cat t l k a) (ltk b ks))))` -> `(recv (enc t-prime k))`
  - Role `resp`: Vars: `(a name)`, `(b name)`, `(ks name)`, `(t text)`, `(t-prime text)`, `(l text)`, `(k skey)` | Role Assumptions: none | Trace (2 events): `(recv (cat (enc (cat a t) k) (enc (cat t l k a) (ltk b ks))))` -> `(send (enc t-prime k))`
  - Role `keyserver`: Vars: `(a name)`, `(b name)`, `(ks name)`, `(t text)`, `(l text)`, `(k skey)` | Role Assumptions: `(uniq-orig k)` | Trace (2 events): `(recv (cat a b))` -> `(send (cat (enc (cat t l k b) (ltk a ks)) (enc (cat t l k a) (ltk b ks))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`kerberos`): `(vars (a name) (b name) (ks name))`, `(defstrand init 4 (a a) (b b) (ks ks))`, `(non-orig (ltk a ks) (ltk b ks))` | Skeleton 2 (`kerberos`): `(vars (a name) (b name) (ks name))`, `(defstrand resp 2 (a a) (b b) (ks ks))`, `(non-orig (ltk a ks) (ltk b ks))` | Skeleton 3 (`kerberos`): `(vars (a name) (b name) (ks name))`, `(defstrand keyserver 2 (a a) (b b) (ks ks))`, `(non-orig (ltk a ks) (ltk b ks))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling Kerberos or KDC-based symmetric ticket distribution protocols using `(ltk a ks)` and understanding why symmetric ticket structures produce multiple shapes unless directional tags distinguish client and server tickets.
- **Key S-Expression Excerpt** (lines 1–37):
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

## lemmas.scm

- **File Path**: `03_examples_scm/lemmas.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald goalsvar)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. Demonstrates CPSA's `(deflemma ...)` and `(defgoal ...)` security goal declarations on the Needham-Schroeder Public-Key protocol (`ns`, from Section 10 of the CPSA Primer). Illustrates the three `deflemma` modes: `(deflemma rule lemma1 ns ...)` (used only as a rewrite rule), `(deflemma both lemma2 ns ...)` (both proved as a goal and used as a rule), and `(deflemma goal lemma3 ns ...)` (proved as a goal only), alongside `(defgoal ns ...)` using role-variable predicate syntax `(strand init z0 3 (n1 n1) (b b))`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 text)` | Role Assumptions: none | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc n1 n2 (pubk a)))` -> `(send (enc n2 (pubk b)))`
  - Role `resp`: Vars: `(b a name)`, `(n2 n1 text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 (pubk a)))` -> `(recv (enc n2 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Lemmas (3)**: `(deflemma rule lemma1 ns (forall ((b name) (n1 text) (z0 strd)) (implies (and (strand init z0 3 (n1 n1) (b b)) (non (privk b)) (uniq n1)) (exists ((z1 strd)) (strand resp z1 2 (b b))))) (comment "Skeleton 1") (comment "Authentication goal: agreement on name b"))`; `(deflemma both lemma2 ns (forall ((b name) (n1 text) (z0 strd)) (implies (and (strand init z0 3 (n1 n1) (b b)) (non (privk b)) (uniq n1)) (exists ((z1 strd)) (and (strand resp z1 2 (b b)) (prec z1 1 z0 2))))) (comment "Prec example. Skeleton 2"))`; `(deflemma goal lemma3 ns (forall ((a b name) (n2 text) (z0 strd)) (implies (and (strand resp z0 3 (n2 n2) (a a) (b b)) (non (privk a)) (uniq n2)) (exists ((z1 strd)) (strand init z1 2 (b b))))) (comment "Skeleton 3") (comment "Failed authentication goal: agreement on name b"))`
  - **Goals (1)**: `(defgoal ns (forall ((a b name) (n2 text) (z0 strd)) (implies (and (strand resp z0 3 (n2 n2) (a a) (b b)) (non (privk a)) (uniq n2)) (exists ((z1 strd)) (strand init z1 2 (b b))))) (comment "Skeleton 4"))`
  - **Skeletons**: None active (note: `;`-commented `defskeleton` blocks appear at the bottom of `scep-tls-dh-broken.scm`)
  - **Keywords & Predicates Used**: `and`, `defgoal`, `deflemma`, `defprotocol`, `defrole`, `exists`, `forall`, `herald`, `implies`, `non`, `prec`, `recv`, `send`, `strand`, `trace`, `uniq`, `vars`
- **When to Reference This Example**: Reference this example when writing `(deflemma <mode> <name> <prot> ...)` or `(defgoal <prot> ...)` formulas using the high-level `(strand <role> <strd> <height> (<var> <val>)...)`, `(non ...)`, `(uniq ...)`, and `(prec ...)` predicates.
- **Key S-Expression Excerpt** (lines 22–61):
```scheme
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

## locn_envelope.scm

- **File Path**: `03_examples_scm/locn_envelope.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Envelope Protocol, location-based version" (bound 30) (limit 1200))` | Flags: `(bound 30)`, `(limit 1200)`
- **Protocol & Purpose**: Protocol(s): `envelope`, `envelope-plus`, `envelope-plus-2`. Comprehensive model of the TPM Envelope Protocol using stateful locations (`locn`), channels (`chan` with `auth` and `conf`), macros (`defmacro`), and state-generation/ordering rules (`defrule` with `gen-st`). Defines three protocol variants (`envelope`, `envelope-plus`, `envelope-plus-2`) to test three scenarios: listening for the secret `v`, listening for the refusal token `(refuse pcr-id n v k aik)`, and listening for both simultaneously (which should be impossible once PCR state splitting and multi-TPM ambiguity are ruled out by `ordered-extends` and `pcr-id-identifies-pcr`).
- **Roles & Variables**:
  - *(Roles are defined via `(defmacro (roles) (^ ...))` and expanded into `envelope`, `envelope-plus`, and `envelope-plus-2`)*:
  - Role `tpm-power-on`: Vars: `(current-value mesg)`, `(pcr locn)`, `(tpm chan)` | Role Assumptions: none | Trace (3 events): `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc`: Vars: `(value current-value mesg)`, `(pcr-id text)`, `(pcr locn)`, `(tpm chan)` | Role Assumptions: none | Trace (4 events): `(recv tpm (cat "extend" pcr-id value))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote`: Vars: `(nonce current-value mesg)`, `(pcr-id text)`, `(aik akey)`, `(pcr locn)`, `(tpm chan)` | Role Assumptions: none | Trace (3 events): `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key`: Vars: `(k aik akey)`, `(pcr-id text)`, `(pcrval mesg)`, `(tpm chan)` | Role Assumptions: `(uniq-orig k)`, `(non-orig (invk k))`, `(auth tpm)` | Trace (2 events): `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt`: Vars: `(m current-value mesg)`, `(pcr-id text)`, `(k aik akey)`, `(pcr locn)`, `(tpm chan)` | Role Assumptions: `(non-orig aik)` | Trace (4 events): `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice`: Vars: `(n v data)`, `(pcr-id text)`, `(k aik akey)`, `(tpm chan)` | Role Assumptions: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpm)` | Trace (4 events): `(send tpm (cat "extend" pcr-id n))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (3)**: `(refuse pcr-id n v k aik)`, `(roles)`, `(genStV-rules)`
  - **Rules (6)**: `genStV-if-hashed-tpm-power-on`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`; `genStV-if-hashed-tpm-extend-enc`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`; `genStV-if-hashed-tpm-decrypt`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`; `genStV-if-hashed-tpm-quote`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`; `ordered-extends`: `(forall ((y z strd) (pcr locn)) (implies (and (p "tpm-extend-enc" y 3) (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "pcr" y pcr) (p "tpm-extend-enc" "pcr" z pcr)) (or (= y z) (prec y 2 z 1) (prec z 2 y 1))))`; `pcr-id-identifies-pcr`: `(forall ((y z strd) (pcr-id text) (pcr pcr-0 locn)) (implies (and (p "tpm-extend-enc" y 3) (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "pcr-id" y pcr-id) (p "tpm-extend-enc" "pcr-id" z pcr-id) (p "tpm-extend-enc" "pcr" y pcr) (p "tpm-extend-enc" "pcr" z pcr-0)) (= pcr pcr-0)))`
  - **Goals**: None
  - **Skeletons (9)**: Skeleton 1 (`envelope`): `(vars (v data))`, `(deflistener v)`, `(defstrand alice 4 (v v))` | Skeleton 2 (`envelope`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 3 (`envelope`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(deflistener v)`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 4 (`envelope-plus`): `(vars (v data))`, `(deflistener v)`, `(defstrand alice 4 (v v))` | Skeleton 5 (`envelope-plus`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 6 (`envelope-plus`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(deflistener v)`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 7 (`envelope-plus-2`): `(vars (v data))`, `(deflistener v)`, `(defstrand alice 4 (v v))` | Skeleton 8 (`envelope-plus-2`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))` | Skeleton 9 (`envelope-plus-2`): `(vars (n v data) (k aik akey) (pcr-id text))`, `(deflistener (refuse pcr-id n v k aik))`, `(deflistener v)`, `(defstrand alice 4 (n n) (v v) (k k) (aik aik))`
  - **Keywords & Predicates Used**: `and`, `auth`, `bound`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `forall`, `gen-st`, `herald`, `implies`, `limit`, `load`, `neq`, `non-orig`, `or`, `p`, `prec`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling stateful hardware security modules or TPM PCR `load`/`stor` transitions over authenticated/confidential channels, or when writing `gen-st` and location-equality rules (`defrule`) to prevent state splitting.
- **Key S-Expression Excerpt** (lines 89–124):
```scheme
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
```

## missing_contraction.scm

- **File Path**: `03_examples_scm/missing_contraction.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `missing-contraction`. Regression and diagnostic test case (`missing-contraction`) illustrating a subtlety in CPSA's cohort generation where solving a test node requires displacement/augmentation rather than ordinary contraction because `(enc a n (pubk b))` is not in the escape set of `(enc a m (pubk a))`.
- **Roles & Variables**:
  - Role `sender`: Vars: `(m n text)`, `(a b name)` | Role Assumptions: none | Trace (2 events): `(send (enc a m (pubk a)))` -> `(send (enc a n (pubk b)))`
  - Role `receiver`: Vars: `(m text)`, `(a b name)` | Role Assumptions: none | Trace (1 events): `(recv (enc a m (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`missing-contraction`): `(vars (m text) (a c name))`, `(defstrand sender 2 (m m) (a a))`, `(defstrand receiver 1 (m m) (a a) (b c))`, `(precedes ((0 1) (1 0)))`, `(uniq-orig m)`, `(non-orig (privk a))` | Skeleton 2 (`missing-contraction`): `(vars (m text) (a c name))`, `(defstrand sender 1 (m m) (a a))`, `(deflistener (enc a m (pubk c)))`, `(uniq-orig m)`, `(non-orig (privk a))` | Skeleton 3 (`missing-contraction`): `(vars (m text) (a b c name))`, `(defstrand sender 2 (m m) (a a) (b b))`, `(defstrand receiver 1 (m m) (a a) (b c))`, `(precedes ((0 1) (1 0)))`, `(uniq-orig m)`, `(non-orig (privk a) (privk b))`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example to understand how CPSA handles multiple encrypted transmissions from the same strand when a nonce `m` originates in one encryption `(enc a m (pubk a))` and is expected in another `(enc a m (pubk b))`.
- **Key S-Expression Excerpt** (lines 21–54):
```scheme

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

## neq_test.scm

- **File Path**: `03_examples_scm/neq_test.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Inequality constraint using facts and rules" (comment "First skeleton should have a shape," "second should be dead."))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `neq-test`. Demonstrates how to enforce an inequality constraint (`n1 != n2`) in CPSA using a custom `(facts (neq n1 n2))` declaration in `defskeleton` paired with a protocol rule `(defrule neq (forall ((a mesg)) (implies (fact neq a a) (false))))`. In the first skeleton (without the inequality fact), CPSA finds a shape by unifying `n1 = n2`; in the second skeleton (with `(facts (neq n1 n2))`), the unification `n1 = n2` triggers `(fact neq a a) -> (false)` and kills the branch, yielding a dead skeleton (no shapes).
- **Roles & Variables**:
  - Role `init`: Vars: `(n1 n2 text)`, `(k skey)` | Role Assumptions: `(non-orig k)`, `(uniq-orig n1 n2)` | Trace (2 events): `(send (cat n1 (enc n1 n2 k)))` -> `(recv n2)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `neq`: `(forall ((a mesg)) (implies (fact neq a a) (false)))`
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`neq-test`): `(vars)`, `(defstrand init 2)` | Skeleton 2 (`neq-test`): `(vars (n1 n2 text))`, `(defstrand init 2 (n1 n1) (n2 n2))`, `(facts (neq n1 n2))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `false`, `forall`, `herald`, `implies`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example whenever you need to assert that two terms or variables are distinct (`x != y`) in a CPSA skeleton using `(facts (neq x y))` and the standard `neq` falsification rule.
- **Key S-Expression Excerpt** (lines 1–30):
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

## neuman-stubblebine.scm

- **File Path**: `03_examples_scm/neuman-stubblebine.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `neuman-stubblebine`. Models the initial exchange of the Neuman-Stubblebine authentication and key distribution protocol (`neuman-stubblebine`) with three roles (`init`, `resp`, `keyserver`) using symmetric long-term keys `(ltk a ks)` and `(ltk b ks)` and fresh session key `k`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b ks name)`, `(ra rb text)`, `(k skey)`, `(tb text)` | Role Assumptions: none | Trace (3 events): `(send (cat a ra))` -> `(recv (cat (enc b ra k tb (ltk a ks)) (enc a k tb (ltk b ks)) rb))` -> `(send (cat (enc a k tb (ltk b ks)) (enc rb k)))`
  - Role `resp`: Vars: `(a b ks name)`, `(ra rb text)`, `(k skey)`, `(tb text)` | Role Assumptions: none | Trace (3 events): `(recv (cat a ra))` -> `(send (cat b rb (enc a ra tb (ltk b ks))))` -> `(recv (cat (enc a k tb (ltk b ks)) (enc rb k)))`
  - Role `keyserver`: Vars: `(a b ks name)`, `(ra rb text)`, `(k skey)`, `(tb text)` | Role Assumptions: `(uniq-orig k)` | Trace (2 events): `(recv (cat b rb (enc a ra tb (ltk b ks))))` -> `(send (cat (enc b ra k tb (ltk a ks)) (enc a k tb (ltk b ks)) rb))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`neuman-stubblebine`): `(vars (a b ks name) (ra rb text))`, `(defstrand init 3 (a a) (b b) (ks ks) (ra ra) (rb rb))`, `(uniq-orig ra rb)`, `(non-orig (ltk a ks) (ltk b ks))` | Skeleton 2 (`neuman-stubblebine`): `(vars (a b ks name) (ra rb text))`, `(defstrand resp 3 (a a) (b b) (ks ks) (ra ra) (rb rb))`, `(uniq-orig ra rb)`, `(non-orig (ltk a ks) (ltk b ks))` | Skeleton 3 (`neuman-stubblebine`): `(vars (a b ks name) (ra rb text))`, `(defstrand keyserver 2 (a a) (b b) (ks ks) (ra ra) (rb rb))`, `(uniq-orig ra rb)`, `(non-orig (ltk a ks) (ltk b ks))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling three-party symmetric key distribution protocols with timestamps/lifetimes (`tb`) and dual nonces (`ra`, `rb`) where the responder forwards the initiator's challenge to the key server.
- **Key S-Expression Excerpt** (lines 1–37):
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

## no_contraction.scm

- **File Path**: `03_examples_scm/no_contraction.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `no-contraction`. Minimal test case (`no-contraction`) where `init` sends a nested signed-then-encrypted term `(enc (enc n (privk a)) (pubk b))` without `b`'s private key being non-originating, while `resp` receives the inner signed term `(enc n (privk a))`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n text)` | Role Assumptions: none | Trace (1 events): `(send (enc (enc n (privk a)) (pubk b)))`
  - Role `resp`: Vars: `(a name)`, `(n text)` | Role Assumptions: none | Trace (1 events): `(recv (enc n (privk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`no-contraction`): `(vars (a b name) (n m text))`, `(defstrand resp 1 (a a) (n n))`, `(defstrand init 1 (n n))`, `(uniq-orig n)`, `(non-orig (privk a))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example as a minimal template for nested sign-then-encrypt (`(enc (enc n (privk a)) (pubk b))`) where the outer encryption key `(pubk b)` is unconstrained so the penetrator can strip the outer layer.
- **Key S-Expression Excerpt** (lines 1–16):
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

## non_transforming.scm

- **File Path**: `03_examples_scm/non_transforming.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `non_transforming`. Regression test (`non_transforming`) illustrating a corner case in CPSA's augmentation step: augmenting a skeleton containing `recv` and two `sender` strands with `(breaker 3)` causes unification (`a = b`) such that the 3rd node of `breaker` sends the exact same term `(enc a (pubk B))` as the 2nd node and is therefore no longer a transforming node.
- **Roles & Variables**:
  - Role `sender`: Vars: `(a b text)`, `(B name)` | Role Assumptions: `(uniq-orig a b)`, `(non-orig (privk B))` | Trace (1 events): `(send (enc a b (pubk B)))`
  - Role `recv`: Vars: `(a b text)`, `(B name)` | Role Assumptions: none | Trace (2 events): `(recv (enc a (pubk B)))` -> `(recv (enc b (pubk B)))`
  - Role `breaker`: Vars: `(a b text)`, `(B name)` | Role Assumptions: none | Trace (3 events): `(recv (enc a b (pubk B)))` -> `(send (enc a (pubk B)))` -> `(send (enc b (pubk B)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`non_transforming`): `(vars (a b c d text) (B B0 B1 name))`, `(defstrand recv 2 (a a) (b b) (B B))`, `(defstrand sender 1 (a a) (b d) (B B0))`, `(defstrand sender 1 (a c) (b b) (B B1))`, `(precedes ((1 0) (0 0)) ((2 0) (0 1)))`, `(uniq-orig a b)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when studying how CPSA's augmentation and unification interact when a helper/breaker role decomposes a pair `(enc a b (pubk B))` into separate components `(enc a (pubk B))` and `(enc b (pubk B))`.
- **Key S-Expression Excerpt** (lines 9–42):
```scheme
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

## nonaug-prune.scm

- **File Path**: `03_examples_scm/nonaug-prune.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `nonaug-prune`. Regression test (`nonaug-prune`) demonstrating that CPSA can prune two existing strands (`trans2`) of a parent skeleton after augmenting with a new strand when variable unifications (`A = B`) make one strand redundant.
- **Roles & Variables**:
  - Role `orig`: Vars: `(n text)`, `(A B name)`, `(k akey)` | Role Assumptions: `(uniq-orig n)`, `(non-orig (invk k))` | Trace (3 events): `(send (enc n B B k))` -> `(send (enc n A k))` -> `(recv (enc n A A A k))`
  - Role `trans1`: Vars: `(n text)`, `(A C name)`, `(k akey)` | Role Assumptions: none | Trace (3 events): `(recv (enc n A A k))` -> `(recv (enc n A k))` -> `(send (enc n n C k))`
  - Role `trans2`: Vars: `(n text)`, `(A name)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc n A k))` -> `(send (enc n A A A k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`nonaug-prune`): `(vars (n text) (A B name) (k akey))`, `(defstrand trans2 2 (n n) (A B) (k k))`, `(defstrand trans2 2 (n n) (A A) (k k))`, `(defstrand orig 3 (n n) (A A) (B B) (k k))`, `(precedes ((2 0) (0 0)) ((2 0) (1 0)))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when analyzing strand pruning and generalization behavior in preskeletons with multiple instances of the same role (`trans2`) bound to different role parameters.
- **Key S-Expression Excerpt** (lines 5–42):
```scheme
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

## ns-l.scm

- **File Path**: `03_examples_scm/ns-l.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Needham-Schroeder-Low Public-Key Protocol" (comment "With deflistener's"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. Models the Needham-Schroeder-Lowe Public-Key Protocol (`ns`, with Lowe's fix including responder identity `b` in message 2: `(enc b n1 n2 (pubk a))`) and includes `(deflistener n1)` and `(deflistener n2)` in the initiator and responder skeletons to verify nonce secrecy alongside authentication.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 text)` | Role Assumptions: none | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc b n1 n2 (pubk a)))` -> `(send (enc n2 (pubk b)))`
  - Role `resp`: Vars: `(b a name)`, `(n2 n1 text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc b n1 n2 (pubk a)))` -> `(recv (enc n2 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(deflistener n1)`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 2 (`ns`): `(vars (a name) (n2 text))`, `(defstrand resp 3 (a a) (n2 n2))`, `(deflistener n2)`, `(non-orig (privk a))`, `(uniq-orig n2)`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for the canonical Needham-Schroeder-Lowe public-key protocol model and the standard pattern for testing nonce confidentiality using `(deflistener <nonce>)` inside `(defskeleton ...)`.
- **Key S-Expression Excerpt** (lines 1–38):
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

## ns-rebinding.scm

- **File Path**: `03_examples_scm/ns-rebinding.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "ALternate Needham-Schroeder Public-Key Protocol Variants")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. Tests variable rebinding and existential quantification in the conclusion of a rule (`rebind-x`: `(forall ((x y text)) (implies (fact rel1 x y) (exists ((x name)) (fact rel2 x y))))`, where `x` is rebound from sort `text` to sort `name`), alongside role-level `(facts (rel1 n1 n2) (rel2 n1 n2))` and double-initiator skeletons on the Needham-Schroeder-Lowe protocol.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 text)` | Role Assumptions: `(facts (rel1 n1 n2) (rel2 n1 n2))` | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc n1 n2 b (pubk a)))` -> `(send (enc n2 (pubk b)))`
  - Role `resp`: Vars: `(b a name)`, `(n2 n1 text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 b (pubk a)))` -> `(recv (enc n2 (pubk b)))`
  - *(Commented-out role)*: Top-level `(comment (defrole keyserver ...))` also illustrates a `guar` event `(guar (and (long-term-key ks a kas) (long-term-key ks b kbs)))`.
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `rebind-x`: `(forall ((x y text)) (implies (fact rel1 x y) (exists ((x name)) (fact rel2 x y))))`
  - **Goals**: None
  - **Skeletons (8)**: Skeleton 1 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 2 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)`, `(facts (rel n1 n1))` | Skeleton 3 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b))`, `(uniq-orig n1)` | Skeleton 4 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(deflistener n1)`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 5 (`ns`): `(vars (a b name) (n1 n1-0 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(defstrand init 3 (a a) (b b) (n1 n1-0))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1 n1-0)` | Skeleton 6 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 7 (`ns`): `(vars (a name) (n2 text))`, `(defstrand resp 3 (a a) (n2 n2))`, `(non-orig (privk a))`, `(uniq-orig n2)` | Skeleton 8 (`ns`): `(vars (x name) (n1 n2 text) (a b name))`, `(defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))`, `(non-orig (privk a) (privk b))`, `(uniq-orig n1)`, `(facts (rel2 x n2) (rel1 n1 n2) (rel2 n1 n2))`
  - **Keywords & Predicates Used**: `comment`, `deflistener`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `exists`, `fact`, `facts`, `forall`, `herald`, `implies`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when attaching custom `(facts ...)` directly inside a `(defrole ...)` definition or when testing variable shadowing/rebinding in `(defrule ...)` existential conclusions.
- **Key S-Expression Excerpt** (lines 15–47):
```scheme
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

```

## ns.scm

- **File Path**: `03_examples_scm/ns.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Needham-Schroeder Public-Key Protocol" (comment "This protocol contains a man-in-the-middle" "attack discovered by Gavin Lowe."))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. The classic original Needham-Schroeder Public-Key Protocol (`ns`) from the CPSA Primer, where message 2 is `(enc n1 n2 (pubk a))` (omitting `b`'s identity), which exhibits Gavin Lowe's famous man-in-the-middle attack when analyzed from the responder's point of view.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 text)` | Role Assumptions: none | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc n1 n2 (pubk a)))` -> `(send (enc n2 (pubk b)))`
  - Role `resp`: Vars: `(b a name)`, `(n2 n1 text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 (pubk a)))` -> `(recv (enc n2 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`ns`): `(vars (a b name) (n1 text))`, `(defstrand init 3 (a a) (b b) (n1 n1))`, `(non-orig (privk b) (privk a))`, `(uniq-orig n1)` | Skeleton 2 (`ns`): `(vars (a name) (n2 text))`, `(defstrand resp 3 (a a) (n2 n2))`, `(non-orig (privk a))`, `(uniq-orig n2)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example as the canonical baseline for public-key challenge-response modeling in CPSA and to see why responder point-of-view analysis fails when the responder's identity `b` is omitted from `(enc n1 n2 (pubk a))`.
- **Key S-Expression Excerpt** (lines 1–37):
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

## nsl3.scm

- **File Path**: `03_examples_scm/nsl3.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Three Party Needham-Schroeder-Lowe Protocol")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `nsl3`. Models a Three-Party Needham-Schroeder-Lowe Protocol (`nsl3`) with roles `init` (`a`), `mid` (`b`), and `resp` (`c`), where each participant originates two fresh nonces (`na0 na1`, `nb0 nb1`, `nc0 nc1`) and forwards nested public-key encrypted tickets to establish mutual authentication across all three parties.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b c name)`, `(na0 na1 nb0 nb1 nc0 nc1 text)` | Role Assumptions: `(uniq-orig na0 na1)` | Trace (3 events): `(send (enc na0 a c (enc na1 a b (pubk c)) (pubk b)))` -> `(recv (enc na1 nc1 c b (enc na0 nb0 b c (pubk a)) (enc nb1 nc0 c a (pubk b)) (pubk a)))` -> `(send (enc nb0 (enc nb1 nc0 c a (pubk b)) (enc nc1 (pubk c)) (pubk b)))`
  - Role `mid`: Vars: `(a b c name)`, `(na0 na1 nb0 nb1 nc0 nc1 text)` | Role Assumptions: `(uniq-orig nb0 nb1)` | Trace (4 events): `(recv (enc na0 a c (enc na1 a b (pubk c)) (pubk b)))` -> `(send (enc nb1 b a (enc na1 a b (pubk c)) (enc na0 nb0 b c (pubk a)) (pubk c)))` -> `(recv (enc nb0 (enc nb1 nc0 c a (pubk b)) (enc nc1 (pubk c)) (pubk b)))` -> `(send (enc nc0 (enc nc1 (pubk c)) (pubk c)))`
  - Role `resp`: Vars: `(a b c name)`, `(na0 na1 nb0 nb1 nc0 nc1 text)` | Role Assumptions: `(uniq-orig nc0 nc1)` | Trace (3 events): `(recv (enc nb1 b a (enc na1 a b (pubk c)) (enc na0 nb0 b c (pubk a)) (pubk c)))` -> `(send (enc na1 nc1 c b (enc na0 nb0 b c (pubk a)) (enc nb1 nc0 c a (pubk b)) (pubk a)))` -> `(recv (enc nc0 (enc nc1 (pubk c)) (pubk c)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`nsl3`): `(vars (a b c name))`, `(defstrand init 3 (a a) (b b) (c c))`, `(non-orig (privk a) (privk b) (privk c))` | Skeleton 2 (`nsl3`): `(vars (a b c name))`, `(defstrand mid 4 (a a) (b b) (c c))`, `(non-orig (privk a) (privk b) (privk c))` | Skeleton 3 (`nsl3`): `(vars (a b c name))`, `(defstrand resp 3 (a a) (b b) (c c))`, `(non-orig (privk a) (privk b) (privk c))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling multi-party (3+ participant) public-key authentication protocols with nested encrypted forwarding tickets (`(enc ... (enc ... (pubk c)) (pubk b))`).
- **Key S-Expression Excerpt** (lines 1–41):
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

```

## nslsk.scm

- **File Path**: `03_examples_scm/nslsk.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Needham-Schroeder-Lowe Protocol with symmetric encryption")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `nslsk`, `nslsk-tag-term`. Models the Needham-Schroeder-Lowe protocol used to distribute a fresh symmetric session key `(k skey)` (`nslsk`) followed by a confirmation message `(enc t k)`, along with a second protocol variant (`nslsk-tag-term`) where the confirmation payload is a constant string literal tag `(enc "t" k)`.
- **Roles & Variables**:
  - Role `init` (in `nslsk`): Vars: `(a b name)`, `(n text)`, `(k skey)`, `(t text)` | Role Assumptions: none | Trace (3 events): `(send (enc n a (pubk b)))` -> `(recv (enc n k b (pubk a)))` -> `(send (enc t k))`
  - Role `resp` (in `nslsk`): Vars: `(b a name)`, `(n text)`, `(k skey)`, `(t text)` | Role Assumptions: none | Trace (3 events): `(recv (enc n a (pubk b)))` -> `(send (enc n k b (pubk a)))` -> `(recv (enc t k))`
  - Role `init` (in `nslsk-tag-term`): Vars: `(a b name)`, `(n text)`, `(k skey)` | Role Assumptions: none | Trace (3 events): `(send (enc n a (pubk b)))` -> `(recv (enc n k b (pubk a)))` -> `(send (enc "t" k))`
  - Role `resp` (in `nslsk-tag-term`): Vars: `(b a name)`, `(n text)`, `(k skey)` | Role Assumptions: none | Trace (3 events): `(recv (enc n a (pubk b)))` -> `(send (enc n k b (pubk a)))` -> `(recv (enc "t" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (4)**: Skeleton 1 (`nslsk`): `(vars (a name) (k skey))`, `(defstrand resp 3 (a a) (k k))`, `(non-orig (privk a))`, `(uniq-orig k)` | Skeleton 2 (`nslsk`): `(vars (b name) (n text))`, `(defstrand init 3 (b b) (n n))`, `(non-orig (privk b))`, `(uniq-orig n)` | Skeleton 3 (`nslsk-tag-term`): `(vars (a name) (k skey))`, `(defstrand resp 3 (a a) (k k))`, `(non-orig (privk a))`, `(uniq-orig k)` | Skeleton 4 (`nslsk-tag-term`): `(vars (b name) (n text))`, `(defstrand init 3 (b b) (n n))`, `(non-orig (privk b))`, `(uniq-orig n)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling hybrid public-key / symmetric-key handshakes (where an asymmetric exchange establishes a symmetric `skey` `k` used to encrypt subsequent traffic or a constant confirmation tag `"t"`).
- **Key S-Expression Excerpt** (lines 1–40):
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

```

## open-closed-multiloc.scm

- **File Path**: `03_examples_scm/open-closed-multiloc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald open-closed (bound 44))` | Flags: `(bound 44)` (commented-out flags in source: `(try-old-strands)`, `(check-nonces)`, `(reverse-nodes)`)
- **Protocol & Purpose**: Protocol(s): `open-closed`. Models a stateful device access-control protocol (`open-closed`) using two distinct state locations (`lk` for key state and `ls` for open/closed status), an authenticated/confidential power-up channel (`start-ch` of sort `chan`), macros (`defmacro`) encoding state terms (`(opened o)` as `(cat o o)`, `(closed o)` as `o`), and rules (`gen-state-close`, `gen-state-pass`, `power-deliver-once`) using `(gen-st ...)`.
- **Roles & Variables**:
  - Role `dev-up`: Vars: `(k skey)`, `(d o name)`, `(old old1 mesg)`, `(start-ch chan)`, `(lk ls locn)` | Role Assumptions: `(auth start-ch)` | Trace (6 events): `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(load ls old1)` -> `(stor ls (dev-state-closed d o))` -> `(stor lk (dev-key-state d o k))` -> `(send (enc "up" k))`
  - Role `owner-power-dev`: Vars: `(k skey)`, `(d o name)`, `(start-ch chan)` | Role Assumptions: `(conf start-ch)` | Trace (2 events): `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "open" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-opened d o))` -> `(send n)`
  - Role `dev-close`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "close" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-closed d o))` -> `(send n)`
  - Role `dev-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: `(uniq-orig n)` | Trace (4 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "may I pass" k))` -> `(load ls (dev-state-opened d o))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(l locn)` | Role Assumptions: none | Trace (2 events): `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (6)**: `(dev-key-state d o k)`, `(opened o)`, `(closed o)`, `(dev-state-opened d o)`, `(dev-state-closed d o)`, `(dev-state-any d o any)`
  - **Rules (3)**: `gen-state-close`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-close" z 1) (p "dev-close" "d" z d) (p "dev-close" "o" z o) (p "dev-close" "k" z k) (p "dev-close" "any" z (opened o))) (gen-st (dev-state-opened d o))))`; `gen-state-pass`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "d" z d) (p "dev-pass" "o" z o) (p "dev-pass" "k" z k)) (gen-st (dev-state-opened d o))))`; `power-deliver-once`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(deflistener k)`, `(uniq-orig k)` | Skeleton 2 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand dev-pass 4 (k k))` | Skeleton 3 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(defstrand dev-pass 4 (k k))`, `(uniq-orig k)`
  - **Keywords & Predicates Used**: `and`, `auth`, `bound`, `comment`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `forall`, `gen-st`, `herald`, `implies`, `load`, `p`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling hardware or protocol state machines with multiple `locn` registers (`lk`, `ls`), channel assumptions (`(auth start-ch)`, `(conf start-ch)`), and `(gen-st ...)` rules.
- **Key S-Expression Excerpt** (lines 24–59):
```scheme
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
```

## open-closed-tag.scm

- **File Path**: `03_examples_scm/open-closed-tag.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald open-closed (bound 44))` | Flags: `(bound 44)` (commented-out flags in source: `(try-old-strands)`, `(check-nonces)`, `(reverse-nodes)`)
- **Protocol & Purpose**: Protocol(s): `open-closed`. Variant of the stateful `open-closed` device protocol where the `opened` and `closed` state macros use string literal tags (`"opened"` and `"closed"`) instead of name-based encodings, and includes an explicit realized 5-strand skeleton showing how `dev-open` and `dev-up` interact across multiple locations (`lk`, `lk-0`, `ls`, `ls-0`).
- **Roles & Variables**:
  - Role `dev-up`: Vars: `(k skey)`, `(d o name)`, `(old old1 mesg)`, `(start-ch chan)`, `(lk ls locn)` | Role Assumptions: `(auth start-ch)` | Trace (6 events): `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(stor lk (dev-key-state d o k))` -> `(load ls old1)` -> `(stor ls (dev-state-closed d o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev`: Vars: `(k skey)`, `(d o name)`, `(start-ch chan)` | Role Assumptions: `(conf start-ch)` | Trace (2 events): `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "open" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-opened d o))` -> `(send n)`
  - Role `dev-close`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "close" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-closed d o))` -> `(send n)`
  - Role `dev-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: `(uniq-orig n)` | Trace (4 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "may I pass" k))` -> `(load ls (dev-state-opened d o))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(l locn)` | Role Assumptions: none | Trace (2 events): `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (6)**: `(dev-key-state d o k)`, `(opened o)`, `(closed o)`, `(dev-state-opened d o)`, `(dev-state-closed d o)`, `(dev-state-any d o any)`
  - **Rules (3)**: `gen-state-close`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-close" z 1) (p "dev-close" "d" z d) (p "dev-close" "o" z o) (p "dev-close" "k" z k) (p "dev-close" "any" z (opened o))) (gen-st (dev-state-opened d o))))`; `gen-state-pass`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "d" z d) (p "dev-pass" "o" z o) (p "dev-pass" "k" z k)) (gen-st (dev-state-opened d o))))`; `power-deliver-once`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
  - **Goals**: None
  - **Skeletons (4)**: Skeleton 1 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(deflistener k)`, `(uniq-orig k)` | Skeleton 2 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand dev-pass 4 (k k))` | Skeleton 3 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(defstrand dev-pass 4 (k k))`, `(uniq-orig k)` | Skeleton 4 (`open-closed`): `(vars (old old1 any mesg) (n n-0 text) (d o name) (k k-0 skey) (start-ch chan) (ls lk ls-0 lk-0 locn))`, `(defstrand owner-power-dev 2 (d d) (o o) (k k) (start-ch start-ch))`, `(defstrand dev-pass 4 (n n) (d d) (o o) (k k) (lk lk) (ls ls))`, `(defstrand dev-up 6 (old old) (old1 old1) (d d) (o o) (k k) (start-ch start-ch) (lk lk) (ls ls-0))`, `(defstrand user-pass 1 (k k))`, `(defstrand dev-open 4 (any any) (n n-0) (d d) (o o) (k k-0) (lk lk-0) (ls ls))`, `(precedes ((0 0) (2 0)) ((2 2) (1 0)) ((2 5) (0 1)) ((3 0) (1 1)) ((4 3) (1 2)))`, `(uniq-orig n k)`
  - **Keywords & Predicates Used**: `and`, `auth`, `bound`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `forall`, `gen-st`, `herald`, `implies`, `load`, `p`, `precedes`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when using string literal tags (`"opened"`, `"closed"`) inside `locn` state macros (`load`/`stor`) and inspecting multi-strand state transition skeletons.
- **Key S-Expression Excerpt** (lines 7–45):
```scheme
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
```

## open-closed.scm

- **File Path**: `03_examples_scm/open-closed.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald open-closed (bound 44))` | Flags: `(bound 44)` (commented-out flags in source: `(try-old-strands)`, `(check-nonces)`, `(reverse-nodes)`)
- **Protocol & Purpose**: Protocol(s): `open-closed`. Full version of the stateful `open-closed` device protocol that extends `open-closed-multiloc.scm` with two additional rules demonstrating built-in location/state predicates: `(same-locn z1 i1 z2 i2)` (recording `(fact ha z1 i1 z2 i2)`) and `(leads-to z1 i1 z2 i2)` (recording `(fact la z1 i1 z2 i2)`), along with rule-level `(comment ...)` clauses.
- **Roles & Variables**:
  - Role `dev-up`: Vars: `(k skey)`, `(d o name)`, `(old old1 mesg)`, `(start-ch chan)`, `(lk ls locn)` | Role Assumptions: `(auth start-ch)` | Trace (6 events): `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(stor lk (dev-key-state d o k))` -> `(load ls old1)` -> `(stor ls (dev-state-closed d o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev`: Vars: `(k skey)`, `(d o name)`, `(start-ch chan)` | Role Assumptions: `(conf start-ch)` | Trace (2 events): `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close`: Vars: `(k skey)`, `(n text)`, `(d o name)` | Role Assumptions: none | Trace (2 events): `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "open" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-opened d o))` -> `(send n)`
  - Role `dev-close`: Vars: `(k skey)`, `(n text)`, `(any mesg)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: none | Trace (5 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "close" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-closed d o))` -> `(send n)`
  - Role `dev-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(lk ls locn)` | Role Assumptions: `(uniq-orig n)` | Trace (4 events): `(load lk (dev-key-state d o k))` -> `(recv (enc "may I pass" k))` -> `(load ls (dev-state-opened d o))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass`: Vars: `(k skey)`, `(n text)`, `(d o name)`, `(l locn)` | Role Assumptions: none | Trace (2 events): `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (6)**: `(dev-key-state d o k)`, `(opened o)`, `(closed o)`, `(dev-state-opened d o)`, `(dev-state-closed d o)`, `(dev-state-any d o any)`
  - **Rules (5)**: `gen-state-close`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-close" z 1) (p "dev-close" "d" z d) (p "dev-close" "o" z o) (p "dev-close" "k" z k) (p "dev-close" "any" z (opened o))) (gen-st (dev-state-opened d o))))`; `gen-state-pass`: `(forall ((z strd) (d o name) (k skey)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "d" z d) (p "dev-pass" "o" z o) (p "dev-pass" "k" z k)) (gen-st (dev-state-opened d o))))`; `power-deliver-once`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z2 z1)))`; `same-locn`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (same-locn z1 i1 z2 i2) (fact ha z1 i1 z2 i2)))`; `leadsto-la`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (leads-to z1 i1 z2 i2) (fact la z1 i1 z2 i2)))`
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(deflistener k)`, `(uniq-orig k)` | Skeleton 2 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand dev-pass 4 (k k))` | Skeleton 3 (`open-closed`): `(vars (k skey) (d o name) (n text) (start-ch chan))`, `(defstrand owner-power-dev 2 (k k))`, `(defstrand dev-pass 4 (k k))`, `(uniq-orig k)`
  - **Keywords & Predicates Used**: `and`, `auth`, `bound`, `comment`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `forall`, `gen-st`, `herald`, `implies`, `leads-to`, `load`, `p`, `recv`, `same-locn`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example to learn the exact syntax of the built-in stateful predicates `(same-locn z1 i1 z2 i2)` and `(leads-to z1 i1 z2 i2)` over strand (`strd`) and node index (`indx`) variables in `(defrule ...)`.
- **Key S-Expression Excerpt** (lines 100–131):
```scheme
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

```

## or.scm

- **File Path**: `03_examples_scm/or.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Otway-Rees Protocol" (comment "Standard version using variables of sort mesg"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `or`. Standard version of the Otway-Rees symmetric key distribution protocol (`or`) with roles `init`, `resp`, and `serv`, demonstrating the use of sort `mesg` variables (`x` and `y`) in `resp` to forward opaque encrypted tickets (`x` from `init` to `serv`, and `y` from `serv` to `init`) that `resp` cannot decrypt.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b s name)`, `(na text)`, `(k skey)`, `(m text)` | Role Assumptions: none | Trace (2 events): `(send (cat m a b (enc na m a b (ltk a s))))` -> `(recv (cat m (enc na k (ltk a s))))`
  - Role `resp`: Vars: `(a b s name)`, `(nb text)`, `(k skey)`, `(m text)`, `(x y mesg)` | Role Assumptions: none | Trace (4 events): `(recv (cat m a b x))` -> `(send (cat m a b x (enc nb m a b (ltk b s))))` -> `(recv (cat m y (enc nb k (ltk b s))))` -> `(send y)`
  - Role `serv`: Vars: `(a b s name)`, `(na nb text)`, `(k skey)`, `(m text)` | Role Assumptions: `(uniq-orig k)` | Trace (2 events): `(recv (cat m a b (enc na m a b (ltk a s)) (enc nb m a b (ltk b s))))` -> `(send (cat m (enc na k (ltk a s)) (enc nb k (ltk b s))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`or`): `(vars (nb text) (s a b name))`, `(defstrand resp 4 (a a) (b b) (s s) (nb nb))`, `(non-orig (ltk a s) (ltk b s))`, `(uniq-orig nb)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example whenever an intermediate or responder role must receive and forward an opaque ciphertext or token it cannot decrypt, using variables of sort `mesg` (`(vars ... (x y mesg))`).
- **Key S-Expression Excerpt** (lines 1–27):
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

## ordered.scm

- **File Path**: `03_examples_scm/ordered.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald ordered)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ordered`. Demonstrates a linear ordering rule (`order`) over decryption strands (`dec`) using the low-level role predicate syntax `(p "dec" y 2)` and `(p "dec" z 2)`, concluding `(or (prec y 1 z 0) (prec z 1 y 0) (= y z))`. Also illustrates how CPSA records rule-application output annotations (`(rule order)`, `(traces ...)`, `(label 3)`, `(parent 0)`, `(unrealized)`, `(shape)`, `(maps ...)`, `(origs)`) in an output skeleton.
- **Roles & Variables**:
  - Role `dec`: Vars: `(t text)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc t k))` -> `(send t)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `order`: `(forall ((y z strd)) (implies (and (p "dec" y 2) (p "dec" z 2)) (or (prec y 1 z 0) (prec z 1 y 0) (= y z))))`
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`ordered`): `(vars (a b text))`, `(defstrand dec 2 (t a))`, `(defstrand dec 2 (t b))`, `(facts (neq a b))` | Skeleton 2 (`ordered`): `(vars (b text) (k akey))`, `(defstrand dec 2 (t b) (k k))`, `(facts (neq b b))`, `(rule order)`, `(traces ((recv (enc b k)) (send b)))`, `(label 3)`, `(parent 0)`, `(unrealized)`, `(shape)`, `(maps ((0 0) ((a b) (b b) (k k) (k-0 k))))`, `(origs)`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `facts`, `forall`, `herald`, `implies`, `label`, `maps`, `neq`, `or`, `origs`, `p`, `parent`, `prec`, `recv`, `rule`, `send`, `shape`, `trace`, `traces`, `unrealized`, `vars`
- **When to Reference This Example**: Reference this example when writing a rule (`defrule`) that forces all instances of a role to execute sequentially (linear ordering via `(or (prec y 1 z 0) (prec z 1 y 0) (= y z))`) using the `(p "<role>" <strd> <height>)` predicate syntax.
- **Key S-Expression Excerpt** (lines 1–39):
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

## orderedvar.scm

- **File Path**: `03_examples_scm/orderedvar.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald ordered)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ordered`. Identical to `ordered.scm` except that the `order` rule is written using CPSA's role-variable predicate syntax `(strand dec y 2)` and `(strand dec z 2)` instead of string-quoted `(p "dec" y 2)`.
- **Roles & Variables**:
  - Role `dec`: Vars: `(t text)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc t k))` -> `(send t)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `order`: `(forall ((y z strd)) (implies (and (strand dec y 2) (strand dec z 2)) (or (prec y 1 z 0) (prec z 1 y 0) (= y z))))`
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`ordered`): `(vars (a b text))`, `(defstrand dec 2 (t a))`, `(defstrand dec 2 (t b))`, `(facts (neq a b))` | Skeleton 2 (`ordered`): `(vars (b text) (k akey))`, `(defstrand dec 2 (t b) (k k))`, `(facts (neq b b))`, `(rule order)`, `(traces ((recv (enc b k)) (send b)))`, `(label 3)`, `(parent 0)`, `(unrealized)`, `(shape)`, `(maps ((0 0) ((a b) (b b) (k k) (k-0 k))))`, `(origs)`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `facts`, `forall`, `herald`, `implies`, `label`, `maps`, `neq`, `or`, `origs`, `parent`, `prec`, `recv`, `rule`, `send`, `shape`, `strand`, `trace`, `traces`, `unrealized`, `vars`
- **When to Reference This Example**: Reference this example to compare the cleaner `(strand <role> <strd> <height>)` syntax against `(p "<role>" <strd> <height>)` inside `(defrule ...)`.
- **Key S-Expression Excerpt** (lines 1–39):
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

## pca.scm

- **File Path**: `03_examples_scm/pca.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Privacy Certificate Authority" (bound 15) (comment "Generation of an Attestation Identity Certificate"))` | Flags: `(bound 15)`
- **Protocol & Purpose**: Protocol(s): `pca`. Models a simplified Privacy Certificate Authority (`pca`) protocol for generating a TPM Attestation Identity Certificate (AIC), with roles `tpm`, `pca`, and `appr` (appraiser) and herald flag `(bound 15)`. The TPM sends a self-signed identity key `(enc ki a (invk ki))` and manufacturer-certified endorsement key `(enc t ke (invk km))` to the PCA, receives the signed AIC `(enc ki a t (invk kp))` encrypted under `ke`, and forwards the AIC to the appraiser.
- **Roles & Variables**:
  - Role `tpm`: Vars: `(ke ki km kp akey)`, `(t a text)` | Role Assumptions: `(non-orig (invk ke) (invk ki) (invk km) (invk kp))`, `(uniq-orig ki)` | Trace (3 events): `(send (cat (enc ki a (invk ki)) (enc t ke (invk km))))` -> `(recv (enc (enc ki a t (invk kp)) ke))` -> `(send (enc ki a t (invk kp)))`
  - Role `pca`: Vars: `(ke ki km kp akey)`, `(t a text)` | Role Assumptions: `(non-orig (invk ke) (invk ki) (invk km) (invk kp))` | Trace (2 events): `(recv (cat (enc ki a (invk ki)) (enc t ke (invk km))))` -> `(send (enc (enc ki a t (invk kp)) ke))`
  - Role `appr`: Vars: `(ki kp akey)`, `(t a text)` | Role Assumptions: `(non-orig (invk ki) (invk kp))` | Trace (1 events): `(recv (enc ki a t (invk kp)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`pca`): `(vars (ki kp akey))`, `(defstrand appr 1 (ki ki) (kp kp))`, `(non-orig (invk ki) (invk kp))`
  - **Keywords & Predicates Used**: `bound`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling PKI certificate issuance or TPM Attestation Identity Certificate (AIC) enrollment where a CA wraps a newly signed certificate `(enc ki a t (invk kp))` inside an encryption key `ke`.
- **Key S-Expression Excerpt** (lines 1–36):
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

## pen-non-orig-test.scm

- **File Path**: `03_examples_scm/pen-non-orig-test.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "pen-non-orig test")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `pennonorigtest`. Minimal test case (`pennonorigtest`) illustrating the exact semantics of `(pen-non-orig pwd)`. Because `pwd` is declared `(pen-non-orig pwd)` in `server`, the penetrator does not know `pwd` initially (so `server` receiving `(cat userid pwd)` in cleartext must still be explained by a legitimate `client` strand), even though the penetrator learns `pwd` once `client` transmits it in the clear (so the second skeleton with `(deflistener pwd)` is also realized).
- **Roles & Variables**:
  - Role `client`: Vars: `(userid name)`, `(pwd text)` | Role Assumptions: none | Trace (1 events): `(send (cat userid pwd))`
  - Role `server`: Vars: `(userid name)`, `(pwd text)` | Role Assumptions: `(pen-non-orig pwd)` | Trace (1 events): `(recv (cat userid pwd))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`pennonorigtest`): `(vars (pwd text))`, `(defstrand server 1 (pwd pwd))` | Skeleton 2 (`pennonorigtest`): `(vars (pwd text))`, `(defstrand server 1 (pwd pwd))`, `(deflistener pwd)`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `pen-non-orig`, `recv`, `send`, `trace`, `vars`
- **When to Reference This Example**: Reference this example to understand the difference between `(non-orig x)` (never sent in the clear or learned by the penetrator) and `(pen-non-orig x)` (not initially known to or originated by the penetrator, even if later exposed on the network, such as passwords or pre-shared session keys).
- **Key S-Expression Excerpt** (lines 1–29):
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

## pfs-via-pubkey.scm

- **File Path**: `03_examples_scm/pfs-via-pubkey.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald pfs-via-pubkey)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `pfs-easy`. Demonstrates how to model Perfect Forward Secrecy (PFS) in CPSA (`pfs-easy`) by having `init` generate an ephemeral asymmetric key `new-akey`, sign it with long-term signing key `(privk "sgn" a)`, receive a secret `s` encrypted under `new-akey`, and then explicitly transmit the long-term private key `(send (privk "sgn" a))` at the end of the trace to model subsequent key compromise (requiring `(uniq-orig (privk "sgn" a))` instead of `(non-orig (privk "sgn" a))`).
- **Roles & Variables**:
  - Role `init`: Vars: `(new-akey akey)`, `(a b name)`, `(n data)`, `(s text)` | Role Assumptions: none | Trace (3 events): `(send (enc a b new-akey n (privk "sgn" a)))` -> `(recv (enc (enc a n s (privk "sgn" b)) new-akey))` -> `(send (privk "sgn" a))`
  - Role `resp`: Vars: `(new-akey akey)`, `(a b name)`, `(n data)`, `(s text)` | Role Assumptions: none | Trace (2 events): `(recv (enc a b new-akey n (privk "sgn" a)))` -> `(send (enc (enc a n s (privk "sgn" b)) new-akey))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`pfs-easy`): `(vars (new-akey akey) (a b name) (n data) (s text))`, `(defstrand init 3 (a a) (b b) (new-akey new-akey) (n n))`, `(non-orig (privk "sgn" b) (invk new-akey))`, `(uniq-orig (privk "sgn" a) new-akey n)` | Skeleton 2 (`pfs-easy`): `(vars (new-akey akey) (a b name) (n data) (s text))`, `(defstrand resp 2 (a a) (new-akey new-akey))`, `(non-orig (privk "sgn" a))` | Skeleton 3 (`pfs-easy`): `(vars (s text) (n data) (a b name) (new-akey akey))`, `(defstrand resp 2 (s s) (n n) (a a) (b b) (new-akey new-akey))`, `(defstrand init 3 (n n) (a a) (b b) (new-akey new-akey))`, `(deflistener s)`, `(precedes ((1 0) (0 0)))`, `(non-orig (invk new-akey))`, `(uniq-orig (privk "sgn" a) s)`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example whenever you need to model Perfect Forward Secrecy (PFS) or post-compromise security by transmitting a long-term key `(send (privk ...))` at the end of a role and declaring it `uniq-orig` rather than `non-orig`.
- **Key S-Expression Excerpt** (lines 1–35):
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

## pkinit.scm

- **File Path**: `03_examples_scm/pkinit.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Kerberos PK init")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `pkinit`. Models the Kerberos PKINIT (Public Key Cryptography for Initial Authentication in Kerberos, RFC 4556) exchange (`pkinit`) between `client` (`c`) and authentication server `auth` (`as`), combining public-key signatures/encryption (`(privk c)`, `(privk as)`, `(pubk c)`) with symmetric session keys (`k`, `ak` of sort `skey`).
- **Roles & Variables**:
  - Role `client`: Vars: `(c t as name)`, `(n2 n1 text)`, `(tc tk tgt data)`, `(k ak skey)` | Role Assumptions: `(uniq-orig n1 n2)` | Trace (2 events): `(send (cat (enc tc n2 (privk c)) c t n1))` -> `(recv (cat (enc (enc k n2 (privk as)) (pubk c)) c tgt (enc ak n1 tk t k)))`
  - Role `auth`: Vars: `(c t as name)`, `(n2 n1 text)`, `(tc tk tgt data)`, `(k ak skey)` | Role Assumptions: `(uniq-orig k ak)` | Trace (2 events): `(recv (cat (enc tc n2 (privk c)) c t n1))` -> `(send (cat (enc (enc k n2 (privk as)) (pubk c)) c tgt (enc ak n1 tk t k)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`pkinit`): `(vars (c as name))`, `(defstrand client 2 (c c) (as as))`, `(non-orig (privk c) (privk as))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling RFC 4556 (Kerberos PKINIT) or protocols that bootstrap symmetric Kerberos tickets (`tgt`) and session keys (`k`, `ak`) from an initial public-key signed request.
- **Key S-Expression Excerpt** (lines 1–22):
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

## preprocess.scm

- **File Path**: `03_examples_scm/preprocess.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Pre-processing test example: modified NS with two responders")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`. Tests CPSA's preskeleton preprocessing on a modified Needham-Schroeder protocol (`ns`) where the responder originates two nonces (`n2`, `n3`) and the initial skeleton entangles one initiator strand (`(n2 n2) (n3 n3)`) with two responder strands (`(n2 n2) (n3 n3p)` and `(n2 n2p) (n3 n3)`).
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n1 n2 n3 text)` | Role Assumptions: `(uniq-orig n1)` | Trace (3 events): `(send (enc n1 a (pubk b)))` -> `(recv (enc n1 n2 n3 (pubk a)))` -> `(send (enc n2 n3 (pubk b)))`
  - Role `resp`: Vars: `(a b name)`, `(n1 n2 n3 text)` | Role Assumptions: `(uniq-orig n2 n3)` | Trace (3 events): `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 n3 (pubk a)))` -> `(recv (enc n2 n3 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`ns`): `(vars (a b name) (n1 n2 n3 n2p n3p text))`, `(defstrand init 3 (a a) (b b) (n1 n1) (n2 n2) (n3 n3))`, `(defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2) (n3 n3p))`, `(defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2p) (n3 n3))`, `(non-orig (privk b) (privk a))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when constructing multi-strand preskeletons that test whether entangled responder sessions must collapse into a single session due to `uniq-orig` constraints.
- **Key S-Expression Excerpt** (lines 1–27):
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

## print.scm

- **File Path**: `03_examples_scm/print.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Print Test" (comment "See if read forms look like printed ones"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `print-test`. Minimal test (`print-test`) verifying the canonical order in which CPSA prints variables of different sorts (`akey`, `skey`, `data`) in `vars` declarations and strand mappings.
- **Roles & Variables**:
  - Role `role`: Vars: `(a b akey)`, `(f g skey)`, `(x y data)` | Role Assumptions: none | Trace (1 events): `(recv (cat a b f g x y))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`print-test`): `(vars (a b akey) (f g skey) (x y data))`, `(defstrand role 1 (a a) (b b) (f f) (g g) (x x) (y y))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `recv`, `trace`, `vars`
- **When to Reference This Example**: Reference this example as a minimal 13-line syntax check for grouping multiple variables per sort `(vars (a b akey) (f g skey) (x y data))` in `defrole` and `defskeleton`.
- **Key S-Expression Excerpt** (lines 1–13):
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

## prottrans.scm

- **File Path**: `03_examples_scm/prottrans.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Protocol Transformations With Rules")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `ns`, `unilateral`, `ns-with-rule`. Demonstrates protocol transformations with rules (`Protocol Transformations With Rules`). Defines three protocols: standard `ns` (with `akey` principals), a 2-message `unilateral` challenge-response protocol (with its Shape Analysis Sentence shown as a commented `defgoal`), and `ns-with-rule`, which embeds the image of the `unilateral` shape analysis sentence as a `(defrule unilateral ...)` inside Needham-Schroeder.
- **Roles & Variables**:
  - Role `init` (in `ns`): Vars: `(a b akey)`, `(na nb text)` | Role Assumptions: none | Trace (3 events): `(send (enc na a b))` -> `(recv (enc na nb a))` -> `(send (enc nb b))`
  - Role `resp` (in `ns`): Vars: `(b a akey)`, `(nb na text)` | Role Assumptions: none | Trace (3 events): `(recv (enc na a b))` -> `(send (enc na nb a))` -> `(recv (enc nb b))`
  - Role `init` (in `unilateral`): Vars: `(n text)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(send (enc n k))` -> `(recv n)`
  - Role `resp` (in `unilateral`): Vars: `(n text)`, `(k akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc n k))` -> `(send n)`
  - Role `init` (in `ns-with-rule`): Vars: `(a b akey)`, `(na nb text)` | Role Assumptions: none | Trace (3 events): `(send (enc na a b))` -> `(recv (enc na nb a))` -> `(send (enc nb b))`
  - Role `resp` (in `ns-with-rule`): Vars: `(b a akey)`, `(nb na text)` | Role Assumptions: none | Trace (3 events): `(recv (enc na a b))` -> `(send (enc na nb a))` -> `(recv (enc nb b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `unilateral`: `(forall ((r strd) (a akey) (nb text)) (implies (and (p "resp" r 3) (p "resp" "a" r a) (p "resp" "nb" r nb) (non (invk a)) (uniq nb)) (exists ((i strd)) (and (p "init" i 3) (p "init" "a" i a) (p "init" "nb" i nb) (prec r 1 i 1) (prec i 2 r 2)))))`
  - **Goals**: None active (contains a commented-out `(defgoal unilateral ...)` inside `(comment ...)` showing the Shape Analysis Sentence before rule translation)
  - **Skeletons (4)**: Skeleton 1 (`ns`): `(vars (a b akey) (na text))`, `(defstrand init 3 (a a) (b b) (na na))`, `(non-orig (invk a) (invk b))`, `(uniq-orig na)` | Skeleton 2 (`ns`): `(vars (a akey) (nb text))`, `(defstrand resp 3 (a a) (nb nb))`, `(non-orig (invk a))`, `(uniq-orig nb)` | Skeleton 3 (`unilateral`): `(vars (k akey) (n text))`, `(defstrand init 2 (n n) (k k))`, `(non-orig (invk k))`, `(uniq-orig n)` | Skeleton 4 (`ns-with-rule`): `(vars (a akey) (nb text))`, `(defstrand resp 3 (a a) (nb nb))`, `(non-orig (invk a))`, `(uniq-orig nb)`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `exists`, `forall`, `herald`, `implies`, `non`, `non-orig`, `p`, `prec`, `recv`, `send`, `trace`, `uniq`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when translating a proved shape analysis sentence (`defgoal`) from a sub-protocol (`unilateral`) into a lemma/rule (`defrule`) inside a larger protocol (`ns-with-rule`).
- **Key S-Expression Excerpt** (lines 65–107):
```scheme
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

## pruning1.scm

- **File Path**: `03_examples_scm/pruning1.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` form in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Protocol(s): `prune`. Regression test (`prune`) demonstrating a subtle case of strand pruning where `init` sends `(enc n (pubk a))` and expects both `(enc n (pubk b) (pubk a))` and `(enc n (privk b) (pubk a))`, requiring two separate instances of the transformer role `trans` (one with `k = (pubk b)` and one with `k = (privk b)`).
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(n text)` | Role Assumptions: `(uniq-orig n)`, `(non-orig (privk a))` | Trace (3 events): `(send (enc n (pubk a)))` -> `(recv (enc n (pubk b) (pubk a)))` -> `(recv (enc n (privk b) (pubk a)))`
  - Role `trans`: Vars: `(a name)`, `(n text)`, `(k akey)` | Role Assumptions: none | Trace (3 events): `(recv (enc n (pubk a)))` -> `(recv k)` -> `(send (enc n k (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`prune`): `(vars (a name) (n text) (k akey))`, `(defstrand init 3)` | Skeleton 2 (`prune`): `(vars (n text) (a b name))`, `(defstrand init 3 (n n) (a a) (b b))`, `(defstrand trans 3 (n n) (a a) (k (pubk b)))`, `(defstrand trans 3 (n n) (a a) (k (privk b)))`, `(precedes ((0 0) (1 0)) ((0 0) (2 0)) ((1 2) (0 1)) ((2 2) (0 2)))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when a protocol role (`trans`) takes a generic key variable `(k akey)` that must be instantiated with both `(pubk b)` and `(privk b)` across distinct strands in the same shape.
- **Key S-Expression Excerpt** (lines 12–42):
```scheme
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

## puzzle_example.scm

- **File Path**: `03_examples_scm/puzzle_example.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald puzzle_example)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `puzzle`. Models a symmetric-key challenge-response and payload encryption protocol (`puzzle`) using `(ltk a b)` and fresh session key `(s skey)`, followed by 7 different `(defskeleton ...)` queries exploring initiator POV, responder POV, and confidentiality of `s` and `payload` with `(deflistener ...)` and explicit `(precedes ...)` constraints.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(na payload text)`, `(s skey)` | Role Assumptions: none | Trace (3 events): `(send na)` -> `(recv (enc na s (ltk a b)))` -> `(send (enc payload s))`
  - Role `resp`: Vars: `(a b name)`, `(na payload text)`, `(s skey)` | Role Assumptions: none | Trace (3 events): `(recv na)` -> `(send (enc na s (ltk a b)))` -> `(recv (enc payload s))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (7)**: Skeleton 1 (`puzzle`): `(vars (a b name) (na payload text) (s skey))`, `(defstrand init 3 (a a) (b b) (na na) (payload payload))`, `(uniq-orig na payload)`, `(non-orig (ltk a b))` | Skeleton 2 (`puzzle`): `(vars (a b name) (na payload text) (s skey))`, `(defstrand init 3 (a a) (b b) (na na) (payload payload))`, `(deflistener payload)`, `(uniq-orig na payload)`, `(non-orig (ltk a b))` | Skeleton 3 (`puzzle`): `(vars (na payload text) (a b name) (s skey))`, `(defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))`, `(defstrand resp 2 (na na) (a a) (b b) (s s))`, `(deflistener s)`, `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`, `(non-orig (ltk a b))`, `(uniq-orig s na payload)` | Skeleton 4 (`puzzle`): `(vars (na payload text) (a b name) (s skey))`, `(defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))`, `(defstrand resp 2 (na na) (a a) (b b) (s s))`, `(deflistener payload)`, `(precedes ((0 0) (1 0)) ((1 1) (0 1)))`, `(non-orig (ltk a b))`, `(uniq-orig s na payload)` | Skeleton 5 (`puzzle`): `(vars (a b name) (na payload text) (s skey))`, `(defstrand resp 3 (a a) (b b) (s s) (payload payload))`, `(uniq-orig s)`, `(non-orig (ltk a b))` | Skeleton 6 (`puzzle`): `(vars (a b name) (na payload text) (s skey))`, `(defstrand resp 3 (a a) (b b) (s s) (payload payload))`, `(deflistener s)`, `(uniq-orig s)`, `(non-orig (ltk a b))` | Skeleton 7 (`puzzle`): `(vars (payload na text) (a b name) (s skey))`, `(defstrand resp 3 (na na) (payload payload) (a a) (b b) (s s))`, `(defstrand init 3 (na na) (payload payload) (a a) (b b) (s s))`, `(deflistener payload)`, `(precedes ((0 1) (1 1)) ((1 2) (0 2)))`, `(non-orig (ltk a b))`, `(uniq-orig s payload)`
  - **Keywords & Predicates Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for a complete set of `defskeleton` patterns testing initiator POV, responder POV, session-key secrecy (`(deflistener s)`), and payload secrecy (`(deflistener payload)`) on a single protocol.
- **Key S-Expression Excerpt** (lines 1–37):
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
```

## reflect.scm

- **File Path**: `03_examples_scm/reflect.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald reflect)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `reflect`. Models a 2-message asymmetric signature protocol (`reflect`) where `init` sends `(enc b (invk a))` and receives `(enc a (invk b))`. Also demonstrates passing an inverted key `(b (invk b))` as a role parameter in the third skeleton and declaring `(non-orig (invk a) b)`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b akey)` | Role Assumptions: none | Trace (2 events): `(send (enc b (invk a)))` -> `(recv (enc a (invk b)))`
  - Role `resp`: Vars: `(a b akey)` | Role Assumptions: none | Trace (2 events): `(recv (enc b (invk a)))` -> `(send (enc a (invk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`reflect`): `(vars (a b akey))`, `(defstrand resp 1 (a a) (b b))`, `(non-orig (invk a) (invk b))` | Skeleton 2 (`reflect`): `(vars (a b akey))`, `(defstrand init 2 (a a) (b b))`, `(non-orig (invk a) (invk b))` | Skeleton 3 (`reflect`): `(vars (a b akey))`, `(defstrand resp 1 (a a) (b (invk b)))`, `(non-orig (invk a) b)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `vars`
- **When to Reference This Example**: Reference this example when testing reflection attacks on two-message signature protocols or when instantiating an `akey` role parameter with an inverse key `(invk b)` in `defstrand`.
- **Key S-Expression Excerpt** (lines 1–32):
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

## renamings.scm

- **File Path**: `03_examples_scm/renamings.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Blanchet's Simple Example Protocol" (comment "There is a flaw in this protocol by design") (comment "It also shows how variable renaming works"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `blanchet`. Models Bruno Blanchet's simple sign-then-encrypt protocol (`blanchet`) using intentionally permuted variable names across `init` (`a b name`, `s skey`, `d data`), `resp` (`d a name`, `b skey`, `s data`), and the `defskeleton` declarations (`(defstrand resp 2 (d s) (a d) (b a) (s b))`) to test CPSA's key-value variable renaming and binding logic.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b name)`, `(s skey)`, `(d data)` | Role Assumptions: none | Trace (2 events): `(send (enc (enc s (privk a)) (pubk b)))` -> `(recv (enc d s))`
  - Role `resp`: Vars: `(d a name)`, `(b skey)`, `(s data)` | Role Assumptions: none | Trace (2 events): `(recv (enc (enc b (privk d)) (pubk a)))` -> `(send (enc s b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`blanchet`): `(vars (s d name) (a skey) (b data))`, `(defstrand resp 2 (d s) (a d) (b a) (s b))`, `(non-orig (privk s) (privk d))`, `(uniq-orig a)` | Skeleton 2 (`blanchet`): `(vars (s d name) (a skey) (b data))`, `(defstrand init 2 (a s) (b d) (s a) (d b))`, `(non-orig (privk d))`, `(uniq-orig a)`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example to understand how `(defstrand <role> <height> (<role-var> <skel-var>)...)` maps role-local variable names (left) to skeleton-level variable names (right) even when their identifiers overlap.
- **Key S-Expression Excerpt** (lines 1–30):
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

## role_uniq.scm

- **File Path**: `03_examples_scm/role_uniq.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Role Unique Origination")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `blanchet`. Demonstrates that a role-level `(uniq-orig s)` assumption in `init` of Blanchet's protocol (`blanchet`) is equivalent to omitting `(uniq-orig s)` from the role and instead adding a protocol rule `(defrule role-uniq (forall ((z strd) (s skey)) (implies (p "init" "s" z s) (uniq s))))`.
- **Roles & Variables**:
  - Role `init`: Vars: `(a b akey)`, `(s skey)`, `(d data)` | Role Assumptions: `(uniq-orig s)` | Trace (2 events): `(send (enc (enc s (invk a)) b))` -> `(recv (enc d s))`
  - Role `resp`: Vars: `(a b akey)`, `(s skey)`, `(d data)` | Role Assumptions: none | Trace (2 events): `(recv (enc (enc s (invk a)) b))` -> `(send (enc d s))`
  - Role `init`: Vars: `(a b akey)`, `(s skey)`, `(d data)` | Role Assumptions: none | Trace (2 events): `(send (enc (enc s (invk a)) b))` -> `(recv (enc d s))`
  - Role `resp`: Vars: `(a b akey)`, `(s skey)`, `(d data)` | Role Assumptions: none | Trace (2 events): `(recv (enc (enc s (invk a)) b))` -> `(send (enc d s))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `role-uniq`: `(forall ((z strd) (s skey)) (implies (p "init" "s" z s) (uniq s)))`
  - **Goals**: None
  - **Skeletons (4)**: Skeleton 1 (`blanchet`): `(vars (a b akey) (s skey) (d data))`, `(defstrand init 2 (a a) (b b) (s s) (d d))`, `(non-orig (invk b))` | Skeleton 2 (`blanchet`): `(vars (a b akey) (s skey) (d data))`, `(defstrand resp 2 (a a) (b b) (s s) (d d))`, `(non-orig (invk a) (invk b))` | Skeleton 3 (`blanchet`): `(vars (a b akey) (s skey) (d data))`, `(defstrand init 2 (a a) (b b) (s s) (d d))`, `(non-orig (invk b))` | Skeleton 4 (`blanchet`): `(vars (a b akey) (s skey) (d data))`, `(defstrand resp 2 (a a) (b b) (s s) (d d))`, `(non-orig (invk a) (invk b))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `forall`, `herald`, `implies`, `non-orig`, `p`, `recv`, `send`, `trace`, `uniq`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example to see how role-level `(uniq-orig ...)` declarations work and how they can be expressed equivalently as logical rules (`(defrule ... (implies (p "init" "s" z s) (uniq s)))`).
- **Key S-Expression Excerpt** (lines 29–56):
```scheme
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

## rule-node.scm

- **File Path**: `03_examples_scm/rule-node.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald rule-node)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `rule-order`, `rule-order-prec`. Tests rules and facts over strand (`strd`) and node index (`indx`) variables in two protocols (`rule-order` and `rule-order-prec`), demonstrating the `(idx 0)` and `(idx 1)` index literal constructors inside skeleton `(facts (le 0 (idx 0) 0 (idx 1)))` as well as `(prec z1 i1 z2 i2)` and `(neq (s t))`.
- **Roles & Variables**:
  - Role `init` (in `rule-order`): Vars: `(s t text)` | Role Assumptions: none | Trace (2 events): `(send (cat s t))` -> `(recv (cat t s))`
  - Role `init` (in `rule-order-prec`): Vars: `(s t text)` | Role Assumptions: none | Trace (2 events): `(send (cat s t))` -> `(recv (cat t s))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (5)**: `le-lt`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (fact le z1 i1 z2 i2) (or (and (= z1 z2) (= i1 i2)) (fact lt z1 i1 z2 i2))))`; `lt-le`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (fact lt z1 i1 z2 i2) (fact le z1 i1 z2 i2)))`; `prec-lt`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (prec z1 i1 z2 i2) (or (fact lt z1 i1 z2 i2))))`; `neq-false`: `(forall ((s mesg)) (implies (fact neq s s) (false)))`; `prec-tell-me`: `(forall ((z1 z2 strd) (i1 i2 indx)) (implies (prec z1 i1 z2 i2) (fact tell-me z1 i1 z2 i2)))`
  - **Goals**: None
  - **Skeletons (5)**: Skeleton 1 (`rule-order`): `(vars (s t s1 t1 text))`, `(defstrand init 2 (s s) (t t))`, `(defstrand init 2 (s t) (t s))`, `(precedes ((1 0) (0 1)))`, `(facts (neq s t))`, `(facts (le 0 (idx 0) 0 (idx 1)))` | Skeleton 2 (`rule-order`): `(vars (s t text))`, `(defstrand init 2 (s s) (t t))`, `(defstrand init 2 (s t) (t s))`, `(precedes ((1 0) (0 1)))`, `(facts (le 1 (idx 0) 0 (idx 1)) (le 0 (idx 0) 0 (idx 1)))` | Skeleton 3 (`rule-order-prec`): `(vars (s t text))`, `(defstrand init 2 (s s) (t t))` | Skeleton 4 (`rule-order-prec`): `(vars (s t text))`, `(defstrand init 2 (s s) (t t))`, `(defstrand init 2 (s t) (t s))`, `(precedes ((1 0) (0 1)))` | Skeleton 5 (`rule-order-prec`): `(vars (s t text))`, `(defstrand init 2 (s s) (t t))`, `(defstrand init 2 (s s) (t t))`, `(precedes ((1 0) (0 1)))`, `(neq (s t))`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `false`, `forall`, `herald`, `implies`, `le`, `neq`, `or`, `prec`, `precedes`, `recv`, `send`, `trace`, `vars`
- **When to Reference This Example**: Reference this example whenever you need to write rules or skeleton `facts` that reference specific strand node indices (`indx` sort and `(idx <int>)` literals) alongside `(prec z1 i1 z2 i2)`.
- **Key S-Expression Excerpt** (lines 1–36):
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

```

## rule-order.scm

- **File Path**: `03_examples_scm/rule-order.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald rule-order)` | Flags: none
- **Protocol & Purpose**: Protocol(s): `rule-order`. Minimal test (`rule-order`) of a disjunctive rule (`ge`: `(forall ((x y text)) (implies (fact le x y) (or (= x y) (fact lt x y))))`) triggered by `(facts (le s t))` in a skeleton, splitting the search into two branches (`s = t` and `(fact lt s t)`).
- **Roles & Variables**:
  - Role `init`: Vars: `(s t text)` | Role Assumptions: none | Trace (1 events): `(send (cat s t))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (1)**: `ge`: `(forall ((x y text)) (implies (fact le x y) (or (= x y) (fact lt x y))))`
  - **Goals**: None
  - **Skeletons (1)**: Skeleton 1 (`rule-order`): `(vars (s t text))`, `(defstrand init 1 (s s) (t t))`, `(facts (le s t))`
  - **Keywords & Predicates Used**: `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `forall`, `herald`, `implies`, `le`, `or`, `send`, `trace`, `vars`
- **When to Reference This Example**: Reference this example for a minimal template of a disjunctive `(defrule ...)` using `(or (= x y) (fact lt x y))` to split CPSA's analysis into equality and strict-inequality cases.
- **Key S-Expression Excerpt** (lines 1–21):
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

## rules.scm

- **File Path**: `03_examples_scm/rules.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Rules and Facts")`; `(herald doorsep (comment "Door Simple Example Protocol"))` | Flags: none
- **Protocol & Purpose**: Protocol(s): `neq-test`, `doorsep`. Contains two complete rule-based protocol examples in one file (each with its own `herald`): `neq-test` (enforcing `n1 != n2` via `(facts (neq n1 n2))` and `(defrule neq ...)`) and `doorsep` (the Door Simple Example Protocol, using `(defrule trust ...)` to express that if an uncompromised person `(non (invk p))` initiates a session with door `d`, then the door's private key is also uncompromised `(non (invk d))`).
- **Roles & Variables**:
  - Role `init` (in `neq-test`): Vars: `(n1 n2 text)`, `(k skey)` | Role Assumptions: `(non-orig k)`, `(uniq-orig n1 n2)` | Trace (2 events): `(send (cat n1 (enc n1 n2 k)))` -> `(recv n2)`
  - Role `person` (in `doorsep`): Vars: `(d p akey)`, `(k skey)`, `(t text)` | Role Assumptions: `(uniq-orig k)` | Trace (3 events): `(send (enc (enc k (invk p)) d))` -> `(recv (enc t k))` -> `(send t)`
  - Role `door` (in `doorsep`): Vars: `(d p akey)`, `(k skey)`, `(t text)` | Role Assumptions: `(uniq-orig t)` | Trace (3 events): `(recv (enc (enc k (invk p)) d))` -> `(send (enc t k))` -> `(recv t)`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros**: None
  - **Rules (2)**: `neq`: `(forall ((a mesg)) (implies (fact neq a a) (false)))`; `trust`: `(forall ((z strd) (p d akey)) (implies (and (p "person" z 1) (p "person" "p" z p) (p "person" "d" z d) (non (invk p))) (non (invk d))))`
  - **Goals**: None
  - **Skeletons (3)**: Skeleton 1 (`neq-test`): `(vars)`, `(defstrand init 2)` | Skeleton 2 (`neq-test`): `(vars (n1 n2 text))`, `(defstrand init 2 (n1 n1) (n2 n2))`, `(facts (neq n1 n2))` | Skeleton 3 (`doorsep`): `(vars (p akey))`, `(defstrand door 3 (p p))`, `(non-orig (invk p))`
  - **Keywords & Predicates Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `false`, `forall`, `herald`, `implies`, `neq`, `non`, `non-orig`, `p`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for the canonical `trust` rule pattern (`(implies (and (p "person" z 1) ... (non (invk p))) (non (invk d)))`), which dynamically derives `(non (invk d))` for whatever peer `d` an honest principal `p` chooses to trust.
- **Key S-Expression Excerpt** (lines 35–67):
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

## scep-tls-dh-broken.scm

- **File Path**: `03_examples_scm/scep-tls-dh-broken.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "Fordham's GREATEST PROTOCOL GO RAMS🐏🐏🐏🐏🐏🐏🐏🐏🐏🐏 Protocol" (algebra diffie-hellman) (comment "By: Mario Marku & Luke Shragher"))` | Flags: `(algebra diffie-hellman)`
- **Protocol & Purpose**: Protocol(s): `dh`. Models a combined TLS + SCEP (Simple Certificate Enrollment Protocol) handshake (`dh`) in the `diffie-hellman` algebra using extensive `(defmacro ...)` definitions (`PMS`, `S_write`, `W_write`, `Tok`, `SCEP-Token`, `Cert_W`, `W_KE`, `S_FMESG`, `SFIN`, `WFIN`) and a confidentiality `(defgoal dh ...)` testing whether an adversary listener `eve` (`(p "" eve 1) (p "" "x" eve (SCEP-Token S M rS))`) can learn the client's SCEP token when `rSp` is sent in the clear.
- **Roles & Variables**:
  - Role `client`: Vars: `(S W M CA name)`, `(rS rW rSp rWp w text)`, `(dh_eS dh_eW rndx)` | Role Assumptions: `(uniq-orig rS rSp)` | Trace (7 events): `(send rSp)` -> `(recv (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))` -> `(send (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))` -> `(recv (WFIN dh_eS dh_eW rSp rWp W CA))` -> `(send (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))` -> `(recv (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))` -> `(send (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))`
  - Role `server`: Vars: `(S W M CA name)`, `(rS rW rSp rWp w text)`, `(dh_eS dh_eW rndx)` | Role Assumptions: `(uniq-orig rW rWp w)` | Trace (7 events): `(recv rSp)` -> `(send (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))` -> `(recv (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))` -> `(send (WFIN dh_eS dh_eW rSp rWp W CA))` -> `(recv (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))` -> `(send (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))` -> `(recv (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (10)**: `(PMS dh_es dh_ew)`, `(S_write dh_es dh_ew rs rw)`, `(W_write dh_es dh_ew rs rw)`, `(Tok X Y data)`, `(SCEP-Token X Y data)`, `(Cert_W W CA dh_ew)`, `(W_KE dh_ew rs rw W)`, `(S_FMESG rs rw W CA dh_ew)`, `(SFIN dh_es dh_ew rs rw W CA)`, `(WFIN dh_es dh_ew rs rw W CA)`
  - **Rules & Lemmas**: None
  - **Goals (1)**: `(defgoal dh (forall ((S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx) (z1 eve strd)) (implies (and (p "client" z1 7) (p "client" "S" z1 S) (p "client" "W" z1 W) (p "client" "M" z1 M) (p "client" "CA" z1 CA) (p "client" "rS" z1 rS) (p "client" "rW" z1 rW) (p "client" "rSp" z1 rSp) (p "client" "rWp" z1 rWp) (p "client" "w" z1 w) (p "client" "dh_eS" z1 dh_eS) (p "client" "dh_eW" z1 dh_eW) (non (privk S)) (non (privk W)) (non (privk M)) (non (privk CA)) (p "" eve 1) (p "" "x" eve (SCEP-Token S M rS))) (false))))`
  - **Skeletons**: None active (note: `;`-commented `defskeleton` blocks appear at the bottom of `scep-tls-dh-broken.scm`)
  - **Keywords & Predicates Used**: `algebra`, `and`, `comment`, `defgoal`, `defmacro`, `defprotocol`, `defrole`, `false`, `forall`, `herald`, `implies`, `non`, `p`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling complex layered protocols (like SCEP over TLS with Diffie-Hellman ephemeral key exchange `(exp (gen) (mul dh_es dh_ew))`) using modular `(defmacro ...)` definitions and low-level `(p ...)` confidentiality goals.
- **Key S-Expression Excerpt** (lines 1–35):
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
```

## scep-tls-dh-fixed.scm

- **File Path**: `03_examples_scm/scep-tls-dh-fixed.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "Fordham's GREATEST PROTOCOL GO RAMS🐏🐏🐏🐏🐏🐏🐏🐏🐏🐏 Protocol" (algebra diffie-hellman) (comment "By: Mario Marku & Luke Shragher"))` | Flags: `(algebra diffie-hellman)`
- **Protocol & Purpose**: Protocol(s): `dh`. Fixed version of `scep-tls-dh-broken.scm` in the `diffie-hellman` algebra where the client encrypts its initial nonce `(send (enc rSp (pubk W)))` under the server's public key, alongside both a confidentiality `(defgoal dh ...)` and two active `(defskeleton dh ...)` declarations using `(defstrandmax client ...)` and `(defstrandmax server ...)` with `(pen-non-orig (privk S) (privk W) (privk CA))`.
- **Roles & Variables**:
  - Role `client`: Vars: `(S W M CA name)`, `(rS rW rSp rWp w text)`, `(dh_eS dh_eW rndx)` | Role Assumptions: `(uniq-orig rS rSp)` | Trace (7 events): `(send (enc rSp (pubk W)))` -> `(recv (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))` -> `(send (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))` -> `(recv (WFIN dh_eS dh_eW rSp rWp W CA))` -> `(send (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))` -> `(recv (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))` -> `(send (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))`
  - Role `server`: Vars: `(S W M CA name)`, `(rS rW rSp rWp w text)`, `(dh_eS dh_eW rndx)` | Role Assumptions: `(uniq-orig rW rWp w)` | Trace (7 events): `(recv (enc rSp (pubk W)))` -> `(send (cat rWp (Cert_W W CA dh_eW) (W_KE dh_eW rSp rWp W)))` -> `(recv (cat (exp (gen) dh_eS) (SFIN dh_eS dh_eW rSp rWp W CA)))` -> `(send (WFIN dh_eS dh_eW rSp rWp W CA))` -> `(recv (enc (cat rS (SCEP-Token S M rS)) (S_write dh_eS dh_eW rSp rWp)))` -> `(send (enc (cat w rW (SCEP-Token W CA w) (enc (hash "server-mutauth" rS rW (SCEP-Token W CA w)) (pubk W))) (W_write dh_eS dh_eW rSp rWp)))` -> `(recv (enc (cat w (enc (hash "client-mutauth" rS rW (SCEP-Token S M rS)) (pubk S))) (S_write dh_eS dh_eW rSp rWp)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (10)**: `(PMS dh_es dh_ew)`, `(S_write dh_es dh_ew rs rw)`, `(W_write dh_es dh_ew rs rw)`, `(Tok X Y data)`, `(SCEP-Token X Y data)`, `(Cert_W W CA dh_ew)`, `(W_KE dh_ew rs rw W)`, `(S_FMESG rs rw W CA dh_ew)`, `(SFIN dh_es dh_ew rs rw W CA)`, `(WFIN dh_es dh_ew rs rw W CA)`
  - **Rules & Lemmas**: None
  - **Goals (1)**: `(defgoal dh (forall ((S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx) (z1 eve strd)) (implies (and (p "client" z1 7) (p "client" "S" z1 S) (p "client" "W" z1 W) (p "client" "M" z1 M) (p "client" "CA" z1 CA) (p "client" "rS" z1 rS) (p "client" "rW" z1 rW) (p "client" "rSp" z1 rSp) (p "client" "rWp" z1 rWp) (p "client" "w" z1 w) (p "client" "dh_eS" z1 dh_eS) (p "client" "dh_eW" z1 dh_eW) (non (privk S)) (non (privk W)) (non (privk M)) (non (privk CA)) (p "" eve 1) (p "" "x" eve (SCEP-Token S M rS))) (false))))`
  - **Skeletons (2)**: Skeleton 1 (`dh`): `(vars (S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx))`, `(defstrandmax client (S S) (W W) (M M) (CA CA) (rS rS) (rW rW) (rSp rSp) (rWp rWp) (w w) (dh_eS dh_eS) (dh_eW dh_eW))`, `(pen-non-orig (privk S) (privk W) (privk CA))` | Skeleton 2 (`dh`): `(vars (S W M CA name) (rS rW rSp rWp w text) (dh_eS dh_eW rndx))`, `(defstrandmax server (S S) (W W) (M M) (CA CA) (rS rS) (rW rW) (rSp rSp) (rWp rWp) (w w) (dh_eS dh_eS) (dh_eW dh_eW))`, `(pen-non-orig (privk S) (privk W) (privk CA))`
  - **Keywords & Predicates Used**: `algebra`, `and`, `comment`, `defgoal`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `false`, `forall`, `herald`, `implies`, `non`, `p`, `pen-non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for combining `diffie-hellman` algebra macros, a confidentiality `(defgoal ...)`, and `(defstrandmax <role> ...)` skeletons in a full TLS + application-layer protocol model.
- **Key S-Expression Excerpt** (lines 88–122):
```scheme
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
```

## sdls-auth-enc-full-payload.scm

- **File Path**: `03_examples_scm/sdls-auth-enc-full-payload.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP Authenticated Encryption: full SDLS-EP rekeying sequence")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-ep-chain-auth-enc`. Full 6-step Space Data Link Security Extended Procedures (CCSDS SDLS-EP, 355.0-B-2 / 355.1-B-1) rekeying chain (`sdls-ep-chain-auth-enc`) in Authenticated Encryption mode between `ground` and `satellite`. Models (1) OTAR key upload under `keymaster`, (2) Key Activation, (3) Rekey SA, (4) Start SA, (5) Key Verification challenge/reply, and (6) Frame Data traffic under the new session keys (`sessionkey1`, `sessionkey2`) and reset sequence number `(successor new_arsn)`, using custom language sorts and hash constructors `(lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash) (spi atom) (gvcid atom))`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(old_arsn new_arsn seq_n)`, `(iv text)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)`, `(keymaster sessionkey1 sessionkey2 skey)`, `(keyid1 keyid2 keyid)`, `(spi spi)`, `(gvcid gvcid)`, `(chal text)`, `(frame_data tc)` | Role Assumptions: `(uniq-gen assumed_enc_key assumed_auth_key old_arsn)`, `(uniq-orig new_arsn chal frame_data sessionkey1 sessionkey2)`, `(non-orig keymaster)` | Trace (7 events): `(send (cat (sdl_header spacecraft) header (successor old_arsn) (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) (hash (sdl_header spacecraft) header (successor old_arsn) (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor old_arsn)) (enc (key_activation_pdu keyid1) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor old_arsn)) (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (enc (start_sa_pdu spi gvcid) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (enc (keyver_cmd keyid1 chal) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor new_arsn) (enc frame_data sessionkey1) (hash (sdl_header spacecraft) header (successor new_arsn) (enc frame_data sessionkey1) sessionkey2)))`
  - Role `satellite`: Vars: `(header text)`, `(old_arsn new_arsn seq_n)`, `(iv text)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)`, `(keymaster sessionkey1 sessionkey2 skey)`, `(keyid1 keyid2 keyid)`, `(spi spi)`, `(gvcid gvcid)`, `(chal text)`, `(frame_data tc)` | Role Assumptions: `(non-orig keymaster)` | Trace (7 events): `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) (hash (sdl_header spacecraft) header (successor old_arsn) (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor old_arsn)) (enc (key_activation_pdu keyid1) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor old_arsn)) (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (enc (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (enc (start_sa_pdu spi gvcid) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (enc (keyver_cmd keyid1 chal) assumed_enc_key) (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor new_arsn) (enc frame_data sessionkey1) (hash (sdl_header spacecraft) header (successor new_arsn) (enc frame_data sessionkey1) sessionkey2)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (9)**: `(sdl_header dest)`, `(otar_pdu masterkeyid uploadblock)`, `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)`, `(otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)`, `(key_activation_pdu keyid)`, `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)`, `(start_sa_pdu spi gvcid)`, `(keyver_cmd keyid chal)`, `(keyver_reply keyid chal sessionkey)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash) (spi atom) (gvcid atom))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-ep-chain-auth-enc`): `(vars (assumed_enc_key assumed_auth_key keymaster skey) (ground spacecraft name) (old_arsn new_arsn seq_n))`, `(defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keymaster keymaster) (old_arsn old_arsn) (new_arsn new_arsn) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_enc_key assumed_auth_key keymaster)`, `(facts (neq old_arsn new_arsn))` | Skeleton 2 (`sdls-ep-chain-auth-enc`): `(vars (assumed_enc_key assumed_auth_key keymaster sessionkey1 sessionkey2 skey) (ground spacecraft name) (old_arsn new_arsn seq_n))`, `(defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2) (old_arsn old_arsn) (new_arsn new_arsn) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_enc_key assumed_auth_key keymaster)`, `(uniq-orig sessionkey1 sessionkey2)`, `(facts (neq old_arsn new_arsn))`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `facts`, `herald`, `lang`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling multi-step key management and rekeying protocols (such as CCSDS SDLS-EP, IPsec/IKEv2 SA rekeying, or counter/sequence-number progression) using custom `(lang (<sort> atom) (<op> hash))` declarations.
- **Key S-Expression Excerpt** (lines 171–206):
```scheme
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
```

## sdls-auth-enc-logic.scm

- **File Path**: `03_examples_scm/sdls-auth-enc-logic.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP Authenticated Encryption")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-auth-enc`. Core framing logic of CCSDS Space Data Link Security Protocol (`sdls-auth-enc`) in Authenticated Encryption mode (encrypt-then-MAC), where `ground` and `satellite` exchange frames containing `(cat (sdl_header ...) header old_arsn (enc frame_data assumed_enc_key) (hash ... assumed_auth_key))` and advance the anti-replay sequence number via `(successor old_arsn)`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(frame_data tc)`, `(old_arsn seq_n)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) (hash (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) assumed_auth_key)))`
  - Role `satellite`: Vars: `(header text)`, `(frame_data tc)`, `(old_arsn seq_n)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc frame_data assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) (hash (sdl_header ground) header (successor old_arsn) (enc frame_data assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (1)**: `(sdl_header dest)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (tc atom) (successor hash))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-auth-enc`): `(vars (header text) (frame_data tc) (old_arsn seq_n) (assumed_enc_key assumed_auth_key skey) (ground spacecraft name))`, `(defstrandmax ground (header header) (frame_data frame_data) (old_arsn old_arsn) (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spacecraft spacecraft) (ground ground))`, `(non-orig assumed_enc_key assumed_auth_key)`, `(uniq-orig old_arsn)` | Skeleton 2 (`sdls-auth-enc`): `(vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name))`, `(defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_enc_key assumed_auth_key)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example for a clean, minimal pattern of Encrypt-then-MAC framing with monotonic sequence numbers `(successor old_arsn)` declared via `(lang (seq_n atom) (tc atom) (successor hash))`.
- **Key S-Expression Excerpt** (lines 1–38):
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
```

## sdls-auth-full-payload.scm

- **File Path**: `03_examples_scm/sdls-auth-full-payload.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP TC Baseline: Authentication Only (AES-CMAC): full SDLS-EP rekeying sequence")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-ep-chain-auth`. Full 6-step CCSDS SDLS-EP rekeying sequence (`sdls-ep-chain-auth`) in Authentication-Only (AES-CMAC) baseline mode, where PDUs and frame payloads are sent in cleartext accompanied by keyed MACs `(hash ... assumed_auth_key)` (except OTAR key upload encrypted under `keymaster` and the Key Verification challenge encryption `(enc chal sessionkey1)`).
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(old_arsn new_arsn seq_n)`, `(iv text)`, `(assumed_auth_key skey)`, `(ground spacecraft name)`, `(keymaster sessionkey1 sessionkey2 skey)`, `(keyid1 keyid2 keyid)`, `(spi spi)`, `(gvcid gvcid)`, `(chal text)`, `(frame_data tc)` | Role Assumptions: none | Trace (7 events): `(send (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor old_arsn)) (key_activation_pdu keyid1) (hash (sdl_header spacecraft) header (successor (successor old_arsn)) (key_activation_pdu keyid1) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (start_sa_pdu spi gvcid) (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (start_sa_pdu spi gvcid) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (keyver_cmd keyid1 chal) (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (keyver_cmd keyid1 chal) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (keyver_reply keyid1 chal sessionkey1) (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))` -> `(send (cat (sdl_header spacecraft) header (successor new_arsn) frame_data (hash (sdl_header spacecraft) header (successor new_arsn) frame_data sessionkey2)))`
  - Role `satellite`: Vars: `(header text)`, `(old_arsn new_arsn seq_n)`, `(iv text)`, `(assumed_auth_key skey)`, `(ground spacecraft name)`, `(keymaster sessionkey1 sessionkey2 skey)`, `(keyid1 keyid2 keyid)`, `(spi spi)`, `(gvcid gvcid)`, `(chal text)`, `(frame_data tc)` | Role Assumptions: none | Trace (7 events): `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor old_arsn)) (key_activation_pdu keyid1) (hash (sdl_header spacecraft) header (successor (successor old_arsn)) (key_activation_pdu keyid1) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) (hash (sdl_header spacecraft) header (successor (successor (successor old_arsn))) (rekey_sa_pdu spi keyid1 keyid2 new_arsn iv) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (start_sa_pdu spi gvcid) (hash (sdl_header spacecraft) header (successor (successor (successor (successor old_arsn)))) (start_sa_pdu spi gvcid) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (keyver_cmd keyid1 chal) (hash (sdl_header spacecraft) header (successor (successor (successor (successor (successor old_arsn))))) (keyver_cmd keyid1 chal) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (keyver_reply keyid1 chal sessionkey1) (hash (sdl_header ground) header (successor (successor (successor (successor (successor (successor old_arsn)))))) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))` -> `(recv (cat (sdl_header spacecraft) header (successor new_arsn) frame_data (hash (sdl_header spacecraft) header (successor new_arsn) frame_data sessionkey2)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (9)**: `(sdl_header dest)`, `(otar_pdu masterkeyid uploadblock)`, `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)`, `(otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)`, `(key_activation_pdu keyid)`, `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)`, `(start_sa_pdu spi gvcid)`, `(keyver_cmd keyid chal)`, `(keyver_reply keyid chal sessionkey)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (tc atom) (successor hash) (keyid atom) (keyid_of hash) (spi atom) (gvcid atom))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-ep-chain-auth`): `(vars (assumed_auth_key keymaster skey) (ground spacecraft name) (old_arsn new_arsn seq_n))`, `(defstrandmax satellite (assumed_auth_key assumed_auth_key) (keymaster keymaster) (old_arsn old_arsn) (new_arsn new_arsn) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_auth_key keymaster)`, `(facts (neq old_arsn new_arsn))`, `(non-orig keymaster)` | Skeleton 2 (`sdls-ep-chain-auth`): `(vars (assumed_auth_key keymaster sessionkey1 sessionkey2 skey) (ground spacecraft name) (old_arsn new_arsn seq_n) (chal text) (frame_data tc))`, `(defstrandmax ground (assumed_auth_key assumed_auth_key) (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2) (old_arsn old_arsn) (new_arsn new_arsn) (ground ground) (spacecraft spacecraft) (chal chal) (frame_data frame_data))`, `(non-orig assumed_auth_key keymaster)`, `(uniq-orig sessionkey1 sessionkey2)`, `(facts (neq old_arsn new_arsn))`, `(uniq-gen old_arsn)`, `(uniq-orig new_arsn chal frame_data sessionkey1 sessionkey2)`, `(non-orig keymaster)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `facts`, `herald`, `lang`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling authenticated-only (MAC/CMAC/HMAC) protocol framing and key rollovers where control headers and payloads are integrity-protected via `(hash ... auth_key)` while key transport remains encrypted.
- **Key S-Expression Excerpt** (lines 168–205):
```scheme
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
```

## sdls-auth-logic.scm

- **File Path**: `03_examples_scm/sdls-auth-logic.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP TC Baseline: Authentication Only (AES-CMAC)")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-tc-auth`. Models CCSDS SDLS Telecommand Baseline Authentication-Only mode (`sdls-tc-auth`) and includes a confidentiality `(defgoal sdls-tc-auth ...)` demonstrating the high-level goal predicates `(strand ground z1 2 ...)`, `(pnon assumed_auth_key)`, `(ugen old_arsn)`, `(uniq frame_data)`, and `(listener eve frame_data)`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(frame_data tc)`, `(old_arsn seq_n)`, `(assumed_auth_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) header (successor old_arsn) frame_data (hash (sdl_header spacecraft) header (successor old_arsn) frame_data assumed_auth_key)))` -> `(recv (cat (sdl_header ground) (successor (successor old_arsn)) frame_data (hash (sdl_header ground) (successor (successor old_arsn)) frame_data assumed_auth_key)))`
  - Role `satellite`: Vars: `(header text)`, `(frame_data tc)`, `(old_arsn seq_n)`, `(assumed_auth_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) header (successor old_arsn) frame_data (hash (sdl_header spacecraft) header (successor old_arsn) frame_data assumed_auth_key)))` -> `(send (cat (sdl_header ground) (successor (successor old_arsn)) frame_data (hash (sdl_header ground) (successor (successor old_arsn)) frame_data assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (1)**: `(sdl_header dest)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (tc atom) (successor hash))`
  - **Rules & Lemmas**: None
  - **Goals (1)**: `(defgoal sdls-tc-auth (forall ((ground spacecraft name) (assumed_auth_key skey) (frame_data tc) (old_arsn seq_n) (z1 eve strd)) (implies (and (strand ground z1 2 (ground ground) (spacecraft spacecraft) (old_arsn old_arsn) (frame_data frame_data) (assumed_auth_key assumed_auth_key)) (pnon assumed_auth_key) (ugen old_arsn) (uniq frame_data) (listener eve frame_data)) (false))) (comment "Confidentiality Goal: Adversary cannot learn telecommand"))`
  - **Skeletons (2)**: Skeleton 1 (`sdls-tc-auth`): `(vars (header text) (old_arsn seq_n) (assumed_auth_key skey) (frame_data tc) (ground spacecraft name))`, `(defstrandmax ground (old_arsn old_arsn) (assumed_auth_key assumed_auth_key) (frame_data frame_data) (spacecraft spacecraft))`, `(pen-non-orig assumed_auth_key)`, `(uniq-gen old_arsn)` | Skeleton 2 (`sdls-tc-auth`): `(vars (header text) (assumed_auth_key skey) (frame_data tc) (old_arsn seq_n) (ground spacecraft name))`, `(defstrandmax satellite (assumed_auth_key assumed_auth_key) (frame_data frame_data) (old_arsn old_arsn) (spacecraft spacecraft) (ground ground))`, `(pen-non-orig assumed_auth_key)`
  - **Keywords & Predicates Used**: `and`, `defgoal`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `false`, `forall`, `herald`, `implies`, `lang`, `listener`, `pen-non-orig`, `pnon`, `recv`, `send`, `strand`, `trace`, `ugen`, `uniq`, `uniq-gen`, `vars`
- **When to Reference This Example**: Reference this example to see the exact syntax of high-level security goal predicates (`strand`, `pnon`, `ugen`, `uniq`, `listener`) inside `(defgoal ...)` when testing whether an authentication-only protocol leaks `frame_data`.
- **Key S-Expression Excerpt** (lines 1–47):
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
```

## sdls-enc-logic.scm

- **File Path**: `03_examples_scm/sdls-enc-logic.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLSP Encryption")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-enc`. Models CCSDS SDLS Encryption-Only mode (`sdls-enc`) where `ground` and `satellite` exchange `(cat (sdl_header ...) (enc frame_data assumed_enc_key))` without a MAC or sequence number, using `(defstrandmax ground ...)` and `(defstrandmax satellite ...)` in the skeletons (with commented-out `defgoal` examples at the bottom).
- **Roles & Variables**:
  - Role `ground`: Vars: `(frame_data text)`, `(assumed_enc_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) (enc frame_data assumed_enc_key)))` -> `(recv (cat (sdl_header ground) (enc frame_data assumed_enc_key)))`
  - Role `satellite`: Vars: `(frame_data text)`, `(assumed_enc_key skey)`, `(ground spacecraft name)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) (enc frame_data assumed_enc_key)))` -> `(send (cat (sdl_header ground) (enc frame_data assumed_enc_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (1)**: `(sdl_header dest)`
  - **Rules & Lemmas**: None
  - **Goals**: None active (contains `;`-commented `(defgoal ...)` templates at the bottom of the file)
  - **Skeletons (2)**: Skeleton 1 (`sdls-enc`): `(vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))`, `(defstrandmax ground (frame_data frame_data) (assumed_enc_key assumed_enc_key) (spacecraft spacecraft) (ground ground))`, `(non-orig assumed_enc_key)` | Skeleton 2 (`sdls-enc`): `(vars (frame_data text) (assumed_enc_key skey) (ground spacecraft name))`, `(defstrandmax satellite (frame_data frame_data) (assumed_enc_key assumed_enc_key) (ground ground) (spacecraft spacecraft))`, `(uniq-orig frame_data)`, `(non-orig assumed_enc_key)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling basic symmetric payload encryption framing with header macros (`(defmacro (sdl_header dest) ...)`) and `(defstrandmax ...)` skeletons.
- **Key S-Expression Excerpt** (lines 1–35):
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

```

## sdls-ep-challenge-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-challenge-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Verification: Authentication Only")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-ep-key-verification-auth`. Models the standalone CCSDS SDLS-EP Key Verification challenge-response procedure in Authentication-Only mode (`sdls-ep-key-verification-auth`), where `ground` sends a signed/MACed challenge `(keyver_cmd keyid1 chal)` at `(successor old_arsn)` and `satellite` replies with `(keyver_reply keyid1 chal sessionkey1)` (containing `(enc chal sessionkey1)`) at `(successor (successor old_arsn))`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(old_arsn seq_n)`, `(assumed_auth_key skey)`, `(ground spacecraft name)`, `(keyid1 keyid)`, `(sessionkey1 skey)`, `(chal text)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) (hash (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) (hash (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))`
  - Role `satellite`: Vars: `(header text)`, `(old_arsn seq_n)`, `(assumed_auth_key skey)`, `(ground spacecraft name)`, `(keyid1 keyid)`, `(sessionkey1 skey)`, `(chal text)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) (hash (sdl_header spacecraft) header (successor old_arsn) (keyver_cmd keyid1 chal) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) (hash (sdl_header ground) header (successor (successor old_arsn)) (keyver_reply keyid1 chal sessionkey1) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (3)**: `(sdl_header dest)`, `(keyver_cmd keyid chal)`, `(keyver_reply keyid chal sessionkey)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (successor hash) (keyid atom))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-ep-key-verification-auth`): `(vars (assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid))`, `(defstrandmax satellite (assumed_auth_key assumed_auth_key) (sessionkey1 sessionkey1) (keyid1 keyid1) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_auth_key)`, `(pen-non-orig sessionkey1)` | Skeleton 2 (`sdls-ep-key-verification-auth`): `(vars (assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid) (chal text) (old_arsn seq_n))`, `(defstrandmax ground (assumed_auth_key assumed_auth_key) (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal) (ground ground) (spacecraft spacecraft) (old_arsn old_arsn))`, `(non-orig assumed_auth_key)`, `(pen-non-orig sessionkey1)`, `(uniq-orig chal)`, `(uniq-gen old_arsn)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `pen-non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling key-confirmation / challenge-response sub-protocols with sequence-number increments `(successor old_arsn)` and `(pen-non-orig sessionkey1)`.
- **Key S-Expression Excerpt** (lines 1–35):
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
```

## sdls-ep-challenge-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-challenge-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Verification: Authenticated Encryption")` | Flags: none
- **Protocol & Purpose**: Protocol(s): `sdls-ep-key-verification-auth-enc`. Models the standalone CCSDS SDLS-EP Key Verification challenge-response procedure in Authenticated Encryption mode (`sdls-ep-key-verification-auth-enc`), where the key verification command and reply PDUs are both encrypted under `assumed_enc_key` and MACed under `assumed_auth_key`.
- **Roles & Variables**:
  - Role `ground`: Vars: `(header text)`, `(old_arsn seq_n)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)`, `(keyid1 keyid)`, `(sessionkey1 skey)`, `(chal text)` | Role Assumptions: none | Trace (2 events): `(send (cat (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))` -> `(recv (cat (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) (hash (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite`: Vars: `(header text)`, `(old_arsn seq_n)`, `(assumed_enc_key assumed_auth_key skey)`, `(ground spacecraft name)`, `(keyid1 keyid)`, `(sessionkey1 skey)`, `(chal text)` | Role Assumptions: none | Trace (2 events): `(recv (cat (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (keyver_cmd keyid1 chal) assumed_enc_key) assumed_auth_key)))` -> `(send (cat (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) (hash (sdl_header ground) header (successor old_arsn) (enc (keyver_reply keyid1 chal sessionkey1) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Macros (3)**: `(sdl_header dest)`, `(keyver_cmd keyid chal)`, `(keyver_reply keyid chal sessionkey)`
  - **Custom Language Declarations (`lang`)**: `(lang (seq_n atom) (successor hash) (keyid atom))`
  - **Rules & Lemmas**: None
  - **Goals**: None
  - **Skeletons (2)**: Skeleton 1 (`sdls-ep-key-verification-auth-enc`): `(vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid))`, `(defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (sessionkey1 sessionkey1) (keyid1 keyid1) (ground ground) (spacecraft spacecraft))`, `(non-orig assumed_enc_key assumed_auth_key)`, `(pen-non-orig sessionkey1)` | Skeleton 2 (`sdls-ep-key-verification-auth-enc`): `(vars (assumed_enc_key assumed_auth_key skey) (ground spacecraft name) (sessionkey1 skey) (keyid1 keyid) (chal text) (old_arsn seq_n))`, `(defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal) (ground ground) (spacecraft spacecraft) (old_arsn old_arsn))`, `(non-orig assumed_enc_key assumed_auth_key)`, `(pen-non-orig sessionkey1)`, `(uniq-orig chal)`, `(uniq-orig old_arsn)`
  - **Keywords & Predicates Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `pen-non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
- **When to Reference This Example**: Reference this example when modeling nested key confirmation inside an already-established authenticated encryption tunnel (`assumed_enc_key` + `assumed_auth_key`).
- **Key S-Expression Excerpt** (lines 1–35):
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
```
````

---

### `refrences/cpsa_kb/04_examples_catalog/03_scm_examples_SDLS_to_Z.md`

*sha256:`89d203a2f7a8` · 3212 lines · 217.0 KB (~55,546 tokens) · lang:`markdown`*

````markdown
# Official MITRE CPSA Examples Catalog (Part 3: sdls-ep-challenge.scm to yes-or-no.scm)

This catalog documents the 48 official MITRE CPSA `.scm` example files in alphabetical slice `[100:148]` (`sdls-ep-challenge.scm` through `yes-or-no.scm`). Every declaration, role, variable sort, trace event, macro, rule, goal, and skeleton is extracted directly from the source `.scm` files.

## sdls-ep-challenge.scm

- **File Path**: `03_examples_scm/sdls-ep-challenge.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Verification")` | Flags: none | Custom `lang`: `(lang (keyid atom))`
- **Protocol & Purpose**: Models the Space Data Link Security Extended Procedures (SDLS-EP) Key Verification procedure (Command PDU Figure 5-7 p.5-10 and Reply PDU Figure 5-8 p.5-11, Recipient steps 3.2.3.5.3.4 and .3.5 p.3-12). The ground station sends a challenge `chal` paired with a custom-sorted key identifier `keyid1`, and the satellite replies with `chal` encrypted under `sessionkey1`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-key-verification`):
    - `vars`: `(keyid1 keyid), (sessionkey1 skey), (chal text)` | Role assumptions: none
    - `trace`: `(send (keyver_cmd keyid1 chal))` -> `(recv (keyver_reply keyid1 chal sessionkey1))`
  - Role `satellite` (in `sdls-ep-key-verification`):
    - `vars`: `(keyid1 keyid), (sessionkey1 skey), (chal text)` | Role assumptions: none
    - `trace`: `(recv (keyver_cmd keyid1 chal))` -> `(send (keyver_reply keyid1 chal sessionkey1))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `pen-non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(keyver_cmd keyid chal)` -> `(cat "ep-pdu" "tag:00-0100-cmd" keyid chal)`; `(keyver_reply keyid chal sessionkey)` -> `(cat "ep-pdu" "tag:00-0100-reply" keyid (enc chal sessionkey))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-key-verification (vars (sessionkey1 skey) (keyid1 keyid) (chal text)) (defstrandmax ground (sessionkey1 sessionkey1) (keyid1 keyid1) (chal chal)) (pen-non-orig sessionkey1) (uniq-orig chal) (comment "Initiator's view"))`
    - `(defskeleton sdls-ep-key-verification (vars (sessionkey1 skey) (keyid1 keyid)) (defstrandmax satellite (sessionkey1 sessionkey1) (keyid1 keyid1)) (pen-non-orig sessionkey1) (comment "Recipient's view of Key Verification"))`
- **When to Reference This Example**: Reference this example when modeling challenge-response key verification PDUs using `(defmacro ...)` for packet tags, custom atomic sorts via `(lang (keyid atom))`, and `(pen-non-orig ...)` for symmetric session keys.
- **Key S-Expression Excerpt**:
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

```

## sdls-ep-key-activation-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-key-activation-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Activation: Authentication Only")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (keyid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Key Activation command with Authentication Only protection. The `ground` role sends a frame containing the Space Data Link header (`sdl_header`), sequence number `(successor old_arsn)`, Key Activation PDU (`key_activation_pdu`), and a keyed MAC modeled as `(hash ... assumed_auth_key)` to `satellite`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-key-activation-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (keyid1 keyid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) (hash (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-key-activation-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (keyid1 keyid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) (hash (sdl_header spacecraft) header (successor old_arsn) (key_activation_pdu keyid1) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len")`; `(key_activation_pdu keyid)` -> `(cat "ep-pdu" "tag:00-0010" keyid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-key-activation-auth (vars (assumed_auth_key skey) (spacecraft name) (keyid1 keyid)) (defstrandmax satellite (assumed_auth_key assumed_auth_key) (keyid1 keyid1) (spacecraft spacecraft)) (non-orig assumed_auth_key) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-key-activation-auth (vars (assumed_auth_key skey) (spacecraft name) (keyid1 keyid) (old_arsn seq_n)) (defstrandmax ground (assumed_auth_key assumed_auth_key) (keyid1 keyid1) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_auth_key) (uniq-gen old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling authenticated unencrypted command frames with anti-replay sequence numbers (`(lang (seq_n atom) (successor hash) (keyid atom))`) and keyed hash MACs.
- **Key S-Expression Excerpt**:
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
```

## sdls-ep-key-activation-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-key-activation-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Activation: Authenticated Encryption")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (keyid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Key Activation command under Authenticated Encryption (Encrypt-then-MAC). The Key Activation PDU is encrypted under `assumed_enc_key`, concatenated with the SDL header and sequence number `old_arsn`, and authenticated with a keyed hash using `assumed_auth_key`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-key-activation-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (keyid1 keyid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-key-activation-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (keyid1 keyid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (key_activation_pdu keyid1) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number")`; `(key_activation_pdu keyid)` -> `(cat "ep-pdu" "tag:00-0010" keyid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-key-activation-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keyid1 keyid)) (defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keyid1 keyid1) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-key-activation-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keyid1 keyid) (old_arsn seq_n)) (defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keyid1 keyid1) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_enc_key assumed_auth_key) (uniq-orig old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling Encrypt-then-MAC authenticated encryption framing with separate encryption and authentication symmetric keys (`assumed_enc_key`, `assumed_auth_key`).
- **Key S-Expression Excerpt**:
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
```

## sdls-ep-key-activation.scm

- **File Path**: `03_examples_scm/sdls-ep-key-activation.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Key Activation")` | Flags: none | Custom `lang`: `(lang (keyid atom))`
- **Protocol & Purpose**: Models the bare SDLS-EP Key Activation Command PDU without link-layer framing or cryptographic wrapping. As noted in the comments, key database state (5.4.1.2 p.5-5) is not modeled and no reply PDU exists for Key Activation (5.4.2.2.1, p.5-7).
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-key-activation`):
    - `vars`: `(keyid1 keyid)` | Role assumptions: none
    - `trace`: `(send (key_activation_pdu keyid1))`
  - Role `satellite` (in `sdls-ep-key-activation`):
    - `vars`: `(keyid1 keyid)` | Role assumptions: none
    - `trace`: `(recv (key_activation_pdu keyid1))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `recv`, `send`, `trace`, `vars`
  - **Macros (1)**: `(key_activation_pdu keyid)` -> `(cat "ep-pdu" "tag:00-0010" keyid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-key-activation (vars (keyid1 keyid)) (defstrandmax satellite (keyid1 keyid1)) (comment "Recipient's view"))`
    - `(defskeleton sdls-ep-key-activation (vars (keyid1 keyid)) (defstrandmax ground (keyid1 keyid1)) (comment "Initiator's view"))`
- **When to Reference This Example**: Reference this example as a minimal baseline for one-way unauthenticated command PDUs using `(defmacro ...)` and `(lang (keyid atom))`.
- **Key S-Expression Excerpt**:
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

## sdls-ep-otar-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-otar-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP OTAR: Authentication Only")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (keyid atom) (keyid_of hash))`
- **Protocol & Purpose**: Models SDLS-EP Over-the-Air Rekeying (OTAR) with Authentication Only link protection. The OTAR payload encrypts a block of new session keys and their key IDs (`keyid1`, `sessionkey1`, `keyid2`, `sessionkey2`) under `keymaster` (identified by `(keyid_of keymaster)`), while the outer frame is authenticated with `assumed_auth_key` and sequence number `(successor old_arsn)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-otar-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-otar-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) (hash (sdl_header spacecraft) header (successor old_arsn) (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros (4)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len")`; `(otar_pdu masterkeyid uploadblock)` -> `(cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock)`; `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)` -> `(cat keyid1 sessionkey1 keyid2 sessionkey2)`; `(otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)` -> `(otar_pdu (keyid_of keymaster) (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-otar-auth (vars (assumed_auth_key skey) (spacecraft name) (keymaster skey)) (defstrandmax satellite (assumed_auth_key assumed_auth_key) (keymaster keymaster) (spacecraft spacecraft)) (non-orig assumed_auth_key keymaster) (non-orig keymaster) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-otar-auth (vars (assumed_auth_key skey) (spacecraft name) (keymaster sessionkey1 sessionkey2 skey) (old_arsn seq_n)) (defstrandmax ground (assumed_auth_key assumed_auth_key) (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_auth_key keymaster) (uniq-orig sessionkey1 sessionkey2) (non-orig keymaster) (uniq-gen old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling key transport / over-the-air rekeying where a master key wraps multiple session keys inside an outer MAC-authenticated frame and key identifiers are functionally bound to keys via `(lang ... (keyid_of hash))`.
- **Key S-Expression Excerpt**:
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
```

## sdls-ep-otar-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-otar-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP OTAR: Authenticated Encryption")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (keyid atom) (keyid_of hash))`
- **Protocol & Purpose**: Models SDLS-EP Over-the-Air Rekeying (OTAR) with Authenticated Encryption link protection. The OTAR payload (which itself encrypts `keyid1`, `sessionkey1`, `keyid2`, `sessionkey2` under `keymaster`) is nested inside an outer link-layer encryption under `assumed_enc_key` and authenticated with `assumed_auth_key`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-otar-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-otar-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (4)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number")`; `(otar_pdu masterkeyid uploadblock)` -> `(cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock)`; `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)` -> `(cat keyid1 sessionkey1 keyid2 sessionkey2)`; `(otar_payload keymaster keyid1 sessionkey1 keyid2 sessionkey2)` -> `(otar_pdu (keyid_of keymaster) (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-otar-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keymaster skey)) (defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keymaster keymaster) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key keymaster) (non-orig keymaster) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-otar-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (keymaster sessionkey1 sessionkey2 skey) (old_arsn seq_n)) (defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_enc_key assumed_auth_key keymaster) (uniq-orig sessionkey1 sessionkey2) (non-orig keymaster) (uniq-orig old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling nested key-wrapping inside an Encrypt-then-MAC link layer with functional key-ID binding `(keyid_of keymaster)`.
- **Key S-Expression Excerpt**:
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
```

## sdls-ep-otar-transmission.scm

- **File Path**: `03_examples_scm/sdls-ep-otar-transmission.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Over-the-Air Rekeying (OTAR)")` | Flags: none | Custom `lang`: `(lang (keyid atom) (keyid_of hash))`
- **Protocol & Purpose**: Models the standalone SDLS-EP Over-the-Air Rekeying (OTAR) command PDU (Figure 5-3 p.5-6; Initiator steps 3.2.3.1.3.2–.3, Recipient step 3.2.3.1.3.4) without outer link-layer framing. The ground station sends `(keyid_of keymaster)` and the encrypted key upload block `(enc (otar_upload_block ...) keymaster)` to the satellite.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-otar`):
    - `vars`: `(keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(send (otar_pdu (keyid_of keymaster) (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))`
  - Role `satellite` (in `sdls-ep-otar`):
    - `vars`: `(keymaster sessionkey1 sessionkey2 skey), (keyid1 keyid2 keyid)` | Role assumptions: none
    - `trace`: `(recv (otar_pdu (keyid_of keymaster) (enc (otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2) keymaster)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(otar_pdu masterkeyid uploadblock)` -> `(cat "ep-pdu" "tag:00-0001" masterkeyid uploadblock)`; `(otar_upload_block keyid1 sessionkey1 keyid2 sessionkey2)` -> `(cat keyid1 sessionkey1 keyid2 sessionkey2)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-otar (vars (keymaster skey)) (defstrandmax satellite (keymaster keymaster)) (non-orig keymaster) (comment "Recipient's view of OTAR"))`
    - `(defskeleton sdls-ep-otar (vars (keymaster sessionkey1 sessionkey2 skey)) (defstrandmax ground (keymaster keymaster) (sessionkey1 sessionkey1) (sessionkey2 sessionkey2)) (non-orig keymaster) (uniq-orig sessionkey1 sessionkey2) (comment "Initiator's view of OTAR"))`
- **When to Reference This Example**: Reference this example when modeling standalone key-upload PDUs where key identifiers sit inside the encrypted payload and a functional hash `(keyid_of hash)` maps keys to their public identifiers.
- **Key S-Expression Excerpt**:
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


```

## sdls-ep-sa-rekey-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-rekey-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Rekey SA: Authentication Only")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (spi atom) (keyid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Rekey Security Association (SA) command with Authentication Only link protection. The `ground` station sends a frame containing the SDL header, `(successor old_arsn)`, the Rekey SA PDU (`spi`, `enckeyid`, `authkeyid`, `new_arsn`, `iv`), and a keyed hash under `assumed_auth_key`, with `(facts (neq old_arsn new_arsn))` distinguishing the old and new anti-replay sequence numbers.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-rekey-sa-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) (hash (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-rekey-sa-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) (hash (sdl_header spacecraft) header (successor old_arsn) (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `facts`, `herald`, `lang`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len")`; `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)` -> `(cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-rekey-sa-auth (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n)) (defstrandmax satellite (assumed_auth_key assumed_auth_key) (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn) (old_arsn old_arsn) (spacecraft spacecraft)) (non-orig assumed_auth_key) (facts (neq old_arsn new_arsn)) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-rekey-sa-auth (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n)) (defstrandmax ground (assumed_auth_key assumed_auth_key) (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn) (old_arsn old_arsn) (spacecraft spacecraft)) (non-orig assumed_auth_key) (uniq-orig new_arsn) (facts (neq old_arsn new_arsn)) (uniq-gen old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling SA rekeying commands with multiple custom atomic sorts (`seq_n`, `spi`, `keyid`) and inequality facts `(facts (neq old_arsn new_arsn))` in skeletons.
- **Key S-Expression Excerpt**:
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

```

## sdls-ep-sa-rekey-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-rekey-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Rekey SA: Authenticated Encryption")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (spi atom) (keyid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Rekey SA command under Authenticated Encryption. The Rekey SA PDU (`spi`, `enckeyid`, `authkeyid`, `new_arsn`, `iv`) is encrypted under `assumed_enc_key` and MAC-authenticated under `assumed_auth_key`, with `(facts (neq old_arsn new_arsn))` enforced in the skeletons.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-rekey-sa-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-rekey-sa-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `facts`, `herald`, `lang`, `neq`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number")`; `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)` -> `(cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-rekey-sa-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n)) (defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn) (old_arsn old_arsn) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key) (facts (neq old_arsn new_arsn)) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-rekey-sa-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (enckeyid authkeyid keyid) (old_arsn new_arsn seq_n)) (defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn) (old_arsn old_arsn) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key) (uniq-orig new_arsn) (facts (neq old_arsn new_arsn)) (uniq-orig old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling encrypted and authenticated SA rekeying frames that update sequence numbers and IVs while enforcing `(facts (neq old_arsn new_arsn))`.
- **Key S-Expression Excerpt**:
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
```

## sdls-ep-sa-rekey.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-rekey.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Rekey SA")` | Flags: none | Custom `lang`: `(lang (spi atom) (keyid atom) (seq_n atom))`
- **Protocol & Purpose**: Models the bare SDLS-EP Rekey SA PDU (Figure 5-14 p.5-16, field order per 5.5.1.4.2.2, Initiator 3.3.3.3.3.2–.3, Recipient 3.3.3.3.3.4) without outer link framing. Transmits `spi`, `enckeyid`, `authkeyid`, `new_arsn`, and `iv` in cleartext.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-rekey-sa`):
    - `vars`: `(spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(send (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv))`
  - Role `satellite` (in `sdls-ep-rekey-sa`):
    - `vars`: `(spi spi), (enckeyid authkeyid keyid), (new_arsn seq_n), (iv text)` | Role assumptions: none
    - `trace`: `(recv (rekey_sa_pdu spi enckeyid authkeyid new_arsn iv))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (1)**: `(rekey_sa_pdu spi enckeyid authkeyid new_arsn iv)` -> `(cat "ep-pdu" "tag:01-0110" spi enckeyid authkeyid new_arsn iv)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-rekey-sa (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n)) (defstrandmax satellite (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn)) (comment "Recipient's view"))`
    - `(defskeleton sdls-ep-rekey-sa (vars (spi spi) (enckeyid authkeyid keyid) (new_arsn seq_n)) (defstrandmax ground (spi spi) (enckeyid enckeyid) (authkeyid authkeyid) (new_arsn new_arsn)) (uniq-orig new_arsn) (comment "Initiator's view."))`
- **When to Reference This Example**: Reference this example when defining custom protocol field sorts (`(lang (spi atom) (keyid atom) (seq_n atom))`) for unframed security association management PDUs.
- **Key S-Expression Excerpt**:
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

## sdls-ep-sa-start-auth.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-start-auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Start SA: Authentication Only")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (spi atom) (gvcid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Start SA command with Authentication Only protection. Sends the Start SA PDU (`spi` and Global Virtual Channel ID `gvcid`) alongside `(successor old_arsn)` and a keyed hash MAC under `assumed_auth_key`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-start-sa-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) (hash (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-start-sa-auth`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_auth_key skey), (spacecraft name), (spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) (hash (sdl_header spacecraft) header (successor old_arsn) (start_sa_pdu spi gvcid) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len")`; `(start_sa_pdu spi gvcid)` -> `(cat "ep-pdu" "tag:01-1011" spi gvcid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-start-sa-auth (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid)) (defstrandmax satellite (assumed_auth_key assumed_auth_key) (spi spi) (gvcid gvcid) (spacecraft spacecraft)) (non-orig assumed_auth_key) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-start-sa-auth (vars (assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid) (old_arsn seq_n)) (defstrandmax ground (assumed_auth_key assumed_auth_key) (spi spi) (gvcid gvcid) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_auth_key) (uniq-gen old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling authenticated SA activation/start commands binding a Security Parameter Index (`spi`) to a channel identifier (`gvcid`).
- **Key S-Expression Excerpt**:
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
```

## sdls-ep-sa-start-authenc.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-start-authenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Start SA: Authenticated Encryption")` | Flags: none | Custom `lang`: `(lang (seq_n atom) (successor hash) (spi atom) (gvcid atom))`
- **Protocol & Purpose**: Models the SDLS-EP Start SA command with Authenticated Encryption. Encrypts `(start_sa_pdu spi gvcid)` under `assumed_enc_key` and authenticates the frame (including `old_arsn`) with a keyed hash under `assumed_auth_key`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-start-sa-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(send (cat (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))`
  - Role `satellite` (in `sdls-ep-start-sa-auth-enc`):
    - `vars`: `(header text), (old_arsn seq_n), (assumed_enc_key assumed_auth_key skey), (spacecraft name), (spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(recv (cat (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) (hash (sdl_header spacecraft) header old_arsn (enc (start_sa_pdu spi gvcid) assumed_enc_key) assumed_auth_key)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(sdl_header dest)` -> `(cat "ver" "bypass flag" "control command flag" "Reserved Spare" dest "VCID" "Frame len" "Frame Sequence Number")`; `(start_sa_pdu spi gvcid)` -> `(cat "ep-pdu" "tag:01-1011" spi gvcid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-start-sa-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid)) (defstrandmax satellite (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spi spi) (gvcid gvcid) (spacecraft spacecraft)) (non-orig assumed_enc_key assumed_auth_key) (comment "Satellite point of view"))`
    - `(defskeleton sdls-ep-start-sa-auth-enc (vars (assumed_enc_key assumed_auth_key skey) (spacecraft name) (spi spi) (gvcid gvcid) (old_arsn seq_n)) (defstrandmax ground (assumed_enc_key assumed_enc_key) (assumed_auth_key assumed_auth_key) (spi spi) (gvcid gvcid) (spacecraft spacecraft) (old_arsn old_arsn)) (non-orig assumed_enc_key assumed_auth_key) (uniq-orig old_arsn) (comment "Ground-station point of view"))`
- **When to Reference This Example**: Reference this example when modeling Encrypt-then-MAC SA start commands with custom atomic sorts `spi`, `gvcid`, and `seq_n`.
- **Key S-Expression Excerpt**:
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
```

## sdls-ep-sa-start.scm

- **File Path**: `03_examples_scm/sdls-ep-sa-start.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "SDLS-EP Start SA")` | Flags: none | Custom `lang`: `(lang (spi atom) (gvcid atom))`
- **Protocol & Purpose**: Models the bare SDLS-EP Start SA PDU (p.5-14, Tag 01,1011, fields per 5.5.1.2.2.2) with one mandatory `spi` and one `gvcid`, assuming the SA precondition (Keyed state) without link-layer framing.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `ground` (in `sdls-ep-start-sa`):
    - `vars`: `(spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(send (start_sa_pdu spi gvcid))`
  - Role `satellite` (in `sdls-ep-start-sa`):
    - `vars`: `(spi spi), (gvcid gvcid)` | Role assumptions: none
    - `trace`: `(recv (start_sa_pdu spi gvcid))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `lang`, `recv`, `send`, `trace`, `vars`
  - **Macros (1)**: `(start_sa_pdu spi gvcid)` -> `(cat "ep-pdu" "tag:01-1011" spi gvcid)`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sdls-ep-start-sa (vars (spi spi) (gvcid gvcid)) (defstrandmax satellite (spi spi) (gvcid gvcid)) (comment "Recipient's view"))`
    - `(defskeleton sdls-ep-start-sa (vars (spi spi) (gvcid gvcid)) (defstrandmax ground (spi spi) (gvcid gvcid)) (comment "Initiator's view"))`
- **When to Reference This Example**: Reference this example as a minimal template for unframed SA management PDUs using custom atomic sorts `(lang (spi atom) (gvcid atom))`.
- **Key S-Expression Excerpt**:
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

## sigenc.scm

- **File Path**: `03_examples_scm/sigenc.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Signed Encrypted Message Example" (comment "Shows examples of key usage of asymmetric keys"))` | Flags: `(comment "Shows examples of key usage of asymmetric keys")`
- **Protocol & Purpose**: Demonstrates asymmetric key separation in a 3-message challenge-response protocol (`mult-keys-sig-enc`) where principals use distinct tagged key pairs for signing (`(privk "sig" a)`) and encryption (`(pubk "enc" b)`). Four skeletons compare the responder's authentication guarantees when trusting only `a`'s signature key, only `a`'s encryption key, or both.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `mult-keys-sig-enc`):
    - `vars`: `(a b name), (n1 n2 text)` | Role assumptions: none
    - `trace`: `(send (enc (enc n1 a (privk "sig" a)) (pubk "enc" b)))` -> `(recv (enc (enc n1 n2 (privk "sig" b)) (pubk "enc" a)))` -> `(send (enc (enc n2 (privk "sig" a)) (pubk "enc" b)))`
  - Role `resp` (in `mult-keys-sig-enc`):
    - `vars`: `(b a name), (n2 n1 text)` | Role assumptions: none
    - `trace`: `(recv (enc (enc n1 a (privk "sig" a)) (pubk "enc" b)))` -> `(send (enc (enc n1 n2 (privk "sig" b)) (pubk "enc" a)))` -> `(recv (enc (enc n2 (privk "sig" a)) (pubk "enc" b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton mult-keys-sig-enc (vars (a b name) (n1 text)) (defstrand init 3 (a a) (b b) (n1 n1)) (non-orig (privk "enc" a) (privk "sig" a) (privk "enc" b)) (uniq-orig n1))`
    - `(defskeleton mult-keys-sig-enc (vars (a b name) (n2 text)) (defstrand resp 3 (a a) (b b) (n2 n2)) (non-orig (privk "sig" a)) (uniq-orig n2))`
    - `(defskeleton mult-keys-sig-enc (vars (a b name) (n2 text)) (defstrand resp 3 (a a) (b b) (n2 n2)) (non-orig (privk "enc" a)) (uniq-orig n2))`
    - `(defskeleton mult-keys-sig-enc (vars (a b name) (n2 text)) (defstrand resp 3 (a a) (b b) (n2 n2)) (non-orig (privk "sig" a) (privk "enc" a)) (uniq-orig n2))`
- **When to Reference This Example**: Reference this example when separating signing and encryption asymmetric keys using string-tagged `(privk "sig" a)` / `(pubk "enc" b)` to prevent cross-key-usage attacks.
- **Key S-Expression Excerpt**:
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
```

## sorted_epmo_acctnum.scm

- **File Path**: `03_examples_scm/sorted_epmo_acctnum.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Electronic Purchase with Money Order Protocol Variant" (bound 12) (comment "This version includes account numbers in exchanges" "This version uses sorts to avoid confusion" "between a nonce and other data"))` | Flags: `(bound 12)`, `(comment "This version includes account numbers in exchanges" "This version uses sorts to avoid confusion" "between a nonce and other data")`
- **Protocol & Purpose**: Models a variant of the Electronic Purchase with Money Order (EPMO) protocol (`sorted_epmo_acctnum`) between `customer`, `merchant`, and `bank` that includes account numbers (`acctnum`), uses sorts (`data` for nonces `nc`, `nm`, `nb` vs. `text` for `acctnum`, `goods`, `price`) to avoid type confusion, models hashing as `(enc "hash" ... (pubk hash))` with `(non-orig (privk hash))`, and attaches formal trust-management `(annotations ...)` using `says`, `implies`, `forall`, and `exists`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `bank` (in `sorted_epmo_acctnum`):
    - `vars`: `(b c m name), (acctnum price text), (hash name), (nc nm nb data)` | Role assumptions/annotations: `(non-orig (privk hash))`, `(annotations b (1 (forall ((pm name)) (implies (and (authtransfer c acctnum b price pm nm) (reqtransfer pm b price pm nm)) (dotransfer acctnum b price pm nm)))) (2 (and (says c (authtransfer c acctnum b price m nm)) (says m (reqtransfer m b price m nm)))))`
    - `trace`: `(recv (enc c nc nm acctnum price (pubk b)))` -> `(send (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b)) (enc nc nb (pubk c))))` -> `(recv (enc (enc "hash" b m nb nm (pubk hash)) (privk m)))`
  - Role `customer` (in `sorted_epmo_acctnum`):
    - `vars`: `(b c m hash name), (acctnum goods price text), (nc nm nb data)` | Role assumptions/annotations: `(non-orig (privk b) (privk hash))`, `(uniq-orig nc)`, `(annotations c (1 (says m (implies (exists ((acctnum2 text)) (dotransfer acctnum2 b price m nm)) (doship m goods c)))) (3 (says b (forall ((pm name)) (implies (and (authtransfer c acctnum b price m nm) (reqtransfer pm b price pm nm)) (dotransfer acctnum b price pm nm))))) (4 (authtransfer c acctnum b price m nm)))`
    - `trace`: `(send (enc c nc goods (pubk m)))` -> `(recv (enc nc nm m price (pubk c)))` -> `(send (enc c nc nm acctnum price (pubk b)))` -> `(recv (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b)) (enc nc nb (pubk c))))` -> `(send (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b)) nb))`
  - Role `merchant` (in `sorted_epmo_acctnum`):
    - `vars`: `(b c m hash name), (goods price text), (nc nm nb data)` | Role assumptions/annotations: `(non-orig (privk hash))`, `(uniq-orig nm)`, `(annotations m (1 (implies (exists ((acctnum2 text)) (dotransfer acctnum2 b price m nm)) (doship m goods c))) (2 (and (says b (forall ((pm name)) (exists ((acctnum2 text)) (implies (and (authtransfer c acctnum2 b price m nm) (reqtransfer pm b price pm nm)) (dotransfer acctnum2 b price pm nm))))) (says c (exists ((acctnum2 text)) (authtransfer c acctnum2 b price m nm))))) (3 (and (reqtransfer m b price m nm) (doship m goods c))))`
    - `trace`: `(recv (enc c nc goods (pubk m)))` -> `(send (enc nc nm m price (pubk c)))` -> `(recv (cat (enc (enc "hash" c nc nb nm price (pubk hash)) (privk b)) nb))` -> `(send (enc (enc "hash" b m nb nm (pubk hash)) (privk m)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `and`, `annotations`, `bound`, `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `exists`, `forall`, `herald`, `implies`, `non-orig`, `recv`, `says`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton sorted_epmo_acctnum (vars (b m c name) (nm nc nb data) (hash name)) (defstrand merchant 4 (b b) (m m) (c c) (nm nm) (nc nc) (nb nb) (hash hash)) (non-orig (privk b) (privk m) (privk c) (privk hash)) (uniq-orig nm nc nb))`
    - `(defskeleton sorted_epmo_acctnum (vars (b m c name) (nm nb nc data) (hash name) (price acctnum text)) (defstrand bank 3 (b b) (m m) (c c) (nm nm) (nb nb) (nc nc) (hash hash)) (non-orig (privk b) (privk m) (privk c) (privk hash)) (uniq-orig nm nc nb))`
- **When to Reference This Example**: Reference this example when using sort separation (`data` vs `text`) to prevent type-flaw attacks in multi-party payment protocols, or when attaching logical `(annotations ...)` to roles.
- **Key S-Expression Excerpt**:
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
```

## sts.scm

- **File Path**: `03_examples_scm/sts.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "Station-to-station protocol" (bound 20) (algebra diffie-hellman))` | Flags: `(bound 20)`, `(algebra diffie-hellman)`
- **Protocol & Purpose**: Models the classic Station-to-Station (STS) authenticated Diffie-Hellman key exchange protocol (`station-to-station`) in the `diffie-hellman` algebra, where both `init` and `resp` include role-level `(uniq-gen x)` / `(uniq-gen y)` assumptions and a fourth event `(send (privk a))` / `(send (privk b))` used in forward-secrecy skeletons.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `station-to-station`):
    - `vars`: `(x rndx), (eta expt), (a b name)` | Role assumptions/annotations: `(uniq-gen x)`
    - `trace`: `(send (exp (gen) x))` -> `(recv (cat (exp (gen) eta) (enc (enc (exp (gen) eta) (exp (gen) x) (privk b)) (exp (exp (gen) eta) x))))` -> `(send (enc (enc (exp (gen) x) (exp (gen) eta) (privk a)) (exp (exp (gen) eta) x)))` -> `(send (privk a))`
  - Role `resp` (in `station-to-station`):
    - `vars`: `(y rndx), (chi expt), (a b name)` | Role assumptions/annotations: `(uniq-gen y)`
    - `trace`: `(recv (exp (gen) chi))` -> `(send (cat (exp (gen) y) (enc (enc (exp (gen) y) (exp (gen) chi) (privk b)) (exp (exp (gen) chi) y))))` -> `(recv (enc (enc (exp (gen) chi) (exp (gen) y) (privk a)) (exp (exp (gen) chi) y)))` -> `(send (privk b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `algebra`, `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (6)**:
    - `(defskeleton station-to-station (vars (a b name)) (defstrand init 3 (a a) (b b)) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station (vars (a b name)) (defstrand resp 3 (a a) (b b)) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-to-station (vars (a b name) (x y rndx) (eta expt)) (defstrand init 3 (a a) (b b) (x x) (eta eta)) (deflistener (exp (exp (gen) eta) x)) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station (vars (a b name) (x y rndx) (chi expt)) (defstrand resp 3 (a a) (b b) (y y) (chi chi)) (deflistener (exp (exp (gen) chi) y)) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-to-station (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (deflistener (exp (gen) (mul x y))) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig (privk b) (privk a)))`
- **When to Reference This Example**: Reference this example when modeling authenticated Diffie-Hellman key exchange (STS) and testing Perfect Forward Secrecy (PFS) by exposing long-term private keys after session completion (`defstrand init 4` with `deflistener (exp (gen) (mul x y))`).
- **Key S-Expression Excerpt**:
```scheme
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

```

## sts_non_role.scm

- **File Path**: `03_examples_scm/sts_non_role.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "Station-to-station protocol:  Weakened version" (bound 20) (algebra diffie-hellman))` | Flags: `(bound 20)`, `(algebra diffie-hellman)`
- **Protocol & Purpose**: Models a weakened version of the Station-to-Station protocol (`station-weak`) in the `diffie-hellman` algebra where `(uniq-gen x)` and `(uniq-gen y)` are commented out at the role level and instead asserted only in individual skeletons.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `station-weak`):
    - `vars`: `(x rndx), (eta expt), (a b name)` | Role assumptions: none
    - `trace`: `(send (exp (gen) x))` -> `(recv (cat (exp (gen) eta) (enc (enc (exp (gen) eta) (exp (gen) x) (privk b)) (exp (exp (gen) eta) x))))` -> `(send (enc (enc (exp (gen) x) (exp (gen) eta) (privk a)) (exp (exp (gen) eta) x)))` -> `(send (privk a))`
  - Role `resp` (in `station-weak`):
    - `vars`: `(y rndx), (chi expt), (a b name)` | Role assumptions: none
    - `trace`: `(recv (exp (gen) chi))` -> `(send (cat (exp (gen) y) (enc (enc (exp (gen) y) (exp (gen) chi) (privk b)) (exp (exp (gen) chi) y))))` -> `(recv (enc (enc (exp (gen) chi) (exp (gen) y) (privk a)) (exp (exp (gen) chi) y)))` -> `(send (privk b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `algebra`, `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (7)**:
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand init 3 (a a) (b b) (x x) (eta y)) (uniq-gen x y) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand resp 3 (a a) (b b) (y y) (chi x)) (uniq-gen x y) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand init 3 (a a) (b b) (x x) (eta y)) (deflistener (exp (exp (gen) y) x)) (uniq-gen x y) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-weak (vars (a b name) (x rndx) (eta expt)) (defstrand init 3 (a a) (b b) (x x) (eta eta)) (deflistener (exp (exp (gen) eta) x)) (uniq-gen x) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-weak (vars (a b name) (y rndx) (chi expt)) (defstrand resp 3 (a a) (b b) (y y) (chi chi)) (deflistener (exp (exp (gen) chi) y)) (non-orig (privk a) (privk b)) (uniq-gen y))`
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-gen x y) (uniq-orig (privk b) (privk a)))`
    - `(defskeleton station-weak (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (deflistener (exp (gen) (mul x y))) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-gen x y) (uniq-orig (privk b) (privk a)))`
- **When to Reference This Example**: Reference this example to understand the difference between role-level `(uniq-gen ...)` (every peer strand generates a fresh DH exponent) and skeleton-level `(uniq-gen ...)` (only the POV/specified strands are guaranteed fresh exponents).
- **Key S-Expression Excerpt**:
```scheme
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
```

## sts_weakened_reflect.scm

- **File Path**: `03_examples_scm/sts_weakened_reflect.scm`
- **Algebra & Herald**: Algebra: `diffie-hellman` | Herald: `(herald "station-to-station-reflect protocol" (bound 20) (algebra diffie-hellman))` | Flags: `(bound 20)`, `(algebra diffie-hellman)`
- **Protocol & Purpose**: Models a weakened Station-to-Station variant (`station-to-station-reflect`) in the `diffie-hellman` algebra that omits the order flip of the Diffie-Hellman exponentials `(exp (gen) eta)` and `(exp (gen) x)` inside the signed component of the second and third messages, enabling a reflection/type-symmetry attack.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `station-to-station-reflect`):
    - `vars`: `(x rndx), (eta expt), (a b name)` | Role assumptions/annotations: `(uniq-gen x)`
    - `trace`: `(send (exp (gen) x))` -> `(recv (cat (exp (gen) eta) (enc (enc (exp (gen) eta) (exp (gen) x) (privk b)) (exp (exp (gen) eta) x))))` -> `(send (enc (enc (exp (gen) eta) (exp (gen) x) (privk a)) (exp (exp (gen) eta) x)))` -> `(send (privk a))`
  - Role `resp` (in `station-to-station-reflect`):
    - `vars`: `(y rndx), (chi expt), (a b name)` | Role assumptions/annotations: `(uniq-gen y)`
    - `trace`: `(recv (exp (gen) chi))` -> `(send (cat (exp (gen) y) (enc (enc (exp (gen) y) (exp (gen) chi) (privk b)) (exp (exp (gen) chi) y))))` -> `(recv (enc (enc (exp (gen) y) (exp (gen) chi) (privk a)) (exp (exp (gen) chi) y)))` -> `(send (privk b))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `algebra`, `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (6)**:
    - `(defskeleton station-to-station-reflect (vars (a b name)) (defstrand init 3 (a a) (b b)) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station-reflect (vars (a b name)) (defstrand resp 3 (a a) (b b)) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-to-station-reflect (vars (a b name) (x y rndx) (eta expt)) (defstrand init 3 (a a) (b b) (x x) (eta eta)) (deflistener (exp (exp (gen) eta) x)) (non-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station-reflect (vars (a b name) (x y rndx) (chi expt)) (defstrand resp 3 (a a) (b b) (y y) (chi chi)) (deflistener (exp (exp (gen) chi) y)) (non-orig (privk a) (privk b)))`
    - `(defskeleton station-to-station-reflect (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig (privk b) (privk a)))`
    - `(defskeleton station-to-station-reflect (vars (a b name) (x y rndx)) (defstrand init 4 (a a) (b b) (eta y) (x x)) (defstrand resp 4 (b b) (chi x) (y y)) (deflistener (exp (gen) (mul x y))) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig (privk b) (privk a)))`
- **When to Reference This Example**: Reference this example when analyzing reflection or role-confusion vulnerabilities in Diffie-Hellman handshake signatures where initiator and responder sign identically ordered transcript terms.
- **Key S-Expression Excerpt**:
```scheme
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
```

## subatomic-open-closed-test-genrule.scm

- **File Path**: `03_examples_scm/subatomic-open-closed-test-genrule.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald subatomic-open-closed-test-genrule (bound 40))` | Flags: `(bound 40)`
- **Protocol & Purpose**: Models a stateful device open/close/pass access-control protocol (`subatomic-open-closed`) with two state locations (`lk` for key state, `ls` for open/closed status), channels (`start-ch`), `(gen-st ...)`, `(facts (same-dev ls lk))`, and explicit `(defgenrule ...)` declarations encoding subatomic state transition semantics (`no-interruption`, `cakeRule`, `scissorsRule`, `shearsRule`, `invShearsRule`, `trans`, `same-locn`, `leads-to`).
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `dev-up` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d o name), (old old1 mesg), (start-ch chan), (lk ls locn)` | Role assumptions/annotations: `(auth start-ch)`, `(facts (same-dev ls lk))`
    - `trace`: `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(load ls old1)` -> `(stor lk (cat "st-k" d o k))` -> `(stor ls (cat "st" d o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d o name), (start-ch chan)` | Role assumptions/annotations: `(conf start-ch)`
    - `trace`: `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name)` | Role assumptions: none
    - `trace`: `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name)` | Role assumptions: none
    - `trace`: `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d o name), (lk ls locn)` | Role assumptions/annotations: `(gen-st (cat "st-k" d o k) (cat "st" d (cat o o)))`, `(facts (same-dev ls lk))`
    - `trace`: `(recv (enc "open" d o n k))` -> `(load ls (cat "st" d any))` -> `(load lk (cat "st-k" d o k))` -> `(stor ls (cat "st" d o o))` -> `(send n)`
  - Role `dev-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d o name), (lk ls locn)` | Role assumptions/annotations: `(gen-st (cat "st-k" d o k))`, `(facts (same-dev ls lk))`
    - `trace`: `(recv (enc "close" d o n k))` -> `(load lk (cat "st-k" d o k))` -> `(load ls (cat "st" d any))` -> `(stor ls (cat "st" d o))` -> `(send n)`
  - Role `dev-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name), (lk ls locn)` | Role assumptions/annotations: `(uniq-orig n)`, `(gen-st (cat "st-k" d o k) (cat "st" d (cat o o)))`, `(facts (same-dev ls lk))`
    - `trace`: `(load lk (cat "st-k" d o k))` -> `(load ls (cat "st" d o o))` -> `(recv (enc "may I pass" k))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey)` | Role assumptions: none
    - `trace`: `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `=`, `and`, `auth`, `bound`, `conf`, `defgenrule`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `false`, `forall`, `gen-st`, `herald`, `implies`, `leads-to`, `load`, `or`, `p`, `prec`, `recv`, `same-locn`, `send`, `stor`, `trace`, `trans`, `uniq-orig`, `vars`
  - **Macros (6)**: `(dev-key-state d o k)` -> `(cat "st-k" d o k)`; `(opened o)` -> `(cat o o)`; `(closed o)` -> `o`; `(dev-state-opened d o)` -> `(cat "st" d (opened o))`; `(dev-state-closed d o)` -> `(cat "st" d (closed o))`; `(dev-state-any d o any)` -> `(cat "st" d any)`
  - **Rules & Genrules (33)**:
    - `(defrule power-deliver-once ...)` in `subatomic-open-closed`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
    - `(defrule same-dev-ls-lk ...)` in `subatomic-open-closed`: `(forall ((ls lk lk-0 locn)) (implies (and (fact same-dev ls lk) (fact same-dev ls lk-0)) (= lk lk-0)))`
    - `(defrule same-dev-lk-ls ...)` in `subatomic-open-closed`: `(forall ((lk ls ls-0 locn)) (implies (and (fact same-dev ls lk) (fact same-dev ls-0 lk)) (= ls ls-0)))`
    - `(defgenrule neqRl_indx ...)` in `subatomic-open-closed`: `(forall ((x indx)) (implies (fact neq x x) (false)))`
    - `(defgenrule neqRl_strd ...)` in `subatomic-open-closed`: `(forall ((x strd)) (implies (fact neq x x) (false)))`
    - `(defgenrule neqRl_mesg ...)` in `subatomic-open-closed`: `(forall ((x mesg)) (implies (fact neq x x) (false)))`
    - `(defgenrule no-interruption ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (leads-to z0 i0 z2 i2) (trans z1 i1) (same-locn z0 i0 z1 i1) (prec z0 i0 z1 i1) (prec z1 i1 z2 i2)) (false)))`
    - `(defgenrule cakeRule ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (trans z0 i0) (trans z1 i1) (leads-to z0 i0 z1 i1) (leads-to z0 i0 z2 i2) (prec z1 i1 z2 i2)) (false)))`
    - `(defgenrule gen-st-dev-pass-0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (o d name)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "o" z o) (p "dev-pass" "d" z d)) (gen-st (cat "st" d o o))))`
    - `(defgenrule gen-st-dev-pass-1 ...)` in `subatomic-open-closed`: `(forall ((z strd) (k skey) (o d name)) (implies (and (p "dev-pass" z 1) (p "dev-pass" "k" z k) (p "dev-pass" "o" z o) (p "dev-pass" "d" z d)) (gen-st (cat "st-k" d o k))))`
    - `(defgenrule fact-dev-pass-same-dev0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (ls lk locn)) (implies (and (p "dev-pass" z 2) (p "dev-pass" "ls" z ls) (p "dev-pass" "lk" z lk)) (fact same-dev ls lk)))`
    - `(defgenrule trRl_dev-close-at-2 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-close" z 3) (trans z 2)))`
    - `(defgenrule trRl_dev-close-at-3 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-close" z 4) (trans z 3)))`
    - `(defgenrule gen-st-dev-close-0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (k skey) (o d name)) (implies (and (p "dev-close" z 1) (p "dev-close" "k" z k) (p "dev-close" "o" z o) (p "dev-close" "d" z d)) (gen-st (cat "st-k" d o k))))`
    - `(defgenrule fact-dev-close-same-dev0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (ls lk locn)) (implies (and (p "dev-close" z 3) (p "dev-close" "ls" z ls) (p "dev-close" "lk" z lk)) (fact same-dev ls lk)))`
    - `(defgenrule trRl_dev-open-at-1 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-open" z 2) (trans z 1)))`
    - `(defgenrule trRl_dev-open-at-3 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-open" z 4) (trans z 3)))`
    - `(defgenrule gen-st-dev-open-0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (o d name)) (implies (and (p "dev-open" z 1) (p "dev-open" "o" z o) (p "dev-open" "d" z d)) (gen-st (cat "st" d o o))))`
    - `(defgenrule gen-st-dev-open-1 ...)` in `subatomic-open-closed`: `(forall ((z strd) (k skey) (o d name)) (implies (and (p "dev-open" z 1) (p "dev-open" "k" z k) (p "dev-open" "o" z o) (p "dev-open" "d" z d)) (gen-st (cat "st-k" d o k))))`
    - `(defgenrule fact-dev-open-same-dev0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (ls lk locn)) (implies (and (p "dev-open" z 3) (p "dev-open" "ls" z ls) (p "dev-open" "lk" z lk)) (fact same-dev ls lk)))`
    - `(defgenrule trRl_dev-up-at-1 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-up" z 2) (trans z 1)))`
    - `(defgenrule trRl_dev-up-at-2 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-up" z 3) (trans z 2)))`
    - `(defgenrule trRl_dev-up-at-3 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-up" z 4) (trans z 3)))`
    - `(defgenrule trRl_dev-up-at-4 ...)` in `subatomic-open-closed`: `(forall ((z strd)) (implies (p "dev-up" z 5) (trans z 4)))`
    - `(defgenrule fact-dev-up-same-dev0 ...)` in `subatomic-open-closed`: `(forall ((z strd) (ls lk locn)) (implies (and (p "dev-up" z 3) (p "dev-up" "ls" z ls) (p "dev-up" "lk" z lk)) (fact same-dev ls lk)))`
    - `(defgenrule scissorsRule ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (trans z0 i0) (trans z1 i1) (trans z2 i2) (leads-to z0 i0 z1 i1) (leads-to z0 i0 z2 i2)) (and (= z1 z2) (= i1 i2))))`
    - `(defgenrule cau-dev-pass-1 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-pass" z 2) (prec z1 i z 1)) (or (= z z1) (prec z1 i z 0))))`
    - `(defgenrule cau-dev-close-2 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-close" z 3) (prec z1 i z 2)) (or (= z z1) (prec z1 i z 1))))`
    - `(defgenrule cau-dev-open-2 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-open" z 3) (prec z1 i z 2)) (or (= z z1) (prec z1 i z 1))))`
    - `(defgenrule cau-dev-up-2 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-up" z 3) (prec z1 i z 2)) (or (= z z1) (prec z1 i z 1))))`
    - `(defgenrule eff-dev-up-3 ...)` in `subatomic-open-closed`: `(forall ((z z1 strd) (i indx)) (implies (and (p "dev-up" z 4) (prec z 3 z1 i)) (or (= z z1) (and (p "dev-up" z 5) (prec z 4 z1 i)))))`
    - `(defgenrule invShearsRule ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (trans z0 i0) (trans z1 i1) (same-locn z0 i0 z1 i1) (leads-to z1 i1 z2 i2) (prec z0 i0 z2 i2)) (or (and (= z0 z1) (= i0 i1)) (prec z0 i0 z1 i1))))`
    - `(defgenrule shearsRule ...)` in `subatomic-open-closed`: `(forall ((z0 z1 z2 strd) (i0 i1 i2 indx)) (implies (and (trans z0 i0) (trans z1 i1) (trans z2 i2) (leads-to z0 i0 z1 i1) (same-locn z0 i0 z2 i2) (prec z0 i0 z2 i2)) (or (and (= z1 z2) (= i1 i2)) (prec z1 i1 z2 i2))))`
  - **Goals**: None.
  - **Skeletons (3)**:
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (deflistener k) (uniq-orig k) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand dev-pass 4 (k k)) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (defstrand dev-pass 4 (k k)) (uniq-orig k) (facts (no-state-split)))`
- **When to Reference This Example**: Reference this example when debugging or writing low-level `(defgenrule ...)` axioms for stateful location (`locn`) transitions, `leads-to`, `trans`, `same-locn`, and `gen-st` without relying on obsolete `critical-sections`.
- **Key S-Expression Excerpt**:
```scheme
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
```

## subatomic-open-closed.scm

- **File Path**: `03_examples_scm/subatomic-open-closed.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald subatomic-open-closed (bound 40))` | Flags: `(bound 40)`
- **Protocol & Purpose**: Models the stateful `subatomic-open-closed` device protocol using state macros (`dev-key-state`, `dev-state-opened`, `dev-state-closed`, `dev-state-any`), two `locn` variables (`lk`, `ls`), channel `start-ch` (`auth`/`conf`), `(gen-st ...)`, and three user-level `(defrule ...)` axioms (`power-deliver-once`, `same-dev-ls-lk`, `same-dev-lk-ls`) without the auto-generated `defgenrule` boilerplate.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `dev-up` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d o name), (old old1 mesg), (start-ch chan), (lk ls locn)` | Role assumptions/annotations: `(auth start-ch)`, `(facts (same-dev ls lk))`
    - `trace`: `(recv start-ch (cat "power-up" d o k))` -> `(load lk old)` -> `(load ls old1)` -> `(stor lk (dev-key-state d o k))` -> `(stor ls (dev-state-closed d o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d o name), (start-ch chan)` | Role assumptions/annotations: `(conf start-ch)`
    - `trace`: `(send start-ch (cat "power-up" d o k))` -> `(recv (enc "up" k))`
  - Role `owner-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name)` | Role assumptions: none
    - `trace`: `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name)` | Role assumptions: none
    - `trace`: `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d o name), (lk ls locn)` | Role assumptions/annotations: `(gen-st (dev-key-state d o k) (dev-state-opened d o))`, `(facts (same-dev ls lk))`
    - `trace`: `(recv (enc "open" d o n k))` -> `(load ls (dev-state-any d o any))` -> `(load lk (dev-key-state d o k))` -> `(stor ls (dev-state-opened d o))` -> `(send n)`
  - Role `dev-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d o name), (lk ls locn)` | Role assumptions/annotations: `(gen-st (dev-key-state d o k))`, `(facts (same-dev ls lk))`
    - `trace`: `(recv (enc "close" d o n k))` -> `(load lk (dev-key-state d o k))` -> `(load ls (dev-state-any d o any))` -> `(stor ls (dev-state-closed d o))` -> `(send n)`
  - Role `dev-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name), (lk ls locn)` | Role assumptions/annotations: `(uniq-orig n)`, `(gen-st (dev-key-state d o k) (dev-state-opened d o))`, `(facts (same-dev ls lk))`
    - `trace`: `(load lk (dev-key-state d o k))` -> `(load ls (dev-state-opened d o))` -> `(recv (enc "may I pass" k))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d o name), (l locn)` | Role assumptions: none
    - `trace`: `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `=`, `and`, `auth`, `bound`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `forall`, `gen-st`, `herald`, `implies`, `load`, `p`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros (6)**: `(dev-key-state d o k)` -> `(cat "st-k" d o k)`; `(opened o)` -> `(cat o o)`; `(closed o)` -> `o`; `(dev-state-opened d o)` -> `(cat "st" d (opened o))`; `(dev-state-closed d o)` -> `(cat "st" d (closed o))`; `(dev-state-any d o any)` -> `(cat "st" d any)`
  - **Rules & Genrules (3)**:
    - `(defrule power-deliver-once ...)` in `subatomic-open-closed`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
    - `(defrule same-dev-ls-lk ...)` in `subatomic-open-closed`: `(forall ((ls lk lk-0 locn)) (implies (and (fact same-dev ls lk) (fact same-dev ls lk-0)) (= lk lk-0)))`
    - `(defrule same-dev-lk-ls ...)` in `subatomic-open-closed`: `(forall ((lk ls ls-0 locn)) (implies (and (fact same-dev ls lk) (fact same-dev ls-0 lk)) (= ls ls-0)))`
  - **Goals**: None.
  - **Skeletons (3)**:
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (deflistener k) (uniq-orig k) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand dev-pass 4 (k k)) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (defstrand dev-pass 4 (k k)) (uniq-orig k) (facts (no-state-split)))`
- **When to Reference This Example**: Reference this example as the clean idiom for modeling multi-location device state with `load`/`stor`, `gen-st`, `facts`, and `defrule` functional dependencies between locations on the same device.
- **Key S-Expression Excerpt**:
```scheme
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
```

## sync_locn_envelope.scm

- **File Path**: `03_examples_scm/sync_locn_envelope.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Envelope Protocol, location-based version" (check-nonces) (bound 30) (limit 6000))` | Flags: `(check-nonces)`, `(bound 30)`, `(limit 6000)`
- **Protocol & Purpose**: Models the TPM Envelope Protocol (`envelope`) using location-based state (`pcr` of sort `locn`) and channels (`tpm`, `tpmconf` of sort `chan`), using higher-order macros `(defmacro (roles) (^ ...))` and `(defmacro (genStV-rules) (^ ...))` with splice operator `^` to share roles and `gen-st` rules across protocol variants.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `tpm-power-on` (in `envelope`):
    - `vars`: `(current-value mesg), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc` (in `envelope`):
    - `vars`: `(value current-value mesg), (pcr-id nonce text), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(uniq-orig nonce)`
    - `trace`: `(send tpm (cat "token" nonce))` -> `(recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote` (in `envelope`):
    - `vars`: `(nonce current-value mesg), (pcr-id text), (aik akey), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key` (in `envelope`):
    - `vars`: `(k aik akey), (pcr-id text), (pcrval mesg), (tpm chan)` | Role assumptions/annotations: `(uniq-orig k)`, `(non-orig (invk k))`, `(auth tpm)`
    - `trace`: `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt` (in `envelope`):
    - `vars`: `(m current-value mesg), (pcr-id text), (k aik akey), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(non-orig aik)`
    - `trace`: `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice` (in `envelope`):
    - `vars`: `(n v data), (pcr-id nonce text), (k aik akey), (tpm tpmconf chan)` | Role assumptions/annotations: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpmconf)`
    - `trace`: `(recv tpm (cat "token" nonce))` -> `(send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `^`, `and`, `auth`, `bound`, `check-nonces`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `facts`, `forall`, `gen-st`, `herald`, `implies`, `limit`, `load`, `neq`, `non-orig`, `p`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros (3)**: `(refuse pcr-id n v k aik)` -> `(enc "quote" pcr-id (hash (hash "0" n) "refuse") (enc v k) aik)`; `(roles)` -> `(^ (defrole tpm-power-on (vars (current-value mesg) (pcr locn) (tpm chan)) (trace (recv tpm "power on") (load pcr current-value) (stor pcr "0"))) (defrole tpm-extend-enc (vars (value current-value mesg) (pcr-id nonce text) (pcr locn) (tpm chan)) (trace (send tpm (cat "token" nonce)) (recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce))) (load pcr current-value) (stor pcr (hash current-value value)) (send "ext ok")) (uniq-orig nonce)) (defrole tpm-quote (vars (nonce current-value mesg) (pcr-id text) (aik akey) (pcr locn) (tpm chan)) (trace (recv tpm (cat "quote" pcr-id nonce)) (load pcr current-value) (send (enc "quote" pcr-id current-value nonce aik)))) (defrole tpm-create-key (vars (k aik akey) (pcr-id text) (pcrval mesg) (tpm chan)) (trace (recv tpm (cat "create-req" pcr-id pcrval)) (send (enc "created" k pcr-id pcrval aik))) (uniq-orig k) (non-orig (invk k)) (auth tpm)) (defrole tpm-decrypt (vars (m current-value mesg) (pcr-id text) (k aik akey) (pcr locn) (tpm chan)) (trace (recv tpm (cat "decrypt" (enc m k))) (recv (enc "created" k pcr-id current-value aik)) (load pcr current-value) (send m)) (non-orig aik)) (defrole alice (vars (n v data) (pcr-id nonce text) (k aik akey) (tpm tpmconf chan)) (trace (recv tpm (cat "token" nonce)) (send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce))) (send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain"))) (recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik)) (send (enc v k))) (neq (k aik)) (uniq-orig n v) (non-orig aik) (conf tpmconf)))`; `(genStV-rules)` -> `(^ (defrule genStV-if-hashed-tpm-power-on (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-extend-enc (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-decrypt (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-quote (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))))`
  - **Rules & Genrules (4)**:
    - `(defrule genStV-if-hashed-tpm-power-on ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-extend-enc ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-decrypt ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-quote ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton envelope (vars (v data)) (deflistener v) (defstrand alice 5 (v v)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)) (facts (no-state-split)))`
- **When to Reference This Example**: Reference this example when modeling TPM PCR `load`/`stor` state machines, channel authentication `(auth tpm)` / confidentiality `(conf tpmconf)`, or when using `(defmacro (name) (^ ...))` to splice multiple roles/rules into a `defprotocol`.
- **Key S-Expression Excerpt**:
```scheme
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
```

## sync_locn_envelope_no_auth.scm

- **File Path**: `03_examples_scm/sync_locn_envelope_no_auth.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Envelope Protocol, location-based version" (check-nonces) (bound 30) (limit 6000))` | Flags: `(check-nonces)`, `(bound 30)`, `(limit 6000)`
- **Protocol & Purpose**: Variant of the location-based TPM Envelope Protocol that comments out `(auth tpm)` in `tpm-create-key`, activates four `genStV-not-catted-*` rules forbidding catted PCR values, and compares three protocol rule sets (`envelope`, `envelope-plus` with `ordered-extends`, and `envelope-plus-2` with `pcr-id-identifies-pcr`).
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `tpm-power-on` (in `envelope`):
    - `vars`: `(current-value mesg), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc` (in `envelope`):
    - `vars`: `(value current-value mesg), (pcr-id nonce text), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(uniq-orig nonce)`
    - `trace`: `(send tpm (cat "token" nonce))` -> `(recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote` (in `envelope`):
    - `vars`: `(nonce current-value mesg), (pcr-id text), (aik akey), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key` (in `envelope`):
    - `vars`: `(k aik akey), (pcr-id text), (pcrval mesg), (tpm chan)` | Role assumptions/annotations: `(uniq-orig k)`, `(non-orig (invk k))`
    - `trace`: `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt` (in `envelope`):
    - `vars`: `(m current-value mesg), (pcr-id text), (k aik akey), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(non-orig aik)`
    - `trace`: `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice` (in `envelope`):
    - `vars`: `(n v data), (pcr-id nonce text), (k aik akey), (tpm tpmconf chan)` | Role assumptions/annotations: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpmconf)`
    - `trace`: `(recv tpm (cat "token" nonce))` -> `(send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
  - Role `tpm-power-on` (in `envelope-plus`):
    - `vars`: `(current-value mesg), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc` (in `envelope-plus`):
    - `vars`: `(value current-value mesg), (pcr-id nonce text), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(uniq-orig nonce)`
    - `trace`: `(send tpm (cat "token" nonce))` -> `(recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote` (in `envelope-plus`):
    - `vars`: `(nonce current-value mesg), (pcr-id text), (aik akey), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key` (in `envelope-plus`):
    - `vars`: `(k aik akey), (pcr-id text), (pcrval mesg), (tpm chan)` | Role assumptions/annotations: `(uniq-orig k)`, `(non-orig (invk k))`
    - `trace`: `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt` (in `envelope-plus`):
    - `vars`: `(m current-value mesg), (pcr-id text), (k aik akey), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(non-orig aik)`
    - `trace`: `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice` (in `envelope-plus`):
    - `vars`: `(n v data), (pcr-id nonce text), (k aik akey), (tpm tpmconf chan)` | Role assumptions/annotations: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpmconf)`
    - `trace`: `(recv tpm (cat "token" nonce))` -> `(send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
  - Role `tpm-power-on` (in `envelope-plus-2`):
    - `vars`: `(current-value mesg), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm "power on")` -> `(load pcr current-value)` -> `(stor pcr "0")`
  - Role `tpm-extend-enc` (in `envelope-plus-2`):
    - `vars`: `(value current-value mesg), (pcr-id nonce text), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(uniq-orig nonce)`
    - `trace`: `(send tpm (cat "token" nonce))` -> `(recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce)))` -> `(load pcr current-value)` -> `(stor pcr (hash current-value value))` -> `(send "ext ok")`
  - Role `tpm-quote` (in `envelope-plus-2`):
    - `vars`: `(nonce current-value mesg), (pcr-id text), (aik akey), (pcr locn), (tpm chan)` | Role assumptions: none
    - `trace`: `(recv tpm (cat "quote" pcr-id nonce))` -> `(load pcr current-value)` -> `(send (enc "quote" pcr-id current-value nonce aik))`
  - Role `tpm-create-key` (in `envelope-plus-2`):
    - `vars`: `(k aik akey), (pcr-id text), (pcrval mesg), (tpm chan)` | Role assumptions/annotations: `(uniq-orig k)`, `(non-orig (invk k))`
    - `trace`: `(recv tpm (cat "create-req" pcr-id pcrval))` -> `(send (enc "created" k pcr-id pcrval aik))`
  - Role `tpm-decrypt` (in `envelope-plus-2`):
    - `vars`: `(m current-value mesg), (pcr-id text), (k aik akey), (pcr locn), (tpm chan)` | Role assumptions/annotations: `(non-orig aik)`
    - `trace`: `(recv tpm (cat "decrypt" (enc m k)))` -> `(recv (enc "created" k pcr-id current-value aik))` -> `(load pcr current-value)` -> `(send m)`
  - Role `alice` (in `envelope-plus-2`):
    - `vars`: `(n v data), (pcr-id nonce text), (k aik akey), (tpm tpmconf chan)` | Role assumptions/annotations: `(neq (k aik))`, `(uniq-orig n v)`, `(non-orig aik)`, `(conf tpmconf)`
    - `trace`: `(recv tpm (cat "token" nonce))` -> `(send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce)))` -> `(send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain")))` -> `(recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik))` -> `(send (enc v k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `=`, `^`, `and`, `bound`, `check-nonces`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `false`, `forall`, `gen-st`, `herald`, `implies`, `limit`, `load`, `neq`, `non-orig`, `or`, `p`, `prec`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros (3)**: `(refuse pcr-id n v k aik)` -> `(enc "quote" pcr-id (hash (hash "0" n) "refuse") (enc v k) aik)`; `(roles)` -> `(^ (defrole tpm-power-on (vars (current-value mesg) (pcr locn) (tpm chan)) (trace (recv tpm "power on") (load pcr current-value) (stor pcr "0"))) (defrole tpm-extend-enc (vars (value current-value mesg) (pcr-id nonce text) (pcr locn) (tpm chan)) (trace (send tpm (cat "token" nonce)) (recv tpm (cat "extend" pcr-id value (hash pcr-id value nonce))) (load pcr current-value) (stor pcr (hash current-value value)) (send "ext ok")) (uniq-orig nonce)) (defrole tpm-quote (vars (nonce current-value mesg) (pcr-id text) (aik akey) (pcr locn) (tpm chan)) (trace (recv tpm (cat "quote" pcr-id nonce)) (load pcr current-value) (send (enc "quote" pcr-id current-value nonce aik)))) (defrole tpm-create-key (vars (k aik akey) (pcr-id text) (pcrval mesg) (tpm chan)) (trace (recv tpm (cat "create-req" pcr-id pcrval)) (send (enc "created" k pcr-id pcrval aik))) (uniq-orig k) (non-orig (invk k))) (defrole tpm-decrypt (vars (m current-value mesg) (pcr-id text) (k aik akey) (pcr locn) (tpm chan)) (trace (recv tpm (cat "decrypt" (enc m k))) (recv (enc "created" k pcr-id current-value aik)) (load pcr current-value) (send m)) (non-orig aik)) (defrole alice (vars (n v data) (pcr-id nonce text) (k aik akey) (tpm tpmconf chan)) (trace (recv tpm (cat "token" nonce)) (send tpmconf (cat "extend" pcr-id n (hash pcr-id n nonce))) (send tpm (cat "create-req" pcr-id (hash (hash "0" n) "obtain"))) (recv (enc "created" k pcr-id (hash (hash "0" n) "obtain") aik)) (send (enc v k))) (neq (k aik)) (uniq-orig n v) (non-orig aik) (conf tpmconf)))`; `(genStV-rules)` -> `(^ (defrule genStV-if-hashed-tpm-power-on (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-extend-enc (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-decrypt (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-if-hashed-tpm-quote (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))) (defrule genStV-not-catted-tpm-power-on (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (cat v1 v2))) (false)))) (defrule genStV-not-catted-tpm-extend-enc (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (cat v1 v2))) (false)))) (defrule genStV-not-catted-tpm-decrypt (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (cat v1 v2))) (false)))) (defrule genStV-not-catted-tpm-quote (forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (cat v1 v2))) (false)))))`
  - **Rules & Genrules (26)**:
    - `(defrule genStV-if-hashed-tpm-power-on ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-extend-enc ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-decrypt ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-quote ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-not-catted-tpm-power-on ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-extend-enc ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-decrypt ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-quote ...)` in `envelope`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-if-hashed-tpm-power-on ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-extend-enc ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-decrypt ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-quote ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-not-catted-tpm-power-on ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-extend-enc ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-decrypt ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-quote ...)` in `envelope-plus`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule ordered-extends ...)` in `envelope-plus`: `(forall ((y z strd) (pcr locn)) (implies (and (p "tpm-extend-enc" y 4) (p "tpm-extend-enc" z 4) (p "tpm-extend-enc" "pcr" y pcr) (p "tpm-extend-enc" "pcr" z pcr)) (or (= y z) (prec y 3 z 2) (prec z 3 y 2))))`
    - `(defrule genStV-if-hashed-tpm-power-on ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-extend-enc ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-decrypt ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-if-hashed-tpm-quote ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (hash v1 v2))) (gen-st (hash v1 v2))))`
    - `(defrule genStV-not-catted-tpm-power-on ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-power-on" z 2) (p "tpm-power-on" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-extend-enc ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-extend-enc" z 2) (p "tpm-extend-enc" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-decrypt ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-decrypt" z 3) (p "tpm-decrypt" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule genStV-not-catted-tpm-quote ...)` in `envelope-plus-2`: `(forall ((z strd) (v1 v2 mesg)) (implies (and (p "tpm-quote" z 2) (p "tpm-quote" "current-value" z (cat v1 v2))) (false)))`
    - `(defrule pcr-id-identifies-pcr ...)` in `envelope-plus-2`: `(forall ((y z strd) (pcr-id text) (pcr pcr-0 locn)) (implies (and (p "tpm-extend-enc" y 3) (p "tpm-extend-enc" z 3) (p "tpm-extend-enc" "pcr-id" y pcr-id) (p "tpm-extend-enc" "pcr-id" z pcr-id) (p "tpm-extend-enc" "pcr" y pcr) (p "tpm-extend-enc" "pcr" z pcr-0)) (= pcr pcr-0)))`
  - **Goals**: None.
  - **Skeletons (9)**:
    - `(defskeleton envelope (vars (v data)) (deflistener v) (defstrand alice 5 (v v)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope-plus (vars (v data)) (deflistener v) (defstrand alice 5 (v v)))`
    - `(defskeleton envelope-plus (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope-plus (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope-plus-2 (vars (v data)) (deflistener v) (defstrand alice 5 (v v)))`
    - `(defskeleton envelope-plus-2 (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
    - `(defskeleton envelope-plus-2 (vars (n v data) (k aik akey) (pcr-id text)) (deflistener (refuse pcr-id n v k aik)) (deflistener v) (defstrand alice 5 (n n) (v v) (k k) (aik aik)))`
- **When to Reference This Example**: Reference this example to see how omitting channel authentication `(auth tpm)` affects TPM state shapes and how `defrule` axioms (`ordered-extends`, `pcr-id-identifies-pcr`) prevent state-splitting across multiple protocol variants in one file.
- **Key S-Expression Excerpt**:
```scheme
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
```

## targetterms1.scm

- **File Path**: `03_examples_scm/targetterms1.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Minimal two-role protocol (`targetterms`) testing CPSA's target terms solved filter: `init` sends `(enc n1 (enc a n2 k) k)` and expects `(enc a n1 k)`, while `resp` decrypts `(enc n1 m k)` and sends `m`, forcing `n1 = n2` and `m = (enc a n1 k)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `targetterms`):
    - `vars`: `(a skey), (n1 n2 text), (k akey)` | Role assumptions: none
    - `trace`: `(send (enc n1 (enc a n2 k) k))` -> `(recv (enc a n1 k))`
  - Role `resp` (in `targetterms`):
    - `vars`: `(n1 text), (m mesg), (k akey)` | Role assumptions: none
    - `trace`: `(recv (enc n1 m k))` -> `(send m)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton targetterms (vars (n1 text) (k akey)) (defstrand init 2 (n1 n1) (k k)) (non-orig (invk k)) (uniq-orig n1))`
- **When to Reference This Example**: Reference this example to understand how CPSA resolves generic `mesg` variables (`m`) in decryptor/responder roles when an initiator's reception requires unifying two distinct nonce variables (`n1` and `n2`).
- **Key S-Expression Excerpt**:
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

## targetterms2.scm

- **File Path**: `03_examples_scm/targetterms2.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Models a target-terms experiment (`targetterms2`) where `init` sends `(enc n (pubk a))` and expects triple-nested `(enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a))`, synthesized by chaining instances of a generic transformer role `trans` that receives `(enc n (pubk a))` and `m` and outputs `(enc n m (pubk a))`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `targetterms2`):
    - `vars`: `(a name), (n text)` | Role assumptions/annotations: `(uniq-orig n)`, `(non-orig (privk a))`
    - `trace`: `(send (enc n (pubk a)))` -> `(recv (enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a)))`
  - Role `trans` (in `targetterms2`):
    - `vars`: `(a name), (n text), (m mesg)` | Role assumptions: none
    - `trace`: `(recv (enc n (pubk a)))` -> `(recv m)` -> `(send (enc n m (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton targetterms2 (vars (a name) (n text)) (defstrand init 2 (a a) (n n)))`
- **When to Reference This Example**: Reference this example when analyzing protocols with recursive or chained wrapping/transforming roles that bind a generic `mesg` variable `m` across multiple strands.
- **Key S-Expression Excerpt**:
```scheme
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

## targetterms6.scm

- **File Path**: `03_examples_scm/targetterms6.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Extends `targetterms2` so `init` receives the concatenation of both the triple-wrapped and double-wrapped terms, exposing historical CPSA bugs in single-position critical message contractions and aggressive cohort pruning when multiple `trans` strands have differently bound `mesg` variables.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `targetterms6`):
    - `vars`: `(a name), (n text), (m mesg)` | Role assumptions/annotations: `(uniq-orig n)`, `(non-orig (privk a))`
    - `trace`: `(send (enc n (pubk a)))` -> `(recv (cat (enc n (enc n (enc n (pubk a)) (pubk a)) (pubk a)) (enc n (enc n (pubk a)) (pubk a))))`
  - Role `trans` (in `targetterms6`):
    - `vars`: `(a name), (n text), (m mesg)` | Role assumptions: none
    - `trace`: `(recv (enc n (pubk a)))` -> `(recv m)` -> `(send (enc n m (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton targetterms6 (vars (a name) (n text)) (defstrand init 2 (a a) (n n)))`
    - `(defskeleton targetterms6 (vars (n text) (a name)) (defstrand init 2 (n n) (a a)) (defstrand trans 3 (m (enc n (pubk a))) (n n) (a a)) (defstrand trans 3 (m (enc n (enc n (pubk a)) (pubk a))) (n n) (a a)) (precedes ((0 0) (1 0)) ((0 0) (2 0)) ((1 2) (2 1)) ((2 2) (0 1))))`
- **When to Reference This Example**: Reference this example when debugging non-termination or missing shapes involving multiple instances of a generic forwarding/wrapping role with `mesg` variables.
- **Key S-Expression Excerpt**:
```scheme
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

## targetterms8.scm

- **File Path**: `03_examples_scm/targetterms8.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Demonstrates the need for condition 2a in CPSA's solved predicate: `init` sends `(enc n1 (enc a n2 k) k)` and receives `(enc a n1 k)`, while `resp` receives `(enc n1 (enc m k) k)` and sends `(enc m k)`. Compares an initial POV with `n1, n2` distinct against a second POV where `n2` is pre-unified with `n1`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `targetterms8`):
    - `vars`: `(a name), (n1 n2 text), (k akey)` | Role assumptions/annotations: `(uniq-orig n1)`, `(non-orig (invk k))`
    - `trace`: `(send (enc n1 (enc a n2 k) k))` -> `(recv (enc a n1 k))`
  - Role `resp` (in `targetterms8`):
    - `vars`: `(n1 text), (m mesg), (k akey)` | Role assumptions: none
    - `trace`: `(recv (enc n1 (enc m k) k))` -> `(send (enc m k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton targetterms8 (vars (a name) (n1 n2 text) (k akey)) (defstrand init 2 (a a) (n1 n1) (n2 n2) (k k)))`
    - `(defskeleton targetterms8 (vars (a name) (n1 text) (k akey)) (defstrand init 2 (a a) (n1 n1) (n2 n1) (k k)))`
- **When to Reference This Example**: Reference this example when a protocol requires an initiator's own terms to unify (`n2 = n1`) via self-augmentation or when testing how nested encryptions `(enc n1 (enc m k) k)` interact with `mesg` variables.
- **Key S-Expression Excerpt**:
```scheme
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

## thisthat.scm

- **File Path**: `03_examples_scm/thisthat.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Needham-Schroeder Public-Key Protocol This-That Variant")` | Flags: none
- **Protocol & Purpose**: Models the Needham-Schroeder Public-Key Protocol 'This-That' variant (`thisthat`), where `init` sends one challenge `(enc n1 a (pubk b))` and receives two responses and two tagged confirmations (`"this"` and `"that"`), requiring concurrent participation of both `this` and `that` responder roles.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `thisthat`):
    - `vars`: `(a b name), (n1 n2 n3 text)` | Role assumptions: none
    - `trace`: `(send (enc n1 a (pubk b)))` -> `(recv (cat (enc n1 n2 (pubk a)) (enc n1 n3 (pubk a))))` -> `(recv (cat (enc "this" n2 (pubk b)) (enc "that" n3 (pubk b))))`
  - Role `this` (in `thisthat`):
    - `vars`: `(b a name), (n2 n1 text)` | Role assumptions/annotations: `(uniq-orig n2)`
    - `trace`: `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n2 (pubk a)))` -> `(send (enc "this" n2 (pubk b)))`
  - Role `that` (in `thisthat`):
    - `vars`: `(b a name), (n3 n1 text)` | Role assumptions/annotations: `(uniq-orig n3)`
    - `trace`: `(recv (enc n1 a (pubk b)))` -> `(send (enc n1 n3 (pubk a)))` -> `(send (enc "that" n3 (pubk b)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton thisthat (vars (a b name) (n1 text)) (defstrand init 3 (a a) (b b) (n1 n1)) (non-orig (privk b) (privk a)) (uniq-orig n1) (comment "Initiator point-of-view"))`
- **When to Reference This Example**: Reference this example when modeling protocols where a single initiator session interacts with multiple distinct responder roles (`this` and `that`) distinguished by string tags.
- **Key S-Expression Excerpt**:
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

## tickle-unique.scm

- **File Path**: `03_examples_scm/tickle-unique.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald tickle-unique)` | Flags: none
- **Protocol & Purpose**: Models a public-key challenge-response protocol (`tickle`) equipped with a guarded rule `uniq-tickle` that asserts `(uniq nb0)` whenever `(fact guard-me)` holds and `resp` reaches length 2, contrasting unguarded vs. fact-guarded skeletons.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `tickle`):
    - `vars`: `(a b name), (na nb text)` | Role assumptions/annotations: `(uniq-orig na)`
    - `trace`: `(send (enc a na (pubk b)))` -> `(recv (enc b na na nb (pubk a)))` -> `(send nb)`
  - Role `resp` (in `tickle`):
    - `vars`: `(a b name), (na nb0 nb text)` | Role assumptions: none
    - `trace`: `(recv (enc a na (pubk b)))` -> `(send (enc b na nb0 nb (pubk a)))` -> `(recv nb)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `and`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `facts`, `forall`, `herald`, `implies`, `non-orig`, `p`, `recv`, `send`, `trace`, `uniq`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Genrules (1)**:
    - `(defrule uniq-tickle ...)` in `tickle`: `(forall ((z strd) (nb0 text)) (implies (and (fact guard-me) (p "resp" z 2) (p "resp" "nb0" z nb0)) (uniq nb0)))`
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton tickle (vars (a b name) (na nb0 nb text)) (defstrand resp 3 (a a) (b b) (nb0 nb0) (nb nb)) (non-orig (privk a)) (uniq-orig nb))`
    - `(defskeleton tickle (vars (a b name) (na nb0 nb text)) (defstrand resp 3 (a a) (b b) (nb0 nb0) (nb nb)) (facts (guard-me)) (non-orig (privk a)) (uniq-orig nb))`
- **When to Reference This Example**: Reference this example to learn how to conditionally enable or disable a `(defrule ...)` in specific skeletons using a trigger fact like `(facts (guard-me))`.
- **Key S-Expression Excerpt**:
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

## timestamping.scm

- **File Path**: `03_examples_scm/timestamping.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald timestamping-service)` | Flags: none
- **Protocol & Purpose**: Models Bruce Schneier's linked Timestamping Service (`timestamping-service`, Applied Cryptography 2nd Ed., p.76) with roles `client`, `server`, `origin`, and `big-bang`, using macros `(link)` and `(timestamp l)` and double-wrapping `(enc (enc ... (privk trent)) (pubk trent))` to represent server state across linked timestamps.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `client` (in `timestamping-service`):
    - `vars`: `(alice alice_1 trent name), (n data), (h h_1 text), (t_1 l mesg)` | Role assumptions: none
    - `trace`: `(send (cat h alice))` -> `(recv (timestamp l))`
  - Role `server` (in `timestamping-service`):
    - `vars`: `(alice alice_1 trent name), (n data), (h h_1 text), (t_1 l_1 mesg)` | Role assumptions/annotations: `(uniq-orig n)`
    - `trace`: `(recv (cat (enc (enc (link) (privk trent)) (pubk trent)) h alice))` -> `(send (cat (timestamp (hash (link))) (enc (enc (hash alice h (timestamp (hash (link))) (hash (link))) (privk trent)) (pubk trent))))`
  - Role `origin` (in `timestamping-service`):
    - `vars`: `(alice alice_1 trent name), (n data), (h h_1 text), (t_1 l_1 text)` | Role assumptions: none
    - `trace`: `(recv (enc (enc n (privk trent)) (pubk trent)))` -> `(send (enc (enc alice h (timestamp (hash (link))) (hash (link)) (privk trent)) (pubk trent)))`
  - Role `big-bang` (in `timestamping-service`):
    - `vars`: `(n data), (trent name)` | Role assumptions/annotations: `(uniq-orig n)`
    - `trace`: `(send (enc (enc n (privk trent)) (pubk trent)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (2)**: `(link)` -> `(cat alice_1 h_1 t_1 l_1)`; `(timestamp l)` -> `(enc n alice h alice_1 h_1 t_1 l (privk trent))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton timestamping-service (vars (trent name) (n_0 data)) (defstrand client 2 (trent trent)) (non-orig (privk trent)))`
- **When to Reference This Example**: Reference this example when modeling hash-chain or linked-timestamping protocols, or when encoding server state as self-encrypted signed tokens `(enc (enc state (privk s)) (pubk s))` in message-passing basic algebra.
- **Key S-Expression Excerpt**:
```scheme
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

## trust-anchor.scm

- **File Path**: `03_examples_scm/trust-anchor.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald trust-anchor (comment "Tests rule application on initial skeleton"))` | Flags: `(comment "Tests rule application on initial skeleton")`
- **Protocol & Purpose**: Minimal roleless protocol (`trust-anchor`) testing rule application on the initial skeleton: defines `(defrule trust-anchor-inverse-is-non ...)` which deduces `(non (invk k))` from `(fact trust-anchor k)`, and compares a skeleton with explicit `(non-orig (privk ca))` against one with `(facts (trust-anchor (pubk ca)))`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Protocol `trust-anchor` (`basic`): No `(defrole ...)` declarations (roleless rule-testing protocol).
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `deflistener`, `defprotocol`, `defrule`, `defskeleton`, `fact`, `facts`, `forall`, `herald`, `implies`, `non`, `non-orig`, `vars`
  - **Macros**: None.
  - **Rules & Genrules (1)**:
    - `(defrule trust-anchor-inverse-is-non ...)` in `trust-anchor`: `(forall ((k akey)) (implies (fact trust-anchor k) (non (invk k))))`
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton trust-anchor (vars (f ca name)) (deflistener (enc f (pubk f) (privk ca))) (non-orig (privk ca)))`
    - `(defskeleton trust-anchor (vars (f ca name)) (deflistener (enc f (pubk f) (privk ca))) (facts (trust-anchor (pubk ca))))`
- **When to Reference This Example**: Reference this example when modeling PKI trust anchors or custom security assumptions via `(facts ...)` that entail `(non ...)` through a `(defrule ...)`.
- **Key S-Expression Excerpt**:
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

## ugen-at.scm

- **File Path**: `03_examples_scm/ugen-at.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald uniq-at)` | Flags: none
- **Protocol & Purpose**: Models the Yahalom protocol (`yahalom-plus-uniq-at`) using `(uniq-gen ...)` for keys and nonces and includes two rules (`uniq-at` and `ugen-at`) that match the strand-location predicates `(uniq-at v z i)` and `(ugen-at v z i)` and record them as facts `(fact remember v z)` and `(fact remember-gen v z)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom-plus-uniq-at`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (enc b k n-a n-b (ltk a c)))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom-plus-uniq-at`):
    - `vars`: `(b a c name), (n-a n-b text), (rest mesg), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b c))))` -> `(recv (cat (enc a k (ltk b c)) rest))` -> `(send rest)` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom-plus-uniq-at`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-gen k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b c))))` -> `(send (cat (enc a k (ltk b c)) (enc b k n-a n-b (ltk a c))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `deflistener`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `forall`, `herald`, `implies`, `non-orig`, `recv`, `send`, `trace`, `ugen-at`, `uniq-at`, `uniq-gen`, `vars`
  - **Macros**: None.
  - **Rules & Genrules (2)**:
    - `(defrule uniq-at ...)` in `yahalom-plus-uniq-at`: `(forall ((z strd) (i indx) (v mesg)) (implies (uniq-at v z i) (fact remember v z)))`
    - `(defrule ugen-at ...)` in `yahalom-plus-uniq-at`: `(forall ((z strd) (i indx) (v mesg)) (implies (ugen-at v z i) (fact remember-gen v z)))`
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton yahalom-plus-uniq-at (vars (a b c name) (n-b text) (k skey)) (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk b c) (ltk a c)) (uniq-gen n-b))`
    - `(defskeleton yahalom-plus-uniq-at (vars (a b c name) (n-a text)) (defstrand init 3 (n-a n-a) (a a) (b b) (c c)) (non-orig (ltk b c) (ltk a c)) (uniq-gen n-a))`
- **When to Reference This Example**: Reference this example when writing `(defrule ...)` formulas that inspect the exact strand and node index where a value is uniquely generated (`(ugen-at v z i)`) or uniquely originated (`(uniq-at v z i)`).
- **Key S-Expression Excerpt**:
```scheme
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

## ugo.scm

- **File Path**: `03_examples_scm/ugo.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald uniq-gen-and-orig-example (comment "Non-executable role examples"))` | Flags: `(comment "Non-executable role examples")`
- **Protocol & Purpose**: Defines three diagnostic protocols (`uniq-gen-example`, `uniq-gen-example-alt`, `uniq-orig-example`) illustrating non-executable role specifications where an asymmetric key `u` and its inverse `(invk u)` are generated or originated across strands in ways that require a responder to magically compute `(invk u)` from `u`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `uniq-gen-example`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(uniq-gen u)`, `(non-orig k)`
    - `trace`: `(send (enc u k))` -> `(recv (invk u))` -> `(send u)`
  - Role `resp` (in `uniq-gen-example`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc u k))` -> `(send (invk u))` -> `(recv u)`
  - Role `init` (in `uniq-gen-example-alt`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(uniq-gen (invk u))`, `(non-orig k)`
    - `trace`: `(send (enc (invk u) k))` -> `(recv u)` -> `(send u)`
  - Role `resp` (in `uniq-gen-example-alt`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc (invk u) k))` -> `(send u)` -> `(recv u)`
  - Role `init` (in `uniq-orig-example`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(uniq-orig u)`, `(non-orig k)`
    - `trace`: `(send (enc u k))` -> `(recv (invk u))` -> `(send u)`
  - Role `resp` (in `uniq-orig-example`):
    - `vars`: `(u akey), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc u k))` -> `(send (invk u))` -> `(recv u)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrandmax`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (6)**:
    - `(defskeleton uniq-gen-example (vars) (defstrandmax resp) (comment "How is the responder able to send (invk u)?"))`
    - `(defskeleton uniq-gen-example (vars (u akey)) (defstrandmax resp (u u)) (uniq-gen (invk u)) (comment "How is the responder able to send (invk u)?"))`
    - `(defskeleton uniq-gen-example-alt (vars) (defstrandmax resp) (comment "How is the responder able to send (invk u)?"))`
    - `(defskeleton uniq-gen-example-alt (vars (u akey)) (defstrandmax resp (u u)) (uniq-gen (invk u)) (comment "How is the responder able to send (invk u)?"))`
    - `(defskeleton uniq-orig-example (vars) (defstrandmax resp))`
    - `(defskeleton uniq-orig-example (vars (u akey)) (defstrandmax resp (u u)) (uniq-orig (invk u)))`
- **When to Reference This Example**: Reference this example to understand CPSA's semantics for asymmetric key pair generation (`uniq-gen` vs `uniq-orig` on `u` and `(invk u)`) and why specifiers must ensure roles do not use unreceived private keys.
- **Key S-Expression Excerpt**:
```scheme
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

```

## uncarried_keys.scm

- **File Path**: `03_examples_scm/uncarried_keys.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Illustrates a subtlety of `uniq-orig` vs. fresh generation (`uncarried-keys`): `init` declares `(uniq-orig a K)` and sends `K` in its 3rd event (node index 2), yet `resp` can use `K` in a non-carried encryption key position before `K` is ever transmitted if `K` is only `uniq-orig` rather than `uniq-gen`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `uncarried-keys`):
    - `vars`: `(a text), (A B name), (K akey)` | Role assumptions/annotations: `(non-orig (privk B) (invk K))`, `(uniq-orig a K)`
    - `trace`: `(send (enc "start" a A B (pubk B)))` -> `(recv (enc a A B (pubk A)))` -> `(send (enc a K (pubk B)))` -> `(recv (enc a A B K))`
  - Role `resp` (in `uncarried-keys`):
    - `vars`: `(a text), (A B name), (K akey)` | Role assumptions: none
    - `trace`: `(recv (enc "start" a A B (pubk B)))` -> `(send (enc a A B (pubk A)))` -> `(recv (enc a K (pubk B)))` -> `(send (enc a A B K))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton uncarried-keys (vars (a text) (A B name) (K akey)) (defstrand init 4 (a a) (A A) (B B) (K K)))`
- **When to Reference This Example**: Reference this example to understand why keys generated during a protocol run should be declared `uniq-gen` (or why `uniq-orig` alone allows a key to be used in encryption-key position prior to its first carried transmission).
- **Key S-Expression Excerpt**:
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

## unilateral.scm

- **File Path**: `03_examples_scm/unilateral.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald unilateral)` | Flags: none
- **Protocol & Purpose**: Presents two unilateral authentication protocols (`unilateral` and `iso-unilateral` from ISO/IEC JTC 1/SC 27/WG 2 N1050) and formulates their security properties both as POV skeletons (`defskeleton`) and as explicit first-order security goals (`defgoal`), including a deliberately false goal to demonstrate counterexample shape generation.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `unilateral`):
    - `vars`: `(n text), (k akey)` | Role assumptions/annotations: `(uniq-orig n)`
    - `trace`: `(send (enc n k))` -> `(recv n)`
  - Role `resp` (in `unilateral`):
    - `vars`: `(n text), (k akey)` | Role assumptions: none
    - `trace`: `(recv (enc n k))` -> `(send n)`
  - Role `resp` (in `iso-unilateral`):
    - `vars`: `(na nb t1 t2 t3 text), (b name)` | Role assumptions/annotations: `(uniq-orig na)`
    - `trace`: `(recv (cat nb t1))` -> `(send (cat na nb b t3 (enc na nb b t2 (privk b))))`
  - Role `init` (in `iso-unilateral`):
    - `vars`: `(na nb t1 t2 t3 text), (b name)` | Role assumptions/annotations: `(uniq-orig nb)`
    - `trace`: `(send (cat nb t1))` -> `(recv (cat na nb b t3 (enc na nb b t2 (privk b))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `and`, `comment`, `defgoal`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `exists`, `false`, `forall`, `herald`, `implies`, `non`, `non-orig`, `p`, `pen-non-orig`, `pnon`, `prec`, `recv`, `send`, `trace`, `uniq-at`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals (4)**:
    - `(defgoal unilateral (forall ((n text) (k akey) (z strd)) (implies (and (p "init" z 2) (p "init" "n" z n) (p "init" "k" z k) (non (invk k)) (uniq-at n z 0)) (exists ((z-0 strd)) (and (p "resp" z-0 2) (p "resp" "n" z-0 n) (p "resp" "k" z-0 k) (prec z 0 z-0 0) (prec z-0 1 z 1))))))`
    - `(defgoal unilateral (forall ((n text) (k akey) (z strd)) (implies (and (p "resp" z 2) (p "resp" "n" z n) (p "resp" "k" z k) (non (invk k)) (pnon n)) (exists ((k-0 akey) (z-0 strd)) (and (p "init" z-0 1) (p "init" "n" z-0 n) (p "init" "k" z-0 k-0) (prec z-0 0 z 0) (uniq-at n z-0 0))))))`
    - `(defgoal iso-unilateral (forall ((b name) (z strd)) (implies (and (p "init" z 2) (p "init" "b" z b) (non (privk b))) (exists ((y strd)) (and (p "resp" y 2) (p "resp" "b" y b))))))`
    - `(defgoal iso-unilateral (forall ((b name) (z strd)) (implies (and (p "init" z 2) (p "init" "b" z b) (non (privk b))) (false))))`
  - **Skeletons (3)**:
    - `(defskeleton unilateral (vars (k akey)) (defstrand init 2 (k k)) (non-orig (invk k)))`
    - `(defskeleton unilateral (vars (n text) (k akey)) (defstrand resp 2 (n n) (k k)) (pen-non-orig n) (non-orig (invk k)))`
    - `(defskeleton iso-unilateral (vars (b name)) (defstrand init 2 (b b)) (non-orig (privk b)))`
- **When to Reference This Example**: Reference this example when writing `(defgoal ...)` authentication and secrecy theorems using `forall`, `implies`, `exists`, `p`, `prec`, `non`, `pnon`, and `uniq-at`.
- **Key S-Expression Excerpt**:
```scheme
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
```

## uniq-at.scm

- **File Path**: `03_examples_scm/uniq-at.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald uniq-at)` | Flags: none
- **Protocol & Purpose**: Companion to `ugen-at.scm` that models `yahalom-plus-uniq-at` using `(uniq-orig ...)` instead of `(uniq-gen ...)` on the server key `k` and skeleton nonces `n-b`, `n-a`, firing the `uniq-at` rule to record `(fact remember v z)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom-plus-uniq-at`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (enc b k n-a n-b (ltk a c)))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom-plus-uniq-at`):
    - `vars`: `(b a c name), (n-a n-b text), (rest mesg), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b c))))` -> `(recv (cat (enc a k (ltk b c)) rest))` -> `(send rest)` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom-plus-uniq-at`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b c))))` -> `(send (cat (enc a k (ltk b c)) (enc b k n-a n-b (ltk a c))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `deflistener`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `fact`, `forall`, `herald`, `implies`, `non-orig`, `recv`, `send`, `trace`, `ugen-at`, `uniq-at`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Genrules (2)**:
    - `(defrule uniq-at ...)` in `yahalom-plus-uniq-at`: `(forall ((z strd) (i indx) (v mesg)) (implies (uniq-at v z i) (fact remember v z)))`
    - `(defrule ugen-at ...)` in `yahalom-plus-uniq-at`: `(forall ((z strd) (i indx) (v mesg)) (implies (ugen-at v z i) (fact remember-gen v z)))`
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton yahalom-plus-uniq-at (vars (a b c name) (n-b text) (k skey)) (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
    - `(defskeleton yahalom-plus-uniq-at (vars (a b c name) (n-a text)) (defstrand init 3 (n-a n-a) (a a) (b b) (c c)) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-a))`
- **When to Reference This Example**: Reference this example alongside `ugen-at.scm` to compare how `(uniq-at v z i)` and `(ugen-at v z i)` behave in `defrule` triggers under `uniq-orig` vs. `uniq-gen`.
- **Key S-Expression Excerpt**:
```scheme
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

## uniq-gen-test.scm

- **File Path**: `03_examples_scm/uniq-gen-test.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Unique generation test protocols." (comment "Skeletons 2, 4, and 7 should have no shapes."))` | Flags: `(comment "Skeletons 2, 4, and 7 should have no shapes.")`
- **Protocol & Purpose**: Tests `uniq-gen` vs. `non-orig` on a symmetric key `k` in `uniqgentest` with roles `init`, `doubler`, and `resp`. When `k` is `uniq-gen` in the `init` skeleton, `doubler` cannot participate because `doubler` would also generate `k` (yielding a dead skeleton); when `k` is merely `non-orig`, `doubler` can supply `(enc a a k)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `uniqgentest`):
    - `vars`: `(a name), (k skey)` | Role assumptions: none
    - `trace`: `(send (enc a k))` -> `(recv (enc a a k))`
  - Role `doubler` (in `uniqgentest`):
    - `vars`: `(a name), (k skey)` | Role assumptions: none
    - `trace`: `(send (enc a a k))`
  - Role `resp` (in `uniqgentest`):
    - `vars`: `(a name), (k skey)` | Role assumptions: none
    - `trace`: `(recv (enc a k))` -> `(send (enc a a k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-gen`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton uniqgentest (vars (k skey)) (defstrand init 2 (k k)) (uniq-gen k))`
    - `(defskeleton uniqgentest (vars (k skey)) (defstrand init 2 (k k)) (non-orig k))`
- **When to Reference This Example**: Reference this example to understand how `(uniq-gen k)` prevents key-generating helper roles from independently using `k` without receiving it, whereas `(non-orig k)` permits pre-shared key usage across roles.
- **Key S-Expression Excerpt**:
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

## uo.scm

- **File Path**: `03_examples_scm/uo.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Minimal two-role protocol (`uniq-orig`) showing that declaring `(uniq-orig n)` in `init` (which sends `n`) does not prevent `resp` from sending `(enc m n)` before receiving `n`, because `n` appears only in the non-carried key position of `(enc m n)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `uniq-orig`):
    - `vars`: `(n text)` | Role assumptions/annotations: `(uniq-orig n)`
    - `trace`: `(send n)`
  - Role `resp` (in `uniq-orig`):
    - `vars`: `(m n text)` | Role assumptions: none
    - `trace`: `(send (enc m n))` -> `(recv n)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton uniq-orig (vars (n text)) (defstrand init 1 (n n)) (defstrand resp 2 (n n)))`
- **When to Reference This Example**: Reference this example for the simplest possible demonstration of why `uniq-orig` only constrains where a term is first *carried* (not where it is first used as an encryption key).
- **Key S-Expression Excerpt**:
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

## wang-hash.scm

- **File Path**: `03_examples_scm/wang-hash.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Wang's Fair Exchange Protocol" (bound 10))` | Flags: `(bound 10)`
- **Protocol & Purpose**: Models Wang's Fair Exchange Protocol (`wang`) with 14 roles (`init1`–`init5`, `resp1`–`resp3`, `ttp-ab1`–`ttp-ab2`, `ttp-rc1`–`ttp-rc2`, `ttp-cf1`–`ttp-cf2`), 14 macros (`em`, `l-prime`, `l-star`, `eoo-star`, `eor-star`, `rr-star`, `at-star`, `ek`, `l`, `l-prime-prime`, `eoo-prime-prime`, `eor-prime-prime`, `rr-prime-prime`, `cf-prime-prime`), and 12 skeletons proving Lemmas 4.1, 4.2, and 4.3 using built-in `(hash ...)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init1` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (cat k r))`
  - Role `init2` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (enc "abcf" (enc "abrq" (l) (privk "sign" a)) (privk "sign" t)))`
  - Role `init3` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))`
  - Role `init4` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (enc "abcf" (enc "abrq" (l) (privk "sign" a)) (privk "sign" t)))`
  - Role `init5` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))`
  - Role `resp1` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (eor-star (hash k) (enc m k) (ek (l))))` -> `(recv (cat k r))`
  - Role `resp2` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l))) (eor-star (hash k) (enc m k) (ek (l)))))` -> `(send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l))) (eor-star (hash k) (enc m k) (ek (l))) (enc "rcrq" (l) (ek (l)) (privk "sign" b))))` -> `(recv (cat k r))`
  - Role `resp3` (in `wang`):
    - `vars`: `(a b t hash_id name), (e1 e2 x mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l-star e1 x) e1 e2 (eoo-star x e1 e2)))` -> `(send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2)))` -> `(send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2) (enc "rcrq" (l-star e1 x) e2 (privk "sign" b))))` -> `(recv (enc "abcf" (enc "abrq" (l-star e1 x) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-ab1` (in `wang`):
    - `vars`: `(a b t hash_id name), (y x mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (enc "abrq" (l-prime y x) (privk "sign" a)))` -> `(send (cat "sync-abrq" (enc "abrq" (l-prime y x) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-ab2` (in `wang`):
    - `vars`: `(a b t hash_id name), (y x e mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (enc "abrq" (l-prime y x) (privk "sign" a)))` -> `(recv (cat "sync-abrq" (enc "eortag" (hash (l-prime y x)) e (privk "sign" b))))` -> `(send (enc "eortag" (hash (l-prime y x)) e (privk "sign" b)))`
  - Role `ttp-rc1` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (rr-prime-prime y))` -> `(send (cat "sync-rc-req" (rr-prime-prime y)))` -> `(send (cat k r))`
  - Role `ttp-rc2` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (rr-prime-prime y))` -> `(recv (cat "sync-rc-req" (enc "abrq" (l-prime-prime y) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime-prime y) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-cf1` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cf-prime-prime y))` -> `(send (cat "sync-cf-req" (cf-prime-prime y)))` -> `(send (enc (cf-prime-prime y) (privk "sign" t)))`
  - Role `ttp-cf2` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cf-prime-prime y))` -> `(recv (cat "sync-cf-req" (enc "abrq" (l-prime-prime y) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime-prime y) (privk "sign" a)) (privk "sign" t)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `comment`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (14)**: `(em)` -> `(enc m k)`; `(l-prime y x)` -> `(cat a b t y x)`; `(l-star e1 x)` -> `(l-prime (hash e1) x)`; `(eoo-star x e1 e2)` -> `(enc (cat "eootag" (hash (l-star e1 x)) e2) (privk "sign" a))`; `(eor-star x e1 e2)` -> `(enc (cat "eortag" (hash (l-star e1 x)) e2) (privk "sign" b))`; `(rr-star x e1 e2)` -> `(cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2) (enc (cat "rcrq" (l-star e1 x) e2) (privk "sign" b)))`; `(at-star e1 x)` -> `(enc (enc "abrq" (l-star e1 x) (privk "sign" a)) (privk "sign" t))`; `(ek l)` -> `(enc (cat "keytag" (hash l) k r) (pubk "encr" t))`; `(l)` -> `(l-prime (hash (enc m k)) (hash k))`; `(l-prime-prime y)` -> `(cat a b t y (hash k))`; `(eoo-prime-prime y)` -> `(enc (cat "eootag" (hash (l-prime-prime y)) (ek (l-prime-prime y))) (privk "sign" a))`; `(eor-prime-prime y)` -> `(enc (cat "eortag" (hash (l-prime-prime y)) (ek (l-prime-prime y))) (privk "sign" b))`; `(rr-prime-prime y)` -> `(cat (l-prime-prime y) (ek (l-prime-prime y)) (eoo-prime-prime y) (eor-prime-prime y) (enc "rcrq" (l-prime-prime y) (ek (l-prime-prime y)) (privk "sign" b)))`; `(cf-prime-prime y)` -> `(cat (l-prime-prime y) (ek (l-prime-prime y)) (eoo-prime-prime y) (eor-prime-prime y) (enc "cfrq" (l-prime-prime y) (ek (l-prime-prime y)) (privk "sign" b)))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (12)**:
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 1 (b b) (t t) (m m) (r r) (k k)) (deflistener m) (non-orig (privk "encr" t)) (uniq-orig m k) (comment "Experiment 1 to prove Lemma 4.1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 1 (b b) (t t) (m m) (r r) (k k)) (deflistener k) (non-orig (privk "encr" t)) (uniq-orig m k) (comment "Experiment 2 to prove Lemma 4.1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 3 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "First of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init3 3 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "Second of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init5 4 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "Third of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand resp1 3 (a a) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" a)) (comment "First of two experiments to prove Lemma 4.2, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand resp2 4 (a a) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" a)) (comment "Second of two experiments to prove Lemma 4.2, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (e1 e2 x mesg)) (defstrand resp3 4 (a a) (t t)) (non-orig (privk "sign" a)) (comment "Experiments to prove Lemma 4.2, clause 3."))`
    - `(defskeleton wang (vars (a b t hash_id name) (y x mesg)) (deflistener (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a)) (privk "sign" t))) (non-orig (privk "sign" t)) (comment "Experiments to prove Lemma 4.3, clause 1."))`
    - `(defskeleton wang (vars (y x mesg) (a b t name)) (defstrand ttp-ab1 3 (y y) (x x) (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 1 to prove Lemma 4.3, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (r text) (k skey) (y mesg)) (defstrand ttp-rc2 3 (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 2 to prove Lemma 4.3, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (r text) (k skey) (y mesg)) (defstrand ttp-cf2 3 (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 3 to prove Lemma 4.3, clause 2."))`
- **When to Reference This Example**: Reference this example when modeling complex optimistic fair-exchange protocols with a Trusted Third Party (TTP), abort/recovery/confirmation subprotocols, and deep macro composition.
- **Key S-Expression Excerpt**:
```scheme

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

```

## wang-key-hash.scm

- **File Path**: `03_examples_scm/wang-key-hash.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Wang's Fair Exchange Protocol" (bound 10))` | Flags: `(bound 10)`
- **Protocol & Purpose**: Variant of `wang-hash.scm` for Wang's Fair Exchange Protocol that overrides `(hash x)` via `(defmacro (hash x) (enc "h" (cat "h" x)))` to model hashing as symmetric encryption under literal tag `"h"` instead of the built-in `hash` constructor.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init1` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (cat k r))`
  - Role `init2` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (enc "abcf" (enc "abrq" (l) (privk "sign" a)) (privk "sign" t)))`
  - Role `init3` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))`
  - Role `init4` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (enc "abcf" (enc "abrq" (l) (privk "sign" a)) (privk "sign" t)))`
  - Role `init5` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(send (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))` -> `(send (enc "abrq" (l) (privk "sign" a)))` -> `(recv (eor-star (hash k) (enc m k) (ek (l))))`
  - Role `resp1` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (eor-star (hash k) (enc m k) (ek (l))))` -> `(recv (cat k r))`
  - Role `resp2` (in `wang`):
    - `vars`: `(a b t hash_id name), (m data), (r text), (k skey)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l) (enc m k) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l)))))` -> `(send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l))) (eor-star (hash k) (enc m k) (ek (l)))))` -> `(send (cat (l) (ek (l)) (eoo-star (hash k) (enc m k) (ek (l))) (eor-star (hash k) (enc m k) (ek (l))) (enc "rcrq" (l) (ek (l)) (privk "sign" b))))` -> `(recv (cat k r))`
  - Role `resp3` (in `wang`):
    - `vars`: `(a b t hash_id name), (e1 e2 x mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cat (l-star e1 x) e1 e2 (eoo-star x e1 e2)))` -> `(send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2)))` -> `(send (cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2) (enc "rcrq" (l-star e1 x) e2 (privk "sign" b))))` -> `(recv (enc "abcf" (enc "abrq" (l-star e1 x) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-ab1` (in `wang`):
    - `vars`: `(a b t hash_id name), (y x mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (enc "abrq" (l-prime y x) (privk "sign" a)))` -> `(send (cat "sync-abrq" (enc "abrq" (l-prime y x) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-ab2` (in `wang`):
    - `vars`: `(a b t hash_id name), (y x e mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (enc "abrq" (l-prime y x) (privk "sign" a)))` -> `(recv (cat "sync-abrq" (enc "eortag" (hash (l-prime y x)) e (privk "sign" b))))` -> `(send (enc "eortag" (hash (l-prime y x)) e (privk "sign" b)))`
  - Role `ttp-rc1` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (rr-prime-prime y))` -> `(send (cat "sync-rc-req" (rr-prime-prime y)))` -> `(send (cat k r))`
  - Role `ttp-rc2` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (rr-prime-prime y))` -> `(recv (cat "sync-rc-req" (enc "abrq" (l-prime-prime y) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime-prime y) (privk "sign" a)) (privk "sign" t)))`
  - Role `ttp-cf1` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cf-prime-prime y))` -> `(send (cat "sync-cf-req" (cf-prime-prime y)))` -> `(send (enc (cf-prime-prime y) (privk "sign" t)))`
  - Role `ttp-cf2` (in `wang`):
    - `vars`: `(a b t hash_id name), (r text), (k skey), (y mesg)` | Role assumptions/annotations: `(non-orig (privk hash_id))`
    - `trace`: `(recv (cf-prime-prime y))` -> `(recv (cat "sync-cf-req" (enc "abrq" (l-prime-prime y) (privk "sign" a))))` -> `(send (enc "abcf" (enc "abrq" (l-prime-prime y) (privk "sign" a)) (privk "sign" t)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `comment`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros (15)**: `(hash x)` -> `(enc "h" (cat "h" x))`; `(em)` -> `(enc m k)`; `(l-prime y x)` -> `(cat a b t y x)`; `(l-star e1 x)` -> `(l-prime (hash e1) x)`; `(eoo-star x e1 e2)` -> `(enc (cat "eootag" (hash (l-star e1 x)) e2) (privk "sign" a))`; `(eor-star x e1 e2)` -> `(enc (cat "eortag" (hash (l-star e1 x)) e2) (privk "sign" b))`; `(rr-star x e1 e2)` -> `(cat (l-star e1 x) e2 (eoo-star x e1 e2) (eor-star x e1 e2) (enc (cat "rcrq" (l-star e1 x) e2) (privk "sign" b)))`; `(at-star e1 x)` -> `(enc (enc "abrq" (l-star e1 x) (privk "sign" a)) (privk "sign" t))`; `(ek l)` -> `(enc (cat "keytag" (hash l) k r) (pubk "encr" t))`; `(l)` -> `(l-prime (hash (enc m k)) (hash k))`; `(l-prime-prime y)` -> `(cat a b t y (hash k))`; `(eoo-prime-prime y)` -> `(enc (cat "eootag" (hash (l-prime-prime y)) (ek (l-prime-prime y))) (privk "sign" a))`; `(eor-prime-prime y)` -> `(enc (cat "eortag" (hash (l-prime-prime y)) (ek (l-prime-prime y))) (privk "sign" b))`; `(rr-prime-prime y)` -> `(cat (l-prime-prime y) (ek (l-prime-prime y)) (eoo-prime-prime y) (eor-prime-prime y) (enc "rcrq" (l-prime-prime y) (ek (l-prime-prime y)) (privk "sign" b)))`; `(cf-prime-prime y)` -> `(cat (l-prime-prime y) (ek (l-prime-prime y)) (eoo-prime-prime y) (eor-prime-prime y) (enc "cfrq" (l-prime-prime y) (ek (l-prime-prime y)) (privk "sign" b)))`
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (12)**:
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 1 (b b) (t t) (m m) (r r) (k k)) (deflistener m) (non-orig (privk "encr" t)) (uniq-orig m k) (comment "Experiment 1 to prove Lemma 4.1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 1 (b b) (t t) (m m) (r r) (k k)) (deflistener k) (non-orig (privk "encr" t)) (uniq-orig m k) (comment "Experiment 2 to prove Lemma 4.1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init1 3 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "First of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init3 3 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "Second of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand init5 4 (b b) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" b)) (comment "Third of three experiments to prove Lemma 4.2, clause 1."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand resp1 3 (a a) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" a)) (comment "First of two experiments to prove Lemma 4.2, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (m data) (r text) (k skey)) (defstrand resp2 4 (a a) (t t) (m m) (r r) (k k)) (non-orig (privk "sign" a)) (comment "Second of two experiments to prove Lemma 4.2, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (e1 e2 x mesg)) (defstrand resp3 4 (a a) (t t)) (non-orig (privk "sign" a)) (comment "Experiments to prove Lemma 4.2, clause 3."))`
    - `(defskeleton wang (vars (a b t hash_id name) (y x mesg)) (deflistener (enc "abcf" (enc "abrq" (l-prime y x) (privk "sign" a)) (privk "sign" t))) (non-orig (privk "sign" t)) (comment "Experiments to prove Lemma 4.3, clause 1."))`
    - `(defskeleton wang (vars (y x mesg) (a b t name)) (defstrand ttp-ab1 3 (y y) (x x) (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 1 to prove Lemma 4.3, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (r text) (k skey) (y mesg)) (defstrand ttp-rc2 3 (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 2 to prove Lemma 4.3, clause 2."))`
    - `(defskeleton wang (vars (a b t hash_id name) (r text) (k skey) (y mesg)) (defstrand ttp-cf2 3 (a a) (b b) (t t)) (non-orig (privk "sign" a) (privk "encr" t)) (comment "Experiment 3 to prove Lemma 4.3, clause 2."))`
- **When to Reference This Example**: Reference this example to compare built-in `(hash ...)` against macro-encoded tagged encryption `(defmacro (hash x) (enc "h" (cat "h" x)))` in large fair-exchange protocols.
- **Key S-Expression Excerpt**:
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
```

## weird.scm

- **File Path**: `03_examples_scm/weird.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Contrasts two protocols (`weird` using `(uniq-orig k)` and `weird-gen` using `(uniq-gen k)`) with roles `originator`, `guesser`, and `encryptor` to demonstrate why `uniq-orig` allows a `guesser` or `encryptor` to use key `k` without causal precedence, whereas `uniq-gen` enforces proper key generation ordering.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `originator` (in `weird`):
    - `vars`: `(k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(send k)`
  - Role `guesser` (in `weird`):
    - `vars`: `(k skey), (a name)` | Role assumptions: none
    - `trace`: `(send (enc a k))`
  - Role `encryptor` (in `weird`):
    - `vars`: `(k skey), (a name)` | Role assumptions: none
    - `trace`: `(recv (enc a k))`
  - Role `originator` (in `weird-gen`):
    - `vars`: `(k skey)` | Role assumptions/annotations: `(uniq-gen k)`
    - `trace`: `(send k)`
  - Role `guesser` (in `weird-gen`):
    - `vars`: `(k skey), (a name)` | Role assumptions: none
    - `trace`: `(send (enc a k))`
  - Role `encryptor` (in `weird-gen`):
    - `vars`: `(k skey), (a name)` | Role assumptions: none
    - `trace`: `(recv (enc a k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `precedes`, `recv`, `send`, `trace`, `uniq-gen`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (6)**:
    - `(defskeleton weird (vars (k skey)) (defstrand originator 1 (k k)) (defstrand guesser 1 (k k)))`
    - `(defskeleton weird (vars (k skey)) (defstrand originator 1 (k k)) (defstrand encryptor 1 (k k)))`
    - `(defskeleton weird (vars (k skey)) (defstrand originator 1 (k k)) (defstrand encryptor 1 (k k)) (precedes ((0 0) (1 0))))`
    - `(defskeleton weird-gen (vars (k skey)) (defstrand originator 1 (k k)) (defstrand guesser 1 (k k)))`
    - `(defskeleton weird-gen (vars (k skey)) (defstrand originator 1 (k k)) (defstrand encryptor 1 (k k)))`
    - `(defskeleton weird-gen (vars (k skey)) (defstrand originator 1 (k k)) (defstrand encryptor 1 (k k)) (precedes ((0 0) (1 0))))`
- **When to Reference This Example**: Reference this example when deciding between `uniq-orig` and `uniq-gen` for dynamically generated symmetric keys.
- **Key S-Expression Excerpt**:
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
```

## wonthull.scm

- **File Path**: `03_examples_scm/wonthull.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald wonthull (bound 9))` | Flags: `(bound 9)`
- **Protocol & Purpose**: Demonstrates a subtle incompleteness in CPSA's augmentation/hulling mechanism (`wonthull`, bound 9) where `init` sends `(cat (enc x1 x2 (pubk a)) (enc x3 x2 (pubk a)))` with `(uniq-orig x1 x2 x3)` and `resp` swaps components in `(enc "okay" y3 y1 (pubk a))`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `wonthull`):
    - `vars`: `(a name), (x1 x2 x3 x4 text)` | Role assumptions/annotations: `(uniq-orig x1 x2 x3)`, `(non-orig (privk a))`
    - `trace`: `(send (cat (enc x1 x2 (pubk a)) (enc x3 x2 (pubk a))))` -> `(recv (enc "okay" x3 x4 (pubk a)))`
  - Role `resp` (in `wonthull`):
    - `vars`: `(a name), (y1 y2 y3 text)` | Role assumptions: none
    - `trace`: `(recv (enc y1 y2 (pubk a)))` -> `(send (enc "okay" y3 y1 (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton wonthull (vars) (defstrand init 2))`
    - `(defskeleton wonthull (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 2 (a a) (x1 x1) (x2 x3) (x3 x3) (x4 x1)) (defstrand resp 2 (a a) (y1 x1) (y2 x3) (y3 x3)) (precedes ((0 0) (1 0)) ((1 1) (0 1))))`
- **When to Reference This Example**: Reference this example when studying CPSA's completeness boundaries regarding augmentation, deorigination, and hulling when multiple uniquely originating nonces can unify.
- **Key S-Expression Excerpt**:
```scheme
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

## wonthull2.scm

- **File Path**: `03_examples_scm/wonthull2.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald wonthull2 (bound 9))` | Flags: `(bound 9)`
- **Protocol & Purpose**: Variant of `wonthull.scm` (`wonthull2`, bound 9) where `init` sends `(cat (enc x1 x3 (pubk a)) (enc x3 x2 (pubk a)))` with only `(uniq-orig x3)`, allowing CPSA to find the shape via variable separation.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `wonthull2`):
    - `vars`: `(a name), (x1 x2 x3 x4 text)` | Role assumptions/annotations: `(uniq-orig x3)`, `(non-orig (privk a))`
    - `trace`: `(send (cat (enc x1 x3 (pubk a)) (enc x3 x2 (pubk a))))` -> `(recv (enc "okay" x3 x4 (pubk a)))`
  - Role `resp` (in `wonthull2`):
    - `vars`: `(a name), (y1 y2 y3 text)` | Role assumptions: none
    - `trace`: `(recv (enc y1 y2 (pubk a)))` -> `(send (enc "okay" y3 y1 (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton wonthull2 (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 2))`
    - `(defskeleton wonthull2 (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 2 (x2 x3) (x4 x1)) (defstrand resp 2 (y1 x1) (y2 x3) (y3 x3)) (precedes ((0 0) (1 0)) ((1 1) (0 1))))`
- **When to Reference This Example**: Reference this example alongside `wonthull.scm` and `wonthull3.scm` when analyzing how deorigination and variable separation interact during CPSA search.
- **Key S-Expression Excerpt**:
```scheme
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

## wonthull3.scm

- **File Path**: `03_examples_scm/wonthull3.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: None (no `(herald ...)` declaration in file; defaults to `basic` algebra) | Flags: none
- **Protocol & Purpose**: Third variant in the `wonthull` series (`wonthull3`) where `init` first sends `(enc x3 (pubk a))` before sending `(cat (enc x1 x2 (pubk a)) (enc x3 x2 (pubk a)))`, showing that deorigination behavior is not tied to the initial node of origination.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `wonthull3`):
    - `vars`: `(a name), (x1 x2 x3 x4 text)` | Role assumptions/annotations: `(uniq-orig x3)`, `(non-orig (privk a))`
    - `trace`: `(send (enc x3 (pubk a)))` -> `(send (cat (enc x1 x2 (pubk a)) (enc x3 x2 (pubk a))))` -> `(recv (enc "okay" x3 x4 (pubk a)))`
  - Role `resp` (in `wonthull3`):
    - `vars`: `(a name), (y1 y2 y3 text)` | Role assumptions: none
    - `trace`: `(recv (enc y1 y2 (pubk a)))` -> `(send (enc "okay" y3 y1 (pubk a)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `non-orig`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton wonthull3 (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 3))`
    - `(defskeleton wonthull3 (vars (a name) (n text) (x1 x2 x3 x4 text)) (defstrand init 3 (x2 x3) (x4 x1)) (defstrand resp 2 (y1 x1) (y2 x3) (y3 x3)) (precedes ((0 1) (1 0)) ((1 1) (0 2))))`
- **When to Reference This Example**: Reference this example when investigating how earlier origination nodes (`(send (enc x3 (pubk a)))`) affect deorigination in subsequent protocol steps.
- **Key S-Expression Excerpt**:
```scheme
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

## woolam.scm

- **File Path**: `03_examples_scm/woolam.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Woo-Lam Protocol")` | Flags: none
- **Protocol & Purpose**: Models the classic Woo-Lam unilateral authentication protocol (`woolam`) among initiator `a`, responder `b`, and server `s` using long-term symmetric keys `(ltk a s)` and `(ltk b s)`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `woolam`):
    - `vars`: `(a s name), (n text)` | Role assumptions/annotations: `(non-orig (ltk a s))`
    - `trace`: `(send a)` -> `(recv n)` -> `(send (enc n (ltk a s)))`
  - Role `resp` (in `woolam`):
    - `vars`: `(a s b name), (n text)` | Role assumptions/annotations: `(non-orig (ltk b s))`, `(uniq-orig n)`
    - `trace`: `(recv a)` -> `(send n)` -> `(recv (enc n (ltk a s)))` -> `(send (enc a (enc n (ltk a s)) (ltk b s)))` -> `(recv (enc a n (ltk b s)))`
  - Role `serv` (in `woolam`):
    - `vars`: `(a s b name), (n text)` | Role assumptions: none
    - `trace`: `(recv (enc a (enc n (ltk a s)) (ltk b s)))` -> `(send (enc a n (ltk b s)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (1)**:
    - `(defskeleton woolam (vars (n text) (a s name)) (defstrand resp 5 (a a) (s s)) (non-orig (ltk a s)))`
- **When to Reference This Example**: Reference this example when modeling symmetric-key server-mediated unilateral authentication protocols using `(ltk a s)`.
- **Key S-Expression Excerpt**:
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

## yahalom-6.3.6.scm

- **File Path**: `03_examples_scm/yahalom-6.3.6.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Yahalom Protocol" (comment "A Survey of Authentication Protocol Literature:" "Version 1.0, John Clark and Jeremy Jacob," "Yahalom Protocol, Section 6.3.6, Page 49") (url "http://www.eecs.umich.edu/acal/swerve/docs/49-1.pdf") (bound 15))` | Flags: `(comment "A Survey of Authentication Protocol Literature:" "Version 1.0, John Clark and Jeremy Jacob," "Yahalom Protocol, Section 6.3.6, Page 49")`, `(url "http://www.eecs.umich.edu/acal/swerve/docs/49-1.pdf")`, `(bound 15)`
- **Protocol & Purpose**: Models the Yahalom protocol as specified in Clark & Jacob's 'A Survey of Authentication Protocol Literature' Section 6.3.6, Page 49, where `init` receives `(cat (enc b k n-a n-b (ltk a s)) blob)` from `serv` and forwards `blob` (which is `(enc a k (ltk b s))`) alongside `(enc n-b k)` to `resp`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom`):
    - `vars`: `(a b s name), (n-a n-b text), (k skey), (blob mesg)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (cat (enc b k n-a n-b (ltk a s)) blob))` -> `(send (cat blob (enc n-b k)))`
  - Role `resp` (in `yahalom`):
    - `vars`: `(a b s name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b s))))` -> `(recv (cat (enc a k (ltk b s)) (enc n-b k)))`
  - Role `serv` (in `yahalom`):
    - `vars`: `(a b s name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b s))))` -> `(send (cat (enc b k n-a n-b (ltk a s)) (enc a k (ltk b s))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `comment`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `url`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton yahalom (vars (a b s name) (n-a n-b text)) (defstrand init 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b)) (non-orig (ltk a s) (ltk b s)) (uniq-orig n-a n-b))`
    - `(defskeleton yahalom (vars (a b s name) (n-a n-b text) (k skey)) (defstrand resp 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk a s) (ltk b s)) (uniq-orig n-a n-b))`
    - `(defskeleton yahalom (vars (a b s name) (n-a n-b text)) (defstrand resp 3 (a a) (b b) (s s) (n-a n-a) (n-b n-b)) (non-orig (ltk a s) (ltk b s)) (uniq-orig n-a n-b))`
    - `(defskeleton yahalom (vars (a b s name) (n-a n-b text)) (defstrand serv 2 (a a) (b b) (s s) (n-a n-a) (n-b n-b)) (non-orig (ltk a s) (ltk b s)) (uniq-orig n-a n-b))`
- **When to Reference This Example**: Reference this example when modeling ticket-forwarding symmetric-key distribution protocols where an untyped `mesg` variable (`blob`) represents an opaque encrypted ticket forwarded by a principal who cannot decrypt it.
- **Key S-Expression Excerpt**:
```scheme
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
```

## yahalom-forward.scm

- **File Path**: `03_examples_scm/yahalom-forward.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Yahalom Protocol With Forwarding" (bound 15))` | Flags: `(bound 15)`
- **Protocol & Purpose**: Models the Yahalom protocol with forwarding where `resp` receives `(cat (enc a k (ltk b c)) rest)` from `serv` and forwards the opaque `mesg` variable `rest` (containing `(enc b k n-a n-b (ltk a c))`) to `init`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (enc b k n-a n-b (ltk a c)))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom`):
    - `vars`: `(b a c name), (n-a n-b text), (rest mesg), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b c))))` -> `(recv (cat (enc a k (ltk b c)) rest))` -> `(send rest)` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b c))))` -> `(send (cat (enc a k (ltk b c)) (enc b k n-a n-b (ltk a c))))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (3)**:
    - `(defskeleton yahalom (vars (a b c name) (n-b text)) (defstrand resp 5 (a a) (b b) (c c) (n-b n-b)) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
    - `(defskeleton yahalom (vars (a b c name) (n-b text) (k skey)) (defstrand resp 5 (a a) (b b) (c c) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
    - `(defskeleton yahalom (vars (a b c name) (n-a text)) (defstrand init 3 (n-a n-a) (a a) (b b) (c c)) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-a))`
- **When to Reference This Example**: Reference this example when the responder (rather than the initiator) acts as the conduit forwarding an opaque server-encrypted ticket (`rest` of sort `mesg`) to the initiator.
- **Key S-Expression Excerpt**:
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

## yahalom.scm

- **File Path**: `03_examples_scm/yahalom.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Yahalom Protocol with Forwarding Removed" (bound 10))` | Flags: `(bound 10)`
- **Protocol & Purpose**: Models the Yahalom protocol with ticket forwarding removed: `serv` sends `(enc b k n-a n-b (ltk a c))` and `(enc a k (ltk b c))` as two separate messages directly to `init` and `resp` without an opaque `mesg` forwarding variable.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (enc b k n-a n-b (ltk a c)))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom`):
    - `vars`: `(b a c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b (enc a n-a n-b (ltk b c))))` -> `(recv (enc a k (ltk b c)))` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b (enc a n-a n-b (ltk b c))))` -> `(send (enc b k n-a n-b (ltk a c)))` -> `(send (enc a k (ltk b c)))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `bound`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (2)**:
    - `(defskeleton yahalom (vars (a b c name) (n-b text)) (defstrand resp 4 (a a) (b b) (c c) (n-b n-b)) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
    - `(defskeleton yahalom (vars (a b c name) (n-b text) (k skey)) (defstrand resp 4 (a a) (b b) (c c) (n-b n-b) (k k)) (deflistener k) (non-orig (ltk b c) (ltk a c)) (uniq-orig n-b))`
- **When to Reference This Example**: Reference this example to see how removing opaque ticket forwarding (`mesg` variables) simplifies state-space bounds (`(bound 10)`) and avoids state-space explosion in KDC protocols.
- **Key S-Expression Excerpt**:
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

## yes-or-no.scm

- **File Path**: `03_examples_scm/yes-or-no.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald yes-or-no)` | Flags: none
- **Protocol & Purpose**: Models a polarized query-response protocol (`yes-or-no`) where an initiator sends an encrypted question alongside two fresh `data` tokens `y` (yes) and `n` (no) under `ans-key`, and separate positive/negative roles (`init-positive`, `init-negative`, `resp-positive`, `resp-negative`) send or receive `y` or `n`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init-positive` (in `yes-or-no`):
    - `vars`: `(y n data), (question text), (ans name), (ans-key akey)` | Role assumptions: none
    - `trace`: `(send (enc question y n ans-key))` -> `(recv y)`
  - Role `init-negative` (in `yes-or-no`):
    - `vars`: `(y n data), (question text), (ans name), (ans-key akey)` | Role assumptions: none
    - `trace`: `(send (enc question y n ans-key))` -> `(recv n)`
  - Role `resp-positive` (in `yes-or-no`):
    - `vars`: `(y n data), (question text), (ans name), (ans-key akey)` | Role assumptions: none
    - `trace`: `(recv (enc question y n ans-key))` -> `(send y)`
  - Role `resp-negative` (in `yes-or-no`):
    - `vars`: `(y n data), (question text), (ans name), (ans-key akey)` | Role assumptions: none
    - `trace`: `(recv (enc question y n ans-key))` -> `(send n)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `non-orig`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton yes-or-no (vars (y data) (ans-key akey)) (defstrand init-positive 2 (y y) (ans-key ans-key)) (uniq-orig y) (non-orig (invk ans-key)))`
    - `(defskeleton yes-or-no (vars (ans-key akey) (n data)) (defstrand init-negative 2 (n n) (ans-key ans-key)) (uniq-orig n) (non-orig (invk ans-key)))`
    - `(defskeleton yes-or-no (vars (y data) (ans-key akey)) (defstrand init-positive 1 (y y) (ans-key ans-key)) (deflistener y) (uniq-orig y) (non-orig (invk ans-key)))`
    - `(defskeleton yes-or-no (vars (n data) (ans-key akey)) (defstrand init-positive 1 (n n) (ans-key ans-key)) (deflistener n) (uniq-orig n) (non-orig (invk ans-key)))`
- **When to Reference This Example**: Reference this example when modeling branching or boolean choice responses (accept/reject, yes/no) by splitting choices into distinct roles (`*-positive`, `*-negative`) and fresh capability tokens.
- **Key S-Expression Excerpt**:
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
```
````

---

### `refrences/cpsa_kb/04_examples_catalog/04_scm_examples_hackage_4_4_9.md`

*sha256:`c6384b8f5134` · 237 lines · 16.7 KB (~4,271 tokens) · lang:`markdown`*

````markdown
# Official MITRE CPSA Examples Catalog (Part 4: Hackage cpsa-4.4.9 Additional Examples)

This catalog documents the 3 additional official MITRE CPSA `.scm` example files from `cpsa-4.4.9/tst/` (`chan-mesg.scm`, `dev-subatomic-open-closed.scm`, and `devlocn.scm`). Every declaration, role, variable sort, trace event, macro, rule, goal, and skeleton is extracted directly from the source `.scm` files.

## chan-mesg.scm

- **File Path**: `03_examples_scm/chan-mesg.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Yahalom Protocol Without Forwarding" (bound 15) (comment "Testing channels as arbitrary messages."))` | Flags: `(bound 15)`, `(comment "Testing channels as arbitrary messages.")`
- **Protocol & Purpose**: Models the Yahalom protocol without forwarding while testing CPSA 4.4.9's support for arbitrary compound messages in channel positions. Instead of atomic `chan` variables, trace events use `(cat b c)`, `(cat c a)`, and `(cat c b)` as directional channel terms in `(send <chan-term> <msg>)` and `(recv <chan-term> <msg>)`, and skeletons declare `(auth (cat c b))` and `(conf (cat c b) (cat c a))` so that matching a channel automatically forces agreement on the endpoint names.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `yahalom`):
    - `vars`: `(a b c name), (n-a n-b text), (k skey)` | Role assumptions: none
    - `trace`: `(send (cat a n-a))` -> `(recv (cat c a) (cat a b k n-a n-b))` -> `(send (enc n-b k))`
  - Role `resp` (in `yahalom`):
    - `vars`: `(b a c name), (n-a n-b text), (k skey), (ch1 ch2 chan)` | Role assumptions: none
    - `trace`: `(recv (cat a n-a))` -> `(send (cat b c) (cat a b n-a n-b))` -> `(recv (cat c b) (cat a b k))` -> `(recv (enc n-b k))`
  - Role `serv` (in `yahalom`):
    - `vars`: `(c a b name), (n-a n-b text), (k skey), (ch1 ch2 ch3 chan)` | Role assumptions/annotations: `(uniq-orig k)`
    - `trace`: `(recv (cat b c) (cat a b n-a n-b))` -> `(send (cat c a) (cat a b k n-a n-b))` -> `(send (cat c b) (cat a b k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `auth`, `bound`, `comment`, `conf`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `herald`, `precedes`, `recv`, `send`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (8)**:
    - `(defskeleton yahalom (vars (a b c name) (n-b text)) (defstrand resp 4 (a a) (b b) (c c) (n-b n-b)) (auth (cat c b)) (uniq-orig n-b))`
    - `(defskeleton yahalom (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b c name)) (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (c c)) (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (c c) (a a) (b b)) (precedes ((1 2) (0 2))) (uniq-orig k n-b) (auth (cat c b)) (conf (cat c b) (cat c a)))`
    - `(defskeleton yahalom (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b c name)) (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (c c)) (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (c c) (a a) (b b)) (uniq-orig k n-b) (auth (cat c b) (cat b c)) (conf (cat c b) (cat c a)))`
    - `(defskeleton yahalom (vars (k skey) (n-b n-a n-a-0 n-b-0 text) (a b c name)) (defstrand resp 4 (k k) (n-a n-a) (n-b n-b) (b b) (a a) (c c)) (defstrand serv 3 (k k) (n-a n-a-0) (n-b n-b-0) (c c) (a a) (b b)) (deflistener k) (uniq-orig k n-b) (auth (cat c b) (cat b c)) (conf (cat c b) (cat c a)))`
    - `(defskeleton yahalom (vars (a b c name) (n-a text) (k skey)) (defstrand init 3 (n-a n-a) (c c) (a a)) (uniq-orig n-a) (auth (cat c a)))`
    - `(defskeleton yahalom (vars (k skey) (n-a n-b text) (a c b c-0 name)) (defstrand init 3 (k k) (n-a n-a) (n-b n-b) (a a) (b b) (c c)) (defstrand serv 2 (k k) (n-a n-a) (n-b n-b) (c c-0) (a a) (b b)) (precedes ((0 0) (1 0)) ((1 1) (0 1))) (uniq-orig k n-a) (auth (cat c a) (cat b c-0)) (conf (cat c-0 a)))`
    - `(defskeleton yahalom (vars (c a b name) (n-a n-b text) (k skey)) (defstrand serv 3 (a a) (b b) (c c)) (auth (cat b c)) (conf (cat c b) (cat c a)))`
    - `(defskeleton yahalom (vars (c a b name) (n-a n-b text) (k skey)) (defstrand serv 3 (k k) (a a) (b b) (c c)) (deflistener k) (auth (cat b c)) (conf (cat c b) (cat c a)))`
- **When to Reference This Example**: Reference this example when modeling point-to-point authenticated or confidential channels parameterized by principal names (`(send (cat a b) msg)`, `(auth (cat a b))`, `(conf (cat a b))`) in CPSA 4.4.9+.
- **Key S-Expression Excerpt**:
```scheme
(herald "Yahalom Protocol Without Forwarding" (bound 15)
	(comment "Testing channels as arbitrary messages."))

(defprotocol yahalom basic
  (defrole init
    (vars (a b c name) (n-a n-b text) (k skey))
    (trace (send (cat a n-a))
	   (recv (cat c a) (cat a b k n-a n-b))
	   (send (enc n-b k))))
  (defrole resp
    (vars (b a c name) (n-a n-b text) (k skey) (ch1 ch2 chan))
    (trace (recv (cat a n-a))
	   (send (cat b c) (cat a b n-a n-b))
	   (recv (cat c b) (cat a b k))
	   (recv (enc n-b k))))
  (defrole serv
    (vars (c a b name) (n-a n-b text) (k skey) (ch1 ch2 ch3 chan))
    (trace (recv (cat b c) (cat a b n-a n-b))
	   (send (cat c a) (cat a b k n-a n-b))
	   (send (cat c b) (cat a b k)))
    (uniq-orig k))
  (comment "Use (cat x y) as channel from x to y. Matching channel should force matching names."))

;;; How much do we know assuming that the resp had a run with an
;;; authenticated channel ch2?  We also assume the responder's nonce
;;; is freshly chosen.

(defskeleton yahalom
  (vars (a b c name) (n-b text))
  (defstrand resp 4 (a a) (b b) (c c) (n-b n-b))
  (auth (cat c b))
  (uniq-orig n-b))

```

## dev-subatomic-open-closed.scm

- **File Path**: `03_examples_scm/dev-subatomic-open-closed.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald dev-subatomic-open-closed (comment "Version that uses (dev const) pairs for locations"))` | Flags: `(comment "Version that uses (dev const) pairs for locations")`
- **Protocol & Purpose**: Models the stateful `subatomic-open-closed` device access-control protocol in CPSA 4.4.9+ using structured `(cat d "lk")` and `(cat d "ls")` `(dev const)` pairs (where `d` has sort `dev`) in the location position of `(load ...)` and `(stor ...)`. By embedding the device identifier `d` directly into the location term, CPSA automatically associates both state registers with device `d` without needing explicit `(facts (same-dev ls lk))` or `same-dev` rules.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `dev-up` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (d dev), (o name), (old old1 mesg), (start-ch chan)` | Role assumptions/annotations: `(auth start-ch)`
    - `trace`: `(recv start-ch (cat "power-up" o k))` -> `(stor (cat d "lk") (dev-key-state o k))` -> `(stor (cat d "ls") (dev-state-closed o))` -> `(send (enc "up" k))`
  - Role `owner-power-dev` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (o name), (start-ch chan)` | Role assumptions/annotations: `(conf start-ch)`
    - `trace`: `(send start-ch (cat "power-up" o k))` -> `(recv (enc "up" k))`
  - Role `owner-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d dev), (o name)` | Role assumptions: none
    - `trace`: `(send (enc "open" d o n k))` -> `(recv n)`
  - Role `owner-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d dev), (o name)` | Role assumptions: none
    - `trace`: `(send (enc "close" d o n k))` -> `(recv n)`
  - Role `dev-open` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d dev), (o name)` | Role assumptions/annotations: `(gen-st (dev-key-state o k) (dev-state-opened o))`
    - `trace`: `(recv (enc "open" d o n k))` -> `(load (cat d "lk") (dev-key-state o k))` -> `(stor (cat d "ls") (dev-state-opened o))` -> `(send n)`
  - Role `dev-close` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (any mesg), (d dev), (o name)` | Role assumptions/annotations: `(gen-st (dev-key-state o k))`
    - `trace`: `(recv (enc "close" d o n k))` -> `(load (cat d "lk") (dev-key-state o k))` -> `(stor (cat d "ls") (dev-state-closed o))` -> `(send n)`
  - Role `dev-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey), (n text), (d dev), (o name)` | Role assumptions/annotations: `(uniq-orig n)`, `(gen-st (dev-key-state o k) (dev-state-opened o))`
    - `trace`: `(load (cat d "lk") (dev-key-state o k))` -> `(load (cat d "ls") (dev-state-opened o))` -> `(recv (enc "may I pass" k))` -> `(send (enc "you may pass" n k))`
  - Role `user-pass` (in `subatomic-open-closed`):
    - `vars`: `(k skey)` | Role assumptions: none
    - `trace`: `(send (enc "may I pass" k))` -> `(recv (enc "you may pass" k))`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `=`, `and`, `auth`, `comment`, `conf`, `deflistener`, `defmacro`, `defprotocol`, `defrole`, `defrule`, `defskeleton`, `defstrand`, `facts`, `forall`, `gen-st`, `herald`, `implies`, `load`, `p`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros (6)**: `(dev-key-state o k)` -> `(cat "st-k" o k)`; `(opened o)` -> `(cat o o)`; `(closed o)` -> `o`; `(dev-state-opened o)` -> `(cat "st" (opened o))`; `(dev-state-closed o)` -> `(cat "st" (closed o))`; `(dev-state-any o any)` -> `(cat "st" any)`
  - **Rules & Genrules (1)**:
    - `(defrule power-deliver-once ...)` in `subatomic-open-closed`: `(forall ((z1 z2 strd) (k skey)) (implies (and (p "dev-up" z1 2) (p "dev-up" z2 2) (p "dev-up" "k" z1 k) (p "dev-up" "k" z2 k)) (= z1 z2)))`
  - **Goals**: None.
  - **Skeletons (4)**:
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (deflistener k) (uniq-orig k) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand dev-pass 4 (k k)) (facts (no-state-split) (useLocName)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand owner-power-dev 2 (k k)) (defstrand dev-pass 4 (k k)) (uniq-orig k) (facts (no-state-split)))`
    - `(defskeleton subatomic-open-closed (vars (k skey) (d o name) (n text) (start-ch chan)) (defstrand dev-pass 4 (k k)) (facts (no-state-split)))`
- **When to Reference This Example**: Reference this example when modeling multi-register stateful devices in CPSA 4.4.9+ using `(vars (d dev))` and compound location terms `(load (cat d "reg") ...)` / `(stor (cat d "reg") ...)` instead of separate `locn` variables and `same-dev` rules.
- **Key S-Expression Excerpt**:
```scheme
(defprotocol subatomic-open-closed basic
  (defrole dev-up
    (vars (k skey) (d dev) (o name) (old old1 mesg) (start-ch chan))
    (trace
     (recv start-ch (cat "power-up" o k))
     (stor (cat d "lk") (dev-key-state o k))
     (stor (cat d "ls") (dev-state-closed o))
     (send (enc "up" k)))
    (auth start-ch)
    )

  (defrole owner-power-dev
    (vars (k skey) (o name) (start-ch chan))
    (trace
     (send start-ch (cat "power-up" o k))
     (recv (enc "up" k)))
    (conf start-ch))

  (defrole owner-open
    (vars (k skey) (n text) (d dev) (o name))
    (trace
     (send (enc "open" d o n k))
     (recv n)))

  (defrole owner-close
    (vars (k skey) (n text) (d dev) (o name))
    (trace
     (send (enc "close" d o n k))
     (recv n)))

  (defrole dev-open
    (vars (k skey) (n text) (any mesg) (d dev) (o name))
    (trace
     (recv (enc "open" d o n k))
     (load (cat d "lk") (dev-key-state o k))
     (stor (cat d "ls") (dev-state-opened o))
     (send n))
    (gen-st (dev-key-state o k) (dev-state-opened o))
    )
```

## devlocn.scm

- **File Path**: `03_examples_scm/devlocn.scm`
- **Algebra & Herald**: Algebra: `basic` | Herald: `(herald "Dev and Locn" (comment "This tests the feature that allows loads and stors to have any message in their location position."))` | Flags: `(comment "This tests the feature that allows loads and stors to have any message in their location position.")`
- **Protocol & Purpose**: Tests CPSA 4.4.9's generalized location terms across three `devlocn` protocol definitions: (1) storing and loading at `(cat d l1)` / `(cat d l2)` where `d` is `dev` and `l1, l2` are `locn`; (2) testing state isolation across skeletons with `(facts (neq d1 d2))` vs. `(facts (neq l1 l2))`; and (3) loading from a generic `mesg` variable `dl` (`(load dl m)`) after acquiring `dl` in `(recv (enc dl k))`.
- **Roles & Variables**:
  - Roletran `(inputs ...)` / `(outputs ...)`: None.
  - Role `init` (in `devlocn` (definition 1)):
    - `vars`: `(d dev), (l1 l2 locn), (n1 n2 data), (k skey)` | Role assumptions/annotations: `(uniq-orig n1 n2 d)`
    - `trace`: `(stor (cat d l1) n1)` -> `(stor (cat d l2) n2)` -> `(send (enc d l1 k))` -> `(send (enc d l2 k))`
  - Role `resp` (in `devlocn` (definition 1)):
    - `vars`: `(d dev), (l locn), (m mesg), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc d l k))` -> `(load (cat d l) m)` -> `(send m)`
  - Role `init` (in `devlocn` (definition 2)):
    - `vars`: `(d dev), (l1 l2 locn), (n1 n2 data), (k skey)` | Role assumptions/annotations: `(uniq-orig n1 l1)`
    - `trace`: `(stor (cat d l1) n1)` -> `(send (enc d l1 k))`
  - Role `resp` (in `devlocn` (definition 2)):
    - `vars`: `(d dev), (l locn), (m mesg), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc d l k))` -> `(load (cat d l) m)` -> `(send m)`
  - Role `init` (in `devlocn` (definition 3)):
    - `vars`: `(d dev), (l1 l2 locn), (n1 n2 data), (k skey)` | Role assumptions/annotations: `(uniq-orig n1 l1)`
    - `trace`: `(stor (cat d l1) n1)` -> `(send (enc d l1 k))`
  - Role `resp` (in `devlocn` (definition 3)):
    - `vars`: `(d dev), (l locn), (dl m mesg), (k skey)` | Role assumptions/annotations: `(non-orig k)`
    - `trace`: `(recv (enc dl k))` -> `(load dl m)` -> `(send m)`
- **Skeletons, Goals, Rules & Macros**:
  - **Keywords Used**: `comment`, `deflistener`, `defprotocol`, `defrole`, `defskeleton`, `defstrand`, `facts`, `gen-st`, `herald`, `load`, `neq`, `non-orig`, `recv`, `send`, `stor`, `trace`, `uniq-orig`, `vars`
  - **Macros**: None.
  - **Rules & Lemmas**: None.
  - **Goals**: None.
  - **Skeletons (8)**:
    - `(defskeleton devlocn (vars (n1 n2 data)) (defstrand init 2 (n1 n1) (n2 n2)) (deflistener n1) (deflistener n2))`
    - `(defskeleton devlocn (vars (n1 n2 data)) (defstrand init 1 (n1 n1)) (defstrand init 1 (n1 n2)) (deflistener n1) (deflistener n2))`
    - `(defskeleton devlocn (vars (n1 n2 data) (d1 d2 dev)) (defstrand init 1 (n1 n1) (d d1)) (defstrand init 1 (n1 n2) (d d2)) (deflistener n1) (deflistener n2) (facts (neq d1 d2)) (comment "With different devices they cannot have the same source."))`
    - `(defskeleton devlocn (vars (n1 n2 data) (l1 l2 locn)) (defstrand init 1 (n1 n1) (l1 l1)) (defstrand init 1 (n1 n2) (l1 l2)) (deflistener n1) (deflistener n2) (facts (neq l1 l2)) (comment "With different locns they cannot have the same source."))`
    - `(defskeleton devlocn (vars (n1 n2 data) (l1 l2 locn) (d dev)) (defstrand init 1 (n1 n1) (l1 l1) (d d)) (defstrand init 1 (n1 n2) (l1 l2) (d d)) (deflistener n1) (deflistener n2) (facts (neq l1 l2)) (comment "With different locns they cannot have the same source even if the devs are the same."))`
    - `(defskeleton devlocn (vars (m mesg)) (defstrand resp 2 (m m)) (gen-st m))`
    - `(defskeleton devlocn (vars (m mesg)) (defstrand resp 2 (m m)) (comment "Possibly strange interpretation. Init has uniq-orig n1 and l1. Resp doesn't necessarily retrieve n1, even though nobody but Init should know l1, so nobody else could stor into it."))`
    - `(defskeleton devlocn (vars (n data)) (defstrand resp 2 (m n)) (defstrand init 2 (n1 n)) (comment "Even if loaded value is not gen-st, since it's uniq-orig, nonce-test still applies."))`
- **When to Reference This Example**: Reference this example when using compound `(cat d l)` or dynamically received `mesg` variables in the location slot of `(load <locn-mesg> <val>)` and `(stor <locn-mesg> <val>)`, or when reasoning about `dev` and `locn` inequality facts.
- **Key S-Expression Excerpt**:
```scheme
(herald "Dev and Locn" 
  (comment "This tests the feature that allows loads and stors to have any message in their location position."))

(defprotocol devlocn basic
  (defrole init
    (vars (d dev) (l1 l2 locn) (n1 n2 data) (k skey))
    (trace
     (stor (cat d l1) n1)
     (stor (cat d l2) n2)
     (send (enc d l1 k))
     (send (enc d l2 k)))
    (uniq-orig n1 n2 d))
  (defrole resp
    (vars (d dev) (l locn) (m mesg) (k skey))
    (trace
     (recv (enc d l k))
     (load (cat d l) m)
     (send m))
    (non-orig k))) 

(defskeleton devlocn
  (vars (n1 n2 data))
  (defstrand init 2 (n1 n1) (n2 n2))
  (deflistener n1)
  (deflistener n2))

(defprotocol devlocn basic
  (defrole init
    (vars (d dev) (l1 l2 locn) (n1 n2 data) (k skey))
    (trace
     (stor (cat d l1) n1)
     (send (enc d l1 k)))
    (uniq-orig n1 l1))
  (defrole resp
    (vars (d dev) (l locn) (m mesg) (k skey))
```
````

---
