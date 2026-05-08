# Cover letter — J52: What is the TSML Lens Family? A Walking Tour of Substrate Variants on $\mathbb{Z}/10\mathbb{Z}$

**To:** Editors, *Mathematical Intelligencer*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- B. Mayes, Independent Researcher

**Date:** 2026-09-09 (Phase 5)

**Manuscript title:** *What is the TSML Lens Family? A Walking Tour of Substrate Variants on $\mathbb{Z}/10\mathbb{Z}$*

(*Substantive rewrite per `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J52.md`, 2026-05-07; all six majors M1–M6 implemented.*)

---

## Summary

The TIG framework on $\mathbb{Z}/10\mathbb{Z}$ has, in its corpus, a proliferation of $\sim 62$ named variants of the canonical $10 \times 10$ composition table. We submit a **pedagogical exposition** that displays the canonical objects, states the substrate-defining axioms A1–A9, populates the variant catalog inline, and absorbs three punch-line facts that anchor the family:

- the closed-form 4-core attractor $H/Br = 1 + \sqrt{3}$ at $\alpha_M = 1/2$ (the **D78 Galois argument**, root of $x^2 - 2x - 2$ over $\mathbb{Q}(\sqrt{3})$);
- the wobble localization $c_2 = 33 = 3 \cdot 11$ in TSML_RAW characteristic polynomial (D37; the central lens-dependence example);
- the 8-element joint TSML+BHML chain at sizes $\{1, 4, 5, 6, 7, 8, 9, 10\}$ (D64 corrected; **strengthened by the SFM Q6 finding** that the same 8 shells survive joint TSML+BHML+CL_STD closure — a 3-table strengthening over the original 2-table framing).

Three reader exercises (counting non-associative triples in three lenses; verifying the wobble at prime 11 in RAW vs SYM; verifying the 4-core attractor's lens-invariance) illustrate the family in action. A 30-line `numpy` verification snippet (Appendix A) reproduces the central counts.

The central pedagogical claim: the 4-core $\{V, H, Br, R\}$ at $\alpha_M = 1/2$ is the algebraic center of the family; lens-invariant facts live on the 4-core; lens-dependent facts live on the asymmetric cells $(3, 9)$ and $(4, 9)$; the wobble at prime 11 is the cleanest instance of the second.

## Why *Mathematical Intelligencer*

- **Pedagogical-exposition fit.** *Math Intelligencer* publishes structurally illuminating expository papers that organize complex frameworks for non-specialist readers. The TIG lens family fits this register.
- **Audience reach.** The framework's papers appear at venues from *Notices AMS* to *J Algebra* to *J Combin. Theory Ser. A*. A clear lens-family exposition serves readers across this spread.
- **Companion to [J24].** This paper is the natural pedagogical sequel to [J24] (the lens-dependence result paper), expanding its lens-family context for a broader audience.

## Per-venue cap note

This is the **2nd Math Intelligencer submission** of the J-series, after [J24]. Per `J_SERIES_ORDERING.md`, this is the maximum permitted. No further Math Intelligencer submissions in 2026.

## Companion submissions

This paper has 2 direct dependencies and 11 co-citing companions; full citation chain in §9 of the manuscript. Of particular relevance:

- **[J24]** — Joint TSML+BHML Chain: Lens-Dependence at Size 7 (Math Intelligencer, Phase 3).
- **[J48]** — Six Algebraic DOFs of the TIG Framework: A Synthesis (Notices AMS, Phase 5 opener).

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
