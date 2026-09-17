#!/usr/bin/env python3
"""
01_extract_chunks.py
Uniform 1000-Word Block Semantic Decomposer for the CPSA Corpus.

Architecture:
- Ingests all scannable files (.pdf, .md, .txt, .scm) across refrences/ (manual & internet).
- Slices documents into cohesive ~1,000-word blocks at natural paragraph boundaries.
- Blocks <= 150 words (e.g. small .scm protocols) are preserved as atomic units.
- Blocks > 150 words are passed to Gemini 3.1 Flash Lite, which identifies natural
  thematic inflection points and returns exact verbatim first-sentence anchors.
- Python slices the text at exact line numbers matching those verbatim anchors,
  preserving 100% source text integrity without dropping or hallucinating words.
- Enriches every chunk with hierarchical context breadcrumbs.
- Real-time streaming persistence: writes immediately to manual_chunks.jsonl.
- Append-only history logging: updates processing_history.log on file completion.
- Re-run verification: checks processing_history.log and checkpoint.json to skip finished files.
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
HISTORY_LOG_PATH = CHUNKS_DIR / "processing_history.log"
CLEAN_MD_PATH = CHUNKS_DIR / "all_references_clean.md"

TARGET_BLOCK_WORDS = 1000
MIN_SPLIT_WORDS = 150
DEFAULT_MODEL = os.environ.get("MODEL_NAME", "gemini/gemini-3.1-flash-lite")
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt"}
EXCLUDE_FILENAMES = {
    "cpsa4manual.txt",       # Duplicate text of cpsa4manual.pdf
    "cpsa4manual_clean.md",  # Duplicate markdown
    "cpsa.cabal.txt",        # Packaging metadata
    "readme.md",             # Empty placeholder
    "manifest.json",         # Download manifest
}

class SemanticBoundary(BaseModel):
    concept_title: str = Field(description="Clear, descriptive title for this specific concept, rule, or mechanism.")
    first_sentence_verbatim: str = Field(description="The exact verbatim first sentence where this concept begins in the text.")

class SemanticBlockSplitter(dspy.Signature):
    """You are a formal methods expert and cryptographic protocol analyst.
