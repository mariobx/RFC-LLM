"""Protocol Syntax Tree and CPSA Intermediate Representation (IR)."""

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field

from src.intermediate_representation.algebraic_sorts import CPSASortEnum


class CPSAVariableDeclaration(BaseModel):
    """Declaration of a typed variable in a role or skeleton."""
    name: str = Field(..., description="Alphanumeric variable identifier")
    sort: CPSASortEnum = Field(..., description="Declared CPSA message algebra sort")

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

        trace_form = ["trace"] + [event.to_cpsa_json() for event in self.trace]

        role_form: List[Any] = ["defrole", self.role_name, vars_form, trace_form]

        if self.unique_originating:
            role_form.append(["uniq-orig"] + self.unique_originating)
        if self.unique_generated:
            role_form.append(["uniq-gen"] + self.unique_generated)
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

        # Procedural roletran annotations
        if self.inputs:
            role_form.append(["inputs"] + self.inputs)
        if self.outputs:
            role_form.append(["outputs"] + self.outputs)

        if self.comment:
            role_form.append(["comment", f'"{self.comment}"'])

        return role_form


class CPSAStrandInstance(BaseModel):
    """Instantiation of a role strand within a preskeleton."""
    role_name: str = Field(..., description="Name of the instantiated role")
    trace_length: int = Field(..., description="Number of executed trace steps (1 to trace height)")
    variable_bindings: Dict[str, Union[str, List[Any]]] = Field(
        default_factory=dict,
        description="Mapping from role variable identifier to instantiated skeleton term",
    )

    def to_cpsa_json(self) -> List[Any]:
        strand_form: List[Any] = ["defstrand", self.role_name, self.trace_length]
        for role_var, term_val in self.variable_bindings.items():
            strand_form.append([role_var, term_val])
        return strand_form


class CPSAPreskeleton(BaseModel):
    """Point-of-view preskeleton to be formally analyzed by CPSA."""
    protocol_name: str = Field(..., description="Target protocol identifier matching a declared defprotocol")
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
        skel_form: List[Any] = ["defskeleton", self.protocol_name]

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

        if self.herald_comment:
            payload.append(["herald", f'"{self.herald_comment}"'])

        prot_form: List[Any] = ["defprotocol", self.protocol_name, self.message_algebra]
        for role in self.roles:
            prot_form.append(role.to_cpsa_json())
        payload.append(prot_form)

        for skel in self.skeletons:
            payload.append(skel.to_cpsa_json())

        return payload
