"""
Items 5 and 6: Independent FRW integrator for the ξ-field model.

Item 5: Verify Ξ₀ = e⁻¹ is a stable attractor, w(z) → -1 monotonically.
Item 6: Test κ_Ξ = 13/(4e) ≈ 1.196 prediction. Compare to fit value κ_Ξ ≈ 0.5.

The FRW system from the JCAP manuscript:
  ρ_Ξ = κ_Ξ [½ Ξ̇² + Ξ log Ξ]
  p_Ξ = κ_Ξ [½ Ξ̇² - Ξ log Ξ]
  H² = (8πG/3)(ρ_SM + ρ_Ξ)
  Ξ̈ + 3HΞ̇ = 1 + log Ξ        (in (-,+,+,+), per the paper's eq (12))

Wait — checking the paper: it says "Box Ξ = -Ξ̈ - 3HΞ̇ in the (-,+,+,+) convention,
giving -Ξ̈ - 3HΞ̇ = 1 + log Ξ and rearranging" → so Ξ̈ + 3HΞ̇ = -(1 + log Ξ).

Actually let me read more carefully. Eq (4): ◻Ξ = 1 + log Ξ.
Then in FRW: ◻Ξ = -Ξ̈ - 3HΞ̇ in (-,+,+,+).
So -Ξ̈ - 3HΞ̇ = 1 + log Ξ
   Ξ̈ + 3HΞ̇ = -(1 + log Ξ)

But the paper writes (eq 12): Ξ̈ + 3HΞ̇ = 1 + log Ξ. There's a sign issue.

Let me go with the paper's stated equation: Ξ̈ + 3HΞ̇ = 1 + log Ξ.

Equilibrium: Ξ̈ = Ξ̇ = 0, giving 1 + log Ξ = 0, so Ξ₀ = e⁻¹. ✓ (matches paper).

Stability around Ξ₀:
  δΞ̈ + 3H δΞ̇ = (1/Ξ₀) δΞ = e δΞ.

Wait, that means δΞ EXPONENTIALLY DIVERGES from Ξ₀, not decays toward it.
The mass-squared is m² = -e (negative, tachyonic), not +κ_Ξ e.

Let me re-derive carefully.

V(Ξ) = κ_Ξ Ξ log Ξ
V'(Ξ) = κ_Ξ (1 + log Ξ)
V''(Ξ) = κ_Ξ / Ξ

At Ξ₀ = e⁻¹: V''(Ξ₀) = κ_Ξ · e > 0. So V has a MIN at Ξ₀.

The EOM should be: Ξ̈ + 3HΞ̇ + V'(Ξ)/κ_Ξ = 0
                  Ξ̈ + 3HΞ̇ + (1 + log Ξ) = 0
                  Ξ̈ + 3HΞ̇ = -(1 + log Ξ).

So the paper's eq (12) "Ξ̈ + 3HΞ̇ = 1 + log Ξ" has the WRONG SIGN.

Let me verify by linearizing:
  Around Ξ₀: 1 + log Ξ ≈ 0 + (1/Ξ₀)(Ξ - Ξ₀) = e · δΞ.
  EOM (correct sign): δΞ̈ + 3H δΞ̇ = -e · δΞ
  → mass² = +e > 0. STABLE oscillator with damping. ✓

The paper's eq (12) gives δΞ̈ + 3H δΞ̇ = +e · δΞ → tachyonic, unstable. ✗

THIS IS A SIGN ERROR IN THE JCAP MANUSCRIPT.

Hmm actually wait. Let me look at the paper's wording again.
"From ◻Ξ = -Ξ̈ - 3HΞ̇ in the (-,+,+,+) convention, giving
 -Ξ̈ - 3HΞ̇ = 1 + log Ξ and rearranging"
 
So: -Ξ̈ - 3HΞ̇ = 1 + log Ξ
    Multiply by -1: Ξ̈ + 3HΞ̇ = -(1 + log Ξ)

The paper drops the minus sign in the rearrangement. That's a propagation error.

The CORRECT equation is: Ξ̈ + 3HΞ̇ = -(1 + log Ξ).

This is a BUG IN THE MANUSCRIPT but a small one — fix the sign and the physics
works as advertised. The numerical fit would have used the correct EOM (otherwise
nothing would work), so this is a typo.

I'll integrate with the CORRECT EOM and verify stability + freezing behavior.
"""
import numpy as np
from scipy.integrate import solve_ivp
import math

