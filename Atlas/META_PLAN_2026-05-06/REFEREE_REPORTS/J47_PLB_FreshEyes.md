# Referee Report — J47: Freezing-Quintessence Letter
## Target venue: *Physics Letters B* (Letter format, ~4 pages)

**Manuscript reviewed:** `Gen13/targets/journals/J_series/J47/manuscript/J16_FreezingQuintessence_Letter_PLB.md`
**Companion full version:** J46 (submitted to JCAP; currently under "CRITICAL numerical reconciliation" referee report)
**Stated WP source:** Letter-format extraction of `paper1_freeze_thaw_v3.tex`
**Cover letter:** `Gen13/targets/journals/J_series/J47/cover_letter.md`
**Folder anomaly noted:** the file `manuscript/manuscript.tex` in the J47 folder is unrelated content (a J23 "Discrete Dirac on F_5^4" paper) — not the freezing-quintessence letter. Confirmed the actual letter is the `.md` file. Flagged in §8 below as a submission-package risk.

**Reviewer disposition:** I evaluate this letter assuming I have never heard of any framework behind it. I am asked specifically whether the dual-regime $w(z)$ profile is a clean PLB Letter, regardless of the J46 numerical reconciliation issue. My verdict is: **structurally, it is close to a clean letter, but it is presently in HOLD status with internal placeholders, and as written it would be desk-rejected at PLB for three reasons that go beyond the held numbers.** Recommendation: **MAJOR REVISION before submission, conditional on (i) J46 v4 reconciliation, (ii) removing the explicit `[J03-RECONCILE]` markup from the body, and (iii) replacing the `J03` / `J16` cross-reference labels (which are inconsistent) with a single stable companion citation.** Detailed rationale follows.

---

## §1 — Manuscript Summary

The letter proposes a dark-energy scalar $\Xi$ with potential $V(\Xi) = \Lambda^4 \Xi \log \Xi$, evaluated as a quintessence model in a flat FRW background with present-day $H_0$.

Core analytic claims (presented as exact theorems):
- The minimum of $V$ sits at $\Xi_0 = e^{-1}$.
- The fluctuation mass is $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$.
- Tuning $m_\Xi \sim H_0$ gives $\Lambda \approx 1.7$ meV.

Core numerical/observational claims (currently held):
- Outbound IC at $z_i \approx 20$ produces a *dual-regime* trajectory: thawing $\to$ frozen turnaround at $z_\star$ $\to$ asymptotic refreeze.
- $w_\Xi(z=0) \approx -0.79$.
- CPL fit gives $(w_0, w_a) \approx (-0.79, -0.71)$.
- $\chi^2$ value vs DESI 2024 DR1 Gaussian summary: placeholder.

Falsification list (F1)–(F5) culminating in (F5) "local minimum of $w_{\rm DE}(z)$ near $-1$ at intermediate $z$" — claimed as the decisive Stage-IV survey signature.

Letter is ~4 pages in target form; sections (1) Model, (2) Dual-regime trajectory, (3) Two-parameter $w(z)$ profile, (4) Falsification, (5) Status/scope/J-series context.

---

## §2 — Is the dual-regime $w(z)$ profile clean letter format? (THE KEY QUESTION)

**Structurally yes; presentationally no.** Three independent reasons.

### §2.1 — The science is letter-shaped

The paper does have one clean, letter-shaped contribution:

> A specific simple potential $V \propto \Xi \log \Xi$ admits an exact analytic vacuum at $\Xi_0 = e^{-1}$ and a one-parameter mass scale $\Lambda \sim 1.7$ meV at the dark-energy scale, leading to a *non-monotone* $w_{\rm DE}(z)$ that distinguishes itself from both freezing and thawing single-regime quintessence by a local minimum near $-1$.

That is a single, falsifiable, surveyable headline result. It fits PLB's letter format in spirit: one clean potential, one analytic feature, one observational signature, one falsification handle. PLB has a strong recent track record of publishing this kind of two-parameter dark-energy parametrization paper. The Albrecht-Skordis tracking-to-freezing precedent is the right comparison, and it would be the natural review benchmark.

If the manuscript stopped at the action plus the analytic vacuum plus (F5), and quietly cited J46 for full numerics, this would be a natural Letter.

### §2.2 — The presentation is not yet letter-clean

Three concrete presentational problems push it below the desk-acceptance threshold:

**(a) `[J03-RECONCILE]` placeholders in the running text.** Section 2 contains literally `z_\star$ \[J03-RECONCILE\]`, Section 3 contains `(w_0, w_a) \approx (-0.79, -0.71)$ \[J03-RECONCILE\]` and `\chi^2 = $ \[J03-RECONCILE\]`, and Section 4 likewise. A PLB editor will see these and assume the paper is not in submission-ready state. This is not a referee-revision issue — it is an artifact of submitting a manuscript that has not yet been finalized. **No editor at PLB will read past the abstract if the body has bracketed-uppercase status tokens in it.** Letters have to look like letters at first glance.

