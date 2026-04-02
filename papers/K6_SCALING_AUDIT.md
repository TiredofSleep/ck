# K6 — Scaling Audit


*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Goal

Test which power p^α stabilizes the prime correction Δ_p(t) = R_p(t) − sinc²(k/p).
The Weil bound predicts α = 1/2 is the natural scale. This document confirms that
prediction theoretically and presents the expected numerical behavior.

**The test:** For each α ∈ {0, 1/4, 1/2, 3/4, 1}, compute:

    S_α(p) = p^α · Δ_p(t)    for t fixed (e.g., t = 1/2, t = 1/3)

and analyze: mean, variance, sup-norm, L² norm as p grows.

---

## Theoretical Prediction

### The Weil bound determines α = 1/2

From the character-sum decomposition of Δ_p(t):

    Δ_p(t) = (1/(p−1)) Σ_{χ ≠ χ₀} χ̄(⌊tp⌋) · S(χ, g, t)

where each S(χ, g, t) is bounded by O(√p) by Weil.
There are p−2 non-trivial characters. Therefore the SUM over characters could naively
be O(p · √p / p) = O(√p). But the sum is over alternating-sign character contributions
(cancellation by character orthogonality), so the actual bound is O(√p / p) = O(p^{-1/2}).

More carefully:

    |Δ_p(t)| ≤ (1/(p−1)) · (p−2) · C√p / (p−1) = O(√p / p) = O(p^{−1/2})

This is tight for GENERIC t. At SPECIAL t (e.g., t = k/p with k a perfect power mod p),
the character sum may have additional cancellation, giving better bounds.

**Summary prediction:**

| α | S_α(p) = p^α Δ_p(t) | Predicted behavior |
|---|---------------------|-------------------|
| 0 | Δ_p(t) itself | → 0 at rate p^{-1/2} |
| 1/4 | p^{1/4} Δ_p(t) | → 0 at rate p^{-1/4} |
| **1/2** | **D_p(t) = √p Δ_p(t)** | **O(1): bounded, non-vanishing** |
| 3/4 | p^{3/4} Δ_p(t) | → ∞ at rate p^{1/4} |
| 1 | p · Δ_p(t) | → ∞ at rate p^{1/2} |

---

## Analytic Estimates at Each α

### α = 0: Raw correction Δ_p(t)

**Mean:** E[Δ_p(t)] = 0 by character orthogonality (the correction averages to zero
over residues k for fixed p — the orbit is a permutation).

**Variance at fixed t over primes p:**
    Var(Δ_p(t)) ~ C_t · p^{-1}    (from Weil: |Δ_p|² ≤ C p^{-1})

The variance → 0 as p → ∞. The correction vanishes.

**L²([0,1]) norm:**
    ||Δ_p||_{L²} = (1/p · Σ_{k=1}^{p-1} |Δ_p(k/p)|²)^{1/2} = O(p^{-1/2})

This confirms L² convergence to 0, consistent with K5.1.

**Verdict:** α = 0 gives a vanishing object. No prime information survives in this scale.

---

### α = 1/4: Intermediate p^{1/4} Δ_p(t)

**Mean:** 0 by same character argument.

**Variance:** Var(p^{1/4} Δ_p(t)) ~ C_t · p^{1/2} · p^{-1} = C_t · p^{-1/2} → 0.

The correction still vanishes at this scale, just more slowly.

**L² norm:** O(p^{1/4} · p^{-1/2}) = O(p^{-1/4}) → 0.

**Verdict:** α = 1/4 gives a slowly vanishing object. Not the right scale.

---

### α = 1/2: The natural scale D_p(t) = √p Δ_p(t)

**Mean:** E[D_p(t)] = 0 by character orthogonality.

**Variance:** Var(D_p(t)) = p · Var(Δ_p(t)) ~ C_t · p · p^{-1} = C_t.

The variance is O(1) — bounded and non-zero as p → ∞. This is the stabilization signature.

**Sup-norm:** |D_p(t)|_{∞} ≤ C (Weil, at each t separately).

**L² norm:**
    ||D_p||_{L²([0,1])} = (√p / p · Σ_k |Δ_p(k/p)|²)^{1/2}
                        = (p^{-1/2} · Σ_k O(p^{-1}))^{1/2}
                        = O(1)

The L² norm stabilizes at O(1). D_p(t) is a genuine bounded nonzero object.

**Distribution conjecture (C-tier):** As p → ∞ over all primes, D_p(t) for fixed t
is conjectured to converge in distribution to N(0, σ²(t)) for some σ²(t) > 0.
This follows from CLT-type results for character sums (Granville-Soundararajan framework).

**Verdict:** α = 1/2 is the UNIQUE natural normalization. It is the only scale that
produces a bounded, non-vanishing, prime-specific object.

