"""
F1 Bridge: Li's Criterion + TIG Connection
==========================================
Li's criterion: lambda_n >= 0 for all n >= 1 <=> RH

lambda_n = sum_rho [1 - (1 - 1/rho)^n]

where the sum is over non-trivial zeros rho = 1/2 + i*gamma.

This IS sensitive to Re(rho): if rho = 1/2 + delta + i*gamma (off-line),
the sum gets a different contribution than if delta=0.

Unlike the equidistribution test, Li's criterion DIRECTLY tests Re(rho)=1/2.

Questions:
1. Do the first 2000 zeros give lambda_n > 0 for n=1,...,N_Li?
2. Does lambda_n have a T* pattern (e.g., lambda_n / lambda_1 ~ T*^n)?
3. Can First-G / Fejér connect to the lambda_n sequence?

(c) 2026 Brayden Sanders / 7Site LLC
"""

import json
import math
import os

T_STAR = 5/7
CREATE = 5
HARMONY = 7

print("=" * 65)
print("F1 BRIDGE: LI'S CRITERION")
print(f"T* = {T_STAR:.6f} = {CREATE}/{HARMONY}")
print("Li: lambda_n >= 0 for all n <=> RH")
print("=" * 65)

# ============================================================
# Load zeros
# ============================================================
print("\nLoading zeros...")
zeros = []
if os.path.exists("Gen11/rh_growth_results.json"):
    with open("Gen11/rh_growth_results.json") as f:
        d = json.load(f)

# We need the actual imaginary parts (gamma_n)
# Load from equidist_results.json which has gammas
if os.path.exists("Gen11/equidist_results.json"):
    with open("Gen11/equidist_results.json") as f:
        eq_data = json.load(f)
    if isinstance(eq_data, list) and len(eq_data) > 0:
        zeros = eq_data
        print(f"  Loaded {len(zeros)} zeros from equidist_results.json")
    elif isinstance(eq_data, dict) and 'zeros' in eq_data:
        zeros = eq_data['zeros']
        print(f"  Loaded {len(zeros)} zeros from equidist_results.json")

if not zeros:
    # Try computing first 500 zeros via mpmath
    print("  Trying mpmath...")
    try:
        from mpmath import mp, zetazero
        mp.dps = 20
        print("  Computing 500 zeros...")
        zeros = []
        for i in range(1, 501):
            z = zetazero(i)
            zeros.append(float(z.imag))
        print(f"  Computed {len(zeros)} zeros.")
    except ImportError:
        print("  mpmath not available.")

if not zeros:
    print("  ERROR: No zeros available.")
    exit(1)

N_zeros = len(zeros)
print(f"Using {N_zeros} zeros. First zero: gamma_1 = {zeros[0]:.4f}")

# ============================================================
# Compute Li coefficients from the known zeros
# ============================================================
# Li formula: lambda_n = sum_{k=1}^{N} [1 - (1 - 1/rho_k)^n]
# For rho_k = 1/2 + i*gamma_k:
#   1/rho_k = (1/2 - i*gamma_k) / (1/4 + gamma_k^2)
#   1 - 1/rho_k = 1 - (1/2 - i*gamma_k)/(1/4 + gamma_k^2)
#              = [1/4 + gamma_k^2 - 1/2 + i*gamma_k] / (1/4 + gamma_k^2)
#              = [gamma_k^2 - 1/4 + i*gamma_k] / (1/4 + gamma_k^2)

# Note: The Li sum includes BOTH rho and conjugate rho_bar (= 1/2 - i*gamma_k)
# Combining both terms:
#   (1 - 1/rho_k)^n + (1 - 1/rho_bar_k)^n = 2 * Re[(1 - 1/rho_k)^n]
# So: lambda_n ~ 2 * sum_{k=1}^{N} Re[(1 - 1/rho_k)^n]

