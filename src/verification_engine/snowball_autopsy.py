"""CPSA 4.4.9 State-Space Snowball Classifier, Herald Injector, and Partial `.txt` Trace Autopsy.

Strictly isolates state-space explosion / non-termination failures (`timed out`, `Step limit exceeded`,
`Strand bound exceeded`, `Heap exhausted`) from ordinary compiler/syntax errors, and extracts a
surgical derivation autopsy from partial `cpsa4` `.txt` output when deterministic search-order
strategies (`--try-old-strands`, `--check-nonces`, `--reverse-nodes`) cannot resolve an
algebraic unification loop.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple

from src.logging_config import get_pipeline_logger
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("snowball_autopsy")

# Ordered portfolio of CPSA 4.4.9 search-order configurations (Manual §9.1.1 & §10.5)
# Tried deterministically (0 LLM tokens) ONLY when the default cpsa4 search snowballs.
SNOWBALL_HERALD_PORTFOLIO: List[Tuple[str, List[str], List[str]]] = [
    (
        "oldest-strand-first (try-old-strands)",
        ["--try-old-strands"],
        ["try-old-strands"],
    ),
    (
        "oldest-strand + nonce-first (try-old-strands + check-nonces)",
        ["--try-old-strands", "--check-nonces"],
        ["try-old-strands", "check-nonces"],
    ),
    (
        "oldest-strand + nonce-first + youngest-node (try-old-strands + check-nonces + reverse-nodes)",
        ["--try-old-strands", "--check-nonces", "--reverse-nodes"],
        ["try-old-strands", "check-nonces", "reverse-nodes"],
    ),
]

_SNOWBALL_ERROR_MARKERS: Tuple[str, ...] = (
    "timed out after",
    "state-space explosion",
    "infinite strand loop",
    "step limit exceeded",
    "step limit reached",
    "strand bound exceeded",
    "heap exhausted",
    "out of memory",
    "aborting after applying 500 rules",
)


def is_snowball_state_error(error_msg: Optional[str]) -> bool:
    """Returns True strictly when `error_msg` is a CPSA 4.4.9 state-space snowball / non-termination error.

    All other errors (syntax errors, undeclared variables, malformed terms, sort mismatches,
    roletran executability errors, or 0-shape dead skeletons) return False and follow the
    normal pipeline route.
    """
    if not error_msg:
        return False
    lowered = error_msg.lower()
    return any(marker in lowered for marker in _SNOWBALL_ERROR_MARKERS)


def inject_herald_options_into_scm(scm_text: str, herald_options: List[str]) -> str:
    """Injects winning search-order options (e.g. `(try-old-strands)`, `(check-nonces)`)
    into the top-level `(herald ...)` form of a `.scm` file without duplicating existing flags.
    """
    valid_opts = [
        opt for opt in herald_options
        if opt in {"try-old-strands", "check-nonces", "reverse-nodes"}
    ]
    if not valid_opts:
        return scm_text

    herald_match = re.search(r"\(\s*herald\b", scm_text)
    if not herald_match:
        opts_str = " ".join(f"({opt})" for opt in valid_opts)
        return f'(herald "Protocol Verification Suite" {opts_str})\n\n{scm_text}'

    start_idx = herald_match.start()
    depth = 0
    in_string = False
    escape = False
    end_idx = -1

    for idx in range(start_idx, len(scm_text)):
        ch = scm_text[idx]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if not in_string:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end_idx = idx
                    break

    if end_idx == -1:
        return scm_text

    herald_block = scm_text[start_idx:end_idx]
    additions: List[str] = []
    for opt in valid_opts:
        if not re.search(rf"\(\s*{re.escape(opt)}\s*\)", herald_block):
            additions.append(f"({opt})")

    if not additions:
        return scm_text

    updated_herald = f"{herald_block} {' '.join(additions)})"
    return scm_text[:start_idx] + updated_herald + scm_text[end_idx + 1 :]


def _extract_balanced_sexp(text: str, start_pos: int) -> Tuple[str, int]:
    """Extracts a balanced parenthesized S-expression starting at or after `start_pos`."""
    open_idx = text.find("(", start_pos)
    if open_idx == -1:
        return "", len(text)
    depth = 0
    in_string = False
    escape = False
    for idx in range(open_idx, len(text)):
        ch = text[idx]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if not in_string:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return text[open_idx : idx + 1], idx + 1
    return text[open_idx:], len(text)


def _normalize_primed_identifiers(sexp_str: str) -> str:
    """Collapses CPSA primed variable suffixes (`var-0`, `var-1`, `var-12`) to `var-*`
    so repeating augmentation operations across generations group together cleanly.
    """
    collapsed_ws = " ".join(sexp_str.split())
    return re.sub(r"\b([a-zA-Z_][a-zA-Z0-9_\-]*)-\d+\b", r"\1-*", collapsed_ws)


def _parse_skeleton_records(raw_txt: str) -> Tuple[int, Optional[str], List[Dict[str, Any]]]:
    """Parses `(defskeleton ...)` blocks from a partial or bounded `cpsa4` `.txt` file.

    Returns:
        (exploding_pov_index, exploding_pov_desc, parsed_skeleton_records)
    """
    # CPSA emits `(defprotocol ...)` before each top-level POV skeleton search tree,
    # and emits `(comment "Nothing left to do")` when a POV search tree finishes.
    chunks = re.split(r"(?=\(\s*defprotocol\b)", raw_txt)
    protocol_sections = [c for c in chunks if re.match(r"\A\(\s*defprotocol\b", c.strip())]

    target_section = raw_txt
    exploding_pov_idx = 1
    if protocol_sections:
        for idx, sec in enumerate(protocol_sections, 1):
            if '(comment "Nothing left to do")' not in sec:
                target_section = sec
                exploding_pov_idx = idx
                break
        else:
            # If all sections completed or `-l` stopped inside the last section
            target_section = protocol_sections[-1]
            exploding_pov_idx = len(protocol_sections)

    records: List[Dict[str, Any]] = []
    pos = 0
    skel_pattern = re.compile(r"\(\s*defskeleton\b")

    while True:
        match = skel_pattern.search(target_section, pos)
        if not match:
            break
        block, next_pos = _extract_balanced_sexp(target_section, match.start())
        if not block:
            break
        pos = next_pos

        label_m = re.search(r"\(\s*label\s+(\d+)\s*\)", block)
        parent_m = re.search(r"\(\s*parent\s+(\d+)\s*\)", block)
        comment_m = re.search(r'\(\s*comment\s+"([^"]+)"\s*\)', block)
        unrealized_m = re.search(r"\(\s*unrealized\s+([^)]*)\)", block)
        strands = re.findall(r"\(\s*defstrand(?:max)?\s+([^\s()]+)\s+(\d+)", block)

        op_match = re.search(r"\(\s*operation\b", block)
        op_raw = ""
        op_type = ""
        op_action = ""
        op_term = ""
        op_node = ""
        if op_match:
            op_raw, _ = _extract_balanced_sexp(block, op_match.start())
            # Format: (operation <test-type> (<action> ...) <critical-term> (<strand> <node>))
            header_m = re.match(
                r"\(\s*operation\s+([^\s()]+)\s+(\([^)]+\)|[^\s()]+)\s*(.*)\)\Z",
                " ".join(op_raw.split()),
            )
            if header_m:
                op_type = header_m.group(1)
                op_action = header_m.group(2)
                remainder = header_m.group(3).strip()
                node_m = re.search(r"\(\s*(\d+\s+\d+)\s*\)\s*(?:\(\s*seen-ops\b.*\))?\Z", remainder)
                if node_m:
                    op_node = f"({node_m.group(1)})"
                    op_term = remainder[: node_m.start()].strip()
                else:
                    op_term = remainder

        # Parse (vars ...) declarations to inspect primed variable explosion
        vars_match = re.search(r"\(\s*vars\b", block)
        vars_block = ""
        if vars_match:
            vars_block, _ = _extract_balanced_sexp(block, vars_match.start())

        records.append({
            "label": int(label_m.group(1)) if label_m else len(records),
            "parent": int(parent_m.group(1)) if parent_m else None,
            "comment": comment_m.group(1) if comment_m else None,
            "unrealized": " ".join(unrealized_m.group(1).split()) if unrealized_m else "",
            "strands": strands,
            "strand_count": len(strands),
            "op_raw": " ".join(op_raw.split()) if op_raw else "",
            "op_type": op_type,
            "op_action": op_action,
            "op_term": op_term,
            "op_node": op_node,
            "vars_block": vars_block,
        })

    pov_desc = None
    if records:
        first_rec = records[0]
        first_strands = ", ".join(f"{r}(h={h})" for r, h in first_rec["strands"])
        pov_desc = f"POV Skeleton #{exploding_pov_idx}"
        if first_rec.get("comment"):
            pov_desc += f' ("{first_rec["comment"]}")'
        if first_strands:
            pov_desc += f" [Initial strands: {first_strands}]"

    return exploding_pov_idx, pov_desc, records


def _extract_primed_variable_stats(vars_block: str) -> List[Tuple[str, str, int]]:
    """Extracts `(base_var_name, sort, clone_count)` for primed variables (`x-0`, `x-1`, ...)
    inside a skeleton's `(vars ...)` block.
    """
    if not vars_block:
        return []
    decl_groups = re.findall(r"\(([^()]+)\)", vars_block)
    base_counts: Counter[Tuple[str, str]] = Counter()
    for grp in decl_groups:
        tokens = grp.strip().split()
        if len(tokens) < 2 or tokens[0] == "vars":
            continue
        sort_name = tokens[-1]
        for var_tok in tokens[:-1]:
            m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_\-]*)-\d+$", var_tok)
            if m:
                base_counts[(m.group(1), sort_name)] += 1
    ranked = sorted(base_counts.items(), key=lambda kv: (-kv[1], kv[0][0]))
    return [(base, sort_name, count) for (base, sort_name), count in ranked]


def analyze_snowball_trace_text(raw_txt: str) -> str:
    """Analyzes a partial or step-bounded `cpsa4` `.txt` derivation file and returns a
    concise, actionable Snowball Autopsy Report pinpointing the exact looping role,
    authentication test, critical term, and cloned variables.
    """
    if not raw_txt or "(defskeleton" not in raw_txt:
        return ""

    _, pov_desc, records = _parse_skeleton_records(raw_txt)
    if not records:
        return ""

    by_label: Dict[int, Dict[str, Any]] = {r["label"]: r for r in records}
    depth_map: Dict[int, int] = {}
    for r in records:
        lbl = r["label"]
        parent = r["parent"]
        depth_map[lbl] = (depth_map.get(parent, 0) + 1) if parent is not None else 0

    deepest_rec = max(records, key=lambda r: (depth_map.get(r["label"], 0), r["strand_count"]))
    max_depth = depth_map.get(deepest_rec["label"], 0)
    max_strands = max(r["strand_count"] for r in records)

    # Reconstruct the deepest parent -> child derivation chain
    deepest_chain: List[Dict[str, Any]] = []
    curr: Optional[Dict[str, Any]] = deepest_rec
    visited = set()
    while curr is not None and curr["label"] not in visited:
        visited.add(curr["label"])
        deepest_chain.append(curr)
        curr = by_label.get(curr["parent"]) if curr["parent"] is not None else None
    deepest_chain.reverse()

    # Count normalized operations across all skeletons and along the deepest chain
    op_counter: Counter[Tuple[str, str, str]] = Counter()
    chain_op_counter: Counter[Tuple[str, str, str]] = Counter()
    role_spawn_counter: Counter[str] = Counter()

    for r in records:
        if r["op_type"] and r["op_action"]:
            norm_action = _normalize_primed_identifiers(r["op_action"])
            norm_term = _normalize_primed_identifiers(r["op_term"])
            op_counter[(r["op_type"], norm_action, norm_term)] += 1
            added_m = re.match(r"\(\s*added-strand\s+([^\s()]+)\s+(\d+)\s*\)", norm_action)
            if added_m:
                role_spawn_counter[f"{added_m.group(1)} (height {added_m.group(2)})"] += 1

    for r in deepest_chain:
        if r["op_type"] and r["op_action"]:
            norm_action = _normalize_primed_identifiers(r["op_action"])
            norm_term = _normalize_primed_identifiers(r["op_term"])
            chain_op_counter[(r["op_type"], norm_action, norm_term)] += 1

    primed_stats = _extract_primed_variable_stats(deepest_rec.get("vars_block", ""))

    # Build the structured autopsy report
    lines: List[str] = [
        "=== CPSA 4.4.9 SNOWBALL STATE AUTOPSY REPORT (Tier 2 Trace Analysis) ===",
        f"Exploding Query: {pov_desc or 'POV Skeleton'}",
        (
            f"Derivation Stats: {len(records)} skeletons inspected | "
            f"Max derivation depth: {max_depth} | Max concurrent strands in a skeleton: {max_strands}"
        ),
    ]

    if role_spawn_counter:
        top_roles = ", ".join(f"{role}: {cnt}x" for role, cnt in role_spawn_counter.most_common(4))
        lines.append(f"Repeatedly Augmented Roles (`added-strand`): {top_roles}")

    if op_counter:
        lines.append("Top Looping Authentication Test Operations Across Derivation Tree:")
        for (op_type, norm_action, norm_term), count in op_counter.most_common(3):
            chain_cnt = chain_op_counter.get((op_type, norm_action, norm_term), 0)
            lines.append(
                f"  - [{count}x total, {chain_cnt}x in deepest chain] "
                f"Test: `{op_type}` | Action: `{norm_action}` | Unifying Critical Term: `{norm_term[:220]}`"
            )

    if primed_stats:
        cloned_summary = ", ".join(
            f"{base}:{sort_name} (cloned {cnt}x as {base}-0..{base}-{cnt - 1})"
            for base, sort_name, cnt in primed_stats[:6]
        )
        lines.append(f"Cloned Unconstrained Variables in Deepest Skeleton: {cloned_summary}")

    if deepest_rec.get("unrealized"):
        lines.append(f"Remaining Unrealized Reception Nodes in Deepest Skeleton: ({deepest_rec['unrealized']})")

    # Synthesize targeted Tier 3 structural repair directives from the autopsy findings
    lines.append("Targeted Structural Anti-Snowballing Fixes Required (Tier 3):")
    full_ops_str = " ".join(
        f"{t} {a} {term}" for (t, a, term) in op_counter.keys()
    )
    if "encryption-test" in full_ops_str or "(enc " in full_ops_str:
        lines.append(
            "  1. DOMAIN-SEPARATE EVERY `(enc ...)` AND `(hash ...)` TERM: The solver is unifying an outgoing "
            "role encryption with an incoming reception (`encryption-test` loop). Distinguish request vs. response "
            "`[\"enc\", ...]` and `[\"hash\", ...]` terms using the actual RFC message type, header, opcode, or "
            "direction label fields from the RFC (and distinct prefix sorts `data` vs `text`) so order-sorted "
            "unification (`unify_0`) fails immediately between different protocol flights."
        )
    if "(ltk " in full_ops_str or any(s == "name" for _, s, _ in primed_stats):
        lines.append(
            "  2. PRINCIPAL INEQUALITY FACTS & IDENTITY BINDING: Add `[\"neq\", \"<principal_a>\", \"<principal_b>\"]` "
            "to `facts` in every `CPSAPreskeleton` to block `A = B` symmetric reflection, and include both "
            "communicating `name` variables inside encrypted flights so augmented strands bind to existing "
            "principals instead of spawning unconstrained `name-0`, `name-1` peers."
        )
    lines.append(
        "  3. SORT SEPARATION (`data` vs `text`): Declare fresh `uniq-orig` nonces/secrets as sort `\"data\"` "
        "and predictable identifiers/headers/labels as sort `\"text\"` (CPSA Primer §16.2) so CPSA's order-sorted "
        "unifier cannot cross-unify a fresh nonce slot with a metadata/identifier slot."
    )

    return "\n".join(lines)


def generate_snowball_autopsy_report(
    scm_path: Path,
    build_dir: Path,
    env: Dict[str, str],
    partial_trace_text: Optional[str] = None,
    step_limit: int = 120,
) -> str:
    """Generates a deterministic Snowball Autopsy Report from `<stem>.txt` or by running a
    fast (<0.4s) step-bounded `cpsa4 -l <step_limit>` probe when `<stem>.txt` was buffered.
    """
    raw_txt = partial_trace_text or ""
    if raw_txt.count("(defskeleton") < 4 and SYSTEM_CONFIG.CPSA4_BIN.exists():
        autopsy_txt_path = build_dir / f"{scm_path.stem}_autopsy.txt"
        try:
            cmd = [
                str(SYSTEM_CONFIG.CPSA4_BIN),
                "+RTS",
                "-M512m",
                "-N",
                "-RTS",
                "-l",
                str(step_limit),
                "-o",
                str(autopsy_txt_path),
                str(scm_path),
            ]
            subprocess.run(
                cmd,
                cwd=build_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=4.0,
                check=False,
            )
            if autopsy_txt_path.exists():
                probed = autopsy_txt_path.read_text(encoding="utf-8", errors="replace")
                if probed.count("(defskeleton") > raw_txt.count("(defskeleton"):
                    raw_txt = probed
        except Exception as exc:
            logger.debug("Bounded cpsa4 autopsy probe encountered exception: %s", exc)
        finally:
            if autopsy_txt_path.exists():
                try:
                    autopsy_txt_path.unlink()
                except Exception:
                    pass

    return analyze_snowball_trace_text(raw_txt)
