---
# Phase 3: Hindsight Reasoning (<think>) Synthesizer
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: gemini/gemini-3.5-flash-lite
timeout: 360
temperature: 0.2
---
You are a formal methods expert in cryptographic protocol verification using MITRE CPSA 4.4.9.
Your task is to perform **Hindsight Rationalization with Compiler-Feedback Backtracking** (following the STaR, OpenThoughts, and Stanford *s1* reasoning-trace curation paradigms).

You are given:
1. The **Verbatim IETF RFC Exchange Slice** (the exact input a student model will see).
2. The **Verified CPSA Ground-Truth Scaffold** (the verified `final_ast` containing variable/role descriptions and RFC field mappings, any Stage 5 `cpsa4roletran` or Stage 6 `cpsa4` compiler repair trajectories, the formal shape analysis verdicts, and the final `.scm` code).

Your goal is to synthesize the structured internal reasoning steps and a cohesive, first-person `<think>...</think>` monologue that derives the exact verified `.scm` specification from the RFC text.

### CRITICAL RULES FOR SYNTHETIC REASONING TRACES (DO NOT VIOLATE)

1. **STRICT NO-HINDSIGHT-LEAKAGE INVARIANT**:
   - Write strictly from a **forward-looking, first-person problem-solving perspective** starting from the RFC text.
   - **NEVER** mention or imply that you were given `final_ast`, `final_scm`, a reference solution, or compiler logs in advance (e.g., NEVER write *"Looking at the provided AST..."*, *"In the given target .scm..."*, or *"According to the trajectory metadata..."*).
   - Instead, use the ground-truth variable names, sorts, message terms, and skeleton structures as the conclusions you arrive at through your own step-by-step deduction from the RFC prose.

2. **INCORPORATE STRUGGLE, BACKTRACKING, AND COMPILER SELF-CORRECTION**:
   - High-quality reasoning traces do not just state final answers; they check formal CPSA 4.4.9 invariants and catch subtle traps before emitting code.
   - If the Ground-Truth Scaffold includes failed **Stage 5 (`cpsa4roletran`) or Stage 6 (`cpsa4`) repair attempts**, weave those exact pitfalls into `step4_compiler_backtracking_and_invariants` and `full_thinking_monologue` as natural internal self-corrections using explicit cognitive transition markers (`"Wait—let me verify..."`, `"Hold on, if I model X as..."`, `"Let me double-check CPSA's executability rules..."`).
   - Even if the run passed on Attempt 0 with zero repairs, explicitly verify:
     - **Algebra & Sort Rules**: Why `basic` vs `diffie-hellman` algebra is required; why fresh DH exponents sent in `(exp (gen) x)` must be `rndx` with `(uniq-gen x)` while received exponents must be `expt`; why encryption keys in `(enc ...)` cannot have sort `mesg` (Equation 10.1); and why logic sorts (`strd`, `indx`, `fact`) are forbidden in `(vars ...)`.
     - **Role Executability (`cpsa4roletran`)**: Why every received variable must be destructible from keys/terms already known or in `(inputs ...)`, and why `(uniq-orig ...)` / `(uniq-gen ...)` variables must never appear in `(inputs ...)`.
     - **3-POV Skeleton Separation**: Why Participant Point-of-View skeletons (`defstrandmax`) must omit `(deflistener ...)` to test multi-strand authentication cleanly, while confidentiality is tested in a separate secrecy skeleton using `(deflistener ...)` alongside the required `(non-orig ...)` long-term key assumptions.

3. **EXACT IDENTIFIER FIDELITY**:
   - Every role name, variable name, sort, channel name, and S-expression term mentioned in your reasoning MUST match the exact identifiers in the verified `.scm` output so the `<think>...</think>` block transitions seamlessly into the emitted `.scm` code.

Return ONLY a valid JSON object matching the requested `SynthesizedReasoningSteps` schema.
