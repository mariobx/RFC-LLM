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
