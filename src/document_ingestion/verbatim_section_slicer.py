"""Verbatim RFC Section Boundary Slicer."""

import re
from typing import List, Optional, Tuple

from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("section_slicer")

_ANY_SECTION_HEADING_RE = re.compile(
    r"^(?:(\d+(?:\.\d+)+)\.?|(\d+)\.|(\d+)|Appendix\s+([A-Z](?:\.\d+)*)\.?|([A-Z](?:\.\d+)+)\.?)\s+"
    r"(?=[A-Za-z0-9\"'\(\[])"
)
_TOC_DOT_LEADER_RE = re.compile(r"(?:\.{3,}|(?:\.\s+){3,})\s*\d+\s*$")


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


def _clean_requested_sec_id(section_id: str) -> str:
    """Normalizes a section identifier for body heading lookup."""
    s = section_id.strip().strip("`'\"")
    s = re.sub(r"^[#§]+\s*", "", s)
    s = re.sub(r"^(?:Section|Sec\.?)\s+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"^(?:Appendix\s+|App-)", "", s, flags=re.IGNORECASE)
    return s.rstrip(".")


def _find_section_start(lines: List[str], section_id: str, search_from_line: int = 0) -> Optional[int]:
    """Finds the line index where a section heading starts at column 0 in the body text."""
    clean_id = _clean_requested_sec_id(section_id)
    if not clean_id:
        return None
    escaped_id = re.escape(clean_id)
    # Match "^7.3.  Title", "^6.7.2.  0x0002 - AUTHENTICATION_TYPE", or "^Appendix A.  Title"
    if "." in clean_id:
        pattern = re.compile(
            rf"^(?:{escaped_id}\.?|Appendix\s+{escaped_id}\.?)\s+[A-Za-z0-9\"'\(\[]",
            re.IGNORECASE,
        )
    else:
        pattern = re.compile(
            rf"^(?:{escaped_id}\.\s+[A-Za-z0-9\"'\(\[]|{escaped_id}\s+[A-Za-z]|Appendix\s+{escaped_id}\.?\s+[A-Za-z0-9\"'\(\[])",
            re.IGNORECASE,
        )

    for idx in range(search_from_line, len(lines)):
        line = lines[idx]
        if pattern.match(line) and not _TOC_DOT_LEADER_RE.search(line):
            return idx
    return None


def _find_section_end(lines: List[str], section_id: str, start_line_idx: int) -> int:
    """Finds the line index where `section_id` (and any of its nested subsections) ends."""
    norm_id = _clean_requested_sec_id(section_id)
    sub_prefix = f"{norm_id}."

    for idx in range(start_line_idx + 1, len(lines)):
        line = lines[idx]
        if _TOC_DOT_LEADER_RE.search(line):
            continue
        match = _ANY_SECTION_HEADING_RE.match(line)
        if match:
            # If matched group(3) (bare integer without dot), require uppercase letter start for title
            if match.group(3) and not re.match(r"^\d+\s+[A-Z]", line):
                continue
            found_id = (
                match.group(1)
                or match.group(2)
                or match.group(3)
                or match.group(4)
                or match.group(5)
                or ""
            ).rstrip(".")
            if found_id and found_id.lower() != norm_id.lower() and not found_id.lower().startswith(sub_prefix.lower()):
                return idx

    return min(start_line_idx + 600, len(lines))


def _slice_unnumbered_rfc_body(lines: List[str], clean_page_breaks: bool = True) -> str:
    """Fallback slicer for short RFCs with unnumbered section headings (e.g., RFC 3268)."""
    start_idx = 0
    for idx, line in enumerate(lines[:150]):
        if re.match(r"^(?:Overview|Introduction|1\.?\s+Introduction)\s*$", line.strip(), re.IGNORECASE):
            start_idx = idx
            break
        if re.match(r"^Abstract\s*$", line.strip(), re.IGNORECASE):
            start_idx = idx
    end_idx = len(lines)
    for idx in range(start_idx + 1, len(lines)):
        if re.match(
            r"^(?:References|Normative References|Informative References|"
            r"Author(?:'s|s')?\s+Address(?:es)?|Full Copyright Statement)\s*$",
            lines[idx].strip(),
            re.IGNORECASE,
        ):
            end_idx = idx
            break
    end_idx = min(end_idx, start_idx + 600)
    sliced = lines[start_idx:end_idx]
    if clean_page_breaks:
        sliced = [line for line in sliced if not _is_rfc_page_break(line)]
    return "\n".join(sliced).strip()


def slice_verbatim_sections(
    raw_rfc_text: str,
    target_section_ids: List[str],
    clean_page_breaks: bool = True,
) -> str:
    """Extracts the verbatim text for the specified section IDs from an RFC document,
    slicing each requested section individually and merging overlapping/contiguous spans.
    """
    lines = raw_rfc_text.splitlines()
    if not target_section_ids or target_section_ids == ["FULL_BODY"]:
        if len(lines) <= 1000 or target_section_ids == ["FULL_BODY"]:
            logger.info("Using unnumbered/full-body fallback slicer (%d document lines)", len(lines))
            return _slice_unnumbered_rfc_body(lines, clean_page_breaks=clean_page_breaks)
        logger.warning("No target section IDs provided for slicing")
        return ""

    # Step 1: Skip past the Table of Contents to avoid matching TOC entries as section starts
    toc_end_idx = 100
    for idx, line in enumerate(lines[:800]):
        if re.match(r"^1(?:\.0)?\.?\s+[A-Z]", line) and not _TOC_DOT_LEADER_RE.search(line):
            toc_end_idx = idx
            break

    # Step 2: Resolve [start, end) line intervals for each requested section
    intervals: List[Tuple[int, int]] = []
    seen_parent_preambles = set()
    for raw_sec_id in target_section_ids:
        sec_id = _clean_requested_sec_id(raw_sec_id) or raw_sec_id.strip()
        # If a first subsection (e.g. "3.1") is requested without its parent ("3"),
        # also include the parent section's introductory preamble ("3" -> "3.1")
        if sec_id.endswith(".1") and sec_id.count(".") == 1:
            parent_id = sec_id.split(".")[0]
            if parent_id not in target_section_ids and parent_id not in seen_parent_preambles:
                seen_parent_preambles.add(parent_id)
                p_start = _find_section_start(lines, parent_id, search_from_line=toc_end_idx)
                if p_start is not None:
                    first_sub = _find_section_start(lines, f"{parent_id}.1", search_from_line=p_start + 1)
                    if first_sub is not None and first_sub > p_start and (first_sub - p_start) <= 120:
                        intervals.append((p_start, first_sub))

        start_idx = _find_section_start(lines, sec_id, search_from_line=toc_end_idx)
        if start_idx is None:
            start_idx = _find_section_start(lines, sec_id, search_from_line=0)
        resolved_sec_id = sec_id
        # Parent-section fallback if a deeply nested subsection (e.g. "6.7.2") has a malformed body heading
        while start_idx is None and "." in resolved_sec_id:
            parent_candidate = resolved_sec_id.rsplit(".", 1)[0]
            logger.warning(
                "Section '%s' not found directly; attempting parent section fallback '%s'",
                resolved_sec_id,
                parent_candidate,
            )
            resolved_sec_id = parent_candidate
            start_idx = _find_section_start(lines, resolved_sec_id, search_from_line=toc_end_idx)
            if start_idx is None:
                start_idx = _find_section_start(lines, resolved_sec_id, search_from_line=0)

        if start_idx is None:
            if not intervals and raw_sec_id == target_section_ids[0] and len(target_section_ids) == 1:
                logger.error("Could not locate starting section '%s' in document", sec_id)
                raise ValueError(f"Section '{sec_id}' not found in document")
            logger.warning("Requested section '%s' not found in document; skipping", sec_id)
            continue
        end_idx = _find_section_end(lines, resolved_sec_id, start_idx)
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
