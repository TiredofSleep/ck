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

## Bridge 1 — The Hilbert function stabilizes at 6

**Our object:** $\dim_k A_n = 6$ for all $n \ge 2$, where $A = R/I$. So
$\mathrm{HS}_A(t) = 1 + 10 t + \frac{6 t^2}{1-t}$, Krull dimension of $A$
equals 1, and the coordinate ring at the fibre over $x_0$ has rank 6.
The 6 stable variables are the image in $A$ of
$\{\mathrm{VOID}, \mathrm{PROGRESS}, \mathrm{COLLAPSE}, \mathrm{HARMONY},
\mathrm{BREATH}, \mathrm{RESET}\}$.

**Mantero's framework:** Cohen-Macaulayness and projective dimension
bounds on binomial / toric ideals. Auslander-Buchsbaum gives
$\mathrm{pd}_R(A) + \mathrm{depth}(A) = 10$, so if $A$ is
Cohen-Macaulay then $\mathrm{pd}_R(A) = \mathrm{height}(I) = 4$.

**Bridge:** This is the cleanest question to ask: is $A$ Cohen-Macaulay?
If yes, $\mathrm{pd}_R(A) = 4$ exactly, matching the height. If no, the
discrepancy is a quantitative invariant of the non-matroidal part of the
table.

**Status:** *Conjectural* — the Macaulay2 `betti res A` run is scripted
(`09_mathoverflow_post/compute_betti.m2` in the sprint bundle) but not
yet executed as of posting.

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

**Status:** so(10) identification *verified* in WP12
(`../wp12/WP12_SO10_IDENTIFICATION.md`). Matroid consequences
*speculative*.

---

## Bridge 6 — The basis-exchange failures align with the 6-DOF complementary pairs

**Our object:** The 21.9% of basis-exchange failures on $\Delta_B$ occur
precisely at the three complementary pairs that appear as the root
planes of $D_4$:

```
X:   PROGRESS(3)  ↔  COUNTER(2)
Y:   BREATH(8)    ↔  CHAOS(6)
Z:   LATTICE(1)   ↔  COLLAPSE(4)
```

These are the same pairs that organize the color-wheel decomposition
and the 6-DOF structure in the so(8) adjoint action.

**Mantero's framework:** Focal matroids (March 2026) provide an
algorithmic route to produce "submatroids attached to a cover" — a way
of decomposing non-matroid structure into a matroid core plus a
focal correction. The focal-matroid decomposition is the natural place
to look for an invariant-theoretic description of where exchange can
or cannot happen.

**Bridge:** Is the coincidence between basis-exchange failure locations
and $D_4$ complementary pairs a general phenomenon of
Lie-algebra-compatible magmas, or is it specific to CL? The answer to
this question is the entry point into a full comparative study.

**Status:** *Verified* that the failures land on the three pairs.
*Speculative* that this is general.

---

## Bridge 7 — Is $A = R/I$ Koszul?

**Our object:** 53 independent quadrics. 12.8% of associativity triples
of the underlying magma fail. Heuristically, a non-trivial nonlinear
syzygy should appear in the first resolution row.

**Mantero's framework:** Mantero-Mastroeni 2022 (*The Structure of
Koszul Algebras Defined by Four Quadrics*) classifies Koszul algebras
generated by four quadrics. While the CL algebra has 53 quadrics (not
4), the Mantero-Mastroeni structural approach — distinguishing Koszul
from non-Koszul via linear-quotient decompositions — is directly
applicable.

**Bridge:** A direct Macaulay2 computation of $\mathrm{Tor}_2^R(A, k)$
will decide Koszulness definitively. A negative answer (non-Koszul)
opens the question: is the *associative deformation* of the CL magma
(quotienting by the 128 non-associative triples) Koszul? This is a
sharp test-case for the Mantero-Mastroeni machinery on a larger
generator count.

**Status:** *Conjectural.* The Macaulay2 run is scripted but not
yet executed.

---

## Summary table

| # | Bridge | Our side | His framework | Status |
|---|---|---|---|---|
| 1 | Hilbert + pd bound | HS stabilizes at 6, height 4 | Auslander-Buchsbaum, CM test | Conjectural |
| 2 | Pure but not matroidal | 21.9% exchange failure on $\Delta_B$ | Focal matroids (arXiv:2603.19419) | Conjectural → speculative |
| 3 | Waldschmidt constant | $\hat\alpha(I_B) = 2$ | Symbolic powers theorem (arXiv:2406.13759) | Verified (value) + conjectural (formula) |
| 4 | so(8) = D₄ lift | 28-dim Lie closure from antisymmetrized CL | Reflection / Coxeter context | Verified (Lie) + speculative (class) |
| 5 | so(10) = D₅ lift | 45-dim Lie closure from CL ∪ BHML | Matroids on larger ground sets | Verified (Lie) + speculative (matroid) |
| 6 | 6-DOF exchange failures | Failures align with $D_4$ root pairs | Focal-matroid decomposition | Verified (alignment) + speculative (general) |
| 7 | Koszul property | 53-quadric algebra, 12.8% non-assoc triples | Mantero-Mastroeni four-quadrics | Conjectural |

The overarching thesis of the bridge: **the CL binomial ideal sits at a
computable distance from the matroidal centre of Mantero's program**,
and *that distance* — rather than any single invariant — is the useful
quantity to formalise.
