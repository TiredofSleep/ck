"""
Full associativity gap landscape, no pre-filtering.

For each ordered triple (a, b, c) in {0,...,9}^3:
  - Compute L = T(T(a,b), c)  (left bracketing)
  - Compute R = T(a, T(b,c))  (right bracketing)
  - Record gap (L vs R) and where each lands

Then look at:
  - Distribution of L - R values
  - Where gaps occur (rows? cols? cells?)
  - What landing values appear
  - Whether σ-fixed points show up specially
  - Whether 6-cycle elements show up specially
  - Whether bumps show up specially
  - Any other patterns we don't anticipate

NO PRE-FILTERING. We look at all 1000 triples.
"""
import numpy as np
from collections import Counter, defaultdict

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=int)

# Categorize indices
six_cycle = {1, 2, 4, 5, 6, 7}  # σ-orbit of cycle: 1→7→6→5→4→2→1
sigma_fixed = {0, 3, 8, 9}      # σ-fixed
bump_cells = []
for i in range(10):
    for j in range(10):
        if T[i,j] not in (0, 7):
            bump_cells.append((i, j, T[i,j]))

# Per CL specification: T-idempotent (T[i,i]=i): {0, 7}
T_idempotent = {0, 7}

print("="*70)
print("STEP 1: Compute the full associativity gap")
print("="*70)

triples = []
for a in range(10):
    for b in range(10):
        for c in range(10):
            L = T[T[a,b], c]
            R = T[a, T[b,c]]
            triples.append({
                'a': a, 'b': b, 'c': c,
                'L': L, 'R': R,
                'gap': L != R,
                'L_minus_R': int(L) - int(R),
            })

n_total = len(triples)
n_assoc = sum(1 for t in triples if not t['gap'])
n_nonassoc = sum(1 for t in triples if t['gap'])

print(f"\nTotal triples: {n_total}")
print(f"Associative (L == R): {n_assoc} ({100*n_assoc/n_total:.1f}%)")
print(f"Non-associative (L != R): {n_nonassoc} ({100*n_nonassoc/n_total:.1f}%)")

print("\n" + "="*70)
print("STEP 2: Distribution of (L, R) pairs across all triples")
print("="*70)
print()

LR_counter = Counter((t['L'], t['R']) for t in triples)
print("(L, R) distribution (just top entries):")
for (L, R), count in sorted(LR_counter.items(), key=lambda x: -x[1])[:20]:
    print(f"  L={L}, R={R}: {count} triples")

print("\n" + "="*70)
print("STEP 3: For non-associative triples, what values appear as L vs R?")
print("="*70)

L_values_nonassoc = Counter(t['L'] for t in triples if t['gap'])
R_values_nonassoc = Counter(t['R'] for t in triples if t['gap'])

print(f"\nL values when L != R:")
for v in range(10):
    print(f"  {v}: {L_values_nonassoc.get(v, 0)}")

print(f"\nR values when L != R:")
for v in range(10):
    print(f"  {v}: {R_values_nonassoc.get(v, 0)}")

# Symmetric: do they have the SAME distribution?
identical = all(L_values_nonassoc.get(v, 0) == R_values_nonassoc.get(v, 0) 
                for v in range(10))
print(f"\nL and R distributions identical? {identical}")
# This tells us if there's a directional bias (left vs right bracketing)

print("\n" + "="*70)
print("STEP 4: How many distinct (L, R) UNORDERED pairs appear?")
print("="*70)

unordered_LR = Counter()
for t in triples:
    if t['gap']:
        pair = tuple(sorted([t['L'], t['R']]))
        unordered_LR[pair] += 1

print(f"\nDistinct unordered {{L, R}} pairs in non-associative triples: {len(unordered_LR)}")
print(f"\nAll unordered pairs:")
for pair, count in sorted(unordered_LR.items(), key=lambda x: -x[1]):
    print(f"  {{{pair[0]}, {pair[1]}}}: {count} triples")

print("\n" + "="*70)
print("STEP 5: Position in input — where do gaps occur?")
print("="*70)

# Does the position of σ-fixed indices in the input matter?
gap_by_input_a = Counter()
gap_by_input_b = Counter()
gap_by_input_c = Counter()
for t in triples:
    if t['gap']:
        gap_by_input_a[t['a']] += 1
        gap_by_input_b[t['b']] += 1
        gap_by_input_c[t['c']] += 1

print(f"\nNon-associative triples by position of input value:")
print(f"  position a: {dict(gap_by_input_a)}")
print(f"  position b: {dict(gap_by_input_b)}")
print(f"  position c: {dict(gap_by_input_c)}")

# What if the inputs are σ-fixed only? 
nonassoc_with_all_fixed = sum(1 for t in triples 
                                if t['gap'] 
                                and t['a'] in sigma_fixed
                                and t['b'] in sigma_fixed
                                and t['c'] in sigma_fixed)
total_all_fixed = sum(1 for t in triples 
                      if t['a'] in sigma_fixed
                      and t['b'] in sigma_fixed
                      and t['c'] in sigma_fixed)
print(f"\nWhen all 3 inputs are σ-fixed: {nonassoc_with_all_fixed}/{total_all_fixed} non-associative")

nonassoc_with_no_fixed = sum(1 for t in triples 
                              if t['gap'] 
                              and t['a'] not in sigma_fixed
                              and t['b'] not in sigma_fixed
                              and t['c'] not in sigma_fixed)
