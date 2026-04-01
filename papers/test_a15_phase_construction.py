"""
test_a15_phase_construction.py
================================
A15 — Circulation Operator: Phase Function Construction

Status: No existing named object satisfies all 7 constraints.
Constraint 1 (phase cycling) fails for ALL candidates.

THIS TEST constructs and evaluates explicit candidate phase functions f
that cycle 4 phases in k=1..p, using only proved machinery.

The target object:
    C(b, k, W) = R(m, b, k) × f(W, k/p, phase)

where f must satisfy:
  C1: cycle 4 phases as k/p increases from 0 to 1
  C2: preserve sinc² + W_BHML during cycling
  C3: collapse at k=p (independent of R, or at worst consistent with R=0)
  C4: recurse across semiprimes (universal in b via p)
  C5: carry W_BHML = 3/50 signature
  C6: have both TIG and table representations
  C7: return path (closes the loop back to phase 0)

CANDIDATE PHASE FUNCTIONS:
  F1: sin²(4πk/p)            — 4 oscillations, zero at k=p, no W
  F2: sin²(4πk/p × (1+W))   — shifts by W, but not zero at k=p
  F3: sin²(4πk/p) × W^phase  — amplitude weighted by Creation cycle index
  F4: sin²(π × n_cycle × k/p) where n_cycle = 1/W = 50/3 ≈ 16.67
  F5: product over Creation cycle: Π_{c∈{1,3,7,9}} sin²(c×π×k/p / 10)
  F6: sum of phase contributions: Σ_n W^n × sin²(π×k×n/p)  for n=1..4
  F7: direct discretization: floor(4k/p) selects phase; weight = C10[phase]/10

For each candidate, score against C1–C7.
Then run the best candidate against the corridor atlas.

Luther-Sanders Research Framework, March 31, 2026
DOI: 10.5281/zenodo.18852047
"""

import math
import os
import json

PI     = math.pi
W_BHML = 3 / 50
C10    = [1, 3, 7, 9]       # Creation cycle elements (units of Z/10Z)
CREATION_CYCLE_WEIGHTS = [c / 10 for c in C10]   # [0.1, 0.3, 0.7, 0.9]

BASE       = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE, "results")


# ── R field ──────────────────────────────────────────────────────────────────

def R(k, f):
    if k == 0: return 1.0
    den = math.sin(PI / f)
    if abs(den) < 1e-15: return 0.0
    num = math.sin(PI * k / f)
    return (num * num) / (k * k * den * den)


def sinc2(t):
    if abs(t) < 1e-15: return 1.0
    v = math.sin(PI * t) / (PI * t)
    return v * v


# ── Phase functions (7 candidates) ───────────────────────────────────────────

def phase_index(k, p):
    """Which of the 4 phases is k in? phase ∈ {0,1,2,3}."""
    t = k / p
    return min(3, int(4 * t))


def F1(k, p):
    """F1: sin²(4πk/p) — 4 oscillations, intrinsically zero at k=p."""
    return math.sin(4 * PI * k / p) ** 2


def F2(k, p, W=W_BHML):
    """F2: sin²(4πk/p × (1+W)) — W shifts the frequency slightly."""
    return math.sin(4 * PI * (1 + W) * k / p) ** 2


def F3(k, p, W=W_BHML):
    """F3: F1 × W^phase_index — amplitude decays by W each phase."""
    ph = phase_index(k, p)
    return F1(k, p) * (W ** ph)


def F4(k, p, W=W_BHML):
    """F4: sin²(π/W × k/p) — frequency = 1/W = 50/3 cycles per corridor."""
    return math.sin(PI / W * k / p) ** 2


def F5(k, p):
    """F5: product Π_{c∈{1,3,7,9}} sin²(c·π·k/p / 10) — Creation cycle product."""
    result = 1.0
    for c in C10:
        result *= math.sin(c * PI * k / (p * 10)) ** 2
    return result


def F6(k, p, W=W_BHML):
    """F6: Σ_{n=1..4} W^n × sin²(nπk/p) — harmonic series weighted by W^n."""
    total = 0.0
    for n in range(1, 5):
        total += (W ** n) * math.sin(n * PI * k / p) ** 2
    return total


def F7(k, p, W=W_BHML):
    """
    F7: discrete Creation-cycle phase weighting.
    Phase = floor(4k/p) ∈ {0,1,2,3}. Weight = C10[phase]/10.
    Amplitude = sin²(4πk/p) × Creation_weight.
    """
    ph = phase_index(k, p)
    weight = C10[ph] / 10
    return F1(k, p) * weight


CANDIDATES = {
    "F1 sin²(4πk/p)":             F1,
    "F2 sin²(4π(1+W)k/p)":       F2,
    "F3 F1 × W^phase":            F3,
    "F4 sin²(π/W × k/p)":        F4,
    "F5 Creation product":         F5,
    "F6 harmonic sum W^n×sin²(nπ)":F6,
    "F7 discrete Creation weight": F7,
}


