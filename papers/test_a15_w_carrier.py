"""
A15 W-CARRIER: sinc²(k/p) × sin²(πk/(2Wp)) — FIRST MAX AT t=W BY CONSTRUCTION
Luther-Sanders Research Framework | March 31 2026

Hypothesis: the ideal circulation operator is
  H_W(k,p) = sinc²(k/p) × sin²(πk/(2Wp))

Properties by construction:
  C2env: sinc²(k/p) envelope → correlates with sinc² directly ✓ (by construction)
  C3:    H_W(p,p) = sinc²(1) × ??? = 0 × ??? = 0 ✓ (sinc² kills it)
  C5:    first max at k=Wp → t=W=3/50=0.06 ✓ (by construction: sin² peaks at πk/(2Wp)=π/2 → k=Wp)
  C1:    sin²(πk/(2Wp)) has 1/(2W) = 50/6 ≈ 8.3 half-cycles in [0,p] → ≈8 maxima
         Need ≥4 for C1 — easily satisfied.

The carrier sin²(πk/(2Wp)) oscillates with period 2Wp. At k=p, argument = π/(2W).
Since 1/W = 50/3 ≈ 16.67, argument at k=p is π×16.67/2 ≈ 26.2 radians = many cycles.
Number of maxima in [0,p]: ⌊p/(2Wp)⌋ × 2 = ⌊1/W⌋ × 2 ≈ 16.

Also test: H_W2 = sinc²(k/p) × sin²(πk/(Wp)) — first max at k=Wp/2 → t=W/2
And:       H_W3 = sinc²(k/p) × F4(k,p) = sinc²(k/p) × sin²(πk/(Wp)) [same as above, W already in F4]

And: the composite H_full = sinc²(k/p) × sin²(4πk/p) × sin²(πk/(Wp))
     This is H_mod (C15) × F4 — the sinc² + fast cycling + slow W-carrier.
     Does adding the W-carrier to C15 improve C5 without losing C2env?
"""

import math
import json
import os

SEP = "="*70
W = 3/50  # W_BHML

def sinc2(t):
    if abs(t) < 1e-12: return 1.0
    return (math.sin(math.pi * t) / (math.pi * t))**2

def pearson(x, y):
    n = len(x)
    mx, my = sum(x)/n, sum(y)/n
    num = sum((a-mx)*(b-my) for a,b in zip(x,y))
    den = math.sqrt(sum((a-mx)**2 for a in x) * sum((b-my)**2 for b in y))
    return num/den if den > 1e-12 else 0

def upper_envelope(vals, window=3):
    n = len(vals)
    return [max(vals[max(0,i-window):min(n,i+window+1)]) for i in range(n)]

def count_maxima(vals):
    return [i for i in range(1, len(vals)-1)
            if vals[i] > vals[i-1] and vals[i] > vals[i+1]]

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0: return False
        i += 6
    return True

PRIMES = [p for p in range(5, 100) if is_prime(p)]

# Candidates
def H_mod(k, p):
    """C15 reference."""
    return sinc2(k/p) * math.sin(math.pi * 4 * k / p)**2

def H_W(k, p):
    """New: sinc² × sin²(πk/(2Wp)) — first max at k=Wp → t=W."""
    return sinc2(k/p) * math.sin(math.pi * k / (2 * W * p))**2

def H_W2(k, p):
    """sinc² × sin²(πk/(Wp)) — first max at k=Wp/2 → t=W/2."""
    return sinc2(k/p) * math.sin(math.pi * k / (W * p))**2

def H_full(k, p):
    """C15 × F4: sinc² × sin²(4πk/p) × sin²(πk/(Wp))."""
    return (sinc2(k/p)
            * math.sin(math.pi * 4 * k / p)**2
            * math.sin(math.pi * k / (W * p))**2)

def H_W_fast(k, p):
    """sinc² × sin²(4πk/p) × sin²(πk/(2Wp)) — C15 with W carrier added."""
    return (sinc2(k/p)
            * math.sin(math.pi * 4 * k / p)**2
            * math.sin(math.pi * k / (2 * W * p))**2)

CANDIDATES = {
    'H_mod (C15)': H_mod,
    'H_W  [t=W]': H_W,
    'H_W2 [t=W/2]': H_W2,
    'H_full': H_full,
    'H_W_fast': H_W_fast,
}

