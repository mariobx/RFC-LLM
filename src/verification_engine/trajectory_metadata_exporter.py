"""Programmatic Trajectory & Formal Verification Metadata Exporter.

Parses MITRE CPSA 4.4.9 solver outputs (`<stem>.txt` and `<stem>_shapes.txt`),
computes deterministic quality tiers (`GOLD`, `SILVER`, `BRONZE`, `REJECTED`),
prepends structured MoE router conditioning headers to `.scm` files, and writes
the separated `<stem>_trajectory.json` artifact for ROCm Megatron-LM post-training.
"""

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.intermediate_representation.protocol_syntax_tree import CPSAProtocolSpecification
from src.logging_config import get_pipeline_logger

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


def _extract_root_deflistener(sexpr: str) -> Optional[str]:
    """Extracts the listener term from a root preskeleton if `(deflistener ...)` is present outside `(operation ...)`."""
    op_block = _extract_clause_block(sexpr, "operation")
    cleaned = sexpr.replace(op_block, "") if op_block else sexpr
    dl_block = _extract_clause_block(cleaned, "deflistener")
    if not dl_block:
        return None
    inner = re.sub(r"^\(\s*deflistener\s+", "", dl_block[:-1]).strip()
    return inner


def _extract_defstrands(sexpr: str) -> List[Dict[str, Any]]:
    """Extracts all `(defstrand <role> <height> ...)` instances from a skeleton block."""
    # Exclude any `(defstrand ...)` inside `(operation ...)`
    op_block = _extract_clause_block(sexpr, "operation")
    cleaned = sexpr.replace(op_block, "") if op_block else sexpr
    strands: List[Dict[str, Any]] = []
    for match in re.finditer(r"\(\s*defstrand(?:max)?\s+([^\s\(\)]+)(?:\s+(\d+))?", cleaned):
        role_name = match.group(1)
        height = int(match.group(2)) if match.group(2) else None
        strands.append({"role": role_name, "height": height})
    return strands


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
    """Extracts compact search telemetry and dead-branch diagnostics from `<stem>.txt`."""
    if not txt_path or not txt_path.exists():
        return {
            "source_file": txt_path.name if txt_path else None,
            "txt_file_size_bytes": 0,
            "total_explored_labels": 0,
            "dead_branch_nodes_count": 0,
            "step_limit_or_bound_hit": False,
            "state_explosion_detected": False,
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

    dead_diagnostics: List[Dict[str, Any]] = []
    if dead_root_labels:
        target_roots = set(dead_root_labels)
        blocks = split_top_level_sexprs(content)
        parent_to_root: Dict[int, int] = {}
        deepest_dead_per_root: Dict[int, Dict[str, Any]] = {}

        for block in blocks:
            if not block.startswith("(defskeleton"):
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
                op_block = _extract_clause_block(block, "operation")
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
            listener_term = _extract_root_deflistener(block)
            has_listener = listener_term is not None
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
                "realized_shape_labels": [],
                "realized_shapes_count": 0,
                "max_strands_in_realized_shape": 0,
                "instantiated_roles_in_shape": [],
                "is_trivial_single_strand_shape": False,
                "goal_satisfied": _extract_goal_satisfaction(block),
                "verdict": "UNREALIZED",
            }
            if is_shape:
                strands = _extract_defstrands(block)
                group["realized_shape_labels"].append(lbl)
                group["realized_shapes_count"] = 1
                group["max_strands_in_realized_shape"] = len(strands)
                group["instantiated_roles_in_shape"] = strands
            preskeleton_groups.append(group)
        else:
            group_idx = label_to_group_idx.get(parent, len(preskeleton_groups) - 1)
            if lbl is not None and group_idx >= 0:
                label_to_group_idx[lbl] = group_idx
            if is_shape and 0 <= group_idx < len(preskeleton_groups):
                group = preskeleton_groups[group_idx]
                strands = _extract_defstrands(block)
                group["realized_shape_labels"].append(lbl)
                group["realized_shapes_count"] += 1
                if len(strands) >= group["max_strands_in_realized_shape"]:
                    group["max_strands_in_realized_shape"] = len(strands)
                    group["instantiated_roles_in_shape"] = strands
                sat = _extract_goal_satisfaction(block)
                if sat is not None:
                    group["goal_satisfied"] = sat

    total_shapes = 0
    for group in preskeleton_groups:
        shapes_cnt = group["realized_shapes_count"]
        total_shapes += shapes_cnt
        max_strands = group["max_strands_in_realized_shape"]
        if group["skeleton_type"] == "participant_pov":
            if shapes_cnt == 0:
                group["verdict"] = "DEAD_HANDSHAKE"
                group["is_trivial_single_strand_shape"] = False
            elif max_strands >= 2:
                group["verdict"] = "AUTHENTICATED_MULTI_STRAND"
                group["is_trivial_single_strand_shape"] = False
            else:
                group["verdict"] = "TRIVIAL_SINGLE_STRAND"
                group["is_trivial_single_strand_shape"] = True
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


