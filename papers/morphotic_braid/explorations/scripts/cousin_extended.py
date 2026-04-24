# PACKET: evening_handoff_2026_04_23/cousin_extended.py
"""
Extend the cousin-family search to:
1. Different N structures: 2p vs pq vs p^2 
2. Characterize h-patterns more precisely
3. Test whether the minimum-bump theorem holds for cousin families
"""

from math import gcd
from itertools import permutations
import numpy as np

def nu(p, n):
    if n == 0: return 999
    k = 0
    while n % p == 0: n //= p; k += 1
    return k

def units(N):
    return [u for u in range(1, N) if gcd(u, N) == 1]

def build_C0_variant(N, sigma_fn, target_sigma=1):
    u_list = units(N)
    sig = {u: sigma_fn(u) for u in u_list}
    cands = [u for u in u_list if u % 2 == 1 and sig[u] == target_sigma]
    if not cands: return None, None, None
    h = max(cands)
    core = [u for u in u_list if sig[u] == target_sigma]
    T = [[0]*N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if x == 0 or y == 0: T[x][y] = 0
            elif x not in core or y not in core: T[x][y] = h
            else:
                sx, sy = sig[x], sig[y]
                if sx < sy: T[x][y] = x
                elif sy < sx: T[x][y] = y
                else: T[x][y] = h
    return T, h, core

def s3_ac(T):
    T = np.array(T, dtype=np.int8); N = len(T)
    brks = [lambda a,b,c,T: T[T[a,b],c], lambda a,b,c,T: T[a,T[b,c]]]
    xs = np.repeat(np.arange(N), N*N).astype(np.int8)
    ys = np.tile(np.repeat(np.arange(N), N), N).astype(np.int8)
    zs = np.tile(np.arange(N), N*N).astype(np.int8)
    fps = set()
    for perm in permutations(range(3)):
        tr = [xs, ys, zs]; p = [tr[i] for i in perm]
        for brk in brks: fps.add(bytes(brk(*p, T).tobytes()))
    return len(fps)

def s4_ac(T):
    T = np.array(T, dtype=np.int8); N = len(T)
    brks = [
        lambda a,b,c,d,T: T[T[T[a,b],c],d],
        lambda a,b,c,d,T: T[T[a,T[b,c]],d],
        lambda a,b,c,d,T: T[T[a,b],T[c,d]],
        lambda a,b,c,d,T: T[a,T[T[b,c],d]],
        lambda a,b,c,d,T: T[a,T[b,T[c,d]]],
    ]
    xs = np.repeat(np.arange(N), N**3).astype(np.int8)
    ys = np.tile(np.repeat(np.arange(N), N**2), N).astype(np.int8)
    zs = np.tile(np.repeat(np.arange(N), N), N**2).astype(np.int8)
    ws = np.tile(np.arange(N), N**3).astype(np.int8)
    fps = set()
    for perm in permutations(range(4)):
        tr = [xs, ys, zs, ws]; p = [tr[i] for i in perm]
        for brk in brks: fps.add(bytes(brk(*p, T).tobytes()))
    return len(fps)

# =============================================
# Test 1: Different N structures
# =============================================
print("="*80)
print("TEST 1: How the TIG recipe (3u+1) performs on different N structures")
print("="*80)
print(f"{'N':>4} {'structure':15s} {'units':25s} {'h':>4} {'core':>12}")

N_types = [
    (10, "2·5 (TIG)"),
    (12, "2^2·3"),
    (14, "2·7"),
    (15, "3·5"),
    (16, "2^4"),
    (18, "2·3^2"),
    (20, "2^2·5"),
    (21, "3·7"),
    (22, "2·11"),
    (25, "5^2"),
    (35, "5·7"),
]

recipe = lambda u: nu(2, 3*u + 1)
for N, struct in N_types:
    T, h, core = build_C0_variant(N, recipe)
    u_str = str(units(N))[:25]
    h_str = str(h) if h is not None else '-'
    core_str = str(core) if core is not None else '-'
    print(f"{N:>4} {struct:15s} {u_str:25s} {h_str:>4} {core_str:>12}")

# =============================================
# Test 2: Find minimum bump for cousin families
# =============================================
print()
print("="*80)
print("TEST 2: Minimum bump theorem across cousin recipes at N=10")
print("="*80)
print("For each cousin recipe giving valid C_0 on Z/10Z:")
print("  - Find all single-cell perturbations achieving s_3^ac=3 AND s_4^ac=15")
print("  - Report: at what cell are the hits? (is h-centering universal?)")
print()

recipes_test = [
    (lambda u: nu(2, 3*u + 1), "TIG: nu_2(3u+1)"),
    (lambda u: nu(2, 3*u - 1), "variant: nu_2(3u-1)"),
    (lambda u: nu(2, u + 1), "variant: nu_2(u+1)"),
    (lambda u: nu(2, 5*u + 1), "variant: nu_2(5u+1)"),
]

for rec, name in recipes_test:
    T, h, core = build_C0_variant(10, rec)
    if T is None:
        print(f"{name}: C_0 not defined at N=10")
        continue
    if s3_ac(np.array(T, dtype=np.int8)) != 1:
        print(f"{name}: C_0 not associative at N=10")
        continue
    
    T_np = np.array(T, dtype=np.int8)
    hits = []
    for i in range(10):
        for j in range(10):
            if T[i][j] == 0: continue  # skip VOID
            for v in range(10):
                if v == T[i][j]: continue
                T_mod = T_np.copy(); T_mod[i,j] = v
                if s3_ac(T_mod) == 3 and s4_ac(T_mod) == 15:
                    hits.append(((i,j), v))
    
    positions = set(hit[0] for hit in hits)
    all_at_hh = all(pos == (h, h) for pos in positions)
    print(f"\n{name}")
    print(f"  h = {h}, C_0 associative = YES")
    print(f"  Single-cell hits: {len(hits)}, positions: {positions}")
    print(f"  All at (h,h)=({h},{h})? {all_at_hh}")
    if all_at_hh:
        vals = sorted(set(hit[1] for hit in hits))
        print(f"  Values v that work: {vals}")

# =============================================
# Test 3: Is this recipe-specific or universal?
# =============================================
print()
print("="*80)
print("TEST 3: For all cousin families, is h ALWAYS the minimum-bump site?")
print("="*80)
print("If yes: the minimum-bump-at-h theorem is a UNIVERSAL law of this construction,")
print("        not specific to the (3u+1) recipe.")

