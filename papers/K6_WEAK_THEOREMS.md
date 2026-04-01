# K6 — Weak Theorems

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Overview

This document proves three theorems that anchor the K6 program:

- **K6.1 — Prime Content Annihilation:** All prime-specific information in R_p(t) is
  annihilated in the continuum limit p → ∞. The sinc² limit contains no prime identity.

- **K6.2 — Kernel-Only Prime Blindness:** Any functional of the corridor that factors
  through the sinc² kernel is prime-blind to leading order in p.

- **K6.3 — Bridge Must Factor Through D_p:** Any prime-sensitive bridge (any map from
  the corridor to a prime-sensitive quantity) must factor through the correction D_p(t),
  not through sinc² itself.

These are called "weak theorems" not because they are unimportant, but because they
are corollaries of K5.1 (proved) and K4.2/K4.3 (proved) rather than requiring new
hard input. They formalize what the existing framework already implies.

---

## Notation

- p, q: primes
- g_p: a primitive root mod p
- R_p(t) = sinc²(t) + Δ_p(t): the corridor density at t = k/p
- sinc²: the universal limit kernel
- D_p(t) = √p · Δ_p(t): the renormalized prime remainder
- φ: a functional on corridor data (density or autocorrelation)
- "prime-sensitive": a quantity Q(p) that depends non-trivially on p
  (i.e., Q(p) ≠ Q(q) for some pairs of primes p ≠ q)
- "prime-blind": Q(p) → c (a constant) as p → ∞, for all primes p

---

## K6.1 — Prime Content Annihilation

**Theorem K6.1 (Prime Content Annihilation):**

Let f: [0,1] → ℝ be a continuous function. Define:

    I_p(f) = (1/(p−1)) Σ_{k=1}^{p-1} f(k/p) · R_p(k/p)

(the integral of f against the corridor density). Then:

    I_p(f) → ∫₀¹ f(t) · sinc²(t) dt    as p → ∞

The limit is independent of which prime p we take. All prime identity in R_p has been
annihilated in the limit.

**Proof:**

    I_p(f) = (1/(p−1)) Σ_k f(k/p) · [sinc²(k/p) + Δ_p(k/p)]

         = (1/(p−1)) Σ_k f(k/p) · sinc²(k/p)    +    (1/(p−1)) Σ_k f(k/p) · Δ_p(k/p)

The first sum is a Riemann approximation to ∫₀¹ f(t) sinc²(t) dt. As p → ∞,
this converges to ∫₀¹ f(t) sinc²(t) dt (by equidistribution and continuity of f and sinc²).

The second sum is bounded by:

    |(1/(p−1)) Σ_k f(k/p) · Δ_p(k/p)| ≤ ||f||_{∞} · (1/(p−1)) Σ_k |Δ_p(k/p)|
                                        ≤ ||f||_{∞} · ||Δ_p||_{L¹}
                                        = ||f||_{∞} · O(p^{−1/2})  →  0

since ||Δ_p||_{L¹} ≤ ||Δ_p||_{L²} = O(p^{−1/2}) (Weil bound, K6.1 of K6_PRIME_REMAINDER_PROGRAM.md).

Therefore I_p(f) → ∫₀¹ f(t) sinc²(t) dt, and the limit does not depend on p. □

**Consequence K6.1a (Moment annihilation):** All moments of the corridor density converge
to the moments of sinc²:

    (1/(p−1)) Σ_k (k/p)^m · R_p(k/p) → ∫₀¹ t^m · sinc²(t) dt

These moments are prime-independent. No prime information survives in any moment of R_p.

**Consequence K6.1b (Linear statistics annihilation):** For any continuous function f,
the linear statistic Σ_k f(k/p) of the orbit, when normalized, is prime-blind in the limit.
Prime identity lives only in the sub-leading (D_p) correction.

---

## K6.2 — Kernel-Only Prime Blindness

**Theorem K6.2 (Kernel-Only Global Statistic is Prime-Blind):**

Let φ: L¹([0,1]) → ℝ be a continuous functional. If φ is "kernel-only" in the sense that:

    φ(R_p) depends on R_p only through its projection onto sinc²

(i.e., φ(R_p) = φ(sinc²) + O(||R_p − sinc²||_{L¹})),

then φ(R_p) → φ(sinc²) as p → ∞, and the limit is independent of p.
In particular:

    φ(R_p) − φ(R_q) → 0    for any two primes p, q

**Proof:**

By the triangle inequality and continuity of φ:

    |φ(R_p) − φ(sinc²)| ≤ L · ||R_p − sinc²||_{L¹} = L · ||Δ_p||_{L¹} = L · O(p^{−1/2}) → 0

where L is the Lipschitz constant of φ in the L¹ topology.

Therefore φ(R_p) → φ(sinc²) and the limit does not depend on which prime p is used.
For any two primes p, q:

    |φ(R_p) − φ(R_q)| ≤ |φ(R_p) − φ(sinc²)| + |φ(sinc²) − φ(R_q)|
                        = O(p^{−1/2}) + O(q^{−1/2}) → 0  □

