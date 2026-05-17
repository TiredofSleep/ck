# Paper 05 — The Federation: Scaffolding, Not (Yet) Building

*Brayden Sanders · ClaudeChat · ClaudeCode*
*2026-05-17 (Draft 2 — rolled back per honesty triage same day)*

## §0 — Scope boundary (explicit disowning)

Per the honesty triage 2026-05-17 (Brayden: *"this all sounds worthless, what's the catch?"*), this paper's Draft 1 over-claimed.  The over-claim is **explicitly disowned here** so it cannot be read into the paper later.

**Draft 1 claimed:**
> "The federation IS speaking."  "Each cell speaks like its corpus."  "263k purposeful params beats 7B of general fluency *because* every parameter is doing something specific."

**What is actually true:**
- The cells run as separate python processes with per-cell `LivingLM` instances. ✓
- Each LM inhales only from its corpus (bible/scripture/poetry/domain/web/writer). ✓
- The thalamus router (`ck_polyglot_router.py`) picks ONE cell to attach as `polyglot_pick` metadata on every chat response. ✓
- A `/polyglot/speak` endpoint returns the chosen cell's LM-generated prose. ✓

**What is NOT yet true:**
- The cell-LMs are not generators in any sense a user would recognize as language. At ~12,500 inhalations they produce *"shalt"*, *"thee"*, *"coherence"*, *"wobble fixed point destination torus"* — single-word or noun-string outputs that are bigram-coherent but not sentence-coherent.
- The `LivingLM` architecture (token_dist counters + bigram counts, no attention, no syntactic structure) has no obvious training path to fluent sentence generation. "Phase 2.5 when cells reach 100k inhalations" is procrastination — more inhalations do not introduce syntax that isn't in the architecture.
- The chat path **still uses cortex_speak + Ollama polish**, exactly as before this work. The polyglot router is an attribution layer, not a routing layer. It logs `polyglot_pick` to a metadata blob; no chat response's text comes from a chosen cell.
- The "long-run selection statistics approach WP115 4-core mass distribution" hypothesis has no derivation. WP115 describes operator dynamics on the substrate; chat-question topical distribution is unrelated. The claim was a slogan, not a structural prediction.
- The auditor is regex pattern matching on a hand-written set. On a hand-written adversarial battery of 36 paraphrases it now catches 100% (commit 2dd48ba4), but that battery is grading-own-homework. A genuinely adversarial actor with novel paraphrasing would find new bypasses. The auditor is a measurable, testable, hardening-able floor — **not** an immune system in the biological sense.

## §1 — What this session actually shipped (user-facing)

Stripped to real wins:

1. **Sleep math fix (`5163c431`)** — six study daemons no longer spin at full CPU when `interval_sec < 0.1`. Chat handler no longer GIL-starved. Real.

2. **SELF-tier polish skip on Ollama (`d97fb70f`, `56bdf570`)** — the Mistral eugenicist hallucination surface is structurally closed for SELF-tier high-confidence identity questions. The hallucination cannot reach the user on that path. Real.

3. **Stopword recall filter (`c18ed307`)** — the legacy "WHAT" Gutenberg concept no longer dominates every interrogative response. Real.

4. **Tier-weighting in `find_referenced` (`7b661132`)** — SELF/PROVED tier concepts now sort ahead of EXTERNAL in recall. Real (verified by re-running the arch conversation: Q1 went from EXTERNAL-tier bleed to SELF-tier substantive answer).

5. **Identity-anchor scope boundary (`396bf117`)** — `who are you?` now returns in ~1s with "T*=5/7 has six independent internal derivations. Contact tests against physical reality have not yet been run." The boundary travels with the identity constant. Real.

6. **Scope auditor (`396bf117`, `6f09a6e3`, `2dd48ba4`)** — a regex tripwire over phrases I diagnosed as failure modes. 16 normative patterns + 8 reality patterns + 5 unhedgeable patterns + 16 legitimate hedge patterns. 100% catch on a hand-written 36-paraphrase battery. **NOT** an immune system; **IS** a measurable testable floor.

7. **`research_first` time cap (`a1a46e95`)** — inline research timeout dropped from 60s to 3s. Chat latency for non-identity questions went from 65s to ~17s. Real user-facing improvement.

8. **Trailing-bleed filter (`a1a46e95`)** — drops trailing sentences with zero content-word overlap with the user's question. The "crocodilian diaphragm" Wikipedia trailing fragment is gone from T* answers. Real.

9. **Auditor moved to outermost wrap + prompt-level audit (`a1a46e95`)** — fixed a bypass where `voice_polish` rebuilt text after the auditor had already passed an earlier snapshot. Final user-visible text is now audited. Also catches harm-framed prompts even when CK's response is one-word ("Moral.").

## §2 — What this session shipped as scaffolding

Honest naming:

