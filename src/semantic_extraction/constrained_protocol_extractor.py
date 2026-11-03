"""Constrained Protocol Semantic Extractor with RAG Grounding.

Translates verbatim RFC message-exchange sections into a validated
`CPSAProtocolSpecification` AST using Hybrid BM25 + Dense RRF reference
grounding, 1-shot self-healing schema correction, and the mandatory
3-Point-of-View preskeleton architecture.
"""

import json
import time
from typing import List, Optional
import json_repair
import litellm
from pydantic import ValidationError

from src.intermediate_representation.protocol_syntax_tree import (
    CPSAPreskeleton,
    CPSAProtocolSpecification,
    CPSAStrandInstance,
    CPSAVariableDeclaration,
)
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_PROTOCOL_EXTRACTION,
    PROMPT_SCHEMA_SELF_CORRECTION,
    build_schema_system_prompt,
    load_prompt_spec,
    parse_llm_json,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("protocol_extractor")

LAST_EXTRACTION_METADATA: dict = {
    "schema_self_correction_triggered": False,
    "schema_validation_error": None,
}


def extract_protocol_specification(
    verbatim_slice: str,
    protocol_name: str,
    principals: Optional[List[str]] = None,
    model: Optional[str] = None,
) -> CPSAProtocolSpecification:
    """Extracts a validated CPSAProtocolSpecification from verbatim RFC text."""
    global LAST_EXTRACTION_METADATA
    LAST_EXTRACTION_METADATA = {
        "schema_self_correction_triggered": False,
        "schema_validation_error": None,
    }
    extraction_spec = load_prompt_spec(PROMPT_PROTOCOL_EXTRACTION)
    model_name = model or extraction_spec.model
    sampling_temp = extraction_spec.temperature if extraction_spec.temperature is not None else 0.0
    logger.info("Extracting CPSAProtocolSpecification for '%s' using %s", protocol_name, model_name)

    principals_hint = f"Expected Principals: {', '.join(principals)}" if principals else ""

    user_prompt = (
        f"Protocol Identifier: {protocol_name}\n"
        f"{principals_hint}\n\n"
        "Verbatim RFC Exchange Specification (SOLE GROUND TRUTH — STRICT 1-TO-1 FIDELITY REQUIRED):\n"
        f"{verbatim_slice}\n\n"
        "Extract the complete CPSAProtocolSpecification adhering to all MITRE CPSA 4.4.9 executability and sort constraints.\n"
        "CRITICAL ZERO-HALLUCINATION RULE: Model strictly the roles, message flights, fields, and cryptographic "
        "operations defined in the Verbatim RFC Exchange Specification above. Do NOT invent fictional messages, "
        "non-RFC variables, or textbook protocol fields that do not appear in the RFC text."
    )

    system_prompt = build_schema_system_prompt(
        PROMPT_PROTOCOL_EXTRACTION,
        CPSAProtocolSpecification,
    )

    llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
        model_name,
        temperature=sampling_temp,
        max_tokens=extraction_spec.max_tokens,
        json_mode=True,
    )
    response = None
    for retry_idx in range(3):
        try:
            response = litellm.completion(
                **llm_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                timeout=extraction_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(response, role="extraction", model_name=model_name, stage=2)
            break
        except Exception as exc:
            err_msg = str(exc)
            if (
                any(
                    token in err_msg
                    for token in (
                        "Timeout",
                        "timed out",
                        "429",
                        "RateLimit",
                        "BadGateway",
                        "502",
                        "503",
                        "504",
                        "incomplete",
                        "output budget",
                    )
                )
                and retry_idx < 2
            ):
                wait_seconds = 10 * (retry_idx + 1)
                logger.warning(
                    "Extraction attempt %d failed (%s). Retrying in %ds...",
                    retry_idx + 1,
                    exc,
                    wait_seconds,
                )
                time.sleep(wait_seconds)
            else:
                raise

    raw_content = response.choices[0].message.content
    parsed_data = parse_llm_json(raw_content)

    try:
        specification = CPSAProtocolSpecification.model_validate(parsed_data)
    except ValidationError as validation_error:
        LAST_EXTRACTION_METADATA["schema_self_correction_triggered"] = True
        LAST_EXTRACTION_METADATA["schema_validation_error"] = str(validation_error)
        logger.warning(
            "Stage 2 schema validation error encountered: %s. Initiating 1-shot self-healing correction...",
            validation_error,
        )
        corr_spec = load_prompt_spec(PROMPT_SCHEMA_SELF_CORRECTION)
        correction_template = corr_spec.body
        if "{validation_error}" in correction_template:
            correction_prompt = correction_template.replace("{validation_error}", str(validation_error))
        else:
            correction_prompt = f"{correction_template}\n\nValidation Errors:\n{validation_error}"

        corr_model = model or corr_spec.model
        corr_temp = corr_spec.temperature if corr_spec.temperature is not None else 0.0
        corr_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            corr_model,
            temperature=corr_temp,
            max_tokens=corr_spec.max_tokens,
            json_mode=True,
        )

        try:
            correction_response = litellm.completion(
                **corr_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": raw_content},
                    {"role": "user", "content": correction_prompt},
                ],
                timeout=corr_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(correction_response, role="extraction", model_name=corr_model, stage=2)
            corrected_content = correction_response.choices[0].message.content
            corrected_data = parse_llm_json(corrected_content)
            specification = CPSAProtocolSpecification.model_validate(corrected_data)
            logger.info("Stage 2 self-healing correction SUCCEEDED")
        except Exception as retry_error:
            logger.error("Self-healing correction failed: %s. Raising validation error.", retry_error)
            raise validation_error from retry_error

    specification = ensure_three_point_of_view_skeletons(specification)

    logger.info(
        "Extraction SUCCESS: Extracted protocol '%s' with %d roles and %d preskeletons",
        specification.protocol_name,
        len(specification.roles),
        len(specification.skeletons),
    )
    return specification


