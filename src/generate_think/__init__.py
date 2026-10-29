"""Phase 3 Hindsight Reasoning (<think>) Synthesizer Package."""

from src.generate_think.think_schema import (
    DPOContrastivePair,
    SynthesizedReasoningSteps,
    ThinkArtifactBundle,
)
from src.generate_think.dspy_think_synthesizer import (
    CPSAHindsightReasoningSignature,
    CPSAHindsightThinkModule,
    compile_deterministic_reasoning_steps,
    generate_think_for_trajectory,
    process_run_directory,
    synthesize_reasoning_steps_via_dspy_or_llm,
)

__all__ = [
    "DPOContrastivePair",
    "SynthesizedReasoningSteps",
    "ThinkArtifactBundle",
    "CPSAHindsightReasoningSignature",
    "CPSAHindsightThinkModule",
    "compile_deterministic_reasoning_steps",
    "generate_think_for_trajectory",
    "process_run_directory",
    "synthesize_reasoning_steps_via_dspy_or_llm",
]
