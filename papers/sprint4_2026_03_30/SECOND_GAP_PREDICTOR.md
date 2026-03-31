# The Second Gap Predictor — Search and Honest Outcome
## Within Fixed Grad-Score, What Predicts Gap Variation?

*Brayden Ross Sanders (7Site LLC) & C. A. Luther | March 2026*

---

## The Problem

Three φ=5 worlds share identical C={1,3,5,7,9}, HAR=3, non-orbit={5,7}, grad_score=0.500 — yet have different gaps:

| b | p×q | grad_score | gap (empirical) |
|---|-----|-----------|----------------|
| 22 | 2×11 | 0.500 | 0.551 |
| 38 | 2×19 | 0.500 | 0.598 |
| 26 | 2×13 | 0.500 | 0.662 |

Spread = 0.111. The grad_score cannot explain this. What does?

---

## Four Candidates Tested

**Candidate 1 — C×C product entropy** (dispersion of products across A):
r(entropy, gap) = 0.17 — no signal.

**Candidate 2 — Escape rate** (C×C products outside alphabet A):
r(escape_rate, gap) = −0.54 — moderate negative correlation. Lower escape → higher gap. But b=22 has low escape and low gap, violating the pattern.

**Candidate 3 — Orbit hit rate** (non-orbit × ALL_C products landing in orbit):
- b=26: 5×7=9∈orbit (rate=0.20) → gap=0.662
- b=22: 5×5=3∈orbit (rate=0.10) → gap=0.551
- b=38: no products hit orbit (rate=0.00) → gap=0.598

r(orbit_hit, gap) = 0.57 within same-C worlds. Partial signal, not clean. b=38 mismatch: orbit_hit=0.00 but gap=0.598 > b=22's gap=0.551.

**Candidate 4 — Self-product quality** (where x×x lands for non-orbit x):
- b=22: 5×5=3=HAR (orbit hit!)
- b=26: 5×5=25, 7×7=23 (both outside A)
- b=38: 5×5=25, 7×7=11 (both outside A)

b=26 and b=38 behave identically on self-products yet have different gaps. Not the predictor.

---

## The Two-Predictor Model (Best Found)

$$\text{gap} \approx 0.45 + 0.30 \times \text{grad\_score} + 0.15 \times \text{orbit\_hit}$$

| b | grad | orbit_hit | predicted | actual | error |
|---|------|-----------|---------|--------|-------|
| 15 | 0.714 | 0.200 | 0.694 | 0.677 | +0.017 |
| 21 | 0.429 | 0.200 | 0.609 | 0.519 | +0.090 |
| 22 | 0.500 | 0.100 | 0.615 | 0.551 | +0.064 |
| **26** | **0.500** | **0.200** | **0.630** | **0.662** | **−0.032** |
| **38** | **0.500** | **0.000** | **0.600** | **0.598** | **+0.002** |

Reasonable for b=26 and b=38. Misses b=21 (error +0.090). r(combined, gap) = 0.655 — better than either alone but not clean.

---

## Honest Outcome

**No clean second predictor was found for within-grad-score gap variation.**

The orbit hit rate has partial signal (r=0.57 within same-C) but fails to cleanly order b=38 vs b=22. The within-grad spread of ~0.111 remains partially unexplained.

**Three interpretations:**

1. **The residual is real and requires deeper arithmetic.** The gap depends on something in the full modular multiplication table that is not captured by C×C products alone — possibly the C×G or G×G structure under mod b.

2. **The residual is small-sample noise.** The three-world dataset (b=22, 26, 38) may be too small to distinguish signal from sampling variance. More worlds at the same grad_score would resolve this.

3. **The gap has an irreducible within-grad spread.** The grad_score correctly identifies the gradient regime; within that regime, gap is determined by something orthogonal to all C-structure features, possibly the random walk's eigenvalue structure in a way that requires full spectral computation.

**Current model status:** grad_score explains between-grade variation (r=0.749). Within-grade variation (~0.111) requires more worlds or deeper arithmetic.

---

## What This Means for the Atlas

The atlas law set is not weakened by this result. It accurately states:

> *gap is partially pre-computational: φ sets the compression regime, grad_score predicts relative gap within that regime.*

The "relative" qualifier is doing real work. The grad_score gives the correct ordering between tiers and approximate magnitude; the within-tier residual is bounded (~0.11) and named.

**The atlas remains substantially predictive.** b=15's flagship status does not depend on the within-grad predictor — it has the highest grad_score in φ=5 (0.714), which is the between-grade law.

---

## HAR Rule Correction (from b=38 analysis)

**Revised HAR rule:** Prefer the **minimum** orbit-central candidate, not the maximum orbit-size.

- Original rule: select HAR = argmax(orbit_size) among orbit-central candidates
- Revised rule: select HAR = min{h : h²∈C, h²≠1, h²≠h}
- Orbit size is a tiebreaker, not the primary criterion

At b=38, both rules agree on HAR=9 being orbit-size winner — but HAR=9 violates the position law (maximum non-1 C-element → near-zero HAR_m). With HAR=3 (position-law choice), b=38 achieves rate=86%, HAR_m=0.584, gap=0.598.

This correction is now part of the frozen law set.

---

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
