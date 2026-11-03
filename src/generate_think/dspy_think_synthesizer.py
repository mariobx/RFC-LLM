"""Phase 3 Agentic DSPy Hindsight Reasoning (<think>) Synthesizer.

Implements state-of-the-art Hindsight Rationalization (STaR) + Compiler-Feedback
Backtracking (Stanford s1 / OpenThoughts) to generate `<protocol>_think.json`
inside each RFC directory alongside `<protocol>_trajectory.json` and `<protocol>.scm`.
"""

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import dspy
import json_repair
import litellm

from src.generate_think.think_schema import (
    DPOContrastivePair,
    SynthesizedReasoningSteps,
    ThinkArtifactBundle,
)
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_THINK_SYNTHESIZER,
    build_schema_system_prompt,
    load_prompt,
    load_prompt_spec,
    parse_llm_json,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("think_synthesizer")

# Quality tier ranking for filtering
TIER_RANK: Dict[str, int] = {
    "GOLD": 4,
    "SILVER": 3,
    "BRONZE": 2,
    "REJECTED": 1,
    "INELIGIBLE": 0,
}

SFT_SYSTEM_PROMPT: str = (
    "You are a formal methods expert specializing in MITRE CPSA 4.4.9. "
    "Given an IETF RFC protocol specification, reason step-by-step inside <think>...</think> tags "
    "about the participating principals, message algebra sorts, role traces, origination and "
    "executability invariants, and 3-Point-of-View security preskeletons, then emit a formally "
    "verifiable CPSA Scheme (.scm) specification."
)


class CPSAHindsightReasoningSignature(dspy.Signature):
    """Synthesize a forward-looking, first-person MITRE CPSA 4.4.9 <think> deduction trace from an RFC slice.
    Write strictly as if you are designing the CPSA model from scratch while reading the RFC.
    NEVER mention 'compiler backtracking history', 'preskeleton verdicts', 'provided AST', or any post-hoc verification results;
    instead, use exact CPSA variable names, sorts (name, text, data, skey, akey, rndx, expt, chan), S-expression terms,
    and natural self-checks ('Wait—let me verify CPSA's executability rules...').
    """

    rfc_context_and_slice: str = dspy.InputField(
        desc="RFC ID, Title, Participating Principals, Selected Sections, and Verbatim RFC Specification Slice"
    )
    target_cpsa_identifiers_and_terms: str = dspy.InputField(
        desc="Exact CPSA variable names, sorts, role traces, and skeleton structures that your forward-looking reasoning must derive"
    )
    cpsa_invariants_and_self_checks: str = dspy.InputField(
        desc="CPSA 4.4.9 sort, roletran executability, and origination pitfalls to weave in as 'Wait—let me verify...' self-correction thoughts"
    )
    step1_protocol_and_algebra: str = dspy.OutputField(
        desc="Step 1: First-person deduction of protocol scope, principals, and why basic or diffie-hellman algebra is required"
    )
    step2_principals_and_variables: str = dspy.OutputField(
        desc="Step 2: First-person mapping of RFC fields to every exact CPSA variable identifier and sort (rndx vs expt, text, data, skey, akey, name, chan)"
    )
    step3_message_flow_and_terms: str = dspy.OutputField(
        desc="Step 3: First-person derivation of each role's ordered send/recv events with exact S-expression terms ((cat ...), (enc ...), (exp (gen) ...))"
    )
    step4_compiler_backtracking_and_invariants: str = dspy.OutputField(
        desc="Step 4: First-person self-check ('Wait—let me check CPSA's rules...') verifying uniq-orig, uniq-gen, non-orig, and roletran (inputs ...) destructibility"
    )
    step5_preskeleton_verdicts_and_goals: str = dspy.OutputField(
        desc="Step 5: First-person construction of the 3 defskeleton blocks (Initiator POV without deflistener, Responder POV without deflistener, and Secrecy POV with deflistener)"
    )
    full_thinking_monologue: str = dspy.OutputField(
        desc="Complete, detailed first-person reasoning monologue integrating all exact variable names, sorts, S-expressions, and 'Wait—let me check...' self-corrections from Steps 1-5"
    )


