#!/usr/bin/env python3
"""
sync_context.py — Agnostic Repository -> Markdown Context Bundler for RFC-LLM.

Reads notebook_context/bundle_config.json and packages the repository's source
code, CLI executables, tests, domain knowledge and documentation into clean,
plain-text Markdown bundles under notebook_context/bundles/, optimized for
uploading to an LLM Notebook knowledge base.

Zero external dependencies (Python 3.8+ stdlib only).

Features
--------
1. Dynamic discovery: resolves `git ls-files` (tracked + untracked, honoring
   .gitignore) against the glob rules in bundle_config.json. Extensionless
   executables and shebang scripts are auto-detected and routed to a fallback
   bundle when no glob claims them.
2. Safety guards: binary files (NUL byte sniff) and files above
   settings.max_file_size_kb are NEVER dumped raw; they are routed to the
   "Excluded & Heavy Assets Inventory" with size, line/record counts and a
   lightweight schema preview (CSV header + sample rows, JSON/JSONL top-level
   keys, NPY shape/dtype, Markdown/TXT heading outline).
3. State tracking: SHA-256 hashes of every discovered file are persisted in
   notebook_context/manifest_state.json. Each run diffs against the previous
   state and prepends a "Changes Since Last Sync" section (added / modified /
   deleted + git branch & commit) to the master index bundle.
4. AST introspection: for every bundled Python file, the stdlib `ast` module
   extracts module docstrings, classes, top-level functions and argparse CLI
   flags into an automated Symbol & Script Registry table in the index bundle.
5. CLI: --check (dry-run delta report, exit 1 on drift), --rebuild (force full
   regeneration), --install-hook (wire .git/hooks/post-commit).

Usage
-----
    python3 notebook_context/sync_context.py            # sync
    python3 notebook_context/sync_context.py --check    # dry-run diff
    python3 notebook_context/sync_context.py --rebuild  # force rebuild
    python3 notebook_context/sync_context.py --install-hook
"""

from __future__ import annotations

import argparse
import ast
import csv
import datetime as _dt
import fnmatch  # noqa: F401  (kept for reference; matching uses regex translation)
import hashlib
import io
import json
import os
import re
import stat
import struct
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

# --------------------------------------------------------------------------
# Paths & Token Metrics
# --------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SCRIPT_DIR, "bundle_config.json")


def resolve_abs_path(path: str) -> str:
    """Resolve relative, external (e.g. ../), or absolute paths cleanly against REPO_ROOT."""
    if os.path.isabs(path):
        return os.path.normpath(path)
    return os.path.normpath(os.path.join(REPO_ROOT, path))


