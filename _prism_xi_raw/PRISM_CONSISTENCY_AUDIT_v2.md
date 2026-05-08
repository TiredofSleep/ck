# PRISM / GCU / Xi-Field: Full Internal Consistency Audit v2
**Authors:** B. Sanders, M. Gish, C.A. Luther, H.J. Johnson  
**Sprint:** 2026-04-10 | Theory Stabilization Pass

---

## 1. Field Inventory

Every object appearing across the current deck, classified by type. Items marked ❌ have no consistent definition as written.

| Object | Appearances | Classification | Status |
|---|---|---|---|
| $g_{\mu\nu}$ | Einstein eq., action | Rank-2 symmetric Lorentzian tensor | ✓ Standard |
| $R$, $G_{\mu\nu}$ | GR sector | Scalar / rank-2 tensor from $g$ | ✓ Standard |
| $\mathcal{L}_{\text{SM}}$ | Action | Scalar density (all SM fields implied) | ✓ Standard |
| $F^{\mu\nu a}$, $J^{\nu a}$ | Gauge equation | Antisymmetric rank-2 / vector in adjoint | ✓ Standard |
| **$\Xi(x)$** | Action, wave eq., gauge eq., unif. panel | **Mixed: scalar / complex / tensor** | ❌ Type conflict |
| $C(\Xi, \nabla\Xi)$ | Action | Scalar density — conditionally OK | ⚠ Sign issue |
| $T^{\Xi}_{\mu\nu}$ | Einstein eq. | Rank-2 symmetric tensor (from formula) | ✓ Formula is correct |
| $J^{\nu}_{\Xi}$ | Gauge equation | Vector, gauge rep. | ❌ Contradicts singlet |
| $\Xi_{\mu\nu}$ | Unification panel | Rank-2 tensor — distinct from scalar $\Xi$ | ❌ Undefined, unnamed |
| $\lambda$ | Action coupling | Dimensionless scalar | ⚠ Notation clash with SM |
| $\alpha$, $\beta$ | Compression functional | Dimensionless real — need $\beta = 2\alpha$ | ⚠ Relation unstated |
| $\kappa$ | Observer coupling | Unknown dimensions | ❌ Undefined |
| $O(\Xi)$ | Observer term | Unknown — operator, functional? | ❌ Undefined |
| $\Psi(t)$ / ORT | Observer eq. | **Phenomenological regime parameter** | ❌ Not a field |
| $\Omega_c = 47/125$ | Threshold panel | Dimensionless number | ❌ Asserted, not derived |
| FCC voxel lattice | Substrate panels | Discrete lattice structure | ⚠ Not in action |
| $a_{\text{vox}}$ | Substrate panels | Length scale (lattice constant) | ⚠ Not in action |
| Golden staircase | Visual panel | Visualization / geometry witness | See §8 |

**Verdict:** Two objects are well-defined (SM sector, metric). Everything involving $\Xi$, ORT, substrate, and threshold is either type-conflicted, underdefined, or asserted without derivation.

---

## 2. Contradiction Audit

### C2.1 — $\Xi$ Has Four Incompatible Types

| Where | What it says | Problem |
|---|---|---|
| Wave equation: $\Box\Xi - (1+\log\Xi)=0$ | $\Xi$ is a real positive scalar | $\log\Xi$ requires real, positive, dimensionless input |
| Compression functional: $\Xi^\dagger \log\Xi$ | $\Xi$ is complex | $\Xi^\dagger \neq \Xi$ unless $\Xi \in \mathbb{R}$ |
| Gauge equation: $J^\nu_\Xi \neq 0$ | $\Xi$ carries gauge charge | Contradicts singlet and complicates the type |
| Unification panel: $\Xi_{\mu\nu}$ | $\Xi$ is a rank-2 tensor | Wholly different object from the scalar above |

**Minimum repair:** Declare $\Xi$ a real, positive, dimensionless scalar field. Drop $\Xi^\dagger$ (replace with $\Xi$). Retire $\Xi_{\mu\nu}$ or name it a separate object.

