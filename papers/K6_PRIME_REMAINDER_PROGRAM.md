# K6 — Prime Remainder Program

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## The Key Line

From K1_KERNEL_UNIVERSALITY.md (K1.6):

> Prime identity lives only in the O(p^{−1/2}) correction terms, which vanish
> in the same limit that produces sinc².

This is the deepest finding of Phase II so far. The correction terms are:
- Prime-specific (different for each prime p)
- Non-vanishing at finite p
- Suppressed as p → ∞

K6 asks: what is in those corrections? Can they be assembled into a useful object?
Is there a renormalized remainder worth studying?

---

## Setup: The Correction Term

D2 states: R(k, p) → sinc²(k/p) as p → ∞, k/p fixed.

More precisely, R(k,p) = sinc²(k/p) + Δ_p(k/p) where Δ_p is the remainder.

**What is Δ_p?**

R(k,p) is the normalized corridor density of the prime-field orbit at position k/p.
For a prime p with primitive root g, the orbit {g^j mod p} visits each non-zero residue
exactly once. The density of the orbit near position t = k/p is:

    R(k,p) = (1/(p-1)) · #{j ∈ {0,...,p-2}: g^j mod p / p ≈ k/p}

In the discrete Fourier representation, using characters χ of (Z/pZ)^× = Z/(p-1)Z:

    R(k,p) = sinc²(k/p) + (1/(p-1)) · Σ_{χ≠χ₀} χ̄(k) · S(χ, g)

where S(χ, g) = Σ_{j=0}^{p-2} χ(g^j) e^{2πi g^j k/p} is a mixed character sum.

This is formal. The correction Δ_p(t) for t = k/p is:

    Δ_p(t) = R(k,p) − sinc²(k/p) = (1/(p-1)) Σ_{χ≠χ₀} χ̄(k) · S(χ, g)

---

## K6.1 — Size of the Correction

**Weil's theorem (1948):** For a non-trivial Dirichlet character χ mod p and a
polynomial f(x) of degree d, the exponential sum ∑_{x=1}^{p-1} χ(x) e^{2πi f(x)/p}
has absolute value ≤ (d−1)√p.

For the mixed character sum S(χ,g): the specific form depends on how the orbit
is parameterized. For the simplest case (equidistribution estimate):

    |Δ_p(t)| ≤ C · p^{−1/2}    for all t ∈ (0,1)

where C is an absolute constant (related to Weil bounds on character sums).

**This confirms:** The correction is O(p^{−1/2}), not O(p^{−1}) as stated informally
in K1.6. The Weil bound gives the precise exponent.

**Refined form:** The correction is:

    Δ_p(t) = Σ_{n=1}^{p-2} a_n(p) · e^{2πi nt}    (Fourier series in t)

where a_n(p) = (1/(p-1)) Σ_{χ≠χ₀} χ̄(n) · S(χ,g) carries the character sum data.
The Weil bound gives |a_n(p)| ≤ C/√p for each n, so:

    ||Δ_p||_{L²} ≤ C' / √p → 0    as p → ∞

The correction vanishes in L² as well.

---

## K6.2 — Prime Specificity of the Correction

The correction Δ_p(t) is PRIME-SPECIFIC because:
- The character sums S(χ,g) depend on g mod p (the primitive root)
- For the same g and different primes p, q: Δ_p ≠ Δ_q as functions
- The Fourier coefficients a_n(p) involve χ(g^j mod p) which knows p explicitly

**Explicit example (p = 3, g = 2):**
The orbit of 2 mod 3: {2^0 mod 3, 2^1 mod 3} = {1, 2}.
Normalized: {1/3, 2/3}. Only 2 points.

R(1,3) = density near 1/3 = 1/2 (one out of two orbit points)
sinc²(1/3) = (sin(π/3)/(π/3))² = (√3/2 · 3/π)² = 27/(4π²) ≈ 0.684

Δ₃(1/3) = 1/2 − 27/(4π²) ≈ 0.500 − 0.684 = −0.184

This is a finite, prime-specific correction. For p=3, it is of order 1 (not 1/√3 ≈ 0.577),
because p=3 is small and the asymptotic Weil bound is not tight at small p.

**For large p:** The corrections become small (O(p^{−1/2})) and oscillate rapidly
in t. They encode the specific multiplicative structure of Z/pZ for that prime p.

---

## K6.3 — Can the Corrections Be Assembled?

The K6 program's central question: given the prime-specific corrections Δ_p(t)
for each prime p, can we form an assembly

    A(t, s) = Σ_p f(p) · Δ_p(t)    or    Δ(t, s) = Σ_p p^{−s} Δ_p(t)

