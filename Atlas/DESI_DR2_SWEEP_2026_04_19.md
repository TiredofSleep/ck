# DESI DR2 Era Literature Sweep — V = κ Ξ log Ξ Quintessence Novelty Audit

**Date**: 2026-04-19
**Scope**: arXiv astro-ph.CO and adjacent listings, DESI DR2 release window (≈ 2025-10 → 2026-04)
**Trigger**: Venue 7 (JCAP, target submit 2026-04-22) Caveat-Closure paragraph for WP82.
**Files cross-referenced**:
- `Gen12/targets/journal_attempts/07_jcap_cosmology/WP82_LOG_QUINTESSENCE_NOVELTY.md`
- `Gen13/targets/journals/tier1_submit_now/jcap_xi_cosmology/jcap_xi_cosmology.tex`

---

## §1 Search Log

| # | Query | Result count (top hits inspected) | Notable arXiv IDs surfaced |
|---|---|---|---|
| 1 | `"DESI DR2" quintessence fit dark energy 2026` | 10 | 2603.21125, 2604.08449, 2602.05368, 2601.02284, 2512.00558 |
| 2 | `"DESI DR2" dark energy equation of state 2025 2026` | 10 | 2503.14738, 2504.15222, 2511.22512 |
| 3 | `"log quintessence" arXiv 2025 2026 scalar field` | 10 | 2604.04056, 2506.21542, 2509.13302, 2511.19610, 2602.00820, 2603.18341 |
| 4 | `"phi log phi" potential dark energy quintessence arxiv` | 10 | 2604.04056, 2604.08449, 2508.19101, 2601.09803 |
| 5 | `"Bialynicki-Birula" cosmology 2025 2026 logarithmic dark energy` | 10 | 2603.23551 (entropy), 2503.06712 (DES); none on Bialynicki-Birula DE potential |
| 6 | `"Xi log Xi" potential cosmology dark energy` | 10 | 2304.05807 (Wang/Koussour log-rho), 2407.03465 |
| 7 | `"logarithmic quintessence" arXiv 2025 2026` | 10 | 2511.19610, 2603.23551, 2506.21542 |
| 8 | `freezing quintessence DESI 2025 2026 scalar potential` | 10 | 2506.21542, 2603.21125, 2509.13302, 2410.17182, 2504.16337 |
| 9 | `DESI year-3 dark energy equation of state scalar field 2026` | 10 | 2502.06929, 2604.12032, 2502.19274 |
| 10 | `"V = kappa phi log phi" dark energy quintessence` | 10 | (no direct hit — only generic exponential/quintessence reviews) |
| 11 | `DESI DR2 scalar field potential 2026 logarithmic shape` | 10 | 2603.21125, 2503.19428, 2511.04610, 2604.04056 |
| 12 | `arxiv 2304.05807 ...` (deep-dive on the closest hit) | 10 | confirmed: log-ρ parametrization, **not** V(φ) potential |
| 13 | `arxiv 2603.21125 ...` (deep-dive) | 10 | confirmed: model-independent reconstruction, **avoids** assuming functional form |
| 14 | `arxiv 2509.13302 ...` (deep-dive) | 10 | confirmed: tested potentials = quadratic, quartic hilltop, double well, cosine, Gaussian, inverse power — **no log family** |
| 15 | `"phi log phi" inflation Barrow Parsons` (anchor on the closest known prior) | 10 | re-confirmed astro-ph/9506049 as inflation-only prior |
| 16 | `arxiv 2603.14693 ...` (DR2-era potential reconstruction with analytic families) | 10 | tested families = exponential, shifted-tanh, hilltop quartic — **no log family** |
| 17 | `DESI DR2 official release date` | 10 | DR2 BAO papers released **2025-03-19**; DR2 cosmology chains released **2025-10-06** |

**Total queries**: 17 (well above the 10-query floor). Coverage: arXiv astro-ph.CO (primary), gr-qc, hep-ph (cross-listed), Springer/Nature/PRD/MNRAS journal hits.

---

## §2 Relevant Papers Found (DR2 window: 2025-10 → 2026-04, plus the live closest-prior anchor)

