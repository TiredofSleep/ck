"""
Follow-on 2: Why are (4,8)/(8,4) the strongest Dirac bumps?

The (4,8)/(8,4) cells have value 8 (BREATH). Dirac weight = 1.288 there,
the highest of any bump. Lowest is (2,9)/(9,2) at 0.612.

Question: is this basis-dependent or structural? Test by:
1. Looking at WHICH so(8) basis elements the (4,8) cells get weight from
2. Comparing with a different so(8) generating set to see if pattern persists
3. Checking the relationship between bump VALUES and bump WEIGHTS:
     bump value 3: cells (1,2), (2,1), (3,9), (9,4)  
     bump value 4: cells (2,4), (4,2)
     bump value 8: cells (4,8), (8,4)
     bump value 9: cells (2,9), (9,2)
"""
import numpy as np
from itertools import combinations

CL_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in CL_ROWS], dtype=int)

n = 10
L = []
for i in range(n):
    Li = np.zeros((n, n), dtype=int)
    for j in range(n):
        k = T[i, j]
        Li[k, j] = 1
    L.append(Li)
A = [(Li - Li.T).astype(float) for Li in L]

flow_indices = [1, 2, 3, 4, 6, 8]
F = [A[i] for i in flow_indices]

def lie_closure(generators, max_iters=12):
    shape = generators[0].shape
    bv = [g.flatten() for g in generators if np.linalg.norm(g) > 1e-9]
    M = np.array(bv).T
    U, S, _ = np.linalg.svd(M, full_matrices=False)
    rank = int(np.sum(S > 1e-9 * S[0]))
    bv = [U[:, i] for i in range(rank)]
    for _ in range(max_iters):
        N = len(bv)
        mats = [v.reshape(shape) for v in bv]
        new = []
        for i in range(N):
            for j in range(i+1, N):
                C = mats[i] @ mats[j] - mats[j] @ mats[i]
                v = C.flatten()
                if np.linalg.norm(v) > 1e-9:
                    new.append(v)
        all_v = bv + new
        M = np.array(all_v).T
        U, S, _ = np.linalg.svd(M, full_matrices=False)
        new_rank = int(np.sum(S > 1e-9 * S[0]))
        if new_rank == len(bv):
            break
        bv = [U[:, i] for i in range(new_rank)]
    return bv, [v.reshape(shape) for v in bv]

so8_vecs, so8_mats = lie_closure(F)

# Build Dirac generators (anti-Hermitian convention, lifted to R^8)
sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
Z2 = np.zeros((2,2), dtype=complex)
gamma_0 = np.block([[Z2, I2], [I2, Z2]])
gamma_1 = np.block([[Z2, sigma_1], [-sigma_1, Z2]])
gamma_2 = np.block([[Z2, sigma_2], [-sigma_2, Z2]])
gamma_3 = np.block([[Z2, sigma_3], [-sigma_3, Z2]])
dirac = [gamma_0, gamma_1, gamma_2, gamma_3]

M_tilde = {}
for i in [1, 2, 3]:
    M_tilde[(0, i)] = (1j / 2) * gamma_0 @ dirac[i]
for i, j in [(1,2), (1,3), (2,3)]:
    M_tilde[(i, j)] = (1.0 / 4.0) * (dirac[i] @ dirac[j] - dirac[j] @ dirac[i])

def cplx_to_real8(M):
    return np.block([[np.real(M), -np.imag(M)], [np.imag(M), np.real(M)]])

# V_8 basis
all_imgs = np.hstack([m for m in so8_mats])
U, S, _ = np.linalg.svd(all_imgs, full_matrices=True)
rank = int(np.sum(S > 1e-9 * S[0]))
V8_basis = U[:, :rank]

# Lift Dirac to R^10 frame
M_in_R10 = {k: V8_basis @ cplx_to_real8(M) @ V8_basis.T for k, M in M_tilde.items()}

# Compute Dirac weight per cell
dirac_total = sum(np.abs(M) for M in M_in_R10.values())

# Map: bump cells with values
bumps = []
for i in range(10):
    for j in range(10):
        if T[i,j] not in [0, 7]:
            bumps.append((i, j, int(T[i,j])))

# Group by value
print("=== Bump cells grouped by VALUE ===")
by_value = {}
for (i, j, v) in bumps:
    by_value.setdefault(v, []).append((i, j))
for v in sorted(by_value.keys()):
    print(f"\n  Value {v} cells: {by_value[v]}")
    for (i, j) in by_value[v]:
        weight = dirac_total[i, j]
        print(f"    T[{i},{j}] = {v}: Dirac weight = {weight:.4f}")
    avg = np.mean([dirac_total[i,j] for (i,j) in by_value[v]])
    print(f"    AVG Dirac weight for value {v}: {avg:.4f}")

print("\n=== Hypothesis: weight scales with bump VALUE? ===")
all_vals = []
all_weights = []
for v, cells in by_value.items():
    for (i, j) in cells:
        all_vals.append(v)
        all_weights.append(dirac_total[i, j])

