"""
Trefoil-survival on the CORRECTED substrate frame.

TSML_8 = TSML_10 restricted to rows/cols {1,2,3,4,5,6,8,9} (V and H removed).
BHML_10 = full BHML on all 10 elements.
V (0) and H (7) are flow cells between the tables.

A triple's trajectory under the runtime processor needs both tables AND
the V/H flow cells. The "passage through 7=0 puncture" is now a precise
event: the trajectory escapes TSML_8's interior onto the flow boundary.

Test: do the 22 trefoil triples remain trefoil-equivalent on this frame?
Or does the corrected frame change which triples are trefoils?
"""
import numpy as np
from itertools import product
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10, SIGMA_PERMUTATION

TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
FLOW_CELLS = {0, 7}  # V, H — between the tables
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]


def runtime_step_corrected(p, alpha=0.5):
    """Runtime processor using corrected substrate.
    
    TSML_8 acts on the 8 interior cells {1,2,3,4,5,6,8,9}.
    BHML_10 acts on all 10 cells.
    Mass on V or H (flow cells) is steered to the BHML output without TSML.
    """
    pt = np.zeros(10)
    pb = np.zeros(10)
    
    # TSML_8: only operates on indices {1..6, 8, 9}; mass on 0, 7 stays put for TSML
    for i in range(10):
        for j in range(10):
            if i in FLOW_CELLS or j in FLOW_CELLS:
                # Flow cell — TSML doesn't act here, mass stays at original index
                # for TSML's contribution. This is the "TSML_8 doesn't see V/H" rule.
                # We'll simply route this mass through BHML alone for these pairs.
                # Equivalently: TSML contribution = 0 for any (i, j) where i or j
                # is in flow.
                pass
            else:
                # Both i and j are in TSML_8 domain
                i_local = TSML_8_INDICES.index(i)
                j_local = TSML_8_INDICES.index(j)
                output = int(TSML_8[i_local, j_local])
                pt[output] += p[i] * p[j]
            # BHML always acts on full 10x10
            pb[BHML_10[i, j]] += p[i] * p[j]
    
    pt = pt / pt.sum() if pt.sum() > 0 else pt
    pb = pb / pb.sum() if pb.sum() > 0 else pb
    p_new = alpha * pt + (1 - alpha) * pb
    return p_new / p_new.sum() if p_new.sum() > 0 else p_new


def triple_initial_dist(a, b, c, eps=1e-3):
    p = np.full(10, eps)
    p[a] += 1.0
    p[b] += 1.0
    p[c] += 1.0
    return p / p.sum()


def count_crossings_corrected(history, mass_threshold=0.01):
    """Count rank-swap crossings."""
    n_cells = 10
    crossings = 0
    crossing_pairs = []
    for t in range(len(history) - 1):
        p_now = history[t]
        p_next = history[t+1]
        rank_now = np.argsort(-p_now)
        rank_next = np.argsort(-p_next)
        for i in range(n_cells):
            for j in range(i+1, n_cells):
                if max(p_now[i], p_next[i]) < mass_threshold: continue
                if max(p_now[j], p_next[j]) < mass_threshold: continue
                pos_i_now = list(rank_now).index(i)
                pos_j_now = list(rank_now).index(j)
                pos_i_next = list(rank_next).index(i)
                pos_j_next = list(rank_next).index(j)
                if (pos_i_now < pos_j_now) != (pos_i_next < pos_j_next):
                    crossings += 1
                    crossing_pairs.append((t, i, j))
    return crossings, crossing_pairs


def trajectory_corrected(a, b, c, max_iter=50):
    p = triple_initial_dist(a, b, c)
    history = [p.copy()]
    for it in range(max_iter):
        p_new = runtime_step_corrected(p, alpha=0.5)
        history.append(p_new.copy())
        if np.max(np.abs(p_new - p)) < 1e-8:
            break
        p = p_new
    history = np.array(history)
    crossings, pairs = count_crossings_corrected(history)
    
    # Track passage through flow cells: max mass on V and H during trajectory
    max_void_mass = float(np.max(history[:, 0]))
    max_harmony_mass = float(np.max(history[:, 7]))
    
    # Also track final state
    final = history[-1]
    final_dom = int(np.argmax(final))
    
    return {
        'triple': (a, b, c),
        'crossings': crossings,
        'crossing_pairs': pairs,
        'max_void_mass': max_void_mass,
        'max_harmony_mass': max_harmony_mass,
        'final_dom': final_dom,
        'iters': len(history),
        'final_void': float(final[0]),
        'final_harmony': float(final[7]),
    }


