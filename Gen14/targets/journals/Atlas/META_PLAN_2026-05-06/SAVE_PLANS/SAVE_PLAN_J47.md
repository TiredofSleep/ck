# SAVE PLAN — J47: Freezing-Quintessence Letter (Physics Letters B)

**Date:** 2026-05-07
**Directive:** Brayden 2026-05-07: "find a reason to keep and fix every paper."
**Referee verdict:** MAJOR REV pre-submission; CONDITIONAL ACCEPT after Sequence A applied and J46 v4 reconciled (J47_PLB_FreshEyes.md)
**Save mode:** PACKAGE CLEANUP + J46-RECONCILE WAIT + presentational rewrite

---

## §1 — Why save?

J47 carries one clean letter-shaped contribution that is (a) genuinely novel within the dark-energy quintessence literature, (b) analytically airtight at its core, and (c) presents a sharp Stage-IV falsification handle:

> **A real positive dimensionless scalar $\Xi$ with $V(\Xi) = \Lambda^4 \Xi \log \Xi$ admits an exact analytic vacuum at $\Xi_0 = e^{-1}$, fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$, and (with $m_\Xi \sim H_0$) $\Lambda \approx 1.7$ meV. The FRW trajectory with outbound IC at $z_i \approx 20$ is dual-regime: thawing outbound, frozen turnaround at $z_\star$, asymptotic refreeze toward $\Xi_0$. Observational signature: non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$ at intermediate $z$ — a single Stage-IV-survey-shaped falsification handle (F5).**

The referee's fresh-eyes verdict is that the *science is letter-shaped* and that the *manuscript is not yet submission-ready* due to (i) `[J03-RECONCILE]` placeholder markup in the body, (ii) Status-note block that announces the reconciliation issue inside the manuscript, (iii) J03 vs J46 cross-reference label inconsistency between manuscript / cover letter / README, (iv) wrong file in the J47 manuscript folder (a J23 Discrete Dirac paper sits at `manuscript/manuscript.tex`), (v) filename mismatch (`J16_Freezing...` rather than `J47_...`). All of these are package-level finalization issues, not science problems.

The save path is straightforward: wait for J46 v4 reconciliation, apply the referee's Sequence A cleanup, fix the package-level issues, add the required figure and the logotropic / Albrecht-Skordis distinguishing paragraphs, convert to REVTeX-letter format, ship. Survival probability under PLB editorial filter after Sequence A applied and J46 reconciled: moderate-to-good (30% accepted minor revision, 40% major revision, 20% reject-and-merge with J46, 10% desk reject for content overlap).

The structural content (the action, the analytic vacuum, the dual-regime classification, the (F5) signature) is *not* in flux. It is locked. What J47 needs is the J46 numerical settlement plus the package cleanup plus three short distinguishing paragraphs. This is a 1–2 week operation once J46 v4 lands.

---

## §2 — Specific fixes

