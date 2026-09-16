# CPSA 4.4 User Guide

The Cryptographic Protocol Shapes Analyzer (CPSA) attempts to enumerate all
essentially different executions possible for a cryptographic protocol. We call
them the shapes of the protocol. Naturally occurring protocols have only
finitely many, indeed very few shapes. Authentication and secrecy properties
are easy to determine from them, as are attacks and anomalies.

For each input problem, the CPSA program is given some initial
behavior, and it discovers what shapes are compatible with
it. Normally, the initial behavior is from the point of view of one
participant. The analysis reveals what the other participants must
have done, given the participant's view. The search is based on a
high-level algorithm that was claimed to be complete, i.e. every shape
can in fact be found in a finite number of steps. Further theoretical
work showed classes of executions that are not found by the algorithm,
however it also showed that every omitted execution requires an
unnatural interpretation of a protocol's roles.  Hence the algorithm
is complete relative to natural role semantics.

The analyzer is designed to work well with other
  tools. S-expressions are used for both input and output. The
  analyzer reads all the problems in its input, writes out the
  solution to each problem, and then exits. This release contains nine
  tools.  The  `cpsa4init`  program
  copies a Makefile and a Haskell script for use
  with  `ghci`  into the current directory.  They orchestrate
  the use of the other tools.
  The  `cpsa4graph`  program
  provides a visualization of answers using Scalable Vector Graphics
  (SVG).
  The  `cpsa4shapes`  program
  removes intermediate results from analyzer runs making the shapes
  easy to identify.
  The  `cpsa4diff`  program compares
  CPSA output files S-expression by S-expression, and prints the first
  skeleton that differs.
  The  `cpsa4sas`  program logical
  formula that can be used to ensure security goals are achieved.
  The  `cpsa4goalsat`  program
  prints skeletons that do not satisfy the goal associated with the
  point of view skeleton.  The
   `cpsa4prot`  program translates
  protocols expressed in Alice and Bob notation into
  CPSA's  `defprotocol`  syntax.
   `cpsa4pp`  program pretty prints its
  input using a CPSA specific algorithm.  It also translates
  S-Expressions into JavaScript Object Notation
  (JSON) to ease processing in other
  languages.  The
   `cpsa4json`  program translates
  JSON encoded CPSA into CPSA
  S-Expressions. The  `cpsa4query` 
  program queries CPSA output as derivation trees.
  The  `cpsa4db` 
  and  `cpsa4dbprolog`  programs
  translate CPSA output into Prolog so it can be analyzed using the
  power and flexibility of Prolog.
  The  `cpsa4dl`  program generates
  Prolog queries written in a dynamic logic.
  Finally,
  the  `cpsa42latex`  program
  translates CPSA macros into equivalent LaTeX macros.

The input syntax is essentially the same as the output syntax. A
  Lisp aware editor will pretty print input, and the output is pretty
  printed. We use Emacs' Scheme mode to prepare input. This document
  describes the syntax, but provides little assistance for its
  interpretation. See the CPSA Primer and
  CPSA Security Goals and Rules for more
  information.

The typical pattern of usage is to enter the set of problems to be analyzed
into a file, in this example,  `prob.scm` , analyze the problems, and if
something interesting is produced, visualize the answers.

   `$ cpsa4 +RTS -M512m -RTS -o prob.txt prob.scm
$ cpsa4graph -o prob.xhtml prob.txt
$ firefox -remote "openFile(`pwd`/prob.xhtml)"` 

Often a summary of the analysis is more enlightening.

   `$ cpsa4shapes -o prob_shapes.txt prob.txt
$ cpsa4graph -o prob_shapes.xhtml prob_shapes.txt
$ firefox -remote "openFile(`pwd`/prob_shapes.xhtml)"` 

 The  `cpsa4init` 
  program creates the
  file  `cpsa4.mk`  for inclusion into
  your makefile. A sample makefile is also created.  The
  file  `cpsa4prolog.pl`  is
  also added to facilitate the analysis of outputs using Prolog.

The CPSA program
  is Emacs friendly.
  If you run the above  `makefile`  via "M-x
  compile", the results will be displayed in a buffer in
  Compilation Mode.  The command "C-x `" will visit
  the locus of the next error message or match ( `next-error` )
  in your CPSA input file.

For platforms without GNU  `make` , the Haskell
 program  `make4.hs`  can be loaded
 into a Haskell interpreter and perform a similar function. Users are
 expected to copy the makefile or the Haskell program into the
 directory containing a set of analysis problems
 using  `cpsa4init` , and then modify
 a file so it specifies the command line flags appropriate for the
 problems in the directory.

## Syntax

The syntax is extensible. Association lists in which the key is always a
symbol are allowed at various points in the grammar. Key-value pairs with
unrecognized keys are ignored, and are available for use by other tools. On
output, unrecognized key-value pairs are preserved when printing protocols, but
elided when printing skeletons, with the exception of the  `comment` 
key.

The input is an option herald form followed by a sequence of
protocol definitions and problem statements.
A herald form allows options normally specified
on the command line to be specified within an input file.  A problem
statement describes the initial behavior as a skeleton or a security
goal.

### Protocols

