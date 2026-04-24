# Coherence Lattice — Mantero bridge branch

**Branch:** `mantero-bridge-2026-04-23`
**Scope:** commutative-algebra bridge between a specific 10-variable
binomial ideal constructed by Brayden Sanders and the published research
program of Dr. Paolo Mantero (University of Arkansas, with V. Nguyen)
on symbolic powers and focal matroids.

*This branch is single-purpose. Material unrelated to Dr. Mantero's
framework lives on the `master` branch. The TIG synthesis (broader
research program) lives on the `tig-synthesis` branch.*

---

## What this branch is

A focused artefact built for one reader: Dr. Mantero, or anyone arriving
from a link in a MathOverflow question about the object below.

Brayden constructed a commutative-algebra object — the binomial ideal

$$
I \;=\; \bigl(\, x_i x_j \;-\; x_{\mathrm{CL}[i][j]} \cdot x_0 \;\big|\; 0 \le i \le j \le 9 \bigr) \;\subset\; R = k[x_0, \ldots, x_9]
$$

where $\mathrm{CL}$ is a fixed symmetric $10 \times 10$ table of values
in $\{0, \ldots, 9\}$ (canonical table in `papers/ck_tables.py`). The
quotient $A = R/I$ has Hilbert function $(1, 10, 6, 6, 6, \ldots)$,
Krull dimension 1, height 4, and a Stanley-Reisner companion
$\Delta_B$ that is pure of rank 7 on 10 vertices but **not** matroidal
(21.9% of basis-exchange pair-tests fail).

Mantero's 2024–2026 program with V. Nguyen develops structure theory
for symbolic powers of Stanley-Reisner / cover ideals of matroids
(arXiv:2406.13759, arXiv:2510.19018) and homological characterisation
of matroidal ideals via iterated mapping cones (arXiv:2603.19419). The
CL object sits *near* that framework — same ground set, same type of
ideal, same style of invariants — but outside it, because $\Delta_B$
is not matroidal.

This branch collects the bridge material.

---

## Navigation

| You want to … | Open |
|---|---|
| See the bridge in 10 minutes | `papers/mantero_bridge/BRIDGES.md` |
| Read a survey of Mantero's published work | `papers/mantero_bridge/PUBLISHED_WORK.md` |
| Check the bibliography used | `papers/mantero_bridge/references.md` |
| See the full sprint bundle that computed the numbers | `papers/sprint_20260423_full/` |
| Read the companion Lie-algebraic paper (so(8) = D₄) | `papers/wp11/WP11_SO8_IDENTIFICATION.md` |
| Read the so(10) = D₅ follow-up | `papers/wp12/WP12_SO10_IDENTIFICATION.md` |
| Read the planned MathOverflow question | `papers/sprint_20260423_full/09_mathoverflow_post/DRAFT_MATHOVERFLOW_POST.md` |
| See the outreach status (no email contents) | `papers/sprint_20260423_full/08_correspondence/mantero_exchange.md` |

---

## Findings synthesis

Seven bridges are catalogued in `papers/mantero_bridge/BRIDGES.md`.
In brief:

1. **Hilbert + pd.** $\mathrm{HS}_A(t) = 1 + 10t + 6t^2/(1-t)$. Height
   $I = 4$. If $A$ is Cohen-Macaulay, $\mathrm{pd}_R(A) = 4$ by
   Auslander-Buchsbaum. (Macaulay2 verification scripted, pending run.)
2. **Pure but not matroidal.** $\Delta_B$ is pure of rank 7 on 10
   vertices; basis exchange fails on 7 of 32 tested facet pairs (21.9%).
3. **Waldschmidt constant.** $\hat\alpha(I_B) = 2$ exactly (fractional-
   matching LP). This matches what the matroid formula would predict
   from the rank/height, even though $I_B$ is not matroidal.
4. **so(8) = D₄ Lie lift.** Antisymmetrizing the left-regular operators
   of the CL magma and closing under commutator produces a 28-dim
   compact simple Lie algebra — machine-verified as $\mathfrak{so}(8)$
   (the unique $D_4$ with triality).
