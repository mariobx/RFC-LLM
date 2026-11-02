"""Verbatim RFC Section Boundary Slicer."""

import re
from typing import List, Optional, Tuple

from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("section_slicer")

_ANY_SECTION_HEADING_RE = re.compile(
    r"^(?:(\d+(?:\.\d+)*)|Appendix\s+([A-Z](?:\.\d+)*))\.?\s+[A-Z]"
)


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


def _find_section_end(lines: List[str], section_id: str, start_line_idx: int) -> int:
    """Finds the line index where `section_id` (and any of its nested subsections) ends."""
    norm_id = re.sub(r"^Appendix\s+", "", section_id.strip(), flags=re.IGNORECASE).rstrip(".")
    sub_prefix = f"{norm_id}."

    for idx in range(start_line_idx + 1, len(lines)):
        match = _ANY_SECTION_HEADING_RE.match(lines[idx])
        if match:
            found_id = (match.group(1) or match.group(2) or "").rstrip(".")
            if found_id and found_id.lower() != norm_id.lower() and not found_id.lower().startswith(sub_prefix.lower()):
                return idx

    return min(start_line_idx + 600, len(lines))


def slice_verbatim_sections(
    raw_rfc_text: str,
    target_section_ids: List[str],
    clean_page_breaks: bool = True,
) -> str:
    """Extracts the verbatim text for the specified section IDs from an RFC document,
    slicing each requested section individually and merging overlapping/contiguous spans.
    """
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

    # Step 2: Resolve [start, end) line intervals for each requested section
    intervals: List[Tuple[int, int]] = []
    for sec_id in target_section_ids:
        start_idx = _find_section_start(lines, sec_id, search_from_line=toc_end_idx)
        if start_idx is None:
            start_idx = _find_section_start(lines, sec_id, search_from_line=0)
        if start_idx is None:
            if not intervals and sec_id == target_section_ids[0]:
                logger.error("Could not locate starting section '%s' in document", sec_id)
                raise ValueError(f"Section '{sec_id}' not found in document")
            logger.warning("Requested section '%s' not found in document; skipping", sec_id)
            continue
        end_idx = _find_section_end(lines, sec_id, start_idx)
        intervals.append((start_idx, end_idx))

    if not intervals:
        raise ValueError(f"None of the requested sections {target_section_ids} were found in document")

    # Step 3: Sort and merge overlapping or adjacent intervals
    intervals.sort(key=lambda pair: pair[0])
    merged: List[Tuple[int, int]] = [intervals[0]]
    for cur_start, cur_end in intervals[1:]:
        prev_start, prev_end = merged[-1]
        if cur_start <= prev_end:
            merged[-1] = (prev_start, max(prev_end, cur_end))
        else:
            merged.append((cur_start, cur_end))

    total_raw_lines = sum(end - start for start, end in merged)
    span_desc = ", ".join(f"{s + 1}..{e}" for s, e in merged)
    logger.info(
        "Slicing sections %s: spans [%s] (%d raw lines)",
        target_section_ids,
        span_desc,
        total_raw_lines,
    )

    sliced_lines: List[str] = []
    for idx, (s_idx, e_idx) in enumerate(merged):
        if idx > 0 and sliced_lines:
            sliced_lines.append("")
        sliced_lines.extend(lines[s_idx:e_idx])

    if clean_page_breaks:
        cleaned = [line for line in sliced_lines if not _is_rfc_page_break(line)]
        logger.debug("Cleaned %d page break lines from slice", len(sliced_lines) - len(cleaned))
        sliced_lines = cleaned

    return "\n".join(sliced_lines)
