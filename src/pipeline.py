"""Command-line interface for RFC-LLM synthesis pipeline supporting single RFCs and directory batching."""

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import List, Set

from src.system_config import SYSTEM_CONFIG
from src.main_pipeline_orchestrator import run_rfc_translation_pipeline, PipelineExecutionSummary


def natural_rfc_sort_key(file_path: Path):
    """Sorts RFC files by integer number if present (e.g. rfc10 before rfc100)."""
    match = re.search(r"rfc(\d+)", file_path.stem.lower())
    if match:
        return (0, int(match.group(1)))
    return (1, file_path.name)


def get_completed_rfc_ids() -> Set[str]:
    """Reads logs/pipeline_runs.csv to retrieve RFC IDs that were already evaluated."""
    csv_path = SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv"
    if not csv_path.exists():
        return set()

    completed = set()
    try:
        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
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


def main():
    parser = argparse.ArgumentParser(
        description="RFC-LLM: End-to-End Synthesis of Verified MITRE CPSA Models from IETF RFCs",
    )
    parser.add_argument(
        "target_path",
        type=str,
        help="Path to an RFC text file (such as refrences/all_RFCs/rfc5246.txt) OR a directory containing RFCs",
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
        "--visualize",
        "-v",
        action="store_true",
        help="Launch the live web dashboard visualizer on localhost",
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
        help="Maximum number of RFC files to process when pointing to a directory",
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

    args = parser.parse_args()
    target = Path(args.target_path)

    if not target.exists():
        print(f"Error: Target path does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    # 1. Resolve Target Files (Single File or Directory Batch)
    if target.is_file():
        rfc_files = [target]
    elif target.is_dir():
        rfc_files = sorted(list(target.glob(args.pattern)), key=natural_rfc_sort_key)
        if not rfc_files:
            # Fallback to all txt files if pattern yielded zero
            rfc_files = sorted(list(target.glob("*.txt")), key=natural_rfc_sort_key)
        if not rfc_files:
            print(f"Error: No RFC text files found in directory {target}", file=sys.stderr)
            sys.exit(1)

        if args.skip_completed:
            completed_ids = get_completed_rfc_ids()
            initial_count = len(rfc_files)
            rfc_files = [
                f for f in rfc_files
                if f.stem.upper().replace(" ", "").replace("_", "") not in completed_ids
            ]
            print(f"[BATCH] Filtered out {initial_count - len(rfc_files)} previously evaluated RFCs ({len(rfc_files)} remaining)")

        if args.limit and args.limit > 0:
            rfc_files = rfc_files[:args.limit]
            print(f"[BATCH] Processing limited to first {len(rfc_files)} RFCs")
    else:
        print(f"Error: Invalid target path: {target}", file=sys.stderr)
        sys.exit(1)

    # 2. Launch Visualizer if Requested
    if args.visualize:
        import webbrowser
        from src.visualizer.server import run_visualizer_in_background

        run_visualizer_in_background(port=args.port)
        url = f"http://127.0.0.1:{args.port}"
        print(f"\n[VISUALIZER] Live Synthesis Studio active at: {url}")
        try:
            webbrowser.open(url)
        except Exception:
            pass

    # 3. Execution Loop
    output_base_dir = Path(args.output_dir) if args.output_dir else None
    results: List[PipelineExecutionSummary] = []
    total_files = len(rfc_files)
    active_router_model = args.router_model or args.model or SYSTEM_CONFIG.DEFAULT_ROUTER_MODEL
    active_extraction_model = args.extraction_model or args.model or SYSTEM_CONFIG.DEFAULT_EXTRACTION_MODEL
    active_repair_model = args.repair_model or args.model or SYSTEM_CONFIG.DEFAULT_REPAIR_MODEL

    for idx, rfc_file in enumerate(rfc_files, 1):
        if total_files > 1:
            print(f"\n{'='*70}")
            print(f"[{idx}/{total_files}] Processing RFC: {rfc_file.name}")
            print(f"{'='*70}")

        summary = run_rfc_translation_pipeline(
            rfc_file_path=rfc_file,
            output_dir=output_base_dir,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            repair_model=active_repair_model,
        )
        results.append(summary)

        if total_files == 1:
            # Single-file reporting and exit code
            if summary.build_successful:
                print("\n[SUCCESS] Synthesis & Formal Verification Completed!")
                print(f"Protocol: {summary.protocol_name}")
                print(f"Verified Shapes XHTML: {summary.build_artifacts.shapes_graph_xhtml_path}")
                sys.exit(0)
            elif summary.roletran_passed:
                print(f"\n[PARTIAL] Roletran passed, but MITRE build failed: {summary.error_message}")
                sys.exit(1)
            else:
                print(f"\n[HALTED] Pipeline stopped: {summary.error_message}")
                sys.exit(2)

    # 4. Batch Summary Report
    print(f"\n{'='*70}")
    print(f"RFC-LLM BATCH SYNTHESIS REPORT ({total_files} RFCs Processed)")
    print(f"{'='*70}")
    verified_count = sum(1 for r in results if r.build_successful)
    eligible_count = sum(1 for r in results if r.is_eligible)
    ineligible_count = sum(1 for r in results if not r.is_eligible)
    roletran_failed = sum(1 for r in results if r.is_eligible and not r.roletran_passed)
    solver_failed = sum(1 for r in results if r.roletran_passed and not r.build_successful)

    print(f"• Total Processed      : {total_files}")
    print(f"• Ineligible (Filtered): {ineligible_count}")
    print(f"• Eligible Protocols   : {eligible_count}")
    print(f"• Formally Verified    : {verified_count}")
    if roletran_failed:
        print(f"• Roletran Failed      : {roletran_failed}")
    if solver_failed:
        print(f"• Solver Failed        : {solver_failed}")
    print(f"• Run Metrics Logged   : {SYSTEM_CONFIG.LOGS_DIR / 'pipeline_runs.csv'}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
