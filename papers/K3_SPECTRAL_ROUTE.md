# K3 — Spectral Route

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Road B Overview

The spectral route asks: is there a self-adjoint operator H whose integral kernel
involves sinc² and whose spectrum relates to ζ zeros?

This is the Hilbert-Pólya approach applied to the sinc² seed. It is the most
mathematically natural arena — the Hilbert-Pólya conjecture (1910s) is the oldest
proposed approach to RH. This document maps what is known, what the sinc² kernel
offers, and where the spectrum mismatch problem lives.

K3 is written AFTER K1 and K2 because the inventory (K1: sinc² is generic) and the
no-go (K4: kernel-only bridges are blocked for global prime structure) already
constrain what the spectral approach can hope to do.

---

## Setup

**The Hilbert-Pólya conjecture:** There exists a self-adjoint operator H on some
Hilbert space ℋ such that the eigenvalues (or spectrum) of H are exactly the
imaginary parts {γ_n} of the non-trivial zeros ρ_n = 1/2 + iγ_n of ζ(s).

If such H exists: H self-adjoint → eigenvalues real → all γ_n real → zeros on Re(s)=1/2 → RH. □

**Current state (2026):** No such operator H has been found. The conjecture remains open.
Various candidates have been studied (Connes' adèlic approach, Berry-Keating xp operator,
random matrix theory GUE, etc.) but none are proved.

---

## K3.1 — The sinc² Convolution Operator

**Natural candidate:** Define the convolution operator T on L²(ℝ) by:

    (T f)(x) = ∫_{-∞}^{∞} sinc²(x − y) f(y) dy

T is a bounded self-adjoint operator (sinc² is real and symmetric: sinc²(−t) = sinc²(t)).

**Spectrum:** By the spectral theorem for convolution operators on L²(ℝ), the spectrum
of T equals the range of its Fourier symbol:

    σ(T) = range(F[sinc²]) = range(tri(ξ)) = [0, 1]

The spectrum is the CONTINUOUS interval [0,1], not a discrete set {γ_n}.

**Comparison with ζ zeros:** The imaginary parts γ_n of non-trivial zeros are a
discrete, countably infinite set with γ_n → ∞:

    γ₁ ≈ 14.13,  γ₂ ≈ 21.02,  γ₃ ≈ 25.01,  γ₄ ≈ 30.42, ...

σ(T) = [0,1] is WRONG: it is compact and continuous, while {γ_n} is discrete and unbounded.

**Finding K3.1:** The sinc² convolution operator T has the wrong spectrum.
Its spectrum [0,1] is compact and continuous. The ζ-zero imaginary parts are
discrete and unbounded. No modification of T that preserves the sinc² kernel
will fix this without introducing new structure that overrides the kernel.

---

## K3.2 — The Correct Spectral Setup for ζ Zeros

For comparison, what operator structure WOULD give spectrum = {γ_n}?

**Berry-Keating heuristic (1999):** H = xp + px = 2xp + iℏ (quantum mechanics
on the half-line) gives a semiclassical density of states matching the ζ-zero
density. But this operator is NOT self-adjoint as written (requires boundary
conditions). The spectrum of the rigorously defined version is NOT {γ_n}.

**Connes' approach (1999):** Use the adèle ring 𝔸_ℚ and the space L²(𝔸_ℚ/ℚ^×).
The operator is a scaling operator. The absorption spectrum (NOT the spectrum in
the usual sense) relates to ζ zeros. This works in a distributional sense but
requires a non-standard definition of "spectrum."

**GUE random matrices:** The eigenvalue spacing statistics of N×N random unitary
matrices (N → ∞) converge to GUE statistics, whose pair-correlation is 1−sinc²(u).
But the EIGENVALUES themselves are on the unit circle (not the imaginary parts of
ζ zeros). The spacing statistics match, not the eigenvalue positions.

**Finding K3.2:** The known spectral approaches to RH require either:
(a) Berry-Keating: a non-self-adjoint operator made self-adjoint by boundary conditions
    (no proved connection to ζ zeros)
