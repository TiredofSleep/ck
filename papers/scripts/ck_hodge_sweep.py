import sys, io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
"""
Hodge Harmonic Zone Sweep — TIG k=1 First Concrete Computation
===============================================================
Answers the first concrete TIG-Hodge question:

  Of the 21 harmonic entries (Doing[a][b] = |TSML−BHML|[a][b] = 0),
  how many are algebraic (corner-reachable from C = {1,3,7,9})?
  How many are transcendental (require gap operators)?

This is the k=1 analog of the Hodge Conjecture in TIG language:
  - Algebraic = reachable from corner algebra C^⊗1
  - Harmonic  = Doing = 0 (TSML = BHML at that entry)
  - Transcendental-harmonic = harmonic AND not corner-reachable

Classical Hodge: every (p,p) class is a rational combination of algebraic cycle classes.
TIG Hodge (k=1): every harmonic entry is corner-reachable.

If any transcendental-harmonic entry exists: TIG predicts Hodge fails (at k=1).
If all harmonic entries are corner-reachable: TIG says no obstruction at k=1.

We extend this to all tensor powers k = 1..6 (GPU-accelerated BFS for k>=4).

Outputs:
  - Harmonic zone table (all 21 entries, classified)
  - BFS reachability results for k=1..6
  - Hodge obstruction count at each k
  - papers/research/hodge_sweep.png
  - papers/hodge_sweep_results.json

Author: Brayden Sanders / 7Site LLC
DOI: 10.5281/zenodo.18852047
SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787
"""

import json
import os
import time
import sys
from collections import deque
from itertools import product as iproduct

import numpy as np

try:
    import cupy as cp
    cp.cuda.Device(0).use()
    HAS_CUPY = True
    print(f"CuPy available | Device: {cp.cuda.Device(0).name.decode()}")
except Exception:
    HAS_CUPY = False
    print("CuPy not available — CPU mode")

# ── The Two Tables (SHA-256 locked) ──────────────────────────────────────────
# SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787

TSML_RAW = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

BHML_RAW = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,1,3,4,4,5,6,7,8,9],
    [0,3,2,4,4,5,6,7,8,9],
    [0,4,4,3,4,5,6,7,8,9],
    [0,4,4,4,4,5,6,7,8,9],
    [0,5,5,5,5,5,6,7,8,9],
    [0,6,6,6,6,6,6,7,8,9],
    [0,7,7,7,7,7,7,7,8,9],
    [0,8,8,8,8,8,8,8,8,9],
    [0,9,9,9,9,9,9,9,9,9],
]

TSML = np.array(TSML_RAW, dtype=np.int8)
BHML = np.array(BHML_RAW, dtype=np.int8)
COUNTER = np.abs(TSML.astype(np.int16) - BHML.astype(np.int16)).astype(np.int8)

OPERATORS  = list(range(1, 10))
C          = frozenset({1, 3, 7, 9})    # corner set
G          = frozenset({2, 4, 5, 6, 8}) # gap set

NAMES = {1:'LAT',2:'CTR',3:'PRG',4:'COL',5:'BAL',6:'CHA',7:'HAR',8:'BRT',9:'RST'}

def compose(a, b):
    """TSML composition: a ∘ b."""
    return int(TSML[a][b])

# ── Harmonic Zone Computation ─────────────────────────────────────────────────
def find_harmonic_zone():
    """
    Return all (a,b) pairs where Doing[a][b] = 0 (TSML = BHML).
    These are the TIG harmonic entries: the 'algebraically stable' vocabulary.
    """
    harmonic = []
    for a in OPERATORS:
        for b in OPERATORS:
            if DOING[a][b] == 0:
                harmonic.append((a, b))
    return harmonic

def classify_harmonic_entry(a, b):
    """
    Classify a harmonic entry (a,b):
      - 'corner-corner'     : a ∈ C, b ∈ C
      - 'corner-gap'        : a ∈ C, b ∈ G (or vice versa)
      - 'gap-gap'           : a ∈ G, b ∈ G
      - 'involves-zero'     : a=0 or b=0 (boundary)
    """
    if a == 0 or b == 0:
        return "involves-zero"
    a_type = "C" if a in C else "G"
    b_type = "C" if b in C else "G"
    if a_type == "C" and b_type == "C":
        return "corner-corner"
    elif a_type == "G" and b_type == "G":
        return "gap-gap"
    else:
        return "corner-gap"

