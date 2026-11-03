"""CPSA 4.4.9 Knowledge Base Indexer, `TOC.md` Flag Manager, and Agentic Searcher Client.

Replaces static vector-chunk RAG with a structured, zero-hallucination CPSA 4.4.9
Knowledge Base (`refrences/cpsa_kb/`) backed by:
1. `TOC.md` with a YAML frontmatter `rebuild_toc: true | false` flag that controls
   whether `TOC.md` and `kb_index.json` are rebuilt from disk on load (and automatically
   resets `rebuild_toc: false` after rebuilding).
2. Concept-split Markdown sections across `01_core_rules/`, `02_manuals/`, and
   `04_examples_catalog/` plus all 151 official MITRE `.scm` protocol files in
   `03_examples_scm/`.
3. In-memory DSL-aware BM25 + exact compiler-error phrase matching + optional in-process
   `FlashRank` ONNX cross-encoder reranking (zero external Ollama embedding dependency).
4. An Agentic Searcher LLM loop (`run_agentic_cpsa_searcher`) that inspects the failing
   `CPSAProtocolSpecification` AST + compiler diagnostic, invokes deterministic tools
   (`read_section`, `search_cpsa_docs`, `find_scm_examples`, `read_scm_example`), and
   returns verified manual rules, working `.scm` examples, and pinpointed AST fixes.
"""

from __future__ import annotations

from collections import Counter
import datetime as dt
import json
import math
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple
import json_repair
import litellm
import yaml

from src.logging_config import get_pipeline_logger
from src.pipeline_events import GLOBAL_EVENT_BUS
from src.prompt_loader import PROMPT_RAG_QUERY_FORMULATION, load_prompt_spec
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("rag_retriever")

CPSA_KB_DIR: Path = SYSTEM_CONFIG.PROJECT_ROOT / "refrences" / "cpsa_kb"
TOC_MD_PATH: Path = CPSA_KB_DIR / "TOC.md"
KB_INDEX_JSON_PATH: Path = CPSA_KB_DIR / "kb_index.json"

_GLOBAL_RETRIEVER: Optional["CPSAKnowledgeBase"] = None
LAST_RETRIEVED_CHUNK_IDS: List[str] = []
LAST_SEARCHER_QUERY: Optional[str] = None
LAST_SEARCHER_DIAGNOSIS: Optional[str] = None
LAST_SEARCHER_TRACE: List[Dict[str, Any]] = []
_SEARCH_CACHE: Dict[str, Tuple[str, str, List[str], Optional[str], List[Dict[str, Any]]]] = {}

_KNOWN_SORTS = {
    "name", "text", "data", "skey", "akey", "mesg", "chan", "locn",
    "rndx", "expt", "base", "tag", "dev", "strd", "indx", "fact",
}
_KNOWN_OPERATORS = {
    "enc", "hash", "cat", "pubk", "privk", "invk", "ltk", "bltk",
    "exp", "gen", "mul", "rec", "one", "send", "recv", "load", "stor",
}
_KNOWN_KEYWORDS = {
    "defprotocol", "defrole", "defskeleton", "defstrand", "defstrandmax",
    "deflistener", "defgoal", "defrule", "defgenrule", "deflemma", "defmacro",
    "herald", "vars", "trace", "inputs", "outputs", "non-orig", "pen-non-orig",
    "uniq-orig", "uniq-gen", "ugen-at", "uniq-at", "auth", "conf", "gen-st",
    "facts", "neq", "lt", "leads-to", "same-locn", "state-node", "trans",
    "ind-zero", "absent", "precur", "priority", "critical-sections", "lang",
}


def tokenize_cpsa_dsl(text: str) -> List[str]:
    """DSL-aware tokenizer preserving Scheme S-expression atoms, hyphenated keywords,
    and structural markers (e.g. defprotocol, non-orig, uniq-gen, cpsa4roletran).
    """
    text_lower = text.lower()
    tokens = re.findall(r"[a-zA-Z0-9_\-]+", text_lower)
    scheme_ops = re.findall(r"\(([a-zA-Z0-9_\-]+)", text_lower)
    tokens.extend(scheme_ops)
    return [t for t in tokens if len(t) > 1]


def _slugify_heading(heading: str) -> str:
    """Converts a Markdown heading string into a clean anchor slug."""
    cleaned = re.sub(r"[`*_~]", "", heading.strip())
    slug = re.sub(r"[^a-zA-Z0-9.\-_]+", "-", cleaned.lower()).strip("-")
    return slug[:64] or "section"


def parse_toc_rebuild_flag(toc_path: Path = TOC_MD_PATH) -> bool:
    """Reads `TOC.md` YAML frontmatter and returns True if `rebuild_toc` is True
    (or if `TOC.md` does not exist yet).
    """
    if not toc_path.exists():
        return True
    try:
        raw = toc_path.read_text(encoding="utf-8", errors="ignore")
        if not raw.startswith("---"):
            return True
        parts = raw.split("---", 2)
        if len(parts) < 3:
            return True
        meta = yaml.safe_load(parts[1])
        if not isinstance(meta, dict):
            return True
        flag = meta.get("rebuild_toc", False)
        if isinstance(flag, bool):
            return flag
        if isinstance(flag, str):
            return flag.strip().lower() in {"true", "yes", "1"}
        return bool(flag)
    except Exception as exc:
        logger.warning("Failed to parse rebuild_toc flag from %s (%s); defaulting to rebuild", toc_path, exc)
        return True