The grammar for a protocol follows.

   `PROTOCOL   ::= (defprotocol ID ALG ROLE+ RULE* PROT-ALIST)
ID         ::= SYMBOL
ALG        ::= SYMBOL
ROLE       ::= (defrole ID VARS TRACE ROLE-ALIST)
VARS       ::= (vars DECL*)
DECL       ::= (ID+ SORT)
TRACE      ::= (trace EVENT+)
EVENT      ::= (send TERM) | (send ID TERM) | (stor ID TERM)
            |  (recv TERM) | (recv ID TERM) | (load ID TERM)
ROLE-ALIST ::= (non-orig POS-TERM*) ROLE-ALIST
            |  (pen-non-orig POS-TERM*) ROLE-ALIST
            |  (uniq-orig TERM*) ROLE-ALIST
            |  (uniq-gen TERM*) ROLE-ALIST
            |  (conf ID*) ROLE-ALIST
            |  (auth ID*) ROLE-ALIST
            |  (priority POS-INT*) ROLE-ALIST
	    |  (gen-st TERM+) ROLE-ALIST
            |  (critical-sections POS-INT+) ROLE-ALIST
	    |  (facts FACTS*) ROLE-ALIST | ...
POS-TERM   ::= TERM | (INT TERM)
POS-INT    ::= (INT INT)
RULE       ::= (defrule ID SENTENCE RULE-ALIST)
RULE-ALIST ::= ...
PROT-ALIST ::= (lang LDECL*) PROT-ALIST | ...
LDECL      ::= (ID+ KIND)
KIND       ::= atom | akey | hash | (tuple INT)
            |  enc | senc | aenc | sign` 

The syntax for  `SORT` ,  `TERM` ,
  and  `SENTENCE`  will be presented later.

The protocol  `ID`  is a symbol that names the protocol, and the role
 `ID`  is a symbol that names the role. The  `ALG` 
symbol identifies the algebra used by the protocol. For the Basic
Cryptographic Algebra, the symbol is  `basic` .
The  `var`  form contains symbols that declare the sort of
the variables used in this role. The set of sort symbols is algebra
specific, but must include  `mesg` 
and  `chan` .

Events specify message transmission ( `send` ) or
  reception ( `recv` ).  A message can be sent on a channel
  using the form  `(send ID TERM)`  where  `ID`  is
  declared to be of sort  `chan` , and similarly for message
  receptions.  A state value may be received or loaded from a location
  using the form  `(stor ID TERM)`  where  `ID`  is
  declared to be of sort  `locn` .  Every store event
  must be in a group consisting of a number of loads followed by a
  number of stores.  Moreover, each  `locn`  in a store
  event must have had a load event earlier in that group.

The protocol association list has no predefined keys, while the
role association list has nine predefined keys. The value associated
with  `non-orig, pen-non-orig, uniq-orig, uniq-gen, conf, auth`  must
be atoms in the algebra. Each  `non-orig`  term must not be
carried by any event in the role's trace, but each of its variables
must occur in some term.  A role non-origination assumption of the
form  `(3 a)`  asserts that atom  `a`  will not be
mapped into an instance unless its height is greater than three.  For
each  `pen-non-orig`  term, each of its variables must occur
in some term, but unlike a non-origination assumption, the term may be
carried.  Each  `uniq-orig`  term must originate in the
role's trace.  Each  `uniq-gen`  term must generate in the
role's trace.  Each  `conf`  term must be a channel variable,
and it asserts the channel is confidential.  Each  `auth` 
term must be a channel variable, and it asserts the channel is
authenticated.  Each  `gen-st`  must be a term loaded in the
role.  It entails that the instances of these terms are not initial
values, and they must be explained by a previous store event on some
strand.  Each  `critical-section`  designates the start and
end of a group of loads and stores that must occur atomically.  It is
not needed when there is only one load and at most one store in the
group of events.  And it is not needed if the events are not assumed
to occur atomically.  Each  `facts`  declaration ensures
that, whenever an instance of the role proceeds long enough to have
chosen parameter values for each parameter that appears in the facts,
the corresponding instance of the fact will be inferred.  Every
variable of sort  `mesg`  must be acquired by the role's
trace.

The structure of sorts and terms in the Basic Cryptographic Algebra
follows.

   `SORT ::= text | data | name | skey | akey | mesg | chan | locn
TERM ::= ID | AKEY | (ltk ID ID) | STRING
      |  (cat TERM+) | (enc TERM+ TERM) | (hash TERM+)
AKEY ::= ID | (invk AKEY) | (pubk ID) | (privk ID)
      |  (pubk STRING ID) | (privk STRING ID)` 

The form ( `cat`  a b c d e) is expands to
  ( `cat`  a ( `cat`  b ( `cat`  c
  ( `cat`  d e)))).  The form ( `enc`  a b c d e) is
  expands to ( `enc`  ( `cat`  a b c d) e).

A term in the Basic Crypto Algebra is an atom if it is a variable
  of a sort other than  `mesg` , or it if formed from one of
  the following
  operations:  `pubk` ,  `privk` ,  `invk` ,
  and  `ltk` .

The Diffie-Hellman algebra adds three
  sorts:  `rndx` ,  `expt` , and  `base` .
  Variables of sort  `rndx`  are considered atoms.  The new
  terms are  `BASE` :

   `BASE ::= ID | (gen) | (exp BASE EXPT)
EXPT ::= ID | (one) | (mul EXPT EXPT) | (rec EXPT)` 

#### Algebra Signature Extensions

The signature of the message algebra used by CPSA is extensible.
  There are two forms of extensibility provided by CPSA.  Users can add
  operations for encryption, tupling, and hashing; and add sorts for
  atomic data.

A common extension is to add tupling operations to message algebras.
  Previously, complex protocols often made use of tagged concatenation
  to encode a tagged sequence of messages.  In CPSA, concatenation is
  implemented as sequences of pairing operations.  Thus, the expression
  for a certificate body of the form

   `(cat "cert-body" dn serial-no pub-key)` 

is syntax for

   `(cat "cert-body" (cat dn (cat serial-no pub-key)))` 

Algebra extensions are declared using the  `lang`  key in
  the protocol's association list, at the end of a protocol.  For the
  certificate body example,

   `(defprotocol cert basic
  ...
  (lang (cert-body (tuple 3))))` 

adds one tupling operation so that the example above can be written as

   `(cert-body dn serial-no pub-key)` 

