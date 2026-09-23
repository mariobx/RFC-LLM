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
    assert captured_kwargs.get("temperature") == 0.4
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
