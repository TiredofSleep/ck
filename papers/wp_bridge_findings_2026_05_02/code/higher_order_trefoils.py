"""
Generalize trefoil characterization to other tuple sizes.

Trefoil (3-element) ⟺ multiset = {V, Br, H} or {V, Br, Br} on corrected frame.

Test:
- 2-element pairs: which produce specific crossing counts under runtime?
- 4-element tuples: are there "doubled trefoil" or "quadrefoil" structures?
- General: what does the V/Br/H pattern look like at higher order?
"""
import numpy as np
from itertools import product
from collections import Counter
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10

TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]
FLOW_CELLS = {0, 7}

FLOW = {1, 3, 5, 7, 9}
STRUCTURE = {2, 4, 8}
TRANSITION = {6}
VOID = {0}


def role(n):
    if n in FLOW: return 'F'
    if n in STRUCTURE: return 'S'
    if n in TRANSITION: return 'T'
    if n in VOID: return 'V'
    return '?'


def runtime_step_corrected(p, alpha=0.5):
    pt = np.zeros(10)
    pb = np.zeros(10)
    for i in range(10):
        for j in range(10):
            if i not in FLOW_CELLS and j not in FLOW_CELLS:
                i_local = TSML_8_INDICES.index(i)
                j_local = TSML_8_INDICES.index(j)
                output = int(TSML_8[i_local, j_local])
                pt[output] += p[i] * p[j]
            pb[BHML_10[i, j]] += p[i] * p[j]
    pt = pt / pt.sum() if pt.sum() > 0 else pt
    pb = pb / pb.sum() if pb.sum() > 0 else pb
    p_new = alpha * pt + (1 - alpha) * pb
    return p_new / p_new.sum() if p_new.sum() > 0 else p_new


def tuple_initial_dist(tup, eps=1e-3):
    p = np.full(10, eps)
    for x in tup:
        p[x] += 1.0
    return p / p.sum()


def count_crossings(history, mass_threshold=0.01):
    n_cells = 10
    crossings = 0
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
    return crossings


def trajectory_crossings(tup, max_iter=50):
    p = tuple_initial_dist(tup)
    history = [p.copy()]
    for _ in range(max_iter):
        p_new = runtime_step_corrected(p, alpha=0.5)
        history.append(p_new.copy())
        if np.max(np.abs(p_new - p)) < 1e-8:
            break
        p = p_new
    return count_crossings(np.array(history))


