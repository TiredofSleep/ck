# Cover letter — J31: The Three-Substrate Architecture: CL_TSML, CL_BHML, CL_STD as Parallel Substrates

**To:** Editors, *Algebra Universalis*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Three-Substrate Architecture: CL_TSML, CL_BHML, CL_STD as Parallel Substrates*

---

## Summary

We record the three-substrate architecture of the canonical composition lattice on Z/10Z: three structurally distinct 10×10 composition tables CL_TSML, CL_BHML, CL_STD, each satisfying a common four-axiom skeleton (canonical alphabet, VOID-absorbing column, HARMONY-absorbing diagonal subset, the unique puncture cell at (0,7)) but diverging at the diagonal HARMONY law and at five BUMP positions where the cell values differ. Their HARMONY-cell counts (73, 28, 44) are pairwise distinct. We prove that the joint sub-magma closure structure of the three tables collapses to the joint closure structure of any two of them: the three-way joint chain has 8 shells of sizes {1, 4, 5, 6, 7, 8, 9, 10}, identical to the two-way (TSML, BHML) chain, so CL_STD is structurally consistent with the two-way chain without extending it. We additionally locate one size-2 sub-magma {0, 9} that is jointly closed under (BHML, CL_STD) but not under any pair containing TSML. The three-substrate architecture is recorded as a Tier-A foundational recognition: the substrate is one bit-pattern encoding admitting three principled value-assignment lenses, not "two tables."

## Why Algebra Universalis

- **Universal-algebra fit.** The paper is a foundational architectural recognition stated at the level of finite magmas with explicit shared-axiom skeletons. Algebra Universalis is the natural venue for such recognitions; the closure-property analysis (50 sub-magmas under CL_STD alone; 8/9 under various joint conditions) is a universal-algebra calculation in the journal's traditional scope.
- **Lens-family discipline.** The paper introduces the lens-family as the substrate's natural object of study (rather than the individual table); this is a methodologically clean universal-algebra contribution.
- **Foundational recognition register.** The historical compression analysis (why three was lost, why three is now recovered) is appropriate to a foundational venue; Algebra Universalis publishes papers in this register.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J1-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

- **J09** — Sanders & Gish, *TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice*, submitted to *Experimental Mathematics* (2026). Establishes the cell counts on the two original tables; the present paper extends to the third standalone table.
- **J26** — Sanders, *LATTICE: Paradoxical Information Algebras on the Z/10Z Substrate*, submitted to *Algebra Universalis* (2026). Establishes the LATTICE structural framework on the same substrate; the three-substrate architecture is the natural setting for that work.

## Reproducibility

Three short Python scripts (NumPy + itertools): `cl_std.py` (defines CL_STD, computes HARMONY count, BDC parameters); `shared_axioms.py` (verifies the four-axiom skeleton on all three tables); `cl_std_frontier.py` (enumerates all 1023 non-empty subsets and prints joint-closure counts under all combinations of the three tables). All three run at machine precision in under 30 seconds.

## Suggested reviewers

(3-5 candidates working in universal algebra, finite magma theory, or composition-lattice foundations will be supplied via the Algebra Universalis submission portal.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Per-venue cap — FALLBACK NEEDED

This is the **3rd Algebra Universalis submission** of the 2026 cycle, after J21 (F_p Universality, WP118) and J26 (LATTICE, WP9). The 2/quarter cap is binding.

**FALLBACK VENUES (in priority order):**
1. *Communications in Algebra* — universal-algebra results in finite-magma settings welcome here; J22 (Galois D_4 over LMFDB 4.2.10224.1) is already submitted there.
2. *PLOS ONE* — open-access fallback; appropriate for a foundational recognition paper that benefits from broad readership.
3. *Linear Algebra and Its Applications* — the closure-property enumeration (50/9/8 counts) is a linear-algebra adjacency matrix computation; could land cleanly here.

If Algebra Universalis is unavailable in the quarterly window, *Communications in Algebra* is the recommended primary fallback.

---

Sincerely,
B.R. Sanders