def estimate_tokens(text: str) -> int:
    """Fast, accurate token heuristic for code and markdown (~4 characters per token)."""
    return max(1, len(text) // 4)

# --------------------------------------------------------------------------
# Glob -> regex translation (supports **, *, ?)
# --------------------------------------------------------------------------

def glob_to_regex(pattern: str) -> "re.Pattern[str]":
    """Translate a path glob into an anchored regex.

    - ``**/`` matches zero or more directory segments.
    - ``**``  (not followed by /) matches anything including '/'.
    - ``*``   matches anything except '/'.
    - ``?``   matches one character except '/'.
    """
    i, n = 0, len(pattern)
    out: List[str] = []
    while i < n:
        c = pattern[i]
        if c == "*":
            if i + 1 < n and pattern[i + 1] == "*":
                if i + 2 < n and pattern[i + 2] == "/":
                    out.append("(?:.*/)?")
                    i += 3
                    continue
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
            i += 1
        elif c == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def matches_any(path: str, patterns: List[str], _cache: Dict[str, "re.Pattern[str]"] = {}) -> bool:
    for p in patterns:
        rx = _cache.get(p)
        if rx is None:
            rx = glob_to_regex(p)
            _cache[p] = rx
        if rx.match(path):
            return True
    return False


# --------------------------------------------------------------------------
# Git helpers
# --------------------------------------------------------------------------

def run_git(args: List[str]) -> str:
    try:
        return subprocess.check_output(
            ["git"] + args, cwd=REPO_ROOT, stderr=subprocess.DEVNULL
        ).decode("utf-8", errors="replace")
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def discover_files(cfg: Optional[Dict[str, Any]] = None) -> List[str]:
    """Tracked + untracked-but-not-ignored files, per git, plus explicit/external files."""
    out = run_git(["ls-files", "--cached", "--others", "--exclude-standard"])
    files = [f for f in out.splitlines() if f.strip()]

    if cfg:
        # 1. Discover explicit files declared across all bundles
        for b in cfg.get("bundles", []):
            for ef in b.get("explicit_files", []):
                if ef not in files:
                    abs_p = resolve_abs_path(ef)
                    if os.path.isfile(abs_p):
                        files.append(ef)

        # 2. Discover files from external sources configured in settings
        external_sources = cfg.get("settings", {}).get("external_sources", [])
        for src in external_sources:
            root = src.get("root")
            if not root:
                continue
            abs_root = resolve_abs_path(root)
            if not os.path.isdir(abs_root):
                continue
            globs = src.get("globs", ["**/*"])
            excludes = src.get("excludes", [".git/**", "**/__pycache__/**"])
            for dirpath, dirnames, filenames in os.walk(abs_root):
                dirnames[:] = [d for d in dirnames if not matches_any(d + "/**", excludes) and not d.startswith(".")]
                rel_dir = os.path.relpath(dirpath, abs_root)
                for fn in filenames:
                    rel_src = fn if rel_dir == "." else os.path.join(rel_dir, fn)
                    if matches_any(rel_src, excludes):
                        continue
                    if matches_any(rel_src, globs):
                        full_file = os.path.join(dirpath, fn)
                        try:
                            rel_to_repo = os.path.relpath(full_file, REPO_ROOT)
                        except ValueError:
                            rel_to_repo = full_file
                        if rel_to_repo not in files:
                            files.append(rel_to_repo)

    # Keep only regular files that exist on disk.
    return sorted(set(f for f in files if os.path.isfile(resolve_abs_path(f))))


def git_context() -> Dict[str, str]:
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"]).strip() or "unknown"
    commit = run_git(["rev-parse", "HEAD"]).strip() or "unknown"
    subject = run_git(["log", "-1", "--pretty=%s"]).strip()
    return {"branch": branch, "commit": commit, "subject": subject}


# --------------------------------------------------------------------------
# File classification helpers
# --------------------------------------------------------------------------

BINARY_SNIFF_BYTES = 8192

def is_binary(path: str) -> bool:
    try:
        with open(path, "rb") as fp:
            chunk = fp.read(BINARY_SNIFF_BYTES)
        return b"\x00" in chunk
    except OSError:
        return True


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_lines(path: str) -> int:
    n = 0
    with open(path, "rb") as fp:
        for _ in fp:
            n += 1
    return n


def read_text(path: str) -> Optional[str]:
    """Strict UTF-8 read; returns None if the file is not valid UTF-8 text."""
    try:
        with open(path, "r", encoding="utf-8") as fp:
            return fp.read()
    except (UnicodeDecodeError, OSError):
        return None


def has_shebang(path: str) -> bool:
    try:
        with open(path, "rb") as fp:
            return fp.read(2) == b"#!"
    except OSError:
        return False


def is_executable(path: str) -> bool:
    try:
        return bool(os.stat(path).st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    except OSError:
        return False


FENCE_LANG_BY_EXT = {
    ".py": "python", ".pyi": "python", ".sh": "bash", ".bash": "bash",
    ".scm": "scheme", ".md": "markdown", ".json": "json", ".jsonl": "json",
    ".yaml": "yaml", ".yml": "yaml", ".toml": "toml", ".ini": "ini",
    ".cfg": "ini", ".txt": "text", ".tex": "latex", ".html": "html",
    ".css": "css", ".js": "javascript", ".csv": "csv", ".sql": "sql",
    ".xml": "xml", ".c": "c", ".h": "c", ".rs": "rust", ".go": "go",
    "": "text",
}


def fence_lang(path: str) -> str:
    if not os.path.basename(path) or "." not in os.path.basename(path):
        # extensionless: guess from shebang
        try:
            with open(path, "rb") as fp:
                first = fp.readline().decode("utf-8", errors="replace")
            if "python" in first:
                return "python"
            if "bash" in first or "sh" in first:
                return "bash"
        except OSError:
            pass
        return "text"
    ext = os.path.splitext(path)[1].lower()
    return FENCE_LANG_BY_EXT.get(ext, ext.lstrip("."))


def safe_fence(content: str) -> str:
    """Return a backtick fence longer than any backtick run inside content."""
    longest = 0
    for m in re.finditer(r"`+", content):
        longest = max(longest, len(m.group(0)))
    return "`" * max(3, longest + 1)


def anchor(text: str) -> str:
    slug = re.sub(r"[^a-z0-9 _-]", "", text.lower())
    return re.sub(r"[ _]+", "-", slug).strip("-")


# --------------------------------------------------------------------------
# Lightweight schema previews for heavy / binary assets (Tier 4)
# --------------------------------------------------------------------------

MAX_JSON_PARSE_BYTES = 32 * 1024 * 1024


def _preview_csv(path: str) -> List[str]:
    lines: List[str] = []
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as fp:
        reader = csv.reader(fp)
        rows = []
        for i, row in enumerate(reader):
            rows.append(row)
            if i >= 3:  # header + 3 samples
                break
        total = count_lines(path)
    if rows:
        lines.append(f"- Header ({len(rows[0])} cols): `{', '.join(rows[0])}`")
        for r in rows[1:]:
            sample = ", ".join(c if len(c) <= 40 else c[:37] + "..." for c in r)
            lines.append(f"- Sample row: `{sample}`")
    lines.append(f"- Total rows (incl. header): {total}")
    return lines


def _preview_json(path: str) -> List[str]:
    size = os.path.getsize(path)
    if size > MAX_JSON_PARSE_BYTES:
        return [f"- JSON file too large to parse for preview ({size/1024/1024:.1f} MB)."]
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fp:
            data = json.load(fp)
    except json.JSONDecodeError:
        # Some ".json" files in this repo are actually JSONL streams.
        return _preview_jsonl(path)
    lines: List[str] = []
    if isinstance(data, dict):
        keys = list(data.keys())
        lines.append(f"- Top-level object with {len(keys)} keys: `{', '.join(str(k) for k in keys[:15])}`"
                     + (" ..." if len(keys) > 15 else ""))
        for k in keys[:8]:
            v = data[k]
            if isinstance(v, list):
                item_keys = ""
                if v and isinstance(v[0], dict):
                    item_keys = " item keys: `" + ", ".join(str(x) for x in list(v[0].keys())[:12]) + "`"
                lines.append(f"  - `{k}`: list[{len(v)}]{item_keys}")
            elif isinstance(v, dict):
                lines.append(f"  - `{k}`: dict with keys `{', '.join(str(x) for x in list(v.keys())[:10])}`")
            else:
                sv = str(v)
                lines.append(f"  - `{k}`: {sv if len(sv) <= 80 else sv[:77] + '...'}")
    elif isinstance(data, list):
        lines.append(f"- Top-level array with {len(data)} records.")
        if data and isinstance(data[0], dict):
            lines.append(f"- Record keys: `{', '.join(str(k) for k in data[0].keys())}`")
    return lines


def _preview_jsonl(path: str) -> List[str]:
    lines: List[str] = []
    first_keys: Optional[List[str]] = None
    n = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            n += 1
            if first_keys is None:
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        first_keys = list(obj.keys())
                except json.JSONDecodeError:
                    first_keys = None
    lines.append(f"- JSONL stream: {n} records.")
    if first_keys is not None:
        lines.append(f"- Record keys: `{', '.join(str(k) for k in first_keys)}`")
    return lines


def _preview_npy(path: str) -> List[str]:
    try:
        with open(path, "rb") as fp:
            magic = fp.read(6)
            if magic != b"\x93NUMPY":
                return ["- Not a valid NPY file (magic mismatch)."]
            major = struct.unpack("B", fp.read(1))[0]
            fp.read(1)  # minor
            if major == 1:
                hdr_len = struct.unpack("<H", fp.read(2))[0]
            else:
                hdr_len = struct.unpack("<I", fp.read(4))[0]
            hdr = fp.read(hdr_len).decode("latin1").strip()
        return [f"- NumPy array header: `{hdr}`"]
    except (OSError, struct.error) as exc:
        return [f"- NPY header unreadable: {exc}"]


def _preview_text_outline(path: str, max_headings: int = 15) -> List[str]:
    """Line count + heading outline for oversized Markdown/text documents."""
    total = count_lines(path)
    headings: List[str] = []
    first_line = ""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fp:
            for i, line in enumerate(fp):
                if i == 0:
                    first_line = line.strip()
                if len(headings) < max_headings and re.match(r"^#{1,3} ", line):
                    headings.append(line.strip()[:90])
                if i > 20000 and len(headings) >= max_headings:
                    break
    except OSError:
        pass
    lines = [f"- Plain-text document: {total} lines."]
    if first_line:
        lines.append(f"- First line: `{first_line[:100]}`")
    if headings:
        lines.append("- Outline (first headings):")
        for h in headings:
            lines.append(f"  - {h}")
    return lines


def _preview_html(path: str) -> List[str]:
    total = count_lines(path)
    title = ""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fp:
            head = fp.read(65536)
        m = re.search(r"<title[^>]*>(.*?)</title>", head, re.S | re.I)
        if m:
            title = m.group(1).strip()[:100]
    except OSError:
        pass
    lines = [f"- Rendered/generated HTML artifact: {total} lines."]
    if title:
        lines.append(f"- <title>: {title}")
    return lines


def _preview_binary(path: str) -> List[str]:
    sig = ""
    try:
        with open(path, "rb") as fp:
            head = fp.read(8)
        if head.startswith(b"%PDF"):
            sig = "PDF document"
        elif head.startswith(b"\x89PNG"):
            sig = "PNG image"
        elif head.startswith(b"\x93NUMPY"):
            sig = "NumPy array"
        elif head[:2] == b"PK":
            sig = "ZIP archive"
        elif head[:4] == b"\x1f\x8b\x08\x00":
            sig = "gzip stream"
    except OSError:
        pass
    return [f"- Binary file{': ' + sig if sig else ' (type unknown)'} — raw bytes excluded from text context."]


def summarize_asset(path: str, reason: str) -> Dict[str, Any]:
    """Build a metadata + schema-preview record for a Tier 4 asset."""
    abs_path = resolve_abs_path(path)
    size = os.path.getsize(abs_path)
    ext = os.path.splitext(path)[1].lower()
    binary = is_binary(abs_path)

    rec: Dict[str, Any] = {
        "path": path,
        "size_bytes": size,
        "size_kb": round(size / 1024, 1),
        "reason": reason,
        "binary": binary,
    }

    preview: List[str] = []
    if binary:
        if ext == ".npy":
            preview = _preview_npy(abs_path)
        else:
            preview = _preview_binary(abs_path)
    elif ext == ".csv":
        preview = _preview_csv(abs_path)
    elif ext == ".jsonl":
        preview = _preview_jsonl(abs_path)
    elif ext == ".json":
        preview = _preview_json(abs_path)
    elif ext == ".npy":
        preview = _preview_npy(abs_path)
    elif ext in (".md", ".txt", ".tex"):
        preview = _preview_text_outline(abs_path)
    elif ext in (".html", ".htm", ".xhtml", ".svg"):
        preview = _preview_html(abs_path)
    else:
        rec["lines"] = count_lines(abs_path)
        preview = [f"- Text file: {rec['lines']} lines."]

    if not binary and "lines" not in rec and ext not in (".csv",):
        try:
            rec["lines"] = count_lines(abs_path)
        except OSError:
            pass
    rec["preview"] = preview
    return rec


# --------------------------------------------------------------------------
# AST introspection (Symbol & Script Registry)
# --------------------------------------------------------------------------

def extract_python_symbols(rel_path: str) -> Optional[Dict[str, Any]]:
    abs_path = resolve_abs_path(rel_path)
    text = read_text(abs_path)
    if text is None:
        return None
    try:
        tree = ast.parse(text, filename=rel_path)
    except SyntaxError:
        return None

    doc = ast.get_docstring(tree) or ""
    doc_first = doc.strip().splitlines()[0] if doc.strip() else ""

    classes: List[str] = []
    funcs: List[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append(node.name)

    cli_args: List[str] = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_argument"):
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str) \
                        and arg.value.startswith("-"):
                    cli_args.append(arg.value)

    return {
        "path": rel_path,
        "docstring": doc_first,
        "classes": classes,
        "functions": funcs,
        "cli_args": cli_args,
    }


# --------------------------------------------------------------------------
# Configuration loading
# --------------------------------------------------------------------------

def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as fp:
        return json.load(fp)


# --------------------------------------------------------------------------
# State manifest
# --------------------------------------------------------------------------

def load_state(path: str) -> Dict[str, Any]:
    if os.path.isfile(path):
        try:
            with open(path, "r", encoding="utf-8") as fp:
                return json.load(fp)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_state(path: str, state: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fp:
        json.dump(state, fp, indent=2, sort_keys=True)
        fp.write("\n")
    os.replace(tmp, path)


def diff_states(old_files: Dict[str, Dict], new_files: Dict[str, Dict]) -> Dict[str, List[str]]:
    added, modified, deleted = [], [], []
    for p, rec in sorted(new_files.items()):
        if p not in old_files:
            added.append(p)
        elif old_files[p].get("sha256") != rec.get("sha256"):
            modified.append(p)
    for p in sorted(old_files):
        if p not in new_files:
            deleted.append(p)
    return {"added": added, "modified": modified, "deleted": deleted}


# --------------------------------------------------------------------------
# Core sync engine
# --------------------------------------------------------------------------

class SyncResult:
    def __init__(self) -> None:
        self.bundles: Dict[str, Dict[str, Any]] = {}
        self.summarized: List[Dict[str, Any]] = []
        self.unclassified: List[str] = []
        self.auto_detected_executables: List[Tuple[str, str]] = []  # (path, bundle)
        self.delta: Dict[str, List[str]] = {"added": [], "modified": [], "deleted": []}
        self.first_run: bool = True
        self.state_files: Dict[str, Dict] = {}


def plan_sync(cfg: Dict[str, Any], files: List[str]) -> SyncResult:
    settings: Dict = cfg.get("settings", {})  # type: ignore[assignment]
    max_kb: float = float(settings.get("max_file_size_kb", 600))
    global_excludes: List[str] = cfg.get("global_excludes", [])  # type: ignore[assignment]
    bundles_cfg: List[Dict] = cfg.get("bundles", [])  # type: ignore[assignment]
    summarized_patterns: List[str] = cfg.get("summarized_assets", {}).get("patterns", [])  # type: ignore[assignment]

    result = SyncResult()
    bundle_files: Dict[str, List[str]] = {b["name"]: [] for b in bundles_cfg}
    fallback_bundle: Optional[str] = None
    master_bundle: Optional[str] = None
    for b in bundles_cfg:
        if b.get("is_master_index"):
            master_bundle = b["name"]
        if "Tier 3" in str(b.get("tier", "")) and fallback_bundle is None:
            fallback_bundle = b["name"]
    if fallback_bundle is None and bundles_cfg:
        fallback_bundle = bundles_cfg[-1]["name"]

    all_explicit: set[str] = set()
    for b in bundles_cfg:
        for ef in b.get("explicit_files", []):
            all_explicit.add(ef)

    summarized_paths: List[str] = []

    # Pass 1 — exclusions, summarized assets, bundle matching.
    for rel in files:
        if rel not in all_explicit and matches_any(rel, global_excludes):
            continue
        abs_path = resolve_abs_path(rel)
        binary = is_binary(abs_path)
        size_kb = os.path.getsize(abs_path) / 1024.0

        explicit_summarized = matches_any(rel, summarized_patterns)

        # Which bundle (if any) claims this file?
        claimed_by: Optional[str] = None
        claimed_bundle_cfg: Optional[Dict] = None
        for b in bundles_cfg:
            if matches_any(rel, b.get("include_globs", [])) or rel in b.get("explicit_files", []):
                claimed_by = b["name"]
                claimed_bundle_cfg = b
                break

        bundle_max_kb = max_kb
        if claimed_bundle_cfg and "max_file_size_kb" in claimed_bundle_cfg:
            bundle_max_kb = float(claimed_bundle_cfg["max_file_size_kb"])

        if binary or size_kb > bundle_max_kb or explicit_summarized:
            if binary:
                reason = "binary file (raw bytes unsafe for text context)"
            elif size_kb > bundle_max_kb:
                reason = f"exceeds max_file_size_kb ({size_kb:.1f} KB > {bundle_max_kb:g} KB)"
            else:
                reason = "declared Tier 4 summarized asset"
            result.summarized.append(summarize_asset(rel, reason))
            summarized_paths.append(rel)
            result.state_files[rel] = {
                "sha256": sha256_of(abs_path),
                "size_bytes": os.path.getsize(abs_path),
                "status": "summarized",
                "bundle": claimed_by or "(tier4)",
            }
            continue

        if claimed_by is not None:
            bundle_files[claimed_by].append(rel)
        else:
            result.unclassified.append(rel)

    # Pass 2 — auto-detect extensionless executables / shebang scripts that no
    # glob claimed, and route them to the fallback (scripts) bundle.
    if settings.get("include_extensionless_executables", True):
        still_unclassified: List[str] = []
        for rel in result.unclassified:
            abs_path = resolve_abs_path(rel)
            ext = os.path.splitext(rel)[1]
            executable = is_executable(abs_path)
            shebang = settings.get("auto_detect_shebangs", True) and has_shebang(abs_path)
            if (ext == "" and executable) or shebang:
                target = fallback_bundle or (master_bundle or "")
                bundle_files[target].append(rel)
                result.auto_detected_executables.append((rel, target))
            else:
                still_unclassified.append(rel)
        result.unclassified = still_unclassified

    # Build state records for included files.
    for bname, flist in bundle_files.items():
        for rel in sorted(flist):
            abs_path = resolve_abs_path(rel)
            result.state_files[rel] = {
                "sha256": sha256_of(abs_path),
                "size_bytes": os.path.getsize(abs_path),
                "status": "included",
                "bundle": bname,
            }

    # Symbol registry across all bundled Python files.
    symbol_registry: List[Dict[str, object]] = []
    if settings.get("generate_ast_symbol_registry", True):
        for bname, flist in bundle_files.items():
            for rel in sorted(flist):
                if rel.endswith(".py"):
                    sym = extract_python_symbols(rel)
                    if sym:
                        sym["bundle"] = bname
                        symbol_registry.append(sym)

    result.bundles = {
        b["name"]: {
            "cfg": b,
            "files": sorted(bundle_files[b["name"]]),
        }
        for b in bundles_cfg
    }
    result.symbol_registry = symbol_registry  # type: ignore[attr-defined]
    result.master_bundle = master_bundle  # type: ignore[attr-defined]
    return result


# --------------------------------------------------------------------------
# Markdown rendering
# --------------------------------------------------------------------------

_CTRL_STRIP_RE = re.compile(r"[\x00-\x08\x0b\x0e-\x1f\x7f]")


def sanitize_text(text: str) -> Tuple[str, int]:
    """Neutralize control-char garbage from PDF-to-text conversions.

    - Form feeds (\\x0c, page separators) become newlines.
    - Carriage returns are normalized away.
    - All other C0/C1-style control characters are stripped.
    Returns (clean_text, number_of_characters_changed).
    """
    n_ff = text.count("\x0c")
    n_cr = text.count("\r")
    out = text.replace("\x0c", "\n").replace("\r\n", "\n").replace("\r", "")
    out, n_ctrl = _CTRL_STRIP_RE.subn("", out)
    return out, n_ff + n_cr + n_ctrl


def render_file_section(rel: str) -> str:
    abs_path = resolve_abs_path(rel)
    text = read_text(abs_path)
    if text is None:
        return ""  # should not happen; binary guard ran earlier
    text, n_sanitized = sanitize_text(text)
    digest = sha256_of(abs_path)[:12]
    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    tokens = estimate_tokens(text)
    lang = fence_lang(rel)
    fence = safe_fence(text)
    body = text.rstrip("\n")
    sanitized_note = f" · {n_sanitized} control chars sanitized" if n_sanitized else ""
    out = [
        f"### `{rel}`",
        "",
        f"*sha256:`{digest}` · {lines} lines · {os.path.getsize(abs_path)/1024:.1f} KB (~{tokens:,} tokens) · lang:`{lang}`{sanitized_note}*",
        "",
        f"{fence}{lang}",
        body,
        fence,
        "",
    ]
    return "\n".join(out)


def render_delta_section(delta: Dict[str, List[str]], git: Dict[str, str], first_run: bool) -> str:
    out = ["## Changes Since Last Sync", ""]
    out.append(f"- **Git branch:** `{git['branch']}`")
    out.append(f"- **Git commit:** `{git['commit'][:12]}` — {git['subject']}")
    if first_run:
        out.append("- **First sync** — no previous manifest state; full baseline established.")
    else:
        total = sum(len(v) for v in delta.values())
        if total == 0:
            out.append("- No file changes detected since the previous sync.")
        for label in ("added", "modified", "deleted"):
            items = delta.get(label, [])
            out.append(f"- **{label.capitalize()} ({len(items)}):**"
                       + (" none" if not items else ""))
            for p in items:
                out.append(f"  - `{p}`")
    out.append("")
    return "\n".join(out)


def render_symbol_registry(registry: List[Dict[str, Any]]) -> str:
    out = ["## Symbol & Script Registry (automated AST introspection)", ""]
    if not registry:
        out.append("_No Python modules were bundled in this sync._")
        out.append("")
        return "\n".join(out)
    out.append(f"{len(registry)} Python modules introspected with the stdlib `ast` module.")
    out.append("")
    out.append("| Module | Docstring | Classes | Top-level Functions | CLI Arguments |")
    out.append("|---|---|---|---|---|")
    for sym in registry:
        path = str(sym["path"])
        doc = str(sym.get("docstring", ""))[:60].replace("|", "\\|")
        classes = sym.get("classes", [])
        funcs = sym.get("functions", [])
        cli = sym.get("cli_args", [])
        c_txt = ", ".join(f"`{c}`" for c in classes[:6]) + (" …" if len(classes) > 6 else "")
        f_txt = ", ".join(f"`{f}`" for f in funcs[:6]) + (" …" if len(funcs) > 6 else "")
        a_txt = ", ".join(f"`{a}`" for a in cli[:10]) + (" …" if len(cli) > 10 else "")
        out.append(f"| `{path}` | {doc or '—'} | {c_txt or '—'} | {f_txt or '—'} | {a_txt or '—'} |")
    out.append("")
    return "\n".join(out)


def render_heavy_inventory(summarized: List[Dict[str, Any]]) -> str:
    out = ["## Excluded & Heavy Assets Inventory (Tier 4)", ""]
    if not summarized:
        out.append("_No heavy or binary assets were detected._")
        out.append("")
        return "\n".join(out)
    total_kb = sum(float(s.get("size_kb", 0)) for s in summarized)
    out.append(
        f"{len(summarized)} assets ({total_kb/1024:.1f} MB total) were **excluded from raw text "
        "dumping** and summarized below with metadata and lightweight schema previews, so the "
        "downstream LLM is aware of every dataset, embedding matrix, manual, figure and log in "
        "the repository without ingesting their bulk."
    )
    out.append("")
    for s in sorted(summarized, key=lambda x: str(x["path"])):
        lines_info = f" · {s['lines']} lines" if "lines" in s else ""
        out.append(f"### `{s['path']}`")
        out.append("")
        out.append(f"*{s['size_kb']} KB{lines_info} · excluded because: {s['reason']}*")
        out.append("")
        for p in s.get("preview", []):
            out.append(str(p))
        out.append("")
    return "\n".join(out)


def render_bundle(name: str, info: Dict[str, Any], result: SyncResult,
                  git: Dict[str, str], delta: Dict[str, List[str]],
                  generated_at: str) -> str:
    bcfg: Dict = info["cfg"]  # type: ignore[assignment]
    files: List[str] = info["files"]  # type: ignore[assignment]
    is_master = bool(bcfg.get("is_master_index"))

    bundle_tokens = 0
    for rel in files:
        txt = read_text(resolve_abs_path(rel))
        if txt:
            bundle_tokens += estimate_tokens(txt)

    out: List[str] = []
    out.append(f"# {bcfg.get('title', name)}")
    out.append("")
    out.append(f"> {bcfg.get('description', '')}")
    out.append("")
    out.append(f"*Generated: {generated_at} · Git: `{git['branch']}` @ `{git['commit'][:12]}` · "
               f"Tier: {bcfg.get('tier', '—')} · Files: {len(files)} · Estimated Tokens: ~{bundle_tokens:,}*")
    out.append("")

    if is_master:
        out.append("---")
        out.append("")
        out.append(render_delta_section(delta, git, result.first_run))
        out.append("---")
        out.append("")
        # Executive Gemini Ingestion & Grounding Guide
        out.append("## Executive Ingestion & Grounding Guide (for LLMs / Gemini)")
        out.append("")
        out.append("This unified repository context is optimized for ingestion into Gemini / LLM Notebooks. Key engineering invariants:")
        out.append("")
        out.append("### 1. Cryptographic Protocol Shapes Analyzer (MITRE CPSA 4.4.9)")
        out.append("- **Order-Sorted Algebras**: Follow Table 10.1–10.6 productions strictly. Protocols using Diffie-Hellman operations **must** declare `(algebra diffie-hellman)` in the top-level `herald` form.")
        out.append("- **Exponent Origination**: In CPSA strand space semantics, exponents (`rndx`, `expt`) are never carried subterms in Dolev-Yao messages. They **must** be declared under `uniq-gen` (unique generated), **never** under `uniq-orig`.")
        out.append("- **3-POV Preskeleton Architecture**: Pure protocol viewpoints (Initiator POV, Responder POV) must contain **zero** listener terms. Secrecy listeners belong **strictly** in dedicated confidentiality skeletons (Skeleton 3) to prevent premature pruning of realized handshake shapes.")
        out.append("- **Pre-Flight Gates**: `cpsa4roletran` only validates `basic` crypto algebra. `diffie-hellman` protocols are pre-flight validated using `cpsa4 -l 1`.")
        out.append("")
        out.append("---")
        out.append("")
        # Bundle catalog
        out.append("## Bundle Catalog")
        out.append("")
        out.append("| Bundle | Title | Files | Size | Estimated Tokens | Tier |")
        out.append("|---|---|---|---|---|---|")
        total_all_tokens = 0
        for bname, binfo in result.bundles.items():
            bc = binfo["cfg"]
            b_files = binfo["files"]
            b_toks = sum(estimate_tokens(read_text(resolve_abs_path(r)) or "") for r in b_files)
            total_all_tokens += b_toks
            b_size_kb = sum(os.path.getsize(resolve_abs_path(r)) for r in b_files if os.path.isfile(resolve_abs_path(r))) / 1024.0
            out.append(f"| `{bname}` | {bc.get('title','')} | {len(b_files)} | {b_size_kb:.1f} KB | ~{b_toks:,} | {bc.get('tier','—')} |")
        out.append("")
        out.append(f"**Total Ingested Context Payload:** ~{total_all_tokens:,} tokens across all bundles ({(total_all_tokens/1_000_000.0)*100:.1f}% of Gemini 1M context window)")
        out.append("")
        if result.auto_detected_executables:
            out.append("## Auto-Detected Executables (shebang / extensionless)")
            out.append("")
            for path, target in result.auto_detected_executables:
                out.append(f"- `{path}` → routed to `{target}`")
            out.append("")
        if result.unclassified:
            out.append("## Unclassified Files (not matched by any bundle rule)")
            out.append("")
            for path in result.unclassified:
                out.append(f"- `{path}`")
            out.append("")
        out.append("---")
        out.append("")
        out.append(render_symbol_registry(result.symbol_registry))  # type: ignore[attr-defined]
        out.append("---")
        out.append("")
        out.append(render_heavy_inventory(result.summarized))
        out.append("---")
        out.append("")

    # Table of contents for this bundle's files
    out.append("## Table of Contents")
    out.append("")
    for rel in files:
        out.append(f"- [`{rel}`](#{anchor(rel)})")
    if not files:
        out.append("_No files matched this bundle's rules in the current repository state._")
    out.append("")
    out.append("---")
    out.append("")

    # File contents
    for rel in files:
        section = render_file_section(rel)
        if section:
            out.append(section)
            out.append("---")
            out.append("")

    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def cmd_sync(cfg: Dict, rebuild: bool) -> int:
    settings: Dict = cfg.get("settings", {})  # type: ignore[assignment]
    out_dir = resolve_abs_path(str(settings.get("output_dir", "notebook_context/bundles")))
    state_path = resolve_abs_path(str(settings.get("state_file", "notebook_context/manifest_state.json")))

    files = discover_files(cfg)
    result = plan_sync(cfg, files)

    old_state = {} if rebuild else load_state(state_path)
    old_files: Dict[str, Dict] = old_state.get("files", {})  # type: ignore[assignment]
    result.first_run = rebuild or not old_files
    delta = diff_states(old_files, result.state_files)
    result.delta = delta

    git = git_context()
    generated_at = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    os.makedirs(out_dir, exist_ok=True)
    written: List[Tuple[str, int, int, float, int]] = []
    total_tokens = 0
    for bname, binfo in result.bundles.items():
        md = render_bundle(bname, binfo, result, git, delta, generated_at)
        dest = os.path.join(out_dir, bname)
        with open(dest, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(md)
        b_tokens = estimate_tokens(md)
        total_tokens += b_tokens
        size_kb = os.path.getsize(dest) / 1024.0
        written.append((bname, len(binfo["files"]), len(md.splitlines()), size_kb, b_tokens))

    new_state = {
        "generated_at": generated_at,
        "git": git,
        "previous_git": old_state.get("git", {}) if isinstance(old_state, dict) else {},
        "config_sha256": sha256_of(CONFIG_PATH),
        "files": result.state_files,
        "delta_of_this_sync": delta,
    }
    save_state(state_path, new_state)

    # ---- console report ----
    print(f"Synced at {generated_at} | git {git['branch']}@{git['commit'][:12]}")
    print(f"Discovered {len(files)} repo & external files (honoring gitignore & bundle rules).")
    print()
    print("Bundles written to", os.path.relpath(out_dir, REPO_ROOT) + "/")
    for bname, nfiles, nlines, size_kb, b_tokens in written:
        print(f"  {bname:<42} files:{nfiles:>4}  lines:{nlines:>7}  size:{size_kb:>8.1f} KB  tokens:~{b_tokens:>8,}")
    print()
    pct_1m = (total_tokens / 1_000_000.0) * 100.0
    print(f"Total Context Payload: ~{total_tokens:,} tokens across all bundles ({pct_1m:.1f}% of Gemini 1M window)")
    print()
    n_inc = sum(1 for r in result.state_files.values() if r["status"] == "included")
    print(f"Included (full text): {n_inc} | Summarized (Tier 4): {len(result.summarized)}")
    if result.auto_detected_executables:
        print("Auto-detected executables:", ", ".join(p for p, _ in result.auto_detected_executables))
    if result.unclassified:
        print("WARNING unclassified files:", ", ".join(result.unclassified))
    print()
    print("Changes since last sync:",
          f"+{len(delta['added'])} added, ~{len(delta['modified'])} modified, -{len(delta['deleted'])} deleted")
    return 0


def cmd_check(cfg: Dict) -> int:
    settings: Dict = cfg.get("settings", {})  # type: ignore[assignment]
    state_path = resolve_abs_path(str(settings.get("state_file", "notebook_context/manifest_state.json")))

    files = discover_files(cfg)
    result = plan_sync(cfg, files)
    old_state = load_state(state_path)
    old_files: Dict[str, Dict] = old_state.get("files", {})  # type: ignore[assignment]
    if not old_files:
        print("No previous manifest state — first run. Use a normal sync to establish the baseline.")
        return 1
    delta = diff_states(old_files, result.state_files)
    git = git_context()
    old_git = old_state.get("git", {})
    print(f"Previous sync: {old_state.get('generated_at','?')} | git {old_git.get('branch','?')}@{str(old_git.get('commit','?'))[:12]}")
    print(f"Current repo:  git {git['branch']}@{git['commit'][:12]} — {git['subject']}")
    total = sum(len(v) for v in delta.values())
    if total == 0:
        print("No drift: repository matches the last sync.")
        return 0
    for label in ("added", "modified", "deleted"):
        items = delta[label]
        print(f"\n{label.upper()} ({len(items)}):")
        for p in items:
            print(f"  {p}")
    print("\nBundles are stale — run: python3 notebook_context/sync_context.py")
    return 1


HOOK_BODY = """#!/bin/sh
# Auto-generated by notebook_context/sync_context.py --install-hook
# Regenerates the LLM Notebook context bundles after every commit.
REPO_ROOT="$(git rev-parse --show-toplevel)"
if [ -x "$(command -v python3)" ]; then
    python3 "$REPO_ROOT/notebook_context/sync_context.py" >/dev/null 2>&1 || \\
        echo "[post-commit] notebook_context sync failed; run it manually." >&2
fi
exit 0
"""


def cmd_install_hook() -> int:
    git_dir = run_git(["rev-parse", "--git-dir"]).strip()
    if not git_dir:
        print("ERROR: not inside a git repository.", file=sys.stderr)
        return 1
    hooks_dir = os.path.join(REPO_ROOT, git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    hook_path = os.path.join(hooks_dir, "post-commit")
    if os.path.exists(hook_path):
        with open(hook_path, "r", encoding="utf-8") as fp:
            existing = fp.read()
        if "sync_context.py" in existing:
            print(f"Hook already installed at {hook_path}")
            return 0
        backup = hook_path + ".bak"
        os.replace(hook_path, backup)
        print(f"Existing post-commit hook backed up to {backup}")
    with open(hook_path, "w", encoding="utf-8") as fp:
        fp.write(HOOK_BODY)
    os.chmod(hook_path, 0o755)
    print(f"Installed post-commit hook: {hook_path}")
    print("Bundles will regenerate automatically after every commit.")
    return 0


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sync_context.py",
        description="Bundle the RFC-LLM repository into Markdown context files for LLM Notebook ingestion.",
    )
    parser.add_argument("--check", action="store_true",
                        help="Dry-run: show what changed since the last sync (exit 1 on drift).")
    parser.add_argument("--rebuild", action="store_true",
                        help="Force full regeneration and reset the delta baseline.")
    parser.add_argument("--install-hook", action="store_true",
                        help="Install a .git/hooks/post-commit hook that re-syncs bundles automatically.")
    args = parser.parse_args(argv)

    if args.install_hook:
        return cmd_install_hook()

    if not os.path.isfile(CONFIG_PATH):
        print(f"ERROR: config not found at {CONFIG_PATH}", file=sys.stderr)
        return 2
    cfg = load_config()

    if args.check:
        return cmd_check(cfg)
    return cmd_sync(cfg, rebuild=args.rebuild)


if __name__ == "__main__":
    sys.exit(main())
