# Tiered Model Routing & Configuration

## 1. Multi-Model Architecture Rationale

Using a single large frontier model (e.g. Claude Opus or GPT-4o) across all stages of the RFC-to-CPSA pipeline is slow and unnecessarily expensive:
- Document applicability checks and TOC parsing process 10,000+ line tables of contents but require simple boolean decisions.
- Diagnostic query formulation requires stripping concrete variables into abstract search keywords, where frontier reasoning is overkill and high latency hurts iteration speed.
- Semantic extraction demands rigorous formal reasoning, zero operator hallucinations, and strict Pydantic JSON adherence.
- Compiler repair requires multi-turn code debugging where expensive per-token billing accumulates rapidly across 5–15 iterative self-healing passes.

RFC-LLM decouples model invocation across four specialized task tiers:

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 RFC-LLM Task Tiers                     │
                  └──────────────────────────┬─────────────────────────────┘
                                             │
      ┌───────────────────────┬──────────────┴───────────────┬───────────────────────┐
      ▼                       ▼                              ▼                       ▼
 [Tier 1: Query]     [Tier 2: Router/Gate]        [Tier 3: Extraction]        [Tier 4: Repair]
  DeepSeek-Chat           DeepSeek-Chat              Claude Haiku 5.5          Claude Haiku 5.5
(Abstract RAG Query) (High Context / Low Cost)    (Strict Formal AST)        (Iterative Repair)
```

---

## 2. Model Task Assignments & Customizable Prompts (`.prompts/`)

All system prompts for these four tiers are externalized in `.prompts/` and loaded dynamically at runtime via `src/prompt_loader.py`.

### 2.1 RAG Diagnostic Query Formulation (`LLM_QUERY_MODEL`)
- **Active Model**: `nous/deepseek/deepseek-chat`
- **Prompt Template**: `.prompts/05_rag_query_formulation.md`
- **CLI Flag**: `--query-model`
- **Task**: Takes raw compiler error diagnostics from `cpsa4roletran` or `cpsa4` (e.g. `"Roletran REJECT: :6:6: Received term cannot be fully destructured"`) and abstracts them into a 3–6 word conceptual search query for the MITRE CPSA manual (e.g. `"roletran trace reception term destructuring"`).
- **Why DeepSeek-Chat**:
  - Fast, low-cost inference via Nous Portal.
  - Strong conceptual abstraction without leaking concrete protocol identifiers (e.g. `client_random`, `edhoc.scm`).

### 2.2 TOC Router & Document Gatekeeper (`LLM_ROUTER_MODEL`)
- **Active Model**: `nous/deepseek/deepseek-chat`
- **Prompt Templates**: `.prompts/01_applicability_gate.md`, `.prompts/02_section_router.md`
- **CLI Flag**: `--router-model`
- **Tasks**:
  1. `protocol_applicability_gate.py`: Classifies whether an RFC describes an interactive security protocol.
  2. `handshake_section_router.py`: Selects the exact section numbers defining message exchanges from 70+ TOC entries.
- **Why DeepSeek-Chat**:
  - Handles massive Table of Contents context effortlessly.
  - Cost per million tokens is a fraction of frontier models.
  - High accuracy for structured classification and JSON selection.

### 2.3 Protocol Semantic Extraction (`LLM_EXTRACTION_MODEL`)
- **Active Model**: `nous/anthropic/claude-haiku-5.5`
- **Prompt Templates**: `.prompts/03_protocol_extraction.md`, `.prompts/04_schema_self_correction.md`
- **CLI Flag**: `--extraction-model`
- **Task**: Analyzes verbatim RFC section slices (typically 200–600 lines) and constructs the complete `CPSAProtocolSpecification` AST (variables, traces, channels, 3 preskeletons).
- **Why Claude Haiku 5.5**:
  - Superior adherence to strict negative constraints (never outputting `aenc`, never nesting dicts in message terms).
  - Eliminates syntax errors during first-pass extraction.

### 2.4 Self-Healing Compiler Repair (`LLM_REPAIR_MODEL`)
- **Active Model**: `nous/anthropic/claude-haiku-5.5`
- **Prompt Template**: `.prompts/06_compiler_repair.md`
- **CLI Flag**: `--repair-model`
- **Task**: Takes a failing AST, the compiler diagnostic, and retrieved MITRE manual passages, then surgically mutates the AST to fix constructibility or scope errors.
- **Why Claude Haiku 5.5**:
  - High formal methods reasoning precision and strict adherence to Pydantic AST and CPSA 4.4.9 scoping constraints during multi-pass compiler repair.

---

## 3. Unified Nous Research Portal Integration

All third-party models (Claude, DeepSeek, Qwen) route through the **Nous Research Portal** (`portal.nousresearch.com` / `https://inference-api.nousresearch.com/v1`) using LiteLLM's `openai/` proxy protocol.

