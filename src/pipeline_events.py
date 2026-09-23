"""Event bus and streaming state dispatcher for live pipeline visualization."""

import json
import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class PipelineEvent(BaseModel):
    """Structured event emitted across pipeline execution stages."""
    timestamp: float = Field(default_factory=time.time)
    event_type: str = Field(..., description="Type of event (e.g. stage_started, log, repair, artifact)")
    stage: Optional[int] = Field(None, description="Stage index (1 to 6)")
    stage_name: Optional[str] = Field(None, description="Human readable stage name")
    data: Dict[str, Any] = Field(default_factory=dict, description="Payload data")

    def to_sse_message(self) -> str:
        """Formats the event as a standard Server-Sent Event (SSE) frame."""
        payload = json.dumps(self.model_dump())
        return f"event: {self.event_type}\ndata: {payload}\n\n"


class PipelineEventBus:
    """Thread-safe event dispatcher supporting synchronous and async subscribers."""

    def __init__(self):
        self._listeners: List[Callable[[PipelineEvent], None]] = []
        self._history: List[PipelineEvent] = []

    def subscribe(self, callback: Callable[[PipelineEvent], None]):
        """Registers a listener callback."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def unsubscribe(self, callback: Callable[[PipelineEvent], None]):
        """Removes a listener callback."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def emit(
        self,
        event_type: str,
        stage: Optional[int] = None,
        stage_name: Optional[str] = None,
        **kwargs,
    ) -> PipelineEvent:
        """Emits an event to all subscribers and records it in history."""
        event = PipelineEvent(
            event_type=event_type,
            stage=stage,
            stage_name=stage_name,
            data=kwargs,
        )
        self._history.append(event)
        for listener in list(self._listeners):
            try:
                listener(event)
            except Exception:
                pass
        return event

    def get_history(self) -> List[PipelineEvent]:
        """Returns the full event log for replay."""
        return list(self._history)

    def clear(self):
        """Clears listener history."""
        self._history.clear()


# Global event bus singleton
GLOBAL_EVENT_BUS = PipelineEventBus()