class CPSAHindsightThinkModule(dspy.Module):
    """DSPy Module wrapping CPSAHindsightReasoningSignature for provider-agnostic <think> generation."""

    def __init__(self) -> None:
        super().__init__()
        # Dynamically bind the externalized prompts/07_think_token_synthesizer.md instructions
        CPSAHindsightReasoningSignature.__doc__ = load_prompt(PROMPT_THINK_SYNTHESIZER)
        self.synthesize = dspy.Predict(CPSAHindsightReasoningSignature)

    def forward(
        self,
        rfc_context_and_slice: str,
        target_cpsa_identifiers_and_terms: str,
        cpsa_invariants_and_self_checks: str,
    ) -> dspy.Prediction:
        return self.synthesize(
            rfc_context_and_slice=rfc_context_and_slice,
            target_cpsa_identifiers_and_terms=target_cpsa_identifiers_and_terms,
            cpsa_invariants_and_self_checks=cpsa_invariants_and_self_checks,
        )


def _format_sexpr(term: Any) -> str:
    """Renders a Python list/str term into a compact CPSA S-expression string."""
    if isinstance(term, list):
        return "(" + " ".join(_format_sexpr(t) for t in term) + ")"
    return str(term)


def _extract_compiler_backtracking_summary(trajectory_data: Dict[str, Any]) -> str:
    """Extracts Stage 2, Stage 5, and Stage 6 pitfalls as forward-looking CPSA design self-checks."""
    lines: List[str] = []
    algebra = trajectory_data.get("rfc_metadata", {}).get("algebra", "basic")

    stage2 = trajectory_data.get("stage2_initial_extraction", {})
    if stage2.get("schema_self_correction_triggered") and stage2.get("schema_validation_error"):
        lines.append(
            f"- Self-check on CPSA AST scoping: avoid `{stage2['schema_validation_error']}`."
        )

    stage5 = trajectory_data.get("stage5_preflight_gate", {})
    for att in stage5.get("repair_attempts", []):
        diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or "roletran executability failure"
        lines.append(
            f"- Backtracking self-check ('Wait—let me check role executability...'): if we are not careful, "
            f"`{stage5.get('validator_binary', 'cpsa4roletran')}` would reject with `{diag.splitlines()[0]}`. "
            f"Explain how the role's `(inputs ...)` and key declarations avoid this error."
        )

    stage6 = trajectory_data.get("stage6_cpsa4_solver", {})
    for att in stage6.get("repair_attempts", []):
        diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or "cpsa4 solver failure"
        lines.append(
            f"- Backtracking self-check ('Hold on—let me check CPSA sort and origination rules...'): "
            f"avoid `{diag.splitlines()[0]}` by ensuring sort and origination consistency across roles and skeletons."
        )

    if algebra == "diffie-hellman":
        lines.append(
            "- Proactive DH self-check ('Wait—let me verify CPSA's Diffie-Hellman exponent rules...'): "
            "any fresh private exponent sent in `(exp (gen) x)` must have sort `rndx` with `(uniq-gen x)`, "
            "while the peer receiving that public share must type the received exponent variable as `expt` "
            "(because CPSA requires `rndx` to be sent first and `expt` to be received first)."
        )
    else:
        lines.append(
            "- Proactive basic-algebra self-check ('Wait—let me verify CPSA Equation 10.1 and roletran rules...'): "
            "encryption keys in `(enc ...)` must have sort `skey` or `akey` (never `mesg`), and `(inputs ...)` "
            "must include trace channels and pre-known keys without overlapping `(uniq-orig ...)`."
        )

    lines.append(
        "- Proactive 3-POV Skeleton self-check: construct separate participant POV skeletons (`defstrandmax` with "
        "NO `deflistener`) to test multi-strand authentication, and a dedicated secrecy skeleton with "
        "`(deflistener ...)` and `(non-orig ...)` to test confidentiality."
    )
    return "\n".join(lines)


