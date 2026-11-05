"""Hardening and edge-case tests for 60s process-group SIGKILL, malformed YAML frontmatter, S-expr splitting, artifact containment, and offline discovery."""

import asyncio
import json
import os
import time
from pathlib import Path
from unittest.mock import MagicMock
from aiohttp import web
import pytest

from src.intermediate_representation.protocol_syntax_tree import (
    CPSAPreskeleton,
    CPSAProtocolRole,
    CPSAProtocolSpecification,
    CPSASortEnum,
    CPSAStrandInstance,
    CPSATraceEvent,
    CPSAVariableDeclaration,
)
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
    assert spec_scalars.timeout == 900
    assert spec_scalars.temperature is None

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
    """Verify `analyze_shapes_txt`, `compute_security_findings`, and `compute_quality_assessment`:
    - Decouple `quality_tier` (modeling & compilation fidelity) from `security_findings` (formal CPSA security verdict)
    - Flag 1-strand/2-strand branched authentication (`RFC 5216` / `RFC 6786`) as `CONDITIONAL_BRANCHED_AUTHENTICATION` in `security_findings` while keeping `quality_tier == "GOLD"`
    - Downgrade pre-seeded multi-strand root skeletons (`max_strands == initial_strand_count` as in `RFC 7469`) to `BRONZE`
    - Grade unilateral server-authenticated KEX (`RFC 5656`) as `GOLD` with `UNILATERAL_AUTHENTICATED` and `SECRECY_PROVED`
    - Detect Lowe MITM principal disagreement (`b` vs `b-0`), same-role reflection, and secrecy leaks in `security_findings` without punishing `quality_tier`.
    """
    from src.verification_engine.trajectory_metadata_exporter import (
        analyze_shapes_txt,
        compute_quality_assessment,
        compute_security_findings,
    )

    # 1. Branched 1-strand/2-strand split (`RFC 5216` / `RFC 6786`): executable & multi-strand -> GOLD,
    # while security_findings records CONDITIONAL_BRANCHED_AUTHENTICATION
    split_shapes_txt = tmp_path / "split_shapes.txt"
    split_shapes_txt.write_text(
        "(defskeleton p (vars (a b name)) (defstrand init 2 (a a) (b b)) (label 0))\n"
        "(defskeleton p (vars (a name)) (defstrand init 2 (a a) (b a)) (label 1) (parent 0) (shape))\n"
        "(defskeleton p (vars (a b name)) (defstrand init 2 (a a) (b b)) (defstrand resp 2 (a a) (b b)) (label 2) (parent 0) (shape))\n"
        "(defskeleton p (vars (a b name)) (defstrand resp 2 (a a) (b b)) (label 3))\n"
        "(defskeleton p (vars (a b name)) (defstrand resp 2 (a a) (b b)) (defstrand init 2 (a a) (b b)) (label 4) (parent 3) (shape))\n"
        "(defskeleton p (vars (k data)) (defstrand init 2) (deflistener k) (label 5))\n",
        encoding="utf-8",
    )
    split_analysis = analyze_shapes_txt(split_shapes_txt)
    assert split_analysis["per_preskeleton_outcomes"][0]["has_self_reflection_split"] is True
    split_sec = compute_security_findings(split_analysis)
    assert split_sec["authentication_profile"] == "CONDITIONAL_BRANCHED_AUTHENTICATION"
    assert split_sec["parameter_agreement_status"] == "FULL_PARAMETER_AGREEMENT"
    split_qa = compute_quality_assessment(True, split_analysis, 0, 0, security_findings=split_sec)
    assert split_qa["quality_tier"] == "GOLD"

    # 2. Pre-seeded 2-strand root skeleton (`RFC 7469`) where CPSA added 0 strands -> BRONZE
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
        "(defskeleton ssh (vars (s name)) (defstrand client 2 (s s)) (label 0))\n"
        "(defskeleton ssh (vars (s name)) (defstrand client 2 (s s)) (defstrand server 2 (s s)) (label 1) (parent 0) (shape))\n"
        "(defskeleton ssh (vars (s name)) (defstrand server 2 (s s)) (label 2))\n"
        "(defskeleton ssh (vars (s name)) (defstrand server 2 (s s)) (label 3) (parent 2) (shape))\n"
        "(defskeleton ssh (vars (k skey)) (defstrand client 2) (deflistener k) (label 4))\n",
        encoding="utf-8",
    )
    unilateral_analysis = analyze_shapes_txt(unilateral_txt)
    unilateral_sec = compute_security_findings(unilateral_analysis)
    assert unilateral_sec["authentication_profile"] == "UNILATERAL_AUTHENTICATED"
    assert unilateral_sec["secrecy_status"] == "SECRECY_PROVED"
    unilateral_qa = compute_quality_assessment(True, unilateral_analysis, 0, 0, security_findings=unilateral_sec)
    assert unilateral_qa["quality_tier"] == "GOLD"

    # 4. Vulnerable protocol (Needham-Schroeder Lowe MITM `b` vs `b-0` + same-role reflection + leaked secret `k`):
    # Model is executable and faithful (`quality_tier == "GOLD"`), while `security_findings` captures all 3 vulnerabilities
    vuln_txt = tmp_path / "vuln_shapes.txt"
    vuln_txt.write_text(
        "(defskeleton ns (vars (a b name) (k skey)) (defstrand init 2 (a a) (b b)) (label 0))\n"
        "(defskeleton ns (vars (a b b-0 name) (k skey)) (defstrand init 2 (a a) (b b)) (defstrand resp 2 (a a) (b b-0)) (label 1) (parent 0) (shape))\n"
        "(defskeleton ns (vars (a b name) (k skey)) (defstrand resp 2 (a a) (b b)) (label 2))\n"
        "(defskeleton ns (vars (a b name) (k skey)) (defstrand resp 2 (a a) (b b)) (defstrand resp 2 (a b) (b a)) (label 3) (parent 2) (shape))\n"
        "(defskeleton ns (vars (k skey)) (defstrand init 2) (deflistener k) (label 4))\n"
        "(defskeleton ns (vars (k skey)) (defstrand init 2) (deflistener k) (label 5) (parent 4) (shape))\n",
        encoding="utf-8",
    )
    vuln_analysis = analyze_shapes_txt(vuln_txt)
    vuln_sec = compute_security_findings(vuln_analysis)
    assert vuln_sec["parameter_agreement_status"] == "PRINCIPAL_DISAGREEMENT_MITM_OR_UKS"
    assert vuln_sec["role_reflection_status"] == "SAME_ROLE_REFLECTION_DETECTED"
    assert vuln_sec["secrecy_status"] == "SECRECY_LEAK_DETECTED"
    assert vuln_sec["leaked_secrets"] == ["k"]
    assert len(vuln_sec["vulnerabilities_and_anomalies"]) >= 3
    vuln_qa = compute_quality_assessment(True, vuln_analysis, 0, 0, security_findings=vuln_sec)
    assert vuln_qa["quality_tier"] == "GOLD"


