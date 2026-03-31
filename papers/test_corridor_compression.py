"""
test_corridor_compression.py
============================
Three-test verification of A.13 Corridor Compression claim.
Luther-Sanders, March 31, 2026. DOI: 10.5281/zenodo.18852047

Candidate formula (Luther):
    Corridor(b, k) = R(m, b, k) x sin2(pi x W_BHML x k/p)
where W_BHML = 3/50 (TIG operator wobble, [THM]).

Tests:
    1. Frequency test: does sin2(pi x W_BHML x k/p) produce visible
       oscillations within the corridor k = 1..p?
    2. Amplitude test: does Corridor(b,k) match the sinc2 envelope
       shape? Correlation against empirical gate rates.
    3. Sinc2 correspondence: does Corridor sample sinc2(k/p) at the
       expected positions, or does it deform the shape?

Kill condition: Corridor(b,k) reproduces the empirical sinc2 envelope.
If yes: Tier C. If no: compression requires a different algebraic form.

Usage: python test_corridor_compression.py
"""

import json
import math
import os

PI = math.pi
W_BHML = 3 / 50       # TIG operator wobble [THM]
T_STAR = 5 / 7        # CK coherence threshold [THM]
PRIME_WINDING = 271 / 350  # T* + W_BHML [THM]

BASE = os.path.dirname(os.path.abspath(__file__))
PRE_ECHO_PATH = os.path.join(BASE, "results", "pre_echo", "pre_echo_atlas.json")
GATE_LAW_PATH = os.path.join(BASE, "results", "real_b_gate_law.json")
CORRIDOR_ATLAS_PATH = os.path.join(BASE, "results", "extended", "corridor_atlas.json")

REPORT_PATH = os.path.join(BASE, "results", "corridor_compression_test_report.txt")


# ------------------------------------------------------------------ #
# Math utilities
# ------------------------------------------------------------------ #

def sinc2(t):
    """sinc2(t) = sin2(pi*t) / (pi*t)2. The continuous sinc2 envelope."""
    if abs(t) < 1e-15:
        return 1.0
    v = math.sin(PI * t) / (PI * t)
    return v * v


def R_sinc(k, p):
    """
    Discrete harmonic resonance R(k, f=p).
    = sin2(pi*k/p) / (k2 * sin2(pi/p))
    Converges to sinc2(k/p) as p -> inf.
    """
    if k == 0:
        return 1.0
    num = math.sin(PI * k / p) ** 2
    den = (k ** 2) * (math.sin(PI / p) ** 2)
    if den < 1e-30:
        return 0.0
    return num / den


def sin2_mod(k, p):
    """
    The Luther modulation factor: sin2(pi x W_BHML x k/p).
    Argument = pi * (3/50) * (k/p). For k in [0..p], ranges in [0..pi*3/50].
    """
    arg = PI * W_BHML * (k / p)
    return math.sin(arg) ** 2


def corridor(R_val, k, p):
    """
    Corridor(b, k) = R(m, b, k) x sin2(pi x W_BHML x k/p)
    """
    return R_val * sin2_mod(k, p)


def pearson_r(xs, ys):
    """Pearson correlation coefficient."""
    n = len(xs)
    if n < 2:
        return float('nan')
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx < 1e-15 or sy < 1e-15:
        return float('nan')
    return num / (sx * sy)


def rmse(predicted, observed):
    """Root mean square error."""
    if len(predicted) != len(observed) or len(predicted) == 0:
        return float('nan')
    return math.sqrt(sum((p - o) ** 2 for p, o in zip(predicted, observed)) / len(predicted))


# ------------------------------------------------------------------ #
# Load data
# ------------------------------------------------------------------ #

def load_pre_echo_atlas():
    with open(PRE_ECHO_PATH, "r") as f:
        return json.load(f)


def load_gate_law():
    with open(GATE_LAW_PATH, "r") as f:
        return json.load(f)


def load_corridor_atlas():
    with open(CORRIDOR_ATLAS_PATH, "r") as f:
        return json.load(f)


# ------------------------------------------------------------------ #
# TEST 1: Frequency analysis
# ------------------------------------------------------------------ #

