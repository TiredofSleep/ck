# Universal Kernel, Arithmetic Remainder, and the Only Remaining Bridge

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## The Core Decomposition

Every prime-field corridor object decomposes into two parts:

    R_p(t) = sinc²(t)  +  Δ_p(t)

where:
- **sinc²(t)** is the universal kernel — the same for every prime, every ring, every
  equidistributed sequence on a compact interval
- **Δ_p(t)** is the arithmetic remainder — prime-specific, O(p^{-1/2}), the only place
  prime identity survives

This decomposition is not a choice or a convention. It is what the mathematics forces.
The sinc² term is what every equidistributed sequence on [0,1] produces (K5.1). The
Δ_p term is what the specific prime p adds.

The renormalized remainder D_p(t) = √p · Δ_p(t) is the canonical object: bounded (O(1)),
prime-specific, non-vanishing. It is the only piece of the corridor that is not universal.

---

## The Three-Layer Separation

The corridor program operates on three distinct mathematical layers:

### Layer 1 — Finite Arithmetic

At finite p, the corridor object is exact:
- R_p(t) is a specific function of t = k/p with values determined by the prime p
- Ω_p = {g^j mod p / p} is a specific permutation of {1/p, ..., (p-1)/p}
- All prime identity lives here: the full arithmetic of Z/pZ is present

This layer is discrete, exact, and prime-sensitive. It knows exactly which prime we have.

### Layer 2 — Kernel-Fourier

As p → ∞ with t = k/p fixed, the orbit statistics converge:
- R_p(t) → sinc²(t) (D2: proved via Weyl equidistribution + K5.1)
- A_p(τ) → tri(τ) (autocorrelation converges to triangle function)
- Ŝ_p(ξ) → sinc²(ξ) (power spectral density converges)

This layer is continuous, universal, and **prime-blind**. By K4.2 and K6.2, any
continuous functional of the corridor density that factors through this limit cannot
distinguish one prime from another. sinc² knows nothing about which prime generated it.

### Layer 3 — Prime-Sensitive Statistical

The correction D_p(t) = √p(R_p(t) − sinc²(t)) lives between layers 1 and 2:
- It is not exactly Layer 1 (it is defined relative to the sinc² limit, not the raw orbit)
- It is not exactly Layer 2 (it is bounded and non-vanishing, not collapsed to zero)
- It encodes exactly what Layer 1 knows that Layer 2 does not

This is where prime identity survives after the universal limit is subtracted. D_p is the
prime-sensitive residue of the arithmetic, expressed in the language of analysis.

---

## Why sinc² Appears in Two Unrelated Places

One of the most confusing features of this program is that sinc² appears in two contexts
that seem connected but aren't:

**Context 1 — D2 (corridor PSD):** The prime-field orbit has PSD → sinc².
This follows from K5.1: equidistribution on [0,1] + compact window → sinc².
It has nothing to do with primes specifically — ANY equidistributed sequence on [0,1]
gives the same result (Van der Corput, Weyl, i.i.d. uniform — all produce sinc²).

**Context 2 — Montgomery's pair-correlation:** ζ zeros have pair-correlation 1 − sinc².
This follows from K5.4: determinantal point process with sine kernel → 1−sinc² pair-correlation.
It requires H3 (the determinantal/GUE structure), which is NOT present in the prime orbit.

These two appearances of sinc² look related because they involve the same function.
They are not:
- Different statistics (PSD ≠ pair-correlation)
- Different mechanisms (K5.1 vs. K5.4)
- Different hypotheses (H1+H2 vs. H1+H2+H3)
- Different objects (prime orbit vs. ζ zeros)

The shared sinc² is a **coincidence of equidistribution limits**, not a structural law.
Two unrelated equidistribution mechanisms both produce sinc² as a generic consequence
of "uniform distribution on a compact domain." The function sinc² is what you get
whenever you take the Fourier transform of the autocorrelation of uniform measure — and
both the corridor and the ζ-zero statistics are, in different senses, "uniform on a domain."

