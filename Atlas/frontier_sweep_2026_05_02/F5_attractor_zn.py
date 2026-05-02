"""
F5 Test: does the WP115 4-core attractor (H/Br = 1+sqrt(3) at alpha=1/2)
generalize from Z/10Z to other Z/nZ?

The WP115 algebra is built from:
  TSML: 10x10 table where HARMONY (=9) absorbs everything except VOID rows;
        canonical synthesis-attractor rule.
  BHML: binary CL-like table; HARMONY/VOID priority + (a+b) mod n on DIS=0,
        HARMONY otherwise.

For Z/nZ the natural analog:
  TSML_n[a][b] = harmony=n-1 if (a,b) not in row 0/col 0; else 0 (VOID).
  BHML_n[a][b] = harmony if a==harmony or b==harmony,
                 0 if a==0 or b==0,
                 (a+b) mod n if (a+b) mod n == (a*b) mod n,
                 harmony otherwise.

Then run T+B-mix at alpha=1/2 and see if a 4-core attractor with
H/Br = 1+sqrt(3) emerges.
"""
import mpmath as mp

def make_tsml(n):
    H = n - 1
    table = [[0]*n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            if a == 0 or b == 0:
                table[a][b] = 0
            else:
                table[a][b] = H
    return table

def make_bhml(n):
    """Binary CL on Z/nZ: HARMONY/VOID priority + DIS=0 ECHO + HARMONY default."""
    H = n - 1
    table = [[0]*n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            if a == H or b == H:
                table[a][b] = H
            elif a == 0 or b == 0:
                table[a][b] = 0
            elif (a + b) % n == (a * b) % n:
                table[a][b] = (a + b) % n
            else:
                table[a][b] = H
    return table

def fuse_mp(p, table, support, n):
    r = [mp.mpf(0)] * n
    for a in support:
        if p[a] == 0: continue
        for b in support:
            if p[b] == 0: continue
            r[table[a][b]] += p[a] * p[b]
    return r

def normalize(v):
    s = sum(v)
    return v if s == 0 else [x/s for x in v]

def attractor_on_shell(n, support, T, B, alpha=mp.mpf("0.5"), max_iter=4000):
    p = [mp.mpf(0)]*n
    for i in support:
        p[i] = mp.mpf(1)/len(support)
    one_minus = mp.mpf(1) - alpha
    for k in range(max_iter):
        pt = normalize(fuse_mp(p, T, support, n))
        pb = normalize(fuse_mp(p, B, support, n))
        new_p = normalize([alpha*pt[i] + one_minus*pb[i] for i in range(n)])
        diff = max(abs(new_p[i] - p[i]) for i in range(n))
        p = new_p
        if diff < mp.mpf(10)**(-30):
            return p, k+1
    return p, max_iter

def find_4core(p, n, threshold=1e-6):
    """Find the support indices with mass > threshold."""
    return [i for i in range(n) if float(p[i]) > threshold]

mp.mp.dps = 40

print("=" * 100)
print("F5 Test: WP115 4-core attractor for Z/nZ at alpha=1/2 -- is n=10 special?")
print("=" * 100)
print()
print(f"  Reference (n=10): 4-core = {{V,H,Br,R}} = {{0,7,8,9}} with H/Br = 1+sqrt(3)")
print(f"                    (V=0.138, H=0.540, Br=0.198, R=0.124)")
print()
print(f"{'n':>4} {'composition':>18} {'iters':>7} {'4-core':>20} {'H/Br ratio':>15} {'1+sqrt(3) match?':>18}")
print("-" * 100)

target = mp.mpf(1) + mp.sqrt(mp.mpf(3))
print(f"  Target H/Br = 1 + sqrt(3) = {float(target):.10f}")
print()

# Test composition types
def factor_label(n):
    factors = []
    m = n
    p = 2
    while p*p <= m:
        if m % p == 0:
            cnt = 0
            while m % p == 0:
                m //= p
                cnt += 1
            factors.append((p, cnt))
        p += 1
    if m > 1:
        factors.append((m, 1))
    if all(e == 1 for _, e in factors):
        if len(factors) == 1: return f"prime"
        return f"squarefree({len(factors)})"
    return f"prime-power" if len(factors)==1 else f"non-squarefree"

# n values to test: cover squarefree composites, prime powers, primes
ns_to_test = [
    6,    # 2*3 squarefree
    8,    # 2^3 prime power
    9,    # 3^2 prime power
    10,   # 2*5 squarefree (REFERENCE)
    12,   # 2^2*3 mixed
    14,   # 2*7 squarefree
    15,   # 3*5 squarefree
    16,   # 2^4 prime power
    21,   # 3*7 squarefree
    22,   # 2*11 squarefree
]

results = []
for n in ns_to_test:
    T = make_tsml(n)
    B = make_bhml(n)
    # Use the full support (all of Z/nZ minus none)
    support = list(range(n))
    attr, iters = attractor_on_shell(n, support, T, B)
    H = n - 1
    # In Z/nZ, the analogs of (V, H, Br, R) need to be defined by ROLE.
    # V = 0 (always), H = n-1 (always), R = harmony source (?).
    # Br for n=10 is index 8 (BREATH), which has special role: penultimate.
    # For Z/nZ, take Br = n-2 (penultimate) by analogy.
    # R = n-3? (for n=10, R=9 is harmony itself; the reset op is n-1 elsewhere)
    # Actually in TSML/BHML at n=10: V=0, H=7, Br=8, R=9 -- so 4-core
    # is the LAST 4 indices in some sense.  Hmm, H=7 not n-1=9.
    # Let me check: BHML[7][b] in n=10: BHML_ROWS[7] = "7234567890" -- index 7 is H,
    # index 9 is R.  So for our generalized BHML, the 4-core
    # {V, H, Br, R} maps to indices {0, n-3, n-2, n-1}? Not quite.
    # Let me just look at what mass concentrates on for each n.
    core = find_4core(attr, n, threshold=1e-4)
    core_str = "{" + ",".join(str(i) for i in core) + "}"
    label = factor_label(n)
    
    # Compute H/Br ratio: try several candidate (H_idx, Br_idx) pairs
    # Identify by mass: 2 highest non-zero indices
    masses = [(float(attr[i]), i) for i in range(n)]
    masses.sort(reverse=True)
    top4 = [(idx, mass) for mass, idx in masses[:4]]
    if len(top4) >= 2:
        m1, m2 = top4[0][1], top4[1][1]
        ratio = m1 / m2 if m2 > 0 else float('inf')
        ratio_match = "Y" if abs(ratio - float(target)) < 1e-3 else "N"
    else:
        ratio = 0; ratio_match = "?"
    
    print(f"{n:>4} {label:>18} {iters:>7} {core_str:>20} {ratio:>15.6f} {ratio_match:>18}")
    results.append((n, label, core, ratio, ratio_match, top4))

print()
print("INTERPRETATION:")
print("  H/Br ratio close to 1+sqrt(3) = 2.7321 -> attractor with WP115 structure")
print("  Otherwise -> different attractor (or no attractor) for that n")
print()
print("DETAILED TOP-4 MASS DISTRIBUTION:")
for n, lbl, core, ratio, m, top4 in results:
    print(f"  n={n:>3} ({lbl:>18}): top-4 = " +
          " ".join(f"idx{idx}={mass:.4f}" for idx, mass in top4))