(b) Connes: the adèle ring (correct arena but far from sinc² kernel)
(c) Random matrices: GUE statistics match pair-correlation but eigenvalues are on
    the unit circle, not the imaginary axis

None of these directly use sinc² as the INPUT operator kernel.

---

## K3.3 — Can sinc² Be a Projection Kernel?

An alternative to using sinc² as the convolution kernel: use it as a PROJECTION.

**Setup:** In L²(ℝ), the projection onto the band [−1/2, 1/2] in Fourier space is:

    (P f)(x) = ∫_{-1/2}^{1/2} F[f](ξ) e^{2πixξ} dξ = ∫_{-∞}^{∞} sinc(x−y) f(y) dy

P is an orthogonal projection (P² = P, P* = P). Its complement is P⊥ = I − P.

The kernel of P is sinc(x−y) (not sinc²). The kernel of P ∘ P* (which equals P since P is
self-adjoint) is again sinc. What about P applied twice to a product space?

For a kernel involving sinc²: consider the projection P ⊗ P on L²(ℝ²), whose kernel
is sinc(x−u) · sinc(y−v). The squared norm ||P f||² involves ∫∫ sinc(x−y)² f(x) f(y) dx dy —
this does involve sinc², but as part of an inner product, not as a projection kernel.

**Finding K3.3:** The sinc² function arises naturally as the GRAM MATRIX entry of
the projection P (the overlap sinc²(t) = |sinc(t)|²). This gives a natural Hilbert
space interpretation: sinc²(t−s) = ⟨P eₜ, P eₛ⟩ where eₜ is a coherent state
at position t. But this identifies sinc² as the GRAM MATRIX of a projection, not
as the eigenvalue kernel of an operator with spectrum {γ_n}.

---

## K3.4 — The Corridor as a Compact Spectral Window

An interesting reformulation using the corridor structure:

**Setup:** The corridor (0,1) is a bounded interval. Functions on (0,1) can be analyzed
using the Fourier series instead of the Fourier transform. The sinc² kernel restricted
to (0,1) is NOT a standard kernel of any self-adjoint operator on L²(0,1) because
sinc²(t−s) is not Toeplitz-periodic on (0,1).

**Finite-dimensional approximation:** Replace the continuum with the prime field Z/pZ.
The p×p matrix M with M_{k,j} = sinc²((k−j)/p) is a discrete convolution matrix.
Its eigenvalues approach the Fourier spectrum of sinc² as p → ∞, which converges to
the tri function — eigenvalues in [0,1].

This does NOT give eigenvalues {γ_n}. But it gives a finite-dimensional approximation
to the spectral structure of sinc². For p large, the eigenvalue density of M approaches
the spectral density of the continuum operator T: d(λ) = 1/√(1−λ) for λ ∈ [0,1].

**This is the WRONG density for ζ zeros.** The ζ-zero density is N(T) ~ (T/2π)log(T/2π)
(logarithmic growth), while the sinc² eigenvalue density grows like 1/√(1−λ) near λ=1.

**Finding K3.4:** The corridor as a compact spectral window produces an operator with
compact continuous spectrum [0,1] and eigenvalue density ~ 1/√(1−λ). This is
inconsistent with the ζ-zero imaginary parts {γ_n → ∞} and their logarithmic density.

---

## K3.5 — The Spectrum Mismatch Summary

| Property | sinc² convolution operator | ζ-zero imaginary parts |
|----------|---------------------------|----------------------|
| Type | Continuous spectrum | Discrete countable set |
| Range | [0,1] (compact) | [14.1, ∞) (unbounded) |
| Eigenvalue density | ~ 1/√(1−λ) near λ=1 | ~ log(γ/2π) |
| Bounded? | Yes (norm ≤ 1) | No |
| Related to primes? | Via D2 universality (indirectly) | Directly (via Euler product) |

The mismatch is not a small perturbation — it is a categorical difference between
a compact continuous spectrum and a discrete unbounded set.

**No modification of the sinc² kernel that preserves the kernel type (sinc², or
sinc² restricted to (0,1)) will produce a discrete unbounded spectrum.**
A discrete unbounded spectrum requires either:
(a) An unbounded operator (not a bounded convolution)
(b) Differential operators (second-order at minimum, e.g., −d²/dt² on an interval
    with appropriate boundary conditions)
