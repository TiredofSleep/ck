#!/usr/bin/env python3
"""
k8_dirichlet_partial_sums.py — Study partial sums of A3(s) = Sigma_p Kl(1,1;p) * p^{-s}

Computes partial sums of A3 for real s > 3/2 (region of absolute convergence).
Also tests the log-weight variant: Ã3(s) = Sigma_p Kl(1,1;p) * log(p) * p^{-s}

Reports:
  (1) A3(s) partial sums at checkpoints for several values of s
  (2) Growth rate of |A3_X(s)| as X -> infinity
  (3) Comparison with Weil bound: A3(s) << 2 * Sigma_p p^{1/2-s} (absolute bound)
  (4) Cancellation ratio: |A3(s)| / absolute_bound (how much Sato-Tate cancellation occurs)

From K8_KLOOSTERMAN_DIRICHLET_SERIES.md:
  - A3(s) converges absolutely for Re(s) > 3/2 (K8.2)
  - Sato-Tate gives mean=0, so A3 converges faster than absolute bound (K8.4)
  - Conditional on Ramanujan, A3 may extend to Re(s) > 1 (C-tier)

Outputs:
    k8_dirichlet_partial_results.json
    k8_dirichlet_partial_summary.txt

Usage:
    python k8_dirichlet_partial_sums.py [--pmax 20000] [--s 1.6 1.8 2.0 2.5]
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


def kloosterman_11(p):
    """Kl(1,1;p) = sum_{k=1}^{p-1} cos(2pi(k+k^{-1})/p). Returns real value."""
    two_pi_over_p = 2 * math.pi / p
    total = 0.0
    for k in range(1, p):
        k_inv = pow(k, p - 2, p)
        total += math.cos(two_pi_over_p * (k + k_inv))
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pmax", type=int, default=5000)
    parser.add_argument("--s", nargs="+", type=float, default=[1.6, 1.8, 2.0, 2.5, 3.0],
                        help="Values of s to study (all > 3/2)")
    parser.add_argument("--out", default="k8_dirichlet_partial_results.json")
    parser.add_argument("--summary", default="k8_dirichlet_partial_summary.txt")
    args = parser.parse_args()

    # Validate s values
    s_vals = [s for s in args.s if s > 1.5]
    if len(s_vals) < len(args.s):
        print(f"[k8_partial] Warning: dropping s values <= 1.5 (outside convergence region)")
    print(f"[k8_partial] s values: {s_vals}")

    primes = primes_up_to(args.pmax)
    print(f"[k8_partial] {len(primes)} primes up to {args.pmax}")

    checkpoints = sorted(set([100, 500, 1000, 2000, 5000, 10000, args.pmax]))
    checkpoints = [c for c in checkpoints if c <= args.pmax]

    # Accumulators for each s
    A3 = {s: 0.0 for s in s_vals}
    A3_abs = {s: 0.0 for s in s_vals}   # absolute bound: sum |Kl| * p^{-s}
    A3_weil = {s: 0.0 for s in s_vals}  # Weil bound: sum 2*sqrt(p) * p^{-s}
    A3_log = {s: 0.0 for s in s_vals}   # log-weight variant: Ã3(s)

    records = {s: [] for s in s_vals}
    cp_idx = {s: 0 for s in s_vals}
    n_primes = 0

    for i, p in enumerate(primes):
        if i % 500 == 0:
            print(f"  p={p} ({i+1}/{len(primes)})")
        kl = kloosterman_11(p)
        kl_abs = abs(kl)
        logp = math.log(p)
        n_primes += 1

        for s in s_vals:
            p_pow = p ** (-s)
            A3[s] += kl * p_pow
            A3_abs[s] += kl_abs * p_pow
            A3_weil[s] += 2 * math.sqrt(p) * p_pow
            A3_log[s] += kl * logp * p_pow

            # Record at checkpoints
            if cp_idx[s] < len(checkpoints) and p >= checkpoints[cp_idx[s]]:
                canc_ratio = A3_abs[s] / A3_weil[s] if A3_weil[s] > 0 else float('nan')
                records[s].append({
                    "X": p,
                    "pi_X": n_primes,
                    "A3": A3[s],
                    "A3_abs_sum": A3_abs[s],
                    "A3_weil_bound": A3_weil[s],
                    "cancellation_ratio": canc_ratio,
                    "A3_log": A3_log[s],
                    "A3_per_A3_weil": abs(A3[s]) / A3_weil[s] if A3_weil[s] > 0 else float('nan'),
                })
                cp_idx[s] += 1

    # Save
    with open(args.out, 'w') as f:
        json.dump({
            "pmax": args.pmax,
            "s_values": s_vals,
            "records": {str(s): records[s] for s in s_vals},
        }, f, indent=2)

    # Summary
    lines = [
        "K8 A3(s) Dirichlet Partial Sums",
        "=" * 70,
        f"pmax = {args.pmax}, {n_primes} primes",
        f"A3(s) = Sigma_p Kl(1,1;p) * p^{{-s}}",
        "",
    ]

    for s in s_vals:
        final = records[s][-1] if records[s] else None
        lines.append(f"s = {s}:")
        lines.append(f"  {'X':>7}  {'A3(s)':>12}  {'|A3|/Weil':>12}  {'abs_sum':>12}  {'Weil_bound':>12}")
        lines.append("  " + "-" * 58)
        for r in records[s]:
            lines.append(
                f"  {r['X']:>7d}  {r['A3']:>12.6f}  {r['A3_per_A3_weil']:>12.6f}"
                f"  {r['A3_abs_sum']:>12.6f}  {r['A3_weil_bound']:>12.6f}"
            )
        if final:
            lines.append(f"  Final A3({s}) = {final['A3']:.8f}")
            lines.append(f"  Final Ã3({s}) = {final['A3_log']:.8f}  (log-weight)")
            lines.append(f"  Cancellation: |A3| / Weil_bound = {final['A3_per_A3_weil']:.4f}"
                         f"  (1.0 = no cancellation)")
        lines.append("")

    # Growth analysis
    if len(s_vals) >= 2 and all(records[s] for s in s_vals):
        lines.append("Growth analysis (final values at X = pmax):")
        for s in s_vals:
            final = records[s][-1] if records[s] else None
            if final:
                lines.append(f"  s={s:.1f}:  A3={final['A3']:.6f}  |A3|/Weil={final['A3_per_A3_weil']:.4f}")
        lines.append("")
        lines.append("  Cancellation ratio = |A3(s)| / Weil_bound_sum")
        lines.append("  Weil bound: sum 2*sqrt(p)*p^{-s} = 2*sum p^{1/2-s}")
        lines.append("  If Sato-Tate cancellation is active: ratio << 1")
        lines.append("  If NO cancellation: ratio approaches 1")

    lines.append("")
    lines.append("INTERPRETATION (K8_KLOOSTERMAN_DIRICHLET_SERIES.md):")
    lines.append("  A3(s) converges absolutely for Re(s) > 3/2 (Theorem K8.2).")
    lines.append("  Sato-Tate (Theorem K8.3): mean(alpha_p)=0, so cancellation occurs.")
    lines.append("  Cancellation ratio << 1 confirms Sato-Tate cancellation in practice.")
    lines.append("  A3 does NOT have an explicit formula — it is NOT Sigma rho X^rho/rho.")
    lines.append("  A3(s) for real s > 3/2 is a well-defined real number with arithmetic content.")
    lines.append("  The GL(2)-to-GL(1) bridge (K8_GL2_TO_GL1_BRIDGE.md) remains open.")

    summary = "\n".join(lines)
    with open(args.summary, 'w') as f:
        f.write(summary)
    print(summary)


if __name__ == "__main__":
    main()
