#!/usr/bin/env python3
"""
Contextual Enrichment Engine for CPSA Technical Documentation Chunks.
Implements the Anthropic Contextual Retrieval technique combined with 
deterministic AST feature extraction for the 1,278 documentation chunks.
"""

import os
import sys
import json
import re
import asyncio
import time
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CHUNKS_PATH = ROOT_DIR / "refrences" / "chunks" / "manual_chunks.jsonl"
CACHE_PATH = ROOT_DIR / "refrences" / "chunks" / "context_headers_cache.json"
ENRICHED_PATH = ROOT_DIR / "refrences" / "chunks" / "manual_chunks_enriched.jsonl"
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(ENV_PATH)
import litellm

# Silence excessive LiteLLM logging
litellm.suppress_debug_info = True

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment or .env", file=sys.stderr)
    sys.exit(1)

MODEL_NAME = "gemini/gemini-3.1-flash-lite"
CONCURRENCY_LIMIT = 12

# Deterministic CPSA AST patterns
AST_PATTERNS = {
    "Forms": re.compile(r"\b(defprotocol|defrole|defskeleton|deflistener|defmacro|defrule|defgenrule)\b"),
    "Assumptions": re.compile(r"\b(non-orig|uniq-orig|pen-non-orig|uniq-gen|role_uniq)\b"),
    "Algebra Sorts": re.compile(r"\b(name|text|data|skey|akey|mesg|chan|locn)\b"),
    "Crypto Terms": re.compile(r"\b(enc|cat|hash|pubk|privk|invk|ltk)\b"),
    "Relations": re.compile(r"\b(send|recv|trace|prec|subsort|auth-test)\b")
}

def extract_ast_features(text: str) -> dict[str, list[str]]:
    """Deterministically extracts Scheme and CPSA syntax primitives from text."""
    features = {}
    for cat, pat in AST_PATTERNS.items():
        matches = sorted(list(set(pat.findall(text))))
        if matches:
            features[cat] = matches
    return features

def build_ast_summary(features: dict[str, list[str]]) -> str:
    if not features:
        return "None detected (prose/derivation)"
    parts = []
    for cat, items in features.items():
        parts.append(f"{cat}: {', '.join(items[:6])}")
    return " | ".join(parts)

SYSTEM_PROMPT = """You are a formal methods expert indexing the MITRE CPSA (Cryptographic Protocol Shapes Analyzer) documentation corpus.
Given the document metadata, detected syntax features, and chunk text, write strictly 1 to 2 concise sentences providing the global orienting context for this chunk.
State:
1. The exact document and structural section this chunk belongs to.
2. The specific protocol, algebraic sort, S-expression syntax rule, or formal verification theorem it defines.

Do NOT summarize the chunk. Output ONLY the 1-2 sentence orienting header."""

PROMPT_TEMPLATE = """Document: {source_file}
Breadcrumb: {breadcrumb}
Section Title: {title}
Detected Syntax Primitives: {ast_summary}

Chunk Text:
{text_snippet}

Context Header:"""

async def generate_header_with_retry(chunk: dict, sem: asyncio.Semaphore, max_retries: int = 5) -> str:
    source_file = chunk.get("source_file", chunk.get("doc_id", "Unknown Document"))
    breadcrumb = chunk.get("breadcrumb", "") or chunk.get("chapter", "")
    title = chunk.get("title", "")
    text = chunk.get("text", "")
    
    ast_features = extract_ast_features(text)
    ast_summary = build_ast_summary(ast_features)
    
    prompt = PROMPT_TEMPLATE.format(
        source_file=source_file,
        breadcrumb=breadcrumb,
        title=title,
        ast_summary=ast_summary,
        text_snippet=text[:1600]
    )
    
    for attempt in range(1, max_retries + 1):
        try:
            async with sem:
                resp = await litellm.acompletion(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    api_key=GEMINI_API_KEY
                )
                header = resp.choices[0].message.content.strip()
                # Clean up any quotes or markdown artifacts
                header = header.replace('"', '').strip()
                return header
        except Exception as e:
            wait_time = 2.0 ** attempt
            if attempt == max_retries:
                # Fallback to deterministic AST header on exhaustion
                return f"This chunk from {source_file} ({title}) details formal verification semantics involving {ast_summary}."
            await asyncio.sleep(wait_time)

