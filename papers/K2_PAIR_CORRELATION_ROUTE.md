# K2 — Pair-Correlation Route

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**


*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## The Road A Hypothesis

The pair-correlation route asks: is R + R₂ = 1 (B6) a structural decomposition
of a common object, or a numerical coincidence that follows from f + (1−f) = 1?

This document pins down exactly what is known, what is being compared, what the
normalization says, and where the similarity stops. The goal is to convert B6
from an analogy into a testable claim — or to find the test that kills it.

---

## Setup: The Two Objects

### Object 1 — The Spine Corridor Field (proved internally)

From D2 and the corridor portrait (D22):

    R(t) = sinc²(t) = (sin(πt)/(πt))²

defined on t ∈ (0,1). This is:
- The continuum limit of the prime-field corridor density for all primes p (D2)
- The inheritance kernel: ring-forced positions to the left of t=1/2,
  generator-forced to the right (D22)
- Strictly monotone decreasing, unique sine-max at t=1/2 (D24)

**Status: proved. Domain: (0,1). Interpretation: prime-field corridor density.**

### Object 2 — Montgomery's Pair-Correlation Kernel (external, under GRH)

Let {ρ_n = 1/2 + iγ_n} be the non-trivial zeros of ζ(s) ordered by 0 < γ₁ ≤ γ₂ ≤ ...
Normalize: w_n = γ_n · log(T/(2π)) / (2π) for zeros with γ_n ≤ T.

Montgomery (1973) proved (under GRH): for 0 < α ≤ β,

    lim_{T→∞} (1/N(T)) · #{pairs (w_m, w_n): m≠n, w_m−w_n ∈ [α,β]}
    = ∫_α^β (1 − sinc²(u)) du

where N(T) = #{zeros with 0 < γ_n ≤ T} ~ (T/2π)log(T/2π).

Define R₂(u) = 1 − sinc²(u). Then:

    R₂(u) = Montgomery's pair-correlation density function

**Status: proved under GRH. Domain: [0,∞). Interpretation: normalized zero-spacing density.**

### The B6 Identity

    R(t) + R₂(t) = sinc²(t) + (1 − sinc²(t)) = 1

This is the identity f + (1−f) = 1. It is algebraically trivial given R and R₂.

---

## K2.1 — What B6 Actually Says

