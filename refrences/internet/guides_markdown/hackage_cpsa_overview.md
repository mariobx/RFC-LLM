Hackage :: [Package]

* 
      
        Search 

* Browse

* What's new

* Upload

* User accounts

# cpsa: Symbolic cryptographic protocol analyzer

      [ bsd3, cryptography, program ]
      [ Propose Tags ]
      [ Report a vulnerability ]

The Cryptographic Protocol Shapes Analyzer (CPSA) attempts to
enumerate all essentially different executions possible for a
cryptographic protocol.  We call them the shapes of the protocol.
Many naturally occurring protocols have only finitely many, indeed
very few shapes.  Authentication and secrecy properties are easy to
determine from them, as are attacks and anomalies, and an auxiliary
tool reads off strongest authentication and secrecy goals from the
shapes.
For each input problem, the CPSA program is given some initial
behavior, and it discovers what shapes are compatible with it.
Normally, the initial behavior is from the point of view of one
participant.  The analysis reveals what the other participants must
have done, given the participant's view.  The search is complete,
i.e. we proved every shape can in fact be found in a finite number
of steps, relative to a procedural semantics of protocol roles.
The package contains a set of programs used to perform the analysis
and display it in a browser.  Program documentation is in the doc
directory in the source distribution, and installed in the package's
data directory.  You can locate the package's data directory by
typing "cpsa --help" to a command prompt.  New users should study
the documentation and the sample inputs in the data directory.  The
source distribution includes a test suite with an expanded set of
input files and is easily installed on operating systems that decend
from Unix.  Serious Windows users should install MSYS so as to allow
the use of make and script execution.
The theory and algorithm used by CPSA was developed with the help of
Joshua D. Guttman, John D. Ramsdell, Jon C. Herzog, Shaddin
F. Doghmi, F. Javier Thayer, Paul D. Rowe, and Moses D. Liskov.
John D. Ramsdell implemented the algorithm in Haskell.  CPSA was
designed and implemented at The MITRE Corporation.

          [Skip to Readme]

## Downloads
* cpsa-4.4.9.tar.gz [browse] (Cabal source package)
* Package description (as included in the package)

#### Maintainer's Corner
          
Package maintainers

* 
              JohnRamsdell, mliskov, joshuaguttman, pauldavidrowe

For package maintainers and hackage trustees

* 
              
                edit package information

Candidates

* 
              No Candidates

              Versions [RSS]
              2.0.0, 2.0.2, 2.0.3, 2.0.4, 2.0.5, 2.1.0, 2.1.1, 2.1.2, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4, 2.2.5, 2.2.6, 2.2.7, 2.2.8, 2.2.9, 2.2.10, 2.2.11, 2.2.12, 2.2.13, 2.3.0, 2.3.1, 2.3.2, 2.3.3, 2.3.4, 2.3.5, 2.4.0, 2.5.0, 2.5.1, 2.5.2, 2.5.3, 2.5.4, 3.3.0, 3.3.1, 3.3.2, 3.4.0, 3.4.1, 3.5.0, 3.5.1, 3.6.0, 3.6.1, 3.6.2, 3.6.3, 3.6.4, 3.6.5, 3.6.6, 3.6.7, 3.6.8, 3.6.9, 3.6.10, 3.6.11, 4.4.1, 4.4.2, 4.4.3, 4.4.4, 4.4.5, 4.4.6, 4.4.7, 4.4.8, 4.4.9

              Change log
              ChangeLog

              Dependencies
              base (>=4.13 && <5), containers (>=0.8 && <0.9), deepseq (>=1.4.8 && <1.5), directory (>=1.3.8 && <1.4), parallel (>=3.3.0 && <3.4) [details]

              License
              BSD-3-Clause

              Author

              Maintainer
              prowe@mitre.org

              Uploaded
              by pauldavidrowe at 2026-05-24T16:08:07Z

              Category
              Cryptography

              Source repo
              head: git clone https://github.com/mitre/cpsa.git

              Distributions

              Reverse Dependencies
              1 direct, 0 indirect  [details]

              Executables
              cpsa4dl, cpsa4dbprolog, cpsa4db, cpsa4query, cpsa4debranch, cpsa4rolecoq, cpsa4coq, cpsa4roletran, cpsa42latex, cpsa4init, cpsa4json, cpsa4pp, cpsa4shapes, cpsa4graph, cpsa4diff, cpsa4goalsat, cpsa4prot, cpsa4sas, cpsa4

              Downloads
              44969 total (309 in the last 30 days)

               Rating
              2.25 (votes: 2)
              [estimated by Bayesian average]

              Your Rating

* λ
                  
* λ
                  
* λ

              Status
              Docs not available [build log]All reported builds failed as of 2026-05-24 [all 2 reports]