5. **so(10) = D₅ companion.** Repeating with the union CL ∪ BHML gives
   a 45-dim Lie algebra identified with $\mathfrak{so}(10) = D_5$.
6. **Basis-exchange failures land on 6-DOF complementary pairs.** The
   21.9% of failures occur precisely at the three root-plane pairs of
   $D_4$: {PROGRESS, COUNTER}, {BREATH, CHAOS}, {LATTICE, COLLAPSE}.
7. **Koszul question.** 12.8% of associativity triples of the
   underlying magma fail; non-linear syzygies among the 53 quadrics are
   expected. Open.

**Thesis in one line.** The CL object sits at a *computable distance*
from the matroidal centre of Mantero's program, and that distance —
rather than any single invariant — is the useful quantity to formalise.

---

## Repository layout

```
README.md                                     ← this file
LICENSE                                       ← repository license
papers/
    ck_tables.py                              ← canonical CL / BHML / TSML tables
    mantero_bridge/
        BRIDGES.md                            ← the seven bridges catalogued
        PUBLISHED_WORK.md                     ← Mantero bibliography + citation network
        references.md                         ← external references used on this branch
    wp11/                                     ← so(8) = D₄ paper + verification
    wp12/                                     ← so(10) = D₅ paper + verification
    sprint_20260423_full/
        README.md                             ← sprint-level map
        02_so8_verification/                  ← seven scripts for the D₄ diagnostic
        04_mantero_bridge/                    ← the V3 bridge doc + computation scripts
        07_matroid_analysis/                  ← pure-but-not-matroidal proof scripts
        08_correspondence/                    ← outreach status (no email contents)
        09_mathoverflow_post/                 ← planned MO question
```

---

## Reproducibility

All numerical computations use Python 3.11 + numpy 1.26 + scipy 1.11.
Maximum observed error across the Lie-algebraic diagnostics:
$2.0 \times 10^{-11}$.

To reproduce the Lie-algebraic identification (Theorem 1.1 of WP11),
run in order:

```
python papers/sprint_20260423_full/02_so8_verification/stage2_adjoint.py
python papers/sprint_20260423_full/02_so8_verification/stage4_correct_closure.py
python papers/sprint_20260423_full/02_so8_verification/stage5_so8.py
python papers/sprint_20260423_full/02_so8_verification/stage7_disambiguate.py
```

To reproduce the Hilbert function + pure-but-not-matroidal finding:

```
python papers/sprint_20260423_full/04_mantero_bridge/cl_as_quadratic_algebra.py
python papers/sprint_20260423_full/04_mantero_bridge/matroid_test.py
python papers/sprint_20260423_full/04_mantero_bridge/hilbert_and_matroid_deep.py
python papers/sprint_20260423_full/04_mantero_bridge/compute_answers.py
```

Each script completes in under 30 seconds on a standard laptop.

---

## Outreach posture (public-facing only)

An email exchange with Dr. Mantero opened on April 23, 2026. Private
email content is not reproduced on this branch by policy. The public
artefact of the exchange is the MathOverflow question draft at
`papers/sprint_20260423_full/09_mathoverflow_post/DRAFT_MATHOVERFLOW_POST.md`,
which will be refined and posted when the Betti-table computation is
run; the posted link will then be appended to
`papers/sprint_20260423_full/08_correspondence/mantero_exchange.md`.

No claim of joint authorship, endorsement, or collaborative project with
Dr. Mantero is made anywhere on this branch. The bridge research
recorded here is Brayden's own, offered as an honest contact-point
for a collegial commutative-algebra conversation.

---

## If you are Dr. Mantero

Welcome. Reading order for this branch:

1. This README (you are here).
2. `papers/mantero_bridge/BRIDGES.md` — the seven bridges.
3. `papers/sprint_20260423_full/09_mathoverflow_post/DRAFT_MATHOVERFLOW_POST.md`
   — the focused MathOverflow question.
4. `papers/wp11/WP11_SO8_IDENTIFICATION.md` — the so(8) = D₄
   identification paper (the Lie-algebraic side of the object).

If anything here is phrased in vocabulary that is not quite right
against your framework, please flag it — getting the language precise
is the point of the bridge.