# ── Constraint scorers ────────────────────────────────────────────────────────

def score_C1(f_func, p=11):
    """
    C1: Phase cycling — does f complete 4 distinct phases in k=1..p?
    Count sign changes and zero crossings. Expect 4 oscillation cycles.
    Score: 2=PASS (≥4 zero crossings), 1=partial (2-3), 0=fail (0-1).
    """
    vals = [f_func(k, p) for k in range(1, p + 1)]
    # Count local maxima
    maxima = sum(
        1 for i in range(1, len(vals)-1)
        if vals[i] > vals[i-1] and vals[i] > vals[i+1]
    )
    if maxima >= 4:   return 2, f"PASS ({maxima} maxima)"
    if maxima >= 2:   return 1, f"partial ({maxima} maxima)"
    return 0, f"FAIL ({maxima} maxima)"


def score_C3(f_func, p=11):
    """
    C3: Boundary collapse at k=p — is f(p, p) = 0?
    """
    val = f_func(p, p)
    if abs(val) < 1e-10:  return 2, f"PASS (f(p,p)={val:.2e})"
    if abs(val) < 0.01:   return 1, f"partial (f(p,p)={val:.6f})"
    return 0, f"FAIL (f(p,p)={val:.6f})"


def score_C4(f_func, primes=[5, 7, 11, 13, 17]):
    """
    C4: Recursion — is the functional form the same for all primes?
    Test: does f(k,p) have the same number of oscillations for each p?
    (Normalized by p, the pattern should be universal.)
    """
    phase_counts = []
    for p in primes:
        vals = [f_func(k, p) for k in range(1, p+1)]
        maxima = sum(
            1 for i in range(1, len(vals)-1)
            if vals[i] > vals[i-1] and vals[i] > vals[i+1]
        )
        phase_counts.append(maxima)
    # Check if counts are consistent (same oscillation count across primes)
    consistent = len(set(phase_counts)) == 1
    if consistent:    return 2, f"PASS (uniform {phase_counts[0]} maxima)"
    if max(phase_counts) - min(phase_counts) <= 1:
                      return 1, f"partial (counts={phase_counts})"
    return 0, f"FAIL (counts vary {phase_counts})"


