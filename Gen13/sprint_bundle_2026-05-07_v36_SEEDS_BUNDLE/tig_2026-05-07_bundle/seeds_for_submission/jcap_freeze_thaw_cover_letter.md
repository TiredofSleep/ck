# JCAP Cover Letter — Freeze-Thaw Transit

**To:** Editors, Journal of Cosmology and Astroparticle Physics

**From:**
- B. R. Sanders (corresponding author), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com
- H. J. Johnson, Independent Researcher, Billings, MT — hjj01986@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at e⁻¹ from a Logarithmic Potential*

---

## Summary

We submit for consideration in JCAP a study of a quintessence dark-energy model defined by the action

$$S = \int d^{4}x\,\sqrt{-g}\!\left[\tfrac{R}{16\pi G} + \mathcal{L}_{\mathrm{SM}} - \tfrac{1}{2}M_{\mathrm{Pl}}^{2}\,g^{\mu\nu}\partial_\mu\Xi\,\partial_\nu\Xi - \Lambda^{4}\,\Xi\log\Xi\right]$$

with $\Xi$ a real, positive, dimensionless scalar field and $\Lambda$ a mass scale. The potential admits an analytic minimum at $\Xi_0 = e^{-1}$, giving a stable massive scalar with $m_\Xi^{2} = \Lambda^{4} e / M_{\mathrm{Pl}}^{2}$. Setting $m_\Xi \sim H_0$ places $\Lambda \approx 1.7$ meV, the dark-energy mass scale.

The substantive observation is that on the rolling branch with outbound initial condition $\dot\Xi_i > 0$ at $z_i \approx 20$, the FRW trajectory is **dual-regime**: the field thaws outbound (Type-T), reaches an instantaneous frozen turnaround at intermediate redshift $z_\star \approx 2$ where $\dot\Xi = 0$ and $w_\Xi(z_\star) = -1$ momentarily (Type-F), then asymptotically refreezes back toward $\Xi_0$ as $z \to -1$ (Type-A). This trajectory traverses **both standard quintessence regimes** of the Caldwell-Linder taxonomy (thawing and freezing) within a single physical history — a structure that is in **neither** Caldwell-Linder class. The observational signature is a non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$ at intermediate redshift.

A representative configuration $(\Lambda^{4}/\rho_{c,0}, \Xi_i, \dot\Xi_i) = (0.231, 0.925, +0.429)$ at $z_i \approx 20$ yields $w_0^{\Xi} = -0.793$, $w_a^{\Xi} = -0.451$, $\chi^{2}_{\mathrm{Gauss}} = 1.52$ against the DESI 2024 DR1 published $(w_0, w_a)$ marginal Gaussian. The paper documents this fit honestly as a Gaussian-on-summary proximity measure, NOT a goodness-of-fit to the underlying joint BAO + CMB + SN likelihood (deferred to a companion numerical paper).

## Why JCAP

The paper fits the JCAP profile in three ways:

1. **A specific, falsifiable quintessence model.** Five Stage-IV falsification criteria are stated explicitly: rolling-branch $w_\Xi(z) \geq -1$, monotone or non-monotone shape per dual-regime hypothesis, asymptotic limit $w \to -1$, two-parameter $w(z)$ profile, and the local-minimum signature of the Type-F turnaround.

2. **Substantive cosmological observation.** The dual-regime trajectory is genuinely novel: it occupies a region of trajectory-shape space outside both Caldwell-Linder classes. The local-minimum-of-$w(z)$ signature is testable with current and near-future Stage-IV data.

3. **Honest framing throughout.** Initial conditions are *tuned*, not predicted; the structural connection $-x \log x$ to the per-bin Gibbs integrand and the Bialynicki-Birula-Mycielski nonlinearity is presented as motivational rhyme, NOT as derivation; the $\chi^2$ values are explicit Gaussian-on-summary proximity measures, NOT joint-likelihood fits.

## Companion submissions

Two companion papers in the same submission cycle place this cosmological model in a broader algebraic-combinatorial setting:

- Sanders & Gish (2026), *Non-Associativity Decay in Binary Composition Tables over* $\mathbb{Z}/N\mathbb{Z}$ — Journal of Combinatorial Theory, Series A.
- Sanders & Gish (2026), *Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on* $\mathbb{Z}/10\mathbb{Z}$ — Algebraic Combinatorics.

The cosmological paper does **not** depend on either companion for its main result; cross-references are provided for readers tracking the broader research program. All three are archived in the shared Zenodo deposit `10.5281/zenodo.18852047`.

## Reproducibility

Two Python scripts (`numpy + math + scipy`) are provided as supplementary material:

- `desi_xi_optimize_v2.py` — grid search over $(\Lambda^{4}, \Xi_i, \dot\Xi_i)$ at $N_{\mathrm{start}} = -4$ (matter era, $z \approx 54$), reading off the trajectory state at $z = 20$ to define the documented initial-condition values. Reproduces the documented best-fit at $(w_0, w_a)$ proximity to DESI Gaussian summary.
- `compute_zstar_v3.py` — z* extraction from the optimize trajectory using the same convention. Identifies the Type-F turnaround by the zero-crossing of $\Xi'$. Supersedes earlier `compute_zstar_v2.py`, which used a different initial-time variable (cosmic time at $z = 20$) and is not directly comparable.

A unit-convention note: the scripts work in $\Omega$-units (densities pre-divided by $\rho_{c,0} = 3 H_0^{2} M_{\mathrm{Pl}}^{2}$); the implicit Friedmann equation is algebraically equivalent to the standard $3 H^{2} = \rho_{\mathrm{total}}$ form. This convention is documented explicitly in §6.1.

## Suggested reviewers

We will provide suggested reviewers through the JCAP submission portal's reviewer-recommendation field rather than in this cover letter. Candidates include scholars working on logarithmic-NL-QM lineage (Zloshchastiev), constructive scalar-field models with analytic vacua (Chavanis 2022), and DESI Stage-IV $w(z)$-reconstruction methodology (Crittenden, Pogosian, Sahni, Holsclaw).

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Notes on the v3 reframe

This is the v3 reframe of an earlier v1 manuscript ("Logarithmic Quintessence"). The v3 version emphasizes the *dual-regime freeze-thaw trajectory* as the substantive observation, which we believe is the most distinctive and falsifiable feature of the model. v3 expanded the bibliography to 69 entries covering foundational quintessence dynamics, the logarithmic-NL-QM lineage, the Chavanis 2022 logotropic comparison (closest direct prior art), and non-parametric $w(z)$ reconstruction methodology.

We acknowledge the paper is shorter than typical JCAP contributions (17 pages) and have written it as a structurally complete unit rather than an expansive review. We will gladly expand any section if the referees indicate that additional material would strengthen the contribution.

---

Thank you for considering the manuscript.

Sincerely,
B. R. Sanders