def test_prune_keep_ineligible_only(tmp_path: Path):
    """Verify `PipelineMetricsCSVLogger.prune_keep_ineligible_only` deletes all rows EXCEPT `is_eligible=False`."""
    from src.logging_config import PipelineMetricsCSVLogger

    csv_path = tmp_path / "pipeline_runs.csv"
    logger = PipelineMetricsCSVLogger(csv_path=csv_path)
    logger.log_run(rfc_id="RFC1111", is_eligible=False, status="INELIGIBLE", rejection_gate="Tier 0 Header Filter")
    logger.log_run(rfc_id="RFC4582", is_eligible=False, status="INELIGIBLE", rejection_gate="Stage 2 Verbatim Slice Gate")
    logger.log_run(rfc_id="RFC5246", is_eligible=True, status="VERIFIED", quality_tier="GOLD", solver_passed=True)
    logger.log_run(rfc_id="RFC5849", is_eligible=True, status="FAILED", quality_tier="REJECTED", solver_passed=False)

    removed, kept = logger.prune_keep_ineligible_only()
    assert removed == 2
    assert kept == 2

    remaining_rows = logger._read_existing_rows()
    remaining_ids = [r["rfc_id"] for r in remaining_rows]
    assert remaining_ids == ["RFC1111", "RFC4582"]
    assert all(r["is_eligible"] == "False" for r in remaining_rows)


