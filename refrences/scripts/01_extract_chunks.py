#!/usr/bin/env python3
"""
01_extract_chunks.py
Recursive Semantic Chunker:
- Sections <= 750 words: Preserved as atomic conceptual units.
- Sections > 750 words: Fed into DSPy Semantic Splitter to identify internal thematic
  inflection points (e.g. separating syntax errors from type errors), slicing them
  into pure, titled sub-concept chunks.
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from pydantic import BaseModel, Field
import pymupdf
import dspy
import backoff
from dotenv import load_dotenv, find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
# Load environment variables (.env in refrences/ or project root)
load_dotenv(find_dotenv(usecwd=True))
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

PDF_PATH = BASE_DIR / "manual" / "cpsa4manual.pdf"
CHUNKS_JSON_PATH = BASE_DIR / "chunks" / "manual_chunks.json"
CLEAN_MD_PATH = BASE_DIR / "manual" / "cpsa4manual_clean.md"

MAX_CHUNK_WORDS = 750
DEFAULT_MODEL = os.environ.get("MODEL_NAME", "gemini/gemini-3.5-flash-lite")
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

class ConceptBoundary(BaseModel):
    subtopic_title: str = Field(description="Descriptive title of this distinct sub-concept or mechanism.")
    first_sentence: str = Field(description="Verbatim first sentence of the paragraph where this sub-concept begins.")

class FindThematicBoundaries(dspy.Signature):
    """You are a formal methods expert analyzing a section of the CPSA 4 manual.
Identify natural thematic inflection points where the text shifts from one subtopic or mechanism to another.

