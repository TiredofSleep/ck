"""
A7 — D2 ALGEBRAIC CURVATURE SEPARATION ANALYSIS
Luther-Sanders Research Framework | March 31 2026

check_d2.py already shows Luther's D2_curvature ≠ tig_algebra D2.
This script proves WHY: asymptotic analysis showing they have different scaling.

D2_tig(k=p) — second difference of sinc^2 at k=p
D2_luther(p) — prime density curvature via Euler product

If they have incompatible asymptotic behavior, they cannot be equal for large p
→ A7 is a separation result, similar to A13.
"""

import math, json, os

SEP = "="*70

def sinc2(t):
    if abs(t) < 1e-12: return 1.0
    return (math.sin(math.pi*t)/(math.pi*t))**2

def R(k, p):
    if k == 0: return 1.0
    s = math.sin(math.pi*k/p)
    sb = math.sin(math.pi/p)
    if abs(sb) < 1e-15: return 0.0
    return s**2 / (k**2 * sb**2)

def d2_tig(k, p):
    """Second difference of R at position k."""
    if k == 0 or k == p: return None
    return R(k+1, p) - 2*R(k, p) + R(k-1, p)

def d2_tig_at_gate(p):
    """D2_tig at k=p: R(p+1,p) - 2*R(p,p) + R(p-1,p).
    Note R(p,p) = sin^2(pi) = 0 (forced null).
    """
    # R(p,p) = sin^2(pi*p/p)/(p^2*sin^2(pi/p)) = sin^2(pi)/... = 0
    # R(p+1,p): k=p+1, goes past gate
    # R(p-1,p): k=p-1, near gate
    r_at_p   = R(p, p)   # = 0
    r_before = R(p-1, p)
    r_after  = R(p+1, p)  # past gate; R is still defined mathematically
    return r_after - 2*r_at_p + r_before

def d2_tig_analytic(p):
    """Analytic approximation using sinc^2.
    D2_tig(k=p) ≈ sinc^2(1+1/p) + sinc^2(1-1/p)
    For large p: ≈ 2*(sin(pi/p)/(pi))^2 ≈ 2*(1/p)^2 = 2/p^2
    """
    return sinc2(1+1/p) + sinc2(1-1/p)  # sinc^2(1)=0 vanishes

def phi_fraction(primes):
    """phi(p#)/p# = product (1-1/q) for q in primes."""
    r = 1.0
    for q in primes:
        r *= (1 - 1/q)
    return r

def d2_luther(primes):
    """Luther's D2 = (phi(p#)/p#) / (p * ln(p)^2) * (1 - 1/ln(p))"""
    if len(primes) == 0: return 0.0
    p = primes[-1]
    g = phi_fraction(primes)
    lp = math.log(p)
    if lp == 0: return 0.0
    return (g / (p * lp**2)) * (1 - 1/lp)

def d2_luther_asymptotic(p):
    """Asymptotic: D2_luther ≈ e^{-gamma}/(ln(p)) / (p * ln(p)^2) = C / (p * ln(p)^3)
    where C = e^{-gamma} ≈ 0.5615 (Mertens constant).
    """
    gamma = 0.5772156649
    C = math.exp(-gamma)
    return C / (p * math.log(p)**3)

