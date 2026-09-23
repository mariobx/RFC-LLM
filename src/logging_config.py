"""Comprehensive Structured Logging Subsystem for RFC-LLM Pipeline."""

import logging
import sys
from pathlib import Path
from typing import Optional

from src.system_config import SYSTEM_CONFIG


class PipelineConsoleFormatter(logging.Formatter):
    """ANSI color-coded console formatter for distinct pipeline stages."""

    GREY = "\x1b[38;20m"
    CYAN = "\x1b[36;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    FORMAT_PREFIX = "%(asctime)s | "
    FORMAT_SUFFIX = " | %(name)s - %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + FORMAT_PREFIX + "DEBUG" + FORMAT_SUFFIX + RESET,
        logging.INFO: CYAN + FORMAT_PREFIX + "INFO " + FORMAT_SUFFIX + RESET,
        logging.WARNING: YELLOW + FORMAT_PREFIX + "WARN " + FORMAT_SUFFIX + RESET,
        logging.ERROR: RED + FORMAT_PREFIX + "ERROR" + FORMAT_SUFFIX + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT_PREFIX + "CRIT " + FORMAT_SUFFIX + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.GREY + self.FORMAT_PREFIX + "%(levelname)s" + self.FORMAT_SUFFIX + self.RESET)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def configure_pipeline_logging(
    log_level: int = logging.INFO,
    run_log_file: Optional[Path] = None,
) -> logging.Logger:
    """Configures the root pipeline logger with both console and file handlers."""
    SYSTEM_CONFIG.LOGS_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger("rfc_llm")
    root_logger.setLevel(log_level)

    # Avoid duplicate handlers on re-entry
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 1. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(PipelineConsoleFormatter())
    root_logger.addHandler(console_handler)

    # 2. Global Pipeline File Handler
    global_log_path = SYSTEM_CONFIG.LOGS_DIR / "rfc_llm_pipeline.log"
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    global_file_handler = logging.FileHandler(global_log_path, mode="a", encoding="utf-8")
    global_file_handler.setLevel(logging.DEBUG)  # Always log debug to file
    global_file_handler.setFormatter(file_formatter)
    root_logger.addHandler(global_file_handler)

    # 3. Optional Per-Run File Handler
    if run_log_file:
        run_log_file.parent.mkdir(parents=True, exist_ok=True)
        run_file_handler = logging.FileHandler(run_log_file, mode="w", encoding="utf-8")
        run_file_handler.setLevel(logging.DEBUG)
        run_file_handler.setFormatter(file_formatter)
        root_logger.addHandler(run_file_handler)

    return root_logger


def get_pipeline_logger(subsystem: str) -> logging.Logger:
    """Returns a namespaced child logger for a specific pipeline subsystem."""
    return logging.getLogger(f"rfc_llm.{subsystem}")


class PipelineMetricsCSVLogger:
    """Logs tabular run-level experiment metrics to a persistent CSV for analysis."""

    CSV_HEADER = [
        "timestamp",
        "rfc_id",
        "is_eligible",
        "protocol_name",
        "selected_sections",
        "sliced_lines_count",
        "role_count",
        "preskeleton_count",
        "roletran_passed",
        "solver_passed",
        "shapes_count",
        "duration_seconds",
        "error_message",
    ]

    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or (SYSTEM_CONFIG.LOGS_DIR / "pipeline_runs.csv")
        self._ensure_header()

    def _ensure_header(self) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.csv_path.exists() or self.csv_path.stat().st_size == 0:
            import csv
            with open(self.csv_path, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.CSV_HEADER)

    def log_run(
        self,
        rfc_id: str,
        is_eligible: bool,
        protocol_name: Optional[str] = None,
        selected_sections: Optional[List[str]] = None,
        sliced_lines_count: int = 0,
        role_count: int = 0,
        preskeleton_count: int = 0,
        roletran_passed: Optional[bool] = None,
        solver_passed: Optional[bool] = None,
        shapes_count: int = 0,
        duration_seconds: float = 0.0,
        error_message: Optional[str] = None,
    ) -> None:
        import csv
        import datetime
        now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sec_str = ";".join(selected_sections) if selected_sections else ""
        row = [
            now_iso,
            rfc_id,
            is_eligible,
            protocol_name or "",
            sec_str,
            sliced_lines_count,
            role_count,
            preskeleton_count,
            "" if roletran_passed is None else str(roletran_passed),
            "" if solver_passed is None else str(solver_passed),
            shapes_count,
            round(duration_seconds, 3),
            error_message or "",
        ]
        with open(self.csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
