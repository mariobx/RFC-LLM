# RFC-LLM Core Source Code, Compilers, IR & CLI Entrypoints

> Tier 2 — Complete core synthesis pipeline (`src/`), including RFC document ingestion, order-sorted message algebra intermediate representation (IR), DSPy/RAG constrained protocol extraction, CPSA 4.4.9 JSON/Scheme code generation, roletran & compiler self-healing verification engine, live web visualizer, and the root `rfc-llm` CLI entrypoint.

*Generated: 2026-10-14 16:18:38 UTC · Git: `main` @ `f572f106cef2` · Tier: Tier 2 — Core Source Code & CLI Entrypoints · Files: 24*

## Table of Contents

- [`rfc-llm`](#rfc-llm)
- [`src/__init__.py`](#src-init-py)
- [`src/code_generation/cpsa_json_serializer.py`](#srccode-generationcpsa-json-serializerpy)
- [`src/code_generation/cpsa_scheme_emitter.py`](#srccode-generationcpsa-scheme-emitterpy)
- [`src/document_ingestion/handshake_section_router.py`](#srcdocument-ingestionhandshake-section-routerpy)
- [`src/document_ingestion/protocol_applicability_gate.py`](#srcdocument-ingestionprotocol-applicability-gatepy)
- [`src/document_ingestion/rfc_header_filter.py`](#srcdocument-ingestionrfc-header-filterpy)
- [`src/document_ingestion/rfc_toc_parser.py`](#srcdocument-ingestionrfc-toc-parserpy)
- [`src/document_ingestion/verbatim_section_slicer.py`](#srcdocument-ingestionverbatim-section-slicerpy)
- [`src/intermediate_representation/algebraic_sorts.py`](#srcintermediate-representationalgebraic-sortspy)
- [`src/intermediate_representation/cpsa_grammar.py`](#srcintermediate-representationcpsa-grammarpy)
- [`src/intermediate_representation/protocol_syntax_tree.py`](#srcintermediate-representationprotocol-syntax-treepy)
- [`src/logging_config.py`](#srclogging-configpy)
- [`src/main_pipeline_orchestrator.py`](#srcmain-pipeline-orchestratorpy)
- [`src/pipeline.py`](#srcpipelinepy)
- [`src/pipeline_events.py`](#srcpipeline-eventspy)
- [`src/semantic_extraction/constrained_protocol_extractor.py`](#srcsemantic-extractionconstrained-protocol-extractorpy)
- [`src/system_config.py`](#srcsystem-configpy)
- [`src/verification_engine/compiler_diagnostic_repair.py`](#srcverification-enginecompiler-diagnostic-repairpy)
- [`src/verification_engine/mitre_build_orchestrator.py`](#srcverification-enginemitre-build-orchestratorpy)
- [`src/verification_engine/roletran_executability_gate.py`](#srcverification-engineroletran-executability-gatepy)
- [`src/visualizer/__init__.py`](#srcvisualizer-init-py)
- [`src/visualizer/server.py`](#srcvisualizerserverpy)
- [`src/visualizer/static/index.html`](#srcvisualizerstaticindexhtml)

---

### `rfc-llm`

*sha256:`a642cacf2f98` · 15 lines · 0.5 KB · lang:`bash`*

```bash
#!/usr/bin/env bash
# RFC-LLM Command-line Runner
# Automatically configures PYTHONPATH and invokes the project virtual environment.

set -e

REPO_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH}"

if [ ! -f "${REPO_ROOT}/.venv/bin/python" ]; then
    echo "Error: Virtual environment not found at ${REPO_ROOT}/.venv" >&2
    exit 1
fi

exec "${REPO_ROOT}/.venv/bin/python" "${REPO_ROOT}/src/pipeline.py" "$@"
```

---

### `src/__init__.py`

*sha256:`5304a7d0e9d5` · 3 lines · 0.1 KB · lang:`python`*

```python
"""RFC-LLM: End-to-End Synthesis of Formally Verified MITRE CPSA Scheme Models from IETF RFCs."""

__version__ = "0.1.0"
```

---

### `src/code_generation/cpsa_json_serializer.py`

*sha256:`160a2e59151d` · 35 lines · 1.5 KB · lang:`python`*

```python
"""CPSA JSON AST Serializer."""

import json
from pathlib import Path
from typing import Any, List, Union

from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("json_serializer")


def serialize_to_cpsa_json(spec: CPSAProtocolSpecification) -> List[List[Any]]:
    """Serializes a CPSAProtocolSpecification into a list of top-level CPSA JSON forms."""
    logger.debug("Serializing CPSAProtocolSpecification for '%s' to native JSON forms", spec.protocol_name)
    payload = spec.to_cpsa_json_payload()
    logger.debug("Serialized %d top-level S-expression forms", len(payload))
    return payload


def serialize_to_cpsa_json_string(spec: CPSAProtocolSpecification) -> str:
    """Serializes the protocol specification into a newline-delimited JSON string for cpsa4json."""
    forms = serialize_to_cpsa_json(spec)
    # Each top-level form is written on its own line / separated by double newlines
    return "\n\n".join(json.dumps(form) for form in forms) + "\n"


def write_cpsa_json_file(spec: CPSAProtocolSpecification, target_path: Path) -> Path:
    """Writes the serialized JSON specification to disk."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    json_content = serialize_to_cpsa_json_string(spec)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(json_content)
    logger.info("Wrote CPSA JSON specification to %s", target_path)
    return target_path
```

---

### `src/code_generation/cpsa_scheme_emitter.py`

*sha256:`83c8ec48f762` · 63 lines · 2.5 KB · lang:`python`*

```python
"""CPSA Scheme S-Expression Emitter using cpsa4json."""

import subprocess
from pathlib import Path
from typing import Optional

from src.code_generation.cpsa_json_serializer import serialize_to_cpsa_json_string
from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("scheme_emitter")


class CPSAJsonCompilationError(Exception):
    """Raised when cpsa4json fails to compile a JSON tree into Scheme S-expressions."""
    pass


def emit_cpsa_scheme(
    spec: CPSAProtocolSpecification,
    output_directory: Path,
    filename_prefix: Optional[str] = None,
) -> Path:
    """Compiles a CPSAProtocolSpecification into a verified MITRE Scheme (.scm) file via cpsa4json."""
    output_directory.mkdir(parents=True, exist_ok=True)
    stem = filename_prefix or spec.protocol_name.replace(" ", "_").lower()
    target_scm_path = output_directory / f"{stem}.scm"

    logger.info("Emitting CPSA Scheme S-expressions for '%s' to %s", spec.protocol_name, target_scm_path)

    json_input_str = serialize_to_cpsa_json_string(spec)

    if not SYSTEM_CONFIG.CPSA4JSON_BIN.exists():
        logger.error("cpsa4json binary not found at %s", SYSTEM_CONFIG.CPSA4JSON_BIN)
        raise FileNotFoundError(f"cpsa4json binary missing at {SYSTEM_CONFIG.CPSA4JSON_BIN}")

    try:
        proc = subprocess.run(
            [str(SYSTEM_CONFIG.CPSA4JSON_BIN)],
            input=json_input_str,
            capture_output=True,
            text=True,
            timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
            check=False,
        )

        if proc.returncode != 0 or "Bad char in atom" in proc.stdout or "Error" in proc.stderr:
            err_msg = proc.stderr.strip() or proc.stdout.strip() or f"Exited with code {proc.returncode}"
            logger.error("cpsa4json compilation failed: %s", err_msg)
            raise CPSAJsonCompilationError(f"cpsa4json compilation error: {err_msg}")

        scm_content = proc.stdout

        with open(target_scm_path, "w", encoding="utf-8") as f:
            f.write(scm_content)

        logger.info("Successfully emitted %d lines of Scheme code to %s", len(scm_content.splitlines()), target_scm_path)
        return target_scm_path

    except subprocess.TimeoutExpired as e:
        logger.error("cpsa4json subprocess timed out after %d seconds", SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS)
        raise CPSAJsonCompilationError(f"cpsa4json compilation timed out: {e}") from e
```

---

### `src/document_ingestion/handshake_section_router.py`

*sha256:`b6c5b4826e9d` · 120 lines · 5.0 KB · lang:`python`*

```python
"""Handshake Section Router for Navigating RFC Table of Contents."""

import json
import re
from typing import List, Optional
from pydantic import BaseModel, Field
import litellm

from src.document_ingestion.rfc_toc_parser import TOCSectionEntry
from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

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
```

---

### `src/document_ingestion/protocol_applicability_gate.py`

*sha256:`e9de96901377` · 133 lines · 5.4 KB · lang:`python`*

```python
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

CRITICAL: Return a populated JSON instance, NOT the schema definition.
Example output format:
{
  "is_cryptographic_protocol": true,
  "protocol_name": "Protocol Name",
  "participating_principals": ["Alice", "Bob"],
  "has_keys_or_nonces": true,
  "rationale": "Clear concise justification"
}"""


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
```

---

### `src/document_ingestion/rfc_header_filter.py`

*sha256:`5d03adfe9e43` · 126 lines · 4.6 KB · lang:`python`*

```python
"""RFC Header and Frontmatter Metadata Filter (Tier 0 Filter)."""

import re
from typing import Optional
from pydantic import BaseModel, Field

from src.logging_config import get_pipeline_logger

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
```

---

### `src/document_ingestion/rfc_toc_parser.py`

*sha256:`dead8f2df65f` · 116 lines · 5.2 KB · lang:`python`*

```python
"""RFC Table of Contents (TOC) Parser."""

import re
from typing import List, Optional
from pydantic import BaseModel, Field

from src.logging_config import get_pipeline_logger

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
```

---

### `src/document_ingestion/verbatim_section_slicer.py`

*sha256:`4fda265d4a4d` · 117 lines · 4.0 KB · lang:`python`*

```python
"""Verbatim RFC Section Boundary Slicer."""

import re
from typing import List, Optional, Tuple

from src.logging_config import get_pipeline_logger

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
```

---

### `src/intermediate_representation/algebraic_sorts.py`

*sha256:`b07a02fb462f` · 28 lines · 1.1 KB · lang:`python`*

```python
"""Order-Sorted Message Algebra Sort Definitions for MITRE CPSA 4.4.9."""

from enum import Enum


class CPSASortEnum(str, Enum):
    """Supported sorts in MITRE CPSA order-sorted algebras (Tables 10.2, 10.4, 10.6)."""

    # Basic Atomic Sorts
    NAME = "name"      # Principal identifiers
    TEXT = "text"      # Fresh nonces and text tokens
    DATA = "data"      # Arbitrary payload / secrets
    TAG = "tag"        # Constant tag atoms
    SKEY = "skey"      # Symmetric encryption keys
    AKEY = "akey"      # Asymmetric keys (public or private)
    DEV = "dev"        # Hardware device identifiers
    CHAN = "chan"      # Communication channels (required by cpsa4roletran)
    LOCN = "locn"      # State memory locations (doors / envelopes)
    MESG = "mesg"      # Top sort (any valid message)

    # Diffie-Hellman Algebra Sorts
    RNDX = "rndx"      # Random exponents (must be uniquely originating)
    EXPT = "expt"      # Exponent expressions

    # Logic & Rule Sorts
    FACT = "fact"      # User-defined facts
    STRD = "strd"      # Strand index in rules/goals
    INDX = "indx"      # Node height index in rules/goals
```

---

### `src/intermediate_representation/cpsa_grammar.py`

*sha256:`fcb3115fcfe3` · 323 lines · 11.3 KB · lang:`python`*

```python
"""MITRE CPSA 4.4.9 Formal Grammar, Keywords, and Arity Specifications.

Derived directly from the authoritative MITRE CPSA Manual Chapters 2, 3, 4, 10 (Tables 10.1 - 10.6).
Provides static typing (Literals and Enums) and compile-time validation for all stages
of CPSA Scheme S-expression and JSON generation.
"""

from typing import Any, Dict, List, Literal, Optional, Set, Tuple, Union, get_args


# =============================================================================
# STAGE 1: Top-Level Scheme S-Expression Forms (Table 10.1)
# =============================================================================
CPSATopLevelKeyword = Literal[
    "herald",
    "defprotocol",
    "defskeleton",
    "defmacro",
    "defrule",
    "defgenrule",
    "defgoal",
    "deflemma",
    "comment",
]
CPSA_TOP_LEVEL_KEYWORDS: Set[str] = set(get_args(CPSATopLevelKeyword))


# =============================================================================
# STAGE 2: Cryptographic Message Algebras (Tables 10.2 & 10.4)
# =============================================================================
CPSAMessageAlgebra = Literal[
    "basic",
    "diffie-hellman",
]
CPSA_ALGEBRAS: Set[str] = set(get_args(CPSAMessageAlgebra))


# =============================================================================
# STAGE 3: Role Declaration Keywords (defrole) (Table 10.1 & Table 10.6)
# =============================================================================
CPSARoleKeyword = Literal[
    "defrole",
    "vars",
    "trace",
    "inputs",
    "outputs",
    "params",
    "returns",
    "non-orig",
    "pen-non-orig",
    "uniq-orig",
    "uniq-gen",
    "role_orig",
    "role-orig",
    "conf",
    "auth",
    "gen-st",
    "priority",
    "facts",
    "assume",
    "comment",
]
CPSA_ROLE_KEYWORDS: Set[str] = set(get_args(CPSARoleKeyword))


# =============================================================================
# STAGE 4: Preskeleton Declaration Keywords (defskeleton) (Table 10.1 & Table 10.6)
# =============================================================================
CPSASkeletonKeyword = Literal[
    "defskeleton",
    "vars",
    "defstrand",
    "defstrandmax",
    "deflistener",
    "non-orig",
    "pen-non-orig",
    "uniq-orig",
    "uniq-gen",
    "precedes",
    "leadsto",
    "priority",
    "facts",
    "goal",
    "comment",
]
CPSA_SKELETON_KEYWORDS: Set[str] = set(get_args(CPSASkeletonKeyword))


# =============================================================================
# STAGE 5: Trace Event Actions & Channels (Section 10.2, Table 10.1)
# =============================================================================
CPSATraceAction = Literal[
    "send",
    "recv",
    "load",
    "stor",
]
CPSA_TRACE_ACTIONS: Set[str] = set(get_args(CPSATraceAction))

CPSATraceAnnotation = Literal[
    "cheq",
    "rely",
    "guarantee",
]
CPSA_TRACE_ANNOTATIONS: Set[str] = set(get_args(CPSATraceAnnotation))


# =============================================================================
# STAGE 6: Message Term Operators (Tables 10.3 & 10.5)
# =============================================================================

# Basic Crypto Algebra Operators (Table 10.3)
CPSABasicOperator = Literal[
    "enc",     # {| m0 ... mn |}k  (arity >= 2)
    "hash",    # #m0 ... mn        (arity >= 1)
    "cat",     # (m0, ..., mn)     (arity >= 1)
    "pubk",    # K(a) or K(a, s)   (arity 1 or 2)
    "privk",   # K(a)^-1           (arity 1 or 2)
    "invk",    # k^-1              (arity 1)
    "ltk",     # ltk(a, b)         (arity 2)
]
CPSA_BASIC_OPERATORS: Set[str] = set(get_args(CPSABasicOperator))

# Diffie-Hellman Crypto Algebra Operators (Table 10.5)
CPSADHOperator = Literal[
    "bltk",    # bltk(a, b) = bltk(b, a) (arity 2)
    "exp",     # h^x                     (arity 2)
    "gen",     # g                       (arity 0)
    "mul",     # x * y                   (arity >= 2)
    "rec",     # x^-1                    (arity 1)
    "one",     # 1                       (arity 0)
]
CPSA_DH_OPERATORS: Set[str] = set(get_args(CPSADHOperator))

# All Authorized Term Operators
CPSAAllOperator = Literal[
    "enc",
    "hash",
    "cat",
    "pubk",
    "privk",
    "invk",
    "ltk",
    "bltk",
    "exp",
    "gen",
    "mul",
    "rec",
    "one",
]
CPSA_ALL_OPERATORS: Set[str] = set(get_args(CPSAAllOperator))


# =============================================================================
# STAGE 7: Operator Arity Constraints (Tables 10.3 & 10.5)
# =============================================================================
# Format: int (exact), set (one of allowed integers), tuple (min, max or None)
CPSA_OPERATOR_ARITY: Dict[str, Union[int, Set[int], Tuple[int, Optional[int]]]] = {
    "enc": (2, None),       # at least 1 payload + 1 key
    "hash": (1, None),      # at least 1 payload
    "cat": (1, None),       # at least 1 term
    "pubk": {1, 2},         # (pubk name) or (pubk name tag)
    "privk": {1, 2},        # (privk name) or (privk name tag)
    "invk": 1,              # (invk akey_var)
    "ltk": 2,               # (ltk name1 name2)
    "bltk": 2,              # (bltk name1 name2)
    "exp": 2,               # (exp base expt)
    "gen": 0,               # (gen)
    "mul": (2, None),       # at least 2 exponent factors
    "rec": 1,               # (rec expt)
    "one": 0,               # (one)
}


# =============================================================================
# STAGE 8: JSON Schema Specification for Strongly-Typed Term AST
# =============================================================================
CPSA_TERM_JSON_SCHEMA: Dict[str, Any] = {
    "title": "CPSATerm",
    "description": (
        "A CPSA 4.4.9 message term: an identifier atom string (e.g. client_random, K_ab), "
        "an integer constant, or a prefix S-expression list [operator, ...args] where operator "
        "is strictly one of: enc, hash, cat, pubk, privk, invk, ltk, bltk, exp, gen, mul, rec, one."
    ),
    "anyOf": [
        {"type": "string", "description": "Identifier atom, variable, or string literal"},
        {"type": "integer", "description": "Integer constant"},
        {
            "type": "array",
            "description": "Prefix operator expression: [operator, ...subterms]",
            "items": {
                "anyOf": [
                    {
                        "type": "string",
                        "enum": sorted(list(CPSA_ALL_OPERATORS)),
                        "description": "Leading CPSA 4.4.9 operator keyword",
                    },
                    {"type": "string", "description": "Subterm variable or constant"},
                    {"type": "integer"},
                    {"type": "array", "description": "Nested subterm expression"},
                ]
            },
            "minItems": 1,
        },
    ],
}


# =============================================================================
# STAGE 9: Canonical Desugaring Mappings (Frontend Compiler Normalizer)
# =============================================================================
# Maps foreign cryptographic operators (from ProVerif, Tamarin, or LLM hallucinations)
# to their canonical MITRE CPSA 4.4.9 equivalents.
CPSA_DESUGAR_MAP: Dict[str, str] = {
    "aenc": "enc",
    "senc": "enc",
    "asym_enc": "enc",
    "sym_enc": "enc",
    "sign": "enc",
    "mac": "hash",
    "hmac": "hash",
}


def desugar_term_tree(term: Any) -> Any:
    """Recursively desugars foreign/hallucinated crypto operators and dictionary nodes to canonical CPSA primitives."""
    if isinstance(term, list):
        if not term:
            return term
        new_list = list(term)
        op = new_list[0]
        if isinstance(op, str) and op in CPSA_DESUGAR_MAP:
            new_list[0] = CPSA_DESUGAR_MAP[op]
        return [desugar_term_tree(x) for x in new_list]
    if isinstance(term, dict):
        # Extract atomic identifier name from dictionary variable representation
        for key in ("name", "variable", "identifier", "var", "id", "atom", "field", "val", "value"):
            if key in term and isinstance(term[key], str):
                return term[key]
        if "term" in term:
            return desugar_term_tree(term["term"])
        if "args" in term and isinstance(term.get("op"), str):
            return desugar_term_tree([term["op"]] + term["args"])
        for v in term.values():
            if isinstance(v, str):
                return v
    return term


def validate_cpsa_term_syntax(
    term: Any,
    algebra: CPSAMessageAlgebra = "basic",
    path: str = "term",
) -> None:
    """Statically validates that a term tree conforms strictly to MITRE CPSA 4.4.9 grammar.

    Enforces:
    1. Operator existence in the authorized CPSA signature.
    2. Message algebra compatibility (forbidding DH operators under 'basic' algebra).
    3. Strict operator arity matching Tables 10.3 & 10.5.
    4. Inductive validation of all subterms.

    Raises:
        ValueError: If an unrecognized keyword, algebra incompatibility, or arity defect is found.
    """
    if isinstance(term, (str, int)):
        return

    if isinstance(term, list):
        if not term:
            raise ValueError(f"Empty term expression at '{path}'. Expected atom or operator form.")

        op = term[0]
        if not isinstance(op, str):
            raise ValueError(f"First element of expression at '{path}' must be an operator string, got {type(op).__name__}.")

        # 1. Operator Keyword Authorization
        if op not in CPSA_ALL_OPERATORS:
            raise ValueError(
                f"Unknown operator keyword '{op}' at '{path}'. "
                f"Valid CPSA 4.4.9 operators: {sorted(list(CPSA_ALL_OPERATORS))}"
            )

        # 2. Algebra Compatibility Check
        if algebra == "basic" and op in CPSA_DH_OPERATORS:
            raise ValueError(
                f"Diffie-Hellman operator '{op}' at '{path}' is forbidden under 'basic' message algebra. "
                "Change protocol message_algebra to 'diffie-hellman' to use exponentiation/DH features."
            )

        # 3. Arity Validation
        args = term[1:]
        arity = len(args)
        expected = CPSA_OPERATOR_ARITY.get(op)

        if isinstance(expected, int):
            if arity != expected:
                raise ValueError(
                    f"Operator '{op}' at '{path}' expects exactly {expected} arguments, got {arity}: {term}"
                )
        elif isinstance(expected, set):
            if arity not in expected:
                raise ValueError(
                    f"Operator '{op}' at '{path}' expects arity in {sorted(list(expected))}, got {arity}: {term}"
                )
        elif isinstance(expected, tuple):
            min_args, max_args = expected
            if arity < min_args:
                raise ValueError(
                    f"Operator '{op}' at '{path}' expects at least {min_args} arguments, got {arity}: {term}"
                )
            if max_args is not None and arity > max_args:
                raise ValueError(
                    f"Operator '{op}' at '{path}' expects at most {max_args} arguments, got {arity}: {term}"
                )

        # 4. Inductive Recursive Subterm Validation
        for idx, subterm in enumerate(args, 1):
            validate_cpsa_term_syntax(subterm, algebra=algebra, path=f"{path}[{idx}]")
    else:
        raise ValueError(
            f"Invalid term node at '{path}'. Expected string atom, integer, or nested operator list, got {type(term).__name__}."
        )
```

---

### `src/intermediate_representation/protocol_syntax_tree.py`

*sha256:`0feeb7e97cfd` · 447 lines · 18.4 KB · lang:`python`*

```python
import re
from typing import Annotated, Any, Dict, List, Literal, Optional, Set, Union
from pydantic import (
    BaseModel,
    BeforeValidator,
    AfterValidator,
    Field,
    WithJsonSchema,
    field_validator,
    model_validator,
)

from src.intermediate_representation.algebraic_sorts import CPSASortEnum
from src.intermediate_representation.cpsa_grammar import (
    CPSA_ALL_OPERATORS,
    CPSA_TERM_JSON_SCHEMA,
    CPSATopLevelKeyword,
    CPSAMessageAlgebra,
    CPSARoleKeyword,
    CPSASkeletonKeyword,
    CPSATraceAction,
    CPSATraceAnnotation,
    desugar_term_tree,
    validate_cpsa_term_syntax,
)


def _validate_cpsa_term(v: Any) -> Any:
    validate_cpsa_term_syntax(v, algebra="diffie-hellman")
    return v


# Strongly-typed CPSA term AST: enforces canonical syntax, algebra compatibility,
# and operator arity while providing an explicit enum/grammar JSON schema to LLMs.
CPSATerm = Annotated[
    Union[str, int, List[Any]],
    BeforeValidator(desugar_term_tree),
    AfterValidator(_validate_cpsa_term),
    WithJsonSchema(CPSA_TERM_JSON_SCHEMA),
]


def sanitize_cpsa_symbol(sym: str) -> str:
    """Sanitizes an identifier to conform strictly to CPSA S-expression symbol grammar.
    CPSA allows: alphanumeric and +-*/<=>!?$:%_&~^.
    Periods (.), spaces, and other punctuation are strictly forbidden in unquoted atoms.
    """
    if not sym:
        return "prot"
    s = re.sub(r'[\.\s]+', '-', sym)
    s = re.sub(r'[^a-zA-Z0-9+\-*/<=>!?$:%_&~^]', '', s)
    return s.strip('-') or "prot"


def normalize_cpsa_term(term: Any, akey_vars: Optional[Set[str]] = None) -> Any:
    """Recursively validates and normalizes message terms into valid CPSA 4.4.9 operators."""
    desugared = desugar_term_tree(term)
    if isinstance(desugared, list):
        if not desugared:
            return desugared
        new_list = list(desugared)
        if akey_vars and len(new_list) == 2 and isinstance(new_list[1], str) and new_list[1] in akey_vars:
            if new_list[0] == "pubk":
                return new_list[1]
            if new_list[0] == "privk":
                return ["invk", new_list[1]]
        return [normalize_cpsa_term(x, akey_vars) for x in new_list]
    return desugared


class CPSAVariableDeclaration(BaseModel):
    """Declaration of a typed variable in a role or skeleton."""
    name: str = Field(..., description="Semantic alphanumeric identifier (e.g. client_random, server_identity)")
    sort: CPSASortEnum = Field(..., description="Declared CPSA message algebra sort")
    description: Optional[str] = Field(default=None, description="Detailed explanation of what this variable represents in the RFC")
    rfc_field: Optional[str] = Field(default=None, description="Exact RFC field name or section mapping (e.g. ClientHello.random)")

    def to_cpsa_json(self) -> List[str]:
        return [self.name, self.sort.value]


class CPSATraceEvent(BaseModel):
    """A directional communication or state event over an optional channel."""
    direction: CPSATraceAction = Field(..., description="Trace event action: send, recv, load, stor")
    channel: Optional[str] = Field(default="ch", description="Channel variable identifier")
    location: Optional[str] = Field(default=None, description="Memory location variable for stateful load/stor events")
    message_term: CPSATerm = Field(
        ...,
        description="Term payload: atom string, integer, or nested operator tree conforming strictly to CPSA 4.4.9 grammar",
    )
    description: Optional[str] = Field(default=None, description="Semantic description of the message event (e.g. Client sends ClientHello)")

    def to_cpsa_json(self) -> List[Any]:
        if self.direction in ["load", "stor"]:
            event = [self.direction]
            if self.channel:
                event.append(self.channel)
            if self.location:
                event.append(self.location)
            event.append(self.message_term)
            return event

        if self.channel:
            return [self.direction, self.channel, self.message_term]
        return [self.direction, self.message_term]


class CPSAProtocolRole(BaseModel):
    """Specification of a principal's behavior in a protocol."""
    role_name: str = Field(..., description="Identifier for the participant role")
    description: Optional[str] = Field(default=None, description="Detailed explanation of the principal's role in the protocol")
    variables: List[CPSAVariableDeclaration] = Field(..., description="Variables declared within the role scope")
    trace: List[CPSATraceEvent] = Field(..., description="Ordered sequence of message events")
    inputs: List[CPSATerm] = Field(
        default_factory=list,
        description="Input parameters required for execution (channels, pre-shared keys, initial parameters)",
    )
    outputs: List[CPSATerm] = Field(
        default_factory=list,
        description="Return parameters yielded upon successful execution",
    )
    unique_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Terms originating uniquely in this role (uniq-orig)",
    )
    unique_generated: List[CPSATerm] = Field(
        default_factory=list,
        description="Terms generated uniquely in this role (uniq-gen)",
    )
    non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Keys assumed never compromised/originating in this role (non-orig)",
    )
    pen_non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Penetrator non-originating terms (pen-non-orig)",
    )
    role_originating: List[str] = Field(
        default_factory=list,
        description="Role-based unique origination assumptions (role_orig)",
    )
    confidential_channels: List[str] = Field(
        default_factory=list,
        description="Channels declared confidential (conf)",
    )
    authenticated_channels: List[str] = Field(
        default_factory=list,
        description="Channels declared authenticated (auth)",
    )
    facts: List[List[Any]] = Field(
        default_factory=list,
        description="User-defined logical facts asserted by this role",
    )
    comment: Optional[str] = None

    def to_cpsa_json(self) -> List[Any]:
        # Group variables by sort: ["vars", ["v1", "v2", "sort1"], ["v3", "sort2"]]
        sort_to_vars: Dict[str, List[str]] = {}
        for v in self.variables:
            sort_to_vars.setdefault(v.sort.value, []).append(v.name)

        vars_form = ["vars"]
        for sort_val, var_names in sort_to_vars.items():
            vars_form.append(var_names + [sort_val])

        akey_vars = {v.name for v in self.variables if v.sort.value == "akey"}

        normalized_events = []
        for event in self.trace:
            evt_json = event.to_cpsa_json()
            if len(evt_json) >= 2:
                evt_json[-1] = normalize_cpsa_term(evt_json[-1], akey_vars)
            normalized_events.append(evt_json)

        trace_form = ["trace"] + normalized_events

        def _extract_tokens(item: Any, out: Set[str]):
            if isinstance(item, str):
                out.add(item)
            elif isinstance(item, (list, tuple)):
                for x in item:
                    _extract_tokens(x, out)
            elif isinstance(item, dict):
                for x in item.values():
                    _extract_tokens(x, out)

        trace_tokens: Set[str] = set()
        _extract_tokens(trace_form, trace_tokens)
        reserved_ops = {"pubk", "privk", "invk", "ltk", "cat", "enc", "hash", "trace", "send", "recv"}.union(CPSA_ALL_OPERATORS)

        def _term_vars_in_trace(term: Any) -> bool:
            if isinstance(term, str):
                return term in trace_tokens
            if isinstance(term, (list, tuple)):
                term_tokens: Set[str] = set()
                _extract_tokens(term, term_tokens)
                var_tokens = term_tokens - reserved_ops
                return bool(var_tokens and var_tokens.issubset(trace_tokens))
            return True

        role_form: List[Any] = ["defrole", sanitize_cpsa_symbol(self.role_name), vars_form, trace_form]

        rndx_vars = {v.name for v in self.variables if v.sort.value in ("rndx", "expt")}
        effective_uo = []
        auto_ug = list(self.unique_generated)
        for term in self.unique_originating:
            if isinstance(term, str) and term in rndx_vars:
                if term not in auto_ug:
                    auto_ug.append(term)
            else:
                effective_uo.append(term)

        if effective_uo:
            valid_uo = [v for v in effective_uo if _term_vars_in_trace(v)]
            if valid_uo:
                role_form.append(["uniq-orig"] + valid_uo)
        if auto_ug:
            valid_ug = [v for v in auto_ug if _term_vars_in_trace(v)]
            if valid_ug:
                role_form.append(["uniq-gen"] + valid_ug)
        if self.non_originating:
            role_form.append(["non-orig"] + self.non_originating)
        if self.pen_non_originating:
            role_form.append(["pen-non-orig"] + self.pen_non_originating)
        if self.role_originating:
            role_form.append(["role_orig"] + self.role_originating)
        if self.confidential_channels:
            role_form.append(["conf"] + self.confidential_channels)
        if self.authenticated_channels:
            role_form.append(["auth"] + self.authenticated_channels)
        if self.facts:
            role_form.append(["facts"] + self.facts)

        # Procedural roletran annotations: every input/output term must be tied to trace variables
        if self.inputs:
            valid_inputs = []
            for inp in self.inputs:
                inp_tokens: Set[str] = set()
                _extract_tokens(inp, inp_tokens)
                var_tokens = inp_tokens - reserved_ops
                if var_tokens and var_tokens.issubset(trace_tokens):
                    valid_inputs.append(normalize_cpsa_term(inp, akey_vars))
            if valid_inputs:
                role_form.append(["inputs"] + valid_inputs)

        if self.outputs:
            valid_outputs = []
            for out in self.outputs:
                out_tokens: Set[str] = set()
                _extract_tokens(out, out_tokens)
                var_tokens = out_tokens - reserved_ops
                if var_tokens and var_tokens.issubset(trace_tokens):
                    valid_outputs.append(normalize_cpsa_term(out, akey_vars))
            if valid_outputs:
                role_form.append(["outputs"] + valid_outputs)

        if self.comment:
            role_form.append(["comment", f'"{self.comment}"'])

        return role_form


class CPSAStrandInstance(BaseModel):
    """Instantiation of a role strand within a preskeleton."""
    role_name: str = Field(..., description="Name of the instantiated role")
    trace_length: Optional[int] = Field(
        default=None,
        description="Trace height (optional; defstrandmax is always used to evaluate full strand)",
    )
    variable_bindings: Dict[str, CPSATerm] = Field(
        default_factory=dict,
        description="Mapping from role variable identifier to instantiated skeleton term conforming to CPSA grammar",
    )

    def to_cpsa_json(self) -> List[Any]:
        strand_form: List[Any] = ["defstrandmax", sanitize_cpsa_symbol(self.role_name)]
        for role_var, term_val in self.variable_bindings.items():
            strand_form.append([sanitize_cpsa_symbol(role_var), term_val])
        return strand_form


class CPSAPreskeleton(BaseModel):
    """Point-of-view preskeleton to be formally analyzed by CPSA."""
    protocol_name: str = Field(..., description="Target protocol identifier matching a declared defprotocol")
    description: Optional[str] = Field(default=None, description="Formal security objective or point-of-view scenario being verified")
    variables: List[CPSAVariableDeclaration] = Field(
        default_factory=list,
        description="Variables appearing across strands in the skeleton",
    )
    strands: List[CPSAStrandInstance] = Field(..., description="Role strands active in this execution scenario")
    non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Keys or secrets assumed never compromised/originating (non-orig)",
    )
    pen_non_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Penetrator non-originating terms (pen-non-orig)",
    )
    unique_originating: List[CPSATerm] = Field(
        default_factory=list,
        description="Nonces or secrets assumed fresh and unique across strands (uniq-orig)",
    )
    unique_generated: List[CPSATerm] = Field(
        default_factory=list,
        description="Uniquely generated terms (uniq-gen)",
    )
    listeners: List[CPSATerm] = Field(
        default_factory=list,
        description="Terms to verify secrecy for via listener strands (deflistener)",
    )
    precedes: List[List[List[int]]] = Field(
        default_factory=list,
        description="Causal message ordering constraints between node pairs: [((s1, n1), (s2, n2))]",
    )
    priority: List[List[Any]] = Field(
        default_factory=list,
        description="Solver priority overrides for specific nodes: [((s, n), int_priority)]",
    )
    facts: List[List[Any]] = Field(
        default_factory=list,
        description="Logical facts asserted in this skeleton",
    )
    comment: Optional[str] = None

    def to_cpsa_json(self) -> List[Any]:
        skel_form: List[Any] = ["defskeleton", sanitize_cpsa_symbol(self.protocol_name)]

        if self.variables:
            sort_to_vars: Dict[str, List[str]] = {}
            for v in self.variables:
                sort_to_vars.setdefault(v.sort.value, []).append(v.name)
            vars_form = ["vars"]
            for sort_val, var_names in sort_to_vars.items():
                vars_form.append(var_names + [sort_val])
            skel_form.append(vars_form)

        for strand in self.strands:
            skel_form.append(strand.to_cpsa_json())

        for listener in self.listeners:
            skel_form.append(["deflistener", listener])

        if self.non_originating:
            skel_form.append(["non-orig"] + self.non_originating)
        if self.pen_non_originating:
            skel_form.append(["pen-non-orig"] + self.pen_non_originating)
        skel_rndx = {v.name for v in self.variables if v.sort.value in ("rndx", "expt")}
        effective_skel_uo = []
        auto_skel_ug = list(self.unique_generated)
        for term in self.unique_originating:
            if isinstance(term, str) and (term in skel_rndx or "exponent" in term.lower() or term.endswith("_dh") or term.endswith("_exp")):
                if term not in auto_skel_ug:
                    auto_skel_ug.append(term)
            else:
                effective_skel_uo.append(term)

        if effective_skel_uo:
            skel_form.append(["uniq-orig"] + effective_skel_uo)
        if auto_skel_ug:
            skel_form.append(["uniq-gen"] + auto_skel_ug)
        if self.precedes:
            skel_form.append(["precedes"] + self.precedes)
        if self.priority:
            skel_form.append(["priority"] + self.priority)
        if self.facts:
            skel_form.append(["facts"] + self.facts)

        if self.comment:
            skel_form.append(["comment", f'"{self.comment}"'])

        return skel_form


class CPSAProtocolSpecification(BaseModel):
    """Complete protocol specification and verification suite."""
    protocol_name: str = Field(..., description="Unique protocol identifier")
    message_algebra: CPSAMessageAlgebra = Field(
        default="basic",
        description="CPSA message algebra selection: basic or diffie-hellman",
    )
    roles: List[CPSAProtocolRole] = Field(..., description="Protocol participant role specifications")
    primary_secrecy_goals: List[CPSATerm] = Field(
        default_factory=list,
        description=(
            "Primary confidential terms (e.g. established session keys, premaster secrets, shared tokens) "
            "semantically identified by the LLM from the RFC whose confidentiality must be verified via listener strands."
        ),
    )
    skeletons: List[CPSAPreskeleton] = Field(
        default_factory=list,
        description="Analysis preskeletons / points of view",
    )
    herald_comment: Optional[str] = None

    @model_validator(mode="after")
    def validate_algebra_consistency(self) -> "CPSAProtocolSpecification":
        """Ensures Diffie-Hellman operators are strictly forbidden under 'basic' message algebra."""
        if self.message_algebra == "basic":
            for term in self.primary_secrecy_goals:
                validate_cpsa_term_syntax(
                    term,
                    algebra="basic",
                    path="primary_secrecy_goals",
                )
            for role in self.roles:
                for evt in role.trace:
                    validate_cpsa_term_syntax(
                        evt.message_term,
                        algebra="basic",
                        path=f"role[{role.role_name}].trace",
                    )
                for term in role.inputs + role.outputs + role.non_originating + role.unique_originating:
                    validate_cpsa_term_syntax(
                        term,
                        algebra="basic",
                        path=f"role[{role.role_name}].declarations",
                    )
            for skel in self.skeletons:
                for listener in skel.listeners:
                    validate_cpsa_term_syntax(
                        listener,
                        algebra="basic",
                        path=f"skeleton[{skel.protocol_name}].listener",
                    )
        return self

    def to_cpsa_json_payload(self) -> List[List[Any]]:
        """Converts the specification into a sequence of top-level CPSA JSON forms."""
        payload: List[List[Any]] = []

        # Every SCM file MUST have a herald declaration per MITRE CPSA manual
        herald_text = self.herald_comment or f"{self.protocol_name} Protocol Verification Suite"
        if self.message_algebra == "diffie-hellman":
            payload.append(["herald", f'"{herald_text}"', ["algebra", "diffie-hellman"]])
        else:
            payload.append(["herald", f'"{herald_text}"'])

        clean_proto_name = sanitize_cpsa_symbol(self.protocol_name)
        prot_form: List[Any] = ["defprotocol", clean_proto_name, self.message_algebra]
        for role in self.roles:
            prot_form.append(role.to_cpsa_json())
        payload.append(prot_form)

        for skel in self.skeletons:
            payload.append(skel.to_cpsa_json())

        return payload
```

---

### `src/logging_config.py`

*sha256:`e6303bce3dae` · 159 lines · 5.6 KB · lang:`python`*

```python
"""Comprehensive Structured Logging Subsystem for RFC-LLM Pipeline."""

import logging
import sys
from pathlib import Path
from typing import Optional

from src.system_config import SYSTEM_CONFIG


class PipelineConsoleFormatter(logging.Formatter):
    """ANSI color-coded console formatter for distinct pipeline stages."""

    GREY = "\x1b[38;20m"
    CYAN = "\x1b[36;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    FORMAT_PREFIX = "%(asctime)s | "
    FORMAT_SUFFIX = " | %(name)s - %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + FORMAT_PREFIX + "DEBUG" + FORMAT_SUFFIX + RESET,
        logging.INFO: CYAN + FORMAT_PREFIX + "INFO " + FORMAT_SUFFIX + RESET,
        logging.WARNING: YELLOW + FORMAT_PREFIX + "WARN " + FORMAT_SUFFIX + RESET,
        logging.ERROR: RED + FORMAT_PREFIX + "ERROR" + FORMAT_SUFFIX + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT_PREFIX + "CRIT " + FORMAT_SUFFIX + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.GREY + self.FORMAT_PREFIX + "%(levelname)s" + self.FORMAT_SUFFIX + self.RESET)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def configure_pipeline_logging(
    log_level: int = logging.INFO,
    run_log_file: Optional[Path] = None,
) -> logging.Logger:
    """Configures the root pipeline logger with both console and file handlers."""
    SYSTEM_CONFIG.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger("rfc_llm")
    root_logger.setLevel(log_level)

    # Avoid duplicate handlers on re-entry
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Silence third-party litellm loggers completely
    for _noisy_logger in ("LiteLLM", "litellm", "LiteLLM Proxy", "LiteLLM Router"):
        _nl = logging.getLogger(_noisy_logger)
        _nl.setLevel(logging.ERROR)
        _nl.propagate = False

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(PipelineConsoleFormatter())
    root_logger.addHandler(console_handler)

    # 2. Global Pipeline File Handler
    global_log_path = SYSTEM_CONFIG.LOGS_DIR / "rfc_llm_pipeline.log"
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    global_file_handler = logging.FileHandler(global_log_path, mode="a", encoding="utf-8")
    global_file_handler.setLevel(logging.DEBUG)  # Always log debug to file
    global_file_handler.setFormatter(file_formatter)
    root_logger.addHandler(global_file_handler)

    # 3. Optional Per-Run File Handler
    if run_log_file:
        run_log_file.parent.mkdir(parents=True, exist_ok=True)
        run_file_handler = logging.FileHandler(run_log_file, mode="w", encoding="utf-8")
        run_file_handler.setLevel(logging.DEBUG)
        run_file_handler.setFormatter(file_formatter)
        root_logger.addHandler(run_file_handler)

    return root_logger


def get_pipeline_logger(subsystem: str) -> logging.Logger:
    """Returns a namespaced child logger for a specific pipeline subsystem."""
    return logging.getLogger(f"rfc_llm.{subsystem}")


class PipelineMetricsCSVLogger:
    """Logs tabular run-level experiment metrics to a persistent CSV for analysis."""

    CSV_HEADER = [
        "timestamp",
        "rfc_id",
        "is_eligible",
        "protocol_name",
        "selected_sections",
        "sliced_lines_count",
        "role_count",
        "preskeleton_count",
        "roletran_passed",
        "solver_passed",
        "shapes_count",
        "duration_seconds",
        "error_message",
    ]

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or (SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv")
        self._ensure_header()

    def _ensure_header(self) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            import csv
            with open(self.csv_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.CSV_HEADER)

    def log_run(
        self,
        rfc_id: str,
        is_eligible: bool,
        protocol_name: Optional[str] = None,
        selected_sections: Optional[List[str]] = None,
        sliced_lines_count: int = 0,
        role_count: int = 0,
        preskeleton_count: int = 0,
        roletran_passed: Optional[bool] = None,
        solver_passed: Optional[bool] = None,
        shapes_count: int = 0,
        duration_seconds: float = 0.0,
        error_message: Optional[str] = None,
    ) -> None:
        import csv
        import datetime
        now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sec_str = ";".join(selected_sections) if selected_sections else ""
        row = [
            now_iso,
            rfc_id,
            is_eligible,
            protocol_name or "",
            sec_str,
            sliced_lines_count,
            role_count,
            preskeleton_count,
            "" if roletran_passed is None else str(roletran_passed),
            "" if solver_passed is None else str(solver_passed),
            shapes_count,
            round(duration_seconds, 3),
            error_message or "",
        ]
        with open(self.csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
```

---

### `src/main_pipeline_orchestrator.py`

*sha256:`9144ac2fae8c` · 428 lines · 18.4 KB · lang:`python`*

```python
"""Main Pipeline Orchestrator for RFC-to-CPSA Synthesis."""

import time
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel, Field

from src.system_config import SYSTEM_CONFIG
from src.logging_config import configure_pipeline_logging, get_pipeline_logger, PipelineMetricsCSVLogger
from src.document_ingestion.rfc_header_filter import filter_rfc_header
from src.document_ingestion.rfc_toc_parser import parse_table_of_contents
from src.document_ingestion.protocol_applicability_gate import evaluate_protocol_applicability
from src.document_ingestion.handshake_section_router import route_handshake_sections
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections
from src.semantic_extraction.constrained_protocol_extractor import extract_protocol_specification
from src.code_generation.cpsa_scheme_emitter import emit_cpsa_scheme
from src.verification_engine.roletran_executability_gate import verify_role_executability
from src.verification_engine.mitre_build_orchestrator import execute_mitre_make_build, CPSABuildArtifacts
from src.verification_engine.compiler_diagnostic_repair import repair_protocol_specification
import hashlib
from src.pipeline_events import GLOBAL_EVENT_BUS

logger = get_pipeline_logger("orchestrator")


class PipelineExecutionSummary(BaseModel):
    """Execution summary of an end-to-end RFC synthesis run."""
    rfc_id: str = Field(..., description="Target RFC identifier")
    protocol_name: Optional[str] = Field(None, description="Identified protocol name")
    is_eligible: bool = Field(..., description="Whether the RFC passed intake filtering")
    selected_sections: List[str] = Field(default_factory=list, description="RFC sections sliced for synthesis")
    sliced_lines_count: int = Field(default=0, description="Number of lines in the verbatim slice")
    roletran_passed: bool = Field(default=False, description="Whether static role executability passed")
    build_successful: bool = Field(default=False, description="Whether MITRE make build succeeded")
    build_artifacts: Optional[CPSABuildArtifacts] = Field(None, description="Generated verification artifacts")
    duration_seconds: float = Field(default=0.0, description="Total pipeline execution time")
    error_message: Optional[str] = Field(None, description="Diagnostic error if pipeline halted")


def run_rfc_translation_pipeline(
    rfc_file_path: Path,
    output_dir: Optional[Path] = None,
    router_model: Optional[str] = None,
    extraction_model: Optional[str] = None,
    repair_model: Optional[str] = None,
    query_model: Optional[str] = None,
) -> PipelineExecutionSummary:
    """Executes the end-to-end RFC to formally verified MITRE CPSA synthesis pipeline."""
    start_time = time.time()
    rfc_id = rfc_file_path.stem.upper()

    target_output_dir = output_dir or (SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR / rfc_file_path.stem.lower())
    target_output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize per-run logger and CSV recorder
    run_log_path = target_output_dir / "run.log"
    configure_pipeline_logging(run_log_file=run_log_path)
    csv_recorder = PipelineMetricsCSVLogger()
    active_repair_model = repair_model or extraction_model or SYSTEM_CONFIG.DEFAULT_REPAIR_MODEL
    active_query_model = query_model or SYSTEM_CONFIG.DEFAULT_QUERY_MODEL

    logger.info("================================================================")
    logger.info("Starting RFC-LLM Synthesis Pipeline for: %s", rfc_file_path.name)
    logger.info("Output Directory: %s", target_output_dir)
    logger.info("================================================================")

    GLOBAL_EVENT_BUS.emit("pipeline_started", rfc_id=rfc_id, rfc_file=rfc_file_path.name)

    if not rfc_file_path.exists():
        err = f"RFC source file not found: {rfc_file_path}"
        logger.error(err)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=err)
        return PipelineExecutionSummary(rfc_id=rfc_id, is_eligible=False, error_message=err)

    with open(rfc_file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_rfc_text = f.read()

    # -------------------------------------------------------------------------
    # STAGE 1a: Tier 0 Header Filter
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=1, stage_name="Document Intake & Applicability Gate")
    header_res = filter_rfc_header(raw_rfc_text)
    if not header_res.is_eligible:
        elapsed = time.time() - start_time
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            error_message=header_res.disqualification_reason,
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, reason=header_res.disqualification_reason)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            is_eligible=False,
            duration_seconds=elapsed,
            error_message=header_res.disqualification_reason,
        )

    rfc_number_str = header_res.rfc_id or rfc_id
    protocol_title = header_res.title or "Unknown Protocol"

    # -------------------------------------------------------------------------
    # STAGE 1b: Full TOC Parsing
    # -------------------------------------------------------------------------
    toc_entries = parse_table_of_contents(raw_rfc_text)

    # Extract abstract lines
    abstract_lines = []
    lines = raw_rfc_text.splitlines()
    for idx, l in enumerate(lines[:120]):
        if re_match := l.strip().lower() == "abstract":
            abstract_lines = lines[idx + 1:idx + 35]
            break
    abstract_text = "\n".join(abstract_lines)

    # -------------------------------------------------------------------------
    # STAGE 1c: Tier 1 Applicability Gate
    # -------------------------------------------------------------------------
    app_report = evaluate_protocol_applicability(
        rfc_id=rfc_number_str,
        title=protocol_title,
        category=header_res.category or "Unknown",
        abstract=abstract_text,
        toc_entries=toc_entries,
        model=router_model,
    )

    if not app_report.is_cryptographic_protocol:
        elapsed = time.time() - start_time
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=False,
            protocol_name=app_report.protocol_name or protocol_title,
            error_message=f"Ineligible: {app_report.rationale}",
            duration_seconds=elapsed,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=1, reason=app_report.rationale)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=app_report.protocol_name or protocol_title,
            is_eligible=False,
            duration_seconds=elapsed,
            error_message=app_report.rationale,
        )

    final_proto_name = app_report.protocol_name or protocol_title
    GLOBAL_EVENT_BUS.emit("stage_completed", stage=1, protocol_name=final_proto_name)

    # -------------------------------------------------------------------------
    # STAGE 1d: Exchange Section Routing
    # -------------------------------------------------------------------------
    target_sections = route_handshake_sections(
        rfc_id=rfc_number_str,
        protocol_name=final_proto_name,
        toc_entries=toc_entries,
        model=router_model,
    )

    # -------------------------------------------------------------------------
    # STAGE 1e: Verbatim Section Slicing
    # -------------------------------------------------------------------------
    verbatim_slice = slice_verbatim_sections(raw_rfc_text, target_sections)
    slice_lines_count = len(verbatim_slice.splitlines())

    # Write slice to disk for auditing
    slice_file = target_output_dir / "verbatim_slice.txt"
    with open(slice_file, "w", encoding="utf-8") as f:
        f.write(verbatim_slice)

    GLOBAL_EVENT_BUS.emit(
        "slice_ready",
        sections=target_sections,
        line_count=slice_lines_count,
        slice_path=str(slice_file),
    )

    # -------------------------------------------------------------------------
    # STAGE 2: Constrained Extraction
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=2, stage_name="Constrained Protocol Extraction")
    try:
        protocol_ast = extract_protocol_specification(
            verbatim_slice=verbatim_slice,
            protocol_name=final_proto_name,
            principals=app_report.participating_principals,
            model=extraction_model,
        )
        GLOBAL_EVENT_BUS.emit(
            "stage_completed",
            stage=2,
            roles_count=len(protocol_ast.roles),
            skeletons_count=len(protocol_ast.skeletons),
            ast=protocol_ast.model_dump(),
        )
    except Exception as e:
        elapsed = time.time() - start_time
        err = f"Extraction failed: {e}"
        logger.error(err)
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            protocol_name=final_proto_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            duration_seconds=elapsed,
            error_message=err,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=2, error_message=err)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_proto_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            duration_seconds=elapsed,
            error_message=err,
        )

    # -------------------------------------------------------------------------
    # STAGE 3 & 4: Scheme SCM Emission
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=3, stage_name="CPSA Scheme Code Generation")
    scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir)
    GLOBAL_EVENT_BUS.emit("stage_completed", stage=3, scm_path=str(scm_path))

    # -------------------------------------------------------------------------
    # STAGE 5: Roletran Executability Gate (<15 ms) with RAG Self-Healing Loop
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=5, stage_name="Roletran Executability Verification")
    roletran_res = verify_role_executability(scm_path)
    attempt = 0
    seen_roletran_hashes = set()

    max_roletran_attempts = SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS
    while not roletran_res.is_executable and attempt < max_roletran_attempts:
        attempt += 1
        current_hash = hashlib.sha256(protocol_ast.model_dump_json().encode()).hexdigest()
        cycle_detected = current_hash in seen_roletran_hashes
        seen_roletran_hashes.add(current_hash)

        GLOBAL_EVENT_BUS.emit(
            "repair_attempt",
            stage=5,
            attempt=attempt,
            max_attempts=max_roletran_attempts,
            diagnostic=roletran_res.error_diagnostic,
            cycle_detected=cycle_detected,
        )

        logger.warning(
            "Roletran check failed on attempt %d/%d (cycle=%s): %s. Initiating fast self-healing repair...",
            attempt,
            max_roletran_attempts,
            cycle_detected,
            roletran_res.error_diagnostic,
        )
        try:
            protocol_ast = repair_protocol_specification(
                failing_spec=protocol_ast,
                error_diagnostic=roletran_res.error_diagnostic or "Executability verification failure",
                verbatim_slice=verbatim_slice,
                failure_stage="roletran",
                model=active_repair_model,
                query_model=active_query_model,
                cycle_detected=cycle_detected,
            )
            scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir)
            roletran_res = verify_role_executability(scm_path)
        except Exception as repair_err:
            logger.error("Self-healing repair exception on attempt %d: %s", attempt, repair_err)
            time.sleep(2)
            continue

    if roletran_res.is_executable:
        logger.info("Roletran executability check passed.")
        GLOBAL_EVENT_BUS.emit("stage_completed", stage=5, status="passed", attempts=attempt)
    else:
        logger.warning(
            "Roletran pre-flight executability check unfulfilled (%s). Proceeding directly to MITRE CPSA solver verification...",
            roletran_res.error_diagnostic,
        )
        GLOBAL_EVENT_BUS.emit(
            "stage_completed",
            stage=5,
            status="unfulfilled",
            diagnostic=roletran_res.error_diagnostic,
            attempts=attempt,
        )

    # -------------------------------------------------------------------------
    # STAGE 6: MITRE Build Orchestration with RAG Self-Healing Loop
    # -------------------------------------------------------------------------
    GLOBAL_EVENT_BUS.emit("stage_started", stage=6, stage_name="MITRE Build & Shapes Exploration")
    artifacts = None
    build_attempt = 0
    last_build_err = None
    seen_solver_hashes = set()

    while build_attempt <= SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS:
        try:
            artifacts = execute_mitre_make_build(scm_path, target_output_dir)
            break
        except Exception as e:
            last_build_err = str(e)
            if build_attempt < SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS:
                build_attempt += 1
                current_hash = hashlib.sha256(protocol_ast.model_dump_json().encode()).hexdigest()
                cycle_detected = current_hash in seen_solver_hashes
                seen_solver_hashes.add(current_hash)

                GLOBAL_EVENT_BUS.emit(
                    "repair_attempt",
                    stage=6,
                    attempt=build_attempt,
                    max_attempts=SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS,
                    diagnostic=last_build_err,
                    cycle_detected=cycle_detected,
                )

                logger.warning(
                    "MITRE make build failed (attempt %d/%d, cycle=%s): %s. Initiating RAG self-healing repair...",
                    build_attempt,
                    SYSTEM_CONFIG.MAX_REPAIR_ATTEMPTS,
                    cycle_detected,
                    last_build_err,
                )
                try:
                    combined_diagnostic = last_build_err
                    if not roletran_res.is_executable and roletran_res.error_diagnostic:
                        combined_diagnostic = (
                            f"MITRE CPSA make / solver failure:\n{last_build_err}\n\n"
                            f"Pre-flight Roletran Executability Diagnostic:\n{roletran_res.error_diagnostic}"
                        )

                    protocol_ast = repair_protocol_specification(
                        failing_spec=protocol_ast,
                        error_diagnostic=combined_diagnostic,
                        verbatim_slice=verbatim_slice,
                        failure_stage="solver",
                        model=active_repair_model,
                        query_model=active_query_model,
                        cycle_detected=cycle_detected,
                    )
                    scm_path = emit_cpsa_scheme(protocol_ast, target_output_dir)
                    roletran_res = verify_role_executability(scm_path)
                    if not roletran_res.is_executable:
                        logger.warning("Repaired spec failed roletran executability: %s", roletran_res.error_diagnostic)
                except Exception as repair_err:
                    logger.error("Build self-healing exception on attempt %d: %s", build_attempt, repair_err)
                    time.sleep(2)
                    continue
            else:
                break

    if artifacts is None:
        elapsed = time.time() - start_time
        err = f"MITRE make build failed after {build_attempt} repair attempts: {last_build_err}"
        logger.error(err)
        csv_recorder.log_run(
            rfc_id=rfc_id,
            is_eligible=True,
            protocol_name=final_proto_name,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            role_count=len(protocol_ast.roles),
            preskeleton_count=len(protocol_ast.skeletons),
            roletran_passed=True,
            solver_passed=False,
            duration_seconds=elapsed,
            error_message=err,
        )
        GLOBAL_EVENT_BUS.emit("stage_failed", stage=6, error_message=err)
        GLOBAL_EVENT_BUS.emit("pipeline_failed", error_message=err)
        return PipelineExecutionSummary(
            rfc_id=rfc_id,
            protocol_name=final_proto_name,
            is_eligible=True,
            selected_sections=target_sections,
            sliced_lines_count=slice_lines_count,
            roletran_passed=True,
            build_successful=False,
            duration_seconds=elapsed,
            error_message=err,
        )

    elapsed = time.time() - start_time
    csv_recorder.log_run(
        rfc_id=rfc_id,
        is_eligible=True,
        protocol_name=final_proto_name,
        selected_sections=target_sections,
        sliced_lines_count=slice_lines_count,
        role_count=len(protocol_ast.roles),
        preskeleton_count=len(protocol_ast.skeletons),
        roletran_passed=True,
        solver_passed=True,
        shapes_count=artifacts.shapes_count,
        duration_seconds=elapsed,
        error_message=None,
    )

    logger.info("================================================================")
    logger.info("Pipeline Complete for %s in %.2fs!", rfc_id, elapsed)
    logger.info("Generated: %s", artifacts.shapes_graph_xhtml_path)
    logger.info("================================================================")

    GLOBAL_EVENT_BUS.emit(
        "pipeline_completed",
        success=True,
        protocol_name=final_proto_name,
        duration_seconds=elapsed,
        shapes_count=artifacts.shapes_count,
        shapes_xhtml=str(artifacts.shapes_graph_xhtml_path),
        shapes_txt=str(artifacts.shapes_txt_path),
        scm_path=str(scm_path),
    )

    return PipelineExecutionSummary(
        rfc_id=rfc_id,
        protocol_name=final_proto_name,
        is_eligible=True,
        selected_sections=target_sections,
        sliced_lines_count=slice_lines_count,
        roletran_passed=True,
        build_successful=True,
        build_artifacts=artifacts,
        duration_seconds=elapsed,
    )
```

---

### `src/pipeline.py`

*sha256:`c1cf9ce2374b` · 272 lines · 10.1 KB · lang:`python`*

```python
"""Command-line interface for RFC-LLM synthesis pipeline supporting single RFCs and directory batching."""

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import List, Set

from src.system_config import SYSTEM_CONFIG
from src.main_pipeline_orchestrator import run_rfc_translation_pipeline, PipelineExecutionSummary


def natural_rfc_sort_key(file_path: Path):
    """Sorts RFC files by integer number if present (e.g. rfc10 before rfc100)."""
    match = re.search(r"rfc(\d+)", file_path.stem.lower())
    if match:
        return (0, int(match.group(1)))
    return (1, file_path.name)


def get_completed_rfc_ids() -> Set[str]:
    """Reads logs/pipeline_runs.csv to retrieve RFC IDs that were already evaluated."""
    csv_path = SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv"
    if not csv_path.exists():
        return set()

    completed = set()
    try:
        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rfc_val = row.get("rfc_id", "").strip()
                if rfc_val:
                    # Normalize 'RFC 5246' or 'RFC5246' to 'RFC5246'
                    clean_id = rfc_val.upper().replace(" ", "").replace("_", "")
                    completed.add(clean_id)
    except Exception:
        pass
    return completed


def main():
    parser = argparse.ArgumentParser(
        description="RFC-LLM: End-to-End Synthesis of Verified MITRE CPSA Models from IETF RFCs",
    )
    parser.add_argument(
        "target_path",
        type=str,
        help="Path to an RFC text file (such as refrences/all_RFCs/rfc5246.txt) OR a directory containing RFCs",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default=None,
        help="Directory to place synthesized models and build artifacts",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help="Global model identifier for all pipeline stages (e.g. 'gemini/gemini-3.5-flash-lite', 'ollama/qwen2.5:7b-instruct')",
    )
    parser.add_argument(
        "--router-model",
        type=str,
        default=None,
        help="Model identifier for document gatekeeper and TOC router",
    )
    parser.add_argument(
        "--extraction-model",
        type=str,
        default=None,
        help="Model identifier for Pydantic constrained semantic extraction",
    )
    parser.add_argument(
        "--repair-model",
        type=str,
        default=None,
        help="Model identifier for RAG self-healing compiler diagnostic repair",
    )
    parser.add_argument(
        "--query-model",
        type=str,
        default=None,
        help="Model identifier for RAG query formulation / conceptual abstraction",
    )
    parser.add_argument(
        "--no-visualize",
        action="store_true",
        help="Disable the live web dashboard visualizer (enabled by default)",
    )
    parser.add_argument(
        "--visualize",
        "-v",
        action="store_true",
        help="Ensure live web dashboard visualizer is enabled",
    )
    parser.add_argument(
        "--keep-alive",
        type=int,
        default=0,
        help="Seconds to keep visualizer server running after completion in non-interactive mode",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Web port for the live visualizer dashboard (default: 8080)",
    )
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=None,
        help="Maximum number of RFC files to process when pointing to a directory",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="rfc*.txt",
        help="Glob pattern for discovering RFC files when scanning a directory (default: 'rfc*.txt')",
    )
    parser.add_argument(
        "--skip-completed",
        action="store_true",
        help="Skip RFCs that already have completed run entries in logs/pipeline_runs.csv",
    )

    args = parser.parse_args()
    target = Path(args.target_path)

    if not target.exists():
        print(f"Error: Target path does not exist: {target}", file=sys.stderr)
        sys.exit(1)

    # 1. Resolve Target Files (Single File or Directory Batch)
    if target.is_file():
        rfc_files = [target]
    elif target.is_dir():
        rfc_files = sorted(list(target.glob(args.pattern)), key=natural_rfc_sort_key)
        if not rfc_files:
            # Fallback to all txt files if pattern yielded zero
            rfc_files = sorted(list(target.glob("*.txt")), key=natural_rfc_sort_key)
        if not rfc_files:
            print(f"Error: No RFC text files found in directory {target}", file=sys.stderr)
            sys.exit(1)

        if args.skip_completed:
            completed_ids = get_completed_rfc_ids()
            initial_count = len(rfc_files)
            rfc_files = [
                f for f in rfc_files
                if f.stem.upper().replace(" ", "").replace("_", "") not in completed_ids
            ]
            print(f"[BATCH] Filtered out {initial_count - len(rfc_files)} previously evaluated RFCs ({len(rfc_files)} remaining)")

        if args.limit and args.limit > 0:
            rfc_files = rfc_files[:args.limit]
            print(f"[BATCH] Processing limited to first {len(rfc_files)} RFCs")
    else:
        print(f"Error: Invalid target path: {target}", file=sys.stderr)
        sys.exit(1)

    # 2. Launch Visualizer (Default Enabled)
    enable_visualizer = not args.no_visualize
    monitor_url = None
    if enable_visualizer:
        import webbrowser
        from src.visualizer.server import run_visualizer_in_background

        try:
            server = run_visualizer_in_background(port=args.port)
            monitor_url = f"http://127.0.0.1:{server.port}"
            print(f"\n{'='*70}")
            print(f" [LIVE MONITOR] Active at: {monitor_url}")
            print(f"{'='*70}\n")
            try:
                webbrowser.open(monitor_url)
            except Exception:
                pass
        except Exception as e:
            print(f"[WARN] Could not launch live monitor: {e}")

    # 3. Execution Loop
    output_base_dir = Path(args.output_dir) if args.output_dir else None
    results: List[PipelineExecutionSummary] = []
    total_files = len(rfc_files)
    active_router_model = args.router_model or args.model or SYSTEM_CONFIG.DEFAULT_ROUTER_MODEL
    active_extraction_model = args.extraction_model or args.model or SYSTEM_CONFIG.DEFAULT_EXTRACTION_MODEL
    active_repair_model = args.repair_model or args.model or SYSTEM_CONFIG.DEFAULT_REPAIR_MODEL
    active_query_model = args.query_model or args.model or SYSTEM_CONFIG.DEFAULT_QUERY_MODEL

    for idx, rfc_file in enumerate(rfc_files, 1):
        if total_files > 1:
            print(f"\n{'='*70}")
            print(f"[{idx}/{total_files}] Processing RFC: {rfc_file.name}")
            print(f"{'='*70}")

        summary = run_rfc_translation_pipeline(
            rfc_file_path=rfc_file,
            output_dir=output_base_dir,
            router_model=active_router_model,
            extraction_model=active_extraction_model,
            repair_model=active_repair_model,
            query_model=active_query_model,
        )
        results.append(summary)

        if total_files == 1:
            # Single-file reporting and exit code
            if summary.build_successful:
                print("\n[SUCCESS] Synthesis & Formal Verification Completed!")
                print(f"Protocol: {summary.protocol_name}")
                print(f"Verified Shapes XHTML: {summary.build_artifacts.shapes_graph_xhtml_path}")
            elif summary.roletran_passed:
                print(f"\n[PARTIAL] Roletran passed, but MITRE build failed: {summary.error_message}")
            else:
                print(f"\n[HALTED] Pipeline stopped: {summary.error_message}")

            if enable_visualizer and monitor_url:
                print(f"\n[LIVE MONITOR] View execution trace and shapes at: {monitor_url}")
                if sys.stdin.isatty():
                    try:
                        input("[LIVE MONITOR] Press Enter to exit (server remains live until keypress)... ")
                    except (EOFError, KeyboardInterrupt):
                        pass
                elif args.keep_alive > 0:
                    import time
                    print(f"[LIVE MONITOR] Keeping server active for {args.keep_alive}s...")
                    time.sleep(args.keep_alive)

            sys.exit(0 if summary.build_successful else (1 if summary.roletran_passed else 2))

    # 4. Batch Summary Report
    print(f"\n{'='*70}")
    print(f"RFC-LLM BATCH SYNTHESIS REPORT ({total_files} RFCs Processed)")
    print(f"{'='*70}")
    verified_count = sum(1 for r in results if r.build_successful)
    eligible_count = sum(1 for r in results if r.is_eligible)
    ineligible_count = sum(1 for r in results if not r.is_eligible)
    roletran_failed = sum(1 for r in results if r.is_eligible and not r.roletran_passed)
    solver_failed = sum(1 for r in results if r.roletran_passed and not r.build_successful)

    print(f"• Total Processed      : {total_files}")
    print(f"• Ineligible (Filtered): {ineligible_count}")
    print(f"• Eligible Protocols   : {eligible_count}")
    print(f"• Formally Verified    : {verified_count}")
    if roletran_failed:
        print(f"• Roletran Failed      : {roletran_failed}")
    if solver_failed:
        print(f"• Solver Failed        : {solver_failed}")
    print(f"• Run Metrics Logged   : {SYSTEM_CONFIG.LOGS_DIR / 'pipeline_runs.csv'}")
    print(f"{'='*70}\n")

    if enable_visualizer and monitor_url:
        print(f"[LIVE MONITOR] Batch dashboard active at: {monitor_url}")
        if sys.stdin.isatty():
            try:
                input("[LIVE MONITOR] Press Enter to exit (server remains live until keypress)... ")
            except (EOFError, KeyboardInterrupt):
                pass
        elif args.keep_alive > 0:
            import time
            print(f"[LIVE MONITOR] Keeping server active for {args.keep_alive}s...")
            time.sleep(args.keep_alive)


if __name__ == "__main__":
    main()
```

---

### `src/pipeline_events.py`

*sha256:`2d908a3ad54e` · 72 lines · 2.4 KB · lang:`python`*

```python
"""Event bus and streaming state dispatcher for live pipeline visualization."""

import json
import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field


class PipelineEvent(BaseModel):
    """Structured event emitted across pipeline execution stages."""
    timestamp: float = Field(default_factory=time.time)
    event_type: str = Field(..., description="Type of event (e.g. stage_started, log, repair, artifact)")
    stage: Optional[int] = Field(None, description="Stage index (1 to 6)")
    stage_name: Optional[str] = Field(None, description="Human readable stage name")
    data: Dict[str, Any] = Field(default_factory=dict, description="Payload data")

    def to_sse_message(self) -> str:
        """Formats the event as a standard Server-Sent Event (SSE) frame."""
        payload = json.dumps(self.model_dump())
        return f"event: {self.event_type}\ndata: {payload}\n\n"


class PipelineEventBus:
    """Thread-safe event dispatcher supporting synchronous and async subscribers."""

    def __init__(self):
        self._listeners: List[Callable[[PipelineEvent], None]] = []
        self._history: List[PipelineEvent] = []

    def subscribe(self, callback: Callable[[PipelineEvent], None]):
        """Registers a listener callback."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def unsubscribe(self, callback: Callable[[PipelineEvent], None]):
        """Removes a listener callback."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def emit(
        self,
        event_type: str,
        stage: Optional[int] = None,
        stage_name: Optional[str] = None,
        **kwargs,
    ) -> PipelineEvent:
        """Emits an event to all subscribers and records it in history."""
        event = PipelineEvent(
            event_type=event_type,
            stage=stage,
            stage_name=stage_name,
            data=kwargs,
        )
        self._history.append(event)
        for listener in list(self._listeners):
            try:
                listener(event)
            except Exception:
                pass
        return event

    def get_history(self) -> List[PipelineEvent]:
        """Returns the full event log for replay."""
        return list(self._history)

    def clear(self):
        """Clears listener history."""
        self._history.clear()


# Global event bus singleton
GLOBAL_EVENT_BUS = PipelineEventBus()
```

---

### `src/semantic_extraction/constrained_protocol_extractor.py`

*sha256:`e78b45a0cb26` · 349 lines · 17.0 KB · lang:`python`*

```python
"""Constrained Protocol Semantic Extractor with RAG Grounding."""

import json
from typing import List, Optional
import litellm
from pydantic import ValidationError

from src.intermediate_representation.protocol_syntax_tree import (
    CPSAProtocolSpecification,
    CPSAPreskeleton,
    CPSAStrandInstance,
    CPSAVariableDeclaration,
)
from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("protocol_extractor")

# Lazy-loaded singleton retriever
_GLOBAL_RETRIEVER = None


def _get_retriever():
    global _GLOBAL_RETRIEVER
    if _GLOBAL_RETRIEVER is None:
        try:
            import importlib
            rag_module = importlib.import_module("refrences.scripts.03_query_rag")
            CPSASemanticRetriever = getattr(rag_module, "CPSASemanticRetriever")
            _GLOBAL_RETRIEVER = CPSASemanticRetriever()
            logger.info("Initialized CPSASemanticRetriever for extraction grounding")
        except Exception as e:
            logger.warning("Could not initialize CPSASemanticRetriever: %s", e)
            _GLOBAL_RETRIEVER = None
    return _GLOBAL_RETRIEVER


EXTRACTION_SYSTEM_PROMPT = """You are a formal methods expert in cryptographic protocol specification for MITRE CPSA 4.4.9.
Your task is to analyze the provided verbatim RFC specification text and extract a complete, mathematically rigorous CPSAProtocolSpecification.

CRITICAL MITRE CPSA 4.4.9 MANUAL GROUNDING (Chapters 2, 3, 4, 10 - Tables 10.1 through 10.6):
Every extracted construct must strictly obey the MITRE CPSA formal syntax:

1. Cryptographic Message Algebra (Tables 10.2, 10.4, 10.5):
   - Select "basic" for symmetric/asymmetric protocols, or "diffie-hellman" if modular exponentiation or Diffie-Hellman groups are used.
   - Diffie-Hellman Sorts (Section 4.2 & 10.3.2): Fresh randomly generated private exponents MUST be declared with sort "rndx" (atomic exponents). Sort "expt" is reserved for compound expressions or unconstrained received values. NEVER declare fresh originating exponents as "expt".

2. Term Syntax & Structure (Tables 10.3 & 10.5):
   - Formal Term Grammar:
     term ::= id | integer | (op term+)
   - STRICT ATOM ENFORCEMENT: A term is strictly an atom string (variable identifier e.g. "client_random", "session_key"), an integer constant (e.g. 1), or a prefix operator list [op, ...args].
   - ABSOLUTE NEGATIVE CONSTRAINT: A term is NEVER a dictionary or object (e.g. NEVER {"name": "...", "description": "..."}).
     Variables MUST BE DECLARED in the role's 'variables' list. In 'message_term', 'inputs', 'outputs', and 'unique_originating', variables are referenced ONLY by their plain string name atom (e.g. "session_key", "client_random").
   - Authorized Operator Signatures:
     * ["enc", term1, ..., termN, encryption_key] (Table 10.3): One or more payload terms followed by the encryption key as the LAST element.
     * ["hash", term1, ...] (Table 10.3): One-way hash digest.
     * ["cat", term1, term2, ...] (Table 10.3): Concatenation of terms.
     * ["pubk", principal_name] or ["privk", principal_name] (Table 10.3): Asymmetric key pairs.
     * ["invk", akey_var] (Table 10.3): Inverse of an asymmetric key variable.
     * ["ltk", principal1, principal2] (Table 10.3): Long-term shared symmetric key.
     * ["exp", base, expt] (Table 10.5): Exponentiation, e.g. ["exp", ["gen"], x].
     * ["gen"] (Table 10.5): 0-ary generator constant.
     * ["mul", expt1, expt2] (Table 10.5): Multiplication of exponents.
     * ["rec", expt] (Table 10.5): Multiplicative inverse of exponent.

3. Principal Roles & Executability Invariants (Tables 10.1 & 10.6, cpsa4roletran):
   - Variable Naming: Full self-explanatory semantic identifiers from the RFC (e.g. "client_identity", "client_random", "server_random", "session_key", "handshake_channel"). Never use single-letter abbreviations.
   - Populated Metadata: 'description' and 'rfc_field' must be populated for every variable.
   - Sort Mapping:
     * "name": principal identifiers
     * "text": fresh nonces and tokens
     * "data": arbitrary secrets, premaster secrets, or session payloads
     * "skey": symmetric encryption keys (keys used in ["enc", ..., key] for symmetric encryption MUST be sort "skey")
     * "akey": asymmetric keys
     * "chan": communication channels (every role must declare a channel variable, e.g. "handshake_channel")
     * "rndx": fresh Diffie-Hellman private exponents
   - Trace Events:
     * direction: "send" or "recv"
     * channel: e.g. "handshake_channel"
     * message_term: prefix term tree using valid operators or plain identifier atoms.
   - ROLETRAN EXECUTABILITY RULE: Every variable in "inputs", "outputs", and "unique_originating" MUST appear in that role's trace events!
     * "inputs": Terms known prior to execution (e.g. "handshake_channel", pre-shared keys).
     * "outputs": Established return terms (e.g. negotiated session tokens).
     * "unique_originating": Fresh nonces or secrets generated and first sent by this role.

4. Primary Secrecy & Confidentiality Goals:
   - Identify the primary confidential terms negotiated by the protocol (e.g. ["session_key"] or ["premaster_secret"]).

5. Point-of-View Preskeletons (Chapters 3 & 6):
   - POV Skeleton 1 (Initiator POV - Realized Handshake Shape):
     * strands: [defstrandmax for initiator role]
     * non_originating: uncompromised long-term/private keys (e.g. ["privk", "server_identity"])
     * unique_originating: fresh nonces generated by initiator (e.g. "client_random")
     * listeners: [] (STRICTLY EMPTY: never include deflistener in pure POV skeletons, or CPSA cannot realize the 2-party shape)
   - POV Skeleton 2 (Responder POV - Mutual Authentication):
     * strands: [defstrandmax for responder role]
     * non_originating: uncompromised long-term/private keys
     * unique_originating: fresh nonces generated by responder (e.g. "server_random")
     * listeners: [] (STRICTLY EMPTY)
   - Secrecy Skeleton 3 (Confidentiality Proof):
     * strands: [defstrandmax for initiator or responder]
     * listeners: [primary confidential term]
     * non_originating: uncompromised keys
     * unique_originating: fresh nonces

Return ONLY a valid JSON object matching the requested CPSAProtocolSpecification schema."""


def extract_protocol_specification(
    verbatim_slice: str,
    protocol_name: str,
    principals: Optional[List[str]] = None,
    model: Optional[str] = None,
) -> CPSAProtocolSpecification:
    """Extracts a validated CPSAProtocolSpecification from verbatim RFC text."""
    model_name = model or SYSTEM_CONFIG.DEFAULT_EXTRACTION_MODEL
    logger.info("Extracting CPSAProtocolSpecification for '%s' using %s", protocol_name, model_name)

    # 1. Retrieve RAG Grounding Context
    rag_context_blocks = []
    retriever = _get_retriever()
    if retriever:
        try:
            rag_query = f"{protocol_name} protocol message exchange encryption keys nonces"
            hits = retriever.search(rag_query, top_k=2, mode="hybrid", rerank=False)
            retrieved_meta = []
            for idx, chunk in enumerate(hits, 1):
                chunk_id = chunk.get("chunk_id") or chunk.get("id") or idx
                chunk_title = chunk.get("title") or chunk.get("breadcrumb") or f"Pattern {idx}"
                chunk_source = chunk.get("source_file") or chunk.get("source") or "MITRE Manual"
                chunk_text = chunk.get("text") or chunk.get("content") or ""
                rag_context_blocks.append(f"--- Reference {idx}: {chunk_title} ({chunk_source}) ---\n{chunk_text[:800]}")
                retrieved_meta.append({
                    "chunk_id": str(chunk_id),
                    "title": chunk_title,
                    "source_file": chunk_source,
                    "snippet": chunk_text[:280].strip() + ("..." if len(chunk_text) > 280 else ""),
                })
            from src.pipeline_events import GLOBAL_EVENT_BUS
            GLOBAL_EVENT_BUS.emit(
                "rag_retrieval",
                stage=2,
                purpose="Protocol Extraction Grounding",
                query=rag_query,
                chunks=retrieved_meta,
            )
        except Exception as e:
            logger.warning("RAG retrieval failed during extraction: %s", e)

    rag_grounding_text = "\n\n".join(rag_context_blocks) if rag_context_blocks else "Use standard MITRE CPSA 4.4.9 syntax conventions."

    principals_hint = f"Expected Principals: {', '.join(principals)}" if principals else ""

    user_prompt = f"""Protocol Identifier: {protocol_name}
{principals_hint}

MITRE CPSA Reference Syntax Examples (Helper Only - Use strictly for syntax and algebraic structure, NEVER as ground truth for protocol facts):
{rag_grounding_text}

Verbatim RFC Exchange Specification (SOLE GROUND TRUTH):
{verbatim_slice}

Extract the complete CPSAProtocolSpecification adhering to all executability and sort constraints.
Do NOT copy protocol elements, names, or messages from the reference examples; extract strictly what is defined in the Verbatim RFC Exchange Specification."""

    schema_str = json.dumps(CPSAProtocolSpecification.model_json_schema(), indent=2)
    system_prompt = f"{EXTRACTION_SYSTEM_PROMPT}\n\nRespond strictly with a valid JSON object matching this schema:\n{schema_str}"

    llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(model_name, temperature=0.0)
    response = None
    import time
    for retry_idx in range(3):
        try:
            response = litellm.completion(
                **llm_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
            )
            break
        except Exception as exc:
            err_msg = str(exc)
            if ("Timeout" in err_msg or "timed out" in err_msg or "429" in err_msg or "RateLimit" in err_msg) and retry_idx < 2:
                wait_sec = 10 * (retry_idx + 1)
                logger.warning("Extraction attempt %d failed (%s). Retrying in %ds...", retry_idx + 1, exc, wait_sec)
                time.sleep(wait_sec)
            else:
                raise

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except Exception:
        import json_repair
        data = json_repair.loads(content)

    try:
        spec = CPSAProtocolSpecification.model_validate(data)
    except ValidationError as val_err:
        logger.warning("Stage 2 schema validation error encountered: %s. Initiating 1-shot self-healing correction...", val_err)
        correction_prompt = f"""Your previous JSON output failed MITRE CPSA schema validation with the following errors:
{val_err}

CRITICAL MITRE CPSA MANUAL GROUNDING RULES (Chapter 10, Tables 10.1 - 10.6):
1. In 'message_term', terms MUST be plain string identifier atoms (e.g. 'client_random', 'session_key'), integers, or prefix lists like ['enc', payload, key].
   NEVER place variable objects or dictionaries inside message_term!
2. In ['enc', ...], the encryption key is ALWAYS the LAST element in the list.
3. Every variable in 'inputs', 'outputs', and 'unique_originating' MUST be sent or received in the role's trace!
4. Diffie-Hellman fresh exponents must be sort 'rndx'.

Return ONLY the corrected, fully valid JSON object."""
        try:
            corr_resp = litellm.completion(
                **llm_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": content},
                    {"role": "user", "content": correction_prompt},
                ],
                response_format={"type": "json_object"},
                timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
            )
            corr_content = corr_resp.choices[0].message.content
            try:
                corr_data = json.loads(corr_content)
            except Exception:
                import json_repair
                corr_data = json_repair.loads(corr_content)
            spec = CPSAProtocolSpecification.model_validate(corr_data)
            logger.info("Stage 2 self-healing correction SUCCEEDED")
        except Exception as retry_err:
            logger.error("Self-healing correction failed: %s. Raising validation error.", retry_err)
            raise val_err from retry_err

    spec = ensure_three_point_of_view_skeletons(spec)

    logger.info(
        "Extraction SUCCESS: Extracted protocol '%s' with %d roles and %d preskeletons",
        spec.protocol_name,
        len(spec.roles),
        len(spec.skeletons),
    )
    return spec


def ensure_three_point_of_view_skeletons(spec: CPSAProtocolSpecification) -> CPSAProtocolSpecification:
    """Guarantees the standard CPSA 3-skeleton architecture:
    1. Dedicated pure POV preskeleton for each communicating role with defstrandmax and NO listeners
       (enabling CPSA to compute minimal realized bilateral handshake shapes).
    2. A distinct secrecy preskeleton containing a deflistener for the primary secret.
    """
    if not spec.roles:
        return spec

    # Collect existing secrecy listeners and non-originating assumptions
    existing_listeners = []
    global_non_orig = []
    for skel in spec.skeletons:
        existing_listeners.extend(skel.listeners)
        global_non_orig.extend(skel.non_originating)

    # Dedup non-originating keys preserving order
    seen_no = set()
    dedup_non_orig = []
    for no in global_non_orig:
        s = json.dumps(no, sort_keys=True)
        if s not in seen_no:
            seen_no.add(s)
            dedup_non_orig.append(no)

    # Separate pure POV skeletons (without listeners) and secrecy skeletons (with listeners)
    roles_with_pure_pov = set()
    pure_skeletons = []
    secrecy_skeletons = []

    for skel in spec.skeletons:
        if not skel.listeners:
            pure_skeletons.append(skel)
            for strand in skel.strands:
                roles_with_pure_pov.add(strand.role_name)
        else:
            secrecy_skeletons.append(skel)

    # Build pure POV skeletons for roles that lack them
    new_pure_skeletons = list(pure_skeletons)
    for role in spec.roles:
        if role.role_name not in roles_with_pure_pov:
            bindings = {v.name: v.name for v in role.variables}
            skel_vars = [CPSAVariableDeclaration(name=v.name, sort=v.sort) for v in role.variables]
            new_skel = CPSAPreskeleton(
                protocol_name=spec.protocol_name,
                description=f"{role.role_name.capitalize()} Point of View (Authentication & Shape Realization)",
                variables=skel_vars,
                strands=[
                    CPSAStrandInstance(
                        role_name=role.role_name,
                        variable_bindings=bindings,
                    )
                ],
                non_originating=dedup_non_orig,
                unique_originating=list(role.unique_originating),
                listeners=[],
                comment=f"{role.role_name.capitalize()} Point of View",
            )
            new_pure_skeletons.append(new_skel)

    # Guarantee at least one secrecy verification skeleton if a secret was semantically identified by the LLM
    final_skeletons = new_pure_skeletons
    if secrecy_skeletons:
        final_skeletons.extend(secrecy_skeletons)
    else:
        # Determine the secrecy target strictly from the LLM's semantic output:
        # Priority 1: Listeners chosen by the LLM in existing skeletons
        # Priority 2: Terms designated in spec.primary_secrecy_goals by the LLM
        secret_targets = existing_listeners or spec.primary_secrecy_goals
        if secret_targets:
            chosen_secret = secret_targets[0]
            # Bind to the principal that originates or establishes this secret
            originating_role = spec.roles[0]
            for r in spec.roles:
                if any(chosen_secret == uo or (isinstance(uo, str) and uo == chosen_secret) for uo in r.unique_originating):
                    originating_role = r
                    break

            bindings = {v.name: v.name for v in originating_role.variables}
            skel_vars = [CPSAVariableDeclaration(name=v.name, sort=v.sort) for v in originating_role.variables]
            sec_skel = CPSAPreskeleton(
                protocol_name=spec.protocol_name,
                description=f"Secrecy Verification: tests confidentiality of {chosen_secret}",
                variables=skel_vars,
                strands=[
                    CPSAStrandInstance(
                        role_name=originating_role.role_name,
                        variable_bindings=bindings,
                    )
                ],
                non_originating=dedup_non_orig,
                unique_originating=list(originating_role.unique_originating),
                listeners=[chosen_secret],
                comment=f"Secrecy Point of View: Listener on {chosen_secret}",
            )
            final_skeletons.append(sec_skel)

    spec.skeletons = final_skeletons
    return spec
```

---

### `src/system_config.py`

*sha256:`087e83d9e0d4` · 115 lines · 5.3 KB · lang:`python`*

```python
import os
import warnings
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import litellm
from pydantic import model_validator
from pydantic_settings import BaseSettings

# Suppress third-party LiteLLM verbosity, debug info, and deprecation warnings
litellm.suppress_debug_info = True
litellm.set_verbose = False
for _logger_name in ("LiteLLM", "litellm", "LiteLLM Proxy", "LiteLLM Router"):
    logging.getLogger(_logger_name).setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning, module=".*litellm.*")
warnings.filterwarnings("ignore", category=UserWarning, module=".*litellm.*")
warnings.filterwarnings("ignore", message=".*temperature.*")

# Load .env file eagerly from project root
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)


class SystemEnvironmentConfig(BaseSettings):
    """Global system file paths, external tool binaries, and directories."""

    # Project Directories
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    RFCS_DIR: Path = PROJECT_ROOT / "refrences" / "all_RFCs"
    CHUNKS_DIR: Path = PROJECT_ROOT / "refrences" / "chunks"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    DEFAULT_OUTPUT_DIR: Path = PROJECT_ROOT / "output"

    # MITRE CPSA 4.4.9 Binary Paths
    CABAL_BIN_DIR: Path = Path.home() / ".cabal" / "bin"
    CPSA4_BIN: Path = CABAL_BIN_DIR / "cpsa4"
    CPSA4JSON_BIN: Path = CABAL_BIN_DIR / "cpsa4json"
    CPSA4ROLETRAN_BIN: Path = CABAL_BIN_DIR / "cpsa4roletran"
    CPSA4INIT_BIN: Path = CABAL_BIN_DIR / "cpsa4init"
    CPSA4SHAPES_BIN: Path = CABAL_BIN_DIR / "cpsa4shapes"
    CPSA4GRAPH_BIN: Path = CABAL_BIN_DIR / "cpsa4graph"
    CPSA4PROT_BIN: Path = CABAL_BIN_DIR / "cpsa4prot"

    # API Keys & Cloud Endpoints
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    NOUS_API_KEY: Optional[str] = os.getenv("NOUS_API_KEY")
    NOUS_API_BASE: str = os.getenv("NOUS_API_BASE", "https://inference-api.nousresearch.com/v1")
    OLLAMA_API_BASE: str = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

    # LLM Settings (Defaults read from MODEL_NAME or LLM_*_MODEL env vars)
    DEFAULT_MODEL: str = os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"
    DEFAULT_QUERY_MODEL: str = os.getenv("LLM_QUERY_MODEL") or os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"
    DEFAULT_ROUTER_MODEL: str = os.getenv("LLM_ROUTER_MODEL") or os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"
    DEFAULT_EXTRACTION_MODEL: str = os.getenv("LLM_EXTRACTION_MODEL") or os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"
    DEFAULT_REPAIR_MODEL: str = os.getenv("LLM_REPAIR_MODEL") or os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"

    # Timeouts & Limits
    SUBPROCESS_TIMEOUT_SECONDS: int = 180
    ROLETRAN_TIMEOUT_SECONDS: int = 15
    MAX_REPAIR_ATTEMPTS: int = 50

    model_config = {"env_file": ".env", "extra": "ignore"}

    @model_validator(mode="after")
    def resolve_empty_models(self) -> "SystemEnvironmentConfig":
        fallback = (self.DEFAULT_MODEL or "").strip() or "gemini/gemini-3.5-flash-lite"
        self.DEFAULT_MODEL = fallback
        if not (self.DEFAULT_QUERY_MODEL or "").strip():
            self.DEFAULT_QUERY_MODEL = fallback
        if not (self.DEFAULT_ROUTER_MODEL or "").strip():
            self.DEFAULT_ROUTER_MODEL = fallback
        if not (self.DEFAULT_EXTRACTION_MODEL or "").strip():
            self.DEFAULT_EXTRACTION_MODEL = fallback
        if not (self.DEFAULT_REPAIR_MODEL or "").strip():
            self.DEFAULT_REPAIR_MODEL = fallback
        return self

    def get_llm_kwargs(self, model_name: str, temperature: Optional[float] = None) -> Dict[str, Any]:
        """Returns provider-specific arguments (API keys, base URLs, sampling) for LiteLLM."""
        kwargs: Dict[str, Any] = {"model": model_name}
        if model_name.startswith("nous/") or model_name.startswith("nousresearch/"):
            target_model = model_name.split("/", 1)[1]
            kwargs["model"] = f"openai/{target_model}"
            kwargs["api_base"] = self.NOUS_API_BASE
            if self.NOUS_API_KEY:
                kwargs["api_key"] = self.NOUS_API_KEY
        elif model_name.startswith("ollama/"):
            kwargs["api_base"] = self.OLLAMA_API_BASE
        elif model_name.startswith("gemini/"):
            if self.GEMINI_API_KEY:
                kwargs["api_key"] = self.GEMINI_API_KEY
        elif model_name.startswith("openai/"):
            if self.OPENAI_API_KEY:
                kwargs["api_key"] = self.OPENAI_API_KEY
        elif model_name.startswith("anthropic/"):
            if self.ANTHROPIC_API_KEY:
                kwargs["api_key"] = self.ANTHROPIC_API_KEY

        # Handle temperature cleanly: Gemini 3+ models deprecate temp < 1.0 and perform best without it
        if temperature is not None:
            if model_name.startswith("gemini/"):
                if temperature > 0.0:
                    kwargs["temperature"] = temperature
            else:
                kwargs["temperature"] = temperature

        return kwargs


# Global singleton instance
SYSTEM_CONFIG = SystemEnvironmentConfig()
```

---

### `src/verification_engine/compiler_diagnostic_repair.py`

*sha256:`27b470b4d99c` · 244 lines · 13.4 KB · lang:`python`*

```python
"""Compiler Diagnostic Repair Engine with RAG-Guided Self-Healing."""

import json
from typing import Literal, Optional
import litellm

from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("diagnostic_repair")

_GLOBAL_RETRIEVER = None


def _get_retriever():
    global _GLOBAL_RETRIEVER
    if _GLOBAL_RETRIEVER is None:
        try:
            import importlib
            rag_module = importlib.import_module("refrences.scripts.03_query_rag")
            CPSASemanticRetriever = getattr(rag_module, "CPSASemanticRetriever")
            _GLOBAL_RETRIEVER = CPSASemanticRetriever()
        except Exception as e:
            logger.warning("Could not initialize CPSASemanticRetriever for repair: %s", e)
            _GLOBAL_RETRIEVER = None
    return _GLOBAL_RETRIEVER


REPAIR_SYSTEM_PROMPT = """You are a formal methods expert in debugging and repairing MITRE CPSA 4.4.9 protocol specifications.
You are given a failing CPSAProtocolSpecification, the verbatim RFC exchange text, the compiler error diagnostic, and retrieved guidance from the MITRE CPSA reference manual.

Your task is to identify the precise defect causing the compiler or solver failure and return a corrected CPSAProtocolSpecification.

Common Diagnostics & Fixes:
1. "Undeclared variable <var>":
   - A variable is declared in "inputs", "outputs", or "unique_originating", but does NOT occur anywhere in the role's trace events!
   - Fix: Remove the variable from "inputs", "outputs", and "unique_originating". In CPSA roletran, every variable in inputs/outputs/uniq-orig must actually appear in a trace send or recv.
2. "Cannot build <term>":
   - A role attempts to send a term before it has been generated ("unique_originating"), received, or passed as an input ("inputs").
   - Or, a symmetric encryption key in ["enc", payload, key] was mistakenly declared as "data" instead of "skey".
   - Fix: Change key sort to "skey". Add fresh originating terms to "unique_originating". Add known parameters or channels to "inputs".
3. "Received term cannot be fully destructured":
   - A role receives an encrypted message or hash, but lacks the necessary decryption key or preimage in its "inputs".
   - Fix: Ensure the role's "inputs" list includes the required key (e.g. held private key or shared secret) to decrypt the incoming payload.
4. Preskeleton Architecture (MANDATORY 3-SKELETON SEPARATION):
   - CRITICAL: Never put 'deflistener' inside pure POV skeletons! A listener on an uncompromised secret causes CPSA to abort without displaying the completed bilateral protocol handshake shape.
   - Separate into 3 distinct skeletons:
     * Skeleton 1: Initiator / Client POV (defstrandmax initiator, listeners: [])
     * Skeleton 2: Responder / Server POV (defstrandmax responder, listeners: [])
     * Skeleton 3: Secrecy POV (defstrandmax + deflistener for the secret)
   - Preserve uncompromised private keys under "non_originating" and fresh nonces under "unique_originating".
5. "Expecting a name":
   - An asymmetric key constructor like ["pubk", key] or ["privk", key] was passed an asymmetric key variable (sort "akey") instead of a principal identifier (sort "name").
   - Fix: In CPSA, if an asymmetric key variable 'k' is declared with sort "akey", use 'k' and ["invk", 'k'] directly without wrapping in "pubk" or "privk". "pubk" and "privk" only accept variables of sort "name".
6. "Uniquely originating value ... does not originate in trace":
   - A variable declared under "unique_originating" is only transmitted inside a ["hash", ...] one-way digest, or is never transmitted.
   - Fix: Remove the variable from "unique_originating". In CPSA, atoms cannot originate inside a one-way hash.
7. Variable Naming & Metadata Integrity:
   - Preserve all descriptive, domain-specific identifiers (e.g. "client_identity", "server_identity", "client_random", "premaster_secret"). Do NOT downgrade them to single-letter or toy abbreviations like 'a', 'b', 'init', 'resp', 'k'.
   - Preserve and update the 'description' and 'rfc_field' metadata fields.
8. NEVER Emit Foreign Operator "aenc" or "senc":
   - CPSA message algebra has NO "aenc" or "senc" operator!
   - In CPSA, ALL encryption (both symmetric and asymmetric) strictly uses "enc": ["enc", payload, key].
   - If encrypting with a public key, use ["enc", payload, ["pubk", name]] or ["enc", payload, key]. NEVER write "aenc".

Return ONLY the repaired, valid CPSAProtocolSpecification matching the requested JSON schema."""


DIAGNOSTIC_QUERY_SYSTEM_PROMPT = """You are a formal verification compiler diagnostic analyst for MITRE CPSA 4.4.9 (Cryptographic Protocol Shapes Analyzer).
Your task is to analyze a compiler/solver diagnostic error and formulate a concise, targeted search query (3 to 6 words) to retrieve the relevant formal rules from the MITRE CPSA reference manual.

CRITICAL INSTRUCTIONS FOR RETRIEVAL PRECISION:
1. ABSTRACT CONCRETE IDENTIFIERS:
   NEVER include protocol-specific variable names, role names, file paths, line numbers, or literals from the error (e.g. forbid 'client_random', 'session_id', 'tls_1_2', 'premaster_secret', 'server_hello_done', '.scm:72:6').
   Abstract them into formal CPSA grammar, algebra, or roletran concepts (e.g. 'roletran term origination trace inputs', 'defskeleton vars declaration binding', 'order-sorted algebra sort mismatch', 'asymmetric key sort rules').
2. OUTPUT FORMAT:
   Output strictly the plain text search query (3 to 6 words). Do NOT include quotes, explanations, markdown, or punctuation."""


def fallback_sanitize_diagnostic_query(diagnostic: str, failure_stage: str) -> str:
    """Fallback sanitizer for compiler diagnostics when LLM query formulation is unavailable,
    stripping file paths, line numbers, and Make boilerplate."""
    import re
    cleaned = re.sub(r'MITRE build failed for [^:]+:\s*', '', diagnostic, flags=re.IGNORECASE)
    cleaned = re.sub(r'make(\[\d+\])?:.*', '', cleaned)
    cleaned = re.sub(r'[a-zA-Z0-9_\-\./]+\.(scm|txt|xhtml|mk|hs|pl)(:\d+:\d+)?:?', '', cleaned)
    cleaned = re.sub(r'\(.*?\)', '', cleaned)
    cleaned = re.sub(r'["\':*#\n\r]', ' ', cleaned)
    tokens = [t for t in cleaned.split() if len(t) > 2 and not t.isdigit() and t.lower() not in {"error", "exit", "code", "failed"}]
    concise = " ".join(tokens[:5])
    if concise:
        return f"CPSA {failure_stage} {concise} syntax manual error rule fix"
    return f"CPSA {failure_stage} syntax manual error rule fix"


def formulate_rag_diagnostic_query(diagnostic: str, failure_stage: str, model: Optional[str] = None) -> str:
    """Uses a dedicated LLM call to formulate a targeted conceptual query for the MITRE CPSA manual,
    purging concrete variable names and local file paths. Falls back to deterministic sanitization if offline."""
    query_model = model or SYSTEM_CONFIG.DEFAULT_QUERY_MODEL
    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(query_model, temperature=0.0)
        user_prompt = f"Failure Stage: {failure_stage}\nCompiler Diagnostic:\n{diagnostic}"
        resp = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": DIAGNOSTIC_QUERY_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            timeout=10,
        )
        content = resp.choices[0].message.content
        if content:
            query = " ".join(content.strip().strip('"').strip("'").split())
            if query:
                return query
    except Exception as exc:
        logger.warning("LLM diagnostic query generation failed (%s), using fallback sanitizer", exc)

    return fallback_sanitize_diagnostic_query(diagnostic, failure_stage)


def clean_rag_diagnostic_query(diagnostic: str, failure_stage: str, model: Optional[str] = None) -> str:
    """Legacy alias routing to LLM query formulation."""
    return formulate_rag_diagnostic_query(diagnostic, failure_stage, model=model)


def repair_protocol_specification(
    failing_spec: CPSAProtocolSpecification,
    error_diagnostic: str,
    verbatim_slice: str,
    failure_stage: Literal["roletran", "solver"],
    model: Optional[str] = None,
    query_model: Optional[str] = None,
    cycle_detected: bool = False,
) -> CPSAProtocolSpecification:
    """Uses RAG-guided diagnostic repair to patch a failing CPSAProtocolSpecification."""
    model_name = model or SYSTEM_CONFIG.DEFAULT_REPAIR_MODEL
    logger.info("Executing RAG-guided repair for stage '%s' (cycle_detected=%s) with diagnostic: %s", failure_stage, cycle_detected, error_diagnostic)

    # 1. RAG Retrieval on Compiler Diagnostic
    retrieved_guidance = []
    retriever = _get_retriever()
    if retriever:
        try:
            rag_query = formulate_rag_diagnostic_query(error_diagnostic, failure_stage, model=query_model)
            hits = retriever.search(rag_query, top_k=2, mode="hybrid", rerank=False)
            retrieved_meta = []
            for idx, chunk in enumerate(hits, 1):
                chunk_id = chunk.get("chunk_id") or chunk.get("id") or idx
                chunk_title = chunk.get("title") or chunk.get("breadcrumb") or f"Manual Section {idx}"
                chunk_source = chunk.get("source_file") or chunk.get("source") or "Manual"
                chunk_text = chunk.get("text") or chunk.get("content") or ""
                retrieved_guidance.append(f"--- Retrieved Manual Guidance {idx}: {chunk_title} ({chunk_source}) ---\n{chunk_text[:800]}")
                retrieved_meta.append({
                    "chunk_id": str(chunk_id),
                    "title": chunk_title,
                    "source_file": chunk_source,
                    "snippet": chunk_text[:280].strip() + ("..." if len(chunk_text) > 280 else ""),
                })
            from src.pipeline_events import GLOBAL_EVENT_BUS
            GLOBAL_EVENT_BUS.emit(
                "rag_retrieval",
                stage=5 if failure_stage == "roletran" else 6,
                purpose=f"Diagnostic Repair ({failure_stage})",
                query=rag_query,
                chunks=retrieved_meta,
            )
        except Exception as e:
            logger.warning("RAG retrieval failed during repair: %s", e)

    guidance_text = "\n\n".join(retrieved_guidance) if retrieved_guidance else "Review standard CPSA executability and preskeleton assumption rules."

    cycle_warning = ""
    if cycle_detected:
        cycle_warning = (
            "\n\nCRITICAL WARNING: An oscillation/cycle was detected. You previously generated a specification "
            "identical or near-identical to this one that already failed. Do NOT repeat the previous edits. "
            "You MUST apply an alternative repair strategy (e.g. check sort declarations, add missing variables to role inputs, "
            "or adjust preskeleton non-originating/unique-originating assumptions) to escape this cycle."
        )

    # Truncate verbatim slice to concise context to preserve token quota across multiple repair passes
    slice_snippet = verbatim_slice[:3000]
    if len(verbatim_slice) > 3000:
        slice_snippet += "\n... [Remaining RFC specification text truncated for compiler repair pass] ..."

    user_prompt = f"""Failing Protocol: {failing_spec.protocol_name}
Failure Stage: {failure_stage}
Compiler Diagnostic / Error:
{error_diagnostic}

MITRE CPSA Reference Guidance (Helper Only - Explains syntax rules and failure mechanisms):
{guidance_text}

Verbatim RFC Exchange Specification (Excerpt for repair context):
{slice_snippet}

Current Failing CPSA Specification (JSON):
{failing_spec.model_dump_json(indent=2)}{cycle_warning}

Provide the complete repaired CPSAProtocolSpecification resolving the error without inventing fictional protocol terms."""

    # Use higher temperature if cycle detected to break greedy minimum
    temp = 0.4 if cycle_detected else 0.0
    schema_str = json.dumps(CPSAProtocolSpecification.model_json_schema(), indent=2)
    system_prompt = f"{REPAIR_SYSTEM_PROMPT}\n\nRespond strictly with a valid JSON object matching this schema:\n{schema_str}"

    llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(model_name, temperature=temp)
    response = None
    for retry_idx in range(4):
        try:
            response = litellm.completion(
                **llm_kwargs,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
            )
            break
        except Exception as exc:
            err_msg = str(exc)
            if ("429" in err_msg or "Quota exceeded" in err_msg or "RateLimitError" in err_msg) and retry_idx < 3:
                wait_sec = 30 * (retry_idx + 1)
                logger.warning("Quota rate limit reached during repair pass. Waiting %ds before retry: %s", wait_sec, exc)
                time.sleep(wait_sec)
            else:
                raise

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except Exception:
        import json_repair
        data = json_repair.loads(content)

    repaired_spec = CPSAProtocolSpecification.model_validate(data)
    from src.semantic_extraction.constrained_protocol_extractor import ensure_three_point_of_view_skeletons
    repaired_spec = ensure_three_point_of_view_skeletons(repaired_spec)

    logger.info("Repair pass completed for '%s'", repaired_spec.protocol_name)
    return repaired_spec
```

---

### `src/verification_engine/mitre_build_orchestrator.py`

*sha256:`ae19df718b6d` · 151 lines · 5.6 KB · lang:`python`*

```python
"""MITRE Build Orchestrator for CPSA Verification and Visualization."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("build_orchestrator")


class CPSABuildArtifacts(BaseModel):
    """Paths to all artifacts emitted by the MITRE CPSA build system."""
    protocol_stem: str = Field(..., description="Base identifier stem for protocol outputs")
    scm_path: Path = Field(..., description="Source MITRE Scheme model file")
    trace_txt_path: Path = Field(..., description="Raw strand space solver derivations (.txt)")
    shapes_txt_path: Path = Field(..., description="Distilled minimal realized shapes (.txt)")
    full_graph_xhtml_path: Path = Field(..., description="Interactive SVG graph of all search steps (.xhtml)")
    shapes_graph_xhtml_path: Path = Field(..., description="Interactive SVG graph of proved shapes (.xhtml)")
    shapes_count: int = Field(default=0, description="Total number of realized shapes discovered")


class CPSABuildError(Exception):
    """Raised when the MITRE make build process fails."""
    pass


def _ensure_cpsa_makefile(target_dir: Path) -> None:
    """Ensures cpsa4init has initialized the official Makefile and cpsa4.mk in target_dir."""
    makefile = target_dir / "Makefile"
    cpsa_mk = target_dir / "cpsa4.mk"

    if makefile.exists() and cpsa_mk.exists():
        return

    logger.info("Initializing MITRE CPSA Makefile in %s via cpsa4init", target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    if not SYSTEM_CONFIG.CPSA4INIT_BIN.exists():
        raise FileNotFoundError(f"cpsa4init binary missing at {SYSTEM_CONFIG.CPSA4INIT_BIN}")

    proc = subprocess.run(
        [str(SYSTEM_CONFIG.CPSA4INIT_BIN)],
        cwd=target_dir,
        capture_output=True,
        text=True,
        check=False,
    )

    if proc.returncode != 0:
        logger.error("cpsa4init failed in %s: %s", target_dir, proc.stderr)
        raise CPSABuildError(f"cpsa4init initialization failed: {proc.stderr}")


def _count_shapes_in_file(shapes_txt_path: Path) -> int:
    """Counts the number of distinct realized shape skeletons in the shape summary file."""
    if not shapes_txt_path.exists():
        return 0
    try:
        with open(shapes_txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        import re
        # Skeletons that are shapes are identified by "(shape" or "(defskeleton" in shapes.txt
        matches = re.findall(r"\(defskeleton\s+", content)
        return len(matches)
    except Exception as e:
        logger.warning("Could not count shapes in %s: %s", shapes_txt_path, e)
        return 0


def execute_mitre_make_build(
    scm_path: Path,
    output_directory: Optional[Path] = None,
    build_full_graph: bool = True,
) -> CPSABuildArtifacts:
    """Orchestrates GNU Make to compile a Scheme model through cpsa4, cpsa4shapes, and cpsa4graph."""
    build_dir = output_directory or scm_path.parent
    build_dir.mkdir(parents=True, exist_ok=True)

    _ensure_cpsa_makefile(build_dir)

    stem = scm_path.stem
    target_scm_in_build = build_dir / f"{stem}.scm"

    # Ensure scm file is located in build_dir
    if scm_path.resolve() != target_scm_in_build.resolve():
        shutil.copy(scm_path, target_scm_in_build)

    logger.info("Executing MITRE make build for '%s' in %s", stem, build_dir)

    # Inject ~/.cabal/bin into subprocess PATH so GNU make resolves cpsa4, cpsa4shapes, cpsa4graph
    env = os.environ.copy()
    cabal_bin_str = str(SYSTEM_CONFIG.CABAL_BIN_DIR)
    env["PATH"] = f"{cabal_bin_str}:{env.get('PATH', '')}"

    # Target 1: Minimal shapes graph (triggers cpsa4, cpsa4shapes, and cpsa4graph)
    target_shapes_xhtml = f"{stem}_shapes.xhtml"
    proc_shapes = subprocess.run(
        ["make", target_shapes_xhtml],
        cwd=build_dir,
        capture_output=True,
        text=True,
        env=env,
        timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
        check=False,
    )

    if proc_shapes.returncode != 0:
        err_msg = proc_shapes.stderr.strip() or proc_shapes.stdout.strip()
        logger.error("Make build failed for %s: %s", target_shapes_xhtml, err_msg)
        raise CPSABuildError(f"MITRE build failed for {target_shapes_xhtml}: {err_msg}")

    # Target 2 (Optional): Full derivation search graph
    if build_full_graph:
        target_full_xhtml = f"{stem}.xhtml"
        subprocess.run(
            ["make", target_full_xhtml],
            cwd=build_dir,
            capture_output=True,
            text=True,
            env=env,
            timeout=SYSTEM_CONFIG.SUBPROCESS_TIMEOUT_SECONDS,
            check=False,
        )

    # Verify generated artifact paths
    trace_txt = build_dir / f"{stem}.txt"
    shapes_txt = build_dir / f"{stem}_shapes.txt"
    full_xhtml = build_dir / f"{stem}.xhtml"
    shapes_xhtml = build_dir / f"{stem}_shapes.xhtml"

    for artifact in [trace_txt, shapes_txt, shapes_xhtml]:
        if not artifact.exists():
            raise CPSABuildError(f"Expected build artifact {artifact} was not produced by make")

    shapes_count = _count_shapes_in_file(shapes_txt)
    logger.info("Build SUCCESS: Generated %s with %d realized shapes", shapes_xhtml.name, shapes_count)

    return CPSABuildArtifacts(
        protocol_stem=stem,
        scm_path=target_scm_in_build,
        trace_txt_path=trace_txt,
        shapes_txt_path=shapes_txt,
        full_graph_xhtml_path=full_xhtml if full_xhtml.exists() else shapes_xhtml,
        shapes_graph_xhtml_path=shapes_xhtml,
        shapes_count=shapes_count,
    )
```

---

### `src/verification_engine/roletran_executability_gate.py`

*sha256:`08032193b650` · 116 lines · 5.0 KB · lang:`python`*

```python
"""MITRE CPSA Roletran Pre-Flight Executability Gate (<15 ms)."""

import re
import subprocess
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("roletran_gate")


class RoletranVerificationResult(BaseModel):
    """Result of the static executability verification pass."""
    is_executable: bool = Field(..., description="True if all roles are mathematically constructible and destructible")
    error_diagnostic: Optional[str] = Field(None, description="Concise error diagnostic if executability failed")
    procedural_defproc_code: Optional[str] = Field(None, description="Compiled defproc procedural code if successful")
    raw_stderr: str = Field(default="", description="Complete stderr from roletran execution")


def verify_role_executability(scm_path: Path) -> RoletranVerificationResult:
    """Executes cpsa4roletran on a Scheme model to prove term constructibility and destructibility."""
    logger.info("Executing roletran pre-flight executability gate on %s", scm_path)

    if not SYSTEM_CONFIG.CPSA4ROLETRAN_BIN.exists():
        logger.error("cpsa4roletran binary missing at %s", SYSTEM_CONFIG.CPSA4ROLETRAN_BIN)
        raise FileNotFoundError(f"cpsa4roletran binary missing at {SYSTEM_CONFIG.CPSA4ROLETRAN_BIN}")

    try:
        with open(scm_path, "r", encoding="utf-8") as f:
            scm_content = f.read()

        is_dh = "diffie-hellman" in scm_content
        if is_dh:
            # MITRE CPSA 4.4.9 cpsa4roletran only supports basic algebra.
            # For Diffie-Hellman protocols, validate pre-flight syntax and role well-formedness using cpsa4.
            logger.info("Protocol uses diffie-hellman message algebra; executing cpsa4 pre-flight validation gate")
            proc = subprocess.run(
                [str(SYSTEM_CONFIG.CPSA4_BIN), "-l", "1", str(scm_path)],
                capture_output=True,
                text=True,
                timeout=SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS,
                check=False,
            )
            stderr_output = proc.stderr.strip()
            stdout_output = proc.stdout.strip()
            combined = (stderr_output + "\n" + stdout_output).strip()
            if "Role not well formed" in combined or "error" in combined.lower() or proc.returncode != 0:
                error_msg = ""
                for line in combined.splitlines():
                    if "Role not well formed" in line or "error" in line.lower() or "Expecting" in line:
                        error_msg = line.strip()
                        break
                error_msg = error_msg or combined[:300]
                logger.warning("Diffie-Hellman pre-flight validation REJECT: %s", error_msg)
                return RoletranVerificationResult(
                    is_executable=False,
                    error_diagnostic=error_msg,
                    raw_stderr=combined,
                )
            logger.info("Diffie-Hellman pre-flight validation PASS: All roles are algebraically well-formed")
            return RoletranVerificationResult(
                is_executable=True,
                procedural_defproc_code="(diffie-hellman-validated)",
                raw_stderr="",
            )

        proc = subprocess.run(
            [str(SYSTEM_CONFIG.CPSA4ROLETRAN_BIN)],
            input=scm_content,
            capture_output=True,
            text=True,
            timeout=SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS,
            check=False,
        )

        stderr_output = proc.stderr.strip()
        stdout_output = proc.stdout.strip()

        if proc.returncode == 0 and not stderr_output:
            logger.info("Roletran PASS: All protocol roles are statically executable")
            return RoletranVerificationResult(
                is_executable=True,
                procedural_defproc_code=stdout_output,
                raw_stderr="",
            )

        # Parse error message: e.g. ":6:6: Received term cannot be fully destructured"
        clean_error = stderr_output
        match = re.search(r":\d+:\d+:\s*(.*)", stderr_output)
        if match:
            clean_error = match.group(1).strip()

        logger.warning("Roletran REJECT: %s", clean_error)
        return RoletranVerificationResult(
            is_executable=False,
            error_diagnostic=clean_error,
            raw_stderr=stderr_output,
        )

    except subprocess.TimeoutExpired:
        logger.error("Roletran check timed out after %d seconds", SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS)
        return RoletranVerificationResult(
            is_executable=False,
            error_diagnostic=f"Roletran verification timed out after {SYSTEM_CONFIG.ROLETRAN_TIMEOUT_SECONDS}s",
            raw_stderr="Timeout",
        )
    except Exception as e:
        logger.error("Unexpected failure running roletran: %s", str(e))
        return RoletranVerificationResult(
            is_executable=False,
            error_diagnostic=str(e),
            raw_stderr=str(e),
        )
```

---

### `src/visualizer/__init__.py`

*sha256:`b5ef0fe4ac5a` · 1 lines · 0.1 KB · lang:`python`*

```python
"""RFC-LLM Live Visualization and Interactive Dashboard Module."""
```

---

### `src/visualizer/server.py`

*sha256:`e377cb5b737c` · 160 lines · 5.9 KB · lang:`python`*

```python
"""Asynchronous web server for live RFC-to-CPSA synthesis visualization."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Set
from aiohttp import web

from src.system_config import SYSTEM_CONFIG
from src.pipeline_events import GLOBAL_EVENT_BUS, PipelineEvent

logger = logging.getLogger("rfc_llm.visualizer")

HTML_TEMPLATE_PATH = Path(__file__).parent / "static" / "index.html"


class VisualizerServer:
    """Manages SSE streaming, artifact serving, and dashboard state."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self._sse_clients: Set[asyncio.Queue] = set()
        self._setup_routes()

        # Connect event bus to SSE clients
        GLOBAL_EVENT_BUS.subscribe(self._on_bus_event)

    def _setup_routes(self):
        self.app.router.add_get("/", self.handle_index)
        self.app.router.add_get("/api/events", self.handle_sse)
        self.app.router.add_get("/api/history", self.handle_history)
        self.app.router.add_get("/api/artifact", self.handle_artifact)
        self.app.router.add_static("/output", SYSTEM_CONFIG.DEFAULT_OUTPUT_DIR, show_index=True)

    def _on_bus_event(self, event: PipelineEvent):
        """Dispatches an event from the pipeline event bus to all connected web clients thread-safely."""
        if hasattr(self, "loop") and self.loop and self.loop.is_running():
            for q in list(self._sse_clients):
                try:
                    self.loop.call_soon_threadsafe(q.put_nowait, event)
                except Exception:
                    pass
        else:
            for q in list(self._sse_clients):
                try:
                    q.put_nowait(event)
                except Exception:
                    pass

    async def handle_index(self, request: web.Request) -> web.Response:
        """Serves the main single-page visualizer dashboard."""
        if not HTML_TEMPLATE_PATH.exists():
            return web.Response(text="Dashboard template not found.", status=404)
        with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        return web.Response(text=content, content_type="text/html")

    async def handle_history(self, request: web.Request) -> web.Response:
        """Returns JSON array of past events for state reconstruction on page load."""
        history = [e.model_dump() for e in GLOBAL_EVENT_BUS.get_history()]
        return web.json_response(history)

    async def handle_artifact(self, request: web.Request) -> web.Response:
        """Serves synthesized code or MITRE verification output files."""
        filepath_str = request.query.get("path")
        if not filepath_str:
            return web.Response(text="Missing 'path' parameter", status=400)

        path = Path(filepath_str).resolve()
        if not path.exists():
            return web.Response(text=f"Artifact not found: {path}", status=404)

        # Content-type detection
        content_type = "text/plain"
        if path.suffix == ".xhtml" or path.suffix == ".html":
            content_type = "application/xhtml+xml"
        elif path.suffix == ".svg":
            content_type = "image/svg+xml"
        elif path.suffix == ".json":
            content_type = "application/json"
        elif path.suffix == ".scm":
            content_type = "text/plain"

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            body = f.read()

        return web.Response(text=body, content_type=content_type)

    async def handle_sse(self, request: web.Request) -> web.StreamResponse:
        """Streams live Server-Sent Events to dashboard clients."""
        response = web.StreamResponse(
            status=200,
            reason="OK",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            },
        )
        await response.prepare(request)

        client_queue: asyncio.Queue = asyncio.Queue()
        self._sse_clients.add(client_queue)

        # Initial ping
        await response.write(b": ping\n\n")

        try:
            while True:
                try:
                    event: PipelineEvent = await asyncio.wait_for(client_queue.get(), timeout=15.0)
                    sse_msg = event.to_sse_message().encode("utf-8")
                    await response.write(sse_msg)
                except asyncio.TimeoutError:
                    # Keep-alive heartbeat
                    await response.write(b": heartbeat\n\n")
        except (asyncio.CancelledError, ConnectionResetError):
            pass
        finally:
            self._sse_clients.discard(client_queue)

        return response


def run_visualizer_in_background(host: str = "127.0.0.1", port: int = 8080):
    """Starts the visualizer server in a background daemon thread."""
    import threading
    import socket
    import time

    def _is_port_available(p: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, p)) != 0

    actual_port = port
    while not _is_port_available(actual_port) and actual_port < port + 20:
        actual_port += 1

    server = VisualizerServer(host=host, port=actual_port)
    server.port = actual_port

    def _target():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server.loop = loop
        runner = web.AppRunner(server.app)
        loop.run_until_complete(runner.setup())
        site = web.TCPSite(runner, host, actual_port)
        loop.run_until_complete(site.start())
        logger.info("Visualizer server active at http://%s:%d", host, actual_port)
        loop.run_forever()

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    time.sleep(0.15)
    return server
```

---

### `src/visualizer/static/index.html`

*sha256:`57cd7359c23f` · 625 lines · 20.0 KB · lang:`html`*

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RFC-LLM Pipeline Monitor</title>
  <style>
    :root {
      --bg-base: #0d1117;
      --bg-surface: #161b22;
      --bg-panel: #1b2129;
      --bg-code: #0b0e14;
      --border-color: #30363d;
      --border-focus: #58a6ff;
      --text-main: #e6edf3;
      --text-muted: #8b949e;
      --color-blue: #58a6ff;
      --color-green: #3fb950;
      --color-yellow: #d29922;
      --color-red: #f85149;
      --color-purple: #bc8cff;
      --mono: "JetBrains Mono", Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg-base);
      color: var(--text-main);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      font-size: 13px;
    }

    /* Top Utility Bar */
    header {
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      padding: 8px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .header-title {
      font-weight: 700;
      font-size: 14px;
      letter-spacing: -0.01em;
    }
    .header-right {
      display: flex;
      align-items: center;
      gap: 16px;
      font-family: var(--mono);
      font-size: 12px;
    }
    .status-badge {
      display: inline-block;
      padding: 2px 8px;
      font-weight: 700;
      font-size: 11px;
      border: 1px solid var(--border-color);
      text-transform: uppercase;
    }
    .status-badge.idle { background: #21262d; color: var(--text-muted); }
    .status-badge.running { background: #0c2d6b; color: #58a6ff; border-color: #1f6feb; }
    .status-badge.success { background: #0e4429; color: #3fb950; border-color: #238636; }
    .status-badge.failed { background: #490202; color: #f85149; border-color: #da3633; }

    /* Pipeline Stages Strip */
    .stepper {
      display: flex;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      flex-shrink: 0;
    }
    .step-item {
      flex: 1;
      padding: 8px 12px;
      border-right: 1px solid var(--border-color);
      background: var(--bg-surface);
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .step-item:last-child {
      border-right: none;
    }
    .step-item.active {
      background: #111a2c;
      border-bottom: 2px solid var(--color-blue);
    }
    .step-item.passed {
      border-bottom: 2px solid var(--color-green);
    }
    .step-item.failed {
      background: #231215;
      border-bottom: 2px solid var(--color-red);
    }
    .step-header {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-family: var(--mono);
      color: var(--text-muted);
    }
    .step-name {
      font-weight: 600;
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .step-status {
      font-size: 11px;
      color: var(--text-muted);
      font-family: var(--mono);
    }

    /* Main Grid */
    .main-grid {
      display: flex;
      flex: 1;
      overflow: hidden;
    }

    /* Left: Live Terminal & Diagnostics */
    .log-panel {
      width: 44%;
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      background: var(--bg-panel);
    }
    .panel-heading {
      padding: 6px 12px;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      font-size: 11px;
      font-weight: 700;
      font-family: var(--mono);
      text-transform: uppercase;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .log-feed {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-family: var(--mono);
      font-size: 11px;
    }
    .log-entry {
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      padding: 6px 8px;
      line-height: 1.45;
    }
    .log-entry.repair {
      border-left: 3px solid var(--color-yellow);
    }
    .log-entry.cycle {
      border-left: 3px solid var(--color-purple);
    }
    .log-entry.error {
      border-left: 3px solid var(--color-red);
    }
    .log-entry.success {
      border-left: 3px solid var(--color-green);
    }
    .log-meta {
      display: flex;
      justify-content: space-between;
      color: var(--text-muted);
      font-size: 10px;
      margin-bottom: 4px;
    }
    .log-type {
      font-weight: 700;
      color: var(--color-blue);
    }
    .log-data {
      white-space: pre-wrap;
      word-break: break-all;
      color: #c9d1d9;
    }

    /* Right: Code & Model Inspection */
    .viewer-panel {
      width: 56%;
      display: flex;
      flex-direction: column;
      background: var(--bg-code);
    }
    .tab-strip {
      display: flex;
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
    }
    .tab {
      padding: 8px 14px;
      background: transparent;
      border: none;
      border-right: 1px solid var(--border-color);
      color: var(--text-muted);
      font-family: var(--mono);
      font-size: 11px;
      cursor: pointer;
      font-weight: 600;
    }
    .tab.active {
      color: var(--text-main);
      background: var(--bg-code);
      border-top: 2px solid var(--color-blue);
      margin-top: -1px;
    }
    .tab-viewport {
      flex: 1;
      overflow: auto;
      padding: 12px;
      position: relative;
    }
    pre code {
      font-family: var(--mono);
      font-size: 12px;
      line-height: 1.55;
      color: #e6edf3;
      white-space: pre;
    }
    .svg-frame {
      width: 100%;
      height: 100%;
      border: none;
      background: #ffffff;
    }

    /* RAG Tab Styles */
    .rag-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 10px 12px;
      margin-bottom: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .rag-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: var(--text-muted);
    }
    .rag-purpose {
      font-weight: 700;
      color: var(--color-purple);
      text-transform: uppercase;
      font-family: var(--mono);
      font-size: 10px;
      border: 1px solid var(--border-color);
      padding: 1px 6px;
      background: var(--bg-base);
    }
    .rag-query-box {
      background: var(--bg-code);
      border: 1px solid var(--border-color);
      padding: 8px 10px;
      font-family: var(--mono);
      font-size: 11px;
      color: var(--color-blue);
      line-height: 1.45;
      word-break: break-all;
    }
    .rag-chunks-container {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-top: 4px;
    }
    .rag-chunk-card {
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      padding: 8px 10px;
      font-size: 11px;
    }
    .rag-chunk-meta {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 4px;
      font-family: var(--mono);
      font-size: 10px;
    }
    .rag-chunk-id {
      background: #1f6feb22;
      color: var(--color-blue);
      border: 1px solid #1f6feb66;
      padding: 1px 5px;
      font-weight: 700;
    }
    .rag-chunk-source {
      color: var(--text-muted);
    }
    .rag-chunk-title {
      font-weight: 600;
      color: var(--text-main);
      margin-bottom: 4px;
    }
    .rag-chunk-snippet {
      font-family: var(--mono);
      font-size: 11px;
      color: #8b949e;
      background: #06090e;
      padding: 6px 8px;
      border: 1px solid #21262d;
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.4;
    }
  </style>
</head>
<body>

  <!-- Top Utility Bar -->
  <header>
    <div class="header-left">
      <span class="header-title">RFC-LLM Pipeline Monitor</span>
    </div>
    <div class="header-right">
      <div>RFC: <span id="rfc-name" style="color:var(--text-main); font-weight:700;">Waiting...</span></div>
      <div id="pipeline-status" class="status-badge idle">IDLE</div>
    </div>
  </header>

  <!-- Horizontal Pipeline Stepper -->
  <div class="stepper">
    <div class="step-item" id="step-1">
      <div class="step-header"><span>01</span><span id="step-1-time">--:--</span></div>
      <div class="step-name">Document Intake</div>
      <div class="step-status" id="step-1-status">Pending</div>
    </div>
    <div class="step-item" id="step-2">
      <div class="step-header"><span>02</span><span id="step-2-time">--:--</span></div>
      <div class="step-name">AST Extraction</div>
      <div class="step-status" id="step-2-status">Pending</div>
    </div>
    <div class="step-item" id="step-3">
      <div class="step-header"><span>03</span><span id="step-3-time">--:--</span></div>
      <div class="step-name">Scheme Emission</div>
      <div class="step-status" id="step-3-status">Pending</div>
    </div>
    <div class="step-item" id="step-4">
      <div class="step-header"><span>04</span><span id="step-4-time">--:--</span></div>
      <div class="step-name">Roletran Gate</div>
      <div class="step-status" id="step-4-status">Pending</div>
    </div>
    <div class="step-item" id="step-5">
      <div class="step-header"><span>05</span><span id="step-5-time">--:--</span></div>
      <div class="step-name">Self-Healing Loop</div>
      <div class="step-status" id="step-5-status">Pending</div>
    </div>
    <div class="step-item" id="step-6">
      <div class="step-header"><span>06</span><span id="step-6-time">--:--</span></div>
      <div class="step-name">MITRE Solver</div>
      <div class="step-status" id="step-6-status">Pending</div>
    </div>
  </div>

  <!-- Main View -->
  <div class="main-grid">
    <!-- Left: Event Stream -->
    <div class="log-panel">
      <div class="panel-heading">
        <span>Execution Diagnostics</span>
        <span id="event-counter" style="color:var(--text-muted); font-size:10px;">0 Events</span>
      </div>
      <div class="log-feed" id="log-feed"></div>
    </div>

    <!-- Right: Code and Proof Inspection -->
    <div class="viewer-panel">
      <div class="tab-strip">
        <button class="tab active" onclick="switchTab('scm')">CPSA Scheme (.scm)</button>
        <button class="tab" onclick="switchTab('ast')">Pydantic AST (JSON)</button>
        <button class="tab" onclick="switchTab('slice')">RFC Sliced Text</button>
        <button class="tab" id="tab-btn-rag" onclick="switchTab('rag')">RAG Knowledge</button>
        <button class="tab" onclick="switchTab('graph')">Verified Shapes (SVG)</button>
      </div>

      <div class="tab-viewport" id="tab-scm">
        <pre><code id="code-scm">; CPSA Scheme model output will appear here...</code></pre>
      </div>
      <div class="tab-viewport" id="tab-ast" style="display:none;">
        <pre><code id="code-ast">// Pydantic JSON AST will appear here...</code></pre>
      </div>
      <div class="tab-viewport" id="tab-slice" style="display:none;">
        <pre><code id="code-slice">Verbatim RFC section slice will appear here...</code></pre>
      </div>
      <div class="tab-viewport" id="tab-rag" style="display:none; padding:12px; overflow-y:auto;">
        <div id="rag-feed" style="display:flex; flex-direction:column; gap:10px;">
          <div style="color:var(--text-muted); font-family:var(--mono); font-size:11px;">
            RAG queries and retrieved manual chunks will stream here in real time...
          </div>
        </div>
      </div>
      <div class="tab-viewport" id="tab-graph" style="display:none; padding:0; height:100%;">
        <div id="graph-container" style="height:100%; display:flex; align-items:center; justify-content:center; color:var(--text-muted); font-family:var(--mono); font-size:11px;">
          MITRE CPSA shapes graph will render here upon successful verification.
        </div>
      </div>
    </div>
  </div>

  <script>
    let activeTabId = 'scm';
    const seenEventKeys = new Set();
    let eventCount = 0;

    function switchTab(tabId) {
      activeTabId = tabId;
      document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-viewport').forEach(v => v.style.display = 'none');

      const targetBtn = Array.from(document.querySelectorAll('.tab')).find(b => b.getAttribute('onclick').includes(tabId));
      if (targetBtn) targetBtn.classList.add('active');

      const targetView = document.getElementById(`tab-${tabId}`);
      if (targetView) targetView.style.display = (tabId === 'graph') ? 'block' : 'block';
    }

    function setStepState(stageNum, state, label) {
      const step = document.getElementById(`step-${stageNum}`);
      if (!step) return;
      step.classList.remove('active', 'passed', 'failed');
      if (state === 'active') step.classList.add('active');
      else if (state === 'passed') step.classList.add('passed');
      else if (state === 'failed') step.classList.add('failed');

      if (label) {
        const statEl = document.getElementById(`step-${stageNum}-status`);
        if (statEl) statEl.innerText = label;
      }
    }

    function processEvent(evt) {
      const key = `${evt.timestamp}_${evt.event_type}_${evt.stage || 0}`;
      if (seenEventKeys.has(key)) return;
      seenEventKeys.add(key);

      eventCount++;
      document.getElementById('event-counter').innerText = `${eventCount} Events`;

      const feed = document.getElementById('log-feed');
      const item = document.createElement('div');
      item.className = 'log-entry';

      const timeStr = new Date(evt.timestamp * 1000).toLocaleTimeString([], { hour12: false });
      let typeLabel = evt.event_type;
      let bodyText = JSON.stringify(evt.data, null, 2);

      if (evt.event_type === 'pipeline_started') {
        typeLabel = 'PIPELINE_INIT';
        document.getElementById('rfc-name').innerText = evt.data.rfc_file || evt.data.rfc_id;
        const pill = document.getElementById('pipeline-status');
        pill.className = 'status-badge running';
        pill.innerText = 'RUNNING';
        setStepState(1, 'active', 'Started');
      } else if (evt.event_type === 'stage_started') {
        typeLabel = `STAGE_${evt.stage}_START`;
        setStepState(evt.stage, 'active', 'Processing');
        const timeEl = document.getElementById(`step-${evt.stage}-time`);
        if (timeEl) timeEl.innerText = timeStr;
      } else if (evt.event_type === 'stage_completed') {
        typeLabel = `STAGE_${evt.stage}_OK`;
        setStepState(evt.stage, 'passed', 'Passed');
        if (evt.data && evt.data.ast) {
          document.getElementById('code-ast').innerText = JSON.stringify(evt.data.ast, null, 2);
        }
        if (evt.data && evt.data.scm_path) {
          fetch(`/api/artifact?path=${encodeURIComponent(evt.data.scm_path)}`)
            .then(r => r.text())
            .then(txt => { document.getElementById('code-scm').innerText = txt; })
            .catch(() => {});
        }
      } else if (evt.event_type === 'slice_ready') {
        typeLabel = 'SLICE_EXTRACTED';
        bodyText = `Sections: ${JSON.stringify(evt.data.sections)}\nLine count: ${evt.data.line_count}`;
        if (evt.data && evt.data.slice_path) {
          fetch(`/api/artifact?path=${encodeURIComponent(evt.data.slice_path)}`)
            .then(r => r.text())
            .then(txt => { document.getElementById('code-slice').innerText = txt; })
            .catch(() => {});
        }
      } else if (evt.event_type === 'rag_retrieval') {
        typeLabel = 'RAG_GROUNDING';
        const chkCount = (evt.data && evt.data.chunks) ? evt.data.chunks.length : 0;
        bodyText = `Purpose: ${evt.data.purpose || 'RAG Retrieval'}\nQuery: ${evt.data.query || ''}\nRetrieved: ${chkCount} chunks`;
        renderRagEvent(evt);
      } else if (evt.event_type === 'repair_attempt') {
        item.classList.add('repair');
        if (evt.data.cycle_detected) item.classList.add('cycle');
        typeLabel = `REPAIR_${evt.data.attempt}_OF_${evt.data.max_attempts}`;
        bodyText = `Diagnostic: ${evt.data.diagnostic}\nCycle Detected: ${evt.data.cycle_detected ? 'YES (Perturbation active)' : 'NO'}`;
        setStepState(5, 'active', `Attempt ${evt.data.attempt}/50`);
      } else if (evt.event_type === 'stage_failed') {
        item.classList.add('error');
        typeLabel = `STAGE_${evt.stage}_FAIL`;
        setStepState(evt.stage, 'failed', 'Failed');
      } else if (evt.event_type === 'pipeline_completed') {
        item.classList.add('success');
        typeLabel = 'SYNTHESIS_VERIFIED';
        const pill = document.getElementById('pipeline-status');
        pill.className = 'status-badge success';
        pill.innerText = 'VERIFIED';
        setStepState(6, 'passed', `Shapes: ${evt.data.shapes_count}`);
        if (evt.data.shapes_xhtml) {
          const container = document.getElementById('graph-container');
          container.innerHTML = `<iframe class="svg-frame" src="/api/artifact?path=${encodeURIComponent(evt.data.shapes_xhtml)}"></iframe>`;
        }
      } else if (evt.event_type === 'pipeline_failed') {
        item.classList.add('error');
        typeLabel = 'PIPELINE_HALTED';
        const pill = document.getElementById('pipeline-status');
        pill.className = 'status-badge failed';
        pill.innerText = 'FAILED';
      }

      item.innerHTML = `
        <div class="log-meta">
          <span class="log-type">${typeLabel}</span>
          <span>${timeStr}</span>
        </div>
        <div class="log-data">${bodyText}</div>
      `;

      feed.appendChild(item);
      feed.scrollTop = feed.scrollHeight;
    }

    let ragFirstEvent = true;
    function renderRagEvent(evt) {
      const feed = document.getElementById('rag-feed');
      if (!feed) return;
      if (ragFirstEvent) {
        feed.innerHTML = '';
        ragFirstEvent = false;
      }

      const card = document.createElement('div');
      card.className = 'rag-card';

      const timeStr = new Date(evt.timestamp * 1000).toLocaleTimeString([], { hour12: false });
      const purpose = (evt.data && evt.data.purpose) || 'RAG Retrieval';
      const query = (evt.data && evt.data.query) || '';
      const chunks = (evt.data && evt.data.chunks) || [];

      let chunksHtml = '';
      chunks.forEach((chk) => {
        chunksHtml += `
          <div class="rag-chunk-card">
            <div class="rag-chunk-meta">
              <span class="rag-chunk-id">Chunk #${chk.chunk_id}</span>
              <span class="rag-chunk-source">${chk.source_file || 'Manual'}</span>
            </div>
            <div class="rag-chunk-title">${chk.title || ''}</div>
            <div class="rag-chunk-snippet">${chk.snippet || ''}</div>
          </div>
        `;
      });

      card.innerHTML = `
        <div class="rag-card-header">
          <span class="rag-purpose">${purpose}</span>
          <span>${timeStr}</span>
        </div>
        <div class="rag-query-box"><strong>Query:</strong> ${query}</div>
        <div class="rag-chunks-container">
          <div style="font-size:10px; color:var(--text-muted); font-family:var(--mono);">Retrieved Grounding Chunks (${chunks.length}):</div>
          ${chunksHtml}
        </div>
      `;

      feed.prepend(card);
    }

    // 1. Initial history fetch
    function syncHistory() {
      fetch('/api/history')
        .then(r => r.json())
        .then(events => {
          if (Array.isArray(events)) {
            events.forEach(processEvent);
          }
        })
        .catch(err => console.error('History sync error:', err));
    }

    syncHistory();

    // 2. Real-time SSE Connection
    const sse = new EventSource('/api/events');
    sse.onmessage = function(e) {
      try {
        const evt = JSON.parse(e.data);
        processEvent(evt);
      } catch (err) {}
    };

    // 3. Fallback sync polling every 1500ms
    setInterval(syncHistory, 1500);
  </script>
</body>
</html>
```

---
