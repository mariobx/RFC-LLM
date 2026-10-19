"""Protocol Applicability Gate (Tier 1 Gatekeeper).

Evaluates an RFC's frontmatter, abstract, and complete Table of Contents to
determine whether it specifies an interactive cryptographic security protocol
eligible for MITRE CPSA 4.4.9 formal verification.
"""

import json
from typing import List, Optional
import litellm
from pydantic import BaseModel, Field

from src.document_ingestion.rfc_toc_parser import TOCSectionEntry
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_APPLICABILITY_GATE,
    build_schema_system_prompt,
    load_prompt,
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


# Loaded from .prompts/01_applicability_gate.md
GATEKEEPER_SYSTEM_PROMPT: str = load_prompt(PROMPT_APPLICABILITY_GATE)


def evaluate_protocol_applicability(
    rfc_id: str,
    title: str,
    category: str,
    abstract: str,
    toc_entries: List[TOCSectionEntry],
    model: Optional[str] = None,
) -> ProtocolApplicabilityReport:
    """Evaluates an RFC using its frontmatter and entire TOC to determine CPSA eligibility."""
    model_name = model or SYSTEM_CONFIG.DEFAULT_ROUTER_MODEL
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
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(model_name, temperature=0.0)
        response = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
        )

        raw_content = response.choices[0].message.content
        try:
            report_data = json.loads(raw_content)
        except Exception:
            import json_repair
            report_data = json_repair.loads(raw_content)

        report = ProtocolApplicabilityReport.model_validate(report_data)

        if report.is_cryptographic_protocol:
            logger.info(
                "Tier 1 ACCEPT: %s is eligible (Protocol: '%s', Principals: %s)",
                rfc_id,
                report.protocol_name,
                report.participating_principals,
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
