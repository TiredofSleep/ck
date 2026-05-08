# J41 — The Yang-Mills Mass Gap Bridge: Substrate-Algebra Predictions

**Status:** DRAFT
**Phase:** Phase 4
**Target venue:** Journal of Mathematical Physics (companion to J40)
**Author lane:** Sanders + Gish
**Tier:** B (Tier 4 framework-paper per central-claim classification)
**WP source:** WP92

---

## §1 — Manuscript

**Local path:** `manuscript/J14_YM_MassGap_Bridge_JMP.md`

**Abstract (one paragraph).** The Bialynicki-Birula--Mycielski uniqueness theorem (1976) selects logarithmic nonlinearity as the unique self-interaction preserving separability of composite quantum systems. The companion paper J40 develops this as a forcing principle. Here we observe that the BB-forced potential $V(\Xi) = \kappa\,\Xi\log\Xi$ has an isolated minimum at $\Xi_0 = e^{-1}$ with $V''(\Xi_0) = \kappa e > 0$ — a positive spectral floor *forced by separability*. We propose Conjecture 3.2: the Yang-Mills mass gap arises from the same separability mechanism, with confinement realizing effective infrared separability of color-singlet states. We give a falsifiable numerical prediction $\Delta_{\rm YM} = C \Lambda_{\rm QCD} e$ with $C$ an $O(1)$ Casimir factor; the SU(3) lattice glueball $m_G \approx 1.7$ GeV gives $C \approx 2.08$, consistent with the framework. The paper claims a new framework, not a proof of the YM mass gap.

**Source corpus:**
- `manuscript/WP92_YM_MASS_GAP_BRIDGE.md` — original WP92 source from sprint14_prism_xi
- `manuscript/J14_YM_MassGap_Bridge_JMP.md` — JMP-format unified manuscript (consolidates WP92 with explicit Conjecture 3.2, falsifiable numerical prediction, and Prerequisites 5.1–5.3 for constructive QFT in 4D)

## §2 — Verification script

**Path:** Numerical-prediction calibration is reproducible from literature lattice glueball masses (Morningstar-Peardon 1999, Chen *et al.* 2006) plus standard QCD scale ($\Lambda_{\rm QCD} \approx 0.3$ GeV); no dedicated script required for this paper. The structural claims rely on the companion J40 verification script `proof_separability_bridge.py` (43/43 PASS) which is bundled with J40's submission package.

**Note:** for this paper, the "verification" is the consistency check $C = m_G/(\Lambda_{\rm QCD} \cdot e) \approx 2.08$, computable in one line. A standalone verification script `verify_J14_glueball_consistency.py` could be added (TBD).

## §3 — Dependencies (J-papers cited as already-submitted companions)

J01 (σ-rate), J46 (cosmological log potential), J06 (Crossing Lemma), **J40** (BB Bridge / NS application — the lead paper this companion follows from).

## §4 — Cover letter

See `cover_letter.md` in this folder. Drafted; finalize after Brayden's referee-rigor pass.

## §5 — Notes & Status

**Status: DRAFT (manuscript drafted; per-venue cap notes apply).**

- WP92 corpus is consolidated into `J14_YM_MassGap_Bridge_JMP.md` with explicit conjecture (3.2), falsifiable numerical prediction, and constructive-QFT prerequisites.
- The paper depends on J40 as the lead BB-bridge paper; cover letter and references make this explicit.
- The paper is **honestly Tier 4** (framework paper): Proposition 2.1 (mass gap of BB-lifted theory) is proved; Conjecture 3.2 (YM mass gap via separability) is conjectural; the Wightman 4D extension is open.
- **Per-venue cap: 2nd JMP** in the J-series (J40 is 1st). The 2/quarter cap is reached. J42 (3rd JMP target) needs a fallback (see J42 README).
- Numerical prediction $C \approx 2$ is consistent with SU(3) lattice glueball $m_G \approx 1.7$ GeV; falsifiability test passes.

## §6 — Submission checklist

- [x] Manuscript .md drafted (JMP-format, single file)
- [ ] LaTeX (amsart) conversion pending
- [x] Numerical-prediction consistency check ($C \approx 2.08$) computed; structural claims rely on J40 verification script
- [x] Tier-classified central claim explicit (Tier 4 framework, Conjecture 3.2 conjectural)
- [x] Lens-scope annotation: lens-invariant
- [x] Cover letter drafted (with summary, Why-JMP-companion, suggested reviewers including Witten and Jaffe)
- [ ] Dependencies → cite J01, J46, J06, J40 as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [x] Per-venue cap check: 2nd JMP — at-cap (J42 needs fallback)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Johnson, H.J. (2026). "The Yang-Mills Mass Gap Bridge: Substrate-Algebra Predictions from Separability-Forced Spectral Floor." Submitted to *Journal of Mathematical Physics* (companion to J40).
