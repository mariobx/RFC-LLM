# CPSA Security Goals, Rules, Lemmas, and Shape Analysis Sentences Manual

*Authors: Joshua D. Guttman, John D. Ramsdell, Moses D. Liskov, Paul D. Rowe (The MITRE Corporation, CPSA Version 4.4)*

---

## Table of Contents

- [1. Introduction to First-Order Security Goals](#1-introduction-to-first-order-security-goals)
- [2. Security Goal Syntax (`defgoal` and Predicates)](#2-security-goal-syntax-defgoal-and-predicates)
  - [2.1 Full CPSA 4.4 Security Goal Grammar](#21-full-cpsa-44-security-goal-grammar)
  - [2.2 Goal Predicates](#22-goal-predicates)
  - [2.3 Syntactic Abbreviations (`strand` and `listener`)](#23-syntactic-abbreviations-strand-and-listener)
- [3. Model-Theoretic Semantics and Characteristic Skeletons](#3-model-theoretic-semantics-and-characteristic-skeletons)
- [4. Authentication and Secrecy Goal Examples](#4-authentication-and-secrecy-goal-examples)
  - [4.1 Counterexample Analysis: Needham-Schroeder Responder (`satisfies no`)](#41-counterexample-analysis-needham-schroeder-responder-satisfies-no)
  - [4.2 Secrecy Goal with Listeners (`(false)` Conclusion)](#42-secrecy-goal-with-listeners-false-conclusion)
- [5. Multi-Sentence Goals, Skeleton `goals` Annotations, and Shape Analysis Sentences](#5-multi-sentence-goals-skeleton-goals-annotations-and-shape-analysis-sentences)
  - [5.1 Shape Analysis Sentences (`cpsa4sas`)](#51-shape-analysis-sentences-cpsa4sas)
- [6. Axiomatic Rewrite Rules (`defrule`) and Facts (`facts`)](#6-axiomatic-rewrite-rules-defrule-and-facts-facts)
  - [6.1 Skeleton Fact Databases (`facts` and `fact`)](#61-skeleton-fact-databases-facts-and-fact)
  - [6.2 Case Study: Door Simple Example Protocol (DoorSEP) and Trust Axioms](#62-case-study-door-simple-example-protocol-doorsep-and-trust-axioms)
- [7. Automatically Generated Rules (`defgenrule`), Built-in Relations, and Trace Annotations](#7-automatically-generated-rules-defgenrule-built-in-relations-and-trace-annotations)
  - [7.1 Built-in Fact Relations (`neq`, `invk`, `lt`, `subsort`) and Generated Rules](#71-built-in-fact-relations-neq-invk-lt-subsort-and-generated-rules)
  - [7.2 Trace Annotations (`cheq`, `assume`, `rely`, `guarantee` / `guar`) and `cpsa4goals`](#72-trace-annotations-cheq-assume-rely-guarantee--guar-and-cpsa4goals)
- [8. Lemmas (`deflemma`)](#8-lemmas-deflemma)
- [9. Formal Specification of Shape Analysis Sentences (Coherent Logic)](#9-formal-specification-of-shape-analysis-sentences-coherent-logic)
  - [9.1 Formal Syntax and Satisfaction Semantics of Skeleton Formulas](#91-formal-syntax-and-satisfaction-semantics-of-skeleton-formulas)
- [10. References](#10-references)

---

## 1. Introduction to First-Order Security Goals

Analyzing a cryptographic protocol means finding out what security
properties—essentially, authentication and secrecy properties—are true in
all its possible executions.
    Given a protocol definition and some assumptions about executions, cpsa
attempts to produce descriptions of all possible executions of the protocol
compatible with the assumptions. Naturally, there are infinitely many possible
 executions of a useful protocol, since different participants can run it
with varying parameters, and the participants can run it repeatedly.
    However, for many naturally occurring protocols, there are only finitely
many of these runs that are essentially different. Indeed, there are frequently
very few, often just one or two, even in cases where the protocol is flawed. We
call these essentially different executions the shapes of the protocol. Authentication
 and secrecy properties are easy to “read off” from the shapes, as are
attacks and anomalies, according to the introduction in the cpsa Primer [4].
    But how easy is it to read off authentication and secrecy properties? What
precisely is it that an expert sees? This paper describes cpsa’s support for
reasoning about security goals using first-order logic. With security goals
expressed in first-order logic, intuition is replaced by determining if a formula
is true in all executions of the protocol.
    This treatment of security goals relies heavily on a branch of first-order
logic called model theory. It deals with the relationship between descriptions
in first-order languages and the structures that satisfy these descriptions. In
our case, the structures are skeletons that denote a collection of executions
of a protocol. This paper attempts to describe the language of security goals
and its structures without requiring the reader to have studied model theory.
    The model theoretical foundation of this approach to security goals appears
 in [1]. A practical use of security goals in protocol standardization is
described in [2]. The precise semantics of the goal language is in [5, Appendix
 C]. The syntax of security goals appears in [4, Table 2].
    The distribution in which this paper is included contains the sample in-put
 cpsa file goals.scm. It contains the examples in this paper. You are
encouraged to run the examples and examine the output while reading this
paper.
    The cpsa Primer [4] is a prerequisite for reading this paper. In particular,
the Needham-Schroeder Protocol in Section 10 is reanalyzed using security
goals here. The roles are displayed in Figure 1.

   init     {|N1 , A|}KB          {|N1 , A|}KB    resp

     •      {|N1 , N2 |}KA       {|N1 , N2 |}KA    •

     •      {|N2 |}KB                {|N2 |}KB     •

```scheme
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
               (recv (enc n2 (pubk b))))))
```
**Figure 1: Needham-Schroeder Initiator and Responder Roles**

```scheme
(defgoal ns                ; Goal
  (forall ((b name) (n1 text) (z0 strd))
    (implies
      (and (p "init" z0 3) (p "init" "n1" z0 n1)
        (p "init" "b" z0 b) (non (privk b)) (uniq n1))
      (exists ((z1 strd))
        (and (p "resp" z1 2) (p "resp" "b" z1 b))))))
```

```scheme
(defskeleton ns            ; Point of view skeleton
  (vars (a b name) (n1 n2 text))
  (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2))
  (non-orig (privk b))
  (uniq-orig n1))
```

                {|N1 , A|}KB                 {|N1 , A|}KB
      init                         ≺                           resp
               {|N1 , N2 |}KA                {|N1 , N2′ |}KA
       •                           ≻                             •
                 {|N2 |}KB
       •

```scheme
(defskeleton ns            ; Shape
  (vars (n1 n2 text) (a b name))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b))
  (defstrand resp 2 (n2 n2-0) (n1 n1) (b b) (a a))
  (precedes ((0 0) (1 0)) ((1 1) (0 1)))
  (non-orig (privk b))
  (uniq-orig n1)
  (satisfies yes))
```
**Figure 2: Needham-Schroeder Initiator Point of View**

    The protocol is analyzed from the point of view of a complete run of
one instance of the initiator role. The input security goal, followed by the
point of view skeleton it generates and the shape produced by cpsa, are
shown in Figure 2. The syntax and semantics of the goal will be explained
later. Roughly speaking, it asserts that if a realized skeleton contains a full
length initiator strand, its private key is uncompromised, and it uniquely
generates n1, then the skeleton will contain a responder strand that agrees
with the initiator on the name b. The shape produced by cpsa contains
the annotation (satisfies yes). This indicates that its structure satisfies
the description given by the security goal. It will be explained later why the
properties of cpsa allows us to conclude that this goal is true in all executions
of the protocol, and therefore conclude that the Needham-Schroeder protocol
achieves this authentication goal.

## 2. Security Goal Syntax (`defgoal` and Predicates)

To be precise, a security goal is an order-sorted first-order logic sentence
in a restricted form. The sentence in Figure 2 has the form shared by all
security goals. It is a universally quantified implication. The antecedent is
a conjunction of atomic formulas. For this sentence, the conclusion is an
existentially quantified conjunction of atomic formulas, but in general, the
conclusion is a disjunction of existentially quantified conjunctions of atomic
formulas. In what follows, (false) is a synonym for the empty disjunction,
(or).

```text
         goal     ←    (defgoal prot sent+ comments)
         sent     ←    (forall (decl∗) (implies antec concl))
        concl     ←    (false) | existl | (or existl∗)
        existl    ←    (exists (decl∗) antec) | antec
        antec     ←    atomic | (and atomic+)
```

    Variables are declared as they are for roles and skeletons with one exception
, there is a new sort symbol strd for strands. Notice that in the sentence
in Figure 2, variables z0 and z1 have sort strd. Every universally quantified
variable must occur in the antecedent of the implication.
    The signature as been expanded to include the natural numbers. A natural
 number has sort nat.

### 2.1 Full CPSA 4.4 Security Goal Grammar

**Table 7.1: Goal syntax. See Tables 10.3 and 10.5 for the algebra syntax, which defines the term and sort symbols.**

```text
               goal     ←    (defgoal id sentence+ alist)
          sentence      ←    (forall (gvdecl∗) implication)
            gvdecl      ←    (id+ sort) | (id+ strd) | (id+ indx)
              vmap      ←    (id id)
        implication     ←    (implies conjunction conclusion)
       conjunction      ←    conjunct | (and conjunct+)

achieves this authentication goal.

          conjunct      ←    atomic | (strand id strdvar integer (vmap∗))
                        |    (listener strdvar id)
         conclusion     ←    (false) | existential
                        |    (or existential+)
        existential     ←    conjunction | (exists (gvdecl∗) conjunction)
             atomic     ←    (p string strdvar integer)
                        |    (p string string strdvar term)
                        |    (prec strdvar index strdvar index)
                        |    (leads-to strdvar index strdvar index)
                        |    (non term) | (pnon term)
                        |    (uniq term) | (uniq-at term strdvar index)
                        |    (ugen term) | (ugen-at term strdvar index)
                        |    (conf term) | (auth term)
                        |    (= strdvar strdvar) | (= term term)
                        |    (gen-st term) | (trans strdvar index)
                        |    (comm-pr strdvar index strdvar index)
                        |    (state-node strdvar index)
                        |    (same-locn strdvar index strdvar index)
                        |    (component term term) | (fact id term*)
            strdvar     ←    symbol
              index     ←    symbol | integer
```

### 2.2 Goal Predicates

**Table 1: Predicates**

```text
 Symbol                 Sort          Description
 p role             strd × nat        Role strand length
 p role param      strd × mesg        Role parameter
 prec         strd × nat × strd × nat Precedes
 non                   atom           Non-origination
 pnon                  atom           Penetrator non-origination
 uniq                  atom           Unique origination
 uniq-at        atom × strd × nat     Unique origination on strand
 auth                  chan           Authenticated channel
 conf                  chan           Confidential channel
 =                    all × all       Equality
```

    The predicates used to construct an atomic formula (atomic) are listed in
Table 1. There are two classes of predicates, protocol specific and protocol
independent predicates, and two kinds of protocol specific predicates, role
strand length and role parameter predicates. Protocol specific predicates are
distinguished from protocol independent predicates by beginning with the
symbol p.
    The first line of the table gives the syntax of a role strand length predicate.
It contains two tokens, p and a string that names a role. That is, for role r,
there is a role strand length predicate, p r. Thus (p "init" z0 3) is an
atomic formula using the role strand length predicate for length 3 in the
init role of the protocol in Figure 1.
    The second line gives the syntax of a role parameter predicate. It contains
 three tokens, p, a string that names a role, and a string that names a
role variable. For role r, there is role parameter predicate for each variable
declared by r. Thus (p "init" "n1" z0 n1) is an atomic formula using the
role parameter predicate for parameter n1 in the init role of the protocol.
    The empty string names the listener role of a protocol. The role has the
variable x of sort mesg as its only role variable. There are two positions in
the listener role. Its trace is (trace (recv x) (send x)).
    When a variable of sort strd occurs in a formula, its length must be
specified using a role strand length formula. When an algebra variable occurs
in a formula, its association with the parameter of some role must be specified
using a role parameter formula.

### 2.3 Syntactic Abbreviations (`strand` and `listener`)

Section 7.2 described how cpsa extracts
      (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2))
from the following conjunction of facts
      (and (p "init" z0 3)
        (p "init" "n1" z0 n1) (p "init" "b" z0 b)).
    Using a conjunction of facts to represent a single defstrand is convenient for defining
and implementing a clear semantics, however it can be quite cumbersome and error prone
to specify these conjunctions. We therefore also provide support for syntactic sugar in the
goal language to allow users to represent these conjunctions in a manner much closer to the
defstrand form found in a skeleton. In particular, the user can write
      (strand init z0 3 (n1 n1) (b b))
as a single conjunct in a formula, and cpsa will ingest it with the same interpretation as if
the user had entered
      (and (p "init" z0 3)
        (p "init" "n1" z0 n1) (p "init" "b" z0 b)).
   Thus the goal in Fig. 7.1 could therefore be written as follows instead:
```scheme
      (defgoal ns
        (forall ((b name) (n1 text) (z0 strd))
          (implies
           (and (strand init z0 3 (n1 n1) (b b))
            (non (privk b)) (uniq n1))
           (exists ((z1 strd))
            (strand resp z1 2 (b b)))))).
    This representation has the benefit of being syntactically quite close to the skeleton
```
representation, and therefore the connection is more visually obvious to the user. Notice
the crucial difference that the (strand ...) form includes a strand variable after the name
of the role. While such a variable is not needed for skeletons, it is required in formulas to
allow other facts to reference the strand it represents.
    We also provide a similar abbreviation for listener strands. Instead of writing
      (and (p "" z0 1) (p "" "x" z0 n1))
we can write the following instead
      (listener z0 n1).
    These abbreviations can be used both in goals and in rules (described below in Section
 7.7).

## 3. Model-Theoretic Semantics and Characteristic Skeletons

In a defgoal sentence, the antecedent specifies the point of view skeleton.
We focus on the antecedent. In the example,

       (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2))

is extracted from

       (and (p "init" z0 3)
         (p "init" "n1" z0 n1) (p "init" "b" z0 b)).

Notice that cpsa adds a binding for a and n2 just as it does had

       (defstrand init 3 (b b) (n1 n1))

been given as input.
    Our aim now is to specify how to decide if a security goal is true in all
possible executions of a protocol. A skeleton defines a set of executions that
contain the skeleton’s structure. We say a skeleton satisfies a formula if the
skeleton contains all of the structure specified by the formula. To decide
if a skeleton satisfies a formula, we decide if it satisfies each of its atomic
formulas, and combine the results using the rules of first-order logic.
    Atomic formula (p "init" z0 3) is called a role strand length formula.
A skeleton k satisfies the formula if z0 maps to a strand s in k such that

    1. the trace of strand s in k has a length greater than 2, and

    2. the trace when truncated to length 3 is an instance of the init role.

Consider the shape in Figure 2. It satisfies (p "init" z0 3) when z0 maps
to 0.
    Atomic formula (p "init" "n1" z0 n1) is called a role parameter formula
. A skeleton k satisfies the formula if z0 maps to strand s in k, n1 first
occurs in at position i in the trace of the init role, and n1 maps to a message
algebra term t in k such that

    1. the trace of strand s in k has a length greater than i,

    2. the trace truncated to length i + 1 is an instance of the init role, and

  3. the truncated trace is compatible with mapping the init role’s "n1" role
     variable to t.

The shape in Figure 2 satisfies (p "init" "n1" z0 n1) when z0 maps to 0
and n1 maps to the message algebra term n1.
   Collectively, a skeleton satisfies the formula

     (and (p "init" z0 3)
          (p "init" "a" z0 a) (p "init" "b" z0 b)
          (p "init" "n1" z0 n1) (p "init" "n2" z0 n2))

if the skeleton contains the structure specified by

     (defstrand init 3 (a a) (b b) (n1 n1) (n2 n2)).

   The antecedent in Figure 2 contains two origination assertions. The formula
 (non (privk b)) is extracted as (privk b). A skeleton k satisfies
the formula if b maps to a message algebra term t in k such that k assumes
that t is non-originating. The unique origination formula for n1 is similarly
extracted.
   Putting it all together, the mapping

                 {n1 7→ n1, n2 7→ n2, a 7→ a, b 7→ b, z0 7→ 0}

shows that the shape in Figure 2 satisfies the antecedent of the security goal.
    The prec predicate is used to assert a node precedes another node. The
conclusion in Figure 2 with (prec z1 1 z0 2) added is satisfied by the
shape using the mapping z0 7→ 0 and z1 7→ 1.
    The uniq-at predicate is used to assert not only that an atom uniquely
originates, but also the node at which it originates. In the Figure 2 goal, the
(uniq n1) formula could have been replaced by (uniq-at n1 z0 0). The
extracted point of view skeleton is the same.
    Recall that our aim in analyzing a protocol is to find out what security
goals are true in all of its possible executions. We are interested in runs of
cpsa that show that when every shape satisfies a goal, it is true in every
execution.
    When cpsa performs a shape analysis, every shape it generates refines
the input skeleton. Skeleton refinement is defined in [4, Section 6]. The
definition makes precise the notion of structure containment, as skeleton A
refines skeleton B if and only if A contains the structure of skeleton B.

    The skeleton k0 extracted from the antecedent of a security goal has the
property that a skeleton refines k0 if and only if it satisfies the antecedent.
A skeleton with this property is called the characteristic skeleton of the
antecedent.
    Given a goal Φ, consider a shape analysis starting from the characteristic
 skeleton k0 of its antecedent. Assume cpsa finds shapes k1 , . . . , kn and
that cpsa determines that each ki satisfies Φ. Consider the executions that
contain the structure in k0 . cpsa tells us that each execution is in the executions
 that contain the structure of some ki . Furthermore, because k0 is a
characteristic skeleton, each ki satisfies the antecedent of Φ. Executions that
do not contain the structure in k0 do not satisfy the antecedent. Therefore, Φ
is true in all executions of the protocol and maximally informative.

## 4. Authentication and Secrecy Goal Examples

This section contains examples of both authentication and secrecy goals.
The first example shows the feedback the user receives when a shape does
not satisfy a security goal. The second example shows how to use a listener
to state a secrecy goal.

### 4.1 Counterexample Analysis: Needham-Schroeder Responder (`satisfies no`)

Figure 3 contains an analysis of Needham-Schroeder from the point of view
of a complete run of the responder under the assumption that the responder’s
private key is uncompromised and the nonce it generates uniquely originates.
    The conclusion of the goal asserts that in an execution compatible with
the point of view, there must be an initiator strand that agrees with the
responder strand on the name b. The shape produced by cpsa is a counterexample
 to this assertion. Because of this, cpsa annotates the shape with

      (satisfies (no (a a) (b b) (n2 n2) (z0 0))).

The annotation includes a variable mapping for the shape that satisfies the
antecedent of the goal but does not satisfy its conclusion. The reason the
shape does not satisfy the goal is because the mapping (b b) maps the
initiator’s b parameter to b, not b-0 as is required to model the shape.
    Galvin Lowe identified this authentication failure in Needham-Schroeder
and provided a fix. In the Needham-Schroeder-Lowe Protocol, the name b

is included within the encryption in second message of both roles. With this
modification, the shape found by cpsa satisfies the security goal in Figure 3,
so Needham-Schroeder-Lowe achieves this authentication goal.

```scheme
(defgoal ns                ; Goal
  (forall ((a b name) (n2 text) (z0 strd))
    (implies
      (and (p "resp" z0 3) (p "resp" "n2" z0 n2)
        (p "resp" "a" z0 a) (p "resp" "b" z0 b)
        (non (privk a)) (uniq n2))
      (exists ((z1 strd))
        (and (p "init" z1 2) (p "init" "b" z1 b))))))
```

```scheme
(defskeleton ns            ; Point of view skeleton
  (vars (a b name) (n1 n2 text))
  (defstrand resp 3 (a a) (b b) (n1 n1) (n2 n2))
  (non-orig (privk a))
  (uniq-orig n2))
```

              {|N1 , A|}KB                {|N1 , A|}KB′
      resp                                                 init
             {|N1 , N2 |}KA               {|N1 , N2 |}KA
       •                        ≺                           •
               {|N2 |}KB                   {|N2 |}KB′
       •                        ≻                           •

```scheme
(defskeleton ns            ; Shape
  (vars (n1 n2 text) (a b b-0 name))
  (defstrand resp 3 (n2 n2) (n1 n1) (b b) (a a))
  (defstrand init 3 (n1 n1) (n2 n2) (a a) (b b-0))
  (precedes ((0 1) (1 1)) ((1 2) (0 2)))
  (non-orig (privk a))
  (uniq-orig n2)
  (satisfies (no (a a) (b b) (n2 n2) (z0 0))))
```
**Figure 3: Needham-Schroeder Responder Point of View**

### 4.2 Secrecy Goal with Listeners (`(false)` Conclusion)

Figure 4 contains an analysis of Needham-Schroeder from the point of view
of a complete run of the initiator under the assumption that the responder’s
and its peer’s private keys are uncompromised and the nonce n1 it generates
uniquely originates. Futhermore, the point of view asserts that the nonce is
leaked using a listener.

      (p "" z1 1) (p "" "x" z1 n1)           ; Listener

   cpsa finds no shapes, so Needham-Schroeder achieves this secrecy goal
and does not leak n1.

```scheme
      (defgoal ns
        (forall ((a b name) (n1 text) (z0 z1 strd))
          (implies
            (and (p "init" z0 3) (p "init" "n1" z0 n1)
              (p "init" "a" z0 a) (p "init" "b" z0 b)
              (p "" z1 1) (p "" "x" z1 n1) ; Listener
              (non (privk a)) (non (privk b))
              (uniq n1))
            (false))))
```
**Figure 4: Needham-Schroeder Secrecy Goal**

## 5. Multi-Sentence Goals, Skeleton `goals` Annotations, and Shape Analysis Sentences

The examples in the previous section demonstrate the typical way security
goals are analyzed with cpsa. However, there are more features that may
be useful.
   A defgoal form may contain more than one sentence. See Figure 5 for
an example. When presented with more than one sentence, cpsa extracts
the point of view skeleton from the first sentence.

```scheme
     (defgoal ns
       (forall ((a b name) (n text) (z0 strd))
         (implies
           (and (p "init" z0 2) (p "init" "n1" z0 n)
             (p "init" "a" z0 a) (p "init" "b" z0 b)
             (non (privk a)) (non (privk b)) (uniq n))
           (exists ((z1 strd))
             (and (p "resp" z1 2) (p "resp" "b" z1 b)))))
       (forall ((a b name) (n text) (z0 strd))
         (implies
           (and (p "init" z0 2) (p "init" "n1" z0 n)
             (p "init" "a" z0 a) (p "init" "b" z0 b)
             (non (privk a)) (non (privk b)) (uniq n))
           (exists ((z1 strd))
             (and (p "resp" z1 2) (p "resp" "a" z1 a))))))
```
**Figure 5: Two Initiator Authentication Goals**

    It is wise to ensure that the antecedent in every sentence is identical.
When cpsa performs satisfaction-checking on sentence Φ, it only determines
if each shape it finds is satisfied. If the point of view skeleton is not the
characteristic skeleton of the antecedent of Φ, the fact that all skeletons
satisfy Φ cannot be used to conclude that Φ is true in all executions of the
protocol.
    cpsa performs satisfaction-checking when an input skeleton in annotated
with one or more security goals. The annotation uses the goals key.

```scheme
     (defskeleton
        ...
        (goals sent+))
```

   The program cpsasas, discussed in the next section, can be used to
generate a formula with an antecedent such that the input skeleton is the
characteristic skeleton of the antecedent.

### 5.1 Shape Analysis Sentences (`cpsa4sas`)

A shape analysis sentence expresses all that can be learned from a run of
cpsa as a security goal. If a security goal can be derived from a shape
analysis sentence, then the protocol achieves the security goal, that is, the
goal is true in all executions of the protocol.
    The program cpsasas extracts shape analysis sentences from the output
of cpsa. Consider the first example in this paper (Figure 2), which is in the
sample file goals.scm. To generate a maximally informative security goal
from the initiator point of view with ghci and Make.hs, type
      $ ghci Make.hs
      *Make> sas "goals"
When using GNU make, type “make goals sas.text”. The resulting shape
analysis sentence is displayed in Figure 6.

```scheme
(defgoal ns
  (forall ((n1 n2 text) (b a name) (z strd))
    (implies
      (and (p "init" z 3) (p "init" "n1" z n1)
        (p "init" "n2" z n2) (p "init" "a" z a)
        (p "init" "b" z b) (non (privk b)) (uniq-at n1 z 0))
      (exists ((n2-0 text) (z-0 strd))
        (and (p "resp" z-0 2) (p "resp" "n2" z-0 n2-0)
          (p "resp" "n1" z-0 n1) (p "resp" "b" z-0 b)
          (p "resp" "a" z-0 a) (prec z 0 z-0 0)
          (prec z-0 1 z 1))))))
```
**Figure 6: Initiator Shape Analysis Sentence**

   A shape analysis sentences asserts that either a realized skeleton does
not satisfy its antecedent or it satisfies one or more of the disjuncts in its
conclusion. cpsa has been designed so that this assertion is true. Therefore,
every shape analysis sentence is true in all executions.
   A security goal is true in all executions if it can be derived from a shape
analysis sentence [3]. In practice, theorem-proving using shape analysis sentences
 is rarely employed. It’s clumsy and it requires too much expertise. The
main use of cpsasas is for generating a formula that is edited to become a
desired security goal.

## 6. Axiomatic Rewrite Rules (`defrule`) and Facts (`facts`)

Support for rules was introduced in version 4.1 of cpsa.
   Each protocol includes a small collection of rules. A rule is a sentence in
the goal language presented in Section 2. Rules are defined after the roles of
a protocol are defined. The syntax of a rule follows.

              rule    ←   (defrule name sent comments)

    A rule is an axiom added to a protocol. cpsa uses the axiom as a rewrite
rule to derive zero or more new skeletons from a skeleton produced during a
step. An example of a protocol with a rule is in Figure 9 on Page 18.
    The trust rule states that when CPSA finds a person strand of length
at least one, and the inverse of it’s p parameter is non-originating, CPSA
should assume the inverse of it’s d parameter is non-originating.

### 6.1 Skeleton Fact Databases (`facts` and `fact`)

Each skeleton includes a small database of facts. A fact is a named relation
among fact terms. A fact term is either a strand of the skeleton or an algebra
term. A set of facts is defined anywhere after strands are defined using the
facts form. The syntax of facts follows.

                      facts ← (facts fact∗)
                       fact ← (symbol fterm∗)
                     fterm ← mesg | nat

   For example, in a skeleton, a user may want to note that strand 0 owns
the private key for a by assuming.

                      (facts (owns 0 (privk a)))

    Facts are most useful when combined with rules. Here is an example of
their combination. Suppose a point of view skeleton has two names, a and b,
and the problem is modeling a situation in which the two names are known
to differ. To enforce this constraint, add
                            (facts (neq a b))
to the point of view skeleton and the neq rule below to the protocol.

```scheme
      (defrule neq
        (forall ((a mesg))
          (implies
            (fact neq a a)
            (false))))
```

### 6.2 Case Study: Door Simple Example Protocol (DoorSEP) and Trust Axioms

As a motivating scenario consider the Door Simple Example Protocol
(DoorSEP), derived from an expository protocol that was designed to have
a weakness. Despite this, the protocol achieves the needs of an application,
given a trust assumption.
    Imagine a door D which is equipped with a badge reader, and a person P
equipped with a badge. When the person swipes the badge, the protocol
executes. Principals such as doors or persons are identified by the public
parts of their key pairs, with D−1 and P −1 being the corresponding private
keys. We write {|M |}K for the encryption of message M with key K. We
represent digital signatures {|M |}P −1 as if they were the result of encrypting
with P ’s private key.
    P initiates the exchange by creating a fresh symmetric key K, signing
it, and sending it to the door D encrypted with the door’s public key. D
extracts the symmetric key after checking the signature, freshly generates
a token T , and sends it—encrypted with the symmetric key—back to P .
P demonstrates they are authorized to enter by decrypting the token and
sending it as plaintext to the door. The two roles of DoorSEP are shown in
Fig. 7, where each vertical column displays the behavior of one of the roles.
The cpsa4 encoding of the roles is in Figure 9.

                        person                               door
                      {|{|K|}P −1 |}D                    {|{|K|}P −1 |}D
               •                            /                              /•
                         {|T |}K                            {|T |}K         
  Fresh: K     •o                                    o                      •    Fresh: T
                                                                            
               •
                            T           /                      T           /•
**Figure 7: DoorSEP Protocol**

    cpsa finds an undesirable execution of DoorSEP. Assume the person’s

private key P −1 is uncompromised and the door has received the token it
sent out. Then cpsa finds that P freshly created the symmetric key K.
However, nothing ensures that the person meant to open door D. If P ever
initiates a run with a compromised door C, the adversary can perform a
man-in-the-middle attack, decrypting using the compromised key C −1 and
re-encrypting with D’s public key, as elided in the · · · in Fig. 8. To verify
this result with cpsa4, remove the trust axiom in the doorsep protocol in
doc/rules.scm and run cpsa4. Thus, without additional assumptions, the
door cannot authenticate the person requesting entry.

              person                                                 door
                        {|{|K|}P −1 |}C            {|{|K|}P −1 |}D
                 •                        / ···                      /•
                                                       {|T |}K         
                                               o                      •
                                                                       
                                                         T           /•

                       Uncompromised: P            Fresh: K, T
**Figure 8: DoorSEP Weakness**

    But possibly we can trust the person to swipe her badge only in front of
doors our organization controls. And we can we ensure that our doors have
uncompromised private keys. If so, then the adversary cannot exercise the
flaw.
    We regard this as a trust assumption, and we can express it as an axiom:

Trust Assumption 1 If an uncompromised signing key P −1 is used to pre-pare
 an instance of the first DoorSEP message, then its owning principal has
ensured that the selected door D has an uncompromised private key.

The responsibility for ensuring the truth of this axiom may be split between
P and the organization controlling D. P makes sure to swipe her badge
only at legitimate doors of the organization’s buildings. The organization
maintains a security posture that protects the corresponding private keys.
Is DoorSEP good enough, assuming the trust axiom? Add the trust
axiom back to the doorsep protocol in doc/rules.scm and see. You should
find that the protocol does its job; namely, ensuring that the door opens only
when an authorized person requests it to open.

```scheme
(defprotocol doorsep basic
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
```

```scheme
(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (comment "Analyze from the doors’s perspective"))
```
**Figure 9: Door Simple Example Protocol**

## 7. Automatically Generated Rules (`defgenrule`), Built-in Relations, and Trace Annotations

### 7.1 Built-in Fact Relations (`neq`, `invk`, `lt`, `subsort`) and Generated Rules

cpsa generates certain rules either automatically in all cases or else as a consequence of
user inputs. The rules generated for a given protocol input may be found in the printed
output for that protocol; these are the formulas appearing in defgenrule forms in the .txt
and .xhtml files.

```scheme
(defprotocol doorsep basic
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
```

```scheme
(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (comment "Analyze from the doors’s perspective"))
```
**Figure 7.8: Door Simple Example Protocol**

```scheme
(defrule trust-sometimes
   (forall ((z strd) (p d akey))
           (implies
            (and (fact use-trust-rule)
                 (p "person" z 1)
                 (p "person" "p" z p)
                 (p "person" "d" z d)
                 (non (invk p)))
            (non (invk d))))
   (comment "The trust rule. Assume (fact use-trust-rule) to enable it"))
```

. . .

```scheme
(defskeleton doorsep
  (vars (p akey))
  (defstrand door 3 (p p))
  (non-orig (invk p))
  (facts (use-trust-rule))
  (comment "Analyze from the doors perspective, with trust rule"))
```
**Figure 7.9: Rule with a flag to control its use**

Negated equalities. Since negated equalities are often needed to express assumptions
users are interested in, cpsa generates three rules with the body:

(implies (fact neq x x)
         (false))

This rule has the effect of terminating a branch of analysis if two expressions that the
user has stipulated should not be equal become unified to the same value. Three rules
are generated since the variable x may be of sort mesg, or of sort strd for a strand in the
skeleton, or of sort indx meaning the index of a node along a strand. To stipulate a negated
equality between two expressions e1 , e2 , the user may write in the input file:

```scheme
(defskeleton protocol
   . . . strand declarations, etc. . . .
   (facts (neq e1 e2 )))
```

Negated equality assertions may also appear in the conclusions of user-defined rules, or
anywhere else that an atomic formula may appear.
    A good number of additional rules are generated to implement cpsa’s model of state
(see Section 8.2, esp. Figs. 8.4–8.5 and pp. 89–90).

“Assume” declarations. A formula may be provided after the trace declaration in a
defprotocol declaration in an assume clause. For instance:1

```scheme
(defrole init
    (vars ...)
    (trace ...)
    ...
    (assume (fact neq (exp (gen) upsilon) (gen))))
```

In this case, the cpsa loader checks that all of the free variables (just upsilon here) appear
in the trace. If i is the first height at which all of the variables have occurred, cpsa
generates a rule stating that any instance of the rule of height ≥ i satisfies this property of
the instances of the role parameters. In this case, i = 4, so the generated formula states:

(defgenrule assume-init-0
    (forall ((z strd) (upsilon expt))
      (implies (and (p "init" z 4) (p "init" "upsilon" z upsilon))
        (fact neq (exp (gen) upsilon) (gen)))))

Here, the assumption is the uninterpreted predicate symbol neq applied to two expressions
. However, the assumption may also involve conjunction and existential quantifiers.
       See the file dhcr_um_expt_assume.scm in the manual examples directory.

cpsa also permits disjunctions, but these typically cause unreasonable branching and bad
performance.
   In case the assumption is a fact, such as the neq assertion above, one can write

```scheme
(defrole init
    (vars ...)
    (trace ...)
    ...
    (facts (neq (gen) (exp (gen) upsilon))))
```

instead of writing the assume annotation above. Many facts may be listed as clauses here,
with the effect of a conjunction. The keyword here is the plural facts, and the singular
fact does not appear in the individual clauses.
    The facts annotation may also appear in a defskeleton query.

```scheme
(defskeleton dhcr-um
  (vars (a b name) (beta expt))
  (defstrand init 5 (a a) (b b) (beta beta))
  (non-orig (privk "sig" b))
  (facts (neq a b) (undisclosed beta)))
```

Currently, cpsa does not recognize the assume keyword in defskeleton queries.

### 7.2 Trace Annotations (`cheq`, `assume`, `rely`, `guarantee` / `guar`) and `cpsa4goals`

cpsa now allows a few types of annotations to be interspersed within the trace declaration
within a role. These are:

rely, used after a reception to declare a formula containing only free variables appearing
      up to and including this reception. Every instance of the role long enough to include
      a successful instance of this reception must satisfy the formula;

guar, used before a transmission to declare a formula containing only free variables appearing
 up to and including the following transmission. Every instance of the role long
     enough to include an instance of the following transmission must satisfy the formula.

All of these trace annotations will cause similar rules to be generated. Trace annotations
do not add to the height of the trace. They simply express constraints on what happens in
the “real” events around them.

Expressing rely and guarantee statements. In work on trust management, and on
compiling cryptographic protocols [9, 7, 11], we introduced the idea of a rely formula that
expresses what a principal learns when a message is received, possibly assuming that certain
peers are uncompromised. We also introduced the idea of a (dual) guarantee formula that

must be true in order for a principal to transmit a message. In particular, if a message
sent by a principal A has a particular guarantee formula ϕ, and a peer B receives it and
authenticates its origin with A in this step of the protocol, then B may rely on a formula
with the meaning, A says ϕ.
    This example will be sound in the sense that the authentication property ensures that
A really did say (i.e. guarantee) ϕ in any execution in which B relies on the claim. The
soundness of rely statements may be checked by analyzing the protocol with the rely state-ments
 omitted, and querying them as goal statements under the relevant non-compromise
assumptions. We will now assume that this soundness checking has been done, and that
any relevant non-compromise assumptions are made in the protocol definition.
    Thus, a rely formula definitely holds true whenever the principal successfully completes
the preceding receive event. Indeed, the operational interpretation of a rely formula is
that the principal will add an assertion to a database of its knowledge. cpsa transforms
a rely formula after a reception which is at height i in a trace into a rule stating: “long-enough
” instances of the role will satisfy the formula, for that instance’s values of the role
parameters.
    This transformation is similar to what cpsa does for a cheq annotation, except that
instead of an equation, the conclusion may involve other atomic formulas, conjunctions,
and existential quantifiers. Disjunctions are permitted, but will usually lead to intractable
cpsa analysis.
    A guarantee formula has a dual relation with a subsequent transmission. Just as the
received message may determine the instances of parameters appearing in a rely formula,
a guarantee formula may dually select instances of parameters that will appear in the
subsequent transmission. As a rely formula is interpreted operationally as an assert to a
database held by the principal, a guarantee formula is interpreted operationally as a query
against that database. Hence, assertions caused by previous rely formulas may influence
the parameter instances selected by subsequent guarantee formulas.

A rely-guarantee example. Consider a protocol in which a customer will interact with
a merchant and a bank to purchase an item at a cost; the merchant will be paid by a debit
from the customer’s account at the bank. Each participant should obtain evidence that
the expected peers are participating in a corresponding session. Moreover, the merchant
does not need to know the customer’s account number, and therefore should not see this
information. The bank does not need to know what item the customer is buying, and
therefore should not see that. Outsiders should not see the details at all. How best to
achieve this goal?
    Each party will need to generate a digital signature, since in case of dispute a third
party must be able to reconstruct who committed to paying whom, and to sending what
merchandise. Moreover, public key encryption will be needed, at least for a handshake,
since the parties must protect secrets from the outsiders and from the third party. Thus,
there is no way to avoid having three digital signatures generated, along with a similar

number of public key encryptions, with corresponding verification and decryption actions.
A protocol that achieves this goal is found in examples/minipay.scm.
    Each party is making assertions, in effect. The customer asserts his desire to buy the
item for the cost. The bank asserts that it will transfer the funds to the merchant. The
merchant asserts that it will ship the item. Moreover, the protocol should ensure that each
party knows that the others have made these commitments. For instance, the merchant is
willing to ship the goods because it knows that the bank will transfer the payment. Thus,
each party makes a guarantee, and each party learns that it may rely on its peers having
made their guarantee. A fine point is the bank’s rely formula; it learns that the customer
has requested some item in exchange for the cost, but not which one. Thus, the item is
existentially bound in the bank’s rely formula.
    This yields the rely and guarantee formulas displayed in Fig. 7.10; the protocol with
these trust annotations may be found in examples/minipay-rely-guar.scm. The principals
 in a particular session are required not to proceed past a guarantee formula unless the
instances of the variables are known to satisfy the property claimed. The rely formulas
summarize what they have learned in the preceding reception.
    But: How do we know these formulas are in fact true in every execution that includes
the preceding reception, or at least every execution satisfying some reasonable assumptions
about uncompromised keys?
    We can use goal formulas to check this. In a separate file, examples/minipay-guar.scm,
we define the protocol with the same message structure and guarantee formulas, but with
no rely formulas. We now pose goal statements for cpsa to resolve; these are shown in
Fig. 7.11–7.12. In these formulas, the conclusions are the rely statements that must be
justified. The hypotheses say that there is a strand z instantiating the relevant role long
enough to reach the rely statement position. They also connect the variables in the rely
formula with the parameters of z. Moreover, each customer goal assumes only the relevant
peer’s signature key to be non-compromised. The merchant assumes only the bank’s signing
key non-compromised, which is desirable since it may have no long-term association with
the customer. The bank presumably has an association with the customer, established
when the customer opened the account; the customer’s signing key could be established at
that time.
    The goals may be constructed from the generated rules cpsa provides when processing
 examples/minipay-rely-guar.scm, essentially adding the non-compromise assumptions
.
    Since cpsa validates these goal formulas in the minipay-guar protocol that contains
the guarantee formulas but not the rely formulas, the generated rules introduced by the
rely formulas are also sound subject to the stated non-compromise assumptions.
    We regard this rely-guarantee method as a systematic way to formalize the trust assumptions
, and the effects, of protocols that accomplish real-world tasks, in this case purchase
and payment.

```scheme
(defrole cust (vars ...)
  (trace
    (guar (fact buy-via c m b item cost n))
    (send ...)
    (recv ...)           ; from bank
    (rely (fact will-transfer c m b cost n mtr btr))
    (recv ...)           ; from merchant
    (rely (fact will-ship c m b item mtr))))
```

```scheme
(defrole merc (vars ...)
  (trace
    (recv ...)           ; from customer
    (send ...)
    (recv ...)           ; from bank
    (rely (and (fact buy-via c m b item cost n)
               (fact will-transfer c m b cost n mtr btr)))
    (guar (fact will-ship c m b item mtr))
    (send ...)))
```

```scheme
(defrole bank (vars ...)
  (trace
    (recv ...)
    (rely (exists ((item merchandise))
                  (fact buy-via c m b item cost n)))
    ;; Do not proceed unless customer signature trustworthy.
    ;; Given that, now commit to transferring the funds
    (guar (and (non (privk "sig" c))
               (fact will-transfer c m b cost n mtr btr)))
    (send ...)))
```
**Figure 7.10: Rely and gauantee formulas in minipay.scm**

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (cost amount) (n data) (mtr btr text))
   (implies
    (and (p "cust" z 2)
         (p "cust" "c" z c)
         (p "cust" "m" z m)
         (p "cust" "b" z b)
         (p "cust" "cost" z cost)
         (p "cust" "n" z n)
         (p "cust" "mtr" z mtr)
         (p "cust" "btr" z btr)
         (non (privk "sig" b)))
    (fact will-transfer c m b cost n mtr btr))))
```

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (item merchandise) (n data) (mtr btr text))
   (implies
    (and (p "cust" z 3)
         (p "cust" "c" z c)
         (p "cust" "m" z m)
         (p "cust" "b" z b)
         (p "cust" "item" z item)
         (p "cust" "n" z n)
         (p "cust" "mtr" z mtr)
         (p "cust" "btr" z btr)
         (non (privk "sig" m)))
    (fact will-ship c m b item mtr))))
```
**Figure 7.11: Goal statements to validate customer’s rely formulas**

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (item merchandise) (cost amount) (n data) (mtr btr text))
   (implies
    (and (p "merc" z 3)
         (p "merc" "c" z c)
         (p "merc" "m" z m)
         (p "merc" "b" z b)
         (p "merc" "item" z item)
         (p "merc" "cost" z cost)
         (p "merc" "n" z n)
         (p "merc" "mtr" z mtr)
         (p "merc" "btr" z btr)
         (non (privk "sig" b)))
    (and (fact will-transfer c m b cost n mtr btr)
         (fact buy-via c m b item cost n)))))
```

```scheme
(defgoal minipay-guar
  (forall
   ((z strd) (c m b name) (cost amount) (n data))
   (implies
    (and (p "bank" z 1)
         (p "bank" "c" z c)
         (p "bank" "m" z m)
         (p "bank" "b" z b)
         (p "bank" "cost" z cost)
         (p "bank" "n" z n)
         (non (privk "sig" c)))
    (exists ((item merchandise))
            (fact buy-via c m b item cost n)))))
```
**Figure 7.12: Goal statements to validate other rely formulas**

## 8. Lemmas (`deflemma`)

One common way in which rules have been used in cpsa is as lemmas. The analyst would
define a goal as a query and run cpsa to check that the goal is satisfied. Then the goal
can be added to the protocol as a rule to help speed up the search for subsequent queries.
One common example is when cpsa repeatedly undergoes a long search to satisfy a listener
for some key that cannot be satisfied. Validating once and for all that the key cannot be
leaked, and then including that fact as a rule can drastically improve performance.
    Unfortunately, the syntax for doing so was not particularly friendly to the user. The
formula stated as a defgoal query resides outside the protocol, while the defrule version
 must be included inside the protocol. Managing these lemmas could become difficult
as there was no built-in management to help determine which rules had previously been
validated as lemmas that hold.
    For this reason, cpsa also includes a deflemma form. It must be place outside the
protocol at the top level, just as a defgoal form. However, the syntax for a lemma differs
slightly from that of a goal in ways that allow cpsa to help manage the complexities that
arise from sometimes wanting to validate a formula as a goal and sometimes wanting to use
it as a rule. The user should look at tst/lemmas.scm for an example of the syntax.
    Compared to a defgoal, a deflemma has two extra arguments that come at the beginning
. The first is a flag that signals to cpsa whether or not it should include a query for
the lemma in order to validate that it is satisfied. There are three valid values: rule, goal,
and both. The second is a name that will be used as the rule name when the lemma is
used as a rule.
    When a lemma uses the rule flag, cpsa will update the protocol identified in the
lemma to include the specified formula as a rule. As a result, all subsequent queries for
that protocol will include the lemma as a rule. cpsa will not generate a query for the
lemma. The result is the same as if a copy of the protocol with the same name had been
added in this location with an extra defrule added to it (hence only subsequent queries
would use the rule).
    The goal flag signals cpsa to treat the lemma as if it were a defgoal. A query will be
added to the analysis, but it will not be included as a rule in any subsequent queries. The
skeletons in the analysis contain a comment indicating the name of the lemma the analysis
is associated with.
    When the both flag is used, the behavior is first to treat the lemma as a goal, and then
as a rule. cpsa will first create a query for the lemma against the specified protocol before
updating the protocol to include the lemma as a rule for subsequent queries.
    Since cpsa updates the protocol with a rule at load time, it cannot know in advance
whether the lemma is satisfied or not. That means that subsequent queries will use the
lemma as a rule, even if the query for the lemma shows that the lemma is not satisfied ! For
this reason, the added rule contains a comment to indicate whether or not an associated
query has been added to check its validity. When the both flag is used for a lemma that is

not satisfied, since a query for the formula is generated as a goal, the output will contain
(satisfies (no ...)) as evidence that some goal was not satisfied.

## 9. Formal Specification of Shape Analysis Sentences (Coherent Logic)

For each point-of-view skeleton and its shapes found by cpsa, there is a
formula in a language of order-sorted first-order logic called  W a shape analysis
 sentence. The sentence has a special form, ∀X(Ψ ⊃ i ∃Yi (∆i ∧ Φi )),
where Ψ, ∆i , and Φi are conjunctions of atomic formulas and X and Yi are
variable sets. This fragment of first-order logic is called coherent logic. Formula
 Ψ describes the point-of-view skeleton k0 . For each homomorphism to
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

### 9.1 Formal Syntax and Satisfaction Semantics of Skeleton Formulas
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
Recall that ΘX is the strand space defined by I, see Section 5.4. We de-fine
 F(k) = (Y, Φ), where Φ is k’s skeleton formula, and Y is the formula’s
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
    The structure preserving maps δi = (ϕi , σi ) are encoded in ∆i by a conjunction
 of equalities. Map σi is coded as equalities between a message algebra
 variable in the domain of σi and the term it maps to. Map ϕi is coded as
equalities between strand variables in Φ0 and strand variables in Φi . Let Z0
be the strand variables freshly generated for k0 , and Zi be the ones generated
for ki . The strand mapping part of ∆i is
                             ^
                                   Z0 (s) = Zi (ϕi (s)).
                              s∈Dom(Z0 )

    The shape analysis sentence for the second analysis of Blanchet’s Simple
 Example Protocol in Section 5.1 is displayed in Figure C.1. The strand
length predicate P [r, h](z) is written rh (z), and the strand parameter predicate
 P [r, x](z, t) is written rx (z, t) with the protocol left implicit.

#### 9.1.1 Semantics of Skeleton Formulas (`k, α |= Φ`)

**Semantics of Skeleton Formulas.** Let k = kX (P, I, ≺, N, U ) and ΘX be
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

#### 9.1.2 Channel Formulas (`auth` and `conf`)

**Channel Formulas.** This appendix has not been updated to reflect the
inclusion of channels into cpsa, but the changes made are straightforward.
There are two new unary predicate symbols, auth and conf, that are similar
to non except their argument must be a variable of sort chan. For skeleton k
and variable assignment α, auth(c) is satisfied iff α(c) ∈ auth(k), and conf(c)
is satisfied iff α(c) ∈ conf (k).

## 10. References
[1] Joshua D. Guttman. Establishing and preserving protocol security goals.
    Journal of Computer Security, 22(2):201–267, 2014.

[2] Joshua D. Guttman, Moses D. Liskov, and Paul D. Rowe. Security goals
    and evolving standards. In Liqun Chen and Chris Mitchell, editors, Security
 Standardization Research, volume 8839 of LNCS, pages 93–110.
    Springer, December 2014.

[3] John D. Ramsdell. Deducing security goals from shape analysis sentences.
    The MITRE Corporation, April 2012. http://arxiv.org/abs/1204.
    0480.

[4] John D. Ramsdell and Joshua D. Guttman. CPSA Primer. The MITRE
    Corporation, 2009. In https://github.com/mitre/cpsaexp source distribution
, doc directory.

[5] John D. Ramsdell, Joshua D. Guttman, Moses D. Liskov, and Paul D.
    Rowe. The CPSA Specification: A Reduction System for Searching for
    Shapes in Cryptographic Protocols. The MITRE Corporation, 2009. In
    https://github.com/mitre/cpsaexp source distribution, doc directory.
