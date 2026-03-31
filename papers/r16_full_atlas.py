"""
r16_full_atlas.py
=================
Complete permutation of finite multiplication algebras mod b.

For every semiprime b up to b_max AND every valid alphabet size k in [2, b-1]:
  - Exact algebraic invariants (no sampling, no approximation)
  - Ternary composition: +1/0/-1 fractions
  - Submatrix structure: CC, CG, GC, GG blocks
  - Unit group order (Euler totient), interleave score
  - Identifies the "native" k = b-1 (full coprime region before wrap)
  - Identifies first-G event (k where |G| first > 0)

Output:
  results/atlas/full_atlas.json    — complete dataset
  results/atlas/summary.csv        — one row per (b,k)
  results/atlas/invariants.png     — big picture invariant plots
  results/atlas/ternary_map_*.png  — ternary composition panels per prime family

Also runs extended gate-rate sweep (optional, --gate) for all semiprimes at
key k values using greedy descent at n_steps=500 (deeper than the 100-step test).

Usage:
    python r16_full_atlas.py                    # algebraic survey only, b<=200
    python r16_full_atlas.py --b_max 500        # full up to 500
    python r16_full_atlas.py --gate --b_max 100 # + gate rates (slow)
    python r16_full_atlas.py --visuals          # generate atlas figures

Author: Brayden Sanders / 7Site LLC | Sprint 4 (March 2026)
DOI: 10.5281/zenodo.18852047
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

import argparse
import csv
import json
import os
import time
from math import gcd
from itertools import product as iproduct
from collections import defaultdict

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# ═══════════════════════════════════════════════════════════════════════════════
#  PRIME / SEMIPRIME UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def sieve(n):
    """Return list of primes <= n."""
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n+1, i):
                is_p[j] = False
    return [i for i in range(2, n+1) if is_p[i]]


def factorize_semiprime(b, primes):
    """
    Return (p, q, is_square) where b = p*q, p <= q, both prime.
    Returns (None, None, False) if b is not a semiprime.
    """
    for p in primes:
        if p * p > b:
            break
        if b % p == 0:
            q = b // p
            if q in prime_set:
                return p, q, (p == q)
    return None, None, False


def euler_totient_semiprime(p, q):
    """phi(b) for b = p*q."""
    if p == q:
        return p * (p - 1)
    return (p - 1) * (q - 1)


# ═══════════════════════════════════════════════════════════════════════════════
#  ALGEBRAIC INVARIANTS FOR (b, k)
# ═══════════════════════════════════════════════════════════════════════════════

def compute_invariants(b, k, p, q):
    """
    Compute all exact algebraic invariants for alphabet {1..k} mod b.
    Returns a dict of scalars — everything is exact.
    """
    # Partition
    C = [x for x in range(1, k+1) if gcd(x, b) == 1]
    G = [x for x in range(1, k+1) if gcd(x, b) > 1]
    nC, nG = len(C), len(G)

    # Build multiplication table
    T = np.zeros((k, k), dtype=np.int32)
    for i in range(1, k+1):
        for j in range(1, k+1):
            T[i-1][j-1] = (i * j) % b

    # Classify every cell
    n_unit = 0   # +1: output is a unit (coprime with b)
    n_zero = 0   # -1: output is 0 mod b
    n_mid  = 0   #  0: output is non-unit, non-zero
    for i in range(k):
        for j in range(k):
            v = int(T[i, j])
            if v == 0:
                n_zero += 1
            elif gcd(v, b) == 1:
                n_unit += 1
            else:
                n_mid += 1
    total = k * k

    # Submatrix analysis: CC, CG, GC, GG blocks
    c_idx = [x-1 for x in C]
    g_idx = [x-1 for x in G]

    def block_counts(rows, cols):
        """unit/zero/mid counts in a submatrix defined by row/col index lists."""
        u = z = m = 0
        for r in rows:
            for c in cols:
                v = int(T[r, c])
                if v == 0:
                    z += 1
                elif gcd(v, b) == 1:
                    u += 1
                else:
                    m += 1
        return u, z, m

    cc_u, cc_z, cc_m = block_counts(c_idx, c_idx)
    cg_u, cg_z, cg_m = block_counts(c_idx, g_idx)
    gc_u, gc_z, gc_m = block_counts(g_idx, c_idx)
    gg_u, gg_z, gg_m = block_counts(g_idx, g_idx)

    cc_n = nC * nC
    cg_n = nC * nG
    gg_n = nG * nG

    # Interleave score: C/G transitions in sequence 1..k
    seq = [1 if x in set(C) else 0 for x in range(1, k+1)]
    transitions = sum(1 for i in range(len(seq)-1) if seq[i] != seq[i+1])
    min_cg = min(nC, nG) if nC > 0 and nG > 0 else 1
    interleave = transitions / (2 * min_cg) if min_cg > 0 else 0.0

    # First G event: is this the k where |G| just became 1?
    # (k is the first_G event if k is the smallest prime factor of b, or its multiple)
    smallest_prime_factor = min(p, q)

    # Euler totient of b
    phi_b = euler_totient_semiprime(p, q)

    # Unit group coverage: how many of the phi_b totient residues are in C
    unit_group_coverage = nC / phi_b if phi_b > 0 else 0.0

    return {
        "b": b, "p": p, "q": q, "is_square": int(p == q),
        "k": k, "phi_b": phi_b,
        "nC": nC, "nG": nG, "unit_frac": nC / k,
        "n_unit": n_unit, "n_zero": n_zero, "n_mid": n_mid,
        "unit_density":   n_unit / total,
        "zero_density":   n_zero / total,
        "nonunit_density": n_mid  / total,
        "interleave": round(interleave, 4),
        "unit_group_coverage": round(unit_group_coverage, 4),
        # CC block (C×C): should be high-unit (group closure)
        "cc_unit_frac": cc_u / cc_n if cc_n > 0 else None,
        "cc_zero_frac": cc_z / cc_n if cc_n > 0 else None,
        # GG block (G×G): should have zeros (the danger zone)
        "gg_zero_frac": gg_z / gg_n if gg_n > 0 else None,
        "gg_unit_frac": gg_u / gg_n if gg_n > 0 else None,
        # CG block (C×G): mixed
        "cg_unit_frac": cg_u / cg_n if cg_n > 0 else None,
        "cg_zero_frac": cg_z / cg_n if cg_n > 0 else None,
        "smallest_prime_factor": smallest_prime_factor,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  FULL SWEEP: ALL SEMIPRIMES × ALL k
# ═══════════════════════════════════════════════════════════════════════════════

def run_full_atlas(b_max, k_hard_max=None):
    """
    Enumerate all semiprimes b <= b_max, all k in [2, b-1].
    Returns list of invariant dicts.
    """
    global prime_set
    primes = sieve(b_max)
    prime_set = set(primes)

    semiprimes = []
    for b in range(4, b_max + 1):
        p, q, is_sq = factorize_semiprime(b, primes)
        if p is not None:
            semiprimes.append((b, p, q, is_sq))

    print(f"Found {len(semiprimes)} semiprimes up to b={b_max}")
    print(f"Computing invariants for all (b, k) pairs...")

    results = []
    total_pairs = sum(b - 2 for b, _, _, _ in semiprimes)
    if k_hard_max:
        total_pairs = sum(min(b-1, k_hard_max) - 1 for b, _, _, _ in semiprimes)
    print(f"Total (b, k) pairs: {total_pairs:,}")

    t0 = time.time()
    done = 0
    for b, p, q, is_sq in semiprimes:
        k_end = b - 1 if k_hard_max is None else min(b - 1, k_hard_max)
        for k in range(2, k_end + 1):
            row = compute_invariants(b, k, p, q)
            results.append(row)
            done += 1
            if done % 5000 == 0:
                elapsed = time.time() - t0
                rate = done / elapsed
                print(f"  {done:,} / {total_pairs:,}  ({rate:.0f}/s)  b={b} k={k}")

    elapsed = time.time() - t0
    print(f"Done: {len(results):,} rows in {elapsed:.1f}s  ({len(results)/elapsed:.0f}/s)")
    return results, semiprimes


# ═══════════════════════════════════════════════════════════════════════════════
#  SAVE TO JSON + CSV
# ═══════════════════════════════════════════════════════════════════════════════

def save_results(results, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    # JSON
    json_path = os.path.join(save_dir, "full_atlas.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {json_path}  ({os.path.getsize(json_path)//1024} KB)")

    # CSV
    csv_path = os.path.join(save_dir, "summary.csv")
    if results:
        fieldnames = list(results[0].keys())
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Saved: {csv_path}  ({os.path.getsize(csv_path)//1024} KB)")


# ═══════════════════════════════════════════════════════════════════════════════
#  ANALYSIS: KEY LAWS FROM FULL PERMUTATION
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_atlas(results):
    """
    Extract patterns from the full permutation.
    Print key findings.
    """
    print(f"\n{'='*70}")
    print("FULL ATLAS ANALYSIS")
    print(f"{'='*70}")
    print(f"Total (b,k) pairs: {len(results):,}")

    # Group by (p,q) structure
    by_pq_type = defaultdict(list)
    for r in results:
        key = ("square" if r["is_square"] else
               f"{r['p']}×{r['q']}" if r["p"] <= 5 else "large")
        by_pq_type[key].append(r)

    # Law 1: CC block unit fraction
    # Theorem: C is closed under multiplication mod b iff all CC outputs are units
    print("\n--- CC BLOCK: Unit group closure ---")
    cc_violations = [r for r in results if r["cc_unit_frac"] is not None
                     and r["cc_unit_frac"] < 1.0]
    if not cc_violations:
        print("  PROVED: CC block is ALWAYS 100% unit. C is closed under * mod b.")
        print(f"  (verified across {sum(1 for r in results if r['cc_unit_frac'] is not None):,} cases)")
    else:
        print(f"  VIOLATION found: {len(cc_violations)} cases where CC has non-units")
        for r in cc_violations[:5]:
            print(f"    b={r['b']} k={r['k']} cc_unit_frac={r['cc_unit_frac']:.3f}")

    # Law 2: GG block zero fraction
    print("\n--- GG BLOCK: Absorption zone ---")
    gg_rows = [r for r in results if r["gg_zero_frac"] is not None]
    if gg_rows:
        zero_fracs = [r["gg_zero_frac"] for r in gg_rows]
        print(f"  GG zero fraction: min={min(zero_fracs):.3f}  max={max(zero_fracs):.3f}"
              f"  mean={sum(zero_fracs)/len(zero_fracs):.3f}")
        pure_zero_gg = [r for r in gg_rows if r["gg_zero_frac"] == 1.0]
        print(f"  GG = pure zeros (100%): {len(pure_zero_gg)} cases")
        zero_gg = [r for r in gg_rows if r["gg_zero_frac"] == 0.0]
        print(f"  GG = no zeros at all:   {len(zero_gg)} cases")

    # Law 3: Interleave vs unit density
    print("\n--- INTERLEAVE vs GATE DIFFICULTY ---")
    rows_with_G = [r for r in results if r["nG"] > 0]
    high_il = [r for r in rows_with_G if r["interleave"] >= 0.9]
    low_il  = [r for r in rows_with_G if r["interleave"] <= 0.2]
    if high_il:
        hi_ud = sum(r["unit_density"] for r in high_il) / len(high_il)
        print(f"  High interleave (>=0.9): n={len(high_il)}  avg unit_density={hi_ud:.3f}")
    if low_il:
        lo_ud = sum(r["unit_density"] for r in low_il) / len(low_il)
        print(f"  Low  interleave (<=0.2): n={len(low_il)}  avg unit_density={lo_ud:.3f}")

    # Law 4: Zero density vs (p,q) structure
    print("\n--- ZERO DENSITY BY SEMIPRIME TYPE ---")
    # Perfect squares (p=q) vs distinct (p≠q)
    squares  = [r for r in results if r["is_square"]]
    distinct = [r for r in results if not r["is_square"]]
    if squares:
        sq_zd = sum(r["zero_density"] for r in squares) / len(squares)
        print(f"  Perfect squares (b=p²): n={len(squares)}  avg zero_density={sq_zd:.4f}")
    if distinct:
        di_zd = sum(r["zero_density"] for r in distinct) / len(distinct)
        print(f"  Distinct products (b=p×q): n={len(distinct)}  avg zero_density={di_zd:.4f}")

    # Law 5: Unit group coverage → convergence as k → b-1
    print("\n--- UNIT GROUP COVERAGE AT k=b-1 (native alphabet) ---")
    native = [r for r in results if r["k"] == r["b"] - 1]
    if native:
        coverages = [r["unit_group_coverage"] for r in native]
        at_full = [r for r in native if r["unit_group_coverage"] >= 1.0]
        print(f"  Native k=b-1 worlds: {len(native)}")
        print(f"  Coverage range: {min(coverages):.3f} – {max(coverages):.3f}")
        print(f"  Worlds with full coverage (100%): {len(at_full)}")

    # Law 6: First-G threshold
    print("\n--- FIRST G EVENT: smallest prime factor ---")
    by_spf = defaultdict(list)
    for r in results:
        by_spf[r["smallest_prime_factor"]].append(r)
    for spf in sorted(by_spf.keys())[:8]:
        rows = by_spf[spf]
        n_with_G = sum(1 for r in rows if r["nG"] > 0 and r["k"] == r["smallest_prime_factor"])
        print(f"  spf={spf}: {len(rows)} (b,k) pairs  |  "
              f"first-G at k=spf: {n_with_G} worlds")

    # Print extremes
    print("\n--- EXTREMES ---")
    # Highest zero density
    top_zero = sorted(results, key=lambda r: r["zero_density"], reverse=True)[:5]
    print("  Highest zero density:")
    for r in top_zero:
        print(f"    b={r['b']:3d} k={r['k']:3d}  zero_density={r['zero_density']:.4f}"
              f"  nC={r['nC']} nG={r['nG']}")
    # Lowest unit density with nG>0
    with_G = [r for r in results if r["nG"] > 0]
    if with_G:
        bot_unit = sorted(with_G, key=lambda r: r["unit_density"])[:5]
        print("  Lowest unit density (with G>0):")
        for r in bot_unit:
            print(f"    b={r['b']:3d} k={r['k']:3d}  unit_density={r['unit_density']:.4f}"
                  f"  nC={r['nC']} nG={r['nG']}")


# ═══════════════════════════════════════════════════════════════════════════════
#  VISUALS: FULL ATLAS FIGURES
# ═══════════════════════════════════════════════════════════════════════════════

CMAP_TERNARY = mcolors.LinearSegmentedColormap.from_list(
    "ternary",
    [(0.0, "#c0392b"), (0.5, "#f5f5f5"), (1.0, "#1a4f7a")]
) if HAS_MPL else None


def plot_unit_density_full(results, semiprimes, save_dir):
    """
    Complete unit density heatmap for all semiprimes × all k.
    Group by prime pair (p, q) on y-axis, k on x-axis.
    """
    if not HAS_MPL:
        return

    # Only show up to k=30 for readability
    k_show = 30
    b_list = [b for b, _, _, _ in semiprimes]

    # Index by (b, k)
    lookup = {(r["b"], r["k"]): r["unit_density"] for r in results}

    k_vals = list(range(2, k_show + 1))
    data = np.full((len(b_list), len(k_vals)), np.nan)
    for ri, (b, p, q, is_sq) in enumerate(semiprimes):
        for ci, k in enumerate(k_vals):
            if k < b:
                v = lookup.get((b, k))
                if v is not None:
                    data[ri, ci] = v

    fig, ax = plt.subplots(figsize=(max(14, len(k_vals)*0.5),
                                     max(8, len(b_list)*0.25)))
    im = ax.imshow(data, cmap="RdYlGn", vmin=0, vmax=1,
                   aspect="auto", interpolation="nearest")
    plt.colorbar(im, ax=ax, label="Unit density (fraction of cells with unit output)")

    ax.set_xticks(range(len(k_vals)))
    ax.set_xticklabels([str(k) for k in k_vals], fontsize=6, rotation=45)
    ax.set_xlabel("Alphabet size k", fontsize=9)

    b_labels = []
    for b, p, q, is_sq in semiprimes:
        label = f"b={b}({p}²)" if is_sq else f"b={b}({p}×{q})"
        b_labels.append(label)
    ax.set_yticks(range(len(b_list)))
    ax.set_yticklabels(b_labels, fontsize=5)
    ax.set_title("Unit Density: ALL semiprimes × k (Red=hard gate, Green=easy gate)",
                 fontsize=11, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(save_dir, "atlas_unit_density_full.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    print(f"Saved: {path}")
    plt.close(fig)


def plot_ternary_composition_full(results, semiprimes, save_dir):
    """
    Three-panel ternary composition map: +1/0/-1 fractions, all semiprimes × k.
    """
    if not HAS_MPL:
        return

    k_show = 30
    b_list = [b for b, _, _, _ in semiprimes]
    k_vals = list(range(2, k_show + 1))

    def get_data(field):
        lookup = {(r["b"], r["k"]): r[field] for r in results}
        data = np.full((len(b_list), len(k_vals)), np.nan)
        for ri, (b, _, _, _) in enumerate(semiprimes):
            for ci, k in enumerate(k_vals):
                if k < b:
                    v = lookup.get((b, k))
                    if v is not None:
                        data[ri, ci] = v
        return data

    d_plus  = get_data("unit_density")
    d_mid   = get_data("nonunit_density")
    d_minus = get_data("zero_density")

    b_labels = [f"b={b}({'sq' if is_sq else f'{p}×{q}'})"
                for b, p, q, is_sq in semiprimes]

    fig, axes = plt.subplots(1, 3, figsize=(max(20, len(k_vals)*1.5),
                                             max(8, len(b_list)*0.25)))
    fig.suptitle("Ternary Composition: ALL semiprimes × k  (+1 unit / 0 non-unit / -1 zero)",
                 fontsize=12, fontweight="bold")

    panels = [
        (d_plus,  "Blues",  "+1 (unit / coherent)"),
        (d_mid,   "Greys",  "0 (non-unit / entangled)"),
        (d_minus, "Reds",   "-1 (zero / absorbed)"),
    ]
    for ax, (data, cmap, title) in zip(axes, panels):
        im = ax.imshow(data, cmap=cmap, vmin=0, vmax=1,
                       aspect="auto", interpolation="nearest")
        plt.colorbar(im, ax=ax, label="fraction of k² cells")
        ax.set_xticks(range(len(k_vals)))
        ax.set_xticklabels([str(k) for k in k_vals], fontsize=5, rotation=45)
        ax.set_yticks(range(len(b_list)))
        ax.set_yticklabels(b_labels, fontsize=4)
        ax.set_title(title, fontsize=9)

    plt.tight_layout()
    path = os.path.join(save_dir, "atlas_ternary_full.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    print(f"Saved: {path}")
    plt.close(fig)


def plot_zero_density_by_spf(results, save_dir):
    """
    Zero density grouped by smallest prime factor — reveals prime-family bands.
    """
    if not HAS_MPL:
        return

    spf_vals = sorted(set(r["smallest_prime_factor"] for r in results))
    k_max = max(r["k"] for r in results)
    k_vals = list(range(2, min(k_max + 1, 31)))

    fig, axes = plt.subplots(1, len(spf_vals), figsize=(4 * len(spf_vals), 5),
                              sharey=True)
    if len(spf_vals) == 1:
        axes = [axes]

    fig.suptitle("Zero density by smallest prime factor — prime family bands",
                 fontsize=11, fontweight="bold")

    for ax, spf in zip(axes, spf_vals):
        fam = [r for r in results if r["smallest_prime_factor"] == spf]
        b_vals = sorted(set(r["b"] for r in fam))
        lookup = {(r["b"], r["k"]): r["zero_density"] for r in fam}

        data = np.full((len(b_vals), len(k_vals)), np.nan)
        for ri, b in enumerate(b_vals):
            for ci, k in enumerate(k_vals):
                if k < b:
                    v = lookup.get((b, k))
                    if v is not None:
                        data[ri, ci] = v

        im = ax.imshow(data, cmap="Reds", vmin=0, vmax=0.5,
                       aspect="auto", interpolation="nearest")
        ax.set_title(f"spf={spf}\n({len(b_vals)} worlds)", fontsize=9)
        ax.set_xticks(range(0, len(k_vals), 5))
        ax.set_xticklabels([str(k_vals[i]) for i in range(0, len(k_vals), 5)], fontsize=7)
        ax.set_yticks(range(len(b_vals)))
        ax.set_yticklabels([str(b) for b in b_vals], fontsize=5)

    plt.tight_layout()
    path = os.path.join(save_dir, "atlas_zero_by_spf.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    print(f"Saved: {path}")
    plt.close(fig)


def plot_cc_closure_check(results, save_dir):
    """
    CC block unit fraction: should be 1.0 everywhere (group closure law).
    Plot deviation from 1.0 to expose any violations.
    """
    if not HAS_MPL:
        return

    k_show = 30
    semiprimes_seen = sorted(set((r["b"], r["p"], r["q"], r["is_square"])
                                  for r in results), key=lambda x: x[0])
    b_list = [b for b, _, _, _ in semiprimes_seen]
    k_vals = list(range(2, k_show + 1))

    lookup = {(r["b"], r["k"]): r["cc_unit_frac"] for r in results
              if r["cc_unit_frac"] is not None}

    data = np.full((len(b_list), len(k_vals)), np.nan)
    for ri, (b, _, _, _) in enumerate(semiprimes_seen):
        for ci, k in enumerate(k_vals):
            v = lookup.get((b, k))
            if v is not None:
                data[ri, ci] = v

    # Deviation from 1.0
    dev = 1.0 - data

    fig, ax = plt.subplots(figsize=(max(14, len(k_vals)*0.5),
                                     max(8, len(b_list)*0.25)))
    im = ax.imshow(dev, cmap="Reds", vmin=0, vmax=0.1,
                   aspect="auto", interpolation="nearest")
    plt.colorbar(im, ax=ax, label="Deviation from 1.0 (0 = perfect closure)")
    ax.set_xticks(range(len(k_vals)))
    ax.set_xticklabels([str(k) for k in k_vals], fontsize=6, rotation=45)
    ax.set_xlabel("k", fontsize=9)
    b_labels = [f"b={b}" for b, _, _, _ in semiprimes_seen]
    ax.set_yticks(range(len(b_list)))
    ax.set_yticklabels(b_labels, fontsize=5)
    ax.set_title("CC block closure: deviation from 100% unit\n"
                 "All-white = proved: C is always closed under * mod b",
                 fontsize=10, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(save_dir, "atlas_cc_closure.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    print(f"Saved: {path}")
    plt.close(fig)


def plot_interleave_map(results, save_dir):
    """
    Interleave score across (b, k) space.
    Shows how deeply the coprime/non-coprime elements interleave as k grows.
    """
    if not HAS_MPL:
        return

    k_show = 30
    semiprimes_seen = sorted(set((r["b"], r["p"], r["q"], r["is_square"])
                                  for r in results), key=lambda x: x[0])
    b_list = [b for b, _, _, _ in semiprimes_seen]
    k_vals = list(range(2, k_show + 1))

    lookup = {(r["b"], r["k"]): r["interleave"] for r in results}

    data = np.full((len(b_list), len(k_vals)), np.nan)
    for ri, (b, _, _, _) in enumerate(semiprimes_seen):
        for ci, k in enumerate(k_vals):
            if k < b:
                v = lookup.get((b, k))
                if v is not None:
                    data[ri, ci] = v

    fig, ax = plt.subplots(figsize=(max(14, len(k_vals)*0.5),
                                     max(8, len(b_list)*0.25)))
    im = ax.imshow(data, cmap="viridis", vmin=0, vmax=1,
                   aspect="auto", interpolation="nearest")
    plt.colorbar(im, ax=ax, label="Interleave score (1.0 = maximal interleave)")
    ax.set_xticks(range(len(k_vals)))
    ax.set_xticklabels([str(k) for k in k_vals], fontsize=6, rotation=45)
    ax.set_xlabel("k", fontsize=9)
    b_labels = [f"b={b}({'sq' if is_sq else f'{p}×{q}'})"
                for b, p, q, is_sq in semiprimes_seen]
    ax.set_yticks(range(len(b_list)))
    ax.set_yticklabels(b_labels, fontsize=5)
    ax.set_title("Interleave score: C/G mixing as k grows\n"
                 "Yellow=max interleave (force field strength), Dark=block pattern",
                 fontsize=10, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(save_dir, "atlas_interleave_map.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    print(f"Saved: {path}")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  EXTENDED GATE SWEEP (optional, --gate flag)
# ═══════════════════════════════════════════════════════════════════════════════

import random as _random

def _gate_objective(T, k, b):
    gate_score = har_col = g_stay = 0
    for i in range(k):
        for j in range(k):
            v = int(T[i, j])
            if gcd(v, b) == 1:
                gate_score += 1
                if v == T[i, i]:
                    har_col += 1
        if int(T[i, i]) != 0 and gcd(int(T[i, i]), b) > 1:
            g_stay += 1
    n = k * k
    return (0.5 * gate_score / n +
            0.25 * har_col / n +
            0.25 * (1 - g_stay / k))


def _gate_trial(args):
    """Module-level worker — picklable for multiprocessing on Windows."""
    b, k, n_steps, seed = args
    rng = _random.Random(seed)
    perm = rng.sample(list(range(1, k+1)), k)
    T_cur = np.zeros((k, k), dtype=np.int32)
    for i in range(k):
        for j in range(k):
            T_cur[i][j] = (perm[i] * perm[j]) % b

    score = _gate_objective(T_cur, k, b)
    for _ in range(n_steps):
        a, bb2 = rng.randrange(k), rng.randrange(k)
        T_new = T_cur.copy()
        T_new[[a, bb2]] = T_new[[bb2, a]]
        T_new[:, [a, bb2]] = T_new[:, [bb2, a]]
        ns = _gate_objective(T_new, k, b)
        if ns >= score:
            T_cur = T_new
            score = ns

    gate_score = sum(1 for i in range(k) for j in range(k)
                     if gcd(int(T_cur[i, j]), b) == 1)
    return gate_score / (k * k) >= 0.85


def run_gate_sweep(semiprimes, k_values, n_trials, n_steps, n_workers, save_dir):
    """
    Extended gate rate test: deeper (n_steps=500), wider (all semiprimes).
    Uses same greedy descent as r16_gate_law_real_b.py but on full semiprime set.
    """
    from multiprocessing import Pool

    print(f"\nExtended gate sweep: n_steps={n_steps}, n_trials={n_trials}")
    print(f"Semiprimes: {len(semiprimes)}, k values: {k_values}")

    gate_results = []
    for b, p, q, is_sq in semiprimes:
        for k in k_values:
            if k >= b:
                continue
            C = [x for x in range(1, k+1) if gcd(x, b) == 1]
            G = [x for x in range(1, k+1) if gcd(x, b) > 1]
            if not G:
                continue  # No G — trivially gated

            trial_args = [(b, k, n_steps, seed) for seed in range(n_trials)]
            with Pool(n_workers) as pool:
                outcomes = pool.map(_gate_trial, trial_args)

            gate_rate = sum(outcomes) / n_trials
            row = {
                "b": b, "p": p, "q": q,
                "k": k, "nG": len(G), "nC": len(C),
                "unit_frac": len(C)/k,
                "gate_rate": round(gate_rate, 4),
                "n_trials": n_trials, "n_steps": n_steps,
            }
            gate_results.append(row)
            print(f"  b={b:3d}({p}×{q}) k={k:2d} |G|={len(G)} "
                  f"gate_rate={gate_rate:.3f}")

    path = os.path.join(save_dir, "gate_sweep_deep.json")
    os.makedirs(save_dir, exist_ok=True)
    with open(path, "w") as f:
        json.dump(gate_results, f, indent=2)
    print(f"Saved: {path}")
    return gate_results


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Full permutation atlas of finite multiplication algebras")
    parser.add_argument("--b_max",    type=int, default=200,
                        help="Upper bound for b (default 200)")
    parser.add_argument("--k_max",    type=int, default=None,
                        help="Hard cap on k (default: b-1 for each b)")
    parser.add_argument("--save_dir", type=str, default="results/atlas")
    parser.add_argument("--visuals",  action="store_true",
                        help="Generate atlas visualization figures")
    parser.add_argument("--gate",     action="store_true",
                        help="Run extended gate sweep (slow)")
    parser.add_argument("--gate_b_max", type=int, default=100)
    parser.add_argument("--gate_k",   type=int, nargs="+", default=[9, 15, 21])
    parser.add_argument("--gate_trials", type=int, default=2000)
    parser.add_argument("--gate_steps",  type=int, default=500)
    parser.add_argument("--workers",  type=int, default=8)
    args = parser.parse_args()

    global prime_set
    prime_set = set(sieve(args.b_max + 10))

    save_dir = args.save_dir
    os.makedirs(save_dir, exist_ok=True)

    # Run full algebraic survey
    results, semiprimes = run_full_atlas(args.b_max, k_hard_max=args.k_max)

    # Save data
    save_results(results, save_dir)

    # Analyze
    analyze_atlas(results)

    # Visuals
    if args.visuals and HAS_MPL:
        print("\nGenerating atlas figures...")
        plot_unit_density_full(results, semiprimes, save_dir)
        plot_ternary_composition_full(results, semiprimes, save_dir)
        plot_zero_density_by_spf(results, save_dir)
        plot_cc_closure_check(results, save_dir)
        plot_interleave_map(results, save_dir)

    # Gate sweep
    if args.gate:
        gate_primes = sieve(args.gate_b_max + 10)
        gate_prime_set = set(gate_primes)
        gate_sp = []
        for b in range(4, args.gate_b_max + 1):
            for p in gate_primes:
                if p * p > b:
                    break
                if b % p == 0:
                    q = b // p
                    if q in gate_prime_set:
                        gate_sp.append((b, p, q, p == q))
                        break
        run_gate_sweep(gate_sp, args.gate_k,
                       args.gate_trials, args.gate_steps,
                       args.workers, save_dir)

    print("\nAtlas complete.")


if __name__ == "__main__":
    main()
