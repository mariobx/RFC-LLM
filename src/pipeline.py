"""Command-line interface for RFC-LLM synthesis pipeline."""

import argparse
import sys
from pathlib import Path

from src.main_pipeline_orchestrator import run_rfc_translation_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="RFC-LLM: End-to-End Synthesis of Verified MITRE CPSA Models from IETF RFCs",
    )
    parser.add_argument(
        "rfc_path",
        type=str,
        help="Path to the RFC text file (such as refrences/all_RFCs/rfc####.txt)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default=None,
        help="Directory to place synthesized models and build artifacts",
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

    args = parser.parse_args()
    rfc_file = Path(args.rfc_path)
    output_dir = Path(args.output_dir) if args.output_dir else None

    summary = run_rfc_translation_pipeline(
        rfc_file_path=rfc_file,
        output_dir=output_dir,
        router_model=args.router_model,
        extraction_model=args.extraction_model,
    )

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


if __name__ == "__main__":
    main()
