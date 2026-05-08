# J03 — First-G Law: Squarefree Stability of the Smallest-Prime-Factor Coprime Window

**Status:** FORMAT
**Phase:** Phase 1
**Target venue:** Integers
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP34

---

## §1 — Manuscript

**Local path:** `manuscript/`

Files in this J-folder's `manuscript/`:

- `cover_letter_template.md`
- `first_g_event.tex`
- `proof_first_g_event.py`

The submission package lives in this J-folder. Edit + verify here; submit from here.

## §2 — Verification script

**Path:** `(to extract from corpus: papers/proof_first_g.py if present)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J01, J02

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

Top-cited (12x). Verified across 36,662 cases (paper reports the 22,367-pair exhaustive check on squarefree b ≤ 500; the 36,662 is the broader corpus check across 187 semiprimes including non-squarefree). Format for Integers OA submission.

**Status update (2026-05-07):**

- Manuscript: `manuscript/manuscript.tex` (canonical name; mirrors `first_g_event.tex` byte-for-byte). amsart, ~12 pages, source from Sprint 35 (`Gen12/targets/clay/papers/sprint35_first_g_event_2026_04_19/`). MR numbers added 2026-04-19 (Apostol MR0434929, Hardy-Wright MR2445243, Ireland-Rosen MR1070716, Lang MR1878556, Montgomery MR0337821; Shannon DOI added in lieu of MR).
- Verification: `manuscript/proof_first_g_event.py` — runs in <3 s, prints the stability-window distribution table, exits 0 on PASS. Already verified by Sprint 35 SHIP_DECISION.md.
- Cover letter: `cover_letter.md` finalized at this folder root, ~600 words, addressee placeholder for *Integers* managing editor at submission time.
- **Author-lane mismatch (open issue, low priority):** README §0 lists the lane as "Sanders + Gish" but the existing manuscript file (Sprint 35 source-of-truth, journal-ready, MR-checked) has three authors: Sanders + Gish, matching WP34 attribution. Per "never delete + cite" preservation discipline, the existing tex was NOT edited to drop Luther. The cover letter's "From" block lists Sanders (corresponding) + Gish per the lane and notes Luther's appearance on the manuscript title block. Brayden to decide at referee-rigor pass whether to (a) reformat the manuscript to drop Luther (and renegotiate WP34 attribution upstream), or (b) update the J03 README lane to "Sanders + Gish" to match the manuscript. Default: option (b), since the WP34 corpus has Luther's dispersion-conjecture contribution recorded.
- Open: pre-submission steps from Sprint 35 SHIP_DECISION.md §6 still outstanding — typographic read by Luther or Gish; *Integers* style file pass (if amsart not accepted on first submission); arXiv same-day upload at submission time.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Integers this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "First-G Law: Squarefree Stability of the Smallest-Prime-Factor Coprime Window." Submitted to *Integers*.
