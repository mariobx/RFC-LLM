#!/usr/bin/env python3
"""
03_query_rag.py
Fast, lightweight retrieval tool to query the generated CPSA manual Q&A database.
Can be run via CLI or imported directly as a Python module in DSPy pipelines.
"""

import sys
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
QA_JSON_PATH = BASE_DIR / "dataset" / "manual_qa_dataset.json"
CHUNKS_PATH = BASE_DIR / "chunks" / "manual_chunks.json"

def tokenize(text: str) -> set[str]:
    """Simple lowercase tokenization stripping punctuation."""
    return set(re.findall(r'[a-zA-Z0-9_\-]+', text.lower()))

class CPSAKnowledgeBase:
    def __init__(self, qa_path: Path = QA_JSON_PATH, chunks_path: Path = CHUNKS_PATH):
        self.qa_records = []
        self.flat_qas = []
        self.chunks = {}

        if chunks_path.exists():
            with open(chunks_path, "r", encoding="utf-8") as f:
                raw_chunks = json.load(f)
                self.chunks = {c["chunk_id"]: c for c in raw_chunks}

        if qa_path.exists():
            with open(qa_path, "r", encoding="utf-8") as f:
                self.qa_records = json.load(f)
                for rec in self.qa_records:
                    chunk_id = rec["chunk_id"]
                    title = rec["title"]
                    chapter = rec["chapter"]
                    for qa in rec.get("qa_pairs", []):
                        self.flat_qas.append({
                            "chunk_id": chunk_id,
                            "title": title,
                            "chapter": chapter,
                            "question": qa["question"],
                            "answer": qa["answer"],
                            "category": qa.get("category", "general"),
                            "key_terms": qa.get("key_terms", []),
                            # Combined search text
                            "_search_text": f"{title} {chapter} {qa['question']} {qa['answer']} {' '.join(qa.get('key_terms', []))}"
                        })

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Search the Q&A dataset by token overlap and keyword relevance."""
        if not self.flat_qas:
            return []

        query_tokens = tokenize(query)
        scored_results = []

        for item in self.flat_qas:
            item_tokens = tokenize(item["_search_text"])
            overlap = query_tokens.intersection(item_tokens)
            if not overlap:
                continue

            # Scoring: question match weighted higher than answer match
            q_tokens = tokenize(item["question"])
            terms_tokens = tokenize(" ".join(item["key_terms"]))
            
            score = len(overlap)
            score += 2.0 * len(query_tokens.intersection(q_tokens))
            score += 3.0 * len(query_tokens.intersection(terms_tokens))

            # Bonus for exact substring match
            if query.lower() in item["question"].lower():
                score += 5.0
            if query.lower() in item["_search_text"].lower():
                score += 2.0

            scored_results.append((score, item))

        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [res[1] for res in scored_results[:top_k]]

    def get_chunk_text(self, chunk_id: int) -> str | None:
        """Retrieve original raw manual chunk text for deeper context."""
        chunk = self.chunks.get(chunk_id)
        return chunk["text"] if chunk else None

def main():
    if len(sys.argv) < 2:
        print("Usage: python 03_query_rag.py '<query string>' [top_k]")
        sys.exit(1)

    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    kb = CPSAKnowledgeBase()
    results = kb.search(query, top_k=top_k)

    print(f"\nQuery: '{query}'")
    print(f"Found {len(results)} matches:\n" + "="*60)

    if not results:
        print("No direct matches found. Try broadening the keywords or generate more chunks.")
        return

    for idx, item in enumerate(results, 1):
        print(f"\nMatch {idx} [{item['category'].upper()}] - {item['title']} (Ch. {item['chapter']})")
        print(f"Q: {item['question']}")
        print(f"A: {item['answer']}")
        if item.get("key_terms"):
            print(f"Key Terms: {', '.join(item['key_terms'])}")
        print("-" * 60)

if __name__ == "__main__":
    main()
