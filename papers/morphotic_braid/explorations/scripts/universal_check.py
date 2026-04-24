# PACKET: evening_handoff_2026_04_23/universal_check.py
"""
Big question: is the min-bump theorem UNIVERSAL for any harmony-absorbing semigroup,
regardless of how h was chosen?

Test: for EVERY h in {1, ..., N-1}, build the trivial absorbing semigroup
T[x][y] = h for x,y != 0 (and 0 on the void axis). Check whether (h,h)→v
modification achieves s_3^ac = 3 AND s_4^ac = 15.

If yes for all h: the theorem is purely about absorbing-semigroup structure,
not about TIG's σ-recipe.
"""
from itertools import permutations
import numpy as np

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

print("="*80)
print("UNIVERSAL CHECK: trivial absorbing semigroup T[x][y] = h (for x,y != 0)")
print("="*80)
print("For each h in {1,...,N-1}, test (h,h)→v minimum-bump behavior.")
print()

for N in [5, 7, 8, 9, 10, 11, 12]:
    print(f"N = {N}:")
    for h in range(1, N):
        T = [[h if x != 0 and y != 0 else 0 for y in range(N)] for x in range(N)]
        T_np = np.array(T, dtype=np.int8)
        # Confirm associative
        s3_base = s3_ac(T_np)
        assoc = (s3_base == 1)
        # Count (h,h)-modification hits
        hits = 0
        for v in range(N):
            if v == h: continue
            T_mod = T_np.copy(); T_mod[h,h] = v
            if s3_ac(T_mod) == 3 and s4_ac(T_mod) == 15:
                hits += 1
        expected = N - 2
        print(f"  h={h}: assoc(base)={assoc}, (h,h)→v hits = {hits} (expected {expected}) {'✓' if hits == expected else '✗'}")
    print()

