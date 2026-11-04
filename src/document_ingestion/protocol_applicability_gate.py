"""Protocol Applicability Gate (Tier 1 Gatekeeper).

Evaluates an RFC's frontmatter, abstract, and complete Table of Contents to
determine whether it specifies an interactive cryptographic security protocol
eligible for MITRE CPSA 4.4.9 formal verification.
"""

import json
from typing import List, Optional
import json_repair
import litellm
from pydantic import BaseModel, Field

from src.document_ingestion.rfc_toc_parser import TOCSectionEntry
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    build_schema_system_prompt,
    load_prompt_spec,
    parse_llm_json,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("applicability_gate")


class ProtocolApplicabilityReport(BaseModel):
    """Assessment of whether an RFC specifies an interactive cryptographic protocol eligible for CPSA."""

    is_cryptographic_protocol: bool = Field(
        ...,
        description="True if the document specifies an interactive protocol with cryptographic terms (keys, nonces, auth)",
    )
    protocol_name: Optional[str] = Field(None, description="Standard protocol name extracted from title")
    participating_principals: List[str] = Field(
        default_factory=list,
        description="Identified roles or principals",
    )
    has_keys_or_nonces: bool = Field(
        ...,
        description="True if the protocol uses encryption keys, certificates, nonces, or digital signatures",
    )
    rationale: str = Field(..., description="Justification for acceptance or rejection")


def evaluate_protocol_applicability(
    rfc_id: str,
    title: str,
    category: str,
    abstract: str,
    toc_entries: List[TOCSectionEntry],
    model: Optional[str] = None,
) -> ProtocolApplicabilityReport:
    """Evaluates an RFC using its frontmatter and entire TOC to determine CPSA eligibility."""
    prompt_spec = load_prompt_spec(PROMPT_APPLICABILITY_GATE)
    model_name = model or prompt_spec.model
    sampling_temp = prompt_spec.temperature
    logger.info("Evaluating protocol applicability for %s: '%s' using model %s", rfc_id, title, model_name)

    toc_summary = "\n".join(f"{entry.section_id} {entry.title}" for entry in toc_entries)

    user_prompt = (
        f"RFC Identifier: {rfc_id}\n"
        f"Title: {title}\n"
        f"Category: {category}\n\n"
        f"Abstract:\n{abstract}\n\n"
        f"Complete Table of Contents:\n{toc_summary}\n\n"
        "Determine if this RFC is an eligible interactive cryptographic protocol for MITRE CPSA formal verification."
    )

    system_prompt = build_schema_system_prompt(
        PROMPT_APPLICABILITY_GATE,
        ProtocolApplicabilityReport,
    )

    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=sampling_temp,
            max_tokens=prompt_spec.max_tokens,
            json_mode=True,
        )
        response = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=prompt_spec.timeout,
        )
        from src.cost_tracker import GLOBAL_COST_TRACKER
        GLOBAL_COST_TRACKER.record_llm_call(response, role="router", model_name=model_name, stage=1)

        raw_content = response.choices[0].message.content
        report_data = parse_llm_json(raw_content)

        report = ProtocolApplicabilityReport.model_validate(report_data)

        if report.is_cryptographic_protocol and (
            not report.has_keys_or_nonces or len(report.participating_principals) < 2
        ):
            logger.info(
                "Tier 1 REJECT (Incomplete Crypto/Principals): %s had is_cryptographic_protocol=True "
                "but has_keys_or_nonces=%s, principals=%s",
                rfc_id,
                report.has_keys_or_nonces,
                report.participating_principals,
            )
            report.is_cryptographic_protocol = False

        if report.is_cryptographic_protocol:
            logger.info(
                "Tier 1 ACCEPT: %s is eligible (Protocol: '%s', Principals: %s). Reason: %s",
                rfc_id,
                report.protocol_name,
                report.participating_principals,
                report.rationale,
            )
        else:
            logger.info("Tier 1 REJECT: %s is ineligible. Reason: %s", rfc_id, report.rationale)

        return report

    except Exception as exc:
        logger.error("LLM gatekeeper evaluation failed: %s. Falling back to heuristic check.", str(exc))
        combined_text = f"{title} {abstract} {toc_summary}".lower()
        has_crypto = any(
            term in combined_text
            for term in ["cryptographic", "handshake", "cipher", "secret", "nonce", "authentication service"]
        )
        is_protocol = any(
            term in combined_text
            for term in ["protocol", "exchange", "message format", "handshake"]
        )

        return ProtocolApplicabilityReport(
            is_cryptographic_protocol=has_crypto and is_protocol,
            protocol_name=title,
            participating_principals=["initiator", "responder"] if has_crypto else [],
            has_keys_or_nonces=has_crypto,
            rationale=f"Heuristic determination: crypto_terms={has_crypto}, protocol_terms={is_protocol}",
        )