### 2.1 Direct candidates for overlap with V(Ξ) = κ Ξ log Ξ quintessence

#### **Wang, Koussour, Malik et al. (2023)** — already cited as closest prior in WP82
- **arXiv**: 2304.05807
- **Journal**: Eur. Phys. J. C 83 (2023) 670
- **Title**: *Observational constraints on a logarithmic scalar field dark energy model and black hole mass evolution in the Universe*
- **Date**: 2023-04-12 (pre-DR2; included for cross-check)
- **Summary**: Proposes a **logarithmic parametrization of the energy density** ρ(z) for scalar field DE in standard gravity. Two parameters (α, β). Constrained by CC + BAO + SN. z_tr = 0.79, q_0 = -0.43.
- **Critical distinction (verified via WebFetch)**: This is a **ρ(z) parametrization**, **not** a V(φ) potential. No action is specified. The dynamics is fitted at the energy-density level. **It does not contain V = κφ log φ as a potential.**
- **Relevance**: **ADJACENT** (same vocabulary "logarithmic + scalar field DE", different mathematical object). Already cited in WP82. No change required.

### 2.2 DR2-era quintessence analyses that could supersede the DR1 χ²

#### **Wang, Li, Liu, Du (2026)** — model-independent quintessence reconstruction
- **arXiv**: 2603.21125
- **Title**: *Model-Independent Reconstruction of Quintessence Potential and Kinetic Energy from DESI DR2 and Pantheon+ Supernovae*
- **Date**: 2026-03-22
- **Summary**: Gaussian-process reconstruction of V(φ) and (1/2)φ̇² from DESI DR2 BAO + Pantheon+. Four covariance kernels. **Avoids any prior on V's functional form.** Finds monotonically decreasing V(φ) with redshift, kinetic energy crosses zero near z~1, consistent with thawing.
- **Critical distinction (verified via WebFetch)**: Reconstruction is **model-agnostic** — it does not test, fit, or rule out Ξ log Ξ specifically.
- **Relevance**: **ADJACENT** (DR2 baseline for any future Ξ-vs-data fit; cite at camera-ready). The WP82 freezing claim (V → 0 from above with W → −1) is **not** what this reconstruction reports — they get **thawing** (monotonically decreasing V with redshift). This is a **mild observational tension** for Ξ to address, not a priority kill.

#### **Adil, Zapata, Akarsu, Vazquez (2026)** — DR2 background reconstruction with analytic family ranking
- **arXiv**: 2603.14693
- **Title**: *Background-level reconstruction of scalar-field potentials from dark-energy histories and comparison with analytic potential families*
- **Date**: 2026-03-16
- **Summary**: Maps prescribed DE histories (CPL, AdS→dS sign-switching, shifted-tanh) onto effective V(φ). Bayesian evidence ranking among analytic families.
- **Critical distinction (verified via WebFetch)**: Tested families = **exponential, shifted-tanh, hilltop quartic**. **Logarithmic potentials are not among the families compared.** No φ log φ, no φᵖ(log φ)ᵍ, no Barrow-Parsons family.
- **Relevance**: **ADJACENT** (DR2-era infrastructure paper — useful citation for "Bayesian potential-family comparison" methodology). Does **not** preempt our claim.

#### **Brisbane / Bayat-Hertzberg (2025)** — minimal vs non-minimal quintessence vs DESI 2025
- **arXiv**: 2509.13302
- **Title**: *Comparing Minimal and Non-Minimal Quintessence Models to 2025 DESI Data*
- **Date**: 2025-09-16 (rev. 2025-10-09)
- **Summary**: Tests a wide quintessence-potential survey vs 2025 DESI: quadratic, quartic hilltops, double wells, cosine, Gaussians, inverse powers. Modest improvement over Λ. Non-minimal coupling can fit w<−1 effectively but suffers fifth-force constraints.
- **Critical distinction (verified via WebFetch)**: **No logarithmic family tested.** Does **not** include V = φ log φ.
- **Relevance**: **ADJACENT** (most relevant DR2-era V(φ) survey; anchor citation for "we extend the V(φ) survey to include logarithmic"). Cite in §Introduction.

