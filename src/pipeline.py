"""Command-line interface for RFC-LLM synthesis pipeline supporting single RFCs and directory batching."""

import argparse
import csv
import datetime as dt
import json
import random
import re
import shlex
import sys
import time
import webbrowser
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from src.cost_tracker import GLOBAL_COST_TRACKER
from src.document_ingestion.rfc_header_filter import filter_rfc_header
from src.logging_config import PipelineMetricsCSVLogger
from src.main_pipeline_orchestrator import PipelineExecutionSummary, run_rfc_translation_pipeline
from src.pipeline_events import GLOBAL_EVENT_BUS
from src.system_config import SYSTEM_CONFIG
from src.visualizer.server import run_visualizer_in_background


def _print_cost_breakdown(cost_summary: dict, title: str = "COST & TOKEN TELEMETRY") -> None:
    """Prints a formatted breakdown of USD cost and tokens by model role."""
    roles = cost_summary.get("roles", {})
    role_labels = [
        ("router", "Router Model"),
        ("extraction", "Extraction Model"),
        ("query", "Query/Searcher Model"),
        ("repair", "Repair Model"),
    ]
    print(f"\n[{title}]")
    for role_key, label in role_labels:
        rb = roles.get(role_key, {})
        mod = rb.get("model") or "n/a"
        usd = float(rb.get("cost_usd", 0.0))
        calls = int(rb.get("calls", 0))
        toks = int(rb.get("total_tokens", 0))
        print(f" - {label:<20}: ${usd:.4f} ({calls} calls, {toks:,} tokens) [{mod}]")
    tot_usd = float(cost_summary.get("total_cost_usd", 0.0))
    tot_calls = int(cost_summary.get("total_calls", 0))
    tot_toks = int(cost_summary.get("total_tokens", 0))
    print(f" - {'Total Run Cost':<20}: ${tot_usd:.4f} ({tot_calls} calls, {tot_toks:,} tokens)")


def natural_rfc_sort_key(file_path: Path):
    """Sorts RFC files by integer number if present (e.g. rfc10 before rfc100)."""
    match = re.search(r"rfc(\d+)", file_path.stem.lower())
    if match:
        return (0, int(match.group(1)))
    return (1, file_path.name)


