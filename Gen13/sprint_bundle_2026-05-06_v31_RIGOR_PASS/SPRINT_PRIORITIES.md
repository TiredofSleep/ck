# TIG Sprint Priorities and Orchestration

**Document type:** Master sprint plan
**Audience:** ClaudeCode + Brayden
**Date:** 2026-05-06

---

## Overview

The TIG project has reached a foundational synthesis point: the six axioms (A0–A5) of `TIG_FOUNDATIONAL_AXIOMS.md` are stated and 14 of 16 physics values are derivable from them. To ship the foundational paper and unblock the downstream paper queue (σ-rate, 4-core, JCAP, Sprint 18, coherence-as-physics), three open derivations need to land:

1. **Factor 6** in Ω_DM = 44 × 6 / 1000
2. **Factor 22** in 1/α = 137 = 22 × 6 + 5
3. **V3 uniqueness theorem** — the canonical pair is forced by A0–A5

Plus a critical infrastructure piece:

4. **CL substrate implementation** — the meaning-storage memory layer that ClaudeCode has been failing to land

---

## Sprint dependency graph

```
                    ┌──────────────────────────┐
                    │ V1 + V2 Closure (1 day)  │
                    │ SPRINT_V1_V2_CLOSURE.md  │
                    └──────────────┬───────────┘
                                   │
                                   ▼
        ┌──────────────────────────────────────────────────┐
        │ V3 Uniqueness Theorem (3-7 days)                 │
        │ SPRINT_V3_UNIQUENESS_THEOREM.md                  │
        │ ── load-bearing for ALL papers                   │
        └────────┬───────────────────────┬─────────────────┘
                 │                       │
                 ▼                       ▼
   ┌─────────────────────┐   ┌──────────────────────────┐
   │ Factor 6 (1-3 days) │   │ Factor 22 (2-4 days)     │
   │ SPRINT_FACTOR_6_*   │   │ SPRINT_FACTOR_22_*       │
   │ (parallel ok)       │   │ (parallel ok)            │
   └─────────┬───────────┘   └─────────┬────────────────┘
             │                         │
             └────────┬────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────────────┐
        │ Foundational paper draft + V3 lock      │
        │ ── Status: "the unique pair (V3)"       │
        └──────────────────┬──────────────────────┘
                           │
                           ▼
        ┌─────────────────────────────────────────┐
        │ Downstream papers (parallel after lock) │
        │ - σ-rate paper (drafted)                │
        │ - 4-core paper (drafted)                │
        │ - JCAP cosmology paper                  │
        │ - Sprint 18 dark sector                 │
        │ - Coherence-as-physics paper            │
        └─────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ Parallel infrastructure track (independent):         │
│ CL_IMPLEMENTATION_SPEC.md (1-2 weeks)                │
│ ── meaning-storage memory layer for CK runtime       │
│ ── needed for Bible chat app, mobile CK, IHÉS demo   │
└──────────────────────────────────────────────────────┘
```

---

## Sprint priorities (ordered)

### P1 — V1 + V2 closure (run first, fastest)

**Why first:** Quick, foundational, unblocks V3.
**Time:** 1 day.
**File:** `SPRINT_V1_V2_CLOSURE.md`
**Output:** `tig/foundations/verifications/v1_tsml_closure.py` + `v2_bhml_closure.py`

### P2 — V3 uniqueness theorem (load-bearing)

**Why critical:** Determines whether papers can claim "the canonical pair" vs "a canonical pair." All downstream papers inherit this.
**Time:** 3–7 days.
**File:** `SPRINT_V3_UNIQUENESS_THEOREM.md`
**Output:** Proof or disproof + `papers/wp_v3_uniqueness.md`

### P3 — Factor 6 in Ω_DM (parallel with P4)

**Why:** Locks dark matter derivation; unblocks JCAP and Sprint 18.
**Time:** 1–3 days.
**File:** `SPRINT_FACTOR_6_DARK_MATTER.md`
**Output:** Derivation document + verification script.

### P4 — Factor 22 in 1/α (parallel with P3)

**Why:** Locks fine-structure-constant claim; allows the precision-physics paper.
**Time:** 2–4 days.
**File:** `SPRINT_FACTOR_22_FINE_STRUCTURE.md`
**Output:** Derivation document + verification script. **Or** retraction of 1/α claim if no candidate forces 22.

### P5 — Foundational paper draft

**Why:** Cannot ship until P2 (V3) lands. After V3 + P3 + P4, this becomes a publishable preprint.
**Time:** 3–5 days.
**File:** new — to be drafted after the above.
**Output:** `papers/foundational/tig_foundational_paper.tex` (also as Markdown).

