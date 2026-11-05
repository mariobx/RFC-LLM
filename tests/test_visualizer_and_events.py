"""Unit and integration tests for Pipeline Event Bus, Cycle Detection, and Visualizer Server."""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import MagicMock
from aiohttp import web

from src.pipeline_events import GLOBAL_EVENT_BUS, PipelineEvent
from src.intermediate_representation.protocol_syntax_tree import (
    CPSAVariableDeclaration,
    CPSATraceEvent,
    CPSAProtocolRole,
    CPSAProtocolSpecification,
)
from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification
from src.visualizer.server import VisualizerServer


@pytest.fixture
def sample_spec() -> CPSAProtocolSpecification:
    return CPSAProtocolSpecification(
        protocol_name="cycle_proto",
        roles=[
            CPSAProtocolRole(
                role_name="r",
                variables=[
                    CPSAVariableDeclaration(name="ch", sort=CPSASortEnum.CHAN),
                    CPSAVariableDeclaration(name="x", sort=CPSASortEnum.TEXT),
                ],
                trace=[
                    CPSATraceEvent(direction="send", channel="ch", message_term="x"),
                ],
                inputs=["ch"],
                outputs=["x"],
            )
        ],
    )


def test_pipeline_event_bus_emission_and_subscription():
    """Event bus properly broadcasts events to listeners and maintains history."""
    received_events = []

    def listener(event: PipelineEvent):
        received_events.append(event)

    GLOBAL_EVENT_BUS.subscribe(listener)
    try:
        GLOBAL_EVENT_BUS.emit("stage_started", stage=1, test_key="test_value")

        assert len(received_events) >= 1
        last = received_events[-1]
        assert last.event_type == "stage_started"
        assert last.stage == 1
        assert last.data["test_key"] == "test_value"

        # Verify SSE message formatting
        sse = last.to_sse_message()
        assert "event: stage_started" in sse
        assert '"test_key": "test_value"' in sse
    finally:
        GLOBAL_EVENT_BUS.unsubscribe(listener)


def test_compiler_repair_cycle_detection_triggers_warning_and_jitter(monkeypatch, sample_spec: CPSAProtocolSpecification):
    """When cycle_detected=True, prompt receives oscillation warning and litellm receives higher temperature."""
    captured_kwargs = {}

    def mock_completion(**kwargs):
        captured_kwargs.update(kwargs)
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock(message=MagicMock(content=sample_spec.model_dump_json()))]
        return mock_resp

    monkeypatch.setattr("litellm.completion", mock_completion)

    repaired = repair_protocol_specification(
        failing_spec=sample_spec,
        error_diagnostic="Repeated syntax error",
        verbatim_slice="Sample RFC text",
        failure_stage="roletran",
        model="dummy_model",
        cycle_detected=True,
    )

    assert repaired is not None
    assert captured_kwargs.get("temperature", 0.0) >= 0.4
    prompt_content = captured_kwargs["messages"][1]["content"]
    assert "CRITICAL WARNING: An oscillation/cycle was detected" in prompt_content


def test_visualizer_server_endpoints(tmp_path: Path):
    """Visualizer web server serves history and artifact content."""
    async def _run():
        server = VisualizerServer(host="127.0.0.1", port=8089)

        # Emit test event
        GLOBAL_EVENT_BUS.emit("test_event", stage=4, detail="unit test")

        # Test history endpoint
        req = MagicMock(spec=web.Request)
        resp = await server.handle_history(req)
        assert resp.status == 200
        import json
        history = json.loads(resp.text)
        assert any(e["event_type"] == "test_event" for e in history)

    asyncio.run(_run())


def test_visualizer_remote_host_binding_and_relative_api_paths():
    """Verifies non-localhost Tailscale/LAN host detection and relative API paths in index.html for reverse proxies."""
    from src.pipeline import _is_localhost_binding
    from src.visualizer.server import HTML_TEMPLATE_PATH

    assert _is_localhost_binding("127.0.0.1") is True
    assert _is_localhost_binding("localhost") is True
    assert _is_localhost_binding("100.64.0.12") is False
    assert _is_localhost_binding("0.0.0.0") is False

    html = HTML_TEMPLATE_PATH.read_text(encoding="utf-8")
    assert "new EventSource('api/events')" in html
    assert "fetch('api/tabs')" in html
    assert "fetch('api/csv')" in html
    assert "fetch('/api/" not in html


