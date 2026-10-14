# CPSA Protocol Specification Language

         The CPSA Specification:
A Reduction System for Searching for Shapes
        in Cryptographic Protocols

      John D. Ramsdell    Joshua D. Guttman
          Moses D. Liskov    Paul D. Rowe
              The MITRE Corporation
                CPSA Version 4.4.8

                February 27, 2026

    © 2010 The MITRE Corporation. Permission to copy without fee all or part of
this material is granted provided that the copies are not made or distributed for direct
commercial advantage, this copyright notice and the title of the publication and its date
appear, and notice in given that copying is by permission of The MITRE Corporation.



Contents


## 1 Introduction                                                                1

  1.1 Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    2


## 2 Order-Sorted Message Algebras                                               3

  2.1 Channel Messages . . . . . . . . . . . . . . . . . . . . . . . . .      6
  2.2 Locations and state messages . . . . . . . . . . . . . . . . . .        7


## 3 Strand Spaces and Bundles                                                   9



## 4 Adversary Model                                                            13



## 5 Skeletons                                                                  15

  5.1 Blanchet’s Simple Example Protocol . . . . . . . . . . . . . .         17
  5.2 Dolev-Yao Example 1.3 . . . . . . . . . . . . . . . . . . . . . .      20
  5.3 Exercise . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   21
  5.4 External Syntax and Instances . . . . . . . . . . . . . . . . . .      21


## 6 Algorithms as Reduction Systems                                            24



## 7 Primitive Preskeleton Operators                                            26



## 8 Reductions on Preskeletons                                            28

  8.1 Reduction Systems . . . . . . . . . . . . . . . . . . . . . . . . 29


## 9 Penetrator Derivable                                                   31

  9.1 Implementation . . . . . . . . . . . . . . . . . . . . . . . . . . 34


## 10 Carried Only Within                                                       36






## 11 Solving Authentication Tests                                            39

   11.1 Test Solving Steps . . . . . . . . . . . . . . . . . . . . . . . . 41
   11.2 Augmentation . . . . . . . . . . . . . . . . . . . . . . . . . . . 42


## 12 Collapsing and Preconditioning                                         45



## 13 Generalization                                                         46



## 14 Skeleton Reduction System                                              49


A Penetrator Non-Origination Assumptions                                  51

B Programs Specified by a Role                                            52

C Shape Analysis Sentences                                                 55
  C.1 Security Goals . . . . . . . . . . . . . . . . . . . . . . . . . . . 55

D Facts and Rules                                                         59





                                 Abstract

We describe a term reduction system that enumerates all essentially different
executions possible for a cryptographic protocol. We call them the shapes of
the protocol. Naturally occurring protocols have only finitely many, indeed
very few shapes. Authentication and secrecy properties are easy to deter-
mine from them, as are attacks and anomalies. Our Cryptographic Protocols
Shapes Analyzer (cpsa) program is a direct implementation of the reduction
system described within, and the form of the reduction system is partially
determined by the implementation.


## Chapter 1


Introduction

The Cryptographic Protocol Shapes Analyzer (cpsa) attempts to enumerate
all essentially different executions possible for a cryptographic protocol. We
call them the shapes of the protocol. Naturally occurring protocols have only
finitely many, indeed very few shapes. Authentication and secrecy properties
are easy to determine from them, as are attacks and anomalies.
    The shapes analysis is performed within a pure Dolev-Yao model. The
cpsa program reads a sequence of problem descriptions, and prints the steps
it used to solve each problem. For each input problem, cpsa is given some
initial behavior, and it descovers what shapes are compatible with it. Nor-
mally, the initial behavior is from the point of view of one participant. The
analysis reveals what the other participants must have done, given the par-
ticipant’s view.
    This document specifies the cpsa program using a term reduction system.
Chapter 2 describes message algebras as order-sorted quotient term algebras.
Chapter 3 presents an implementation-oriented view of strand spaces. Chap-
ter 4 details the model of the adversary. The formal definition of a partial
run of a protocol is called a skeleton, and is introduced in Chapter 5.
    The term reduction systems used to specify the algorithm is presented
in Chapter 6, and the primitive reduction rules are in Chapter 7. The rules
used to transform terms called preskeletons into skeletons are in Chapter 8.
    The algorithm used to model adversarial behavior is in Chapter 9. The
algorithms used to infer what else must have happened given a partial de-
scription of a run of a protocol as skeleton is in Chapters 10 and 11. Chap-
ters 13 and 12 find most general descriptions of cpsa answers—the shapes.
Finally, Chapter 14 assembles reduction rules into one system that specifies


the cpsa program.
    Appendix A describes an extension to Strand Space theory that models
passwords and related concepts. Appendix B details the sense in which a
protocol role can be viewed as an abstraction of a program. Appendix C
describes a formula in the language of order-sorted first-order logic for each
problem and its shapes found by cpsa. The formula is called a shape analysis
sentence. The formula is modeled by all skeletons that describe full runs of
a protocol when cpsa finds all the shapes for the problem.
    cpsa’s search is based on a high-level algorithm that was claimed to
be complete, i.e. every shape can in fact be found in a finite number of
steps [5, 8]. Further theoretical work [10] showed classes of executions that
are not found by the algorithm, however it also showed that every omitted
execution requires an unnatural interpretation of a protocol’s roles. Hence
the algorithm is complete relative to natural role semantics. See [13, Ap-
pendix B] for more on omitted executions.
    A cpsa release includes two other documents, the cpsa Design [12] and
the cpsa Primer [13]. The design document describes details of the cpsa
implementation that would clutter this one. It should be read by anyone
interesting in reading and modifying the source code. The cpsa Primer
provides an overview of cpsa, and is worth reading before this document is
approached.



### 1.1       Notation

A finite sequence is a function from an initial segment of the natural numbers.
The length of a sequence X is |X|, and sequence X = ⟨X(0), . . . , X(n − 1)⟩
for n = |X|. Alternatively, ⟨x0 , x1 , . . . , xn−1 ⟩ = x0 :: x1 :: . . . :: xn−1 :: ⟨⟩. If S
is a set, then S ∗ is the set of finite sequences of S, and S + is the non-empty
finite sequences of S. The concatenation of sequences X0 and X1 is X0 ⌢ X1 .
The prefix of sequence X of length n is X † n.
    Generally, when discussing terms, a lowercase Latin letter is used to de-
note a term, and an uppercase Latin letter is used to denote a set of terms
or a sequence of terms.






## Chapter 2


Order-Sorted Message Algebras

cpsa models a message by an equivalence class of terms over a signature. A
sort system is used to classify messages. cpsa depends on the sort system
to allow it to treat a variable that represents an asymmetric key differently
from a variable that represents an arbitrary message. In particular, cpsa uses
order-sorted quotient term algebras [6] for message algebras. This formalism
enables the use of well-known algorithms for unification and matching in the
presences of equations and sorts [2].
    This paper makes no attempt to provide a general introduction to order-
sorted quotient term algebras. We use a message algebra called the Basic
Crypto Algebra (bca), which is the main algebra used by cpsa.
    There are six bca sorts: mesg, the sort of all messages, skey, the sort
of symmetric keys, akey, the sort of asymmetric keys, name, the sort of
participant names, and text and data for ordinary values. Sort mesg is
sometimes written as ⊤ and the other sorts are called base sorts. All base
sorts are subsorts of mesg. The function symbols, or operations, used to
form terms are given by the signature in Figure 2.1.
    Each variable x used to form a term has a unique sort s, written x : s.
Variable set X is an indexed set of sets of variables, Xs = {x | x : s}. For
bca, Xmesg , Xskey , Xakey , Xname , Xtext , and Xdata partition the set of
variables in X. By abuse of notation, at times, we write X for the set of
variables in X.
    The Basic Crypto Quotient Term Algebra A generated by variable set X
