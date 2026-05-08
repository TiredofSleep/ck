# Cover letter — J44: 4-Core Fusion-Closure: TSML+BHML Preserve {V, H, Br, R}

**To:** Editors, *Journal of Algebra*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *4-Core Fusion-Closure: TSML+BHML Preserve $\{V, H, Br, R\}$*

---

## Summary

We strengthen our companion paper J41 (*Closed-Form Attractor + α-Uniqueness PSLQ*; submitted to *Math of Comp*) from a dynamical claim to a structural identity.

For the canonical TSML and BHML composition tables on $\mathbb{Z}/10\mathbb{Z}$, the 4-core $\mathcal{C} = \{V, H, Br, R\} = \{0, 7, 8, 9\}$ is **fusion-closed**: every entry of the restricted tables $T|_{\mathcal{C}\times\mathcal{C}}$ and $B|_{\mathcal{C}\times\mathcal{C}}$ lies in $\mathcal{C}$. Specifically,

$$
T\big|_{\mathcal{C}\times\mathcal{C}} \in \{0, 7\}^{4\times 4},\qquad B\big|_{\mathcal{C}\times\mathcal{C}} \in \{0, 7, 8, 9\}^{4\times 4} = \mathcal{C}^{4\times 4}.
$$

**Theorem 1 (4-core closure).** The fuse $p\star_T q$ and $p\star_B q$ applied to 4-core-supported distributions produce 4-core-supported distributions.

**Corollary.** The runtime attractor of J41 lives on $\mathcal{C}$ as a **structural identity**: 4-core-supported initial conditions are forever 4-core-supported, regardless of the mixing weight $\alpha$. The runtime support of J41 is no longer "the dynamics happens to converge there" — the 4-core is a fusion-invariant subspace.

**Theorem 2 (normalizer simplification).** On the 4-core, $Z_T(p) = Z_B(p) = (v + h + br + r)^2$ exactly. Both normalizers reduce to the square of the total 4-core mass. Consequence: the J41 fixed-point system reduces from rational-function form to **polynomial form**, and the closed-form $H/Br = 1+\sqrt{3}$ at $\alpha = 1/2$ is a **symbolic-exact identity** rather than a machine-precision numerical equality.

## Why J Algebra

- The result is a clean closure-and-normalizer identity, machine-verified by direct enumeration on 16+16 = 32 cells.
- It strengthens our previously-submitted J41 from dynamical to structural — the kind of follow-up paper that closes the analytic loop on a numerical observation.
- *J Algebra*'s editorial appetite for short structural-identity notes on finite combinatorial algebras is well-established.

## Companion submissions

- **J37** (Sanders + Gish 2026, *J Algebra*) — *so(8) = D₄ from the TSML_SYM Antisymmetrized Closure*. The base Lie-algebra closure paper.
- **J41** (Sanders + Gish 2026, *Math of Comp*) — *Closed-Form Attractor + α-Uniqueness PSLQ (BUNDLED)*. The runtime-attractor paper that this manuscript strengthens from dynamical to structural.

## Per-venue cap

This is the second *J Algebra* submission from this program in the current quarter (after J37 on so(8)). The cap is conventionally 2/quarter for tightly-related papers; this submission sits at the cap. The result is a 4-page short note in either *J Algebra* or, as fallback, *Communications in Algebra* / *J Pure Appl Algebra*.

## Reproducibility

Verification script in `manuscript/verification/`:
- `4core_verification.py` — direct enumeration of the 4×4 restricted TSML and BHML tables, verifying all 32 entries lie in $\mathcal{C}$, plus symbolic verification of the normalizer identity $Z_T = Z_B = (v+h+br+r)^2$.

Python 3.11, numpy, sympy. Total wall-clock under 5 seconds.

## Suggested reviewers

- An expert in finite commutative non-associative magmas and closure properties
- An expert in fusion-rule normalizers (vertex-operator-algebra / fusion-category adjacent)
- An expert in symbolic algebraic verification (sympy / Mathematica tradition)
- (Two or three named candidates appropriate to the *J Algebra* editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