def ensure_three_point_of_view_skeletons(spec: CPSAProtocolSpecification) -> CPSAProtocolSpecification:
    """Guarantees the standard MITRE CPSA 3-skeleton architecture:
    1. Dedicated pure POV preskeleton for each communicating role with defstrandmax and NO listeners
       (enabling CPSA to compute minimal realized bilateral handshake shapes).
    2. A distinct secrecy preskeleton containing a deflistener for the primary confidential term.
    """
    if not spec.roles:
        return spec

    # Collect existing secrecy listeners and non-originating assumptions
    existing_listeners = []
    global_non_originating = []
    for skel in spec.skeletons:
        existing_listeners.extend(skel.listeners)
        global_non_originating.extend(skel.non_originating)

    # Deduplicate non-originating keys while preserving insertion order
    seen_non_orig_keys = set()
    deduplicated_non_orig = []
    for non_orig_term in global_non_originating:
        serialized_term = json.dumps(non_orig_term, sort_keys=True)
        if serialized_term not in seen_non_orig_keys:
            seen_non_orig_keys.add(serialized_term)
            deduplicated_non_orig.append(non_orig_term)

    # Separate pure POV skeletons (without listeners) and secrecy skeletons (with listeners)
    # CRITICAL: Filter out any invalid listener term that is also declared in non_originating
    # or pen_non_originating (which causes CPSA fatal error: `non-orig <key> carried`).
    non_orig_set = {json.dumps(t, sort_keys=True) for t in deduplicated_non_orig}
    for skel in spec.skeletons:
        for pno in skel.pen_non_originating:
            non_orig_set.add(json.dumps(pno, sort_keys=True))
    for role in spec.roles:
        for no_t in role.non_originating + role.pen_non_originating:
            non_orig_set.add(json.dumps(no_t, sort_keys=True))

    spec.primary_secrecy_goals = [
        t for t in spec.primary_secrecy_goals if json.dumps(t, sort_keys=True) not in non_orig_set
    ]

    roles_with_pure_pov = set()
    pure_pov_skeletons = []
    secrecy_skeletons = []

    for skel in spec.skeletons:
        valid_listeners = [
            l for l in skel.listeners if json.dumps(l, sort_keys=True) not in non_orig_set
        ]
        skel.listeners = valid_listeners
        if not skel.listeners:
            pure_pov_skeletons.append(skel)
            for strand in skel.strands:
                roles_with_pure_pov.add(strand.role_name)
        else:
            secrecy_skeletons.append(skel)

    # Build pure POV skeletons for any roles that lack them
    final_skeletons = list(pure_pov_skeletons)
    for role in spec.roles:
        if role.role_name not in roles_with_pure_pov:
            variable_bindings = {var.name: var.name for var in role.variables}
            skeleton_variables = [
                CPSAVariableDeclaration(name=var.name, sort=var.sort)
                for var in role.variables
            ]
            pure_role_skeleton = CPSAPreskeleton(
                protocol_name=spec.protocol_name,
                description=f"{role.role_name.capitalize()} Point of View (Authentication & Shape Realization)",
                variables=skeleton_variables,
                strands=[
                    CPSAStrandInstance(
                        role_name=role.role_name,
                        variable_bindings=variable_bindings,
                    )
                ],
                non_originating=deduplicated_non_orig,
                unique_originating=list(role.unique_originating),
                listeners=[],
                comment=f"{role.role_name.capitalize()} Point of View",
            )
            final_skeletons.append(pure_role_skeleton)

    # Guarantee at least one secrecy verification skeleton if a valid transmitted secret was identified
    if secrecy_skeletons:
        final_skeletons.extend(secrecy_skeletons)
    else:
        valid_existing_listeners = [
            l for l in existing_listeners if json.dumps(l, sort_keys=True) not in non_orig_set
        ]
        secret_targets = valid_existing_listeners or spec.primary_secrecy_goals
        if secret_targets:
            chosen_secret = secret_targets[0]
            originating_role = spec.roles[0]
            for role in spec.roles:
                if any(
                    chosen_secret == uo or (isinstance(uo, str) and uo == chosen_secret)
                    for uo in role.unique_originating
                ):
                    originating_role = role
                    break

            variable_bindings = {var.name: var.name for var in originating_role.variables}
            skeleton_variables = [
                CPSAVariableDeclaration(name=var.name, sort=var.sort)
                for var in originating_role.variables
            ]
            secrecy_skeleton = CPSAPreskeleton(
                protocol_name=spec.protocol_name,
                description=f"Secrecy Verification: tests confidentiality of {chosen_secret}",
                variables=skeleton_variables,
                strands=[
                    CPSAStrandInstance(
                        role_name=originating_role.role_name,
                        variable_bindings=variable_bindings,
                    )
                ],
                non_originating=deduplicated_non_orig,
                unique_originating=list(originating_role.unique_originating),
                listeners=[chosen_secret],
                comment=f"Secrecy Point of View: Listener on {chosen_secret}",
            )
            final_skeletons.append(secrecy_skeleton)

    spec.skeletons = final_skeletons
    return spec
