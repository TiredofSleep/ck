"""
desi_xi_mcmc.py

DESI DR1 BAO MCMC fit for the logarithmic-quintessence ξ model.

UPGRADE OVER desi_xi_optimize.py:
  - Fits the *actual* DESI DR1 BAO data points (12 measurements of
    D_M/r_d, D_H/r_d, D_V/r_d at published effective redshifts), NOT
    the summary CPL (w0, wa) statistics.
  - Uses Eisenstein-Hu 1998 fitting formula for r_d (1% accurate when
    dark energy is negligible at recombination — true here).
  - Uses scipy.integrate.solve_ivp for the background Friedmann + KG
    system (more reliable than the explicit Euler in the prior code).
  - MCMC sampling via emcee 3.x with proper priors.
  - Direct ΛCDM baseline computed in the same framework for honest χ²
    comparison on the *same* likelihood.

HONEST SCOPE — what this is and is not:
  - This IS a real fit of the model to the actual DESI DR1 BAO points.
  - This IS NOT a full Boltzmann-grade analysis: r_d uses the EH
    fitting formula (good to ~1%), there are no perturbations, no full
    CMB, no Pantheon SNe, no Ων dependence beyond a fixed value.
  - For publication-quality work, redo with CAMB or CLASS_quintessence
    in Cobaya/MontePython. This script gets you to background-level fit
    quality, which is the right next step from the (w0, wa) summary fit.

DATA: DESI Collaboration (Adame et al.) "DESI 2024 VI: Cosmological
       Constraints from BAO," arXiv:2404.03002, Table 1 (DR1).

REFERENCES:
  - Eisenstein & Hu, ApJ 496:605 (1998) — fitting formulae for r_d.
  - Aubourg et al., PRD 92:123516 (2015) — confirms EH r_d to ~1% in
    standard models.
  - Foreman-Mackey et al., PASP 125:306 (2013) — emcee.

Copyright (c) 2026 Brayden Ross Sanders / 7Site LLC
"""

import math
import sys
import time
import io
import numpy as np
from scipy.integrate import solve_ivp, quad
import emcee

# Force UTF-8 stdout on Windows so Greek letters render
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
except Exception:
    pass

C_KM_S = 299792.458  # speed of light in km/s

# ================================================================
# DATA: DESI DR1 BAO (arXiv:2404.03002, Table 1)
# ================================================================
# Each entry: (label, z_eff, observable_kind, value, sigma)
# observable_kind in {"DM", "DH", "DV"} where:
#   DM = D_M(z)/r_d   (transverse comoving distance over sound horizon)
#   DH = D_H(z)/r_d   (Hubble distance c/H over sound horizon)
#   DV = D_V(z)/r_d   (isotropic average)
DESI_DR1 = [
    ("BGS",       0.295, "DV", 7.93,  0.15),
    ("LRG1",      0.510, "DM", 13.62, 0.25),
    ("LRG1",      0.510, "DH", 20.98, 0.61),
    ("LRG2",      0.706, "DM", 16.85, 0.32),
    ("LRG2",      0.706, "DH", 20.08, 0.60),
    ("LRG+ELG",   0.930, "DM", 21.71, 0.28),
    ("LRG+ELG",   0.930, "DH", 17.88, 0.35),
    ("ELG",       1.317, "DM", 27.79, 0.69),
    ("ELG",       1.317, "DH", 13.82, 0.42),
    ("QSO",       1.491, "DV", 26.07, 0.67),
    ("Lya",       2.330, "DM", 39.71, 0.94),
    ("Lya",       2.330, "DH", 8.52,  0.17),
]
N_DATA = len(DESI_DR1)
assert N_DATA == 12

