"""Verbatim RFC Section Boundary Slicer."""

import re
from typing import List, Optional, Tuple

from rfc_llm.logging_config import get_pipeline_logger

logger = get_pipeline_logger("section_slicer")


def _is_rfc_page_break(line: str) -> bool:
    """Detects RFC pagination artifacts (form feeds, header/footer lines)."""
    stripped = line.strip()
    if "\x0c" in line:
        return True
    if re.search(r"\[Page\s+\d+\]$", stripped, re.IGNORECASE):
        return True
    if re.search(r"^RFC\s+\d+", stripped, re.IGNORECASE):
        return True
    return False


def _find_section_start(lines: List[str], section_id: str, search_from_line: int = 0) -> Optional[int]:
    """Finds the line index where a section heading starts at column 0 in the body text."""
    # Pattern matching "^7.3.  Title" or "^7.3  Title" or "^Appendix A.  Title"
    escaped_id = re.escape(section_id)
    pattern = re.compile(rf"^(?:{escaped_id}|Appendix\s+{escaped_id})\.?\s+[A-Z]", re.IGNORECASE)

    for idx in range(search_from_line, len(lines)):
        line = lines[idx]
        if pattern.match(line):
            return idx
    return None


def slice_verbatim_sections(
    raw_rfc_text: str,
    target_section_ids: List[str],
    clean_page_breaks: bool = True,
) -> str:
    """Extracts the verbatim text for the specified section IDs from an RFC document."""
    if not target_section_ids:
        logger.warning("No target section IDs provided for slicing")
        return ""

    lines = raw_rfc_text.splitlines()

    # Step 1: Skip past the Table of Contents to avoid matching TOC entries as section starts
    toc_end_idx = 100
    for idx, line in enumerate(lines[:350]):
        if re.match(r"^1\.?\s+[A-Z]", line):
            toc_end_idx = idx
            break

    # Step 2: Locate start of the first requested section
    first_sec = target_section_ids[0]
    start_line_idx = _find_section_start(lines, first_sec, search_from_line=toc_end_idx)

    if start_line_idx is None:
        # Fallback to searching from line 0
        start_line_idx = _find_section_start(lines, first_sec, search_from_line=0)

    if start_line_idx is None:
        logger.error("Could not locate starting section '%s' in document", first_sec)
        raise ValueError(f"Section '{first_sec}' not found in document")

    # Step 3: Locate end boundary (the start of the section immediately following the target set)
    last_sec = target_section_ids[-1]
    # Derive next sibling or parent section boundary
    parts = last_sec.split(".")
    candidates_for_next: List[str] = []

    if len(parts) > 1:
        # e.g., for "7.4", next sibling is "7.5", parent next is "8"
        try:
            next_num = int(parts[-1]) + 1
            candidates_for_next.append(".".join(parts[:-1] + [str(next_num)]))
        except ValueError:
            pass
        try:
            parent_next = int(parts[0]) + 1
            candidates_for_next.append(str(parent_next))
        except ValueError:
            pass
    else:
        try:
            candidates_for_next.append(str(int(parts[0]) + 1))
        except ValueError:
            pass

    end_line_idx: Optional[int] = None
    for cand in candidates_for_next:
        idx = _find_section_start(lines, cand, search_from_line=start_line_idx + 1)
        if idx is not None:
            if end_line_idx is None or idx < end_line_idx:
                end_line_idx = idx

    if end_line_idx is None:
        # If no next section found, slice to end or 500 lines ahead
        end_line_idx = min(start_line_idx + 600, len(lines))

    logger.info(
        "Slicing sections %s: lines %d to %d (%d raw lines)",
        target_section_ids,
        start_line_idx + 1,
        end_line_idx,
        end_line_idx - start_line_idx,
    )

    sliced_lines = lines[start_line_idx:end_line_idx]

    if clean_page_breaks:
        cleaned = [line for line in sliced_lines if not _is_rfc_page_break(line)]
        logger.debug("Cleaned %d page break lines from slice", len(sliced_lines) - len(cleaned))
        sliced_lines = cleaned

    return "\n".join(sliced_lines)
