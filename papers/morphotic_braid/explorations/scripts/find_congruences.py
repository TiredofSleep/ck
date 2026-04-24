# PACKET: evening_handoff_2026_04_23/find_congruences.py
"""
Find all congruences of TSML. A congruence is an equivalence relation
~ such that a~a', b~b' ⟹ T[a][b]~T[a'][b'].

The lattice of congruences of a magma tells us exactly which quotient 
structures are valid.

Method: generate all partitions of {0,...,9}, filter for congruences,
report their class counts.
"""
from itertools import combinations
from functools import lru_cache

TSML = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]
N = 10

def is_congruence(partition, T):
    """partition: list of frozensets covering 0..N-1."""
    N = len(T)
    cls = {}
    for i, p in enumerate(partition):
        for e in p: cls[e] = i
    # Check: for each pair of classes, all element-pair outputs are same class
    for p1 in partition:
        for p2 in partition:
            outs = set()
            for a in p1:
                for b in p2:
                    outs.add(cls[T[a][b]])
                    if len(outs) > 1: return False
    return True

def partitions(elements):
    """Generate all set partitions of a list of elements."""
    if len(elements) == 1:
        yield [set(elements)]
        return
    first = elements[0]
    for rest_part in partitions(elements[1:]):
        # Case 1: first is in its own class
        yield [{first}] + [s.copy() for s in rest_part]
        # Case 2: first joins one of the existing classes
        for i in range(len(rest_part)):
            new_part = [s.copy() for s in rest_part]
            new_part[i].add(first)
            yield new_part

print("Enumerating all 115,975 partitions of {0..9} (Bell number B_10)...")
# Actually this is a lot. Let me use a smarter approach — generate partitions 
# with at most 8 classes (since we want interesting quotients).

congruences = []
count = 0
for part in partitions(list(range(10))):
    count += 1
    if is_congruence(part, TSML):
        congruences.append([sorted(c) for c in part])

print(f"Total partitions examined: {count}")
print(f"Congruences found: {len(congruences)}")
print()

# Group by class count
by_count = {}
for cong in congruences:
    by_count.setdefault(len(cong), []).append(cong)

print("="*75)
print("CONGRUENCES OF TSML BY CLASS COUNT")
print("="*75)
for k in sorted(by_count.keys()):
    print(f"\n{len(by_count[k])} congruence(s) with {k} classes:")
    for c in by_count[k][:5]:  # show first 5
        # Format nicely
        parts_str = ", ".join("{" + ",".join(str(x) for x in sorted(p)) + "}" for p in c)
        print(f"  {parts_str}")
    if len(by_count[k]) > 5:
        print(f"  ... and {len(by_count[k]) - 5} more")

# Focus on 7-class congruences
print()
print("="*75)
print("ALL 7-CLASS CONGRUENCES (target: Brayden's intuition)")
print("="*75)
if 7 in by_count:
    for c in by_count[7]:
        parts_str = ", ".join("{" + ",".join(str(x) for x in sorted(p)) + "}" for p in c)
        print(f"  {parts_str}")
else:
    print("  No congruences with exactly 7 classes.")
    # Show 6 and 8 class counts
    for k in [6, 8]:
        if k in by_count:
            print(f"\n  But there ARE {len(by_count[k])} congruences with {k} classes:")
            for c in by_count[k][:10]:
                parts_str = ", ".join("{" + ",".join(str(x) for x in sorted(p)) + "}" for p in c)
                print(f"    {parts_str}")

