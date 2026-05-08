"""
DESI PARAMETER OPTIMIZATION: Logarithmic Quintessence xi Model
SIGN-FIX DIAGNOSTIC VERSION (2026-05-05)

Original script (Sprint 15, 2026-04-10) had EoM sign error on line 70:
    OLD (WRONG): xi_pp = -(3 + Hp_over_H) * xi_p + (1 + log(xi)) / H2
    NEW (RIGHT): xi_pp = -(3 + Hp_over_H) * xi_p - (1 + log(xi)) / H2

In FRW with (-,+,+,+) signature: Box(xi) = -xi_ddot - 3H*xi_dot.
EoM is Box(xi) = 1 + log(xi), so xi_ddot + 3H*xi_dot = -(1+log(xi)).
The minus sign on the (1+log(xi)) term is correct.

Also in this version: derivative `xi_p` is d_xi/dN (e-folding), so the
chain rule gives xi_ddot in cosmic time t as:
  xi_ddot = H^2 * xi_pp + H_dot * xi_p
The script does this implicitly via Hp_over_H.

This diagnostic version keeps the OLD action (single kappa on both
kinetic and potential terms). After validating the sign fix, a separate
script applies the dimensional rewrite (M_Pl^2 kinetic + Lambda^4
potential).

Copyright (c) 2026 Brayden Ross Sanders / 7Site LLC
"""

import numpy as np
import math
import sys

# =====================================================================
# COSMOLOGICAL PARAMETERS
# =====================================================================
Omega_m0 = 0.315
Omega_r0 = 9.1e-5
Omega_xi0 = 1 - Omega_m0 - Omega_r0
xi0_vac = math.exp(-1)

# DESI DR1 targets (NOT DR2 — original script's labels were wrong; these
# are the published DR1 values. DR2 release came later.)
W0_DESI = -0.827
W0_ERR = 0.063
WA_DESI = -0.75
WA_ERR = 0.27  # average of +0.29/-0.25

def solve_xi_frw(kappa, xi_init, xi_dot_init, N_start=-4, N_end=0.5, N_steps=5000):
    """Solve coupled xi + Friedmann. Returns w0, wa, xi_today, w_at_z dict.
    
    SIGN FIX applied to xi_pp on line marked below.
    """
    dN = (N_end - N_start) / N_steps
    xi = xi_init
    xi_p = xi_dot_init  # d_xi/dN (e-folding derivative)

    w_at_z = {}  # store w at key redshifts

    for step in range(N_steps):
        N = N_start + step * dN
        a = math.exp(N)

        rho_m = Omega_m0 * a**(-3)
        rho_r = Omega_r0 * a**(-4)

        if xi < 1e-30:
            xi = 1e-30

        xi_log_xi = xi * math.log(xi)
        denom = 1 - 0.5 * kappa * xi_p**2
        if denom < 0.01:
            denom = 0.01

        H2 = (rho_m + rho_r + kappa * xi_log_xi) / denom
        if H2 < 1e-30:
            H2 = 1e-30
        H = math.sqrt(H2)

        rho_xi = 0.5 * kappa * H2 * xi_p**2 + kappa * xi_log_xi
        p_xi = 0.5 * kappa * H2 * xi_p**2 - kappa * xi_log_xi

        w = p_xi / rho_xi if abs(rho_xi) > 1e-30 else -1.0
        w = max(-2.0, min(1.0, w))  # clamp

        z = 1.0/a - 1 if a > 0.01 else 100.0

        # Store w at key redshifts
        for z_target in [0.0, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0]:
            if abs(z - z_target) < 0.05 and z_target not in w_at_z:
                w_at_z[z_target] = w

        # Evolve
        Hp_over_H = -1.5 * rho_m / H2 - 2.0 * rho_r / H2
        # SIGN FIX: was `+ (1 + log(xi))/H2`, correct is `- (1 + log(xi))/H2`
        xi_pp = -(3 + Hp_over_H) * xi_p - (1 + math.log(xi)) / H2

        xi += xi_p * dN
        xi_p += xi_pp * dN
        if xi < 1e-30:
            xi = 1e-30

    # Extract w0 and wa
    w0 = w_at_z.get(0.0, -1.0)
    w05 = w_at_z.get(0.5, w0)
    a05 = 1.0 / 1.5
    wa = (w05 - w0) / (1 - a05) if abs(1 - a05) > 0.01 else 0

    return w0, wa, xi, w_at_z

# =====================================================================
# GRID SEARCH
# =====================================================================
print("=" * 70)
print("DESI PARAMETER OPTIMIZATION (SIGN-FIX DIAGNOSTIC)")
print(f"Target: w0 = {W0_DESI} +/- {W0_ERR}, wa = {WA_DESI} +/- {WA_ERR}")
print("=" * 70)

# Search grid (matches original script)
kappa_range = np.linspace(0.5, 5.0, 20)
xi_init_range = np.linspace(0.3, 3.0, 20)
xi_dot_range = np.linspace(-0.5, 0.5, 15)

best_chi2 = 1e10
best_params = None
all_results = []
total = len(kappa_range) * len(xi_init_range) * len(xi_dot_range)
count = 0

print(f"\nSearching {total} parameter combinations...")

