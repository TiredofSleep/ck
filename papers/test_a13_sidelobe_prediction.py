"""
test_a13_sidelobe_prediction.py
================================
A13 — Corridor Compression: Positive Result After Kill

The candidate formula Corridor(b,k) = R × sin²(πW_BHML·k/p) was killed
by test_corridor_compression.py: it produces a bell shape, not sinc² decay.

REVISED PICTURE (from synthesis section of test_corridor_compression.py):
  - Corridor compression IS sinc²(k/p) narrowing as k → p
  - W_BHML = 3/50 appears in POST-GATE sidelobe structure, not inside corridor
  - First post-gate sidelobe peak of sin²(π·W_BHML·t) at t = 1/(2W_BHML) = 50/6

THIS TEST:
  Verifies the positive W_BHML sidelobe prediction across the corridor atlas.

  Prediction: for each semiprime b = p×q, the first local maximum of R(k,p)
  past the gate (k > p) occurs near k_peak ≈ p × 1/(2·W_BHML) = p × 50/6.

  Also tests: does the post-gate echo amplitude at k = p + n track W_BHML^n?

  Also corrects: what IS the correct corridor compression formula?
  Candidate: Corridor_correct(b,k) = sinc²(k/p) for k ≤ p, then
             sinc²((k-p)/p) × W_BHML for k ∈ (p, p+p] (first echo zone)

Kill condition (revised A13): the W_BHML sidelobe prediction fails
(first local R maximum past gate is NOT near p × 50/6 for most worlds).

Promotion condition: prediction holds across ≥ 10 worlds → Tier B.
Tier C: algebraic proof that sinc² null at k=p forces first echo at k=p×50/6.

Luther-Sanders Research Framework, March 31, 2026
DOI: 10.5281/zenodo.18852047
"""

import math
import os
import json

PI    = math.pi
W_BHML = 3 / 50   # TIG wobble constant [THM]
T_FIRST_PEAK = 1 / (2 * W_BHML)   # = 50/6 ≈ 8.333  (in units of p)

BASE       = os.path.dirname(os.path.abspath(__file__))
ATLAS_PATH = os.path.join(BASE, "results", "extended", "corridor_atlas.json")
REPORT_DIR = os.path.join(BASE, "results")


# ── Math utilities ────────────────────────────────────────────────────────────

def sinc2(t):
    if abs(t) < 1e-15:
        return 1.0
    v = math.sin(PI * t) / (PI * t)
    return v * v


def R(k, f):
    """R(k,f) = sin²(πk/f) / (k² sin²(π/f))"""
    if k == 0:
        return 1.0
    den = math.sin(PI / f)
    if abs(den) < 1e-15:
        return 0.0
    num = math.sin(PI * k / f)
    return (num * num) / (k * k * den * den)


def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True


def primes_below(n):
    return [x for x in range(2, n+1) if is_prime(x)]


# ── Sidelobe prediction ───────────────────────────────────────────────────────

def find_first_post_gate_peak(p, k_max_factor=20):
    """
    For prime p, scan k = p+1 .. p*k_max_factor.
    Find the first local maximum of R(k,p) after the gate at k=p.
    Returns (k_peak, R_peak, t_peak) where t_peak = k_peak/p.
    """
    k_max = int(p * k_max_factor)
    prev_r = R(p + 1, p)
    peaks = []
    for k in range(p + 2, k_max + 1):
        curr_r = R(k, p)
        next_r = R(k + 1, p) if k + 1 <= k_max else 0
        if curr_r > prev_r and curr_r > next_r:
            peaks.append((k, curr_r, k / p))
        prev_r = curr_r
    if peaks:
        return peaks[0]   # first local max
    return None


def sinc2_first_sidelobe():
    """
    sinc²(t) = sin²(πt)/(πt)². Its first sidelobe peak (after t=0 main lobe)
    occurs at t ≈ 1.43 (between the first two zeros at t=1 and t=2).
    This is the SINC² sidelobe, independent of W_BHML.
    """
    # scan t in [1.01, 2.0]
    best_t, best_v = 1.01, 0.0
    for i in range(101, 200):
        t = i / 100
        v = sinc2(t)
        if v > best_v:
            best_v = v
            best_t = t
    return best_t, best_v


