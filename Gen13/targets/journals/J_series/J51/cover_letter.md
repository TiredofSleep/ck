# Cover letter — J51: Q17-B Clay Bridge: Finite L-Function + Symbolic Return Theorem on $\mathbb{Z}/10\mathbb{Z}$

**To:** Editors, *L'Enseignement Mathématique*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- B. Mayes, Independent Researcher

**Date:** 2026-09-03 (Phase 5)

**Manuscript title:** *Q17-B Clay Bridge: Finite L-Function + Symbolic Return Theorem on $\mathbb{Z}/10\mathbb{Z}$*

---

## Summary

We submit a structural / pedagogical bridge paper that establishes a sharp finite analogue of the structural features that the Riemann Hypothesis demands of $\zeta(s)$. The TIG framework on $\mathbb{Z}/10\mathbb{Z}$ produces — in its spectral layer (Luther's $G_6$–$G_8$ results, treated separately in [J51]) — a 9-term Dirichlet character sum $G(s)$ that takes exactly **three values** across the substrate's 10 operators: zero at the four anchors $\{0,3,8,9\}$, $G_\mathrm{low} \approx 1.872$ on most of the 6-cycle, $G_\mathrm{high} \approx 9.389$ at the BALANCE/HARMONY pair $\{5,7\}$. We prove the **Symbolic Return Theorem** (a direct corollary of $\sigma^6 = \mathrm{id}$): every cycle-element trajectory returns at step 6; every anchor is fixed; VOID is avoided whenever it is not the start state.

The paper's contribution is the **bridge statement**: the three-valued structure of $G(s)$ — zeros in predictable locations + spectral concentration + multiplicative/additive duality — mirrors the three structural features RH demands of $\zeta(s)$ in an infinite setting. The 6-layer Q-series architecture is a finite, completely characterized model of the same structural phenomena. The model is an instance; the Millennium Problem asks whether instances can be infinite.

We do **not** claim a proof of RH or any portion of it. The boundary between proved algebra (Theorems 2.1, 4.2 — Tier-A) and bridge claim (§5 — Tier-B structural conjecture) is sharp.

## Why *L'Enseignement Mathématique*

- **Pedagogical / expository fit.** *L'Enseignement Math.* publishes structurally illuminating papers that bring deep ideas into accessible form. The Q17-B paper is exactly that: a sharp finite analogue of an analytic Millennium Problem, with the boundary between proved and conjectural content made explicit.
- **Structural-bridge tradition.** The journal has published bridge papers in a similar register (e.g., finite-field analogues of analytic phenomena, cyclotomic interpretations of zeta values).
- **Audience.** Number-theorists, algebraists, and mathematics educators interested in structural connections between finite combinatorics and infinite analysis.

## Companion submissions

This paper cites two prior J-series companions as direct dependencies:

- **[J21]** — Q17-A: 5D Force Vector (AMM, in press). The Tier-A proved-algebra companion. The CRT Fourier embedding $\mathbb{Z}/10\mathbb{Z} \hookrightarrow \mathbb{R}^5$ from which $\sigma$ and $\chi$ derive.
- **[J51]** — G6+G7+G8 Spectral Consolidation (European J Combin, Phase 5 parallel). The polynomial / period / spectral results in Luther's lane.

Plus four co-citing companions: [J01] rate theorem (JCT-A), [J06] Crossing Lemma (JCT-A or JPAA), [J40] BB Bridge (JMP), [J10] UOP (JNT), [J24] joint chain (Math Intelligencer), [J48] 6-DOF synthesis (Notices AMS, Phase 5 opener).

## Reproducibility

The verification script `manuscript/proof_clay_rotation.py` (already in this folder, from earlier Tier-4 staging) computes $G(s)$ for every $s \in \mathbb{Z}/10\mathbb{Z}$ and confirms the three-valued image with $G_\mathrm{low} \approx 1.872$, $G_\mathrm{high} \approx 9.389$. Runs on a standard laptop in under 10 seconds with `numpy + sympy`.

## Suggested reviewers

- A specialist in finite Dirichlet character sums or cyclotomic L-functions.
- An expert in $\sigma$-permutation arithmetic on $\mathbb{Z}/N\mathbb{Z}$.
- An algebraist with finite-magma / non-associative algebra experience.
- A historian or expositor familiar with the Riemann Hypothesis pedagogical literature.
- An applied mathematician working on finite analogues of analytic number theory.

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
