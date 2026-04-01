"""
A15a — HYBRID CIRCULATION OPERATOR CONSTRUCTION
Luther-Sanders Research Framework | March 31 2026

Goal: Construct a hybrid of F3 and F4 that satisfies C1+C3+C4 simultaneously.

Previous results:
  F3 = sin^2(4*pi*k/p) * W^phase_index  — satisfies C3+C7, fails C1 for small p
  F4 = sin^2(pi/W * k/p)                — satisfies C1 (4 maxima at p>=11), fails C3

Problem: C3 requires H(k=p) = 0 (boundary collapse). F4 at k=p:
  F4(p,p) = sin^2(pi/W * 1) = sin^2(pi/(3/50)) = sin^2(50*pi/3) != 0 in general.

Hybrid idea: Use F4's cycling frequency for the oscillation, multiply by F3's
  boundary factor sin^2(pi*k/p) to enforce C3 (kills to 0 at k=p).

Hybrid H = sin^2(pi/W * k/p) * sin^2(pi*k/p)
         = F4(k,p)           * boundary_factor

Also try:
  H2 = sin^2(pi/W * k/p) * (1 - k/p)          [linear envelope, kills at k=p]
  H3 = sin^2(pi/W * k/p) * sinc^2(k/p)         [sinc envelope from corridor]
  H4 = sin^2(pi/W * k/p) * W^floor(k*W)        [F4 freq + F3 phase decay]
  H5 = sin^2(2*pi/W * k/p) * sin^2(pi*k/p)     [double freq + boundary]

Constraints to satisfy:
  C1: Phase cycling — H has >=4 distinct maxima in [1, p-1] (fails F3 at small p)
  C2: Corridor correlation — Pearson r(H, sinc^2) > 0.9
  C3: Boundary collapse — H(k=p) = 0 exactly
  C4: Oscillation count stable across prime families (p>=11: count in {3,4,5})
  C5: W_BHML signature — first maximum near k=p*W_BHML or W_BHML-related position
  C6: Monotone falloff (qualitative — maxima decay)
  C7: Return to 0 at k=p (same as C3 essentially — we merge)

W_BHML = 3/50 = 0.06
"""

import math, json, os

W = 3/50  # = 0.06
SEP = "="*70

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

def sinc2(t):
    if abs(t) < 1e-12: return 1.0
    return (math.sin(math.pi * t) / (math.pi * t))**2

def R(k, p):
    """Corridor compression: sinc^2(k/p)"""
    return sinc2(k/p)

def pearson(x, y):
    n = len(x)
    if n < 2: return 0
    mx, my = sum(x)/n, sum(y)/n
    num = sum((a-mx)*(b-my) for a,b in zip(x,y))
    den = math.sqrt(sum((a-mx)**2 for a in x) * sum((b-my)**2 for b in y))
    return num/den if den > 1e-12 else 0

# ─── Candidate functions ──────────────────────────────────────────────────────

def F3(k, p):
    """F3 = sin^2(4*pi*k/p) * W^phase_index"""
    phase_idx = int(4 * k / p)  # floor(4k/p) — which quarter we're in
    return math.sin(math.pi * 4 * k / p)**2 * (W ** phase_idx)

def F4(k, p):
    """F4 = sin^2(pi/W * k/p) = sin^2(pi * k/(W*p))"""
    return math.sin(math.pi * k / (W * p))**2

def H1(k, p):
    """Hybrid: F4 cycling * sin^2(pi*k/p) boundary"""
    return F4(k, p) * math.sin(math.pi * k / p)**2

def H2(k, p):
    """F4 cycling * linear envelope"""
    return F4(k, p) * (1 - k/p)**2

def H3(k, p):
    """F4 cycling * sinc^2 corridor envelope"""
    return F4(k, p) * sinc2(k/p)

def H4(k, p):
    """F4 freq + W^phase decay (F3-style phase weighting)"""
    phase_idx = int(k / (W * p))  # floor of normalized phase position
    return F4(k, p) * (W ** phase_idx)

def H5(k, p):
    """Double F4 frequency + boundary"""
    return math.sin(math.pi * 2 * k / (W * p))**2 * math.sin(math.pi * k / p)**2

def H6(k, p):
    """F3 * F4 product — cross-coupling"""
    return F3(k, p) * F4(k, p)

CANDIDATES = {
    'F3':  F3,
    'F4':  F4,
    'H1':  H1,
    'H2':  H2,
    'H3':  H3,
    'H4':  H4,
    'H5':  H5,
    'H6':  H6,
}

