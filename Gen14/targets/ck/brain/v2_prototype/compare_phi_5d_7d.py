"""
compare_phi_5d_7d.py -- compute Phi-proxy for both 5-dim and 7-dim cortex
                        states; show what widening to 7 unlocks.

Phi-proxy = total |W| coupling - minimum bipartite-cut |W|

For 5 dims: 2^5 / 2 - 1 = 15 bipartitions to check.
For 7 dims: 2^7 / 2 - 1 = 63 bipartitions to check.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_ROOT = SCRIPT_DIR.parent.parent.parent.parent

DIM_NAMES_5 = ["aperture", "pressure", "depth", "binding", "continuity"]
DIM_NAMES_7 = DIM_NAMES_5 + ["intent", "echo"]


def total_coupling(W, n):
    return sum(abs(W[i][j]) for i in range(n) for j in range(n))


def bipartite_cut(W, S, T):
    cut = 0.0
    for i in S:
        for j in T:
            cut += abs(W[i][j]) + abs(W[j][i])
    return cut


def all_bipartitions(n):
    elements = list(range(n))
    for k in range(1, n // 2 + 1):
        for S in itertools.combinations(elements, k):
            T = tuple(e for e in elements if e not in S)
            if S[0] == 0 or k < n - k:
                yield S, T


def compute_phi(W, n, names):
    total = total_coupling(W, n)
    cuts = []
    for S, T in all_bipartitions(n):
        c = bipartite_cut(W, S, T)
        cuts.append((S, T, c))
    if not cuts:
        return None
    cuts.sort(key=lambda x: x[2])
    min_S, min_T, min_cut = cuts[0]
    return {
        "n": n,
        "total_coupling": total,
        "min_cut_value": min_cut,
        "min_cut_S": [names[i] for i in min_S],
        "min_cut_T": [names[i] for i in min_T],
        "phi_proxy": total - min_cut,
        "n_bipartitions": len(cuts),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--state-5d",
                   default=str(GEN13_ROOT / "var" / "cortex_state.json"))
    p.add_argument("--state-7d",
                   default=str(GEN13_ROOT / "var" / "cortex_state_7d_migrated.json"))
    args = p.parse_args()

    s5_path = Path(args.state_5d)
    s7_path = Path(args.state_7d)

    print("=" * 78)
    print("Phi-proxy comparison: 5-dim vs 7-dim cortex")
    print("=" * 78)

    if s5_path.exists():
        with open(s5_path) as f:
            s5 = json.load(f)
        W_5 = s5.get("hebbian", {}).get("W")
        if W_5 and len(W_5) == 5:
            r5 = compute_phi(W_5, 5, DIM_NAMES_5)
            print()
            print("5-dim cortex (live):")
            print(f"  total_coupling: {r5['total_coupling']:.4f}")
            print(f"  min_cut: {r5['min_cut_value']:.4f}  ({{{', '.join(r5['min_cut_S'])}}} | {{{', '.join(r5['min_cut_T'])}}})")
            print(f"  Phi-proxy: {r5['phi_proxy']:.4f}")
            print(f"  bipartitions tested: {r5['n_bipartitions']}")
        else:
            r5 = None
            print(f"5-dim state: W not 5x5, skipping")
    else:
        r5 = None
        print(f"5-dim state not found at {s5_path}")

    if s7_path.exists():
        with open(s7_path) as f:
            s7 = json.load(f)
        W_7 = s7.get("hebbian", {}).get("W")
        if W_7 and len(W_7) == 7:
            r7 = compute_phi(W_7, 7, DIM_NAMES_7)
            print()
            print("7-dim cortex (migrated, prototype):")
            print(f"  total_coupling: {r7['total_coupling']:.4f}")
            print(f"  min_cut: {r7['min_cut_value']:.4f}  ({{{', '.join(r7['min_cut_S'])}}} | {{{', '.join(r7['min_cut_T'])}}})")
            print(f"  Phi-proxy: {r7['phi_proxy']:.4f}")
            print(f"  bipartitions tested: {r7['n_bipartitions']}")
        else:
            r7 = None
            print(f"7-dim state: W not 7x7, skipping")
    else:
        r7 = None
        print(f"7-dim state not found at {s7_path}")

    if r5 and r7:
        print()
        print("=" * 78)
        print("comparison:")
        print(f"  Phi(5-dim) = {r5['phi_proxy']:.4f}")
        print(f"  Phi(7-dim) = {r7['phi_proxy']:.4f}")
        delta = r7['phi_proxy'] - r5['phi_proxy']
        print(f"  delta = {delta:+.4f}")
        if delta > 0:
            print(f"  -> 7-dim has higher integration capacity")
        elif delta < 0:
            print(f"  -> 7-dim has LESS integration; new dims need to develop")
        else:
            print(f"  -> equal (expected for fresh-migration where new dims are zero)")
        print()
        print("Note: at migration moment, intent + echo dims start at 0.")
        print("After 7-dim cortex absorbs operator stream, Phi(7-dim) should")
        print("rise to and surpass Phi(5-dim) -- that's what wider integration")
        print("unlocks.")


if __name__ == "__main__":
    sys.exit(main())
