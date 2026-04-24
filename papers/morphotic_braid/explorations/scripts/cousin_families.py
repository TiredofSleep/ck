<!-- PACKET: evening_handoff_2026_04_23/cousin_families.py -->
"""
Explore structural cousins of the σ-based C_0 family.

TSML's recipe: canonical operator on Z/NZ with h = max odd unit having
sigma(u) = nu_2(3u+1) = 1. This is specifically the "3u+1" recipe.

What about variants?
  A) nu_2(au + b) for other (a, b)
  B) nu_p(u) for primes p != 2
  C) different divisibility conditions
  D) multiplicative order-based families

For each variant family, check:
  - Which N admits a canonical h?
  - Does C_0 remain associative?
  - Is the minimum-bump theorem same structure?
  - Does h ∈ {3,7} hold, or different?
"""

from math import gcd
from itertools import permutations
import numpy as np

def nu(p, n):
    if n == 0: return 999
    k = 0
    while n % p == 0:
        n //= p; k += 1
    return k

def units(N):
    return [u for u in range(1, N) if gcd(u, N) == 1]

# Sigma variants: sigma_rule returns sigma(u) given u; we look for "nice" h elements
def build_C0_variant(N, sigma_fn, target_sigma=1):
    """Build C_0 on Z/NZ using a custom sigma function. 
    h = max odd unit with sigma(u) = target_sigma."""
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

# Variant A: nu_2(au + b) for (a, b) in small combinations
print("="*80)
print("VARIANT A: nu_2(au + b) recipes")
print("="*80)
print(f"{'recipe':20s} {'N=10 h':>8} {'N=14 h':>8} {'N=22 h':>8} {'C_0 assoc?':>12}")

# Test several (a,b) pairs
recipes_A = [
    (1, 0, "nu_2(u)"),       # just 2-adic valuation of u — but u is odd unit so this is 0
    (3, 1, "nu_2(3u+1)"),    # canonical TIG
    (3, -1, "nu_2(3u-1)"),   # variant
    (1, 1, "nu_2(u+1)"),     # simpler
    (5, 1, "nu_2(5u+1)"),    # different multiplier
    (1, 2, "nu_2(u+2)"),     
    (3, 2, "nu_2(3u+2)"),
]

for (a, b, name) in recipes_A:
    row_h = []
    assoc_at_10 = "N/A"
    for N in [10, 14, 22]:
        T, h, core = build_C0_variant(N, lambda u, a=a, b=b: nu(2, a*u + b))
        row_h.append(str(h) if h is not None else '-')
        if N == 10 and T is not None:
            assoc_at_10 = "YES" if s3_ac(T) == 1 else "NO"
    print(f"{name:20s} {row_h[0]:>8} {row_h[1]:>8} {row_h[2]:>8} {assoc_at_10:>12}")

print()
print("="*80)
print("VARIANT B: nu_p(3u+1) for p != 2 (different primes)")
print("="*80)
print(f"{'recipe':20s} {'N=10 h':>8} {'N=14 h':>8} {'N=22 h':>8} {'C_0 assoc?':>12}")
recipes_B = [
    (3, "nu_3(3u+1)"),
    (5, "nu_5(3u+1)"),
    (7, "nu_7(3u+1)"),
]
for (p, name) in recipes_B:
    row_h = []
    assoc_at_10 = "N/A"
    for N in [10, 14, 22]:
        T, h, core = build_C0_variant(N, lambda u, p=p: nu(p, 3*u + 1))
        row_h.append(str(h) if h is not None else '-')
        if N == 10 and T is not None:
            assoc_at_10 = "YES" if s3_ac(T) == 1 else "NO"
    print(f"{name:20s} {row_h[0]:>8} {row_h[1]:>8} {row_h[2]:>8} {assoc_at_10:>12}")

print()
print("="*80)
print("VARIANT C: multiplicative order-based sigma")
print("="*80)
print(f"{'recipe':20s} {'N=10 h':>8} {'N=14 h':>8} {'N=22 h':>8} {'C_0 assoc?':>12}")

def mult_order(u, N):
    """Order of u in (Z/NZ)^*."""
    if gcd(u, N) != 1: return 999
    k = 1
    v = u % N
    while v != 1:
        v = (v * u) % N
        k += 1
        if k > N: return 999
    return k

recipes_C = [
    ("mult_order", "mult_order_u_mod_N"),
]
for (name, desc) in recipes_C:
    row_h = []
    assoc_at_10 = "N/A"
    for N in [10, 14, 22]:
        T, h, core = build_C0_variant(N, lambda u, N=N: mult_order(u, N), target_sigma=1)
        # target_sigma = 1 means: u is a fixed point of multiplication (only u=1 usually)
        row_h.append(str(h) if h is not None else '-')
        if N == 10 and T is not None:
            assoc_at_10 = "YES" if s3_ac(T) == 1 else "NO"
    print(f"{desc:20s} {row_h[0]:>8} {row_h[1]:>8} {row_h[2]:>8} {assoc_at_10:>12}")

# Try target_sigma = 2 (elements of order 2)
for N in [10, 14, 22]:
    T, h, core = build_C0_variant(N, lambda u, N=N: mult_order(u, N), target_sigma=2)
    name = f"mult_order=2, N={N}"
    if T is not None:
        print(f"  {name}: h={h}, core={core}, C_0 assoc? {'YES' if s3_ac(T)==1 else 'NO'}")

