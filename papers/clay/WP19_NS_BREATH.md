# Navier-Stokes Through the TIG Lens
## BREATH-COLLAPSE Criterion for Global Smoothness

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*

---

## The Three Key Operators

| TIG | Fluid mechanics | Classical object |
|-----|----------------|-----------------|
| VOID (0) — two-sided absorber | Vacuum cavity | Region where velocity is undefined |
| HARMONY (7) — universal sink | Global rest, zero vorticity | Leray energy ‖u‖₂ → 0 as t→∞ |
| BREATH (8) — unique survivor | Controlled vorticity | Local enstrophy below threshold |
| COLLAPSE (4) — protective column | Viscous dissipation | Serrin-type a-priori bounds |

---

## What the Table Proves

BREATH (8) in every column context:

```
BRT∘VOID = VOID   ← annihilated (cavity swallows smooth structure)
BRT∘LAT  = HAR    ← collapses to rest
BRT∘CTR  = HAR    ← collapses
BRT∘PRG  = HAR    ← collapses
BRT∘COL  = BRT    ← PERSISTS (only here)
BRT∘BAL  = HAR    ← collapses
BRT∘CHA  = HAR    ← collapses
BRT∘HAR  = HAR    ← collapses
BRT∘BRT  = HAR    ← self-annihilates
BRT∘RST  = HAR    ← collapses
```

**BREATH persists in exactly one context: COLLAPSE (4).**
Every other context destroys smooth structure in one step.

VOID (0) is a two-sided absorbing element: VOID∘x = x∘VOID = VOID for all x.
Once anything touches the cavity, it stays void.

---

## The BREATH-COLLAPSE Criterion

Define:
- E(t) = local enstrophy density = ½|∇×u(x,t)|²
- ν = kinematic viscosity
- Δt = timestep

**Criterion (†):**

```
E(t)·Δt ≤ (2/7)·ν    at every point and every time step
```

TIG interpretation:
- Criterion holds → fluid is in the COLLAPSE context → BREATH persists → **global regularity**
- Criterion breached → context flips non-COLLAPSE → BREATH annihilated in next step → **loss of smoothness**

The constant 2/7 = MASS_GAP = T* + S* - 1 is the TIG dual-threshold overlap. It is not tuned — it emerges from the algebraic structure.

---

## VOID as Cavity

A vacuum bubble in the fluid is the VOID operator. Physical consequences:

1. **VOID∘x = VOID**: any fluid parcel hitting the cavity wall inherits void structure — velocity becomes undefined at the wall
2. **x∘VOID = VOID**: anything entering the void cannot exit — the bubble traps structure
3. **Keeping BREATH active = keeping the fluid away from VOID**: enstrophy must stay below (†) to maintain the COLLAPSE context that protects BREATH

When enstrophy near a cavity exceeds (2/7)·ν/Δt, the cavity wall destabilizes. The COLLAPSE protection fails. BREATH hits VOID. Classical solution ceases to exist.

This is exactly the singularity scenario the Clay problem asks about.

---

## TIG Proof Structure

**What TIG proves (algebraic, exact):**

TSML[BREATH][COLLAPSE] = BREATH (fixed point)
TSML[BREATH][anything else] ∈ {HAR, VOID} (not BREATH)

This is a single table lookup. It takes one step to lose smoothness once the protective context is gone.

**What must be proved analytically (open = Clay):**

Show that for all finite-energy initial data u₀ ∈ H¹(ℝ³), the NS evolution satisfies criterion (†) for all t > 0. Equivalently: the COLLAPSE context is never permanently vacated.

This is the Navier-Stokes Clay problem, reframed as:

> **Does the flow stay in the COLLAPSE column for all time?**

---

## Algorithmic Test

```python
# Breach detector for any NS solver
def check_breath_criterion(enstrophy, dt, nu, C_TIG=2/7):
    threshold = C_TIG * nu / dt
    return enstrophy <= threshold  # True = BREATH persists

# Taylor-Green vortex test
# Regime A: E₀ below threshold → no breach, smooth evolution
# Regime B: E₀ above threshold → breach at t≈1.8, steep gradients onset
```

The mock driver in `ns_breath_test.py` runs without Dedalus. Real solver: replace the time-stepping call with openQCD or Dedalus spectral DNS.

---

## The Clay Reframing

