# Cover Letter — Integers Submission

**To:** Editors, Integers — Electronic Journal of Combinatorial
Number Theory

**From:** B. R. Sanders (corresponding author)
7Site LLC, Hot Springs, Arkansas, USA
brayden@7site.co

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** The First-G Event and a Discrete Sinc² Identity

**Co-author:** M. Gish (Independent Researcher, Hot Springs, AR)

---

## Summary

We submit for consideration in Integers a short note (≈10 pages)
combining two elementary results into a single synchronization
statement:

1. **First-G localization.** For an integer b > 1, the smallest
   alphabet size k at which {1,...,k} contains an element
   non-coprime to b is exactly k* = spf(b), the smallest prime
   factor of b. The proof is a one-line gcd argument.

2. **Discrete sinc² identity.** The squared modulus of the
   normalized finite exponential sum
   S(k,f) = (1/k) Σ_{j=1}^{k} e^{2πij/f}
   admits the closed form
   R(k,f) = sin²(πk/f) / (k² sin²(π/f)),
   a discrete relative of the Fejér kernel.

3. **Synchronization.** For f = p₁ = spf(b), the First-G event and
   the first integer zero of R(k, p₁) coincide at k = p₁: the
   arithmetic event "the alphabet first contains an obstruction
   modulo b" and the harmonic event "the unit-alphabet exponential
   sum at frequency 1/p₁ first vanishes" colocalize at the same
   integer.

4. **Continuum limit.** R(k,f) → sinc²(k/f) as f → ∞ along
   k/f → t fixed, identifying R(k,f) as a discrete approximant
   to the rectangular-pulse power spectrum.

## Why Integers

The note is short, elementary, and fits the Integers profile of
self-contained results in combinatorial number theory. We make no
claim of novelty for the closed-form identity itself (it is the
standard Fejér calculation specialized to rational arguments);
the contribution is the packaging — synchronizing the arithmetic
First-G event with the harmonic zero of a discrete sinc²-type
function in a single elementary statement valid for every b > 1
via f = spf(b).

The §8 Scope section makes explicit what the note does not claim:
no consequence for the Riemann hypothesis, no implication for prime
distribution beyond what the smallest-prime-factor function already
provides, and no consequence for cryptographic factoring difficulty.

## Companion submissions

Two companion papers with overlapping authorship are submitted
simultaneously to other venues:

- "Logarithmic Quintessence: A Dimensionless Scalar Dark Energy Model
  with an Analytic Vacuum"
  (submitted to JCAP)
- "Non-Associativity Decay in Binary Composition Tables over ℤ/Nℤ"
  (submitted to Journal of Combinatorial Theory, Series A)

The Integers paper is independent of both. The cross-references in
the bibliography exist for readers interested in the broader
foundational program. All three share Zenodo DOI 10.5281/zenodo.18852047.

## Reproducibility

A self-contained Python script verify_first_g.py is provided as
supplementary material. The script verifies the First-G localization
for every squarefree b in [2, 500] (305 values, 22,367 (b,k) pairs,
zero counterexamples), the closed form for R(k,f) at every prime
f ∈ {3,5,...,23} with maximum deviation below machine epsilon, the
synchronization at the canonical test set {10, 30, 35, 77, 105, 210,
1001, 2310}, and the continuum limit at t = 1/2 and t = 1/4 along
geometric scaling of f.

## Conflict of interest

The authors declare no competing interests. No funding was received
for this work.

---

Thank you for considering the manuscript.

Sincerely,
B. R. Sanders
