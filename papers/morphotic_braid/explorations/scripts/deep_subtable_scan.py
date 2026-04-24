# PACKET: evening_handoff_2026_04_23/deep_subtable_scan.py
"""
Deeper scan:
1. Find the actual DISTINCT algebraic types hiding inside TSML
2. Scan BHML for substructures too (cross-table comparison)
3. Look specifically for alternative, Lie-adjacent, exotic categories
"""
from itertools import combinations

N = 10
TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 7, 7],  # wait let me double check
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],
]
# fix row 4 (COLLAPSE): (4,8) -> 8 per S_MAX
TSML[4] = [0, 7, 4, 7, 7, 7, 7, 7, 8, 7]

BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]

def is_closed(S, T):
    S_set = set(S)
    return all(T[x][y] in S_set for x in S for y in S)

def restricted(S, T):
    idx = {x: i for i, x in enumerate(S)}
    n = len(S)
    R = [[0]*n for _ in range(n)]
    for x in S:
        for y in S:
            R[idx[x]][idx[y]] = idx[T[x][y]]
    return R

# Property tests
def tests(R):
    n = len(R)
    comm = all(R[i][j] == R[j][i] for i in range(n) for j in range(n))
    assoc = all(R[R[i][j]][k] == R[i][R[j][k]] for i in range(n) for j in range(n) for k in range(n))
    ident = next((e for e in range(n) if all(R[e][i]==i and R[i][e]==i for i in range(n))), None)
    absb = next((a for a in range(n) if all(R[a][i]==a and R[i][a]==a for i in range(n))), None)
    quasi = all(sorted([R[i][j] for j in range(n)]) == list(range(n)) and sorted([R[j][i] for j in range(n)]) == list(range(n)) for i in range(n))
    jordan = all(R[R[x][x]][R[x][y]] == R[x][R[R[x][x]][y]] for x in range(n) for y in range(n))
    flex = all(R[a][R[b][a]] == R[R[a][b]][a] for a in range(n) for b in range(n))
    alt = all(R[R[a][a]][b] == R[a][R[a][b]] and R[R[a][b]][b] == R[a][R[b][b]] for a in range(n) for b in range(n))
    pow_assoc = True
    for x in range(n):
        xx = R[x][x]
        if R[xx][x] != R[x][xx]: pow_assoc = False; break
        xxx = R[xx][x]
        if R[xxx][x] != R[x][xxx] or R[x][xxx] != R[xx][xx]: pow_assoc = False; break
    idem_all = all(R[i][i]==i for i in range(n))
    return {'comm':comm,'assoc':assoc,'id':ident,'abs':absb,'quasi':quasi,'jordan':jordan,'flex':flex,'alt':alt,'pow':pow_assoc,'idem_all':idem_all}

def category_label(p):
    """Name the algebraic category based on property profile."""
    labels = []
    if p['assoc'] and p['quasi']:
        labels.append("GROUP" if p['id'] is not None else "assoc-quasigroup")
    elif p['assoc']:
        if p['id'] is not None and p['abs'] is not None: labels.append("MONOID-WITH-ZERO")
        elif p['id'] is not None: labels.append("MONOID")
        elif p['abs'] is not None: labels.append("ABSORBING-SEMIGROUP")
        else: labels.append("semigroup")
        if p['idem_all']: labels.append("band")
    else:
        if p['alt']: labels.append("ALTERNATIVE-nonassoc")
        elif p['jordan']: labels.append("JORDAN-nonassoc")
        if p['quasi']: labels.append("quasigroup-nonassoc")
        if not labels: labels.append("basic-magma")
    return ", ".join(labels)

def scan_table(T, name):
    print(f"\n{'='*70}")
    print(f"SCANNING {name} FOR SUBSTRUCTURES")
    print(f"{'='*70}")
    
    all_closed = []
    for size in range(1, N+1):
        for subset in combinations(range(N), size):
            if is_closed(subset, T):
                R = restricted(list(subset), T)
                p = tests(R)
                all_closed.append((subset, p))
    
    print(f"Total closed subsets: {len(all_closed)}")
    
    # Count by category
    cat_counts = {}
    cat_examples = {}
    for (s, p) in all_closed:
        cat = category_label(p)
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
        if cat not in cat_examples or len(s) < len(cat_examples[cat]):
            cat_examples[cat] = s
    
    print("\nCategory distribution:")
    for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        ex = cat_examples[cat]
        print(f"  {cat:45s} count={cnt:4d}  smallest example: {ex}")
    
    # Specifically look for exotic: ALTERNATIVE-nonassoc, GROUPs, quasigroups
    print("\nExotic finds (non-trivial):")
    found_exotic = False
    for (s, p) in all_closed:
        if p['alt'] and not p['assoc']:
            print(f"  ALTERNATIVE-nonassoc: {s}")
            found_exotic = True
        if p['assoc'] and p['quasi'] and p['id'] is not None and len(s) > 1:
            print(f"  GROUP of order {len(s)}: {s}")
            found_exotic = True
        if p['jordan'] and p['alt'] and not p['assoc']:
            print(f"  JORDAN+ALTERNATIVE-nonassoc: {s}")
            found_exotic = True
    if not found_exotic:
        print("  (none)")
    
    return all_closed

tsml_results = scan_table(TSML, "TSML")
bhml_results = scan_table(BHML, "BHML")

# Look at BHML more carefully — are there Jordan substructures?
print()
print("="*70)
print("DOES BHML CONTAIN JORDAN SUBSTRUCTURES?")
print("="*70)
bhml_jordan_subs = [(s, p) for (s, p) in bhml_results if p['jordan'] and not p['assoc']]
bhml_jordan_subs.sort(key=lambda x: len(x[0]))
print(f"BHML Jordan-nonassoc subtables: {len(bhml_jordan_subs)}")
for (s, p) in bhml_jordan_subs[:10]:
    print(f"  {s}")

bhml_associative_subs = [(s, p) for (s, p) in bhml_results if p['assoc']]
print(f"\nBHML associative subtables: {len(bhml_associative_subs)}")
for (s, p) in sorted(bhml_associative_subs, key=lambda x: len(x[0]))[:10]:
    cat = category_label(p)
    print(f"  {s}  [{cat}]")

