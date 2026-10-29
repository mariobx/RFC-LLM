"""Unit and integration tests for Phase 3 Hindsight Reasoning (<think>) Synthesizer."""

import json
from pathlib import Path
from unittest.mock import patch

from src.generate_think.think_schema import SynthesizedReasoningSteps, ThinkArtifactBundle
from src.generate_think.dspy_think_synthesizer import (
    _sanitize_hindsight_leakage,
    compile_deterministic_reasoning_steps,
    generate_think_for_trajectory,
    process_run_directory,
)


def _sample_trajectory_dict() -> dict:
    return {
        "schema_version": "1.0.0",
        "run_id": "rfc 9999_20261022T190000Z",
        "timestamp_utc": "2026-10-22T19:00:00Z",
        "duration_seconds": 12.5,
        "rfc_metadata": {
            "rfc_id": "RFC 9999",
            "rfc_title": "Test Mutual Auth Protocol",
            "protocol_name": "test_proto",
            "algebra": "basic",
            "participating_principals": ["init", "resp"],
            "selected_sections": ["2"],
            "sliced_lines_count": 10,
            "verbatim_rfc_slice": "2. Protocol Handshake\nInit sends encrypted nonce n under k to Resp.",
        },
        "stage2_initial_extraction": {
            "schema_self_correction_triggered": False,
            "schema_validation_error": None,
            "initial_ast": None,
            "initial_scm": None,
        },
        "stage5_preflight_gate": {
            "validator_binary": "cpsa4roletran",
            "roletran_algebra_supported": True,
            "initial_passed": False,
            "final_passed": True,
            "total_attempts": 1,
            "compiled_defproc_output": "(defproc ...)",
            "repair_attempts": [
                {
                    "attempt_number": 1,
                    "cycle_detected": False,
                    "rejected_ast": {},
                    "rejected_scm": "(defprotocol test_proto basic (defrole init ...))",
                    "raw_stderr": ":5:4: Received term cannot be fully destructured",
                    "parsed_diagnostic": "Received term cannot be fully destructured",
                    "rag_query": "cpsa4roletran received term destructured inputs",
                    "retrieved_chunk_ids": [95, 114],
                    "repaired_ast": {},
                    "repaired_scm": "(defprotocol test_proto basic (defrole init (inputs ch k) ...))",
                    "passed_after_repair": True,
                }
            ],
        },
        "stage6_cpsa4_solver": {
            "validator_binary": "cpsa4",
            "initial_passed": True,
            "final_passed": True,
            "total_attempts": 0,
            "repair_attempts": [],
            "exploration_telemetry_from_txt": {
                "source_file": "test_proto.txt",
                "txt_file_size_bytes": 1200,
                "total_explored_labels": 4,
                "dead_branch_nodes_count": 0,
                "step_limit_or_bound_hit": False,
                "state_explosion_detected": False,
                "dead_preskeleton_diagnostics": [],
            },
            "shapes_analysis_from_shapes_txt": {
                "source_file": "test_proto_shapes.txt",
                "shapes_file_size_bytes": 800,
                "total_preskeletons": 2,
                "total_realized_shapes": 1,
                "per_preskeleton_outcomes": [
                    {
                        "skeleton_index": 0,
                        "root_label": 0,
                        "skeleton_type": "participant_pov",
                        "comment": "Initiator POV",
                        "has_deflistener": False,
                        "listener_term": None,
                        "realized_shape_labels": [1],
                        "realized_shapes_count": 1,
                        "max_strands_in_realized_shape": 2,
                        "instantiated_roles_in_shape": [
                            {"role": "init", "height": 2},
                            {"role": "resp", "height": 2},
                        ],
                        "is_trivial_single_strand_shape": False,
                        "goal_satisfied": None,
                        "verdict": "AUTHENTICATED_MULTI_STRAND",
                    }
                ],
            },
        },
        "quality_assessment": {
            "quality_tier": "GOLD",
            "all_participant_povs_realized": True,
            "all_participant_povs_multi_strand": True,
            "all_secrecy_listeners_unrealized": True,
            "post_training_routing": {
                "eligible_for_sft_positive": True,
                "dpo_contrastive_pairs_available": 1,
                "compiler_repair_trajectories_available": 1,
            },
        },
        "final_verified_output": {
            "final_ast": {
                "protocol_name": "test_proto",
                "message_algebra": "basic",
                "herald_comment": "Test mutual auth protocol",
                "roles": [
                    {
                        "role_name": "init",
                        "description": "Initiator role",
                        "variables": [
                            {"name": "ch", "sort": "chan", "description": "Channel", "rfc_field": "Sec 2"},
                            {"name": "n", "sort": "text", "description": "Fresh nonce", "rfc_field": "Sec 2"},
                            {"name": "k", "sort": "akey", "description": "Public key", "rfc_field": "Sec 2"},
                        ],
                        "trace": [
                            {
                                "direction": "send",
                                "channel": "ch",
                                "message_term": ["enc", "n", "k"],
                                "description": "Send encrypted nonce",
                            },
                            {
                                "direction": "recv",
                                "channel": "ch",
                                "message_term": "n",
                                "description": "Receive plaintext nonce",
                            },
                        ],
                        "inputs": ["ch", "k"],
                        "outputs": ["n"],
                        "unique_originating": ["n"],
                        "unique_generated": [],
                        "non_originating": [],
                    }
                ],
                "skeletons": [
                    {
                        "protocol_name": "test_proto",
                        "description": "Initiator POV",
                        "variables": [
                            {"name": "n", "sort": "text"},
                            {"name": "k", "sort": "akey"},
                        ],
                        "strands": [
                            {"role_name": "init", "variable_bindings": {"n": "n", "k": "k"}},
                        ],
                        "non_originating": [["invk", "k"]],
                        "unique_originating": ["n"],
                        "listeners": [],
                        "comment": "Initiator POV",
                    }
                ],
            },
            "final_scm_with_header": ";;; [RFC-ID: RFC 9999]\n(defprotocol test_proto basic ...)",
            "distilled_shapes_txt": "(herald ...)",
        },
    }


