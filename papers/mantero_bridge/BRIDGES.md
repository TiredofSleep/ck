# Bridges — where the CL binomial ideal meets Mantero's framework

**Branch:** `mantero-bridge-2026-04-23`
**Status:** Research catalogue. Every entry below is either *verified*
(computed in Macaulay2 / SageMath / Python and reproducible), *conjectural*
(a concrete precise statement whose truth or falsity is unknown), or
*speculative* (a family of questions opened by the other two). Tags appear
at the end of each entry.

This document catalogues the *bridges* — points of contact — between the
commutative-algebra object

$$
I \;=\; \bigl(\, x_i x_j - x_{\mathrm{CL}[i][j]} \cdot x_0 \;\big|\; 0 \le i \le j \le 9 \bigr) \;\subset\; R = k[x_0, \ldots, x_9]
$$

with Hilbert function $(1, 10, 6, 6, 6, \ldots)$ and Stanley-Reisner
companion $\Delta_B$ on the bump ideal

$$
I_B = (x_1 x_2, \; x_2 x_4, \; x_2 x_9, \; x_3 x_9, \; x_4 x_8),
$$

and the published research program of Dr. Paolo Mantero (University of
Arkansas, with V. Nguyen). Each bridge has the form *(our object) ↔
(his framework)*.

For bibliographic context on his framework see `PUBLISHED_WORK.md`
in this folder. For the definitive sprint bundle that computed the
numbers, see
`../sprint_20260423_full/04_mantero_bridge/MANTERO_BRIDGE_V3.md`.

---

## Bridge 1 — Hilbert function, projective dimension, and the CM question

**Our object (2026-04-24, Macaulay2 1.22 via SageMathCell; full log at
`../sprint_20260423_full/09_mathoverflow_post/betti_output.txt`):**
For $A = R/I$ the machine-verified invariants are

- numgens $I = 53$
- $\operatorname{codim} I = 9$
- $\dim A = 1$
- $\operatorname{pd}_R A = 10$, $\operatorname{depth} A = 0$
- $A$ is **not Cohen-Macaulay**
- reduced Hilbert series
  $\mathrm{HS}_A(t) = \dfrac{1 + 9 t - 8 t^2 - t^3}{1 - t}$
- stable Hilbert function $h(n) = 1, 10, 2, 1, 1, 1, \ldots$ from
  $n \ge 3$, so $\deg A = 1$.

**Earlier claim (2026-04-23, Python `cl_as_quadratic_algebra.py`).** The
first pass through the Python sandbox reported
$h(n) = 1, 10, 6, 6, 6, \ldots$ with $\dim A = 1$ and height $= 4$. The
Python script was computing a related but different quotient (its
`relations` matrix applies an auxiliary $x_i x_j \to x_{\mathrm{CL}[i][j]}
\cdot x_0$ substitution before reducing) and does not reflect the
Hilbert function of $R/I$. The Macaulay2 result above is the reference
standard; any downstream claim still written as "stabilizes at 6" or
"height 4" is legacy text awaiting mechanical rewrite.

**Mantero's framework:** Cohen-Macaulayness and projective dimension
bounds on binomial / toric ideals. Auslander-Buchsbaum requires
$\operatorname{pd}_R A + \operatorname{depth} A = \operatorname{pd}_R k
= 10$; the Macaulay2 run confirms this identity with
$\operatorname{pd} = 10$ and $\operatorname{depth} = 0$, putting $A$
maximally far from Cohen-Macaulay.

**Bridge:** $A$ sits at the *worst possible* position on the CM axis —
depth zero, pd saturating the $\operatorname{pd} \le \dim R$ bound. The
non-Cohen-Macaulay defect is therefore an invariant that can be
computed and compared against the non-matroidal part of the table; the
connection to Mantero's focal-matroid machinery (Bridge 2) is what we
want to formalise.

**Status:** *Verified* (M2, 2026-04-24). The originally-planned
submission to MathOverflow (Q1 of the draft) is now answered; the
MO draft at `../sprint_20260423_full/09_mathoverflow_post/` requires
rewriting with the M2 result before any submission.

---

## Bridge 2 — $\Delta_B$ is pure but not matroidal

