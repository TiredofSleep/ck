"""
DESI PARAMETER OPTIMIZATION: Logarithmic Quintessence xi Model
NEW ACTION VERSION (2026-05-05)

Replaces single-kappa parametrization with explicit M_Pl^2 kinetic + Lambda^4
potential prefactors:

  L_xi = (1/2) * M_Pl^2 * g^uv * d_u xi * d_v xi + Lambda^4 * xi * log(xi)

In reduced Planck units (M_Pl = 1, 8 pi G = 1):
  rho_xi = (1/2) * dot(xi)^2 + Lambda^4 * xi * log(xi)
  p_xi   = (1/2) * dot(xi)^2 - Lambda^4 * xi * log(xi)
  EoM (cosmic time): xi_ddot + 3 H xi_dot = -Lambda^4 * (1 + log(xi))
  EoM (e-folding):   xi'' = -(3 + H'/H) xi' - Lambda^4 * (1 + log(xi)) / H^2

Vacuum xi_0 = e^{-1} unchanged (Lambda^4 cancels in 1 + log(xi_0) = 0).
Mass m_xi^2 = Lambda^4 * e (in reduced Planck units, gives Lambda ~ dark energy
scale when m_xi ~ H_0).

Sign fix from original script applied: EoM has minus sign on (1+log xi)/H^2.
Dimensional rewrite: kappa removed from kinetic term, replaced by 1
(reduced Planck units); kappa on potential term becomes Lambda^4.

Copyright (c) 2026 Brayden Ross Sanders / 7Site LLC
"""

import numpy as np
import math
import sys

# =====================================================================
# COSMOLOGICAL PARAMETERS (reduced Planck units, energies in H_0^2 units)
# =====================================================================
Omega_m0 = 0.315
Omega_r0 = 9.1e-5
Omega_xi0 = 1 - Omega_m0 - Omega_r0
xi0_vac = math.exp(-1)

# DESI DR1 targets
W0_DESI = -0.827
W0_ERR = 0.063
WA_DESI = -0.75
WA_ERR = 0.27

def solve_xi_frw(Lambda4, xi_init, xi_dot_init, N_start=-4, N_end=0.5, N_steps=5000):
    """Solve coupled xi + Friedmann under the new action.
    
    Lambda4 is the potential prefactor in reduced Planck units, in units
    where rho is normalized to 3 H_0^2 (so total Omega = 1 today).
    """
    dN = (N_end - N_start) / N_steps
    xi = xi_init
    xi_p = xi_dot_init  # d_xi/dN

    w_at_z = {}

    for step in range(N_steps):
        N = N_start + step * dN
        a = math.exp(N)

        rho_m = Omega_m0 * a**(-3)
        rho_r = Omega_r0 * a**(-4)

        if xi < 1e-30:
            xi = 1e-30

        xi_log_xi = xi * math.log(xi)
        # Kinetic backreaction: M_Pl^2 = 1, so denom = 1 - (1/2) * xi_p^2 * H2 / H2
        # Wait: kinetic energy in cosmic time is (1/2) M_Pl^2 dot(xi)^2.
        # dot(xi) = H * xi_p, so kinetic = (1/2) H^2 xi_p^2 (M_Pl^2 = 1)
        # The kinetic energy enters the Friedmann implicit denominator:
        # H^2 = (rho_m + rho_r + V) + 0.5 H^2 xi_p^2
        # H^2 (1 - 0.5 xi_p^2) = rho_m + rho_r + V
        # So denom = 1 - 0.5 * xi_p^2  (kappa removed; M_Pl^2 = 1)
        denom = 1 - 0.5 * xi_p**2
        if denom < 0.01:
            denom = 0.01

        # Potential term in Friedmann: Lambda^4 * xi * log(xi)
        H2 = (rho_m + rho_r + Lambda4 * xi_log_xi) / denom
        if H2 < 1e-30:
            H2 = 1e-30
        H = math.sqrt(H2)

        # Energy density and pressure (in script's units, where dot(xi)^2 = H^2 xi_p^2)
        # rho_xi = (1/2) M_Pl^2 dot(xi)^2 + Lambda^4 V_form
        #        = 0.5 H^2 xi_p^2 + Lambda^4 xi log(xi)
        rho_xi = 0.5 * H2 * xi_p**2 + Lambda4 * xi_log_xi
        p_xi   = 0.5 * H2 * xi_p**2 - Lambda4 * xi_log_xi

        w = p_xi / rho_xi if abs(rho_xi) > 1e-30 else -1.0
        w = max(-2.0, min(1.0, w))

        z = 1.0/a - 1 if a > 0.01 else 100.0

        for z_target in [0.0, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0]:
            if abs(z - z_target) < 0.05 and z_target not in w_at_z:
                w_at_z[z_target] = w

        # Hp_over_H: dot(H) / H^2 from Friedmann II
        # In FRW: dot(H) = -(1/2)(rho_m + rho_r + dot(xi)^2) ignoring radiation pressure
        # = -(1/2) rho_m - 2*(1/2) rho_r - (1/2) H^2 xi_p^2 (in reduced Planck)
        # divide by H^2:
        # H'/H = dot(H)/H^2 = -1.5 rho_m/H2 - 2 rho_r/H2 - 0.5 xi_p^2
        # (Including the kinetic backreaction that the original script was missing.)
        Hp_over_H = -1.5 * rho_m / H2 - 2.0 * rho_r / H2 - 0.5 * xi_p**2

        # EoM in e-foldings, NEW ACTION + SIGN FIX:
        # xi_pp = -(3 + H'/H) xi_p - Lambda^4 (1 + log xi) / H^2
        xi_pp = -(3 + Hp_over_H) * xi_p - Lambda4 * (1 + math.log(xi)) / H2

        xi += xi_p * dN
        xi_p += xi_pp * dN
        if xi < 1e-30:
            xi = 1e-30

    w0 = w_at_z.get(0.0, -1.0)
    w05 = w_at_z.get(0.5, w0)
    a05 = 1.0 / 1.5
    wa = (w05 - w0) / (1 - a05) if abs(1 - a05) > 0.01 else 0

    return w0, wa, xi, w_at_z

