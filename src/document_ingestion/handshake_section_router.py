"""Handshake Section Router for Navigating RFC Table of Contents.

Selects the exact RFC section numbers from the Table of Contents that contain
the cryptographic message exchange or handshake flow.
"""

import json
from typing import List, Optional
import litellm
from pydantic import BaseModel, Field

from src.document_ingestion.rfc_toc_parser import TOCSectionEntry
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_SECTION_ROUTER,
    build_schema_system_prompt,
    load_prompt,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("section_router")


class SectionRoutingDecision(BaseModel):
    """Decision indicating which RFC sections contain the cryptographic message exchange."""

    selected_section_ids: List[str] = Field(
        ...,
        description="List of section IDs containing the protocol message traces (such as ['#.#', '#.#.#'])",
    )
    rationale: str = Field(..., description="Explanation of why these sections were selected")


# Loaded from .prompts/02_section_router.md
ROUTER_SYSTEM_PROMPT: str = load_prompt(PROMPT_SECTION_ROUTER)


def route_handshake_sections(
    rfc_id: str,
    protocol_name: str,
    toc_entries: List[TOCSectionEntry],
    model: Optional[str] = None,
) -> List[str]:
    """Uses a structured LLM call to select the exchange section IDs from the TOC."""
    model_name = model or SYSTEM_CONFIG.DEFAULT_ROUTER_MODEL
    logger.info("Routing exchange sections for %s ('%s') using %s", rfc_id, protocol_name, model_name)

    toc_formatted = "\n".join(f"{entry.section_id} {entry.title}" for entry in toc_entries)

    user_prompt = (
        f"Protocol Name: {protocol_name}\n"
        f"RFC: {rfc_id}\n\n"
        f"Table of Contents:\n{toc_formatted}\n\n"
        "Select the section IDs containing the primary cryptographic message exchange or handshake."
    )

    system_prompt = build_schema_system_prompt(
        PROMPT_SECTION_ROUTER,
        SectionRoutingDecision,
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
            decision_data = json.loads(raw_content)
        except Exception:
            import json_repair
            decision_data = json_repair.loads(raw_content)

        decision = SectionRoutingDecision.model_validate(decision_data)

        valid_toc_ids = {entry.section_id for entry in toc_entries}
        filtered_section_ids = [
            section_id for section_id in decision.selected_section_ids if section_id in valid_toc_ids
        ]

        if not filtered_section_ids:
            logger.warning(
                "Model suggested sections %s not in TOC. Falling back to heuristic.",
                decision.selected_section_ids,
            )
            return _heuristic_section_router(toc_entries)

        logger.info("Router selected sections %s: %s", filtered_section_ids, decision.rationale)
        return filtered_section_ids

    except Exception as exc:
        logger.error("LLM section router failed: %s. Using heuristic fallback.", str(exc))
        return _heuristic_section_router(toc_entries)


def _heuristic_section_router(toc_entries: List[TOCSectionEntry]) -> List[str]:
    """Deterministic keyword fallback for selecting exchange sections from TOC."""
    exchange_keywords = [
        "handshake protocol overview",
        "handshake protocol",
        "message exchange",
        "authentication service",
        "protocol description",
    ]

    # First pass: Look for high-priority exact phrase matches
    selected_sections: List[str] = []
    for entry in toc_entries:
        title_lower = entry.title.lower()
        if any(keyword in title_lower for keyword in exchange_keywords):
            selected_sections.append(entry.section_id)

    # Second pass: If nothing matched, look for "handshake", "exchange", or "operation"
    if not selected_sections:
        for entry in toc_entries:
            title_lower = entry.title.lower()
            if any(term in title_lower for term in ["handshake", "exchange", "protocol operation"]):
                selected_sections.append(entry.section_id)

    if not selected_sections and toc_entries:
        # Final fallback: Pick Section 2 or 3
        for entry in toc_entries:
            if entry.section_id in ["2", "3", "3.1"]:
                selected_sections.append(entry.section_id)

    logger.info("Heuristic router selected sections: %s", selected_sections)
    return selected_sections or (["1"] if toc_entries else [])
