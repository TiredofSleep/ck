# Cover letter — J15: Galois D_4 over LMFDB 4.2.10224.1: Number-Field Identification of the Four-Core Attractor

**To:** Editors, *Communications in Algebra*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Galois D_4 over LMFDB 4.2.10224.1: Number-Field Identification of the Four-Core Attractor*

---

## Summary

We extract and present in self-contained form the Galois-theoretic content of the four-core attractor identified in J02 (already submitted to *Algebraic Combinatorics*). The unique interior fixed point of the symmetric-mixing fuse iteration F_{1/2} on a four-element fusion-closed sub-magma of Z/10 has its coordinate ratio ξ* = r/β characterized as the unique positive real root of the irreducible monic integer quartic x^4 + 4x^3 - x^2 + 2x - 2. The Galois group over Q is the dihedral group D_4 of order 8; the number field K = Q[x]/(f) is the catalogued LMFDB 4.2.10224.1, with discriminant -10224, class number 1, signature (2,1). The number field is catalogued and not new; what is novel is the route — a quartic D_4 field arising as the ring of definition for the fixed-point coordinates of a symmetric-mixing iteration on a four-element fusion-closed sub-magma of Z/10.

## Why Communications in Algebra

- Subject fit: explicit Galois-group computation, irreducibility argument, number-field identification with LMFDB — all squarely within Comm Algebra's scope.
- The result is fully self-contained in 12 pages, with verification reduced to two-line sympy computations (`sympy.factor(f, extension=[sqrt(-71)])` and `sympy.factor(f, extension=[sqrt(3)])`).
- The combinatorial origin of the quartic — as the algebra of fixed-point coordinates of a fuse iteration on a finite magma — is unusual and worth recording as a "new route to a known field" entry in the literature.

## Companion submissions

- J02 (*Algebraic Combinatorics*) — Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on Z/10Z. The four-core paper from which the present Galois content is extracted.

## Reproducibility

Verification: `sympy.factor(f, extension=[sqrt(-71)])` confirms D_4 (single irreducible factor); `sympy.factor(f, extension=[sqrt(3)])` confirms the explicit factorization in Q(√3)[x]; LMFDB cross-check via Tschirnhaus reduction x ↦ -x - 1 to the canonical defining polynomial x^4 - 7x^2 - 12x - 8 of LMFDB 4.2.10224.1. All checks run in <5 seconds with `sympy` as the only external dependency. Scripts deposited alongside J02 at https://github.com/TiredofSleep/ck/tree/tig-synthesis.

## Suggested reviewers

- A specialist on Galois groups of low-degree polynomials (resolvent-cubic classification, Cohen-style computational number theory).
- A specialist on small-discriminant quartic fields and the LMFDB catalogue.
- A specialist on number fields arising from finite-magma / dynamical-system fixed points (a small but distinctive niche).

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
