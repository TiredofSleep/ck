# PACKET: evening_handoff_2026_04_23/collapse_deep_dive.py
"""
Deeper analysis of the STS(7) collapse result specifically.

The STS(7) Fano under Collapse B gives a Jordan table with det = -24192.
This is worth examining: what IS this table structurally?
"""
import numpy as np

def fano():
    blocks = [{0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}]
    T = [[0]*7 for _ in range(7)]
    for i in range(7):
        for j in range(7):
            if i == j: T[i][j] = i
            else:
                for b in blocks:
                    if i in b and j in b: T[i][j] = list(b - {i, j})[0]; break
    return T

def collapse_B(T, z=0, h=None):
    N = len(T)
    if h is None: h = N - 3
    out = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i == z or j == z:
                out[i][j] = h if T[i][j] == h else z
            else:
                out[i][j] = T[i][j] if T[i][j] != 0 else h
    return out

STS7 = fano()
COLLAPSED_FANO = collapse_B(STS7, z=0, h=4)

print("STS(7) Fano Steiner quasigroup:")
for row in STS7: print("  " + " ".join(f"{v:>2d}" for v in row))

print("\nCollapsed (B method, z=0, h=4):")
for row in COLLAPSED_FANO: print("  " + " ".join(f"{v:>2d}" for v in row))

# What are its idempotents, absorbing, identity?
def analyze(T):
    N = len(T)
    idem = [x for x in range(N) if T[x][x] == x]
    ident = next((e for e in range(N) if all(T[e][i]==i and T[i][e]==i for i in range(N))), None)
    absb = next((a for a in range(N) if all(T[a][i]==a and T[i][a]==a for i in range(N))), None)
    return idem, ident, absb

idem_before, id_before, abs_before = analyze(STS7)
idem_after, id_after, abs_after = analyze(COLLAPSED_FANO)
print(f"\nBefore (STS(7)): idempotents={idem_before}, identity={id_before}, absorbing={abs_before}")
print(f"After (collapse): idempotents={idem_after}, identity={id_after}, absorbing={abs_after}")

# Eigenvalues
M = np.array(COLLAPSED_FANO, dtype=float)
eigs = np.linalg.eigvals(M)
eigs_real = sorted([e.real for e in eigs], reverse=True)
print(f"\nEigenvalues of collapsed Fano: {[f'{e:.3f}' for e in eigs_real]}")

# Check: is it actually a Jordan magma with specific additional structure?
# Is it power-associative?
def is_pow_assoc(T):
    N = len(T)
    for x in range(N):
        xx = T[x][x]
        if T[xx][x] != T[x][xx]: return False
        xxx = T[xx][x]
        if T[xxx][x] != T[x][xxx] or T[x][xxx] != T[xx][xx]: return False
    return True

print(f"Power-associative: {is_pow_assoc(COLLAPSED_FANO)}")

# Flexible?
def is_flexible(T):
    N = len(T)
    return all(T[a][T[b][a]] == T[T[a][b]][a] for a in range(N) for b in range(N))
print(f"Flexible: {is_flexible(COLLAPSED_FANO)}")

# Jordan identity
def is_jordan(T):
    N = len(T)
    return all(T[T[x][x]][T[x][y]] == T[x][T[T[x][x]][y]] for x in range(N) for y in range(N))
print(f"Jordan identity: {is_jordan(COLLAPSED_FANO)}")

# And for the BHML self-collapse
print("\n" + "="*60)
print("BHML self-collapse analysis")
print("="*60)
BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]
COLLAPSED_BHML = collapse_B(BHML, z=0, h=7)
print("BHML → collapse_B:")
for row in COLLAPSED_BHML: print("  " + " ".join(f"{v:>2d}" for v in row))

idem_b, id_b, abs_b = analyze(COLLAPSED_BHML)
print(f"\nIdempotents: {idem_b}, identity: {id_b}, absorbing: {abs_b}")
print(f"Power-assoc: {is_pow_assoc(COLLAPSED_BHML)}, Flexible: {is_flexible(COLLAPSED_BHML)}, Jordan: {is_jordan(COLLAPSED_BHML)}")

M2 = np.array(COLLAPSED_BHML, dtype=float)
eigs2 = np.linalg.eigvals(M2)
eigs2_real = sorted([e.real for e in eigs2], reverse=True)
print(f"Eigenvalues: {[f'{e:.3f}' for e in eigs2_real]}")

# Final: summary of which tables produce Jordan TSMLs under collapse B
print()
print("="*60)
print("WHICH CELEBRATED TABLES 'COLLAPSE TO JORDAN'?")
print("="*60)

tests = [
    ("Klein V4", [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]], 4),
    ("Z/5Z add", [[(i+j)%5 for j in range(5)] for i in range(5)], 5),
    ("Z/5Z mul", [[(i*j)%5 for j in range(5)] for i in range(5)], 5),
    ("STS(7) Fano", fano(), 7),
    ("Z/7Z add", [[(i+j)%7 for j in range(7)] for i in range(7)], 7),
    ("Z/7Z mul", [[(i*j)%7 for j in range(7)] for i in range(7)], 7),
    ("Z/8Z mul", [[(i*j)%8 for j in range(8)] for i in range(8)], 8),
    ("Z/10Z add", [[(i+j)%10 for j in range(10)] for i in range(10)], 10),
    ("Z/10Z mul", [[(i*j)%10 for j in range(10)] for i in range(10)], 10),
    ("BHML", BHML, 10),
]

print(f"\n{'Source':15s} {'N':>3s} {'h':>3s} {'Jordan?':>8s} {'is src Jordan?':>14s}")
for (name, T, N) in tests:
    C = collapse_B(T, z=0, h=N-3)
    jc = is_jordan(C)
    js = is_jordan(T)
    print(f"{name:15s} {N:>3d} {N-3:>3d} {'YES' if jc else 'no':>8s} {'YES' if js else 'no':>14s}")