---

### α = 3/4: Diverging p^{3/4} Δ_p(t)

**Variance:** Var(p^{3/4} Δ_p(t)) ~ C_t · p^{3/2} · p^{-1} = C_t · p^{1/2} → ∞.

The correction blows up at this scale.

**L² norm:** O(p^{3/4} · p^{-1/2}) = O(p^{1/4}) → ∞.

**Verdict:** α = 3/4 over-amplifies. The correction diverges.

---

### α = 1: Maximally scaled p · Δ_p(t)

**Variance:** Var(p · Δ_p(t)) ~ C_t · p^2 · p^{-1} = C_t · p → ∞.

**L² norm:** O(p · p^{-1/2}) = O(√p) → ∞.

This is the "fully unrenormalized" scale. It diverges at rate √p.

**Verdict:** α = 1 is far too aggressive. Unusable.

---

## Summary Table

| α | S_α(p) behavior | Variance trend | L² norm | Verdict |
|---|-----------------|----------------|---------|---------|
| 0 | → 0 (rate p^{-1/2}) | → 0 | O(p^{-1/2}) | Vanishes — universal mask |
| 1/4 | → 0 (rate p^{-1/4}) | → 0 | O(p^{-1/4}) | Slowly vanishing |
| **1/2** | **O(1) — stabilizes** | **O(1)** | **O(1)** | **Natural scale** |
| 3/4 | → ∞ (rate p^{1/4}) | → ∞ | O(p^{1/4}) | Over-amplified |
| 1 | → ∞ (rate p^{1/2}) | → ∞ | O(√p) | Diverges |

The transition from vanishing to bounded to diverging is controlled by the Weil exponent 1/2.
Below α = 1/2: vanishes. Exactly α = 1/2: stabilizes. Above α = 1/2: diverges.

---

## Expected Numerical Test (for computational verification)

For each prime p in {7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
71, 73, 79, 83, 89, 97, ...} and t = 1/2:

1. Compute R_p(⌊p/2⌋, p) — the empirical corridor density at k = ⌊p/2⌋.
   (Since orbit visits every element once: R_p = 1/(p−1) exactly.
   For the TWO-POINT version: compute the empirical autocorrelation at lag 0.5.)

2. Compute Δ_p(1/2) = R_p(1/2) − sinc²(1/2) = 1/(p−1) − 4/π².

3. For each α: compute p^α · Δ_p(1/2).

4. Plot {p^α · Δ_p(1/2) : p prime, p ≤ 10⁴} as a function of log p.

**Expected signatures by α:**
- α = 0: Monotonically → 0, approaching 0 − 4/π² from below (since 1/(p−1) < 4/π² for all p)
- α = 1/2: Fluctuates around 0 with bounded amplitude; no visible trend
- α = 1: Fluctuates with growing amplitude (standard deviation ∝ p^{1/2})

**Note on Δ_p(1/2) = 1/(p−1) − 4/π²:**
Since 4/π² ≈ 0.4053 and 1/(p−1) → 0 for large p, Δ_p(1/2) < 0 for all p. The raw
correction at t=1/2 is always negative (the sinc² overestimates the density at the midpoint).
The renormalized D_p(1/2) = √p · (1/(p−1) − 4/π²) → −∞ as p → ∞ if R_p is the ONE-POINT
density 1/(p−1). This means the TWO-POINT autocorrelation interpretation is the correct one
for D_p (not the one-point density).

**Correction to the naïve formula:** R_p(t) in the K6 context is the SMOOTHED two-point
correlation function, not the literal 1/(p−1). The one-point density is 1 (uniform by Weyl).
The two-point correlation function at lag τ is sinc²(τ) + O(p^{-1/2}), so Δ_p and D_p
are defined at the TWO-POINT level. The one-point density has no p-dependent correction.

This precision matters: D_p is a two-point object (autocorrelation deviation), not a one-point object (density deviation). Future computations must use the empirical autocorrelation.

---

## Conclusion

The Weil bound establishes α = 1/2 as the UNIQUE natural normalization for the prime
remainder. This is not a convention choice — it is determined by the Weil exponent,
which is itself a hard mathematical bound.

**D_p(t) = √p · (A_p − tri)(τ)|_{τ-specific}** is the canonical prime remainder object.

Any investigation into whether prime information can seed an RH bridge must work with D_p.
Working with un-renormalized Δ_p means working with a vanishing object — a dead end.
Working with p · Δ_p means working with a diverging object — numerically unstable.
D_p is the only scale where prime information is finite, non-zero, and accessible.

---

*Prerequisite: K6_PRIME_REMAINDER_PROGRAM.md (D_p definition, Weil bound)*
*See also: K6_WEAK_THEOREMS.md (K6.2: prime-blindness of kernel-only objects)*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