CPSA represents this form internally as sequence of messages with a
  distinguished mark.  This representation is more efficient as compared
  with the tagged concatenation representation.

   `LANG  ::= (lang LDECL*)
LDECL ::= (ID+ KIND)
KIND  ::= atom | akey | hash | (tuple INT)
       |  enc | senc | aenc | sign` 

The syntax of a  `lang`  declaration is given above.
There are eight kinds of ways that CPSA algebras can be extended.

* An atomic sort is added to the algebra when a symbol is declared
    to be of kind  `atom` .  If  `dollar`  is
    declared to be an atomic sort, than  `(price dollar)`  in
    a  `var`  form declares  `price`  to be of
    sort  `dollar` .

* An atomic sort is also added to the algebra when a symbol is
    declared to be of kind  `akey` .  However, in addition to
    adding the sort, CPSA adds the equation  `(invk (invk x)) =
    x`  for variables of the new sort.

* A unary operation is added to the algebra when a symbol is
    declared to be of kind  `hash` .  As with the default
    hash operation, the adversary cannot extract the contents of the
    hash.

* An N-ary operation is added to the algebra when a symbol is
    declared to be of kind ( `tuple`  N).  As with
    concatenation, the adversary can construct and extract contents of
    tuples.  N must be positive.

* A binary operation is added to the algebra when a symbol is
    declared to be of kind  `enc` .  As with the default
    encryption operation, the adversary cannot extract contents of the
    encryption without access to the inverse of the key.

* A symbol of kind  `senc`  is just like one of kind
     `enc`  except that the key supplied when it is applied
    must be symmetric.

* A symbol of kind  `aenc`  is just like one of kind
     `enc`  except that the key supplied when it is applied
    must be asymmetric.

* A symbol of kind  `sign`  is just like one of kind
     `enc`  except that the key supplied when it is applied
    must be the inverse applied to an asymmetric key.

### Skeletons

   `SKELETON   ::= (defskeleton ID VARS STRAND+ SKEL-ALIST)
STRAND     ::= (defstrand ID INT MAPLET*) | (deflistener TERM)
MAPLET     ::= (TERM TERM)
SKEL-ALIST ::= (non-orig TERM*) SKEL-ALIST
            |  (pen-non-orig TERM*) SKEL-ALIST
            |  (uniq-orig TERM*) SKEL-ALIST
            |  (uniq-gen TERM*) SKEL-ALIST
            |  (conf ID*) SKEL-ALIST
            |  (auth ID*) SKEL-ALIST
            |  (precedes NODE-PAIR*) SKEL-ALIST
            |  (facts FACTS*) SKEL-ALIST
            |  (priority NODE-INT*) SKEL-ALIST | ...
NODE-PAIR  ::= (NODE NODE)
NODE       ::= (INT INT)
FACT       ::= (ID FTERM*)
FTERM      ::= TERM | INT` 

The  `ID`  in the skeleton form names a protocol. It refers to the last
protocol definition of that name which precedes the skeleton form. The
 `ID`  in the strand form names a role. The integer in the strand form
gives the height of the strand. The sequence of pairs of terms in the strand
form specify an environment used to construct the messages in a strand from its
role's trace. The first term is interpreted using the role's variables and the
second term uses the skeleton's variables. The environment used to produce the
strand's trace is derived by matching the second term using the first term as a
pattern.

The first integer in a node identifies a strand, and the second one
specifies the position of the node in the strand. Zero-based indexing is used.
Zero identifies the first strand, and the first node in a strand has position
zero.

A variable may occur in more then one role within a protocol. The
reader performs a renaming so as to ensure these occurrences do not
overlap.  Furthermore, the maplets used to specify a strand need not
specify how to map every role variable. The reader inserts missing
mappings, and renames every skeleton variable that also occurs in a
role of its protocol. The sort of every skeleton variable that occurs
in the  `non-orig` ,  `pen-non-orig` ,
 `uniq-orig` ,  `uniq-gen` ,  `conf` ,
or  `auth`  list or in a maplet must be declared.

On output, key-value pairs are added to all skeleton's association list.
Every skeleton in the output is labeled with a unique identifier with
 `(label INT)`  A skeleton has  `(parent INT)`  if it is a member of
the cohort of the identified parent. A skeleton has  `(seen INT+)`  when
members of its cohort are isomorphic to previously seen skeletons. A skeleton
lists its unrealized nodes with  `(unrealized NODE*)` . The traces
associated with each strand is given by the  `(traces ...)`  form.
Finally, the operation used to derive this skeleton from its parent is recorded
with  `(operation TEST KIND TERM NODE TERM*)` , where  `TEST`  is the
authentication test  `encryption-test` ,  `nonce` ,
or  `channel-test` ;  `KIND` 
is  `(added-strand ID INT)` ,
 `(displaced INT INT ID INT)` ,
 `(contracted MAPLET*)` ,
 `(added-listener TERM)` ;
 `TERM`  is the critical term;
 `NODE`  in the test node;
and the remaining terms specify the escape set.
When the operation kind is augmenting, the instance's role name and height are
provided.
For kind displacing, the first number is the strand being merged, the
second number is the strand it was merged into, and the remaining give
the new instance's role name and height.
For kind listening, a term is provided. For kind contracting, the
substitution is provided. When a substitution refers to a variable not in the
skeleton, its name is unpredictable. For generalization, the operation is
recorded as  `(operation generalization METHOD)` , where  `METHOD` 
is one of  `deleted NODE` ,  `weakened NODE-PAIR` ,  `separated
TERM`  and  `forgot TERM` . Generalization is used to find shapes from
realized skeletons. For shape collapsing, the operation is recorded as
 `(operation collapsed INT INT)` , where the two  `INT` s identify
the strands merged. Shape collapsing is used to find related shapes.

### First-order Logic and Security Goals

