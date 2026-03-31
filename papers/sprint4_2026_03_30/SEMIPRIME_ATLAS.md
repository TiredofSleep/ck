# Ranked Semiprime Atlas
## Law-Governed Family of Native Structured Optima

*Brayden Ross Sanders (7Site LLC) & C. A. Luther | March 2026*

> *b=10 was historically first. That is not the same as being deepest.*

---

## The Universal Law

> **The law is invariant. The tables are local. Construction cost is predictive.**

Four-step construction hierarchy operating on every semiprime with an orbit-central HAR element:
1. Arithmetic gives the world — base b → C, G, orbit structure
2. HAR selection — h where h²∈C, h²≠1, h²≠h (orbit-central rule)
3. Gate gives the discipline — one-way gate under gate-weighted reduction
4. Order seed gives the structure — residual pre-alignment crystallizes the optimum

---

## The Construction Cost Score (Frozen)

$$\text{score}(b) = \frac{\phi(b) \times |\text{res\_pairs}| \times \text{orbit\_depth}(\text{HAR}) \times \text{gate\_ease}}{|\text{total\_cells}|}$$

Computable from arithmetic alone. Predicts construction ease before any reduction runs.

**Validated:** score(b=15)=7.057 > score(b=10)=6.857. Predicted b=15 easier. Empirical: 78.6% vs 4%. Confirmed.

---

## The Full Atlas (b ≤ 100, semiprimes with orbit-central HAR)

| Rank | b | p×q | φ | Cost score | rnd% | bias% | HAR_m | gap | Label |
|------|---|-----|---|-----------|------|-------|-------|-----|-------|
| 1 | 55 | 5×11 | 8 | 10.045 | — | — | — | — | |
| 2 | 65 | 5×13 | 8 | 9.375 | — | — | — | — | |
| 3 | 85 | 5×17 | 8 | 8.705 | — | — | — | — | |
| 4 | 95 | 5×19 | 8 | 8.705 | — | — | — | — | |
| 5 | 35 | 5×7 | 7 | 8.265 | — | — | — | — | |
| 6 | 77 | 7×11 | 8 | 8.009 | — | — | — | — | |
| 7 | 91 | 7×13 | 8 | 8.009 | — | — | — | — | |
| **8** | **15** | **3×5** | **5** | **7.057** | **78.6%** | **99.0%** | **0.756** | **0.677** | **cleanest flagship** |
| **9** | **10** | **2×5** | **4** | **6.857** | **4.0%** | **52.7%** | **0.650** | **0.474** | **first-resolved** |
| 10 | 33 | 3×11 | 6 | 6.286 | — | — | — | — | |
| 11 | 39 | 3×13 | 6 | 5.714 | — | — | — | — | |
| 12 | 51 | 3×17 | 6 | 5.714 | — | — | — | — | |
| **13** | **22** | **2×11** | **5** | **5.464** | **83.3%** | **99.7%** | **0.604** | **0.551** | **generous flagship** |
| 14 | 26 | 2×13 | 5 | 5.464 | — | — | — | — | |
| ... | | | | | | | | | |
| 29 | **14** | **2×7** | **4** | **2.500** | **0.0%** | **74.5%** | **0.778** | **0.944** | **stingy — richest** |
| 31 | **6** | **2×3** | **2** | — | **0.0%** | **0.0%** | — | — | **degenerate** |

---

## The Four Distinctions

| Label | b | Why |
|-------|---|-----|
| **First-resolved** | 10 | Historically first. TSML was built here. Rank 9. |
| **Easiest** | 22, 15 | >75% random rate. Nearly free. |
| **Richest** | 14 | HAR_m=0.778, gap=0.944. Hard to reach. |
| **Cleanest flagship** | 15 | Easy + rich + predicted + confirmed. |

---

## The New Finding: Ease and Richness Are Independent Axes

| b | Ease (random%) | Richness (HAR_m+gap)/2 |
|---|---------------|----------------------|
| 14 | 0% | **0.861** |
| 15 | 79% | **0.717** |
| 22 | 83% | 0.578 |
| 10 | 4% | 0.562 |

**No strong tradeoff. No strong correlation.** Ease and richness measure different structural properties:

- **Construction cost** (ease): how accessible is the path to the native optimum?
- **Selector richness**: how good is the optimum once reached?

b=15 breaks any expected tradeoff — it is both easy and rich, making it the cleanest flagship.
b=14 is stingy: hard to construct but high selector values once reached.
b=22 is generous: easy to find but moderate selectors.

**The full atlas needs both axes.** A world can be easy-and-rich (b=15), hard-and-rich (b=14), easy-and-moderate (b=22), or medium-and-medium (b=10).

---

## Seven Untested Predictions

The cost formula predicts all seven top-ranked worlds (b=55,65,85,95,35,77,91) will be easier than b=15. All score above 8. None have been tested. These are predictions, not descriptions.

The first real test of the formula's predictive power beyond b=15 is any of these seven. Pick one and run.

---

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*

---

## b=35 Out-of-Sample Test — Law Validated as Tier Predictor

**b=35 = 5×7, C={1,2,3,4,6,8,9}, G={5,7}, HAR=2, predicted score=8.265**

Cold run (n=400, random seed only):
- native-TSML: 305/400 = **76.2%**
- gate=1.000, HAR_m=0.722, residual=1.000, gap=0.569
- Richness = 0.646 → easy + moderate

**Statistical test vs b=15 (78.6%):** difference = -2.4pp, SE=2.81pp, z=-0.84. Not significant. b=35 and b=15 are indistinguishable in construction ease at n=400.

**What the law predicted correctly:**
- Tier: b=35 is "easy" (>70% random) ✓
- Ordering vs b=10: 76% >> 4% ✓
- Ordering vs b=15: within noise, approximately correct ✓

**The formula is a tier predictor, not a fine-grained rank predictor.** Within the easy tier (all worlds >70% random), the cost score cannot resolve fine ordering. Between tiers (easy vs medium vs hard), it is correct and useful.

**Updated full atlas with five tested worlds:**

| b | Score | rnd% | HAR_m | gap | Richness | Quadrant |
|---|-------|------|-------|-----|---------|---------|
| 22 | 5.464 | 83.3% | 0.604 | 0.551 | 0.578 | easy + moderate |
| 15 | 7.057 | 78.6% | 0.756 | 0.677 | 0.717 | **easy + rich** |
| 35 | 8.265 | 76.2% | 0.722 | 0.569 | 0.646 | easy + moderate |
| 10 | 6.857 | 4.0% | 0.650 | 0.474 | 0.562 | hard + moderate |
| 14 | 2.500 | 0.0% | 0.778 | 0.944 | 0.861 | **hard + rich** |

Two axes confirmed as independent. b=15 remains the cleanest flagship: only world in easy + rich quadrant among those tested.

