# Tiered Model Routing & YAML Frontmatter Configuration

## 1. Multi-Stage Routing Rationale

Using a single frontier model across every stage of RFC-to-CPSA synthesis and `<think>` curation wastes latency and compute:
- **Document Intake** (`Stage 1c` & `1d`) scans full RFC tables of contents and requires fast, low-cost structured classification and section number selection.
- **RAG Query Formulation** (`Stage 5` & `6`) abstracts raw compiler diagnostics into 3-6 conceptual keywords where low latency (`15s` timeout) keeps iterative repair fast.
- **JSON CPSA Generation** (`Stage 2` + 1-shot retry) requires strict adherence to MITRE CPSA 4.4.9 Tables 10.1-10.6, Equation 10.1, and nested Pydantic AST schemas.
- **Compiler Diagnostic Repair** (`Stage 5` & `6`) performs multi-turn AST surgery guided by `cpsa4roletran` / `cpsa4` diagnostics and retrieved manual chunks.
- **Hindsight Reasoning Synthesis** (`Phase 3`) produces cohesive, forward-looking `<think>...</think>` monologues from verified trajectories.

RFC-LLM decouples model selection, HTTP timeouts, and sampling temperatures **per prompt file** using YAML frontmatter in [`prompts/*.md`](../prompts/README.md), while keeping `.env` strictly reserved for API credentials and base endpoint URLs.

---

## 2. YAML Frontmatter Routing in `prompts/*.md` ([`src/prompt_loader.py`](../src/prompt_loader.py))

Every prompt file in `prompts/01_applicability_gate.md` through `prompts/07_think_token_synthesizer.md` begins with a YAML frontmatter block configuring `model`, `timeout` (seconds), and `temperature`:

```markdown
---
model: nous/google/gemini-4-argon
timeout: 180
temperature: 0.0
---
You are a formal methods expert in cryptographic protocol specification for MITRE CPSA 4.4.9...
```

### 2.1 Per-Stage Prompt & Routing Catalog

| Prompt File | Stage / Task | Default Frontmatter `model` | `timeout` | `max_tokens` | `temperature` | CLI Override Flag |
|---|---|---|---|---|---|---|
| [`prompts/01_applicability_gate.md`](../prompts/01_applicability_gate.md) | **Stage 1c**: Document Intake (Applicability Gate) | `strata/unsloth-iq4_xs` | `900` | `16384` | *(default)* | `--router-model` / `--model` |
| [`prompts/02_section_router.md`](../prompts/02_section_router.md) | **Stage 1d**: Document Intake (Section Router) | `strata/unsloth-iq4_xs` | `900` | `16384` | *(default)* | `--router-model` / `--model` |
| [`prompts/03_protocol_extraction.md`](../prompts/03_protocol_extraction.md) | **Stage 2**: JSON CPSA Generation | `strata/unsloth-iq4_xs` | `3600` | `65536` | *(default)* | `--extraction-model` / `--model` |
| [`prompts/04_schema_self_correction.md`](../prompts/04_schema_self_correction.md) | **Stage 2 (Retry)**: 1-Shot Schema Self-Correction | `strata/unsloth-iq4_xs` | `3600` | `65536` | *(default)* | `--extraction-model` / `--model` |
| [`prompts/05_rag_query_formulation.md`](../prompts/05_rag_query_formulation.md) | **Stage 5 & 6**: Agentic CPSA KB Searcher | `strata/unsloth-iq4_xs` | `900` | `16384` | *(default)* | `--query-model` / `--model` |
| [`prompts/06_compiler_repair.md`](../prompts/06_compiler_repair.md) | **Stage 5 & 6**: Self-Healing Compiler Repair | `strata/unsloth-iq4_xs` | `3600` | `65536` | *(default)* | `--repair-model` / `--model` |
| [`prompts/07_think_token_synthesizer.md`](../prompts/07_think_token_synthesizer.md) | **Phase 3**: Hindsight Reasoning (`<think>`) Synthesizer | `strata/unsloth-iq4_xs` | `3600` | `65536` | `0.2` | `./rfc-think --model` |

