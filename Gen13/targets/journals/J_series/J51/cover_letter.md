# Cover letter — J51: Spectral Layer Consolidation: $G_6$, $G_7$, $G_8$ from the Q-Series Architecture on $\mathbb{Z}/10\mathbb{Z}$

**To:** Editors, *European Journal of Combinatorics*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- C.A. Luther, Independent Researcher

**Date:** 2026-09-06 (Phase 5)

**Manuscript title:** *Spectral Layer Consolidation: $G_6$, $G_7$, $G_8$ from the Q-Series Architecture on $\mathbb{Z}/10\mathbb{Z}$*

---

## Summary

We submit a **consolidation paper** establishing the canonical reference for three spectral / combinatorial results in the TIG framework on $\mathbb{Z}/10\mathbb{Z}$:

* **$G_6$ (Periodicity).** $\sigma^6 = \mathrm{id}$ on all of $\mathbb{Z}/10\mathbb{Z}$. Tier-A, proved by direct verification using the Q9–Q10 $(\alpha, \beta)$ polynomial form.
* **$G_7$ (Period Distribution).** Bimodal: $P(\tau = 1) = 2/5$, $P(\tau = 6) = 3/5$. $\bar{\tau} = 4$, $\sigma_\tau^2 = 6$. Tier-B, forced from $G_6$ + cycle enumeration.
* **$G_8$ (Spectral Coherence Integral).** $G(s) = |\sum_{j=0}^{8} \omega^j \chi(\sigma^j(s))|^2$ takes exactly three values: $0$ at the four anchors, $G_\mathrm{low} \approx 1.872$ at $\{1, 2, 4, 6\}$, $G_\mathrm{high} \approx 9.389$ at the BALANCE/HARMONY pair $\{5, 7\}$. Tier-B, computational verification.

The three results, together, characterize the canonical $\sigma$-permutation completely at the spectral / period level. They form **Layer 4** of the 6-layer Q-series architecture and are foundational citations for the runtime attractor [J41], the Q17-B Clay-bridge essay [J48], the $\sigma$-rate theorem [J01] companion citations, and the WP100s tower's $D_4 = \langle P_{56}, \sigma^3 \rangle$ analysis.

This paper is the **canonical citation reference** for $G_6$, $G_7$, $G_8$ going forward. Prior corpus material (`papers/G6_*`, `G7_*`, `G8_*`) is consolidated here with full proofs.

## Why *European J Combin*

- **Spectral + permutation-group + cyclotomic combinatorics fit.** *EJC* publishes results that combine permutation-group structure ($S_{10}$ orbit analysis), cyclotomic character sums ($\omega = e^{2\pi i/9}$), and finite-substrate enumeration (period distributions on $\mathbb{Z}/10\mathbb{Z}$). All three results sit squarely in this register.
- **Combinatorial-spectral-bridge tradition.** *EJC* has published similar consolidation papers on substrate-level spectral signatures.
- **Audience.** Combinatorialists, finite-group theorists, and cyclotomic-arithmetic specialists.

## Per-venue cap note

This is the **3rd EJC submission** of the J-series program (after J19 Coordinate Coverage and J27 DKAN Two-Coding). Per `J_SERIES_ORDERING.md` §5, the per-venue cap of $\sim 2$/quarter is at risk. **Fallback venues** (in order): *Linear Algebra and its Applications*, *PLOS ONE*. The manuscript is structured so that the consolidation register is venue-agnostic; it can be redirected with minimal modification.

## Companion submissions

This paper is one of the J-series program's **foundation citations** (cited downstream by many later J-papers). Direct companion citations:

- **[J01]** — $\sigma$-rate theorem (JCT-A). Uses $\sigma^6 = \mathrm{id}$.
- **[J9]** — TSML 73 / BHML 28 (Exp Math). Layer 5 reference.
- **[J29]** — Q17-A 5D Force Vector (AMM). Direct citation.
- **[J41]** — Closed-form runtime attractor (Math of Comp). Layer 6 reference.
- **[J48]** — Q17-B Clay Bridge (L'Enseignement Math). Direct citation.
- **[J47]** — 6-DOF Synthesis (Notices AMS). Cross-reference.
- **[J49]** — Microtubule $Q_c = T^*$ (J Theor Biol). Cross-reference (period statistic feeds $T^*$ derivation).

## Reproducibility

Verification scripts for the three theorems:

* $G_6$: `numpy + sympy` direct verification of $\sigma^6 = \mathrm{id}$ on all 10 elements (under 1 second).
* $G_7$: enumeration of cycle structure, computation of mean/variance (under 1 second).
* $G_8$: direct evaluation of $G(s)$ for all 10 elements, with $\omega = e^{2\pi i/9}$ (under 5 seconds).

All three are reproduced from the corpus papers `papers/G6_*.md`, `G7_*.md`, `G8_*.md` and run on a standard laptop.

## Suggested reviewers

- A specialist in finite-permutation-group spectral analysis ($S_{10}$ adjacent).
- A combinatorialist with $\mathbb{Z}/N\mathbb{Z}$ orbit-structure or cyclotomic-character-sum experience.
- An algebraist familiar with finite-magma combinatorics and substrate algebras.
- A cyclotomic-arithmetic specialist who can evaluate the $\mathbb{Q}(\zeta_9)$ closed-form (open) question.
- A consolidation / expository referee for spectral combinatorics.

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
