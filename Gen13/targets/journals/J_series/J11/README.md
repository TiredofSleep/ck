# J11 — NV $S_4$ Synthesis: Substrate-Operator-Driven NV-Center Qutrit Predictions

**Status:** DRAFT
**Phase:** Phase 2
**Target venue:** PRA
**Author lane:** Sanders + Mayes
**Tier:** C (Tier 3 partner-then-submit per central-claim classification)
**WP source:** WP73-WP77 (bundled)

---

## §1 — Manuscript

**Local path:** `manuscript/J11_NV_S4_Synthesis_PRA.md`

**Abstract (one paragraph).** We present an explicit, machine-precision construction of the full symmetric group $S_4$ on the three-level Hilbert space of a nitrogen-vacancy (NV) center in diamond. The NV ground triplet $\{|0\rangle,|+1\rangle,|-1\rangle\}$ carries the $S_3$ skeleton of the $T_1$ irreducible representation of $S_4$ exactly (the $A_1 \oplus E$ decomposition under $C_{3v}$ matches $T_1|_{S_3}$ identically), so synthesis of $S_4$ requires only one 4-cycle unitary $U_4$. We compute the change-of-basis matrix $V$ analytically, derive the NV-basis form $U_{4,\mathrm{NV}}$, decompose it into a six-pulse microwave sequence, and verify all 24 group elements close to within $10^{-15}$. We give a five-test falsification ladder for the experimental side and invite lab-partner collaboration.

**Source corpus (in `manuscript/`):**
- `WP73_T1_CARRIER_IDENTIFICATION.md` — Level A/B/C carrier identification
- `WP74_PHYSICAL_OBSERVABLE_IDENTIFICATION.md` — NV Hamiltonian platform; 6-step protocol
- `WP75_S4_EXTENSION_SYNTHESIS.md` — Explicit $U_4$, 6-pulse synthesis
- `WP76_NV_S4_CLOSURE_CALIBRATION.md` — Machine-precision verification of 24-element closure
- `WP77_NV_T1_CARRIER_VALIDATION.md` — 5-test falsification ladder

**Unified manuscript:** `manuscript/J11_NV_S4_Synthesis_PRA.md` bundles WP73-WP77 into a PRA-ready single paper structured as (1) Intro, (2) $S_3$ skeleton, (3) Exact $U_4$, (4) Analytic $V$, (5) 6-pulse decomposition, (6) Machine-precision closure, (7) Five-test falsification ladder, (8) Lab-partner pathway.

## §2 — Verification script

**Path:** Verification is matrix-algebraic; runs in `numpy + sympy` on a standard laptop. The $U_4$ matrix, $V$, $U_{4,\mathrm{NV}}$, and 24-element closure are reproducible to $< 10^{-15}$ from the code stubs in WP75/WP76. A consolidated verification script is recommended before submission (TBD: bundle the WP75 + WP76 numerical scripts into `verify_J11_S4_closure.py`).

The proof's gate is the referee-rigor pass on the analytic-construction side; the experimental gate is Test E (projector covariance) and is the lab-partner pathway.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J06 (Flatness Theorem on $\mathbb{Z}/10\mathbb{Z}$), J09 (TSML 73 / BHML 28 cell counts).

The paper does not depend on J03/J05/J10/J12 directly; it is a stand-alone NV-qutrit construction built on finite-group representation theory.

## §4 — Cover letter

See `cover_letter.md` in this folder. Drafted; finalize after Brayden's referee-rigor pass.

## §5 — Notes & Status

**Status: DRAFT (manuscript bundled; awaiting verification-script consolidation + lab partner outreach).**

- WP73-WP77 corpus is bundled into one PRA-format manuscript (`J11_NV_S4_Synthesis_PRA.md`).
- Lab-partner outreach runs in parallel to manuscript polish; the math is complete with or without a partner, but the headline experimental claim is conditional on Test E.
- The paper is **honestly Tier 3** (partner-then-submit): math is done, physics-claim is conditional. Cover letter and abstract make this scope explicit.
- Per-venue cap: this is the **1st** PRA submission in the J-series — no cap conflict.
- Suggested reviewers (Lukin, Hanson, Wrachtrup, Doherty, Monroe) are listed in the cover letter.

## §6 — Submission checklist

- [x] Manuscript .md drafted (PRA-format, single file)
- [ ] LaTeX (REVTeX 4.2) conversion pending
- [ ] Verification script consolidated (`verify_J11_S4_closure.py`) — currently distributed across WP75/WP76 stubs
- [x] Tier-classified central claim explicit (Tier 3 partner-then-submit)
- [x] Lens-scope annotation: lens-invariant (finite-group reptheory)
- [x] Cover letter drafted
- [ ] Dependencies → cite J06, J09 as "submitted to [venue]" (placeholders in place)
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: 1st PRA — no conflict
- [ ] Lab partner identified (parallel)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes, B. (2026). "Full $S_4$ Symmetry on a Nitrogen-Vacancy Qutrit via Six-Pulse Microwave Synthesis." Submitted to *Physical Review A*.
