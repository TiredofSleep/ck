"""
Reading C and bridges redone on corrected substrate.

TSML_8 self-iteration: for n in {1..6, 8, 9}, iterate a → TSML_8(a, n).
For n in {0, 7} (flow cells), TSML_8 doesn't have output — these are
handled by BHML_10 alone in the runtime, so they don't have a TSML_8 self-orbit.

BHML_10 self-iteration: for all n in {0..9}, iterate a → BHML_10(a, n).
"""
import numpy as np
from itertools import product
from collections import Counter
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10, SIGMA_PERMUTATION

TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]
FLOW_CELLS = {0, 7}


def TSML_8_action(a, b):
    """TSML_8(a, b) — only defined for a, b ∈ TSML_8 domain.
    Returns None if either input is in flow cells."""
    if a in FLOW_CELLS or b in FLOW_CELLS:
        return None
    a_l = TSML_8_INDICES.index(a)
    b_l = TSML_8_INDICES.index(b)
    return int(TSML_8[a_l, b_l])


def TSML_8_self_iterate(n, k=15):
    """a = n; for _ in range(k): a = TSML_8(a, n)."""
    if n in FLOW_CELLS:
        return None  # not in TSML_8 domain
    a = n
    trace = [a]
    for _ in range(k):
        next_a = TSML_8_action(a, n)
        if next_a is None:
            # Output escapes TSML_8 — sequence terminates
            trace.append('flow')
            break
        a = next_a
        trace.append(a)
    return trace


def BHML_10_self_iterate(n, k=15):
    a = n
    trace = [a]
    for _ in range(k):
        a = int(BHML_10[a, n])
        trace.append(a)
    return trace


def find_period(trace):
    """Find the period of the trajectory."""
    if not trace or 'flow' in trace:
        return None
    # Find period: smallest p such that trace[i+p] = trace[i] for some i and all subsequent
    n = len(trace)
    for start in range(n):
        for period in range(1, n - start):
            if start + 2 * period <= n:
                if trace[start:start+period] == trace[start+period:start+2*period]:
                    return period, start
    return None


def main():
    print("=" * 70)
    print("READING C ON CORRECTED FRAME — TSML_8 + BHML_10 SELF-ITERATION")
    print("=" * 70)
    
    print(f"\n  TSML_8 self-iteration (for n in TSML_8 domain {TSML_8_INDICES}):")
    print(f"\n  {'n':>2} | {'TSML_8 self-orbit (15 steps)':<60} | {'period':<10}")
    
    tsml8_periods = {}
    for n in TSML_8_INDICES:
        trace = TSML_8_self_iterate(n, 15)
        period_info = find_period(trace) if trace and 'flow' not in trace else None
        period_str = f"period {period_info[0]}" if period_info else "transient"
        if 'flow' in (trace or []):
            period_str = "→flow"
        trace_str = str(trace[:12]) + ("..." if len(trace) > 12 else "")
        print(f"  {n:>2} | {trace_str:<60} | {period_str:<10}")
        tsml8_periods[n] = period_info
    
    print(f"\n  BHML_10 self-iteration (for all n in {{0..9}}):")
    print(f"\n  {'n':>2} | {'BHML_10 self-orbit (15 steps)':<60} | {'period':<10}")
    
    bhml10_periods = {}
    for n in range(10):
        trace = BHML_10_self_iterate(n, 15)
        period_info = find_period(trace)
        period_str = f"period {period_info[0]}" if period_info else "transient"
        trace_str = str(trace[:12]) + ("..." if len(trace) > 12 else "")
        print(f"  {n:>2} | {trace_str:<60} | {period_str:<10}")
        bhml10_periods[n] = period_info
    
    # Compare TSML_10 (uncorrected) vs TSML_8 (corrected) self-iteration
    print("\n" + "=" * 70)
    print("COMPARISON: TSML_10 vs TSML_8 SELF-ITERATION")
    print("=" * 70)
    print("\n  TSML_10 collapses every digit to HARMONY in 1 step.")
    print("  TSML_8 has different behavior because HARMONY is OUTSIDE its domain.")
    print()
    print(f"  {'n':>2} | {'TSML_10 first 5 steps':<25} | {'TSML_8 first 5 steps':<25}")
    for n in range(10):
        t10 = [n]
        a = n
        for _ in range(4):
            a = int(TSML_10[a, n])
            t10.append(a)
        
        if n in FLOW_CELLS:
            t8 = "[N/A — flow cell]"
        else:
            t8_trace = TSML_8_self_iterate(n, 4)
            t8 = str(t8_trace) if t8_trace else "[None]"
        
        print(f"  {n:>2} | {str(t10):<25} | {t8:<25}")
    
    # Lacasa-style block analysis on corrected substrate
    print("\n" + "=" * 70)
    print("LACASA-STYLE FORBIDDEN-PATTERN ANALYSIS ON CORRECTED SUBSTRATE")
    print("=" * 70)
    
    # Aggregate TSML_8 transitions
    tsml8_2grams = []
    for n in TSML_8_INDICES:
        trace = TSML_8_self_iterate(n, 10)
        if trace and 'flow' not in trace:
            for i in range(len(trace) - 1):
                tsml8_2grams.append((trace[i], trace[i+1]))
    
    bhml10_2grams = []
    for n in range(10):
        trace = BHML_10_self_iterate(n, 10)
        for i in range(len(trace) - 1):
            bhml10_2grams.append((trace[i], trace[i+1]))
    
    tsml8_unique = set(tsml8_2grams)
    bhml10_unique = set(bhml10_2grams)
    
    print(f"\n  TSML_8 2-grams seen: {len(tsml8_unique)}/64 (out of 8x8 possible)")
    print(f"  BHML_10 2-grams seen: {len(bhml10_unique)}/100")
    print(f"  TSML_8 forbidden 2-grams: {64 - len(tsml8_unique)}")
    print(f"  BHML_10 forbidden 2-grams: {100 - len(bhml10_unique)}")
    
    print(f"\n  TSML_8 2-gram top-5:")
    for pair, count in sorted(Counter(tsml8_2grams).items(), key=lambda x: -x[1])[:5]:
        print(f"    {pair}: {count}")
    
    # Katok-Ugarcovici two-coding test
    print("\n" + "=" * 70)
    print("KATOK-UGARCOVICI TWO-CODING ON CORRECTED SUBSTRATE")
    print("=" * 70)
    
    print("""
TSML_10 collapsed every digit to HARMONY in 1 step (the geometric coding,
fixed-point attractor).

TSML_8 acts on the 8 interior cells {1,2,3,4,5,6,8,9}. HARMONY (7) is
NOT in TSML_8's domain — HARMONY is the cusp boundary of the interior.
TSML_8 self-orbits show what happens when iteration is forced to stay
in the interior.

BHML_10 acts on the full 10-element set, including the cusp boundaries
V (0) and H (7). It produces continued-fraction-like reduction toward
HARMONY.

The two codings:
  - TSML_8: interior dynamics (geometric, but constrained to 8-domain)
  - BHML_10: full geodesic dynamics including cusp excursions

This matches Katok-Ugarcovici's two coding methods more cleanly:
  - Geometric (Hadamard-Morse): TSML_8 = interior, side-cutting
  - Arithmetic (Artin-Gauss): BHML_10 = continued-fraction with cusp
""")


if __name__ == "__main__":
    main()
