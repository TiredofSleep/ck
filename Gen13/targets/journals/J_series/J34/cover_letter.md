# Cover letter — J34: F_p Extensions of CL_BHML: Universality Across Six Prime Fields

**To:** Editors, *Communications in Algebra*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *F_p Extensions of CL_BHML: Universality Across Six Prime Fields*

---

## Summary

We extend the F_p universality result of Sanders-Gish (J21, Algebra Universalis) — established for the canonical TSML 4-core algebra — to the parallel BHML substrate. Specifically, we verify that the 4-dimensional commutative non-associative algebra obtained by F_p-bilinear extension of the BHML composition table on the 4-core {0,7,8,9} has structurally invariant features (idempotent count = 4, eigenspace dimensions 1+3 and 2+2 under left-multiplication, |Aut(V)| = 40, power-associativity, 1-dimensional associator image) across all six primes p in {2, 3, 5, 7, 11, 13}. The chain-shell determinants of BHML_k for k in {4,5,6,7,8,9,10} are computed explicitly, with the BHML_8_YM = +70 = C(8,4) integer identity preserved. We conjecture extension to all primes p outside {2,5}.

## Why Communications in Algebra

- The paper extends a known F_p universality result to a parallel commutative non-associative algebra with distinct structural data; the central technique (F_p verification + automorphism-orbit count + eigenspace signature analysis) is a clean exercise in finite-field algebra.
- The result completes the F_p-universality picture for the lens family: TSML side (J21, prior submission) plus BHML side (this paper) give the field-invariance backbone for the three-substrate architecture (J31).
- The BHML_8_YM = C(8,4) determinant identity is a remarkable integer-arithmetic fact deserving documentation in a venue that reaches the commutative-algebra and finite-magma research communities.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J1-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

- J21 — *F_p Universality: The Operator-Substrate Construction over Prime Fields*, Algebra Universalis (TSML side, this paper extends to BHML)
- J33 — *The CL Forcing Axioms: A1-A9 Uniquely Force the Canonical Composition Lattice*, Algebraic Combinatorics (parent forcing framework)
- J31 — *The Three-Substrate Architecture*, Algebra Universalis (provides the BHML substrate definition)

## Reproducibility

Verification: the F_p check for each of p in {2, 3, 5, 7, 11, 13} is executed by the script `verify_discrete_dirac_4core.py` (mod-p arithmetic in the BHML version) in under one minute total. The full BHML 10x10 multiplication table is hardcoded in `Gen13/targets/foundations/lenses.py:BHML`; the 4-core restriction is the standard sub-table on indices {0, 7, 8, 9}.

## Suggested reviewers

- An expert in commutative non-associative algebras (axial-algebra/Griess-algebra researcher)
- An expert in finite-field algebraic structures and their universality
- An expert in F_p extensions of Z-defined multiplication tables

(Specific names available on request from the corresponding author.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Per-venue cap note

This is the second paper from this research program targeting *Communications in Algebra* (after J22, *Galois D_4 over LMFDB 4.2.10224.1*). Per-venue cap is 1/quarter; the venue is within budget.

---

Sincerely,
B.R. Sanders