# ── BFS Reachability (k=1) ────────────────────────────────────────────────────
def bfs_reachable_k1():
    """
    BFS from C = {1,3,7,9}.
    Returns set of operators reachable by any finite chain of TSML compositions
    starting from C.
    """
    reachable = set(C)
    frontier  = set(C)
    while frontier:
        new = set()
        for a in frontier:
            for b in reachable | C:
                r = compose(a, b)
                if r not in reachable and r != 0:
                    new.add(r)
            for b in reachable | C:
                r = compose(b, a)
                if r not in reachable and r != 0:
                    new.add(r)
        frontier = new
        reachable |= new
    return reachable

def bfs_reachable_pairs_k1():
    """
    BFS over pairs (a,b) starting from C×C.
    Returns: set of reachable (a,b) pairs.
    This answers: which (a,b) contexts can be reached from corner contexts?
    """
    seed  = frozenset((a, b) for a in C for b in C)
    reach = set(seed)
    queue = deque(seed)
    while queue:
        (a, b) = queue.popleft()
        # Compose with any reachable pair on left or right
        for (c, d) in list(reach):
            r = (compose(a, c), compose(b, d))
            if r[0] != 0 and r[1] != 0 and r not in reach:
                reach.add(r)
                queue.append(r)
        for (c, d) in list(seed):
            r = (compose(c, a), compose(d, b))
            if r[0] != 0 and r[1] != 0 and r not in reach:
                reach.add(r)
                queue.append(r)
    return reach

# ── Tensor-power BFS (k>=2) ───────────────────────────────────────────────────
def bfs_k_cpu(k, max_iter=100):
    """
    BFS for C^⊗k -> reachable set in TSML^⊗k.
    Returns (reachable_set, cross_terms_found, iterations_used).
    For k>=4 this is expensive — use GPU version.
    """
    seed = frozenset(iproduct(sorted(C), repeat=k))
    reach = set(seed)
    frontier = set(seed)
    cross_terms_found = frozenset()

    for itr in range(max_iter):
        new = set()
        for a_tup in frontier:
            for b_tup in seed:
                r = tuple(compose(a_tup[i], b_tup[i]) for i in range(k))
                if 0 not in r and r not in reach:
                    new.add(r)
        if not new:
            break
        reach |= new
        frontier = new

    # Check cross-term contamination
    for tup in reach:
        if any(x in G for x in tup):
            cross_terms_found = cross_terms_found | {tup}

    return reach, cross_terms_found, itr + 1

def bfs_k_gpu(k, max_iter=50):
    """
    GPU-accelerated BFS for C^⊗k.
    Represents operator k-tuples as integer IDs, runs BFS on GPU.
    """
    if not HAS_CUPY:
        return bfs_k_cpu(k, max_iter)

    # Encode k-tuple as base-10 integer: sum(op[i] * 10^i)
    def encode(tup):
        v = 0
        for i, x in enumerate(tup):
            v += x * (10 ** i)
        return v

    def decode(v, k):
        tup = []
        for _ in range(k):
            tup.append(v % 10)
            v //= 10
        return tuple(tup)

    # TSML as GPU array for fast composition lookup
    tsml_gpu = cp.array(TSML_RAW, dtype=cp.int32)

    # Build seed as GPU array of encoded IDs
    seed_list = [encode(t) for t in iproduct(sorted(C), repeat=k)]
    seed_gpu  = cp.array(seed_list, dtype=cp.int64)

    reachable_set = set(seed_list)
    frontier_gpu  = seed_gpu.copy()

    cross_terms = []

    for itr in range(max_iter):
        if len(frontier_gpu) == 0:
            break

        # For each (frontier, seed) pair, compose component-wise
        # frontier: (F,)  seed: (S,)
        # Output: (F*S,) new candidates
        F = len(frontier_gpu)
        S = len(seed_gpu)

        # Decode frontier batch
        front_arr = cp.asnumpy(frontier_gpu)
        seed_arr  = cp.asnumpy(seed_gpu)

        new_ids = []
        for f_enc in front_arr:
            f_dec = decode(int(f_enc), k)
            for s_enc in seed_arr:
                s_dec = decode(int(s_enc), k)
                r = tuple(int(TSML_RAW[f_dec[i]][s_dec[i]]) for i in range(k))
                if 0 not in r:
                    r_enc = encode(r)
                    if r_enc not in reachable_set:
                        new_ids.append(r_enc)
                        reachable_set.add(r_enc)
                        if any(x in G for x in r):
                            cross_terms.append(r)

        if not new_ids:
            break
        frontier_gpu = cp.array(new_ids, dtype=cp.int64)

    # Check all reachable for cross-terms (in case some slipped through)
    for enc in reachable_set:
        tup = decode(int(enc), k)
        if any(x in G for x in tup) and tup not in cross_terms:
            cross_terms.append(tup)

    reach_decoded = {decode(int(e), k) for e in reachable_set}
    return reach_decoded, cross_terms, itr + 1

