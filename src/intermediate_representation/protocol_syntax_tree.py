"""Strongly-Typed Intermediate Representation (AST) for MITRE CPSA 4.4.9 Protocols.

Enforces strict syntactic, algebraic, and positional keyword scoping across all
CPSA 4.4.9 constructs (Tables 10.1 – 10.6, Equation 10.1, and CPSA4 Roletran).
"""

import re
from typing import Annotated, Any, Dict, List, Optional, Set, Union
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    Field,
    WithJsonSchema,
    field_validator,
    model_validator,
)

from src.intermediate_representation.algebraic_sorts import (
    CPSA_ALL_VARIABLE_SORTS,
    CPSA_DH_ONLY_VARIABLE_SORTS,
    CPSA_LOGIC_ONLY_SORTS,
    CPSASortEnum,
)
from src.intermediate_representation.cpsa_grammar import (
    CPSA_ALL_OPERATORS,
    CPSA_KEY_CONSTRUCTOR_OPERATORS,
    CPSA_ROLE_ONLY_KEYWORDS,
    CPSA_SKELETON_ONLY_KEYWORDS,
    CPSA_TERM_JSON_SCHEMA,
    CPSAMessageAlgebra,
    CPSATraceAction,
    desugar_term_tree,
    validate_cpsa_term_syntax,
)


def _validate_cpsa_term(value: Any) -> Any:
    validate_cpsa_term_syntax(value, algebra="diffie-hellman")
    return value


# Strongly-typed CPSA term AST: enforces canonical syntax, algebra compatibility,
# and operator arity while providing an explicit enum/grammar JSON schema to LLMs.
CPSATerm = Annotated[
    Union[str, int, List[Any]],
    BeforeValidator(desugar_term_tree),
    AfterValidator(_validate_cpsa_term),
    WithJsonSchema(CPSA_TERM_JSON_SCHEMA),
]


# Forbidden misplaced keys per Pydantic model scope (Tables 10.1 & 10.6)
_FORBIDDEN_IN_ROLE: Set[str] = CPSA_SKELETON_ONLY_KEYWORDS | {"strands", "listeners"}
_FORBIDDEN_IN_SKELETON: Set[str] = CPSA_ROLE_ONLY_KEYWORDS | {"role_name"}
_FORBIDDEN_IN_EVENT: Set[str] = (
    CPSA_ROLE_ONLY_KEYWORDS
    | CPSA_SKELETON_ONLY_KEYWORDS
    | {"vars", "variables", "strands", "listeners", "unique_originating", "non_originating"}
) - {"trace"}
_FORBIDDEN_AT_TOP_LEVEL: Set[str] = (
    CPSA_ROLE_ONLY_KEYWORDS
    | CPSA_SKELETON_ONLY_KEYWORDS
    | {"strands", "listeners"}
) - {"defskeleton"}


def sanitize_cpsa_symbol(symbol: str) -> str:
    """Sanitizes an identifier to conform strictly to CPSA S-expression symbol grammar.

    CPSA allows alphanumeric characters and +-*/<=>!?$:%_&~^.
    Periods (.), spaces, and other punctuation are forbidden in unquoted atoms.
    """
    if not symbol:
        return "prot"
    sanitized = re.sub(r"[\.\s]+", "-", symbol)
    sanitized = re.sub(r"[^a-zA-Z0-9+\-*/<=>!?$:%_&~^]", "", sanitized)
    return sanitized.strip("-") or "prot"


def _quote_cpsa_tag_literal(val: str) -> str:
    """Formats an undeclared constant atom or number as a quoted CPSA 4.4.9 tag literal."""
    inner = val.strip()
    if len(inner) >= 2 and inner.startswith('"') and inner.endswith('"'):
        inner = inner[1:-1]
    inner = inner.replace("\\", "/").replace('"', "'")
    return f'"{inner}"'


def _is_quoted_tag_literal(term: Any) -> bool:
    """Returns True if `term` is a quoted CPSA string tag literal (`\"...\"`)."""
    return isinstance(term, str) and len(term) >= 2 and term.startswith('"') and term.endswith('"')


def _collect_implied_variable_sorts(
    term: Any,
    implied_sorts: Dict[str, str],
    akey_vars: Set[str],
    name_vars: Set[str],
) -> None:
    """Infers mandatory CPSA 4.4.9 variable sorts from operator positions (e.g. `ltk`/`pubk`/`privk` -> `name`)."""
    desugared = desugar_term_tree(term)
    if not isinstance(desugared, list) or not desugared:
        return
    op = desugared[0]
    if op in ("ltk", "bltk") and len(desugared) == 3:
        for arg in desugared[1:]:
            if isinstance(arg, str) and not _is_quoted_tag_literal(arg) and arg not in CPSA_ALL_OPERATORS:
                implied_sorts.setdefault(arg, CPSASortEnum.NAME.value)
    elif op in ("pubk", "privk"):
        if len(desugared) == 2:
            arg = desugared[1]
            if (
                isinstance(arg, str)
                and not _is_quoted_tag_literal(arg)
                and arg not in akey_vars
                and arg not in CPSA_ALL_OPERATORS
            ):
                implied_sorts.setdefault(arg, CPSASortEnum.NAME.value)
        elif len(desugared) == 3:
            a1, a2 = desugared[1], desugared[2]
            if isinstance(a1, str) and isinstance(a2, str):
                if a1 in name_vars and a2 not in name_vars:
                    pass
                elif not _is_quoted_tag_literal(a2) and a2 not in CPSA_ALL_OPERATORS:
                    implied_sorts.setdefault(a2, CPSASortEnum.NAME.value)
    elif op == "invk" and len(desugared) == 2:
        arg = desugared[1]
        if isinstance(arg, str) and not _is_quoted_tag_literal(arg) and arg not in CPSA_ALL_OPERATORS:
            implied_sorts.setdefault(arg, CPSASortEnum.AKEY.value)
    elif op == "enc" and len(desugared) >= 2:
        key_arg = desugared[-1]
        if isinstance(key_arg, str) and not _is_quoted_tag_literal(key_arg) and key_arg not in CPSA_ALL_OPERATORS:
            implied_sorts.setdefault(key_arg, CPSASortEnum.SKEY.value)

    for sub in desugared[1:]:
        _collect_implied_variable_sorts(sub, implied_sorts, akey_vars, name_vars)


