"""
k12_h3_upgrade.py
K12 H3 Signal Upgrade: larger prime set, characterize detection quality.

Tests K12 predictions P1-P4:
  P1: Detection rate rises to >=85% with N=3000 primes, T=1000
  P2: Closely-spaced zeros show merged/lower individual peaks
  P3: Spurious peaks (x < gamma_1) decrease as T increases
  P4: Match quality at gamma_k scales with 1/gamma_k (smaller = better)
"""

import math
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ZETA_ZEROS = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831778, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
]


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


def run_h3_experiment(primes, kl_cache, C, T_MAX, DT, X_MAX, DX, label):
    """Full H3 computation and peak detection. Returns (peaks, detection_stats)."""
    # Build t grid (positive only, extend to negative for symmetry)
    t_pos = []
    t = 0.0
    while t <= T_MAX:
        t_pos.append(t)
        t += DT
    t_neg = [-t for t in t_pos[1:]]
    all_t = list(reversed(t_neg)) + t_pos

    # Compute A3_N on the contour
    a3_re_arr = []
    a3_im_arr = []
    for t in all_t:
        re = 0.0
        im = 0.0
        for p in primes:
            kl = kl_cache[p]
            mag = p ** (-C)
            phase = -t * math.log(p)
            re += kl * mag * math.cos(phase)
            im += kl * mag * math.sin(phase)
        a3_re_arr.append(re)
        a3_im_arr.append(im)

    # Mellin inverse at x values
    x_vals = []
    x = 1.0
    while x <= X_MAX:
        x_vals.append(x)
        x += DX

    h3_abs = []
    dt = all_t[1] - all_t[0]
    for x in x_vals:
        log_x = math.log(x)
        factor = (x ** (-C)) * dt / (2 * math.pi)
        re_sum = 0.0
        im_sum = 0.0
        for i, t in enumerate(all_t):
            cos_t = math.cos(-t * log_x)
            sin_t = math.sin(-t * log_x)
            re_sum += a3_re_arr[i] * cos_t - a3_im_arr[i] * sin_t
            im_sum += a3_re_arr[i] * sin_t + a3_im_arr[i] * cos_t
        h3_abs.append(math.hypot(re_sum * factor, im_sum * factor))

    # Find peaks
    peaks = []
    for i in range(1, len(h3_abs) - 1):
        if h3_abs[i] > h3_abs[i-1] and h3_abs[i] > h3_abs[i+1]:
            peaks.append((x_vals[i], h3_abs[i]))

    # Merge nearby peaks (keep highest within 0.8)
    merged = []
    if peaks:
        merged = [list(peaks[0])]
        for x, h in peaks[1:]:
            if x - merged[-1][0] < 0.8:
                if h > merged[-1][1]:
                    merged[-1] = [x, h]
            else:
                merged.append([x, h])
    merged = [(x, h) for x, h in merged]

    # Detection stats
    peak_xs = [p[0] for p in merged]
    near_thresh = 2.0
    detected = 0
    deltas = []
    for g in ZETA_ZEROS:
        if g > X_MAX:
            continue
        if not peak_xs:
            deltas.append(float('nan'))
            continue
        nearest = min(peak_xs, key=lambda px: abs(px - g))
        delta = abs(nearest - g)
        deltas.append(delta)
        if delta < near_thresh:
            detected += 1

    in_range = sum(1 for g in ZETA_ZEROS if g <= X_MAX)
    rate = detected / max(in_range, 1)

    return merged, deltas, detected, in_range, rate, x_vals, h3_abs