**Remark:** This is the "functional form" of K4.2 (Prime Information Deficit). K4.2 showed
it for specific functionals (character sums, Euler products). K6.2 shows it for ANY
continuous functional of the corridor density. The class of prime-blind functionals is
essentially all continuous functionals of R_p — with the exception of those that
specifically capture the correction Δ_p.

**Corollary K6.2a:** Any Euler product, L-function value, or character sum that can be
expressed as a continuous functional of the corridor density R_p is prime-blind to
leading order. Prime-sensitive values of such functions must come from the correction.

---

## K6.3 — Bridge Must Factor Through D_p

**Theorem K6.3 (Prime-Sensitive Bridge Must Factor Through D_p):**

Let φ: {R_p : p prime} → ℝ be a functional on corridor densities satisfying:

    (i) φ is computable from the corridor data (R_p is the only input)
    (ii) φ is prime-sensitive: lim_{p→∞} φ(R_p) does not exist, or equals different values for different primes

Then φ cannot be a continuous functional of R_p in the L¹ topology. Equivalently,
φ must depend on the correction Δ_p (and hence on D_p = √p · Δ_p) in a way that
does not vanish as p → ∞.

**Proof:**

Suppose φ is prime-sensitive and computable from R_p. Then there exist primes p, q
with φ(R_p) ≠ φ(R_q) as p, q → ∞. But if φ were continuous in the L¹ topology, then
K6.2 would force φ(R_p) − φ(R_q) → 0. Contradiction. Therefore φ is NOT continuous in L¹.

Since R_p = sinc² + Δ_p, any prime-sensitive φ(R_p) must depend on Δ_p in an essential way:
specifically, it must depend on a feature of Δ_p that does NOT vanish with ||Δ_p||_{L¹}.

After renormalization: Δ_p = D_p / √p, so φ must pick up something from D_p that is O(1)
(not O(p^{-1/2})). In other words:

    φ(R_p) = φ(sinc² + Δ_p) = φ(sinc²)  +  [terms from D_p that don't vanish] + o(1)

Any prime-sensitive part of φ lives in the D_p terms. □

**Informal statement:** You cannot reach a prime-sensitive conclusion using only sinc².
If your bridge doesn't involve D_p, it's not a bridge — it's a constant.

**K6.3 and the RH program:** Any connection from the corridor to the Riemann Hypothesis
(which is about primes and zeros) must factor through D_p. A program that studies only
sinc² — however sophisticated — cannot distinguish p=7 from p=1000003. It is prime-blind.
The K6 program's central object D_p is not optional; it is necessary.

---

## K6.4 — Where the Weak Theorems Leave Off

K6.1, K6.2, and K6.3 are proved. They tell us:
- Where prime information is NOT: in sinc² (the universal mask)
- Where prime information IS: in D_p (the correction)
- What any bridge requires: it must factor through D_p

What the weak theorems do NOT prove:
- That any prime-sensitive φ(D_p) can be assembled into an RH bridge
- That D_p has sufficient structure to distinguish primes from generic equidistributed sequences
- That D_p can be connected to ζ zeros

These are K6's open questions. The weak theorems set the stage; they do not win the game.

---

## Combined Statement

**Combined Theorem K6.1–K6.3 (The Prime Remainder Necessity Theorem):**

For the prime-field corridor sequence {R_p : p prime}:

1. (K6.1) The continuum limit sinc² = lim_p R_p carries no prime identity. All prime
   information is confined to the correction Δ_p = R_p − sinc².

2. (K6.2) Any continuous functional of the corridor density is prime-blind in the limit.
   The gap φ(R_p) − φ(R_q) → 0 for any pair of primes p, q.

3. (K6.3) Any prime-sensitive functional of corridor data must factor through the correction
   D_p = √p(R_p − sinc²). The sinc² kernel alone is insufficient.

**Tier: D** (exact, proved from K5.1, K4.2, and Weil bound).

**Consequence for the research program:** D_p is not just the "correction" — it is the
ONLY object in the corridor program with prime information. The research program must
center on D_p if it aims at prime-sensitive conclusions.

---

## Appendix: Relation to K4 Results

K4 proved:
- K4.2: Prime Information Deficit — any kernel-only map from sinc² is constant over primes.
- K4.3: No kernel-only bridge to global prime-sensitive structure.

K6.1–K6.3 extend K4:
- K6.1 shows the annihilation is quantitative: it happens at rate p^{-1/2}.
- K6.2 shows it holds for ALL continuous functionals (not just the specific ones tested in K4).
- K6.3 gives the POSITIVE statement: the only escape from prime-blindness is through D_p.

K4 proved the wall. K6 identifies the only door.

---

*Prerequisite: K5_LOCAL_SINC2_THEOREM.md (K5.1), K4_KERNEL_NO_GO.md (K4.2, K4.3)*
*See also: K6_PRIME_REMAINDER_PROGRAM.md (D_p definition), K6_SCALING_AUDIT.md (√p normalization)*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