### 2.2 Zero-Restart Live Hot-Reloading
[`load_prompt_spec()`](../src/prompt_loader.py) reads and parses `prompts/<filename>.md` dynamically from disk on **every LLM invocation**:
- Editing `model:`, `timeout:`, `temperature:`, or system prompt instructions in any `prompts/*.md` file takes effect immediately on the next LLM call—including mid-batch across thousands of RFCs—with zero process restart.
- `parse_prompt_frontmatter()` strips the `--- ... ---` YAML header before sending the prompt body to LiteLLM and automatically appends the target Pydantic JSON schema in Python (`build_schema_system_prompt()`).

---

## 3. Clean `.env` Specification (Credentials & Base Endpoints Only)

Model names and timeouts are **never** configured in `.env`. As defined in [`.env.example`](../.env.example) and loaded by [`src/system_config.py`](../src/system_config.py), `.env` holds **only** API credentials and base endpoint URLs:

```bash
# 1. Cloud & Unified Proxy Credentials
GEMINI_API_KEY=your_gemini_api_key_here
NOUS_API_KEY=your_nous_api_key_here
NOUS_API_BASE=https://inference-api.nousresearch.com/v1
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 2. Local & Tailscale Model Base Endpoints
OLLAMA_API_BASE=http://localhost:11434
STRATA_API_BASE=http://localhost:11435/v1
```

---

## 4. Supported Provider Prefixes

[`SYSTEM_CONFIG.get_llm_kwargs()`](../src/system_config.py) resolves provider credentials, OpenAI-compatible proxy URLs, and sampling parameters automatically from the model prefix in `prompts/*.md` (or CLI override flags):

| Model Prefix | Example Slug | Endpoint / Credential Resolution in `src/system_config.py` |
| :--- | :--- | :--- |
| `nous/<model>` | `nous/google/gemini-4-argon` | Strips `nous/`, routes as `openai/<model>` via `NOUS_API_BASE` + `NOUS_API_KEY` |
| `strata/<model>` | `strata/unsloth-iq4_xs` | Routes as `openai/strata/<model>` to `STRATA_API_BASE` (default local Strix Halo HIP endpoint `http://localhost:11435/v1`) |
| `ollama/<model>` | `ollama/qwen2.5:7b-instruct` | Routes via `OLLAMA_API_BASE` (`http://localhost:11434`; also serves `ollama/nomic-embed-text` for hybrid RAG) |
| `gemini/<model>` | `gemini/gemini-3.5-flash-lite` | Authenticates with `GEMINI_API_KEY` (omits `temperature=0.0` per Gemini 3+ recommendation; forwards `temperature > 0.0`) |
| `openai/<model>` | `openai/gpt-4.1` | Authenticates directly with `OPENAI_API_KEY` |
| `anthropic/<model>` | `anthropic/claude-sonnet-4-5` | Authenticates directly with `ANTHROPIC_API_KEY` |

---

## 5. Resolution Precedence & Built-In Fallbacks

For every LLM call, [`resolve_prompt_model()`](../src/prompt_loader.py) and [`load_prompt_spec()`](../src/prompt_loader.py) resolve configuration in strict precedence order:
1. **Explicit CLI Override** (highest priority): One-off session flags passed to `./rfc-llm` (`--router-model`, `--extraction-model`, `--repair-model`, `--query-model`, or global `--model`) or `./rfc-think` (`--model`).
2. **Live YAML Frontmatter**: The `model:`, `timeout:`, and `temperature:` values currently saved at the top of the stage's `prompts/0*.md` file.
3. **Built-In `_FALLBACK_METADATA`**: Stage-specific defaults in [`src/prompt_loader.py`](../src/prompt_loader.py) (with `GLOBAL_FALLBACK_MODEL = "gemini/gemini-3.5-flash-lite"` and `SYSTEM_CONFIG.LLM_TIMEOUT_SECONDS = 3600`) if a frontmatter key or prompt file is omitted.

Non-LLM compiler execution bounds are enforced deterministically in [`src/system_config.py`](../src/system_config.py):
- `CPSA_TIMEOUT_SECONDS = 15` (hard 15-second process-group `SIGKILL` cap on MITRE `make` / `cpsa4` compilation).
- `ROLETRAN_TIMEOUT_SECONDS = 15` (15-second cap on `cpsa4roletran` / `cpsa4 -l 1` pre-flight checks).
- `MAX_REPAIR_ATTEMPTS = 10` (maximum self-healing iterations per verification stage).