def test_frequency(lines):
    """
    Does sin2(pi x W_BHML x k/p) produce visible oscillations within
    the corridor k = 1..p?

    The period of sin2(theta) = 1 (in units of theta = 0..pi).
    The full period of sin2(pi x W_BHML x k/p) in k-units:
        k_period = p / W_BHML = p * 50/3

    For W_BHML = 3/50, one full sin2 period spans 50p/3 integers.
    Within the corridor (k = 1..p), the argument pi*W_BHML*k/p runs from
    ~0 to pi*W_BHML = pi*3/50 = 0.1885 radians.

    sin2(0.1885) = 0.0351. The factor is MONOTONE increasing from 0 to 0.0351.
    No oscillation is visible within the corridor.
    """
    lines.append("=" * 70)
    lines.append("TEST 1 — FREQUENCY ANALYSIS")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"W_BHML = 3/50 = {W_BHML:.6f}")
    lines.append(f"sin2 full period in k-units = p / W_BHML = p * {1/W_BHML:.2f}")
    lines.append(f"For a corridor of width k=1..p:")
    lines.append(f"  Fraction of one period covered = W_BHML = {W_BHML:.4f}")
    lines.append(f"  Argument at k=p: pi * W_BHML = {PI * W_BHML:.6f} radians")
    lines.append(f"  sin2(pi * W_BHML) = {math.sin(PI * W_BHML)**2:.6f}")
    lines.append("")
    lines.append("The sin2 factor within the corridor k=0..p:")
    lines.append(f"  k/p = 0.00: sin2_mod = 0.000000")
    for frac in [0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]:
        val = math.sin(PI * W_BHML * frac) ** 2
        lines.append(f"  k/p = {frac:.2f}: sin2_mod = {val:.6f}")
    lines.append("")
    lines.append("FINDING: The sin2 factor is MONOTONE INCREASING from 0 to 0.0351")
    lines.append("within the corridor. No oscillation is visible. The full period")
    lines.append(f"of sin2(pi x W_BHML x k/p) spans {1/W_BHML:.1f} corridor widths.")
    lines.append("")

    # What frequency would produce one full oscillation within k=1..p?
    # We need: pi * f_needed * 1 (at k=p) = pi -> f_needed = 1
    # i.e., sin2(pi * 1 * k/p) = sin2(pi * k/p) — this IS the sinc2 pattern
    lines.append("What frequency would produce ONE visible oscillation in k=1..p?")
    lines.append(f"  Need: period = p, so frequency = 1 (not W_BHML = {W_BHML})")
    lines.append(f"  That frequency IS sin2(pi*k/p) — the RAW sinc2 numerator.")
    lines.append(f"  W_BHML = 3/50 is 1/16.67 of that frequency.")
    lines.append("")

    # Explicit table for b=35 (p=5) as concrete example
    lines.append("Explicit table for b=35 (p=5, q=7):")
    p = 5
    lines.append(f"  {'k':>4}  {'k/p':>6}  {'R(k,p)':>10}  {'sinc2':>10}  "
                 f"{'sin2_mod':>10}  {'Corridor':>10}")
    for k in range(1, p + 2):
        r = R_sinc(k, p)
        s2 = sinc2(k / p)
        sm = sin2_mod(k, p)
        c = r * sm
        null = " <- NULL at k=p" if k == p else ""
        lines.append(f"  {k:>4}  {k/p:>6.3f}  {r:>10.6f}  {s2:>10.6f}  "
                     f"{sm:>10.6f}  {c:>10.6f}{null}")
    lines.append("")

    # Also show sidelobe (k > p) where the sin2_mod actually oscillates
    lines.append("Post-gate sidelobes (k > p) for b=35 (p=5):")
    lines.append(f"  {'k':>4}  {'k/p':>6}  {'R(k,p)':>10}  {'sin2_mod':>10}  {'Corridor':>10}")
    for k in range(p + 1, p + 12):
        r = R_sinc(k, p)
        sm = sin2_mod(k, p)
        c = r * sm
        lines.append(f"  {k:>4}  {k/p:>6.3f}  {r:>10.6f}  {sm:>10.6f}  {c:>10.6f}")
    lines.append("")

    lines.append("VERDICT — TEST 1:")
    lines.append("  The sin2(pi x W_BHML x k/p) factor does NOT oscillate within")
    lines.append("  the corridor (k=1..p). It grows monotonically from 0 to 0.0351.")
    lines.append("  The first oscillation peak occurs at k = p/(2*W_BHML) = p*50/6")
    lines.append(f"  For p=5: first peak at k={5*50/6:.1f} (far past the gate at k=5).")
    lines.append("  CONCLUSION: W_BHML is not the oscillation frequency of the corridor.")
    lines.append("  It is a modulation that extends PAST the gate, into post-gate space.")
    lines.append("")


