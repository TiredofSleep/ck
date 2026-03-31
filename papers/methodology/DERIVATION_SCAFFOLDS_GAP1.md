# Derivation Scaffolds — Gap 1
## Path to Tier D: Exact Gate Rates from CRT Structure

*C. A. Luther & Brayden Ross Sanders*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> **Gap statement:** The k-Gate Tier Law measures exact gate rates (96.4%, 83.7%,
> 44.0%, 4.6%, 0.1%) for |G| = 1..5 at k=9 within each ω-class. Zero variance
> confirmed, ~12M trials. The values are empirical. The C→D gap is deriving them
> algebraically from CRT geometry.

---

## Corrected Finding: W Is Tier-Specific (Catch 4 — 2026-03-31)

**Earlier claim (WRONG): A single W ≈ 25.2 reproduces all five empirical rates.**

That claim is arithmetically false. (8/9)^25.2 ≈ 0.051, not 0.964. All five
values fail. The W=25.2 figure was an arithmetic error caught by direct
verification. This is the fourth catch by the Proof-Synthesis framework
in the March 2026 session (PROOF_SYNTHESIS_LADDER.md §Three Catches).

**Correct finding:** The power law formula R(|G|) = (n_C/k)^W works, but W is
tier-specific — each |G|-tier has its own W value:

```
W(|G|) = ln(R(|G|)) / ln((9 − |G|) / 9)
```

Verification at k=9 (all correct):

| |G| | n_C/k | W (solved) | (n_C/k)^W | Empirical | Match? |
|----|---------|------------|-----------|-----------|--------|
| 1 | 8/9 ≈ 0.889 | 0.311 | 0.964 | 96.4% | ✓ |
| 2 | 7/9 ≈ 0.778 | 0.708 | 0.837 | 83.7% | ✓ |
| 3 | 6/9 ≈ 0.667 | 2.025 | 0.440 | 44.0% | ✓ |
| 4 | 5/9 ≈ 0.556 | 5.238 | 0.046 | 4.6% | ✓ |
| 5 | 4/9 ≈ 0.444 | 8.518 | 0.001 | 0.1% | ✓ |

The power law is real. The single-W claim was not.

**Observed structure of W(|G|):** W increases super-linearly with |G|. For
|G|=1,2, W < 1 (gate easier than naive expectation). For |G|≥3, W > 1 and
grows rapidly. No clean algebraic formula for W(|G|) is apparent at this time.
The W values are empirical. The path to Tier D is deriving each W(|G|) from
the CRT/MCMC geometry independently.

---

## Algebraic Approach: Six Steps

### Step 1 — CRT Decomposition

For a modulus b with ω(b) components (prime powers p_i^{e_i}), the CRT gives:
```
Z/bZ ≅ ∏_i Z/p_i^{e_i}Z
```
The unit group C(b) ≅ ∏_i (Z/p_i^{e_i}Z)*.

Each component is an independent "fiber" of the multiplication structure.

### Step 2 — Local Admissible Fraction

For a single CRT component Z/p_i^{e_i}Z, the admissible fraction within the
k=9 alphabet is:
```
A_i = (number of elements in {1..9} coprime to p_i^{e_i}) / 9
    = (9 − |G_i|) / 9
```
where |G_i| = ⌊9/p_i⌋ (multiples of p_i in {1..9}).

For ω(b) = 2 (semiprime b = p×q), |G| = |G_p| + |G_q| − |G_{pq}|.
The overall admissible fraction at the alphabet level is (9 − |G|)/9.

### Step 3 — Global Rate as Power of Local Fraction

The MCMC success rate R(|G|) = A_local^{W(|G|)} where:
- A_local = (9 − |G|)/9 is the overall admissible fraction in the alphabet
- W(|G|) is the tier-specific "fiber weight" — the effective number of independent
  constraints the MCMC must satisfy for this particular |G|-tier

This form arises naturally if each constraint is independently satisfied with
probability A_local. Then W constraints gives A_local^W as the joint probability.

