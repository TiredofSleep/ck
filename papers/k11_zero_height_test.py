"""
k11_zero_height_test.py
K11 Attempt F: Numerical cross-correlation test.

Question: Is |A3_N(3/2 + i*gamma_k)| statistically special at ζ-zero heights gamma_k?

Protocol:
  1. Compute A3_N(s) at s = 3/2 + i*gamma_k for first 50 known ζ-zeros
  2. Compute A3_N(s) at s = 3/2 + i*t for 200 uniformly random t in [0, 200]
  3. KS test: are the |A3_N| distributions at zeros vs random different?
  4. Report mean, variance, and any systematic bias

If zeros ARE special: C-tier structural connection confirmed, motivates K12 theory.
If zeros are NOT special: closes Attempt F as D-tier no-go.
"""

import math
import random
import statistics
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── First 100 imaginary parts of ζ-zeros (standard tables) ───────────────────
# Source: Odlyzko's tables, first 100 non-trivial zeros on critical line
ZETA_ZEROS_IMAG = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831778, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 111.029535, 111.874659,
    114.320220, 116.226680, 118.790782, 121.370125, 122.946829,
    124.256819, 127.516684, 129.578704, 131.087688, 133.497737,
    134.756510, 138.116042, 139.736209, 141.123707, 143.111846,
    146.000982, 147.422765, 150.053521, 150.925257, 153.024694,
    156.112909, 157.597591, 158.849988, 161.188964, 163.030709,
    165.537069, 167.184439, 169.094516, 169.911976, 173.411536,
    174.754191, 176.441434, 178.377407, 179.916485, 182.207078,
    184.874467, 185.598783, 187.228922, 189.416159, 192.026657,
    193.079726, 195.265397, 196.876481, 198.015309, 201.264751,
    202.493595, 204.189671, 205.394697, 207.906259, 209.576510,
    211.690861, 213.347919, 214.547044, 216.169538, 219.067596,
    220.714918, 221.430705, 224.007000, 224.983324, 227.421444,
    229.337413, 231.250188, 231.987235, 233.693404, 236.524230,
]

# ── Kloosterman sum ────────────────────────────────────────────────────────────

def kloosterman(p: int) -> float:
    total = 0.0
    for k in range(1, p):
        kinv = pow(k, -1, p)
        total += math.cos(2 * math.pi * (k + kinv) / p)
    return total


def sieve_primes(N: int) -> list:
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, N+1, i):
                sieve[j] = False
    return [i for i in range(2, N+1) if sieve[i]]


def a3_partial(primes, kl_cache, s_real, s_imag):
    """A3_N(s) = Σ_p Kl(1,1;p) * p^{-s}, s = s_real + i*s_imag."""
    re_total = 0.0
    im_total = 0.0
    for p in primes:
        kl = kl_cache[p]
        # p^{-s} = exp(-s * log p) = exp(-s_real*log p) * exp(-i*s_imag*log p)
        mag = p ** (-s_real)
        phase = -s_imag * math.log(p)
        re_total += kl * mag * math.cos(phase)
        im_total += kl * mag * math.sin(phase)
    return math.hypot(re_total, im_total)


# ── Statistical utilities ──────────────────────────────────────────────────────

def ks_statistic(sample1, sample2):
    """Two-sample KS statistic."""
    combined = sorted(set(sample1 + sample2))
    n1, n2 = len(sample1), len(sample2)
    s1 = sorted(sample1)
    s2 = sorted(sample2)
    i, j = 0, 0
    D = 0.0
    for x in combined:
        while i < n1 and s1[i] <= x:
            i += 1
        while j < n2 and s2[j] <= x:
            j += 1
        F1 = i / n1
        F2 = j / n2
        D = max(D, abs(F1 - F2))
    return D


def percentile(data, p):
    sorted_data = sorted(data)
    idx = (len(sorted_data) - 1) * p / 100
    lo = int(idx)
    hi = lo + 1
    if hi >= len(sorted_data):
        return sorted_data[-1]
    frac = idx - lo
    return sorted_data[lo] * (1 - frac) + sorted_data[hi] * frac


# ── Main test ──────────────────────────────────────────────────────────────────