is displayed in Figure 2.2. The union of the messages in A is set of terms
generated by X, and A partitions the set of terms into a set of equivalence
classes induced by the equations. Terms t0 and t1 are equivalent, written


           Sorts: name, text, data, skey, akey < mesg
             Base sorts: name, text, data, skey, akey
            Carried positions: • denotes a carried position.
       {| • |}(·) : mesg × mesg → mesg      Encryption
       #(·) : mesg → mesg                   Hashing
       (•, •) : mesg × mesg → mesg          Pairing
       “. . . ” : mesg                      Tag constants
       K(·) : name → akey                   Public key of name
       (·)−1 : akey → akey                  Inverse of key
       ltk(·, ·) : name × name → skey       Long term key
                  Equation: (x−1 )−1 ≈ x for x : akey


          Figure 2.1: Basic Crypto Signature and Equation




    Askey = {{x} | x ∈ Xskey } ∪ {{ltk(a, b)} | a ∈ Xname , b ∈ Xname }
    Aakey = {{x−2n | n ∈ N} | x ∈ Xakey }
               ∪ {{x−2n−1 | n ∈ N} | x ∈ Xakey }
               ∪ {{Kx−2n | n ∈ N} | x ∈ Xname }
               ∪ {{Kx−2n−1 | n ∈ N} | x ∈ Xname }
    Aname = {{x} | x ∈ Xname }
     Atext = {{x} | x ∈ Xtext }
    Adata = {{x} | x ∈ Xdata }
        B = Askey ∪ Aakey ∪ Aname ∪ Atext ∪ Adata
       A0 = B ∪ {{x} | x ∈ Xmesg } ∪ {{x} | x is a tag constant }
      n+1
     A     = An ∪ {{(t0 , t1 ) | t0 ∈ T0 , t1 ∈ T1 } | T0 ∈ An , T1 ∈ An }
                ∪ {{{|t0 |}t1 | t0 ∈ T0 , t1 ∈ T1 } | T0 ∈ An , T1 ∈ An }
             S ∪ {{#t     | t ∈ T } | T ∈ An }
A = Amesg = n∈N An

              Figure 2.2: bca Messages A and Atoms B




t0 ≡ t1 , iff t0 ∈ T ∧ t1 ∈ T for some T ∈ A. The canonical representative
of a message is the t in {t′ | t′ ≡ t} with the fewest occurrences of the (·)−1
operation.
    Keys, names, data, and texts in the algebra are called atoms and are
members of B. We write t : B iff {t′ | t′ ≡ t} ∈ B. Note that encryption
is defined with an encryption key of sort mesg. When the encryption key
is of sort akey this is meant to model asymmetric encryption: otherwise,
this models symmetric encryption. Note that even complex messages such
as encryptions can be used as encryption keys in the symmetric sense.
    To find the decryption key associated with an encryption, one must ex-
clude the case in which the key is a variable of sort mesg, as there is no way
to determine if the encryption operation denotes symmetric or asymmetric
encryption. Therefore, the decryption key associated with encryption key t
is inv (t).
                       
                        invk(t)     if t : akey;
             inv (t) =   undefined if t is a variable of sort mesg;
                         t           otherwise.
                       

    An important property possessed by the algebra is that for all T ∈ A, if
there are any encryptions in T then all members of T are encryptions. As
a result, a message can be identified as representing an encryption and if it
is, decomposed into its plaintext and its decryption key. This property is a
consequence of the fact that equations relate atoms, not arbitrary messages.
A similar property holds for pairs and hashes. A hash is treated as a kind of
encryption in which the term that is hashed is the encryption key.
    We write AX when it is important to identify the variable set X that
generates the algebra. Given two variable sets X and Y , a substitution is
an order-sorted map σ : X → AY such that σ(x) ̸= x for only finitely many
elements of X. For a substitution σ, the domain is the set of variables
Dom(σ) = {x | σ(x) ̸= x} and the range is the set Ran(σ) = {σ(x) |
x ∈ Dom(σ)}. Substitution σ0 is more general than σ1 , written σ0 ⊴ σ1 ,
if there exists a substitution σ2 such that ∀x σ1 (x) ≡ σ2 (σ0 (x)). Given a
substitution σ : X → AY , the unique homomorphism σ ∗ : AX → AY induced
by σ is also denoted σ.
    A position p is a finite sequence of natural numbers. The term in t that





occurs at p, written t @ p, is:

                       t @ ⟨⟩ = t;
                       (t0 , t1 ) @ i :: p = ti @ p for i ∈ {0, 1};
                       {|t0 |}t1 @ i :: p = ti @ p for i ∈ {0, 1};
                       t−1 @ 0 :: p = t @ p.

A term t occurs in term t′ if t = t′ @ p for some p. A message T occurs
in message T ′ if the canonical representative of T occurs in the canonical
representative of T ′ .
   A carried term is one that can be extracted from a message reception
assuming plaintext is extractable from encryptions. The positions at which
term t is carried in t′ is carpos(t, t′ ), where

                                {⟨⟩} if t′ ≡ t, else
                             
                             
                             
                                {0 :: p | p ∈ carpos(t, t1 )}
                             
                             
                             
                             
                                        if t′ = {|t0 |}t1 , else
                             
            carpos(t, t′ ) =
                             
                               {i :: p | i ∈ {0, 1}, p ∈ carpos(t, ti )}
                                        if t′ = (t0 , t1 ) else
                             
                             
                             
                             
                                ∅       otherwise.
                             

     Term t carries t′ if carpos(t′ , t) is not empty, and t′ ⊑ t when t′ is car-
ried by t. Note that for all terms t0 , t1 , t′0 , t′1 , if t0 ≡ t1 and t′0 ≡ t′1 , then
carpos(t0 , t′0 ) = carpos(t1 , t′1 ). We write t′ ⊑p t when p ∈ carpos(t′ , t) and
t @ p ≡ t′ .
     In what follows, we will often conflate a term with the message of which
it is a member, and use lowercase letters to denote both.



### 2.1      Channel Messages

As of cpsa version 4.2, messages can optionally be transported on a channel.
For t ∈ AX , a plain message is written [t], and when the message is bound
to channel c, it is written [c, t].
    The channel message algebra adds two sorts to the underlying message
algebra, chan and chmsg, and two operations to the signature:

                  [·] : mesg → chmsg        Plain message
               [·, ·] : chan × mesg → chmsg Channel message



Let X be a bca variable set, and X̄ be a variable set that adds channel
variables to X. If AX is the algebra associated with sort mesg, then ĀX̄ is
the algebra associated with sort chmsg, the Basic Crypto Channel Algebra
generated from X̄.
   Positions are extended to channel messages as follows:

                              m @ ⟨⟩ = m;
                              [t] @ 0 :: p = t @ p;
                              [c, t] @ 1 :: p = t @ p.

The set of carried positions is extended to channel messages in the obvious
way. The plain message [t] will often be written as t when the context
disambiguates the reference.



### 2.2      Locations and state messages

The cpsa 4 treatment of state makes two additions to the message algebra.
First, we introduce a new sort of channel, called locations and written locn.
These are handled exactly like chans in building channel messages:

            [·] : mesg → chmsg                 Plain message
         [·, ·] : (chan ∪ locn) × mesg → chmsg Channel message

We also add a new sort to the underlying message sorts, the sort of points
pval, which are a base sort.
            Sorts: pval, name, text, data, skey, akey < mesg
              Base sorts: pval, name, text, data, skey, akey
We leave the operators and equations unchanged. cpsa protocol specifica-
tions never mention point values explicitly, but the cpsa loader incorporates
them whenever it reads roles that load state values from locations or store
them into locations.
    The state value is a pair (pt, t) consisting of a point pt : pval and the user-
specified message term t; the point occurring when a state value is stored into
a location is always assumed to be uniquely originating. This ensures that
loads that receive the same value (including the point component) are in fact
observing the same state transition event. This allows cpsa to reconstruct
the state histories of different state registers.


    Thus, when m is a message, it may be a plain message [t] or a channel
message [c, t], where either c : chan or c : locn. In case c : locn, cpsa
always arranges that t is a pair of the form t = (pt, t0 ) where pt : pval and
t0 is a point-free term.






## Chapter 3


Strand Spaces and Bundles

When using strand space theory, one normally hypothesizes the existence of
a single global strand space. This is a very reasonable assumption for the-
oretical analysis, but from the point view of an implementer, it turns out
that it is better to assume there are many local strand spaces and the de-
sign specification task is to describe the relations between these local spaces.
Our reformulation of strand space notation provides an implementation ori-
ented way of describing the concept of a local strand space, and a direct
link between from algorithm specification to the data structures used in the
implementation.
    A run of a protocol is viewed as an exchange of messages by a finite set
of local sessions of the protocol. Each local session is called a strand. The
behavior of a strand, its trace, is a sequence of messaging events. An event
is either a message transmission or a reception.
    An outbound message m ∈ ĀX is written as +m, and a message m is
written as −m.

State events: Stores and loads. When m = [c, (pt, t0 )] for c : locn and
pt : pval, +m is a store event, in which the value t0 is written into the
location c, and −m is a load event, in which the value t0 is read out of the
location c. In the latter case, pt may be the point associated with an earlier
store event e that wrote t0 into c. In this case, our theory will ensure that e
is the most recent store event involving c.

Traces and strand spaces. The set of traces over ĀX is CX = (±ĀX )+ .
A message originates in a trace if it is carried by some event and the first


event in which it is carried is outbound. A message is gained by a trace if it
is carried by some event and the first event in which it is carried is inbound.
A message is acquired by a trace if it first occurs in a reception event and is
also carried by that event.
    Abstractly, a strand space is a multiset of traces, but since we wish to
name each element, a strand space ΘX over algebra ĀX is defined to be a
sequence of traces in CX . A strand s is a member of the domain of ΘX , and
its trace is ΘX (s).
    Message events occur at nodes in a strand space. For each strand s, there
is a node for every event in Θ(s). The nodes of strand space Θ are {(s, i) |
s ∈ Dom(Θ), 0 ≤ i < |Θ(s)|}, the event at a node is evt Θ (s, i) = Θ(s)(i),
and the message at a node is msg Θ (s, i) = m such that evt Θ (s, i) = ±m.
Just as a position names a subterm within another term, a strand names a
trace within a strand space, and a node names an event in a strand space.
The relation ⇒ defined by {(s, i − 1) ⇒ (s, i) | s ∈ Dom(Θ), 1 ≤ i < |Θ(s)|}
is called the strand succession relation.
    A bundle in strand space Θ is a finite directed acyclic graph Υ(Θ, →),
where the vertices are the nodes of Θ, and an edge represents communica-
tion (→) or strand succession (⇒). For communication, if n0 → n1 , then
there is a channel message m such that evt Θ (n0 ) = +m and evt Θ (n1 ) = −m.
For each reception node n1 , there is a unique transmission node n0 with
n0 → n1 .
    Each acyclic graph has a transitive irreflexive relation ≺ on its vertices.
The relation specifies the causal ordering of nodes in a bundle. An transitive
irreflexive binary relation is also called a strict partial order.

Authentic and confidential channels. An atom uniquely originates in
a bundle if it originates in the trace of exactly one strand. An atom is non-
originating in a bundle if it originates on no strand, but each of its variables
occurs in some strand’s trace. A channel is authenticated if only regular
strands in a bundle use it to transmit messages. A channel is confidential if
only regular strands in a bundle use it to receive messages.

Channel properties of locations. Every location is regarded as a con-
fidential channel. Thus, we are modeling long term state registers that are
associated with devices under the control of regular (i.e. compliant) par-
ticipants. The adversary never observes a location directly; the adversary



observes only messages from regular participants that may reflect the con-
tents of locations. The adversary may store certain values directly, namely
the possible initial values for a location. Thus, we rely on the adversary
to initialize locations values. Other values that can be produced only by a
state transition cannot be inserted by the adversary; only a regular partic-
ipant’s store event can cause them. The protocol specification determines
the sufficient conditions for these non-initial values, or, as we will call them,
generated state values. Naturally, messages the adversary delivers to regular
participants may affect what generated state values they subsequently store.

Roles. In a run of a protocol, the behavior of each strand is constrained by
a role in a protocol. Adversarial strands are constrained by roles as are non-
adversarial strands. What follows is the definition of a role before channels
and channel messages were introduced into cpsa, followed by a discussion of
the additions caused by channels.
    Given an ĀY , and C ∈ CY , N ⊆ BY , and U ⊆ BY , if:
  1. t ∈ N implies t is not carried in C, and all variables in N occur in C;
  2. t ∈ U implies t originates in C;
  3. if variable x occurs in C then x is an atom or it is acquired in C; and
  4. the trace of a role may not match the pattern ⟨−m, +m, . . .⟩,
then rY (C, N, U ) is a role over ĀY . The trace of rY (C, N, U ) is C, its non-
origination assumptions are N , and its unique origination assumptions are U .
Item (4) is meant to ensure that listeners, which are introduced on Page 17,
cannot be confused with protocol constrained strands.
     A protocol P is a set of roles. Let Vars(P ) be the set of variables that
occur in the traces of the roles in protocol P .
     A bundle Υ(ΘX , →) is a run of protocol P if there is a role mapping
rl : ΘX → P that satisfies properties for each s ∈ Dom(ΘX ). Assuming
rl (s) = rY (C, N, U ) and X and Y share no variables, and let h = |ΘX (s)|, the
properties are (1) h ≤ |C|, (2) there is a homomorphism σ : ĀY → ĀX such
that σ ◦ C † h = ΘX (s), (3) Dom(σ) is the set of variables that occur in C † h,
(4) if the variables in t ∈ N occur in Dom(σ), then σ(t) is non-originating in
Υ(ΘX , →), and (5) if t ∈ U originates at index i in C, and i < h, then σ(t)
uniquely originates in Υ(ΘX , →) at node (s, i). Origination assumptions in
bundles specified by roles are called inherited origination assumptions.


Roles and channels. The introduction of channels adds two new fields to
a role, a set of channels assumed to be authenticated, and a set of channels
assumed to be confidential. For a bundle to be a run of a protocol, the
inherited channel assumptions must be honored by the bundle. State adds
no other fields to the role data structure, although when c : locn, c will
always be among the confidential channels.






## Chapter 4


Adversary Model

A fixed set of penetrator roles encodes the adversary model associated with
a message algebra. For the Basic Crypto Algebra, there are nine roles. Each
role makes no origination assumptions, and the trace of each role is given
in Figure 4.1. The first line of the figure specifies many traces, one for each
base sort, and a trace for each tag.
    A strand exhibits non-adversarial behavior when its role is not a pen-
etrator role. A non-adversarial strand is called a regular strand as is its
role.
    The penetrator cannot use a non-originating atom to encrypt or decrypt a
message, because every key it uses must be carried in a message. Consider a
uniquely originating atom that originates on a regular strand. The penetrator
cannot make the atom using a create role, because the atom would originate
in more than one trace. Therefore, the penetrator can use a uniquely orig-
inating atom to encrypt or decrypt a message only if it is transmitted by a
regular strand unprotected by encryption.
    When a channel is authenticated, the penetrator cannot send a message

       Create(z : B)         ⟨+z⟩                 ⟨+“. . . ”⟩
       Pair(x, y : ⊤)        ⟨−x, −y, +(x, y)⟩    ⟨−(x, y), +x, +y⟩
       Encrypt(x, y : ⊤)     ⟨−x, −y, +{|x|}y ⟩   ⟨−{|x|}y , − inv (y), +x⟩
       Hash(x : ⊤)           ⟨−x, +#x⟩
       Chan(c : Ch, x : ⊤)   ⟨−x, +[c, x]⟩        ⟨−[c, x], +x⟩

         Figure 4.1: Basic Crypto Algebra Penetrator Role Traces



on it. When a channel is confidential, the penetrator cannot receive a message
on it.






## Chapter 5


Skeletons

The details of penetrator behavior are abstracted away when performing
protocol analysis. The abstracted description of a bundle is called a realized
skeleton, which is defined using a protoskeleton. A protoskeleton over ĀX is
kX (rl , P, ΘX , ≺, N, U ), where rl : Dom(ΘX ) → P is a role map, the sets X
and Vars(P ) are disjoint, ΘX is a sequence of traces in CX , ≺ is a relation on
the nodes in ΘX , N ⊆ BX are its non-origination assumptions, and U ⊆ BX
are its unique origination assumptions. Unlike a strand space, the sort of a
variable in X need not be a base sort.
    The introduction of channels adds two new fields to a skeleton, a set of
channels assumed to be authenticated, and a set of channels assumed to be
confidential. The implications of the additions is straightforward, and we
simply retain the original description of skeletons.
    Assume the strands in bundle Υ(ΘX , →) have been permuted so that
regular strands precede penetrator strands in sequence ΘX , and rl demon-
strates the bundle is a run of protocol P . Let P ′ be P without penetrator
roles. Skeleton kX (rl ′ , P ′ , Θ′X , ≺, N, U ) realizes the bundle if rl ′ and Θ′X are
the truncations of rl and ΘX respectively that omit penetrator strands from
their domains, ≺ is the transitive irreflexive relation associated with the
bundle without penetrator nodes, N is the set of non-originating atoms with
variables that occur in Θ′X , and U is the set of atoms that uniquely originate
and are carried by some regular event.
    A protoskeleton kX (rl , P, ΘX , ≺, N, U ) is a preskeleton if the following
properties hold.
   1. Sequence rl demonstrates that the strands in Dom(ΘX ) satisfy the
      conditions for being a part of a run of protocol P .


   2. Relation ≺ is transitive, irreflexive, and includes the strand succession
      relation (⇒).

   3. If n ≺ n′ , then either n ⇒ n′ , evt ΘX (n) = +t and evt ΘX (n′ ) = −t′ , or
      n ≺ n′′ ≺ n′ for some n′′ .

   4. Each atom in N is carried by no event, and each variable in the atom
      occurs in some event.

   5. Each atom in U is carried by some event.

   6. N includes the non-originating atoms inherited from roles via the role
      map.

   7. U includes the uniquely originating atoms inherited from roles via the
      role map.

    Let Ok (t) be the set of nodes at which t originates in preskeleton k,
and Gk (t) be the set of nodes at which t is gained in k. Preskeleton
kX (rl , P, ΘX , ≺, N, U ) is a skeleton if each atom in U originates on at most
one strand, and the node of origination precedes each node that gains the
atom, i.e. for every t ∈ U , n0 ∈ Ok (t) and n1 ∈ Gk (t) implies n0 ≺ n1 .
    Let k0 = kX (rl0 , P, Θ0 , ≺0 , N0 , U0 ) and k1 = kY (rl1 , P, Θ1 , ≺1 , N1 , U1 ) be
preskeletons. There is a preskeleton homomorphism from k0 to k1 if ϕ and σ
are maps with the following properties:

   1. ϕ maps strands of k0 into those of k1 , and nodes as ϕ((s, i)) = (ϕ(s), i),
      that is ϕ is in Dom(Θ0 ) → Dom(Θ1 );

   2. σ : ĀX → ĀY is a message algebra homomorphism;

   3. n ∈ nodes(Θ0 ) implies σ(evt Θ0 (n)) = evt Θ1 (ϕ(n));

   4. n0 ≺0 n1 implies ϕ(n0 ) ≺1 ϕ(n1 );

   5. σ(N0 ) ⊆ N1 ;

   6. σ(U0 ) ⊆ U1 ;

   7. t ∈ U0 implies ϕ(Ok0 (t)) ⊆ Ok1 (σ(t)).




    A homomorphism is strandwise injective if its strand map is injective.
Two preskeletons are isomorphic if they are related by strandwise injective
homomorphism in both directions. A homomorphism is nodewise isomorphic
if the strand map ϕ implies a bijection on nodes, and n0 ≺1 n1 implies
ϕ−1 (n0 ) ≺0 ϕ−1 (n1 ). A skeleton is realized if there is a nodewise isomorphic
homomorphism from it to a skeleton that realizes a bundle, and message
component of the homomorphism is injective.
    Our formalism requires that every protocol include a listener role of the
form: lsn(x : ⊤) = r(⟨−x, +x⟩, ∅, ∅). Instances of this role are sometimes used
to make penetrator derived messages visible in skeletons. We say skeleton k
realizes modulo listeners bundle Υ(Θ, →) if k realizes Υ(Θ′ , →′ ) and Υ(Θ, →)
is the result of removing listener strands, and adjusting the communication
ordering → appropriately.
    The set of bundles denoted by preskeleton k, [[k]], is:
                          ϕ,σ
           [[k]] = {Υ | k 7−→ k ′ and k ′ realizes modulo listeners Υ}
A cpsa algorithm is complete if when given a preskeleton k, either the al-
gorithm diverges, or else it terminates       and produces a finite set of realized
skeletons K, such that [[k]] = k′ ∈K [[k ′ ]].
                              S



5.1      Blanchet’s Simple Example Protocol
The following protocol is a simplified version of the Denning-Sacco key dis-
tribution protocol [4] due to Bruno Blanchet.
                                A → B : {|{|s|}a−1 |}b
                                B → A : {|d|}s
Symmetric key s is freshly generated, asymmetric keys a−1 and b−1 are un-
compromised, and the goal of the protocol is to keep data d secret. The
protocol was constructed with a known flaw for expository purposes.
    This cpsa description of the protocol has an initiator and a responder
role.
           init(a, b : A, s : S, d : D) = r(⟨+{|{|s|}a−1 |}b , −{|d|}s ⟩, ∅, ∅)
          resp(a, b : A, s : S, d : D) = r(⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩, ∅, ∅)
where we use A for sort akey, S for sort skey, and D for sort data to
save space. The algebra for the initiator role is generated from X, where
XA = {a, b}, XS = {s}, XD = {d}, Xtext = ∅, Xname = ∅, and X⊤ = ∅.


    An interesting point of view for analysis is to see if the authentication
goals of the initiator are met. To do so, we assume there was full length run
of an initiator strand, and let cpsa determine what else must have happened.
Let variable set Y = a, b : A, s : S, d : D. The point-of-view skeleton is:
       kY (⟨init(a0 , b0 , s0 , d0 )⟩,                             Role map
           {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )},   Protocol
           ⟨⟨+{|{|s|}a−1 |}b , −{|d|}s ⟩⟩,                         Traces
           ∅,                                                      Node orderings
           {a−1 , b−1 },                                           Non-origination
           {s})                                                    Unique origination
where the variable set that generates the algebra for the initiator and respon-
der roles have been renamed so as to avoid conflicts with the variable set Y
used by the skeleton.
    The skeleton produced by cpsa for this problem follows. Notice that the
two strands agree on the key b used in the outermost encryption of their
first message, and indication that the authentication goals of the initiator
are met. See Figure 5.1 to see the structure of the shape.
       kY (⟨init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )⟩,   Role map
           {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )},   Protocol
           ⟨⟨+{|{|s|}a−1 |}b , −{|d|}s ⟩,                          Traces
            ⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩⟩,
           {(0, 0) ≺ (1, 0), (1, 1) ≺ (0, 1)},                     Node orderings
           {a−1 , b−1 },                                           Non-origination
           {s})                                                    Unique origination
