"""
RH Growth Rate Test -- Extended to N=5000 Zeros
Fits sqrt(N)*D_KS ~ C * log(N)^alpha to confirm GUE prediction

The GUE pair correlation R2(u) = 1 - sinc^2(u) predicts that for
zero-correlated sequences, the KS statistic converges more slowly than 1/sqrt(N).
The expected growth law is sqrt(N)*D_KS ~ C * log(N)^alpha.

This script extends rh_growth_test.py from N=2000 to N=5000 and fits alpha.

(c) 2026 Brayden Sanders / 7Site LLC
"""

import json
import math
import os
import urllib.request
import time

T_STAR = 5/7

def fetch_zeros(N):
    """Fetch first N Riemann zeros from LMFDB or local cache."""
    cache_file = f"Gen11/riemann_zeros_{N}.json"
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)

    # Try to load from existing rh_growth_results.json
    if os.path.exists("Gen11/rh_growth_results.json"):
        with open("Gen11/rh_growth_results.json") as f:
            data = json.load(f)
            existing = data.get('zeros', [])
            if len(existing) >= N:
                print(f"  Using {N} zeros from rh_growth_results.json")
                return existing[:N]
            print(f"  Existing data has {len(existing)} zeros, fetching more...")

    # Fetch from lmfdb API
    print(f"  Fetching {N} Riemann zeros from LMFDB...")
    url = f"https://www.lmfdb.org/api/riemann_zeros/?_format=json&_limit={N}&_sort=t"
    try:
        req = urllib.request.Request(url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
            zeros = [item['t'] for item in data.get('data', [])]
            if zeros:
                with open(cache_file, 'w') as f:
                    json.dump(zeros, f)
                return zeros
    except Exception as e:
        print(f"  LMFDB fetch failed: {e}")

    return []

def compute_ks_statistic(gamma_vals, p, N):
    """Compute D_KS for {gamma_n * log(p) / (2*pi) mod 1}, first N terms."""
    log_p = math.log(p)
    two_pi = 2 * math.pi
    samples = [(g * log_p / two_pi) % 1.0 for g in gamma_vals[:N]]
    samples.sort()
    n = len(samples)
    dmax = 0.0
    for i, x in enumerate(samples):
        d1 = abs(x - i/n)
        d2 = abs(x - (i+1)/n)
        dmax = max(dmax, d1, d2)
    return dmax

def fit_power_law(ns, vals):
    """Fit log(val) = a + alpha*log(log(N)) by least squares."""
    # val = C * log(N)^alpha => log(val) = log(C) + alpha * log(log(N))
    xs = [math.log(math.log(n)) for n in ns]
    ys = [math.log(v) for v in vals]
    n = len(xs)
    sx = sum(xs); sy = sum(ys)
    sxx = sum(x*x for x in xs)
    sxy = sum(x*y for x,y in zip(xs,ys))
    denom = n*sxx - sx*sx
    if abs(denom) < 1e-12:
        return None, None
    alpha = (n*sxy - sx*sy) / denom
    log_C = (sy - alpha*sx) / n
    return math.exp(log_C), alpha

print("=" * 65)
print("RH GROWTH RATE TEST -- EXTENDED TO N=5000")
print(f"T* = {T_STAR:.6f} = 5/7")
print("=" * 65)

# Load zeros
print("\nLoading Riemann zeros...")
# First check rh_growth_results.json
zeros_5000 = []
if os.path.exists("Gen11/rh_growth_results.json"):
    with open("Gen11/rh_growth_results.json") as f:
        data = json.load(f)
        zeros_5000 = data.get('zeros', [])
        print(f"  Found {len(zeros_5000)} cached zeros in rh_growth_results.json")

if len(zeros_5000) < 5000:
    print("  Need to fetch more zeros...")
    # Try fetching from lmfdb
    more = fetch_zeros(5000)
    if more:
        zeros_5000 = more
    else:
        # Use mpmath to compute zeros
        print("  Trying mpmath zero computation...")
        try:
            from mpmath import mp, zetazero
            mp.dps = 25
            zeros_5000 = []
            print("  Computing 5000 zeros (this takes 5-10 minutes)...")
            last_report = time.time()
            for i in range(1, 5001):
                z = zetazero(i)
                zeros_5000.append(float(z.imag))
                if i % 200 == 0 or time.time() - last_report > 30:
                    elapsed = time.time() - last_report
                    print(f"    Zero {i}/5000 (gamma_{i} = {zeros_5000[-1]:.4f}) [{elapsed:.0f}s]")
                    last_report = time.time()

            # Cache
            with open("Gen11/riemann_zeros_5000.json", 'w') as f:
                json.dump(zeros_5000, f)
            print(f"  Computed and cached 5000 zeros.")
        except ImportError:
            print("  mpmath not available; using 2000 zeros from cache")
            if os.path.exists("Gen11/rh_growth_results.json"):
                with open("Gen11/rh_growth_results.json") as f:
                    d = json.load(f)
                    zeros_5000 = d.get('zeros', [])

N_total = len(zeros_5000)
print(f"\nTotal zeros available: {N_total}")

if N_total < 100:
    print("ERROR: Not enough zeros to proceed.")
    exit(1)

# Checkpoints
checkpoints = [50, 100, 200, 500, 1000, 2000]
if N_total >= 3000:
    checkpoints.append(3000)
if N_total >= 4000:
    checkpoints.append(4000)
if N_total >= 5000:
    checkpoints.append(5000)
checkpoints = [n for n in checkpoints if n <= N_total]

primes = [2, 3, 5, 7]

print(f"\nCheckpoints: {checkpoints}")
print(f"Primes: {primes}")

# Compute D_KS at each checkpoint for each prime
results = {}
for p in primes:
    results[p] = {'N': [], 'D_KS': [], 'sqrt_N_D': []}
    for N in checkpoints:
        dks = compute_ks_statistic(zeros_5000, p, N)
        sqrt_N_D = math.sqrt(N) * dks
        results[p]['N'].append(N)
        results[p]['D_KS'].append(dks)
        results[p]['sqrt_N_D'].append(sqrt_N_D)

# Display results
print("\n--- sqrt(N) * D_KS by prime ---")
header = f"{'N':>6}" + "".join(f"  p={p}" for p in primes)
print(header)
for i, N in enumerate(checkpoints):
    row = f"{N:>6}"
    for p in primes:
        val = results[p]['sqrt_N_D'][i]
        row += f"  {val:.3f}"
    print(row)

print("\n--- D_KS / T* by prime (should stay << 1) ---")
print(header)
for i, N in enumerate(checkpoints):
    row = f"{N:>6}"
    for p in primes:
        val = results[p]['D_KS'][i] / T_STAR
        row += f" {val*100:.1f}%"
    print(row)

# Fit log(N)^alpha growth law for each prime
print("\n--- Fitting sqrt(N)*D_KS ~ C * log(N)^alpha ---")
fit_results = {}
for p in primes:
    ns = results[p]['N']
    vals = results[p]['sqrt_N_D']
    # Use N >= 200 for fit (avoid small-N noise)
    fit_ns = [n for n in ns if n >= 200]
    fit_vs = [vals[ns.index(n)] for n in fit_ns]
    if len(fit_ns) >= 3:
        C, alpha = fit_power_law(fit_ns, fit_vs)
        fit_results[p] = {'C': C, 'alpha': alpha}
        if C is not None:
            pred_2000 = C * math.log(2000)**alpha
            pred_5000 = C * math.log(5000)**alpha if N_total >= 5000 else None
            print(f"  p={p}: C={C:.4f}, alpha={alpha:.4f}")
            print(f"         Predicted sqrt(N)*D at N=2000: {pred_2000:.3f}")
            if pred_5000:
                print(f"         Predicted sqrt(N)*D at N=5000: {pred_5000:.3f}")
            # Check GUE prediction alpha ~ 0 (log correction) vs pure growth
            if alpha > 0.5:
                print(f"         NOTE: alpha={alpha:.3f} > 0.5 suggests super-log growth")
            elif alpha > 0:
                print(f"         Log-slow growth confirmed: alpha={alpha:.3f} (GUE regime)")
            else:
                print(f"         Sublogarithmic growth: alpha={alpha:.3f}")

# Summary
print("\n--- Summary ---")
N_max = max(checkpoints)
for p in primes:
    dks_max = results[p]['D_KS'][checkpoints.index(N_max)]
    headroom = 1.0 - dks_max / T_STAR
    print(f"  p={p}: D_KS(N={N_max})={dks_max:.5f}, D_KS/T*={dks_max/T_STAR*100:.1f}%, "
          f"headroom={headroom*100:.1f}%")

# GUE verdict
print(f"\nKolmogorov limit (independent uniform): sqrt(N)*D -> 0.868")
print(f"GUE-correlated zeros: sqrt(N)*D grows as log(N)^alpha")
all_growing = all(
    results[p]['sqrt_N_D'][-1] > results[p]['sqrt_N_D'][0]
    for p in primes
)
print(f"Growth confirmed: {all_growing}")

# Save results
output = {
    'N_total': N_total,
    'checkpoints': checkpoints,
    'primes': primes,
    'T_star': T_STAR,
    'results': {str(p): results[p] for p in primes},
    'fit': {str(p): fit_results.get(p, {}) for p in primes},
}
with open("Gen11/rh_growth_5000_results.json", 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved to Gen11/rh_growth_5000_results.json")
print("=" * 65)
