# J08 — The Sinc² Zero Law for Squarefree Moduli

**Status:** SUBMISSION-READY
**Phase:** Phase 1
**Target venue:** Integers
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** (sinc² zero law)

---

## §1 — Manuscript

**Local path:** `manuscript/`

Files in this J-folder's `manuscript/`:

- `cover_letter_template.md`
- `LATEX_BUNDLE_NOTES.md`
- `proof_d25_loop_closure.py`
- `sinc2_zero_law.tex`
- `SUBMIT_INSTRUCTIONS.md`
- `WP34_FIRST_G_LAW.md`
- `WP_SINC2_ZERO_LAW.md`

The submission package lives in this J-folder. Edit + verify here; submit from here.

## §2 — Verification script

**Path:** `papers/proof_d25_loop_closure.py`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J04

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**Status (2026-05-07): SUBMISSION-READY (FORMAT pass).** Manuscript re-scoped from
the 2026-04-18 prime-only draft (which was pulled back on 2026-04-19 after a
pre-push audit observed that the basic biconditional sinc²(k/n) = 0 ⇔ n | k is
uniform in n) to the squarefree-modulus formulation. The basic biconditional is
retained as Lemma 1; the squarefree-specific Theorem 2 ("the smallest k at which
any non-trivial divisor d | b produces a sinc² zero is k = spf(b)") is the
genuinely prime-dependent statement, and is the sinc² image of the First-G Event
Localization Theorem of J04 (cited as already-submitted *Integers* companion).

**Verification:** `proof_d25_loop_closure.py` runs green for all primes 3..199
(zero exceptions, exact arithmetic, runtime < 5s; ALL ASSERTIONS PASSED on
2026-05-07). The multi-prime squarefree case is verified by the J04 companion
script (`proof_first_g_event.py`, all squarefree b ≤ 500, 36,662 pairs, zero
exceptions); not duplicated here.

**Per-venue cap:** 2nd *Integers* paper this quarter after J04 (within cap).

**Authors:** Sanders + Gish.

**Cite:** J04 (First-G companion, submitted to *Integers*).

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

Sanders, B.R., Gish. (2026). "The Sinc² Zero Law for Squarefree Moduli." Submitted to *Integers*.