def _invert_cpsa_key(key_term: Any, akey_vars: Set[str]) -> Any:
    """Returns the inverse key term required to decrypt/verify `(enc ... key_term)` in `cpsa4roletran`."""
    if isinstance(key_term, list) and key_term:
        op = key_term[0]
        if op == "pubk":
            return ["privk"] + key_term[1:]
        if op == "privk":
            return ["pubk"] + key_term[1:]
        if op == "invk" and len(key_term) == 2:
            return key_term[1]
        return key_term
    if isinstance(key_term, str) and key_term in akey_vars:
        return ["invk", key_term]
    return key_term


def extract_term_tokens(item: Any, token_set: Set[str]) -> None:
    """Recursively extracts all string tokens from an S-expression tree."""
    if isinstance(item, str):
        token_set.add(item)
    elif isinstance(item, (list, tuple)):
        for subitem in item:
            extract_term_tokens(subitem, token_set)
    elif isinstance(item, dict):
        for subitem in item.values():
            extract_term_tokens(subitem, token_set)


def normalize_cpsa_term(
    term: Any,
    akey_vars: Optional[Set[str]] = None,
    name_vars: Optional[Set[str]] = None,
    declared_vars: Optional[Set[str]] = None,
    quote_undeclared: bool = False,
) -> Any:
    """Recursively validates and normalizes message terms into valid CPSA 4.4.9 forms.

    Handles:
    1. Unwrapping (pubk k) -> k and (privk k) -> (invk k) when k has sort 'akey'.
    2. Repairing reversed 2-arg (pubk name tag) -> (pubk "tag" name) and quoting 2-arg tags per Table 10.3.
    3. Expanding bare 'gen' or 'one' in DH expressions to ['gen'] / ['one'] when not declared as variables.
    4. Auto-quoting undeclared constant atoms/numbers as CPSA string tag literals when `quote_undeclared=True`.
    """
    desugared = desugar_term_tree(term)
    if isinstance(desugared, list):
        if not desugared:
            return desugared
        normalized_list = list(desugared)
        operator = normalized_list[0]

        # 1. 1-argument pubk/privk applied to an 'akey' variable instead of 'name'
        if (
            akey_vars
            and len(normalized_list) == 2
            and isinstance(normalized_list[1], str)
            and (normalized_list[1] in akey_vars or sanitize_cpsa_symbol(normalized_list[1]) in akey_vars)
        ):
            clean_k = sanitize_cpsa_symbol(normalized_list[1]) if quote_undeclared else normalized_list[1]
            if operator == "pubk":
                return clean_k
            if operator == "privk":
                return ["invk", clean_k]

        # 2. 2-argument pubk/privk: Table 10.3 requires (pubk string_tag name_id)
        if (
            operator in ("pubk", "privk")
            and len(normalized_list) == 3
            and isinstance(normalized_list[1], str)
            and isinstance(normalized_list[2], str)
        ):
            first_arg, second_arg = normalized_list[1], normalized_list[2]
            if name_vars and (first_arg in name_vars or sanitize_cpsa_symbol(first_arg) in name_vars) and second_arg not in name_vars:
                tag_str = _quote_cpsa_tag_literal(second_arg)
                clean_name = sanitize_cpsa_symbol(first_arg) if quote_undeclared else first_arg
                return [operator, tag_str, clean_name]
            tag_str = _quote_cpsa_tag_literal(first_arg)
            clean_name = sanitize_cpsa_symbol(second_arg) if quote_undeclared else second_arg
            return [operator, tag_str, clean_name]

        # 3. Bare 'gen' or 'one' inside Diffie-Hellman operators (exp, mul, rec)
        if operator in ("exp", "mul", "rec"):
            for idx in range(1, len(normalized_list)):
                arg = normalized_list[idx]
                if arg == "gen" and (not declared_vars or "gen" not in declared_vars):
                    normalized_list[idx] = ["gen"]
                elif arg == "one" and (not declared_vars or "one" not in declared_vars):
                    normalized_list[idx] = ["one"]

        return [normalized_list[0]] + [
            normalize_cpsa_term(
                subterm,
                akey_vars=akey_vars,
                name_vars=name_vars,
                declared_vars=declared_vars,
                quote_undeclared=quote_undeclared,
            )
            for subterm in normalized_list[1:]
        ]

    if isinstance(desugared, str):
        if _is_quoted_tag_literal(desugared):
            return _quote_cpsa_tag_literal(desugared)
        if quote_undeclared and declared_vars is not None:
            clean_sym = sanitize_cpsa_symbol(desugared)
            if desugared in declared_vars or clean_sym in declared_vars:
                return clean_sym
            if desugared in ("gen", "one"):
                return desugared
            return _quote_cpsa_tag_literal(desugared)
    return desugared


def _validate_no_mesg_encryption_key(term: Any, mesg_vars: Set[str], path: str) -> None:
    """Enforces MITRE CPSA 4.4.9 Equation 10.1: encryption keys in (enc ...) cannot be variables of sort 'mesg'."""
    if not mesg_vars or not isinstance(term, list) or not term:
        return
    operator = term[0]
    if operator == "enc" and len(term) >= 2:
        key_term = term[-1]
        if isinstance(key_term, str) and key_term in mesg_vars:
            raise ValueError(
                f"Variable '{key_term}' of sort 'mesg' at '{path}' cannot be used as an encryption key in (enc ...) "
                "per MITRE CPSA 4.4.9 Equation 10.1 (sort 'mesg' lacks a well-defined key inverse). "
                "Declare the key with sort 'skey' or 'akey'."
            )
    for idx, subterm in enumerate(term[1:], 1):
        _validate_no_mesg_encryption_key(subterm, mesg_vars, f"{path}[{idx}]")


def _is_valid_roletran_input_term(term: Any) -> bool:
    """Checks whether a term is a basic value or channel allowed in cpsa4roletran (inputs ...)."""
    if isinstance(term, str):
        return True
    if isinstance(term, list) and term:
        op = term[0]
        if op in ("pubk", "privk", "invk"):
            return len(term) == 2
        if op in ("ltk", "bltk"):
            return len(term) == 3
    return False


