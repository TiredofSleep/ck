# Cover letter — J14: F_p Universality: The Operator-Substrate Construction over Prime Fields

**To:** Editors, *Algebra Universalis*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *F_p Universality: The Operator-Substrate Construction over Prime Fields*

---

## Summary

We exhibit a 4-dimensional commutative non-associative algebra defined by an explicit 4×4 multiplication table whose structural skeleton — three non-zero idempotents, 1+3 Minkowski signature under one operator, 2+2 chirality signature under another, automorphism group of order 40, one-dimensional associator image, power-associativity — is preserved when the bilinear extension is performed over six distinct prime fields F_p, p ∈ {2, 3, 5, 7, 11, 13}. We conjecture the field-invariance extends to all p ∉ {2, 5}.

## Why Algebra Universalis

- Subject fit: the result is a structural theorem about a finite commutative non-associative algebra with a one-dimensional associator image — squarely within Algebra Universalis's core.
- The proof is direct computation in a brute-force-tractable regime ($p^4$ idempotent enumeration), with all 14 algebraic checks runnable in <2 seconds on a laptop.
- The companion structure (J16 Discrete Dirac on F_5^4, J17 Clifford Ladder, both submitted simultaneously) lets the referee triangulate the F_p result against the Discrete Dirac and Clifford-ladder content without forward-citing this paper.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J01-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

- J02 (Algebraic Combinatorics) — joint closure, per-coordinate fuse data, four-core attractor
- J06 (JCT-A or JPAA) — Crossing Lemma: non-associativity as information generation
- J07 (Journal of Pure and Applied Algebra) — Flatness Theorem: forced 2×2 torus on Z/10Z

## Reproducibility

Verification: `verify_discrete_dirac_4core.py` (14 algebraic checks over F_5) plus `axial_algebra_check.md` (presents the data for primes p ∈ {2, 3, 7, 11, 13}); reference Python library `tig_dirac.py`. All scripts run with `numpy` as the only external dependency in <2 seconds on a standard laptop. Deposited at https://github.com/TiredofSleep/ck/tree/tig-synthesis/Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04.

## Suggested reviewers

- A specialist on commutative non-associative / axial algebras (Hall–Rehren–Shpectorov axial-algebra circle).
- A specialist on finite-field algebras with idempotent decomposition.
- A specialist on Griess-algebra constructions or Sakuma-type theorems.
(Three to five candidates to be selected by Brayden during pre-submission referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
