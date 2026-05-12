# Cover letter — J33: Closed-Form Algebraic Attractor + α-Uniqueness PSLQ (REVISED 2026-05-07)

**To:** Editors, *Mathematics of Computation*

**From:**
- B. R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *A Closed-Form Algebraic Attractor for a Quadratic Table-Fusion Process on $\mathbb{Z}/10\mathbb{Z}$, with $\alpha$-Uniqueness via PSLQ on a Stern-Brocot Grid.*

---

## Summary

We submit a single, unified result on a specific quadratic dynamical system on the probability simplex $\Delta^9 \subset \mathbb{R}^{10}$, defined by two integer composition tables $T, B$ on $\mathbb{Z}/10\mathbb{Z}$ (stated in full in §1.1). The result has two complementary parts.

**Part A (closed form, structural).** The 4-element subset $C = \{0, 7, 8, 9\}$ is jointly closed under both quadratic table-fusions $\widehat{T}, \widehat{B}$, by direct read-off of the 16 cells of each $4 \times 4$ submatrix (Lemma 2.1). The fixed point of $F_{1/2} = \tfrac{1}{2}(\widehat{T} + \widehat{B})$ on the 3-simplex $\Delta^3_C$ has, exactly:
* $h / \beta = 1 + \sqrt{3}$, derived from the BREATH coordinate equation by direct algebraic manipulation (§3.4),
* $r / \beta$ is the unique positive real root of $f(x) = x^4 + 4 x^3 - x^2 + 2 x - 2 = 0$, derived from the RESET coordinate equation by elimination of $\sqrt{3}$ via squaring (§3.5).

The Galois group of $f$ over $\mathbb{Q}$ is $D_4$, established via the resolvent cubic $R_3(y) = y^3 + y^2 + 16 y + 36 = (y + 2)(y^2 - y + 18)$ and the standard quartic-Galois classification (Theorem 4.1). The number field $\mathbb{Q}[\xi]/(f)$ is **LMFDB 4.2.10224.1**, with discriminant $-10224$, class number 1, signature $(2, 1)$; the LMFDB identification is verified by the explicit Tschirnhaus relation $h(-x - 1) = f(x)$, where $h$ is the LMFDB defining polynomial. The factorization
$$
f(x) = (x^2 + (2 - \sqrt{3}) x + (\sqrt{3} - 1))(x^2 + (2 + \sqrt{3}) x - (\sqrt{3} + 1))
$$
over $\mathbb{Q}(\sqrt{3})$ realizes the same $\sqrt{3}$ that appears in $h / \beta = 1 + \sqrt{3}$ (Corollary 4.2).

**Part B (PSLQ, complementary).** Across the 17-point Stern-Brocot grid $\mathcal{G} = \{p/q : 0 < p < q, q \le 7\}$ at 50-digit mpmath precision, the PSLQ algorithm (Ferguson--Bailey 1999) at degree $\le 8$ and coefficient bound $\le 50$ finds an integer-coefficient algebraic relation for both fixed-point ratios $R_h(\alpha) = h^* / \beta^*$ and $R_r(\alpha) = r^* / \beta^*$ at $\alpha = 1/2$ and at no other rational in $\mathcal{G}$. The relations recovered at $\alpha = 1/2$ are exactly the Galois-derived $x^2 - 2 x - 2$ and $f$ (Theorem 5.1).

Together, the two parts establish the **rationally-structured center** of the iteration at $\alpha = 1/2$: Part A proves rational structure exists at $\alpha = 1/2$; Part B is numerical evidence that no comparable rational structure exists (within the bounded PSLQ search) at the other 16 rationals of $\mathcal{G}$.

## Why Mathematics of Computation

* The result is a closed-form algebraic identification verified by symbolic manipulation (Galois-D₄ identification of the LMFDB-cataloged quartic) and high-precision empirical PSLQ — exactly the computational/symbolic balance that *Math. Comp.* publishes.
* The 4-core invariance is proven structurally from a 16-cell read-off (Lemma 2.1), not asserted from numerical iteration.
* The BREATH equation, the RESET quartic, and the Tschirnhaus map to the LMFDB defining polynomial are written out in the manuscript as explicit derivations, not folded into a verification script. The verification script confirms each derivation at machine precision.

## Revisions from the previous draft (per fresh-eyes referee report 2026-05-07)

This is a substantially-revised submission. The previous draft, which bundled a parallel research-program framing, is replaced by a single self-contained theorem. Specifically:

* The "TIG" framework, "lens scope" formalism, and references to companion papers (WP102-WP104) have been **excised**. The manuscript stands on its own, with the tables $T, B$ stated in full in §1.1.
* The proof of Theorem 3.1 (the closed form) has been **written out in the manuscript** rather than folded into the verification script — §3.4 derives the BREATH equation; §3.5 derives the RESET quartic.
* The 4-core invariance is now a **structural lemma** (Lemma 2.1) proved by the 16-cell read-off, not by empirical iteration.
* The α-uniqueness conjecture has been **weakened** from "transcendental over $\mathbb{Q}$" to "no algebraic relation of bounded degree and coefficient height" (Conjecture 5.2), to match the strength of finite-PSLQ evidence.
* The §Headline overstatement of 19-point sweep "uniqueness" has been replaced by Theorem 5.1 (Stern-Brocot, PSLQ-bounded), without the misleading 1-dimensional-continuum framing.
* The §4.3 "two D₄'s match" speculation has been removed.

The mathematical content (closed form, Galois identification, LMFDB number field, PSLQ uniqueness on the grid) is unchanged; the framing, the proof exposition, and the hand-picked-table acknowledgement are all rewritten for *Math. Comp.*'s audience.

## Companion submissions

J33 is presented as a stand-alone result. No companion paper is required for evaluation.

## Fallback unbundling

If the bundled submission is desk-rejected:
* Part A (closed-form attractor + Galois identification) → *Communications in Algebra*.
* Part B (PSLQ on Stern-Brocot grid) → *Experimental Mathematics*.

The two parts can be split using the same source material, since Part A is structural and Part B is computational.

## Reproducibility

Verification scripts in `manuscript/verification/`:
* `06_attractor_closed_form.py` — Part A: BREATH equation derivation, $h / \beta = 1 + \sqrt{3}$ at machine precision.
* `07_full_closed_form.py` — Part A: RESET quartic + LMFDB Tschirnhaus check at machine precision.
* `alpha_pslq_sweep.py` — Part B: 17-point Stern-Brocot grid + PSLQ at 50-digit precision.

Python 3.11+, numpy, sympy, mpmath. All checks deterministic; total wall-clock under 5 minutes (the Stern-Brocot sweep at 50 digits dominates). Tables $T, B$ inlined in each script (no external paths).

## Suggested reviewers

* An expert in algorithmic number theory / PSLQ / integer-relation algorithms (Bailey-Borwein lineage).
* An expert in Galois theory of small-degree number fields (LMFDB-aware).
* An expert in finite-magma representations and quadratic table-fusion dynamics.

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,

B. R. Sanders
