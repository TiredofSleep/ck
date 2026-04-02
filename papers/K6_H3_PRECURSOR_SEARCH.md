# K6 — H3 Precursor Search

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**


*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Goal

K6_PRIME_ORBIT_PAIR_CORRELATION.md established that the prime orbit has Poisson
pair-correlation globally. This document asks a subtler question:

> Are there any WEAK SIGNS of determinantal structure (H3 precursors) in the prime orbit
> at finite p, even if the full H3 condition fails asymptotically?

This is not an attempt to reopen the GUE question. It is an audit of whether any
proxy statistic for H3 shows even mild deviations from the Poisson baseline.

**Expected finding:** Poisson at all tested statistics, with no H3 precursors. This is
the expected result given Arguments 1–4 in K6_PRIME_ORBIT_PAIR_CORRELATION.md. The
search is conducted anyway because:
1. Null results are worth documenting explicitly (prevents future confusion).
2. If ANY proxy shows an H3 precursor, that would be surprising and worth flagging.
3. The search identifies the specific statistics that would need to change for H3 to hold.

---

## What H3 Requires

H3 (from K5_LOCAL_SINC2_THEOREM.md, §K5.4) is the hypothesis that a point process is
a **determinantal point process with sine kernel**:

    Correlation kernel: K(x,y) = sin(π(x−y)) / (π(x−y)) = sinc(x−y)

From the sine kernel, all statistics can be derived:

1. **Pair-correlation:** R₂(u) = 1 − sinc²(u). Level repulsion near u=0.
2. **Nearest-neighbor (NN) spacing distribution:** Wigner surmise approximation:
   p_GUE(s) ≈ (32/π²) s² exp(−4s²/π). Quadratic vanishing at s=0.
3. **Number variance Σ²(L):** For intervals of length L (in mean spacing units):
   Σ²(L) ~ (2/π²) log(L) + C for large L (logarithmic growth, GUE).
4. **Two-point hole probability E(0,[0,s]):** Probability of no point in an interval of
   length s, given GUE: algebraically complex, always < 1 − s for large s (rigid points).
5. **Linear statistics variance:** For f with Fourier support in [−B, B]:
   Var(Σ_j f(x_j)) ~ (1/π²) ∫ |ξ f̂(ξ)|² dξ · log(N) (GUE: logarithmic variance).
