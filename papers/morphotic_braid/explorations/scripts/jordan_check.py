# PACKET: evening_handoff_2026_04_23/jordan_check.py
"""
Check: is TSML a Jordan-type magma?

Jordan identity: (x² · y) · x = x² · (y · x)
or equivalently: x²(xy) = x(x²y) for commutative groupoids

Also check related weak identities.
"""

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

def jordan_identity(T):
    """Jordan: x²(xy) = x(x²y) for commutative groupoid."""
    failures = []
    for x in range(N):
        for y in range(N):
            xx = T[x][x]
            xy = T[x][y]
            xxy = T[xx][y]
            lhs = T[xx][xy]
            rhs = T[x][xxy]
            if lhs != rhs:
                failures.append((x, y, lhs, rhs))
    return len(failures), failures

def right_bol(T):
    """((z·y)·x)·y = z·((y·x)·y)"""
    failures = 0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                lhs = T[T[T[z][y]][x]][y]
                rhs = T[z][T[T[y][x]][y]]
                if lhs != rhs: failures += 1
    return failures

def left_bol(T):
    """x·(y·(x·z)) = (x·(y·x))·z"""
    failures = 0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                lhs = T[x][T[y][T[x][z]]]
                rhs = T[T[x][T[y][x]]][z]
                if lhs != rhs: failures += 1
    return failures

def moufang(T):
    """Moufang identity: (x·y)·(z·x) = (x·(y·z))·x"""
    failures = 0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                lhs = T[T[x][y]][T[z][x]]
                rhs = T[T[x][T[y][z]]][x]
                if lhs != rhs: failures += 1
    return failures

def dm_diassociative(T):
    """Every pair (x, y) generates an associative subgroupoid.
    Equivalent for commutative: x(xy) = (xx)y, x(yy) = (xy)y."""
    for x in range(N):
        for y in range(N):
            if T[x][T[x][y]] != T[T[x][x]][y]: return False
            if T[x][T[y][y]] != T[T[x][y]][y]: return False
    return True

def check_idempotents_closure(T):
    """Do idempotents form a subsemigroup?"""
    idem = [x for x in range(N) if T[x][x] == x]
    for x in idem:
        for y in idem:
            if T[x][y] not in idem: 
                return False, idem, (x, y, T[x][y])
    return True, idem, None

print("="*70)
print("JORDAN and related identity tests for TSML")
print("="*70)

print("\nTSML:")
n_fail, examples = jordan_identity(TSML)
print(f"  Jordan identity x²(xy) = x(x²y): {n_fail} failures out of 100")
if n_fail > 0:
    print(f"    Example: (x=y={examples[0][0]},{examples[0][1]}): lhs={examples[0][2]}, rhs={examples[0][3]}")
else:
    print(f"    JORDAN IDENTITY HOLDS")

print(f"  Moufang: {moufang(TSML)} failures")
print(f"  Left Bol: {left_bol(TSML)} failures")
print(f"  Right Bol: {right_bol(TSML)} failures")
print(f"  Diassociative: {dm_diassociative(TSML)}")

closure, idem, ex = check_idempotents_closure(TSML)
print(f"  Idempotents: {idem}")
print(f"  Idempotents closed under T? {closure}")
if not closure:
    print(f"    Counterexample: T[{ex[0]}][{ex[1]}] = {ex[2]} not in idempotents")

print("\nBHML:")
n_fail, examples = jordan_identity(BHML)
print(f"  Jordan identity: {n_fail} failures")
print(f"  Moufang: {moufang(BHML)} failures")
print(f"  Diassociative: {dm_diassociative(BHML)}")

closure, idem, ex = check_idempotents_closure(BHML)
print(f"  Idempotents: {idem}")
print(f"  Idempotents closed under T? {closure}")