async def main():
    print("=" * 80)
    print("CPSA DOCUMENTATION CHUNK CONTEXTUAL ENRICHMENT PIPELINE")
    print("Model: Gemini 3.1 Flash Lite | Concurrency: 12")
    print("=" * 80)
    
    # 1. Load chunks
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        all_chunks = [json.loads(line) for line in f if line.strip()]
    
    doc_chunks = [c for c in all_chunks if c.get("chunk_type") != "code_example" and not c.get("is_code", False)]
    code_chunks = [c for c in all_chunks if c.get("chunk_type") == "code_example" or c.get("is_code", False)]
    
    print(f"Loaded {len(all_chunks)} total chunks:")
    print(f"  • Documentation chunks to enrich: {len(doc_chunks)}")
    print(f"  • Code model chunks (already enriched): {len(code_chunks)}")
    
    # 2. Load Cache if exists
    cache = {}
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                cache = json.load(f)
            print(f"Loaded {len(cache)} cached headers from {CACHE_PATH.name}")
        except Exception:
            cache = {}
            
    # 3. Filter chunks needing generation
    to_process = [c for c in doc_chunks if str(c["chunk_id"]) not in cache]
    print(f"Chunks requiring LLM generation: {len(to_process)}")
    
    sem = asyncio.Semaphore(CONCURRENCY_LIMIT)
    t0 = time.perf_counter()
    
    if to_process:
        async def worker(chunk):
            cid = str(chunk["chunk_id"])
            header = await generate_header_with_retry(chunk, sem)
            cache[cid] = header
            return cid, header

        # Run in batches of 50 to periodically persist cache
        batch_size = 50
        for i in range(0, len(to_process), batch_size):
            batch = to_process[i:i + batch_size]
            tasks = [worker(c) for c in batch]
            await asyncio.gather(*tasks)
            # Save cache checkpoint
            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=2)
            processed_so_far = min(i + batch_size, len(to_process))
            elapsed = time.perf_counter() - t0
            rate = processed_so_far / elapsed if elapsed > 0 else 0.0
            print(f"Progress: {processed_so_far:4d}/{len(to_process)} ({processed_so_far/len(to_process)*100:5.1f}%) | Rate: {rate:4.1f} chunks/sec | Elapsed: {elapsed:5.1f}s")

    t1 = time.perf_counter()
    print(f"\nContext generation completed in {t1 - t0:.2f}s.")
    
    # 4. Assemble Enriched Chunks
    enriched_chunks = []
    for c in all_chunks:
        cid = str(c["chunk_id"])
        c_copy = dict(c)
        if cid in cache:
            c_copy["context_header"] = cache[cid]
            # Attach deterministic AST features as structured metadata
            c_copy["ast_features"] = extract_ast_features(c.get("text", ""))
        enriched_chunks.append(c_copy)
        
    # Write enriched output
    with open(ENRICHED_PATH, "w", encoding="utf-8") as f:
        for c in enriched_chunks:
            f.write(json.dumps(c) + "\n")
    print(f"Wrote {len(enriched_chunks)} enriched chunks to {ENRICHED_PATH}")
    
    # Backup original and swap
    backup_path = CHUNKS_PATH.with_suffix(".jsonl.bak")
    if not backup_path.exists():
        import shutil
        shutil.copyfile(CHUNKS_PATH, backup_path)
        print(f"Created corpus backup at {backup_path.name}")
    
    import shutil
    shutil.copyfile(ENRICHED_PATH, CHUNKS_PATH)
    print(f"Updated primary corpus: {CHUNKS_PATH.name}")

if __name__ == "__main__":
    asyncio.run(main())
