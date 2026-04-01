#!/usr/bin/env python3
"""
k7_scan_scaling.py — Confirm p^alpha normalization for D_p at larger range

Tests alpha in {0, 0.25, 0.5, 0.75, 1.0} and reports which stabilizes.

From K7_EXACT_FORMULA_FOR_RP.md: the PSD correction Delta_p(xi) = O(1/p),
so the natural normalization in FREQUENCY SPACE is alpha=1 (multiply by p),
not alpha=1/2 (which was the Weil-bound result in position space).

This script:
  1. Computes Delta_p(xi) = S_p(xi) - sinc^2(xi) for primes up to pmax
  2. For each alpha, computes p^alpha * Delta_p(xi)
  3. Reports mean, variance, sup across primes for each alpha

Outputs:
    k7_scaling_results.json
    k7_scaling_summary.txt

Usage:
    python k7_scan_scaling.py [--pmax 50000] [--xi 0.5]
"""

import argparse
import json
import math


def primes_up_to(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
    return [i for i in range(2, n + 1) if sieve[i]]


def sinc2(xi):
    if abs(xi) < 1e-12:
        return 1.0
    x = math.pi * xi
    return (math.sin(x) / x) ** 2


def psd_exact(xi, p):
    if abs(xi) < 1e-12:
        return 1.0
    u = math.pi * xi / p
    if abs(math.sin(u)) < 1e-14:
        return float('nan')
    num = math.sin(math.pi * xi * (p - 1) / p) ** 2
    den = (p - 1) ** 2 * math.sin(u) ** 2
    return num / den


def delta_p(xi, p):
    sp = psd_exact(xi, p)
    if math.isnan(sp):
        return float('nan')
    return sp - sinc2(xi)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmax", type=int, default=20000)
    parser.add_argument("--xi", type=float, default=0.5)
    parser.add_argument("--out", default="k7_scaling_results.json")
    parser.add_argument("--summary", default="k7_scaling_summary.txt")
    args = parser.parse_args()

    primes = primes_up_to(args.pmax)
    xi = args.xi
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]

    print(f"[k7_scaling] xi={xi}, {len(primes)} primes up to {args.pmax}")

    # Compute scaled corrections
    scaled = {alpha: [] for alpha in alphas}
    for p in primes:
        d = delta_p(xi, p)
        if math.isnan(d):
            continue
        for alpha in alphas:
            scaled[alpha].append((p, p**alpha * d))

    # Statistics per alpha
    stats = {}
    for alpha in alphas:
        vals = [v for _, v in scaled[alpha]]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        var = sum((v - mean)**2 for v in vals) / len(vals)
        sup = max(abs(v) for v in vals)
        # Trend: does it grow/shrink? Compare mean at first half vs second half
        mid = len(vals) // 2
        mean_early = sum(vals[:mid]) / mid if mid else float('nan')
        mean_late = sum(vals[mid:]) / (len(vals) - mid) if len(vals) > mid else float('nan')
        stats[alpha] = {
            "mean": mean,
            "variance": var,
            "sup_norm": sup,
            "mean_early_primes": mean_early,
            "mean_late_primes": mean_late,
            "trend": "GROWING" if abs(mean_late) > abs(mean_early) * 1.5
                     else "SHRINKING" if abs(mean_late) < abs(mean_early) * 0.67
                     else "STABLE",
        }

    # Determine natural alpha
    stable_alphas = [a for a, s in stats.items() if s["trend"] == "STABLE"]

    # Save
    with open(args.out, 'w') as f:
        json.dump({"xi": xi, "pmax": args.pmax, "stats": {str(a): s for a, s in stats.items()}},
                  f, indent=2)

    # Summary
    lines = [
        "K7 Scaling Audit Results",
        "=" * 60,
        f"xi = {xi},  primes up to {args.pmax}",
        "",
        f"{'alpha':>6}  {'mean':>12}  {'variance':>12}  {'sup':>12}  {'trend':>10}",
        "-" * 60,
    ]
    for alpha in alphas:
        s = stats.get(alpha, {})
        lines.append(
            f"{alpha:>6.2f}  {s.get('mean', float('nan')):>12.4e}  "
            f"{s.get('variance', float('nan')):>12.4e}  "
            f"{s.get('sup_norm', float('nan')):>12.4e}  "
            f"{s.get('trend', '?'):>10}"
        )
    lines.append("")
    lines.append(f"STABLE alpha(s): {stable_alphas}")
    lines.append("")
    lines.append("INTERPRETATION (from K7_EXACT_FORMULA_FOR_RP.md):")
    lines.append("  Delta_p(xi) = O(1/p) in frequency space (exact formula, not Weil bound).")
    lines.append("  Natural normalization: alpha = 1 (multiply by p) gives D_p^PSD = O(1).")
    lines.append("  NOTE: This D_p^PSD has a DETERMINISTIC limit -2[sinc(2xi)-sinc^2(xi)].")
    lines.append("  The prime-specific correction is at the NEXT order: O(1/p) after subtracting leading term.")
    lines.append("  Contrast with K6 position-space Weil bound: alpha=1/2 stabilizes position-space D_p.")
    lines.append("  Frequency space and position space have DIFFERENT natural normalizations.")

    summary = "\n".join(lines)
    with open(args.summary, 'w') as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main()