def get_completed_rfc_ids(csv_path: Optional[Path] = None) -> Set[str]:
    """Reads a pipeline_runs.csv ledger to retrieve RFC IDs that were already evaluated."""
    target_csv = csv_path or (SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv")
    if not target_csv.exists():
        return set()

    completed = set()
    try:
        with open(target_csv, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rfc_val = row.get("rfc_id", "").strip()
                if rfc_val:
                    # Normalize 'RFC 5246' or 'RFC5246' to 'RFC5246'
                    clean_id = rfc_val.upper().replace(" ", "").replace("_", "")
                    completed.add(clean_id)
    except Exception:
        pass
    return completed


def get_failed_rfc_ids(csv_path: Optional[Path] = None) -> Set[str]:
    """Reads a pipeline_runs.csv ledger to retrieve RFC IDs whose latest status is FAILED or PARTIAL."""
    target_csv = csv_path or (SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv")
    if not target_csv.exists():
        return set()

    failed = set()
    try:
        with open(target_csv, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rfc_val = row.get("rfc_id", "").strip()
                status_val = (row.get("status") or "").strip().upper()
                if rfc_val and status_val in {"FAILED", "PARTIAL"}:
                    clean_id = rfc_val.upper().replace(" ", "").replace("_", "")
                    failed.add(clean_id)
    except Exception:
        pass
    return failed


def get_eligible_rfc_count(csv_path: Optional[Path] = None) -> int:
    """Counts how many already-recorded RFC rows in pipeline_runs.csv were eligible protocols."""
    target_csv = csv_path or (SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv")
    if not target_csv.exists():
        return 0
    count = 0
    try:
        with open(target_csv, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row.get("is_eligible") or "").strip().lower() == "true":
                    count += 1
    except Exception:
        pass
    return count


def _is_localhost_binding(host: str) -> bool:
    """Returns True when the visualizer host is bound to a local loopback address."""
    return (host or "127.0.0.1").strip().lower() in {"127.0.0.1", "localhost", "::1"}


def _list_recent_run_dirs(base_output_dir: Path, limit: int = 3) -> List[Path]:
    """Returns the most recent `run_*` directories inside `base_output_dir`, sorted newest-first."""
    if not base_output_dir.exists():
        return []
    candidates = [
        d for d in base_output_dir.iterdir()
        if d.is_dir() and d.name.startswith("run_")
    ]
    # Sort by folder name (timestamp `run_YYYY-MM-DD_HH-MM-SS`) and mtime as tie-breaker, newest first
    candidates.sort(key=lambda d: (d.name, d.stat().st_mtime), reverse=True)
    return candidates[:limit]


def _summarize_run_dir(run_dir: Path) -> str:
    """Returns a concise one-line progress summary for a `run_*` directory."""
    csv_file = run_dir / "pipeline_runs.csv"
    idx_file = run_dir / "metadata_index.json"
    total_rows = 0
    eligible_rows = 0
    verified_rows = 0
    model_hint = ""

    if csv_file.exists() and csv_file.stat().st_size > 0:
        try:
            with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row.get("rfc_id"):
                        continue
                    total_rows += 1
                    if (row.get("is_eligible") or "").strip().lower() == "true":
                        eligible_rows += 1
                    if (row.get("status") or "").strip().upper() == "VERIFIED":
                        verified_rows += 1
                    if not model_hint:
                        model_hint = row.get("extraction_model") or row.get("router_model") or ""
        except Exception:
            pass
    elif idx_file.exists():
        try:
            idx_data = json.loads(idx_file.read_text(encoding="utf-8", errors="ignore"))
            runs = idx_data.get("runs") or []
            filtered = idx_data.get("filtered_rfcs") or []
            eligible_rows = sum(1 for r in runs if r.get("is_eligible", True))
            verified_rows = sum(1 for r in runs if r.get("build_successful"))
            total_rows = int(idx_data.get("total_rfcs_processed") or (len(runs) + len(filtered)))
        except Exception:
            pass

    manifest_file = run_dir / "run_manifest.json"
    if not model_hint and manifest_file.exists():
        try:
            m_data = json.loads(manifest_file.read_text(encoding="utf-8", errors="ignore"))
            cli_a = m_data.get("cli_args") or {}
            model_hint = cli_a.get("model") or cli_a.get("extraction_model") or ""
        except Exception:
            pass

    model_str = f" | model: {model_hint}" if model_hint else ""
    return f"{total_rows} processed, {eligible_rows} eligible, {verified_rows} verified{model_str}"


def _infer_models_from_csv(csv_file: Path) -> Dict[str, Optional[str]]:
    """Infers stage model overrides from the most recent row of an existing pipeline_runs.csv."""
    inferred: Dict[str, Optional[str]] = {
        "router_model": None,
        "extraction_model": None,
        "repair_model": None,
        "query_model": None,
    }
    if not csv_file.exists() or csv_file.stat().st_size == 0:
        return inferred
    try:
        with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            last_row = None
            for row in reader:
                if row.get("rfc_id"):
                    last_row = row
            if last_row:
                for key in tuple(inferred.keys()):
                    val = (last_row.get(key) or "").strip()
                    if val:
                        inferred[key] = val
    except Exception:
        pass
    return inferred


def _to_portable_relpath(p: Path) -> str:
    """Converts a path inside the repository to a portable project-relative path string."""
    try:
        return str(p.resolve().relative_to(SYSTEM_CONFIG.PROJECT_ROOT.resolve()))
    except ValueError:
        return str(p)


def _resolve_portable_path(raw_str: str, base_dir: Optional[Path] = None) -> Optional[Path]:
    """Resolves a path string that may be project-relative or an absolute path from another PC."""
    if not raw_str:
        return None
    cand = Path(raw_str)
    if cand.exists():
        return cand.resolve()

    proj_cand = SYSTEM_CONFIG.PROJECT_ROOT / raw_str
    if proj_cand.exists():
        return proj_cand.resolve()

    if base_dir is not None:
        for b_cand in (base_dir / raw_str, base_dir / cand.name):
            if b_cand.exists():
                return b_cand.resolve()

    # Rebase absolute paths originating from another machine/user directory
    parts = cand.parts
    for anchor in ("refrences", "output", "data", "logs"):
        if anchor in parts:
            idx = parts.index(anchor)
            rebased = SYSTEM_CONFIG.PROJECT_ROOT.joinpath(*parts[idx:])
            if rebased.exists():
                return rebased.resolve()

    if cand.name.lower().startswith("rfc") and cand.suffix.lower() == ".txt":
        fallback_rfc = SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "all_RFCs" / cand.name
        if fallback_rfc.exists():
            return fallback_rfc.resolve()

    return None


def _build_resume_command_string(
    run_root_dir: Path,
    targets: List[Path],
    args: argparse.Namespace,
) -> str:
    """Builds the full expanded `./rfc-llm -r <run_dir> ...` command string saved to `output/.last_run`."""
    run_arg = _to_portable_relpath(run_root_dir)
    cmd: List[str] = ["./rfc-llm", "-r", run_arg]
    for t in targets:
        cmd.append(_to_portable_relpath(t))

    if getattr(args, "model", None):
        cmd.extend(["--model", str(args.model)])
    if getattr(args, "router_model", None):
        cmd.extend(["--router-model", str(args.router_model)])
    if getattr(args, "extraction_model", None):
        cmd.extend(["--extraction-model", str(args.extraction_model)])
    if getattr(args, "repair_model", None):
        cmd.extend(["--repair-model", str(args.repair_model)])
    if getattr(args, "query_model", None):
        cmd.extend(["--query-model", str(args.query_model)])
    if getattr(args, "limit", None) is not None:
        cmd.extend(["--limit", str(args.limit)])
    if getattr(args, "target_eligible", None) is not None:
        cmd.extend(["--target-eligible", str(args.target_eligible)])
    if getattr(args, "pattern", None) and args.pattern != "rfc*.txt":
        cmd.extend(["--pattern", str(args.pattern)])
    if getattr(args, "tier0_eligible_only", False):
        cmd.append("--tier0-eligible-only")
    if getattr(args, "random", False):
        cmd.append("--random")
    if getattr(args, "retry_failed", False):
        cmd.append("--retry-failed")
    if getattr(args, "keep_ineligible", False):
        cmd.append("--keep-ineligible")
    if getattr(args, "no_visualize", False):
        cmd.append("--no-visualize")
    if getattr(args, "keep_alive", 0) and args.keep_alive > 0:
        cmd.extend(["--keep-alive", str(args.keep_alive)])
    if getattr(args, "host", "127.0.0.1") and args.host != "127.0.0.1":
        cmd.extend(["--host", str(args.host)])
    if getattr(args, "port", 8080) and args.port != 8080:
        cmd.extend(["--port", str(args.port)])

    return shlex.join(cmd)


def _save_run_manifest_and_last_run(
    run_root_dir: Path,
    base_output_dir: Path,
    targets: List[Path],
    args: argparse.Namespace,
    planned_rfc_files: List[Path],
) -> Tuple[Path, Path, str]:
    """Writes `<run_root_dir>/run_manifest.json` and updates `<base_output_dir>/.last_run` with the full resume command."""
    run_root_dir.mkdir(parents=True, exist_ok=True)
    base_output_dir.mkdir(parents=True, exist_ok=True)

    resume_cmd = _build_resume_command_string(run_root_dir, targets, args)
    last_run_path = base_output_dir / ".last_run"
    last_run_path.write_text(resume_cmd + "\n", encoding="utf-8")

    manifest_path = run_root_dir / "run_manifest.json"
    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    existing_created = now_utc
    if manifest_path.exists():
        try:
            old_m = json.loads(manifest_path.read_text(encoding="utf-8"))
            existing_created = old_m.get("created_at_utc") or now_utc
        except Exception:
            pass

    manifest_payload = {
        "schema_version": "1.0.0",
        "run_root_dir": _to_portable_relpath(run_root_dir),
        "resume_command": resume_cmd,
        "created_at_utc": existing_created,
        "updated_at_utc": now_utc,
        "targets": [_to_portable_relpath(t) for t in targets],
        "cli_args": {
            "model": args.model,
            "router_model": args.router_model,
            "extraction_model": args.extraction_model,
            "repair_model": args.repair_model,
            "query_model": args.query_model,
            "limit": args.limit,
            "target_eligible": args.target_eligible,
            "pattern": args.pattern,
            "tier0_eligible_only": bool(args.tier0_eligible_only),
            "random": bool(args.random),
            "retry_failed": bool(args.retry_failed),
            "keep_ineligible": bool(args.keep_ineligible),
            "skip_completed": bool(args.skip_completed),
            "no_visualize": bool(args.no_visualize),
            "keep_alive": int(args.keep_alive or 0),
            "host": args.host,
            "port": int(args.port),
        },
        "planned_rfc_files": [_to_portable_relpath(f) for f in planned_rfc_files],
    }
    manifest_path.write_text(json.dumps(manifest_payload, indent=2), encoding="utf-8")
    return manifest_path, last_run_path, resume_cmd


def _build_parser(suppress_defaults: bool = False) -> argparse.ArgumentParser:
    """Constructs the CLI argument parser. When `suppress_defaults=True`, only explicitly passed CLI flags are populated."""
    d_none = argparse.SUPPRESS if suppress_defaults else None
    d_false = argparse.SUPPRESS if suppress_defaults else False
    d_zero = argparse.SUPPRESS if suppress_defaults else 0
    d_host = argparse.SUPPRESS if suppress_defaults else "127.0.0.1"
    d_port = argparse.SUPPRESS if suppress_defaults else 8080
    d_pat = argparse.SUPPRESS if suppress_defaults else "rfc*.txt"

    parser = argparse.ArgumentParser(
        description="RFC-LLM: End-to-End Synthesis of Verified MITRE CPSA Models from IETF RFCs",
        add_help=not suppress_defaults,
    )
    parser.add_argument(
        "target_path",
        type=str,
        nargs="*",
        default=d_none if suppress_defaults else [],
        help="One or more RFC text files (such as refrences/all_RFCs/rfc5246.txt) OR a directory containing RFCs",
    )
    parser.add_argument(
        "--resume",
        "-r",
        nargs="?",
        const="__LAST_RUN__",
        default=d_none,
        metavar="RUN_DIR_OR_NUM",
        help="Resume a previous run in-place. Pass -r alone to resume output/.last_run, or pass a run folder / index (1-3).",
    )
    parser.add_argument(
        "--view",
        type=str,
        default=d_none,
        help="Open an existing run directory (e.g. output/run_2026-10-28_16-03-11) or metadata_index.json in offline visualizer replay mode",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default=d_none,
        help="Directory to place synthesized models and build artifacts",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=d_none,
        help="Global model identifier for all pipeline stages (e.g. 'gemini/gemini-3.5-flash-lite', 'ollama/qwen2.5:7b-instruct')",
    )
    parser.add_argument(
        "--router-model",
        type=str,
        default=d_none,
        help="Model identifier for document gatekeeper and TOC router",
    )
    parser.add_argument(
        "--extraction-model",
        type=str,
        default=d_none,
        help="Model identifier for Pydantic constrained semantic extraction",
    )
    parser.add_argument(
        "--repair-model",
        type=str,
        default=d_none,
        help="Model identifier for RAG self-healing compiler diagnostic repair",
    )
    parser.add_argument(
        "--query-model",
        type=str,
        default=d_none,
        help="Model identifier for RAG query formulation / conceptual abstraction",
    )
    parser.add_argument(
        "--no-visualize",
        action="store_true",
        default=d_false,
        help="Disable the live web dashboard visualizer (enabled by default)",
    )
    parser.add_argument(
        "--visualize",
        "-v",
        action="store_true",
        default=d_false,
        help="Ensure live web dashboard visualizer is enabled",
    )
    parser.add_argument(
        "--keep-alive",
        type=int,
        default=d_zero,
        help="Seconds to keep visualizer server running after completion in non-interactive mode",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=d_host,
        help="Host/IP address to bind the web visualizer dashboard (default: 127.0.0.1; pass Tailscale IP or 0.0.0.0 for remote access)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=d_port,
        help="Web port for the live visualizer dashboard (default: 8080)",
    )
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=d_none,
        help="Maximum number of RFC files to scan when pointing to a directory",
    )
    parser.add_argument(
        "--target-eligible",
        "-e",
        type=int,
        default=d_none,
        help="Stop batch processing once N eligible cryptographic protocols have been synthesized",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default=d_pat,
        help="Glob pattern for discovering RFC files when scanning a directory (default: 'rfc*.txt')",
    )
    parser.add_argument(
        "--skip-completed",
        action="store_true",
        default=d_false,
        help="Skip RFCs that already have completed run entries in logs/pipeline_runs.csv",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        default=d_false,
        help="Run only RFCs recorded in logs/pipeline_runs.csv with status FAILED or PARTIAL (overwriting their rows in-place)",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        default=d_false,
        help="Randomly sample RFC files when pointing to a directory (useful with --limit)",
    )
    parser.add_argument(
        "--tier0-eligible-only",
        action="store_true",
        default=d_false,
        help="Pre-filter directory candidates using deterministic Tier 0 frontmatter check before applying --limit",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=d_none,
        help="Path to an existing pipeline_runs.csv or older run directory to copy/seed into this new run's pipeline_runs.csv (source CSV is never modified)",
    )
    parser.add_argument(
        "--keep-ineligible",
        "--reset-eligible",
        dest="keep_ineligible",
        action="store_true",
        default=d_false,
        help="Prune the active run's pipeline_runs.csv by deleting all rows EXCEPT ineligible RFCs (is_eligible=False), and skip those ineligible RFCs when starting a new batch run",
    )
    return parser


def main(argv: Optional[List[str]] = None):
    raw_argv = list(argv) if argv is not None else sys.argv[1:]
    parser = _build_parser(suppress_defaults=False)
    args = parser.parse_args(raw_argv)

    explicit_parser = _build_parser(suppress_defaults=True)
    explicit_ns, _ = explicit_parser.parse_known_args(raw_argv)
    explicit_overrides = vars(explicit_ns)
    if explicit_overrides.get("target_path") == []:
        explicit_overrides.pop("target_path", None)

    # Offline Replay Mode (--view <run_dir>)
    if args.view:
        view_path = Path(args.view)
        if not view_path.exists():
            print(f"Error: Run directory or index does not exist: {view_path}", file=sys.stderr)
            sys.exit(1)

        overview = GLOBAL_EVENT_BUS.load_run_from_disk(view_path, is_live=False)
        if args.csv:
            src_csv = Path(args.csv)
            if src_csv.is_dir():
                src_csv = src_csv / "pipeline_runs.csv"
            if src_csv.exists():
                GLOBAL_EVENT_BUS.set_run_directory(
                    Path(overview.get("run_directory") or view_path),
                    is_live=False,
                    csv_path=src_csv,
                )
        server = run_visualizer_in_background(host=args.host, port=args.port)
        monitor_url = f"http://{args.host}:{server.port}"

        print(f"\n{'='*70}")
        print(f" [OFFLINE REPLAY MONITOR] Active at: {monitor_url}")
        print(f" - Run Directory   : {overview.get('run_directory')}")
        print(f" - Run Metrics CSV : {GLOBAL_EVENT_BUS.get_csv_path()}")
        print(f" - Accepted Tabs   : {len(overview.get('accepted_tabs', []))}")
        print(f" - Filtered / Skips: {overview.get('filtered_total', 0)}")
        print(f"{'='*70}\n")

        if not args.no_visualize and _is_localhost_binding(args.host):
            try:
                webbrowser.open(monitor_url)
            except Exception:
                pass

        if sys.stdin.isatty() and args.keep_alive <= 0:
            try:
                input("[OFFLINE REPLAY MONITOR] Press Enter to exit (server remains live until keypress)... ")
            except (EOFError, KeyboardInterrupt):
                pass
        else:
            wait_sec = args.keep_alive if args.keep_alive > 0 else 60
            print(f"[OFFLINE REPLAY MONITOR] Keeping server active for {wait_sec}s...")
            time.sleep(wait_sec)
        sys.exit(0)

    # -------------------------------------------------------------------------
    # Resume Mode (--resume / -r [RUN_DIR_OR_NUM])
    # -------------------------------------------------------------------------
    base_dir = Path(args.output_dir) if args.output_dir else SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR
    is_resuming = args.resume is not None
    resuming_run_dir: Optional[Path] = None
    manifest_data: Dict[str, Any] = {}

    if is_resuming:
        last_run_file = base_dir / ".last_run"
        saved_tokens: Optional[List[str]] = None

        if args.resume == "__LAST_RUN__":
            if last_run_file.exists():
                raw_last_cmd = last_run_file.read_text(encoding="utf-8", errors="ignore").strip()
                if raw_last_cmd:
                    try:
                        tokens = shlex.split(raw_last_cmd)
                        while tokens and (
                            tokens[0].endswith("rfc-llm")
                            or tokens[0].endswith("python")
                            or tokens[0].endswith("python3")
                            or tokens[0].endswith("pipeline.py")
                        ):
                            tokens.pop(0)
                        parsed_saved = parser.parse_args(tokens)
                        if parsed_saved.resume and parsed_saved.resume != "__LAST_RUN__":
                            cand = _resolve_portable_path(parsed_saved.resume, base_dir=base_dir)
                            if cand and cand.is_dir():
                                resuming_run_dir = cand.resolve()
                                saved_tokens = tokens
                    except Exception:
                        resuming_run_dir = None

            if resuming_run_dir is None:
                recent_runs = _list_recent_run_dirs(base_dir, limit=3)
                if recent_runs:
                    print("No active output/.last_run found. Top 3 most recent runs available to resume:")
                    for idx_num, r_dir in enumerate(recent_runs, 1):
                        try:
                            rel_r = r_dir.resolve().relative_to(SYSTEM_CONFIG.PROJECT_ROOT.resolve())
                            disp = str(rel_r)
                        except ValueError:
                            disp = str(r_dir)
                        print(f"  [{idx_num}] {disp:<34} ({_summarize_run_dir(r_dir)})")
                    print(
                        "\nTo continue this, re-run the command with -r <folder_number> "
                        "(e.g., ./rfc-llm -r 1) or -r <folder_path>."
                    )
                    sys.exit(0)
                else:
                    print(
                        "No previous runs found in output/. The -r / --resume flag is used after a first initial run "
                        "(e.g., ./rfc-llm refrences/all_RFCs/ --model ...)."
                    )
                    sys.exit(0)
        else:
            raw_spec = args.resume.strip()
            if raw_spec.isdigit() and not Path(raw_spec).exists():
                pick_idx = int(raw_spec) - 1
                recent_runs = _list_recent_run_dirs(base_dir, limit=10)
                if 0 <= pick_idx < len(recent_runs):
                    resuming_run_dir = recent_runs[pick_idx].resolve()
                else:
                    top3 = recent_runs[:3]
                    if top3:
                        print(f"Error: Run number '{raw_spec}' is out of range.", file=sys.stderr)
                        for idx_num, r_dir in enumerate(top3, 1):
                            print(f"  [{idx_num}] {r_dir} ({_summarize_run_dir(r_dir)})", file=sys.stderr)
                        print("To continue this, re-run the command with -r <folder_number>.", file=sys.stderr)
                    else:
                        print(
                            "No previous runs found in output/. The -r / --resume flag is used after a first initial run.",
                            file=sys.stderr,
                        )
                    sys.exit(1)
            else:
                cand = _resolve_portable_path(raw_spec, base_dir=base_dir)
                if not cand or not cand.is_dir():
                    print(f"Error: Resume run directory does not exist: {raw_spec}", file=sys.stderr)
                    recent_runs = _list_recent_run_dirs(base_dir, limit=3)
                    if recent_runs:
                        print("Top 3 most recent runs available to resume:", file=sys.stderr)
                        for idx_num, r_dir in enumerate(recent_runs, 1):
                            print(f"  [{idx_num}] {r_dir} ({_summarize_run_dir(r_dir)})", file=sys.stderr)
                        print("To continue this, re-run the command with -r <folder_number>.", file=sys.stderr)
                    sys.exit(1)
                resuming_run_dir = cand.resolve()

        # Load run_manifest.json from resuming_run_dir if available
        manifest_file = resuming_run_dir / "run_manifest.json"
        if manifest_file.exists():
            try:
                manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))
            except Exception:
                manifest_data = {}

        if saved_tokens is None and manifest_data.get("resume_command"):
            try:
                m_tokens = shlex.split(manifest_data["resume_command"])
                while m_tokens and (
                    m_tokens[0].endswith("rfc-llm")
                    or m_tokens[0].endswith("python")
                    or m_tokens[0].endswith("python3")
                    or m_tokens[0].endswith("pipeline.py")
                ):
                    m_tokens.pop(0)
                saved_tokens = m_tokens
            except Exception:
                saved_tokens = None

        if saved_tokens is not None:
            base_args = parser.parse_args(saved_tokens)
        else:
            base_args = parser.parse_args([])
            saved_cli = manifest_data.get("cli_args") or {}
            for k, v in saved_cli.items():
                if hasattr(base_args, k) and v is not None:
                    setattr(base_args, k, v)
            if manifest_data.get("targets"):
                base_args.target_path = list(manifest_data["targets"])
            else:
                inferred_models = _infer_models_from_csv(resuming_run_dir / "pipeline_runs.csv")
                for mk, mv in inferred_models.items():
                    if mv and not getattr(base_args, mk, None):
                        setattr(base_args, mk, mv)
                default_rfc_dir = SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "all_RFCs"
                if default_rfc_dir.exists():
                    base_args.target_path = [str(default_rfc_dir)]

        # Overlay any CLI flags explicitly passed on the current `-r` invocation
        if "model" in explicit_overrides:
            for stage_m in ("router_model", "extraction_model", "repair_model", "query_model"):
                if stage_m not in explicit_overrides:
                    setattr(base_args, stage_m, None)
        for k, v in explicit_overrides.items():
            if k != "resume":
                setattr(base_args, k, v)
        base_args.resume = str(resuming_run_dir)
        args = base_args

    # Require --csv whenever --keep-ineligible, --skip-completed, or --retry-failed is used (unless resuming with -r)
    if not is_resuming and (args.keep_ineligible or args.skip_completed or args.retry_failed) and not args.csv:
        active_flags = [
            flag
            for flag, enabled in (
                ("--keep-ineligible", args.keep_ineligible),
                ("--skip-completed", args.skip_completed),
                ("--retry-failed", args.retry_failed),
            )
            if enabled
        ]
        parser.error(
            f"{', '.join(active_flags)} requires --csv <path_to_existing_csv_or_run_dir> (or --resume / -r). "
            "Pass --csv pointing to the existing CSV ledger (or run directory) these flags should apply to, "
            "or remove those flags to start a fresh run."
        )

    # Standalone --keep-ineligible --csv <path> prune mode (no target_path passed)
    if not is_resuming and args.keep_ineligible and not args.target_path:
        cand = Path(args.csv)
        if not cand.exists():
            print(f"Error: Source --csv path does not exist: {cand}", file=sys.stderr)
            sys.exit(1)
        standalone_csv_path = (cand / "pipeline_runs.csv") if cand.is_dir() else cand
        csv_logger = PipelineMetricsCSVLogger(csv_path=standalone_csv_path)
        removed_cnt, kept_cnt = csv_logger.prune_keep_ineligible_only()
        print(
            f"[CSV PRUNE] Updated {csv_logger.csv_path}: removed {removed_cnt} eligible row(s), "
            f"retained {kept_cnt} INELIGIBLE row(s) (is_eligible=False)."
        )
        sys.exit(0)

    if not args.target_path:
        parser.error("the following arguments are required: target_path (or pass --resume / -r or --view <run_dir>)")

    targets: List[Path] = []
    for p in args.target_path:
        resolved_t = _resolve_portable_path(str(p), base_dir=base_dir)
        if resolved_t is None:
            print(f"Error: Target path does not exist: {p}", file=sys.stderr)
            sys.exit(1)
        targets.append(resolved_t)

    if args.csv and not Path(args.csv).exists():
        print(f"Error: Source --csv path does not exist: {args.csv}", file=sys.stderr)
        sys.exit(1)

    # Pre-flight verification of MITRE CPSA 4.4.9 compiler binaries before starting LLM synthesis
    missing_cpsa_bins = SYSTEM_CONFIG.verify_cpsa_toolchain()
    if missing_cpsa_bins:
        print(
            "Error: MITRE CPSA 4.4.9 compiler toolchain is missing required binaries:\n"
            + "\n".join(f"  - {b}" for b in missing_cpsa_bins)
            + "\nInstall CPSA 4.4.9 (`cabal update && cabal install cpsa`) or ensure ~/.cabal/bin is populated before running synthesis.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 1. Create or Re-Attach Run Directory & Per-Run CSV Ledger
    if is_resuming and resuming_run_dir is not None:
        run_root_dir = resuming_run_dir
        base_dir = run_root_dir.parent
    else:
        run_timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_dir = Path(args.output_dir) if args.output_dir else SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR
        if base_dir.name.startswith("run_"):
            run_root_dir = base_dir
            base_dir = run_root_dir.parent
        else:
            run_root_dir = base_dir / f"run_{run_timestamp}"

    run_root_dir.mkdir(parents=True, exist_ok=True)
    run_csv_path = run_root_dir / "pipeline_runs.csv"
    csv_logger = PipelineMetricsCSVLogger(csv_path=run_csv_path)

    if is_resuming:
        # Ensure legacy runs that only had metadata_index.json have their CSV populated before filtering
        if (
            (not run_csv_path.exists() or len(get_completed_rfc_ids(csv_path=run_csv_path)) == 0)
            and (run_root_dir / "metadata_index.json").exists()
        ):
            csv_logger.seed_from_source(run_root_dir / "metadata_index.json")

        if explicit_overrides.get("keep_ineligible"):
            removed_cnt, kept_cnt = csv_logger.prune_keep_ineligible_only()
            print(
                f"[CSV PRUNE] Pruned {run_csv_path}: removed {removed_cnt} eligible row(s), "
                f"retained {kept_cnt} INELIGIBLE row(s) (is_eligible=False)."
            )

        overview = GLOBAL_EVENT_BUS.load_run_from_disk(run_root_dir, is_live=True)
        GLOBAL_EVENT_BUS.set_run_directory(run_root_dir, is_live=True, csv_path=run_csv_path)
        GLOBAL_COST_TRACKER.restore_batch_summary(overview.get("batch_cost_telemetry"))
        prior_eligible_count = 0 if args.retry_failed else get_eligible_rfc_count(csv_path=run_csv_path)
    else:
        prior_eligible_count = 0
        # Seed new run's CSV from --csv <source> (source CSV is never mutated)
        if args.csv:
            src_csv_path = Path(args.csv)
            seeded_count = csv_logger.seed_from_source(src_csv_path)
            print(
                f"[CSV SEED] Copied {seeded_count} row(s) from {src_csv_path} -> {run_csv_path} "
                f"(source left untouched)."
            )

        if args.keep_ineligible:
            removed_cnt, kept_cnt = csv_logger.prune_keep_ineligible_only()
            print(
                f"[CSV PRUNE] Pruned {run_csv_path}: removed {removed_cnt} eligible row(s), "
                f"retained {kept_cnt} INELIGIBLE row(s) (is_eligible=False)."
            )
            args.skip_completed = True

        GLOBAL_EVENT_BUS.set_run_directory(run_root_dir, is_live=True, csv_path=run_csv_path)

    # 2. Resolve Target Files (Single File, Multiple Files, Directory Batch, or Resumed Queue)
    queue_affecting_overrides = {"target_path", "limit", "random", "tier0_eligible_only", "pattern"}
    can_reuse_manifest_queue = (
        is_resuming
        and bool(manifest_data.get("planned_rfc_files"))
        and not any(k in explicit_overrides for k in queue_affecting_overrides)
    )

    planned_rfc_files: List[Path] = []
    if can_reuse_manifest_queue:
        for raw_p in manifest_data["planned_rfc_files"]:
            rp = _resolve_portable_path(str(raw_p), base_dir=base_dir)
            if rp is not None and rp.is_file():
                planned_rfc_files.append(rp)

    if not planned_rfc_files and (len(targets) > 1 or targets[0].is_file()):
        planned_rfc_files = [t for t in targets if t.is_file()]
    elif not planned_rfc_files and targets[0].is_dir():
        target = targets[0]
        raw_candidates = [f for f in target.glob(args.pattern) if f.is_file()]
        if args.pattern == "rfc*.txt":
            # Exclude non-numeric index/reference files such as rfc-index-latest.txt or rfc-ref-old.txt
            numeric_candidates = [f for f in raw_candidates if re.fullmatch(r"rfc\d+\.txt", f.name.lower())]
            planned_rfc_files = sorted(numeric_candidates or raw_candidates, key=natural_rfc_sort_key)
        else:
            planned_rfc_files = sorted(raw_candidates, key=natural_rfc_sort_key)
        if not planned_rfc_files:
            # Fallback to all existing txt files if pattern yielded zero
            planned_rfc_files = sorted([f for f in target.glob("*.txt") if f.is_file()], key=natural_rfc_sort_key)
        if not planned_rfc_files:
            print(f"Error: No RFC text files found in directory {target}", file=sys.stderr)
            sys.exit(1)

        if not is_resuming:
            if args.retry_failed:
                failed_ids = get_failed_rfc_ids(csv_path=run_csv_path)
                planned_rfc_files = [
                    f for f in planned_rfc_files
                    if f.stem.upper().replace(" ", "").replace("_", "") in failed_ids
                ]
                print(f"[BATCH] Filtered to {len(planned_rfc_files)} previously FAILED/PARTIAL RFCs from {run_csv_path}")
            elif args.skip_completed:
                completed_ids = get_completed_rfc_ids(csv_path=run_csv_path)
                initial_count = len(planned_rfc_files)
                planned_rfc_files = [
                    f for f in planned_rfc_files
                    if f.stem.upper().replace(" ", "").replace("_", "") not in completed_ids
                ]
                print(f"[BATCH] Filtered out {initial_count - len(planned_rfc_files)} previously evaluated RFCs ({len(planned_rfc_files)} remaining)")

        if args.tier0_eligible_only:
            before_t0 = len(planned_rfc_files)
            planned_rfc_files = [
                f for f in planned_rfc_files
                if filter_rfc_header(f.read_text(encoding="utf-8", errors="ignore")).is_eligible
            ]
            print(f"[BATCH] Tier 0 pre-filter retained {len(planned_rfc_files)}/{before_t0} candidate RFCs")

        if args.random:
            random.shuffle(planned_rfc_files)
            print("[BATCH] Shuffled candidate RFC list randomly")

        if args.limit and args.limit > 0:
            planned_rfc_files = planned_rfc_files[:args.limit]
            print(f"[BATCH] Processing limited to {len(planned_rfc_files)} RFCs: {[f.name for f in planned_rfc_files]}")
    elif not planned_rfc_files:
        print(f"Error: Invalid target path: {targets[0]}", file=sys.stderr)
        sys.exit(1)

    if is_resuming:
        if args.retry_failed:
            failed_ids = get_failed_rfc_ids(csv_path=run_csv_path)
            rfc_files = [
                f for f in planned_rfc_files
                if f.stem.upper().replace(" ", "").replace("_", "") in failed_ids
            ]
            print(f"[RESUME] Filtered to {len(rfc_files)} previously FAILED/PARTIAL RFCs in {run_root_dir.name}")
        else:
            completed_ids = get_completed_rfc_ids(csv_path=run_csv_path)
            rfc_files = [
                f for f in planned_rfc_files
                if f.stem.upper().replace(" ", "").replace("_", "") not in completed_ids
            ]
            skipped_count = len(planned_rfc_files) - len(rfc_files)
            print(
                f"[RESUME] Continuing {run_root_dir.name}: skipped {skipped_count} already-processed RFC(s), "
                f"{len(rfc_files)} remaining in queue."
            )
    else:
        rfc_files = list(planned_rfc_files)

    manifest_path, last_run_file, resume_cmd_str = _save_run_manifest_and_last_run(
        run_root_dir=run_root_dir,
        base_output_dir=base_dir,
        targets=targets,
        args=args,
        planned_rfc_files=planned_rfc_files,
    )

    if is_resuming and not rfc_files:
        print(
            f"[RESUME] All candidate RFCs in {run_root_dir} have already been processed (0 remaining). "
            f"Use ./rfc-llm --view {run_root_dir} to inspect results."
        )
        sys.exit(0)

    # 3. Launch Visualizer (Default Enabled)
    enable_visualizer = not args.no_visualize
    monitor_url = None
    if enable_visualizer:
        try:
            server = run_visualizer_in_background(host=args.host, port=args.port)
            monitor_url = f"http://{args.host}:{server.port}"
            print(f"\n{'='*70}")
            print(f" [LIVE MONITOR] Active at: {monitor_url}")
            print(f"{'='*70}\n")
            if _is_localhost_binding(args.host):
                try:
                    webbrowser.open(monitor_url)
                except Exception:
                    pass
        except Exception as e:
            print(f"[WARN] Could not launch live monitor: {e}")

    master_index_path = run_root_dir / "metadata_index.json"
    if not master_index_path.exists():
        now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        master_index_path.write_text(
            json.dumps(
                {
                    "schema_version": "1.0.0",
                    "run_directory": str(run_root_dir.resolve()),
                    "csv_file": str(run_csv_path.resolve()),
                    "created_at_utc": now_utc,
                    "updated_at_utc": now_utc,
                    "total_rfcs_processed": 0,
                    "total_ineligible_filtered": 0,
                    "total_eligible_protocols": 0,
                    "metadata_json_files": [],
                    "rfc_directories": [],
                    "runs": [],
                    "filtered_rfcs": [],
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    print(f"[RUN] {'Resumed' if is_resuming else 'Created'} run directory   : {run_root_dir}")
    print(f"[RUN] Master Metadata Index           : {master_index_path}")
    print(f"[RUN] Run CSV Ledger                  : {run_csv_path}")
    print(f"[RUN] Saved Resume Command (.last_run): {resume_cmd_str}")

    # 4. Execution Loop (Models resolve dynamically from prompts/*.md unless CLI overrides are passed)
    results: List[PipelineExecutionSummary] = []
    total_files = len(rfc_files)
    cli_router_model = args.router_model or args.model
    cli_extraction_model = args.extraction_model or args.model
    cli_repair_model = args.repair_model or args.model
    cli_query_model = args.query_model or args.model

    if is_resuming and args.target_eligible and args.target_eligible > 0 and prior_eligible_count >= args.target_eligible:
        print(
            f"\n[RESUME] Run {run_root_dir.name} already reached target of "
            f"{prior_eligible_count}/{args.target_eligible} eligible cryptographic protocols."
        )
        sys.exit(0)

    for idx, rfc_file in enumerate(rfc_files, 1):
        if total_files > 1:
            print(f"\n{'='*70}")
            print(f"[{idx}/{total_files}] Processing RFC: {rfc_file.name}")
            print(f"{'='*70}")

        rfc_output_dir = run_root_dir / rfc_file.stem.lower()
        try:
            summary = run_rfc_translation_pipeline(
                rfc_file_path=rfc_file,
                output_dir=rfc_output_dir,
                router_model=cli_router_model,
                extraction_model=cli_extraction_model,
                repair_model=cli_repair_model,
                query_model=cli_query_model,
                run_root_dir=run_root_dir,
                csv_path=run_csv_path,
                resume_checkpoint=is_resuming,
            )
        except Exception as exc:
            print(f"[ERROR] Unhandled exception on {rfc_file.name}: {exc}", file=sys.stderr)
            summary = PipelineExecutionSummary(
                rfc_id=rfc_file.stem.upper(),
                is_eligible=False,
                error_message=f"Unhandled pipeline exception: {exc}",
            )
        results.append(summary)

        if args.target_eligible and args.target_eligible > 0:
            eligible_so_far = prior_eligible_count + sum(1 for r in results if r.is_eligible)
            if eligible_so_far >= args.target_eligible:
                print(
                    f"\n[BATCH] Reached target of {eligible_so_far}/{args.target_eligible} "
                    f"eligible cryptographic protocols after scanning {idx} RFC(s)."
                )
                break

        if total_files == 1:
            # Single-file reporting and exit code
            if summary.build_successful:
                print("\n[SUCCESS] Synthesis & Formal Verification Completed!")
                print(f"Protocol             : {summary.protocol_name}")
                print(f"Quality Tier         : {summary.quality_tier}")
                if summary.intake_rationale:
                    print(f"Intake Rationale     : Eligible: {summary.intake_rationale}")
                if summary.security_findings:
                    sf = summary.security_findings
                    print(
                        f"Security Findings    : Auth={sf.get('authentication_profile', 'N/A')} | "
                        f"Agreement={sf.get('parameter_agreement_status', 'N/A')} | "
                        f"Secrecy={sf.get('secrecy_status', 'N/A')} | "
                        f"Anomalies={sf.get('anomalies_count', 0)}"
                    )
                print(f"Run Directory        : {run_root_dir}")
                print(f"Master Metadata Index: {master_index_path}")
                print(f"Run Metrics Logged   : {run_csv_path}")
                print(f"RFC Directory        : {rfc_output_dir}")
                print(f"RFC Trajectory JSON  : {summary.trajectory_json_path}")
                print(f"Verified Shapes XHTML: {summary.build_artifacts.shapes_graph_xhtml_path}")
            elif summary.roletran_passed:
                print(f"\n[PARTIAL] Roletran passed, but MITRE build failed: {summary.error_message}")
                print(f"Run Directory        : {run_root_dir}")
                print(f"Master Metadata Index: {master_index_path}")
                print(f"Run Metrics Logged   : {run_csv_path}")
                print(f"RFC Trajectory JSON  : {summary.trajectory_json_path}")
            else:
                print(f"\n[HALTED] Pipeline stopped: {summary.error_message}")
                print(f"Run Directory        : {run_root_dir}")
                print(f"Master Metadata Index: {master_index_path}")
                print(f"Run Metrics Logged   : {run_csv_path}")
                if summary.trajectory_json_path:
                    print(f"RFC Trajectory JSON  : {summary.trajectory_json_path}")

            _print_cost_breakdown(GLOBAL_COST_TRACKER.get_current_rfc_summary(), "RFC RUN COST & TOKEN TELEMETRY")

            if enable_visualizer and monitor_url:
                print(f"\n[LIVE MONITOR] View execution trace and shapes at: {monitor_url}")
                if sys.stdin.isatty():
                    try:
                        input("[LIVE MONITOR] Press Enter to exit (server remains live until keypress)... ")
                    except (EOFError, KeyboardInterrupt):
                        pass
                elif args.keep_alive > 0:
                    print(f"[LIVE MONITOR] Keeping server active for {args.keep_alive}s...")
                    time.sleep(args.keep_alive)

            sys.exit(0 if summary.build_successful else (1 if summary.roletran_passed else 2))

    # 5. Batch Summary Report
    print(f"\n{'='*70}")
    print(f"RFC-LLM BATCH SYNTHESIS REPORT ({total_files} RFCs Processed)")
    print(f"{'='*70}")
    verified_count = sum(1 for r in results if r.build_successful)
    eligible_count = sum(1 for r in results if r.is_eligible)
    ineligible_count = sum(1 for r in results if not r.is_eligible)
    roletran_failed = sum(1 for r in results if r.is_eligible and not r.roletran_passed)
    solver_failed = sum(1 for r in results if r.roletran_passed and not r.build_successful)

    print(f"- Total Processed      : {total_files}")
    print(f"- Ineligible (Filtered): {ineligible_count}")
    print(f"- Eligible Protocols   : {eligible_count}")
    print(f"- Formally Verified    : {verified_count}")
    if roletran_failed:
        print(f"- Roletran Failed      : {roletran_failed}")
    if solver_failed:
        print(f"- Solver Failed        : {solver_failed}")
    print(f"- Run Directory        : {run_root_dir}")
    print(f"- Master Metadata Index: {master_index_path}")
    print(f"- Run Metrics Logged   : {run_csv_path}")
    _print_cost_breakdown(GLOBAL_COST_TRACKER.get_batch_summary(), "BATCH COST & TOKEN TELEMETRY BY MODEL ROLE")
    print(f"{'='*70}\n")

    if enable_visualizer and monitor_url:
        print(f"[LIVE MONITOR] Batch dashboard active at: {monitor_url}")
        if sys.stdin.isatty():
            try:
                input("[LIVE MONITOR] Press Enter to exit (server remains live until keypress)... ")
            except (EOFError, KeyboardInterrupt):
                pass
        elif args.keep_alive > 0:
            print(f"[LIVE MONITOR] Keeping server active for {args.keep_alive}s...")
            time.sleep(args.keep_alive)


if __name__ == "__main__":
    main()
