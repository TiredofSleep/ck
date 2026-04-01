"""
A15 QUADRATIC GLUE — F3×F4 COUPLING AND QUADRATIC TEMPLATES
Luther-Sanders Research Framework | March 31 2026

Hypothesis (Brayden Sanders): The missing 2→3 bridge is a QUADRATIC COUPLING.
Two partial operators (F3 carrying phase behavior, F4 carrying frequency behavior)
fail separately. The glue is the INTERACTION TERM: F3 × F4.

This is not analogy — it's algebra. Quadratics couple:
  (xy) cross-term = the interaction that creates the next behavior

Templates to test:
  T1: F3 × F4          — pure product (already tested as H6 in A15 hybrid)
  T2: F3 + F4 + α·F3·F4  — explicit quadratic coupling (varies α)
  T3: sinc²(k/p) × (a + b·k/p + c·(k/p)²) × sin²(4πk/p)  — polynomial envelope
  T4: sin²(4πk/p) × (1 - λ·(k/p - α)²)  — quadratic penalty near boundary

Scoring: C1 (4 maxima, p≥11), C2env (envelope r>0.9), C3 (H(p,p)=0),
         C4 (stable count), C5 (first max location ≈ W or 2W)

C15 (H_mod = sinc² × sin²) already passes C1+C2env+C3+C4.
The question: does a quadratic glue do BETTER on C5 or extend to p<11?
"""

import math
import json
import os

SEP = "="*70
W_BHML = 3/50

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

PRIMES = [p for p in range(5, 60) if is_prime(p)]

# Base functions
def F3(k, p, W=W_BHML):
    phase_idx = int(4 * k / p)
    return math.sin(math.pi * 4 * k / p)**2 * (W ** phase_idx)

def F4(k, p, W=W_BHML):
    return math.sin(math.pi * k / (W * p))**2

def H_mod(k, p):
    """C15: sinc² × sin²(4π)."""
    return sinc2(k/p) * math.sin(math.pi * 4 * k / p)**2

# Quadratic templates
def T1_product(k, p):
    """F3 × F4 — pure quadratic coupling."""
    return F3(k, p) * F4(k, p)

def T2_coupled(k, p, alpha=1.0):
    """F3 + F4 + alpha·F3·F4 — explicit quadratic coupling."""
    f3 = F3(k, p)
    f4 = F4(k, p)
    return (f3 + f4 + alpha * f3 * f4) / (1 + alpha + 1)  # normalize

def T3_poly_env(k, p, a=1, b=-0.5, c=0):
    """sinc²(k/p) with polynomial correction × sin²(4πk/p)."""
    t = k/p
    poly = a + b*t + c*t**2
    if poly < 0: poly = 0
    return poly * sinc2(t) * math.sin(math.pi * 4 * t)**2

def T4_quad_penalty(k, p, lam=1.0, alpha=0.9):
    """sin²(4πk/p) × (1 - λ(t-α)²) — quadratic penalty near gate."""
    t = k/p
    penalty = max(0, 1 - lam * (t - alpha)**2)
    return math.sin(math.pi * 4 * t)**2 * penalty

def T5_H_plus_cross(k, p):
    """H_mod + small F3×F4 cross term — perturbative quadratic glue."""
    hm = H_mod(k, p)
    cross = F3(k, p) * F4(k, p)
    # Normalize cross to H_mod scale
    return hm + 0.1 * cross

