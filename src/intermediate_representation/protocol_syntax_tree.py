import re
from typing import Any, Dict, List, Literal, Optional, Union, Set
from pydantic import BaseModel, Field

from src.intermediate_representation.algebraic_sorts import CPSASortEnum


def sanitize_cpsa_symbol(sym: str) -> str:
    """Sanitizes an identifier to conform strictly to CPSA S-expression symbol grammar.
    CPSA allows: alphanumeric and +-*/<=>!?$:%_&~^.
    Periods (.), spaces, and other punctuation are strictly forbidden in unquoted atoms.
    """
    if not sym:
        return "prot"
    s = re.sub(r'[\.\s]+', '-', sym)
    s = re.sub(r'[^a-zA-Z0-9+\-*/<=>!?$:%_&~^]', '', s)
    return s.strip('-') or "prot"


class CPSAVariableDeclaration(BaseModel):
    """Declaration of a typed variable in a role or skeleton."""
    name: str = Field(..., description="Semantic alphanumeric identifier (e.g. client_random, server_identity)")
    sort: CPSASortEnum = Field(..., description="Declared CPSA message algebra sort")
    description: Optional[str] = Field(default=None, description="Detailed explanation of what this variable represents in the RFC")
    rfc_field: Optional[str] = Field(default=None, description="Exact RFC field name or section mapping (e.g. ClientHello.random)")

    def to_cpsa_json(self) -> List[str]:
        return [self.name, self.sort.value]


class CPSATraceEvent(BaseModel):
    """A directional communication or state event over an optional channel."""
    direction: Literal["send", "recv", "load", "stor"] = Field(..., description="Trace event action")
    channel: Optional[str] = Field(default="ch", description="Channel variable identifier")
    location: Optional[str] = Field(default=None, description="Memory location variable for stateful load/stor events")
    message_term: Union[str, int, List[Any]] = Field(
        ...,
        description="Term payload: atom string, integer, or nested operator tree",
    )
    description: Optional[str] = Field(default=None, description="Semantic description of the message event (e.g. Client sends ClientHello)")

    def to_cpsa_json(self) -> List[Any]:
        if self.direction in ["load", "stor"]:
            event = [self.direction]
            if self.channel:
                event.append(self.channel)
            if self.location:
                event.append(self.location)
            event.append(self.message_term)
            return event

        if self.channel:
            return [self.direction, self.channel, self.message_term]
        return [self.direction, self.message_term]