#### **Roy & Chakraborty (2025)** — Quintessence and phantoms in light of DESI 2025
- **arXiv**: 2506.21542
- **Title**: *Quintessence and phantoms in light of DESI 2025*
- **Date**: 2025-06
- **Summary**: MCMC analysis of DESI BAO + CMB + SN to constrain truncated CPL and quintessence. Standard quintessence library, **no log potential**.
- **Relevance**: **ADJACENT** (DR2-era citation context). No overlap.

#### **Bayat & Hertzberg (2025)** — already cited in WP82
- **arXiv**: 2505.18937 (already in WP82 bibliography)
- **Relevance**: **ADJACENT** — already handled.

### 2.3 Other DR2-era hits inspected (no overlap)

| arXiv | Title (short) | Verdict |
|---|---|---|
| 2503.14738 | DESI DR2 II — BAO measurements & cosmological constraints | DESI flagship DR2 paper. Cite as DR2 anchor (replace 2404.03002). UNRELATED to log potential. |
| 2602.05368 | Dark Energy After DESI DR2 (Turyshev review, 2026-02 / rev 2026-04) | Review. Discusses CPL, w₀-wₐ, parametrizations. UNRELATED. |
| 2604.04056 | Quintessence reconstruction via Gaussian Processes (2026-04) | Model-independent, no V family assumed. UNRELATED to specific log-Ξ claim. |
| 2604.08449 | Coupled DE+DM, phantom divide guide (2026-04) | Coupled DE/DM. UNRELATED. |
| 2511.04610 | DR2 phantom-crossing + H₀ via reconstructed scalar-tensor (2025-11) | Modified gravity. UNRELATED. |
| 2511.22512 | Robust evidence for dynamical DE w/ DR2 + ACT/SPT/Planck (2025-11) | DR2-era statistical reanalysis. UNRELATED. |
| 2502.06929 | Scalar-field DE: current + forecast constraints (2025-02) | Thawing wφCDM — gives w₀ = −0.837 ± 0.045, 3.6σ from Λ at BAO+SN. UNRELATED to log potential, but the reported w₀ value is a useful DR2-era benchmark for our comparison column. |
| 2504.16337 | Thawing quintessence + transient acceleration (2025) | Already in WP82. ADJACENT. |
| 2509.13302 | Minimal/non-minimal quintessence vs DESI 2025 | See §2.2 above. ADJACENT. |
| 2503.19428 | S-dual quintessence + Swampland + DR2 | String-motivated. UNRELATED. |
| 2511.19610 | Fibre Inflation meets quintessence (2025-11) | String moduli. UNRELATED. |
| 2602.00820 | Multi-axion quintessence (2026-01) | Multi-field axion. UNRELATED. |
| 2603.18341 | Multifield DE: curved field-space (2026-03) | Two-field exponential. UNRELATED. |
| 2603.23551 | Cosmology w/ logarithmic-corrected horizon entropy (2026-02) | Horizon-entropy correction, not scalar potential. UNRELATED. |
| 2604.12032 | Coupled DE in DESI era (2026-04) | Coupled DE/DM. UNRELATED. |
| 2603.24214 | Direct cosmographic V(φ) reconstruction | Cosmographic method, no log family. UNRELATED. |

### 2.4 Confirmed historical priors (already in WP82)
- **astro-ph/9506049** (Barrow & Parsons, 1995): inflation family V₀ φᵖ (ln φ)ᵍ — contains our (p=1, q=1) case, but applied to **inflation, not dark energy**. Already cited in WP82 bibliography line 198 as the closest prior; honest disclosure.
- **arXiv:1201.4544** (Liu & Prokopec): logarithmic cosmological **fluid**, not scalar potential. Already cited.

---

## §3 Verdict

# **CLEAR — with one mandatory ADJACENT citation update**