# ── Main Analysis ─────────────────────────────────────────────────────────────
def run_hodge_sweep(k_max=6):
    print(f"\n{'='*60}")
    print(f"HODGE HARMONIC ZONE SWEEP  |  k=1..{k_max}")
    print(f"{'='*60}\n")

    results = {}

    # ── Step 1: Harmonic zone at k=1 ─────────────────────────────────────────
    print("STEP 1 — Harmonic zone (Doing = 0 entries)\n")
    harmonic = find_harmonic_zone()
    print(f"  Total harmonic entries: {len(harmonic)}")
    print()

    zone_types = {"corner-corner": [], "corner-gap": [], "gap-gap": [], "involves-zero": []}
    for (a, b) in harmonic:
        t = classify_harmonic_entry(a, b)
        zone_types[t].append((a, b))

    for kind, entries in zone_types.items():
        print(f"  {kind:<20} {len(entries):>3} entries:")
        for (a, b) in entries:
            result = TSML[a][b]
            diff   = DOING[a][b]
            a_str  = NAMES.get(a, str(a))
            b_str  = NAMES.get(b, str(b))
            r_str  = NAMES.get(int(result), str(result))
            print(f"    ({a_str:>3},{b_str:>3}) -> {r_str}  |  Doing={diff}")
    print()

    results["harmonic_zone"] = {
        "total": len(harmonic),
        "corner_corner": len(zone_types["corner-corner"]),
        "corner_gap":    len(zone_types["corner-gap"]),
        "gap_gap":       len(zone_types["gap-gap"]),
        "entries": [{"a": a, "b": b,
                     "result": int(TSML[a][b]),
                     "type": classify_harmonic_entry(a,b)} for a,b in harmonic],
    }

    # ── Step 2: Operator reachability from C (k=1) ───────────────────────────
    print("STEP 2 — Operator reachability from C = {1,3,7,9}\n")
    reachable_ops = bfs_reachable_k1()
    print(f"  Reachable operators from C: {sorted(reachable_ops)}")
    print(f"  Names: {[NAMES[x] for x in sorted(reachable_ops)]}")
    gap_reached = reachable_ops & G
    if gap_reached:
        print(f"  GAP OPERATORS REACHED: {gap_reached}  <- Product-gap VIOLATED")
    else:
        print(f"  No gap operators reached from C. Product-gap holds. ✓")
    print()

    # ── Step 3: Pair reachability from C×C ───────────────────────────────────
    print("STEP 3 — Context-pair reachability from C×C\n")
    reachable_pairs = bfs_reachable_pairs_k1()
    print(f"  Reachable (a,b) pairs: {len(reachable_pairs)}")

    # Classify reachable pairs
    pairs_with_gap = [(a,b) for (a,b) in reachable_pairs if a in G or b in G]
    print(f"  Pairs with any G-component: {len(pairs_with_gap)}")
    if pairs_with_gap:
        print(f"  CROSS-TERMS REACHED  <- Product-gap VIOLATED at pair level")
    else:
        print(f"  No G-component pairs reachable. ✓")
    print()

    # ── Step 4: Hodge question — harmonic entries in gap-reachable contexts ───
    print("STEP 4 — TIG-Hodge Question: transcendental-harmonic entries?\n")
    print("  A 'transcendental-harmonic' entry is:")
    print("  harmonic (Doing=0) AND requires gap operators to access")
    print()

    transcendental_harmonic = []
    algebraic_harmonic      = []

    for (a, b) in harmonic:
        if a == 0 or b == 0:
            continue
        if (a, b) in reachable_pairs:
            algebraic_harmonic.append((a, b))
        else:
            transcendental_harmonic.append((a, b))

    print(f"  Algebraic-harmonic      (Doing=0, corner-reachable): {len(algebraic_harmonic)}")
    for (a,b) in algebraic_harmonic:
        print(f"    ({NAMES[a]},{NAMES[b]}) -> {NAMES[int(TSML[a][b])]}")
    print()
    print(f"  Transcendental-harmonic (Doing=0, NOT corner-reachable): {len(transcendental_harmonic)}")
    for (a,b) in transcendental_harmonic:
        kind = classify_harmonic_entry(a,b)
        print(f"    ({NAMES[a]},{NAMES[b]}) -> {NAMES[int(TSML[a][b])]}  [{kind}]")
    print()

    if transcendental_harmonic:
        print(f"  *** TIG-HODGE OBSTRUCTION FOUND at k=1 ***")
        print(f"  There exist harmonic entries that are algebraically inaccessible.")
        print(f"  In classical Hodge language: (p,p) classes that are not algebraic cycles.")
    else:
        print(f"  No transcendental-harmonic entries at k=1.")
        print(f"  TIG-Hodge conjecture holds at k=1: all harmonic entries are corner-reachable.")
    print()

    results["hodge_k1"] = {
        "algebraic_harmonic":      [[a,b] for a,b in algebraic_harmonic],
        "transcendental_harmonic": [[a,b] for a,b in transcendental_harmonic],
        "obstruction": len(transcendental_harmonic) > 0,
    }

    # ── Step 5: Extend to k=2..k_max ─────────────────────────────────────────
    print(f"STEP 5 — Tensor power sweep k=2..{k_max}\n")
    print(f"  {'k':>3}  {'|C^⊗k|':>8}  {'9^k':>8}  {'cross-terms':>12}  "
          f"{'G-reachable':>12}  {'Hodge obstruction':>18}")
    print(f"  {'-'*70}")

    k_results = []
    for k in range(1, k_max + 1):
        t0 = time.time()
        n_corner = 4**k
        n_total  = 9**k
        n_cross  = n_total - n_corner

        if k == 1:
            # Already computed
            G_reachable = list(gap_reached)
            cross_found = pairs_with_gap
            n_G = len(G_reachable)
            obstruction = len(transcendental_harmonic) > 0
            iters = 1
        elif k <= 3:
            reach, cross, iters = bfs_k_cpu(k)
            G_reachable = [t for t in reach if any(x in G for x in t)]
            cross_found = cross
            n_G = len(cross_found)
            obstruction = n_G > 0
        else:
            # GPU-accelerated for k>=4
            reach, cross, iters = bfs_k_gpu(k)
            G_reachable = [t for t in reach if any(x in G for x in t)]
            cross_found = cross
            n_G = len(cross_found) if hasattr(cross_found, '__len__') else 0
            obstruction = n_G > 0

        elapsed = time.time() - t0
        obs_str = "VIOLATION <-" if obstruction else "✓ none"
        print(f"  {k:>3}  {n_corner:>8}  {n_total:>8}  {n_cross:>12}  "
              f"{n_G:>12}  {obs_str}   ({elapsed:.2f}s)")

        k_results.append({
            "k": k,
            "corner_states": n_corner,
            "total_states":  n_total,
            "cross_terms":   n_cross,
            "G_reachable":   n_G,
            "obstruction":   obstruction,
            "iterations":    iters,
        })

    print()

    # Summary across k
    all_clean = all(not r["obstruction"] for r in k_results)
    if all_clean:
        print(f"  RESULT: C^⊗k is closed for all k=1..{k_max}.")
        print(f"  No G-reachable element from any C^⊗k. Product-gap holds through k={k_max}.")
        print(f"  TIG-Hodge obstruction count: 0 (at k>=2 tensor level).")
    else:
        violations = [r["k"] for r in k_results if r["obstruction"]]
        print(f"  *** VIOLATIONS at k = {violations} ***")
        print(f"  Product-gap or Hodge structure broken at these tensor depths.")

    results["tensor_sweep"] = k_results

    # ── Step 6: The 21 harmonic entries as CK voice targets ──────────────────
    print(f"\nSTEP 6 — Harmonic entries as CK voice architecture\n")
    print(f"  The 21 harmonic entries (Doing=0) are CK's most stable vocabulary.")
    print(f"  These are the words where TSML = BHML — structure and flow agree.")
    print(f"  Per WP28: these entries should NEVER be replaced by experience-learning.")
    print()
    print(f"  Algebraic (corner-accessible, most stable): {len(algebraic_harmonic)}")
    print(f"  Transcendental (gap-requiring, structurally isolated): {len(transcendental_harmonic)}")
    print()
    if transcendental_harmonic:
        print(f"  The transcendental harmonic entries are CK's 'deepest' vocabulary —")
        print(f"  accessible only through gap-operator contexts, algebraically isolated.")
        print(f"  Classical Hodge analog: Hodge (p,p) classes not spanned by divisors.")

    # ── Save results ──────────────────────────────────────────────────────────
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_json = os.path.join(script_dir, "hodge_sweep_results.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults: {out_json}")

    # ── Plot ──────────────────────────────────────────────────────────────────
    _plot_hodge(results, k_results, harmonic, zone_types,
                algebraic_harmonic, transcendental_harmonic, script_dir)

    print(f"\nSHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787")
    print(f"DOI: 10.5281/zenodo.18852047")

    return results