---

### C2.2 — Coefficient Relation $\beta = 2\alpha$ Is Unstated but Required

The compression functional is $C = \alpha|\nabla\Xi|^2 + \beta\,\Xi\log\Xi$.

The Euler–Lagrange equation from varying the action $+\lambda C$ is:
$$-2\lambda\alpha\,\Box\Xi + \lambda\beta(1 + \log\Xi) = 0 \implies \Box\Xi = \frac{\beta}{2\alpha}(1+\log\Xi)$$

The deck's wave equation $\Box\Xi - (1+\log\Xi) = 0$ requires $\beta/2\alpha = 1$, i.e., $\beta = 2\alpha$.

This is internally consistent **only if this relation is stated**. As currently written, $\alpha$ and $\beta$ appear as free independent coefficients, making the wave equation inconsistent with the action unless the constraint is imposed.

**Minimum repair:** Either state $\beta = 2\alpha$ explicitly, or canonicalize by setting $\alpha = 1/2$, $\beta = 1$ and writing $C = \tfrac{1}{2}|\nabla\Xi|^2 + \Xi\log\Xi$.

---

### C2.3 — Gauge Singlet vs. Gauge Current (Hard Contradiction)

One panel declares $\Xi$ a **gauge singlet**: it transforms trivially under $G_\text{SM} = \text{SU}(3)\times\text{SU}(2)\times\text{U}(1)$.

Another panel writes a **modified gauge equation**:
$$\nabla_\mu F^{\mu\nu a} = J^{\nu a}_\text{SM} + J^{\nu a}_\Xi$$

If $\Xi$ is genuinely a singlet, its Noether current for any gauge transformation is identically zero: $J^{\nu a}_\Xi \equiv 0$. A singlet does not source gauge fields. There is no equation to write.

The only way $J^{\nu a}_\Xi \neq 0$ is if $\Xi$ couples to gauge fields through:
- A non-trivial gauge representation (it is not a singlet), or
- A higher-dimensional operator in the action of the form $\Xi\,F^2$ (indirect coupling)

Neither is present in the current action. This is not a wording problem — it is a logical impossibility.

**Minimum repair:** Remove $J^{\nu a}_\Xi$ from the gauge equation. The gauge equation is standard: $\nabla_\mu F^{\mu\nu a} = J^{\nu a}_\text{SM}$.

---

### C2.4 — Stress-Energy Formula vs. Prose Description

The displayed formula for $T^\Xi_{\mu\nu}$ is:
$$T^\Xi_{\mu\nu} = \partial_\mu\Xi\,\partial_\nu\Xi - g_{\mu\nu}\left[\tfrac{1}{2}(\partial\Xi)^2 + V(\Xi)\right]$$

This is **symmetric** in $\mu,\nu$. It is correct for a scalar field. It couples legitimately to the symmetric $G_{\mu\nu}$ in Einstein's equation.

The accompanying prose describes $T^\Xi_{\mu\nu}$ as **"an antisymmetric 2-form tracking recursion twists."**

A 2-form has $T_{\mu\nu} = -T_{\nu\mu}$, which implies $T_{\mu\mu} = 0$ for all $\mu$, and it cannot appear on the right-hand side of Einstein's equation (which is symmetric). This is not a terminological ambiguity. The formula and the prose describe incompatible mathematical objects.

**Minimum repair:** Delete the antisymmetric/2-form language from the prose. The formula is right. Describe $T^\Xi_{\mu\nu}$ as "the symmetric stress-energy tensor of the $\Xi$ scalar field, minimally coupled to gravity."

---

### C2.5 — Log Potential Domain and Dimensionality

The expression $\beta\,\Xi^\dagger\log\Xi$ is problematic on three grounds:

1. **If $\Xi$ is real:** $\Xi^\dagger = \Xi$, so write $\beta\,\Xi\log\Xi$. The $\dagger$ implies complex; remove it.
2. **If $\Xi$ has dimensions:** $\log\Xi$ is illegal without a reference scale. Write $\Xi\log(\Xi/\Xi_0)$ where $\Xi_0$ is a reference value. If $\Xi$ is dimensionless, $\Xi_0 = 1$ and the issue disappears.
3. **Domain:** $\log\Xi$ requires $\Xi > 0$. This must be stated as a domain constraint, or enforced by writing $\Xi = e^\phi$ for an unconstrained field $\phi$.

The ground state is at $\Xi_0 = e^{-1} \approx 0.368$ (from $d(\Xi\log\Xi)/d\Xi = 1 + \log\Xi = 0$). Effective mass at the ground state: $m^2_\Xi = \lambda V''(\Xi_0) = \lambda/\Xi_0 = \lambda e$.

**Minimum repair:** Replace $\Xi^\dagger$ with $\Xi$. State $\Xi > 0$ and $\Xi$ is dimensionless. The potential is then $V(\Xi) = \Xi\log\Xi$ with ground state at $\Xi_0 = e^{-1}$.

---

### C2.6 — ORT Cannot Enter the Action

The two versions of the ORT equation in the deck are:

**Version A:** $\Psi(t) = k \times R \times \lambda \times R_e \times M / (1 + \Delta S)$

**Version B:** $\Psi = M \cdot \lambda \cdot \alpha / \Delta S$

Neither version has consistent units. In Version B, if $M$ is mass [kg], $\lambda$ is wavelength [m], $\alpha$ is the fine structure constant [dimensionless], and $\Delta S$ is entropy [J/K = kg·m²·s⁻²·K⁻¹]:
$$[\Psi] = \frac{\text{kg}\cdot\text{m}}{\text{kg}\cdot\text{m}^2\cdot\text{s}^{-2}\cdot\text{K}^{-1}} = \text{K}\cdot\text{s}^2\cdot\text{m}^{-1}$$

This is not a Lorentz scalar, not dimensionless, and cannot be varied to yield Euler–Lagrange equations. The expanded action term $\kappa\,\Xi \circ O(\Xi)$ also has no defined meaning for the composition $\circ$ or the object $O$.

**Minimum repair:** Remove ORT from the action entirely. Retain $\Psi$ as an external phenomenological parameter characterizing observer regimes, explicitly labeled "not a dynamical field."

---

### C2.7 — FCC Substrate vs. Continuum Action

The action $S = \int[\ldots]\sqrt{-g}\,d^4x$ is a continuum integral over a smooth manifold.

The FCC substrate is a discrete lattice with a finite voxel size $a$. These are compatible only in the **effective field theory (EFT) framework**: the continuum theory is the low-energy description valid for wavelengths $\gg a$, with the discrete structure generating higher-dimensional operators suppressed by powers of $(E/\Lambda)$ where $\Lambda = 1/a$.

The current presentation does not:
1. State the EFT cutoff scale $\Lambda$ explicitly
2. Identify which operators become important near $\Lambda$
3. Explain how the $\Xi$ field emerges from the substrate microscopics

This is not a fatal contradiction, but it is an incomplete argument. The substrate claims and the continuum action must be separated into (a) the EFT action valid at low energies and (b) the UV completion provided by the FCC lattice.

**Minimum repair:** Add one sentence: "The action above is understood as an effective field theory valid below the substrate scale $\Lambda = 1/a_{\text{vox}}$."

---

### C2.8 — 47/125 Is Asserted, Not Derived

The coherence threshold $\Omega_c = 47/125 = 0.376$ is presented as a fixed-point result. No fixed-point equation is shown.

Numerical checks:
- $47/125 = 0.3760$
- $3/8 = 0.3750$ (difference: 0.001 — suspiciously close)
- $1/e \approx 0.3679$ (the ground state of $\Xi\log\Xi$ — also suspicious)
- $47$ is prime; $125 = 5^3$; there is no obvious geometric or algebraic reason for this denominator

Without the equation $f(\Omega) = \Omega$ being shown and solved, this number is a claim, not a result. Any referee will ask for this derivation first.