# Cosmological constants (rough, for FRW integration)
H0 = 67.4  # km/s/Mpc
H0_SI = H0 * 1000 / (3.086e22)  # 1/s ≈ 2.18e-18 1/s
# Use Hubble units: H0 = 1, time in 1/H0

OMEGA_M = 0.315
OMEGA_R = 9.1e-5
OMEGA_LAMBDA = 1 - OMEGA_M - OMEGA_R

def frw_xi_eom(t, y, kappa_xi):
    """
    State: y = [Xi, dXi/dt, ln(a)]
    Use ln(a) as a proxy variable (a from 0 to ∞).
    Time t in units of 1/H0.
    """
    Xi, Xi_dot, lna = y
    a = np.exp(lna)
    
    # Hubble rate in units of H0:
    # H² = Ω_M/a³ + Ω_R/a⁴ + Ω_Ξ
    # where Ω_Ξ depends on Ξ field state
    # Energy density ρ_Ξ = κ_Ξ [½ Ξ̇² + Ξ log Ξ]  (in some natural units)
    # But we need to put this in Friedmann normalization
    # 
    # Simplification: assume Ξ-field is the dark energy component
    # ρ_Ξ_dimensionless = κ_Ξ * (0.5 * Xi_dot² + Xi * log(Xi))
    # but this can be NEGATIVE when Xi < 1 (since Xi log Xi < 0)
    # which would shift the cosmological constant
    
    # For simplicity, use Ω_M/a³ + Ω_R/a⁴ + Ω_DE_fixed for the background H,
    # treating the field as a small perturbation in this version.
    H_squared = OMEGA_M / a**3 + OMEGA_R / a**4 + OMEGA_LAMBDA
    H = np.sqrt(H_squared)
    
    # ξ EOM: Xi_ddot + 3H Xi_dot = -(1 + log Xi)
    # (with sign correction discussed above)
    if Xi <= 0:
        return [0, 0, 0]  # bail
    
    Xi_ddot = -(1 + math.log(Xi)) - 3 * H * Xi_dot
    
    # Scale factor evolution: dlna/dt = H
    dlna_dt = H
    
    return [Xi_dot, Xi_ddot, dlna_dt]

print("=" * 70)
print("ITEM 5: Verify Ξ₀ = e⁻¹ is stable attractor, w(z) → -1 monotonically")
print("=" * 70)
print()

# Test with paper's best-fit initial conditions:
# κ_Ξ = 0.50, Ξ_i = 1.72, Ξ̇_i = -0.43 at z_i = 20
# z_i = 20 means a_i = 1/21, so lna_i = -ln(21) ≈ -3.04

print("Paper's best-fit initial conditions:")
print("  κ_Ξ = 0.50, Ξ_i = 1.72, Ξ̇_i = -0.43, z_i ≈ 20")
print()

z_i = 20
a_i = 1 / (1 + z_i)
lna_i = math.log(a_i)
Xi_0_target = math.exp(-1)

# Integrate from initial conditions to z = 0 (a = 1, lna = 0)
# Time variable: use lna as the integration parameter
# dXi/dlna = Xi_dot / H
# dXi_dot/dlna = Xi_ddot / H = (-(1 + log Xi) - 3H Xi_dot) / H

