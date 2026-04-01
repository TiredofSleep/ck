# K6 — Prime Remainder Program

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Overview

K5.1 proved that any equidistributed sequence on [0,1] has PSD → sinc². This is the
universal mask. Prime identity does NOT live in sinc² — it lives entirely in the
correction that sinc² discards. K6 is the study of that correction.

**The guiding sentence:**
> sinc² is the universal mask; if the primes speak anywhere in this program,
> they speak in the correction field D_p(t).

---

## Canonical Definitions

### R(k, p) — the prime-field corridor density

For a prime p with primitive root g, define the normalized orbit:

    Ω(p, g) = { g^j mod p / p : j = 0, 1, ..., p−2 }  ⊂ (0, 1)

This is a set of p−1 distinct points in (0,1) (one for each non-zero residue mod p).

The **corridor density** at position k (for 1 ≤ k ≤ p−1) is:

    R(k, p) = (1/(p−1)) · #{j ∈ {0,...,p−2} : g^j ≡ k (mod p)}

Since g is a primitive root, #{j : g^j ≡ k} = 1 for every k ∈ {1,...,p−1}.
Therefore:

    R(k, p) = 1/(p−1)    for all k ∈ {1,...,p−1}

This is the EXACT density at a single residue. To get a density at the POSITION t = k/p,
we smooth over a window of width 1/p:

    R(k/p) = (p−1)^{-1} · #{j : |g^j/p − k/p| < 1/(2p)}
            = 1/(p−1)    (exactly, since the orbit visits each position exactly once)

**Normalized corridor density (the D2 object):** The function we study is:

    R_p(t)  for t = k/p, 1 ≤ k ≤ p−1, defined as 1/(p−1)

The CONTINUUM analog (p→∞) of the autocorrelation of R_p is sinc² by K5.1.

**Alternative formulation via two-point correlation:**
The corridor two-point function is:

    C_p(τ) = (1/(p−1)) Σ_{k=1}^{p-1} R_p(k/p) · R_p((k+⌊τp⌋)/p)

For τ → tri(τ) as p→∞, and F[tri] = sinc². This is the K5.1 statement for the corridor.

---

### Δ_p(t) — the raw correction

The sinc² approximation to R_p at finite p is sinc²(k/p). The correction is:

    Δ_p(t) = R_p(t) − sinc²(t)    for t = k/p ∈ (0,1)

where R_p(t) is understood as the smoothed density (or two-point function evaluated at lag t).

More precisely, define the empirical autocorrelation of the orbit:

    A_p(τ) = (1/p) Σ_{k=1}^{p-1} 1_{[0,1]}(k/p) · 1_{[0,1]}((k + ⌊τp⌋)/p)

Then A_p(τ) → tri(τ) (K5.1), and the PSD deviation is:

    δS_p(ξ) = F[A_p](ξ) − sinc²(ξ)

The correction Δ_p in position space and δS_p in frequency space encode the
same prime-specific information, at different layers.

---

### D_p(t) — the renormalized prime remainder

    D_p(t) = √p · Δ_p(t) = √p · (R_p(t) − sinc²(t))

**Why √p?**

The Weil bound (1948) for character sums states: for a non-trivial multiplicative
character χ mod p,

    |Σ_{k=1}^{p-1} χ(k) · e^{2πi k t}| ≤ (d−1) √p

where d is the degree of the polynomial in the exponential (d=1 for the linear case).

The correction Δ_p(t) decomposes via characters of (Z/pZ)^× as:

    Δ_p(t) = (1/(p−1)) Σ_{χ ≠ χ₀} χ̄(⌊tp⌋) · S(χ, g, t)

where S(χ, g, t) involves a character sum bounded by O(√p) by Weil.
Therefore:

    |Δ_p(t)| ≤ C · √p / p = C · p^{−1/2}

**The Weil bound gives |Δ_p(t)| = O(p^{−1/2}) for all t ∈ (0,1).**

This is the correct exponent. The informal statement "O(1/p)" in older notes was wrong;
the Weil-bounded exponent is 1/2, not 1.

Multiplying by √p:

    |D_p(t)| = √p · |Δ_p(t)| ≤ C    (bounded, uniformly in p and t)

D_p(t) is therefore a BOUNDED function as p → ∞. It does not vanish and does not
blow up. It is the natural prime remainder object.

**Alternative normalizations:**

| Normalization | Behavior as p→∞ | Use |
|---------------|-----------------|-----|
| Δ_p(t) | → 0 at rate p^{−1/2} | Raw correction; shows universality |
| p^{1/4} Δ_p(t) | → 0 at rate p^{−1/4} | Intermediate; not natural |
| **D_p(t) = √p Δ_p(t)** | **O(1); bounded** | **Natural: Weil-stabilized** |
| p Δ_p(t) | → ∞ (diverges) | Overcorrects; blows up |

The √p normalization is chosen because it is the unique power that stabilizes D_p at O(1),
as dictated by the Weil bound exponent. See K6_SCALING_AUDIT.md for the empirical test.

