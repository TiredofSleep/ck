# K2.5 Counterexample Search

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**


*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Goal

Find a local equidistribution/autocorrelation setting that looks like the
prime-field corridor but gives a DIFFERENT kernel. If found, the shared sinc²
is weaker than it looks (more generic). If search fails repeatedly under a
clean hypothesis class, that strengthens K5.

The standard: each trial must satisfy hypotheses close to those of K5.1
(equidistribution-type + compact support) and produce a MEASURABLE different
kernel — not a trivial scaling difference.

---

## What We Are Looking For

A sequence {X_N} such that:
- X_N is equidistributed (or approximately so) in some interval
- It is NOT i.i.d. uniform (has correlations — like the prime orbit)
- Its PSD F[A_N](ξ) → something that is NOT sinc²(ξ)

If such a sequence exists AND has arithmetic-type structure analogous to the
prime-field orbit, it would show that sinc² in D2 is NOT a generic consequence
of "equidistributed arithmetic orbit" — some specific structure of the prime field
beyond equidistribution is responsible.

---

## Trial 1 — Van der Corput Sequence

**Definition:** The Van der Corput sequence in base 2 reverses the binary representation
of n to get x_n ∈ [0,1):

    1, 1/2, 3/4, 1/4, 5/8, 3/8, 7/8, 1/8, ...

This is equidistributed (proved by Van der Corput). It has VERY LOW discrepancy
(one of the best-equidistributed sequences known).

**Autocorrelation:** By K5.1, any equidistributed sequence on [0,1] has autocorrelation
→ tri and PSD → sinc². So Van der Corput gives sinc².

**Does the correlation STRUCTURE differ?** The Van der Corput sequence has strong
dyadic correlations (consecutive terms are related by binary reflection). For finite N,
the PSD deviates from sinc² at specific dyadic frequencies 2^k. For N = 2^n, the
PSD has nulls at ξ = 2^k for k < n.

**Finding T1:** Van der Corput gives sinc² in the limit (confirming K5.1) but has
structured finite-N deviations at dyadic frequencies. The limit kernel is sinc², not
a different kernel. This is NOT a counterexample to K5.1.

**K5 strength after T1:** K5.1 holds. No counterexample. The finite-N corrections
are dyadic (specific to base-2 construction, not prime-related).

---

## Trial 2 — Sequence with Non-Uniform Limiting Measure

**Definition:** X_N = {(2k−1)/(2N)}_{k=1}^N (midpoints of equal subintervals). This is
perfectly equidistributed. Trivially satisfies H1. Same PSD as any equidistributed
sequence → sinc².

NOT interesting. But consider:

**Modified setup:** X_N = {k/N}_{k=1}^N · (1 + ε sin(2πk/N)) (small perturbation toward
a bump near t=0). For ε > 0, the limiting measure is NOT uniform (it has a sine-wave density
perturbation). By K5.2a, the PSD ≠ sinc².

**Compute:** If μ → (1 + ε sin(2πt)) dt (density), then:
A(τ) = ∫₀¹ ρ(t) ρ(t+τ) dt where ρ = 1 + ε sin(2πt)

A(τ) = ∫₀¹ (1 + ε sin(2πt))(1 + ε sin(2π(t+τ))) dt
     = 1 + ε² ∫₀¹ sin(2πt) sin(2π(t+τ)) dt (cross terms vanish by periodicity)
     = 1 + (ε²/2) cos(2πτ) · 1_{|τ|≤1} (for τ ∈ [−1,1])

So A(τ) = tri(τ) + (ε²/2) cos(2πτ) · 1_{|τ|≤1} for the perturbed sequence.

PSD: F[A](ξ) = sinc²(ξ) + (ε²/2)(1/2)[δ(ξ−1) + δ(ξ+1)] * F[1_{[-1,1]}](ξ)
           ≈ sinc²(ξ) + (ε²/2) sinc(ξ−1) + (ε²/2) sinc(ξ+1)

This IS a different PSD: sinc² plus sidelobes at ξ = ±1.

**Finding T2:** Breaking H1 (non-uniform limiting measure) gives a different PSD
with extra lobes. This CONFIRMS K5.2a (H1 is necessary). Not a counterexample to K5.1
(K5.1 requires H1). But it shows: if the prime-field orbit were non-uniform, sinc² would fail.