The homomorphism from the point-of-view skeleton to the shape is
                         (⟨1⟩, {a 7→ a, b 7→ b, s 7→ s, d 7→ d}).
    An analysis of the authentication goals for the responder shows the flaw
built into the protocol. To do the analysis, assume there was a full length run
of a responder strand, and let cpsa determine what else must have happened.
In this case, the point-of-view skeleton is:
       kY (⟨resp(a0 , b0 , s0 , d0 )⟩,                             Role map
           {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )},   Protocol
           ⟨⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩⟩,                         Traces
           ∅,                                                      Node orderings
           {a−1 , b−1 },                                           Non-origination
           {s})                                                    Unique origination


                            init        resp          resp         init


                             •            /•            •o             •

                                                       
                             •o           •             •

                     Figure 5.1: Shapes for Blanchet’s Protocol

    The shape generated by cpsa follows. An early indication of a problem
is the variable set for the shape has three asymmetric keys. Let variable set
Z = a, b, b′ : A, s : S, d : D. The shape is:

      kZ (⟨resp(a0 , b0 , s0 , d0 ), init(a1 , b1 , s1 , d1 )⟩,   Role map
          {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 )},   Protocol
          ⟨⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩,                          Traces
           ⟨+{|{|s|}a−1 |}b′ ⟩⟩,                                  Note key is b′ not b!
          {(1, 0) ≺ (0, 0)},                                      Node orderings
          {a−1 , b−1 },                                           Non-origination
          {s})                                                    Unique origination

   Notice that the two strands do not agree on the key used in the outermost
encryption of their first message—an authentication failure. To see that the
authentication failure leads to the failure to protect the secrecy of data d,
the protocol is analyzed using the following point-of-view:

   kY (⟨resp(a0 , b0 , s0 , d0 ), lsn(x)⟩,                                 Role map
       {init(a0 , b0 , s0 , d0 ), resp(a1 , b1 , s1 , d1 ), lsn(x)},       Protocol
       ⟨⟨−{|{|s|}a−1 |}b , +{|d|}s ⟩, ⟨−d, +d⟩⟩,                           Traces
       {(0, 1) ≺ (1, 0)},                                                  Node orderings
       {a−1 , b−1 },                                                       Non-origination
       {s, d})                                                             Unique origination

   cpsa finds a shape that shows how data d is revealed to the adversary.





5.2      Dolev-Yao Example 1.3
The intended run of the protocol in the Dolev-Yao Example 1.3 is:
                                  A → B : {|{|m|}b , a|}b
                                  B → A : {|{|m|}a , b|}a

assuming text m is freshly generated, and asymmetric keys a−1 and b−1 are
uncompromised.
    The cpsa description of the protocol also has an initiator and a responder
role.
          init(a, b : A, m : D) = r(⟨+{|{|m|}b , a|}b , −{|{|m|}a , b|}a ⟩, ∅, ∅)
         resp(a, b : A, m : ⊤) = r(⟨−{|{|m|}b , a|}b , +{|{|m|}a , b|}a ⟩, ∅, ∅)

    An interesting point of view for analysis is to see if m is kept secret after
the initiator sends its message. Let variable set Z = a, b : A, m : D. The
initial scenario preskeleton is:
      kZ (⟨init(a0 , b0 , m0 ), lsn(x)⟩,                            Role map
          {init(a0 , b0 , m0 ), resp(a1 , b1 , m1 ), lsn(x)},       Protocol
          ⟨⟨+{|{|m|}b , a|}b ⟩, ⟨−m⟩⟩,                              Traces
          ∅,                                                        Node orderings
          {a−1 , b−1 },                                             Non-origination
          {m})                                                      Unique origination

where the variable set that generates the algebra for the initiator role has
been renamed so as to avoid conflicts with the variable set Z used by the
preskeleton.
   cpsa determines m is not kept secret by producing the shape in Fig-
ure 5.2. The added strands in the shape are instances of responder roles.
The strands in the shape are:
                  ⟨+{|{|m|}b , a|}b ⟩
                  ⟨−m⟩
                  ⟨−{|{|m|}b , a′ |}b , +{|{|m|}a′ , b|}a′ ⟩
                  ⟨−{|{|{|m|}b , a|}b , a′′ |}b , +{|{|{|m|}b , a|}a′′ , b|}a′′ ⟩

The non-origination and unique origination assumptions are as they are in
the initial scenario preskeleton. An interesting exercise left for the reader is
to produce a bundle that is realized by the shape.


                        init               resp        resp


                          •                             /•


                                                         
                                              •o         •

                                              
                                   •o         •

                                    
                                   •

                  Figure 5.2: Dolev-Yao Example 1.3 Shape


### 5.3      Exercise

Consider the following roles.

                     init(a, b : A) = r(⟨+(a, b), −(b, a)⟩, ∅, ∅)
                    resp(a, b : A) = r(⟨−(a, b), +(b, a)⟩, ∅, ∅)

Let X = x, y : A and k = kX (⟨init(a, b), resp(a, b), resp(a, b)⟩,
                             {init(a, b), resp(a, b)},
                             ⟨⟨+(x, y), −(y, x)⟩,
                              ⟨−(x, y), +(y, x)⟩,
                              ⟨−(x, y), +(y, x)⟩⟩,
                             Node ordering in Figure 5.3,
                             ∅,
                             ∅)
   What is [[k]]?
   One member is shown in Figure 5.4.



### 5.4      External Syntax and Instances

