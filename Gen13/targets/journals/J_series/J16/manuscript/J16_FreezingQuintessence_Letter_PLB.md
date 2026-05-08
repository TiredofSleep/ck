# Freezing-Quintessence Letter: A Two-Parameter $w(z)$ Profile from a Logarithmic Potential

**Authors:** B.R. Sanders$^{1}$, M. Gish$^{2}$, H.J. Johnson$^{3}$
$^{1}$7Site LLC, Hot Springs, AR — brayden@7site.co
$^{2}$Independent Researcher, Hot Springs, AR
$^{3}$Independent Researcher, Billings, MT

**Target venue:** Physics Letters B (Letter format, ~4 pages)
**Manuscript class:** Letter (numerical claims extracted from companion full paper J03)
**PACS:** 95.36.+x (dark energy); 98.80.Es (observational cosmology); 98.80.Cq (cosmological perturbations)
**Date:** 2026-05-07 (DRAFT — STATUS: DEPENDS_ON_J03)

---

> **Status note (read first).** This letter is the 4-page extraction of the companion paper J03 (Sanders, Gish, Johnson 2026, "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at $e^{-1}$ from a Logarithmic Potential," submitted to *JCAP*). The numerical claims in this letter ($z_\star$, $w(z=0)$, $\chi^2$, $\Lambda$ value) **must be reconciled with whatever J03 settles on** after the JCAP referee report's CRITICAL numerical reconciliation issue is resolved. The current draft uses placeholders flagged `[J03-RECONCILE]` for any value that may shift. Until J03 lands its v4, **J16 status is DEPENDS_ON_J03**.

---

## Abstract

A real positive dimensionless scalar field $\Xi$ minimally coupled to gravity with self-interaction $V(\Xi) = \Lambda^4\,\Xi\log\Xi$ has an analytic vacuum at $\Xi_0 = e^{-1}$ and a fluctuation mass $m_\Xi^2 = \Lambda^4 e/M_{\rm Pl}^2$. Tuning $m_\Xi \sim H_0$ places $\Lambda \approx 1.7$ meV, near the observed dark-energy scale. In a flat FRW background with outbound initial condition $\dot\Xi_i > 0$ at $z_i \approx 20$, the field traverses a *dual-regime* trajectory: thawing outbound (Type-T), instantaneous frozen turnaround at $z_\star$ where $\dot\Xi = 0$ and $w_\Xi(z_\star) = -1$ momentarily (Type-F), then asymptotic refreeze toward $\Xi_0$ as $z \to -1$ (Type-A). The observational signature is a non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$ at intermediate redshift. We report the two-parameter $w(z)$ profile, its consistency with the DESI 2024 DR1 $(w_0, w_a)$ Gaussian summary, and falsification criterion $(F_5)$: a non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$, distinguishing this dual-regime model from any single-regime quintessence. *(Numerical values pending J03 reconciliation; see status note above.)*

---

## 1. The model

The action of the minimal model is

$$S = \int d^4x \sqrt{-g}\left[\frac{R}{16\pi G} + \mathcal{L}_{\rm SM} - \tfrac{1}{2}M_{\rm Pl}^2\, g^{\mu\nu}\partial_\mu \Xi\,\partial_\nu\Xi - \Lambda^4\,\Xi\log\Xi\right].$$

