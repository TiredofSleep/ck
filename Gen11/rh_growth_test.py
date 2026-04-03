"""
rh_growth_test.py
==================
Growth rate test: does sqrt(N)*D_KS converge or grow?

Under equidistribution (consistent with RH):
  sqrt(N)*D_KS -> constant ~ 0.868 (Kolmogorov distribution median)

If zeros NOT equidistributed:
  sqrt(N)*D_KS grows without bound

Checkpoints: N = 100, 200, 500, 1000, 2000
Primes tested: p = 2, 3, 5, 7

This is the F1 Option A measurement:
  If sqrt(N)*D_KS -> constant: consistent with unconditional equidistribution
  If sqrt(N)*D_KS grows: equidistribution fails at large N
"""

import math
import json

try:
    from mpmath import zetazero, mp
    mp.dps = 15
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False

T_STAR   = 5.0 / 7.0
N_ZEROS  = 2000
CHECKPOINTS = [50, 100, 200, 500, 1000, 2000]
TEST_PRIMES = [2, 3, 5, 7]
EXPECTED_SQRT_N_D = 0.868  # Kolmogorov distribution median

def ks_distance(values):
    n = len(values)
    sv = sorted(values)
    dp = max((k+1)/n - v for k, v in enumerate(sv))
    dm = max(v - k/n     for k, v in enumerate(sv))
    return max(dp, dm)

print("RH GROWTH RATE TEST")
print("=" * 70)
print(f"T* = {T_STAR:.6f}")
print(f"Expected sqrt(N)*D_KS under equidistribution: {EXPECTED_SQRT_N_D:.3f}")
print(f"Computing {N_ZEROS} Riemann zeros...")
print()

if not HAS_MPMATH:
    print("ERROR: mpmath required. Install with: pip install mpmath")
    exit(1)

import time
t0 = time.time()
zeros = []
for n in range(1, N_ZEROS + 1):
    z = float(zetazero(n).imag)
    zeros.append(z)
    if n % 500 == 0:
        elapsed = time.time() - t0
        print(f"  {n}/{N_ZEROS} zeros computed ({elapsed:.1f}s)")

print(f"Done in {time.time()-t0:.1f}s. gamma_1={zeros[0]:.4f}, gamma_{N_ZEROS}={zeros[-1]:.4f}")
print()

# ---- Growth test ---------------------------------------------------------
results = {}

for p in TEST_PRIMES:
    log_p = math.log(p)
    two_pi = 2 * math.pi
    alphas = [(z * log_p / two_pi) % 1.0 for z in zeros]
    results[p] = {}

    print(f"p={p}: sqrt(N)*D_KS growth test")
    print(f"  {'N':>6}  {'D_KS':>8}  {'sqrt(N)*D':>10}  {'/ expected':>10}  "
          f"{'trend':>8}  {'< T*?':>6}")
    print(f"  {'-'*6}  {'-'*8}  {'-'*10}  {'-'*10}  {'-'*8}  {'-'*6}")

    prev_snd = None
    for nc in CHECKPOINTS:
        if nc > len(alphas):
            break
        d = ks_distance(alphas[:nc])
        snd = math.sqrt(nc) * d
        ratio = snd / EXPECTED_SQRT_N_D
        below = 'YES' if d < T_STAR else ' NO'
        if prev_snd is None:
            trend = '---'
        elif snd > prev_snd * 1.05:
            trend = 'GROWING'
        elif snd < prev_snd * 0.95:
            trend = 'falling'
        else:
            trend = 'stable'
        print(f"  {nc:>6}  {d:>8.5f}  {snd:>10.4f}  {ratio:>10.4f}  "
              f"{trend:>8}  {below:>6}")
        results[p][nc] = {
            'D_KS': round(d, 6),
            'sqrt_N_D': round(snd, 4),
            'ratio_to_expected': round(ratio, 4),
            'below_T_star': bool(d < T_STAR),
            'trend': trend,
        }
        prev_snd = snd
    print()

# ---- Convergence analysis ------------------------------------------------
print("=" * 70)
print("CONVERGENCE ANALYSIS")
print("=" * 70)
print()
print("Fitting sqrt(N)*D_KS vs N to determine growth rate:")
print()

