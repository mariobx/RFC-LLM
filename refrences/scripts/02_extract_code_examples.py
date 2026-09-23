#!/usr/bin/env python3
"""
02_extract_code_examples.py
Extracts CPSA SCM Code Examples with Full Formal Grammar Features and Semantic Scenario Summaries.

Architecture:
- Ingests all .scm files across refrences/internet/examples_scm/
- 100% Intact Code: Never splits S-expressions; every .scm file is preserved as an atomic executable model.
- Option C (Static AST Extraction): Extracts heralds, protocols, algebras, roles, cryptographic primitives,
  channels, state locations, assumptions (non-orig, uniq-orig, pen-non-orig), rules, and comments.
- Option B (Gemini 3.1 Flash Lite Summary): Generates a natural, short, and informative overview of what protocol
  is modeled, security properties/attacks analyzed (MITM, replay, secrecy), and key modeling mechanisms.
- Streaming Persistence: Writes immediately to code_examples.jsonl and syncs to code_examples.json.
- Also appends to manual_chunks.jsonl so the retriever can search documentation and code examples simultaneously.
- Checkpointing & History Logging: Skips completed files on reruns.
"""

import os
import sys
import time
import json
import re
import argparse
import logging
import warnings
from pathlib import Path
from pydantic import BaseModel, Field
import dspy
import backoff
from dotenv import load_dotenv, find_dotenv
import litellm

# Silence LiteLLM log spam and deprecation warnings
litellm.suppress_debug_info = True
litellm.set_verbose = False
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning)

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(usecwd=True))
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

EXAMPLES_DIR = BASE_DIR / "internet" / "examples_scm"
CHUNKS_DIR = BASE_DIR / "chunks"
CODE_JSONL_PATH = CHUNKS_DIR / "code_examples.jsonl"
CODE_JSON_PATH = CHUNKS_DIR / "code_examples.json"
MANUAL_JSONL_PATH = CHUNKS_DIR / "manual_chunks.jsonl"
MANUAL_JSON_PATH = CHUNKS_DIR / "manual_chunks.json"
CHECKPOINT_PATH = CHUNKS_DIR / "code_examples_checkpoint.json"
HISTORY_LOG_PATH = CHUNKS_DIR / "code_examples_history.log"

DEFAULT_MODEL = os.environ.get("MODEL_NAME", "gemini/gemini-3.1-flash-lite")
DEFAULT_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DEFAULT_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")

# =====================================================================
# Option C: Static Formal CPSA Grammar Feature Extractor
# =====================================================================

def strip_scheme_comments(content: str) -> str:
    """Strip line comments (;...) and block comments (#|...|#) while preserving string literals."""
    strings = []
    def save_str(m):
        strings.append(m.group(0))
        return f"__STR_LITERAL_{len(strings)-1}__"

    # Protect string literals from semicolon stripping
    protected = re.sub(r'"(?:\\.|[^"\\])*"', save_str, content)
    # Strip block comments #| ... |#
    protected = re.sub(r'#\|.*?\|#', ' ', protected, flags=re.DOTALL)
    # Strip line comments ; ...
    protected = re.sub(r';.*$', ' ', protected, flags=re.MULTILINE)
    # Restore string literals
    for idx, s in enumerate(strings):
        protected = protected.replace(f"__STR_LITERAL_{idx}__", s)
    return protected