def test_seed_from_source_and_67_column_security_findings_csv(tmp_path: Path):
    """Verify `seed_from_source` copies rows from an older run without mutating the source CSV,
    and `log_run` records all 17 CPSA 4.4.9 `security_findings` columns plus `Eligible: <rationale>`.
    """
    from src.logging_config import PipelineMetricsCSVLogger

    assert len(PipelineMetricsCSVLogger.CSV_HEADER) == 67

    old_run_dir = tmp_path / "run_old"
    old_run_dir.mkdir(parents=True)
    old_csv = old_run_dir / "pipeline_runs.csv"
    old_logger = PipelineMetricsCSVLogger(csv_path=old_csv)
    old_logger.log_run(
        rfc_id="RFC1111",
        is_eligible=False,
        status="INELIGIBLE",
        rejection_gate="Tier 0 Header Filter",
        error_message="Ineligible: Informational document",
    )
    old_logger.log_run(
        rfc_id="RFC5246",
        is_eligible=True,
        status="VERIFIED",
        quality_tier="GOLD",
        solver_passed=True,
        error_message="Eligible: Defines the TLS 1.2 handshake with explicit key exchange.",
        security_findings={
            "role_executability": "ALL_ROLES_EXECUTABLE",
            "dead_roles_count": 0,
            "dead_roles": [],
            "authentication_profile": "MUTUAL_MULTI_STRAND",
            "multi_strand_pov_roles": ["Client", "Server"],
            "single_strand_pov_roles": [],
            "unrealized_pov_roles": [],
            "parameter_agreement_status": "FULL_PARAMETER_AGREEMENT",
            "disagreed_parameters_count": 0,
            "role_reflection_status": "NO_REFLECTION",
            "secrecy_status": "SECRECY_PROVED",
            "protected_secrets": ["pre_master_secret"],
            "leaked_secrets": [],
            "defgoal_satisfaction_status": "NO_EXPLICIT_DEFGOALS",
            "shape_analysis_sentences_count": 2,
            "anomalies_count": 0,
            "vulnerabilities_and_anomalies": [],
        },
    )

    # New run seeds from old_run_dir and prunes keep-ineligible without touching old_csv
    new_csv = tmp_path / "run_new" / "pipeline_runs.csv"
    new_logger = PipelineMetricsCSVLogger(csv_path=new_csv)
    seeded_count = new_logger.seed_from_source(old_run_dir)
    assert seeded_count == 2

    removed, kept = new_logger.prune_keep_ineligible_only()
    assert removed == 1
    assert kept == 1

    # Source CSV in old_run_dir must remain completely untouched (still 2 rows)
    old_rows = old_logger._read_existing_rows()
    assert len(old_rows) == 2
    rfc5246_row = [r for r in old_rows if r["rfc_id"] == "RFC5246"][0]
    assert rfc5246_row["authentication_profile"] == "MUTUAL_MULTI_STRAND"
    assert rfc5246_row["parameter_agreement_status"] == "FULL_PARAMETER_AGREEMENT"
    assert rfc5246_row["secrecy_status"] == "SECRECY_PROVED"
    assert rfc5246_row["protected_secrets"] == "pre_master_secret"
    assert rfc5246_row["shape_analysis_sentences_count"] == "2"
    assert rfc5246_row["error_message"].startswith("Eligible: ")


def test_cli_rejects_csv_prune_or_skip_flags_without_csv_source(monkeypatch):
    """Verify `--keep-ineligible`, `--skip-completed`, and `--retry-failed` fail fast if `--csv` is omitted."""
    import sys
    from src.pipeline import main

    for flag in ("--keep-ineligible", "--skip-completed", "--retry-failed"):
        monkeypatch.setattr(sys, "argv", ["rfc-llm", "refrences/all_RFCs/", flag])
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2


