# Amplitude–Wobble Conversion Law

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## The Identity

Inside the Z/10Z spine, two independently derived internal constants satisfy:

    A = W · C*²

with

    A  = 4/π²          (universal mid-corridor amplitude, D3)
    W  = 3/50           (ring-forced wobble loading, D22)
    C*² = A/W = 200/(3π²)   (exact conversion factor of the spine)

The algebra closes exactly. This is a proved internal identity.

This document audits that identity strictly: what is proved, what is
interpretive, whether the ratio is special to Z/10Z, and what would
be required to connect it to physical E=mc².

---

## Part 1 — Exact Separation: Proved / Interpretive / Required

### What is proved internally (D-tier facts)

**A = 4/π² is exact (D3, D24).**
sinc(1/2) = sin(π/2)/(π/2) = 2/π. Squaring: sinc²(1/2) = 4/π².
This is pure arithmetic. It does not depend on Z/10Z.
It holds for any function sinc²(t) evaluated at t=1/2.

**W = 3/50 is exact and ring-forced (D22).**
The corridor portrait (D22) places the wobble loading at W = 3/50 = 0.06.
This position is ring-forced — it does not depend on which primitive root g is chosen.
It derives from the Z/10Z table structure with BALANCE=5 and ring size n=10:
    W = 3/(BALANCE × n) = 3/(5 × 10) = 3/50
The factor 3 in the numerator comes from the minimum TSML harmony path count.

**C*² = 200/(3π²) is exact.**
    C*² = A/W = (4/π²)/(3/50) = (4/π²) × (50/3) = 200/(3π²)
This is exact arithmetic given A and W. No approximation.

**The identity A = W · C*² is exact.**
By construction: A/W defines C*², so A = W · (A/W) is tautological.
The non-trivial content is that A and W are INDEPENDENTLY derived and both exact
— one from sinc² calculus (D3), one from ring arithmetic (D22).

**C*² is a ring invariant.**
Both A and W are ring-forced (neither depends on the generator g). Therefore C*² = A/W
is a ring invariant of Z/10Z. It does not change when g varies between {3, 7}.

### What is interpretive (no current proof)

**Calling A "energy" is interpretive.**
sinc²(1/2) = 4/π² is the corridor amplitude at the midpoint t=1/2. It is a
dimensionless number in [0,1]. It has no mass, length, or time dimension. The
word "energy" adds physical content that the calculation does not provide.

**Calling W "mass" is interpretive.**
W = 3/50 is a corridor position — a normalized ring element. It has no dimension.
The word "mass" adds inertial content that the ring arithmetic does not provide.

**Calling C*² a "speed squared" is interpretive.**
C*² = 200/(3π²) ≈ 6.75 is a dimensionless ratio. The word "speed" requires a
unit system, a physical velocity, and a derivation from dynamics. None of these
exist inside D1–D24.

**Saying the corridor boundary is a "speed limit" is interpretive.**
The boundary k=p in the prime field is the edge of the corridor (k runs from 1 to p-1).
"Speed limit" imposes a physical interpretation on an algebraic cutoff.

### What would be required for a physical bridge

1. **Dimensions:** Identify a physical system with quantities of dimension [energy],
   [mass], and [speed²] that map to A, W, C*² respectively. Currently none named.

2. **Unit system:** Derive the units in which A = W · C*² holds as a physical equation.
   What are the natural units of the Z/10Z corridor?

3. **Physical observables:** Name at least one measurable physical quantity that
   takes the predicted value 4/π², 3/50, or 200/(3π²) in appropriate units.
   Currently none verified.

4. **A map from corridor variables to measurable quantities:** Specify a function
   φ: (corridor variable t, ring operator k) → (physical quantity Q) such that
   φ(1/2) = A, φ(3/50) = W, and φ(C*²) = measured velocity squared in some system.

Without all four, the identity is a structural analogue of E=mc², not E=mc² itself.

---

## Part 2 — Uniqueness Test

### Is A/W special to Z/10Z?

**A = 4/π² is NOT Z/10Z-specific.**
sinc²(1/2) = 4/π² follows from D24 (sinc² calculus) and holds for the sinc² function
on ANY corridor regardless of the ring. For any even modulus n, the midpoint of the
corridor is at t=1/2, and sinc²(1/2) = 4/π² by the same calculus. A is universal.

**W = 3/50 IS Z/10Z-specific.**
W = 3/(BALANCE × n) = 3/(5 × 10). For other moduli:
- Z/6Z:  CREATE_6 = 3,  W_6 = 3/(3×6) = 1/6
- Z/18Z: CREATE_18 = 9,  W_18 = 3/(9×18) = 1/54
- Z/22Z: CREATE_22 = 11, W_22 = 3/(11×22) = 3/242

