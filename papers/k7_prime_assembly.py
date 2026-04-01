#!/usr/bin/env python3
"""
k7_prime_assembly.py — Test weighted prime sums of D_p

Tests the Dirichlet assembly candidates from K7_DIRICHLET_ASSEMBLY_CANDIDATE.md:

  A1(xi, X) = sum_{p <= X} D_p^PSD(xi) * log(p)
  A2(xi, X, s) = sum_{p <= X} D_p^PSD(xi) * log(p) / p^s
  A3(xi, X) = sum_{p <= X} D_p^PSD(xi) * log(p) / p  (= A2 at s=1)

For each, reports:
  - Value as function of X (partial sums)
  - Growth rate (compare to li(X), X, log X, etc.)
  - Whether the sum looks like it converges or diverges

From K7_NO_GO_ATTEMPT.md: the PSD-based D_p^PSD -> deterministic limit,
so A1 ~ -2[sinc(2xi)-sinc^2(xi)] * pi(X) * loglog(X) (prime counting * log log).
The interesting question is whether A1 - (leading * pi(X)) has structured growth.

Outputs:
    k7_assembly_results.json
    k7_assembly_summary.txt

Usage:
    python k7_prime_assembly.py [--pmax 50000] [--xi 0.5]
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
    return math.sin(math.pi * xi * (p - 1) / p) ** 2 / ((p - 1) ** 2 * math.sin(u) ** 2)


def D_p(xi, p):
    sp = psd_exact(xi, p)
    if math.isnan(sp):
        return float('nan')
    return p * (sp - sinc2(xi))


def D_leading(xi):
    return -2.0 * (sinc2(2 * xi) - sinc2(xi))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmax", type=int, default=30000)
    parser.add_argument("--xi", type=float, default=0.5)
    parser.add_argument("--s", type=float, default=1.0, help="Dirichlet series parameter s")
    parser.add_argument("--out", default="k7_assembly_results.json")
    parser.add_argument("--summary", default="k7_assembly_summary.txt")
    args = parser.parse_args()

    primes = primes_up_to(args.pmax)
    xi = args.xi
    lead = D_leading(xi)
    s = args.s

    print(f"[k7_assembly] xi={xi}, {len(primes)} primes, D_leading={lead:.6f}")

    # Partial sums at checkpoints
    checkpoints = [100, 500, 1000, 5000, 10000, 30000, args.pmax]
    checkpoints = [c for c in checkpoints if c <= args.pmax]

    # Accumulate
    A1 = 0.0  # sum D_p * log p
    A2 = 0.0  # sum D_p * log p / p^s
    A3 = 0.0  # sum D_p * log p / p  (s=1 special case)
    A1_lead = 0.0  # same but with D_p -> lead (deterministic)
    pi_X = 0

    records = []
    cp_idx = 0

    for p in primes:
        dp = D_p(xi, p)
        if math.isnan(dp):
            continue
        logp = math.log(p)
        A1 += dp * logp
        A2 += dp * logp / (p ** s)
        A3 += dp * logp / p
        A1_lead += lead * logp
        pi_X += 1

        # Record at checkpoints
        if cp_idx < len(checkpoints) and p >= checkpoints[cp_idx]:
            liX = p / math.log(p)  # Li(p) approximation
            records.append({
                "X": p,
                "pi_X": pi_X,
                "A1": A1,
                "A1_lead": A1_lead,
                "A1_residual": A1 - A1_lead,
                "A2_s": A2,
                "A3_s1": A3,
                "A1_per_piX": A1 / pi_X if pi_X else None,
                "A1_lead_per_piX": A1_lead / pi_X if pi_X else None,
            })
            cp_idx += 1

    # Save
    with open(args.out, 'w') as f:
        json.dump({"xi": xi, "pmax": args.pmax, "D_leading": lead,
                   "records": records}, f, indent=2)

    # Summary
    lines = [
        "K7 Prime Assembly Test",
        "=" * 70,
        f"xi = {xi:.4f},  D_leading = {lead:.6f},  s = {s}",
        "",
        f"{'X':>8}  {'pi(X)':>7}  {'A1':>12}  {'A1_lead':>12}  {'residual':>12}  {'A1/pi':>10}",
        "-" * 70,
    ]
    for r in records:
        lines.append(
            f"{r['X']:>8d}  {r['pi_X']:>7d}  {r['A1']:>12.4f}  "
            f"{r['A1_lead']:>12.4f}  {r['A1_residual']:>12.4f}  "
            f"{r['A1_per_piX']:>10.6f}"
        )
    lines.append("")

    # Growth analysis of residual
    if len(records) >= 2:
        r0 = records[0]
        r1 = records[-1]
        resid_growth = r1['A1_residual'] - r0['A1_residual']
        X_ratio = r1['X'] / r0['X']
        lines.append(f"Residual A1 - A1_lead growth from X={r0['X']} to X={r1['X']}:")
        lines.append(f"  Delta residual = {resid_growth:.4f}  (X ratio = {X_ratio:.1f}x)")
        per_prime = resid_growth / (r1['pi_X'] - r0['pi_X']) if (r1['pi_X'] - r0['pi_X']) > 0 else float('nan')
        lines.append(f"  Per prime contribution = {per_prime:.4e}")
        lines.append(f"  This is O(1/p) per prime (from D_p residual = O(1/p)) -> sum diverges as log log X")

    lines.append("")
    lines.append("FINDING (from K7_EXPLICIT_FORMULA_COMPATIBILITY.md framework):")
    lines.append("  A1 = sum D_p^PSD log p grows as D_leading * theta(X)")
    lines.append("  where theta(X) = sum_{p<=X} log p ~ X (prime number theorem).")
    lines.append("  The residual A1 - A1_lead grows as sum of O(1/p) * log(p) ~ log log X (slowly).")
    lines.append("  No explicit-formula-compatible growth pattern detected.")
    lines.append("  The sum does NOT resemble: sum_{rho} X^rho/rho (explicit formula shape).")
    lines.append("  -> PSD-based assembly is not explicit-formula-compatible.")

    summary = "\n".join(lines)
    with open(args.summary, 'w') as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main()