The external syntax used by cpsa is a little different than what has been
described here. In the external syntax, the trace and the role associated
with a strand is specified by an instance. An instance is of the form i(r, h, σ),


                init       resp      resp


                  •        /•         ,•


                                      
                  • lo      •          •

              Figure 5.3: Exercise Skeleton




       init   ⟨+(x, y), −(y, x)⟩
       resp   ⟨−(x, y), +(y, x)⟩
       resp   ⟨−(x, y), +(y, x)⟩
       pair   ⟨−(y, x), −(y, x), +((y, x), (y, x))⟩
       sep    ⟨−((y, x), (y, x)), +(y, x)⟩

      init      resp       resp       pair      sep


       •         /•         ,•


                               
                  •         •          /•


                                       - •


                                            
                                        •        /•


                                                 
       •o                                         •

Figure 5.4: A Bundle Realized by the Example Skeleton




where r is a role, h specifies the length of a trace instantiated from the role,
and σ specifies how to instantiate the variables in the role to obtain the trace.
Thus when r = rY (C, N, U ), the trace associated with i(r, h, σ) is σ ◦ C † h.
An instance is well-formed if 1 ≤ h ≤ |C|, and Dom(σ) is the set of variables
that occur in C † h.
     In the external syntax, the role map and sequence of traces are replaced
by a sequence of instances. So for preskeleton kX (rl , P, ΘX , ≺, N, U ), the
external syntax is kX (P, I, ≺, N, U ), where for each s ∈ Dom(Θx ), I(s) =
i(r, h, σ), r = rl (s), and the trace of i(r, h, σ) is ΘX (s).






## Chapter 6


Algorithms as Reduction
Systems

Algorithms in this paper are specified as abstract reduction systems [1, Chap-
ter 2]. A reduction system is a pair (A, →), where reduction → is a binary
relation → ⊆ A × A. Element x ∈ A is a normal form if there is no y such
that x → y. The transitive closure of → is →+ . The reflexive transitive
closure of → is →∗ . A reduction is confluent if x →∗ y0 and x →∗ y1 implies
there is a z such that y0 →∗ z and y1 →∗ z. A reduction is terminating
if there are no infinite descending chains. A reduction is convergent if it is
confluent and terminating.
    Let K be the set of preskeletons. Algorithms are specified as reduction
systems of the form (K, →), which are then used to specify a related setwise
reduction system of the form (2K , ↠). Setwise reduction systems are the
ones with the interesting normal forms and confluence properties. In a setwise
reduction system, reduction rewrites one element of a set to a set of elements.

Definition 6.1 (Setwise Reduction System). The setwise reduction system
of binary relation ⇝⊆ K × 2K is a reduction system (2K , ↠), where for each
K0 ∈ 2K , K0 ↠ K1 if for some k0 ∈ K0 , k0 ⇝ K2 , K1 = K2 ∪ (K0 \ {k0 }),
and K1 ̸= K0 .

   The cpsa algorithm will be specified as a setwise term reduction system,
where the initial problem is given a singleton in 2K , and the answers computed
by an implementation of the algorithm are a normal form of the setwise
reduction relation ↠k defined in Chapter 14.



    In what follows the relation k ⇝ K is defined in terms of →⊆ K × K by
specifying {k} ↠ K using →, so the ⇝ relation is not explicitly defined.
    We regard sets of preskeletons as factored by isomorphism, where each
set has at most one representative of the equivalence class of isomorphic
preskeletons. The definition of isomorphic preskeletons is given on Page 17.
    The cpsa Design [12] describes an extension of a message algebra signa-
ture that models the data structures used in the cpsa program. The terms
over the extended signature include ones that model preskeletons. Sets of
terms of sort preskeleton are the domain of our setwise reduction systems.






## Chapter 7


Primitive Preskeleton
Operators

The are four primitive operators on preskeletons used by cpsa to solve
authentication tests. Each operator is a partial map from preskeletons to
preskeletons.

Definition 7.1 (Substitution Operator). For order-sorted substitution σ : X →
AY , the operator Sσ is:

                Sσ (kX (rl , P, ΘX , ≺, N, U )) =
                  kY (rl , P, s 7→ σ ◦ ΘX (s), ≺, σ(N ), σ(U ))

   For k ′ = Sσ (k), there is a homomorphism from k to k ′ only if for all
t ∈ Uk , Ok (t) ⊆ Ok′ (σ(t)). The structure preserving maps associated with
the homomorphism are ϕid and σ.

Definition 7.2 (Compression Operator). For distinct strands s and s′ , op-
erator Cs,s′ compresses strand s into s′ .

                    Cs,s′ (kX (rl , P, ΘX , ≺, N, U )) =
                      kX (rl ◦ ϕ′s , P, ΘX ◦ ϕ′s , ≺′ , N, U )

where                              
                                       j + 1 if j ≥ s
                       ϕ′s (j) =
                                       j     otherwise,




relation ≺′ is the transitive closure of ϕs,s′ (≺), and

                                      ϕs (s′ ) if j = s
                                    
                        ϕs,s′ (j) =
                                     ϕs (j) otherwise
                                      j − 1 if j > s
                          ϕs (j) =
                                      j        otherwise.

    The compression operator is only used when ΘX (s) is a prefix of ΘX (s′ ),
and when there is a homomorphism from k to Cs,s′ (k). The structure pre-
serving maps associated with the homomorphism are ϕs,s′ and σid . Note that
the compression operator is defined only when relation ≺′ is asymmetric, and
that ϕs,s′ ◦ ϕ′s = ϕid .

Definition 7.3 (Ordering Enrichment Operator). Operator O applied to k
enriches ≺k by adding all elements implied by unique origination. That
is O(k) = kX (rl , P, ΘX , ≺′ , N, U )), where k = kX (rl , P, ΘX , ≺, N, U ) and
≺′ = (≺ ∪{(n0 , n1 ) | n0 ∈ O(k, t) ∧ n1 ∈ G(k, t)})∗ .

   The ordering enrichment operator is total and idempotent. The struc-
ture preserving maps associated with the operator’s homomorphism are ϕid
and σid , i.e. the homomorphism is an embedding.

Definition 7.4 (Augmentation Operator). For node n, role r, and trace C,
operator An,r,C is:

                     An,r,C (kX (rl , P, ΘX , ≺, N, U )) =
                       kX ′ (rl ⌢ r, P, ΘX (s) ⌢ C, ≺′ , N ′ , U ′ )

where X ′ is X extended to include the variables in C, ≺′ is the minimal
extension of ≺ such that (|ΘX | + 1, |C|) ≺′ n, N ′ is N extended with non-
origination assumptions inherited from r by C, and likewise for U ′ .

    The structure preserving maps associated with the augmentation opera-
tor’s homomorphism are ϕid and σid , i.e. the homomorphism is an embedding.






## Chapter 8


Reductions on Preskeletons

This chapter describes the algorithm used to transform a preskeleton into a
skeleton as a setwise term reduction system (K, ↠). Recall that the relation
k ⇝ K in Chapter 6 is defined in terms of →⊆ K × K by specifying {k} ↠ K
using →. Additionally, when k = k(rl , P, Θ, ≺, N, U ), Uk is used to name U ,
and so forth for other components of k.
    If a preskeleton k is not a skeleton, then it is either because some t ∈ Uk
actually originates at more than one node, or because for some t ∈ Uk ,
there is a node n1 ∈ Gk (t), and a node n0 ∈ Ok (t) such that n0 ⊀k n1 . A
preskeleton in which an atom assumed to be uniquely originating originates
more than once is simply expunged. The second obstruction is resolved by
enriching node orderings. A hulled preskeleton is a preskeleton in which every
uniquely originating atom originates at most once, but it may lack some node
orderings needed to be a skeleton.
    Skeletons may contain “effectively equivalent” strands. After converting
preskeletons to skeletons, a preskeleton reduction system may remove effec-
tively equivalent strands using a process called thinning. A skeleton without
any effectively equivalent strands is called a thinned skeleton.

Definition 8.1 (Hulling Reduction). A non-hulled preskeleton k is expunged.
                                           H
The setwise hulling reduction rule is {k} −↠ {} when k is not hulled.

Definition 8.2 (Order Enrichment). Suppose hulled preskeleton k0 is not a
skeleton. Hulled preskeleton k0 reduces to skeleton k1 by order enrichment,
             O
written k0 −→ k1 , iff k1 is the result of adding node orderings implied by
origination. That is, ≺k1 = (≺k0 ∪ {(n0 , n1 ) | n0 ∈ O(k0 , t) ∧ n1 ∈ G(k0 , t)})∗ .



There is a homomorphism from k0 to k1 that is an embedding. For the
                                           O           O
setwise order enrichment reduction, {k0 } −↠ {k1 | k0 −→ k1 } when k0 is a
hulled preskeleton that is not a skeleton.
   The thinning operator Ts removes an effectively equivalent strand.
Definition 8.3 (Thinning). Two strands s and s′ in a skeleton k are effec-
tively equivalent if k with s removed and k with s′ removed are isomorphic.
(Page 17 defines isomorphic skeletons.) Skeleton k0 reduces to skeleton k1
                           Ts
by thinning, written k0 −→     k1 , if and only if there exists a strand s′ that
is effectively equivalent to s in k0 and k1 is isomorphic to both k0 with s
                                                     Ts
removed and k0 with s′ removed. In detail, k0 −→         k1 if and only if there
                  ′
exists a strand s such that
  1. strands s and s′ are not in the image of k0 ’s strand map from the
     point-of-view skeleton;
  2. Θk0 (s) is isomorphic to Θk0 (s′ );
  3. let k1 be k0 with strand s removed, along with extraneous origination
     assumptions;
  4. let k2 be k0 with strand s′ removed, along with extraneous origination
     assumptions;
  5. k1 is isomorphic to k2 .
                                              Ts           sT
    For the setwise thinning reduction, {k0 } −↠ {k1 | k0 −→ k1 }, when there
                      Ts
is a k1 such that k0 −→ k1 .
    Thinning in cpsa is also implemented for the case of sets of multiple
strands rather than pairs of individual strands. The correctness of thinning
has yet to be demonstrated.



### 8.1      Reduction Systems

Notice that a setwise hulling reduction may produce the empty set, but a
setwise order enrichment and thinning reduction never does.
   There are two preskeleton reduction systems, one with thinning, and one
                                                S     H      O
without. For the one without, let reduction ↠= s,s′ −↠ ∪ −↠.


Definition 8.4 (Preskeleton Reduction System). Preskeleton k0 reduces to
                         skel
skeleton k1 , written k0 −→ k1 , if {k0 } ↠∗ K, k1 ∈ K, and K is a normal
form of ↠.
                         skel
   For each skeleton k, k −→ k.
                                        S      H    O  S Ts
   When using thinning, let reduction ↠= s,s′ −↠ ∪ −↠ ∪ s −↠.

Definition 8.5 (Preskeleton Reduction System with Thinning). Preskele-
                                                   tskel
ton k0 reduces to thinned skeleton k1 , written k0 −→ k1 , if {k0 } ↠∗ K,
k1 ∈ K, and K is a normal form of ↠.
                                 tskel
   For each thinned skeleton k, k −→ k.






## Chapter 9


Penetrator Derivable

For each algebra, the powers of the adversary are defined by a set of roles.
For the Basic Crypto Signature in Figure 2.1, the traces of the penetrator
roles are in Figure 9.1. Penetrator roles make no origination assumptions.
    The context in which penetrator strands appear determine the messages
the adversary can derive. The context includes previously sent messages
and atoms it is forbidden to originate. An atom that is assumed to be non-
originating must be avoided as is a uniquely originating atom that is assumed
to originate on a regular strand.
    The ternary relation Tp : Ta ⊢ t states that message t is penetrator
derivable from previously sent messages Tp while avoiding atoms Ta . The
relation is defined by a set of inference rules. Most of the rules are justified by
a penetrator role that when instantiated, derives a message in the conclusion

                base(t) = ⟨+t⟩, where t is an atom
                  tag(t) = ⟨+t⟩, where t is a tag
            pair (t0 , t1 ) = ⟨−t0 , −t1 , +(t0 , t1 )⟩
             sep(t0 , t1 ) = ⟨−(t0 , t1 ), +t0 , +t1 ⟩
             enc(t0 , t1 ) = ⟨−t0 , −t1 , +{|t0 |}t1 ⟩
             dec(t0 , t1 ) = ⟨−{|t0 |}t1 , −t2 , +t0 ⟩, where t2 = inv (t1 )
                hash(t) = ⟨−t, +#t⟩
               put(c, t) = ⟨−t, +[c, t]⟩
              take(c, t) = ⟨−[c, t], +t⟩

                         Figure 9.1: Penetrator Traces