def compile_deterministic_reasoning_steps(trajectory_data: Dict[str, Any]) -> SynthesizedReasoningSteps:
    """Deterministically compiles a rich 5-step <think> trace directly from the AST and compiler trajectory.

    Requires zero LLM calls while preserving 100% identifier fidelity and compiler backtracking checks.
    """
    rfc_meta = trajectory_data.get("rfc_metadata", {})
    rfc_id = rfc_meta.get("rfc_id", "Unknown RFC")
    rfc_title = rfc_meta.get("rfc_title", "Unknown Protocol")
    algebra = rfc_meta.get("algebra", "basic")
    principals = rfc_meta.get("participating_principals", [])
    sections = rfc_meta.get("selected_sections", [])

    final_out = trajectory_data.get("final_verified_output", {})
    final_ast = final_out.get("final_ast") or trajectory_data.get("stage2_initial_extraction", {}).get("initial_ast") or {}
    herald_comment = final_ast.get("herald_comment", "")
    roles = final_ast.get("roles", [])
    skeletons = final_ast.get("skeletons", [])

    # Step 1: Protocol & Algebra
    algebra_rationale = (
        "Because the handshake employs ephemeral Diffie-Hellman exponentiation `(exp (gen) ...)` to establish "
        "shared session keys, we must select the MITRE CPSA `diffie-hellman` message algebra rather than `basic`."
        if algebra == "diffie-hellman"
        else "Because the protocol relies on symmetric/asymmetric encryption, nonces, hashes, and signatures without "
        "Diffie-Hellman group exponentiation, we select the MITRE CPSA `basic` message algebra."
    )
    step1 = (
        f"Let's analyze {rfc_id} ({rfc_title}), focusing on sections {', '.join(sections) or 'describing the core exchange'}. "
        f"The interactive cryptographic exchange involves {len(roles)} primary roles ({', '.join(r.get('role_name', '') for r in roles) or ', '.join(principals)}). "
        f"{algebra_rationale} "
        f"Scope note: {herald_comment}"
    ).strip()

    # Step 2: Principals & Variables
    role_var_paragraphs: List[str] = []
    for role in roles:
        r_name = role.get("role_name", "role")
        r_desc = role.get("description") or f"Participant role `{r_name}`"
        var_items: List[str] = []
        for var in role.get("variables", []):
            v_name = var.get("name")
            v_sort = var.get("sort")
            v_rfc = var.get("rfc_field")
            v_desc = var.get("description")
            mapping_str = f"`{v_name}` (sort `{v_sort}`)"
            if v_rfc:
                mapping_str += f" [RFC: {v_rfc}]"
            if v_desc:
                mapping_str += f": {v_desc}"
            var_items.append(mapping_str)
        role_var_paragraphs.append(
            f"For role `{r_name}` ({r_desc}), we declare the following typed variables in `(vars ...)`: "
            + "; ".join(var_items)
            + "."
        )
    step2 = "\n".join(role_var_paragraphs) if role_var_paragraphs else "We map each principal's variables to strict CPSA 4.4.9 sorts."

    # Step 3: Message Flow & Terms
    trace_paragraphs: List[str] = []
    for role in roles:
        r_name = role.get("role_name", "role")
        ev_lines: List[str] = []
        for idx, ev in enumerate(role.get("trace", [])):
            direction = ev.get("direction", "send")
            chan = ev.get("channel") or ev.get("location") or ""
            term_str = _format_sexpr(ev.get("message_term", ""))
            ev_desc = ev.get("description") or f"Event {idx}"
            if chan:
                sexpr_ev = f"({direction} {chan} {term_str})"
            else:
                sexpr_ev = f"({direction} {term_str})"
            ev_lines.append(f"Event {idx} ({ev_desc}) -> `{sexpr_ev}`")
        trace_paragraphs.append(
            f"In role `{r_name}`, the ordered `(trace ...)` sequence is: " + "; ".join(ev_lines) + "."
        )
    step3 = "\n".join(trace_paragraphs) if trace_paragraphs else "We construct the ordered send/recv trace events for each role."

    # Step 4: Compiler Backtracking & Invariants
    backtrack_notes: List[str] = []
    stage5 = trajectory_data.get("stage5_preflight_gate", {})
    stage6 = trajectory_data.get("stage6_cpsa4_solver", {})
    for att in stage5.get("repair_attempts", []):
        diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or ""
        backtrack_notes.append(
            f"Wait—let me check pre-flight role executability (`{stage5.get('validator_binary', 'cpsa4roletran')}`): "
            f"an initial formulation would trigger `{diag.splitlines()[0] if diag else 'an executability error'}`. "
            f"We must ensure every received term can be destructured using keys already in scope or declared in `(inputs ...)`."
        )
    for att in stage6.get("repair_attempts", []):
        diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or ""
        backtrack_notes.append(
            f"Hold on—when `cpsa4` evaluates the search space, we must avoid `{diag.splitlines()[0] if diag else 'solver rejection'}` "
            f"by aligning sort declarations and origination assumptions across roles and skeletons."
        )

    for role in roles:
        r_name = role.get("role_name", "role")
        uo = [_format_sexpr(x) for x in role.get("unique_originating", [])]
        ug = [_format_sexpr(x) for x in role.get("unique_generated", [])]
        no = [_format_sexpr(x) for x in role.get("non_originating", [])]
        ins = [_format_sexpr(x) for x in role.get("inputs", [])]
        outs = [_format_sexpr(x) for x in role.get("outputs", [])]
        inv_parts: List[str] = []
        if uo:
            inv_parts.append(f"`(uniq-orig {' '.join(uo)})` for freshly originated nonces/identifiers")
        if ug:
            inv_parts.append(f"`(uniq-gen {' '.join(ug)})` for fresh DH exponents of sort `rndx`")
        if no:
            inv_parts.append(f"`(non-orig {' '.join(no)})` for uncompromised long-term keys")
        if ins:
            inv_parts.append(f"`(inputs {' '.join(ins)})` (excluding any `uniq-orig`/`uniq-gen` terms per cpsa4roletran rules)")
        if outs:
            inv_parts.append(f"`(outputs {' '.join(outs)})`")
        if inv_parts:
            backtrack_notes.append(f"For role `{r_name}`, we enforce: " + ", ".join(inv_parts) + ".")

    if algebra == "diffie-hellman":
        backtrack_notes.append(
            "Wait—let me verify CPSA's Diffie-Hellman exponent discipline: any exponent chosen freshly by a role "
            "and sent first in `(exp (gen) x)` must have sort `rndx` and `(uniq-gen x)`, whereas the peer role "
            "receiving that public share must declare its corresponding exponent variable with sort `expt` "
            "(since CPSA requires `expt` variables to be received first and `rndx` variables to be sent first)."
        )
    else:
        backtrack_notes.append(
            "Wait—let me verify MITRE CPSA Equation 10.1 and `cpsa4roletran` invariants: no variable of sort `mesg` "
            "is used as an encryption key in `(enc ...)`, and every role's `(inputs ...)` contains its trace channels "
            "and initial keys without overlapping `(uniq-orig ...)`."
        )
    step4 = " ".join(backtrack_notes)

    # Step 5: Preskeletons
    skel_notes: List[str] = []
    for idx, skel in enumerate(skeletons):
        s_desc = skel.get("description") or skel.get("comment") or f"Preskeleton {idx + 1}"
        strands_str = ", ".join(f"`(defstrandmax {s.get('role_name')})`" for s in skel.get("strands", []))
        listeners = [_format_sexpr(l) for l in skel.get("listeners", [])]
        non_orig = [_format_sexpr(n) for n in skel.get("non_originating", [])]
        if listeners:
            skel_notes.append(
                f"Skeleton {idx + 1} ({s_desc}): instantiates {strands_str} with `(deflistener {' '.join(listeners)})` "
                f"and `(non-orig {' '.join(non_orig)})` to test whether the penetrator can learn the secret."
            )
        else:
            skel_notes.append(
                f"Skeleton {idx + 1} ({s_desc}): pure participant POV instantiating {strands_str} with NO `deflistener` "
                f"and `(non-orig {' '.join(non_orig)})` so `cpsa4` can realize multi-strand authenticated shapes."
            )
    step5 = " ".join(skel_notes) if skel_notes else "We construct participant POV and secrecy preskeletons."

    full_monologue = (
        f"1. Protocol Scope & Message Algebra:\n{step1}\n\n"
        f"2. Principal Roles & Variable Sort Mapping:\n{step2}\n\n"
        f"3. Message Exchange Trace & Term Construction:\n{step3}\n\n"
        f"4. Compiler Invariants & Self-Correction Checks:\n{step4}\n\n"
        f"5. Point-of-View & Secrecy Preskeleton Formulation:\n{step5}"
    )

    return SynthesizedReasoningSteps(
        step1_protocol_and_algebra=step1,
        step2_principals_and_variables=step2,
        step3_message_flow_and_terms=step3,
        step4_compiler_backtracking_and_invariants=step4,
        step5_preskeleton_verdicts_and_goals=step5,
        full_thinking_monologue=full_monologue,
    )


