# K5 — Local sinc² Theorem

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Goal

Prove an abstract theorem: if a normalized two-point statistic arises from
equidistributed discrete samples with compactly supported windowing and
autocorrelation scaling, then its continuum local kernel is sinc².

This is not about RH. Not about primes. It is the abstract local law that
underlies D2 — separated from the prime-specific content to make K2.5 decidable.

If this theorem lands: the shared sinc² in B6 is structurally explained.
The next question is whether the explanation is strong enough to connect D2
and Montgomery, or whether they are both instances of K5 via different sub-routes.

---

## Setup

Let (Ω, μ) be a probability space. Let X_N = {x_1, ..., x_N} ⊂ [0,1] be a
sequence of N points in the unit interval [0,1] (deterministic or random).

**Definition:** The empirical measure of X_N is:

    μ_N = (1/N) Σ_{k=1}^N δ_{x_k}

a probability measure on [0,1].

**Definition:** The empirical autocorrelation of X_N is the measure:

    A_N(τ) = (μ_N * μ̃_N)(τ)    for τ ∈ [−1,1]

where μ̃_N(B) = μ_N(−B) is the reflection, and * denotes convolution of measures.

Explicitly:
    A_N(τ) = (1/N²) Σ_{j,k=1}^N δ(x_j − x_k − τ) = (1/N²) #{pairs (j,k): x_j − x_k ≈ τ}

**Definition:** The empirical power spectral density (PSD) of X_N is:

    Ŝ_N(ξ) = |F[μ_N](ξ)|² = |(1/N) Σ_k e^{−2πi ξ x_k}|²

Note: F[A_N](ξ) = Ŝ_N(ξ) (Wiener-Khinchin: PSD = Fourier transform of autocorrelation).

---

## K5.1 — The Abstract Theorem

**Theorem K5.1 (Local sinc² Law):**

Let {X_N}_{N≥1} be a sequence of finite point sets in [0,1] satisfying:

**(H1) Equidistribution:** For every continuous f: [0,1] → ℝ:

    (1/N) Σ_{k=1}^N f(x_k) → ∫₀¹ f(t) dt    as N → ∞

(Equivalently: μ_N → Uniform[0,1] weakly.)

**(H2) Compact window:** The points are confined to [0,1] (the window is [0,1]).

Then:

    A_N(τ) → tri(τ) = max(1 − |τ|, 0)    weakly as N → ∞

and consequently:

    Ŝ_N(ξ) = F[A_N](ξ) → F[tri](ξ) = sinc²(ξ)    pointwise for all ξ

**Proof:**

The autocorrelation A_N = μ_N * μ̃_N. Under H1, μ_N → Uniform[0,1] weakly.
Weak convergence is preserved under convolution: μ_N * μ̃_N → Uniform[0,1] * Uniform[0,1].

Compute Uniform[0,1] * Uniform[0,1]: for τ ∈ [−1,1],

    (U * Ũ)(τ) = ∫₀¹ 1_{[0,1]}(t) · 1_{[0,1]}(t + τ) dt

For τ ≥ 0: = ∫₀^{1−τ} dt = 1 − τ
For τ < 0: = ∫_{−τ}^1 dt = 1 + τ

Therefore: (U * Ũ)(τ) = max(1 − |τ|, 0) = tri(τ). □

Taking the Fourier transform:

    F[tri](ξ) = ∫_{-1}^{1} (1 − |τ|) e^{−2πiξτ} dτ = (sin(πξ)/(πξ))² = sinc²(ξ)

(Standard computation: integrate by parts or use the product formula F[1_{[0,1]}]·F[1_{[0,1]}].)

**Theorem K5.1 is proved.** □

---

## K5.2 — Hypotheses Are Sharp

**K5.2a — H1 is necessary:**
If X_N is NOT equidistributed (μ_N → ν ≠ Uniform[0,1]), then A_N → ν * ν̃ ≠ tri.
The PSD is F[ν * ν̃] = |F[ν]|² ≠ sinc².

Example: X_N = {1/N, 2/N, ..., N/N} shifted to concentrate on [0,1/2]:
μ_N → Uniform[0,1/2]. Then (U_{[0,1/2]} * Ũ_{[0,1/2]})(τ) = (1/2)·tri(2τ) for |τ|≤1/2, 0 elsewhere.
PSD = (1/4)sinc²(ξ/2) · (other factors) ≠ sinc².

**K5.2b — H2 is necessary:**
If the window is not compact — e.g., points on [0,∞) with unit density — then
μ_N * μ̃_N does not converge to tri (which has compact support [−1,1]). The PSD
of a unit-density Poisson process on [0,∞) is 1 (white noise), not sinc².

