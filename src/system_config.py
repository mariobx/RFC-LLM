"""System and Environment Configuration for RFC-LLM."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class SystemEnvironmentConfig(BaseSettings):
    """Global system file paths, external tool binaries, and directories."""

    # Project Directories
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    RFCS_DIR: Path = PROJECT_ROOT / "refrences" / "all_RFCs"
    CHUNKS_DIR: Path = PROJECT_ROOT / "refrences" / "chunks"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    DEFAULT_OUTPUT_DIR: Path = PROJECT_ROOT / "output"

    # MITRE CPSA 4.4.9 Binary Paths
    CABAL_BIN_DIR: Path = Path.home() / ".cabal" / "bin"
    CPSA4_BIN: Path = CABAL_BIN_DIR / "cpsa4"
    CPSA4JSON_BIN: Path = CABAL_BIN_DIR / "cpsa4json"
    CPSA4ROLETRAN_BIN: Path = CABAL_BIN_DIR / "cpsa4roletran"
    CPSA4INIT_BIN: Path = CABAL_BIN_DIR / "cpsa4init"
    CPSA4SHAPES_BIN: Path = CABAL_BIN_DIR / "cpsa4shapes"
    CPSA4GRAPH_BIN: Path = CABAL_BIN_DIR / "cpsa4graph"
    CPSA4PROT_BIN: Path = CABAL_BIN_DIR / "cpsa4prot"

    # LLM Settings
    OLLAMA_API_BASE: str = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
    DEFAULT_ROUTER_MODEL: str = os.getenv("LLM_ROUTER_MODEL", "ollama/qwen2.5:7b-instruct")
    DEFAULT_EXTRACTION_MODEL: str = os.getenv("LLM_EXTRACTION_MODEL", "ollama/qwen2.5:7b-instruct")
    DEFAULT_REPAIR_MODEL: str = os.getenv("LLM_REPAIR_MODEL", "ollama/qwen2.5:7b-instruct")

    # Timeouts & Limits
    SUBPROCESS_TIMEOUT_SECONDS: int = 60
    ROLETRAN_TIMEOUT_SECONDS: int = 15
    MAX_REPAIR_ATTEMPTS: int = 50

    model_config = {"env_file": ".env", "extra": "ignore"}


# Global singleton instance
SYSTEM_CONFIG = SystemEnvironmentConfig()
