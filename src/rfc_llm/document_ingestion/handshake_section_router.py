"""Handshake Section Router for Navigating RFC Table of Contents."""

import json
import re
from typing import List, Optional
from pydantic import BaseModel, Field
import litellm

from rfc_llm.document_ingestion.rfc_toc_parser import TOCSectionEntry
from rfc_llm.system_config import SYSTEM_CONFIG
from rfc_llm.logging_config import get_pipeline_logger

logger = get_pipeline_logger("section_router")


class SectionRoutingDecision(BaseModel):
    """Decision indicating which RFC sections contain the cryptographic message exchange."""
    selected_section_ids: List[str] = Field(
        ...,
        description="List of section IDs containing the protocol message traces (such as ['#.#', '#.#.#'])",
    )
    rationale: str = Field(..., description="Explanation of why these sections were selected")


ROUTER_SYSTEM_PROMPT = """You are a protocol analyst reading an RFC's Table of Contents.
Your task is to identify the EXACT section numbers that define the cryptographic message exchange or handshake between principals.

Guidelines:
- Choose sections that contain the message sequence, trace flow (such as directional transmissions or sequence ladders), and message payload structures.
- Do NOT select high-level requirements, introductory terminology, security considerations, or IANA registries.
- Typically 1 to 3 consecutive or related sections contain the complete exchange.
- Return ONLY a valid JSON object matching the requested schema."""


def route_handshake_sections(
    rfc_id: str,
    protocol_name: str,
    toc_entries: List[TOCSectionEntry],
    model: Optional[str] = None,
) -> List[str]:
    """Uses a fast structured model call to select the exchange section IDs from the TOC."""
    model_name = model or SYSTEM_CONFIG.DEFAULT_ROUTER_MODEL
    logger.info("Routing exchange sections for %s ('%s') using %s", rfc_id, protocol_name, model_name)

    toc_formatted = "\n".join(f"{e.section_id} {e.title}" for e in toc_entries)

    user_prompt = f"""Protocol Name: {protocol_name}
RFC: {rfc_id}

Table of Contents:
{toc_formatted}

Select the section IDs containing the primary cryptographic message exchange or handshake."""

    schema_str = json.dumps(SectionRoutingDecision.model_json_schema(), indent=2)
    system_prompt = f"{ROUTER_SYSTEM_PROMPT}\n\nRespond strictly with a valid JSON object matching this schema:\n{schema_str}"

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

        content = response.choices[0].message.content
        try:
            decision_data = json.loads(content)
        except Exception:
            import json_repair
            decision_data = json_repair.loads(content)

        decision = SectionRoutingDecision.model_validate(decision_data)

        # Validate that the selected IDs actually exist in the TOC
        valid_toc_ids = {e.section_id for e in toc_entries}
        filtered_ids = [sid for sid in decision.selected_section_ids if sid in valid_toc_ids]

        if not filtered_ids:
            logger.warning("Model suggested sections %s not in TOC. Falling back to heuristic.", decision.selected_section_ids)
            return _heuristic_section_router(toc_entries)

        logger.info("Router selected sections %s: %s", filtered_ids, decision.rationale)
        return filtered_ids

    except Exception as e:
        logger.error("LLM section router failed: %s. Using heuristic fallback.", str(e))
        return _heuristic_section_router(toc_entries)


def _heuristic_section_router(toc_entries: List[TOCSectionEntry]) -> List[str]:
    """Deterministic keyword fallback for selecting exchange sections from TOC."""
    exchange_keywords = ["handshake protocol overview", "handshake protocol", "message exchange", "authentication service", "protocol description"]

    # First pass: Look for high-priority exact phrase matches
    selected = []
    for entry in toc_entries:
        title_lower = entry.title.lower()
        if any(kw in title_lower for kw in exchange_keywords):
            selected.append(entry.section_id)

    # Second pass: If nothing matched, look for "handshake", "exchange", or "operation"
    if not selected:
        for entry in toc_entries:
            title_lower = entry.title.lower()
            if any(term in title_lower for term in ["handshake", "exchange", "protocol operation"]):
                selected.append(entry.section_id)

    if not selected and toc_entries:
        # Final fallback: Pick Section 2 or 3
        for entry in toc_entries:
            if entry.section_id in ["2", "3", "3.1"]:
                selected.append(entry.section_id)

    logger.info("Heuristic router selected sections: %s", selected)
    return selected or (["1"] if toc_entries else [])
