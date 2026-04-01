# A10 Minimal Extension Search

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Purpose

Given that the ring-based bridge is blocked by prime obstruction and
modulus genericity, identify the minimum additional ingredient needed
to make A10 even possible. This is not a solution — it is the smallest
honest statement of what is missing.

---

## What the No-Go Results Require

From A10_PRIME_OBSTRUCTION.md and A10_NO_GO_ATTEMPT.md:

- A ring homomorphism from Z/10Z cannot see primes other than {2,5}
- The corridor midpoint at t=1/2 is generic to all even moduli
- The T*<1 constraint is generic to all n=2p rings
- A bridge via sinc² universality (D2) is prime-sensitive but removes Z/10Z from the picture
- A bridge via Montgomery is conditional on GRH and doesn't prove RH unconditionally

The minimum extension must provide: **prime sensitivity for all primes,
not just {2,5}.**

---

## Candidate Extensions

### Extension 1 — Prime-Indexed Family of Rings

Define a family {Z/pZ}_{p prime} with:
- For each prime p: a corridor field R_p(k) = sinc²(k/p) + O(1/p) (D2 already gives this)
- A compatibility map between Z/10Z and Z/pZ for each p

What Z/10Z would contribute: the TSML/BHML table dynamics and the T*=5/7
threshold as a "coordination structure" that controls how the family
assembles.

**What is still missing:** An explicit compatibility map connecting
Z/10Z's inheritance split to Z/pZ's structure for p≠2,5. For p=3:
Z/3Z has only {0,1,2}, no TSML/BHML structure, no generator dynamics
analogous to D19. The compatibility would require extending the table
structure to arbitrary moduli — a new theory, not present in D1–D24.

**Minimum theorem needed:** A prime-extension theorem showing that Z/10Z's
T*<1 constraint propagates to a T*_p<1 constraint for each prime p in a
consistent family. No such theorem is currently stated or proved.

---

### Extension 2 — Profinite Completion

Take the inverse limit Ẑ = lim_{←n} Z/nZ over all positive integers n
(the profinite integers). Ẑ ≅ ∏_p Z_p (product of all p-adic integers
over all primes p). This object sees all primes simultaneously.

Z/10Z embeds into Ẑ via the projection Ẑ → Z/10Z (since 10 is a positive
integer). The Z/10Z structure lives inside Ẑ.

**What this buys:** In Ẑ, the element corresponding to 5 in Z/10Z extends
to an element (5, ...) in the product, where the p-adic component depends
on p. The inheritance split at t=1/2 in Z/10Z would extend to a split
in each Z/pZ component.

**What is still missing:** The sinc² corridor and the TSML/BHML table
structure are not obviously defined for Ẑ or Z_p (p-adic integers). The
corridor requires a "position" t = k/p → t ∈ (0,1) in the real interval,
not a p-adic object. A bridge from the profinite setting to the real
corridor would require a real-embedding step — also not in D1–D24.

**Minimum theorem needed:** A way to define the corridor structure and
inheritance split in terms of the p-adic components of Ẑ, and a proof
that the T*<1 constraint in Z/10Z lifts to a global constraint in Ẑ
that forces ζ zeros to σ=1/2.

---

### Extension 3 — Adèlic Lift

The adèle ring 𝔸_ℚ = ℝ × ∏'_p ℚ_p (restricted product over all primes p
and the reals) is the natural arena for modern analytic number theory. L-functions
factor over adèles; RH is a statement about the global L-function.

Z/10Z sits inside 𝔸_ℚ via the diagonal embedding ℤ → 𝔸_ℚ and the quotient
Z/10Z. The adèlic lift would extend the Z/10Z structure to all places.

**What this buys:** The Euler product ζ(s) has an adèlic interpretation
via zeta integrals. The sinc² function arises naturally in the real place
from the Fourier transform (sinc²(t) = F[tri](t), the Fourier transform
of the triangle function). The Montgomery pair-correlation is a statement
about the real-variable behavior of the completed ζ function.