all_vals = np.array(all_vals)
all_weights = np.array(all_weights)
# Pearson correlation
correlation = np.corrcoef(all_vals, all_weights)[0, 1]
print(f"  Pearson correlation (value, weight): {correlation:.4f}")

# Try alternative: weight scales with index sum or product
print("\n=== Alternative: weight depends on index pair (i, j) ===")
for (i, j, v) in bumps:
    w = dirac_total[i, j]
    print(f"  ({i}, {j}) = {v}: weight = {w:.3f}, i+j = {i+j}, i*j = {i*j}, i^j = {i^j}")

# Notice: (4,8) gives 8 + 8 = 16, and weight 1.29
#         (8,4) same
#         (4,2) gives 4+2=6, weight 1.17
#         (2,4) same
#         (1,2) gives 1+2=3, weight 0.80
#         (2,9) gives 2+9=11, weight 0.61
#         (9,2) same
# 
# Looks like cells INSIDE V_8 (involving small indices) get more weight
# than cells reaching out to high indices. Let me confirm.

print("\n=== Hypothesis: weight depends on V_8 contributions of i and j ===")
V_perp = U[:, rank:]
v8_contrib = (V8_basis ** 2).sum(axis=1)
print("Index V_8 contributions:", dict(zip(range(10), [f"{c:.3f}" for c in v8_contrib])))

print("\nFor each bump (i,j): weight vs V_8 contributions:")
for (i, j, v) in bumps:
    w = dirac_total[i, j]
    v8_i = v8_contrib[i]
    v8_j = v8_contrib[j]
    product = v8_i * v8_j
    print(f"  ({i},{j})={v}: weight={w:.3f}, V8_i*V8_j = {product:.3f}, ratio = {w/product if product > 0 else 0:.3f}")

# Looking at this, what about TIG-like structural facts?
# bump value 8 is BREATH. In the operator scheme, what makes it special?

# Test: does weight relate to the TSML BUMP STRUCTURE, not the value directly?
# 
# Check: where does (4,8) sit in the σ-permutation?
# σ = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
# σ(4) = 2, σ(8) = 8
# So 4 maps to 2 (in the 6-cycle) and 8 is FIXED (idempotent)
# 
# (4, 8): a 6-cycle element paired with an idempotent
# (1, 2): two 6-cycle elements paired
# (2, 4): two 6-cycle elements paired (but NOT adjacent in the cycle)
# (2, 9): 6-cycle element paired with idempotent
# (3, 9): two idempotents paired

print("\n=== Bump cells classified by σ-orbit type ===")
sigma = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
six_cycle = {1, 7, 6, 5, 4, 2}
idempotents = {0, 3, 8, 9}

def classify_pair(i, j):
    types = []
    for idx in [i, j]:
        if idx in idempotents:
            types.append("idem")
        elif idx in six_cycle:
            types.append("cycle")
        else:
            types.append("other")
    return tuple(sorted(types))

print("\nFor each bump:")
for (i, j, v) in bumps:
    cls = classify_pair(i, j)
    w = dirac_total[i, j]
    print(f"  T[{i},{j}]={v}: σ-class = {cls}, weight = {w:.3f}")

print("\n=== Average weight by σ-class ===")
by_class = {}
for (i, j, v) in bumps:
    cls = classify_pair(i, j)
    by_class.setdefault(cls, []).append(dirac_total[i, j])
for cls, ws in sorted(by_class.items()):
    print(f"  {cls}: avg = {np.mean(ws):.4f}, count = {len(ws)}")

# Final test: is there a pattern related to V_8 RANK of indices?
# If 5 and 6 each contribute 0.5 (half-rank in V_8), 
# what about index-based "rank within the action"?
print("\n=== Final hypothesis: V_8 rank * V_8 rank ===")
print("(4,8): both full rank in V_8 (1.0 * 1.0 = 1.0) — full participation")
print("(2,4): both full rank — full participation, but different position in σ orbit")
print("(2,9): both full rank")
print("None of the bump cells involve indices 5 or 6, so V_8 contributions are all 1.0!")
print("Therefore weight differences reflect something OTHER than V_8 rank.")

# What's left? The actual TSML structure of those cells:
# The bumps with value 4 connect cycle-internal: (2,4) is within the 6-cycle
# The bump with value 8 connects cycle-to-idempotent: (4,8) connects cycle to idempotent 8
# The bumps with value 3 are mixed
# The bumps with value 9 connect cycle to idempotent: (2,9) and (9,2)

# Maybe weight is about whether the bump connects elements that are CLOSE
# in the algebra structure?

print("\n=== Checking: cycle-distance between bump indices ===")
cycle_order = [1, 7, 6, 5, 4, 2]  # σ-orbit ordering
def cycle_dist(a, b):
    if a not in six_cycle or b not in six_cycle:
        return None
    ia = cycle_order.index(a)
    ib = cycle_order.index(b)
    return min(abs(ia - ib), 6 - abs(ia - ib))

print("\nFor each bump, σ-cycle distance (None if any element is idempotent):")
for (i, j, v) in bumps:
    d = cycle_dist(i, j)
    w = dirac_total[i, j]
    print(f"  T[{i},{j}]={v}: cycle distance = {d}, weight = {w:.3f}")