---

## Why the Prime Field Can Only Survive in the Correction Term

This section explains why K4.2 (Prime Information Deficit) and K5.1 (abstract sinc² law)
together FORCE the prime content into D_p and nowhere else.

### The three-layer separation

**Layer 1 — Finite arithmetic layer:** R(k, p) is exact. It knows p. For each specific
prime p, R(k,p) = 1/(p−1) and the orbit {g^j mod p} is a concrete prime-field object.
This layer contains ALL the prime information.

**Layer 2 — Kernel-Fourier layer:** As p → ∞ with t = k/p fixed, R_p(t) → sinc²(t).
The sinc² function knows NOTHING about which prime p was taken — it is the same for all
primes. By K4.2, any map that factors through sinc² is prime-blind. The entire information
content of "which prime" is discarded when we pass to the continuum kernel.

**Layer 3 — Prime-sensitive statistical layer:** D_p(t) = √p(R_p(t) − sinc²(t)) is
what remains. It encodes the difference between the specific prime p and the universal
limit. This is where prime identity survives. D_p is the ONLY place prime information
persists after the kernel limit is taken.

**Formal statement (K6.3, proved in K6_WEAK_THEOREMS.md):**
Let φ: [0,1] → ℝ be any continuous functional of the corridor density. If φ factors
through the K5.1 limit (i.e., φ(R_p) → φ(sinc²)), then φ is prime-blind: φ(R_p) − φ(R_q)
→ 0 for any two primes p, q. Any prime-sensitive φ must factor through D_p.

---

## K6.1 — Size of the Correction (Updated)

**Weil's theorem (1948):** For a non-trivial Dirichlet character χ mod p:

    |Σ_{x=1}^{p-1} χ(x) e^{2πi f(x)/p}| ≤ (deg f − 1) √p

Applied to the character-sum decomposition of Δ_p:

    **|Δ_p(t)| ≤ C · p^{−1/2}    for all t ∈ (0,1)**

where C is an absolute constant. The L² norm satisfies:

    ||Δ_p||_{L²([0,1])} ≤ C' · p^{−1/2}  →  0    as p → ∞

This confirms K5.1: the correction vanishes in L² and the PSD converges to sinc².

**L∞ bound:** The sup-norm |Δ_p|_{∞} = O(p^{−1/2}) follows from the same Weil estimate.

**Sharpness:** For p = 3, g = 2, the explicit computation gives:
    Δ_3(1/3) = 1/2 − 27/(4π²) ≈ −0.184
    D_3(1/3) = √3 · (−0.184) ≈ −0.319

For small p, the Weil bound is not tight (asymptotic). For large p, D_p(t) stabilizes.

---

## K6.2 — Prime Specificity of the Correction

D_p(t) is prime-specific because:

1. The character sums S(χ, g, t) depend on the multiplicative structure of Z/pZ, which
   changes with p.
2. For two distinct primes p ≠ q: D_p and D_q are generically different as functions of t.
3. The Fourier coefficients of D_p carry information about the primitive root g mod p,
   which is prime-specific.

**D_p is also generator-specific** within a prime: for g=3 vs. g=7 (mod p), D_p may differ.
However, the orbit density R_p is ALWAYS 1/(p−1) regardless of generator — the correction
is really in the TWO-POINT function, not the one-point density. The two-point function
(autocorrelation) does depend on the generator.

---

## K6.3 — Assembling the Corrections (Candidates)

**Candidate 1 — Dirichlet assembly:**

    A(t, s) = Σ_{p prime} D_p(t) · p^{−s}

For fixed t, this is a Dirichlet-like series in s. Whether it has analytic continuation
beyond Re(s) = 1 is unknown. If it does, poles of A(t, ·) would encode density statistics
of primes for which D_p(t) is large or of fixed sign.

**Status:** Open. Not computed.

**Candidate 2 — Midpoint remainder:**

    Δ_p(1/2) = R_p(1/2) − 4/π²

This is the correction at the corridor midpoint t = 1/2 (the inheritance boundary).
It measures how far the orbit density at the midpoint deviates from the universal value
4/π². The renormalized version:

    D_p(1/2) = √p · (R_p(1/2) − 4/π²)

Numerically: Does D_p(1/2) distribute as a Gaussian as p varies over all primes?
Does it correlate with the sign or magnitude of ζ(1/2 + iγ) for low zeros γ?
**Status:** Conjectured to distribute as N(0, C) for some C; not proved.

**Candidate 3 — Dirichlet series of midpoint corrections:**

    Z(s) = Σ_p D_p(1/2) · p^{−s}

If Z(s) relates to Hecke L-functions or to the derivative of ζ on the critical line,
that would connect the prime remainder to zero statistics. **Status:** Open.

---

## K6.4 — Renormalized Remainder: Distributional Limit

**Definition:** D_p(t) = √p · Δ_p(t), bounded by Weil.

