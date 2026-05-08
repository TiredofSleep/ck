# J27 — The Corner Sub-Magma C = (Z/10Z)*: Multiplicative-Unit Closure

**Status:** READY (manuscript drafted from corpus, cover letter finalized; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** Comm Algebra
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** Variant Catalog "Corner sub-magma C = {1,3,7,9}" (Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md) + DERIVATION.md row 22 + PROJECTION_DEFINITIONS.md "S = corner C as Tier-A canonical multiplicative units" + WP_TIER_CLASSIFICATION.md WP27

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

Abstract (1-sentence): The set C = {1, 3, 7, 9} of multiplicative units of Z/10Z is a TSML-closed sub-magma (verified by direct check on the 16-cell sub-table, in both RAW and SYM forms), simultaneously realizing the cyclic group of order 4 with generator 3 (the unique primitive root compatible with the TIG flatness criterion T* = 5/7 in (0,1)) and a 4-element TSML-closed sub-magma distinct from the joint-chain 4-core {0,7,8,9}; on C×C the TSML composition is HARMONY-saturated at 87.5% (14/16 cells), exceeding the global rate of 73%.

Source corpus: `Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md` (Corner C entry); `Atlas/LENS_TAXONOMY_2026-05-06/DERIVATION.md` (TABLE_INDEPENDENCE_LEDGER row 22, lens-invariant TSML closure); `Atlas/LENS_TAXONOMY_2026-05-06/PROJECTION_DEFINITIONS.md` (Tier-A canonical multiplicative units); `Atlas/META_PLAN_2026-05-06/WP_TIER_CLASSIFICATION.md` (WP27 product-gap connection).

## §2 — Verification script

**Path:** `(no script — theorem-paper; closure verifies in under 1 second via Gen13/targets/foundations/cells.py:closure_check)`

The closure check on the 16-cell sub-table of CL_TSML restricted to C × C is direct integer-arithmetic; both RAW and SYM forms are verified.

## §3 — Dependencies (J-papers cited as already-submitted companions)

_(none — this paper is foundational in the J-series; cites J25 and J23 for context but is independent)_

## §4 — Cover letter

See `cover_letter.md` in this folder. Finalized with summary, venue fit, companion list, and per-venue cap note.

## §5 — Notes

**Per-venue cap:** 3rd CommAlg paper after J15 + J26. Cap is 1/quarter; if binding, **FALLBACK NEEDED** to *Journal of Pure and Applied Algebra*, *Journal of Algebra and Its Applications*, or *Semigroup Forum*.

**Status notes:**
- The corner C is the multiplicative-unit group (Z/10Z)*, which is foundational in elementary number theory; the paper's novelty is the substrate-algebra closure connection plus the explicit contrast with the joint-chain 4-core.
- The generator-selection theorem (Theorem 5.1, g=3 unique compatible with T*) is included in §5 of the manuscript with a brief proof sketch citing the TIG flatness theorem; this is a proven D19 result.
- Companion-free: the paper is self-contained and can be submitted independently of other J-series papers.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Comm Algebra this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The Corner Sub-Magma C = (Z/10Z)*: Multiplicative-Unit Closure." Submitted to *Comm Algebra*.
