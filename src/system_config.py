"""Global environment, binary paths, execution limits, and provider configuration."""

import os
import shutil
import warnings
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import litellm
from pydantic_settings import BaseSettings

# Suppress third-party LiteLLM verbosity, debug info, and deprecation warnings
litellm.suppress_debug_info = True
litellm.set_verbose = False
litellm.drop_params = True
litellm.request_timeout = 2700
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
    CPSA4SAS_BIN: Path = CABAL_BIN_DIR / "cpsa4sas"
    CPSA4GOALSAT_BIN: Path = CABAL_BIN_DIR / "cpsa4goalsat"

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
    LLM_TIMEOUT_SECONDS: int = 2700
    CPSA_TIMEOUT_SECONDS: int = 15
    ROLETRAN_TIMEOUT_SECONDS: int = 15
    MAX_REPAIR_ATTEMPTS: int = 10

    model_config = {"env_file": ".env", "extra": "ignore"}

    def verify_cpsa_toolchain(self) -> List[str]:
        """Verifies that required MITRE CPSA 4.4.9 binaries exist on disk or PATH.
        Returns a list of missing binary names (empty list if all are present).
        """
        required_bins = [
            ("cpsa4", self.CPSA4_BIN),
            ("cpsa4json", self.CPSA4JSON_BIN),
            ("cpsa4roletran", self.CPSA4ROLETRAN_BIN),
            ("cpsa4shapes", self.CPSA4SHAPES_BIN),
            ("cpsa4graph", self.CPSA4GRAPH_BIN),
        ]
        missing: List[str] = []
        for bin_name, bin_path in required_bins:
            if bin_path.exists() and os.access(bin_path, os.X_OK):
                continue
            found_on_path = shutil.which(bin_name)
            if found_on_path:
                continue
            missing.append(f"{bin_name} (expected at {bin_path})")
        return missing

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

    def get_llm_kwargs(
        self,
        model_name: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
    ) -> Dict[str, Any]:
        """Returns provider-specific arguments (API keys, base URLs, sampling) for LiteLLM."""
        kwargs: Dict[str, Any] = {"model": model_name}
        effective_max_tokens = int(max_tokens) if (max_tokens is not None and max_tokens > 0) else 65536
        kwargs["max_tokens"] = effective_max_tokens
        if temperature is not None:
            kwargs["temperature"] = float(temperature)

        is_local_provider = model_name.startswith("strata/") or model_name.startswith("ollama/")
        if json_mode and not is_local_provider:
            kwargs["response_format"] = {"type": "json_object"}
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
            ollama_base = os.getenv("OLLAMA_API_BASE") or os.getenv("OLLAMA_HOST") or self.OLLAMA_API_BASE
            if ollama_base and not ollama_base.startswith("http"):
                ollama_base = f"http://{ollama_base}"
            kwargs["api_base"] = ollama_base.rstrip("/")
        elif model_name.startswith("gemini/"):
            if self.GEMINI_API_KEY:
                kwargs["api_key"] = self.GEMINI_API_KEY
        elif model_name.startswith("openai/"):
            if self.OPENAI_API_KEY:
                kwargs["api_key"] = self.OPENAI_API_KEY
        elif model_name.startswith("anthropic/"):
            if self.ANTHROPIC_API_KEY:
                kwargs["api_key"] = self.ANTHROPIC_API_KEY

        return kwargs


# Global singleton instance
SYSTEM_CONFIG = SystemEnvironmentConfig()