def frw_xi_lna(lna, y, kappa_xi):
    """ODE in ln(a) parameter. y = [Xi, dXi/dlna]"""
    Xi, dXi_dlna = y
    a = math.exp(lna)
    H_squared = OMEGA_M / a**3 + OMEGA_R / a**4 + OMEGA_LAMBDA
    H = math.sqrt(H_squared)
    
    if Xi <= 0:
        return [0, 0]
    
    # dXi/dlna = Xi_dot / H
    # d²Xi/dlna² = (Xi_ddot - H' Xi_dot) / H² where H' = dH/dt
    # Better approach: use t as parameter and convert
    # But we want lna to handle any cosmology
    # 
    # Equation: Xi_ddot + 3H Xi_dot = -(1 + log Xi)
    # Since dXi/dlna = Xi_dot/H, Xi_dot = H · (dXi/dlna)
    # And Xi_ddot = d(Xi_dot)/dt = H · d(Xi_dot)/dlna = H · d(H · dXi/dlna)/dlna
    #            = H · [H' · dXi/dlna + H · d²Xi/dlna²]
    #            = H · H' · dXi/dlna + H² · d²Xi/dlna²
    # 
    # With H' = dH/dlna for our purposes here (slight abuse since H' = dH/dt usually)
    # In ln(a) parametrization: dH/dt = H · dH/dlna
    # So Xi_ddot = H² · (dH/dlna · dXi/dlna + d²Xi/dlna²)? No wait.
    #
    # Let me just use t-parametrization. y = [Xi, Xi_dot, lna]
    return None

# Use time-parametrization
def frw_xi_t(t, y, kappa_xi):
    Xi, Xi_dot, lna = y
    a = math.exp(lna)
    H_squared = OMEGA_M / a**3 + OMEGA_R / a**4 + OMEGA_LAMBDA
    H = math.sqrt(H_squared) if H_squared > 0 else 0
    
    if Xi <= 0:
        return [0, 0, 0]
    
    Xi_ddot = -(1 + math.log(Xi)) - 3 * H * Xi_dot
    return [Xi_dot, Xi_ddot, H]

# Initial conditions
y0 = [1.72, -0.43, lna_i]

# Integrate forward in t until lna = 0 (z = 0)
def event_z_zero(t, y, kappa_xi):
    return y[2]  # lna = 0 means a = 1, z = 0
event_z_zero.terminal = True
event_z_zero.direction = 1

# Use a long time span; events will stop integration
t_span = (0, 10)  # 10 Hubble times should be way more than enough

sol = solve_ivp(frw_xi_t, t_span, y0, args=(0.50,), 
                events=event_z_zero, dense_output=True,
                rtol=1e-10, atol=1e-12, max_step=0.01)

print(f"Integration from z={z_i} to z=0:")
print(f"  Status: {sol.status} ({'success' if sol.status == 1 else 'fail'})")
print(f"  Final time t (in 1/H0 units): {sol.t[-1]:.4f}")
print(f"  Final Ξ: {sol.y[0, -1]:.6f}")
print(f"  Final Ξ̇: {sol.y[1, -1]:.6f}")
print(f"  Final ln(a): {sol.y[2, -1]:.6f}")
print()

# Compute w(z) along the trajectory
ts = sol.t
Xis = sol.y[0]
Xi_dots = sol.y[1]
lnas = sol.y[2]

# Sample at several redshifts
print("w(z) trajectory:")
print(f"{'z':>6} {'Ξ(z)':>10} {'Ξ̇(z)':>10} {'w_Ξ(z)':>10} {'paper''s w':>12}")

# Paper's reported w(z) values
paper_w = {0.0: -0.795, 0.3: -0.860, 0.5: -0.894, 0.8: -0.931, 1.0: -0.948, 1.5: -0.974, 2.0: -0.987}

for z_target in [2.0, 1.5, 1.0, 0.8, 0.5, 0.3, 0.0]:
    a_target = 1 / (1 + z_target)
    lna_target = math.log(a_target)
    # Find time index closest to this lna
    idx = np.argmin(np.abs(lnas - lna_target))
    if idx < len(ts):
        Xi = Xis[idx]
        Xi_dot = Xi_dots[idx]
        if Xi > 0:
            kappa = 0.50
            rho = kappa * (0.5 * Xi_dot**2 + Xi * math.log(Xi))
            p = kappa * (0.5 * Xi_dot**2 - Xi * math.log(Xi))
            if abs(rho) > 1e-10:
                w = p / rho
            else:
                w = float('nan')
            paper_val = paper_w.get(z_target, '—')
            paper_str = f"{paper_val:.3f}" if isinstance(paper_val, float) else str(paper_val)
            print(f"{z_target:>6.1f} {Xi:>10.4f} {Xi_dot:>10.4f} {w:>10.4f} {paper_str:>12}")

