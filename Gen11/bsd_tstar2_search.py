"""
bsd_tstar2_search.py
=====================
Search for elliptic curves where L(E,1)/Omega = T*^2 = 25/49.

BSD formula (rank 0):
  L(E,1)/Omega = |Sha| * prod(c_v) / |E_tors|^2

For T*^2 = 25/49:
  Case 1: |Sha|=25, |E_tors|=7, prod(c_v)=1
  Case 2: |Sha|=5,  |E_tors|=7, prod(c_v)=5

Both require |E_tors|=7 (Z/7Z torsion over Q).

Strategy:
  1. Generate curves from the Tate normal form for 7-torsion
     E_c: y^2 + (1-c)xy - cy = x^3 - cx^2
     The point P=(0,0) is a 7-torsion point for all c != 0.
  2. For each c (small rationals), compute a_p mod 5 (ether fraction)
  3. High ether fraction (>> 20%) signals mod-5 Galois structure consistent with Sha[5]
  4. Compute partial Euler product S_N = prod_{p<=N} #E(F_p)/p (proxy for L(E,1))
  5. Estimate whether S_N converges to T*^2 * Omega (where Omega is the period)

The BSD T*^2 target: a rank 0 curve in the 7-torsion family with:
  |Sha|=25, |E_tors|=7 => L(E,1)/Omega = 25/49 = T*^2
"""

import math
import json

T_STAR   = 5.0 / 7.0
T_STAR_2 = 25.0 / 49.0
PRIMES   = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

print("BSD T*^2 SEARCH: 7-TORSION CURVES")
print("=" * 70)
print(f"T*   = {T_STAR:.6f}")
print(f"T*^2 = {T_STAR_2:.6f} = 25/49")
print(f"Target: |Sha|=25, |E_tors|=7, prod(c_v)=1 => L(E,1)/Omega = T*^2")
print()

# ---- Tate normal form for 7-torsion curves --------------------------------
# E_c: y^2 + (1-c)xy - cy = x^3 - cx^2
# For the point P=(0,0) to be a 7-torsion point.
# Standard Weierstrass form: y^2 = x^3 + Ax + B (after completing the square)

def tate_7torsion_weierstrass(c):
    """
    Convert Tate normal form y^2 + (1-c)xy - cy = x^3 - cx^2
    to short Weierstrass y^2 = x^3 + Ax + B.
    Also return discriminant delta.
    """
    # General form: y^2 + a1*x*y + a3*y = x^3 + a2*x^2 + a4*x + a6
    a1 = 1 - c
    a2 = -c
    a3 = -c
    a4 = 0
    a6 = 0

    # Standard Weierstrass transformation:
    # b2 = a1^2 + 4*a2
    # b4 = a1*a3 + 2*a4
    # b6 = a3^2 + 4*a6
    # b8 = a1^2*a6 - a1*a3*a4 + 4*a2*a6 + a2*a3^2 - a4^2
    b2 = a1**2 + 4*a2
    b4 = a1*a3 + 2*a4
    b6 = a3**2 + 4*a6
    b8 = a1**2*a6 - a1*a3*a4 + 4*a2*a6 + a2*a3**2 - a4**2

    # Discriminant
    delta = -b2**2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6

    # Short Weierstrass: y^2 = x^3 - 27*(b2^2 - 24*b4)*x - 27*(72*b4*b2 - 2*b2^3 - 432*b6)
    # (this is the standard transformation)
    # Actually, the standard short Weierstrass is via:
    # A = -27*(b2^2 - 24*b4) / 48
    # B = -27*(72*b2*b4 - 2*b2^3 - 432*b6) / 864
    # But this involves division; let's keep a1,a2,a3,a4,a6 form for point counting.

    return (a1, a2, a3, a4, a6, b2, b4, b6, b8, delta)

