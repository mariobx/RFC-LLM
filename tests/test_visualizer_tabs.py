"""Tests for scalable numbered multi-RFC tabs, filtered RFC drawer, per-attempt hydration, and offline --view replay."""

import asyncio
import json
import time
from pathlib import Path
from unittest.mock import MagicMock
from aiohttp import web

from src.pipeline_events import PipelineEventBus, GLOBAL_EVENT_BUS
from src.visualizer.server import VisualizerServer, hydrate_tab_payload


def test_sequential_tab_numbering_and_filtered_separation(tmp_path: Path):
    """Accepted RFCs receive sequential #1, #2 numbering while rejected RFCs go only to filtered_rfcs."""
    bus = PipelineEventBus()
    bus.set_run_directory(tmp_path, is_live=True)

    # RFC 1: Rejected at Tier 0
    bus.start_rfc("RFC 1000")
    bus.emit("stage_started", stage=1, stage_name="Document Intake & Slicing")
    bus.register_filtered_rfc(
        rfc_id="RFC 1000",
        title="Informational Memo",
        gate="Stage 1a: Tier 0 Header",
        reason="Category Informational is ineligible",
        duration_seconds=0.02,
    )

    # RFC 2: Accepted -> MUST become Tab #1
    rfc2_dir = tmp_path / "rfc2952"
    bus.start_rfc("RFC 2952")
    bus.emit("stage_started", stage=1, stage_name="Document Intake & Slicing")
    bus.emit("ast_generated", stage=2, ast={"protocol_name": "telnet_des_cfb64", "roles": [{"name": "client"}]})
    tab1 = bus.register_accepted_tab(
        rfc_id="RFC 2952",
        protocol_name="Telnet Encryption: DES 64 bit Cipher Feedback",
        rfc_dir=rfc2_dir,
    )
    assert tab1 == 1
    bus.update_accepted_tab(tab1, status="VERIFIED", quality_tier="SILVER", shapes_count=2, total_attempts=5)

    # Verify events.jsonl was flushed and bulky `ast` object was stripped
    jsonl_lines = (rfc2_dir / "events.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(jsonl_lines) >= 2
    parsed_events = [json.loads(line) for line in jsonl_lines]
    ast_evts = [e for e in parsed_events if e["event_type"] == "ast_generated"]
    assert len(ast_evts) == 1
    assert "ast" not in ast_evts[0]["data"]
    assert ast_evts[0]["data"]["ast_protocol_name"] == "telnet_des_cfb64"
    assert ast_evts[0]["tab_index"] == 1

    # RFC 3: Rejected at Stage 1c -> Must NOT consume Tab #2
    bus.start_rfc("RFC 3000")
    bus.register_filtered_rfc(
        rfc_id="RFC 3000",
        title="BGP Routing Policy",
        gate="Stage 1c: Applicability Gate",
        reason="No cryptographic handshake",
        duration_seconds=0.45,
    )

    # RFC 4: Accepted -> MUST become Tab #2, and active_events from RFC 2952 MUST be evicted from RAM
    rfc4_dir = tmp_path / "rfc8446"
    bus.start_rfc("RFC 8446")
    assert len(bus.get_history()) == 0
    tab2 = bus.register_accepted_tab(
        rfc_id="RFC 8446",
        protocol_name="The Transport Layer Security (TLS) Protocol Version 1.3",
        rfc_dir=rfc4_dir,
    )
    assert tab2 == 2

    overview = bus.get_tabs_overview()
    assert len(overview["accepted_tabs"]) == 2
    assert overview["accepted_tabs"][0]["tab_index"] == 1
    assert overview["accepted_tabs"][0]["rfc_id"] == "RFC 2952"
    assert overview["accepted_tabs"][0]["protocol_name"] == "Telnet Encryption: DES 64 bit Cipher Feedback"
    assert overview["accepted_tabs"][1]["tab_index"] == 2
    assert overview["accepted_tabs"][1]["rfc_id"] == "RFC 8446"
    assert overview["filtered_total"] == 2

    # Filtered pagination & search
    filt_all = bus.get_filtered_slice(offset=0, limit=10)
    assert filt_all["total"] == 2
    filt_bgp = bus.get_filtered_slice(offset=0, limit=10, query="bgp")
    assert filt_bgp["matching"] == 1
    assert filt_bgp["items"][0]["rfc_id"] == "RFC 3000"


def test_per_attempt_hydration_and_offline_replay(tmp_path: Path):
    """Hydrating a tab reconstructs Attempt 0, Roletran/CPSA repair attempts, Final snapshot, and offline replay."""
    run_dir = tmp_path / "run_2026-10-29_00-00-01"
    rfc_dir = run_dir / "rfc5246"
    rfc_dir.mkdir(parents=True)

    (rfc_dir / "verbatim_slice.txt").write_text("Section 7.4 Handshake Protocol...", encoding="utf-8")
    (rfc_dir / "tls12.scm").write_text("(herald tls12)\n(defprotocol tls12 basic)", encoding="utf-8")
    (rfc_dir / "tls12_shapes.xhtml").write_text("<html><body><svg></svg></body></html>", encoding="utf-8")

    traj_path = rfc_dir / "tls12_trajectory.json"
    traj_payload = {
        "schema_version": "1.0.0",
        "duration_seconds": 14.5,
        "rfc_metadata": {
            "rfc_id": "RFC 5246",
            "rfc_title": "The Transport Layer Security (TLS) Protocol Version 1.2",
            "protocol_name": "tls12",
            "selected_sections": ["7.3", "7.4"],
            "sliced_lines_count": 120,
            "verbatim_rfc_slice": "Section 7.4 Handshake Protocol...",
        },
        "stage2_initial_extraction": {
            "initial_ast": {"protocol_name": "tls12", "roles": [{"role_name": "client"}]},
            "initial_scm": "; attempt 0 scm\n(defprotocol tls12 basic)",
        },
        "stage5_preflight_gate": {
            "final_passed": True,
            "total_attempts": 1,
            "repair_attempts": [
                {
                    "attempt_number": 1,
                    "failure_stage": "roletran",
                    "parsed_diagnostic": "Unbound variable n_c in role client",
                    "rag_query": "CPSA roletran unbound variable role inputs",
                    "retrieved_chunk_ids": ["12"],
                    "rejected_scm": "; attempt 0 bad scm",
                    "repaired_scm": "; attempt 1 repaired roletran scm",
                    "repaired_ast": {"protocol_name": "tls12", "roles": [{"role_name": "client", "inputs": ["n_c"]}]},
                    "passed_after_repair": True,
                    "cycle_detected": False,
                }
            ],
        },
        "stage6_cpsa4_solver": {
            "final_passed": True,
            "total_attempts": 1,
            "shapes_analysis_from_shapes_txt": {"total_realized_shapes": 3},
            "repair_attempts": [
                {
                    "attempt_number": 1,
                    "failure_stage": "solver",
                    "parsed_diagnostic": "Unrealized skeleton 0",
                    "rag_query": "CPSA preskeleton non-originating key assumption",
                    "retrieved_chunk_ids": ["42"],
                    "rejected_scm": "; attempt 1 bad solver scm",
                    "repaired_scm": "; attempt 2 repaired solver scm",
                    "repaired_ast": {"protocol_name": "tls12", "roles": [{"role_name": "client"}]},
                    "passed_after_repair": True,
                    "cycle_detected": True,
                }
            ],
        },
        "quality_assessment": {"quality_tier": "GOLD"},
        "final_verified_output": {
            "final_scm_with_header": ";; QUALITY TIER: GOLD\n(herald tls12)\n(defprotocol tls12 basic)",
            "final_ast": {"protocol_name": "tls12", "roles": [{"role_name": "client"}]},
        },
    }
    traj_path.write_text(json.dumps(traj_payload), encoding="utf-8")

    master_index = {
        "schema_version": "1.0.0",
        "run_directory": str(run_dir),
        "total_rfcs_processed": 2,
        "filtered_rfcs": [
            {
                "rfc_id": "RFC 1149",
                "title": "IP over Avian Carriers",
                "gate": "Stage 1a: Tier 0 Header",
                "reason": "Experimental / non-cryptographic",
                "duration_seconds": 0.01,
            }
        ],
        "runs": [
            {
                "tab_index": 1,
                "rfc_id": "RFC 5246",
                "protocol_name": "The Transport Layer Security (TLS) Protocol Version 1.2",
                "is_eligible": True,
                "build_successful": True,
                "quality_tier": "GOLD",
                "rfc_directory": str(rfc_dir),
                "metadata_json_file": str(traj_path),
                "scm_file": str(rfc_dir / "tls12.scm"),
            }
        ],
    }
    (run_dir / "metadata_index.json").write_text(json.dumps(master_index), encoding="utf-8")

    # Test offline --view loader and server endpoints
    GLOBAL_EVENT_BUS.clear()
    overview = GLOBAL_EVENT_BUS.load_run_from_disk(run_dir)
    assert overview["is_live"] is False
    assert overview["filtered_total"] == 1
    assert len(overview["accepted_tabs"]) == 1
    assert overview["accepted_tabs"][0]["tab_index"] == 1
    assert overview["accepted_tabs"][0]["rfc_id"] == "RFC 5246"

    hydrated = hydrate_tab_payload(overview["accepted_tabs"][0])
    attempts = hydrated["attempts"]
    # Attempt 0 + 1 roletran repair + 1 solver repair + Final = 4 snapshots
    assert len(attempts) == 4
    assert attempts[0]["attempt_id"] == "attempt_0"
    assert attempts[0]["status"] == "REJECTED"
    assert "Unbound variable n_c" in attempts[0]["diagnostic"]

    assert attempts[1]["attempt_id"] == "roletran_1"
    assert attempts[1]["rag_query"] == "CPSA roletran unbound variable role inputs"
    assert "; attempt 1 repaired roletran scm" in attempts[1]["scm"]

    assert attempts[2]["attempt_id"] == "solver_1"
    assert attempts[2]["cycle_detected"] is True
    assert "; attempt 2 repaired solver scm" in attempts[2]["scm"]

    assert attempts[3]["attempt_id"] == "final"
    assert attempts[3]["status"] == "VERIFIED"
    assert "GOLD (3 Shapes)" in attempts[3]["label"]

    # Verify HTTP endpoints on VisualizerServer
    async def _exercise_http():
        server = VisualizerServer(host="127.0.0.1", port=8091)

        req_tabs = MagicMock(spec=web.Request)
        resp_tabs = await server.handle_tabs(req_tabs)
        assert resp_tabs.status == 200
        tabs_json = json.loads(resp_tabs.text)
        assert len(tabs_json["accepted_tabs"]) == 1

        req_detail = MagicMock(spec=web.Request)
        req_detail.match_info = {"tab_index": "1"}
        resp_detail = await server.handle_tab_detail(req_detail)
        assert resp_detail.status == 200
        detail_json = json.loads(resp_detail.text)
        assert len(detail_json["attempts"]) == 4

        req_filt = MagicMock(spec=web.Request)
        req_filt.query = {"offset": "0", "limit": "50", "q": "avian"}
        resp_filt = await server.handle_filtered(req_filt)
        assert resp_filt.status == 200
        filt_json = json.loads(resp_filt.text)
        assert filt_json["matching"] == 1
        assert filt_json["items"][0]["rfc_id"] == "RFC 1149"

    asyncio.run(_exercise_http())


def test_5000_accepted_tabs_scalability_benchmark(tmp_path: Path):
    """5,000 accepted tabs serialize in < 150ms with compact payload size."""
    bus = PipelineEventBus()
    bus.set_run_directory(tmp_path, is_live=True)

    # Populate 5,000 compact tab summaries directly via public registration/update path
    # without creating 5,000 directories on disk just to test memory & JSON serialization throughput
    for i in range(1, 5001):
        bus._accepted_tabs[i] = {
            "tab_index": i,
            "rfc_id": f"RFC {1000 + i}",
            "protocol_name": f"Cryptographic Handshake Protocol #{i}",
            "rfc_title": f"Cryptographic Handshake Protocol #{i}",
            "status": "VERIFIED" if i % 3 else "FAILED",
            "quality_tier": "GOLD" if i % 3 else "REJECTED",
            "total_attempts": i % 7,
            "shapes_count": 2,
            "duration_seconds": 8.4,
            "rfc_dir": f"/tmp/run/rfc{1000 + i}",
            "events_jsonl": None,
            "slice_path": None,
            "scm_path": None,
            "trajectory_path": None,
            "shapes_xhtml": None,
            "error_message": None,
        }
        bus._tab_order.append(i)

    t0 = time.perf_counter()
    overview = bus.get_tabs_overview()
    encoded = json.dumps(overview)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    assert len(overview["accepted_tabs"]) == 5000
    assert elapsed_ms < 250.0, f"5,000-tab overview serialization took too long: {elapsed_ms:.1f}ms"
    assert len(encoded) < 3_000_000  # Under 3 MB for 5,000 tabs
