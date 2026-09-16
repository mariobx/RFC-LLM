[CPSA User Guide]
[CPSA Introductory Slides]
[CPSA Primer]
[CPSA Security Goals and Rules]
[CPSA Manual]
[CPSA Correctness Proof]

# CPSA

The Cryptographic Protocol Shapes Analyzer (CPSA) attempts to
  enumerate all essentially different executions possible for a
  cryptographic protocol. We call them the shapes of the
  protocol. Naturally occurring protocols have only finitely many,
  indeed very few shapes. Authentication and secrecy properties are
  easy to determine from them, as are attacks and anomalies.

CPSA comes with a user guide, a manual, a primer, goal
  documentation, and some slides.  The user guide provides usage
  information for each program in the CPSA package.  The
  manual is the primary documentation.
  Its sources are contained in the manual
  source directory, and a large set of examples discussed in the
  manual are in the examples
  subdirectory.  The primer provides an English language description
  of the CPSA algorithm.

At this point, new users should open the
  introductory slides and start
  using CPSA by analyzing the protocols that come with this document.
  Copy the contents of this directory to a place that allows it to be
  modified.  In a Unix shell, type:

   `$ echo build | ghci Make.hs` 

In Windows, click on  `Make.hs`  and type  `build`  at
  the  `GHCi`  prompt  `*Make>` .
  The CPSA User Guide describes a
  better way to analyze protocols when GNU Make is available.

After running the analysis, you will note files with the extension
   `.xhtml` . These are XHTML/SVG compound documents that can
  be viewed by standards compliant browsers. See the section
  on visualization in the user
  guide for help interpreting these documents.

New users should study CPSA's analysis of the following protocols
  in order, Blanchet ( `blanchet.xhtml` ), Needham-Schroeder
  ( `ns.xhtml` ), Woo-Lam ( `woolam.xhtml` ),
  Yahalom ( `yahalom.xhtml` ), ffgg
  ( `ffgg.xhtml` ), and finally Otway-Rees
  ( `or.xhtml` ). When studying the full output,
  simultaneously display the extracted shapes. The shapes file has an
  extension of  `_shapes.xhtml` .

An analysis of Needham-Schroeder
  using security goals is
  in  `goals.xhtml` .  Examples of using the security goal
  language for rewrite rules is in  `rules.xhtml` .  These
  examples can safely be ignored by new users.

To make effective use of CPSA, new users should scan the
  user guide to get a flavor of its
  contents, and then read the primer.
  The remainder of this document contains some usage tips to be read
  after running CPSA and learning to understand its output.

## Tips

Choose a small, simple protocol for your first analysis task. When
  analyzing complex protocols, analyze small parts of the protocol
  first, and then enrich the description of the problem. 

The source distribution contains additional programs and a test
  suite with many examples.  The README in the top-level directory of
  the source distribution contains the installation instructions and
  is essential reading for its effective use.  Serious users should
  favor the source distribution if on a Unix-like platform.

Authentication tests guide the search for new skeletons in CPSA.
  The authentication test solved at each step of the search is
  described by the  `operation`  form in CPSA output.  When CPSA
  generates unexpected output, find the first skeleton in the
  derivation tree that exhibits the problem and read
  the  `operation`  form to find out what happened.
  Authentication tests are introduced in
  the primer and described in full
  detail in the The CPSA
  Specification.

An origination assumption
  ( `non-orig` ,  `pen-non-orig` ,
  and  `unig-orig` ), can be specified in a role or in a
  skeleton.  Be sure to read the advice in
  the primer on the proper placement of
  origination assumptions.

Variables of sort message unify with any message.  See Otway-Rees
  ( `or.xhtml` ) for an example of the use of variables of this
  sort.

A quoted string is a constant of sort message and is called a tag.
  Tags can be used to distinguish messages that have similar
  structure in the case where the implementation of the protocol
  contains protections against message conflation.

Lisp-like macros in  `cpsa`  input can be used to replace
  multiple occurrences of a message with one named definition of it.
  Macros are described in the primer.

When the  `cpsagraph`  program is given
  the  `--zoom`  option, it produces diagrams that scale.
  This is useful when viewing large diagrams.

In CPSA, a security goal is expressed as a sentence in first-order
  logic.  It asserts that if some properties hold for a skeleton, then
  some other properties must hold for all shapes computed by CPSA
  starting with the skeleton.  Security goals can be used to state
  authentication and secrecy goals of a protocol.  See
  CPSA Security Goals and Rules.  An
  analysis of Needham-Schroeder using first-order logic is
  in  `goals.xhtml` .  Examples of using the security goal
  language for rewrite rules is in  `rules.xhtml` .

When the  `cpsapp`  program is given
  the  `--json`  option, it translates S-expressions into
  JavaScript Object Notation (JSON).  The  `cpsajson` 
  program translates JSON into S-expressions.  These two programs
  makes it easy to manipulate CPSA input and output using Python or
  other languages with JSON libraries.

The goal of CPSA is to automatically characterize the possible
  executions of a protocol compatible with a specified partial
  execution. There is a rigorous
  proof
  that the algorithm enumerates all of these characterizations.

The specification describes the CPSA
  algorithm as a term reduction system.
  The design describes implementation
  choices made and should be read when viewing the source code.