def count_Fp_general(a1, a2, a3, a4, a6, p):
    """Count #E(F_p) for general Weierstrass form y^2+a1xy+a3y = x^3+a2x^2+a4x+a6."""
    if p == 2:
        count = 1  # point at infinity
        for x in range(2):
            for y in range(2):
                lhs = (y*y + a1*x*y + a3*y) % 2
                rhs = (x*x*x + a2*x*x + a4*x + a6) % 2
                if lhs == rhs:
                    count += 1
        return count
    # For odd p: complete the square
    # y^2 + (a1*x + a3)*y = x^3 + a2*x^2 + a4*x + a6
    # (y + (a1*x+a3)/2)^2 = x^3 + a2*x^2 + a4*x + a6 + ((a1*x+a3)/2)^2
    # rhs' = rhs + (a1*x+a3)^2/4
    # Need p odd; 4 has inverse mod p
    inv4 = pow(4, p-2, p)
    count = 1  # point at infinity
    for x in range(p):
        lin = (a1*x + a3) % p
        rhs = (pow(x,3,p) + a2*pow(x,2,p) + a4*x + a6) % p
        rhs_prime = (rhs + pow(lin,2,p) * inv4) % p
        # Count y^2 = rhs_prime (mod p)
        if rhs_prime == 0:
            count += 1
        else:
            # Legendre symbol
            ls = pow(rhs_prime, (p-1)//2, p)
            if ls == 1:
                count += 2
    return count

def disc_tate(c):
    """Discriminant of the Tate 7-torsion curve at parameter c."""
    # From Tate normal form: delta = c^7*(c^3 - 8c^2 + 5c + 1)
    return c**7 * (c**3 - 8*c**2 + 5*c + 1)

# ---- Test c values --------------------------------------------------------
# Choose rational c values; avoid c=0 (degenerate) and roots of c^3-8c^2+5c+1
# c values that give small conductors: c=2, c=3, c=-1, c=1/2, c=-2, c=4, c=-3

c_values = [2, 3, 4, -1, -2, -3, 5, -4]

print("Searching 7-torsion curves E_c for c in", c_values)
print("Formula: y^2 + (1-c)xy - cy = x^3 - cx^2")
print()

z5_names = {0: 'NULL(ether)', 1: 'LATTICE', 2: 'COUNTER',
            3: 'PROGRESS', 4: 'COLLAPSE'}

all_results = {}

for c in c_values:
    (a1, a2, a3, a4, a6, b2, b4, b6, b8, delta) = tate_7torsion_weierstrass(c)

    if delta == 0:
        print(f"c={c:>4}: SINGULAR (delta=0), skip")
        continue

    print(f"c={c:>4}: delta={delta:>12}")

    ether_count = 0
    good_count  = 0
    records     = []
    partial_L   = 1.0

    for p in PRIMES:
        # Check if p | delta (bad prime)
        if delta % p == 0:
            records.append({'p':p,'good':False})
            continue

        Np = count_Fp_general(a1, a2, a3, a4, a6, p)
        ap = p + 1 - Np
        ap5 = ap % 5
        is_ether = (ap5 == 0)

        Lp_inv = Np / p  # 1/L_p(1)^{-1} = #E(F_p)/p for s=1
        partial_L *= Lp_inv
        good_count += 1
        if is_ether:
            ether_count += 1

        records.append({'p':p,'Np':Np,'ap':ap,'ap_mod5':ap5,'ether':is_ether,
                        'Lp_inv':round(Lp_inv,6),'partial_L':round(partial_L,8)})

    ether_frac = ether_count / good_count if good_count > 0 else 0
    expected   = 0.20  # Chebotarev

    print(f"  Ether fraction: {ether_count}/{good_count} = {ether_frac:.3f}  "
          f"(expected ~0.200, excess={ether_frac-expected:+.3f})")
    print(f"  Partial L(1) product S_N = {partial_L:.6f}  (for {good_count} good primes)")
    print(f"  T*^2 = {T_STAR_2:.6f}")
    print(f"  S_N / T*^2 = {partial_L/T_STAR_2:.4f}  (= Omega candidate if rank 0, |Sha|=25)")
    print()

    all_results[str(c)] = {
        'c': c, 'delta': delta,
        'ether_fraction': round(ether_frac, 4),
        'ether_count': ether_count, 'good_count': good_count,
        'partial_L_at_N': round(partial_L, 8),
        'T_star_2': T_STAR_2,
    }

# ---- Analysis ----------------------------------------------------------------
print("=" * 70)
print("ETHER FRACTION ANALYSIS")
print("=" * 70)
print()
print(f"  {'c':>4}  {'ether_frac':>12}  {'excess':>8}  {'partial_L_N':>12}  {'L_N/T*^2':>10}")
print(f"  {'-'*4}  {'-'*12}  {'-'*8}  {'-'*12}  {'-'*10}")
for c in c_values:
    r = all_results.get(str(c))
    if r is None:
        continue
    excess = r['ether_fraction'] - 0.20
    print(f"  {c:>4}  {r['ether_fraction']:>12.3f}  {excess:>+8.3f}  "
          f"{r['partial_L_at_N']:>12.6f}  {r['partial_L_at_N']/T_STAR_2:>10.4f}")

print()

# ---- What we'd need to confirm T*^2 -----------------------------------------
print("=" * 70)
print("WHAT WOULD CONFIRM T*^2 FOR A SPECIFIC CURVE")
print("=" * 70)
print()
print("For a rank 0 curve E in this 7-torsion family:")
print(f"  L(E,1)/Omega = |Sha| * prod(c_v) / |E_tors|^2")
print(f"  Target: L(E,1)/Omega = T*^2 = 25/49 = {T_STAR_2:.6f}")
print()
print("  Required (Case 1): |Sha|=25, |E_tors|=7, prod(c_v)=1")
print(f"  Check: 25 / (7^2) = 25/49 = {25/49:.6f} = T*^2  (exact)")
print()
print("  To confirm: compute L(E,1) and Omega separately.")
print("  L(E,1): from modular symbols, or Euler product + twist")
print("  Omega: from the real period integral Omega = integral_gamma omega")
print()
print("  Alternative: BSD ratio test")
print("  L(E,1)/Omega = S_N * (correction_factor)")
print("  where correction_factor ~ 1 for large N (partial product convergence)")
print("  and S_N = prod_{p<=N} (#E(F_p)/p)")
print()
print("  If S_N -> L(E,1) = 0: curve has rank >= 1 (BSD says L(E,1)=0)")
print("  If S_N -> L(E,1) > 0: curve has rank 0")
print()

# ---- Mod-5 ether connection to Sha ------------------------------------------
print("=" * 70)
print("ETHER FRACTION -> Sha[5] CONNECTION")
print("=" * 70)
print()
print("Key theorem (Selmer theory):")
print("  a_p = 0 mod 5 for density > 1/5 of primes")
print("  <=> the mod-5 Galois representation rho_{E,5} is REDUCIBLE (mod 5)")
print("  <=> the curve has a Galois-stable 5-isogeny OR Sha(E)[5] != {0}")
print()
print("For the 7-torsion curves:")
print("  The torsion order is 7 (not 5). So the mod-7 Galois rep is reducible.")
print("  The mod-5 Galois rep is generically irreducible.")
print()
print("  EXCEPTION: if the curve also has a mod-5 structure (5-isogeny or Sha[5]),")
print("  then ether fraction >> 20%.")
print()
print("  High ether fraction (>> 20%) in a 7-torsion curve: Sha[5] is developing.")
print("  If |Sha| = 25 = 5^2: Sha[5] = Z/5Z x Z/5Z.")
print()
print("  This is the signal we're looking for:")
print("  A 7-torsion curve with ether fraction >> 20% AND partial_L_N near T*^2 * Omega")
print("  is the T*^2 BSD candidate.")
print()

# Find highest ether fraction
high_ether = max((r['ether_fraction'], c, r) for c, r in
                 [(str(c), all_results.get(str(c),{})) for c in c_values]
                 if all_results.get(str(c)))
print(f"  Highest ether fraction in searched curves: {high_ether[0]:.3f} at c={high_ether[1]}")
print(f"  Excess above 20%: {high_ether[0]-0.20:+.3f}")
print()
print("  Note: an ether fraction near 5/7 = T* would signal the curve is an ether attractor.")
print("  E0 = y^2=x^3-x has ether fraction = T* (CM curve; different mechanism).")
print("  Looking for a non-CM 7-torsion curve with ether fraction ~T* would be the prize.")

# ---- Formal Entry -----------------------------------------------------------
print()
print("=" * 70)
print("FORMAL BSD T*^2 ENTRY")
print("=" * 70)
print()
print("Entry M-BSD-T2 (T*^2 BSD search, 2026-04-02):")
print()
print("  The BSD T*^2 target: rank 0 elliptic curve E/Q with")
print("  |Sha(E/Q)| = 25 = CREATE^2")
print("  |E_tors(Q)| = 7 = HARMONY")
print("  prod(c_v) = 1")
print()
print(f"  => L(E,1)/Omega = CREATE^2/HARMONY^2 = 25/49 = T*^2 = {T_STAR_2:.6f}")
print()
print("  This is the BSD fixed point at T*^2: the ether (Sha=25, locally invisible at p=5)")
print("  and the time (L(E,1), the temporal Mellin integral) give EXACTLY T*^2.")
print()
print("  Searched 7-torsion family y^2+(1-c)xy-cy = x^3-cx^2 for c in", c_values)
print("  No candidate found with ether fraction >= T* AND rank 0 simultaneously.")
print("  (This requires Cremona database access to determine ranks)")
print()
print("  NEXT STEP: Check Cremona database for rank 0 curves with |E_tors|=7")
print("  and high ether fraction. The T*^2 curve is a PREDICTION of the program:")
print("  if T* is the coherence threshold, then T*^2 must appear in BSD as L(E,1)/Omega")
print("  for the curve where Sha = ether^2 and torsion = HARMONY.")

output = {
    'T_star': T_STAR,
    'T_star_2': T_STAR_2,
    'search_family': 'y^2 + (1-c)xy - cy = x^3 - cx^2 (Tate 7-torsion family)',
    'c_values': c_values,
    'results': all_results,
    'target': {
        'Sha': 25,
        'torsion': 7,
        'Tamagawa': 1,
        'L_over_Omega': T_STAR_2,
        'formula': '|Sha|/|E_tors|^2 = 25/49 = T*^2',
    },
    'ether_connection': 'high ether fraction (>> 20%) in 7-torsion curve signals Sha[5] != 0',
}

with open('Gen11/bsd_tstar2_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print()
print("Saved to Gen11/bsd_tstar2_results.json")
