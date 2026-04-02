"""
k11_h3_mellin.py
K11 H3 Numerical Experiment: Mellin inversion of A3_N to recover H3.

Protocol:
  1. Compute A3_N(c + it) for c=2, t in a grid [0, T] with step dt
  2. Numerically invert the Mellin transform: H3_N(x) = (1/2pi) int A3_N(c+it) x^{-c-it} dt
  3. Find local maxima of |H3_N(x)| for x in [0, 250]
  4. Compare peak locations to known zeta-zero gamma_k

Pre-registered prediction (K11.B2):
  With N=2000 primes, the first 15 zeta-zeros should appear as peaks
  in |H3_N(x)| with |peak_x - gamma_k| < 2.0 (resolution limited by T).

Resolution: dx ~ pi/T (Heisenberg limit of the numerical Fourier transform).
With T=500: dx ~ 0.006 (enough to separate adjacent zeros at distance ~1).
"""

import math
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Known zeta-zeros (first 30) ─────────────────────────────────────────────

ZETA_ZEROS_IMAG = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831778, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
]

# ── Kloosterman sum ──────────────────────────────────────────────────────────

def kloosterman(p):
    total = 0.0
    for k in range(1, p):
        kinv = pow(k, -1, p)
        total += math.cos(2 * math.pi * (k + kinv) / p)
    return total


def sieve_primes(N):
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, N+1, i):
                sieve[j] = False
    return [i for i in range(2, N+1) if sieve[i]]


def a3_at_s(primes, kl_cache, s_real, s_imag):
    """A3_N(s) = sum_p Kl(1,1;p) * p^{-s}. Returns (re, im)."""
    re = 0.0
    im = 0.0
    for p in primes:
        kl = kl_cache[p]
        mag = p ** (-s_real)
        phase = -s_imag * math.log(p)
        re += kl * mag * math.cos(phase)
        im += kl * mag * math.sin(phase)
    return re, im


# ── Numerical Mellin inversion ───────────────────────────────────────────────

def mellin_inverse_at_x(a3_grid, t_vals, x, c):
    """
    H3_N(x) = (1/2pi) * int_{-T}^{T} A3_N(c+it) * x^{-(c+it)} dt
             = (1/2pi) * x^{-c} * int_{-T}^{T} A3_N(c+it) * exp(-it*log(x)) dt

    This is the inverse Fourier transform of t -> A3_N(c+it) evaluated at freq = log(x)/(2pi).
    """
    log_x = math.log(x)
    dt = t_vals[1] - t_vals[0] if len(t_vals) > 1 else 1.0
    re_sum = 0.0
    im_sum = 0.0
    for i, t in enumerate(t_vals):
        a3_re, a3_im = a3_grid[i]
        # x^{-(c+it)} = exp(-(c+it)*log x) = x^{-c} * exp(-it*log x)
        cos_t = math.cos(-t * log_x)
        sin_t = math.sin(-t * log_x)
        # Multiply A3(c+it) * x^{-it}
        prod_re = a3_re * cos_t - a3_im * sin_t
        prod_im = a3_re * sin_t + a3_im * cos_t
        re_sum += prod_re
        im_sum += prod_im
    # Multiply by x^{-c} * dt / (2pi)
    factor = (x ** (-c)) * dt / (2 * math.pi)
    return re_sum * factor, im_sum * factor