def parse_cpsa_scm(content: str, file_name: str) -> dict:
    """Extract complete formal CPSA 4.4 grammar AST features from an S-expression file."""
    # 1. Developer Intent Comments (extracted from raw content before stripping)
    dev_comments = [line.strip("; \t") for line in re.findall(r";;;+(.+)", content) if line.strip("; \t")]

    # 2. Strip comments to analyze only active syntax forms
    clean_code = strip_scheme_comments(content)

    # 3. Herald Title and Comment
    m_herald = re.search(r"\(herald\s+[\"\x27]([^\"]+)[\"\x27](.*?)\)", clean_code, re.DOTALL)
    herald_title = m_herald.group(1).strip() if m_herald else ""
    herald_comment = ""
    if m_herald:
        m_c = re.search(r"\(comment\s+[\"\x27]([^\"]+)[\"\x27]", m_herald.group(2))
        if m_c:
            herald_comment = m_c.group(1).strip()

    # 4. Protocols and Algebras
    protocols = []
    for pm in re.finditer(r"\(defprotocol\s+([^\s\(\)]+)\s+([^\s\(\)]+)", clean_code):
        protocols.append({"name": pm.group(1), "algebra": pm.group(2)})
    algebras = list(dict.fromkeys([p["algebra"] for p in protocols]))
    if re.search(r"\bdiffie-hellman\b", clean_code) and "diffie-hellman" not in algebras:
        algebras.append("diffie-hellman")

    # 5. Roles
    roles = list(dict.fromkeys(re.findall(r"\(defrole\s+([^\s\(\)]+)", clean_code)))

    # 6. Sorts
    all_sorts = ["text", "data", "name", "skey", "akey", "mesg", "chan", "locn", "rndx", "expt", "base", "strd"]
    sorts_used = [s for s in all_sorts if re.search(r"\b" + s + r"\b", clean_code)]

    # 7. Cryptographic Primitives
    all_crypto = ["pubk", "privk", "invk", "ltk", "cat", "enc", "senc", "aenc", "sign", "hash", "exp", "gen", "mul", "rec"]
    crypto_used = [c for c in all_crypto if re.search(r"\b" + c + r"\b", clean_code)]

    # 8. Channels and State Operations
    all_state_chan = ["auth", "conf", "stor", "load", "gen-st", "critical-sections"]
    state_chan_used = [sc for sc in all_state_chan if re.search(r"\b" + sc + r"\b", clean_code)]

    # 9. Assumptions and Constraints
    all_assumptions = ["non-orig", "pen-non-orig", "uniq-orig", "uniq-gen", "precedes", "priority", "facts"]
    assumptions_used = [a for a in all_assumptions if re.search(r"\b" + a + r"\b", clean_code)]

    # 10. Top-Level Entity Counts
    skel_count = len(re.findall(r"\(defskeleton\b", clean_code))
    listener_count = len(re.findall(r"\(deflistener\b", clean_code))
    goal_count = len(re.findall(r"\(defgoal\b", clean_code))
    rule_count = len(re.findall(r"\(defrule\b|\(rule\b", clean_code))

    title = herald_title or Path(file_name).stem.replace("_", " ").title()

    return {
        "file": file_name,
        "title": title,
        "herald_title": herald_title,
        "herald_comment": herald_comment,
        "protocols": protocols,
        "algebras": algebras,
        "roles": roles,
        "sorts": sorts_used,
        "crypto_primitives": crypto_used,
        "channels_and_state": state_chan_used,
        "assumptions": assumptions_used,
        "counts": {
            "skeletons": skel_count,
            "listeners": listener_count,
            "goals": goal_count,
            "rules": rule_count
        },
        "dev_comments": dev_comments[:4]
    }

# =====================================================================
# Option B: Gemini 3.1 Flash Lite Scenario Summarizer
# =====================================================================

class SCMExampleSummarizer(dspy.Signature):
    """You are a formal methods expert and cryptographic protocol analyst specializing in CPSA.
Analyze the provided CPSA Scheme (.scm) source code and its extracted AST metadata.
Synthesize a concise, rigorous technical summary of the protocol model.

Requirements:
1. Scenario & Classification: Identify the specific protocol or cryptographic interaction being modeled. If the file is a theoretical benchmark, regression test, minimal counterexample, or sanity check rather than an RFC protocol, explicitly state its theoretical purpose. Do not force-map abstract models to named real-world protocols.
2. Security Properties & Goals: State the exact security invariants, shapes, or adversarial behaviors under verification, as evidenced by the skeletons, listeners, and goal declarations.
3. Formal Modeling Constructs: Detail the key CPSA primitives actually declared in formal_metadata and the code (algebras, sorts, channel abstractions, state operations, origination assumptions, and custom rewrite rules). Never reference primitives that are absent from the model.
4. Grounding: Base the summary strictly on the source code, comments, and formal AST. Avoid generic boilerplate.
5. Determinism: Maintain strict factual precision and low variance. State only verifiable AST constructs and explicit security goals."""
    file_name: str = dspy.InputField(desc="Filename of the CPSA Scheme model")
    formal_metadata: str = dspy.InputField(desc="Extracted formal AST features (herald, protocols, roles, primitives, assumptions)")
    scm_code: str = dspy.InputField(desc="Verbatim Scheme source code")
    scenario_summary: str = dspy.OutputField(desc="Accurate, factual 2-4 sentence summary of the model's protocol scenario, security properties, and modeling mechanics")
    tags: list[str] = dspy.OutputField(desc="List of 3 to 6 lowercase kebab-case tags capturing the protocol name, algebra, key primitives, and verified properties")

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
def run_summarizer_with_backoff(summarizer, **kwargs):
    return summarizer(**kwargs)