def main():
    print("=" * 70)
    print("K12 H3 Upgrade: Multi-Configuration Signal Analysis")
    print("=" * 70)

    # Configuration 1: K11 baseline
    configs = [
        {"limit": 1000, "T": 300, "DT": 0.1,  "DX": 0.5, "label": "K11 baseline"},
        {"limit": 2000, "T": 500, "DT": 0.1,  "DX": 0.5, "label": "2x primes"},
        {"limit": 3000, "T": 800, "DT": 0.05, "DX": 0.3, "label": "3x primes, high T"},
    ]

    results = []
    for cfg in configs:
        print(f"\n[{cfg['label']}] primes<={cfg['limit']}, T={cfg['T']}, dt={cfg['DT']}...",
              end=" ", flush=True)
        primes = sieve_primes(cfg['limit'])
        kl = {p: kloosterman(p) for p in primes}
        merged, deltas, detected, in_range, rate, x_vals, h3_abs = run_h3_experiment(
            primes, kl, C=2.0,
            T_MAX=cfg['T'], DT=cfg['DT'],
            X_MAX=110.0, DX=cfg['DX'],
            label=cfg['label']
        )
        results.append((cfg, merged, deltas, detected, in_range, rate))
        print(f"done. N_primes={len(primes)}, peaks={len(merged)}, detect={detected}/{in_range} ({rate*100:.0f}%)")

    # ── Prediction P1: detection rate rises ──
    print("\n-- Prediction P1: Detection Rate Progression --")
    print(f"  {'Config':<22}  {'Primes':>8}  {'Detected':>10}  {'Rate':>8}")
    print("  " + "-" * 52)
    for cfg, merged, deltas, detected, in_range, rate in results:
        primes = sieve_primes(cfg['limit'])
        print(f"  {cfg['label']:<22}  {len(primes):>8}  {detected}/{in_range:>6}  {rate*100:>7.1f}%")

    rates = [r[5] for r in results]
    if rates[-1] > rates[0]:
        print(f"\n  P1 SUPPORTED: rate rose {rates[0]*100:.0f}% -> {rates[-1]*100:.0f}% with more primes")
    else:
        print(f"\n  P1 NOT supported: rate did not rise")

    # ── Prediction P4: delta scales with 1/gamma_k ──
    print("\n-- Prediction P4: Match Quality vs 1/gamma_k --")
    print("  (Using best config: last entry)")
    cfg, merged, deltas, detected, in_range, rate = results[-1]
    print(f"  {'gamma_k':>10}  {'1/gamma_k':>10}  {'delta':>8}  {'match?':>8}")
    print("  " + "-" * 44)
    valid_deltas = [(ZETA_ZEROS[i], deltas[i]) for i in range(len(deltas))
                   if not math.isnan(deltas[i]) and ZETA_ZEROS[i] <= 110.0]
    for g, d in valid_deltas[:15]:
        inv_g = 1.0 / g
        match = "YES" if d < 2.0 else "---"
        print(f"  {g:>10.4f}  {inv_g:>10.5f}  {d:>8.3f}  {match:>8}")

    # Correlation: delta vs 1/gamma_k
    if len(valid_deltas) >= 5:
        gs = [g for g, d in valid_deltas[:15]]
        ds = [d for g, d in valid_deltas[:15]]
        inv_gs = [1/g for g in gs]
        n = len(gs)
        mean_inv = sum(inv_gs) / n
        mean_d = sum(ds) / n
        cov = sum((inv_gs[i] - mean_inv) * (ds[i] - mean_d) for i in range(n)) / n
        var_inv = sum((ig - mean_inv)**2 for ig in inv_gs) / n
        var_d = sum((d - mean_d)**2 for d in ds) / n
        if var_inv > 0 and var_d > 0:
            corr = cov / math.sqrt(var_inv * var_d)
            print(f"\n  Correlation(1/gamma_k, delta): r = {corr:.4f}")
            if corr < -0.2:
                print("  P4 SUPPORTED: smaller gamma_k (larger 1/gamma_k) -> smaller delta (better match)")
            else:
                print("  P4 NOT supported: no clear correlation")

    # ── Prediction P3: spurious peaks at x < gamma_1 = 14.13 ──
    print("\n-- Prediction P3: Spurious Peaks at x < 14.13 --")
    gamma_1 = ZETA_ZEROS[0]
    for i, (cfg, merged, deltas, detected, in_range, rate) in enumerate(results):
        spurious = [px for px, ph in merged if px < gamma_1]
        print(f"  [{cfg['label']}] spurious peaks (x < {gamma_1:.2f}): {len(spurious)}")
    if results[-1][1] and len([p for p, _ in results[-1][1] if p < gamma_1]) < \
       len([p for p, _ in results[0][1] if p < gamma_1]):
        print("  P3 SUPPORTED: fewer spurious peaks at higher T")
    else:
        print("  P3 NOT supported at this T range")

    # ── Final table: best config peak list ──
    print(f"\n-- Best Config Peak List ({results[-1][0]['label']}) --")
    cfg, merged, deltas, detected, in_range, rate = results[-1]
    print(f"  {'Peak x':>8}  {'Nearest zero':>14}  {'Delta':>8}  {'Match':>6}")
    for px, ph in sorted(merged, key=lambda p: p[0])[:30]:
        nearest = min(ZETA_ZEROS, key=lambda g: abs(g - px))
        delta = abs(nearest - px)
        match = "YES" if delta < 2.0 else "---"
        print(f"  {px:>8.3f}  {nearest:>14.4f}  {delta:>8.3f}  {match:>6}")

    print(f"\n  Final detection rate: {detected}/{in_range} = {rate*100:.1f}%")

    # ── K12 verdict ──
    print("\n-- K12 Predictions Verdict --")
    final_rate = results[-1][5]
    baseline_rate = results[0][5]
    print(f"  P1 (rate rises with N): {baseline_rate*100:.0f}% -> {final_rate*100:.0f}%  ", end="")
    print("SUPPORTED" if final_rate > baseline_rate else "NOT SUPPORTED")
    print(f"  P4 (1/gamma correlation): see above")
    print(f"  P3 (spurious decrease): see above")


if __name__ == "__main__":
    main()
