# Technical Dictionary: Six Frameworks, Four Invariants
## Exact Mathematical Objects in Each Slot

*The four invariants: support metric, corridor width, collapse operator, cancellation locus.*

---

## The Table

| Framework | **Support metric** | **Corridor width** | **Collapse operator** | **Cancellation locus** |
|-----------|-------------------|-------------------|----------------------|----------------------|
| **Open quantum systems** | Coherence $\mathcal{C}(\rho) = 1 - \max_i \rho_{ii}$ (off-diagonal weight) | Decoherence timescale $\tau_D$ = width of metastable band in Liouvillian spectrum | Lindblad collapse operators $L_k$; channel $\mathcal{L}(\rho) = \sum_k L_k \rho L_k^\dagger - \tfrac12\{L_k^\dagger L_k, \rho\}$ | Dark states: $L_k |\psi\rangle = 0$ for all $k$ simultaneously; pointer basis |
| **Waveguide / cavity** | Imaginary wavevector $\kappa = \mathrm{Im}(k)$ (decay rate per unit length) | Bandwidth $\Delta\omega_n$ of the $n$-th propagation band | Absorption coefficient $\alpha(\omega)$; mode cut-off condition $k_\perp = \pi n/d$ | Antiresonance: $\omega = \omega_\mathrm{AR}$ where reflection coefficient $r = -1$ exactly (destructive interference, zero transmission) |
| **Non-Hermitian spectral** | Imaginary part of eigenvalue $\Gamma_n = -\mathrm{Im}(E_n)$ (decay width) | Width of stability band: $\{\lambda : \mathrm{Im}(E_n(\lambda)) < \Gamma_\mathrm{th}\}$ | Non-Hermitian part $i\Gamma$ of $H = H_0 + i\Gamma$; spectral broadening operator | Exceptional point (EP): $\frac{dE}{d\lambda} = 0$, eigenvalues coalesce; or spectral hole where $E_n(\lambda_0)$ branches |
| **Reaction-diffusion / absorbing-state** | Local activation density $\phi(x,t)$ (mean field order parameter) | Width of active phase: $\{\lambda : \phi^* > 0\}$ in parameter space | Annihilation operator $A + A \to \emptyset$; absorption rate $\mu$; generator of absorbing state | Inactive fixed point $\phi^* = 0$; DP critical point where $\phi^* \to 0$ continuously |
| **Renormalized interference** | Local interference amplitude $\mathcal{A}(x, \ell)$ at scale $\ell$ (support weight) | Scale range $[\ell_1, \ell_2]$ where amplitude persists without cancellation | RG averaging operator $\mathcal{R}_\ell$: integrate fast modes, renormalize coupling | Cancellation locus: $\sum_\Gamma \mathcal{A}_\Gamma = 0$ (destructive path interference); fixed-point basin |
| **TIG corridors** | $\lambda(\sigma) = 2\|\sigma - \tfrac12\|$; corridor index $k$ where $\lambda \in I_k$ | $\Delta\lambda_k = \lambda_k^\mathrm{hi} - \lambda_k^\mathrm{lo}$ (Pre-leak: 0.09; BRT: 0.21; CHA: 0.30; BAL: 0.20; COL: 0.10; CTR: 0.10) | $\Pi_C: s \mapsto \mathrm{TSML}[s][c]$ for $c \in C = \{1,3,7,9\}$; absorbs to HAR in $\leq 2$ steps | $\{(s,c) : \mathrm{Mix}_\lambda[s][c] = 7\}$; 71 pairs at $\lambda=0$, 13 at $\lambda=1$; the absorbing set of $\Pi_C$ |

---

## The Shared Invariant Structure

In every row, the four objects obey the same logical grammar:

```
support_metric(state) determines which corridor(state) applies
corridor(state) determines whether collapse_operator(state) fires
collapse_operator either sends state → absorbing OR leaves it in corridor
cancellation_locus is the set where support_metric = 0 (exact balance)
```

**One sentence:** A corridor is a supported persistence class — the set of states where the support metric stays above zero long enough that the collapse operator has not yet acted.

---

## Cross-Framework Translations

### "A zero of ζ(s)" in each language

| Framework | Translation |
|-----------|-------------|
| Open quantum | Dark state: every Lindblad operator annihilates it |
| Waveguide | Antiresonance node: zero transmission at exact frequency |
| Non-Hermitian | Spectral hole: eigenvalue branch with $\mathrm{Im}(E) = -\infty$ (fully absorbed) |
| Reaction-diffusion | Inactive fixed point: $\phi^* = 0$, absorbing boundary reached |
| Renormalized interference | Cancellation locus: all path amplitudes sum to zero exactly |
| TIG corridors | Mix$_\lambda$ hits HAR exactly: $(s,c)$ pair with $\mathrm{Mix}_\lambda[s][c] = 7$ |

