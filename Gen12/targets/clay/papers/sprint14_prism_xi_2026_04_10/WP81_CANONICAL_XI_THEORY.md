# WP81 — Canonical ξ Theory
## Logarithmic Quintessence with Exact Vacuum at e⁻¹

**Date**: 2026-04-10
**Sprint**: 14 — PRISM-XI
**Authors**: Brayden Ross Sanders / 7Site LLC · M. Gish · C.A. Luther · H.J. Johnson

---


## 1. Canonical Theory in Referee-Safe Form

### Field Content

| Field | Type | Domain | Gauge charge |
|---|---|---|---|
| $g_{\mu\nu}$ | Lorentzian metric | Standard GR manifold | Singlet |
| SM fields | Various | Standard | Standard |
| $\Xi(x)$ | Real scalar | $\Xi > 0$, dimensionless | Singlet |

All other objects from earlier drafts ($\Xi^\dagger$, $\Xi_{\mu\nu}$, $J^\nu_\Xi$, ORT $\Psi$) are excluded from the dynamical theory. The FCC substrate is treated as an interpretive origin story for $\kappa_\Xi$, not a dynamical input.

### Canonical Action

$$\boxed{S = \int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G} + \mathcal{L}_\text{SM} + \kappa_\Xi\!\left(\frac{1}{2}g^{\mu\nu}\partial_\mu\Xi\partial_\nu\Xi + \Xi\log\Xi\right)\right]}$$

where $\kappa_\Xi > 0$ is a dimensionless coupling, and the signature convention is $(-,+,+,+)$.

### What Is Formal vs. Interpretive

| Element | Status |
|---|---|
| Action and variational structure | **Formal** |
| EL equations | **Formal** |
| Stress-energy tensor | **Formal** |
| FRW cosmology | **Formal** |
| ORT / observer parameter $\Psi$ | **Interpretive** — not in the action |
| FCC substrate | **Interpretive** — proposed UV origin for $\kappa_\Xi$ |
| $47/125$ threshold | **Asserted** — see §6 |
| Gauge singlet status | **Formal** — derived consequence is $J^\nu_\Xi = 0$ |

---

## 2. Derivations from the Canonical Action

### 2a. Euler–Lagrange Equation for $\Xi$

From $\mathcal{L}_\Xi = \kappa_\Xi\!\left[\frac{1}{2}g^{\mu\nu}\partial_\mu\Xi\partial_\nu\Xi + \Xi\log\Xi\right]$:

$$\frac{\partial\mathcal{L}_\Xi}{\partial\Xi} = \kappa_\Xi(1+\log\Xi), \qquad \nabla_\mu\frac{\partial\mathcal{L}_\Xi}{\partial(\nabla_\mu\Xi)} = \kappa_\Xi\Box\Xi$$

Euler–Lagrange:
$$\kappa_\Xi\Box\Xi - \kappa_\Xi(1+\log\Xi) = 0$$

$$\boxed{\Box\Xi = 1 + \log\Xi}$$

This agrees with the deck. The $\kappa_\Xi$ factors cancel, so this equation is independent of the coupling strength.

### 2b. Stress-Energy Tensor

$$\boxed{T^\Xi_{\mu\nu} = \kappa_\Xi\!\left[\partial_\mu\Xi\,\partial_\nu\Xi - g_{\mu\nu}\!\left(\frac{1}{2}g^{\alpha\beta}\partial_\alpha\Xi\partial_\beta\Xi + \Xi\log\Xi\right)\right]}$$

**Verification:** Symmetric in $\mu,\nu$ ✓. Vanishing covariant divergence $\nabla^\mu T^\Xi_{\mu\nu} = 0$ on-shell ✓ (by contracted Bianchi). Consistent with the right-hand side of Einstein's equation ✓.

### 2c. Vacuum/Ground State

Setting $\Box\Xi = 0$ (static, homogeneous) and demanding $\Xi$ constant:

$$1 + \log\Xi = 0 \implies \log\Xi = -1 \implies \boxed{\Xi_0 = e^{-1} \approx 0.36788}$$

