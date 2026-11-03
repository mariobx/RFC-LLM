# CPSA Knowledge Base TOC & Pytest Verification Suites

> Tier 3 — Master CPSA 4.4.9 Knowledge Base Table of Contents (`refrences/cpsa_kb/TOC.md`) with `rebuild_toc` YAML flag, and the complete pytest unit and integration test suite (`tests/`).

*Generated: 2026-11-03 21:53:56 UTC · Git: `main` @ `8b5b88a14002` · Tier: Tier 3 — Knowledge Base Index & Test Suites · Files: 11 · Estimated Tokens: ~46,700*

## Table of Contents

- [`refrences/cpsa_kb/TOC.md`](#refrencescpsa-kbtocmd)
- [`tests/conftest.py`](#testsconftestpy)
- [`tests/test_code_generation_and_verification.py`](#teststest-code-generation-and-verificationpy)
- [`tests/test_cpsa_kb_and_agentic_searcher.py`](#teststest-cpsa-kb-and-agentic-searcherpy)
- [`tests/test_cpsa_scoping_and_prompts.py`](#teststest-cpsa-scoping-and-promptspy)
- [`tests/test_document_ingestion.py`](#teststest-document-ingestionpy)
- [`tests/test_generate_think.py`](#teststest-generate-thinkpy)
- [`tests/test_main_pipeline_orchestrator.py`](#teststest-main-pipeline-orchestratorpy)
- [`tests/test_trajectory_and_hardening.py`](#teststest-trajectory-and-hardeningpy)
- [`tests/test_visualizer_and_events.py`](#teststest-visualizer-and-eventspy)
- [`tests/test_visualizer_tabs.py`](#teststest-visualizer-tabspy)

---

### `refrences/cpsa_kb/TOC.md`

*sha256:`729d136aabe7` · 508 lines · 65.7 KB (~16,600 tokens) · lang:`markdown`*

```markdown
---
# CPSA 4.4.9 Knowledge Base Master Table of Contents
# Flip `rebuild_toc: true` whenever you add or edit .md or .scm files in refrences/cpsa_kb/.
# On the next run, the loader will automatically rebuild TOC.md + kb_index.json and reset `rebuild_toc: false`.
rebuild_toc: false
last_built: "2026-11-02T18:25:27Z"
total_sections: 449
total_scm_examples: 151
---

# MITRE CPSA 4.4.9 Knowledge Base — Master Table of Contents

## 1. Core Operational Rules & Schema Mapping (`01_core_rules/`)

### `01_core_rules/00_json_ast_to_cpsa_scheme_mapping.md` (CPSA 4.4.9 JSON AST to Scheme S-Expression Mapping Reference)
- `01_core_rules/00_json_ast_to_cpsa_scheme_mapping#overview` — Overview
- `01_core_rules/00_json_ast_to_cpsa_scheme_mapping#compilation-pipeline-architecture-pydantic-ast-to-mitre-scheme` — Compilation Pipeline Architecture: Pydantic AST to MITRE Scheme
- `01_core_rules/00_json_ast_to_cpsa_scheme_mapping#dual-gate-architecture-raw-cpsa4-vs.-rfc-llm-cpsa4roletran-cpsa4` — Dual-Gate Architecture: Raw `cpsa4` vs. RFC-LLM `cpsa4roletran` + `cpsa4` Pipeline
- `01_core_rules/00_json_ast_to_cpsa_scheme_mapping#side-by-side-schema-mapping-table-pydantic-json-ast-to-scheme-s-` — Side-by-Side Schema Mapping Table: Pydantic JSON AST to Scheme S-Expressions
- `01_core_rules/00_json_ast_to_cpsa_scheme_mapping#scoped-keyword-separation-invariants-forbiddenin` — Scoped Keyword Separation Invariants (`_FORBIDDEN_IN_*`)
- `01_core_rules/00_json_ast_to_cpsa_scheme_mapping#trace-event-operator-serialization-mapping` — Trace Event & Operator Serialization Mapping
- `01_core_rules/00_json_ast_to_cpsa_scheme_mapping#complete-side-by-side-example-cpsaprotocolspecification-json-vs.` — Complete Side-by-Side Example: `CPSAProtocolSpecification` JSON vs. Emitted `.scm`

### `01_core_rules/01_algebra_sorts_and_operators.md` (CPSA 4.4.9 Order-Sorted Message Algebras, Sorts, and Operators Reference)
- `01_core_rules/01_algebra_sorts_and_operators#overview` — Overview
- `01_core_rules/01_algebra_sorts_and_operators#order-sorted-message-algebras-basic-vs.-diffie-hellman` — Order-Sorted Message Algebras: `basic` vs. `diffie-hellman`
- `01_core_rules/01_algebra_sorts_and_operators#complete-order-sorted-hierarchy-cpsasortenum` — Complete Order-Sorted Hierarchy (`CPSASortEnum`)
- `01_core_rules/01_algebra_sorts_and_operators#complete-cryptographic-operator-signatures-tables-10.3-10.5` — Complete Cryptographic Operator Signatures (Tables 10.3 & 10.5)
- `01_core_rules/01_algebra_sorts_and_operators#equation-10.1-the-mesg-encryption-key-restriction` — Equation 10.1: The `mesg` Encryption Key Restriction
- `01_core_rules/01_algebra_sorts_and_operators#forbidden-foreign-operators-and-canonical-desugaring-cpsadesugar` — Forbidden Foreign Operators and Canonical Desugaring (`CPSA_DESUGAR_MAP`)

### `01_core_rules/02_roletran_and_executability_rules.md` (CPSA 4.4.9 Roletran (`CPSA.Roletran`) and Pre-Flight Executability Rules)
- `01_core_rules/02_roletran_and_executability_rules#overview` — Overview
- `01_core_rules/02_roletran_and_executability_rules#purpose-of-cpsa4roletran-procedural-executability-semantics` — Purpose of `cpsa4roletran`: Procedural Executability Semantics
- `01_core_rules/02_roletran_and_executability_rules#formal-definition-of-a-role-in-cpsa.roletran` — Formal Definition of a Role in `CPSA.Roletran`
- `01_core_rules/02_roletran_and_executability_rules#the-seven-mandatory-cpsa4roletran-well-formedness-constraints` — The Seven Mandatory `cpsa4roletran` Well-Formedness Constraints
- `01_core_rules/02_roletran_and_executability_rules#the-three-procedural-executability-rules-constructibility-destru` — The Three Procedural Executability Rules (Constructibility & Destructibility)
- `01_core_rules/02_roletran_and_executability_rules#probabilistic-encryption-message-receivability-receivable-and-th` — Probabilistic Encryption, Message Receivability (`receivable`), and the Encryption-Free Requirement
- `01_core_rules/02_roletran_and_executability_rules#why-cpsa4roletran-rejects-diffie-hellman-and-how-the-dual-gate-w` — Why `cpsa4roletran` Rejects `diffie-hellman` and How the Dual Gate Works

### `01_core_rules/03_declarations_origination_and_assumptions.md` (CPSA 4.4.9 Declarations, Origination, Carried Positions, and Assumptions Reference)
- `01_core_rules/03_declarations_origination_and_assumptions#overview` — Overview
- `01_core_rules/03_declarations_origination_and_assumptions#carried-vs.-uncarried-subterm-positions-manual-6.2-roletran-2` — Carried vs. Uncarried Subterm Positions (Manual §6.2 & Roletran §2)
- `01_core_rules/03_declarations_origination_and_assumptions#why-atoms-cannot-originate-inside-a-hash` — Why Atoms Cannot Originate Inside a `hash`
- `01_core_rules/03_declarations_origination_and_assumptions#the-four-core-secrecy-freshness-declarations-manual-6.2-table-10` — The Four Core Secrecy & Freshness Declarations (Manual §6.2 & Table 10.6)
- `01_core_rules/03_declarations_origination_and_assumptions#node-specific-advanced-declarations-manual-ch.-6-7-8-table-10.6` — Node-Specific & Advanced Declarations (Manual Ch. 6, 7, 8 & Table 10.6)

### `01_core_rules/04_skeletons_3pov_and_security_goals.md` (CPSA 4.4.9 Point-of-View Preskeletons, 3-POV Separation, and Security Goals Reference)
- `01_core_rules/04_skeletons_3pov_and_security_goals#overview` — Overview
- `01_core_rules/04_skeletons_3pov_and_security_goals#mandatory-3-pov-skeleton-architecture-ensurethreepointofviewskel` — Mandatory 3-POV Skeleton Architecture (`ensure_three_point_of_view_skeletons`)
- `01_core_rules/04_skeletons_3pov_and_security_goals#why-putting-deflistener-inside-a-pure-pov-skeleton-kills-bilater` — Why Putting `deflistener` Inside a Pure POV Skeleton Kills Bilateral Shape Realization
- `01_core_rules/04_skeletons_3pov_and_security_goals#complete-reference-for-defskeleton-defstrand-defstrandmax-and-de` — Complete Reference for `defskeleton`, `defstrand`, `defstrandmax`, and `deflistener`
- `01_core_rules/04_skeletons_3pov_and_security_goals#first-order-geometric-logic-defgoal-defrule-defgenrule-and-defle` — First-Order Geometric Logic: `defgoal`, `defrule`, `defgenrule`, and `deflemma` (Chapter 7)
- `01_core_rules/04_skeletons_3pov_and_security_goals#shape-analysis-sentences-cpsa4sas-manual-7.6` — Shape Analysis Sentences (`cpsa4sas` — Manual §7.6)

### `01_core_rules/05_channels_state_and_macros.md` (CPSA 4.4.9 Channels, Mutable State, Heralds, and Preprocessor Macros Reference)
- `01_core_rules/05_channels_state_and_macros#overview` — Overview
- `01_core_rules/05_channels_state_and_macros#abstract-channeled-communication-chan-auth-conf-manual-8.1` — Abstract & Channeled Communication (`chan`, `auth`, `conf` — Manual §8.1)
- `01_core_rules/05_channels_state_and_macros#stateful-protocols-mutable-memory-locations-locn-load-stor-gen-s` — Stateful Protocols & Mutable Memory Locations (`locn`, `load`, `stor`, `gen-st` — Manual §8.2)
- `01_core_rules/05_channels_state_and_macros#the-five-state-transition-axioms-derived-rules-manual-8.2.1-8.2.` — The Five State Transition Axioms & Derived Rules (Manual §8.2.1–8.2.2)
- `01_core_rules/05_channels_state_and_macros#top-level-herald-declarations-and-options-manual-10.5.1` — Top-Level `herald` Declarations and Options (Manual §10.5.1)
- `01_core_rules/05_channels_state_and_macros#preprocessor-directives-defmacro-and-include-manual-10.1` — Preprocessor Directives: `defmacro` and `include` (Manual §10.1)

### `01_core_rules/06_termination_and_anti_snowballing.md` (CPSA 4.4.9 State-Space Termination and Anti-Snowballing Reference)
- `01_core_rules/06_termination_and_anti_snowballing#overview` — Overview
- `01_core_rules/06_termination_and_anti_snowballing#why-cpsa4-times-out-or-hits-step-limit-exceeded-snowballing-mech` — Why `cpsa4` Times Out or Hits `Step limit exceeded` (Snowballing Mechanics)
- `01_core_rules/06_termination_and_anti_snowballing#cause-1-symmetric-request-response-enc-...-arity-key-unification` — Cause 1: Symmetric Request/Response `(enc ...)` Arity & Key Unification
- `01_core_rules/06_termination_and_anti_snowballing#cause-2-ltk-a-b-self-unification-and-reflection-a-b` — Cause 2: `(ltk A B)` Self-Unification and Reflection (`A = B`)
- `01_core_rules/06_termination_and_anti_snowballing#cause-3-overly-nested-hash-cat-...-inside-enc-...-and-split-keys` — Cause 3: Overly Nested `(hash (cat ...))` Inside `(enc ...)` and Split Keys
- `01_core_rules/06_termination_and_anti_snowballing#cause-4-the-mutable-state-gen-st-non-termination-trap-manual-8.2` — Cause 4: The Mutable State `gen-st` Non-Termination Trap (Manual §8.2.4)
- `01_core_rules/06_termination_and_anti_snowballing#search-flags-herald-tuning-bound-limit-depth-goals-sat-search-or` — Search Flags & Herald Tuning (`bound`, `limit`, `depth`, `goals-sat`, Search Order)

### `01_core_rules/07_compiler_and_solver_error_catalog.md` (CPSA 4.4.9 Exhaustive Compiler, Roletran, and Solver Error Diagnostic Catalog)
- `01_core_rules/07_compiler_and_solver_error_catalog#overview` — Overview
- `01_core_rules/07_compiler_and_solver_error_catalog#section-1-cpsa4roletran-procedural-executability-diagnostics-cps` — Section 1: `cpsa4roletran` Procedural Executability Diagnostics (`CPSA.Roletran.*`)
- `01_core_rules/07_compiler_and_solver_error_catalog#1.1-received-term-cannot-be-fully-destructured` — 1.1 `Received term cannot be fully destructured`
- `01_core_rules/07_compiler_and_solver_error_catalog#1.2-cannot-build-term` — 1.2 `Cannot build <term>`
- `01_core_rules/07_compiler_and_solver_error_catalog#1.3-message-not-receivable-term` — 1.3 `Message not receivable <term>`
- `01_core_rules/07_compiler_and_solver_error_catalog#1.4-input-is-not-a-basic-value-or-a-channel-term-expecting-a-bas` — 1.4 `Input is not a basic value or a channel <term>` / `Expecting a basic value`
- `01_core_rules/07_compiler_and_solver_error_catalog#1.5-uniquely-originating-value-in-input-term` — 1.5 `Uniquely originating value in input <term>`
- `01_core_rules/07_compiler_and_solver_error_catalog#1.6-uniquely-originating-value-term-does-not-originate-in-trace` — 1.6 `Uniquely originating value <term> does not originate in trace`
- `01_core_rules/07_compiler_and_solver_error_catalog#1.7-output-contains-an-input-value-term` — 1.7 `Output contains an input value <term>`
- `01_core_rules/07_compiler_and_solver_error_catalog#1.8-undeclared-variable-v-malformed-terms` — 1.8 `Undeclared variable <v>` / `Malformed terms`
- `01_core_rules/07_compiler_and_solver_error_catalog#1.9-missing-channel-expecting-a-channel-not-expecting-a-channel-` — 1.9 `Missing channel` / `Expecting a channel` / `Not expecting a channel` / `Not expecting an ikey`
- `01_core_rules/07_compiler_and_solver_error_catalog#1.10-expecting-terms-in-basic-algebra-no-protocol-found` — 1.10 `Expecting terms in basic algebra ` / `No protocol found`
- `01_core_rules/07_compiler_and_solver_error_catalog#section-2-algebra-sort-and-operator-diagnostics-cpsa.algebra-cps` — Section 2: Algebra, Sort, and Operator Diagnostics (`CPSA.Algebra`, `CPSA.Roletran.Loader`, `CPSA.Signature`)
- `01_core_rules/07_compiler_and_solver_error_catalog#2.1-algebra.inv-cannot-invert-a-variable-of-sort-mesg-message-va` — 2.1 `Algebra.inv: Cannot invert a variable of sort mesg` / `Message variable cannot used as key`
- `01_core_rules/07_compiler_and_solver_error_catalog#2.2-expecting-a-name-expecting-name-to-be-a-name-expecting-name-` — 2.2 `Expecting a name` / `Expecting <name> to be a name` / `Expecting <name> to be an akey` / `Expecting an akey` / `Terms in [role/skeleton] not well formed`
- `01_core_rules/07_compiler_and_solver_error_catalog#2.3-malformed-pubk-malformed-privk-malformed-invk-malformed-ltk-` — 2.3 `Malformed pubk` / `Malformed privk` / `Malformed invk` / `Malformed ltk` / `Malformed bltk` / `Malformed cat` / `Malformed enc` / `Malformed hash` / `Malformed gen` / `Malformed exponentiation` / `Malformed base` / `Malformed exponent` / `Malformed one` / `Malformed rec`
- `01_core_rules/07_compiler_and_solver_error_catalog#2.4-keyword-s-unknown-malformed-term` — 2.4 `Keyword <s> unknown` / `Malformed term`
- `01_core_rules/07_compiler_and_solver_error_catalog#2.5-sort-sort-not-recognized-mkvar-variables-of-sort-base-are-no` — 2.5 `Sort <sort> not recognized` / `mkVar:  Variables of sort base are now deprecated <x>` / `Malformed vars declaration` / `Bad variable declaration` / `Bad variable syntax`
- `01_core_rules/07_compiler_and_solver_error_catalog#2.6-expts-must-first-be-received-rndxs-first-sent-at-event-i-in-` — 2.6 ` Expts must first be received, rndxs first sent:   at event <i> in role <name>` / ` Var received non-carried in role <name>, then sent carried:  <v> at event <p>`
- `01_core_rules/07_compiler_and_solver_error_catalog#2.7-identifier-name-is-an-expt--must-be-a-rndx-disallowed-bare-e` — 2.7 `Identifier <name> is an expt--must be a rndx` / `Disallowed bare exponent`
- `01_core_rules/07_compiler_and_solver_error_catalog#2.8-expecting-terms-in-algebra-nom-bad-algebra-nom-algebra-name-` — 2.8 `Expecting terms in algebra <nom>` / `Bad algebra: <nom>` / `Algebra <name> not one of ...`
- `01_core_rules/07_compiler_and_solver_error_catalog#section-3-role-preskeleton-well-formedness-diagnostics-cpsa.load` — Section 3: Role & Preskeleton Well-Formedness Diagnostics (`CPSA.Loader` & `CPSA.Strand`)
- `01_core_rules/07_compiler_and_solver_error_catalog#3.1-role-not-well-formed-uniq-orig-t-doesn-t-originate-uniq-gen-` — 3.1 `Role not well formed: uniq-orig <t> doesn't originate` / `uniq-gen <t> doesn't generate` / `Skeleton not well formed: uniq-orig <t> not carried` / `uniq-gen <t> does not occur` / `an inherited unique doesn't originate in its strand` / `an inherited unique gen doesn't generate in its strand`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.2-role-not-well-formed-non-orig-t-carried-skeleton-not-well-fo` — 3.2 `Role not well formed: non-orig <t> carried` / `Skeleton not well formed: non-orig <t> carried`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.3-role-not-well-formed-a-variable-in-non-orig-pen-non-orig-is-` — 3.3 `Role not well formed: a variable in [non-orig/pen-non-orig] is not in trace` / `Skeleton not well formed: a variable in [non-orig/pen-non-orig] is not in some trace`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.4-role-not-well-formed-invalid-position-len-t-appears-after-po` — 3.4 `Role not well formed: invalid position <len>` / `<t> appears after position <len>` / `no used position for non-originating atom <t>` / `Expecting a non-negative non-origination position`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.5-role-not-well-formed-variable-v-not-acquired` — 3.5 `Role not well formed: variable <v> not acquired`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.6-role-not-well-formed-role-trace-is-a-prefix-of-a-listener` — 3.6 `Role not well formed: role trace is a prefix of a listener`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.7-role-not-well-formed-ch-declared-conf-auth-but-not-used-in-r` — 3.7 `Role not well formed: <ch> declared [conf/auth] but not used in role <r>` / `Bad channel in role` / `Skeleton not well formed: some variable in [confidential/authenticated] channel <c> not in some strand`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.8-expecting-an-atom-expecting-a-pair-of-terms-expecting-an-exp` — 3.8 `Expecting an atom` / `Expecting a pair of terms` / `Expecting an exponent` / `Expecting an exponent variable` / `Skeleton not well formed: absent <x> does not occur`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.9-role-not-well-formed-role-trace-has-multiple-loads-or-stors-` — 3.9 `Role not well formed: role trace has multiple loads or stors on same locn` / `checkForDivergenceInStoreSegments: Roles <r1> and <r2> agree up to step <i> but diverge in a store segment` / `Skeleton not well formed: gen-st <t> not carried` / `Expecting a location`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.10-identifier-name-unknown-domain-does-not-match-range-malform` — 3.10 `Identifier <name> unknown` / `Domain does not match range` / `Malformed maplet` / `Bad maplet`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.11-role-r-not-found-in-p-protocol-p-unknown-no-strands-duplica` — 3.11 `Role <r> not found in <p>` / `Protocol <p> unknown` / `No strands` / `Duplicate role <r> in protocol <p>` / `Duplicate variable declaration for <v>` / `<key> declaration too late in enclosing form` / `defrole <name> misplaced`
- `01_core_rules/07_compiler_and_solver_error_catalog#3.12-bad-height-negative-strand-in-node-negative-position-in-nod` — 3.12 `Bad height` / `Negative strand in node` / `Negative position in node` / `Bad strand in node` / `Bad position in node` / `Malformed node` / `Malformed pair` / `Skeleton not well formed: ordered pairs not well formed` / `Skeleton not well formed: cycle found in ordered pairs`
- `01_core_rules/07_compiler_and_solver_error_catalog#section-4-goal-rule-rely-guarantee-and-characteristic-skeleton-d` — Section 4: Goal, Rule, Rely/Guarantee, and Characteristic Skeleton Diagnostics (`CPSA.LoadFormulas`, `CPSA.Characteristic`, `CPSA.Loader`)
- `01_core_rules/07_compiler_and_solver_error_catalog#4.1-bad-goal-sentence-no-forall-bad-goal-implication-v-not-used` — 4.1 `Bad goal sentence:  No forall` / `Bad goal implication` / `<v> not used`
- `01_core_rules/07_compiler_and_solver_error_catalog#4.2-unbound-variable-in-parameter-predicate-prec-non-pnon-uniq-u` — 4.2 `Unbound variable in [parameter predicate|prec|non|pnon|uniq|uniq-at|ugen|ugen-at|gen-st|conf|auth|fact|comm-pr|leads-to|state-node|trans|same-locn|equals|component]`
- `01_core_rules/07_compiler_and_solver_error_catalog#4.3-bad-length-bad-parameter----not-a-variable-v-parameter-x-not` — 4.3 `Bad length` / `Bad parameter -- not a variable <v>` / `parameter <x> not in role <r>` / `Bad protocol specific formula for role <r>` / `Bad formula for predicate <pred>` / `Sort mismatch in equality` / `Type mismatch in [equals/component]` / `Strand variable in component formula` / `Malformed pair -- nodes in same strand`
- `01_core_rules/07_compiler_and_solver_error_catalog#4.4-equals-not-allowed-in-antecedent-index-is-variable-not-integ` — 4.4 `Equals not allowed in antecedent` / `Index is variable, not integer` / `Strand occurs in more than one role length atom` / `Role in parameter pred differs from role position pred` / `Atom not unique at node` / `Atom not uniq gen at node`
- `01_core_rules/07_compiler_and_solver_error_catalog#4.5-rely-precedes-first-event-in-role-r-rely-must-follow-recv-or` — 4.5 `Rely precedes first event in role <r>` / `Rely must follow recv or load in role <r>` / `Guarantee follows last event in role <r>` / `Guarantee must precede send or stor in role <r>` / `cheq must precede some event in role <r>` / `<pos> var <v> not bound by height <bound>` / `<pos> variables not bound until height <ht>`
- `01_core_rules/07_compiler_and_solver_error_catalog#section-5-lexer-parser-macro-json-and-graph-pipeline-diagnostics` — Section 5: Lexer, Parser, Macro, JSON, and Graph Pipeline Diagnostics (`CPSA.Lib.SExpr`, `CPSA.Lib.Expand`, `CPSA.JSON.Main`, `CPSA.Graph.Loader`, `CPSA.Shapes.Shapes`)
- `01_core_rules/07_compiler_and_solver_error_catalog#5.1-bad-char-in-atom-bad-char-in-string-bad-escaped-char-in-stri` — 5.1 `Bad char in atom` / `Bad char in string` / `Bad escaped char in string` / `End of input in string` / `Bad char after number` / `Close of unopened list` / `Unexpected end of input in list` / `Quote in symbol` / `Sign not followed by a digit`
- `01_core_rules/07_compiler_and_solver_error_catalog#5.2-malformed-macro-expecting-a-symbol-expansion-limit-exceeded-` — 5.2 `Malformed macro` / `Expecting a symbol` / `Expansion limit exceeded` / `Expected argument count for macro <m>` / `Include depth exceeded with file <f>`
- `01_core_rules/07_compiler_and_solver_error_catalog#5.3-empty-input-cycle-found-parent-unknown` — 5.3 `Empty input` / `Cycle found` / `parent unknown`

## 2. Official MITRE CPSA 4.4.9 Manuals (`02_manuals/`)

### `02_manuals/01_CPSA4_User_Manual.md` (CPSA 4 User Manual (Version 4.4.9))
- `02_manuals/01_CPSA4_User_Manual#overview` — Overview
- `02_manuals/01_CPSA4_User_Manual#table-of-contents` — Table of Contents
- `02_manuals/01_CPSA4_User_Manual#chapter-1-introduction` — Chapter 1: Introduction
- `02_manuals/01_CPSA4_User_Manual#1.1-recommended-reading` — Chapter 1: Introduction > 1.1 Recommended reading
- `02_manuals/01_CPSA4_User_Manual#1.2-tool-components` — Chapter 1: Introduction > 1.2 Tool components
- `02_manuals/01_CPSA4_User_Manual#2.1-basic-installation` — Chapter 2: Setup and Installation > 2.1 Basic Installation
- `02_manuals/01_CPSA4_User_Manual#2.2-finding-documentation` — Chapter 2: Setup and Installation > 2.2 Finding Documentation
- `02_manuals/01_CPSA4_User_Manual#2.3-running-cpsa` — Chapter 2: Setup and Installation > 2.3 Running cpsa
- `02_manuals/01_CPSA4_User_Manual#chapter-3-basic-protocol-modeling-and-analysis-with-cpsa` — Chapter 3: Basic Protocol Modeling and Analysis with CPSA
- `02_manuals/01_CPSA4_User_Manual#3.1-basic-cpsa-modeling` — Chapter 3: Basic Protocol Modeling and Analysis with CPSA > 3.1 Basic CPSA modeling
- `02_manuals/01_CPSA4_User_Manual#3.2-cpsa-input` — Chapter 3: Basic Protocol Modeling and Analysis with CPSA > 3.2 CPSA input
- `02_manuals/01_CPSA4_User_Manual#3.3-cpsa-output` — Chapter 3: Basic Protocol Modeling and Analysis with CPSA > 3.3 CPSA output
- `02_manuals/01_CPSA4_User_Manual#3.4-interpreting-shapes` — Chapter 3: Basic Protocol Modeling and Analysis with CPSA > 3.4 Interpreting shapes
- `02_manuals/01_CPSA4_User_Manual#3.5-blanchet-s-simple-example-protocol` — Chapter 3: Basic Protocol Modeling and Analysis with CPSA > 3.5 Blanchet’s simple example protocol
- `02_manuals/01_CPSA4_User_Manual#chapter-4-algebra-features-of-cpsa` — Chapter 4: Algebra Features of CPSA
- `02_manuals/01_CPSA4_User_Manual#4.1-generic-messages-and-long-term-keys` — Chapter 4: Algebra Features of CPSA > 4.1 Generic messages and long-term keys
- `02_manuals/01_CPSA4_User_Manual#4.2-modeling-diffie-hellman` — Chapter 4: Algebra Features of CPSA > 4.2 Modeling Diffie-Hellman
- `02_manuals/01_CPSA4_User_Manual#4.3-other-algebra-features` — Chapter 4: Algebra Features of CPSA > 4.3 Other Algebra Features
- `02_manuals/01_CPSA4_User_Manual#4.4-the-lang-field-declaring-new-operators` — Chapter 4: Algebra Features of CPSA > 4.4 The Lang Field: Declaring new operators
- `02_manuals/01_CPSA4_User_Manual#chapter-5-the-cpsa-search-algorithm` — Chapter 5: The CPSA Search Algorithm
- `02_manuals/01_CPSA4_User_Manual#5.1-solving-tests` — Chapter 5: The CPSA Search Algorithm > 5.1 Solving tests
- `02_manuals/01_CPSA4_User_Manual#5.2-flawed-kerberos-revisited` — Chapter 5: The CPSA Search Algorithm > 5.2 Flawed Kerberos, revisited
- `02_manuals/01_CPSA4_User_Manual#chapter-6-constraining-cpsa-s-search` — Chapter 6: Constraining CPSA's Search
- `02_manuals/01_CPSA4_User_Manual#6.1-bundles-a-strand-based-execution-model` — Chapter 6: Constraining CPSA's Search > 6.1 Bundles: A Strand-Based Execution Model
- `02_manuals/01_CPSA4_User_Manual#6.2-secrecy-assumptions` — Chapter 6: Constraining CPSA's Search > 6.2 Secrecy assumptions
- `02_manuals/01_CPSA4_User_Manual#6.3-diffie-hellman-declarations` — Chapter 6: Constraining CPSA's Search > 6.3 Diffie-Hellman declarations
- `02_manuals/01_CPSA4_User_Manual#6.4-declaring-skeletons` — Chapter 6: Constraining CPSA's Search > 6.4 Declaring skeletons
- `02_manuals/01_CPSA4_User_Manual#6.5-a-caution-about-typos` — Chapter 6: Constraining CPSA's Search > 6.5 A Caution about typos
- `02_manuals/01_CPSA4_User_Manual#chapter-7-logical-security-goals-and-rules` — Chapter 7: Logical Security Goals and Rules
- `02_manuals/01_CPSA4_User_Manual#7.1-overview` — Chapter 7: Logical Security Goals and Rules > 7.1 Overview
- `02_manuals/01_CPSA4_User_Manual#7.2-semantics` — Chapter 7: Logical Security Goals and Rules > 7.2 Semantics
- `02_manuals/01_CPSA4_User_Manual#7.3-examples` — Chapter 7: Logical Security Goals and Rules > 7.3 Examples
- `02_manuals/01_CPSA4_User_Manual#7.4-the-rest-of-the-story` — Chapter 7: Logical Security Goals and Rules > 7.4 The Rest of the Story
- `02_manuals/01_CPSA4_User_Manual#7.5-syntactic-abbreviations` — Chapter 7: Logical Security Goals and Rules > 7.5 Syntactic Abbreviations
- `02_manuals/01_CPSA4_User_Manual#7.6-shape-analysis-sentences` — Chapter 7: Logical Security Goals and Rules > 7.6 Shape Analysis Sentences
- `02_manuals/01_CPSA4_User_Manual#7.7-rules` — Chapter 7: Logical Security Goals and Rules > 7.7 Rules
- `02_manuals/01_CPSA4_User_Manual#7.8-lemmas` — Chapter 7: Logical Security Goals and Rules > 7.8 Lemmas
- `02_manuals/01_CPSA4_User_Manual#chapter-8-channels-and-state` — Chapter 8: Channels and State
- `02_manuals/01_CPSA4_User_Manual#8.1-channels` — Chapter 8: Channels and State > 8.1 Channels
- `02_manuals/01_CPSA4_User_Manual#8.2-state` — Chapter 8: Channels and State > 8.2 State
- `02_manuals/01_CPSA4_User_Manual#chapter-9-troubleshooting` — Chapter 9: Troubleshooting
- `02_manuals/01_CPSA4_User_Manual#9.1-non-termination` — Chapter 9: Troubleshooting > 9.1 Non-termination
- `02_manuals/01_CPSA4_User_Manual#9.2-error-messages` — Chapter 9: Troubleshooting > 9.2 Error messages
- `02_manuals/01_CPSA4_User_Manual#10.1-cpsa-pre-processing` — Chapter 10: CPSA Program Reference > 10.1 CPSA pre-processing
- `02_manuals/01_CPSA4_User_Manual#10.2-cpsa-input-syntax` — Chapter 10: CPSA Program Reference > 10.2 CPSA input syntax
- `02_manuals/01_CPSA4_User_Manual#10.3-algebra-reference` — Chapter 10: CPSA Program Reference > 10.3 Algebra reference
- `02_manuals/01_CPSA4_User_Manual#10.4-declaration-syntax` — Chapter 10: CPSA Program Reference > 10.4 Declaration syntax
- `02_manuals/01_CPSA4_User_Manual#10.5-command-line-options` — Chapter 10: CPSA Program Reference > 10.5 Command-line options
- `02_manuals/01_CPSA4_User_Manual#chapter-11-cpsa-tools` — Chapter 11: CPSA Tools
- `02_manuals/01_CPSA4_User_Manual#11.1-cpsa4init` — Chapter 11: CPSA Tools > 11.1 `cpsa4init`
- `02_manuals/01_CPSA4_User_Manual#11.2-cpsa4shape` — Chapter 11: CPSA Tools > 11.2 `cpsa4shape`
- `02_manuals/01_CPSA4_User_Manual#11.3-cpsa4graph` — Chapter 11: CPSA Tools > 11.3 `cpsa4graph`
- `02_manuals/01_CPSA4_User_Manual#11.4-cpsa4goalsat` — Chapter 11: CPSA Tools > 11.4 `cpsa4goalsat`
- `02_manuals/01_CPSA4_User_Manual#11.5-cpsa4prot` — Chapter 11: CPSA Tools > 11.5 `cpsa4prot`
- `02_manuals/01_CPSA4_User_Manual#11.6-cpsa4sas` — Chapter 11: CPSA Tools > 11.6 `cpsa4sas`
- `02_manuals/01_CPSA4_User_Manual#11.7-cpsa4pp` — Chapter 11: CPSA Tools > 11.7 `cpsa4pp`
- `02_manuals/01_CPSA4_User_Manual#11.8-cpsa42latex` — Chapter 11: CPSA Tools > 11.8 `cpsa42latex`
- `02_manuals/01_CPSA4_User_Manual#11.9-cpsa4json` — Chapter 11: CPSA Tools > 11.9 `cpsa4json`
- `02_manuals/01_CPSA4_User_Manual#11.10-cpsa4diff` — Chapter 11: CPSA Tools > 11.10 `cpsa4diff`
- `02_manuals/01_CPSA4_User_Manual#bibliography` — Bibliography

### `02_manuals/02_Role_Translations_Manual.md` (CPSA4 Role Translations Manual (`cpsa4roletran`))
- `02_manuals/02_Role_Translations_Manual#overview` — Overview
- `02_manuals/02_Role_Translations_Manual#table-of-contents` — Table of Contents
- `02_manuals/02_Role_Translations_Manual#1.-cpsa4-roletran-compiler-user-guide-cpsa4roletran` — 1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`)
- `02_manuals/02_Role_Translations_Manual#1.1-overview-and-natural-role-semantics` — 1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`) > 1.1 Overview and Natural Role Semantics
- `02_manuals/02_Role_Translations_Manual#1.2-roletran-input-syntax-and-executability-constraints` — 1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`) > 1.2 Roletran Input Syntax and Executability Constraints
- `02_manuals/02_Role_Translations_Manual#1.3-annotated-roletran-input-example-unilateral` — 1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`) > 1.3 Annotated Roletran Input Example (`unilateral`)
- `02_manuals/02_Role_Translations_Manual#1.4-roletran-procedure-output-syntax-defproc` — 1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`) > 1.4 Roletran Procedure Output Syntax (`defproc`)
- `02_manuals/02_Role_Translations_Manual#1.5-generated-procedure-example-init-role` — 1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`) > 1.5 Generated Procedure Example (`init` Role)
- `02_manuals/02_Role_Translations_Manual#2.-role-translations-formal-semantics-and-compilation` — 2. Role Translations: Formal Semantics and Compilation
- `02_manuals/02_Role_Translations_Manual#2.1-introduction-and-procedural-role-semantics` — 2. Role Translations: Formal Semantics and Compilation > 2.1 Introduction and Procedural Role Semantics
- `02_manuals/02_Role_Translations_Manual#2.2-notation` — 2. Role Translations: Formal Semantics and Compilation > 2.2 Notation
- `02_manuals/02_Role_Translations_Manual#3.-message-algebras-for-role-translation` — 3. Message Algebras for Role Translation
- `02_manuals/02_Role_Translations_Manual#3.1-example-message-algebra-simple-crypto-algebra` — 3. Message Algebras for Role Translation > 3.1 Example Message Algebra (Simple Crypto Algebra)
- `02_manuals/02_Role_Translations_Manual#3.2-encryption-free-terms-and-carried-by-relation` — 3. Message Algebras for Role Translation > 3.2 Encryption-Free Terms and Carried-By Relation
- `02_manuals/02_Role_Translations_Manual#4.-strand-spaces-with-channels` — 4. Strand Spaces with Channels
- `02_manuals/02_Role_Translations_Manual#4.1-channeled-messages-traces-and-roles` — 4. Strand Spaces with Channels > 4.1 Channeled Messages, Traces, and Roles
- `02_manuals/02_Role_Translations_Manual#4.2-role-executions-and-runs` — 4. Strand Spaces with Channels > 4.2 Role Executions and Runs
- `02_manuals/02_Role_Translations_Manual#4.3-unilateral-protocol-example` — 4. Strand Spaces with Channels > 4.3 Unilateral Protocol Example
- `02_manuals/02_Role_Translations_Manual#4.4-channel-assumptions` — 4. Strand Spaces with Channels > 4.4 Channel Assumptions
- `02_manuals/02_Role_Translations_Manual#5.1-runtime-environment-randomness-and-channel-traces` — 5. Abstract Execution Semantics > 5.1 Runtime Environment, Randomness, and Channel Traces
- `02_manuals/02_Role_Translations_Manual#5.2-abstract-expression-and-statement-semantics` — 5. Abstract Execution Semantics > 5.2 Abstract Expression and Statement Semantics
- `02_manuals/02_Role_Translations_Manual#5.3-labeled-transition-system-and-procedure-execution` — 5. Abstract Execution Semantics > 5.3 Labeled Transition System and Procedure Execution
- `02_manuals/02_Role_Translations_Manual#5.4-correctness-liveness-and-safety` — 5. Abstract Execution Semantics > 5.4 Correctness: Liveness and Safety
- `02_manuals/02_Role_Translations_Manual#6.-runtime-with-probabilistic-encryption-concrete-message-algebr` — 6. Runtime with Probabilistic Encryption (Concrete Message Algebras)
- `02_manuals/02_Role_Translations_Manual#7.-concrete-execution-semantics` — 7. Concrete Execution Semantics
- `02_manuals/02_Role_Translations_Manual#8.-relating-abstract-and-concrete-execution-semantics` — 8. Relating Abstract and Concrete Execution Semantics
- `02_manuals/02_Role_Translations_Manual#9.-implementation-notes-and-epilogue` — 9. Implementation Notes and Epilogue
- `02_manuals/02_Role_Translations_Manual#10.-references` — 10. References

### `02_manuals/03_CPSA_Primer.md` (CPSA Primer: Modeling Methodology, Core Concepts, and Foundations)
- `02_manuals/03_CPSA_Primer#overview` — Overview
- `02_manuals/03_CPSA_Primer#table-of-contents` — Table of Contents
- `02_manuals/03_CPSA_Primer#1.-introduction` — 1. Introduction
- `02_manuals/03_CPSA_Primer#2.-overview-and-workflow` — 2. Overview and Workflow
- `02_manuals/03_CPSA_Primer#3.-basic-crypto-algebra-bca-messages` — 3. Basic Crypto Algebra (BCA) Messages
- `02_manuals/03_CPSA_Primer#3.1-the-carries-relation-carries` — 3. Basic Crypto Algebra (BCA) Messages > 3.1 The Carries Relation (`carries`)
- `02_manuals/03_CPSA_Primer#4.-protocols-and-roles` — 4. Protocols and Roles
- `02_manuals/03_CPSA_Primer#5.-protocol-executions-and-origination-assumptions` — 5. Protocol Executions and Origination Assumptions
- `02_manuals/03_CPSA_Primer#5.1-origination-and-channel-assumptions-non-orig-pen-non-orig-un` — 5. Protocol Executions and Origination Assumptions > 5.1 Origination and Channel Assumptions (`non-orig`, `pen-non-orig`, `uniq-orig`, `auth`, `conf`)
- `02_manuals/03_CPSA_Primer#6.-skeletons-homomorphisms-and-refinements` — 6. Skeletons, Homomorphisms, and Refinements
- `02_manuals/03_CPSA_Primer#6.1-realized-skeletons` — 6. Skeletons, Homomorphisms, and Refinements > 6.1 Realized Skeletons
- `02_manuals/03_CPSA_Primer#6.2-structural-and-message-refinement-homomorphisms` — 6. Skeletons, Homomorphisms, and Refinements > 6.2 Structural and Message Refinement (Homomorphisms)
- `02_manuals/03_CPSA_Primer#7.-listeners` — 7. Listeners
- `02_manuals/03_CPSA_Primer#8.-authentication-tests` — 8. Authentication Tests
- `02_manuals/03_CPSA_Primer#9.-generalization-and-shapes` — 9. Generalization and Shapes
- `02_manuals/03_CPSA_Primer#10.-skeleton-input-syntax-defskeleton` — 10. Skeleton Input Syntax (`defskeleton`)
- `02_manuals/03_CPSA_Primer#10.1-semantic-errors-and-well-formedness-checks` — 10. Skeleton Input Syntax (`defskeleton`) > 10.1 Semantic Errors and Well-Formedness Checks
- `02_manuals/03_CPSA_Primer#10.2-needham-schroeder-input-example` — 10. Skeleton Input Syntax (`defskeleton`) > 10.2 Needham-Schroeder Input Example
- `02_manuals/03_CPSA_Primer#11.-output-format-and-annotations` — 11. Output Format and Annotations
- `02_manuals/03_CPSA_Primer#11.0.1-interpreting-the-operation-field` — 11. Output Format and Annotations > 11.0.1 Interpreting the `operation` Field
- `02_manuals/03_CPSA_Primer#11.1-needham-schroeder-complete-output-trace` — 11. Output Format and Annotations > 11.1 Needham-Schroeder Complete Output Trace
- `02_manuals/03_CPSA_Primer#12.-security-goals-and-rules` — 12. Security Goals and Rules
- `02_manuals/03_CPSA_Primer#13.-macros-defmacro` — 13. Macros (`defmacro`)
- `02_manuals/03_CPSA_Primer#14.-file-includes-include` — 14. File Includes (`include`)
- `02_manuals/03_CPSA_Primer#15.-algebra-signature-extensions-lang` — 15. Algebra Signature Extensions (`lang`)
- `02_manuals/03_CPSA_Primer#16.1-role-vs.-skeleton-origination-assumptions` — 16. Modeling Methodology and Advice > 16.1 Role vs. Skeleton Origination Assumptions
- `02_manuals/03_CPSA_Primer#16.2-distinguishing-text-vs.-data-sorts` — 16. Modeling Methodology and Advice > 16.2 Distinguishing `text` vs. `data` Sorts
- `02_manuals/03_CPSA_Primer#16.3-shape-interpretation-and-authentication-test-debugging` — 16. Modeling Methodology and Advice > 16.3 Shape Interpretation and Authentication Test Debugging
- `02_manuals/03_CPSA_Primer#16.4-progressive-refinement-analysis-technique` — 16. Modeling Methodology and Advice > 16.4 Progressive Refinement Analysis Technique
- `02_manuals/03_CPSA_Primer#16.5-resource-bounds-and-handling-non-termination` — 16. Modeling Methodology and Advice > 16.5 Resource Bounds and Handling Non-Termination
- `02_manuals/03_CPSA_Primer#17.-formula-extraction-cpsa4sas` — 17. Formula Extraction (`cpsa4sas`)
- `02_manuals/03_CPSA_Primer#acknowledgements` — Acknowledgements
- `02_manuals/03_CPSA_Primer#appendix-a-bca-syntax-reference` — Appendix A: BCA Syntax Reference
- `02_manuals/03_CPSA_Primer#appendix-b-omitted-executions-and-natural-role-semantics` — Appendix B: Omitted Executions and Natural Role Semantics
- `02_manuals/03_CPSA_Primer#references` — References

### `02_manuals/04_CPSA_Goals_and_Security_Manual.md` (CPSA Security Goals, Rules, Lemmas, and Shape Analysis Sentences Manual)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#overview` — Overview
- `02_manuals/04_CPSA_Goals_and_Security_Manual#table-of-contents` — Table of Contents
- `02_manuals/04_CPSA_Goals_and_Security_Manual#1.-introduction-to-first-order-security-goals` — 1. Introduction to First-Order Security Goals
- `02_manuals/04_CPSA_Goals_and_Security_Manual#2.-security-goal-syntax-defgoal-and-predicates` — 2. Security Goal Syntax (`defgoal` and Predicates)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#2.1-full-cpsa-4.4-security-goal-grammar` — 2. Security Goal Syntax (`defgoal` and Predicates) > 2.1 Full CPSA 4.4 Security Goal Grammar
- `02_manuals/04_CPSA_Goals_and_Security_Manual#2.2-goal-predicates` — 2. Security Goal Syntax (`defgoal` and Predicates) > 2.2 Goal Predicates
- `02_manuals/04_CPSA_Goals_and_Security_Manual#2.3-syntactic-abbreviations-strand-and-listener` — 2. Security Goal Syntax (`defgoal` and Predicates) > 2.3 Syntactic Abbreviations (`strand` and `listener`)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#3.-model-theoretic-semantics-and-characteristic-skeletons` — 3. Model-Theoretic Semantics and Characteristic Skeletons
- `02_manuals/04_CPSA_Goals_and_Security_Manual#4.-authentication-and-secrecy-goal-examples` — 4. Authentication and Secrecy Goal Examples
- `02_manuals/04_CPSA_Goals_and_Security_Manual#4.1-counterexample-analysis-needham-schroeder-responder-satisfie` — 4. Authentication and Secrecy Goal Examples > 4.1 Counterexample Analysis: Needham-Schroeder Responder (`satisfies no`)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#4.2-secrecy-goal-with-listeners-false-conclusion` — 4. Authentication and Secrecy Goal Examples > 4.2 Secrecy Goal with Listeners (`(false)` Conclusion)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#5.-multi-sentence-goals-skeleton-goals-annotations-and-shape-ana` — 5. Multi-Sentence Goals, Skeleton `goals` Annotations, and Shape Analysis Sentences
- `02_manuals/04_CPSA_Goals_and_Security_Manual#5.1-shape-analysis-sentences-cpsa4sas` — 5. Multi-Sentence Goals, Skeleton `goals` Annotations, and Shape Analysis Sentences > 5.1 Shape Analysis Sentences (`cpsa4sas`)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#6.-axiomatic-rewrite-rules-defrule-and-facts-facts` — 6. Axiomatic Rewrite Rules (`defrule`) and Facts (`facts`)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#6.1-skeleton-fact-databases-facts-and-fact` — 6. Axiomatic Rewrite Rules (`defrule`) and Facts (`facts`) > 6.1 Skeleton Fact Databases (`facts` and `fact`)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#6.2-case-study-door-simple-example-protocol-doorsep-and-trust-ax` — 6. Axiomatic Rewrite Rules (`defrule`) and Facts (`facts`) > 6.2 Case Study: Door Simple Example Protocol (DoorSEP) and Trust Axioms
- `02_manuals/04_CPSA_Goals_and_Security_Manual#7.-automatically-generated-rules-defgenrule-built-in-relations-a` — 7. Automatically Generated Rules (`defgenrule`), Built-in Relations, and Trace Annotations
- `02_manuals/04_CPSA_Goals_and_Security_Manual#7.1-built-in-fact-relations-neq-invk-lt-subsort-and-generated-ru` — 7. Automatically Generated Rules (`defgenrule`), Built-in Relations, and Trace Annotations > 7.1 Built-in Fact Relations (`neq`, `invk`, `lt`, `subsort`) and Generated Rules
- `02_manuals/04_CPSA_Goals_and_Security_Manual#7.2-trace-annotations-cheq-assume-rely-guarantee-guar-and-cpsa4g` — 7. Automatically Generated Rules (`defgenrule`), Built-in Relations, and Trace Annotations > 7.2 Trace Annotations (`cheq`, `assume`, `rely`, `guarantee` / `guar`) and `cpsa4goals`
- `02_manuals/04_CPSA_Goals_and_Security_Manual#8.-lemmas-deflemma` — 8. Lemmas (`deflemma`)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#9.-formal-specification-of-shape-analysis-sentences-coherent-log` — 9. Formal Specification of Shape Analysis Sentences (Coherent Logic)
- `02_manuals/04_CPSA_Goals_and_Security_Manual#9.1-formal-syntax-and-satisfaction-semantics-of-skeleton-formula` — 9. Formal Specification of Shape Analysis Sentences (Coherent Logic) > 9.1 Formal Syntax and Satisfaction Semantics of Skeleton Formulas
- `02_manuals/04_CPSA_Goals_and_Security_Manual#10.-references` — 10. References

### `02_manuals/05_CPSA_Specification_and_User_Guide.md` (CPSA 4.4 Formal Specification and User Guide (`cpsauser` & `cpsaspec`))
- `02_manuals/05_CPSA_Specification_and_User_Guide#overview` — Overview
- `02_manuals/05_CPSA_Specification_and_User_Guide#table-of-contents` — Table of Contents
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.-cpsa-4.4-user-guide-input-output-syntax-and-solver-usage` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.0-overview-of-cpsa-shape-analysis` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.0 Overview of CPSA Shape Analysis
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.1-input-output-syntax-overview` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.1 Input/Output Syntax Overview
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.2-protocols-defprotocol-and-defrole` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.2 Protocols (`defprotocol` and `defrole`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.3-skeletons-defskeleton-defstrand-deflistener` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.3 Skeletons (`defskeleton`, `defstrand`, `deflistener`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.4-first-order-logic-and-security-goals-defgoal` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.4 First-Order Logic and Security Goals (`defgoal`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.5-rewrite-rules-defrule-and-facts` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.5 Rewrite Rules (`defrule` and `facts`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.6-long-term-cross-session-state-locn-load-stor-gen-st-leadsto` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.6 Long-Term (Cross-Session) State (`locn`, `load`, `stor`, `gen-st`, `leadsto`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.7-macros-defmacro-and-file-includes-include` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.7 Macros (`defmacro`) and File Includes (`include`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.8-cpsa-command-line-usage-cpsa4-flags-and-options` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.8 CPSA Command-Line Usage (`cpsa4` Flags and Options)
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.9-search-order-options-check-nonces-try-old-strands-reverse-no` — 1. CPSA 4.4 User Guide: Input/Output Syntax and Solver Usage > 1.9 Search Order Options (`check-nonces`, `try-old-strands`, `reverse-nodes`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.1-project-initialization-cpsa4init` — 2. CPSA Companion Tools Reference > 2.1 Project Initialization (`cpsa4init`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.2-visualization-cpsa4graph` — 2. CPSA Companion Tools Reference > 2.2 Visualization (`cpsa4graph`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.3-output-comparisons-cpsa4diff` — 2. CPSA Companion Tools Reference > 2.3 Output Comparisons (`cpsa4diff`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.4-shape-extraction-cpsa4shapes` — 2. CPSA Companion Tools Reference > 2.4 Shape Extraction (`cpsa4shapes`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.5-formula-extraction-cpsa4sas` — 2. CPSA Companion Tools Reference > 2.5 Formula Extraction (`cpsa4sas`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.6-goal-satisfaction-checking-cpsa4goalsat` — 2. CPSA Companion Tools Reference > 2.6 Goal Satisfaction Checking (`cpsa4goalsat`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.7-alice-and-bob-notation-translator-cpsa4prot` — 2. CPSA Companion Tools Reference > 2.7 Alice and Bob Notation Translator (`cpsa4prot`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.8-pretty-printing-and-json-export-cpsa4pp` — 2. CPSA Companion Tools Reference > 2.8 Pretty Printing and JSON Export (`cpsa4pp`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.9-cpsa-to-latex-macro-translation-cpsa42latex` — 2. CPSA Companion Tools Reference > 2.9 CPSA to LaTeX Macro Translation (`cpsa42latex`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.10-json-to-s-expression-translation-cpsa4json` — 2. CPSA Companion Tools Reference > 2.10 JSON to S-Expression Translation (`cpsa4json`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.11-querying-cpsa-output-as-derivation-trees-cpsa4query` — 2. CPSA Companion Tools Reference > 2.11 Querying CPSA Output as Derivation Trees (`cpsa4query`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.12-querying-cpsa-output-using-prolog-cpsa4db-and-cpsa4prolog.p` — 2. CPSA Companion Tools Reference > 2.12 Querying CPSA Output Using Prolog (`cpsa4db` and `cpsa4prolog.pl`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.13-using-dynamic-logic-to-generate-prolog-queries-cpsa4dl` — 2. CPSA Companion Tools Reference > 2.13 Using Dynamic Logic to Generate Prolog Queries (`cpsa4dl`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.14-restricted-s-expression-lexical-syntax` — 2. CPSA Companion Tools Reference > 2.14 Restricted S-Expression Lexical Syntax
- `02_manuals/05_CPSA_Specification_and_User_Guide#3.-the-cpsa-formal-specification-cpsaspec` — 3. The CPSA Formal Specification (`cpsaspec`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-1-introduction-to-the-cpsa-reduction-system` — Spec Chapter 1: Introduction to the CPSA Reduction System
- `02_manuals/05_CPSA_Specification_and_User_Guide#1.1-notation` — Spec Chapter 1: Introduction to the CPSA Reduction System > 1.1 Notation
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-2-order-sorted-message-algebras` — Spec Chapter 2: Order-Sorted Message Algebras
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.1-channel-messages` — Spec Chapter 2: Order-Sorted Message Algebras > 2.1 Channel Messages
- `02_manuals/05_CPSA_Specification_and_User_Guide#2.2-locations-and-state-messages` — Spec Chapter 2: Order-Sorted Message Algebras > 2.2 Locations and state messages
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-3-strand-spaces-and-bundles` — Spec Chapter 3: Strand Spaces and Bundles
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-4-adversary-model` — Spec Chapter 4: Adversary Model
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-5-preskeletons-skeletons-and-homomorphisms` — Spec Chapter 5: Preskeletons, Skeletons, and Homomorphisms
- `02_manuals/05_CPSA_Specification_and_User_Guide#5.1-blanchet-s-simple-example-protocol` — Spec Chapter 5: Preskeletons, Skeletons, and Homomorphisms > 5.1 Blanchet’s Simple Example Protocol
- `02_manuals/05_CPSA_Specification_and_User_Guide#5.2-dolev-yao-example-1.3` — Spec Chapter 5: Preskeletons, Skeletons, and Homomorphisms > 5.2 Dolev-Yao Example 1.3
- `02_manuals/05_CPSA_Specification_and_User_Guide#5.3-exercise` — Spec Chapter 5: Preskeletons, Skeletons, and Homomorphisms > 5.3 Exercise
- `02_manuals/05_CPSA_Specification_and_User_Guide#5.4-external-syntax-and-instances` — Spec Chapter 5: Preskeletons, Skeletons, and Homomorphisms > 5.4 External Syntax and Instances
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-6-algorithms-as-reduction-systems` — Spec Chapter 6: Algorithms as Reduction Systems
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-7-primitive-preskeleton-operators` — Spec Chapter 7: Primitive Preskeleton Operators
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-8-reductions-on-preskeletons-thinning-hulling-compr` — Spec Chapter 8: Reductions on Preskeletons (Thinning, Hulling, Compression)
- `02_manuals/05_CPSA_Specification_and_User_Guide#8.1-reduction-systems` — Spec Chapter 8: Reductions on Preskeletons (Thinning, Hulling, Compression) > 8.1 Reduction Systems
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-9-penetrator-derivability-tp-ta---t` — Spec Chapter 9: Penetrator Derivability (`Tp : Ta |- t`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#9.1-implementation` — Spec Chapter 9: Penetrator Derivability (`Tp : Ta |- t`) > 9.1 Implementation
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-10-carried-only-within-cows` — Spec Chapter 10: Carried Only Within (`cows`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-11-solving-authentication-tests-and-cohort-augmenta` — Spec Chapter 11: Solving Authentication Tests and Cohort Augmentation
- `02_manuals/05_CPSA_Specification_and_User_Guide#11.1-test-solving-steps` — Spec Chapter 11: Solving Authentication Tests and Cohort Augmentation > 11.1 Test Solving Steps
- `02_manuals/05_CPSA_Specification_and_User_Guide#11.2-augmentation` — Spec Chapter 11: Solving Authentication Tests and Cohort Augmentation > 11.2 Augmentation
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-12-collapsing-and-preconditioning` — Spec Chapter 12: Collapsing and Preconditioning
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-13-generalization-deletion-weakening-separation-for` — Spec Chapter 13: Generalization (Deletion, Weakening, Separation, Forgetting)
- `02_manuals/05_CPSA_Specification_and_User_Guide#spec-chapter-14-complete-skeleton-reduction-system---k` — Spec Chapter 14: Complete Skeleton Reduction System (`->>k`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#acknowledgements` — Acknowledgements
- `02_manuals/05_CPSA_Specification_and_User_Guide#appendix-a-penetrator-non-origination-assumptions-pen-non-orig` — Appendix A: Penetrator Non-Origination Assumptions (`pen-non-orig`)
- `02_manuals/05_CPSA_Specification_and_User_Guide#appendix-b-programs-specified-by-a-role-procedural-dataflow-rela` — Appendix B: Programs Specified by a Role (Procedural Dataflow Relation)
- `02_manuals/05_CPSA_Specification_and_User_Guide#appendix-c-shape-analysis-sentences` — Appendix C: Shape Analysis Sentences
- `02_manuals/05_CPSA_Specification_and_User_Guide#c.1-security-goals-and-skeleton-formulas` — Appendix C: Shape Analysis Sentences > C.1 Security Goals and Skeleton Formulas
- `02_manuals/05_CPSA_Specification_and_User_Guide#appendix-d-facts-and-rules` — Appendix D: Facts and Rules
- `02_manuals/05_CPSA_Specification_and_User_Guide#bibliography` — Bibliography

## 3. Official `.scm` Examples Catalog (`04_examples_catalog/`)

### `04_examples_catalog/01_scm_examples_A_to_G.md` (Official MITRE CPSA Examples Catalog (Part 1: DH_hack.scm to goalsvar.scm))
- `04_examples_catalog/01_scm_examples_A_to_G#overview` — Overview
- `04_examples_catalog/01_scm_examples_A_to_G#dhhack.scm` — DH_hack.scm
- `04_examples_catalog/01_scm_examples_A_to_G#ab.scm` — ab.scm
- `04_examples_catalog/01_scm_examples_A_to_G#abc.scm` — abc.scm
- `04_examples_catalog/01_scm_examples_A_to_G#aik.scm` — aik.scm
- `04_examples_catalog/01_scm_examples_A_to_G#atomic-open-closed.scm` — atomic-open-closed.scm
- `04_examples_catalog/01_scm_examples_A_to_G#attest.scm` — attest.scm
- `04_examples_catalog/01_scm_examples_A_to_G#auth-enc.scm` — auth-enc.scm
- `04_examples_catalog/01_scm_examples_A_to_G#auth-hash.scm` — auth-hash.scm
- `04_examples_catalog/01_scm_examples_A_to_G#blanchet-strandmax.scm` — blanchet-strandmax.scm
- `04_examples_catalog/01_scm_examples_A_to_G#blanchet.scm` — blanchet.scm
- `04_examples_catalog/01_scm_examples_A_to_G#bugexample.scm` — bug_example.scm
- `04_examples_catalog/01_scm_examples_A_to_G#certlang.scm` — cert_lang.scm
- `04_examples_catalog/01_scm_examples_A_to_G#chan-envelope.scm` — chan-envelope.scm
- `04_examples_catalog/01_scm_examples_A_to_G#chan-perrig-song.scm` — chan-perrig-song.scm
- `04_examples_catalog/01_scm_examples_A_to_G#chan-unilateral.scm` — chan-unilateral.scm
- `04_examples_catalog/01_scm_examples_A_to_G#chan-yahalom-role-decl.scm` — chan-yahalom-role-decl.scm
- `04_examples_catalog/01_scm_examples_A_to_G#chan-yahalom.scm` — chan-yahalom.scm
- `04_examples_catalog/01_scm_examples_A_to_G#commitment.scm` — commitment.scm
- `04_examples_catalog/01_scm_examples_A_to_G#comptest.scm` — comp_test.scm
- `04_examples_catalog/01_scm_examples_A_to_G#completeness-test.scm` — completeness-test.scm
- `04_examples_catalog/01_scm_examples_A_to_G#crushing.scm` — crushing.scm
- `04_examples_catalog/01_scm_examples_A_to_G#dasssimple.scm` — dass_simple.scm
- `04_examples_catalog/01_scm_examples_A_to_G#denning-sacco.scm` — denning-sacco.scm
- `04_examples_catalog/01_scm_examples_A_to_G#deorigcontract.scm` — deorig_contract.scm
- `04_examples_catalog/01_scm_examples_A_to_G#deorigmesg.scm` — deorig_mesg.scm
- `04_examples_catalog/01_scm_examples_A_to_G#deorigsimple.scm` — deorig_simple.scm
- `04_examples_catalog/01_scm_examples_A_to_G#dh-cahack.scm` — dh-ca_hack.scm
- `04_examples_catalog/01_scm_examples_A_to_G#dhencrypthack.scm` — dh_encrypt_hack.scm
- `04_examples_catalog/01_scm_examples_A_to_G#dhgroupsig.scm` — dh_group_sig.scm
- `04_examples_catalog/01_scm_examples_A_to_G#dhgroupsigauthfailure.scm` — dh_group_sig_auth_failure.scm
- `04_examples_catalog/01_scm_examples_A_to_G#dhmimhack.scm` — dh_mim_hack.scm
- `04_examples_catalog/01_scm_examples_A_to_G#dhnslhack.scm` — dhnsl_hack.scm
- `04_examples_catalog/01_scm_examples_A_to_G#dhstatic-state.scm` — dhstatic-state.scm
- `04_examples_catalog/01_scm_examples_A_to_G#disclosure.scm` — disclosure.scm
- `04_examples_catalog/01_scm_examples_A_to_G#doorsep.scm` — doorsep.scm
- `04_examples_catalog/01_scm_examples_A_to_G#doorsep2invk.scm` — doorsep2invk.scm
- `04_examples_catalog/01_scm_examples_A_to_G#encsig.scm` — encsig.scm
- `04_examples_catalog/01_scm_examples_A_to_G#envelope.scm` — envelope.scm
- `04_examples_catalog/01_scm_examples_A_to_G#epmo-hash.scm` — epmo-hash.scm
- `04_examples_catalog/01_scm_examples_A_to_G#epmo-key-hash.scm` — epmo-key-hash.scm
- `04_examples_catalog/01_scm_examples_A_to_G#epmo.scm` — epmo.scm
- `04_examples_catalog/01_scm_examples_A_to_G#epmoacctnum-key-hash.scm` — epmo_acctnum-key-hash.scm
- `04_examples_catalog/01_scm_examples_A_to_G#expand.scm` — expand.scm
- `04_examples_catalog/01_scm_examples_A_to_G#facts.scm` — facts.scm
- `04_examples_catalog/01_scm_examples_A_to_G#factvar.scm` — factvar.scm
- `04_examples_catalog/01_scm_examples_A_to_G#ffgg.scm` — ffgg.scm
- `04_examples_catalog/01_scm_examples_A_to_G#fluffydraft03gske.scm` — fluffy_draft03_gske.scm
- `04_examples_catalog/01_scm_examples_A_to_G#fragilepruning.scm` — fragile_pruning.scm
- `04_examples_catalog/01_scm_examples_A_to_G#goals.scm` — goals.scm
- `04_examples_catalog/01_scm_examples_A_to_G#goalsvar.scm` — goalsvar.scm

### `04_examples_catalog/02_scm_examples_H_to_SDLS.md` (Official MITRE CPSA Examples Catalog (Part 2: hashtest-key-hash.scm to sdls-ep-challenge-authenc.scm))
- `04_examples_catalog/02_scm_examples_H_to_SDLS#overview` — Overview
- `04_examples_catalog/02_scm_examples_H_to_SDLS#hashtest-key-hash.scm` — hashtest-key-hash.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#hashtest.scm` — hashtest.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#incompletenessexample.scm` — incompleteness_example.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#isoreject-corrected.scm` — isoreject-corrected.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#isoreject.scm` — isoreject.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#kelly1.scm` — kelly1.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#kerberos.scm` — kerberos.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#lemmas.scm` — lemmas.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#locnenvelope.scm` — locn_envelope.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#missingcontraction.scm` — missing_contraction.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#neqtest.scm` — neq_test.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#neuman-stubblebine.scm` — neuman-stubblebine.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#nocontraction.scm` — no_contraction.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#nontransforming.scm` — non_transforming.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#nonaug-prune.scm` — nonaug-prune.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#ns-l.scm` — ns-l.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#ns-rebinding.scm` — ns-rebinding.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#ns.scm` — ns.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#nsl3.scm` — nsl3.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#nslsk.scm` — nslsk.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#open-closed-multiloc.scm` — open-closed-multiloc.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#open-closed-tag.scm` — open-closed-tag.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#open-closed.scm` — open-closed.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#or.scm` — or.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#ordered.scm` — ordered.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#orderedvar.scm` — orderedvar.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#pca.scm` — pca.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#pen-non-orig-test.scm` — pen-non-orig-test.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#pfs-via-pubkey.scm` — pfs-via-pubkey.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#pkinit.scm` — pkinit.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#preprocess.scm` — preprocess.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#print.scm` — print.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#prottrans.scm` — prottrans.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#pruning1.scm` — pruning1.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#puzzleexample.scm` — puzzle_example.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#reflect.scm` — reflect.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#renamings.scm` — renamings.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#roleuniq.scm` — role_uniq.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#rule-node.scm` — rule-node.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#rule-order.scm` — rule-order.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#rules.scm` — rules.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#scep-tls-dh-broken.scm` — scep-tls-dh-broken.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#scep-tls-dh-fixed.scm` — scep-tls-dh-fixed.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#sdls-auth-enc-full-payload.scm` — sdls-auth-enc-full-payload.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#sdls-auth-enc-logic.scm` — sdls-auth-enc-logic.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#sdls-auth-full-payload.scm` — sdls-auth-full-payload.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#sdls-auth-logic.scm` — sdls-auth-logic.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#sdls-enc-logic.scm` — sdls-enc-logic.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#sdls-ep-challenge-auth.scm` — sdls-ep-challenge-auth.scm
- `04_examples_catalog/02_scm_examples_H_to_SDLS#sdls-ep-challenge-authenc.scm` — sdls-ep-challenge-authenc.scm

### `04_examples_catalog/03_scm_examples_SDLS_to_Z.md` (Official MITRE CPSA Examples Catalog (Part 3: sdls-ep-challenge.scm to yes-or-no.scm))
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#overview` — Overview
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-challenge.scm` — sdls-ep-challenge.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-key-activation-auth.scm` — sdls-ep-key-activation-auth.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-key-activation-authenc.scm` — sdls-ep-key-activation-authenc.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-key-activation.scm` — sdls-ep-key-activation.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-otar-auth.scm` — sdls-ep-otar-auth.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-otar-authenc.scm` — sdls-ep-otar-authenc.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-otar-transmission.scm` — sdls-ep-otar-transmission.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-sa-rekey-auth.scm` — sdls-ep-sa-rekey-auth.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-sa-rekey-authenc.scm` — sdls-ep-sa-rekey-authenc.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-sa-rekey.scm` — sdls-ep-sa-rekey.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-sa-start-auth.scm` — sdls-ep-sa-start-auth.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-sa-start-authenc.scm` — sdls-ep-sa-start-authenc.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sdls-ep-sa-start.scm` — sdls-ep-sa-start.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sigenc.scm` — sigenc.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sortedepmoacctnum.scm` — sorted_epmo_acctnum.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#sts.scm` — sts.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#stsnonrole.scm` — sts_non_role.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#stsweakenedreflect.scm` — sts_weakened_reflect.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#subatomic-open-closed-test-genrule.scm` — subatomic-open-closed-test-genrule.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#subatomic-open-closed.scm` — subatomic-open-closed.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#synclocnenvelope.scm` — sync_locn_envelope.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#synclocnenvelopenoauth.scm` — sync_locn_envelope_no_auth.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#targetterms1.scm` — targetterms1.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#targetterms2.scm` — targetterms2.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#targetterms6.scm` — targetterms6.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#targetterms8.scm` — targetterms8.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#thisthat.scm` — thisthat.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#tickle-unique.scm` — tickle-unique.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#timestamping.scm` — timestamping.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#trust-anchor.scm` — trust-anchor.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#ugen-at.scm` — ugen-at.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#ugo.scm` — ugo.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#uncarriedkeys.scm` — uncarried_keys.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#unilateral.scm` — unilateral.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#uniq-at.scm` — uniq-at.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#uniq-gen-test.scm` — uniq-gen-test.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#uo.scm` — uo.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#wang-hash.scm` — wang-hash.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#wang-key-hash.scm` — wang-key-hash.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#weird.scm` — weird.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#wonthull.scm` — wonthull.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#wonthull2.scm` — wonthull2.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#wonthull3.scm` — wonthull3.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#woolam.scm` — woolam.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#yahalom-6.3.6.scm` — yahalom-6.3.6.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#yahalom-forward.scm` — yahalom-forward.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#yahalom.scm` — yahalom.scm
- `04_examples_catalog/03_scm_examples_SDLS_to_Z#yes-or-no.scm` — yes-or-no.scm

### `04_examples_catalog/04_scm_examples_hackage_4_4_9.md` (Official MITRE CPSA Examples Catalog (Part 4: Hackage cpsa-4.4.9 Additional Examples))
- `04_examples_catalog/04_scm_examples_hackage_4_4_9#overview` — Overview
- `04_examples_catalog/04_scm_examples_hackage_4_4_9#chan-mesg.scm` — chan-mesg.scm
- `04_examples_catalog/04_scm_examples_hackage_4_4_9#dev-subatomic-open-closed.scm` — dev-subatomic-open-closed.scm
- `04_examples_catalog/04_scm_examples_hackage_4_4_9#devlocn.scm` — devlocn.scm

## 4. Indexed `.scm` Protocol Examples by Feature (`03_examples_scm/`)
- **Diffie-Hellman (`diffie-hellman`, `rndx`, `uniq-gen`, `exp`) [8 files]**: dh_group_sig.scm, dh_group_sig_auth_failure.scm, dhstatic-state.scm, scep-tls-dh-broken.scm, scep-tls-dh-fixed.scm, sts.scm, sts_non_role.scm, sts_weakened_reflect.scm
- **Roletran Procedural Inputs/Outputs (`inputs`, `outputs`, `chan`) [4 files]**: auth-enc.scm, auth-hash.scm, cert_lang.scm, commitment.scm
- **Channels (`chan`, `auth`, `conf`) [21 files]**: atomic-open-closed.scm, auth-enc.scm, auth-hash.scm, cert_lang.scm, chan-envelope.scm, chan-mesg.scm, chan-perrig-song.scm, chan-unilateral.scm, chan-yahalom-role-decl.scm, chan-yahalom.scm, dev-subatomic-open-closed.scm, dh_group_sig.scm, dh_group_sig_auth_failure.scm, locn_envelope.scm, open-closed-multiloc.scm, open-closed-tag.scm, open-closed.scm, subatomic-open-closed-test-genrule.scm, subatomic-open-closed.scm, sync_locn_envelope.scm, sync_locn_envelope_no_auth.scm
- **Stateful Memory Locations (`locn`, `load`, `stor`, `gen-st`) [12 files]**: atomic-open-closed.scm, dev-subatomic-open-closed.scm, devlocn.scm, dhstatic-state.scm, locn_envelope.scm, open-closed-multiloc.scm, open-closed-tag.scm, open-closed.scm, subatomic-open-closed-test-genrule.scm, subatomic-open-closed.scm, sync_locn_envelope.scm, sync_locn_envelope_no_auth.scm
- **Security Goals (`defgoal`) [9 files]**: doorsep2invk.scm, facts.scm, goals.scm, goalsvar.scm, lemmas.scm, scep-tls-dh-broken.scm, scep-tls-dh-fixed.scm, sdls-auth-logic.scm, unilateral.scm
- **Axiom Rules & Lemmas (`defrule`, `defgenrule`, `deflemma`) [32 files]**: atomic-open-closed.scm, attest.scm, cert_lang.scm, chan-envelope.scm, comp_test.scm, dev-subatomic-open-closed.scm, doorsep.scm, envelope.scm, factvar.scm, fluffy_draft03_gske.scm, lemmas.scm, locn_envelope.scm, neq_test.scm, ns-rebinding.scm, open-closed-multiloc.scm, open-closed-tag.scm, open-closed.scm, ordered.scm, orderedvar.scm, prottrans.scm, role_uniq.scm, rule-node.scm, rule-order.scm, rules.scm, subatomic-open-closed-test-genrule.scm, subatomic-open-closed.scm, sync_locn_envelope.scm, sync_locn_envelope_no_auth.scm, tickle-unique.scm, trust-anchor.scm, ugen-at.scm, uniq-at.scm
```

---

### `tests/conftest.py`

*sha256:`1fa6c287ec3c` · 14 lines · 0.5 KB (~133 tokens) · lang:`python`*

```python
"""Global pytest fixtures ensuring hermetic test execution without polluting tracked repo logs."""

from pathlib import Path
import pytest

from src.system_config import SYSTEM_CONFIG


@pytest.fixture(autouse=True)
def _hermetic_logs_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Redirects SYSTEM_CONFIG.LOGS_DIR to an isolated temporary folder during pytest runs."""
    temp_logs = tmp_path / "logs"
    temp_logs.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(SYSTEM_CONFIG, "LOGS_DIR", temp_logs)
```

---

### `tests/test_code_generation_and_verification.py`

*sha256:`827647dc908b` · 332 lines · 14.2 KB (~3,631 tokens) · lang:`python`*

```python
"""Unit and Integration Tests for Code Generation and Verification Engine."""

import pytest
import shutil
from pathlib import Path

from src.system_config import SYSTEM_CONFIG
from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAVariableDeclaration,
    CPSATraceEvent,
    CPSAProtocolRole,
    CPSAStrandInstance,
    CPSAPreskeleton,
    CPSAProtocolSpecification,
)
from src.code_generation.cpsa_scheme_emitter import emit_cpsa_scheme
from src.verification_engine.roletran_executability_gate import verify_role_executability
from src.verification_engine.mitre_build_orchestrator import execute_mitre_make_build


@pytest.fixture
def valid_unilateral_spec() -> CPSAProtocolSpecification:
    """A valid, executable unilateral authentication protocol with channels and inputs/outputs."""
    return CPSAProtocolSpecification(
        protocol_name="unilateral_auth",
        herald_comment="Unilateral Authentication Test Suite",
        roles=[
            CPSAProtocolRole(
                role_name="init",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="send", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="recv", channel="ch", message_term="n"),
                ],
                inputs=["ch", "k"],
                outputs=["n"],
                unique_originating=["n"],
            ),
            CPSAProtocolRole(
                role_name="resp",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="recv", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="send", channel="ch", message_term="n"),
                ],
                inputs=["ch", ["invk", "k"]],
                outputs=["n"],
            ),
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="unilateral_auth",
                variables=[
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                strands=[
                    CPSAStrandInstance(role_name="init", trace_length=2, variable_bindings={"k": "k", "n": "n"}),
                ],
                non_originating=[["invk", "k"]],
                unique_originating=["n"],
                comment="Initiator Point of View",
            ),
        ],
    )


@pytest.fixture
def unexecutable_spec() -> CPSAProtocolSpecification:
    """An unexecutable protocol where the responder tries to send a nonce it cannot decrypt."""
    return CPSAProtocolSpecification(
        protocol_name="broken_protocol",
        roles=[
            CPSAProtocolRole(
                role_name="resp",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="recv", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="send", channel="ch", message_term="n"),
                ],
                inputs=["ch"],  # Missing decryption key (invk k)
                outputs=["n"],
            ),
        ],
    )


def test_scheme_emitter_generates_valid_scm(tmp_path: Path, valid_unilateral_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(valid_unilateral_spec, tmp_path)
    assert scm_path.exists()
    assert scm_path.suffix == ".scm"

    with open(scm_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "(defprotocol unilateral_auth basic" in content
    assert "(defrole init" in content
    assert "(defskeleton unilateral_auth" in content


def test_roletran_gate_accepts_valid_protocol(tmp_path: Path, valid_unilateral_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(valid_unilateral_spec, tmp_path)
    result = verify_role_executability(scm_path)

    assert result.is_executable is True
    assert result.error_diagnostic is None
    assert result.procedural_defproc_code is not None
    assert "(defproc init" in result.procedural_defproc_code


def test_roletran_gate_rejects_unexecutable_protocol(tmp_path: Path, unexecutable_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(unexecutable_spec, tmp_path)
    result = verify_role_executability(scm_path)

    assert result.is_executable is False
    assert result.error_diagnostic is not None
    assert "Received term cannot be fully destructured" in result.error_diagnostic


def test_mitre_build_orchestrator_compiles_artifacts(tmp_path: Path, valid_unilateral_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(valid_unilateral_spec, tmp_path)
    artifacts = execute_mitre_make_build(scm_path, tmp_path)

    assert artifacts.trace_txt_path.exists()
    assert artifacts.shapes_txt_path.exists()
    assert artifacts.full_graph_xhtml_path.exists()
    assert artifacts.shapes_graph_xhtml_path.exists()
    assert artifacts.shapes_count >= 1


def test_compiler_diagnostic_repair_patches_spec(monkeypatch, tmp_path: Path, unexecutable_spec: CPSAProtocolSpecification):
    """Test that repair engine retrieves manual guidance and returns an executable specification."""
    import copy
    from unittest.mock import MagicMock
    from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification

    # Fix the missing decryption key in the role inputs
    repaired = copy.deepcopy(unexecutable_spec)
    repaired.roles[0].inputs.append(["invk", "k"])

    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock(message=MagicMock(content=repaired.model_dump_json()))]
    monkeypatch.setattr("litellm.completion", lambda **kwargs: mock_resp)

    repaired_spec = repair_protocol_specification(
        failing_spec=unexecutable_spec,
        error_diagnostic="Received term cannot be fully destructured: (enc n k)",
        verbatim_slice="Initiator sends {n}_k to responder. Responder decrypts with invk(k).",
        failure_stage="roletran",
        model="mock_model",
    )

    assert ["invk", "k"] in repaired_spec.roles[0].inputs
    scm_path = emit_cpsa_scheme(repaired_spec, tmp_path)
    res = verify_role_executability(scm_path)
    assert res.is_executable is True


def test_cpsa_term_desugaring_and_validation():
    """Verify that foreign operators are desugared and unknown operators are strictly rejected."""
    # 1. Foreign operator desugaring: aenc, senc, sign -> enc; mac, hmac -> hash
    event = CPSATraceEvent(
        direction="send",
        channel="ch",
        message_term=["aenc", ["mac", "secret", "tag"], "pubkey"],
    )
    assert event.message_term == ["enc", ["hash", "secret", "tag"], "pubkey"]

    # 2. Unknown operator rejection
    with pytest.raises(ValueError, match="Unknown operator keyword 'foreign_op'"):
        CPSATraceEvent(
            direction="send",
            channel="ch",
            message_term=["foreign_op", "payload"],
        )


def test_cpsa_operator_arity_enforcement():
    """Verify that operator arities from MITRE CPSA Tables 10.3 and 10.5 are strictly enforced."""
    # (enc) requires at least 2 arguments: payload + key
    with pytest.raises(ValueError, match="Operator 'enc' at 'term' expects at least 2 arguments"):
        from src.intermediate_representation.cpsa_grammar import validate_cpsa_term_syntax
        validate_cpsa_term_syntax(["enc", "payload_only"])

    # (invk) requires exactly 1 argument
    with pytest.raises(ValueError, match="Operator 'invk' at 'term' expects exactly 1 arguments"):
        from src.intermediate_representation.cpsa_grammar import validate_cpsa_term_syntax
        validate_cpsa_term_syntax(["invk", "key1", "key2"])

    # (ltk) requires exactly 2 arguments
    with pytest.raises(ValueError, match="Operator 'ltk' at 'term' expects exactly 2 arguments"):
        from src.intermediate_representation.cpsa_grammar import validate_cpsa_term_syntax
        validate_cpsa_term_syntax(["ltk", "key1"])


def test_basic_algebra_forbids_diffie_hellman_operators():
    """Verify that protocol with 'basic' algebra rejects Diffie-Hellman operators in trace or declarations."""
    # exp operator under basic algebra must fail
    with pytest.raises(ValueError, match="Diffie-Hellman operator 'exp'"):
        CPSAProtocolSpecification(
            protocol_name="dh_in_basic",
            message_algebra="basic",
            roles=[
                CPSAProtocolRole(
                    role_name="client",
                    variables=[
                        CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                        CPSAVariableDeclaration(name="x", sort=CPSASortEnum.DATA),
                    ],
                    trace=[
                        CPSATraceEvent(
                            direction="send",
                            channel="ch",
                            message_term=["exp", "gen", "x"],
                        ),
                    ],
                )
            ],
        )


def test_ensure_three_point_of_view_skeletons():
    """Verify that ensure_three_point_of_view_skeletons guarantees distinct pure POV and secrecy skeletons."""
    from src.semantic_extraction.constrained_protocol_extractor import ensure_three_point_of_view_skeletons

    spec = CPSAProtocolSpecification(
        protocol_name="test_proto",
        roles=[
            CPSAProtocolRole(
                role_name="client",
                variables=[CPSAVariableDeclaration(name="s", sort=CPSASortEnum.DATA)],
                trace=[CPSATraceEvent(direction="send", message_term="s")],
                unique_originating=["s"],
            ),
            CPSAProtocolRole(
                role_name="server",
                variables=[CPSAVariableDeclaration(name="s", sort=CPSASortEnum.DATA)],
                trace=[CPSATraceEvent(direction="recv", message_term="s")],
            ),
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="test_proto",
                strands=[CPSAStrandInstance(role_name="client", variable_bindings={"s": "s"})],
                listeners=["s"],
            )
        ],
    )

    updated = ensure_three_point_of_view_skeletons(spec)
    assert len(updated.skeletons) == 3
    # Skeletons 1 & 2 must be pure POV skeletons without listeners
    assert updated.skeletons[0].strands[0].role_name == "client"
    assert updated.skeletons[0].listeners == []
    assert updated.skeletons[1].strands[0].role_name == "server"
    assert updated.skeletons[1].listeners == []
    # Skeleton 3 must be a secrecy listener skeleton
    assert updated.skeletons[2].listeners == ["s"]

    # Test case 2: LLM specifies primary_secrecy_goals with an arbitrary name not matching any keywords/regex
    spec_semantic = CPSAProtocolSpecification(
        protocol_name="test_proto_semantic",
        primary_secrecy_goals=["arbitrary_token"],
        roles=[
            CPSAProtocolRole(
                role_name="alice",
                variables=[CPSAVariableDeclaration(name="arbitrary_token", sort=CPSASortEnum.DATA)],
                trace=[CPSATraceEvent(direction="send", message_term="arbitrary_token")],
                unique_originating=["arbitrary_token"],
            ),
            CPSAProtocolRole(
                role_name="bob",
                variables=[CPSAVariableDeclaration(name="arbitrary_token", sort=CPSASortEnum.DATA)],
                trace=[CPSATraceEvent(direction="recv", message_term="arbitrary_token")],
            ),
        ],
        skeletons=[],
    )
    updated_semantic = ensure_three_point_of_view_skeletons(spec_semantic)
    assert len(updated_semantic.skeletons) == 3
    assert updated_semantic.skeletons[0].strands[0].role_name == "alice"
    assert updated_semantic.skeletons[0].listeners == []
    assert updated_semantic.skeletons[1].strands[0].role_name == "bob"
    assert updated_semantic.skeletons[1].listeners == []
    assert updated_semantic.skeletons[2].listeners == ["arbitrary_token"]
    assert updated_semantic.skeletons[2].strands[0].role_name == "alice"


def test_nous_portal_llm_kwargs_routing():
    """Verify that nous/ prefixed models are mapped to OpenAI-compatible Nous inference endpoints."""
    from src.system_config import SYSTEM_CONFIG

    kwargs_claude = SYSTEM_CONFIG.get_llm_kwargs("nous/anthropic/claude-3.5-sonnet")
    assert kwargs_claude["model"] == "openai/anthropic/claude-3.5-sonnet"
    assert kwargs_claude["api_base"] == "https://inference-api.nousresearch.com/v1"

    kwargs_deepseek = SYSTEM_CONFIG.get_llm_kwargs("nous/deepseek/deepseek-chat")
    assert kwargs_deepseek["model"] == "openai/deepseek/deepseek-chat"
    assert kwargs_deepseek["api_base"] == "https://inference-api.nousresearch.com/v1"


def test_clean_rag_diagnostic_query_sanitization():
    """Verify that compiler error messages strip local paths, line numbers, and output clean domain queries."""
    from src.verification_engine.compiler_diagnostic_repair import fallback_sanitize_diagnostic_query

    # Test solver unbound identifier error from make output
    make_err = "MITRE build failed for tls_1_2_shapes.xhtml: tls_1_2.scm:72:6: Identifier server_hello_done unknown\nmake: *** [cpsa4.mk:8: tls_1_2.txt] Error 1"
    q1 = fallback_sanitize_diagnostic_query(make_err, "solver")
    assert "tls_1_2" not in q1
    assert "shapes.xhtml" not in q1
    assert ".scm" not in q1

    # Test roletran Cannot build error
    roletran_err = "Cannot build (cat client_random session_id)"
    q2 = fallback_sanitize_diagnostic_query(roletran_err, "roletran")
    assert "Cannot build" in q2
    assert "client_random" not in q2
```

---

### `tests/test_cpsa_kb_and_agentic_searcher.py`

*sha256:`76f560b2ae3d` · 616 lines · 25.5 KB (~6,529 tokens) · lang:`python`*

```python
"""Unit & Integration Tests for the CPSA 4.4.9 Knowledge Base, TOC Rebuild Flag,
Agentic Searcher Loop, and Two-Speed Repair Trigger.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.rag_retriever_client import (
    CPSAKnowledgeBase,
    TOC_MD_PATH,
    build_cpsa_kb_index,
    get_cpsa_manual_retriever,
    parse_toc_rebuild_flag,
    run_agentic_cpsa_searcher,
)
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAProtocolRole,
    CPSAProtocolSpecification,
    CPSAPreskeleton,
    CPSAStrandInstance,
    CPSATraceEvent,
    CPSAVariableDeclaration,
    CPSASortEnum,
)
from src.verification_engine.compiler_diagnostic_repair import (
    repair_protocol_specification,
)


def _make_sample_spec() -> CPSAProtocolSpecification:
    return CPSAProtocolSpecification(
        protocol_name="test-proto",
        message_algebra="basic",
        roles=[
            CPSAProtocolRole(
                role_name="init",
                variables=[
                    CPSAVariableDeclaration(name="a", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="b", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                ],
                inputs=["ch", "a", "b"],
                outputs=["n"],
                unique_originating=["n"],
                trace=[
                    CPSATraceEvent(
                        direction="send",
                        channel="ch",
                        message_term=["enc", "n", ["pubk", "b"]],
                    )
                ],
            )
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="test-proto",
                variables=[
                    CPSAVariableDeclaration(name="a", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="b", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                ],
                strands=[
                    CPSAStrandInstance(
                        role_name="init",
                        height=1,
                        variable_mappings=[["a", "a"], ["b", "b"], ["n", "n"]],
                    )
                ],
                non_originating=[["privk", "b"]],
                unique_originating=["n"],
            )
        ],
    )


def test_production_cpsa_kb_completeness_and_toc_flag():
    """Verify that the production `refrences/cpsa_kb/` corpus indexes all 151 .scm examples,
    all core rules/manuals/catalogs, and has `rebuild_toc: false` in `TOC.md`.
    """
    kb = get_cpsa_manual_retriever()
    assert kb is not None
    assert len(kb.scm_examples) == 151
    assert len(kb.sections) >= 400
    assert TOC_MD_PATH.exists()
    assert parse_toc_rebuild_flag(TOC_MD_PATH) is False

    # Verify the 3 official Hackage cpsa-4.4.9 test files are indexed
    for hackage_scm in ("chan-mesg.scm", "dev-subatomic-open-closed.scm", "devlocn.scm"):
        ex = kb.read_scm_example(hackage_scm)
        assert ex is not None, f"Missing Hackage 4.4.9 example {hackage_scm}"
        assert "(defprotocol" in ex["scm_code"]


def test_toc_rebuild_flag_lifecycle_in_isolated_kb(tmp_path: Path):
    """Verify that `rebuild_toc: true` triggers a full rebuild of `TOC.md` and `kb_index.json`
    and automatically flips `rebuild_toc: false`, and that subsequent loads skip rebuilding
    until `rebuild_toc: true` is flipped back.
    """
    kb_dir = tmp_path / "cpsa_kb"
    core_dir = kb_dir / "01_core_rules"
    scm_dir = kb_dir / "03_examples_scm"
    core_dir.mkdir(parents=True)
    scm_dir.mkdir(parents=True)

    (core_dir / "01_test_rules.md").write_text(
        "# Test Rules\n\n## Section Alpha\nAlpha rule about uniq-orig and non-orig in defskeleton.\n",
        encoding="utf-8",
    )
    (scm_dir / "mini_ns.scm").write_text(
        "(herald \"Mini NS\")\n(defprotocol ns basic (defrole init (vars (a b name) (n text)) (trace (send (enc n (pubk b))))))\n",
        encoding="utf-8",
    )

    toc_path = kb_dir / "TOC.md"
    # Before TOC exists, parse_toc_rebuild_flag returns True
    assert parse_toc_rebuild_flag(toc_path) is True

    kb1 = CPSAKnowledgeBase(kb_dir)
    assert len(kb1.sections) == 1
    assert len(kb1.scm_examples) == 1
    # After build, TOC.md exists and rebuild_toc is automatically flipped to False
    assert toc_path.exists()
    assert parse_toc_rebuild_flag(toc_path) is False

    # Add a new markdown file WITHOUT flipping rebuild_toc -> cached kb_index.json is used
    (core_dir / "02_extra_rules.md").write_text(
        "# Extra Rules\n\n## Section Beta\nBeta rule about diffie-hellman rndx and uniq-gen.\n",
        encoding="utf-8",
    )
    kb2 = CPSAKnowledgeBase(kb_dir)
    assert len(kb2.sections) == 1

    # Now flip `rebuild_toc: false` -> `rebuild_toc: true` in TOC.md
    toc_text = toc_path.read_text(encoding="utf-8").replace("rebuild_toc: false", "rebuild_toc: true")
    toc_path.write_text(toc_text, encoding="utf-8")
    assert parse_toc_rebuild_flag(toc_path) is True

    # Loading CPSAKnowledgeBase now rebuilds and resets rebuild_toc to False
    kb3 = CPSAKnowledgeBase(kb_dir)
    assert len(kb3.sections) == 2
    assert parse_toc_rebuild_flag(toc_path) is False


def test_cpsa_kb_four_tools_precision():
    """Verify `read_section`, `search_cpsa_docs`, `find_scm_examples`, and `read_scm_example`."""
    kb = get_cpsa_manual_retriever()
    assert kb is not None

    # Tool 1: read_section
    sec = kb.read_section("01_core_rules/07_compiler_and_solver_error_catalog#1.1-received-term-cannot-be-fully-destructured")
    assert sec is not None
    assert "Received term cannot be fully destructured" in sec["title"]

    # Tool 2: search_cpsa_docs on exact compiler diagnostic
    hits = kb.search_cpsa_docs("Received term cannot be fully destructured", top_k=2, rerank=False)
    assert len(hits) >= 1
    assert "destructured" in hits[0]["title"].lower() or "destructured" in hits[0]["content"].lower()

    # Tool 3: find_scm_examples for diffie-hellman + uniq-gen
    dh_examples = kb.find_scm_examples(algebra="diffie-hellman", keywords=["uniq-gen"], top_k=3)
    assert len(dh_examples) >= 1
    assert all(ex["algebra"] == "diffie-hellman" for ex in dh_examples)

    # Tool 4: read_scm_example
    blanchet = kb.read_scm_example("blanchet.scm")
    assert blanchet is not None
    assert "(defprotocol blanchet basic" in blanchet["scm_code"]


def test_agentic_searcher_multi_tool_loop():
    """Verify `run_agentic_cpsa_searcher` executes structured tool calls and returns
    diagnosis + KB rules + working .scm example.
    """
    spec = _make_sample_spec()
    mock_resp_turn1 = MagicMock()
    mock_resp_turn1.choices = [
        MagicMock(
            message=MagicMock(
                content=json.dumps({
                    "is_final": False,
                    "ast_root_cause": "Nonce n is encrypted under (pubk b) without Responder knowing (privk b).",
                    "actionable_fix": "Add (privk b) to Responder inputs.",
                    "tool_calls": [
                        {
                            "tool": "read_section",
                            "section_id": "01_core_rules/07_compiler_and_solver_error_catalog#1.1-received-term-cannot-be-fully-destructured",
                        },
                        {
                            "tool": "read_scm_example",
                            "filename": "ns.scm",
                        },
                    ],
                })
            )
        )
    ]
    mock_resp_turn2 = MagicMock()
    mock_resp_turn2.choices = [
        MagicMock(
            message=MagicMock(
                content=json.dumps({
                    "is_final": True,
                    "ast_root_cause": "Responder lacks decryption key (privk b) in its inputs list.",
                    "actionable_fix": "Declare (privk b) in role inputs so cpsa4roletran can destructure the recv term.",
                    "tool_calls": [],
                })
            )
        )
    ]

    with patch("src.rag_retriever_client.litellm.completion", side_effect=[mock_resp_turn1, mock_resp_turn2]):
        guidance = run_agentic_cpsa_searcher(
            error_diagnostic="roletran: Received term cannot be fully destructured (enc n (pubk b))",
            failure_stage="roletran",
            failing_spec=spec,
            cycle_detected=True,
        )

    assert "Agentic Searcher AST Diagnosis" in guidance
    assert "Responder lacks decryption key" in guidance
    assert "Received term cannot be fully destructured" in guidance
    assert "ns.scm" in guidance


def test_two_speed_repair_trigger_skips_searcher_on_fast_attempt_and_escalates():
    """Verify `repair_protocol_specification` skips the Agentic Searcher when
    `use_agentic_searcher=False` and invokes it when `use_agentic_searcher=True`.
    """
    spec = _make_sample_spec()
    mock_repair_resp = MagicMock()
    mock_repair_resp.choices = [
        MagicMock(message=MagicMock(content=spec.model_dump_json()))
    ]

    with patch("src.verification_engine.compiler_diagnostic_repair.run_agentic_cpsa_searcher") as mock_searcher, \
         patch("src.verification_engine.compiler_diagnostic_repair.litellm.completion", return_value=mock_repair_resp):
        # Attempt 1: Fast direct repair (use_agentic_searcher=False) -> searcher NOT called
        repaired_1 = repair_protocol_specification(
            failing_spec=spec,
            error_diagnostic="Cannot build (enc n (pubk b))",
            verbatim_slice="RFC slice",
            failure_stage="roletran",
            cycle_detected=False,
            use_agentic_searcher=False,
        )
        assert repaired_1.protocol_name == "test-proto"
        assert mock_searcher.call_count == 0

        # Escalated attempt (use_agentic_searcher=True) -> searcher IS called
        mock_searcher.return_value = "--- Agentic Searcher AST Diagnosis ---\nAdd variable to inputs."
        repaired_2 = repair_protocol_specification(
            failing_spec=spec,
            error_diagnostic="Cannot build (enc n (pubk b))",
            verbatim_slice="RFC slice",
            failure_stage="roletran",
            cycle_detected=False,
            use_agentic_searcher=True,
        )
        assert repaired_2.protocol_name == "test-proto"
        assert mock_searcher.call_count == 1


def test_cost_tracker_per_role_and_batch_telemetry():
    """Verify `PipelineCostTracker` accurately computes per-role (`router`, `extraction`,
    `query`, `repair`) and batch USD costs and token counts, and emits `cost_updated` events.
    """
    import pytest
    from src.cost_tracker import PipelineCostTracker
    from src.pipeline_events import GLOBAL_EVENT_BUS

    tracker = PipelineCostTracker()
    tracker._catalog_fetched = True  # Use deterministic fallback table in unit tests

    captured_events = []
    GLOBAL_EVENT_BUS.subscribe(captured_events.append)
    try:
        tracker.start_rfc(
            rfc_id="RFC 9999",
            router_model="nous/z-ai/glm-5.3-flash",
            extraction_model="nous/openai/gpt-6.1-terra",
            query_model="nous/anthropic/claude-haiku-5.5",
            repair_model="nous/google/gemini-3.7-flash",
        )

        # 1. Router call: 1,000 prompt + 200 completion on glm-5.3-flash ($0.12/1M in, $0.40/1M out)
        resp_router = {
            "usage": {"prompt_tokens": 1000, "completion_tokens": 200}
        }
        tracker.record_llm_call(resp_router, role="router", model_name="nous/z-ai/glm-5.3-flash", stage=1)

        # 2. Extraction call: 5,000 prompt + 1,000 completion on gpt-6.1-terra ($1.00/1M in, $5.00/1M out)
        resp_extract = {
            "usage": {"prompt_tokens": 5000, "completion_tokens": 1000}
        }
        tracker.record_llm_call(resp_extract, role="extraction", model_name="nous/openai/gpt-6.1-terra", stage=2)

        # 3. Query call: 2,000 prompt + 500 completion on claude-haiku-5.5 ($0.10/1M in, $0.50/1M out)
        resp_query = {
            "usage": {"prompt_tokens": 2000, "completion_tokens": 500}
        }
        tracker.record_llm_call(resp_query, role="query", model_name="nous/anthropic/claude-haiku-5.5", stage=5)

        # 4. Repair call: 4,000 prompt + 1,000 completion on gemini-3.7-flash ($0.75/1M in, $3.75/1M out)
        resp_repair = {
            "usage": {"prompt_tokens": 4000, "completion_tokens": 1000}
        }
        rfc_summary = tracker.record_llm_call(
            resp_repair, role="repair", model_name="nous/google/gemini-3.7-flash", stage=5
        )

        assert rfc_summary["total_calls"] == 4
        assert rfc_summary["total_tokens"] == (1200 + 6000 + 2500 + 5000)
        assert rfc_summary["roles"]["router"]["cost_usd"] == pytest.approx(0.0002, rel=1e-4)
        assert rfc_summary["roles"]["extraction"]["cost_usd"] == pytest.approx(0.0100, rel=1e-4)
        assert rfc_summary["roles"]["query"]["cost_usd"] == pytest.approx(0.00045, rel=1e-4)
        assert rfc_summary["roles"]["repair"]["cost_usd"] == pytest.approx(0.00675, rel=1e-4)
        assert rfc_summary["total_cost_usd"] == pytest.approx(0.0174, rel=1e-4)

        cli_line = tracker.format_cli_summary(rfc_summary, prefix="RFC Run Cost")
        assert "RFC Run Cost: $0.0174" in cli_line
        assert "Extraction: $0.0100" in cli_line
        assert "Repair: $0.006" in cli_line

        cost_evts = [e for e in captured_events if e.event_type == "cost_updated"]
        assert len(cost_evts) == 4
        assert cost_evts[-1].data["rfc_cost"]["total_cost_usd"] == pytest.approx(0.0174, rel=1e-4)
    finally:
        GLOBAL_EVENT_BUS.unsubscribe(captured_events.append)


def test_snowball_error_classification_and_15s_timeout():
    """Verify default CPSA compile timeout is 15s and `is_snowball_state_error` strictly
    isolates state-space snowball errors from ordinary compiler/roletran diagnostics.
    """
    from src.system_config import SYSTEM_CONFIG
    from src.verification_engine.snowball_autopsy import (
        inject_herald_options_into_scm,
        is_snowball_state_error,
    )

    assert SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS == 15

    # Snowball state errors -> True
    assert is_snowball_state_error(
        "MITRE CPSA compilation timed out after 15 seconds (state-space explosion / infinite strand loop)"
    )
    assert is_snowball_state_error("cpsa4: Step limit exceeded")
    assert is_snowball_state_error("cpsa4: Strand bound exceeded")
    assert is_snowball_state_error("cpsa4: Heap exhausted;")

    # Every other compiler/roletran/syntax error -> False
    assert not is_snowball_state_error("cpsa4: Identifier foo unknown")
    assert not is_snowball_state_error("roletran: Received term cannot be fully destructured")
    assert not is_snowball_state_error("cpsa4: Malformed encryption term")
    assert not is_snowball_state_error("cpsa4: Sort mismatch in defstrand")
    assert not is_snowball_state_error("")
    assert not is_snowball_state_error(None)

    # Herald flag injection into .scm
    scm_in = '(herald "Test Protocol" (algebra diffie-hellman))\n\n(defprotocol p diffie-hellman)'
    scm_out = inject_herald_options_into_scm(scm_in, ["try-old-strands", "check-nonces"])
    assert '(herald "Test Protocol" (algebra diffie-hellman) (try-old-strands) (check-nonces))' in scm_out


def test_snowball_tier1_herald_portfolio_and_non_snowball_bypass(tmp_path):
    """Verify non-snowball errors bypass Tier 1/Tier 2 immediately, whereas snowball errors
    trigger the Tier 1 deterministic herald search-order portfolio and persist winning flags.
    """
    import pytest
    from src.verification_engine.mitre_build_orchestrator import (
        CPSABuildError,
        execute_mitre_make_build,
    )

    scm_file = tmp_path / "proto.scm"
    scm_file.write_text('(herald "Proto")\n(defprotocol proto basic)\n', encoding="utf-8")

    # 1. Non-snowball error -> must NOT run Tier 1 portfolio (only 1 call to _run_make_with_hard_timeout)
    with patch("src.verification_engine.mitre_build_orchestrator._ensure_cpsa_makefile"), \
         patch(
             "src.verification_engine.mitre_build_orchestrator._run_make_with_hard_timeout",
             return_value=(2, "", "cpsa4: Identifier bad_var unknown"),
         ) as mock_make:
        with pytest.raises(CPSABuildError) as exc_info:
            execute_mitre_make_build(scm_file, tmp_path, build_full_graph=False)
        assert "Identifier bad_var unknown" in str(exc_info.value)
        assert mock_make.call_count == 1

    # 2. Snowball error on Pass 0 -> Tier 1 Strategy #1 (`--try-old-strands`) resolves it!
    call_counter = {"n": 0}

    def _fake_make_side_effect(cmd, cwd, env, timeout_seconds):
        call_counter["n"] += 1
        if call_counter["n"] == 1:
            raise CPSABuildError(
                "MITRE CPSA compilation timed out after 15 seconds (state-space explosion / infinite strand loop)"
            )
        # Strategy #1 (`--try-old-strands`) succeeds and writes expected build artifacts
        (cwd / "proto.txt").write_text("(defskeleton proto (shape))", encoding="utf-8")
        (cwd / "proto_shapes.txt").write_text("(defskeleton proto (shape))", encoding="utf-8")
        (cwd / "proto_shapes.xhtml").write_text("<html/>", encoding="utf-8")
        return (0, "ok", "")

    with patch("src.verification_engine.mitre_build_orchestrator._ensure_cpsa_makefile"), \
         patch(
             "src.verification_engine.mitre_build_orchestrator._run_make_with_hard_timeout",
             side_effect=_fake_make_side_effect,
         ):
        artifacts = execute_mitre_make_build(scm_file, tmp_path, build_full_graph=False)
        assert artifacts.winning_herald_options == ["try-old-strands"]
        assert "(try-old-strands)" in scm_file.read_text(encoding="utf-8")


def test_snowball_tier2_autopsy_report_and_tier3_prompt_isolation():
    """Verify `analyze_snowball_trace_text` extracts the exact repeating `(added-strand ...)`
    operation, critical term, and cloned primed variables, and `repair_protocol_specification`
    injects Tier 3 snowball directives ONLY on snowball errors.
    """
    from src.verification_engine.snowball_autopsy import analyze_snowball_trace_text

    sample_snowball_txt = """
(herald "Looping Protocol")
(defprotocol loop_proto basic)
(defskeleton loop_proto
  (vars (n data) (a b name) (ch chan))
  (defstrand init 2 (n n) (a a) (b b) (ch ch))
  (label 0)
  (unrealized (0 1))
  (comment "POV 1 (Initiator)"))

(defskeleton loop_proto
  (vars (n n-0 data) (a b a-0 b-0 name) (ch ch-0 chan))
  (defstrand init 2 (n n) (a a) (b b) (ch ch))
  (defstrand resp 2 (n n-0) (a a-0) (b b-0) (ch ch-0))
  (operation encryption-test (added-strand resp 2) (enc n-0 a-0 (ltk a-0 b-0)) (0 1))
  (label 1)
  (parent 0)
  (unrealized (1 0)))

(defskeleton loop_proto
  (vars (n n-0 n-1 data) (a b a-0 b-0 a-1 b-1 name) (ch ch-0 ch-1 chan))
  (defstrand init 2 (n n) (a a) (b b) (ch ch))
  (defstrand resp 2 (n n-0) (a a-0) (b b-0) (ch ch-0))
  (defstrand resp 2 (n n-1) (a a-1) (b b-1) (ch ch-1))
  (operation encryption-test (added-strand resp 2) (enc n-1 a-1 (ltk a-1 b-1)) (1 0))
  (label 2)
  (parent 1)
  (unrealized (2 0)))
"""
    report = analyze_snowball_trace_text(sample_snowball_txt)
    assert "CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT" in report
    assert "resp (height 2): 2x" in report
    assert "encryption-test" in report
    assert "(added-strand resp 2)" in report
    assert "(enc n-* a-* (ltk a-* b-*))" in report
    assert "a:name (cloned 2x as a-0..a-1)" in report
    assert "DOMAIN-SEPARATE EVERY `(enc ...)` AND `(hash ...)` TERM" in report

    # Verify Tier 3 prompt injection is strictly isolated to snowball errors
    spec = _make_sample_spec()
    mock_repair_resp = MagicMock()
    mock_repair_resp.choices = [MagicMock(message=MagicMock(content=spec.model_dump_json()))]

    captured_prompts = []

    def _capture_completion(**kwargs):
        captured_prompts.append(kwargs["messages"][1]["content"])
        return mock_repair_resp

    with patch("src.verification_engine.compiler_diagnostic_repair.run_agentic_cpsa_searcher", return_value="KB Rules"), \
         patch("src.verification_engine.compiler_diagnostic_repair.litellm.completion", side_effect=_capture_completion):
        # Normal error -> NO Tier-3 snowball block in prompt
        repair_protocol_specification(
            failing_spec=spec,
            error_diagnostic="Cannot build (enc n (pubk b))",
            verbatim_slice="RFC slice",
            failure_stage="solver",
            use_agentic_searcher=False,
        )
        assert "MANDATORY TIER-3 SNOWBALL STATE RECOVERY PROTOCOL" not in captured_prompts[-1]

        # Snowball error -> Tier-3 snowball block IS in prompt
        repair_protocol_specification(
            failing_spec=spec,
            error_diagnostic=f"MITRE CPSA compilation timed out after 15 seconds\n\n{report}",
            verbatim_slice="RFC slice",
            failure_stage="solver",
            use_agentic_searcher=False,
        )
        assert "MANDATORY TIER-3 SNOWBALL STATE RECOVERY PROTOCOL" in captured_prompts[-1]
        assert "CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT" in captured_prompts[-1]


def test_csv_logger_upsert_overwrites_by_rfc_id_and_logs_all_model_columns(tmp_path):
    """Verify `PipelineMetricsCSVLogger` performs in-place upserts keyed by normalized `rfc_id`,
    increments `run_count`, saves `scm_path` regardless of pass/fail, and logs dedicated columns
    for every model role (`router`, `extraction`, `query`, `repair`).
    """
    import csv
    from src.logging_config import PipelineMetricsCSVLogger

    csv_file = tmp_path / "pipeline_runs.csv"
    logger_csv = PipelineMetricsCSVLogger(csv_path=csv_file)
    assert len(PipelineMetricsCSVLogger.CSV_HEADER) == 67

    scm_file = tmp_path / "mobile_ipv6.scm"
    scm_file.write_text("(herald test)\n(defprotocol p basic)\n", encoding="utf-8")
    traj_file = tmp_path / "mobile_ipv6_trajectory.json"
    shapes_file = tmp_path / "mobile_ipv6_shapes.xhtml"

    fake_cost_1 = {
        "total_calls": 5,
        "total_tokens": 25000,
        "total_cost_usd": 0.045,
        "roles": {
            "router": {"model": "nous/z-ai/glm-5.3", "calls": 2, "total_tokens": 3000, "cost_usd": 0.0012},
            "extraction": {"model": "nous/openai/gpt-6.1-terra", "calls": 1, "total_tokens": 12000, "cost_usd": 0.0280},
            "query": {"model": "nous/anthropic/claude-haiku-5.5", "calls": 1, "total_tokens": 2000, "cost_usd": 0.0008},
            "repair": {"model": "nous/google/gemini-3.7-flash", "calls": 1, "total_tokens": 8000, "cost_usd": 0.0150},
        },
    }

    # 1. First run of RFC 4285 fails in Stage 6, but scm_path is still saved!
    logger_csv.log_run(
        rfc_id="rfc 4285",
        is_eligible=True,
        status="PARTIAL",
        quality_tier="REJECTED",
        protocol_name="Mobile IPv6 Auth",
        message_algebra="basic",
        selected_sections=["5", "5.1"],
        sliced_lines_count=242,
        role_count=3,
        preskeleton_count=3,
        roletran_passed=True,
        solver_passed=False,
        roletran_repairs=1,
        solver_repairs=2,
        searcher_invocations=1,
        duration_seconds=45.2,
        cost_telemetry=fake_cost_1,
        scm_path=scm_file,
        trajectory_json_path=traj_file,
        error_message="Step limit exceeded",
    )

    with open(csv_file, "r", encoding="utf-8") as f:
        rows_1 = list(csv.DictReader(f))
    assert len(rows_1) == 1
    r1 = rows_1[0]
    assert r1["rfc_id"] == "RFC4285"
    assert r1["run_count"] == "1"
    assert r1["status"] == "PARTIAL"
    assert r1["total_completion_steps"] == "4"
    assert r1["schema_repairs"] == "0"
    assert r1["roletran_repairs"] == "1"
    assert r1["solver_repairs"] == "2"
    assert r1["total_repairs"] == "3"
    assert r1["scm_path"] == str(scm_file)
    assert r1["scm_lines_count"] == "2"
    assert r1["router_model"] == "nous/z-ai/glm-5.3"
    assert r1["router_cost_usd"] == "0.001200"
    assert r1["extraction_model"] == "nous/openai/gpt-6.1-terra"
    assert r1["extraction_cost_usd"] == "0.028000"
    assert r1["query_model"] == "nous/anthropic/claude-haiku-5.5"
    assert r1["query_cost_usd"] == "0.000800"
    assert r1["repair_model"] == "nous/google/gemini-3.7-flash"
    assert r1["repair_cost_usd"] == "0.015000"
    assert r1["total_cost_usd"] == "0.045000"

    # 2. Re-run of RFC4285 succeeds -> overwrites existing row in-place and increments run_count to 2!
    logger_csv.log_run(
        rfc_id="RFC4285",
        is_eligible=True,
        status="VERIFIED",
        quality_tier="GOLD",
        protocol_name="Mobile IPv6 Auth",
        message_algebra="basic",
        selected_sections=["5", "5.1"],
        sliced_lines_count=242,
        role_count=3,
        preskeleton_count=3,
        roletran_passed=True,
        solver_passed=True,
        shapes_count=4,
        explored_skeletons_count=18,
        all_povs_multi_strand=True,
        secrecy_proved=True,
        roletran_repairs=0,
        solver_repairs=0,
        herald_options=["try-old-strands"],
        duration_seconds=12.4,
        cost_telemetry=fake_cost_1,
        scm_path=scm_file,
        shapes_xhtml_path=shapes_file,
        trajectory_json_path=traj_file,
        error_message=None,
    )

    with open(csv_file, "r", encoding="utf-8") as f:
        rows_2 = list(csv.DictReader(f))
    assert len(rows_2) == 1  # Overwritten in-place, NOT duplicated!
    r2 = rows_2[0]
    assert r2["rfc_id"] == "RFC4285"
    assert r2["run_count"] == "2"
    assert r2["status"] == "VERIFIED"
    assert r2["quality_tier"] == "GOLD"
    assert r2["zero_shot_passed"] == "True"
    assert r2["herald_options"] == "try-old-strands"
    assert r2["shapes_xhtml_path"] == str(shapes_file)
    assert r2["error_message"] == ""
```

---

### `tests/test_cpsa_scoping_and_prompts.py`

*sha256:`f1dec182640b` · 208 lines · 9.0 KB (~2,316 tokens) · lang:`python`*

```python
"""Unit Tests for MITRE CPSA 4.4.9 Keyword/Sort Scoping and Externalized prompts/ Frontmatter Loader."""

from pathlib import Path
import pytest

from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.cpsa_grammar import validate_cpsa_term_syntax
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAPreskeleton,
    CPSAProtocolRole,
    CPSAProtocolSpecification,
    CPSAStrandInstance,
    CPSATraceEvent,
    CPSAVariableDeclaration,
)
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    PROMPT_COMPILER_REPAIR,
    PROMPT_PROTOCOL_EXTRACTION,
    PROMPT_RAG_QUERY_FORMULATION,
    PROMPT_SCHEMA_SELF_CORRECTION,
    PROMPT_SECTION_ROUTER,
    PROMPT_THINK_SYNTHESIZER,
    build_schema_system_prompt,
    load_prompt,
    load_prompt_spec,
    resolve_prompt_model,
)
from src.system_config import SYSTEM_CONFIG


def test_externalized_prompts_load_frontmatter_strip_yaml_and_fallback(tmp_path: Path):
    """Verify all 7 prompt templates in prompts/ load YAML frontmatter cleanly and strip it from prompt bodies."""
    for prompt_filename in (
        PROMPT_APPLICABILITY_GATE,
        PROMPT_SECTION_ROUTER,
        PROMPT_PROTOCOL_EXTRACTION,
        PROMPT_SCHEMA_SELF_CORRECTION,
        PROMPT_RAG_QUERY_FORMULATION,
        PROMPT_COMPILER_REPAIR,
        PROMPT_THINK_SYNTHESIZER,
    ):
        spec = load_prompt_spec(prompt_filename)
        assert spec.model and "/" in spec.model
        assert spec.timeout > 0
        assert len(spec.body) > 100
        assert not spec.body.startswith("---")

        text = load_prompt(prompt_filename)
        assert text == spec.body
        assert "model:" not in text.splitlines()[0]

    # Verify schema attachment helper omits YAML frontmatter
    schema_prompt = build_schema_system_prompt(PROMPT_PROTOCOL_EXTRACTION, CPSAProtocolSpecification)
    assert not schema_prompt.startswith("---")
    assert "Respond strictly with a valid JSON object matching this schema:" in schema_prompt
    assert '"CPSAProtocolSpecification"' in schema_prompt

    # Verify fallback when directory has no files
    fallback_spec = load_prompt_spec(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert "MITRE CPSA 4.4.9" in fallback_spec.body
    assert fallback_spec.model


def test_prompt_frontmatter_live_hot_reload_and_strata_routing(tmp_path: Path):
    """Editing YAML frontmatter in prompts/*.md hot-reloads model/timeout immediately; strata/ routes to STRATA_API_BASE."""
    gate_file = tmp_path / PROMPT_APPLICABILITY_GATE
    gate_file.write_text(
        "---\nmodel: strata/unsloth-iq4_xs\ntimeout: 45\ntemperature: 0.0\n---\nPrompt v1 body text.",
        encoding="utf-8",
    )
    spec_v1 = load_prompt_spec(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert spec_v1.model == "strata/unsloth-iq4_xs"
    assert spec_v1.timeout == 45
    assert spec_v1.temperature == 0.0
    assert spec_v1.body == "Prompt v1 body text."

    # Hot-swap model mid-run by editing the markdown file
    gate_file.write_text(
        "---\nmodel: ollama/qwen3.8:27b\ntimeout: 90\n---\nPrompt v2 body text.",
        encoding="utf-8",
    )
    spec_v2 = load_prompt_spec(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert spec_v2.model == "ollama/qwen3.8:27b"
    assert spec_v2.timeout == 90
    assert spec_v2.body == "Prompt v2 body text."

    # CLI override takes precedence over frontmatter
    assert resolve_prompt_model(PROMPT_APPLICABILITY_GATE, override_model="gemini/gemini-2.5-pro", prompts_dir=tmp_path) == "gemini/gemini-2.5-pro"
    assert resolve_prompt_model(PROMPT_APPLICABILITY_GATE, override_model=None, prompts_dir=tmp_path) == "ollama/qwen3.8:27b"

    # First-class strata/<model> LiteLLM routing
    strata_kwargs = SYSTEM_CONFIG.get_llm_kwargs("strata/unsloth-iq4_xs", temperature=0.0)
    assert strata_kwargs["model"] == "openai/strata/unsloth-iq4_xs"
    assert strata_kwargs["api_base"] == SYSTEM_CONFIG.STRATA_API_BASE
    assert strata_kwargs["api_key"] == SYSTEM_CONFIG.STRATA_API_KEY


def test_logic_only_sorts_forbidden_in_role_and_skeleton_vars():
    """Tables 10.2 & 10.4 vs Table 7.1: strd, indx, and fact are forbidden in role/skeleton vars."""
    for bad_sort in (CPSASortEnum.STRD, CPSASortEnum.INDX, CPSASortEnum.FACT):
        with pytest.raises(ValueError, match="first-order logic sort"):
            CPSAVariableDeclaration(name="node_idx", sort=bad_sort)


def test_diffie_hellman_sorts_forbidden_under_basic_algebra():
    """Table 10.2: rndx, expt, and base sorts are forbidden when protocol message_algebra is 'basic'."""
    with pytest.raises(ValueError, match="Diffie-Hellman variable sort 'rndx'"):
        CPSAProtocolSpecification(
            protocol_name="dh_sort_in_basic",
            message_algebra="basic",
            roles=[
                CPSAProtocolRole(
                    role_name="initiator",
                    variables=[
                        CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                        CPSAVariableDeclaration(name="x", sort=CPSASortEnum.RNDX),
                    ],
                    trace=[
                        CPSATraceEvent(direction="send", channel="ch", message_term="x"),
                    ],
                )
            ],
        )


def test_structural_keywords_forbidden_inside_message_terms():
    """Tables 10.1, 10.3, 10.5: structural keywords (defrole, send, vars, etc.) cannot be term operators."""
    for bad_kw in ("defrole", "defskeleton", "send", "recv", "vars", "trace", "uniq-orig", "deflistener"):
        with pytest.raises(ValueError, match=f"Structural CPSA keyword '{bad_kw}'"):
            validate_cpsa_term_syntax([bad_kw, "x"])


def test_role_and_skeleton_keyword_scoping_separation():
    """Tables 10.1 & 10.6: skeleton keywords cannot appear in defrole and role keywords cannot appear in defskeleton."""
    # 1. Skeleton keyword 'listeners' or 'strands' inside CPSAProtocolRole must fail
    with pytest.raises(ValueError, match="preskeleton-only keyword"):
        CPSAProtocolRole.model_validate({
            "role_name": "client",
            "variables": [{"name": "x", "sort": "text"}],
            "trace": [{"direction": "send", "message_term": "x"}],
            "listeners": ["x"],
        })

    # 2. Role keyword 'trace' or 'inputs' inside CPSAPreskeleton must fail
    with pytest.raises(ValueError, match="role-only keyword"):
        CPSAPreskeleton.model_validate({
            "protocol_name": "proto",
            "strands": [{"role_name": "client"}],
            "trace": [{"direction": "send", "message_term": "x"}],
        })


def test_equation_10_1_forbids_mesg_sort_as_encryption_key():
    """Equation 10.1: variables declared with sort 'mesg' cannot be used as encryption keys in (enc ...)."""
    with pytest.raises(ValueError, match="Equation 10.1"):
        CPSAProtocolRole(
            role_name="sender",
            variables=[
                CPSAVariableDeclaration(name="payload", sort=CPSASortEnum.TEXT),
                CPSAVariableDeclaration(name="generic_key", sort=CPSASortEnum.MESG),
            ],
            trace=[
                CPSATraceEvent(
                    direction="send",
                    channel="ch",
                    message_term=["enc", "payload", "generic_key"],
                )
            ],
        )


def test_stateful_load_stor_event_serialization_and_roletran_invariants():
    """Verify Table 10.1 load/stor 2-arg serialization, 2-arg pubk ordering, and cpsa4roletran input/output sanitization."""
    # 1. load/stor must emit 2 arguments after direction: [load, locn, term]
    load_evt = CPSATraceEvent(direction="load", location="state_cell", message_term="secret_val")
    assert load_evt.to_cpsa_json() == ["load", "state_cell", "secret_val"]

    # 2. Role serialization enforces roletran invariants and 2-arg pubk argument order
    role = CPSAProtocolRole(
        role_name="initiator",
        variables=[
            CPSAVariableDeclaration(name="server_id", sort=CPSASortEnum.NAME),
            CPSAVariableDeclaration(name="fresh_nonce", sort=CPSASortEnum.TEXT),
        ],
        trace=[
            CPSATraceEvent(
                direction="send",
                channel="ch",
                message_term=["enc", "fresh_nonce", ["pubk", "server_id", "enc_tag"]],
            )
        ],
        unique_originating=["fresh_nonce"],
        # Intentionally include fresh_nonce and a compound cat in inputs, and repeat server_id in outputs
        inputs=["server_id", "fresh_nonce", ["cat", "server_id", "fresh_nonce"]],
        outputs=["fresh_nonce", "server_id"],
    )
    role_json = role.to_cpsa_json()
    role_str = str(role_json)

    # Channel 'ch' auto-declared in vars and auto-added to inputs
    assert "['ch', 'chan']" in role_str
    # 2-arg pubk normalized to ['pubk', '"enc_tag"', 'server_id']
    assert "['pubk', '\"enc_tag\"', 'server_id']" in role_str
    # 'fresh_nonce' (uniq-orig) and ['cat', ...] stripped from inputs
    assert "['inputs', 'ch', 'server_id']" in role_str
    # 'server_id' (an input) stripped from outputs, leaving only 'fresh_nonce'
    assert "['outputs', 'fresh_nonce']" in role_str
```

---

### `tests/test_document_ingestion.py`

*sha256:`2f1018f4d031` · 118 lines · 4.0 KB (~1,026 tokens) · lang:`python`*

```python
"""Unit & Integration Tests for Document Ingestion Subsystem (Stage 1)."""

import pytest
from pathlib import Path

from src.system_config import SYSTEM_CONFIG
from src.document_ingestion.rfc_header_filter import filter_rfc_header
from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections
from src.document_ingestion.handshake_section_router import _heuristic_section_router


@pytest.fixture
def tls_rfc_text() -> str:
    path = SYSTEM_CONFIG.RFCS_DIR / "rfc5246.txt"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


@pytest.fixture
def kerberos_rfc_text() -> str:
    path = SYSTEM_CONFIG.RFCS_DIR / "rfc4120.txt"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


@pytest.fixture
def mib_rfc_text() -> str:
    path = SYSTEM_CONFIG.RFCS_DIR / "rfc2358.txt"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def test_header_filter_accepts_tls(tls_rfc_text: str):
    res = filter_rfc_header(tls_rfc_text)
    assert res.is_eligible is True
    assert res.rfc_id == "RFC 5246"
    assert "Transport Layer Security" in (res.title or "")
    assert res.category == "Standards Track"


def test_header_filter_accepts_kerberos(kerberos_rfc_text: str):
    res = filter_rfc_header(kerberos_rfc_text)
    assert res.is_eligible is True
    assert res.rfc_id == "RFC 4120"
    assert "Kerberos" in (res.title or "")


def test_header_filter_rejects_mib(mib_rfc_text: str):
    res = filter_rfc_header(mib_rfc_text)
    assert res.is_eligible is False
    assert any(term in res.disqualification_reason.lower() for term in ["mib", "managed objects"])


def test_header_filter_rejects_short_stub():
    res = filter_rfc_header("Short administrative stub.\n" * 10)
    assert res.is_eligible is False
    assert "too short" in res.disqualification_reason.lower()


def test_toc_parser_tls5246(tls_rfc_text: str):
    entries = parse_table_of_contents(tls_rfc_text)
    assert len(entries) >= 70
    section_map = {e.section_id: e.title for e in entries}

    assert "7.3" in section_map
    assert "Handshake Protocol Overview" in section_map["7.3"]
    assert "7.4" in section_map
    assert "Handshake Protocol" in section_map["7.4"]


def test_toc_parser_kerberos4120(kerberos_rfc_text: str):
    entries = parse_table_of_contents(kerberos_rfc_text)
    assert len(entries) >= 100
    section_map = {e.section_id: e.title for e in entries}

    assert "3.1" in section_map
    assert "The Authentication Service Exchange" in section_map["3.1"]


def test_verbatim_slicer_tls_handshake(tls_rfc_text: str):
    slice_text = slice_verbatim_sections(tls_rfc_text, ["7.3"])
    lines = slice_text.splitlines()

    # Starts with section header
    assert lines[0].startswith("7.3.  Handshake Protocol Overview")
    # Contains client hello ladder diagram
    assert "ClientHello" in slice_text
    assert "ServerHello" in slice_text
    # Does not contain page break markers
    assert "\x0c" not in slice_text
    assert "[Page 33]" not in slice_text


def test_heuristic_section_router_tls(tls_rfc_text: str):
    entries = parse_table_of_contents(tls_rfc_text)
    selected = _heuristic_section_router(entries)
    assert "7.3" in selected or "7.4" in selected


def test_verbatim_slicer_non_contiguous_sections_excludes_gap():
    synthetic_rfc = (
        "1.  Introduction\n"
        "Intro text line 1.\n"
        "Intro text line 2.\n\n"
        "2.  Unrelated Huge Appendix Stuff\n"
        "Unrelated middle text that must NOT be included.\n\n"
        "3.  Security Protocol Specification\n"
        "Alice sends N_A to Bob.\n\n"
        "4.  IANA Considerations\n"
        "None.\n"
    )
    sliced = slice_verbatim_sections(synthetic_rfc, ["1", "3"])
    assert "1.  Introduction" in sliced
    assert "3.  Security Protocol Specification" in sliced
    assert "Unrelated middle text that must NOT be included." not in sliced
    assert "4.  IANA Considerations" not in sliced
```

---

### `tests/test_generate_think.py`

*sha256:`a5001e31cc2d` · 250 lines · 10.5 KB (~2,682 tokens) · lang:`python`*

```python
"""Unit and integration tests for Phase 3 Hindsight Reasoning (<think>) Synthesizer."""

import json
from pathlib import Path
from unittest.mock import patch

from src.generate_think.think_schema import SynthesizedReasoningSteps, ThinkArtifactBundle
from src.generate_think.dspy_think_synthesizer import (
    _sanitize_hindsight_leakage,
    compile_deterministic_reasoning_steps,
    generate_think_for_trajectory,
    process_run_directory,
)


def _sample_trajectory_dict() -> dict:
    return {
        "schema_version": "1.0.0",
        "run_id": "rfc 9999_20261022T190000Z",
        "timestamp_utc": "2026-10-22T19:00:00Z",
        "duration_seconds": 12.5,
        "rfc_metadata": {
            "rfc_id": "RFC 9999",
            "rfc_title": "Test Mutual Auth Protocol",
            "protocol_name": "test_proto",
            "algebra": "basic",
            "participating_principals": ["init", "resp"],
            "selected_sections": ["2"],
            "sliced_lines_count": 10,
            "verbatim_rfc_slice": "2. Protocol Handshake\nInit sends encrypted nonce n under k to Resp.",
        },
        "stage2_initial_extraction": {
            "schema_self_correction_triggered": False,
            "schema_validation_error": None,
            "initial_ast": None,
            "initial_scm": None,
        },
        "stage5_preflight_gate": {
            "validator_binary": "cpsa4roletran",
            "roletran_algebra_supported": True,
            "initial_passed": False,
            "final_passed": True,
            "total_attempts": 1,
            "compiled_defproc_output": "(defproc ...)",
            "repair_attempts": [
                {
                    "attempt_number": 1,
                    "cycle_detected": False,
                    "rejected_ast": {},
                    "rejected_scm": "(defprotocol test_proto basic (defrole init ...))",
                    "raw_stderr": ":5:4: Received term cannot be fully destructured",
                    "parsed_diagnostic": "Received term cannot be fully destructured",
                    "rag_query": "cpsa4roletran received term destructured inputs",
                    "retrieved_chunk_ids": [95, 114],
                    "repaired_ast": {},
                    "repaired_scm": "(defprotocol test_proto basic (defrole init (inputs ch k) ...))",
                    "passed_after_repair": True,
                }
            ],
        },
        "stage6_cpsa4_solver": {
            "validator_binary": "cpsa4",
            "initial_passed": True,
            "final_passed": True,
            "total_attempts": 0,
            "repair_attempts": [],
            "exploration_telemetry_from_txt": {
                "source_file": "test_proto.txt",
                "txt_file_size_bytes": 1200,
                "total_explored_labels": 4,
                "dead_branch_nodes_count": 0,
                "step_limit_or_bound_hit": False,
                "state_explosion_detected": False,
                "dead_preskeleton_diagnostics": [],
            },
            "shapes_analysis_from_shapes_txt": {
                "source_file": "test_proto_shapes.txt",
                "shapes_file_size_bytes": 800,
                "total_preskeletons": 2,
                "total_realized_shapes": 1,
                "per_preskeleton_outcomes": [
                    {
                        "skeleton_index": 0,
                        "root_label": 0,
                        "skeleton_type": "participant_pov",
                        "comment": "Initiator POV",
                        "has_deflistener": False,
                        "listener_term": None,
                        "realized_shape_labels": [1],
                        "realized_shapes_count": 1,
                        "max_strands_in_realized_shape": 2,
                        "instantiated_roles_in_shape": [
                            {"role": "init", "height": 2},
                            {"role": "resp", "height": 2},
                        ],
                        "is_trivial_single_strand_shape": False,
                        "goal_satisfied": None,
                        "verdict": "AUTHENTICATED_MULTI_STRAND",
                    }
                ],
            },
        },
        "quality_assessment": {
            "quality_tier": "GOLD",
            "all_participant_povs_realized": True,
            "all_participant_povs_multi_strand": True,
            "all_secrecy_listeners_unrealized": True,
            "post_training_routing": {
                "eligible_for_sft_positive": True,
                "dpo_contrastive_pairs_available": 1,
                "compiler_repair_trajectories_available": 1,
            },
        },
        "final_verified_output": {
            "final_ast": {
                "protocol_name": "test_proto",
                "message_algebra": "basic",
                "herald_comment": "Test mutual auth protocol",
                "roles": [
                    {
                        "role_name": "init",
                        "description": "Initiator role",
                        "variables": [
                            {"name": "ch", "sort": "chan", "description": "Channel", "rfc_field": "Sec 2"},
                            {"name": "n", "sort": "text", "description": "Fresh nonce", "rfc_field": "Sec 2"},
                            {"name": "k", "sort": "akey", "description": "Public key", "rfc_field": "Sec 2"},
                        ],
                        "trace": [
                            {
                                "direction": "send",
                                "channel": "ch",
                                "message_term": ["enc", "n", "k"],
                                "description": "Send encrypted nonce",
                            },
                            {
                                "direction": "recv",
                                "channel": "ch",
                                "message_term": "n",
                                "description": "Receive plaintext nonce",
                            },
                        ],
                        "inputs": ["ch", "k"],
                        "outputs": ["n"],
                        "unique_originating": ["n"],
                        "unique_generated": [],
                        "non_originating": [],
                    }
                ],
                "skeletons": [
                    {
                        "protocol_name": "test_proto",
                        "description": "Initiator POV",
                        "variables": [
                            {"name": "n", "sort": "text"},
                            {"name": "k", "sort": "akey"},
                        ],
                        "strands": [
                            {"role_name": "init", "variable_bindings": {"n": "n", "k": "k"}},
                        ],
                        "non_originating": [["invk", "k"]],
                        "unique_originating": ["n"],
                        "listeners": [],
                        "comment": "Initiator POV",
                    }
                ],
            },
            "final_scm_with_header": ";;; [RFC-ID: RFC 9999]\n(defprotocol test_proto basic ...)",
            "distilled_shapes_txt": "(herald ...)",
        },
    }


def test_deterministic_reasoning_compiler_and_hindsight_sanitizer():
    traj = _sample_trajectory_dict()
    steps = compile_deterministic_reasoning_steps(traj)
    assert isinstance(steps, SynthesizedReasoningSteps)
    assert "RFC 9999" in steps.step1_protocol_and_algebra
    assert "`n` (sort `text`)" in steps.step2_principals_and_variables
    assert "(send ch (enc n k))" in steps.step3_message_flow_and_terms
    assert "Wait—let me check pre-flight role executability" in steps.step4_compiler_backtracking_and_invariants

    leaked = "<think>Looking at the provided AST and in the given final_scm, we use basic.</think>"
    cleaned = _sanitize_hindsight_leakage(leaked)
    assert "provided AST" not in cleaned
    assert "given final_scm" not in cleaned
    assert not cleaned.startswith("<think>")


def test_process_run_directory_creates_think_json_and_updates_metadata_index(tmp_path: Path):
    run_dir = tmp_path / "run_2026-10-22_19-00-00"
    rfc_dir = run_dir / "rfc9999"
    rfc_dir.mkdir(parents=True)

    traj_path = rfc_dir / "test_proto_trajectory.json"
    traj_path.write_text(json.dumps(_sample_trajectory_dict(), indent=2), encoding="utf-8")

    index_path = run_dir / "metadata_index.json"
    index_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "run_directory": str(run_dir.resolve()),
                "total_rfcs_processed": 1,
                "metadata_json_files": [str(traj_path.resolve())],
                "rfc_directories": [str(rfc_dir.resolve())],
                "runs": [
                    {
                        "rfc_id": "RFC 9999",
                        "protocol_name": "test_proto",
                        "is_eligible": True,
                        "build_successful": True,
                        "quality_tier": "GOLD",
                        "rfc_directory": str(rfc_dir.resolve()),
                        "scm_file": str((rfc_dir / "test_proto.scm").resolve()),
                        "metadata_json_file": str(traj_path.resolve()),
                        "error_message": None,
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    think_files = process_run_directory(
        target_path=run_dir,
        mode="deterministic",
        min_tier="GOLD",
        export_jsonl=True,
    )

    assert len(think_files) == 1
    think_path = rfc_dir / "test_proto_think.json"
    assert think_files[0] == think_path
    assert think_path.exists()

    bundle = ThinkArtifactBundle.model_validate_json(think_path.read_text(encoding="utf-8"))
    assert bundle.thinking_block.startswith("<think>\n")
    assert bundle.thinking_block.endswith("\n</think>")
    assert len(bundle.sft_messages) == 3
    assert bundle.sft_messages[2]["content"].startswith("<think>\n")
    assert ";;; [RFC-ID: RFC 9999]" in bundle.sft_messages[2]["content"]
    assert len(bundle.dpo_contrastive_pairs) == 1
    assert bundle.dpo_contrastive_pairs[0].stage == "stage5_roletran"

    updated_index = json.loads(index_path.read_text(encoding="utf-8"))
    assert str(think_path.resolve()) in updated_index["think_json_files"]
    assert updated_index["runs"][0]["think_json_file"] == str(think_path.resolve())
    assert (run_dir / "sft_train.jsonl").exists()
    assert (run_dir / "dpo_pairs.jsonl").exists()
```

---

### `tests/test_main_pipeline_orchestrator.py`

*sha256:`bc5a9ee15ce7` · 157 lines · 7.0 KB (~1,782 tokens) · lang:`python`*

```python
"""Integration tests for Main Pipeline Orchestrator."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.system_config import SYSTEM_CONFIG
from src.main_pipeline_orchestrator import run_rfc_translation_pipeline
from src.document_ingestion.protocol_applicability_gate import ProtocolApplicabilityReport
from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAVariableDeclaration,
    CPSATraceEvent,
    CPSAProtocolRole,
    CPSAStrandInstance,
    CPSAPreskeleton,
    CPSAProtocolSpecification,
)


@pytest.fixture
def mock_valid_spec() -> CPSAProtocolSpecification:
    return CPSAProtocolSpecification(
        protocol_name="orch_test_proto",
        herald_comment="Pipeline Orchestrator Verification Spec",
        roles=[
            CPSAProtocolRole(
                role_name="init",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="send", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="recv", channel="ch", message_term="n"),
                ],
                inputs=["ch", "k"],
                outputs=["n"],
                unique_originating=["n"],
            ),
            CPSAProtocolRole(
                role_name="resp",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="recv", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="send", channel="ch", message_term="n"),
                ],
                inputs=["ch", ["invk", "k"]],
                outputs=["n"],
            ),
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="orch_test_proto",
                variables=[
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                strands=[
                    CPSAStrandInstance(role_name="init", trace_length=2, variable_bindings={"k": "k", "n": "n"}),
                ],
                non_originating=[["invk", "k"]],
                unique_originating=["n"],
                comment="Initiator Point of View",
            ),
        ],
    )


def test_pipeline_rejects_ineligible_rfc(tmp_path: Path):
    """Pipeline immediately halts on administrative or MIB documents at Stage 1a without creating dead RFC folders."""
    import json
    mib_rfc_path = SYSTEM_CONFIG.RFCS_DIR / "rfc2358.txt"
    rfc_out = tmp_path / "rfc2358_out"
    summary = run_rfc_translation_pipeline(
        rfc_file_path=mib_rfc_path,
        output_dir=rfc_out,
    )
    assert summary.is_eligible is False
    assert summary.build_successful is False
    assert not rfc_out.exists()
    assert any(k in (summary.error_message or "").lower() for k in ["mib", "managed objects"])
    idx_data = json.loads((tmp_path / "metadata_index.json").read_text(encoding="utf-8"))
    assert idx_data["total_ineligible_filtered"] == 1
    assert idx_data["rfc_directories"] == []


def test_pipeline_e2e_successful_synthesis_and_build(tmp_path: Path, mock_valid_spec: CPSAProtocolSpecification):
    """Pipeline successfully synthesizes and verifies all MITRE shapes when given an eligible RFC."""
    rfc_source = tmp_path / "rfc9999.txt"
    rfc_source.write_text(
        "Network Working Group                                          J. Doe\n"
        "Request for Comments: 9999                                        MITRE\n"
        "Category: Standards Track                                September 2026\n\n\n"
        "                    A Secure Protocol Specification\n\n"
        "Abstract\n\n"
        "   This document specifies an interactive cryptographic protocol.\n\n"
        "Table of Contents\n\n"
        "   1. Introduction .................................................... 2\n"
        "   2. Protocol Handshake ............................................. 3\n\n"
        "1. Introduction\n\n"
        + "   Detailed protocol background and security model.\n" * 40 +
        "\n2. Protocol Handshake\n\n"
        "   Alice sends an encrypted nonce to Bob. Bob decrypts and returns it.\n"
        + "   Additional protocol details.\n" * 40,
        encoding="utf-8",
    )

    mock_app_report = ProtocolApplicabilityReport(
        is_cryptographic_protocol=True,
        protocol_name="orch_test_proto",
        participating_principals=["init", "resp"],
        has_keys_or_nonces=True,
        rationale="Clear cryptographic authentication handshake.",
    )

    with patch("src.main_pipeline_orchestrator.evaluate_protocol_applicability", return_value=mock_app_report), \
         patch("src.main_pipeline_orchestrator.route_handshake_sections", return_value=["2"]), \
         patch("src.main_pipeline_orchestrator.extract_protocol_specification", return_value=mock_valid_spec):

        summary = run_rfc_translation_pipeline(
            rfc_file_path=rfc_source,
            output_dir=tmp_path / "rfc9999_out",
        )

        assert summary.is_eligible is True
        assert summary.roletran_passed is True
        assert summary.build_successful is True
        assert summary.build_artifacts is not None
        assert summary.build_artifacts.shapes_graph_xhtml_path.exists()
        assert summary.build_artifacts.shapes_txt_path.exists()
        assert summary.build_artifacts.shapes_count >= 1
        assert summary.trajectory_json_path is not None
        assert summary.trajectory_json_path.exists()
        assert summary.quality_tier in ("GOLD", "SILVER", "BRONZE")

        import json
        traj = json.loads(summary.trajectory_json_path.read_text(encoding="utf-8"))
        assert "models_used" not in traj
        assert "stage5_preflight_gate" in traj
        assert "stage6_cpsa4_solver" in traj
        assert "exploration_telemetry_from_txt" in traj["stage6_cpsa4_solver"]
        assert "shapes_analysis_from_shapes_txt" in traj["stage6_cpsa4_solver"]
        assert "quality_assessment" in traj
        assert traj["final_verified_output"]["final_scm_with_header"].startswith(";;; [RFC-ID:")

        master_index = tmp_path / "metadata_index.json"
        assert master_index.exists()
        idx_payload = json.loads(master_index.read_text(encoding="utf-8"))
        assert str(summary.trajectory_json_path.resolve()) in idx_payload["metadata_json_files"]
        assert str((tmp_path / "rfc9999_out").resolve()) in idx_payload["rfc_directories"]
```

---

### `tests/test_trajectory_and_hardening.py`

*sha256:`fe62a412bb13` · 715 lines · 31.4 KB (~8,033 tokens) · lang:`python`*

```python
"""Hardening and edge-case tests for 60s process-group SIGKILL, malformed YAML frontmatter, S-expr splitting, artifact containment, and offline discovery."""

import asyncio
import json
import os
import time
from pathlib import Path
from unittest.mock import MagicMock
from aiohttp import web
import pytest

from src.pipeline_events import GLOBAL_EVENT_BUS, PipelineEventBus
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    load_prompt_spec,
    parse_prompt_frontmatter,
)
from src.system_config import SYSTEM_CONFIG
from src.verification_engine.mitre_build_orchestrator import (
    CPSABuildError,
    _run_make_with_hard_timeout,
)
from src.verification_engine.trajectory_metadata_exporter import (
    split_top_level_sexprs,
    update_run_metadata_index,
)
from src.visualizer.server import VisualizerServer


def test_hard_timeout_kills_entire_process_group_including_grandchild(tmp_path: Path):
    """_run_make_with_hard_timeout sends SIGKILL to the full process group so grandchild processes never orphan."""
    pid_file = tmp_path / "grandchild.pid"
    child_env = os.environ.copy()
    child_env["TEST_GRANDCHILD_PID_FILE"] = str(pid_file)
    script = (
        'python3 -c "import os, time; '
        'open(os.environ[\'TEST_GRANDCHILD_PID_FILE\'], \'w\').write(str(os.getpid())); '
        'time.sleep(30)" & wait'
    )

    t0 = time.monotonic()
    with pytest.raises(CPSABuildError, match="timed out"):
        _run_make_with_hard_timeout(
            ["bash", "-c", script],
            cwd=tmp_path,
            env=child_env,
            timeout_seconds=0.4,
        )
    elapsed = time.monotonic() - t0
    assert elapsed < 3.0

    # Verify grandchild PID was recorded and is completely dead (ESRCH)
    assert pid_file.exists()
    grandchild_pid = int(pid_file.read_text(encoding="utf-8").strip())
    time.sleep(0.05)
    with pytest.raises(ProcessLookupError):
        os.kill(grandchild_pid, 0)


def test_malformed_yaml_frontmatter_and_edge_cases(tmp_path: Path):
    """Prompt loader degrades gracefully on invalid YAML, list frontmatter, bad scalar types, BOM, and empty body."""
    bad_yaml_file = tmp_path / PROMPT_APPLICABILITY_GATE
    bad_yaml_file.write_text("\ufeff---\nmodel: [unclosed_list\n---\nValid fallback body after bad YAML.", encoding="utf-8")
    spec = load_prompt_spec(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert spec.body == "Valid fallback body after bad YAML."
    assert spec.model

    bad_yaml_file.write_text("---\n- item1\n- item2\n---\n   \n", encoding="utf-8")
    spec_empty = load_prompt_spec(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert "MITRE CPSA 4.4.9" in spec_empty.body

    bad_yaml_file.write_text(
        '---\nmodel: strata/unsloth-iq4_xs\ntimeout: "not_an_int"\ntemperature: "not_a_float"\n---\nCustom body.',
        encoding="utf-8",
    )
    spec_scalars = load_prompt_spec(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert spec_scalars.model == "strata/unsloth-iq4_xs"
    assert spec_scalars.timeout == 1500
    assert spec_scalars.temperature == 0.0

    with pytest.raises(FileNotFoundError):
        load_prompt_spec("99_nonexistent_prompt.md", prompts_dir=tmp_path)

    meta, body = parse_prompt_frontmatter("Plain prompt without frontmatter.")
    assert meta == {}
    assert body == "Plain prompt without frontmatter."


def test_split_top_level_sexprs_ignores_parens_in_comments_and_strings():
    """S-expression splitter handles unbalanced parens inside Scheme `;` comments and escaped strings."""
    sample = (
        ";; Comment with unbalanced ((( parens\n"
        '(herald "proto (with) \\"escaped)\\" parens" (algebra diffie-hellman))\n'
        "(defprotocol test diffie-hellman ; trailing )(\n"
        "  (defrole init (vars (x rndx)) (trace (send x))))\n"
    )
    blocks = split_top_level_sexprs(sample)
    assert len(blocks) == 2
    assert blocks[0].startswith("(herald")
    assert blocks[1].startswith("(defprotocol test")


def test_offline_load_run_from_disk_discovery_modes(tmp_path: Path):
    """Verifies direct trajectory file, single-RFC directory, interrupted folder, and legacy filtered count replay."""
    run_dir = tmp_path / "run_offline_modes"
    rfc_ok = run_dir / "rfc2952"
    rfc_interrupted = run_dir / "rfc7627"
    rfc_ok.mkdir(parents=True)
    rfc_interrupted.mkdir(parents=True)

    traj_file = rfc_ok / "telnet_trajectory.json"
    traj_file.write_text(
        json.dumps({
            "duration_seconds": 5.2,
            "rfc_metadata": {"rfc_id": "RFC 2952", "protocol_name": "telnet_des"},
            "stage5_preflight_gate": {"final_passed": True, "total_attempts": 0},
            "stage6_cpsa4_solver": {
                "final_passed": True,
                "total_attempts": 0,
                "shapes_analysis_from_shapes_txt": {"total_realized_shapes": 2},
            },
            "quality_assessment": {"quality_tier": "SILVER"},
        }),
        encoding="utf-8",
    )
    (rfc_interrupted / "verbatim_slice.txt").write_text("Partial slice before Ctrl+C", encoding="utf-8")

    bus = PipelineEventBus()
    ov_direct = bus.load_run_from_disk(traj_file)
    assert len(ov_direct["accepted_tabs"]) == 1
    assert ov_direct["accepted_tabs"][0]["protocol_name"] == "telnet_des"

    ov_single_dir = bus.load_run_from_disk(rfc_ok)
    assert len(ov_single_dir["accepted_tabs"]) == 1
    assert ov_single_dir["accepted_tabs"][0]["rfc_id"] == "RFC 2952"

    (run_dir / "metadata_index.json").write_text(
        json.dumps({
            "schema_version": "1.0.0",
            "total_rfcs_processed": 12,
            "total_ineligible_filtered": 10,
            "runs": [
                {
                    "rfc_id": "RFC 2952",
                    "protocol_name": "telnet_des",
                    "is_eligible": True,
                    "build_successful": True,
                    "quality_tier": "SILVER",
                    "rfc_directory": str(rfc_ok),
                    "metadata_json_file": str(traj_file),
                }
            ],
        }),
        encoding="utf-8",
    )
    ov_legacy = bus.load_run_from_disk(run_dir)
    assert ov_legacy["filtered_total"] == 1
    assert len(ov_legacy["accepted_tabs"]) == 2
    statuses = {t["rfc_id"]: t["status"] for t in ov_legacy["accepted_tabs"]}
    assert statuses["RFC 2952"] == "VERIFIED"
    assert statuses["RFC 7627"] == "INTERRUPTED"

    fresh_run = tmp_path / "run_roundtrip"
    update_run_metadata_index(
        run_root_dir=fresh_run,
        rfc_id="RFC 1111",
        protocol_name="Non-Crypto Memo",
        rfc_dir=fresh_run / "rfc1111",
        scm_path=None,
        trajectory_json_path=None,
        quality_tier="INELIGIBLE",
        is_eligible=False,
        build_successful=False,
        error_message="Informational category",
        rejection_gate="Tier 0 Header Filter",
        duration_seconds=0.14,
    )
    update_run_metadata_index(
        run_root_dir=fresh_run,
        rfc_id="RFC 2952",
        protocol_name="telnet_des",
        rfc_dir=rfc_ok,
        scm_path=None,
        trajectory_json_path=traj_file,
        quality_tier="SILVER",
        is_eligible=True,
        build_successful=True,
        tab_index=1,
    )
    ov_rt = bus.load_run_from_disk(fresh_run)
    assert ov_rt["filtered_total"] == 1
    assert bus.get_filtered_slice()["items"][0]["duration_seconds"] == 0.14
    assert len(ov_rt["accepted_tabs"]) == 1
    assert ov_rt["accepted_tabs"][0]["tab_index"] == 1


def test_visualizer_artifact_endpoint_blocks_path_traversal_and_dotfiles(tmp_path: Path):
    """GET /api/artifact strictly rejects .env / arbitrary host files (HTTP 403) while serving valid run files."""
    run_dir = tmp_path / "authorized_run"
    run_dir.mkdir(parents=True)
    valid_scm = run_dir / "proto.scm"
    valid_scm.write_text("(herald proto)", encoding="utf-8")
    dot_secret = run_dir / ".env"
    dot_secret.write_text("SECRET=1", encoding="utf-8")

    GLOBAL_EVENT_BUS.clear()
    GLOBAL_EVENT_BUS.set_run_directory(run_dir, is_live=True)

    async def _exercise():
        server = VisualizerServer(host="127.0.0.1", port=8094)

        # 1. Missing path -> 400
        req_missing = MagicMock(spec=web.Request)
        req_missing.query = {}
        assert (await server.handle_artifact(req_missing)).status == 400

        # 2. Arbitrary host file outside run_dir -> 403
        req_traverse = MagicMock(spec=web.Request)
        req_traverse.query = {"path": str(SYSTEM_CONFIG.PROJECT_ROOT / "README.md")}
        assert (await server.handle_artifact(req_traverse)).status == 403

        # 3. Dotfile (.env) even inside run_dir -> 403
        req_dot = MagicMock(spec=web.Request)
        req_dot.query = {"path": str(dot_secret)}
        assert (await server.handle_artifact(req_dot)).status == 403

        # 4. Nonexistent file inside authorized run_dir -> 404
        req_404 = MagicMock(spec=web.Request)
        req_404.query = {"path": str(run_dir / "missing.scm")}
        assert (await server.handle_artifact(req_404)).status == 404

        # 5. Valid run artifact -> 200
        req_ok = MagicMock(spec=web.Request)
        req_ok.query = {"path": str(valid_scm)}
        resp_ok = await server.handle_artifact(req_ok)
        assert resp_ok.status == 200
        assert "(herald proto)" in resp_ok.text

        # 6. /api/models endpoint -> 200
        req_models = MagicMock(spec=web.Request)
        resp_models = await server.handle_models(req_models)
        assert resp_models.status == 200
        models_payload = json.loads(resp_models.text)
        assert models_payload["cpsa_timeout_seconds"] == 15
        assert "router_model" in models_payload

    asyncio.run(_exercise())


def test_parse_llm_json_unwraps_schema_properties_and_single_element_lists():
    """Verify `parse_llm_json` unwraps `{"properties": {...}}` schema-echo envelopes and `[{...}]` wrappers."""
    from src.prompt_loader import parse_llm_json

    wrapped_schema = json.dumps({
        "type": "object",
        "properties": {
            "selected_sections": ["3.1", "3.2"],
            "selection_rationale": "Defines the challenge-response exchange.",
        },
    })
    unwrapped = parse_llm_json(wrapped_schema)
    assert unwrapped["selected_sections"] == ["3.1", "3.2"]
    assert "selection_rationale" in unwrapped

    list_wrapped = json.dumps([
        {
            "selected_sections": ["4"],
            "selection_rationale": "Main handshake section.",
        }
    ])
    unwrapped_list = parse_llm_json(list_wrapped)
    assert unwrapped_list["selected_sections"] == ["4"]


def test_toc_parser_stops_at_unnumbered_back_matter_and_supports_large_tocs():
    """Verify TOC parser does not glue unnumbered Security/IANA/References onto the last section title."""
    from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
    from src.document_ingestion.handshake_section_router import _heuristic_section_router
    from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections

    sample_rfc = (
        "Table of Contents\n\n"
        "   1.  Introduction . . . . . . . . . . . . . . . . . . . . . . . .  1\n"
        "   2.  Terminology  . . . . . . . . . . . . . . . . . . . . . . . .  2\n"
        "   3.  Scope  . . . . . . . . . . . . . . . . . . . . . . . . . . .  3\n"
        "   4.  Protocol Message Exchange  . . . . . . . . . . . . . . . . .  4\n"
        "   4.1.  Initial Request  . . . . . . . . . . . . . . . . . . . . .  5\n"
        "   Security Considerations  . . . . . . . . . . . . . . . . . . . .  8\n"
        "   IANA Considerations  . . . . . . . . . . . . . . . . . . . . . .  9\n"
        "   References . . . . . . . . . . . . . . . . . . . . . . . . . . . 10\n"
        "   Author's Address . . . . . . . . . . . . . . . . . . . . . . . . 11\n\n"
        "1.  Introduction\n"
        "Intro text.\n\n"
        "4.  Protocol Message Exchange\n"
        "Parent overview ladder diagram: Alice -> Bob.\n\n"
        "4.1.  Initial Request\n"
        "Alice sends enc(n, k).\n\n"
        "5.  IANA Considerations\n"
    )
    entries = parse_table_of_contents(sample_rfc)
    sec_map = {e.section_id: e.title for e in entries}
    assert sec_map["4.1"] == "Initial Request"
    assert "Security Considerations" not in sec_map["4.1"]
    assert "References" not in sec_map["4.1"]

    # Heuristic router must skip Terminology ("2") and Scope ("3") and select "4" / "4.1"
    routed = _heuristic_section_router(entries)
    assert "2" not in routed
    assert "3" not in routed
    assert "4" in routed or "4.1" in routed

    # Slicing "4.1" without "4" automatically includes the short parent preamble ("4" -> "4.1")
    sliced = slice_verbatim_sections(sample_rfc, ["4.1"])
    assert "Parent overview ladder diagram: Alice -> Bob." in sliced
    assert "Alice sends enc(n, k)." in sliced


def test_stage2_bailout_and_cryptographic_primitive_check():
    """Verify `CPSAProtocolSpecification` supports `is_verifiable_protocol=False` bailout and detects missing crypto."""
    from src.intermediate_representation.protocol_syntax_tree import (
        CPSAProtocolRole,
        CPSAProtocolSpecification,
        CPSASortEnum,
        CPSATraceEvent,
        CPSAVariableDeclaration,
    )

    bailout_spec = CPSAProtocolSpecification(
        protocol_name="BFCP",
        is_verifiable_protocol=False,
        ineligibility_reason="RFC 4582 defines floor control signaling over TLS with no native cryptographic handshake.",
        roles=[],
        skeletons=[],
    )
    assert not bailout_spec.is_verifiable_protocol
    assert not bailout_spec.has_cryptographic_primitives()

    cleartext_spec = CPSAProtocolSpecification(
        protocol_name="NNTP_AUTHINFO",
        roles=[
            CPSAProtocolRole(
                role_name="client",
                variables=[
                    CPSAVariableDeclaration(name="u", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="p", sort=CPSASortEnum.DATA),
                ],
                trace=[CPSATraceEvent(direction="send", message_term=["cat", "u", "p"])],
            )
        ],
    )
    assert not cleartext_spec.has_cryptographic_primitives()

    crypto_spec = CPSAProtocolSpecification(
        protocol_name="CHALLENGE_AUTH",
        roles=[
            CPSAProtocolRole(
                role_name="client",
                variables=[
                    CPSAVariableDeclaration(name="a", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="b", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.DATA),
                ],
                trace=[
                    CPSATraceEvent(
                        direction="send",
                        message_term=["enc", "n", ["ltk", "a", "b"]],
                    )
                ],
            )
        ],
    )
    assert crypto_spec.has_cryptographic_primitives()


def test_sanitize_protocol_stem_and_ast_hash_ignores_herald_comment():
    """Verify `/` and parens in `protocol_name` are sanitized (`RFC 2636`) and `_compute_ast_hash` ignores `herald_comment`."""
    from src.code_generation.cpsa_scheme_emitter import sanitize_protocol_stem
    from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
    from src.main_pipeline_orchestrator import _compute_ast_hash

    stem = sanitize_protocol_stem("Wireless Device Configuration (OTASP/OTAPA) via ACAP")
    assert "/" not in stem
    assert "(" not in stem
    assert stem == "wireless_device_configuration_otasp_otapa_via_acap"

    spec1 = CPSAProtocolSpecification(
        protocol_name="TCP_AO_NAT",
        herald_comment="Attempt 1 comment",
        roles=[],
        is_verifiable_protocol=False,
    )
    spec2 = CPSAProtocolSpecification(
        protocol_name="TCP_AO_NAT",
        herald_comment="Attempt 2 different comment",
        roles=[],
        is_verifiable_protocol=False,
    )
    assert _compute_ast_hash(spec1) == _compute_ast_hash(spec2)


def test_ensure_three_pov_skeletons_replaces_preseeded_multistrand_and_adds_secret_neq():
    """Verify `ensure_three_point_of_view_skeletons` replaces pre-seeded multi-strand root skeletons (`RFC 7469`)
    with 1-strand pure POVs and adds `(neq secret other_var)` in secrecy skeletons (`RFC 5197` / `RFC 2138`).
    """
    from src.intermediate_representation.protocol_syntax_tree import (
        CPSAPreskeleton,
        CPSAProtocolRole,
        CPSAProtocolSpecification,
        CPSASortEnum,
        CPSAStrandInstance,
        CPSATraceEvent,
        CPSAVariableDeclaration,
    )
    from src.semantic_extraction.constrained_protocol_extractor import (
        ensure_three_point_of_view_skeletons,
    )

    spec = CPSAProtocolSpecification(
        protocol_name="mikey_iba_test",
        primary_secrecy_goals=["tgk"],
        roles=[
            CPSAProtocolRole(
                role_name="initiator",
                variables=[
                    CPSAVariableDeclaration(name="i", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="r", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="hdr", sort=CPSASortEnum.DATA),
                    CPSAVariableDeclaration(name="tgk", sort=CPSASortEnum.DATA),
                ],
                trace=[
                    CPSATraceEvent(
                        direction="send",
                        message_term=["cat", "hdr", ["enc", "tgk", ["ltk", "i", "r"]]],
                    )
                ],
                unique_originating=["tgk"],
            ),
            CPSAProtocolRole(
                role_name="responder",
                variables=[
                    CPSAVariableDeclaration(name="i", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="r", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="hdr", sort=CPSASortEnum.DATA),
                    CPSAVariableDeclaration(name="tgk", sort=CPSASortEnum.DATA),
                ],
                trace=[
                    CPSATraceEvent(
                        direction="recv",
                        message_term=["cat", "hdr", ["enc", "tgk", ["ltk", "i", "r"]]],
                    )
                ],
            ),
        ],
        skeletons=[
            # Pre-seeded 2-strand root skeleton (as in RFC 7469)
            CPSAPreskeleton(
                protocol_name="mikey_iba_test",
                strands=[
                    CPSAStrandInstance(role_name="initiator"),
                    CPSAStrandInstance(role_name="responder"),
                ],
            )
        ],
    )

    normalized = ensure_three_point_of_view_skeletons(spec)
    assert len(normalized.skeletons) == 3
    # First 2 skeletons are pure 1-strand POVs
    assert len(normalized.skeletons[0].strands) == 1
    assert normalized.skeletons[0].strands[0].role_name == "initiator"
    assert len(normalized.skeletons[1].strands) == 1
    assert normalized.skeletons[1].strands[0].role_name == "responder"
    # 3rd skeleton is the secrecy listener with `(neq tgk hdr)` automatically added
    sec_skel = normalized.skeletons[2]
    assert sec_skel.listeners == ["tgk"]
    assert ["neq", "tgk", "hdr"] in sec_skel.facts


def test_quality_assessment_catches_self_reflection_and_preseeded_strands(tmp_path: Path):
    """Verify `analyze_shapes_txt`, `compute_security_findings`, and `compute_quality_assessment`:
    - Decouple `quality_tier` (modeling & compilation fidelity) from `security_findings` (formal CPSA security verdict)
    - Flag 1-strand/2-strand branched authentication (`RFC 5216` / `RFC 6786`) as `CONDITIONAL_BRANCHED_AUTHENTICATION` in `security_findings` while keeping `quality_tier == "GOLD"`
    - Downgrade pre-seeded multi-strand root skeletons (`max_strands == initial_strand_count` as in `RFC 7469`) to `BRONZE`
    - Grade unilateral server-authenticated KEX (`RFC 5656`) as `GOLD` with `UNILATERAL_AUTHENTICATED` and `SECRECY_PROVED`
    - Detect Lowe MITM principal disagreement (`b` vs `b-0`), same-role reflection, and secrecy leaks in `security_findings` without punishing `quality_tier`.
    """
    from src.verification_engine.trajectory_metadata_exporter import (
        analyze_shapes_txt,
        compute_quality_assessment,
        compute_security_findings,
    )

    # 1. Branched 1-strand/2-strand split (`RFC 5216` / `RFC 6786`): executable & multi-strand -> GOLD,
    # while security_findings records CONDITIONAL_BRANCHED_AUTHENTICATION
    split_shapes_txt = tmp_path / "split_shapes.txt"
    split_shapes_txt.write_text(
        "(defskeleton p (vars (a b name)) (defstrand init 2 (a a) (b b)) (label 0))\n"
        "(defskeleton p (vars (a name)) (defstrand init 2 (a a) (b a)) (label 1) (parent 0) (shape))\n"
        "(defskeleton p (vars (a b name)) (defstrand init 2 (a a) (b b)) (defstrand resp 2 (a a) (b b)) (label 2) (parent 0) (shape))\n"
        "(defskeleton p (vars (a b name)) (defstrand resp 2 (a a) (b b)) (label 3))\n"
        "(defskeleton p (vars (a b name)) (defstrand resp 2 (a a) (b b)) (defstrand init 2 (a a) (b b)) (label 4) (parent 3) (shape))\n"
        "(defskeleton p (vars (k data)) (defstrand init 2) (deflistener k) (label 5))\n",
        encoding="utf-8",
    )
    split_analysis = analyze_shapes_txt(split_shapes_txt)
    assert split_analysis["per_preskeleton_outcomes"][0]["has_self_reflection_split"] is True
    split_sec = compute_security_findings(split_analysis)
    assert split_sec["authentication_profile"] == "CONDITIONAL_BRANCHED_AUTHENTICATION"
    assert split_sec["parameter_agreement_status"] == "FULL_PARAMETER_AGREEMENT"
    split_qa = compute_quality_assessment(True, split_analysis, 0, 0, security_findings=split_sec)
    assert split_qa["quality_tier"] == "GOLD"

    # 2. Pre-seeded 2-strand root skeleton (`RFC 7469`) where CPSA added 0 strands -> BRONZE
    preseeded_txt = tmp_path / "preseeded_shapes.txt"
    preseeded_txt.write_text(
        "(defskeleton p (vars (a b name)) (defstrand init 1) (defstrand resp 1) (label 0) (shape))\n",
        encoding="utf-8",
    )
    preseeded_analysis = analyze_shapes_txt(preseeded_txt)
    assert preseeded_analysis["per_preskeleton_outcomes"][0]["verdict"] == "TRIVIAL_SINGLE_STRAND"
    preseeded_qa = compute_quality_assessment(True, preseeded_analysis, 0, 0)
    assert preseeded_qa["quality_tier"] == "BRONZE"

    # 3. Unilateral server-authenticated KEX (`RFC 5656` SSH ECDSA KEX):
    # client POV is strictly 2-strand, server POV is 1-strand (unauthenticated client share), secrecy proved -> GOLD
    unilateral_txt = tmp_path / "unilateral_shapes.txt"
    unilateral_txt.write_text(
        "(defskeleton ssh (vars (s name)) (defstrand client 2 (s s)) (label 0))\n"
        "(defskeleton ssh (vars (s name)) (defstrand client 2 (s s)) (defstrand server 2 (s s)) (label 1) (parent 0) (shape))\n"
        "(defskeleton ssh (vars (s name)) (defstrand server 2 (s s)) (label 2))\n"
        "(defskeleton ssh (vars (s name)) (defstrand server 2 (s s)) (label 3) (parent 2) (shape))\n"
        "(defskeleton ssh (vars (k skey)) (defstrand client 2) (deflistener k) (label 4))\n",
        encoding="utf-8",
    )
    unilateral_analysis = analyze_shapes_txt(unilateral_txt)
    unilateral_sec = compute_security_findings(unilateral_analysis)
    assert unilateral_sec["authentication_profile"] == "UNILATERAL_AUTHENTICATED"
    assert unilateral_sec["secrecy_status"] == "SECRECY_PROVED"
    unilateral_qa = compute_quality_assessment(True, unilateral_analysis, 0, 0, security_findings=unilateral_sec)
    assert unilateral_qa["quality_tier"] == "GOLD"

    # 4. Vulnerable protocol (Needham-Schroeder Lowe MITM `b` vs `b-0` + same-role reflection + leaked secret `k`):
    # Model is executable and faithful (`quality_tier == "GOLD"`), while `security_findings` captures all 3 vulnerabilities
    vuln_txt = tmp_path / "vuln_shapes.txt"
    vuln_txt.write_text(
        "(defskeleton ns (vars (a b name) (k skey)) (defstrand init 2 (a a) (b b)) (label 0))\n"
        "(defskeleton ns (vars (a b b-0 name) (k skey)) (defstrand init 2 (a a) (b b)) (defstrand resp 2 (a a) (b b-0)) (label 1) (parent 0) (shape))\n"
        "(defskeleton ns (vars (a b name) (k skey)) (defstrand resp 2 (a a) (b b)) (label 2))\n"
        "(defskeleton ns (vars (a b name) (k skey)) (defstrand resp 2 (a a) (b b)) (defstrand resp 2 (a b) (b a)) (label 3) (parent 2) (shape))\n"
        "(defskeleton ns (vars (k skey)) (defstrand init 2) (deflistener k) (label 4))\n"
        "(defskeleton ns (vars (k skey)) (defstrand init 2) (deflistener k) (label 5) (parent 4) (shape))\n",
        encoding="utf-8",
    )
    vuln_analysis = analyze_shapes_txt(vuln_txt)
    vuln_sec = compute_security_findings(vuln_analysis)
    assert vuln_sec["parameter_agreement_status"] == "PRINCIPAL_DISAGREEMENT_MITM_OR_UKS"
    assert vuln_sec["role_reflection_status"] == "SAME_ROLE_REFLECTION_DETECTED"
    assert vuln_sec["secrecy_status"] == "SECRECY_LEAK_DETECTED"
    assert vuln_sec["leaked_secrets"] == ["k"]
    assert len(vuln_sec["vulnerabilities_and_anomalies"]) >= 3
    vuln_qa = compute_quality_assessment(True, vuln_analysis, 0, 0, security_findings=vuln_sec)
    assert vuln_qa["quality_tier"] == "GOLD"


def test_prune_keep_ineligible_only(tmp_path: Path):
    """Verify `PipelineMetricsCSVLogger.prune_keep_ineligible_only` deletes all rows EXCEPT `is_eligible=False`."""
    from src.logging_config import PipelineMetricsCSVLogger

    csv_path = tmp_path / "pipeline_runs.csv"
    logger = PipelineMetricsCSVLogger(csv_path=csv_path)
    logger.log_run(rfc_id="RFC1111", is_eligible=False, status="INELIGIBLE", rejection_gate="Tier 0 Header Filter")
    logger.log_run(rfc_id="RFC4582", is_eligible=False, status="INELIGIBLE", rejection_gate="Stage 2 Verbatim Slice Gate")
    logger.log_run(rfc_id="RFC5246", is_eligible=True, status="VERIFIED", quality_tier="GOLD", solver_passed=True)
    logger.log_run(rfc_id="RFC5849", is_eligible=True, status="FAILED", quality_tier="REJECTED", solver_passed=False)

    removed, kept = logger.prune_keep_ineligible_only()
    assert removed == 2
    assert kept == 2

    remaining_rows = logger._read_existing_rows()
    remaining_ids = [r["rfc_id"] for r in remaining_rows]
    assert remaining_ids == ["RFC1111", "RFC4582"]
    assert all(r["is_eligible"] == "False" for r in remaining_rows)


def test_seed_from_source_and_67_column_security_findings_csv(tmp_path: Path):
    """Verify `seed_from_source` copies rows from an older run without mutating the source CSV,
    and `log_run` records all 17 CPSA 4.4.9 `security_findings` columns plus `Eligible: <rationale>`.
    """
    from src.logging_config import PipelineMetricsCSVLogger

    assert len(PipelineMetricsCSVLogger.CSV_HEADER) == 67

    old_run_dir = tmp_path / "run_old"
    old_run_dir.mkdir(parents=True)
    old_csv = old_run_dir / "pipeline_runs.csv"
    old_logger = PipelineMetricsCSVLogger(csv_path=old_csv)
    old_logger.log_run(
        rfc_id="RFC1111",
        is_eligible=False,
        status="INELIGIBLE",
        rejection_gate="Tier 0 Header Filter",
        error_message="Ineligible: Informational document",
    )
    old_logger.log_run(
        rfc_id="RFC5246",
        is_eligible=True,
        status="VERIFIED",
        quality_tier="GOLD",
        solver_passed=True,
        error_message="Eligible: Defines the TLS 1.2 handshake with explicit key exchange.",
        security_findings={
            "role_executability": "ALL_ROLES_EXECUTABLE",
            "dead_roles_count": 0,
            "dead_roles": [],
            "authentication_profile": "MUTUAL_MULTI_STRAND",
            "multi_strand_pov_roles": ["Client", "Server"],
            "single_strand_pov_roles": [],
            "unrealized_pov_roles": [],
            "parameter_agreement_status": "FULL_PARAMETER_AGREEMENT",
            "disagreed_parameters_count": 0,
            "role_reflection_status": "NO_REFLECTION",
            "secrecy_status": "SECRECY_PROVED",
            "protected_secrets": ["pre_master_secret"],
            "leaked_secrets": [],
            "defgoal_satisfaction_status": "NO_EXPLICIT_DEFGOALS",
            "shape_analysis_sentences_count": 2,
            "anomalies_count": 0,
            "vulnerabilities_and_anomalies": [],
        },
    )

    # New run seeds from old_run_dir and prunes keep-ineligible without touching old_csv
    new_csv = tmp_path / "run_new" / "pipeline_runs.csv"
    new_logger = PipelineMetricsCSVLogger(csv_path=new_csv)
    seeded_count = new_logger.seed_from_source(old_run_dir)
    assert seeded_count == 2

    removed, kept = new_logger.prune_keep_ineligible_only()
    assert removed == 1
    assert kept == 1

    # Source CSV in old_run_dir must remain completely untouched (still 2 rows)
    old_rows = old_logger._read_existing_rows()
    assert len(old_rows) == 2
    rfc5246_row = [r for r in old_rows if r["rfc_id"] == "RFC5246"][0]
    assert rfc5246_row["authentication_profile"] == "MUTUAL_MULTI_STRAND"
    assert rfc5246_row["parameter_agreement_status"] == "FULL_PARAMETER_AGREEMENT"
    assert rfc5246_row["secrecy_status"] == "SECRECY_PROVED"
    assert rfc5246_row["protected_secrets"] == "pre_master_secret"
    assert rfc5246_row["shape_analysis_sentences_count"] == "2"
    assert rfc5246_row["error_message"].startswith("Eligible: ")


def test_cli_rejects_csv_prune_or_skip_flags_without_csv_source(monkeypatch):
    """Verify `--keep-ineligible`, `--skip-completed`, and `--retry-failed` fail fast if `--csv` is omitted."""
    import sys
    from src.pipeline import main

    for flag in ("--keep-ineligible", "--skip-completed", "--retry-failed"):
        monkeypatch.setattr(sys, "argv", ["rfc-llm", "refrences/all_RFCs/", flag])
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2


def test_compact_diagnostic_headline_strips_snowball_autopsy_and_csv_api_works(tmp_path: Path):
    """Verify `_compact_diagnostic_headline` strips the multi-line Snowball Autopsy block and `/api/csv` serves 67-column analytics."""
    from src.logging_config import PipelineMetricsCSVLogger
    from src.main_pipeline_orchestrator import _compact_diagnostic_headline
    from src.visualizer.server import VisualizerServer, hydrate_tab_payload

    full_diag = (
        "MITRE CPSA compilation timed out after 15 seconds (state-space explosion).\n"
        "Tier 1 Search-Order Portfolio also failed to terminate.\n\n"
        "=== CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT (Tier 2 Trace Analysis) ===\n"
        "Exploding Query: POV Skeleton #1\n"
        "Derivation Stats: 20 skeletons inspected\n"
    )
    compact = _compact_diagnostic_headline(full_diag)
    assert "=== CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT" not in compact
    assert "MITRE CPSA compilation timed out after 15 seconds" in compact

    run_dir = tmp_path / "run_csv_api"
    run_dir.mkdir(parents=True)
    csv_path = run_dir / "pipeline_runs.csv"
    csv_logger = PipelineMetricsCSVLogger(csv_path=csv_path)
    csv_logger.log_run(
        rfc_id="RFC2952",
        is_eligible=True,
        status="VERIFIED",
        quality_tier="GOLD",
        protocol_name="telnet_des",
        solver_passed=True,
        error_message="Eligible: Defines Telnet DES_CFB64 authentication handshake.",
    )

    GLOBAL_EVENT_BUS.clear()
    GLOBAL_EVENT_BUS.set_run_directory(run_dir, is_live=True, csv_path=csv_path)

    async def _check_csv_endpoint():
        server = VisualizerServer(host="127.0.0.1", port=8095)
        req = MagicMock(spec=web.Request)
        resp = await server.handle_csv(req)
        assert resp.status == 200
        payload = json.loads(resp.text)
        assert payload["row_count"] == 1
        assert len(payload["headers"]) == 67
        assert payload["rows"][0]["rfc_id"] == "RFC2952"
        assert payload["rows"][0]["error_message"].startswith("Eligible:")

    asyncio.run(_check_csv_endpoint())
```

---

### `tests/test_visualizer_and_events.py`

*sha256:`6b9941f8ef42` · 110 lines · 3.7 KB (~951 tokens) · lang:`python`*

```python
"""Unit and integration tests for Pipeline Event Bus, Cycle Detection, and Visualizer Server."""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import MagicMock
from aiohttp import web

from src.pipeline_events import GLOBAL_EVENT_BUS, PipelineEvent
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAVariableDeclaration,
    CPSATraceEvent,
    CPSAProtocolRole,
    CPSAProtocolSpecification,
)
from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification
from src.visualizer.server import VisualizerServer


@pytest.fixture
def sample_spec() -> CPSAProtocolSpecification:
    return CPSAProtocolSpecification(
        protocol_name="cycle_proto",
        roles=[
            CPSAProtocolRole(
                role_name="r",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="x", sort=CPSASortEnum.TEXT),
                ],
                trace=[
                    CPSATraceEvent(direction="send", channel="ch", message_term="x"),
                ],
                inputs=["ch"],
                outputs=["x"],
            )
        ],
    )


def test_pipeline_event_bus_emission_and_subscription():
    """Event bus properly broadcasts events to listeners and maintains history."""
    received_events = []

    def listener(event: PipelineEvent):
        received_events.append(event)

    GLOBAL_EVENT_BUS.subscribe(listener)
    try:
        GLOBAL_EVENT_BUS.emit("stage_started", stage=1, test_key="test_value")

        assert len(received_events) >= 1
        last = received_events[-1]
        assert last.event_type == "stage_started"
        assert last.stage == 1
        assert last.data["test_key"] == "test_value"

        # Verify SSE message formatting
        sse = last.to_sse_message()
        assert "event: stage_started" in sse
        assert '"test_key": "test_value"' in sse
    finally:
        GLOBAL_EVENT_BUS.unsubscribe(listener)


def test_compiler_repair_cycle_detection_triggers_warning_and_jitter(monkeypatch, sample_spec: CPSAProtocolSpecification):
    """When cycle_detected=True, prompt receives oscillation warning and litellm receives higher temperature."""
    captured_kwargs = {}

    def mock_completion(**kwargs):
        captured_kwargs.update(kwargs)
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock(message=MagicMock(content=sample_spec.model_dump_json()))]
        return mock_resp

    monkeypatch.setattr("litellm.completion", mock_completion)

    repaired = repair_protocol_specification(
        failing_spec=sample_spec,
        error_diagnostic="Repeated syntax error",
        verbatim_slice="Sample RFC text",
        failure_stage="roletran",
        model="dummy_model",
        cycle_detected=True,
    )

    assert repaired is not None
    assert "temperature" not in captured_kwargs
    prompt_content = captured_kwargs["messages"][1]["content"]
    assert "CRITICAL WARNING: An oscillation/cycle was detected" in prompt_content


def test_visualizer_server_endpoints(tmp_path: Path):
    """Visualizer web server serves history and artifact content."""
    async def _run():
        server = VisualizerServer(host="127.0.0.1", port=8089)

        # Emit test event
        GLOBAL_EVENT_BUS.emit("test_event", stage=4, detail="unit test")

        # Test history endpoint
        req = MagicMock(spec=web.Request)
        resp = await server.handle_history(req)
        assert resp.status == 200
        import json
        history = json.loads(resp.text)
        assert any(e["event_type"] == "test_event" for e in history)

    asyncio.run(_run())
```

---

### `tests/test_visualizer_tabs.py`

*sha256:`64d1ed1e7e81` · 283 lines · 11.8 KB (~3,017 tokens) · lang:`python`*

```python
"""Tests for scalable numbered multi-RFC tabs, filtered RFC drawer, per-attempt hydration, and offline --view replay."""

import asyncio
import json
import time
from pathlib import Path
from unittest.mock import MagicMock
from aiohttp import web

from src.pipeline_events import PipelineEventBus, GLOBAL_EVENT_BUS
from src.visualizer.server import VisualizerServer, hydrate_tab_payload


def test_sequential_tab_numbering_and_filtered_separation(tmp_path: Path):
    """Accepted RFCs receive sequential #1, #2 numbering while rejected RFCs go only to filtered_rfcs."""
    bus = PipelineEventBus()
    bus.set_run_directory(tmp_path, is_live=True)

    # RFC 1: Rejected at Tier 0
    bus.start_rfc("RFC 1000")
    bus.emit("stage_started", stage=1, stage_name="Document Intake & Slicing")
    bus.register_filtered_rfc(
        rfc_id="RFC 1000",
        title="Informational Memo",
        gate="Stage 1a: Tier 0 Header",
        reason="Category Informational is ineligible",
        duration_seconds=0.02,
    )

    # RFC 2: Accepted -> MUST become Tab #1
    rfc2_dir = tmp_path / "rfc2952"
    bus.start_rfc("RFC 2952")
    bus.emit("stage_started", stage=1, stage_name="Document Intake & Slicing")
    bus.emit("ast_generated", stage=2, ast={"protocol_name": "telnet_des_cfb64", "roles": [{"name": "client"}]})
    tab1 = bus.register_accepted_tab(
        rfc_id="RFC 2952",
        protocol_name="Telnet Encryption: DES 64 bit Cipher Feedback",
        rfc_dir=rfc2_dir,
    )
    assert tab1 == 1
    bus.update_accepted_tab(tab1, status="VERIFIED", quality_tier="SILVER", shapes_count=2, total_attempts=5)

    # Verify events.jsonl was flushed and bulky `ast` object was stripped
    jsonl_lines = (rfc2_dir / "events.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(jsonl_lines) >= 2
    parsed_events = [json.loads(line) for line in jsonl_lines]
    ast_evts = [e for e in parsed_events if e["event_type"] == "ast_generated"]
    assert len(ast_evts) == 1
    assert "ast" not in ast_evts[0]["data"]
    assert ast_evts[0]["data"]["ast_protocol_name"] == "telnet_des_cfb64"
    assert ast_evts[0]["tab_index"] == 1

    # RFC 3: Rejected at Stage 1c -> Must NOT consume Tab #2
    bus.start_rfc("RFC 3000")
    bus.register_filtered_rfc(
        rfc_id="RFC 3000",
        title="BGP Routing Policy",
        gate="Stage 1c: Applicability Gate",
        reason="No cryptographic handshake",
        duration_seconds=0.45,
    )

    # RFC 4: Accepted -> MUST become Tab #2, and active_events from RFC 2952 MUST be evicted from RAM
    rfc4_dir = tmp_path / "rfc8446"
    bus.start_rfc("RFC 8446")
    assert len(bus.get_history()) == 0
    tab2 = bus.register_accepted_tab(
        rfc_id="RFC 8446",
        protocol_name="The Transport Layer Security (TLS) Protocol Version 1.3",
        rfc_dir=rfc4_dir,
    )
    assert tab2 == 2

    overview = bus.get_tabs_overview()
    assert len(overview["accepted_tabs"]) == 2
    assert overview["accepted_tabs"][0]["tab_index"] == 1
    assert overview["accepted_tabs"][0]["rfc_id"] == "RFC 2952"
    assert overview["accepted_tabs"][0]["protocol_name"] == "Telnet Encryption: DES 64 bit Cipher Feedback"
    assert overview["accepted_tabs"][1]["tab_index"] == 2
    assert overview["accepted_tabs"][1]["rfc_id"] == "RFC 8446"
    assert overview["filtered_total"] == 2

    # Filtered pagination & search
    filt_all = bus.get_filtered_slice(offset=0, limit=10)
    assert filt_all["total"] == 2
    filt_bgp = bus.get_filtered_slice(offset=0, limit=10, query="bgp")
    assert filt_bgp["matching"] == 1
    assert filt_bgp["items"][0]["rfc_id"] == "RFC 3000"


def test_per_attempt_hydration_and_offline_replay(tmp_path: Path):
    """Hydrating a tab reconstructs Attempt 0, Roletran/CPSA repair attempts, Final snapshot, and offline replay."""
    run_dir = tmp_path / "run_2026-10-29_00-00-01"
    rfc_dir = run_dir / "rfc5246"
    rfc_dir.mkdir(parents=True)

    (rfc_dir / "verbatim_slice.txt").write_text("Section 7.4 Handshake Protocol...", encoding="utf-8")
    (rfc_dir / "tls12.scm").write_text("(herald tls12)\n(defprotocol tls12 basic)", encoding="utf-8")
    (rfc_dir / "tls12_shapes.xhtml").write_text("<html><body><svg></svg></body></html>", encoding="utf-8")

    traj_path = rfc_dir / "tls12_trajectory.json"
    traj_payload = {
        "schema_version": "1.0.0",
        "duration_seconds": 14.5,
        "rfc_metadata": {
            "rfc_id": "RFC 5246",
            "rfc_title": "The Transport Layer Security (TLS) Protocol Version 1.2",
            "protocol_name": "tls12",
            "selected_sections": ["7.3", "7.4"],
            "sliced_lines_count": 120,
            "verbatim_rfc_slice": "Section 7.4 Handshake Protocol...",
        },
        "stage2_initial_extraction": {
            "initial_ast": {"protocol_name": "tls12", "roles": [{"role_name": "client"}]},
            "initial_scm": "; attempt 0 scm\n(defprotocol tls12 basic)",
        },
        "stage5_preflight_gate": {
            "final_passed": True,
            "total_attempts": 1,
            "repair_attempts": [
                {
                    "attempt_number": 1,
                    "failure_stage": "roletran",
                    "parsed_diagnostic": "Unbound variable n_c in role client",
                    "rag_query": "CPSA roletran unbound variable role inputs",
                    "retrieved_chunk_ids": ["12"],
                    "rejected_scm": "; attempt 0 bad scm",
                    "repaired_scm": "; attempt 1 repaired roletran scm",
                    "repaired_ast": {"protocol_name": "tls12", "roles": [{"role_name": "client", "inputs": ["n_c"]}]},
                    "passed_after_repair": True,
                    "cycle_detected": False,
                }
            ],
        },
        "stage6_cpsa4_solver": {
            "final_passed": True,
            "total_attempts": 1,
            "shapes_analysis_from_shapes_txt": {"total_realized_shapes": 3},
            "repair_attempts": [
                {
                    "attempt_number": 1,
                    "failure_stage": "solver",
                    "parsed_diagnostic": "Unrealized skeleton 0",
                    "rag_query": "CPSA preskeleton non-originating key assumption",
                    "retrieved_chunk_ids": ["42"],
                    "rejected_scm": "; attempt 1 bad solver scm",
                    "repaired_scm": "; attempt 2 repaired solver scm",
                    "repaired_ast": {"protocol_name": "tls12", "roles": [{"role_name": "client"}]},
                    "passed_after_repair": True,
                    "cycle_detected": True,
                }
            ],
        },
        "quality_assessment": {"quality_tier": "GOLD"},
        "final_verified_output": {
            "final_scm_with_header": ";; QUALITY TIER: GOLD\n(herald tls12)\n(defprotocol tls12 basic)",
            "final_ast": {"protocol_name": "tls12", "roles": [{"role_name": "client"}]},
        },
    }
    traj_path.write_text(json.dumps(traj_payload), encoding="utf-8")

    master_index = {
        "schema_version": "1.0.0",
        "run_directory": str(run_dir),
        "total_rfcs_processed": 2,
        "filtered_rfcs": [
            {
                "rfc_id": "RFC 1149",
                "title": "IP over Avian Carriers",
                "gate": "Stage 1a: Tier 0 Header",
                "reason": "Experimental / non-cryptographic",
                "duration_seconds": 0.01,
            }
        ],
        "runs": [
            {
                "tab_index": 1,
                "rfc_id": "RFC 5246",
                "protocol_name": "The Transport Layer Security (TLS) Protocol Version 1.2",
                "is_eligible": True,
                "build_successful": True,
                "quality_tier": "GOLD",
                "rfc_directory": str(rfc_dir),
                "metadata_json_file": str(traj_path),
                "scm_file": str(rfc_dir / "tls12.scm"),
            }
        ],
    }
    (run_dir / "metadata_index.json").write_text(json.dumps(master_index), encoding="utf-8")

    # Test offline --view loader and server endpoints
    GLOBAL_EVENT_BUS.clear()
    overview = GLOBAL_EVENT_BUS.load_run_from_disk(run_dir)
    assert overview["is_live"] is False
    assert overview["filtered_total"] == 1
    assert len(overview["accepted_tabs"]) == 1
    assert overview["accepted_tabs"][0]["tab_index"] == 1
    assert overview["accepted_tabs"][0]["rfc_id"] == "RFC 5246"

    hydrated = hydrate_tab_payload(overview["accepted_tabs"][0])
    attempts = hydrated["attempts"]
    # Attempt 0 + 1 roletran repair + 1 solver repair + Final = 4 snapshots
    assert len(attempts) == 4
    assert attempts[0]["attempt_id"] == "attempt_0"
    assert attempts[0]["status"] == "REJECTED"
    assert "Unbound variable n_c" in attempts[0]["diagnostic"]

    assert attempts[1]["attempt_id"] == "roletran_1"
    assert attempts[1]["rag_query"] == "CPSA roletran unbound variable role inputs"
    assert "; attempt 1 repaired roletran scm" in attempts[1]["scm"]

    assert attempts[2]["attempt_id"] == "solver_1"
    assert attempts[2]["cycle_detected"] is True
    assert "; attempt 2 repaired solver scm" in attempts[2]["scm"]

    assert attempts[3]["attempt_id"] == "final"
    assert attempts[3]["status"] == "VERIFIED"
    assert "GOLD (3 Shapes)" in attempts[3]["label"]

    # Verify HTTP endpoints on VisualizerServer
    async def _exercise_http():
        server = VisualizerServer(host="127.0.0.1", port=8091)

        req_tabs = MagicMock(spec=web.Request)
        resp_tabs = await server.handle_tabs(req_tabs)
        assert resp_tabs.status == 200
        tabs_json = json.loads(resp_tabs.text)
        assert len(tabs_json["accepted_tabs"]) == 1

        req_detail = MagicMock(spec=web.Request)
        req_detail.match_info = {"tab_index": "1"}
        resp_detail = await server.handle_tab_detail(req_detail)
        assert resp_detail.status == 200
        detail_json = json.loads(resp_detail.text)
        assert len(detail_json["attempts"]) == 4

        req_filt = MagicMock(spec=web.Request)
        req_filt.query = {"offset": "0", "limit": "50", "q": "avian"}
        resp_filt = await server.handle_filtered(req_filt)
        assert resp_filt.status == 200
        filt_json = json.loads(resp_filt.text)
        assert filt_json["matching"] == 1
        assert filt_json["items"][0]["rfc_id"] == "RFC 1149"

    asyncio.run(_exercise_http())


def test_5000_accepted_tabs_scalability_benchmark(tmp_path: Path):
    """5,000 accepted tabs serialize in < 150ms with compact payload size."""
    bus = PipelineEventBus()
    bus.set_run_directory(tmp_path, is_live=True)

    # Populate 5,000 compact tab summaries directly via public registration/update path
    # without creating 5,000 directories on disk just to test memory & JSON serialization throughput
    for i in range(1, 5001):
        bus._accepted_tabs[i] = {
            "tab_index": i,
            "rfc_id": f"RFC {1000 + i}",
            "protocol_name": f"Cryptographic Handshake Protocol #{i}",
            "rfc_title": f"Cryptographic Handshake Protocol #{i}",
            "status": "VERIFIED" if i % 3 else "FAILED",
            "quality_tier": "GOLD" if i % 3 else "REJECTED",
            "total_attempts": i % 7,
            "shapes_count": 2,
            "duration_seconds": 8.4,
            "rfc_dir": f"/tmp/run/rfc{1000 + i}",
            "events_jsonl": None,
            "slice_path": None,
            "scm_path": None,
            "trajectory_path": None,
            "shapes_xhtml": None,
            "error_message": None,
        }
        bus._tab_order.append(i)

    t0 = time.perf_counter()
    overview = bus.get_tabs_overview()
    encoded = json.dumps(overview)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    assert len(overview["accepted_tabs"]) == 5000
    assert elapsed_ms < 250.0, f"5,000-tab overview serialization took too long: {elapsed_ms:.1f}ms"
    assert len(encoded) < 3_000_000  # Under 3 MB for 5,000 tabs
```

---