total_no_fixed = sum(1 for t in triples 
                    if t['a'] not in sigma_fixed
                    and t['b'] not in sigma_fixed
                    and t['c'] not in sigma_fixed)
print(f"When NO inputs are σ-fixed: {nonassoc_with_no_fixed}/{total_no_fixed} non-associative")

# What if exactly one position is σ-fixed?
for pos in ['a', 'b', 'c']:
    nonassoc_with_pos_fixed = sum(1 for t in triples 
                                    if t['gap'] 
                                    and t[pos] in sigma_fixed
                                    and all(t[p] not in sigma_fixed 
                                          for p in ['a','b','c'] if p != pos))
    total_pos_fixed = sum(1 for t in triples 
                          if t[pos] in sigma_fixed
                          and all(t[p] not in sigma_fixed 
                                for p in ['a','b','c'] if p != pos))
    print(f"Only position {pos} σ-fixed: {nonassoc_with_pos_fixed}/{total_pos_fixed} non-associative")

print("\n" + "="*70)
print("STEP 6: Distribution of LANDING values (L and R combined)")
print("="*70)

all_landings = Counter()
for t in triples:
    if t['gap']:
        all_landings[t['L']] += 1
        all_landings[t['R']] += 1

total_landings = sum(all_landings.values())
print(f"\nValues that appear as L or R in non-associative triples ({total_landings} total):")
for v in range(10):
    count = all_landings.get(v, 0)
    pct = 100 * count / total_landings if total_landings else 0
    
    # Classify v
    classes = []
    if v in sigma_fixed: classes.append("σ-fixed")
    if v in six_cycle: classes.append("6-cycle")
    if v in T_idempotent: classes.append("T-idempotent")
    if v == 0: classes.append("VOID")
    if v == 7: classes.append("HARMONY")
    cls_str = ", ".join(classes) if classes else "—"
    
    print(f"  {v} ({cls_str:<25}): {count} ({pct:.1f}%)")

print("\n" + "="*70)
print("STEP 7: Check signed gap (L - R) distribution")
print("="*70)

gap_dist = Counter(t['L_minus_R'] for t in triples if t['gap'])
print(f"\nDistribution of (L - R) for non-associative triples:")
for diff in sorted(gap_dist.keys()):
    count = gap_dist[diff]
    print(f"  L - R = {diff:+d}: {count}")

# Check directional bias
positive = sum(c for d, c in gap_dist.items() if d > 0)
negative = sum(c for d, c in gap_dist.items() if d < 0)
print(f"\nL > R: {positive} triples")
print(f"L < R: {negative} triples")
print(f"Balance: {'left-biased' if positive > negative else 'right-biased' if negative > positive else 'symmetric'}")

print("\n" + "="*70)
print("STEP 8: Inverting the analysis — where are the SOLID triples?")
print("="*70)

# What's the structure of the 50.2% that ARE associative?
assoc_landings = Counter()
for t in triples:
    if not t['gap']:
        assoc_landings[t['L']] += 1

total_assoc_landings = sum(assoc_landings.values())
print(f"\nValues that appear in ASSOCIATIVE triples (L = R), {total_assoc_landings} total:")
for v in range(10):
    count = assoc_landings.get(v, 0)
    pct = 100 * count / total_assoc_landings if total_assoc_landings else 0
    print(f"  {v}: {count} ({pct:.1f}%)")

print("\n" + "="*70)
print("STEP 9: Cross-tabulation — does σ-class of input correlate with output?")
print("="*70)

# For non-associative triples only:
# Classify input as (σ-fixed count, 6-cycle count) and see what (L,R) emerges
def classify_input(t):
    f = sum(1 for x in [t['a'],t['b'],t['c']] if x in sigma_fixed)
    c = sum(1 for x in [t['a'],t['b'],t['c']] if x in six_cycle)
    return (f, c)

input_class_to_LR = defaultdict(Counter)
for t in triples:
    if t['gap']:
        cls = classify_input(t)
        input_class_to_LR[cls][(t['L'], t['R'])] += 1

print("\nFor each input-class (σ-fixed count, 6-cycle count) → (L,R) distribution:")
for cls in sorted(input_class_to_LR.keys()):
    cnt = input_class_to_LR[cls]
    total = sum(cnt.values())
    print(f"\n  Input class (σ-fixed={cls[0]}, 6-cycle={cls[1]}, total triples: {total}):")
    for (L, R), c in sorted(cnt.items(), key=lambda x: -x[1])[:5]:
        print(f"    (L={L}, R={R}): {c} ({100*c/total:.1f}%)")

print("\n" + "="*70)
print("STEP 10: Save full landscape for hand-off")
print("="*70)

# Save the FULL list of non-associative triples to file
import json
nonassoc_list = [
    {
        'a': t['a'], 'b': t['b'], 'c': t['c'],
        'left_bracketing': int(t['L']),
        'right_bracketing': int(t['R']),
        'L_minus_R': t['L_minus_R'],
    }
    for t in triples if t['gap']
]

with open('/home/claude/gap_landscape/nonassoc_triples.json', 'w') as f:
    json.dump(nonassoc_list, f, indent=2)

print(f"\nSaved {len(nonassoc_list)} non-associative triples to nonassoc_triples.json")
print("This is the COMPLETE landscape — no filtering, no selection.")
print("Ready for TIG-canonical fuse-rule assignment by Brayden / Claude Code.")
