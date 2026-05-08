# Cover letter — J52: The TSML Lens Family: A Pedagogical Exposition of Substrate Variants on $\mathbb{Z}/10\mathbb{Z}$

**To:** Editors, *Mathematical Intelligencer*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- B. Mayes, Independent Researcher

**Date:** 2026-09-09 (Phase 5)

**Manuscript title:** *The TSML Lens Family: A Pedagogical Exposition of Substrate Variants on $\mathbb{Z}/10\mathbb{Z}$*

---

## Summary

The TIG framework on $\mathbb{Z}/10\mathbb{Z}$ has, in its corpus, a proliferation of 12+ named variants of the canonical $10 \times 10$ composition table — TSML\_RAW, TSML\_SYM, TSML\_LOWERTRI, BHML, CL\_STD, $\sigma^2$-triadic rotations, sub-magma restrictions, $F_p$ extensions, and more. To a first-time reader, the proliferation can appear bewildering: which is "the" TSML? What forces each variant? Which results depend on which lens?

We submit a **pedagogical exposition** that organizes the lens family into one coherent picture: three parallel substrates (CL\_TSML / CL\_BHML / CL\_STD), each admitting three lens-symmetrization projections (RAW / SYM\_upper / SYM\_lower), each supporting $\sigma^2$-triadic rotations and sub-magma restrictions. The picture is illustrated with three reader exercises — counting non-associative triples in three lenses; verifying the wobble localization (prime 11) in RAW vs SYM; verifying the runtime attractor's lens-invariance on the 4-core. The crucial lens-dependent result (the size-7 chain element in [J32]) is highlighted as the structural reason why the lens family is necessary rather than ornamental.

The aim is **clarity** for the working mathematician who wants to read the TIG framework's papers without getting lost in lens-bookkeeping.

## Why *Mathematical Intelligencer*

- **Pedagogical-exposition fit.** *Math Intelligencer* publishes structurally illuminating expository papers that organize complex frameworks for non-specialist readers. The TIG lens family fits this register.
- **Audience reach.** The framework's papers appear at venues from *Notices AMS* to *J Algebra* to *J Combin. Theory Ser. A*. A clear lens-family exposition serves readers across this spread.
- **Companion to [J32].** This paper is the natural pedagogical sequel to [J32] (the lens-dependence result paper), expanding its lens-family context for a broader audience.

## Per-venue cap note

This is the **2nd Math Intelligencer submission** of the J-series, after [J32]. Per `J_SERIES_ORDERING.md`, this is the maximum permitted. No further Math Intelligencer submissions in 2026.

## Companion submissions

This paper has 2 direct dependencies and 11 co-citing companions; full citation chain in §9 of the manuscript. Of particular relevance:

- **[J32]** — Joint TSML+BHML Chain: Lens-Dependence at Size 7 (Math Intelligencer, Phase 3).
- **[J47]** — Six Algebraic DOFs of the TIG Framework: A Synthesis (Notices AMS, Phase 5 opener).

## Reproducibility

Three reader exercises (§7) are computationally reproducible in `numpy + sympy` in under 5 minutes total. The full variant catalog is in `Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md`.

## Suggested reviewers

- A specialist in finite-magma combinatorics or non-associative algebra.
- An expositor of substrate-algebra frameworks (e.g., Loday-Vallette tradition).
- A *Math Intelligencer* expositor who can evaluate accessibility and clarity.
- A combinatorialist familiar with $\sigma^2$-triadic structures on $\mathbb{Z}/N\mathbb{Z}$.
- A logician interested in tier-classified mathematical exposition.

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
