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
    assert spec_scalars.timeout == 180
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
        assert models_payload["cpsa_timeout_seconds"] == 60
        assert "router_model" in models_payload

    asyncio.run(_exercise())