class CPSAVariableDeclaration(BaseModel):
    """Declaration of a typed variable in a role or skeleton (Tables 10.2 & 10.4)."""

    name: str = Field(..., description="Semantic alphanumeric identifier (e.g. client_random, server_identity)")
    sort: CPSASortEnum = Field(..., description="Declared CPSA message algebra sort")
    description: Optional[str] = Field(
        default=None,
        description="Detailed explanation of what this variable represents in the RFC",
    )
    rfc_field: Optional[str] = Field(
        default=None,
        description="Exact RFC field name or section mapping (e.g. ClientHello.random)",
    )

    @field_validator("sort")
    @classmethod
    def validate_variable_sort_scope(cls, sort_val: CPSASortEnum) -> CPSASortEnum:
        """Forbids first-order logic sorts (strd, indx, fact) in role/skeleton (vars ...) declarations."""
        if sort_val.value in CPSA_LOGIC_ONLY_SORTS:
            raise ValueError(
                f"Sort '{sort_val.value}' is a first-order logic sort (Table 7.1) restricted to defrule/defgoal "
                f"quantifiers and is forbidden in role or skeleton (vars ...) declarations (Tables 10.2 & 10.4). "
                f"Valid variable sorts: {sorted(list(CPSA_ALL_VARIABLE_SORTS))}"
            )
        return sort_val

    def to_cpsa_json(self) -> List[str]:
        return [sanitize_cpsa_symbol(self.name), self.sort.value]


class CPSATraceEvent(BaseModel):
    """A directional communication or state event over an optional channel or location (Table 10.1)."""

    direction: CPSATraceAction = Field(..., description="Trace event action: send, recv, load, stor")
    channel: Optional[str] = Field(default="ch", description="Channel variable identifier for send/recv")
    location: Optional[str] = Field(default=None, description="Memory location variable for stateful load/stor events")
    message_term: CPSATerm = Field(
        ...,
        description="Term payload: atom string, integer, or nested operator tree conforming strictly to CPSA 4.4.9 grammar",
    )
    description: Optional[str] = Field(
        default=None,
        description="Semantic description of the message event (e.g. Client sends ClientHello)",
    )

    @model_validator(mode="before")
    @classmethod
    def forbid_non_event_keywords(cls, data: Any) -> Any:
        if isinstance(data, dict):
            misplaced = set(data.keys()) & _FORBIDDEN_IN_EVENT
            if misplaced:
                bad_key = sorted(list(misplaced))[0]
                raise ValueError(
                    f"Keyword '{bad_key}' is not allowed inside CPSATraceEvent (Table 10.1 event <- (dir term? term))."
                )
        return data

    def to_cpsa_json(self) -> List[Any]:
        # Per MITRE CPSA 4.4.9 Table 10.1: event <- (dir term? term)
        # load/stor take an optional location (locn) and a message_term (never both channel and location).
        if self.direction in ("load", "stor"):
            loc_var = self.location or (self.channel if self.channel and self.channel != "ch" else None)
            if loc_var:
                return [self.direction, sanitize_cpsa_symbol(loc_var), self.message_term]
            return [self.direction, self.message_term]

        if self.channel:
            return [self.direction, sanitize_cpsa_symbol(self.channel), self.message_term]
        return [self.direction, self.message_term]


