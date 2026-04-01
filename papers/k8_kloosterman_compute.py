#!/usr/bin/env python3
"""
k8_kloosterman_compute.py — Compute Kl(1,1;p) for primes up to N

Computes:
    Kl(1,1;p) = sum_{k=1}^{p-1} exp(2pi i (k + k^{-1})/p)
    alpha_p = Kl(1,1;p) / (2*sqrt(p))   (normalized, in [-1,1] by Weil)

Outputs:
    k8_kloosterman_raw.json      -- raw values for all primes
    k8_kloosterman_summary.txt   -- statistics + comparison to Weil bound

From K8_KLOOSTERMAN_DIRICHLET_SERIES.md:
    - Weil bound: |Kl(1,1;p)| <= 2*sqrt(p) (proved, D-tier)
    - Sato-Tate: alpha_p equidistributed by semicircle (proved, D-tier, Katz 1988)
    - Expected: mean(alpha_p) near 0, var(alpha_p) near 1/2

Usage:
    python k8_kloosterman_compute.py [--pmax 10000] [--out k8_kloosterman_raw.json]
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
    """
    Kl(1,1;p) = sum_{k=1}^{p-1} exp(2pi i (k + k^{-1})/p)
    k^{-1} = modular inverse of k mod p = pow(k, p-2, p) by Fermat's little theorem.
    """
    two_pi_i_over_p = 2j * math.pi / p
    total = 0.0 + 0j
    for k in range(1, p):
        k_inv = pow(k, p - 2, p)
        total += cmath.exp(two_pi_i_over_p * (k + k_inv))
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmax", type=int, default=5000)
    parser.add_argument("--out", default="k8_kloosterman_raw.json")
    parser.add_argument("--summary", default="k8_kloosterman_summary.txt")
    args = parser.parse_args()

    primes = primes_up_to(args.pmax)
    print(f"[k8_kl] Computing Kl(1,1;p) for {len(primes)} primes up to {args.pmax}...")

    records = []
    alpha_vals = []
    weil_violations = 0

    for i, p in enumerate(primes):
        if i % 100 == 0:
            print(f"  p={p} ({i+1}/{len(primes)})")
        kl = kloosterman_11(p)
        kl_re = kl.real
        kl_abs = abs(kl)
        weil = 2 * math.sqrt(p)
        alpha = kl_re / weil  # normalized; note: Kl(1,1;p) is REAL (it equals its conjugate
                               # because k and k^{-1} pair up: k -> p-k maps k^{-1} -> -(k^{-1}),
                               # so imaginary part cancels). Verify below.
        alpha_im = kl.imag / weil  # should be near 0

        if kl_abs > weil + 1e-6:
            weil_violations += 1

        alpha_vals.append(alpha)
        records.append({
            "p": p,
            "Kl_re": round(kl_re, 6),
            "Kl_im": round(kl.imag, 6),
            "Kl_abs": round(kl_abs, 6),
            "weil_bound": round(weil, 6),
            "alpha": round(alpha, 8),
            "alpha_im": round(alpha_im, 8),
            "weil_ratio": round(kl_abs / weil, 6),
        })

    # Statistics
    n = len(alpha_vals)
    mean_alpha = sum(alpha_vals) / n
    var_alpha = sum((a - mean_alpha)**2 for a in alpha_vals) / n
    max_alpha = max(alpha_vals)
    min_alpha = min(alpha_vals)
    max_abs_alpha = max(abs(a) for a in alpha_vals)

    # Check imaginary part (should be ~0 for all primes, as Kl(1,1;p) is real)
    max_im = max(abs(r["Kl_im"]) for r in records)

    # Save
    with open(args.out, 'w') as f:
        json.dump({
            "pmax": args.pmax,
            "n_primes": len(primes),
            "stats": {
                "mean_alpha": mean_alpha,
                "var_alpha": var_alpha,
                "max_alpha": max_alpha,
                "min_alpha": min_alpha,
                "max_abs_alpha": max_abs_alpha,
                "weil_violations": weil_violations,
                "max_Kl_im": max_im,
            },
            "records": records,
        }, f, indent=2)
    print(f"[k8_kl] Saved to {args.out}")

    # Summary text
    lines = [
        "K8 Kloosterman Sums: Kl(1,1;p) Raw Computation",
        "=" * 65,
        f"Primes up to {args.pmax}:  {len(primes)} primes",
        "",
        "Statistics of alpha_p = Kl(1,1;p) / (2*sqrt(p)):",
        f"  Mean (expect ~0):        {mean_alpha:>10.6f}",
        f"  Variance (expect ~0.5):  {var_alpha:>10.6f}",
        f"  Max:                     {max_alpha:>10.6f}",
        f"  Min:                     {min_alpha:>10.6f}",
        f"  Max |alpha_p|:           {max_abs_alpha:>10.6f}  (Weil: <=1.0)",
        "",
        "Weil bound check:",
        f"  Violations (|Kl|>2sqrt(p)): {weil_violations}  (expected 0)",
        "",
        "Reality check (Kl(1,1;p) should be REAL):",
        f"  Max |Im(Kl)|: {max_im:.3e}  (expected ~0 up to float precision)",
        "",
    ]

    # Sample of extreme values
    sorted_by_alpha = sorted(records, key=lambda r: r["alpha"])
    lines.append("Smallest alpha_p (most negative Kloosterman):")
    for r in sorted_by_alpha[:5]:
        lines.append(f"  p={r['p']:>7d}  Kl={r['Kl_re']:>10.4f}  alpha={r['alpha']:>8.5f}"
                     f"  Weil_ratio={r['weil_ratio']:.4f}")
    lines.append("")
    lines.append("Largest alpha_p (most positive Kloosterman):")
    for r in sorted_by_alpha[-5:]:
        lines.append(f"  p={r['p']:>7d}  Kl={r['Kl_re']:>10.4f}  alpha={r['alpha']:>8.5f}"
                     f"  Weil_ratio={r['weil_ratio']:.4f}")
    lines.append("")

    # Interpretation
    lines.append("INTERPRETATION (K8_KLOOSTERMAN_DIRICHLET_SERIES.md):")
    lines.append("  Weil bound |Kl(1,1;p)| <= 2*sqrt(p) is proved (Theorem K8.1).")
    lines.append("  Mean(alpha_p) -> 0: zero bias (Theorem K8.4, from Sato-Tate).")
    lines.append("  Var(alpha_p) -> 1/2: semicircle distribution (Theorem K8.3).")
    lines.append("  Kl(1,1;p) is REAL for all primes (complete sum over symmetric pairs).")
    lines.append("  g-independence: same values regardless of primitive root choice.")
    lines.append("")
    passed = (weil_violations == 0 and
              abs(mean_alpha) < 0.05 and
              abs(var_alpha - 0.5) < 0.1 and
              max_im < 1e-3)
    if passed:
        lines.append("STATUS: ALL PRE-REGISTERED PREDICTIONS CONFIRMED (P1, P2, P3 from K8_SATO_TATE).")
    else:
        lines.append("STATUS: ANOMALY DETECTED — check computation.")
        if weil_violations > 0:
            lines.append(f"  VIOLATION: {weil_violations} primes exceed Weil bound!")
        if abs(mean_alpha) >= 0.05:
            lines.append(f"  BIAS: mean={mean_alpha:.4f}, expected ~0")
        if abs(var_alpha - 0.5) >= 0.1:
            lines.append(f"  VARIANCE ANOMALY: var={var_alpha:.4f}, expected ~0.5")

    summary = "\n".join(lines)
    with open(args.summary, 'w') as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main()
