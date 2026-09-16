#!/usr/bin/env python3
"""
01_extract_chunks.py
Unified, recursive semantic component chunker for the entire CPSA corpus.

Scans all readable documents (.pdf, .md, .txt, .scm) in refrences/ (manual and internet)
and extracts pure, atomic semantic components using exact line-break boundary splitting.

Features:
- Automated recursive scanner: finds all .pdf, .md, .txt, and .scm files without artificial source flags.
- Preserves sections <= 750 words as pure, self-contained conceptual units.
- Sections > 750 words are analyzed by Gemini 3.1 Flash Lite to detect exact verbatim line-break
  anchors, with Python slicing at exact line numbers to guarantee 100% source text integrity.
- Real-time incremental persistence: every chunk is appended and flushed to manual_chunks.jsonl.
- Automatic resume: tracks completed files in checkpoint.json so reruns skip finished files.
- Synchronizes with manual_chunks.json for downstream tool compatibility.
"""

import os
import sys
import time
import json
import re
import argparse
from pathlib import Path
from pydantic import BaseModel, Field
import pymupdf
import dspy
import backoff
from dotenv import load_dotenv, find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(usecwd=True))
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

DEFAULT_SEARCH_DIRS = [BASE_DIR / "manual", BASE_DIR / "internet"]
CHUNKS_DIR = BASE_DIR / "chunks"
CHUNKS_JSONL_PATH = CHUNKS_DIR / "manual_chunks.jsonl"
CHUNKS_JSON_PATH = CHUNKS_DIR / "manual_chunks.json"
CHECKPOINT_PATH = CHUNKS_DIR / "checkpoint.json"
CLEAN_MD_PATH = CHUNKS_DIR / "all_references_clean.md"

MAX_CHUNK_WORDS = 750
DEFAULT_MODEL = os.environ.get("MODEL_NAME", "gemini/gemini-3.1-flash-lite")
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt", ".scm"}
EXCLUDE_FILENAMES = {
    "cpsa4manual.txt",       # Duplicate text of cpsa4manual.pdf
    "cpsa4manual_clean.md",  # Duplicate markdown
    "cpsa.cabal.txt",        # Packaging metadata
    "readme.md",             # Empty placeholder
    "manifest.json",         # Download manifest
}

class ThematicLineBreak(BaseModel):
    subtopic_title: str = Field(description="Descriptive title of the new subtopic, rule, or mechanism.")
    break_line_verbatim: str = Field(description="The EXACT verbatim sentence or line where this new subtopic begins.")

class FindExactThematicBreaks(dspy.Signature):
    """You are a formal methods expert and cryptographic protocol analyst.
Analyze the provided text from CPSA documentation.
Identify distinct thematic inflection points where a new subtopic, protocol rule, algebraic concept, or diagnostic mechanism begins.
For each boundary, return the EXACT verbatim line or first sentence from the text where the transition occurs.
Do NOT alter, paraphrase, or invent words. Return the exact line as it appears in the text."""
    section_title: str = dspy.InputField()
    category: str = dspy.InputField()
    section_text: str = dspy.InputField()
    breaks: list[ThematicLineBreak] = dspy.OutputField(desc="List of exact thematic breaks with verbatim line anchors.")