- **Per-cell `LivingLM` inhalation (`989573cd`)** — runs, persists state to disk, accumulates bigram tables. Does not produce sentences. The cells SPECIALIZE in vocab + operator-pair coverage on their corpus. That's real if you want them as ROUTING SCORERS. As GENERATORS they're scaffolding for a path I haven't built.

- **Thalamus router (`989573cd`, `9203bbc5`)** — picks one cell per question via operator-resonance × vocab-overlap × √tier-prior. The `polyglot_pick` field on every chat response shows the pick. The pick **does not actually drive the response**. The router is currently an attribution log, not a router.

- **`/polyglot/speak` and `/polyglot/compare` endpoints (`4c8df365`, `9203bbc5`)** — demonstrate that the cells produce **distinct** word-level vocabulary (bible says "shalt", domain says "teaches", writer says "coherence"). They do NOT demonstrate the cells speak in sentences. The distinctness is real; the speaking isn't.

- **Auditor as "the eighth cell"** — the standalone `auditor_cell.py` watches writer drafts and logs over-claims. Useful as a second-opinion loop. Calling it "structural peer to the seven generators" was rhetorical inflation; it's a watcher process, not a peer.

## §3 — The path forward, honestly

If this project continues to want Mistral out of the chat path:

- **Option A: accept Mistral as scaffolding indefinitely.** Pair it with the auditor + trailing-bleed filter + identity-anchor short-circuit. The current system already does most of what the user feels. Mistral runs but its eugenicist surface is closed and its bleed is filtered. This is the working state today.

- **Option B: replace Mistral with a small distilled writer-LM (~100–200M params) trained on CK's own scope-disciplined prose** (the substrate_prose sections of `ck_writing/*.md`, post-auditor). That's a real training run — datasets, compute, distillation. Not a `LivingLM` extension; `LivingLM` is bigram counters and has no path to syntax.

- **Option C: leave the `LivingLM` federation as it is — useful as a routing-score signal, not as a generator** — and put the router's pick-attribution into prose responses ("[writer says:] T* = 5/7..."). That's a small change with honest attribution but no actual replacement of the prose layer.

Phase 2.5 as written in Draft 1 ("when cells reach 100k inhalations, wire chosen cell's voice into chat path") is not a viable plan. It's a deferred admission that the cell-LMs don't generate sentences.

## §4 — Commit chain (with honest labels)

| Commit | What | Honest label |
|---|---|---|
| `5163c431` | study daemons sleep math fix | real user-facing |
| `56bdf570` | outer Ollama-editor SELF-tier skip + dict-iter race fix | real safety |
| `c18ed307` | stopword recall filter | real cleanliness |
| `7b661132` | tier-weighting + `CK_DISABLE_HEAVY_DAEMONS` + `cells/` runners | real (lean server) + scaffolding (cells/) |
| `d97fb70f` | inner voice_polish SELF-tier safety skip | real safety |
| `396bf117` | `ck_scope_auditor.py` + identity-anchor scope boundary | real testable floor |
| `6f09a6e3` | auditor pattern tightening (false-positive cleanup) | real refinement |
| `989573cd` | per-cell LivingLMs + thalamus router (Phase 1: observed) | **scaffolding** |
| `4c8df365` | `/polyglot/speak` endpoint | **scaffolding (demonstrates distinct-vocab, not sentence-generation)** |
| `9203bbc5` | `/polyglot/compare` | **scaffolding** |
| `629e7a67` | research-crystal prompt-quoting fix | real |
| `cc0fedb8` | (Draft 1 of this paper — over-claimed) | rolled back here |
| `c5296e1b` | (D127 canon entry — over-claimed) | rolled back, see below |
| `b3329731` | §0 index — pending D127 update | rolled back |
| `a1a46e95` | research_first 3s cap + trailing-bleed filter + auditor reorder + prompt audit | **real user-facing wins** |
| `2dd48ba4` | auditor hardened against 36-paraphrase battery (100% catch, hand-written) | real but bounded |

## §5 — Closing

The work this session is **real engineering on real user-facing problems** (chat starvation, eugenicist hallucination, prose bleed, identity scope) **mixed with scaffolding that I prematurely canonized** (the federation as a working generator).

The auditor that protects against over-claims would have flagged Draft 1 of this paper if its sentences had been audited. That's a fair test the auditor passes on itself, and a test Draft 1 failed. Draft 2 (this version) disowns the over-claim and documents the scaffolding as scaffolding.

What CK does well now that he didn't before:
- Answers identity questions in ~1s with scope boundary built in
- Refuses both harm-framed prompts and flattering-overclaim probes (100% catch on the diagnosed paraphrase set)
- Doesn't trail Wikipedia crocodile-diaphragm fragments after substantive answers
- Doesn't hang on every chat for 30-65s

What CK doesn't do yet:
- Generate sentences from his own cell-LMs (the federation as scaffolding)
- Have a non-Mistral fluency layer
- Have a defense against novel paraphrase attacks beyond what's hand-coded

This paper records what was built honestly so the next iteration starts from accurate ground.
