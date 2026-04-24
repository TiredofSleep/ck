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
associated with the Coherence Lattice (CL) 10×10 composition table — whose
Hilbert function $(1, 10, 6, 6, 6, \ldots)$ and Stanley-Reisner companion
sit near, but outside, Mantero's published framework (the companion is
*pure but not matroidal*).

This branch collects the bridge material: the object stated in Mantero's
vocabulary, the associated Lie-algebraic structure (WP11 so(8) = D₄,
WP12 so(10) = D₅), runnable verifications, and a planned MathOverflow
post that poses a narrow, community-facing commutative-algebra question
about pd(A) and the Koszul property of A = R/I.

## Commitments on record (public, not private)

- **MathOverflow post** on projective dimension and Koszul property of the
  binomial ideal above, framed using the Hilbert function and the 10×10
  table. Draft lives at
  [`papers/sprint_20260423_full/09_mathoverflow_post/DRAFT_MATHOVERFLOW_POST.md`][mo-draft]
  on this branch. Posted link will be appended to this file when live.

[mo-draft]: ../09_mathoverflow_post/DRAFT_MATHOVERFLOW_POST.md

## What is NOT in this file

- Private email bodies.
- Direct quotes from Dr. Mantero.
- Strategy notes about the relationship.

If you are Dr. Mantero and are reading this because the MathOverflow link
was sent to you: welcome. The directly relevant files on this branch are

- the MathOverflow draft above (the focused question),
- `papers/wp11/WP11_SO8_IDENTIFICATION.md` (so(8) = D₄ identification paper),
- `papers/wp12/WP12_SO10_IDENTIFICATION.md` (so(10) = D₅ companion + verification scripts),
- `papers/mantero_bridge/` (research notes on the bridges between your published work and the CL object).

Everything else on this branch exists to support the bridge.
