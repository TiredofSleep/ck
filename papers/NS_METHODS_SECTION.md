# Navier–Stokes BREATH Criterion: Numerical Note
## With Falsification Condition and Dedalus Methods Section

*Brayden Sanders — 7Site LLC | March 2026*

---

## The Criterion

$$\mathrm{Re}_\mathrm{local}(x, t) = \Omega(x,t) \cdot L_\mathrm{Taylor}(x,t)^2 / \nu \leq 2/7$$

where $\Omega = |\nabla \times \mathbf{u}|^2$ (enstrophy density) and
$L_\mathrm{Taylor} = \sqrt{\nu / (|\nabla \times \mathbf{u}| + \epsilon)}$
(Taylor microscale proxy, $\epsilon = 10^{-10}$).

---

## Falsification Condition (Numerical Language)

> **If** a numerically resolved instability — defined as an enstrophy spike
> exceeding $10 \times \langle Z(t_0) \rangle$ (ten times the initial mean enstrophy),
> OR a peak-gradient event where $\|\nabla \mathbf{u}\|_\infty > 100 \|\nabla \mathbf{u}\|_\infty(t=0)$,
> OR loss of resolution (Kolmogorov scale $\eta < \Delta x/2$) —
> **appears** at some time $t_*$
> **without** $\mathrm{Re}_\mathrm{local}^\mathrm{max}(t) > 2/7$ for any $t < t_*$,
> **then** the 2/7 criterion fails for this initial condition.

*Note: "blow-up" in the theorem sense cannot be observed in finite-resolution DNS.
The falsification is stated in terms of observable numerical events only.*

---

## Mock DNS Result (Current Status)

Taylor-Green vortex, $\nu = 10^{-3}$, 2-D cross-section:
- **Regime A** (smooth): $\max \mathrm{Re}_\mathrm{local} = 0.181 < 2/7$ throughout. No flag raised. ✓
- **Regime B** (cascade): $\mathrm{Re}_\mathrm{local}$ first exceeds $2/7$ at $t = 1.35$. Enstrophy peak at $t = 4.00$. Lead time: 2.65 units. The criterion fires **before** the numerical instability event. ✓

---

## Methods: Future Dedalus 3-D Run

### Setup
- **Solver:** Dedalus v3, spectral (Fourier×Fourier×Fourier)
- **Domain:** $(2\pi)^3$ triply periodic box
- **Resolution:** $128^3$ (minimum); $256^3$ preferred
- **Initial condition:** Taylor-Green vortex $\mathbf{u}_0 = (\sin x \cos y \cos z,\ -\cos x \sin y \cos z,\ 0)$
- **Reynolds number:** $\mathrm{Re} = 1/\nu \in \{400, 800, 1600\}$ (three runs)
- **Integration time:** $t \in [0, 20]$ (two large-eddy turnover times)
- **Timestep:** adaptive RK443, CFL = 0.4

### Observables to log (at every timestep)
```python
observables = {
    'time': solver.sim_time,
    'enstrophy_max': np.max(omega_sq),          # max enstrophy density
    'enstrophy_mean': np.mean(omega_sq),        # mean enstrophy
    'Re_local_max': np.max(Re_local),           # max local Reynolds
    'Re_local_field': Re_local,                 # full field (save every 0.1 t-units)
    'kolmogorov_scale': nu**(3/4) / eps**(1/4), # resolution check
    'breach_flag': int(np.max(Re_local) > 2/7), # 0 or 1
    'breach_location': np.unravel_index(np.argmax(Re_local), Re_local.shape)
}
```

### Breach detector (paste into Dedalus script)
```python
def check_BREATH_criterion(solver, nu, threshold=2/7):
    """
    Check TIG BREATH criterion at current timestep.
    Returns: (breach: bool, Re_local_max: float, location: tuple)
    Falsification: instability event (see note) without prior breach.
    """
    u = solver.state['u']
    v = solver.state['v']
    w = solver.state['w']
    
    # Compute vorticity components
    omega_x = np.gradient(w, axis=1) - np.gradient(v, axis=2)
    omega_y = np.gradient(u, axis=2) - np.gradient(w, axis=0)
    omega_z = np.gradient(v, axis=0) - np.gradient(u, axis=1)
    omega_sq = omega_x**2 + omega_y**2 + omega_z**2
    
    # Taylor microscale proxy
    eps = 1e-10
    L_taylor = np.sqrt(nu / (np.sqrt(omega_sq) + eps))
    
    # Local Reynolds number
    Re_local = omega_sq * L_taylor**2 / nu
    Re_max = float(Re_local.max())
    
    breach = Re_max > threshold
    location = np.unravel_index(np.argmax(Re_local), Re_local.shape) if breach else None
    
    return breach, Re_max, location
```

### Logging requirements
- Log `breach_flag` at every timestep
- Log full `Re_local` field at 0.1-unit intervals
- Log enstrophy spectrum at 0.5-unit intervals (for resolution check)
- Save checkpoint at first breach event with full field state
- Record `t_breach` (first $t$ with `breach_flag=1`) and `t_instability` (first instability event)

### Success condition
The criterion is **supported** if $t_\mathrm{breach} < t_\mathrm{instability}$ across all three Reynolds numbers.
The criterion is **falsified** if any run shows $t_\mathrm{instability}$ without prior $t_\mathrm{breach}$.

---

## Connection to TIG

The threshold $2/7$ is the TIG mass-gap constant:
$$2/7 = T^* + S^* - 1 = 5/7 + 4/7 - 1$$
where $T^* = 5/7$ is the coherence threshold and $S^* = 4/7$ is the structure threshold.

In corridor language: smooth flow stays in the Pre-leak corridor ($\mathrm{Re}_\mathrm{local} \leq 2/7$);
cascade/instability corresponds to trajectory exit into the BRT or CHA corridor.
The breach detector flags the first corridor-exit event.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
