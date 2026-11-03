"""Handshake Section Router for Navigating RFC Table of Contents.

Selects the exact RFC section numbers from the Table of Contents that contain
the cryptographic message exchange or handshake flow.
"""

import json
from typing import List, Optional
import json_repair
import litellm
from pydantic import BaseModel, Field

from src.document_ingestion.rfc_toc_parser import TOCSectionEntry
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_SECTION_ROUTER,
    build_schema_system_prompt,
    load_prompt_spec,
    parse_llm_json,
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


def route_handshake_sections(
    rfc_id: str,
    protocol_name: str,
    toc_entries: List[TOCSectionEntry],
    model: Optional[str] = None,
) -> List[str]:
    """Uses a structured LLM call to select the exchange section IDs from the TOC."""
    prompt_spec = load_prompt_spec(PROMPT_SECTION_ROUTER)
    model_name = model or prompt_spec.model
    sampling_temp = prompt_spec.temperature if prompt_spec.temperature is not None else 0.0
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
        decision_data = parse_llm_json(raw_content)

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
    excluded_titles = (
        "introduction",
        "terminology",
        "conventions",
        "requirements language",
        "notation",
        "definitions",
        "scope",
        "background",
        "iana considerations",
        "security considerations",
        "references",
        "normative references",
        "informative references",
        "acknowledgements",
        "acknowledgments",
    )

    exchange_keywords = [
        "handshake",
        "message exchange",
        "protocol exchange",
        "authentication",
        "key exchange",
        "key agreement",
        "protocol overview",
        "protocol description",
        "protocol operation",
        "overview of operation",
        "operation",
        "communication",
        "transactions",
        "packet types",
        "message format",
    ]

    selected_sections: List[str] = []
    for entry in toc_entries:
        title_lower = entry.title.lower().strip()
        if any(title_lower == ex or title_lower.startswith(ex + " ") for ex in excluded_titles):
            continue
        # Prefer top-level or second-level sections matching exchange/crypto keywords
        if entry.section_id.count(".") <= 1 and any(keyword in title_lower for keyword in exchange_keywords):
            selected_sections.append(entry.section_id)

    if not selected_sections:
        for entry in toc_entries:
            title_lower = entry.title.lower().strip()
            if any(title_lower == ex or title_lower.startswith(ex + " ") for ex in excluded_titles):
                continue
            if entry.section_id.count(".") == 0 and entry.section_id not in ("1",):
                selected_sections.append(entry.section_id)
                if len(selected_sections) >= 3:
                    break

    logger.info("Heuristic router selected sections: %s", selected_sections)
    return selected_sections or (["2"] if toc_entries else [])