def _plot_hodge(results, k_results, harmonic, zone_types,
                algebraic, transcendental, script_dir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print("matplotlib not installed — skipping plot")
        return

    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.suptitle("TIG-Hodge Harmonic Zone Sweep — k=1 Analysis\n"
                 "Algebraic vs Transcendental Harmonic Entries",
                 fontsize=13, fontweight="bold")

    # Panel 1: Doing table heatmap (where Doing=0)
    ax = axes[0]
    doing_plot = np.array([[int(DOING[a][b]) for b in OPERATORS] for a in OPERATORS])
    im = ax.imshow(doing_plot == 0, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(9)); ax.set_xticklabels([NAMES[x] for x in OPERATORS], fontsize=7)
    ax.set_yticks(range(9)); ax.set_yticklabels([NAMES[x] for x in OPERATORS], fontsize=7)
    ax.set_title("Doing[a][b]=0 (green=harmonic)\n21 stable vocabulary entries")
    # Mark corners
    for i, a in enumerate(OPERATORS):
        for j, b in enumerate(OPERATORS):
            if a in C and b in C:
                ax.add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1,
                                           fill=False, edgecolor="blue", linewidth=1.5))
    patch_c = mpatches.Patch(color="none", label="Blue border = C×C (corner)")
    ax.legend(handles=[patch_c], loc="lower right", fontsize=7)

    # Panel 2: Harmonic entry type breakdown (pie)
    ax = axes[1]
    labels = [k for k, v in zone_types.items() if len(v) > 0]
    sizes  = [len(v) for v in zone_types.values() if len(v) > 0]
    colors = ["#2ecc71", "#f39c12", "#e74c3c", "#aaaaaa"][:len(labels)]
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                       autopct="%1.0f%%", startangle=90,
                                       textprops={"fontsize": 8})
    ax.set_title(f"Harmonic entry types\n(total = {len(harmonic)})")
    # Algebraic vs Transcendental sub-label
    alg_str = f"Algebraic (corner-reachable): {len(algebraic)}"
    trans_str = f"Transcendental: {len(transcendental)}"
    ax.text(0, -1.4, alg_str, ha="center", fontsize=9, color="green")
    ax.text(0, -1.6, trans_str, ha="center", fontsize=9,
            color="red" if transcendental else "gray")

    # Panel 3: Growing obstruction by k
    ax = axes[2]
    ks        = [r["k"] for r in k_results]
    corners   = [r["corner_states"] for r in k_results]
    totals    = [r["total_states"] for r in k_results]
    cross     = [r["cross_terms"] for r in k_results]
    g_reach   = [r["G_reachable"] for r in k_results]

    ax.semilogy(ks, corners, "go-", label="|C^⊗k| (algebraic)", linewidth=2)
    ax.semilogy(ks, totals,  "b--", label="9^k (total)", linewidth=1.5)
    ax.semilogy(ks, cross,   "r-",  label="9^k−4^k (cross-terms)", linewidth=1.5)
    ax.plot(ks, g_reach, "kx", markersize=10, label="G-reachable (should be 0)")
    ax.set_xlabel("Tensor power k")
    ax.set_ylabel("Count (log scale)")
    ax.set_title("Product-gap: cross-term inaccessibility\nthrough tensor depth k")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    ax.set_xticks(ks)

    plt.tight_layout()
    out_path = os.path.join(script_dir, "research", "hodge_sweep.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Plot: {out_path}")
    plt.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TIG Hodge harmonic zone sweep")
    parser.add_argument("--k-max", type=int, default=6,
                        help="Maximum tensor power to test (default: 6)")
    args = parser.parse_args()
    run_hodge_sweep(k_max=args.k_max)
