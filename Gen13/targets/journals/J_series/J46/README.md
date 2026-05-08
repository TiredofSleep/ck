# J46 — Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at e^-1 from a Logarithmic Potential

**Status:** BLOCKED — referee-flagged numerical inconsistency must be resolved before submission
**Phase:** Phase 5
**Target venue:** JCAP
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** (paper1_freeze_thaw_v3)

---

## §1 — Manuscript

**Path:** `../../../../Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/tig_2026-05-07_bundle/seeds_for_submission/paper1_freeze_thaw_v3.tex`

When the manuscript is in this J-folder, replace this section with a 1-2 sentence abstract and a path-link to the .tex / .md file.

## §2 — Verification script

**Path:** `../../../../Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/tig_2026-05-07_bundle/seeds_supporting/verification_scripts/compute_zstar_v3.py`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

_(none — this paper is foundational in the J-series)_

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

v3 (3 issues fixed: Friedmann Omega-units convention; z_init/N_start footnote; compute_zstar_v3 reconciliation). Cover letter ready.

### JCAP referee report findings (May 2026 — see `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J3_JCAP_REFEREE_REPORT.md`)

**Decision: MAJOR REVISIONS.**

Three top-priority issues:

1. **CRITICAL — Numerical reproducibility failure on z_star.** Paper claims z_star ≈ 1.3 at IC (Λ⁴/ρ_c,0, Ξ_i, Ξ'_i) = (0.231, 0.925, +0.470), but independent execution of `compute_zstar_v3.py` with those exact IC reproduces w(z=0) ≈ -0.79 (consistent) but z_star = **2.131**, not 1.3. The 4 supplied scripts + the Eq. 31 IC + the z_star ≈ 1.3 claim are not mutually consistent. Internal: Abstract still says ≈2, body says 1.3, χ² body=1.24 vs Summary=1.52. **Must reconcile before resubmission.**

2. **IC tuning without naturalness/attractor mechanism.** No tracker analysis, no 2D scan in (Ξ_i, Ξ'_i), no fraction-of-IC-space estimate for dual-regime trajectories. JCAP quintessence referees demand this.

3. **Missing adjacent prior art.** Albrecht-Skordis 2000 (PRL 84, 2076) — tracking-to-freezing quintessence transition, closest direct precedent. Boisseau-Esposito-Farese-Polarski-Starobinsky 2000 (PRL 85, 2236), Tsujikawa-Sami 2007 (PLB 651, 224), Ferreira-Avelino 2018 logotropic.

**Estimated revision effort:** 2-4 weeks. Path to acceptance: produce a single canonical script that reproduces Eq. 31 + the w(z) table to 4-digit accuracy + converges on a SINGLE z_star value; expand §7.4 perturbations + 2D IC scan; add missing citations.

### What this blocks

J46 ships **AFTER** Brayden's full referee-rigor pass + script reconciliation. The triadic launch can still go: J01 + J02 ship Week 1 (May 13-14); J46 follows in Week 2 once the z_star inconsistency is resolved. Alternative: ship all three Week 1 with J46 explicitly flagged "v3 — addresses prior reviewer feedback" with the script reconciled in advance.

Awaiting Brayden's decision on which path.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to JCAP this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish, Johnson. (2026). "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at e^-1 from a Logarithmic Potential." Submitted to *JCAP*.