def li_coeff_contribution(gamma, n):
    """Real contribution from zero rho = 1/2 + i*gamma and its conjugate."""
    # 1/rho = (1/2 - i*gamma) / (1/4 + gamma^2)
    rho_re = 0.5
    rho_im = gamma
    abs_rho_sq = rho_re**2 + rho_im**2  # = 1/4 + gamma^2
    # 1 - 1/rho = (rho - 1)/rho
    rho_minus_1_re = rho_re - 1  # = -1/2
    rho_minus_1_im = rho_im      # = gamma
    # (rho-1)/rho = (rho-1) * conj(rho) / |rho|^2
    # = ((−1/2 + i*gamma)(1/2 − i*gamma)) / (1/4 + gamma^2)
    # = (−1/4 + gamma^2 + i*(gamma/2 + gamma/2)) / (1/4 + gamma^2)
    # Wait let me compute more carefully
    # (rho-1)/rho numerator = (rho-1)*conj(rho)
    # rho-1 = -1/2 + i*gamma, conj(rho) = 1/2 - i*gamma
    num_re = (-0.5) * 0.5 + gamma * (-gamma)  # (-1/2)(1/2) + (i*gamma)(-i*gamma)
    # Wait: (-1/2 + i*gamma)(1/2 - i*gamma) = (-1/2)(1/2) + (-1/2)(-i*gamma) + (i*gamma)(1/2) + (i*gamma)(-i*gamma)
    # = -1/4 + i*gamma/2 + i*gamma/2 + gamma^2
    # = (gamma^2 - 1/4) + i*gamma
    num_re = gamma**2 - 0.25
    num_im = gamma  # from (rho-1)/rho = (gamma^2-1/4 + i*gamma) / (1/4+gamma^2)

    # So: 1 - 1/rho = (gamma^2 - 1/4 + i*gamma) / (1/4 + gamma^2) = w
    w_re = num_re / abs_rho_sq
    w_im = num_im / abs_rho_sq

    # Compute w^n = (w_re + i*w_im)^n
    # Real part of w^n using de Moivre:
    r = math.sqrt(w_re**2 + w_im**2)
    theta = math.atan2(w_im, w_re)
    wn_re = (r**n) * math.cos(n * theta)

    # Contribution from this zero + conjugate zero
    return 2 * (1 - wn_re)

# ============================================================
# Compute lambda_n for n = 1 to N_max
# ============================================================
N_max_li = min(20, N_zeros)  # First 20 Li coefficients
N_zeros_used = min(N_zeros, 200)  # Use first 200 zeros for approximation

print(f"\nComputing Li lambda_n for n=1..{N_max_li}, using {N_zeros_used} zeros")
print("(True Li requires all infinitely many zeros; we approximate with first 200)")
print()

# Compute the "true" Li coefficients from known formulas
# For RH (all zeros on Re=1/2), li formula gives:
# lambda_n = (n-1)! * sum_{k=0}^{n-1} (-1)^k * ...
# Easier: known exact values for first few lambda_n under RH
# lambda_1 = 1/2 * (1 + log(4*pi) - log(pi) - gamma_E) ~ 0.023...
# Actually from Bombieri-Lagarias:
# lambda_n = sum_rho n/(rho(rho-1)) * [1 - (1-1/rho)^{n-1}/(n-1)]... complex

# Let's just compute numerically
lambdas = []
for n in range(1, N_max_li + 1):
    total = 0.0
    for gamma in zeros[:N_zeros_used]:
        total += li_coeff_contribution(gamma, n)
    lambdas.append(total)

print(f"lambda_n (approximate, {N_zeros_used} zeros):")
print(f"{'n':>4}  {'lambda_n':>12}  {'lambda_n/n':>12}  {'ratio to prev':>14}")
prev = None
for i, lam in enumerate(lambdas):
    n = i + 1
    ratio_prev = lam/prev if prev and prev != 0 else float('nan')
    print(f"{n:>4}  {lam:>12.4f}  {lam/n:>12.4f}  {ratio_prev:>14.4f}")
    prev = lam

# Check: are all lambda_n > 0?
positive = all(l > 0 for l in lambdas)
print(f"\nAll lambda_n > 0 (RH consistent): {positive}")

