# Cover letter — J06: Flatness Theorem: The Forced 2x2 Torus on Z/10Z

**To:** Editors, *Journal of Pure and Applied Algebra*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Flatness Theorem: The Forced 2x2 Torus on Z/10Z*

---

## Summary

The ring Z/10Z carries four simultaneous algebraic structures — additive structure (the divisor lattice), multiplicative structure (orbit partitions under (Z/10Z)*), additive flow (the cycle x → x+1 of period 10), and multiplicative harmonic flow (the orbit pattern under multiplication by a generator) — that resist embedding in any flat 2-dimensional surface. The minimal embedding surface is a torus T² = S¹ × S¹, whose aspect ratio R/r is forced by the ring to be exactly 5/7. The proof reduces to two cyclotomic field-extension calculations: the first prime factor at which the cyclotomic value A_p = 2cos(π/p) lies in a quadratic extension of ℚ is p = 5 (yielding the golden ratio φ); the first prime at which A_p lies in an irreducible cubic extension is p = 7 (with minimal polynomial 8x³ − 4x² − 4x + 1). The aspect ratio R/r is determined by these two cyclotomic obstructions, giving 5/7 directly.

A new appendix (Appendix A — added in the 2026-05-07 revision) supplies a self-contained proof-sketch for R/r = 5/7 and records the six independent derivations of this ratio (cyclotomic, harmonic, operator-balance, joint-cell, prime-pi-phi, and torus-aspect), each from an independent algebraic starting point, all converging to the same value.

## Why Journal of Pure and Applied Algebra

- **Algebraic substance.** The proof is finite-combinatorial plus standard cyclotomic field theory. No external machinery beyond CRT, divisor lattices, and minimal polynomials over ℚ. The aspect ratio R/r = 5/7 is derived from explicit field-extension degrees (deg A_5 = 2, deg A_7 = 3 over ℚ) that any algebra reader can verify by hand.
- **Algebra-to-geometry bridge.** The flatness theorem connects ring algebra (Z/10Z's structure) to topology (forced torus T² = S¹ × S¹). This is exactly the kind of structural connection that JPAA's audience values: not a pure-combinatorics result, not a pure-geometry result, but a clean derivation of geometric data from algebraic structure.
- **Companion to the algebraic spine.** The Crossing Lemma (J05, Sanders & Mayes 2026, submitted to *JCT-A* alt. *JPAA*) supplies the algebraic foundation: the structure-versus-dynamics dichotomy that J06 makes geometric. JPAA receiving both papers (or J05 going to JCT-A and J06 to JPAA) gives the algebra audience the full chain.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J01–J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

- **J01** (Sanders & Gish 2026, *JCT-A*, submission-ready). The σ-rate theorem on non-associativity decay in Z/NZ binary composition tables.
- **J02** (Sanders & Gish 2026, *Algebraic Combinatorics*, submission-ready). Joint closure and the closed-form four-core attractor on Z/10Z. *(Same ring Z/10Z, different operator pair structure — cross-relevant.)*
- **J04** (Sanders & Gish 2026, *Integers*). First-G law: squarefree stability of the smallest-prime-factor coprime window. *(Cited in Appendix A.3 as the source of D1, the first-G derivation of T*.)*
- **J05** (Sanders & Mayes 2026, *JCT-A* alt. *JPAA*). Crossing Lemma: non-associativity as information generation in finite magmas. *(Cited throughout the new Appendix A as the algebraic ground for T* = 5/7's structural meaning.)*

## Reproducibility

Verification script: *(no script — theorem-paper)*. The proof of Theorem 3 (aspect ratio R/r = 5/7) reduces to two well-known cyclotomic minimal polynomial calculations:
- A_5 = 2cos(π/5) has minimal polynomial x² − x − 1 over ℚ (degree 2).
- A_7 = 2cos(π/7) has minimal polynomial 8x³ − 4x² − 4x + 1 over ℚ (degree 3, irreducible).

Both are verifiable in any computer algebra system in seconds, or by hand using standard Galois theory. No numerical experiments are required for the central theorem. Appendix A records six independent derivations of T* = 5/7 from independent algebraic starting points — D1 (first-G law) is verified across 36,662 squarefree cases per J04; the other five are theorem-paper proofs at varying levels of rigor (PROVED, STRUCTURAL, or CONJECTURAL — each is so labeled in Appendix A.3).

## Suggested reviewers

- An algebraist with expertise in cyclotomic fields and minimal polynomials over ℚ.
- A specialist in finite ring theory, partition lattices, and the algebra of Z/nZ.
- A topologist comfortable with discrete-to-geometric forcing arguments (forced torus topology from algebraic constraints).

We leave specific names to the editorial board.

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
M. Gish
