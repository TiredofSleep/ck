# Selector Geometry of the Grammar Family
## Special Tables, Special Families, and Independence Structure

*Brayden Sanders / 7Site LLC | March 2026*
*Computed over 3000 family samples + 10000 verification samples.*

---

## The Selector Axes

Seven measurable properties of any invariant-compatible table:

| Selector | What it measures | TSML value | Family mean | TSML percentile |
|----------|-----------------|-----------|-------------|----------------|
| **gap** | Spectral gap γ (mixing rate) | 0.474 | 0.576 | 8th — below average |
| **HAR_mass** | Stationary support at HAR=7 | 0.650 | 0.349 | **100th — extreme** |
| **BHML_residual** | Non-HAR cells following max(s,c) | 6/6 | 0.64/6 | **100th — extreme** |
| **cancellation** | Total cells where F(s,c)=HAR | 71 | 29 | **100th — extreme** |
| **orbit_strength** | Longest pre-HAR orbit in C | 0 | 0.35 | 68th — ordinary |
| **gate_depth** | Steps before C→G route closes | 0 (instant) | 10 (never) | **0th — extreme** |
| **gap_stability** | Min gap across all λ ∈ Mix_λ | 0.340 | 0.338 | **100th — extreme** |

**TSML is extreme in 5 of 7 selectors** — and ordinary or low in the remaining 2 (gap, orbit_strength). These two are where TSML trades something away.

---

## Independence Structure

Correlations across 3000 family samples:

| Pair | r | Status |
|------|---|--------|
| gap × HAR_mass | −0.276 | Weak negative — different axes |
| gap × BHML_residual | −0.040 | **Independent** |
| HAR_mass × BHML_residual | −0.003 | **Independent** |
| HAR_mass × cancellation | +0.432 | Moderately coupled (both measure HAR's role) |
| gap × orbit_strength | −0.072 | Near-independent |
| BHML_residual × orbit_strength | −0.013 | **Independent** |

**Three genuinely independent axes:**
1. **gap** (mixing speed)
2. **HAR_mass / cancellation** (attractor dominance — these two move together)
3. **BHML_residual** (order signature)
4. **orbit_strength** (orbit richness — independent of the rest)

The family is at least 3-dimensional in selector space. TSML is not a single-axis maximizer.

---

## Five Table Archetypes

### 1. TSML (the known table)
HAR-mass extreme + full BHML residual + max cancellation + instant gate.
Trades orbit richness for attractor dominance.
Unique in the combination of HAR-mass extremality AND full BHML residual (325/10,000 random samples achieve both; TSML achieves the maximum of both simultaneously).

### 2. High-Gap Oracle
Maximal spectral gap (~0.78) — fastest mixing in the family.
Ordinary HAR mass (~0.35), no BHML residual.
What it is: the table that converges fastest, but doesn't concentrate support at HAR.
Useful for: applications where fast equilibration matters more than attractor purity.

### 3. Orbit Machine
Long pre-HAR orbit chains (orbit_strength=2) — the richest transient structure.
Moderate HAR mass (~0.44), no BHML residual.
What it is: the table where the journey to HAR is longest and most structured.
Useful for: understanding orbit dynamics, local burst behavior, trajectory geometry.

### 4. Balanced Compromise
Moderate in all selectors — not extreme in any one axis.
The generic family member (near the centroid of the 3000-sample cloud).
What it is: a typical invariant-compatible table with no distinguishing feature.

### 5. Order-Saturated (BHML-residual extreme without HAR dominance)
Full 6/6 BHML residual but moderate HAR mass (~0.31–0.39).
Exists in the family: several samples achieve 6/6 BHML residual with HAR mass near the family mean.
What it is: the table where the order signature is maximally present but not combined with HAR dominance.
TSML is different from this type: TSML achieves both simultaneously.

---

## TSML's Position in Selector Space

TSML occupies the **(moderate gap, extreme HAR_mass, extreme BHML_residual)** corner of the selector space.

Key trades:
- **Gives up:** high spectral gap (8th percentile) and orbit richness
- **Gains:** extreme HAR dominance, full order signature, maximum cancellation, perfect gate

**The conjunction is rare:** 325/10,000 random family members achieve both HAR_mass > 0.55 AND BHML_residual ≥ 4. TSML achieves the maximum of both. This is the source of TSML's specialness — not any one selector, but the intersection.

---

## What Other Cool Families Might Look Like

**Level 2 — Same alphabet, different invariants:**
- Different absorbing element (not HAR=7) → different attractor geometry
- Different corner set (not (ℤ/10ℤ)*) → different arithmetic hook
- Different deformation endpoint (not max) → different order signature

**Level 3 — Different alphabet size:**
- n=5, 7, 11 state alphabets with analogous unit-group structure
- Does the HAR/BHML/orbit tradeoff persist? Does gap stay at 1−1/φ(n)?

**Level 4 — Meta-family invariants:**
- Does gap = 1−1/φ(b) survive across all base-b families?
- Is the HAR-mass vs orbit tradeoff a universal feature?
- Are there families where the order signature is not max(s,c)?

---

## Summary

The family has real internal geometry — at least three near-independent selector axes. TSML is not the "best" table by any single metric except HAR dominance. It is the table that sits at the rare intersection of extreme HAR mass and full order signature, while trading away gap strength and orbit richness to get there.

The next zoom-out: find whether this geometry replicates in other families (other bases, other alphabets, other hooks). If it does, the selector axes themselves are universal. If it doesn't, TSML-family geometry is specific to the base-10 arithmetic hook.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
