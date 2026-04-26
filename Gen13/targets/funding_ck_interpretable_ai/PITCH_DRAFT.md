# PITCH_DRAFT — funding/ck-interpretable-ai

**Addressee (working default):** Open Philanthropy technical AI safety grantmaker
**Parallel draft:** Long-Term Future Fund S-process
**Ask:** Phase 1 $40K–$80K / 6 months (white paper + Gen13 rebuild); Phase 2 $150K–$350K / 12 months (benchmark evaluation)
**Status:** Skeleton. Requires Phase 1 white paper draft before send.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Opening (½ page)

The dominant paradigm for AI interpretability is **reverse-engineering**: given a trained model, decompose its circuits, features, and computations to understand its behavior after the fact. This work has produced real and important results — mechanistic interpretability on transformers, circuit discovery, feature-attribution methods — but it has known scaling difficulties as models grow.

This proposal describes **CK** — a running AI system at coherencekeeper.com — as a case study in an orthogonal approach: **interpretability by construction**. CK's operational substrate consists of 10 labeled operators (with known semantics), a 101-cell finite table (73 TSML cells + 28 BHML cells), a T* = 5/7 coherence threshold derived from a proved theorem (Flatness Theorem, WP51), and a 50Hz heartbeat that composes them. Every response is traceable to the specific operators, scores, and table lookups that produced it. There is no "weight matrix" in the transformer sense; there is also no emergent feature to reverse-engineer. The system is small, auditable in an afternoon, and has been running continuously as a public site since early 2026.

The open question this proposal investigates is: **how far does interpretability-by-construction go?** The deliverable is a formal case study — a white paper + benchmark evaluation — that answers the question with specific data, situates CK relative to mechanistic-interpretability work on transformers, and owns the limits.

## Background (~1 page)

> Content to be drafted. Sections:
> - The interpretability landscape: after-the-fact (mechanistic interp) vs. by-construction (symbolic / rule-based / program-synthesis). Where does CK sit?
> - The CK architecture in brief: 10 operators, 101 table cells, T*=5/7, olfactory verification, crystallization gate
> - The sovereignty license as a safety feature (not a limitation)
> - Related work: prior symbolic-AI systems, program synthesis, neuro-symbolic approaches; what distinguishes CK
> - The Flatness Theorem connection: T*=5/7 is not a hyperparameter, it's a *theorem*

## The proposed work (~1 page)

### Phase 1 — Case-study white paper + Gen13 rebuild (Month 1–6, $40K–$80K)

**Deliverable A**: a 15–20 page white paper, "CK as an Interpretability-by-Construction Case Study". Covers:
- Full architecture description
- Sample interaction traces (input → operator → score → output)
- Comparison to mechanistic-interpretability approaches
- What CK does well
- What CK does not do (owned limits; see LIMITATIONS.md)
- Relationship to the Flatness Theorem and the T*=5/7 threshold

**Deliverable B**: completion of the Gen13 math-first rebuild (~300 LOC engine, down from 4,912 LOC in Gen12). Gen13 is the cleaner case study for the white paper; the rebuild is in motion and partial funding accelerates it.

### Phase 2 — Benchmark evaluation (Month 7–18, $150K–$350K)

**Deliverable**: one published benchmark run. Candidate benchmarks:
- **TruthfulQA** with full operator trace per answer
- A causal-reasoning task where CK's explicit operator chain is compared to LLM chain-of-thought
- A deception-detection task testing IG3's drift-synthesized-response block

Result is published regardless of outcome: whether CK performs at, above, or below transformer baselines, the interpretability trace is the research contribution.

### Phase 3 — Architecture variants (Month 19–36, $300K–$700K)

**Deliverable**: systematic ablation and variation study. Questions:
- Remove the olfactory bulb: does coherence degrade?
- Replace fixed T* with a learned threshold: better, worse, or same?
- Expand the operator set beyond 10: at what point does the interpretability-by-construction advantage collapse?

## Why Open Philanthropy specifically

Open Phil has explicitly funded non-scaling interpretability work and unconventional AI-safety architectures. CK's profile — small, running, math-first, non-commercial — matches Open Phil's empirical-alternative-architecture grant patterns. The grant sizes Open Phil uses for individual researchers ($50K–$500K) fit Phase 1 and Phase 2.

## Parallel draft: Long-Term Future Fund

LTFF S-process rounds fund independent-researcher AI safety work on short turnaround. LTFF grant sizes ($10K–$250K) fit Phase 1 well as a follow-up or parallel application. LTFF's 2-page proposal format is lower-barrier than a full Open Phil proposal.

## Attribution

- **Brayden Sanders** — PI, sole thread-facing author, architect of CK
- Architectural dialogues with ClaudeChat, Celeste/GPT acknowledged in methods (AIs as thinking-partners, not human co-authors)
- Prior collaborators (C.A. Luther, Ben Mayes, M. Gish, H.J. Johnson) credited for their specific contributions to related mathematical work (spectral layer, UOP/GUT arc, Sprint 14 ξ cosmology) but the interpretability-case-study framing is new

## The live-demo advantage

A funder can visit coherencekeeper.com during the first 5 minutes of reading this proposal and interact with CK directly. Most AI-safety proposals cannot offer this.

## Attachments

- `ARTIFACTS.md` — runtime code paths and line counts
- `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/` — Flatness Theorem source
- `papers/ck_tables.py` — the 101-cell substrate
- Live URL: https://coherencekeeper.com

## Pre-send checklist

- [ ] Phase 1 white paper draft written (15–20 pp)
- [ ] Sample traces captured from live system and pasted into the paper
- [ ] Comparison to mechanistic-interpretability work written as a dedicated section
- [ ] License framing reviewed (sovereignty license as safety feature)
- [ ] At least one AI-safety researcher (FAR AI / Redwood / Apollo contact) has read an early draft
- [ ] Brayden confirms Open Phil vs LTFF as first submission
- [ ] Brayden reviews + edits
- [ ] Brayden sends