def clean_page_text(text: str) -> str:
    """Clean recurring PDF headers/footers."""
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if "MITRE Corporation" in stripped or stripped.isdigit():
            continue
        if stripped.startswith("The Cryptographic Protocol Shapes Analyzer:"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()

def split_by_verbatim_lines(text: str, breaks: list[ThematicLineBreak], base_title: str) -> list[tuple[str, str]]:
    """Split text at exact line numbers matching the LLM's verbatim break anchors."""
    if not breaks:
        return [(base_title, text)]

    lines = text.splitlines()
    if not lines:
        return [(base_title, text)]

    split_indices = []
    titles = []

    for b in breaks:
        anchor = b.break_line_verbatim.strip().lower()
        if not anchor:
            continue
        anchor_sub = anchor[:35]

        found_idx = -1
        for idx, line in enumerate(lines):
            line_clean = line.strip().lower()
            if not line_clean:
                continue
            if anchor in line_clean or line_clean in anchor or anchor_sub in line_clean:
                found_idx = idx
                break

        if found_idx != -1 and (not split_indices or found_idx > split_indices[-1]):
            split_indices.append(found_idx)
            titles.append(b.subtopic_title)

    if not split_indices:
        return [(base_title, text)]

    slices = []
    if split_indices[0] > 0:
        head_text = "\n".join(lines[0:split_indices[0]]).strip()
        if head_text:
            slices.append((f"{base_title} (Overview)", head_text))

    for i in range(len(split_indices)):
        start = split_indices[i]
        end = split_indices[i + 1] if i + 1 < len(split_indices) else len(lines)
        slice_text = "\n".join(lines[start:end]).strip()
        if slice_text:
            sub_title = titles[i]
            if sub_title.lower() not in base_title.lower():
                slice_title = f"{base_title} - {sub_title}"
            else:
                slice_title = sub_title
            slices.append((slice_title, slice_text))

    return slices if slices else [(base_title, text)]

def mechanical_paragraph_fallback(text: str, max_words: int = MAX_CHUNK_WORDS) -> list[str]:
    """Fallback paragraph grouping to guarantee chunks never exceed max_words."""
    paragraphs = text.split("\n\n")
    parts = []
    curr = []
    curr_w = 0
    for p in paragraphs:
        p_w = len(p.split())
        if curr_w + p_w > max_words and curr:
            parts.append("\n\n".join(curr))
            curr = [p]
            curr_w = p_w
        else:
            curr.append(p)
            curr_w += p_w
    if curr:
        parts.append("\n\n".join(curr))
    return parts

def ensure_bounded_slices(slices: list[tuple[str, str]], max_words: int = MAX_CHUNK_WORDS) -> list[tuple[str, str]]:
    bounded = []
    for title, text in slices:
        words = text.split()
        if len(words) <= max_words:
            bounded.append((title, text))
        else:
            fb = mechanical_paragraph_fallback(text, max_words=max_words)
            for idx, pt in enumerate(fb, 1):
                bounded.append((f"{title} (Part {idx})", pt))
    return bounded

@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=8,
    max_time=180,
    jitter=backoff.full_jitter,
    on_backoff=lambda details: print(
        f"  [RateLimit/Retry] Backing off {details['wait']:.1f}s after try {details['tries']}..."
    )
)
def run_splitter_with_backoff(splitter, **kwargs):
    return splitter(**kwargs)