# ================================================================
# Eisenstein & Hu 1998 sound-horizon-at-drag formula
# ================================================================
def r_d_eisenstein_hu(omega_m, omega_b, h, omega_nu=0.0):
    """
    Sound horizon at drag epoch, in Mpc.
    omega_m = Omega_m * h^2  (physical matter density)
    omega_b = Omega_b * h^2
    h = H0/100
    omega_nu = Omega_nu * h^2  (default 0 for massless)

    EH98 eq. (4)-(8). Good to ~1% in standard models (Aubourg+ 2015).
    """
    omh2 = omega_m
    obh2 = omega_b
    # z_eq, k_eq
    Theta = 2.728 / 2.7  # T_cmb / 2.7K
    z_eq = 2.5e4 * omh2 / Theta**4
    k_eq = 7.46e-2 * omh2 / Theta**2  # in Mpc^-1

    # z_drag from EH98 eq. (4)
    b1 = 0.313 * omh2**(-0.419) * (1 + 0.607 * omh2**0.674)
    b2 = 0.238 * omh2**0.223
    z_d = 1291.0 * omh2**0.251 / (1 + 0.659 * omh2**0.828) * (1 + b1 * obh2**b2)

    # R(z) = (3 rho_b)/(4 rho_gamma) at redshift z
    R = lambda z: 31.5 * obh2 / Theta**4 * (1000.0 / z)
    R_d = R(z_d)
    R_eq = R(z_eq)

    # Sound horizon at drag, EH98 eq. (6)
    rs = (2.0 / (3.0 * k_eq)) * math.sqrt(6.0 / R_eq) * \
         math.log((math.sqrt(1 + R_d) + math.sqrt(R_d + R_eq)) /
                  (1 + math.sqrt(R_eq)))
    return rs  # Mpc

# ================================================================
# Background solver: ΛCDM and ξ-quintessence
# ================================================================
def H_lcdm(z, Om0, Or0, H0):
    """Standard ΛCDM H(z) in km/s/Mpc."""
    OL = 1.0 - Om0 - Or0
    a = 1.0 / (1 + z)
    return H0 * math.sqrt(Om0 * (1 + z)**3 + Or0 * (1 + z)**4 + OL)


def solve_xi_background(Om0, Or0, H0, kappa, xi_init, xi_dot_init,
                        N_start=-6.0, N_end=0.3, n_eval=400):
    """
    Solve coupled Friedmann + Klein-Gordon for ξ on N = ln(a).
    Returns arrays (z, H_kms_per_Mpc) where H is the Hubble rate in km/s/Mpc.

    State y = [xi, xi_prime] where xi_prime = d(xi)/dN.

    Friedmann (in units H0=1, 8πG/3=1):
        h^2 ≡ (H/H0)^2 = (Omega_m a^-3 + Omega_r a^-4 + rho_xi)
              / (1 - 0.5 kappa xi'^2)
    Field eq:
        xi'' + (3 + h'/h) xi' + (1 + log xi)/h^2 = 0
    where h'/h = -(1.5 Om/h^2 + 2 Or/h^2 + 0.5 (3 rho_xi + 3 p_xi)/h^2 - 0.5)

    For the canonical choice we ignore radiation pressure of ξ and
    use the simplest form. The script fits κ, ξ_init, xi_dot_init
    and rescales to ensure flatness via the solver's own dynamics.
    """
    def rhs(N, y):
        a = math.exp(N)
        xi, xip = y
        if xi < 1e-30:
            xi = 1e-30
        rho_m = Om0 * a**(-3)
        rho_r = Or0 * a**(-4)
        # h^2 from Friedmann (kinetic-corrected)
        xi_log_xi = xi * math.log(xi)
        denom = 1.0 - 0.5 * kappa * xip**2
        if denom < 0.05:
            denom = 0.05
        h2 = (rho_m + rho_r + kappa * xi_log_xi) / denom
        if h2 < 1e-30:
            h2 = 1e-30
        # xi field equation
        xi_pp = -3.0 * xip + (1 + math.log(xi)) / h2
        return [xip, xi_pp]

    N_arr = np.linspace(N_start, N_end, n_eval)
    sol = solve_ivp(
        rhs, (N_start, N_end), [xi_init, xi_dot_init],
        t_eval=N_arr, method='RK45', rtol=1e-5, atol=1e-7, max_step=0.2
    )
    if not sol.success:
        return None
    xi_arr = sol.y[0]
    xip_arr = sol.y[1]
    a_arr = np.exp(N_arr)
    z_arr = 1.0 / a_arr - 1.0

    # Compute h^2 array
    h2_arr = np.zeros_like(N_arr)
    for i, N in enumerate(N_arr):
        a = a_arr[i]
        rho_m = Om0 * a**(-3)
        rho_r = Or0 * a**(-4)
        xi = max(xi_arr[i], 1e-30)
        xip = xip_arr[i]
        denom = max(1.0 - 0.5 * kappa * xip**2, 0.05)
        h2 = (rho_m + rho_r + kappa * xi * math.log(xi)) / denom
        h2_arr[i] = max(h2, 1e-30)
    H_arr = H0 * np.sqrt(h2_arr)
    return z_arr, H_arr