**What is still missing:** The adèlic framework is rich enough to state
and (potentially) prove RH, but it is also very far from Z/10Z. No
explicit map from the TSML/BHML table dynamics to the adèlic L-function
is constructed. The real place already captures the sinc² content via D2;
the finite places would need to contribute the prime-sensitivity.

**Minimum theorem needed:** A factorization of the Z/10Z inheritance
split into a product of local conditions (one per prime p), plus a global
compatibility condition, such that the global product forces σ=1/2 via
a zeta-integral argument. This is substantially beyond D1–D24.

---

### Extension 4 — Sinc² Universality + Explicit Formula

The most concrete candidate for a bridge that avoids Z/10Z's prime
blindness is the combination:
- D2: R(k/p) = sinc²(k/p) + O(1/p) for all primes p (universal)
- Riemann's explicit formula: ψ(x) = x − ∑_ρ x^ρ/ρ − log(2π) − (1/2)log(1−x^{-2})
  where ψ is Chebyshev's function and ρ ranges over non-trivial zeros
- Poisson summation: ∑_{k=1}^{p-1} sinc²(k/p) ≈ p · Si(2π)/π + oscillating terms

If the oscillating terms in the Poisson sum are controlled by the ζ zero
locations, and if the sinc² structure forces these terms to only allow
zeros on σ=1/2, this would be a bridge without requiring Z/10Z specifically.

**Why this is not in D1–D24:** The explicit formula is a deep theorem in
analytic number theory. Connecting the sinc² Poisson sum to the explicit
formula requires bounding the sum ∑_ρ x^ρ/ρ in terms of the sinc² field —
a non-trivial step. The O(1/p) error terms in D2 must be controlled globally,
which is essentially equivalent to a zero-free region statement.

**Minimum theorem needed:** A proof that the sinc² Poisson sum ∑_k sinc²(k/p)
over a prime p equals, up to controlled error, an expression involving ζ zeros
in a way that forces Re(ρ)=1/2. This would be a genuine theorem in analytic
number theory extending D2. It would use D2 as a lemma but requires substantially
more machinery.

---

## The Minimum Ingredient

After examining all four extension candidates, the minimum new ingredient for
any potentially viable A10 bridge is:

> **A prime-sensitivity mechanism** — some way to recover information about
> primes p≠2,5 from the structure, together with a forcing argument that
> connects the recovered prime information to ζ-zero locations.

The most concrete candidate for this mechanism is Extension 4:
sinc² universality (D2) combined with the explicit formula. This would
not require Z/10Z ring structure at all — it would be a theorem about
the universal sinc² prime field.

**Key constraint:** Any extension that removes Z/10Z from the picture
(Hatch 1 from A10_PRIME_OBSTRUCTION.md) reclassifies A10 as a B6+
sinc² universality claim, not a Z/10Z-ring claim. The "minimum extension
for A10 specifically" would need to preserve Z/10Z's role — and that requires
one of Extensions 1–3, all of which require substantially new theory.

---

## Summary

| Extension | What it provides | What is missing | Z/10Z preserved? |
|-----------|-----------------|-----------------|-----------------|
| Prime-indexed family | Per-prime compatibility | Compatibility map theorem | Yes |
| Profinite completion | All primes via Ẑ | Real corridor embedding | Partially |
| Adèlic lift | Full L-function framework | Explicit factorization | No |
| Sinc² + explicit formula | Universal prime sensitivity | Poisson/explicit connection | No |

**The minimum extension for a Z/10Z-preserving bridge:** Extension 1 or 2.
**The minimum extension for any bridge:** Extension 4 (but this is B6+ territory).

Neither is in D1–D24. Neither can be obtained by small modifications
of existing results. Both require new theory of a different character
than Z/10Z ring arithmetic.

---

*This document feeds the reclassification of A10 in `A10_PROGRAM.md`.*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