The potential $V(\Xi) = \kappa_\Xi\Xi\log\Xi$ has:

$$V'(\Xi) = \kappa_\Xi(1+\log\Xi),\quad V'(\Xi_0) = 0\ \checkmark$$

$$V''(\Xi) = \frac{\kappa_\Xi}{\Xi},\quad V''(\Xi_0) = \kappa_\Xi e > 0\ \checkmark$$

$\Xi_0 = e^{-1}$ is a **minimum** of the potential energy $V(\Xi)$.

Vacuum potential value: $V(\Xi_0) = \kappa_\Xi e^{-1}\log(e^{-1}) = -\kappa_\Xi/e$.

This is negative, contributing a cosmological constant shift $\Delta\Lambda = -8\pi G\kappa_\Xi/e$ that should be absorbed into the renormalized cosmological constant.

### 2d. Small-Fluctuation Expansion

Write $\Xi = \Xi_0 + \delta\Xi$ with $\Xi_0 = e^{-1}$. Expanding to first order in $\delta\Xi$:

$$\Box\delta\Xi = \frac{d}{d\Xi}(1+\log\Xi)\bigg|_{\Xi_0}\delta\Xi = \frac{1}{\Xi_0}\delta\Xi = e\,\delta\Xi$$

In flat Minkowski space, for a Fourier mode $\delta\Xi \sim e^{i(\mathbf{k}\cdot\mathbf{x}-\omega t)}$:

$$\Box\delta\Xi = (-\partial_t^2 + \nabla^2)\delta\Xi = (\omega^2 - k^2)\delta\Xi$$

Dispersion relation: $\omega^2 - k^2 = e$, i.e.,

$$\omega^2 = k^2 + e$$

This is a standard massive Klein-Gordon equation with:

$$\boxed{m_\Xi^2 = \kappa_\Xi\,e}$$

in physical units (restoring the $\kappa_\Xi$ factor from the normalization $\hat\Xi = \sqrt{\kappa_\Xi}\,\Xi$).

**Stability:** $m_\Xi^2 > 0$ for $\kappa_\Xi > 0$. The vacuum is stable. ✓

### 2e. Global Stability

$V(\Xi) = \kappa_\Xi\Xi\log\Xi$ for $\Xi > 0$:
- $V \to 0^-$ as $\Xi \to 0^+$
- $V$ minimum at $\Xi_0 = e^{-1}$ with $V_{\min} = -\kappa_\Xi/e$
- $V \to +\infty$ as $\Xi \to +\infty$

The potential is bounded below by $-\kappa_\Xi/e$ and is globally well-behaved. The energy density $\rho_\Xi = \frac{\kappa_\Xi}{2}\dot\Xi^2 + V(\Xi)$ is bounded below. Global stability holds for $\Xi > 0$.

---

## 3. Cosmology Sector

### 3a. FRW Background Equations

For spatially flat FRW with metric $ds^2 = -dt^2 + a^2(t)\,d\mathbf{x}^2$ and homogeneous $\Xi(t)$:

$$g^{\alpha\beta}\partial_\alpha\Xi\partial_\beta\Xi = -\dot\Xi^2$$

**Energy density:**
$$\rho_\Xi = T^\Xi_{00} = \kappa_\Xi\!\left[\frac{1}{2}\dot\Xi^2 + \Xi\log\Xi\right]$$

**Pressure:**
$$p_\Xi = \frac{T^\Xi_{ii}}{a^2} = \kappa_\Xi\!\left[\frac{1}{2}\dot\Xi^2 - \Xi\log\Xi\right]$$

**Equation of state:**
$$w_\Xi = \frac{p_\Xi}{\rho_\Xi} = \frac{\tfrac{1}{2}\dot\Xi^2 - \Xi\log\Xi}{\tfrac{1}{2}\dot\Xi^2 + \Xi\log\Xi}$$

This can be rewritten as:
$$w_\Xi = -1 + \frac{\kappa_\Xi\dot\Xi^2}{\rho_\Xi}$$