The Euler-Lagrange equation gives $M_{\rm Pl}^2\,\Box\Xi = \Lambda^4(1 + \log\Xi)$. The vacuum sits at $\Xi_0 = e^{-1}$ (where $V'(\Xi_0) = 0$ and $V''(\Xi_0) = \Lambda^4 e > 0$); the fluctuation mass is

$$m_\Xi^2 = \frac{\Lambda^4 e}{M_{\rm Pl}^2}.$$

For $m_\Xi \sim H_0$, dimensional analysis gives $\Lambda \approx 1.5$ meV; the numerical fit in J03 gives $\Lambda \approx 1.7$ meV — both place $\Lambda$ near the observed dark-energy scale.

---

## 2. The dual-regime trajectory

In a spatially flat FRW background with $\dot\Xi_i > 0$ at $z_i \approx 20$, the field equation drives a three-regime cosmological history:

- **Type-T (thawing):** outbound from $\Xi_i$ near $\Xi_0$; $w_\Xi$ increases from $-1$.
- **Type-F (frozen turnaround):** instantaneous $\dot\Xi = 0$ at $z = z_\star$ `[J03-RECONCILE]`; $w_\Xi(z_\star) = -1$ momentarily.
- **Type-A (asymptotic refreeze):** inbound back toward $\Xi_0$ as $z \to -1$; $w \to -1$ at the late-time endpoint.

Caldwell-Linder (2005) classify standard quintessence as either *freezing* (monotone $w \to -1$ from above) or *thawing* (monotone departure from $-1$). The dual-regime trajectory studied here belongs to *neither* class and traverses both within a single physical history. The observational signature is non-monotone $w_{\rm DE}(z)$ with a local minimum near $-1$ at intermediate $z$.

The present-epoch value $w_\Xi(z=0) \approx -0.79$ `[J03-RECONCILE]` reflects the field's position on the inbound (Type-A) leg of the trajectory.

---

## 3. The two-parameter $w(z)$ profile

The trajectory is fully specified by two parameters: the initial-time energy density ratio $\Xi_i^2/(2\Lambda^4)$ and the initial velocity $\dot\Xi_i/H_i$ at $z_i \approx 20$. The CPL parametrization $w(z) = w_0 + w_a z/(1+z)$ approximates the bare $w_\Xi(z)$ over $0 \leq z \leq 2$ with `[J03-RECONCILE]` typical fitted values $(w_0, w_a) \approx (-0.79, -0.71)$.

$\chi^2$ against the DESI 2024 DR1 $(w_0, w_a)$ Gaussian summary on the CPL parametrization: $\chi^2 = $ `[J03-RECONCILE]`. The $\chi^2$ here quantifies proximity to the *published* $(w_0, w_a)$ marginal Gaussian and is not derived from the underlying joint BAO + CMB + SN likelihood, which is deferred to a companion paper.

---

## 4. Falsification

Five Stage-IV predictions discriminate this model from $\Lambda$CDM and from single-regime quintessence:

- **(F1)** Rolling-branch $w_\Xi(z) \geq -1$ for all $z \geq 0$.
- **(F2)** Monotone or non-monotone $w(z)$ shape per the dual-regime hypothesis.
- **(F3)** Asymptotic limit $w \to -1$ at the late-time endpoint $z \to -1$.
- **(F4)** Two-parameter $w(z)$ profile parametrizable by $(\Xi_i, \dot\Xi_i)$ at $z_i$.
- **(F5)** *(Decisive.)* Local minimum of $w_{\rm DE}(z)$ near $-1$ at intermediate $z$ — the Type-F turnaround signature.

Detection of $w_{\rm DE}(z) > -1$ for all $z$ in a Stage-IV survey would *not* falsify this model. Detection of monotone $w(z)$ across the full observable redshift range *would* falsify (F5). The local minimum near $-1$ is the single observational signature that picks out dual-regime quintessence.

---

## 5. Status, scope, and J-series context

**Status note.** The numerical claims in this letter are the J03 v3 / v4 values. As of 2026-05-07, J03 has a JCAP-referee-flagged numerical reconciliation issue (the supplied scripts + the IC + the $z_\star \approx 1.3$ claim were not mutually consistent in v3; the referee-independent execution gave $z_\star \approx 2.131$). J16 status is **DEPENDS_ON_J03**: this letter cannot be submitted until J03 reconciles to a consistent set of numbers. The current draft uses `[J03-RECONCILE]` placeholders for any number that may shift.

**Scope.** This is a *letter* (~4 pages); the full derivations, comparison to standard quintessence potentials, $w_{\rm DE}(z)$ table, EFT-validity discussion, perturbation analysis, and prior-art audit are in the companion full paper J03. The letter format strips J03 to: (1) the action and the analytic vacuum, (2) the dual-regime trajectory, (3) the two-parameter $w(z)$ profile, (4) the five falsification criteria. The $\chi^2$ vs DESI is summarized in a single number; the J03 paper has the full discussion.

**Tier classification.** Tier B / Tier 2 contingent on J03 reconciliation. The action and the analytic vacuum at $\Xi_0 = e^{-1}$ are exact theorems; the dual-regime trajectory is a numerical claim about the FRW trajectory and depends on the J03 v4 reconciliation passing.

**Lens scope.** Lens-invariant. The cosmological model is independent of the TSML / BHML lens taxonomy.

---

## References

### Core companion (full version)
- [J03] Sanders, B.R., Gish, M., Johnson, H.J. (2026). "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at $e^{-1}$ from a Logarithmic Potential." Submitted to *JCAP*.

### Quintessence and dark energy
- Caldwell, R.R., Linder, E.V. (2005). *Phys. Rev. Lett.* **95**:141301.
- Chevallier, M., Polarski, D. (2001); Linder, E.V. (2003).
- Ratra, B., Peebles, P.J.E. (1988); Wetterich, C. (1988).
- Steinhardt, P.J., Wang, L., Zlatev, I. (1999); Caldwell, R.R., Dave, R., Steinhardt, P.J. (1998).
- Albrecht, A., Skordis, C. (2000). *Phys. Rev. Lett.* **84**:2076. (Tracking-to-freezing quintessence)
- Boisseau, B., Esposito-Farese, G., Polarski, D., Starobinsky, A.A. (2000). *Phys. Rev. Lett.* **85**:2236.
- Tsujikawa, S., Sami, M. (2007). *Phys. Lett. B* **651**:224. (Logotropic-type)
- Ferreira, P.C., Avelino, P.P. (2018). Logotropic dark energy.

### DESI 2024
- DESI Collaboration (2024). *DESI 2024 BAO Results.*
- DESI Collaboration (2024). *DESI 2024 Cosmological Implications (DESI 2024 VI).*

### Bialynicki-Birula and structural connection
- Bialynicki-Birula, I., Mycielski, J. (1976). *Annals of Physics* **100**(1-2):62--93.

### Companion submissions in the J-series
- [J01] Sanders & Gish (2026). $\sigma$-rate paper. *JCT-A*.
- [J02] Sanders & Gish (2026). Four-core paper. *Algebraic Combinatorics*.
- [J13] Sanders & Johnson (2026). BB Bridge. *JMP*.

DOI for verification scripts: 10.5281/zenodo.18852047.
