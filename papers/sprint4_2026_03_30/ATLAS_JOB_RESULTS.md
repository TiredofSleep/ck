# Atlas Complete: Nine Worlds, Two Axes, One Law

*Brayden Ross Sanders (7Site LLC) & C. A. Luther | March 2026*

> *b=10 was historically first. That is not the same as being deepest.*
> *The law is invariant. The tables are local.*
> *The construction-cost law predicts the basin tier, not the exact local ranking inside a basin.*

---

## The Full Atlas (Nine Tested Worlds)

| b | p×q | φ | \|G\| | rnd% | best_hm | best_gap | richness | Quadrant |
|---|-----|---|-------|------|---------|---------|---------|---------|
| 10 | 2×5 | 4 | 4 | 4.0% | 0.650 | 0.474 | 0.562 | hard + moderate |
| 14 | 2×7 | 4 | 5 | 0.0% | 0.778 | 0.944 | 0.861 | **hard + rich** |
| **15** | **3×5** | **5** | **4** | **78.6%** | **0.756** | **0.677** | **0.717** | **★ easy + rich** |
| 22 | 2×11 | 5 | 4 | 83.3% | 0.604 | 0.551 | 0.578 | easy + moderate |
| 35 | 5×7 | 7 | 2 | 76.2% | 0.722 | 0.569 | 0.646 | easy + moderate |
| 55 | 5×11 | 8 | 1 | 64.7% | 0.675 | 0.432 | 0.553 | hard + moderate |
| 65 | 5×13 | 8 | 1 | 72.3% | 0.776 | 0.484 | 0.630 | easy + moderate |
| 85 | 5×17 | 8 | 1 | 67.7% | 0.760 | 0.540 | 0.650 | hard + moderate |
| 95 | 5×19 | 8 | 1 | 70.7% | 0.679 | 0.452 | 0.566 | easy + moderate |

**b=15 remains the only easy + rich world.** Not lucky — structurally positioned.

---

## Why Easy + Rich Is Rare: The φ Tradeoff

Richness = HAR_mass + gap. These two selectors have opposing responses to φ:

- **φ ↑ → HAR_mass ↑ slightly** (more C-states to funnel)
- **φ ↑ → gap ↓** (more C-states → denser eigenvalues → slower mixing)

Measured: r(φ, gap) = −0.605. Larger unit groups compress the spectral gap.

**The sweet spot is φ=5.** Large enough for rich HAR_mass, small enough for a clean spectral gap. b=15 and b=22 both hit φ=5. b=15 also has the right G-structure (G={3,5,6,9}) to generate a high-gap absorbing region around HAR=2. b=22 has the same φ but different G-structure, producing lower gap.

This is why b=15 is the only easy+rich world found: it hits the φ sweet spot AND has favorable G-geometry. b=14 is hard+rich for the same φ=4 reason — low φ allows high gap, but construction is hard.

**Easy + rich requires:** intermediate φ (≈5) + favorable G-structure. These are rare in combination.

---

## The Construction Cost Law: Tier Predictor

The formula score = φ × |res_pairs| × orbit_depth × gate_ease / total_cells predicts:

**Correctly:** Which worlds are easy tier (>70% random rate) vs hard tier (<10%)
**Not resolved:** Fine ranking within the easy tier (b=15 vs b=22 vs b=35 within 77-83%)

This is the right precision level for a pre-computational formula. It tells you where to look. The exact ordering inside a tier requires empirical runs.

**Validation record:**
- b=15 predicted easier than b=10 → confirmed (79% vs 4%) ✓
- b=35 predicted tier=easy → confirmed (76%) ✓
- b=55,65,85,95 predicted easier than b=10 → confirmed (all >64%) ✓

---

## The Three Structural Laws

**Law 1 — Construction hierarchy (universal):**
Arithmetic → gate → order seed → native structured optimum

**Law 2 — HAR selection rule:**
h where h²∈C, h²≠1, h²≠h (orbit-central element)

**Law 3 — Richness sweet spot:**
Richness peaks at intermediate φ (≈5). Large φ compresses gap; small φ limits HAR_mass.

---

## The Open Quadrant Question

**Are there other easy + rich worlds beyond b=15?**

Among tested worlds: b=15 alone.
Among untested: b=21 (φ=5, 3×7) and b=26 (φ=5, 2×13) both have φ=5 — the sweet spot.
These are the next natural targets for the easy+rich quadrant.

