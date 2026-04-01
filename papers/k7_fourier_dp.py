#!/usr/bin/env python3
"""
k7_fourier_dp.py — Spectral decomposition of D_p in xi

For each prime p, computes D_p^PSD(xi) = p * (S_p(xi) - sinc^2(xi)) across a
dense xi grid, then takes the Fourier transform of D_p as a function of xi.

Goal: determine whether D_p(xi) as a function of xi has structured dominant
frequencies, or whether it looks like a smooth deterministic curve.

Expected finding from K7_EXACT_FORMULA_FOR_RP.md:
  D_p^PSD(xi) -> -2[sinc(2xi) - sinc^2(xi)]  (deterministic, no prime-specific oscillation)
The Fourier transform of the leading term is:
  F[-2(sinc(2xi) - sinc^2(xi))] = -2(tri(t/2)/2 - tri(t)) = tri(t) - tri(t/2)
  (using F[sinc^2(xi)] = tri(t) and F[sinc(2xi)] = (1/2)tri(t/2) scaled)

If D_p has additional cross-prime structure, it would appear as prime-specific peaks
in the Fourier transform that are NOT in the deterministic leading term.

Outputs:
    k7_fourier_dp.json
    k7_fourier_summary.txt

Usage:
    python k7_fourier_dp.py [--pmax 10000] [--nxi 512]
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


def D_leading(xi):
    """Deterministic leading limit of D_p^PSD."""
    return -2.0 * (sinc2(2 * xi) - sinc2(xi))


def dft(vals):
    """Naive DFT (for small arrays). Returns magnitudes."""
    n = len(vals)
    result = []
    for k in range(n // 2):
        s = sum(v * cmath.exp(-2j * math.pi * k * j / n) for j, v in enumerate(vals))
        result.append(abs(s) / n)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmax", type=int, default=5000)
    parser.add_argument("--nxi", type=int, default=128)
    parser.add_argument("--out", default="k7_fourier_dp.json")
    parser.add_argument("--summary", default="k7_fourier_summary.txt")
    args = parser.parse_args()

    primes = primes_up_to(args.pmax)
    nxi = args.nxi
    # xi grid: (0, 3) range, evenly spaced
    xi_vals = [3.0 * (i + 0.5) / nxi for i in range(nxi)]

    print(f"[k7_fourier] {len(primes)} primes, {nxi} xi points")

    # Compute D_p(xi) and leading limit for each prime
    leading = [D_leading(xi) for xi in xi_vals]
    leading_dft = dft(leading)

    # For each prime: D_p(xi), residual = D_p - leading, and their DFTs
    all_dp = []
    all_residual = []

    for p in primes:
        dp_row = []
        resid_row = []
        for xi in xi_vals:
            sp = psd_exact(xi, p)
            if math.isnan(sp):
                sp = sinc2(xi)  # fill with limit at singularity
            dp = p * (sp - sinc2(xi))
            lead = D_leading(xi)
            dp_row.append(dp)
            resid_row.append(dp - lead)
        all_dp.append(dp_row)
        all_residual.append(resid_row)

    # Average DFT of D_p across primes
    n_freq = nxi // 2
    avg_dp_dft = [0.0] * n_freq
    avg_resid_dft = [0.0] * n_freq
    for dp_row, resid_row in zip(all_dp, all_residual):
        dp_freq = dft(dp_row)
        resid_freq = dft(resid_row)
        for k in range(n_freq):
            avg_dp_dft[k] += dp_freq[k]
            avg_resid_dft[k] += resid_freq[k]
    n = len(primes)
    avg_dp_dft = [v / n for v in avg_dp_dft]
    avg_resid_dft = [v / n for v in avg_resid_dft]

    # Save
    with open(args.out, 'w') as f:
        json.dump({
            "pmax": args.pmax, "nxi": nxi,
            "xi_grid": xi_vals[:20],
            "leading_dft": leading_dft[:20],
            "avg_dp_dft": avg_dp_dft[:20],
            "avg_residual_dft": avg_resid_dft[:20],
        }, f, indent=2)

    # Summary
    top_leading = sorted(range(n_freq), key=lambda k: -leading_dft[k])[:5]
    top_resid = sorted(range(n_freq), key=lambda k: -avg_resid_dft[k])[:5]

    lines = [
        "K7 Fourier Analysis of D_p^PSD",
        "=" * 60,
        f"pmax={args.pmax}, nxi={nxi}",
        "",
        "Leading deterministic term dominant frequencies:",
    ]
    for k in top_leading:
        freq = k * 3.0 / nxi
        lines.append(f"  k={k:4d}  xi-freq={freq:.3f}  amplitude={leading_dft[k]:.4e}")
    lines.append("")
    lines.append("Average residual (D_p - leading) dominant frequencies:")
    for k in top_resid:
        freq = k * 3.0 / nxi
        lines.append(f"  k={k:4d}  xi-freq={freq:.3f}  amplitude={avg_resid_dft[k]:.4e}")

    lines.append("")
    lines.append("INTERPRETATION:")
    lines.append("  If avg_residual_dft has amplitude << leading_dft: residual is noise,")
    lines.append("  no prime-specific oscillation structure detected.")
    lines.append("  If avg_residual_dft peaks at unexpected frequencies: possible arithmetic signal.")
    lines.append("")
    # Compare magnitudes
    max_lead = max(leading_dft) if leading_dft else 1.0
    max_resid = max(avg_resid_dft) if avg_resid_dft else 0.0
    ratio = max_resid / max_lead if max_lead > 0 else float('inf')
    lines.append(f"  max(leading_dft) = {max_lead:.4e}")
    lines.append(f"  max(resid_dft)   = {max_resid:.4e}")
    lines.append(f"  ratio            = {ratio:.4e}")
    if ratio < 0.05:
        lines.append("  FINDING: residual is < 5% of leading term — consistent with NO prime-specific structure.")
    else:
        lines.append(f"  FINDING: residual is {ratio*100:.1f}% of leading term — investigate further.")

    summary = "\n".join(lines)
    with open(args.summary, 'w') as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main()
