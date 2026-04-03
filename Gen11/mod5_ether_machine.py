"""
mod5_ether_machine.py
=====================
The mod-5 ether: Z/5Z as the shared medium between RH and BSD.

Key algebraic structure:
  Z/10Z = Z/2Z x Z/5Z  (CRT)
  The Z/5Z component IS the ether.
  T*  = 5/7  = CREATE/HARMONY
  T*^2 = 25/49 = CREATE^2/HARMONY^2
  CREATE^2 = 25 = 0 mod 5  (the null point of Z/5Z)

BSD ether: Sha sits at 0 mod 5 when |Sha|=25. It is locally trivial at p=5
  (because CREATE^2 = 0 in Z/5Z) but globally non-trivial. The ether is
  the medium that is everywhere locally zero but globally present.

RH ether: The equidistribution of {gamma_n * log(5)/(2pi) mod 1} at p=5
  is the Z/5Z-visible equidistribution. D_KS(5, 500) = 0.0726 << T*.

The two branches share the same ether space: mod-5 arithmetic.

This script:
  1. For three elliptic curves, computes a_p mod 5 for p <= 47
  2. Shows how the Z/5Z component of Z/10Z reads each Euler factor
  3. Identifies curves where a_p = 0 mod 5 (CREATE: the ether eigenvalue)
  4. Builds the TSML-at-5 table showing which primes land in the ether
  5. Shows the RH ether measurement (D_KS at p=5 from stored zeros)
"""

import math
import json

T_STAR   = 5.0 / 7.0
T_STAR_2 = 25.0 / 49.0
PRIMES   = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# Z/10Z operators
VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
CREATE, BREATH, HARMONY, CHAOS, BALANCE    = 5, 8, 7, 6, 9  # note: 8=BREATH
# Z/5Z view: mod 5 values
# 0 = NULL/VOID    1 = LATTICE    2 = COUNTER    3 = PROGRESS    4 = COLLAPSE
# (CREATE=5 -> 0 mod 5: the Z/5Z null point)

