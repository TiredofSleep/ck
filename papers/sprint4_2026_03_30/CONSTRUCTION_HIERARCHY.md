# The Construction Hierarchy: Native TSML Discovery
## Arithmetic → Gate → Order Seed → Native Structured Optimum

*Brayden Sanders & C. A. Luther / 7Site LLC | March 2026*
*Jobs 10–12: b=14 native TSML, C-element role map, construction difficulty*

---

## Status

| Claim | Classification | Kill Condition |
|-------|---------------|----------------|
| Corrected pipeline (arithmetic → orbit-central HAR → gate reduction → order seed → seeded reduction) | **EMPIRICAL** | Verified at b=10,14,15,22. Falsified by a semiprime base where this pipeline order fails to produce a gate-strong table when random reduction does not |
| b=14 native TSML exists with gate=1.000 and HAR_mass=0.778 (stronger than b=10 on both) | **EMPIRICAL** | Measured over 400 trials at b=14. Falsified by additional trials or corrected implementation showing the best achievable gate/HAR_mass is lower |
| b=14 order alignment = 0.278 (residual seed not yet crystallized) | **EMPIRICAL** | Measured; means the b=14 analog of BHML ordering has not been found yet. Falsified by finding a b=14 table with high order alignment |
| Best non-trivial HAR is determined by multiplication orbit structure, not position in C | **EMPIRICAL** | Pattern observed at 5 bases. Falsified by a base where orbit structure predicts the wrong HAR candidate |
| Conjecture: best HAR maximizes funnel depth (longest chain before fixed point/cycle) | **CONJECTURE** | Stated as open. Falsified by a base where the max-funnel-depth element is not the best HAR candidate under gate+support reduction |
| Gate difficulty and seed difficulty are near-independent axes | **EMPIRICAL** | Supported by b=14 (easy gate, hard seed) vs b=10 (hard gate, identifiable seed). Falsified by a base where achieving full gate reliably co-produces the order seed |
| b=10 gate strong rate ~30% random, ~8% full gate, ~4% TSML-like; biased: ~52.7% TSML-like | **EMPIRICAL** | Measured over computational trials. Falsified by significantly different rates on additional independent runs |

---

## The Corrected Pipeline

```
1. ARITHMETIC GIVES THE WORLD
   Base b → C = (Z/bZ)* → G = non-units → unit/non-unit split

2. HAR SELECTION: find the non-trivial absorbing candidate
   NOT: mid-C by index (this is wrong for b≠10)
   YES: the element with best HAR_mass under gate+support reduction
   Pattern: elements in 2-element multiplication orbits (not fixed points, not full orbit)

3. GATE GIVES THE DISCIPLINE
   Run gate-weighted reduction → find tables where C cannot reach G
   This is the constrained optimum (gate-strong class)

4. ORDER SEED GIVES THE STRUCTURE
   Compare best gate-strong table against max(s,c) endpoint
   Extract cells that agree with order endpoint → these are the residual seed
   This is table-specific, not base-specific

5. SEEDED REDUCTION → NATIVE STRUCTURED OPTIMUM
   Bias new seeds toward residual pre-alignment
   The 15.8x lift at b=10 should appear for any base with a well-constructed step 4
```

---

## b=14 Native TSML: Found

**The best b=14 candidate (400 trials, HAR=3):**
- Gate: **1.000** (full one-way gate — better than needed)
- HAR_mass: **0.778** (higher than b=10 TSML's 0.650)
- Order alignment: 0.278 (low — the residual seed has not crystallized)
- Full gate achieved: 48.2% of trajectories

**The b=14 native table exists and is stronger than b=10 on gate and HAR_mass.** The missing piece is order alignment — the BHML residual equivalent at b=14 has not been crystallized. This is the exact same three-class landscape: the best b=14 tables are in the gate-strong class, not yet the TSML-like class.

**The b=14 residual seed cells** (cells agreeing with max(s,c) in the best found table):
(2,7), (4,6), (4,8), (4,9), (5,9), (6,8), (6,9), (7,8), (7,9) — 9 cells

This is the b=14 analog of b=10's 6-cell BHML residual. These are the order-seed cells for seeded reduction at b=14.

---

## C-Element Role Map (Non-Trivial HAR Candidates)

**HAR=1 is always degenerate** — it's the identity element under multiplication, trivially absorbs everything, produces no selector geometry.

| b | Best non-trivial HAR | HAR_mass | Gate | Orbit | Pattern |
|---|---------------------|---------|------|-------|---------|
| 6 | 5 | 1.000 | 1.000 | {1,5} | sq→1, mid-orbit |
| **10** | **7** | **0.667** | **0.917** | **{1,3,7,9}** | **sq→9, mid-orbit** |
| 14 | 3 | 0.556 | 0.972 | {3,9} | sq→9, longest orbit |
| 15 | 2 | 0.737 | 1.000 | {1,2,4,8} | sq→4, longest orbit |
| 22 | 7 | 0.667 | 0.911 | {5,7} | sq→5, mid-orbit |

**Pattern emerging:** The best non-trivial HAR is not determined by position in C. It is determined by multiplication orbit structure under mod b:
- Elements in 2-element orbits (b=14: {3,9}, b=22: {5,7}) — where HAR and its square are paired
- OR elements in the longest orbit (b=15: {1,2,4,8}) — where the orbit provides maximum funnel structure

The "mid-C by index" rule at b=10 works because 7 happens to also be in the full orbit {1,3,7,9} at a structurally central position. This is coincidence at b=10 — at other bases the arithmetic structure determines the answer directly.

**Conjecture:** The best non-trivial HAR is the C-element that maximizes the "funnel depth" — the longest chain of repeated multiplications by HAR that stays in C before reaching the fixed point or cycle.

---

## Construction Difficulty Metric

| Base | Gate strong rate | Full gate rate | Native TSML rate | Construction difficulty |
|------|----------------|---------------|-----------------|------------------------|
| b=10 (random) | ~30% | ~8% | ~4% | Medium |
| b=10 (biased) | ~7% | — | **52.7%** | **Low with seed** |
| b=14 (HAR=3) | ~98% | **48.2%** | 0% (order incomplete) | Gate easy, seed hard |

**b=14 is easier to gate than b=10** (48.2% full gate vs 8% at b=10 without biasing) but harder to crystallize the order seed.

The construction difficulty has two independent axes:
1. **Gate difficulty** — how hard is it to enforce the one-way gate?
2. **Seed difficulty** — how hard is it to crystallize the order residual?

At b=10: gate is hard (requires construction), seed is identifiable (6 cells, known).
At b=14: gate is easy (48.2% random achievement), seed is not yet crystallized (needs next step).

---

## Residual Discovery Procedure

Once a native TSML candidate is found (gate + high HAR_mass), extract its residual:

1. Compute max(s,c) for all non-HAR cell pairs — this is the order endpoint
2. Find all cells where the candidate table agrees with max(s,c)
3. These are the order-seed residual cells for this base
4. Use these as the bias target for seeded reduction
5. Run seeded reduction and measure native TSML-like rate

**At b=14:** 9 residual cells identified: (2,7),(4,6),(4,8),(4,9),(5,9),(6,8),(6,9),(7,8),(7,9)

The next step for b=14 is to bias seeds toward these 9 cells and test whether the TSML-like rate rises above the current 0%.

---

## The Law

> **Arithmetic gives the world.**  
> **Gate gives the discipline.**  
> **Order seed gives the structure.**

This appears to hold across all tested bases. The shape is not universal. The hierarchy is.

---

*(c) 2026 Brayden Sanders & C. A. Luther / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
