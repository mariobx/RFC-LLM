"""Unit Tests for MITRE CPSA 4.4.9 Keyword/Sort Scoping and Externalized .prompts/ Loader."""

from pathlib import Path
import pytest

from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.cpsa_grammar import validate_cpsa_term_syntax
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAPreskeleton,
    CPSAProtocolRole,
    CPSAProtocolSpecification,
    CPSAStrandInstance,
    CPSATraceEvent,
    CPSAVariableDeclaration,
)
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    PROMPT_COMPILER_REPAIR,
    PROMPT_PROTOCOL_EXTRACTION,
    PROMPT_RAG_QUERY_FORMULATION,
    PROMPT_SCHEMA_SELF_CORRECTION,
    PROMPT_SECTION_ROUTER,
    build_schema_system_prompt,
    load_prompt,
)


def test_externalized_prompts_load_from_disk_and_fallback(tmp_path: Path):
    """Verify all 6 prompt templates in .prompts/ exist, load cleanly, and support fallback."""
    for prompt_filename in (
        PROMPT_APPLICABILITY_GATE,
        PROMPT_SECTION_ROUTER,
        PROMPT_PROTOCOL_EXTRACTION,
        PROMPT_SCHEMA_SELF_CORRECTION,
        PROMPT_RAG_QUERY_FORMULATION,
        PROMPT_COMPILER_REPAIR,
    ):
        text = load_prompt(prompt_filename)
        assert len(text) > 100

    # Verify schema attachment helper
    schema_prompt = build_schema_system_prompt(PROMPT_PROTOCOL_EXTRACTION, CPSAProtocolSpecification)
    assert "Respond strictly with a valid JSON object matching this schema:" in schema_prompt
    assert '"CPSAProtocolSpecification"' in schema_prompt

    # Verify fallback when directory has no files
    fallback_text = load_prompt(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert "MITRE CPSA 4.4.9" in fallback_text


def test_logic_only_sorts_forbidden_in_role_and_skeleton_vars():
    """Tables 10.2 & 10.4 vs Table 7.1: strd, indx, and fact are forbidden in role/skeleton vars."""
    for bad_sort in (CPSASortEnum.STRD, CPSASortEnum.INDX, CPSASortEnum.FACT):
        with pytest.raises(ValueError, match="first-order logic sort"):
            CPSAVariableDeclaration(name="node_idx", sort=bad_sort)


def test_diffie_hellman_sorts_forbidden_under_basic_algebra():
    """Table 10.2: rndx, expt, and base sorts are forbidden when protocol message_algebra is 'basic'."""
    with pytest.raises(ValueError, match="Diffie-Hellman variable sort 'rndx'"):
        CPSAProtocolSpecification(
            protocol_name="dh_sort_in_basic",
            message_algebra="basic",
            roles=[
                CPSAProtocolRole(
                    role_name="initiator",
                    variables=[
                        CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                        CPSAVariableDeclaration(name="x", sort=CPSASortEnum.RNDX),
                    ],
                    trace=[
                        CPSATraceEvent(direction="send", channel="ch", message_term="x"),
                    ],
                )
            ],
        )


def test_structural_keywords_forbidden_inside_message_terms():
    """Tables 10.1, 10.3, 10.5: structural keywords (defrole, send, vars, etc.) cannot be term operators."""
    for bad_kw in ("defrole", "defskeleton", "send", "recv", "vars", "trace", "uniq-orig", "deflistener"):
        with pytest.raises(ValueError, match=f"Structural CPSA keyword '{bad_kw}'"):
            validate_cpsa_term_syntax([bad_kw, "x"])


def test_role_and_skeleton_keyword_scoping_separation():
    """Tables 10.1 & 10.6: skeleton keywords cannot appear in defrole and role keywords cannot appear in defskeleton."""
    # 1. Skeleton keyword 'listeners' or 'strands' inside CPSAProtocolRole must fail
    with pytest.raises(ValueError, match="preskeleton-only keyword"):
        CPSAProtocolRole.model_validate({
            "role_name": "client",
            "variables": [{"name": "x", "sort": "text"}],
            "trace": [{"direction": "send", "message_term": "x"}],
            "listeners": ["x"],
        })

    # 2. Role keyword 'trace' or 'inputs' inside CPSAPreskeleton must fail
    with pytest.raises(ValueError, match="role-only keyword"):
        CPSAPreskeleton.model_validate({
            "protocol_name": "proto",
            "strands": [{"role_name": "client"}],
            "trace": [{"direction": "send", "message_term": "x"}],
        })


def test_equation_10_1_forbids_mesg_sort_as_encryption_key():
    """Equation 10.1: variables declared with sort 'mesg' cannot be used as encryption keys in (enc ...)."""
    with pytest.raises(ValueError, match="Equation 10.1"):
        CPSAProtocolRole(
            role_name="sender",
            variables=[
                CPSAVariableDeclaration(name="payload", sort=CPSASortEnum.TEXT),
                CPSAVariableDeclaration(name="generic_key", sort=CPSASortEnum.MESG),
            ],
            trace=[
                CPSATraceEvent(
                    direction="send",
                    channel="ch",
                    message_term=["enc", "payload", "generic_key"],
                )
            ],
        )


def test_stateful_load_stor_event_serialization_and_roletran_invariants():
    """Verify Table 10.1 load/stor 2-arg serialization, 2-arg pubk ordering, and cpsa4roletran input/output sanitization."""
    # 1. load/stor must emit 2 arguments after direction: [load, locn, term]
    load_evt = CPSATraceEvent(direction="load", location="state_cell", message_term="secret_val")
    assert load_evt.to_cpsa_json() == ["load", "state_cell", "secret_val"]

    # 2. Role serialization enforces roletran invariants and 2-arg pubk argument order
    role = CPSAProtocolRole(
        role_name="initiator",
        variables=[
            CPSAVariableDeclaration(name="server_id", sort=CPSASortEnum.NAME),
            CPSAVariableDeclaration(name="fresh_nonce", sort=CPSASortEnum.TEXT),
        ],
        trace=[
            CPSATraceEvent(
                direction="send",
                channel="ch",
                message_term=["enc", "fresh_nonce", ["pubk", "server_id", "enc_tag"]],
            )
        ],
        unique_originating=["fresh_nonce"],
        # Intentionally include fresh_nonce and a compound cat in inputs, and repeat server_id in outputs
        inputs=["server_id", "fresh_nonce", ["cat", "server_id", "fresh_nonce"]],
        outputs=["fresh_nonce", "server_id"],
    )
    role_json = role.to_cpsa_json()
    role_str = str(role_json)

    # Channel 'ch' auto-declared in vars and auto-added to inputs
    assert "['ch', 'chan']" in role_str
    # 2-arg pubk normalized to ['pubk', '"enc_tag"', 'server_id']
    assert "['pubk', '\"enc_tag\"', 'server_id']" in role_str
    # 'fresh_nonce' (uniq-orig) and ['cat', ...] stripped from inputs
    assert "['inputs', 'ch', 'server_id']" in role_str
    # 'server_id' (an input) stripped from outputs, leaving only 'fresh_nonce'
    assert "['outputs', 'fresh_nonce']" in role_str