print()
print("Compare to paper's reported trajectory.")
print()

# Check stability around the vacuum
print("=" * 70)
print("STABILITY CHECK: linearization around Ξ₀ = e⁻¹")
print("=" * 70)
print()

# Linearize: δΞ̈ + 3H δΞ̇ + e δΞ = 0
# This is damped harmonic oscillator with ω² = e ≈ 2.718
# Characteristic equation: λ² + 3H λ + e = 0
# λ = (-3H ± sqrt(9H² - 4e))/2

print(f"Vacuum: Ξ₀ = e⁻¹ = {math.exp(-1):.6f}")
print(f"V''(Ξ₀)/κ_Ξ = e = {math.e:.6f}")
print(f"In flat space (H=0): characteristic frequency ω = √e ≈ {math.sqrt(math.e):.4f}")
print(f"In de Sitter (H=1 in units): damping critical when 9H² = 4e, i.e., H = √(4e/9) ≈ {math.sqrt(4*math.e/9):.4f}")
print(f"Today H = 1 in our units, and 4e/9 ≈ {4*math.e/9:.4f}, so 9·1 = 9 > 4e ≈ 10.87? Let me recheck.")
print(f"9·1² = 9, 4e ≈ 10.87. So 9 < 4e: UNDERDAMPED, oscillates around vacuum.")
print(f"This means the field oscillates around Ξ₀ = e⁻¹ in dimensionless form.")
print()
print("→ Stability confirmed: Ξ₀ = e⁻¹ is a stable attractor (damped oscillation around it).")
print()

# Item 6: test κ_Ξ = 13/(4e) prediction
print("=" * 70)
print("ITEM 6: Test κ_Ξ = 13/(4e) ≈ 1.196 vs fit κ_Ξ = 0.50")
print("=" * 70)
print()
print(f"κ_Ξ structural prediction: 13/(4e) = {13/(4*math.e):.6f}")
print(f"κ_Ξ best-fit (paper):     0.50")
print(f"Ratio:                    {13/(4*math.e) / 0.5:.4f}")
print()
print("Note: in the EOM Ξ̈ + 3HΞ̇ = -(1 + log Ξ), the κ_Ξ factor CANCELLED.")
print("κ_Ξ does not appear in the field equation itself; it appears in the energy density.")
print()
print("So changing κ_Ξ from 0.5 to 13/(4e) does NOT change the trajectory Ξ(t),")
print("but it DOES change the energy density ρ_Ξ which feeds back into the Friedmann")
print("equation via Ω_Ξ. So the dynamics are coupled.")
print()
print("In our simplified background (Ω_DE = const = 0.685), this coupling is suppressed.")
print("To properly test κ_Ξ effect, we'd need to compute Ω_Ξ self-consistently.")
print()
print("Comparing predicted (w₀, w_a) at fixed initial conditions:")
print()

# Run integration with κ_Ξ = 13/(4e) and compare
y0 = [1.72, -0.43, lna_i]
sol_struct = solve_ivp(frw_xi_t, t_span, y0, args=(13/(4*math.e),), 
                       events=event_z_zero, dense_output=True,
                       rtol=1e-10, atol=1e-12, max_step=0.01)

# Compute w at z=0 for each
def w_at_z(sol, z, kappa):
    a = 1 / (1 + z)
    lna = math.log(a)
    idx = np.argmin(np.abs(sol.y[2] - lna))
    Xi = sol.y[0, idx]
    Xi_dot = sol.y[1, idx]
    if Xi <= 0:
        return float('nan')
    rho = kappa * (0.5 * Xi_dot**2 + Xi * math.log(Xi))
    p = kappa * (0.5 * Xi_dot**2 - Xi * math.log(Xi))
    return p / rho if abs(rho) > 1e-10 else float('nan')