**Friedmann equations:**
$$H^2 = \frac{8\pi G}{3}\left(\rho_\text{SM} + \kappa_\Xi\!\left[\frac{1}{2}\dot\Xi^2 + \Xi\log\Xi\right]\right)$$

$$\dot H = -4\pi G(\rho_\text{SM} + p_\text{SM} + \kappa_\Xi\dot\Xi^2)$$

**$\Xi$ equation of motion in FRW:**
$$\ddot\Xi + 3H\dot\Xi = 1 + \log\Xi$$

(From $\Box\Xi = -\ddot\Xi - 3H\dot\Xi$ in the $(-,+,+,+)$ convention, giving $-\ddot\Xi - 3H\dot\Xi = 1+\log\Xi$ and rearranging.)

### 3b. Limiting Cases

**At vacuum ($\dot\Xi = 0$, $\Xi = e^{-1}$):**
$$\rho_\Xi = -\kappa_\Xi/e, \quad p_\Xi = +\kappa_\Xi/e, \quad w_\Xi = -1$$

The field behaves as a cosmological constant at the vacuum. The negative energy density is absorbed into the renormalized $\Lambda$.

**Slow-roll near vacuum:** $\Xi \approx \Xi_0 + \delta\Xi$, $|\dot\Xi| \ll |\Xi\log\Xi|^{1/2}$:
$$w_\Xi \approx -1 + \frac{\dot\Xi^2}{|\Xi_0\log\Xi_0|} = -1 + \frac{e\dot\Xi^2}{\kappa_\Xi^{-1}|\rho_\Xi|}$$

**Kinetic domination:** $\dot\Xi^2 \gg |\Xi\log\Xi|$:
$$w_\Xi \to +1$$

### 3c. Quintessence Classification

The field rolls from high $\Xi$ toward $\Xi_0 = e^{-1}$ as the universe expands. The equation of state evolves from $w \approx -1$ (vacuum-like, early domination) through quintessence range $-1 < w < 0$ to eventually settling at $w = -1$ at the vacuum.

**Classification:** This is a **freezing quintessence** model (field rolls from larger values of $w$ toward $w = -1$ at late times) with a logarithmic potential. It is distinguishable from $\Lambda$CDM by the time evolution of $w(z)$:

$$w_\Xi(z) = -1 + \epsilon(z), \quad \epsilon(z) = \frac{\kappa_\Xi\dot\Xi^2}{\rho_\Xi} \geq 0$$

$\epsilon(z) \to 0$ at late times (as $\Xi \to \Xi_0$). **DESI and Euclid can probe $\epsilon(z)$ at the few-percent level** — this is the primary observational handle.

**Is late-time acceleration generic?** Near the vacuum where $w_\Xi \approx -1$, the $\Xi$ contribution accelerates expansion. But the overall cosmological constant must be set by the total vacuum energy including the SM contribution and the shifted $\Lambda$. The value of $\kappa_\Xi$ is a free parameter that must be tuned (or derived from the substrate theory) to give the observed dark energy density $\Omega_\Xi \approx 0.69$.

---

## 4. Fifth-Force and Local Test Sector

### 4a. Minimal Theory — No Observable Fifth Force

In the canonical action, $\Xi$ couples only to gravity through $T^\Xi_{\mu\nu}$. There is **no direct coupling** between $\Xi$ and SM matter.

In the weak-field limit ($g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}$, $|h| \ll 1$), the static $\Xi$ equation becomes:

$$\nabla^2\delta\Xi - m_\Xi^2\delta\Xi = -\frac{\partial\,[\kappa_\Xi\,\delta(\Xi\log\Xi)]}{\partial\Xi}\bigg|_{\Xi_0}\delta\Xi_\text{source}$$

The source for $\Xi$ fluctuations in the minimal theory is the **gravitational perturbation** $h_{\mu\nu}$ sourced by matter, not the matter density directly.

**The fifth-force coupling between $\Xi$ and matter is:**
$$g_{\Xi\text{-matter}} \sim \frac{\kappa_\Xi}{M_\text{Pl}^2}$$