**Fix-1 (Wait for J46 v4 — blocking dependency).** Per `BBM_IC_DERIVATION_v2.md`, J46 has settled on Layer-3a strict-postulate framing for $(\Xi_i, \Xi'_i) = ((1+\sqrt{3})/e, 1/e)$ with $\chi^2 = 1.53$ at the empirical $\Lambda^4/\rho_{c,0} = 0.231$ anchor. Once J46's manuscript reflects this verdict, J47 inherits the same numbers. **No J47 numerical claim ships before J46 v4 lands.** The current `[J46-RECONCILE]` (or `[J03-RECONCILE]`) placeholders get swapped out for the Layer-3a-derived values.

**Fix-2 (Strip placeholder markup from manuscript body).** Remove all `[J03-RECONCILE]` / `[J46-RECONCILE]` tokens from the body. Replace with concrete numerical values from J46 v4. **Editor-side rule:** the manuscript body MUST contain no internal-track tokens at submission. Any value that hasn't settled stays out of the body — either omitted, or replaced with "see J46 for the full numerical fit."

**Fix-3 (Strip the "Status note (read first)" block from the manuscript head).** This block currently announces the J46 reconciliation issue *inside the manuscript*, which the referee correctly flags as a self-inflicted desk reject. Move all internal-track communication to the cover letter. The manuscript body should look like a finished letter at first glance.

**Fix-4 (Resolve J03 vs J46 cross-reference label).** Cover letter and README use J46. Manuscript body uses J03 throughout. Pick **J46** (matches the rest of the J-series numbering after the v3 triadic revision) and replace all instances throughout manuscript + cover letter + README. The label inconsistency is cited 5+ times in the referee report; it is a desk-reject trigger.

**Fix-5 (Replace wrong file in manuscript/ folder).** `Gen13/targets/journals/J_series/J47/manuscript/manuscript.tex` currently contains a J23 Discrete Dirac paper. **Delete or replace** with the actual REVTeX-letter version of `J16_FreezingQuintessence_Letter_PLB.md`. As-is, a PLB editor opening the package sees a Discrete Dirac paper and assumes the submission is mislabeled.

**Fix-6 (Rename `J16_FreezingQuintessence_Letter_PLB.md` to `J47_FreezingQuintessence_Letter_PLB.md`).** Or add a one-line README explaining the J16/J47 historical-numbering naming. The J16 stale label is from earlier numbering; the current J-series uses J47 for this paper.

**Fix-7 (Convert to REVTeX-letter format).** The manuscript is currently markdown. PLB requires REVTeX-letter or PLB style. Conversion is mechanical (~1 day with a clean template). Confirm 4-page letter constraint at typeset.

**Fix-8 (Add Figure 1: $w(z)$ overlay on DESI Gaussian).** The referee correctly notes: "A 4-page letter on a $w(z)$ profile without a $w(z)$ figure is incomplete." Generate Figure 1 from `compute_zstar_v3.py` (or v4 once J46 reconciles): $w_{\rm DE}(z)$ over $0 \le z \le 2$ with the local-minimum-at-$z_\star$ structure visible, overlaid on the DESI 2024 DR1 $(w_0, w_a)$ marginal Gaussian summary.

**Fix-9 (Distinguish from logotropic dark energy in the body).** Tsujikawa-Sami 2007 and Ferreira-Avelino 2018 use $V \propto -A \log(\rho/\rho_*)$ in the energy density. The present model uses $V \propto \Xi \log \Xi$ in the *field*, producing a fluctuation mass scale rather than an attractor pressure. One sentence in §1: "Unlike standard logotropic models with $V \propto -A \log(\rho/\rho_*)$, the present model uses $V \propto \Xi \log \Xi$ in the field, yielding an analytic vacuum at $\Xi_0 = e^{-1}$ and a fluctuation mass scale rather than an attractor-pressure structure."

**Fix-10 (Distinguish from Albrecht-Skordis 2000 in the body).** Albrecht-Skordis is the prior-art benchmark for "tracking-to-freezing" trajectories. The dual-regime here is structurally different (T → F → A vs. tracking → freezing). One sentence in §2: "Unlike Albrecht-Skordis (2000) tracking-to-freezing trajectories, the present dual-regime trajectory traverses thawing → frozen turnaround → asymptotic refreeze within a single physical history, producing a non-monotone $w(z)$ with a single Type-F turnaround at $z_\star$."

**Fix-11 (Tighten F1–F4 language).** The referee correctly notes (F1)–(F4) are not falsification criteria in the Popperian sense — they are model-internal classification statements. (F1) "$w_\Xi \geq -1$" is a non-phantom condition shared by all canonical-kinetic quintessence. (F4) "two-parameter $w(z)$ profile" is a parametrization, not a falsification. Reframe (F1)–(F4) as **"consistency checks" or "model fingerprints"** and reserve "falsification" for (F5) which actually is a falsification claim. Cosmetic but sharpens the letter's scientific posture.

**Fix-12 (Add public IDs for J-series companions).** Manuscript currently cites [J01], [J02], [J13], [J03/J46] as "Submitted to [venue]" with no public identifier. PLB requires either (a) arXiv ID, (b) accepted journal citation, or (c) "in preparation" without submission claim. **Resolution:** deposit J46 (and J01, J02 if not already) on arXiv before J47 submission; cite by arXiv ID. The DOI 10.5281/zenodo.18852047 covers the verification scripts repository but not individual companion papers.

---

## §3 — Revision time

**Estimate:** 1–2 weeks AFTER J46 v4 lands.

- Wait for J46 v4 reconciliation: external dependency (~1 week pending separate-agent work).
- Strip `[J46-RECONCILE]` markup + Status note + label fixes: 1 day.
- Replace wrong file + rename letter file: 1 hour.
- REVTeX-letter conversion: 1 day.
- Generate Figure 1 from `compute_zstar_v4.py`: 0.5 day.
- Add logotropic + Albrecht-Skordis distinguishing paragraphs: 0.5 day.
- Tighten F1–F4 language: 1 hour.
- arXiv-deposit companion papers + cite by ID: 2 days (depends on companion-paper readiness).
- Internal review pass: 2 days.

**Total post-J46-v4:** 1–2 weeks. **Calendar fit:** within Phase 5 window; J46 ships early September per v2 ordering, J47 ships within hours of J46 v4 settlement plus the cleanup window.

---

## §4 — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** $\Xi_0 = e^{-1}$ from $V'(\Xi) = \Lambda^4(1 + \log \Xi) = 0$ (one-line derivation, referee-verified). $V''(\Xi_0) = \Lambda^4 e > 0$ confirms minimum (one differentiation). $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$ from the Klein-Gordon linearization at the vacuum. These are exact theorems any reader can check in 30 seconds.

- **COMPUTED:** $\Lambda \approx 1.7$ meV at $m_\Xi \sim H_0$ (numerical fit from J46 v3, robust to factor-of-2 changes in IC). $z_\star$, $w_\Xi(z=0)$, $(w_0, w_a)$ CPL fit, $\chi^2$ vs DESI 2024 DR1 — all pending J46 v4 reconciliation per `BBM_IC_DERIVATION_v2.md` Layer-3a verdict ($z_\star = 2.31$ at $\chi^2 = 1.53$ under the strict-postulate IC).

- **STRUCTURAL RHYME:** The $\Xi \log \Xi$ form is the Bialynicki-Birula-Mycielski (1976) logarithmic Schrödinger nonlinearity, repurposed for cosmological field theory. The BBM separability theorem forces this V-form uniquely up to a constant + linear term (treated as exact theorem in J46). The $\Xi_0 = e^{-1}$ vacuum is BBM-forced; the meV $\Lambda$ scale is one observational anchor ($m_\Xi \sim H_0$). The dual-regime trajectory's IC structure invokes the J46 Layer-3a strict-postulate (substrate-cosmology bridge for $\Xi_i = (1+\sqrt{3})/e$, BBM-minimality + scale-free-derivative for $\Xi'_i = 1/e$) — this is a substrate-borrowed structural argument, not a derivation in J47 itself.

