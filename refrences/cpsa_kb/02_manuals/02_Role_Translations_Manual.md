# CPSA4 Role Translations Manual (`cpsa4roletran`)

*Author: John D. Ramsdell (The MITRE Corporation)*

---

## Table of Contents

- [1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`)](#1-cpsa4-roletran-compiler-user-guide-cpsa4roletran)
  - [1.1 Overview and Natural Role Semantics](#11-overview-and-natural-role-semantics)
  - [1.2 Roletran Input Syntax and Executability Constraints](#12-roletran-input-syntax-and-executability-constraints)
  - [1.3 Annotated Roletran Input Example (`unilateral`)](#13-annotated-roletran-input-example-unilateral)
  - [1.4 Roletran Procedure Output Syntax (`defproc`)](#14-roletran-procedure-output-syntax-defproc)
  - [1.5 Generated Procedure Example (`init` Role)](#15-generated-procedure-example-init-role)
- [2. Role Translations: Formal Semantics and Compilation](#2-role-translations-formal-semantics-and-compilation)
  - [2.1 Introduction and Procedural Role Semantics](#21-introduction-and-procedural-role-semantics)
  - [2.2 Notation](#22-notation)
- [3. Message Algebras for Role Translation](#3-message-algebras-for-role-translation)
  - [3.1 Example Message Algebra (Simple Crypto Algebra)](#31-example-message-algebra-simple-crypto-algebra)
  - [3.2 Encryption-Free Terms and Carried-By Relation](#32-encryption-free-terms-and-carried-by-relation)
- [4. Strand Spaces with Channels](#4-strand-spaces-with-channels)
  - [4.1 Channeled Messages, Traces, and Roles](#41-channeled-messages-traces-and-roles)
  - [4.2 Role Executions and Runs](#42-role-executions-and-runs)
  - [4.3 Unilateral Protocol Example](#43-unilateral-protocol-example)
  - [4.4 Channel Assumptions](#44-channel-assumptions)
- [5. Abstract Execution Semantics](#5-abstract-execution-semantics)
  - [5.1 Runtime Environment, Randomness, and Channel Traces](#51-runtime-environment-randomness-and-channel-traces)
  - [5.2 Abstract Expression and Statement Semantics](#52-abstract-expression-and-statement-semantics)
  - [5.3 Labeled Transition System and Procedure Execution](#53-labeled-transition-system-and-procedure-execution)
  - [5.4 Correctness: Liveness and Safety](#54-correctness-liveness-and-safety)
- [6. Runtime with Probabilistic Encryption (Concrete Message Algebras)](#6-runtime-with-probabilistic-encryption-concrete-message-algebras)
- [7. Concrete Execution Semantics](#7-concrete-execution-semantics)
- [8. Relating Abstract and Concrete Execution Semantics](#8-relating-abstract-and-concrete-execution-semantics)
- [9. Implementation Notes and Epilogue](#9-implementation-notes-and-epilogue)
- [10. References](#10-references)

---

## 1. CPSA4 Roletran Compiler User Guide (`cpsa4roletran`)

### 1.1 Overview and Natural Role Semantics

The Cryptographic Protocol Shapes Analyzer (CPSA) attempts to
enumerate all essentially different executions possible for a
cryptographic protocol.  We call them the shapes of the
protocol. Naturally occurring protocols have only finitely many,
indeed very few shapes.  Authentication and secrecy properties are
easy to determine from them, as are attacks and anomalies.

For each input problem, the CPSA program is given some initial
behavior, and it discovers what shapes are compatible with it.
Normally, the initial behavior is from the point of view of one
participant.  The analysis reveals what the other participants must
have done, given the participant's view.  The search is complete,
i.e. we proved every shape can in fact be found in a finite number of
steps, relative to a procedural semantics of protocol roles.

When we say a role has natural role semantics, we mean that there
exists a program that implements the intent of the specified role.
Until now, establishing the correspondence between a CPSA role and its
implementation has been informal.  It requires a programmer that is
well versed in the semantics of CPSA.  As the messages used in roles
become more complex, the likelihood of errors in the correspondence
increases, even when employing the best programmer/CPSA expert.  The
`cpsa4roletran` compiler automates the translation of a CPSA role into
a language independent procedure.  It uses the same algorithms
implemented in CPSA to ensure a faithful translation.

This document describes the use of the compiler.  It assumes the
reader is experienced with CPSA4, version four of CPSA.  This version
of CPSA is required because channels play an essential part in the
translation.

In typical usage, protocols are analyzed using CPSA4 to ensure they
achieve desired security goals before any attempt is made to construct
programs that implement them.

### 1.2 Roletran Input Syntax and Executability Constraints

`cpsa4roletran` translates an annotated CPSA4 role into a language
independent procedure.  The translator consumes the first protocol
that appears in a CPSA4 input file, and ignores everything else in the
file.  Within the protocol, the translators ignores everything but the
protocol name and the role definitions.

There are two syntactic constraints on roles accepted by `cpsa4roletran`.

 * Every messaging event in the trace of a role must occur on a channel.

 * Every role must include two fields particular to `cpsa4roletran`:
   `inputs` and `outputs`.  The `inputs` specify the terms that become
   the formal parameters of the generated procedure.  The `inputs`
   must include all channel variables that occur in the role's trace.
   The `outputs` contain the terms returned by the generated
   procedure.

The params `field` is an alias for the `inputs` field and the
`returns` field is an alias for the `outputs` field.

The translator ignores all fields in a role definition except its
name, `vars`, `trace`, `uniq-orig`, `inputs`, `params`, `outputs`, and
`returns`.

The translator performs various checks to ensure that each role read
is well formed.  It ensures the each term in the inputs is either a
basic value or a channel.  It ensures that any basic value assumed to
be uniquely originating originates in the role's trace, and that no
uniquely originating value is in the inputs.  It ensures that no input
variable is specified as an output.  It also ensures that every
variable in terms that occur in the inputs, outputs, or are assumed to
be uniquely originating also occur in the role's trace.

Finally, a role must be executable.  A role is *executable* iff

 * each transmitted term can be built from the inputs and previously
   sent and received terms;

 * each received term can be destructured into previously seen basic
   values and hashes; and

 * each output term can be build from the inputs and previously sent
   and received terms.

### 1.3 Annotated Roletran Input Example (`unilateral`)

Here is a protocol that performs unilateral authentication.  Its roles
have been annotated for `cpsa4roletran`.

```scheme
(defprotocol unilateral basic
  (defrole init
    (vars (ch chan) (n text) (k akey))
    (trace
     (send ch (enc n k))
     (recv ch n))
    (uniq-orig n)
    (inputs ch k)
    (outputs n))
  (defrole resp
    (vars (ch chan) (n text) (k akey))
    (trace
     (recv ch (enc n k))
     (send ch n))
    (inputs ch (invk k))
    (outputs n)))
```

The initiator role `init` creates a fresh nonce `n` and sends it on
channel `ch` encrypted with public asymmetric key `k`.  To perform the
encryption, the inputs include the key.  The initiator concludes that
it is communicating with a party that possesses the private companion
key by receiving a nonce unencrypted and ensuring it is what it sent.

The responder role `resp` receives the encrypted nonce, and decrypts
with the private key `(invk k)`.  To do the decryption, the inputs
include that key.  In this example, both roles return the nonce for
use by other parts of the program.

### 1.4 Roletran Procedure Output Syntax (`defproc`)

The compiler generates a language independent procedure for each role
in the input protocol.  A user need not understand the details of the
generated code, but a rough understanding can be helpful when the code
generated is unexpected.  It could mean that the CPSA role specifies
something other that what its author intended.

The structure of a generated procedure is:

```scheme
(comment "Role: NAME (FILE_POSITION)")
(defproc NAME (PARAMS) (OUTPUTS) STMTS)
```

where NAME is the name of the role, FILE_POSITION is the location of
the role's definition in the source file, PARAMS are the input
parameters of the procedure, OUTPUTS is the output types of the
procedure, and STMTS is the statements that make up the body of the
procedure.

There are six kinds of statements.

- `(let (VAR TYPE) EXPR)` binds variable VAR to the results of
  expression EXPR.
- `(let (VAR TYPE) (recv CVAR))` binds variable VAR to the results of
  reading a message on channel CVAR.
- `(send CVAR VAR)` transmits the contents of variable VAR on channel
  CVAR.
- `(same VAR1 VAR2)` ensures the contents of VAR1 agrees with what is
  in VAR2.
- `(return VAR ...)` returns the contents of a sequence of variables
  from the procedure.

Finally, there is a comment statement for each message event that
tells where the event being translated occurs in the source file.

Expressions are self explanatory.  They include pairing, projection,
encryption, decryption, hashing, and nonce generation.  The names of
procedures called in expressions include letters that follow the
underscore character which specify type information.  This part of the
procedure name can be safely ignored.

### 1.5 Generated Procedure Example (`init` Role)

The code generated for the `init` role in the unilateral protocol
follows.  Notice how this code agrees with the description of the
role.

```scheme
(comment "Role: init (rtst/unilateral.scm:6:3)")

(defproc init ((p0 chan) (p1 akey)) (text)
  (comment "Send (rtst/unilateral.scm:9:7)")
  (let (v2 text) (frsh_t))
  (let (v3 aenc) (encr_ta v2 p1))
  (send_m p0 v3)
  (comment "Recv (rtst/unilateral.scm:10:7)")
  (let (v4 text) (recv_t p0))
  (same_t v4 v2)
  (return v2))
```

The initiator role `init` creates a fresh nonce `n` (`v2`) and sends
it on channel `ch` (`p0`) encrypted with public asymmetric key `k`
(`p1`).  To perform the encryption, the inputs include the key.  The
initiator concludes that it is communicating with a party that
possesses the private companion key by receiving a nonce unencrypted
(`v4`) and ensuring it is what it sent `(same_t v4 v2)`.

---

## 2. Role Translations: Formal Semantics and Compilation

### 2.1 Introduction and Procedural Role Semantics

The Cryptographic Protocol Shapes Analyzer (cpsa) [8] attempts to enumerate
all essentially different executions possible for a cryptographic protocol. We call
them the shapes of the protocol. Naturally occurring protocols have only finitely
many, indeed very few shapes. Authentication and secrecy properties are easy
to determine from them, as are attacks and anomalies.
    For each input problem, the cpsa program is given some initial behavior,
and it discovers what shapes are compatible with it. Normally, the initial behavior
 is from the point of view of one participant. The analysis reveals what the
other participants must have done, given the participant’s view. The search is
complete, i.e. we proved every shape can in fact be found in a finite number of
steps, relative to a procedural semantics of protocol roles [7].
When we say a role has procedural semantics, we mean that there exists a
program that implements the intent of the specified role. Until now, establishing
 the correspondence between a cpsa role and its implementation has been
informal. It requires a programmer that is well versed in the semantics of cpsa.
As the messages used in roles become more complex, the likelihood of errors in
the correspondence increases, even when employing the best programmer/cpsa
expert. The Roletran compiler automates the translation of a cpsa role into a
procedure that is easily translated into the source for an existing programming
language, in our case, Rust. It uses the same algorithms implemented in cpsa to
ensure a faithful translation. But how do we know its translations are correct?
    Section 4 presents the abstract semantics of procedures used to guide our
implementation of a runtime system for Roletran generated programs. It includes
a definition of correctness, Definition 8, that precisely defines whether the output
of Roletran correctly implements the role it is given.
    The semantics presented in Sect. 4 has been specified in Coq [1]. An attempt
was made to specify the Roletran compiler as a function in Coq and prove that
every output of Roletran correctly implements the role it is given. However,
the proofs turned out to be too complex and challenging, and the attempt was
abandoned.
    As a fallback, one can present Coq with the runtime semantics, a role, and
procedure, and when the procedure is the output of Roletran, Coq will automatically
 prove it correctly implements the role. The Coq automation succeeds on
protocols of substantial size. Thus for high-assurance applications, we provide a
means to validate compiler input/output pairs in lieu of verifying the compiler
algorithm.
    There is one loose end in what might seem to be a tidy story at this
point. Real implementations of cryptographic functions make use of probabilistic
encryption. This means that there may be several bit patterns that correspond
to one encryption term in cpsa. If the compiler generates code that asserts that
two encryptions are equal, the assertion might fail at runtime if the two encryptions
 differ only because of the randomness used to generate them. To explore
these issues, a more concrete semantics has been defined that models randomness
in encryptions. The paper concludes by showing that
1. the concrete semantics is faithful to the abstract semantics, in that for every
   run of the concrete semantics, there is a corresponding run of the abstract
   semantics, and
2. the concrete semantics is adequate with respect to the abstract semantics,
   in that for every run of the abstract semantics and choice of random values,
   there is a corresponding run of the concrete semantics.
      Therefore, probabilistic encryption is handled correctly.

   The Roletran compiler and supporting Coq proofs were written by the author
and the sources are available on GitHub [8]. The sources contain about 5800 lines
of Coq scripts and the Intro module presents an overview of the work.

    There have been a variety of systems that compile high-level descriptions of
protocols into executable code [2,5]. To our knowledge, this is the first example
of a compiler that uses the input of a cryptographic protocol analyzer as its sole
input and honors its semantics.

### 2.2 Notation

**Notation.** A finite sequence f is a function from an initial segment of the natural
numbers. The length of f is |f |, and f = f (0), . . . , f (n − 1) for n = |f |. The
sequence x::f is x, f (0), . . . , f (n−1). The concatenation of sequences f1 and f2
is f1  f2 .
    If S is a set, then S ∗ is the set of finite sequences over S, and S + is the
                                                                   →
                                                                   −
non-empty finite sequences over S. If S is a finite set, then S is some injective
sequence that is onto S. That is, it is a sequence that contains every element in
S without duplicates.
    Suppose g : X  Y is a finite partial function.
                                             
                                               y    if z = x,
                          g[x → y](z) =
                                               g(z) otherwise.

We use ∅ to denote the finite partial function that has an empty domain.

## 3. Message Algebras for Role Translation

This section describes the formalism on which cpsa message algebras are based.
The parameters to an algebra are:

1. a set of messages Alg. The set of messages Alg is the carrier set (or domain)
   of a term algebra.
2. a set of basic values BV ⊂ Alg. Keys and nonces are examples of basic values.
3. a carried by relation ⊆ Alg × Alg. Intuitively, a message t0 is carried by t1
   if it is possible to extract t0 from t1 by someone who knows the relevant
   decryption keys.

### 3.1 Example Message Algebra (Simple Crypto Algebra)

**Example Message Algebra.** The signature of one possible order-sorted [4] message
algebra is in Fig. 1. The algebra is the simplification of the cpsa message algebra
used by the examples in this paper.
     In an order-sorted algebra, each variable x has a unique sort S. The declaration
 of x is x : S.
     The algebra of interest is the order-sorted quotient term algebra generated by
a set of declarations X. The message algebra AlgX is the carrier set for sort M.
The set of basic values BVX is the union of the carrier sets for sorts A, S, and D.
The carrier set for sort A contains the algebra’s asymmetric key pairs. We write
t : S to say that term t is in the carrier set of sort S.
     A variable has no intrinsic sort associated with it. The declarations that
generate an algebra determine the sort of variables that occur within terms of
the algebra. A variable declared to be of sort M is called a message variable.

**Fig. 1. Simple crypto algebra signature**

```text
                Sorts:      M, A, S, D
                Subsorts: A < M, S < M, D < M
                Operations: (·, ·)          : M × M → M Pairing
                            {| · |}(·) : M × M → M Encryption
                            #               :M→M        Hash
                            (·)−1           :M→M        Key inverse
                            τ0 , τ1 , . . . : M         Tag constants
                Equations: (x−1 )−1 = x for x : A; x−1 = x otherwise
```

    The Simple Crypto Algebra is interesting because like cpsa’s message algebra
, any message can be used as a key when constructing an encryption, with
the exception of a message variable. The reason for the exception is that message
variable x could be unified with any basic value, and so what equation applies
to x−1 ?
    Each element of the message algebra is a set of terms. The canonical representative
 of each element is the term with the fewest number of occurrences of the
                     −1
inverse operation (·) . Thus when x is a variable, the canonical representative
of the algebra element that contains
                                          −1 −1
                                   ((x−1 )   )

is x−1 if x : A, and x otherwise. Message t0 occurs in t1 iff the canonical representative
 of t0 is a subterm of the canonical representative of t1 . In what follows,
we conflate each algebra element with its canonical representative.
### 3.2 Encryption-Free Terms and Carried-By Relation

**Definition 1 (Encryption free terms).** Term t is encryption free, written
enc f ree t, iff no encryption term occurs in t.
    A message t0 is carried by t1 , written t0   t1 , if t0 can be derived from t1
given the right set of keys. That is: is the smallest reflexive, transitive relation
such that
                t0 (t0 , t1 ), t1 (t0 , t1 ),  and t0 {|t0 |}t1 .

## 4. Strand Spaces with Channels

The foundation of this work is a version of strand spaces in which messages are
transmitted over channels. This change facilitates the translation of a role into
code by adding a natural handle for performing input and output in generated
code.
    Recall that a strand space [9] is a finite map from a local session of a protocol,
called a strand, to its behavior, called a trace. The addition of channels changes
the standard definition of a trace, but otherwise leaves the basic definitions of
strand space theory unchanged.

    A channel is a variable of sort C. For h : C and t : M, [h, t] associates message
t with channel h, and is called a channeled message. The additions to a message
signature required to support channels follow.

             Extra Sorts: C, CM
             Operation: [·, ·] : C × M → CM       Channeled messages

The sort associated with a channeled message is CM. The carrier set for that
sort is AlgX . Variables of sort CM are not allowed in X. The carrier set for sort
                 
C is ChnX . Let Alg X = AlgX ∪ ChnX .

### 4.1 Channeled Messages, Traces, and Roles

**Traces and Roles.** The behavior of a strand, its trace, is a finite non-empty
sequence of events. An event is either a channeled message transmission or a
channeled message reception. An event transmitting m ∈ AlgX is written as +m;
and an event receiving channeled message m is written as −m. If e = ±[h, t] is
                                                                       +
an event, then msg(e) = t. The set of traces over AlgX is (±AlgX ) .
    A message t originates in trace c at index i iff c(i) = +[h, t1 ], t t1 , and for
all j < i, t msg(c(j)). A message t uniquely originates in strand space Θ iff
it originates in exactly one trace in Θ. A message t is non-originating in strand
space Θ iff it originates in no trace in Θ.
    Structure rX (c, i, o, u) is a role when
                            +
1. c is a trace in (±AlgX ) ,
2. each variable declared in X occurs in c,
3. i ∈ (BVX ∪ ChnX )∗ is a sequence of basic values and channels that specify
   the inputs to the role,
4. o ∈ Alg∗X is a sequence of terms that specify the outputs of the role, and
5. u ⊆ BVX is a set of basic values that originate in c.
The elements of i and o are a sequence because the order matters when generating
a procedure from the role. Elements of u are freshly generated when the compiled
role executes.

### 4.2 Role Executions and Runs

**Executions.** An execution eY (c, i, o, u) is similar to a role except that its uniquely
originating values are a sequence, not a set. The semantics of an execution
requires that the fresh values be presented in the order in which they are consumed
. Otherwise, the components of an execution must satisfy the same con-
                  
straints. Let φ : Alg     
                      X → AlgY be a homomorphism, and φ̄ be the extension of φ
to traces and sequences of terms in the obvious way.

**Definition 2 (Run of a role).** Execution eY (c , i , o , u ) is a run of role
rX (c, i, o, u) iff there exists a homomorphism φ such that φ̄(c) = c , φ̄(i) = i ,
φ̄(o) = o , φ̄(u) = u , and u is some sequence that contains the elements in u.

   The strand spaces model of a protocol execution is a bundle. A bundle adds
a communication relation to a strand space, and constraints that ensure that
causality is respected in that every received message is transmitted previously

in the bundle. In strand spaces, a Dolev-Yao adversary [3] is modeled by strands
in a bundle along with the strands derived from the protocol being analyzed.
    cpsa does not represent executions using bundles or adversarial behavior
using strands. Instead, it uses a skeleton to represent a collection of bundles. A
skeleton has a strand space, an ordering relation between events, and some origination
 assumptions that must be satisfied by the strand space of the skeleton.
A bundle is modeled by a skeleton if it contains all of the structure specified by
the skeleton, in other words, there is a homomorphism from the skeleton into
the bundle.
    For each input problem, cpsa is given some initial behavior, and it discovers
what shapes are compatible with it. A shape is a special kind of skeleton in that
it contains enough protocol behavior to explain all message receptions in the
presence of adversarial behavior, and it is minimal in that if there is a homomorphism
 from another skeleton to the shape, then there is a homomorphism
from the shape to the other skeleton.
    To describe the executions of a protocol, each strand in a skeleton must be
an instance of some role in the protocol, which is defined to mean there is a
homomorphism from the role to the strand. The definition of a run of a role
codifies that link for procedure execution semantics.

### 4.3 Unilateral Protocol Example

The Unilateral Protocol is a very simple authentication protocol. It consists of
two roles, an initiator and a responder. The initiator encrypts a freshly chosen
nonce using the public key of the responder and sends it. The responder decrypts
the encryption it receives using its private key, and transmits the plaintext. If the
initiator receives the nonce it sent unencrypted, it concludes it is communicating
with a responder that possesses the corresponding private key, assuming the
private key has not been compromised. In the notation presented above, the
protocol is specified as follows.
**Example 3 (Unilateral Protocol)**
             init = rh:C,n:D,k:A (+[h, {|n|}k ], −[h, n], h, k, n, {n})
            resp = rh:C,n:D,k:A (−[h, {|n|}k ], +[h, n], h, k −1 , n, {})
    Both the initiator and the responder use a message algebra generated by
a channel h, a datum n, and an asymmetric key k. The trace of the initiator
contains two events, a channeled message transmission followed by a channeled
message reception. The inputs to the initiator are a channel and the public part
of a key pair. The inputs to the responder are a channel and the private part
of a key pair. The outputs produced by both roles is the single nonce n. The
initiator freshly generates nonce n, and the responder freshly generates nothing.
    cpsa determines that if an instance of an initiator role runs to completion,
and the private part of the key pair is not compromised, i.e. is non-originating,
then there must have been a corresponding run of the responder role that agrees
with the initiator on the values of the nonce and the public key.

### 4.4 Channel Assumptions

With the addition of channels to cpsa, skeletons now include additional kinds of
assumptions besides origination assumptions. A channel can be assumed to be
authenticated and/or confidential. In a bundle, when a channel is authenticated,
the adversary is not allowed to transmit a message on the channel, and when
it is confidential, the adversary is not allowed to received a message on the
channel. The addition of channel assumptions allows interesting new analyses of
protocols, but does not impact Roletran, so it will not be further discussed.

## 5. Abstract Execution Semantics

### 5.1 Runtime Environment, Randomness, and Channel Traces

Roletran generates a procedure for each role in a protocol. To build an executable
program, the procedure is trivially translated into source code for an existing
programming language, in our case Rust. The code is compiled and linked with
a runtime system. The implementer of the program provides a main routine that
invokes the procedure with inputs that must be compatible with inputs of the
translated role. We trust the implementor to do so.
     When the program executes, it goes through state changes associated with
each statement generated by Roletran. The abstract execution semantics specifies
 an abstract view of properties of the states that must be preserved in order
to be in compliance with the execution semantics stated in the previous section.
     When the compiled translation of a role is executing, the runtime system
for the source language maintains a binding between program variables and
binary objects that represent message fragments. The abstract execution semantics
 models these bindings with a map from program variables to terms in the
message algebra. This map is called an environment. The implementor of the
runtime library must ensure that each binary object naturally abstracts into the
corresponding term in the message algebra as specified by the current environment
.
     A runtime system for a program provides two more capabilities, support for
sending and receiving messages on channels, and freshly generating random values
. To model freshly generating random values, the abstract execution semantics
maintains a sequence of basic values that is the source of randomness. Initially
it is the sequence of uniquely originating values in an execution. The implementor
 of the runtime library must ensure each binary object it creates naturally
abstracts into the corresponding term in the message algebra as specified by the
abstract execution semantics.
     To model messaging on channels, the abstract execution semantics maintains
a trace that initially is the trace in the execution. The implementor of the runtime
 library must ensure each binary object transmitted or received naturally
abstracts into the corresponding event over the message algebra as specified by
the abstract execution semantics.

### 5.2 Abstract Expression and Statement Semantics

**Fig. 2. Abstract execution expression semantics**

```text
             ae :       Alg Y environment
                           ∗
                × (±AlgY ) input trace
                      ∗
                × AlgY        input fresh values
                ×E            expression
                × AlgY        value
                           ∗
                × (±AlgY ) output trace
                × Alg∗Y       output fresh values

                  ae(E, c, u, quot(τ ) , τ, c, u)                     (1)

                 E(v1 ) = t1        E(v2 ) = t2
                                                                      (2)
             ae(E, c, u, pair(v1 , v2 ) , (t1 , t2 ), c, u)

                  E(v1 ) = t1       E(v2 ) = t2
                                                                      (3)
             ae(E, c, u, encr(v1 , v2 ) , {|t1 |}t2 , c, u)
                           E(v1 ) = t1
                                                                      (4)
                ae(E, c, u, hash(v1 ) , #t1 , c, u)

                        E(v1 ) = (t1 , t2 )
                                                                      (5)
                  ae(E, c, u, frst(v1 ) , t1 , c, u)
                        E(v1 ) = (t1 , t2 )
                                                                      (6)
                 ae(E, c, u, scnd(v1 ) , t2 , c, u)

        E(v1 ) = {|t1 |}t2 E(v2 ) = t2 −1 enc free t2 −1
                                                                      (7)
               ae(E, c, u, decr(v1 , v2 ) , t1 , c, u)
                            E(v1 ) = h
                                                                      (8)
             ae(E, −[h, t] :: c, u, recv(v1 ) , t, c, u)

                   ae(E, c, t :: u, frsh , t, c, u)                   (9)
```

    The output of the compiler is an executable procedure x(p, s), where p is
a sequence of parameters and s is a sequence of statements. Each parameter
is a program variable and its type, and is associated with an input when the
procedure is invoked. A type is one of M, A, I, S, D, and C.
    The code generated by the compiler is a sequence of statements. Let V be
the syntactic category for program variables. The syntax of a statement is

```text
        S :: = V : T ← E | V ≈ V | invp(V, V) | send(V, V) | return(V ∗ )
        T :: = M | A | I | S | D | C
        E :: = quot(τ ) | pair(V, V) | encr(V, V) | hash(V)
            | frst(V) | scnd(V) | decr(V, V) | recv(V) | frsh
```

**Fig. 3. Abstract execution statement semantics**

```text
                as :      AlgY input environment
                             ∗
                   × (±AlgY ) input trace
                        ∗
                   × AlgY      input fresh values
                   ×S          statement
                   ×      AlgY output environment
                             ∗
                   × (±AlgY ) output trace
                        ∗
                   × AlgY      output fresh values

                ae(E, c1 , u1 , x, t, c2 , u2 ) chk (t, k)
                                                                                     (10)
             as(E, c1 , u1 , v : k ← x , E[v       t], c2 , u2 )

               chk (t, M) always true
               chk (t, A) iff t is a variable of sort A
               chk (t, I) iff t−1 is a variable of sort A
                                                                                     (11)
               chk (t, S) iff t is a variable of sort S
               chk (t, D) iff t is a variable of sort D
               chk (t, C) iff t is a variable of sort C
                   E(v1 ) = E(v2 ) enc free E(v1 )
                                                                                     (12)
                    as(E, c, u, v1 ≈ v2 , E, c, u)

                  E(v1 ) = E(v2 )−1 enc free E(v1 )
                                                                                     (13)
                  as(E, c, u, invp(v1 , v2 ) , E, c, u)
                      E(v1 ) = h E(v2 ) = t
                                                                                     (14)
             as(E, +[h, t] :: c, u, send(v1 , v2 ) , E, c, u)

                            as∗(E, , , , E )                                         (15)

         as(E1 , c1 , u1 , x, E2 , c2 , u2 ) as∗(E2 , c2 , u2 , s, E3 )
                                                                                     (16)
                         as∗(E1 , c1 , u1 , x :: s, E3 )
```

    At runtime, a program variable is associated with an element of a message
algebra. This association is represented by an environment E :V  Alg    Y , a finite
partial function. The semantics of a sequence of statements is specified using the
                                                                                   ∗
relation asret(E, c, u, s, o), where E is an environment, c is a trace in (±AlgY ) ,
u is a sequence of fresh terms in Alg∗Y , s is a sequence of statements, and o is a
sequence of outputs in Alg∗Y .

                 as∗(E, c, u, s, E  ) E  ◦ v0 , v1 , . . . = t0 , t1 , . . .
                                                                                           (17)
                 asret(E, c, u, s return(v0 , v1 , . . .), t0 , t1 , . . .)

The semantics of the remaining statements are given in Fig. 3. The semantics of
expressions are given in Fig. 2. Note that Eq. 7, 12, and 13 make assertions that
some terms must be free of encryptions. the purpose of these restrictions has to do with the correct handling of probabilistic encryption and will be explained in
Sect. 7.
### 5.3 Labeled Transition System and Procedure Execution

The intuition behind the semantics can be gleaned from the statement semantics
 as in Fig. 3. Think of an environment, trace, fresh values triple (E, c, u) as
a state, and a statement as a label. Figure 3 specifies a labeled transition system
. It defines how the states evolve during the course of an execution. For a
sameness test v1 ≈ v2  (Eq. 12), the state does not change. Execution halts
if the test fails. For a send statement send(v1 , v2 ) (Eq. 14), only the trace is
updated. For a bind statement v : k ← x (Eq. 10), all three components of the
state are updated as determined by the expression semantics ae. The trace is
changed only in response to a recv(v1 ) expression (Eq. 8), and a fresh value
is consumed only in response to a frsh expression (Eq. 9). Sequences of state
transitions are tied together in the natural way by as∗ (Eqs. 15 and 16). The
asret predicate (Eq. 17) ensures that the final statement in a procedure is a
return statement, and that the outputs of the procedure are correctly retrieved
from the final environment.
**Definition 4 (Procedure execution).** Let p = (v0 , k0 ), . . . , (vn−1 , kn−1 )
and i = i0 , . . . , in−1 . Execution e = eY (c, i, o, u) is an execution of procedure
x = x(p, s), written exec(x, e), iff
1. for all j < n, chk (ij , kj ), and
2. asret(E, c, u, s, o), where E = ∅[v0 → i0 ] · · · [vn−1 → in−1 ].
See Eq. 11 for the definition of chk .
      Roletran generates the following procedures for the Unilateral Protocol.
**Example 5 (Unilateral Protocol Procedures)**
          initp = x((v0 , C), (v1 , A),      respp = x((v0 , C), (v1 , I),
                    v2 : D ← frsh                        v2 : M ← recv(v0 )
                    v3 : M ← encr(v2 , v1 )              v3 : D ← decr(v2 , v1 )
                    send(v0 , v3 )                       send(v0 , v3 )
                    v4 : D ← recv(v0 )                   return(v3 ))
                    v2 ≈ v4
                    return(v2 ))

   The execution inite = eh:C,n:D,k:A (+[h, {|n|}k ], −[h, n], h, k, n, n) is an
execution of procedure initp. The state transitions caused by this execution of
procedure initp are shown in Fig. 4.

### 5.4 Correctness: Liveness and Safety

**Definition 6 (Liveness).** Procedure x is live for role r, iff there exists an execution
 e such that

1. e is a run of r, and
2. e is an execution of x.

**Definition 7 (Safety).** Procedure x is safe for role r, iff when

1. e is an execution of x, then
2. e is a run of r.

**Definition 8 (Correctness).** Procedure x correctly implements role r, iff x is
live and safe for r.

    The Coq scripts that come with Roletran automatically prove that the Uni-lateral
 Protocol procedures it generates correctly implement their respective
roles.
    Consider the case in which Roletran mistakenly omitted the sameness test
(v2 ≈ v4 ) in the initiator procedure. The Coq scripts would determine that
ec:C,n,n :D,k:A (+[h, {|n|}k ], −[h, n ], h, k, n, n) is an execution of procedure
initp , but note that this execution violates the safety condition. The safety
condition ensures that runs of a collection of procedures that correctly implement
the roles of a protocol achieve the security goals of the protocol.

## 6. Runtime with Probabilistic Encryption (Concrete Message Algebras)

This section presents message algebras, called concrete message algebras, that
are very similar to the ones used by the abstract execution semantics. The only
difference is the way in which they model encryption. The signature used by the
previous algebras has one operation for encryption, {|(·)|}(·) (See Fig. 1), which
suggests that two encryptions are the same if the plaintext and the key used to
construct them are the same. This is not true for implementations of encryption
in actual use. Instead, some randomness is added to an encryption during its
construction in such a way that knowledge of the randomness is not needed to
recover the plaintext by someone in possession of the decryption key.

    Figure 5 shows the signature used for concrete algebras that model probabilistic
 encryption. This signature features a family of encryption operations,
{(·)}i(·) , one for each natural number i. The natural number is meant to represent
 the randomness used while creating the encryption. In concrete algebras,
two encryptions created with the same plaintext and key are equal only if they
were created using the same random value.
    The algebra of interest is the order-sorted quotient term algebra generated by
a set of declarations Y . The message algebra CAlgY is the carrier set for sort M.
The definitions of traces, roles, and executions, extend to concrete algebras in
the obvious ways.

**Definition 9 (Forgetful function).** Let F : CAlgY → AlgY be the obvious
function that forgets the randomness used to create encryptions.

**Lemma 10.** For x ∈ AlgY , if x is encryption free (enc f ree x), then there
exists a unique y ∈ AlgY such that F(y) = x.

Proof. By induction on the structure of y.

      The lemma used in proofs follows.
**Lemma 11.** For x, y ∈ CAlgY , if enc free(F(x)) and F(x) = F(y), then x = y.

## 7. Concrete Execution Semantics

The concrete execution semantics is analogous to the abstract execution semantics
 except that references to message algebras are replaced with references to
concrete message algebras. There is one big exception. When executing an encr
expression, there must be a source of randomness for use in creating an encryption
. To provide a source of fresh basic values, the abstract execution semantics
 threads a sequence of values through state changes. In the concrete execution
 semantics, a sequence of natural numbers γ is also threaded through state
changes and used to create encryptions.

                              E(v1 ) = t1         E(v2 ) = t2
                                                                                 (18)
                   ce(E, c, u, ι :: γ, encr(v1 , v2 ), {t1 }ιt2 , c, u, γ)

                              E(v1 ) = t1        E(v2 ) = t2
                                                                                      (19)
                     ce(E, c, u, , encr(v1 , v2 ), {t1 }0t2 , c, u, )
Equation 19 handles the case in which the source of randomness has been
exhausted.
   Other than the case for the encr expression, the definition of the concrete execution
 semantics follows that of the abstract execution semantics in the obvious
ways.
**Definition 12 (Concrete procedure execution)**
Assume p = (v0 , k0 ), . . . , (vn−1 , kn−1 ) and i = i0 , . . . , in−1 . Execution e =
eY (c , i , o , u ) is a concrete execution of procedure x = x(p, s) with randomness
 γ, written cexec(x, e, γ), iff
1. for all j < n, chk (F(ij ), kj );
2. csret(E, c, u, γ, s, o), where E = ∅[v0 → i0 ] · · · [vn−1 → in−1 ];
3. c is the result of mapping c using F;
4. i = F ◦ i;
5. o = F ◦ o; and
6. u = F ◦ u.

## 8. Relating Abstract and Concrete Execution Semantics

The proofs of the theorems stated in this section were performed using Coq and
the proof scripts are available in the distribution of cpsa [8].
**Theorem 13 (Faithfulness).** cexec(x, e, γ) implies exec(x, e).
    The proof of faithfulness is tedious but straightforward. The forgetful function
 in Definition 9 is used to map items in the concrete semantics to items in
the abstract semantics, and then the proofs go through as expected.
**Theorem 14 (Adequacy).** exec(x, e) implies cexec(x, e, γ).
    The proof of adequacy is tricky. Where there is a sequence of state transitions
in the abstract execution semantics, one must find a corresponding sequence
in the concrete execution semantics. During both sequences, an event in the
trace is consumed when a send statement or a receive expression is encountered.
The case of a receive expression is the easy situation. The received term in the
complex algebra can be any term as long as applying the forgetful function
to it produces the received term in the abstract algebra. However, the case
of a send statement is quite different. The transmitted term in the complex
algebra must agree with what is in the environment associated with the send
statement’s message variable. And the term in the environment depends on the
particular sequence of random values consumed up to this point in the execution.
Engineering a proof that maintains this property is what makes the proof tricky.
    The proof of adequacy makes demands on both the abstract and concrete
execution semantics. The proof depends on the fact that the following terms
must not contain an encryption,

– the key used during a decryption (see Eq. 7),
– the terms compared with a sameness test (see Eq. 12), and
– the terms compared with an inverse key predicate test (see Eq. 13).
The lack of encryptions allow the use of Lemma 11.
   With these checks in place, the means we use to validate compiler
input/output pairs correctly handles probabilistic encryption.

## 9. Implementation Notes and Epilogue

The development of the Roletran compiler is part of a project aimed at addressing
 the fact that there are systems built on aging software components with
questionable security. An approach to protecting such systems is to isolate each
component, and mediate communication between the components using trusted
software that achieves desired security goals. Verified implementations of protocols
 is a key component to our approach. Members of this project include Ian
D. Kretz and Dan J. Dougherty. The project is led by Joshua D. Guttman.
    The project has developed a runtime system in Rust for code generated by
Roletran, and several test protocols have been analyzed and then translated
into running code, the simplest of which is the Unilateral Protocol. The project
has another compiler that compiles protocols that make use of state. Future
work might include the construction of a verified runtime system for Roletran
generated code.
    The addition of channels to cpsa was due to yet another successful collaboration
 between Joshua and the author.

Acknowledgement. Paul D. Rowe provided valuable comments that improved this
paper.

## 10. References
1. The Coq proof assistant reference manual (2021). http://coq.inria.fr
2. Bhargavan, K., Corin, R., Deniélou, P., Fournet, C., Leifer, J.J.: Cryptographic
   protocol synthesis and verification for multiparty sessions. In: Proceedings of the
   22nd IEEE Computer Security Foundations Symposium, CSF 2009, Port Jefferson,
   New York, USA, 8–10 July 2009, pp. 124–140. IEEE Computer Society (2009).
   https://doi.org/10.1109/CSF.2009.26
3. Dolev, D., Yao, A.C.: On the security of public key protocols. IEEE Trans. Inf.
   Theory 29(2), 198–207 (1983). https://doi.org/10.1109/TIT.1983.1056650
4. Goguen, J.A., Meseguer, J.: Order-sorted algebra I: equational deduction for multiple
 inheritance, overloading, exceptions and partial operations. Theor. Comput.
   Sci. 105(2), 217–273 (1992). https://citeseer.ist.psu.edu/goguen92ordersorted.html
5. Guttman, J.D., Herzog, J.C., Ramsdell, J.D., Sniffen, B.T.: Programming cryptographic
 protocols. In: De Nicola, R., Sangiorgi, D. (eds.) TGC 2005. LNCS, vol. 3705,
   pp. 116–145. Springer, Heidelberg (2005). https://doi.org/10.1007/11580850 8
6. Guttman, J.D., Wand, M.: VLISP: a verified implementation of scheme. Lisp Symbolic
 Comput. 8, 5–32 (1995). https://doi.org/10.1007/BF01128406

7. Liskov, M.D., Rowe, P.D., Thayer, F.J.: Completeness of CPSA. Technical
   report, MTR110479, The MITRE Corporation (2011). https://www.mitre.org/
   publications/technical-papers/completeness-of-cpsa
8. Ramsdell, J.D., Guttman, J.D.: CPSA4: A cryptographic protocol shapes analyzer.
   The MITRE Corporation (2018). https://github.com/mitre/cpsaexp
9. Thayer, F.J., Herzog, J.C., Guttman, J.D.: Strand spaces: proving security protocols
 correct. J. Comput. Secur. 7(1), 191–230 (1999). http://content.iospress.com/
   articles/journal-of-computer-security/jcs117