def test_cli_resume_three_tier_resolution_and_overrides(tmp_path: Path, monkeypatch, capsys):
    """Tests -r / --resume: (1) empty output dir, (2) top-3 listing when .last_run missing, (3) .last_run & CLI overrides."""
    from src import pipeline

    out_dir = tmp_path / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    rfc_dir = tmp_path / "rfcs"
    rfc_dir.mkdir(parents=True, exist_ok=True)
    for num in (1001, 1002, 1003):
        (rfc_dir / f"rfc{num}.txt").write_text(f"Request for Comments: {num}\n", encoding="utf-8")

    # 1. No .last_run and no run_* directories -> explains -r is used after an initial run
    with pytest.raises(SystemExit) as exc1:
        pipeline.main(["-r", "-o", str(out_dir)])
    assert exc1.value.code == 0
    out1 = capsys.readouterr().out
    assert "No previous runs found" in out1
    assert "used after a first initial run" in out1

    # 2. Create 4 run_* directories without .last_run -> lists top 3 latest runs and prompts -r <folder_number>
    for idx, ts in enumerate(
        ("2026-11-01_10-00-00", "2026-11-02_10-00-00", "2026-11-03_10-00-00", "2026-11-04_10-00-00"),
        1,
    ):
        rdir = out_dir / f"run_{ts}"
        rdir.mkdir(parents=True, exist_ok=True)

    with pytest.raises(SystemExit) as exc2:
        pipeline.main(["-r", "-o", str(out_dir)])
    assert exc2.value.code == 0
    out2 = capsys.readouterr().out
    assert "Top 3 most recent runs available to resume" in out2
    assert "[1]" in out2 and "run_2026-11-04_10-00-00" in out2
    assert "[2]" in out2 and "run_2026-11-03_10-00-00" in out2
    assert "[3]" in out2 and "run_2026-11-02_10-00-00" in out2
    assert "run_2026-11-01_10-00-00" not in out2
    assert "re-run the command with -r <folder_number>" in out2

    # 3. Initial run writes output/.last_run (full expanded command with -r) and run_manifest.json
    latest_run = out_dir / "run_2026-11-04_10-00-00"
    parser = pipeline._build_parser()
    initial_args = parser.parse_args(
        [
            str(rfc_dir),
            "--model",
            "strata/unsloth-iq4_xs",
            "--host",
            "100.64.0.12",
            "--port",
            "8088",
            "--no-visualize",
        ]
    )
    planned = [rfc_dir / "rfc1001.txt", rfc_dir / "rfc1002.txt", rfc_dir / "rfc1003.txt"]
    manifest_path, last_run_file, cmd_str = pipeline._save_run_manifest_and_last_run(
        run_root_dir=latest_run,
        base_output_dir=out_dir,
        targets=[rfc_dir],
        args=initial_args,
        planned_rfc_files=planned,
    )
    assert last_run_file.exists()
    assert "./rfc-llm -r" in cmd_str
    assert "strata/unsloth-iq4_xs" in cmd_str
    assert "--host 100.64.0.12" in cmd_str
    assert "--port 8088" in cmd_str

    # Mark rfc1001 as already completed in latest_run/pipeline_runs.csv
    from src.logging_config import PipelineMetricsCSVLogger
    csv_logger = PipelineMetricsCSVLogger(csv_path=latest_run / "pipeline_runs.csv")
    csv_logger.log_run(rfc_id="RFC1001", is_eligible=False, status="INELIGIBLE", error_message="Ineligible")

    processed_calls = []

    def fake_run_pipeline(rfc_file_path, output_dir, router_model, extraction_model, repair_model, query_model, run_root_dir, csv_path, resume_checkpoint=False):
        processed_calls.append({
            "rfc_file": rfc_file_path.name,
            "model": extraction_model,
            "run_root_dir": run_root_dir,
            "resume_checkpoint": resume_checkpoint,
        })
        from src.main_pipeline_orchestrator import PipelineExecutionSummary
        return PipelineExecutionSummary(rfc_id=rfc_file_path.stem.upper(), is_eligible=False, error_message="Filtered")

    monkeypatch.setattr(pipeline, "run_rfc_translation_pipeline", fake_run_pipeline)

    # Resume using bare `-r` while overriding `--model` half-way through the run
    pipeline.main(["-r", "-o", str(out_dir), "--model", "gemini/gemini-2.5-pro"])

    assert [c["rfc_file"] for c in processed_calls] == ["rfc1002.txt", "rfc1003.txt"]
    assert all(c["model"] == "gemini/gemini-2.5-pro" for c in processed_calls)
    assert all(c["run_root_dir"] == latest_run.resolve() for c in processed_calls)
    assert all(c["resume_checkpoint"] is True for c in processed_calls)
    # Verify .last_run was updated with the new overridden model while preserving --host and --port
    updated_last_run = last_run_file.read_text(encoding="utf-8")
    assert "gemini/gemini-2.5-pro" in updated_last_run
    assert "100.64.0.12" in updated_last_run
    assert "8088" in updated_last_run

    # 4. Cross-PC portability: paths originating from another machine's directory structure rebase cleanly
    alien_rfc = "/Users/friend_box/projects/RFC-LLM/refrences/all_RFCs/rfc5246.txt"
    rebased = pipeline._resolve_portable_path(alien_rfc, base_dir=out_dir)
    if (pipeline.SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "all_RFCs" / "rfc5246.txt").exists():
        assert rebased == (pipeline.SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "all_RFCs" / "rfc5246.txt").resolve()
    alien_run = "/Users/friend_box/projects/RFC-LLM/output/run_2026-11-04_10-00-00"
    assert pipeline._resolve_portable_path(alien_run, base_dir=out_dir) == latest_run.resolve()