class CPSAProtocolRole(BaseModel):
    """Specification of a principal's behavior in a protocol (defrole, Tables 10.1 & 10.6)."""

    role_name: str = Field(..., description="Identifier for the participant role")
    description: Optional[str] = Field(
        default=None,
        description="Detailed explanation of the principal's role in the protocol",
    )
    variables: List[CPSAVariableDeclaration] = Field(..., description="Variables declared within the role scope")
    trace: List[CPSATraceEvent] = Field(..., description="Ordered sequence of message events")
    inputs: List[CPSATerm] = Field(
        default_factory=list,
        description="Input parameters required for execution (channels, pre-shared keys, initial parameters)",
    )
    outputs: List[CPSATerm] = Field(
        default_factory=list,
        description="Return parameters yielded upon successful execution",
    )
    unique_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Terms originating uniquely in this role (uniq-orig)",
    )
    unique_generated: List[CPSATerm] = Field(
        default_factory=list,
        description="Terms generated uniquely in this role (uniq-gen)",
    )
    non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Keys assumed never compromised/originating in this role (non-orig)",
    )
    pen_non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Penetrator non-originating terms (pen-non-orig)",
    )
    confidential_channels: List[str] = Field(
        default_factory=list,
        description="Channels declared confidential (conf)",
    )
    authenticated_channels: List[str] = Field(
        default_factory=list,
        description="Channels declared authenticated (auth)",
    )
    gen_st: List[CPSATerm] = Field(
        default_factory=list,
        description="Stored state values with authenticity property (gen-st, Table 10.6)",
    )
    facts: List[List[Any]] = Field(
        default_factory=list,
        description="User-defined logical facts asserted by this role",
    )
    comment: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def forbid_skeleton_keywords_in_role(cls, data: Any) -> Any:
        if isinstance(data, dict):
            misplaced = set(data.keys()) & _FORBIDDEN_IN_ROLE
            if misplaced:
                bad_key = sorted(list(misplaced))[0]
                raise ValueError(
                    f"Keyword '{bad_key}' is a preskeleton-only keyword (MITRE CPSA 4.4.9 Tables 10.1 & 10.6) "
                    "and is strictly forbidden inside CPSAProtocolRole (defrole)."
                )
        return data

    @model_validator(mode="after")
    def validate_role_invariants(self) -> "CPSAProtocolRole":
        mesg_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.MESG}
        if mesg_vars:
            for idx, event in enumerate(self.trace):
                _validate_no_mesg_encryption_key(
                    event.message_term,
                    mesg_vars,
                    f"role[{self.role_name}].trace[{idx}]",
                )
        return self

    def get_sanitized_var_sorts(self) -> Dict[str, str]:
        """Returns the complete map of sanitized variable names to CPSA sort strings for this role,
        including variables implied by key constructors (`ltk`, `bltk`, `pubk`, `privk`, `invk`),
        channels (`chan`), and memory locations (`locn`).
        """
        akey_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.AKEY} | {
            sanitize_cpsa_symbol(var.name) for var in self.variables if var.sort == CPSASortEnum.AKEY
        }
        name_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.NAME} | {
            sanitize_cpsa_symbol(var.name) for var in self.variables if var.sort == CPSASortEnum.NAME
        }
        implied_sorts: Dict[str, str] = {}
        for event in self.trace:
            _collect_implied_variable_sorts(event.message_term, implied_sorts, akey_vars, name_vars)
        for term in (
            self.unique_originating
            + self.unique_generated
            + self.non_originating
            + self.pen_non_originating
            + self.inputs
            + self.outputs
            + self.gen_st
        ):
            _collect_implied_variable_sorts(term, implied_sorts, akey_vars, name_vars)
        for fact in self.facts:
            for ft in fact[1:] if isinstance(fact, list) and len(fact) > 1 else []:
                _collect_implied_variable_sorts(ft, implied_sorts, akey_vars, name_vars)

        var_sorts: Dict[str, str] = {}
        for var_decl in self.variables:
            clean_name = sanitize_cpsa_symbol(var_decl.name)
            if clean_name not in var_sorts:
                var_sorts[clean_name] = var_decl.sort.value

        for raw_name, sort_val in implied_sorts.items():
            clean_name = sanitize_cpsa_symbol(raw_name)
            if clean_name not in var_sorts:
                var_sorts[clean_name] = sort_val

        for event in self.trace:
            if event.direction in ("send", "recv") and event.channel:
                clean_chan = sanitize_cpsa_symbol(event.channel)
                var_sorts.setdefault(clean_chan, CPSASortEnum.CHAN.value)
            elif event.direction in ("load", "stor"):
                loc_var = event.location or (event.channel if event.channel and event.channel != "ch" else None)
                if loc_var:
                    clean_loc = sanitize_cpsa_symbol(loc_var)
                    var_sorts.setdefault(clean_loc, CPSASortEnum.LOCN.value)
        return var_sorts

    def to_cpsa_json(self) -> List[Any]:
        var_sorts_map = self.get_sanitized_var_sorts()
        akey_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.AKEY.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.AKEY
        }
        name_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.NAME.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.NAME
        }
        declared_vars = set(var_sorts_map.keys()) | {var.name for var in self.variables}

        # Normalize trace events and collect all channels and locations used in trace events
        normalized_events: List[List[Any]] = []
        used_channels: List[str] = []
        used_locations: List[str] = []
        for event in self.trace:
            event_sexpr = event.to_cpsa_json()
            if len(event_sexpr) >= 2:
                event_sexpr[-1] = normalize_cpsa_term(
                    event_sexpr[-1],
                    akey_vars=akey_vars,
                    name_vars=name_vars,
                    declared_vars=declared_vars,
                    quote_undeclared=True,
                )
            if event.direction in ("send", "recv") and event.channel:
                clean_chan = sanitize_cpsa_symbol(event.channel)
                if clean_chan not in used_channels:
                    used_channels.append(clean_chan)
            elif event.direction in ("load", "stor"):
                loc_var = event.location or (event.channel if event.channel and event.channel != "ch" else None)
                if loc_var:
                    clean_loc = sanitize_cpsa_symbol(loc_var)
                    if clean_loc not in used_locations:
                        used_locations.append(clean_loc)
            normalized_events.append(event_sexpr)

        trace_form = ["trace"] + normalized_events

        trace_tokens: Set[str] = set()
        extract_term_tokens(trace_form, trace_tokens)
        reserved_operators = {
            "pubk", "privk", "invk", "ltk", "cat", "enc", "hash", "trace", "send", "recv", "load", "stor"
        } | CPSA_ALL_OPERATORS

        # Group declared variables by sort, keeping all declared variables and any implied variables that occur in trace
        sort_to_vars: Dict[str, List[str]] = {}
        declared_sanitized: Set[str] = set()
        explicit_sanitized = {sanitize_cpsa_symbol(v.name) for v in self.variables}
        for clean_var_name, sort_val in var_sorts_map.items():
            if clean_var_name not in explicit_sanitized and clean_var_name not in trace_tokens:
                continue
            if clean_var_name not in declared_sanitized:
                declared_sanitized.add(clean_var_name)
                sort_to_vars.setdefault(sort_val, []).append(clean_var_name)

        vars_form: List[Any] = ["vars"]
        for sort_value, var_names in sort_to_vars.items():
            vars_form.append(var_names + [sort_value])

        def _term_vars_in_trace(term: Any) -> bool:
            if _is_quoted_tag_literal(term):
                return False
            if isinstance(term, str):
                return term in trace_tokens and term in declared_sanitized
            if isinstance(term, (list, tuple)):
                term_tokens: Set[str] = set()
                extract_term_tokens(term, term_tokens)
                var_tokens = {
                    t for t in (term_tokens - reserved_operators) if not _is_quoted_tag_literal(t)
                }
                return bool(var_tokens and var_tokens.issubset(trace_tokens) and var_tokens.issubset(declared_sanitized))
            return False

        role_form: List[Any] = ["defrole", sanitize_cpsa_symbol(self.role_name), vars_form, trace_form]

        # Enforce Section 4.2 & Table 10.6: rndx/expt variables must be in uniq-gen, never uniq-orig
        dh_exponent_vars = {k for k, v in var_sorts_map.items() if v in ("rndx", "expt")}
        effective_uniq_orig: List[Any] = []
        effective_uniq_gen: List[Any] = [
            normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True)
            for t in self.unique_generated
        ]
        for raw_term in self.unique_originating:
            term = normalize_cpsa_term(
                raw_term, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
            )
            if isinstance(term, str) and term in dh_exponent_vars:
                if term not in effective_uniq_gen:
                    effective_uniq_gen.append(term)
            else:
                effective_uniq_orig.append(term)

        valid_uniq_orig = [term for term in effective_uniq_orig if _term_vars_in_trace(term)]
        if valid_uniq_orig:
            role_form.append(["uniq-orig"] + valid_uniq_orig)

        valid_uniq_gen = [term for term in effective_uniq_gen if _term_vars_in_trace(term)]
        if valid_uniq_gen:
            role_form.append(["uniq-gen"] + valid_uniq_gen)

        normalized_non_orig = [
            normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True)
            for t in self.non_originating
        ]
        valid_non_orig = [t for t in normalized_non_orig if _term_vars_in_trace(t)]
        if valid_non_orig:
            role_form.append(["non-orig"] + valid_non_orig)

        normalized_pen_non_orig = [
            normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True)
            for t in self.pen_non_originating
        ]
        valid_pen_non_orig = [t for t in normalized_pen_non_orig if _term_vars_in_trace(t)]
        if valid_pen_non_orig:
            role_form.append(["pen-non-orig"] + valid_pen_non_orig)

        if self.confidential_channels:
            role_form.append(["conf"] + [sanitize_cpsa_symbol(c) for c in self.confidential_channels])
        if self.authenticated_channels:
            role_form.append(["auth"] + [sanitize_cpsa_symbol(c) for c in self.authenticated_channels])
        if self.gen_st:
            valid_gen_st = [
                normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True)
                for t in self.gen_st
            ]
            valid_gen_st = [t for t in valid_gen_st if _term_vars_in_trace(t)]
            if valid_gen_st:
                role_form.append(["gen-st"] + valid_gen_st)
        if self.facts:
            role_form.append(["facts"] + self.facts)

        # Deterministic cpsa4roletran procedural inputs synthesis:
        # 1. Every input/output variable must occur in trace.
        # 2. All trace channels and locations must be included in inputs.
        # 3. No uniq-orig or uniq-gen value may appear in inputs (cpsa4roletran.md).
        # 4. Each input must be a basic value or channel/locn (no compound cat/enc/hash).
        # 5. Any variable or key constructor needed before being bound by recv/load must be in inputs.
        orig_set = {str(t) for t in (valid_uniq_orig + valid_uniq_gen)}
        non_orig_set = {str(t) for t in (valid_non_orig + valid_pen_non_orig)}

        valid_inputs: List[Any] = []
        known_vars: Set[str] = {
            t for t in (valid_uniq_orig + valid_uniq_gen) if isinstance(t, str)
        } | set(used_channels) | set(used_locations)

        for chan_name in used_channels:
            if chan_name not in valid_inputs:
                valid_inputs.append(chan_name)
        for loc_name in used_locations:
            if loc_name not in valid_inputs and loc_name not in orig_set:
                valid_inputs.append(loc_name)

        def _add_required_input(candidate: Any) -> None:
            if _is_quoted_tag_literal(candidate):
                return
            if str(candidate) in orig_set:
                return
            if not _is_valid_roletran_input_term(candidate):
                return
            if not _term_vars_in_trace(candidate):
                return
            if candidate not in valid_inputs:
                valid_inputs.append(candidate)
            if isinstance(candidate, str):
                known_vars.add(candidate)

        for input_term in self.inputs:
            normalized_input = normalize_cpsa_term(
                input_term,
                akey_vars=akey_vars,
                name_vars=name_vars,
                declared_vars=declared_vars,
                quote_undeclared=True,
            )
            _add_required_input(normalized_input)

        def _require_buildable(term: Any) -> None:
            if isinstance(term, str):
                if not _is_quoted_tag_literal(term) and term in declared_sanitized and term not in known_vars:
                    _add_required_input(term)
            elif isinstance(term, list) and term:
                op = term[0]
                if op in CPSA_KEY_CONSTRUCTOR_OPERATORS:
                    _add_required_input(term)
                else:
                    for sub in term[1:]:
                        _require_buildable(sub)

        def _process_recv_term(term: Any) -> None:
            if isinstance(term, str):
                if not _is_quoted_tag_literal(term) and term in declared_sanitized:
                    known_vars.add(term)
            elif isinstance(term, list) and term:
                op = term[0]
                if op == "cat":
                    for sub in term[1:]:
                        _process_recv_term(sub)
                elif op == "enc" and len(term) >= 2:
                    key_term = term[-1]
                    dec_key = _invert_cpsa_key(key_term, akey_vars)
                    payload_tokens: Set[str] = set()
                    for p in term[1:-1]:
                        extract_term_tokens(p, payload_tokens)
                    payload_vars = {
                        t
                        for t in (payload_tokens - reserved_operators)
                        if not _is_quoted_tag_literal(t) and t in declared_sanitized
                    }
                    has_unbound_payload = bool(payload_vars - known_vars)
                    if _is_valid_roletran_input_term(dec_key):
                        is_unprovided_invk = isinstance(dec_key, list) and dec_key and dec_key[0] == "invk"
                        is_peer_secret_key = (
                            isinstance(dec_key, list)
                            and dec_key
                            and dec_key[0] in ("privk", "invk")
                            and str(dec_key) in non_orig_set
                            and not has_unbound_payload
                        )
                        if not is_peer_secret_key and not is_unprovided_invk:
                            if isinstance(dec_key, str):
                                if dec_key not in known_vars:
                                    _add_required_input(dec_key)
                            else:
                                _add_required_input(dec_key)
                    else:
                        _require_buildable(dec_key)
                    for p in term[1:-1]:
                        _process_recv_term(p)
                elif op in CPSA_KEY_CONSTRUCTOR_OPERATORS:
                    _add_required_input(term)
                else:
                    for sub in term[1:]:
                        _require_buildable(sub)

        for event_sexpr in normalized_events:
            if len(event_sexpr) < 2:
                continue
            ev_dir = event_sexpr[0]
            ev_msg = event_sexpr[-1]
            if ev_dir in ("send", "stor"):
                _require_buildable(ev_msg)
            elif ev_dir in ("recv", "load"):
                _process_recv_term(ev_msg)

        if valid_inputs:
            role_form.append(["inputs"] + valid_inputs)

        input_set = {str(t) for t in valid_inputs}
        if self.outputs:
            valid_outputs: List[Any] = []
            for output_term in self.outputs:
                normalized_output = normalize_cpsa_term(
                    output_term,
                    akey_vars=akey_vars,
                    name_vars=name_vars,
                    declared_vars=declared_vars,
                    quote_undeclared=True,
                )
                if str(normalized_output) in input_set:
                    continue
                if not _term_vars_in_trace(normalized_output):
                    continue
                if normalized_output not in valid_outputs:
                    valid_outputs.append(normalized_output)
            if valid_outputs:
                role_form.append(["outputs"] + valid_outputs)

        if self.comment:
            role_form.append(["comment", f'"{self.comment}"'])

        return role_form


