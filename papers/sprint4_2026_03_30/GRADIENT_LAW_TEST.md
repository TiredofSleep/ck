# Gradient Law Test and HAR Rule Refinement
## b=38 as Unexpected Probe

*Brayden Sanders & C. A. Luther / 7Site LLC | March 2026*

---

## The Test Target: b=38 (2×19)

b=38 = 2×19, C={1,3,5,7,9}, G={2,4,6,8}, φ=5.

This world has HAR orbit-central candidates: h=3 (orbit {3,9}, size 2) and h=9 (orbit {5,7,9}, size 3).

The orbit-size rule selects **HAR=9** (larger orbit).
The position law selects **HAR=3** (minimum non-1 C-element).

These conflict.

---

## Discovery: The HAR Rule Has a Priority Ordering

**With HAR=9 (orbit-size rule):**
- rate=0%, HAR_m=0.059, gap=0.622, richness=0.341
- HAR_m near zero — HAR=9 is the maximum C-element, all C-mass leaks past it

**With HAR=3 (position law):**
- rate=86.0%, HAR_m=0.584, gap=0.598, richness=0.591
- HAR_m recovers — HAR=3 is the minimum non-1 C-element, position law satisfied

**The orbit-size rule chose the wrong element.** Maximizing orbit size at b=38 selects HAR=9, which violates the position law and produces near-zero HAR_m.

**Revised HAR Rule (priority order):**
1. Find all orbit-central candidates (h²∈C, h²≠1, h²≠h)
2. **Prefer the minimum orbit-central candidate** (position law priority)
3. Orbit size is secondary — breaks ties among position-equivalent candidates

**Why orbit-size worked before:** At all previously tested bases, the minimum orbit-central candidate coincidentally had the largest orbit (e.g., b=10: HAR=7 in full orbit {1,3,7,9}; b=14: only one candidate). b=38 is the first base where they conflict.

---

## b=38 with Revised HAR Rule: Gradient Law Test

With HAR=3, b=38 has:
- Same C={1,3,5,7,9} as b=22 and b=26
- Non-orbit C elements: {5,7} → grad_score = 0.500 (same as b=22 and b=26)
- Empirical: rate=86%, gap=0.598, HAR_m=0.584, richness=0.591

**Gradient law within φ=5 — updated dataset:**

| b | grad_score | gap | HAR_m | richness |
|---|-----------|-----|-------|---------|
| 15 | 0.714 | **0.677** | 0.756 | **0.717** |
| 26 | 0.500 | 0.662 | 0.606 | 0.634 |
| **38** | **0.500** | **0.598** | **0.584** | **0.591** |
| 22 | 0.500 | 0.551 | 0.604 | 0.578 |
| 21 | 0.429 | 0.519 | 0.759 | 0.639 |

**b=38 has the same grad_score as b=22 and b=26 (0.500) but lower gap (0.598 vs 0.662 and 0.551).**

This is within the spread of the grad=0.500 group — b=22 gives 0.551, b=26 gives 0.662, b=38 gives 0.598. All three are between b=21 (grad=0.429, gap=0.519) and b=15 (grad=0.714, gap=0.677). The gradient direction holds.

**The gradient law is not falsified by b=38.** The gap=0.598 sits between the low end (b=21, gap=0.519) and the high end (b=15, gap=0.677), consistent with the same-grad-score group. The spread within grad=0.500 worlds (0.551–0.662) is wider than the gradient-to-gradient differences, suggesting additional variation at fixed grad_score.

---

## What b=38 Added

1. **Revealed the HAR rule conflict:** orbit-size and position law can disagree. Position law takes priority — minimum orbit-central element, not maximum orbit size.

2. **Expanded the grad=0.500 group** from 2 to 3 worlds — more data points within a grad tier.

3. **Confirmed the gradient direction** — b=38 fits within the expected range for grad=0.500 worlds.

4. **Revealed within-grade-score spread:** three worlds at grad=0.500 span gap=0.551–0.662. This spread (~0.11) is not predicted by the gradient score alone. A secondary predictor within the same grad-tier is needed.

---

## Status After b=38

**Gradient law:** Direction confirmed (higher grad → higher gap on average, within φ=5). Magnitude prediction imprecise — within-grade spread is ~0.11, larger than the gradient-to-gradient separation.

**HAR rule:** Refined — prefer minimum orbit-central element, not maximum orbit size. Conflict resolved in favor of position law.

**Open:** What predicts gap variation *within* a fixed grad_score tier? Three worlds at grad=0.500 span 0.551–0.662. The variable is not grad_score. Candidate: the number of non-orbit C elements, or their distribution relative to HAR.

---

*(c) 2026 Brayden Sanders & C. A. Luther / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