Return a JSON object containing a "boundaries" array. Each item in "boundaries" must have:
- "subtopic_title": string (descriptive title of this distinct sub-concept or mechanism)
- "first_sentence": string (the exact verbatim sentence where this sub-concept begins in the text)
"""
    section_title: str = dspy.InputField()
    chapter: str = dspy.InputField()
    section_text: str = dspy.InputField()
    boundaries: list[ConceptBoundary] = dspy.OutputField(desc="List of objects, each with exact keys subtopic_title and first_sentence")

def clean_page_text(text: str) -> str:
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

def split_by_thematic_boundaries(text: str, boundaries: list[ConceptBoundary], base_title: str) -> list[tuple[str, str]]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not boundaries or len(boundaries) <= 1:
        return [(base_title, text)]

    slices = []
    current_title = boundaries[0].subtopic_title if boundaries else base_title
    current_paras = []

    boundary_idx = 1
    next_boundary_text = boundaries[boundary_idx].first_sentence.lower() if boundary_idx < len(boundaries) else None

    for p in paragraphs:
        p_clean = p.lower().replace("\n", " ")
        if next_boundary_text and next_boundary_text[:30] in p_clean:
            if current_paras:
                slices.append((f"{base_title} - {current_title}", "\n\n".join(current_paras)))
                current_paras = []
            current_title = boundaries[boundary_idx].subtopic_title
            boundary_idx += 1
            next_boundary_text = boundaries[boundary_idx].first_sentence.lower() if boundary_idx < len(boundaries) else None

        current_paras.append(p)

    if current_paras:
        slices.append((f"{base_title} - {current_title}", "\n\n".join(current_paras)))

    return slices if len(slices) > 1 else [(base_title, text)]

def mechanical_paragraph_fallback(text: str, max_words: int = MAX_CHUNK_WORDS) -> list[str]:
    paragraphs = text.split('\n\n')
    parts = []
    curr = []
    curr_w = 0
    for p in paragraphs:
        p_w = len(p.split())
        if curr_w + p_w > max_words and curr:
            parts.append('\n\n'.join(curr))
            curr = [p]
            curr_w = p_w
        else:
            curr.append(p)
            curr_w += p_w
    if curr:
        parts.append('\n\n'.join(curr))
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

def main():
    parser = argparse.ArgumentParser(description="Extract and semantically chunk CPSA manual.")
    parser.add_argument("--semantic-split", action="store_true", help="Use DSPy LLM to find semantic boundaries in sections > 750 words.")
    parser.add_argument("--rechunk-all", action="store_true", help="Run semantic splitter on all sections, including those under 750 words.")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help=f"Model identifier (Gemini or Ollama). Default: {DEFAULT_MODEL}")
    parser.add_argument("--api-key", type=str, default=DEFAULT_API_KEY, help="API key for Gemini (defaults to GEMINI_API_KEY from .env).")
    parser.add_argument("--api-base", type=str, default=DEFAULT_API_BASE, help=f"API base URL for Ollama. Default: {DEFAULT_API_BASE}")
    parser.add_argument("--delay", type=float, default=None, help="Pacing delay (seconds) between LLM calls. Default: 4.2s for Gemini, 0.0s for Ollama.")
    args = parser.parse_args()

    if not PDF_PATH.exists():
        print(f"Error: {PDF_PATH} does not exist.", file=sys.stderr)
        sys.exit(1)

    print(f"Opening {PDF_PATH}...")
    doc = pymupdf.open(PDF_PATH)
    toc = doc.get_toc()

    splitter = None
    is_gemini = args.model.startswith("gemini") or "gemini" in args.model.lower()
    delay = args.delay if args.delay is not None else (4.2 if is_gemini else 0.0)

    if args.semantic_split or args.rechunk_all:
        if is_gemini:
            model_tag = args.model if args.model.startswith("gemini/") else f"gemini/{args.model}"
            api_key = args.api_key or os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                print("Error: GEMINI_API_KEY is required for Gemini models. Set it in .env or pass --api-key.", file=sys.stderr)
                sys.exit(1)
            os.environ["GEMINI_API_KEY"] = api_key
            print(f"Connecting to Gemini via LiteLLM using model '{model_tag}' (delay: {delay}s)...")
            lm = dspy.LM(model_tag, api_key=api_key)
        else:
            clean_model = args.model
            for prefix in ["ollama_chat/", "ollama/"]:
                if clean_model.startswith(prefix):
                    clean_model = clean_model[len(prefix):]
            print(f"Connecting to local Ollama at {args.api_base} with model '{clean_model}' (keep_alive: Forever)...")
            lm = dspy.LM(
                f"ollama_chat/{clean_model}",
                api_base=args.api_base,
                api_key="",
                temperature=0.1,
                extra_body={"keep_alive": -1}
            )
        dspy.configure(lm=lm)
        splitter = dspy.Predict(FindThematicBoundaries)

    chunks = []
    chunk_id = 0
    current_chapter = "General"
    full_clean_md = ["# CPSA 4 Manual (Extracted Reference)\n"]

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
        words = raw_text.split()
        if len(words) < 25:
            continue

        if not args.rechunk_all and len(words) <= MAX_CHUNK_WORDS:
            # Atomic as-is
            chunk_id += 1
            chunks.append({
                "chunk_id": chunk_id,
                "title": title,
                "chapter": current_chapter,
                "level": level,
                "page_start": start_page + 1,
                "page_end": end_page,
                "word_count": len(words),
                "text": raw_text
            })
            heading_prefix = "#" * min(level + 1, 6)
            full_clean_md.append(f"\n{heading_prefix} {title}\n*(Chapter: {current_chapter})*\n\n{raw_text}\n")
        else:
            # Section requires semantic splitting
            sub_slices = []
            if splitter:
                print(f"[Semantic Split] Re-processing section: '{title}' ({len(words)} words) with LLM...")
                sys.stdout.flush()
                try:
                    sec_input = " ".join(words[:1800])
                    pred = run_splitter_with_backoff(splitter, section_title=title, chapter=current_chapter, section_text=sec_input)
                    if pred.boundaries:
                        print(f"  -> Found {len(pred.boundaries)} thematic boundaries:")
                        for b in pred.boundaries:
                            print(f"     * {b.subtopic_title}")
                        sys.stdout.flush()
                        sub_slices = split_by_thematic_boundaries(raw_text, pred.boundaries, title)
                    if delay > 0:
                        time.sleep(delay)
                except Exception as e:
                    print(f"  -> Error during semantic splitting of {title}: {e}")
                    sys.stdout.flush()

            if not sub_slices or len(sub_slices) <= 1:
                fb_parts = mechanical_paragraph_fallback(raw_text, max_words=MAX_CHUNK_WORDS)
                sub_slices = [(f"{title} (Part {idx})", pt) for idx, pt in enumerate(fb_parts, 1)]

            # Ensure all slices strictly obey max words
            bounded_slices = ensure_bounded_slices(sub_slices, max_words=MAX_CHUNK_WORDS)

            for sub_title, sub_text in bounded_slices:
                chunk_id += 1
                sub_words = len(sub_text.split())
                chunks.append({
                    "chunk_id": chunk_id,
                    "title": sub_title,
                    "chapter": current_chapter,
                    "level": level,
                    "page_start": start_page + 1,
                    "page_end": end_page,
                    "word_count": sub_words,
                    "text": sub_text
                })
                heading_prefix = "#" * min(level + 1, 6)
                full_clean_md.append(f"\n{heading_prefix} {sub_title}\n*(Chapter: {current_chapter})*\n\n{sub_text}\n")

    print(f"\nExtracted {len(chunks)} total chunks.")
    print(f"Word count range: {min(c['word_count'] for c in chunks)} - {max(c['word_count'] for c in chunks)} words.")
    print(f"Median word count: {sorted([c['word_count'] for c in chunks])[len(chunks)//2]} words.")

    with open(CHUNKS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"Saved catalog to {CHUNKS_JSON_PATH}")

    with open(CLEAN_MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(full_clean_md))
    print(f"Saved clean reference markdown to {CLEAN_MD_PATH}")

if __name__ == "__main__":
    main()
