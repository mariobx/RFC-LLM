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
) -> Any:
    """Recursively validates and normalizes message terms into valid CPSA 4.4.9 forms.

    Handles:
    1. Unwrapping (pubk k) -> k and (privk k) -> (invk k) when k has sort 'akey'.
    2. Repairing reversed 2-arg (pubk name tag) -> (pubk "tag" name) per Table 10.3.
    3. Expanding bare 'gen' or 'one' in DH expressions to ['gen'] / ['one'] when not declared as variables.
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
            and normalized_list[1] in akey_vars
        ):
            if operator == "pubk":
                return normalized_list[1]
            if operator == "privk":
                return ["invk", normalized_list[1]]

        # 2. 2-argument pubk/privk: Table 10.3 requires (pubk string_tag name_id)
        if (
            operator in ("pubk", "privk")
            and len(normalized_list) == 3
            and name_vars
            and isinstance(normalized_list[1], str)
            and isinstance(normalized_list[2], str)
        ):
            first_arg, second_arg = normalized_list[1], normalized_list[2]
            if first_arg in name_vars and second_arg not in name_vars:
                tag_str = second_arg if second_arg.startswith('"') else f'"{second_arg}"'
                normalized_list[1] = tag_str
                normalized_list[2] = first_arg

        # 3. Bare 'gen' or 'one' inside Diffie-Hellman operators (exp, mul, rec)
        if operator in ("exp", "mul", "rec"):
            for idx in range(1, len(normalized_list)):
                arg = normalized_list[idx]
                if arg == "gen" and (not declared_vars or "gen" not in declared_vars):
                    normalized_list[idx] = ["gen"]
                elif arg == "one" and (not declared_vars or "one" not in declared_vars):
                    normalized_list[idx] = ["one"]

        return [
            normalize_cpsa_term(subterm, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars)
            for subterm in normalized_list
        ]
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
        return term[0] in CPSA_KEY_CONSTRUCTOR_OPERATORS
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
    role_originating: List[str] = Field(
        default_factory=list,
        description="Deprecated legacy field; ignored on emission because role_orig is not a valid defrole input keyword in Table 10.6",
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

    def to_cpsa_json(self) -> List[Any]:
        akey_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.AKEY}
        name_vars = {var.name for var in self.variables if var.sort == CPSASortEnum.NAME}
        declared_vars = {var.name for var in self.variables}

        # Normalize trace events and collect all channels used in send/recv events
        normalized_events: List[List[Any]] = []
        used_channels: List[str] = []
        for event in self.trace:
            event_sexpr = event.to_cpsa_json()
            if len(event_sexpr) >= 2:
                event_sexpr[-1] = normalize_cpsa_term(
                    event_sexpr[-1],
                    akey_vars=akey_vars,
                    name_vars=name_vars,
                    declared_vars=declared_vars,
                )
            if event.direction in ("send", "recv") and event.channel:
                clean_chan = sanitize_cpsa_symbol(event.channel)
                if clean_chan not in used_channels:
                    used_channels.append(clean_chan)
            normalized_events.append(event_sexpr)

        trace_form = ["trace"] + normalized_events

        # Group declared variables by sort, ensuring any channel used in trace is declared as 'chan'
        sort_to_vars: Dict[str, List[str]] = {}
        declared_sanitized: Set[str] = set()
        for var_decl in self.variables:
            clean_var_name = sanitize_cpsa_symbol(var_decl.name)
            if clean_var_name not in declared_sanitized:
                declared_sanitized.add(clean_var_name)
                sort_to_vars.setdefault(var_decl.sort.value, []).append(clean_var_name)

        for chan_name in used_channels:
            if chan_name not in declared_sanitized:
                declared_sanitized.add(chan_name)
                sort_to_vars.setdefault(CPSASortEnum.CHAN.value, []).append(chan_name)

        vars_form: List[Any] = ["vars"]
        for sort_value, var_names in sort_to_vars.items():
            vars_form.append(var_names + [sort_value])

        trace_tokens: Set[str] = set()
        extract_term_tokens(trace_form, trace_tokens)
        reserved_operators = {"pubk", "privk", "invk", "ltk", "cat", "enc", "hash", "trace", "send", "recv", "load", "stor"} | CPSA_ALL_OPERATORS

        def _term_vars_in_trace(term: Any) -> bool:
            if isinstance(term, str):
                return term in trace_tokens
            if isinstance(term, (list, tuple)):
                term_tokens: Set[str] = set()
                extract_term_tokens(term, term_tokens)
                var_tokens = term_tokens - reserved_operators
                return bool(var_tokens and var_tokens.issubset(trace_tokens))
            return True

        role_form: List[Any] = ["defrole", sanitize_cpsa_symbol(self.role_name), vars_form, trace_form]

        # Enforce Section 4.2 & Table 10.6: rndx/expt variables must be in uniq-gen, never uniq-orig
        dh_exponent_vars = {var.name for var in self.variables if var.sort.value in ("rndx", "expt")}
        effective_uniq_orig: List[Any] = []
        effective_uniq_gen: List[Any] = list(self.unique_generated)
        for term in self.unique_originating:
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

        if self.non_originating:
            role_form.append(["non-orig"] + [
                normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars)
                for t in self.non_originating
            ])
        if self.pen_non_originating:
            role_form.append(["pen-non-orig"] + [
                normalize_cpsa_term(t, akey_vars=akey_vars, name_vars=name_vars, declared_vars=declared_vars)
                for t in self.pen_non_originating
            ])
        if self.confidential_channels:
            role_form.append(["conf"] + self.confidential_channels)
        if self.authenticated_channels:
            role_form.append(["auth"] + self.authenticated_channels)
        if self.gen_st:
            role_form.append(["gen-st"] + self.gen_st)
        if self.facts:
            role_form.append(["facts"] + self.facts)

        # Procedural cpsa4roletran annotations:
        # 1. Every input/output variable must occur in trace.
        # 2. All trace channels must be included in inputs.
        # 3. No uniq-orig or uniq-gen value may appear in inputs (cpsa4roletran.md).
        # 4. Each input must be a basic value or channel (no compound cat/enc/hash).
        # 5. No input value may appear in outputs (cpsa4roletran.md).
        orig_set = {str(t) for t in (valid_uniq_orig + valid_uniq_gen)}

        valid_inputs: List[Any] = []
        if self.inputs or self.outputs:
            for chan_name in used_channels:
                if chan_name not in valid_inputs:
                    valid_inputs.append(chan_name)

        for input_term in self.inputs:
            normalized_input = normalize_cpsa_term(
                input_term,
                akey_vars=akey_vars,
                name_vars=name_vars,
                declared_vars=declared_vars,
            )
            if str(normalized_input) in orig_set:
                continue
            if not _is_valid_roletran_input_term(normalized_input):
                continue
            input_tokens: Set[str] = set()
            extract_term_tokens(normalized_input, input_tokens)
            var_tokens = input_tokens - reserved_operators
            if var_tokens and var_tokens.issubset(trace_tokens) and normalized_input not in valid_inputs:
                valid_inputs.append(normalized_input)

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
                )
                if str(normalized_output) in input_set:
                    continue
                output_tokens: Set[str] = set()
                extract_term_tokens(normalized_output, output_tokens)
                var_tokens = output_tokens - reserved_operators
                if var_tokens and var_tokens.issubset(trace_tokens) and normalized_output not in valid_outputs:
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

    def to_cpsa_json(self) -> List[Any]:
        strand_form: List[Any] = ["defstrandmax", sanitize_cpsa_symbol(self.role_name)]
        for role_var, term_val in self.variable_bindings.items():
            strand_form.append([sanitize_cpsa_symbol(role_var), term_val])
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

    def to_cpsa_json(self) -> List[Any]:
        skel_form: List[Any] = ["defskeleton", sanitize_cpsa_symbol(self.protocol_name)]

        if self.variables:
            sort_to_vars: Dict[str, List[str]] = {}
            declared_sanitized: Set[str] = set()
            for var_decl in self.variables:
                clean_var_name = sanitize_cpsa_symbol(var_decl.name)
                if clean_var_name not in declared_sanitized:
                    declared_sanitized.add(clean_var_name)
                    sort_to_vars.setdefault(var_decl.sort.value, []).append(clean_var_name)
            vars_form: List[Any] = ["vars"]
            for sort_value, var_names in sort_to_vars.items():
                vars_form.append(var_names + [sort_value])
            skel_form.append(vars_form)

        for strand in self.strands:
            skel_form.append(strand.to_cpsa_json())

        for listener in self.listeners:
            skel_form.append(["deflistener", listener])

        if self.non_originating:
            skel_form.append(["non-orig"] + self.non_originating)
        if self.pen_non_originating:
            skel_form.append(["pen-non-orig"] + self.pen_non_originating)

        skel_dh_vars = {var.name for var in self.variables if var.sort.value in ("rndx", "expt")}
        effective_skel_uniq_orig: List[Any] = []
        effective_skel_uniq_gen: List[Any] = list(self.unique_generated)
        for term in self.unique_originating:
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
    message_algebra: CPSAMessageAlgebra = Field(
        default="basic",
        description="CPSA message algebra selection: basic or diffie-hellman",
    )
    roles: List[CPSAProtocolRole] = Field(..., description="Protocol participant role specifications")
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
        """Ensures Diffie-Hellman sorts and operators are strictly forbidden under 'basic' message algebra."""
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
        if self.message_algebra == "diffie-hellman":
            payload.append(["herald", f'"{herald_text}"', ["algebra", "diffie-hellman"]])
        else:
            payload.append(["herald", f'"{herald_text}"'])

        clean_proto_name = sanitize_cpsa_symbol(self.protocol_name)
        protocol_form: List[Any] = ["defprotocol", clean_proto_name, self.message_algebra]
        for role in self.roles:
            protocol_form.append(role.to_cpsa_json())
        payload.append(protocol_form)

        for skel in self.skeletons:
            payload.append(skel.to_cpsa_json())

        return payload
