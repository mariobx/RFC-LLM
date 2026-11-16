"""Zero-Cost Deterministic Protocol Specification De-Bloater.

Strips mechanical formatting noise, running page headers/footers, non-protocol
back-matter, and broken PDF table whitespace at $0.00 cost BEFORE `--rfc-style`
or Stage 2 extraction sees the slice—never mutating field names, variable names,
normative security clauses, cryptographic formulas, or ASCII ladder diagrams.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Tuple

# Lines preserved untouched because whitespace encodes column/arrow alignment
_ASCII_DIAGRAM_LINE_RE = re.compile(
    r"(?:--->|<---|<-->|===>|<===|\+--\+|\+---|\|.*\|)"
)

# Mechanical pagination headers/footers across IETF RFCs and global SDOs
_PAGINATION_LINE_PATTERNS = [
    re.compile(r"^\s*\[Page\s+\d+\]\s*$", re.IGNORECASE),
    re.compile(r"^\s*Page\s+\d+(?:\s+of\s+\d+)?\s*$", re.IGNORECASE),
    re.compile(r"^\s*-\s*\d+\s*-\s*$"),
    re.compile(r"^\s*RFC\s+\d+\s+.*\b(?:19|20)\d{2}\s*$"),
    re.compile(r"^\s*Internet-Draft\s+.*(?:Expires|19\d{2}|20\d{2}).*$", re.IGNORECASE),
    re.compile(r"^\s*CCSDS\s+\d+\.\d+-[A-Z]-\d+(?:\s+Page\s+[\dA-Za-z-]+.*)?$", re.IGNORECASE),
    re.compile(r"^\s*Page\s+[A-Z0-9-]+\s+CCSDS\s+\d+\.\d+-[A-Z]-\d+.*$", re.IGNORECASE),
    re.compile(r"^\s*(?:3GPP\s+TS|ETSI\s+(?:TS|EN|GS)|ITU-T\s+Rec\.?|DMTF\s+DSP\d+)\s+[^\n]{0,90}\s*$"),
    re.compile(r"^\s*(?:3GPP|ETSI)\s+\d+(?:\.\d+)*\s+Release\s+\d+.*$", re.IGNORECASE),
    re.compile(r"^\s*Copyright\s*(?:\(c\)|©)?\s*(?:19|20)\d{2}.*(?:All rights reserved|IETF Trust|ETSI|CCSDS|3GPP|DMTF|Microsoft|NIST|EMVCo|FIDO).*$", re.IGNORECASE),
    re.compile(r"^\s*(?:CONFIDENTIAL|PROPRIETARY|FOR INFORMATION ONLY)\s*$", re.IGNORECASE),
    re.compile(r"^\s*[A-Za-z0-9._-]+\s+(?:Standards Track|Informational|Experimental|Best Current Practice)\s+\[Page\s+\d+\]\s*$", re.IGNORECASE),
]

# Non-protocol administrative tail headings that add zero cryptographic protocol semantics
_ADMIN_SECTION_START_RE = re.compile(
    r"^\s*(?:(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)*)\.?[\s\-]+)?(?:"
    r"Change\s+History|Revision\s+History|Document\s+History|"
    r"Acknowledg(?:e)?ments|Bibliography|Informative\s+References|"
    r"Author(?:'s|s')?\s+Address(?:es)?|Editor(?:'s|s')?\s+Address(?:es)?|"
    r"Intellectual\s+Property(?:\s+Rights)?|Patent\s+Statement|"
    r"Full\s+Copyright\s+Statement|Disclaimer\s+of\s+Validity|"
    r"Contributors?"
    r")\s*:?\s*$",
    re.IGNORECASE,
)

# Next structural numbered heading that terminates a skipped admin subsection
_NUMBERED_HEADING_RE = re.compile(
    r"^\s*(?:(?:\d+(?:\.\d+)*)|(?:Appendix\s+[A-Z](?:\.\d+)*)|(?:Annex\s+[A-Z](?:\.\d+)*))(?:\.|\s+-)?\s+[A-Z]"
)

# Pure decorative horizontal divider or empty table grid row
_EMPTY_TABLE_OR_RULE_RE = re.compile(
    r"^\s*(?:\|(?:[\s\-\+\=_\|]*\|)+\s*|[-=_~*]{12,})\s*$"
)
_TOC_DOT_LEADER_LINE_RE = re.compile(
    r"^(?!.*(?:--->|<---|===)).*\s(?:\.{4,}|(?:\.\s+){4,})\s*\d+\s*$"
)
_EXCESS_SPACES_RE = re.compile(r"(?<=\S)[ \t]{6,}(?=\S)")


def _is_pagination_noise(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    for pat in _PAGINATION_LINE_PATTERNS:
        if pat.match(line):
            return True
    if _EMPTY_TABLE_OR_RULE_RE.match(line):
        return True
    if _TOC_DOT_LEADER_LINE_RE.match(line):
        return True
    return False


def debloat_protocol_slice(raw_slice: str, is_non_rfc: bool = False) -> Tuple[str, Dict[str, Any]]:
    """Deterministically de-bloats a verbatim protocol slice at $0.00 cost.

    Preserves 100% of normative specification sentences, field/variable names,
    cryptographic formulas, and ASCII ladder diagrams while stripping pagination
    headers/footers, form-feed artifacts, broken PDF whitespace, dot leaders,
    and purely administrative trailing sections.
    """
    if not raw_slice:
        return "", {
            "raw_chars": 0,
            "debloated_chars": 0,
            "saved_chars": 0,
            "saved_pct": 0.0,
            "raw_lines": 0,
            "debloated_lines": 0,
        }

    raw_chars = len(raw_slice)
    normalized_text = raw_slice.replace("\r\n", "\n").replace("\r", "\n").replace("\x0c", "\n")
    raw_lines = normalized_text.splitlines()

    filtered_lines = []
    skipping_admin_block = False
    blank_streak = 0

    for idx, line in enumerate(raw_lines):
        stripped = line.strip()

        if skipping_admin_block:
            if _NUMBERED_HEADING_RE.match(line) and not _ADMIN_SECTION_START_RE.match(line):
                skipping_admin_block = False
            else:
                continue

        if _ADMIN_SECTION_START_RE.match(line):
            skipping_admin_block = True
            continue

        if _is_pagination_noise(line):
            continue

        # Strip standalone indented PDF page numbers isolated by blank lines (e.g. "    4")
        if re.match(r"^\s{2,}\d{1,4}\s*$", line):
            prev_blank = idx == 0 or not raw_lines[idx - 1].strip()
            next_blank = idx + 1 == len(raw_lines) or not raw_lines[idx + 1].strip()
            if is_non_rfc or (prev_blank and next_blank):
                continue

        if not stripped:
            blank_streak += 1
            if blank_streak <= 1:
                filtered_lines.append("")
            continue

        blank_streak = 0

        # Preserve indentation and spacing on ASCII message ladders and box diagrams
        if _ASCII_DIAGRAM_LINE_RE.search(line):
            filtered_lines.append(line.rstrip())
            continue

        # Compress wide intra-line PDF column gaps without altering prose tokens
        compacted = _EXCESS_SPACES_RE.sub("  ", line.rstrip())
        if is_non_rfc and compacted.startswith("          "):
            # Trim excessive uniform PDF left margins while keeping shallow structural indent
            compacted = "    " + compacted.lstrip()
        filtered_lines.append(compacted)

    cleaned_text = "\n".join(filtered_lines).strip()
    if cleaned_text:
        cleaned_text += "\n"

    debloated_chars = len(cleaned_text)
    saved_chars = max(0, raw_chars - debloated_chars)
    saved_pct = round((saved_chars / raw_chars) * 100.0, 2) if raw_chars > 0 else 0.0

    stats: Dict[str, Any] = {
        "raw_chars": raw_chars,
        "debloated_chars": debloated_chars,
        "saved_chars": saved_chars,
        "saved_pct": saved_pct,
        "raw_lines": len(raw_lines),
        "debloated_lines": len(cleaned_text.splitlines()),
    }
    return cleaned_text, stats