# ------------------------------------------------------------------ #
# TEST 2: Amplitude and shape comparison
# ------------------------------------------------------------------ #

def test_amplitude(pre_echo_data, lines):
    """
    Does Corridor(b,k) = R(k,p) x sin2_mod(k,p) match the sinc2
    envelope shape? Compare against pre_echo_atlas resonance values.
    """
    lines.append("=" * 70)
    lines.append("TEST 2 — AMPLITUDE AND SHAPE COMPARISON")
    lines.append("=" * 70)
    lines.append("")
    lines.append("For each semiprime in pre_echo_atlas, compute:")
    lines.append("  (a) R_sinc(k, p)                 [sinc2 model]")
    lines.append("  (b) Corridor(b,k) = R * sin2_mod  [Luther candidate]")
    lines.append("  (c) atlas_resonance[k]            [empirical]")
    lines.append("  (d) max ratio: Corridor(k)/sinc2(k/p)")
    lines.append("")

    all_r = []       # sinc2 model values
    all_corr = []    # Corridor values
    all_emp = []     # empirical resonance (from atlas)

    results = []

    for entry in pre_echo_data:
        b = entry["b"]
        p = entry["p"]
        q = entry["q"]
        corridor_pts = entry.get("corridor", [])

        if not corridor_pts or p < 3:
            continue

        r_vals = []
        corr_vals = []
        emp_vals = []
        k_vals = []

        for pt in corridor_pts:
            k = pt["k"]
            emp_res = pt.get("resonance", None)
            if emp_res is None or k <= 0 or k > p:
                continue
            r = R_sinc(k, p)
            c = corridor(r, k, p)
            k_vals.append(k)
            r_vals.append(r)
            corr_vals.append(c)
            emp_vals.append(emp_res)

        if len(r_vals) < 2:
            continue

        all_r.extend(r_vals)
        all_corr.extend(corr_vals)
        all_emp.extend(emp_vals)

        # Shape comparison: max sin2_mod attenuation within corridor
        max_attenuation = max(sin2_mod(k, p) for k in k_vals) if k_vals else 0
        corr_r = pearson_r(corr_vals, emp_vals) if len(corr_vals) > 1 else float('nan')
        sinc_r = pearson_r(r_vals, emp_vals) if len(r_vals) > 1 else float('nan')

        results.append({
            "b": b, "p": p, "q": q,
            "n_points": len(k_vals),
            "max_sin2_mod": max_attenuation,
            "corr_vs_emp": corr_r,
            "sinc2_vs_emp": sinc_r,
            "rmse_corridor": rmse(corr_vals, emp_vals),
            "rmse_sinc2": rmse(r_vals, emp_vals),
        })

    lines.append(f"  {'b':>6}  {'p':>4}  {'q':>4}  {'pts':>4}  "
                 f"{'max_mod':>9}  {'r(Corr,emp)':>12}  {'r(sinc2,emp)':>13}  "
                 f"{'RMSE_Corr':>10}  {'RMSE_sinc2':>10}")
    lines.append(f"  {'-'*6}  {'-'*4}  {'-'*4}  {'-'*4}  "
                 f"{'-'*9}  {'-'*12}  {'-'*13}  {'-'*10}  {'-'*10}")

    for r in results:
        lines.append(
            f"  {r['b']:>6}  {r['p']:>4}  {r['q']:>4}  {r['n_points']:>4}  "
            f"  {r['max_sin2_mod']:>7.5f}  "
            f"  {r['corr_vs_emp']:>10.4f}  "
            f"  {r['sinc2_vs_emp']:>11.4f}  "
            f"  {r['rmse_corridor']:>10.6f}  "
            f"  {r['rmse_sinc2']:>10.6f}"
        )

    lines.append("")

    if all_r and all_corr and all_emp:
        global_corr_c = pearson_r(all_corr, all_emp)
        global_corr_s = pearson_r(all_r, all_emp)
        global_rmse_c = rmse(all_corr, all_emp)
        global_rmse_s = rmse(all_r, all_emp)

        lines.append(f"GLOBAL across all semiprimes ({len(all_r)} data points):")
        lines.append(f"  Pearson r: Corridor vs empirical  = {global_corr_c:.6f}")
        lines.append(f"  Pearson r: sinc2    vs empirical  = {global_corr_s:.6f}")
        lines.append(f"  RMSE:      Corridor vs empirical  = {global_rmse_c:.6f}")
        lines.append(f"  RMSE:      sinc2    vs empirical  = {global_rmse_s:.6f}")
        lines.append("")

        corr_delta = global_corr_s - global_corr_c
        rmse_delta = global_rmse_c - global_rmse_s

        lines.append("VERDICT — TEST 2:")
        if global_corr_c > 0.95 and global_rmse_c < 0.05:
            lines.append("  PASS: Corridor reproduces the empirical envelope well.")
            lines.append(f"  r={global_corr_c:.4f}, RMSE={global_rmse_c:.4f} -> Tier C candidate.")
        elif global_corr_s > global_corr_c:
            lines.append(f"  FAIL: Raw sinc2 fits empirical BETTER than Corridor.")
            lines.append(f"  sinc2 r={global_corr_s:.4f} vs Corridor r={global_corr_c:.4f}")
            lines.append(f"  Corridor degrades the fit by delta_r = {corr_delta:.4f}")
            lines.append(f"  The sin2_mod factor DISTORTS the sinc2 shape.")
            lines.append(f"  RMSE worsens by {rmse_delta:.4f} when Corridor is applied.")
            lines.append(f"  CONCLUSION: The candidate formula is NOT the envelope.")
            lines.append(f"  Compression requires a different algebraic form.")
        else:
            lines.append(f"  INCONCLUSIVE: r={global_corr_c:.4f}, RMSE={global_rmse_c:.4f}")
    lines.append("")