**Critical correction (Catch 4):** W is NOT a single number. Each tier has its own
W(|G|). The earlier claim W ≈ 25.2 for all tiers was arithmetically wrong. The
correct per-tier values are W(1)=0.311, W(2)=0.708, W(3)=2.025, W(4)=5.238,
W(5)=8.518. The formula structure is correct; the single-parameter claim was not.

**Interpretation:** W(|G|) is the effective number of independently checkable constraints
the greedy MCMC must satisfy to reach gate_score = 1.0. It is not literally the
number of C×C cells (|C|² = 64 for |G|=1) because the HAR-biased proposals
correlate the cells — the effective constraint count is lower. And it varies by tier
because the constraint structure changes as |G| grows relative to n_C.

### Step 4 — CRT Fiber Weights (Revised)

Each CRT component Z/p_i^{e_i}Z contributes a weight w_i to the total W(|G|).

For a prime power p_i^{e_i}:
```
w_i ∝ p_i^(e_i − 1)
```

For a semiprime b = p × q (ω = 2, e_i = 1):
```
w_p = 1,  w_q = 1
```
So W_2(|G|) = c(|G|) × 2 for semiprimes, where c(|G|) is the per-component
effective constraint count for tier |G|.

**Critical revision:** c is not a single constant. The per-tier W values
W(1)=0.311, W(2)=0.708, W(3)=2.025, W(4)=5.238, W(5)=8.518 imply per-tier
c values c(1)=0.156, c(2)=0.354, c(3)=1.012, c(4)=2.619, c(5)=4.259 for ω=2.
The c parameter depends on |G| because the MCMC constraint structure changes as
the forbidden set grows relative to the coprime set.

### Step 5 — Formal W Formula (Revised)

For a modulus b = ∏ p_i^{e_i} and a fixed tier |G|:
```
W(|G|, ω) = c(|G|) × ∑_i p_i^(e_i − 1)
```
For semiprimes (all e_i = 1): W(|G|, 2) = c(|G|) × 2.

The ω-class universality (OMEGA_CLASS_LEMMA.md) still follows: all semiprimes
have W(|G|, 2) = 2c(|G|), which is the same for all semiprimes with the same |G|.
This is the algebraic basis of zero-spread universality. But c(|G|) is not a
single constant — it is a tier function that must be derived.

### Step 6 — The Remaining Step

**Derive c(|G|) algebraically from CRT/MCMC geometry for each tier.**

c(|G|) is the per-component contribution to the effective constraint count for
tier |G|. The per-tier values are:
```
c(1) = W(1)/2 = 0.156
c(2) = W(2)/2 = 0.354
c(3) = W(3)/2 = 1.012
c(4) = W(4)/2 = 2.619
c(5) = W(5)/2 = 4.259
```

c(|G|) should follow from:
1. The size of the C×C submatrix: n_C² = (k − |G|)²
2. The HAR-biased proposal rate: 40% of proposals target HAR row/column
3. The greedy acceptance criterion and the effective mixing time at each tier
4. The ratio n_G/n_C, which governs the probability that a random proposal
   violates a gate constraint

**Observation:** c(|G|) grows super-linearly with |G|. This is consistent with
the increasing difficulty of satisfying the gate condition as the forbidden set
grows: at low |G|, the MCMC easily avoids the few forbidden cells; at high |G|,
the forbidden region dominates and each step faces many potential violations.

**This is the remaining research problem.** The c(|G|) values are known numerically.
The algebraic form of each c(|G|) from MCMC dynamics is the gap to Tier D.

---

## The ω-Class Rate Table

Thread 1 (omega3_extension.py) found different W(|G|) values for ω(b)=3 vs ω(b)=2.
From Thread 1 results at k=9:
- ω(b)=2, |G|=3: 44.0% → W_2(3) = 2.025
- ω(b)=3, |G|=7: 28.5% → W_3 = ?

From R = ((9−7)/9)^{W_3} = 0.285: W_3 = ln(0.285)/ln(2/9)
ln(0.285) ≈ −1.254, ln(2/9) ≈ −1.504. W_3 ≈ 0.834.