def _split_markdown_file_into_sections(
    md_path: Path,
    kb_dir: Path,
    category: str,
) -> List[Dict[str, Any]]:
    """Splits a Markdown file into self-contained conceptual sections at `## ` headings
    (and `### ` headings when a `## ` chapter exceeds 3,200 characters).
    """
    rel_path = md_path.relative_to(kb_dir).as_posix()
    file_stem = f"{category}/{md_path.stem}"
    raw_text = md_path.read_text(encoding="utf-8", errors="ignore").strip()
    if not raw_text:
        return []

    # Strip optional YAML frontmatter if present
    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)
        if len(parts) >= 3:
            raw_text = parts[2].strip()

    lines = raw_text.splitlines()
    doc_title = md_path.stem.replace("_", " ")
    for line in lines[:15]:
        if line.startswith("# "):
            doc_title = line[2:].strip()
            break

    # Split at top-level `## ` headings first
    h2_blocks: List[Tuple[str, List[str]]] = []
    cur_h2_title = "Overview"
    cur_h2_lines: List[str] = []

    for line in lines:
        if line.startswith("## "):
            if cur_h2_lines:
                h2_blocks.append((cur_h2_title, cur_h2_lines))
            cur_h2_title = line[3:].strip()
            cur_h2_lines = [line]
        else:
            cur_h2_lines.append(line)
    if cur_h2_lines:
        h2_blocks.append((cur_h2_title, cur_h2_lines))

    sections: List[Dict[str, Any]] = []
    seen_ids: Counter = Counter()

    for h2_title, h2_lines in h2_blocks:
        block_text = "\n".join(h2_lines).strip()
        if not block_text or len(block_text) < 40:
            continue

        # If a manual chapter is large (>3,200 chars) and has `### ` sub-headings, split by `### `
        has_h3 = any(l.startswith("### ") for l in h2_lines)
        if category == "02_manuals" and len(block_text) > 3200 and has_h3:
            cur_h3_title = h2_title
            cur_h3_lines: List[str] = []
            h3_blocks: List[Tuple[str, List[str]]] = []
            for l in h2_lines:
                if l.startswith("### "):
                    if cur_h3_lines:
                        h3_blocks.append((cur_h3_title, cur_h3_lines))
                    cur_h3_title = f"{h2_title} > {l[4:].strip()}"
                    cur_h3_lines = [f"## {h2_title}", l]
                else:
                    cur_h3_lines.append(l)
            if cur_h3_lines:
                h3_blocks.append((cur_h3_title, cur_h3_lines))

            for sub_title, sub_lines in h3_blocks:
                sub_text = "\n".join(sub_lines).strip()
                if len(sub_text) < 40:
                    continue
                slug = _slugify_heading(sub_title.split(">")[-1])
                base_id = f"{file_stem}#{slug}"
                seen_ids[base_id] += 1
                sec_id = base_id if seen_ids[base_id] == 1 else f"{base_id}-{seen_ids[base_id]}"
                sections.append({
                    "section_id": sec_id,
                    "category": category,
                    "source_file": rel_path,
                    "doc_title": doc_title,
                    "title": sub_title,
                    "content": sub_text,
                })
        else:
            slug = _slugify_heading(h2_title)
            base_id = f"{file_stem}#{slug}"
            seen_ids[base_id] += 1
            sec_id = base_id if seen_ids[base_id] == 1 else f"{base_id}-{seen_ids[base_id]}"
            sections.append({
                "section_id": sec_id,
                "category": category,
                "source_file": rel_path,
                "doc_title": doc_title,
                "title": h2_title,
                "content": block_text,
            })

    return sections


def _extract_scm_metadata_from_source(scm_path: Path, kb_dir: Path) -> Dict[str, Any]:
    """Deterministically parses a `.scm` file to extract algebra, herald flags, protocols,
    roles, sorts, operators, keywords, and header comment summary.
    """
    raw = scm_path.read_text(encoding="utf-8", errors="ignore")
    rel_path = scm_path.relative_to(kb_dir).as_posix()

    # Extract leading `;` comments for summary
    comment_lines: List[str] = []
    for line in raw.splitlines()[:25]:
        stripped = line.strip()
        if stripped.startswith(";"):
            cleaned = stripped.lstrip(";").strip()
            if cleaned and not cleaned.lower().startswith("copyright"):
                comment_lines.append(cleaned)
        elif stripped and not stripped.startswith("(herald"):
            break

    algebra = "diffie-hellman" if "diffie-hellman" in raw else "basic"
    protocols = re.findall(r"\(\s*defprotocol\s+([a-zA-Z0-9_\-]+)", raw)
    roles = list(dict.fromkeys(re.findall(r"\(\s*defrole\s+([a-zA-Z0-9_\-]+)", raw)))

    tokens_set = set(tokenize_cpsa_dsl(raw))
    sorts_used = sorted(tokens_set & _KNOWN_SORTS)
    operators_used = sorted(tokens_set & _KNOWN_OPERATORS)
    keywords_used = sorted(tokens_set & _KNOWN_KEYWORDS)

    herald_flags: List[str] = []
    for flag in ("bound", "limit", "depth", "goals-sat", "try-old-strands", "reverse-nodes", "check-nonces", "algebra"):
        if re.search(rf"\(\s*{flag}\b", raw):
            herald_flags.append(flag)

    summary = " ".join(comment_lines[:3])[:260] or f"Official MITRE CPSA {algebra} example ({scm_path.name})"
    return {
        "example_id": rel_path,
        "filename": scm_path.name,
        "protocol_names": protocols,
        "algebra": algebra,
        "herald_flags": herald_flags,
        "roles": roles,
        "sorts_used": sorts_used,
        "operators_used": operators_used,
        "keywords_used": keywords_used,
        "uses_channels": bool({"chan", "auth", "conf"} & tokens_set),
        "uses_state_locn": bool({"locn", "load", "stor", "gen-st"} & tokens_set),
        "uses_goals": "defgoal" in tokens_set,
        "uses_rules_or_lemmas": bool({"defrule", "defgenrule", "deflemma"} & tokens_set),
        "uses_macros": "defmacro" in tokens_set,
        "has_roletran_declarations": bool({"inputs", "outputs"} & tokens_set),
        "summary": summary,
    }


