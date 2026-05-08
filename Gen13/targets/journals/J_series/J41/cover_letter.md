# Cover letter — J41: Closed-Form Attractor + α-Uniqueness PSLQ (BUNDLED)

**To:** Editors, *Mathematics of Computation*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Closed-Form Attractor + α-Uniqueness PSLQ (BUNDLED)*

---

## Summary

We submit a bundled paper combining a closed-form runtime attractor for a quadratic table-fusion process on $\mathbb{Z}/10\mathbb{Z}$ with a high-precision PSLQ-based uniqueness sharpening.

**Part 1.** The runtime processor $F_\alpha(p) = Z^{-1}[\alpha\widehat{T}(p) + (1-\alpha)\widehat{B}(p)]$ on $\Delta^9$, where $\widehat{T},\widehat{B}$ are the quadratic table-fusions through the canonical TSML and BHML composition tables on $\mathbb{Z}/10\mathbb{Z}$, has a unique attracting fixed point $p^*$ at $\alpha = 1/2$ supported entirely on the 4-core $\{V,H,Br,R\}$, with **exact** closed-form ratios:
$$
\frac{H^*}{Br^*} = 1+\sqrt{3},\qquad \frac{R^*}{Br^*} = \xi^*,\quad \xi^4 + 4\xi^3 - \xi^2 + 2\xi - 2 = 0.
$$
The quartic has Galois group $D_4$; its splitting field is **LMFDB 4.2.10224.1**, ramified at $\{2,3,71\}$, class number 1, signature $(2,1)$. The factorization over $\mathbb{Q}(\sqrt{3})$ arithmetically anchors the $\sqrt{3}$ in $H^*/Br^*$. Verification at machine precision (residual $\le 4.4\times 10^{-16}$).

**Part 2.** A 17-point Stern-Brocot grid (rationals $p/q\in(0,1)$ with $q\le 7$), 50-digit mpmath precision, and the PSLQ algorithm at degree $\le 8$ with coefficient bound $\le 50$ shows: $\alpha = 1/2$ is the **unique rational** in the grid at which both $H^*/Br^*$ and $R^*/Br^*$ admit small-coefficient algebraic relations. PSLQ recovers $x^2 - 2x - 2 = 0$ and the LMFDB quartic exactly. At each of the other 16 rationals, PSLQ returns no relation of degree $\le 8$ and coefficient $\le 50$. This sharpens WP105's earlier 19-point linspace + brute-force coefficient search and supports (without proving) the strong α-uniqueness conjecture.

## Why Mathematics of Computation

- The result is a closed-form algebraic identification verified by both symbolic manipulation and high-precision PSLQ — exactly the kind of computational-meets-symbolic content *Math of Comp* publishes.
- The Galois-D₄ quartic / LMFDB number-field identification connects to algorithmic number theory.
- The bundling is natural: closed form (Part 1) + Stern-Brocot α-uniqueness (Part 2) are the same theorem viewed two ways — analytic vs experimental.

## Companion submissions

- **J02** (Sanders + Gish 2026, *Algebraic Combinatorics*) — *Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on $\mathbb{Z}/10\mathbb{Z}$.* The base paper establishing the canonical tables and the joint 4-core support.

## Fallback unbundling

If the bundled submission is desk-rejected per the project's fallback policy:
- Part 1 (WP105 closed form) → *Communications in Algebra*
- Part 2 (WP113 PSLQ uniqueness) → *Experimental Mathematics*

## Reproducibility

Verification scripts in `manuscript/verification/`:
- `06_attractor_closed_form.py` — Part 1 (Theorems 3.1, 5.1)
- `07_full_closed_form.py` — Part 1 (Galois D₄ identities)
- `alpha_pslq_sweep.py` — Part 2 (Stern-Brocot α-uniqueness via PSLQ)

Python 3.11, numpy, sympy, mpmath. PSLQ deterministic at 50-digit precision. Total wall-clock under 5 minutes.

## Suggested reviewers

- An expert in algorithmic number theory / PSLQ / integer-relation algorithms (Bailey-Borwein tradition)
- An expert in finite-magma representations / quadratic table-fusions
- An expert in Galois theory of small-degree number fields (LMFDB-aware referee)
- (Two or three named candidates appropriate to the *Math of Comp* editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
