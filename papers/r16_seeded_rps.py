"""
r16_seeded_rps.py
==================
Seeded Entry RPS -- Force-Start Topological Recoil Measurement

Fixes the large-semiprime zero-RPS problem:
  For b >= 77, |G_k| at k=p is often exactly 1, and a walk starting from
  a random UNIT rarely lands on that single G element (probability ~1/b per
  step), so the old RPS reads near-zero for large worlds even though the
  obstruction is real.

FIX: Seeded Entry RPS
  Force-start the walk AT a G element. Measure how many steps until the walk
  escapes back to a unit in C_k.  This is the TRUE topological recoil:
  "given you're stuck in the obstruction zone, how long to escape?"

  seeded_rps(b, k, trials=500)
    - seed_x = p  (the first non-unit, the canonical G element)
    - for each trial: start at seed_x, step until state in C_k (or cap)
    - mean_escape_length = mean(steps_to_escape over trials)
    - seeded_RPS(b, k) = mean_escape_length / k

Survey:
  - All 12 semiprimes in original survey
  - k = p, p+1, ..., min(q-1, p+6)  (full bridge zone)
  - 500 trials per measurement

Key questions answered:
  1. Does seeded_RPS(k=p) predict (q-p) or q/p?
     => Pearson r(seeded_RPS(p), q-p)  and  r(seeded_RPS(p), q/p)
  2. Does the slope of seeded_RPS over the bridge encode the gap?
     => r(slope, q-p)  and  r(slope, q/p)
  3. Geometric shortcut: can f(seeded_RPS(p+1) - seeded_RPS(p)) estimate q-p?

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

# ─── parameters ──────────────────────────────────────────────────────────────
N_TRIALS   = 500    # trials per (b, k) measurement
MAX_ESCAPE = 5000   # cap on steps to prevent infinite loops


# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────

def g_elements(k: int, b: int) -> List[int]:
    """Integers in {1..k} that share a factor with b (the obstruction zone)."""
    return [x for x in range(1, k + 1) if math.gcd(x, b) > 1]


def c_elements(k: int, b: int) -> List[int]:
    """Integers in {1..k} coprime to b (the unit zone)."""
    return [x for x in range(1, k + 1) if math.gcd(x, b) == 1]


# ─────────────────────────────────────────────────────────────────────────────
#  Seeded RPS: Force-Start Measurement
# ─────────────────────────────────────────────────────────────────────────────

def seeded_rps(b: int, k: int, seed_x: int, trials: int = N_TRIALS,
               rng_seed: int = 0) -> Optional[float]:
    """
    Seeded Entry RPS for (b, k).

    Args:
        b:       semiprime
        k:       alphabet size (walk operators in {1..k})
        seed_x:  starting element (MUST be in G_k, typically = p)
        trials:  number of independent escape measurements
        rng_seed: reproducibility seed

    Returns:
        seeded_RPS = mean_escape_length / k
        None if G_k is empty or C_k is empty or seed_x not in G_k.

    Algorithm per trial:
        1. Start at seed_x (a G element).
        2. At each step: pick random operator o in {1..k},
           compute nxt = (state * o) % b.
           If nxt == 0 or nxt > k: boundary bounce (stay).
        3. Count steps until state first lands in C_k (a unit).
           If MAX_ESCAPE steps reached without escaping, record MAX_ESCAPE
           (this preserves ordering even for very sticky zones).
        4. escape_lengths = list of steps-to-escape over all trials.
        5. seeded_RPS = mean(escape_lengths) / k
    """
    G_set = set(g_elements(k, b))
    C_set = set(c_elements(k, b))
    if not G_set or not C_set:
        return None
    if seed_x not in G_set:
        return None

    operators = list(range(1, k + 1))
    rng = random.Random(rng_seed)

    escape_lengths: List[int] = []

    for _ in range(trials):
        state = seed_x
        steps = 0
        escaped = False

        while steps < MAX_ESCAPE:
            op  = rng.choice(operators)
            nxt = (state * op) % b
            if nxt == 0 or nxt > k:
                nxt = state  # boundary bounce

            steps += 1
            if nxt in C_set:
                escaped = True
                break
            state = nxt

        escape_lengths.append(steps)

    if not escape_lengths:
        return None

    mean_escape = statistics.mean(escape_lengths)
    return mean_escape / k


# ─────────────────────────────────────────────────────────────────────────────
#  Linear slope helper
# ─────────────────────────────────────────────────────────────────────────────

def estimate_slope(k_vals: List[int], rps_vals: List[float]) -> float:
    """OLS slope of rps_vals ~ k_vals."""
    if len(k_vals) < 2:
        return 0.0
    x = np.array(k_vals, dtype=float)
    y = np.array(rps_vals, dtype=float)
    x_mean = x.mean()
    y_mean = y.mean()
    num = float(np.dot(x - x_mean, y - y_mean))
    den = float(np.dot(x - x_mean, x - x_mean))
    return num / den if den != 0.0 else 0.0


def pearson(xs: List[float], ys: List[float]) -> float:
    """Pearson correlation coefficient."""
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


# ─────────────────────────────────────────────────────────────────────────────
#  Main survey
# ─────────────────────────────────────────────────────────────────────────────

def run_seeded_survey() -> Tuple[List[dict], List[dict]]:
    """
    Run seeded RPS survey over all semiprime targets.
    Returns (all_rows, world_summary).
    """
    all_rows: List[dict] = []
    world_summary: List[dict] = []

    print("Seeded Entry RPS Survey")
    print("=" * 90)
    print(f"  trials={N_TRIALS}  max_escape={MAX_ESCAPE}  seed_x=p (first non-unit)")
    print(f"  Bridge zone: k = p .. min(q-1, p+6)")
    print()

    print(f"{'b':>6}  {'label':>7}  {'k':>4}  {'dk':>4}  {'|G|':>4}  "
          f"{'|C|':>4}  {'srps':>9}  {'escape*k':>9}  note")
    print("-" * 90)

    for b, label, p, q in TARGETS:
        # Bridge zone: k = p .. min(q-1, p+6)
        k_max = min(q - 1, p + 6)
        k_range = list(range(p, k_max + 1))

        srps_map: dict = {}  # k -> seeded_rps value
        escape_map: dict = {}  # k -> raw mean_escape (un-normalized)

        t0 = time.time()
        for k in k_range:
            G = g_elements(k, b)
            # seed_x = p (the first G element; always in G_k for k >= p)
            seed_x = p
            val = seeded_rps(b, k, seed_x, trials=N_TRIALS,
                             rng_seed=b * 10000 + k)
            srps_map[k] = val
            # also store raw mean escape = val * k
            escape_map[k] = (val * k) if val is not None else None

        elapsed = time.time() - t0

        # Bridge slope: over k in range where srps is defined
        bridge_ks  = [k for k in k_range if srps_map.get(k) is not None]
        bridge_rps = [srps_map[k] for k in bridge_ks]
        bridge_slope = estimate_slope(bridge_ks, bridge_rps)

        # seeded_RPS at k=p (the First-G event)
        srps_at_p  = srps_map.get(p)
        # seeded_RPS at k=p+1
        srps_at_p1 = srps_map.get(p + 1) if (p + 1) <= k_max else None

        # Geometric shortcut: delta_srps = srps(p+1) - srps(p)
        delta_srps = None
        if srps_at_p is not None and srps_at_p1 is not None:
            delta_srps = srps_at_p1 - srps_at_p

        # Print per-k rows
        world_rows = []
        for k in k_range:
            G   = g_elements(k, b)
            C   = c_elements(k, b)
            dk  = k - p
            val = srps_map.get(k)
            raw = escape_map.get(k)

            if val is None:
                val_str = "     None"
                raw_str = "     None"
                note    = "no G or seed not in G"
            else:
                val_str = f"{val:9.5f}"
                raw_str = f"{raw:9.3f}" if raw is not None else "     None"
                if k == p:
                    note = f"<<< First-G >>>  srps(p)={val:.5f}"
                elif k < q:
                    note = f"bridge  slope={bridge_slope:+.5f}"
                else:
                    note = "<<< Second-G >>>"

            row = {
                "b": b, "label": label, "p": p, "q": q,
                "k": k, "dk": dk,
                "G_size": len(G), "C_size": len(C),
                "seeded_rps": val,
                "mean_escape": raw,
                "bridge_slope": bridge_slope,
                "srps_at_p": srps_at_p,
                "srps_at_p1": srps_at_p1,
                "delta_srps": delta_srps,
                "q_over_p": round(q / p, 6),
                "q_minus_p": q - p,
            }
            all_rows.append(row)
            world_rows.append(row)

            print(f"{b:>6}  {label:>7}  {k:>4}  {dk:>+4}  {len(G):>4}  "
                  f"{len(C):>4}  {val_str}  {raw_str}  {note}")

        world_summary.append({
            "b": b, "label": label, "p": p, "q": q,
            "q_over_p": round(q / p, 6), "q_minus_p": q - p,
            "srps_at_p": srps_at_p,
            "srps_at_p1": srps_at_p1,
            "delta_srps": delta_srps,
            "bridge_slope": bridge_slope,
            "elapsed_s": round(elapsed, 2),
        })

        print(f"  => srps(p)={srps_at_p}  srps(p+1)={srps_at_p1}  "
              f"delta={delta_srps}  bridge_slope={bridge_slope:+.6f}  ({elapsed:.1f}s)")
        print()

    # ─── Key Question Analysis ────────────────────────────────────────────────
    print()
    print("=" * 90)
    print("KEY QUESTION ANALYSIS")
    print("-" * 90)

    # Filter worlds where srps_at_p is defined
    valid = [w for w in world_summary if w["srps_at_p"] is not None]

    gaps       = [w["q_minus_p"]    for w in valid]
    ratios     = [w["q_over_p"]     for w in valid]
    srps_p     = [w["srps_at_p"]    for w in valid]
    slopes     = [w["bridge_slope"] for w in valid]
    deltas     = [w["delta_srps"]   for w in valid
                  if w["delta_srps"] is not None]
    delta_gaps = [w["q_minus_p"]    for w in valid
                  if w["delta_srps"] is not None]
    delta_ratios = [w["q_over_p"]   for w in valid
                    if w["delta_srps"] is not None]

    r_srps_gap   = pearson(gaps,   srps_p)
    r_srps_ratio = pearson(ratios, srps_p)
    r_slope_gap  = pearson(gaps,   slopes)
    r_slope_ratio= pearson(ratios, slopes)

    print(f"\n  1. seeded_RPS(k=p) vs prime structure:")
    print(f"     Pearson r(seeded_RPS(p), q-p)   = {r_srps_gap:+.4f}")
    print(f"     Pearson r(seeded_RPS(p), q/p)   = {r_srps_ratio:+.4f}")

    if abs(r_srps_gap) > abs(r_srps_ratio):
        verdict1 = f"seeded_RPS(p) correlates MORE with gap (q-p)  [r={r_srps_gap:+.4f}]"
    elif abs(r_srps_ratio) > abs(r_srps_gap):
        verdict1 = f"seeded_RPS(p) correlates MORE with ratio (q/p)  [r={r_srps_ratio:+.4f}]"
    else:
        verdict1 = "seeded_RPS(p) shows equal/no correlation with either measure"
    print(f"     => {verdict1}")

    print(f"\n  2. Bridge slope vs prime structure:")
    print(f"     Pearson r(bridge_slope, q-p)    = {r_slope_gap:+.4f}")
    print(f"     Pearson r(bridge_slope, q/p)    = {r_slope_ratio:+.4f}")

    if abs(r_slope_gap) > abs(r_slope_ratio):
        verdict2 = f"bridge_slope correlates MORE with gap (q-p)  [r={r_slope_gap:+.4f}]"
    elif abs(r_slope_ratio) > abs(r_slope_gap):
        verdict2 = f"bridge_slope correlates MORE with ratio (q/p)  [r={r_slope_ratio:+.4f}]"
    else:
        verdict2 = "bridge_slope shows equal/no correlation with either measure"
    print(f"     => {verdict2}")

    # ─── Geometric shortcut test ──────────────────────────────────────────────
    print(f"\n  3. Geometric Shortcut: estimated_gap = f(delta_srps)")
    print(f"     delta_srps = seeded_RPS(p+1) - seeded_RPS(p)")
    print()

    shortcut_rows = []
    for w in valid:
        if w["delta_srps"] is None:
            continue
        d = w["delta_srps"]
        actual_gap = w["q_minus_p"]

        # Simple linear estimate: slope of delta vs gap, scale from p
        # naive_estimate = delta_srps * p  (dimensional restoration)
        # (we'll also try delta * b and delta * (p+1))
        est_naive = d * w["p"]    # scale by p
        est_b     = d * w["b"]    # scale by b
        est_pp1   = d * (w["p"] + 1)  # scale by p+1

        err_naive = abs(est_naive - actual_gap)
        err_b     = abs(est_b     - actual_gap)
        err_pp1   = abs(est_pp1   - actual_gap)

        shortcut_rows.append({
            "b": w["b"], "label": w["label"],
            "p": w["p"], "q": w["q"],
            "actual_gap": actual_gap,
            "delta_srps": d,
            "est_naive": est_naive,   # delta * p
            "est_b": est_b,           # delta * b
            "est_pp1": est_pp1,       # delta * (p+1)
            "err_naive": err_naive,
            "err_b": err_b,
            "err_pp1": err_pp1,
        })

        print(f"  {w['label']:>7}  actual_gap={actual_gap:>3}  "
              f"delta_srps={d:+8.5f}  "
              f"est(delta*p)={est_naive:6.2f}  "
              f"est(delta*b)={est_b:7.2f}  "
              f"est(delta*(p+1))={est_pp1:6.2f}")

    if shortcut_rows:
        mae_naive = statistics.mean(r["err_naive"] for r in shortcut_rows)
        mae_b     = statistics.mean(r["err_b"]     for r in shortcut_rows)
        mae_pp1   = statistics.mean(r["err_pp1"]   for r in shortcut_rows)
        print()
        print(f"  MAE  delta*p   = {mae_naive:.4f}")
        print(f"  MAE  delta*b   = {mae_b:.4f}")
        print(f"  MAE  delta*(p+1) = {mae_pp1:.4f}")

        best_method = min(
            [("delta*p", mae_naive), ("delta*b", mae_b), ("delta*(p+1)", mae_pp1)],
            key=lambda x: x[1]
        )
        print(f"  Best geometric estimate: {best_method[0]}  (MAE={best_method[1]:.4f})")

    # ─── Per-world table ──────────────────────────────────────────────────────
    print()
    print("  Per-world summary (sorted by q/p):")
    print(f"  {'b':>6}  {'label':>7}  {'q/p':>6}  {'q-p':>4}  "
          f"{'srps(p)':>10}  {'srps(p+1)':>10}  {'delta':>10}  {'slope':>10}")
    for w in sorted(world_summary, key=lambda x: x["q_over_p"]):
        print(f"  {w['b']:>6}  {w['label']:>7}  {w['q_over_p']:>6.3f}  "
              f"{w['q_minus_p']:>4}  "
              f"{str(round(w['srps_at_p'],  5) if w['srps_at_p']  is not None else 'None'):>10}  "
              f"{str(round(w['srps_at_p1'], 5) if w['srps_at_p1'] is not None else 'None'):>10}  "
              f"{str(round(w['delta_srps'], 5) if w['delta_srps'] is not None else 'None'):>10}  "
              f"{w['bridge_slope']:>10.6f}")

    # ─── Save JSON ────────────────────────────────────────────────────────────
    json_path = OUT / "seeded_rps_data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "parameters": {
                "n_trials": N_TRIALS,
                "max_escape": MAX_ESCAPE,
                "seed_method": "x=p (first non-unit, canonical G element)",
                "bridge_zone": "k = p .. min(q-1, p+6)",
            },
            "rows": all_rows,
            "world_summary": world_summary,
            "correlations": {
                "r_seeded_rps_p_vs_gap":   r_srps_gap,
                "r_seeded_rps_p_vs_ratio": r_srps_ratio,
                "r_bridge_slope_vs_gap":   r_slope_gap,
                "r_bridge_slope_vs_ratio": r_slope_ratio,
            },
            "shortcut_test": shortcut_rows,
        }, f, indent=2)
    print(f"\n  Data saved: {json_path}")

    return all_rows, world_summary, shortcut_rows, {
        "r_srps_gap": r_srps_gap,
        "r_srps_ratio": r_srps_ratio,
        "r_slope_gap": r_slope_gap,
        "r_slope_ratio": r_slope_ratio,
    }


# ─────────────────────────────────────────────────────────────────────────────
#  Plotting
# ─────────────────────────────────────────────────────────────────────────────

def make_plots(all_rows: List[dict], world_summary: List[dict],
               shortcut_rows: List[dict]) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
    except ImportError:
        print("  matplotlib not available -- skipping plots")
        return

    colors = cm.tab20(np.linspace(0, 1, len(TARGETS)))
    color_map = {b: colors[i] for i, (b, *_) in enumerate(TARGETS)}

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # ── Panel A: seeded_RPS vs k (bridge zone), all worlds ──────────────────
    ax = axes[0, 0]
    for b, label, p, q in TARGETS:
        world_rows = [r for r in all_rows if r["b"] == b
                      and r["seeded_rps"] is not None]
        if not world_rows:
            continue
        k_vals  = [r["k"]          for r in world_rows]
        srp_vals= [r["seeded_rps"] for r in world_rows]
        ax.plot(k_vals, srp_vals, marker="o", markersize=5,
                color=color_map[b], label=f"b={b} ({label})", linewidth=1.5)

    ax.set_xlabel("k  (alphabet size)", fontsize=11)
    ax.set_ylabel("Seeded RPS = mean_escape / k", fontsize=11)
    ax.set_title("Seeded RPS vs k in Bridge Zone\n(walk force-started at x=p)", fontsize=11)
    ax.legend(fontsize=7, loc="upper left", ncol=2)
    ax.grid(True, alpha=0.3)

    # ── Panel B: seeded_RPS(p) vs q-p ───────────────────────────────────────
    ax = axes[0, 1]
    valid_summary = [w for w in world_summary if w["srps_at_p"] is not None]
    xs_gap = [w["q_minus_p"] for w in valid_summary]
    ys_srp = [w["srps_at_p"] for w in valid_summary]
    labels_ = [w["label"]    for w in valid_summary]

    for x, y, lbl, w in zip(xs_gap, ys_srp, labels_, valid_summary):
        col = color_map[w["b"]]
        ax.scatter(x, y, color=col, s=90, zorder=5)
        ax.annotate(lbl, (x, y), textcoords="offset points",
                    xytext=(4, 4), fontsize=8)

    if len(xs_gap) >= 2:
        c_ = np.polyfit(xs_gap, ys_srp, 1)
        xf = np.linspace(min(xs_gap), max(xs_gap), 100)
        r_ = pearson(xs_gap, ys_srp)
        ax.plot(xf, np.polyval(c_, xf), "r--",
                linewidth=1.5, label=f"fit  r={r_:+.3f}")

    ax.set_xlabel("q - p  (prime gap)", fontsize=11)
    ax.set_ylabel("Seeded RPS at k=p", fontsize=11)
    ax.set_title("Seeded RPS(p) vs Prime Gap\n(does it predict q-p?)", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # ── Panel C: seeded_RPS(p) vs q/p ratio ─────────────────────────────────
    ax = axes[1, 0]
    xs_rat = [w["q_over_p"]  for w in valid_summary]
    ys_srp = [w["srps_at_p"] for w in valid_summary]
    labels_= [w["label"]     for w in valid_summary]

    for x, y, lbl, w in zip(xs_rat, ys_srp, labels_, valid_summary):
        col = color_map[w["b"]]
        ax.scatter(x, y, color=col, s=90, zorder=5)
        ax.annotate(lbl, (x, y), textcoords="offset points",
                    xytext=(4, 4), fontsize=8)

    if len(xs_rat) >= 2:
        c_ = np.polyfit(xs_rat, ys_srp, 1)
        xf = np.linspace(min(xs_rat), max(xs_rat), 100)
        r_ = pearson(xs_rat, ys_srp)
        ax.plot(xf, np.polyval(c_, xf), "b--",
                linewidth=1.5, label=f"fit  r={r_:+.3f}")

    ax.set_xlabel("q/p  (prime ratio)", fontsize=11)
    ax.set_ylabel("Seeded RPS at k=p", fontsize=11)
    ax.set_title("Seeded RPS(p) vs q/p Ratio\n(does it predict q/p?)", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # ── Panel D: Geometric shortcut -- actual vs estimated gap ───────────────
    ax = axes[1, 1]
    if shortcut_rows:
        actual  = [r["actual_gap"] for r in shortcut_rows]
        est_b   = [r["est_b"]      for r in shortcut_rows]
        est_p   = [r["est_naive"]  for r in shortcut_rows]
        lbls_sc = [r["label"]      for r in shortcut_rows]

        for ag, eb, ep, lbl, r_ in zip(actual, est_b, est_p, lbls_sc, shortcut_rows):
            col = color_map[r_["b"]]
            ax.scatter(ag, eb,  color=col,      marker="o", s=80, zorder=5)
            ax.scatter(ag, ep,  color=col,      marker="s", s=60, zorder=5,
                       alpha=0.6)
            ax.annotate(lbl, (ag, eb), textcoords="offset points",
                        xytext=(4, 4), fontsize=7)

        # y=x line (perfect prediction)
        all_vals = actual + est_b + est_p
        mn, mx = min(all_vals), max(all_vals)
        ax.plot([mn, mx], [mn, mx], "k--", linewidth=1, alpha=0.5,
                label="perfect y=x")
        ax.scatter([], [], marker="o", color="gray", label="delta*b")
        ax.scatter([], [], marker="s", color="gray", label="delta*p", alpha=0.6)

    ax.set_xlabel("Actual (q - p)", fontsize=11)
    ax.set_ylabel("Estimated gap", fontsize=11)
    ax.set_title("Geometric Shortcut: delta_srps * scale vs Actual Gap\n"
                 "(circles=delta*b, squares=delta*p)", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.suptitle("Seeded Entry RPS -- Force-Start Topological Recoil\n"
                 "(n_trials=500, seed_x=p, bridge zone k=p..min(q-1,p+6))",
                 fontsize=13, y=1.01)
    fig.tight_layout()

    p3 = OUT / "plot3_seeded_rps.png"
    fig.savefig(p3, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Plot 3 saved: {p3}")


# ─────────────────────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    t_start = time.time()
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    all_rows, world_summary, shortcut_rows, corrs = run_seeded_survey()
    make_plots(all_rows, world_summary, shortcut_rows)

    total = time.time() - t_start

    # ─── Write run log ────────────────────────────────────────────────────────
    log_path = OUT / "run_seeded.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Seeded RPS Run Log\n")
        f.write(f"==================\n")
        f.write(f"Run time:      {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total elapsed: {total:.1f}s\n")
        f.write(f"n_trials:      {N_TRIALS}\n")
        f.write(f"max_escape:    {MAX_ESCAPE}\n")
        f.write(f"seed_method:   x=p (canonical G element)\n")
        f.write(f"bridge_zone:   k=p..min(q-1,p+6)\n\n")
        f.write(f"Correlations:\n")
        f.write(f"  r(seeded_RPS(p), q-p)   = {corrs['r_srps_gap']:+.6f}\n")
        f.write(f"  r(seeded_RPS(p), q/p)   = {corrs['r_srps_ratio']:+.6f}\n")
        f.write(f"  r(bridge_slope,  q-p)   = {corrs['r_slope_gap']:+.6f}\n")
        f.write(f"  r(bridge_slope,  q/p)   = {corrs['r_slope_ratio']:+.6f}\n\n")
        f.write(f"World Summary:\n")
        for w in sorted(world_summary, key=lambda x: x["b"]):
            f.write(
                f"  b={w['b']:>5}  {w['label']:>7}  p={w['p']:>3}  q={w['q']:>3}  "
                f"srps(p)={w['srps_at_p']}  "
                f"srps(p+1)={w['srps_at_p1']}  "
                f"delta={w['delta_srps']}  "
                f"slope={w['bridge_slope']:+.6f}\n"
            )
        f.write(f"\nOutput directory: {OUT.resolve()}\n")

    print()
    print(f"Total elapsed: {total:.1f}s")
    print(f"Log saved:     {log_path}")
    print(f"Output dir:    {OUT.resolve()}")
    print("Done.")
