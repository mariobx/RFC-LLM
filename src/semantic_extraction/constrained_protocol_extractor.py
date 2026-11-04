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
    sampling_temp = extraction_spec.temperature
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

    response = None
    for retry_idx in range(3):
        effective_temp = (
            max(0.5, sampling_temp or 0.0)
            if retry_idx > 0
            else sampling_temp
        )
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=effective_temp,
            max_tokens=extraction_spec.max_tokens,
            json_mode=True,
        )
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
        corr_temp = corr_spec.temperature
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

    # Stage 2 Cryptographic Primitive Gate: if the LLM extracted roles with zero CPSA cryptographic
    # primitives (e.g., cleartext messages or bare variables), give it 1 self-correction pass to either
    # bail out with `is_verifiable_protocol=False` or model the RFC's actual cryptographic operations.
    if (
        specification.is_verifiable_protocol
        and specification.roles
        and not specification.has_cryptographic_primitives()
    ):
        crypto_error = (
            "Extracted specification contains zero CPSA cryptographic operators (`enc`, `hash`, `ltk`, `pubk`, "
            "`privk`, `invk`, `akey`, `skey`, `exp`, `gen`) across all role traces and assumptions. "
            "Either (a) the Verbatim RFC Exchange Specification defines a cleartext, transport-delegated, or "
            "non-cryptographic exchange — in which case you MUST set `\"is_verifiable_protocol\": false`, "
            "populate `\"ineligibility_reason\"`, and set `\"roles\": []` and `\"skeletons\": []`; OR "
            "(b) you omitted the RFC's cryptographic operations — in which case you MUST model the RFC's "
            "encryption, MAC/PRF (`hash`), signature (`enc` with `privk`), or Diffie-Hellman (`exp`/`gen`) "
            "operations explicitly in the role traces."
        )
        LAST_EXTRACTION_METADATA["schema_self_correction_triggered"] = True
        LAST_EXTRACTION_METADATA["schema_validation_error"] = crypto_error
        logger.warning(
            "Stage 2 extracted protocol '%s' has zero cryptographic primitives. Triggering 1-shot verification gate...",
            protocol_name,
        )
        corr_spec = load_prompt_spec(PROMPT_SCHEMA_SELF_CORRECTION)
        corr_model = model or corr_spec.model
        corr_temp = corr_spec.temperature
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
                    {"role": "assistant", "content": specification.model_dump_json()},
                    {"role": "user", "content": crypto_error},
                ],
                timeout=corr_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(correction_response, role="extraction", model_name=corr_model, stage=2)
            corrected_content = correction_response.choices[0].message.content
            corrected_data = parse_llm_json(corrected_content)
            specification = CPSAProtocolSpecification.model_validate(corrected_data)
        except Exception as exc:
            logger.warning("Cryptographic primitive self-correction call failed (%s); marking unverifiable.", exc)

        if specification.is_verifiable_protocol and not specification.has_cryptographic_primitives():
            specification.is_verifiable_protocol = False
            specification.ineligibility_reason = (
                specification.ineligibility_reason
                or "Extracted specification contains zero cryptographic primitives (cleartext or transport-delegated protocol)."
            )

    if not specification.is_verifiable_protocol or not specification.roles:
        logger.info(
            "Stage 2 determined '%s' is not a verifiable cryptographic protocol: %s",
            protocol_name,
            specification.ineligibility_reason,
        )
        return specification

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
    1. Dedicated pure POV preskeleton for each communicating role with a single defstrandmax and NO listeners
       (enabling CPSA to compute minimal realized bilateral handshake shapes without pre-seeded strands).
    2. A distinct secrecy preskeleton containing a deflistener for the primary confidential term.
    """
    if not spec.is_verifiable_protocol or not spec.roles:
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
            if len(skel.strands) == 1:
                role_name = skel.strands[0].role_name
                if role_name not in roles_with_pure_pov:
                    roles_with_pure_pov.add(role_name)
                    pure_pov_skeletons.append(skel)
        else:
            if len(skel.strands) > 1:
                skel.strands = [skel.strands[0]]
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

    # Ensure every skeleton's strands explicitly bind role variables to skeleton variables
    # (preventing `Skeleton not well formed: a variable in non-orig is not in some trace`),
    # strip redundant skeleton-level `uniq-orig` atoms already declared in the strand's `defrole`
    # (preventing `Skeleton not well formed: uniq-orig <var> not carried` when encrypted under a non-orig key),
    # and add sort-disjointness `(neq secret other_var)` facts in secrecy skeletons so CPSA cannot
    # alias a secret `data` variable with a cleartext `data` header/identifier in the same strand.
    role_map = {r.role_name: r for r in spec.roles}
    secret_atom_set = {
        s for s in spec.primary_secrecy_goals if isinstance(s, str)
    }
    for skel in spec.skeletons:
        existing_var_names = {v.name for v in skel.variables}
        role_level_uniq_orig = set()
        for strand in skel.strands:
            matched_role = role_map.get(strand.role_name)
            if not matched_role:
                continue
            for r_var in matched_role.variables:
                if r_var.name not in existing_var_names:
                    skel.variables.append(CPSAVariableDeclaration(name=r_var.name, sort=r_var.sort))
                    existing_var_names.add(r_var.name)
                if r_var.name not in strand.variable_bindings:
                    strand.variable_bindings[r_var.name] = r_var.name
            for uo in matched_role.unique_originating:
                if isinstance(uo, str):
                    role_level_uniq_orig.add(uo)
        if role_level_uniq_orig and skel.unique_originating:
            skel.unique_originating = [
                uo for uo in skel.unique_originating
                if not (isinstance(uo, str) and uo in role_level_uniq_orig)
            ]
        if skel.listeners:
            var_sort_map = {v.name: v.sort for v in skel.variables}
            existing_facts = {
                (f[1], f[2])
                for f in skel.facts
                if isinstance(f, list) and len(f) == 3 and f[0] == "neq"
            } | {
                (f[2], f[1])
                for f in skel.facts
                if isinstance(f, list) and len(f) == 3 and f[0] == "neq"
            }
            listener_atoms = [l for l in skel.listeners if isinstance(l, str)]
            for secret_var in listener_atoms:
                secret_sort = var_sort_map.get(secret_var)
                if not secret_sort:
                    continue
                for v in skel.variables:
                    if (
                        v.name != secret_var
                        and v.sort == secret_sort
                        and v.name not in secret_atom_set
                        and v.name not in listener_atoms
                        and (secret_var, v.name) not in existing_facts
                    ):
                        skel.facts.append(["neq", secret_var, v.name])
                        existing_facts.add((secret_var, v.name))

    return spec