### 3.1 Implementation in `src/system_config.py`
Any model slug starting with `nous/` or `nousresearch/` is automatically intercepted:
```python
if model_name.startswith("nous/") or model_name.startswith("nousresearch/"):
    clean_model = model_name.split("/", 1)[1]  # e.g. "anthropic/claude-haiku-5.5"
    return {
        "model": f"openai/{clean_model}",
        "api_key": self.NOUS_API_KEY,
        "api_base": self.NOUS_API_BASE,
        "temperature": temperature,
    }
```

### 3.2 Configuration File (`.env`)
```bash
# Nous Research Portal Credentials
NOUS_API_KEY=sk-nous-...
NOUS_API_BASE=https://inference-api.nousresearch.com/v1

# Google Gemini Credentials (Optional Fallback)
GEMINI_API_KEY=AIzaSy...

# Decoupled Model Routing
LLM_QUERY_MODEL=nous/deepseek/deepseek-chat
LLM_ROUTER_MODEL=nous/deepseek/deepseek-chat
LLM_EXTRACTION_MODEL=nous/anthropic/claude-haiku-5.5
LLM_REPAIR_MODEL=nous/anthropic/claude-haiku-5.5

# Subprocess & HTTP Timeouts (Seconds)
SUBPROCESS_TIMEOUT_SECONDS=180
ROLETRAN_TIMEOUT_SECONDS=30
```

---

## 4. Local Workstation Model Endpoints (`100.77.124.9`)

When running local open-weight models instead of cloud APIs, inference requests route over Tailscale to the workstation (`100.77.124.9`):

| Runtime Service | Base Endpoint | OpenAI-Compatible Endpoint | Usage in RFC-LLM |
| :--- | :--- | :--- | :--- |
| **Desktop Ollama (Standard GPU)** | `http://100.77.124.9:11434` | `http://100.77.124.9:11434/v1` | `OLLAMA_API_BASE=http://100.77.124.9:11434` with `ollama/<model>` slugs |
| **Strata (Strix Halo HIP)** | `http://100.77.124.9:11435` | `http://100.77.124.9:11435/v1` | OpenAI-compatible proxy (`openai/<model>` via `http://100.77.124.9:11435/v1`) |

---

## 5. Fallback Hierarchy

In [`src/system_config.py`](file:///home/mario/Work/RFC-LLM/src/system_config.py), `SystemEnvironmentConfig` validates task model assignments using a `@model_validator`:
1. If `LLM_EXTRACTION_MODEL` is blank, falls back to `MODEL_NAME` (global default).
2. If `LLM_ROUTER_MODEL` is blank, falls back to `MODEL_NAME`.
3. If `LLM_REPAIR_MODEL` is blank, falls back to `MODEL_NAME`.
4. If `LLM_QUERY_MODEL` is blank, falls back to `MODEL_NAME`.
5. If `MODEL_NAME` is blank, defaults to `gemini/gemini-3.5-flash-lite`.

This guarantees that leaving any specific task env var empty does not crash the pipeline.