def test_compact_diagnostic_headline_strips_snowball_autopsy_and_csv_api_works(tmp_path: Path):
    """Verify `_compact_diagnostic_headline` strips the multi-line Snowball Autopsy block and `/api/csv` serves 67-column analytics."""
    from src.logging_config import PipelineMetricsCSVLogger
    from src.main_pipeline_orchestrator import _compact_diagnostic_headline
    from src.visualizer.server import VisualizerServer, hydrate_tab_payload

    full_diag = (
        "MITRE CPSA compilation timed out after 15 seconds (state-space explosion).\n"
        "Tier 1 Search-Order Portfolio also failed to terminate.\n\n"
        "=== CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT (Tier 2 Trace Analysis) ===\n"
        "Exploding Query: POV Skeleton #1\n"
        "Derivation Stats: 20 skeletons inspected\n"
    )
    compact = _compact_diagnostic_headline(full_diag)
    assert "=== CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT" not in compact
    assert "MITRE CPSA compilation timed out after 15 seconds" in compact

    run_dir = tmp_path / "run_csv_api"
    run_dir.mkdir(parents=True)
    csv_path = run_dir / "pipeline_runs.csv"
    csv_logger = PipelineMetricsCSVLogger(csv_path=csv_path)
    csv_logger.log_run(
        rfc_id="RFC2952",
        is_eligible=True,
        status="VERIFIED",
        quality_tier="GOLD",
        protocol_name="telnet_des",
        solver_passed=True,
        error_message="Eligible: Defines Telnet DES_CFB64 authentication handshake.",
    )

    GLOBAL_EVENT_BUS.clear()
    GLOBAL_EVENT_BUS.set_run_directory(run_dir, is_live=True, csv_path=csv_path)

    async def _check_csv_endpoint():
        server = VisualizerServer(host="127.0.0.1", port=8095)
        req = MagicMock(spec=web.Request)
        resp = await server.handle_csv(req)
        assert resp.status == 200
        payload = json.loads(resp.text)
        assert payload["row_count"] == 1
        assert len(payload["headers"]) == 67
        assert payload["rows"][0]["rfc_id"] == "RFC2952"
        assert payload["rows"][0]["error_message"].startswith("Eligible:")

    asyncio.run(_check_csv_endpoint())


def test_section_router_normalizes_hash_prefixes_and_section_labels():
    """Verify `_match_valid_toc_id` and `normalize_section_id_token` normalize `#7.1.1` (RFC 6143), `Section 3.2.`, and `Appendix A`."""
    from src.document_ingestion.handshake_section_router import (
        SectionRoutingDecision,
        _match_valid_toc_id,
        normalize_section_id_token,
    )

    assert normalize_section_id_token("#7.1.1") == "7.1.1"
    assert normalize_section_id_token("Section 3.2.") == "3.2"
    assert normalize_section_id_token("§4.1 Handshake Protocol") == "4.1"
    assert normalize_section_id_token("Appendix A.") == "App-A"

    valid_ids = {"3", "3.2", "7.1.1", "7.1.2", "App-A"}
    assert _match_valid_toc_id("#7.1.1", valid_ids) == "7.1.1"
    assert _match_valid_toc_id("Section 3.2.", valid_ids) == "3.2"
    assert _match_valid_toc_id("Appendix A", valid_ids) == "App-A"
    assert _match_valid_toc_id("#99.9", valid_ids) is None

    # Schema description must never suggest '#.#'
    schema_desc = SectionRoutingDecision.model_json_schema()["properties"]["selected_section_ids"]["description"]
    assert "#.#" not in schema_desc


def test_verbatim_slicer_handles_hex_titles_parent_fallback_and_short_unnumbered_rfcs():
    """Verify `slice_verbatim_sections` slices `6.7.2.  0x0002 - AUTHENTICATION_TYPE` (RFC 7868),
    falls back to parent `6.7` if a leaf subsection is missing, and handles short unnumbered RFCs (RFC 3268).
    """
    from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections

    rfc7868_excerpt = (
        "Table of Contents\n\n"
        "   1.  Introduction . . . . . . . . . . . . . . . . . . . . . . . .  1\n"
        "   6.7.  EIGRP Packet TLVs  . . . . . . . . . . . . . . . . . . . . 52\n"
        "   6.7.2.  0x0002 - AUTHENTICATION_TYPE . . . . . . . . . . . . . . 53\n\n"
        "1.  Introduction\n"
        "Intro text.\n\n"
        "6.7.  EIGRP Packet TLVs\n"
        "Parent TLV section overview.\n\n"
        "6.7.2.  0x0002 - AUTHENTICATION_TYPE\n"
        "This TLV conveys authentication type and MD5/SHA256 data.\n\n"
        "6.8.  Next Section\n"
        "Trailing text.\n"
    )
    sliced_hex = slice_verbatim_sections(rfc7868_excerpt, ["#6.7.2"])
    assert "0x0002 - AUTHENTICATION_TYPE" in sliced_hex
    assert "MD5/SHA256 data" in sliced_hex
    assert "Trailing text." not in sliced_hex

    # Parent fallback if leaf '6.7.99' is missing in body
    sliced_parent = slice_verbatim_sections(rfc7868_excerpt, ["6.7.99"])
    assert "Parent TLV section overview." in sliced_parent

    # Short unnumbered RFC (like RFC 3268)
    rfc3268_short = (
        "Network Working Group\n"
        "Request for Comments: 3268\n\n"
        "Overview\n\n"
        "This document proposes AES ciphersuites for TLS.\n\n"
        "Cipher Usage\n\n"
        "TLS_RSA_WITH_AES_128_CBC_SHA\n\n"
        "References\n\n"
        "[TLS] Dierks, T., RFC 2246.\n"
    )
    sliced_unnumbered = slice_verbatim_sections(rfc3268_short, ["FULL_BODY"])
    assert "TLS_RSA_WITH_AES_128_CBC_SHA" in sliced_unnumbered
    assert "[TLS] Dierks" not in sliced_unnumbered


