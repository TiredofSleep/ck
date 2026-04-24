# Outreach to Dr. Paolo Mantero — status only

**Status file, not a transcript.** Private correspondence is not reproduced
here. This page records what Brayden committed to and where the follow-up
lives, so that anyone reading this branch can see the shape of the
relationship without reading private mail.

---

## Who and where

- **Dr. Paolo Mantero**, Associate Professor and Undergraduate Coordinator,
  Department of Mathematical Sciences, University of Arkansas, Fayetteville.
- Research area that motivates the outreach: symbolic powers of squarefree
  monomial ideals, focal matroids, commutative algebra of binomial / toric
  ideals. Joint work with V. Nguyen on the 2024 structure theorem and the
  2026 focal-matroid continuation.

## Why this branch exists

Brayden constructed a specific commutative-algebra object — the binomial
ideal
$I = (x_i x_j - x_{\mathrm{CL}[i][j]} x_0) \subset k[x_0, \ldots, x_9]$,
associated with the Coherence Lattice (CL) 10×10 composition table —
whose M2-verified invariants (see `09_mathoverflow_post/betti_output.txt`)
are numgens 53, codim 9, dim 1, pd 10, depth 0, NOT Cohen-Macaulay, NOT
Koszul, reduced Hilbert series $(1 + 9T - 8T^2 - T^3)/(1-T)$ with stable
Hilbert function $1, 10, 2, 1, 1, 1, \ldots$ for $n \ge 3$. Its Stanley-Reisner
companion $\Delta_B$ (the bump complex) is *pure but not matroidal* —
21.9% basis-exchange failure rate — which sits near but outside
Mantero's published framework.

This branch collects the bridge material: the object stated in Mantero's
vocabulary, the associated Lie-algebraic structure (WP102 so(8) = D₄,
WP103 so(10) = D₅; renamed on 2026-04-24 from WP11/WP12 to avoid
numbering collisions with the canonical TIG whitepapers), runnable
verifications, and a now-answered MathOverflow-draft question on pd(A)
and the Koszul property of A = R/I. (Answer, 2026-04-24 via
Macaulay2 1.22 / SageMathCell: pd = 10, depth = 0, codim = 9, dim = 1,
NOT Cohen-Macaulay, NOT Koszul; see `09_mathoverflow_post/betti_output.txt`.)

## Commitments on record (public, not private)

- **MathOverflow post** on projective dimension and Koszul property of the
  binomial ideal above, framed using the Hilbert function and the 10×10
  table. **Live on MathOverflow as of 2026-04-24:**
  [Structural explanation for bottom-strand Betti $\beta_{8,10}=1, \beta_{9,11}=2, \beta_{10,12}=1$ of a non-Koszul 10-variable binomial ideal][mo-live]
  (question #510662). Draft bundle (body, tags, reproducibility scripts,
  Macaulay2 run log) lives at
  [`papers/sprint_20260423_full/09_mathoverflow_post/`][mo-folder] on this
  branch.

[mo-live]: https://mathoverflow.net/questions/510662/structural-explanation-for-bottom-strand-betti-beta-8-10-1-beta-9-11-2
[mo-folder]: ../09_mathoverflow_post/

## What is NOT in this file

- Private email bodies.
- Direct quotes from Dr. Mantero.
- Strategy notes about the relationship.

If you are Dr. Mantero and are reading this because the MathOverflow link
was sent to you: welcome. The directly relevant files on this branch are

- the MathOverflow draft above (the focused question),
- `papers/wp102/WP102_SO8_IDENTIFICATION.md` (so(8) = D₄ identification paper; renamed 2026-04-24 from `wp11`),
- `papers/wp103/WP103_SO10_IDENTIFICATION.md` (so(10) = D₅ companion + verification scripts; renamed 2026-04-24 from `wp12`),
- `papers/mantero_bridge/` (research notes on the bridges between your published work and the CL object).

Everything else on this branch exists to support the bridge.