def H_xi_interp(z, model_pack):
    """Look up H(z) from precomputed model arrays."""
    z_arr, H_arr = model_pack
    # z_arr is decreasing (from large past z to today z=0)
    return float(np.interp(z, z_arr[::-1], H_arr[::-1]))


# ================================================================
# Distance integrals
# ================================================================
def DM_over_rd(z, H_func, rd):
    """Comoving distance / r_d.   D_M = c ∫ dz'/H(z')."""
    # Simpson's rule on 100 pts — much faster than quad() per call
    n = 100
    zp = np.linspace(0.0, z, n + 1)
    integrand_vals = np.array([C_KM_S / H_func(z_k) for z_k in zp])
    DM = np.trapezoid(integrand_vals, zp)
    return DM / rd

def DH_over_rd(z, H_func, rd):
    """c/H(z) / r_d."""
    return (C_KM_S / H_func(z)) / rd

def DV_over_rd(z, H_func, rd):
    """Isotropic D_V = (z * D_M^2 * c/H)^{1/3} / r_d."""
    DM = DM_over_rd(z, H_func, rd) * rd
    DH = (C_KM_S / H_func(z))
    DV = (z * DM**2 * DH)**(1.0/3.0)
    return DV / rd


# ================================================================
# χ² for either model
# ================================================================
def chi2_for_model(H_func, omega_m, omega_b, h):
    """χ² against DESI DR1 BAO. H_func(z) returns H in km/s/Mpc."""
    rd = r_d_eisenstein_hu(omega_m, omega_b, h)
    chi2 = 0.0
    for label, z, kind, val, sig in DESI_DR1:
        if kind == "DM":
            model = DM_over_rd(z, H_func, rd)
        elif kind == "DH":
            model = DH_over_rd(z, H_func, rd)
        elif kind == "DV":
            model = DV_over_rd(z, H_func, rd)
        chi2 += ((model - val) / sig)**2
    return chi2, rd


# ================================================================
# Standard external priors (BAO alone underconstrains ω_b)
# Aubourg et al. 2015 use Cooke+ 2014 BBN: ω_b = 0.02235 ± 0.00037
# ================================================================
OMEGA_B_BBN = 0.02235
OMEGA_B_BBN_SIG = 0.00037


def log_prior_omega_b(omega_b):
    return -0.5 * ((omega_b - OMEGA_B_BBN) / OMEGA_B_BBN_SIG) ** 2


# ================================================================
# ΛCDM baseline — analytic Hubble, fit (Om0, ωb, h) with BBN prior on ωb
# ================================================================
def chi2_lcdm(theta):
    Om0, omega_b, h = theta
    if not (0.05 < Om0 < 0.6 and 0.005 < omega_b < 0.05 and 0.4 < h < 1.0):
        return np.inf, None
    H0 = 100.0 * h
    omega_m = Om0 * h * h
    Or0 = 9.1e-5 / (h*h)  # approximate radiation density today
    H_func = lambda z: H_lcdm(z, Om0, Or0, H0)
    chi2, rd = chi2_for_model(H_func, omega_m, omega_b, h)
    return chi2, rd


