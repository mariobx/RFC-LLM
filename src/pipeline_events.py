"""Bounded event bus, sequential tab registry, and disk telemetry sink for pipeline visualization."""

import json
import re
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class PipelineEvent(BaseModel):
    """Structured event emitted across pipeline execution stages."""
    timestamp: float = Field(default_factory=time.time)
    event_type: str = Field(..., description="Type of event (e.g. stage_started, repair_attempt, tab_accepted)")
    stage: Optional[int] = Field(None, description="Stage index (1 to 6)")
    stage_name: Optional[str] = Field(None, description="Human readable stage name")
    rfc_id: Optional[str] = Field(None, description="RFC identifier associated with this event")
    tab_index: Optional[int] = Field(None, description="Sequential 1-based tab number if RFC was accepted")
    data: Dict[str, Any] = Field(default_factory=dict, description="Payload data")

    def to_sse_message(self) -> str:
        """Formats the event as a standard Server-Sent Event (SSE) frame."""
        payload = json.dumps(self.model_dump())
        return f"event: {self.event_type}\ndata: {payload}\n\n"


def _strip_bulky_event_fields(event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Strips large AST blobs before writing compact event lines to events.jsonl
    (full per-attempt ASTs and .scm snapshots are already stored in <stem>_trajectory.json).
    """
    data = event_dict.get("data")
    if not isinstance(data, dict) or "ast" not in data:
        return event_dict
    slim_copy = dict(event_dict)
    slim_data = dict(data)
    ast_obj = slim_data.pop("ast", None)
    if isinstance(ast_obj, dict):
        slim_data["ast_protocol_name"] = ast_obj.get("protocol_name")
    slim_copy["data"] = slim_data
    return slim_copy


class PipelineEventBus:
    """Thread-safe, O(1)-RAM event dispatcher with sequential accepted-RFC tab indexing."""

    def __init__(self):
        self._lock = threading.RLock()
        self._listeners: List[Callable[[PipelineEvent], None]] = []
        # Bounded buffer: holds ONLY the currently executing RFC's events in RAM
        self._active_events: List[PipelineEvent] = []
        self._current_rfc_id: Optional[str] = None
        self._current_tab_index: Optional[int] = None
        self._current_events_jsonl: Optional[Path] = None

        # Run-level compact registries (~150 bytes per entry -> <1 MB for 5,000 RFCs)
        self._run_root_dir: Optional[Path] = None
        self._csv_path: Optional[Path] = None
        self._is_live: bool = True
        self._next_tab_index: int = 0
        self._accepted_tabs: Dict[int, Dict[str, Any]] = {}
        self._tab_order: List[int] = []
        self._filtered_rfcs: List[Dict[str, Any]] = []
        self._batch_cost_telemetry: Dict[str, Any] = {}

    def subscribe(self, callback: Callable[[PipelineEvent], None]):
        """Registers a listener callback."""
        with self._lock:
            if callback not in self._listeners:
                self._listeners.append(callback)

    def unsubscribe(self, callback: Callable[[PipelineEvent], None]):
        """Removes a listener callback."""
        with self._lock:
            if callback in self._listeners:
                self._listeners.remove(callback)

    def set_run_directory(
        self,
        run_root_dir: Path,
        is_live: bool = True,
        csv_path: Optional[Path] = None,
    ) -> None:
        """Binds the current run root directory and active CSV ledger path."""
        with self._lock:
            self._run_root_dir = run_root_dir.resolve()
            self._csv_path = (csv_path or (self._run_root_dir / "pipeline_runs.csv")).resolve()
            self._is_live = is_live

    def get_csv_path(self) -> Optional[Path]:
        """Returns the bound CSV path for the active or replayed run."""
        with self._lock:
            return self._csv_path

    def get_run_root_dir(self) -> Optional[Path]:
        """Returns the bound run root directory."""
        with self._lock:
            return self._run_root_dir

    def start_rfc(self, rfc_id: str, rfc_file: Optional[str] = None) -> None:
        """Evicts the completed RFC's in-memory event buffer and prepares for the next RFC."""
        with self._lock:
            self._active_events.clear()
            self._current_rfc_id = rfc_id
            self._current_tab_index = None
            self._current_events_jsonl = None
            self._is_live = True

    def register_accepted_tab(
        self,
        rfc_id: str,
        protocol_name: str,
        rfc_dir: Path,
        rfc_title: Optional[str] = None,
        intake_rationale: Optional[str] = None,
    ) -> int:
        """Allocates the next sequential 1-based tab number (#1, #2, ...) for an accepted RFC,
        binds its per-RFC events.jsonl sink, and flushes buffered Stage 1 events to disk.
        """
        with self._lock:
            self._next_tab_index += 1
            tab_idx = self._next_tab_index
            self._current_tab_index = tab_idx
            self._current_rfc_id = rfc_id

            resolved_dir = rfc_dir.resolve()
            resolved_dir.mkdir(parents=True, exist_ok=True)
            jsonl_path = resolved_dir / "events.jsonl"
            self._current_events_jsonl = jsonl_path

            tab_summary: Dict[str, Any] = {
                "tab_index": tab_idx,
                "rfc_id": rfc_id,
                "protocol_name": protocol_name,
                "rfc_title": rfc_title or protocol_name,
                "status": "RUNNING",
                "quality_tier": "PENDING",
                "total_attempts": 0,
                "shapes_count": 0,
                "duration_seconds": 0.0,
                "cost_usd": 0.0,
                "cost_telemetry": {},
                "rfc_dir": str(resolved_dir),
                "events_jsonl": str(jsonl_path),
                "slice_path": None,
                "scm_path": None,
                "trajectory_path": None,
                "shapes_xhtml": None,
                "error_message": None,
                "intake_rationale": intake_rationale,
                "security_findings": {},
            }
            self._accepted_tabs[tab_idx] = tab_summary
            self._tab_order.append(tab_idx)

            # Backfill tab_index onto buffered intake events and flush them to events.jsonl
            try:
                with open(jsonl_path, "w", encoding="utf-8") as handle:
                    for buffered_evt in self._active_events:
                        buffered_evt.tab_index = tab_idx
                        if not buffered_evt.rfc_id:
                            buffered_evt.rfc_id = rfc_id
                        slim = _strip_bulky_event_fields(buffered_evt.model_dump())
                        handle.write(json.dumps(slim) + "\n")
            except Exception:
                pass

        self.emit("tab_accepted", stage=1, tab=tab_summary)
        return tab_idx

    def update_accepted_tab(self, tab_index: int, **updates: Any) -> Optional[Dict[str, Any]]:
        """Updates metadata on an existing numbered tab and notifies connected clients."""
        with self._lock:
            tab = self._accepted_tabs.get(tab_index)
            if not tab:
                return None
            for k, v in updates.items():
                if v is not None or k in ("error_message",):
                    tab[k] = v
            snapshot = dict(tab)

        self.emit("tab_updated", tab=snapshot)
        return snapshot

    def register_filtered_rfc(
        self,
        rfc_id: str,
        title: str,
        gate: str,
        reason: str,
        duration_seconds: float = 0.0,
    ) -> Dict[str, Any]:
        """Records a disqualified/non-cryptographic RFC without allocating a numbered tab."""
        with self._lock:
            entry = {
                "index": len(self._filtered_rfcs) + 1,
                "rfc_id": rfc_id,
                "title": title or rfc_id,
                "gate": gate,
                "reason": reason,
                "duration_seconds": round(duration_seconds, 2),
                "timestamp": time.time(),
            }
            self._filtered_rfcs.append(entry)
            total = len(self._filtered_rfcs)

        self.emit("rfc_filtered", stage=1, filtered_total=total, entry=entry)
        return entry

    def emit(
        self,
        event_type: str,
        stage: Optional[int] = None,
        stage_name: Optional[str] = None,
        **kwargs,
    ) -> PipelineEvent:
        """Emits an event to all subscribers, stores it in the bounded active buffer, and appends to events.jsonl."""
        with self._lock:
            rfc_id = kwargs.get("rfc_id") or self._current_rfc_id
            tab_index = kwargs.get("tab_index") or self._current_tab_index
            event = PipelineEvent(
                event_type=event_type,
                stage=stage,
                stage_name=stage_name,
                rfc_id=rfc_id,
                tab_index=tab_index,
                data=kwargs,
            )
            if event_type == "cost_updated":
                if isinstance(kwargs.get("batch_cost"), dict):
                    self._batch_cost_telemetry = kwargs["batch_cost"]
                if tab_index and tab_index in self._accepted_tabs and isinstance(kwargs.get("rfc_cost"), dict):
                    self._accepted_tabs[tab_index]["cost_telemetry"] = kwargs["rfc_cost"]
                    self._accepted_tabs[tab_index]["cost_usd"] = round(
                        float(kwargs["rfc_cost"].get("total_cost_usd", 0.0)), 6
                    )

            # Meta-events for filtered RFCs don't need to bloat an accepted tab's buffer,
            # while active RFC progress events stay in the bounded buffer.
            if event_type != "rfc_filtered":
                self._active_events.append(event)

            jsonl_target = self._current_events_jsonl
            if jsonl_target and event_type not in ("rfc_filtered",):
                try:
                    slim = _strip_bulky_event_fields(event.model_dump())
                    with open(jsonl_target, "a", encoding="utf-8") as handle:
                        handle.write(json.dumps(slim) + "\n")
                except Exception:
                    pass

            listeners_snapshot = list(self._listeners)

        for listener in listeners_snapshot:
            try:
                listener(event)
            except Exception:
                pass
        return event

    def get_history(self) -> List[PipelineEvent]:
        """Returns the bounded event log for the currently active RFC."""
        with self._lock:
            return list(self._active_events)

    def get_active_state(self) -> Dict[str, Any]:
        """Returns active RFC identification and its bounded in-memory event stream."""
        with self._lock:
            return {
                "is_live": self._is_live,
                "rfc_id": self._current_rfc_id,
                "tab_index": self._current_tab_index,
                "events": [e.model_dump() for e in self._active_events],
            }

    def get_tabs_overview(self) -> Dict[str, Any]:
        """Returns the compact O(N) summary array (~150B/tab) for the virtualized tab strip."""
        with self._lock:
            tabs = [dict(self._accepted_tabs[idx]) for idx in self._tab_order if idx in self._accepted_tabs]
            return {
                "is_live": self._is_live,
                "run_directory": str(self._run_root_dir) if self._run_root_dir else None,
                "csv_path": str(self._csv_path) if self._csv_path else None,
                "active_rfc_id": self._current_rfc_id,
                "active_tab_index": self._current_tab_index,
                "accepted_tabs": tabs,
                "filtered_total": len(self._filtered_rfcs),
                "batch_cost_telemetry": self._batch_cost_telemetry,
            }

    def get_tab_summary(self, tab_index: int) -> Optional[Dict[str, Any]]:
        """Returns a single tab summary by 1-based index."""
        with self._lock:
            tab = self._accepted_tabs.get(tab_index)
            return dict(tab) if tab else None

    def get_filtered_slice(self, offset: int = 0, limit: int = 100, query: str = "") -> Dict[str, Any]:
        """Returns a paginated, optionally filtered slice of disqualified RFCs."""
        with self._lock:
            items = self._filtered_rfcs
            if query:
                q_low = query.lower().strip()
                items = [
                    it for it in items
                    if q_low in it.get("rfc_id", "").lower()
                    or q_low in it.get("title", "").lower()
                    or q_low in it.get("reason", "").lower()
                    or q_low in it.get("gate", "").lower()
                ]
            total_matching = len(items)
            sliced = items[max(0, offset) : max(0, offset) + max(1, min(limit, 500))]
            return {
                "total": len(self._filtered_rfcs),
                "matching": total_matching,
                "offset": offset,
                "limit": limit,
                "items": sliced,
            }

    def clear(self):
        """Resets all active and run-scoped event bus state."""
        with self._lock:
            self._active_events.clear()
            self._current_rfc_id = None
            self._current_tab_index = None
            self._current_events_jsonl = None
            self._run_root_dir = None
            self._csv_path = None
            self._is_live = True
            self._next_tab_index = 0
            self._accepted_tabs.clear()
            self._tab_order.clear()
            self._filtered_rfcs.clear()
            self._batch_cost_telemetry = {}

    def load_run_from_disk(self, target_path: Path) -> Dict[str, Any]:
        """Reconstructs numbered accepted tabs and filtered RFCs from an existing run directory,
        metadata_index.json, or single <protocol>_trajectory.json for offline `--view` replay.
        """
        resolved = target_path.resolve()
        with self._lock:
            self.clear()
            self._is_live = False

            index_file: Optional[Path] = None
            run_dir: Path = resolved

            if resolved.is_file():
                if resolved.name == "metadata_index.json":
                    index_file = resolved
                    run_dir = resolved.parent
                elif resolved.suffix.lower() == ".csv":
                    self._csv_path = resolved
                    run_dir = resolved.parent
                    if (run_dir / "metadata_index.json").exists():
                        index_file = run_dir / "metadata_index.json"
                elif resolved.name.endswith("_trajectory.json"):
                    run_dir = resolved.parent.parent
                    self._run_root_dir = run_dir
                    self._csv_path = (run_dir / "pipeline_runs.csv").resolve()
                    self._ingest_trajectory_as_tab(resolved, explicit_index=1)
                    return self.get_tabs_overview()
            elif resolved.is_dir():
                if (resolved / "metadata_index.json").exists():
                    index_file = resolved / "metadata_index.json"
                    run_dir = resolved
                else:
                    # Check if pointed directly at a single RFC output folder
                    trajs = sorted(resolved.glob("*_trajectory.json"))
                    if trajs:
                        self._run_root_dir = resolved.parent
                        self._csv_path = (resolved.parent / "pipeline_runs.csv").resolve()
                        for t_path in trajs:
                            self._ingest_trajectory_as_tab(t_path)
                        return self.get_tabs_overview()

            self._run_root_dir = run_dir
            if self._csv_path is None:
                self._csv_path = (run_dir / "pipeline_runs.csv").resolve()

            if index_file and index_file.exists():
                try:
                    idx_data = json.loads(index_file.read_text(encoding="utf-8"))
                except Exception:
                    idx_data = {}

                if isinstance(idx_data.get("batch_cost_telemetry"), dict):
                    self._batch_cost_telemetry = idx_data["batch_cost_telemetry"]

                # 1. Restore filtered/rejected RFC list if persisted
                for filt in idx_data.get("filtered_rfcs", []):
                    self._filtered_rfcs.append({
                        "index": len(self._filtered_rfcs) + 1,
                        "rfc_id": filt.get("rfc_id", "UNKNOWN"),
                        "title": filt.get("title") or filt.get("protocol_name") or filt.get("rfc_id", "Unknown"),
                        "gate": filt.get("gate", "Intake Gate"),
                        "reason": filt.get("reason") or filt.get("error_message") or "Filtered",
                        "duration_seconds": float(filt.get("duration_seconds", 0.0)),
                        "timestamp": 0.0,
                    })

                # Backward-compat: if older metadata_index.json only stored total_ineligible_filtered count
                persisted_ineligible_count = int(idx_data.get("total_ineligible_filtered", 0))
                if not self._filtered_rfcs and persisted_ineligible_count > 0:
                    self._filtered_rfcs.append({
                        "index": 1,
                        "rfc_id": f"{persisted_ineligible_count} RFCs",
                        "title": "Legacy Run Filtered Summary",
                        "gate": "Stage 1a / Stage 1c",
                        "reason": (
                            f"{persisted_ineligible_count} non-cryptographic RFC(s) were filtered prior to "
                            "detailed per-RFC filtered logging."
                        ),
                        "duration_seconds": 0.0,
                        "timestamp": 0.0,
                    })

                # 2. Restore accepted protocol tabs in exact run order
                runs_list = idx_data.get("runs", [])
                seen_dirs = set()
                for run_entry in runs_list:
                    if not run_entry.get("is_eligible", True):
                        self._filtered_rfcs.append({
                            "index": len(self._filtered_rfcs) + 1,
                            "rfc_id": run_entry.get("rfc_id", "UNKNOWN"),
                            "title": run_entry.get("protocol_name") or run_entry.get("rfc_id", "Unknown"),
                            "gate": "Intake Gate",
                            "reason": run_entry.get("error_message") or "Ineligible",
                            "duration_seconds": 0.0,
                            "timestamp": 0.0,
                        })
                        continue

                    rfc_dir_str = run_entry.get("rfc_directory")
                    traj_str = run_entry.get("metadata_json_file")
                    rfc_dir_path = Path(rfc_dir_str) if rfc_dir_str else None
                    if rfc_dir_path:
                        seen_dirs.add(str(rfc_dir_path.resolve()))
                    traj_path = Path(traj_str) if traj_str else None
                    if (not traj_path or not traj_path.exists()) and rfc_dir_path and rfc_dir_path.exists():
                        candidates = sorted(rfc_dir_path.glob("*_trajectory.json"))
                        if candidates:
                            traj_path = candidates[0]

                    if traj_path and traj_path.exists():
                        self._ingest_trajectory_as_tab(traj_path, fallback_entry=run_entry)
                    elif rfc_dir_path and rfc_dir_path.exists():
                        self._ingest_folder_without_trajectory(rfc_dir_path, fallback_entry=run_entry)

                # Also pick up any accepted RFC directories in run_dir that weren't flushed to metadata_index.json
                # (for example, if a batch run was interrupted with Ctrl+C mid-RFC)
                if run_dir.is_dir():
                    for child in sorted(run_dir.iterdir()):
                        if child.is_dir() and str(child.resolve()) not in seen_dirs:
                            trajs = sorted(child.glob("*_trajectory.json"))
                            if trajs:
                                self._ingest_trajectory_as_tab(trajs[0])
                            elif any(child.iterdir()):
                                self._ingest_folder_without_trajectory(child)
            elif run_dir.is_dir():
                for child in sorted(run_dir.iterdir()):
                    if child.is_dir():
                        trajs = sorted(child.glob("*_trajectory.json"))
                        if trajs:
                            self._ingest_trajectory_as_tab(trajs[0])

            return self.get_tabs_overview()

    def _ingest_trajectory_as_tab(
        self,
        traj_path: Path,
        fallback_entry: Optional[Dict[str, Any]] = None,
        explicit_index: Optional[int] = None,
    ) -> int:
        """Populates a numbered tab entry from a saved <stem>_trajectory.json file."""
        fallback_entry = fallback_entry or {}
        try:
            traj = json.loads(traj_path.read_text(encoding="utf-8"))
        except Exception:
            traj = {}

        rfc_dir = traj_path.parent.resolve()
        meta = traj.get("rfc_metadata", {})
        s5 = traj.get("stage5_preflight_gate", {})
        s6 = traj.get("stage6_cpsa4_solver", {})
        qa = traj.get("quality_assessment", {})

        self._next_tab_index = explicit_index if explicit_index else (self._next_tab_index + 1)
        tab_idx = self._next_tab_index

        rfc_id = meta.get("rfc_id") or fallback_entry.get("rfc_id") or rfc_dir.name.upper()
        proto_name = (
            meta.get("protocol_name")
            or fallback_entry.get("protocol_name")
            or traj_path.stem.replace("_trajectory", "")
        )
        rfc_title = meta.get("rfc_title") or fallback_entry.get("protocol_name") or proto_name
        quality_tier = qa.get("quality_tier") or fallback_entry.get("quality_tier") or "REJECTED"
        solver_passed = bool(s6.get("final_passed") or fallback_entry.get("build_successful"))
        roletran_passed = bool(s5.get("final_passed"))
        total_attempts = int(s5.get("total_attempts", 0)) + int(s6.get("total_attempts", 0))
        shapes_count = int(
            s6.get("shapes_analysis_from_shapes_txt", {}).get("total_realized_shapes", 0)
        )
        duration_sec = float(traj.get("duration_seconds", 0.0))

        scm_candidates = sorted(rfc_dir.glob("*.scm"))
        scm_path = str(scm_candidates[0]) if scm_candidates else fallback_entry.get("scm_file")
        shapes_candidates = sorted(rfc_dir.glob("*_shapes.xhtml"))
        shapes_xhtml = str(shapes_candidates[0]) if shapes_candidates else None
        slice_file = rfc_dir / "verbatim_slice.txt"
        events_jsonl = rfc_dir / "events.jsonl"

        if solver_passed:
            status = "VERIFIED"
        elif roletran_passed:
            status = "PARTIAL"
        else:
            status = "FAILED"

        cost_tel = traj.get("cost_telemetry") or fallback_entry.get("cost_telemetry") or {}
        cost_usd = round(
            float(cost_tel.get("total_cost_usd", fallback_entry.get("cost_usd", 0.0))), 6
        )
        if not self._batch_cost_telemetry and cost_tel:
            self._batch_cost_telemetry = cost_tel

        sec_findings = (
            traj.get("security_findings")
            or qa.get("security_findings")
            or fallback_entry.get("security_findings")
            or {}
        )
        intake_rationale = meta.get("intake_rationale") or fallback_entry.get("intake_rationale")

        tab_summary = {
            "tab_index": tab_idx,
            "rfc_id": rfc_id,
            "protocol_name": proto_name,
            "rfc_title": rfc_title,
            "status": status,
            "quality_tier": quality_tier,
            "total_attempts": total_attempts,
            "shapes_count": shapes_count,
            "duration_seconds": round(duration_sec, 2),
            "cost_usd": cost_usd,
            "cost_telemetry": cost_tel,
            "rfc_dir": str(rfc_dir),
            "events_jsonl": str(events_jsonl) if events_jsonl.exists() else None,
            "slice_path": str(slice_file) if slice_file.exists() else None,
            "scm_path": scm_path,
            "trajectory_path": str(traj_path.resolve()),
            "shapes_xhtml": shapes_xhtml,
            "error_message": fallback_entry.get("error_message"),
            "intake_rationale": intake_rationale,
            "security_findings": sec_findings,
        }
        self._accepted_tabs[tab_idx] = tab_summary
        self._tab_order.append(tab_idx)
        return tab_idx

    def _ingest_folder_without_trajectory(
        self,
        rfc_dir: Path,
        fallback_entry: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Handles an interrupted accepted RFC directory (e.g. Ctrl+C mid-extraction)."""
        fallback_entry = fallback_entry or {}
        resolved_dir = rfc_dir.resolve()
        self._next_tab_index += 1
        tab_idx = self._next_tab_index

        m = re.match(r"rfc(\d+)", resolved_dir.name.lower())
        inferred_rfc = f"RFC {m.group(1)}" if m else resolved_dir.name.upper()
        rfc_id = fallback_entry.get("rfc_id") or inferred_rfc
        proto_name = fallback_entry.get("protocol_name") or resolved_dir.name

        scm_candidates = sorted(resolved_dir.glob("*.scm"))
        shapes_candidates = sorted(resolved_dir.glob("*_shapes.xhtml"))
        slice_file = resolved_dir / "verbatim_slice.txt"
        events_jsonl = resolved_dir / "events.jsonl"

        tab_summary = {
            "tab_index": tab_idx,
            "rfc_id": rfc_id,
            "protocol_name": proto_name,
            "rfc_title": proto_name,
            "status": "VERIFIED" if shapes_candidates else "INTERRUPTED",
            "quality_tier": fallback_entry.get("quality_tier") or "INCOMPLETE",
            "total_attempts": 0,
            "shapes_count": 0,
            "duration_seconds": 0.0,
            "rfc_dir": str(resolved_dir),
            "events_jsonl": str(events_jsonl) if events_jsonl.exists() else None,
            "slice_path": str(slice_file) if slice_file.exists() else None,
            "scm_path": str(scm_candidates[0]) if scm_candidates else None,
            "trajectory_path": None,
            "shapes_xhtml": str(shapes_candidates[0]) if shapes_candidates else None,
            "error_message": fallback_entry.get("error_message") or "Interrupted before trajectory export",
            "intake_rationale": fallback_entry.get("intake_rationale"),
            "security_findings": fallback_entry.get("security_findings") or {},
        }
        self._accepted_tabs[tab_idx] = tab_summary
        self._tab_order.append(tab_idx)
        return tab_idx


# Global event bus singleton
GLOBAL_EVENT_BUS = PipelineEventBus()
