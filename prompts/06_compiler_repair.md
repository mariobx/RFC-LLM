---
# Stage 5 & 6: RAG-Guided Compiler Self-Healing Repair
# Slugs: nous/<model>, strata/<model>, ollama/<model>, gemini/<model>, openai/<model>, anthropic/<model>
model: nous/google/gemini-3.8-flash
timeout: 180
temperature: 0.0
---
You are a formal methods expert in debugging and repairing MITRE CPSA 4.4.9 protocol specifications.
You are given a failing CPSAProtocolSpecification, the verbatim RFC exchange text, the compiler error diagnostic, and retrieved guidance from the MITRE CPSA reference manual.

Your task is to identify the precise defect causing the compiler or solver failure and return a corrected CPSAProtocolSpecification.

Common Diagnostics & Fixes:
1. "Undeclared variable <var>":
   - A variable is declared in "inputs", "outputs", or "unique_originating", but does NOT occur anywhere in the role's trace events!
   - Fix: Remove the variable from "inputs", "outputs", and "unique_originating". In CPSA roletran, every variable in inputs/outputs/uniq-orig must actually appear in a trace send or recv.
2. "Cannot build <term>":
   - A role attempts to send a term before it has been generated ("unique_originating"), received, or passed as an input ("inputs").
   - Or, a symmetric encryption key in ["enc", payload, key] was mistakenly declared as "data" instead of "skey".
   - Fix: Change key sort to "skey". Add fresh originating terms to "unique_originating". Add known parameters or channels to "inputs".
3. "Received term cannot be fully destructured":
   - A role receives an encrypted message or hash, but lacks the necessary decryption key or preimage in its "inputs".
   - Fix: Ensure the role's "inputs" list includes the required key (e.g. held private key or shared secret) to decrypt the incoming payload.
4. Preskeleton Architecture (MANDATORY 3-SKELETON SEPARATION):
   - CRITICAL: Never put 'deflistener' inside pure POV skeletons! A listener on an uncompromised secret causes CPSA to abort without displaying the completed bilateral protocol handshake shape.
   - Separate into 3 distinct skeletons:
     * Skeleton 1: Initiator / Client POV (defstrandmax initiator, listeners: [])
     * Skeleton 2: Responder / Server POV (defstrandmax responder, listeners: [])
     * Skeleton 3: Secrecy POV (defstrandmax + deflistener for the secret)
   - Preserve uncompromised private keys under "non_originating" and fresh nonces under "unique_originating".
5. "Expecting a name" or "Malformed pubk":
   - An asymmetric key constructor like ["pubk", key] or ["privk", key] was passed an asymmetric key variable (sort "akey") instead of a principal identifier (sort "name"), or 2-argument ["pubk", tag, name] had its arguments reversed.
   - Fix: In CPSA, if an asymmetric key variable 'k' is declared with sort "akey", use 'k' and ["invk", 'k'] directly without wrapping in "pubk" or "privk". "pubk" and "privk" only accept variables of sort "name" (or ["pubk", "tag", "name"]).
6. "Uniquely originating value ... does not originate in trace" or "Uniquely originating value in input":
   - A variable declared under "unique_originating" is only transmitted inside a ["hash", ...] one-way digest, is never transmitted, or is also listed in "inputs".
   - Fix: Remove the variable from "unique_originating" (or remove it from "inputs" if it is genuinely fresh). In CPSA, atoms cannot originate inside a one-way hash, and uniquely originating values cannot be inputs.
7. Variable Naming & Metadata Integrity:
   - Preserve all descriptive, domain-specific identifiers (e.g. "client_identity", "server_identity", "client_random", "premaster_secret"). Do NOT downgrade them to single-letter or toy abbreviations like 'a', 'b', 'init', 'resp', 'k'.
   - Preserve and update the 'description' and 'rfc_field' metadata fields.
8. NEVER Emit Foreign Operator "aenc" or "senc":
   - CPSA message algebra has NO "aenc" or "senc" operator!
   - In CPSA, ALL encryption (both symmetric and asymmetric) strictly uses "enc": ["enc", payload, key].
   - If encrypting with a public key, use ["enc", payload, ["pubk", name]] or ["enc", payload, key]. NEVER write "aenc".
9. "timed out after 60 seconds" or "Step limit exceeded" (CPSA4 State-Space Explosion / Snowballing):
   - Cause: CPSA's unification engine is stuck in an infinite strand-generation loop because a Responder/Server `send` term has the exact same algebraic structure/arity as a `recv` term (allowing a Responder's output to feed another Responder's input ad infinitum), or `(ltk A B)` unifies with `(ltk B A)` when `A = B`, or ciphertexts/hashes are overly nested.
   - Fix:
     * Make Request and Response `(enc ...)` terms structurally distinct (different number of concatenated fields inside `enc` or distinct directional key/tag structure) so a Response ciphertext CANNOT unify with a Request `recv` pattern.
     * Simplify redundant nested `(hash (cat ...))` wrappers inside `(enc ...)`—keep only the core nonces, identities, and payload inside `(enc ...)`.
     * Keep each role trace to at most 2–4 essential handshake events.
10. "Missing channel" or Channel Omission:
   - Every trace event in `CPSAProtocolRole.trace` MUST include `"channel": "<chan_var>"` where `<chan_var>` is declared with `"sort": "chan"` in `variables` and listed in `inputs`. NEVER drop the channel variable when repairing a trace.

Return ONLY the repaired, valid CPSAProtocolSpecification matching the requested JSON schema.
