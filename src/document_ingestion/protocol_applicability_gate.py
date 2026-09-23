"""Protocol Applicability Gate (Tier 1 Gatekeeper)."""

import json
from typing import List, Optional
from pydantic import BaseModel, Field
import litellm

from src.document_ingestion.rfc_toc_parser import TOCSectionEntry
from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

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


GATEKEEPER_SYSTEM_PROMPT = """You are a formal methods expert in cryptographic protocol verification using MITRE CPSA.
Your task is to analyze an IETF RFC's metadata and Table of Contents to determine if it specifies an interactive cryptographic security protocol.

ELIGIBLE for CPSA:
- Interactive protocols between two or more principals.
- Employs cryptographic primitives: keys (symmetric or asymmetric), nonces, digital signatures, hashes, or Diffie-Hellman exponent groups.
- Focuses on authentication, secrecy, key establishment, or secure channel setup.

INELIGIBLE for CPSA:
- Network transport or routing protocols with no cryptographic mechanisms.
- Static data formats, ASN.1 management information bases, XML schemas, or database definitions.
- Administrative memos, requirements catalogs, problem statements, or surveys without message flows.

Return ONLY a valid JSON object matching the requested schema."""


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

    # Format the entire TOC into a compact text block
    toc_summary = "\n".join(f"{e.section_id} {e.title}" for e in toc_entries)

    user_prompt = f"""RFC Identifier: {rfc_id}
Title: {title}
Category: {category}

Abstract:
{abstract}

Complete Table of Contents:
{toc_summary}

Determine if this RFC is an eligible interactive cryptographic protocol for MITRE CPSA formal verification."""

    schema_str = json.dumps(ProtocolApplicabilityReport.model_json_schema(), indent=2)
    system_prompt = f"{GATEKEEPER_SYSTEM_PROMPT}\n\nRespond strictly with a valid JSON object matching this schema:\n{schema_str}"

    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(model_name)
        response = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
            timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
        )

        content = response.choices[0].message.content
        try:
            report_data = json.loads(content)
        except Exception:
            import json_repair
            report_data = json_repair.loads(content)

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

    except Exception as e:
        logger.error("LLM gatekeeper evaluation failed: %s. Falling back to heuristic check.", str(e))
        # Deterministic heuristic fallback
        combined_text = (title + " " + abstract + " " + toc_summary).lower()
        has_crypto = any(term in combined_text for term in ["cryptographic", "handshake", "cipher", "secret", "nonce", "authentication service"])
        is_proto = any(term in combined_text for term in ["protocol", "exchange", "message format", "handshake"])

        return ProtocolApplicabilityReport(
            is_cryptographic_protocol=has_crypto and is_proto,
            protocol_name=title,
            participating_principals=["initiator", "responder"] if has_crypto else [],
            has_keys_or_nonces=has_crypto,
            rationale=f"Heuristic determination: crypto_terms={has_crypto}, protocol_terms={is_proto}",
        )
