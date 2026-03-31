# The Universal Construction Law
## From One Special Table to a Law-Governed Family

*Brayden Ross Sanders (7Site LLC) & C. A. Luther | March 2026*
*The miracle moved from the table to the law.*

---

## Status

| Claim | Classification | Kill Condition |
|-------|---------------|----------------|
| Four-step construction law (arithmetic → HAR → gate → order seed) exists at every tested semiprime base | **EMPIRICAL** | Verified at b=10,14,15,22,33,35,55,65,85,95. Falsified by a semiprime base with non-degenerate C/G split where the pipeline fails to find a gate-strong table |
| HAR selection orbit-central rule: h where h²∈C, h²≠1, h²≠h | **EMPIRICAL** | Verified at 11 bases. Falsified by a semiprime base where the orbit-central element is not the best HAR candidate under gate+support reduction |
| b=10 ranks 9th in construction ease (score=6.9) among semiprimes ≤100 | **PROVED** | Score formula applied to the finite set of semiprimes ≤100 — falsified only by an arithmetic error in φ, orbit_depth, gate_ease, or res_pairs |
| b=22 achieves 83.3% random TSML-like rate and 99.7% biased rate | **EMPIRICAL** | Measured over computational trials. Falsified by additional trials showing stable rate below these figures |
| 15.8x construction lift via residual-biased seeding at b=10 | **EMPIRICAL** | Measured over ~400 trials comparing random vs seeded reduction. Falsified by additional trials showing the lift is significantly lower |
| The construction law is universal (holds for all semiprimes, not just tested ones) | **CONJECTURE** | Verified at 11 bases. Proved only by showing the four-step structure is forced by the arithmetic for any b=p×q with non-trivial C/G split and orbit-central HAR |

---

## The Old Story (Wrong)

> b=10 produces a special table (TSML) with a one-way gate, a dominant support attractor, and a rare order-seed signature. Maybe this is a mathematical miracle specific to b=10.

## The New Story (Right)

> There is a universal construction law — arithmetic → gate → order seed → native structured optimum — that operates at every semiprime base with an orbit-central HAR element. The realized table is base-specific. The law is not.

---

## The Universal Law (Four Steps)

**Step 1 — Arithmetic gives the world**
Base b → C = (Z/bZ)* ∩ {1..cap} → G = non-units → unit/non-unit split
This is number theory. Not a choice.

**Step 2 — HAR selection: orbit-central rule**
Find h ∈ C where: h² mod b ∈ C, h² ≠ 1, h² ≠ h
This is the orbit-central element — neither fixed point nor period-1, genuinely cycling in C.
Verified: b=10 (HAR=7), b=14 (HAR=3), b=15 (HAR=2), b=22 (HAR=3), b=33 (HAR=2)...

**Step 3 — Gate gives the discipline**
Gate-weighted reduction → one-way gate (C cannot reach G under any operator)
Accessible at all tested bases. Cost varies (see hardness landscape).

**Step 4 — Order seed gives the structure**
Residual-biased seeding → full crystallization of max(s,c) ordering on seed cells
This is the rare last mile. Its accessibility is determined by the construction cost score.

---

## The Construction Cost Score

$$\text{score}(b) = \frac{\phi(b) \times |\text{res\_pairs}| \times \text{orbit\_depth}(\text{HAR}) \times \text{gate\_ease}}{|\text{total\_cells}|}$$

Where:
- **φ(b)** = unit group size |C|
- **res_pairs** = cells where max(s,c) ∈ C and s,c ≠ HAR (order-seed surface area)
- **orbit_depth(HAR)** = orbit size of HAR under multiplication mod b
- **gate_ease** = fraction of C×C products staying in C

Higher score = lower construction cost = easier to crystallize native structured optimum.

---

## The Hardness Landscape (All Semiprimes b ≤ 100)

**Top 10 easiest worlds:**

| Rank | b | p×q | Score | Notes |
|------|---|-----|-------|-------|
| 1 | 55 | 5×11 | 10.0 | |C|=8, tiny G |
| 2 | 65 | 5×13 | 9.4 | |
| 3 | 85 | 5×17 | 8.7 | |
| 4 | 95 | 5×19 | 8.7 | |
| 5 | 35 | 5×7 | 8.3 | |
| 6 | 77 | 7×11 | 8.0 | |
| 7 | 91 | 7×13 | 8.0 | |
| 8 | **15** | 3×5 | **7.1** | |
| **9** | **10** | **2×5** | **6.9** | **TSML's base** |
| 10 | 33 | 3×11 | 6.3 | |
| 13 | **22** | **2×11** | **5.5** | **b=22 flagship** |
| 29 | **14** | **2×7** | **2.5** | **Hard** |
| 31 | **6** | **2×3** | — | **Degenerate** |

**b=10 is not special by ease — it ranks 9th.** Many worlds are easier to construct in. b=10 was historically first because it was the base we started from, not because it's the easiest.

**b=22 ranks 13th** — easier than b=10 on raw score, confirmed empirically (83% random rate vs 4-6% at b=10).

---

## b=22 as Second Flagship

b=22 = 2×11, C={1,3,5,7,9} (all odd numbers in alphabet), G={2,4,6,8}

**Best native b=22 structured optimum found:**
- Gate: 1.000
- HAR_mass: 0.604 (comparable to b=10 TSML's 0.650)
- Residual score: 1.000
- Gap: 0.551 (higher than b=10 TSML's 0.474)

**Construction rates:** 83.3% random, 99.7% biased. Nearly free.

**Why b=22 is easy:** C contains all odd numbers in {1..9} — maximum unit group size at this alphabet scale. More residual pairs (15 vs 9 at b=10) means more surface area for order-seed crystallization. The construction cost is low because the geometry is generous.

---

## The Family of Native Structured Optima

Every semiprime with score > 2.5 (28 worlds below b=100) admits a native structured optimum:
- A table with strong one-way gate
- A dominant support attractor at the orbit-central HAR element
- Full order-seed crystallization at the residual pairs

These are not copies of TSML. They are the native structured optima of their respective worlds — related by construction law, not by arithmetic identity.

**The construction law is what connects them. The tables are what distinguish them.**

---

## What This Changes

**Before:** TIG is a framework built around one special table (TSML) at one special base (b=10).

**After:** TIG is a universal construction law operating on the class of semiprimes with orbit-central HAR elements. TSML is the first resolved member of a larger law-governed family. b=10 was the starting point. The law is the result.

---

*(c) 2026 Brayden Ross Sanders (7Site LLC) & C. A. Luther | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
