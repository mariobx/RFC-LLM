"""Command-line interface for Phase 3 Hindsight Reasoning (<think>) Synthesis."""

import argparse
import sys
from pathlib import Path

from src.logging_config import configure_pipeline_logging
from src.system_config import SYSTEM_CONFIG
from src.generate_think.dspy_think_synthesizer import process_run_directory


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "RFC-LLM Phase 3 (<think> Synthesizer): Generates <protocol>_think.json alongside "
            "<protocol>_trajectory.json using DSPy Hindsight Rationalization + Compiler Backtracking."
        ),
    )
    parser.add_argument(
        "target_path",
        type=str,
        help=(
            "Path to a timestamped run directory (e.g. output/run_2026-10-19_19-17-33), "
            "a metadata_index.json file, an RFC directory, or a specific <protocol>_trajectory.json file."
        ),
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help=(
            "Provider-agnostic model identifier (e.g. 'strata/unsloth-iq4_xs', 'ollama/qwq:32b', 'nous/deepseek/deepseek-chat', "
            "'gemini/gemini-2.5-flash'). Defaults to `model:` in prompts/07_think_token_synthesizer.md."
        ),
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "llm", "deterministic"],
        default="auto",
        help=(
            "Synthesis mode: 'auto' (DSPy/LLM hindsight rationalization with deterministic fallback), "
            "'llm' (DSPy/LLM hindsight rationalization), or 'deterministic' (100%% programmatic AST + "
            "compiler trajectory rendering with zero LLM calls)."
        ),
    )
    parser.add_argument(
        "--min-tier",
        choices=["GOLD", "SILVER", "BRONZE", "REJECTED"],
        default="BRONZE",
        help="Minimum verification quality tier to synthesize <think> tokens for (default: BRONZE).",
    )
    parser.add_argument(
        "--no-jsonl",
        action="store_true",
        help="Do not export consolidated sft_train.jsonl and dpo_pairs.jsonl in the run directory.",
    )

    args = parser.parse_args()
    target = Path(args.target_path)

    if not target.exists():
        print(f"Error: Target path does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    configure_pipeline_logging()
    active_model = args.model or SYSTEM_CONFIG.DEFAULT_THINK_MODEL

    print(f"\n{'=' * 70}")
    print(" RFC-LLM PHASE 3: HINDSIGHT REASONING (<think>) SYNTHESIZER")
    print(f"{'=' * 70}")
    print(f"- Target Path : {target.resolve()}")
    print(f"- Mode        : {args.mode}")
    if args.mode != "deterministic":
        print(f"- Model       : {active_model}")
    print(f"- Min Tier    : {args.min_tier}")
    print(f"{'=' * 70}\n")

    generated_files = process_run_directory(
        target_path=target,
        model=active_model,
        mode=args.mode,
        min_tier=args.min_tier,
        export_jsonl=not args.no_jsonl,
    )

    print(f"\n{'=' * 70}")
    print(f" PHASE 3 COMPLETE: Generated {len(generated_files)} <protocol>_think.json artifact(s)")
    print(f"{'=' * 70}")
    for path in generated_files:
        print(f"  -> {path}")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()
