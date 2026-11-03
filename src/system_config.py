"""Global environment, binary paths, execution limits, and provider configuration."""

import os
import warnings
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import litellm
from pydantic_settings import BaseSettings

# Suppress third-party LiteLLM verbosity, debug info, and deprecation warnings
litellm.suppress_debug_info = True
litellm.set_verbose = False
litellm.drop_params = True
for _logger_name in ("LiteLLM", "litellm", "LiteLLM Proxy", "LiteLLM Router"):
    logging.getLogger(_logger_name).setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning, module=".*litellm.*")
warnings.filterwarnings("ignore", category=UserWarning, module=".*litellm.*")
warnings.filterwarnings("ignore", message=".*temperature.*")

# Load .env file eagerly from project root (credentials & base URLs only)
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)


class SystemEnvironmentConfig(BaseSettings):
    """Global system file paths, external tool binaries, API credentials, and endpoints."""

    # Project Directories
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
    PROMPTS_DIR: Path = PROJECT_ROOT / "prompts"
    RFCS_DIR: Path = PROJECT_ROOT / "refrences" / "all_RFCs"
    CPSA_KB_DIR: Path = PROJECT_ROOT / "refrences" / "cpsa_kb"
    CHUNKS_DIR: Path = PROJECT_ROOT / "refrences" / "legacy_rag_archive" / "chunks"
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

    # API Keys & Base Endpoints (Loaded from .env)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    NOUS_API_KEY: Optional[str] = os.getenv("NOUS_API_KEY")
    NOUS_API_BASE: str = os.getenv("NOUS_API_BASE", "https://inference-api.nousresearch.com/v1")
    OLLAMA_API_BASE: str = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
    STRATA_API_BASE: str = os.getenv("STRATA_API_BASE", "http://localhost:11435/v1")
    STRATA_API_KEY: str = os.getenv("STRATA_API_KEY", "local-strata")

    # Compiler & Harness Execution Limits
    LLM_TIMEOUT_SECONDS: int = 180
    CPSA_TIMEOUT_SECONDS: int = 15
    ROLETRAN_TIMEOUT_SECONDS: int = 15
    MAX_REPAIR_ATTEMPTS: int = 50

    model_config = {"env_file": ".env", "extra": "ignore"}

    # Live model properties backed directly by `prompts/*.md` YAML frontmatter
    @property
    def DEFAULT_ROUTER_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_APPLICABILITY_GATE, resolve_prompt_model
        return resolve_prompt_model(PROMPT_APPLICABILITY_GATE)

    @property
    def DEFAULT_SECTION_ROUTER_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_SECTION_ROUTER, resolve_prompt_model
        return resolve_prompt_model(PROMPT_SECTION_ROUTER)

    @property
    def DEFAULT_EXTRACTION_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_PROTOCOL_EXTRACTION, resolve_prompt_model
        return resolve_prompt_model(PROMPT_PROTOCOL_EXTRACTION)

    @property
    def DEFAULT_CORRECTION_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_SCHEMA_SELF_CORRECTION, resolve_prompt_model
        return resolve_prompt_model(PROMPT_SCHEMA_SELF_CORRECTION)

    @property
    def DEFAULT_QUERY_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_RAG_QUERY_FORMULATION, resolve_prompt_model
        return resolve_prompt_model(PROMPT_RAG_QUERY_FORMULATION)

    @property
    def DEFAULT_REPAIR_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_COMPILER_REPAIR, resolve_prompt_model
        return resolve_prompt_model(PROMPT_COMPILER_REPAIR)

    @property
    def DEFAULT_THINK_MODEL(self) -> str:
        from src.prompt_loader import PROMPT_THINK_SYNTHESIZER, resolve_prompt_model
        return resolve_prompt_model(PROMPT_THINK_SYNTHESIZER)

    def get_llm_kwargs(self, model_name: str, temperature: Optional[float] = None) -> Dict[str, Any]:
        """Returns provider-specific arguments (API keys, base URLs, sampling) for LiteLLM."""
        kwargs: Dict[str, Any] = {"model": model_name}
        if model_name.startswith("nous/") or model_name.startswith("nousresearch/"):
            target_model = model_name.split("/", 1)[1]
            kwargs["model"] = f"openai/{target_model}"
            kwargs["api_base"] = self.NOUS_API_BASE
            if self.NOUS_API_KEY:
                kwargs["api_key"] = self.NOUS_API_KEY
        elif model_name.startswith("strata/"):
            kwargs["model"] = f"openai/{model_name}"
            kwargs["api_base"] = self.STRATA_API_BASE
            kwargs["api_key"] = self.STRATA_API_KEY
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

        # Omit `temperature` from outbound API requests: modern reasoning & frontier models
        # (gpt-5/6, gemini-3/4, claude, glm-5, deepseek) either reject temperature != 1.0
        # when reasoning is active or perform best at their provider-native default.
        return kwargs


# Global singleton instance
SYSTEM_CONFIG = SystemEnvironmentConfig()
