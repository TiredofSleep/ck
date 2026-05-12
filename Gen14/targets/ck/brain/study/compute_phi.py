"""
compute_phi.py -- compute integrated-information Phi proxy on CK's 5x5
                 cortex.

CK's thesis (papers/ck_thesis_2026_04_29/) Bridge 1 claims:
  "The harmony attractor in TIG serves a role similar to phi by maintaining
   integrated and coherent states."

This script gives him a NUMBER for that claim.  It computes a Phi-proxy
on the live cortex_state.json:

  Phi-proxy = (total |W| coupling) - (minimum bipartite-cut |W|)

Interpretation:
  - total |W| = how much the 5x5 cortex is connected
  - min cut = the minimum disconnect achievable by partitioning into
    2 groups; what survives "worst-case factoring"
  - Phi-proxy = the surviving integration that resists factorization

This is NOT Tononi 3.0 Phi exactly (which requires cause-effect
repertoires over all subsystems and minimum information partitions on
each).  It's a graph-theoretic proxy that captures the SAME intuition:
the part of the coupling that can't be broken by separating the system
into two non-interacting halves.

For 5 nodes there are 2^5/2 - 1 = 15 unique bipartitions.  Exact min-cut
is feasible.

Reference: Tononi 2008 (Φ as integrated information); IIT 3.0 Oizumi/
Albantakis/Tononi 2014.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_ROOT = SCRIPT_DIR.parent.parent.parent.parent
DEFAULT_STATE = GEN13_ROOT / "var" / "cortex_state.json"

DIM_NAMES = ["aperture", "pressure", "depth", "binding", "continuity"]


def total_coupling(W):
    """Sum of |W_ij| over all (i, j) including diagonal."""
    return sum(abs(W[i][j]) for i in range(5) for j in range(5))


def bipartite_cut(W, S, T):
    """Sum of |W_ij| where i in S and j in T (or vice versa)."""
    cut = 0.0
    for i in S:
        for j in T:
            cut += abs(W[i][j]) + abs(W[j][i])
    return cut


def all_bipartitions(n=5):
    """Yield all unique bipartitions (S, T) of {0..n-1}.  For n=5 there
    are 2^(n-1) - 1 = 15 bipartitions (treating (S, T) ~ (T, S))."""
    elements = list(range(n))
    for k in range(1, n // 2 + 1):
        for S in itertools.combinations(elements, k):
            T = tuple(e for e in elements if e not in S)
            # avoid duplicates: only yield with smaller-indexed element in S
            if S[0] == 0 or k < n - k:
                yield S, T


def compute_phi_proxy(W):
    """Compute the integrated-information proxy:
       Phi = (total coupling) - (minimum bipartite cut)
    """
    total = total_coupling(W)
    bipartitions = list(all_bipartitions(5))
    cuts = [(S, T, bipartite_cut(W, S, T)) for S, T in bipartitions]
    # Min cut = the easiest factorization
    min_cut_S, min_cut_T, min_cut = min(cuts, key=lambda x: x[2])
    phi = total - min_cut
    return {
        "total_coupling": total,
        "min_cut_pairs": (min_cut_S, min_cut_T),
        "min_cut_value": min_cut,
        "phi_proxy": phi,
        "all_cuts": [
            {
                "S": [DIM_NAMES[i] for i in S],
                "T": [DIM_NAMES[j] for j in T],
                "cut": round(c, 4),
            }
            for S, T, c in sorted(cuts, key=lambda x: x[2])
        ],
    }


def effective_information_proxy(W):
    """Effective information proxy: 1 - (rank-1 approximation residual / total).

    If the cortex W matrix can be approximated well by a rank-1 outer product
    (one dominant mode), the system is factorizable and EI is low.  If
    multiple comparable singular values, EI is high.

    Computes top 2 singular values (no numpy required if we use a small power
    iteration; for now just use sum of |eigenvalues|).
    """
    # Use sum of squares of W entries as Frobenius norm squared
    frobenius_sq = sum(W[i][j] ** 2 for i in range(5) for j in range(5))
    # Approximate top singular value by max row norm (lower bound)
    # for proxy purposes
    max_row_norm_sq = max(sum(W[i][j] ** 2 for j in range(5)) for i in range(5))
    if frobenius_sq < 1e-12:
        return 0.0
    # EI proxy: 1 - (top mode fraction); higher = more integrated
    top_mode_frac = max_row_norm_sq / frobenius_sq
    return 1.0 - top_mode_frac


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--state-path", default=str(DEFAULT_STATE))
    args = p.parse_args()

    state_path = Path(args.state_path)
    if not state_path.exists():
        print(f"cortex state not found: {state_path}", file=sys.stderr)
        return 2

    with open(state_path) as f:
        state = json.load(f)

    W = state.get("hebbian", {}).get("W")
    if not W or len(W) != 5 or len(W[0]) != 5:
        print(f"unexpected W shape: {len(W) if W else None}x{len(W[0]) if W else None}", file=sys.stderr)
        return 3

    print("=" * 70)
    print("CK cortex Phi-proxy (test of thesis Bridge 1)")
    print("=" * 70)
    print()
    print(f"  cortex_state: {state_path.name}")
    print(f"  tick: {state.get('state', {}).get('tick')}")
    print()
    print(f"  W matrix (5x5 Hebbian):")
    for i, row in enumerate(W):
        print(f"    {DIM_NAMES[i]:<10}: " + ", ".join(f"{w:+.4f}" for w in row))
    print()

    result = compute_phi_proxy(W)
    print(f"  Total coupling (sum |W_ij|): {result['total_coupling']:.4f}")
    print(f"  Minimum bipartite cut: {result['min_cut_value']:.4f}")
    cut_S = "{" + ", ".join(DIM_NAMES[i] for i in result['min_cut_pairs'][0]) + "}"
    cut_T = "{" + ", ".join(DIM_NAMES[i] for i in result['min_cut_pairs'][1]) + "}"
    print(f"  Easiest factor: {cut_S} | {cut_T}")
    print()
    print(f"  >>>  PHI-PROXY  =  {result['phi_proxy']:.4f}  <<<")
    print()
    print(f"  Interpretation: the surviving integration that resists")
    print(f"  the worst-case factorization of CK's 5-dim cortex.")
    print(f"  Higher = more integrated, more 'phi-like'.")
    print()

    print("  All 15 bipartite cuts (sorted, smallest first):")
    for c in result['all_cuts']:
        s_str = "{" + ",".join(c['S']) + "}"
        t_str = "{" + ",".join(c['T']) + "}"
        print(f"    cut={c['cut']:6.4f}  {s_str:30s} | {t_str}")
    print()

    ei = effective_information_proxy(W)
    print(f"  Effective Information proxy (1 - top-mode frac): {ei:.4f}")
    print(f"  Higher = more multi-modal coupling; less rank-1 reducible.")
    print()
    print("=" * 70)
    print("Bridge 1 status (CK thesis):")
    print("  The Phi-proxy is now a real number CK can compute on himself.")
    print("  Repeated study sessions will show Phi changing as W changes.")
    print(f"  Current snapshot: Phi-proxy = {result['phi_proxy']:.4f}")
    print(f"                    EI-proxy  = {ei:.4f}")
    print("=" * 70)


if __name__ == "__main__":
    sys.exit(main())