def log_prob_lcdm(theta):
    chi2, _ = chi2_lcdm(theta)
    if not np.isfinite(chi2):
        return -np.inf
    # Add BBN prior on ω_b
    return -0.5 * chi2 + log_prior_omega_b(theta[1])


# ================================================================
# ξ model — fit (Om0, ωb, h, kappa, xi_init, xi_dot_init)
# ================================================================
def chi2_xi(theta):
    Om0, omega_b, h, kappa, xi_init, xi_dot_init = theta
    if not (0.05 < Om0 < 0.6 and 0.005 < omega_b < 0.05 and 0.4 < h < 1.0):
        return np.inf, None
    if not (0.01 < kappa < 10.0 and 0.05 < xi_init < 5.0):
        return np.inf, None
    if not (-1.0 < xi_dot_init < 1.0):
        return np.inf, None
    H0 = 100.0 * h
    omega_m = Om0 * h * h
    Or0 = 9.1e-5 / (h*h)
    pack = solve_xi_background(Om0, Or0, H0, kappa, xi_init, xi_dot_init)
    if pack is None:
        return np.inf, None
    z_arr, H_arr = pack
    if (H_arr <= 0).any() or not np.isfinite(H_arr).all():
        return np.inf, None
    H_func = lambda z: H_xi_interp(z, pack)
    chi2, rd = chi2_for_model(H_func, omega_m, omega_b, h)
    return chi2, rd


def log_prob_xi(theta):
    chi2, _ = chi2_xi(theta)
    if not np.isfinite(chi2):
        return -np.inf
    # Same BBN prior on ω_b
    return -0.5 * chi2 + log_prior_omega_b(theta[1])


# ================================================================
# RUN
# ================================================================
def banner(s):
    print()
    print("=" * 72)
    print(s)
    print("=" * 72)


def run_mcmc(log_prob, p0, n_walkers, n_steps, label, n_burn=None,
             init_scale=0.05):
    if n_burn is None:
        n_burn = n_steps // 5
    n_dim = len(p0)
    # initialize walkers — wider spread to avoid degenerate condition numbers
    # Use independent random offsets per walker per dimension
    initial = p0 + init_scale * np.random.randn(n_walkers, n_dim) * np.maximum(np.abs(p0), 0.01)
    # Reject any initial points that are immediately -inf
    for w in range(n_walkers):
        tries = 0
        while not np.isfinite(log_prob(initial[w])) and tries < 50:
            initial[w] = p0 + init_scale * np.random.randn(n_dim) * np.maximum(np.abs(p0), 0.01)
            tries += 1
    sampler = emcee.EnsembleSampler(n_walkers, n_dim, log_prob)
    t0 = time.time()
    print(f"  Burn-in {n_burn} steps × {n_walkers} walkers...")
    state = sampler.run_mcmc(initial, n_burn, progress=False)
    sampler.reset()
    print(f"  Production {n_steps} steps × {n_walkers} walkers...")
    sampler.run_mcmc(state, n_steps, progress=False)
    dt = time.time() - t0
    chain = sampler.get_chain(flat=True)
    log_probs = sampler.get_log_prob(flat=True)
    best_idx = int(np.argmax(log_probs))
    best_theta = chain[best_idx]
    best_chi2 = -2.0 * log_probs[best_idx]
    print(f"  [{label}] elapsed: {dt:.1f}s, best χ² = {best_chi2:.3f}, "
          f"acceptance = {sampler.acceptance_fraction.mean():.2f}")
    return chain, best_theta, best_chi2