def _sanitize_hindsight_leakage(text: str) -> str:
    """Removes any accidental references to pre-supplied AST/trajectory artifacts."""
    banned_patterns = [
        (
            r"(?i)\bin the (?:provided|given|supplied) (?:final_ast|initial_ast|final_scm|initial_scm|ast|scm|trajectory|scaffold)\b",
            "in our CPSA model",
        ),
        (
            r"(?i)\blooking at the (?:provided|given|supplied) (?:final_ast|initial_ast|final_scm|initial_scm|ast|scm|code|solution)\b",
            "analyzing the protocol structure",
        ),
        (r"(?i)\baccording to the trajectory metadata\b", "by CPSA's strand-space semantics"),
        (r"(?i)\bthe compiler backtracking history (?:indicates|shows) that\b", "Wait—let me verify CPSA's compiler invariants:"),
        (r"(?i)\bthe preskeleton verdicts confirm that\b", "To verify our security goals in CPSA,"),
    ]
    cleaned = text.strip()
    for pat, repl in banned_patterns:
        cleaned = re.sub(pat, repl, cleaned)
    # Strip any outer <think> or </think> tags if the model included them inside full_thinking_monologue
    cleaned = re.sub(r"^\s*<think>\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*</think>\s*$", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def _compose_comprehensive_monologue(steps: SynthesizedReasoningSteps) -> str:
    """Ensures full_thinking_monologue preserves all concrete variable mappings, sorts, and S-expression terms."""
    if "(cat" in steps.full_thinking_monologue or "(enc" in steps.full_thinking_monologue or "(exp" in steps.full_thinking_monologue:
        return steps.full_thinking_monologue
    return (
        f"1. Protocol Scope & Message Algebra:\n{steps.step1_protocol_and_algebra}\n\n"
        f"2. Principal Roles & Variable Sort Mapping:\n{steps.step2_principals_and_variables}\n\n"
        f"3. Message Exchange Trace & Term Construction:\n{steps.step3_message_flow_and_terms}\n\n"
        f"4. Compiler Invariants & Self-Correction Checks:\n{steps.step4_compiler_backtracking_and_invariants}\n\n"
        f"5. Point-of-View & Secrecy Preskeleton Formulation:\n{steps.step5_preskeleton_verdicts_and_goals}"
    )


def synthesize_reasoning_steps_via_dspy_or_llm(
    trajectory_data: Dict[str, Any],
    model: Optional[str] = None,
) -> Tuple[SynthesizedReasoningSteps, str]:
    """Synthesizes `<think>` steps using DSPy / LiteLLM provider-agnostic routing, with deterministic fallback."""
    think_spec = load_prompt_spec(PROMPT_THINK_SYNTHESIZER)
    model_name = model or think_spec.model
    sampling_temp = think_spec.temperature if think_spec.temperature is not None else 0.2
    rfc_meta = trajectory_data.get("rfc_metadata", {})
    rfc_id = rfc_meta.get("rfc_id", "Unknown RFC")
    rfc_title = rfc_meta.get("rfc_title", "Unknown Protocol")
    principals = rfc_meta.get("participating_principals", [])
    sections = rfc_meta.get("selected_sections", [])
    verbatim_slice = rfc_meta.get("verbatim_rfc_slice", "")

    final_out = trajectory_data.get("final_verified_output", {})
    final_ast = final_out.get("final_ast") or trajectory_data.get("stage2_initial_extraction", {}).get("initial_ast")
    final_scm = final_out.get("final_scm_with_header") or trajectory_data.get("stage2_initial_extraction", {}).get("initial_scm") or ""

    rfc_context_and_slice = (
        f"RFC ID: {rfc_id}\n"
        f"Title: {rfc_title}\n"
        f"Participating Principals: {', '.join(principals)}\n"
        f"Selected Sections: {', '.join(sections)}\n\n"
        f"Verbatim RFC Specification Slice:\n{verbatim_slice}"
    )
    verified_scaffold = (
        f"Verified CPSA AST (JSON):\n{json.dumps(final_ast, indent=2)}\n\n"
        f"Verified CPSA Scheme (.scm):\n{final_scm}"
    )
    backtracking_history = _extract_compiler_backtracking_summary(trajectory_data)

    llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
        model_name,
        temperature=sampling_temp,
        max_tokens=think_spec.max_tokens,
    )

    # First attempt: DSPy CPSAHindsightThinkModule configured with provider-agnostic LM
    try:
        logger.info("Synthesizing <think> reasoning trace for %s using DSPy module (%s)", rfc_id, model_name)
        lm_params = {k: v for k, v in llm_kwargs.items() if k != "model"}
        dspy_lm = dspy.LM(model=llm_kwargs["model"], **lm_params)
        module = CPSAHindsightThinkModule()
        with dspy.context(lm=dspy_lm):
            pred = module(
                rfc_context_and_slice=rfc_context_and_slice,
                target_cpsa_identifiers_and_terms=verified_scaffold,
                cpsa_invariants_and_self_checks=backtracking_history,
            )
        steps = SynthesizedReasoningSteps(
            step1_protocol_and_algebra=_sanitize_hindsight_leakage(str(pred.step1_protocol_and_algebra)),
            step2_principals_and_variables=_sanitize_hindsight_leakage(str(pred.step2_principals_and_variables)),
            step3_message_flow_and_terms=_sanitize_hindsight_leakage(str(pred.step3_message_flow_and_terms)),
            step4_compiler_backtracking_and_invariants=_sanitize_hindsight_leakage(
                str(pred.step4_compiler_backtracking_and_invariants)
            ),
            step5_preskeleton_verdicts_and_goals=_sanitize_hindsight_leakage(
                str(pred.step5_preskeleton_verdicts_and_goals)
            ),
            full_thinking_monologue=_sanitize_hindsight_leakage(str(pred.full_thinking_monologue)),
        )
        steps.full_thinking_monologue = _compose_comprehensive_monologue(steps)
        if len(steps.full_thinking_monologue) >= 120:
            return steps, "dspy_hindsight_llm"
    except Exception as dspy_exc:
        logger.warning(
            "DSPy adapter call for %s encountered (%s); attempting direct JSON-schema completion via LiteLLM...",
            rfc_id,
            dspy_exc,
        )

    # Second attempt: Direct LiteLLM JSON-schema completion using prompts/07_think_token_synthesizer.md
    try:
        system_prompt = build_schema_system_prompt(
            PROMPT_THINK_SYNTHESIZER,
            SynthesizedReasoningSteps,
        )
        user_prompt = (
            f"{rfc_context_and_slice}\n\n"
            f"Compiler & Solver Backtracking Points to Include as Internal Self-Checks:\n{backtracking_history}\n\n"
            f"Target Ground-Truth Scaffold (Arrive at these exact identifiers/terms via first-principles deduction "
            f"without ever mentioning they were provided):\n{verified_scaffold}"
        )
        direct_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=sampling_temp,
            max_tokens=think_spec.max_tokens,
            json_mode=True,
        )
        response = litellm.completion(
            **direct_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=think_spec.timeout,
        )
        raw_content = response.choices[0].message.content
        parsed = parse_llm_json(raw_content)

        steps = SynthesizedReasoningSteps.model_validate(parsed)
        steps.step1_protocol_and_algebra = _sanitize_hindsight_leakage(steps.step1_protocol_and_algebra)
        steps.step2_principals_and_variables = _sanitize_hindsight_leakage(steps.step2_principals_and_variables)
        steps.step3_message_flow_and_terms = _sanitize_hindsight_leakage(steps.step3_message_flow_and_terms)
        steps.step4_compiler_backtracking_and_invariants = _sanitize_hindsight_leakage(
            steps.step4_compiler_backtracking_and_invariants
        )
        steps.step5_preskeleton_verdicts_and_goals = _sanitize_hindsight_leakage(
            steps.step5_preskeleton_verdicts_and_goals
        )
        steps.full_thinking_monologue = _sanitize_hindsight_leakage(steps.full_thinking_monologue)
        steps.full_thinking_monologue = _compose_comprehensive_monologue(steps)
        return steps, "dspy_hindsight_llm"
    except Exception as llm_exc:
        logger.warning(
            "LLM synthesis failed for %s (%s); falling back to deterministic AST + compiler trajectory compiler.",
            rfc_id,
            llm_exc,
        )
        return compile_deterministic_reasoning_steps(trajectory_data), "deterministic_ast_compiler"


