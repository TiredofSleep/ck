"""
r16_ternary_survey.py
=====================
Ternary I-0 view: same {-1, 0, +1} mask data as r16_visual_survey.py
but displayed with a DIVERGING colormap so the three states read as
signed poles rather than just "orange / not orange".

  +1  =  unit (coprime output)       →  BLUE  (coherent)
   0  =  non-unit (G-class output)   →  WHITE / pale (entangled, middle ground)
  -1  =  zero element (b | i*j)      →  RED   (absorbed)

This makes the algebraic polarity visible:
  - Blue cells = structure preserved (unit → unit path)
  - Red cells  = information absorbed (product hit zero)
  - White cells = entangled (fell into G, neither free nor zero)

The ternary structure is what balanced ternary arithmetic IS.
Each cell in the table is a ternary digit: coherent / entangled / absorbed.

Usage:
    python r16_ternary_survey.py
    python r16_ternary_survey.py --b 4 9 15 35 --k_max 12 --evolution
    python r16_ternary_survey.py --cross_k 9 --b 4 6 9 10 14 15 21 25 35 55

Author: Brayden Sanders / 7Site LLC | Sprint 4 (March 2026)
DOI: 10.5281/zenodo.18852047
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

import argparse
import os
from math import gcd

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    from matplotlib.patches import Patch
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("matplotlib not available")


# ═══════════════════════════════════════════════════════════════════════════════
#  COLORMAPS
# ═══════════════════════════════════════════════════════════════════════════════

# Ternary diverging: RED (absorbed=-1) → WHITE (entangled=0) → BLUE (coherent=+1)
CMAP_TERNARY = mcolors.LinearSegmentedColormap.from_list(
    "ternary",
    [
        (0.0,  "#c0392b"),   # -1 = zero/absorbed  = deep red
        (0.25, "#e8a0a0"),   # intermediate red
        (0.5,  "#f5f5f5"),   #  0 = non-unit        = near-white
        (0.75, "#8ab4d4"),   # intermediate blue
        (1.0,  "#1a4f7a"),   # +1 = unit/coherent   = deep blue
    ]
) if HAS_MPL else None

# Keep original binary colormap for comparison
CMAP_BINARY = mcolors.ListedColormap(
    ["#1a1a2e", "#e8e8e8", "#ff6b35"]  # zero=dark navy, non-unit=gray, unit=orange
) if HAS_MPL else None

CMAP_IO = "plasma"

LEGEND_TERNARY = [
    Patch(facecolor="#1a4f7a", label="+1 = unit (coherent)"),
    Patch(facecolor="#f5f5f5", label=" 0 = non-unit (entangled)", edgecolor="#aaa"),
    Patch(facecolor="#c0392b", label="-1 = zero (absorbed)"),
] if HAS_MPL else []

LEGEND_BINARY = [
    Patch(facecolor="#ff6b35", label="1 = unit"),
    Patch(facecolor="#e8e8e8", label="0 = non-unit", edgecolor="#aaa"),
    Patch(facecolor="#1a1a2e", label="· = zero"),
] if HAS_MPL else []


# ═══════════════════════════════════════════════════════════════════════════════
#  TABLE COMPUTATION  (identical to r16_visual_survey.py)
# ═══════════════════════════════════════════════════════════════════════════════

def is_semiprime(b):
    for p in range(2, int(b**0.5) + 1):
        if b % p == 0:
            q = b // p
            if all(q % i != 0 for i in range(2, int(q**0.5) + 1)):
                return True, p, q
    return False, 0, 0


def build_table(b, k):
    T = np.zeros((k, k), dtype=np.int32)
    for i in range(1, k + 1):
        for j in range(1, k + 1):
            T[i-1][j-1] = (i * j) % b
    return T


def build_mask(T, b, k):
    """
    Ternary signed mask: {-1, 0, +1}
      +1 = unit   (gcd(output, b) == 1)
       0 = non-unit, non-zero   (0 < output < b, gcd > 1)
      -1 = zero element  (output == 0 mod b)
    """
    mask = np.zeros((k, k), dtype=np.float32)
    for i in range(k):
        for j in range(k):
            v = int(T[i, j])
            if v == 0:
                mask[i, j] = -1.0
            elif gcd(v, b) == 1:
                mask[i, j] = 1.0
            else:
                mask[i, j] = 0.0
    return mask


def partition_info(b, k):
    C = [x for x in range(1, k+1) if gcd(x, b) == 1]
    G = [x for x in range(1, k+1) if gcd(x, b) > 1]
    return C, G


def _draw_lines(ax, c_indices, g_indices, k, color="white", alpha=0.5, lw=0.8):
    """White separator lines at C/G boundaries."""
    if not c_indices or not g_indices:
        return
    prev = None
    for idx in range(k):
        curr = idx in c_indices
        if prev is not None and curr != prev:
            ax.axhline(idx - 0.5, color=color, linewidth=lw, alpha=alpha)
            ax.axvline(idx - 0.5, color=color, linewidth=lw, alpha=alpha)
        prev = curr


def _annotate(ax, T, mask, k, fontsize=5.5):
    """Annotate cells with signed ternary symbol: +1 / 0 / -"""
    for i in range(k):
        for j in range(k):
            v = mask[i, j]
            sym = "+1" if v > 0 else ("-" if v < 0 else "0")
            color = "white" if v > 0.5 else ("white" if v < -0.5 else "black")
            ax.text(j, i, sym, ha="center", va="center",
                    fontsize=fontsize, color=color, fontweight="bold")


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT: THREE-ROW COMPARISON  (IO / Binary I-0 / Ternary I-0)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_three_row(b, k_values, save_dir=None, show=False):
    """
    Three rows per b: IO (full values) / Binary I-0 / Ternary I-0 (signed).
    This shows exactly what the ternary colormap adds: the absorbed/coherent polarity.
    """
    if not HAS_MPL:
        return
    n_k = len(k_values)
    fig, axes = plt.subplots(3, n_k, figsize=(2.2 * n_k, 7))
    if n_k == 1:
        axes = axes.reshape(3, 1)

    ok, p, q = is_semiprime(b)
    fig.suptitle(
        f"b = {b}  ({p}×{q})   |   Three views: IO · Binary I-0 · Ternary I-0",
        fontsize=11, fontweight="bold", y=1.01
    )

    for col, k in enumerate(k_values):
        T    = build_table(b, k)
        mask = build_mask(T, b, k)
        C, G = partition_info(b, k)
        c_idx = sorted(x-1 for x in C)
        g_idx = sorted(x-1 for x in G)

        # ── Row 0: IO ──────────────────────────────────────────────────────────
        ax0 = axes[0][col]
        ax0.imshow(T, cmap=CMAP_IO, vmin=0, vmax=b-1,
                   aspect="equal", interpolation="nearest")
        ax0.set_title(f"k={k}\n|C|={len(C)} |G|={len(G)}", fontsize=8)
        ax0.set_xticks(range(k))
        ax0.set_yticks(range(k))
        ax0.set_xticklabels(range(1, k+1), fontsize=6)
        ax0.set_yticklabels(range(1, k+1), fontsize=6)
        _draw_lines(ax0, c_idx, g_idx, k)

        # ── Row 1: Binary I-0 (original) ──────────────────────────────────────
        ax1 = axes[1][col]
        ax1.imshow(mask, cmap=CMAP_BINARY, vmin=-1, vmax=1,
                   aspect="equal", interpolation="nearest")
        ax1.set_xticks(range(k))
        ax1.set_yticks(range(k))
        ax1.set_xticklabels(range(1, k+1), fontsize=6)
        ax1.set_yticklabels(range(1, k+1), fontsize=6)
        _draw_lines(ax1, c_idx, g_idx, k)
        if k <= 9:
            for i in range(k):
                for j in range(k):
                    v = mask[i, j]
                    sym = "·" if v < 0 else ("1" if v > 0 else "0")
                    fc = "black" if v >= 0 else "white"
                    ax1.text(j, i, sym, ha="center", va="center",
                             fontsize=6, color=fc)

        # ── Row 2: Ternary I-0 (signed diverging) ─────────────────────────────
        ax2 = axes[2][col]
        ax2.imshow(mask, cmap=CMAP_TERNARY, vmin=-1, vmax=1,
                   aspect="equal", interpolation="nearest")
        ax2.set_xticks(range(k))
        ax2.set_yticks(range(k))
        ax2.set_xticklabels(range(1, k+1), fontsize=6)
        ax2.set_yticklabels(range(1, k+1), fontsize=6)
        _draw_lines(ax2, c_idx, g_idx, k, color="#888888")
        if k <= 9:
            _annotate(ax2, T, mask, k, fontsize=5)

    axes[0][0].set_ylabel("IO\n(i·j mod b)", fontsize=8, fontweight="bold")
    axes[1][0].set_ylabel("I-0\n(binary)", fontsize=8, fontweight="bold")
    axes[2][0].set_ylabel("I-0\n(ternary)", fontsize=8, fontweight="bold")

    # Legends
    leg_bin = fig.legend(handles=LEGEND_BINARY, loc="lower left",
                         ncol=3, fontsize=7, framealpha=0.9,
                         bbox_to_anchor=(0.0, -0.04), title="Binary")
    leg_ter = fig.legend(handles=LEGEND_TERNARY, loc="lower right",
                         ncol=3, fontsize=7, framealpha=0.9,
                         bbox_to_anchor=(1.0, -0.04), title="Ternary")
    fig.add_artist(leg_bin)

    plt.tight_layout()
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, f"ternary_b{b:03d}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"  Saved: {path}")
    if show:
        plt.show()
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT: TERNARY EVOLUTION  (k grows, ternary colormap only)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_ternary_evolution(b, k_max, save_dir=None, show=False):
    """
    Ternary-only evolution as k grows.
    Reveals how the coherent/absorbed/entangled regions form and crystallize.
    """
    if not HAS_MPL:
        return
    k_vals = list(range(2, min(k_max + 1, b)))
    n = len(k_vals)
    fig, axes = plt.subplots(1, n, figsize=(1.8 * n, 2.5))
    if n == 1:
        axes = [axes]

    ok, p, q = is_semiprime(b)
    fig.suptitle(
        f"Ternary I-0 Evolution: b={b} ({p}×{q}), k = 2 → {min(k_max, b-1)}\n"
        "Blue=coherent(+1)  White=entangled(0)  Red=absorbed(-1)",
        fontsize=9, y=1.06
    )

    for col, k in enumerate(k_vals):
        T    = build_table(b, k)
        mask = build_mask(T, b, k)
        C, G = partition_info(b, k)
        c_idx = sorted(x-1 for x in C)
        g_idx = sorted(x-1 for x in G)

        ax = axes[col]
        ax.imshow(mask, cmap=CMAP_TERNARY, vmin=-1, vmax=1,
                  aspect="equal", interpolation="nearest")
        ax.set_title(f"k={k}\n|C|={len(C)}\n|G|={len(G)}", fontsize=7)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("→j", fontsize=6)
        _draw_lines(ax, c_idx, g_idx, k, color="#888", alpha=0.5)

    axes[0].set_ylabel("↓i", fontsize=7)
    plt.tight_layout()

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, f"ternary_evolution_b{b:03d}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"  Saved: {path}")
    if show:
        plt.show()
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT: CROSS-b AT FIXED k  (ternary only, for comparing b values)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_ternary_cross_b(b_values, k, save_dir=None, show=False):
    """
    All b values at fixed k, ternary view only.
    Side by side: shows how different factorizations fill the ternary space.
    """
    if not HAS_MPL:
        return
    n_b = len(b_values)
    fig, axes = plt.subplots(1, n_b, figsize=(2.5 * n_b, 3.5))
    if n_b == 1:
        axes = [axes]

    fig.suptitle(
        f"Ternary I-0: k = {k}, all b values\n"
        "Blue=unit(+1)  White=non-unit(0)  Red=zero(-1)",
        fontsize=10, fontweight="bold", y=1.03
    )

    for col, b in enumerate(b_values):
        ok, p, q = is_semiprime(b)
        T    = build_table(b, k)
        mask = build_mask(T, b, k)
        C, G = partition_info(b, k)
        c_idx = sorted(x-1 for x in C)
        g_idx = sorted(x-1 for x in G)

        ax = axes[col]
        ax.imshow(mask, cmap=CMAP_TERNARY, vmin=-1, vmax=1,
                  aspect="equal", interpolation="nearest")
        ax.set_title(f"b={b}\n({p}×{q})\n|C|={len(C)} |G|={len(G)}", fontsize=8)
        ax.set_xticks(range(k))
        ax.set_yticks(range(k))
        ax.set_xticklabels(range(1, k+1), fontsize=5)
        ax.set_yticklabels(range(1, k+1), fontsize=5)
        _draw_lines(ax, c_idx, g_idx, k, color="#888")
        if k <= 9:
            _annotate(ax, T, mask, k, fontsize=5)

    from matplotlib.patches import Patch
    fig.legend(handles=LEGEND_TERNARY, loc="lower center", ncol=3,
               fontsize=7, framealpha=0.9, bbox_to_anchor=(0.5, -0.06))

    plt.tight_layout()
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, f"ternary_cross_k{k:02d}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"  Saved: {path}")
    if show:
        plt.show()
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT: TERNARY DENSITY MAP  (fraction of each class across (b,k) space)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_ternary_density_map(b_values, k_values, save_dir=None, show=False):
    """
    Three heatmaps stacked: fraction of +1, 0, -1 cells across (b,k) space.
    Reveals how the ternary composition changes as alphabet grows.
    """
    if not HAS_MPL:
        return

    plus1  = np.zeros((len(b_values), len(k_values)))
    zero_c = np.zeros_like(plus1)
    minus1 = np.zeros_like(plus1)

    for ri, b in enumerate(b_values):
        for ci, k in enumerate(k_values):
            if k >= b:
                plus1[ri, ci] = np.nan
                zero_c[ri, ci] = np.nan
                minus1[ri, ci] = np.nan
                continue
            T    = build_table(b, k)
            mask = build_mask(T, b, k)
            n    = k * k
            plus1[ri, ci]  = np.sum(mask == 1.0)  / n
            zero_c[ri, ci] = np.sum(mask == 0.0)  / n
            minus1[ri, ci] = np.sum(mask == -1.0) / n

    b_labels = []
    for b in b_values:
        ok, p, q = is_semiprime(b)
        b_labels.append(f"b={b} ({p}×{q})" if ok else f"b={b}")
    k_labels = [f"k={k}" for k in k_values]

    fig, axes = plt.subplots(1, 3, figsize=(max(18, len(k_values) * 1.5), max(6, len(b_values) * 0.8)))
    fig.suptitle(
        "Ternary Composition Map: fraction of +1 / 0 / -1 across (b, k) space",
        fontsize=12, fontweight="bold"
    )

    data_list  = [plus1, zero_c, minus1]
    titles     = ["+1 (unit / coherent)", "0 (non-unit / entangled)", "-1 (zero / absorbed)"]
    cmaps      = ["Blues", "Greys", "Reds"]

    for ax, data, title, cmap in zip(axes, data_list, titles, cmaps):
        im = ax.imshow(data, cmap=cmap, vmin=0, vmax=1,
                       aspect="auto", interpolation="nearest")
        plt.colorbar(im, ax=ax, label="fraction of k² cells")
        ax.set_xticks(range(len(k_values)))
        ax.set_yticks(range(len(b_values)))
        ax.set_xticklabels(k_labels, rotation=45, ha="right", fontsize=7)
        ax.set_yticklabels(b_labels, fontsize=7)
        ax.set_title(title, fontsize=10)
        for ri in range(len(b_values)):
            for ci in range(len(k_values)):
                v = data[ri, ci]
                if not np.isnan(v):
                    color = "white" if v > 0.5 else "black"
                    ax.text(ci, ri, f"{v:.2f}", ha="center", va="center",
                            fontsize=5.5, color=color)

    plt.tight_layout()
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, "ternary_composition_map.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"  Saved: {path}")
    if show:
        plt.show()
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_B  = [4, 6, 9, 10, 14, 15, 21, 25, 35, 55]
DEFAULT_K_MAX = 15


def main():
    parser = argparse.ArgumentParser(
        description="Ternary I-0 visual survey of finite multiplication algebras")
    parser.add_argument("--b",         type=int, nargs="+", default=DEFAULT_B)
    parser.add_argument("--k_max",     type=int, default=DEFAULT_K_MAX)
    parser.add_argument("--k_min",     type=int, default=2)
    parser.add_argument("--k_step",    type=int, default=1)
    parser.add_argument("--save_dir",  type=str, default="results/visual")
    parser.add_argument("--show",      action="store_true")
    parser.add_argument("--evolution", action="store_true",
                        help="Ternary evolution figures for each b")
    parser.add_argument("--cross_k",   type=int, nargs="*",
                        help="k values for cross-b ternary comparison")
    parser.add_argument("--density_map", action="store_true",
                        help="Three-panel ternary composition map")
    args = parser.parse_args()

    b_values = args.b
    k_values = list(range(args.k_min, args.k_max + 1, args.k_step))
    save_dir = args.save_dir

    if not HAS_MPL:
        print("matplotlib not available — cannot generate images")
        return

    print(f"\nTernary I-0 Survey")
    print(f"  b = {b_values}")
    print(f"  k = {k_values}")
    print(f"  save_dir = {save_dir}")
    print()

    # Three-row comparison for each b
    for b in b_values:
        valid_k = [k for k in k_values if k < b]
        if not valid_k:
            continue
        print(f"  Ternary three-row: b={b}  k={valid_k}")
        plot_three_row(b, valid_k, save_dir=save_dir, show=args.show)

    # Evolution figures
    if args.evolution:
        for b in b_values:
            print(f"  Ternary evolution: b={b}")
            plot_ternary_evolution(b, args.k_max, save_dir=save_dir, show=args.show)

    # Cross-b at fixed k
    if args.cross_k:
        for k in args.cross_k:
            valid_b = [b for b in b_values if k < b]
            if not valid_b:
                continue
            print(f"  Ternary cross-b: k={k}  b={valid_b}")
            plot_ternary_cross_b(valid_b, k, save_dir=save_dir, show=args.show)

    # Ternary composition density map
    if args.density_map:
        print(f"  Ternary composition map: all (b,k)")
        plot_ternary_density_map(b_values, k_values, save_dir=save_dir, show=args.show)

    print("\nDone.")


if __name__ == "__main__":
    main()