**Minimum repair:** Either write the fixed-point equation explicitly and show $\Omega = 47/125$ solves it uniquely in the relevant domain, or replace the specific number with "a coherence threshold $\Omega_c$ to be derived from the fixed-point structure of equation [X]."

---

### C2.9 — Longitudinal GW at $\sqrt{2}\,c$ Is Ruled Out as Stated

GW170817 (the neutron star merger with EM counterpart GRB 170817A) constrains the GW propagation speed to:
$$\left|\frac{v_\text{GW}}{c} - 1\right| < 5 \times 10^{-16}$$

The prediction $v = \sqrt{2}\,c$ gives a deviation of $|\sqrt{2}-1| \approx 0.414$. This is ruled out by GW170817 by approximately **$8\times10^{14}$ orders of magnitude** compared to the experimental bound.

The only escape routes are:
1. This is a **phase velocity** (not a group/signal velocity) of a new longitudinal mode. Phase velocities can exceed $c$ without violating causality.
2. This longitudinal mode **did not have an EM counterpart** and therefore is not constrained by GW170817.
3. The mode exists only in the **substrate rest frame** and is not a standard GW mode.

All three escape routes require explicit framing. Without it, the prediction as stated is dead on contact with the literature.

**Minimum repair:** Reframe as "a longitudinal mode with phase velocity $v_\phi = \sqrt{2}\,c$ in the substrate frame, distinct from standard tensor GW modes, not constrained by multi-messenger timing." Add a citation to GW170817 speed bounds.

---

## 3. Minimal Repair Set

**Seven edits. No new objects.**

| Edit | What to do |
|---|---|
| R1 | Declare $\Xi$ real, positive, dimensionless. Replace $\Xi^\dagger$ with $\Xi$. Remove $\Xi_{\mu\nu}$ from unification panel or give it a different name. |
| R2 | State $\beta = 2\alpha$ explicitly in the compression functional, or canonicalize: $\alpha = 1/2$, $\beta = 1$. |
| R3 | Remove $J^{\nu a}_\Xi$ from the gauge equation. $\Xi$ is a singlet; no gauge current. |
| R4 | Delete all prose describing $T^\Xi_{\mu\nu}$ as antisymmetric, a 2-form, or rotational. The formula is correct as-is. |
| R5 | Remove ORT from the action. Retain $\Psi$ as an external regime parameter, not a dynamical field. |
| R6 | Either derive $\Omega_c = 47/125$ from an explicit fixed-point equation or downgrade to "$\Omega_c$ to be determined." |
| R7 | Reframe the longitudinal GW prediction explicitly as a phase velocity in the substrate frame, not constrained by GW170817 tensor-mode bounds. |

---

## 4. Canonical Reduced Theory

After applying R1–R7, the minimal self-consistent theory is:

$$\boxed{S = \int \left[\frac{R}{16\pi G} + \mathcal{L}_\text{SM} + \frac{\kappa_\Xi}{2}\left((\partial\Xi)^2 - 2\Xi\log\Xi\right)\right]\sqrt{-g}\,d^4x}$$

where:
- $\kappa_\Xi > 0$ is a dimensionless coupling (renamed from $\lambda$ to avoid notation clash with SM Higgs coupling)
- $\Xi(x) > 0$ is a real, dimensionless scalar field
- The SM sector is completely unmodified
- ORT does not appear
- $\Xi$ has no gauge coupling

**What this eliminates:** $J^\nu_\Xi$, $\Xi_{\mu\nu}$, $\Xi^\dagger$, $\kappa\,\Xi\circ O(\Xi)$, and all ORT action terms. None of these removals change what is currently derivable.

**The potential:** $V(\Xi) = \Xi\log\Xi$. Ground state: $\Xi_0 = e^{-1}$. Effective mass: $m^2_\Xi = \kappa_\Xi\,e$ (in natural units).

---

## 5. Correct Equations

### Euler–Lagrange Equation for $\Xi$

$$\Box\Xi - (1 + \log\Xi) = 0$$