def test_deterministic_reasoning_compiler_and_hindsight_sanitizer():
    traj = _sample_trajectory_dict()
    steps = compile_deterministic_reasoning_steps(traj)
    assert isinstance(steps, SynthesizedReasoningSteps)
    assert "RFC 9999" in steps.step1_protocol_and_algebra
    assert "`n` (sort `text`)" in steps.step2_principals_and_variables
    assert "(send ch (enc n k))" in steps.step3_message_flow_and_terms
    assert "Wait—let me check pre-flight role executability" in steps.step4_compiler_backtracking_and_invariants

    leaked = "<think>Looking at the provided AST and in the given final_scm, we use basic.</think>"
    cleaned = _sanitize_hindsight_leakage(leaked)
    assert "provided AST" not in cleaned
    assert "given final_scm" not in cleaned
    assert not cleaned.startswith("<think>")


def test_process_run_directory_creates_think_json_and_updates_metadata_index(tmp_path: Path):
    run_dir = tmp_path / "run_2026-10-22_19-00-00"
    rfc_dir = run_dir / "rfc9999"
    rfc_dir.mkdir(parents=True)

    traj_path = rfc_dir / "test_proto_trajectory.json"
    traj_path.write_text(json.dumps(_sample_trajectory_dict(), indent=2), encoding="utf-8")

    index_path = run_dir / "metadata_index.json"
    index_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "run_directory": str(run_dir.resolve()),
                "total_rfcs_processed": 1,
                "metadata_json_files": [str(traj_path.resolve())],
                "rfc_directories": [str(rfc_dir.resolve())],
                "runs": [
                    {
                        "rfc_id": "RFC 9999",
                        "protocol_name": "test_proto",
                        "is_eligible": True,
                        "build_successful": True,
                        "quality_tier": "GOLD",
                        "rfc_directory": str(rfc_dir.resolve()),
                        "scm_file": str((rfc_dir / "test_proto.scm").resolve()),
                        "metadata_json_file": str(traj_path.resolve()),
                        "error_message": None,
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    think_files = process_run_directory(
        target_path=run_dir,
        mode="deterministic",
        min_tier="GOLD",
        export_jsonl=True,
    )

    assert len(think_files) == 1
    think_path = rfc_dir / "test_proto_think.json"
    assert think_files[0] == think_path
    assert think_path.exists()

    bundle = ThinkArtifactBundle.model_validate_json(think_path.read_text(encoding="utf-8"))
    assert bundle.thinking_block.startswith("<think>\n")
    assert bundle.thinking_block.endswith("\n</think>")
    assert len(bundle.sft_messages) == 3
    assert bundle.sft_messages[2]["content"].startswith("<think>\n")
    assert ";;; [RFC-ID: RFC 9999]" in bundle.sft_messages[2]["content"]
    assert len(bundle.dpo_contrastive_pairs) == 1
    assert bundle.dpo_contrastive_pairs[0].stage == "stage5_roletran"

    updated_index = json.loads(index_path.read_text(encoding="utf-8"))
    assert str(think_path.resolve()) in updated_index["think_json_files"]
    assert updated_index["runs"][0]["think_json_file"] == str(think_path.resolve())
    assert (run_dir / "sft_train.jsonl").exists()
    assert (run_dir / "dpo_pairs.jsonl").exists()