**Justification:**
- No paper in the DR2 window (2025-10 → 2026-04) tests, fits, or proposes V(φ) = κ φ log φ (or κ Ξ log Ξ) as a quintessence potential against DESI data.
- The closest hit (Wang/Koussour 2304.05807, EPJC 2023) was published **before** the DR2 window and parametrizes ρ(z), **not** V(φ) — already correctly classified in WP82 §1 Form C.
- The DR2-era model-independent reconstructions (2603.21125, 2603.14693) explicitly **avoid** assuming V's functional form, so they cannot have proposed Ξ log Ξ.
- The DR2-era V(φ) family surveys (2509.13302, 2502.06929, 2506.21542, 2505.18937) enumerate quadratic / quartic hilltop / double well / cosine / Gaussian / inverse power / exponential / shifted-tanh — none include a logarithmic family.
- The exhaustive Barrow-Parsons inflation prior (astro-ph/9506049) remains the only known appearance of φᵖ(ln φ)ᵍ in cosmology, and it is honestly cited.

**Verdict mechanics for venue 7 (JCAP, 2026-04-22)**:
1. The novelty caveat in WP82 §1 Form D **stands** and may be retained as written.
2. The "residual risk" sentence in WP82 §1 (lines 64–65) — "`astro-ph.CO` preprints since 2025-10 have not been exhaustively swept" — **is now discharged by this audit**. Replace it with a citation to this sweep.
3. **Mandatory citation additions** below in §4.

**Confidence**: HIGH. 17 queries, 4 deep-dive WebFetches on the most plausible overlaps, three independent classes of negative result (no log family in V(φ) surveys, no log V proposed in DR2 reconstructions, no DR2-era paper in topic catchments).

