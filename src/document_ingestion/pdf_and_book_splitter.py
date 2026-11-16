"""Native PDF/DOCX/HTML/Markdown Reader and Multi-Protocol Book Splitter.

Extracts layout-preserved text and PDF bookmark hierarchies, splits multi-protocol
standards books into standalone verbatim `.txt` dossiers (across all CPU cores at
$0.00 cost by default, or opt-in `--llm-split`), and emits clean normalized
protocol `.txt` files ready for `RFC-LLM` Stage 1-6 synthesis.
"""

from __future__ import annotations

import csv
import html
import os
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import litellm
import pymupdf
from pydantic import BaseModel, Field

from src.document_ingestion.programmatic_debloater import debloat_protocol_slice
from src.document_ingestion.rfc_header_filter import (
    FRONTMATTER_CRYPTO_REGEX,
    FRONTMATTER_PROTOCOL_REGEX,
)
from src.document_ingestion.rfc_toc_parser import TOCSectionEntry, parse_table_of_contents
from src.document_ingestion.verbatim_section_slicer import slice_verbatim_sections
from src.logging_config import get_pipeline_logger
from src.prompt_loader import PROMPT_BOOK_SPLITTER, build_schema_system_prompt, load_prompt_spec, parse_llm_json
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("pdf_book_splitter")

SUPPORTED_BOOK_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown", ".html", ".htm", ".docx", ".mediawiki", ".rst"}

# Headings indicating a distinct cryptographic handshake or security procedure inside a multi-protocol book
_PROTOCOL_HEADING_KEYWORDS = (
    "authentication",
    "authenticated",
    "key agreement",
    "key establishment",
    "key exchange",
    "key management",
    "key transport",
    "key wrapping",
    "key derivation",
    "over-the-air rekeying",
    "rekey",
    "otar",
    "handshake",
    "pairing",
    "bonding",
    "provisioning",
    "commissioning",
    "onboarding",
    "session establishment",
    "session setup",
    "secure channel",
    "security mode",
    "security association",
    "registration",
    "handover",
    "bootstrapping",
    "challenge",
    "attestation",
    "enrollment",
    "certificate request",
    "ticket",
    "token exchange",
    "pase",
    "case",
    "pace",
    "chip authentication",
    "terminal authentication",
    "active authentication",
    "basic access control",
    "spake",
    "aka",
    "eap-",
    "ntor",
    "x3dh",
    "pqxdh",
    "ratchet",
    "olm",
    "megolm",
    "secret connection",
    "join procedure",
    "join-request",
    "rlpx",
    "bip-324",
    "noise_",
    "protocol flow",
    "message exchange",
    "login",
    "mutual",
)

_SUPPORTING_SECTION_KEYWORDS = (
    "key derivation",
    "kdf",
    "hkdf",
    "prf",
    "cryptographic algorithms",
    "cipher suite",
    "pdu format",
    "message format",
    "frame format",
    "security header",
    "cryptogram",
)

_EXCLUDED_SPLIT_HEADINGS = (
    "scope",
    "introduction",
    "normative references",
    "informative references",
    "references",
    "terms, definitions",
    "terms and definitions",
    "abbreviations",
    "abbreviated terms",
    "acronyms",
    "conventions",
    "foreword",
    "change history",
    "revision history",
    "document history",
    "table of contents",
    "contents",
    "list of figures",
    "list of tables",
    "bibliography",
    "acknowledgements",
    "acknowledgments",
    "annex a (informative)",
    "glossary",
    "requirements",
    "compliance",
    "conformance",
)


class LLMBookProtocolBundle(BaseModel):
    protocol_slug: str = Field(..., description="Short snake_case filename slug")
    protocol_title: str = Field(..., description="Descriptive protocol title")
    section_ids: List[str] = Field(..., description="Exact section IDs from the TOC")


class LLMBookSplitPlan(BaseModel):
    protocols: List[LLMBookProtocolBundle] = Field(default_factory=list)


