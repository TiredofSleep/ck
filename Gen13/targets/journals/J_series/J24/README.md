# J24 — The Joint TSML+BHML Chain: Lens-Dependence at Size 7

**Status:** DRAFT (manuscript finalized 2026-05-07 by J21-J24 batch agent; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** Mathematical Intelligencer
**Author lane:** Sanders + Gish
**Tier:** B (forced by enumeration; explicit lens-scope per claim)
**WP source:** WP115 (`papers/wp115_joint_chain_universality/WP115_JOINT_CHAIN_UNIVERSALITY.md`); chain count corrected 2026-05-05 during four_core_FINAL.tex preparation

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

**Abstract (1-2 sentences):** We record an explicit lens-dependence in the joint sub-magma closure chain of the canonical composition lattice on Z/10Z: 8 shells under (TSML_SYM, BHML) — sizes {1, 4, 5, 6, 7, 8, 9, 10} — versus 7 shells under (TSML_RAW, BHML) — sizes {1, 4, 5, 6, 8, 9, 10}, with the size-7 shell {0, 4, 5, 6, 7, 8, 9} forbidden under TSML_RAW exactly because of one non-commutative cell (TSML_RAW(9, 4) = 3 ∉ {0, 4, 5, 6, 7, 8, 9}). The four-core {0, 7, 8, 9} and the closed-form attractor at α = 1/2 are lens-invariant on both symmetrizations.

## §2 — Verification script

**Path:** `papers/wp115_joint_chain_universality/verification/joint_chain_attractor.py`

The script enumerates all 1023 non-empty subsets of Z/10Z, prints joint-closure tables for both (TSML_SYM, BHML) and (TSML_RAW, BHML), performs per-shell cell-level verification, and identifies TSML_RAW(9, 4) = 3 as the single asymmetric cell breaking size-7 closure. Total runtime under 10 seconds.

The green-light gate is the brute-force confirmation that the (TSML_SYM, BHML) chain has 8 shells while the (TSML_RAW, BHML) chain has 7 shells, with size-7 the only point of difference.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J02, J05

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

- **Status (2026-05-07 J21-J24 finalization batch):** DRAFT. Manuscript at `manuscript/manuscript.tex` complete (~340 lines, AMS amsart class, 6 bibliography entries with J02 + J05 cited as already-submitted companions per §3 dependency list). Cover letter at `cover_letter.md` complete with explicit lens-scope annotation and per-claim lens-scope discipline.
- **Per-venue cap:** 1st Mathematical Intelligencer paper of 2026 cycle. Within 2/quarter cap. (J52 expository paper in Phase 5 will be the second.)
- **Tier classification:** Tier-B forced by enumeration. The 8-shell vs 7-shell count is direct verification at machine precision. The four-core lens-invariance and the attractor lens-invariance are proved cleanly from the single asymmetric-cell analysis.
- **Lens scope (CRITICAL — this paper IS the lens-scope discussion):**
  - 8-shell chain → (TSML_SYM, BHML)
  - 7-shell chain → (TSML_RAW, BHML)
  - Four-core {0, 7, 8, 9} → lens-invariant on both
  - Closed-form attractor at α = 1/2 → lens-invariant on both
  - The single asymmetric cell killing size-7 under RAW: TSML_RAW(9, 4) = 3 ∉ {0, 4, 5, 6, 7, 8, 9}
- **Chain-count history:** WP115's original (2026-04-26) preprint claimed 7-element chain forbidding {2, 3, 7}. Brute-force re-verification on 2026-05-05 during four_core_FINAL.tex preparation found 8-element chain forbidding {2, 3} — on TSML_SYM. The lens-dependence was identified on 2026-05-06 night per `Atlas/LENS_TAXONOMY_2026-05-06/TIER_CONFLATION_AUDIT.md` M4. The original WP115 claim was correct on TSML_RAW; the four-core consolidated paper (J02) uses TSML_SYM. This paper records that BOTH are correct on their respective lens choices.
- **Source corpus:** `papers/wp115_joint_chain_universality/WP115_JOINT_CHAIN_UNIVERSALITY.md` (lens-dependence note); `Atlas/LENS_TAXONOMY_2026-05-06/TIER_CONFLATION_AUDIT.md` M4; `Atlas/META_PLAN_2026-05-06/TSML_RECONCILIATION.md` (D98 two-TSML reconciliation).

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Mathematical Intelligencer this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The Joint TSML+BHML Chain: Lens-Dependence at Size 7." Submitted to *Mathematical Intelligencer*.