Another way to specify a problem statement is with a security
  goal. A security goal a sentence in first-order logic.  It asserts
  that if some properties hold for a skeleton, then some other
  properties must hold for all shapes computed by CPSA starting with
  the skeleton.  Security goals can be used to formally state
  authentication and secrecy goals of a protocol.

The  `defgoal`  form is used to pose an analysis problem
  with a sentence instead of a skeleton.  CPSA extracts a point of
  view skeleton from the antecedent of the formula and then analyzes
  it.  When a  `defgoal`  form has a sequence of sentences,
  they must all contain the same antecedent.  CPSA will evaluate all
  of the conclusions during the analysis of this shared antecedent.
  When it prints a shape, it checks to see if the shape satisfies the
  conclusions of the security goal sentences.  When invoked with
  the  `goals-sat`  option, CPSA will successfully terminate
  any branch of its analysis as soon as the conclusions of the goals
  are satisfied.  See
  CPSA Security Goals and Rules for
  details.

To be precise, a security goal is an order-sorted first-order logic
  sentence in a restricted form.  The set of sort symbols available
  for use in a  `DECL`  is the ones provided by the message
  algebra augmented with the symbol  `strd` .  The form of a
  sentence is restricted by the syntax that follows.

   `GOAL        ::= (defgoal ID SENTENCE+ GOAL-ALIST)
SENTENCE    ::= (forall (DECL*) (implies ANTECEDENT CONCLUSION))
CONCLUSION  ::= (false) | EXISTENTIAL | (or EXISTENTIAL*)
EXISTENTIAL ::= (exists (DECL*) ANTECEDENT) | ANTECEDENT
ANTECEDENT  ::= ATOMIC | (and ATOMIC+)
ATOMIC      ::= (p ROLEID SVAR HGT) | (p ROLEID PARAM SVAR TERM)
             |  (prec SVAR POS SVAR POS) | (non TERM) | (pnon TERM)
             |  (uniq TERM) | (uniq-at TERM SVAR POS)
             |  (ugen TERM) | (ugen-at TERM SVAR POS)
             |  (conf ID) | (auth ID)
	     |  (gen-st TERM) | (comm-pr SVAR POS SVAR POS)
	     |  (same-locn SVAR POS SVAR POS) | (state-node SVAR POS)
	     |  (trans SVAR POS) | (leads-to SVAR POS SVAR POS)
             |  (fact ID TERM*) | (= TERM TERM)
ROLEID      ::= STRING
HGT         ::= INT
POS         ::= INT | ID
SVAR        ::= ID
PARAM       ::= STRING` 

An atomic formula asserts that a skeleton has some property.  The
  formula  `(p "init" s 3)`  asserts that
  strand  `s`  in the skeleton is an instance of
  an  `init`  role and is of length 3 or greater.  The
  formula  `(p "init" "x" s y)`  asserts that
  strand  `s`  is an instance of an
   `init`  role and is of a length that is great enough so
  that role parameter  `x`  occurs in the role, and the role
  parameter  `x`  is instantiated to become
  term  `y` .  Formula  `(prec (x 2) (y 1))` 
  asserts that for some strands  `x`  and  `y`  in
  the skeleton, the transitive closure of the precedence relation
  contains the mentioned pair of nodes.  Formula  `(non t)` 
  asserts  `t`  is assumed to be non-originating in the
  skeleton.  Predicates  `pnon`  and  `uniq`  have
  similar interpretations. The formula  `(fact foo s (invk
  t))`  asserts the skeleton contains a fact
  called  `foo`  relating a strand to the inverse of some term.
  The formula  `(= s t)`  asserts that  `s` 
  and  `t`  refer to the same object in the skeleton.

The empty string names the listener role of a protocol.  The
  role has the variable  `x`  of sort  `mesg` 
  as its only role variable. There are two positions in the listener
  role.

  `gen-st`  asserts that its argument is a generated state
  value, and cannot be an initial value.   `comm-pr`  asserts
  that the two nodes that follow are a transmission-reception pair
  with the same message.   `same-locn`  asserts that the two
  nodes that follow are state nodes involving the same
  location.   `same-locn`  asserts that the node that follows
  is a state node.   `trans`  asserts that the node that
  follows is a transition node rather than a pure
  observation.   `leads-to`  asserts that the two nodes that
  follow are a transmission and a reception on the same location that
  are immediately related, ie no other transition comes between them.

### Rules

Each protocol may include a small collection of rules.  A rule is
  written using the language of security goals.

A rule is an axiom added to a protocol.  CPSA uses the axiom as a
  rewrite rule to derive zero or more new skeletons from a skeleton
  produced after each analysis step.  A protocol with a rule
  follows.

 `(defprotocol doorsep basic
  (defrole person
    (vars (d p akey) (k skey) (t text))
    (trace
     (send (enc (enc k (invk p)) d))
     (recv (enc t k))
     (send t)))
  (defrole door
    (vars (d p akey) (k skey) (t text))
    (trace
     (recv (enc (enc k (invk p)) d))
     (send (enc t k))
     (recv t)))
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
  (comment "Analyze from the doors's perspective"))` 

The trust rule states that when CPSA finds a person strand of
  length at least one, and the inverse of it's  `p` 
  parameter is non-originating, CPSA should assume the inverse of
  it's  `d`  parameter is non-originating.

### Long-term (cross-session) state

Some protocols manipulate state.  Key management protocols acquire
secrets and certificates, and store them so that subsequent rules can
use them.  Hardware security modules store keys and other data, and
use them in a succession of controlled ways, some of which modifies
the data.  Many other examples arise.

CPSA supports long-term state using two basic event forms,
namely  `(load l term)`  and  `(stor l term)` .
A  `load`  event acquires the piece of state in
location  `l`  of sort  `locn` .  The
term  `term`  in  `(load l term)`  constrains the
value in  `l`  at the time this event occurs.  That value
must have the form of  `term` , and any variables
within  `term`  that are already bound constrain the value
found there.  All remaining variables are newly bound here, and will
constrain the subsequent occurrences.

