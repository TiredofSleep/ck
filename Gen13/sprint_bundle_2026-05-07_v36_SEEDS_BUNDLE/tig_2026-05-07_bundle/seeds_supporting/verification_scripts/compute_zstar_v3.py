"""
compute_zstar_v3.py — z* turnaround extraction from the desi_xi_optimize_v2 trajectory

Reconciles with desi_xi_optimize_v2.py by using EXACTLY the same:
  - convention (H^2 = rho_total in Omega-units; densities pre-divided by 3)
  - initial redshift (N_start = -4 corresponds to z_i ~= 54, NOT z_i = 20)
  - variable (xi_p = d xi / d N, evolved in e-folds)
  - kinetic backreaction (1 - 0.5 * xi_p^2 in implicit Friedmann)
  - sign-fixed EoM (xi_pp = -(3 + H'/H) xi_p - Lambda^4 (1 + log xi) / H^2)

Identifies z* by tracking w_xi(z) along the trajectory and finding the local
minimum (or zero-crossing of d xi / d N) on the inbound-to-vacuum leg.

This SUPERSEDES compute_zstar_v2.py, which started from z_i = 20 in cosmic
time and could not reproduce the documented best-fit w_0 = -0.79 because
the initial-value problem differs from the optimize script's IVP.

Brayden Sanders / 7Site LLC — 2026-05-07
"""

import math
import numpy as np

# ---------------------------------------------------------------
# Convention (same as desi_xi_optimize_v2.py): H^2 = rho_total
# in Omega-units, densities pre-divided by 3.
# ---------------------------------------------------------------
Omega_m0 = 0.315
Omega_r0 = 9.1e-5
Omega_xi0 = 1 - Omega_m0 - Omega_r0


def trajectory(Lambda4, xi_init, xi_dot_init, N_start=-4, N_end=0.5, N_steps=20000):
    """Evolve the (xi, xi_p, N) system using the same convention as
    desi_xi_optimize_v2.py.solve_xi_frw, but record the full trajectory.

    Returns numpy arrays (N, z, xi, xi_p, w_xi, H).
    """
    dN = (N_end - N_start) / N_steps
    xi = float(xi_init)
    xi_p = float(xi_dot_init)

    Ns = np.zeros(N_steps + 1)
    zs = np.zeros(N_steps + 1)
    xis = np.zeros(N_steps + 1)
    xi_ps = np.zeros(N_steps + 1)
    ws = np.zeros(N_steps + 1)
    Hs = np.zeros(N_steps + 1)

    for step in range(N_steps + 1):
        N = N_start + step * dN
        a = math.exp(N)
        z = 1.0 / a - 1 if a > 1e-9 else 1e9

        rho_m = Omega_m0 * a ** (-3)
        rho_r = Omega_r0 * a ** (-4)

        if xi < 1e-30:
            xi = 1e-30
        xi_log_xi = xi * math.log(xi)
        denom = 1 - 0.5 * xi_p ** 2
        if denom < 0.01:
            denom = 0.01
        H2 = (rho_m + rho_r + Lambda4 * xi_log_xi) / denom
        if H2 < 1e-30:
            H2 = 1e-30
        H = math.sqrt(H2)

        rho_xi = 0.5 * H2 * xi_p ** 2 + Lambda4 * xi_log_xi
        p_xi = 0.5 * H2 * xi_p ** 2 - Lambda4 * xi_log_xi
        w = p_xi / rho_xi if abs(rho_xi) > 1e-30 else -1.0
        w = max(-2.0, min(1.0, w))

        Ns[step] = N
        zs[step] = z
        xis[step] = xi
        xi_ps[step] = xi_p
        ws[step] = w
        Hs[step] = H

        if step == N_steps:
            break

        Hp_over_H = -1.5 * rho_m / H2 - 2.0 * rho_r / H2 - 0.5 * xi_p ** 2
        xi_pp = -(3 + Hp_over_H) * xi_p - Lambda4 * (1 + math.log(xi)) / H2

        xi += xi_p * dN
        xi_p += xi_pp * dN
        if xi < 1e-30:
            xi = 1e-30

    return Ns, zs, xis, xi_ps, ws, Hs


