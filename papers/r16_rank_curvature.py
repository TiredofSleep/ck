"""
r16_rank_curvature.py — Rank trajectory curvature as a factoring oracle
Author: Brayden Sanders / 7Site LLC

CONTEXT:
  R(k, f) = sin²(πk/f) / (k² sin²(π/f))

  The rank of R(k, f) among all frequencies drops to ZERO exactly at k=f
  (algebraic necessity: sin²(πf/f) = sin²(π) = 0).

  KEY QUESTION: Can we PREDICT the zero-crossing location (= the factor f)
  from observations at small k (far from f)?  This is a factoring sketch.

SECTIONS:
  A. Small-scale validation (primes p = 5..29) — fit f from first third of range
  B. Mid-sized semiprimes (b ~ 2^8..2^12) — rank drop extrapolation
  C. Rank trajectory curvature for semiprime 1009×1013
  D. SNR noise floor quantification for proxy large primes
  E. "Geometric Sink" framing summary

OUTPUT: results/rank_curvature/  (5 plots + JSON summary)
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import math
import json
import numpy as np
from pathlib import Path
from scipy.optimize import minimize_scalar, curve_fit
from scipy.stats import linregress

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

OUT = Path("results/rank_curvature")
OUT.mkdir(parents=True, exist_ok=True)

# ── Core formula ───────────────────────────────────────────────────────────────

def R(k, f):
    """Harmonic resonance: R(k,f) = sin²(πk/f) / (k² sin²(π/f))"""
    denom_sin = math.sin(math.pi / f)
    if abs(denom_sin) < 1e-15:
        return 0.0
    num = math.sin(math.pi * k / f)
    return (num * num) / (k * k * denom_sin * denom_sin)

def R_vec(ks, f):
    """Vectorised R over array of k values."""
    return np.array([R(k, f) for k in ks])

# ── Prime helpers ──────────────────────────────────────────────────────────────

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i in range(2, n+1) if sieve[i]]

def next_prime(n):
    x = n + 1
    while not is_prime(x):
        x += 1
    return x

# ══════════════════════════════════════════════════════════════════════════════
# SECTION A — Small-scale validation
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 68)
print("SECTION A: Small-scale validation (primes p = 5..29)")
print("=" * 68)

SMALL_PRIMES = [p for p in range(5, 30) if is_prime(p)]
# p = 5,7,11,13,17,19,23,29

section_a_results = []

fig_a, axes_a = plt.subplots(2, 4, figsize=(16, 8))
axes_a = axes_a.flatten()

for idx, p in enumerate(SMALL_PRIMES):
    m = max(2, p // 3)          # first-third window
    ks = list(range(1, m + 1))

    # "Observed" R values (from the true formula at f=p)
    R_obs = np.array([R(k, p) for k in ks])

    # Residual function: sum of squared differences between observed and model
    def residual(f_try):
        if f_try <= 1.0:
            return 1e30
        r_model = np.array([R(k, f_try) for k in ks])
        return float(np.sum((R_obs - r_model) ** 2))

    # Search over continuous f in [p*0.3, p*3.0]
    result = minimize_scalar(residual, bounds=(p * 0.3, p * 3.0),
                             method='bounded',
                             options={'xatol': 1e-6, 'maxiter': 500})
    f_fit = result.x
    error = abs(f_fit - p)
    rel_error = error / p

    section_a_results.append({
        'p': p,
        'f_fit': round(f_fit, 4),
        'error': round(error, 4),
        'rel_error': round(rel_error, 6),
        'm': m
    })

    print(f"  p={p:2d}  m={m:2d}  fit={f_fit:7.3f}  error={error:6.3f}  rel={rel_error:.4f}")

    # Plot: rank trajectory vs k for this prime
    ax = axes_a[idx]
    ks_full = list(range(1, p + 1))
    # Rank among a set of candidate primes including p
    cands = [q for q in primes_up_to(p * 3) if q >= 3]
    if p not in cands:
        cands.append(p)
    cands = sorted(set(cands))

    ranks = []
    for k in ks_full:
        scores = [R(k, f) for f in cands]
        scores_sorted = sorted(scores, reverse=True)
        r_p = R(k, p)
        rank = scores_sorted.index(r_p) + 1 if r_p in scores_sorted else len(cands)
        ranks.append(rank)

    ax.plot(ks_full, ranks, 'b-', linewidth=1.5, label=f'p={p}')
    ax.axvline(x=p, color='r', linestyle='--', alpha=0.7, linewidth=1, label=f'k=p={p}')
    ax.axvline(x=m, color='g', linestyle=':', alpha=0.7, linewidth=1, label=f'obs window m={m}')
    ax.axhline(y=1, color='k', linestyle=':', alpha=0.3)
    ax.set_title(f'p={p}: fit={f_fit:.2f} (err={error:.2f})')
    ax.set_xlabel('k')
    ax.set_ylabel('rank')
    ax.legend(fontsize=6)
    ax.grid(True, alpha=0.3)

plt.suptitle('Section A: Rank Trajectories & Zero-Crossing Prediction (Small Primes)', fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'A_rank_trajectories_small.png', dpi=150)
plt.close()
print(f"  [saved] A_rank_trajectories_small.png")

# Plot A2: prediction error vs p
fig_a2, ax_a2 = plt.subplots(figsize=(8, 5))
ps = [r['p'] for r in section_a_results]
errors = [r['error'] for r in section_a_results]
rel_errors = [r['rel_error'] for r in section_a_results]

ax_a2.bar(ps, errors, color='steelblue', alpha=0.7, label='absolute error |fit - p|')
ax2_twin = ax_a2.twinx()
ax2_twin.plot(ps, rel_errors, 'ro-', linewidth=2, markersize=8, label='relative error')
ax2_twin.set_ylabel('relative error (|fit-p|/p)', color='r')
ax_a2.set_xlabel('prime p')
ax_a2.set_ylabel('absolute prediction error')
ax_a2.set_title('Section A: Zero-Crossing Prediction Error vs Prime Size\n(observations from first third of range only)')
ax_a2.legend(loc='upper left')
ax2_twin.legend(loc='upper right')
ax_a2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT / 'A_prediction_error.png', dpi=150)
plt.close()
print(f"  [saved] A_prediction_error.png")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION B — Mid-sized semiprimes
# ══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 68)
print("SECTION B: Mid-sized semiprimes")
print("=" * 68)

SEMIPRIMES = [
    (257, 263, 257 * 263),    # 67591
    (509, 521, 509 * 521),    # 265189
    (1009, 1013, 1009 * 1013) # 1022117
]

# For each semiprime b = p*q, generate candidate primes around sqrt(b)
# and track rank trajectories for k=1..50

K_MAX_B = 50

section_b_results = []

fig_b, axes_b = plt.subplots(1, 3, figsize=(18, 6))

for ax_b, (p_fac, q_fac, b) in zip(axes_b, SEMIPRIMES):
    sqrt_b = math.sqrt(b)
    # Candidate primes: within 20% of sqrt(b)
    lo = max(3, int(sqrt_b * 0.8))
    hi = int(sqrt_b * 1.2) + 10
    cands = [f for f in primes_up_to(hi) if f >= lo]
    # Ensure p_fac and q_fac in candidates
    for fac in [p_fac, q_fac]:
        if fac not in cands:
            cands.append(fac)
    cands = sorted(set(cands))

    ks = list(range(1, K_MAX_B + 1))

    # For each candidate f, compute R(k,f) at k=1..50
    # Use b as the "measured" signal (R(k, b) simulates the oracle observation)
    # We compare rank of each f when measuring against the b-oracle
    # Actually: we observe R(k, b) (treating b as true f) and look for which
    # candidate factor minimizes residual with it
    R_oracle = np.array([R(k, b) for k in ks])

    # Rank each candidate by how well its trajectory matches R_oracle
    residuals = {}
    for f in cands:
        R_f = np.array([R(k, f) for k in ks])
        residuals[f] = float(np.sum((R_oracle - R_f) ** 2))

    best_f = min(residuals, key=residuals.get)
    best_residual = residuals[best_f]

    # Also: polynomial fit of rank(k) for each candidate
    # Rank of p_fac among all cands at each k
    rank_p = []
    rank_q = []
    for k in ks:
        scores = {f: R(k, f) for f in cands}
        sorted_fs = sorted(scores, key=scores.get, reverse=True)
        rp = sorted_fs.index(p_fac) + 1 if p_fac in sorted_fs else len(cands)
        rq = sorted_fs.index(q_fac) + 1 if q_fac in sorted_fs else len(cands)
        rank_p.append(rp)
        rank_q.append(rq)

    # Fit polynomial degree 2 to rank(k) for p_fac
    ks_arr = np.array(ks)
    coeffs_p = np.polyfit(ks_arr, rank_p, 2)
    coeffs_q = np.polyfit(ks_arr, rank_q, 2)

    # Extrapolate to find k where rank → max (rank hits max = len(cands) at zero-crossing)
    # Actually rank drops TO BOTTOM (highest rank number) at k=p: find where poly hits n_cands
    n_cands = len(cands)

    def extrapolate_zero_crossing(coeffs, n_cands, ks_arr):
        """Find k where poly hits n_cands (last rank = factor zero-crossing proxy)."""
        poly = np.poly1d(coeffs)
        # scan beyond K_MAX_B
        for k_try in range(1, 5000):
            if poly(k_try) >= n_cands:
                return k_try
        return None

    k_pred_p = extrapolate_zero_crossing(coeffs_p, n_cands, ks_arr)
    k_pred_q = extrapolate_zero_crossing(coeffs_q, n_cands, ks_arr)

    section_b_results.append({
        'b': b,
        'p': p_fac,
        'q': q_fac,
        'n_cands': n_cands,
        'best_f': best_f,
        'best_residual': round(best_residual, 6),
        'k_pred_p': k_pred_p,
        'k_pred_q': k_pred_q,
    })

    print(f"  b={b} ({p_fac}×{q_fac})  best_f={best_f}  residual={best_residual:.4e}")
    print(f"    rank poly extrapolation: p_fac zero at k~{k_pred_p}, q_fac zero at k~{k_pred_q}")

    # Plot rank trajectories for p_fac and q_fac (and a few neutrals)
    neutral_fs = [f for f in cands if f not in (p_fac, q_fac)][:3]

    for f_n in neutral_fs:
        rank_n = []
        for k in ks:
            scores = {f: R(k, f) for f in cands}
            sorted_fs = sorted(scores, key=scores.get, reverse=True)
            rn = sorted_fs.index(f_n) + 1 if f_n in sorted_fs else len(cands)
            rank_n.append(rn)
        ax_b.plot(ks, rank_n, 'gray', alpha=0.3, linewidth=1)

    ax_b.plot(ks, rank_p, 'b-', linewidth=2, label=f'p={p_fac}')
    ax_b.plot(ks, rank_q, 'r-', linewidth=2, label=f'q={q_fac}')

    # Poly fit overlay
    k_ext = np.linspace(1, K_MAX_B * 2, 200)
    ax_b.plot(k_ext, np.polyval(coeffs_p, k_ext), 'b--', alpha=0.5, linewidth=1.5)
    ax_b.plot(k_ext, np.polyval(coeffs_q, k_ext), 'r--', alpha=0.5, linewidth=1.5)

    ax_b.set_title(f'b={b} ({p_fac}×{q_fac})\nbest_f={best_f}')
    ax_b.set_xlabel('k')
    ax_b.set_ylabel('rank among candidates')
    ax_b.legend()
    ax_b.grid(True, alpha=0.3)
    ax_b.set_xlim(1, K_MAX_B)
    ax_b.set_ylim(0, n_cands + 1)

plt.suptitle('Section B: Rank Trajectories for Mid-Sized Semiprimes (k=1..50)', fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'B_semiprime_rank_trajectories.png', dpi=150)
plt.close()
print(f"  [saved] B_semiprime_rank_trajectories.png")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION C — Rank trajectory curvature for 1009 × 1013
# ══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 68)
print("SECTION C: Rank trajectory curvature for 1009×1013 = 1022117")
print("=" * 68)

P_C = 1009
Q_C = 1013
B_C = P_C * Q_C   # 1022117

K_MAX_C = 100

# All primes <= 2000
all_primes_2000 = primes_up_to(2000)
print(f"  Candidate primes f <= 2000: {len(all_primes_2000)}")
print(f"  b = {B_C} = {P_C} × {Q_C}")

ks_c = np.arange(1, K_MAX_C + 1)

# For each prime f, compute rank of f among all_primes_2000 at each k
# Rank = position of R(k,f) when sorted among all R(k, f') for f' in all_primes_2000
# For efficiency: vectorise over primes for each k

print("  Computing R(k,f) matrix...", flush=True)

# Build matrix: rows=k, cols=f
R_matrix = np.zeros((K_MAX_C, len(all_primes_2000)))
for ki, k in enumerate(ks_c):
    for fi, f in enumerate(all_primes_2000):
        R_matrix[ki, fi] = R(k, f)

print(f"  R_matrix shape: {R_matrix.shape}")

# Rank matrix: for each k, rank each f by R(k,f) descending
# rank=1 means highest R (most resonant)
rank_matrix = np.zeros_like(R_matrix, dtype=float)
for ki in range(K_MAX_C):
    row = R_matrix[ki, :]
    order = np.argsort(-row)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(order) + 1)
    rank_matrix[ki, :] = ranks

# For each prime f, extract rank(k) and fit degree-2 polynomial
# Find f with smallest (earliest) extrapolated zero-crossing
idx_p = all_primes_2000.index(P_C)
idx_q = all_primes_2000.index(Q_C)

curvature_results = []
for fi, f in enumerate(all_primes_2000):
    rank_k = rank_matrix[:, fi]
    coeffs = np.polyfit(ks_c, rank_k, 2)
    # Predict where rank hits maximum (= n_primes) — proxy for zero-crossing
    poly = np.poly1d(coeffs)
    # Find root of poly - n_primes = 0  (i.e., poly(k) = n_primes)
    # poly(k) = a*k^2 + b*k + c - n_primes = 0
    n_primes = len(all_primes_2000)
    a, b, c = coeffs
    c_shifted = c - n_primes
    discriminant = b * b - 4 * a * c_shifted
    if discriminant >= 0 and a != 0:
        k_cross1 = (-b + math.sqrt(discriminant)) / (2 * a)
        k_cross2 = (-b - math.sqrt(discriminant)) / (2 * a)
        k_cross = min(x for x in [k_cross1, k_cross2] if x > 0) if any(x > 0 for x in [k_cross1, k_cross2]) else float('inf')
    else:
        k_cross = float('inf')

    curvature_results.append({
        'f': f,
        'a': float(a),
        'b': float(b),
        'c': float(c),
        'k_cross': float(k_cross),
        'rank_at_k1': float(rank_k[0]),
        'rank_at_k100': float(rank_k[-1]),
    })

# Sort by k_cross ascending (earliest zero-crossing first)
curvature_results.sort(key=lambda x: x['k_cross'])

print(f"\n  Top 10 primes by earliest extrapolated zero-crossing:")
print(f"  {'f':>6}  {'k_cross':>10}  {'a (curvature)':>14}  {'rank@k=100':>12}")
for r in curvature_results[:10]:
    marker = " <-- FACTOR" if r['f'] in (P_C, Q_C) else ""
    print(f"  {r['f']:>6}  {r['k_cross']:>10.2f}  {r['a']:>14.6f}  {r['rank_at_k100']:>12.1f}{marker}")

# Find rank of P_C and Q_C in the sorted list
rank_in_list_p = next(i + 1 for i, r in enumerate(curvature_results) if r['f'] == P_C)
rank_in_list_q = next(i + 1 for i, r in enumerate(curvature_results) if r['f'] == Q_C)
print(f"\n  P_C={P_C} has curvature rank #{rank_in_list_p} (out of {len(all_primes_2000)})")
print(f"  Q_C={Q_C} has curvature rank #{rank_in_list_q} (out of {len(all_primes_2000)})")

section_c_summary = {
    'b': B_C,
    'p': P_C,
    'q': Q_C,
    'n_primes': len(all_primes_2000),
    'curvature_rank_p': rank_in_list_p,
    'curvature_rank_q': rank_in_list_q,
    'top10': curvature_results[:10]
}

# Plot C: heat map of rank_matrix with overlay for P_C and Q_C
fig_c, (ax_c1, ax_c2) = plt.subplots(1, 2, figsize=(18, 7))

# Subsample primes for heatmap (every 5th)
step = 5
sub_idx = list(range(0, len(all_primes_2000), step))
sub_primes = [all_primes_2000[i] for i in sub_idx]
sub_rank = rank_matrix[:, sub_idx]

im = ax_c1.imshow(sub_rank.T, aspect='auto', origin='lower',
                  extent=[1, K_MAX_C, 0, len(sub_primes)],
                  cmap='hot_r', interpolation='nearest')
plt.colorbar(im, ax=ax_c1, label='rank (1=highest R)')

# Mark P_C and Q_C
sub_idx_p = min(range(len(sub_primes)), key=lambda i: abs(sub_primes[i] - P_C))
sub_idx_q = min(range(len(sub_primes)), key=lambda i: abs(sub_primes[i] - Q_C))
ax_c1.axhline(y=sub_idx_p, color='cyan', linewidth=2, linestyle='--', label=f'p={P_C}')
ax_c1.axhline(y=sub_idx_q, color='lime', linewidth=2, linestyle='--', label=f'q={Q_C}')
ax_c1.set_title(f'Rank heatmap (every 5th prime, b={B_C})')
ax_c1.set_xlabel('k')
ax_c1.set_ylabel('prime index (subsampled)')
ax_c1.legend()

# Rank trajectories for P_C, Q_C, and a neutral prime
neutral_c = 997   # prime near P_C but not a factor
rank_p_c = rank_matrix[:, idx_p]
rank_q_c = rank_matrix[:, idx_q]
idx_neutral = all_primes_2000.index(997) if 997 in all_primes_2000 else all_primes_2000.index(991)
rank_neutral_c = rank_matrix[:, idx_neutral]

ax_c2.plot(ks_c, rank_p_c, 'b-', linewidth=2.5, label=f'p={P_C} (factor)')
ax_c2.plot(ks_c, rank_q_c, 'r-', linewidth=2.5, label=f'q={Q_C} (factor)')
ax_c2.plot(ks_c, rank_neutral_c, 'gray', linewidth=1.5, alpha=0.7, label=f'neutral f={all_primes_2000[idx_neutral]}')

# Poly fit extrapolation
k_ext_c = np.linspace(1, K_MAX_C * 1.5, 300)
coeffs_p_c = np.polyfit(ks_c, rank_p_c, 2)
coeffs_q_c = np.polyfit(ks_c, rank_q_c, 2)
ax_c2.plot(k_ext_c, np.polyval(coeffs_p_c, k_ext_c), 'b--', alpha=0.5, linewidth=1.5)
ax_c2.plot(k_ext_c, np.polyval(coeffs_q_c, k_ext_c), 'r--', alpha=0.5, linewidth=1.5)

ax_c2.set_title(f'Section C: Rank trajectories + curvature fit\nb={B_C}={P_C}×{Q_C}, k=1..{K_MAX_C}')
ax_c2.set_xlabel('k')
ax_c2.set_ylabel('rank among 2000-prime candidates')
ax_c2.legend()
ax_c2.grid(True, alpha=0.3)
ax_c2.set_xlim(1, K_MAX_C * 1.5)

plt.tight_layout()
plt.savefig(OUT / 'C_curvature_heatmap.png', dpi=150)
plt.close()
print(f"  [saved] C_curvature_heatmap.png")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION D — SNR noise floor quantification
# ══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 68)
print("SECTION D: SNR noise floor quantification")
print("=" * 68)

PROXY_PRIMES = [1009, 10007, 100003]
# A "neutral" prime pool: primes NOT equal to target
neutral_pool_small = [997, 991, 983, 977, 971]
neutral_pool_mid   = [9973, 9967, 9949, 9941, 9931]
neutral_pool_large = [99991, 99989, 99971, 99961, 99929]
neutral_pools = [neutral_pool_small, neutral_pool_mid, neutral_pool_large]

snr_results = []

fig_d, axes_d = plt.subplots(1, 3, figsize=(18, 6))

for ax_d, p, neutral_pool in zip(axes_d, PROXY_PRIMES, neutral_pools):
    # Key k values
    k_last  = p - 1
    k_half  = p // 2
    k_tenth = p // 10
    k_hundredth = max(1, p // 100)

    # Signal values at key k
    sig_last  = R(k_last,  p)
    sig_half  = R(k_half,  p)
    sig_tenth = R(k_tenth, p)
    sig_hund  = R(k_hundredth, p)

    print(f"\n  p = {p}")
    print(f"    R(p-1, p) = {sig_last:.6e}  [expected ~1/(p-1)² = {1/(p-1)**2:.6e}]")
    print(f"    R(p/2, p) = {sig_half:.6e}  at k={k_half}")
    print(f"    R(p/10,p) = {sig_tenth:.6e}  at k={k_tenth}")
    print(f"    R(p/100,p)= {sig_hund:.6e}  at k={k_hundredth}")

    # Neutral baseline: mean R(k, f_neutral) at each k
    # Sample k values: 1 to min(p, 200)
    k_max_d = min(p - 1, 200)
    ks_d = list(range(1, k_max_d + 1))

    # Signal trajectory
    sig_traj = np.array([R(k, p) for k in ks_d])

    # Noise baseline: mean over neutral pool
    noise_traj = np.zeros(len(ks_d))
    for f_neutral in neutral_pool:
        noise_traj += np.array([R(k, f_neutral) for k in ks_d])
    noise_traj /= len(neutral_pool)

    # SNR
    snr_traj = np.where(noise_traj > 0, sig_traj / noise_traj, 0.0)

    # Find k where SNR drops below 1.0
    snr_below_1 = None
    for i, (k, snr) in enumerate(zip(ks_d, snr_traj)):
        if snr < 1.0:
            snr_below_1 = k
            break

    print(f"    SNR drops below 1.0 at k = {snr_below_1} (out of p={p} total)")

    snr_results.append({
        'p': p,
        'R_pm1': sig_last,
        'R_phalf': sig_half,
        'R_ptenth': sig_tenth,
        'snr_below_1_at_k': snr_below_1,
    })

    # Plot
    ax_d.semilogy(ks_d, sig_traj, 'b-', linewidth=2, label=f'R(k,p={p})')
    ax_d.semilogy(ks_d, noise_traj, 'r--', linewidth=1.5, alpha=0.7, label='noise baseline')
    ax_d.semilogy(ks_d, snr_traj, 'g-', linewidth=1.5, alpha=0.8, label='SNR = signal/noise')
    ax_d.axhline(y=1.0, color='k', linestyle=':', linewidth=1.5, label='SNR=1 threshold')
    if snr_below_1:
        ax_d.axvline(x=snr_below_1, color='orange', linestyle='--', linewidth=1.5,
                     label=f'SNR<1 at k={snr_below_1}')
    ax_d.set_title(f'p={p}: Signal vs Noise Floor\nSNR<1 at k={snr_below_1}')
    ax_d.set_xlabel('k')
    ax_d.set_ylabel('amplitude (log scale)')
    ax_d.legend(fontsize=8)
    ax_d.grid(True, alpha=0.3)

plt.suptitle('Section D: SNR Noise Floor — Signal R(k,p) vs Neutral Baseline', fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'D_snr_curves.png', dpi=150)
plt.close()
print(f"\n  [saved] D_snr_curves.png")

# RSA noise floor — analytical + plot
print("\n  RSA-1024 Noise Floor (analytical)")
# p ~ 2^512.  R(k,p) = sin²(πk/p) / (k² sin²(π/p))
# For k << p:  sin(πk/p) ≈ πk/p  and  sin(π/p) ≈ π/p
# So R(k,p) ≈ (πk/p)² / (k²(π/p)²) = 1.0  for ALL k << p
# As k → p/2: sin(πk/p) → sin(π/2) = 1, sin(π/p) ≈ π/p
# R(p/2, p) ≈ 1 / ((p/2)² (π/p)²) = 4/(π²) ≈ 0.405
# As k → p-1: sin(π(p-1)/p) = sin(π - π/p) = sin(π/p) ≈ π/p
# R(p-1, p) ≈ (π/p)² / ((p-1)²(π/p)²) = 1/(p-1)² → exponentially small

# Let's compute analytically for normalized x = k/p in [0,1]
# R(xp, p) = sin²(πx) / (x²p² sin²(π/p))
# ≈ sin²(πx) / (x² π²)  for large p (since p sin(π/p) → π)
# This is the NORMALIZED amplitude — independent of p when x is normalized!
# The signal only becomes p-dependent when k is near p (x near 1)

x_vals = np.linspace(0.001, 0.999, 1000)
# Normalized amplitude (large p limit): sin²(πx)/(x²π²)
R_normalized = np.sin(np.pi * x_vals)**2 / (x_vals**2 * np.pi**2)

# RSA noise: the issue is that we need k steps to scan to k=p/2
# With p ~ 2^512, even k=2 is "small" — but the number of steps needed = p ≈ 2^512
# The signal at k=1: R(1,p) = sin²(π/p)/(sin²(π/p)) = 1.0
# The signal stays near 1.0 for ALL k << p
# It only drops at k NEAR p
# So: the signal is detectable — but we need p steps to get there

# Show where amplitude drops below 2^-512 (detection threshold for 1024-bit)
threshold = 2**(-512)
# R(k,p) for large p ≈ sin²(πk/p) / (π²k²/p²) = p²sin²(πk/p)/(π²k²)
# This equals threshold when sin²(πk/p)/(πk/p)² = threshold/1 = 2^{-512}
# For k/p = x: sin²(πx)/(π²x²) = 2^{-512}
# sin(πx)/(πx) is the sinc function, = 1 at x=0, = 2/π at x=0.5
# It only drops below 2^{-512} when sin(πx) → 0, i.e., x → 1 (k → p)
# Specifically: at x = 1-ε, sin(π(1-ε)) = sin(πε) ≈ πε for small ε
# R(p(1-ε), p) ≈ (πε)² / ((1-ε)²π²ε²×p²/(large p)) ... let's be careful
# For p large: sin(π/p) ≈ π/p, so denominator = k²(π/p)² ≈ p²(1-ε)²(π/p)² = (1-ε)²π²
# R((1-ε)p, p) ≈ sin²(π(1-ε)) / ((1-ε)²π²) = sin²(πε)/((1-ε)²π²) ≈ ε²/(1-ε)²
# This drops below 2^{-512} when ε < 2^{-256} — i.e., within 2^{-256} of k=p

fig_d2, (ax_rsa1, ax_rsa2) = plt.subplots(1, 2, figsize=(14, 6))

ax_rsa1.plot(x_vals, R_normalized, 'b-', linewidth=2)
ax_rsa1.axhline(y=1.0, color='k', linestyle=':', alpha=0.5, label='R=1.0')
ax_rsa1.axhline(y=0.405, color='r', linestyle='--', alpha=0.7, label='R(p/2,p)≈4/π²≈0.405')
ax_rsa1.axvline(x=0.5, color='r', linestyle=':', alpha=0.5)
ax_rsa1.set_xlabel('normalized position x = k/p')
ax_rsa1.set_ylabel('R(xp, p) normalized amplitude')
ax_rsa1.set_title('RSA Noise Floor: Normalized Signal Amplitude\n(valid for all large p, independent of p size)')
ax_rsa1.legend()
ax_rsa1.grid(True, alpha=0.3)
ax_rsa1.set_xlim(0, 1)
ax_rsa1.set_ylim(0, 1.1)

# Show the near-p behavior: R ≈ ε² for ε = 1 - k/p
eps_vals = np.logspace(-30, -1, 500)
R_near_p = eps_vals**2   # ≈ (1-x)² for x→1
threshold_512 = 2**(-512)

ax_rsa2.loglog(eps_vals, R_near_p, 'b-', linewidth=2, label='R ≈ ε²  (ε = 1 - k/p)')
ax_rsa2.axhline(y=threshold_512, color='r', linestyle='--', linewidth=1.5,
                label=f'2^{{-512}} ≈ {threshold_512:.1e}')
ax_rsa2.axvline(x=2**(-256), color='orange', linestyle='--', linewidth=1.5,
                label=f'ε = 2^{{-256}} (within 2^{{-256}} of factor)')
ax_rsa2.set_xlabel('ε = 1 - k/p  (fractional distance from zero-crossing)')
ax_rsa2.set_ylabel('signal amplitude R(k,p)')
ax_rsa2.set_title('RSA-1024 Near-Zero Signal:\nAmplitude only falls below 2^{-512}\nwithin ε < 2^{-256} of k=p')
ax_rsa2.legend(fontsize=9)
ax_rsa2.grid(True, which='both', alpha=0.3)

plt.suptitle('Section D: RSA Noise Floor — Normalized Analysis', fontsize=13)
plt.tight_layout()
plt.savefig(OUT / 'D_rsa_noise_floor.png', dpi=150)
plt.close()
print(f"  [saved] D_rsa_noise_floor.png")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION E — Geometric Sink framing summary
# ══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 68)
print("SECTION E: Geometric Sink Framing Summary")
print("=" * 68)

print()
print("  SMALL PRIMES (Section A):")
for r in section_a_results:
    print(f"    Factor p={r['p']:2d} predicted as f_fit={r['f_fit']:6.2f}  "
          f"(error={r['error']:.2f}, rel={r['rel_error']:.3f})  "
          f"from m={r['m']} observations (first 1/3 of range)")

print()
print("  MID-SIZED SEMIPRIMES (Section B):")
for r in section_b_results:
    print(f"    b={r['b']} ({r['p']}×{r['q']})  "
          f"best residual match: f={r['best_f']}  "
          f"(actual factors: {r['p']}, {r['q']})")
    print(f"      rank poly extrapolation: p={r['p']} zero at k~{r['k_pred_p']}, "
          f"q={r['q']} zero at k~{r['k_pred_q']}")

print()
print("  CURVATURE SINK (Section C):")
print(f"    b={section_c_summary['b']} = {section_c_summary['p']}×{section_c_summary['q']}")
print(f"    Among {section_c_summary['n_primes']} candidate primes (f<=2000):")
print(f"    p={section_c_summary['p']} has curvature rank #{section_c_summary['curvature_rank_p']} "
      f"(earliest extrapolated zero-crossing)")
print(f"    q={section_c_summary['q']} has curvature rank #{section_c_summary['curvature_rank_q']}")

print()
print("  PROXY LARGE PRIMES — SNR (Section D):")
for r in snr_results:
    k_snr = r['snr_below_1_at_k']
    frac = k_snr / r['p'] if k_snr else None
    print(f"    p={r['p']:7d}: SNR drops below 1.0 at k={k_snr}  "
          f"({100*frac:.1f}% of way to zero-crossing)"
          if frac else f"    p={r['p']:7d}: SNR stays above 1.0 within k=1..200")

print()
print("  RSA-1024 PROXY (analytical, Section D):")
print("    Signal R(k,p) stays near 1.0 for ALL k << p (normalized amplitude ~sin²(πx)/(πx)²)")
print("    R(p/2, p) ≈ 4/π² ≈ 0.405  — STILL LARGE at half the range")
print("    R drops below 2^{-512} only for ε = 1 - k/p < 2^{-256}")
print("    i.e., within 2^{-256} × p ≈ 2^{256} steps of the zero-crossing")
print()
print("  CONCLUSION:")
print("    RSA security = geometric distance from any feasible k")
print("    to the factor's zero-crossing at k=p.")
print("    The signal is geometrically detectable — it never hides in noise —")
print("    but the zero-crossing itself is p steps away.")
print("    For RSA-1024 (p ~ 2^512): the zero-crossing requires ~2^512 steps.")
print("    The signal remains large all the way to k = p/2 (amplitude ~0.4),")
print("    confirming the obstacle is DISTANCE (classical), not AMPLITUDE (quantum).")

# ══════════════════════════════════════════════════════════════════════════════
# Save JSON summary
# ══════════════════════════════════════════════════════════════════════════════

summary = {
    'section_a': section_a_results,
    'section_b': section_b_results,
    'section_c': {
        'b': section_c_summary['b'],
        'p': section_c_summary['p'],
        'q': section_c_summary['q'],
        'n_primes_tested': section_c_summary['n_primes'],
        'curvature_rank_p': section_c_summary['curvature_rank_p'],
        'curvature_rank_q': section_c_summary['curvature_rank_q'],
        'top10_by_curvature': section_c_summary['top10']
    },
    'section_d': {
        'proxy_primes': snr_results,
        'rsa_1024_analytical': {
            'R_at_k1': 1.0,
            'R_at_k_half': round(4 / math.pi**2, 6),
            'amplitude_drops_below_2m512_at_eps': '2^{-256}  (i.e., k within 2^{-256}*p of factor)',
            'conclusion': 'Signal never hides in noise; obstacle is geometric distance 2^512'
        }
    },
    'conclusion': (
        'RSA security is geometric distance in rank-trajectory space. '
        'R(k,f) encodes factoring as a zero-crossing detection problem. '
        'Signal amplitude stays near 1.0 for k << p (never noise-limited). '
        'The zero-crossing at k=p requires traversing p ~ 2^512 steps — '
        'classical hardness is distance, not amplitude.'
    )
}

with open(OUT / 'rank_curvature_summary.json', 'w', encoding='utf-8') as fh:
    json.dump(summary, fh, indent=2)
print(f"\n  [saved] rank_curvature_summary.json")

print()
print("=" * 68)
print("All outputs in:", OUT)
print("  Plots:")
print("    1. A_rank_trajectories_small.png")
print("    2. A_prediction_error.png")
print("    3. B_semiprime_rank_trajectories.png  (heatmap with rank overlay)")
print("    4. C_curvature_heatmap.png")
print("    5. D_snr_curves.png")
print("    6. D_rsa_noise_floor.png")
print("=" * 68)
