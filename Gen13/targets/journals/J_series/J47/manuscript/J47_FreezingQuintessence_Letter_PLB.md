# Dual-Regime Quintessence from $V(\Xi) = \Lambda^4 \Xi\log\Xi$: A Letter

**Authors:** B.R. Sanders$^{1}$, M. Gish$^{2}$
$^{1}$7Site LLC, Hot Springs, AR — brayden@7site.co
$^{2}$Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Target venue:** Physics Letters B (Letter format, ~4 pages, REVTeX-letter)
**Manuscript class:** Letter (numerical claims extracted from companion full paper J46)
**PACS:** 95.36.+x (dark energy); 98.80.Es (observational cosmology); 98.80.Cq (cosmological perturbations)
**Date:** 2026-05-07 (SAVE-PLAN APPLIED — wrong file replaced; J46-RECONCILE markup stripped; numerical values per BBM_IC_DERIVATION_v2.md S2.7 Layer-3a)

**Note:** The REVTeX-letter conversion is `manuscript.tex` in this folder; this .md is the legacy markdown source file, retained for reference. File renamed from `J16_FreezingQuintessence_Letter_PLB.md` per save plan Fix-6.

---

## Abstract

A real positive dimensionless scalar field $\Xi$ minimally coupled to gravity with self-interaction $V(\Xi) = \Lambda^4 \Xi\log\Xi$ has an analytic vacuum at $\Xi_0 = e^{-1}$ and fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$. Tuning $m_\Xi \sim H_0$ places $\Lambda \approx 1.7$ meV, near the observed dark-energy scale. In a flat FRW background with outbound initial condition $(\Xi_i, \Xi'_i) = ((1+\sqrt{3})/e, 1/e)$ at $z_i \approx 20$ (set under the substrate-cosmology bridge axiom plus the BBM-minimality + scale-free-derivative postulates of [J46]), the field traverses a *dual-regime* trajectory: thawing outbound (Type-T), instantaneous frozen turnaround at $z_\star \approx 2.31$ where $\dot\Xi = 0$ and $w_\Xi(z_\star) = -1$ momentarily (Type-F), then asymptotic refreeze toward $\Xi_0$ as $z \to -1$ (Type-A). The CPL fit gives $(w_0, w_a) \approx (-0.798, -0.440)$ with $\chi^2 \approx 1.53$ against the DESI 2024 DR1 marginal Gaussian summary. The decisive observational signature is a non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$ at $z \approx z_\star$: a single Stage-IV-survey-shaped falsification handle (criterion F5).

---

## 1. The model

The action of the minimal logarithmic-quintessence model is

$$S = \int d^4x \sqrt{-g}\left[\frac{R}{16\pi G} + \mathcal{L}_{\rm SM} - \tfrac{1}{2}M_{\rm Pl}^2\, g^{\mu\nu}\partial_\mu \Xi\,\partial_\nu\Xi - \Lambda^4\,\Xi\log\Xi\right],$$

with $\Xi$ a real positive dimensionless scalar. The Euler-Lagrange equation gives $M_{\rm Pl}^2\,\Box\Xi = \Lambda^4(1 + \log\Xi)$. The vacuum sits at $\Xi_0 = e^{-1}$ (where $V'(\Xi_0) = 0$ and $V''(\Xi_0) = \Lambda^4 e > 0$); the fluctuation mass is

$$m_\Xi^2 = \frac{\Lambda^4 e}{M_{\rm Pl}^2}.$$

For $m_\Xi \sim H_0$, dimensional analysis gives $\Lambda \approx 1.5$ meV; the IC scan in [J46] (where $\Lambda^4/\rho_{c,0} = 0.231$) gives $\Lambda \approx 1.7$ meV — both place $\Lambda$ near the observed dark-energy scale.

**Distinction from logotropic dark energy.** Tsujikawa-Sami (2007) and Ferreira-Avelino (2018) use $V \propto -A \log(\rho/\rho_*)$ in the energy density of the dark-energy sector. The present model uses $V \propto \Xi \log \Xi$ in the *field*, producing a fluctuation mass scale at a definite vacuum rather than an attractor-pressure structure. The logotropic V has no isolated minimum; the present V has an analytic minimum at $\Xi_0 = e^{-1}$.

**BBM-separability origin.** The form $V \propto \Xi \log \Xi$ is forced uniquely (up to a constant + linear term) by the Bialynicki-Birula-Mycielski (1976) separability theorem on real scalar field theory.

---

## 2. The dual-regime trajectory

In a spatially flat FRW background with $\dot\Xi_i > 0$ at $z_i \approx 20$, the field equation drives a three-regime cosmological history:

- **Type-T (thawing):** outbound from $\Xi_i$ near $\Xi_0$; $w_\Xi$ increases from $-1$.
- **Type-F (frozen turnaround):** instantaneous $\dot\Xi = 0$ at $z = z_\star \approx 2.31$; $w_\Xi(z_\star) = -1$ momentarily; $w$ has a local minimum at $z_\star$.
- **Type-A (asymptotic refreeze):** inbound back toward $\Xi_0$ as $z \to -1$; $w \to -1$ at the late-time endpoint.

Caldwell-Linder (2005) classify standard quintessence trajectories as either *freezing* (monotone $w \to -1$ from above) or *thawing* (monotone departure from $-1$). The dual-regime trajectory studied here belongs to *neither* class and traverses both within a single physical history.

**Distinction from Albrecht-Skordis 2000.** Albrecht-Skordis introduced "tracking-to-freezing" quintessence in which a scaling tracker IC is captured into a late-time freezing state. The dual-regime here is structurally different: the rolling branch traverses thawing → frozen turnaround → asymptotic refreeze, all driven by the analytic vacuum at $\Xi_0 = e^{-1}$, with a non-monotone $w(z)$ and a single Type-F turnaround at $z_\star$. The Albrecht-Skordis trajectory is monotone in $w$ at late times; the present trajectory is not.

The present-epoch value $w_\Xi(z=0) \approx -0.80$ reflects the field's position on the inbound (Type-A) leg of the trajectory.

---

## 3. Initial conditions and the substrate-cosmology bridge

The rolling-branch IC at $z_i \approx 20$ is

$$(\Lambda^4/\rho_{c,0},\; \Xi_i,\; \Xi'_i) = (0.231,\; (1+\sqrt{3})/e,\; 1/e) \approx (0.231,\; 1.005,\; 0.368),$$

set under three structural inputs documented in [J46]:

1. **Theorem (BBM):** the vacuum $\Xi_0 = e^{-1}$.
2. **Postulate (substrate-cosmology bridge):** the 4-core substrate attractor $h/\beta = 1+\sqrt{3}$ of WP105/[J35], applied as a position-scaling factor relative to the vacuum, gives $\Xi_i = (1+\sqrt{3})\,\Xi_0 = (1+\sqrt{3})/e$.
3. **Postulate (BBM-minimality + scale-free derivative):** the canonical velocity scale at the vacuum in $\Omega$-units, with no additional dimensionless inputs beyond BBM's $e$, is unity in vacuum-position units, giving $\Xi'_i = 1 \cdot \Xi_0 = 1/e$.

The two postulates (2) and (3) are stated by name and defended on parsimony / structural-similarity grounds in [J46]; they are not theorems of BBM 1976 or of the substrate algebra alone. Falsification handle F5 below probes them directly.

---

## 4. The two-parameter $w(z)$ profile

The trajectory is fully specified by the two-parameter IC $(\Xi_i, \Xi'_i)$ at $z_i$. The CPL parametrization $w(z) = w_0 + w_a z/(1+z)$ approximates the bare $w_\Xi(z)$ over $0 \leq z \leq 2$ with fitted values

$$(w_0, w_a) \approx (-0.798,\; -0.440),\qquad z_\star \approx 2.31,$$

and $\chi^2 \approx 1.53$ against the DESI 2024 DR1 marginal $(w_0, w_a)$ Gaussian summary on the CPL parametrization. The $\chi^2$ here quantifies proximity to the published $(w_0, w_a)$ two-dimensional Gaussian and is not derived from the underlying joint BAO + CMB + SN likelihood, which is deferred to [J46].

**Figure 1.** Figure 1 (in `manuscript.tex`) shows $w_{\rm DE}(z)$ over $0 \leq z \leq 2$, with the local-minimum-at-$z_\star$ structure visible, overlaid on the DESI 2024 DR1 $(w_0, w_a)$ marginal Gaussian summary. The plot is generated by the verification script `compute_zstar_v4.py` of [J46] (DOI 10.5281/zenodo.18852047) under the IC of §3.

---

## 5. Consistency checks and falsification

Five Stage-IV predictions discriminate this model from $\Lambda$CDM and from single-regime quintessence. The first four are *consistency checks* (model fingerprints rather than Popperian falsifications); the fifth is the decisive falsification handle.

- **(F1) Non-phantom rolling branch:** $w_\Xi(z) \geq -1$ for all $z \geq 0$. Consistency check shared by canonical-kinetic quintessence.
- **(F2) Non-monotone $w(z)$:** the dual-regime hypothesis predicts non-monotone $w(z)$ with a single internal extremum. Consistency check distinguishing trajectory class from monotone freezing/thawing.
- **(F3) Late-time refreeze:** $w \to -1$ as $z \to -1$. Consistency check shared by all freezing classes.
- **(F4) Two-parameter profile:** $w_{\rm DE}(z)$ is parametrizable by $(\Xi_i, \Xi'_i)$ at $z_i$; CPL is a reasonable two-parameter summary over $0 \leq z \leq 2$. Consistency check.
- **(F5) Type-F turnaround at $z_\star$ (decisive).** Local minimum of $w_{\rm DE}(z)$ near $-1$ within $\Delta z = 0.5$ of $z_\star = 2.31$.

**Falsification.** Detection of $w_{\rm DE}(z) > -1$ for all $z$ in a Stage-IV survey would *not* falsify this model. Detection of monotone $w(z)$ across the full observable redshift range *would* falsify (F5). Absence of a local minimum within $\Delta z = 0.5$ of $z_\star = 2.31$, or detection of a local minimum outside that window, would falsify the IC of §3 and specifically the BBM-minimality + scale-free-derivative postulates of [J46]. The local minimum near $-1$ at $z \approx z_\star$ is the single observational signature distinguishing dual-regime quintessence from any single-regime class.

---

## 6. Lens scope and J-series context

**Lens-invariance.** The cosmological model $V(\Xi) = \Lambda^4 \Xi\log\Xi$ is lens-invariant in the strict sense: it depends on no choice of TSML / BHML / RAW / SYM lens on the underlying $\mathbb{Z}/10\mathbb{Z}$ substrate. The substrate-cosmology bridge axiom invoked for $\Xi_i$ (the 4-core attractor at $h/\beta = 1+\sqrt{3}$ from [J35]/WP105) is itself lens-invariant: the 4-core $\{V, H, Br, R\}$ is the algebraic center of the family per FAMILY_STRUCTURE_v1.md §2, with the closed-form attractor at $\alpha_M = 1/2$ holding identically across TSML/BHML and across $\mathbb{F}_p$ ring extensions. The five-criterion membership statement applies (substrate, commutativity, 4-core preservation, $\alpha$-bounded non-associativity, HARMONY-attracting iteration); J47's content sits cleanly inside the family and uses only its center.

**Tier classification.** Tier B / Tier 2. The action and the analytic vacuum at $\Xi_0 = e^{-1}$ are exact theorems; the dual-regime trajectory is a numerical claim about the FRW trajectory that depends on the J46 v4 numerics passing (Layer-3a strict-postulate framing per BBM_IC_DERIVATION_v2.md §S4).

**Companion full paper.** Full derivations, prior-art audit, perturbation analysis, joint BAO + CMB + SN likelihood, and the postulate-defense paragraphs are in [J46] (Sanders+Gish, JCAP).

---

## References

### Core companion (full version)
- [J46] Sanders, B.R., Gish, M. (2026). "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at $e^{-1}$ from a Logarithmic Potential." JCAP (in preparation).

### Quintessence and dark energy
- Caldwell, R.R., Linder, E.V. (2005). *Phys. Rev. Lett.* **95**:141301.
- Chevallier, M., Polarski, D. (2001); Linder, E.V. (2003).
- Ratra, B., Peebles, P.J.E. (1988); Wetterich, C. (1988).
- Steinhardt, P.J., Wang, L., Zlatev, I. (1999); Caldwell, R.R., Dave, R., Steinhardt, P.J. (1998).
- Albrecht, A., Skordis, C. (2000). *Phys. Rev. Lett.* **84**:2076. (Tracking-to-freezing quintessence)
- Boisseau, B., Esposito-Farese, G., Polarski, D., Starobinsky, A.A. (2000). *Phys. Rev. Lett.* **85**:2236.
- Tsujikawa, S., Sami, M. (2007). *Phys. Lett. B* **651**:224. (Logotropic-type)
- Ferreira, P.C., Avelino, P.P. (2017). *Phys. Lett. B* **770**:213. (Logotropic dark energy)

### DESI 2024
- DESI Collaboration (2024). *DESI 2024 II: Sample definitions, characteristics, and two-point clustering statistics.* arXiv:2411.12022.
- DESI Collaboration (2024). *DESI 2024 VI: Cosmological constraints from the measurements of baryon acoustic oscillations.* arXiv:2404.03002.

### Bialynicki-Birula and structural connection
- Bialynicki-Birula, I., Mycielski, J. (1976). *Annals of Physics* **100**(1-2):62–93.

### Companion submissions in the J-series
- [J35] Sanders, B.R., Gish, M. (2026). "Closed-Form 4-Core Attractor: $h/\beta = 1+\sqrt{3}$ in LMFDB 4.2.10224.1, Galois $D_4$." (in preparation)

### Family-structure framing
- Sanders, B.R., et al. (2026). "TIG Family Structure: Membership, Center, Boundaries (v1)." `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`.

DOI for verification scripts: 10.5281/zenodo.18852047.