def compute_quality_assessment(
    solver_passed: bool,
    shapes_analysis: Dict[str, Any],
    stage5_attempts_count: int,
    stage6_attempts_count: int,
) -> Dict[str, Any]:
    """Computes the deterministic 4-tier quality grade (`GOLD`, `SILVER`, `BRONZE`, `REJECTED`)."""
    outcomes = shapes_analysis.get("per_preskeleton_outcomes", [])
    participant_povs = [o for o in outcomes if o.get("skeleton_type") == "participant_pov"]
    listener_povs = [o for o in outcomes if o.get("skeleton_type") == "secrecy_listener_pov"]

    if not solver_passed or not outcomes:
        return {
            "quality_tier": "REJECTED",
            "all_participant_povs_realized": False,
            "all_participant_povs_multi_strand": False,
            "all_secrecy_listeners_unrealized": False,
            "post_training_routing": {
                "eligible_for_sft_positive": False,
                "dpo_contrastive_pairs_available": 0,
                "compiler_repair_trajectories_available": stage5_attempts_count + stage6_attempts_count,
            },
        }

    all_povs_realized = bool(participant_povs) and all(
        o.get("realized_shapes_count", 0) > 0 for o in participant_povs
    )
    all_povs_multi_strand = all_povs_realized and all(
        o.get("max_strands_in_realized_shape", 0) >= 2 for o in participant_povs
    )
    all_listeners_unrealized = bool(listener_povs) and all(
        o.get("realized_shapes_count", 0) == 0 for o in listener_povs
    )

    if not all_povs_realized:
        tier = "BRONZE"
    elif all_povs_multi_strand and all_listeners_unrealized:
        tier = "GOLD"
    else:
        tier = "SILVER"

    total_repairs = stage5_attempts_count + stage6_attempts_count
    return {
        "quality_tier": tier,
        "all_participant_povs_realized": all_povs_realized,
        "all_participant_povs_multi_strand": all_povs_multi_strand,
        "all_secrecy_listeners_unrealized": all_listeners_unrealized,
        "post_training_routing": {
            "eligible_for_sft_positive": tier == "GOLD",
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
) -> str:
    """Formats the structured Scheme comment header for MoE router conditioning."""
    sections_str = ", ".join(selected_sections) if selected_sections else "all"
    roles_str = ", ".join(roles) if roles else "none"
    secrecy_str = "PROVED" if secrecy_proved else "UNVERIFIED"
    lines = [
        f";;; [RFC-ID: {rfc_id}]",
        f";;; [PROTOCOL: {protocol_name}]",
        f";;; [SECTIONS: {sections_str}]",
        f";;; [ALGEBRA: {algebra}]",
        f";;; [ROLES: {roles_str}]",
        f";;; [QUALITY-TIER: {quality_tier} | REALIZED-SHAPES: {realized_shapes} | SECRECY: {secrecy_str}]",
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

    stage5_attempts = stage5_record.get("repair_attempts", [])
    stage6_attempts = stage6_record.get("repair_attempts", [])
    quality_assessment = compute_quality_assessment(
        solver_passed=solver_passed,
        shapes_analysis=shapes_analysis,
        stage5_attempts_count=len(stage5_attempts),
        stage6_attempts_count=len(stage6_attempts),
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
        )
        final_scm_with_header = header + clean_scm_body
        final_scm_path.write_text(final_scm_with_header, encoding="utf-8")

    distilled_shapes_content = None
    if shapes_txt_path and shapes_txt_path.exists():
        distilled_shapes_content = shapes_txt_path.read_text(encoding="utf-8", errors="replace")

    stem = (
        final_scm_path.stem
        if final_scm_path
        else (final_spec.protocol_name if final_spec else rfc_id).replace(" ", "_").lower()
    )
    trajectory_path = output_dir / f"{stem}_trajectory.json"

    from src.cost_tracker import GLOBAL_COST_TRACKER
    rfc_cost_summary = GLOBAL_COST_TRACKER.get_current_rfc_summary()

    payload: Dict[str, Any] = {
        "schema_version": "1.0.0",
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
        },
        "stage2_initial_extraction": stage2_record,
        "stage5_preflight_gate": stage5_record,
        "stage6_cpsa4_solver": stage6_full,
        "quality_assessment": quality_assessment,
        "final_verified_output": {
            "final_ast": final_spec.model_dump() if final_spec else None,
            "final_scm_with_header": final_scm_with_header or None,
            "distilled_shapes_txt": distilled_shapes_content,
        },
    }

    with open(trajectory_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    logger.info(
        "Wrote trajectory metadata (%s, shapes=%d) to %s",
        quality_assessment["quality_tier"],
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
    effective_tab_idx = tab_index if tab_index is not None else (len(index_data.get("runs", [])) + 1)

    index_data["runs"].append({
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
        "cost_usd": round(float(rfc_cost.get("total_cost_usd", 0.0)), 6),
        "cost_telemetry": rfc_cost,
    })

    with open(index_path, "w", encoding="utf-8") as handle:
        json.dump(index_data, handle, indent=2)

    return index_path

