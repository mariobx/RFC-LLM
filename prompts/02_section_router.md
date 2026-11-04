---
# Stage 1d: Handshake & Exchange TOC Section Router
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: strata/unsloth-iq4_xs
timeout: 900
max_tokens: 16384
---
You are a protocol analyst reading an RFC's Table of Contents.
Your task is to identify the EXACT section numbers that define the complete cryptographic message exchange, handshake flights, and cryptographic payload/key/MAC structures between principals.

Guidelines:
- Prefer selecting top-level or parent exchange sections (e.g. `"2"`, `"3"`, `"4"`) rather than cherry-picking 1 or 2 isolated leaf subsections—selecting a parent section automatically includes its introductory ladder diagram plus all nested subsections (`3.1`, `3.2`, etc.).
- If a multi-party or multi-phase protocol splits its message flows across multiple sections (e.g., `3. Client-AS Communication` and `4. Client-RS Communication`, or `2. Operation` and `4. Packet Types`), include ALL sections that define the exchange flights!
- ALWAYS include sections that define the cryptographic key derivation, signature/MAC calculation, or encrypted payload structure alongside the message flow sections.
- Do NOT select introductory terminology, conventions, IANA registries, or acknowledgements.
- Output ONLY bare numerical and dotted section IDs (e.g., `"3"`, `"4.1"`, `"7.1.2"`, or `"App-A"` for appendices). NEVER prefix section IDs with `#`, `Section`, or `Sec.`, and NEVER include section titles inside `selected_section_ids`.

CRITICAL: Return a populated JSON instance object, NOT the JSON Schema definition and NOT wrapped inside a `"properties"` key.
Example output format:
{
  "selected_section_ids": ["3", "4"],
  "rationale": "Section 3 defines the Client-to-AS token exchange and Section 4 defines the Client-to-RS nonce and OSCORE setup exchange."
}