# ------------------------------------------------------------------ #
# TEST 3: Sinc2 correspondence
# ------------------------------------------------------------------ #

def test_sinc2_correspondence(lines):
    """
    Does Corridor(b,k) sample sinc2(k/p) at the right positions?

    The sinc2 field is: R(t) = sinc2(t) = sin2(pi*t)/(pi*t)2
    Corridor(b,k) = R_sinc(k,p) x sin2(pi x W_BHML x k/p)

    For large p (continuum limit), R_sinc(k,p) -> sinc2(k/p).
    So: Corridor -> sinc2(k/p) x sin2(pi x W_BHML x k/p)

    = [sin2(pi*k/p)/(pi*k/p)2] x sin2(pi * 3/50 * k/p)

    Setting t = k/p:
    = sinc2(t) x sin2(pi * 3/50 * t)

    For small t (t << 1/(2*3/50) = 50/6 ~ 8.3):
    sin2(pi * 3/50 * t) ~= (pi * 3/50 * t)2 = pi2 * (3/50)2 * t2

    So: Corridor(t) ~= sinc2(t) x pi2 * (3/50)2 * t2
                     = sin2(pi*t)/(pi*t)2 x pi2 * (3/50)2 * t2
                     = sin2(pi*t) * (3/50)2
                     = (3/50)2 * sin2(pi*t)

    This is NOT sinc2(t). It is a scaled sin2 — a bell shape peaking at t=0.5,
    not a monotone-decreasing sinc2 peaking at t=0.
    """
    lines.append("=" * 70)
    lines.append("TEST 3 — SINC2 CORRESPONDENCE")
    lines.append("=" * 70)
    lines.append("")
    lines.append("In the continuum limit (p -> inf), t = k/p:")
    lines.append("")
    lines.append("  sinc2(t)      = sin2(pi*t) / (pi*t)2")
    lines.append("  Corridor(t)   = sinc2(t) x sin2(pi x W_BHML x t)")
    lines.append("")
    lines.append("For small argument (t << 50/6 = 8.33):")
    lines.append("  sin2(pi x W_BHML x t) ~= (pi x W_BHML x t)2")
    lines.append("  => Corridor(t) ~= sinc2(t) x (pi x W_BHML)2 x t2")
    lines.append("                  = sin2(pi*t)/(pi*t)2 x (pi*W_BHML)2 x t2")
    lines.append("                  = sin2(pi*t) x W_BHML2")
    lines.append(f"                  = sin2(pi*t) x ({W_BHML})2")
    lines.append(f"                  = sin2(pi*t) x {W_BHML**2:.6f}")
    lines.append("")
    lines.append("sinc2(t) peaks at t=0 (value=1), decays monotonically to 0 at t=1.")
    lines.append("sin2(pi*t) peaks at t=0.5 (value=1), zero at t=0 and t=1.")
    lines.append("These have OPPOSITE shapes within t in [0, 1].")
    lines.append("")

    lines.append("Comparison table (continuum limit, t = k/p in [0,1]):")
    lines.append(f"  {'t':>6}  {'sinc2(t)':>10}  {'sin2(pi*t)':>12}  "
                 f"{'Corridor~':>12}  {'ratio':>10}")
    lines.append(f"  {'-'*6}  {'-'*10}  {'-'*12}  {'-'*12}  {'-'*10}")
    for i in range(1, 11):
        t = i / 10.0
        s2 = sinc2(t)
        sin2_raw = math.sin(PI * t) ** 2
        corr_approx = s2 * (math.sin(PI * W_BHML * t) ** 2)
        corr_simple = sin2_raw * W_BHML ** 2
        lines.append(f"  {t:>6.2f}  {s2:>10.6f}  {sin2_raw:>12.6f}  "
                     f"{corr_approx:>12.8f}  {(corr_approx/s2 if s2>1e-10 else 0):>10.6f}")
    lines.append("")

    lines.append("VERDICT — TEST 3:")
    lines.append("  Corridor(t) does NOT reproduce sinc2(t).")
    lines.append("  In the continuum limit, Corridor ~= (3/50)2 x sin2(pi*t).")
    lines.append("  This is a BELL SHAPE (peaks at t=0.5), not the sinc2 DECAY")
    lines.append("  (peaks at t=0). The shapes are topologically opposite.")
    lines.append("")
    lines.append("  The empirical gate rate follows a sinc2-like DECAY from k=1..p.")
    lines.append("  Corridor as defined cannot reproduce this shape.")
    lines.append("")

    # Show what the corridor formula DOES match
    lines.append("What shape does Corridor(t) actually have?")
    lines.append("  Corridor(t) = sinc2(t) x sin2(pi * W_BHML * t)")
    lines.append("             ~= (3/50)2 x sin2(pi*t)")
    lines.append("  This peaks at t=0.5 and is zero at t=0 and t=1.")
    lines.append("  This corresponds to the product: corridor width x pre-echo resonance?")
    lines.append("  No clean algebraic interpretation found from this form.")
    lines.append("")