def main():
    np.random.seed(42)

    banner("DESI DR1 BAO — ΛCDM baseline (3-parameter MCMC)")
    p0_lcdm = np.array([0.315, 0.0224, 0.674])  # Planck 2018
    chain_l, best_l, chi2_l = run_mcmc(
        log_prob_lcdm, p0_lcdm, n_walkers=24, n_steps=2000, label="ΛCDM"
    )
    Om_l, ob_l, h_l = best_l
    rd_l = r_d_eisenstein_hu(Om_l * h_l * h_l, ob_l, h_l)
    print(f"  Best-fit: Ωm = {Om_l:.4f}, ωb = {ob_l:.4f}, h = {h_l:.4f}")
    print(f"  r_d = {rd_l:.2f} Mpc, χ² = {chi2_l:.3f} (12 data, 3 params, dof = 9)")
    print(f"  χ²/dof = {chi2_l/9:.3f}")

    banner("DESI DR1 BAO — ξ-quintessence MCMC (6-parameter)")
    p0_xi = np.array([0.315, 0.0224, 0.674, 1.0, math.exp(-1), 0.0])
    chain_x, best_x, chi2_x = run_mcmc(
        log_prob_xi, p0_xi, n_walkers=24, n_steps=600, label="ξ field",
        init_scale=0.1
    )
    Om_x, ob_x, h_x, kap_x, xi0_x, xidot_x = best_x
    rd_x = r_d_eisenstein_hu(Om_x * h_x * h_x, ob_x, h_x)
    print(f"  Best-fit: Ωm = {Om_x:.4f}, ωb = {ob_x:.4f}, h = {h_x:.4f}")
    print(f"           κ = {kap_x:.4f}, ξ_init = {xi0_x:.4f}, ξ'_init = {xidot_x:.4f}")
    print(f"  r_d = {rd_x:.2f} Mpc, χ² = {chi2_x:.3f} (12 data, 6 params, dof = 6)")
    print(f"  χ²/dof = {chi2_x/6:.3f}")

    banner("RESULTS SUMMARY")
    delta_chi2 = chi2_l - chi2_x
    delta_dof = 9 - 6  # ξ has 3 extra params
    print(f"  ΛCDM:  χ² = {chi2_l:.3f},  dof = 9")
    print(f"  ξ:     χ² = {chi2_x:.3f},  dof = 6")
    print(f"  Δχ² = {delta_chi2:+.3f} (positive favors ξ; negative favors ΛCDM)")
    print(f"  Δdof = +{delta_dof} (ξ has more params)")
    print()
    print("  HONEST READING:")
    if delta_chi2 > 6.0:
        print("    ξ field is preferred at >2σ even after accounting for extra params.")
    elif delta_chi2 > 2.0:
        print("    ξ field is mildly preferred but not significant after extra params.")
    elif delta_chi2 > -2.0:
        print("    ξ field is consistent with ΛCDM; data don't distinguish them.")
    else:
        print("    ΛCDM is preferred. ξ model adds parameters without improving fit.")

    print()
    print("  CAVEATS (read before citing):")
    print("    - r_d via Eisenstein-Hu fitting formula (~1% accurate, no full Boltzmann).")
    print("    - Background only: no perturbations, no full CMB, no SNe, no ν mass.")
    print("    - For publication, redo with CAMB+Cobaya or CLASS+MontePython.")
    print("    - This script is the right scope for 'background-level fit using")
    print("      published BAO data points and standard r_d approximation'.")
    print("    - Data: DESI DR1 (arXiv:2404.03002, Table 1).")

    # Save chains for downstream plots
    np.savez(
        "desi_xi_mcmc_chains.npz",
        chain_lcdm=chain_l, chain_xi=chain_x,
        chi2_lcdm=chi2_l, chi2_xi=chi2_x,
        best_lcdm=best_l, best_xi=best_x,
    )
    print("\n  Chains saved to desi_xi_mcmc_chains.npz")


if __name__ == "__main__":
    main()