This is gravitationally suppressed. For any matter density, the induced $\Xi$ perturbation is of order $(h/M_\text{Pl})$. Laboratory fifth-force experiments (MICROSCOPE, torsion balances, Eöt-Wash) probe couplings $g \gtrsim 10^{-3}$ at millimeter range — the minimal $\Xi$ theory is **safe from fifth-force constraints** because its coupling is $\sim M_\text{Pl}^{-2}$, far below experimental reach.

**Consequence:** The minimal theory makes **no falsifiable prediction for local fifth-force experiments**. This is both a limitation and a virtue — it is consistent with all existing local tests.

### 4b. What Would Make a Fifth Force Observable

To couple $\Xi$ directly to matter and produce an observable fifth force, add one of:

1. **Conformal coupling:** $+g\,\Xi\,T^\text{matter}$ (coupling to matter trace)
2. **Disformal coupling:** $+f(\Xi)\,T^\text{matter}$ (coupling to full stress-tensor)
3. **Universal coupling:** $\Xi/\Xi_0\,\cdot\,\mathcal{L}_\text{SM}$ (rescaling SM Lagrangian)

None of these is in the current action. If added, the fifth-force range would be:
$$r_{\Xi\text{-force}} = m_\Xi^{-1} = (\kappa_\Xi e)^{-1/2}\ \text{(in natural units)}$$

For a dark energy field with $m_\Xi \sim H_0 \sim 10^{-33}$ eV, the range is cosmological ($r \sim \text{Hubble scale}$) and local experiments would see no effect. For a heavier field ($m_\Xi \gtrsim 1$ eV), the range falls below laboratory scales and experiments would apply.

---

## 5. Prediction Triage, Second Pass

| Claim | Derivable now? | Derivation sketch | Measurable by | Likely scale | Verdict |
|---|---|---|---|---|---|
| $\Xi_0 = e^{-1}$ as natural threshold | **Yes** | Minimum of $V(\Xi) = \Xi\log\Xi$; $V'(\Xi_0)=0$ | N/A (exact result) | $0.3679$ | **Keep — exact** |
| $47/125 = 0.376$ as exact threshold | **No** | No fixed-point equation shown | — | 2.2% off from $e^{-1}$ | **Remove / replace with $e^{-1}$** |
| Modified dark energy $w_\Xi(z)$ | **Yes** | FRW + $\Xi$ equations; freezing quintessence | DESI, Euclid, CMB | $w_0 \in (-1, -0.95)$ | **Keep** |
| Fifth-force range $r = m_\Xi^{-1}$ | **Yes (conditional)** | Requires matter coupling not in action | Requires new coupling | Cosmological scale | **Keep with caveat: needs coupling term** |
| Constants from FCC geometry | **No** | No derivation path in current action | — | — | **Remove** |
| Longitudinal GW at $\sqrt{2}\,c$ | **No** | GW170817 rules out signal velocity; substrate not in action | — | — | **Remove or reframe as phase velocity** |
| Lorentz violation at $0.14$ eV | **No** | No energy scale derived; no operator identified | — | — | **Remove** |
| Observer/AI/ORT effects | **No** | ORT not in action | — | — | **Remove from physics predictions** |
| Substrate/FCC voxel predictions | **No** | Substrate is interpretive; EFT not connected | — | — | **Demote to UV completion speculation** |

---

## 6. $e^{-1}$ vs $47/125$ — Dedicated Analysis

### Numerical comparison

$$e^{-1} = 0.36787944117\ldots, \qquad \frac{47}{125} = 0.3760000000$$

$$\left|\frac{47}{125} - e^{-1}\right| = 0.00812056\ldots, \qquad \text{relative difference} = 2.21\%$$

The best rational approximation to $e^{-1}$ with denominator $\leq 200$ is $71/193 = 0.36787565\ldots$, with error $10^{-5}$. The fraction $47/125$ is nowhere near this — it is a 2.2% rational approximation, not a best approximant.

