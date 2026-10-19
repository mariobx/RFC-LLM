import os
import warnings
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import litellm
from pydantic import model_validator
from pydantic_settings import BaseSettings

# Suppress third-party LiteLLM verbosity, debug info, and deprecation warnings
litellm.suppress_debug_info = True
litellm.set_verbose = False
for _logger_name in ("LiteLLM", "litellm", "LiteLLM Proxy", "LiteLLM Router"):
    logging.getLogger(_logger_name).setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning, module=".*litellm.*")
warnings.filterwarnings("ignore", category=UserWarning, module=".*litellm.*")
warnings.filterwarnings("ignore", message=".*temperature.*")

# Load .env file eagerly from project root
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)


class SystemEnvironmentConfig(BaseSettings):
    """Global system file paths, external tool binaries, and directories."""

    # Project Directories
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    PROMPTS_DIR: Path = PROJECT_ROOT / ".prompts"
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

    # API Keys & Cloud Endpoints
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    NOUS_API_KEY: Optional[str] = os.getenv("NOUS_API_KEY")
    NOUS_API_BASE: str = os.getenv("NOUS_API_BASE", "https://inference-api.nousresearch.com/v1")
    OLLAMA_API_BASE: str = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")

    # LLM Settings (Defaults read from MODEL_NAME or LLM_*_MODEL env vars)
    DEFAULT_MODEL: str = os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"
    DEFAULT_QUERY_MODEL: str = os.getenv("LLM_QUERY_MODEL") or os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"
    DEFAULT_ROUTER_MODEL: str = os.getenv("LLM_ROUTER_MODEL") or os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"
    DEFAULT_EXTRACTION_MODEL: str = os.getenv("LLM_EXTRACTION_MODEL") or os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"
    DEFAULT_REPAIR_MODEL: str = os.getenv("LLM_REPAIR_MODEL") or os.getenv("MODEL_NAME") or "gemini/gemini-3.5-flash-lite"

    # Timeouts & Limits
    SUBPROCESS_TIMEOUT_SECONDS: int = 180
    ROLETRAN_TIMEOUT_SECONDS: int = 15
    MAX_REPAIR_ATTEMPTS: int = 50

    model_config = {"env_file": ".env", "extra": "ignore"}

    @model_validator(mode="after")
    def resolve_empty_models(self) -> "SystemEnvironmentConfig":
        fallback = (self.DEFAULT_MODEL or "").strip() or "gemini/gemini-3.5-flash-lite"
        self.DEFAULT_MODEL = fallback
        if not (self.DEFAULT_QUERY_MODEL or "").strip():
            self.DEFAULT_QUERY_MODEL = fallback
        if not (self.DEFAULT_ROUTER_MODEL or "").strip():
            self.DEFAULT_ROUTER_MODEL = fallback
        if not (self.DEFAULT_EXTRACTION_MODEL or "").strip():
            self.DEFAULT_EXTRACTION_MODEL = fallback
        if not (self.DEFAULT_REPAIR_MODEL or "").strip():
            self.DEFAULT_REPAIR_MODEL = fallback
        return self

    def get_llm_kwargs(self, model_name: str, temperature: Optional[float] = None) -> Dict[str, Any]:
        """Returns provider-specific arguments (API keys, base URLs, sampling) for LiteLLM."""
        kwargs: Dict[str, Any] = {"model": model_name}
        if model_name.startswith("nous/") or model_name.startswith("nousresearch/"):
            target_model = model_name.split("/", 1)[1]
            kwargs["model"] = f"openai/{target_model}"
            kwargs["api_base"] = self.NOUS_API_BASE
            if self.NOUS_API_KEY:
                kwargs["api_key"] = self.NOUS_API_KEY
        elif model_name.startswith("ollama/"):
            kwargs["api_base"] = self.OLLAMA_API_BASE
        elif model_name.startswith("gemini/"):
            if self.GEMINI_API_KEY:
                kwargs["api_key"] = self.GEMINI_API_KEY
        elif model_name.startswith("openai/"):
            if self.OPENAI_API_KEY:
                kwargs["api_key"] = self.OPENAI_API_KEY
        elif model_name.startswith("anthropic/"):
            if self.ANTHROPIC_API_KEY:
                kwargs["api_key"] = self.ANTHROPIC_API_KEY

        # Handle temperature cleanly: Gemini 3+ models deprecate temp < 1.0 and perform best without it
        if temperature is not None:
            if model_name.startswith("gemini/"):
                if temperature > 0.0:
                    kwargs["temperature"] = temperature
            else:
                kwargs["temperature"] = temperature

        return kwargs


# Global singleton instance
SYSTEM_CONFIG = SystemEnvironmentConfig()