**Derivation:** Varying the action with $\alpha = 1/2$, $\beta = 1$ (so $\beta = 2\alpha$):
$$\frac{\partial\mathcal{L}_\Xi}{\partial\Xi} = -\kappa_\Xi(1+\log\Xi), \quad \nabla_\mu\frac{\partial\mathcal{L}_\Xi}{\partial(\partial_\mu\Xi)} = \kappa_\Xi\Box\Xi$$
$$\implies \kappa_\Xi\Box\Xi - \kappa_\Xi(1+\log\Xi) = 0 \implies \Box\Xi = 1 + \log\Xi \checkmark$$

This agrees with the deck's wave equation. The $\kappa_\Xi$ factors cancel. ✓

### Modified Einstein Equation

$$G_{\mu\nu} = 8\pi G\left(T^\text{SM}_{\mu\nu} + \kappa_\Xi\,T^\Xi_{\mu\nu}\right)$$

### Stress-Energy Tensor for $\Xi$

$$\boxed{T^\Xi_{\mu\nu} = \partial_\mu\Xi\,\partial_\nu\Xi - g_{\mu\nu}\left[\frac{1}{2}(\partial\Xi)^2 + \Xi\log\Xi\right]}$$

- **Symmetric in $\mu,\nu$:** ✓
- **Trace:** $T^\Xi = g^{\mu\nu}T^\Xi_{\mu\nu} = -(\partial\Xi)^2 - 4\Xi\log\Xi$
- **Energy density (FRW, homogeneous):** $\rho_\Xi = \frac{1}{2}\dot\Xi^2 + \Xi\log\Xi$
- **Pressure:** $p_\Xi = \frac{1}{2}\dot\Xi^2 - \Xi\log\Xi$

### Gauge Equations (Unmodified)

$$\nabla_\mu F^{\mu\nu a} = J^{\nu a}_\text{SM}$$

$\Xi$ sources no gauge current. End of statement.

### Domain Conditions

- $\Xi(x) > 0$ everywhere (required for $\log\Xi$ to be real)
- $\Xi$ dimensionless (so $\log\Xi$ has no reference scale issue)
- $\Xi \to \Xi_0 = e^{-1}$ as the vacuum value (ground state)

---

## 6. Prediction Triage

### Derivable Now

| Prediction | How |
|---|---|
| Dark energy equation of state $w_\Xi(z)$ | Solve $\ddot\Xi + 3H\dot\Xi = 1+\log\Xi$ in FRW; compute $w = p/\rho$ |
| Fifth force range $r = (m_\Xi)^{-1}$ | $m^2_\Xi = \kappa_\Xi\,V''(\Xi_0) = \kappa_\Xi\,e$; range $r = (\sqrt{\kappa_\Xi\,e})^{-1}$ |
| $\Xi$ scalar mass in terms of $\kappa_\Xi$ | $m_\Xi = \sqrt{\kappa_\Xi\,e}$ in natural units |
| CMB power spectrum modification | $\Xi$-inflation coupling gives modified scalar spectral index (requires inflation assumption) |
| Fifth-force experiments: Yukawa screening | $\Xi$ exchange gives $V_{\text{5th}}(r) = -A\,e^{-m_\Xi r}/r$; constrained by MICROSCOPE, torsion balances |

### Maybe Derivable After Further Work

| Prediction | What is needed |
|---|---|
| Coherence threshold $\Omega_c$ | Write and solve the fixed-point equation for $\Xi$ dynamics in a specific cosmological context |
| Lorentz violation scale | FCC substrate lattice must enter the action; Lorentz-breaking operators must be computed from symmetry breaking by lattice |
| Substrate-derived constants | The EFT matching conditions connecting FCC lattice parameters to $\kappa_\Xi$, $G$, $\hbar$, etc. must be worked out explicitly |

### Must Be Removed Now

