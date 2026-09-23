"""
bench_visualize.py -- Pareto-frontier plots from the bench results.

Reads bench_results_30k.jsonl (the publication-ready 30k Adult run)
and produces:
  bench_plots/tabular_pareto.png    -- privacy-utility frontier for Adult
  bench_plots/stream_pareto.png     -- privacy-utility frontier for Power
  bench_plots/histogram_pareto.png  -- privacy-utility frontier for KOS

Each plot shows:
  - RGD points connected by line (depth knob trajectory)
  - DP points connected by line (epsilon knob trajectory)
  - k-anon points connected by line (k knob trajectory)
  - Pareto-undominated points highlighted with bold markers
  - The strict dominance of RGD d=2 over DP eps=0.1 (tabular) annotated

Run: python papers/bench_visualize.py
Output: PNG files in bench_plots/
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from typing import Any, Dict, List, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_results(path: str) -> Dict[str, List[Dict[str, Any]]]:
    """Read jsonl and group by dataset."""
    by_dataset: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            by_dataset[r["dataset"]].append(r)
    return by_dataset


def is_pareto_undominated(p: Dict[str, Any], points: List[Dict[str, Any]]) -> bool:
    """A point is Pareto-undominated if no other has lower attacker AND higher utility."""
    for q in points:
        if q is p:
            continue
        if (q["attacker_success"] <= p["attacker_success"]
            and q["utility"] >= p["utility"]
            and (q["attacker_success"] < p["attacker_success"]
                 or q["utility"] > p["utility"])):
            return False
    return True


def plot_dataset(
    dataset: str,
    points: List[Dict[str, Any]],
    out_path: str,
    title_suffix: str = "",
) -> None:
    """Plot the Pareto frontier for one dataset."""
    by_method: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for p in points:
        by_method[p["method"]].append(p)
    for method in by_method:
        # Order by knob (parse numeric portion)
        def knob_key(p):
            knob = p["knob"]
            try:
                return float(knob.split("=")[1])
            except (IndexError, ValueError):
                return 0.0
        by_method[method].sort(key=knob_key)

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = {"RGD": "#1f77b4", "DP": "#d62728", "k-anon": "#2ca02c"}
    markers = {"RGD": "o", "DP": "s", "k-anon": "^"}

    for method, mpoints in by_method.items():
        xs = [p["attacker_success"] for p in mpoints]
        ys = [p["utility"] for p in mpoints]
        ax.plot(xs, ys, "-", color=colors.get(method, "gray"), alpha=0.5,
                linewidth=1.5, label=None)
        # Mark Pareto-undominated with bold border
        for p in mpoints:
            undom = is_pareto_undominated(p, points)
            ax.scatter(
                [p["attacker_success"]], [p["utility"]],
                marker=markers.get(method, "o"),
                color=colors.get(method, "gray"),
                s=130 if undom else 65,
                edgecolor="black" if undom else colors.get(method, "gray"),
                linewidth=2 if undom else 0.5,
                zorder=10,
                label=f"{method} {p['knob']}",
            )
            # Annotate knob
            ax.annotate(
                p["knob"],
                xy=(p["attacker_success"], p["utility"]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8,
                color=colors.get(method, "gray"),
                alpha=0.8,
            )

    ax.set_xlabel("Attacker success (lower = better privacy)")
    ax.set_ylabel("Utility (higher = better)")
    ax.set_title(f"{dataset}: privacy-utility frontier {title_suffix}")
    ax.grid(True, alpha=0.3)

    # Custom legend
    from matplotlib.lines import Line2D
    legend_elems = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=colors["RGD"],
               markersize=10, label="RGD (depth knob)"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor=colors["DP"],
               markersize=10, label="DP (epsilon knob)"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor=colors["k-anon"],
               markersize=10, label="k-anon (k knob)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
               markeredgecolor="black", markeredgewidth=2, markersize=12,
               label="Pareto-undominated"),
    ]
    ax.legend(handles=legend_elems, loc="best", fontsize=9, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {out_path}")


def main() -> int:
    os.makedirs("bench_plots", exist_ok=True)

    for path, scale_label in [
        ("bench_results.jsonl", "(5k sample)"),
        ("bench_results_10k.jsonl", "(10k sample)"),
        ("bench_results_30k.jsonl", "(30k full Adult sample)"),
    ]:
        if not os.path.exists(path):
            continue
        print(f"\nProcessing {path}:")
        by_ds = load_results(path)
        for dataset, pts in by_ds.items():
            suffix = path.replace("bench_results", "").replace(".jsonl", "")
            out = f"bench_plots/{dataset}_pareto{suffix or '_5k'}.png"
            plot_dataset(dataset, pts, out, title_suffix=scale_label)

    print(f"\nDone.  {len(os.listdir('bench_plots'))} plots in bench_plots/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