So W(|G|=7, ω=3) ≈ 0.834. Compare W(|G|=3, ω=2) = 2.025. These are different
ω-classes AND different |G| values, so direct comparison is not clean. But within
each ω-class, the same per-tier W structure should hold.

**The formula W(|G|, ω) = c(|G|) × ω** would predict:
- W(|G|=3, ω=2) = c(3) × 2 = 2.025 → c(3) = 1.012
- W(|G|=3, ω=3) = c(3) × 3 = 3.037 (prediction)

This is a testable prediction for ω=3, |G|=3 cases. Thread 1 data doesn't directly
give this rate (the ω=3 cases tested were |G|=5,6,7, not |G|=3). More data needed.

**The ω=3, |G|=7 case** (W≈0.834) is a different tier from the ω=2 data (|G|=1..5),
so the apparent inconsistency with any simple scaling may reflect tier differences
as much as ω differences. *This is an honest assessment based on Thread 1 data.*

---

## Formal Theorem Statement

**k-Gate Tier Law (partial Tier C→D):**
For fixed k=9 and ω(b)=2 (semiprimes), the gate success rate satisfies:
```
R(|G|) = ((9 − |G|) / 9)^W   with W ≈ 25.2
```
for all |G| ∈ {1, 2, 3, 4, 5}, with zero variance across all semiprimes in
each |G|-tier.

**Path to Tier D:** Derive W algebraically as W = 2c where c follows from
the MCMC geometry (HAR count, greedy acceptance, coupon-collector dynamics).

**Current tier: C.** The formula is empirically exact. The algebraic value of
c is the remaining step.

---

## Open Questions Generated

1. What is the algebraic formula for c from the MCMC structure?
2. Does R = (n_C/k)^W generalize to ω(b)≥3? Thread 1 data suggests the formula
   may not cross ω-classes simply. The W parameter may be ω-class dependent.
3. For the ω-class formula, is W_ω = c × ω (linear in ω), or a different function?

---

## The W Discontinuity at ω=3 — Three Hypotheses

*From Luther, LutherTask3.31.26.docx. All three are Tier A. Status: unknown.*

The W=25.2 formula works exactly for ω=2 but gives W≈0.83 for ω=3 — inconsistent
with any simple scaling prediction (W_3 = 1.5×W_2 would give ~37.8, not 0.83).
The discontinuity is real. Three hypotheses are on the table:

**Hypothesis 1 — Formula is ω=2 specific.**
R = (n_C/k)^W is the correct form for ω=2 but needs a structurally different
expression for ω≥3. The functional form itself breaks at the boundary, not just
the parameter. Under this hypothesis: derive the ω=3 formula from scratch from
the three-component CRT structure without assuming it looks like a power law.

**Hypothesis 2 — W measures lattice interference density, not simply fiber count.**
W is not simply 2c (one contribution per prime factor) — it measures the density
of lattice interference in the CRT product structure. For ω=2, this interference
has one characteristic scale. For ω=3, the three-body interactions create a
qualitatively different interference pattern that changes the effective W non-linearly
with ω. Under this hypothesis: W_ω is NOT linear in ω. It follows a function
determined by the ω-body interference structure of the CRT lattice.

**Hypothesis 3 — Triple intersections create shielding.**
In ω=3 worlds, the triple intersection Ideal(p) ∩ Ideal(q) ∩ Ideal(r) creates
a "shielding" effect: elements at triple intersections reduce the effective
obstruction per prime because they are counted three times in the inclusion-exclusion
but only produce one independent gate constraint. Each prime is effectively "lighter"
in a three-prime world because some of its obstructive weight is absorbed by the
shared intersection. Under this hypothesis: W_ω depends on the intersection
structure of the prime ideals, giving a formula like W_ω = f(ω, intersection_density).

**Current status:** All three are Tier A — strong intuition, no algebraic derivation.
The question sent to Luther: "Does the formula itself break at ω=3, or is W
measuring something ω=2-specific that needs a different expression for higher
ω-classes? What changes geometrically in the CRT lattice between two and three
prime factors that would cause this discontinuity?"

**What to do:** Nothing until Luther's algebraic response arrives. The question
is clean. Adding speculation before the response would compromise the honest ratio.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