def find_zstar(zs, xi_ps, ws):
    """Identify the Type-F turnaround point z* on the rolling-branch trajectory.

    Definition: z* is the redshift where d xi / d N changes sign (the
    instantaneous frozen point) within the observable window 0 < z < 6.
    Equivalently, the redshift where w_xi reaches its local minimum on the
    inbound leg (post-thaw, pre-asymptotic-refreeze).

    Returns (z_star, w_at_z_star, xi_p_at_z_star).
    Returns (None, None, None) if no turnaround is found in the window.
    """
    mask = (zs >= 0) & (zs <= 6) & np.isfinite(ws) & np.isfinite(xi_ps)
    if not mask.any():
        return None, None, None

    z_in = zs[mask]
    xi_p_in = xi_ps[mask]
    w_in = ws[mask]

    # Method 1: zero-crossing of xi_p (sign change)
    sign_changes = np.where(np.diff(np.signbit(xi_p_in)))[0]
    if len(sign_changes) > 0:
        idx = sign_changes[0]
        # interpolate
        z1, z2 = z_in[idx], z_in[idx + 1]
        xp1, xp2 = xi_p_in[idx], xi_p_in[idx + 1]
        if abs(xp2 - xp1) > 1e-15:
            t = -xp1 / (xp2 - xp1)
            z_star = z1 + t * (z2 - z1)
        else:
            z_star = (z1 + z2) / 2
        w_at = (w_in[idx] + w_in[idx + 1]) / 2
        return z_star, w_at, 0.0

    # Method 2: local minimum of w_xi on the trajectory
    if len(w_in) > 4:
        idx_min = np.argmin(w_in[1:-1]) + 1  # exclude endpoints
        return z_in[idx_min], w_in[idx_min], xi_p_in[idx_min]

    return None, None, None


def reproduce_documented_fit(Lambda4=2.0, xi_init=2.05, xi_dot=0.005):
    """Reproduce the documented best-fit trajectory from the desi_xi_optimize_v2
    grid search. The default parameters are tunable; pass values consistent
    with the grid-search top-10 output.

    The documented best fit is approximately:
      Lambda4 ~ 2.0 (in Omega-units; 3 H_0^2 M_Pl^2)
      xi_init ~ 2.0 (at z ~ 54)
      xi_dot  ~ 0.0 (small outbound velocity)
    yielding w_0 = -0.793, w_a = -0.451, chi^2 = 1.52
    against the DESI 2024 (w_0, w_a) Gaussian.
    """
    Ns, zs, xis, xi_ps, ws, Hs = trajectory(Lambda4, xi_init, xi_dot)

    # Compute w(z) at standard redshifts
    print("=" * 72)
    print(f"Trajectory: Lambda4={Lambda4}, xi_init={xi_init}, xi_dot={xi_dot}")
    print(f"Initial redshift z_i = {zs[0]:.2f} (corresponds to N_start = {Ns[0]:.2f})")
    print("=" * 72)
    print(f"\n  z       N        Xi        Xi_p        w_xi      H")
    for tz in [54.0, 20.0, 10.0, 5.0, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.3, 0.1, 0.0]:
        idx = np.argmin(np.abs(zs - tz))
        print(f"  {tz:5.2f}   {Ns[idx]:+.3f}  {xis[idx]:.4f}   {xi_ps[idx]:+.4f}     "
              f"{ws[idx]:+.4f}    {Hs[idx]:.4f}")

    # z* extraction
    z_star, w_at_z_star, xi_p_at = find_zstar(zs, xi_ps, ws)
    print()
    if z_star is not None:
        print(f"  z*       = {z_star:.3f}")
        print(f"  w(z*)    = {w_at_z_star:+.5f}")
        print(f"  xi'(z*)  = {xi_p_at:+.5f}  (~0 at the Type-F turnaround)")
    else:
        print("  No z* turnaround found in 0 < z < 6.")

    # w(z) summary at z = 0
    idx0 = np.argmin(np.abs(zs - 0))
    print(f"\n  w_0 (at z=0)  = {ws[idx0]:+.4f}")
    print(f"  Xi(z=0)       = {xis[idx0]:.4f}")
    print(f"  Xi'(z=0)      = {xi_ps[idx0]:+.5f}")

    return {'Ns': Ns, 'zs': zs, 'xis': xis, 'xi_ps': xi_ps, 'ws': ws, 'Hs': Hs,
            'z_star': z_star, 'w_at_z_star': w_at_z_star}


if __name__ == "__main__":
    # Reproduce the documented best fit
    print("\n" + "#" * 72)
    print("# z* extraction from the desi_xi_optimize_v2 trajectory")
    print("# Convention: H^2 = rho_total (Omega-units); xi evolved in e-folds")
    print("#             N_start = -4 corresponds to z_i ~= 54")
    print("#" * 72 + "\n")
    result = reproduce_documented_fit(Lambda4=2.0, xi_init=2.05, xi_dot=0.005)

    # Sanity check: pi_i in cosmic time (for those who think in dot xi)
    # dot xi (z=z_i) = H(z=z_i) * xi_p(z=z_i)
    H_init = result['Hs'][0]
    pi_i_cosmic = H_init * result['xi_ps'][0]
    print(f"\n  For reference (cosmic-time IC):")
    print(f"    H(z={result['zs'][0]:.1f}) = {H_init:.4f}  (in H_0 units)")
    print(f"    pi_i = dot xi = H * xi_p = {pi_i_cosmic:+.4f}  (in H_0 units)")
    print(f"    The compute_zstar_v2.py 'pi_i = 0.429' uses z_i = 20 in cosmic")
    print(f"    time, which corresponds to a DIFFERENT initial value problem")
    print(f"    starting deeper in the matter era. That script is superseded.")
