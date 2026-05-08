"""
Retry with pi_i = 0.429 directly (in H_0 units), not multiplied by H_i.
"""
import numpy as np
from scipy.integrate import solve_ivp

Omega_m = 0.315
Omega_r = 9.1e-5
Lambda4_over_rhoc0 = 0.231
Lambda4 = Lambda4_over_rhoc0 * 3.0

z_i = 20.0
N_i = -np.log(1 + z_i)


def system_t(t, y):
    Xi, pi_, ln_a = y
    a = np.exp(ln_a)
    rho_m = 3 * Omega_m / a**3
    rho_r = 3 * Omega_r / a**4
    if Xi <= 0:
        Xi = 1e-12
    rho_Xi_K = 0.5 * pi_**2
    rho_Xi_V = Lambda4 * Xi * np.log(Xi)
    rho_total = rho_m + rho_r + rho_Xi_K + rho_Xi_V
    if rho_total < 1e-15:
        rho_total = 1e-15
    H = np.sqrt(rho_total / 3.0)
    dXi_dt = pi_
    dpi_dt = -3 * H * pi_ - Lambda4 * (1 + np.log(Xi))
    dln_a_dt = H
    return [dXi_dt, dpi_dt, dln_a_dt]


def integrate_and_analyze(Xi_i, pi_i, z_i=20.0, t_max=80.0, n=8000):
    N_i = -np.log(1 + z_i)
    y0 = [Xi_i, pi_i, N_i]
    sol = solve_ivp(system_t, [0, t_max], y0, dense_output=True,
                    rtol=1e-10, atol=1e-12, max_step=0.05)
    t_s = np.linspace(0, sol.t[-1], n)
    Y = sol.sol(t_s)
    Xi_a, pi_a, ln_a_a = Y[0], Y[1], Y[2]
    z_a = np.exp(-ln_a_a) - 1
    w_a = np.empty_like(t_s)
    for i in range(n):
        Xi = Xi_a[i]
        pi_ = pi_a[i]
        if Xi <= 0:
            w_a[i] = np.nan; continue
        K = 0.5 * pi_**2
        V = Lambda4 * Xi * np.log(Xi)
        rho = K + V
        w_a[i] = (K - V) / rho if abs(rho) > 1e-15 else -1.0
    return t_s, Xi_a, pi_a, z_a, w_a


# Try pi_i = 0.429 in H_0 units (my second interpretation)
print("="*72)
print("INTERPRETATION 2: pi_i = 0.429 H_0 (i.e., Xi-dot in H_0 units)")
print("="*72)
t_s, Xi_a, pi_a, z_a, w_a = integrate_and_analyze(Xi_i=0.925, pi_i=0.429)

print("\nTrajectory snapshots:")
for tz in [20, 5, 3, 2.5, 2, 1.5, 1, 0.8, 0.5, 0.3, 0]:
    idx = np.argmin(np.abs(z_a - tz))
    print(f"  z={tz:6.2f}   Xi={Xi_a[idx]:.4f}   pi={pi_a[idx]:+.4f}   w={w_a[idx]:+.4f}")

# Find min w in 0<z<6
mask = (z_a >= 0) & (z_a <= 6) & ~np.isnan(w_a)
if mask.any():
    z_in = z_a[mask]; w_in = w_a[mask]
    idx_min = np.argmin(w_in)
    z_star = z_in[idx_min]; w_star = w_in[idx_min]
    print(f"\n  *** z* = {z_star:.3f}   w_min = {w_star:.5f}")

# Cross-check: paper claims w_0 = -0.79, Xi(z=0) ≈ 0.97
idx_z0 = np.argmin(np.abs(z_a - 0))
print(f"\n  At z=0: Xi = {Xi_a[idx_z0]:.4f}  (paper: 0.97)")
print(f"  At z=0: w = {w_a[idx_z0]:+.4f}  (paper: -0.79)")

# If still off, try smaller pi_i
print("\n" + "="*72)
print("Scanning over pi_i to match paper's w_0 = -0.79")
print("="*72)
best_pi = None; best_diff = 1e9
for pi_test in np.linspace(0.05, 1.0, 20):
    try:
        _, Xi_b, pi_b, z_b, w_b = integrate_and_analyze(Xi_i=0.925, pi_i=pi_test)
        idx = np.argmin(np.abs(z_b - 0))
        w_at_0 = w_b[idx]
        diff = abs(w_at_0 - (-0.79))
        if diff < best_diff:
            best_diff = diff; best_pi = pi_test
        print(f"  pi_i = {pi_test:5.3f}  w_0 = {w_at_0:+.4f}  Xi_0 = {Xi_b[idx]:.4f}")
    except Exception as e:
        print(f"  pi_i = {pi_test:5.3f}  ERROR")

print(f"\n  Best match: pi_i = {best_pi:.4f}")

# Detailed integration at best pi_i
print("\n" + "="*72)
print(f"Detailed trajectory at best-match pi_i = {best_pi:.4f}")
print("="*72)
t_s, Xi_a, pi_a, z_a, w_a = integrate_and_analyze(Xi_i=0.925, pi_i=best_pi)
print(f"\n  z       Xi        pi        w")
for tz in [20, 10, 5, 4, 3, 2.5, 2, 1.5, 1, 0.8, 0.5, 0.3, 0.1, 0]:
    idx = np.argmin(np.abs(z_a - tz))
    print(f"  {tz:5.2f}   {Xi_a[idx]:.4f}   {pi_a[idx]:+.4f}   {w_a[idx]:+.4f}")

mask = (z_a >= 0) & (z_a <= 6) & ~np.isnan(w_a)
if mask.any():
    z_in = z_a[mask]; w_in = w_a[mask]
    idx_min = np.argmin(w_in)
    z_star = z_in[idx_min]; w_star = w_in[idx_min]
    print(f"\n  *** z* = {z_star:.3f}   w_min = {w_star:.5f}")