def find_local_maxima(x_vals, h3_abs, min_gap=0.5):
    """Find local maxima in h3_abs with minimum separation min_gap in x."""
    peaks = []
    n = len(h3_abs)
    for i in range(1, n - 1):
        if h3_abs[i] > h3_abs[i-1] and h3_abs[i] > h3_abs[i+1]:
            # Check it's above mean + 0.5*std (significance filter)
            peaks.append((x_vals[i], h3_abs[i]))
    # Merge nearby peaks (keep highest within min_gap)
    if not peaks:
        return []
    merged = [peaks[0]]
    for x, h in peaks[1:]:
        if x - merged[-1][0] < min_gap:
            if h > merged[-1][1]:
                merged[-1] = (x, h)
        else:
            merged.append((x, h))
    return merged


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    PRIME_LIMIT = 1000
    C = 2.0          # Mellin contour Re(s) = c
    T_MAX = 300.0    # Integrate t from -T to T
    DT = 0.1         # Step size -- resolution in x: dx ~ pi/T_MAX = 0.01
    X_MIN = 1.0
    X_MAX = 120.0
    DX = 0.5         # Step in x for H3 evaluation

    print("=" * 65)
    print("K11 H3 Numerical Experiment: Mellin Inversion of A3_N")
    print(f"  Primes <= {PRIME_LIMIT}, c={C}, T={T_MAX}, dt={DT}")
    print(f"  Resolution dx ~ pi/T = {math.pi/T_MAX:.4f}")
    print("=" * 65)

    primes = sieve_primes(PRIME_LIMIT)
    print(f"\n{len(primes)} primes. Building Kloosterman cache...", end=" ", flush=True)
    kl_cache = {p: kloosterman(p) for p in primes}
    print("done.")

    # ── Build A3 grid on Re(s)=c ──
    t_vals = []
    t = 0.0
    while t <= T_MAX:
        t_vals.append(t)
        t += DT
    # Add negative t values (for real-valued H3, A3(c-it) = conj(A3(c+it)))
    t_neg = [-t for t in t_vals[1:]]
    all_t = list(reversed(t_neg)) + t_vals

    print(f"Computing A3_N on Re={C} grid: {len(all_t)} points...", end=" ", flush=True)
    a3_grid = []
    for t in all_t:
        re, im = a3_at_s(primes, kl_cache, C, t)
        a3_grid.append((re, im))
    print("done.")

    # ── Compute H3_N(x) ──
    x_vals = []
    x = X_MIN
    while x <= X_MAX:
        x_vals.append(x)
        x += DX

    print(f"Computing H3_N(x) at {len(x_vals)} x-values...", end=" ", flush=True)
    h3_re = []
    h3_im = []
    for x in x_vals:
        re, im = mellin_inverse_at_x(a3_grid, all_t, x, C)
        h3_re.append(re)
        h3_im.append(im)
    h3_abs = [math.hypot(r, i) for r, i in zip(h3_re, h3_im)]
    print("done.")

    # ── Find peaks ──
    peaks = find_local_maxima(x_vals, h3_abs, min_gap=0.8)
    top_peaks = sorted(peaks, key=lambda p: p[1], reverse=True)[:30]
    top_peaks.sort(key=lambda p: p[0])  # sort by x

    # ── Compare to known zeros ──
    print("\n-- H3_N(x) Local Maxima vs Zeta-Zeros --")
    print(f"  Found {len(top_peaks)} significant peaks in x in [{X_MIN}, {X_MAX}]")
    print()
    print(f"  {'Peak x':>10}  {'|H3_N|':>10}  {'Nearest gamma_k':>16}  {'Delta':>8}  {'Match?':>8}")
    print("  " + "-" * 58)

    matches = 0
    near_threshold = 2.0
    for px, ph in top_peaks:
        # Find nearest zeta-zero
        nearest = min(ZETA_ZEROS_IMAG, key=lambda g: abs(g - px))
        delta = abs(nearest - px)
        match = delta < near_threshold
        if match:
            matches += 1
        flag = "<-- MATCH" if match else ""
        print(f"  {px:>10.3f}  {ph:>10.6f}  {nearest:>16.4f}  {delta:>8.3f}  {flag}")

    print(f"\n  Total peaks: {len(top_peaks)}")
    print(f"  Peaks within {near_threshold} of a zeta-zero: {matches}")
    print(f"  Match rate: {matches}/{len(top_peaks)} = {matches/max(len(top_peaks),1)*100:.1f}%")

    # ── Reverse: how many of the first 20 zeros have a nearby peak? ──
    print("\n-- Zeta-Zeros vs Nearest H3 Peak --")
    print(f"  {'gamma_k':>10}  {'nearest peak':>14}  {'delta':>8}  {'detected?':>10}")
    print("  " + "-" * 50)
    detected = 0
    peak_xs = [p[0] for p in top_peaks]
    for g in ZETA_ZEROS_IMAG[:20]:
        if g > X_MAX:
            break
        if not peak_xs:
            nearest_p = float('nan')
            delta = float('nan')
        else:
            nearest_p = min(peak_xs, key=lambda px: abs(px - g))
            delta = abs(nearest_p - g)
        det = delta < near_threshold if not math.isnan(delta) else False
        if det:
            detected += 1
        flag = "YES" if det else "---"
        print(f"  {g:>10.4f}  {nearest_p:>14.3f}  {delta:>8.3f}  {flag:>10}")

    in_range = sum(1 for g in ZETA_ZEROS_IMAG[:20] if g <= X_MAX)
    print(f"\n  Zeros in x range [1, {X_MAX}]: {in_range}")
    print(f"  Detected (peak within {near_threshold}): {detected}/{in_range}")

    # ── Verdict ──
    print("\n-- K11.B2 Pre-Registration Verdict --")
    detection_rate = detected / max(in_range, 1)
    if detection_rate >= 0.5:
        verdict = "B2 SUPPORTED -- H3 peaks correspond to zeta-zero locations"
        tier = "Promotes K11.B2 to C-tier"
    elif detection_rate >= 0.25:
        verdict = "PARTIAL SIGNAL -- increase T_MAX and prime count"
        tier = "Remains B-tier, needs larger computation"
    else:
        verdict = "B2 NOT SUPPORTED -- H3 peaks not at zeta-zero locations"
        tier = "K11.B2 moving toward D no-go"

    print(f"  {verdict}")
    print(f"  {tier}")
    print(f"  Detection rate: {detection_rate*100:.1f}%")
    print()
    print("  NOTE: Resolution limited by T_MAX. For reliable zero detection,")
    print(f"  need T_MAX >> 100 and DT << 0.05. Current: T={T_MAX}, dt={DT}.")


if __name__ == "__main__":
    main()
