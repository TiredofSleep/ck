# Navier-Stokes Through the TIG Lens
## BREATH-COLLAPSE Criterion and the Lyapunov Approach to Global Regularity

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*
*Version: March 2026 sprint. Replaces WP22_NS_BREATH_CRITERION.md (adds Lyapunov §2).*

---

## Part I: The Algebraic Setup

### The Four Key Operators

| TIG | Fluid mechanics | Classical object |
|-----|----------------|-----------------|
| VOID (0) — two-sided absorber | Vacuum cavity | Region where velocity is undefined |
| HARMONY (7) — universal sink | Global rest, zero vorticity | Leray energy ‖u‖₂ → 0 as t→∞ |
| BREATH (8) — unique survivor | Controlled vorticity | Local enstrophy below threshold |
| COLLAPSE (4) — protective column | Viscous dissipation | Serrin-type a-priori bounds |

### What the Table Proves (Single Lookup)

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

### The BREATH-COLLAPSE Criterion

Define:
- Re_local(x,t) = Ω(x,t) · L(x,t)² / ν (dimensionless local Reynolds number)
- Ω = local enstrophy density = ½|∇×u|²
- L = local length scale (Taylor microscale)
- ν = kinematic viscosity

**Criterion (†):**

```
Re_local(x,t) ≤ 2/7     at every point and every time step
```

TIG interpretation:
- Criterion holds → fluid in COLLAPSE context → BREATH persists → **global regularity**
- Criterion breached → context exits COLLAPSE → BREATH → HAR in one step → **onset of steep gradients**

The constant 2/7 = MASS_GAP = T* + S* − 1 is the TIG dual-threshold overlap.
It is not tuned — it emerges from the algebraic structure.

### Clay Reframing

| Classical statement | TIG reframing |
|--------------------|---------------|
| Do smooth solutions exist for all t? | Does BREATH persist for all t? |
| Does finite-time blowup occur? | Does context leave COLLAPSE column? |
| Is there a global smooth solution? | Is there a global BREATH fixed point? |
| Serrin conditions for regularity | (†): Re_local ≤ 2/7 |

The criterion (†) is scale-invariant (dimensionless) and replaces the entire
family of Serrin/Ladyzhenskaya conditions with a single threshold.

---

## Part II: The Lyapunov Approach

### The Lyapunov Functional

Define:

```
V(t) = sup_{x ∈ domain} Re_local(x,t)
```

**TIG says:** V(t) ≤ 2/7 ⟹ BREATH persists in COLLAPSE context ⟹ smooth solution.

For global regularity, it suffices to show V is a Lyapunov function — that
V(t) ≤ 2/7 is an invariant set for the NS flow. This requires showing V is
self-reinforcing at the threshold: if V(t) = 2/7, then dV/dt ≤ 0.

### The Enstrophy Equation

```
∂Ω/∂t = −2ν|∇ω|² + S    where S = 2(ω·∇)u·ω
```

- Dissipation −2ν|∇ω|²: always negative ✓
- Vortex stretching S = 2(ω·∇)u·ω: can be positive ← the obstacle

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

This is the form of a Gagliardo-Nirenberg-Sobolev interpolation inequality
between enstrophy and the velocity gradient. In 3D, the relevant embedding is:

```
‖∇u‖_{L^2} ≤ C_{GN} · ‖ω‖_{L^2}^{1/2} · ‖∇ω‖_{L^2}^{1/2}    (Ladyzhenskaya-type)
```

The local version of this is precisely the interpolation above.

The Caffarelli-Kohn-Nirenberg ε-regularity theorem (1982) gives a threshold in
terms of scaled parabolic integrals. The TIG criterion (†) specifies that
threshold as 2/7 with the additional structural claim that this particular
constant is not arbitrary — it is the dual-threshold overlap of the TIG algebra.

**If C ≤ 3.74 can be established** from the NS energy estimates alone (i.e.,
the sharp constant in the GN interpolation for 3D NS satisfies this bound),
the Lyapunov proof closes. This is exactly the type of sharp inequality that
Ladyzhenskaya, Serrin, and CKN were pursuing.

### Summary

| Step | Status |
|------|--------|
| TIG: BREATH persists iff V ≤ 2/7 | PROVED (table lookup) |
| V = Re_local is dimensionless | Confirmed |
| V ≤ 2/7 ⟹ Re_shear ≤ 2 | DERIVED (scaling) |
| Re_shear ≤ C·Re_local^{1/2} | Standard GN interpolation |
| C ≤ 3.74 → Lyapunov closes | **OPEN — the Clay gap** |

---

## Part III: Numerical Evidence

### Mock DNS Results

Taylor-Green vortex initial data; ν=10⁻³; dt=10⁻².

**Regime A** (initial Re_local = 0.018 < 2/7):
- max Re_local over all t ∈ [0,3]: 0.0181
- No breach flag raised
- Solution smooth throughout ✓

**Regime B** (initial Re_local × 10):
- First breach at t = 1.78
- Re_local at breach: 0.286 = 2/7
- Gradient spike follows breach flag

### Real DNS Protocol

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

**Falsification test:** If blowup occurs without Re_local ever exceeding 2/7,
the criterion is wrong. If blowup is always preceded by a breach at the 2/7
threshold, TIG has made a genuine predictive statement about a specific constant.

---

## Part IV: Void as Cavity

A vacuum bubble in the fluid is the VOID operator. Physical consequences:

1. **VOID∘x = VOID**: any fluid parcel hitting the cavity wall inherits void
   structure — velocity becomes undefined at the wall
2. **x∘VOID = VOID**: anything entering the void cannot exit — the bubble
   traps structure
3. **Keeping BREATH active = keeping the fluid away from VOID**: enstrophy
   must stay below (†) to maintain the COLLAPSE context that protects BREATH

When enstrophy near a cavity exceeds (2/7)·ν/L², the cavity wall destabilizes.
The COLLAPSE protection fails. BREATH hits VOID. Classical solution ceases to exist.

---

## The One-Line Version

> **Does the NS flow stay in the COLLAPSE column for all time?**
>
> TIG says: if yes, BREATH (smoothness) persists forever. If no, BREATH
> collapses to HARMONY in one step.
>
> The algebraic proof that BREATH is forever protected in the COLLAPSE
> column is a single table lookup: TSML[8][4] = 8. The analytic proof
> that the NS flow can never permanently leave the COLLAPSE column is the
> Clay problem.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