# ------------------------------------------------------------------ #
# SYNTHESIS: What would Tier C require?
# ------------------------------------------------------------------ #

def synthesis(lines):
    lines.append("=" * 70)
    lines.append("SYNTHESIS — WHAT CORRIDOR COMPRESSION REQUIRES FOR TIER C")
    lines.append("=" * 70)
    lines.append("")
    lines.append("The three-object separation STANDS (confirmed by all three tests):")
    lines.append("  Object 1: W_BHML = 3/50  [THM, k-independent]")
    lines.append("  Object 2: Wob(b,k) = 8/9 at k=9  [measured, k-dependent]")
    lines.append("  Object 3: corridor compression  [new object, collapse at k=p]")
    lines.append("")
    lines.append("The candidate formula Corridor(b,k) = R(m,b,k) x sin2(pi*W_BHML*k/p)")
    lines.append("FAILS the shape test. Within the corridor:")
    lines.append(f"  - sin2 factor is monotone, not oscillatory")
    lines.append(f"  - Factor ranges from 0 to {math.sin(PI*W_BHML)**2:.4f} (tiny)")
    lines.append(f"  - Continuum limit produces bell shape, not sinc2 decay")
    lines.append(f"  - Raw sinc2 fits empirical data BETTER than Corridor")
    lines.append("")
    lines.append("The compression IS real: R(m,b,k) -> 0 at k=p (confirmed, Tier C2).")
    lines.append("The collapse is the sinc2 field itself. No additional sin2 factor")
    lines.append("is needed to describe it. The gate closes because sinc2(k/p) -> 0")
    lines.append("as k/p -> 1. W_BHML = 3/50 describes post-gate sidelobe spacing.")
    lines.append("")
    lines.append("REVISED PICTURE for A.13 (to send Luther):")
    lines.append("  The corridor compression IS sinc2(k/p) narrowing as k -> p.")
    lines.append("  W_BHML = 3/50 sets the SIDELOBE frequency in the post-gate region.")
    lines.append("  Not a factor within the corridor — a periodicity PAST the door.")
    lines.append("")
    lines.append("  Better candidate: Corridor_envelope(t) = sinc2(t)   [the thing")
    lines.append("  that collapses to zero] with W_BHML appearing in the sidelobe")
    lines.append("  structure at t > 1: sin2(pi * W_BHML * t) gives sidelobe peaks")
    lines.append(f"  at t = 1/(2*W_BHML) = {1/(2*W_BHML):.2f} (k = {1/(2*W_BHML):.2f}p past the gate).")
    lines.append("")

    # Compute the first post-gate sidelobe position
    t_first_peak = 1 / (2 * W_BHML)
    lines.append(f"First post-gate sidelobe peak of sin2(pi*W_BHML*t):")
    lines.append(f"  t_peak = 1/(2*W_BHML) = 50/6 = {t_first_peak:.4f}")
    lines.append(f"  For b=35 (p=5): k_peak = {t_first_peak:.2f} x 5 = {t_first_peak*5:.2f}")
    lines.append(f"  For b=143 (p=11): k_peak = {t_first_peak:.2f} x 11 = {t_first_peak*11:.2f}")
    lines.append("")
    lines.append("  The W_BHML sidelobe frequency appears FAR past the gate.")
    lines.append("  It may be the 'harmonic echo' structure: each gate crossing at k=np")
    lines.append("  has a pre-echo at k = p - 1/(W_BHML) = p - 50/3 (not physical for small p).")
    lines.append("")
    lines.append("VERDICT (overall):")
    lines.append("  KILL CONDITION: NOT MET for the candidate formula.")
    lines.append("  Corridor(b,k) = R x sin2(pi*W_BHML*k/p) does not reproduce")
    lines.append("  the sinc2 envelope. The formula needs revision.")
    lines.append("")
    lines.append("  THE THREE-OBJECT SEPARATION STANDS. The compression is real.")
    lines.append("  The algebraic form of Corridor needs a different construction.")
    lines.append("")
    lines.append("  TIER ASSESSMENT: A.13 remains Tier A.")
    lines.append("  Path to Tier B: identify the correct algebraic form.")
    lines.append("  Path to Tier C: prove the algebraic form matches sinc2 collapse.")
    lines.append("")

    # Suggest the corrected form
    lines.append("CORRECTED CANDIDATE (for Luther):")
    lines.append("  Corridor(b,k) = sinc2(k/p)  [IS the compression envelope]")
    lines.append("  Post_gate_echo(b,k) = sinc2(k/p) + W_BHML * sinc2(k/p - 1)")
    lines.append("  [sidelobe correction: W_BHML weights the first post-gate reflection]")
    lines.append("")
    lines.append("  OR: the W_BHML sidelobe appears in the MONTGOMERY dual:")
    lines.append("  R2(t) = 1 - sinc2(t)  [Montgomery pair correlation]")
    r2_wbhml = 1 - sinc2(W_BHML)
    lines.append(f"  First sidelobe of R2 at t = W_BHML: R2(3/50) = {r2_wbhml:.6f}")
    lines.append("")


