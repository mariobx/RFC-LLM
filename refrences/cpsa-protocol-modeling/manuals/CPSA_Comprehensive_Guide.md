# Comprehensive Guide to CPSA Modeling

Approved for Public Release; Distribution Unlimited
Case # 12-0038




                       MTR110479
                       MITRE TECHNICAL REPORT


                       Completeness of CPSA



                       October 2011

                       Moses D. Liskov
                       Paul D. Rowe
                       F. Javier Thayer




                       Sponsor:       NSA/R2D            Contract No.:    W15P7T-12-C-F600
                       Dept. No.:     G020               Project No.:     0712N60B



                       The views, opinions and/or findings contained in       This document was prepared for authorized
                       this report are those of The MITRE Corporation         distribution only. It has not been approved
                       and should not be construed as an official             for public release.
                       Government position, policy, or decision, unless
                       designated by other documentation.

                        c 2011 The MITRE Corporation. All Rights Reserved.




                       Center for Integrated Intelligence Systems
                       Bedford, Massachusetts

                                Abstract

The Cryptographic Protocol Shapes Analyzer (cpsa) is a program for au-
tomatically characterizing the possible executions of a protocol compatible
with a specified partial execution. This paper presents a mathematically
rigorous theory that backs up the implementation of cpsa in Haskell, and
proves the algorithm produces characterizations that are complete, and that
the algorithm enumerates these characterizations.

Contents

## 1 Introduction                                                                 3

  1.1 Previous and Related Work . . . . . . . . . . . . . . . . . . .          3
  1.2 Document structure . . . . . . . . . . . . . . . . . . . . . . . .       4


## 2 Preliminaries                                                                5

  2.1 Basic Cryptoalgebra . . . . . . . . . . . . . . . . . . . . . . .        5
  2.2 Path Viewpoint . . . . . . . . . . . . . . . . . . . . . . . . . .       5


## 3 Upward and Downward Closure                                             7

  3.1 Closure Properties . . . . . . . . . . . . . . . . . . . . . . . . 10


## 4 Critical Path                                                               14



## 5 Fragments                                                                   18



## 6 Protocols                                                               21

  6.1 Roles and Protocols . . . . . . . . . . . . . . . . . . . . . . . . 22


## 7 Skeletons                                                                   24

  7.1 Preskeletons . . . . . . . . . . . . . . . . . . . . . . . . . . . .    27
  7.2 Hierarchies and Commitments . . . . . . . . . . . . . . . . . .         28
      7.2.1 Assignment Committed Protoskeletons . . . . . . . . .             29
      7.2.2 Listener Committed Protoskeletons . . . . . . . . . . .           30
  7.3 Diagrams . . . . . . . . . . . . . . . . . . . . . . . . . . . . .      31
  7.4 Preservation Properties . . . . . . . . . . . . . . . . . . . . . .     32
  7.5 Coverage . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    33


## 8 Operators                                                                   34

  8.1 Suites . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    36
  8.2 Filters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   36
  8.3 Primitive Operators . . . . . . . . . . . . . . . . . . . . . . . .     36


## 9 Suites and the Setwise Reduction                                            41

  9.1 The Pre-Cohort Suite . . . . . . . . . . . . . . . . . . . . . . .      42
  9.2 The Skeletonization Suite . . . . . . . . . . . . . . . . . . . .       44
  9.3 Post-Processing Filters . . . . . . . . . . . . . . . . . . . . . .     46
  9.4 The Cohort and the CPSA Set Reduction . . . . . . . . . . .             47




## 10 Suite Completeness                                                    48

   10.1 Top-level Completeness Proof . . . . . . . . . . . . . . . . . . 53


## 11 Skeletonization                                                             55



## 12 Pre-Cohort Completeness                                                     63

   12.1 Preliminaries . . . . . . . . . . . . . . . . . . . . . . . . . . .    63
   12.2 Contractions . . . . . . . . . . . . . . . . . . . . . . . . . . . .   64
   12.3 Listener Augmentation . . . . . . . . . . . . . . . . . . . . . .      65
   12.4 Regular Augmentation . . . . . . . . . . . . . . . . . . . . . .       68
   12.5 Exhaustivity of the Cases . . . . . . . . . . . . . . . . . . . .      70
   12.6 Proof of Lemma 10.11 . . . . . . . . . . . . . . . . . . . . . .       76


## 13 Enumerability                                                               77


A The cowt Algorithm                                                           82






## 1     Introduction

The Cryptographic Protocol Shapes Analyzer (cpsa) is a program for au-
tomatically characterizing the possible executions of a protocol compatible
with a specified partial execution [17]. The purpose of this document is to
present a mathematically rigorous theory that backs up the implementation
of cpsa in Haskell, and prove the algorithm produces characterizations that
are complete, and that the algorithm enumerates these characterizations.


### 1.1    Previous and Related Work

cpsa is the result of a line of research on the formal analysis of security
protocols, typically traced to seminal work of Dolev and Yao [12]. Formal
analysis of security protocols treats cryptographic tools such as encryption
and digital signatures as abstractions, and thus reduces the problem of an-
alyzing a security protocol to a simpler task. Meadows [16] and Lowe [15]
showed that automatic tools for analysis of security protocols are both prac-
tical and effective. Numerous tools have been developed since for automated
protocol analysis [15, 4, 6, 5, 1, 21, 3, 2, 8, 13].
    The cryptographic protocol shapes analyzer is unusual among these tools
because it aims to give a complete characterization of possible executions,
independent of any specific security property to confirm or contradict. cpsa
is an automated tool that aims at complete characterization, and works with
Strand Space theory [20, 14]. Its structure is described in [9, 11], and the al-
gorithm is more fully specified in [18]. However, no full proof of the algorithm
has been given until now.
    It is worth noting a few of the similarities and differences from one tool
in particular named Scyther [8, 7], created by Cas Cremers. We highlight
this tool due to its close similarity to cpsa. Scyther’s algorithm is based on
the algorithm used in Avispa [1] and also aims to produce complete char-
acterizations of protocols. It is also based on the theory of Strand Spaces,
although its semantics is not quite identical to that of cpsa. Scyther’s char-
acterizations are sensitive to certain types of adversarial actions, and so these
actions are explicitly included in the output, while cpsa focuses solely on the
projection of executions onto the regular participants. This difference also
manifests itself in the algorithms used by the two tools. In choosing to have
characterizations that are insensitive to which adversary actions are used,
cpsa must base its algorithm on so-called “authentication tests” [10]. This


appears to add noticeable complexity to the proof of completeness. There
has been no systematic comparison of these tools with regard to their per-
formance and expressibility; nor have there been any studies to compare the
similarities and differences between the characterizations that the two tools
output.


### 1.2    Document structure

In sections 2, 3, 4, and 5, we describe the formal algebra used to model mes-
sages in our protocols and the capabilities of the adversary, and develop some
key definitions and reasoning that support the algorithmic design of cpsa.
We are mainly concerned with the notion of derivability, specifically, given a
message, can the adversary derive it from available messages, and if not, why
not? The main result of importance to the proof is the development of the
definitions of an escape set and a critical path, and the relationship between
escape sets, critical paths, and derivability, which we prove in Theorem 4.11.
    In sections 6, and 7, we describe our mathematical notion of a protocol
and its roles, and describe skeletons, which capture our idea of a (possibly
partial) protocol execution. We also describe homomorphisms, maps from
one skeleton to another, that indicate that the target is an extension of
the source as a partial execution. This makes it possible for us to describe
coverage and to formally explain the goal of the cpsa algorithm.
    In sections 8, and 9, we give a mathematical theory of operators (trans-
formative operations on skeletons) and suites in order to define the cohort
suite, the main algorithmic operation of cpsa. We also define the overall
algorithm of cpsa.
    In sections 10, 11, 12, and 13, we formally state and prove the top-level
theorems about cpsa we wish to establish: Theorem 10.17, which proves
that cpsa gives a complete characterization of its input, and Theorem 13.1,
which proves that our algorithm enumerates normal characterizations of any
input.






## 2     Preliminaries


### 2.1    Basic Cryptoalgebra

We use a message algebra called the Basic Cryptoalgebra which is the main
algebra used by cpsa.

                                Sorts
        Sorts:       name, text, data, skey, akey < mesg
        Base sorts: name, text, data, skey, akey
                              Operations
        {| · |}(·)   mesg × mesg → mesg Encryption
        (·, ·)       mesg × mesg → mesg Pairing
        K(·)         name → akey           Public key of name
            −1
        (·)          akey → akey           Inverse of key
        ltk(·, ·)    name × name → skey
                              Constants
        T ags        mesg                  Tag constants
                              Equations
        (a−1 )−1 = a a : akey

The base sorts are pairwise disjoint. Given a set X of generators AX is the
free cryptoalgebra generated by X. The set elements of sort base is denoted
BX .
            B = Askey ∪ Aakey ∪ Aname ∪ Atext ∪ Adata                   (1)
Elements of B are called atoms in the cpsa Theory paper. The set B
consists of those terms which are not pairs, not encryptions, not variables of
sort message and not tags.
    End(A) is the set of homomorphisms A −→ A. There is a bijective
correspondence between elements of End(A) and mappings X −→ A. If
σ ∈ End(A), s-dom σ is the set of variables that are not fixed by σ.


### 2.2    Path Viewpoint

A position π is a finite sequence of whole numbers. We write π a π 0 to indicate
the concatenation of sequences π and π 0 . When π 0 is a prefix of π, we write
(π − π 0 ) to indicate the unique sequence π 00 such that π 0 a π 00 = π.



   The term in t that occurs at π, written t @ π, is:
                   t @ hi = t;
                   (t1 , t2 ) @ hii a π = ti @ π for i ∈ {1, 2};
                   {|t1 |}t2 @ hii a π = ti @ π for i ∈ {1, 2};
                   t−1 @ h1i a π = t @ π.
All references to terms are considered in A. A term t occurs in term t0 if
t = t0 @ p for some p.
    We consider the elements of A as a directed graph with labeled nodes
                a
and arrows; t → s where t, s ∈ A if and only if t @ hai = s, where a ∈ {1, 2}.
Given a term t, the set of paths p from t is denoted by Path(t).
Remark 2.1. A position π determines a path in the parse tree of a term t.
We can associate to each path from t a position π and conversely positions π
in a term t determines a path from t. For compatibility with cpsa notation
we identify a path p from t with a pair (t, π) where π is a position in t. For
any prefix ρ of position π, t @ ρ is a node on the path. We will use similar
terminology for paths and positions. For example, a prefix of a path (t, π) is
a path (t, ρ) where ρ is a prefix of π. If p is a path from t, then t @ p is the
endpoint of the path p. the free algebra.
  1. A path p = (t, π) traverses a term a if t @ ρ = a for some proper prefix
     ρ of π. As a particular case of this, note that any non-null path from
     t traverses t.
  2. A path p = (t, π) terminates at a if t @ π = a. Alternative phrases are
     p leads from t to a or a is an endpoint of p.
  3. A path p visits a if p traverses a or terminates at a.
  4. A path p = (t, π) in t traverses the i-th position of a function symbol
     f of arity n ≥ i if for some position ρ, t @ ρ is a term with constructor
     f and ρ a hii is a prefix of π. Cases of interest are plaintext edges and
     key edges of encryptions and key inverse.
  5. A path p is carried if it does not traverse any key edge or any inverse
     edge. The set of carried paths at t is denoted CarPath(t).
  6. A term a is reachable from t if some path leads from t to a; a is reachable
     by a carried path if there is a carried path that leads from t to a. In
     other words, a occurs in t if it is reachable from t, and a is carried by t
     if it is reachable from t via a carried path.



## 3     Upward and Downward Closure

Remarks 3.1 (Notational). Destructuring is either one of the two operations
which map a pair (a, b) into its components. If a is a term,
                                 −1
                                 a    if a : akey
                     inv(a) =      a   if a ∈
                                            / Xmesg                     (2)
                                   ⊥   otherwise.
                                

Decryption with a key u is the operation {|a|}u 7→ a. Encryption with a key
u is the operation a 7→ {|a|}u .
    It is convenient to separate the notion of available terms from the notion
of the context, which is a set of keys that may be used in derivations. We
will use calligraphic fonts S to emphasize that a set of terms is regarded as
a context.
Definition 3.2. Suppose S is a set of terms regarded as a cryptographic
context. A carried path p is S-decryptable if the only encryptions that p
traverses are of the form {|b|}u where inv(u) ∈ S. A carried path p is S-
encryptable if the only encryptions p traverses are of the form {|b|}u where
u ∈ S.
   An S-decryptable path may terminate at an encryption {|b|}u with
inv(u) ∈
       / S.
Definition 3.3. A maximal S-decryptable carried path is an S-decryptable
carried path p which is not a proper prefix of an S-decryptable carried path.
Completely analogously, we can define a maximal S-encryptable carried path.
Remark 3.4. Clearly an S-decryptable carried path p is maximal (in the set
of S-decryptable carried paths) if and only if it terminates at an encryption
{|b|}u with inv(u) ∈
                   / S or terminates at a term which is not an encryption and
not a pair. Similarly an S-encryptable carried path p is maximal (in the set
of S-encryptable carried paths) if and only if it terminates at an encryption
{|b|}u with u ∈
              / S or terminates at a term which is not an encryption and not
a pair.
Remark 3.5. For a carried path p from t exactly one of the following alter-
natives must hold:
    1. p is a maximal S-decryptable carried path from t.


  2. A proper prefix of p is a maximal S-decryptable carried path from t.
     This will be the case if and only if p is not S-decryptable.

  3. p is a proper prefix of a maximal S-decryptable carried path from t.

There is a corresponding version of the above assertion with “S-decryptable”
replaced by “S-encryptable”.
Remark 3.6. The maximal S-decryptable prefix of a path p from t if it exists
is unique. This is immediate since the set of prefixes of p is totally ordered.
However p may have more than one maximal S-decryptable extension. The
same remark holds if “S-decryptable” is replaced with “S-encryptable”.
Remark 3.7. If a carried path p terminates at a term c such that c is either
an encryption {|b|}u with inv(u) ∈/ S or c is not an encryption and not a pair,
then p has no proper extensions which are S-decryptable carried paths. In
this case some prefix of p (possibly hi or p itself) is a maximal S-decryptable
carried path from t. In the other direction, if p is an S-decryptable carried
path that has no proper extensions which are S-decryptable carried paths,
then p terminates at a term c such that c is either an encryption {|b|}u with
inv(u) ∈/ S or c is not an encryption and not a pair. Again there is a corre-
sponding statement for maximal S-encryptable carried path: It terminates
at a term c such that c is either an encryption {|b|}u with u ∈  / S or c is not
an encryption and not a pair.
   First we adapt some terminology which is more-or-less standard in the
context of paths and graphs: If p is a path, t a term and L a set of terms such
that p visits an element of L, the first L-visit prefix of p at t is the minimal
prefix of p which visits an element of L.

Definition 3.8. Given a set L of terms, the depth of L relative to a term
a, denoted depth(L, S, a), is the supremum over all maximal S-encryptable
carried paths p from a of the length of the first L-visit prefix of p. By conven-
tion, if there is a maximal S-encryptable carried path which does not visit
L, then depth(L, S, a) = +∞.
    A set L is an S-support for a if depth(L, S, a) < ∞. Alternative phrase:
a is S-supported by L.

Remark 3.9. For every term a, {a} is an S-support of a. Clearly a is S-
supported by L if and only if every maximal S-encryptable carried path
visits L.


Definition 3.10. Let P and S be sets of terms, where we regard S as a
context. The S-downclosure of P denoted Cl↓ (P, S) consists of those terms
a which are endpoints of an S-decryptable carried path beginning at some
element of P . The S-upclosure of P denoted Cl↑ (P, S) consists of those
terms a which are S-supported by P .
    The S-frontier of P denoted Fr(P, S) consists of those terms which are
endpoints of a maximal S-decryptable carried path beginning at some element
of P .

Remark 3.11. Taking the contrapositive of Definition 3.10, a ∈ / Cl↓ (P, S) if
and only if there is no S-decryptable carried path starting at an element of
P that reaches a.
   Equivalently,

Lemma 3.12. a ∈  / Cl↓ (P, S) if and only if every carried path from an element
of P to a traverses Fr(P, S).

Proof. Suppose a ∈/ Cl↓ (P, S) and p is a path from t to a. By Definition 3.10,
p is not S-decryptable, and therefore has a proper prefix q which is maximal
S-decryptable. The endpoint eq of the path q is an element of Fr(P, S)
and clearly p traverses eq . Conversely, if a ∈ Cl↓ (P, S) then there is an S-
decryptable path p from an element of P to a. Every encryption c traversed
by p is S-decryptable and therefore by Remark 3.4, no such c can be the
endpoint of a maximal S-decryptable path from anywhere. Therefore no such
c can be an element of Fr(P, S). Thus p traverses no element of Fr(P, S).
Remark 3.13. In other words, Lemma 3.12 asserts that a ∈     / Cl↓ (P, S) if and
only for all t ∈ P , a is carried in t only within Fr(P, S). Some elements of
Fr(P, S) may not carry a at all.

Remark 3.14. By Remark 3.4 any element in Fr(P, S) is either an encryption
of the form {|b|}u with inv(u) ∈
                               / S or is not an encryption and not a pair or
equivalently, either an encryption or an atom. Every element of Cl↓ (P, S) is
visited by an S-decryptable path starting at some element of P .
   The frontier has a boundary-like property:

Proposition 3.15. If t ∈ Cl↓ (P, S), a ∈
                                       / Cl↓ (P, S) and p is a path from t to
a then p traverses Fr(P, S).




                                                             P




                                                             Encryptions {|b|}u , inv(u) ∈ S




      Encryptions {|b|}u , inv(u) ∈
                                  /S                                 Fr(P, S)




                                Figure 1: Frontier

Proof. By Definition 3.10, there is an S-decryptable path r from some ele-
ment of P to t. Now consider the path r a p. Again by Definition 3.10, r a p
is not S-decryptable. Therefore r a p has a proper maximal S-decryptable
prefix q. However q must be an extension of r, possibly r itself. Moreover,
the endpoint eq of q is an element of the frontier Fr(P, S) and an element of
Cl↓ (P, S). Since r a p is a path from an element of P to a, eq is an element of
Fr(P, S). It follows that p visits eq ∈ Fr(P, S) as claimed and since a 6= eq , p
traverses eq .


### 3.1    Closure Properties

A set Z of terms is derivational if it is closed under pairing, encryption with
a key u such that u ∈ Z, destructuring and decryption with a key u such that
inv(u) ∈ Z. The smallest derivational set containing P is denoted D(P ).
    A set Z of terms is S-constructive if and only if it is closed under pairing
and encryption with a key u such that u ∈ S. A set Z is S-deconstructive
if and only if it is closed under destructuring and decryption with a key
u such that inv(u) ∈ S. A set Z is S-derivational if and only if it is S-
constructive and S-deconstructive. The smallest S-derivational set contain-
ing P is D(P, S).
    We can characterize these sets in terms of the path heuristic.


                        P




                                                    r
                                                        t ∈ Cl↓ (P, S)




                                                q
                                        eq



                                 rap
                                            p

                                        / Cl↓ (P, S)
                                       a∈



            Figure 2: Frontier as a Boundary (Proposition 3.15)

Lemma 3.16. A set Z is S-deconstructive if and only if every term a which
is the endpoint of an S-decryptable carried path p from t ∈ Z, is also an
element of Z.

Proof. Suppose Z is S-deconstructive. We show that if a term a is reachable
from t ∈ Z by an S-decryptable carried path p, then a ∈ Z. We use induction
on the length of the path p. If p has length 0, then p = hi and a = t ∈ Z.
Suppose the claim is true for all carried paths of length n and p has length
n + 1. Then p = q a hai where q has length n. q is an S-decryptable carried
path and therefore by the induction hypothesis t @ q ∈ Z. If t @ q is an
encryption {|b|}u , then by the assumption p is S-decryptable, inv(u) ∈ S.
Since Z is S-deconstructive, t @ p = b ∈ Z. If t @ q is a pair (x, y) then both
x, y ∈ Z and t @ p is either x or y.
    Suppose that every a reachable from t ∈ Z by an S-decryptable carried
path p is an element of Z. If a = (x, y) then x and y are reachable from
t by the carried paths p a h1i, p a h2i and therefore x, y ∈ Z. If a = {|b|}u


with inv(u) ∈ S, then p a h1i is an S-decryptable path so b ∈ Z. Thus Z is
S-deconstructive.
   There is an analogous statement, Lemma 3.17, for S-constructive sets,
but this requires the notion of support.

Lemma 3.17. A set Z is S-constructive if and only if every term t which is
S-supported by Z is an element of Z.

Proof. Suppose Z is S-constructive. We show that for every integer n ≥ 0,
if depth(Z, S, t) ≤ n, then t ∈ Z. We use induction on n. If n = 0, then
t ∈ Z and {t} is an S-support set for t. Suppose the assertion holds for n − 1
and depth(Z, S, t) = n ≥ 1. In particular, t is either a pair or an encryption.
If t = (x, y) then depth(Z, S, x) ≤ n − 1 and similarly for y. Thus x ∈ Z
and y ∈ Z by the induction hypothesis. Since Z is S-constructive, t ∈ Z.
If t = {|b|}u with u ∈ S, then depth(Z, S, b) ≤ n − 1. By the inductive
hypothesis b ∈ Z. Since Z is S-constructive, t ∈ Z.
    Conversely, if every t which is S-supported by Z is an element of Z it is
straightforward to show Z is constructive.

Corollary 3.18. The smallest S-constructive set containing P is the set of
terms t which are S-supported by P .

Proposition 3.19. Cl↓ (P, S) is the smallest S-deconstructive set containing
P.

Proof. Let Z be the smallest S-deconstructive set containing P . By
Lemma 3.16, Cl↓ (P, S) is S-deconstructive. Since Cl↓ (P, S) ⊇ P , it fol-
lows that Z ⊆ Cl↓ (P, S). Po prove the converse, by definition Z is S-
deconstructive and so by Lemma 3.16 if t ∈ Z and p is an S-decryptable
carried path from t then t@p ∈ Z. Since P ⊆ Z, it follows Z ⊇ Cl↓ (P, S).
   Analogously, applying Lemma 3.17,

Proposition 3.20. Cl↑ (P, S) is the smallest S-constructive set containing
P.

Lemma 3.21. If Z is S-deconstructive, then Cl↑ (Z, S) is S-deconstructive.





                                   t ∈ Cl↑ (Z, S)




                              p

                              ep


                                                          qi = p a qi0
                                                    qi0
                     Z




             Figure 3: Cl↑ (Z.S) is S-deconstructive (Case (2))

Proof. By Lemma 3.16, it suffices to show that the endpoint of every carried
S-decryptable path from t ∈ Cl↑ (Z, S) is also in Cl↑ (Z, S). Let p be an S-
decryptable path from t ∈ Cl↑ (Z, S) with endpoint ep . By the S-encryptable
version of Remark 3.5, one of two things must hold for p: (1) there is a
maximal S-encryptable path q which is a (not necessarily proper) prefix of
p, or (2) p has maximal S-encryptable proper extensions. Let q1 , . . . , q` be
all the maximal S-encryptable extensions.
    Consider case (1). By Corollary 3.18 and Proposition 3.20, every element
of Cl↑ (Z, S) is S-supported by Z, and so some prefix q 0 of q terminates in an
element of Z. Thus we can write p = q 0 a q 00 where q 00 is an S-decryptable
path from an element of Z to ep . Since Z is S-deconstructive, ep ∈ Cl↑ (Z, S).
    In case (2), we can write qi = p a qi0 for each 1 ≤ i ≤ ` where each qi0 is
a maximal S-encryptable path starting at ep . Again, since Cl↑ (Z, S) is S-
supported by Z, we know that each qi visits an element of Z. If this happens
with some q 0 which is a prefix of p, then we can argue as we did in case
(1) that ep must be in Cl↑ (Z, S). Otherwise, we are guaranteed that each qi0
visits an element of Z. Since these qi are the maximal S-encryptable paths
of ep , we know ep is S-supported by Z. By Lemma 3.17 ep ∈ Cl↑ (Z, S).
   The previous results immediately yield:

Proposition 3.22. D(P, S) = Cl↑ (Cl↓ (P, S), S).


   In particular, by the characterization of the S-upclosure of a set given by
Proposition 3.20:

Corollary 3.23. A necessary and sufficient condition t ∈ D(P, S) is that t
be S-supported by some subset of Cl↓ (P, S).