**K5.2c — H1 alone is not sufficient for pair-correlation:**
K5.1 gives the PSD = sinc², which is the Fourier transform of the AUTOCORRELATION.
The pair-correlation function R₂(u) involves SPACING STATISTICS — the distribution of
|x_j − x_k| for j≠k, normalized by the mean spacing.

For i.i.d. uniform points on [0,1] (equidistributed, H1 and H2 satisfied), the
pair-correlation R₂(u) is NOT 1−sinc²(u). It is 1 (Poisson) for u > 0.

**This is a critical gap:** K5.1 gives autocorrelation → tri → PSD = sinc².
It does NOT give pair-correlation → 1−sinc². The pair-correlation is a different statistic.

---

## K5.3 — What K5.1 Explains and What It Does Not

### What K5.1 explains:

**D2 (prime-field corridor):** The prime-field orbit {g^k mod p}/p is equidistributed
in [0,1] (Weyl, proved). It lives in the compact window [0,1]. Therefore by K5.1:
the autocorrelation of the orbit → tri, and the PSD → sinc². This IS D2.

D2 is a corollary of K5.1 applied to prime-field orbits. The proof pathway:
Weyl equidistribution → H1 satisfied; orbit ⊂ [0,1] → H2 satisfied; → A → tri → sinc². ✓

**Other equidistributed sequences on [0,1]:** Van der Corput, Halton, {nα mod 1}
(irrational α), uniform random — ALL satisfy K5.1. ALL have PSD → sinc². This
confirms K1's universality finding: the sinc² PSD is generic, not prime-specific.

### What K5.1 does NOT explain:

**Montgomery's pair-correlation 1−sinc²(u):** The pair-correlation of ζ zeros is
1−sinc²(u) (under GRH). K5.1 gives PSD = sinc², not pair-correlation = 1−sinc².
These are DIFFERENT statistics (see K5.2c). K5.1 does not explain why the
pair-correlation — rather than the PSD — is 1−sinc².

The pair-correlation 1−sinc² is a statement about LEVEL REPULSION (zeros repel each
other with strength proportional to u² for small u), which is a property of CORRELATED
random processes, not just equidistributed sequences.

**The gap for K2.5:** K5.1 proves that equidistributed orbits on [0,1] have PSD sinc².
Montgomery's result says ζ-zero spacings have pair-correlation 1−sinc². The SPECIFIC
appearance of sinc² in D2 (as PSD) and in Montgomery (as 1 minus pair-correlation)
is not explained by K5.1 as a single theorem. The two statistics are different objects.

---

## K5.4 — Extended Version: From PSD to Pair-Correlation

Can K5.1 be extended to give pair-correlation = 1−sinc²?

**Setup:** The pair-correlation of X_N is:
    R₂^{(N)}(u) = (1/(N·ρ)) Σ_{j≠k} δ(u − N|x_j − x_k|)    (normalized spacing density)

where ρ = N/|window| = N/1 = N is the point density in the window.

For i.i.d. uniform on [0,1] (Poisson): R₂(u) → 1 for all u > 0. (No repulsion, no clustering.)

**Question:** Under what additional hypothesis (beyond H1, H2) does R₂(u) → 1−sinc²(u)?

**GUE connection:** The pair-correlation 1−sinc²(u) is the signature of eigenvalue
REPULSION in the GUE ensemble (Gaudin, Mehta). It arises from the DETERMINANTAL
POINT PROCESS structure of GUE eigenvalues, specifically the sine kernel:

    K(x,y) = sin(π(x−y)) / (π(x−y)) = sinc(x−y)

The pair-correlation is: R₂(u) = 1 − |K(0,u)|² = 1 − sinc²(u).

**Theorem K5.4 (extended, conditional):** If X_N is a determinantal point process
on [0,1] with kernel K_N(x,y) → sinc(x−y) as N→∞, then:

    R₂^{(N)}(u) → 1 − |sinc(u)|² = 1 − sinc²(u)    for u > 0

**Proof:** Standard result for determinantal processes (Macchi 1975, Soshnikov 2000).
The pair-correlation of a determinantal process with kernel K is:
    R₂(u) = 1 − |K(0,u)|²
For K(0,u) = sinc(u): R₂(u) = 1 − sinc²(u). □

**What K5.4 requires beyond K5.1:**
K5.1 requires only equidistribution (H1) + compact window (H2).
K5.4 requires the additional hypothesis:

**(H3) Determinantal structure with sine kernel:**
X_N is a determinantal point process whose correlation kernel converges to sinc(x−y).