# =====================================================================
# Stream and Checkpoint Manager
# =====================================================================

class CodeExampleStreamManager:
    def __init__(self, code_jsonl_path: Path, code_json_path: Path,
                 manual_jsonl_path: Path, manual_json_path: Path,
                 checkpoint_path: Path, history_log_path: Path,
                 reprocess_all: bool = False):
        self.code_jsonl_path = code_jsonl_path
        self.code_json_path = code_json_path
        self.manual_jsonl_path = manual_jsonl_path
        self.manual_json_path = manual_json_path
        self.checkpoint_path = checkpoint_path
        self.history_log_path = history_log_path

        self.code_jsonl_path.parent.mkdir(parents=True, exist_ok=True)

        if reprocess_all:
            if self.code_jsonl_path.exists():
                self.code_jsonl_path.unlink()
            if self.code_json_path.exists():
                self.code_json_path.unlink()
            if self.checkpoint_path.exists():
                self.checkpoint_path.unlink()
            if self.history_log_path.exists():
                self.history_log_path.unlink()
            # Strip previous code_example records from manual_chunks.jsonl to avoid duplicates
            if self.manual_jsonl_path.exists():
                doc_lines = []
                with open(self.manual_jsonl_path, "r", encoding="utf-8") as mf:
                    for line in mf:
                        if line.strip():
                            try:
                                rec = json.loads(line)
                                if rec.get("chunk_type") != "code_example":
                                    doc_lines.append(line)
                            except Exception:
                                doc_lines.append(line)
                with open(self.manual_jsonl_path, "w", encoding="utf-8") as mf:
                    mf.writelines(doc_lines)
            self.completed_files = set()
            self.all_examples = []
            self.current_chunk_id = self._get_next_manual_chunk_id()
        else:
            self.completed_files = self._load_completed()
            self.all_examples = self._load_existing_examples()
            self.current_chunk_id = self._get_next_manual_chunk_id()

        self._code_f = open(self.code_jsonl_path, "a", encoding="utf-8")
        self._manual_f = open(self.manual_jsonl_path, "a", encoding="utf-8") if self.manual_jsonl_path.exists() else None

    def _get_next_manual_chunk_id(self) -> int:
        max_id = 0
        if self.manual_jsonl_path.exists():
            with open(self.manual_jsonl_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            c = json.loads(line)
                            if c.get("chunk_type") != "code_example":
                                max_id = max(max_id, c.get("chunk_id", 0))
                        except Exception:
                            pass
        return max_id

    def _load_completed(self) -> set[str]:
        completed = set()
        if self.checkpoint_path.exists():
            try:
                with open(self.checkpoint_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    completed.update(data.get("completed_files", []))
            except Exception:
                pass
        if self.history_log_path.exists():
            with open(self.history_log_path, "r", encoding="utf-8") as f:
                for line in f:
                    m = re.search(r"COMPLETED:\s*([^\s|]+)", line)
                    if m:
                        completed.add(m.group(1).strip())
        return completed

    def _load_existing_examples(self) -> list[dict]:
        examples = []
        if self.code_jsonl_path.exists():
            with open(self.code_jsonl_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            examples.append(json.loads(line))
                        except Exception:
                            pass
        return examples

    def is_file_completed(self, file_key: str) -> bool:
        return file_key in self.completed_files

    def add_example(self, source_file: str, meta: dict, scenario_summary: str, tags: list[str], code: str) -> dict:
        self.current_chunk_id += 1
        prot_names = ", ".join([p["name"] for p in meta.get("protocols", [])]) or "protocol"
        breadcrumb = f"Code Examples > {prot_names} > {meta['title']}"

        chunk = {
            "chunk_id": self.current_chunk_id,
            "chunk_type": "code_example",
            "source_file": source_file,
            "breadcrumb": breadcrumb,
            "title": meta["title"],
            "word_count": len(code.split()),
            "scenario_summary": scenario_summary,
            "tags": tags,
            "formal_metadata": meta,
            "text": code
        }

        self.all_examples.append(chunk)

        # Write to code_examples.jsonl
        self._code_f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        self._code_f.flush()
        os.fsync(self._code_f.fileno())

        # Also append to manual_chunks.jsonl for unified RAG search (check deduplication)
        if self._manual_f:
            already_in_manual = False
            if self.manual_jsonl_path.exists():
                with open(self.manual_jsonl_path, "r", encoding="utf-8") as mf:
                    for line in mf:
                        if f'"{source_file}"' in line:
                            already_in_manual = True
                            break
            if not already_in_manual:
                self._manual_f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                self._manual_f.flush()
                os.fsync(self._manual_f.fileno())

        return chunk

    def mark_completed(self, file_key: str, words: int):
        self.completed_files.add(file_key)
        self._save_checkpoint()
        self.sync_to_json()

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] COMPLETED: {file_key:<55} | Words: {words:6,d}\n"
        with open(self.history_log_path, "a", encoding="utf-8") as hf:
            hf.write(log_line)
            hf.flush()

    def _save_checkpoint(self):
        with open(self.checkpoint_path, "w", encoding="utf-8") as f:
            json.dump({
                "completed_files": sorted(list(self.completed_files)),
                "total_examples": len(self.all_examples),
                "last_chunk_id": self.current_chunk_id,
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=2)

    def sync_to_json(self):
        with open(self.code_json_path, "w", encoding="utf-8") as f:
            json.dump(self.all_examples, f, indent=2, ensure_ascii=False)

    def close(self):
        if not self._code_f.closed:
            self._code_f.close()
        if self._manual_f and not self._manual_f.closed:
            self._manual_f.close()
        self.sync_to_json()
        self._save_checkpoint()

# =====================================================================
# Processing Logic
# =====================================================================

def process_scm_file(scm_path: Path, summarizer, delay: float, stream_mgr: CodeExampleStreamManager):
    file_key = f"internet/examples_scm/{scm_path.name}"
    if stream_mgr.is_file_completed(file_key):
        print(f"[Skip] Already completed: {file_key}")
        return

    code = scm_path.read_text(encoding="utf-8", errors="ignore").strip()
    words = len(code.split())
    if words < 10:
        return

    print(f"\n========================================================")
    print(f"[Processing SCM Example] {file_key} ({words} words)")
    print(f"========================================================")

    # 1. Option C: Static Formal CPSA Grammar Extraction
    meta = parse_cpsa_scm(code, scm_path.name)
    print(f"  Title:      {meta['title']}")
    if meta['herald_comment']:
        print(f"  Comment:    {meta['herald_comment']}")
    print(f"  Protocols:  {meta['protocols']}")
    print(f"  Roles:      {meta['roles']}")
    print(f"  Primitives: {meta['crypto_primitives']}")
    print(f"  Assumptions:{meta['assumptions']}")

    # 2. Option B: Gemini 3.1 Flash Lite Scenario Summarization
    scenario_summary = ""
    tags = []
    if summarizer:
        meta_str = json.dumps(meta, indent=2)
        try:
            print(f"  -> Generating scenario summary via Gemini 3.1 Flash Lite...")
            sys.stdout.flush()
            pred = run_summarizer_with_backoff(
                summarizer,
                file_name=scm_path.name,
                formal_metadata=meta_str,
                scm_code=code
            )
            scenario_summary = getattr(pred, "scenario_summary", "").strip()
            tags = getattr(pred, "tags", []) or []
            print(f"  -> Summary: {scenario_summary}")
            print(f"  -> Tags:    {tags}")
            if delay > 0:
                time.sleep(delay)
        except Exception as e:
            print(f"  -> Summarizer warning for {scm_path.name}: {e}", file=sys.stderr)
            scenario_summary = meta.get("herald_comment", "") or f"Example CPSA protocol model for {meta['title']}."
            tags = [p["name"] for p in meta.get("protocols", [])]
    else:
        scenario_summary = meta.get("herald_comment", "") or f"Example CPSA protocol model for {meta['title']}."
        tags = [p["name"] for p in meta.get("protocols", [])]

    chunk = stream_mgr.add_example(
        source_file=file_key,
        meta=meta,
        scenario_summary=scenario_summary,
        tags=tags,
        code=code
    )
    print(f"  [Chunk #{chunk['chunk_id']:04d}] Saved un-split SCM example: '{chunk['title']}'")

    stream_mgr.mark_completed(file_key, words)

# =====================================================================
# Main CLI
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description="Extract CPSA SCM Code Examples with Formal AST and Scenario Summaries.")
    parser.add_argument("--file", "-f", type=str, default=None, help="Process a single specific .scm file.")
    parser.add_argument("--no-llm", action="store_true", help="Disable Gemini LLM; use static AST metadata and comments only.")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help=f"Model identifier. Default: {DEFAULT_MODEL}")
    parser.add_argument("--api-key", type=str, default=DEFAULT_API_KEY, help="Gemini API key.")
    parser.add_argument("--api-base", type=str, default=DEFAULT_API_BASE, help="Ollama API base URL.")
    parser.add_argument("--delay", type=float, default=None, help="Pacing delay between LLM calls. Default: 3.5s for Gemini.")
    parser.add_argument("--reprocess-all", action="store_true", help="Clear checkpoint and reprocess all files.")
    args = parser.parse_args()

    summarizer = None
    is_gemini = args.model.startswith("gemini") or "gemini" in args.model.lower()
    delay = args.delay if args.delay is not None else (3.5 if is_gemini else 0.0)

    if not args.no_llm:
        if is_gemini:
            model_tag = args.model if args.model.startswith("gemini/") else f"gemini/{args.model}"
            api_key = args.api_key or os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                print("Error: GEMINI_API_KEY is required for Gemini models.", file=sys.stderr)
                sys.exit(1)
            os.environ["GEMINI_API_KEY"] = api_key
            print(f"Configuring Gemini ('{model_tag}', delay: {delay}s) for SCM scenario summarization...")
            lm = dspy.LM(model_tag, api_key=api_key)
        else:
            clean_model = args.model
            for prefix in ["ollama_chat/", "ollama/"]:
                if clean_model.startswith(prefix):
                    clean_model = clean_model[len(prefix):]
            print(f"Connecting to Ollama at {args.api_base} with model '{clean_model}'...")
            lm = dspy.LM(f"ollama_chat/{clean_model}", api_base=args.api_base, api_key="", temperature=0.2)

        dspy.configure(lm=lm)
        summarizer = dspy.Predict(SCMExampleSummarizer)

    stream_mgr = CodeExampleStreamManager(
        code_jsonl_path=CODE_JSONL_PATH,
        code_json_path=CODE_JSON_PATH,
        manual_jsonl_path=MANUAL_JSONL_PATH,
        manual_json_path=MANUAL_JSON_PATH,
        checkpoint_path=CHECKPOINT_PATH,
        history_log_path=HISTORY_LOG_PATH,
        reprocess_all=args.reprocess_all
    )

    if args.file:
        target_path = Path(args.file).resolve()
        if not target_path.exists():
            print(f"Error: Target file '{target_path}' not found.", file=sys.stderr)
            sys.exit(1)
        all_files = [target_path]
    else:
        all_files = sorted(list(EXAMPLES_DIR.glob("*.scm")))

    print(f"\n========================================================")
    print(f"CPSA SCM Code Examples Pipeline")
    print(f"  Discovered SCM files:        {len(all_files)}")
    print(f"  Existing SCM examples in DB: {len(stream_mgr.all_examples)}")
    print(f"  Completed files recognized:  {len(stream_mgr.completed_files)}")
    print(f"  Summarization:               {'ENABLED (Gemini 3.1 Flash Lite)' if summarizer else 'DISABLED (Static AST Only)'}")
    print(f"========================================================\n")

    for f_path in all_files:
        process_scm_file(
            scm_path=f_path,
            summarizer=summarizer,
            delay=delay,
            stream_mgr=stream_mgr
        )

    stream_mgr.close()

    total = len(stream_mgr.all_examples)
    print(f"\nFinished SCM processing.")
    print(f"Total SCM code examples in catalog: {total}")
    print(f"Catalog saved to:\n  - {CODE_JSONL_PATH}\n  - {CODE_JSON_PATH}")
    print(f"Also appended to:\n  - {MANUAL_JSONL_PATH}")
    print(f"History log: {HISTORY_LOG_PATH}")
    print(f"Checkpoint:  {CHECKPOINT_PATH}")

if __name__ == "__main__":
    main()