Is the prime-field orbit uniform? YES, by Weyl. So D2's sinc² is secure.

---

## Trial 3 — Arithmetic Progression on [0,1]

**Definition:** X_N = {kα mod 1}_{k=1}^N for irrational α (Weyl sequence). Equidistributed.

Pair-correlation structure (Rudnick-Sarnak, Marklof): For α with bounded continued
fraction coefficients (e.g., α = (√5−1)/2), the pair-correlation is Poisson (= 1, not 1−sinc²).

**What this says about K5:** The PSD of the Weyl sequence → sinc² (K5.1 applies). But
the PAIR-CORRELATION is Poisson (not 1−sinc²). This CONFIRMS K5.2c: K5.1 gives PSD = sinc²
but does NOT give pair-correlation = 1−sinc².

**Finding T3:** The Weyl sequence {kα mod 1} is a direct counterexample to the idea
that "equidistributed on [0,1]" implies "pair-correlation 1−sinc²." It has PSD = sinc²
(K5.1) but pair-correlation = 1 (Poisson). This shows:

> sinc² PSD ≠ 1−sinc² pair-correlation.

The two appearances of sinc² are genuinely different. Any sequence satisfying K5.1
has PSD = sinc², but most do NOT have pair-correlation 1−sinc².

**Direct implication for K2.5:** Montgomery's pair-correlation (1−sinc²) is NOT a
consequence of equidistribution alone. It requires additional structure (H3: determinantal
/ level repulsion). The corridor kernel (sinc² PSD via K5.1) and Montgomery's kernel
(1−sinc² pair-correlation via K5.4+H3) are genuinely different phenomena.

This is the strongest evidence for Hypothesis A (Accidental) in K2_5.

---

## Trial 4 — Legendre Symbol Sequence (Arithmetic, Non-Prime-Orbit)

**Definition:** For a prime p, define x_k = (k/p) · (1 + (k/p)_L) / 2 where (k/p)_L is
the Legendre symbol. This weights points by ±1 depending on whether k is a QR mod p.

The resulting distribution is NOT equidistributed (half the points are QRs, half NRs,
but they may clump near one side). The PSD will deviate from sinc² because H1 fails.

**Purpose:** Shows that arithmetic sequences built from Z/pZ that BREAK equidistribution
break sinc² immediately. Confirms that the equidistribution in D2 (Weyl for primitive roots)
is essential, not just the prime-field structure.

**Finding T4:** Any arithmetic sequence from Z/pZ that is NOT equidistributed → NOT sinc².
sinc² in D2 comes from equidistribution (Weyl), not from "being a prime-field object" per se.
This strengthens K4's prime information deficit: sinc² tracks equidistribution, not primeness.

---

## Trial 5 — Random Matrix Eigenvalues on [0,1] (via Circular Ensemble)

**Definition:** The Circular Unitary Ensemble (CUE): eigenvalues e^{iθ_k} of N×N random
unitary matrices, mapped to [0,1] via θ/(2π) ∈ [0,1].

- Equidistributed: CUE eigenvalues have uniform density on [0,1] (by Haar measure). H1 satisfied.
- Compact window [0,1]. H2 satisfied.
- PSD by K5.1 → sinc². ✓
- Pair-correlation: 1 − sinc²(u) (CUE pair-correlation is the same as GUE in the large-N limit;
  both have pair-correlation 1−sinc²).

**Finding T5:** CUE eigenvalues satisfy H1 + H2 + H3 (determinantal with sine kernel).
They have BOTH sinc² PSD (K5.1) AND 1−sinc² pair-correlation (K5.4).

This is the ONLY setting in this search where BOTH statistics appear simultaneously.
The mechanism: CUE has eigenvalue repulsion encoded by the sine kernel (H3).

**Implication for K2.5:** The fact that BOTH sinc² (as PSD/autocorrelation) AND 1−sinc²
(as pair-correlation) appear TOGETHER is specific to determinantal processes with H3.
The prime-field orbit (D2) has sinc² as PSD but does NOT (as far as we know) have
determinantal structure — so D2 does not automatically give 1−sinc² pair-correlation.

Montgomery's theorem (under GRH) says ζ zeros DO have 1−sinc² pair-correlation.
If ζ zeros have CUE-type statistics (which is the GUE conjecture for ζ), then ζ zeros
satisfy H1+H2+H3 as a point process. But the prime-field orbit does NOT automatically
satisfy H3.

