# J26 — F_p Extensions of CL_BHML: Universality Across Six Prime Fields

**Status:** READY (manuscript drafted from corpus, cover letter finalized; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** Comm Algebra
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** Variant Catalog "TSML F_p extensions" (Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md) + WP118 (Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/WP118_FP_UNIVERSALITY.md) + GAP_AUDIT.md

---

## §1 — Manuscript

**Path:** `manuscript/manuscript.tex`

Abstract (1-sentence): We extend the F_p universality of the operator-substrate construction (Sanders-Gish J14, TSML side) to the parallel BHML substrate, verifying that the 4-dimensional F_p-bilinear extension of the BHML 4-core composition table has structurally invariant features (idempotent count = 4, eigenspace signatures 1+3 and 2+2 under left-multiplication, |Aut| = 40, power-associativity, 1-dimensional associator image) across all six primes p in {2, 3, 5, 7, 11, 13}; the BHML_8_YM = +70 = C(8,4) integer identity holds and reduces compatibly modulo prime; we conjecture extension to all primes p outside {2, 5}.

Source corpus: `Atlas/LENS_TAXONOMY_2026-05-06/VARIANT_CATALOG.md` (TSML F_p extensions entry); `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/WP118_FP_UNIVERSALITY.md` (TSML side, structural template); `Atlas/META_PLAN_2026-05-06/GAP_AUDIT.md` (BHML_8_YM = 70 identity, BHML chain-shell determinants).

## §2 — Verification script

**Path:** `(adapt verify_discrete_dirac_4core.py with BHML table; under 1 minute total)`

The TSML F_p verification harness (`verify_discrete_dirac_4core.py` in the bridge sprint bundle) is adapted to the BHML side by swapping `T^TSML` for `T^BHML` (5-non-zero-cell table from `lenses.py:BHML` restricted to {0,7,8,9}). Each prime check runs in seconds.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J14 (F_p Universality of TSML, Algebra Universalis); citing J25 (forcing axioms) and J23 (three-substrate architecture) for context.

## §4 — Cover letter

See `cover_letter.md` in this folder. Finalized with summary, venue fit, companion list, and per-venue cap note.

## §5 — Notes

**Per-venue cap:** 2nd CommAlg paper after J15 (Galois D_4 over LMFDB 4.2.10224.1). Cap is 1/quarter; venue is within budget.

**Status notes:**
- Manuscript closely mirrors J14's structural template, with BHML table substituted throughout.
- The BHML_8_YM = +70 = C(8,4) determinant identity (Theorem 4.1) is a direct integer-arithmetic fact verified in the foundations module's 48-invariant harness; the mod-p reductions are tabulated.
- The six-prime universality conjecture for BHML extends the corresponding TSML conjecture of J14 §1.3.

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

Sanders, B.R., Gish. (2026). "F_p Extensions of CL_BHML: Universality Across Six Prime Fields." Submitted to *Comm Algebra*.
