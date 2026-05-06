#!/usr/bin/env python3
"""
Sprint 18 -- Operator-to-observable conjecture: empirical baseline scan.

Conjecture (informal): each fundamental physical observable corresponds
to a specific operator from {0, 1, ..., 9} via small-integer terms of
the form OPERATOR^k / |Z/10|^m, with small-denominator rational
multiplicities.

Falsifiability test: for each well-measured fundamental constant outside
the dark-sector trinity fit, scan small-integer (OPERATOR, k, m,
multiplier) tuples and report:
  (a) whether ANY tuple lies within 1 sigma of the measured value
  (b) what fraction of the tuple search space matches at 1 sigma
      (the "look-elsewhere" baseline)
  (c) the best matching tuple's residual

The conjecture is supported only when the per-observable matches survive
correction for look-elsewhere effects across the full constellation.

Usage:
  python3 verify_operator_observable_baseline.py
"""

OPERATORS = list(range(10))   # {0, 1, ..., 9}
N = 10                         # |Z/10|


def scan_one(value, value_err, k_max=4, m_max=12, multiplier_num_max=20,
             multiplier_den_max=20, allow_one_minus=True):
    """Scan small-integer (op, k, m, p, q, mode) tuples for matches.

    For each (op, k, m, p, q, mode):
      mode = 'plain' :  (p/q) * op**k / N**m
      mode = 'one_minus':  1 - (p/q) * op**k / N**m
    Filter: tuple matches if abs(form - value) < value_err.
    """
    hits = []
    total = 0
    for op in OPERATORS:
        for k in range(0, k_max + 1):
            for m in range(0, m_max + 1):
                for p in range(1, multiplier_num_max + 1):
                    for q in range(1, multiplier_den_max + 1):
                        total += 1
                        try:
                            base = (p / q) * (op ** k) / (N ** m) if op > 0 or k == 0 else 0
                        except ZeroDivisionError:
                            continue
                        for mode in (('plain', base),
                                     ('one_minus', 1 - base) if allow_one_minus else None):
                            if mode is None:
                                continue
                            tag, val = mode
                            if abs(val - value) < value_err:
                                hits.append((op, k, m, p, q, tag, val))
    return hits, total


def main():
    print("=" * 78)
    print("Sprint 18 -- Operator-to-observable conjecture: baseline scan")
    print("=" * 78)
    print()
    print("Search space: OPERATOR in {0..9}, k in 0..4, m in 0..12,")
    print("              multiplier p/q with p, q in 1..20,")
    print("              two forms each: (p/q)*OP^k/N^m  and  1 - (p/q)*OP^k/N^m")
    print()

    # Observables to test, all OUTSIDE the dark-sector trinity fit.
    targets = [
        # name,                value,                error,                k_max, m_max
        ("n_s (spectral idx)", 0.9649,               0.0042,               4, 12),
        ("eta_b (baryon-photon)", 6.10e-10,          0.06e-10,             4, 12),
        ("alpha (fine str.)", 1.0/137.036,           1e-9,                 4, 12),
        ("m_e/m_p",            5.4462e-4,            1e-7,                 4, 12),
        ("m_mu/m_e",           206.768,              1e-3,                 4, 12),
        ("D/H (BBN)",          2.527e-5,             0.030e-5,             4, 12),
        ("sigma_8",            0.811,                0.006,                4, 12),
        ("Hubble tension dH/H", 0.05,                0.01,                 4, 12),
    ]

    print(f"{'Observable':<24}{'Total':>10}{'Hits':>8}{'Rate':>8}  {'Best fit':<24}{'Resid.':<8}")
    print("-" * 78)
    summary = []
    for name, val, err, kmax, mmax in targets:
        hits, total = scan_one(val, err, k_max=kmax, m_max=mmax)
        rate_pct = 100.0 * len(hits) / total if total else 0.0
        if hits:
            # Best by smallest residual
            best = min(hits, key=lambda t: abs(t[6] - val))
            op, k, m, p, q, tag, fv = best
            resid_pct = (fv - val) / val * 100.0 if val != 0 else 0
            if tag == "one_minus":
                desc = f"1 - ({p}/{q})*{op}^{k}/{N}^{m}"
            else:
                desc = f"({p}/{q})*{op}^{k}/{N}^{m}"
            summary.append((name, len(hits), rate_pct, desc, resid_pct))
            print(f"{name:<24}{total:>10}{len(hits):>8}{rate_pct:>7.2f}%  "
                  f"{desc:<24}{resid_pct:>+7.3f}%")
        else:
            print(f"{name:<24}{total:>10}{0:>8}{0:>7.2f}%  "
                  f"{'(no match)':<24}{'--':<8}")

    print()
    print("=" * 78)
    print("Interpretation")
    print("=" * 78)
    print()
    print("If the conjecture is structural, we expect each observable to")
    print("admit at least one (operator, k, m, p, q) tuple matching within")
    print("1 sigma -- and the look-elsewhere rate to be small enough that")
    print("the constellation of matches is unlikely under the null")
    print("hypothesis 'small-integer formulas hit fundamental constants'.")
    print()
    print("  - HIGH rate (> 10%): the family is too rich; per-observable")
    print("    matches are fittable, not predictive. The conjecture fails")
    print("    falsifiability at this scope and needs further structural")
    print("    constraints (e.g., the operator selection function omitted in")
    print("    the present scan).")
    print("  - LOW rate (< 0.1%) for any individual observable: small.")
    print("    The fact that the family can hit at all is informative,")
    print("    and the specific tuple has structural meaning to chase.")
    print("  - The 'best fit' column above shows the closest tuple to the")
    print("    measured value; structural plausibility of these tuples")
    print("    (whether they use specific operators in expected ways)")
    print("    is a separate, qualitative judgment.")
    print()
    print("The dark-sector trinity sits in this family with:")
    print("    Omega_b   = HARMONY^2/N^3      (op=7, k=2, m=3, p/q=1/1)")
    print("    Omega_L   = (2*HARMONY^3+1)/N^3 (op=7, k=3 + op=H^0=1, m=3)")
    print("    Omega_DM = 264/1000             (op-mixed: BHML+sigma)")
    print("    n_s      = 1 - HARMONY/(2*N^2)  (op=7, k=1, m=2, p/q=1/2)")
    print("None of these used the data outside the dark-sector trinity to")
    print("fit; their look-elsewhere baselines (where computed) range from")
    print("the unique exact-closure (H,N,a)=(7,10,+1) for the trinity to")
    print("the ~2.4% baseline for n_s.")
    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