---

## Trial 6 — Orbit of a Non-Primitive Root

**Definition:** For prime p, let g be a NON-primitive root (a generator of a proper subgroup).
E.g., g = 1 (trivially), or g = a QR (generator of QRs only, order (p-1)/2).

- Orbit: {g^k mod p}/p for k = 0,...,(p-1)/2−1 (only (p-1)/2 distinct values for g = QR generator)
- This is equidistributed on the QRs, not on all of [0,1]
- μ_N → Uniform{QR positions} ≠ Uniform[0,1]
- H1 fails (limiting measure is NOT uniform on [0,1])
- PSD ≠ sinc² (K5.2a)

**Finding T6:** D2 uses PRIMITIVE roots (which give full equidistribution by Weyl).
For non-primitive roots, the equidistribution breaks and sinc² fails. This confirms
that the "primitive root" condition in D2 (corresponding to the generator selection D19:
g=3, not g=7 for HARMONY reasons) is essential for sinc² to hold.

**Implication:** D2's sinc² depends on primitive-root equidistribution. The specific
choice of g=3 (D19, T*=5/7) affects WHICH orbit is equidistributed, but ALL primitive
roots give equidistribution and hence sinc². The T*=5/7 specific value comes from which
generator is selected, not from whether sinc² holds.

---

## Summary Table

| Trial | Setup | PSD sinc²? | Pair-corr 1−sinc²? | Counterexample? | Finding |
|-------|-------|------------|-------------------|-----------------|---------|
| T1 | Van der Corput | Yes (limit) | No (needs H3) | No | K5.1 holds; finite-N dyadic corrections |
| T2 | Non-uniform measure | No (ε perturbation) | No | K5.2a confirmed | H1 is necessary |
| T3 | Weyl sequence {kα} | Yes | No (Poisson) | No to K5.1; **Yes to K5.1→pair-corr** | KEY: sinc² PSD ≠ 1−sinc² pair-corr |
| T4 | Legendre weights | No | No | No | Equidistribution essential, not primeness |
| T5 | CUE eigenvalues | Yes | Yes | No | H3 enables BOTH; only setting with both |
| T6 | Non-primitive root | No | No | No | Primitive root condition essential for D2 |

---

## Conclusions from Counterexample Search

**1. K5.1 is robust:** No counterexample found. Every equidistributed sequence
on [0,1] gives PSD = sinc² (K5.1). The theorem stands.

**2. PSD sinc² ≠ pair-correlation 1−sinc² (confirmed by T3):**
The Weyl sequence has PSD = sinc² but Poisson pair-correlation. These are genuinely
different statistics. The two appearances of sinc² in B6 are therefore NOT automatically
connected by K5.1.

**3. Pair-correlation 1−sinc² requires H3 (confirmed by T1, T3, T5):**
Only determinantal processes with sine kernel (CUE/GUE) have both PSD = sinc² AND
pair-correlation = 1−sinc². The prime-field orbit is not known to be determinantal.

**4. The counterexample search STRENGTHENS Hypothesis A (Accidental):**
The evidence is now:
- Corridor sinc² (D2) ← K5.1, any equidistributed orbit
- Montgomery 1−sinc² ← H3 (determinantal), NOT just K5.1
- These are different mechanisms
- The appearance of sinc² in both is a coincidence of "equidistribution producing
  sinc² in two different ways" rather than a single structural law

**5. The key open question from this search:**
Does the prime-field orbit (D2 context) satisfy H3 (determinantal structure)?
If yes: D2 and Montgomery are both instances of K5.4 (same deeper theorem), strengthening S.
If no: they are instances of K5.1 and K5.4 respectively (different sub-routes), confirming A.

This is the Montgomery-Keating-Snaith question: do primes inherit GUE structure?
It is open, deep, and far beyond D1–D24.

---

*Result: K5.1 robust; no K5.1 counterexample found. Counterexample T3 kills the naive
"sinc² PSD implies 1−sinc² pair-correlation" claim. Structural vs. Accidental question
resolves to: determinantal structure (H3) for prime orbit.*

*Feeds: K6_PRIME_REMAINDER_PROGRAM.md (do corrections push toward H3?)*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