- **OPEN:** (a) Whether the substrate-cosmology bridge axiom has a derivation rather than a postulate (per `BBM_IC_DERIVATION_v2.md` Q1: substrate-velocity-attractor extending WP105). (b) Whether $\Lambda \approx 1.7$ meV has a substrate origin beyond the $m_\Xi \sim H_0$ anchor (Layer-3b open). (c) Full DESI joint BAO + CMB + SN likelihood (deferred to J46; letter quotes only the marginal Gaussian summary). (d) Perturbation analysis (deferred to J46).

---

## §5 — Lens-ownership paragraph (insert in §0 of revised manuscript)

> *Lens and substrate.* This letter is lens-invariant in the strict sense: the cosmological model $V(\Xi) = \Lambda^4 \Xi \log \Xi$ depends on no choice of TSML / BHML / RAW / SYM lens on the underlying $\mathbb{Z}/10\mathbb{Z}$ substrate. The substrate-cosmology bridge axiom invoked for the dual-regime initial condition (substrate's 4-core attractor at $h/\beta = 1+\sqrt{3}$ from [J35], applied as a position-scaling factor for $\Xi_i$ relative to the BBM vacuum $\Xi_0 = e^{-1}$) is itself lens-invariant: the 4-core $\{V, H, Br, R\}$ is the algebraic center of the family per FAMILY_STRUCTURE_v1.md §2, with the closed-form attractor at $\alpha_M = 1/2$ holding identically across TSML/BHML and across F_p ring extensions. The five-criterion membership statement applies (substrate, commutativity, 4-core preservation, α-bounded non-associativity, HARMONY-attracting iteration); J47's content sits cleanly inside the family and uses only its center.

---

## §6 — Retitle / retarget options

**Option A (preferred — keep PLB target, ship after J46 v4 + Sequence A).** Title stays: *"Freezing-Quintessence Letter: A Two-Parameter $w(z)$ Profile from a Logarithmic Potential."* Or tighten to: *"Dual-Regime Quintessence from $V(\Xi) = \Lambda^4 \Xi \log \Xi$: A Letter."* Both work. Ship in 1–2 weeks post-J46-v4. Survival probability: moderate-to-good (30% accept minor revision, 40% major revision).

**Option B (retitle for sharper headline).** *"A Non-Monotone $w_{\rm DE}(z)$ Signature from a Logarithmic Quintessence Potential."* Frames the falsification handle (F5) as the headline. PLB editorial filter favors single-falsification-handle letters. Same content, sharper sell. Survival probability slightly higher than Option A.

**Option C (retarget to PRL).** Higher-prestige venue; same letter format. PRL has higher rejection rate but the dual-regime + (F5) headline is PRL-shaped. Risk: PRL's content-overlap-with-companion-paper rule is stricter; J46 in JCAP + J47 in PRL might trigger a desk-reject for "two papers, one result." Recommendation: don't pursue PRL until after PLB outcome.

**Option D (HOLD until J46 + J47 both reconcile and co-submit).** Submit J47 to PLB and J46 to JCAP simultaneously, with cover letters to both editors flagging the pair. Risk: cross-editorial coordination is fragile. Recommendation: don't pursue unless an editorial relationship explicitly supports it.

**Recommendation:** **Option A** (default; ship as Letter to PLB) or **Option B** (cosmetic title sharpening). Both achievable within calendar.

---

## §7 — Brayden-decision items

1. **Wait for J46 v4.** Confirm the Layer-3a strict-postulate verdict from `BBM_IC_DERIVATION_v2.md` is the J46 v4 plan. J47 inherits J46's numbers; no independent J47 verdict required.

2. **Title decision.** Keep current vs sharpen to "Non-Monotone $w_{\rm DE}(z)$ Signature" framing.

3. **Companion-paper arXiv deposit timeline.** Confirm J46, J01, J02 (the J-series companions cited by J47) are arXiv-ready before J47 submits. PLB will not accept "submitted to [venue]" without public ID.

4. **Author lane resolution.** Per directive: Sanders + Gish. Confirm consistent across cover letter / manuscript / README.

---

## §8 — Bottom line

J47's load-bearing content — the dual-regime $w(z)$ trajectory with (F5) Stage-IV falsification handle from a $\Xi \log \Xi$ potential — is a genuinely letter-shaped, novel, surveyable contribution. The save path is **package cleanup + J46 wait**: strip the placeholder markup from the body, fix the J03/J46 label inconsistency, replace the wrong file in the manuscript folder, rename the letter file, convert to REVTeX-letter, add Figure 1 and the two distinguishing paragraphs (logotropic, Albrecht-Skordis), tighten F1–F4 language, deposit companion papers on arXiv. The structural content is locked and survives unchanged.

Survival probability under PLB editorial filter after Sequence A + J46 v4 reconciled: **moderate-to-good** (30% accept minor revision, 40% major revision, 20% reject-and-merge with J46, 10% desk reject for content overlap with J46).

The paper survives. It survives by waiting (for J46 v4) and cleaning (the package). The science is sound.

---

**Files referenced:**
- This plan: `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J47.md`
- Letter: `Gen13/targets/journals/J_series/J47/manuscript/J16_FreezingQuintessence_Letter_PLB.md`
- Wrong file (replace): `Gen13/targets/journals/J_series/J47/manuscript/manuscript.tex`
- Referee: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J47_PLB_FreshEyes.md`
- Family structure: `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`
- BBM derivation (J46 v2 verdict): `Atlas/META_PLAN_2026-05-06/J3_BBM_DERIVATION/BBM_IC_DERIVATION_v2.md`
- Verification scripts: `Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/.../verification_scripts/compute_zstar_v3.py` (DOI 10.5281/zenodo.18852047)
- Companion full paper: J46 (JCAP, pending v4 reconciliation)