def main():
    # Pairs (2-element)
    print("=" * 70)
    print("PAIR ANALYSIS (2-element tuples)")
    print("=" * 70)
    
    print("\n  Crossing distribution for all 100 pairs:")
    pair_crossings = {}
    for a, b in product(range(10), repeat=2):
        pair_crossings[(a, b)] = trajectory_crossings((a, b))
    
    crossing_dist_pairs = Counter(pair_crossings.values())
    for c, n in sorted(crossing_dist_pairs.items()):
        print(f"    {c} crossings: {n} pairs")
    
    # 1-crossing pairs (analog of "trefoil" but for pairs)
    one_cross_pairs = [p for p, c in pair_crossings.items() if c == 1]
    print(f"\n  1-crossing pairs: {one_cross_pairs}")
    
    if one_cross_pairs:
        ms_set = set(tuple(sorted(p)) for p in one_cross_pairs)
        print(f"  Multisets: {sorted(ms_set)}")
    
    # 0-crossing pairs (trivial)
    zero_pairs = [p for p, c in pair_crossings.items() if c == 0]
    if zero_pairs:
        ms_set = set(tuple(sorted(p)) for p in zero_pairs)
        print(f"\n  0-crossing pairs ({len(zero_pairs)}): multisets {sorted(ms_set)}")
    
    # Quadruples (4-element)
    print("\n" + "=" * 70)
    print("QUADRUPLE ANALYSIS (4-element tuples)")
    print("=" * 70)
    
    print(f"\n  Computing crossings for 4-element tuples in 4-core...")
    four_core = [0, 7, 8, 9]
    four_core_quadruples = list(product(four_core, repeat=4))
    quad_crossings = {q: trajectory_crossings(q) for q in four_core_quadruples}
    
    quad_dist = Counter(quad_crossings.values())
    print(f"\n  Crossing distribution on 4-core quadruples ({len(four_core_quadruples)} total):")
    for c, n in sorted(quad_dist.items()):
        print(f"    {c} crossings: {n} quadruples")
    
    # The trefoil (3-crossing) quadruples
    print(f"\n  3-crossing quadruples (trefoil-extended):")
    three_quads = [q for q, c in quad_crossings.items() if c == 3]
    for q in sorted(three_quads):
        roles = ''.join(role(x) for x in q)
        print(f"    {q}: roles {roles}")
    
    # 4-crossing (next knot up?)
    print(f"\n  4-crossing quadruples (figure-eight-like?):")
    four_cross_quads = [q for q, c in quad_crossings.items() if c == 4]
    if len(four_cross_quads) <= 30:
        for q in sorted(four_cross_quads):
            roles = ''.join(role(x) for x in q)
            print(f"    {q}: roles {roles}")
    else:
        print(f"  ({len(four_cross_quads)} quadruples — showing first 10)")
        for q in sorted(four_cross_quads)[:10]:
            roles = ''.join(role(x) for x in q)
            print(f"    {q}: roles {roles}")
    
    # Multiset distribution at 4-core 3-crossing
    if three_quads:
        ms_dist = Counter(tuple(sorted(q)) for q in three_quads)
        print(f"\n  Multiset distribution of 3-crossing 4-core quadruples:")
        for ms, count in sorted(ms_dist.items()):
            roles_ms = ''.join(role(x) for x in ms)
            print(f"    {ms} ({roles_ms}): {count} permutations")
    
    # Pure trefoil set extended: V + Br + H/Br + something
    print("\n" + "=" * 70)
    print("DOES TREFOIL CHARACTERIZATION EXTEND TO QUADRUPLES?")
    print("=" * 70)
    
    print(f"\n  Trefoil pattern on triples: {{V, Br, H}} or {{V, Br, Br}}")
    print(f"  Hypothesis for quadruples: {{V, Br, H/Br, X}} for X in 4-core?")
    
    # Check: V + Br + H + X for X in {V, H, Br, R}
    print(f"\n  V + Br + H + X (3-crossing tests):")
    for x in [0, 7, 8, 9]:
        ms = tuple(sorted([0, 7, 8, x]))
        # try a permutation
        from itertools import permutations
        seen_ms = set()
        seen_ms.add(ms)
        # Find any permutation in our quadruples
        for perm in permutations([0, 7, 8, x]):
            if perm in quad_crossings:
                c = quad_crossings[perm]
                print(f"    {ms} (one perm gives) {c} crossings")
                break
    
    # Look at 5-element tuples too?
    print("\n" + "=" * 70)
    print("HIGHER-ORDER PATTERNS")
    print("=" * 70)
    
    # 5-tuples in 4-core
    print(f"\n  5-element tuples in 4-core ({len(four_core)**5} = 1024 total):")
    print(f"  Computing... (this may take a moment)")
    
    five_core = list(product([0, 7, 8, 9], repeat=5))
    five_crossings = {}
    for q in five_core:
        five_crossings[q] = trajectory_crossings(q)
    
    five_dist = Counter(five_crossings.values())
    print(f"\n  Crossing distribution on 4-core 5-tuples:")
    for c, n in sorted(five_dist.items())[:15]:
        print(f"    {c} crossings: {n} 5-tuples")
    
    three_five = [q for q, c in five_crossings.items() if c == 3]
    print(f"\n  3-crossing 5-tuples: {len(three_five)}")
    
    if three_five and len(three_five) <= 30:
        print(f"  Multisets:")
        ms_dist = Counter(tuple(sorted(q)) for q in three_five)
        for ms, count in sorted(ms_dist.items()):
            roles_ms = ''.join(role(x) for x in ms)
            print(f"    {ms} ({roles_ms}): {count} perms")
    
    # Also test the relationship between length and crossings
    print("\n" + "=" * 70)
    print("CROSSINGS vs TUPLE LENGTH")
    print("=" * 70)
    
    print(f"\n  How does crossing count scale with tuple length?")
    print(f"  Pure 4-core tuples of length k:")
    
    for k in [2, 3, 4, 5]:
        all_tuples = list(product([0, 7, 8, 9], repeat=k))
        crossings_dist = []
        for q in all_tuples:
            if k == 2:
                c = pair_crossings.get(q, trajectory_crossings(q))
            elif k == 3:
                c = trajectory_crossings(q)
            elif k == 4:
                c = quad_crossings.get(q, trajectory_crossings(q))
            elif k == 5:
                c = five_crossings.get(q, trajectory_crossings(q))
            crossings_dist.append(c)
        print(f"    k={k}: min={min(crossings_dist)}, max={max(crossings_dist)}, "
              f"mean={np.mean(crossings_dist):.1f}, median={np.median(crossings_dist):.1f}")


if __name__ == "__main__":
    main()