of the rule. Note there are no rules that pertain to channel messages. Channel
messages are handled elsewhere.
    The first rule states that no additional penetrator behavior is required to
derive t if it has been previously sent.
                                    t ∈ Tp
                                                                          (9.1)
                                  Tp : Ta ⊢ t

By base(t):
                            t an atom      t∈/ Ta
                                                                          (9.2)
                                 Tp : Ta ⊢ t
By tag(“. . . ”):
                                Tp : ta ⊢ “. . . ”                        (9.3)
By pair (t0 , t1 ):
                         Tp : Ta ⊢ t0     Tp : Ta ⊢ t1
                                                                          (9.4)
                               Tp : Ta ⊢ (t0 , t1 )
By sep(t0 , t1 ):
                               Tp : Ta ⊢ (t0 , t1 )
                                                                          (9.5)
                                 Tp : Ta ⊢ t0
By sep(t0 , t1 ):
                               Tp : Ta ⊢ (t0 , t1 )
                                                                          (9.6)
                                 Tp : Ta ⊢ t1
By enc(t, k):
                          Tp : Ta ⊢ t     Tp : Ta ⊢ k
                                                                          (9.7)
                                Tp : Ta ⊢ {|t|}k
By dec(t, k):
                      Tp : Ta ⊢ {|t|}k     Tp : Ta ⊢ inv k
                                                                          (9.8)
                                   Tp : Ta ⊢ t
By hash(t):
                          Tp : Ta ⊢ t     Tp : Ta ⊢ k
                                                                          (9.9)
                                 Tp : Ta ⊢ #t
A non-base sorted variable is derivable in a bundle that instantiates it with
any message other than an element of X⊤ .
                                   t ∈ X⊤
                                                                        (9.10)
                                  Tp : Ta ⊢ t


Definition 9.1 (Sent Channel Messages). The sent channel messages of
skeleton k at n is sntchmsg(k, n) = {msg k (n0 ) | n0 ≺k n, n0 is transmitting}.

Definition 9.2 (Public Messages). The public messages of skeleton k at n
is
       pubmsg(k, n) = {t | [t] ∈ M } ∪ {t | [c, t] ∈ M ∧ c ∈
                                                           / conf (k)},
where M = sntchmsg(k, n), and conf (k) is the set of channels assumed to
be confidential in k.

Definition 9.3 (Avoidance Set). The avoidance set of skeleton k is avoid (k) =
Nk ∪ {t | t ∈ Uk ∧ |Ok (t)| = 1}.

   An atom in avoid (k) is not available to the penetrator, except if it is
exposed by a messages transmission. Clearly, only uniquely originating atoms
can be exposed.

Definition 9.4 (Derivable Before). A channel message m is derivable before
reception node n in skeleton k, written der (k, n, t), if

  1. m ∈ sntchmsg(k, n),

  2. m = [t] and Tp : Ta ⊢ t, or

  3. m = [c, t], c ∈
                   / auth k, and Tp : Ta ⊢ t,

where Tp = pubmsg(k, n), Ta = avoid (k), and auth(k) is the set of channels
assumed to be authenticated in k.

Definition 9.5 (Realized Node). A reception node n is realized in skeleton k
if msg k (n) is derivable before n in k.

   Notice that one can read off penetrator behavior from the proof tree used
to demonstrate that msg k (n) is derivable before n in k. For example, if
a decryption step is required by the proof, an instance of the penetrator’s
decryption role is indicated. In a bundle, for a non-base sorted variable,
there is a substitution that maps the variable to a message that is not a non-
base sorted variable. The substitution determines the penetrator behavior
associated with the variable.

Conjecture 9.1 (Realized Skeleton). A skeleton is realized if and only if all
of its reception nodes are realized.


Partial Proof. Given a skeleton k in which all of its reception nodes are real-
ized, the combination of the regular behavior in the skeleton, the penetrator
behavior specified by the proof trees used to demonstrate each node is real-
ized, and a substitution for non-base sorted variables determines a bundle.
The skeleton of the bundle may have more non-originating atoms than is
in Nk , however since the extra non-originating atoms are derivable by the
bundle that realizes k, the proof trees for those atoms specify any additional
penetrator behavior required.
    The “only if” part of this proof has yet to be completed.



### 9.1      Implementation

The derivable before a node predicate is implemented using auxiliary func-
tions.

Definition 9.6 (Buildable). Message t is buildable from previously sent mes-
sages Tp while avoiding Ta , written bld (t, Tp , Ta ), if Tp : Ta ⊢ t without the
use of Inference Rules 9.5, 9.6, and 9.8.

   Consider the following reduction system based on Inference Rules 9.5,
9.10, 9.6, and 9.8.

                   Tp : Ta → Tp : Ta \ {t}                      if t ∈ Tp and t ∈ Ta
                   Tp : Ta → Tp \ {x} : Ta                      if x ∈ Tp and x ∈ X⊤
    {(t0 , t1 )} ∪ Tp : Ta → {t0 , t1 , (t0 , t1 )} ∪ Tp : Ta   if t0 or t1 ∈/ Tp
    {{|t0 |}t1 } ∪ Tp : Ta → {t0 , {|t0 |}t1 } ∪ Tp : Ta        if t0 ∈
                                                                      / Tp and
                                                                bld (inv (t1 ), Tp , Ta )

Definition 9.7 (Decompose). Previously sent messages Tp and avoidance
set Ta decompose to Tp′ , Ta′ , written decompose(Tp , Ta ) = (Tp′ , Ta′ ), if Tp :
Ta →∗ Tp′ : Ta′ and (Tp′ , Ta′ ) is a normal form of reduction →.

   The penetrator derivable predicate Tp : Ta ⊢ t is implemented as

                        Tp : Ta ⊢ t =
                          let Tp′ , Ta′ = decompose(Tp , Ta ) in
                          bld (t, Tp′ , Ta′ )
   The decomposition at a node function is



               dcmp(k, n) =
                 decompose(pubmsg(k, n), avoid (k))
The derivable before a node predicate is implemented as
                   der (k, n, t) =
                     let Tp , Ta = dcmp(k, n) in
                     bld (t, Tp , Ta )






## Chapter 10


Carried Only Within

A set of encryptions Te protects critical message t in message t′ if t is carried
by t′ only within a member of Te . The definition of the carried only within
(cow) relation to follow makes this concept precise. The concept is used
when solving authentication tests (Chapter 11).

Definition 10.1 (Ancestors). Let t′ = t @ p. The ancestors of t′ in t at p is
the set anc(t, p) = {t @ p′ | p′ a proper prefix of p}.

Definition 10.2 (Carried Only Within). Message t is carried only within
set Te in t′ if for all carried positions p of t in t′ , there exists an ancestor ta ∈
anc(t′ , p) and te ∈ Te such that ta ≡ te .

   The function defines carpos(t, t′ ) is defined on Page 6, the set of positions
at which t′ carries t. The interface to each algebra exports unify 0 , where

               unify 0 (t, t′ , σ) = {σ ′ ◦ σ | σ ′ ∈ unify(σ(t), σ(t′ ))}.

Unification is extended to channel messages as:

             unify0 ([t], [t′ ], σ) = unify0 (t, t′ , σ)
             unify0 ([c, t], [c′ , t′ ], σ) =
                  {σ ′′ | σ ′ ∈ unify0 (c, c′ , σ) ∧ σ ′′ ∈ unify0 (t, t′ , σ ′ )}

   The details of a reduction on skeletons called a augmentation will be
described in Section 11.2. In simplified form, for an augmentation, given t, Te ,
and t′ , one must find all most general unifiers σ such that σ(t) is carried only
within set σ(Te ) in σ(t′ ).


cows(t, T, t′ ) =
  cows 0 (t, T, t′ , σid )   — σid is the identity subst

cows 0 (t, T, t′ , σ) =
  if σ(t) is cow σ(T ) at σ(t′ ) then
     {σ}
  else
     let S = fold (t, T, t′ , σ) in
                              ′   ′
     S
        σ ′ ∈S cows 0 (t, T, t , σ )


fold (t, T, t′ , σ) =
   {σ ′ ◦ σ | σ ′ ∈ fold 0 (σ(T ), σ(t′ ), {σid }, carpos(σ(t), σ(t′ )))}

fold 0 (T, t′ , S, {}) = S
fold 0 (T, t′ , S, ⟨p⟩ ⌢ P ) =
   fold 0 (T, t′ , solve(anc(t′ , p), T, S), P )

solve(T, T ′ , S) =
  {σ ′ | t ∈ T, t′ ∈ T ′ , σ ∈ S, σ ′ ∈ unify 0 (t, t′ , σ)}


                  Figure 10.1: The cows Function





              fold (t, T, t′ , σ) =
                 fold 0 (t, T, t′ , σ, {σid }, carpos(σ(t), σ(t′ )))

              fold 0 (t, T, t′ , σ, S, {}) = {σ ′ ◦ σ|σ ′ ∈ S}
              fold 0 (t, T, t′ , σ, S, ⟨p⟩ ⌢ P ) =
                 fold 0 (t, T, t′ , σ, solve(anc(σ(t′ ), p), σ(T ), S), P )


                  Figure 10.2: The Alternate fold Function

    A carried only within solution cannot be directly computed using Defi-
nition 10.2. Given terms ta and te , the unify 0 function finds substitutions σ
such σ(ta ) ≡ σ(te ), however, the carried positions carpos(σ(t), σ(t′ )), are
used before the unify 0 function computes the substitution σ. Figure 10.1
displays the iterative procedure that breaks the cyclic dependencies. Each
step of the iteration improves an approximation of a solution to the problem.
The correctness of this function is shown in [9], although for a version of the
algorithm with the alternate definition for the function fold in Figure 10.2.






## Chapter 11


Solving Authentication Tests

Definition 11.1 (Protectors). The protectors of t are encryptions that carry t
and cannot be decrypted. Function prot(Tp , Ta , t) is undefined if bld (t, Tp , Ta ),
otherwise

    prot(Tp , Ta , t) = {{|t0 |}t1 ∈ Tp | t0 carries t and ¬ bld (inv (t1 ), Tp , Ta )}

Definition 11.2 (Escape Set). The escape set for message tc at n in skele-
ton k, esc(k, n, tc ), contains encryptions and channel messages. Function
esc(k, n, tc ) = prot(tc , Tp , Ta ) ∪ M , where (Tp , Ta ) = dcmp(k, n) (See Defini-
tion 9.7), and M is the set of sent channel messages with confidential channels
that carry tc . It is undefined when tc is derivable in k at n.

Definition 11.3 (Critical Position, Critical Message). Position p is a critical
position at n in k if for m = msg k (n)

   1. p is a carried position in m,

   2. m @ p is not derivable before n in k,

   3. either

       (a) m @ p ∈ Uk ,
       (b) m @ p = #t1 ,
       (c) m @ p = {|t0 |}t1 and t1 is not derivable before n in k, or
       (d) m = [c, t], p = ⟨⟩, and c ∈ auth(k).



  4. anc(t, p) ∩ esc(k, n, t @ p) = ∅.

The message at a critical position is called a critical message.

Definition 11.4 (Authentication Test). The triple (k, n, p) is an authenti-
cation test iff p is a critical position at reception node n in k.

     An authentication test is a nonce test if the critical message is an atom,
it is a channel test if the critical message is a channel message, otherwise it
is an encryption test. (A hash is treated as a kind of encryption in which
the term that is hashed is the encryption key.) Observe that every critical
message at a node in a skeleton is not derivable at the node.

Conjecture 11.1. A reception node is unrealized iff it has a critical position.

Definition 11.5 (Target Messages). Let Te be a set of messages, and tc be
a message. The set of target messages is

   targ(tc , Te ) = {tc } ∪ {tt | te ∈ Te , p ∈ carpos(tc , te ), tt ∈ anc(te , p)} \ Te .

Definition 11.6 (Critical Position Solved). Suppose p is a critical position
                     ϕ,σ
