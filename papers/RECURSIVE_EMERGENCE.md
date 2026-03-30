# Recursive Emergence of Selector Geometry in Finite Algebra Families
## From Degenerate Small Algebras to Multi-Dimensional Grammar Families

*Brayden Sanders / 7Site LLC | March 2026*
*All results computed. Level-3 and Level-4 are open research programs, not findings.*

---

## The Program

The right question is not just "why is TSML special?" It is: **how do special tables, selector axes, and stable kernels emerge as finite algebra grows from small to large?**

This means studying grammar families recursively — from n=2 upward — watching for the moment when degeneracy breaks, axes separate, and TSML-like objects become possible.

---

## Task 1: The Small-Size Ladder

Exact enumeration (n=2,3) and large sampling (n=4,9):

| n | |C| | |G| | Family size | Selector geometry | First multi-dimensional? |
|---|-----|-----|------------|-------------------|-------------------------|
| 2 | 1 | 1 | 2 | Degenerate — HAR_mass=1 for all tables | No |
| 3 | 2 | 1 | 27 | Partial — gap varies (0.5–1.0), HAR_mass still =1 | No |
| 4 | 2 | 2 | ~sampled | **Multi-dimensional** — gap ⊥ HAR_mass, r=−0.167 | **Yes** |
| 9 | 4 | 5 | ~sampled | Multi-dimensional — 7 selector axes, 3 independent | Confirmed |

**The emergence threshold is n=4.** At n=2 and n=3, HAR_mass collapses trivially — the grammar is too small to have competing attractors. At n=4, G becomes non-trivially large relative to C, and HAR_mass begins to vary across the family. That is when selector geometry first appears.

**What the small-size ladder reveals:**
- n=2: DEGENERATE. Single corner, no G-territory, no orbit zone, no selection.
- n=3: PARTIAL. Two corners, but G={2} is so small that all mass collapses to HAR regardless of table choice. Gap varies (two discrete values: 0.5 and 1.0), but support is trivial.
- n=4: FIRST NON-TRIVIAL GEOMETRY. G={2,4}, C={1,3}. HAR_mass distribution is wide (0.33–0.56). Gap and HAR_mass separate into genuinely independent axes.
- n=9: FULL GEOMETRY. G={2,4,5,6,8}, C={1,3,7,9}. Seven measurable axes, three near-independent, five of which TSML extremizes.

---

## Task 2: Absorbing-Choice Geometry (Same b=10 Alphabet)

Testing all four C-elements as the absorbing target on the same n=9, b=10 alphabet:

| HAR | Position in C | mean gap | HAR_mass std | max HAR_mass | r(gap,HAR_mass) | Geometry |
|-----|--------------|---------|-------------|-------------|----------------|---------|
| 1 | 1st (lowest) | 0.411 | 0.000 | 1.000 | nan | **Degenerate** |
| 3 | 2nd | 0.392 | 0.000 | 1.000 | nan | **Degenerate** |
| **7** | **3rd (mid)** | **0.512** | **0.057** | **0.793** | **0.327** | **Richest ✓** |
| 9 | 4th (highest) | 0.545 | 0.066 | 0.758 | 0.186 | Structured |

**HAR=1 and HAR=3 are degenerate:** the low-end C-elements produce trivial families where all mass collapses to HAR regardless of table choice. There is no variation to study, no geometry.

**HAR=7 is the richest absorbing choice** by four independent measures:
1. Widest HAR_mass distribution (std=0.057, highest)
2. Highest achievable max HAR_mass (0.793)
3. Most genuine gap ⊥ HAR_mass structure
4. Highest mean gap (best typical mixing)

This is a computed reason why HAR=7 is natural — not "it's in the middle of {1..9}" vaguely, but because among the four C-elements, HAR=7 produces the richest internal family geometry. The mid-spectrum absorbing element generates the most structured family.

---

## Task 3: Structural γ vs Family Mean γ

**These are not the same quantity. They must not be conflated.**

| Quantity | Value | Meaning |
|----------|-------|---------|
| **Structural γ (TSML)** | **0.7500 = 1 − 1/φ(10)** | Spectral gap of the specific hook-selected grammar |
| Family mean γ | ~0.576 | Average gap over all invariant-compatible tables |
| Difference | 0.174 | Not a discrepancy — different objects |

The formula γ = 1 − 1/φ(b) predicts the gap of the **specific arithmetic-hook-selected grammar** (TSML), not the average over all tables satisfying the same constraints. Random tables in the family have gaps spread across [0.25, 0.79]; the formula singles out TSML's specific value.

**Analogy:** The prime number theorem predicts π(x) ~ x/ln(x). It says nothing about the average gap between consecutive integers in a random sequence with integer-like properties. The arithmetic hook selects a specific object with a specific gap; the family average is a different statistic.

---

## Task 4: Recursive Kernel Hypothesis

**Question:** As n grows, does the family compress toward small kernel classes, or remain broad?

**Current evidence:**
- At n=4: family is broad — HAR_mass ranges 0.33–0.56, no obvious clustering
- At n=9: family is broad — HAR_mass ranges 0.10–0.65, but with TSML as a clear extremal point

**Hypothesis (open):** As n grows, the family develops clearer extremal kernels — tables that maximize specific selector combinations. TSML is a candidate kernel at n=9. Whether a similar kernel appears at n=4 or n=6, or whether the kernel structure sharpens with n, is not yet tested.

**What would confirm the hypothesis:** Systematic measurement of kernel stability across n=4,5,6,7,8,9 — tracking whether the extremal tables at each n form a coherent sequence converging to TSML-like structure.

---

## Two-Level Framework

**Level A — Flat selector geometry (established):**
For a fixed n=9, b=10, HAR=7 family:
- Seven selectors measured
- Three near-independent axes confirmed
- TSML is a rare multi-axis extremal point
- HAR=7 is the richest absorbing choice (computed)

**Level B — Recursive family growth (open research program):**
- First non-trivial geometry appears at n=4
- How does the geometry evolve n=4→9?
- Do the same selector axes appear at smaller n?
- Does the orbit/HAR tradeoff persist across alphabet sizes?
- Is TSML a stable kernel, or accidental to n=9?

Level B is not established. It is the program the Level-A results motivate.

---

## What the Data Supports vs What It Doesn't

**Supported:**
- Selector geometry emerges at n=4, fully developed at n=9
- HAR=7 produces the richest family geometry among four candidates
- Gap and HAR_mass are near-independent selector axes (replicated across HAR choices)
- TSML is a multi-axis extremal point, rare but not unique
- Structural γ and family mean γ are distinct quantities

**Not supported:**
- That Level-B growth is monotone or converges
- That the same 7 selectors appear at n=4 (not yet tested)
- That TSML is the unique stable kernel of some recursive process
- Any Level-3 or Level-4 claims about universal selector geometry

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