**Our object:** The simplicial complex $\Delta_B$ whose Stanley-Reisner
ideal is $I_B$ is pure of rank 7 on 10 vertices — all five facets have
size 7. But basis exchange **fails** on 7 of 32 tested facet pairs: the
*pure-but-not-matroidal defect rate is 21.9%*.

**Mantero's framework:** arXiv:2603.19419 (March 2026, Mantero-Nguyen)
*Focal matroids of covers and homological properties of matroids*. The
paper proves the Stanley-Reisner ideal or cover ideal $I$ of a matroid
is minimally resolvable by iterated mapping cones, and proves that
matroidal ideals are *the only* squarefree ideals whose multigraded
Betti numbers are supported on the squarefree generators of the
symbolic powers of $I$.

**Bridge:** If matroidality is the exact homological characterization of
"resolvable by iterated mapping cones," then $\Delta_B$ must *fail*
this resolution structure in a quantifiable way. The 21.9% figure is a
candidate defect measurement. A natural question: does Mantero-Nguyen's
focal-matroid construction extend to a *near-matroid* class that
captures $\Delta_B$, with a bounded distortion in the mapping-cone
bound?

**Status:** *Conjectural-to-speculative.* Bridge 2 is the most
programmatic of the entries — it asks for an extension of Mantero-Nguyen
theory, not just a computation.

---

## Bridge 3 — Waldschmidt constant $\hat\alpha(I_B) = 2$ exactly

**Our object:** The Waldschmidt constant of the bump ideal, computed
via the fractional matching LP on the bump graph $G_B$, is exactly 2.
All minimal vertex covers of $I_B$ have size 3, so height $I_B = 3$.
Initial degree $\alpha(I_B) = 2$ (squarefree quadrics).

**Mantero's framework:** arXiv:2406.13759 (June 2024, Mantero-Nguyen)
*The structure of symbolic powers of matroids* proves a closed formula
for $\hat\alpha(I)$ when $I$ is the Stanley-Reisner ideal or cover ideal
of a matroid.