at n in k0 and k0 7−→ k1 . Let t = msg k0 (n)@p, and T = esc(k0 , n, t). Critical
position p is solved in k1 after k0 at n if:

  1. anc(msg k1 (ϕ(n)), p) ∩ σ(T ) ̸= ∅, or

  2. for some tp ∈ sntchmsg(k1 , ϕ(n)), σ(t) is not carried only within σ(T )
     in tp , or

  3. targ(σ(t), σ(T )) \ σ(targ(t, T )) ̸= ∅ and there are variables in k’s pro-
     tocol that are not atoms, or

  4. the decryption key of a member of σ(T ) is derivable before ϕ(n) in k1 ,
     or

  5. σ(t) is an encryption and its encryption key is derivable before ϕ(n)
     in k1 .






### 11.1        Test Solving Steps

A step used to solve a test is a contraction (Definition 11.7), a regular aug-
mentation (Definition 11.8), a displacement (Definition 11.9), or a listener
augmentation (Definition 11.10).
Definition 11.7 (Contraction). Let p be a critical position at n in k, t =
msg k (n), and Te = esc(k, n, t@p). Suppose there is a substitution σ such that
for some ta ∈ anc(t, p), te ∈ Te , σ(ta ) = σ(te ). Skeleton k1 is a contraction if
   Sσ      tskel
k −→   k0 −→ k1 .
   cpsa computes a set of substitutions for each critical position, and then
removes some substitutions to form a complete set of most general unifiers.
Only most general unifiers are used for contractions.
Definition 11.8 (Regular Augmentation). Suppose substitution σ, non-
listener role r, and trace C are selected as described in Section 11.2. Skele-
                                       σ             S        An,r,C      tskel
ton k2 is a regular augmentation if k −→ k0 −→ k1 −→ k2 .
Definition 11.9 (Displacement). Let substitution σ, non-listener role r, and
trace C be selected as described in Section 11.2, and there be a preskeleton k1
               S       An,r,C
such that k −→   σ
                    k0 −→ k1 . Suppose there are strands s and s′ , where one
of them is the newly created strand, and a most general unifier σ ′ such
that σ ′ (Θk1 (s)(j)) ≡ σ ′ (Θk1 (s′ )(j)) for 0 ≤ j < |Θk1 (s)|. Skeleton k4 is a
                    σ S ′       Cs,s′       tskel
displacement if k1 −→ k2 −→ k3 −→ k4 .
Definition 11.10 (Listener Augmentation). Let p be a critical position at n
in k, tc = msg k (n) @ p, and Te = esc(k, n, tc ). For each {|t0 |}t1 ∈ Te , skele-
                                                         An,lsn,C      tskel
ton k1 is a listener augmentation if k −→ k0 −→ k1 and C listens for
inv (t1 ), i.e. C = ⟨− inv (t1 ), + inv (t1 )⟩. If tc = {|t0 |}t1 , then skeleton k1 is a
                                 An,lsn,C       tskel
listener augmentation if k −→ k0 −→ k1 and C = ⟨−t1 , +t1 ⟩.
   For regular augmentation and displacement, cpsa removes solutions that
lead to skeletons that are less general than other solutions, that is, when
there is a homomorphism from a solution to the omitted solution.
Definition 11.11 (Cohort Member). For unrealized node n in a skeleton k0 ,
                           n,p
and a position p at n, k0 −→ k1 asserts that k1 is a member of the cohort of k0 ,
where k1 is derived using contraction, regular augmentation, displacement,


or listener augmentation, and p is solved in k1 after k0 at n. For the setwise
                                     n,p       n,p
cohort member reduction, {k0 } −↠ {k1 | k0 −→ k1 }, when n is unrealized
in k0 , and p is a critical position at n.
                                                          n0 ,p0   n1 ,p1   nℓ−1 ,pℓ−1
Conjecture 11.2 (Critical Message Solved). If k0 −→ k1 −→ . . . −→ kℓ
is a sequence of cohort member reductions, then for positive ℓ, p0 is solved
in kℓ after k0 at n0 .



### 11.2        Augmentation

Let tc be the critical message that demonstrates n is a test node in skeleton k.
For each triple (σ, r, C) that satisfies some properties, there is a potential
                               tskel   An,r,Cσ   S
regular augmentation with −→ ◦ −→ ◦ −→.          When successful, the message t
in the last event of the added strand is outbound, carries σ(tc ), but σ(tc ) is
not carried only within escape set σ(Te ) in t, where Te = esc(k, n, tc ), the
escape set. Moreover, for every other message t in the strand, σ(tc ) is carried
only within escape set σ(Te ) in t. The last event in the strand is called a
transforming event, as this event no longer protects the critical message, but
events that precede it do.
    cpsa computes the parameters for a set of augmentation steps as follows.
Suppose skeleton k = kX ( , P, , , , ). First, compute the target messages,
Tt = targ(tc , Te ). Next, for each non-listener role r(Cr , Nr , Ur ) ∈ P and each
index h where Cr (h) = +t, a transmission, do the following.

Create fresh variables: Let σr be a sort preserving variable renaming,
    where the domain is the variables that occur in Cr †h, and every variable
    in the range does not occur in X or in P .

Insert critical message: For each message t′ carried by t, and each tt ∈
     targ(tc , Te ), consider most general unifiers σ ′ where, σ ′ (t′ ) = σ ′ (tt ) and
     σr ⊴ σ ′ . (In other words, σ ′ = σ0 ◦ σr for some σ0 .)

Ensure previous events do not transform: For each σ ′ , find most gen-
    eral unifiers σ such that for 0 ≤ i < h, σ(tc ) is carried only within
    σ(Te ) at σ(C(i)) and σ ′ ⊴ σ. The function cowt, presented in Fig-
    ure 11.1, performs the explorations, producing the substitutions S ′ =
    cowt(tc , Te , Cr † h, S). Function fold is defined in Figure 10.1. Let Sr,h
    be the set S ′ with non-most general unifiers removed.


                cowt(t,
                  S T, C, S) =
                    σ∈S cowt 0 (t, T, C, σ)


                cowt 0 (t, T, C, σ) =
                  if ∀t ±t ∈ C → σ(t) is cow σ(T ) at σ(t′ ) then
                     {σ}
                  else
                     cowt(t, T, C, foldn(t, T, C, {σ}))

                foldn(t, T, ⟨⟩, S) = S
                foldn(t, T, ⟨±t′ ⟩S
                                  ⌢
                                    C, S) =
                   foldn(t, T, C, σ∈S fold (t, T, t′ , σ))


                             Figure 11.1: The cowt Function

Ensure last event transforms: For each σ ∈ Sr,h , if σ(tc ) is not carried
    only with σ(Te ) at σ(C(h)), try augmenting with parameters n, r,
    σ ◦ C † h, and σ.
    For target terms to be the reasonable set for insertion of the critical mes-
sage, one must require that variables of sort message are acquired. This fact
needs to be explained and noted as another reason for the acquired variable
constraint.
    The following example shows the need for Item 3 in the definition of a
solved critical position. The protocol has two roles.

     init(a : N, n1 , n2 : D, k : A) = r(⟨+{|n1 , {|a, n2 |}k |}k , −{|a, n1 |}k ⟩, ∅, ∅)
       resp(n1 : D, m : ⊤, k : A) = r(⟨−{|n1 , m|}k , +m⟩, ∅, ∅)
where we use N for sort name, D for sort data A for sort akey, and ⊤ for
sort mesg to save space. Notice the responder declares m to be of sort mesg.
    The point-of-view skeleton k0 is:
        kY (⟨init(a′ , n′1 , n′2 , k ′ )⟩                              Role map
            {init(a′ , n′1 , n′2 , k ′ ), resp(n′′1 , m′′ , k ′′ )},   Protocol
            ⟨⟨+{|n1 , {|a, n2 |}k |}k , −{|a, n1 |}k ⟩⟩,               Traces
            ∅,                                                         Node orderings
            {k −1 },                                                   Non-origination
            {n1 })                                                     Unique origination


where Y = a : N, n1 , n2 : D, k : A.
    cpsa finds the nonce test (k0 , (0, 1), ⟨0, 1⟩) with critical message n1 . The
escape set E = esc(k0 , (0, 1), n1 ) = {{|n1 , {|a, n2 |}k |}k }.
    cpsa solves this test to produce skeleton k1 with a displacement that
                                          ϕ,σ
simply equates n1 and n2 . Thus, k0 7−→ k1 where ϕ = ⟨0⟩ and σ = {n1 7→
n2 }.
    Consider Definition 11.6, the definition of critical position solved. Item 1
does not apply because an ancestor of the image of the critical position does
not match E. Item 2 does not apply because (k1 , (0, 1), ⟨0, 1⟩) is a nonce
test. Item 4 does not apply because the key that protects the member of
the escape set is non-originating. Finally, Item 5 does not apply because the
critical message is not an encryption.
    Item 3 applies in this example because

                    targs(n1 , E) = {n1 , (n1 , {|a, n2 |}k )}
              targs(σ(n1 ), σ(E)) = {n2 , (n2 , {|a, n2 |}k ), (a, n2 )}.

so targs(σ(n1 ), σ(E)) \ σ(targs(n1 , E)) = {(a, n2 )}.
    Once n1 and n2 have been equated, cpsa easily finds the one shape by
adding a responder instance. The shape corresponds to a rather odd use of
the initiator role. The instance of that role picks a fresh value for n1 and
then makes use of that value for its n2 parameter. See Appendix B for more
on the relation between roles and the programs they specify.






## Chapter 12


Collapsing and Preconditioning

The input preskeleton is preconditioned before it is subjected to authen-
tication test solving. The preskeleton is converted to a skeleton and then
collapsing is applied so as to ensure all shapes are found. Collapsing handles
the case in which strands merged in the input lead to shapes.

Definition 12.1 (Collapsing). Let k0 and k1 be two skeletons such that
there are two strands, s and s′ , and a most general unifier σ such that
σ(Θk0 (s)(j)) ≡ σ(Θk0 (s′ )(j)) for all 0 ≤ j < |Θk0 (s)|. Then k0 collapses
                  clp          S         Cs,s′   skel
                                  σ
to k1 , written k0 −→ k1 , if k0 −→ k −→ k ′ −→ k1 .

Definition 12.2 (Preconditioning). For point-of-view preskeleton k0 , k0 is
                                   pre              skel   clp
preconditioned to k1 , written k0 −→ k1 , if k0 −→ k (−→)∗ k1 .






## Chapter 13


Generalization

The cohort reduction system produces a set of realized skeletons. General-
ization attempts to convert that set into a set of skeletons. Not all possible
cases are implemented due to performance issues, so it is not uncommon to
find a realized skeleton in the output of a run of cpsa that is not a shape.

Conjecture 13.1 (Shape Completeness). Without generalization, cpsa pro-
duces a complete set of shapes among the realized skeletons in its output.

Definition 13.1 (Generalize). A skeleton k0 generalizes skeleton k1 , written
     <
k1 −→k k0 , if both k0 and k1 are realized, k0 and k1 are not isomorphic, there
is a homomorphism from a point-of-view skeleton k to k0 , and a strandwise
injective homomorphism k0 7→ k1 .
                                                             ≤
    If skeletons are allowed to be isomorphic, we write k1 −→k k0 , and note
       ≤
that −→k defines a partial ordering. Therefore, there are maximal elements
in the partial ordering. A shape associated with a preskeleton is a maximally
generalized realized skeleton derived from the preskeleton.
                                                                     pre
Definition 13.2 (Shape). Let k0 be a preskeleton such that k0 −→ k for
some skeleton k, and let k1 be a realized skeleton such that k 7→ k1 . Skele-
                               ≤
ton k2 is a shape of k0 if k1 −→k k2 , and k2 is maximal among skeletons that
generalize k1 .

    There are four generalization reductions used to transform a realized
skeleton into its shapes: deletion, weakening, forgetting, and separation.



Definition 13.3 (Deletion). Skeleton k0 generalizes by deletion skeleton k1 ,
            Dn               <          skel
written k1 −→  k k0 , if k1 −→k k0 , k2 −→ k0 , and k2 is the result of deleting
node n in k1 and all of the nodes that follow it in its strand.

Definition 13.4 (Weakening). Skeleton k0 generalizes by weakening skele-
                    Wn,n′             <            skel
ton k1 , written k1 −→ k k0 , if k1 −→k k0 , k2 −→ k0 , and k2 is k1 except
≺k2 = (≺k1 \ {(n, n′ )})∗ .