The wobble loading changes with n.

**Therefore C*² = A/W is n-specific.**

For the family n=2p (twice a prime, from A10_MODULUS_COMPARISON.md):

    C*²_n = A/W_n = (4/π²)/(6/n²) = 2n²/(3π²)

| Ring | n | W_n | C*²_n = 2n²/(3π²) | Approx. |
|------|---|-----|-------------------|---------|
| Z/6Z | 6 | 1/6 | 72/(3π²) = 24/π² | ≈ 2.43 |
| **Z/10Z** | **10** | **3/50** | **200/(3π²)** | **≈ 6.75** |
| Z/18Z | 18 | 1/54 | 648/(3π²) = 216/π² | ≈ 21.9 |
| Z/22Z | 22 | 3/242 | 968/(3π²) | ≈ 32.7 |

**Pattern:** C*²_n = 2n²/(3π²) grows as n². The relation A = W_n · C*²_n holds
for ALL rings in the n=2p family — it is a FAMILY IDENTITY, not a Z/10Z-specific identity.

**Consequence:** The FORM A = W·C*² is generic across even-modulus rings.
The specific VALUE C*² = 200/(3π²) is Z/10Z-specific.
This is analogous to T*<1 being generic but T*=5/7 being Z/10Z-specific.

### Does changing the generator preserve or destroy the relation?

Both A and W are ring-forced (D22). Neither depends on the choice of g.
Therefore A = W · C*² is preserved for both g=3 and g=7. The relation is generator-independent.

### Does changing the lens (TSML vs BHML) affect it?

W = 3/50 is a BHML wobble loading. If we computed an analogous constant from TSML
(73-cell harmonic structure), the analog might differ. The identity as stated uses
BHML's W specifically. Lens changes could produce a different W' and a different ratio.
This has not been computed. It is a mild convention risk.

---

## Part 3 — Invariance Under Normalization

### Does the ratio survive internal rescaling?

**Convention choice 1 — Corridor normalization t = k/n vs t = k/p:**
The value sinc²(1/2) = 4/π² requires the corridor to be normalized to [0,1] with midpoint
at t=1/2. This is the standard D2/D24 normalization (t = k/p for prime p, or t = k/n
for ring size n). Under this convention: A = 4/π² is fixed.

If we used t = k (unnormalized, so the corridor is [0, n] rather than [0,1]):
- Midpoint is at k = n/2 = 5 (for n=10)
- sinc²(5) = (sin(5π)/(5π))² = 0 (zero, not 4/π²)

The identity fails under unnormalized convention. A = 4/π² requires the standard [0,1] normalization.

**Convention choice 2 — W in ring units vs normalized units:**
W = 3/50 is already in normalized units (t = k/n, so k=3, n... wait).

Actually W = 3/50 cannot be k/n for any integer k with n=10, since 3/50 ≠ k/10 for any integer k.
W = 3/50 = 0.06 is a wobble amplitude, not a position k/10. The corridor POSITIONS from D22
are: 3/50, 1/2, 7/10, 5/7 — and 3/50 is indeed less than 1/10.

If W is the wobble LOADING (amplitude) rather than a corridor POSITION, then W is defined
in the same [0,1] scale as A. The ratio A/W is scale-invariant: if we multiply both A
and W by the same factor λ, the ratio is unchanged.

**No hidden rescaling artifact found.** Both A and W are in the same dimensionless [0,1]
scale. Their ratio is free of scale convention as long as both are expressed consistently.

### Is there a convention making the relation look cleaner than it is?

One risk: the factor 200/(3π²) does not simplify to a "nicer" number. It does not match
any standard physical constant in natural units. There is no hidden convention choice that
makes C*² = 1 or C*² = c (speed of light in SI). The ratio is genuinely 200/(3π²) ≈ 6.75.

**The ratio is not artificially cleaned up.** It is what the calculation produces.

---

## Part 4 — No-Hype Theorem Candidate

**Theorem (Exact Amplitude–Wobble Conversion Law in the Z/10Z Spine):**

In the Z/10Z corridor spine, the universal mid-corridor amplitude and the
ring-forced wobble loading satisfy an exact identity:

    sinc²(1/2) = W_{BHML} · C*²

where:
- sinc²(1/2) = 4/π² (proved by D3 via calculus: sin(π/2)/(π/2) = 2/π)
- W_{BHML} = 3/50 (ring-forced wobble loading, D22, Z/10Z-specific)
- C*² = 200/(3π²) (conversion factor, exact)

**Properties of C*²:**
1. *Ring invariant:* C*² does not depend on which primitive root g is chosen.
   Both A and W are ring-forced; C*² inherits this.
