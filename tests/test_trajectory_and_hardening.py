"""Hardening and edge-case tests for 60s process-group SIGKILL, malformed YAML frontmatter, S-expr splitting, artifact containment, and offline discovery."""

import asyncio
import json
import os
import time
from pathlib import Path
from unittest.mock import MagicMock
from aiohttp import web
import pytest

from src.pipeline_events import GLOBAL_EVENT_BUS, PipelineEventBus
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    load_prompt_spec,
    parse_prompt_frontmatter,
)
from src.system_config import SYSTEM_CONFIG
from src.verification_engine.mitre_build_orchestrator import (
    CPSABuildError,
    _run_make_with_hard_timeout,
)
from src.verification_engine.trajectory_metadata_exporter import (
    split_top_level_sexprs,
    update_run_metadata_index,
)
from src.visualizer.server import VisualizerServer


def test_hard_timeout_kills_entire_process_group_including_grandchild(tmp_path: Path):
    """_run_make_with_hard_timeout sends SIGKILL to the full process group so grandchild processes never orphan."""
    pid_file = tmp_path / "grandchild.pid"
    child_env = os.environ.copy()
    child_env["TEST_GRANDCHILD_PID_FILE"] = str(pid_file)
    script = (
        'python3 -c "import os, time; '
        'open(os.environ[\'TEST_GRANDCHILD_PID_FILE\'], \'w\').write(str(os.getpid())); '
        'time.sleep(30)" & wait'
    )

    t0 = time.monotonic()
    with pytest.raises(CPSABuildError, match="timed out"):
        _run_make_with_hard_timeout(
            ["bash", "-c", script],
            cwd=tmp_path,
            env=child_env,
            timeout_seconds=0.4,
        )
    elapsed = time.monotonic() - t0
    assert elapsed < 3.0

    # Verify grandchild PID was recorded and is completely dead (ESRCH)
    assert pid_file.exists()
    grandchild_pid = int(pid_file.read_text(encoding="utf-8").strip())
    time.sleep(0.05)
    with pytest.raises(ProcessLookupError):
        os.kill(grandchild_pid, 0)


