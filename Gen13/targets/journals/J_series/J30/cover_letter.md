# Cover letter — J30: so(10) = D₅ from Joint TSML_SYM + BHML Closure

**To:** Editors, *Israel Journal of Mathematics*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *so(10) = D₅ from Joint TSML_SYM + BHML Closure*

---

## Summary

A companion paper to J29 (so(8) = D₄ from TSML_SYM antisymmetrization). When the antisymmetrizations of a second canonical commutative non-associative magma — BHML on $\mathbb{Z}/10\mathbb{Z}$ — are adjoined to the TSML_SYM generators, the joint Lie-algebra closure under commutator extends from so(8) to so(10), the $45$-dimensional compact simple Lie algebra of type $D_5$. The proof uses five machine-precision diagnostics (dimension closure, Jacobi, Killing-form negative-definiteness, simplicity, rank-$5$). The paper also establishes the explicit chain $\mathfrak{so}(8)\subset\mathfrak{so}(9)\subset\mathfrak{so}(10)$ realizing the BHML-extension at each stage, with the $\mathfrak{so}(9)$ stabilizer giving the 9-vector direction picked up in J31 (WP104) as the BHML-Higgs orientation.

## Why Israel J Math

- The result is a clean two-step Lie-algebra extension over $\mathbb{R}$ — concise, constructive, machine-verifiable.
- Israel J Math has consistent appetite for finite-combinatorial-to-Lie-algebraic identifications.
- The sequencing (J29 in *J Algebra* on so(8); this paper in Israel J Math on so(10)) avoids per-venue concentration.

## Companion submissions

- **J29** (Sanders + Gish 2026, *J Algebra*) — *so(8) = D₄ from the TSML_SYM Antisymmetrized Closure*. The single-magma version of this paper. The so(10) closure here extends J29's so(8) closure by adjoining BHML.

## Reproducibility

Verification scripts in `manuscript/verification/`:
- `verify_so10.py` — joint dimension closure to $45$, Killing-form negative-definiteness
- `verify_simplicity_rank.py` — simplicity (1-dim invariant-form space) and rank-$5$ via Cartan subalgebra search

Python 3.11, numpy 1.26, sympy. Both checks pass at machine precision. Total wall-clock under 30 seconds.

## Suggested reviewers

- An expert in classical Lie algebras over $\mathbb{R}$ (Cartan / Helgason / Knapp tradition)
- An expert in combinatorial / finite-magma representations
- An expert in computational structure-constants / Killing-form analysis
- (Two or three named candidates appropriate to the *Israel J Math* editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