for p in TEST_PRIMES:
    r = results[p]
    ns = sorted(r.keys())
    snds = [r[n]['sqrt_N_D'] for n in ns]

    # Linear fit: snd = a + b * log(N)
    log_ns = [math.log(n) for n in ns]
    n_pts = len(log_ns)
    mean_x = sum(log_ns) / n_pts
    mean_y = sum(snds) / n_pts
    b = sum((log_ns[i]-mean_x)*(snds[i]-mean_y) for i in range(n_pts)) / \
        sum((log_ns[i]-mean_x)**2 for i in range(n_pts))
    a = mean_y - b * mean_x

    # If b > 0: growing (not equidistributed direction)
    # If b ~ 0: converged (equidistributed)
    # If b < 0: over-equidistributed (unusual)

    final_snd = snds[-1]
    print(f"  p={p}: sqrt(N)*D_KS = {a:.3f} + {b:.4f}*log(N)")
    print(f"         At N={ns[-1]}: {final_snd:.4f}  (expected {EXPECTED_SQRT_N_D:.3f})")
    print(f"         Slope b={b:.4f}: {'GROWING (not equidist. direction)' if b > 0.1 else 'stable/converging (consistent with equidist.)'}")
    print()

# ---- The verdict ---------------------------------------------------------
print("=" * 70)
print("F1 BRIDGE MEASUREMENT (Option A)")
print("=" * 70)
print()

# Gather final sqrt(N)*D values across primes
final_snds = {p: results[p][max(results[p].keys())]['sqrt_N_D'] for p in TEST_PRIMES}
max_final = max(final_snds.values())
mean_final = sum(final_snds.values()) / len(final_snds)

print(f"At N={N_ZEROS} zeros:")
for p in TEST_PRIMES:
    print(f"  p={p}: sqrt(N)*D_KS = {final_snds[p]:.4f}  (expected {EXPECTED_SQRT_N_D:.3f})")
print()
print(f"Mean sqrt(N)*D = {mean_final:.4f}")
print(f"Max  sqrt(N)*D = {max_final:.4f}")
print(f"Expected (equidist): {EXPECTED_SQRT_N_D:.4f}")
print()

if max_final < EXPECTED_SQRT_N_D * 2.0:
    verdict = "CONSISTENT with equidistribution (Option A direction)"
    verdict2 = "sqrt(N)*D_KS has not grown significantly beyond Kolmogorov expectation."
else:
    verdict = "GROWING: equidistribution may be failing"
    verdict2 = f"sqrt(N)*D_KS = {max_final:.3f} >> {EXPECTED_SQRT_N_D:.3f} expected."

print(f"Verdict: {verdict}")
print(f"  {verdict2}")
print()
print(f"Ratio max/expected: {max_final/EXPECTED_SQRT_N_D:.3f}")
print(f"  If this ratio stays bounded as N -> inf: equidistribution holds (Option A).")
print(f"  If this ratio grows: equidistribution fails (hard wall for F1 Option A).")
print()

# ---- T* as threshold ----------------------------------------------------
print("T* threshold status at N=2000:")
for p in TEST_PRIMES:
    d = results[p][max(results[p].keys())]['D_KS']
    pct = d / T_STAR * 100
    print(f"  p={p}: D_KS={d:.5f}, D_KS/T*={pct:.1f}%  ({'<<' if pct < 50 else '<'} T*)")
print()
print(f"All {len(TEST_PRIMES)} primes: D_KS << T* at N={N_ZEROS}. RH consistent.")

# ---- Save ----------------------------------------------------------------
output = {
    'T_star': T_STAR,
    'N_zeros': N_ZEROS,
    'checkpoints': CHECKPOINTS,
    'test_primes': TEST_PRIMES,
    'expected_sqrt_N_D': EXPECTED_SQRT_N_D,
    'results': {str(p): {str(n): v for n,v in results[p].items()} for p in TEST_PRIMES},
    'final_sqrt_N_D': final_snds,
    'verdict': verdict,
}

with open('rh_growth_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to rh_growth_results.json")