def test_malformed_yaml_frontmatter_and_edge_cases(tmp_path: Path):
    """Prompt loader degrades gracefully on invalid YAML, list frontmatter, bad scalar types, BOM, and empty body."""
    bad_yaml_file = tmp_path / PROMPT_APPLICABILITY_GATE
    bad_yaml_file.write_text("\ufeff---\nmodel: [unclosed_list\n---\nValid fallback body after bad YAML.", encoding="utf-8")
    spec = load_prompt_spec(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert spec.body == "Valid fallback body after bad YAML."
    assert spec.model

    bad_yaml_file.write_text("---\n- item1\n- item2\n---\n   \n", encoding="utf-8")
    spec_empty = load_prompt_spec(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert "MITRE CPSA 4.4.9" in spec_empty.body

    bad_yaml_file.write_text(
        '---\nmodel: strata/unsloth-iq4_xs\ntimeout: "not_an_int"\ntemperature: "not_a_float"\n---\nCustom body.',
        encoding="utf-8",
    )
    spec_scalars = load_prompt_spec(PROMPT_APPLICABILITY_GATE, prompts_dir=tmp_path)
    assert spec_scalars.model == "strata/unsloth-iq4_xs"
    assert spec_scalars.timeout == 1500
    assert spec_scalars.temperature == 0.0

    with pytest.raises(FileNotFoundError):
        load_prompt_spec("99_nonexistent_prompt.md", prompts_dir=tmp_path)

    meta, body = parse_prompt_frontmatter("Plain prompt without frontmatter.")
    assert meta == {}
    assert body == "Plain prompt without frontmatter."


def test_split_top_level_sexprs_ignores_parens_in_comments_and_strings():
    """S-expression splitter handles unbalanced parens inside Scheme `;` comments and escaped strings."""
    sample = (
        ";; Comment with unbalanced ((( parens\n"
        '(herald "proto (with) \\"escaped)\\" parens" (algebra diffie-hellman))\n'
        "(defprotocol test diffie-hellman ; trailing )(\n"
        "  (defrole init (vars (x rndx)) (trace (send x))))\n"
    )
    blocks = split_top_level_sexprs(sample)
    assert len(blocks) == 2
    assert blocks[0].startswith("(herald")
    assert blocks[1].startswith("(defprotocol test")


def test_offline_load_run_from_disk_discovery_modes(tmp_path: Path):
    """Verifies direct trajectory file, single-RFC directory, interrupted folder, and legacy filtered count replay."""
    run_dir = tmp_path / "run_offline_modes"
    rfc_ok = run_dir / "rfc2952"
    rfc_interrupted = run_dir / "rfc7627"
    rfc_ok.mkdir(parents=True)
    rfc_interrupted.mkdir(parents=True)

    traj_file = rfc_ok / "telnet_trajectory.json"
    traj_file.write_text(
        json.dumps({
            "duration_seconds": 5.2,
            "rfc_metadata": {"rfc_id": "RFC 2952", "protocol_name": "telnet_des"},
            "stage5_preflight_gate": {"final_passed": True, "total_attempts": 0},
            "stage6_cpsa4_solver": {
                "final_passed": True,
                "total_attempts": 0,
                "shapes_analysis_from_shapes_txt": {"total_realized_shapes": 2},
            },
            "quality_assessment": {"quality_tier": "SILVER"},
        }),
        encoding="utf-8",
    )
    (rfc_interrupted / "verbatim_slice.txt").write_text("Partial slice before Ctrl+C", encoding="utf-8")

    bus = PipelineEventBus()
    ov_direct = bus.load_run_from_disk(traj_file)
    assert len(ov_direct["accepted_tabs"]) == 1
    assert ov_direct["accepted_tabs"][0]["protocol_name"] == "telnet_des"

    ov_single_dir = bus.load_run_from_disk(rfc_ok)
    assert len(ov_single_dir["accepted_tabs"]) == 1
    assert ov_single_dir["accepted_tabs"][0]["rfc_id"] == "RFC 2952"

    (run_dir / "metadata_index.json").write_text(
        json.dumps({
            "schema_version": "1.0.0",
            "total_rfcs_processed": 12,
            "total_ineligible_filtered": 10,
            "runs": [
                {
                    "rfc_id": "RFC 2952",
                    "protocol_name": "telnet_des",
                    "is_eligible": True,
                    "build_successful": True,
                    "quality_tier": "SILVER",
                    "rfc_directory": str(rfc_ok),
                    "metadata_json_file": str(traj_file),
                }
            ],
        }),
        encoding="utf-8",
    )
    ov_legacy = bus.load_run_from_disk(run_dir)
    assert ov_legacy["filtered_total"] == 1
    assert len(ov_legacy["accepted_tabs"]) == 2
    statuses = {t["rfc_id"]: t["status"] for t in ov_legacy["accepted_tabs"]}
    assert statuses["RFC 2952"] == "VERIFIED"
    assert statuses["RFC 7627"] == "INTERRUPTED"

    fresh_run = tmp_path / "run_roundtrip"
    update_run_metadata_index(
        run_root_dir=fresh_run,
        rfc_id="RFC 1111",
        protocol_name="Non-Crypto Memo",
        rfc_dir=fresh_run / "rfc1111",
        scm_path=None,
        trajectory_json_path=None,
        quality_tier="INELIGIBLE",
        is_eligible=False,
        build_successful=False,
        error_message="Informational category",
        rejection_gate="Tier 0 Header Filter",
        duration_seconds=0.14,
    )
    update_run_metadata_index(
        run_root_dir=fresh_run,
        rfc_id="RFC 2952",
        protocol_name="telnet_des",
        rfc_dir=rfc_ok,
        scm_path=None,
        trajectory_json_path=traj_file,
        quality_tier="SILVER",
        is_eligible=True,
        build_successful=True,
        tab_index=1,
    )
    ov_rt = bus.load_run_from_disk(fresh_run)
    assert ov_rt["filtered_total"] == 1
    assert bus.get_filtered_slice()["items"][0]["duration_seconds"] == 0.14
    assert len(ov_rt["accepted_tabs"]) == 1
    assert ov_rt["accepted_tabs"][0]["tab_index"] == 1


def test_visualizer_artifact_endpoint_blocks_path_traversal_and_dotfiles(tmp_path: Path):
    """GET /api/artifact strictly rejects .env / arbitrary host files (HTTP 403) while serving valid run files."""
    run_dir = tmp_path / "authorized_run"
    run_dir.mkdir(parents=True)
    valid_scm = run_dir / "proto.scm"
    valid_scm.write_text("(herald proto)", encoding="utf-8")
    dot_secret = run_dir / ".env"
    dot_secret.write_text("SECRET=1", encoding="utf-8")

    GLOBAL_EVENT_BUS.clear()
    GLOBAL_EVENT_BUS.set_run_directory(run_dir, is_live=True)

    async def _exercise():
        server = VisualizerServer(host="127.0.0.1", port=8094)

        # 1. Missing path -> 400
        req_missing = MagicMock(spec=web.Request)
        req_missing.query = {}
        assert (await server.handle_artifact(req_missing)).status == 400

        # 2. Arbitrary host file outside run_dir -> 403
        req_traverse = MagicMock(spec=web.Request)
        req_traverse.query = {"path": str(SYSTEM_CONFIG.PROJECT_ROOT / "README.md")}
        assert (await server.handle_artifact(req_traverse)).status == 403

        # 3. Dotfile (.env) even inside run_dir -> 403
        req_dot = MagicMock(spec=web.Request)
        req_dot.query = {"path": str(dot_secret)}
        assert (await server.handle_artifact(req_dot)).status == 403

        # 4. Nonexistent file inside authorized run_dir -> 404
        req_404 = MagicMock(spec=web.Request)
        req_404.query = {"path": str(run_dir / "missing.scm")}
        assert (await server.handle_artifact(req_404)).status == 404

        # 5. Valid run artifact -> 200
        req_ok = MagicMock(spec=web.Request)
        req_ok.query = {"path": str(valid_scm)}
        resp_ok = await server.handle_artifact(req_ok)
        assert resp_ok.status == 200
        assert "(herald proto)" in resp_ok.text

        # 6. /api/models endpoint -> 200
        req_models = MagicMock(spec=web.Request)
        resp_models = await server.handle_models(req_models)
        assert resp_models.status == 200
        models_payload = json.loads(resp_models.text)
        assert models_payload["cpsa_timeout_seconds"] == 15
        assert "router_model" in models_payload

    asyncio.run(_exercise())


def test_parse_llm_json_unwraps_schema_properties_and_single_element_lists():
    """Verify `parse_llm_json` unwraps `{"properties": {...}}` schema-echo envelopes and `[{...}]` wrappers."""
    from src.prompt_loader import parse_llm_json

    wrapped_schema = json.dumps({
        "type": "object",
        "properties": {
            "selected_sections": ["3.1", "3.2"],
            "selection_rationale": "Defines the challenge-response exchange.",
        },
    })
    unwrapped = parse_llm_json(wrapped_schema)
    assert unwrapped["selected_sections"] == ["3.1", "3.2"]
    assert "selection_rationale" in unwrapped

    list_wrapped = json.dumps([
        {
            "selected_sections": ["4"],
            "selection_rationale": "Main handshake section.",
        }
    ])
    unwrapped_list = parse_llm_json(list_wrapped)
    assert unwrapped_list["selected_sections"] == ["4"]


def test_toc_parser_stops_at_unnumbered_back_matter_and_supports_large_tocs():
    """Verify TOC parser does not glue unnumbered Security/IANA/References onto the last section title."""
    from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
    from src.document_ingestion.handshake_section_router import _heuristic_section_router
    from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections

    sample_rfc = (
        "Table of Contents\n\n"
        "   1.  Introduction . . . . . . . . . . . . . . . . . . . . . . . .  1\n"
        "   2.  Terminology  . . . . . . . . . . . . . . . . . . . . . . . .  2\n"
        "   3.  Scope  . . . . . . . . . . . . . . . . . . . . . . . . . . .  3\n"
        "   4.  Protocol Message Exchange  . . . . . . . . . . . . . . . . .  4\n"
        "   4.1.  Initial Request  . . . . . . . . . . . . . . . . . . . . .  5\n"
        "   Security Considerations  . . . . . . . . . . . . . . . . . . . .  8\n"
        "   IANA Considerations  . . . . . . . . . . . . . . . . . . . . . .  9\n"
        "   References . . . . . . . . . . . . . . . . . . . . . . . . . . . 10\n"
        "   Author's Address . . . . . . . . . . . . . . . . . . . . . . . . 11\n\n"
        "1.  Introduction\n"
        "Intro text.\n\n"
        "4.  Protocol Message Exchange\n"
        "Parent overview ladder diagram: Alice -> Bob.\n\n"
        "4.1.  Initial Request\n"
        "Alice sends enc(n, k).\n\n"
        "5.  IANA Considerations\n"
    )
    entries = parse_table_of_contents(sample_rfc)
    sec_map = {e.section_id: e.title for e in entries}
    assert sec_map["4.1"] == "Initial Request"
    assert "Security Considerations" not in sec_map["4.1"]
    assert "References" not in sec_map["4.1"]

    # Heuristic router must skip Terminology ("2") and Scope ("3") and select "4" / "4.1"
    routed = _heuristic_section_router(entries)
    assert "2" not in routed
    assert "3" not in routed
    assert "4" in routed or "4.1" in routed

    # Slicing "4.1" without "4" automatically includes the short parent preamble ("4" -> "4.1")
    sliced = slice_verbatim_sections(sample_rfc, ["4.1"])
    assert "Parent overview ladder diagram: Alice -> Bob." in sliced
    assert "Alice sends enc(n, k)." in sliced


def test_stage2_bailout_and_cryptographic_primitive_check():
    """Verify `CPSAProtocolSpecification` supports `is_verifiable_protocol=False` bailout and detects missing crypto."""
    from src.intermediate_representation.protocol_syntax_tree import (
        CPSAProtocolRole,
        CPSAProtocolSpecification,
        CPSASortEnum,
        CPSATraceEvent,
        CPSAVariableDeclaration,
    )

    bailout_spec = CPSAProtocolSpecification(
        protocol_name="BFCP",
        is_verifiable_protocol=False,
        ineligibility_reason="RFC 4582 defines floor control signaling over TLS with no native cryptographic handshake.",
        roles=[],
        skeletons=[],
    )
    assert not bailout_spec.is_verifiable_protocol
    assert not bailout_spec.has_cryptographic_primitives()

    cleartext_spec = CPSAProtocolSpecification(
        protocol_name="NNTP_AUTHINFO",
        roles=[
            CPSAProtocolRole(
                role_name="client",
                variables=[
                    CPSAVariableDeclaration(name="u", sort=CPSASortEnum.TEXT),
                    CPSAVariableDeclaration(name="p", sort=CPSASortEnum.DATA),
                ],
                trace=[CPSATraceEvent(direction="send", message_term=["cat", "u", "p"])],
            )
        ],
    )
    assert not cleartext_spec.has_cryptographic_primitives()

    crypto_spec = CPSAProtocolSpecification(
        protocol_name="CHALLENGE_AUTH",
        roles=[
            CPSAProtocolRole(
                role_name="client",
                variables=[
                    CPSAVariableDeclaration(name="a", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="b", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.DATA),
                ],
                trace=[
                    CPSATraceEvent(
                        direction="send",
                        message_term=["enc", "n", ["ltk", "a", "b"]],
                    )
                ],
            )
        ],
    )
    assert crypto_spec.has_cryptographic_primitives()


def test_sanitize_protocol_stem_and_ast_hash_ignores_herald_comment():
    """Verify `/` and parens in `protocol_name` are sanitized (`RFC 2636`) and `_compute_ast_hash` ignores `herald_comment`."""
    from src.code_generation.cpsa_scheme_emitter import sanitize_protocol_stem
    from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
    from src.main_pipeline_orchestrator import _compute_ast_hash

    stem = sanitize_protocol_stem("Wireless Device Configuration (OTASP/OTAPA) via ACAP")
    assert "/" not in stem
    assert "(" not in stem
    assert stem == "wireless_device_configuration_otasp_otapa_via_acap"

    spec1 = CPSAProtocolSpecification(
        protocol_name="TCP_AO_NAT",
        herald_comment="Attempt 1 comment",
        roles=[],
        is_verifiable_protocol=False,
    )
    spec2 = CPSAProtocolSpecification(
        protocol_name="TCP_AO_NAT",
        herald_comment="Attempt 2 different comment",
        roles=[],
        is_verifiable_protocol=False,
    )
    assert _compute_ast_hash(spec1) == _compute_ast_hash(spec2)


def test_ensure_three_pov_skeletons_replaces_preseeded_multistrand_and_adds_secret_neq():
    """Verify `ensure_three_point_of_view_skeletons` replaces pre-seeded multi-strand root skeletons (`RFC 7469`)
    with 1-strand pure POVs and adds `(neq secret other_var)` in secrecy skeletons (`RFC 5197` / `RFC 2138`).
    """
    from src.intermediate_representation.protocol_syntax_tree import (
        CPSAPreskeleton,
        CPSAProtocolRole,
        CPSAProtocolSpecification,
        CPSASortEnum,
        CPSAStrandInstance,
        CPSATraceEvent,
        CPSAVariableDeclaration,
    )
    from src.semantic_extraction.constrained_protocol_extractor import (
        ensure_three_point_of_view_skeletons,
    )

    spec = CPSAProtocolSpecification(
        protocol_name="mikey_iba_test",
        primary_secrecy_goals=["tgk"],
        roles=[
            CPSAProtocolRole(
                role_name="initiator",
                variables=[
                    CPSAVariableDeclaration(name="i", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="r", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="hdr", sort=CPSASortEnum.DATA),
                    CPSAVariableDeclaration(name="tgk", sort=CPSASortEnum.DATA),
                ],
                trace=[
                    CPSATraceEvent(
                        direction="send",
                        message_term=["cat", "hdr", ["enc", "tgk", ["ltk", "i", "r"]]],
                    )
                ],
                unique_originating=["tgk"],
            ),
            CPSAProtocolRole(
                role_name="responder",
                variables=[
                    CPSAVariableDeclaration(name="i", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="r", sort=CPSASortEnum.NAME),
                    CPSAVariableDeclaration(name="hdr", sort=CPSASortEnum.DATA),
                    CPSAVariableDeclaration(name="tgk", sort=CPSASortEnum.DATA),
                ],
                trace=[
                    CPSATraceEvent(
                        direction="recv",
                        message_term=["cat", "hdr", ["enc", "tgk", ["ltk", "i", "r"]]],
                    )
                ],
            ),
        ],
        skeletons=[
            # Pre-seeded 2-strand root skeleton (as in RFC 7469)
            CPSAPreskeleton(
                protocol_name="mikey_iba_test",
                strands=[
                    CPSAStrandInstance(role_name="initiator"),
                    CPSAStrandInstance(role_name="responder"),
                ],
            )
        ],
    )

    normalized = ensure_three_point_of_view_skeletons(spec)
    assert len(normalized.skeletons) == 3
    # First 2 skeletons are pure 1-strand POVs
    assert len(normalized.skeletons[0].strands) == 1
    assert normalized.skeletons[0].strands[0].role_name == "initiator"
    assert len(normalized.skeletons[1].strands) == 1
    assert normalized.skeletons[1].strands[0].role_name == "responder"
    # 3rd skeleton is the secrecy listener with `(neq tgk hdr)` automatically added
    sec_skel = normalized.skeletons[2]
    assert sec_skel.listeners == ["tgk"]
    assert ["neq", "tgk", "hdr"] in sec_skel.facts


def test_quality_assessment_catches_self_reflection_and_preseeded_strands(tmp_path: Path):
    """Verify `analyze_shapes_txt` and `compute_quality_assessment` downgrade:
    - 1-strand self-reflection splits (`min_strands == 1, max_strands == 2` as in `RFC 5216` / `RFC 6786`) from GOLD to SILVER
    - Pre-seeded multi-strand root skeletons (`max_strands == initial_strand_count` as in `RFC 7469`) to BRONZE
    - Pure 1-strand unauthenticated models (`authenticated_pov_count == 0`) to BRONZE
    while grading true mutual or unilateral server-authenticated KEX (`RFC 5656`) with proved secrecy as GOLD.
    """
    from src.verification_engine.trajectory_metadata_exporter import (
        analyze_shapes_txt,
        compute_quality_assessment,
    )

    # 1. Self-reflection split (`RFC 5216` / `RFC 6786`): POV 1 has both a 1-strand shape and a 2-strand shape
    split_shapes_txt = tmp_path / "split_shapes.txt"
    split_shapes_txt.write_text(
        "(defskeleton p (vars (a b name)) (defstrand init 2) (label 0))\n"
        "(defskeleton p (vars (a name)) (defstrand init 2) (label 1) (parent 0) (shape))\n"
        "(defskeleton p (vars (a b name)) (defstrand init 2) (defstrand resp 2) (label 2) (parent 0) (shape))\n"
        "(defskeleton p (vars (a b name)) (defstrand resp 2) (label 3))\n"
        "(defskeleton p (vars (a b name)) (defstrand resp 2) (defstrand init 2) (label 4) (parent 3) (shape))\n"
        "(defskeleton p (vars (k data)) (defstrand init 2) (deflistener k) (label 5))\n",
        encoding="utf-8",
    )
    split_analysis = analyze_shapes_txt(split_shapes_txt)
    assert split_analysis["per_preskeleton_outcomes"][0]["has_self_reflection_split"] is True
    assert split_analysis["per_preskeleton_outcomes"][0]["verdict"] == "TRIVIAL_SINGLE_STRAND"
    split_qa = compute_quality_assessment(True, split_analysis, 0, 0)
    assert split_qa["quality_tier"] == "SILVER"

    # 2. Pre-seeded 2-strand root skeleton (`RFC 7469`) where CPSA added 0 strands
    preseeded_txt = tmp_path / "preseeded_shapes.txt"
    preseeded_txt.write_text(
        "(defskeleton p (vars (a b name)) (defstrand init 1) (defstrand resp 1) (label 0) (shape))\n",
        encoding="utf-8",
    )
    preseeded_analysis = analyze_shapes_txt(preseeded_txt)
    assert preseeded_analysis["per_preskeleton_outcomes"][0]["verdict"] == "TRIVIAL_SINGLE_STRAND"
    preseeded_qa = compute_quality_assessment(True, preseeded_analysis, 0, 0)
    assert preseeded_qa["quality_tier"] == "BRONZE"

    # 3. Unilateral server-authenticated KEX (`RFC 5656` SSH ECDSA KEX):
    # client POV is strictly 2-strand, server POV is 1-strand (unauthenticated client share), secrecy proved -> GOLD
    unilateral_txt = tmp_path / "unilateral_shapes.txt"
    unilateral_txt.write_text(
        "(defskeleton ssh (vars (s name)) (defstrand client 2) (label 0))\n"
        "(defskeleton ssh (vars (s name)) (defstrand client 2) (defstrand server 2) (label 1) (parent 0) (shape))\n"
        "(defskeleton ssh (vars (s name)) (defstrand server 2) (label 2))\n"
        "(defskeleton ssh (vars (s name)) (defstrand server 2) (label 3) (parent 2) (shape))\n"
        "(defskeleton ssh (vars (k skey)) (defstrand client 2) (deflistener k) (label 4))\n",
        encoding="utf-8",
    )
    unilateral_analysis = analyze_shapes_txt(unilateral_txt)
    unilateral_qa = compute_quality_assessment(True, unilateral_analysis, 0, 0)
    assert unilateral_qa["quality_tier"] == "GOLD"

