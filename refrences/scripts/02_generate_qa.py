#!/usr/bin/env python3
"""
02_generate_qa.py
Sequentially processes manual chunks through DSPy one at a time.
Keeps the Ollama model warm in memory (keep_alive: -1).
Prints the current chunk being processed and the questions generated from the previous chunk.
"""

import os
import sys
import json
import time
import argparse
import urllib.request
from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field
import dspy
import backoff
from dotenv import load_dotenv, find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
# Load environment variables (.env in refrences/ or project root)
load_dotenv(find_dotenv(usecwd=True))
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

CHUNKS_PATH = BASE_DIR / "chunks" / "manual_chunks.json"
QA_JSONL_PATH = BASE_DIR / "dataset" / "manual_qa_dataset.jsonl"
QA_JSON_PATH = BASE_DIR / "dataset" / "manual_qa_dataset.json"

DEFAULT_MODEL = os.environ.get("MODEL_NAME", "gemini/gemini-3.5-flash-lite")
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

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
def run_extractor_with_backoff(extractor, **kwargs):
    return extractor(**kwargs)

class QAPair(BaseModel):
    question: str = Field(description="A specific, technically precise question about CPSA concepts, syntax, rules, or diagnostics.")
    answer: str = Field(description="A detailed, factual answer derived strictly and exclusively from the text.")
    category: Literal[
        "syntax", 
        "algebra", 
        "modeling_rule", 
        "adversary_assumption", 
        "skeleton_goal", 
        "troubleshooting", 
        "general_concept"
    ] = Field(description="Functional category.")
    key_terms: list[str] = Field(description="CPSA keywords or symbols involved.")

class ExtractManualQA(dspy.Signature):
    """You are a formal methods expert compiling an authoritative, exhaustive Q&A database from the CPSA 4 manual.
Extract exhaustive, technically precise question-answer pairs derived strictly and exclusively from the provided manual chunk.
Do not hallucinate external knowledge or general cryptographic facts not in the text.
Generate approximately target_qa_count questions covering all distinct rules, keywords, parameters, and diagnostics.

Return a JSON object containing a "qa_pairs" array. Each item in "qa_pairs" must have:
- "question": string (a specific, technically precise question about CPSA concepts, syntax, rules, or diagnostics)
- "answer": string (a detailed, factual answer derived strictly and exclusively from the text)
- "category": string (one of: syntax, algebra, modeling_rule, adversary_assumption, skeleton_goal, troubleshooting, general_concept)
- "key_terms": list of strings (CPSA keywords or symbols involved)
"""
    chapter_title: str = dspy.InputField(desc="The chapter this section belongs to.")
    section_title: str = dspy.InputField(desc="Title of this specific section.")
    target_qa_count: int = dspy.InputField(desc="Target number of distinct Q&A pairs to generate.")
    chunk_text: str = dspy.InputField(desc="The verbatim text of this manual section.")
    qa_pairs: list[QAPair] = dspy.OutputField(desc="List of objects, each with exact keys question, answer, category, key_terms")

