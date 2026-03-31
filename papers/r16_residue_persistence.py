"""
r16_residue_persistence.py
===========================
Residue Persistence Score (RPS) -- Topological Recoil Metric

Fixes the degenerate best_score_k() which tracked hit_G and stay_G as
the same counter, yielding 0.5*(x) + 0.5*(1-x) = 0.5 always (flat).

NEW METRIC: Residue Persistence Score (RPS)
For each (b, k):
  - Run a random walk through the CL multiplication table (mod b)
  - Start at a random unit x in C_k  (gcd(x,b) == 1)
  - At each step: pick a random operator o in {1..k}, compute x*o mod b
  - When the walk first lands in G_k (gcd(r,b) > 1), record how many
    CONSECUTIVE steps it stays in G before returning to a unit
  - RPS(b,k) = mean(steps_stuck_in_G) / k   (normalized by alphabet size)

This measures "topological recoil" -- how sticky the obstruction zone is.

Corridor Skew = RPS(b, k=p+1) - RPS(b, k=p-1)
The jump in stickiness across the First-G event.

KEY QUESTION: Does the post-First-G RPS slope in the bridge k=p..q
encode the prime gap (q-p) or ratio q/p? Can we estimate q from the
post-G recovery rate without reaching k=q?

Author: Brayden Sanders / 7Site LLC  |  Sprint 4 (March 2026)
DOI: 10.5281/zenodo.18852047
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

import json
import math
import os
import random
import statistics
import time
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

# ─── output directory ────────────────────────────────────────────────────────
OUT = Path("results/residue_persistence")
OUT.mkdir(parents=True, exist_ok=True)

# ─── survey targets: (b, label, p, q) ────────────────────────────────────────
TARGETS: List[Tuple[int, str, int, int]] = [
    (15,   "3x5",   3,  5),
    (21,   "3x7",   3,  7),
    (35,   "5x7",   5,  7),
    (55,   "5x11",  5, 11),
    (77,   "7x11",  7, 11),
    (91,   "7x13",  7, 13),
    (143,  "11x13", 11, 13),
    (187,  "11x17", 11, 17),
    (221,  "13x17", 13, 17),
    (323,  "17x19", 17, 19),
    (667,  "23x29", 23, 29),
    (1073, "29x37", 29, 37),
]

# ─── RPS parameters ──────────────────────────────────────────────────────────
N_STEPS  = 1000   # random walk steps per trial
N_TRIALS = 200    # trials per (b, k) measurement


# ─────────────────────────────────────────────────────────────────────────────
#  G elements: integers in {1..k} that share a factor with b
# ─────────────────────────────────────────────────────────────────────────────

def g_elements(k: int, b: int) -> List[int]:
    return [x for x in range(1, k + 1) if math.gcd(x, b) > 1]


def c_elements(k: int, b: int) -> List[int]:
    return [x for x in range(1, k + 1) if math.gcd(x, b) == 1]


# ─────────────────────────────────────────────────────────────────────────────
#  Core RPS measurement
# ─────────────────────────────────────────────────────────────────────────────

def measure_rps(b: int, k: int, n_steps: int = N_STEPS,
                n_trials: int = N_TRIALS, seed: int = 0) -> Optional[float]:
    """
    Residue Persistence Score for (b, k).

    Returns None if G_k is empty (no obstruction yet) or C_k is empty.

    Algorithm per trial:
      1. Start at a random unit in C_k.
      2. At each step: pick random operator o in {1..k},
         compute nxt = (state * o) % b.
         If nxt == 0 or nxt > k: stay (boundary bounce).
      3. When entering G_k: count consecutive G-steps until exit.
         A "stuck run" = length of that consecutive G-stay.
      4. Collect all stuck-run lengths across all G-contacts in this trial.

    RPS = median(all_stuck_runs) / k
    (Uses median across 200 trials to avoid outlier inflation.)
    """
    G_set = set(g_elements(k, b))
    C_list = c_elements(k, b)
    if not G_set or not C_list:
        return None

    operators = list(range(1, k + 1))
    rng = random.Random(seed)

    # Collect per-trial mean stuck-run (so we can take median over trials)
    trial_means: List[float] = []

    for _ in range(n_trials):
        state = rng.choice(C_list)
        stuck_runs: List[int] = []
        in_G = False
        run_len = 0

        for _ in range(n_steps):
            op  = rng.choice(operators)
            nxt = (state * op) % b
            if nxt == 0 or nxt > k:
                nxt = state  # boundary bounce: stay

            if nxt in G_set:
                if not in_G:
                    # just entered G
                    in_G  = True
                    run_len = 1
                else:
                    run_len += 1
            else:
                if in_G:
                    # just exited G -- record the run
                    stuck_runs.append(run_len)
                    in_G  = False
                    run_len = 0

            state = nxt

        # if still in G at end of walk, record partial run
        if in_G and run_len > 0:
            stuck_runs.append(run_len)

        if stuck_runs:
            trial_means.append(statistics.mean(stuck_runs))
        else:
            trial_means.append(0.0)

    if not trial_means:
        return 0.0

    # median over trials, then normalize by k
    med = statistics.median(trial_means)
    return med / k


# ─────────────────────────────────────────────────────────────────────────────
#  Post-First-G slope analysis
# ─────────────────────────────────────────────────────────────────────────────

def estimate_slope(k_vals: List[int], rps_vals: List[float]) -> float:
    """Linear slope of RPS vs k over the bridge zone."""
    if len(k_vals) < 2:
        return 0.0
    n = len(k_vals)
    x = np.array(k_vals, dtype=float)
    y = np.array(rps_vals, dtype=float)
    x_mean = x.mean()
    y_mean = y.mean()
    num = float(np.dot(x - x_mean, y - y_mean))
    den = float(np.dot(x - x_mean, x - x_mean))
    return num / den if den != 0.0 else 0.0


# ─────────────────────────────────────────────────────────────────────────────
#  Main survey
# ─────────────────────────────────────────────────────────────────────────────

def run_survey() -> List[dict]:
    """Run RPS survey over all semiprime targets. Returns list of row dicts."""
    all_rows: List[dict] = []
    summary_by_world: List[dict] = []

    print("Residue Persistence Score Survey")
    print("=" * 80)
    print(f"  n_steps={N_STEPS}  n_trials={N_TRIALS}  (median RPS)")
    print()

    # Header
    print(f"{'b':>6}  {'label':>7}  {'k':>4}  {'dk':>4}  {'|G|':>4}  "
          f"{'|C|':>4}  {'RPS':>8}  {'corr_skew':>10}  note")
    print("-" * 80)

    for b, label, p, q in TARGETS:
        k_min = p - 2
        k_max = min(q, p + 8)
        # Ensure k_min >= 1
        k_min = max(1, k_min)

        # k range to sweep
        k_range = list(range(k_min, k_max + 1))

        rps_map: dict = {}

        t0 = time.time()
        for k in k_range:
            rps = measure_rps(b, k, N_STEPS, N_TRIALS, seed=b * 1000 + k)
            rps_map[k] = rps

        elapsed = time.time() - t0

        # Corridor skew: RPS(p+1) - RPS(p-1)
        rps_pm1 = rps_map.get(p - 1) or 0.0
        rps_pp1 = rps_map.get(p + 1) or 0.0
        corridor_skew = (rps_pp1 if rps_pp1 is not None else 0.0) - \
                        (rps_pm1 if rps_pm1 is not None else 0.0)

        # Bridge slope: k = p..min(q, p+8)
        bridge_ks   = [k for k in range(p, k_max + 1) if rps_map.get(k) is not None]
        bridge_rps  = [rps_map[k] for k in bridge_ks]
        bridge_slope = estimate_slope(bridge_ks, bridge_rps)

        # Emit per-row
        world_rows = []
        for k in k_range:
            rps = rps_map.get(k)
            G   = g_elements(k, b)
            C   = c_elements(k, b)
            dk  = k - p  # relative to First-G event

            if rps is None:
                rps_str = "   None"
                note    = "no G or no C"
                rps_val = None
            else:
                rps_str = f"{rps:8.5f}"
                if k < p:
                    note = "pre-G (flat expected)"
                elif k == p:
                    note = "<<< First-G >>>"
                elif k < q:
                    note = f"bridge  slope={bridge_slope:+.5f}"
                else:
                    note = "<<< Second-G >>>"

            row = {
                "b": b, "label": label, "p": p, "q": q,
                "k": k, "dk": dk,
                "G_size": len(G), "C_size": len(C),
                "rps": rps,
                "corridor_skew": corridor_skew,
                "bridge_slope": bridge_slope,
                "q_over_p": round(q / p, 6),
                "q_minus_p": q - p,
            }
            all_rows.append(row)
            world_rows.append(row)

            print(f"{b:>6}  {label:>7}  {k:>4}  {dk:>+4}  {len(G):>4}  "
                  f"{len(C):>4}  {rps_str}  {corridor_skew:>10.5f}  {note}")

        # Per-world summary
        summary_by_world.append({
            "b": b, "label": label, "p": p, "q": q,
            "q_over_p": round(q / p, 6), "q_minus_p": q - p,
            "corridor_skew": corridor_skew,
            "bridge_slope": bridge_slope,
            "elapsed_s": round(elapsed, 2),
        })

        print(f"  => corridor_skew={corridor_skew:+.5f}  "
              f"bridge_slope={bridge_slope:+.6f}  "
              f"({elapsed:.1f}s)")
        print()

    # ── Answer the key question ──────────────────────────────────────────────
    print()
    print("=" * 80)
    print("KEY QUESTION ANALYSIS: Does RPS slope encode q-p or q/p?")
    print("-" * 80)

    gaps      = [w["q_minus_p"]    for w in summary_by_world]
    ratios    = [w["q_over_p"]     for w in summary_by_world]
    slopes    = [w["bridge_slope"] for w in summary_by_world]
    skews     = [w["corridor_skew"] for w in summary_by_world]

    # Pearson correlation: slope vs gap and slope vs ratio
    def pearson(xs, ys):
        n = len(xs)
        if n < 2:
            return 0.0
        mx, my = sum(xs) / n, sum(ys) / n
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        dx  = math.sqrt(sum((x - mx) ** 2 for x in xs))
        dy  = math.sqrt(sum((y - my) ** 2 for y in ys))
        if dx * dy == 0:
            return 0.0
        return num / (dx * dy)

    r_slope_gap   = pearson(gaps,   slopes)
    r_slope_ratio = pearson(ratios, slopes)
    r_skew_gap    = pearson(gaps,   skews)
    r_skew_ratio  = pearson(ratios, skews)

    print(f"  Pearson r(bridge_slope, q-p)   = {r_slope_gap:+.4f}")
    print(f"  Pearson r(bridge_slope, q/p)   = {r_slope_ratio:+.4f}")
    print(f"  Pearson r(corridor_skew, q-p)  = {r_skew_gap:+.4f}")
    print(f"  Pearson r(corridor_skew, q/p)  = {r_skew_ratio:+.4f}")
    print()

    if abs(r_slope_gap) > abs(r_slope_ratio):
        print("  RESULT: bridge_slope correlates more strongly with (q-p) than q/p")
    elif abs(r_slope_ratio) > abs(r_slope_gap):
        print("  RESULT: bridge_slope correlates more strongly with (q/p) than q-p")
    else:
        print("  RESULT: bridge_slope shows equal/no correlation with either measure")

    if abs(r_skew_gap) > abs(r_skew_ratio):
        print("  RESULT: corridor_skew correlates more strongly with (q-p)")
    elif abs(r_skew_ratio) > abs(r_skew_gap):
        print("  RESULT: corridor_skew correlates more strongly with (q/p)")

    print()
    print("  Per-world summary (sorted by q/p):")
    print(f"  {'b':>6}  {'label':>7}  {'q/p':>6}  {'q-p':>4}  "
          f"{'skew':>10}  {'slope':>10}")
    for w in sorted(summary_by_world, key=lambda x: x["q_over_p"]):
        print(f"  {w['b']:>6}  {w['label']:>7}  {w['q_over_p']:>6.3f}  "
              f"{w['q_minus_p']:>4}  {w['corridor_skew']:>10.5f}  "
              f"{w['bridge_slope']:>10.6f}")

    # ── Save JSON ────────────────────────────────────────────────────────────
    json_path = OUT / "rps_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "parameters": {"n_steps": N_STEPS, "n_trials": N_TRIALS},
            "rows": all_rows,
            "world_summary": summary_by_world,
            "correlations": {
                "r_slope_gap": r_slope_gap,
                "r_slope_ratio": r_slope_ratio,
                "r_skew_gap": r_skew_gap,
                "r_skew_ratio": r_skew_ratio,
            },
        }, f, indent=2)
    print(f"\n  Data saved: {json_path}")

    return all_rows, summary_by_world


# ─────────────────────────────────────────────────────────────────────────────
#  Plotting
# ─────────────────────────────────────────────────────────────────────────────

def make_plots(all_rows: List[dict], summary: List[dict]) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
    except ImportError:
        print("  matplotlib not available -- skipping plots")
        return

    colors = cm.tab20(np.linspace(0, 1, len(TARGETS)))

    # ── Plot 1: RPS vs dk (normalized k-p) for all worlds ────────────────────
    fig, ax = plt.subplots(figsize=(12, 7))

    for i, (b, label, p, q) in enumerate(TARGETS):
        world_rows = [r for r in all_rows if r["b"] == b]
        if not world_rows:
            continue
        dk_vals  = [r["dk"]  for r in world_rows if r["rps"] is not None]
        rps_vals = [r["rps"] for r in world_rows if r["rps"] is not None]
        if not dk_vals:
            continue
        ax.plot(dk_vals, rps_vals, marker="o", markersize=5,
                color=colors[i], label=f"b={b} ({label})", linewidth=1.5)
        # mark First-G event (dk=0)
        ax.axvline(x=0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)

    ax.set_xlabel("k - p  (relative to First-G event)", fontsize=12)
    ax.set_ylabel("RPS = mean(steps_stuck_in_G) / k", fontsize=12)
    ax.set_title("Residue Persistence Score vs Alphabet Position\n"
                 "(dk=0 is First-G contact; pre-G zone dk<0 should be flat/near-zero)",
                 fontsize=12)
    ax.legend(fontsize=8, loc="upper left", ncol=2)
    ax.grid(True, alpha=0.3)
    ax.axvline(x=0, color="black", linestyle="-", linewidth=1.2, alpha=0.7,
               label="First-G (k=p)")

    fig.tight_layout()
    p1 = OUT / "plot1_rps_vs_dk.png"
    fig.savefig(p1, dpi=150)
    plt.close(fig)
    print(f"  Plot 1 saved: {p1}")

    # ── Plot 2: corridor_skew vs q/p ratio ───────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: skew vs q/p
    ax = axes[0]
    xs_ratio = [w["q_over_p"]     for w in summary]
    ys_skew  = [w["corridor_skew"] for w in summary]
    labels_  = [w["label"]         for w in summary]

    for x, y, lbl, col in zip(xs_ratio, ys_skew, labels_, colors):
        ax.scatter(x, y, color=col, s=80, zorder=5)
        ax.annotate(lbl, (x, y), textcoords="offset points",
                    xytext=(4, 4), fontsize=8)

    # Fit line
    if len(xs_ratio) >= 2:
        x_arr = np.array(xs_ratio)
        y_arr = np.array(ys_skew)
        coeffs = np.polyfit(x_arr, y_arr, 1)
        x_fit = np.linspace(min(x_arr), max(x_arr), 100)
        ax.plot(x_fit, np.polyval(coeffs, x_fit), "r--",
                linewidth=1.5, label=f"fit: slope={coeffs[0]:+.4f}")

    ax.set_xlabel("q/p  (prime ratio)", fontsize=12)
    ax.set_ylabel("Corridor Skew = RPS(p+1) - RPS(p-1)", fontsize=12)
    ax.set_title("Corridor Skew vs q/p Ratio\n"
                 "(wider ratio = closer primes in relative sense?)", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # Right: slope vs q-p
    ax = axes[1]
    xs_gap   = [w["q_minus_p"]    for w in summary]
    ys_slope = [w["bridge_slope"] for w in summary]

    for x, y, lbl, col in zip(xs_gap, ys_slope, labels_, colors):
        ax.scatter(x, y, color=col, s=80, zorder=5)
        ax.annotate(lbl, (x, y), textcoords="offset points",
                    xytext=(4, 4), fontsize=8)

    if len(xs_gap) >= 2:
        x_arr = np.array(xs_gap, dtype=float)
        y_arr = np.array(ys_slope, dtype=float)
        coeffs = np.polyfit(x_arr, y_arr, 1)
        x_fit = np.linspace(min(x_arr), max(x_arr), 100)
        ax.plot(x_fit, np.polyval(coeffs, x_fit), "b--",
                linewidth=1.5, label=f"fit: slope={coeffs[0]:+.4f}")

    ax.set_xlabel("q - p  (prime gap)", fontsize=12)
    ax.set_ylabel("Bridge Slope  dRPS/dk  (k in p..q)", fontsize=12)
    ax.set_title("Bridge Slope vs Prime Gap\n"
                 "(does larger gap = steeper or shallower recovery?)", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.suptitle("Residue Persistence: Corridor Skew and Bridge Slope\n"
                 "as functions of prime gap geometry", fontsize=13, y=1.02)
    fig.tight_layout()
    p2 = OUT / "plot2_skew_vs_prime_gap.png"
    fig.savefig(p2, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Plot 2 saved: {p2}")


# ─────────────────────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    t_start = time.time()
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    all_rows, summary = run_survey()
    make_plots(all_rows, summary)

    print()
    print(f"Total elapsed: {time.time() - t_start:.1f}s")
    print(f"Output directory: {OUT.resolve()}")
    print("Done.")
