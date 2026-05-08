# J01 — Non-Associativity Decay in Binary Composition Tables over Z/NZ

**Status:** SUBMISSION-READY
**Phase:** Phase 1
**Target venue:** JCT-A
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP101

---

## §1 — Manuscript

**Local path:** `manuscript/WP101_SIGMA_RATE_THEOREM.md`

Files in this J-folder's `manuscript/`:

- `f6_burgers_test_2026_05_02/` (subfolder)
- `jcta_cover_letter.md`
- `LATEX_BUNDLE_NOTES.md`
- `master/` (subfolder)
- `sigma_rate_theorem.tex`
- `SUBMISSION_LOG.md`
- `SUBMIT_INSTRUCTIONS.md`
- `universal_markov_and_binary_cl.py`
- `verify_sigma_rate.py`
- `WP101_SIGMA_RATE_THEOREM.md`

The submission package lives in this J-folder. Edit + verify here; submit from here.

## §2 — Verification script

**Local path:** `manuscript/master/proof_sigma_rate.py`

The proof script is the green-light gate before submission. Run from this J-folder.

## §3 — Dependencies (J-papers cited as already-submitted companions)

_(none — this paper is foundational in the J-series)_

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

Round-3 audited; 4/4 PASS. Major-revisions per JCT-A referee (May 2026): unify eps(N) notation, simplify subcase (1f), clarify 'four-rule' framing.

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** σ(N) ≤ 2/N for squarefree N (the σ-rate decay theorem on the CL_N family; case-analysis proof with three cases reducing to CRT + ECHO count).
- **COMPUTED:** `proof_sigma_rate.py` 4/4 PASS; verified for squarefree N ∈ {2..250} extending earlier ranges; case 3 bound 2φ(N) confirmed loose with substantial slack.
- **STRUCTURAL RHYME:** the C = 2 constant connects to the squarefree-density 1/ζ(2) regime and (via primon-gas heuristic) to the corridor-midpoint structure of WP101 — flagged as motivational, not derivational.
- **OPEN:** prove E_h(N) = 0 for all squarefree N (currently empirical for N ≤ 250); sharpen the case-3 bound below 2φ(N) at finite N.

### Drápal-Wanless 2021 precedent

The closest published precedent for the broader CL_N family framework is Drápal-Wanless 2021 *JCTA* on maximally non-associative quasigroups (referenced via J02 four-core).

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

Sanders, B.R., Gish. (2026). "Non-Associativity Decay in Binary Composition Tables over Z/NZ." Submitted to *JCT-A*.