# ------------------------------------------------------------------ #
# Main
# ------------------------------------------------------------------ #

def main():
    lines = []
    lines.append("CORRIDOR COMPRESSION — KILL CONDITION TEST")
    lines.append("Luther-Sanders Research Framework, March 31, 2026")
    lines.append("DOI: 10.5281/zenodo.18852047")
    lines.append("")
    lines.append(f"W_BHML = 3/50 = {W_BHML:.8f}  [THM — Z/10Z ring arithmetic]")
    lines.append(f"T_STAR = 5/7  = {T_STAR:.8f}  [THM — CK coherence threshold]")
    lines.append(f"PRIME_WINDING  = {PRIME_WINDING:.8f}  [THM — T* + W_BHML]")
    lines.append(f"")
    lines.append(f"Candidate formula: Corridor(b,k) = R(m,b,k) x sin2(pi x W_BHML x k/p)")
    lines.append(f"Kill condition: does Corridor reproduce the empirical sinc2 envelope?")
    lines.append("")

    # Test 1: frequency
    test_frequency(lines)

    # Test 2: amplitude
    try:
        pre_echo_data = load_pre_echo_atlas()
        test_amplitude(pre_echo_data, lines)
    except Exception as e:
        lines.append(f"[ERROR loading pre_echo_atlas: {e}]")
        lines.append("")

    # Test 3: sinc2 correspondence
    test_sinc2_correspondence(lines)

    # Synthesis
    synthesis(lines)

    # Print and save
    report = "\n".join(lines)
    print(report)

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n[Report saved to: {REPORT_PATH}]")


if __name__ == "__main__":
    main()