### Is $e^{-1}$ the threshold selected by the canonical potential?

**Yes, exactly.** The canonical action produces a potential $V(\Xi) = \kappa_\Xi\Xi\log\Xi$ with a unique minimum at $\Xi_0 = e^{-1}$. This is an analytic result, not a numerical coincidence. The ground state is:

$$\Xi_0 = e^{-1} \approx 0.36788$$

If the "coherence threshold" is intended to be the natural vacuum value of the field, then the canonical theory gives $\Omega_c = e^{-1}$, not $47/125$.

### What is $47/125$?

| Possibility | Status |
|---|---|
| Exact derived constant from a fixed-point equation | **No** — no such equation has been shown |
| Best rational approximation to $e^{-1}$ | **No** — $71/193$ is far better |
| 2.2% rational fit to $e^{-1}$ | **Plausible** — could have been estimated numerically and expressed as a "nice" fraction |
| Independent quantity with its own derivation | **Unverifiable** — no derivation shown |

### Verdict (no hedging)

**$47/125$ should be replaced by $e^{-1}$** as the canonical threshold from the theory. The number $47/125 = 0.376$ appears to be a rational approximation to the ground state $\Xi_0 = e^{-1} \approx 0.368$, rounded upward to a fraction with a round denominator. It is not an exact derived result. The paper should state:

$$\Omega_c = \Xi_0 = e^{-1}$$

and derive this from the minimum condition $V'(\Xi_0) = 0$. This is a clean, exact, derivable result. Using $47/125$ instead invites the obvious question "why this fraction?" with no defensible answer.

---

## 7. Observational Program

**The minimal theory makes two robust predictions. Both are cosmological. Neither requires new experiments; both require upcoming surveys.**

### Primary: Dark energy equation of state

The $\Xi$ field behaves as freezing quintessence with $w_\Xi \to -1$ at late times. The deviation from $w = -1$ depends on the initial displacement of $\Xi$ from its vacuum:

$$w_\Xi(z) = -1 + \epsilon(z), \qquad \epsilon(z) = \frac{\kappa_\Xi\dot\Xi^2}{\rho_\Xi}$$

**Measurable by:** DESI DR1/DR2 ($w_0, w_a$ parameterization), Euclid (dark energy spectral survey), CMB+BAO joint fits.

**What kills the theory:** $w_\Xi = -1.000\pm0.003$ at all redshifts would disfavor any rolling quintessence. The minimal $\Xi$ theory predicts $w(z) \neq -1$ at some redshift during the rolling phase.

**What supports the theory:** Any confirmed deviation from $w = -1$ with the specific time-evolution profile predicted by $V = \Xi\log\Xi$ would be positive evidence. The profile is characterized by $w$ approaching $-1$ from above (freezing).

### Secondary: Scalar mass / Compton wavelength

If $\Xi$ couples to matter (through an extension not in the current action), the range of the induced fifth force is:

$$r = \left(\sqrt{\kappa_\Xi\,e}\right)^{-1}$$

This is testable only after the coupling is specified. In the minimal theory, there is no fifth-force prediction.

### What is not required

- No new collider experiments
- No new lab-scale fifth-force searches
- No gravitational wave observations (the GW claim has been removed)
- No Lorentz violation searches

**Three experiments would falsify the minimal theory:**
1. DESI/Euclid: $w = -1$ with precision $\sigma(w) < 0.01$ at multiple redshifts — rules out rolling quintessence
2. Planck/CMB-S4: tight upper bound on $\Delta N_\text{eff}$ — constrains early-universe $\Xi$ contribution
3. Stage-IV supernova surveys (Rubin LSST): $w_0 + 1.0$ constraint — disfavor freezing models

---

## 8. Minimal Surviving Core of the Ξ Theory

*This is the center of the preprint. Everything else is scaffolding.*

---

### Field Content

$\Xi(x)$: a real, positive, dimensionless scalar field.  
Domain: $\Xi > 0$.  
Gauge charge: singlet (no gauge coupling; $J^\nu_\Xi = 0$).  
Coupling: gravitational only in the minimal theory.