| Prediction | Why |
|---|---|
| **Fundamental constants from FCC geometry** | No derivation path in current action; FCC is not in the EFT |
| **Longitudinal GW at exactly $\sqrt{2}\,c$ as signal velocity** | Ruled out by GW170817 by $\sim 10^{15}$ unless reframed as phase velocity of non-tensorial mode |
| **Lorentz violation at exactly $0.14$ eV** | Unmotivated energy scale; no derivation; no connection to any term in the action |
| **$\Omega_c = 47/125$ as derived threshold** | No fixed-point equation shown; cannot be stated as a prediction |
| **Observer/AI testability panels** | ORT is not in the action; these panels are phenomenological commentary, not predictions |

---

## 7. Surviving Core

After the seven edits, what remains is a **real, legitimate physical proposal**.

**The surviving theory:** A real positive dimensionless scalar field $\Xi(x)$ with a logarithmic self-interaction potential $V = \Xi\log\Xi$, minimally coupled to gravity, gauge-neutral. The action is standard; the equations are well-posed; the stress-energy is correct; the ground state is at $\Xi_0 = e^{-1}$.

**Why this is not standard dark energy:** The logarithmic potential $V = \Xi\log\Xi$ is qualitatively different from power-law ($\Xi^n$) or exponential ($e^{-\Xi}$) quintessence potentials. Its equation of state evolution is distinct and detectable in principle by DESI or Euclid-class surveys.

**What is genuinely new here:**
1. The specific logarithmic potential form with its fixed ground state at $\Xi_0 = e^{-1}$ — an exact result
2. The claim that this potential arises from an informational/compression principle — this is the conceptual novelty, even if it is not yet formally derived from first principles
3. The potential connection between $\Xi_0 = e^{-1} \approx 0.368$ and the asserted $\Omega_c \approx 0.376$ — suggestive but requires the fixed-point equation

**What survives of ORT:** The conceptual structure — distinguishing "epistemic" and "ontic" layers, characterizing observer regimes by complexity measures — is intellectually coherent. It does not currently enter the physics, but it could motivate a specific coupling between $\Xi$ and matter (a "sensor" coupling to entropy production, for instance) that would be derivable.

**What survives of the substrate:** The FCC voxel picture is a plausible UV completion story. It is not in tension with the canonical action as long as the action is understood as the EFT below the substrate scale. The substrate could in principle fix the value of $\kappa_\Xi$ and predict the fifth-force coupling — this is the right way to use the substrate idea.

**Honest assessment:** The field equations are real physics. The conceptual architecture is ambitious. The gap is that the conceptual architecture (ORT, substrate, threshold, observer) has not yet been connected to the field equations by derivation. That connection is the work that remains.

---

## 8. Visual Geometry: The Golden Staircase

**Classification: Heuristic witness — qualitatively motivated but not a formal object.**

Based on the description of a radial interleave staircase figure:

A radial spiral in the context of the canonical $\Xi$-field theory could represent several exact objects:
- **Phase space portrait** of the homogeneous $\Xi$ equation $\ddot\Xi = 1 + \log\Xi$: spiral-in dynamics near $\Xi_0$ are a real feature of this equation
- **Potential well** $V(\Xi) = \Xi\log\Xi$ plotted in polar coordinates — but this is not naturally spiral-shaped
- **Renormalization group flow** of $\kappa_\Xi$ — possible but not shown

The logarithmic potential $V = \Xi\log\Xi$ does have a natural "staircase" structure in the sense that each recursion of $\Xi\log\Xi$ generates a new scale, which is consistent with the informational interpretation. However, this is a qualitative observation, not a proof.

**What would make it a formal object:** If the radial structure corresponds to the asymptotic expansion of the homogeneous $\Xi$-field solution in an FRW background, the staircase could represent specific e-folding epochs. This is derivable. The figure would then be the exact phase-space trajectory, and "radian visual of the proof" would mean showing that each step corresponds to one radian of phase in the $(\Xi, \dot\Xi)$ plane.

Without seeing the actual figure and the claimed formal correspondence, this cannot be certified as more than a heuristic witness. It may become a formal object when the cosmological fixed-point analysis is completed.

---

## 9. Consistency Closure Sheet
*Center page for the preprint. All other sections derive from this.*

---

### Field Inventory (Canonical)

