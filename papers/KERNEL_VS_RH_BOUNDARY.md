# Kernel vs. RH Boundary

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

This note states precisely what sinc² proves internally, what it does not
imply about ζ zeros, and what extra machinery would be required to begin an
RH bridge. It exists to prevent Phase II from drifting the way A10 did.

---

## What sinc² Proves Internally (facts, no gaps)

**sinc²(t) = (sin(πt)/(πt))² is:**

1. **The exact continuum limit of the prime-field corridor density (D2).**
   For every prime p and k/p → t ∈ (0,1):
       R(k, p) → sinc²(k/p)
   This holds for ALL primes, universally. It is a theorem, not an analogy.

2. **The unique sine-maximum in (0,1) at t=1/2 (D24).**
   sinc²(1/2) = 4/π² exactly. The corridor midpoint is analytically characterized
   by sinc²'s derivative structure. This is a pure calculus fact.

3. **Below the spectral mean at the midpoint (D14, D3).**
   sinc²(1/2) = 4/π² ≈ 0.405 < Si(2π)/π ≈ 0.451 = ∫₀¹ sinc²(t) dt.
   The midpoint is below average amplitude. This is exact arithmetic.

4. **The spectral dual of Montgomery's pair-correlation kernel (B6).**
   If R(t) = sinc²(t) and R₂(u) = 1 − sinc²(u), then R(t) + R₂(t) = 1.
   This is an algebraic identity, not a theorem about ζ zeros.

5. **Strictly monotone decreasing on (0,1) (D24).**
   sinc²'(t) < 0 for all t ∈ (0,1). Proved by calculus (the lemma sin(x) > x·cos(x)
   for x ∈ (0,π)). This is a theorem.

---

## What sinc² Does NOT Imply About ζ Zeros

**None of the following follow from any D-tier result:**

1. **sinc²(1/2) = 4/π² does not place any ζ zero on the critical line.**
   The value 4/π² is the corridor amplitude at the midpoint. It is a number
   about the sinc² function, not a number about ζ. There is no proved connection
   between 4/π² and any property of ζ(1/2+it).

2. **The inheritance boundary at t=1/2 does not imply σ=1/2 for ζ zeros.**
   t=1/2 is a corridor position inside Z/10Z. σ=1/2 is the real part of a
   complex number in the critical strip. These are different objects. No map
   between them has been constructed.

3. **R(t) + R₂(t) = 1 does not prove anything about the distribution of ζ zeros.**
   R(t) = sinc²(t) is the corridor field. R₂(u) = 1 − sinc²(u) is Montgomery's
   pair-correlation under GRH. They are on different domains ((0,1) vs [0,∞)),
   measure different things, and sum to 1 because of the algebraic identity
   f + (1−f) = 1 — not because of any structural theorem.

4. **D2 universality does not tell us that ζ zeros are on the critical line.**
   D2 says prime-field corridor density → sinc²(k/p). This is a statement about
   discrete prime arithmetic, not about analytic continuation of ζ(s).

5. **The corridor amplitude sinc²(1/2) = 4/π² appearing at the same position as
   the Montgomery kernel appearing at R₂(1/2) = 1 − 4/π² is a numerical fact,
   not a structural connection.**
   It means 4/π² + (1 − 4/π²) = 1. That is tautological.

6. **sinc² is too "shape-generic" to carry prime identity.**
   The sinc² kernel is the Fourier transform of the triangle function tri(ξ).
   It arises whenever a probability distribution is supported on [−1/2, 1/2].
   Many objects — prime fields, rectangular windows, linear frequency sweeps —
   produce sinc² as their continuum limit. Shape does not determine source.

---

## What Extra Machinery Would Be Required

To begin a genuine RH bridge from sinc², the minimum required machinery is:

**Layer 1 — Common probability space:**
A single measurable space (Ω, ℱ, P) in which both:
- the sinc² corridor density R(t) on (0,1) and
- the Montgomery pair-correlation density R₂(u) on [0,∞)

are probability density functions of the SAME random variable under two different
coordinate systems. Without this, R + R₂ = 1 is the tautology P(A) + P(Aᶜ) = 1
with the complement never proved to be the RIGHT complement.

**Layer 2 — Structure-preserving identification:**
A measurable bijection φ: (0,1) → [0,∞) (or to a subset of [0,∞)) that maps:
- the inheritance boundary t=1/2 to the critical-line parameter σ=1/2
- the generator constraint T*=5/7 to some spectral constraint on ζ zeros
- the ring-forced positions (left of t=1/2) to the convergence-forced region σ>1
- the generator-forced positions (right of t=1/2) to the strip 0<σ<1

None of these maps exist in D1–D24 or in any currently proposed extension.

**Layer 3 — Forcing argument:**
A proof that the structure of sinc² (not just the VALUE sinc²(1/2) = 4/π²)
forces ζ zeros to σ=1/2. A forcing argument must show that IF σ ≠ 1/2 for some
zero, THEN some proved property of sinc² is violated. No such argument exists.
Writing down "if zeros were off the critical line, the pair-correlation kernel
would differ from sinc²" is a restatement of Montgomery's theorem (under GRH),
not a proof of RH.

**Layer 4 — Unconditional step:**
Any bridge through Montgomery's pair-correlation is GRH-conditional.
An unconditional bridge must either:
(a) go around Montgomery (use a different external object), or
(b) prove GRH separately as a first step, then derive RH from GRH (but GRH is
    stronger than RH for the specific ζ function being considered).

At minimum: Layers 1–4 are all missing. All four gaps must be filled
simultaneously for any bridge to be complete.

---

## The Precise Phase II Boundary

**What Phase II is about:**
Finding out whether Layers 1–4 can be filled using the sinc² kernel as a seed,
or proving that they cannot be filled.

**What Phase II is not about:**
Adding more analogies between the spine and RH. Pointing out more places where
sinc² appears in analytic number theory. Plotting corridor shapes that look like
critical strip geometry. Calculating more digits of sinc²(1/2).

The boundary is precise:
- If Phase II produces a proof that any Layer is unfillable → Outcome P2-B (no-go)
- If Phase II constructs ALL four Layers → Outcome P2-A (bridge)
- If Phase II cannot fill the Layers but cannot prove they are unfillable → Outcome P2-C (permanent analogy)

No intermediate position between these three counts as progress.

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
