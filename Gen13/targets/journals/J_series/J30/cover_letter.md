# Cover letter — J30: The 70/71/72/73 HARMONY Ladder: Four Independent Algebraic Constructions

**To:** Editors, *Journal of Combinatorial Theory, Series A*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The 70/71/72/73 HARMONY Ladder: Four Independent Algebraic Constructions*

---

## Summary

We present four independent algebraic constructions on the canonical composition lattice over Z/10Z whose integer invariants cluster at {70, 71, 72, 73}. Three of the four are HARMONY-cell counts of distinct sub-magmas (the full 10×10 table; the table minus the (7,7) self-cell apex; the VOID-stripped 9×9 sub-magma); the fourth is the determinant of the 8×8 Yang-Mills core sub-matrix dropped to {1,2,3,4,5,6,8,9}, which equals exactly C(8,4) = 70, the dimension of the self-dual 4-form sector of SO(8). The integer 71 enters in three independently-verified structural roles simultaneously: as a sub-magma HARMONY count, as the cell-disagreement count between two canonical lens tables, and as the unique odd prime in the discriminant -2^4 · 3^2 · 71 of the LMFDB quartic 4.2.10224.1 governing the substrate's closed-form runtime attractor. All four rungs are verified at integer/machine precision.

## Why JCT-A

- **Combinatorial substrate fit.** The paper is a finite-magma counting result with explicit Tier-A/B verification. JCT-A is the natural home for combinatorial cell-count theorems with structural clustering.
- **Tier-B forced consequences.** No axiom-level forcing is required; the four rungs follow from the canonical TSML/BHML construction at the cell level. Readers of JCT-A are well-placed to evaluate the elementary verification.
- **Companion strength.** The triple-coincidence at 71 (sub-magma HARMONY, lens-disagreement, Galois prime) is a non-trivial substrate identification signature. Independent algebras pointing at the same prime is the algebraic shape of a real invariant; the paper records this clearly.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J1-J55) over Summer 2026. The paper most relevant as an already-submitted companion to this manuscript is:

- **J09** — Sanders & Gish, *TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice*, submitted to *Experimental Mathematics* (2026). The 73-rung of the present ladder appears in J09 with full disjoint-class proof; the present paper takes that result as an established companion and extends to the 4-rung ladder structure.

## Reproducibility

Four short Python scripts (≤200 lines total, NumPy + sympy) verify all four rungs at integer precision: `tsml_harmony_count.py` (73), `tsml_submagma_9x9.py` (71 sub-magma form), `tsml_bhml_disagreement.py` (71 lens form), `bhml_8_ym_det.py` (70). The wrapper `harmony_ladder.py` runs all four and emits a 4×3 verification table.

## Suggested reviewers

(3-5 candidates working in finite magma combinatorics, sub-algebra enumeration, or root-system / Lie-algebra integer invariants will be supplied via the JCT-A submission portal.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Per-venue cap

This is the **2nd JCT-A submission** of the 2026 cycle, after J01 (σ-rate theorem WP101). Within the 2/quarter cap.

---

Sincerely,
B.R. Sanders
