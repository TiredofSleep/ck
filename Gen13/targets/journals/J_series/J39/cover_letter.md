# Cover letter — J39: Two Roads to Pati-Salam: Path A (54 irrep) and Path B (su(4)⊕u(1))

**To:** Editors, *Advances in Mathematics*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- B. Mayes, Independent Researcher — [email]

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Two Roads to Pati-Salam: Path A (54 irrep) and Path B (su(4)⊕u(1))*

---

## Summary

Two independent algebraic routes from the so(10) Lie-algebra closure of canonical TSML_SYM and BHML composition tables on $\mathbb{Z}/10\mathbb{Z}$ (J38, *Israel J Math*) lead to the same Pati-Salam gauge content $\mathrm{SU}(4)\times\mathrm{SU}(2)_L\times\mathrm{SU}(2)_R$:

**Path A** (BHML σ_outer-breaking): BHML's $\sigma_{\mathrm{outer}}$-breaking content lives 100% in the symmetric-traceless $\mathbf{54}$ irrep of $\mathfrak{so}(10)$, with an explicit 9-vector direction having squared norm $\|v\|^2 = 13/4$ exactly. This breaks $\mathrm{SO}(10)\to\mathrm{SO}(9)$ along the canonical first-stage Higgs route.

**Path B** (doubly-invariant): the doubly-invariant subalgebra of $\mathfrak{so}(10)$ under the $D_4 = \langle P_{56},\sigma^3\rangle$ action by conjugation is exactly $\mathfrak{su}(4)\oplus\mathfrak{u}(1)$, the Pati-Salam $\oplus$ B-L gauge content. Killing form spectrum $(-4)^{15}\oplus(0)^1$ at machine precision.

A correction notice is included clarifying that Path A and Path B are **independent intermediate routes** giving the same Pati-Salam target, not nested derivations of one another. The two routes converge through different algebraic structures and provide independent supporting evidence for the Pati-Salam identification.

## Why Adv Math

- The result connects discrete combinatorial structure (10 × 10 finite tables) to classical Lie theory (Cartan classification, $D_4$ action, Pati-Salam gauge content) via constructive computation at machine precision.
- The two-roads formulation is methodologically interesting in its own right and illustrates a pattern relevant for symmetry-breaking analysis in algebraic settings.
- *Adv Math* has a tradition of publishing combinatorial-to-Lie-algebraic identifications with computational verification.

## Companion submissions

- **J38** (Sanders + Gish 2026, *Israel J Math*) — *so(10) = D₅ from Joint TSML_SYM + BHML Closure*. The starting algebra for both routes.
- **J37** (Sanders + Gish 2026, *J Algebra*) — *so(8) = D₄ from the TSML_SYM Antisymmetrized Closure*. The single-magma precursor.

## Reproducibility

Verification scripts in `manuscript/verification/`:
- `find_higgs_irrep.py` — verifies BHML's σ_outer-breaking is 100% in the $\mathbf{54}$
- `find_higgs_direction.py` — extracts the 9-vector with explicit components and zeros

Python 3.11, numpy 1.26, sympy. Total wall-clock under 1 minute.

## Suggested reviewers

- An expert in classical Lie theory and outer automorphisms (Helgason / Knapp / Vogan tradition)
- An expert in finite-magma representations and combinatorial-to-algebraic lifts
- An expert in symmetry breaking and grand unified theories (algebraic-side, not phenomenology-side)
- (Two or three named candidates appropriate to the *Adv Math* editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