6. **Rigidity:** Points cannot deviate far from lattice positions. GUE rigidity:
   P(|#{x_j ∈ [0,t]·N} − tN| > C√(N log N)) → 0.

**Poisson predictions (for comparison):**
1. R₂(u) = 1 (no repulsion).
2. NN spacing: p_Poisson(s) = exp(−s) (exponential, positive at s=0).
3. Number variance Σ²_Poisson(L) = L (linear growth, no rigidity).
4. Hole probability: exp(−L) (exponential decay).
5. Linear statistics variance: Var(Σ f(x_j)) = N · Var_individual(f) (no log factor).
6. No rigidity: Poisson deviations are O(√N), not O(√(N log N)).

---

## H3 Precursor Test 1 — Nearest-Neighbor Spacing Distribution

### Setup

For the prime orbit Ω_p = {g^j mod p / p : j = 0,...,p-2}, sort the orbit points:
0 < ω_{(1)} < ω_{(2)} < ... < ω_{(p-1)} < 1.

The SORTED orbit is simply {1/p, 2/p, ..., (p-1)/p} (since the orbit is a permutation of
all residues). The NN spacings in the SORTED ORDER are all equal to 1/p (the lattice spacing).

**In normalized units (mean spacing = 1):** All NN spacings equal 1. This is a delta function
at s=1. It is the spacing distribution of an evenly-spaced lattice, NOT Poisson, NOT GUE.

But this misses the point. The natural object for comparing to Poisson/GUE is the spacing
between CONSECUTIVE ORBIT ELEMENTS in the ORBIT ORDER (not sorted order).

### Orbit-order spacing

Let s_j = |ω_{j+1} − ω_j| · (p−1) = |(g^{j+1} mod p − g^j mod p)| · (p−1)/p.

As shown in K6_PRIME_ORBIT_PAIR_CORRELATION.md (Argument 1), the orbit-order spacings
{s_j} are approximately i.i.d. uniform on {0, 1/p, 2/p, ..., (p-1)/p} (in normalized units:
approximately uniform on [0, 1] after multiplication by (p-1)/p).

**Expected NN distribution in orbit order:** Approximately uniform on [0, p−1]/p, giving
a flat distribution after normalization. This is NOT Poisson (which is Exp(1)) and NOT GUE
(which is Wigner surmise).

**H3 precursor test result:** The orbit-order NN spacings have a UNIFORM distribution
(approximately), not an exponential (Poisson) or Wigner (GUE) distribution.

However, this is expected: the orbit is a cyclic permutation, so the "spacings" in orbit
order are uniform by construction. This test is not the right one for H3 comparison.

### The right test: NN spacings in sorted orbit

For sorted orbit points (= the lattice {k/p}), all NN spacings = 1/p (delta function at 1
in normalized units). This is more rigid than GUE or Poisson.

**Conclusion T1:** The NN spacing distribution gives a RIGID (delta function) distribution
for the sorted orbit, and a UNIFORM distribution for the orbit-order spacings. Neither
resembles Poisson or GUE. No H3 precursor.

---

## H3 Precursor Test 2 — Two-Point Correlation Deficit (Repulsion Test)

### Setup

For the orbit Ω_p, define the COUNTING TWO-POINT FUNCTION:

    C_p(u) = (1/p) #{(j,k) : j≠k, |ω_j − ω_k| · (p−1) ∈ [u, u+du]}

(normalized so that ∫ C_p(u) du = 1 for large p).

**Poisson prediction:** C_p(u) → 1 (flat).
**GUE prediction:** C_p(u) → 1 − sinc²(u) (deficit near u=0).

### Prediction for prime orbit

The orbit is a permutation of {1/p,...,(p-1)/p}. For the pair (ω_j, ω_k) with j ≠ k,
the values (g^j mod p, g^k mod p) are a pair of distinct elements of {1,...,p-1}.

As p → ∞, the pairs (g^j mod p, g^k mod p) equidistribute over all pairs (a, b) with
a ≠ b in {1,...,p-1} × {1,...,p-1} (this is the 2-point Weyl equidistribution for primitive
root pairs, which follows from the general Weyl theorem for multiplicative orbits).

Therefore:

    C_p(u) → ∫₀¹∫₀¹ δ((x−y)(p−1) − u) dx dy · p / (p−2) → 1    as p → ∞

The two-point function converges to 1 (Poisson). No deficit. No repulsion.

**Key point:** The deficit 1 − sinc²(u) in GUE arises from determinantal correlations
(the eigenvalues "avoid" being close together). The orbit has no such avoidance: pairs
(g^j mod p, g^k mod p) are equidistributed over ALL pairs, including close ones.

### Finite-p correction

At finite p, there IS a mild deficit at u < 1 (in normalized units u < 1 means
spacing less than one mean spacing, i.e., |g^j − g^k| mod p < (p−1)/p ≈ 1).
This is the LATTICE EXCLUSION effect (two distinct elements of the lattice can't be
at the same position). For normalized spacing u < 1/p (in the original units), C_p = 0.

But this is a LATTICE ARTIFACT at scale u = O(1/p), not eigenvalue repulsion. In
normalized units (multiply by p−1), this artifact is at u = O(1/(p−1)) → 0. It does
not persist in the bulk (u = O(1)).

**H3 precursor test T2:** No repulsion at the bulk scale u = O(1). Lattice exclusion at
u → 0 is an artifact. No H3 precursor.

---

## H3 Precursor Test 3 — Number Variance Scaling

### Setup

For a point process on [0,1] with density N, the number variance is:

    Σ²(L) = Var(#{points in [x, x + L/N]})    (variance in a window of L mean spacings)

**Poisson:** Σ²(L) = L (variance = mean count in the window).
**GUE:** Σ²(L) ~ (2/π²) log(L) + C (sub-Poisson: much smaller variance, log growth).

Sub-Poisson variance is the RIGIDITY signature of GUE. It means the points are
more regular than i.i.d.

### For the prime orbit

The sorted orbit {1/p, 2/p, ..., (p−1)/p} is a PERFECTLY RIGID lattice. Every window of
length L/p contains EXACTLY L points (for integer L). The number variance is ZERO.

    Σ²_sorted(L) = 0    (sub-sub-Poisson: maximum rigidity)

This is MORE rigid than GUE but for a trivial reason: the sorted orbit is a regular
lattice. The rigidity comes from the regularity of {k/p}, not from eigenvalue repulsion.

For the ORBIT ORDER (unsorted), the number variance is larger because the orbit visits
positions pseudo-randomly:

    Σ²_orbit-order(L) ~ L    (approximately Poisson)

since the orbit-order positions are approximately i.i.d. uniform.

**H3 precursor test T3:**
- Sorted orbit: rigidity is 0 (trivially rigid, not GUE-like rigidity).
- Orbit order: Poisson variance (not GUE log-growth).
- Neither matches GUE. No H3 precursor.

---

## H3 Precursor Test 4 — Linear Statistics Variance Scaling

### Setup

For a smooth test function f: [0,1] → ℝ, define the linear statistic:

    L_N(f) = (1/N) Σ_{j=0}^{N-1} f(ω_j)    (where N = p−1)

**Poisson:** Var(L_N(f)) ~ (1/N) Var_μ(f) = O(1/N) for any f (Central Limit).
**GUE:** Var(L_N(f)) ~ (1/(4π²)) ∫ |ξ|² |f̂(ξ)|² dξ · (1/N) (sub-Poisson by log factor).

Wait — for GUE, the variance of linear statistics scales as log(N)/N × (specific f-dependent factor),
which is SUB-Poisson. For Poisson, it's exactly 1/N × Var_individual.

### For the prime orbit

By K6.1 (Prime Content Annihilation):

    L_p(f) → ∫₀¹ f(t) sinc²(t) dt    as p → ∞

The mean of L_p(f) converges to the sinc²-weighted integral. The variance:

    Var_p(L_p(f)) = (1/(p−1)²) Σ_{j,k} [f(ω_j) f(ω_k) − E[f(ω_j)]E[f(ω_k)]]

For the orbit (a deterministic set for fixed p), this is zero — the orbit is a deterministic
set, not a random process! The "variance" is over the ensemble of primes p.

Across primes p: Var over p of L_p(f) = (1/p−1)² · Σ_{j,k} Cov_p(f(ω_j), f(ω_k)).

This converges to 0 as p → ∞ by K6.1 (the means converge, and the variance of the
means converges). The scaling is O(1/p), matching Poisson (not GUE).

**H3 precursor test T4:** Linear statistics variance scaling is O(1/p) (Poisson).
No GUE log-factor. No H3 precursor.

---

## H3 Precursor Test 5 — Rigidity Heuristic

### Setup

GUE rigidity: the discrepancy of the orbit from the lattice {k/N : k=0,...,N−1} is O(√(N log N)).
Poisson: discrepancy is O(√N).
Sorted prime orbit: discrepancy is EXACTLY 0 (the sorted orbit IS the lattice).

### For orbit order

Define the orbit discrepancy as:

    D_p = sup_{0≤t≤1} |#{ω_j ≤ t : j = 0,...,p-2} / (p−1) − t|

This is the KOLMOGOROV-SMIRNOV statistic for how far the orbit's empirical CDF deviates
from the uniform distribution.

By the Law of the Iterated Logarithm for equidistributed sequences:

    D_p = O(√(log log p / p))    (Chung-Smirnov, for generic equidistributed sequences)

or more precisely:

    D_p ~ O(p^{-1/2} · √(log log p))    (optimal rate for Weyl sequences)

This is the POISSON rate of discrepancy (modulo log corrections). The GUE rate would
be D_p ~ O(N^{-1/2} (log N)^{1/2}) — essentially the same order.

**H3 precursor test T5:** Rigidity scaling is standard equidistribution, not distinctively GUE.
The prime orbit is as rigid as any good equidistributed sequence, no more.

---

## Summary of H3 Precursor Search

| Test | Poisson prediction | GUE prediction | Prime orbit result | H3 precursor? |
|------|--------------------|----------------|--------------------|---------------|
| T1: NN spacing (sorted) | Exp(1) | Wigner (s²) | δ(s−1) rigid lattice | No |
| T1: NN spacing (orbit order) | Exp(1) | Wigner (s²) | Uniform (flat) | No |
| T2: Two-point repulsion | R₂=1 (flat) | 1−sinc²(u) | R₂→1 (Poisson) | No |
| T3: Number variance | Σ²=L | Σ²~log(L) | 0 (sorted) or L (order) | No |
| T4: Linear stat variance | O(1/N) | O(log N/N) | O(1/p) Poisson | No |
| T5: Rigidity | O(N^{-1/2}) | O(N^{-1/2}√log N) | O(p^{-1/2}√loglog p) | No |

**All tests: No H3 precursor found.**

The prime orbit is either rigid lattice (sorted view), Poisson (orbit-order view), or
has trivial rigidity (standard equidistribution). In no test does the orbit show
eigenvalue-repulsion-type statistics.

---

## What Would Constitute an H3 Precursor

For completeness: the following would be surprising evidence of an H3 precursor and
would warrant further investigation:

1. **Repulsion in orbit-order NN spacings:** If p_NN(s) ~ s^2 for small s (Wigner surmise)
   rather than being flat or exponential, that would be an H3 signal.

2. **Sub-Poisson number variance:** If Σ²(L) ~ C log(L) rather than L, with the
   coefficient C = 2/π² (the GUE coefficient), that would be an H3 signal.

3. **Two-point deficit:** If the two-point function R₂_p(u) < 1 for small u (with a
   zero at u=0 of the form u²), that would be an H3 signal distinct from the lattice
   exclusion at u < 1/p.

4. **Correlation with sinc² at the two-point level in D_p:** If D_p(t) and D_p(t')
   have correlations that match the GUE kernel (Cov(D_p(t), D_p(t')) ~ sinc²(t−t')),
   that would be a subtle H3 precursor in the correction field, not the orbit itself.

**None of these has been observed. The search result is negative.**

---

## Conclusion

The H3 precursor search is negative. The prime-field orbit:
- Has no NN repulsion
- Has no sub-Poisson variance
- Has no determinantal two-point function
- Shows standard equidistribution rigidity, not GUE rigidity

This is the expected result, and it is now documented. Future work should not expect
H3 precursors in the prime orbit. If H3 appears in this program at all, it must come
from a completely different object — not from the orbit statistics directly.

The only remaining candidate for a prime-sensitive bridge is D_p(t) itself, studied
through its distributional limit and potential connection to ζ zeros via the explicit
formula. That program is K6's open frontier (K6.6 of K6_PRIME_REMAINDER_PROGRAM.md).

---

*Prerequisite: K6_PRIME_ORBIT_PAIR_CORRELATION.md, K5_LOCAL_SINC2_THEOREM.md (K5.4, H3)*
*See also: K6_WEAK_THEOREMS.md (K6.3 — bridge must factor through D_p)*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