class CPSAProtocolRole(BaseModel):
    """Specification of a principal's behavior in a protocol."""
    role_name: str = Field(..., description="Identifier for the participant role")
    description: Optional[str] = Field(default=None, description="Detailed explanation of the principal's role in the protocol")
    variables: List[CPSAVariableDeclaration] = Field(..., description="Variables declared within the role scope")
    trace: List[CPSATraceEvent] = Field(..., description="Ordered sequence of message events")
    inputs: List[Union[str, List[Any]]] = Field(
        default_factory=list,
        description="Input parameters required for execution (channels, pre-shared keys, initial parameters)",
    )
    outputs: List[Union[str, List[Any]]] = Field(
        default_factory=list,
        description="Return parameters yielded upon successful execution",
    )
    unique_originating: List[Union[str, List[Any]]] = Field(
        default_factory=list,
        description="Terms originating uniquely in this role (uniq-orig)",
    )
    unique_generated: List[Union[str, List[Any]]] = Field(
        default_factory=list,
        description="Terms generated uniquely in this role (uniq-gen)",
    )
    non_originating: List[Union[str, List[Any]]] = Field(
        default_factory=list,
        description="Keys assumed never compromised/originating in this role (non-orig)",
    )
    pen_non_originating: List[Union[str, List[Any]]] = Field(
        default_factory=list,
        description="Penetrator non-originating terms (pen-non-orig)",
    )
    role_originating: List[str] = Field(
        default_factory=list,
        description="Role-based unique origination assumptions (role_orig)",
    )
    confidential_channels: List[str] = Field(
        default_factory=list,
        description="Channels declared confidential (conf)",
    )
    authenticated_channels: List[str] = Field(
        default_factory=list,
        description="Channels declared authenticated (auth)",
    )
    facts: List[List[Any]] = Field(
        default_factory=list,
        description="User-defined logical facts asserted by this role",
    )
    comment: Optional[str] = None

    def to_cpsa_json(self) -> List[Any]:
        # Group variables by sort: ["vars", ["v1", "v2", "sort1"], ["v3", "sort2"]]
        sort_to_vars: Dict[str, List[str]] = {}
        for v in self.variables:
            sort_to_vars.setdefault(v.sort.value, []).append(v.name)

        vars_form = ["vars"]
        for sort_val, var_names in sort_to_vars.items():
            vars_form.append(var_names + [sort_val])

        akey_vars = {v.name for v in self.variables if v.sort.value == "akey"}

        def _normalize_term(term: Any) -> Any:
            if isinstance(term, list):
                if len(term) == 2 and term[0] == "pubk" and isinstance(term[1], str) and term[1] in akey_vars:
                    return term[1]
                if len(term) == 2 and term[0] == "privk" and isinstance(term[1], str) and term[1] in akey_vars:
                    return ["invk", term[1]]
                return [_normalize_term(x) for x in term]
            return term

        normalized_events = []
        for event in self.trace:
            evt_json = event.to_cpsa_json()
            if len(evt_json) >= 2:
                evt_json[-1] = _normalize_term(evt_json[-1])
            normalized_events.append(evt_json)

        trace_form = ["trace"] + normalized_events

        # Extract all tokens appearing in trace and channel annotations to satisfy roletran constraints
        def _extract_tokens(item: Any, out: Set[str]):
            if isinstance(item, str):
                out.add(item)
            elif isinstance(item, (list, tuple)):
                for x in item:
                    _extract_tokens(x, out)
            elif isinstance(item, dict):
                for x in item.values():
                    _extract_tokens(x, out)

        trace_tokens: Set[str] = set()
        _extract_tokens(trace_form, trace_tokens)
        reserved_ops = {"pubk", "privk", "invk", "ltk", "cat", "enc", "hash", "trace", "send", "recv"}

        role_form: List[Any] = ["defrole", sanitize_cpsa_symbol(self.role_name), vars_form, trace_form]

        if self.unique_originating:
            valid_uo = [v for v in self.unique_originating if v in trace_tokens]
            if valid_uo:
                role_form.append(["uniq-orig"] + valid_uo)
        if self.unique_generated:
            valid_ug = [v for v in self.unique_generated if v in trace_tokens]
            if valid_ug:
                role_form.append(["uniq-gen"] + valid_ug)
        if self.non_originating:
            role_form.append(["non-orig"] + self.non_originating)
        if self.pen_non_originating:
            role_form.append(["pen-non-orig"] + self.pen_non_originating)
        if self.role_originating:
            role_form.append(["role_orig"] + self.role_originating)
        if self.confidential_channels:
            role_form.append(["conf"] + self.confidential_channels)
        if self.authenticated_channels:
            role_form.append(["auth"] + self.authenticated_channels)
        if self.facts:
            role_form.append(["facts"] + self.facts)

        # Procedural roletran annotations: every input/output term must be tied to trace variables
        if self.inputs:
            valid_inputs = []
            for inp in self.inputs:
                inp_tokens: Set[str] = set()
                _extract_tokens(inp, inp_tokens)
                var_tokens = inp_tokens - reserved_ops
                if var_tokens and var_tokens.issubset(trace_tokens):
                    valid_inputs.append(_normalize_term(inp))
            if valid_inputs:
                role_form.append(["inputs"] + valid_inputs)

        if self.outputs:
            valid_outputs = []
            for out in self.outputs:
                out_tokens: Set[str] = set()
                _extract_tokens(out, out_tokens)
                var_tokens = out_tokens - reserved_ops
                if var_tokens and var_tokens.issubset(trace_tokens):
                    valid_outputs.append(_normalize_term(out))
            if valid_outputs:
                role_form.append(["outputs"] + valid_outputs)

        if self.comment:
            role_form.append(["comment", f'"{self.comment}"'])

        return role_form


class CPSAStrandInstance(BaseModel):
    """Instantiation of a role strand within a preskeleton."""
    role_name: str = Field(..., description="Name of the instantiated role")
    trace_length: Optional[int] = Field(
        default=None,
        description="Trace height (optional; defstrandmax is always used to evaluate full strand)",
    )
    variable_bindings: Dict[str, Union[str, List[Any]]] = Field(
        default_factory=dict,
        description="Mapping from role variable identifier to instantiated skeleton term",
    )

    def to_cpsa_json(self) -> List[Any]:
        strand_form: List[Any] = ["defstrandmax", sanitize_cpsa_symbol(self.role_name)]
        for role_var, term_val in self.variable_bindings.items():
            strand_form.append([sanitize_cpsa_symbol(role_var), term_val])
        return strand_form