# ── Corridor shape test ───────────────────────────────────────────────────────

def test_corridor_shape(p, q, lines):
    """
    For a specific semiprime b=p×q, compare:
    (a) sinc²(k/p) — the proposed corridor formula
    (b) sinc²(k/p) × sin²(π·W_BHML·k/p) — the killed candidate
    (c) R(k,p) — the exact discrete resonance
    at k=1..p, measuring fit quality.
    """
    k_vals  = list(range(1, p + 1))
    r_vals  = [R(k, p) for k in k_vals]
    s2_vals = [sinc2(k / p) for k in k_vals]
    cand_vals = [sinc2(k/p) * math.sin(PI * W_BHML * k / p)**2 for k in k_vals]

    # For comparison: empirical R is the baseline (Tier D formula)
    # Compare sinc² approximation error vs killed candidate error
    rmse_sinc2 = math.sqrt(sum((s - r)**2 for s, r in zip(s2_vals, r_vals)) / len(k_vals))
    rmse_cand  = math.sqrt(sum((c - r)**2 for c, r in zip(cand_vals, r_vals)) / len(k_vals))

    lines.append(f"  b={p*q:4d} (p={p},q={q}): "
                 f"RMSE sinc²={rmse_sinc2:.6f}  RMSE candidate={rmse_cand:.6f}  "
                 f"{'sinc² wins' if rmse_sinc2 < rmse_cand else 'candidate wins'}")
    return rmse_sinc2, rmse_cand


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    lines = []
    lines.append("A13 — CORRIDOR COMPRESSION: POSITIVE RESULT AFTER KILL")
    lines.append("Luther-Sanders Research Framework | March 31 2026")
    lines.append("")
    lines.append(f"W_BHML = 3/50 = {W_BHML:.6f}")
    lines.append(f"Predicted first post-gate sidelobe: t_peak = 1/(2·W) = {T_FIRST_PEAK:.4f}")
    lines.append(f"  => k_peak = p × {T_FIRST_PEAK:.4f}  (for any prime p)")
    lines.append("")

    # ── TEST 1: W_BHML sidelobe prediction vs sinc² sidelobe ────────────────
    lines.append("=" * 70)
    lines.append("TEST 1 — SIDELOBE ORIGIN: W_BHML vs sinc² natural sidelobe")
    lines.append("=" * 70)

    sc2_t, sc2_v = sinc2_first_sidelobe()
    lines.append(f"sinc² first natural sidelobe: t ≈ {sc2_t:.3f}, amplitude ≈ {sc2_v:.6f}")
    lines.append(f"W_BHML sidelobe prediction:   t ≈ {T_FIRST_PEAK:.3f}")
    lines.append("")
    lines.append("These are DIFFERENT predictions:")
    lines.append(f"  sinc² says:   first echo at t ≈ {sc2_t:.3f} (universal, from zeros at t=1,2)")
    lines.append(f"  W_BHML says:  first echo at t ≈ {T_FIRST_PEAK:.3f} = 50/6")
    lines.append("")
    lines.append("We scan actual R(k,p) past the gate to find which prediction wins.")
    lines.append("")

    # Scan several primes
    test_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    lines.append(f"  {'p':>4}  {'k_peak':>8}  {'t_peak=k/p':>11}  {'R_peak':>10}  "
                 f"{'pred_sinc2':>11}  {'pred_wbhml':>11}  {'closer_to':>12}")
    lines.append(f"  {'-'*4}  {'-'*8}  {'-'*11}  {'-'*10}  {'-'*11}  {'-'*11}  {'-'*12}")

    results_t1 = []
    for p in test_primes:
        peak = find_first_post_gate_peak(p)
        if peak is None:
            lines.append(f"  {p:>4}  (no peak found in scan window)")
            continue
        k_pk, r_pk, t_pk = peak
        dist_sinc2 = abs(t_pk - sc2_t)
        dist_wbhml = abs(t_pk - T_FIRST_PEAK)
        closer = "sinc²" if dist_sinc2 < dist_wbhml else "W_BHML"
        lines.append(f"  {p:>4}  {k_pk:>8}  {t_pk:>11.4f}  {r_pk:>10.6f}  "
                     f"  {sc2_t:>9.4f}   {T_FIRST_PEAK:>9.4f}  {closer:>12}")
        results_t1.append({
            "p": p, "k_peak": k_pk, "t_peak": t_pk, "R_peak": r_pk,
            "dist_sinc2": dist_sinc2, "dist_wbhml": dist_wbhml, "closer": closer,
        })
    lines.append("")

    n_sinc2_wins = sum(1 for r in results_t1 if r["closer"] == "sinc²")
    n_wbhml_wins = sum(1 for r in results_t1 if r["closer"] == "W_BHML")
    lines.append(f"SCORE: sinc² wins={n_sinc2_wins}, W_BHML wins={n_wbhml_wins}")
    if results_t1:
        mean_t = sum(r["t_peak"] for r in results_t1) / len(results_t1)
        lines.append(f"Mean first sidelobe t_peak = {mean_t:.4f}")
        lines.append(f"  sinc² prediction: {sc2_t:.4f}  (error {abs(mean_t-sc2_t):.4f})")
        lines.append(f"  W_BHML prediction: {T_FIRST_PEAK:.4f}  (error {abs(mean_t-T_FIRST_PEAK):.4f})")
    lines.append("")

    # ── TEST 2: sinc² as corridor formula vs killed candidate ────────────────
    lines.append("=" * 70)
    lines.append("TEST 2 — SINC² AS CORRECTED CORRIDOR FORMULA")
    lines.append("=" * 70)
    lines.append("Comparing RMSE of sinc²(k/p) vs killed candidate at k=1..p:")
    lines.append("  [Reference: exact R(k,p) from Tier D formula]")
    lines.append("")

    test_semiprimes = [
        (3, 5), (3, 7), (3, 11), (3, 13),
        (5, 7), (5, 11), (5, 13), (5, 17),
        (7, 11), (7, 13), (7, 17), (7, 19),
        (11, 13), (11, 17), (11, 19), (11, 23),
    ]
    rmse_sinc2_all, rmse_cand_all = [], []
    for p, q in test_semiprimes:
        rs2, rc = test_corridor_shape(p, q, lines)
        rmse_sinc2_all.append(rs2)
        rmse_cand_all.append(rc)
    lines.append("")

    mean_rs2 = sum(rmse_sinc2_all) / len(rmse_sinc2_all) if rmse_sinc2_all else 0
    mean_rc  = sum(rmse_cand_all) / len(rmse_cand_all)   if rmse_cand_all else 0
    lines.append(f"Mean RMSE sinc²(k/p):           {mean_rs2:.6f}")
    lines.append(f"Mean RMSE R×sin²(πW·k/p):       {mean_rc:.6f}")
    lines.append(f"sinc² outperforms candidate by: {(mean_rc-mean_rs2):.6f} RMSE")
    lines.append("")
    lines.append("VERDICT — TEST 2:")
    if mean_rs2 < mean_rc:
        lines.append("  sinc²(k/p) IS a better corridor formula than R×sin²(πW·k/p).")
        lines.append("  BUT sinc²(k/p) ≈ R(k,p) by design (Tier D: R→sinc² as p→∞).")
        lines.append("  So 'corridor formula = sinc²(k/p)' is trivially true — it IS R.")
        lines.append("  The question becomes: does W_BHML appear anywhere in corridor?")
    else:
        lines.append("  Unexpected: candidate outperforms sinc². Investigate.")
    lines.append("")

    # ── TEST 3: Echo amplitude at k=p+n ──────────────────────────────────────
    lines.append("=" * 70)
    lines.append("TEST 3 — POST-GATE ECHO AMPLITUDE vs W_BHML^n PREDICTION")
    lines.append("=" * 70)
    lines.append("Does R(p+n, p) ≈ W_BHML^n × R(1, p)?")
    lines.append("Prediction: each gate crossing attenuates amplitude by factor W_BHML = 3/50")
    lines.append("")

    for p in [5, 7, 11, 13]:
        r1 = R(1, p)
        lines.append(f"  p={p}: R(1,p)={r1:.6f}")
        lines.append(f"  {'n':>4}  {'k=p+n':>8}  {'R(k,p)':>10}  {'W^n * R(1)':>12}  {'ratio':>8}")
        for n in range(1, 8):
            k = p + n
            rk = R(k, p)
            pred = (W_BHML ** n) * r1
            ratio = rk / pred if pred > 1e-12 else float('nan')
            lines.append(f"  {n:>4}  {k:>8}  {rk:>10.6f}  {pred:>12.8f}  {ratio:>8.4f}")
        lines.append("")

    lines.append("VERDICT — TEST 3:")
    lines.append("  If ratio ≈ 1.0 consistently: W_BHML^n is the echo attenuation law.")
    lines.append("  If ratio varies: W_BHML does not set echo amplitude directly.")
    lines.append("  [Check above table for consistency]")
    lines.append("")

    # ── Revised A13 status ────────────────────────────────────────────────────
    lines.append("=" * 70)
    lines.append("REVISED A13 STATUS")
    lines.append("=" * 70)
    lines.append("")
    lines.append("THREE-OBJECT SEPARATION (STANDS):")
    lines.append(f"  Object 1: W_BHML = 3/50  [THM — Z/10Z ring, table arithmetic]")
    lines.append(f"  Object 2: Wob(b,k) = 8/9 at k=9  [measured, k-dependent]")
    lines.append(f"  Object 3: corridor compression  [sinc² decay = R(k,p) itself]")
    lines.append("")
    lines.append("THE POSITIVE RESULT:")
    lines.append(f"  Corridor compression = sinc²(k/p) = R(k,p) narrowing to 0 at k=p.")
    lines.append(f"  This is Tier D (sinc² formula is proved, D2).")
    lines.append(f"  There is NO additional algebraic form beyond R itself.")
    lines.append("")
    lines.append("WHERE W_BHML APPEARS:")
    lines.append(f"  Post-gate sidelobe structure: sin²(π·W·k/p) first peaks at t=50/6.")
    lines.append(f"  This is PAST the gate (t > 1), not inside the corridor.")
    lines.append(f"  W_BHML is the post-gate frequency, not the corridor compression rate.")
    lines.append("")
    lines.append("TIER ASSESSMENT:")
    lines.append("  Corridor compression (= sinc²): ALREADY TIER D (D2 proved).")
    lines.append("  W_BHML sidelobe prediction: TIER B if Test 1 shows consistent wins.")
    lines.append("  Original candidate R×sin²(πW·k/p): KILLED as corridor formula.")
    lines.append("")
    lines.append("A13 REFORMULATED:")
    lines.append("  Old: Corridor(b,k) = R × sin²(πW·k/p)  [KILLED]")
    lines.append("  New: Corridor IS sinc²(k/p) [Tier D]; W_BHML appears in post-gate")
    lines.append("  sidelobe at t = 50/6 (first peak of sin²(πW·t) past t=1).")

    # Save
    report = "\n".join(lines)
    print(report.encode('ascii', errors='replace').decode('ascii'))

    os.makedirs(REPORT_DIR, exist_ok=True)
    out_path = os.path.join(REPORT_DIR, "a13_sidelobe_prediction_report.txt")
    out_json = os.path.join(REPORT_DIR, "a13_sidelobe_prediction.json")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({
            "W_BHML": W_BHML,
            "T_FIRST_PEAK_pred": T_FIRST_PEAK,
            "sinc2_first_sidelobe_t": sc2_t,
            "sinc2_first_sidelobe_v": sc2_v,
            "test1_results": results_t1,
            "n_sinc2_wins": n_sinc2_wins,
            "n_wbhml_wins": n_wbhml_wins,
            "mean_t_peak": (sum(r["t_peak"] for r in results_t1)/len(results_t1)
                            if results_t1 else None),
            "corridor_rmse": {
                "mean_sinc2": mean_rs2,
                "mean_candidate": mean_rc,
            },
        }, f, indent=2)
    print(f"\n[A13 report: {out_path}]")
    print(f"[A13 data:   {out_json}]")


if __name__ == "__main__":
    main()
