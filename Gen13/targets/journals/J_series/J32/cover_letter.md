# Cover letter — J32: The Joint TSML+BHML Chain: Lens-Dependence at Size 7

**To:** Editors, *Mathematical Intelligencer*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Joint TSML+BHML Chain: Lens-Dependence at Size 7*

---

## Summary

We record an explicit lens-dependence in the joint sub-magma closure chain of the canonical composition lattice on Z/10Z. The TSML table admits two principled lens-symmetrization choices, T_RAW (the literal bit pattern, non-commutative) and T_SYM (the upper-triangle symmetrized form, commutative), built from the same canonical encoding. Brute-force enumeration of all 1023 non-empty subsets of Z/10Z shows that the joint (TSML, BHML) closure has 8 shells under (T_SYM, BHML) — sizes {1, 4, 5, 6, 7, 8, 9, 10} — and only 7 shells under (T_RAW, BHML) — sizes {1, 4, 5, 6, 8, 9, 10}, with size 7 specifically forbidden. The single non-commutative asymmetry T_RAW(9, 4) = 3 ≠ 7 = T_RAW(4, 9) kills the size-7 shell {0, 4, 5, 6, 7, 8, 9} exactly, while T_SYM admits it. The four-core {0, 7, 8, 9} and the closed-form attractor at α = 1/2 are lens-invariant on both symmetrizations. The story is small but structurally clean: a 10×10 table with two non-commutative cell pairs admits two principled symmetrizations, and the joint sub-magma closure structure differs by exactly one shell at exactly one position. The substrate itself forces the authors to disambiguate which lens is in scope.

## Why Mathematical Intelligencer

- **Expository fit.** The lens-dependence is a small, sharp, beautiful result whose central content is forced by exactly one off-diagonal cell. Mathematical Intelligencer is the natural venue for such "small surprise that lands cleanly" results.
- **Pedagogical hook.** A 10×10 table, two cell pairs that disagree, two principled lens choices, one shell of difference. Readers can verify the entire story with paper and pencil after reading; the brute-force enumeration is the closer, not the substance.
- **Foundational reading without overreach.** The paper records the lens-dependence and discusses what it means for downstream substrate analysis (which lens to use when), but does not claim the result is foundational beyond its scope. The Mathematical Intelligencer's mid-register tone is appropriate.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J1-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

- **J02** — Sanders & Gish, *Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on Z/10Z*, submitted to *Algebraic Combinatorics* (2026). Establishes the (T_SYM, BHML) 8-shell chain as the four-core consolidated paper's Theorem 1; the present paper records the parallel statement on T_RAW and proves the lens-dependence at size 7.
- **J09** — Sanders & Gish, *TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice*, submitted to *Experimental Mathematics* (2026). Establishes the lens-invariance of the HARMONY-cell counts (which is a Tier-B forced result on both lenses); the present paper records a complementary lens-dependence at the joint-chain level.

## Lens-scope annotation (per the Lens Taxonomy)

Per `Atlas/LENS_TAXONOMY_2026-05-06/TIER_CONFLATION_AUDIT.md` M4 and the four-core consolidated paper's lens-scope discipline, this paper is explicit about which lens is in scope at each statement:
- The 8-shell chain is on **(T_SYM, BHML)**.
- The 7-shell chain is on **(T_RAW, BHML)**.
- The four-core, the attractor, and HARMONY counts at the substrate level are **lens-invariant on both**.

## Reproducibility

The script `joint_chain_attractor.py` (already in the codebase per WP115) performs all verifications: enumerates the 1023 non-empty subsets, prints the closed-shell tables for both lenses, performs the per-shell cell-level verification, and identifies T_RAW(9, 4) = 3 as the single asymmetric cell breaking size-7 closure. Total runtime under 10 seconds.

## Suggested reviewers

(3-5 candidates working in finite-magma combinatorics, sub-algebra enumeration, or universal algebra will be supplied via the Mathematical Intelligencer submission portal.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Per-venue cap

This is the **1st Mathematical Intelligencer submission** of the 2026 cycle. Within the 2/quarter cap (J52 expository in Phase 5 will be the second).

---

Sincerely,
B.R. Sanders