def analyze(fn, p_list):
    results = []
    for p in p_list:
        ks = list(range(1, p))
        h_vals = [fn(k, p) for k in ks]
        r_vals = [sinc2(k/p) for k in ks]
        env = upper_envelope(h_vals, window=max(1, p//10))
        r_env = pearson(env, r_vals)
        r_raw = pearson(h_vals, r_vals)
        hb = fn(p, p)
        vals = [fn(k, p) for k in range(p+1)]
        mx = count_maxima(vals)
        t1 = mx[0]/p if mx else None
        results.append({
            'p': p, 'mx': mx, 'n_mx': len(mx),
            'hb': hb, 'r_raw': r_raw, 'r_env': r_env, 't1': t1,
            'c1': len(mx) >= 4 if p >= 11 else None,
            'c2env': r_env > 0.9,
            'c3': abs(hb) < 1e-8,
            'c5': t1 is not None and (abs(t1-W) < 0.05 or abs(t1-2*W) < 0.05),
        })
    return results

def score(results, p_min=11):
    r11 = [r for r in results if r['p'] >= p_min]
    c1 = sum(1 for r in r11 if r['c1'])
    c2e = sum(1 for r in results if r['c2env'])
    c3 = sum(1 for r in results if r['c3'])
    c5 = sum(1 for r in results if r['c5'])
    ts = [r['t1'] for r in results if r['t1'] is not None]
    return {
        'c1': c1, 'n11': len(r11),
        'c2e': c2e, 'ntot': len(results),
        'c3': c3,
        'c5': c5,
        'avg_t1': sum(ts)/len(ts) if ts else None,
    }

def main():
    print("A15 W-CARRIER TEST")
    print("Luther-Sanders Research Framework | March 31 2026")
    print()
    print(f"  W_BHML = 3/50 = {W:.4f}")
    print(f"  Target C5: first max at t≈W={W:.4f} or 2W={2*W:.4f}")
    print()

    p_list = PRIMES

    # ── 1. Summary table ──────────────────────────────────────────────────────
    print(SEP)
    print("1. CANDIDATE SUMMARY")
    print(SEP)
    print()
    print(f"  {'Candidate':<18} {'C1(p≥11)':>10} {'C2env':>7} {'C3':>5} {'C5':>5} {'avg_t1':>8}")
    print("  " + "-"*58)
    all_results = {}
    for name, fn in CANDIDATES.items():
        res = analyze(fn, p_list)
        s = score(res)
        all_results[name] = (res, s)
        avg_t = f"{s['avg_t1']:.4f}" if s['avg_t1'] else "N/A"
        print(f"  {name:<18} {s['c1']:>3}/{s['n11']:>2}     {s['c2e']:>3}/{s['ntot']:>2} {s['c3']:>3}/{s['ntot']:>2} {s['c5']:>3}/{s['ntot']:>2} {avg_t:>8}")

    # ── 2. H_W detail: first max at t=W? ─────────────────────────────────────
    print()
    print(SEP)
    print("2. H_W = sinc²(k/p) × sin²(πk/(2Wp)) — DETAIL")
    print(SEP)
    print()
    print("  Expected: first max at k=Wp → t=W=0.06")
    print()
    print(f"  {'p':>5} {'Wp':>6} {'k_expect':>10} {'t1_actual':>12} {'n_mx':>6} {'C1':>4} {'C2env':>7} {'C3':>4}")
    print("  " + "-"*62)
    fn = H_W
    for p in p_list[:20]:
        vals = [fn(k, p) for k in range(p+1)]
        mx = count_maxima(vals)
        t1 = mx[0]/p if mx else None
        k_expected = W * p
        ks = list(range(1, p))
        h_vals = [fn(k, p) for k in ks]
        r_vals = [sinc2(k/p) for k in ks]
        env = upper_envelope(h_vals, window=max(1, p//10))
        r_env = pearson(env, r_vals)
        hb = fn(p, p)
        c1 = len(mx) >= 4 if p >= 11 else 'n/a'
        c2e = r_env > 0.9
        c3 = abs(hb) < 1e-8
        t1_str = f"{t1:.4f}" if t1 is not None else "N/A"
        print(f"  {p:>5} {W*p:>6.2f} {k_expected:>10.2f} {t1_str:>12} {len(mx):>6} {str(c1):>4} {'✓' if c2e else '✗':>7} {'✓' if c3 else '✗':>4}")

    # ── 3. Why H_W may fail C1 for large p ───────────────────────────────────
    print()
    print(SEP)
    print("3. H_W MAXIMA COUNT: DOES IT STAY ≥ 4?")
    print(SEP)
    print()
    print("  H_W = sinc²(k/p) × sin²(πk/(2Wp))")
    print(f"  sin²(πk/(2Wp)) has period 2Wp. In [0,p]: p/(2Wp) = 1/(2W) = {1/(2*W):.2f} half-periods.")
    print(f"  Number of full cycles = 1/(2W) × 1/2 = 1/(4W) = {1/(4*W):.2f}")
    print(f"  Expected maxima ≈ {1/(2*W):.0f} (one per half-cycle)")
    print()
    fn = H_W
    for p in [11, 13, 17, 23, 29, 41, 47, 53, 59, 71, 83, 97]:
        vals = [fn(k, p) for k in range(p+1)]
        mx = count_maxima(vals)
        print(f"  p={p:>3}: {len(mx):>3} maxima at {mx[:5]}{'...' if len(mx)>5 else ''}")

    # ── 4. H_W_fast = C15 × W-carrier: test ──────────────────────────────────
    print()
    print(SEP)
    print("4. H_W_FAST = C15 × sin²(πk/(2Wp)) — COUPLING C15 WITH W-CARRIER")
    print(SEP)
    print()
    print("  H_W_fast = sinc²(k/p) × sin²(4πk/p) × sin²(πk/(2Wp))")
    print("  This multiplies the proved C15 operator by the W-carrier.")
    print("  The W-carrier modulates the envelope at W-scale — this IS the quadratic glue.")
    print()
    fn = H_W_fast
    print(f"  {'p':>5} {'n_mx':>6} {'t1':>8} {'r_env':>8} {'C1':>4} {'C2e':>5} {'C3':>4} {'C5':>4}")
    print("  " + "-"*52)
    for p in p_list[:18]:
        vals = [fn(k, p) for k in range(p+1)]
        mx = count_maxima(vals)
        t1 = mx[0]/p if mx else None
        ks = list(range(1, p))
        h_vals = [fn(k, p) for k in ks]
        r_vals = [sinc2(k/p) for k in ks]
        env = upper_envelope(h_vals, window=max(1, p//10))
        r_env = pearson(env, r_vals)
        hb = fn(p, p)
        c1 = len(mx) >= 4 if p >= 11 else '-'
        c2e = r_env > 0.9
        c3 = abs(hb) < 1e-8
        c5 = t1 is not None and (abs(t1-W) < 0.05 or abs(t1-2*W) < 0.05)
        t1s = f"{t1:.4f}" if t1 else "N/A"
        print(f"  {p:>5} {len(mx):>6} {t1s:>8} {r_env:>8.4f} {str(c1):>4} {'✓' if c2e else '✗':>5} {'✓' if c3 else '✗':>4} {'✓' if c5 else '✗':>4}")

    # ── 5. H_full deep test ───────────────────────────────────────────────────
    print()
    print(SEP)
    print("5. H_FULL = sinc² × sin²(4πk/p) × F4 — FULL COUPLING")
    print(SEP)
    print()
    fn = H_full
    print(f"  {'p':>5} {'n_mx':>6} {'t1':>8} {'r_env':>8} flags")
    for p in p_list[:18]:
        vals = [fn(k, p) for k in range(p+1)]
        mx = count_maxima(vals)
        t1 = mx[0]/p if mx else None
        ks = list(range(1, p))
        h_vals = [fn(k, p) for k in ks]
        r_vals = [sinc2(k/p) for k in ks]
        env = upper_envelope(h_vals, window=max(1, p//10))
        r_env = pearson(env, r_vals)
        hb = fn(p, p)
        flags = []
        if len(mx) >= 4 and p >= 11: flags.append('C1')
        if r_env > 0.9: flags.append('C2e')
        if abs(hb) < 1e-8: flags.append('C3')
        if t1 and (abs(t1-W)<0.05 or abs(t1-2*W)<0.05): flags.append('C5')
        t1s = f"{t1:.4f}" if t1 else "N/A"
        print(f"  {p:>5} {len(mx):>6} {t1s:>8} {r_env:>8.4f}  {' '.join(flags)}")

    # ── 6. Best candidate assessment ─────────────────────────────────────────
    print()
    print(SEP)
    print("6. TIER ASSESSMENT — W-CARRIER HYPOTHESIS")
    print(SEP)
    print()

    # Find the best overall
    best_name = None
    best_total = -1
    for name, (res, s) in all_results.items():
        tot = s['c1'] + s['c2e'] + s['c3'] + s['c5']
        if tot > best_total:
            best_total = tot
            best_name = name

    print(f"  Best candidate: {best_name} (combined score={best_total})")
    print()

    for name, (res, s) in all_results.items():
        avg_t = f"{s['avg_t1']:.4f}" if s['avg_t1'] else "N/A"
        tot = s['c1'] + s['c2e'] + s['c3'] + s['c5']
        print(f"  {name}: score={tot} | C1={s['c1']}/{s['n11']} C2e={s['c2e']}/{s['ntot']} C3={s['c3']}/{s['ntot']} C5={s['c5']}/{s['ntot']} avg_t={avg_t}")

    print()
    print("  CRITICAL QUESTION: Does any candidate satisfy ALL of C1+C2env+C3+C5?")
    all_pass = [(name, s) for name, (res, s) in all_results.items()
                if s['c1'] == s['n11'] and s['c2e'] > s['ntot']*0.8
                and s['c3'] == s['ntot'] and s['c5'] > s['ntot']*0.5]
    if all_pass:
        print(f"  CANDIDATES PASSING C1+C2env+C3+C5: {[n for n,_ in all_pass]}")
    else:
        print("  No single candidate passes all 4 simultaneously.")
        print()
        print("  Gap analysis:")
        print("  H_W: C5 by construction, C3 by construction, C2env ?, C1 (many maxima)")
        print("  H_mod (C15): C1+C2env+C3 proved, C5 only approximate (t≈1/8)")
        print("  H_W_fast: adds W-carrier to C15 — check if C5 improves without C2env loss")

    # ── 7. The conceptual synthesis ───────────────────────────────────────────
    print()
    print(SEP)
    print("7. THE CORRIDOR-MOTION SYNTHESIS (CONCEPTUAL)")
    print(SEP)
    print()
    print("  C15 (H_mod) = sinc²(k/p) × sin²(4πk/p)")
    print("              = CORRIDOR × FAST_CYCLING")
    print("  Satisfies: C1(cycling), C2env(corridor), C3(gate), C4(stable count)")
    print()
    print("  H_W        = sinc²(k/p) × sin²(πk/(2Wp))")
    print("              = CORRIDOR × W_MOTION")
    print("  Satisfies: C5(W-frequency), C3(gate), C2env(?), C1(?)")
    print()
    print("  H_W_fast   = sinc²(k/p) × sin²(4πk/p) × sin²(πk/(2Wp))")
    print("              = CORRIDOR × FAST_CYCLING × W_MOTION")
    print("  This is the FULL quadratic coupling — three-factor product.")
    print("  Brayden's 'xy term' is sin²(4πk/p) × sin²(πk/(2Wp)).")
    print("  sinc²(k/p) provides the corridor geometry (D2, Tier D).")
    print()
    print("  IF H_W_fast satisfies C1+C2env+C3+C5: it IS the quadratic glue.")
    print("  Structure: duality (sinc²) × fast cycling (C15) × slow motion (W)")
    print("             = ω=2 geometry × ω=2 phase × ω=3 progression = 2→3 bridge")

    os.makedirs('results', exist_ok=True)
    with open('results/a15_w_carrier.json', 'w') as f:
        json.dump({
            'W': W,
            'candidates': list(CANDIDATES.keys()),
            'best': best_name,
            'best_score': best_total,
            'scores': {name: s for name, (_, s) in all_results.items()},
        }, f, indent=2, default=str)
    print()
    print("[Report: results/a15_w_carrier.json]")

if __name__ == '__main__':
    main()