def build_cpsa_kb_index(kb_dir: Path = CPSA_KB_DIR) -> Dict[str, Any]:
    """Scans all Markdown guides/manuals/catalogs and `.scm` examples in `kb_dir`,
    writes `kb_index.json`, and writes `TOC.md` with `rebuild_toc: false`.
    """
    kb_dir.mkdir(parents=True, exist_ok=True)
    sections: List[Dict[str, Any]] = []

    for category in ("01_core_rules", "02_manuals", "04_examples_catalog"):
        cat_dir = kb_dir / category
        if not cat_dir.exists():
            continue
        for md_file in sorted(cat_dir.glob("*.md")):
            sections.extend(_split_markdown_file_into_sections(md_file, kb_dir, category))

    # Load curated batch*_meta.json if available, then merge with all .scm files in 03_examples_scm/
    curated_scm_meta: Dict[str, Dict[str, Any]] = {}
    catalog_dir = kb_dir / "04_examples_catalog"
    if catalog_dir.exists():
        for meta_file in sorted(catalog_dir.glob("batch*_meta.json")):
            try:
                items = json.loads(meta_file.read_text(encoding="utf-8", errors="ignore"))
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, dict) and item.get("filename"):
                            curated_scm_meta[item["filename"]] = item
            except Exception as exc:
                logger.warning("Could not parse %s: %s", meta_file, exc)

    scm_examples: List[Dict[str, Any]] = []
    scm_dir = kb_dir / "03_examples_scm"
    if scm_dir.exists():
        for scm_file in sorted(scm_dir.glob("*.scm")):
            auto_meta = _extract_scm_metadata_from_source(scm_file, kb_dir)
            if scm_file.name in curated_scm_meta:
                merged = {**auto_meta, **curated_scm_meta[scm_file.name]}
                merged["example_id"] = auto_meta["example_id"]
                merged["filename"] = scm_file.name
            else:
                merged = auto_meta
            scm_examples.append(merged)

    built_iso = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    index_payload = {
        "schema_version": "2.0.0",
        "built_at": built_iso,
        "total_sections": len(sections),
        "total_scm_examples": len(scm_examples),
        "sections": sections,
        "scm_examples": scm_examples,
    }

    index_path = kb_dir / "kb_index.json"
    index_path.write_text(json.dumps(index_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Build human- and LLM-readable TOC.md with rebuild_toc: false frontmatter flag
    toc_lines: List[str] = [
        "---",
        "# CPSA 4.4.9 Knowledge Base Master Table of Contents",
        "# Flip `rebuild_toc: true` whenever you add or edit .md or .scm files in refrences/cpsa_kb/.",
        "# On the next run, the loader will automatically rebuild TOC.md + kb_index.json and reset `rebuild_toc: false`.",
        "rebuild_toc: false",
        f'last_built: "{built_iso}"',
        f"total_sections: {len(sections)}",
        f"total_scm_examples: {len(scm_examples)}",
        "---",
        "",
        "# MITRE CPSA 4.4.9 Knowledge Base — Master Table of Contents",
        "",
    ]

    for cat_key, cat_header in (
        ("01_core_rules", "## 1. Core Operational Rules & Schema Mapping (`01_core_rules/`)"),
        ("02_manuals", "## 2. Official MITRE CPSA 4.4.9 Manuals (`02_manuals/`)"),
        ("04_examples_catalog", "## 3. Official `.scm` Examples Catalog (`04_examples_catalog/`)"),
    ):
        cat_secs = [s for s in sections if s["category"] == cat_key]
        if not cat_secs:
            continue
        toc_lines.append(cat_header)
        by_file: Dict[str, List[Dict[str, Any]]] = {}
        for s in cat_secs:
            by_file.setdefault(s["source_file"], []).append(s)
        for src_file, file_secs in by_file.items():
            toc_lines.append(f"\n### `{src_file}` ({file_secs[0]['doc_title']})")
            for s in file_secs:
                toc_lines.append(f"- `{s['section_id']}` — {s['title']}")
        toc_lines.append("")

    if scm_examples:
        dh_ex = [e["filename"] for e in scm_examples if e.get("algebra") == "diffie-hellman"]
        chan_ex = [e["filename"] for e in scm_examples if e.get("uses_channels")]
        state_ex = [e["filename"] for e in scm_examples if e.get("uses_state_locn")]
        goal_ex = [e["filename"] for e in scm_examples if e.get("uses_goals")]
        rule_ex = [e["filename"] for e in scm_examples if e.get("uses_rules_or_lemmas")]
        roletran_ex = [e["filename"] for e in scm_examples if e.get("has_roletran_declarations")]
        toc_lines.extend([
            "## 4. Indexed `.scm` Protocol Examples by Feature (`03_examples_scm/`)",
            f"- **Diffie-Hellman (`diffie-hellman`, `rndx`, `uniq-gen`, `exp`) [{len(dh_ex)} files]**: {', '.join(dh_ex)}",
            f"- **Roletran Procedural Inputs/Outputs (`inputs`, `outputs`, `chan`) [{len(roletran_ex)} files]**: {', '.join(roletran_ex)}",
            f"- **Channels (`chan`, `auth`, `conf`) [{len(chan_ex)} files]**: {', '.join(chan_ex)}",
            f"- **Stateful Memory Locations (`locn`, `load`, `stor`, `gen-st`) [{len(state_ex)} files]**: {', '.join(state_ex)}",
            f"- **Security Goals (`defgoal`) [{len(goal_ex)} files]**: {', '.join(goal_ex)}",
            f"- **Axiom Rules & Lemmas (`defrule`, `defgenrule`, `deflemma`) [{len(rule_ex)} files]**: {', '.join(rule_ex)}",
            "",
        ])

    toc_path = kb_dir / "TOC.md"
    toc_path.write_text("\n".join(toc_lines), encoding="utf-8")
    logger.info(
        "Built CPSA Knowledge Base index (%d sections, %d .scm examples) and set rebuild_toc=false in %s",
        len(sections),
        len(scm_examples),
        toc_path,
    )
    return index_payload


class CPSAKnowledgeBase:
    """In-memory CPSA 4.4.9 Knowledge Base supporting TOC section lookup, DSL-aware BM25 +
    exact compiler-error substring boost + optional FlashRank ONNX cross-encoder reranking,
    and operator-indexed `.scm` example retrieval.
    """

    def __init__(self, kb_dir: Path = CPSA_KB_DIR):
        self.kb_dir = Path(kb_dir)
        self.toc_path = self.kb_dir / "TOC.md"
        self.index_path = self.kb_dir / "kb_index.json"

        if parse_toc_rebuild_flag(self.toc_path) or not self.index_path.exists():
            payload = build_cpsa_kb_index(self.kb_dir)
        else:
            try:
                payload = json.loads(self.index_path.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                payload = build_cpsa_kb_index(self.kb_dir)

        self.sections: List[Dict[str, Any]] = payload.get("sections", [])
        self.scm_examples: List[Dict[str, Any]] = payload.get("scm_examples", [])
        self.section_by_id: Dict[str, Dict[str, Any]] = {
            s["section_id"]: s for s in self.sections if s.get("section_id")
        }
        self.scm_by_name: Dict[str, Dict[str, Any]] = {}
        for ex in self.scm_examples:
            self.scm_by_name[ex["filename"]] = ex
            self.scm_by_name[ex["example_id"]] = ex

        # Build compact navigator map for the Agentic Searcher LLM prompt
        self.compact_toc_map: str = self._build_compact_searcher_map()

        # Build DSL-BM25 lexical index over all sections
        self.doc_tokens: List[List[str]] = []
        self.doc_term_freqs: List[Counter] = []
        self.term_doc_freqs: Counter = Counter()
        self.doc_lengths: List[int] = []
        for sec in self.sections:
            combined = f"{sec.get('section_id', '')} {sec.get('title', '')} {sec.get('doc_title', '')} {sec.get('content', '')}"
            toks = tokenize_cpsa_dsl(combined)
            tf = Counter(toks)
            self.doc_tokens.append(toks)
            self.doc_term_freqs.append(tf)
            self.doc_lengths.append(len(toks))
            for term in tf:
                self.term_doc_freqs[term] += 1

        self.total_docs = len(self.sections)
        self.avg_doc_len = (sum(self.doc_lengths) / self.total_docs) if self.total_docs else 1.0

        # Lazy-loaded local in-process ONNX cross-encoder reranker (FlashRank)
        self._ranker = None
        self._ranker_initialized = False

    def _get_ranker(self):
        if not self._ranker_initialized:
            self._ranker_initialized = True
            try:
                from flashrank import Ranker
                self._ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")
            except Exception:
                self._ranker = None
        return self._ranker

    def _build_compact_searcher_map(self) -> str:
        """Builds a compact (~700-token) directory of `01_core_rules/`, `02_manuals/`,
        and `.scm` categories for the Agentic Searcher LLM's system prompt.
        """
        lines: List[str] = ["AVAILABLE CPSA 4.4.9 KNOWLEDGE BASE SECTIONS:"]
        core_secs = [s for s in self.sections if s.get("category") == "01_core_rules"]
        for s in core_secs:
            lines.append(f"  - {s['section_id']} : {s['title']}")

        manual_files: Dict[str, List[str]] = {}
        for s in self.sections:
            if s.get("category") == "02_manuals":
                manual_files.setdefault(s["source_file"], []).append(s["section_id"])
        if manual_files:
            lines.append("\nOFFICIAL MANUAL CHAPTERS (`02_manuals/`):")
            for src, sids in manual_files.items():
                sample_ids = ", ".join(sids[:5])
                more = f" (+{len(sids) - 5} more)" if len(sids) > 5 else ""
                lines.append(f"  - {src}: {sample_ids}{more}")

        dh_files = [e["filename"] for e in self.scm_examples if e.get("algebra") == "diffie-hellman"]
        roletran_files = [e["filename"] for e in self.scm_examples if e.get("has_roletran_declarations")]
        chan_files = [e["filename"] for e in self.scm_examples if e.get("uses_channels")]
        state_files = [e["filename"] for e in self.scm_examples if e.get("uses_state_locn")]
        lines.extend([
            f"\nINDEXED OFFICIAL .SCM EXAMPLES ({len(self.scm_examples)} files in `03_examples_scm/` & `04_examples_catalog/`):",
            f"  - Diffie-Hellman examples: {', '.join(dh_files[:12])}",
            f"  - Roletran (inputs/outputs/chan) examples: {', '.join(roletran_files[:12])}",
            f"  - Channel (auth/conf) examples: {', '.join(chan_files[:10])}",
            f"  - Stateful (locn/load/stor/gen-st) examples: {', '.join(state_files[:10])}",
        ])
        return "\n".join(lines)

    def read_section(self, section_id: str) -> Optional[Dict[str, Any]]:
        """Tool 1: Looks up a Markdown section by exact or partial `section_id`."""
        if not section_id:
            return None
        target = section_id.strip().strip("`'\"")
        if target in self.section_by_id:
            return self.section_by_id[target]

        # Fuzzy suffix or substring match
        target_low = target.lower()
        for sid, sec in self.section_by_id.items():
            if sid.lower() == target_low or sid.lower().endswith(target_low) or target_low in sid.lower():
                return sec
        return None

    def search_cpsa_docs(
        self,
        query: str,
        category: str = "all",
        top_k: int = 3,
        rerank: bool = True,
    ) -> List[Dict[str, Any]]:
        """Tool 2: Searches Markdown sections using DSL-BM25 + exact error phrase boosting
        + optional in-process FlashRank ONNX cross-encoder reranking.
        """
        if not self.sections:
            return []

        q_tokens = tokenize_cpsa_dsl(query)
        q_lower = query.lower().strip()
        k1 = 1.5
        b = 0.75

        scored: List[Tuple[float, int]] = []
        for idx, sec in enumerate(self.sections):
            if category != "all" and sec.get("category") != category:
                continue

            tf_map = self.doc_term_freqs[idx]
            doc_len = self.doc_lengths[idx] or 1
            score = 0.0

            for tok in q_tokens:
                df = self.term_doc_freqs.get(tok, 0)
                if df == 0:
                    continue
                idf = math.log(1.0 + (self.total_docs - df + 0.5) / (df + 0.5))
                tf = tf_map.get(tok, 0)
                if tf > 0:
                    score += idf * ((tf * (k1 + 1.0)) / (tf + k1 * (1.0 - b + b * (doc_len / self.avg_doc_len))))

            title_low = sec.get("title", "").lower()
            content_low = sec.get("content", "").lower()

            # Boost core rules and exact title/phrase matches
            if sec.get("category") == "01_core_rules":
                score *= 1.35
            for tok in q_tokens:
                if tok in title_low:
                    score += 3.5
            if len(q_lower) >= 6 and q_lower in content_low:
                score += 12.0

            if score > 0:
                scored.append((score, idx))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        candidate_indices = [idx for _, idx in scored[: max(top_k * 4, 12)]]
        if not candidate_indices:
            candidate_indices = list(range(min(top_k, len(self.sections))))

        ranker = self._get_ranker() if rerank else None
        if ranker is not None and len(candidate_indices) > top_k:
            try:
                from flashrank import RerankRequest
                passages = [
                    {
                        "id": idx,
                        "text": f"{self.sections[idx]['title']}\n{self.sections[idx]['content'][:1500]}",
                    }
                    for idx in candidate_indices
                ]
                reranked = ranker.rerank(RerankRequest(query=query, passages=passages))
                bm25_ranks = {idx: rank for rank, idx in enumerate(candidate_indices, 1)}
                ce_ranks = {int(item["id"]): rank for rank, item in enumerate(reranked, 1)}
                fused = sorted(
                    candidate_indices,
                    key=lambda i: (1.0 / (20 + bm25_ranks.get(i, 50))) + (1.0 / (20 + ce_ranks.get(i, 50))),
                    reverse=True,
                )
                return [self.sections[i] for i in fused[:top_k]]
            except Exception:
                pass

        return [self.sections[i] for i in candidate_indices[:top_k]]

    def find_scm_examples(
        self,
        algebra: Optional[str] = None,
        operators: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        query: Optional[str] = None,
        top_k: int = 3,
    ) -> List[Dict[str, Any]]:
        """Tool 3: Filters and ranks the 151 official MITRE `.scm` examples by algebra,
        operators, assumption/goal keywords, and free-text query.
        """
        q_tokens = set(tokenize_cpsa_dsl(query or ""))
        req_ops = {op.lower().strip() for op in (operators or []) if op}
        req_kws = {kw.lower().strip() for kw in (keywords or []) if kw}
        req_alg = algebra.lower().strip() if algebra else None

        scored: List[Tuple[float, Dict[str, Any]]] = []
        for ex in self.scm_examples:
            score = 0.0
            ex_alg = (ex.get("algebra") or "basic").lower()
            if req_alg and req_alg in {"basic", "diffie-hellman"}:
                if ex_alg == req_alg:
                    score += 5.0
                else:
                    continue

            ex_ops = set(ex.get("operators_used") or [])
            ex_kws = set(ex.get("keywords_used") or [])
            ex_sorts = set(ex.get("sorts_used") or [])
            all_tags = ex_ops | ex_kws | ex_sorts

            for op in req_ops:
                if op in all_tags:
                    score += 4.0
            for kw in req_kws:
                if kw in all_tags:
                    score += 4.0

            haystack = f"{ex.get('filename', '')} {' '.join(ex.get('protocol_names') or [])} {ex.get('summary', '')}".lower()
            for qt in q_tokens:
                if qt in all_tags:
                    score += 3.0
                if qt in haystack:
                    score += 2.5

            if ex.get("has_roletran_declarations"):
                score += 0.5

            if score > 0 or not (req_ops or req_kws or q_tokens):
                scored.append((score, ex))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [ex for _, ex in scored[:top_k]]

    def read_scm_example(self, filename_or_id: str) -> Optional[Dict[str, Any]]:
        """Tool 4: Reads the full verbatim `.scm` code and catalog entry for a MITRE `.scm` example."""
        if not filename_or_id:
            return None
        key = Path(filename_or_id.strip().strip("`'\"")).name
        ex = self.scm_by_name.get(key) or self.scm_by_name.get(filename_or_id.strip())
        if not ex:
            for cand_name, cand_ex in self.scm_by_name.items():
                if key.lower() in cand_name.lower():
                    ex = cand_ex
                    break
        if not ex:
            return None

        scm_file = self.kb_dir / ex["example_id"]
        scm_code = scm_file.read_text(encoding="utf-8", errors="ignore") if scm_file.exists() else ""
        return {
            **ex,
            "scm_code": scm_code,
        }

    def search(
        self,
        query: str,
        top_k: int = 2,
        mode: str = "hybrid",
        rerank: bool = True,
    ) -> List[Dict[str, Any]]:
        """Backward-compatible `.search()` interface returning standard chunk dicts."""
        hits = self.search_cpsa_docs(query=query, category="all", top_k=top_k, rerank=rerank)
        results: List[Dict[str, Any]] = []
        for sec in hits:
            results.append({
                "chunk_id": sec["section_id"],
                "title": sec["title"],
                "source_file": sec["source_file"],
                "text": sec["content"],
            })
        return results


def get_cpsa_manual_retriever(force_reload: bool = False) -> Optional[CPSAKnowledgeBase]:
    """Returns the lazy-loaded singleton `CPSAKnowledgeBase` instance, automatically rebuilding
    `TOC.md` and `kb_index.json` if `rebuild_toc: true` is set in `TOC.md`.
    """
    global _GLOBAL_RETRIEVER
    if _GLOBAL_RETRIEVER is None or force_reload or parse_toc_rebuild_flag(TOC_MD_PATH):
        try:
            _GLOBAL_RETRIEVER = CPSAKnowledgeBase(CPSA_KB_DIR)
            logger.info(
                "Initialized CPSAKnowledgeBase (%d sections, %d .scm examples)",
                len(_GLOBAL_RETRIEVER.sections),
                len(_GLOBAL_RETRIEVER.scm_examples),
            )
        except Exception as exc:
            logger.warning("Could not initialize CPSAKnowledgeBase: %s", exc)
            _GLOBAL_RETRIEVER = None
    return _GLOBAL_RETRIEVER


def retrieve_cpsa_manual_guidance(
    query: str,
    stage: int,
    purpose: str,
    header_prefix: str = "Reference",
    top_k: int = 2,
    fallback_message: str = "Use standard MITRE CPSA 4.4.9 syntax conventions.",
) -> str:
    """Executes a search over `CPSAKnowledgeBase`, emits a `rag_retrieval` telemetry event,
    and returns formatted reference blocks.
    """
    global LAST_RETRIEVED_CHUNK_IDS, LAST_SEARCHER_QUERY
    LAST_RETRIEVED_CHUNK_IDS = []
    LAST_SEARCHER_QUERY = query
    kb = get_cpsa_manual_retriever()
    if not kb:
        return fallback_message

    try:
        search_hits = kb.search(query, top_k=top_k, rerank=True)
        formatted_blocks: List[str] = []
        telemetry_chunks: List[dict] = []

        for idx, chunk in enumerate(search_hits, 1):
            chunk_id = str(chunk.get("chunk_id") or idx)
            chunk_title = chunk.get("title") or f"Section {idx}"
            chunk_source = chunk.get("source_file") or "CPSA Knowledge Base"
            chunk_text = chunk.get("text") or ""

            LAST_RETRIEVED_CHUNK_IDS.append(chunk_id)
            formatted_blocks.append(
                f"--- {header_prefix} {idx}: {chunk_title} ({chunk_source}) ---\n{chunk_text[:1800]}"
            )
            telemetry_chunks.append({
                "chunk_id": chunk_id,
                "title": chunk_title,
                "source_file": chunk_source,
                "snippet": chunk_text[:280].strip() + ("..." if len(chunk_text) > 280 else ""),
            })

        GLOBAL_EVENT_BUS.emit(
            "rag_retrieval",
            stage=stage,
            purpose=purpose,
            query=query,
            chunks=telemetry_chunks,
        )
        if formatted_blocks:
            return "\n\n".join(formatted_blocks)
    except Exception as exc:
        logger.warning("Knowledge base retrieval failed during %s: %s", purpose, exc)

    return fallback_message


def _summarize_failing_ast_for_searcher(failing_spec: Any) -> str:
    """Produces a compact structural summary of the failing `CPSAProtocolSpecification`
    so the Searcher LLM can inspect role variables, sorts, inputs/outputs/origination,
    and skeleton declarations without 10KB of raw JSON noise.
    """
    try:
        data = failing_spec.model_dump() if hasattr(failing_spec, "model_dump") else dict(failing_spec)
        lines = [
            f"Protocol: {data.get('protocol_name')} | Algebra: {data.get('message_algebra', 'basic')}",
        ]
        for r in data.get("roles", []):
            vars_str = ", ".join(f"{v['name']}:{v['sort']}" for v in r.get("variables", []))
            lines.append(
                f"  Role '{r.get('role_name')}': vars=[{vars_str}] | "
                f"inputs={r.get('inputs', [])} | outputs={r.get('outputs', [])} | "
                f"uniq_orig={r.get('unique_originating', [])} | trace_len={len(r.get('trace', []))}"
            )
        for idx, sk in enumerate(data.get("skeletons", []), 1):
            strands_str = ", ".join(s.get("role_name", "?") for s in sk.get("strands", []))
            lines.append(
                f"  Skeleton #{idx}: strands=[{strands_str}] | listeners={sk.get('listeners', [])} | "
                f"non_orig={sk.get('non_originating', [])} | uniq_orig={sk.get('unique_originating', [])} | "
                f"uniq_gen={sk.get('unique_generated', [])}"
            )
        return "\n".join(lines)
    except Exception:
        return "AST summary unavailable."


def run_agentic_cpsa_searcher(
    error_diagnostic: str,
    failure_stage: str,
    failing_spec: Optional[Any] = None,
    model: Optional[str] = None,
    cycle_detected: bool = False,
    fallback_query_fn: Optional[Any] = None,
) -> str:
    """Runs the Agentic CPSA Knowledge Base Searcher (`05_rag_query_formulation.md`).

    The Searcher LLM inspects the Master TOC map, the failing AST summary, and the
    compiler diagnostic, invokes deterministic KB tools (`read_section`, `search_cpsa_docs`,
    `find_scm_examples`, `read_scm_example`), and returns verified CPSA rules, working
    `.scm` examples, and a pinpointed AST fix brief for the Stage 5/6 Repair LLM.
    """
    global LAST_RETRIEVED_CHUNK_IDS, LAST_SEARCHER_QUERY, LAST_SEARCHER_DIAGNOSIS, LAST_SEARCHER_TRACE
    LAST_RETRIEVED_CHUNK_IDS = []
    LAST_SEARCHER_DIAGNOSIS = None
    LAST_SEARCHER_TRACE = []
    kb = get_cpsa_manual_retriever()
    if not kb:
        return "Review standard MITRE CPSA 4.4.9 executability and preskeleton assumption rules."

    # Normalize error signature for caching across non-cycling attempts
    norm_sig = f"{failure_stage}:{re.sub(r'[0-9]+', '#', error_diagnostic[:220])}"
    if not cycle_detected and norm_sig in _SEARCH_CACHE:
        cached_query, cached_guidance, cached_ids, cached_diag, cached_trace = _SEARCH_CACHE[norm_sig]
        LAST_SEARCHER_QUERY = cached_query
        LAST_RETRIEVED_CHUNK_IDS = list(cached_ids)
        LAST_SEARCHER_DIAGNOSIS = cached_diag
        LAST_SEARCHER_TRACE = list(cached_trace)
        return cached_guidance

    searcher_spec = load_prompt_spec(PROMPT_RAG_QUERY_FORMULATION)
    searcher_model = model or searcher_spec.model
    sampling_temp = searcher_spec.temperature if searcher_spec.temperature is not None else 0.0

    ast_summary = _summarize_failing_ast_for_searcher(failing_spec) if failing_spec is not None else ""
    algebra_hint = getattr(failing_spec, "message_algebra", "basic") if failing_spec is not None else "basic"

    collected_sections: Dict[str, Dict[str, Any]] = {}
    collected_examples: Dict[str, Dict[str, Any]] = {}
    searcher_diagnosis: Optional[str] = None
    executed_queries: List[str] = []
    searcher_turns: List[Dict[str, Any]] = []

    # Step 1: Ask the Searcher LLM which KB tools/sections to inspect (up to 2 turns)
    user_context = (
        f"{kb.compact_toc_map}\n\n"
        f"FAILURE STAGE: {failure_stage}\n"
        f"CYCLE DETECTED: {cycle_detected}\n"
        f"COMPILER DIAGNOSTIC:\n{error_diagnostic}\n\n"
        f"FAILING PROTOCOL AST SUMMARY:\n{ast_summary}\n"
    )

    messages = [
        {"role": "system", "content": searcher_spec.body},
        {"role": "user", "content": user_context},
    ]

    try:
        llm_kwargs = SYSTEM_CONFIG.get_llm_kwargs(
            searcher_model,
            temperature=sampling_temp,
            max_tokens=searcher_spec.max_tokens,
        )
        for turn_idx in range(2):
            resp = litellm.completion(
                **llm_kwargs,
                messages=messages,
                timeout=searcher_spec.timeout,
                num_retries=0,
            )
            from src.cost_tracker import GLOBAL_COST_TRACKER
            GLOBAL_COST_TRACKER.record_llm_call(
                resp,
                role="query",
                model_name=searcher_model,
                stage=5 if failure_stage == "roletran" else 6,
            )
            raw_reply = (resp.choices[0].message.content or "").strip()
            if not raw_reply:
                break

            # Support both structured JSON tool-action replies and plain search query replies
            parsed_json = None
            if "{" in raw_reply and "}" in raw_reply:
                try:
                    parsed_json = json.loads(raw_reply)
                except Exception:
                    try:
                        parsed_json = json_repair.loads(raw_reply)
                    except Exception:
                        parsed_json = None

            if isinstance(parsed_json, dict) and (
                "tool_calls" in parsed_json or "actions" in parsed_json or "ast_root_cause" in parsed_json
            ):
                root_cause_str = parsed_json.get("ast_root_cause") or parsed_json.get("diagnosis") or ""
                fix_str = parsed_json.get("actionable_fix") or parsed_json.get("fix_instructions") or ""
                if root_cause_str or fix_str:
                    searcher_diagnosis = (
                        f"Root Cause in AST: {root_cause_str}\n"
                        f"Recommended AST Fix: {fix_str}"
                    ).strip()

                tool_calls = parsed_json.get("tool_calls") or parsed_json.get("actions") or []
                tool_feedback_blocks: List[str] = []
                turn_tool_log: List[Dict[str, Any]] = []

                for call in tool_calls[:4]:
                    if not isinstance(call, dict):
                        continue
                    t_name = (call.get("tool") or call.get("action") or "").strip()
                    if t_name == "read_section":
                        sec_id = call.get("section_id") or call.get("id") or ""
                        executed_queries.append(f"read_section({sec_id})")
                        sec = kb.read_section(sec_id)
                        if sec:
                            collected_sections[sec["section_id"]] = sec
                            tool_feedback_blocks.append(
                                f"[Section {sec['section_id']}: {sec['title']}]\n{sec['content'][:1600]}"
                            )
                            turn_tool_log.append({
                                "tool": "read_section",
                                "args": sec_id,
                                "retrieved": f"{sec['section_id']} ({sec['title']})",
                            })
                        else:
                            turn_tool_log.append({
                                "tool": "read_section",
                                "args": sec_id,
                                "retrieved": "No matching section found",
                            })
                    elif t_name == "search_cpsa_docs":
                        q = call.get("query") or ""
                        cat = call.get("category") or "all"
                        if q:
                            executed_queries.append(q)
                            hits = kb.search_cpsa_docs(q, category=cat, top_k=2)
                            hit_labels: List[str] = []
                            for sec in hits:
                                collected_sections[sec["section_id"]] = sec
                                hit_labels.append(f"{sec['section_id']} ({sec['title']})")
                                tool_feedback_blocks.append(
                                    f"[Section {sec['section_id']}: {sec['title']}]\n{sec['content'][:1400]}"
                                )
                            turn_tool_log.append({
                                "tool": "search_cpsa_docs",
                                "args": f"query='{q}', category='{cat}'",
                                "retrieved": ", ".join(hit_labels) or "0 hits",
                            })
                    elif t_name in {"find_scm_examples", "read_scm_example"}:
                        fname = call.get("filename") or call.get("example_id")
                        if fname:
                            ex = kb.read_scm_example(fname)
                            if ex:
                                executed_queries.append(f"read_scm_example({ex['filename']})")
                                collected_examples[ex["example_id"]] = ex
                                tool_feedback_blocks.append(
                                    f"[Example {ex['filename']} ({ex['algebra']})]\n{ex.get('scm_code', '')[:1400]}"
                                )
                                turn_tool_log.append({
                                    "tool": "read_scm_example",
                                    "args": fname,
                                    "retrieved": f"{ex['filename']} ({ex['algebra']}): {ex.get('summary', '')[:120]}",
                                })
                        else:
                            alg = call.get("algebra") or algebra_hint
                            ops = call.get("operators") or []
                            kws = call.get("keywords") or []
                            q = call.get("query") or ""
                            executed_queries.append(f"find_scm({alg}, ops={ops}, kws={kws})")
                            matches = kb.find_scm_examples(algebra=alg, operators=ops, keywords=kws, query=q, top_k=2)
                            match_names: List[str] = []
                            for match_ex in matches:
                                full_ex = kb.read_scm_example(match_ex["filename"])
                                if full_ex:
                                    collected_examples[full_ex["example_id"]] = full_ex
                                    match_names.append(f"{full_ex['filename']} ({full_ex['algebra']})")
                                    tool_feedback_blocks.append(
                                        f"[Example {full_ex['filename']} ({full_ex['algebra']})]\n{full_ex.get('scm_code', '')[:1400]}"
                                    )
                            turn_tool_log.append({
                                "tool": "find_scm_examples",
                                "args": f"algebra={alg}, ops={ops}, kws={kws}",
                                "retrieved": ", ".join(match_names) or "0 examples",
                            })

                is_final_turn = bool(parsed_json.get("is_final") or not tool_feedback_blocks or turn_idx == 1)
                searcher_turns.append({
                    "turn": turn_idx + 1,
                    "is_final": is_final_turn,
                    "status": "Final Diagnosis & Evidence Ready" if is_final_turn else "Ingested Tool Results -> Requesting Follow-up Synthesis",
                    "ast_root_cause": root_cause_str,
                    "actionable_fix": fix_str,
                    "tool_calls": turn_tool_log,
                })

                if is_final_turn:
                    break

                messages.append({"role": "assistant", "content": raw_reply})
                messages.append({
                    "role": "user",
                    "content": (
                        "TOOL RESULTS:\n"
                        + "\n\n".join(tool_feedback_blocks[:3])
                        + "\n\nNow output your final JSON with `is_final: true`, `ast_root_cause`, and `actionable_fix`."
                    ),
                })
            else:
                # Plain query string returned (e.g. lightweight model or unit test mock)
                clean_q = " ".join(raw_reply.strip().strip('"').strip("'").split())
                if clean_q:
                    executed_queries.append(clean_q)
                    hits = kb.search_cpsa_docs(clean_q, top_k=2)
                    for sec in hits:
                        collected_sections[sec["section_id"]] = sec
                    searcher_turns.append({
                        "turn": turn_idx + 1,
                        "is_final": True,
                        "status": "Direct Query Search Completed",
                        "ast_root_cause": "",
                        "actionable_fix": "",
                        "tool_calls": [{
                            "tool": "search_cpsa_docs",
                            "args": clean_q,
                            "retrieved": ", ".join(s["section_id"] for s in hits),
                        }],
                    })
                break
    except Exception as exc:
        logger.warning("Agentic CPSA searcher LLM step encountered exception (%s); using deterministic KB lookup", exc)

    # Step 2: If this is a Snowball State Error, always pin the authoritative CPSA 4.4.9
    # Anti-Snowballing & Termination core rule section so the Repair LLM has exact mathematical guidance.
    from src.verification_engine.snowball_autopsy import is_snowball_state_error
    if is_snowball_state_error(error_diagnostic):
        for sec in kb.search_cpsa_docs(
            "state space snowballing non-termination encryption-test try-old-strands check-nonces domain separation tags neq",
            category="01_core_rules",
            top_k=2,
        ):
            if "06_termination_and_anti_snowballing" in sec.get("source_file", "") or not collected_sections:
                collected_sections[sec["section_id"]] = sec

    # Step 3: Always guarantee high-precision deterministic fallback / enrichment from the error string
    if not collected_sections:
        fallback_q = (
            fallback_query_fn(error_diagnostic, failure_stage)
            if callable(fallback_query_fn)
            else f"CPSA {failure_stage} {error_diagnostic[:120]}"
        )
        executed_queries.append(fallback_q)
        for sec in kb.search_cpsa_docs(fallback_q, top_k=2):
            collected_sections[sec["section_id"]] = sec

    # Also pull 1 working .scm example matching the protocol's algebra if none was pulled yet
    if not collected_examples:
        for match_ex in kb.find_scm_examples(algebra=algebra_hint, query=error_diagnostic[:100], top_k=1):
            full_ex = kb.read_scm_example(match_ex["filename"])
            if full_ex:
                collected_examples[full_ex["example_id"]] = full_ex

    # Assemble final reference package and emit telemetry
    formatted_blocks: List[str] = []
    telemetry_chunks: List[Dict[str, Any]] = []

    if searcher_diagnosis:
        formatted_blocks.append(f"--- Agentic Searcher AST Diagnosis ---\n{searcher_diagnosis}")

    for idx, (sec_id, sec) in enumerate(list(collected_sections.items())[:3], 1):
        LAST_RETRIEVED_CHUNK_IDS.append(sec_id)
        formatted_blocks.append(
            f"--- Retrieved CPSA Rule {idx}: {sec['title']} ({sec['source_file']}) ---\n{sec['content'][:2200]}"
        )
        telemetry_chunks.append({
            "chunk_id": sec_id,
            "title": sec["title"],
            "source_file": sec["source_file"],
            "snippet": sec["content"][:280].strip() + ("..." if len(sec["content"]) > 280 else ""),
        })

    for idx, (ex_id, ex) in enumerate(list(collected_examples.items())[:1], 1):
        LAST_RETRIEVED_CHUNK_IDS.append(ex_id)
        scm_snippet = (ex.get("scm_code") or "")[:1600]
        formatted_blocks.append(
            f"--- Official MITRE .scm Example: {ex['filename']} (algebra: {ex.get('algebra')}) ---\n"
            f"Summary: {ex.get('summary', '')}\n{scm_snippet}"
        )
        telemetry_chunks.append({
            "chunk_id": ex_id,
            "title": f"MITRE Example: {ex['filename']} ({ex.get('algebra')})",
            "source_file": ex_id,
            "snippet": f"{ex.get('summary', '')}\n{scm_snippet[:200]}",
        })

    summary_query_str = " | ".join(executed_queries[:3]) or f"KB Search ({failure_stage})"
    LAST_SEARCHER_QUERY = summary_query_str
    LAST_SEARCHER_DIAGNOSIS = searcher_diagnosis
    LAST_SEARCHER_TRACE = list(searcher_turns)

    stage_num = 5 if failure_stage == "roletran" else 6
    GLOBAL_EVENT_BUS.emit(
        "rag_retrieval",
        stage=stage_num,
        purpose=f"Agentic KB Search ({failure_stage})",
        query=summary_query_str,
        searcher_diagnosis=searcher_diagnosis,
        searcher_turns=searcher_turns,
        chunks=telemetry_chunks,
    )

    final_guidance = "\n\n".join(formatted_blocks)
    _SEARCH_CACHE[norm_sig] = (
        summary_query_str,
        final_guidance,
        list(LAST_RETRIEVED_CHUNK_IDS),
        searcher_diagnosis,
        list(searcher_turns),
    )
    return final_guidance
