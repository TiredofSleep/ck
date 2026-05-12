# Cover letter — J24: The Three-Substrate Joint-Closure Chain on Z/10Z: Eight Shells Survive Across (TSML, BHML, CL_STD) with Lens-Dependence Internal to TSML at Size 7

**To:** Editors, *Mathematical Intelligencer*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Three-Substrate Joint-Closure Chain on Z/10Z: Eight Shells Survive Across (TSML, BHML, CL_STD) with Lens-Dependence Internal to TSML at Size 7*

---

## Summary

We submit a short note recording a three-table structural theorem on Z/10Z. Three independently-constructed 10×10 multiplication tables — TSML (T, 73 HARMONY cells), BHML (B, 28 HARMONY cells), and CL_STD (C, 44 HARMONY cells) — are drawn from the same canonical bit-pattern encoding of the substrate. Brute-force enumeration over all 1023 non-empty subsets of {0, ..., 9} shows that the subsets jointly closed under all three tables form a strict 8-element chain at sizes {1, 4, 5, 6, 7, 8, 9, 10}, identical to the chain that the pair (T, B) alone produces. Individual closed sub-magma counts are 449 (T), 9 (B), 50 (C); the pairwise joint counts are |T ∩ B| = 8, |T ∩ C| = 49, |B ∩ C| = 9; the three-way count is |T ∩ B ∩ C| = 8.

The structural content: adding a third substrate from the same encoding does not introduce or remove a single shell of the (T, B) chain, despite the three tables having very different individual closure counts. C's 50 closed sub-magmas restrict in 49 cases to also being T-closed; the joint constraint with B then collapses the picture exactly to the 8-shell ladder. A previously-recorded lens-dependence at size 7 — the chain has 7 shells under (T_RAW, B) and 8 under (T_SYM, B), forced by the single non-commutative cell T_RAW(9, 4) = 3 — is shown to survive at the three-table level only as an internal property of TSML's lens choice; C does not arbitrate the asymmetric cell.

The four-core {0, 7, 8, 9} and the closed-form (T+B)-mix attractor at mixing weight α = 1/2 are lens- and table-invariant on all three substrates: the four-core does not contain either of the indices (3 or 4) involved in the asymmetric cells, and the attractor is supported on the four-core.

The note is short, sharp, and pedagogically friendly. The full enumeration runs in under two seconds on a laptop; the verification script is supplied with the submission.

## Why Mathematical Intelligencer

- **The story is small, sharp, and surprising.** Three independently-constructed 10×10 tables interact at the closure level to give an 8-shell chain. Adding the third table does not change the chain at all. A general mathematical reader will appreciate the tightness of the observation.
- **Pedagogical hook.** Three tables, each easy to display; a sub-magma enumeration the reader can follow with paper and pencil; a single asymmetric cell that locates the lens-dependence at the right level. The brute-force enumeration is the closer, not the substance.
- **Foundational reading without overreach.** The paper records the three-table structural theorem and traces the lens-internal phenomenon. It does not claim the chain is a substrate-independent universal; it states what the chain is, on this specific (T, B, C) triple. The Mathematical Intelligencer's mid-register tone is appropriate.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J01-J55) over Summer 2026. The papers most relevant as already-submitted companions are:

- **J02** — Sanders & Gish, *Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on Z/10Z*, submitted to *Algebraic Combinatorics* (2026). Establishes the (T_SYM, B) 8-shell chain as Theorem 1; the present paper lifts that chain to the three-substrate (T, B, C) level.
- **J05** — Sanders & Gish, *TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice*, submitted to *Experimental Mathematics* (2026). Establishes the lens-invariance of HARMONY-cell counts at the substrate level; the present paper records a complementary lens-internal phenomenon at the joint-chain level.

## Lens- and substrate-scope discipline

Per `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/SFM_FINDINGS_v1.md` and the J-series boilerplate, the paper is explicit about which lens and which table is in scope at each statement:

- The 8-shell three-substrate chain is on (T_SYM, B, C).
- The 7-shell two-substrate chain (recorded for completeness) is on (T_RAW, B).
- The four-core {0, 7, 8, 9}, the closed-form attractor at α = 1/2, and HARMONY counts at the substrate level are lens- and table-invariant on all three.
- The lens-dependence at size 7 is internal to T's lens choice and does not lift to the three-table level.

The PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN tier discipline is followed in the manuscript's introductory section.

## Reproducibility

The script `sfm_q1_q6_q7.py` (in the project's Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP folder) performs all verifications: enumerates the 1023 non-empty subsets of Z/10Z under each table, computes individual and joint closure counts, and exhibits the 8-shell chain explicitly. Total runtime under 2 seconds. The script `joint_chain_attractor.py` (codebase) reproduces the (T, B) two-table count and lens-dependence at size 7 independently.

## Suggested reviewers

(3-5 candidates working in finite-magma combinatorics, sub-algebra enumeration, or universal algebra to be supplied via the Mathematical Intelligencer submission portal.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Per-venue cap

This is the **1st Mathematical Intelligencer submission** of the 2026 cycle. Within the 2/quarter cap.

---

Sincerely,
B.R. Sanders