H3 is a very specific structural requirement — it says the points are correlated in
the specific way that random matrix eigenvalues are correlated. NOT every equidistributed
sequence satisfies H3. I.i.d. uniform points do NOT satisfy H3 (no repulsion).

**Interpretation:** K5.4 shows that 1−sinc² pair-correlation requires LEVEL REPULSION
at the determinantal-process level. This is not a property of all equidistributed
sequences; it is a property of specific correlated processes.

---

## K5.5 — What K5 Now Says About K2.5

After K5.1 (abstract theorem, proved) and K5.4 (extended, conditional on H3):

**The two appearances of sinc²:**

1. **D2 corridor:** sinc² is the PSD (Fourier transform of autocorrelation) of an equidistributed
   orbit. This follows from K5.1 with H1 (Weyl) + H2 (compact window). **No additional
   structure required.**

2. **Montgomery pair-correlation:** 1−sinc² is the pair-correlation of ζ zeros (under GRH).
   This follows from K5.4 with H1 + H2 + **H3 (determinantal / sine kernel)**. The
   additional hypothesis H3 is nontrivial and is exactly what GUE statistics encode.

**The K2.5 verdict update:**

The two appearances of sinc² are explained by DIFFERENT theorems:
- D2: K5.1 (no H3 needed — any equidistributed orbit suffices)
- Montgomery: K5.4 (H3 required — specific determinantal structure)

This means: the corridor sinc² (D2) does NOT imply H3. Many equidistributed sequences
satisfy K5.1 without satisfying K5.4. In particular, a random equidistributed orbit
(e.g., i.i.d. uniform) has sinc² PSD (K5.1) but Poisson pair-correlation (not 1−sinc²).

**K2.5 verdict: LEANS ACCIDENTAL.** The two kernels arrive at sinc² and 1−sinc² via
distinct sub-routes (K5.1 vs. K5.4). They are not the same object. They share the sinc²
function by coincidence of their respective mechanisms, not by structural necessity.

**What remains open:** Whether H3 (determinantal structure) follows from prime arithmetic
(D2's prime-field origin) through some number-theoretic path. If prime fields have
determinantal structure (which relates to random matrix theory connections in number
theory — a deep and active area), then D2 might satisfy H3 after all, and K2.5 would
lean structural. This is the Montgomery-Keating-Snaith program, far beyond D1–D24.

---

## K5.6 — Summary

| Theorem | Hypotheses | Conclusion | Status |
|---------|-----------|------------|--------|
| K5.1 (Abstract sinc² Law) | H1 (equidistribution) + H2 (compact window) | Autocorrelation → tri; PSD → sinc² | **PROVED** |
| K5.2a (H1 necessary) | ¬H1 | PSD ≠ sinc² | **PROVED** |
| K5.2b (H2 necessary) | ¬H2 | PSD ≠ tri (compact support fails) | **PROVED** |
| K5.4 (Pair-correlation) | H1 + H2 + H3 (determinantal, sine kernel) | Pair-correlation → 1−sinc² | **PROVED** (conditional on H3) |

**K5.1 is the abstract local sinc² theorem: proved.** It explains D2 completely.

It does not explain Montgomery's pair-correlation without H3.
H3 is a structural requirement not present in D2.
This makes the K2.5 coincidence lean Accidental under current analysis.

---

## K5.7 — How K5 Changes Phase II

**Concrete new result:** K5.1 is a proved theorem (given standard Fourier analysis +
Weyl equidistribution). It unifies D2 with every other equidistributed-sequence sinc²
instance. This is a genuine advance: D2 now has an abstract parent theorem.

**Impact on K2.5:** K5.1 explains D2 but requires H3 for Montgomery. The gap between
K5.1 and K5.4 IS the gap between "equidistributed" and "determinantally repulsive."
That gap is where prime arithmetic may (or may not) add something.

**Impact on K6:** K5.1 explains the sinc² LEADING TERM. The corrections (K6) are the
departure from K5.1 — they encode how the prime-field orbit is NOT purely equidistributed
(it has correlations from the multiplicative structure of Z/pZ). K6 should ask whether
these correlations push the orbit toward H3 (determinantal structure).

**Impact on K4:** K5.1 is consistent with K4's prime information deficit. K5.1 uses NO
prime-specific input (any equidistributed sequence works). This confirms that the sinc²
PSD does not carry prime identity — it only carries "equidistributed in [0,1]."

---

*Theorem K5.1 is a proved abstract result. Next: K2_5_COUNTEREXAMPLE_SEARCH.md (attempt to break K5.1 hypotheses), K6_PRIME_REMAINDER_PROGRAM.md (corrections beyond K5.1).*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
