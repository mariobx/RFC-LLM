"""MITRE CPSA 4.4.9 Formal Grammar, Scoped Keywords, and Arity Specifications.

Derived directly from the authoritative MITRE CPSA 4.4.9 User Manual:
- Chapters 2, 3, 4, 7, 10 (Tables 7.1, 10.1 – 10.6, Equation 10.1)
- CPSA4 Roletran Specification (`cpsa4roletran.md` & `Role_Translations.md`)

Enforces strict syntactic and positional scoping so every CPSA keyword, sort,
and operator can only appear in the exact grammatical production where the
MITRE CPSA 4.4.9 specification allows it.
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
# STAGE 3: Scoped Declaration Keywords (Table 10.1, Table 10.6 & Roletran)
# =============================================================================

# Declaration keywords valid in BOTH defrole and defskeleton (Table 10.6)
CPSASharedDeclarationKeyword = Literal[
    "vars",
    "non-orig",
    "pen-non-orig",
    "uniq-orig",
    "uniq-gen",
    "conf",
    "auth",
    "gen-st",
    "priority",
    "facts",
    "comment",
]
CPSA_SHARED_DECLARATION_KEYWORDS: Set[str] = set(get_args(CPSASharedDeclarationKeyword))

# Keywords valid EXCLUSIVELY inside defrole (Table 10.1, Table 10.6, cpsa4roletran)
CPSARoleOnlyKeyword = Literal[
    "defrole",
    "trace",
    "inputs",
    "outputs",
    "params",
    "returns",
    "assume",
    "ind-zero",
]
CPSA_ROLE_ONLY_KEYWORDS: Set[str] = set(get_args(CPSARoleOnlyKeyword))

# Complete set of authorized keywords inside a (defrole ...) form
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
    "conf",
    "auth",
    "gen-st",
    "priority",
    "facts",
    "assume",
    "ind-zero",
    "comment",
]
CPSA_ROLE_KEYWORDS: Set[str] = set(get_args(CPSARoleKeyword))

# Keywords valid EXCLUSIVELY inside defskeleton (Table 10.1 & Table 10.6)
CPSASkeletonOnlyKeyword = Literal[
    "defskeleton",
    "defstrand",
    "defstrandmax",
    "deflistener",
    "precedes",
    "leadsto",
    "goal",
    "goals",
]
CPSA_SKELETON_ONLY_KEYWORDS: Set[str] = set(get_args(CPSASkeletonOnlyKeyword))

# Complete set of authorized keywords inside a (defskeleton ...) form
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
    "conf",
    "auth",
    "gen-st",
    "precedes",
    "leadsto",
    "priority",
    "facts",
    "goal",
    "goals",
    "comment",
]
CPSA_SKELETON_KEYWORDS: Set[str] = set(get_args(CPSASkeletonKeyword))


# =============================================================================
# STAGE 4: Trace Event Actions & Annotations (Section 10.2, Table 10.1)
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
# STAGE 5: Message Term Operators (Tables 10.3 & 10.5)
# =============================================================================

# Basic Crypto Algebra Operators (Table 10.3)
CPSABasicOperator = Literal[
    "enc",     # (enc term+ key)             (arity >= 2; key is last arg)
    "hash",    # (hash term+)                (arity >= 1)
    "cat",     # (cat term+)                 (arity >= 1)
    "pubk",    # (pubk name) | (pubk str id) (arity 1 or 2)
    "privk",   # (privk name)| (privk str id)(arity 1 or 2)
    "invk",    # (invk akey_var)             (arity 1)
    "ltk",     # (ltk name1 name2)           (arity 2)
]
CPSA_BASIC_OPERATORS: Set[str] = set(get_args(CPSABasicOperator))

# Diffie-Hellman Crypto Algebra Operators (Table 10.5)
CPSADHOperator = Literal[
    "bltk",    # (bltk name1 name2)          (arity 2)
    "exp",     # (exp base expt)             (arity 2)
    "gen",     # (gen)                       (arity 0)
    "mul",     # (mul expt1 expt2 ...)       (arity >= 2)
    "rec",     # (rec expt)                  (arity 1)
    "one",     # (one)                       (arity 0)
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

# Key-constructing operators whose result is a basic value (akey or skey) allowed in roletran inputs
CPSA_KEY_CONSTRUCTOR_OPERATORS: Set[str] = {"pubk", "privk", "invk", "ltk", "bltk"}

# Structural keywords that must NEVER appear as operators inside a message term
CPSA_STRUCTURAL_NON_TERM_KEYWORDS: Set[str] = (
    CPSA_TOP_LEVEL_KEYWORDS
    | CPSA_ROLE_KEYWORDS
    | CPSA_SKELETON_KEYWORDS
    | CPSA_TRACE_ACTIONS
    | CPSA_TRACE_ANNOTATIONS
    | CPSA_ALGEBRAS
)


# =============================================================================
# STAGE 6: Operator Arity Constraints (Tables 10.3 & 10.5)
# =============================================================================
# Format: int (exact), set (one of allowed integers), tuple (min, max or None)
CPSA_OPERATOR_ARITY: Dict[str, Union[int, Set[int], Tuple[int, Optional[int]]]] = {
    "enc": (2, None),       # at least 1 payload + 1 encryption key (last argument)
    "hash": (1, None),      # at least 1 payload term
    "cat": (1, None),       # at least 1 component term
    "pubk": {1, 2},         # (pubk name_id) or (pubk tag_string name_id) per Table 10.3
    "privk": {1, 2},        # (privk name_id) or (privk tag_string name_id) per Table 10.3
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
# STAGE 7: JSON Schema Specification for Strongly-Typed Term AST
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
# STAGE 8: Canonical Desugaring Mappings (Frontend Compiler Normalizer)
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
        normalized_list = list(term)
        operator = normalized_list[0]
        if isinstance(operator, str) and operator in CPSA_DESUGAR_MAP:
            normalized_list[0] = CPSA_DESUGAR_MAP[operator]
        return [desugar_term_tree(subterm) for subterm in normalized_list]

    if isinstance(term, dict):
        # Extract atomic identifier name from dictionary variable representation
        for key in ("name", "variable", "identifier", "var", "id", "atom", "field", "val", "value"):
            if key in term and isinstance(term[key], str):
                return term[key]
        if "term" in term:
            return desugar_term_tree(term["term"])
        if "args" in term and isinstance(term.get("op"), str):
            return desugar_term_tree([term["op"]] + term["args"])
        for val in term.values():
            if isinstance(val, str):
                return val

    return term


def validate_cpsa_term_syntax(
    term: Any,
    algebra: CPSAMessageAlgebra = "basic",
    path: str = "term",
) -> None:
    """Statically validates that a term tree conforms strictly to MITRE CPSA 4.4.9 grammar.

    Enforces:
    1. Rejection of structural keywords (defrole, defskeleton, send, recv, vars, etc.) inside terms.
    2. Operator existence in the authorized CPSA 4.4.9 signature (Tables 10.3 & 10.5).
    3. Message algebra compatibility (forbidding DH operators under 'basic' algebra).
    4. Strict operator arity matching Tables 10.3 & 10.5.
    5. Inductive validation of all subterms.

    Raises:
        ValueError: If an unrecognized keyword, structural keyword leak, algebra incompatibility,
                    or arity defect is found.
    """
    if isinstance(term, (str, int)):
        return

    if isinstance(term, list):
        if not term:
            raise ValueError(f"Empty term expression at '{path}'. Expected atom or operator form.")

        operator = term[0]
        if not isinstance(operator, str):
            raise ValueError(
                f"First element of expression at '{path}' must be an operator string, got {type(operator).__name__}."
            )

        # 1. Check for misplaced structural CPSA keywords inside message terms
        if operator in CPSA_STRUCTURAL_NON_TERM_KEYWORDS and operator not in CPSA_ALL_OPERATORS:
            raise ValueError(
                f"Structural CPSA keyword '{operator}' at '{path}' cannot be used as a message term operator. "
                f"Valid CPSA 4.4.9 term operators: {sorted(list(CPSA_ALL_OPERATORS))}"
            )

        # 2. Operator Keyword Authorization
        if operator not in CPSA_ALL_OPERATORS:
            raise ValueError(
                f"Unknown operator keyword '{operator}' at '{path}'. "
                f"Valid CPSA 4.4.9 operators: {sorted(list(CPSA_ALL_OPERATORS))}"
            )

        # 3. Algebra Compatibility Check
        if algebra == "basic" and operator in CPSA_DH_OPERATORS:
            raise ValueError(
                f"Diffie-Hellman operator '{operator}' at '{path}' is forbidden under 'basic' message algebra. "
                "Change protocol message_algebra to 'diffie-hellman' to use exponentiation/DH features."
            )

        # 4. Arity Validation
        arguments = term[1:]
        arity = len(arguments)
        expected_arity = CPSA_OPERATOR_ARITY.get(operator)

        if isinstance(expected_arity, int):
            if arity != expected_arity:
                raise ValueError(
                    f"Operator '{operator}' at '{path}' expects exactly {expected_arity} arguments, got {arity}: {term}"
                )
        elif isinstance(expected_arity, set):
            if arity not in expected_arity:
                raise ValueError(
                    f"Operator '{operator}' at '{path}' expects arity in {sorted(list(expected_arity))}, got {arity}: {term}"
                )
        elif isinstance(expected_arity, tuple):
            min_args, max_args = expected_arity
            if arity < min_args:
                raise ValueError(
                    f"Operator '{operator}' at '{path}' expects at least {min_args} arguments, got {arity}: {term}"
                )
            if max_args is not None and arity > max_args:
                raise ValueError(
                    f"Operator '{operator}' at '{path}' expects at most {max_args} arguments, got {arity}: {term}"
                )

        # 5. Inductive Recursive Subterm Validation
        for idx, subterm in enumerate(arguments, 1):
            validate_cpsa_term_syntax(subterm, algebra=algebra, path=f"{path}[{idx}]")
    else:
        raise ValueError(
            f"Invalid term node at '{path}'. Expected string atom, integer, or nested operator list, got {type(term).__name__}."
        )
