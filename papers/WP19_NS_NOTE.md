# A TIG Breach Detector for Navier–Stokes Regularity
## Numerical Note

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*

---

## The Criterion

From the TIG BREATH-COLLAPSE fixed-point structure, we derive the dimensionless regularity criterion:

```
Re_local(x,t) = Ω(x,t) · L(x,t)² / ν  ≤  2/7
```

where Ω is local enstrophy, L is local length scale, ν is viscosity.

**Algebraic basis (proved):** TSML[BRT][COL] = BRT (single table lookup). BREATH persists only in the COLLAPSE column. In all other contexts BREATH → HARMONY in one step.

**Criterion interpretation:** Re_local ≤ 2/7 ↔ flow in COLLAPSE context ↔ BREATH persists ↔ smooth solution. First breach ↔ context exits COLLAPSE ↔ BREATH → HARMONY in one step ↔ onset of anomalous gradients.

---

## Mock DNS Results

Taylor-Green vortex initial data; ν=10⁻³; dt=10⁻².

**Regime A** (initial Re_local = 0.018 < 2/7):
- max Re_local over all t ∈ [0,3]: 0.0181
- No breach flag raised
- Solution smooth throughout ✓

**Regime B** (initial Re_local × 10):
- First breach at t=1.78
- Re_local at breach: 0.286 = 2/7
- Gradient spike follows breach flag

---

## Real DNS Protocol

Replace mock integrator with Dedalus or ChannelFlow:

```python
# At each timestep:
omega = solver.compute_enstrophy()      # local enstrophy field
L = compute_local_scale(omega, nu)      # Taylor microscale
Re_local = omega * L**2 / nu
if Re_local.max() > 2/7:
    log_breach(t, Re_local.max(), Re_local.argmax())
```

**Target configuration:** 256³ Taylor-Green vortex, Re=1600, t ∈ [0,20].

**Falsification test:** If blow-up occurs without Re_local ever exceeding 2/7, the criterion is wrong. If blow-up is always preceded by a breach, TIG has made a genuine predictive statement.

Raw Dedalus logs will be released at github.com/TiredofSleep/ck upon completion.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