Corollary 3.24. A necessary and sufficient condition t ∈ D(P, S) is that
every maximal S-encryptable path p beginning at t visit some element of
Cl↓ (P, S).

Proof. Apply Remark 3.9 and Corollary 3.23.
   Corollary 3.24 leads to the notion of essential obstruction and critical
path in the next section.

Proposition 3.25. Suppose t ∈ D(P, S), p is a path from t to a and either
(i) a = {|b|}u with u ∈
                      / S or (ii) a is not an encryption and not a pair. Then
either p traverses Fr(P, S) or a ∈ Cl↓ (P, S).

Proof. Consider case (i): Suppose a ∈     / Cl↓ (P, S). Since u ∈   / S, by Re-
mark 3.7, the path p is has a maximal S-encryptable prefix (possibly p it-
self.) By Corollary 3.24, that prefix must visit some element b of Cl↓ (P, S);
                                  / Cl↓ (P, S), it is in fact a proper prefix q of
in particular p visits b. Since a ∈
p that visits b. Let r be the remnant of p after q. r is a path from b to a. By
Proposition 3.15, r traverses Fr(P, S).
    In case (ii) the argument is identical, since the only fact used was that
the path p is has a maximal S-encryptable prefix.



## 4     Critical Path

Definition 4.1. An essential obstruction of t relative to P, S is a maximal
S-encryptable path beginning at t which does not visit an element of Cl↓ (P, S).

    The set of essential obstructions is denoted Eob(P, S, t).
Remark 4.2. The content of Corollary 3.24 is that t ∈ D(P, S) if and only if
Eob(P, S, t) = ∅.
    For the cpsa search algorithm, in particular for its notion of “progress”
the set of essential obstructions is too small. This leads to the notion of
critical path.


                                        t
                 Eob(P, S, t)




                           Cl↓ (P, S)




                         Figure 4: Essential Obstruction

Definition 4.3. Let p ∈ CarPath(t) have endpoint ep . p is critical relative
to P, S if and only (1) ep is an encryption {|b|}u with u ∈/ S or an element
which is not a pair and not an encryption (2) ep ∈ / Cl↓ (P, S) and (3) p does
not visit Fr(P, S).

   The set of critical paths is denoted CritPath(P, S, t).

Proposition 4.4. Let p ∈ CarPath(t) have endpoint ep . A necessary and
sufficient condition for p to be critical relative to P, S is that (A) ep is an
encryption {|b|}u with u ∈/ S or an element which is not a pair and not an
encryption, (B) p does not visit an element of Cl↓ (P, S).

Proof. Conditions (1) of Definition 4.3 and (A) are identical. Now suppose
p ∈ CarPath(t) is such that (1) holds. Then properties (2) and (3) of Def-
inition 4.3 are equivalent to (B): In one direction, suppose (B) holds, that
is, p does not visit Cl↓ (P, S). Since p visits ep , it follows that ep ∈
                                                                        / Cl↓ (P, S)
                                            ↓
which is (2). By definition Fr(P, S) ⊆ Cl (P, S), and therefore p cannot visit
any element of Fr(P, S) proving (3). In the other direction, suppose (2) and
(3) hold, but p visits a ∈ Cl↓ (P, S). Now a 6= ep , for otherwise p is a maximal
S-encryptable path from an element of P to a (by Remark 3.7) and therefore
ep = a ∈ Fr(P, S) ⊆ Cl↓ (P, S) which contradicts (2). Otherwise, let q be
the remnant of p from a. By the boundary property of Fr(P, S) (Proposi-



tion 3.15), q visits an element of Fr(P, S). Therefore p visits an element of
Fr(P, S) which contradicts (3).
Remark 4.5. Any essential obstruction is a critical path. Proof: By the
version of Remark 3.7 for S-encryptable paths, any essential obstruction
satisfies (A) of Proposition 4.4. (B) is part of the definition of essential
obstruction.
Remark 4.6. If p ∈ CritPath(P, S, t), by Remark 3.6 p has a unique maximal
S-encryptable prefix µ(p). Since p does not visit Cl↓ (P, S), no prefix of p
can visit Cl↓ (P, S). In particular, µ(p) ∈ Eob(P, S, t). Now Eob(P, S, t) ⊆
CritPath(P, S, t) and µ is the identity on Eob(P, S, t) and the mapping µ :
CritPath(P, S, t) −→ Eob(P, S, t) is the identity on Eob(P, S, t).

Proposition 4.7. A necessary and sufficient condition t ∈ D(P, S) is that

                            CritPath(P, S, t) = ∅.                        (3)

Proof. Consider the map µ : CritPath(P, S, t) −→ Eob(P, S, t) defined in Re-
mark 4.6. The map µ is surjective and therefore CritPath(P, S, t) 6= ∅ ⇐⇒
Eob(P, S, t) 6= ∅. The result now follows by Remark 4.2.

Definition 4.8. The escape set of a relative to P, S, denoted Esc(P, S, a) is
the union of the set of those elements of Fr(P, S) which carry a with the set
{a} if a ∈ Cl↓ (P, S).

Remark 4.9. By Remark 3.14, every element of Esc(P, S, a) other than a is
either an encryption or an atom.

Proposition 4.10. If p ∈ CarPath(t) with endpoint ep and p                 ∈
CritPath(P, S, t), then the following conditions hold:

  1. p does not visit Esc(P, S, ep ).

  2. Every path from an element of P to ep visits Esc(P, S, ep ).

  3. For every encryption {|b|}u ∈ Esc(P, S, ep ), inv(u) ∈
                                                          / S.

  4. If ep is an encryption {|b|}u , then u ∈
                                            / S.





Proof. Suppose p ∈ CritPath(P, S, t). By Definition 4.3, p does not
visit Fr(P, S). Moreover, also by Definition 4.3, ep ∈    / Cl↓ (P, S). Thus
Esc(P, S, ep ) ⊆ Fr(P, S) by the Definition 4.8 of escape set. This proves (1).
Since ep ∈/ Cl↓ (P, S), any path from P to ep must traverse some element
d ∈ Fr(P, S) by the boundary property of the frontier (Proposition 3.15). d
carries ep and therefore d ∈ Esc(P, S, ep ). This proves (2). Property (3) is
immediate from the definition of frontier. Finally Property (4) follows from
the definition of critical path.


Theorem 4.11. Suppose p ∈ CarPath(t) with endpoint ep and E ⊆ A con-
sists of encryptions or atoms. If p ∈
                                    / CritPath(P, S, t), then one of the fol-
lowing conditions holds:
  1. p visits E.

  2. There is a path from an element of P to ep which does not visit E.

  3. For some {|b|}u ∈ E, inv(u) ∈ S.

  4. ep is an encryption {|b|}u with u ∈ S.
Proof. Since p ∈/ CritPath(P, S, t), by taking the contrapositive of Proposi-
tion 4.4, we conclude that the one of the following must hold:
 (A) It is not the case that ep is an encryption of the form {|b|}u with u ∈
                                                                           /S
     and ep is not an atom.

 (B) p visits an element of Cl↓ (P, S, t).

    Case (A) is equivalent to: ep is an encryption of the form {|b|}u with
u ∈ S. Thus in case (A), condition (4) of the Lemma holds. Thus we may
henceforth assume that (A) fails and (B) holds. In particular, p visits an
element d of Cl↓ (P, S, t). Let q be the remnant of p starting at d, and let r
be an S-decryptable path from an element of P to d. In this case one of the
following statements holds:
 (a) p visits E

 (b) r visits E

 (c) Neither p nor r visit E


                                                                  aF 0
                                      PF 0




                                                   r
             SF 0 -decryptable path
                                                        d ∈ Cl↓ (F 0 )

                                             q     p0


                                             e0p


                       Figure 5: Case (B) of Lemma 5.6

In case (a), this is simply Condition (1) of the lemma. If (a) case does not
hold but (b) does hold, then we conclude that r traverses an element x ∈ E,
for if r terminated at x, then p would visit E contrary to the assumption that
(a) does not hold. By hypothesis, x is either an encryption or atom, but x
cannot be an atom since no path can traverse an atom. Thus x is of the form
{|c|}v . Since r is S-decryptable, inv(v) ∈ S, thereby meeting Condition (3)
of the lemma. In case (c), the carried path r_ q is a path from P to ep which
does not visit E, thereby satisfying Condition (2) of the lemma.



## 5    Fragments

So far we have considered derivability in the basic cryptoalgebra setting. This
section introduces a further refinement in which the available messages and
the context are determined by other considerations which occur naturally in
the setting of a protocol execution. In the section on the adversary model,
it is explained why the penetrator cannot use terms in the what is called the
exclusion set. Recall that B = Askey ∪ Aakey ∪ Aname ∪ Atext ∪ Adata



Definition 5.1. A fragment consists of a tuple F = (T, X, a) where X ⊆ B
and a is a term. The X in a fragment is called the exclusion set. The set of
public messages at F is

                     PF = T ∪ (B \ X) ∪ Xmesg ∪ Tags .                      (4)

The encryption context at F is SF = D(PF ). If F is an fragment, TF , XF ,
and aF are the components of F.

Definition 5.2. The critical pathset of a fragment F is the set CritPath(F) =
CritPath(PF , SF , aF ). The critical pathset at F is denoted CritPath(F). The
escape set of a term a in F is Esc(F, a) = Esc(PF , SF , a). Similar conven-
tions apply to the sets Cl↑ , Cl↓ ,

Remark 5.3. By virtue of (4), Xmesg ∪ Tags ⊆ Cl↓ (F).
    In the intended interpretation of a fragment for skeletons, U corresponds
to the declared uniquely originating atoms which actually originate in A.

Definition 5.4. If F = (T, X, a), F 0 = (T 0 , X 0 , a0 ) are fragments, a homo-
morphism σ : F −→ F 0 is an algebra homomorphism such that σ(T ) ⊆ T 0 ,
σ(X) ⊆ X 0 , and σ(a) = a0 .

   We now consider possible ways of resolving a critical path.

Definition 5.5 (Critical Path Solved). Suppose F, F 0 are fragments and p
is a critical path with endpoint ep of the term aF at F. Let σ : A −→ A be an
algebra homomorphism. Let E 0 = σ(Esc(F, ep )), p0 = σ(p) and e0p = σ(ep ).
Path p from aF is solved in F 0 by σ, if and only if one of the following
conditions holds:

   • Sol1. p0 visits E 0 .

   • Sol2. There is a carried path from an element of TF 0 to e0p which does
     not visit E 0 .

   • Sol3. For some {|b|}u ∈ E 0 , inv(u) ∈ SF 0 .

   • Sol4. e0p = {|b|}u , and u ∈ SF 0 .

Let Solved(F, p) = {(σ, F 0 ) : σ is a homomorphism A −→ A. and σ solves p in F 0 }



   In words, cpsa makes progress by a contraction (Item 1), where mes-
sages are identified, an augmentation (Item 2), where something is added to
the escape set, or a listener augmentation (Item 3 and Item 4), where an
assumption about the lack of the derivability of a key is shown to be invalid.
                                                         σ
Lemma 5.6. Suppose F, F 0 are fragments and A →− A is an algebra homo-
                                      / CritPath(F 0 ), then σ solves p in
morphism. If p ∈ CritPath(F) and σ(p) ∈
F 0.
Proof. Let ep be the endpoint of p. By Proposition 4.4, ep is either (a) an
encryption of the form {|b|}u with u ∈   / SF or (b) not a pair and not an
encryption. The only possibility for ep in case (b) is ep ∈ B: For by clause
(B) of Proposition 4.4 ep ∈  / Cl↓ (F) and variables Xmesg or Tags are in
Cl↓ (F) by Remark 5.3. Now by Remark 4.9 all elements of Esc(F, ep ) other
than ep are either encryptions or atoms. Therefore all elements of Esc(F, ep )
are either encryptions or atoms.
    Let E 0 = σ(Esc(F, ep )), p0 = σ(p) and e0p = σ(ep ). By the last statement
of the previous paragraph, all elements of E 0 are encryptions or atoms. Now
apply Theorem 4.11.
    When dealing with instantiating variables of sort mesg while inferring
additional honest behavior, cpsa uses the notion of the set of “target terms,”
to keeps its behavior finite. First the set of threshold terms between a term
a and a set of terms S:
Thr(S, a) = {a}∪{t | t carries a, t is a proper carried subterm of some s ∈ S}.
Note that a is always a threshold term regardless of whether a is carried
within some element of a.
Definition 5.7 (Target terms). The set of target terms for a critical path p
with endpoint t in a fragment F is the set Thr(Esc(F, t), t).
Definition 5.8 (Critical Path Weakly Solved). Suppose F, F 0 are fragments
and p is a critical path with endpoint ep of the term aF at F. Let σ : A −→ A
be an algebra homomorphism. Let E 0 = σ(Esc(F, ep )), p0 = σ(p) and e0p =
σ(ep ). Path p from aF is weakly solved in F 0 by σ, if and only if p is solved
in F 0 by σ, or if
   • Sol5. There is an element of Targ(Esc(F 0 , e0p ), e0p )) not in σ(Targ(E, ep )).
   The notion of a path being weakly solved is needed later in the proof of
completeness. Sol5 represents a very weak form of progress, where we have
only improved our set of target terms.



## 6     Protocols

A run of a protocol is viewed as an exchange of messages by a finite set of
local sessions of the protocol.
     An event is either a message transmission or a reception. If m is a mes-
sage, an outbound message event is written as +m, and inbound message
event is written as −m. By abuse of language, if e is an event we will write
−e to signify that e is an inbound event and similarly for outbound events.
A trace in A is a sequence he1 , . . . , en i of message events. The set of traces
over A is denoted CA . A restriction of a trace τ = he1 , . . . , en i is any trace
τ 0 = he1 , . . . , ek i for 1 ≤ k ≤ n. We will also use the phrase t is an extension
of t0 and the notation τ 0 = τ |k. Endomorphisms σ ∈ End(A) act on message
events and traces: σ(±m) = ±σ(m) and σhe1 , . . . , en i = hσ(e1 ), . . . , σ(en )i.
     Traces of the form h−m, +mi where m ∈ A are referred to as listener
traces. The special trace h−x, +xi where x is a variable of sort message
matches any listener trace.


                              t      t        t         = occurs in



                              +t    −t     −t           = carried within




                    Figure 6: Originates, Gained, Acquired

    Let t be a trace, m a message. m originates in t if it is carried by some
event on t and the first event on t in which it is carried is a transmission. m is
gained by t if it is carried by some event t and the first event on t in which it
is carried is a reception; however, this condition allows for prior occurrences
of the message m. m is acquired by t if it first occurs on t in a reception
event and is also carried by that event.






### 6.1    Roles and Protocols

In a run of a protocol, the behavior of each strand is constrained, in a sense
made precise below, by a composite structure called a role. A protorole
over a cryptoalgebra A with atoms B is a structure ρ = (C, N, U ), where
C ∈ CA , N ⊆ B, and U ⊆ B. The trace of the role ρ is C, its non-origination
assumptions are N , and its unique origination assumptions are U . In case of
ambiguity, the components of ρ are denoted (Cρ , Nρ , Uρ ).
Definition 6.1. A protorole ρ = (C, N, U ) is a role if
  1. t ∈ N implies t is not carried in C, and all variables in N occur in C.

  2. t ∈ U implies t originates in C.

  3. If a variable x occurs in C then x is an atom or it is acquired in C.
Equivalently, condition (3) states that a variable x of sort mesg occurs in C
only if it is acquired in C.
  A listener trace is any trace of the form h−m, +mi where m is of sort
mesg.
Remark 6.2. Any role ρ whose trace is h−x, +xi, x a variable of sort mesg,
must have Nρ = Uρ = ∅. However if a role is of the form h−m, +mi where
m is not a variable of sort mesg, then Nρ may be non-empty. For example
h−{|x|}u , +{|x|}u i where u ∈ skey. However, it is always the case that Uρ = ∅,
since nothing originates on a listener trace.
   A listener role is one of the form

                            lsn = (h−x, +xi, ∅, ∅).                         (5)

where x is a variable of sort mesg. This is a legitimate role: (1) and (2) are
vacuous and the variable x is acquired in the trace.
    We introduce a pseudorole £, not a role, which is used as a special anno-
tation for roles of auxiliary traces introduced by the cpsa search algorithm.
This artifice allows us to distinguish between genuine protocol roles which
may behave like listener roles and the roles of these auxiliary traces. However
£ is associated to the listener trace defined previously and accordingly we
introduce the following (somewhat abusive) notation:
   • C£ is the listener trace h−x, +xi where x is a variable of sort mesg.


   • U£ = N£ = ∅.

   Essentially a trace is constrained by a role if it agrees with an instance of
the role restricted up to the length of the trace. The term we will actually
use is role specification which completely determines the trace.

Definition 6.3. A role specification for a trace τ is a structure (ρ, σ) where
σ ∈ End(A) and either (a) ρ is a role or (b) ρ is the pseudorole £, and the
following holds

  1. τ is a restriction of σ(Cρ ) and

  2. s-dom σ is the set of variables that occur in the trace Cρ | len Θ(s)τ .

Remark 6.4. Condition (2) means that the substitution σ transforms pre-
cisely those variables that occur within the role up to the height of the
strand.
   Note that the definition of role specification (ρ, σ) for a trace τ does not
involve origination assumptions. However, the origination assumptions of ρ
are transported onto τ by the substitution σ. First some notation. Given a
σ ∈ End(A) and E ⊆ A, [σ]∗ E is the set

                     {σ(t) : t ∈ E, Vars(t) ⊆ s-dom(σ)}.

Definition 6.5. Suppose τ is a trace and (ρ, σ) is a role specification for τ .
The origination assumptions inherited by τ via (ρ, σ) are

                              N(ρ,σ) = [σ]∗ Nρ ,

and
                                 U(ρ,σ) = σUs ,
where Us are the elements of Uρ that originate on before the event at position
len τ on the role strand Cρ .

Remark 6.6. Since N£ = U£ = ∅, there are no inherited origination assump-
tions for strands with specification £.
    A protocol is a set of roles. Let Vars(P ) be the set of variables that occur
in the traces of the roles in protocol P .





## 7     Skeletons

Fix a protocol P for the remainder of the paper. The details of penetrator
behavior are abstracted away when performing protocol analysis. The ab-
stracted description is called a realized skeleton. To define this and as an
essential tool of analysis we introduce structures with increasing specificity.
In the following A denotes a cryptoalgebra.
     We begin with a general notion which formalizes a notion of collection
of “locally linearly ordered” communication events. A node space is a pair
(I, Θ) where Θ is a map from I to the set of traces over A. Associated to a
node space A = (I, Θ) are the following objects: The nodes of A is the set
of pairs (s, i) where s ∈ I and i ≤ len Θ(s). By abuse of notation we write
(s, i) ∈ A to indicate that (s, i) is a node of A. The elements of the index set
I are the strands of the node space. Nodes (s, i) and (s0 , j) are on the same
strand if s = s0 . The set of variables occurring in the traces of A is denoted
Vars(A). If the variables in Vars(A) are all of base sort, the node space is
instantiated. For any t ∈ A, OA (t) is the set of nodes at which t originates
in A, GA (t) is the set of nodes at which t is gained in A, and CA (t) is the set
of nodes at which t is carried in A. A strand is a node space consisting of a
single strand.
     There is no intrinsic association between a node space A and a protocol
P . However, we can establish such an association by requiring that each
strand of A be constrained by some specified role. Before stating this condi-
tion, we state the blanket variable hygiene condition for protoskeletons and
protocols which we will assume throughout: Vars(P ) ∪ Vars(lsn) is disjoint
from Vars(Θ).
     A P -role assignment for a node space A is a mapping A which associates
to each strand s ∈ I a P -role specification A(s) = (ρs , σs ).
Remark 7.1. By the variable hygiene requirement, Vars(P ) and Vars(Θ) are
disjoint. The substitution σs must affect every variable that occurs within
the role up to the height of the strand.
   A node space may have no P -role assignments or it may have more than
one role assignment.
   Given a node space A and a role assignment A for A, the origination
