"""Global pytest fixtures ensuring hermetic test execution without polluting tracked repo logs."""

from pathlib import Path
import pytest

from src.system_config import SYSTEM_CONFIG


@pytest.fixture(autouse=True)
def _hermetic_logs_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Redirects SYSTEM_CONFIG.LOGS_DIR to an isolated temporary folder during pytest runs."""
    temp_logs = tmp_path / "logs"
    temp_logs.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(SYSTEM_CONFIG, "LOGS_DIR", temp_logs)
