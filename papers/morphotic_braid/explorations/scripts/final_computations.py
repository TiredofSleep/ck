<!-- PACKET: evening_handoff_2026_04_23/final_computations.py -->
"""
Final computations before PC handoff.
1. Partial Task 3: 2-cell Moufang search bounded
2. Partial Task 4: small-primes det optimization  
3. Matrix commutator TSML_Jordan x TSML_Idempotent
4. TSML_Idempotent norm/trace/rank fingerprint
"""
import numpy as np
from itertools import combinations, product
import time

N = 10
TSML_Idempotent = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,1,7,7,7,7,7,7,7,7],
    [0,7,2,7,7,7,7,7,7,7],
    [0,7,7,3,7,7,7,7,7,7],
    [0,7,7,7,4,7,7,7,7,7],
    [0,7,7,7,7,5,7,7,7,7],
    [0,7,7,7,7,7,6,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,9],
]
TSML_Jordan = [
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

def mou_count(T):
    c = 0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                if T[T[x][y]][T[z][x]] == T[x][T[T[y][z]][x]]:
                    c += 1
    return c

def jord_count(T):
    c = 0
    for x in range(N):
        for y in range(N):
            if T[T[x][x]][T[x][y]] == T[x][T[T[x][x]][y]]:
                c += 1
    return c

# Task 3 — 2-cell perturbation search (bounded)
print("="*70)
print("TASK 3 PARTIAL: 2-cell Moufang search on TSML_Idempotent")
print("="*70)

body = [(i,j) for i in range(1,10) for j in range(i,10) if i != 7 and j != 7]
print(f"Body positions: {len(body)}")

best_mou = 830
best_cfg = None
t0 = time.time()
count = 0
for (i1,j1), (i2,j2) in combinations(body, 2):
    for v1, v2 in product(range(10), repeat=2):
        if v1 == 7 and v2 == 7: continue
        T = [row[:] for row in TSML_Idempotent]
        T[i1][j1] = T[j1][i1] = v1
        T[i2][j2] = T[j2][i2] = v2
        count += 1
        if count % 100000 == 0:
            print(f"  checked {count}, best={best_mou}, elapsed {time.time()-t0:.1f}s")
        if count > 500000:  # bounded
            print(f"  Stopped at {count} checks (time budget)")
            break
        m = mou_count(T)
        if m > best_mou:
            j = jord_count(T)
            r = np.linalg.matrix_rank(np.array(T))
            if r == 10 and j == 100:
                best_mou = m
                best_cfg = ((i1,j1,v1), (i2,j2,v2), m, r, j)
                print(f"  NEW: Mou={m}/1000, cells={best_cfg[:2]}, rank={r}, jord={j}/100")
    else:
        continue
    break

print(f"\nFinal: best Moufang count = {best_mou}/1000")
if best_cfg: print(f"Config: {best_cfg}")
print(f"Total checks: {count}, Time: {time.time()-t0:.1f}s")

# Task 4 — det optimization
print("\n" + "="*70)
print("TASK 4 PARTIAL: smaller-prime det search on TSML_Idempotent")
print("="*70)

def has_small_primes(n, allowed={2,3,5,7}):
    n = abs(n)
    if n == 0: return False
    for p in allowed:
        while n % p == 0: n //= p
    return n == 1

found = []
t0 = time.time()
count = 0
for cells in combinations(body, 2):  # 2-cell perturbations
    for vals in product(range(10), repeat=2):
        count += 1
        if count > 200000: break
        T = [row[:] for row in TSML_Idempotent]
        for (i,j), v in zip(cells, vals):
            T[i][j] = T[j][i] = v
        det = int(round(np.linalg.det(np.array(T, dtype=float))))
        if det != 0 and has_small_primes(det):
            j = jord_count(T)
            if j == 100:
                found.append((det, cells, vals, j))
    if count > 200000: break

print(f"Checked: {count}")
print(f"Clean-det configurations (primes ⊆ {{2,3,5,7}}) with Jordan=100%: {len(found)}")
if found:
    found.sort(key=lambda x: abs(x[0]))
    print(f"Top 5 smallest |det|:")
    for (d, cells, vals, j) in found[:5]:
        print(f"  det={d:>8d}, cells={cells}, vals={vals}, jord={j}/100")

# Commutator of TSML_Jordan and TSML_Idempotent
print("\n" + "="*70)
print("MATRIX COMMUTATOR: [M_TSML_Jordan, M_TSML_Idempotent]")
print("="*70)

M_J = np.array(TSML_Jordan, dtype=float)
M_I = np.array(TSML_Idempotent, dtype=float)
comm = M_J @ M_I - M_I @ M_J
print(f"Frobenius norm of commutator: {np.linalg.norm(comm):.3f}")
print(f"Rank: {np.linalg.matrix_rank(comm)}")
eigs = np.linalg.eigvals(comm)
print(f"Real parts of eigenvalues: {sorted([e.real for e in eigs], reverse=True)}")
print(f"Imaginary parts (abs): {sorted([abs(e.imag) for e in eigs], reverse=True)}")

# How anti-Hermitian?
sym = (comm + comm.T) / 2
antisym = (comm - comm.T) / 2
print(f"Symmetric part norm: {np.linalg.norm(sym):.3f}")
print(f"Antisymmetric part norm: {np.linalg.norm(antisym):.3f}")
print(f"Ratio (antisym/sym): {np.linalg.norm(antisym)/np.linalg.norm(sym):.3f}")

print("\n" + "="*70)
print("DONE - ready for handoff packaging")
print("="*70)