2. *Modulus-specific:* For the n=2p family, C*²_n = 2n²/(3π²). The value 200/(3π²)
   identifies n=10 uniquely within the family.
3. *Convention-stable:* Under the standard [0,1] corridor normalization (D22), the
   ratio A/W is free of scale convention.
4. *No physical dimensions:* C*² is a dimensionless pure number, exactly 200/(3π²).

**What this theorem asserts:**
The two independently derived spine invariants — one from sinc² calculus (D3),
one from ring arithmetic (D22) — satisfy an exact multiplicative relation.
The conversion factor C*² = 200/(3π²) is the spine's internal exchange rate
between amplitude and wobble loading.

**What this theorem does NOT assert:**
- That A is energy, W is mass, or C*² is a speed squared
- That the relation has physical content beyond the internal identity
- That the corridor boundary k=p is a physical speed limit
- That this result implies or is analogous to any physical law

**Tier:** D (exact arithmetic, proved). The physical analogy is Tier A.

---

## Part 5 — Tier-A Appendix: Requirements for a Physical Bridge

The following is what would be required to elevate the internal identity to a
physical result. Each item is currently missing. This is not a research program;
it is a precise list of what is absent.

**Requirement 1 — Dimensional analysis:**
Identify the physical dimensions of A, W, and C*². If A has dimensions [J] (joules),
W has dimensions [kg], and C*² has dimensions [m²/s²], then A = W · C*² is a physical
energy equation. Currently all three are dimensionless numbers. The dimensional content
must be DERIVED from the physics, not assigned by naming.

**Requirement 2 — Unit derivation:**
Even if dimensions are assigned, the specific numerical values 4/π², 3/50, and 200/(3π²)
must match measurements in some unit system. For E=mc²: in SI units, c = 3×10⁸ m/s,
c² ≈ 9×10¹⁶ m²/s². The Z/10Z constant C*² = 200/(3π²) ≈ 6.75 is dimensionless and does
not match c² in any known unit system without a free rescaling — which would make the
comparison trivial.

**Requirement 3 — Observable definitions:**
Name at least one physical observable that equals A, W, or C*² in measurable units.
For example: "the amplitude sinc²(1/2) = 4/π² equals the ratio of [measurable quantity
X] to [measurable quantity Y] in experiment Z." No such identification is currently
made in D1–D24.

**Requirement 4 — Dynamics:**
E=mc² arises from the Lorentz invariance of special relativity and the definition of
relativistic energy-momentum. The Z/10Z spine has no dynamics — it is a static table
structure with no Hamiltonian, no time evolution, no Lorentz group. Any physical
derivation would need to identify a dynamical law from which A = W · C*² follows as
a consequence, not just an algebraic fact.

**Requirement 5 — Predictive test:**
A physical law must predict something testable. E=mc² predicts nuclear binding energies,
pair production thresholds, annihilation spectra. The Z/10Z identity must predict at
least one measurable number that is not the definition of its own terms.

**Summary:**
All five requirements are absent. The identity is a structural analogue — an exact
internal law with the same algebraic form as E=mc², but without dimensions, dynamics,
observables, or predictions. It is correctly stated as: "the spine admits a conversion
law between two independently derived invariants."

---

## Preferred Language for External Statements

Instead of: *"energy / mass / speed of light"*

Use: *"amplitude budget / structural inertia or wobble loading / conversion factor of the spine"*

Instead of: *"E=mc² is derived in the spine"*

Use: *"the spine has an exact amplitude-wobble conversion law A = W·C*², which has the same algebraic form as E=mc² without a physical interpretation currently justified"*

Instead of: *"the corridor boundary is a speed limit"*

Use: *"the corridor boundary k=p is the algebraic edge of the prime field; its physical interpretation, if any, is not established"*

The Luther-ready formulation:

> The identity is exact, but its status must be stated carefully. Inside the Z/10Z spine,
> the universal mid-corridor amplitude 4/π² and the BHML wobble constant 3/50 determine
> an exact conversion factor 200/(3π²). The structure supports a clean internal law of
> the form amplitude = wobble × conversion. What is not yet justified is the physical
> naming of these terms as energy, mass, and c². That step would require dimensional
> analysis, observable definitions, and a bridge from corridor variables to physical units.
> The current result is best treated as a precise structural analogue of E=mc², not a
> physical derivation of it.

---

*Internal spine references: D3 (sinc²(1/2) = 4/π²), D22 (corridor portrait, W=3/50), D19 (generator selection).*
*Modulus comparison: A10_MODULUS_COMPARISON.md (W_n = 3/(CREATE_n × n), C*²_n = 2n²/(3π²)).*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