def _build_sft_and_dpo_records(
    trajectory_data: Dict[str, Any],
    thinking_block: str,
) -> Tuple[List[Dict[str, str]], List[DPOContrastivePair]]:
    """Constructs the 3-turn SFT chat payload and extracts any compiler-rejected DPO contrastive pairs."""
    rfc_meta = trajectory_data.get("rfc_metadata", {})
    rfc_id = rfc_meta.get("rfc_id", "Unknown RFC")
    rfc_title = rfc_meta.get("rfc_title", "Unknown Protocol")
    verbatim_slice = rfc_meta.get("verbatim_rfc_slice", "")

    final_out = trajectory_data.get("final_verified_output", {})
    final_scm = (
        final_out.get("final_scm_with_header")
        or trajectory_data.get("stage2_initial_extraction", {}).get("initial_scm")
        or ""
    ).strip()

    user_message = (
        f"Synthesize a formally verified MITRE CPSA 4.4.9 specification for {rfc_id} ({rfc_title}) "
        f"from the following verbatim RFC specification sections:\n\n{verbatim_slice}"
    )
    chosen_completion = f"{thinking_block}\n\n{final_scm}"

    prompt_messages = [
        {"role": "system", "content": SFT_SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
    sft_messages = prompt_messages + [
        {"role": "assistant", "content": chosen_completion},
    ]

    dpo_pairs: List[DPOContrastivePair] = []
    for stage_key, stage_label in (
        ("stage5_preflight_gate", "stage5_roletran"),
        ("stage6_cpsa4_solver", "stage6_cpsa4"),
    ):
        stage_obj = trajectory_data.get(stage_key, {})
        for att in stage_obj.get("repair_attempts", []):
            rejected_scm = (att.get("rejected_scm") or "").strip()
            if not rejected_scm or rejected_scm == final_scm:
                continue
            diag = att.get("parsed_diagnostic") or att.get("raw_stderr") or "Compiler verification failure"
            dpo_pairs.append(
                DPOContrastivePair(
                    stage=stage_label,
                    attempt_number=int(att.get("attempt_number", 1)),
                    compiler_diagnostic=diag,
                    rag_query=att.get("rag_query"),
                    retrieved_chunk_ids=list(att.get("retrieved_chunk_ids", [])),
                    prompt_messages=prompt_messages,
                    chosen_response=chosen_completion,
                    rejected_response=rejected_scm,
                )
            )

    return sft_messages, dpo_pairs


def update_metadata_index_with_think_file(
    run_root_dir: Path,
    trajectory_json_path: Path,
    think_json_path: Path,
) -> Optional[Path]:
    """Updates `metadata_index.json` in `run_root_dir` to register the generated `<protocol>_think.json`."""
    index_path = run_root_dir / "metadata_index.json"
    if not index_path.exists():
        return None

    try:
        index_data = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception:
        return None

    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    index_data["updated_at_utc"] = now_utc

    if "think_json_files" not in index_data:
        index_data["think_json_files"] = []

    think_abs = str(think_json_path.resolve())
    traj_abs = str(trajectory_json_path.resolve())

    if think_abs not in index_data["think_json_files"]:
        index_data["think_json_files"].append(think_abs)

    for run_entry in index_data.get("runs", []):
        if run_entry.get("metadata_json_file") == traj_abs:
            run_entry["think_json_file"] = think_abs

    index_path.write_text(json.dumps(index_data, indent=2), encoding="utf-8")
    return index_path


def generate_think_for_trajectory(
    trajectory_json_path: Path,
    model: Optional[str] = None,
    mode: str = "auto",
    run_root_dir: Optional[Path] = None,
) -> Path:
    """Reads `<protocol>_trajectory.json`, synthesizes `<think>` tokens, writes `<protocol>_think.json`
    in the same RFC directory, and updates `metadata_index.json` if present.
    """
    trajectory_json_path = trajectory_json_path.resolve()
    if not trajectory_json_path.exists():
        raise FileNotFoundError(f"Trajectory JSON not found: {trajectory_json_path}")

    trajectory_data = json.loads(trajectory_json_path.read_text(encoding="utf-8"))
    rfc_dir = trajectory_json_path.parent
    stem = re.sub(r"_trajectory$", "", trajectory_json_path.stem)
    think_json_path = rfc_dir / f"{stem}_think.json"
    scm_filename = f"{stem}.scm"

    if mode == "deterministic":
        reasoning_steps = compile_deterministic_reasoning_steps(trajectory_data)
        synthesis_mode = "deterministic_ast_compiler"
    else:
        reasoning_steps, synthesis_mode = synthesize_reasoning_steps_via_dspy_or_llm(
            trajectory_data=trajectory_data,
            model=model,
        )

    thinking_block = f"<think>\n{reasoning_steps.full_thinking_monologue.strip()}\n</think>"
    sft_messages, dpo_pairs = _build_sft_and_dpo_records(trajectory_data, thinking_block)

    rfc_meta = trajectory_data.get("rfc_metadata", {})
    quality_tier = trajectory_data.get("quality_assessment", {}).get("quality_tier", "REJECTED")
    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    bundle = ThinkArtifactBundle(
        schema_version="1.0.0",
        run_id=trajectory_data.get("run_id", f"{stem}_{now_utc}"),
        timestamp_utc=now_utc,
        rfc_id=rfc_meta.get("rfc_id", "Unknown RFC"),
        rfc_title=rfc_meta.get("rfc_title", "Unknown Protocol"),
        protocol_name=rfc_meta.get("protocol_name", stem),
        algebra=rfc_meta.get("algebra", "basic"),
        quality_tier=quality_tier,
        synthesis_mode=synthesis_mode,
        source_trajectory_file=trajectory_json_path.name,
        target_scm_file=scm_filename,
        reasoning_steps=reasoning_steps,
        thinking_block=thinking_block,
        sft_messages=sft_messages,
        dpo_contrastive_pairs=dpo_pairs,
    )

    think_json_path.write_text(
        json.dumps(bundle.model_dump(), indent=2),
        encoding="utf-8",
    )
    logger.info(
        "Wrote <think> artifact (%s, mode=%s, dpo_pairs=%d) to %s",
        quality_tier,
        synthesis_mode,
        len(dpo_pairs),
        think_json_path,
    )

    effective_run_root = run_root_dir or rfc_dir.parent
    update_metadata_index_with_think_file(
        run_root_dir=effective_run_root,
        trajectory_json_path=trajectory_json_path,
        think_json_path=think_json_path,
    )
    return think_json_path


def process_run_directory(
    target_path: Path,
    model: Optional[str] = None,
    mode: str = "auto",
    min_tier: str = "BRONZE",
    export_jsonl: bool = True,
) -> List[Path]:
    """Processes a timestamped run directory (via `metadata_index.json`), an RFC directory,
    or a single `<protocol>_trajectory.json` file, generating `<protocol>_think.json` files
    and optional consolidated `sft_train.jsonl` / `dpo_pairs.jsonl` datasets.
    """
    target_path = target_path.resolve()
    min_rank = TIER_RANK.get(min_tier.upper(), 2)
    trajectory_files: List[Path] = []
    run_root_dir: Optional[Path] = None

    if target_path.is_file():
        if target_path.name == "metadata_index.json":
            run_root_dir = target_path.parent
            idx_data = json.loads(target_path.read_text(encoding="utf-8"))
            trajectory_files = [Path(p) for p in idx_data.get("metadata_json_files", []) if Path(p).exists()]
        elif target_path.name.endswith("_trajectory.json"):
            trajectory_files = [target_path]
            run_root_dir = target_path.parent.parent
        else:
            raise ValueError(f"Unsupported file target: {target_path}. Provide a *_trajectory.json or metadata_index.json.")
    elif target_path.is_dir():
        index_candidate = target_path / "metadata_index.json"
        if index_candidate.exists():
            run_root_dir = target_path
            idx_data = json.loads(index_candidate.read_text(encoding="utf-8"))
            trajectory_files = [Path(p) for p in idx_data.get("metadata_json_files", []) if Path(p).exists()]
        else:
            trajectory_files = sorted(target_path.rglob("*_trajectory.json"))
            run_root_dir = target_path
    else:
        raise FileNotFoundError(f"Target path does not exist: {target_path}")

    generated_think_files: List[Path] = []
    sft_records: List[Dict[str, Any]] = []
    dpo_records: List[Dict[str, Any]] = []

    for traj_path in trajectory_files:
        try:
            traj_data = json.loads(traj_path.read_text(encoding="utf-8"))
        except Exception as exc:
            logger.warning("Skipping unreadable trajectory file %s: %s", traj_path, exc)
            continue

        tier = traj_data.get("quality_assessment", {}).get("quality_tier", "REJECTED")
        if TIER_RANK.get(tier.upper(), 0) < min_rank:
            logger.info("Skipping %s (quality_tier=%s < min_tier=%s)", traj_path.name, tier, min_tier)
            continue

        think_path = generate_think_for_trajectory(
            trajectory_json_path=traj_path,
            model=model,
            mode=mode,
            run_root_dir=run_root_dir,
        )
        generated_think_files.append(think_path)

        think_data = json.loads(think_path.read_text(encoding="utf-8"))
        sft_records.append({
            "run_id": think_data["run_id"],
            "rfc_id": think_data["rfc_id"],
            "protocol_name": think_data["protocol_name"],
            "algebra": think_data["algebra"],
            "quality_tier": think_data["quality_tier"],
            "messages": think_data["sft_messages"],
        })
        for pair in think_data.get("dpo_contrastive_pairs", []):
            dpo_records.append({
                "run_id": think_data["run_id"],
                "rfc_id": think_data["rfc_id"],
                "protocol_name": think_data["protocol_name"],
                "quality_tier": think_data["quality_tier"],
                **pair,
            })

    if export_jsonl and run_root_dir and generated_think_files:
        sft_jsonl_path = run_root_dir / "sft_train.jsonl"
        with open(sft_jsonl_path, "w", encoding="utf-8") as sft_f:
            for rec in sft_records:
                sft_f.write(json.dumps(rec) + "\n")
        logger.info("Exported %d SFT records to %s", len(sft_records), sft_jsonl_path)

        if dpo_records:
            dpo_jsonl_path = run_root_dir / "dpo_pairs.jsonl"
            with open(dpo_jsonl_path, "w", encoding="utf-8") as dpo_f:
                for rec in dpo_records:
                    dpo_f.write(json.dumps(rec) + "\n")
            logger.info("Exported %d DPO contrastive pairs to %s", len(dpo_records), dpo_jsonl_path)

    return generated_think_files
