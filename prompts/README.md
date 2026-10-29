# RFC-LLM Customizable Prompt Templates & Model Routing (`prompts/`)

This directory contains the externalized system prompts **and per-stage LLM routing configuration** driving every LLM step of the RFC-to-CPSA synthesis and Phase 3 `<think>` generation pipelines.

Each `.md` file starts with a YAML frontmatter block defining its `model`, HTTP `timeout` (seconds), and `temperature`. Environment configuration in `.env` (template: [`.env.example`](../.env.example)) holds **only** API credentials (`GEMINI_API_KEY`, `NOUS_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) and base endpoint URLs (`NOUS_API_BASE`, `OLLAMA_API_BASE`, `STRATA_API_BASE`).

```markdown
---
model: strata/unsloth-iq4_xs
timeout: 180
temperature: 0.0
---
You are a formal methods expert...
```

---

## Prompt Catalog & Pipeline Mapping

| Prompt File | Pipeline Stage | Calling Module | Default Timeout / Temp | Supported Provider Prefixes | Uses RAG? |
|---|---|---|---|---|---|
| [`01_applicability_gate.md`](01_applicability_gate.md) | **Stage 1c**: Document Intake (Applicability Gate) | [`src/document_ingestion/protocol_applicability_gate.py`](../src/document_ingestion/protocol_applicability_gate.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | No |
| [`02_section_router.md`](02_section_router.md) | **Stage 1d**: Document Intake (Handshake Section Router) | [`src/document_ingestion/handshake_section_router.py`](../src/document_ingestion/handshake_section_router.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | No |
| [`03_protocol_extraction.md`](03_protocol_extraction.md) | **Stage 2**: JSON CPSA Generation | [`src/semantic_extraction/constrained_protocol_extractor.py`](../src/semantic_extraction/constrained_protocol_extractor.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | **Yes** (Hybrid RRF) |
| [`04_schema_self_correction.md`](04_schema_self_correction.md) | **Stage 2 (Retry)**: 1-Shot Schema & Grammar Self-Correction | [`src/semantic_extraction/constrained_protocol_extractor.py`](../src/semantic_extraction/constrained_protocol_extractor.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | Via Stage 2 context |
| [`05_rag_query_formulation.md`](05_rag_query_formulation.md) | **Stage 5 & 6**: Self-Healing Loop (RAG Query Formulation) | [`src/verification_engine/compiler_diagnostic_repair.py`](../src/verification_engine/compiler_diagnostic_repair.py) | `15s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | **Yes** (Formulates query) |
| [`06_compiler_repair.md`](06_compiler_repair.md) | **Stage 5 & 6**: Self-Healing Loop (Compiler Diagnostic Repair) | [`src/verification_engine/compiler_diagnostic_repair.py`](../src/verification_engine/compiler_diagnostic_repair.py) | `180s` / `0.0` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | **Yes** (Consumes chunks) |
| [`07_think_token_synthesizer.md`](07_think_token_synthesizer.md) | **Phase 3**: Hindsight Reasoning (`<think>`) Synthesizer | [`src/generate_think/dspy_think_synthesizer.py`](../src/generate_think/dspy_think_synthesizer.py) | `180s` / `0.2` | `nous/`, `strata/`, `ollama/`, `gemini/`, `openai/`, `anthropic/` | Trajectory-backed |

---

## Architecture & Live Hot-Reload Guarantees

Prompts and frontmatter metadata are loaded dynamically on every invocation via [`src/prompt_loader.py`](../src/prompt_loader.py):
1. **Zero-Restart Live Hot-Reload**: Editing `model:`, `timeout:`, `temperature:`, or prompt instructions in any `prompts/*.md` file takes effect on the **next LLM call**—even mid-batch—without restarting `./rfc-llm`.
2. **One-Off CLI Overrides**: Passing `--model`, `--router-model`, `--extraction-model`, `--repair-model`, or `--query-model` to `./rfc-llm` (or `--model` to `./rfc-think`) overrides the frontmatter `model:` for that CLI session without modifying `prompts/*.md` on disk.
3. **Frontmatter Stripping & Schema Safety**: [`load_prompt`](../src/prompt_loader.py) strips the `--- ... ---` YAML block before sending the system prompt to LiteLLM, and mandatory Pydantic JSON schemas (`ProtocolApplicabilityReport`, `SectionRoutingDecision`, `CPSAProtocolSpecification`, `SynthesizedReasoningSteps`) are appended automatically in Python.
4. **Template Placeholders**: [`04_schema_self_correction.md`](04_schema_self_correction.md) supports the `{validation_error}` placeholder for 1-shot retry diagnostics.
5. **Resilient Fallback**: If frontmatter fields or `.md` files are missing, [`src/prompt_loader.py`](../src/prompt_loader.py) falls back cleanly to built-in defaults (`GLOBAL_FALLBACK_MODEL = "gemini/gemini-3.5-flash-lite"`).