**(b) The "Status note (read first)" block at the top.** A 6-line italicized block telling PLB editors that this letter "is the 4-page extraction of the companion paper J03" and that "the numerical claims must be reconciled with whatever J03 settles on after the JCAP referee report's CRITICAL numerical reconciliation issue is resolved" — *in the manuscript itself* — is a self-inflicted desk reject. This is internal-track communication that should be in the cover letter (and only the cover letter, and only with a softer phrasing). PLB does not publish letters that announce in their second sentence that their numerical claims are under reconciliation elsewhere.

**(c) Inconsistent cross-reference label.** The cover letter calls the companion full paper "J46" five times. The README also calls it "J46." The manuscript header line 9 says "(numerical claims extracted from companion full paper J03)." Manuscript line 11 says "DEPENDS_ON_J03." Manuscript footnote line 15 references "the companion paper J03 (Sanders, Gish, Johnson 2026...)" — but the README and cover letter say the companion is J46. This is a real inconsistency, not a typo: the labels J03 and J46 are used for the same paper across the package. A reader cannot tell which is the citing label and which is the cited label without checking the README. **Pick one, and use it consistently throughout the manuscript, cover letter, and README.**

### §2.3 — The dual-regime claim, once cleaned, is appropriate for PLB

After (a)/(b)/(c) are resolved and the J46 numbers reconcile, the remaining science is letter-appropriate:

- The action and the $\Xi_0 = e^{-1}$ vacuum are exact, three-line derivations; PLB readers can verify on the back of an envelope.
- The fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$ is one differentiation step from the vacuum.
- The dual-regime trajectory (T → F → A) is a clean classification statement and the only numerical content.
- The two-parameter CPL approximation is the standard observational handle PLB readers expect.
- Falsification (F5) is a single Stage-IV-survey-shaped sentence ("look for a local minimum of $w_{\rm DE}(z)$ near $-1$ at intermediate $z$").

This is a reasonable PLB letter once (a)/(b)/(c) are fixed.

---

## §3 — Substance of the analytic claims (lens-free reading)

I evaluate the analytic theorems on their own terms, with no framework assumed.

### §3.1 — The $\Xi_0 = e^{-1}$ vacuum

Setting $V'(\Xi) = \Lambda^4 (1 + \log \Xi) = 0$ gives $\Xi_0 = e^{-1}$. Setting $V''(\Xi_0) = \Lambda^4 / \Xi_0 = \Lambda^4 e > 0$ confirms this is a minimum. **Verified by direct calculation; this is an exact statement that any reader can check in 30 seconds.** The statement is mathematically correct as written.

The $V(\Xi) = \Xi \log \Xi$ potential is not new — it is the Bialynicki-Birula-Mycielski (1976) logarithmic Schrödinger nonlinearity, repurposed here for cosmological field theory. The authors cite this in their reference list, which is correct attribution. The novelty in this paper is the *cosmological* application (BB used it as a quantum-mechanical nonlinearity).

The Tsujikawa-Sami (2007) and Ferreira-Avelino (2018) "logotropic" precedents need to be addressed *in the body of the letter*, not just in the bibliography. PLB readers will immediately ask: *how is this distinct from logotropic dark energy?* If the answer is "the IC structure produces a non-monotone $w(z)$ while the logotropic models do not," that should be one sentence in the body.

### §3.2 — $\Lambda \approx 1.7$ meV scale

Tuning $m_\Xi \sim H_0$ gives $\Lambda = (m_\Xi^2 M_{\rm Pl}^2 / e)^{1/4}$. With $m_\Xi \sim H_0 \sim 1.5 \times 10^{-33}$ eV and $M_{\rm Pl} \sim 2.4 \times 10^{18}$ GeV, this gives $\Lambda \sim (10^{-66} \cdot 10^{36})^{1/4} \sim (10^{-30})^{1/4}$ meV. The arithmetic checks out at one-significant-figure precision. The "1.7 meV" specific value comes from J46 v3 numerics and is one of the quantities flagged for J46 reconciliation. Reviewer cannot verify the trailing digit without J46 reconciliation, but the $\sim$meV scale is robust to factor-of-2 changes.

### §3.3 — Dual-regime trajectory

The qualitative classification (T → F → A) is well-defined: thawing then frozen turnaround then asymptotic refreeze toward the vacuum. The quantitative claim — that this happens at $z_\star \approx 1.3$ (v3) or $z_\star \approx 2.131$ (referee-independent execution per the JCAP report) — is currently in dispute and **cannot be evaluated without J46 v4**. The factor-of-2 difference between $z_\star \approx 1.3$ and $z_\star \approx 2.131$ is a substantial observational statement (the difference between a turnaround inside Stage-IV survey range vs. just outside it), and **(F5) becomes a different falsification claim depending on which $z_\star$ is correct**. This is the heart of the JCAP referee's substantive concern, and it cannot be deferred away in the PLB letter.

