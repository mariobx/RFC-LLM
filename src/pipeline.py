"""Command-line interface for RFC-LLM synthesis pipeline supporting single RFCs and directory batching."""

import argparse
import csv
import datetime as dt
import json
import random
import re
import sys
import time
import webbrowser
from pathlib import Path
from typing import List, Optional, Set

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


def main():
    parser = argparse.ArgumentParser(
        description="RFC-LLM: End-to-End Synthesis of Verified MITRE CPSA Models from IETF RFCs",
    )
    parser.add_argument(
        "target_path",
        type=str,
        nargs="*",
        help="One or more RFC text files (such as refrences/all_RFCs/rfc5246.txt) OR a directory containing RFCs",
    )
    parser.add_argument(
        "--view",
        type=str,
        default=None,
        help="Open an existing run directory (e.g. output/run_2026-10-28_16-03-11) or metadata_index.json in offline visualizer replay mode",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default=None,
        help="Directory to place synthesized models and build artifacts",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help="Global model identifier for all pipeline stages (e.g. 'gemini/gemini-3.5-flash-lite', 'ollama/qwen2.5:7b-instruct')",
    )
    parser.add_argument(
        "--router-model",
        type=str,
        default=None,
        help="Model identifier for document gatekeeper and TOC router",
    )
    parser.add_argument(
        "--extraction-model",
        type=str,
        default=None,
        help="Model identifier for Pydantic constrained semantic extraction",
    )
    parser.add_argument(
        "--repair-model",
        type=str,
        default=None,
        help="Model identifier for RAG self-healing compiler diagnostic repair",
    )
    parser.add_argument(
        "--query-model",
        type=str,
        default=None,
        help="Model identifier for RAG query formulation / conceptual abstraction",
    )
    parser.add_argument(
        "--no-visualize",
        action="store_true",
        help="Disable the live web dashboard visualizer (enabled by default)",
    )
    parser.add_argument(
        "--visualize",
        "-v",
        action="store_true",
        help="Ensure live web dashboard visualizer is enabled",
    )
    parser.add_argument(
        "--keep-alive",
        type=int,
        default=0,
        help="Seconds to keep visualizer server running after completion in non-interactive mode",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Web port for the live visualizer dashboard (default: 8080)",
    )
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=None,
        help="Maximum number of RFC files to scan when pointing to a directory",
    )
    parser.add_argument(
        "--target-eligible",
        "-e",
        type=int,
        default=None,
        help="Stop batch processing once N eligible cryptographic protocols have been synthesized",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="rfc*.txt",
        help="Glob pattern for discovering RFC files when scanning a directory (default: 'rfc*.txt')",
    )
    parser.add_argument(
        "--skip-completed",
        action="store_true",
        help="Skip RFCs that already have completed run entries in logs/pipeline_runs.csv",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Run only RFCs recorded in logs/pipeline_runs.csv with status FAILED or PARTIAL (overwriting their rows in-place)",
    )
    parser.add_argument(
        "--random",
        action="store_true",
        help="Randomly sample RFC files when pointing to a directory (useful with --limit)",
    )
    parser.add_argument(
        "--tier0-eligible-only",
        action="store_true",
        help="Pre-filter directory candidates using deterministic Tier 0 frontmatter check before applying --limit",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Path to an existing pipeline_runs.csv or older run directory to copy/seed into this new run's pipeline_runs.csv (source CSV is never modified)",
    )
    parser.add_argument(
        "--keep-ineligible",
        "--reset-eligible",
        dest="keep_ineligible",
        action="store_true",
        help="Prune the active run's pipeline_runs.csv by deleting all rows EXCEPT ineligible RFCs (is_eligible=False), and skip those ineligible RFCs when starting a new batch run",
    )

    args = parser.parse_args()

    # Offline Replay Mode (--view <run_dir>)
    if args.view:
        view_path = Path(args.view)
        if not view_path.exists():
            print(f"Error: Run directory or index does not exist: {view_path}", file=sys.stderr)
            sys.exit(1)

        overview = GLOBAL_EVENT_BUS.load_run_from_disk(view_path)
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
        server = run_visualizer_in_background(port=args.port)
        monitor_url = f"http://127.0.0.1:{server.port}"

        print(f"\n{'='*70}")
        print(f" [OFFLINE REPLAY MONITOR] Active at: {monitor_url}")
        print(f" - Run Directory   : {overview.get('run_directory')}")
        print(f" - Run Metrics CSV : {GLOBAL_EVENT_BUS.get_csv_path()}")
        print(f" - Accepted Tabs   : {len(overview.get('accepted_tabs', []))}")
        print(f" - Filtered / Skips: {overview.get('filtered_total', 0)}")
        print(f"{'='*70}\n")

        if not args.no_visualize:
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

    # Require --csv whenever --keep-ineligible, --skip-completed, or --retry-failed is used
    if (args.keep_ineligible or args.skip_completed or args.retry_failed) and not args.csv:
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
            f"{', '.join(active_flags)} requires --csv <path_to_existing_csv_or_run_dir>. "
            "Pass --csv pointing to the existing CSV ledger (or run directory) these flags should apply to, "
            "or remove those flags to start a fresh run."
        )

    # Standalone --keep-ineligible --csv <path> prune mode (no target_path passed)
    if args.keep_ineligible and not args.target_path:
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
        parser.error("the following arguments are required: target_path (or pass --view <run_dir>)")

    targets = [Path(p) for p in args.target_path]
    for t in targets:
        if not t.exists():
            print(f"Error: Target path does not exist: {t}", file=sys.stderr)
            sys.exit(1)

    if args.csv and not Path(args.csv).exists():
        print(f"Error: Source --csv path does not exist: {args.csv}", file=sys.stderr)
        sys.exit(1)

    # 1. Create Unique Timestamped Run Directory & Per-Run CSV Ledger
    run_timestamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_dir = Path(args.output_dir) if args.output_dir else SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR
    if base_dir.name.startswith("run_"):
        run_root_dir = base_dir
    else:
        run_root_dir = base_dir / f"run_{run_timestamp}"
    run_root_dir.mkdir(parents=True, exist_ok=True)
    run_csv_path = run_root_dir / "pipeline_runs.csv"
    csv_logger = PipelineMetricsCSVLogger(csv_path=run_csv_path)

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

    # 2. Resolve Target Files (Single File, Multiple Files, or Directory Batch)
    if len(targets) > 1 or targets[0].is_file():
        rfc_files = [t for t in targets if t.is_file()]
    elif targets[0].is_dir():
        target = targets[0]
        raw_candidates = [f for f in target.glob(args.pattern) if f.is_file()]
        if args.pattern == "rfc*.txt":
            # Exclude non-numeric index/reference files such as rfc-index-latest.txt or rfc-ref-old.txt
            numeric_candidates = [f for f in raw_candidates if re.fullmatch(r"rfc\d+\.txt", f.name.lower())]
            rfc_files = sorted(numeric_candidates or raw_candidates, key=natural_rfc_sort_key)
        else:
            rfc_files = sorted(raw_candidates, key=natural_rfc_sort_key)
        if not rfc_files:
            # Fallback to all existing txt files if pattern yielded zero
            rfc_files = sorted([f for f in target.glob("*.txt") if f.is_file()], key=natural_rfc_sort_key)
        if not rfc_files:
            print(f"Error: No RFC text files found in directory {target}", file=sys.stderr)
            sys.exit(1)

        if args.retry_failed:
            failed_ids = get_failed_rfc_ids(csv_path=run_csv_path)
            rfc_files = [
                f for f in rfc_files
                if f.stem.upper().replace(" ", "").replace("_", "") in failed_ids
            ]
            print(f"[BATCH] Filtered to {len(rfc_files)} previously FAILED/PARTIAL RFCs from {run_csv_path}")
        elif args.skip_completed:
            completed_ids = get_completed_rfc_ids(csv_path=run_csv_path)
            initial_count = len(rfc_files)
            rfc_files = [
                f for f in rfc_files
                if f.stem.upper().replace(" ", "").replace("_", "") not in completed_ids
            ]
            print(f"[BATCH] Filtered out {initial_count - len(rfc_files)} previously evaluated RFCs ({len(rfc_files)} remaining)")

        if args.tier0_eligible_only:
            before_t0 = len(rfc_files)
            rfc_files = [
                f for f in rfc_files
                if filter_rfc_header(f.read_text(encoding="utf-8", errors="ignore")).is_eligible
            ]
            print(f"[BATCH] Tier 0 pre-filter retained {len(rfc_files)}/{before_t0} candidate RFCs")

        if args.random:
            random.shuffle(rfc_files)
            print("[BATCH] Shuffled candidate RFC list randomly")

        if args.limit and args.limit > 0:
            rfc_files = rfc_files[:args.limit]
            print(f"[BATCH] Processing limited to {len(rfc_files)} RFCs: {[f.name for f in rfc_files]}")
    else:
        print(f"Error: Invalid target path: {targets[0]}", file=sys.stderr)
        sys.exit(1)

    # 3. Launch Visualizer (Default Enabled)
    enable_visualizer = not args.no_visualize
    monitor_url = None
    if enable_visualizer:
        try:
            server = run_visualizer_in_background(port=args.port)
            monitor_url = f"http://127.0.0.1:{server.port}"
            print(f"\n{'='*70}")
            print(f" [LIVE MONITOR] Active at: {monitor_url}")
            print(f"{'='*70}\n")
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

    print(f"[RUN] Created timestamped run directory: {run_root_dir}")
    print(f"[RUN] Master Metadata Index           : {master_index_path}")
    print(f"[RUN] Run CSV Ledger                  : {run_csv_path}")

    # 4. Execution Loop (Models resolve dynamically from prompts/*.md unless CLI overrides are passed)
    results: List[PipelineExecutionSummary] = []
    total_files = len(rfc_files)
    cli_router_model = args.router_model or args.model
    cli_extraction_model = args.extraction_model or args.model
    cli_repair_model = args.repair_model or args.model
    cli_query_model = args.query_model or args.model

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
            eligible_so_far = sum(1 for r in results if r.is_eligible)
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
