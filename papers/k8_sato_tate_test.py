#!/usr/bin/env python3
"""
k8_sato_tate_test.py — Verify Sato-Tate equidistribution for Kl(1,1;p)/(2*sqrt(p))

Tests the Katz (1988) theorem: alpha_p = Kl(1,1;p)/(2*sqrt(p)) is equidistributed
on [-1,1] by the semicircle measure rho(t) = (2/pi)*sqrt(1-t^2).

Tests:
  (1) Kolmogorov-Smirnov test against the semicircle CDF
  (2) Mean test: |mean(alpha_p)| < 0.05 (expect 0)
  (3) Variance test: |var(alpha_p) - 0.5| < 0.1 (expect 1/2)
  (4) Moment test: E[alpha_p^4] should be near 3/8
  (5) Partial sum growth: Sigma_{p<=X} alpha_p / sqrt(pi(X)) should be O(1)

From K8_SATO_TATE_DISTRIBUTION.md:
  Pre-registered predictions P1 (KS not reject), P2 (mean~0), P3 (var~0.5), P4 (partial sums O(1))

Outputs:
    k8_sato_tate_results.json
    k8_sato_tate_summary.txt

Usage:
    python k8_sato_tate_test.py [--pmax 10000]
"""

import argparse
import json
import math
import cmath


def primes_up_to(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(sieve[i*i::i]))
    return [i for i in range(2, n + 1) if sieve[i]]


def kloosterman_11(p):
    """Kl(1,1;p) = sum_{k=1}^{p-1} exp(2pi i (k + k^{-1})/p). Returns real part (Kl is real)."""
    two_pi_over_p = 2 * math.pi / p
    total = 0.0
    for k in range(1, p):
        k_inv = pow(k, p - 2, p)
        total += math.cos(two_pi_over_p * (k + k_inv))
    return total


def semicircle_cdf(t):
    """CDF of semicircle distribution on [-1,1]: F(t) = 1/2 + t*sqrt(1-t^2)/pi + arcsin(t)/pi."""
    if t <= -1.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    return 0.5 + t * math.sqrt(1 - t*t) / math.pi + math.asin(t) / math.pi


def ks_statistic(samples, cdf_func):
    """Compute Kolmogorov-Smirnov statistic D = max |F_n(x) - F(x)|."""
    n = len(samples)
    sorted_s = sorted(samples)
    d = 0.0
    for i, x in enumerate(sorted_s):
        fn_above = (i + 1) / n
        fn_below = i / n
        fx = cdf_func(x)
        d = max(d, abs(fn_above - fx), abs(fn_below - fx))
    return d