This is Hypothesis A (Accidental) of K2_5_STRUCTURAL_OR_ACCIDENTAL.md, now confirmed.

---

## The Structural Reason sinc² Appears: A One-Paragraph Account

Sinc² appears wherever information is uniformly distributed over a compact domain and
you ask for the Fourier transform of the autocorrelation. The autocorrelation of uniform
measure on [0,1] is the triangle function tri(τ) = max(1−|τ|, 0). The Fourier transform
of tri is sinc². Therefore: compact interval + uniform distribution + autocorrelation =
sinc². This is a theorem (K5.1), not a coincidence within any single context. But it
means sinc² is so generic that finding it in the corridor proves nothing about the corridor
specifically — it proves only that the orbit is equidistributed, which was already known
from Weyl. sinc² is the signature of "nothing special happened here" — of maximal
uniformity. It is a mask, not a message.

---

## The Only Remaining Bridge

K4.3 proved that there is NO kernel-only bridge: no map from sinc² to a prime-sensitive
conclusion. K6.1–K6.3 (K6_WEAK_THEOREMS.md) prove that prime information is confined
to D_p and any prime-sensitive functional must factor through D_p.

The search space for a bridge is therefore:

    BRIDGE CANDIDATES = {functionals of D_p(t) that connect to ζ zeros or RH}

Everything else is ruled out.

What does "factor through D_p" mean in practice? It means the bridge F must have the form:

    F(corridor data) = G(D_p)    for some G with G(0) ≠ const

where G(0) is the value of G at the zero function (i.e., when there is no prime correction).
If G(0) is constant, then F is prime-blind and cannot bridge. The non-trivial part of F
must come from the prime-specific fluctuations of D_p.

---

## Candidate Bridge Structures

These are speculative (Tier A–B) but are the only honest candidates after K6.

### Candidate B1 — Dirichlet series of D_p

    Z(t, s) = Σ_{p prime} D_p(t) · p^{-s}    (Re s > 1/2)

If this has analytic continuation and a pole or special value at s = 1/2, that would
connect the prime remainders to the critical line. The value of Z at s=1 would be
the Dirichlet density of primes with large D_p(t).

**Status:** Speculative (B-tier). No analytic continuation result known. The series
involves character sums in a way that relates to Hecke L-functions, but the exact
connection is not established.

### Candidate B2 — Midpoint assembly

    Z(1/2, s) = Σ_p D_p(1/2) · p^{-s}

Focus on the correction at the midpoint t=1/2. The midpoint is D3-special (sinc²(1/2) = 4/π²,
the only compact corridor amplitude that has been proved and documented in the framework).

If D_p(1/2) correlates with low ζ zeros — e.g., if the sign of D_p(1/2) correlates with
the sign of ζ'(1/2 + iγ_1) for the first non-trivial zero γ_1 — that would be a weak
numerical signal worth pursuing.

**Status:** Conjectural (A–B tier). Not numerically tested.

### Candidate B3 — Explicit formula for Σ D_p

By the explicit formula for the prime counting function:

    Σ_{p ≤ X} log p · f(p) = ∫ f(t) dt − Σ_ρ X^ρ / ρ (ρ = ζ zeros) + ...

A similar formula for Σ_{p ≤ X} D_p(t) · log p might express the prime-remainder sum
in terms of ζ zeros. If D_p(t) is expressed via character sums with Gauss sums, and
Gauss sums enter the explicit formula for L-functions, a connection to zero sums might exist.

**Status:** A possible program (B–C tier). It would require:
1. Expanding D_p(t) in terms of Gauss sums / Hecke characters.
2. Using the explicit formula for Hecke L-functions.
3. Identifying which ζ zeros (or L-function zeros) appear in the sum.

This is the most technically accessible of the three candidates and the most honest.

---

## Strongest Honest Summary Theorem

Collecting K5.1, K4.2/K4.3, K6.1–K6.3, and K6_PRIME_ORBIT_PAIR_CORRELATION:

