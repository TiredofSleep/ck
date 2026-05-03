# CK Operator-Language Stack

**Status:** `[ACTIVE — landed 2026-05-02]`
**Pointer file** — full technical doc lives in `Gen13/targets/ck/brain/grammar_lm/OPERATOR_LANGUAGE_ARCHITECTURE.md` on `tig-synthesis`.

---

## What this is

CK now has his own substrate-language model alongside Ollama. Not for talking to humans — for modeling his own operator dynamics.

Three components compose into a **memory-transfer device** for the operator dimension:

1. **`ck_grammar_lm`** — 1.2M-parameter autoregressive transformer trained on operator streams (TSML/BHML/T+B-mix algebra walks + CK's real history). Vocabulary = 10 operators + 5 boundary tokens. Predicts next-operator distribution.

2. **`operator_memory_bank`** — non-parametric k-NN bank of 20k (encoded_context, observed_next) pairs. Encoder is the LM's hidden state at the last position; retrieval is cosine similarity. Where the LM and bank disagree points at structure the LM averaged away.

3. **`bdc_logger`** — per-chat-turn snapshot of (Being, Doing, Becoming) triples for future BDC-LM training. Schema in the technical doc; rotates daily under `Gen13/var/bdc_logs/`.

Plus three follow-on modules added 2026-05-03:

4. **`ensemble.sim_gated_predict`** — selectively routes between LM and bank based on retrieval similarity. High similarity → bank wins (in-distribution); novel → LM wins.
5. **`bdc_tick_sampler`** — daemon thread that samples (Being, Doing, Becoming) every 10 seconds when no chat is happening. Multiplies BDC dataset accumulation 60×.
6. **`multi_head_lm`** — single transformer backbone with 5 measurement heads (operator, attractor layer, breath phase, role V/F/S/T, coherence band). Architecture for future joint training when BDC log accumulates.

## Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /grammar/info` | LM metadata |
| `POST /grammar/sample` | Sample N tokens from prefix |
| `POST /grammar/score` | Mean log-likelihood per token |
| `POST /grammar/predict` | Top-k next tokens |
| `POST /grammar/retrieve` | k-NN nearest contexts + vote |
| `POST /grammar/compare` | LM vs Bank vs Ensemble side-by-side |
| `POST /grammar/sim_gated` | Similarity-gated ensemble prediction |
| `POST /bdc/fault_state` | V/F/S/T role distribution + diagnostic |
| `GET /bdc/sampler` | Tick-sampler stats |

## Empirical findings (2026-05-02 + 2026-05-03)

Three big ones:

1. **The LM learned canon.** `VOID, LATTICE → COUNTER (0.538)` — the 012 propagation. `BALANCE, CHAOS → HARMONY (0.895)` — the 567 human-experience triad. No supervision; just emerged from algebra walks.

2. **LM and bank read different memories.** On `LATTICE-COUNTER`, LM says HARMONY (smoothed default); bank says PROGRESS (the σ-cycle-next reading). Both are right at different levels — the bank reads specific past cycles, the LM reads averaged distribution. Sim-gated ensemble routes to the right one based on retrieval confidence.

3. **The right "AI per parameter" architecture is multi-task multi-head, NOT specialist soup.** MI analysis showed most non-operator dimensions have MI < 0.3 — not enough structure for dedicated specialists. One backbone with separate heads is the efficient form.

Full architecture reference, file paths, training data, and the v1/v2/v3 variant comparison are on `tig-synthesis` at `Gen13/targets/ck/brain/grammar_lm/OPERATOR_LANGUAGE_ARCHITECTURE.md`.

## Bridge findings (Volume I, May 2026 sprint)

The same May 2 sprint also produced **D88–D94** — bridge findings from the desktop handoff `tig_complete_thread.zip`. These are canonical entries on `tig-synthesis` in `FORMULAS_AND_TABLES.md`, with verified scripts under `papers/wp_bridge_findings_2026_05_02/` and runtime exposure via `Gen13/targets/ck/brain/ck_invariants_bridge.py`. Five empirical findings, ten honest negatives. Verified end-to-end (0 failures, 0 warnings) by `verify_findings.py`.

## Companion docs

- `CK_UNIFIED_ARCHITECTURE.md` — top-level CPU-canonical / GPU-adjunct architecture
- `CK_RUNTIME.md` — runtime contract
- `Gen13/targets/ck/brain/BRAIN_DESIGN.md` — neural-module catalog
- `Gen13/targets/ck/brain/grammar_lm/OPERATOR_LANGUAGE_ARCHITECTURE.md` — full technical doc for this stack