def main():
    PRIME_LIMIT = 2000
    S_REAL = 1.6  # Well inside Re(s) > 3/2 convergence strip
    N_RANDOM = 300
    RANDOM_T_RANGE = (0.5, 250.0)
    random.seed(42)

    print("=" * 65)
    print("K11 Attempt F: Zero-Height Correlation Test")
    print(f"  A3_N(s) at s = {S_REAL} + i*t")
    print(f"  Primes up to: {PRIME_LIMIT}")
    print("=" * 65)

    primes = sieve_primes(PRIME_LIMIT)
    print(f"\nBuilding Kloosterman cache for {len(primes)} primes...", end=" ", flush=True)
    kl_cache = {p: kloosterman(p) for p in primes}
    print("done.")

    # ── Evaluate at ζ-zero heights ──
    print(f"\nEvaluating at first {len(ZETA_ZEROS_IMAG)} zeta-zero heights...")
    zero_vals = []
    for gamma in ZETA_ZEROS_IMAG:
        val = a3_partial(primes, kl_cache, S_REAL, gamma)
        zero_vals.append(val)

    # ── Evaluate at random heights ──
    print(f"Evaluating at {N_RANDOM} random heights in [{RANDOM_T_RANGE[0]}, {RANDOM_T_RANGE[1]}]...")
    random_ts = [random.uniform(*RANDOM_T_RANGE) for _ in range(N_RANDOM)]
    random_vals = []
    for t in random_ts:
        val = a3_partial(primes, kl_cache, S_REAL, t)
        random_vals.append(val)

    # ── Statistics ──
    z_mean = statistics.mean(zero_vals)
    z_std = statistics.stdev(zero_vals)
    z_med = percentile(zero_vals, 50)

    r_mean = statistics.mean(random_vals)
    r_std = statistics.stdev(random_vals)
    r_med = percentile(random_vals, 50)

    ks = ks_statistic(zero_vals, random_vals)

    print("\n── Results ──")
    print(f"{'Metric':<22} {'At ζ-zeros':>14} {'At random t':>14} {'Ratio':>10}")
    print("-" * 62)
    print(f"{'Mean |A3_N|':<22} {z_mean:>14.6f} {r_mean:>14.6f} {z_mean/r_mean:>10.4f}")
    print(f"{'Std dev':<22} {z_std:>14.6f} {r_std:>14.6f} {z_std/r_std:>10.4f}")
    print(f"{'Median':<22} {z_med:>14.6f} {r_med:>14.6f} {z_med/r_med:>10.4f}")
    print(f"{'Min':<22} {min(zero_vals):>14.6f} {min(random_vals):>14.6f}")
    print(f"{'Max':<22} {max(zero_vals):>14.6f} {max(random_vals):>14.6f}")
    print(f"\n  KS statistic (two-sample): {ks:.6f}")
    print(f"  (KS > 0.20 suggests distinct distributions; < 0.10 suggests same)")

    # ── Histogram ──
    print("\n── Distribution Histogram (|A3_N|) ──")
    all_vals = zero_vals + random_vals
    lo, hi = min(all_vals), max(all_vals)
    bins = 10
    width = (hi - lo) / bins
    print(f"  Range: [{lo:.4f}, {hi:.4f}]   bin width: {width:.4f}")
    print(f"  {'bin':>8}  {'zeros':>6}  {'random':>6}")
    for i in range(bins):
        blo = lo + i * width
        bhi = blo + width
        zc = sum(1 for v in zero_vals if blo <= v < bhi)
        rc = sum(1 for v in random_vals if blo <= v < bhi)
        z_bar = '#' * zc
        r_bar = '.' * min(rc, 30)
        print(f"  [{blo:6.3f},{bhi:6.3f})  {zc:>6}  {rc:>6}  {z_bar}{r_bar}")

    # ── First few ζ-zeros ──
    print("\n── First 15 ζ-zeros vs |A3_N| ──")
    print(f"  {'gamma':>10}  {'|A3_N|':>12}  {'vs r_mean':>12}")
    for gamma, val in zip(ZETA_ZEROS_IMAG[:15], zero_vals[:15]):
        diff = (val - r_mean) / r_std
        print(f"  {gamma:>10.4f}  {val:>12.6f}  {diff:>+10.3f} σ")

    # ── Verdict ──
    print("\n── K11 Attempt F Verdict ──")
    ratio = z_mean / r_mean
    if abs(ratio - 1.0) < 0.05 and ks < 0.10:
        verdict = "NO STRUCTURE DETECTED — Attempt F → D-tier no-go"
        detail = "ζ-zero heights show no statistical anomaly in A3_N."
    elif abs(ratio - 1.0) < 0.15 and ks < 0.20:
        verdict = "WEAK SIGNAL — Attempt F remains B-tier"
        detail = "Marginal difference. Larger N_primes needed."
    else:
        verdict = "STRUCTURE DETECTED — Attempt F → C-tier, motivates K12"
        detail = f"Mean ratio={ratio:.4f}, KS={ks:.4f} — statistically distinct."
    print(f"  {verdict}")
    print(f"  {detail}")

    # ── K11 implications ──
    print("\n── K11 Structural Implications ──")
    print(f"  If A3_N values at ζ-zero heights are NOT special:")
    print(f"    → The Kloosterman sum carries no local memory of ζ-zero locations")
    print(f"    → The Eisenstein bridge must be GLOBAL (integral, not pointwise)")
    print(f"    → Double Dirichlet Z(s,w) becomes the only theoretical path")
    print()
    print(f"  If A3_N values ARE special:")
    print(f"    → A3(s) has an analytic feature (zero, pole, saddle) at s=3/2+i*gamma_k")
    print(f"    → This would be a completely new result — analytic structure of A3 at ζ-heights")
    print(f"    → K12 must explain WHY: which mechanism links A3 poles/zeros to ζ-zeros?")


if __name__ == "__main__":
    main()