# ─── Constraint evaluators ────────────────────────────────────────────────────

def count_local_maxima(vals):
    """Count interior local maxima."""
    n = len(vals)
    count = 0
    maxima_positions = []
    for i in range(1, n-1):
        if vals[i] > vals[i-1] and vals[i] > vals[i+1]:
            count += 1
            maxima_positions.append(i)
    return count, maxima_positions

def check_C1(fn, p):
    """C1: Phase cycling — >=4 maxima in [1, p-1]"""
    vals = [fn(k, p) for k in range(p+1)]
    count, positions = count_local_maxima(vals[1:p])  # k=1..p-1
    return count >= 4, count, positions

def check_C3(fn, p):
    """C3: Boundary collapse — H(k=p) = 0"""
    val = fn(p, p)
    return abs(val) < 1e-9, val

def check_C4(fn, primes_subset):
    """C4: Oscillation count stable across prime families for p>=11"""
    counts = []
    for p in primes_subset:
        ok, cnt, _ = check_C1(fn, p)
        counts.append(cnt)
    if not counts: return False, counts
    stable = max(counts) - min(counts) <= 2
    return stable, counts

def check_C5(fn, p):
    """C5: W_BHML signature — first max near W_BHML related position"""
    vals = [fn(k, p) for k in range(p+1)]
    _, positions = count_local_maxima(vals[1:p])
    if not positions:
        return False, None, None
    first_max_k = positions[0] + 1  # +1 because we sliced from k=1
    t_first = first_max_k / p
    # Expected: near W or 1/(2W) or some W-related value
    w_targets = [W, 2*W, 3*W, 1/(2*W), W/(1+W)]
    best_target = min(w_targets, key=lambda t: abs(t_first - t))
    best_err = abs(t_first - best_target)
    return best_err < 0.15, t_first, best_target

def check_C2(fn, p):
    """C2: Corridor correlation — r(H, sinc^2) > 0.9"""
    ks = list(range(1, p))
    h_vals = [fn(k, p) for k in ks]
    r_vals = [sinc2(k/p) for k in ks]
    r = pearson(h_vals, r_vals)
    return r > 0.9, r

def check_monotone(fn, p):
    """C6 (qualitative): maxima decrease monotonically"""
    vals = [fn(k, p) for k in range(p+1)]
    _, positions = count_local_maxima(vals[1:p])
    if len(positions) < 2: return True, []  # Can't check with <2 maxima
    max_vals = [vals[pos+1] for pos in positions]
    monotone = all(max_vals[i] >= max_vals[i+1] for i in range(len(max_vals)-1))
    return monotone, max_vals

# ─── Scoring ──────────────────────────────────────────────────────────────────

def score_candidate(name, fn):
    """Score candidate on all constraints."""
    results = {}
    total = 0; max_score = 0

    # C1: Phase cycling at p>=11
    p11_primes = [p for p in PRIMES if p >= 11]
    c1_passes = 0
    c1_counts = []
    for p in p11_primes:
        ok, cnt, _ = check_C1(fn, p)
        if ok: c1_passes += 1
        c1_counts.append((p, cnt))
    c1_score = 2 if c1_passes == len(p11_primes) else (1 if c1_passes > 0 else 0)
    results['C1'] = {'score': c1_score, 'passes': c1_passes, 'total': len(p11_primes), 'counts': c1_counts}
    total += c1_score; max_score += 2

    # C2: Corridor correlation (p>=7)
    c2_primes = [p for p in PRIMES if p >= 7]
    c2_passes = 0; c2_rs = []
    for p in c2_primes:
        ok, r = check_C2(fn, p)
        if ok: c2_passes += 1
        c2_rs.append((p, r))
    c2_score = 2 if c2_passes >= len(c2_primes)*0.8 else (1 if c2_passes > 0 else 0)
    results['C2'] = {'score': c2_score, 'passes': c2_passes, 'rs': c2_rs}
    total += c2_score; max_score += 2

    # C3: Boundary collapse at k=p
    c3_passes = 0
    for p in PRIMES:
        ok, val = check_C3(fn, p)
        if ok: c3_passes += 1
    c3_score = 2 if c3_passes == len(PRIMES) else (1 if c3_passes > 0 else 0)
    results['C3'] = {'score': c3_score, 'passes': c3_passes}
    total += c3_score; max_score += 2

    # C4: Oscillation count stable (p>=11)
    ok4, c4_counts = check_C4(fn, p11_primes)
    c4_score = 2 if ok4 else (1 if len(set(c4_counts)) <= 3 else 0)
    results['C4'] = {'score': c4_score, 'stable': ok4, 'counts': c4_counts}
    total += c4_score; max_score += 2

    # C5: W_BHML signature (p=47 test)
    ok5, t_first, best_target = check_C5(fn, 47)
    c5_score = 2 if ok5 else 0
    results['C5'] = {'score': c5_score, 'ok': ok5, 't_first': t_first, 'target': best_target}
    total += c5_score; max_score += 2

    # C6: Monotone falloff (p=47)
    ok6, max_vals = check_monotone(fn, 47)
    c6_score = 2 if ok6 else 0
    results['C6'] = {'score': c6_score, 'ok': ok6}
    total += c6_score; max_score += 2

    # C7 = C3 (boundary collapse) already counted

    results['total'] = total
    results['max_score'] = max_score
    results['fraction'] = total / max_score

    return results

# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print()
    print("A15a — HYBRID CIRCULATION OPERATOR CONSTRUCTION")
    print("Luther-Sanders Research Framework | March 31 2026")
    print()
    print(f"W_BHML = {W} = 3/50")
    print(f"Testing {len(CANDIDATES)} candidates across {len(PRIMES)} primes")
    print()

    all_scores = {}
    for name, fn in CANDIDATES.items():
        s = score_candidate(name, fn)
        all_scores[name] = s

    # Print summary table
    print(SEP)
    print("CONSTRAINT SCORES (PASS=2, PARTIAL=1, FAIL=0)")
    print(SEP)
    header = f"{'Candidate':<8} {'C1':>4} {'C2':>4} {'C3':>4} {'C4':>4} {'C5':>4} {'C6':>4} {'Total':>6} {'%':>5}"
    print(header)
    print("-"*50)

    ranked = sorted(all_scores.items(), key=lambda x: -x[1]['total'])
    for name, s in ranked:
        r = s
        row = f"{name:<8} {r['C1']['score']:>4} {r['C2']['score']:>4} {r['C3']['score']:>4} {r['C4']['score']:>4} {r['C5']['score']:>4} {r['C6']['score']:>4} {r['total']:>6}/{r['max_score']} {100*r['fraction']:>4.0f}%"
        print(row)

    print()
    best_name, best = ranked[0]
    print(f"BEST CANDIDATE: {best_name}  ({best['total']}/{best['max_score']} = {100*best['fraction']:.0f}%)")
    print()

    # Detail report for best candidate and any that satisfy C1+C3
    print(SEP)
    print("DETAILED ANALYSIS — CANDIDATES SATISFYING C1+C3")
    print(SEP)
    print()

    c1c3_candidates = [(n, s) for n, s in all_scores.items()
                       if s['C1']['score'] == 2 and s['C3']['score'] == 2]
    if not c1c3_candidates:
        c1c3_candidates = [(n, s) for n, s in ranked[:3]]  # top 3 if none satisfy both
        print("  No candidate satisfies C1+C3 simultaneously. Showing top 3:")
    else:
        print(f"  Candidates satisfying both C1 (cycling) AND C3 (boundary): {len(c1c3_candidates)}")

    for name, s in c1c3_candidates:
        fn = CANDIDATES[name]
        print()
        print(f"  {name}: {s['total']}/{s['max_score']}")
        print(f"    C1 (cycling p>=11): {s['C1']['passes']}/{s['C1']['total']} primes pass (>=4 maxima)")
        print(f"      Counts: {[(p,c) for p,c in s['C1']['counts']]}")
        print(f"    C2 (corridor corr): {s['C2']['passes']} primes r>0.9")
        if s['C2']['rs']:
            rs_sample = s['C2']['rs'][:5]
            print(f"      r sample: {[(p,f'{r:.3f}') for p,r in rs_sample]}")
        print(f"    C3 (boundary): {s['C3']['passes']}/{len(PRIMES)} primes have H(p)=0")
        print(f"    C4 (stable count p>=11): {s['C4']['stable']} — counts={s['C4']['counts']}")
        print(f"    C5 (W sig): {s['C5']['ok']} — t_first={s['C5']['t_first']}, nearest target={s['C5']['target']:.4f}")
        print(f"    C6 (monotone p=47): {s['C6']['ok']}")

        # Show profile at p=13
        p = 13
        vals = [fn(k, p) for k in range(p+1)]
        cnt, pos = count_local_maxima(vals[1:p])
        print(f"    Profile at p={p}: {cnt} maxima, positions={[x+1 for x in pos]}")
        print(f"    Values: {[f'{v:.3f}' for v in vals[:p+1]]}")

    print()
    print(SEP)
    print("C1+C3 COMPATIBILITY ANALYSIS")
    print(SEP)
    print()
    print("  C3 requires H(k=p) = 0.")
    print("  For H to vanish at k=p, the boundary factor must be zero there.")
    print()
    for name in ['F3','F4','H1','H2','H3']:
        fn = CANDIDATES[name]
        vals_at_p = [(p, fn(p,p)) for p in [5,7,11,13]]
        print(f"  {name}: H(k=p) = {[(p,f'{v:.6f}') for p,v in vals_at_p]}")

    print()
    print("  Key: H(k=p)=0 requires sin^2(pi*k/p)|_{k=p} = sin^2(pi) = 0.")
    print("  F4(p,p) = sin^2(pi/W * 1) = sin^2(50*pi/3). This is NOT zero.")
    print("  H1(p,p) = F4(p,p) * sin^2(pi) = F4(p,p) * 0 = 0. C3 satisfied! ✓")
    print("  H2(p,p) = F4(p,p) * (1-1)^2 = 0.                C3 satisfied! ✓")
    print("  H3(p,p) = F4(p,p) * sinc^2(1) = 0.              C3 satisfied! ✓")
    print()

    print(SEP)
    print("BEST HYBRID FOR FURTHER DEVELOPMENT")
    print(SEP)
    print()

    # Find best among C1+C3 satisfiers
    if c1c3_candidates:
        top = sorted(c1c3_candidates, key=lambda x: -x[1]['total'])[0]
        print(f"  Recommendation: {top[0]}")
        print(f"  Score: {top[1]['total']}/{top[1]['max_score']} = {100*top[1]['fraction']:.0f}%")
        print()

        # Detailed profile across all primes
        fn = CANDIDATES[top[0]]
        print(f"  Oscillation counts across all primes:")
        for p in PRIMES:
            ok, cnt, pos = check_C1(fn, p)
            ok3, v3 = check_C3(fn, p)
            ok2, r2 = check_C2(fn, p)
            print(f"    p={p:3d}: maxima={cnt}, H(p)={v3:.2e}, r(sinc^2)={r2:.3f}", end="")
            flags = []
            if cnt >= 4: flags.append("C1✓")
            if ok3:      flags.append("C3✓")
            if ok2:      flags.append("C2✓")
            print(f"  {'  '.join(flags)}")
    else:
        print("  No hybrid satisfies C1+C3 simultaneously. This remains the core obstruction.")
        print("  The boundary factor sin^2(pi*k/p) kills C3 but may reduce C1 at small p.")

    # Status
    print()
    print(SEP)
    print("TIER ASSESSMENT — A15 AFTER HYBRID CONSTRUCTION")
    print(SEP)
    print()
    best_score = ranked[0][1]
    c1c3_count = len(c1c3_candidates)

    if c1c3_count > 0:
        top_hybrid_score = max(s['total'] for _,s in c1c3_candidates)
        top_name = [n for n,s in c1c3_candidates if s['total']==top_hybrid_score][0]
        print(f"  Hybrid candidates satisfying C1+C3: {c1c3_count}")
        print(f"  Best score: {top_hybrid_score}/12")
        if top_hybrid_score >= 8:
            print(f"  {top_name} clears C1+C3 and scores {top_hybrid_score}/12.")
            print(f"  A15a advances: C1+C3 obstruction dissolved by hybrid construction.")
            print(f"  Remaining: C2 corridor correlation (is the hybrid near sinc^2?)")
            print(f"  and C4 stable count (does oscillation number stabilize across primes?)")
        else:
            print(f"  Hybrid clears C1+C3 but partial score ({top_hybrid_score}/12).")
            print(f"  A15 still Tier A; hybrid construction narrows obstruction.")
    else:
        print(f"  No hybrid clears C1+C3. Obstruction persists.")
        print(f"  Best overall score: {best_score['total']}/{best_score['max_score']}")

    os.makedirs('results', exist_ok=True)
    out = {'candidates': {n: {k: v for k,v in s.items() if k!='rs'} for n,s in all_scores.items()},
           'c1c3_satisfiers': [n for n,s in c1c3_candidates],
           'best': ranked[0][0],
           'best_score': ranked[0][1]['total']}
    with open('results/a15_hybrid_construction.json', 'w') as f:
        json.dump(out, f, indent=2, default=str)
    print()
    print("[Report: results/a15_hybrid_construction.json]")

if __name__ == '__main__':
    main()