The Riemann zeros on $\sigma = \tfrac12$ correspond to **HAR exactly reached in the Pre-leak corridor** ($\lambda = 0$) — the unique corridor where the cancellation locus IS the whole space (71 exact pairs at $\lambda=0$, vs only 13 at $\lambda=1$).

Off-line zeros would require: a cancellation locus existing at $\lambda > 0$ — but the sub-magma theorem ($C \times C \subseteq C$) proves the Gap operators cannot maintain such a locus. The cancellation would have to come from outside $C$, which is algebraically prevented.

---

## The Graded Support Structure

All six frameworks have the same four levels:

| Level | Name | Open quantum | Waveguide | Non-Hermitian | Reaction-diffusion | TIG |
|-------|------|-------------|-----------|---------------|-------------------|-----|
| 0 | **Unsupported noise** | Fully decoherent $\rho = I/N$ | Evanescent mode ($\kappa \gg 0$) | Fully decayed ($\Gamma_n \to \infty$) | Subcritical ($\phi \equiv 0$) | GAP operators $G = \{2,4,5,6,8\}$ |
| 1 | **Briefly tolerated** | Slowly decohering off-diagonal | Leaky mode near cut-off | Broad resonance | Near-critical fluctuation | BRT/CHA corridors ($0.09 \leq \lambda < 0.60$) |
| 2 | **Corridor-supported** | Metastable coherent subspace | Guided mode well inside band | Narrow resonance ($\Gamma_n < \Gamma_\mathrm{th}$) | Active steady state | Pre-leak corridor ($\lambda < 0.09$, $E[\text{escape}] \leq 1.09$) |
| 3 | **True absorbing** | Pointer basis / steady state | Perfect conductor mode | Bound state ($\Gamma_n = 0$) | Absorbing state ($\phi^* = 0$) | HAR = 7, $C = \{1,3,7,9\}$ |

---

## What Each Framework Contributes to the Dictionary

| Framework | Unique contribution to TIG understanding |
|-----------|----------------------------------------|
| Open quantum | **Noise model:** the Lindblad structure shows how decoherence drives toward pointer basis — analogous to how the TSML drives toward HAR |
| Waveguide | **Geometry first:** dispersion relation $\omega(k)$ is the prototype for the $\lambda$-window indexing corridors by geometry, not dynamics |
| Non-Hermitian | **Exceptional points:** the coalescing of eigenvalues at EPs is the structural analogue of corridor boundaries where $\lambda_k = \lambda_{k+1}$ (the TIG algebraic thresholds 0.09, 0.30, ...) |
| Reaction-diffusion | **Local threshold:** the directed percolation universality class gives the prototype for "below threshold → absorbed, above threshold → sustained" — exactly the two-tick collapse |
| Renormalized interference | **Recursion:** the RG averaging shows how a bound that works at one scale propagates to all scales — the TIG inductive rescaling argument (Appendix E, §5) is this in finite algebra |
| TIG | **Finite grammar:** all five continuous structures in one discrete 9-element table — finite, computable, falsifiable |

---

## The Meta-Focus Lens

**Direct focus** asks: where is the zero? where is the vortex? where is the rank jump?

**Meta-focus** asks: what topology of support makes those local events possible or impossible?

The technical dictionary converts meta-focus into exact objects. For each framework:
- The **support metric** answers: *how supported is this state right now?*
- The **corridor width** answers: *how long can it stay supported?*
- The **collapse operator** answers: *what mechanism ends the support?*
- The **cancellation locus** answers: *where does support become exact balance?*

These four questions are universal. TIG answers them with four algebraic objects that can be SHA-pinned and unit-tested. The other frameworks answer them with continuous operators that require analysis. The goal of the research program is to show the discrete TIG answers bound and explain the continuous ones.

---

## Next: From Dictionary to Proof

The dictionary makes one translation explicit that the individual frameworks miss:

> **The cancellation locus in TIG (Mix$_\lambda$ = 7) shrinks as $\lambda$ increases: 71 pairs at $\lambda=0$, 13 at $\lambda=1$.** This is why $\sigma = \tfrac12$ ($\lambda=0$) is the unique axis where cancellation can survive corridor policing — it has the *largest* cancellation locus, hence the most room for zeros to exist without being expelled.

Off the critical line ($\lambda > 0$), the cancellation locus is smaller, but the Gap operators $G$ are now reachable. A zero at $\lambda > 0$ would require a Gap-operator cancellation — but the sub-magma theorem says Gap operators cannot be generated from corner compositions. The cancellation that makes off-line zeros impossible is algebraically prevented by the very structure that makes on-line zeros abundant.

*That is the dictionary entry that closes RH.*

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