assumptions inherited by A from P via A are
                           [                [
                     NA =     NA(s) , UA =    UA(s) .
                             s∈I                s∈I



The sets N and U are the declared non-origination terms and uniquely orig-
inating terms of A.

Definition 7.2. Suppose P is a protocol. A protoskeleton for P is a structure
A = (I, Θ, ≺, N, U ), where (I, Θ) is a node space, N ⊆ B, U ⊆ B, and ≺ is
a relation on the nodes of A such that there is a role assignment A with the
following properties:

  1. NA ⊆ N .

  2. UA ⊆ U .

The role assignment A in Definition 7.2 is a protoskeleton validating role
assignment. In contexts where the protocol is understood, we simply refer to
a protoskeleton for P as a protoskeleton. If A is a protoskeleton, IA ,ΘA , ≺A ,
NA , UA are the components of A.

   Protoskeleton validating role assignments for a structure A = (I, Θ, ≺,
N, U ) can be mixed:
Remark 7.3. Note that in general, a P -role specification (ρ, σ) for a strand
need not respect points of origination, that is if t originates at position i on
Cρ |n, σ(t) may originate at some earlier node on σ(Cρ )|n. However, condi-
tion (5) of Definition 7.2 states that a protoskeleton must have at least one
P -role assignment such that all role specifications are origination preserving.

Definition 7.4 (Protomorphism). Let A, B be protoskeletons. A protomor-
phism from A to B is a pair λ = (ϕ, σ) where ϕ maps nodes of A to nodes
of B and σ ∈ End(A) is such that:

  1. There exists a map ϕstr : IA → IB such that for all (s, i) ∈ A, ϕ(s, i) =
     (ϕstr (s), i).

  2. n ∈ nodes(A) implies σ(evt(n)) = evt(ϕ(n)).

  3. σ(NA ) ⊆ NB ;

  4. σ(UA ) ⊆ UB

Remark 7.5. The mapping ϕstr is called the strand mapping. The strand
mapping is unique. By abuse of notation, in most contexts we will use ϕ to
denote the strand mapping.


                                     ϕ
                     b                           σ(b)




                                      ϕstr



                Figure 7: Protomorphism of Protoskeletons

                 λ
   We write A 99K B when λ is protomorphism.
                                                                    ϕ,σ
Definition 7.6 (Structure-preserving). A protomorphism A 99K B is
structure-preserving if n0 ≺A n1 implies ϕ(n0 ) ≺B ϕ(n1 ).

    Clearly the composition of structure-preserving protomorphisms is a
structure-preserving protomorphism.

Definition 7.7 (Point of origination preserving morphisms). A protomor-
         ϕ,σ
phism A 99K B preserves points of origination if ϕ(OA (t)) ⊆ OB (σ(t)) for all
t ∈ UA .
                                                           ϕ,σ
Definition 7.8 (Homomorphism). A protomorphism A 99K B is a homo-
morphism if it is structure-preserving and preserves points of origination.

   Definition 7.8 allows the image of an atom in UA to originate at more
than one point.
                 λ
   We write A →  − B when λ is a homomorphism. We use Protom(A, B) to
denote the set of all protomorphisms from A to B, and Hom(A, B) to denote
the set of all homomorphisms from A to B.

Proposition 7.9. The composition of homomorphisms between protoskele-
tons is a homomorphism.




                    (ϕ0 ,σ0 )    (ϕ1 ,σ1 )
Proof. Suppose A −−−−→ B, B −−−−→ C are homomorphisms. For each t ∈
UA , σ0 (t) ∈ UB by Property (4) of protomorphisms and thus by the definition
of homomorphism,

               ϕ1 (ϕ0 (OA (t))) ⊆ ϕ1 (OB (σ0 (t))) ⊆ OC σ1 (σ0 (t))



   Given a protoskeleton A = (I, Θ, ≺, N, U ) and a receiving node n of A,
we can define a fragment FA,n = (T, U, N, a) where −a = evt(n) and where

                T = {t | ∃n0 ∈ A, n0 ≺ n and evt(n0 ) = +t}.

We write PA,n to refer to PFA,n .
   Protoskeletons and protomorphisms form a category as well as protoskele-
tons and homomorphisms.


### 7.1    Preskeletons

We now consider two additional subcategories of the protoskeleton categories.
These categories will be full subcategories. Accordingly, when we refer to a
protomorphism or homomorphism we will always regard it as a pair (ϕ, σ).

Definition 7.10. A protoskeleton A = (I, Θ, ≺, N, U ) for a protocol P is a
preskeleton if

  1. Relation ≺ is transitive, asymmetric, and includes the strand succession
     relation: (s, i) ⇒ (s, i + 1) for all (s, i + 1) ∈ A.

  2. If s 6= s0 and (s, i) ≺ (s0 , j) then either evt(s, i) = +e and evt(s0 , j) =
     −e0 , or there exists a node n such that (s, i) ≺ n ≺ (s0 , j).

  3. Each atom in N is carried at no node of A, and each variable in the
     atom occurs at some node of A.

  4. Each atom in U is carried at some node of A.

  5. If s is any strand such that ρs ∈ P , and t ∈ Uρs such that t originates
     in Cρs | len Θ(s) at event i, then σ(t) originates in Θ(s) at (s, i).




   +e            ≺              +e0         +e     ≺               ≺      +e0
                                      =⇒
                                                          ∃n ∈ A



      s                          s0         s                             s0



Figure 8: One Case of Intermediate Node Condition: (2) of Definition 7.10.
Two remaining cases: −e, −e0 and −e, +e0 .

                                      Protoskeleton    Preskeleton     Skeleton
 Has valid role assignment                  •               •             •
 Inherited origination nodes                •               •             •
 ≺ is a strict partial order                                •             •
 Origination assumptions satisfied                                        •


   Figure 9: Salient differences between Proto, Pre and Proper Skeletons

Definition 7.11. A preskeleton A = (I, Θ, ≺, N, U ) for P is a skeleton
for P if each atom in U originates on exactly one strand, and the node of
origination precedes each other node that carries the atom, i.e. for every t ∈
U , n0 ∈ OA (t) and n1 ∈ CA (t), n1 6= n0 implies n0 ≺ n1 .

    In contexts where the protocol is understood, we simply refer to a skeleton
for P as a skeleton.
    We use PSkel(P ), PreSkel(P ) and Skel(P ) to denote the collections of
valid protoskeletons for P , valid preskeletons for P , and valid skeletons for
P , respectively. Since the protocol P is fixed for the remainder of the paper,
the argument P will be mostly omitted.


### 7.2       Hierarchies and Commitments

In this section we fix a protocol P . To analyse the cpsa algorithm, we
need to introduce additional structure on the basic protoskeleton category.



A protoskeleton refinement category is a category C and a functor F : C −→
PSkel.


### 7.2.1   Assignment Committed Protoskeletons

A pair (A, A) consisting of a protoskeleton A and a P -role assignment A is
an assignment committed protoskeleton. To make this class of objects into a
category, we first consider the behavior of role assignments under morphisms.
There is no universally applicable way that role assignments can be regarded
as transforming either covariantly, that is pushing the assignments forward
under morphisms or contravariantly, pulling them back. We can however
regard them as transforming covariantly in a weaker sense. Suppose A, B
are node spaces, λ = (ϕ, σ) : A −→ B is a homomorphism of node spaces. If
                           A = {(ρA    A
                                  s , σs ) : s ∈ IA },
                           B = {(ρBt , σtB ) : t ∈ IB }
are role assignments for A, B respectively such that for all s ∈ IA , ρBϕ(s) = ρA
                                                                                s
then the role assignment B is a pushforward of A under λ. Thus instead of
being a function, “pushforward” is a relation between role assignments.
Remark 7.12. The definition of pushforward under λ = (ϕ, σ) says nothing
about the substitutions σ A and σ B . However in the basic cryptoalgebra,
                               σ ◦ σ A (v) = σ B (v)                         (6)
for all variables v which occur in Cρs | len Θ(s).
                                                                      ϕ,σ
Definition 7.13 (Assignment-preserving). A protomorphism A 99K B is a
protomorphism of assignment-committed protoskeletons (A, AA ) −→ (B, AB )
if the role assignment AB is a pushforward of the role assignment AA under
(ϕ, σ).
Remark 7.14. It follows immediately from the definitions that
                               F•→ : (A, A) 7→ A
maps the class of assignment committed protoskeletons onto the class of
protoskeletons. Any assignment-preserving protomorphism is a protomor-
phism, so F•→ can be considered a functor from the category of assignment-
committed protoskeletons to protoskeletons.
   We denote the category of assignment-committed protoskeletons by PSkel.



### 7.2.2   Listener Committed Protoskeletons

Remark 7.15. The definition of protocol P allows for roles ρ such that the
trace Cρ is a listener strand. However, to conform to the established usage
in the cpsa specification we will use the term listener to refer to a strand
which is specified by the listener pseudorole. Accordingly the listener set of
a role assignment A is

                    L(A) = {s ∈ IA : ∃σ A(s) = (£, σ)}.                    (7)

By extension, we will also call this set the listeners of an assignment commit-
ted protoskeleton (A, A). Let A be a protoskeleton for protocol P . A valid
set of listeners for A is a set of strands L ⊆ IA of the form L(A) for some
role assignment A. The protoskeleton A may contain listener strands not in
L(A) if the protocol P has listener roles.
    A listener committed protoskeleton is a pair (A, LA ) where LA is a valid
set of listeners for A.
                                              ϕ,σ
Definition 7.16 (Listener-respecting). A 99K B is a protomorphism of
listener-committed protoskeletons from (A, LA ) to (B, LB ) if for every strand
s ∈ A, s ∈/ LA implies ϕ(s) ∈
                            / LB .
                   ϕ,σ              ϕ,σ
   We write A◦ 99K B◦ and A◦ −−→ B◦ to denote that (ϕ, σ) is a pro-
tomorphism (respectively homomorphism) of listener-committed protoskele-
tons from A◦ to B◦ .
Remark 7.17. Similarly, there is a well-defined functor F◦→ from listener
committed protoskeletons to protoskeletons which simply forgets the listener
set. Clearly
                           F•→ = F◦→ ◦ F•→◦ .                            (8)
Since F•→ is surjective (Remark 7.14) F◦→ is surjective.
Remark 7.18. It follows immediately from the definitions that

                         F•→◦ : (A, A) 7→ (A, L(A))

maps the class of assignment committed protoskeletons onto the class of lis-
tener committed protoskeletons. If (ϕ, σ) is a protomorphism of assignment-
committed protoskeletons, then (ϕ, σ)is also a protomorphism of the corre-
sponding listener-committed protoskeletons. Thus we can consider F•→◦ as
a functor.


                                                λ
Definition 7.19. A protomorphism A◦ 99K B◦ is assignment-consistent if
there exist role assignments A• = (A, AA ), B• = (B, AB ) such that (1) A◦ is
the listener-committed version of A determined by A• , (2) B◦ is the listener-
committed version of B determined by B• , and λ is a protomorphism of
assignment-committed protoskeletons from A• to B• .
                    λ
Remark 7.20. A◦ 99K B◦ is assignment-consistent if and only if it is of the
                                  λ•
form F•→◦ (λ• ) for some A• 99K B• .


### 7.3    Diagrams

We use PSkel• (P ), PreSkel• (P ) and Skel• (P ) to denote the collections of
assignment committed protoskeletons for P , assignment committed preskele-
tons for P , and assignment committed skeletons for P , respectively. PSkel◦ (P ),
PreSkel◦ (P ) and Skel◦ (P ) denote the collections of listener committed pro-
toskeletons for P , listener committed preskeletons for P , and listener com-
mitted skeletons for P , respectively.
Remark 7.21. As a notational heuristic, we use A• , B• and A◦ , B◦ as symbols
to denote assignment committed and listener committed skeletons (possibly
proto or pre). Morever, unless explicitly stated to the contrary, in a context in
which either one of the symbols A• or A◦ are mentioned, the symbol A refers
to the underlying protoskeleton, and, in a context in which A• is mentioned,
A◦ refers to the listener-restriction of A• .
   Let P be a protocol. We have the following diagram:
                         PSkel• ⇐== PreSkel• ⇐=== Skel•

                     F•→◦
                              ?             ?            ?
                         PSkel◦ ⇐== PreSkel◦ ⇐=== Skel◦                      (9)

                        F◦→
                              ?             ?            ?
                         PSkel ⇐=== PreSkel ⇐==== Skel
where the downward arrows are structure removing mappings and leftward
arrows are inclusion mappings. At this point of the exposition nothing can be


said about functoriality of the arrows since no morphisms have been defined
for any of these collections. That is the object of the next section.
    The preceding remarks are summarized in the following proposition:

Proposition 7.22. In the diagram (9), the mappings F•→◦ and F◦→ are
defined and surjective on all the columns.


### 7.4    Preservation Properties

In arguments involving objects such as protoskeletons and protomorphisms,
it is desirable to identify properties of these objects which are preserved under
some specific transformation or more generally some relation. Some of the
properties we single out are in fact negations of conditions used to define the
main categories in the theory.
     Non-asymmetry of protoskeleton A is the property that there are nodes
m, n for which m ≺ n and n ≺ m. A non-asymetric protoskeleton is not a
skeleton.

Proposition 7.23 (Non-asymmetry preserved under structure-preserving
protomorphisms). If A is a protoskeleton such that ≺A is not asymmetric,
then there is no structure-preserving protomorphism λ from A to a protoskel-
eton B.

Proof. If m ≺ n and n ≺ m in A, and λ = (ϕ, σ) is structure-preserving,
then ϕ(m) ≺ ϕ(n) and ϕ(n) ≺ ϕ(m) in B, so B is not a preskeleton. Note
that even if ϕ(m) = ϕ(n), ≺ is not asymmetric in B.

Proposition 7.24 (Point of origination non-preservation preserved under
                       ϕ,σ
extensions). Suppose A 99K B and t ∈ UA are such that n ∈ OA (t), but
                         ϕ0 ,σ 0
ϕ(n) ∈/ OB (σ(t)). If B 99K C is any protomorphism to any protoskeleton,
then (ϕ0 ◦ ϕ)(n) ∈
                 / OC ((σ 0 ◦ σ)(t)).

Proof. Note that the message at n carries t in A, so the message at ϕ(n)
carries σ(t) in B. If ϕ(n) is not a point of origination of σ(t) in B, there must
be a node n0 = (s, i) where n = (s, j) and i < j, where ϕ(n0 ) carries σ(t).
Then ϕ0 (ϕ(n0 )) carries σ 0 (σ(t)), so ϕ0 (ϕ(n)) ∈
                                                  / OC (σ 0 (σ(t))).

Proposition 7.25 (Point of origination preservation preserved under proto-
                                            ϕ,σ                    ϕ0 ,σ 0
morphism factoring). Suppose we have A 99K B and we have A 99K C where


                  ϕ00 ,σ 00
there is some B 99K C such that ϕ = ϕ00 ◦ ϕ0 and σ = σ 00 ◦ σ 0 . Then if (ϕ, σ)
preserves points of origination, (ϕ0 , σ 0 ) preserves points of origination.

Proof. We prove the contrapositive: that if (ϕ0 , σ 0 ) does not preserve points of
origination then neither does (ϕ, σ). Suppose (ϕ0 , σ 0 ) does not preserve points
of origination, and suppose t ∈ UA and suppose n ∈ OA (t) are such that
ϕ0 (n) ∈
       / OC (σ 0 (t)). By Proposition 7.24, ϕ00 (ϕ0 (n)) = ϕ(n) ∈
                                                                / OB (σ 00 (σ 0 (t))) =
OB (σ(t)). Thus, (ϕ, σ) does not preserve points of origination.

Proposition 7.26 (Violation of role-inherited unique origination constraints
preserved under protomorphisms of assignment-committed protoskeletons).
Suppose A• is a protoskeleton, B• is a protoskeleton meeting condition (5)
of the definition of preskeleton and λ is a protomorphism of assignment-
committed protoskeletons from A• to B• . Then A• meets condition (5) of the
definition of preskeleton.

Proof. Argue by contradiction. Suppose A• = (A, A) does not meet condi-
tion (5) of the definition of preskeleton. Then there is a strand s and a t ∈ Uρs
such that t originates in Cρs | len ΘA (s) at event i but σs (t) does not originate
in ΘA (s) at event i. Thus σs (t) is carried at an earlier event j on ΘA (s). But
then σ(σs (t)) is carried at event j in strand ϕ(s) in B• . However, strand ϕ(s)
is associated in B• with ρs and thus B• does not meet condition (5) of the
definition of preskeleton.


### 7.5     Coverage

If A = (I, Θ, ≺, N, U ) is a protoskeleton and I 0 ⊂ I is any subset, then

                RmvI 0 (A) = (I \ I 0 , Θ|I\I 0 , ≺ |(I\I 0 )×(I\I 0 ) , N, U ).

We are particularly interested in the case where I 0 is a valid listener set for
A. In that case, RmvI 0 (A) is a preskeleton (or skeleton) if A is a preskeleton
(or skeleton). If A◦ = (A, LA ) is a listener committed protoskeleton, then

                                 Rmv A◦ = RmvLA (A).                               (10)

Remark 7.27. By definition Rmv maps objects in PSkel◦ to objects in PSkel.
        λ
If A◦ 99K B◦ is a protomorphism of listener-committed skeletons then by
Definition 7.16, λ |Rmv A◦ is a protomorphism Rmv A◦ 99K Rmv B◦ . Thus


we can view Rmv as a functor in the protomorphism categories PSkel◦ −→
PSkel. We will denote λ |Rmv A◦ by Rmv(λ).
          λ
    If A◦ →
          − B◦ is a homomorphism Rmv A◦ →     − Rmv B◦ is a homomorphism.
Proof: The order preserving property is obvious. Nothing can originate on
a listener strand (Remark 6.2), therefore deleting any set of listener nodes
does not affect origination nodes.
Remark 7.28. If A◦ is a realized skeleton then Rmv(A◦ ) is also realized. Proof:
Removing listener strands on a preskeleton has no effect on the fragments at
any of the remaining nodes.
Definition 7.29. The coverage of a listener committed skeleton A◦ , which
we denote [[A◦ ]], is the collection of homomorphisms λ |Rmv(A◦ ) as λ ranges
over homomorphisms A◦ →     − B◦ with B realized.
    Alternatively,
                                                                  λ
         [[A◦ ]] = {(Rmv B◦ , λ |Rmv(A◦ ) ) | B is realized and A◦ →
                                                                   − B◦ }.   (11)
Thus the coverage is some collection of homomorphisms Rmv(A◦ ) →
                                                               − B into
realized skeletons B.



## 8     Operators

In this section, we define the notion of an operator, which transforms proto-
skeletons. We will then define the set of operators that cpsa most depends
on. In general, an operator on a collection S is a mapping F which whose
domain consists pairs (a, τ ) where a ∈ S and τ is an auxiliary parameter.
    An operator for a protocol P is a self-mapping on PSkel(P ). An assignment-
transforming operator is a partial self-mapping on PSkel• (P ). A listener-
transforming operator is a partial self-mapping on PSkel◦ (P ). We will also
use the generic term “operator” informally to refer to an operator on any of
the protoskeleton categories and as a self-mapping on the category of node
spaces.
    In the assignment-transforming operators f we consider below, the pro-
toskeleton component of f(A, A) depends only on A and the role assignment
component depends only on A. We will call the role assignment compo-
nent the role-assignment transformation. A desirable property of the role-
assignment transformation is that the set of listeners in f(A, A) depends only
on the set of listener strands in A.


Definition 8.1. An assignment-transforming operator f is well-behaved with
respect to listeners if whenever A and A0 are role assignments for a proto-
skeleton A which have the same set of pseudolisteners, the role assignments
of f(A, A) and f(A, A0 ) also have the same set of pseudolisteners.

    Whenever f is an assignment-transforming operator well-behaved with
respect to listeners, we can view f as describing a well-defined listener-
transforming operator, which we will also refer to as f, abusing notation.
Specifically, if LA is a valid listener set for A then let A be a role assignment
justifying its validity. Since the set of listeners under f(A) depends only on
LA , we can view that set as the well-defined result of applying f to LA .
    A linking map Λf associated to an operator f (on any of the protoskele-
ton categories) associates to any protoskeleton A a protomorphism Λf (A) =
(ϕf (A), σf (A)) from A to f(A). For each protoskeleton A, Λf (A) is called the
linking protomorphism. In particular, if the operator f acts on the protoskel-
eton category PSkel• , for each A• ∈ PSkel• , the linking protomorphism will
be required to be an assignment-preserving protomorphism.
Remark 8.2. Suppose (A, A) is an assignment-committed protoskeleton with
linking protomorphism Λf (A) = (ϕ, σ). Λf (A) is assignment-preserving if
and only if the role assignment of B of f(A, A) satisfies ρBϕ(s) = ρA
                                                                    s for every
strand s in A. In particular ρϕ(s) is a pseudolistener if and only if ρA
                               B
                                                                         s is a
pseudolistener. This remark proves:

Proposition 8.3. Suppose f is an assignment transforming operator with
linking protomorphism Λf . If for every assignment committed protoskeleton
(A, A) the node mapping component of Λf (A, A) is surjective, then f is well-
behaved with respect to listeners.

   cpsa operates at the listener-committed protoskeleton level, so it is im-
portant that:

   • Operators we use are listener-transforming, and

   • Operators we use have linking protomorphisms that are protomor-
     phisms of listener-committed protoskeletons from A◦ to f(A◦ ).

Most of the operators we use are actually assignment-transforming operators
well-behaved with respect to listeners.





### 8.1    Suites

A suite is a map from Pskel◦ to a set of listener-transforming operators, that
is
          f : Pskel◦ −→ P({f|f is a listener-transforming operator})
   We use f[A◦ ] to denote {f(A◦ )|f ∈ f(A◦ )}.
   If f and g are suites, then f ◦ g is a suite where f ◦ g(A◦ ) = {f ◦ g|g ∈
g(A◦ ), f ∈ f(g(A◦ ))}.
   At the top level, cpsa is a setwise term reduction system, driven by
reductions f[·] for various suites.


### 8.2    Filters

A filter is a predicate on pairs (A◦ , f) where f is an operator on A◦ . If F
is a filter and f is a suite, fF is a suite, where fF (A◦ ) = {f|f ∈ f(A◦ ) and
(A◦ , f) ∈ F }.
    If F is a filter and f is a listener-transforming operator, then f F is a suite
which, on input A◦ , is {f} if (A◦ , f) ∈ F and ∅ otherwise.


### 8.3    Primitive Operators

In this section we describe some very simple operators from which our more
complicated test-solving operators are built.

Definition 8.4 (Identity operator). For any protoskeleton A, Id(A) = A.
The corresponding role-assignment transformation is Id(A) = A.
   The linking map ΛId is the identity protomorphism:

                               Λf (A) = (IdA , IdA ).

   The linking protomorphism for Id(A) is a protomorphism of assignment-
commited protoskeletons.
   If σ is a substitution, we can define an operator Subσ based on σ: basically,
we apply σ to all algebraic parts of A while leaving its node structure alone.

Definition 8.5 (Substitution operator). If σ ∈ End(A) then we define the
operator Subσ as follows. If A = (I, Θ, ≺, N, U ) then

                     Subσ (A) = (I, σ ◦ Θ, ≺, σ(N ), σ(U )).


The linking map ΛSubσ is defined as follows:

                               ΛSubσ (A) = (IdA , σ)

The role-assignment transformation is defined as follows: If A = {(ρs , σs ) :
s ∈ I} is a role assignment, then Subσ (A) = {(ρs , σ ◦ σs ) : s ∈ I}.

Remark 8.6. If A = (I, Θ, ≺, N, U ) is a protoskeleton with validating role
assignment A, Subσ (A) is a protoskeleton with validating role assignment
Subσ (A). This follows from the definition of protoskeleton (7.2).

                     NSubσ (A) = σ(N ) ⊇ σ(NA ) = NSubσ (A)

and
                     USubσ (A) = σ(U ) ⊇ σ(UA ) = USubσ (A) .
Remark 8.7. By Proposition 8.3, the substitution operators are well-behaved
with respect to assignments.
    Note that the linking protomorphism ΛSubσ (A) is not necessarily a homo-
morphism since preservation of nodes of origination may fail. We say that a
substitution σ is homomorphic if the linking protomorphism of Subσ is a ho-
momorphism. Note also that the linking protomorphism is a protomorphism
of listener-committed protoskeletons.
    The compression operator combines two compatible strands. Recall that
a strand is a node space consisting of a single strand.

Definition 8.8 (Compression operator). Suppose s, s0 are strands and A is
a protoskeleton. Comps,s0 (A) is defined only when s, s0 ∈ IA and Θ(s) is a
prefix of Θ(s0 ) or Θ(s0 ) is a prefix of Θ(s). Assume this is the case. If s, s0
have different lengths, let smax be the strand out of {s, s0 } of greater length
and let smin be the other strand; otherwise smax = s and smin = s0 .

                Comps,s0 (A) = (I \ {smin }, Θ|I\{smin } , ≺0 , N, U )

where the relation ≺0 is defined based on the linking protomorphism

                         ΛComps,s0 (A) = (ϕComps,s0 , IdA )

where ϕComps,s0 is the identity on the nodes in I \ {smin } but ϕComps,s0 (smin ) =
smax .


   The relation ≺0 is the smallest transitive relation such that for all n, n0 ∈
A, if n ≺ n0 then ϕComps,s0 (n) ≺0 ϕComps,s0 (n0 ).
   The listener transformation of Comps,s0 is defined as follows

                                   LA \ {smin } if {s, s0 } ⊂ LA
                                
               Comps,s0 (LA ) =
                                   LA \ {s, s0 } otherwise
Remark 8.9. The compression operator is not always viewable as assignment-
transforming: the main issue is that although Θ(s) is a prefix of Θ(s0 ) this
does not guarantee that both s and s0 are instances of the same role in all role
assignments. However, our description of Comps,s0 as a listener-transforming
operator guarantees that the linking protomorphism will always be a proto-
morphism of listener-committed protoskeletons.
Remark 8.10. First a definition: Given a role assignment A = {(ρs , σs ) : s ∈
I} and strands s, s0 , A(s) is compatible with A(s0 ) if and only if ρs = ρs0 .
Suppose s, s0 are given. If an an assignment-committed protoskeleton (A, A)
is such that s, s0 are such that A(s) is compatible with A(s0 ), then one can
view Comps,s0 as an assignment-transforming operator on (A, A). Moreover
by Proposition 8.3 the operator is well-behaved with respect to listeners.
Remark 8.11. It is clear that Comps,s0 (A) is a protoskeleton, regardless of the
relation ≺0 . However, if A is a preskeleton, Comps,s0 (A) need not be a preskel-
eton because ≺0 may have a cycle violating Condition 1 of Definition 7.10.
   Given a protoskeleton A, order enrichment only affects the order relation.

Definition 8.12 (Order enrichment operator). If A = (IA , ΘA , ≺0 , NA , UA ),
then
                     OE(A) = (IA , ΘA , ≺0 , NA , UA )
where ≺0 is the smallest transitive relation such that

  1. If n ≺A n0 then n ≺0 n0 and

  2. If t ∈ U and t originates in A at n, and n0 is any other node at which
     t is carried then n ≺0 n0 .

The role-assignment transformation is the identity.
   The linking protomorphism is the identity:

                              ΛOE (A) = (IdA , IdA )



   The linking protomorphism is clearly a protomorphism of assignment-
committed protoskeletons.
Remark 8.13. By Proposition 8.3, the order enrichment operator is well-
behaved with respect to listeners.
    Finally, the augmentation operator adds a strand. Recall that for a role
or pseudorole ρ, Cρ is the trace of ρ.

Definition 8.14 (Augmentation operator). Let A = (I, Θ, ≺, N, U ). Let
n ∈ A be any reception node. Let ρ ∈ (P ∪ {£}). Let i ≤ |Cρ | such that
evt Cρ , i is a transmission and let σ be any substitution. Let s? ∈
                                                                   / IA . Then

                         Augn,ρ,i,σ,s? (A) = (I 0 , Θ0 , ≺0 , N 0 , U 0 )

where:

   • I 0 = I ∪ {s? }.

   • Θ0 (s) = Θ(s) for s ∈ I and Θ0 (s? ) = σ(Cρ |i).

   • (s1 , i1 ) ≺0 (s2 , i2 ) if and only if one of the following holds:

         1. s1 , s2 ∈ I and (s1 , i1 ) ≺ (s2 , i2 ),
         2. s1 = s2 = s? and i1 < i2 , or
         3. s1 = s? , s2 ∈ I, and n  (s2 , i2 ).

   • N 0 = N ∪ [σ]∗ Nρ

   • U 0 = U ∪ [σ]∗ Uρ

The augmentation operator has an associated linking protomorphism where

                              ΛAugn,ρ,i,σ,s? (A) = (IdA , IdA ).

The role assignment transformation Augn,ρ,i,σ,s? (A) is equal to A on strands
in I but maps s? to (ρ, σ).

    Note that Augn,ρ,i,σ,s? (A) may not always be a preskeleton even if A is, but
ΛAugn,ρ,i,σ,s? (A) is always a homomorphism, and is always a homomorphism of
assignment-committed protoskeletons.



Remark 8.15. Any augmentation operator f is well-behaved with respect to
listeners. This does not immediately follow from Proposition 8.3 since the
node mapping component of the node mapping component of Λf (A, A) is not
surjective. However Λf (A, A) only misses those elements in the new strand
s? and the role for this new strand is prescribed by ρ which is a parameter
in f.
Theorem 8.16 (Preskeleton property preserved under primitive operators).
Let A• and B• be preskeletons and f be an assignment-transforming primitive
operator on A• such that there is a commutative diagram:
                                      Λf (A•-)
                                A•                  f(A• )

                                                    λ0                           (12)
                                       λ

                                                -

                                                         ?
                                          B•
where λ is a structure-preserving protomorphism of assignment-committed
preskeletons and λ0 is a protomorphism of assignment-committed protoskele-
tons. Then f(A• ) is a preskeleton.
Proof. Asymmetry of ≺ (part of Condition (1) of Definition 7.10) is assured
by Proposition 7.23 and Condition (5) is assured by Proposition 7.26. For
the remaining properties our proof proceeds by cases, one for each primitive
operator. Let λ = (ϕ, σ) and let λ0 = (ϕ0 , σ 0 ).

  f = Id: Since Id(A• ) = A• , f(A• ) is a preskeleton, and meets all required
conditions.

   f = Subσ0 : Since the set of nodes and the ordering of f(A• ) are the same
as those of A• , it should be clear that f(A• ) meets condition (2) and satisfies
the remaining properties of (1).
    Proof of Property (3): Suppose t ∈ Nf(A• ) . If t is carried at a node n of
f(A• ) then σ 0 (t) ∈ σ 0 (Nf(A• ) ) ⊂ NB• is carried at node ϕ0 (n). This contradicts
B• being a preskeleton. Therefore t is carried at no node of f(A• ). Next, t is
of the form σ0 (s) for some some s ∈ NA . Every variable in s occurs at some
node in A• . Therefore every variable in t occurs at some node in B• .
    Proof of Property (4). Let t ∈ Uf(A• ) . t is of the form σ0 (s) for some some
s ∈ NA . s is carried at a node n in A• , and therefore t is carried at node n.


   f = Comps,s0 : Note that if f is assignment-transforming in this case then
A(s), A(s0 ) are compatible (Remark 8.10). The ordering ≺Comps,s0 (A• ) is de-
fined to be transitive. Moreover, since the linking homomorphism is surjec-
tive, the ordering ≺Comps,s0 (A• ) includes the strand ordering. Condition (2)
follows from the fact that ϕComps,s0 (A• ) is defined to be structure-preserving.
Conditions (3) and (4) follow from the fact that NComps,s0 (A• ) = NA• and
UComps,s0 (A• ) = UA• , and that every event in A• is present in f(A• ) since we
eliminate only completely duplicated nodes.

   f = OE: Like Comps,s0 , ≺OE(A• ) is defined to be structure-preserving and
transitive, and all events in A• are present (at the same node) in OE(A• ), so
all required conditions are clearly met.

  f = Augn,ρ,i,σ0 ,s? : Here, transitivity of ≺f(A• ) is established as follows. If
n1 = (s1 , i1 ), n2 = (s2 , i2 ), n3 = (s3 , i3 ) are nodes in f(A• ) and n1 ≺ n2 and
n2 ≺ n3 then:

    • If s2 ∈ I then s3 must be in I and n2 ≺A• n3 . If n1 ≺A• n2 then by
      transitivity in A• , n1 ≺A• n3 . If s1 = s? then n ≺A• n2 , so n ≺A• n3
      and thus n1 ≺f(A• ) n3 .

    • If s2 = s? then s1 = s? also. If s3 = s? then i3 > i2 and i2 > i1 so
      n1 ≺ n3 . Otherwise, n ≺A• n3 so n1 ≺f(A• ) n3 .

    Condition (2) holds in f(A• ): if n1 = (s1 , i1 ) and n2 = (s2 , i2 ) and n1 ≺ n2
where s1 6= s2 then there are two cases. If s1 , s2 ∈ I the property holds
because A• is a preskeleton. Otherwise, it must be the case that s1 = s? and
s2 ∈ I. If there is no node between n1 and n2 it must be that n2 = n and n1
is the last node of s? . But the event at n is a reception and the event at the
last node of s? is a transmission.
   An obvious corrollary to this theorem is that the same property holds for
any composition of any number of primitive operators, so long as they are
each assignment-transforming.



## 9     Suites and the Setwise Reduction

cpsa proceeds by maintaining a set of listener-committed skeletons A◦ for


P . The initial state consists of one skeleton {A◦ } which we call the point of
view 1 .
    At each iteration, we rewrite the set by replacing an unrealized skeleton in
the set with a set of skeletons called the cohort of the unrealized skeleton (for
a specific critical path in an unrealized node in that skeleton). The cohort cal-
culation takes place in two phases: first, we calculate the pre-cohort, which is
a set of listener-committed preskeletons. Then, we calculate the skeletoniza-
tion of each pre-cohort member, which produces a set listener-committed
skeletons. We describe the cohort, the pre-cohort, and the skeletonization
steps as suites.
    In addition to these suites, cpsa also makes use of certain algorithms
for arbitrary choices. In this document we pay no attention to how these
functions are instantiated, we only remark the following:

   • N AM E(A) is a choice of name for a new strand to add to A.
     N AM E(A) ∈
               / IA .

   • T EST (A) is a choice of a test (see Definition 10.5) in an unrealized
     skeleton.

   • U OI(A) is a choice of a unique origination issue. If A does not satisfy
     the condition of being a skeleton that every atom in UA originates at at
     most one node, then U OI(A) returns a triple (t, n, n0 ) such that t ∈ UA
     and n 6= n0 are both in OA (t).

   • SEARCH(S) is a choice of which skeleton to perform the cohort op-
     eration on. Given a set S of listener-committed skeletons, at least
     one of which is unrealized, SEARCH(S) returns one of the unrealized
     skeletons in S.

   • F R(A, ρ, i) is a substitution that maps each variable occurring in Cρ |i
     to a distinct variable not occurring in A or in any role of the protocol.


### 9.1     The Pre-Cohort Suite

The pre-cohort suite is designed to infer additional honest behavior or re-
strictions on a skeleton in order to make progress in resolving a critical path.
    Actually, cpsa allows the user to specify a pre-skeleton which is then skeletonized,
but this is a convenience feature.



    Suppose A is an unrealized skeleton with valid listener set LA , and that
n is an unrealized node of A, and that p is a critical path with endpoint ep
of the term evt A (n) in the fragment FA,n . The pre-cohort suite is

             Pn,p (A◦ ) = cn,p (A◦ ) ∪ an,p (A◦ ) ∪ dn,p (A◦ ) ∪ ln,p (A◦ ),   (13)

where the suites in the union are defined as follows.

Definition 9.1 (Contraction suite).

                          cn,p (A◦ ) = ∪S∈Z {Subσ |σ ∈ S}                      (14)

where Z is a set of Sa,b for each a ∈ Esc(FA,n , ep ) and for each b visited by p
where Sa,b is a complete set of most general unifiers of a, b.

Definition 9.2 (Regular Augmentation suite).

                   an,p (A◦ ) = {Subσ1 ◦ Augn,ρ,i,σ0 ◦F R(A,ρ,i),s? }          (15)

where σ0 ∈ S0 , σ1 ∈ S1 , s? = N AM E(A) and ρ, i, σ0 , σ1 , S0 , S1 are as defined
below}.

   • R ∈ P and i is such that CR (i) is defined and is a send event. Let
     C = CR |i.

   • There is a path pp ∈ CarPath(C(i)) and a term tt such that either (i)
     the endpoint of pp is a variable not of sort mesg and tt = ep or (ii) the
     endpoint of pp is a variable of sort mesg and tt ∈ Targ(Esc(F, ep ), ep ).

   • S0 is a set of most general unifiers of tt with the endpoint of
     F R(A, ρ, i)(pp).

   • S1 is a set of most general maps σ1 such that for all i0 < i and for all
     paths p0 ∈ CarPath(C(i0 )), if the endpoint of σ1 ((σ0 ◦ F R(A, ρ, i))(p0 ))
     is σ1 (ep ) then σ1 (p0 ) visits an element of σ1 (Esc(FA,n , ep )).

    Note that it is not obvious that S1 exists, let alone that there is a finite set
of such maps we can calculate efficiently. However, their existence, and the
ability of cpsa to identify a covering set of them, is proven in Appendix A.





Definition 9.3 (Displacement suite.).

            dn,p (A◦ ) = {Comps,s? ◦ Subσ2 ◦σ1 ◦ Augn,ρ,i,σ0 ◦F R(A,ρ,i),s? }    (16)

where ρ, i, σ0 , σ1 , s? are as in the definition of an,p (A◦ ), σ2 ∈ S, and s, S have
the properties described below.

   • s is a strand in A and there exists a role assignment A such that s is
     associated with role ρ.

   • S is a set of most general unifiers of the first i0 events in s and the first
     i0 events in s0 where i0 is the smaller of |s| and i.

Remark 9.4. Displacement is the only pre-cohort sub-suite that involves the
compression operator, and is thus the only place where a concern arises as
to whether operators in the pre-cohort suite can be viewed as assignment-
transforming. A displacement operator Comps,s? ◦ Subσ2 ◦σ1 ◦ Augn,ρ,i,σ0 ,s? is
assignment-transforming on (A, A) whenever A associates strand s with ρ,
because in such cases compression occurs between two strands with the same
role association, and therefore, the association of the combined strand is
unambiguous.

Definition 9.5 (Listener augmentation suite.). ln,p (A◦ ) = esln,p (A◦ )∪cpln,p (A◦ )
where:

   • Escape set listener augmentation. esln,p (A◦ ) = {Augn,£,2,σ,s? |s? =
     N AM E(A), {|c|}u ∈ Esc(FA,n , ep ) and σ maps the m in the listener role
     to inv(u)}.

   • Critical path listener augmentation. cpln,p (A◦ ) = {Augn,£,2,σ,s? |s? =
     N AM E(A), ep = {|c|}u and σ maps the m in the listener role to u}.
     Note that cpln,p (A◦ ) is ∅ if ep is not an encryption.


### 9.2     The Skeletonization Suite

The skeletonization suite is designed to rectify pre-skeletons back into skele-
tons.
   The overall process is as follows. If A is not a skeleton, then either it is
not a skeleton because some atom in U originates on more than one strand,
or because there are required orderings that are not present. We resolve all


of the former issues before the latter. When a restricted atom originates on
multiple strands, we resolve the problem in one of two ways: either we merge
two strands on which the atom originates, via unification and compression, or
we de-originate one of the origination points, in which we apply a substitution
to the strand so that the atom is gained at an earlier point.
    The skeletonization suite is S(A◦ ) = {OE ◦ f|f ∈ ur(A◦ )}. The unique
origination rectification suite, ur, is defined to be {Id} if NUO(A◦ ) is empty,
where NUO(A◦ ), the set of non-compliant unique origination constraints, is
defined to be {(t, n, n0 )|t ∈ UA and n and n0 are distinct points of origination
of t in A}, or otherwise defined recursively as follows:

    ur(A◦ ) = {f ◦ f 0 |(t, n, n0 ) = U OI(A), f 0 ∈ urt,n,n0 (A◦ ), f ∈ ur(f(A◦ ))},
    where urt,n,n0 (A◦ ) = Mt,n,n0 (A◦ ) ∪ Dt,n,n0 (A◦ ), and where M (the merging
suite) and D (the deorigination suite) are defined below. Recall that U OI(A)
outputs a triple in N U O(A) as long as N U O(A) is non-empty.
Definition 9.6 (Merging suite.). Let n be in strand s and let n0 be in strand
s0 . Let i be the smaller of the lengths of s and s0 . Note that s and s0 must
be distinct because for any t there can be only one point of origination per
strand, and n and n0 are distinct. Then Mt,n,n0 = {Comps,s0 ◦ Subσ |σ ∈ U }
where U is a set of most general unifiers of Θ(s)|i with Θ(s0 )|i.
Remark 9.7. Merging is the only skeletonization-related suite that involves
the compression operator, and is thus the only place where a concern arises as
to whether operators in the skeletonization suite can be viewed as assignment-
transforming. A merging operator Comps,s0 ◦Subσ is assignment-transforming
on (A, A) whenever A associates strands s and s0 with the same role, be-
cause in such cases compression occurs between two strands with the same
role association, and therefore, the association of the combined strand is
unambiguous.
Definition 9.8 (Deorigination suite.). Let n = (s, i). Let V = {(i0 , pp)|i0 < i
and pp ∈ CarPath(mesg(s, i0 ))}. Then let Ui0 ,pp be a set of most general
unifiers of the endpoint of pp with t, if the endpoint of pp is not a variable
of sort mesg. If pp does terminate in a variable of sort mesg, let Ui0 ,pp be a
set of most general unifiers of the endpoint of pp with a term that carries t.
Then Dt,n,n0 = ∪(i0 ,pp)∈V {Subσ |σ ∈ Ui0 ,pp }.
Remark 9.9. When pp terminates in a variable of sort mesg, Ui0 ,pp is not
finite. Therefore, if this situation ever comes up, cpsa will not terminate.



### 9.3          Post-Processing Filters

The post-processing filters filter out operators that are invalid or have failed
to make progress. Once these filters are defined, we can define the cohort,
which is cpsa’s high-level reduction step.
    Let A be a protoskeleton, let LA be a valid listener set for A, and let f be
an operator defined on A◦ . Let n be an unrealized node of A and let p be a
critical path of evt A (n) in the fragment FA,n .
Definition 9.10 (Post-processing filter). The post-processing filter P Pn,p is
defined to be W F ∩ HC ∩ SFn,p .
Definition 9.11 (Well-formed filter). W F = {(A◦ , f) such that f(A) is a
preskeleton}.
Definition 9.12 (Homomorphism check). HC = {(A◦ , f) such that Λf (A) is
a homomorphism from A to f(A)}.
Definition 9.13 (Solved filter). SFn,p is the set of pairs (A◦ , f) such that p
is weakly solved in Ff(A),ϕ(n) by σ, where Λf(A) = (ϕ, σ).
   In our proof later it would be desirable to prove that if (A◦ , f) is in SFn,p
then so is (A◦ , g◦f) for all g. This is the case for some of the solved conditions:
                                                                                         ϕ,σ
Remark 9.14. Let n, p be a test in unrealized skeleton A◦ and let A◦ 99K
   ϕ0 ,σ 0
B◦ 99K C◦ , and let F = FA,n , F 0 = FB,ϕ(n) , and F 00 = FC,ϕ0 (ϕ(n)) . Then:
   1. If p, F, F 0 , (ϕ, σ) meet condition Sol1 then so do p, F, F 00 , (ϕ0 ◦ϕ, σ 0 ◦σ).
   2. If p, F, F 0 , (ϕ, σ) meet condition Sol3 then so do p, F, F 00 , (ϕ0 ◦ϕ, σ 0 ◦σ).
   3. If p, F, F 0 , (ϕ, σ) meet condition Sol4 then so do p, F, F 00 , (ϕ0 ◦ϕ, σ 0 ◦σ).
   However, this is not the case generally: progress guaranteed by condition
Sol2 or Sol5 can be reversed, for instance, by later unifications. What we can
prove is that these properties are preserved under extensions of an operator
that factor a map to another protoskeleton in which the same property holds.
Remark 9.15. Let n, p be a test in unrealized skeleton A◦1 and let
                                 ϕ1 ,σ1    ϕ2 ,σ2    ϕ3 ,σ3
                             A◦1 99K A◦2 99K A◦3 99K A◦4 .
   Let F1 = FA1 ,n , let F2 = FA2 ,ϕ1 (n) , let F3 = FA3 ,ϕ2 (ϕ1 (n)) , and let F4 =
FA4 ,ϕ3 (ϕ2 (ϕ1 (n))) . Let λ = (ϕ, σ) = (ϕ1 , σ1 ), λ0 = (ϕ0 , σ 0 ) = (ϕ2 ◦ ϕ1 , σ2 ◦ σ1 ),
and λ00 = (ϕ00 , σ 00 ) = (ϕ3 ◦ ϕ2 ◦ ϕ1 , σ3 ◦ σ2 ◦ σ1 ). Then:


  1. If p, F1 , F2 , λ meet condition Sol2 with path p0 , and if p, F1 , F4 , λ00 meet
     condition Sol2 with path σ3 (σ2 (p0 )), then p, F1 , F3 , λ0 meet condition
     Sol5 with path σ2 (p0 ).

  2. If p, F1 , F2 , λ meet condition Sol5 with term tt, and if p, F1 , F4 , λ00 meet
     condition Sol5 with term σ3 (σ2 (tt)) then p, F1 , F3 , λ0 meet condition
     Sol5 with term σ2 (tt).

    Although these claims are complex, they both boil down to the same
observation: if two terms have not been unified in A2 but are unified in A3 ,
they must be unified in A4 . Therefore, knowing they are not unified in both
A2 and A4 implies they are not unified in A3 . In the case of Sol2, the pairs
of terms are those visited by (t, π) and those in the image of Esc(F1 , ep ).
In the case of Sol5, the pairs are the new target term and the image of
Targ(Esc(F1 , ep )).


### 9.4    The Cohort and the CPSA Set Reduction

First, we define the cohort, the top-level suite used in the cpsa algorithm.

Definition 9.16 (The cohort). The cohort, cohn,p (A◦ ), is defined to be

                       cohn,p (A◦ ) = (S ◦ Pn,p )P Pn,p (A◦ ).

    Next we define the reduction relation , on sets of listener-committed
skeletons.

Definition 9.17 (Setwise reduction). Let S = {(A◦i )|1 ≤ i ≤ k} be a set of
listener-committed skeletons. If A◦i = SEARCH(S) and (n, p) = T EST (Ai )
then S  {A◦j |1 ≤ j ≤ k, j 6= i} ∪ cohn,p [A◦i ].

    The overall operation of cpsa is as follows. The user specifies the point
of view A• along with the protocol P . We calculate the initial set S = {A◦ }.
Then we proceed as follows:

  1. If ∃T such that S  T , let S ← T , and go to 1.

  2. Else, output S.





    cpsa in fact picks a particular element of S and a particular n and p and
chooses the T resulting from that choice. However, cpsa is configurable to
make different choices of these sorts, so we simply need to understand that
cpsa (when it halts) outputs a normal form of the reduction , that is, a
set S such that ¬∃T : S  T .



## 10      Suite Completeness

In this section we state and prove varous suite completeness theorems, cul-
minating in a proof that cpsa’s overall approach is complete.
    First, we state a number of definitions that should help to simplify and
clarify the complex theorem statements and proofs to follow. Most of the
theorems proving the completeness of cpsa are ones that concern proving
that coverage of a certain type can be maintained while advancing from one
listener-committed protoskeleton to another via a certain suite. The notion
of coverage varies for each theorem, and what is essential to understand from
the lemmas are the particular properties of that coverage, which are distinct
for each theorem. There is also, in each of these theorems, a complicated
logical structure, but one that is largely similar for all the theorems. We first
make definitions reflecting this generic logical structure, and then proceed to
discuss the various lemmas and theorems.

Definition 10.1 (Coverage property). A coverage context is a tuple C =
(X, Y, Act) where X, Y are sets and Act is a mapping PSkel ×X × Opr• → X
where Opr• is the collection of assignment-transforming operators. A cover-
age property relative to the coverage context C is a set C ⊂ ((PSkel• ×X) ×
Protom ×Y) such that for all ((A• , β), λ, α) ∈ C, λ is a protomorphism from
A.
    If β ∈ X, we use the notation f(A).β to refer to Act(A, β, f). In cases
where A is unambiguous, we sometimes use the notation f.β.

   If X or Y are sets of tuples themselves, we omit the extra nexting of
parentheses, as in ((A• , t, n, n0 ), λ, α1 , α2 ).

Definition 10.2 (Suite factoring protomorphisms from protoskeleton un-
der conditions P guaranteeing conditions Q). Fix a coverage context C =
(X, Y, Act). Let s be a suite, P and Q coverage properties relative to C, A◦
a listener-committed protoskeleton, and β ∈ X.


   We say s factors protomorphisms from (A◦ , β) under conditions P guar-
anteeing conditions Q, expressed as
                                                      s
                                (A◦ , β) : [P =⇒ Q]                           (17)
if for all λ, A• , α such that ((A• , β), λ, α) ∈ P and (adhering to the convention
adopted in Remark 7.21) A• is an assignment committed protoskeleton such
that F•→◦ (A• ) = A◦ , there is a commutative diagram
                                       Λf(A)
                                 A               - f(A)


                                       λ                  λ0                  (18)

                                                  -
                                                          ?
                                                          B
where f ∈ s(A◦ ) is assignment-transforming on (A, A) and
                        ((f(A• ), Act(A, β, f)), λ0 , α) ∈ Q.
Definition 10.3 (Suite factoring coverings from protoskeleton under condi-
tions P guaranteeing conditions Q). Fix a coverage context C = (X, Y, Act).
Let s be a suite, P and Q coverage properties relative to C, A◦ a listener-
committed protoskeleton, and β ∈ X.
    We say s factors coverings from (A◦ , β) under conditions P guaranteeing
conditions Q expressed as
                                                      s
                                (A◦ , β) : [[P =⇒ Q]]                         (19)
if for all λ, A• , α such that ((A• , β), λ, α) ∈ P there exists an operator f ∈
s(A◦ ) that is assignment-transforming on (A, A) and a λ0 such that
                         λ|Rmv(A◦ ) = (λ0 ◦ Λf(A◦ ) )|Rmv(A◦ )                (20)
and ((f(A• ), Act(A, β, f)), λ0 , α) ∈ Q.
Remark 10.4. This notion is nearly identical to the idea of a suite factoring
a protomorphism from protoskeleton w.r.t. a predicate, except that the con-
dition expressed by the commutative diagram (18) can only be considered to
                                                                        s
be true modulo listeners. Note the difference in notation: A◦ : [[P =⇒ Q]]
                                                                         s
uses double brackets, as in our notation for coverage, whereas A◦ : [P =⇒ Q]
does not.


Definition 10.5 (Test). A test of an unrealized skeleton A◦ is a pair (n, p)
where n is an unrealized node of A◦ , and p is a critical path of evt A◦ (n) in
the fragment FA◦ ,n .
                                                          R
Definition 10.6 (Equivalence modulo listeners). A◦ ≡ B◦ if and only if
Rmv(A◦ ) = Rmv(B◦ ).
                                  R
   In what follows, we only use ≡ among realized skeletons.

Definition 10.7 (Strict role-generated uniques). Let A• = (A, A) be a pre-
skeleton and let A0◦ be a protoskeleton and (ϕ, σ) be a protomorphism where
     ϕ,σ
A0◦ 99K A◦ . Then A• has strictly role-generated unique origination assump-
tions over (A0◦ , (ϕ, σ)) if UA = σ(UA0 ) ∪ UA .

Definition 10.8 (Coverage modulo listeners context). Let the cover-
age modulo listeners context CM be (Opr, (PSkel◦ × PSkel◦ ), ActM ) where
ActM (A, g, f) = f ◦ g.

Definition 10.9 (Precohort coverage property). The precohort coverage prop-
erty PCohn,p is defined with respect to the context CM , and includes the set
of 4-tuples ((A• , g), λ, B◦ , A0◦ ) such that

   • P1. A• is a preskeleton.

   • P2. B◦ is a realized skeleton.
                                                           R
   • P3. There exists B0• , a realized skeleton, with B◦ ≡ B0◦ such that λ is
                                       λ
      structure-preserving and A• 99K B0• .

   • P4. g(A0◦ ) = A◦ .

   • P5. A• has strictly role-generated unique originations assumptions over
     (A0◦ , Λg(A0◦ ) ).
                                      λ0        λ00
   • P6. For all λ0 such that A 99K C 99K B0 with λ = λ00 ◦ λ0 , p is weakly
     solved in FC,ϕ0 (n) by σ 0 where λ0 = (ϕ0 , σ 0 ).

Definition 10.10 (Cohort coverage property). The cohort coverage predicate
Coh is defined with respect to the context CM , and includes the set of 4-tuples
((A• , g), λ, B◦ , A0◦ ) such that


   • C1. A• is a skeleton.

   • P2. B◦ is a realized skeleton.
                                                                   R
   • C3. There exists B0• , a realized skeleton, with B◦ ≡ B0◦ such that
        λ
     A• →
        − B0• .

   • P4. g(A0◦ ) = A◦ .

    In the definition of the cohort coverage property, we need to allow for
existence of some B0 rather than simply use B, due to the the case in which
f adds a listener strand that had no available image in B.
    The main theorem to be established first is the completeness of the cpsa
cohort suite. This is proven given two central lemmas, which we state here
but prove later. The pre-cohort completeness lemma establishes that the pre-
cohort produces a complete (in terms of coverage) set of preskeleton outputs
that pass the solved filter.

Lemma 10.11 (Pre-cohort completeness). Let A◦ be an unrealized skeleton
                                                         PP Pn,p
and let (n, p) be any test of A◦ . Then (A◦ , Id) : [[Coh ====⇒ PCohn,p ]].

    We prove Lemma 10.11 in Section 12.
    The skeletonization completeness lemma establishes that skeletonization
is complete with regard to homomorphisms to a skeleton, and produces only
skeletons. Informally: when A → A0 where A is a skeleton but A0 is only
presumed to be a preskeleton, then any homomorphism from A to a skeleton
that factors through the map to A0 factors, further, through the linking
protomorphism of some element of the skeletonization suite on A0 .

Definition 10.12 (Ancestor-aware coverage context). Let the ancestor-aware
coverage context CA be (Protom, PSkel• , ActA ) where ActA (A, λ, f) = Λf(A) ◦λ.

Definition 10.13 (Skeleton coverage property). Let A◦0 be a skeleton. Then
the skeleton coverage property SklA0 is defined with respect to the context CA ,
and includes the set of 3-tuples ((A• , λ0 ), λ, B• ) such that

   • S1. A• is a preskeleton.

   • S2. B• is a skeleton.
              λ
   • S3. A◦0 −→
                A◦ .


              λ◦λ
   • S4. A◦0 −−→
                 B◦ .
               λ
   • S5. A• 99K B• and λ is structure-preserving.

   • S6. A• has strictly role-generated unique origination assumptions over
     (A◦0 , λ0 ).
Definition 10.14 (Skeleton homomorphism coverage property). Let A◦0 be
a skeleton. Then the skeleton homomorphism coverage property SklHomA0
is defined with respect to the context CA , and includes the set of 3-tuples
((A• , λ0 ), λ, B• ) that meet conditions S2, S3, S4, S6, and
   • SH1. A• is a skeleton.
                   λ
   • SH5. A• →
             − B• .
   In order to discuss the homomorphism check filter properly in the skele-
tonization completeness lemma, we must first describe the homomorphism
check filter in a different way. Let HCA,λ = {(A0◦ , f)|Λf (A0 ) ◦ λ is a homo-
morphism from A to f(A0 )}.
Lemma 10.15 (Skeletonization completeness). Let A◦0 be a skeleton and let
                                                                         W F ∩HCA ,λ
                                   λ                                 S           0 0
A◦ be a preskeleton such that A◦0 −→
                                     A◦ . Then (A◦ , λ0 ) : [SklA0 =========⇒
SklHomA0 ].
   We prove Lemma 10.15 in Section 11.
   From these, we can give a proof of Theorem 10.16.
Theorem 10.16 (cpsa cohort completeness). Let A◦ be an unrealized skele-
                                                            cohn,p
ton and let (n, p) be any test of A◦ . Then (A◦ , Id) : [[Coh ===⇒ Coh]].
Proof. Let A◦ be an unrealized skeleton and let (n, p) be a test of A◦ . Let
((A• , Id), λ, B◦ , A◦ ) ∈ Coh, with (B0• ) satisfying condition C3.
                                        PP
                                       Pn,pn,p
    By Lemma 10.11, (A◦ , Id) : [[Coh ====⇒ PCohn,p ]]. Let g be an assignment-
                            PP
transforming operator in Pn,pn,p and λ0 be such that ((g(A• ), g)λ0 , B◦ , A◦ ) ∈
PCohn,p and λ|Rmv(A◦ ) = (λ0 ◦ Λg(A) )|Rmv(A◦ ) . Let B00• = (B00 , B 00 ) be an
assignment-committed realized skeleton satisfying condition P3.
    We claim that the 3-tuple ((g(A• ), Λg(A) ), λ0 , B00• ) is in SklA .
   • S1. Guaranteed because (A◦ , g) ∈ W F .


   • S2. We already know B00• is a skeleton, so S2 is met.

   • S3. Guaranteed because (A◦ , g) ∈ HC.

   • S4.     We know that λ|Rmv(A◦ ) = (λ0 ◦ Λg(A) )|Rmv(A◦ ) , and we know
           λ0 ◦Λg(A)
       A◦0 99K B00◦ . As noted below, λ0 is structure-preserving, and so is
       Λg since it is a composition of linking maps of primitive operators.
       Therefore, λ0 ◦ Λg(A) is structure-preserving. Furthermore, it preserves
       points of origination, since all points of origination occur in Rmv(A◦ ).
       Therefore, λ0 ◦ Λg(A) is a homomorphism.
                       λ0
   • S5. g(A• ) 99K B00• and λ0 is structure-preserving by condition P3.

   • S6. Guaranteed because of conditions P4 and P5.

    Thus, by Lemma 10.15, there is an assignment-transforming h ∈
  W F ∩HCA,Λg(A)
S                    and a λ00 such that ((h(g(A• )), Λg(A) ◦ λ0 ), λ00 , B00• ) is in
SklHomA . Let f = h ◦ g ∈ cohn,p (A◦ ). We claim that the 4-tuple
((f(A• ), f), λ00 , B◦ , A◦ ) is in Coh.

   • C1. Guaranteed by condition SH1.

   • P2. Guaranteed by condition P2 for the 4-tuple ((A• , Id), λ, B◦ , A◦ ).

   • C3. B00• satisfies this condition. We already know B00• is a realized
                           R                                             λ00
     skeleton and that B◦ ≡ B00◦ , and condition SH5 guarantees that A• −→
     B00• .

   • P4. Applying f to A◦ gives f(A◦ ).

   We know that f ∈ S ◦ Pn,p ; we need only prove that (A◦ , f) ∈ P Pn,p . We
know (A◦ , f) ∈ W F from condition C1 and (A◦ , f) ∈ HC from condition C3.
Also, we know that (A◦ , f) ∈ SFn,p by condition P6.


### 10.1      Top-level Completeness Proof

Assuming the results of Theorem 10.16, we can prove the main completeness
result:




Theorem 10.17 (cpsa overall completeness). Let A◦ be the input to
cpsa and suppose cpsa produces a set S in a finite number of steps dur-
                                                                                 λ
ing its setwise reduction. Let HB◦ be the set of homomorphisms A◦ →              − B◦ .
Then
                    [
          [[A◦ ]] =   {(A0 , λ0 ◦ (λ|Rmv(A◦ ) ))|(A0 , λ0 ) ∈ [[B◦ ]], λ ∈ HB◦ }
                   B◦ ∈S

Proof. Let A◦ be the input to cpsa and suppose cpsa produces S during
its setwise reduction in a finite number, n, of steps. Let S1 , . . . , Sn be the
sequence of sets cpsa calculates, where S1 = {A◦ } and Sn = S. For each i
from 1 to n − 1, let A◦i , ni , pi be such that Si+1 = (Si \ {A◦i }) ∪ cohni ,pi [A◦i ],
where A◦i = SEARCH(Si ) and (ni , pi ) = T EST (Ai ).
    Now we must prove that
                    [
          [[A◦ ]] =   {(A0 , λ0 ◦ (λ|Rmv(A◦ ) ))|(A0 , λ0 ) ∈ [[B◦ ]], λ ∈ HB◦ }.
                   B◦ ∈S

   Let (A0 , µ) ∈ [[A◦ ]], and let B0• be any realized skeleton such that
                                                                 ν
Rmv(B0◦ ) = A0 , and let A• and ν be such that A• →              − B0• such that
ν|Rmv(A◦ ) = µ.
   We define a sequence of tuples (C•i , λi , B•i , νi ) such that
((C•i , Id), νi , B0◦ , C◦i ) ∈ Coh where (B•i ) satisfies condition C3, such
            λi
that A• −   → C•i , and (νi ◦ λi )|Rmv(A◦ ) = µ. The sequence is defined as follows:

   • B•1 = B0• , C•1 = A• , λ1 = ΛId , and ν1 = ν. The tuple (C•1 , λ1 , B•1 , ν1 )
     clearly has the required properties.

   • If C◦i 6= A◦i then C•i+1 = C•i , B•i+1 = B•i , λi+1 = λi , and νi+1 = νi . All
     required properties of the tuple are clear.

   • If C◦i = A◦i , then by Theorem 10.16 there is an f ∈ cohni ,pi (A◦i ) and a
     νi+1 such that ((f(C•i ), f), νi+1 , B0◦ , C◦i ) ∈ Coh and a B•i+1 that satisfies
     the conditions of property C3. Note that ((f(C•i ), Id), νi+1 , B0◦ , f(C◦i )) ∈
     Coh and the same B•i+1 satisfies conditions C3, because the only con-
     dition affected by the changed fields is P4.
      Define C•i+1 = f(C•i ) and define λi+1 = Λf(Ai ) ◦ λi . Then the tuple
      (C•i+1 , λi+1 , B•i+1 , νi+1 ) has the required properties:




         – We already know ((f(C•i ), Id), νi+1 , B0◦ , f(C◦i )) ∈ Coh where (B•i+1 )
           satisfies condition C3.
         – We know that (νi+1 ◦ Λf(Ai ) )|Rmv(A◦i ) = νi |Rmv(A◦i ) and (νi ◦
           λi )|Rmv(A◦ ) = µ. Because λi is a homomorphism of listener-
           committed skeletons, all non-listener strands of A◦ map to non-
           listener strands of A◦i . Thus, (νi+1 ◦ Λf(A◦i ) ◦ λi )|Rmv(A◦ ) = (νi ◦
           λi )|Rmv(A◦ ) = µ, and since Λf(A◦i ) ◦ λi = λi+1 , we have that
           (νi+1 ◦ λi+1 )|Rmv(A◦ ) = µ.

     Thus, we have (C•n , λn , B•n , νn ) with these properties, where C◦n ∈ Sn = S.
                       νn
Note that since C◦n −→       B◦n where B◦n is realized, (Rmv(B◦n ), νn |Rmv(C◦n ) ) ∈
   ◦
[[Cn ]]. Furthermore, λn ∈ HC◦n and (νn ◦ λn )|Rmv(A◦ ) = µ. Since λn is a
homomorphism of listener-committed skeletons, all non-listener strands of
A◦ map to non-listener strands of C◦n , so (νn |Rmv(C◦n ) ◦ λn )|Rmv(A◦ ) = (νn ◦
λn )|Rmv(A◦ ) = µ.
     This proves that [[A◦ ]] ⊆ B◦ ∈S {(A0 , λ0 ◦ (λ|Rmv(A◦ ) ))|(A0 , λ0 ) ∈ [[B◦ ]], λ ∈
                                  S
HB◦ }. To prove equality we must also establish the other inclusion.
    Suppose (A0 , µ) ∈ [[B◦ ]] where B◦ ∈ S, and suppose λ ∈ HB◦ . We know
     λ                                                   ν
A◦ →− B◦ . Let B0◦ and ν be such that B◦ →               − B0◦ , Rmv(B0◦ ) = A0 , and
                             ν◦λ
µ = ν|Rmv(B◦ ) . Then A◦ −−→ B0◦ , and (ν◦λ)|Rmv(A◦ ) = (µ◦(λ|Rmv(A◦ ) )) because
λ is a homomorphism of listener-committed skeletons. Thus, (Rmv(B0◦ ), (µ ◦
(λ|Rmv(A◦ ) ))) = (A0 , (µ ◦ (λ|Rmv(A◦ ) ))) ∈ [[A◦ ]]. This completes the proof.



## 11      Skeletonization

In this section we prove Lemma 10.15.
Definition 11.1 (Ancestor-aware coverage context with term and node
pair). Let N be the set of nodes appearing in members of PSkel. Let
the ancestor-aware coverage context with term and node pair CA2 be
((Protom × A × N × N ), PSkel• , ActA2 ) where ActA2 (A, (t, n, n0 , λ), f) =
(σf(A) (t), ϕf(A) (n), ϕf(A) (n0 ), Λf(A) ◦ λ).
Definition 11.2 (Unique origination issue coverage property). Let A◦0 be
                             λ0
a skeleton and let A◦0 −→         A◦ . Then the unique origination issue coverage
property UrIA0 is defined with respect to the context CA2 , and includes the set
of 3-tuples ((A• , t, n, n0 , λ0 ), λ, B• ) such that ((A◦ , λ0 ), λ, B• ) ∈ SklA0 and


    • UI1. n and n0 are distinct and are both points of origination of t in A.
    The unique origination issue predicate refers to coverage (in the same
sense as the skeleton coverage) in which there is a violation of a unique
origination specification (n, t, t0 ). The next predicate indicates the same kind
of coverage but with the violation resolved.
Definition 11.3 (Unique origination issue resolved coverage property). Let
                                 λ0
A◦0 be a skeleton and let A◦0 −→      A◦ . Then the unique origination issue resolved
property UrRA0 is defined with respect to the context CA2 , and includes the
set of 3-tuples ((A• , t, n, n0 , λ0 ), λ, B• ) such that ((A◦ , λ0 ), λ, B• ) ∈ SklA0 and
    • UR1. n = n0 or one of n, n0 are not points of origination of t in A.
    First we state a main lemma about the unique origination rectification
suite:
Lemma 11.4 (ur-universality). Let A◦0 be a skeleton and let A◦ be a pre-
                               λ0
skeleton such that A◦0 −→           A◦ . Let t be a term in UA and let n and n0 be
distinct nodes in A which are both points of origination of t in A. Then
                                urt,n,n0
(A◦ , t, n, n0 , λ0 ) : [UrIA0 ====⇒ UrRA0 ].
    In other words, urt,n,n0 can resolve unique origination issues while main-
taining skeleton coverage.
    The proof is largely split into two cases: one for using the merging suite
and one for using the deorigination suite. With a little work these can be
their own lemmas.
Definition 11.5 (Unique origination issue (merging) coverage property). Let
                                 λ0
A◦0 be a skeleton and let A◦0 −→      A◦ . Then the unique origination issue (merg-
ing) predicate UrIMA0 is defined with respect to the context CA2 , and includes
the set of 3-tuples ((A• , t, n, n0 , λ0 ), λ, B• ) such that ((A• , t, n, n0 , λ0 ), λ, B• ) ∈
UrIA0 and
    • UIM1. ϕ(n) = ϕ(n0 ) where λ = (ϕ, σ).
Definition 11.6 (Unique origination issue (deorig) coverage property). Let
                                  λ0
A◦0 be a skeleton and let A◦0 −→       A◦ . Then the unique origination issue (de-
orig) predicate UrIDA0 is defined with respect to the context CA2 , and includes
the set of 3-tuples ((A• , t, n, n0 , λ0 ), λ, B• ) such that ((A• , t, n, n0 , λ0 ), λ, B• ) ∈
UrIA0 and


    • ¬UIM1. ϕ(n) 6= ϕ(n0 ) where λ = (ϕ, σ).
Lemma 11.7 (Merging universality). Let A◦0 be a skeleton and let A◦ be a
                           λ0
preskeleton such that A◦0 −→  A◦ . Let t be a term in UA and let n and n0
be distinct nodes in A which are both points of origination of t in A. Then
                               Mt,n,n0
(A◦ , t, n, n0 , λ0 ) : [UrIMA0 ====⇒ UrRA0 ].
                                                                                   λ
Proof. Let A◦0 be a skeleton and let A◦ be a preskeleton such that A◦0 −→            0
                                                                                       A◦ .
Let t be a term in UA and let n and n0 be distinct nodes in A which are both
points of origination of t in A. Suppose we have ((A• , t, n, n0 , λ0 ), λ, B• ) ∈
UrIA0 , and let (ϕ, σ) = λ and (s, i) = n.
    Observe that n and n0 are in different strands (since each strand can only
originate any atom once), and that ϕ maps these two strands to the same
strand in B◦ . Let l be the minimum of the lengths of strands s and s0 in A.
Then in order for (ϕ, σ) to be a well-defined protomorphism, it must be that
σ is a unifier of msg A (s, j) and msg A (s0 , j) for every 1 ≤ j ≤ l. Let σ0 be a
most general unifier of Θ(s)|l with Θ(s0 )|l such that σ = σ 0 ◦ σ0 for some σ 0 .
    Let f = Comps,s0 ◦ Subσ0 ∈ Mt,n,n0 (A◦ ). Let (ϕf , σf ) = Λf(A◦ ) . Let ϕ0 be
defined strandwise on f(A◦ ) so that ϕ0 (ϕf (s)) = ϕ(s) for all s; note that this is
possible in f(A) since ϕ(s) = ϕ(s0 ). Note that since (ϕ, σ) is a protomorphism
of assignment-committed protoskeletons, A assigns both s and s0 to the same
role, so f in this situation is assignment-transforming.
    Then we claim that ((f(A• ), σf (t), ϕf (n), ϕf (n0 ), Λf(A) ◦λ0 ), λ0 , B• ) ∈ UrRA0 ,
where λ0 = (ϕ0 , σ 0 ). We have that ϕf (n) = ϕf (n0 ), so it remains for us to prove
that ((f(A• ), Λf(A◦ ) ◦ λ0 ), λ0 , B• ) ∈ SklA0 . We proceed through each require-
ment in the definition of the skeleton coverage predicate:
    • S1. f(A• ) is a preskeleton by Theorem 8.16.

    • S2. Guaranteed because ((A• , λ0 ), λ, B• ) ∈ SklA0 .

    • S3. We must prove Λf(A◦ ) ◦ λ0 is structure-preserving and that it
      preserves points of origination. The former property is guaranteed
      since f is a composition of primitive operators and because λ0 is
      structure-preserving. Furthermore, it preserves points of origination
      by Lemma 7.25.

    • S4. λ0 ◦ Λf(A◦ ) ◦ λ0 = λ ◦ λ0 , and by property S4 we previously know
                 λ◦λ
      that A◦0 −−→
                   B◦ .


    • S5. We know λ is a protomorphism of assignment-committed proto-
      skeletons; only the compression operator could have an effect on this,
      and we have already remarked that the two strands we compress both
      were assigned to the same role.
      Let ≺ refer to ≺A◦ . Let ≺M be such that n ≺M n0 only when n = (s, i)
      and n0 = (s0 , j) or n = (s0 , i) and n0 = (s, j) for some i < j. The
      ordering ≺f(A◦ ) is the transitive closure of ≺ ∪ ≺M . Thus, n ≺f(A◦ ) n0 if
      and only if we can define a sequence n = n0 , n1 , . . . , nl = n0 such that
      for every 1 ≤ i ≤ l, ni−1 ≺ ni or ni−1 ≺M ni .
      If ni−1 ≺M ni , then ϕ0 (ni−1 ) ≺B ϕ0 (ni ) because ϕ0 (ni−1 ) will precede
      ϕ0 (ni ) in the same strand in B. If ni−1 ≺A ni then ϕ0 (ni−1 ) ≺ ϕ0 (ni )
      because ϕ0 (ni−1 ) = ϕ(ni−1 ) and ϕ0 (ni ) = ϕ(ni ), and λ is structure-
      preserving. So we have that ϕ(n) = ϕ(n0 ) ≺B . . . ≺B ϕ(nl ) = ϕ(n0 )
      and so ϕ(n) ≺B ϕ(n0 ) because ≺B is transitive.

    • S6. We know that f(A• ) has strictly role-generated unique origination
      assumptions over (A0 , Λf(A◦ ) ◦ λ0 ) because (A• ) did over (A◦0 , λ0 ) and
      Uf(A◦ ) = σf(A◦ ) (UA◦ ).


Lemma 11.8 (Deorigination universality). Let A◦0 be a skeleton and let A◦
                                λ0
be a preskeleton such that A◦0 −→  A◦ . Let t be a term in UA and let n and n0
be distinct nodes in A which are both points of origination of t in A. Then
                               Dt,n,n0
(A◦ , t, n, n0 , λ0 ) : [UrIDA0 ====⇒ UrRA0 ].
                                                                                    λ
Proof. Let A◦0 be a skeleton and let A◦ be a preskeleton such that A◦0 −→         0
                                                                                      A◦ .
Let t be a term in UA and let n and n be distinct nodes in A which are both
points of origination of t in A. Suppose we have ((A• , t, n, n0 , λ0 ), λ, B• ) ∈
UrIA0 , and let (ϕ, σ) = λ and (s, i) = n.
    Since B is a skeleton, σ(t) cannot originate at both ϕ(n) and ϕ(n0 ). With-
out loss of generality, assume that ϕ(n) is not a point of origination of σ(t)
in B.
    Note that σ(t) is carried at node ϕ(n) so it must be that there is an earlier
node (s, i0 ) ≺ n such that σ(t) is the termination point of a carried path
(msg B (ϕ(s, i0 )), π). Let π 0 be the largest prefix of π such that (msg A◦ (s, i0 ), π 0 )
is a well-defined path; note also that this path is a carried path. Then either
π = π 0 or (msg B◦ (s, i0 ), π 0 ) terminates at a variable m of sort mesg. (Note


that in the latter case we are guaranteed to terminate at a variable of sort
mesg because of the stipulation that the path is carried.) In the former
case, σ is a unifier of the endpoint of (msg A (s, i0 ), π) with t, and in the latter
case σ is a unifier of m with a term that carries t. Either way, we can write
σ = σ 0 ◦ σ0 where f = Subσ0 ∈ Dt,n,n0 (A◦ ). Let ϕ0 = ϕ.
    We will show that ((f(A• ), σ0 (t), n, n0 , Λf(A) ◦ λ0 ), λ0 , B• ) ∈ UrRA0 , where
λ0 = (ϕ0 , σ 0 ). We know that σ0 (t) is carried in msg f(A◦ ) (s, i0 ), so σ0 (t) does
not originate at node n in f(A◦ ), so we need only prove that ((f(A• ), Λf(A) ◦
λ0 ), λ0 , B• ) ∈ SklA0 . We proceed through each requirement in the definition
of the skeleton coverage predicate:
   • S1. f(A• ) is a preskeleton by Theorem 8.16.
   • S2. Guaranteed because ((A• , λ0 ), λ, B• ) ∈ SklA0 .
   • S3. We must prove Λf(A◦ ) ◦ λ0 is structure-preserving and that it
     preserves points of origination. The former property is guaranteed
     since f is a composition of primitive operators and because λ0 is
     structure-preserving. Furthermore, it preserves points of origination
     by Lemma 7.25.
   • S4. λ0 ◦ Λf(A◦ ) ◦ λ0 = λ ◦ λ0 , and by property S4 we previously know
                λ◦λ
      that A◦0 −−→
                   B◦ .
   • S5. Since it is the same as λ on strands, we already know λ0 is a
     protomorphism of assignment-committed protoskeletons. Furthermore,
     the orderings in f(A) are the same as the orderings in A, so λ0 must be
     structure-preserving.
   • S6. We know that f(A• ) has strictly role-generated unique origination
     assumptions over (A0 , Λf(A◦ ) ◦ λ0 ) because (A• ) did over (A◦0 , λ0 ) and
     Uf(A◦ ) = σf(A◦ ) (UA◦ ).


   We now give the proof of Lemma 11.4.
proof of Lemma 11.4. Let A◦0 be a skeleton and let A◦ be a preskeleton such
            λ0
that A◦0 −→       A◦ . Let t be a term in UA and let n and n0 be distinct nodes
in A which are both points of origination of t in A. Suppose we have
((A• , t, n, n0 , λ0 ), λ, B• ) ∈ UrIA0 , and let (ϕ, σ) = λ and (s, i) = n.


       The proof proceeds by cases. One of the following must be the case:
   Case 1: ϕ(n) = ϕ(n0 ). In this case, ((A• , t, n, n0 , λ0 ), λ, B• ) ∈ UrIA0 , so by
   Lemma 11.7 there exists an f ∈ Mt,n,n0 (A◦ ) ⊂ urt,n,n0 (A◦ ) and a λ0 such that
   ((f(A• ), f(t), f(n), f(n0 ), f(λ0 )), λ0 , B• ) ∈ UrRA0 and such that λ = λ0 ◦ Λf(A) .
   Case 2: ϕ(n) 6= ϕ(n0 ). In this case, ((A• , t, n, n0 , λ0 ), λ, B• ) ∈ UrIA0 , so
   by Lemma 11.8 there exists an f ∈ Dt,n,n0 (A◦ ) ⊂ urt,n,n0 (A◦ ) and a λ0 such
   that ((f(A• ), f(t), f(n), f(n0 ), f(λ0 )), λ0 , B• ) ∈ UrRA0 and such that λ = λ0 ◦
   Λf(A) .
      Next, we prove a lemma about the order enrichment operator.

   Definition 11.9 (Skeleton coverage without unique origination issues). Let
   A◦0 be a skeleton. Then skeleton coverage without unique origination issues,
   SklUA0 , is defined with respect to the context CA , and includes the set of
   3-tuples ((A• , λ0 ), λ, B• ) in SklA0 such that N U O(A) = ∅.

   Lemma 11.10 (Order enrichment). Let A◦0 be a skeleton and let A◦ be a
                              λ0                                 oe
   preskeleton such that A◦0 −→  A◦ . Then (A◦ , λ0 ) : [SklUA0 =⇒ SklHomA0 ],
   where oe = {OE}.
                                                                                  λ
   Proof. Let A◦0 be a skeleton and let A◦ be a preskeleton such that A◦0 −→      0
                                                                                    A◦ .
   Let λ0 = (ϕ0 , σ0 ) and let λ = (ϕ, σ).
       Let ((A• , λ0 ), λ, B• ) ∈ SklUA0 . Then we claim that ((OE(A• ), λ0 ), λ, B• ) ∈
   SklHomA0 ; note that ΛOE(A◦ ) ◦ λ0 = λ0 . We need only establish that OE(A• )
   is a skeleton and that λ is a homomorphism.
       We know that OE(A◦ ) is a preskeleton by Theorem 8.16. To prove that
   OE(A◦ ) is a skeleton, we need to check two things: first, that each uniquely-
   originating atom originates on exactly one strand, and second, that the node
   of origination precedes each other node that carries that atom. The latter
   condition is guaranteed because all such instances of that requirement are
   ensured to be in the ordering after applying OE.
       Each uniquely-originating atom originates on at most one strand in A◦
   since NUO(A) = ∅. To prove that each uniquely-originating atom orig-
   inates on at least one strand, we appeal to the fact that A• has strictly
   role-generated unique origination assumptions over (A◦0 , λ0 ). For every t in
   Uf(A◦ ) , either:

Case 1: There exists a t0 ∈ UA◦0 such that t = σ0 (t). In this case, because
        A0 is a skeleton, t0 must originate at a node n ∈ A0 . Therefore, t


          originates at ϕ0 (n); this point of origination must be preserved because
          it is preserved under an extension, namely λ ◦ λ0 .

Case 2: There exists a strand s ∈ OE(A◦ ) with A(s) = (ρs , σs ), and a t0 ∈ Uρs
        such that σs (t0 ) = t, such that t0 originates in Cρs | len(ΘOE(A◦ ) (s)) at
        event i. Since OE(A◦ ) is a preskeleton, σs (t) originates in OE(A◦ ) at
        (s, i).

        Next we must prove that λ is a homomorphism.
        First we prove that λ preserves points of origination. Let t ∈ UOE(A◦ ) and
    let n be a point of origination of t in OE(A◦ ). There are two cases. Either:

Case 1: There is a t0 ∈ UA0 and a point n0 ∈ A0 such that σ0 (t0 ) = t and
        t0 originates at n0 in A0 . This point of origination must be preserved
        because it is preserved under λ ◦ λ0 .

Case 2: Let n = (s, i0 ). Then A(s) = (ρs , σs ), and there is a t0 ∈ Uρs such
        that σs (t0 ) = t and such that t0 originates in Cρs | len(ΘA◦ (s)) at event
        i. Since OE(A◦ ) is a preskeleton, σs (t) originates in OE(A◦ ) at (s, i),
        and thus i0 = i. Since λ is a protomorphism of assignment-committed
        protoskeletons, and since B• is a preskeleton, σ(t) must originate at
        node ϕ(n).

        These cases are exhaustive since A• has strictly role-generated unique
    origination assumptions over (A0 , λ0 ), and thus so does OE(A• ) since it only
    differs from A• in its orderings.
        All that is left is to prove that λ is a structure-preserving protomor-
    phism from OE(A◦ ) to B◦ . We already know that λ is a structure-preserving
    protomorphism from A◦ to B◦ , because we know ((A◦ , λ0 ), λ, B• ) ∈ SklA0 .
    However, OE(A◦ ) may have additional orderings and we must prove these
    are preserved under λ.
        Let ≺ refer to ≺A◦ , that is, ≺ refers to the ordering before order-enrichment.
    Let ≺OE be such that n ≺OE n0 where n, n0 ∈ OE(A◦ ) if and only if there
    is a t ∈ UOE(A◦ ) that originates at n and is carried at n0 6= n. Recall that
    ≺OE(A◦ ) is the transitive closure of ≺ ∪ ≺OE . Thus, n ≺OE(A◦ ) n0 if and
    only if we can define a sequence n = n0 , n1 , . . . , nl = n0 such that for every
    1 ≤ i ≤ l, ni−1 ≺ ni or ni−1 ≺OE ni .
        If ni−1 ≺OE ni , there is a term ti−1 originating at ni−1 in f(A◦ ) that is
    carried at ni . Since λ preserves points of origination, σ(ti−1 ) ∈ UB , σ(ti−1 )


originates at ϕ(ni−1 ) in B, and is carried at ϕ(n0i ) in B. Since B is a skeleton,
ϕ(ni−1 ) ≺B ϕ(ni ). Of course, if ni−1 ≺ ni then ϕ(ni−1 ) ≺B ϕ(ni ) since λ is
structure preserving from A◦ to B◦ . So we have that ϕ(n) = ϕ(n0 ) ≺B . . . ≺B
ϕ(nl ) = ϕ(n0 ) and so ϕ(n) ≺B ϕ(n0 ) because ≺B is transitive. This completes
the proof.
   Now we can prove Lemma 10.15.

Lemma 10.15 (Skeletonization completeness). Let A◦0 be a skeleton and let
                                                                                  W F ∩HCA ,λ
                                        λ                                     S           0 0
A◦ be a preskeleton such that A◦0 −→
                                     A◦ . Then (A◦ , λ0 ) : [SklA0 =========⇒
SklHomA0 ]
                                                                                      λ
Proof. Let A◦0 be a skeleton and let A◦ be a preskeleton such that A◦0 −→   0
                                                                              A◦ ,
and assume ((A• , λ0 ), µ, B• ) ∈ SklA0 .
    We define a sequence of tuples ((A•i , λi ), µi , B• , fi ) with 1 ≤ i ≤ k as
follows:

   1. A•1 = A• , λ1 = λ0 , µ1 = µ. Note that ((A•1 , λ1 ), µ1 , B• ) ∈ SklA0 . We do
      not yet define f1 ; nonetheless, note that µ1 = µ◦(Λfi−1 (A◦i−1 ) ◦. . .◦Λf1 (A◦1 ) )
      for i = 1, since the sequence is empty.

   2. For i ≥ 1, if NUO(Ai ) is nonempty, let (ti , ni , n0i ) be U OI(A).
      We know that ((A•i , ti , ni , n0i , λi ), µi , B• ) ∈ UrIA0 . By Lemma 11.4
      that there is an fi ∈ urti ,ni ,n0i (A◦i ) and a µi+1 such that
      ((fi (A•i ), fi (ti ), fi (ni ), fi (n0i ), fi (λi )), µi+1 , B• ) ∈ UrRA0 and µ = µi ◦
      (Λfi−1 (A◦i−1 ) ◦ . . . ◦ Λf1 (A◦1 ) ).
      If we let A•i+1 = fi (A•i ) and λi+1                     =     Λfi (A◦i ) ◦ λi then
      ((A•i+1 , λi+1 ), µi+1 , B• ) ∈ SklA0 .

   3. If i ≥ 1 but NUO(Ai ) is empty then let k = i and let fi = Id.

    By assuming that a k exists we are effectively assuming that this part of
skeletonization terminates in finitely many steps. However, it clearly must: at
every step, the sum of the heights of each point of origination of a uniquely
originating term is strictly decreasing, because when we use the merging
suite, we reduce the sum by the height of one of the origination points that
merge, and when we use the deorigination suite, we either destroy a point
of origination without replacing it, or we replace it at an earlier node in the
same strand.


    Note that fk ∈ ur(A◦k ) since NUO(Ak ) = ∅. Also note that for 1 ≤ i < k, if
fk ◦. . .◦fi+1 ∈ ur(A◦i+1 ) then fk ◦. . .◦fi ∈ ur(A◦i ). Therefore let g = fk ◦. . .◦f1 ∈
ur(A◦1 ) = ur(A◦ ), and let f = OE ◦ g ∈ S(A◦ ). Note that as a composition of
assignment-transforming operators, f is assignment-transforming.
    Note that we already know that ((g(A• ), Λg(A◦ ) ◦ λ0 ), µ0 , B• ) ∈ SklUA0 .
Therefore, ((f(A• ), Λf(A◦ ) ◦ λ0 ), µ0 , B• ) ∈ SklHomA0 by Lemma 11.10.
    We must only prove that (A◦ , f) ∈ W F ∩ HCA0 ,λ0 . f(A◦ ) is clearly a
preskeleton by Theorem 8.16. Also, Λf(A◦ ) ◦ λ0 is a homomorphism since
((f(A• ), λ), µ0 , B• ) ∈ SklHomA0 .
                                                                W F ∩HCA ,λ
                                                            S           0 0
    This completes the proof that (A◦ , λ0 ) : [SklA0 =========⇒ SklHomA0 ].




## 12      Pre-Cohort Completeness

In this section we build up to a proof of Lemma 10.11.


### 12.1      Preliminaries

First, some definitions. Earlier we defined cohort coverage and precohort cov-
erage, which were defined in terms of a protomorphism to a realized skeleton
remove-equivalent to a target. In two of the main lemmas needed to prove
Lemma 10.11, we get factorization of the homomorphism to the same target;
we only need that flexibility for the case where we employ listener augmen-
tation. As a precursor to the definitions we use for these two lemmas, we
first define direct cohort and precohort coverage.
Definition 12.1 (Direct coverage context). Let the direct coverage context
CD be (Opr, (PSkel• × PSkel◦ ), ActD ) where ActD (A, g, f) = f ◦ g.
Definition 12.2 (Direct cohort coverage). The direct cohort coverage prop-
erty DCoh is defined with respect to the context CD , and includes the set of
4-tuples ((A• , g), λ, B• , A0◦ ) such that:
    • DC1 A• is a skeleton.

    • DC2 B• is a skeleton.
                 λ
    • DC3 A• →
             − B• .


   • DC4 g(A0◦ ) = A◦ .

Definition 12.3 (Direct precohort coverage). The direct precohort coverage
property DPCohn,p is defined with respect to the context CD , and includes the
set of 4-tuples ((A• , g), λ, B• , A0◦ ) such that:

   • DPC1 A• is a preskeleton.

   • DC2 B• is a skeleton.
                  λ
   • DPC3 A• 99K B• , where λ is structure-preserving.

   • DC4 g(A0◦ ) = A◦ .

   • DPC5 A• has strictly role-generated unique origination assumptions
     over (A0◦ , Λg(A0◦ ) ).
                                        λ0     λ00
   • DPC6. For all λ0 such that A 99K C 99K B with λ = λ00 ◦ λ0 , p is weakly
     solved in FC,ϕ0 (n) by σ 0 where λ0 = (ϕ0 , σ 0 ).

    The three main lemmas in this section will correspond to the contraction,
regular augmentation, and listener augmentation suites. In each case, we
will state the lemma as a suite factoring statement; the conditions before
will be more specific than cohort coverage (or direct cohort coverage) and
the conditions after will be either precohort or direct precohort coverage.


### 12.2     Contractions

For the contraction case, the condition that guarantees a contraction will
work is the following:

Definition 12.4 (Direct cohort coverage with test destroyed). Let A◦ be an
unrealized skeleton and let (n, p) be a test. Then the direct cohort coverage
with test destroyed coverage property DCohTDn,p is defined with respect to
the context CD , and includes the set of 4-tuples ((A• , g), λ, B• , A0◦ ) such that
((A• , g), λ, B• , A0◦ ) ∈ DCoh and

   • TD1 σ(p) visits σ(Esc(FA◦ ,n , ep )), where (ϕ, σ) = λ.

   This allows us to state and prove the completeness lemma for the con-
traction suite.


Lemma 12.5 (Contraction completeness). Let A◦ be an unrealized skeleton
                                                        cHC
                                                         n,p
and let (n, p) be a test. Then (A◦ , Id) : [DCohTDn,p ==⇒ DPCohn,p ].

Proof. Let ((A• , Id), λ, B• , A◦ ) ∈ DCohTDn,p , where λ = (ϕ, σ) and p =
(t, π). Let p0 = (σ(t), π). Since we know p0 visits σ(Esc(FA,n , ep )), σ unifies
a b visited by p and an a in Esc(FA,n , ep ). Therefore, there is a σ0 ∈ ∪S∈Z S
such that σ0 unifies a and b, and such that σ = σ 0 ◦ σ0 for some σ 0 , and
Subσ0 ∈ cn,p . Let f = Subσ0 , and let λ0 = (ϕ, σ 0 ).
    We claim that ((f(A• ), f), λ0 , B• , A◦ ) ∈ DPCohn,p .

  1. DPC1 is guaranteed by Theorem 8.16.

  2. DC2 is known since ((A• , Id), λ, B• , A◦ ) ∈ DCohTDn,p .

  3. DPC3 Whether λ0 is a structure-preserving protomorphism or not, and
     whether it is a protomorphism of assignment-committed protoskeletons
     or not, depends only on its strand mapping, ϕ. Since λ is a homomor-
     phism, it has these properties and thus so does λ0 .

  4. DC4 is obvious.

  5. DPC5 Since Uf(A) = UA , all unique origination assumptions are directly
     inherited, so this condition is met.

  6. DPC6 Note that since σ0 unifies a and b, it is immediately clear that
     (σ0 (t), π) visits σ0 (Esc(FA,n , ep )). By Remark 9.14, this remains true
     under any extension.
                                     Λf(A)
    We need only prove that A◦ −−−→ f(A). It is obvious that Λf(A) is
structure-preserving, and by Lemma 7.25, since λ preserves points of origi-
nation, so does Λf(A) .




### 12.3     Listener Augmentation

Next, we address the case of listener augmentation. For this suite, we cannot
make use of direct versions of our coverage properties, because if we add a
listener but no corresponding listener is present in B, there is no homomor-
phism. Rather, we find a proper place to add a listener to B.


Definition 12.6 (Cohort coverage with certain values derivable). Let A◦
be a skeleton and let (n, p) be a test and let ep be the endpoint of p. The
cohort coverage with certain values derivable coverage property CohCVDn,p
is defined with respect to the context CM , and includes the set of 4-tuples
((A• , g), λ, B◦ , A0◦ ) in Coh such that
   • CVD. Let λ = (ϕ, σ). Then either:
         – EL. There exists {|c|}u ∈ Esc(FA,n , ep ) such that inv(σ(u)) ∈ SFB0 ,ϕ(n) .
         – CL. ep = {|c|}u and σ(u) ∈ SFB0 ,ϕ(n) .

Lemma 12.7 (Listener augmentation completeness). Let A◦ be an unrealized
                                                                     lHC
                                                                      n,p
skeleton and let (n, p) be a test. Then (A◦ , Id) : [[CohCVDn,p ==⇒ PCohn,p ]].
Proof. Let ((A• , Id), λ, B◦ , A◦ ) be in CohCVDn,p with λ = (ϕ, σ). Let B0•
satisfy condition C3. There are two cases: either EL holds or CL holds. Let
s? be N AM E(A). Let s0? ∈     / IB0 .
    If condition EL holds for {|c|}u ∈ Esc FA,n , ep then let f = Augn,lsn,2,σ? ,s?
where σ ? maps the m in the listener role to inv(u). Note that f ∈ esln,p (A◦ ).
In this case, let t = inv(u). Note that σ(t) ∈ D(PB0 ,ϕ(n) ) = SFB0 ,ϕ(n) because
σ(inv(u)) = inv(σ(u)) as u is not a variable of sort mesg.
    If condition CL holds then let f = Augn,£,2,σ? ,s? where σ ? maps the m in
the listener role to u. Note that f ∈ cpln,p (A◦ ). In this case, let t = u. Note
that σ(t) ∈ SFB0 ,ϕ(n) by condition CL.
    Either way, note that f ∈ ln,p (A◦ ). Let λ0 = (ϕ0 , σ) where ϕ0 = ϕ on
all strands in A• and ϕ0 (s? ) = s0? . Let f 0 = Fn,(s0? ,1) ◦ Augϕ(n),£,2,σ◦σ? ,s0? ,
where Fn,n0 is a (non-primitive) operator that forces all transmissions before
n to be before n0 . Formally, Fn,n0 (A, A) = ((IA , ΘA , ≺0 , NA , UA ), A) where ≺0
is the transitive closure of ≺A ∪ ≺n,n0 where n1 ≺n,n0 n0 whenever n1 is a
transmission node such that n1 ≺A n.
    We claim that ((f(A• ), f), λ0 , B◦ , A◦ ) ∈ PCohn,p , with f 0 (B0• ) satisfying
condition P3.
   • P1. We know f(A• ) is a preskeleton by Theorem 8.16.
   • P2. B◦ is a realized skeleton because ((A• , (Id)), λ, B◦ , A◦ ) ∈ Coh.
   • P3. To see that f 0 (B0• ) is a skeleton, we need to establish that the nodes
     in s0? are ordered after all the points of origination of any uniquely-
     originating atoms they carry. However, we know that σ(t) ∈ D(PB0 ,ϕ(n) )


      and thus every uniquely-originating atom carried by σ(t) is also carried
      by a transmission prior to n in B0 . Since B0 is a skeleton, the origination
      point of that atom is before that transmission, and that transmission is
      before both nodes in the new listener in f 0 (B0• ). The only reception in
      f 0 (B0• ) not in B• is the reception in the listener strand s0? , of σ(t), and
      σ(t) ∈ D(PB0 ,ϕ(n) ). Since Pf 0 (B0 ),(s0? ,1) = PB0 ,ϕ0 (n) , σ(t) ∈ D(Pf 0 (B0 ),(s0? ,1) ),
      so the additional reception is realized, and all other receptions in f 0 (B0 )
      are realized because they are realized in B0 . Therefore, B0• is realized.
                                              R                             R
      It should be obvious that B0◦ ≡ f 0 (B0◦ ) and thus B◦ ≡ f 0 (B0◦ ).
                                                                                 λ0
      It should be clear that λ0 is a protomorphism f(A• ) 99K f 0 (B0• ); the
      only role not known to be preserved by the fact that λ is assignment-
      preserving is the role of s? which is lsn in both f(A• ) and f 0 (B0• ). λ0
      is structure-preserving: if n1 ≺ n2 in f(A• ) there are two possibilities.
      The first is that n1 , n2 ∈ A• in which case, λ0 maps both n1 and n2
      just as λ does, and since λ is structure-preserving, ϕ0 (n1 ) ≺B0 ϕ0 (n2 )
      so ϕ0 (n1 ) ≺f 0 (B0 ) ϕ0 (n2 ). The other is that n1 is in the strand s? and
      n  n2 . But then ϕ0 (n1 ) is in the strand s? and since n, n2 ∈ A• ,
      ϕ0 (n) ≺f 0 (B0 ) ϕ0 (n2 ), and since by the operation of Aug, ϕ0 (n1 ) ≺f 0 (B0 )
      ϕ0 (n), we have that ϕ0 (n1 ) ≺f 0 (B0 ) ϕ0 (n2 ).

   • P4 is obvious.

   • P5 is true because since £ has no uniquely originating atoms, Uf(A) =
     UA .

   • P6 Since t is in SFf(A),n , we meet either condition Sol3 or Sol4 of Defi-
     nition 5.5. By Remark 9.14 this remains true in any extension.

   Furthermore, λ|Rmv(A◦ ) = (λ0 ◦ Λf(A) )|Rmv(A◦ ) because Λf(A) |Rmv(A◦ ) is the
identity and λ0 is the same as λ on all strands in A.
                                              Λf(A)
    We need only prove that A◦ −−−→ f(A). It is obvious that Λf(A) is
structure-preserving. Since Λf(A) is the identity homomorphism on the al-
gebra, it preserves points of origination.
                                   ln,p
    Thus, (A◦ , Id) : [[CohCVDn,p ==⇒ PCohn,p ]].






### 12.4     Regular Augmentation

Third, we address the case of regular augmentation. Here, we can use the
direct form of coverage again, but this time we make very strong assumptions
about B.

Definition 12.8 (Direct cohort coverage with good augmentation candi-
date). Let A◦ be an unrealized skeleton and let (n, p) be a test. Then the di-
rect cohort coverage with good augmentation candidate property DCohGACn,p
is defined with respect to the context CD , and includes the set of 4-tuples
((A• , g), λ, B• , A0◦ ) with λ = (ϕ, σ) such that ((A• , g), λ, B• , A0◦ ) ∈ DCoh and
there exists a strand sB in IB and a 4-tuple (ρ, i, π, tt) with ρ a protocol role,
i ≤ |Cρ | with event i in Cρ being a transmission, (Cρ (i), π) is a carried path
ending at a variable, and tt ∈ Targ(Esc(FA,n , ep ), ep ) with (tt, π tt ) a carried
path ending at ep such that:

   • WFC1. If the endpoint of (Cρ (i), π) is not a variable of sort mesg then
     tt = ep .

   • FC1. sB is associated with role ρ in B• , and |ΘB (sB )| ≥ i.

   • FC2. (sB , i) ≺B ϕ(n).

   • FC3. The endpoint of (msg B (sA , i), π) is σ(tt).

   • WFC2. For all i0 < i, for all carried paths p0 = (msg B (sB , i0 ), π 0 ) with
     endpoint σ(ep ), p0 visits σ(Esc(FA,n , ep )).

   • WFC3. Either:

         – WFC3a. The path (msg B (sA , i), π a π tt ) does not visit σ(Esc(FA,n , ep )),
           or
         – WFC3b. There is a prefix π 0 of π a π tt such that (msg B (sB , i), π 0 )
           traverses a term in Esc(FB,ϕ(n) , σ(ep )) and the endpoint of
           (msg B (sA , i), π 0 ) is not in σ(Targ(Esc(FA,n , ep ), ep )).

    A note on the naming of these conditions: WFC stands for “well-formed
candidate.” These are the conditions that guarantee that our candidate
augmentation will be in the an,p suite. FC stands for “factoring candidate.”
These conditions guarantee that the candidate augmentation results in a
factoring of the coverage we care about.


Lemma 12.9 (Regular augmentation completeness). Let A◦ be an unrealized
                                                                         aHC
                                                                          n,p
skeleton and let (n, p) be a test. Then (A◦ , Id) : [DCohGACn,p ==⇒ PCohn,p ].

Proof. Suppose ((A• , Id), λ, B• , A◦ ) is in DCohGACn,p , with sB , ρ, i, π, tt as
specified in the definition. Let s? = N AM E(A).
   Note that the endpoint of (Cρ (i), π) is a variable v. There is a unique
most general unifier of F R(A, ρ, i)(v) with tt, call it σ0 . Let A0• =
Augn,ρ,i,σ0 ◦F R(A,ρ,i),N AM E(A) (A• ). We extend λ = (ϕ, σ) to a map (ϕ0 , σ 0 )
from A0• to B• as follows: ϕ0 = ϕ on all strands other than N AM E(A),
and ϕ0 (N AM E(A)) = sB . Since sB is an instance of role ρ, ϕ0 preserves role
associations. Let σ 0 = σ on all variables occurring in A. The only variables
occurring in A0 that do not occur in A are the variables F C(A, ρ, i)(v 0 ) for v 0 a
variable occurring in Cρ |i other than v 0 = v. σ 0 (F C(A, ρ, i)(v 0 )) = σB(sB ) (v 0 ).
                     ϕ0 ,σ 0
Thus we have A0• 99K B• .
    Note, by WFC2, that σ 0 is a map such that for all i0 < i, for all carried
paths p0 ∈ CarPath(C(i0 )) such that the endpoint of σ 0 ((σ0 ◦ F R(A, ρ, i))(p0 ))
is σ 0 (ep ), p0 visits σ 0 (Esc(FA,n , ep )). Let σ1 be a most general map with this
property more general than σ 0 , so that σ 0 = σ 00 ◦ σ1 .
    Then f = Subσ1 ◦ Augn,ρ,i,σ0 ◦F R(A,ρ,i),N AM E(A) ; we claim that f ∈ an,p (A).
Observe:

    • Cρ (i) is assumed to be a send event in Definition 12.8.

    • If pp = (Cρ (i), π) then the endpoint of pp is a variable v, and if that
      variable is not of sort mesg then tt = ep , by condition WFC1.

    • σ0 is the most general unifier of tt with v, and thus S0 = {σ0 } so in
      particular σ0 ∈ S0 .

    • σ1 is a most general map such that for all i0 < i and for all carried
      paths p0 ∈ CarPath(C(i0 )), if the endpoint of σ1 ((σ0 ◦ F R(A, ρ, i))(p0 ))
      is σ1 (ep ) then σ1 (p0 ) visits an element of σ1 (Esc(FA,n , ep )).

    Let λ0 = (ϕ0 , σ 00 ). We claim that ((f(A• ), f), λ0 , B• , A◦ ) ∈ DPCohn,p .

    • DPC1 holds by Theorem 8.16.

    • DC2 is already known to be true.



                           λ0
   • We know f(A• ) 99K B• . To see that λ0 is structure-preserving, note
     that this property depends only on ϕ0 , and that ϕ0 = ϕ for all nodes
     other than those in N AM E(A). To see that ϕ0 is structure-preserving,
     we need only establish that it is structure-preserving for orderings of
     the form n1 ≺ n2 with n1 in the strand N AM E(A). Either n2 is also
     in that strand, in which case ϕ0 (n1 ) ≺ ϕ0 (n2 ) by the inclusion of the
     strand succession relation, or n2 is not in that strand and n  n2 .
     But (sB , i) ≺ ϕ(n) so by the structure-preserving property of ϕ and
     transitivity, ϕ0 (n1 ) ≺B ϕ0 (n2 ). This establishes DPC3.
   • DC4 is obvious.
   • DPC5 is guaranteed, because f adds to UA only where required to by
     Augn,ρ,i,σ0 ◦F R(A,ρ,i),N AM E(A) .
   • DPC6 is the most complicated to prove.
       If WFC3a holds, then condition Sol2 applies in both f(A• ) and B• , so
       it must apply in any intermediate factorization by Remark 9.15.
       If WFC3b holds, then condition Sol5 applies in B• ; the fact
       that (msg B (sB , i), π 0 ) traverses rather than visits the escape set
       establishes that the new potential target term is a proper car-
       ried substring of an escape set member. Sol5 applies in f(A• ),
       because (msg f(A) (N AM E(A), i), π a π tt ) is a carried path ending
       at t0 and thus must have some maximal decryptable subpath
       (msg f(A) (N AM E(A), i), π 00 ). Furthermore, (msg B (sB , i), π 00 ) must be
       decryptable. Since (msg B (sB , i), π 0 ) traverses the maximal decryptable
       subpath of (msg B (sB , i), π a π tt ), so does (msg f(A) (N AM E(A), i), π 0 ).
       Therefore, Sol5 must apply in any intermediate factorization by Re-
       mark 9.15.
                                        Λf(A)
    We need only prove that A◦ −−−→ f(A). It is obvious that Λf(A) is
structure-preserving, and by Lemma 7.25, since λ preserves points of origi-
nation, so does Λf(A) .




### 12.5      Exhaustivity of the Cases

In this section we prove that cohort coverage implies one of the three critical
coverage properties used in lemmas 12.5, 12.7, and 12.9.


    The proof intimiately deals with the four conditions for a test being
solved. Let A be an unrealized skeleton with test (n, p) and let B be a
                          ϕ,σ
realized skeleton with A −−→ B. The four conditions (from Definition 5.5)
are:

   • Sol1. σ(p) visits σ(Esc(FA,n , ep )).

   • Sol2. There is a carried path from an element of TFA,n to σ(ep ) which
     does not visit σ(Esc(FA,n , ep )).

   • Sol3. There exists a {|b|}u ∈ Esc(FA,n , ep ) such that σ(inv(u)) ∈ SFB,ϕ(n) .

   • Sol4. ep = {|b|}u and σ(u) ∈ SFB,ϕ(n) .

   First we state and prove the top-level proof, assuming a lemma we will
prove later.

Lemma 12.10 (Case exhaustivity). Let A◦ be an unrealized skeleton with
test (n, p), and let ((A• , Id), λ, B◦ , A◦ ) ∈ Coh, with B0• satisfying condition
C3. Then one of the following holds:

   1. ((A• , Id), λ, B0• , A◦ ) ∈ DCohTDn,p ,

   2. ((A• , Id), λ, B0• , A◦ ) ∈ DCohGACn,p , or

   3. ((A• , Id), λ, B◦ , A◦ ) ∈ CohCVDn,p .

Proof. The main observation is that since σ(p) is not a critical path in B at
ϕ(n) (where λ = (ϕ, σ)), by Theorem 5.6, p is solved in FB,ϕ(n) by σ.
   Note that Sol1 is just the same as TD1, so in that case, ((A• , Id), λ, B0• , A◦ ) ∈
DCohTDn,p .
   Note also that Sol3 is the same as EL (since σ(inv(u)) = inv(σ(u))), and
Sol4 is the same as CL, so in either of those two cases, ((A• , Id), λ, B◦ , A◦ ) ∈
CohCVDn,p .
   By Lemma 12.13, if neither of the two cases above apply, then there exists
a good augmentation candidate (ρ, i, π, tt) and a target strand sB0 . Therefore,
((A• , Id), λ, B0• , A◦ ) ∈ DCohGACn,p .
   Before we state and prove our lemma guaranteeing the existance of a
good augmentation candidate, we state and prove two lemmas that will be
helpful.


Lemma 12.11 (Image of the escape set without Sol3). Let A be an unrealized
                                                                        ϕ,σ
protoskeleton with test (n, p) and let B be a protoskeleton such that A 99K B,
and suppose that Sol3 does not hold. Then we have that σ(Esc(FA,n , ep )) ⊂
Esc(FB,ϕ(n) , σ(ep )).

Proof. Let t ∈ Esc(FA,n , ep ). Then either t = ep and ep ∈ Cl↓ (PFA,n , SFA,n ),
or t is a term in Fr(PFA,n , SFA,n ) that carries ep .
    First we observe that σ(Cl↓ (PFA,n , SFA,n )) ⊂ Cl↓ (PFB,ϕ(n) , SFB,ϕ(n) ), which
takes care of the former case. In the latter case, we also need to show that
t is not the endpoint of a path that is the proper prefix of another carried
path in the downward closure. However since we know that in such a case t
is an encryption {|b|}u , we know that σ(inv(u)) ∈     / SFB,ϕ(n) because Sol3 does
not hold. Therefore, σ(t) is in the frontier.

Lemma 12.12 (Critical derivability property preserved without Sol4). Let A
be an unrealized protoskeleton with test (n, p) and let B be a realized skeleton
              ϕ,σ
such that A• 99K B• , and suppose that Sol4 does not hold. Then of n0 ≺ ϕ(n)
is any reception node in B and p0 is any carried path from msg B (n0 ) to σ(ep ),
p0 visits Esc(PFB,n0 , SFB,ϕ(n) , σ(ep )).

Proof. Since B is realized we know that msg B (n0 ) ∈ D(PFB,n0 , SFB,n0 ). A
weaker constraint is that msg B (n0 ) ∈ D(PFB,n0 , SFB,ϕ(n) ). By Proposi-
tion 4.7, p0 must not be a critical path. Since Sol4 does not hold, if
ep is an encryption {|b|}u we know that σ(u) ∈        / SFB,ϕ(n) . Therefore, ei-
                   ↓
ther σ(ep ) ∈ Cl (PFB,n0 , SFB,ϕ(n) ) or p visits Fr(PFB,n0 , SFB,ϕ(n) ). In the for-
mer case, σep ∈ Esc(PFB,n0 , SFB,ϕ(n) , σ(ep )) and thus in either case p visits
Esc(PFB,n0 , SFB,ϕ(n) , σ(ep )).


Lemma 12.13 (Existence of a good augmentation candidate). Let A• be
                                                                      ϕ,σ
an unrealized skeleton and let B• be a realized skeleton with A• −−→ B• with
λ = (ϕ, σ). Let Sol2 hold, but let neither Sol3 nor Sol4 hold.
   Then there exists a sB and a 4-tuple (ρ, i, π, tt) such that conditions WFC1,
WFC2, WFC3, FC1, FC2, and FC3 are satisfied.

Proof. We will show that if Sol2 and neither Sol3 nor Sol4, then
((A• , Id), λ, B0• , A◦ ) ∈ DCohGACn,p , however this is far from straightfor-
ward. In brief, the problem is that while Sol2 establishes that there is some
transmission outside the escape set, that does not make that transmission


a candidate for augmentation now. What we need to find is a transmission
outside the escape set that can serve as a “transforming node” from the
current escape set: a first new transmission.
    Let t = ep and let t0 = σ(t). Let E = Esc(FA,n , t) and let E 0 = σ(E). We
define a sequence of tuples (Ti , ti , πi , πi0 , ni ) for 0 ≤ i ≤ k with the following
properties:

     1. For i > 0, Ti = E 0 \ {t1 , . . . , ti }, and ti ∈ Ti−1 .

     2. For i > 0, πi0 is a prefix of πi .

     3. (ti , πi ) is a carried path that ends at t0 , and for i > 0, the endpoint of
        (ti , πi0 ) is not in σ(Targ(E, t)).

     4. For all i ≥ 0, ni ≺ ϕ(n).

     5. There is a carried path from msg B (ni ) ending at t0 that does not visit
        Ti .

     Note that because E 0 is finite, only a finite sequence can satisfy property
1.
    To define the sequence, we let T0 = E 0 . Since Sol2 holds we know there is
a carried path from an element of TFA,n to t0 that does not visit T0 ; let n0 be
a any node transmitting such an element, let t0 = t0 , and let π0 = π00 = hi.
Note that n0 6= ϕ(n) because ϕ(n) is a reception. Note that properties 1, 2,
and the latter part of 3 are trivial for i = 0, and properties 4 and 5 and the
first part of 3 are easily observed to be true for i = 0.
    Let n0i be a minimal node such that msg B (n0i ) contains a carried path
ending at t0 that does not visit Ti .

Claim 1. Node n0i must contain a transmission event.
Proof of Claim 1. If n0i is a reception then since B is realized and Sol4 does
not hold, by Lemma 12.12, all carried paths ending at t0 in msg B (n0i ) must
visit Esc(PFB,n0 , SFB,ϕ(n) , t0 ). Since there is a path ending at t0 in msg B (n0i )
                i
that does not visit Ti , we must conclude that the first element, e, of
Esc(PFB,n0 , SFB,ϕ(n) , t0 ) visited by that path is not in Ti , and that e contains
         i
a carried path ending at t0 that does not visit Ti . However, e can only be in
Esc(PFB,n0 , SFB,ϕ(n) , t0 ) if an earlier node n0 transmitted a term with a carried
            i




path q visiting e, such that q does not visit Ti after it visits e, and such that
every plaintext edge q traverses before e is one for which the inverse key is
in SFB,ϕ(n) . If q visits Ti it must do so before it visits e, but then it would
visit Ti at a term σ({|b|}u ) for which inv(u) ∈ SFB,ϕ(n) . Since Sol3 does not
hold this cannot happen, so n0 is an earlier node than n0i such that msg B (n0 )
contains a carried path ending at t0 that does not visit Ti .


   Define a carried path pi = (msg B (n0i ), αi ) to t0 as follows:

  1. If there is a carried path from msg B (n0i ) to t0 that does not visit E 0 , let
     pi be such a path.

  2. If there is a carried path from msg B (n0i ) to t0 that visits E 0 but does
     not visit Ti , it must visit E 0 at a point tj for 1 ≤ j ≤ i. Let αi be such
     that pi visits tj and such that πj is a suffix of αi .

   Let n0i = (si , hi ) and let ρi be the role associated with si in B. Let βi
be the maximal prefix of αi such that (Cρi (hi ), βi ) is well-defined. There are
three cases.

  1. If βi = αi then let tt = t and terminate the sequence, that is, set k = i.
      Otherwise, (Cρi (hi ), βi ) ends at a variable mi of sort mesg.

  2. If (msg B (n0i ), βi ) ends at an element of σ(Targ(E, t)), let tt ∈ Targ(E, t)
     such that σ(tt) is the endpoint of (msg B (n0i ), βi ) and set k = i.

  3. Otherwise, (msg B (n0i ), βi ) ends at a non-element of σ(Targ(E, t)). Be-
     cause ρi meets condition 3 of Definition 6.1, mi must be acquired in ρi .
     Let h0i be the node at which mi first occurs in Cρi , and let (Cρi (h0i ), γi )
     be a carried path ending at mi . Note that h0i < hi . Let n00i = (si , h0i ),
     and note that n00i ≺ n0i  ni . Since σB(si ) (mi ) is both the endpoint
     of (msg B (n0i ), βi ) and the endpoint of (msg B (n00i ), γi ), we may conclude
     that qi = (msg B (n00i ), γi a (αi −βi )) is a carried path ending at t0 . By the
     minimality of n0i , qi visits Ti ; let δi be the largest prefix of (γi a (αi −βi ))
     such that msg B (n00i ) @ δi = ti+1 ∈ Ti .
      Note that if γi is a prefix of δi , then σB(si ) (mi )@(δi −γi ) ∈ Ti and there-
      fore, pi visits Ti , which contradicts our earlier assumption. Therefore,
      δi is a proper prefix of γi .


               0                                0
      Let πi+1        = (γi − δi ). Let πi+1 = πi+1 a
                                                      (αi − βi ). Let Ti+1 = E 0 \
      {t1 , . . . , ti+1 }. Since Sol3 does not hold, by Lemma 12.11 we know
      that ti+1 ∈ Ti ⊆ E 0 ⊆ Esc(FB,ϕ(n) , t0 ). Since we know ti+1 6= t0 , ti+1
      must be in Fr(PFB,ϕ(n) , SFB,ϕ(n) ). Therefore, ti+1 must be the endpoint
      of a maximal SFB,ϕ(n) -decryptable path beginning at an element t? of
      PFB,ϕ(n) . Since t? cannot be an atom, a variable or sort mesg, or a tag,
      t? must be a transmission, and therefore there is a node ni+1 ≺ ϕ(n)
      that transmits t? .
Claim 2. When we are in case 3 above, (Ti+1 , ti+1 , πi+1 , πi+1 , ni+1 ) satisfy
properties 1-5.
Proof of Claim 2. Consider the properties one at a time.

  1. We chose Ti+1 = E 0 \ {t1 , . . . , ti+1 }, and chose ti+1 ∈ Ti .
  2. Here, πi+1 was explicitly described as an extension of πi+1 , so this is
     obvious.

  3. First, note that (ti+1 , πi+1 ) is a carried path, since it is a subpath of
     (msg skelB (n00i ), (δi a (αi − βi ))), which we know is a carried path. Also,
     (ti+1 , πi+1 ) ends at t0 :

             ti+1 @ πi+1 =      (msg B (n00i ) @ δi ) @ ((γi − δi ) a (αi − βi ))
                         =      msg B (n00i ) @ (δi a (γi − δi ) a (αi − βi ))
                         =      msg B (n00i ) @ (γi a (αi − βi ))
                         =      σB(si ) (mi ) @ (αi − βi )
                         =      msg B (n0i ) @ (βi a (αi − βi ))
                         =      msg B (n0i ) @ αi
                         =      t0

      The endpoint of (ti+1 , πi+1 ) = msg B (n0i ) @ βi , which we know is not an
      element of σ(Targ(E, t)) since we are in case 3.

  4. We have already noted that ni ≺ ϕ(n).

  5. There is a carried path from msg B (ni ) ending at t0 that does not visit
     Ti , namely the one whose maximal decryptable subpath is ti .



   Now we prove that, (ρk , hk , βk , tt) is a good augmentation candidate with
sB = sk and π tt = (αk − βk ):
   • WFC1. If the endpoint of (Cρk (hk ), βk ) is not a variable of sort mesg
     then either tt = t or (msg B (n0 ), αk ) would not be a carried path.
   • FC1 is obvious.
   • FC2. n0k = (sB , hk ) ≺ ϕ(n) by property 5 of our sequence.
   • FC3 is true by construction in the latter case; when αk = βk , the
     endpoint is t0 = σ(t) = σ(tt).
   • WFC2 is guaranteed by the minimality of n0k .
   • WFC3. Note that (tt, π tt ) is a carried path ending at t. Note further
     that (msg B (n0k ), (βk ) a (αk − βk )) = pk . Thus, if pk does not visit E 0 ,
     we meet WFC3a.
       Otherwise, pk visits some tj , and πj is a suffix of αk , so we can write
       αk = αk0 a πj . Let π 0 = αk0 a πj0 . We know that (msg B (n0k ), π 0 ) traverses
       E 0 since it visits tj ∈ E 0 , and by Lemma 12.11, (msg B (n0k ), π 0 ) traverses
       Esc(FB,ϕ(n) , t0 ). We also know, by property 3 of our sequence, that the
       endpoint of (msg B (n0k ), π 0 ), which is the same as the endpoint of (tj , πj0 ),
       is not in σ(Targ(E, t)), so we meet WFC3b.
   This completes the proof of Lemma 12.13.

12.6      Proof of Lemma 10.11
Lemma 10.11. (Pre-cohort completeness) Let A◦ be an unrealized skeleton
                                                               PP Pn,p
and let (n, p) be any test of A◦ . Then (A◦ , Id) : [[Coh ====⇒ PCohn,p ]].

Proof. Suppose ((A• , Id), λ, B◦ , A◦ ) ∈ Coh, with B0• satisfying condition C3.
   By Lemma 12.10, one of the following three cases applies:

  1. ((A• , Id), λ, B0• , A◦ ) ∈ DCohTDn,p .
       In this case, by Lemma 12.5, there exists an f ∈ cn,p (A◦ ) ⊂ Pn,p and a
       λ0 such that ((f(A• ), f), λ0 , B0• , A◦ ) ∈ DPCohn,p .


  2. ((A• , Id), λ, B0• , A◦ ) ∈ DCohGACn,p , or
     In this case, by Lemma 12.9, there exists an f ∈ an,p (A◦ ) ⊂ Pn,p and a
     λ0 such that ((f(A• ), f), λ0 , B0• , A◦ ) ∈ DPCohn,p .
     In either case 1 or case 2, we have f ∈ Pn,p and a λ0 such that
     ((f(A• ), f), λ0 , B0• , A◦ ) ∈ DPCohn,p . Therefore, ((f(A• ), f), λ0 , B◦ , A◦ ) ∈
     PCohn,p with B0• satisfying condition P3.

  3. ((A• , Id), λ, B◦ , A◦ ) ∈ CohCVDn,p .
     In this case, by Lemma 12.9, there exists an f ∈ ln,p (A◦ ) ⊂ Pn,p and a
     λ0 such that ((f(A• ), f), λ0 , B◦ , A◦ ) ∈ PCohn,p .

    We need only prove that (A◦ , f) ∈ P Pn,p to complete the theorem. We
know that f(A◦ ) is a preskeleton by Theorem 8.16. We also know that
(A◦ , f) ∈ SFn,p by property P6, with f(A) itself as the intermediate fac-
toring. Finally, all three of the lemmas established that (A◦ , f) ∈ HC. This
completes the proof.



## 13     Enumerability

In this section, we go beyond the concept of completeness and show that
cpsa enumerates covering realized skeletons.

Theorem 13.1 (cpsa enumerates). For all (A0 , λ) ∈ [[A◦ ]], there exists an
n ≥ 0 such that if S is the set of skeletons cpsa produces after n setwise
                                                                         λ0
reduction operations, there is a realized B0◦ ∈ S and a homomorphism A◦ −→
B◦ such that (A0 , λ00 ) ∈ [[B◦ ]] and λ = λ00 ◦ (λ0 |Rmv(A◦ ) ).

    To accomplish this cleanly, we need to modify the cpsa algorithm slightly.
Our approach to proving enumerability is to prove that cpsa maintains a
nodewise-injective map to the desired target through the cohort complete-
ness arguments. However, to ensure that we have a nodewise-injective map
initially, we must modify cpsa to do all possible merges of strands in the
initial input first.

Definition 13.2 (Merge-all suite). Let

        X(A◦ ) = {Id} ∪ {Comps1 ,s2 ◦ Subσ |s1 6= s2 ∈ IA , σ ∈ Us1 ,s2 },



   where Us1 ,s2 is a set of most general unifiers of Θ(s1 )|i and Θ(s2 )|i for
i = min(|Θ(s1 )|, |Θ(s2 )|).
   Then the merge-all suite is defined to be

                            Ma(A◦ ) = X(A◦ )|IA | .

Lemma 13.3 (Initial nodewise injectivity). If there is a homomorphism from
                      λ
the user’s input A◦ → − B◦ with B◦ realized, there is an f ∈ (S ◦ Ma)(A◦ )
such that f(A◦ ) is a skeleton and there is a nodewise injective λ0 such that
      λ0
f(A◦ ) −
       → B◦ and λ = λ0 ◦ Λf(A) .

Proof. Simply put, for every pair of strands in A that are unified in B, we
merge one pair of these strands at a time in each application of X until no
more are needed. After that, we choose Id ∈ X. The result is an operator
that merges all strands in A◦ that are merged in B◦ . After this, the remaining
factorization of the original map must be nodewise injective.
    By Lemma 10.15, λ0 is structure-preserving. Note that f(A) has only
inherited unique origination assumptions from A under Λf(A) .

                       λ
Lemma 13.4. If A 99K B and λ is nodewise-injective, and f = OE or f =
                                   λ0
Subσ for any σ, such that f(A) 99K B where λ = λ0 ◦ Λf , λ0 is nodewise-
injective.

Proof. For all such operators, the nodes in f(A) are in one-to-one correspon-
dance with the nodes in A. Thus, if two nodes f(n1 ) and f(n2 ) in f(A) map
to the same node in B, then so did n1 and n2 in A, which we assumed was
not the case.
   This already shows that much of the proof of completeness holds if we add
the requirement that λ be nodewise-injective to all the coverage properties.
What remains is to handle those cases where we use the compression or
augmentation primitive operators. Fortunately, these come up in only three
places.

  1. In skeletonization, we use the compression operator in the merging suite
     mn,p . However, the precondition for Lemma 11.7 renders the merging
     suite moot when we require a nodewise injective λ, because it requires
     that ϕ(n) = ϕ(n0 ) for distinct nodes n, n0 .


  2. In listener augmentation, we use the augmentation operator to add a
     listener. If the listener were to map to a node already in the image of
     A, this would break node injectivity. Fortunately during listener aug-
     mentation, we adjust the target B to include a new listener specifically
     to be the image of the new listener added to A, so node-injectivity is
     always preserved.
  3. In regular augmentation, we may sometimes augment with a strand
     whose image is already in λ(A). Specifically, suppose that we have
     f = Subσ1 ◦ Augn,ρ,i,σ0 ◦F R(A,ρ,i),N AM E(A) and the corresponding λ0 , a ho-
     momorphism from f(A• ) to B• , but that λ0 is not nodewise-injective.
     Since λ was nodewise-injective, no node collision can occur unless one of
     the nodes is in the new strand N AM E(A). Suppose ϕ0 (N AM E(A)) =
     ϕ0 (s) for some other strand s ∈ IA . Note that σ 0 is a unifier of s
     with N AM E(A) up to the minimum of their heights; let σ2 be a
     most general unifier of those terms more general than σ 0 . Then con-
     sider f 0 = Comps,N AM E(A) ◦ Subσ2 ◦ f. Clearly, there is a λ00 such that
     λ0 = λ00 ◦ ΛComps,N AM E(A) ◦Subσ2 (A) . f 0 ∈ dn,p (A◦ ) by our definition of the
     deorigination suite.
     ((f 0 (A• ), f 0 ), λ00 , B• , A◦ ) ∈ DPCohn,p . Most conditions are easy to estab-
     lish given that we already know ((f(A• ), f), λ0 , B• , A◦ ) ∈ DPCohn,p ; the
     only one that is non-trivial is that λ00 is structure-preserving. The proof
     that λ00 must be structure-preserving essentially follows the argument
     that merging satisfies condition S5 in Lemma 11.7.
                   Λf 0 (A)
     Finally, A◦ −−−→ f 0 (A◦ ). Again it is obvious that Λf 0 (A) is structure-
     preserving, and by Lemma 7.25, it preserves points of origination. This
                                                                       (an,p ∪dn,p )HCn,p
     allows us to conclude that (A◦ , Id) : [NIDCohGACn,p ==========⇒
     NIPCohn,p ], where NIDCohGAC and NIPCoh, respectively, are the
     equivalent coverage properties with the additional requirement that
     the map λ be nodewise-injective.
     Since an,p ∪ dn,p ⊂ Pn,p , this weakened statement is still strong enough
     for use in the proof of Lemma 10.11.

    Finally, we prove that maintaining nodewise-injective maps guarantees
a finite number of cohort steps to a realized skeleton. Note that since we
maintain nodewise-injective maps, we can use only finitely many operators
that add nodes to our current skeleton while maintaining coverage of the


target realized skeleton. There are only finitely many missing orderings, so
again we can only use finitely many operators that add additional orderings.
Since no cohort step consists of only Id, the only way we can fail to reach the
target (or something covering it) in finitely may steps is for there to be an
infinite sequence of substitutions, each more specific than the last, factoring a
specific substitution. And to be more specific, every subsequent substitution
is a unification. However, it is known (see Lemma A.10) that this cannot be
the case for our algebra. Thus, either we reach our target in a finite number
of steps, or we reach something realized before that, in which case we reach
something covering our target in finitely many steps.


References
 [1] A. Armando, D. Basin, Y. Boichut, Y. Chevalier, L. Compagna, J. Cuel-
     lar, P. Hankes Drielsma, P.C. Hem, O. Kouchnarenko, J. Mantovani,
     S. Mdersheim, D. von Oheimb, M. Rusinowitch, J. Santiago, M. Tu-
     ruani, L. Vigan, and L. Vigneron. The avispa tool for the automated
     validation of internet security protocols and applications. In Kousha
     Etessami and Sriram K. Rajamani, editors, Computer Aided Verifica-
     tion, volume 3576 of Lecture Notes in Computer Science, pages 135–165.
     Springer Berlin / Heidelberg, 2005.
 [2] A. Armando and L. Compagna. Sat-based model checking for secu-
     rity protocols analysis. International Journal of Information Security,
     7(1):3–32, 2008.
 [3] M. Backes, S. Lorenz, M. Maffei, and K. Pecina. The CASPA tool:
     Causality-based abstraction for security protocol analysis. In A. Gupta
     and S. Malik, editors, CAV, volume 5123 of Lecture Notes in Computer
     Science, pages 419–422. Springer, 2008.
 [4] Bruno Blanchet. An efficient cryptographic protocol verifier based on
     prolog rules. In 14th IEEE Computer Security Foundations Workshop
     (CSFW-14 2001), pages 82–96, 2001.
 [5] Y. Boichut, P.C. Heam, O. Kouchnarenko, and F. Oehl. Improvements
     on the genet and klay technique to automatically verify security pro-
     tocols. In Proc. International Workshop on Automatic Verification of
     Infinite-State Systems (AVIS’04), 2004.


 [6] R. Corin and S. Etalle. An improved constraint-based system for the ver-
     ification of security protocols. In Proc. 9th International Static Analysis
     Symposium (SAS), volume 2477 of Lecture Notes in Computer Science,
     pages 326–341. Springer, September 2002.

 [7] C.J.F. Cremers. Scyther - Semantics and Verification of Security Pro-
     tocols. Ph.D. dissertation, Eindhoven University of Technology, 2006.

 [8] C.J.F. Cremers. The Scyther Tool: Verification, falsification, and
     analysis of security protocols. In Computer Aided Verification, 20th
     International Conference, CAV 2008, Princeton, USA, Proc., vol-
     ume 5123/2008 of Lecture Notes in Computer Science, pages 414–418.
     Springer, 2008.

 [9] Shaddin F. Doghmi, Joshua D. Guttman, and F. Javier Thayer. Search-
     ing for shapes in cryptographic protocols (extended version). http:
     //eprint.iacr.org/2006/435, November 2006.

[10] Shaddin F. Doghmi, Joshua D. Guttman, and F. Javier Thayer. Com-
     pleteness of the authentication tests. In J. Biskup and J. Lopez, editors,
     European Symposium on Research in Computer Security (ESORICS),
     number 4734 in LNCS, pages 106–121. Springer-Verlag, September 2007.

[11] Shaddin F. Doghmi, Joshua D. Guttman, and F. Javier Thayer. Search-
     ing for shapes in cryptographic protocols. In Tools and Algorithms
     for Construction and Analysis of Systems (TACAS), number 4424 in
     LNCS, pages 523–538. Springer, March 2007. Extended version at
     http://eprint.iacr.org/2006/435.

[12] Daniel Dolev and Andrew Yao. On the security of public-key protocols.
     IEEE Transactions on Information Theory, 29:198–208, 1983.

[13] Santiago Escobar, Catherine Meadows, and Jos Meseguer. Maude-
     NPA: Cryptographic protocol analysis modulo equational properties. In
     Alessandro Aldini, Gilles Barthe, and Roberto Gorrieri, editors, Foun-
     dations of Security Analysis and Design V, volume 5705 of Lecture Notes
     in Computer Science, pages 1–50. Springer Berlin / Heidelberg, 2009.

[14] Joshua D. Guttman and F. Javier Thayer. Authentication tests and the
     structure of bundles. Theor. Comput. Sci., 283(2):333–380, 2002.



[15] G. Lowe. Breaking and fixing the needham-schroeder public-key pro-
     tocol using FDR. In Proc. 2nd International Conference on Tools and
     Algorithms for the Construction and Analysis of Systems (TACAS), vol-
     ume 1055 of Lecture Notes in Computer Science, pages 147–166, 1996.
[16] C. Meadows. The NRL protocol analyzer: An overview. Journal of
     Logical Programming, 26(2):113–131, 1996.
[17] John D. Ramsdell and Joshua D. Guttman. CPSA: A cryptographic
     protocol shapes analyzer. In Hackage. The MITRE Corporation, 2009.
     http://hackage.haskell.org/package/cpsa.
[18] John D. Ramsdell, Joshua D. Guttman, and Paul D. Rowe. The
     CPSA Specification: A Reduction System for Searching for Shapes in
     Cryptographic Protocols. The MITRE Corporation, 2009. In http:
     //hackage.haskell.org/package/cpsa source distribution, doc direc-
     tory.
[19] Alan Robinson and Andrei Voronkov. Handbook of Automated Reason-
     ing. The MIT Press, 2001.
[20] F. Javier Thayer, Jonathan C. Herzog, and Joshua D. Guttman. Strand
     spaces: Proving security protocols correct. Journal of Computer Secu-
     rity, 7(1), 1999.
[21] M. Turuani. The CL-Atse protocol analyser. In Proc. RTA ’06, volume
     4098 of Lecture Notes in Computer Science, pages 227–286. Springer,
     August 2006.


A      The cowt Algorithm
This section describes the algebra specific part of the computation used in
regular augmentation and displacement.
   First we recall the definition of the regular augmentation suite:

Definition 9.2 (Regular augmentation suite)
                   an,p (A◦ ) = {Subσ1 ◦ Augn,ρ,i,σ0 ◦F R(A,ρ,i),s? }
where σ0 ∈ S0 , σ1 ∈ S1 , s? = N AM E(A) and ρ, i, σ0 , σ1 , S0 , S1 are as defined
below}.


   • R ∈ P and i is such that CR (i) is defined and is a send event. Let
     C = CR |i.

   • There is a path pp ∈ CarPath(C(i)) and a term tt such that either (i)
     the endpoint of pp is a variable not of sort mesg and tt = ep or (ii) the
     endpoint of pp is a variable of sort mesg and tt ∈ Targ(Esc(F, ep ), ep ).

   • S0 is a set of most general unifiers of tt with the endpoint of F R(A, ρ, i)(pp).

   • S1 is a set of most general maps σ1 such that for all i0 < i and for all
     paths p0 ∈ CarPath(C(i0 )), if the endpoint of σ1 ((σ0 ◦ F R(A, ρ, i))(p0 ))
     is σ1 (ep ) then σ1 (p0 ) visits an element of σ1 (Esc(FA,n , ep )).

    Note that it is not obvious that S1 exists, let alone that there is a finite
set of such maps we can calculate efficiently.

Definition A.1 (Carried only within). Message t is carried only within
set T in t0 , if for all carried paths p ending at t in t0 , p visits T .
    A message t is carried only within set T in a set of messages T 0 if for all
t0 ∈ T 0 , t is carried only within T in t0 .

    In calculating the regular augmentation suite, we must find a set S1 of
most general maps σ1 such that σ1 (ep ) is carried only within σ1 (Esc(FA,n , ep ))
in {(σ0 ◦ F R(A, ρ, i))(C|i−1 )}.

Definition A.2 (Carried only within problem). A carried only within prob-
lem is a triple (t, T, T 0 ).

Definition A.3 (Carried only within problem solution). The solution to a
carried only within problem (t, T, T 0 ) is a complete set of most general unifiers
S such that for every σ ∈ S, σ(t) is carried only within σ(T ) in σ(T 0 ).

    The notion of a carried only within problem and its solution allows us to
describe the cpsa approach to computing the regular augmentation suite as
its own algorithm.
    A unification problem is a finite set
                                      ?               ?
                           E = {t1 = t01 , . . . , tn = t0n },

and a unifier of E is a substitution σ such that σ(t1 ) ≡ σ(t01 ), . . . , σ(tn ) ≡
σ(t0n ). Definitions in this section follow [19, Chapter 9].


      When solving a unification problem E, we rely on the fact that the order
in which the equations are solved is irrelevant in the following sense. Let
C(E) be a finite complete set of unifiers for E. Let E = E0 ∪ E1 be a
decomposition of E, and let S = {σ1 ◦ σ0 | σ0 ∈ C(E0 ) ∧ σ1 ∈ C(σ0 (E1 ))}.
Then S is a finite complete set of unifiers for E. Decompositions E = E0 ∪E1
in this section often are such that E0 ⊂ E, and E1 = E. Thus, solving a
unification problem can be done from a function unify that, on input t and
t0 , finds a set of most general substitutions σ such that σ(t) = σ(t0 ).
      In what follows, C({}) = {IdA }.
      A carried only within solution cannot be directly computed. Given terms t
and t0 , the unify function finds a most general set of substitutions σ such that
σ(t) ≡ σ(t0 ), however, the set of carried paths ending at t may become larger
after we apply a unifying substitution.
      The remainder of this section describes an iterative procedure that breaks
the cyclic dependencies. Each step of the iteration improves an approxima-
tion of a solution to the problem.
Definition A.4 (Carried only within at a substitution). Message t is carried
only within T in t0 at substitution σ if for all carried paths p ending at t in t0 ,
σ(p) visits σ(T ).
   Each step in the iterative procedure involves finding subsequently more
specific substitutions such that t is cow T in t0 at σ for each t0 ∈ T 0 . The
sense in which each step approximates the solution is captured by the fol-
lowing lemmas.
   The algorithm uses specific terms rather than equivalence classes of terms.
Lemma A.5. σ(CarPath(t, t0 )) ⊆ CarPath(σ(t), σ(t0 )).
Proof. Let p = (t0 , π) be a path that ends at t. Then σ(p) = (σ(t0 ), π), which
is a path that ends at σ(t). Moreover, p is a carried path if and only if σ(p)
is.
      The case in which t = x and t0 = hx, yi, and σ unifies x and y provides
an example in which the subset relation is proper.
      Lemma A.5 can be used to show why the problem of finding carried only
within solutions is non-trivial. If σ(t) ≡ σ(t0 ) and σ E σ 0 , then σ 0 (t) ≡
σ 0 (t0 ), however, if σ(t) is cow σ(T ) in σ(t0 ) and σ E σ 0 , one cannot conclude
that σ 0 (t) is cow σ 0 (T ) in σ 0 (t0 ), because by Lemma A.5, it is possible that
CarPath(σ(t), σ(t0 )) ( CarPath(σ 0 (t), σ 0 (t0 )).


    The implementation must consider all possible solutions to the equations.
It does so by operating on sets of terms and substitutions. Given solutions S
to some other equations, solve(T, T 0 , S) extends them to include solutions to
one pair from T and T 0 .

               solve(T, T 0 , S) =
                 {σ 0 | t ∈ T, t0 ∈ T 0 , σ ∈ S, σ 0 ∈ unify 0 (t, t0 , σ)}
               unify 0 (t, t0 , σ) = {σ 0 ◦ σ | σ 0 ∈ unify(σ(t), σ(t0 ))}

    An algebra module in cpsa exports unify 0 , not unify, and substitu-
tion composition is intertwined with unification steps. Obviously, if σ 0 ∈
unify 0 (t, t0 , σ) then σ E σ 0 .
    The implementation combines the solutions for single equations by folding
the substitutions produced by the solve function. The set-oriented version
of the cow at a substitution function is:
               fold (t, T, t0 , σ) =
                  fold 0 (t, T, t0 , σ, {IdA }, CarPath(σ(t), σ(t0 )))

               fold 0 (t, T, t0 , σ, S, {}) = {σ 0 ◦ σ|σ 0 ∈ S}
               fold 0 (t, T, t0 , σ, S, {p} ∪ P ) =
                  fold 0 (t, T, t0 , σ, solve(anc(σ(t0 ), p), σ(T ), S), P )
     The fold function on (t, T, t0 , σ) is meant to return the set of substitutions
{σ 0 ◦ σ|σ(t) is cow σ(T ) in σ(t0 ) at σ 0 }. However, we do not need to prove
this behavior specifically to establish the theorems we want to prove. The
important observation is that t being cow T in t0 at σ is insufficient to
guarantee that σ(t) is cow σ(T ) in σ(t0 ).
     Iterating the fold function can be used to find contractions. Potential
contractions are in cows(t, T, t0 ), where
                      cows(t, T, t0 ) =
                        cows 0 (t, T, t0 , IdA )

                      cows 0 (t, T, t0 , σ) =
                        if σ(t) is cow σ(T ) at σ(t0 ) then
                           {σ}
                        else
                           let
                           S S = fold (t, T, t0 , σ)       in
                              σ 0 ∈S cows 0 (t, T, t , σ )



   We now show the cows function produces the unifiers that make up a
carried only within solution. It may also produce non-minimal unifiers. An
additional step is required to remove these unifiers.
   The cows function terminates because each step in the iteration reduces
the number of variables in the problem statement. Several lemmas are re-
quired to show termination.

Lemma A.6. σ 0 ∈ unify 0 (t, t0 , σ) and σ(t) 6≡ σ(t0 ) implies σ C σ 0 .

Proof. We know σ E σ 0 . Assume the negation of the conclusion, that there
is a substitution σ 00 such that σ = σ 00 ◦ σ 0 . The first hypothesis implies
σ 0 (t) ≡ σ 0 (t0 ), so σ 00 (σ 0 (t)) ≡ σ 00 (σ 0 (t0 )), a contradiction.

Lemma A.7. σ 0 ∈ fold (t, T, t0 , σ) and σ(t) not cow σ(T ) in σ(t0 ) implies
σ C σ0.

Proof. If σ(t) not cow σ(T ) in σ(t0 ), there is some position p in
CarPath(σ(t), σ(t0 )) such that no ancestor of σ(t0 ) @ p is equivalent to any
member of σ(T ). We know σ E σ 0 (by observation, all outputs of fold extend
the initial σ), so assume the negation of the conclusion, that there is a substi-
tution σ 00 such that σ = σ 00 ◦ σ 0 . By the fact that σ 0 ∈ fold (t, T, t0 , σ) we know
that t is cow T in t0 at σ 0 , so there is a t00 ∈ T and a proper prefix p0 of p such
that σ 0 (t00 ) ≡ σ 0 (t0 @p0 ). Thus, σ(t00 ) = σ 00 (σ 0 (t00 )) ≡ σ 00 (σ 0 (t0 @p0 )) = σ(t0 @p0 )
which contradicts what we know about p, as σ(t0 @ p0 ) = σ(t0 ) @ p0 is an an-
cestor of σ(t0 ) equivalent to σ(t00 ) which is in σ(T ).


   Now we prove our three main results about cows. We give sufficient
conditions to guarantee that cows terminates (Theorem A.8), we prove that
cows gives answers with the property we want (Theorem A.9), and we prove
that cows produces a complete set of such outputs (Theorem A.11).

Theorem A.8. If the algebra A has variable-reducing, finitary unification,
the function cows(t, T, t0 ) terminates on all inputs.

Proof. By an examination of fold , each substitution produced is a unification
of a set of equations. By Lemma A.7, each substitution produced is strictly
less general than IdA . Therefore, every substitution produced by fold is a
non-trivial unification. Since every unification is variable-reducing, there is a
maximum number of successive non-trivial unifications that can be applied


before further unification becomes impossible, namely, the number of vari-
ables appearing in the original t, T , and t0 . Furthermore, since the unification
is finitary, we know that every node of the tree of substitutions we explore
has a finite branching factor. Thus, the entire tree of potential solutions is
finite, so cows terminates.

Theorem A.9. σ ∈ cows(t, T, t0 ) implies σ(t) is cow σ(T ) in σ(t0 ).

Proof. We prove this by structural induction on the execution of cows. If
σ ∈ cows(t, T, t0 ) and cows 0 outputs without recursing then σ = IdA and the
property holds by the required condition in the algorithm.
    If σ ∈ cows(t, T, t0 ) and cows 0 outputs after recursing, then ∃σ 0 , σ 00 such
that σ = σ 00 ◦ σ 0 where σ 0 ∈ S and σ 00 ∈ cows0 (t, T, t0 , σ 0 ). By inductive
assumption, σ 00 (σ 0 (t)) is cow σ 00 (σ 0 (T )) in σ 00 (σ 0 (t0 )). This proves that σ(t)
is cow σ(T ) in σ(t0 ).

Lemma A.10. For any strand space algebra with variable-reducing unifica-
tion, the following holds: Let IdA = σ0 E σ1 E . . . be an infinite sequence of
substitutions all generated over the same finite set of variables, such that for
every σi , σi Eσ and such that every σi0 (where σi+1 = σi0 ◦σi ) is a most general
unification. Then for at most finitely many i ≥ 0, σi C σi+1 .

Proof. Let {x1 , . . . , xn } be the finite set of variables over which the sequence
of substitutions is defined. For each i, define vi to be |V ars(σi (x1 , . . . , xn ))|
with v0 = n, and let v = |V ars(σ(x1 , . . . , xn ))|. For each i, we know that
σi0 is a most general unification; if it is a unification of terms which are all
already equivalent then σi0 must be a renaming and then it cannot be the case
that σi C σi+1 . If σi0 is a unification of one or more pairs of non-equivalent
terms, it is variable-reducing, so vi > vi+1 . However, this sort of step can be
taken at most n − v times.

Theorem A.11. If the algebra A has variable-reducing unification, σ(t) is
cow σ(T ) in σ(t0 ) implies there exists a substitution σ 0 such that σ 0 E σ and
σ 0 ∈ cows(t, T, t0 ).2

Proof. We aim to define a sequence of substitutions IdA = σ0 E σ1 . . . E
σn E σ, such that σn (t) is cow σn (T ) in σn (t0 ), where each σi is produced
    Note that cows(t, T, t0 ) is a well-defined set regardless of whether a computer could
calculate it in a finite number of steps.



incrementally during the cows computation, where σn will serve as the σ 0 in
the theorem.
    By saying that σi is “produced incrementally during the cows computa-
tion” we mean that (i) if i > 0, σi is an output of fold (t, T, t0 , σi−1 ), and
(ii) if i < n, cows 0 (t, T, t0 , σi ) is a recursive call within the execution of
cows0 (t, T, t0 , IdA ).
    We develop the sequence inductively. Note that σ0 = IdA E σ for any
σ, and that our initial call of cows(t, T, t0 ) establishes that we run cows0 on
(t, T, t0 , σ0 ).
    Suppose that we have IdA = σ0 E. . .Eσi Eσ and that we run cows 0 (t, T, t0 , σi ).
If σi (t) is cow σi (T ) in σi (t0 ) then n = i and our sequence is complete. Oth-
erwise, we calculate S = fold (t, T, t0 , σi ); we wish to prove that there exists
a σi+1 ∈ S such that σi E σi+1 E σ.
    By Lemma A.5, we know that CarPath(σi (t), σi (t0 )) ⊆ CarPath(σ(t), σ(t0 )).
Let p1 , . . . , pk be the positions in CarPath(σi (t), σi (t0 )). In fold0 , the set S
initially contains ϕ0 = IdA ; note that ϕ0 ◦ σi E σ. In the next paragraph we
show how to define a sequence of substitutions ϕ0 E. . .Eϕk in S in successive
calls to fold 0 , such that ϕl ◦ σi E σ. This sequence will serve to bridge the
difference between σi and σi+1 .
    Suppose that ϕl ∈ S in fold 0 when P consists of pl+1 , . . . , pk , and that
ϕl ◦ σi E σ. Since σ(t) is cow σ(T ) in σ(t0 ), there exists a proper prefix p0l+1
of pl+1 and a te ∈ T such that σ(t0 @ p0l+1 ) ≡ σ(te ). Note that σi (te ) ∈ σi (T ),
and that σi (t0 ) @ p0l+1 ∈ anc(σi (t0 ) @ pl+1 )). Thus, fold 0 calls solve(X, Y, S)
where σi (te ) ∈ X, σi (t0 @ p0l+1 ) ∈ Y , and ϕl ∈ S.
    Write σ = ψl ◦ ϕl ◦ σi : note that ψl is a unifier of ϕl (te ) and ϕl (t0 @ p0l+1 ).
Thus, there exists a ψl0 ∈ unify(ϕl (te ), ϕl (t0 @ p0l+1 )) such that ψl0 E ψl . Let
ϕl+1 = ψl0 ◦ ϕl : note that ψl0 ◦ ϕl E ψl ◦ ϕl so σi E ϕl E ϕl+1 E σ. Note further
that ϕl+1 ∈ solve(X, Y, S) and thus ϕl+1 is in S in fold 0 when P consists of
pl+2 , . . . , pk .
    Consider ϕk : note that σi Eϕk Eσ and that ϕk ∈ S in fold 0 when P = {},
so ϕk ∈ fold (t, T, t0 , σi ). Let σi+1 = ϕk . Because ϕk is in the output of
fold (t, T, t0 , σi ), note that we make a recursive call to cows 0 on (t, T, t0 , σi+1 ).
    In this way we define a (potentially infinite) sequence IdA = σ0 Eσ1 E. . .E
σi E . . . E σ. Moreover, by Lemma A.7, we know that σ0 C . . . C σi C . . . E σ.
Note that each substitution is produced by composing a unification with the
previous substitution. Thus, by Lemma A.10, the sequence must be finite,
with σn being the last substitution before σ. But the sequence can only
end at σn if σn (t) is cow σn (T ) in σn (t0 ). If this is the case, then in the


recursive call to cows on σn (t), σn (T ), σn (t0 ), IdA is returned, so σn ◦ IdA =
σn ∈ cows(t, T, t0 ). This completes the proof, with σ 0 = σn .
    The cows function finds solutions to a single carried only within problem.
To calculate substitutions, we need the following function, cowt, which finds
solutions to a set of carried only within problems.

                            cowt(t, T, T 0 ) =
                              cows(t, T, concat(T 0 ))

   where concat(T 0 ) is a concatenation, by successive pairings, of the mes-
sages in T 0 .

Lemma A.12. cowt complete terminates cowt(t, T, T 0 ) is a most general set
of substitutions σ such that σ(t) is carried only within σ(T ) in σ(T 0 ), and
cowt(t, T, T 0 ) can be calculated in finitely many steps.

Proof. It should be obvious that cowt will terminate. Note that the carried
paths of concat(T 0 ) are in one-to-one correspondance with the carried paths
of members of T 0 ; this establishes that cowt gives a complete set of most
general substitutions such that σ(t) is carried only within σ(T ) in σ(T 0 ),
because cows is complete.