class CPSAStrandInstance(BaseModel):
    """Instantiation of a role strand within a preskeleton (defstrandmax, Table 10.1)."""

    role_name: str = Field(..., description="Name of the instantiated role")
    trace_length: Optional[int] = Field(
        default=None,
        description="Trace height (optional; defstrandmax is always used to evaluate full strand)",
    )
    variable_bindings: Dict[str, CPSATerm] = Field(
        default_factory=dict,
        description="Mapping from role variable identifier to instantiated skeleton term conforming to CPSA grammar",
    )

    def to_cpsa_json(
        self,
        akey_vars: Optional[Set[str]] = None,
        name_vars: Optional[Set[str]] = None,
        declared_vars: Optional[Set[str]] = None,
        valid_role_vars: Optional[Set[str]] = None,
        auto_bind_vars: Optional[Set[str]] = None,
    ) -> List[Any]:
        strand_form: List[Any] = ["defstrandmax", sanitize_cpsa_symbol(self.role_name)]
        bound_role_vars: Set[str] = set()
        for role_var, term_val in self.variable_bindings.items():
            clean_role_var = sanitize_cpsa_symbol(role_var)
            if valid_role_vars is not None and clean_role_var not in valid_role_vars:
                continue
            norm_val = normalize_cpsa_term(
                term_val,
                akey_vars=akey_vars,
                name_vars=name_vars,
                declared_vars=declared_vars,
                quote_undeclared=declared_vars is not None,
            )
            strand_form.append([clean_role_var, norm_val])
            bound_role_vars.add(clean_role_var)

        if valid_role_vars and auto_bind_vars:
            for extra_var in sorted(valid_role_vars & auto_bind_vars):
                if extra_var not in bound_role_vars:
                    strand_form.append([extra_var, extra_var])
                    bound_role_vars.add(extra_var)

        return strand_form


