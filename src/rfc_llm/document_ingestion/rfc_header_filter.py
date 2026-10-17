"""RFC Header and Frontmatter Metadata Filter (Tier 0 Filter)."""

import re
from typing import Optional
from pydantic import BaseModel, Field

from rfc_llm.logging_config import get_pipeline_logger

logger = get_pipeline_logger("header_filter")


class HeaderFilterResult(BaseModel):
    """Result of Tier 0 RFC frontmatter analysis."""
    is_eligible: bool = Field(..., description="Whether the RFC is potentially an eligible protocol")
    rfc_id: Optional[str] = Field(None, description="RFC identifier (e.g. 'RFC ####')")
    title: Optional[str] = Field(None, description="Extracted document title")
    category: Optional[str] = Field(None, description="Category (Standards Track, Informational, etc.)")
    disqualification_reason: Optional[str] = Field(None, description="Reason if disqualified")


DISQUALIFIED_TITLE_KEYWORDS = [
    "management information base",
    "managed objects",
    "definitions of managed objects",
    " mib",
    " mib-",
    "architecture",
    "applicability statement",
    "problem statement",
    "requirements for",
    "iana considerations",
    "registry",
    "guidelines for",
    "meeting",
    "minutes",
    "equipment purchase",
    "millennium problem",
]

DISQUALIFIED_CATEGORIES = [
    "historic",
    "best current practice",
]


def filter_rfc_header(raw_rfc_text: str) -> HeaderFilterResult:
    """Evaluates the top 100 lines of an RFC for eligibility before invoking any LLM."""
    lines = raw_rfc_text.splitlines()[:100]
    header_text = "\n".join(lines)

    logger.debug("Executing Tier 0 frontmatter filter on top %d lines", len(lines))

    # 1. Line count check (trivial errata / 1-page stubs)
    total_lines = len(raw_rfc_text.splitlines())
    if total_lines < 60:
        logger.info("Tier 0 REJECT: File has only %d lines (trivial stub)", total_lines)
        return HeaderFilterResult(
            is_eligible=False,
            disqualification_reason=f"Document is too short to be a protocol ({total_lines} lines)",
        )

    # 2. Extract RFC ID
    rfc_match = re.search(r"Request for Comments:\s*#?(\d+)", header_text, re.IGNORECASE)
    rfc_id = f"RFC {rfc_match.group(1)}" if rfc_match else None

    # 3. Extract Category (stop at multiple spaces before right-column date)
    category_match = re.search(r"Category:\s*([A-Za-z\s]+?)(?:\s{2,}|\n|$)", header_text, re.IGNORECASE)
    category = category_match.group(1).strip() if category_match else "Unknown"

    for dis_cat in DISQUALIFIED_CATEGORIES:
        if dis_cat.lower() in category.lower():
            logger.info("Tier 0 REJECT: Disqualified category '%s'", category)
            return HeaderFilterResult(
                is_eligible=False,
                rfc_id=rfc_id,
                category=category,
                disqualification_reason=f"Category '{category}' is not a protocol specification",
            )

    # 4. Extract Title: lines between author/category block and "Status of This Memo"
    title: Optional[str] = None
    status_idx = next(
        (i for i, l in enumerate(lines) if re.search(r"(Status of [Tt]his Memo|Abstract)", l, re.IGNORECASE)),
        len(lines),
    )

    # Search backwards from Status of This Memo for consecutive non-empty lines
    title_candidate_lines = []
    idx = status_idx - 1
    # Skip any trailing blank lines right before "Status of This Memo"
    while idx >= 0 and not lines[idx].strip():
        idx -= 1

    # Now collect all consecutive non-empty lines belonging to the title
    while idx >= 0 and lines[idx].strip():
        line_str = lines[idx].strip()
        # If we reached the header block (Category, Date, RFC, etc.), stop
        if re.search(r"(Category:|Updates:|Obsoletes:|Request for Comments|Network Working Group|ISSN:)", line_str, re.IGNORECASE):
            break
        title_candidate_lines.insert(0, line_str)
        idx -= 1

    if title_candidate_lines:
        title = " ".join(title_candidate_lines)

    # 5. Check Title Keywords
    if title:
        title_lower = title.lower()
        for kw in DISQUALIFIED_TITLE_KEYWORDS:
            if kw in title_lower:
                logger.info("Tier 0 REJECT: Title '%s' matches blacklist keyword '%s'", title, kw)
                return HeaderFilterResult(
                    is_eligible=False,
                    rfc_id=rfc_id,
                    title=title,
                    category=category,
                    disqualification_reason=f"Title keyword '{kw}' indicates non-protocol document",
                )

    logger.info("Tier 0 PASS: %s - '%s' (%s)", rfc_id or "Unknown RFC", title or "Unknown Title", category)
    return HeaderFilterResult(
        is_eligible=True,
        rfc_id=rfc_id,
        title=title,
        category=category,
    )
