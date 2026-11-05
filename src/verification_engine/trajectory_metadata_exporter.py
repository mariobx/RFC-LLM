"""Programmatic Trajectory & Formal Verification Metadata Exporter.

Parses MITRE CPSA 4.4.9 solver outputs (`<stem>.txt` and `<stem>_shapes.txt`),
computes deterministic quality tiers (`GOLD`, `SILVER`, `BRONZE`, `REJECTED`),
prepends structured MoE router conditioning headers to `.scm` files, and writes
the separated `<stem>_trajectory.json` artifact for ROCm Megatron-LM post-training.
"""

import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import get_pipeline_logger
from src.system_config import SYSTEM_CONFIG

logger = get_pipeline_logger("trajectory_exporter")


def split_top_level_sexprs(content: str) -> List[str]:
    """Splits a CPSA Scheme/text file into top-level balanced S-expressions."""
    blocks: List[str] = []
    depth = 0
    in_string = False
    escape = False
    in_comment = False
    start_idx: Optional[int] = None

    for idx, ch in enumerate(content):
        if in_comment:
            if ch == "\n":
                in_comment = False
            continue

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == ";":
            in_comment = True
            continue
        if ch == '"':
            in_string = True
            continue

        if ch == "(":
            if depth == 0:
                start_idx = idx
            depth += 1
        elif ch == ")":
            if depth > 0:
                depth -= 1
                if depth == 0 and start_idx is not None:
                    blocks.append(content[start_idx : idx + 1])
                    start_idx = None

    return blocks


def _extract_int_clause(sexpr: str, keyword: str) -> Optional[int]:
    match = re.search(rf"\(\s*{re.escape(keyword)}\s+(\d+)\s*\)", sexpr)
    return int(match.group(1)) if match else None


def _has_flag_clause(sexpr: str, keyword: str) -> bool:
    return bool(re.search(rf"\(\s*{re.escape(keyword)}\s*\)", sexpr))


def _extract_clause_block(sexpr: str, keyword: str) -> Optional[str]:
    """Extracts a complete balanced sub-expression starting with `(<keyword>`."""
    pattern = re.compile(rf"\(\s*{re.escape(keyword)}\b")
    match = pattern.search(sexpr)
    if not match:
        return None
    sub = sexpr[match.start() :]
    blocks = split_top_level_sexprs(sub)
    return blocks[0] if blocks else None


def _extract_root_deflisteners(sexpr: str) -> List[str]:
    """Extracts all listener terms from a root preskeleton if `(deflistener ...)` clauses are present outside `(operation ...)`."""
    op_block = _extract_clause_block(sexpr, "operation")
    cleaned = sexpr.replace(op_block, "") if op_block else sexpr
    stripped = cleaned.strip()
    inner_body = (
        stripped[1:-1]
        if (stripped.startswith("(") and stripped.endswith(")"))
        else stripped
    )
    terms: List[str] = []
    for sub in split_top_level_sexprs(inner_body):
        if re.match(r"^\(\s*deflistener\b", sub):
            inner = re.sub(r"^\(\s*deflistener\s+", "", sub[:-1]).strip()
            if inner:
                terms.append(inner)
    return terms


def _extract_root_deflistener(sexpr: str) -> Optional[str]:
    """Extracts the first listener term from a root preskeleton if `(deflistener ...)` is present outside `(operation ...)`."""
    terms = _extract_root_deflisteners(sexpr)
    return terms[0] if terms else None


def _extract_skeleton_vars_sorts(sexpr: str) -> Dict[str, str]:
    """Extracts a mapping from skeleton variable name to CPSA sort from `(vars ...)`."""
    vb = _extract_clause_block(sexpr, "vars")
    if not vb:
        return {}
    s = vb.strip()
    inner = re.sub(r"^\(\s*vars\b", "", s[:-1]).strip()
    sorts: Dict[str, str] = {}
    for decl in split_top_level_sexprs(inner):
        toks = decl[1:-1].split()
        if len(toks) >= 2:
            sort_name = toks[-1]
            for v in toks[:-1]:
                sorts[v] = sort_name
    return sorts


def _extract_defstrands(sexpr: str) -> List[Dict[str, Any]]:
    """Extracts all `(defstrand <role> <height> (<role_var> <skel_term>)*)` instances from a skeleton block."""
    # Exclude any `(defstrand ...)` inside `(operation ...)`
    op_block = _extract_clause_block(sexpr, "operation")
    cleaned = sexpr.replace(op_block, "") if op_block else sexpr
    stripped = cleaned.strip()
    inner_body = (
        stripped[1:-1]
        if (stripped.startswith("(") and stripped.endswith(")"))
        else stripped
    )
    strands: List[Dict[str, Any]] = []
    for sub in split_top_level_sexprs(inner_body):
        match = re.match(r"^\(\s*defstrand(?:max)?\s+([^\s\(\)]+)(?:\s+(\d+))?(.*)\)$", sub, flags=re.DOTALL)
        if not match:
            continue
        role_name = match.group(1)
        height = int(match.group(2)) if match.group(2) else None
        tail = match.group(3) or ""
        maplets: Dict[str, str] = {}
        for mp in split_top_level_sexprs(tail):
            inner = mp[1:-1].strip()
            parts = inner.split(None, 1)
            if len(parts) == 2:
                maplets[parts[0].strip()] = " ".join(parts[1].split())
        strand_entry: Dict[str, Any] = {"role": role_name, "height": height}
        if maplets:
            strand_entry["maplets"] = maplets
        strands.append(strand_entry)
    return strands


