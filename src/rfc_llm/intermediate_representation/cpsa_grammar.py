"""MITRE CPSA 4.4.9 Formal Grammar, Keywords, and Arity Specifications.

Derived directly from the authoritative MITRE CPSA Manual Chapters 2, 3, 4, 10 (Tables 10.1 - 10.6).
Provides static typing (Literals and Enums) and compile-time validation for all stages
of CPSA Scheme S-expression and JSON generation.
"""

from typing import Any, Dict, List, Literal, Optional, Set, Tuple, Union, get_args


# =============================================================================
# STAGE 1: Top-Level Scheme S-Expression Forms (Table 10.1)
# =============================================================================
CPSATopLevelKeyword = Literal[
    "herald",
    "defprotocol",
    "defskeleton",
    "defmacro",
    "defrule",
    "defgenrule",
    "defgoal",
    "deflemma",
    "comment",
]
CPSA_TOP_LEVEL_KEYWORDS: Set[str] = set(get_args(CPSATopLevelKeyword))


# =============================================================================
# STAGE 2: Cryptographic Message Algebras (Tables 10.2 & 10.4)
# =============================================================================
CPSAMessageAlgebra = Literal[
    "basic",
    "diffie-hellman",
]
CPSA_ALGEBRAS: Set[str] = set(get_args(CPSAMessageAlgebra))


# =============================================================================
# STAGE 3: Role Declaration Keywords (defrole) (Table 10.1 & Table 10.6)
# =============================================================================
CPSARoleKeyword = Literal[
    "defrole",
    "vars",
    "trace",
    "inputs",
    "outputs",
    "params",
    "returns",
    "non-orig",
    "pen-non-orig",
    "uniq-orig",
    "uniq-gen",
    "role_orig",
    "role-orig",
    "conf",
    "auth",
    "gen-st",
    "priority",
    "facts",
    "assume",
    "comment",
]
CPSA_ROLE_KEYWORDS: Set[str] = set(get_args(CPSARoleKeyword))


# =============================================================================
# STAGE 4: Preskeleton Declaration Keywords (defskeleton) (Table 10.1 & Table 10.6)
# =============================================================================
CPSASkeletonKeyword = Literal[
    "defskeleton",
    "vars",
    "defstrand",
    "defstrandmax",
    "deflistener",
    "non-orig",
    "pen-non-orig",
    "uniq-orig",
    "uniq-gen",
    "precedes",
    "leadsto",
    "priority",
    "facts",
    "goal",
    "comment",
]
CPSA_SKELETON_KEYWORDS: Set[str] = set(get_args(CPSASkeletonKeyword))


# =============================================================================
# STAGE 5: Trace Event Actions & Channels (Section 10.2, Table 10.1)
# =============================================================================
CPSATraceAction = Literal[
    "send",
    "recv",
    "load",
    "stor",
]
CPSA_TRACE_ACTIONS: Set[str] = set(get_args(CPSATraceAction))

CPSATraceAnnotation = Literal[
    "cheq",
    "rely",
    "guarantee",
]
CPSA_TRACE_ANNOTATIONS: Set[str] = set(get_args(CPSATraceAnnotation))


# =============================================================================
# STAGE 6: Message Term Operators (Tables 10.3 & 10.5)
# =============================================================================

# Basic Crypto Algebra Operators (Table 10.3)
CPSABasicOperator = Literal[
    "enc",     # {| m0 ... mn |}k  (arity >= 2)
    "hash",    # #m0 ... mn        (arity >= 1)
    "cat",     # (m0, ..., mn)     (arity >= 1)
    "pubk",    # K(a) or K(a, s)   (arity 1 or 2)
    "privk",   # K(a)^-1           (arity 1 or 2)
    "invk",    # k^-1              (arity 1)
    "ltk",     # ltk(a, b)         (arity 2)
]
CPSA_BASIC_OPERATORS: Set[str] = set(get_args(CPSABasicOperator))

# Diffie-Hellman Crypto Algebra Operators (Table 10.5)
CPSADHOperator = Literal[
    "bltk",    # bltk(a, b) = bltk(b, a) (arity 2)
    "exp",     # h^x                     (arity 2)
    "gen",     # g                       (arity 0)
    "mul",     # x * y                   (arity >= 2)
    "rec",     # x^-1                    (arity 1)
    "one",     # 1                       (arity 0)
]
CPSA_DH_OPERATORS: Set[str] = set(get_args(CPSADHOperator))

# All Authorized Term Operators
CPSAAllOperator = Literal[
    "enc",
    "hash",
    "cat",
    "pubk",
    "privk",
    "invk",
    "ltk",
    "bltk",
    "exp",
    "gen",
    "mul",
    "rec",
    "one",
]
CPSA_ALL_OPERATORS: Set[str] = set(get_args(CPSAAllOperator))


# =============================================================================
# STAGE 7: Operator Arity Constraints (Tables 10.3 & 10.5)
# =============================================================================
# Format: int (exact), set (one of allowed integers), tuple (min, max or None)
CPSA_OPERATOR_ARITY: Dict[str, Union[int, Set[int], Tuple[int, Optional[int]]]] = {
    "enc": (2, None),       # at least 1 payload + 1 key
    "hash": (1, None),      # at least 1 payload
    "cat": (1, None),       # at least 1 term
    "pubk": {1, 2},         # (pubk name) or (pubk name tag)
    "privk": {1, 2},        # (privk name) or (privk name tag)
    "invk": 1,              # (invk akey_var)
    "ltk": 2,               # (ltk name1 name2)
    "bltk": 2,              # (bltk name1 name2)
    "exp": 2,               # (exp base expt)
    "gen": 0,               # (gen)
    "mul": (2, None),       # at least 2 exponent factors
    "rec": 1,               # (rec expt)
    "one": 0,               # (one)
}