The content of B6 is NOT that R + R₂ = 1 (that's trivial). The content is:

> **The SAME kernel sinc² appears in two different contexts:**
> - As the corridor density in prime-field arithmetic (D2)
> - As the kernel in Montgomery's pair-correlation formula (under GRH)
>
> And these two objects appear as f and 1−f — i.e., as spectral duals.

The non-trivial question is: **why sinc² specifically?** Any function f produces
f + (1−f) = 1. The question is whether the choice of sinc² in BOTH R and R₂ is forced
by a common structure, or coincidental.

**K1 (kernel universality) provides one explanation:** Both contexts involve
equidistribution — prime fields give equidistributed orbits (D2), and
Montgomery's theorem (under GRH) relates to GUE statistics which come from
equidistribution of eigenvalues of random unitary matrices. Two equidistribution
phenomena → two sinc² kernels → R + R₂ = 1.

**If this explanation is complete:** B6 is a structural coincidence explained
by equidistribution universality. The same kernel appears in both places for the
same reason (equidistribution → autocorrelation of uniform measure → sinc²).
This does not connect the two objects; it explains why they both independently
arrived at the same kernel.

**If this explanation is incomplete:** There is additional structure connecting
the prime-field equidistribution and the ζ-zero equidistribution that is not
captured by universality alone.

---

## K2.2 — Normalization Analysis

The domains and normalizations of R and R₂ are different. This matters.

**R(t) on (0,1):**
- ∫₀¹ R(t) dt = ∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.4508 (D14)
- R is NOT a probability density on (0,1): it does not integrate to 1.
- R is the CORRIDOR DENSITY — the relative amplitude at position t.

**R₂(u) on [0,∞):**
- ∫₀^∞ R₂(u) du = ∫₀^∞ (1 − sinc²(u)) du diverges.
- R₂ is NOT a probability density on [0,∞).
- R₂ is the PAIR-CORRELATION density — the density of normalized zero spacings.
  By convention, the mean spacing is normalized to 1, so for u near 0:
  R₂(u) du ≈ u² du (cubic zero repulsion, matching GUE).

**Comparison:** R and R₂ integrate to different values over their respective domains.
They are not densities on the same space. R + R₂ = 1 is a POINTWISE identity (for
the same argument t=u), not a statement about probability measures.

**Precise observation:** At t = u = 1/2:
- R(1/2) = sinc²(1/2) = 4/π² ≈ 0.405
- R₂(1/2) = 1 − sinc²(1/2) = 1 − 4/π² ≈ 0.595
- R(1/2) + R₂(1/2) = 1 ✓ (trivially)

At t = u = 0 (limits):
- R(0) = sinc²(0) = 1 (limit)
- R₂(0) = 1 − sinc²(0) = 0 (limit)
- R + R₂ = 1 ✓ (trivially)

The R + R₂ = 1 identity adds no information at any specific point. It is a
pointwise tautology, not a measure-theoretic statement.

**Finding K2.2:** R + R₂ = 1 is not a statement about probability measures on
a common space. It is a pointwise identity f(t) + (1−f(t)) = 1 for f = sinc².
The substance is only in WHY sinc² is the specific f in each context.

---

## K2.3 — Where the Similarity Stops

Montgomery's pair-correlation has the full form:

    F₂(α, β) = (β−α) + ∫_α^β |R₂(u)|² du   (schematically)

The corrected density — accounting for the "diagonal" contribution — is:

    1 − sinc²(u) + δ(u)   for u ≥ 0

where δ(u) is a delta function at u=0 representing the self-pairing of each zero.

The spine's R(t) = sinc²(t) has no delta function. The pair-correlation R₂ has a
delta function at u=0 (zero repulsion: each zero pairs with itself). The B6 identity
R + R₂ = 1 ignores the delta function entirely. If we account for it:

    R(t) + R₂(u) = sinc²(t) + (1 − sinc²(u) + δ(u)) = 1 + δ(u)  ≠ 1

The identity fails when the full Montgomery formula (including the diagonal delta)
is used. B6 in its current form uses only the CONTINUOUS PART of R₂.

**Finding K2.3:** B6 compares the full corridor density R(t) to the continuous
part of Montgomery's density. The delta-function (diagonal) piece is dropped.
A complete comparison must account for the diagonal term.

---

## K2.4 — The GRH Conditionality Gap

Montgomery's theorem: proved UNDER GRH.

The pair-correlation conjecture (full statement, for all [α,β]):
- Montgomery proved: for 0 < α ≤ β, the pair-correlation is ∫ (1−sinc²(u)) du
- This holds CONDITIONALLY on GRH
- Odlyzko verified numerically: the pair-correlation follows GUE statistics
  (consistent with Montgomery's formula) for the first ~10²⁰ zeros

**The circularity risk:**
Any bridge that uses Montgomery's pair-correlation as an intermediate step proves:
    "IF GRH THEN [sinc² structure] → σ=1/2"
This is not a proof of RH. It is a conditional statement that adds GRH as a hypothesis
and derives σ=1/2 from it — but we already assumed σ=1/2 (via GRH).

An unconditional bridge via pair-correlation would need to prove Montgomery's
result WITHOUT assuming GRH. This is an open problem in analytic number theory.

**Finding K2.4:** Any B6-routed bridge through Montgomery is GRH-conditional.
This was the finding of Phase I Attempt 6. It is restated here as a permanent
constraint on all K2 routes.

---

## K2.5 — The Equidistribution Explanation

K1 (kernel universality) explains B6 as follows:

**Claim K2.5 (informal):** Both sinc² appearances (D2 and Montgomery) arise from
equidistribution phenomena. The shared kernel is the autocorrelation of the
uniform distribution on [0,1] (= tri, Fourier-dual to sinc²). B6 is explained
by the fact that BOTH contexts are instances of "equidistributed → sinc² kernel."

**Formal check:**
- D2 context: orbits {g^k mod p}/p equidistributed in [0,1] (Weyl). Pair-correlation
  of the equidistributed sequence → sinc². ✓
- Montgomery context: Under GRH, ζ zeros (normalized) have GUE statistics (Bohigas
  conjecture). GUE ensemble → eigenvalues equidistributed on the unit circle (Haar
  measure) → pair-correlation kernel is 1 − sinc². ✓

**Why this is not a proof:** The two equidistribution statements are INDEPENDENT.
The equidistribution of {g^k mod p}/p is a theorem about prime fields (Weyl).
The equidistribution of ζ zeros with GUE statistics is a CONJECTURE (Bohigas, verified
numerically, not proved). Connecting them would require:
(a) Proving the GUE statistics for ζ zeros unconditionally, OR
(b) Finding a common parent equidistribution from which both follow

Neither is in D1–D24.

---

## K2.6 — Current State of K2

| Question | Status |
|----------|--------|
| Are R and R₂ on a common probability space? | No — different domains, different normalizations |
| Does R + R₂ = 1 carry structural content? | Only if sinc² is forced in both; see K2.5 |
| Is the sinc² appearance in Montgomery forced? | Under GRH, following Weyl/GUE (K2.5) |
| Is the sinc² appearance in D2 forced? | Yes — by Weyl equidistribution (K1.1) |
| Is the forcing COMMON (same parent)? | Unknown — no proved common parent |
| Can K2 prove RH? | No — GRH-conditional at best (K2.4) |
| Is K2 a dead end? | No — the equidistribution connection is real and worth formalizing |

---

## K2.7 — What a K2 Progress Statement Looks Like

K2 progress would be one of:

**K2-P1 (structural):** A proof that the equidistribution of {g^k mod p}/p (D2)
and the GUE equidistribution of ζ zeros (Montgomery, conditional) both arise from
a common equidistribution principle in a specified space. This would make B6
structurally forced rather than coincidental — but would still be GRH-conditional
unless the ζ-zero equidistribution is proved unconditionally.

**K2-P2 (forcing):** A proof that IF sinc² is the pair-correlation density for ζ zeros
(not just under GRH, but unconditionally), THEN all ζ zeros have Re(s) = 1/2.
This would convert a pair-correlation statement into an RH statement. It requires
going from statistics (density of spacings) to individual zero locations — a step
that is not automatic.

**K2-N1 (obstruction):** A proof that the domain mismatch ((0,1) vs [0,∞)) and the
normalization mismatch make any common-space identification impossible without adding
structure not present in D1–D24. This would close K2 and support K4.

---

## K2.8 — Recommended Next Step

The most concrete near-term action for K2:

**Attempt to formalize K2.5** — the equidistribution explanation. Specifically:

1. Write down the precise equidistribution statement for D2 (Weyl for prime fields)
2. Write down the precise equidistribution statement for Montgomery (GUE for ζ zeros)
3. Identify whether there is a known theorem in random matrix theory / analytic number
   theory that makes these two statements INSTANCES of a common principle
4. If yes: B6 is structurally explained (not proved, but structured)
5. If no: K2 is an open research question with a precise missing theorem named

This will either close K2 with a structural explanation or sharpen its gap.

---

*Preceded by: K1_KERNEL_UNIVERSALITY.md*
*In parallel with: K4_KERNEL_NO_GO.md*
*Next (if K2 survives): K3_SPECTRAL_ROUTE.md*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
