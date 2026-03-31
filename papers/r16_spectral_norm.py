"""
r16_spectral_norm.py — Spectral normalization: do p and q show meaningful resonance?
Author: Brayden Sanders / 7Site LLC

HYPOTHESIS TO TEST:
  The dominant frequency in R(k, f) for all k in the pre-echo zone is always the
  largest prime in the frequency list — this is a geometric artifact because
  R(k,f) = sin²(πk/f) / (k² sin²(π/f)), and for large f, sin²(π/f) → (π/f)² → 0,
  so R grows trivially with f regardless of algebraic structure.

FOUR NORMALIZED TESTS:
  1. Relative drop rate: R(1,f) → R(p-1,f) normalized against a neutral prime baseline
  2. Residual after baseline subtraction: R(k,p) and R(k,q) vs smooth large-prime curve
  3. Phase coherence at k=p-1: is R(p-1,p) = 1/(p-1)² unusually low vs neutral primes?
  4. Spectral contrast: rank of p and q among all freqs through k=1..p+q

OUTPUT: results/spectral_norm/ — JSON data + plots + conclusions
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import math
import json
import numpy as np
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import UnivariateSpline

OUT = Path("results/spectral_norm")
OUT.mkdir(parents=True, exist_ok=True)

# ── Helpers ────────────────────────────────────────────────────────────────────

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def primes_up_to(n):
    return [x for x in range(2, n+1) if is_prime(x)]

def next_prime(n):
    x = n + 1
    while not is_prime(x):
        x += 1
    return x

def harmonic_resonance(k, f):
    """Closed form: R(k,f) = sin²(πk/f) / (k² sin²(π/f))"""
    denom_sin = math.sin(math.pi / f)
    if abs(denom_sin) < 1e-15:
        return 0.0
    num = math.sin(math.pi * k / f)
    return (num * num) / (k * k * denom_sin * denom_sin)

# ── Test worlds: (b, p, q) semiprimes ─────────────────────────────────────────
WORLDS = [
    (15,  3,  5),
    (35,  5,  7),
    (77,  7, 11),
    (143, 11, 13),
    (323, 17, 19),
    (667, 23, 29),
    (899, 29, 31),
    (1763, 41, 43),
    (2021, 43, 47),
    (3127, 53, 59),
]

# Neutral primes: primes far from p and q used as baseline reference
# For each world we'll pick primes in the "spectral neighborhood" minus p, q
def get_neutral_primes(p, q, n_below=4, n_above=6):
    """Return primes near q that are NOT p or q."""
    candidates = []
    # Below p
    x = p - 1
    count = 0
    while count < n_below and x >= 2:
        if is_prime(x) and x != p and x != q:
            candidates.append(x)
            count += 1
        x -= 1
    # Above q
    x = q + 1
    count = 0
    while count < n_above:
        if is_prime(x) and x != p and x != q:
            candidates.append(x)
            count += 1
        x += 1
    return sorted(candidates)


print("=" * 72)
print("r16_spectral_norm.py — Spectral normalization analysis")
print("=" * 72)
print(f"Testing {len(WORLDS)} semiprime worlds")
print(f"Output: {OUT.absolute()}")
print()

all_results = []

for world_idx, (b, p, q) in enumerate(WORLDS):
    print(f"\n{'='*72}")
    print(f"WORLD {world_idx+1}: b={b}  (p={p}, q={q})")
    print(f"{'='*72}")

    neutrals = get_neutral_primes(p, q)
    all_freqs = sorted(set([p, q] + neutrals))
    k_max = p + q
    k_range = list(range(1, k_max + 1))

    print(f"  Freqs tested: {all_freqs}")
    print(f"  k range: 1..{k_max}")
    print(f"  Neutral primes: {neutrals}")
    print()

    # ── Build R(k, f) matrix ───────────────────────────────────────────────────
    R = {}  # R[k][f]
    for k in k_range:
        R[k] = {f: harmonic_resonance(k, f) for f in all_freqs}

    # ══════════════════════════════════════════════════════════════════════════
    # TEST 1: Relative drop rate
    # For each freq f: compute the ratio R(p-1, f) / R(1, f)
    # A freq that "supports" the pre-echo zone should drop MORE (smaller ratio)
    # than a neutral freq of similar size.
    # ══════════════════════════════════════════════════════════════════════════
    print("  TEST 1: Relative drop rate R(p-1, f) / R(1, f)")
    print(f"  {'freq':>6}  {'R(1,f)':>9}  {'R(p-1,f)':>10}  {'ratio':>8}  {'label':>8}")

    drop_rates = {}
    for f in all_freqs:
        r1 = R[1][f]
        rpm1 = R[p-1][f]
        ratio = rpm1 / r1 if r1 > 1e-15 else float('inf')
        drop_rates[f] = ratio
        label = "p" if f == p else ("q" if f == q else "neutral")
        print(f"  {f:>6}  {r1:>9.5f}  {rpm1:>10.6f}  {ratio:>8.5f}  {label:>8}")

    # Baseline: mean ratio for neutral primes close in size to p
    neutral_ratios = [drop_rates[f] for f in neutrals]
    baseline_mean = np.mean(neutral_ratios)
    baseline_std  = np.std(neutral_ratios) if len(neutral_ratios) > 1 else 0.0
    ratio_p = drop_rates[p]
    ratio_q = drop_rates.get(q, None)

    z_p_t1 = (ratio_p - baseline_mean) / (baseline_std + 1e-10)
    z_q_t1 = ((ratio_q - baseline_mean) / (baseline_std + 1e-10)) if ratio_q is not None else None

    print(f"  Neutral baseline: mean={baseline_mean:.5f}  std={baseline_std:.5f}")
    print(f"  p({p}) z-score: {z_p_t1:+.3f}  {'** DISTINCTIVE' if abs(z_p_t1) > 1.5 else '(ordinary)'}")
    if z_q_t1 is not None:
        print(f"  q({q}) z-score: {z_q_t1:+.3f}  {'** DISTINCTIVE' if abs(z_q_t1) > 1.5 else '(ordinary)'}")

    # ══════════════════════════════════════════════════════════════════════════
    # TEST 2: Residual after baseline subtraction
    # For each k in pre-echo zone (k=1..p-1), fit a polynomial in f over
    # neutral primes, then check if R(k, p) and R(k, q) deviate from fit.
    # ══════════════════════════════════════════════════════════════════════════
    print(f"\n  TEST 2: Residual after baseline — k=1..{p-1}")
    print(f"  {'k':>4}  {'baseline_p':>12}  {'R(k,p)':>9}  {'resid_p':>9}  "
          f"{'baseline_q':>12}  {'R(k,q)':>9}  {'resid_q':>9}")

    test2_rows = []
    for k in range(1, p):
        # Fit: for neutral primes, R(k, f) as fn of f
        x_pts = np.array([float(f) for f in neutrals])
        y_pts = np.array([R[k][f] for f in neutrals])

        # Use log(f) → log(R) linear fit (captures 1/f² structure)
        if np.all(y_pts > 0) and len(x_pts) >= 2:
            log_x = np.log(x_pts)
            log_y = np.log(y_pts)
            coeffs = np.polyfit(log_x, log_y, 1)
            slope, intercept = coeffs
            baseline_p = math.exp(intercept) * (p ** slope)
            baseline_q = math.exp(intercept) * (q ** slope)
        else:
            # Linear fallback
            coeffs = np.polyfit(x_pts, y_pts, 1)
            baseline_p = np.polyval(coeffs, p)
            baseline_q = np.polyval(coeffs, q)

        resid_p = R[k][p] - baseline_p
        resid_q = R[k][q] - baseline_q if q in R[k] else None

        print(f"  {k:>4}  {baseline_p:>12.6f}  {R[k][p]:>9.6f}  {resid_p:>+9.6f}  "
              f"{baseline_q:>12.6f}  {R[k].get(q, 0):>9.6f}  "
              f"{resid_q:>+9.6f}" if resid_q is not None else
              f"  {k:>4}  {baseline_p:>12.6f}  {R[k][p]:>9.6f}  {resid_p:>+9.6f}  "
              f"{'n/a':>12}  {'n/a':>9}  {'n/a':>9}")

        test2_rows.append({
            "k": k,
            "baseline_p": baseline_p, "R_k_p": R[k][p], "resid_p": resid_p,
            "baseline_q": baseline_q, "R_k_q": R[k].get(q),
            "resid_q": resid_q
        })

    mean_resid_p = np.mean([r["resid_p"] for r in test2_rows])
    mean_resid_q_vals = [r["resid_q"] for r in test2_rows if r["resid_q"] is not None]
    mean_resid_q = np.mean(mean_resid_q_vals) if mean_resid_q_vals else None

    print(f"  Mean residual p({p}): {mean_resid_p:+.6f}  "
          f"{'BELOW baseline (suppressed)' if mean_resid_p < -1e-4 else 'ABOVE baseline' if mean_resid_p > 1e-4 else 'near baseline'}")
    if mean_resid_q is not None:
        print(f"  Mean residual q({q}): {mean_resid_q:+.6f}  "
              f"{'BELOW baseline (suppressed)' if mean_resid_q < -1e-4 else 'ABOVE baseline' if mean_resid_q > 1e-4 else 'near baseline'}")

    # ══════════════════════════════════════════════════════════════════════════
    # TEST 3: Phase coherence at k=p-1
    # R(p-1, p) = 1/(p-1)² — the countdown clock.
    # Compare this to R(p-1, f) for all neutral primes of similar size.
    # ══════════════════════════════════════════════════════════════════════════
    print(f"\n  TEST 3: Phase coherence at k=p-1={p-1}")
    print(f"  {'freq':>6}  {'R(p-1,f)':>12}  {'label':>8}")

    phase_coh = {}
    for f in all_freqs:
        rv = R[p-1][f]
        phase_coh[f] = rv
        label = "p" if f == p else ("q" if f == q else "neutral")
        print(f"  {f:>6}  {rv:>12.8f}  {label:>8}")

    # The countdown value for p
    countdown_p = 1.0 / (p-1)**2
    print(f"  Countdown clock 1/(p-1)² = {countdown_p:.8f}")

    # Rank R(p-1, f): does p land at MINIMUM (as expected from countdown)?
    sorted_by_R = sorted(all_freqs, key=lambda f: phase_coh[f])
    rank_p = sorted_by_R.index(p)  # 0 = lowest R
    rank_q = sorted_by_R.index(q)

    print(f"  Rank of p({p}) at k=p-1 (0=lowest): {rank_p} / {len(all_freqs)-1}  "
          f"{'-> p is MINIMUM (expected)' if rank_p == 0 else '-> NOT minimum'}")
    print(f"  Rank of q({q}) at k=p-1 (0=lowest): {rank_q} / {len(all_freqs)-1}")

    # Neutral primes R at k=p-1 vs p's value
    neutral_phase = [phase_coh[f] for f in neutrals]
    p_phase = phase_coh[p]
    z_p_t3 = (p_phase - np.mean(neutral_phase)) / (np.std(neutral_phase) + 1e-10)
    print(f"  z-score of p's phase coherence vs neutrals: {z_p_t3:+.3f}  "
          f"{'** UNUSUALLY LOW' if z_p_t3 < -1.5 else '** UNUSUALLY HIGH' if z_p_t3 > 1.5 else '(ordinary)'}")

    # ══════════════════════════════════════════════════════════════════════════
    # TEST 4: Spectral contrast — rank trajectory of p and q
    # For each k in 1..p+q, rank all freqs by R(k,f).
    # Track whether p's rank drops to 0 exactly at k=p.
    # ══════════════════════════════════════════════════════════════════════════
    print(f"\n  TEST 4: Spectral contrast — rank of p and q through k=1..{k_max}")
    print(f"  {'k':>4}  {'rank_p':>7}  {'rank_q':>7}  {'dominant_f':>12}  {'artifact?':>10}")

    rank_p_traj = []
    rank_q_traj = []
    dominant_freq_traj = []
    test4_rows = []

    for k in k_range:
        row = R[k]
        sorted_freqs = sorted(all_freqs, key=lambda f: row[f])  # ascending → 0=lowest
        rp = sorted_freqs.index(p)
        rq = sorted_freqs.index(q)
        dominant = sorted_freqs[-1]  # highest R
        is_artifact = is_prime(dominant) and dominant > q  # largest prime wins → artifact

        rank_p_traj.append(rp)
        rank_q_traj.append(rq)
        dominant_freq_traj.append(dominant)

        test4_rows.append({
            "k": k, "rank_p": rp, "rank_q": rq,
            "dominant_f": dominant, "is_artifact": is_artifact
        })

        if k <= p + 5 or k == p or k == q:
            print(f"  {k:>4}  {rp:>7}  {rq:>7}  {dominant:>12}  "
                  f"{'YES' if is_artifact else 'no':>10}")

    # Special check: does p rank drop to 0 AT k=p?
    rank_at_kp = rank_p_traj[p-1]   # k=p → index p-1
    print(f"\n  Rank of p({p}) at k=p:   {rank_at_kp} / {len(all_freqs)-1}  "
          f"{'-> p IS minimum at k=p (structural)' if rank_at_kp == 0 else '-> p NOT minimum at k=p'}")

    # How often is largest prime dominant? (artifact fraction)
    largest_prime_in_list = max(all_freqs)
    artifact_count = sum(1 for r in test4_rows if r["dominant_f"] == largest_prime_in_list)
    artifact_frac = artifact_count / len(test4_rows)
    print(f"  Largest prime ({largest_prime_in_list}) dominant: {artifact_count}/{len(k_range)} "
          f"= {artifact_frac:.1%}  {'-> STRONG ARTIFACT' if artifact_frac > 0.7 else '-> weak artifact'}")

    # ── Aggregate world result ─────────────────────────────────────────────────
    world_result = {
        "b": b, "p": p, "q": q,
        "neutrals": neutrals,
        "all_freqs": all_freqs,
        "test1": {
            "drop_rates": {str(f): drop_rates[f] for f in all_freqs},
            "baseline_mean": baseline_mean,
            "baseline_std": baseline_std,
            "z_p": z_p_t1,
            "z_q": z_q_t1,
            "verdict": "distinctive" if abs(z_p_t1) > 1.5 else "ordinary"
        },
        "test2": {
            "mean_resid_p": mean_resid_p,
            "mean_resid_q": mean_resid_q,
            "rows": test2_rows,
            "verdict_p": ("suppressed" if mean_resid_p < -1e-4
                          else "elevated" if mean_resid_p > 1e-4 else "neutral")
        },
        "test3": {
            "phase_coh": {str(f): phase_coh[f] for f in all_freqs},
            "countdown_p": countdown_p,
            "rank_p_at_pm1": rank_p,
            "rank_q_at_pm1": rank_q,
            "z_p": z_p_t3,
            "verdict": ("minimum_as_expected" if rank_p == 0 else "not_minimum")
        },
        "test4": {
            "rank_p_at_kp": rank_at_kp,
            "artifact_fraction": artifact_frac,
            "rank_p_traj": rank_p_traj,
            "rank_q_traj": rank_q_traj,
            "dominant_freq_traj": dominant_freq_traj,
            "verdict": ("p_min_at_kp" if rank_at_kp == 0 else "p_not_min_at_kp")
        }
    }
    all_results.append(world_result)

# ── Save JSON ──────────────────────────────────────────────────────────────────
with open(OUT / "spectral_norm_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)
print(f"\n\nJSON saved: {OUT / 'spectral_norm_results.json'}")


# ══════════════════════════════════════════════════════════════════════════════
# PLOT: 4-panel figure per world (use first 4 worlds for readability)
# ══════════════════════════════════════════════════════════════════════════════

N_PLOT_WORLDS = min(4, len(WORLDS))

fig = plt.figure(figsize=(20, 5 * N_PLOT_WORLDS))
fig.suptitle("Spectral Normalization: Do p and q Show Meaningful Resonance?\n"
             "R(k,f) = sin²(πk/f) / (k² sin²(π/f))", fontsize=13, y=1.01)

gs = gridspec.GridSpec(N_PLOT_WORLDS, 4, figure=fig, hspace=0.55, wspace=0.35)

for wi, wr in enumerate(all_results[:N_PLOT_WORLDS]):
    b, p, q = wr["b"], wr["p"], wr["q"]
    neutrals = wr["neutrals"]
    all_freqs = wr["all_freqs"]
    k_max = p + q
    k_range = list(range(1, k_max + 1))

    # Rebuild R matrix for plot
    R = {}
    for k in k_range:
        R[k] = {f: harmonic_resonance(k, f) for f in all_freqs}

    # ── Panel 1: Drop rate comparison ─────────────────────────────────────────
    ax1 = fig.add_subplot(gs[wi, 0])
    dr = wr["test1"]["drop_rates"]
    freqs_sorted = sorted(all_freqs)
    colors = ['red' if f == p else 'blue' if f == q else 'gray' for f in freqs_sorted]
    bars = ax1.bar([str(f) for f in freqs_sorted],
                   [dr[str(f)] for f in freqs_sorted], color=colors)
    ax1.axhline(wr["test1"]["baseline_mean"], color='orange', linestyle='--',
                label=f'neutral mean', linewidth=1.5)
    ax1.set_title(f"b={b} (p={p},q={q})\nTest1: Drop Rate R(p-1,f)/R(1,f)", fontsize=9)
    ax1.set_xlabel("freq", fontsize=8)
    ax1.set_ylabel("ratio", fontsize=8)
    ax1.tick_params(labelsize=7)
    # Add z-score annotations
    zp = wr["test1"]["z_p"]
    zq = wr["test1"]["z_q"]
    ax1.text(0.02, 0.95, f"z(p)={zp:+.2f}\nz(q)={zq:+.2f}" if zq else f"z(p)={zp:+.2f}",
             transform=ax1.transAxes, fontsize=7, va='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax1.legend(fontsize=7)

    # ── Panel 2: Residuals through k=1..p-1 ───────────────────────────────────
    ax2 = fig.add_subplot(gs[wi, 1])
    rows2 = wr["test2"]["rows"]
    ks2 = [r["k"] for r in rows2]
    rp_vals = [r["resid_p"] for r in rows2]
    rq_vals = [r["resid_q"] if r["resid_q"] is not None else 0.0 for r in rows2]
    ax2.plot(ks2, rp_vals, 'r-o', markersize=4, label=f"resid(p={p})")
    ax2.plot(ks2, rq_vals, 'b-s', markersize=4, label=f"resid(q={q})")
    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.fill_between(ks2, rp_vals, 0, alpha=0.2, color='red')
    ax2.set_title(f"Test2: Residual vs Neutral Baseline\n(k=1..p-1={p-1})", fontsize=9)
    ax2.set_xlabel("k", fontsize=8)
    ax2.set_ylabel("R(k,f) - baseline(f)", fontsize=8)
    ax2.tick_params(labelsize=7)
    mr_p = wr["test2"]["mean_resid_p"]
    mr_q = wr["test2"]["mean_resid_q"]
    ax2.text(0.02, 0.05,
             f"mean resid p: {mr_p:+.4f}\nmean resid q: {mr_q:+.4f}" if mr_q is not None
             else f"mean resid p: {mr_p:+.4f}",
             transform=ax2.transAxes, fontsize=7, va='bottom',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    ax2.legend(fontsize=7)

    # ── Panel 3: Phase coherence at k=p-1 ─────────────────────────────────────
    ax3 = fig.add_subplot(gs[wi, 2])
    ph = wr["test3"]["phase_coh"]
    freqs_s = sorted(all_freqs)
    ph_vals = [ph[str(f)] for f in freqs_s]
    cols3 = ['red' if f == p else 'blue' if f == q else 'gray' for f in freqs_s]
    ax3.bar([str(f) for f in freqs_s], ph_vals, color=cols3)
    ax3.axhline(wr["test3"]["countdown_p"], color='red', linestyle=':', linewidth=1.5,
                label=f'1/(p-1)²={wr["test3"]["countdown_p"]:.4f}')
    ax3.set_title(f"Test3: Phase Coherence at k=p-1\nRank p={wr['test3']['rank_p_at_pm1']}/0=lowest",
                  fontsize=9)
    ax3.set_xlabel("freq", fontsize=8)
    ax3.set_ylabel(f"R(p-1={p-1}, f)", fontsize=8)
    ax3.tick_params(labelsize=7)
    z3 = wr["test3"]["z_p"]
    ax3.text(0.02, 0.95, f"z(p)={z3:+.2f}\n{wr['test3']['verdict']}",
             transform=ax3.transAxes, fontsize=7, va='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax3.legend(fontsize=7)

    # ── Panel 4: Rank trajectory of p and q ───────────────────────────────────
    ax4 = fig.add_subplot(gs[wi, 3])
    rp_traj = wr["test4"]["rank_p_traj"]
    rq_traj = wr["test4"]["rank_q_traj"]
    n_freqs = len(all_freqs) - 1  # max rank

    ax4.plot(k_range, rp_traj, 'r-', linewidth=1.5, label=f"rank(p={p})")
    ax4.plot(k_range, rq_traj, 'b--', linewidth=1.5, label=f"rank(q={q})")
    ax4.axvline(p, color='red', alpha=0.4, linewidth=1, linestyle=':')
    ax4.axvline(q, color='blue', alpha=0.4, linewidth=1, linestyle=':')
    ax4.axhline(0, color='green', alpha=0.3, linewidth=1)  # minimum rank line

    # Mark k=p point
    if p - 1 < len(rp_traj):
        ax4.plot(p, rp_traj[p-1], 'r*', markersize=10, zorder=5)

    ax4.set_ylim(-0.5, n_freqs + 0.5)
    ax4.set_title(f"Test4: Rank Trajectory (0=lowest R)\nartifact={wr['test4']['artifact_fraction']:.0%}",
                  fontsize=9)
    ax4.set_xlabel("k", fontsize=8)
    ax4.set_ylabel("rank of f among all freqs", fontsize=8)
    ax4.tick_params(labelsize=7)
    rp_kp = wr["test4"]["rank_p_at_kp"]
    ax4.text(0.02, 0.95,
             f"rank(p) at k=p: {rp_kp}\nartifact: {wr['test4']['artifact_fraction']:.0%}",
             transform=ax4.transAxes, fontsize=7, va='top',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    ax4.legend(fontsize=7)

plt.savefig(OUT / "spectral_norm_plot.png", dpi=120, bbox_inches='tight')
print(f"Plot saved: {OUT / 'spectral_norm_plot.png'}")


# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY AND VERDICT
# ══════════════════════════════════════════════════════════════════════════════

print("\n")
print("=" * 72)
print("FINAL VERDICT: Is the spectral horizon a geometric artifact?")
print("=" * 72)

# Tally results across all worlds
t1_distinctive = sum(1 for wr in all_results if abs(wr["test1"]["z_p"]) > 1.5)
t1_ordinary    = len(all_results) - t1_distinctive

t2_suppressed  = sum(1 for wr in all_results if wr["test2"]["verdict_p"] == "suppressed")
t2_elevated    = sum(1 for wr in all_results if wr["test2"]["verdict_p"] == "elevated")
t2_neutral     = len(all_results) - t2_suppressed - t2_elevated

t3_minimum     = sum(1 for wr in all_results if wr["test3"]["verdict"] == "minimum_as_expected")
t3_not_min     = len(all_results) - t3_minimum

t3_low_z       = sum(1 for wr in all_results if wr["test3"]["z_p"] < -1.5)
t3_high_z      = sum(1 for wr in all_results if wr["test3"]["z_p"] > 1.5)

t4_p_min_at_kp = sum(1 for wr in all_results if wr["test4"]["rank_p_at_kp"] == 0)
t4_strong_art  = sum(1 for wr in all_results
                     if wr["test4"]["artifact_fraction"] > 0.7)

N = len(all_results)

print(f"\n  N worlds: {N}")
print()
print(f"  TEST 1 (Drop rate z-score):")
print(f"    p is DISTINCTIVE (|z|>1.5): {t1_distinctive}/{N}")
print(f"    p is ORDINARY:              {t1_ordinary}/{N}")
print()
print(f"  TEST 2 (Residual after baseline):")
print(f"    p SUPPRESSED below baseline: {t2_suppressed}/{N}")
print(f"    p ELEVATED above baseline:   {t2_elevated}/{N}")
print(f"    p near baseline:             {t2_neutral}/{N}")
print()
print(f"  TEST 3 (Phase coherence at k=p-1):")
print(f"    p lands at MINIMUM rank (expected from countdown): {t3_minimum}/{N}")
print(f"    p NOT at minimum:                                  {t3_not_min}/{N}")
print(f"    p UNUSUALLY LOW (z<-1.5):  {t3_low_z}/{N}")
print(f"    p UNUSUALLY HIGH (z>1.5):  {t3_high_z}/{N}")
print()
print(f"  TEST 4 (Spectral contrast — rank trajectory):")
print(f"    p rank drops to 0 AT k=p (structural minimum): {t4_p_min_at_kp}/{N}")
print(f"    Dominant = largest prime >70% of k range:      {t4_strong_art}/{N}")
print()

# Determine verdict
artifact_score = 0  # +1 for each artifact signal
structure_score = 0  # +1 for each genuine structure signal

# Artifact evidence: large-f domination
if t4_strong_art >= N * 0.7:
    artifact_score += 2
    print("  ARTIFACT EVIDENCE: Largest prime dominates rank in most worlds.")

# Genuine structure evidence: p ranks minimum AT k=p
if t4_p_min_at_kp >= N * 0.5:
    structure_score += 2
    print("  STRUCTURE EVIDENCE: p reaches rank minimum AT k=p in majority of worlds.")

# Genuine structure: p suppressed below baseline
if t2_suppressed >= N * 0.5:
    structure_score += 1
    print("  STRUCTURE EVIDENCE: p consistently suppressed below neutral-prime baseline.")

if t2_elevated >= N * 0.5:
    artifact_score += 1
    print("  ARTIFACT EVIDENCE: p elevated above baseline (follows large-f trend).")

# Genuine structure: p at minimum in phase coherence test
if t3_minimum >= N * 0.5:
    structure_score += 1
    print("  STRUCTURE EVIDENCE: p consistently at minimum rank at k=p-1 (countdown law).")

# Drop rate distinctive
if t1_distinctive >= N * 0.5:
    structure_score += 1
    print("  STRUCTURE EVIDENCE: p shows distinctive drop rate vs neutral primes.")

print()
print(f"  Artifact score:  {artifact_score}")
print(f"  Structure score: {structure_score}")
print()

if artifact_score > structure_score + 1:
    verdict = "GEOMETRIC ARTIFACT"
    explanation = (
        "The spectral horizon (dominant = next prime beyond q) is primarily a "
        "geometric artifact of the R(k,f) formula. For large f, sin²(π/f) → (π/f)² → 0, "
        "so R grows trivially with f. The largest prime in the frequency list will always "
        "dominate in raw magnitude. p and q do NOT show distinctive normalized signatures "
        "that exceed what neutral primes of similar size produce."
    )
elif structure_score > artifact_score + 1:
    verdict = "REAL SIGNAL"
    explanation = (
        "Despite the large-f bias, p shows distinctive structure in normalized measures. "
        "The rank drop to 0 at k=p, the suppression below the neutral baseline, and the "
        "minimum at k=p-1 are algebraically forced by the countdown law R(p-1,p)=1/(p-1)². "
        "These are genuine structural signals that neutral primes do NOT produce at the "
        "same k values. The spectral horizon is partly artifact but p's countdown structure "
        "is real."
    )
else:
    verdict = "MIXED"
    explanation = (
        "Both effects coexist. The raw dominance of large primes is a geometric artifact. "
        "However, p does show at least some normalized signatures that neutral primes lack: "
        "the countdown law R(p-1,p)=1/(p-1)² is algebraically exact and p DOES reach rank "
        "minimum at k=p in many worlds. The spectral horizon is an artifact in raw terms, "
        "but the algebraic structure at k=p is real information layered on top of it."
    )

print(f"  VERDICT: {verdict}")
print()
print(f"  {explanation}")
print()

# Per-world summary table
print("  Per-world summary:")
print(f"  {'b':>6}  {'p':>4}  {'q':>4}  "
      f"{'t1_z':>6}  {'t2_resid_p':>10}  "
      f"{'t3_rank_p':>10}  {'t4_pk_rank':>10}  {'art%':>6}")
for wr in all_results:
    print(f"  {wr['b']:>6}  {wr['p']:>4}  {wr['q']:>4}  "
          f"{wr['test1']['z_p']:>+6.2f}  {wr['test2']['mean_resid_p']:>+10.6f}  "
          f"{wr['test3']['rank_p_at_pm1']:>10}  {wr['test4']['rank_p_at_kp']:>10}  "
          f"{wr['test4']['artifact_fraction']:>6.0%}")

# Save verdict
verdict_data = {
    "verdict": verdict,
    "explanation": explanation,
    "scores": {"artifact": artifact_score, "structure": structure_score},
    "tallies": {
        "N": N,
        "t1_distinctive": t1_distinctive,
        "t2_suppressed": t2_suppressed, "t2_elevated": t2_elevated,
        "t3_minimum": t3_minimum, "t3_low_z": t3_low_z,
        "t4_p_min_at_kp": t4_p_min_at_kp, "t4_strong_artifact": t4_strong_art
    },
    "per_world": [
        {
            "b": wr["b"], "p": wr["p"], "q": wr["q"],
            "t1_z_p": wr["test1"]["z_p"],
            "t2_mean_resid_p": wr["test2"]["mean_resid_p"],
            "t3_rank_p_at_pm1": wr["test3"]["rank_p_at_pm1"],
            "t3_z_p": wr["test3"]["z_p"],
            "t4_rank_p_at_kp": wr["test4"]["rank_p_at_kp"],
            "t4_artifact_fraction": wr["test4"]["artifact_fraction"]
        }
        for wr in all_results
    ]
}

with open(OUT / "verdict.json", "w", encoding="utf-8") as f:
    json.dump(verdict_data, f, indent=2)

print(f"\n  Verdict saved: {OUT / 'verdict.json'}")
print(f"  All outputs in: {OUT.absolute()}")