A  `(stor l term)`  event places the value
of  `term`  into location  `l`  so that
subsequent  `load` s will receive it.  We say that
a  `stor`  event on location  `l`  leads to
a  `load`  event on the same location  `l`  if the
latter happens immediately after; CPSA formalizes this internally by
creating a special value (a "point") that originates uniquely at
each  `stor`  and must match in an immediately
subsequent  `load`  event.  There may be several immediately
subsequent  `load`  events, since several events may observe the
value without causing a transition.  A transition consists of a pair
of adjacent events, one which  `load` s the current value,
followed by another the  `stor` es the subsequent value.
There can be at most one transition to which a
single  `stor`  event leads.

Internally, CPSA regards a location  `l`  of
sort  `locn`  as a kind of channel.  It is a confidential
channel, since the location remains within the device, and the
adversary can obtain the value only via message transmissions.  It is
not a channel with (full) authenticity, since we regard initial values
as always being available.  However, any value that is non-initial
must be generated by a previous transition; i.e. a location offers
authenticity for values known to be non-initial.

We formalize this using a  `gen-st`  predicate in the rule
language.  CPSA uses the formula  `(gen-st term)`  to assert
that  `term`  is definitely non-initial, and requires a
(regular)  `(stor l term)`  event to explain it being
available in location  `l` .  Rules with this kind of
conclusion allow CPSA to infer these formulas when needed.

Within a role definition, a declaration  `(gen-st term-1
... term-i)`  causes CPSA to generate rules that establish that
each of the terms given is  `gen-st`  as long as a role
instance is long enough for the variables in it to be
well-defined.

### Macros and Includes

After reading the input,  `cpsa4`  expands macros before analyzing
the results. A macro definition is a top-level form.

   `(defmacro (NAME ARG*) BODY)` 

The  `cpsa4`  program expands all calls to macros in
non-macro defining S-expressions using the macros that have been
defined previously. A macro definition can be used to expand a call if
the first element of a list matches the name of the macro, and the
length of the remaining elements in the list matches the length of the
macro's argument list. When two macros definitions are applicable, the
last definition takes precedence. The  `cpsa4`  program omits
macro definitions from its output.

After expanding a list, elements of the list of the
  form  `(^`  ... `)`  are spliced into the output.
  Thus  `(a ^(b c) d)`  becomes
   `(a b c d)`  after macro expansion.

A source file can be included within another with the top-level
include form,

   `(include FILE)` 

where  `FILE`  is a string. The  `cpsa4`  program
includes files while it does macro expansion.

### Usage of CPSA

   `$ cpsa4 -h
Usage: cpsa4 [OPTIONS] [FILE]
  -o FILE    --output=FILE      output FILE
  -l INT     --limit=INT        step count limit (default 2000)
  -b INT     --bound=INT        strand count bound (default 12)
  -d INT     --depth=INT        tree depth bound (default unbounded)
  -m INT     --margin=INT       set output margin (default 72)
  -e         --expand           expand macros only; don't analyze
  -n         --noisochk         disable isomorphism checks
  -c         --check-nonces     check nonces first
  -t         --try-old-strands  try old strands first
  -r         --reverse-nodes    try younger nodes first
  -g         --goals-sat        Stop when goals are satisfied
  -a STRING  --algebra=STRING   algebra (default basic)
  -s         --show-algebras    show algebras
  -h         --help             show help message
  -v         --version          show version number` 

This program will abort if too many steps are taken. A skeleton is
printed for each step taken by the program. The step count limit
option is used to override the default step count limit. It will also
abort when it detects a skeleton with too many strands. The strand
count bound option is used to override the default strand count
bound. The tree depth bound option is used to override the default
tree depth bound.  Another way to limit resources used by the program
is to limit the amount of memory it may use. The command-line
option  `+RTS -M512m -RTS`  limits memory usage to 512m.

The herald form can be used to specify options within a file.  The
  grammar for a herald form follows, where  `ALIST`  is an
  association list with symbols as keys.

   `HERALD ::= (herald TITLE ALIST)
TITLE  ::= SYMBOL | STRING` 

The title is used by  `cpsa4graph`  when generating XHTML.
  In the following example, the herald form specifies a strand bound
  of 12 in a way that is equivalent to the command line
  option  `--bound=12` .

   `(herald "Needham-Schroeder Public-Key Protocol" (bound 12))` 

The herald form is only interpreted by the  `cpsa4`  program,
  and is treated as a comment by all other programs.  In particular,
  specifying a  `margin`  option effects  `cpsa4`  only.

For long running problems, SMP parallelism is available. For example, on a
quad-core machine, we would probably use  `+RTS -N4 -RTS` .

In addition to the options provided on the command line or a herald
  form, one can influence the order in which test nodes are sought.
  When a role includes  `(reverse-search)`  in its association
  list as a comment, the nodes in its instances will be searched in
  reverse order.

When run with isomorphism checks disabled ( `--noisochk` ), CPSA
searches for realized skeletons, not shapes. It attempts to speed up analysis
by not identifying duplicate skeletons or generalizing realized skeletons,
however in many cases, run times increase. It is used when normal analysis
takes too much time on the chance that avoiding the checks makes more progress.

In no isomorphism checking mode output, every realized skeleton is labeled a
shape even when it is not. This allows the extraction of every realized
skeletons from the output using the  `cpsa4shapes`  program.

An error message that begins with "No test for unrealized node" identifies a
severe error that should be reported as a bug.

### Search order

In its analysis, CPSA will attempt to solve unrealized nodes until the
skeleton is realized, and then generalize until a shape is obtained.  When
there are multiple unrealized nodes, by default, CPSA will chose the topmost,
rightmost unrealized node among those unrealized nodes with maximum priority.
The default priority of a node is 5, and higher numbers represent a higher
priority.  When a node has non-positive priority, it is left unsolved.

