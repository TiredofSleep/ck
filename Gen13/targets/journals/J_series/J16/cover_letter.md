# Cover letter — J16: Freezing-Quintessence Letter

**To:** Editors, *Physics Letters B*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com
- H.J. Johnson, Independent Researcher, Billings, MT — hjj01986@gmail.com

**Date:** [DATE OF SUBMISSION — pending J03 reconciliation]

**Manuscript title:** *Freezing-Quintessence Letter: A Two-Parameter $w(z)$ Profile from a Logarithmic Potential*

---

## Status note (read first)

This letter is the 4-page extraction of the companion paper J03 (Sanders, Gish, Johnson 2026, "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at $e^{-1}$ from a Logarithmic Potential," submitted to *JCAP*). The numerical claims in this letter ($z_\star$, $w(z=0)$, $\chi^2$, $\Lambda$) **must be reconciled with whatever J03 settles on** after the JCAP referee report's CRITICAL numerical reconciliation issue (v3 had inconsistent IC/script/$z_\star$ values; referee independent execution gave $z_\star \approx 2.131$ where v3 claimed $\approx 1.3$). **J16 status is DEPENDS_ON_J03** until J03 v4 lands; a separate reconciliation agent is working on J03 currently.

## Summary

A real positive dimensionless scalar field $\Xi$ minimally coupled to gravity with self-interaction $V(\Xi) = \Lambda^4 \Xi \log \Xi$ has an analytic vacuum at $\Xi_0 = e^{-1}$, fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$, and (with $m_\Xi \sim H_0$) $\Lambda \approx 1.7$ meV near the dark-energy scale. With outbound IC at $z_i \approx 20$, the FRW trajectory is *dual-regime*: thawing outbound, frozen turnaround at $z_\star$ (Type-F, $w_\Xi = -1$ momentarily), asymptotic refreeze toward $\Xi_0$. The observational signature is a non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$ at intermediate $z$ — this is criterion (F5) and is the decisive falsification handle. The two-parameter $w(z)$ profile is consistent with the DESI 2024 DR1 Gaussian summary on $(w_0, w_a)$ for appropriately chosen IC.

## Why Phys Lett B

- 4-page Letter format; the companion full paper J03 is the JCAP version with full derivations, prior-art audit, perturbation analysis, and DESI fit. PLB is the natural short-format venue for the headline result.
- The decisive falsification criterion (F5) — a local minimum of $w_{\rm DE}(z)$ near $-1$ — is the kind of falsifiable Stage-IV-survey prediction PLB readers respond to.
- The model is testable against DESI 2024 / DESI 2025 / DESI BAO + CMB joint analyses on roughly the same timescale as the letter's review.

## Companion submissions

The TIG/CK research program is shipping a coordinated J-series. Most relevant:

- **J03** Sanders, Gish, Johnson (2026), "Freeze-Thaw Transit." Submitted to *JCAP* — the full version of this letter. Currently under JCAP referee revision (numerical reconciliation issue being addressed).
- **J01** Sanders & Gish (2026). $\sigma$-rate paper. *JCT-A*.
- **J02** Sanders & Gish (2026). Four-core paper. *Algebraic Combinatorics*.
- **J13** Sanders & Johnson (2026). BB Bridge. *JMP* (provides the structural derivation of why $V \propto \Xi\log\Xi$ is forced by separability).

## Reproducibility

Same verification script as J03: `compute_zstar_v3.py` (or v4 once reconciled). Runs with `numpy + scipy` on a standard laptop in under 5 minutes. DOI: 10.5281/zenodo.18852047.

## Suggested reviewers

- E.V. Linder (Berkeley) — Caldwell-Linder freezing/thawing classification
- R.R. Caldwell (Dartmouth) — quintessence dynamics
- A. Albrecht (UC Davis) — Albrecht-Skordis tracking-to-freezing precedent
- A.A. Starobinsky (Landau Institute) — quintessence theory
- L. Verde (Barcelona) / DESI Collaboration — DESI 2024 / 2025 observational interpretation

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Tier and dependencies

Central claim is **Tier B / Tier 2** contingent on J03 v4. The analytic vacuum $\Xi_0 = e^{-1}$ and fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$ are exact theorems; the dual-regime trajectory is a numerical claim that depends on J03's reconciliation passing.

**This letter is HELD pending J03 reconciliation.** Submission timing: after J03 v4 lands, with the same numerical values.

---

Sincerely,
B.R. Sanders