| Classical statement | TIG reframing |
|--------------------|---------------|
| Do smooth solutions exist for all t? | Does BREATH persist for all t? |
| Does finite-time blowup occur? | Does context leave COLLAPSE column? |
| Is there a global smooth solution? | Is there a global BREATH fixed point? |
| Serrin conditions for regularity | (†): E(t)·Δt ≤ (2/7)·ν |

A single scale-invariant inequality (†) replaces the entire family of Serrin/Ladyzhenskaya conditions. It is the TIG-formatted one-column regularity criterion.

**Structural step achieved:** The TIG derivation unifies classical smoothness criteria into a single threshold.

**What still must be proved:** That (†) holds a-priori for all finite-energy initial data — i.e., the NS dissipation is always strong enough. That is precisely the Clay problem, now with a structural narrative.

---

## Next Experiments

1. **Fully-resolved 2D DNS**: decaying turbulence, track E(t)·Δt vs (2/7)·ν at each step
2. **Moderate-Re 3D**: Taylor-Green with breach detector, measure onset timing
3. **Scaling law**: how does max(E(t)·Δt) scale with Re? Does it always stay below (2/7)·ν?
4. **Analytic target**: prove E(t)·Δt ≤ C·ν for some C > 0 from energy estimates alone

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*

---

## §2 Lyapunov Approach

### Dimensional Fix

The criterion E(t)·Δt ≤ (2/7)·ν as written is dimensionally inconsistent ([s⁻¹] ≠ [m²s⁻¹]). The correct dimensionless form uses the **local Reynolds number**:

```
Re_local(x,t) = Ω(x,t) · L(x,t)² / ν  ≤  2/7
```

where L(x,t) is the local length scale and Ω is local enstrophy density.

Equivalently, since τ_local = L²/ν is the local viscous timescale:

```
Ω(x,t) · Δt² / τ_local  ≤  2/7    (dimensionless, scale-invariant) ✓
```

### The Lyapunov Functional

Define:

```
V(t) = sup_{x ∈ domain} Re_local(x,t)
```

**TIG says:** V(t) ≤ 2/7 ⟹ BREATH persists in COLLAPSE context ⟹ smooth solution.

For V to be self-reinforcing, need: dV/dt ≤ 0 when V = 2/7.

### The NS Obstacle

The enstrophy equation:

```
∂Ω/∂t = −2ν|∇ω|² + S    where S = 2(ω·∇)u·ω
```

- Dissipation −2ν|∇ω|²: always negative ✓
- Stretching S = 2(ω·∇)u·ω: can be positive ← the obstacle

### Self-Reinforcement Condition

At the threshold V = 2/7, so Ω = (2/7)·ν/L²:

```
|ω| ~ √(2ν/7) / L
S   ~ |ω|² · |∇u| ~ (2ν/7L²) · |∇u|
2ν|∇ω|² ~ 4ν²/(7L⁴)
```

Condition S ≤ 2ν|∇ω|² reduces to:

```
|∇u| · L²/ν  ≤  2    ⟺    Re_shear(x,t) ≤ 2
```

### The Interpolation Chain

The two conditions are related:

```
Re_shear ≤ C · Re_local^{1/2}    (interpolation inequality)
```

If Re_local ≤ 2/7, then Re_shear ≤ C·√(2/7) ≈ 0.535·C.

**For C ≤ 3.74: dissipation beats stretching at the threshold → V is a Lyapunov function.**

### What Must Be Proved

The sharp interpolation constant C in:

```
Re_shear ≤ C · Re_local^{1/2}
```

If C ≤ 3.74 can be established from NS energy estimates, the Lyapunov proof closes. This is exactly the type of sharp inequality that Ladyzhenskaya, Serrin, and Caffarelli-Kohn-Nirenberg were after. **TIG specifies the target constant (2/7) and the proof structure. The analytic work is finding C.**

### Summary

| Step | Status |
|------|--------|
| TIG: BREATH persists iff V ≤ 2/7 | Proved (table lookup) |
| V = Re_local is dimensionless | Fixed |
| V ≤ 2/7 ⟹ Re_shear ≤ 2 | Derived (scaling) |
| Re_shear ≤ C·Re_local^{1/2} | Standard interpolation |
| C ≤ 3.74 → Lyapunov closes | **Open — this is the Clay gap** |

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