In a role, in order to specify a priority for an event other than
the default, add a comment of the
form  `(priority (i p))` ,
where i is the index of the event in the trace,
and p is the priority.
Priorities are inherited
from roles, but may be overridden in a skeleton with a
 `priority`  comment of the form
 `(priority (n p))` ,
where n is a node.

## Initialization

The  `cpsa4init`  copies the
  files  `Makefile` ,  `cpsa4.mk` ,
  and  `Make4.hs`  into the current directory.  It will not
  overwrite existing files of the same name.  The makefile is for use
  with systems that provide GNU  `make` .  Windows users should
  load  `Make4.hs`  into  `ghci` .  Read the
  comments in the script for usage instructions.

### Usage

   `$ cpsa4init -h
Usage: cpsa4init [OPTIONS]
  -h       --help          show help message
  -v       --version       show version number` 

## Visualization

The  `cpsa4graph`  program produces a graphical rendering of the output
or input of an analyzer using SVG. It is viewable only with a
standards-compliant web browser such as FireFox.

When applied to the output of CPSA, the program groups together all the
skeletons related to each problem statement in the input. The program assembles
the related skeletons into a directed acyclic graph using the parent identifier
and renders it as a tree using SVG. Each vertex in the tree is the label added
to the skeleton by the CPSA program. Click the label in the tree to view the
skeleton. Hover over a node in a skeleton drawing to see the term associated
with it. Hover over a role to see the mapping from role variables to skeleton
variables.

A node ordering edge in a skeleton drawing indicates that the message
transmission at the source of the edge happened before message reception at the
destination edge. The edge is solid if the transmitting term is syntactically
identical to the receiving term, otherwise the edge is dashed. Thus in an
algebra with a commutative operation  `*` , the graphing program sometimes
draws a dashed line between  `(send (* a b))`  and  `(recv (* b
a))` .

In the tree drawing, the label of a shape is blue, and the label of
  a realized skeleton that is not a shape is grey. For dead
skeletons, the label is red, unless it has been seen before, in which
case it is orange. Otherwise the label is green for skeletons seen
before. Seen skeleton labels are rendered in an italic font.

By the default,  `cpsa4graph`  generates a view of CPSA S-expressions as
a compound document that contains SVG within XHTML. This view integrates
graphics with the input text.

In compact mode,  `cpsa4graph`  generates an SVG document. The tree is
displayed immediately to the left of skeleton drawings. When there is more than
one tree, the left-hand-side of the drawing contains a vertical listing of the
trees. Compact mode output should never be used as a replacement for studying
the text version of the output. The text version contains strictly more
information, and should be displayed next to its graphical rendition.

In LaTeX mode,  `cpsa4graph`  generates LaTeX source. XY-pic is used for
drawings of skeletons. The margin specified in  `cpsa4.mk`  produces good results. 

### Usage

   `$ cpsa4graph -h
Usage: cpsa4graph [OPTIONS] [FILE]
  -o FILE  --output=FILE   output FILE
  -x       --expanded      use expanded format (default)
  -z       --zoom          enable diagram scaling
  -t       --treeless      use treeless expanded format
  -c       --compact       use compact format
  -l       --latex         use LaTeX format
  -m INT   --margin=INT    set output margin (default 72)
  -p       --purge-traces  purge traces
  -h       --help          show help message
  -v       --version       show version number` 

## Output Comparisons

The  `cpsa4diff`  program compares CPSA output files
S-expression by S-expression, and prints the first skeleton that
differs.

### Usage

   `$ cpsa4diff -h
Usage: cpsa4diff [OPTIONS] OLD-FILE NEW-FILE
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

## Shape Extraction

The  `cpsa4shapes`  program extracts the original problems and the
shapes from the output of a CPSA run. The shapes are linked to their problem so
the output can be graphed.

### Usage

   `$ cpsa4shapes -h