def test_temperature_forwarding_on_cycle_detected_and_default_omission():
    """Verify `SYSTEM_CONFIG.get_llm_kwargs` omits `temperature` when `None` and forwards `temperature` when set."""
    from src.prompt_loader import PROMPT_COMPILER_REPAIR, PROMPT_PROTOCOL_EXTRACTION, load_prompt_spec

    ext_spec = load_prompt_spec(PROMPT_PROTOCOL_EXTRACTION)
    rep_spec = load_prompt_spec(PROMPT_COMPILER_REPAIR)
    assert ext_spec.timeout == 3600
    assert rep_spec.timeout == 3600
    assert ext_spec.temperature is None
    assert rep_spec.temperature is None

    kwargs_default = SYSTEM_CONFIG.get_llm_kwargs("strata/unsloth-iq4_xs", temperature=None, max_tokens=65536)
    assert "temperature" not in kwargs_default

    kwargs_cycle = SYSTEM_CONFIG.get_llm_kwargs("nous/anthropic/claude-haiku-5.5", temperature=0.5, max_tokens=65536)
    assert kwargs_cycle["temperature"] == 0.5


def test_cpsa_toolchain_preflight_verification(monkeypatch, tmp_path: Path):
    """Verify `SYSTEM_CONFIG.verify_cpsa_toolchain` detects missing CPSA binaries."""
    import shutil

    # Normally all binaries exist on this machine
    assert SYSTEM_CONFIG.verify_cpsa_toolchain() == []

    # Simulate missing cpsa4json binary and not on PATH
    monkeypatch.setattr(SYSTEM_CONFIG, "CPSA4JSON_BIN", tmp_path / "nonexistent_cpsa4json")
    monkeypatch.setattr(shutil, "which", lambda name: None if name == "cpsa4json" else f"/usr/bin/{name}")
    missing = SYSTEM_CONFIG.verify_cpsa_toolchain()
    assert len(missing) == 1
    assert "cpsa4json" in missing[0]


def test_deterministic_ast_prenormalizer_quotes_tags_infers_names_and_inputs(tmp_path: Path):
    """Verify integer constants, undeclared string tags, implied ltk/pubk names, and roletran inputs auto-normalize."""
    from src.code_generation.cpsa_scheme_emitter import emit_cpsa_scheme
    from src.verification_engine.roletran_executability_gate import verify_role_executability

    spec = CPSAProtocolSpecification(
        protocol_name="sake_like_proto",
        message_algebra="basic",
        roles=[
            CPSAProtocolRole(
                role_name="Server",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="rand_s", sort=CPSASortEnum.DATA),
                    CPSAVariableDeclaration(name="rand_p", sort=CPSASortEnum.DATA),
                ],
                trace=[
                    CPSATraceEvent(
                        direction="send",
                        channel="ch",
                        # 1 is an integer constant, "SAKE_CHALLENGE" is an undeclared tag,
                        # and server_id / peer_id are implied 'name' variables from ltk
                        message_term=["cat", 1, "SAKE_CHALLENGE", "rand_s"],
                    ),
                    CPSATraceEvent(
                        direction="recv",
                        channel="ch",
                        message_term=[
                            "cat",
                            2,
                            "SAKE_CONFIRM",
                            "rand_p",
                            ["hash", 2, "rand_s", "rand_p", ["ltk", "server_id", "peer_id"]],
                        ],
                    ),
                ],
                unique_originating=["rand_s"],
                inputs=["ch"],
            )
        ],
        skeletons=[
            CPSAPreskeleton(
                protocol_name="sake_like_proto",
                variables=[
                    CPSAVariableDeclaration(name="rand_s", sort=CPSASortEnum.DATA),
                ],
                strands=[
                    CPSAStrandInstance(role_name="Server", variable_bindings={"rand_s": "rand_s"}),
                ],
                non_originating=[["ltk", "server_id", "peer_id"]],
            )
        ],
    )

    scm_path = emit_cpsa_scheme(spec, tmp_path)
    scm_text = scm_path.read_text(encoding="utf-8")
    assert '"1"' in scm_text
    assert '"SAKE_CHALLENGE"' in scm_text
    assert "server_id peer_id name" in scm_text
    assert "(ltk server_id peer_id)" in scm_text

    rt_res = verify_role_executability(scm_path)
    assert rt_res.is_executable, f"Expected roletran PASS, got: {rt_res.raw_stderr}"