### §3.4 — CPL fit

CPL is the right format. The $(w_0, w_a) \approx (-0.79, -0.71)$ values are flagged for reconciliation. The note that "the $\chi^2$ here quantifies proximity to the *published* $(w_0, w_a)$ marginal Gaussian and is not derived from the underlying joint BAO + CMB + SN likelihood" is honest and appropriate; PLB readers will accept this scoping if the wording is preserved.

### §3.5 — Falsification list

(F1)–(F4) are not falsification criteria in the usual Popperian sense — they are model-internal classification statements. (F1) "$w_\Xi \geq -1$ for $z \geq 0$" is a non-phantom condition shared by all canonical-kinetic quintessence models. (F4) "two-parameter $w(z)$ profile" is a parametrization statement, not a falsification statement. **The letter should describe (F1)–(F4) as "consistency checks" or "model fingerprints" and reserve "falsification" for (F5), which actually is a falsification claim.** This is a cosmetic edit but it sharpens the letter's scientific posture.

(F5) is the real falsification handle and is correctly stated. The single sentence "Detection of monotone $w(z)$ across the full observable redshift range *would* falsify (F5)" is the kind of one-sentence falsification statement PLB rewards.

---

## §4 — Letter format compliance

PLB Letter format: ~4 pages, single-column, REVTeX-letter or PLB style. Currently the manuscript is markdown, which is not the submission format. The README §6 acknowledges "LaTeX (revtex4) conversion pending."

**Word count.** Approximating the markdown at ~750 words for the body plus abstract, the typeset version should fit comfortably in 4 pages.

**References.** The manuscript cites 18 references across quintessence, DESI, Bialynicki-Birula, and J-series companions. PLB letters tolerate 20–30 references; this is fine. **However:** the J-series internal references (J01, J02, J13, J03/J46) are listed as "submitted to [venue]" with no public identifier. PLB requires actual references — at minimum a preprint number (arXiv ID) or a stable repository URL. The DOI 10.5281/zenodo.18852047 is given for verification scripts but not for the companion papers themselves. **Each cited J-paper needs to be either (a) on arXiv with an ID, (b) accepted with a journal citation, or (c) cited as "Sanders et al., in preparation" with no submission claim.** "Submitted to [venue]" without a public copy is not a citation PLB will accept.

**Equations.** The model equation (the action) and the EL equation are clean. No display equation is excessively wide.

**Figures.** None included. The dual-regime $w(z)$ curve **must** be shown as Figure 1 in any PLB version of this letter. A 4-page letter on a $w(z)$ profile without a $w(z)$ figure is incomplete. The figure should overlay the model curve on the DESI 2024 DR1 $(w_0, w_a)$ Gaussian summary.

---

## §5 — What's missing for PLB acceptance

Three additions, each one-paragraph:

1. **Distinction from logotropic dark energy** (Tsujikawa-Sami 2007, Ferreira-Avelino 2018). One sentence in §1 saying "Unlike standard logotropic models with $V \propto -A \log(\rho/\rho_*)$ in the energy density, the present model uses $V \propto \Xi \log \Xi$ in the *field*, producing a fluctuation mass scale rather than an attractor pressure." (Or whatever the actual distinction is — but the distinction needs to be in the body.)

2. **The $w_{\rm DE}(z)$ figure** as discussed in §4.

3. **Distinction from Albrecht-Skordis** (cited in references but not addressed in the body). Albrecht-Skordis is the prior-art benchmark for "tracking-to-freezing" trajectories. The dual-regime here is structurally different (T → F → A vs. tracking → freezing) but PLB readers will assume similarity unless the letter says otherwise. One sentence in §2.

---

## §6 — Recommended decision sequence

Given the J46 hold and the presentational issues:

**Sequence A (recommended):**
1. Wait for J46 v4 reconciliation.
2. Strip the `[J03-RECONCILE]` markup and the Status note from the manuscript body.
3. Resolve the J03/J46 label inconsistency.
4. Convert to REVTeX-letter; add Figure 1 ($w(z)$ overlay on DESI Gaussian).
5. Address logotropic and Albrecht-Skordis precedent in body (one sentence each).
6. Tighten (F1)–(F4) language ("consistency checks" not "falsification").
7. Submit.

**Sequence B (do not recommend):** Submit now with placeholders. Outcome: desk reject within 48 hours with editor note "manuscript not in submission-ready state." The cost is one PLB submission slot for the senior author and a small reputational ding.

---

## §7 — Survival probability under PLB editorial filter

