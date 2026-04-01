#!/usr/bin/env python3
"""
k7_character_probe.py — Probe correlation of D_p with character families

Tests whether D_p^PSD(xi) correlates with:
  (A) Additive character values: e^{2pi i a p / q} for small q
  (B) Multiplicative character values: Legendre symbol (p/q) for small primes q
  (C) Kloosterman sums: Kl(1, 1; p) = sum_{k=1}^{p-1} e^{2pi i (k + 1/k) / p}
  (D) Gauss sums: g(chi_2, p) = sum_{k=1}^{p-1} (k/p) e^{2pi i k/p}

From K7_MULTIPLICATIVE_CHARACTER_ROUTE.md:
  - Kloosterman sums carry genuine g-dependent prime-specific information
  - Gauss sums satisfy g(chi_2, p) = sqrt(p) * (-1)^{(p-1)/2 * ...} (known closed form)
  - Expected: Kloosterman sums will show O(sqrt(p)) structure; PSD-based D_p will NOT correlate

Outputs:
    k7_character_probe.json
    k7_character_summary.txt

Usage:
    python k7_character_probe.py [--pmax 5000] [--xi 0.5]
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
    return math.sin(math.pi * xi * (p - 1) / p) ** 2 / ((p - 1) ** 2 * math.sin(u) ** 2)


def D_p(xi, p):
    sp = psd_exact(xi, p)
    if math.isnan(sp):
        return float('nan')
    return p * (sp - sinc2(xi))


def D_leading(xi):
    return -2.0 * (sinc2(2 * xi) - sinc2(xi))


def legendre(a, p):
    """Legendre symbol (a/p). Returns 0, 1, or -1."""
    if a % p == 0:
        return 0
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def gauss_sum(p):
    """Quadratic Gauss sum: sum_{k=1}^{p-1} (k/p) e^{2pi i k/p}.
    Known: |g| = sqrt(p). Returns normalized value g/sqrt(p).
    """
    g = sum(legendre(k, p) * cmath.exp(2j * math.pi * k / p) for k in range(1, p))
    return g / math.sqrt(p)  # normalized to O(1)


def kloosterman(a, b, p):
    """Kloosterman sum Kl(a,b;p) = sum_{k=1}^{p-1} e^{2pi i (ak + b*k^{-1})/p}.
    Weil bound: |Kl| <= 2*sqrt(p). Returns normalized value Kl/(2*sqrt(p)).
    """
    kl = sum(cmath.exp(2j * math.pi * (a * k + b * pow(k, p - 2, p)) / p)
             for k in range(1, p))
    return kl / (2 * math.sqrt(p))  # normalized to [-1, 1]


def correlation(xs, ys):
    """Pearson correlation coefficient."""
    n = len(xs)
    if n < 2:
        return float('nan')
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx)**2 for x in xs))
    den_y = math.sqrt(sum((y - my)**2 for y in ys))
    if den_x < 1e-14 or den_y < 1e-14:
        return float('nan')
    return num / (den_x * den_y)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmax", type=int, default=2000)
    parser.add_argument("--xi", type=float, default=0.5)
    parser.add_argument("--out", default="k7_character_probe.json")
    parser.add_argument("--summary", default="k7_character_summary.txt")
    args = parser.parse_args()

    primes = primes_up_to(args.pmax)
    # Exclude very small primes (Kloosterman approximations rough there)
    primes = [p for p in primes if p >= 7]
    xi = args.xi
    lead = D_leading(xi)

    print(f"[k7_probe] xi={xi}, {len(primes)} primes (>=7), lead={lead:.6f}")

    # Compute for each prime
    dp_vals = []
    dp_resid = []
    gauss_re = []
    gauss_im = []
    kl_re = []
    kl_im = []
    kl_abs = []
    legendre3 = []  # Legendre (p/3)
    legendre5 = []  # Legendre (p/5)

    for p in primes:
        dp = D_p(xi, p)
        if math.isnan(dp):
            continue
        dp_vals.append(dp)
        dp_resid.append(dp - lead)

        g = gauss_sum(p)
        gauss_re.append(g.real)
        gauss_im.append(g.imag)

        kl = kloosterman(1, 1, p)
        kl_re.append(kl.real)
        kl_im.append(kl.imag)
        kl_abs.append(abs(kl))

        legendre3.append(float(legendre(p, 3)) if p != 3 else 0.0)
        legendre5.append(float(legendre(p, 5)) if p != 5 else 0.0)

    # Correlations
    corr_dp_gauss_re = correlation(dp_vals, gauss_re)
    corr_dp_gauss_im = correlation(dp_vals, gauss_im)
    corr_dp_kl_re = correlation(dp_vals, kl_re)
    corr_dp_kl_im = correlation(dp_vals, kl_im)
    corr_dp_kl_abs = correlation(dp_vals, kl_abs)
    corr_resid_gauss_re = correlation(dp_resid, gauss_re)
    corr_resid_kl_re = correlation(dp_resid, kl_re)
    corr_resid_kl_abs = correlation(dp_resid, kl_abs)
    corr_dp_leg3 = correlation(dp_vals, legendre3)
    corr_dp_leg5 = correlation(dp_vals, legendre5)

    # Intrinsic Kloosterman statistics
    kl_mean = sum(kl_re) / len(kl_re)
    kl_var = sum((x - kl_mean)**2 for x in kl_re) / len(kl_re)

    results = {
        "xi": xi, "pmax": args.pmax, "n_primes": len(primes),
        "D_leading": lead,
        "corr_dp_vs_gauss_Re": corr_dp_gauss_re,
        "corr_dp_vs_gauss_Im": corr_dp_gauss_im,
        "corr_dp_vs_kl_Re": corr_dp_kl_re,
        "corr_dp_vs_kl_Im": corr_dp_kl_im,
        "corr_dp_vs_kl_abs": corr_dp_kl_abs,
        "corr_resid_vs_gauss_Re": corr_resid_gauss_re,
        "corr_resid_vs_kl_Re": corr_resid_kl_re,
        "corr_resid_vs_kl_abs": corr_resid_kl_abs,
        "corr_dp_vs_legendre3": corr_dp_leg3,
        "corr_dp_vs_legendre5": corr_dp_leg5,
        "kl_mean_Re": kl_mean,
        "kl_var_Re": kl_var,
    }

    with open(args.out, 'w') as f:
        json.dump(results, f, indent=2)

    lines = [
        "K7 Character Probe Results",
        "=" * 60,
        f"xi = {xi:.4f},  {len(primes)} primes up to {args.pmax}",
        f"D_leading = {lead:.6f}",
        "",
        "Pearson correlations of D_p^PSD vs character families:",
        f"  D_p vs Gauss sum Re:         {corr_dp_gauss_re:>8.4f}",
        f"  D_p vs Gauss sum Im:         {corr_dp_gauss_im:>8.4f}",
        f"  D_p vs Kloosterman Re:       {corr_dp_kl_re:>8.4f}",
        f"  D_p vs Kloosterman Im:       {corr_dp_kl_im:>8.4f}",
        f"  D_p vs Kloosterman |Kl|:     {corr_dp_kl_abs:>8.4f}",
        f"  D_p vs Legendre (p/3):       {corr_dp_leg3:>8.4f}",
        f"  D_p vs Legendre (p/5):       {corr_dp_leg5:>8.4f}",
        "",
        "Residual (D_p - leading) correlations:",
        f"  resid vs Gauss sum Re:       {corr_resid_gauss_re:>8.4f}",
        f"  resid vs Kloosterman Re:     {corr_resid_kl_re:>8.4f}",
        f"  resid vs Kloosterman |Kl|:   {corr_resid_kl_abs:>8.4f}",
        "",
        "Kloosterman intrinsic statistics (independently verifying Weil):",
        f"  Kl(1,1;p)/2sqrt(p) mean Re:  {kl_mean:>8.4f}  (expected ~0)",
        f"  Kl(1,1;p)/2sqrt(p) var Re:   {kl_var:>8.4f}  (expected ~1/4)",
        "",
        "INTERPRETATION:",
    ]

    def sig(corr):
        return "SIGNIFICANT" if abs(corr) > 0.1 else "none"

    lines.append(f"  D_p vs Kloosterman: {sig(corr_dp_kl_re)}")
    lines.append(f"  D_p vs Gauss:       {sig(corr_dp_gauss_re)}")
    lines.append(f"  Resid vs Kloosterman: {sig(corr_resid_kl_re)}")
    lines.append("")
    lines.append("EXPECTED FINDING (from K7_MULTIPLICATIVE_CHARACTER_ROUTE.md):")
    lines.append("  D_p^PSD is the SET-based PSD correction — independent of generator g.")
    lines.append("  Kloosterman sums Kl(1,1;p) ARE g-dependent and prime-specific.")
    lines.append("  Therefore: LOW correlation between D_p^PSD and Kloosterman is expected.")
    lines.append("  If high correlation is found: needs investigation (unexpected signal).")
    lines.append("  The absence of correlation CONFIRMS the separation between PSD route and")
    lines.append("  character-sum route. See K7_MULTIPLICATIVE_CHARACTER_ROUTE.md for the")
    lines.append("  correct object (sequence-based D_p, not set-based PSD).")

    summary = "\n".join(lines)
    with open(args.summary, 'w') as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main()