Definition 13.5 (Forgetting). Skeleton k0 generalizes by origination as-
                                              Ft               <          skel
sumption forgetting skeleton k1 , written k1 −→  k k0 , if k1 −→k k0 , k2 −→ k0 ,
and k2 is k1 except Uk2 = Uk1 \ {t} and Nk2 = Nk1 \ {t}.

    Sometimes a more general skeleton can be found by replacing some oc-
currences of one variable by a fresh variable. For variable separation, the
location of an occurrence of a variable is defined using a skeleton’s instance.
Recall that in the external syntax, strand s in skeleton k is described by an
instance of the form i(r, h, σ). (Instances are introduced in Section 5.4.)

Definition 13.6 (Location). Variable x is at location (s, y, p) in k if the
instance at Θk (s) is i(r, h, σ) and x = σ(y) @ p.

Definition 13.7 (Variable Separation). Skeleton k0 generalizes by variable
                                      Vt               <          skel
separation skeleton k1 , written k1 −→   k k0 , if k1 −→k k0 , k2 −→ k0 , and k2
is k1 except t is a variable that occurs in multiple locations in k1 , and k2 is
the result of replacing t with a variable t0 of the same sort at a proper subset
of t’s locations, where t0 occurs nowhere in k1 .

    When separating a non-originating term, both the term and its clone are
non-originating. When separating a uniquely originating term, either the
term or its clone is uniquely originating.
    What happens when separating t in k into t and t0 , and ltk(t, t) ∈ Nk ?
Should a skeleton k0 with ltk(t, t0 ) ∈ Nk0 be a candidate separation? Cur-
rently, only skeletons k1 with ltk(t, t) ∈ Nk1 and ltk(t0 , t0 ) ∈ Nk1 are consid-
ered.
                                                     gen      S Dn        S    Wn,n′
Definition 13.8 (Generalization). The reduction −→k = n −→            k ∪ n,n′ −→ k
  S Ft        S Vt
∪ t −→    k ∪ t −→k is the generalization relation. For the setwise general-
                         gen                  gen
ization reduction, {k0 } −↠k {k1 } when k0 −→k k1 .



    The fact that each generalization reduction replaces a singleton with just
a singleton requires explanation. It’s simply a matter of performance. If
all possibilities are considered, cpsa run time would become dominated by
generalization. Since generalization failures do not interfere with producing
a complete description of the input, an approximation of the set of shapes is
okay.
                                                    gen
Conjecture 13.2 (Generalization). The relation −↠k is terminating.


Discussion
In [5], the shapes of a point-of-view skeleton are said to be minimal, in
the partial ordering induced by injective homomorphism, among all realized
homomorphic images of the point-of-view skeleton. Minimal corresponds to
maximally generalized. The need for origination assumption forgetting was
not known when [5] was written. Generalization by variable separation uses
non-carried positions, and in particular, positions that traverse an atom edge.
Algebras in previous strand space papers have no concept of a position that
traverses an atom edge, and therefore cannot be used to specify generalization
by variable separation.
    Variable separation can be expensive when there are many possible ways
to separate variables. The implementation simply truncates the search when
it grows too large. The current implementation never attempts to separate
channel variables.






## Chapter 14


Skeleton Reduction System

                     co    gen
Let reduction ↠k = (−↠ ∪ −↠k )+ . This reduction system specifies the cpsa
program.

Conjecture 14.1. The reduction ↠k is confluent.

Conjecture 14.2 (Soundness). Let k0 be a preskeleton and k be an unreal-
                           pre
ized skeleton such that k0 −→ k. Skeleton k1 is a shape of k0 if {k} ↠k K,
k1 ∈ K, and K is a normal form.

   The set of bundles denoted by preskeleton k, [[k]] is defined on Page 17.

Conjecture 14.3 (Completeness). Let k0 be a preskeleton and k be an
                                      pre
unrealized
         S    skeleton   such that k0 −→  k. For all K such that {k} ↠k K,
[[k0 ]] = k1 ∈K [[k1 ]].





Acknowledgement

Carolyn Talcott and Leonard Monk provided valuable feedback on drafts of
this document.





Appendix A

Penetrator Non-Origination
Assumptions

Penetrator non-origination assumptions have been added as an extension to
the basic strand space theory. An atom is penetrator non-originating in a
bundle if it originates on no penetrator strand, but each of its variables occurs
in some strand’s trace.
    Penetrator non-origination assumptions can be used to model passwords.
Several regular participants might know a password and originate it in a run
of a protocol, but an idealized password is one the penetrator cannot guess.
    A penetrator non-originating atom is similar to a non-originating atom,
except in that it can be carried. There are two definitions that require
change. Penetrator non-originating atoms must be added to the avoidance
set of Definition 9.3. When the message at a critical position is an atom (see
Definition 11.3, Item 3), instead of being uniquely originating, and can also
be penetrator non-originating.





Appendix B

Programs Specified by a Role

Given the definitions in Chapter 3, a role can be viewed as an abstraction of
a program, and a strand as an abstraction of a run of a program. But what
program is specified by a role?
    Consider a role that contains the event −{|t0 |}t1 . If the program has the
decryption key inv (t1 ) before the message is received, the program could
decrypt the message and extract t0 . Alternatively, if the program has {|t0 |}t1 ,
or has t0 and the encryption key t1 , it might check to see if the received
message is the same as the expected message, and abort the run if not.
    Here is an example of when the second behavior is desired. In cpsa,
before hashing was part of the algebra, an encryption was used to represent
hashing. The hash of t, #t, expanded to {|“hash”, t|}h , where h was an
asymmetric key known to all, but no one knew h−1 . The tag “hash” was
added to the encryption so as to ensure a hash was never confused with
other uses of encryption.
    A role does not specify a valid program if the only possible way of in-
terpreting the event −#t is by using h−1 to decrypt {|“hash”, t|}h . The
remainder of this section describes how this class of specification errors is
detected for the Basic Crypto Algebra.
    The behaviors associated with a trace depend on the set of messages
available initially. The behaviors are specified by a data flow relation, T0 , C ▷
T1 . For trace C, the relation T0 , C ▷ T1 asserts that when messages T0 are
available initially, there is a behavior of C that produces messages T1 .
    A derivation tree used to demonstrate T0 , C ▷ T1 shows the steps that
enable the flow of data. The tree can be linearized, and thus specifies a
sequential program that implements the role.


    The data flow relation is defined with the aid of a data flow relation for
a sequence of events, T0 , C ▷ T1 .

                                      T0 , ⟨±t⟩ ▷ T T, C ▷ T1
                  T, ⟨⟩ ▷ T
                                           T0 , ⟨±t⟩ ⌢ C ▷ T1
   The T0 , ⟨±t⟩ ▷ T1 relation is defined using the T0 , C ▷ T1 relation. An
outbound message can be formed if it is available initially
                                         t∈T
                                     T, ⟨+t⟩ ▷ T
or if it can be formed by construction.
                                                                            
                 T, ⟨+t1 , . . . , +tn ⟩ ▷ T          f (t1 , . . . , tn )
                 T, ⟨+f (t1 , . . . , tn )⟩ ▷ T       not an atom
   An inbound message makes atoms and acquired variables available.
                T, ⟨−t⟩ ▷ T ∪ {t} [t an atom or a variable]
When the decryption key is available, the contents of the encryption are
also available. Furthermore, the encryption can be sent in future messages
without access to its encryption key.
                     T0 , ⟨+ inv (t1 )⟩ ▷ T0 T0 , ⟨−t0 ⟩ ▷ T1
                         T0 , ⟨−{|t0 |}t1 ⟩ ▷ T1 ∪ {{|t0 |}t1 }
A received encryption that can be sent ensures the encryption agrees with
currently available terms and makes nothing new available.
                                 T, ⟨+{|t0 |}t1 ⟩ ▷ T
                                 T, ⟨−{|t0 |}t1 ⟩ ▷ T
   Consider an operation f other than the encryption operation. The order
in which messages that occur in a message constructed using f are made
available may determine if the decryption key of an encryption is available.
All possible orderings must be explored. Let πn be a permutation on the
domain of a sequence of length n.
                                                                          
                T0 , ⟨−t1 , . . . , −tn ⟩ ◦ πn ▷ T1   f (t1 , . . . , tn )
                 T0 , ⟨−f (t1 , . . . , tn )⟩ ▷ T1    not an atom
   The data flow relation is used to find initial sets of atoms that are com-
patible with some behavior of a trace that produces messages.


               proc(a, n, Kb , Ka−1 )            proc(a, n, Kb , Ka )
                 send({|a, n|}Kb );                send({|a, n|}Kb );
                 x0 ← recv();                      x0 ← recv();
                 x1 ← decrypt(x0 , Ka−1 );         x1 ← {|n|}Ka ;
                 x1 ̸= n → fail;                   x0 ̸= x1 → fail;
               end                               end


Figure B.1: Two programs that implement the role ⟨+{|a, n|}Kb , −{|n|}Ka ⟩.

Definition B.1 (Trace Parameters). The set of atoms T0 are parameters of
trace C if T0 , C ▷ T1 for some T1 , and T0 is minimal, that is for all T0′ such
that T0′ , C ▷ T1 , T0′ ̸⊂ T0 .

    The role ⟨+{|a, n|}Kb , −{|n|}Ka ⟩ has two sets of parameters, {a, n, Kb , Ka−1 }
and {a, n, Kb , Ka }. See Figure B for two examples of programs that imple-
ment the role, using distinct parameter sets.
    The cpsa distribution contains a program that computes the set of pa-
rameters of a role. It was used to find an error in a role’s use of hashing as
described at the beginning of this section. The role in question is the verifier
role that is part of an attestation protocol [3]. In an earlier version of the
role, every set of parameters included the decryption key of the encryption
used as a hash. The role was so complicated that inspection did not reveal
the error.
    Note that this section is specific to the basic crypto algebra in the sense
that all non-atomic operations are assumed to be constructable, and encryp-
tion has the specific de-construction recipe shown. Although carried positions
were not mentioned in this section, the inference system specifies the same
concept. In fact, in future work we hope to show that the inference system is
all one needs to define, and that which positions are carried, which are pro-
tected, and which sorts are atoms can be defined in terms of the inferences
available.





Appendix C

Shape Analysis Sentences

For each point-of-view skeleton and its shapes found by cpsa, there is a
formula in a language of order-sorted first-order logic called  W a shape analy-
sis sentence. The sentence has a special form, ∀X(Ψ ⊃ i ∃Yi (∆i ∧ Φi )),
where Ψ, ∆i , and Φi are conjunctions of atomic formulas and X and Yi are
variable sets. This fragment of first-order logic is called coherent logic. For-
mula Ψ describes the point-of-view skeleton k0 . For each homomorphism to
               δi
a shape, k0 7−→   ki , formula ∆i describes the structure preserving maps δi ,
and the shape ki is described by Φi .
    An interpretation of a shape analysis sentence is a skeleton. If cpsa finds
all of the shapes and the homomorphisms associated with a point-of-view
skeleton, the analysis’ sentence is satisfied in all realized skeletons. Let Σ be
a shape analysis sentence and Ψ be a security goal. If Σ ⊃ Ψ is a theorem in
order-sorted first-order logic, then Ψ is satisfied in all realized skeletons and
its protocol achieves this goal.
    Shape analysis sentences are closely related to security goals in [7], and
were motivated by that work. This material was extracted from [11], the
paper that introduced shape analysis sentences.


C.1       Security Goals
The signature for security goal terms extends the one used for the underlying
message algebra with sort Z. Variables of this sort denote strands.
   Security goals make use of protocol specific and protocol independent
predicates. For each role rY (C, N, U ) ∈ P , there are strand length predicates



and strand parameter predicates. There are |C| unary length predicates
P [r, h] : Z, with 1 ≤ h ≤ |r|. Relative to skeleton k, P [r, h](z) asserts
that strand z in k is an instance of r and has a length of at least h. For
each variable x : S that occurs in C, there is a binary parameter predicate
P [r, x] : Z × S. Relative to skeleton k, P [r, x](z, t) asserts that strand z in k
is an instance of r in which x is instantiated as t.
    For each base sort B, there are unary predicates non : B and uniq : B.
non(t) asserts t is non-originating in k and uniq(t) asserts t uniquely originates
in k.
    Let m be the length of the longest role in P . There are m2 precedence