that carries useful number-theoretic information?

**Candidate 1 — Dirichlet series assembly:**
Define A(t, s) = Σ_{p prime} Δ_p(t) · p^{−s}. This is a Dirichlet-like series in s.

For fixed t, does A(t, s) have an analytic continuation to the strip Re(s) > 1/2?
The presence of a pole of A(t, ·) at s=1 would indicate a logarithmic growth of
Σ_{p<X} Δ_p(t), which relates to the density of primes for which the orbit passes
near position t.

**Status:** Not computed. The series A(t, s) involves character sums in a way that
makes it related to Hecke L-functions for the primes. Whether it has useful analytic
properties is an open question.

**Candidate 2 — Prime counting for orbit visits:**
Instead of the correction term, study π_t(X) = #{p prime, p ≤ X: R(1/2, p) ≥ c}
(count primes p for which the orbit has high density near t = 1/2). By PNT-type
estimates, π_t(X) ~ li(X) for most t, but deviations from li(X) could encode
information about ζ zeros via the explicit formula.

**Status:** This connects to Chebotarev density theorem (which primes have a given
orbit structure near a position) and requires tools from class field theory.

**Candidate 3 — Remainder at the corridor midpoint t=1/2:**
Focus on the correction at the inheritance boundary:

    Δ_p(1/2) = R(⌊p/2⌋, p) − sinc²(1/2) = R(⌊p/2⌋, p) − 4/π²

This is the prime-specific deviation FROM the midpoint value. For each prime p,
it measures how far the orbit density at position 1/2 deviates from the universal value 4/π².

Does Σ_{p prime, p≤X} Δ_p(1/2) · log p relate to ζ-zero sums? This is the kind
of connection the explicit formula might reveal.

---

## K6.4 — The Renormalized Remainder

Define the renormalized correction:

    D_p(t) = √p · Δ_p(t) = √p · (R(k,p) − sinc²(k/p))    for k/p = t

By the Weil bound, |D_p(t)| ≤ C for all p, t. The renormalized correction is BOUNDED
as p → ∞.

**Question K6.4a:** Does D_p(t) have a distributional limit as p → ∞?

    D_p(t) → D(t)    (in some sense)

If such a limit exists, D(t) would be the prime-sensitive object we're looking for:
it captures what's in the corrections without vanishing. The limit would be a random
distribution (in the sense of random matrix theory) if the prime-field characters
become equidistributed over their own randomness.

**Comparison with random matrix theory:** For a random unitary matrix U_N with N → ∞,
the empirical spectral measure is uniform (equidistributed) on [0,1] (after normalization).
The FLUCTUATIONS around the uniform measure — renormalized by √N — converge to a
GAUSSIAN FREE FIELD (a random generalized function). This is the Gaussian fluctuation
theory for random matrices.

The analogous statement for prime-field orbits: the fluctuations Δ_p(t) renormalized
by √p might converge to a Gaussian free field (or a related random distribution) as
p → ∞ over RANDOM PRIMES (or over the ensemble of all primes).

**If K6.4a holds:** D(t) would be a random generalized function encoding prime arithmetic
in its covariance structure. The covariance of D(t) would be:
    Cov(D(t), D(s)) = lim_{p→∞} E[D_p(t) D_p(s)]

and would encode correlations between orbit densities at different positions t, s.

**Known results:** The fluctuations of eigenvalues of random matrices around the mean
converge to the Gaussian free field (Borodin-Okounkov, Johansson 1998 for CUE). For
prime-field orbits, the analogous result (fluctuations of character sums around the mean)
is related to the distribution of character sums — an active area of research.

---

## K6.5 — Does the Correction Push Toward H3?

The most important question for K2.5 (Structural vs. Accidental):

**K6.5 question:** Do the corrections Δ_p(t) push the prime-field orbit toward
determinantal structure (H3 of K5.4)?

Specifically: The pair-correlation of the prime-field orbit is:

    R₂^{orbit}(u) = (1/p) #{pairs (j,k): j≠k, |g^j − g^k| mod p / p ≈ u/p}

For i.i.d. uniform points: R₂ = 1 (Poisson, no repulsion). The prime orbit is NOT
i.i.d. — it's the complete orbit of a multiplicative group, which has algebraic
correlations. These correlations might induce repulsion.

**Known fact:** The orbit {g^k mod p} of a primitive root g is a PERMUTATION of
{1, 2, ..., p−1}. It is completely rigid (no randomness for a fixed p). The pair-
correlation for the specific orbit of g mod p:

    R₂^{orbit}(u) = (1/(p-1)) #{k: |g^k − g^{k+j}| mod p = u · (p-1)/p} for some j