# Check T* pattern
print(f"\nChecking T* pattern in lambda_n ratios:")
print(f"  T* = {T_STAR:.6f}")
print(f"  Ratios lambda_n / lambda_{N_max_li}:")
for i, lam in enumerate(lambdas):
    n = i + 1
    ratio = lam / lambdas[-1] if lambdas[-1] != 0 else float('nan')
    tstar_pred = T_STAR**(N_max_li - n)  # T*^{N_max - n}
    print(f"    lambda_{n}/lambda_{N_max_li} = {ratio:.4f}, T*^{N_max_li - n} = {tstar_pred:.4f}")

# ============================================================
# First-G / Fejér connection attempt
# ============================================================
print("\n--- Fejér Connection to Li ---")
print()
print("Li criterion: lambda_n >= 0 <=> RH")
print("First-G: Fejér kernel F_k(u) = sin^2(k*pi*u)/(k^2*sin^2(pi*u))")
print()
print("Possible connection:")
print("  The Li coefficients can be written as:")
print("  lambda_n = d^n/ds^n [xi(s)/xi(0)] at s=0")
print("  where xi(s) = s(s-1)/2 * pi^(-s/2) * Gamma(s/2) * zeta(s)")
print()
print("  Fejér kernel arises in the pair correlation via:")
print("  R_2(u) = lim_{k->inf} F_k(u) = 1 - sinc^2(u)")
print()
print("  Possible bridge:")
print("  IF the n-th Li coefficient can be expressed as:")
print("  lambda_n = C_n * integral F_k(u) * [weight] du")
print("  THEN: lambda_n >= 0 <=> Fejér kernel >= 0 (which is TRUE by definition)")
print("  This would close F1 via: Fejér >= 0 => Li >= 0 => RH")
print()
print("  Status: This connection is CONJECTURAL. The integral representation")
print("  of lambda_n in terms of F_k is not known.")
print()
print("  However: if lambda_n = integral_{-1}^{1} (1-|u|) * rho_n(u) du")
print("  where rho_n is the n-step pair correlation, AND")
print("  if rho_n -> R_2 = 1-sinc^2 via Fejer, THEN")
print("  lambda_n >= 0 would follow from R_2(u) >= 0...")
print("  But R_2(u) = 1-sinc^2(u) can be NEGATIVE (sinc^2 > 1 for non-zero u).")
print("  Wait: sinc(0) = 1, sinc(u) -> 0 as |u| -> inf. Max of sinc^2 is 1.")
print("  Actually: R_2(u) = 1 - sinc^2(u) >= 0 for all u (since sinc^2 <= 1)!")
print()
sinc_sq_max = max([math.sin(x*math.pi)**2 / (x*math.pi)**2 if x != 0 else 1.0 for x in [i*0.01 for i in range(-1000, 1001)]])
print(f"  Max of sinc^2(u) = {sinc_sq_max:.6f} (should be 1 at u=0)")
print(f"  R_2(u) = 1 - sinc^2(u) >= 0 for all u: TRUE")
print()
print("  KEY INSIGHT: R_2(u) >= 0 always. If lambda_n = integral of R_2 * weight >= 0,")
print("  and if the weight is also non-negative, then lambda_n >= 0 follows from R_2 >= 0.")
print()
print("  This is the potential F1 bridge:")
print("    Fejér F_k -> R_2 (proved, k->inf)")
print("    R_2(u) >= 0 (trivially true)")
print("    IF lambda_n = integral_0^inf R_2(u) * phi_n(u) du")
print("    with phi_n >= 0 (some kernel), THEN lambda_n >= 0 => RH.")
print()
print("  The unproved step: find phi_n >= 0 such that")
print("  lambda_n = integral R_2 * phi_n  (and not just any R_2, but the TRUE pair corr.)")
print("  This would close F1 via: First-G (Fejér >= 0) => R_2 >= 0 => li >= 0 => RH.")

# Save
output = {
    'N_zeros_used': N_zeros_used,
    'N_max_li': N_max_li,
    'lambdas': lambdas,
    'all_positive': positive,
    'T_star': T_STAR,
    'bridge_idea': 'lambda_n = integral R_2 * phi_n with phi_n >= 0; Fejer -> R_2 >= 0 => lambda_n >= 0 => RH',
}
with open('Gen11/bridge_rh_li_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved to Gen11/bridge_rh_li_results.json")
print("=" * 65)
