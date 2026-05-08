# Cover letter — J08: The Sinc² Zero Law for Squarefree Moduli

**To:** Editors, *Integers — Electronic Journal of Combinatorial Number Theory*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Sinc² Zero Law for Squarefree Moduli*

---

## Summary

We submit a short note on a divisibility-controlled zero-set property of the squared sinc function on rational arguments with squarefree denominator. The basic biconditional sinc²(k/b) = 0 ⇔ b | k is recorded as a uniform-in-b lemma, and the squarefree-specific content is then extracted: for a squarefree integer b = p₁p₂…pᵣ with p₁ < … < pᵣ, the smallest positive k at which sinc²(k/d) = 0 for at least one non-trivial divisor d | b is exactly k = p₁ = spf(b). Three corollaries (layered loop closure, prime-indexed amplitude transitions, stability window of width p₁ – 1) follow immediately. The result is the sinc² shadow of the First-G Event Localization Theorem (companion paper J04, also submitted to *Integers*); the two papers share a verification script.

## Why Integers

- The paper is short, finite, and runnable: a two-page proof, four corollaries, and a verification script that completes in under five seconds. This matches the *Integers* scope of clean elementary number-theory results with electronic supplements.
- The squarefree re-scoping addresses a known triviality concern with the prime-only formulation (the basic biconditional is uniform in b), while preserving the genuinely prime-dependent content via the smallest-prime-factor structure.
- The result connects elementary divisibility theory to the Shannon/Montgomery sinc² literature at the level of basis functions (no claim of new analytic content beyond the algebraic localization).

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J01–J55) over Summer 2026. The paper most relevant as an already-submitted companion to this manuscript is:

- **J04 — Sanders & Gish, 2026**, *The First-G Event in the Coprimality Partition: Stability Windows, CRT Idempotent Count, and Prime-Indexed Phase Transitions* (submitted to *Integers*). The squarefree sinc² zero law is proved in J08 as the sinc² image of the algebraic First-G localization in J04. The two papers share the verification script `proof_first_g_event.py` for the multi-prime squarefree case; the present submission additionally verifies the single-prime squarefree case via `proof_d25_loop_closure.py`.

This is the second submission to *Integers* in this quarterly cap.

## Reproducibility

Verification script: `proof_d25_loop_closure.py` (supplied as electronic supplementary material). Runs in standard CPython with no external dependencies; verifies the prime case b = p for all primes p ∈ {3, 5, 7, …, 199} (46 primes, 4 distinct assertion blocks, zero exceptions) in under five seconds on a standard laptop. Uses `fractions.Fraction` and `sympy` for exact rational arithmetic on the rational input. The multi-prime squarefree case is verified by the companion script `proof_first_g_event.py` (in J04, all squarefree b ≤ 500, 36,662 (b, k) pairs, zero exceptions).

## Suggested reviewers

[3–5 candidates appropriate to *Integers*; to be filled at submission time. Suggested orientations: elementary number theory / sieve-of-Eratosthenes pedagogy; combinatorial number theory; signal-processing-flavored sinc² literature.]

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
M. Gish