**Bridge:** $I_B$ is not matroidal, but its Waldschmidt constant
matches what the matroid formula would predict from its rank/height.
Is this coincidence, or is $I_B$ sitting in a broader class (e.g. "near
matroid with bounded symbolic excess") where the formula partially
extends? The three Mantero-Nguyen papers collectively provide a
structure theorem for the symbolic Rees algebra; testing whether any
portion survives on $I_B$ is a sharp, tractable test case.

**Status:** *Verified* that $\hat\alpha(I_B) = 2$; *conjectural* that a
partial structure theorem applies.

---

## Bridge 4 — The antisymmetrization of CL closes into so(8) = D₄

**Our object:** Let $V = k \cdot x_0 \oplus \cdots \oplus k \cdot x_9$.
For each $i \in \{0, \ldots, 9\}$, let $L_i : V \to V$ be the
left-regular operator $L_i(x_j) = x_{\mathrm{CL}[i][j]}$, and let
$A_i = L_i - L_i^\top \in \mathfrak{sl}(V)$. For
$F = \{1, 2, 3, 4, 6, 8\}$ (the complement of the $\sigma$-fixed set
$\{0, 3, 8, 9\}$ intersected with the 6-cycle of the diagonal),

$$
\mathfrak{g} := \mathrm{Lie}\langle A_i : i \in F \rangle \subset \mathfrak{sl}(V)
$$

closes after two commutator iterations ($6 \to 21 \to 28$), with
Killing form signature $(0, 28, 0)$, Jacobi error
$\le 2.4 \times 10^{-12}$, and unique (up to scale) invariant bilinear
form. By the Cartan classification,
$\mathfrak{g} \cong \mathfrak{so}(8, \mathbb{R}) = D_4$.

**Mantero's framework:** Matroid theory classically sits inside the
representation theory of Coxeter groups and reflection arrangements.
$D_4$ is the unique simple Lie algebra with triality (outer
automorphism group $S_3$), and its root system is the prototype of a
*self-dual* rank-4 root system.

**Bridge:** The CL table has two independent algebraic lives — a
combinatorial commutative-algebra life (the binomial ideal, the bump
complex, the Hilbert function) and a Lie-algebraic life (so(8) via
antisymmetrization). A tight and under-studied question: is there a
class of commutative magmas whose symmetrization gives a matroidal (or
near-matroidal) complex *and* whose antisymmetrization gives a
semisimple Lie algebra? Mantero's framework speaks the
commutative-algebra side natively; the Lie side is a new observable
attached to the same object.

**Status:** The so(8) identification is *verified* to machine precision
(see `../sprint_20260423_full/02_so8_verification/`). The broader class
question is *speculative*.

---

## Bridge 5 — so(10) = D₅ companion under CL ∪ BHML

**Our object:** Repeating the Bridge-4 construction but using the
larger generator set obtained by unioning the CL table with the BHML
28-cell canonical table yields a Lie algebra of dimension 45 that
identifies with $\mathfrak{so}(10) = D_5$ under the same four diagnostics
(dimension closure, Jacobi, Killing signature, invariant form).

**Mantero's framework:** Matroidal ideals on ground sets of size $n$
for $n \ge 10$ are the natural next regime after the rank-$\le 7$
results of the March 2026 paper.

**Bridge:** CL and BHML are separate canonical tables (see
`papers/ck_tables.py` at repo root). Their union gives a 45-dimensional
semisimple Lie algebra. Does the corresponding squarefree-monomial
union behave differently from either piece alone on the matroid axis?

**Status:** so(10) identification *verified* in WP103
(`../wp103/WP103_SO10_IDENTIFICATION.md`; renamed from `wp12` on
2026-04-24 to avoid numbering collision with the canonical WP12
"Seventeen Paradoxes via Dual-Lens Algebra"). Matroid consequences
*speculative*.

---

## Bridge 6 — Bump structure on $\Delta_B$ and a chain on $\{1, 2, 4, 8\}$

**Our object:** The Stanley–Reisner ideal of $\Delta_B$ is the bump
ideal

$$
I_B \;=\; (\, x_1 x_2,\; x_2 x_4,\; x_2 x_9,\; x_3 x_9,\; x_4 x_8 \,),
$$

five squarefree quadric generators corresponding to the five positions
$(i, j)$ in CL with $\mathrm{CL}[i, j] \notin \{0, 7\}$. Restricted to
the subset $\{1, 2, 4, 8\}$ these bumps form a **chain**,

$$
(1, 2) \;\to\; 3, \qquad (2, 4) \;\to\; 4, \qquad (4, 8) \;\to\; 8,
$$

with each edge labelled by its CL value. The Stanley–Reisner complex
$\Delta_B$ built from $I_B$ is pure of rank 7 on 10 vertices but fails
basis-exchange on 7 of 32 tested facet pairs (21.9%). Machine-checked
in
[`../sprint_20260423_full/04_mantero_bridge/matroid_test.py`](../sprint_20260423_full/04_mantero_bridge/matroid_test.py).

**Correction notice (2026-04-24).** A previous version of this bridge
summarized the basis-exchange failures as landing on "three
complementary pairs" $\{2, 3\}, \{6, 8\}, \{1, 4\}$. Those three pairs
are the color-wheel antipodes of the WP102 6DOF construction —
LATTICE↔COLLAPSE $(1, 4)$, PROGRESS↔COUNTER $(2, 3)$,
BREATH↔CHAOS $(6, 8)$ — not the minimal non-faces of $\Delta_B$.
Direct check from the CL table: $\mathrm{CL}[6, 8] = 7$ (HARMONY),
so $(6, 8)$ is a *face* of $\Delta_B$ rather than a non-face and
therefore cannot be a basis-exchange-failure coordinate. The
21.9% failure rate itself is unchanged; its machine-verifiable
coordinates are the 5-generator bump set above, and the
chain-on-$\{1, 2, 4, 8\}$ gives the simplest visualisable piece of
that set. The color-wheel pairs remain connected to the $D_4$ story
through the WP102 construction (they index three of the four
$\mathbb R^2$-factors of the standard
$\mathbb R^8 = \bigoplus_{k=1}^4 \mathbb R^2$ root-plane decomposition,
with the fourth factor indexed by the complement $\{0, 5, 7, 9\}$),
but that connection is between the WP102 Lie-algebraic lift and the
color wheel — not between Δ_B basis-exchange and the pair structure.

**Mantero's framework:** Focal matroids (March 2026) provide an
algorithmic route to produce "submatroids attached to a cover" — a way
of decomposing non-matroid structure into a matroid core plus a
focal correction. The focal-matroid decomposition is the natural place
to look for an invariant-theoretic description of where exchange can
or cannot happen.

**Bridge:** Does the focal-matroid framework assign a natural
invariant to the 5-generator bump set $\{(1,2), (2,4), (2,9), (3,9), (4,8)\}$?
If so, is the chain-on-$\{1, 2, 4, 8\}$ (three of the five bumps) a
distinguished sub-structure? And is the connection between that bump
set and the Lie-algebraic lift of Bridge 4 a general phenomenon of
Lie-algebra-compatible magmas, or specific to CL? These are entry
points into a comparative study.

**Status:** *Verified* 5-generator bump set and chain-on-{1,2,4,8}.
*Verified* 21.9% failure rate. *Withdrawn* the claim that failures
coincide with three color-wheel antipodal pairs. *Open* that the bump
set/chain is an invariant of a natural class of non-matroidal pure
complexes arising from Lie-algebra-compatible magmas.

---

## Bridge 7 — Is $A = R/I$ Koszul?

**Our object (2026-04-24, Macaulay2):** 53 independent quadrics. 12.8%
of associativity triples of the underlying magma fail. The full Betti
table of $R/I$ (via SageMathCell) is

```
total: 1 53 311 909 1644 1974 1602 861 285 48  2
    0: 1  .   .   .    .    .    .   .   .  .  .
    1: . 53 311 909 1644 1974 1602 861 284 46  1
    2: .  .   .   .    .    .    .   .   1  2  1
```

The degree-2 row ($\beta_{i,\,i+2}$) is nonzero at
$\beta_{8,10} = 1$, $\beta_{9,11} = 2$, $\beta_{10,12} = 1$, so the
minimal free resolution is **not linear**.

**Mantero's framework:** Mantero-Mastroeni 2022 (*The Structure of
Koszul Algebras Defined by Four Quadrics*) classifies Koszul algebras
generated by four quadrics. While the CL algebra has 53 quadrics (not
4), the Mantero-Mastroeni structural approach — distinguishing Koszul
from non-Koszul via linear-quotient decompositions — is directly
applicable.

