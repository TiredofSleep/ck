<!-- PACKET: evening_handoff_2026_04_23/family_study.py -->
"""
Systematic family study: canonical C_0 on Z/NZ for N = 2..10.
For each N:
1. Identify units, sigma-classes, harmony element h
2. Build C_0 canonical operator
3. Compute associative spectrum (s_3)
4. Find minimum 1-cell perturbation that achieves ac-freeness
5. Identify the "HARMONY" position in the CRT decomposition

Following Huang-Lehtonen 2022 definitions of ac-spectrum.
"""

from itertools import permutations
from math import gcd
import numpy as np

def nu2(n):
    if n == 0: return 999
    k = 0
    while n % 2 == 0: n //= 2; k += 1
    return k

def units(N):
    return [u for u in range(1, N) if gcd(u, N) == 1]

def sigma_units(N):
    return {u: nu2(3*u + 1) for u in units(N)}

def find_h(N):
    """h_N = max odd unit with sigma=1, if exists."""
    if N < 4: return None
    sig = sigma_units(N)
    cands = [u for u in units(N) if u % 2 == 1 and sig[u] == 1]
    return max(cands) if cands else None

def find_core(N):
    """σ-class-1 subset."""
    sig = sigma_units(N)
    return [u for u in units(N) if sig[u] == 1]

def build_C0(N):
    h = find_h(N)
    if h is None: return None, None, None
    core = find_core(N)
    sig = sigma_units(N)
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
    """Ac-spectrum at n=3 via numpy."""
    T = np.array(T, dtype=np.int8)
    N = len(T)
    brks = [lambda a,b,c,T: T[T[a,b],c], lambda a,b,c,T: T[a,T[b,c]]]
    xs = np.repeat(np.arange(N), N*N).astype(np.int8)
    ys = np.tile(np.repeat(np.arange(N), N), N).astype(np.int8)
    zs = np.tile(np.arange(N), N*N).astype(np.int8)
    fps = set()
    for perm in permutations(range(3)):
        tr = [xs, ys, zs]; p = [tr[i] for i in perm]
        for brk in brks:
            fps.add(bytes(brk(*p, T).tobytes()))
    return len(fps)

def s4_ac(T):
    """Ac-spectrum at n=4."""
    T = np.array(T, dtype=np.int8)
    N = len(T)
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
        for brk in brks:
            fps.add(bytes(brk(*p, T).tobytes()))
    return len(fps)

print("="*80)
print("FAMILY STUDY: CANONICAL C_0 ON Z/NZ, N = 2..10")
print("="*80)
print(f"{'N':>3} {'units':20s} {'h':>4} {'core':>10} {'C_0 assoc':>12} {'s_3^ac(C_0)':>13} {'target(3)=3':>12}")
print("-"*85)

results = []
for N in range(2, 11):
    T, h, core = build_C0(N)
    if T is None:
        print(f"{N:>3}   (no h found, C_0 not defined)")
        continue
    u = units(N)
    s3 = s3_ac(T)
    assoc = (s3 == 1)
    target = 3  # (2*3-3)!! = 3
    results.append((N, u, h, core, s3, assoc))
    print(f"{N:>3} {str(u):20s} {h:>4} {str(core):>10} {'YES' if assoc else 'NO':>12} {s3:>13} {target:>12}")

print()
print("="*80)
print("MINIMUM 1-CELL PERTURBATION FOR EACH N")
print("="*80)
print("For each N, find cells (a,b) and values v such that modifying C_0[a][b]=v")
print("(keeping C_0[b][a] same if a!=b, or symmetric if commutative-slot search)")
print("yields s_3^ac = 3 AND s_4^ac = 15.")
print()

for (N, u, h, core, s3_C0, assoc) in results:
    if not assoc: 
        print(f"N={N}: C_0 is NOT associative (s_3^ac={s3_C0}). Skipping min-bump analysis.")
        continue
    if N < 4:
        print(f"N={N}: too small for n=4 spectrum (would need |T^3| > 0). Skipping.")
        continue
    
    T_base, h, core = build_C0(N)
    T_np_base = np.array(T_base, dtype=np.int8)
    
    # Single-cell asymmetric search
    single_cell_hits = []
    for i in range(N):
        for j in range(N):
            if T_base[i][j] == 0: continue  # skip VOID
            for v in range(N):
                if v == T_base[i][j]: continue
                T = T_np_base.copy()
                T[i,j] = v
                if s3_ac(T) == 3 and s4_ac(T) == 15:
                    single_cell_hits.append(((i,j), v))
    
    # Commutative-slot search
    slot_hits = []
    for i in range(1, N):
        for j in range(i, N):
            for v in range(N):
                if v == T_base[i][j]: continue
                T = T_np_base.copy()
                T[i,j] = v; T[j,i] = v
                if s3_ac(T) == 3 and s4_ac(T) == 15:
                    slot_hits.append(((i,j), v))
    
    # Where is h's position?
    h_pos = (h, h)
    h_in_single = [ok for ok in single_cell_hits if ok[0] == h_pos]
    h_in_slot = [ok for ok in slot_hits if ok[0] == h_pos or (ok[0][0] == h or ok[0][1] == h)]
    
    print(f"N={N}: h={h}, core={core}")
    print(f"  Single-cell hits (asymmetric): {len(single_cell_hits)}")
    if single_cell_hits:
        all_at_hh = all(hit[0] == (h, h) for hit in single_cell_hits)
        print(f"  All hits at (h,h)=({h},{h})? {all_at_hh}")
        if all_at_hh:
            vals = sorted(set(hit[1] for hit in single_cell_hits))
            print(f"  Values v that work: {vals}")
    print(f"  Commutative-slot hits: {len(slot_hits)}")
    if slot_hits:
        involves_h = all((hit[0][0] == h or hit[0][1] == h) for hit in slot_hits)
        print(f"  All hits involve h={h}? {involves_h}")
        # Count hit types
        diag_h = [hit for hit in slot_hits if hit[0] == (h, h)]
        offdiag_h = [hit for hit in slot_hits if (hit[0][0] == h or hit[0][1] == h) and hit[0] != (h,h)]
        other = [hit for hit in slot_hits if hit[0][0] != h and hit[0][1] != h]
        print(f"  Diagonal (h,h): {len(diag_h)}, off-diagonal involving h: {len(offdiag_h)}, other: {len(other)}")
    print()

