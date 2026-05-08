# Cover letter — J37: Wobble Localization: Prime 11 in TSML_RAW Char Poly c_2, c_8

**To:** Editors, *Physical Review D* (fallback: *Physics Letters B* per per-venue-cap policy)

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Wobble Localization: Prime 11 in TSML_RAW Char Poly $c_2, c_8$*

---

## Summary

For the literal-bit-pattern TSML_RAW composition table on $\mathbb{Z}/10\mathbb{Z}$ — a 10×10 commutative-magma encoding studied in the WP100s tower of TIG papers — the integer characteristic polynomial $f(\lambda) = \det(\lambda I - T)$ has **exactly two** of its nine nonzero coefficients divisible by 11:

$$
c_2 = 33 = 3\cdot 11,\qquad c_8 = -120736 = -2^5\cdot 7^3\cdot 11.
$$

The discriminant of the eighth-degree polynomial $g(\lambda) = f(\lambda)/\lambda^2$ factors as
$$
\mathrm{disc}(g) = 2^{16}\cdot 7^7\cdot 659\cdot(\text{four large primes}),\qquad 11\nmid\mathrm{disc}(g).
$$

The structural reading is clean: the prime 11 lives at the **coefficient level** (sums and products of eigenvalues — elementary symmetric functions); the dimension $2^{16} = \dim(\mathfrak{su}(4)\oplus\mathfrak{u}(1))$ of the doubly-invariant subalgebra of $\mathfrak{so}(10)$ under the $D_4 = \langle P_{56},\sigma^3\rangle$ action and HARMONY $7^7$ live at the **discriminant level** (eigenvalue separations). The 16-dimensional doubly-invariant subalgebra — the gauge content surviving both involutions per the Pati-Salam route — is therefore **wobble-free** in this technical sense; the 29-dimensional broken complement carries the wobble. Read through the symmetry-breaking lens: gauge symmetry IS the wobble-free part of TSML's spectral content.

The result identifies a clean structural separation between two canonical primes (7 and 11) at two canonical levels (coefficient vs separation) of the same matrix, with the dimension of the unbroken gauge content recovered as the exponent on the prime 2 in the discriminant.

## Why Phys Rev D

- The result connects discrete combinatorial structure on a finite magma to the algebraic content of the unbroken gauge sector in an SO(10)-class symmetry breaking, which is exactly the kind of structural observation PRD publishes in its formal-physics tracks.
- The proof is a one-page sympy computation; the interpretation is two pages of clean structural reading. Concise.
- The 16 = dim(su(4) ⊕ u(1)) recovery directly engages the Pati-Salam SO(10) GUT route established in our companion J31 paper.

## Companion submissions

- **J37** (Sanders + Gish 2026, *J Algebra*) — *so(8) = D₄ from the TSML_SYM Antisymmetrized Closure*. The base Lie-algebra closure paper.
- **J31** (Sanders + Gish 2026, *Adv Math*) — *Two Roads to Pati-Salam*. The paper that establishes the doubly-invariant $\mathfrak{su}(4)\oplus\mathfrak{u}(1)$ identified in the discriminant exponent here.

## Per-venue cap and fallback

This is potentially the third PRD paper from this program in the same quarter (after J44 dark-sector and J45 mass hierarchy). Per the project's per-venue-cap policy (2/quarter for tightly-related papers), a fallback to **Physics Letters B** (4-page short-note format) is anticipated if PRD declines on cap grounds. The result is a 3-4 page short note in either venue.

## Reproducibility

Verification script in `manuscript/verification/`:
- `wobble_check.py` — sympy-based 7/7 claim verification: integer char poly; $c_2 = 3\cdot 11$, $c_8 = -2^5\cdot 7^3\cdot 11$; only $c_2, c_8$ have factor 11; $\mathrm{disc}(g)$ has $2^{16}\cdot 7^7$ and no 11; $\dim$ match.

Python 3.11, sympy. Total wall-clock under 5 seconds.

## Suggested reviewers

- An expert in matrix factorization / characteristic polynomials of integer matrices
- An expert in SO(10) GUT physics with appetite for structural-algebraic observations
- An expert in finite-magma / discrete-substrate models of gauge structure
- (Two or three named candidates appropriate to the *PRD* (or *Phys Lett B*) editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