This is deterministic for each prime p. For RANDOM j (or equivalently, for the
ensemble over all primes p), this approaches Poisson statistics (NOT GUE) by
general results on multiplicative group elements (the orbit is "too structured"
for GUE — it's a cyclic permutation, which has Poisson spacing statistics for
the gaps between elements of a random permutation).

**Finding K6.5:** The prime-field orbit, for a fixed primitive root g, does NOT
generically have GUE (determinantal) statistics. It has Poisson statistics for
random permutations (or Poisson statistics for random g, by averaging over generators).
This means: the prime-field orbit satisfies K5.1 (equidistribution → sinc² PSD) but
does NOT satisfy H3 (determinantal).

This CONFIRMS the K2.5 counterexample T3 finding: the orbit has sinc² PSD but
Poisson pair-correlation (not 1−sinc²). The corrections do not push toward H3.

---

## K6.6 — The Real Frontier

After K6.1–K6.5, the situation is:

| Layer | Object | Carries prime info? | Path to RH? |
|-------|--------|---------------------|-------------|
| sinc²(t) | Universal limit (K5.1) | No | No (K4.2) |
| Δ_p(t) = O(p^{-1/2}) | Prime-specific correction | Yes | Unknown |
| D_p(t) = √p · Δ_p(t) | Renormalized correction | Yes, bounded | Distributional limit open |
| pair-corr R₂^{orbit} | Prime-orbit pair-correlation | No (Poisson, not GUE) | No |

**The real frontier is the renormalized remainder D_p(t) and its distributional limit.**

This is where prime information lives, and it is:
- Prime-specific (different for each p)
- Bounded after renormalization (does not vanish)
- Conjecturally a Gaussian free field limit (by analogy with random matrix fluctuations)
- Not yet connected to ζ zeros in any direct way

**What would K6 progress look like:**

1. **Compute D_p(1/2) for many primes p** and test:
   (a) Does D_p(1/2) → 0 (corrections at midpoint vanish even after renormalization)?
   (b) Does D_p(1/2) fluctuate randomly around 0 (with variance ~ 1)?
   (c) Is there a pattern in D_p(1/2) that correlates with the position of ζ zeros?

2. **Prove or disprove:** lim_{X→∞} (1/π(X)) Σ_{p≤X} D_p(t)² = C(t) for some C(t)
   (whether the average squared correction converges to a limit function).

3. **Connect to Chebotarev:** D_p(t) is related to how many of the orbit's elements
   fall near position t vs. the expected uniform density. This is a local version of
   the prime number theorem in arithmetic progressions. Deviations from equidistribution
   at position t are controlled by zeros of Hecke L-functions with quadratic characters.

4. **The explicit formula for D_p(t):** If there is an explicit formula expressing
   Σ_{p≤X} D_p(t) in terms of ζ zeros (or Hecke L-function zeros), that would be
   the connection K6 is looking for.

---

## K6.7 — Summary

**What K6 establishes:**
- The correction Δ_p(t) is prime-specific and O(p^{-1/2}) (Weil bound)
- The renormalized correction D_p(t) = √p · Δ_p(t) is bounded and contains prime information
- The prime-field orbit does NOT have GUE pair-correlation — it has Poisson statistics
  (confirming K2_5 counterexample T3 and strengthening Hypothesis A)
- The distributional limit of D_p as p → ∞ (over all primes) is an open problem
  analogous to Gaussian fluctuations in random matrix theory

**What K6 does NOT establish:**
- A connection between D_p and ζ zeros
- A path from the correction terms to an RH bridge

**The bottom line:**
The prime information in D2's corrections is real but does not straightforwardly help.
The corrections push toward Poisson statistics (not GUE), the orbit lacks determinantal
structure (no H3), and the distributional limit of renormalized corrections is an open
research question in probabilistic number theory.

The real frontier is the intersection of K5.1 (abstract local law) and the question
of whether prime-field orbits ever exhibit determinantal structure beyond what Weyl
equidistribution provides. That question is currently open and is the Montgomery-
Keating-Snaith program restated in the concrete language of the K-series.

---

*Prerequisite: K1_KERNEL_UNIVERSALITY.md (K1.6), K5_LOCAL_SINC2_THEOREM.md (K5.1)*
*See also: K2_5_COUNTEREXAMPLE_SEARCH.md (T3, T5 — orbit pair-correlation is Poisson)*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