---

### Canonical Action

$$S = \int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G} + \mathcal{L}_\text{SM} + \kappa_\Xi\!\left(\frac{1}{2}g^{\mu\nu}\partial_\mu\Xi\partial_\nu\Xi + \Xi\log\Xi\right)\right]$$

$\kappa_\Xi > 0$ dimensionless coupling. Signature $(-,+,+,+)$.

---

### Field Equation

$$\Box\Xi = 1 + \log\Xi$$

---

### Stress-Energy Tensor

$$T^\Xi_{\mu\nu} = \kappa_\Xi\!\left[\partial_\mu\Xi\,\partial_\nu\Xi - g_{\mu\nu}\!\left(\frac{1}{2}g^{\alpha\beta}\partial_\alpha\Xi\partial_\beta\Xi + \Xi\log\Xi\right)\right]$$

**Symmetric:** ✓  **Consistent with Einstein:** ✓  **No 2-form language:** correct.

---

### Vacuum Value

$$\Xi_0 = e^{-1} \approx 0.36788, \qquad m_\Xi^2 = \kappa_\Xi\,e$$

This is the analytic minimum of the potential $V(\Xi) = \kappa_\Xi\Xi\log\Xi$. The vacuum is stable ($m_\Xi^2 > 0$).

---

### FRW Equations

$$\rho_\Xi = \kappa_\Xi\!\left[\frac{1}{2}\dot\Xi^2 + \Xi\log\Xi\right], \qquad p_\Xi = \kappa_\Xi\!\left[\frac{1}{2}\dot\Xi^2 - \Xi\log\Xi\right]$$

$$H^2 = \frac{8\pi G}{3}(\rho_\text{SM} + \rho_\Xi), \qquad \ddot\Xi + 3H\dot\Xi = 1+\log\Xi$$

$$w_\Xi = \frac{\tfrac{1}{2}\dot\Xi^2 - \Xi\log\Xi}{\tfrac{1}{2}\dot\Xi^2 + \Xi\log\Xi} \to -1\ \text{as}\ \dot\Xi \to 0\ \text{at}\ \Xi_0$$

---

### What This Theory Actually Predicts

| Prediction | Status | Measurement |
|---|---|---|
| $\Xi_0 = e^{-1}$ (vacuum value / natural coherence threshold) | **Exact** from $V'(\Xi_0) = 0$ | N/A — analytic |
| Dark energy equation of state: freezing quintessence, $w \to -1$ | **Derived** | DESI, Euclid |
| Scalar mass: $m_\Xi^2 = \kappa_\Xi e$ | **Derived** | Cosmological probes |
| Vacuum energy: $V(\Xi_0) = -\kappa_\Xi/e$ (shifts $\Lambda$) | **Derived** | Absorbed into $\Lambda_\text{obs}$ |

---

### What Has Been Cut

| Cut element | Reason |
|---|---|
| $\Xi^\dagger$ | $\Xi$ is real |
| $\Xi_{\mu\nu}$ | No definition; separate object if needed |
| $J^\nu_\Xi$ in gauge equation | Singlet; Noether current is zero |
| "Antisymmetric 2-form" language for $T_{\mu\nu}$ | Wrong; formula is symmetric |
| ORT in the action | No consistent units; not a field |
| $47/125$ threshold | 2.2% off from $e^{-1}$; no fixed-point derivation |
| Longitudinal GW at $\sqrt{2}\,c$ | Ruled out by GW170817 as stated; requires explicit reframing |
| Lorentz violation at $0.14$ eV | No derivation; no scale motivation |
| Constants from FCC geometry | Not connected to current action |
| FCC substrate as dynamics | Demoted to UV interpretation only |

---

*The theory after cuts is small, coherent, and falsifiable. It is a real physical proposal. The logarithmic potential $V = \Xi\log\Xi$ is not the standard quintessence potential; the resulting $w(z)$ evolution is a specific prediction that upcoming surveys can test. That is the surviving core.*