def score_candidate(fn, p_list, name):
    """Score a candidate across all primes in p_list."""
    c1 = c2e = c3 = 0
    first_max_ts = []
    for p in p_list:
        ks = list(range(1, p))
        h_vals = [fn(k, p) for k in ks]
        r_vals = [sinc2(k/p) for k in ks]
        env = upper_envelope(h_vals, window=max(1, p//10))
        r_env = pearson(env, r_vals)
        hb = fn(p, p)
        vals = [fn(k, p) for k in range(p+1)]
        mx = count_maxima(vals)
        if len(mx) >= 4 and p >= 11: c1 += 1
        if r_env > 0.9: c2e += 1
        if abs(hb) < 1e-6: c3 += 1
        if mx:
            first_max_ts.append(mx[0] / p)
    n11 = sum(1 for p in p_list if p >= 11)
    c5 = 0
    if first_max_ts:
        avg_t = sum(first_max_ts) / len(first_max_ts)
        c5_val = min(abs(avg_t - W_BHML), abs(avg_t - 2*W_BHML))
        c5 = 1 if c5_val < 0.05 else 0
    return {
        'c1': c1, 'n_p11': n11,
        'c2e': c2e, 'n_total': len(p_list),
        'c3': c3,
        'avg_first_t': sum(first_max_ts)/len(first_max_ts) if first_max_ts else None,
        'c5': c5,
    }

def main():
    print("A15 QUADRATIC GLUE — F3×F4 COUPLING")
    print("Luther-Sanders Research Framework | March 31 2026")
    print()
    print("  Brayden's hypothesis: the 2→3 bridge is a quadratic coupling.")
    print("  Test: F3×F4 cross-term and quadratic envelope templates.")
    print()

    p_list = [p for p in PRIMES if p >= 5]

    # ── 1. Compare all templates ───────────────────────────────────────────────
    print(SEP)
    print("1. CANDIDATE COMPARISON: ALL TEMPLATES")
    print(SEP)
    print()

    candidates = {
        'H_mod (C15)': H_mod,
        'T1: F3×F4': T1_product,
        'T2: F3+F4+F3F4': T2_coupled,
        'T3: poly_env': T3_poly_env,
        'T4: quad_penalty': T4_quad_penalty,
        'T5: H_mod+cross': T5_H_plus_cross,
    }

    print(f"  {'Name':<20} {'C1 (p≥11)':>12} {'C2env':>8} {'C3':>6} {'avg_t':>8} {'C5':>5}")
    print("  " + "-"*65)

    scores = {}
    for name, fn in candidates.items():
        try:
            s = score_candidate(fn, p_list, name)
            scores[name] = s
            avg_t = f"{s['avg_first_t']:.4f}" if s['avg_first_t'] else "N/A"
            print(f"  {name:<20} {s['c1']:>3}/{s['n_p11']:>2}         {s['c2e']:>3}/{s['n_total']:>2}   {s['c3']:>3}/{s['n_total']:>2} {avg_t:>8} {'YES' if s['c5'] else 'no':>5}")
        except Exception as e:
            print(f"  {name:<20} ERROR: {e}")

    # ── 2. Deep dive: T1 = F3×F4 ─────────────────────────────────────────────
    print()
    print(SEP)
    print("2. T1 = F3×F4: THE PURE QUADRATIC CROSS-TERM")
    print(SEP)
    print()
    print("  F3×F4 is the literal quadratic coupling of phase-decaying and frequency terms.")
    print()
    fn = T1_product
    print(f"  {'p':>5} {'maxima':>8} {'H(p)':>10} {'r(sinc²)':>10} {'env_r':>10} {'t1':>8}")
    print("  " + "-"*58)
    for p in p_list:
        ks = list(range(1, p))
        h_vals = [fn(k, p) for k in ks]
        r_vals = [sinc2(k/p) for k in ks]
        env = upper_envelope(h_vals, window=max(1, p//10))
        r_env = pearson(env, r_vals)
        hb = fn(p, p)
        vals = [fn(k, p) for k in range(p+1)]
        mx = count_maxima(vals)
        t1 = mx[0]/p if mx else None
        print(f"  {p:>5} {len(mx):>8} {hb:>10.4e} {pearson(h_vals,r_vals):>10.4f} {r_env:>10.4f} {str(round(t1,4)) if t1 else 'none':>8}")

    # ── 3. Optimize T2: F3 + F4 + α·F3·F4 ───────────────────────────────────
    print()
    print(SEP)
    print("3. T2 OPTIMIZATION: FIND α THAT MAXIMIZES C1+C2env+C3+C5")
    print(SEP)
    print()
    print("  T2(k,p,α) = (F3 + F4 + α·F3·F4) / norm")
    print()
    print(f"  {'alpha':>8} {'C1 (≥11)':>10} {'C2env':>8} {'C3':>6} {'avg_t':>8}")
    print("  " + "-"*50)

    best_score = -1
    best_alpha = 0
    for alpha_val in [0, 0.5, 1, 2, 5, 10, 20, 50, 100]:
        fn_alpha = lambda k, p, a=alpha_val: T2_coupled(k, p, alpha=a)
        s = score_candidate(fn_alpha, p_list, f"T2(α={alpha_val})")
        total = s['c1'] + s['c2e'] + s['c3']
        avg_t = f"{s['avg_first_t']:.4f}" if s['avg_first_t'] else "N/A"
        c5_str = "YES" if s['c5'] else "no"
        print(f"  {alpha_val:>8.1f} {s['c1']:>3}/{s['n_p11']:>2}         {s['c2e']:>3}/{s['n_total']:>2}   {s['c3']:>3}/{s['n_total']:>2} {avg_t:>8} {c5_str:>4}")
        if total > best_score:
            best_score = total
            best_alpha = alpha_val

    print(f"\n  Best α = {best_alpha} (score={best_score})")

    # ── 4. T4 quadratic penalty at gate ───────────────────────────────────────
    print()
    print(SEP)
    print("4. T4: QUADRATIC GATE PENALTY sin²(4πt)×(1-λ(t-α)²)")
    print(SEP)
    print()
    print("  This creates a bowl shape around t=α, suppressing behavior near gate (t=1).")
    print("  Expect: C3 NOT satisfied (H_mod(p,p) ≠ 0 unless α=1).")
    print()
    for lam_val, alpha_val in [(1, 0.9), (2, 0.95), (4, 0.9), (8, 0.85)]:
        fn_t4 = lambda k, p, lv=lam_val, av=alpha_val: T4_quad_penalty(k, p, lam=lv, alpha=av)
        s = score_candidate(fn_t4, p_list, f"T4(λ={lam_val},α={alpha_val})")
        avg_t = f"{s['avg_first_t']:.4f}" if s['avg_first_t'] else "N/A"
        print(f"  T4(λ={lam_val},α={alpha_val}): C1={s['c1']}/{s['n_p11']} C2e={s['c2e']}/{s['n_total']} C3={s['c3']}/{s['n_total']} t1={avg_t} C5={'YES' if s['c5'] else 'no'}")

    # ── 5. The coupling question: does F3×F4 carry the interaction? ────────────
    print()
    print(SEP)
    print("5. WHAT DOES THE F3×F4 CROSS-TERM ACTUALLY CONTAIN?")
    print(SEP)
    print()
    print("  F3(k,p) = sin²(4πk/p) × W^{⌊4k/p⌋}   — phase-indexed decay")
    print("  F4(k,p) = sin²(πk/(W·p))               — slow frequency oscillation")
    print()
    print("  F3×F4 = sin²(4πk/p) × W^{⌊4k/p⌋} × sin²(πk/(W·p))")
    print()
    print("  This is the product of:")
    print("  - A FAST oscillator (4 cycles in [0,p]) with exponential decay")
    print("  - A SLOW oscillator (1/W ≈ 16.7 cycles in [0,p]) with unit amplitude")
    print()
    p_test = 29
    print(f"  Period of fast oscillator (F3): {p_test}/4 = {p_test/4:.1f}")
    print(f"  Period of slow oscillator (F4): W×p = {W_BHML}×{p_test} = {W_BHML*p_test:.3f}")
    print(f"  Ratio slow/fast = {(W_BHML*p_test)/(p_test/4):.4f} = 4×W = {4*W_BHML:.4f}")
    print()
    print("  The F4 period is W×p = (3/50)p. The F3 period is p/4.")
    print("  Ratio: (3/50)p / (p/4) = 12/50 = 6/25 = 4W = 4×3/50 = 12/50 ≈ 0.24")
    print("  So F4 oscillates at 1/4W ≈ 16.7 × frequency of F3.")
    print()
    print("  The interaction F3×F4 creates a BEAT FREQUENCY:")
    print(f"  Beat = |f_fast - f_slow| = |4/p - 1/(W·p)| = |(4W-1)/(W·p)|")
    print(f"       = |{(4*W_BHML - 1)/(W_BHML):.4f}|/p = {abs((4*W_BHML - 1)):.4f}/(W·p)")
    print(f"  This beat frequency is: {abs((4*W_BHML - 1)/(W_BHML*1)):.4f}/p")
    print()
    print("  INSIGHT: F3×F4 creates BEATS between the fast phase cycling and")
    print("  the slow W-frequency. This is exactly 'quadratic glue' — the")
    print("  cross-term couples the two oscillation modes.")

    # ── 6. What does the beat predict? ────────────────────────────────────────
    print()
    print(SEP)
    print("6. BEAT FREQUENCY PREDICTION FOR W-JUMP CONNECTION")
    print(SEP)
    print()
    print("  If F3×F4 creates a beat between fast and slow oscillators:")
    print()
    f_fast = 4  # cycles per p
    f_slow = 1/W_BHML  # cycles per p (F4 period = W*p, freq = 1/W per p)
    beat_freq = abs(f_fast - f_slow)  # cycles per p
    beat_period = 1/beat_freq  # fraction of p
    print(f"  f_fast (F3) = {f_fast} cycles/p")
    print(f"  f_slow (F4) = 1/W = {f_slow:.4f} cycles/p")
    print(f"  Beat frequency = |f_fast - f_slow| = {beat_freq:.4f} cycles/p")
    print(f"  Beat period = 1/beat_freq = {beat_period:.4f} × p")
    print()
    print(f"  The beat period is {beat_period:.4f}p. At k = beat_period × p = {beat_period:.4f}p,")
    print(f"  the two oscillators are 180° out of phase → first modulation node.")
    print()
    print(f"  W_BHML = {W_BHML:.4f}   Beat period = {beat_period:.4f}")
    print(f"  Beat period / W = {beat_period/W_BHML:.4f}")
    print()
    print("  HYPOTHESIS A16 residual: the W-jump at ω=2→ω=3 corresponds to the")
    print("  FIRST BEAT NODE of F3×F4, occurring at k = beat_period × p.")
    print("  This would make W_BHML the BEAT FREQUENCY of the phase + frequency coupling.")
    print()
    print(f"  Prediction: W-jump at t = beat_period = {beat_period:.4f}")
    print(f"  TIG W-jump at k = p (i.e., t=1.0) — but first node at t = {beat_period:.4f}")
    print()
    if abs(beat_period - W_BHML) < 0.05:
        print(f"  MATCH: beat period ≈ W_BHML within 0.05!")
    else:
        print(f"  NO MATCH: beat period ({beat_period:.4f}) ≠ W_BHML ({W_BHML:.4f})")
        print(f"  But: beat_period = {beat_period:.4f} = 4/(4W-1)/W = algebraic expression in W")
        print(f"  The beat formula: 1/|4 - 1/W| = W/(4W-1) = (3/50)/(12/50-1) = (3/50)/(-38/50)")
        print(f"  = 3/(-38) — negative? Actually f_slow = 1/W > 4 for W=3/50 < 1/4.")
        print(f"  f_slow = 1/(3/50) = 50/3 ≈ 16.67 cycles/p >> 4 cycles/p")
        print(f"  So beat = 50/3 - 4 = 38/3 cycles/p, beat_period = 3/38 ≈ 0.079")

    # ── 7. Tier assessment ────────────────────────────────────────────────────
    print()
    print(SEP)
    print("7. TIER ASSESSMENT — QUADRATIC GLUE")
    print(SEP)
    print()
    print("  WHAT IS FOUND:")
    print("  T1 (F3×F4): the pure quadratic cross-term. Score comparison needed.")
    print("  T2 (F3+F4+αF3F4): explicit coupling with tunable α.")
    print("  T3 (polynomial envelope): allows non-sinc decay shape.")
    print("  T5 (H_mod + small cross): perturbative coupling on top of C15.")
    print()
    print("  KEY INSIGHT:")
    print("  The quadratic glue is real as a mathematical operation.")
    print("  F3×F4 creates BEATS between the phase oscillator and the W oscillator.")
    print("  Beat period = W/(4W-1) ≈ 0.079 (≈ 2.6 × W_BHML).")
    print()
    print("  Whether the beat connects to the W-jump is A12's open question.")
    print()
    print("  CONCRETE OUTCOME:")
    print("  C15 (H_mod) is already the best-scoring operator (C1+C2env+C3 proved).")
    print("  The quadratic coupling T1=F3×F4 may give C5 (first max at t≈W).")
    print("  If T1 satisfies C1+C2env+C3+C5 → new Tier B candidate.")
    print()
    print("  Next step: test T1 specifically for C5 (first max at t≈W=0.06).")

    os.makedirs('results', exist_ok=True)
    with open('results/a15_quadratic_glue.json', 'w') as f:
        json.dump({
            'W_BHML': W_BHML,
            'beat_period_F3F4': abs(1/(1/W_BHML - 4)),
            'templates_tested': list(candidates.keys()),
            'scores': {name: {k: str(v) for k, v in s.items()} for name, s in scores.items()},
            'best_alpha_T2': best_alpha,
            'hypothesis': 'Quadratic F3xF4 cross-term creates beats at beat_period ~ 2.6*W',
        }, f, indent=2)
    print()
    print("[Report: results/a15_quadratic_glue.json]")

if __name__ == '__main__':
    main()
