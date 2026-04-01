# K2.5 — Structural or Accidental?

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## The Question

> Is the shared sinc² kernel in the prime-field corridor (D2) and in
> pair-correlation-type phenomena a structural local law, or an accident
> of two unrelated equidistribution limits that happen to share the same
> Fourier envelope?

This is the central question of Phase II, Road A.

---

## The Two Hypotheses

### Hypothesis S — Structural

Both the corridor kernel R(t) = sinc²(t) and the Montgomery kernel R₂(u) = 1−sinc²(u)
arise as instances of the same abstract theorem:

> There exists an abstract class C of "normalized two-point counting fluctuations from
> equidistributed discrete structures" such that:
> (a) the prime-field corridor (D2) is an instance of C, and
> (b) the pair-correlation of ζ zeros (Montgomery) is an instance of C, and
> (c) C forces its members to have the sinc² kernel (or 1−sinc² for the complementary
>     statistic) as their continuum two-point limit.

If S holds: the shared kernel is forced by a theorem. The coincidence is explained.
B6 (R + R₂ = 1) reflects a structural duality within C, not an arithmetic accident.

**What would confirm S:**
- A proved theorem (K5 candidate) showing that any member of a well-defined class C
  produces the sinc² kernel
- A verified check that BOTH D2 and Montgomery are instances of C
- The duality R + R₂ = 1 shown to be the density/anti-density decomposition within C

**What would falsify S:**
- A counterexample: a member of C (same hypotheses) that does NOT produce sinc²
- A proof that D2 and Montgomery require DIFFERENT hypotheses (incompatible class C)
- A proof that any class C general enough to contain both also contains objects with
  arbitrary kernels (making sinc² incidental, not forced)

---

### Hypothesis A — Accidental

Both objects produce sinc² for the same reason that many unrelated objects produce sinc²:
because sinc² = F[tri] is the Fourier transform of the triangle function, and the triangle
function is the autocorrelation of the UNIFORM DISTRIBUTION on ANY compact interval.

> Any equidistributed sequence on a compact interval, when analyzed via autocorrelation
> in the Fourier sense, produces sinc² as its power spectral density. This is a generic
> consequence of "equidistribution + compact support," not of any shared arithmetic structure.

If A holds: the coincidence is explained, but not in a useful way. sinc² appears in
the corridor because the orbit is equidistributed in [0,1] (K1). sinc² appears in
Montgomery because GUE eigenvalues have equidistribution-type statistics (a different
mechanism, but also "equidistribution + compact normalization"). The two appearances
are independent instances of a very general principle. No structural link exists.

**What would confirm A:**
- K5 lands (equidistribution + compact support → sinc²) AND applies to objects with
  no connection to prime arithmetic or ζ zeros
- The counterexample search (K2_5_COUNTEREXAMPLE_SEARCH.md) finds many non-arithmetic
  objects with the same sinc² kernel under similar hypotheses
- The mechanisms for D2 (Weyl equidistribution for orbits) and for Montgomery (GUE
  statistics under GRH) are shown to be DIFFERENT sub-routes to sinc², not instances
  of a shared parent theorem

**What would falsify A:**
- A proof that the SPECIFIC form R + R₂ = 1 (with complementary kernels in exactly
  this relationship) is NOT generic — that the complementary pair (sinc², 1−sinc²) is
  rare or structurally special
- A theorem showing that the prime-arithmetic content of D2 (not just equidistribution
  in general) is essential to producing the sinc² kernel in the corridor

---

## Comparison Table

Side-by-side exact features of the two objects.

