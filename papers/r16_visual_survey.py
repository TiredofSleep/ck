"""
r16_visual_survey.py
=====================
Visual Survey of Finite Multiplication Algebras: Fixed b, Variable Alphabet Size k

Fresh-eyes approach: no hypothesis, no target metric.
Just display multiplication tables (i*j) mod b for {1..k} in two views:

  IO  view: full output value — every cell colored by its value (0..b)
  I-0 view: binary unit mask — cell = 1 if output is coprime with b, else 0

Sweep:
  b in {4, 6, 9, 10, 14, 15, 21, 25, 35, 55} (semiprimes, small to medium)
  k from 2 up to min(b-1, 27) — alphabet {1..k}

Layout:
  One figure per b: rows = IO / I-0, columns = k values
  One summary figure: all b values at same k (e.g. k=9), side by side

Usage:
    python r16_visual_survey.py
    python r16_visual_survey.py --b 9 15 35 --k_max 15
    python r16_visual_survey.py --b 9 --k_max 9 --save_dir results/visual

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
    from matplotlib.gridspec import GridSpec
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("matplotlib not available — text output only")


# ═══════════════════════════════════════════════════════════════════════════════
#  CORE TABLE COMPUTATION
# ═══════════════════════════════════════════════════════════════════════════════

def is_semiprime(b):
    for p in range(2, int(b**0.5) + 1):
        if b % p == 0:
            q = b // p
            if all(q % i != 0 for i in range(2, int(q**0.5) + 1)):
                return True, p, q
    return False, 0, 0


def build_table(b, k):
    """
    Build k×k multiplication table: T[i][j] = (i * j) mod b
    for alphabet {1..k}.
    Values are in {0..b-1}; 0 = zero element (if b | i*j).
    """
    T = np.zeros((k, k), dtype=np.int32)
    for i in range(1, k + 1):
        for j in range(1, k + 1):
            T[i - 1][j - 1] = (i * j) % b
    return T


def build_binary_mask(T, b, k):
    """
    Binary unit mask: cell = 1 if T[i][j] is coprime with b (unit), else 0.
    If T[i][j] = 0: mark as -1 (zero element, different from both).
    """
    mask = np.zeros_like(T, dtype=np.float32)
    for i in range(k):
        for j in range(k):
            v = int(T[i, j])
            if v == 0:
                mask[i, j] = -1.0   # zero element
            elif gcd(v, b) == 1:
                mask[i, j] = 1.0    # unit (coprime) — I
            else:
                mask[i, j] = 0.0    # non-unit — 0
    return mask


def partition_info(b, k):
    C = [x for x in range(1, k + 1) if gcd(x, b) == 1]
    G = [x for x in range(1, k + 1) if gcd(x, b) > 1]
    return C, G


# ═══════════════════════════════════════════════════════════════════════════════
#  TEXT OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

def print_table(b, k, show_binary=True):
    T = build_table(b, k)
    mask = build_binary_mask(T, b, k)
    C, G = partition_info(b, k)

    print(f"\nb={b}  k={k}  C={C}  G={G}")
    print("  IO table (i*j mod b):")
    hdr = "    " + "  ".join(f"{j+1:2d}" for j in range(k))
    print(hdr)
    for i in range(k):
        row = "  ".join(f"{T[i,j]:2d}" for j in range(k))
        print(f"  {i+1:2d}| {row}")

    if show_binary:
        print("  I-0 mask (1=unit, 0=non-unit, ·=zero):")
        print(hdr)
        for i in range(k):
            symbols = []
            for j in range(k):
                v = mask[i, j]
                if v < 0:
                    symbols.append(" ·")
                elif v > 0:
                    symbols.append(" 1")
                else:
                    symbols.append(" 0")
            print(f"  {i+1:2d}| {'  '.join(symbols)}")


# ═══════════════════════════════════════════════════════════════════════════════
#  VISUAL OUTPUT
# ═══════════════════════════════════════════════════════════════════════════════

# Color maps
CMAP_IO   = "plasma"          # Full value: continuous, high contrast
CMAP_UNIT = matplotlib.colors.ListedColormap(
    ["#1a1a2e", "#e8e8e8", "#ff6b35"]  # zero=dark navy, non-unit=light gray, unit=orange
) if HAS_MPL else None


def plot_single_b(b, k_values, save_dir=None, show=False):
    """One figure per b: IO row + I-0 row, one column per k."""
    if not HAS_MPL:
        for k in k_values:
            print_table(b, k)
        return

    n_k = len(k_values)
    fig, axes = plt.subplots(2, n_k, figsize=(2.2 * n_k, 5))
    if n_k == 1:
        axes = axes.reshape(2, 1)

    _, p, q = is_semiprime(b)
    fig.suptitle(f"b = {b}  ({p}×{q})   —   Full values (top) vs Unit mask (bottom)",
                 fontsize=12, fontweight="bold", y=1.02)

    for col, k in enumerate(k_values):
        T = build_table(b, k)
        mask = build_binary_mask(T, b, k)
        C, G = partition_info(b, k)

        # ── IO view ─────────────────────────────────────────────────────────
        ax_io = axes[0][col]
        im = ax_io.imshow(T, cmap=CMAP_IO, vmin=0, vmax=b - 1,
                          aspect="equal", interpolation="nearest")
        ax_io.set_title(f"k={k}\n|C|={len(C)}, |G|={len(G)}", fontsize=8)
        ax_io.set_xticks(range(k))
        ax_io.set_yticks(range(k))
        ax_io.set_xticklabels(range(1, k + 1), fontsize=6)
        ax_io.set_yticklabels(range(1, k + 1), fontsize=6)
        ax_io.tick_params(length=2)

        # Draw partition boundary lines
        c_indices = sorted(x - 1 for x in C)
        g_indices = sorted(x - 1 for x in G)
        _draw_partition_lines(ax_io, c_indices, g_indices, k)

        # ── I-0 view ─────────────────────────────────────────────────────────
        ax_bin = axes[1][col]
        # Use three distinct colors: -1→navy, 0→gray, 1→orange
        display_mask = mask.copy()
        im2 = ax_bin.imshow(display_mask, cmap=CMAP_UNIT, vmin=-1, vmax=1,
                             aspect="equal", interpolation="nearest")
        ax_bin.set_xticks(range(k))
        ax_bin.set_yticks(range(k))
        ax_bin.set_xticklabels(range(1, k + 1), fontsize=6)
        ax_bin.set_yticklabels(range(1, k + 1), fontsize=6)
        ax_bin.tick_params(length=2)
        _draw_partition_lines(ax_bin, c_indices, g_indices, k)

        # Annotate cells for small k
        if k <= 9:
            for i in range(k):
                for j in range(k):
                    v = int(T[i, j])
                    sym = "·" if v == 0 else str(v)
                    color = "white" if mask[i, j] != 1.0 else "black"
                    ax_io.text(j, i, sym, ha="center", va="center",
                               fontsize=5.5, color=color, fontweight="bold")
                    io_sym = "·" if mask[i, j] < 0 else ("1" if mask[i, j] > 0 else "0")
                    ax_bin.text(j, i, io_sym, ha="center", va="center",
                                fontsize=6, color="black" if mask[i, j] >= 0 else "white")

    # Row labels
    axes[0][0].set_ylabel("IO\n(i·j mod b)", fontsize=8, fontweight="bold")
    axes[1][0].set_ylabel("I-0\n(unit mask)", fontsize=8, fontweight="bold")

    # Legend for I-0
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#ff6b35", label="1 = unit (coprime)"),
        Patch(facecolor="#e8e8e8", label="0 = non-unit"),
        Patch(facecolor="#1a1a2e", label="· = zero"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=3,
               fontsize=7, framealpha=0.9, bbox_to_anchor=(0.5, -0.04))

    plt.tight_layout()
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, f"survey_b{b:03d}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"  Saved: {path}")
    if show:
        plt.show()
    plt.close(fig)


def plot_cross_b(b_values, k, save_dir=None, show=False):
    """Compare multiple b values at the same k: IO and I-0 side by side."""
    if not HAS_MPL:
        for b in b_values:
            print_table(b, k, show_binary=True)
        return

    n_b = len(b_values)
    fig, axes = plt.subplots(2, n_b, figsize=(2.2 * n_b, 5))
    if n_b == 1:
        axes = axes.reshape(2, 1)

    fig.suptitle(f"k = {k}  — All b values: IO (top) vs Unit mask (bottom)",
                 fontsize=12, fontweight="bold", y=1.02)

    for col, b in enumerate(b_values):
        T = build_table(b, k)
        mask = build_binary_mask(T, b, k)
        C, G = partition_info(b, k)
        _, p, q = is_semiprime(b)

        ax_io = axes[0][col]
        ax_bin = axes[1][col]

        ax_io.imshow(T, cmap=CMAP_IO, vmin=0, vmax=b - 1,
                     aspect="equal", interpolation="nearest")
        ax_io.set_title(f"b={b}\n({p}×{q})\n|C|={len(C)} |G|={len(G)}", fontsize=7)
        ax_io.set_xticks(range(k))
        ax_io.set_yticks(range(k))
        ax_io.set_xticklabels(range(1, k + 1), fontsize=5)
        ax_io.set_yticklabels(range(1, k + 1), fontsize=5)

        c_indices = sorted(x - 1 for x in C)
        g_indices = sorted(x - 1 for x in G)
        _draw_partition_lines(ax_io, c_indices, g_indices, k)

        ax_bin.imshow(mask, cmap=CMAP_UNIT, vmin=-1, vmax=1,
                      aspect="equal", interpolation="nearest")
        ax_bin.set_xticks(range(k))
        ax_bin.set_yticks(range(k))
        ax_bin.set_xticklabels(range(1, k + 1), fontsize=5)
        ax_bin.set_yticklabels(range(1, k + 1), fontsize=5)
        _draw_partition_lines(ax_bin, c_indices, g_indices, k)

        if k <= 9:
            for i in range(k):
                for j in range(k):
                    v = int(T[i, j])
                    ax_io.text(j, i, str(v) if v != 0 else "·",
                               ha="center", va="center", fontsize=5,
                               color="white" if mask[i, j] != 1.0 else "black")
                    io_sym = "·" if mask[i, j] < 0 else ("1" if mask[i, j] > 0 else "0")
                    ax_bin.text(j, i, io_sym, ha="center", va="center",
                                fontsize=5.5,
                                color="black" if mask[i, j] >= 0 else "white")

    axes[0][0].set_ylabel("IO", fontsize=8, fontweight="bold")
    axes[1][0].set_ylabel("I-0", fontsize=8, fontweight="bold")

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#ff6b35", label="1 = unit"),
        Patch(facecolor="#e8e8e8", label="0 = non-unit"),
        Patch(facecolor="#1a1a2e", label="· = zero"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=3,
               fontsize=7, framealpha=0.9, bbox_to_anchor=(0.5, -0.04))

    plt.tight_layout()
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, f"survey_cross_k{k:02d}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"  Saved: {path}")
    if show:
        plt.show()
    plt.close(fig)


def plot_density_overview(b_values, k_values, save_dir=None, show=False):
    """
    Summary heatmap: rows = b, columns = k.
    Each cell = unit density (fraction of k² cells where output is coprime with b).
    This is the 'gate score at random' = |C|/k baseline.
    """
    if not HAS_MPL:
        return

    data = np.zeros((len(b_values), len(k_values)))
    for ri, b in enumerate(b_values):
        for ci, k in enumerate(k_values):
            T = build_table(b, k)
            mask = build_binary_mask(T, b, k)
            unit_frac = np.sum(mask == 1.0) / (k * k)
            data[ri, ci] = unit_frac

    fig, ax = plt.subplots(figsize=(max(8, len(k_values) * 0.8),
                                     max(5, len(b_values) * 0.7)))
    im = ax.imshow(data, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    plt.colorbar(im, ax=ax, label="Unit density (fraction of cells with coprime output)")
    ax.set_xticks(range(len(k_values)))
    ax.set_yticks(range(len(b_values)))
    ax.set_xticklabels([f"k={k}" for k in k_values], rotation=45, ha="right", fontsize=8)
    b_labels = []
    for b in b_values:
        ok, p, q = is_semiprime(b)
        b_labels.append(f"b={b} ({p}×{q})" if ok else f"b={b}")
    ax.set_yticklabels(b_labels, fontsize=8)
    ax.set_title("Unit Density Map: (b, k) space\n"
                 "Green = high unit density (easy gate), Red = low (hard gate)", fontsize=11)

    # Annotate each cell
    for ri in range(len(b_values)):
        for ci in range(len(k_values)):
            v = data[ri, ci]
            color = "black" if 0.3 < v < 0.8 else "white"
            ax.text(ci, ri, f"{v:.2f}", ha="center", va="center",
                    fontsize=6, color=color)

    # Draw the 0.85 threshold line
    above_085 = np.argmax(data >= 0.85, axis=1)  # first k where density >= 0.85
    for ri, ci in enumerate(above_085):
        if data[ri, ci] >= 0.85:
            ax.axvline(ci - 0.5, color="blue", linewidth=0.5, alpha=0.4)

    plt.tight_layout()
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, "survey_density_overview.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"  Saved: {path}")
    if show:
        plt.show()
    plt.close(fig)


def _draw_partition_lines(ax, c_indices, g_indices, k):
    """Draw subtle lines separating C and G regions."""
    if not c_indices or not g_indices:
        return
    all_idx = sorted(range(k))
    prev_type = None
    for idx in all_idx:
        curr_type = idx in c_indices
        if prev_type is not None and curr_type != prev_type:
            ax.axhline(idx - 0.5, color="white", linewidth=0.8, alpha=0.6)
            ax.axvline(idx - 0.5, color="white", linewidth=0.8, alpha=0.6)
        prev_type = curr_type


def plot_pattern_evolution(b, k_max, save_dir=None, show=False):
    """
    Animation-style: one figure showing how the I-0 pattern evolves as k grows.
    Each row is one k value, padded to k_max so they align.
    Reveals how the binary pattern 'fills in' as the alphabet expands.
    """
    if not HAS_MPL:
        return

    k_vals = list(range(2, min(k_max + 1, b)))
    n = len(k_vals)
    fig, axes = plt.subplots(1, n, figsize=(1.8 * n, 2.5))
    if n == 1:
        axes = [axes]

    _, p, q = is_semiprime(b)
    fig.suptitle(f"Pattern Evolution: b={b} ({p}×{q}), k = 2 → {min(k_max, b-1)}\n"
                 "I-0 mask: orange=unit, gray=non-unit, dark=zero",
                 fontsize=10, y=1.05)

    for col, k in enumerate(k_vals):
        T = build_table(b, k)
        mask = build_binary_mask(T, b, k)
        C, G = partition_info(b, k)

        ax = axes[col]
        ax.imshow(mask, cmap=CMAP_UNIT, vmin=-1, vmax=1,
                  aspect="equal", interpolation="nearest")
        ax.set_title(f"k={k}\n|C|={len(C)}\n|G|={len(G)}", fontsize=7)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("→j", fontsize=6)

    axes[0].set_ylabel("↓i", fontsize=7)
    plt.tight_layout()

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, f"survey_evolution_b{b:03d}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"  Saved: {path}")
    if show:
        plt.show()
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  TEXT SUMMARY (runs even without matplotlib)
# ═══════════════════════════════════════════════════════════════════════════════

def text_survey(b_values, k_values):
    """Print a concise text overview of all (b, k) pairs."""
    print(f"\n{'='*70}")
    print("FINITE ALGEBRA VISUAL SURVEY — TEXT SUMMARY")
    print(f"{'='*70}")
    print(f"  b = {b_values}")
    print(f"  k = {k_values}")
    print()
    print(f"  {'b':>5}  {'factor':>8}  {'k':>3}  {'|C|':>4}  {'|G|':>4}  "
          f"{'|C|/k':>6}  {'unit_density':>13}  pattern")
    print(f"  {'-'*70}")

    for b in b_values:
        ok, p, q = is_semiprime(b)
        label = f"{p}×{q}" if ok else "?"
        for k in k_values:
            if k >= b:
                continue
            T = build_table(b, k)
            mask = build_binary_mask(T, b, k)
            C, G = partition_info(b, k)
            unit_density = np.sum(mask == 1.0) / (k * k)
            unit_frac = len(C) / k if k > 0 else 0

            # Simple pattern descriptor for I-0 mask
            # Count runs of same value in first row
            row0 = mask[0]
            pattern_str = "".join(
                ("1" if v > 0 else ("·" if v < 0 else "0"))
                for v in row0
            )

            print(f"  {b:>5}  {label:>8}  {k:>3}  {len(C):>4}  {len(G):>4}  "
                  f"{unit_frac:>6.3f}  {unit_density:>13.3f}  [{pattern_str}]")
        print()


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_B_VALUES = [4, 6, 9, 10, 14, 15, 21, 25, 35, 55]
DEFAULT_K_MAX = 15


def main():
    parser = argparse.ArgumentParser(
        description="Visual survey of finite multiplication algebras mod b")
    parser.add_argument("--b", type=int, nargs="+", default=DEFAULT_B_VALUES)
    parser.add_argument("--k_max", type=int, default=DEFAULT_K_MAX)
    parser.add_argument("--k_min", type=int, default=2)
    parser.add_argument("--k_step", type=int, default=1)
    parser.add_argument("--save_dir", type=str, default="results/visual")
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--text_only", action="store_true")
    parser.add_argument("--evolution", action="store_true",
                        help="Show pattern evolution (k=2 to k_max) for each b")
    parser.add_argument("--cross_b", type=int, nargs="*",
                        help="k values for cross-b comparison figures")
    args = parser.parse_args()

    b_values = sorted(args.b)
    k_values = list(range(args.k_min, args.k_max + 1, args.k_step))

    # Always print text summary
    text_survey(b_values, k_values)

    if args.text_only or not HAS_MPL:
        print("\n(matplotlib not available or --text_only set; skipping plots)")
        return

    print(f"\nGenerating plots → {args.save_dir}/")
    os.makedirs(args.save_dir, exist_ok=True)

    # 1. Per-b figures: IO + I-0 across k
    for b in b_values:
        valid_k = [k for k in k_values if k < b]
        if not valid_k:
            continue
        # Show up to 8 k values per figure (readability)
        chunk = valid_k[:8] if len(valid_k) > 8 else valid_k
        print(f"  b={b}: k={chunk}")
        plot_single_b(b, chunk, save_dir=args.save_dir, show=args.show)

    # 2. Pattern evolution: how the I-0 mask fills in as k grows
    if args.evolution:
        for b in b_values:
            print(f"  Evolution b={b}: k=2..{args.k_max}")
            plot_pattern_evolution(b, args.k_max, save_dir=args.save_dir, show=args.show)

    # 3. Cross-b comparison at specific k values
    cross_ks = args.cross_b if args.cross_b is not None else [4, 9]
    for k in cross_ks:
        valid_b = [b for b in b_values if b > k]
        if not valid_b:
            continue
        print(f"  Cross-b at k={k}: b={valid_b}")
        plot_cross_b(valid_b, k, save_dir=args.save_dir, show=args.show)

    # 4. Density overview: (b, k) heatmap
    print(f"  Density overview: {len(b_values)} b × {len(k_values)} k")
    plot_density_overview(b_values, k_values, save_dir=args.save_dir, show=args.show)

    print(f"\nDone. All figures saved to {args.save_dir}/")
    print("Files:")
    for f in sorted(os.listdir(args.save_dir)):
        if f.endswith(".png"):
            print(f"  {f}")


if __name__ == "__main__":
    main()