for kappa in kappa_range:
    for xi_init in xi_init_range:
        for xi_dot in xi_dot_range:
            count += 1
            if count % 1000 == 0:
                print(f"  {count}/{total} searched, best chi2 = {best_chi2:.2f}", end='\r')

            try:
                w0, wa, xi_today, w_z = solve_xi_frw(kappa, xi_init, xi_dot)

                if abs(w0) > 2 or abs(wa) > 5:
                    continue

                chi2 = ((w0 - W0_DESI) / W0_ERR)**2 + ((wa - WA_DESI) / WA_ERR)**2

                all_results.append({
                    'kappa': kappa, 'xi_init': xi_init, 'xi_dot': xi_dot,
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
print(f"{'kappa':>8} {'xi_init':>8} {'xi_dot':>8} {'w0':>8} {'wa':>8} {'chi2':>8} {'xi_today':>10}")
print("-" * 70)
for r in all_results[:10]:
    print(f"{r['kappa']:>8.3f} {r['xi_init']:>8.3f} {r['xi_dot']:>8.3f} "
          f"{r['w0']:>8.4f} {r['wa']:>8.4f} {r['chi2']:>8.3f} {r['xi_today']:>10.4f}")

# =====================================================================
# BEST FIT ANALYSIS
# =====================================================================
if best_params:
    b = best_params
    print(f"\n{'='*70}")
    print(f"BEST FIT PARAMETERS (sign-fixed)")
    print(f"{'='*70}")
    print(f"  kappa_xi  = {b['kappa']:.4f}")
    print(f"  xi_init   = {b['xi_init']:.4f} (at z~{math.exp(-(-4))-1:.0f})")
    print(f"  xi_dot    = {b['xi_dot']:.4f}")
    print(f"  w0        = {b['w0']:.4f}  (DESI: {W0_DESI} +/- {W0_ERR})")
    print(f"  wa        = {b['wa']:.4f}  (DESI: {WA_DESI} +/- {WA_ERR})")
    print(f"  chi2      = {b['chi2']:.3f}  ({math.sqrt(b['chi2']):.1f} sigma)")
    print(f"  xi_today  = {b['xi_today']:.6f} (vacuum = {xi0_vac:.6f})")

    print(f"\n  w(z) profile:")
    for z in sorted(b['w_z'].keys()):
        print(f"    w(z={z:.1f}) = {b['w_z'][z]:.4f}")

    # Is xi_today near vacuum?
    dist_to_vac = abs(b['xi_today'] - xi0_vac)
    print(f"\n  Distance to vacuum: |xi_today - e^{{-1}}| = {dist_to_vac:.4f}")
    if dist_to_vac < 0.1:
        print(f"  --> Field is NEAR vacuum (freezing nearly complete)")
    elif b['xi_today'] > xi0_vac:
        print(f"  --> Field is ABOVE vacuum (still rolling down)")
    else:
        print(f"  --> Field is BELOW vacuum (overshooting)")

    # 1-sigma and 2-sigma regions
    print(f"\n--- Parameter Constraints ---")
    in_1sigma = [r for r in all_results if r['chi2'] < 2.30]
    in_2sigma = [r for r in all_results if r['chi2'] < 6.18]

    if in_1sigma:
        kappas = [r['kappa'] for r in in_1sigma]
        xis = [r['xi_init'] for r in in_1sigma]
        xds = [r['xi_dot'] for r in in_1sigma]
        print(f"  1-sigma region ({len(in_1sigma)} points):")
        print(f"    kappa:   [{min(kappas):.3f}, {max(kappas):.3f}]")
        print(f"    xi_init: [{min(xis):.3f}, {max(xis):.3f}]")
        print(f"    xi_dot:  [{min(xds):.3f}, {max(xds):.3f}]")

    if in_2sigma:
        kappas = [r['kappa'] for r in in_2sigma]
        xis = [r['xi_init'] for r in in_2sigma]
        xds = [r['xi_dot'] for r in in_2sigma]
        print(f"  2-sigma region ({len(in_2sigma)} points):")
        print(f"    kappa:   [{min(kappas):.3f}, {max(kappas):.3f}]")
        print(f"    xi_init: [{min(xis):.3f}, {max(xis):.3f}]")
        print(f"    xi_dot:  [{min(xds):.3f}, {max(xds):.3f}]")

# =====================================================================
# COMPARISON TABLE
# =====================================================================
print(f"\n{'='*70}")
print(f"MODEL COMPARISON")
print(f"{'='*70}")
chi2_lcdm = ((-1 - W0_DESI)/W0_ERR)**2 + ((0 - WA_DESI)/WA_ERR)**2
chi2_phantom = ((-1.1 - W0_DESI)/W0_ERR)**2 + ((-0.5 - WA_DESI)/WA_ERR)**2

print(f"""
| Model           | w0     | wa     | chi2  | Notes                    |
|-----------------|--------|--------|-------|--------------------------|
| LCDM            | -1.000 |  0.000 |  {chi2_lcdm:.1f} | Fixed cosmological constant |
| xi best-fit     | {b['w0']:.3f} | {b['wa']:.3f} | {b['chi2']:.1f}   | Freezing quintessence    |
| DESI DR1        | -0.827 | -0.750 |  0.0  | Observational target     |
| CPL phantom     | -1.100 | -0.500 |  {chi2_phantom:.1f} | Phantom crossing (ruled out by xi) |
""")

print("FALSIFIABILITY:")
print("  - xi model CANNOT produce w < -1 (no phantom crossing)")
print("  - If DESI/Euclid confirm phantom: xi model falsified")
print("  - If DESI/Euclid confirm freezing toward -1: xi model supported")
print("  - The xi model is DISTINGUISHABLE from LCDM by the w(z) trajectory")