class _StructuredHTMLTextExtractor(HTMLParser):
    """Converts HTML specs into structured plain text while preserving headings and <pre> ladders."""

    _BLOCK_TAGS = {"p", "div", "section", "article", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "pre", "br", "hr"}

    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._in_pre = False
        self._chunks: List[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        t = tag.lower()
        if t in {"script", "style", "nav", "footer", "svg"}:
            self._skip_depth += 1
            return
        if self._skip_depth > 0:
            return
        if t == "pre":
            self._in_pre = True
            self._chunks.append("\n")
        elif t in self._BLOCK_TAGS:
            self._chunks.append("\n")
        elif t in {"td", "th"}:
            self._chunks.append("  ")

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t in {"script", "style", "nav", "footer", "svg"} and self._skip_depth > 0:
            self._skip_depth -= 1
            return
        if self._skip_depth > 0:
            return
        if t == "pre":
            self._in_pre = False
            self._chunks.append("\n")
        elif t in {"p", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "li"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        if self._in_pre:
            self._chunks.append(data)
        else:
            collapsed = re.sub(r"[ \t\r\n]+", " ", data)
            if collapsed.strip():
                self._chunks.append(collapsed)

    def get_text(self) -> str:
        raw = html.unescape("".join(self._chunks))
        return re.sub(r"\n{3,}", "\n\n", raw).strip()


def sanitize_filename_token(text: str, max_len: int = 64) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", (text or "").strip().lower()).strip("_")
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len].rstrip("_")
    return cleaned or "protocol"


def _infer_org_and_doc_id(source_path: Path, raw_text: str) -> Tuple[str, str]:
    stem = source_path.stem
    parent = source_path.parent.name.upper()
    head = "\n".join(raw_text.splitlines()[:120])

    if re.search(r"CCSDS\s+\d+\.\d+-[A-Z]-\d+", head, re.I) or "ccsds" in stem.lower() or "SPACE" in parent:
        m = re.search(r"(CCSDS\s+\d+\.\d+-[A-Z]-\d+)", head, re.I)
        return "CCSDS", (m.group(1).replace(" ", "_") if m else stem)
    if re.search(r"3GPP\s+TS\s+\d+\.\d+|ETSI\s+TS\s+1\d{2}\s+\d+", head, re.I) or "3gpp" in str(source_path).lower() or "etsi" in str(source_path).lower():
        m = re.search(r"(?:3GPP\s+TS|ETSI\s+(?:TS|EN|GS))\s+[\d.\s]+", head, re.I)
        org = "ETSI" if "etsi" in str(source_path).lower() and "3gpp" not in head.lower() else "3GPP"
        return org, (m.group(0).strip().replace(" ", "_") if m else stem)
    if re.search(r"\[MS-[A-Z0-9]+\]|Microsoft Corporation", head, re.I) or stem.lower().startswith("ms-") or "[ms-" in stem.lower():
        m = re.search(r"(MS-[A-Z0-9]+)", head + " " + stem, re.I)
        return "MICROSOFT", (m.group(1).upper() if m else stem)
    if re.search(r"\bNIST\s+(?:SP|FIPS)\s+[\w.-]+", head, re.I) or "nist" in str(source_path).lower():
        m = re.search(r"((?:NIST\s+)?(?:SP|FIPS)\s+[\w.-]+)", head, re.I)
        return "NIST", (m.group(1).replace(" ", "_") if m else stem)
    if re.search(r"\bDSP\d{4}\b|\bSPDM\b", head, re.I) or "dsp0" in stem.lower():
        m = re.search(r"(DSP\d{4})", head + " " + stem, re.I)
        return "DMTF", (m.group(1).upper() if m else stem)
    if re.search(r"\bBSI\s+TR-\d+|\bICAO\s+Doc\s+9303\b", head, re.I):
        return "GOV_ID", stem
    if "ietf" in str(source_path).lower() or stem.lower().startswith("draft-"):
        return "IETF_DRAFT", stem
    return (parent if parent and parent not in {"RAW_SPECS", "TMP"} else "STD"), stem


def extract_text_and_bookmarks_from_pdf(pdf_path: Path) -> Tuple[str, List[Tuple[int, str, int]]]:
    """Extracts layout-preserved text (`pdftotext -layout`, fallback `pymupdf`) and PDF outline bookmarks."""
    bookmarks: List[Tuple[int, str, int]] = []
    doc_title_meta = ""
    try:
        with pymupdf.open(str(pdf_path)) as doc:
            doc_title_meta = (doc.metadata or {}).get("title") or ""
            raw_toc = doc.get_toc() or []
            for item in raw_toc:
                if len(item) >= 3:
                    bookmarks.append((int(item[0]), str(item[1]).strip(), int(item[2])))
    except Exception as exc:
        logger.debug("pymupdf outline inspection skipped for %s: %s", pdf_path.name, exc)

    extracted_text = ""
    pdftotext_bin = shutil.which("pdftotext")
    if pdftotext_bin:
        try:
            proc = subprocess.run(
                [pdftotext_bin, "-layout", "-enc", "UTF-8", str(pdf_path), "-"],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                extracted_text = proc.stdout
        except Exception as exc:
            logger.debug("pdftotext failed on %s (%s); falling back to pymupdf", pdf_path.name, exc)

    if not extracted_text.strip():
        pages_txt: List[str] = []
        with pymupdf.open(str(pdf_path)) as doc:
            for page in doc:
                pages_txt.append(page.get_text("text"))
        extracted_text = "\n\f\n".join(pages_txt)

    if doc_title_meta and doc_title_meta.strip() and doc_title_meta.strip().lower() not in extracted_text[:800].lower():
        extracted_text = f"{doc_title_meta.strip()}\n\n{extracted_text}"

    return extracted_text, bookmarks


def extract_text_from_docx(docx_path: Path) -> str:
    """Extracts structured plain text (headings, paragraphs, tables) from a `.docx` archive using stdlib."""
    ns_w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    lines: List[str] = []
    with zipfile.ZipFile(docx_path, "r") as zf:
        if "word/document.xml" not in zf.namelist():
            return ""
        xml_bytes = zf.read("word/document.xml")
    root = ET.fromstring(xml_bytes)
    body = root.find(f"{ns_w}body")
    if body is None:
        return ""
    for child in body:
        tag = child.tag
        if tag == f"{ns_w}p":
            txt = "".join(t.text or "" for t in child.iter(f"{ns_w}t")).strip()
            if txt:
                lines.append(txt)
        elif tag == f"{ns_w}tbl":
            for tr in child.findall(f".//{ns_w}tr"):
                cells = []
                for tc in tr.findall(f".//{ns_w}tc"):
                    cell_txt = " ".join("".join(t.text or "" for t in p.iter(f"{ns_w}t")).strip() for p in tc.findall(f".//{ns_w}p"))
                    if cell_txt.strip():
                        cells.append(cell_txt.strip())
                if cells:
                    lines.append(" | ".join(cells))
            lines.append("")
    return "\n".join(lines)


def extract_text_from_any_document(doc_path: Path) -> Tuple[str, List[Tuple[int, str, int]]]:
    """Reads `.pdf`, `.docx`, `.html`, `.md`, or `.txt` into plain UTF-8 text + optional outline bookmarks."""
    suffix = doc_path.suffix.lower()
    if suffix == ".pdf":
        return extract_text_and_bookmarks_from_pdf(doc_path)
    if suffix == ".docx":
        return extract_text_from_docx(doc_path), []
    raw = doc_path.read_text(encoding="utf-8", errors="ignore")
    if suffix in {".html", ".htm"}:
        parser = _StructuredHTMLTextExtractor()
        parser.feed(raw)
        return parser.get_text(), []
    if suffix in {".md", ".markdown", ".mediawiki", ".rst"}:
        # Convert Markdown headings (`## 3.2 Handshake`) cleanly to column-0 numbered/titled lines when numbered
        converted_lines = []
        for line in raw.splitlines():
            m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
            if m:
                converted_lines.append(m.group(2).strip())
            else:
                converted_lines.append(line)
        return "\n".join(converted_lines), []
    return raw, []


def _bookmarks_to_toc_entries(bookmarks: List[Tuple[int, str, int]]) -> List[TOCSectionEntry]:
    entries: List[TOCSectionEntry] = []
    for level, title, page in bookmarks:
        m = re.match(
            r"^\s*(?:Section\s+|Clause\s+)?((?:\d+(?:\.\d+)*)|(?:(?:Annex|Appendix)\s+[A-Z](?:\.\d+)*)|(?:[A-Z]\.\d+(?:\.\d+)*))(?:\.|:|\s+-)?\s+(.+)$",
            title,
            re.IGNORECASE,
        )
        if m:
            sec_id = re.sub(r"^(?:Appendix|Annex)\s+", "App-", m.group(1).strip(), flags=re.IGNORECASE).rstrip(".")
            sec_title = m.group(2).strip()
            entries.append(TOCSectionEntry(section_id=sec_id, title=sec_title, page_number=page, indent_level=max(0, level - 1)))
    return entries


def _looks_like_noise_protocol_section(text: str) -> bool:
    """Quick $0 gate verifying a split section actually has interactive cryptographic protocol terms."""
    if len(text.splitlines()) < 15 or len(text) < 500:
        return False
    return bool(FRONTMATTER_CRYPTO_REGEX.search(text) and FRONTMATTER_PROTOCOL_REGEX.search(text))


def _format_standard_dossier(
    doc_id: str,
    org: str,
    source_doc_name: str,
    proto_title: str,
    selected_sections: Sequence[str],
    abstract_excerpt: str,
    toc_lines: Sequence[str],
    body_text: str,
) -> str:
    clean_body, _ = debloat_protocol_slice(body_text, is_non_rfc=True)
    header = [
        f"Document-ID: {doc_id}",
        f"Source-Organization: {org}",
        f"Source-Document: {source_doc_name}",
        "Category: Standards Track",
        f"Protocol-Title: {proto_title}",
        f"Source-Sections: {', '.join(selected_sections) if selected_sections else 'ALL'}",
        "",
        "Abstract",
        "",
    ]
    for al in (abstract_excerpt or f"Extracted protocol specification section from {source_doc_name}.").splitlines()[:18]:
        header.append(f"   {al.strip()}" if al.strip() else "")
    header.extend(["", "Table of Contents", ""])
    for tl in toc_lines[:45]:
        header.append(f"   {tl}")
    header.extend(["", clean_body.strip(), ""])
    return "\n".join(header)


def _deterministic_split_single_doc(
    doc_path: Path,
    out_dir: Path,
    org_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Splits one PDF/DOCX/HTML/MD/TXT specification into 1 or more standalone `.txt` protocol dossiers ($0)."""
    raw_text, bookmarks = extract_text_and_bookmarks_from_pdf(doc_path) if doc_path.suffix.lower() == ".pdf" else extract_text_from_any_document(doc_path)
    if not raw_text.strip() or len(raw_text.splitlines()) < 30:
        return {"source": str(doc_path), "emitted_files": [], "skipped_reason": "empty_or_too_short"}

    org, doc_id_base = _infer_org_and_doc_id(doc_path, raw_text)
    if org_override:
        org = org_override

    lines = raw_text.splitlines()
    # Extract a compact Abstract / Scope snippet
    abstract_lines: List[str] = []
    for idx, ln in enumerate(lines[:350]):
        if re.match(r"^\s*(?:\d+(?:\.\d+)*\s+)?(?:Abstract|Scope|Executive Summary|1\.?\s+Introduction|1\.?\s+Overview)\s*$", ln, re.IGNORECASE):
            abstract_lines = [l.strip() for l in lines[idx + 1 : idx + 25] if l.strip()]
            break
    if not abstract_lines:
        abstract_lines = [l.strip() for l in lines[:20] if l.strip()][:10]
    abstract_excerpt = "\n".join(abstract_lines[:12])

    # Build combined TOC (explicit TOC or PDF bookmarks, merging missing top-level bookmarks)
    toc_entries = parse_table_of_contents(raw_text)
    bm_entries = _bookmarks_to_toc_entries(bookmarks)
    if len(bm_entries) > len(toc_entries):
        toc_entries = bm_entries
    elif bm_entries:
        existing_ids = {e.section_id for e in toc_entries}
        merged_bm = [e for e in bm_entries if e.section_id not in existing_ids]
        if merged_bm:
            toc_entries = merged_bm + toc_entries

    # Identify shared cryptographic supporting sections (KDF, algorithms, PDU formats)
    supporting_ids: List[str] = []
    for e in toc_entries:
        t_low = e.title.lower().strip()
        if any(ex in t_low for ex in _EXCLUDED_SPLIT_HEADINGS):
            continue
        if e.section_id.count(".") <= 1 and any(sk in t_low for sk in _SUPPORTING_SECTION_KEYWORDS):
            if e.section_id not in supporting_ids:
                supporting_ids.append(e.section_id)
        if len(supporting_ids) >= 2:
            break

    # Identify candidate distinct protocol procedures
    candidate_bundles: List[Tuple[str, str, List[str]]] = []
    seen_prefixes: set = set()
    for e in toc_entries:
        t_low = e.title.lower().strip()
        if any(t_low == ex or t_low.startswith(ex + " ") or t_low.startswith(ex + ":") for ex in _EXCLUDED_SPLIT_HEADINGS):
            continue
        # Avoid creating nested duplicates when parent section is already selected
        if any(e.section_id == p or e.section_id.startswith(p + ".") for p in seen_prefixes):
            continue
        if e.section_id.count(".") <= 2 and any(kw in t_low for kw in _PROTOCOL_HEADING_KEYWORDS):
            sec_bundle = [e.section_id]
            for s_id in supporting_ids:
                if s_id != e.section_id and not s_id.startswith(e.section_id + ".") and not e.section_id.startswith(s_id + "."):
                    sec_bundle.append(s_id)
            candidate_bundles.append((sanitize_filename_token(e.title, max_len=48), e.title, sec_bundle))
            seen_prefixes.add(e.section_id)

    emitted: List[Dict[str, str]] = []
    out_dir.mkdir(parents=True, exist_ok=True)
    file_prefix = f"{sanitize_filename_token(org, 18)}_{sanitize_filename_token(doc_id_base, 40)}"

    # If the document is already a focused single-protocol spec (or <= 950 lines and <= 1 bundle) -> emit 1 dossier
    if len(lines) <= 950 or len(candidate_bundles) <= 1:
        if not _looks_like_noise_protocol_section(raw_text):
            return {"source": str(doc_path), "emitted_files": [], "skipped_reason": "no_crypto_protocol_vocab"}

        proto_title = (
            candidate_bundles[0][1]
            if candidate_bundles
            else next((l.strip() for l in lines[:35] if len(l.strip()) > 6 and not re.match(r"^(?:page|ccsds|3gpp|etsi|nist|rfc)\b", l.strip(), re.I)), doc_path.stem)
        )
        proto_title = re.sub(r"\s+", " ", proto_title)[:140]
        if len(lines) <= 1800 or not candidate_bundles:
            body_text = raw_text
            sel_secs = ["ALL"]
        else:
            try:
                body_text = slice_verbatim_sections(raw_text, candidate_bundles[0][2])
                sel_secs = candidate_bundles[0][2]
            except Exception:
                body_text = "\n".join(lines[:1800])
                sel_secs = ["ALL"]

        if not _looks_like_noise_protocol_section(body_text):
            return {"source": str(doc_path), "emitted_files": [], "skipped_reason": "slice_lacks_crypto"}

        toc_lines = [f"{e.section_id}  {e.title}" for e in toc_entries] or ["1.  Specification"]
        out_name = f"{file_prefix}.txt"
        out_path = out_dir / out_name
        dossier = _format_standard_dossier(
            doc_id=f"{org}-{doc_id_base}",
            org=org,
            source_doc_name=doc_path.name,
            proto_title=proto_title,
            selected_sections=sel_secs,
            abstract_excerpt=abstract_excerpt,
            toc_lines=toc_lines,
            body_text=body_text,
        )
        out_path.write_text(dossier, encoding="utf-8")
        emitted.append({
            "filename": out_name,
            "path": str(out_path),
            "org": org,
            "doc_id": f"{org}-{doc_id_base}",
            "protocol_title": proto_title,
            "source_sections": ";".join(sel_secs),
            "chars": str(len(dossier)),
            "source_file": str(doc_path),
        })
        return {"source": str(doc_path), "emitted_files": emitted, "skipped_reason": ""}

    # Multi-protocol book mode: emit one clean .txt dossier per detected procedure (cap at 30 per single book)
    toc_map = {e.section_id: e.title for e in toc_entries}
    for idx_b, (p_slug, p_title, sec_ids) in enumerate(candidate_bundles[:30], 1):
        try:
            sliced = slice_verbatim_sections(raw_text, sec_ids)
        except Exception:
            continue
        if len(sliced.splitlines()) > 2600:
            # Guard against bloated catch-all chapters by truncating only supporting tail or keeping primary section
            try:
                sliced = slice_verbatim_sections(raw_text, [sec_ids[0]])
            except Exception:
                continue
        if not _looks_like_noise_protocol_section(sliced):
            continue

        toc_lines = [f"{sid}  {toc_map.get(sid, proto)}" for sid, proto in [(s, p_title) for s in sec_ids]]
        out_name = f"{file_prefix}__{p_slug}.txt"
        out_path = out_dir / out_name
        if out_path.exists():
            out_name = f"{file_prefix}__{idx_b:02d}_{p_slug}.txt"
            out_path = out_dir / out_name

        dossier = _format_standard_dossier(
            doc_id=f"{org}-{doc_id_base}-{p_slug[:24]}",
            org=org,
            source_doc_name=doc_path.name,
            proto_title=p_title[:140],
            selected_sections=sec_ids,
            abstract_excerpt=abstract_excerpt,
            toc_lines=toc_lines,
            body_text=sliced,
        )
        out_path.write_text(dossier, encoding="utf-8")
        emitted.append({
            "filename": out_name,
            "path": str(out_path),
            "org": org,
            "doc_id": f"{org}-{doc_id_base}-{p_slug[:24]}",
            "protocol_title": p_title[:140],
            "source_sections": ";".join(sec_ids),
            "chars": str(len(dossier)),
            "source_file": str(doc_path),
        })

    return {
        "source": str(doc_path),
        "emitted_files": emitted,
        "skipped_reason": "" if emitted else "no_crypto_sections_matched",
    }


def _llm_split_single_doc(
    doc_path: Path,
    out_dir: Path,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Optional `--llm-split` handler using `prompts/00_book_protocol_splitter.md`."""
    raw_text, bookmarks = extract_text_from_any_document(doc_path)
    toc_entries = parse_table_of_contents(raw_text) or _bookmarks_to_toc_entries(bookmarks)
    if not toc_entries:
        return _deterministic_split_single_doc(doc_path, out_dir)

    prompt_spec = load_prompt_spec(PROMPT_BOOK_SPLITTER)
    model_name = model or prompt_spec.model
    system_prompt = build_schema_system_prompt(PROMPT_BOOK_SPLITTER, LLMBookSplitPlan)
    toc_str = "\n".join(f"{e.section_id} {e.title}" for e in toc_entries[:300])
    user_prompt = f"Document: {doc_path.name}\n\nTable of Contents:\n{toc_str}"

    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=prompt_spec.temperature if prompt_spec.temperature is not None else 0.0,
            max_tokens=prompt_spec.max_tokens,
            json_mode=True,
        )
        resp = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=prompt_spec.timeout,
        )
        plan = LLMBookSplitPlan.model_validate(parse_llm_json(resp.choices[0].message.content))
    except Exception as exc:
        logger.warning("LLM book splitter failed on %s (%s); using deterministic splitter.", doc_path.name, exc)
        return _deterministic_split_single_doc(doc_path, out_dir)

    if not plan.protocols:
        return _deterministic_split_single_doc(doc_path, out_dir)

    org, doc_id_base = _infer_org_and_doc_id(doc_path, raw_text)
    file_prefix = f"{sanitize_filename_token(org, 18)}_{sanitize_filename_token(doc_id_base, 40)}"
    out_dir.mkdir(parents=True, exist_ok=True)
    toc_map = {e.section_id: e.title for e in toc_entries}
    emitted: List[Dict[str, str]] = []
    for b in plan.protocols:
        try:
            sliced = slice_verbatim_sections(raw_text, b.section_ids)
        except Exception:
            continue
        if not _looks_like_noise_protocol_section(sliced):
            continue
        p_slug = sanitize_filename_token(b.protocol_slug, max_len=48)
        out_name = f"{file_prefix}__{p_slug}.txt"
        out_path = out_dir / out_name
        dossier = _format_standard_dossier(
            doc_id=f"{org}-{doc_id_base}-{p_slug[:24]}",
            org=org,
            source_doc_name=doc_path.name,
            proto_title=b.protocol_title[:140],
            selected_sections=b.section_ids,
            abstract_excerpt=f"Extracted via LLM book splitter from {doc_path.name}.",
            toc_lines=[f"{sid}  {toc_map.get(sid, '')}" for sid in b.section_ids],
            body_text=sliced,
        )
        out_path.write_text(dossier, encoding="utf-8")
        emitted.append({
            "filename": out_name,
            "path": str(out_path),
            "org": org,
            "doc_id": f"{org}-{doc_id_base}-{p_slug[:24]}",
            "protocol_title": b.protocol_title[:140],
            "source_sections": ";".join(b.section_ids),
            "chars": str(len(dossier)),
            "source_file": str(doc_path),
        })
    return {"source": str(doc_path), "emitted_files": emitted, "skipped_reason": "" if emitted else "no_crypto_sections"}


def split_books_directory(
    targets: Sequence[Path],
    output_dir: Optional[Path] = None,
    workers: Optional[int] = None,
    use_llm: bool = False,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Converts and splits one or more files/directories into standalone `.txt` protocol files.

    Uses all available CPU cores via `ProcessPoolExecutor` in deterministic `$0.00` mode.
    """
    out_dir = output_dir or (SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "global_standards" / "protocols_txt")
    out_dir.mkdir(parents=True, exist_ok=True)

    candidate_files: List[Path] = []
    for t in targets:
        if t.is_file():
            if t.suffix.lower() in SUPPORTED_BOOK_EXTENSIONS:
                candidate_files.append(t)
        elif t.is_dir():
            for p in sorted(t.rglob("*")):
                if p.is_file() and p.suffix.lower() in SUPPORTED_BOOK_EXTENSIONS:
                    candidate_files.append(p)

    # Deduplicate resolved paths
    seen: set = set()
    unique_files: List[Path] = []
    for p in candidate_files:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            unique_files.append(p)

    all_emitted: List[Dict[str, str]] = []
    skipped: List[Tuple[str, str]] = []

    if use_llm:
        for fpath in unique_files:
            res = _llm_split_single_doc(fpath, out_dir, model=model)
            if res["emitted_files"]:
                all_emitted.extend(res["emitted_files"])
            else:
                skipped.append((str(fpath), res.get("skipped_reason", "skipped")))
    else:
        max_w = max(1, min(workers or (os.cpu_count() or 8), len(unique_files) or 1))
        if max_w == 1 or len(unique_files) <= 2:
            for fpath in unique_files:
                res = _deterministic_split_single_doc(fpath, out_dir)
                if res["emitted_files"]:
                    all_emitted.extend(res["emitted_files"])
                else:
                    skipped.append((str(fpath), res.get("skipped_reason", "skipped")))
        else:
            with ProcessPoolExecutor(max_workers=max_w) as pool:
                futs = {pool.submit(_deterministic_split_single_doc, fpath, out_dir): fpath for fpath in unique_files}
                for fut in as_completed(futs):
                    fpath = futs[fut]
                    try:
                        res = fut.result()
                        if res["emitted_files"]:
                            all_emitted.extend(res["emitted_files"])
                        else:
                            skipped.append((str(fpath), res.get("skipped_reason", "skipped")))
                    except Exception as exc:
                        skipped.append((str(fpath), f"error: {exc}"))

    # Write INDEX.csv inside out_dir
    index_csv = out_dir / "INDEX.csv"
    fieldnames = ["filename", "org", "doc_id", "protocol_title", "source_sections", "chars", "source_file", "path"]
    all_emitted.sort(key=lambda r: r["filename"])
    with open(index_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_emitted)

    return {
        "input_files_scanned": len(unique_files),
        "emitted_protocols_count": len(all_emitted),
        "skipped_count": len(skipped),
        "output_dir": str(out_dir),
        "index_csv": str(index_csv),
        "emitted_files": all_emitted,
        "skipped": skipped,
    }