predicates prec[i, j] : Z × Z for 0 ≤ i, j < m. prec[i, j](x, y) asserts that node
(x, i) is before node (y, j) in k. There are 3m origin predicates uniq-at[i] :
B ×Z, with 0 ≤ i < m and B as before. uniq-at[i](t, z) asserts that t uniquely
originates in k at node (z, i). The predicate false has arity zero and, of course,
equality is binary.
    To improve the readability of formulas to follow, we write prec(x, i, y, j)
for prec[i, j](x, y) and uniq-at(t, z, i) for uniq-at[i](t, z).
    Let k = kX (P, I, ≺, N, U ) and let ≺− be the transitive reduction of ≺.
Recall that ΘX is the strand space defined by I, see Section 5.4. We de-
fine F(k) = (Y, Φ), where Φ is k’s skeleton formula, and Y is the formula’s
variable set. For F(k) = (Y, Φ), the variable set Y is X augmented with a
fresh variable of sort Z for each strand in k. Let Z(s) be the strand variable
associated with strand s ∈ Dom(I).
    The formula Φ is a conjunction of atomic formulas composed as follows.
   • For each s ∈ Dom(I), let I(s) = i(r, h, σ) and z = Z(s). Assert
     P [r, h](z). Let r = r(C, N, U ). For each variable x ∈ Vars(C † h) and
     term t = σ(x), assert P [r, x](z, t).
   • For each (s, i) ≺− (s′ , i′ ) such that s ̸= s′ , assert prec(Z(s), i, Z(s′ ), i′ ).
   • For each t ∈ N , assert non(t).
   • For each t ∈ U and (s, i) ∈ Ok (t), assert uniq-at(t, Z(s), i).
   • For each t ∈ U without a point of origination in k, assert uniq(t).
   Given a set of homomorphisms δi : k0 7→ ki , its shape analysis sentence is
                                             _
               S(δi : k0 7→ ki ) = ∀X0 (Φ0 ⊃   ∃Xi (∆i ∧ Φi )),         (C.1)
                                                   i



        ∀a0 , b0 : A, s0 : S, d0 : D, z0 : Z(
          resp 2 (z0 ) ∧ resp a (z0 , a0 ) ∧ resp b (z0 , b0 )
               ∧ resp s (z0 , s0 ) ∧ resp d (z0 , d0 )
               ∧ non(a−1 0 ) ∧ non(b0 )
                                        −1

          ⊃
          ∃a1 , b1 , b2 : A, s1 : S, d1 : D, z1 , z2 : Z(
              z0 = z1 ∧ a0 = a1 ∧ b0 = b1 ∧ s0 = s1 ∧ d0 = d1
                 ∧ resp 2 (z1 ) ∧ resp a (z1 , a1 ) ∧ resp b (z1 , b1 )
                 ∧ resp s (z1 , s1 ) ∧ resp d (z1 , d1 )
                 ∧ init 1 (z2 ) ∧ init a (z2 , a1 ) ∧ init b (z2 , b2 ) ∧ init s (z2 , s1 )
                 ∧ uniq-at(s1 , z2 , 0) ∧ prec(z2 , 0, z1 , 0)
                 ∧ non(a−1                −1
                           1 ) ∧ non(b1 )))


       Figure C.1: Shape Analysis Sentence for Blanchet’s Protocol

where F(k0 ) = (X0 , Φ0 ). The same procedure produces Xi and Φi for
shape ki with one proviso—the variables in Xi that also occur in X0 must be
renamed to avoid trouble while encoding the structure preserving maps δi .
    The structure preserving maps δi = (ϕi , σi ) are encoded in ∆i by a con-
junction of equalities. Map σi is coded as equalities between a message alge-
bra variable in the domain of σi and the term it maps to. Map ϕi is coded as
equalities between strand variables in Φ0 and strand variables in Φi . Let Z0
be the strand variables freshly generated for k0 , and Zi be the ones generated
for ki . The strand mapping part of ∆i is
                             ^
                                   Z0 (s) = Zi (ϕi (s)).
                              s∈Dom(Z0 )


    The shape analysis sentence for the second analysis of Blanchet’s Sim-
ple Example Protocol in Section 5.1 is displayed in Figure C.1. The strand
length predicate P [r, h](z) is written rh (z), and the strand parameter predi-
cate P [r, x](z, t) is written rx (z, t) with the protocol left implicit.

Semantics of Skeleton Formulas. Let k = kX (P, I, ≺, N, U ) and ΘX be
its strand space. When formula Φ is satisfied in skeleton k with order-sorted
variable assignment α, we write k, α |= Φ. For x : S ∈ X, α(x) is in the
carrier set of ĀX for sort S. For x : Z, α(x) ∈ Dom(ΘX ). We write ᾱ when α



is extended to terms in the obvious way. When sentence Σ is satisfied in
skeleton k, we write k |= Σ.

   • k, α |= P [r, h](z) iff h ≤ |ΘX (s)|, and for some σ,

                                 ΘX (s) † h = σ ◦ C † h

      where s = α(z) and r = r(C, N, U ).

   • k, α |= P [r, x](y, t) iff for some σ with σ(x) = ᾱ(t),

                                 ΘX (s) † h = σ ◦ C † h

      where s = α(z), r = r(C, N, U ), and h is the smallest ℓ such that x
      occurs in C † ℓ.

   • k, α |= prec(x, i, y, j) iff (α(x), i) ≺ (α(y), j).

   • k, α |= non(t) iff ᾱ(t) ∈ N .

   • k, α |= uniq(t) iff ᾱ(t) ∈ U .

   • k, α |= uniq-at(t, z, i) iff ᾱ(t) ∈ U and (α(z), i) ∈ Ok (ᾱ(t)).

   • k, α |= y = z iff ᾱ(y) = ᾱ(z).

    Let Σ be a shape analysis sentence and Ψ be a security goal. If Σ ⊃ Ψ is
a theorem in order-sorted first-order logic, then Ψ is satisfied in all realized
skeletons and its protocol achieves this goal.

Channel Formulas. This appendix has not been updated to reflect the
inclusion of channels into cpsa, but the changes made are straightforward.
There are two new unary predicate symbols, auth and conf, that are similar
to non except their argument must be a variable of sort chan. For skeleton k
and variable assignment α, auth(c) is satisfied iff α(c) ∈ auth(k), and conf(c)
is satisfied iff α(c) ∈ conf (k).





Appendix D

Facts and Rules

Support for facts and rules was introduced in version 4.1 of cpsa.
    Each skeleton includes a small database of facts. A fact is a named
relation among fact terms. A fact term is either a strand of the skeleton or
an algebra term. For example, in skeleton k, a user may want to note that
strand 0 owns the private key for a by asserting fact (owns, ⟨0, a−1 ⟩).
    Each protocol includes a small collection of rules. A rule is a sentence in
the goal language presented in Section C.1. A rule is an axiom added to a
protocol. cpsa uses the axiom as a rewrite rule to derive zero or more new
skeletons from a skeleton produced during a cohort step.





Bibliography

[1] Franz Baader and Tobias Nipkow. Term Rewriting and All That. Cam-
    bridge University Press, 1998.
[2] Franz Baader and Wayne Snyder. Unification theory. In Alan Robin-
    son and Andrei Voronkov, editors, Handbook of Automated Reasoning,
    volume 1, chapter 8. The MIT Press, 2001. https://www.cs.bu.edu/
    fac/snyder/publications/UnifChapter.pdf.
[3] George Coker, Joshua Guttman, Peter Loscocco, Amy Herzog, Jonathan
    Millen, Brian O’Hanlon, John Ramsdell, Ariel Segall, Justin Sheehy, and
    Brian Sniffen. Principles of remote attestation. International Journal
    of Information Security, 10:63–81, 2011. 10.1007/s10207-011-0124-7.
[4] Dorothy E. Denning and Giovanni M. Sacco. Timestamps in key distri-
    bution protocols. Communications of the ACM, 24(8):533–536, August
    1981.
[5] Shaddin F. Doghmi, Joshua D. Guttman, and F. Javier Thayer. Search-
    ing for shapes in cryptographic protocols. In Tools and Algorithms
    for Construction and Analysis of Systems (TACAS), number 4424 in
    LNCS, pages 523–538. Springer, March 2007. Extended version at
    http://eprint.iacr.org/2006/435.
[6] Joseph A. Goguen and Jose Meseguer. Order-sorted algebra I: Equa-
    tional deduction for multiple inheritance, overloading, exceptions and
    partial operations. Theoretical Computer Science, 105(2):217–273, 1992.
[7] Joshua D. Guttman. Security theorems via model theory. In Ex-
    press: Expressiveness in Concurrency, Workshop affiliated with Con-
    cur, September 2009. Post-proceedings to appear in EPTCS, http:
    //www.eptcs.org/.


 [8] Joshua D. Guttman. Shapes: Surveying crypto protocol runs. In
     Veronique Cortier and Steve Kremer, editors, Formal Models and Tech-
     niques for Analyzing Security Protocols, volume 5 of Cryptology and
     Information Security Series. IOS Press, 2011.

 [9] Moses Liskov and John D. Ramsdell. Implementing strand space al-
     gebras. http://www.ccs.neu.edu/home/ramsdell/papers/algimpl.
     pdf, 2011.

[10] Moses D. Liskov, Paul D. Rowe, and F. Javier Thayer. Completeness of
     CPSA. Technical Report MTR110479, The MITRE Corporation, 2011.

[11] John D. Ramsdell. Deducing security goals from shape analysis sen-
     tences. The MITRE Corporation, April 2012. http://arxiv.org/abs/
     1204.0480.

[12] John D. Ramsdell and Joshua D. Guttman. CPSA Design. The MITRE
     Corporation, 2009. In https://github.com/mitre/cpsaexp source dis-
     tribution, doc directory.

[13] John D. Ramsdell and Joshua D. Guttman. CPSA Primer. The MITRE
     Corporation, 2009. In https://github.com/mitre/cpsaexp source dis-
     tribution, doc directory.





Index

acquired, 10                          escape set, 39
ancestors, 36                         event, 9
atoms, 5                              evt, 10
authenticated channel, 10
authentication test, 40               fact term, 59
avoidance set, 33                     forgetting, 47

base sorts, 3                         gained, 10
buildable, 34                         hash, 5, 40
bundle, 10                            homomorphism
carpos, 6                                 algebra, 5
carried positions, 6                      nodewise isomorphic, 17
carried only within, 36                   preskeleton, 16
carried positions, 36                     strandwise injective, 17
carries, 6                            hulled preskeleton, 28
channel message, 6                    inherited origination assumptions, 11
channel test, 40                      instance, 21
cohort, 41                            inverse key, 5
communication, 10                     isomorphic preskeletons, 17
confidential channel, 10
contraction, 41                       listener augmentation, 41
cows, 37                              listener role, 17
critical position, 39                 locations, 7

deletion, 47                          more general substitution, 5
derivable before, 33                  msg, 10
displacement, 41
domain, 5                             nodes, 10
                                      nodewise isomorphic homomorphism,
effectively equivalent strands, 29            17
encryption test, 40                   non-originating, 10


   penetrator, 51                      thinned, 28
nonce test, 40                    solved critical position, 40
normal form, 24                   sorts, 3
                                  strand, 9
occurs in, 6                      strand space, 10
operations, 3                     strand succession, 10
operators, 26                     strandwise injective homomorphism,
originates, 9                              17
parameters, 54                    strict partial order, 10
partial order                     substitution, 5
    strict, 10                    target messages, 40
penetrator non-originating, 51    thinned skeleton, 28
points, 7                         thinning, 28
position, 5                       trace, 9
preskeleton, 15                   transforming event, 42
    hulled, 28                    tskel , 30
preskeleton homomorphism, 16
preskeletons                      unify, 36
    isomorphic, 17                uniquely originates, 10
protectors, 39
protocol, 11                      variable separation, 47
public messages, 33               variable set, 3
                                  Vars, 11
range, 5
realized skeleton, 15, 17         weakening, 47
regular strand, 13
regular augmentation, 41
role, 11
run of protocol, 11

sent channel messages, 33
sequence, 2
setwise reduction system, 24
shape, 46
shape analysis sentence, 55
skel , 30
skeleton, 16
     realized, 15, 17

