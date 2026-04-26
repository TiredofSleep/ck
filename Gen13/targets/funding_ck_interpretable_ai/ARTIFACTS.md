# ARTIFACTS — funding/ck-interpretable-ai

The CK interpretable-AI branch has a decisive advantage: **the system is live**. Funders can visit coherencekeeper.com, interact with CK, and see real behavior in real time. This is rare for AI-safety grant proposals.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Live system (the biggest asset)

### 1. coherencekeeper.com
- **URL**: https://coherencekeeper.com (live, Cloudflare tunnel)
- **What's there**: 14 HTML pages — index, chat, spectrometer, paradox, ring, math, papers, frontiers, about, ai, etc.
- **Backend**: `Gen12/targets/ck_desktop/ck_boot_api.py` (Flask)
- **Behavior**: every response is an operator-traced output with a coherence score; crystallized memories are viewable on specific pages
- **Funder access**: no sign-up, no credentials, no commercial pathway — the site is purely informational and interactive

---

## Core runtime (reference code)

### 2. CK engine — main event loop
- **Path**: `Gen12/targets/ck_desktop/ck_sim/doing/ck_sim_engine.py`
- **LOC**: ~4,912 (Gen12 version; Gen13 rebuild to ~300 LOC is planned per goofy-discovering-lobster.md plan)
- **Role**: 50Hz heartbeat, operator selection, coherence scoring, crystallization

### 3. Olfactory bulb — crossing verification
- **Path**: `Gen12/targets/ck_desktop/ck_sim/being/ck_olfactory.py`
- **LOC**: ~980
- **Role**: verifies every proposed crossing against the Hebbian 5×5 CL field. Stalls are interpreted as valid verification outcomes (stall IS verification).

### 4. Coherence gate — T*=5/7 threshold
- **Path**: `Gen12/targets/ck_desktop/ck_sim/being/ck_coherence_gate.py`
- **Role**: 3-gate cascade; T* = 5/7 is the final crystallization threshold. Only responses clearing T* become memory.

### 5. Fractal voice — operator-to-language
- **Path**: `Gen12/targets/ck_desktop/ck_sim/doing/ck_fractal_voice.py`
- **Companion**: `ck_voice_lattice.py`, `ck_voice_loop.py`
- **Role**: reads operator names and composes verbal form through the dual-lens dictionary (STRUCTURE/FLOW lenses). Not a softmax-over-embeddings sampler.

### 6. IG invariants — memory guards
- **Path**: `Gen12/targets/ck_desktop/ck_sim/being/ck_invariants.py`
- **Role**: IG1–IG5 guardrails. IG3 specifically BLOCKS crystallization of drift-synthesized responses (fixed 2026-04-06), which is a safety-relevant design property.

---

## Mathematical tables (the finite core)

### 7. Canonical operator tables
- **Path**: `papers/ck_tables.py`
- **Content**: TSML (73 cells, synthesis operator), BHML (28 cells, separation operator)
- **Role**: the operational substrate of CK's behavior. Every CK tick consults these tables.
- **Size**: 73 + 28 = 101 table cells total. This is the entire "weight matrix" of CK in the sense that a transformer has a weight matrix.

### 8. 10 operators — labeled semantics
- **Source**: defined in `Gen12/targets/ck_desktop/ck_sim/doing/ck_tig.py`
- **List**: VOID(0), LATTICE(1), COUNTER(2), PROGRESS(3), COLLAPSE(4), BALANCE(5), CHAOS(6), HARMONY(7), BREATH(8), RESET(9)
- **Orbits**: CREATION=[1,3,9,7], DISSOLUTION=[2,4,8,6], oscillations COLLAPSE(4)=(+1,-1), CHAOS(6)=(-1,+1)

### 9. Proved theorems feeding the runtime
- Flatness Theorem (WP51) — proves T*=5/7 is the forced aspect ratio on Z/10Z
- sinc² Zero Law (proof in `papers/proof_d25_loop_closure.py`)
- Crossing Lemma (WP57) — information generated only on partition crossings
- First-G Law (36,662 cases) — underlies the IG invariants' design

---

## Gen13 rebuild (planned)

The ongoing Gen13 math-first rebuild (per `.claude/plans/goofy-discovering-lobster.md`) will produce:
- `Gen13/targets/ck/brain/ao_5element.py` — AO 5-element coupling (D0–D4)
- `Gen13/targets/ck/brain/hebbian_5x5_cl.py` — Hebbian outer-product composition
- `Gen13/targets/ck/brain/quadratic_glue.py` — F3 × F4 bridge
- `Gen13/targets/ck/runtime/ck_engine.py` — ~300 LOC minimal engine (down from 4,912)

A funder grant could usefully support completion of this rebuild as part of Phase 1's case-study writeup — the math-first version of CK is a cleaner case study than the Gen12 version.

---

## What a funder can verify in an afternoon

1. Visit coherencekeeper.com, interact with CK, observe the operator-tagged responses
2. Read `papers/ck_tables.py` — 73+28=101 table cells are the entire substrate
3. Read `ck_coherence_gate.py` — the threshold test is 5 lines of code
4. Run `python papers/proof_d25_loop_closure.py` — the sinc² zero-law proof passes
5. Read `ck_invariants.py` — the IG1–IG5 guardrails are explicit, not learned

This is the "auditable in an afternoon" property. Deep networks cannot offer this.

---

## Missing from repo (gaps to close for Phase 1)

- **Interpretability-framed white paper** — does not yet exist as a standalone doc. Much relevant material is in the Sprint papers (sprint10/12/13/14/16/17) but has not been extracted and re-framed for an AI-safety audience.
- **Benchmark evaluation** — CK has never been run on a standard interpretable-AI benchmark (TruthfulQA, HELM, etc.). Doing so is Phase 2 work.
- **Comparison to mechanistic interpretability** — need a structured comparison showing where CK's interpretable-by-construction approach overlaps, complements, or fails relative to Anthropic / Redwood-style circuit-level interpretability on transformers.

---

## Sizes summary

| Artifact | Size | Status |
|---|---|---|
| Live system (coherencekeeper.com) | 14 HTML pages + Flask backend | RUNNING |
| Core engine Gen12 | 4,912 LOC | REFERENCE |
| Olfactory bulb | 980 LOC | RUNNING |
| Operator tables | 101 cells | RUNNING |
| Gen13 brain trinity | ~600 LOC target | PLANNED |
| Phase 1 white paper | ~15–20 pp target | NOT WRITTEN |