class CPSAPreskeleton(BaseModel):
    """Point-of-view preskeleton to be formally analyzed by CPSA (defskeleton, Tables 10.1 & 10.6)."""

    protocol_name: str = Field(..., description="Target protocol identifier matching a declared defprotocol")
    description: Optional[str] = Field(
        default=None,
        description="Formal security objective or point-of-view scenario being verified",
    )
    variables: List[CPSAVariableDeclaration] = Field(
        default_factory=list,
        description="Variables appearing across strands in the skeleton",
    )
    strands: List[CPSAStrandInstance] = Field(..., description="Role strands active in this execution scenario")
    non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Keys or secrets assumed never compromised/originating (non-orig)",
    )
    pen_non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Penetrator non-originating terms (pen-non-orig)",
    )
    unique_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Nonces or secrets assumed fresh and unique across strands (uniq-orig)",
    )
    unique_generated: List[CPSATerm] = Field(
        default_factory=list,
        description="Uniquely generated terms (uniq-gen)",
    )
    listeners: List[CPSATerm] = Field(
        default_factory=list,
        description="Terms to verify secrecy for via listener strands (deflistener)",
    )
    precedes: List[List[List[int]]] = Field(
        default_factory=list,
        description="Causal message ordering constraints between node pairs: [((s1, n1), (s2, n2))]",
    )
    leadsto: List[List[List[int]]] = Field(
        default_factory=list,
        description="State synchronization ordering constraints between node pairs: [((s1, n1), (s2, n2))]",
    )
    priority: List[List[Any]] = Field(
        default_factory=list,
        description="Solver priority overrides for specific nodes: [((s, n), int_priority)]",
    )
    facts: List[List[Any]] = Field(
        default_factory=list,
        description="Logical facts asserted in this skeleton",
    )
    comment: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def forbid_role_keywords_in_skeleton(cls, data: Any) -> Any:
        if isinstance(data, dict):
            misplaced = set(data.keys()) & _FORBIDDEN_IN_SKELETON
            if misplaced:
                bad_key = sorted(list(misplaced))[0]
                raise ValueError(
                    f"Keyword '{bad_key}' is a role-only keyword (MITRE CPSA 4.4.9 Tables 10.1 & 10.6) "
                    "and is strictly forbidden inside CPSAPreskeleton (defskeleton)."
                )
        return data

    @model_validator(mode="after")
    def validate_skeleton_invariants(self) -> "CPSAPreskeleton":
        mesg_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.MESG}
        if mesg_vars:
            for listener in self.listeners:
                _validate_no_mesg_encryption_key(
                    listener,
                    mesg_vars,
                    f"skeleton[{self.protocol_name}].listeners",
                )
        return self

    def to_cpsa_json(
        self,
        role_var_sorts_by_role: Optional[Dict[str, Dict[str, str]]] = None,
    ) -> List[Any]:
        skel_form: List[Any] = ["defskeleton", sanitize_cpsa_symbol(self.protocol_name)]

        var_sorts_map: Dict[str, str] = {}
        for var_decl in self.variables:
            clean_var_name = sanitize_cpsa_symbol(var_decl.name)
            if clean_var_name not in var_sorts_map:
                var_sorts_map[clean_var_name] = var_decl.sort.value

        # Infer sorts from strand variable bindings if role_var_sorts_by_role is provided
        if role_var_sorts_by_role:
            for strand in self.strands:
                clean_role = sanitize_cpsa_symbol(strand.role_name)
                role_sorts = role_var_sorts_by_role.get(clean_role, {})
                for role_var, bound_val in strand.variable_bindings.items():
                    clean_rv = sanitize_cpsa_symbol(role_var)
                    rv_sort = role_sorts.get(clean_rv)
                    if rv_sort and isinstance(bound_val, str) and not _is_quoted_tag_literal(bound_val):
                        clean_bv = sanitize_cpsa_symbol(bound_val)
                        var_sorts_map.setdefault(clean_bv, rv_sort)

        akey_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.AKEY.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.AKEY
        }
        name_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.NAME.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.NAME
        }

        implied_sorts: Dict[str, str] = {}
        for strand in self.strands:
            for bound_val in strand.variable_bindings.values():
                _collect_implied_variable_sorts(bound_val, implied_sorts, akey_vars, name_vars)
        for term in (
            self.listeners
            + self.non_originating
            + self.pen_non_originating
            + self.unique_originating
            + self.unique_generated
        ):
            _collect_implied_variable_sorts(term, implied_sorts, akey_vars, name_vars)
        for fact in self.facts:
            for ft in fact[1:] if isinstance(fact, list) and len(fact) > 1 else []:
                _collect_implied_variable_sorts(ft, implied_sorts, akey_vars, name_vars)

        for raw_name, sort_val in implied_sorts.items():
            clean_name = sanitize_cpsa_symbol(raw_name)
            var_sorts_map.setdefault(clean_name, sort_val)

        akey_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.AKEY.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.AKEY
        }
        name_vars = {k for k, v in var_sorts_map.items() if v == CPSASortEnum.NAME.value} | {
            var.name for var in self.variables if var.sort == CPSASortEnum.NAME
        }
        declared_vars = set(var_sorts_map.keys()) | {var.name for var in self.variables}

        if var_sorts_map:
            sort_to_vars: Dict[str, List[str]] = {}
            for clean_var_name, sort_val in var_sorts_map.items():
                sort_to_vars.setdefault(sort_val, []).append(clean_var_name)
            vars_form: List[Any] = ["vars"]
            for sort_value, var_names in sort_to_vars.items():
                vars_form.append(var_names + [sort_value])
            skel_form.append(vars_form)

        strand_forms: List[List[Any]] = []
        skel_trace_tokens: Set[str] = set()
        for strand in self.strands:
            clean_role = sanitize_cpsa_symbol(strand.role_name)
            valid_role_vars = (
                set(role_var_sorts_by_role[clean_role].keys())
                if role_var_sorts_by_role and clean_role in role_var_sorts_by_role
                else None
            )
            s_form = strand.to_cpsa_json(
                akey_vars=akey_vars,
                name_vars=name_vars,
                declared_vars=declared_vars,
                valid_role_vars=valid_role_vars,
                auto_bind_vars=set(var_sorts_map.keys()) if valid_role_vars is not None else None,
            )
            strand_forms.append(s_form)
            for maplet in s_form[2:]:
                if isinstance(maplet, list) and len(maplet) == 2:
                    extract_term_tokens(maplet[1], skel_trace_tokens)

        skel_form.extend(strand_forms)

        for listener in self.listeners:
            norm_listener = normalize_cpsa_term(
                listener, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
            )
            extract_term_tokens(norm_listener, skel_trace_tokens)
            skel_form.append(["deflistener", norm_listener])

        reserved_operators = {
            "pubk", "privk", "invk", "ltk", "cat", "enc", "hash", "trace", "send", "recv", "load", "stor"
        } | CPSA_ALL_OPERATORS

        def _skel_term_in_trace(term: Any) -> bool:
            if _is_quoted_tag_literal(term):
                return False
            if not skel_trace_tokens:
                return True
            if isinstance(term, str):
                return term in skel_trace_tokens
            if isinstance(term, (list, tuple)):
                toks: Set[str] = set()
                extract_term_tokens(term, toks)
                var_toks = {t for t in (toks - reserved_operators) if not _is_quoted_tag_literal(t)}
                return bool(var_toks and var_toks.issubset(skel_trace_tokens))
            return False

        if self.non_originating:
            norm_non_orig = [
                normalize_cpsa_term(
                    t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
                )
                for t in self.non_originating
            ]
            norm_non_orig = [t for t in norm_non_orig if _skel_term_in_trace(t)]
            if norm_non_orig:
                skel_form.append(["non-orig"] + norm_non_orig)
        if self.pen_non_originating:
            norm_pen_non_orig = [
                normalize_cpsa_term(
                    t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
                )
                for t in self.pen_non_originating
            ]
            norm_pen_non_orig = [t for t in norm_pen_non_orig if _skel_term_in_trace(t)]
            if norm_pen_non_orig:
                skel_form.append(["pen-non-orig"] + norm_pen_non_orig)

        skel_dh_vars = {k for k, v in var_sorts_map.items() if v in ("rndx", "expt")}
        effective_skel_uniq_orig: List[Any] = []
        effective_skel_uniq_gen: List[Any] = [
            normalize_cpsa_term(
                t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
            )
            for t in self.unique_generated
        ]
        effective_skel_uniq_gen = [t for t in effective_skel_uniq_gen if _skel_term_in_trace(t)]
        for raw_term in self.unique_originating:
            term = normalize_cpsa_term(
                raw_term, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars, quote_undeclared=True
            )
            if not _skel_term_in_trace(term):
                continue
            if isinstance(term, str) and (
                term in skel_dh_vars
                or "exponent" in term.lower()
                or term.endswith("_dh")
                or term.endswith("_exp")
            ):
                if term not in effective_skel_uniq_gen:
                    effective_skel_uniq_gen.append(term)
            else:
                effective_skel_uniq_orig.append(term)

        if effective_skel_uniq_orig:
            skel_form.append(["uniq-orig"] + effective_skel_uniq_orig)
        if effective_skel_uniq_gen:
            skel_form.append(["uniq-gen"] + effective_skel_uniq_gen)
        if self.precedes:
            skel_form.append(["precedes"] + self.precedes)
        if self.leadsto:
            skel_form.append(["leadsto"] + self.leadsto)
        if self.priority:
            skel_form.append(["priority"] + self.priority)
        if self.facts:
            skel_form.append(["facts"] + self.facts)

        if self.comment:
            skel_form.append(["comment", f'"{self.comment}"'])

        return skel_form


