# J02 — Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on Z/10Z

**Status:** SUBMISSION-READY
**Phase:** Phase 1
**Target venue:** Algebraic Combinatorics
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** (four-core consolidated)

---

## §1 — Manuscript

**Local path:** `manuscript/four_core_consolidated.tex`

Files in this J-folder's `manuscript/`:

- `4core_verification.py`
- `four_core_consolidated.tex`
- `four_core_consolidated_cover_letter.md`
- `four_core_seed.tex`
- `HOLD_PENDING_AUDIT.md`
- `master/` (subfolder)
- `SUBMISSION_LOG.md`
- `verification/` (subfolder)

The submission package lives in this J-folder. Edit + verify here; submit from here.

## §2 — Verification script

**Local path:** `manuscript/4core_verification.py`

The proof script is the green-light gate before submission. Run from this J-folder.

## §3 — Dependencies (J-papers cited as already-submitted companions)

_(none — this paper is foundational in the J-series)_

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

6/6 PASS. Major-revisions per AlgComb referee (May 2026): correct '93 of 100' → '71 of 100' disagreement count; name symmetrization choice for T; consider lifting closed-form fixed-point as Theorem 3.

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** chain structure of joint-closed sub-magmas of (TSML_SYM, BHML) on Z/10Z (8-shell chain at sizes {1,4,5,6,7,8,9,10}; size 7 admitted at {0,4,5,6,7,8,9}; sizes 2,3 forbidden), per the corrected 2026-05-05 enumeration. Closed-form attractor at α=½ with h/β = 1+√3 exact (LMFDB 4.2.10224.1 quartic, Galois D₄).
- **COMPUTED:** `4core_verification.py` 6/6 PASS. PSLQ at 50-digit precision; sympy galois_group confirms Galois D₄.
- **STRUCTURAL RHYME:** the 71 disagreement count between TSML and BHML on the 100-cell joint table coincides with the prime 71 in disc(LMFDB 4.2.10224.1) and with the σ-fixed disagreement count — three independent appearances of 71 in the same neighborhood. Cited as structural motivation, not derivation.
- **OPEN:** characterize the joint-closed sub-magma chain combinatorially without brute-force enumeration; lift the closed-form fixed-point as a third theorem (per AlgComb referee suggestion) using elementary algebra from `06_attractor_closed_form.py`.

### Drápal-Wanless 2021 precedent

The closest published precedent for this work is:

> Drápal, A. & Wanless, I.M. (2021). "Maximally non-associative quasigroups." *J. Combinatorial Theory, Series A*, **184**, 105510.

Same domain (small finite commutative non-associative structures); opposite extremum (Drápal-Wanless: maximally non-associative; this paper: specifically structured with integer-rational invariants). Same intellectual neighborhood. Adding to bibliography per external collaborator calibration 2026-05-07.

**Authors:** Sanders + Gish.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Algebraic Combinatorics this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on Z/10Z." Submitted to *Algebraic Combinatorics*.
