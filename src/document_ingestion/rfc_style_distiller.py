"""Lossless RFC-Style Protocol Slice Distiller & Shared-Stem Companion Cache.

Produces `<stem>__rfc_style.txt` paired side-by-side with `<stem>__verbatim.txt`
and `<stem>__debloated.txt` inside per-protocol directories:
`refrences/global_standards/paired_slices/<stem>/` and `<run>/<stem>/<stem>_slices/`,
linked by `Verbatim-SHA256` for $0.00 cross-run cache hits.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
import litellm

from src.document_ingestion.programmatic_debloater import debloat_protocol_slice
from src.logging_config import get_pipeline_logger
from src.prompt_loader import (
    PROMPT_RFC_STYLE_DISTILLER,
    load_prompt_spec,
)
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("rfc_style_distiller")

PAIRED_INDEX_HEADER = [
    "stem",
    "doc_id",
    "protocol_title",
    "source_file",
    "verbatim_file",
    "debloated_file",
    "rfc_style_file",
    "verbatim_sha256",
    "raw_chars",
    "debloated_chars",
    "rfc_style_chars",
    "distiller_model",
    "updated_at_utc",
]

_HEADER_DIVIDER = "=" * 72


def get_paired_slices_dir(paired_dir: Optional[Path] = None) -> Path:
    target = paired_dir or (SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "global_standards" / "paired_slices")
    target.mkdir(parents=True, exist_ok=True)
    return target


def sanitize_paired_stem(raw_stem: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "_", (raw_stem or "protocol").strip()).strip("_.")
    return (cleaned[:96] or "protocol").lower()


def compute_text_sha256(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _parse_cached_sha256(cached_text: str) -> Optional[str]:
    for line in cached_text.splitlines()[:20]:
        if line.startswith("Verbatim-SHA256:"):
            return line.split(":", 1)[1].strip().lower()
    return None


def _strip_distiller_preamble(raw_response: str) -> str:
    text = (raw_response or "").strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:text|txt|markdown|md|rfc)?\s*\n?", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\n?```\s*$", "", text).strip()
    return text


def _upsert_paired_index(index_path: Path, entry: Dict[str, str]) -> None:
    rows = []
    if index_path.exists() and index_path.stat().st_size > 0:
        try:
            with open(index_path, "r", encoding="utf-8", errors="ignore", newline="") as f:
                rows = [r for r in csv.DictReader(f) if r.get("stem")]
        except Exception:
            rows = []

    updated = False
    for idx, row in enumerate(rows):
        if row.get("stem") == entry["stem"]:
            rows[idx] = entry
            updated = True
            break
    if not updated:
        rows.append(entry)

    tmp = index_path.with_suffix(".csv.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=PAIRED_INDEX_HEADER, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(index_path)


def synthesize_or_load_rfc_style_slice(
    stem: str,
    doc_id: str,
    protocol_name: str,
    verbatim_slice: str,
    debloated_slice: Optional[str] = None,
    source_file: Optional[Path] = None,
    selected_sections: Optional[list] = None,
    run_output_dir: Optional[Path] = None,
    paired_dir: Optional[Path] = None,
    model: Optional[str] = None,
    refresh: bool = False,
) -> Tuple[str, Dict[str, object]]:
    """Generates or loads cached `<stem>__rfc_style.txt` paired with `<stem>__verbatim.txt`.

    Returns `(rfc_style_text, metadata_dict)` where `metadata_dict["cache_hit"]` is True
    when the cached companion in `paired_slices/` matched `Verbatim-SHA256` at $0.00 cost.
    """
    canon_stem = sanitize_paired_stem(stem)
    cache_dir = get_paired_slices_dir(paired_dir)
    proto_cache_dir = cache_dir / canon_stem
    proto_cache_dir.mkdir(parents=True, exist_ok=True)
    verbatim_sha = compute_text_sha256(verbatim_slice)

    if debloated_slice is None:
        is_non_rfc = not re.match(r"^rfc\s*\d+$", (doc_id or "").strip(), re.IGNORECASE)
        debloated_slice, debloat_stats = debloat_protocol_slice(verbatim_slice, is_non_rfc=is_non_rfc)
    else:
        debloat_stats = {
            "raw_chars": len(verbatim_slice),
            "debloated_chars": len(debloated_slice),
            "saved_chars": max(0, len(verbatim_slice) - len(debloated_slice)),
        }

    cache_verbatim_path = proto_cache_dir / f"{canon_stem}__verbatim.txt"
    cache_debloated_path = proto_cache_dir / f"{canon_stem}__debloated.txt"
    cache_rfc_style_path = proto_cache_dir / f"{canon_stem}__rfc_style.txt"

    # Auto-migrate legacy flat paired_slices/<stem>__*.txt into paired_slices/<stem>/
    for suffix, dest_path in (
        ("verbatim", cache_verbatim_path),
        ("debloated", cache_debloated_path),
        ("rfc_style", cache_rfc_style_path),
    ):
        legacy_flat = cache_dir / f"{canon_stem}__{suffix}.txt"
        if legacy_flat.exists() and not dest_path.exists():
            legacy_flat.replace(dest_path)

    prompt_spec = load_prompt_spec(PROMPT_RFC_STYLE_DISTILLER)
    model_name = (model or "").strip() or prompt_spec.model

    cache_hit = False
    rfc_style_text = ""

    if not refresh and cache_rfc_style_path.exists():
        existing = cache_rfc_style_path.read_text(encoding="utf-8", errors="ignore")
        cached_sha = _parse_cached_sha256(existing)
        if cached_sha == verbatim_sha and existing.strip():
            rfc_style_text = existing
            cache_hit = True
            logger.info(
                "RFC-Style Cache HIT ($0.00): %s/%s (sha256=%s...)",
                canon_stem,
                cache_rfc_style_path.name,
                verbatim_sha[:12],
            )

    if not cache_hit:
        logger.info(
            "Synthesizing RFC-style slice for %s ('%s') via %s (input %d -> %d debloated chars)",
            doc_id,
            protocol_name,
            model_name,
            len(verbatim_slice),
            len(debloated_slice),
        )
        sections_str = ", ".join(selected_sections or []) or "all"
        user_prompt = (
            f"Document ID: {doc_id}\n"
            f"Protocol Name: {protocol_name}\n"
            f"Source Sections: {sections_str}\n\n"
            "Convert the following $0-debloated verbatim specification slice into the clean RFC-Style "
            "cryptographic specification format without altering any field names, cryptographic formulas, "
            "or omitted checks:\n\n"
            f"{debloated_slice}"
        )
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            model_name,
            temperature=prompt_spec.temperature if prompt_spec.temperature is not None else 0.0,
            max_tokens=prompt_spec.max_tokens,
            json_mode=False,
        )
        response = litellm.completion(
            **llm_kwargs,
            messages=[
                {"role": "system", "content": prompt_spec.body},
                {"role": "user", "content": user_prompt},
            ],
            timeout=prompt_spec.timeout,
        )
        from src.cost_tracker import GLOBAL_COST_TRACKER
        GLOBAL_COST_TRACKER.record_llm_call(response, role="distiller", model_name=model_name, stage=1)

        body = _strip_distiller_preamble(response.choices[0].message.content or "")
        if not body:
            body = debloated_slice

        try:
            portable_src = str(source_file.resolve().relative_to(SYSTEM_CONFIG.PROJECT_ROOT.resolve())) if source_file else ""
        except Exception:
            portable_src = str(source_file or "")

        provenance_header = "\n".join([
            f"Document-ID: {doc_id}",
            f"Protocol-Title: {protocol_name}",
            f"Source-File: {portable_src}",
            f"Verbatim-Companion: {canon_stem}__verbatim.txt",
            f"Debloated-Companion: {canon_stem}__debloated.txt",
            f"Verbatim-SHA256: {verbatim_sha}",
            f"Source-Sections: {sections_str}",
            f"Distiller-Model: {model_name}",
            _HEADER_DIVIDER,
            "",
        ])
        rfc_style_text = provenance_header + body.rstrip() + "\n"

        # Persist paired companions inside per-protocol cache directory
        cache_verbatim_path.write_text(verbatim_slice, encoding="utf-8")
        cache_debloated_path.write_text(debloated_slice, encoding="utf-8")
        cache_rfc_style_path.write_text(rfc_style_text, encoding="utf-8")

        _upsert_paired_index(
            cache_dir / "PAIRED_INDEX.csv",
            {
                "stem": canon_stem,
                "doc_id": doc_id,
                "protocol_title": protocol_name,
                "source_file": portable_src,
                "verbatim_file": f"{canon_stem}/{cache_verbatim_path.name}",
                "debloated_file": f"{canon_stem}/{cache_debloated_path.name}",
                "rfc_style_file": f"{canon_stem}/{cache_rfc_style_path.name}",
                "verbatim_sha256": verbatim_sha,
                "raw_chars": str(len(verbatim_slice)),
                "debloated_chars": str(len(debloated_slice)),
                "rfc_style_chars": str(len(rfc_style_text)),
                "distiller_model": model_name,
                "updated_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        )
    else:
        if not cache_verbatim_path.exists():
            cache_verbatim_path.write_text(verbatim_slice, encoding="utf-8")
        if not cache_debloated_path.exists():
            cache_debloated_path.write_text(debloated_slice, encoding="utf-8")

    run_rfc_style_path: Optional[Path] = None
    if run_output_dir is not None:
        run_slices_dir = run_output_dir / f"{canon_stem}_slices"
        run_slices_dir.mkdir(parents=True, exist_ok=True)
        (run_slices_dir / f"{canon_stem}__verbatim.txt").write_text(verbatim_slice, encoding="utf-8")
        (run_slices_dir / f"{canon_stem}__debloated.txt").write_text(debloated_slice, encoding="utf-8")
        run_rfc_style_path = run_slices_dir / f"{canon_stem}__rfc_style.txt"
        run_rfc_style_path.write_text(rfc_style_text, encoding="utf-8")

    return rfc_style_text, {
        "stem": canon_stem,
        "cache_hit": cache_hit,
        "distiller_model": model_name,
        "verbatim_sha256": verbatim_sha,
        "debloat_stats": debloat_stats,
        "cache_rfc_style_path": str(cache_rfc_style_path),
        "run_rfc_style_path": str(run_rfc_style_path) if run_rfc_style_path else None,
        "verbatim_chars": len(verbatim_slice),
        "debloated_chars": len(debloated_slice),
        "rfc_style_chars": len(rfc_style_text),
    }