def main():
    print("=" * 70)
    print("CORRECTED FRAME: TSML_8 + BHML_10 RUNTIME PROCESSOR")
    print("=" * 70)
    print(f"\nTSML_8 acts on: {TSML_8_INDICES}")
    print(f"Flow cells (V, H = 0, 7) between tables")
    print(f"BHML_10 acts on full {{0..9}}")
    
    print("\n" + "=" * 70)
    print("ALL 1000 TRIPLES — CROSSING COUNT DISTRIBUTION ON CORRECTED FRAME")
    print("=" * 70)
    
    results = []
    for a, b, c in product(range(10), repeat=3):
        r = trajectory_corrected(a, b, c)
        results.append(r)
    
    from collections import Counter
    crossing_dist = Counter(r['crossings'] for r in results)
    print(f"\nDistribution of crossing counts (1000 triples on corrected frame):")
    for cn in sorted(crossing_dist.keys())[:20]:
        bar = '█' * (crossing_dist[cn] * 50 // max(crossing_dist.values()))
        print(f"  {cn:>3} crossings: {crossing_dist[cn]:>4} triples  {bar}")
    
    print("\n" + "=" * 70)
    print("3-CROSSING TRIPLES ON CORRECTED FRAME")
    print("=" * 70)
    
    three_crossing = [r for r in results if r['crossings'] == 3]
    print(f"\n  Number of 3-crossing triples: {len(three_crossing)}")
    
    print(f"\n  All 3-crossing triples:")
    for r in three_crossing:
        t = r['triple']
        print(f"    {t}: V_max={r['max_void_mass']:.3f}, H_max={r['max_harmony_mass']:.3f}, "
              f"final_dom={r['final_dom']}")
    
    # Compare to OLD trefoil-22 (from uncorrected frame)
    OLD_TREFOIL_22 = {
        (0,0,8), (0,7,7), (0,7,9), (0,8,0), (0,9,7),
        (7,0,7), (7,0,9), (7,7,0), (7,7,7), (7,7,9),
        (7,8,9), (7,9,0), (7,9,7), (7,9,8),
        (8,0,0), (8,7,9), (8,9,7),
        (9,0,7), (9,7,0), (9,7,7), (9,7,8), (9,8,7),
    }
    
    new_trefoil_set = set(r['triple'] for r in three_crossing)
    
    in_both = OLD_TREFOIL_22 & new_trefoil_set
    only_old = OLD_TREFOIL_22 - new_trefoil_set
    only_new = new_trefoil_set - OLD_TREFOIL_22
    
    print(f"\n  Comparison to UNCORRECTED frame's trefoil-22:")
    print(f"    In both: {len(in_both)}")
    print(f"    Old (uncorrected) only: {len(only_old)}")
    print(f"    New (corrected) only: {len(only_new)}")
    
    if only_old:
        print(f"\n    LOST when correcting frame:")
        for t in sorted(only_old):
            print(f"      {t}")
    
    if only_new:
        print(f"\n    GAINED when correcting frame:")
        for t in sorted(only_new):
            print(f"      {t}")
    
    # Multiset analysis on corrected frame
    if three_crossing:
        new_multisets = Counter(tuple(sorted(r['triple'])) for r in three_crossing)
        print(f"\n  Multiset structure (corrected frame):")
        for ms, count in sorted(new_multisets.items()):
            print(f"    {ms}: {count} permutations")
    
    # Canonical grammar on corrected frame
    print("\n" + "=" * 70)
    print("CANONICAL PROPAGATION GRAMMAR ON CORRECTED FRAME")
    print("=" * 70)
    canonical = [(0,1,2), (0,7,1), (5,6,7), (7,8,9), (7,8,8)]
    print(f"\n  Triple    | crossings | V_max | H_max | final")
    for t in canonical:
        r = trajectory_corrected(*t)
        print(f"  {str(t):<10} | {r['crossings']:>9} | {r['max_void_mass']:>5.3f} | "
              f"{r['max_harmony_mass']:>5.3f} | {r['final_dom']}")
    
    # 4-core triples on corrected frame
    print("\n" + "=" * 70)
    print("4-CORE TRIPLES ON CORRECTED FRAME")
    print("=" * 70)
    four_core = {0, 7, 8, 9}
    fc_triples = [(a,b,c) for a,b,c in product(four_core, repeat=3)]
    fc_results = [trajectory_corrected(*t) for t in fc_triples]
    fc_crossings = Counter(r['crossings'] for r in fc_results)
    print(f"\n  Crossings distribution on 4-core (64 triples):")
    for cn in sorted(fc_crossings.keys()):
        print(f"    {cn} crossings: {fc_crossings[cn]} triples")
    
    fc_trefoil = [r for r in fc_results if r['crossings'] == 3]
    print(f"\n  4-core triples with 3 crossings on corrected frame: {len(fc_trefoil)}")
    return results, three_crossing, only_old, only_new


if __name__ == "__main__":
    main()
