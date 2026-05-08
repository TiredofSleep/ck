# J05 — TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice

**Status:** FORMAT
**Phase:** Phase 1
**Target venue:** Experimental Mathematics
**Author lane:** Sanders + Gish
**Tier:** B (lens-invariant)
**WP source:** (73/28 paper)

---

## §1 — Manuscript

**Local path:** `manuscript/`

Files in this J-folder's `manuscript/`:

- `proof_d10_tsml_73_cells.py`
- `proof_d16_bhml_28_cells.py`
- `proof_fourier_bridge.py`
- `SUBMIT_INSTRUCTIONS.md`
- `WP35_PRIME_PHASE_TRANSITION.md`
- `WP_OPERATOR_RING_PARTITION.md`

The submission package lives in this J-folder. Edit + verify here; submit from here.

## §2 — Verification script

**Path:** `(corpus: 73/28 verification scripts)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J01 (sigma rate, JCTA), J02 (four-core, Algebraic Combinatorics) — companions in the Z/10Z structure.

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status (2026-05-07): SUBMISSION-READY (FORMAT pass).** Manuscript consolidated
into single-file `manuscript/tsml_bhml_cell_counts.tex` (`amsart`); markdown
source-of-record `WP_OPERATOR_RING_PARTITION.md` updated in lockstep.

**Lens-invariance section added (per Round-3 audit).** New §4 proves Theorem 3
(harmony cell counts are constant under every bijection π ∈ Stab(7) of the
operator alphabet that fixes the harmony output value). This Tier-B
classification is contrasted explicitly in §4 and §6 with the *lens-dependent*
joint sub-magma chain count of J02 (the four-core companion paper) — clarifying
that the 73/28 counts are intrinsic to the rule families while the chain count
is an interaction-dependent invariant requiring both operations simultaneously.

**Verification:** `proof_d10_tsml_73_cells.py` and `proof_d16_bhml_28_cells.py`
both run green from the manuscript folder (each completes in <0.1s and ends in
`ALL ASSERTIONS PASSED`; verified 2026-05-07). `ck_tables.py` is bundled in the
manuscript folder so the verification scripts are self-contained — a reader can
run the enumerations from the submission package alone, no PYTHONPATH gymnastics
required.

**Per-venue cap:** 2nd *Experimental Mathematics* paper this quarter after J08
(within cap).

**Authors:** Sanders + Gish.

**Cite:** J01 (sigma rate, JCTA), J02 (four-core, Algebraic Combinatorics) —
companions in the Z/10Z structure. J02 is the lens-dependent counterpart to the
present paper's lens-invariant cell counts; the contrast is the point of §4.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Experimental Mathematics this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice." Submitted to *Experimental Mathematics*.