If submitted in current form: **near-zero** survival. Desk reject probability ~85% on the placeholder text alone.

If submitted with Sequence A applied and J46 v4 reconciled to consistent numbers: **moderate-to-good** survival. PLB has published comparable two-parameter $w(z)$ letters in the dark-energy series (Caldwell-Linder 2005, Linder 2003, Tsujikawa-Sami 2007). The (F5) Stage-IV falsification handle is exactly the kind of headline PLB rewards. A sympathetic editor would assign this to one of the suggested reviewers (Linder, Caldwell, Albrecht, Starobinsky, or a DESI member), and the review would focus on:
- Reproducibility of the $w(z)$ curve (the J46 reconciliation has to land first).
- Distinction from Albrecht-Skordis and logotropic dark energy.
- Coverage of the perturbation analysis (which the letter defers to J46).
- Consistency with DESI BAO + CMB joint constraints, not just the marginal Gaussian.

Realistic review outcomes after Sequence A:
- **30%:** accepted with minor revision.
- **40%:** major revision (most likely concerns: distinguishing from logotropic; perturbation analysis required even in letter form; full DESI joint likelihood).
- **20%:** reject with referral to a longer-format venue (PRD or JCAP — but JCAP already has the long version as J46, so this is effectively "reject and merge with J46").
- **10%:** desk reject for substantial content overlap with J46 (if the JCAP editor and PLB editor flag the overlap).

---

## §8 — Submission-package issues (independent of science)

Five items the package needs before submission:

1. **The `manuscript/manuscript.tex` file in the J47 folder is the wrong content.** It is a paper titled "Discrete Dirac on F_5^4: Substrate Algebra of the 4-Core" — a J23-class algebraic paper, not the J47 freezing-quintessence letter. Either delete this file from the J47 submission package or replace it with the actual REVTeX-letter version of `J16_FreezingQuintessence_Letter_PLB.md`. As-is, a PLB editor opening the package will see a Discrete Dirac paper and assume the submission is mislabeled.

2. **File-naming inconsistency.** The actual letter file is `J16_FreezingQuintessence_Letter_PLB.md`. The folder is `J47`. The README references "J47 — Freezing-Quintessence Letter". The `J16` filename is presumably a stale label from earlier numbering. **Rename the file to match the J47 folder, or add a one-line README note explaining the J16/J47 naming.**

3. **J03 vs J46 inconsistency.** Already noted in §2.2(c). The cover letter uses J46. The manuscript uses J03 throughout. The README uses J46. Pick one.

4. **Per-venue cap.** README says "1st PLB submission in the J-series — no cap conflict." Verified — no other J-paper is targeted at PLB. Good.

5. **Author affiliations.** "Independent Researcher, Hot Springs, AR" and "Independent Researcher, Billings, MT" are valid, but PLB will flag two distinct independent-researcher affiliations on a three-author paper. Not a desk reject; just a soft note.

---

## §9 — Final disposition

**Verdict on the science:** the dual-regime $w(z)$ profile is a clean, letter-shaped contribution once the J46 reconciliation lands and the placeholders are resolved. The model is structurally distinct from canonical freezing/thawing quintessence (the dual T → F → A trajectory is the genuine novelty), and (F5) is a real Stage-IV falsification handle.

**Verdict on the manuscript as currently constituted:** **NOT submission-ready.** The internal-track placeholder markup, the in-body status note, the J03/J46 label inconsistency, and the wrong file in the manuscript folder add up to "package not ready." This is **not** a science problem; it is a finalization problem.

**Recommendation:** **MAJOR REVISION** in the meta-sense (i.e., before submission). Specifically:

1. Wait for J46 v4 reconciliation (the JCAP referee's CRITICAL numerical issue must close first; the letter cannot lock its numbers until J46 settles).
2. Apply the Sequence A cleanup in §6.
3. Resolve the §8 submission-package issues.
4. Then submit. The science holds.

**Tier classification.** Reviewer agrees with the README's Tier B / Tier 2 contingent classification: the action and analytic vacuum are exact theorems (Tier A content); the dual-regime trajectory is a numerical claim conditional on J46 reconciliation (Tier B). The honesty of this self-classification is a credit to the package.

**One last note.** The WP-source line in the README says "Letter is extracted from `Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/...paper1_freeze_thaw_v3.tex`." That file path is internal-track. PLB readers cannot resolve it. After J46 ships to JCAP, the public reference becomes "Sanders, Gish, Johnson 2026 (JCAP, in press)" or the arXiv ID. Update this line in the README and the manuscript before submission.

---

**Reviewer signature:** Anonymous referee, PLB.
**Date of review:** 2026-05-07.
**Recommendation:** MAJOR REVISION (pre-submission); CONDITIONAL ACCEPT after Sequence A applied and J46 v4 reconciled.