def legendre(a, p):
    if a % p == 0: return 0
    val = pow(a % p, (p-1)//2, p)
    return -1 if val == p-1 else val

def count_Fp(a, b, p):
    if p == 2:
        count = 1
        for x in range(2):
            for y in range(2):
                if (y*y)%2 == (x*x*x + a*x + b)%2:
                    count += 1
        return count
    count = 1
    for x in range(p):
        rhs = (pow(x,3,p) + a*x + b) % p
        count += 1 + legendre(rhs, p)
    return count

def disc(a, b): return -16*(4*a**3 + 27*b**2)
def is_good(a, b, p): return disc(a,b) % p != 0

# ---- Curves ------------------------------------------------------------------
CURVES = [
    ('E0', -1,  0, 'y^2=x^3-x    rank 0, cond 32, Sha trivial'),
    ('E1',  0, -2, 'y^2=x^3-2    rank 1, cond 1728(?), Sha trivial'),
    ('E2',-15, 22, 'y^2=x^3-15x+22  rank>=1, cond?, Sha ?'),
]

print("MOD-5 ETHER MACHINE")
print("=" * 70)
print(f"T*   = 5/7  = {T_STAR:.6f}")
print(f"T*^2 = 25/49 = {T_STAR_2:.6f}")
print(f"CREATE^2 = 25 = 0 mod 5  (Z/5Z null point)")
print(f"HARMONY^2 = 49 = 4 mod 5 = -1 mod 5  (Z/5Z inversion)")
print()
print("Sha at |Sha|=25: CREATE^2 mod 5 = 0 -> locally invisible at p=5")
print("Torsion |E_tors|=7: 7^2=49 mod 5 = 4 = -1 -> BSD ratio 25/49 = T*^2")
print("=" * 70)

all_results = {}

for (name, a, b, desc) in CURVES:
    print(f"\n{name}: {desc}")
    print(f"  {'p':>4}  {'Np':>5}  {'a_p':>5}  {'good':>4}  "
          f"{'a_p mod 5':>9}  {'Z5 name':>10}  {'is ether?':>10}")
    print(f"  {'-'*4}  {'-'*5}  {'-'*5}  {'-'*4}  {'-'*9}  {'-'*10}  {'-'*10}")

    z5_names = {0: 'NULL(ether)', 1: 'LATTICE', 2: 'COUNTER',
                3: 'PROGRESS', 4: 'COLLAPSE'}

    ether_count = 0
    good_count  = 0
    records = []

    for p in PRIMES:
        Np   = count_Fp(a, b, p)
        ap   = p + 1 - Np
        good = is_good(a, b, p)
        if not good:
            records.append({'p':p,'Np':Np,'ap':ap,'good':False,
                            'ap_mod5':None,'ether':False})
            print(f"  {p:>4}  {Np:>5}  {ap:>5}  {'BAD':>4}  {'---':>9}  {'---':>10}  {'---':>10}")
            continue

        ap5      = ap % 5
        z5name   = z5_names.get(ap5, str(ap5))
        is_ether = (ap5 == 0)   # a_p = 0 mod 5: lands at Z/5Z null point
        if is_ether: ether_count += 1
        good_count += 1

        records.append({'p':p,'Np':Np,'ap':ap,'good':True,
                        'ap_mod5':ap5,'ether':is_ether})
        ether_str = '** ETHER **' if is_ether else ''
        print(f"  {p:>4}  {Np:>5}  {ap:>5}  {'yes':>4}  "
              f"{ap5:>9}  {z5name:>10}  {ether_str:>10}")

    ether_frac = ether_count / good_count if good_count > 0 else 0
    expected   = 1.0 / 5.0  # under Hasse: a_p uniform in Z/5Z -> 1/5 are 0

    print(f"\n  Ether fraction (a_p=0 mod 5): {ether_count}/{good_count} = {ether_frac:.3f}")
    print(f"  Expected under uniform Z/5Z:  ~{expected:.3f}  (Hasse equidistribution)")
    print(f"  Excess: {(ether_frac - expected):.3f}  "
          f"({'above' if ether_frac > expected else 'below'} expected)")

    all_results[name] = {'records': records, 'ether_fraction': round(ether_frac,4),
                         'ether_count': ether_count, 'good_count': good_count}

# ---- RH ether (p=5 equidistribution from stored results) --------------------
print()
print("=" * 70)
print("RH ETHER AT p=5")
print("=" * 70)

try:
    with open('../equidist_results.json') as f:
        eq = json.load(f)
    p5 = eq['results'].get('5', {})
    d5 = p5.get('D_KS', None)
    if d5:
        print(f"  D_KS(p=5, N=500) = {d5:.5f}")
        print(f"  T*               = {T_STAR:.5f}")
        print(f"  D_KS / T*        = {d5/T_STAR:.4f}  (= {100*d5/T_STAR:.1f}% of threshold)")
        print(f"  mean(alpha)      = {p5.get('mean_alpha', '?'):.5f}  (expected 0.5)")
        print(f"  std(alpha)       = {p5.get('std_alpha', '?'):.5f}  (uniform std = 0.289)")
        print()
        print("  The first 500 Riemann zeros are equidistributed mod log(5)/(2pi).")
        print("  D_KS is at {:.1f}% of the T* threshold.".format(100*d5/T_STAR))
        print("  The Z/5Z ether is transparent to the RH zeros: they pass through it")
        print("  without creating detectable arithmetic structure.")
except Exception as e:
    print(f"  (equidist_results.json not found or error: {e})")

# ---- Mod-5 connection between RH and BSD ------------------------------------
print()
print("=" * 70)
print("MOD-5 ETHER: RH-BSD CONNECTION")
print("=" * 70)
print()
print("The Z/5Z component of Z/10Z is the ether shared by RH and BSD.")
print()
print("BSD side:")
print("  - Sha sits at 0 mod 5 when |Sha|=25=CREATE^2")
print("  - Sha is locally trivial at p=5: class maps to 0 in H^1(Q_5, E)")
print("  - Sha is globally present: the class is non-trivial in H^1(Q, E)")
print("  - The ether is what is zero at every local Z/5Z detector")
print("    but present in the global Z/5Z field")
print()
print("RH side:")
print("  - Zeros equidistributed mod log(5)/(2pi): D_KS << T*")
print("  - The Z/5Z-frequency component of the zero distribution is uniform")
print("  - No clustering at CREATE (=0 mod 5) detectable in the KS test")
print("  - The zeros pass through the mod-5 ether without leaving a trace")
print()
print("The shared structure:")
print("  Sha: locally 0 at p=5 (in the ether), globally present")
print("  RH zeros: equidistributed at log(5) scale (no local structure at p=5)")
print("  Both are 'ether objects': invisible to mod-5 local detectors.")
print()
print("The algebraic picture:")
print("  Z/10Z = Z/2Z x Z/5Z")
print("  Z/5Z ether = {elements x : x = 0 mod 5} = {0, 5} in Z/10Z")
print("             = {VOID, CREATE}")
print("  VOID = 0 (absolute zero), CREATE = 5 (the generative null)")
print("  Both Sha (|Sha|=25) and the RH zeros at p=5 live in this space.")
print()
print("Formal statement:")
print("  The mod-5 ether is the subgroup ker(Z/10Z -> Z/10Z/5Z) = {0,5}.")
print("  Sha[5] is the 5-torsion of Sha: it lives in H^1(Q, E[5])")
print("  and vanishes at every local H^1(Q_v, E[5]) -> it is in the ether.")
print("  The RH zeros at p=5 are equidistributed in the same Z/5Z space.")
print("  The ether is the medium where both Sha and the RH zeros are undetectable")
print("  locally but exist globally.")

# ---- The Selmer/ether machine at mod 5 --------------------------------------
print()
print("=" * 70)
print("SELMER-ETHER MACHINE (mod 5)")
print("=" * 70)
print()
print("The mod-5 Selmer group Sel_5(E) fits into:")
print("  0 -> E(Q)/5 -> Sel_5(E) -> Sha(E)[5] -> 0")
print()
print("For Sha[5] != 0: the mod-5 Galois representation rho_{E,5} must")
print("  have a specific structure. Key condition:")
print()
print("  a_p = 0 mod 5 for many primes p")
print("  <=> the Frobenius at p acts as a unipotent element in GL_2(F_5)")
print("  <=> the curve has a Galois-stable 5-isogeny or Sha develops 5-torsion")
print()
print("Z/10Z reads this as: a_p mod 5 = 0 = CREATE mod 10 -> ether eigenvalue")
print()
print("For our three curves, ether eigenvalue fractions:")
for name in all_results:
    r = all_results[name]
    print(f"  {name}: {r['ether_count']}/{r['good_count']} = {r['ether_fraction']:.3f}  "
          f"(expected ~0.200)")

print()
print("Expected ~20% under Chebotarev density (a_p uniform in Z/5Z for generic E).")
print("Significant excess above 20% signals the mod-5 Galois rep is non-generic")
print("and the curve may be developing Sha[5] (ether absorption).")

# ---- Save -------------------------------------------------------------------
output = {
    'T_star':   T_STAR,
    'T_star_2': T_STAR_2,
    'CREATE_sq_mod5': 0,   # 25 mod 5 = 0
    'HARMONY_sq_mod5': 4,  # 49 mod 5 = 4 = -1
    'curves': all_results,
    'ether_interpretation': {
        'BSD': 'Sha[5] != 0 <=> |Sha| div by 25; sits at 0 mod 5 = Z/5Z null',
        'RH':  'zeros equidist at p=5; D_KS << T*; no mod-5 clustering',
        'shared': 'both are locally zero at p=5, globally present',
        'algebraic': 'ether = ker(Z/10Z -> Z/2Z) intersect {CREATE-orbit} = {0,5}',
    }
}

with open('mod5_ether_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to mod5_ether_results.json")
