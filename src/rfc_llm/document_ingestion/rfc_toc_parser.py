"""RFC Table of Contents (TOC) Parser."""

import re
from typing import List, Optional
from pydantic import BaseModel, Field

from rfc_llm.logging_config import get_pipeline_logger

logger = get_pipeline_logger("toc_parser")


class TOCSectionEntry(BaseModel):
    """A single section entry parsed from an RFC Table of Contents."""
    section_id: str = Field(..., description="Dotted section number or identifier (e.g. '7.3', 'A.1')")
    title: str = Field(..., description="Section title")
    page_number: Optional[int] = Field(None, description="Page number if present in TOC")
    indent_level: int = Field(default=0, description="Nesting level derived from leading indentation")

    def __str__(self) -> str:
        page_str = f" (p. {self.page_number})" if self.page_number else ""
        return f"{self.section_id} {self.title}{page_str}"


TOC_HEADER_PATTERN = re.compile(r"^\s*(Table of Contents|CONTENTS)\s*$", re.IGNORECASE)

# Matches lines like:
# "   7.3. Handshake Protocol Overview ...............................33"
# "     5.1.  Updated Section "Location Attributes" . . . . . . . . . .   8"
# "   Appendix A.  Protocol Structures ..................................68"
# "   1.  Introduction"
TOC_LINE_PATTERN = re.compile(
    r"^(?P<indent>\s*)(?P<sec_id>(?:(?:[0-9]+(?:\.[0-9]+)*)|(?:Appendix\s+[A-Z](?:\.[0-9]+)*)|(?:[A-Z]\.[0-9]+)))\.?\s+"
    r"(?P<title>.+?)"
    r"(?:\s*(?:\.{2,}|(?:\.\s+){2,})\s*(?P<page>[0-9]+))?\s*$",
    re.IGNORECASE,
)


def parse_table_of_contents(raw_rfc_text: str) -> List[TOCSectionEntry]:
    """Extracts the complete Table of Contents hierarchy from an RFC text document."""
    lines = raw_rfc_text.splitlines()
    toc_start_idx: Optional[int] = None

    # Step 1: Find the TOC Header within the first 250 lines
    for idx, line in enumerate(lines[:250]):
        if TOC_HEADER_PATTERN.match(line):
            toc_start_idx = idx + 1
            break

    entries: List[TOCSectionEntry] = []

    if toc_start_idx is not None:
        logger.debug("Found TOC header at line %d", toc_start_idx)
        current_entry: Optional[TOCSectionEntry] = None

        # Scan forward until the first section begins at column 0 (e.g. "1.  Introduction")
        for line in lines[toc_start_idx:]:
            # If we hit the actual start of Section 1 at column 0, TOC has ended
            if re.match(r"^1\.?\s+[A-Z]", line):
                break
            # Or if we hit 400 lines without stopping
            if len(entries) > 150:
                break

            match = TOC_LINE_PATTERN.match(line)
            if match:
                sec_id = match.group("sec_id").strip()
                # Clean up "Appendix A" -> "App-A"
                sec_id = re.sub(r"Appendix\s+", "App-", sec_id, flags=re.IGNORECASE)
                title = match.group("title").strip()
                page = int(match.group("page")) if match.group("page") else None
                indent = len(match.group("indent"))

                current_entry = TOCSectionEntry(
                    section_id=sec_id,
                    title=title,
                    page_number=page,
                    indent_level=indent,
                )
                entries.append(current_entry)
            elif current_entry and line.strip():
                stripped_line = line.strip()
                # Skip form feeds, page headers, footers
                if (
                    "\x0c" in line
                    or re.search(r"\[Page\s+\d+\]", stripped_line, re.IGNORECASE)
                    or re.search(r"\b(Standards Track|Informational|Experimental)\b", stripped_line, re.IGNORECASE)
                    or re.search(r"^RFC\s+\d+", stripped_line, re.IGNORECASE)
                ):
                    continue

                # Strip trailing dots or page numbers if on second line
                dots_match = re.search(r"^(.*?)(?:\s*(?:\.{2,}|(?:\.\s+){2,})\s*([0-9]+))?$", stripped_line)
                if dots_match:
                    sub_title = dots_match.group(1).strip()
                    # Do not append if sub_title looks like a new unnumbered section or noise
                    if sub_title and not re.search(r"(Normative References|Informative References|Author's Address|Acknowledgments)", sub_title, re.IGNORECASE):
                        current_entry.title += f" {sub_title}"
                    if dots_match.group(2) and current_entry.page_number is None:
                        current_entry.page_number = int(dots_match.group(2))

    # Step 2: Fallback if no explicit TOC header exists: scan column-0 headings in body
    if not entries:
        logger.info("No explicit TOC block found. Scanning body headings for synthetic TOC...")
        body_heading_pattern = re.compile(
            r"^(?P<sec_id>(?:[0-9]+(?:\.[0-9]+)*)|(?:[A-Z]\.[0-9]+))\.?\s+(?P<title>[A-Z][A-Za-z0-9\s\-_,:()'\"]{3,60})$"
        )
        for idx, line in enumerate(lines):
            match = body_heading_pattern.match(line)
            if match:
                sec_id = match.group("sec_id").strip()
                title = match.group("title").strip()
                entries.append(TOCSectionEntry(section_id=sec_id, title=title, page_number=None, indent_level=0))

    logger.info("Parsed %d TOC section entries", len(entries))
    return entries