## Readme for cpsa-4.4.9
      [back to package description]
      
 `CPSA4: Cryptographic Protocol Shapes Analyzer Version 4

The Cryptographic Protocol Shapes Analyzer (CPSA) attempts to
enumerate all essentially different executions possible for a
cryptographic protocol.  We call them the shapes of the protocol.
Naturally occurring protocols have only finitely many, indeed very few
shapes.  Authentication and secrecy properties are easy to determine
from them, as are attacks and anomalies.

For each input problem, the CPSA program is given some initial
behavior, and it discovers what shapes are compatible with it.
Normally, the initial behavior is from the point of view of one
participant.  The analysis reveals what the other participants must
have done, given the participant's view.  The search is complete,
i.e. we proved every shape can in fact be found in a finite number of
steps, relative to a procedural semantics of protocol roles.

CPSA4 is based on a refactoring of CPSA2.  It is distinct from CPSA3.
It is used to experiment with new features.  It is where a different
security goal language, the strand-oriented language described in
"Deducing Security Goals From Shape Analysis Sentences"
<https://arxiv.org/abs/1204.0480>, was first implemented.  The size of
the formulas expressed in the strand-oriented language is typically
smaller than the ones produced using the previous node-oriented
language, an important property when the formulas are used to interact
with theorem provers and proof assistants.

CPSA4 provides rules and facts.  Rules are associated with protocols,
and facts are associated with skeletons.  A rule is a geometric
formula that is used as a rewrite rule, and a fact is a named relation
between values.

CPSA4 provides channels.  Channels are designed to model confidential
and authenticated communication channels.

This program has been built and tested using the Haskell miminal
installer and Haskell Platform.  These are available from
<http://haskell.org> or from an operating system specific source.  The
name of the Linux package is usually haskell-platform.  If you have
problems installing Haskell, try using Haskell Stack, and issue the
commands "stack init; stack build, stack install".

INSTALLING FROM A TARBALL

Build and install with:

$ cabal build
$ cabal install --overwrite-policy=always

DOCUMENTATION LOCATION

To find the directory containing documentation and samples, type:

$ cpsa4 -h

QUICK START (Linux)

: To analyze a protocol you have put in prob.scm type:
$ cpsa4 -o prob.txt prob.scm
$ cpsa4graph -o prob.xhtml prob.txt
$ firefox -remote "openFile(`pwd`/prob.xhtml)"

QUICK START (Mac)

: To analyze a protocol you have put in prob.scm type:
$ cpsa4 -o prob.txt prob.scm
$ cpsa4graph -o prob.xhtml prob.txt
$ open prob.xhtml

QUICK START (Windows)

With Cygwin or MinGW, the installation is similar to the Linux
install.  The software has been tested on a Windows system on which
neither MinGW or Cygwin has been installed.  Install Haskell Platform
Core and then run:

C:\...> cabal update
C:\...> cabal install parallel
C:\...> cabal build
C:\...> cabal install --overwrite-policy=always

Documentation and samples are in the directory given by
C:\...> cpsa4 -h

The installed programs can be run from the command prompt or via a
batch file.  Alternatively, copy doc/Make4.hs into the directory
containing your CPSA problem statements, and load it into a Haskell
interpreter.  Read the source for usage instructions.

MAKEFILE

To start your own project, create a fresh directory and then type:

$ cpsa4init

This will create a Makefile that automates the analysis process.  For
Windows, it will also create Make4.hs, a cpsa build script written in
Haskell.

PARALLELISM

CPSA is built so it can make use of multiple processors.  To make use
of more than one processor, start CPSA with the -N runtime flag, as in
"+RTS -N -RTS".  The GHC documentation describes the -N option in
detail.

DOCUMENTATION

The starting point for CPSA documentation doc/index.html.  Most users
should read it and skip the rest of this section.  The documentation
includes a user guide as an XHTML document, and three LaTeX documents.
The CPSA Primer provides the background required to make effective use
of the CPSA tool collection.  For those interested in the
implementation, The CPSA Theory contains a high-level description of
the algorithm and the current state of the effort to show that when
program terminates, it produces a description of every possible
execution of the protocol consistent with the initial point-of-view
skeleton.  The CPSA Specification formally describes the implemented
algorithm as a term reduction system.  The CPSA Design describes
implementation details and assumes The CPSA Specification has been
read.  The CPSA Design should be read if one is interested in reading
the Haskell source for the tool collection.

TEST SUITE

Cabal currently fails to preserve permissions correctly.  To fix this
problem, type:

$ /bin/sh fixperms

: To run the test suite type:
$ ./cpsatst

Tests with the .scm extension are expected to complete without error,
tests with the .lsp extension are expected to fail, and tests with the
.lisp extension are not run.  New users should read tst/README, and
then browse the files it suggests while reading CPSA documentation.

ADDITIONAL PROGRAMS

The src directory of the source distributions includes programs
written in Scheme, Prolog, Elisp, and OCaml for performing tasks.  Use
them as templates for your special purpose CPSA analysis and
transformation needs.  Also, when given the --json option, the CPSA
pretty printer cpsapp will transform CPSA S-expressions into
JavaScript Object Notation (JSON).

On Linux, the GHC runtime can request so much memory that thrashing
results.  The script in src/ghcmemlimit sets an environment variable
that limits memory to the amount of free and reclaimable memory on
your machine.

KNOWN BUGS

Variable separation in generalization fails to separate variables in
terms of the form (ltk a a).
` 

    Produced by hackage and Cabal 3.16.1.0.