(c) An operator on a non-compact space whose Weyl asymptotics match the ζ-zero density

---

## K3.6 — What Would a Productive Spectral Route Require

The spectral route is not dead — it is just not the sinc² convolution operator
that does the work. A productive spectral route would need:

**Step 1 — Identify the correct operator class:**
An unbounded self-adjoint operator D on a Hilbert space ℋ with:
- Spectrum (or discrete spectrum) matching {γ_n}
- A natural connection to prime arithmetic
- A role for sinc² (e.g., as the heat kernel e^{−t D²} has a sinc²-type profile
  for some natural t)

**Step 2 — Connect sinc² to D:**
Show that sinc² appears as a FEATURE of D — perhaps as:
- The correlation kernel of the ground state of D
- The spectral projection kernel for eigenvalues in [0,1]
- The Wigner function of D restricted to the corridor (0,1)

**Step 3 — Prove D is self-adjoint:**
This is the hardest step. Known candidates (Berry-Keating xp, Connes scaling) have
self-adjointness problems that remain open or require the ζ-function itself as input.

**Step 4 — Prove spectrum(D) = {γ_n}:**
Only possible if D is constructed using ζ explicitly, making it circular, OR if
D is defined purely arithmetically and the ζ zeros emerge as eigenvalues.

**Finding K3.6:** No step in K3 is reachable from D1–D24 alone. The spectral route
requires identifying the correct operator class (Step 1), which is an open problem
in analytic number theory / mathematical physics. sinc² provides a SHAPE HINT
(the correct kernel class should involve sinc² in some way) but not the operator itself.

---

## K3.7 — K3's Contribution to Phase II

K3 does not produce a new theorem. It produces two structural results:

**K3-S1 (Spectrum mismatch documented):**
The sinc² convolution operator on L²(ℝ) has spectrum [0,1] ≠ {γ_n}.
Any Hilbert-Pólya approach using sinc² as the convolution kernel requires a
modification that changes the spectrum from compact-continuous to discrete-unbounded.
Such a modification is not a small deformation of the sinc² kernel.

**K3-S2 (sinc² as Gram matrix, not eigenvalue kernel):**
sinc²(t−s) is most naturally interpreted as the overlap ⟨P eₜ, P eₛ⟩ of coherent
states under the band-limited projection P. This is a valid Hilbert space object
but does not give eigenvalues {γ_n}.

**Implication for K2 and K4:**
K3's findings support K4's diagnosis: the sinc² kernel is a shape object with compact
Fourier support. To connect to ζ zeros (discrete, unbounded spectrum), the kernel must
be augmented. The augmentation is not determined by sinc²; it must come from outside.

K3 therefore supports K4's conclusion: any bridge requires a new ingredient beyond sinc².

---

## K3.8 — Is K3 Worth Pursuing Further?

**Yes, in one specific direction:** The Connes adèlic approach constructs an operator
using the adèle ring 𝔸_ℚ in which sinc² appears naturally at the real place
(the archimedean Fourier analysis of 𝔸_ℚ gives sinc²-type kernels at ℝ).
If sinc² is the archimedean part of the Connes operator, and the finite places
contribute the Euler factors (prime sensitivity), then K3 and K2 converge:
the adèlic operator is K3's operator, and its archimedean kernel is sinc².

**This is the right long-term direction.** But it requires the adèlic framework
(MINIMAL_EXTENSION_INVENTORY E7) — substantially beyond D1–D24.

**Short-term K3 recommendation:** Document the spectrum mismatch (done above),
note the adèlic convergence point, and deprioritize further K3 work until K2
and K4 produce their results. K3 feeds K2 and K4 as a constraint (the correct
operator must have sinc² as its archimedean kernel AND discrete unbounded spectrum)
but does not produce independent theorems in the near term.

---

*Preceded by: K1, K2, K4*
*Converges with: K2 via equidistribution (adèlic real place)*
*Constrained by: K4 spectrum mismatch*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