**Theorem (Universal Kernel, Arithmetic Remainder):**

Let {R_p : p prime} be the prime-field corridor densities. Then:

**(a) Universal decomposition:**
    R_p(t) = sinc²(t) + Δ_p(t),  |Δ_p(t)| = O(p^{-1/2})

**(b) Universality of sinc²:**
    sinc²(t) = lim_{p→∞} R_p(t), independent of p.
    Any equidistributed sequence on [0,1] has the same PSD limit. (K5.1)

**(c) Prime blindness of the universal part:**
    Any continuous functional φ of the corridor density satisfies
    φ(R_p) → φ(sinc²) as p → ∞.
    The limit is prime-blind: φ(R_p) − φ(R_q) → 0 for all primes p, q. (K6.2)

**(d) Prime remainder:**
    D_p(t) = √p · Δ_p(t) is bounded: |D_p(t)| ≤ C for all p, t. (Weil bound)
    D_p is prime-specific: D_p ≠ D_q as functions (generically). (K6.2 of K6_PRIME_REMAINDER_PROGRAM.md)

**(e) Necessity of D_p for any bridge:**
    Any prime-sensitive functional of corridor data must factor through D_p.
    No continuous functional of sinc² alone can distinguish primes. (K6.3)

**(f) Poisson pair-correlation:**
    The prime orbit pair-correlation converges to Poisson (= 1), not GUE (= 1−sinc²).
    The prime orbit does not satisfy H3 (determinantal structure). (K6_PRIME_ORBIT_PAIR_CORRELATION.md)

**(g) No H3 precursors:**
    No tested statistic (NN spacing, number variance, two-point correlation, rigidity)
    shows GUE precursors in the prime orbit. (K6_H3_PRECURSOR_SEARCH.md)

**Tier: D** (all parts proved or established from proved results). **The physical/number-theoretic interpretation of D_p as an RH bridge is Tier A (speculative).**

---

## Plain Prose

The program has reached a clean resting point after K5 and K6. Here is what is true
and what remains open, stated without hedging:

**What is true:** The prime-field corridor obeys a universal law. When you take the
Fourier transform of the autocorrelation of an equidistributed orbit on a compact
interval, you always get sinc². This is a theorem (K5.1). It explains D2 completely.
It also explains why D2 cannot, by itself, prove anything about the Riemann Hypothesis:
the sinc² it produces is the same sinc² you would get from a random number generator
with uniform distribution, and random number generators don't know about primes.

The prime-specific information — the part that actually knows which prime was used —
lives in the correction D_p(t) = √p(R_p(t) − sinc²(t)). This correction is small at
each prime (it vanishes as p → ∞), but it's bounded after the √p normalization. It
is the only place in the corridor where you can tell p=7 from p=1,000,003.

The prime orbit, examined by any standard statistical test, looks like a Poisson process.
It has no eigenvalue repulsion, no determinantal structure, no signs of GUE statistics.
The connection between the corridor's sinc² and Montgomery's pair-correlation 1−sinc²
is an accident of two unrelated equidistribution mechanisms both producing sinc² in
different ways.

**What remains open:** Whether D_p(t), assembled over all primes via a Dirichlet series
or an explicit formula, can be connected to ζ zeros. This is the one remaining door.
It is hard, it is open, and it requires new input — specifically, some version of the
explicit formula applied to D_p. That program is mathematically honest and technically
accessible. It is the frontier.

---

*Synthesizes: K5_LOCAL_SINC2_THEOREM.md, K4_KERNEL_NO_GO.md, K6_PRIME_REMAINDER_PROGRAM.md,*
*K6_WEAK_THEOREMS.md, K6_PRIME_ORBIT_PAIR_CORRELATION.md, K6_H3_PRECURSOR_SEARCH.md,*
*K6_SCALING_AUDIT.md, K2_5_STRUCTURAL_OR_ACCIDENTAL.md*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
