"""MITRE Build Orchestrator for CPSA Verification and Visualization."""

import os
import re
import shutil
import signal
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from src.system_config import SYSTEM_CONFIG
from src.logging_config import get_pipeline_logger

logger = get_pipeline_logger("build_orchestrator")


def _run_make_with_hard_timeout(
    cmd: List[str],
    cwd: Path,
    env: Dict[str, str],
    timeout_seconds: float,
) -> Tuple[int, str, str]:
    """Runs a command in its own process group and hard-kills all child processes (e.g. cpsa4) on timeout."""
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout_str, stderr_str = proc.communicate(timeout=timeout_seconds)
        return proc.returncode, stdout_str or "", stderr_str or ""
    except subprocess.TimeoutExpired as exc:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            proc.kill()
            proc.communicate(timeout=2.0)
        except Exception:
            pass
        raise CPSABuildError(
            f"MITRE CPSA compilation timed out after {timeout_seconds:.0f} seconds "
            f"(state-space explosion / infinite strand loop in {' '.join(cmd)})."
        ) from exc


class CPSABuildArtifacts(BaseModel):
    """Paths to all artifacts emitted by the MITRE CPSA build system."""
    protocol_stem: str = Field(..., description="Base identifier stem for protocol outputs")
    scm_path: Path = Field(..., description="Source MITRE Scheme model file")
    trace_txt_path: Path = Field(..., description="Raw strand space solver derivations (.txt)")
    shapes_txt_path: Path = Field(..., description="Distilled minimal realized shapes (.txt)")
    full_graph_xhtml_path: Path = Field(..., description="Interactive SVG graph of all search steps (.xhtml)")
    shapes_graph_xhtml_path: Path = Field(..., description="Interactive SVG graph of proved shapes (.xhtml)")
    shapes_count: int = Field(default=0, description="Total number of realized shapes discovered")


class CPSABuildError(Exception):
    """Raised when the MITRE make build process fails."""
    pass


def _ensure_cpsa_makefile(target_dir: Path) -> None:
    """Ensures cpsa4init has initialized the official Makefile and cpsa4.mk in target_dir."""
    makefile = target_dir / "Makefile"
    cpsa_mk = target_dir / "cpsa4.mk"

    if makefile.exists() and cpsa_mk.exists():
        return

    logger.info("Initializing MITRE CPSA Makefile in %s via cpsa4init", target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    if not SYSTEM_CONFIG.CPSA4INIT_BIN.exists():
        raise FileNotFoundError(f"cpsa4init binary missing at {SYSTEM_CONFIG.CPSA4INIT_BIN}")

    proc = subprocess.run(
        [str(SYSTEM_CONFIG.CPSA4INIT_BIN)],
        cwd=target_dir,
        capture_output=True,
        text=True,
        check=False,
    )

    if proc.returncode != 0:
        logger.error("cpsa4init failed in %s: %s", target_dir, proc.stderr)
        raise CPSABuildError(f"cpsa4init initialization failed: {proc.stderr}")


def _count_shapes_in_file(shapes_txt_path: Path) -> int:
    """Counts the number of distinct realized shape skeletons in the shape summary file."""
    if not shapes_txt_path.exists():
        return 0
    try:
        with open(shapes_txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        shape_flags = re.findall(r"\(\s*shape\s*\)", content)
        if shape_flags:
            return len(shape_flags)
        matches = re.findall(r"\(defskeleton\s+", content)
        return len(matches)
    except Exception as e:
        logger.warning("Could not count shapes in %s: %s", shapes_txt_path, e)
        return 0


def execute_mitre_make_build(
    scm_path: Path,
    output_directory: Optional[Path] = None,
    build_full_graph: bool = True,
) -> CPSABuildArtifacts:
    """Orchestrates GNU Make to compile a Scheme model through cpsa4, cpsa4shapes, and cpsa4graph."""
    build_dir = output_directory or scm_path.parent
    build_dir.mkdir(parents=True, exist_ok=True)

    _ensure_cpsa_makefile(build_dir)

    stem = scm_path.stem
    target_scm_in_build = build_dir / f"{stem}.scm"

    # Ensure scm file is located in build_dir
    if scm_path.resolve() != target_scm_in_build.resolve():
        shutil.copy(scm_path, target_scm_in_build)

    logger.info("Executing MITRE make build for '%s' in %s", stem, build_dir)

    # Inject ~/.cabal/bin into subprocess PATH so GNU make resolves cpsa4, cpsa4shapes, cpsa4graph
    env = os.environ.copy()
    cabal_bin_str = str(SYSTEM_CONFIG.CABAL_BIN_DIR)
    env["PATH"] = f"{cabal_bin_str}:{env.get('PATH', '')}"

    # Remove stale derived artifacts before running make so each attempt is fresh
    for stale_name in (f"{stem}.txt", f"{stem}_shapes.txt", f"{stem}_shapes.xhtml", f"{stem}.xhtml"):
        stale_file = build_dir / stale_name
        if stale_file.exists():
            stale_file.unlink()

    max_budget_sec = min(60.0, float(getattr(SYSTEM_CONFIG, "CPSA_TIMEOUT_SECONDS", 60)))
    start_ts = time.monotonic()

    # Target 1: Minimal shapes graph (triggers cpsa4, cpsa4shapes, and cpsa4graph)
    target_shapes_xhtml = f"{stem}_shapes.xhtml"
    rc_shapes, out_shapes, err_shapes = _run_make_with_hard_timeout(
        ["make", "-B", target_shapes_xhtml],
        cwd=build_dir,
        env=env,
        timeout_seconds=max_budget_sec,
    )

    if rc_shapes != 0:
        err_msg = err_shapes.strip() or out_shapes.strip()
        logger.error("Make build failed for %s: %s", target_shapes_xhtml, err_msg)
        raise CPSABuildError(f"MITRE build failed for {target_shapes_xhtml}: {err_msg}")

    # Target 2 (Optional): Full derivation search graph (capped within remaining 60s budget)
    if build_full_graph:
        remaining_sec = max(1.0, max_budget_sec - (time.monotonic() - start_ts))
        target_full_xhtml = f"{stem}.xhtml"
        try:
            _run_make_with_hard_timeout(
                ["make", target_full_xhtml],
                cwd=build_dir,
                env=env,
                timeout_seconds=remaining_sec,
            )
        except CPSABuildError:
            logger.warning("Full derivation graph %s exceeded remaining budget; keeping shapes graph.", target_full_xhtml)

    # Verify generated artifact paths
    trace_txt = build_dir / f"{stem}.txt"
    shapes_txt = build_dir / f"{stem}_shapes.txt"
    full_xhtml = build_dir / f"{stem}.xhtml"
    shapes_xhtml = build_dir / f"{stem}_shapes.xhtml"

    for artifact in [trace_txt, shapes_txt, shapes_xhtml]:
        if not artifact.exists():
            raise CPSABuildError(f"Expected build artifact {artifact} was not produced by make")

    shapes_count = _count_shapes_in_file(shapes_txt)
    logger.info("Build SUCCESS: Generated %s with %d realized shapes", shapes_xhtml.name, shapes_count)

    return CPSABuildArtifacts(
        protocol_stem=stem,
        scm_path=target_scm_in_build,
        trace_txt_path=trace_txt,
        shapes_txt_path=shapes_txt,
        full_graph_xhtml_path=full_xhtml if full_xhtml.exists() else shapes_xhtml,
        shapes_graph_xhtml_path=shapes_xhtml,
        shapes_count=shapes_count,
    )