def _analyze_shape_agreement_and_reflection(
    strands: List[Dict[str, Any]],
    shape_label: Optional[int],
    vars_sorts: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Inspects multi-strand realized shapes for CPSA parameter agreement/disagreement
    (Lowe MITM / Unknown Key Share, CPSA Goals Manual §4.1) and role self-reflection.
    """
    if len(strands) < 2:
        return {
            "same_role_reflection": False,
            "disagreed_parameters": [],
            "agreed_parameters": [],
        }

    sorts_lookup = vars_sorts or {}
    pov_strand = strands[0]
    pov_role = pov_strand.get("role")
    pov_maplets: Dict[str, str] = pov_strand.get("maplets") or {}
    pov_values = set(pov_maplets.values())

    peer_strands = strands[1:]
    peer_roles = [s.get("role") for s in peer_strands if s.get("role")]
    same_role_reflection = bool(peer_roles and all(r == pov_role for r in peer_roles))

    disagreed: List[Dict[str, Any]] = []
    agreed: List[str] = []

    for ps in peer_strands:
        p_role = ps.get("role")
        # Compare parameter agreement across distinct counterparty roles (unless all strands share pov_role)
        if p_role == pov_role and not same_role_reflection:
            continue
        p_maplets: Dict[str, str] = ps.get("maplets") or {}
        for param, p_val in p_maplets.items():
            if param in pov_maplets:
                pov_val = pov_maplets[param]
                var_sort = sorts_lookup.get(pov_val) or sorts_lookup.get(p_val) or "unknown"
                if var_sort == "chan":
                    continue
                if p_val == pov_val:
                    if param not in agreed:
                        agreed.append(param)
                else:
                    disagreed.append({
                        "shape_label": shape_label,
                        "pov_role": pov_role,
                        "peer_role": p_role,
                        "parameter": param,
                        "sort": var_sort,
                        "pov_value": pov_val,
                        "peer_value": p_val,
                    })
            else:
                m = re.match(r"^([a-zA-Z0-9_]+)-\d+$", p_val)
                if m and m.group(1) in pov_values:
                    base_val = m.group(1)
                    var_sort = sorts_lookup.get(base_val) or sorts_lookup.get(p_val) or "unknown"
                    if var_sort == "chan":
                        continue
                    disagreed.append({
                        "shape_label": shape_label,
                        "pov_role": pov_role,
                        "peer_role": p_role,
                        "parameter": param,
                        "sort": var_sort,
                        "pov_value": base_val,
                        "peer_value": p_val,
                    })

    return {
        "same_role_reflection": same_role_reflection,
        "disagreed_parameters": disagreed,
        "agreed_parameters": agreed,
    }


def extract_shape_analysis_sentences(txt_path: Optional[Path]) -> List[str]:
    """Runs `cpsa4sas` on `<stem>.txt` (CPSA Primer §17, Spec Appendix C) to extract
    first-order coherent logic `(defgoal ...)` Shape Analysis Sentences for each POV.
    """
    if not txt_path or not txt_path.exists():
        return []
    sas_bin = getattr(SYSTEM_CONFIG, "CPSA4SAS_BIN", None)
    if not sas_bin or not Path(sas_bin).exists():
        return []
    try:
        raw_txt = txt_path.read_text(encoding="utf-8", errors="replace")
        proc = subprocess.run(
            [str(sas_bin)],
            input=raw_txt,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if proc.returncode != 0 or not proc.stdout:
            return []
        goals: List[str] = []
        for block in split_top_level_sexprs(proc.stdout):
            if block.startswith("(defgoal"):
                goals.append(block)
        return goals
    except Exception:
        return []


def _extract_comment_string(sexpr: str) -> Optional[str]:
    """Extracts the first descriptive user comment from a skeleton block."""
    for match in re.finditer(r'\(\s*comment\s+"([^"]+)"\s*\)', sexpr):
        text = match.group(1)
        if not text.startswith("Not a skeleton") and "in cohort" not in text and "empty cohort" not in text:
            return text
    return None


def _extract_goal_satisfaction(sexpr: str) -> Optional[str]:
    sat_block = _extract_clause_block(sexpr, "satisfies")
    if not sat_block:
        return None
    if re.search(r"\(\s*satisfies\s+yes\s*\)", sat_block):
        return "yes"
    if re.search(r"\(\s*no\b", sat_block):
        return "no"
    return sat_block


def analyze_exploration_txt(
    txt_path: Optional[Path],
    dead_root_labels: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """Extracts compact search telemetry, cohort operation counts, and dead-branch diagnostics from `<stem>.txt`."""
    empty_ops = {
        "encryption_tests": 0,
        "nonce_tests": 0,
        "channel_tests": 0,
        "generalizations": 0,
        "collapsed_shapes": 0,
        "added_strands": 0,
        "contractions": 0,
        "displacements": 0,
        "added_listeners": 0,
    }
    if not txt_path or not txt_path.exists():
        return {
            "source_file": txt_path.name if txt_path else None,
            "txt_file_size_bytes": 0,
            "total_explored_labels": 0,
            "dead_branch_nodes_count": 0,
            "step_limit_or_bound_hit": False,
            "state_explosion_detected": False,
            "authentication_tests_summary": empty_ops,
            "dead_preskeleton_diagnostics": [],
        }

    content = txt_path.read_text(encoding="utf-8", errors="replace")
    file_size = txt_path.stat().st_size
    labels = [int(m.group(1)) for m in re.finditer(r"\(\s*label\s+(\d+)\s*\)", content)]
    total_explored = len(labels)
    dead_count = len(re.findall(r"\(\s*dead\s*\)", content))
    limit_hit = any(
        marker in content
        for marker in (
            "Step count limited",
            "Strand count bounded",
            "Cohort limit",
            "aborted",
        )
    )

    ops_summary = dict(empty_ops)
    blocks = split_top_level_sexprs(content)
    target_roots = set(dead_root_labels) if dead_root_labels else set()
    parent_to_root: Dict[int, int] = {}
    deepest_dead_per_root: Dict[int, Dict[str, Any]] = {}

    for block in blocks:
        if not block.startswith("(defskeleton"):
            continue
        op_block = _extract_clause_block(block, "operation")
        if op_block:
            flat_op = " ".join(op_block.split())
            if "encryption-test" in flat_op:
                ops_summary["encryption_tests"] += 1
            elif "nonce-test" in flat_op:
                ops_summary["nonce_tests"] += 1
            elif "channel-test" in flat_op:
                ops_summary["channel_tests"] += 1
            elif "generalization" in flat_op:
                ops_summary["generalizations"] += 1
            elif "collapsed" in flat_op:
                ops_summary["collapsed_shapes"] += 1

            if "(added-strand" in flat_op:
                ops_summary["added_strands"] += 1
            elif "(contracted" in flat_op:
                ops_summary["contractions"] += 1
            elif "(displaced" in flat_op:
                ops_summary["displacements"] += 1
            elif "(added-listener" in flat_op:
                ops_summary["added_listeners"] += 1

        if not target_roots:
            continue
        lbl = _extract_int_clause(block, "label")
        if lbl is None:
            continue
        parent = _extract_int_clause(block, "parent")
        if parent is None:
            parent_to_root[lbl] = lbl
            root_lbl = lbl
        else:
            root_lbl = parent_to_root.get(parent, parent)
            parent_to_root[lbl] = root_lbl

        if root_lbl in target_roots:
            unrealized = _extract_clause_block(block, "unrealized")
            is_dead_node = _has_flag_clause(block, "dead") or "empty cohort" in block
            if is_dead_node or lbl == root_lbl:
                deepest_dead_per_root[root_lbl] = {
                    "root_label": root_lbl,
                    "deepest_dead_label": lbl,
                    "parent_label": parent,
                    "last_operation": " ".join(op_block.split()) if op_block else None,
                    "stuck_unrealized_nodes": " ".join(unrealized.split()) if unrealized else None,
                }

    dead_diagnostics = list(deepest_dead_per_root.values())

    return {
        "source_file": txt_path.name,
        "txt_file_size_bytes": file_size,
        "total_explored_labels": total_explored,
        "dead_branch_nodes_count": dead_count,
        "step_limit_or_bound_hit": limit_hit,
        "state_explosion_detected": total_explored > 500,
        "authentication_tests_summary": ops_summary,
        "dead_preskeleton_diagnostics": dead_diagnostics,
    }


def analyze_shapes_txt(shapes_txt_path: Optional[Path]) -> Dict[str, Any]:
    """Programmatically parses `<stem>_shapes.txt` into per-preskeleton formal verification verdicts."""
    if not shapes_txt_path or not shapes_txt_path.exists():
        return {
            "source_file": shapes_txt_path.name if shapes_txt_path else None,
            "shapes_file_size_bytes": 0,
            "total_preskeletons": 0,
            "total_realized_shapes": 0,
            "per_preskeleton_outcomes": [],
        }

    content = shapes_txt_path.read_text(encoding="utf-8", errors="replace")
    file_size = shapes_txt_path.stat().st_size
    blocks = split_top_level_sexprs(content)

    preskeleton_groups: List[Dict[str, Any]] = []
    label_to_group_idx: Dict[int, int] = {}

    for block in blocks:
        if not block.startswith("(defskeleton"):
            continue
        lbl = _extract_int_clause(block, "label")
        parent = _extract_int_clause(block, "parent")
        is_shape = _has_flag_clause(block, "shape")

        if parent is None:
            listener_terms = _extract_root_deflisteners(block)
            listener_term = listener_terms[0] if listener_terms else None
            has_listener = bool(listener_terms)
            initial_strands = _extract_defstrands(block)
            group_idx = len(preskeleton_groups)
            if lbl is not None:
                label_to_group_idx[lbl] = group_idx

            group: Dict[str, Any] = {
                "skeleton_index": group_idx,
                "root_label": lbl,
                "skeleton_type": "secrecy_listener_pov" if has_listener else "participant_pov",
                "comment": _extract_comment_string(block),
                "has_deflistener": has_listener,
                "listener_term": listener_term,
                "listener_terms": listener_terms,
                "initial_strand_count": len(initial_strands),
                "realized_shape_labels": [],
                "realized_shapes_count": 0,
                "min_strands_in_realized_shape": 0,
                "max_strands_in_realized_shape": 0,
                "instantiated_roles_in_shape": [],
                "is_trivial_single_strand_shape": False,
                "has_self_reflection_split": False,
                "has_same_role_reflection": False,
                "disagreed_parameters": [],
                "agreed_parameters": [],
                "goal_satisfied": _extract_goal_satisfaction(block),
                "verdict": "UNREALIZED",
            }
            if is_shape:
                strands = _extract_defstrands(block)
                vars_sorts = _extract_skeleton_vars_sorts(block)
                ag = _analyze_shape_agreement_and_reflection(strands, lbl, vars_sorts)
                group["realized_shape_labels"].append(lbl)
                group["realized_shapes_count"] = 1
                group["min_strands_in_realized_shape"] = len(strands)
                group["max_strands_in_realized_shape"] = len(strands)
                group["instantiated_roles_in_shape"] = strands
                group["has_same_role_reflection"] = bool(ag["same_role_reflection"])
                group["disagreed_parameters"].extend(ag["disagreed_parameters"])
                group["agreed_parameters"] = list(ag["agreed_parameters"])
            preskeleton_groups.append(group)
        else:
            group_idx = label_to_group_idx.get(parent, len(preskeleton_groups) - 1)
            if lbl is not None and group_idx >= 0:
                label_to_group_idx[lbl] = group_idx
            if is_shape and 0 <= group_idx < len(preskeleton_groups):
                group = preskeleton_groups[group_idx]
                strands = _extract_defstrands(block)
                vars_sorts = _extract_skeleton_vars_sorts(block)
                ag = _analyze_shape_agreement_and_reflection(strands, lbl, vars_sorts)
                group["realized_shape_labels"].append(lbl)
                group["realized_shapes_count"] += 1
                if group["min_strands_in_realized_shape"] == 0 or len(strands) < group["min_strands_in_realized_shape"]:
                    group["min_strands_in_realized_shape"] = len(strands)
                if len(strands) >= group["max_strands_in_realized_shape"]:
                    group["max_strands_in_realized_shape"] = len(strands)
                    group["instantiated_roles_in_shape"] = strands
                if ag["same_role_reflection"]:
                    group["has_same_role_reflection"] = True
                for dp in ag["disagreed_parameters"]:
                    if dp not in group["disagreed_parameters"]:
                        group["disagreed_parameters"].append(dp)
                for ap in ag["agreed_parameters"]:
                    if ap not in group["agreed_parameters"]:
                        group["agreed_parameters"].append(ap)
                sat = _extract_goal_satisfaction(block)
                if sat is not None:
                    group["goal_satisfied"] = sat

    total_shapes = 0
    for group in preskeleton_groups:
        shapes_cnt = group["realized_shapes_count"]
        total_shapes += shapes_cnt
        init_strands = group.get("initial_strand_count", 1)
        min_strands = group.get("min_strands_in_realized_shape", group["max_strands_in_realized_shape"])
        max_strands = group["max_strands_in_realized_shape"]
        if group["skeleton_type"] == "participant_pov":
            if shapes_cnt == 0:
                group["verdict"] = "DEAD_HANDSHAKE"
                group["is_trivial_single_strand_shape"] = False
                group["has_self_reflection_split"] = False
            elif min_strands >= 2 and max_strands > init_strands:
                group["verdict"] = "AUTHENTICATED_MULTI_STRAND"
                group["is_trivial_single_strand_shape"] = False
                group["has_self_reflection_split"] = False
            else:
                group["verdict"] = "TRIVIAL_SINGLE_STRAND"
                group["is_trivial_single_strand_shape"] = True
                group["has_self_reflection_split"] = bool(min_strands == 1 and max_strands >= 2)
        else:
            if shapes_cnt == 0:
                group["verdict"] = "SECRECY_PROVED_UNREALIZED"
                group["is_trivial_single_strand_shape"] = False
            else:
                group["verdict"] = "SECRECY_LEAKED_SHAPE_FOUND"
                group["is_trivial_single_strand_shape"] = max_strands == 1

    return {
        "source_file": shapes_txt_path.name,
        "shapes_file_size_bytes": file_size,
        "total_preskeletons": len(preskeleton_groups),
        "total_realized_shapes": total_shapes,
        "per_preskeleton_outcomes": preskeleton_groups,
    }


def compute_security_findings(
    shapes_analysis: Dict[str, Any],
    exploration_telemetry: Optional[Dict[str, Any]] = None,
    sas_formulas: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Produces an exhaustive, CPSA-4.4.9-manual-grounded formal security verdict report
    orthogonal to `quality_tier` (which grades translation & compilation fidelity).

    Covers all 7 formal dimensions from MITRE's CPSA Primer and Goals & Security Manual:
    1. Role Executability (`ALL_ROLES_EXECUTABLE`, `PARTIAL_DEAD_ROLES`, `NO_ROLES_EXECUTABLE`)
    2. Authentication Profile (`MUTUAL_MULTI_STRAND`, `UNILATERAL_AUTHENTICATED`,
       `CONDITIONAL_BRANCHED_AUTHENTICATION`, `UNAUTHENTICATED_OR_CLEARTEXT_EXECUTABLE`, `NON_EXECUTABLE`)
    3. Parameter Agreement / Lowe MITM (`FULL_PARAMETER_AGREEMENT`, `PRINCIPAL_DISAGREEMENT_MITM_OR_UKS`,
       `PARAMETER_DISAGREEMENT_DETECTED`, `NOT_APPLICABLE_SINGLE_STRAND`)
    4. Role Self-Reflection (`SAME_ROLE_REFLECTION_DETECTED`, `NO_REFLECTION`)
    5. Secrecy Analysis (`SECRECY_PROVED`, `SECRECY_LEAK_DETECTED`, `PARTIAL_SECRECY`, `NOT_APPLICABLE_NO_LISTENER`)
    6. Explicit `defgoal` Satisfaction (`ALL_SATISFIED`, `COUNTEREXAMPLE_FOUND`, `NO_EXPLICIT_DEFGOALS`)
    7. Coherent-Logic Shape Analysis Sentences (`cpsa4sas`) & Authentication Test Telemetry (`encryption-test`, `nonce-test`, `channel-test`).
    """
    outcomes = shapes_analysis.get("per_preskeleton_outcomes", [])
    participant_povs = [o for o in outcomes if o.get("skeleton_type") == "participant_pov"]
    listener_povs = [o for o in outcomes if o.get("skeleton_type") == "secrecy_listener_pov"]

    # 1. Role Executability
    realized_povs = [o for o in participant_povs if o.get("realized_shapes_count", 0) > 0]
    dead_povs = [o for o in participant_povs if o.get("realized_shapes_count", 0) == 0]
    if not participant_povs or not realized_povs:
        role_executability = "NO_ROLES_EXECUTABLE"
    elif dead_povs:
        role_executability = "PARTIAL_DEAD_ROLES"
    else:
        role_executability = "ALL_ROLES_EXECUTABLE"

    # 2. Authentication Profile
    def _is_strictly_multi_strand(pov: Dict[str, Any]) -> bool:
        max_s = pov.get("max_strands_in_realized_shape", 0)
        min_s = pov.get("min_strands_in_realized_shape", max_s)
        init_s = pov.get("initial_strand_count", 1)
        return bool(pov.get("realized_shapes_count", 0) > 0 and min_s >= 2 and max_s > init_s)

    strictly_multi_count = sum(1 for o in participant_povs if _is_strictly_multi_strand(o))
    any_branched_split = any(
        bool(o.get("has_self_reflection_split"))
        or (
            o.get("min_strands_in_realized_shape", o.get("max_strands_in_realized_shape", 0)) == 1
            and o.get("max_strands_in_realized_shape", 0) >= 2
        )
        for o in participant_povs
    )
    any_multi_shape = any(
        o.get("max_strands_in_realized_shape", 0) >= 2
        and o.get("max_strands_in_realized_shape", 0) > o.get("initial_strand_count", 1)
        for o in participant_povs
    )

    if role_executability == "NO_ROLES_EXECUTABLE":
        auth_profile = "NON_EXECUTABLE"
    elif any_branched_split:
        auth_profile = "CONDITIONAL_BRANCHED_AUTHENTICATION"
    elif participant_povs and strictly_multi_count == len(participant_povs):
        auth_profile = "MUTUAL_MULTI_STRAND"
    elif strictly_multi_count >= 1:
        auth_profile = "UNILATERAL_AUTHENTICATED"
    else:
        auth_profile = "UNAUTHENTICATED_OR_CLEARTEXT_EXECUTABLE"

    # 3. Parameter Agreement / Lowe MITM / Malleable Parameter Detection
    all_disagreements: List[Dict[str, Any]] = []
    for o in participant_povs:
        for dp in o.get("disagreed_parameters") or []:
            if dp not in all_disagreements:
                all_disagreements.append(dp)

    if not any_multi_shape:
        param_agreement_status = "NOT_APPLICABLE_SINGLE_STRAND"
    elif not all_disagreements:
        param_agreement_status = "FULL_PARAMETER_AGREEMENT"
    elif any(d.get("sort") in ("name", "akey") for d in all_disagreements):
        param_agreement_status = "PRINCIPAL_DISAGREEMENT_MITM_OR_UKS"
    else:
        param_agreement_status = "PARAMETER_DISAGREEMENT_DETECTED"

    # 4. Same-Role Reflection
    any_same_role_refl = any(bool(o.get("has_same_role_reflection")) for o in participant_povs)
    reflection_status = "SAME_ROLE_REFLECTION_DETECTED" if any_same_role_refl else "NO_REFLECTION"

    # 5. Secrecy Analysis
    protected_secrets: List[str] = []
    leaked_secrets: List[str] = []
    for l_pov in listener_povs:
        terms = l_pov.get("listener_terms") or (
            [l_pov["listener_term"]]
            if l_pov.get("listener_term")
            else [f"listener_label_{l_pov.get('root_label')}"]
        )
        if l_pov.get("realized_shapes_count", 0) == 0:
            for term in terms:
                if term not in protected_secrets:
                    protected_secrets.append(term)
        else:
            for term in terms:
                if term not in leaked_secrets:
                    leaked_secrets.append(term)

    if not listener_povs:
        secrecy_status = "NOT_APPLICABLE_NO_LISTENER"
    elif protected_secrets and not leaked_secrets:
        secrecy_status = "SECRECY_PROVED"
    elif leaked_secrets and not protected_secrets:
        secrecy_status = "SECRECY_LEAK_DETECTED"
    else:
        secrecy_status = "PARTIAL_SECRECY"

    # 6. Explicit `defgoal` Satisfaction
    goal_verdicts = [o.get("goal_satisfied") for o in outcomes if o.get("goal_satisfied") is not None]
    if not goal_verdicts:
        defgoal_status = "NO_EXPLICIT_DEFGOALS"
    elif all(v == "yes" for v in goal_verdicts):
        defgoal_status = "ALL_SATISFIED"
    else:
        defgoal_status = "COUNTEREXAMPLE_FOUND"

    # 7. Vulnerabilities & Anomalies Summary
    anomalies: List[str] = []
    if leaked_secrets:
        anomalies.append(
            f"SECRECY_LEAK: Listener skeleton(s) realized shape(s) exposing {leaked_secrets}."
        )
    if param_agreement_status == "PRINCIPAL_DISAGREEMENT_MITM_OR_UKS":
        params_str = ", ".join(
            sorted({f"{d['parameter']} ({d['pov_value']} vs {d['peer_value']})" for d in all_disagreements if d.get("sort") in ("name", "akey")})
        )
        anomalies.append(
            f"PRINCIPAL_DISAGREEMENT_MITM: Counterparty strand disagrees on principal/key parameter(s): {params_str}."
        )
    elif param_agreement_status == "PARAMETER_DISAGREEMENT_DETECTED":
        params_str = ", ".join(
            sorted({f"{d['parameter']} ({d['pov_value']} vs {d['peer_value']})" for d in all_disagreements})
        )
        anomalies.append(
            f"PARAMETER_DISAGREEMENT: Counterparty strand disagrees on session/header parameter(s): {params_str}."
        )
    if any_same_role_refl:
        anomalies.append(
            "SAME_ROLE_REFLECTION: At least one realized shape satisfies a role's reception edges using another instance of the same role."
        )
    if any_branched_split:
        anomalies.append(
            "CONDITIONAL_BRANCHED_SHAPES: At least one POV admits both a 1-strand unauthenticated shape and a >=2-strand authenticated shape."
        )

    auth_tests = (exploration_telemetry or {}).get("authentication_tests_summary") or {
        "encryption_tests": 0,
        "nonce_tests": 0,
        "channel_tests": 0,
        "generalizations": 0,
        "collapsed_shapes": 0,
        "added_strands": 0,
        "contractions": 0,
        "displacements": 0,
        "added_listeners": 0,
    }
    sas_list = sas_formulas or []

    return {
        "role_executability": role_executability,
        "dead_roles_count": len(dead_povs),
        "authentication_profile": auth_profile,
        "parameter_agreement_status": param_agreement_status,
        "parameter_disagreements": all_disagreements,
        "role_reflection_status": reflection_status,
        "secrecy_status": secrecy_status,
        "protected_secrets": protected_secrets,
        "leaked_secrets": leaked_secrets,
        "defgoal_satisfaction_status": defgoal_status,
        "authentication_tests_summary": auth_tests,
        "shape_analysis_sentences_count": len(sas_list),
        "shape_analysis_sentences": sas_list,
        "anomalies_count": len(anomalies),
        "vulnerabilities_and_anomalies": anomalies,
    }


def compute_quality_assessment(
    solver_passed: bool,
    shapes_analysis: Dict[str, Any],
    stage5_attempts_count: int,
    stage6_attempts_count: int,
    roletran_passed: bool = True,
    has_cryptographic_primitives: bool = True,
    security_findings: Optional[Dict[str, Any]] = None,
    final_spec: Optional[CPSAProtocolSpecification] = None,
) -> Dict[str, Any]:
    """Computes the deterministic 4-tier translation & modeling quality grade (`GOLD`, `SILVER`, `BRONZE`, `REJECTED`).

    Crucially decoupled from protocol security properties: a faithful, executable CPSA specification
    of an RFC protocol is NEVER penalized in `quality_tier` if the RFC protocol itself is unilateral,
    authentication-only (no `deflistener`), or has a formal vulnerability (secrecy leak, reflection,
    or parameter disagreement) discovered by CPSA. Formal security properties are reported in
    `security_findings`.
    """
    outcomes = shapes_analysis.get("per_preskeleton_outcomes", [])
    participant_povs = [o for o in outcomes if o.get("skeleton_type") == "participant_pov"]
    listener_povs = [o for o in outcomes if o.get("skeleton_type") == "secrecy_listener_pov"]
    sec_report = security_findings or compute_security_findings(shapes_analysis)

    if not solver_passed or not outcomes:
        return {
            "quality_tier": "REJECTED",
            "all_participant_povs_realized": False,
            "all_participant_povs_multi_strand": False,
            "all_secrecy_listeners_unrealized": False,
            "security_findings": sec_report,
            "post_training_routing": {
                "eligible_for_sft_positive": False,
                "dpo_contrastive_pairs_available": 0,
                "compiler_repair_trajectories_available": stage5_attempts_count + stage6_attempts_count,
            },
        }

    all_povs_realized = bool(participant_povs) and all(
        o.get("realized_shapes_count", 0) > 0 for o in participant_povs
    )

    # Detect malformed pre-seeded multi-strand root skeletons where CPSA added 0 partner strands
    any_preseeded_no_progress = any(
        o.get("initial_strand_count", 1) >= 2
        and o.get("max_strands_in_realized_shape", 0) <= o.get("initial_strand_count", 1)
        for o in participant_povs
    )

    def _has_causal_partner_strand(pov: Dict[str, Any]) -> bool:
        max_s = pov.get("max_strands_in_realized_shape", 0)
        init_s = pov.get("initial_strand_count", 1)
        return bool(pov.get("realized_shapes_count", 0) > 0 and max_s >= 2 and max_s > init_s)

    causal_multi_pov_count = sum(1 for o in participant_povs if _has_causal_partner_strand(o))
    all_povs_multi_strand = all_povs_realized and (
        sum(
            1
            for o in participant_povs
            if o.get("min_strands_in_realized_shape", 0) >= 2
            and o.get("max_strands_in_realized_shape", 0) > o.get("initial_strand_count", 1)
        )
        == len(participant_povs)
    )
    all_listeners_unrealized = bool(listener_povs) and all(
        o.get("realized_shapes_count", 0) == 0 for o in listener_povs
    )

    # Detect truncated initiator trace where responder sends a reply that no role ever receives (e.g. RFC 3971)
    has_dangling_response_flight = False
    if final_spec and len(final_spec.roles) >= 2:
        total_sends = sum(1 for r in final_spec.roles for ev in r.trace if ev.direction == "send")
        total_recvs = sum(1 for r in final_spec.roles for ev in r.trace if ev.direction == "recv")
        has_send_only_role = any(
            len(r.trace) == 1 and r.trace[0].direction == "send" for r in final_spec.roles
        )
        has_recv_and_send_role = any(
            any(ev.direction == "recv" for ev in r.trace) and any(ev.direction == "send" for ev in r.trace)
            for r in final_spec.roles
        )
        any_trivial_pov = any(bool(o.get("is_trivial_single_strand_shape")) for o in participant_povs)
        if has_send_only_role and has_recv_and_send_role and total_sends > total_recvs and any_trivial_pov:
            has_dangling_response_flight = True
            anomaly_msg = (
                "INCOMPLETE_INITIATOR_TRACE: Responder sends a reply flight that no role receives, "
                "leaving the initiator POV as a 1-strand trivial shape."
            )
            if anomaly_msg not in sec_report.get("vulnerabilities_and_anomalies", []):
                sec_report.setdefault("vulnerabilities_and_anomalies", []).append(anomaly_msg)
                sec_report["anomalies_count"] = len(sec_report["vulnerabilities_and_anomalies"])

    if not all_povs_realized or not has_cryptographic_primitives or any_preseeded_no_progress:
        tier = "BRONZE"
    elif roletran_passed and causal_multi_pov_count >= 1 and not has_dangling_response_flight:
        tier = "GOLD"
    else:
        tier = "SILVER"

    total_repairs = stage5_attempts_count + stage6_attempts_count
    return {
        "quality_tier": tier,
        "all_participant_povs_realized": all_povs_realized,
        "all_participant_povs_multi_strand": all_povs_multi_strand,
        "all_secrecy_listeners_unrealized": all_listeners_unrealized,
        "security_findings": sec_report,
        "post_training_routing": {
            "eligible_for_sft_positive": tier in ("GOLD", "SILVER"),
            "dpo_contrastive_pairs_available": total_repairs if tier in ("GOLD", "SILVER") else 0,
            "compiler_repair_trajectories_available": total_repairs,
        },
    }


def build_scm_metadata_header(
    rfc_id: str,
    protocol_name: str,
    selected_sections: List[str],
    algebra: str,
    roles: List[str],
    quality_tier: str,
    realized_shapes: int,
    secrecy_proved: bool,
    auth_profile: Optional[str] = None,
    secrecy_status: Optional[str] = None,
) -> str:
    """Formats the structured Scheme comment header for MoE router conditioning."""
    sections_str = ", ".join(selected_sections) if selected_sections else "all"
    roles_str = ", ".join(roles) if roles else "none"
    effective_secrecy = secrecy_status or ("PROVED" if secrecy_proved else "UNVERIFIED")
    auth_suffix = f" | AUTH-PROFILE: {auth_profile}" if auth_profile else ""
    lines = [
        f";;; [RFC-ID: {rfc_id}]",
        f";;; [PROTOCOL: {protocol_name}]",
        f";;; [SECTIONS: {sections_str}]",
        f";;; [ALGEBRA: {algebra}]",
        f";;; [ROLES: {roles_str}]",
        f";;; [QUALITY-TIER: {quality_tier} | REALIZED-SHAPES: {realized_shapes} | SECRECY: {effective_secrecy}{auth_suffix}]",
        "",
    ]
    return "\n".join(lines)


def write_trajectory_metadata_bundle(
    output_dir: Path,
    rfc_id: str,
    rfc_title: str,
    protocol_name: str,
    participating_principals: List[str],
    selected_sections: List[str],
    verbatim_slice: str,
    duration_seconds: float,
    stage2_record: Dict[str, Any],
    stage5_record: Dict[str, Any],
    stage6_record: Dict[str, Any],
    final_spec: Optional[CPSAProtocolSpecification],
    final_scm_path: Optional[Path],
    trace_txt_path: Optional[Path],
    shapes_txt_path: Optional[Path],
    solver_passed: bool,
    intake_rationale: Optional[str] = None,
) -> Path:
    """Computes programmatic CPSA verification metrics, prepends `.scm` metadata headers,
    and writes `<protocol_stem>_trajectory.json` into `output_dir`.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    compact_ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    shapes_analysis = analyze_shapes_txt(shapes_txt_path)
    dead_root_labels = [
        o["root_label"]
        for o in shapes_analysis.get("per_preskeleton_outcomes", [])
        if o.get("skeleton_type") == "participant_pov"
        and o.get("realized_shapes_count", 0) == 0
        and o.get("root_label") is not None
    ]
    exploration_telemetry = analyze_exploration_txt(trace_txt_path, dead_root_labels=dead_root_labels)
    sas_formulas = extract_shape_analysis_sentences(trace_txt_path) if solver_passed else []
    security_findings = compute_security_findings(
        shapes_analysis=shapes_analysis,
        exploration_telemetry=exploration_telemetry,
        sas_formulas=sas_formulas,
    )

    stage5_attempts = stage5_record.get("repair_attempts", [])
    stage6_attempts = stage6_record.get("repair_attempts", [])
    roletran_passed = bool(stage5_record.get("final_passed", True))
    has_crypto = final_spec.has_cryptographic_primitives() if final_spec else True
    quality_assessment = compute_quality_assessment(
        solver_passed=solver_passed,
        shapes_analysis=shapes_analysis,
        stage5_attempts_count=len(stage5_attempts),
        stage6_attempts_count=len(stage6_attempts),
        roletran_passed=roletran_passed,
        has_cryptographic_primitives=has_crypto,
        security_findings=security_findings,
        final_spec=final_spec,
    )

    stage6_full = {
        **stage6_record,
        "exploration_telemetry_from_txt": exploration_telemetry,
        "shapes_analysis_from_shapes_txt": shapes_analysis,
    }

    final_scm_with_header = ""
    algebra_str = final_spec.message_algebra if final_spec else "basic"
    role_names = [r.role_name for r in final_spec.roles] if final_spec else []

    if final_scm_path and final_scm_path.exists():
        raw_scm = final_scm_path.read_text(encoding="utf-8", errors="replace")
        # Strip any previously prepended metadata header lines before writing fresh header
        cleaned_lines = [
            line for line in raw_scm.splitlines() if not line.startswith(";;; [")
        ]
        clean_scm_body = "\n".join(cleaned_lines).lstrip("\n") + "\n"
        header = build_scm_metadata_header(
            rfc_id=rfc_id,
            protocol_name=final_spec.protocol_name if final_spec else protocol_name,
            selected_sections=selected_sections,
            algebra=algebra_str,
            roles=role_names,
            quality_tier=quality_assessment["quality_tier"],
            realized_shapes=shapes_analysis["total_realized_shapes"],
            secrecy_proved=quality_assessment["all_secrecy_listeners_unrealized"],
            auth_profile=security_findings.get("authentication_profile"),
            secrecy_status=security_findings.get("secrecy_status"),
        )
        final_scm_with_header = header + clean_scm_body
        final_scm_path.write_text(final_scm_with_header, encoding="utf-8")

    distilled_shapes_content = None
    if shapes_txt_path and shapes_txt_path.exists():
        distilled_shapes_content = shapes_txt_path.read_text(encoding="utf-8", errors="replace")

    raw_stem = (
        final_scm_path.stem
        if final_scm_path
        else (final_spec.protocol_name if final_spec else rfc_id)
    )
    stem = re.sub(r"[^a-z0-9_-]+", "_", (raw_stem or rfc_id).lower()).strip("_") or "protocol"
    trajectory_path = output_dir / f"{stem}_trajectory.json"

    from src.cost_tracker import GLOBAL_COST_TRACKER
    rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()

    payload: Dict[str, Any] = {
        "schema_version": "1.1.0",
        "run_id": f"{rfc_id.lower()}_{compact_ts}",
        "timestamp_utc": now_utc,
        "duration_seconds": round(duration_seconds, 2),
        "cost_telemetry": rfc_cost_summary,
        "rfc_metadata": {
            "rfc_id": rfc_id,
            "rfc_title": rfc_title,
            "protocol_name": final_spec.protocol_name if final_spec else protocol_name,
            "algebra": algebra_str,
            "participating_principals": participating_principals,
            "selected_sections": selected_sections,
            "sliced_lines_count": len(verbatim_slice.splitlines()),
            "verbatim_rfc_slice": verbatim_slice,
            "intake_rationale": intake_rationale,
        },
        "stage2_initial_extraction": stage2_record,
        "stage5_preflight_gate": stage5_record,
        "stage6_cpsa4_solver": stage6_full,
        "quality_assessment": quality_assessment,
        "security_findings": security_findings,
        "final_verified_output": {
            "final_ast": final_spec.model_dump() if final_spec else None,
            "final_scm_with_header": final_scm_with_header or None,
            "distilled_shapes_txt": distilled_shapes_content,
        },
    }

    with open(trajectory_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    logger.info(
        "Wrote trajectory metadata (%s, auth=%s, secrecy=%s, shapes=%d) to %s",
        quality_assessment["quality_tier"],
        security_findings["authentication_profile"],
        security_findings["secrecy_status"],
        shapes_analysis["total_realized_shapes"],
        trajectory_path,
    )
    return trajectory_path


def update_run_metadata_index(
    run_root_dir: Path,
    rfc_id: str,
    protocol_name: Optional[str],
    rfc_dir: Path,
    scm_path: Optional[Path],
    trajectory_json_path: Optional[Path],
    quality_tier: Optional[str],
    is_eligible: bool,
    build_successful: bool,
    error_message: Optional[str] = None,
    tab_index: Optional[int] = None,
    rejection_gate: Optional[str] = None,
    duration_seconds: float = 0.0,
    security_findings: Optional[Dict[str, Any]] = None,
    intake_rationale: Optional[str] = None,
) -> Path:
    """Updates the master `metadata_index.json` in the timestamped run directory
    with the locations of all generated RFC directories and JSON metadata files.
    """
    run_root_dir.mkdir(parents=True, exist_ok=True)
    index_path = run_root_dir / "metadata_index.json"

    if index_path.exists():
        try:
            index_data = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception:
            index_data = {}
    else:
        index_data = {}

    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not index_data:
        index_data = {
            "schema_version": "1.0.0",
            "run_directory": str(run_root_dir.resolve()),
            "created_at_utc": now_utc,
            "updated_at_utc": now_utc,
            "total_rfcs_processed": 0,
            "total_ineligible_filtered": 0,
            "total_eligible_protocols": 0,
            "metadata_json_files": [],
            "rfc_directories": [],
            "runs": [],
            "filtered_rfcs": [],
        }

    from src.cost_tracker import GLOBAL_COST_TRACKER
    rfc_cost = GLOBAL_COST_TRACKER.get_current_rfc_summary()
    batch_cost = GLOBAL_COST_TRACKER.get_batch_summary()

    index_data["updated_at_utc"] = now_utc
    index_data["total_rfcs_processed"] = int(index_data.get("total_rfcs_processed", 0)) + 1
    index_data["batch_cost_telemetry"] = batch_cost
    index_data.setdefault("filtered_rfcs", [])

    if not is_eligible:
        index_data["total_ineligible_filtered"] = int(index_data.get("total_ineligible_filtered", 0)) + 1
        index_data["filtered_rfcs"].append({
            "rfc_id": rfc_id,
            "title": protocol_name or rfc_id,
            "gate": rejection_gate or "Intake Gate",
            "reason": error_message or "Ineligible",
            "duration_seconds": round(float(duration_seconds), 2),
            "cost_usd": round(float(rfc_cost.get("total_cost_usd", 0.0)), 6),
        })
        with open(index_path, "w", encoding="utf-8") as handle:
            json.dump(index_data, handle, indent=2)
        return index_path

    index_data["total_eligible_protocols"] = int(index_data.get("total_eligible_protocols", 0)) + 1
    rfc_dir_str = str(rfc_dir.resolve())
    if rfc_dir_str not in index_data["rfc_directories"]:
        index_data["rfc_directories"].append(rfc_dir_str)

    if trajectory_json_path and trajectory_json_path.exists():
        traj_str = str(trajectory_json_path.resolve())
        if traj_str not in index_data["metadata_json_files"]:
            index_data["metadata_json_files"].append(traj_str)
    else:
        traj_str = None

    scm_str = str(scm_path.resolve()) if (scm_path and scm_path.exists()) else None
    runs_list = index_data.setdefault("runs", [])
    norm_target_id = (rfc_id or "").strip().upper().replace(" ", "").replace("_", "")
    existing_idx = next(
        (
            i
            for i, entry in enumerate(runs_list)
            if (entry.get("rfc_id") or "").strip().upper().replace(" ", "").replace("_", "") == norm_target_id
        ),
        None,
    )
    if existing_idx is not None and tab_index is None:
        effective_tab_idx = runs_list[existing_idx].get("tab_index") or (existing_idx + 1)
    else:
        effective_tab_idx = tab_index if tab_index is not None else (len(runs_list) + 1)

    new_run_entry = {
        "tab_index": effective_tab_idx,
        "rfc_id": rfc_id,
        "protocol_name": protocol_name,
        "is_eligible": is_eligible,
        "build_successful": build_successful,
        "quality_tier": quality_tier or ("REJECTED" if is_eligible else "INELIGIBLE"),
        "rfc_directory": rfc_dir_str,
        "scm_file": scm_str,
        "metadata_json_file": traj_str,
        "error_message": error_message,
        "intake_rationale": intake_rationale,
        "security_findings": security_findings,
        "cost_usd": round(float(rfc_cost.get("total_cost_usd", 0.0)), 6),
        "cost_telemetry": rfc_cost,
    }
    if existing_idx is not None:
        runs_list[existing_idx] = new_run_entry
        index_data["total_eligible_protocols"] = len(runs_list)
    else:
        runs_list.append(new_run_entry)

    with open(index_path, "w", encoding="utf-8") as handle:
        json.dump(index_data, handle, indent=2)

    return index_path