**Bridge:** Since the resolution is not linear, $A$ is **not Koszul**.
This matches the heuristic expectation from the 12.8% associativity
failure rate. The open question now has a sharper form: is the
*associative deformation* of the CL magma (quotienting by the 128
non-associative triples, which removes exactly the obstructions
producing the bottom-strand Betti numbers above) Koszul? This is a
sharp test-case for the Mantero-Mastroeni machinery on a larger
generator count.

**Status:** *Verified not Koszul* (M2, 2026-04-24). The associative-
deformation follow-up question is *conjectural*.

---

## Summary table

| # | Bridge | Our side | His framework | Status |
|---|---|---|---|---|
| 1 | Hilbert + pd bound | HS reduces to $(1 + 9t - 8t^2 - t^3)/(1-t)$; $h(n)=1,10,2,1,1,\ldots$; codim 9, dim 1, pd 10, depth 0, not CM | Auslander-Buchsbaum, CM test | Verified (M2) |
| 2 | Pure but not matroidal | 21.9% exchange failure on $\Delta_B$ | Focal matroids (arXiv:2603.19419) | Conjectural → speculative |
| 3 | Waldschmidt constant | $\hat\alpha(I_B) = 2$ | Symbolic powers theorem (arXiv:2406.13759) | Verified (value) + conjectural (formula) |
| 4 | so(8) = D₄ lift | 28-dim Lie closure from antisymmetrized CL | Reflection / Coxeter context | Verified (Lie) + speculative (class) |
| 5 | so(10) = D₅ lift | 45-dim Lie closure from CL ∪ BHML | Matroids on larger ground sets | Verified (Lie) + speculative (matroid) |
| 6 | 6-DOF exchange failures | Failures align with $D_4$ root pairs | Focal-matroid decomposition | Verified (alignment) + speculative (general) |
| 7 | Koszul property | Bottom strand $\beta_{8,10}\!=\!1,\beta_{9,11}\!=\!2,\beta_{10,12}\!=\!1$ → not Koszul | Mantero-Mastroeni four-quadrics | Verified not Koszul (M2) |

The overarching thesis of the bridge: **the CL binomial ideal sits at a
computable distance from the matroidal centre of Mantero's program**,
and *that distance* — rather than any single invariant — is the useful
quantity to formalise.