class CPSAPreskeleton(BaseModel):
    """Point-of-view preskeleton to be formally analyzed by CPSA."""
    protocol_name: str = Field(..., description="Target protocol identifier matching a declared defprotocol")
    description: Optional[str] = Field(default=None, description="Formal security objective or point-of-view scenario being verified")
    variables: List[CPSAVariableDeclaration] = Field(
        default_factory=list,
        description="Variables appearing across strands in the skeleton",
    )
    strands: List[CPSAStrandInstance] = Field(..., description="Role strands active in this execution scenario")
    non_originating: List[Union[str, List[Any]]] = Field(
        default_factory=list,
        description="Keys or secrets assumed never compromised/originating (non-orig)",
    )
    pen_non_originating: List[Union[str, List[Any]]] = Field(
        default_factory=list,
        description="Penetrator non-originating terms (pen-non-orig)",
    )
    unique_originating: List[str] = Field(
        default_factory=list,
        description="Nonces or secrets assumed fresh and unique across strands (uniq-orig)",
    )
    unique_generated: List[str] = Field(
        default_factory=list,
        description="Uniquely generated terms (uniq-gen)",
    )
    listeners: List[Union[str, List[Any]]] = Field(
        default_factory=list,
        description="Terms to verify secrecy for via listener strands (deflistener)",
    )
    precedes: List[List[List[int]]] = Field(
        default_factory=list,
        description="Causal message ordering constraints between node pairs: [((s1, n1), (s2, n2))]",
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

    def to_cpsa_json(self) -> List[Any]:
        skel_form: List[Any] = ["defskeleton", sanitize_cpsa_symbol(self.protocol_name)]

        if self.variables:
            sort_to_vars: Dict[str, List[str]] = {}
            for v in self.variables:
                sort_to_vars.setdefault(v.sort.value, []).append(v.name)
            vars_form = ["vars"]
            for sort_val, var_names in sort_to_vars.items():
                vars_form.append(var_names + [sort_val])
            skel_form.append(vars_form)

        for strand in self.strands:
            skel_form.append(strand.to_cpsa_json())

        for listener in self.listeners:
            skel_form.append(["deflistener", listener])

        if self.non_originating:
            skel_form.append(["non-orig"] + self.non_originating)
        if self.pen_non_originating:
            skel_form.append(["pen-non-orig"] + self.pen_non_originating)
        if self.unique_originating:
            skel_form.append(["uniq-orig"] + self.unique_originating)
        if self.unique_generated:
            skel_form.append(["uniq-gen"] + self.unique_generated)
        if self.precedes:
            skel_form.append(["precedes"] + self.precedes)
        if self.priority:
            skel_form.append(["priority"] + self.priority)
        if self.facts:
            skel_form.append(["facts"] + self.facts)

        if self.comment:
            skel_form.append(["comment", f'"{self.comment}"'])

        return skel_form


class CPSAProtocolSpecification(BaseModel):
    """Complete protocol specification and verification suite."""
    protocol_name: str = Field(..., description="Unique protocol identifier")
    message_algebra: Literal["basic", "diffie-hellman"] = Field(
        default="basic",
        description="CPSA message algebra selection",
    )
    roles: List[CPSAProtocolRole] = Field(..., description="Protocol participant role specifications")
    skeletons: List[CPSAPreskeleton] = Field(
        default_factory=list,
        description="Analysis preskeletons / points of view",
    )
    herald_comment: Optional[str] = None

    def to_cpsa_json_payload(self) -> List[List[Any]]:
        """Converts the specification into a sequence of top-level CPSA JSON forms."""
        payload: List[List[Any]] = []

        # Every SCM file MUST have a herald declaration per MITRE CPSA manual
        herald_text = self.herald_comment or f"{self.protocol_name} Protocol Verification Suite"
        payload.append(["herald", f'"{herald_text}"'])

        clean_proto_name = sanitize_cpsa_symbol(self.protocol_name)
        prot_form: List[Any] = ["defprotocol", clean_proto_name, self.message_algebra]
        for role in self.roles:
            prot_form.append(role.to_cpsa_json())
        payload.append(prot_form)

        for skel in self.skeletons:
            payload.append(skel.to_cpsa_json())

        return payload