# =====================================================================
# GRID SEARCH over (Lambda^4, xi_init, xi_dot)
# =====================================================================
print("=" * 70)
print("DESI PARAMETER OPTIMIZATION (NEW ACTION + SIGN FIX)")
print(f"Target: w0 = {W0_DESI} +/- {W0_ERR}, wa = {WA_DESI} +/- {WA_ERR}")
print("Action: L = (1/2)(d xi)^2 + Lambda^4 xi log(xi)  [reduced Planck units]")
print("=" * 70)

# Search grid for Lambda^4 — same range as old kappa, since rho_xi today
# should still match Omega_xi ~ 0.685
Lambda4_range = np.linspace(0.3, 3.0, 20)
xi_init_range = np.linspace(0.5, 3.0, 20)
xi_dot_range = np.linspace(-0.5, 0.5, 15)

best_chi2 = 1e10
best_params = None
all_results = []
total = len(Lambda4_range) * len(xi_init_range) * len(xi_dot_range)
count = 0

print(f"\nSearching {total} parameter combinations...")

for Lambda4 in Lambda4_range:
    for xi_init in xi_init_range:
        for xi_dot in xi_dot_range:
            count += 1
            if count % 1000 == 0:
                print(f"  {count}/{total} searched, best chi2 = {best_chi2:.2f}", end='\r')

            try:
                w0, wa, xi_today, w_z = solve_xi_frw(Lambda4, xi_init, xi_dot)

                if abs(w0) > 2 or abs(wa) > 5:
                    continue

                chi2 = ((w0 - W0_DESI) / W0_ERR)**2 + ((wa - WA_DESI) / WA_ERR)**2

                all_results.append({
                    'Lambda4': Lambda4, 'xi_init': xi_init, 'xi_dot': xi_dot,
                    'w0': w0, 'wa': wa, 'chi2': chi2, 'xi_today': xi_today,
                    'w_z': w_z
                })

                if chi2 < best_chi2:
                    best_chi2 = chi2
                    best_params = all_results[-1]

            except Exception:
                pass

