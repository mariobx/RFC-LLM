"""Pydantic Schemas for Phase 3 Hindsight Reasoning (<think>) Synthesis and SFT/DPO Curation."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SynthesizedReasoningSteps(BaseModel):
    """Structured 5-phase hindsight reasoning steps with compiler-feedback backtracking."""

    step1_protocol_and_algebra: str = Field(
        ...,
        description=(
            "First-person deduction of the protocol scope, participating principals, "
            "and why 'basic' or 'diffie-hellman' message algebra is required by the RFC text."
        ),
    )
    step2_principals_and_variables: str = Field(
        ...,
        description=(
            "First-person mapping of RFC message fields to CPSA variable identifiers and sorts "
            "(name, text, data, skey, akey, rndx, expt, chan, locn, mesg), justifying sort rules."
        ),
    )
    step3_message_flow_and_terms: str = Field(
        ...,
        description=(
            "Step-by-step derivation of each role's ordered trace events (send/recv/load/stor) "
            "and nested S-expression cryptographic terms (cat, enc, hash, pubk, privk, invk, ltk, exp, gen)."
        ),
    )
    step4_compiler_backtracking_and_invariants: str = Field(
        ...,
        description=(
            "Explicit self-correction, backtracking ('Wait—let me check...'), and formal verification "
            "of CPSA 4.4.9 compiler invariants: cpsa4roletran term destructibility, inputs/outputs "
            "disjointness from uniq-orig/uniq-gen, Equation 10.1 encryption key sort rules, and "
            "avoidance/resolution of any Stage 5 or Stage 6 compiler diagnostics."
        ),
    )
    step5_preskeleton_verdicts_and_goals: str = Field(
        ...,
        description=(
            "Derivation of the 3-Point-of-View defskeleton blocks: why participant POV skeletons "
            "omit deflistener to realize multi-strand authentication shapes, and how the secrecy "
            "skeleton uses deflistener alongside non-orig/uniq-orig/uniq-gen assumptions."
        ),
    )
    full_thinking_monologue: str = Field(
        ...,
        description=(
            "Cohesive, natural first-person reasoning monologue integrating Steps 1-5 (including "
            "backtracking and compiler invariant checks) without <think> wrapper tags. Never mention "
            "that a ground-truth AST or .scm was provided in advance."
        ),
    )


class DPOContrastivePair(BaseModel):
    """Compiler-verified Direct Preference Optimization (DPO) contrastive pair."""

    stage: str = Field(..., description="Verification stage where rejection occurred ('stage5_roletran' or 'stage6_cpsa4')")
    attempt_number: int = Field(..., description="1-based repair attempt index")
    compiler_diagnostic: str = Field(..., description="Exact compiler or solver error diagnostic that rejected the candidate")
    rag_query: Optional[str] = Field(default=None, description="RAG query used to retrieve MITRE CPSA manual guidance")
    retrieved_chunk_ids: List[int] = Field(default_factory=list, description="MITRE CPSA manual chunk IDs retrieved")
    prompt_messages: List[Dict[str, str]] = Field(
        ...,
        description="Input conversation messages ([system, user]) shared by chosen and rejected completions",
    )
    chosen_response: str = Field(
        ...,
        description="Verified completion containing <think>...</think> followed by the final verified .scm code",
    )
    rejected_response: str = Field(
        ...,
        description="Compiler-rejected .scm specification from this failed attempt",
    )


class ThinkArtifactBundle(BaseModel):
    """Complete `<protocol>_think.json` artifact saved alongside `<protocol>_trajectory.json`."""

    schema_version: str = Field(default="1.0.0", description="Schema version for <protocol>_think.json")
    run_id: str = Field(..., description="Run identifier matching <protocol>_trajectory.json")
    timestamp_utc: str = Field(..., description="UTC ISO-8601 timestamp when thinking tokens were synthesized")
    rfc_id: str = Field(..., description="RFC identifier (e.g. 'RFC 9528')")
    rfc_title: str = Field(..., description="RFC document title")
    protocol_name: str = Field(..., description="Synthesized CPSA protocol name")
    algebra: str = Field(..., description="CPSA message algebra ('basic' or 'diffie-hellman')")
    quality_tier: str = Field(..., description="Programmatic verification quality tier (GOLD, SILVER, BRONZE, REJECTED)")
    synthesis_mode: str = Field(
        ...,
        description="Method used to synthesize thinking tokens ('dspy_hindsight_llm' or 'deterministic_ast_compiler')",
    )
    source_trajectory_file: str = Field(..., description="Filename of the source <protocol>_trajectory.json")
    target_scm_file: str = Field(..., description="Filename of the target <protocol>.scm")
    reasoning_steps: SynthesizedReasoningSteps = Field(
        ...,
        description="Structured 5-step reasoning breakdown and full monologue",
    )
    thinking_block: str = Field(
        ...,
        description="Complete <think>\\n...\\n</think> block ready for SFT injection",
    )
    sft_messages: List[Dict[str, str]] = Field(
        ...,
        description="Ready-to-train 3-turn chat messages ([system, user, assistant]) where assistant combines <think> + .scm",
    )
    dpo_contrastive_pairs: List[DPOContrastivePair] = Field(
        default_factory=list,
        description="Contrastive (chosen vs. compiler-rejected) pairs extracted from Stage 5 and Stage 6 repair attempts",
    )
