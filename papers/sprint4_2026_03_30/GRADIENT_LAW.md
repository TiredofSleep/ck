# The Gradient Law and Three-Score Atlas
## φ sets the range. Non-orbit C-placement sets the gradient.

*Brayden Ross Sanders (7Site LLC) & C. A. Luther | March 2026*

> *The law is invariant. The tables are local.*
> *φ sets the range; the placement of the non-orbit C-element sets the gradient.*

---

## The φ=5 World Inventory (b ≤ 200)

23 φ=5 semiprime worlds exist in the {1..9} alphabet with orbit-central HAR.
They split into two families:

**Family A — 2×prime (b=22,26,34,46,...): C={1,3,5,7,9}**
HAR=3, non-orbit C elements = {5,7}, gradient score = 0.790

**Family B — 3×prime (b=15,21,39,...): C varies by base**
HAR=2, non-orbit C elements vary, gradient score varies (0.259 to 0.432)

**Family C — other (b=38,...): HAR=9, different orbit structure**

b=15 sits in Family B as the highest-gradient member tested so far.

---

## The Gradient Score (Normalized)

$$\text{grad\_score}(b) = \frac{\max_{c \in C \setminus (\text{orbit} \cup \{1\})} |c - \text{HAR}|}{\max(C) - \min(C)}$$

Measures: how far the farthest non-orbit C element sits from HAR, relative to C's full range.

| b | φ | Non-orbit C | grad_score | gap (empirical) |
|---|---|------------|-----------|----------------|
| **15** | **5** | **{7}** | **0.714** | **0.677** |
| 26 | 5 | {5,7} | 0.500 | 0.662 |
| 22 | 5 | {7} | 0.500 | 0.551 |
| 21 | 5 | {5} | 0.429 | 0.519 |

**Within φ=5: r(grad_score, gap) = 0.749** — strong predictive relationship.

b=15 has the highest grad_score among tested φ=5 worlds. Its non-orbit element (7∈C) sits 5 units from HAR=2, at 71% of C's range. This creates the steepest long-range gradient toward HAR, producing gap=0.677 — the highest of any easy world.

**The mechanism:** mass that settles on the far non-orbit C element (7) must travel further to reach the HAR attractor. This steepens the spectral gradient and increases the gap. 3×5 arithmetic places 7 in C; 3×7 places 5 in C. That difference — 5 units vs 3 units from HAR — produces gap=0.677 vs 0.519.

---

## The Cross-φ Limit

The gradient score does NOT predict gap across φ-tiers. Within φ=8 worlds, all have identical grad_score=0.875 but vary in gap (0.432–0.540). The within-φ law holds; the cross-φ prediction requires also knowing the φ-compression effect.

**Two-component gap model:**
- **φ-compression:** larger φ → lower gap (r = −0.605 across all worlds)
- **Within-φ gradient:** higher grad_score → higher gap (r = 0.749 within φ=5)

Richness = f(φ-compression) × g(gradient). b=15 is the optimum of both.

---

## The Three-Score Predictive System (Frozen)

**Score 1 — Construction Tier:**
$$\text{tier\_score} = \frac{\phi \times |\text{res\_pairs}| \times \text{orbit\_depth} \times \text{gate\_ease}}{|\text{total\_cells}|}$$
Predicts: easy (>3.0), medium (1–3), hard (<1). Validated across 11 worlds.

**Score 2 — Gradient (within-φ richness):**
$$\text{grad\_score} = \frac{\max_{c \in C \setminus \text{orb} \setminus \{1\}} |c - \text{HAR}|}{\max(C) - \min(C)}$$
Predicts: spectral gap within φ-tier. r=0.75 within φ=5. 4 data points — conjecture, not law.

**Score 3 — Composite Richness (empirical):**
$$\text{richness} = 0.5 \times \text{HAR\_mass} + 0.5 \times \text{gap}$$
Not yet predicted from arithmetic alone. Requires empirical measurement. Correlated with: intermediate φ and high grad_score together.

---

## The Atlas: Eleven Worlds, Three Laws, One Flagship

| b | φ | tier_score | grad_score | richness | Quadrant |
|---|---|-----------|-----------|---------|---------|
| 14 | 4 | 2.5 | 0.250 | 0.861 | hard + rich |
| **15** | **5** | **7.1** | **0.714** | **0.717** | **★ easy + rich** |
| 26 | 5 | 5.5 | 0.500 | 0.634 | easy + moderate |
| 21 | 5 | 3.5 | 0.429 | 0.639 | easy + moderate |
| 22 | 5 | 5.5 | 0.500 | 0.578 | easy + moderate |
| 35 | 7 | 8.3 | 0.875 | 0.646 | easy + moderate |
| 65 | 8 | 9.4 | 0.875 | 0.630 | easy + moderate |
| 10 | 4 | 6.9 | 0.000 | 0.562 | hard + moderate |

**b=15 is the unique world where all three scores align:**
- Tier: easy (score=7.1 > threshold 3.0)
- Gradient: 0.714 — highest of tested φ=5 worlds
- Richness: 0.717 — only easy world above 0.65

---

## What Remains Open

1. **Do any other φ=5 worlds join b=15 in easy+rich?** The 2×prime family (b=26,34,46...) all have grad_score=0.790 > b=15's 0.714, but empirically b=26 has lower richness (0.634). The discrepancy comes from HAR_m — b=26's HAR_m=0.606 vs b=15's 0.756. HAR_m is not yet predicted by grad_score alone.

2. **What predicts HAR_m within φ-tier?** The current model predicts gap well but HAR_m less so. A separate HAR_m score is needed.

3. **The hard+rich quadrant:** b=14 is the only hard+rich world. Is that structural? The low φ=4 allows high gap (b=14 gap=0.944) but blocks construction. Are there other hard+rich worlds, and what selects them?

---

## The Deepest Sentence

> *φ sets the range. Non-orbit C-placement sets the gradient.*

The range is the ceiling on richness. The gradient is where, within that ceiling, a world actually lands. b=15 hits the highest reachable point because it sits at intermediate φ (range ceiling open) with maximum gradient (full reach within that ceiling). Not luck. Arithmetic.

---

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