| Field | Type | Gauge rep. | Equation |
|---|---|---|---|
| $g_{\mu\nu}$ | Rank-2 symmetric tensor | Singlet | Einstein equations |
| SM fields | Standard | Standard reps | Standard SM |
| $\Xi(x) > 0$ | Real positive dimensionless scalar | Singlet | $\Box\Xi = 1 + \log\Xi$ |

---

### Canonical Action

$$S = \int \left[\frac{R}{16\pi G} + \mathcal{L}_\text{SM} + \frac{\kappa_\Xi}{2}\left((\partial\Xi)^2 - 2\Xi\log\Xi\right)\right]\sqrt{-g}\,d^4x$$

**Conditions:** $\Xi > 0$, $\Xi$ dimensionless, $\kappa_\Xi > 0$.

---

### Xi Field Equation

$$\Box\Xi = 1 + \log\Xi, \qquad \text{ground state: } \Xi_0 = e^{-1}, \quad m^2_\Xi = \kappa_\Xi e$$

Sign convention: $\Box = g^{\mu\nu}\nabla_\mu\nabla_\nu$ in $(-,+,+,+)$ signature.

---

### Stress-Energy Tensor

$$T^\Xi_{\mu\nu} = \partial_\mu\Xi\,\partial_\nu\Xi - g_{\mu\nu}\!\left[\frac{1}{2}(\partial\Xi)^2 + \Xi\log\Xi\right]$$

**Symmetric:** ✓ | **Couples to $G_{\mu\nu}$:** ✓ | **Antisymmetric/2-form:** ✗ (discard that language)

---

### Gauge Consistency Statement

$\Xi$ is a gauge singlet. $\nabla_\mu F^{\mu\nu a} = J^{\nu a}_\text{SM}$. No modification. No $\Xi$ gauge current.

---

### Observer / ORT Status

$\Psi$ is a **phenomenological regime parameter**, not a dynamical field. It does not appear in the action. It cannot currently be varied to yield equations of motion. It characterizes observer complexity in a qualitative sense.

---

### Substrate Status

The FCC voxel lattice is a proposed **UV completion** at scale $\Lambda = 1/a_\text{vox}$. The canonical action above is the **effective field theory** valid at energies $E \ll \Lambda$. The substrate is not in the current action. It may fix $\kappa_\Xi$ and $a_\text{vox}$ when the EFT matching is done.

---

### Threshold Status

$\Omega_c = 47/125$: **Underived.** Requires an explicit fixed-point equation and proof of uniqueness.  
Suggestion: $\Omega_c \approx \Xi_0 = e^{-1} \approx 0.368$ — the ground state of the $\Xi$ potential — is a natural candidate for a coherence threshold derivable from the theory. Check if this is what was intended.

---

### Prediction Status

| Prediction | Status |
|---|---|
| Dark energy $w_\Xi(z)$ | ✓ Derivable now |
| Fifth-force range $r = (\sqrt{\kappa_\Xi e})^{-1}$ | ✓ Derivable now |
| CMB power spectrum | ✓ Derivable (with inflation coupling) |
| Constants from FCC geometry | ❌ Remove — no derivation path |
| Longitudinal GW at $\sqrt{2}\,c$ (signal velocity) | ❌ Ruled out by GW170817 — reframe or remove |
| Lorentz violation at $0.14$ eV | ❌ Remove — no derivation, unmotivated scale |
| $\Omega_c = 47/125$ | ❌ Downgrade to open prediction until derived |

---

### Formal vs. Heuristic

| Item | Status |
|---|---|
| Action and equations | **Formal** |
| Stress-energy tensor | **Formal** |
| Ground state $\Xi_0 = e^{-1}$ | **Exact** |
| Fifth-force range | **Formal (derivable)** |
| Dark energy equation of state | **Formal (derivable)** |
| ORT / $\Psi$ | **Heuristic / phenomenological** |
| FCC substrate | **Heuristic / proposed UV completion** |
| $\Omega_c = 47/125$ | **Asserted** |
| Longitudinal GW claim | **Framing required** |
| Golden staircase visual | **Heuristic witness** |