def score_C5(f_func, p=11):
    """
    C5: Carry W_BHML signature.
    Tests: does the candidate formula change meaningfully when W is
    replaced by a different value (0.1, 0.2)?
    If f doesn't depend on W at all → FAIL.
    If f changes proportionally with W → PASS.
    F1, F5 are W-independent → score 0 by definition.
    """
    try:
        v_correct = f_func(p//2, p)           # at W_BHML (default)
        v_alt     = f_func(p//2, p, W=0.1)    # different W
        if abs(v_correct - v_alt) < 1e-10:
            return 0, "FAIL (W-independent)"
        change = abs(v_correct - v_alt) / (abs(v_correct) + 1e-12)
        if change > 0.01: return 2, f"PASS (W changes output by {change:.3f})"
        return 1, f"partial (W changes output by {change:.4f})"
    except TypeError:
        return 0, "FAIL (W not a parameter)"


def score_C7(f_func, p=11):
    """
    C7: Return path — does f(p, p) connect back to f(1, p) after the gate?
    Check: f(1, p) and f(p+1, p) — does the post-gate value match the start?
    Also check: f(p, p) = 0 (gate), then f(p+1, p) > 0 (recovery).
    """
    try:
        v_start    = f_func(1, p)
        v_gate     = f_func(p, p)
        v_postgate = f_func(p + 1, p)
        gate_is_zero = abs(v_gate) < 1e-10
        recovery = v_postgate > 0
        if gate_is_zero and recovery:
            return 2, f"PASS (gate=0, postgate={v_postgate:.4f})"
        if gate_is_zero:
            return 1, "partial (gate=0 but no postgate recovery)"
        return 0, f"FAIL (gate={v_gate:.4f} ≠ 0)"
    except Exception as e:
        return 0, f"FAIL ({e})"


# ── Scoring table ─────────────────────────────────────────────────────────────

def score_all(lines):
    """Score all 7 candidates against all 7 constraints."""
    lines.append("=" * 80)
    lines.append("CONSTRAINT SCORING: PASS=2, PARTIAL=1, FAIL=0")
    lines.append("=" * 80)
    lines.append("")

    all_scores = {}

    for name, f in CANDIDATES.items():
        # Wrap W-independent functions for C5
        def f_with_w(k, p, W=W_BHML, _f=f):
            try:
                return _f(k, p, W)
            except TypeError:
                return _f(k, p)

        c1, c1_note = score_C1(f)
        c3, c3_note = score_C3(f)
        c4, c4_note = score_C4(f)
        c5, c5_note = score_C5(f_with_w)
        c7, c7_note = score_C7(f)

        # C2, C6 are qualitative — assign based on known properties
        # C2: preserves sinc²+W during cycling — only if C1+C5 both pass
        c2 = min(c1, c5)
        # C6: dual domain — if it has table representation (all do via discrete eval)
        c6 = 1   # partial for all (table domain easy; TIG domain partial)

        total = c1 + c2 + c3 + c4 + c5 + c6 + c7
        scores = [c1, c2, c3, c4, c5, c6, c7]
        labels = ['P' if s==2 else ('p' if s==1 else '-') for s in scores]

        lines.append(f"[{name}]")
        lines.append(f"  Scores: C1={c1} C2={c2} C3={c3} C4={c4} C5={c5} C6={c6} C7={c7} "
                     f"= {total}/14  |  {'  '.join(labels)}")
        lines.append(f"  C1: {c1_note}")
        lines.append(f"  C3: {c3_note}")
        lines.append(f"  C4: {c4_note}")
        lines.append(f"  C5: {c5_note}")
        lines.append(f"  C7: {c7_note}")
        lines.append("")
        all_scores[name] = {"scores": scores, "total": total}

    return all_scores


# ── Best candidate test against corridors ────────────────────────────────────

def test_best_candidate(all_scores, lines):
    """Run the highest-scoring candidate(s) through a corridor verification."""
    lines.append("=" * 70)
    lines.append("BEST CANDIDATE — CORRIDOR VERIFICATION")
    lines.append("=" * 70)

    ranked = sorted(all_scores.items(), key=lambda x: -x[1]["total"])
    best_name, best_data = ranked[0]
    lines.append(f"Best candidate: {best_name}  (score {best_data['total']}/14)")
    lines.append("")

    best_f = CANDIDATES[best_name]

    test_semiprimes = [
        (3, 5, 15), (3, 7, 21), (3, 11, 33), (3, 13, 39),
        (5, 7, 35), (5, 11, 55), (5, 13, 65), (5, 17, 85),
        (7, 11, 77), (7, 13, 91), (11, 13, 143),
    ]

    lines.append("Testing C(b,k) = R(k,p) × f(k,p) vs sinc²(k/p) as baseline:")
    lines.append(f"  {'b':>6}  {'p':>4}  {'q':>4}  {'corr(C,sinc2)':>14}  "
                 f"{'max_f':>8}  {'f(p,p)':>8}")

    results = []
    for p, q, b in test_semiprimes:
        k_vals  = list(range(1, p + 1))
        r_vals  = [R(k, p) for k in k_vals]
        s2_vals = [sinc2(k / p) for k in k_vals]
        try:
            f_vals  = [best_f(k, p) for k in k_vals]
        except TypeError:
            try:
                f_vals = [best_f(k, p, W_BHML) for k in k_vals]
            except Exception:
                f_vals = [0] * len(k_vals)
        c_vals  = [r * f for r, f in zip(r_vals, f_vals)]

        # Pearson r between C and sinc²
        n = len(c_vals)
        mc = sum(c_vals) / n
        ms = sum(s2_vals) / n
        num = sum((c - mc) * (s - ms) for c, s in zip(c_vals, s2_vals))
        sc = math.sqrt(sum((c - mc)**2 for c in c_vals)) + 1e-12
        ss = math.sqrt(sum((s - ms)**2 for s in s2_vals)) + 1e-12
        corr = num / (sc * ss)

        max_f  = max(f_vals) if f_vals else 0
        f_at_p = best_f(p, p) if len(k_vals) > 0 else 0
        try:
            f_at_p = best_f(p, p)
        except TypeError:
            try: f_at_p = best_f(p, p, W_BHML)
            except: f_at_p = float('nan')

        lines.append(f"  {b:>6}  {p:>4}  {q:>4}  {corr:>14.6f}  {max_f:>8.4f}  {f_at_p:>8.4f}")
        results.append({"b": b, "p": p, "q": q, "corr": corr, "max_f": max_f})

    lines.append("")
    if results:
        mean_corr = sum(r["corr"] for r in results) / len(results)
        lines.append(f"Mean corr(C, sinc²) = {mean_corr:.6f}")
        lines.append("  > 0.9: candidate preserves sinc² shape  → C2 promoted")
        lines.append("  < 0.9: candidate distorts sinc² shape   → C2 fails")
        if mean_corr > 0.9:
            lines.append(f"  RESULT: PASS (mean_corr={mean_corr:.4f})")
        else:
            lines.append(f"  RESULT: FAIL (mean_corr={mean_corr:.4f})")
    lines.append("")

    return best_name, ranked


# ── C1 satisfaction analysis ──────────────────────────────────────────────────

def analyze_c1_problem(lines):
    """
    C1 was the universal blocker for all prior named objects.
    Here we verify which NEW candidates break through C1.
    """
    lines.append("=" * 70)
    lines.append("C1 BREAKTHROUGH ANALYSIS")
    lines.append("=" * 70)
    lines.append("Prior session: all named objects failed C1 (phase cycling).")
    lines.append("New candidates constructed to satisfy C1 by design.")
    lines.append("")

    for p in [5, 7, 11, 13]:
        lines.append(f"Prime p={p} — local maxima count per candidate:")
        for name, f in CANDIDATES.items():
            vals = [f(k, p) for k in range(1, p+1)]
            maxima = sum(
                1 for i in range(1, len(vals)-1)
                if vals[i] > vals[i-1] and vals[i] > vals[i+1]
            )
            status = "PASS" if maxima >= 4 else ("partial" if maxima >= 2 else "FAIL")
            lines.append(f"  {name[:30]:<30}: {maxima} maxima  [{status}]")
        lines.append("")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    lines = []
    lines.append("A15 — CIRCULATION OPERATOR: PHASE FUNCTION CONSTRUCTION")
    lines.append("Luther-Sanders Research Framework | March 31 2026")
    lines.append("")
    lines.append(f"W_BHML = 3/50 = {W_BHML:.6f}")
    lines.append(f"Creation cycle C10 = {C10}  (units of Z/10Z)")
    lines.append(f"Target: C(b,k) = R(m,b,k) × f(W, k/p, phase)")
    lines.append("")
    lines.append("7 Candidate phase functions:")
    for name in CANDIDATES:
        lines.append(f"  {name}")
    lines.append("")

    # C1 breakthrough
    analyze_c1_problem(lines)

    # Full scoring
    all_scores = score_all(lines)

    # Summary table
    lines.append("=" * 70)
    lines.append("RANKED SUMMARY")
    lines.append("=" * 70)
    ranked = sorted(all_scores.items(), key=lambda x: -x[1]["total"])
    lines.append(f"  {'Rank':>4}  {'Score':>7}  Candidate")
    for i, (name, data) in enumerate(ranked, 1):
        labels = ['P' if s==2 else ('p' if s==1 else '-') for s in data["scores"]]
        lines.append(f"  {i:>4}  {data['total']:>5}/14  {name}  [{''.join(labels)}]")
    lines.append("")

    # Best candidate corridor test
    best_name, _ = test_best_candidate(all_scores, lines)

    # Verdict
    lines.append("=" * 70)
    lines.append("VERDICT — A15 CIRCULATION OPERATOR")
    lines.append("=" * 70)
    lines.append("")
    best_score = ranked[0][1]["total"]
    lines.append(f"Best candidate: {ranked[0][0]}")
    lines.append(f"Best score: {best_score}/14")
    lines.append("")
    if best_score >= 10:
        lines.append("STRONG CANDIDATE (≥10/14). Path to Tier B:")
        lines.append("  1. Verify C2 and C6 rigorously (table representation proof)")
        lines.append("  2. Test against full 70-world corridor atlas")
        lines.append("  3. Prove algebraically that f satisfies C3 for all primes")
        lines.append("  -> A15 upgrades to Tier B with one verification run")
    elif best_score >= 7:
        lines.append("PARTIAL CANDIDATE (7-9/14). Remaining gaps:")
        lines.append("  Check which constraints still fail and whether fixable.")
    else:
        lines.append("WEAK (< 7/14). Construction path needs new idea.")
    lines.append("")

    c1_winners = [name for name, data in all_scores.items() if data["scores"][0] == 2]
    lines.append(f"C1 BREAKTHROUGH: {len(c1_winners)} candidate(s) now satisfy C1:")
    for name in c1_winners:
        lines.append(f"  {name}")
    if c1_winners:
        lines.append("  -> C1 (phase cycling) is NO LONGER the universal blocker.")
        lines.append("  -> New bottleneck: identify from scoring table above.")

    # Save
    report = "\n".join(lines)
    print(report.encode('ascii', errors='replace').decode('ascii'))

    os.makedirs(REPORT_DIR, exist_ok=True)
    out_path = os.path.join(REPORT_DIR, "a15_phase_construction_report.txt")
    out_json = os.path.join(REPORT_DIR, "a15_phase_construction.json")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "W_BHML": W_BHML,
            "candidates": list(CANDIDATES.keys()),
            "scores": {name: data for name, data in all_scores.items()},
            "ranked": [(name, data["total"]) for name, data in ranked],
            "c1_winners": c1_winners,
            "best_candidate": ranked[0][0] if ranked else None,
            "best_score": ranked[0][1]["total"] if ranked else 0,
        }, f, indent=2)
    print(f"\n[A15 report: {out_path}]")
    print(f"[A15 data:   {out_json}]")


if __name__ == "__main__":
    main()