class CPSAProtocolSpecification(BaseModel):
    """Complete protocol specification and verification suite (defprotocol + defskeletons, Table 10.1)."""

    protocol_name: str = Field(..., description="Unique protocol identifier")
    is_verifiable_protocol: bool = Field(
        default=True,
        description=(
            "True if the provided RFC excerpt specifies an interactive multi-message cryptographic or "
            "authenticated exchange that can be modeled in CPSA; False if this RFC is a false positive "
            "(e.g., no message flights, delegates key exchange to an external RFC, only defines packet/frame "
            "formats or local flags, or is a plaintext application protocol)."
        ),
    )
    ineligibility_reason: Optional[str] = Field(
        default=None,
        description="If is_verifiable_protocol is False, concise explanation of why the RFC excerpt cannot be modeled as an interactive cryptographic protocol.",
    )
    message_algebra: CPSAMessageAlgebra = Field(
        default="basic",
        description="CPSA message algebra selection: basic or diffie-hellman",
    )
    roles: List[CPSAProtocolRole] = Field(
        default_factory=list,
        description="Protocol participant role specifications (empty ONLY when is_verifiable_protocol is False)",
    )
    primary_secrecy_goals: List[CPSATerm] = Field(
        default_factory=list,
        description=(
            "Primary confidential terms (e.g. established session keys, premaster secrets, shared tokens) "
            "semantically identified by the LLM from the RFC whose confidentiality must be verified via listener strands."
        ),
    )
    skeletons: List[CPSAPreskeleton] = Field(
        default_factory=list,
        description="Analysis preskeletons / points of view",
    )
    herald_comment: Optional[str] = None
    herald_options: List[str] = Field(
        default_factory=list,
        description=(
            "Optional CPSA 4.4.9 search-order herald flags persisted when non-default search order "
            "resolves state-space snowballing (allowed: 'try-old-strands', 'check-nonces', 'reverse-nodes')."
        ),
    )

    def has_cryptographic_primitives(self) -> bool:
        """Returns True if the specification uses at least one CPSA cryptographic operator, key sort, or secure channel."""
        crypto_ops = {"enc", "hash", "ltk", "pubk", "privk", "invk", "bltk", "exp", "gen", "mul", "rec"}
        crypto_sorts = {"skey", "akey", "rndx", "expt", "base"}

        def _term_has_crypto(term: Any) -> bool:
            if isinstance(term, list) and term:
                if isinstance(term[0], str) and term[0] in crypto_ops:
                    return True
                return any(_term_has_crypto(sub) for sub in term[1:])
            return False

        for role in self.roles:
            if role.confidential_channels or role.authenticated_channels:
                return True
            if role.non_originating or role.pen_non_originating or role.unique_generated:
                return True
            for v in role.variables:
                if v.sort.value in crypto_sorts:
                    return True
            for ev in role.trace:
                if _term_has_crypto(ev.message_term):
                    return True
            for t in role.inputs + role.outputs + role.unique_originating:
                if _term_has_crypto(t):
                    return True
        for skel in self.skeletons:
            if skel.non_originating or skel.pen_non_originating or skel.unique_generated:
                return True
        return False

    @model_validator(mode="before")
    @classmethod
    def forbid_scoped_keywords_at_top_level(cls, data: Any) -> Any:
        if isinstance(data, dict):
            misplaced = set(data.keys()) & _FORBIDDEN_AT_TOP_LEVEL
            if misplaced:
                bad_key = sorted(list(misplaced))[0]
                raise ValueError(
                    f"Keyword '{bad_key}' is scoped to defrole or defskeleton (MITRE CPSA 4.4.9 Table 10.1) "
                    "and is forbidden directly on the top-level CPSAProtocolSpecification."
                )
        return data

    @model_validator(mode="after")
    def validate_algebra_consistency(self) -> "CPSAProtocolSpecification":
        """Ensures role traces are non-empty and Diffie-Hellman sorts/operators are forbidden under 'basic' algebra."""
        if not self.roles:
            self.is_verifiable_protocol = False
            if not self.ineligibility_reason:
                self.ineligibility_reason = (
                    self.herald_comment
                    or "No interactive cryptographic protocol roles could be extracted from the provided RFC slice."
                )
        else:
            for role in self.roles:
                if not role.trace:
                    raise ValueError(
                        f"Role '{role.role_name}' has an empty trace: []. Every CPSA defrole must contain at least "
                        "one send/recv trace event (or if this RFC does not specify a message exchange, set "
                        "is_verifiable_protocol=False and roles=[])."
                    )
        if self.message_algebra == "basic":
            for term in self.primary_secrecy_goals:
                validate_cpsa_term_syntax(
                    term,
                    algebra="basic",
                    path="primary_secrecy_goals",
                )
            for role in self.roles:
                for var_decl in role.variables:
                    if var_decl.sort.value in CPSA_DH_ONLY_VARIABLE_SORTS:
                        raise ValueError(
                            f"Diffie-Hellman variable sort '{var_decl.sort.value}' on variable '{var_decl.name}' "
                            f"in role '{role.role_name}' is forbidden under 'basic' message algebra (Table 10.2). "
                            "Change protocol message_algebra to 'diffie-hellman' or use a basic algebra sort."
                        )
                for event in role.trace:
                    validate_cpsa_term_syntax(
                        event.message_term,
                        algebra="basic",
                        path=f"role[{role.role_name}].trace",
                    )
                for term in (
                    role.inputs
                    + role.outputs
                    + role.non_originating
                    + role.pen_non_originating
                    + role.unique_originating
                    + role.unique_generated
                ):
                    validate_cpsa_term_syntax(
                        term,
                        algebra="basic",
                        path=f"role[{role.role_name}].declarations",
                    )
            for skel in self.skeletons:
                for var_decl in skel.variables:
                    if var_decl.sort.value in CPSA_DH_ONLY_VARIABLE_SORTS:
                        raise ValueError(
                            f"Diffie-Hellman variable sort '{var_decl.sort.value}' on variable '{var_decl.name}' "
                            f"in skeleton '{skel.protocol_name}' is forbidden under 'basic' message algebra (Table 10.2)."
                        )
                for strand in skel.strands:
                    for bound_var, bound_term in strand.variable_bindings.items():
                        validate_cpsa_term_syntax(
                            bound_term,
                            algebra="basic",
                            path=f"skeleton[{skel.protocol_name}].strand[{strand.role_name}].{bound_var}",
                        )
                for term in (
                    skel.listeners
                    + skel.non_originating
                    + skel.pen_non_originating
                    + skel.unique_originating
                    + skel.unique_generated
                ):
                    validate_cpsa_term_syntax(
                        term,
                        algebra="basic",
                        path=f"skeleton[{skel.protocol_name}].declarations",
                    )
        return self

    def to_cpsa_json_payload(self) -> List[List[Any]]:
        """Converts the specification into a sequence of top-level CPSA JSON forms."""
        payload: List[List[Any]] = []

        # Every SCM file MUST have a herald declaration as the first form per MITRE CPSA Table 10.1
        herald_text = self.herald_comment or f"{self.protocol_name} Protocol Verification Suite"
        herald_form: List[Any] = ["herald", f'"{herald_text}"']
        if self.message_algebra == "diffie-hellman":
            herald_form.append(["algebra", "diffie-hellman"])
        for opt in self.herald_options:
            if opt in {"try-old-strands", "check-nonces", "reverse-nodes"}:
                herald_form.append([opt])
        payload.append(herald_form)

        clean_proto_name = sanitize_cpsa_symbol(self.protocol_name)
        protocol_form: List[Any] = ["defprotocol", clean_proto_name, self.message_algebra]
        role_var_sorts_by_role: Dict[str, Dict[str, str]] = {}
        for role in self.roles:
            clean_role_name = sanitize_cpsa_symbol(role.role_name)
            role_var_sorts_by_role[clean_role_name] = role.get_sanitized_var_sorts()
            protocol_form.append(role.to_cpsa_json())
        payload.append(protocol_form)

        for skel in self.skeletons:
            payload.append(skel.to_cpsa_json(role_var_sorts_by_role=role_var_sorts_by_role))

        return payload
