# Cover letter — J37: so(8) = D₄ from the TSML_SYM Antisymmetrized Closure

**To:** Editors, *Journal of Algebra*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *so(8) = D₄ from the TSML_SYM Antisymmetrized Closure*

---

## Summary

We prove that a finite combinatorial object — the canonical TSML_SYM composition table on $\mathbb{Z}/10\mathbb{Z}$ (a frozen $10\times 10$ commutative non-associative magma in upper-triangle authoritative symmetrization) — carries a natural Lie-algebraic lift to $\mathfrak{so}(8,\mathbb{R})$, the $28$-dimensional compact simple Lie algebra of type $D_4$. The lift is given by $A_i = L_i - L_i^\top$, the antisymmetrizations of the left-regular representations of the magma's flow indices $F=\{1,2,3,4,6,8\}$, and the proof is via four independent machine-precision diagnostics: dimension closure ($6\to 21\to 28$), Jacobi identity, Killing form negative definiteness, and simplicity (one-dimensional invariant-form space plus ideal-saturation). As $D_4$ is the unique simple Lie algebra with $S_3$ outer automorphism (triality), the result identifies the magma as a discrete combinatorial substrate carrying triality natively, with consequent embeddings $\mathfrak{so}(8)\supset\mathfrak{so}(7)\supset\mathfrak{g}_2\supset\mathfrak{su}(3)$ as standard Cartan-classification corollaries.

## Why J Algebra

- The result is a clean Lie-algebraic identification with explicit constructive proof at machine precision.
- The substrate is a finite combinatorial object (a $10\times 10$ table) — accessible to algebraists outside the specific application domain.
- The route uses standard tools (left-regular representations, antisymmetrization, Killing-form Cartan signature, ideal-saturation simplicity test) and produces a classical conclusion.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J1-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

- **J02** (Sanders + Gish 2026, *Algebraic Combinatorics*) — *Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on $\mathbb{Z}/10\mathbb{Z}$.* Establishes the canonical TSML_SYM and BHML tables jointly; provides 4-core closure and the closed-form $\alpha=1/2$ attractor that recurs in J41.
- **J32** (Sanders + Gish 2026, *Mathematical Intelligencer*) — *The Joint TSML+BHML Chain: Lens-Dependence at Size 7.* Establishes the joint sub-magma chain on which the so(8) and so(10) closures live.

## Reproducibility

Verification scripts in `manuscript/verification/`:
- `stage2_adjoint.py` — Jacobi identity (Lemma 3.2)
- `stage4_correct_closure.py` — Dimension closure $6\to 21\to 28$ (Lemma 3.1)
- `stage5_so8.py` — Killing form signature negative-definite (Lemma 3.3)
- `stage7_disambiguate.py` — Simplicity via invariant-form count + ideal saturation (Lemmas 3.4-3.5)

Python 3.11, numpy 1.26, sympy. All checks pass at machine precision (residual $\le 2\times 10^{-11}$ in all diagnostics). Total wall-clock under 1 minute on a standard laptop.

## Suggested reviewers

- An expert in finite-dimensional simple Lie algebras over $\mathbb{R}$ (Cartan classification, $D_4$ triality)
- An expert in commutative non-associative algebras / magma representations
- An expert in computational Lie theory / structure-constant verification
- (Two or three named candidates appropriate to *J Algebra*'s editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