Analyze the provided ~1000-word block of CPSA technical documentation.
Identify every distinct conceptual component, rule, protocol definition, algebraic operation, or diagnostic mechanism.
For each distinct component, output:
- concept_title: descriptive title of the sub-concept
- first_sentence_verbatim: the exact verbatim line/sentence from the text where it begins.
Do NOT alter, paraphrase, or invent words. Return exact verbatim lines as they appear in the text."""
    source_context: str = dspy.InputField(desc="File and block breadcrumb context")
    block_text: str = dspy.InputField(desc="Verbatim text of the block")
    boundaries: list[SemanticBoundary] = dspy.OutputField(desc="List of distinct concept boundaries with verbatim anchors")

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

def partition_into_paragraph_blocks(text: str, target_words: int = TARGET_BLOCK_WORDS, max_single_words: int = 1400) -> list[str]:
    """
    Split text into balanced ~1000-word blocks respecting clean paragraph boundaries.
    - If text <= max_single_words (e.g. 1200-1400 words), preserves as 1 unified block
      to give the LLM full document context and avoid awkward runt tails.
    - For larger texts, divides dynamically into k balanced blocks (e.g. 2300w -> 2 x 1150w).
    """
    raw_paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not raw_paras:
        return []

    words = text.split()
    total_words = len(words)
    if total_words <= max_single_words:
        return ["\n\n".join(raw_paras)]

    k = max(2, round(total_words / target_words))
    target_per_block = total_words // k

    blocks = []
    curr_paras = []
    curr_words = 0

    for p in raw_paras:
        p_words = len(p.split())
        if len(blocks) < k - 1 and curr_words + p_words > target_per_block and curr_paras:
            blocks.append("\n\n".join(curr_paras))
            curr_paras = [p]
            curr_words = p_words
        else:
            curr_paras.append(p)
            curr_words += p_words

    if curr_paras:
        blocks.append("\n\n".join(curr_paras))

    return blocks

def clip_block_by_anchors(block_text: str, boundaries: list[SemanticBoundary], base_title: str) -> list[dict]:
    """Clip a text block at exact line numbers matching the verbatim anchors."""
    if not boundaries:
        return [{"title": base_title, "text": block_text}]

    lines = block_text.splitlines()
    split_indices = []
    titles = []

    for b in boundaries:
        anchor = b.first_sentence_verbatim.strip().lower()
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
            titles.append(b.concept_title)

    if not split_indices:
        return [{"title": base_title, "text": block_text}]

    slices = []
    prepend_to_first = ""

    # Handle text preceding the first boundary
    if split_indices[0] > 0:
        head_text = "\n".join(lines[0:split_indices[0]]).strip()
        if len(head_text.split()) < 25:
            # Prepend small header to the first slice instead of creating an orphan chunk
            prepend_to_first = head_text + "\n\n"
        else:
            slices.append({"title": f"{base_title} (Intro)", "text": head_text})

    for i in range(len(split_indices)):
        start = split_indices[i]
        end = split_indices[i + 1] if i + 1 < len(split_indices) else len(lines)
        slice_text = "\n".join(lines[start:end]).strip()
        if i == 0 and prepend_to_first:
            slice_text = prepend_to_first + slice_text
        slices.append({"title": titles[i], "text": slice_text})
    raw_slices = slices if slices else [{"title": base_title, "text": block_text}]
    return ensure_minimum_chunk_floor(raw_slices, min_words=60)

def ensure_minimum_chunk_floor(slices: list[dict], min_words: int = 60) -> list[dict]:
    """Merge undersized slices (< 60 words) into adjacent slices to prevent over-fragmentation."""
    if len(slices) <= 1:
        return slices

    merged = []
    curr = None
    for s in slices:
        w_count = len(s["text"].split())
        if curr is None:
            curr = dict(s)
        elif len(curr["text"].split()) < min_words:
            curr["title"] = f"{curr['title']} / {s['title']}"
            curr["text"] = f"{curr['text']}\n\n{s['text']}"
        elif w_count < min_words:
            curr["title"] = f"{curr['title']} / {s['title']}"
            curr["text"] = f"{curr['text']}\n\n{s['text']}"
        else:
            merged.append(curr)
            curr = dict(s)

    if curr:
        if merged and len(curr["text"].split()) < min_words:
            merged[-1]["title"] = f"{merged[-1]['title']} / {curr['title']}"
            merged[-1]["text"] = f"{merged[-1]['text']}\n\n{curr['text']}"
        else:
            merged.append(curr)

    return merged

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
    """Manages streaming append of chunks, history logging, and checkpoint tracking."""
    def __init__(self, jsonl_path: Path, json_path: Path, checkpoint_path: Path,
                 history_log_path: Path, reprocess_all: bool = False):
        self.jsonl_path = jsonl_path
        self.json_path = json_path
        self.checkpoint_path = checkpoint_path
        self.history_log_path = history_log_path
        self.jsonl_path.parent.mkdir(parents=True, exist_ok=True)
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

    def add_chunk(self, source_file: str, breadcrumb: str, title: str, text: str) -> dict:
        self.current_chunk_id += 1
        words = text.split()
        chunk = {
            "chunk_id": self.current_chunk_id,
            "chunk_type": "documentation",
            "source_file": source_file,
            "breadcrumb": breadcrumb,
            "title": title,
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

def process_document_text(full_text: str, source_file: str, splitter, delay: float,
                          stream_mgr: ChunkStreamManager, full_md_lines: list[str] = None):
    words = full_text.split()
    total_words = len(words)
    if total_words < 15:
        return

    file_title = Path(source_file).stem.replace("_", " ").title()
    is_scm = Path(source_file).suffix.lower() == ".scm"

    # For .scm code files <= 1000 words, preserve as 1 complete atomic protocol model
    # For prose/guides, preserve <= 150 words directly as 1 atomic chunk
    if (is_scm and total_words <= TARGET_BLOCK_WORDS) or total_words <= MIN_SPLIT_WORDS or not splitter:
        breadcrumb = f"{file_title} > Complete Protocol" if is_scm else f"{file_title} > Overview"
        chunk = stream_mgr.add_chunk(
            source_file=source_file,
            breadcrumb=breadcrumb,
            title=file_title,
            text=full_text
        )
        print(f"  [Chunk {chunk['chunk_id']:04d}] Saved atomic ({total_words} words): '{file_title}'")
        if full_md_lines is not None:
            full_md_lines.append(f"\n## {file_title}\n*({breadcrumb})*\n\n{full_text}\n")
        return

    # Slices document into cohesive ~1000-word paragraph blocks
    blocks = partition_into_paragraph_blocks(full_text, target_words=TARGET_BLOCK_WORDS)
    total_blocks = len(blocks)

    for b_idx, block_text in enumerate(blocks, 1):
        b_words = len(block_text.split())
        block_breadcrumb = f"{file_title} > Block {b_idx}/{total_blocks}"

        # If block is small, keep as-is
        if b_words <= MIN_SPLIT_WORDS:
            chunk = stream_mgr.add_chunk(
                source_file=source_file,
                breadcrumb=block_breadcrumb,
                title=f"{file_title} (Part {b_idx})",
                text=block_text
            )
            print(f"  [Chunk {chunk['chunk_id']:04d}] Saved atomic ({b_words} words): '{chunk['title']}'")
            continue

        # Send ~1000-word block to Gemini 3.1 Flash Lite for semantic boundary detection
        boundaries = []
        try:
            print(f"  [Semantic Split] Block {b_idx}/{total_blocks} ({b_words} words) -> Gemini 3.1 Flash Lite...")
            sys.stdout.flush()
            pred = run_splitter_with_backoff(
                splitter,
                source_context=block_breadcrumb,
                block_text=block_text
            )
            boundaries = pred.boundaries or []
            if boundaries:
                print(f"    -> Detected {len(boundaries)} semantic concepts:")
                for b in boundaries:
                    print(f"       * [{b.concept_title}]")
                sys.stdout.flush()
            if delay > 0:
                time.sleep(delay)
        except Exception as e:
            print(f"    -> Splitter warning for {block_breadcrumb}: {e}", file=sys.stderr)
            sys.stdout.flush()

        # Clip the block text at exact line numbers matching verbatim anchors
        slices = clip_block_by_anchors(block_text, boundaries, base_title=f"{file_title} (Part {b_idx})")

        for s in slices:
            sub_title = s["title"]
            sub_text = s["text"]
            sub_words = len(sub_text.split())
            chunk_breadcrumb = f"{file_title} > {sub_title}"

            chunk = stream_mgr.add_chunk(
                source_file=source_file,
                breadcrumb=chunk_breadcrumb,
                title=sub_title,
                text=sub_text
            )
            print(f"  [Chunk {chunk['chunk_id']:04d}] Saved slice ({sub_words} words): '{sub_title}'")

            if full_md_lines is not None:
                full_md_lines.append(f"\n### {sub_title}\n*({chunk_breadcrumb})*\n\n{sub_text}\n")

def read_file_content(file_path: Path) -> str:
    """Read content according to file type."""
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        doc = pymupdf.open(file_path)
        pages_text = [clean_page_text(p.get_text()) for p in doc]
        return "\n\n".join([t for t in pages_text if t]).strip()
    else:
        return file_path.read_text(encoding="utf-8", errors="ignore").strip()

def discover_corpus_files(search_dirs: list[Path]) -> list[Path]:
    """Recursively discover all scannable files in search directories."""
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

def process_file(file_path: Path, splitter, delay: float,
                 stream_mgr: ChunkStreamManager, full_md_lines: list[str]):
    try:
        rel_path = str(file_path.relative_to(BASE_DIR))
    except ValueError:
        rel_path = file_path.name

    if stream_mgr.is_file_completed(rel_path):
        print(f"[Skip] Already completed in history/checkpoint: '{rel_path}'")
        return

    print(f"\n========================================================")
    print(f"[Processing] {rel_path}")
    print(f"========================================================")
    sys.stdout.flush()

    content = read_file_content(file_path)
    process_document_text(
        full_text=content,
        source_file=rel_path,
        splitter=splitter,
        delay=delay,
        stream_mgr=stream_mgr,
        full_md_lines=full_md_lines
    )

    stream_mgr.mark_file_completed(rel_path)
    print(f"[Completed] '{rel_path}' -> Total chunks in DB: {stream_mgr.current_chunk_id}")

def main():
    parser = argparse.ArgumentParser(description="Uniform 1000-word block semantic chunker for CPSA.")
    parser.add_argument("--dir", "-d", type=str, default=None,
                        help="Target directory to scan (defaults to refrences/manual and refrences/internet).")
    parser.add_argument("--file", "-f", type=str, default=None,
                        help="Process a single specific file path.")
    parser.add_argument("--no-llm", action="store_true",
                        help="Disable Gemini LLM; slice strictly at 1000-word paragraph boundaries.")
    parser.add_argument("--semantic-split", action="store_true", default=True,
                        help="Enable semantic line-break splitting (default: True, kept for compatibility).")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL,
                        help=f"Model identifier (e.g. gemini/gemini-3.1-flash-lite). Default: {DEFAULT_MODEL}")
    parser.add_argument("--api-key", type=str, default=DEFAULT_API_KEY,
                        help="Gemini API key (defaults to GEMINI_API_KEY from .env).")
    parser.add_argument("--api-base", type=str, default=DEFAULT_API_BASE,
                        help=f"Ollama API base URL. Default: {DEFAULT_API_BASE}")
    parser.add_argument("--delay", type=float, default=None,
                        help="Pacing delay (seconds) between LLM calls. Default: 3.5s for Gemini, 0.0s for local.")
    parser.add_argument("--reprocess-all", action="store_true",
                        help="Clear checkpoint and history log to reprocess all chunks from scratch.")
    args = parser.parse_args()

    splitter = None
    is_gemini = args.model.startswith("gemini") or "gemini" in args.model.lower()
    delay = args.delay if args.delay is not None else (3.5 if is_gemini else 0.0)

    if not args.no_llm:
        if is_gemini:
            model_tag = args.model if args.model.startswith("gemini/") else f"gemini/{args.model}"
            api_key = args.api_key or os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                print("Error: GEMINI_API_KEY is required for Gemini models. Set it in .env or pass --api-key.", file=sys.stderr)
                sys.exit(1)
            os.environ["GEMINI_API_KEY"] = api_key
            print(f"Configuring Gemini 3.1 Flash Lite ('{model_tag}', delay: {delay}s) for 1000-word block splitting...")
            lm = dspy.LM(model_tag, api_key=api_key, temperature=0.1)
        else:
            clean_model = args.model
            for prefix in ["ollama_chat/", "ollama/"]:
                if clean_model.startswith(prefix):
                    clean_model = clean_model[len(prefix):]
            print(f"Connecting to Ollama at {args.api_base} with model '{clean_model}'...")
            lm = dspy.LM(f"ollama_chat/{clean_model}", api_base=args.api_base, api_key="", temperature=0.1)

        dspy.configure(lm=lm)
        splitter = dspy.Predict(SemanticBlockSplitter)

    stream_mgr = ChunkStreamManager(
        jsonl_path=CHUNKS_JSONL_PATH,
        json_path=CHUNKS_JSON_PATH,
        checkpoint_path=CHECKPOINT_PATH,
        history_log_path=HISTORY_LOG_PATH,
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
    print(f"CPSA 1000-Word Block Semantic Decomposer")
    print(f"  Discovered scannable files:    {len(all_files)}")
    print(f"  Existing chunks in database:   {len(stream_mgr.all_chunks)}")
    print(f"  Completed files recognized:    {len(stream_mgr.completed_files)}")
    print(f"  Target block size:             ~{TARGET_BLOCK_WORDS} words")
    print(f"  Semantic line-break splitting: {'ENABLED (Gemini 3.1 Flash Lite)' if splitter else 'DISABLED'}")
    print(f"========================================================\n")

    for f_path in all_files:
        process_file(
            file_path=f_path,
            splitter=splitter,
            delay=delay,
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
    print(f"History log saved to:\n  - {HISTORY_LOG_PATH}")
    print(f"Checkpoint saved to:\n  - {CHECKPOINT_PATH}")

if __name__ == "__main__":
    main()