class ChunkStreamManager:
    """Manages streaming append of chunks and checkpoint tracking."""
    def __init__(self, jsonl_path: Path, json_path: Path, checkpoint_path: Path, reprocess_all: bool = False):
        self.jsonl_path = jsonl_path
        self.json_path = json_path
        self.checkpoint_path = checkpoint_path
        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)

        self.history_log_path = CHUNKS_DIR / "processing_history.log"
        self.current_file_chunks = []

        if reprocess_all:
            if self.jsonl_path.exists():
                self.jsonl_path.unlink()
            if self.json_path.exists():
                self.json_path.unlink()
            if self.checkpoint_path.exists():
                self.checkpoint_path.unlink()
            if self.history_log_path.exists():
                self.history_log_path.unlink()
            self.completed_files = set()
            self.current_chunk_id = 0
            self.all_chunks = []
        else:
            ckpt_files = self._load_checkpoint()
            hist_files = self._load_completed_from_history()
            self.completed_files = ckpt_files.union(hist_files)
            self.all_chunks = self._load_existing_chunks()
            self.current_chunk_id = max((c["chunk_id"] for c in self.all_chunks), default=0)

        self._out_f = open(self.jsonl_path, "a", encoding="utf-8")

    def _load_completed_from_history(self) -> set[str]:
        completed = set()
        if self.history_log_path.exists():
            with open(self.history_log_path, "r", encoding="utf-8") as f:
                for line in f:
                    m = re.search(r"COMPLETED:\s*([^\s|]+)", line)
                    if m:
                        completed.add(m.group(1).strip())
        return completed

    def _load_checkpoint(self) -> set[str]:
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return set(data.get("completed_files", []))
            except Exception:
                pass
        return set()

    def _save_checkpoint(self):
        with open(self.checkpoint_path, "w", encoding="utf-8") as f:
            json.dump({
                "completed_files": sorted(list(self.completed_files)),
                "total_chunks": self.current_chunk_id,
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=2)

    def _load_existing_chunks(self) -> list[dict]:
        chunks = []
        if self.jsonl_path.exists():
            with open(self.jsonl_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            chunks.append(json.loads(line))
                        except Exception:
                            pass
        return chunks

    def is_file_completed(self, file_key: str) -> bool:
        return file_key in self.completed_files

    def mark_file_completed(self, file_key: str):
        self.completed_files.add(file_key)
        self._save_checkpoint()
        self.sync_to_json()

        # Append to processing history log
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        chunk_count = len(self.current_file_chunks)
        if chunk_count > 0:
            first_id = self.current_file_chunks[0]["chunk_id"]
            last_id = self.current_file_chunks[-1]["chunk_id"]
            total_words = sum(c["word_count"] for c in self.current_file_chunks)
            log_line = f"[{timestamp}] COMPLETED: {file_key:<55} | Chunks: {chunk_count:3d} (IDs: #{first_id:04d}-#{last_id:04d}) | Words: {total_words:6,d}\n"
        else:
            log_line = f"[{timestamp}] COMPLETED: {file_key:<55} | Chunks:   0 | Words:      0\n"

        with open(self.history_log_path, "a", encoding="utf-8") as hf:
            hf.write(log_line)
            hf.flush()

        self.current_file_chunks = []

    def add_chunk(self, source_file: str, chapter: str, title: str, text: str,
                  level: int = 1, page_start: int = None, page_end: int = None) -> dict:
        self.current_chunk_id += 1
        words = text.split()
        chunk = {
            "chunk_id": self.current_chunk_id,
            "source_file": source_file,
            "chapter": chapter,
            "title": title,
            "level": level,
            "page_start": page_start,
            "page_end": page_end,
            "word_count": len(words),
            "text": text
        }
        self.all_chunks.append(chunk)
        self.current_file_chunks.append(chunk)
        self._out_f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        self._out_f.flush()
        os.fsync(self._out_f.fileno())
        return chunk

    def sync_to_json(self):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.all_chunks, f, indent=2, ensure_ascii=False)

    def close(self):
        if not self._out_f.closed:
            self._out_f.close()
        self.sync_to_json()
        self._save_checkpoint()

def process_section_text(title: str, category: str, raw_text: str, source_file: str,
                         splitter, delay: float, rechunk_all: bool,
                         stream_mgr: ChunkStreamManager, level: int = 1,
                         page_start: int = None, page_end: int = None,
                         full_md_lines: list[str] = None):
    words = raw_text.split()
    if len(words) < 15:
        return

    if not rechunk_all and len(words) <= MAX_CHUNK_WORDS:
        chunk = stream_mgr.add_chunk(
            source_file=source_file,
            chapter=category,
            title=title,
            text=raw_text,
            level=level,
            page_start=page_start,
            page_end=page_end
        )
        print(f"  [Chunk {chunk['chunk_id']:03d}] Saved atomic: '{title}' ({len(words)} words)")
        if full_md_lines is not None:
            heading = "#" * min(level + 1, 6)
            full_md_lines.append(f"\n{heading} {title}\n*(Source: {source_file} | Chapter: {category})*\n\n{raw_text}\n")
        return

    # Requires semantic line-break splitting
    sub_slices = []
    if splitter:
        print(f"  [Semantic Split] Analyzing '{title}' ({len(words)} words) with Gemini...")
        sys.stdout.flush()
        try:
            sec_input = " ".join(words[:1800])
            pred = run_splitter_with_backoff(
                splitter,
                section_title=title,
                category=category,
                section_text=sec_input
            )
            if pred.breaks:
                print(f"    -> Identified {len(pred.breaks)} verbatim line break anchors:")
                for b in pred.breaks:
                    print(f"       * [{b.subtopic_title}] -> '{b.break_line_verbatim[:45]}...'")
                sys.stdout.flush()
                sub_slices = split_by_verbatim_lines(raw_text, pred.breaks, title)
            if delay > 0:
                time.sleep(delay)
        except Exception as e:
            print(f"    -> Warning during semantic splitting of '{title}': {e}")
            sys.stdout.flush()

    if not sub_slices or len(sub_slices) <= 1:
        fb_parts = mechanical_paragraph_fallback(raw_text, max_words=MAX_CHUNK_WORDS)
        sub_slices = [(f"{title} (Part {idx})", pt) for idx, pt in enumerate(fb_parts, 1)]

    bounded_slices = ensure_bounded_slices(sub_slices, max_words=MAX_CHUNK_WORDS)
    for sub_title, sub_text in bounded_slices:
        sub_words = len(sub_text.split())
        chunk = stream_mgr.add_chunk(
            source_file=source_file,
            chapter=category,
            title=sub_title,
            text=sub_text,
            level=level,
            page_start=page_start,
            page_end=page_end
        )
        print(f"  [Chunk {chunk['chunk_id']:03d}] Saved split slice: '{sub_title}' ({sub_words} words)")
        if full_md_lines is not None:
            heading = "#" * min(level + 1, 6)
            full_md_lines.append(f"\n{heading} {sub_title}\n*(Source: {source_file} | Chapter: {category})*\n\n{sub_text}\n")

def process_pdf_file(pdf_path: Path, rel_path: str, splitter, delay: float, rechunk_all: bool,
                     stream_mgr: ChunkStreamManager, full_md_lines: list[str]):
    print(f"\n[Processing PDF] {rel_path}...")
    doc = pymupdf.open(pdf_path)
    toc = doc.get_toc()

    if toc:
        current_chapter = pdf_path.stem.replace("_", " ").title()
        for i, entry in enumerate(toc):
            level, title, start_page_1idx = entry
            start_page = max(0, start_page_1idx - 1)
            end_page = max(start_page + 1, toc[i + 1][2] - 1) if i + 1 < len(toc) else len(doc)

            if level == 1:
                current_chapter = title

            text_parts = []
            for p in range(start_page, min(end_page, len(doc))):
                cleaned = clean_page_text(doc[p].get_text())
                if cleaned:
                    text_parts.append(cleaned)

            raw_text = "\n\n".join(text_parts).strip()
            process_section_text(
                title=title,
                category=current_chapter,
                raw_text=raw_text,
                source_file=rel_path,
                splitter=splitter,
                delay=delay,
                rechunk_all=rechunk_all,
                stream_mgr=stream_mgr,
                level=level,
                page_start=start_page + 1,
                page_end=end_page,
                full_md_lines=full_md_lines
            )
    else:
        # Fallback if no TOC
        text_parts = [clean_page_text(p.get_text()) for p in doc]
        full_text = "\n\n".join([t for t in text_parts if t]).strip()
        process_section_text(
            title=pdf_path.stem.replace("_", " ").title(),
            category=pdf_path.stem.replace("_", " ").title(),
            raw_text=full_text,
            source_file=rel_path,
            splitter=splitter,
            delay=delay,
            rechunk_all=rechunk_all,
            stream_mgr=stream_mgr,
            level=1,
            full_md_lines=full_md_lines
        )

def parse_markdown_sections(text: str, default_title: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    sections = []
    current_title = default_title
    current_lines = []

    for line in lines:
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            if current_lines:
                sec_text = "\n".join(current_lines).strip()
                if sec_text:
                    sections.append((current_title, sec_text))
                current_lines = []
            current_title = m.group(2).strip()
        else:
            current_lines.append(line)

    if current_lines:
        sec_text = "\n".join(current_lines).strip()
        if sec_text:
            sections.append((current_title, sec_text))

    return sections if sections else [(default_title, text)]

def parse_text_sections(text: str, default_title: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    sections = []
    current_title = default_title
    current_lines = []

    for line in lines:
        stripped = line.strip()
        # Look for section headers like "1 Introduction" or "2.3 Diffie-Hellman"
        m = re.match(r"^([0-9]+(\.[0-9]+)*)\s+([A-Z][A-Za-z0-9\s,\-:]+)$", stripped)
        if m and len(stripped) < 80:
            if current_lines:
                sec_text = "\n".join(current_lines).strip()
                if sec_text:
                    sections.append((current_title, sec_text))
                current_lines = []
            current_title = f"{m.group(1)} {m.group(3)}"
        else:
            current_lines.append(line)

    if current_lines:
        sec_text = "\n".join(current_lines).strip()
        if sec_text:
            sections.append((current_title, sec_text))

    return sections if sections else [(default_title, text)]

def parse_scm_file(content: str, default_title: str) -> list[tuple[str, str]]:
    """Parse S-expression files into protocol and skeleton blocks."""
    # Try splitting on top-level (defprotocol or (defskeleton
    blocks = re.split(r'\n(?=\((?:defprotocol|defskeleton)\s+)', content)
    clean_blocks = [b.strip() for b in blocks if b.strip()]
    if len(clean_blocks) > 1:
        sections = []
        for b in clean_blocks:
            m = re.match(r'^\((defprotocol|defskeleton)\s+([^\s\)]+)', b)
            if m:
                block_type, block_name = m.groups()
                sections.append((f"{block_name} ({block_type})", b))
            else:
                sections.append((default_title, b))
        return sections
    return [(default_title, content)]

def discover_corpus_files(search_dirs: list[Path]) -> list[Path]:
    """Recursively discover all scannable files in the search directories."""
    discovered = []
    for d in search_dirs:
        if not d.exists():
            continue
        for p in sorted(d.rglob("*")):
            if not p.is_file():
                continue
            if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if p.name in EXCLUDE_FILENAMES:
                continue
            # Skip papers_pdf because we already converted papers to text in guides_markdown
            if "papers_pdf" in p.parts and p.suffix.lower() == ".pdf":
                continue
            discovered.append(p)
    return discovered

def process_file(file_path: Path, splitter, delay: float, rechunk_all: bool,
                 stream_mgr: ChunkStreamManager, full_md_lines: list[str]):
    try:
        rel_path = str(file_path.relative_to(BASE_DIR))
    except ValueError:
        rel_path = file_path.name

    if stream_mgr.is_file_completed(rel_path):
        print(f"[Skip] Already completed in checkpoint: '{rel_path}'")
        return

    ext = file_path.suffix.lower()
    base_name = file_path.stem.replace("_", " ").title()

    if ext == ".pdf":
        process_pdf_file(
            pdf_path=file_path,
            rel_path=rel_path,
            splitter=splitter,
            delay=delay,
            rechunk_all=rechunk_all,
            stream_mgr=stream_mgr,
            full_md_lines=full_md_lines
        )
    elif ext == ".md":
        print(f"\n[Processing Markdown] {rel_path}...")
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        sections = parse_markdown_sections(content, default_title=base_name)
        for s_title, s_text in sections:
            process_section_text(
                title=s_title,
                category=base_name,
                raw_text=s_text,
                source_file=rel_path,
                splitter=splitter,
                delay=delay,
                rechunk_all=rechunk_all,
                stream_mgr=stream_mgr,
                level=2,
                full_md_lines=full_md_lines
            )
    elif ext == ".txt":
        print(f"\n[Processing Text] {rel_path}...")
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        sections = parse_text_sections(content, default_title=base_name)
        for s_title, s_text in sections:
            process_section_text(
                title=s_title,
                category=base_name,
                raw_text=s_text,
                source_file=rel_path,
                splitter=splitter,
                delay=delay,
                rechunk_all=rechunk_all,
                stream_mgr=stream_mgr,
                level=2,
                full_md_lines=full_md_lines
            )
    elif ext == ".scm":
        content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
        if len(content.split()) >= 15:
            sections = parse_scm_file(content, default_title=f"Protocol: {file_path.name}")
            for s_title, s_text in sections:
                process_section_text(
                    title=s_title,
                    category="Reference SCM Models",
                    raw_text=s_text,
                    source_file=rel_path,
                    splitter=splitter,
                    delay=delay,
                    rechunk_all=rechunk_all,
                    stream_mgr=stream_mgr,
                    level=3,
                    full_md_lines=full_md_lines
                )

    stream_mgr.mark_file_completed(rel_path)
    print(f"[Completed] File '{rel_path}'. Total chunks so far: {stream_mgr.current_chunk_id}")

def main():
    parser = argparse.ArgumentParser(description="Unified recursive semantic chunker for the CPSA corpus.")
    parser.add_argument("--dir", "-d", type=str, default=None,
                        help="Target directory to scan (defaults to refrences/manual and refrences/internet).")
    parser.add_argument("--file", "-f", type=str, default=None,
                        help="Process a single specific file path.")
    parser.add_argument("--semantic-split", action="store_true",
                        help="Use Gemini 3.1 Flash Lite to find exact thematic line breaks for sections > 750 words.")
    parser.add_argument("--rechunk-all", action="store_true",
                        help="Run semantic line-break splitter on all sections > 150 words.")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL,
                        help=f"Model identifier (e.g. gemini/gemini-3.1-flash-lite). Default: {DEFAULT_MODEL}")
    parser.add_argument("--api-key", type=str, default=DEFAULT_API_KEY,
                        help="Gemini API key (defaults to GEMINI_API_KEY from .env).")
    parser.add_argument("--api-base", type=str, default=DEFAULT_API_BASE,
                        help=f"Ollama API base URL. Default: {DEFAULT_API_BASE}")
    parser.add_argument("--delay", type=float, default=None,
                        help="Pacing delay (seconds) between LLM calls. Default: 4.0s for Gemini, 0.0s for local.")
    parser.add_argument("--reprocess-all", action="store_true",
                        help="Clear checkpoint and reprocess all chunks from scratch.")
    args = parser.parse_args()

    splitter = None
    is_gemini = args.model.startswith("gemini") or "gemini" in args.model.lower()
    delay = args.delay if args.delay is not None else (4.0 if is_gemini else 0.0)

    if args.semantic_split or args.rechunk_all:
        if is_gemini:
            model_tag = args.model if args.model.startswith("gemini/") else f"gemini/{args.model}"
            api_key = args.api_key or os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                print("Error: GEMINI_API_KEY is required for Gemini models. Set it in .env or pass --api-key.", file=sys.stderr)
                sys.exit(1)
            os.environ["GEMINI_API_KEY"] = api_key
            print(f"Configuring Gemini 3.1 Flash Lite ('{model_tag}', delay: {delay}s) for exact line-break detection...")
            lm = dspy.LM(model_tag, api_key=api_key, temperature=0.1)
        else:
            clean_model = args.model
            for prefix in ["ollama_chat/", "ollama/"]:
                if clean_model.startswith(prefix):
                    clean_model = clean_model[len(prefix):]
            print(f"Connecting to Ollama at {args.api_base} with model '{clean_model}'...")
            lm = dspy.LM(f"ollama_chat/{clean_model}", api_base=args.api_base, api_key="", temperature=0.1)

        dspy.configure(lm=lm)
        splitter = dspy.Predict(FindExactThematicBreaks)

    stream_mgr = ChunkStreamManager(
        jsonl_path=CHUNKS_JSONL_PATH,
        json_path=CHUNKS_JSON_PATH,
        checkpoint_path=CHECKPOINT_PATH,
        reprocess_all=args.reprocess_all
    )

    full_md_lines = ["# Complete CPSA Reference Corpus (Clean Markdown)\n"]

    if args.file:
        target_path = Path(args.file).resolve()
        if not target_path.exists():
            print(f"Error: Target file '{target_path}' not found.", file=sys.stderr)
            sys.exit(1)
        all_files = [target_path]
    elif args.dir:
        search_dir = Path(args.dir).resolve()
        all_files = discover_corpus_files([search_dir])
    else:
        all_files = discover_corpus_files(DEFAULT_SEARCH_DIRS)

    print(f"\n========================================================")
    print(f"CPSA Recursive Semantic Component Chunker")
    print(f"  Discovered scannable files:    {len(all_files)}")
    print(f"  Existing chunks in database:   {len(stream_mgr.all_chunks)}")
    print(f"  Completed files in checkpoint: {len(stream_mgr.completed_files)}")
    print(f"  Semantic line-break splitting: {'ENABLED (Gemini 3.1 Flash Lite)' if splitter else 'DISABLED'}")
    print(f"========================================================\n")

    for f_path in all_files:
        process_file(
            file_path=f_path,
            splitter=splitter,
            delay=delay,
            rechunk_all=args.rechunk_all,
            stream_mgr=stream_mgr,
            full_md_lines=full_md_lines
        )

    stream_mgr.close()

    if len(full_md_lines) > 1:
        with open(CLEAN_MD_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(full_md_lines))
        print(f"\n[Saved] Consolidated clean markdown to {CLEAN_MD_PATH}")

    total = len(stream_mgr.all_chunks)
    print(f"\nFinished processing.")
    print(f"Total atomic semantic chunks: {total}")
    if total > 0:
        words = [c["word_count"] for c in stream_mgr.all_chunks]
        print(f"Word count: min={min(words)}, max={max(words)}, median={sorted(words)[total // 2]}")
    print(f"Chunks saved to:\n  - {CHUNKS_JSONL_PATH}\n  - {CHUNKS_JSON_PATH}")
    print(f"Checkpoint saved to:\n  - {CHECKPOINT_PATH}")

if __name__ == "__main__":
    main()