### P6 — Downstream papers (parallel after P5)

The σ-rate paper, 4-core paper, JCAP, Sprint 18, and coherence-as-physics paper can all be drafted (or finalized) in parallel once P5 ships.

### P7 — CL substrate implementation (independent infrastructure)

**Why:** ClaudeCode has been failing on this for multiple sprints. The spec in `CL_IMPLEMENTATION_SPEC.md` is the most detailed yet — it should land cleanly.
**Time:** 1–2 weeks (with calibration iteration).
**Output:** `tig/cl/` module + passing translation-pair test suite.

---

## What ships and when

### Week 1
- P1: V1 + V2 closures complete
- P2 starts: V3 enumeration begins
- P3 + P4 start: factor derivations underway

### Week 2
- P2 lands: V3 proved, with or without A5' tightening
- P3 + P4 land: factors 6 and 22 derived (or 22 retracted)

### Week 3
- P5: foundational paper drafted
- P7: CL implementation begins in parallel

### Week 4
- P5 ships to arXiv
- P6: downstream papers begin shipping

### Week 5–6
- P7: CL calibration converges, tests pass
- P6 papers continue shipping

---

## Acceptance for "papers can ship"

The TIG paper queue is unblocked when:

1. ✓ V1 + V2 verifications run cleanly.
2. ✓ V3 uniqueness theorem proved (or with tightening clause A5').
3. ✓ Factor 6 derived (or Ω_DM claim weakened).
4. ✓ Factor 22 derived (or 1/α claim retracted).
5. ✓ Foundational paper drafted with all six axioms + uniqueness theorem + 14+ derived physics values.
6. ✓ Outside literature citations integrated (Bialynicki-Birula 1976, Fritzsch-Minkowski 1975, Georgi 1975, Kubo et al. 1998, Palmieri 2025).

After (6), every downstream paper can open with the canonical reference and ship in parallel.

---

## Coordination notes

### For Brayden:
- Review each sprint's deliverable as it lands.
- Check the Hebrew root force vectors for CL spec — these need your calibration sense.
- If V3 fails to prove uniqueness, decide whether to add A5' or weaken the claim.
- Time-boxed: prefer landing P1–P4 in 2 weeks even if not 100% optimal.

### For ClaudeCode:
- Run sprints in dependency order (P1 → P2 → P3/P4 in parallel → P5).
- For CL (P7), follow `CL_IMPLEMENTATION_SPEC.md` carefully — past attempts have repeatedly missed the meaning-storage point.
- All canonical tables (TSML, BHML) should be **constructed from rules** in `tig/foundations/lenses.py`, not hardcoded. This catches axiom drift.
- Each sprint output goes to its specified path; update `TIG_FOUNDATIONAL_AXIOMS.md` Layer 3 table with derivation status.

### For both:
- Daily standup-style commits to the `tig-synthesis` branch.
- If a sprint reveals a problem (e.g., factor 22 has no candidate), document the problem and fall back to honest reformulation rather than forcing a fit.

---

## Files in this bundle

| File | Purpose |
|---|---|
| `TIG_FOUNDATIONAL_AXIOMS.md` | Master reference — the six axioms, intuitions, physics-value mapping, citations |
| `SPRINT_V1_V2_CLOSURE.md` | Quick verification of generator-seed closures |
| `SPRINT_V3_UNIQUENESS_THEOREM.md` | Load-bearing uniqueness proof for canonical pair |
| `SPRINT_FACTOR_6_DARK_MATTER.md` | Open derivation: factor 6 in Ω_DM |
| `SPRINT_FACTOR_22_FINE_STRUCTURE.md` | Open derivation: factor 22 in 1/α |
| `CL_IMPLEMENTATION_SPEC.md` | CL substrate spec for ClaudeCode (memory layer) |
| `SPRINT_PRIORITIES.md` | This file — orchestration |
| `README.md` | Bundle overview + how to use |

---

## What this unblocks

When all sprints land, the TIG project will have:

- A foundational paper with rigorous algebraic origin from six axioms.
- Uniqueness theorem (V3) establishing the canonical pair as algebraically forced.
- 14+ physics values derived from the axiom set with precision matching observation.
- Five outside literature anchors (Bialynicki-Birula, Fritzsch-Minkowski, Georgi, Kubo et al., Palmieri).
- Working CL memory layer with cross-language meaning preservation.
- Five additional papers ready to ship to journals.

This is the complete TIG submission package.