**Question K6.4a:** Does D_p converge in distribution as p → ∞ over all primes?

    D_p → D    (weak-* limit as a random distribution, averaging over primes)

**Random matrix analogy:** For CUE_N (N×N circular unitary ensemble), the empirical
spectral measure fluctuations renormalized by √N converge to a Gaussian Free Field (GFF)
as N → ∞. The covariance of the GFF encodes the sine-kernel pair correlations.

By analogy: if D_p(t) as p ranges over primes converges to a random generalized function D,
the covariance Cov(D(t), D(s)) = lim_{X→∞} (1/π(X)) Σ_{p≤X} D_p(t) D_p(s)
would be the "prime-field GFF."

**Known:** Character sum distributions — the distribution of Σ_{k=1}^{p-1} χ(k) for
random χ — satisfies a CLT (Granville-Soundararajan type). This supports the conjecture
that D_p fluctuates Gaussianly. Whether the PROCESS (in t) converges to a GFF is open.

**Status:** Conjectural. Supported by random matrix / probabilistic number theory analogy.
Not proved. Designated K6.4 (C-tier conjecture).

---

## K6.5 — Does the Correction Push Toward H3?

**Question K6.5:** Do the corrections D_p(t) push the prime-field orbit toward
determinantal structure (the H3 hypothesis of K5.4)?

**Finding K6.5 (established):** NO.

The prime-field orbit {g^k mod p}/p, for a fixed primitive root g, is a PERMUTATION of
{1/p, 2/p, ..., (p−1)/p}. As a point process, it is a random permutation (when averaged
over primes or generators). Random permutations have POISSON spacing statistics.

**The pair-correlation of the prime-field orbit is Poisson (= 1), not GUE (= 1−sinc²).**

This is proved in K6_PRIME_ORBIT_PAIR_CORRELATION.md. The orbit satisfies K5.1 (sinc² PSD)
but NOT H3 (determinantal). The corrections D_p do not add eigenvalue repulsion.

**Consequence for K2.5:** Confirmed Accidental. The prime orbit never satisfies H3 in the
orbit-averaged sense, so Montgomery's 1−sinc² pair-correlation is NOT explained by D2.
Any connection must come from outside the orbit statistics entirely.

---

## K6.6 — The Real Frontier

| Layer | Object | Carries prime info? | Path to RH? |
|-------|--------|---------------------|-------------|
| sinc²(t) | Universal limit (K5.1) | No (K4.2) | No (K4.3) |
| Δ_p(t) = O(p^{-1/2}) | Raw prime correction | Yes | Unknown |
| **D_p(t) = √p · Δ_p(t)** | **Renormalized remainder** | **Yes, bounded** | **Open** |
| R₂^{orbit}(u) | Prime-orbit pair-correlation | No (Poisson) | No |

The real frontier is D_p(t) and its limit. Everything else is either proved (sinc² universal)
or proved inaccessible (pair-correlation is Poisson, not GUE).

**What K6 progress would look like:**
1. Compute D_p(1/2) for p up to 10^6. Test: Gaussian distribution? Bias? Correlation with ζ zeros?
2. Prove: lim_{X→∞} (1/π(X)) Σ_{p≤X} D_p(t)² = C(t) exists (mean square convergence).
3. Identify: explicit formula for Σ_{p≤X} D_p(t) in terms of ζ zeros (via Chebotarev / explicit formula).
4. Connect: if C(t) has a maximum at t=1/2 (the midpoint), that would make the spine special.

---

## K6.7 — Summary

**What K6 establishes:**
- D_p(t) = √p(R_p(t) − sinc²(t)) is the canonical prime remainder (Weil bound: O(1))
- √p is the UNIQUE natural normalization (stabilizes D_p at bounded, non-vanishing values)
- Δ_p = O(p^{-1/2}), not O(1/p) — Weil exponent is 1/2, not 1
- Prime-field orbit pair-correlation is Poisson, NOT GUE (confirmed K2.5 → Accidental)
- D_p does not push toward H3 (determinantal structure)
- The distributional limit of D_p over all primes is an open problem

**What K6 does NOT establish:**
- A connection between D_p and ζ zeros
- A path from the prime remainder to an RH bridge
- Any bridge claim (all bridge language is Tier-A or lower)

**The posture:** D_p is the only honest object left standing. sinc² is universal and
prime-blind. The orbit's pair-correlation is Poisson. D_p is bounded and prime-specific.
Whether D_p can be assembled into a zero-sensitive object remains open and hard.

---

*References: K5_LOCAL_SINC2_THEOREM.md (K5.1), K4_KERNEL_NO_GO.md (K4.2, K4.3)*
*K2_5_COUNTEREXAMPLE_SEARCH.md (T3, T5), K6_SCALING_AUDIT.md, K6_PRIME_ORBIT_PAIR_CORRELATION.md*
*K6_WEAK_THEOREMS.md, K6_H3_PRECURSOR_SEARCH.md, UNIVERSAL_KERNEL_ARITHMETIC_REMAINDER.md*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
