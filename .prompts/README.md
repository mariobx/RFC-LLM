# RFC-LLM Customizable Prompt Templates (`.prompts/`)

This directory contains the externalized system and self-correction prompts driving the 4 LLM stages of the RFC-to-CPSA synthesis pipeline. You can edit any `.md` file in this directory to tune domain instructions, few-shot examples, or formal modeling heuristics without modifying Python code.

---

## Prompt Catalog & Pipeline Mapping

| Prompt File | Pipeline Stage | Calling Module | Configured Model Variable (`.env`) | Uses RAG? |
|---|---|---|---|---|
| [`01_applicability_gate.md`](./01_applicability_gate.md) | **Stage 1c**: Tier 1 Protocol Applicability Gatekeeper | [`src/document_ingestion/protocol_applicability_gate.py`](../src/document_ingestion/protocol_applicability_gate.py) | `LLM_ROUTER_MODEL` | No |
| [`02_section_router.md`](./02_section_router.md) | **Stage 1d**: Handshake & Exchange Section Router | [`src/document_ingestion/handshake_section_router.py`](../src/document_ingestion/handshake_section_router.py) | `LLM_ROUTER_MODEL` | No |
| [`03_protocol_extraction.md`](./03_protocol_extraction.md) | **Stage 2**: Constrained CPSA Protocol Semantic Extraction | [`src/semantic_extraction/constrained_protocol_extractor.py`](../src/semantic_extraction/constrained_protocol_extractor.py) | `LLM_EXTRACTION_MODEL` | **Yes** (Hybrid RRF) |
| [`04_schema_self_correction.md`](./04_schema_self_correction.md) | **Stage 2 (Retry)**: 1-Shot Schema & Grammar Self-Correction | [`src/semantic_extraction/constrained_protocol_extractor.py`](../src/semantic_extraction/constrained_protocol_extractor.py) | `LLM_EXTRACTION_MODEL` | Via Stage 2 context |
| [`05_rag_query_formulation.md`](./05_rag_query_formulation.md) | **Stage 5 & 6**: RAG Compiler Diagnostic Query Formulation | [`src/verification_engine/compiler_diagnostic_repair.py`](../src/verification_engine/compiler_diagnostic_repair.py) | `LLM_QUERY_MODEL` | **Yes** (Formulates query) |
| [`06_compiler_repair.md`](./06_compiler_repair.md) | **Stage 5 & 6**: RAG-Guided Compiler Self-Healing Repair | [`src/verification_engine/compiler_diagnostic_repair.py`](../src/verification_engine/compiler_diagnostic_repair.py) | `LLM_REPAIR_MODEL` | **Yes** (Consumes chunks) |

---

## Architecture & Safety Guarantees

Prompts are loaded dynamically at runtime via [`src/prompt_loader.py`](../src/prompt_loader.py):
1. **Schema Safety**: Mandatory Pydantic JSON schemas (`ProtocolApplicabilityReport`, `SectionRoutingDecision`, `CPSAProtocolSpecification`) are appended automatically in Python *after* loading the Markdown prompt. Editing `.prompts/*.md` will never corrupt the structural JSON contract.
2. **Template Placeholders**: [`04_schema_self_correction.md`](./04_schema_self_correction.md) supports the `{validation_error}` placeholder, which is populated with the exact Pydantic / CPSA 4.4.9 scoping diagnostic when a 1-shot retry is triggered.
3. **Resilient Fallback**: If a file in `.prompts/` is accidentally deleted or empty, [`src/prompt_loader.py`](../src/prompt_loader.py) automatically falls back to its built-in default prompt so pipeline execution never crashes.