print(f"\n\nSearched {count} combinations. Valid results: {len(all_results)}")

# =====================================================================
# TOP 10 RESULTS
# =====================================================================
all_results.sort(key=lambda x: x['chi2'])

print(f"\n--- Top 10 Configurations ---")
print(f"{'Lambda^4':>10} {'xi_init':>8} {'xi_dot':>8} {'w0':>8} {'wa':>8} {'chi2':>8} {'xi_today':>10}")
print("-" * 75)
for r in all_results[:10]:
    print(f"{r['Lambda4']:>10.4f} {r['xi_init']:>8.3f} {r['xi_dot']:>8.3f} "
          f"{r['w0']:>8.4f} {r['wa']:>8.4f} {r['chi2']:>8.3f} {r['xi_today']:>10.4f}")

# =====================================================================
# BEST FIT ANALYSIS
# =====================================================================
if best_params:
    b = best_params
    print(f"\n{'='*70}")
    print(f"BEST FIT PARAMETERS (new action, sign-fixed)")
    print(f"{'='*70}")
    print(f"  Lambda^4  = {b['Lambda4']:.4f}  (in units of 3 H_0^2 M_Pl^2)")
    print(f"  xi_init   = {b['xi_init']:.4f} (at z~54)")
    print(f"  xi_dot    = {b['xi_dot']:.4f} (d xi / d N at z_init)")
    print(f"  w0        = {b['w0']:.4f}  (DESI: {W0_DESI} +/- {W0_ERR})")
    print(f"  wa        = {b['wa']:.4f}  (DESI: {WA_DESI} +/- {WA_ERR})")
    print(f"  chi2      = {b['chi2']:.3f}  ({math.sqrt(b['chi2']):.1f} sigma)")
    print(f"  xi_today  = {b['xi_today']:.6f} (vacuum = {xi0_vac:.6f})")

    print(f"\n  w(z) profile:")
    for z in sorted(b['w_z'].keys()):
        print(f"    w(z={z:.1f}) = {b['w_z'][z]:.4f}")

    dist_to_vac = abs(b['xi_today'] - xi0_vac)
    print(f"\n  Distance to vacuum: |xi_today - e^{{-1}}| = {dist_to_vac:.4f}")
    if dist_to_vac < 0.1:
        print(f"  --> Field is NEAR vacuum (freezing nearly complete)")
    elif b['xi_today'] > xi0_vac:
        print(f"  --> Field is ABOVE vacuum (still rolling down)")
    else:
        print(f"  --> Field is BELOW vacuum (overshooting)")

    print(f"\n--- Parameter Constraints ---")
    in_1sigma = [r for r in all_results if r['chi2'] < 2.30]
    in_2sigma = [r for r in all_results if r['chi2'] < 6.18]

    if in_1sigma:
        L4s = [r['Lambda4'] for r in in_1sigma]
        xis = [r['xi_init'] for r in in_1sigma]
        xds = [r['xi_dot'] for r in in_1sigma]
        print(f"  1-sigma region ({len(in_1sigma)} points):")
        print(f"    Lambda^4: [{min(L4s):.3f}, {max(L4s):.3f}]")
        print(f"    xi_init:  [{min(xis):.3f}, {max(xis):.3f}]")
        print(f"    xi_dot:   [{min(xds):.3f}, {max(xds):.3f}]")

# =====================================================================
# COMPARISON TABLE
# =====================================================================
print(f"\n{'='*70}")
print(f"MODEL COMPARISON")
print(f"{'='*70}")
chi2_lcdm = ((-1 - W0_DESI)/W0_ERR)**2 + ((0 - WA_DESI)/WA_ERR)**2

print(f"""
| Model           | w0     | wa     | chi2  | Notes                    |
|-----------------|--------|--------|-------|--------------------------|
| LCDM            | -1.000 |  0.000 |  {chi2_lcdm:.1f} | Fixed cosmological constant |
| xi best-fit     | {b['w0']:.3f} | {b['wa']:.3f} | {b['chi2']:.1f}   | Freezing quintessence    |
| DESI DR1        | -0.827 | -0.750 |  0.0  | Observational target     |
""")