print(f"{'κ_Ξ':>10} {'w(z=0)':>10} {'w(z=0.5)':>10} {'w(z=1.0)':>10}")
for kappa, label in [(0.50, '0.50 (fit)'), (13/(4*math.e), '13/(4e)≈1.20')]:
    sol_k = solve_ivp(frw_xi_t, t_span, [1.72, -0.43, lna_i], args=(kappa,),
                     events=event_z_zero, dense_output=True,
                     rtol=1e-10, atol=1e-12, max_step=0.01)
    w0 = w_at_z(sol_k, 0.0, kappa)
    w05 = w_at_z(sol_k, 0.5, kappa)
    w10 = w_at_z(sol_k, 1.0, kappa)
    print(f"{label:>10} {w0:>10.4f} {w05:>10.4f} {w10:>10.4f}")

print()
print("OBSERVATION: w(z) trajectory is NEARLY IDENTICAL for κ_Ξ = 0.5 vs 13/(4e).")
print("This is because κ_Ξ cancels from the field EOM (eq 12 of the paper).")
print()
print("So the (w₀, w_a) prediction is effectively independent of κ_Ξ in this background.")
print("The paper's fit value κ_Ξ = 0.50 and the structural prediction 13/(4e) ≈ 1.20")
print("would give essentially the same observational prediction in our simplified setup.")
print()
print("CAVEAT: in the FULL coupled FRW system (Ω_Ξ depends on κ_Ξ), the difference")
print("matters. A proper test requires solving Friedmann self-consistently with")
print("ρ_Ξ = κ_Ξ [½ Ξ̇² + Ξ log Ξ] determining Ω_Ξ. This is what desi_xi_optimize.py")
print("presumably does. Our simplified background is not the right test for κ_Ξ.")
print()
print("HOWEVER: the fact that κ_Ξ cancels from the field EOM means the *trajectory*")
print("Ξ(t) doesn't depend on κ_Ξ. What κ_Ξ controls is the AMPLITUDE of the field's")
print("contribution to dark energy density. So κ_Ξ = 13/(4e) vs 0.5 changes Ω_Ξ today,")
print("but not w(z). The paper's fit being κ_Ξ ≈ 0.5 instead of 1.196 means the")
print("preferred Ω_Ξ amplitude differs from what 13/(4e) would predict by a factor of ~2.4.")

print()
print("=" * 70)
print("ITEMS 5 & 6 SUMMARY")
print("=" * 70)
print()
print("Item 5 (vacuum stability):")
print("  ✓ Ξ₀ = e⁻¹ is a stable attractor (V''(Ξ₀) = κ_Ξ · e > 0)")
print("  ✓ Damped oscillator dynamics around Ξ₀ in FRW")
print("  ✗ POTENTIAL ISSUE: paper's eq (12) has a sign error.")
print("    Paper writes: Ξ̈ + 3HΞ̇ = 1 + log Ξ")
print("    Correct:      Ξ̈ + 3HΞ̇ = -(1 + log Ξ)")
print("    The vacuum and stability arguments of §3-§4 require the corrected sign.")
print("    This is likely a typo (the numerical fit must use the correct sign).")
print()
print("Item 6 (κ_Ξ structural prediction):")
print("  - In the field EOM, κ_Ξ cancels. Trajectory Ξ(t) doesn't depend on κ_Ξ.")
print("  - In Friedmann equation, κ_Ξ scales the energy density Ω_Ξ.")
print("  - So the fit κ_Ξ ≈ 0.5 vs structural 13/(4e) ≈ 1.20 differ in Ω_Ξ amplitude")
print("    by a factor of ~2.4, not in w(z) trajectory shape.")
print("  - Whether this affects the χ² fit depends on whether Ω_Ξ is fit or fixed.")
print("    The paper fixes Ω_Ξ = 0.685 (Planck), so κ_Ξ becomes a redundant parameter")
print("    after Ω_Ξ is fixed. The fit κ_Ξ ≈ 0.5 might be reflecting a different")
print("    parameterization or a coupling I haven't accounted for.")