Usage: cpsa4shapes [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

## Formula Extraction

The  `cpsa4sas`  program extracts a formula in the language
  of order-sorted first-order logic for each problem and its shapes
  from a CPSA run. The formula is called a
  shape analysis
  sentence. The formula is satisfied in all realized skeletons
  when CPSA finds all the shapes for the problem.

### Usage

   `$ cpsa4sas -h
Usage: cpsa4sas [OPTIONS] [FILE]
  -o FILE    --output=FILE     output FILE
  -m INT     --margin=INT      set output margin (default 72)
  -a STRING  --algebra=STRING  algebra (default basic)
  -s         --show-algebras   show algebras
  -h         --help            show help message
  -v         --version         show version number` 

## Goal Satisfaction Checking

The  `cpsa4goalsat`  program prints the labels of
  skeletons that do not satisfy a  `defgoal` .  For each
  point of view skeleton specified by a goal, the program prints a
  list.  The first element of the list is the label of the point of
  view skeleton.  The remaining elements of the list are labels of the
  skeletons that do not satisfy the goal.

### Usage

   `$ cpsa4goalsat -h
Usage: cpsa4goalsat [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

## Alice and Bob notation to CPSA

The  `cpsa4prot`  program translates protocols expressed
  in Alice and Bob notation into CPSA's  `defprotocol` 
  syntax.  It translates  `defprot`  forms, and passes all
  else through unchanged.  The syntax of a  `defprot`  form
  is:

   `PROT       ::= (defprot NAME ALGEBRA (vars DECLS) NOTATION* RULE* PROT-ALIST)
NOTATION   ::= (msg ROLE ROLE CHMSG)
            |  (msg ROLE ROLE CHMSG CHMSG)
            |  (from ROLE CHMSG)
            |  (to ROLE CHMSG)
            |  (clone ROLE ROLE)
            |  (assume ROLE ASSUMPTION*)
CHMSG      ::= (chmsg CHAN TERM) | (chmsg TERM) | TERM
ASSUMPTION ::= (uniq-orig ...) | (non-orig ...) | ...
RULE       ::= (defrule ...)` 

The form  `(msg A B M)`  says role  `A` 
  sends  `M` , and role  `B`  receives
   `M` .  The form  `(msg A B M N)`  says
  role  `A`  sends  `M` , and role  `B` 
  receives  `N` .  The form  `(from A M)`  says
  role  `A`  sends  `M` .  The form  `(to A
  M)`  says role  `A`  receives  `M` .
  The form  `(clone A B)`  says make role  `B`  have
  the same messages as  `A`  up to this point in the
  specification.

### Example

   `$ cat blanchet.prot
(defprot blanchet basic
  (vars (a b akey) (s skey) (d data))
  (msg init resp (enc (enc s (invk a)) b))
  (msg resp init (enc d s))
  (assume init (uniq-orig s))
  (assume resp (uniq-orig d))
  (comment "Blanchet's protocol"))
$ cpsa4prot blanchet.prot
(defprotocol blanchet basic
  (defrole init
    (vars (a b akey) (s skey) (d data))
    (trace (send (enc (enc s (invk a)) b)) (recv (enc d s)))
    (uniq-orig s))
  (defrole resp
    (vars (a b akey) (s skey) (d data))
    (trace (recv (enc (enc s (invk a)) b)) (send (enc d s)))
    (uniq-orig d))
  (comment "Blanchet's protocol"))
$` 

### Usage

   `$ cpsa4prot -h
Usage: cpsa4prot [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -e       --expand       expand macros first
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

## Pretty Printing

The  `cpsa4pp`  program program pretty prints its input
using the CPSA specific algorithm.  It also translates S-Expressions
into JavaScript Object Notation (JSON)
to ease processing in other languages.

### Usage

   `$ cpsa4pp -h
Usage: cpsa4pp [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -j       --json         output uses JSON notation
  -h       --help         show help message
  -v       --version      show version number` 

## CPSA to LaTeX Macro Translation

The  `cpsa42latex`  program translates CPSA macros
  specifying message formats into equivalent LaTeX macros. CPSA
  algebra primitives are mapped to unspecified LaTeX macros with the
  same name and arity (sometimes with an optional tag), allowing the
  user to easily customize how they would like these primitives to be
  typeset. 

### Usage

   `$ cpsa42latex -h
Usage: cpsa42latex [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -h       --help         show help message
  -v       --version      show version number` 

## JSON to S-Expression Translation

The  `cpsa4json`  program translates JSON encoded CPSA into
CPSA S-Expressions.

### Usage

   `$ cpsa4json -h
Usage: cpsa4json [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

## Querying CPSA Output as Derivation Trees

The  `cpsa4query`  program loads CPSA output and a query.
It assembles the skeletons in the output into a forest of derivation
trees.  It then runs the query against the selected trees in the
forest and returns the labels of the skeletons that satisfy the
query.

Each tree vertex is a skeleton represented as a S-Expression.
Information in the skeleton can be accessed by treating it as an
association list.  The query language allows one to ask questions
about the association list, such as if it has a given key.  For
example, you can list the shapes in a tree by asking if the
association list has the symbol "shape" as a key.

### Usage

   `$ cpsa4query -h
Usage: cpsa4query [OPTIONS] QUERY [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

### Description

A query is a file containing S-Expressions.  The first S-Expression
contains the query proper, and the remaining S-Expressions are integers
that select which trees in the forest will be the searched by the
query proper.  If there are no integers, the entire forest is
searched.  The syntax of the query proper is:

   `QUERY ::= (has-key SYMBOL)
       |  (null SYMBOL)
       |  (member SEXPR SYMBOL)
       |  (has-children)
       |  (has-duplicates)
       |  (not QUERY)
       |  (and QUERY*)
       |  (or QUERY*)` 

The  `has-key`  predicate asks if  `SYMBOL`  is a
key in a skeleton.  The  `null`  predicate asks
if  `SYMBOL`  is a key and the value is the empty list.  The
 `member`  predicate asks if  `SEXPR`  is a member
of the value associated with key  `SYMBOL` .
The  `has-children`  predicate asks if the current skeleton
has children.  The  `has-duplicates`  predicate asks if the
current skeleton has duplicates as descendents.  The remaining
operations implement the usual way to combine boolean functions.

### Examples

   `(has-key shape) 0 1` 

finds the skeletons in the first and second tree that have shape as
a key.  If this query is run against the test file output
 `tst/unilateral.txt` , it will find that skeletons 1 and 3
are shapes.

   `(has-key aborted)` 

finds the skeletons in the forest that have aborted as a key.  If
this query is run against the test file output
 `tst/wide-mouth-frog.txt` , it will find that skeleton 18 is
aborted.

   `(and (not (has-children))
     (not (has-duplicates))
     (has-key unrealized))` 

finds the skeletons in the forest that are terminal and unrealized.
If this query is run against the test file output
 `tst/blanchet.txt` , it will produce

   `    2    6    8   16   20   22   30   34   36   42` 

### Transcript

   `$ cat query.txt
(has-key shape) 0 1
$ cpsa4query query.txt tst/unilateral.txt
    1    3` 

## Querying CPSA Output Using Prolog

The  `cpsa4db`  program is used to produce a database of
  facts about the output of CPSA in S-Expression syntax.  The facts
  provide a logical description of a run of CPSA.

The database contains facts about skeletons and facts about how
  skeletons are related to each other in the output.  There are two
  kinds of facts about each skeleton.  The body of a skeleton is
  provided as an association list with the  `skel/2` 
  predicate.  The first argument is the skeleton's label, and the
  second is the association list.  Each skeleton is also described
  using a subset of the goal language, however, the predicate symbol
  used for length predicates is  `l`  to make them easily
  distinguishable from parameter predicates.

The output of CPSA relates skeletons in two ways, by its tree
  structure and its cohort step structure.  Each non-root skeleton has one
  parent.  That information is used to form the tree used to display
  CPSA output.  The  `child/2`  predicate encodes the tree
  structure using skeleton labels.  This predicate is used to visit
  each skeleton once during a search.

A skeleton that is part of a cohort step is either a child of the
  analyzed skeleton or a seen child, meaning it is the child of a
  previously analyzed skeleton.  The  `step/3`  predicate
  specifies the cohort step relation, where its second argument is the
  operation used by CPSA to produce the cohort member from the
  analyzed skeleton.  Thus, the  `step/3`  predicate
  describes a run as a labeled transition system.

For each cohort step not produced by generalization, there is a
  homomorphism from the parent to the cohort member, and when a member
  is produced by generalization, there is a homomorphism from the
  member to the parent.  The homomorphism is available with
  the  `stwa/5`  and  `mtwa/5`  predicates.
  The  `stwa/5`  predicate specifies how strands are mapped,
  and the  `mtwa`  predicate specifies how message variables
  are mapped.  For both of these predicates, the first and forth
  arguments are skeleton labels, and the third argument is the
  operation.

The  `cpsa4dbprolog`  translates a database of facts into
  Prolog syntax so that the database can be queried using all of the
  power and flexibility of Prolog.  To be loadable by Prolog, the
  output must be sorted so that clauses of one predicate are
  colocated.  The sorting program provided in all dialects of Unix
  does the job.

The generated Prolog must be used with a dialect of Prolog in which
  strings are not be atoms, such as SWI Prolog and not GNU Prolog.
  Load the file using  `consult/1` .  Next load your query.
  The file  `cpsa4prolog.pl` 
  contains useful predicates that may help formulate your query.  The
  comments for each predicate are intended help users understand the
  output format.

Most Prolog implementations allow one to use list notation to
  easily consult several files.  If your database is
  called  `db.pl` , and your query is
  called  `query.pl` , you can load all three files with:

   `?- ['db.pl', 'cpsa4prolog.pl', 'query.pl'].` 

### Usage

   `$ cpsa4db [OPTIONS] [FILE]
  -o FILE    --output=FILE     output FILE
  -m INT     --margin=INT      set output margin (default 72)
  -a STRING  --algebra=STRING  algebra (default basic)
  -s         --show-algebras   show algebras
  -h         --help            show help message
  -v         --version         show version number` 

   `$ cpsa4dbprolog [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

## Using Dynamic Logic to Generate Prolog Queries

The  `cpsa4dl`  program translates parts of queries
  written in the dynamic logic into Prolog.  Parts of queries that
  make use of the fact that descendents of a skeleton that are related
  to the ancestor by a homomorphism can be produced automatically by
  specifying those parts in the dynamic language and translating the
  result into Prolog.

Each step in a CPSA output contains some direct children and seen
  children.  When a direct descendent in derived using an
  authentication test, there is a homomorphism from the parent to the
  descendent, that is, all of the structure in the parent is contained
  in the descendent.  When a direct descendent is derived using
  generalization, there is a homomorphism from the descendent to the
  parent.

The dynamic logic implemented provides the usual logical operators
  for specifying properties of a skeleton.  Queries that only use
  them might as well be written directly in Prolog.

What is special about the dynamic logic is it includes the diamond
  and box operators that map formulas about descendents of a skeleton
  using homomorphisms.  For example, if the parent contains the
  message variable  `a` , and it is mapped to the
  message variable  `b`  in the descendent by the homomorphism,
  the generated code knows how to honor the mapping.

A diamond operator applied to a formula is satisfied when the
  formula is satisfied by at least one of the current formula's direct
  descendents.  A box operator applied to a formula is satisfied when
  the formula is satisfied by all of the current formula's direct
  descendents.  When the action associated with a dynamic operator
  is  `plus` , then the operator is applied to all of the
  skeleton's descendents.  The syntax of a dynamic logic query is:

   `QUERY ::= (defquery (SYMBOL DECL*) FORM+)
DECL ::= (SYMBOL SORT)
SORT ::= mesg | strd | node | othr
FORM ::= (SYMBOL TERM*)
      |  (and FORM+)
      |  (or FORM+)
      |  (exists (DECL*) FORM)
      |  (forall (DECL*) FORM)
      |  (diamond ACT FORM)
      |  (box ACT FORM)
TERM ::= SYMBOL | STRING | INTEGER | (INTEGER INTEGER)
ACT  ::= one | plus | star` 

The constant "_" is treated specially and is translated as a Prolog
  anonymous variable.

### Usage

   `$ cpsa4dl [OPTIONS] [FILE]
  -o FILE  --output=FILE  output FILE
  -m INT   --margin=INT   set output margin (default 72)
  -h       --help         show help message
  -v       --version      show version number` 

## S-expressions

The S-expressions used are restricted so that most dialects of Lisp
can read them, and characters within symbols and strings never need
quoting. Every list is proper. An atom is either a symbol, an integer,
or a string. The characters that make up a symbol are the letters, the
digits, and the special characters in
" `+-*/<=>!?:$%_&~^` ". A symbol may not begin with
a digit or a sign followed by a digit. The characters that make up a
string are the printing characters omitting double quote and
backslash, except when double quote and backslash are escaped using
the backslash character. Double quotes delimit a string. A comment
begins with a semicolon, or is an S-expression list at top-level that
starts with the  `comment`  symbol. 

Copyright (c) 2017 The MITRE Corporation. Permission to copy without fee all
or part of this material is granted provided that the copies are not made or
distributed for direct commercial advantage, this copyright notice and the
title of the publication and its date appear, and notice in given that copying
is by permission of The MITRE Corporation.