def test_compute_ast_hash_ignores_role_comment_and_descriptions():
    """Verify `_compute_ast_hash` produces identical hashes when only role.comment or variable/event descriptions differ."""
    from src.main_pipeline_orchestrator import _compute_ast_hash

    spec_a = CPSAProtocolSpecification(
        protocol_name="ping_pong_proto",
        roles=[
            CPSAProtocolRole(
                role_name="Initiator",
                comment="Attempt 1 comment",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN, description="desc A", rfc_field="Sec 3"),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.DATA, description="nonce A", rfc_field="Sec 3.1"),
                ],
                trace=[
                    CPSATraceEvent(direction="send", channel="ch", message_term="n", description="send A"),
                ],
                unique_originating=["n"],
                inputs=["ch"],
            )
        ],
    )
    spec_b = spec_a.model_copy(deep=True)
    spec_b.roles[0].comment = "Attempt 3 different comment"
    spec_b.roles[0].variables[0].description = "different var description"
    spec_b.roles[0].variables[0].rfc_field = "Section 4.2"
    spec_b.roles[0].trace[0].description = "different trace event description"

    assert _compute_ast_hash(spec_a) == _compute_ast_hash(spec_b)


def test_hyphenated_headings_bare_appendices_and_legacy_rfc_header():
    """Verify RFC 3007 hyphenated headings, RFC 3957 bare appendices, and pre-RFC-2223 title extraction."""
    from src.document_ingestion.handshake_section_router import _heuristic_section_router
    from src.document_ingestion.rfc_header_filter import filter_rfc_header
    from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
    from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections

    # 1. RFC 3007 style hyphenated body headings + Full Copyright Statement
    rfc3007_text = (
        "Network Working Group                                      B. Wellington\n"
        "Request for Comments: 3007                                Nominum, Inc.\n"
        "Category: Standards Track                                  November 2000\n\n"
        "              Secure Domain Name System (DNS) Dynamic Update\n\n"
        "Status of this Memo\n"
        "   Standards Track.\n\n"
        "1 - Introduction\n"
        "   Intro text.\n\n"
        "2 - Authentication\n"
        "   DNS dynamic update authentication message exchange details.\n\n"
        "9. Full Copyright Statement\n"
        "   Copyright (C) The Internet Society (2000).\n"
    )
    toc = parse_table_of_contents(rfc3007_text)
    sec_ids = [e.section_id for e in toc]
    assert "1" in sec_ids and "2" in sec_ids
    routed = _heuristic_section_router(toc)
    assert "2" in routed
    assert "9" not in routed
    sliced = slice_verbatim_sections(rfc3007_text, ["2"])
    assert "DNS dynamic update authentication" in sliced
    assert "Copyright (C)" not in sliced

    # 2. Pre-RFC-2223 header without "Status of This Memo" or "Abstract"
    legacy_rfc = (
        "Network Working Group                                          R. Thomas\n"
        "Request for Comments: 644                                           BBN\n"
        "NIC #30879                                                    July 1974\n\n"
        "         On the Problem of Signature Authentication for Network Mail\n\n"
        "1. Introduction\n"
        "   This note describes a protocol for authenticated network mail.\n"
        + "\n".join(f"   Body line {i} discussing mail signatures." for i in range(60))
    )
    hdr = filter_rfc_header(legacy_rfc)
    assert hdr.title == "On the Problem of Signature Authentication for Network Mail"


