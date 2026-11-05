"""Asynchronous web server for live and offline multi-RFC synthesis visualization."""

import asyncio
import csv
import json
import logging
import socket
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from aiohttp import web

from src.logging_config import PipelineMetricsCSVLogger
from src.pipeline_events import GLOBAL_EVENT_BUS, PipelineEvent
from src.system_config import SYSTEM_CONFIG
from src.verification_engine.trajectory_metadata_exporter import compute_security_findings

logger = logging.getLogger("rfc_llm.visualizer")

HTML_TEMPLATE_PATH = Path(__file__).parent / "static" / "index.html"

# Lazy lightweight chunk-id -> {title, source_file, snippet} lookup cache for offline hydration
_MANUAL_CHUNK_LOOKUP: Optional[Dict[str, Dict[str, str]]] = None


def _get_manual_chunk_lookup() -> Dict[str, Dict[str, str]]:
    """Loads compact section/example metadata from `refrences/cpsa_kb/kb_index.json`
    (plus legacy `manual_chunks.jsonl` if present) for offline RAG card hydration.
    """
    global _MANUAL_CHUNK_LOOKUP
    if _MANUAL_CHUNK_LOOKUP is not None:
        return _MANUAL_CHUNK_LOOKUP

    lookup: Dict[str, Dict[str, str]] = {}
    kb_index_path = SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "cpsa_kb" / "kb_index.json"
    if kb_index_path.exists():
        try:
            kb_data = json.loads(kb_index_path.read_text(encoding="utf-8", errors="ignore"))
            for sec in kb_data.get("sections", []):
                sid = str(sec.get("section_id") or "")
                if sid:
                    txt = sec.get("content") or ""
                    lookup[sid] = {
                        "chunk_id": sid,
                        "title": sec.get("title") or sid,
                        "source_file": sec.get("source_file") or "CPSA Knowledge Base",
                        "snippet": txt[:280].strip() + ("..." if len(txt) > 280 else ""),
                    }
            for ex in kb_data.get("scm_examples", []):
                ex_id = str(ex.get("example_id") or "")
                if ex_id:
                    lookup[ex_id] = {
                        "chunk_id": ex_id,
                        "title": f"MITRE Example: {ex.get('filename')} ({ex.get('algebra', 'basic')})",
                        "source_file": ex_id,
                        "snippet": ex.get("summary") or "",
                    }
        except Exception:
            pass

    jsonl_path = SYSTEM_CONFIG.CHUNKS_DIR / "manual_chunks.jsonl"
    if jsonl_path.exists():
        try:
            with open(jsonl_path, "r", encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    cid = str(obj.get("chunk_id") or obj.get("id") or "")
                    if cid and cid not in lookup:
                        txt = obj.get("text") or obj.get("content") or ""
                        lookup[cid] = {
                            "chunk_id": cid,
                            "title": obj.get("title") or obj.get("breadcrumb") or f"Chunk #{cid}",
                            "source_file": obj.get("source_file") or "MITRE Manual",
                            "snippet": txt[:280].strip() + ("..." if len(txt) > 280 else ""),
                        }
        except Exception:
            pass
    _MANUAL_CHUNK_LOOKUP = lookup
    return lookup


def _resolve_chunks_by_ids(chunk_ids: List[Any]) -> List[Dict[str, str]]:
    lookup = _get_manual_chunk_lookup()
    resolved = []
    for raw_id in chunk_ids or []:
        cid = str(raw_id)
        if cid in lookup:
            resolved.append(lookup[cid])
        else:
            resolved.append({
                "chunk_id": cid,
                "title": f"MITRE CPSA Manual Chunk #{cid}",
                "source_file": "manual_chunks.jsonl",
                "snippet": "",
            })
    return resolved


def hydrate_tab_payload(tab_summary: Dict[str, Any]) -> Dict[str, Any]:
    """Hydrates a single numbered RFC tab on demand from disk (<rfc_dir>/events.jsonl + <stem>_trajectory.json)."""
    rfc_dir = Path(tab_summary["rfc_dir"]) if tab_summary.get("rfc_dir") else None
    traj_path = Path(tab_summary["trajectory_path"]) if tab_summary.get("trajectory_path") else None
    if (not traj_path or not traj_path.exists()) and rfc_dir and rfc_dir.exists():
        candidates = sorted(rfc_dir.glob("*_trajectory.json"))
        if candidates:
            traj_path = candidates[0]

    traj: Dict[str, Any] = {}
    if traj_path and traj_path.exists():
        try:
            traj = json.loads(traj_path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            traj = {}

    meta = traj.get("rfc_metadata", {})
    s2 = traj.get("stage2_initial_extraction", {})
    s5 = traj.get("stage5_preflight_gate", {})
    s6 = traj.get("stage6_cpsa4_solver", {})
    qa = traj.get("quality_assessment", {})
    final_out = traj.get("final_verified_output", {})

    # 1. Verbatim RFC Slice
    verbatim_slice = meta.get("verbatim_rfc_slice") or ""
    if not verbatim_slice and rfc_dir and (rfc_dir / "verbatim_slice.txt").exists():
        verbatim_slice = (rfc_dir / "verbatim_slice.txt").read_text(encoding="utf-8", errors="ignore")

    # Load Chronological Events early so we can reconstruct in-flight attempts for RUNNING tabs
    events: List[Dict[str, Any]] = []
    events_jsonl_path = (
        Path(tab_summary["events_jsonl"])
        if tab_summary.get("events_jsonl")
        else (rfc_dir / "events.jsonl" if rfc_dir else None)
    )
    if events_jsonl_path and events_jsonl_path.exists():
        try:
            with open(events_jsonl_path, "r", encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    line = line.strip()
                    if line:
                        events.append(json.loads(line))
        except Exception:
            events = []

    active_state = GLOBAL_EVENT_BUS.get_active_state()
    if active_state.get("tab_index") == tab_summary.get("tab_index") and active_state.get("events"):
        if not events:
            events = active_state["events"]

    # 2. Build Ordered Per-Attempt Time-Travel Snapshots
    attempts: List[Dict[str, Any]] = []
    s5_repairs = s5.get("repair_attempts") or []
    s6_repairs = s6.get("repair_attempts") or []

    initial_ast = s2.get("initial_ast")
    initial_scm = s2.get("initial_scm")
    if not initial_scm and s5_repairs:
        initial_scm = s5_repairs[0].get("rejected_scm")
    if not initial_scm and s6_repairs:
        initial_scm = s6_repairs[0].get("rejected_scm")

    # If trajectory.json is not written yet (e.g. tab is RUNNING), recover latest AST/.scm from live events
    is_running_tab = (tab_summary.get("status") == "RUNNING") and not traj
    if not initial_ast and events:
        for evt in events:
            if evt.get("event_type") == "stage_completed" and evt.get("stage") == 2:
                initial_ast = (evt.get("data") or {}).get("ast")
                break
    if not initial_scm and tab_summary.get("scm_path") and Path(tab_summary["scm_path"]).exists():
        initial_scm = Path(tab_summary["scm_path"]).read_text(encoding="utf-8", errors="ignore")

    # Determine whether Attempt 0 passed directly or what diagnostic rejected it
    attempt0_diag: Optional[str] = None
    if s5_repairs:
        attempt0_diag = s5_repairs[0].get("parsed_diagnostic") or s5_repairs[0].get("raw_stderr")
        attempt0_status = "REJECTED"
    elif s6_repairs:
        attempt0_diag = s6_repairs[0].get("parsed_diagnostic") or s6_repairs[0].get("raw_stderr")
        attempt0_status = "REJECTED"
    elif s2.get("schema_validation_error") and not initial_ast:
        attempt0_diag = s2.get("schema_validation_error")
        attempt0_status = "FAILED"
    elif s6.get("final_passed"):
        attempt0_status = "PASSED"
    elif initial_ast or initial_scm:
        attempt0_diag = tab_summary.get("error_message")
        attempt0_status = "GENERATED"
    elif is_running_tab:
        attempt0_diag = "Stage 2 JSON CPSA synthesis currently in progress..."
        attempt0_status = "GENERATED"
    else:
        attempt0_diag = tab_summary.get("error_message") or "Initial JSON extraction did not complete."
        attempt0_status = "FAILED"

    attempts.append({
        "attempt_number": 0,
        "attempt_id": "attempt_0",
        "label": "Attempt 0 | Initial",
        "stage": "Stage 2/3: Initial JSON & .scm Synthesis",
        "status": attempt0_status,
        "cycle_detected": False,
        "scm": initial_scm or "; Synthesizing initial .scm model...",
        "ast": initial_ast,
        "diagnostic": attempt0_diag,
        "rag_query": None,
        "retrieved_chunks": [],
    })

    seq_num = 0
    for idx, rep in enumerate(s5_repairs):
        seq_num += 1
        # Diagnostic that this repair produced on the NEXT check (if another repair followed)
        next_diag = None
        if not rep.get("passed_after_repair"):
            if idx + 1 < len(s5_repairs):
                next_diag = s5_repairs[idx + 1].get("parsed_diagnostic")
            elif rep.get("repair_exception"):
                next_diag = rep.get("repair_exception")
        attempts.append({
            "attempt_number": seq_num,
            "attempt_id": f"roletran_{rep.get('attempt_number', idx + 1)}",
            "label": f"Attempt {seq_num} | Roletran Repair",
            "stage": f"Stage 5: Roletran Self-Healing (#{rep.get('attempt_number', idx + 1)})",
            "status": "PASSED" if rep.get("passed_after_repair") else "REJECTED",
            "cycle_detected": bool(rep.get("cycle_detected", False)),
            "scm": rep.get("repaired_scm") or rep.get("rejected_scm") or "; Repair failed to emit .scm",
            "rejected_scm": rep.get("rejected_scm"),
            "ast": rep.get("repaired_ast") or rep.get("rejected_ast"),
            "trigger_diagnostic": rep.get("parsed_diagnostic") or rep.get("raw_stderr"),
            "diagnostic": rep.get("parsed_diagnostic") or rep.get("repair_exception") or next_diag,
            "rag_query": rep.get("rag_query"),
            "searcher_diagnosis": rep.get("searcher_diagnosis"),
            "searcher_turns": rep.get("searcher_turns") or [],
            "retrieved_chunks": _resolve_chunks_by_ids(rep.get("retrieved_chunk_ids", [])),
        })

    for idx, rep in enumerate(s6_repairs):
        seq_num += 1
        attempts.append({
            "attempt_number": seq_num,
            "attempt_id": f"solver_{rep.get('attempt_number', idx + 1)}",
            "label": f"Attempt {seq_num} | CPSA Repair",
            "stage": f"Stage 6: CPSA Compilation Self-Healing (#{rep.get('attempt_number', idx + 1)})",
            "status": "PASSED" if rep.get("passed_after_repair") else "REJECTED",
            "cycle_detected": bool(rep.get("cycle_detected", False)),
            "scm": rep.get("repaired_scm") or rep.get("rejected_scm") or "; Repair failed to emit .scm",
            "rejected_scm": rep.get("rejected_scm"),
            "ast": rep.get("repaired_ast") or rep.get("rejected_ast"),
            "trigger_diagnostic": rep.get("parsed_diagnostic") or rep.get("raw_stderr"),
            "diagnostic": rep.get("parsed_diagnostic") or rep.get("repair_exception") or rep.get("raw_stderr"),
            "rag_query": rep.get("rag_query"),
            "searcher_diagnosis": rep.get("searcher_diagnosis"),
            "searcher_turns": rep.get("searcher_turns") or [],
            "retrieved_chunks": _resolve_chunks_by_ids(rep.get("retrieved_chunk_ids", [])),
        })

    # Reconstruct in-progress repair attempts from live events if trajectory.json is not finalized yet
    if is_running_tab and events:
        latest_ast = initial_ast
        for evt in events:
            et = evt.get("event_type")
            ed = evt.get("data") or {}
            if et == "stage_completed" and evt.get("stage") == 3 and ed.get("ast"):
                latest_ast = ed.get("ast")
            elif et == "repair_attempt":
                seq_num += 1
                stg = evt.get("stage", 5)
                att_n = ed.get("attempt", seq_num)
                attempts.append({
                    "attempt_number": seq_num,
                    "attempt_id": f"live_repair_{seq_num}",
                    "label": f"Attempt {seq_num} | {'Roletran' if stg == 5 else 'CPSA'} Repair",
                    "stage": f"Stage {stg}: Live Self-Healing (#{att_n})",
                    "status": "GENERATED",
                    "cycle_detected": bool(ed.get("cycle_detected", False)),
                    "scm": initial_scm or "; Repair in progress...",
                    "ast": latest_ast,
                    "diagnostic": ed.get("diagnostic"),
                    "rag_query": None,
                    "retrieved_chunks": [],
                })

    final_scm = final_out.get("final_scm_with_header")
    final_ast = final_out.get("final_ast")
    if not is_running_tab and not final_scm and tab_summary.get("scm_path") and Path(tab_summary["scm_path"]).exists():
        final_scm = Path(tab_summary["scm_path"]).read_text(encoding="utf-8", errors="ignore")

    if not is_running_tab and (final_scm or final_ast):
        tier = qa.get("quality_tier") or tab_summary.get("quality_tier") or "REJECTED"
        shapes_n = int(
            s6.get("shapes_analysis_from_shapes_txt", {}).get(
                "total_realized_shapes", tab_summary.get("shapes_count", 0)
            )
        )
        solver_ok = bool(s6.get("final_passed") or tab_summary.get("status") == "VERIFIED")
        final_label = f"Final | {tier} ({shapes_n} Shapes)" if solver_ok else f"Final | {tier}"
        attempts.append({
            "attempt_number": seq_num + 1,
            "attempt_id": "final",
            "label": final_label,
            "stage": "Final Synthesized Artifact",
            "status": "VERIFIED" if solver_ok else "FAILED",
            "cycle_detected": False,
            "scm": final_scm or "; No final .scm file.",
            "ast": final_ast,
            "diagnostic": None if solver_ok else tab_summary.get("error_message"),
            "rag_query": None,
            "retrieved_chunks": [],
        })

    if not events:
        events = _synthesize_events_from_trajectory(tab_summary, traj, attempts)

    shapes_xhtml = tab_summary.get("shapes_xhtml")
    if not shapes_xhtml and rfc_dir and rfc_dir.exists():
        xhtmls = sorted(rfc_dir.glob("*_shapes.xhtml"))
        if xhtmls:
            shapes_xhtml = str(xhtmls[0])

    cost_telemetry = traj.get("cost_telemetry") or tab_summary.get("cost_telemetry") or {}
    if not cost_telemetry and events:
        for evt in reversed(events):
            if evt.get("event_type") == "cost_updated":
                rc = (evt.get("data") or {}).get("rfc_cost")
                if isinstance(rc, dict):
                    cost_telemetry = rc
                    break

    sec_findings = (
        traj.get("security_findings")
        or qa.get("security_findings")
        or tab_summary.get("security_findings")
        or {}
    )
    if not sec_findings and traj:
        try:
            sec_findings = compute_security_findings(
                shapes_analysis=s6.get("shapes_analysis_from_shapes_txt") or {},
                exploration_telemetry=s6.get("exploration_telemetry_from_txt") or {},
                sas_formulas=final_out.get("shape_analysis_sentences") or [],
            )
        except Exception:
            sec_findings = {}

    intake_rationale = (
        meta.get("intake_rationale")
        or tab_summary.get("intake_rationale")
        or None
    )
    if not intake_rationale:
        err_msg = tab_summary.get("error_message") or ""
        if "Eligible:" in err_msg:
            intake_rationale = err_msg.split("Eligible:", 1)[1].strip()

    return {
        "tab": {
            **tab_summary,
            "shapes_xhtml": shapes_xhtml,
            "security_findings": sec_findings,
            "intake_rationale": intake_rationale,
        },
        "rfc_metadata": meta,
        "intake_rationale": intake_rationale,
        "quality_assessment": qa,
        "security_findings": sec_findings,
        "shapes_analysis": s6.get("shapes_analysis_from_shapes_txt") or {},
        "exploration_telemetry": s6.get("exploration_telemetry_from_txt") or {},
        "cost_telemetry": cost_telemetry,
        "verbatim_slice": verbatim_slice,
        "shapes_xhtml": shapes_xhtml,
        "attempts": attempts,
        "events": events,
    }


def _synthesize_events_from_trajectory(
    tab_summary: Dict[str, Any],
    traj: Dict[str, Any],
    attempts: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Synthesizes clean replay events and RAG cards for legacy runs created prior to events.jsonl."""
    base_ts = time.time()
    evts: List[Dict[str, Any]] = []
    meta = traj.get("rfc_metadata", {})
    s2 = traj.get("stage2_initial_extraction", {})
    s5 = traj.get("stage5_preflight_gate", {})
    s6 = traj.get("stage6_cpsa4_solver", {})
    tab_idx = tab_summary.get("tab_index")
    rfc_id = tab_summary.get("rfc_id")

    def _push(offset: float, etype: str, stage: Optional[int], data: Dict[str, Any]):
        evts.append({
            "timestamp": base_ts + offset,
            "event_type": etype,
            "stage": stage,
            "stage_name": None,
            "rfc_id": rfc_id,
            "tab_index": tab_idx,
            "data": data,
        })

    _push(0.0, "pipeline_started", 1, {"rfc_id": rfc_id, "rfc_file": rfc_id})
    _push(0.1, "stage_completed", 1, {"protocol_name": tab_summary.get("protocol_name")})
    if meta.get("selected_sections"):
        _push(0.2, "slice_ready", 1, {
            "sections": meta.get("selected_sections", []),
            "line_count": meta.get("sliced_lines_count", 0),
        })

    if s2.get("initial_ast"):
        _push(0.3, "stage_completed", 2, {
            "roles_count": len(s2["initial_ast"].get("roles", [])),
            "skeletons_count": len(s2["initial_ast"].get("skeletons", [])),
        })
        _push(0.4, "stage_completed", 3, {"scm_path": tab_summary.get("scm_path")})
    else:
        err = s2.get("schema_validation_error") or tab_summary.get("error_message") or "Extraction failed"
        _push(0.3, "stage_failed", 2, {"error_message": err})
        _push(0.4, "pipeline_failed", 2, {"error_message": err})
        return evts

    t_off = 0.5
    for att in attempts:
        if att["attempt_id"] in ("attempt_0", "final"):
            continue
        is_roletran = att["attempt_id"].startswith("roletran_")
        st_num = 5 if is_roletran else 6
        if att.get("rag_query") or att.get("retrieved_chunks") or att.get("searcher_turns"):
            _push(t_off, "rag_retrieval", st_num, {
                "purpose": att["stage"],
                "query": att.get("rag_query") or "",
                "searcher_diagnosis": att.get("searcher_diagnosis"),
                "searcher_turns": att.get("searcher_turns") or [],
                "chunks": att.get("retrieved_chunks") or [],
            })
            t_off += 0.05
        _push(t_off, "repair_attempt", st_num, {
            "attempt": att["attempt_number"],
            "max_attempts": SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS,
            "diagnostic": att.get("diagnostic") or "",
            "cycle_detected": att.get("cycle_detected", False),
        })
        t_off += 0.05

    if s5.get("final_passed"):
        _push(t_off, "stage_completed", 4, {"status": "passed"})
        _push(t_off + 0.02, "stage_completed", 5, {"status": "passed", "attempts": s5.get("total_attempts", 0)})
    else:
        _push(t_off, "stage_failed", 5, {"reason": "Roletran executability unfulfilled"})

    if s6.get("final_passed") or tab_summary.get("status") == "VERIFIED":
        _push(t_off + 0.1, "pipeline_completed", 6, {
            "success": True,
            "protocol_name": tab_summary.get("protocol_name"),
            "shapes_count": tab_summary.get("shapes_count", 0),
            "quality_tier": tab_summary.get("quality_tier"),
            "shapes_xhtml": tab_summary.get("shapes_xhtml"),
        })
    else:
        _push(t_off + 0.1, "stage_failed", 6, {"error_message": tab_summary.get("error_message")})
        _push(t_off + 0.12, "pipeline_failed", 6, {"error_message": tab_summary.get("error_message")})

    return evts


def _load_csv_analytics_payload() -> Dict[str, Any]:
    """Reads and normalizes the active run's 67-column pipeline_runs.csv off the main thread.
    If viewing a legacy run directory that only has metadata_index.json (no pipeline_runs.csv yet),
    reconstructs the 67-column rows from metadata_index.json + trajectory JSONs.
    """
    headers = list(PipelineMetricsCSVLogger.CSV_HEADER)
    csv_path = GLOBAL_EVENT_BUS.get_csv_path()
    run_dir = GLOBAL_EVENT_BUS.get_run_root_dir()

    target_csv: Optional[Path] = None
    if csv_path and csv_path.exists() and csv_path.stat().st_size > 0:
        target_csv = csv_path
    elif run_dir and (run_dir / "pipeline_runs.csv").exists() and (run_dir / "pipeline_runs.csv").stat().st_size > 0:
        target_csv = run_dir / "pipeline_runs.csv"

    rows: List[Dict[str, str]] = []
    if target_csv and target_csv.exists():
        try:
            with open(target_csv, mode="r", newline="", encoding="utf-8", errors="ignore") as handle:
                reader = csv.DictReader(handle)
                for raw_row in reader:
                    normalized = {col: str(raw_row.get(col) or "") for col in headers}
                    rows.append(normalized)
        except Exception:
            rows = []

    # If CSV has 0 rows (e.g., offline --view on a legacy run folder with metadata_index.json),
    # reconstruct rows from metadata_index.json into run_dir/pipeline_runs.csv
    if not rows and run_dir and (run_dir / "metadata_index.json").exists():
        try:
            generated_csv = run_dir / "pipeline_runs.csv"
            temp_logger = PipelineMetricsCSVLogger(csv_path=generated_csv)
            temp_logger.seed_from_source(run_dir / "metadata_index.json")
            target_csv = generated_csv
            with open(generated_csv, mode="r", newline="", encoding="utf-8", errors="ignore") as handle:
                reader = csv.DictReader(handle)
                for raw_row in reader:
                    normalized = {col: str(raw_row.get(col) or "") for col in headers}
                    rows.append(normalized)
        except Exception:
            rows = []

    return {
        "csv_path": str(target_csv or csv_path or ""),
        "headers": headers,
        "row_count": len(rows),
        "rows": rows,
    }


class VisualizerServer:
    """Manages SSE streaming, lazy per-tab hydration, and dashboard state."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self._sse_clients: Set[asyncio.Queue] = set()
        self._setup_routes()

        # Connect event bus to SSE clients
        GLOBAL_EVENT_BUS.subscribe(self._on_bus_event)

    def _setup_routes(self):
        self.app.router.add_get("/", self.handle_index)
        self.app.router.add_get("/api/events", self.handle_sse)
        self.app.router.add_get("/api/history", self.handle_history)
        self.app.router.add_get("/api/tabs", self.handle_tabs)
        self.app.router.add_get("/api/active", self.handle_active)
        self.app.router.add_get("/api/tab/{tab_index}", self.handle_tab_detail)
        self.app.router.add_get("/api/filtered", self.handle_filtered)
        self.app.router.add_get("/api/csv", self.handle_csv)
        self.app.router.add_get("/api/models", self.handle_models)
        self.app.router.add_get("/api/artifact", self.handle_artifact)
        if SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR.exists():
            self.app.router.add_static("/output", SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR, show_index=True)

    async def handle_csv(self, request: web.Request) -> web.Response:
        """Reads and parses the active run's 67-column CSV ledger in a worker thread off the main event loop."""
        payload = await asyncio.to_thread(_load_csv_analytics_payload)
        return web.json_response(payload)

    async def handle_models(self, request: web.Request) -> web.Response:
        """Returns the live stage-specific models resolved from prompts/*.md frontmatter."""
        return web.json_response({
            "router_model": SYSTEM_CONFIG.DEFAULT_ROUTER_MODEL,
            "section_router_model": SYSTEM_CONFIG.DEFAULT_SECTION_ROUTER_MODEL,
            "extraction_model": SYSTEM_CONFIG.DEFAULT_EXTRACTION_MODEL,
            "correction_model": SYSTEM_CONFIG.DEFAULT_CORRECTION_MODEL,
            "repair_model": SYSTEM_CONFIG.DEFAULT_REPAIR_MODEL,
            "query_model": SYSTEM_CONFIG.DEFAULT_QUERY_MODEL,
            "think_model": SYSTEM_CONFIG.DEFAULT_THINK_MODEL,
            "cpsa_timeout_seconds": SYSTEM_CONFIG.CPSA_TIMEOUT_SECONDS,
        })

    async def handle_tabs(self, request: web.Request) -> web.Response:
        """Returns the compact O(N) tab summary list and filtered count."""
        return web.json_response(GLOBAL_EVENT_BUS.get_tabs_overview())

    async def handle_active(self, request: web.Request) -> web.Response:
        """Returns the bounded in-memory event stream for the currently running RFC only."""
        return web.json_response(GLOBAL_EVENT_BUS.get_active_state())

    async def handle_tab_detail(self, request: web.Request) -> web.Response:
        """Hydrates a numbered tab (#1..#N) on demand from disk JSON artifacts."""
        raw_idx = request.match_info.get("tab_index", "")
        try:
            tab_idx = int(raw_idx)
        except ValueError:
            return web.json_response({"error": f"Invalid tab_index: {raw_idx}"}, status=400)

        tab_summary = GLOBAL_EVENT_BUS.get_tab_summary(tab_idx)
        if not tab_summary:
            return web.json_response({"error": f"Tab #{tab_idx} not found"}, status=404)

        payload = hydrate_tab_payload(tab_summary)
        return web.json_response(payload)

    async def handle_filtered(self, request: web.Request) -> web.Response:
        """Returns paginated disqualified/filtered RFCs for the collapsible drawer."""
        try:
            offset = int(request.query.get("offset", "0"))
        except ValueError:
            offset = 0
        try:
            limit = int(request.query.get("limit", "100"))
        except ValueError:
            limit = 100
        query = request.query.get("q", "")
        return web.json_response(GLOBAL_EVENT_BUS.get_filtered_slice(offset=offset, limit=limit, query=query))

    def _on_bus_event(self, event: PipelineEvent):
        """Dispatches an event from the pipeline event bus to all connected web clients thread-safely."""
        if hasattr(self, "loop") and self.loop and self.loop.is_running():
            for q in list(self._sse_clients):
                try:
                    self.loop.call_soon_threadsafe(q.put_nowait, event)
                except Exception:
                    pass
        else:
            for q in list(self._sse_clients):
                try:
                    q.put_nowait(event)
                except Exception:
                    pass

    async def handle_index(self, request: web.Request) -> web.Response:
        """Serves the main single-page visualizer dashboard."""
        if not HTML_TEMPLATE_PATH.exists():
            return web.Response(text="Dashboard template not found.", status=404)
        with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return web.Response(text=content, content_type="text/html")

    async def handle_history(self, request: web.Request) -> web.Response:
        """Returns JSON array of active RFC events (bounded)."""
        history = [e.model_dump() for e in GLOBAL_EVENT_BUS.get_history()]
        return web.json_response(history)

    def _is_allowed_artifact_path(self, resolved_path: Path) -> bool:
        """Restricts /api/artifact reads strictly to pipeline output directories and rejects dotfiles."""
        if resolved_path.name.startswith("."):
            return False
        allowed_roots = [SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR.resolve()]
        overview = GLOBAL_EVENT_BUS.get_tabs_overview()
        run_dir = overview.get("run_directory")
        if run_dir:
            allowed_roots.append(Path(run_dir).resolve())
        for tab in overview.get("accepted_tabs", []):
            rfc_dir = tab.get("rfc_dir")
            if rfc_dir:
                allowed_roots.append(Path(rfc_dir).resolve())
        return any(resolved_path.is_relative_to(root) for root in allowed_roots)

    async def handle_artifact(self, request: web.Request) -> web.Response:
        """Serves synthesized code or MITRE verification output files within authorized run directories."""
        filepath_str = request.query.get("path")
        if not filepath_str:
            return web.Response(text="Missing 'path' parameter", status=400)

        path = Path(filepath_str).resolve()
        if not self._is_allowed_artifact_path(path):
            return web.Response(text="Forbidden: path outside authorized output directories", status=403)
        if not path.exists() or not path.is_file():
            return web.Response(text=f"Artifact not found: {path.name}", status=404)

        content_type = "text/plain"
        if path.suffix in (".xhtml", ".html"):
            content_type = "application/xhtml+xml"
        elif path.suffix == ".svg":
            content_type = "image/svg+xml"
        elif path.suffix == ".json":
            content_type = "application/json"
        elif path.suffix == ".scm":
            content_type = "text/plain"

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            body = f.read()

        return web.Response(text=body, content_type=content_type)

    async def handle_sse(self, request: web.Request) -> web.StreamResponse:
        """Streams live Server-Sent Events to dashboard clients."""
        response = web.StreamResponse(
            status=200,
            reason="OK",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
                "Access-Control-Allow-Origin": "*",
            },
        )
        await response.prepare(request)

        client_queue: asyncio.Queue = asyncio.Queue()
        self._sse_clients.add(client_queue)

        await response.write(b": ping\n\n")

        try:
            while True:
                try:
                    event: PipelineEvent = await asyncio.wait_for(client_queue.get(), timeout=15.0)
                    sse_msg = event.to_sse_message().encode("utf-8")
                    await response.write(sse_msg)
                except asyncio.TimeoutError:
                    await response.write(b": heartbeat\n\n")
        except (asyncio.CancelledError, ConnectionResetError):
            pass
        finally:
            self._sse_clients.discard(client_queue)

        return response


def run_visualizer_in_background(host: str = "127.0.0.1", port: int = 8080):
    """Starts the visualizer server in a background daemon thread with access_log disabled."""

    def _is_port_available(p: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                s.bind((host, p))
                return True
            except OSError:
                return False

    actual_port = port
    while not _is_port_available(actual_port) and actual_port < port + 20:
        actual_port += 1

    server = VisualizerServer(host=host, port=actual_port)
    server.port = actual_port

    def _target():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server.loop = loop
        runner = web.AppRunner(server.app, access_log=None)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, host, actual_port)
        loop.run_until_complete(site.start())
        logger.info("Visualizer server active at http://%s:%d", host, actual_port)
        loop.run_forever()

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    time.sleep(0.15)
    return server
