"""Unit and Integration Tests for Code Generation and Verification Engine."""

import pytest
import shutil
from pathlib import Path

from src.system_config import SYSTEM_CONFIG
from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAVariableDeclaration,
    CPSATraceEvent,
    CPSAProtocolRole,
    CPSAStrandInstance,
    CPSAPreskeleton,
    CPSAProtocolSpecification,
)
from src.code_generation.cpsa_scheme_emitter import emit_cpsa_scheme
from src.verification_engine.roletran_executability_gate import verify_role_executability
from src.verification_engine.mitre_build_orchestrator import execute_mitre_make_build


@pytest.fixture
def valid_unilateral_spec() -> CPSAProtocolSpecification:
    """A valid, executable unilateral authentication protocol with channels and inputs/outputs."""
    return CPSAProtocolSpecification(
        protocol_name="unilateral_auth",
        herald_comment="Unilateral Authentication Test Suite",
        roles=[
            CPSAProtocolRole(
                role_name="init",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="send", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="recv", channel="ch", message_term="n"),
                ],
                inputs=["ch", "k"],
                outputs=["n"],
                unique_originating=["n"],
            ),
            CPSAProtocolRole(
                role_name="resp",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="recv", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="send", channel="ch", message_term="n"),
                ],
                inputs=["ch", ["invk", "k"]],
                outputs=["n"],
            ),
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="unilateral_auth",
                variables=[
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                strands=[
                    CPSAStrandInstance(role_name="init", trace_length=2, variable_bindings={"k": "k", "n": "n"}),
                ],
                non_originating=[["invk", "k"]],
                unique_originating=["n"],
                comment="Initiator Point of View",
            ),
        ],
    )


@pytest.fixture
def unexecutable_spec() -> CPSAProtocolSpecification:
    """An unexecutable protocol where the responder tries to send a nonce it cannot decrypt."""
    return CPSAProtocolSpecification(
        protocol_name="broken_protocol",
        roles=[
            CPSAProtocolRole(
                role_name="resp",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="k", sort=CPSASortEnum.AKEY),
                ],
                trace=[
                    CPSATraceEvent(direction="recv", channel="ch", message_term=["enc", "n", "k"]),
                    CPSATraceEvent(direction="send", channel="ch", message_term="n"),
                ],
                inputs=["ch"],  # Missing decryption key (invk k)
                outputs=["n"],
            ),
        ],
    )


def test_scheme_emitter_generates_valid_scm(tmp_path: Path, valid_unilateral_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(valid_unilateral_spec, tmp_path)
    assert scm_path.exists()
    assert scm_path.suffix == ".scm"

    with open(scm_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "(defprotocol unilateral_auth basic" in content
    assert "(defrole init" in content
    assert "(defskeleton unilateral_auth" in content


def test_roletran_gate_accepts_valid_protocol(tmp_path: Path, valid_unilateral_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(valid_unilateral_spec, tmp_path)
    result = verify_role_executability(scm_path)

    assert result.is_executable is True
    assert result.error_diagnostic is None
    assert result.procedural_defproc_code is not None
    assert "(defproc init" in result.procedural_defproc_code


def test_roletran_gate_rejects_unexecutable_protocol(tmp_path: Path, unexecutable_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(unexecutable_spec, tmp_path)
    result = verify_role_executability(scm_path)

    assert result.is_executable is False
    assert result.error_diagnostic is not None
    assert "Received term cannot be fully destructured" in result.error_diagnostic


def test_mitre_build_orchestrator_compiles_artifacts(tmp_path: Path, valid_unilateral_spec: CPSAProtocolSpecification):
    scm_path = emit_cpsa_scheme(valid_unilateral_spec, tmp_path)
    artifacts = execute_mitre_make_build(scm_path, tmp_path)

    assert artifacts.trace_txt_path.exists()
    assert artifacts.shapes_txt_path.exists()
    assert artifacts.full_graph_xhtml_path.exists()
    assert artifacts.shapes_graph_xhtml_path.exists()
    assert artifacts.shapes_count >= 1


def test_compiler_diagnostic_repair_patches_spec(monkeypatch, tmp_path: Path, unexecutable_spec: CPSAProtocolSpecification):
    """Test that repair engine retrieves manual guidance and returns an executable specification."""
    import copy
    from unittest.mock import MagicMock
    from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification

    # Fix the missing decryption key in the role inputs
    repaired = copy.deepcopy(unexecutable_spec)
    repaired.roles[0].inputs.append(["invk", "k"])

    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock(message=MagicMock(content=repaired.model_dump_json()))]
    monkeypatch.setattr("litellm.completion", lambda **kwargs: mock_resp)

    repaired_spec = repair_protocol_specification(
        failing_spec=unexecutable_spec,
        error_diagnostic="Received term cannot be fully destructured: (enc n k)",
        verbatim_slice="Initiator sends {n}_k to responder. Responder decrypts with invk(k).",
        failure_stage="roletran",
        model="mock_model",
    )

    assert ["invk", "k"] in repaired_spec.roles[0].inputs
    scm_path = emit_cpsa_scheme(repaired_spec, tmp_path)
    res = verify_role_executability(scm_path)
    assert res.is_executable is True

