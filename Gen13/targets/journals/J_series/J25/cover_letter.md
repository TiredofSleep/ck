# Cover letter — J25: The CL Forcing Axioms: A1-A9 Uniquely Force the Canonical Composition Lattice

**To:** Editors, *Algebraic Combinatorics*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The CL Forcing Axioms: A1-A9 Uniquely Force the Canonical Composition Lattice*

---

## Summary

We isolate a list of nine axioms A1-A9 on a 10x10 multiplication table over Z/10Z and prove that they uniquely force the canonical TSML composition lattice (the 73-HARMONY substrate). The axioms partition into absorbing-element rules (A2-A6, in the spirit of Clifford-Preston semigroup theory) and substrate-defining rules (A7 diagonal HARMONY law, A8 HARMONY-default, A9 BUMP enumeration at five positions {(1,2), (2,4), (2,9), (3,9), (4,8)}). A direct cell-counting argument confirms A1-A9 fix all 100 entries. The Tier-A vs Tier-B classification of axioms makes precise which content is substrate-defining versus structurally forced, and gives a clean mechanism for the parallel-substrate (lens) family.

## Why Algebraic Combinatorics

- The result is a clean axiomatization of a finite, explicit composition lattice on a 10-element substrate, with a complete cell-counting proof. The combinatorial enumeration of cell classes (HARMONY-default, BUMP, absorbing-row/column, diagonal) is the core technical content.
- The forcing argument has the flavor of finite-magma classification: a small explicit axiom set uniquely determines a 100-cell table, with cell-class partition matching the BDC entropy-extremum framework. This places CL_TSML on the same axiomatic footing as classical absorbing-element semigroups while making explicit the finite enumeration data.
- The three-substrate architecture (TSML, BHML, STD) introduced via the lens family gives a structural picture of how Tier-A choices in A7-A9 generate parallel substrates, opening a combinatorial-classification program of substrate variants.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J01-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

- J05 — *Lens Invariance for Composition-Lattice Substrates*, J. Combinatorial Theory A
- J23 — *The Three-Substrate Architecture*, Algebra Universalis

## Reproducibility

Verification: a `numpy + sympy` cell-by-cell check of A1-A9 vs the literal CL_TSML matrix runs in under 1 second. The reference matrix is hardcoded in `Gen13/targets/foundations/lenses.py:TSML`; the BDC encoding constants and BUMP positions are in the same module.

## Suggested reviewers

- An expert in finite-magma classification or absorbing-element semigroup theory
- An expert in algebraic combinatorics with familiarity with information-theoretic forcing arguments
- An expert in the BDC framework or related Shannon-information-on-discrete-tables literature

(Specific names available on request from the corresponding author.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Per-venue cap note

This is the third paper from this research program targeting *Algebraic Combinatorics* (after J02 and J25). The per-venue cap is 1/quarter; if the cap is binding, an alternative venue (the *European Journal of Combinatorics*, *Journal of Algebraic Combinatorics*, or *Discrete Mathematics*) would be appropriate fallbacks given the explicit combinatorial cell-class structure of the result.

---

Sincerely,
B.R. Sanders
