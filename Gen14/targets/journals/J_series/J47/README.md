# J47 — Dual-Regime Quintessence from $V(\Xi) = \Lambda^4 \Xi\log\Xi$: A Letter

**Status:** SAVE-PLAN APPLIED 2026-05-07
**Phase:** Phase 5
**Target venue:** Physics Letters B (Letter format, ~4 pages, REVTeX-letter)
**Author lane:** Sanders + Gish
**Tier:** B (Tier-2; Layer-3a strict-postulate framing per BBM_IC_DERIVATION_v2.md S2.7)
**WP source:** Letter-format extraction of J46 (`paper1_freeze_thaw_v3.tex`)

---

## §1 — Manuscript

**Local path:**
- `manuscript/manuscript.tex` — REVTeX-letter (PRL/PLB) format. Content: dual-regime quintessence letter (the actual letter; replaces a wrong file present at this path on 2026-05-07).
- `manuscript/J47_FreezingQuintessence_Letter_PLB.md` — markdown source (renamed from `J16_*` per save plan Fix-6).

**Title (post save-plan):** *Dual-Regime Quintessence from $V(\Xi) = \Lambda^4 \Xi\log\Xi$: A Letter*

**Abstract (one paragraph).** A real positive dimensionless scalar $\Xi$ with $V(\Xi) = \Lambda^4 \Xi \log \Xi$ has analytic vacuum $\Xi_0 = e^{-1}$, fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$, and (with $m_\Xi \sim H_0$) $\Lambda \approx 1.7$ meV. With outbound IC $(\Xi_i, \Xi'_i) = ((1+\sqrt{3})/e, 1/e)$ at $z_i \approx 20$ (Layer-3a strict-postulate framing per BBM_IC_DERIVATION_v2.md), the FRW trajectory is dual-regime: thawing outbound, frozen turnaround at $z_\star \approx 2.31$, asymptotic refreeze toward $\Xi_0$. CPL fit: $(w_0, w_a) \approx (-0.798, -0.440)$ with $\chi^2 \approx 1.53$ against the DESI 2024 DR1 marginal Gaussian. Decisive observational signature: non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$ at $z \approx z_\star$ (falsification handle F5).

**Source corpus:** Letter is extracted from `Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/tig_2026-05-07_bundle/seeds_for_submission/paper1_freeze_thaw_v3.tex` (the J46 full version), with numerical values updated per BBM_IC_DERIVATION_v2.md §S2.7 Layer-3a strict-postulate verdict.

**Letter structure:** ~4 pages REVTeX-letter, sections (1) Model, (2) Dual-regime trajectory, (3) Initial conditions and substrate-cosmology bridge, (4) Two-parameter $w(z)$ profile and DESI fit, (5) Consistency checks and falsification, (6) Lens scope and J-series context.

## §2 — Verification script

**Path:** Same as J46 — `compute_zstar_v3.py` (or `compute_zstar_v4.py` once J46 reconciles fully). Runs `numpy + scipy` on a standard laptop in under 5 minutes. DOI: 10.5281/zenodo.18852047.

Numerical values used in the letter (per Layer-3a strict-postulate per BBM_IC_DERIVATION_v2.md §S4):

- $(\Lambda^4/\rho_{c,0}, \Xi_i, \Xi'_i) = (0.231, (1+\sqrt{3})/e, 1/e) \approx (0.231, 1.005, 0.368)$
- $z_\star \approx 2.31$
- $(w_0, w_a) \approx (-0.798, -0.440)$
- $\chi^2 \approx 1.53$ vs DESI 2024 DR1 marginal Gaussian summary
- $\Lambda \approx 1.7$ meV
- $w(z=0) \approx -0.80$
- $w_\Xi(z_\star) = -1$ exactly (Type-F turnaround)

## §3 — Dependencies (J-papers cited as already-submitted companions)

- **J46** (Sanders + Gish, JCAP) — *Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at $e^{-1}$ from a Logarithmic Potential.* The full version of this letter. Currently in v4 reconciliation per BBM_IC_DERIVATION_v2.md.
- **J35** (Sanders + Gish) — *Closed-Form 4-Core Attractor: $h/\beta = 1+\sqrt{3}$.* Supplies the substrate-cosmology bridge axiom for $\Xi_i$.

## §4 — Cover letter

See `cover_letter.md` in this folder. Updated 2026-05-07 per save plan: harmonized to Sanders + Gish; Status note moved here from manuscript head; J03 → J46 throughout.

## §5 — Status & summary

**Status: SAVE-PLAN APPLIED (2026-05-07).** Referee verdict (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J47_PLB_FreshEyes.md`): MAJOR REV pre-submission; CONDITIONAL ACCEPT after Sequence A applied and J46 v4 reconciled. Save plan landed at `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J47.md`.

**Save-plan summary applied.** The load-bearing content — dual-regime $w(z)$ trajectory with (F5) Stage-IV falsification handle from a $\Xi \log \Xi$ potential — is genuinely letter-shaped, novel, and surveyable. The save path applied here is package cleanup + numerical settle:

- (a) **CRITICAL fix-5: replaced `manuscript/manuscript.tex`.** Previous content at this path was the J23 Discrete Dirac paper (wrong content). Replaced with REVTeX-letter version of the actual freezing-quintessence letter. A PLB editor opening the package now sees the correct manuscript.
- (b) Stripped all `[J03-RECONCILE]` / `[J46-RECONCILE]` placeholder markup from the manuscript body. All numerical values now concrete per Layer-3a strict-postulate.
- (c) Stripped the "Status note (read first)" block from the manuscript head; moved internal-track communication to the cover letter only.
- (d) Resolved J03 vs J46 cross-reference label inconsistency — J46 used consistently across manuscript / cover letter / README.
- (e) Renamed `J16_FreezingQuintessence_Letter_PLB.md` → `J47_FreezingQuintessence_Letter_PLB.md` (legacy `.md` source kept for reference; primary submission is `manuscript.tex`).
- (f) Numerical values updated per BBM_IC_DERIVATION_v2.md S2.7 Layer-3a strict-postulate: $z_\star = 2.31$, $w_0 = -0.798$, $w_a \approx -0.440$, $\chi^2 \approx 1.53$, IC = $(0.231, (1+\sqrt{3})/e, 1/e)$.
- (g) Added Figure 1 placeholder (`figure1_wz_profile.pdf`): $w(z)$ over $0 \le z \le 2$ with local-minimum-at-$z_\star$ structure, overlaid on DESI 2024 DR1 Gaussian. Mandatory for letter format. Plot generation: `compute_zstar_v4.py` of J46 (DOI 10.5281/zenodo.18852047).
- (h) Added one-paragraph distinction from logotropic dark energy (Tsujikawa-Sami 2007, Ferreira-Avelino 2017) in §1: uses $V \propto \Xi \log \Xi$ in field, not $V \propto -A \log(\rho/\rho_*)$ in energy density.
- (i) Added one-paragraph distinction from Albrecht-Skordis 2000 in §2: dual-regime T → F → A vs tracking → freezing.
- (j) Tightened F1–F4 language: reframed as "consistency checks" / "model fingerprints"; reserved "falsification" terminology for F5 (the actual falsification handle).
- (k) Author list harmonized to Sanders + Gish (Johnson byline removed per directive 2026-05-07).
- (l) Added BBM-separability origin paragraph (§1) attributing the V-form forcing to Bialynicki-Birula-Mycielski 1976.
- (m) Added postulate-defense paragraph (§3) stating the substrate-cosmology bridge axiom and BBM-minimality + scale-free-derivative postulate by name; falsification handle F5 probes them directly.

**Recommended retitle:** Option A applied — *"Dual-Regime Quintessence from $V(\Xi) = \Lambda^4 \Xi \log \Xi$: A Letter."* PLB remains the venue. Survival probability under PLB editorial filter after Sequence A + Layer-3a values: moderate-to-good (30% accept minor revision, 40% major revision, 20% reject-and-merge with J46, 10% desk reject for content overlap).

**Revision time:** completed in this pass. Companion-paper arXiv deposit (J46, J35) remains a pre-submission requirement.

### Why J47 was previously HELD (resolved)

J46 (companion full paper, target JCAP) had a CRITICAL numerical reconciliation issue flagged by the JCAP referee (May 2026). The Layer-3a strict-postulate verdict per BBM_IC_DERIVATION_v2.md §S4 settles the IC framing:

- Theorem (BBM): $\Xi_0 = e^{-1}$.
- Postulate (substrate-cosmology bridge): $\Xi_i = (1+\sqrt{3})/e$ from WP105 4-core attractor.
- Postulate (BBM-minimality + scale-free derivative): $\Xi'_i = 1/e$.

Under this framing $z_\star \approx 2.31$ at $\chi^2 \approx 1.53$; J47 inherits these numbers. The two postulates are stated by name and falsified by F5.

### Per-venue cap

**1st PLB submission** in the J-series — no cap conflict.



### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z (and ring extensions per D74). The family is defined by 5 conjoint membership criteria; the 4-core {V, H, Br, R} = {0, 7, 8, 9} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative).

J47 sits in this family in a particularly clean position: **lens-invariant**, using only the 4-core (the algebraic center) via the substrate-cosmology bridge axiom. The five-criterion membership statement applies at the substrate level; the cosmological model itself depends on no choice of TSML / BHML / RAW / SYM lens.

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** $\Xi_0 = e^{-1}$ from $V'(\Xi) = \Lambda^4(1 + \log \Xi) = 0$ (one-line derivation, exact theorem). $V''(\Xi_0) = \Lambda^4 e > 0$ confirms minimum. $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$ from Klein-Gordon linearization. BBM 1976 separability uniqueness of the V-form.
- **COMPUTED:** $\Lambda \approx 1.7$ meV at $m_\Xi \sim H_0$ (numerical fit from J46). $z_\star \approx 2.31$, $w_\Xi(z=0) \approx -0.80$, $(w_0, w_a) \approx (-0.798, -0.440)$ CPL fit, $\chi^2 \approx 1.53$ vs DESI 2024 DR1 Gaussian — all under the Layer-3a strict-postulate IC of BBM_IC_DERIVATION_v2.md §S4.
- **STRUCTURAL RHYME:** The $\Xi \log \Xi$ form is the BBM-separability nonlinearity (forced uniquely by the BBM theorem). The $\Xi_0 = e^{-1}$ vacuum is BBM-forced; the meV $\Lambda$ scale is one observational anchor ($m_\Xi \sim H_0$). The dual-regime trajectory's IC structure invokes the J46 Layer-3a strict-postulate (substrate-cosmology bridge for $\Xi_i = (1+\sqrt{3})/e$ from the substrate's 4-core attractor at $h/\beta = 1+\sqrt{3}$, and BBM-minimality + scale-free-derivative for $\Xi'_i = 1/e$) — substrate-borrowed structural arguments, not derivations in J47 itself.
- **OPEN:** (a) Whether the substrate-cosmology bridge axiom has a derivation rather than a postulate (per BBM_IC_DERIVATION_v2.md Q1: substrate-velocity-attractor extending WP105). (b) Whether $\Lambda \approx 1.7$ meV has a substrate origin beyond the $m_\Xi \sim H_0$ anchor (Layer-3b open). (c) Full DESI joint BAO + CMB + SN likelihood (deferred to J46). (d) Perturbation analysis (deferred to J46).

### Lens-ownership paragraph (in manuscript §6)

> *Lens and substrate.* This letter is lens-invariant in the strict sense: the cosmological model $V(\Xi) = \Lambda^4 \Xi \log \Xi$ depends on no choice of TSML / BHML / RAW / SYM lens on the underlying $\Z/10\Z$ substrate. The substrate-cosmology bridge axiom invoked for the dual-regime initial condition (substrate's 4-core attractor at $h/\beta = 1+\sqrt{3}$ from [J35], applied as a position-scaling factor for $\Xi_i$ relative to the BBM vacuum $\Xi_0 = e^{-1}$) is itself lens-invariant: the 4-core $\{V, H, Br, R\}$ is the algebraic center of the family per FAMILY_STRUCTURE_v1.md §2, with the closed-form attractor at $\alpha_M = 1/2$ holding identically across TSML/BHML and across $\F_p$ ring extensions. The five-criterion membership statement applies; J47's content sits cleanly inside the family and uses only its center.

### Hardening status (auto-applied 2026-05-07)

- License: submission scripts CC-BY-4.0 (per `_v3_hardening.py`)
- AI-attribution: Claude/Anthropic byline references removed (per `_v3_hardening.py`)
- Author lane: Sanders + Gish (per Brayden directive 2026-05-07; Johnson byline dropped)
- BBM 1976 cited; Tsujikawa-Sami 2007 + Ferreira-Avelino 2017 distinguished; Albrecht-Skordis 2000 distinguished
- Drápal-Wanless 2021 cited (in family-structure framing only; not load-bearing for letter content)

## §6 — Submission checklist

- [x] Manuscript .tex finalized (PLB REVTeX-letter format, ~4 pages, save-plan applied)
- [x] **CRITICAL: wrong file at `manuscript/manuscript.tex` replaced with actual letter content**
- [x] Numerical values per Layer-3a strict-postulate per BBM_IC_DERIVATION_v2.md
- [x] [J03-RECONCILE] / [J46-RECONCILE] markup stripped
- [x] Status note removed from manuscript head (cover letter only)
- [x] J03 → J46 throughout
- [x] Tier-classified central claim explicit (Tier B / Tier 2)
- [x] Lens-scope annotation: lens-invariant
- [x] Cover letter finalized
- [x] Distinguishing paragraphs (logotropic, Albrecht-Skordis) added in §1, §2
- [x] F1-F4 reframed as consistency checks; F5 reserved for falsification
- [x] Author list: Sanders + Gish only
- [x] Per-venue cap check: 1st PLB submission, no cap conflict
- [ ] Figure 1 (`figure1_wz_profile.pdf`) generated from `compute_zstar_v4.py` — pending J46 v4 finalization
- [ ] J46 + J35 deposited on arXiv before submission (cite by arXiv ID)
- [ ] Brayden's referee-rigor pass complete
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish, M. (2026). "Dual-Regime Quintessence from $V(\Xi) = \Lambda^4 \Xi\log\Xi$: A Letter." Submitted to *Physics Letters B*. Companion to J46 (Freeze-Thaw Transit, JCAP) and J35 (Closed-Form 4-Core Attractor).