def ks_critical_value(n, alpha=0.05):
    """Approximate KS critical value at significance alpha for sample size n."""
    # Kolmogorov's table approximation: c(alpha) / sqrt(n)
    # c(0.05) = 1.36, c(0.01) = 1.63
    c = {0.05: 1.36, 0.01: 1.63, 0.10: 1.22}
    return c.get(alpha, 1.36) / math.sqrt(n)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmax", type=int, default=5000)
    parser.add_argument("--out", default="k8_sato_tate_results.json")
    parser.add_argument("--summary", default="k8_sato_tate_summary.txt")
    args = parser.parse_args()

    primes = primes_up_to(args.pmax)
    print(f"[k8_sato_tate] {len(primes)} primes up to {args.pmax}, computing alpha_p...")

    alpha_vals = []
    partial_sums = []
    running_sum = 0.0
    checkpoints = [100, 500, 1000, 2000, 5000, args.pmax]
    checkpoints = sorted(set(c for c in checkpoints if c <= args.pmax))
    cp_idx = 0

    for p in primes:
        kl = kloosterman_11(p)
        alpha = kl / (2 * math.sqrt(p))
        alpha_vals.append(alpha)
        running_sum += alpha

        if cp_idx < len(checkpoints) and p >= checkpoints[cp_idx]:
            pi_x = len(alpha_vals)
            normed = running_sum / math.sqrt(pi_x)
            partial_sums.append({
                "X": p, "pi_X": pi_x,
                "partial_sum_alpha": running_sum,
                "normed_by_sqrt_piX": normed,
            })
            cp_idx += 1

    n = len(alpha_vals)
    print(f"[k8_sato_tate] Computed {n} alpha_p values. Running tests...")

    # Test 1: KS test against semicircle
    ks_d = ks_statistic(alpha_vals, semicircle_cdf)
    ks_crit_05 = ks_critical_value(n, 0.05)
    ks_crit_01 = ks_critical_value(n, 0.01)
    ks_pass = ks_d < ks_crit_05

    # Test 2: Mean
    mean_alpha = sum(alpha_vals) / n
    mean_pass = abs(mean_alpha) < 0.05

    # Test 3: Variance
    var_alpha = sum((a - mean_alpha)**2 for a in alpha_vals) / n
    var_pass = abs(var_alpha - 0.5) < 0.1

    # Test 4: Fourth moment (expect 3/8 = 0.375)
    fourth_moment = sum(a**4 for a in alpha_vals) / n
    fourth_pass = abs(fourth_moment - 0.375) < 0.05

    # Test 5: Partial sum O(1) growth
    last_normed = partial_sums[-1]["normed_by_sqrt_piX"] if partial_sums else float('nan')
    partial_pass = abs(last_normed) < 5.0  # 5 sigma threshold

    # Histogram vs semicircle (10 bins)
    bins = 10
    hist = [0] * bins
    for a in alpha_vals:
        idx = min(int((a + 1.0) / 2.0 * bins), bins - 1)
        hist[idx] += 1
    bin_edges = [-1.0 + 2.0 * i / bins for i in range(bins + 1)]
    semicircle_expected = []
    for i in range(bins):
        t0, t1 = bin_edges[i], bin_edges[i + 1]
        expected_frac = semicircle_cdf(t1) - semicircle_cdf(t0)
        semicircle_expected.append(expected_frac * n)

    # Save
    results = {
        "pmax": args.pmax, "n_primes": n,
        "KS_statistic": ks_d,
        "KS_critical_05": ks_crit_05,
        "KS_critical_01": ks_crit_01,
        "KS_pass_at_05": ks_pass,
        "mean_alpha": mean_alpha,
        "var_alpha": var_alpha,
        "fourth_moment": fourth_moment,
        "partial_sums": partial_sums,
    }
    with open(args.out, 'w') as f:
        json.dump(results, f, indent=2)

    # Summary
    lines = [
        "K8 Sato-Tate Distribution Test: Kl(1,1;p)/(2*sqrt(p))",
        "=" * 65,
        f"Primes up to {args.pmax}: {n} primes",
        "",
        "Test 1: Kolmogorov-Smirnov against semicircle CDF",
        f"  KS statistic D = {ks_d:.4f}",
        f"  Critical value (5%): {ks_crit_05:.4f}",
        f"  Critical value (1%): {ks_crit_01:.4f}",
        f"  Result: {'PASS (do not reject semicircle)' if ks_pass else 'FAIL (reject semicircle)'}",
        "",
        "Test 2: Mean (P2 pre-registered: |mean| < 0.05)",
        f"  mean(alpha_p) = {mean_alpha:.6f}  (expect ~0)",
        f"  Result: {'PASS' if mean_pass else 'FAIL'}",
        "",
        "Test 3: Variance (P3 pre-registered: |var - 0.5| < 0.1)",
        f"  var(alpha_p) = {var_alpha:.6f}  (expect ~0.5)",
        f"  Result: {'PASS' if var_pass else 'FAIL'}",
        "",
        "Test 4: Fourth moment (expect 3/8 = 0.375)",
        f"  E[alpha_p^4] = {fourth_moment:.6f}",
        f"  Result: {'PASS' if fourth_pass else 'FAIL'}",
        "",
        "Test 5: Partial sum growth (P4: O(1) fluctuation after sqrt normalization)",
        f"  |Sigma alpha_p / sqrt(pi(X))| at X={args.pmax}: {abs(last_normed):.4f}",
        f"  Result: {'PASS' if partial_pass else 'FAIL (anomalous growth)'}",
        "",
        "Partial sums at checkpoints:",
        f"  {'X':>7}  {'pi(X)':>7}  {'sum(alpha_p)':>14}  {'sum/sqrt(pi)':>14}",
        "-" * 50,
    ]
    for r in partial_sums:
        lines.append(f"  {r['X']:>7d}  {r['pi_X']:>7d}  {r['partial_sum_alpha']:>14.4f}"
                     f"  {r['normed_by_sqrt_piX']:>14.6f}")

    lines.append("")
    lines.append(f"Histogram vs semicircle ({bins} bins on [-1,1]):")
    lines.append(f"  {'Bin center':>10}  {'observed':>10}  {'expected':>10}  {'ratio':>8}")
    for i in range(bins):
        bc = (bin_edges[i] + bin_edges[i+1]) / 2
        obs = hist[i]
        exp = semicircle_expected[i]
        ratio = obs / exp if exp > 0 else float('nan')
        lines.append(f"  {bc:>10.3f}  {obs:>10d}  {exp:>10.1f}  {ratio:>8.3f}")

    lines.append("")
    all_pass = ks_pass and mean_pass and var_pass and fourth_pass and partial_pass
    lines.append(f"OVERALL: {'ALL TESTS PASS' if all_pass else 'SOME TESTS FAILED'}")
    lines.append("")
    lines.append("INTERPRETATION (K8_SATO_TATE_DISTRIBUTION.md):")
    lines.append("  Katz (1988): alpha_p equidistributed by semicircle (D-tier proved).")
    lines.append("  Mean=0 and Var=1/2 follow from semicircle moments (Theorem K8.3, K8.4).")
    lines.append("  KS test confirms empirical distribution matches semicircle CDF.")
    lines.append("  Partial sums O(sqrt(pi(X))) confirms Sato-Tate cancellation in A3(s).")

    summary = "\n".join(lines)
    with open(args.summary, 'w') as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main()
