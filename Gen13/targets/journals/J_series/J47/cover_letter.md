# Cover letter — J47: Dual-Regime Quintessence from $V(\Xi) = \Lambda^4 \Xi \log \Xi$: A Letter

**To:** Editors, *Physics Letters B*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Dual-Regime Quintessence from $V(\Xi) = \Lambda^4 \Xi \log \Xi$: A Letter*

---

## Summary

A real positive dimensionless scalar field $\Xi$ minimally coupled to gravity with self-interaction $V(\Xi) = \Lambda^4 \Xi \log \Xi$ has an analytic vacuum at $\Xi_0 = e^{-1}$, fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$, and (with $m_\Xi \sim H_0$) $\Lambda \approx 1.7$ meV near the dark-energy scale. With outbound IC $(\Xi_i, \Xi'_i) = ((1+\sqrt{3})/e, 1/e)$ at $z_i \approx 20$ — set under the substrate-cosmology bridge axiom plus the BBM-minimality + scale-free-derivative postulates of the companion full paper J46 — the FRW trajectory is *dual-regime*: thawing outbound (Type-T), frozen turnaround at $z_\star \approx 2.31$ (Type-F, $w_\Xi = -1$ momentarily), asymptotic refreeze toward $\Xi_0$ (Type-A). The CPL parametrization gives $(w_0, w_a) \approx (-0.798, -0.440)$ with $\chi^2 \approx 1.53$ against the DESI 2024 DR1 marginal Gaussian summary on $(w_0, w_a)$. The decisive observational signature is a non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$ at $z \approx z_\star$ — this is criterion (F5) and is the single Stage-IV-survey-shaped falsification handle for the model, distinguishing dual-regime quintessence from any single-regime class.

## Why Phys Lett B

- **Letter format.** ~4-page REVTeX-letter; the companion full paper J46 (in preparation for JCAP) carries the full derivations, prior-art audit, perturbation analysis, and joint BAO + CMB + SN likelihood. PLB is the natural short-format venue for the headline result.
- **Single decisive falsification handle.** Criterion (F5) — a local minimum of $w_{\rm DE}(z)$ near $-1$ within $\Delta z = 0.5$ of $z_\star = 2.31$ — is the kind of falsifiable Stage-IV-survey prediction PLB readers respond to. The other four predictions (F1-F4) are consistency checks (model fingerprints) rather than independent falsifications, and the letter says so explicitly.
- **Stage-IV-timescale relevance.** The model is testable against DESI 2024 / DESI 2025 / future joint BAO + CMB + SN analyses on roughly the same timescale as the letter's review.
- **Distinct from prior art.** The paper distinguishes the present model from logotropic dark energy (Tsujikawa-Sami 2007, Ferreira-Avelino 2017 — those use $V \propto -A \log(\rho/\rho_*)$ in energy density; this model uses $V \propto \Xi\log\Xi$ in field, yielding an analytic vacuum at $\Xi_0 = e^{-1}$ rather than an attractor pressure) and from Albrecht-Skordis 2000 tracking-to-freezing (different trajectory class — Albrecht-Skordis is monotone in $w$ at late times, the present trajectory is non-monotone with a Type-F turnaround).

## Note on package finalization (read before review)

The manuscript at `manuscript/manuscript.tex` is the REVTeX-letter version of the freezing-quintessence content. An earlier draft of this submission package contained a wrong file at this path (a J23 Discrete Dirac paper from a prior J-series numbering); that has been corrected before this submission. The numerical values quoted in the abstract and §3-4 reflect the Layer-3a strict-postulate IC settled in BBM_IC_DERIVATION_v2.md (Sanders + Gish 2026, Atlas/META_PLAN_2026-05-06): $z_\star = 2.31$, $(w_0, w_a) = (-0.798, -0.440)$, $\chi^2 = 1.53$ at $(\Lambda^4/\rho_{c,0}, \Xi_i, \Xi'_i) = (0.231, (1+\sqrt{3})/e, 1/e)$.

## Companion submissions

The TIG/CK research program is shipping a coordinated J-series. Most relevant:

- **J46** Sanders, Gish (2026), "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at $e^{-1}$ from a Logarithmic Potential." Companion full paper (in preparation for *JCAP*) — the full version of this letter. Currently in v4 reconciliation per BBM_IC_DERIVATION_v2.md; numerical values now settled at the Layer-3a strict-postulate values.
- **J35** Sanders, Gish (2026). "Closed-Form 4-Core Attractor: $h/\beta = 1+\sqrt{3}$ in LMFDB 4.2.10224.1, Galois $D_4$." Supplies the substrate-cosmology bridge axiom for $\Xi_i$ (the 4-core attractor at $h/\beta = 1+\sqrt{3}$).

J46 + J35 will be deposited on arXiv prior to the J47 submission so both can be cited by arXiv ID rather than as "in preparation."

## Reproducibility

Same verification script as J46: `compute_zstar_v3.py` (or `compute_zstar_v4.py` once J46 v4 lands fully). Runs with `numpy + scipy` on a standard laptop in under 5 minutes. DOI: 10.5281/zenodo.18852047.

The script reproduces:
- $\Xi_0 = e^{-1}$ (BBM vacuum, exact theorem, one differentiation)
- $z_\star = 2.31$ at the IC of §3
- $w_\Xi(z=0) \approx -0.80$
- $(w_0, w_a) \approx (-0.798, -0.440)$ CPL fit
- $\chi^2 \approx 1.53$ vs DESI 2024 DR1 Gaussian summary

## Suggested reviewers

- E.V. Linder (Berkeley) — Caldwell-Linder freezing/thawing classification
- R.R. Caldwell (Dartmouth) — quintessence dynamics
- A. Albrecht (UC Davis) — Albrecht-Skordis tracking-to-freezing precedent
- A.A. Starobinsky (Landau Institute) — quintessence theory
- L. Verde (Barcelona) / DESI Collaboration — DESI 2024 / 2025 observational interpretation

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Tier and dependencies

Central claim is **Tier B / Tier 2** (Layer-3a strict-postulate framing per BBM_IC_DERIVATION_v2.md §S4). The analytic vacuum $\Xi_0 = e^{-1}$ and fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$ are exact theorems forced by the BBM 1976 separability theorem. The dual-regime trajectory is a numerical claim under two named postulates: the substrate-cosmology bridge axiom (substrate's 4-core attractor at $h/\beta = 1+\sqrt{3}$ applied as a position-scaling factor relative to the vacuum) and the BBM-minimality + scale-free-derivative axiom (canonical velocity scale at the vacuum is unity in vacuum-position units). Both postulates are stated by name and defended on parsimony / structural-similarity grounds in J46. Falsification handle F5 probes them directly.

---

Sincerely,
B.R. Sanders