def test_multi_deflistener_telemetry_and_dangling_response_quality_cap(tmp_path: Path):
    """Verify multi-deflistener secrets extraction (`RFC 3957`) and dangling response cap (`RFC 3971`)."""
    from src.verification_engine.trajectory_metadata_exporter import (
        analyze_shapes_txt,
        compute_quality_assessment,
        compute_security_findings,
    )

    shapes_file = tmp_path / "mipv4_shapes.txt"
    shapes_file.write_text(
        '(defskeleton mipv4\n'
        '  (vars (k_ha k_fa skey) (mn fa name) (ch chan))\n'
        '  (defstrandmax ForeignAgent (ch ch))\n'
        '  (deflistener k_ha)\n'
        '  (deflistener k_fa)\n'
        '  (label 0)\n'
        '  (comment "Secrecy POV"))\n'
        '(defskeleton mipv4\n'
        '  (vars (mn fa name) (ch chan))\n'
        '  (defstrand Initiator 1 (ch ch))\n'
        '  (label 1)\n'
        '  (parent 0)\n'
        '  (shape))\n',
        encoding="utf-8",
    )
    # Test multi-deflistener extraction on unrealized secrecy skeleton
    shapes_file_unrealized = tmp_path / "mipv4_unrealized_shapes.txt"
    shapes_file_unrealized.write_text(
        '(defskeleton mipv4\n'
        '  (vars (mn fa name) (ch chan))\n'
        '  (defstrand Initiator 1 (ch ch))\n'
        '  (label 0))\n'
        '(defskeleton mipv4\n'
        '  (vars (mn fa name) (ch chan))\n'
        '  (defstrand Initiator 1 (ch ch))\n'
        '  (label 1)\n'
        '  (parent 0)\n'
        '  (shape))\n'
        '(defskeleton mipv4\n'
        '  (vars (mn fa name) (ch chan))\n'
        '  (defstrand Responder 2 (ch ch))\n'
        '  (label 2))\n'
        '(defskeleton mipv4\n'
        '  (vars (mn fa name) (ch chan))\n'
        '  (defstrand Responder 2 (ch ch))\n'
        '  (defstrand Initiator 1 (ch ch))\n'
        '  (label 3)\n'
        '  (parent 2)\n'
        '  (shape))\n'
        '(defskeleton mipv4\n'
        '  (vars (k_ha k_fa skey) (mn fa name) (ch chan))\n'
        '  (defstrandmax Responder (ch ch))\n'
        '  (deflistener k_ha)\n'
        '  (deflistener k_fa)\n'
        '  (label 4))\n',
        encoding="utf-8",
    )
    sa = analyze_shapes_txt(shapes_file_unrealized)
    sec = compute_security_findings(sa)
    assert "k_ha" in sec["protected_secrets"]
    assert "k_fa" in sec["protected_secrets"]

    # Truncated initiator role (send only) while Responder has recv + send -> capped at SILVER
    truncated_spec = CPSAProtocolSpecification(
        protocol_name="send_proto",
        roles=[
            CPSAProtocolRole(
                role_name="Initiator",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.DATA),
                ],
                trace=[CPSATraceEvent(direction="send", channel="ch", message_term="n")],
            ),
            CPSAProtocolRole(
                role_name="Responder",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="n", sort=CPSASortEnum.DATA),
                ],
                trace=[
                    CPSATraceEvent(direction="recv", channel="ch", message_term="n"),
                    CPSATraceEvent(direction="send", channel="ch", message_term="n"),
                ],
            ),
        ],
    )
    qa = compute_quality_assessment(
        solver_passed=True,
        shapes_analysis=sa,
        stage5_attempts_count=0,
        stage6_attempts_count=0,
        roletran_passed=True,
        has_cryptographic_primitives=True,
        security_findings=sec,
        final_spec=truncated_spec,
    )
    assert qa["quality_tier"] == "SILVER"
    assert any("INCOMPLETE_INITIATOR_TRACE" in a for a in qa["security_findings"]["vulnerabilities_and_anomalies"])