# =============================================================================
# STAGE 8: JSON Schema Specification for Strongly-Typed Term AST
# =============================================================================
CPSA_TERM_JSON_SCHEMA: Dict[str, Any] = {
    "title": "CPSATerm",
    "description": (
        "A CPSA 4.4.9 message term: an identifier atom string (e.g. client_random, K_ab), "
        "an integer constant, or a prefix S-expression list [operator, ...args] where operator "
        "is strictly one of: enc, hash, cat, pubk, privk, invk, ltk, bltk, exp, gen, mul, rec, one."
    ),
    "anyOf": [
        {"type": "string", "description": "Identifier atom, variable, or string literal"},
        {"type": "integer", "description": "Integer constant"},
        {
            "type": "array",
            "description": "Prefix operator expression: [operator, ...subterms]",
            "items": {
                "anyOf": [
                    {
                        "type": "string",
                        "enum": sorted(list(CPSA_ALL_OPERATORS)),
                        "description": "Leading CPSA 4.4.9 operator keyword",
                    },
                    {"type": "string", "description": "Subterm variable or constant"},
                    {"type": "integer"},
                    {"type": "array", "description": "Nested subterm expression"},
                ]
            },
            "minItems": 1,
        },
    ],
}


# =============================================================================
# STAGE 9: Canonical Desugaring Mappings (Frontend Compiler Normalizer)
# =============================================================================
# Maps foreign cryptographic operators (from ProVerif, Tamarin, or LLM hallucinations)
# to their canonical MITRE CPSA 4.4.9 equivalents.
CPSA_DESUGAR_MAP: Dict[str, str] = {
    "aenc": "enc",
    "senc": "enc",
    "asym_enc": "enc",
    "sym_enc": "enc",
    "sign": "enc",
    "mac": "hash",
    "hmac": "hash",
}


def desugar_term_tree(term: Any) -> Any:
    """Recursively desugars foreign/hallucinated crypto operators and dictionary nodes to canonical CPSA primitives."""
    if isinstance(term, list):
        if not term:
            return term
        new_list = list(term)
        op = new_list[0]
        if isinstance(op, str) and op in CPSA_DESUGAR_MAP:
            new_list[0] = CPSA_DESUGAR_MAP[op]
        return [desugar_term_tree(x) for x in new_list]
    if isinstance(term, dict):
        # Extract atomic identifier name from dictionary variable representation
        for key in ("name", "variable", "identifier", "var", "id", "atom", "field", "val", "value"):
            if key in term and isinstance(term[key], str):
                return term[key]
        if "term" in term:
            return desugar_term_tree(term["term"])
        if "args" in term and isinstance(term.get("op"), str):
            return desugar_term_tree([term["op"]] + term["args"])
        for v in term.values():
            if isinstance(v, str):
                return v
    return term


def validate_cpsa_term_syntax(
    term: Any,
    algebra: CPSAMessageAlgebra = "basic",
    path: str = "term",
) -> None:
    """Statically validates that a term tree conforms strictly to MITRE CPSA 4.4.9 grammar.

    Enforces:
    1. Operator existence in the authorized CPSA signature.
    2. Message algebra compatibility (forbidding DH operators under 'basic' algebra).
    3. Strict operator arity matching Tables 10.3 & 10.5.
    4. Inductive validation of all subterms.

    Raises:
        ValueError: If an unrecognized keyword, algebra incompatibility, or arity defect is found.
    """
    if isinstance(term, (str, int)):
        return

    if isinstance(term, list):
        if not term:
            raise ValueError(f"Empty term expression at '{path}'. Expected atom or operator form.")

        op = term[0]
        if not isinstance(op, str):
            raise ValueError(f"First element of expression at '{path}' must be an operator string, got {type(op).__name__}.")

        # 1. Operator Keyword Authorization
        if op not in CPSA_ALL_OPERATORS:
            raise ValueError(
                f"Unknown operator keyword '{op}' at '{path}'. "
                f"Valid CPSA 4.4.9 operators: {sorted(list(CPSA_ALL_OPERATORS))}"
            )

        # 2. Algebra Compatibility Check
        if algebra == "basic" and op in CPSA_DH_OPERATORS:
            raise ValueError(
                f"Diffie-Hellman operator '{op}' at '{path}' is forbidden under 'basic' message algebra. "
                "Change protocol message_algebra to 'diffie-hellman' to use exponentiation/DH features."
            )

        # 3. Arity Validation
        args = term[1:]
        arity = len(args)
        expected = CPSA_OPERATOR_ARITY.get(op)

        if isinstance(expected, int):
            if arity != expected:
                raise ValueError(
                    f"Operator '{op}' at '{path}' expects exactly {expected} arguments, got {arity}: {term}"
                )
        elif isinstance(expected, set):
            if arity not in expected:
                raise ValueError(
                    f"Operator '{op}' at '{path}' expects arity in {sorted(list(expected))}, got {arity}: {term}"
                )
        elif isinstance(expected, tuple):
            min_args, max_args = expected
            if arity < min_args:
                raise ValueError(
                    f"Operator '{op}' at '{path}' expects at least {min_args} arguments, got {arity}: {term}"
                )
            if max_args is not None and arity > max_args:
                raise ValueError(
                    f"Operator '{op}' at '{path}' expects at most {max_args} arguments, got {arity}: {term}"
                )

        # 4. Inductive Recursive Subterm Validation
        for idx, subterm in enumerate(args, 1):
            validate_cpsa_term_syntax(subterm, algebra=algebra, path=f"{path}[{idx}]")
    else:
        raise ValueError(
            f"Invalid term node at '{path}'. Expected string atom, integer, or nested operator list, got {type(term).__name__}."
        )