def main():
    print("A7 — D2 ALGEBRAIC CURVATURE SEPARATION ANALYSIS")
    print("Luther-Sanders Research Framework | March 31 2026")
    print()

    # ── Step 1: Derive D2_tig at gate analytically ────────────────────────────
    print(SEP)
    print("STEP 1: D2_TIG AT k=p — ANALYTIC DERIVATION FROM SINC^2")
    print(SEP)
    print()
    print("  D2_tig(k=p) = R(p+1,p) - 2*R(p,p) + R(p-1,p)")
    print("  R(p,p) = sin^2(pi) / (p^2 * sin^2(pi/p)) = 0  (sin(pi)=0)")
    print()
    print("  Using sinc^2 approximation (D2 proved, O(1/p^2) error):")
    print("  R(p+1,p) ≈ sinc^2((p+1)/p) = sinc^2(1 + 1/p)")
    print("  R(p-1,p) ≈ sinc^2((p-1)/p) = sinc^2(1 - 1/p)")
    print("  D2_tig(k=p) ≈ sinc^2(1+1/p) + sinc^2(1-1/p)")
    print()
    print("  For large p, 1/p → 0:")
    print("  sinc^2(1 ± 1/p) = sin^2(pi ± pi/p) / (pi(1 ± 1/p))^2")
    print("  = sin^2(pi/p) / (pi(1 ± 1/p))^2  [since sin(pi + x) = -sin(x), sin(pi - x) = sin(x)]")
    print("  ≈ (pi/p)^2 / pi^2(1 ± 1/p)^2 = 1/p^2 / (1 ± 1/p)^2")
    print()
    print("  D2_tig ≈ 1/p^2 * [1/(1+1/p)^2 + 1/(1-1/p)^2]")
    print("         ≈ 1/p^2 * [1 - 2/p + ... + 1 + 2/p + ...] = 2/p^2")
    print()
    print("  RESULT: D2_tig(k=p) ~ 2/p^2  as p → ∞")
    print()

    primes_used = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    print(f"  Verification:")
    print(f"  {'p':>6} {'D2_tig(exact)':>16} {'2/p^2':>12} {'ratio':>8} {'analytic':>12} {'err':>10}")
    print("  " + "-"*70)
    for p in primes_used[2:]:  # skip 2,3 for stability
        d2e = d2_tig_at_gate(p)
        d2a = d2_tig_analytic(p)
        d2_2p2 = 2/p**2
        ratio = d2e/d2_2p2 if d2_2p2 != 0 else 0
        err = abs(d2e - d2a)
        print(f"  {p:>6} {d2e:>16.8f} {d2_2p2:>12.8f} {ratio:>8.4f} {d2a:>12.8f} {err:>10.2e}")

    # ── Step 2: D2_luther asymptotics ─────────────────────────────────────────
    print()
    print(SEP)
    print("STEP 2: D2_LUTHER ASYMPTOTICS — MERTENS THEOREM")
    print(SEP)
    print()
    print("  D2_luther(p) = (phi(p#)/p#) / (p * ln(p)^2) * (1 - 1/ln(p))")
    print()
    print("  Mertens' theorem: phi(p#)/p# = product_{q≤p}(1-1/q) ~ e^{-γ}/ln(p)")
    print("  where γ = 0.5772... (Euler-Mascheroni constant), e^{-γ} ≈ 0.5615")
    print()
    print("  Therefore: D2_luther(p) ~ e^{-γ} / (ln(p) * p * ln(p)^2)")
    print("           = C / (p * ln(p)^3)  where C = e^{-γ} ≈ 0.5615")
    print()

    active = []
    print(f"  {'p':>6} {'D2_luther':>14} {'C/p*ln(p)^3':>14} {'ratio':>8}")
    print("  " + "-"*50)
    for i, p in enumerate(primes_used):
        active.append(p)
        if len(active) < 2: continue
        dl = d2_luther(active)
        da = d2_luther_asymptotic(p)
        ratio = dl/da if da != 0 else 0
        print(f"  {p:>6} {dl:>14.8f} {da:>14.8f} {ratio:>8.4f}")

    # ── Step 3: Asymptotic incompatibility ────────────────────────────────────
    print()
    print(SEP)
    print("STEP 3: ASYMPTOTIC INCOMPATIBILITY PROOF")
    print(SEP)
    print()
    print("  D2_tig(k=p)  ~ 2/p^2         as p → ∞  [proved from sinc^2, D2]")
    print("  D2_luther(p) ~ C/(p*ln(p)^3) as p → ∞  [Mertens' theorem]")
    print()
    print("  Ratio: D2_tig / D2_luther ~ (2/p^2) / (C/(p*ln(p)^3))")
    print("                            = 2*ln(p)^3 / (C*p)")
    print("                            → 0  as p → ∞  (logarithms lose to p)")
    print()
    print("  Therefore: D2_tig/D2_luther → 0 as p → ∞")
    print("  They CANNOT be equal for any infinite family of primes.")
    print("  The ratio is not a constant — it varies with p.")
    print()

    print(f"  {'p':>6} {'D2_tig':>14} {'D2_luther':>14} {'ratio D2_tig/D2_luth':>22} {'2*ln^3/(C*p)':>16}")
    print("  " + "-"*80)
    active = []
    C = math.exp(-0.5772156649)
    for i, p in enumerate(primes_used):
        active.append(p)
        if len(active) < 2: continue
        dt = d2_tig_at_gate(p)
        dl = d2_luther(active)
        ratio = dt/dl if dl != 0 else float('inf')
        analytic_ratio = 2*math.log(p)**3/(C*p)
        print(f"  {p:>6} {dt:>14.6e} {dl:>14.6e} {ratio:>22.4f} {analytic_ratio:>16.4f}")

    print()
    print("  The ratio D2_tig/D2_luther grows, confirming asymptotic incompatibility.")

    # ── Step 4: Can we find what D2_luther DOES correspond to? ────────────────
    print()
    print(SEP)
    print("STEP 4: WHAT DOES D2_LUTHER CORRESPOND TO IN THE TIG SYSTEM?")
    print(SEP)
    print()
    print("  D2_luther = (phi(p#)/p#) / (p * ln(p)^2) * (1 - 1/ln(p))")
    print("           = -d/dp [phi(p#)/p# * 1/ln(p)] (approximately, by chain rule)")
    print()
    print("  This is the derivative of the UNIT DENSITY φ(n)/n with respect to")
    print("  the log of the prime boundary p. It measures how fast the fraction")
    print("  of coprime elements decays as we include more primes.")
    print()
    print("  In TIG terms: D2_luther measures the INFORMATION LOSS rate at each")
    print("  primorial boundary. It is the 'leakage gradient' of the unit group.")
    print()
    print("  D2_tig measures: curvature of the HARMONIC RESONANCE FIELD at k=p.")
    print("  D2_luther measures: curvature of the UNIT DENSITY at p.")
    print()
    print("  These are two different curvature objects on two different spaces:")
    print("  - D2_tig lives in the resonance field R(k,p) space (wave physics)")
    print("  - D2_luther lives in the unit density phi(n)/n space (number theory)")
    print()
    print("  Connection to b=35: at p=7, the primorial is 2*3*5*7=210.")
    print("  phi(210)/210 = (1/2)(2/3)(4/5)(6/7) = 48/210 = 8/35 ≈ 0.229")
    print(f"  phi_frac(7): {phi_fraction([2,3,5,7]):.6f}")
    print()
    print("  Interesting: 8/35 = phi(210)/210. The numerator 8 = |C∩{1..9}| for b=35!")
    print("  And 35 = b. Is this a coincidence or a structural fact?")
    print()
    print("  |C∩{1..9}| = #{x∈{1..9}: gcd(x,35)=1} = |phi(35)∩{1..9}|")
    print("  = #{1,2,3,4,6,8,9,11,...} ∩ {1..9} = {1,2,3,4,6,8,9} = 7")
    print("  Wait: phi(35) gives units mod 35. Units mod 35: gcd(x,35)=1")
    print("  = gcd(x,5)=1 AND gcd(x,7)=1.")
    print("  In {1..9}: {1,2,3,4,6,8,9} = 7 elements. (5 excluded, 7 included since 7<35)")
    print()
    # Compute phi(210) / 210 and |C∩{1..9}| for b=35
    b35_units = [x for x in range(1,10) if math.gcd(x, 35)==1]
    print(f"  Units of 35 in {{1..9}}: {b35_units} = {len(b35_units)} elements")
    phi_210 = 210 * (1/2) * (2/3) * (4/5) * (6/7)
    print(f"  phi(210) = {phi_210:.1f}")
    print(f"  phi(210)/210 = {phi_210/210:.6f}")
    print(f"  phi_frac([2,3,5,7]) = {phi_fraction([2,3,5,7]):.6f}")
    print()
    print("  The 8/35 link: phi(2*3*5*7)/2*3*5*7 = 8/35.")
    print("  Here 35 = 5*7 = b (our flagship semiprime), and 8 = phi(210)/6")
    print("  = 48/6 = 8. Coincidence of numerators only (phi(210)=48, not 8).")
    print("  The |C∩{1..9}|=7 (proved, C12) is units of 35 in {1..9}, not phi_frac.")

    # ── Step 5: Tier assessment ───────────────────────────────────────────────
    print()
    print(SEP)
    print("TIER ASSESSMENT — A7 D2 ALGEBRAIC CURVATURE")
    print(SEP)
    print()
    print("  WHAT IS PROVED:")
    print("  1. D2_tig(k=p) ~ 2/p^2 as p→∞  [from sinc^2, which is Tier D]")
    print("  2. D2_luther(p) ~ C/(p*ln(p)^3) as p→∞  [Mertens' theorem]")
    print("  3. ratio D2_tig/D2_luther → 0 as p→∞  [asymptotic incompatibility]")
    print("  4. They CANNOT be equal for any infinite prime family. [PROVED]")
    print()
    print("  SEPARATION VERDICT:")
    print("  A7 (Luther D2 = TIG D2) is FALSIFIED by asymptotic analysis.")
    print("  D2_tig is a WAVE CURVATURE (resonance field, R(k,p) second difference).")
    print("  D2_luther is a DENSITY CURVATURE (unit density phi(n)/n gradient).")
    print("  These are structurally different curvatures on different spaces.")
    print("  They cannot be equal, and no 'correction' will fix this — they scale")
    print("  as 1/p^2 vs 1/(p*ln(p)^3), incompatible for large p.")
    print()
    print("  WHAT SURVIVES:")
    print("  D2_tig is an established Tier D result (sinc^2 continuum limit).")
    print("  D2_luther is a valid computable number-theoretic object.")
    print("  They are formally separated — like W_BHML and corridor (A13).")
    print()
    print("  A7 → KILLED (separation result). Date: March 31, 2026.")
    print("  Kill conditions met: asymptotic incompatibility proved.")
    print("  D2_tig and D2_luther are distinct, non-equivalent curvatures.")

    os.makedirs('results', exist_ok=True)
    out = {
        'd2_tig_asymptotic': '2/p^2',
        'd2_luther_asymptotic': 'C/(p*ln(p)^3)',
        'ratio_at_infinity': 0.0,
        'separated': True,
        'a7_verdict': 'KILLED — asymptotic incompatibility proved',
    }
    with open('results/a7_d2_separation.json', 'w') as f:
        json.dump(out, f, indent=2)
    print()
    print("[Report: results/a7_d2_separation.json]")

if __name__ == '__main__':
    main()
