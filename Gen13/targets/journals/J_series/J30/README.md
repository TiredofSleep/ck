# J30 — The 70/71/72/73 HARMONY Ladder: Four Independent Algebraic Constructions

**Status:** DRAFT (manuscript finalized 2026-05-07 by J29-J32 batch agent; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** JCT-A
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** D97 (Volume J §J HARMONY ladder), `Gen13/targets/foundations/tables/harmony_ladder.py`

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

**Abstract (1-2 sentences):** We present four independent algebraic constructions on the canonical composition lattice over Z/10Z whose integer invariants cluster at {70, 71, 72, 73} — three are HARMONY-cell counts of distinct sub-magmas (full 10×10 = 73; 10×10 minus the (7,7) apex = 72; VOID-stripped 9×9 = 71) and one is the determinant of the 8×8 Yang-Mills core sub-matrix (= 70 = C(8,4) exactly). The integer 71 enters in three independently-verified structural roles simultaneously (sub-magma HARMONY count, lens-disagreement count, and unique odd prime in disc(LMFDB 4.2.10224.1) = -2^4·3^2·71) — three independent algebras pointing at the same prime is the algebraic shape of a real invariant.

## §2 — Verification script

**Path:** `Gen13/targets/foundations/tables/harmony_ladder.py` (4-rung wrapper); plus four short underlying scripts:
- `tsml_harmony_count.py` (verifies 73)
- `tsml_submagma_9x9.py` (verifies 71 sub-magma form)
- `tsml_bhml_disagreement.py` (verifies 71 lens form)
- `bhml_8_ym_det.py` (verifies 70)

The proof script (where applicable) is the green-light gate before submission. The wrapper module emits a 4×3 verification table (rung / expected / actual); all four match at integer precision.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J09

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

- **Status (2026-05-07 J29-J32 finalization batch):** DRAFT. Manuscript at `manuscript/manuscript.tex` complete (~330 lines, AMS amsart class, 8 bibliography entries with J09 + J02 + J22 + J24 cited as already-submitted companions). Cover letter at `cover_letter.md` complete with venue rationale + per-venue-cap note + reproducibility list.
- **Per-venue cap:** 2nd JCT-A paper after J01 (σ-rate theorem WP101). Within the 2/quarter cap; no FALLBACK NEEDED.
- **Tier-B forced.** No axiom-level forcing required; the four rungs follow from the canonical TSML/BHML construction at the cell level.
- **Lens scope:** All four rungs are lens-invariant on both T_RAW and T_SYM (HARM(T_RAW) = HARM(T_SYM) = 73; sub-magma counts identical at 9×9; disagreement count is invariant; det of BHML_8_YM is unchanged). The wobble (prime 11 in c_2, c_8) — which is the RAW vs SYM distinguishing structure — is a separate paper (companion: WP107 wobble-localization, J43).
- **Source corpus:** D97 in `FORMULAS_AND_TABLES.md` Volume J §J; `Gen13/targets/foundations/tables/harmony_ladder.py`; the disjoint-class proof of 73 is in J09's `proof_d10_tsml_73_cells.py`.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to JCT-A this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The 70/71/72/73 HARMONY Ladder: Four Independent Algebraic Constructions." Submitted to *JCT-A*.