def preload_model_in_vram(model_name: str, api_base: str):
    """Ensure Ollama loads the model into VRAM and keeps it resident indefinitely."""
    clean_model = model_name
    for prefix in ["ollama_chat/", "ollama/"]:
        if clean_model.startswith(prefix):
            clean_model = clean_model[len(prefix):]
    url = f"{api_base}/api/generate"
    payload = json.dumps({"model": clean_model, "keep_alive": -1}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp.read()
    except Exception as e:
        print(f"Warning: Failed to preload model in Ollama: {e}", file=sys.stderr)

def load_processed_data() -> tuple[set[int], dict[int, list[str]]]:
    """Load previously completed chunk IDs and their generated questions."""
    processed_ids = set()
    last_questions = {}
    if QA_JSONL_PATH.exists():
        with open(QA_JSONL_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        cid = record["chunk_id"]
                        processed_ids.add(cid)
                        last_questions[cid] = [qa["question"] for qa in record.get("qa_pairs", [])]
                    except Exception:
                        pass
    return processed_ids, last_questions

def sync_jsonl_to_json():
    """Consolidate JSONL into formatted JSON file."""
    if not QA_JSONL_PATH.exists():
        return
    records = []
    with open(QA_JSONL_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
    with open(QA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive Q&A dataset from CPSA manual chunks.")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help=f"Model identifier (Gemini or Ollama). Default: {DEFAULT_MODEL}")
    parser.add_argument("--api-key", type=str, default=DEFAULT_API_KEY, help="API key for Gemini (defaults to GEMINI_API_KEY from .env).")
    parser.add_argument("--api-base", type=str, default=DEFAULT_API_BASE, help=f"API base URL for Ollama. Default: {DEFAULT_API_BASE}")
    parser.add_argument("--delay", type=float, default=None, help="Pacing delay (seconds) between LLM calls. Default: 4.2s for Gemini, 0.0s for Ollama.")
    parser.add_argument("--reprocess-all", action="store_true", help="Reprocess all chunks from scratch, overwriting existing dataset.")
    args = parser.parse_args()

    if not CHUNKS_PATH.exists():
        print(f"Error: {CHUNKS_PATH} does not exist.", file=sys.stderr)
        sys.exit(1)

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        all_chunks = json.load(f)

    total_chunks = len(all_chunks)

    is_gemini = args.model.startswith("gemini") or "gemini" in args.model.lower()
    delay = args.delay if args.delay is not None else (4.2 if is_gemini else 0.0)

    if is_gemini:
        model_tag = args.model if args.model.startswith("gemini/") else f"gemini/{args.model}"
        api_key = args.api_key or os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            print("Error: GEMINI_API_KEY is required for Gemini models. Set it in .env or pass --api-key.", file=sys.stderr)
            sys.exit(1)
        os.environ["GEMINI_API_KEY"] = api_key
        print(f"Connecting to Gemini via LiteLLM using model '{model_tag}' (delay: {delay}s)...")
        lm = dspy.LM(model_tag, api_key=api_key, temperature=0.2)
    else:
        clean_model = args.model
        for prefix in ["ollama_chat/", "ollama/"]:
            if clean_model.startswith(prefix):
                clean_model = clean_model[len(prefix):]
        print(f"Preloading and pinning '{clean_model}' in GPU memory via Ollama at {args.api_base} (keep_alive: Forever)...")
        preload_model_in_vram(clean_model, args.api_base)
        lm = dspy.LM(
            f"ollama_chat/{clean_model}",
            api_base=args.api_base,
            api_key="",
            temperature=0.2,
            extra_body={"keep_alive": -1}
        )
    dspy.configure(lm=lm)
    extractor = dspy.Predict(ExtractManualQA)

    if args.reprocess_all:
        processed_ids = set()
        historical_questions = {}
        open_mode = "w"
    else:
        processed_ids, historical_questions = load_processed_data()
        open_mode = "a"

    previous_chunk_info = None

    # If some chunks were already processed, grab the most recent one for the initial log
    if processed_ids:
        last_id = max(processed_ids)
        if last_id in historical_questions:
            last_chunk_title = next((c["title"] for c in all_chunks if c["chunk_id"] == last_id), f"Chunk {last_id}")
            previous_chunk_info = (last_id, last_chunk_title, historical_questions[last_id])

    QA_JSONL_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(QA_JSONL_PATH, open_mode, encoding="utf-8") as out_f:
        for chunk in all_chunks:
            chunk_id = chunk["chunk_id"]
            if chunk_id in processed_ids:
                continue

            title = chunk["title"]
            chapter = chunk["chapter"]
            text = chunk["text"]
            word_count = chunk.get("word_count", len(text.split()))
            target_qa = max(4, min(10, word_count // 90))

            # Terminal Display: Current chunk and previous chunk's questions
            print("\n" + "=" * 70)
            if previous_chunk_info:
                p_id, p_title, p_questions = previous_chunk_info
                print(f"Questions Generated from Previous Chunk [{p_id}/{total_chunks}] - '{p_title}':")
                for q_idx, q_text in enumerate(p_questions, 1):
                    print(f"  {q_idx}. {q_text}")
                print("-" * 70)

            print(f"CURRENTLY PROCESSING CHUNK [{chunk_id}/{total_chunks}]")
            print(f"  Title:      {title}")
            print(f"  Chapter:    {chapter}")
            print(f"  Word Count: {word_count} words (Target: ~{target_qa} questions)")
            print("=" * 70)
            sys.stdout.flush()

            try:
                pred = run_extractor_with_backoff(
                    extractor,
                    chapter_title=chapter,
                    section_title=title,
                    target_qa_count=target_qa,
                    chunk_text=text
                )

                qa_list = [qa.model_dump() for qa in pred.qa_pairs] if pred.qa_pairs else []
                record = {
                    "chunk_id": chunk_id,
                    "chapter": chapter,
                    "title": title,
                    "target_qa_count": target_qa,
                    "page_range": [chunk.get("page_start"), chunk.get("page_end")],
                    "qa_pairs": qa_list,
                    "count": len(qa_list)
                }

                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
                out_f.flush()
                sync_jsonl_to_json()

                if delay > 0:
                    time.sleep(delay)

                generated_questions = [qa["question"] for qa in qa_list]
                previous_chunk_info = (chunk_id, title, generated_questions)

            except Exception as e:
                print(f"Error processing chunk [{chunk_id}/{total_chunks}]: {e}", file=sys.stderr)

    # Print final chunk's questions at completion
    if previous_chunk_info:
        p_id, p_title, p_questions = previous_chunk_info
        print("\n" + "=" * 70)
        print(f"Questions Generated from Final Chunk [{p_id}/{total_chunks}] - '{p_title}':")
        for q_idx, q_text in enumerate(p_questions, 1):
            print(f"  {q_idx}. {q_text}")
        print("=" * 70)

    print("\nAll chunks processed successfully. Dataset synchronized to manual_qa_dataset.json.")

if __name__ == "__main__":
    main()