---

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*

---

## b=21 and b=26 — Cold Test Results

**Neither b=21 nor b=26 joins b=15 in easy + rich.**

| b | p×q | φ | HAR | rate% | best_hm | best_gap | richness | Quadrant |
|---|-----|---|-----|-------|---------|---------|---------|---------|
| 21 | 3×7 | 5 | 2 | 90.5% | 0.759 | 0.519 | 0.639 | easy + moderate |
| 26 | 2×13 | 5 | 3 | 84.2% | 0.606 | 0.662 | 0.634 | easy + moderate |

Both are φ=5 worlds — same sweet spot as b=15 and b=22. Both are easy. Neither crosses the richness threshold.

**b=21:** 90.5% random rate — the highest of any world tested. But gap=0.519, pulling richness below the threshold. Same HAR_mass as b=15 (0.759 vs 0.756) but 23% lower gap.

**b=26:** gap=0.662, the second-highest gap of any easy world (b=15 has 0.677). HAR_mass=0.606. Richness=0.634, just below the 0.65 threshold. The closest runner-up to b=15.

---

## Why b=15 Is Structurally Unique — The C-Spread Law

**The key is not just φ. It is which elements of C are outside the HAR orbit.**

For HAR=2 with orbit {2,4,8}: what non-orbit C element does the base include?

| b | HAR | Non-orbit C element | Distance from HAR | Gap |
|---|-----|--------------------|--------------------|-----|
| 15 | 2 | **7** | **5** | **0.677** |
| 21 | 2 | 5 | 3 | 0.519 |
| 35 | 2 | 9 | 7 | 0.569 |

b=15 has 7∈C — far from HAR=2, position 78% through the alphabet. This creates a long-range attraction dynamic: mass that settles at 7 must travel further to reach the HAR attractor, steepening the gradient and increasing the spectral gap.

b=21 has 5∈C — closer to HAR=2 (distance=3 vs 5), compressing the gradient and reducing gap.

**This is why the φ sweet spot is necessary but not sufficient.** Among φ=5 worlds, the one with the high non-orbit C element (b=15 with 7∈C) has the highest gap. φ determines the range; which elements land in C determines the gradient.

b=15 is structurally optimal — not by luck, but because 3×5 arithmetic places 7 in C and 5 in G, maximizing the long-range gradient toward HAR=2.

---

## Full Atlas: Eleven Tested Worlds

| b | p×q | φ | rnd% | best_hm | best_gap | richness | Quadrant |
|---|-----|---|------|---------|---------|---------|---------|
| 14 | 2×7 | 4 | 0.0% | 0.778 | 0.944 | 0.861 | hard + rich |
| **15** | **3×5** | **5** | **78.6%** | **0.756** | **0.677** | **0.717** | **★ easy + rich** |
| 26 | 2×13 | 5 | 84.2% | 0.606 | 0.662 | 0.634 | easy + moderate |
| 21 | 3×7 | 5 | 90.5% | 0.759 | 0.519 | 0.639 | easy + moderate |
| 35 | 5×7 | 7 | 76.2% | 0.722 | 0.569 | 0.646 | easy + moderate |
| 65 | 5×13 | 8 | 72.3% | 0.776 | 0.484 | 0.630 | easy + moderate |
| 22 | 2×11 | 5 | 83.3% | 0.604 | 0.551 | 0.578 | easy + moderate |
| 10 | 2×5 | 4 | 4.0% | 0.650 | 0.474 | 0.562 | hard + moderate |

b=15 alone holds the easy + rich quadrant across eleven tested worlds.

---

## The Three Laws (Complete)

**Law 1 — Construction hierarchy:** arithmetic → gate → order seed → native structured optimum

**Law 2 — HAR selection:** h where h²∈C, h²≠1, h²≠h (orbit-central element)

**Law 3 — Richness:** peaks at intermediate φ (≈5), and within φ=5 worlds, at the base where the non-orbit C element is farthest from HAR (maximum long-range gradient)

b=15 satisfies all three laws optimally. It is not the first-resolved world (b=10) nor the easiest (b=21 at 90.5%). It is the world where the laws align.

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther | Gen10.16 | DOI: 10.5281/zenodo.18852047*