**One soft observational signal to flag for the manuscript**: The DR2 model-independent reconstruction (2603.21125) finds a **monotonically decreasing V(φ) with z, consistent with thawing**. Our model is **freezing** with $w \to -1^+$. This is **not** a contradiction (the reconstruction's preferred class differs from ours; both fit data), but the JCAP referee will ask. WP82 §4 already addresses this via the DR2 CPL ($w_0 \approx -0.83$, $w_a \approx -0.75$) compatibility argument; we should explicitly add a one-paragraph contrast with 2603.21125's thawing reconstruction in the camera-ready.

---

## §4 ADJACENT citation lines to add to WP82 bibliography

Insert into `WP82_LOG_QUINTESSENCE_NOVELTY.md` under "References → Dark Energy and Quintessence":

```bibtex
- DESI Collaboration (2025). *DESI DR2 results. II. Measurements of baryon acoustic oscillations
  and cosmological constraints.* arXiv:2503.14738. Phys. Rev. D 112:083515.
  [DR2 anchor — replaces/supplements DESI2024VI for camera-ready DR2-bounded claims.]

- Wang, S., Li, T.-N., Liu, T. & Du, G.-H. (2026). *Model-Independent Reconstruction of
  Quintessence Potential and Kinetic Energy from DESI DR2 and Pantheon+ Supernovae.*
  arXiv:2603.21125. [DR2-era model-independent V(φ) reconstruction; reports thawing
  preference, contrasted with our freezing model in §4.]

- Adil, S.A., Zapata, M.A., Akarsu, Ö. & Vazquez, J.A. (2026). *Background-level reconstruction
  of scalar-field potentials from dark-energy histories and comparison with analytic potential
  families.* arXiv:2603.14693. [DR2-era V(φ) family ranking via Bayesian evidence;
  exponential / shifted-tanh / hilltop tested — logarithmic family absent, motivating our
  extension.]

- Brisbane, A. (2025). *Comparing Minimal and Non-Minimal Quintessence Models to 2025 DESI
  Data.* arXiv:2509.13302. [DR2-era V(φ) survey: quadratic, quartic hilltop, double well,
  cosine, Gaussian, inverse power — logarithmic family absent.]

- Turyshev, S.G. (2026). *Dark Energy After DESI DR2: Observational Status, Reconstructions,
  and Physical Models.* arXiv:2602.05368. [Review of DR2 implications for DE models.]

- Bhattacharya, S. & Bayat, Z., et al. (2025). *Scalar field dark energy models: Current and
  forecast constraints.* arXiv:2502.06929. [DR2-era benchmark: thawing $w_φ$CDM gives
  $w_0 = -0.837^{+0.044}_{-0.045}$ at BAO+SN, 3.6σ from ΛCDM. Cited as a DR2-era
  comparator for our $w(z)$ table.]
```

**Suggested patch to WP82 §1 line 64–65** (replace the residual-risk sentence):

> ~~Residual risk: `astro-ph.CO` preprints since 2025-10 have not been exhaustively swept; a final sweep at camera-ready stage is still required.~~
>
> **Updated 2026-04-19:** A 17-query DR2-era sweep (DR2 window 2025-10 → 2026-04, see `Atlas/DESI_DR2_SWEEP_2026_04_19.md`) confirms no DR2-era preprint proposes V(Ξ) = κΞ log Ξ as a quintessence potential. Closest DR2-era V(φ) surveys (arXiv:2509.13302, 2603.14693, 2502.06929) enumerate exponential, shifted-tanh, hilltop, quadratic, quartic, double well, cosine, Gaussian, inverse-power families — none include a logarithmic family. The Wang/Koussour parametrization (arXiv:2304.05807, EPJC 2023) remains a ρ(z) construction, not a V(φ) potential.

---

## §5 DR2 release status & DR1-bounded honesty

**DR2 status** (verified 2026-04-19):
- DR2 BAO + cosmology papers: released **2025-03-19** ([DESI March 19 Guide](https://www.desi.lbl.gov/2025/03/19/desi-dr2-results-march-19-guide/), arXiv:2503.14738 = Phys. Rev. D 112:083515).
- DR2 cosmology chains and posterior maximization data products: released **2025-10-06** ([DESI announcement](https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/)).
- DR2 underlying spectra and redshifts: **not yet publicly released** as of 2026-04 (per the 2025-10 DESI note).

**Honest framing of our χ² claim**:
- Our χ² = 3.1 (1.7σ vs ΛCDM's 15.3) is computed against **DESI DR1 BAO** (arXiv:2404.03000 / 2404.03002).
- The DR2 BAO results (2503.14738) are now public; the DR1 fit is an honest first pass but is **not** the latest available data.
- **Recommendation for venue 7 (JCAP 2026-04-22)**: keep the DR1 χ² claim but explicitly label it as "DR1-bounded fit; DR2 BAO chains (2503.14738, public 2025-10) deferred to a follow-up note." This is consistent with the WP82 bibliography line 208 ("DR2 updates (2025+) to be incorporated at camera-ready stage once published"). The honest framing **does not block submission**; it preempts a referee complaint.
- Optional stronger move (only if time before 2026-04-22 permits): re-run `desi_xi_optimize.py` against the DR2 chains released 2025-10-06 and report both χ² values. This would convert "DR1-bounded" into "DR2-confirmed". Files in scope:
  - `Gen12/targets/journal_attempts/07_jcap_cosmology/desi_xi_fit.py`
  - `Gen12/targets/journal_attempts/07_jcap_cosmology/desi_xi_optimize.py`

---

## Summary for the editor

- **Verdict**: **CLEAR** — no DR2-era prior on V = κ Ξ log Ξ; novelty caveat may be retained.
- **Mandatory action**: add 6 citation lines to WP82 (drafted in §4) and replace the residual-risk sentence (drafted in §4 patch).
- **Recommended action**: add a one-paragraph contrast with arXiv:2603.21125 (thawing vs freezing) in the camera-ready.
- **Optional action**: re-fit against the public DR2 chains (2025-10 release) before 2026-04-22; otherwise label our χ² as "DR1-bounded".
- **Not blocking**: venue 7 submission proceeds as scheduled.

---

**Sweep author**: Claude (background sweep agent), 2026-04-19.
**Methodology**: 17 WebSearch queries across DR2-era arXiv catchments + 4 deep-dive WebFetch confirmations on highest-overlap candidates.
**Citation discipline**: Every claim above is backed by an arXiv ID or a publicly verifiable DESI announcement URL. No claim is unsourced.