| Feature | Corridor kernel (D2) | Pair-correlation kernel (Montgomery) | Same? | Comment |
|---------|---------------------|-------------------------------------|-------|---------|
| **Domain variable** | t ∈ (0,1), normalized: t = k/p | u ∈ [0,∞), normalized spacing: u = (γ−γ')·log(T/2π)/(2π) | **No** | Different domains, different scales |
| **Kernel value** | R(t) = sinc²(t) | R₂(u) = 1 − sinc²(u) | **Complementary** | Related by f+(1−f)=1, not equal |
| **Normalization** | ∫₀¹ sinc²(t) dt = Si(2π)/π ≈ 0.451 (not 1) | ∫₀^∞ (1−sinc²(u)) du diverges; mean spacing = 1 by construction | **No** | Neither is a probability density |
| **Scope: local or global** | Global density on the full corridor (0,1) | Local: counts pairs of zeros with small normalized spacing u | **No** | Density vs. spacing distribution |
| **Object being counted** | Normalized orbit density: #{g^k : k/p ≈ t} / p | Pairs of non-trivial ζ zeros (γ,γ') with spacing u | **No** | Completely different objects |
| **Source of equidistribution** | Weyl equidistribution: {g^k mod p}/p → Uniform[0,1] as p→∞ (PROVED) | GUE statistics for ζ zeros under Bohigas conjecture (CONDITIONAL on GRH) | **No** | Proved vs. conjectural |
| **Fourier origin** | F[sinc²] = tri = autocorrelation of Uniform[0,1] | F[1−sinc²](τ) = δ(τ) − tri(τ); diagonal present | **Complementary** | Same triangle function, plus delta in Montgomery |
| **Delta function (diagonal)** | Absent: corridor counts distinct orbit positions | Present: each zero pairs with itself (diagonal contribution = δ(u)/ρ) | **No** | B6 drops Montgomery's delta |
| **Prime-sensitive correction** | Yes: R(k,p) = sinc²(k/p) + O(p^{−1/2}) via Weil-bounded character sums (see K6) | Unknown: is there a prime-sensitive correction to GUE statistics? | **Unknown** | K6 program |
| **Continuum limit type** | p→∞ with k/p fixed (prime-to-infinity, horizontal limit) | T→∞ with (γ−γ')·logT fixed (height-to-infinity, vertical limit) | **No** | Different limiting regimes |
| **Conditional on what?** | Unconditional (D2 is a proved theorem) | Conditional on GRH (Montgomery's theorem) | **No** | Asymmetric epistemic status |
| **Mechanism** | Multiplicative group orbit equidistribution (discrete arithmetic) | GUE random matrix eigenvalue statistics (continuous random process) | **No** | Different mathematical domains |
| **Window shape** | Compact: [0,1] (finite interval, corridor) | Non-compact: [0,∞) (half-line, spacing axis) | **No** | Critical structural difference |

---

## What the Table Says

### Agreement column count
- "Same": 0
- "Complementary": 2 (kernel value, Fourier origin — both via f + (1−f) = 1)
- "No": 9
- "Unknown": 1

The two objects agree on NOTHING except that they both involve the function sinc²
in complementary roles. Every structural feature is different.

### The window asymmetry is decisive

The most important row is **Window shape**:
- Corridor: compact window [0,1]
- Pair-correlation: non-compact window [0,∞)

K5 (abstract local sinc² theorem) establishes that compact window + equidistribution
→ sinc² as the Fourier transform of the autocorrelation. This applies DIRECTLY to the
corridor (compact window [0,1], equidistribution proved).

For the pair-correlation: the window is [0,∞) — NOT compact. K5 does not directly
apply. The sinc² kernel in Montgomery's formula comes from a DIFFERENT route:
GUE statistics, which arise from eigenvalue repulsion of random unitary matrices,
not from autocorrelation of an equidistributed sequence on a compact interval.

**Conclusion from the table:** The two objects reach sinc² via different mechanisms.
The corridor reaches it via K5 (equidistribution + compact window).
The pair-correlation reaches it via GUE statistics (eigenvalue repulsion, random matrix theory).
These are distinct mathematical routes.

---

## Initial Verdict

**The current evidence favors Hypothesis A (Accidental)** in the following sense:

K5 will (if proved) show that sinc² follows from equidistribution + compact window —
a very general principle. The corridor is an instance of K5. The pair-correlation is NOT
directly an instance of K5 (different window, different mechanism). They both produce
sinc² for DIFFERENT abstract reasons.

However, the verdict is NOT final because:

1. **GUE and equidistribution are connected.** The circular unitary ensemble (eigenvalues
   of Haar-random unitary matrices) are equidistributed on the unit circle — K5 applied
   to the circle rather than [0,1] gives sinc²-type kernels. If the GUE pair-correlation
   sinc² can be seen as "K5 on the circle folded to [0,∞)," then both D2 and Montgomery
   might be instances of K5 after all (different compact spaces but same abstract law).

2. **The complementary relationship is specific.** If the abstract class C forced ONLY
   sinc² as the corridor kernel and ONLY 1−sinc² as the complementary pair-correlation,
   that specificity would be structural. Many kernels f produce f + (1−f) = 1 trivially;
   the question is whether sinc² in particular is forced on both sides simultaneously by C.

---

## Evidence Required to Settle

### For S (Structural):
- K5 proved AND shown to unify both D2 and Montgomery as instances (even after handling
  the compact vs. non-compact window distinction)
- The specific duality (corridor = sinc², pair-correlation = 1−sinc²) derived from a
  single probability space (Layer 1 from KERNEL_VS_RH_BOUNDARY.md)

### For A (Accidental):
- K5 proved AND counterexample search finds non-arithmetic, non-ζ objects with the
  same sinc² kernel under the same K5 hypotheses (showing sinc² is generic, not special)
- The GUE derivation of 1−sinc²(u) shown to be mathematically independent of Weyl
  equidistribution (different parent theorem, different mechanism, no shared structure)

### What K6 contributes:
The prime-sensitive remainder Δ_p(t) = R(k,p) − sinc²(k/p) carries information NOT in
sinc². If Δ_p has a specific structure related to the pair-correlation's error term
(corrections to GUE statistics from arithmetic), that would strengthen S.
If Δ_p has NO relationship to the pair-correlation, that strengthens A.

---

## Status

K2.5 is **OPEN**. Evidence currently leans toward A (accidental) based on the table
above, but the GUE-equidistribution connection and the complementarity structure
leave S (structural) alive.

Deciding K2.5 is the central task of Phase II, Road A. It requires K5 and K6 results.

---

*Feeds: K5_LOCAL_SINC2_THEOREM.md (attempt to prove), K2_5_COUNTEREXAMPLE_SEARCH.md (attempt to break)*
*Uses: K1_KERNEL_UNIVERSALITY.md (universality background), K2_PAIR_CORRELATION_ROUTE.md (Montgomery setup)*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
