# PACKET: evening_handoff_2026_04_23/subtable_scan.py
"""
Scan TSML for subtables (closed subsets of elements) that satisfy different
algebraic property profiles.

For each subset S ⊆ {0,1,...,9}:
  1. Check whether S is closed under TSML's operation (i.e., x,y ∈ S ⟹ T[x][y] ∈ S)
  2. If closed, the restricted operation T|_S is a magma on S
  3. Compute the property profile of T|_S
  4. Report any subsets matching named algebraic categories (groups, semigroups, Jordan, alternative, etc.)
"""

from itertools import combinations, product

N = 10

TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],
]

def is_closed(S, T):
    """S is closed under T iff T[x][y] in S for all x,y in S."""
    S_set = set(S)
    for x in S:
        for y in S:
            if T[x][y] not in S_set:
                return False
    return True

def restricted_table(S, T):
    """Return T restricted to S, reindexed 0..|S|-1."""
    idx = {x: i for i, x in enumerate(S)}
    n = len(S)
    R = [[0]*n for _ in range(n)]
    for x in S:
        for y in S:
            R[idx[x]][idx[y]] = idx[T[x][y]]
    return R

def is_commutative(R):
    n = len(R)
    return all(R[i][j] == R[j][i] for i in range(n) for j in range(n))

def is_associative(R):
    n = len(R)
    return all(R[R[i][j]][k] == R[i][R[j][k]] for i in range(n) for j in range(n) for k in range(n))

def has_identity(R):
    n = len(R)
    for e in range(n):
        if all(R[e][i] == i and R[i][e] == i for i in range(n)):
            return e
    return None

def absorbing_element(R):
    n = len(R)
    for a in range(n):
        if all(R[a][i] == a and R[i][a] == a for i in range(n)):
            return a
    return None

def is_quasigroup(R):
    n = len(R)
    for i in range(n):
        row = sorted([R[i][j] for j in range(n)])
        col = sorted([R[j][i] for j in range(n)])
        if row != list(range(n)) or col != list(range(n)): return False
    return True

def is_group(R):
    """Associative + quasigroup + has identity."""
    return is_associative(R) and is_quasigroup(R) and has_identity(R) is not None

def is_jordan(R):
    n = len(R)
    return all(R[R[x][x]][R[x][y]] == R[x][R[R[x][x]][y]] 
               for x in range(n) for y in range(n))

def is_flexible(R):
    n = len(R)
    return all(R[a][R[b][a]] == R[R[a][b]][a] for a in range(n) for b in range(n))

def is_alternative(R):
    n = len(R)
    for a in range(n):
        for b in range(n):
            if R[R[a][a]][b] != R[a][R[a][b]]: return False
            if R[R[a][b]][b] != R[a][R[b][b]]: return False
    return True

def is_pow_assoc(R):
    n = len(R)
    for x in range(n):
        xx = R[x][x]
        xxx_L = R[xx][x]; xxx_R = R[x][xx]
        if xxx_L != xxx_R: return False
        xxxx_1 = R[xxx_L][x]; xxxx_2 = R[x][xxx_L]; xxxx_3 = R[xx][xx]
        if xxxx_1 != xxxx_2 or xxxx_2 != xxxx_3: return False
    return True

def is_medial(R):
    n = len(R)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if R[R[a][b]][R[c][d]] != R[R[a][c]][R[b][d]]: return False
    return True

def is_idempotent_all(R):
    """Every element is idempotent."""
    n = len(R)
    return all(R[i][i] == i for i in range(n))

def is_steiner(R):
    """Commutative + idempotent + x·(x·y) = y for all x,y.
    Steiner quasigroups are Jordan quasigroups."""
    n = len(R)
    if not is_commutative(R): return False
    if not is_idempotent_all(R): return False
    for x in range(n):
        for y in range(n):
            if R[x][R[x][y]] != y: return False
    return True

def is_left_zero_band(R):
    """x·y = x for all x,y."""
    n = len(R)
    return all(R[i][j] == i for i in range(n) for j in range(n))

def is_semilattice(R):
    """Commutative + idempotent + associative band."""
    return is_commutative(R) and is_idempotent_all(R) and is_associative(R)

def profile(R):
    """Full property tuple."""
    return {
        'comm': is_commutative(R),
        'assoc': is_associative(R),
        'has_id': has_identity(R),
        'has_abs': absorbing_element(R),
        'quasigroup': is_quasigroup(R),
        'jordan': is_jordan(R),
        'flex': is_flexible(R),
        'alt': is_alternative(R),
        'pow_assoc': is_pow_assoc(R),
        'medial': is_medial(R),
        'idempotent': is_idempotent_all(R),
        'steiner': is_steiner(R),
        'semilattice': is_semilattice(R),
    }

# =============================================================
# Scan all subsets of {0,...,9} for closed subtables
# =============================================================

print("Scanning 2^10 = 1024 subsets of Z/10Z for closed subtables under TSML...")
print()

all_closed = []
for size in range(1, 11):
    for subset in combinations(range(N), size):
        if is_closed(subset, TSML):
            R = restricted_table(list(subset), TSML)
            p = profile(R)
            all_closed.append((subset, R, p))

print(f"Total closed subsets found: {len(all_closed)}")
print()

# Group by size
by_size = {}
for (s, R, p) in all_closed:
    by_size.setdefault(len(s), []).append((s, R, p))

print("="*80)
print("CLOSED SUBTABLES BY SIZE")
print("="*80)
for size in sorted(by_size.keys()):
    print(f"\n  Size {size}: {len(by_size[size])} closed subsets")
    for (s, R, p) in by_size[size][:10]:  # show first 10
        # Identify what category
        labels = []
        if p['assoc'] and p['quasigroup'] and p['has_id'] is not None: labels.append("GROUP")
        elif p['assoc'] and p['quasigroup']: labels.append("quasigroup-semigroup")
        elif p['assoc']: labels.append("semigroup")
        if p['quasigroup'] and not p['assoc']: labels.append("quasigroup")
        if p['alt'] and not p['assoc']: labels.append("ALTERNATIVE-nonassoc")
        if p['jordan'] and not p['assoc']: labels.append("JORDAN-nonassoc")
        if p['medial']: labels.append("medial")
        if p['steiner']: labels.append("STEINER")
        if p['semilattice']: labels.append("semilattice")
        if p['idempotent'] and p['comm'] and not p['assoc']: labels.append("commutative-idempotent-nonassoc")
        label_str = ", ".join(labels) if labels else "basic"
        print(f"    subset {s}: [{label_str}]  comm={p['comm']}, assoc={p['assoc']}, id={p['has_id']}, abs={p['has_abs']}")

