"""Integration tests for Main Pipeline Orchestrator."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.system_config import SYSTEM_CONFIG
from src.main_pipeline_orchestrator import run_rfc_translation_pipeline
from src.document_ingestion.protocol_applicability_gate import ProtocolApplicabilityReport
from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAVariableDeclaration,
    CPSATraceEvent,
    CPSAProtocolRole,
    CPSAStrandInstance,
    CPSAPreskeleton,
    CPSAProtocolSpecification,
)


@pytest.fixture
def mock_valid_spec() -> CPSAProtocolSpecification:
    return CPSAProtocolSpecification(
        protocol_name="orch_test_proto",
        herald_comment="Pipeline Orchestrator Verification Spec",
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
                protocol_name="orch_test_proto",
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


def test_pipeline_rejects_ineligible_rfc(tmp_path: Path):
    """Pipeline immediately halts on administrative or MIB documents at Stage 1a without creating dead RFC folders."""
    import json
    mib_rfc_path = SYSTEM_CONFIG.RFCS_DIR / "rfc2358.txt"
    rfc_out = tmp_path / "rfc2358_out"
    summary = run_rfc_translation_pipeline(
        rfc_file_path=mib_rfc_path,
        output_dir=rfc_out,
    )
    assert summary.is_eligible is False
    assert summary.build_successful is False
    assert not rfc_out.exists()
    assert any(k in (summary.error_message or "").lower() for k in ["mib", "managed objects"])
    idx_data = json.loads((tmp_path / "metadata_index.json").read_text(encoding="utf-8"))
    assert idx_data["total_ineligible_filtered"] == 1
    assert idx_data["rfc_directories"] == []


def test_pipeline_e2e_successful_synthesis_and_build(tmp_path: Path, mock_valid_spec: CPSAProtocolSpecification):
    """Pipeline successfully synthesizes and verifies all MITRE shapes when given an eligible RFC."""
    rfc_source = tmp_path / "rfc9999.txt"
    rfc_source.write_text(
        "Network Working Group                                          J. Doe\n"
        "Request for Comments: 9999                                        MITRE\n"
        "Category: Standards Track                                September 2026\n\n\n"
        "                    A Secure Protocol Specification\n\n"
        "Abstract\n\n"
        "   This document specifies an interactive cryptographic protocol.\n\n"
        "Table of Contents\n\n"
        "   1. Introduction .................................................... 2\n"
        "   2. Protocol Handshake ............................................. 3\n\n"
        "1. Introduction\n\n"
        + "   Detailed protocol background and security model.\n" * 40 +
        "\n2. Protocol Handshake\n\n"
        "   Alice sends an encrypted nonce to Bob. Bob decrypts and returns it.\n"
        + "   Additional protocol details.\n" * 40,
        encoding="utf-8",
    )

    mock_app_report = ProtocolApplicabilityReport(
        is_cryptographic_protocol=True,
        protocol_name="orch_test_proto",
        participating_principals=["init", "resp"],
        has_keys_or_nonces=True,
        rationale="Clear cryptographic authentication handshake.",
    )

    with patch("src.main_pipeline_orchestrator.evaluate_protocol_applicability", return_value=mock_app_report), \
         patch("src.main_pipeline_orchestrator.route_handshake_sections", return_value=["2"]), \
         patch("src.main_pipeline_orchestrator.extract_protocol_specification", return_value=mock_valid_spec):

        summary = run_rfc_translation_pipeline(
            rfc_file_path=rfc_source,
            output_dir=tmp_path / "rfc9999_out",
        )

        assert summary.is_eligible is True
        assert summary.roletran_passed is True
        assert summary.build_successful is True
        assert summary.build_artifacts is not None
        assert summary.build_artifacts.shapes_graph_xhtml_path.exists()
        assert summary.build_artifacts.shapes_txt_path.exists()
        assert summary.build_artifacts.shapes_count >= 1
        assert summary.trajectory_json_path is not None
        assert summary.trajectory_json_path.exists()
        assert summary.quality_tier in ("GOLD", "SILVER", "BRONZE")

        import json
        traj = json.loads(summary.trajectory_json_path.read_text(encoding="utf-8"))
        assert "models_used" not in traj
        assert "stage5_preflight_gate" in traj
        assert "stage6_cpsa4_solver" in traj
        assert "exploration_telemetry_from_txt" in traj["stage6_cpsa4_solver"]
        assert "shapes_analysis_from_shapes_txt" in traj["stage6_cpsa4_solver"]
        assert "quality_assessment" in traj
        assert traj["final_verified_output"]["final_scm_with_header"].startswith(";;; [RFC-ID:")

        master_index = tmp_path / "metadata_index.json"
        assert master_index.exists()
        idx_payload = json.loads(master_index.read_text(encoding="utf-8"))
        assert str(summary.trajectory_json_path.resolve()) in idx_payload["metadata_json_files"]
        assert str((tmp_path / "rfc9999_out").resolve()) in idx_payload["rfc_directories"]

