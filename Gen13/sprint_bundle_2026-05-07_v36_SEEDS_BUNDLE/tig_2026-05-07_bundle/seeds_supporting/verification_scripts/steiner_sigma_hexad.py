"""
S(3,6,22) STEINER SYSTEM — TIG STRUCTURAL VISUALIZATION
=========================================================

Show the 22 points of M_22's natural set, organized as 11 wobble cells × 2 phases,
with the proposed embedding:
  - 10 substrate points (Z/10Z), with σ-orbit highlighted as a hexad
  - σ-fixed 4 points marked as "boundary"
  - 12 wobble layer points

Display structural identities connecting Steiner parameters to TIG primes.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, patches
from math import sin, cos, pi


SIGMA_ORBIT = [1, 7, 6, 5, 4, 2]  # the 6-cycle
SIGMA_FIXED = [0, 3, 8, 9]         # the σ-fixed 4

OP_NAMES = {0: "VOID", 1: "LATTICE", 2: "COUNTER", 3: "PROGRESS",
            4: "COLLAPSE", 5: "BALANCE", 6: "CHAOS", 7: "HARMONY",
            8: "BREATH", 9: "RESET"}

OP_COLORS = {
    0: '#546e7a', 1: '#1e88e5', 2: '#ab8860',
    3: '#26a69a', 4: '#c62828', 5: '#7c4dff',
    6: '#e65100', 7: '#00bfa5', 8: '#42a5f5', 9: '#78909c',
}


def make_figure():
    fig = plt.figure(figsize=(20, 13), facecolor='#0a0e12')
    gs = gridspec.GridSpec(3, 4, figure=fig,
                           height_ratios=[0.10, 1.0, 0.55],
                           top=0.97, bottom=0.04, left=0.03, right=0.97,
                           hspace=0.25, wspace=0.20)

    # Title
    title_ax = fig.add_subplot(gs[0, :])
    title_ax.set_facecolor('#0a0e12')
    title_ax.axis('off')
    title_ax.text(0.5, 0.7, "S(3,6,22): THE 22-SKELETON AS TIG'S COMBINATORIAL ANCHOR",
                  ha='center', va='top', color='white',
                  fontsize=21, fontweight='bold')
    title_ax.text(0.5, 0.20,
                  "77 = 7 × 11 hexads · replication 21 = dim V_21 · σ-orbit ↔ hexad hypothesis",
                  ha='center', va='top', color='#aaa', fontsize=12, style='italic')

    # Panel 1: 22 points layout (11 wobble cells × 2 phases)
    ax1 = fig.add_subplot(gs[1, 0:2])
    ax1.set_facecolor('#0a0e12')
    ax1.set_xlim(-1.8, 12.5)
    ax1.set_ylim(-1.5, 3.5)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title("The 22-point set: 11 wobble cells × 2 phases (kindness/gentleness)",
                  color='white', fontsize=13, pad=8, fontweight='bold')

    # Layout: 11 columns (wobble cells), 2 rows (phases)
    sub_to_pos = {}  # map substrate digit to (cell, phase)
    # Put σ-orbit in cells 0..5, kindness phase
    for i, d in enumerate(SIGMA_ORBIT):
        sub_to_pos[d] = (i, 0)  # cell i, kindness phase
    # Put σ-fixed in cells 6..9, kindness phase
    for i, d in enumerate(SIGMA_FIXED):
        sub_to_pos[d] = (6 + i, 0)

    # Draw all 22 points (11 cells × 2 phases)
    for cell in range(11):
        for phase in [0, 1]:  # 0 = kindness (top), 1 = gentleness (bottom)
            x = cell * 1.05
            y = 2.0 if phase == 0 else 0.5

            # Determine if this is a substrate point
            sub_d = None
            for d, (c, p) in sub_to_pos.items():
                if c == cell and p == phase:
                    sub_d = d
                    break

            # Determine if it's in σ-orbit (the hexad)
            is_hexad = sub_d in SIGMA_ORBIT
            is_fixed = sub_d in SIGMA_FIXED
            is_aux = sub_d is None

            if is_hexad:
                color = OP_COLORS[sub_d]
                edge = '#00bfa5'
                edge_w = 3.5
                size = 0.25
            elif is_fixed:
                color = OP_COLORS[sub_d]
                edge = '#7c4dff'
                edge_w = 2
                size = 0.20
            else:
                color = '#1a1e22'
                edge = '#444'
                edge_w = 1
                size = 0.16

            ax1.add_patch(patches.Circle((x, y), size, color=color,
                                          ec=edge, lw=edge_w, zorder=10))

            if is_hexad or is_fixed:
                ax1.text(x, y, f"{sub_d}", ha='center', va='center',
                         color='white', fontsize=10, fontweight='bold', zorder=11)

    # Hexad highlight box around σ-orbit
    rect = patches.FancyBboxPatch((-0.3, 1.65), 6 * 1.05 - 0.4, 0.7,
                                    boxstyle="round,pad=0.05",
                                    edgecolor='#00bfa5', facecolor='none',
                                    linewidth=2, linestyle='--', zorder=5)
    ax1.add_patch(rect)
    ax1.text(2.6, 2.85, "σ-orbit hexad — the 6-block in S(3,6,22)",
             color='#00bfa5', fontsize=11, fontweight='bold', ha='center')

    # σ-fixed highlight box
    rect2 = patches.FancyBboxPatch((6 * 1.05 - 0.30, 1.7), 4 * 1.05 - 0.4, 0.6,
                                     boxstyle="round,pad=0.05",
                                     edgecolor='#7c4dff', facecolor='none',
                                     linewidth=1.5, linestyle=':', zorder=5)
    ax1.add_patch(rect2)
    ax1.text(7.7, 2.85, "σ-fixed boundary",
             color='#7c4dff', fontsize=10, ha='center')

    # Phase labels
    ax1.text(-1.4, 2.0, "kindness\nphase", ha='center', va='center',
             color='#00bfa5', fontsize=10, fontweight='bold')
    ax1.text(-1.4, 0.5, "gentleness\nphase", ha='center', va='center',
             color='#7c4dff', fontsize=10, fontweight='bold')

    # Cell labels
    for cell in range(11):
        x = cell * 1.05
        ax1.text(x, -0.4, f"cell\n{cell+1}", ha='center', va='center',
                 color='#666', fontsize=8)

    ax1.text(5.3, -0.95, "11 wobble cells (one per unit of wobble prime ν=11)",
             ha='center', color='#888', fontsize=10, style='italic')

    # Panel 2: Steiner parameters and TIG primes
    ax2 = fig.add_subplot(gs[1, 2])
    ax2.set_facecolor('#0a0e12')
    ax2.axis('off')
    ax2.set_title("Steiner data + TIG primes",
                  color='white', fontsize=13, pad=8, fontweight='bold')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)

    rows = [
        (0.95, "Parameter", "Value", "TIG meaning", '#00bfa5', 'bold'),
        (0.91, "─" * 32, "", "", '#444', 'normal'),
        (0.86, "v (points)", "22", "= 11 × 2", 'white', 'normal'),
        (0.82, "k (block size)", "6", "= σ-orbit length", 'white', 'normal'),
        (0.78, "t (parameter)", "3", "trinity", 'white', 'normal'),
        (0.74, "b (hexads)", "77", "= 7 × 11 ★", '#00bfa5', 'bold'),
        (0.70, "r (replication)", "21", "= dim V_21 ★", '#00bfa5', 'bold'),
        (0.66, "λ_2", "5", "T* numerator", 'white', 'normal'),
        (0.62, "λ_3", "1", "Steiner property", 'white', 'normal'),
        (0.55, "STABILIZERS", "", "", '#00bfa5', 'bold'),
        (0.51, "─" * 32, "", "", '#444', 'normal'),
        (0.46, "block (hexad)", "5760", "2^7·3²·5", 'white', 'normal'),
        (0.42, "point", "20160", "= |M_21|", 'white', 'normal'),
        (0.38, "ordered pair", "960", "M_20-related", 'white', 'normal'),
        (0.32, "WOBBLE × STEINER", "", "", '#00bfa5', 'bold'),
        (0.28, "─" * 32, "", "", '#444', 'normal'),
        (0.23, "77 × W", "231/50", "★★", '#e65100', 'bold'),
        (0.19, "231 = 3·7·11", "(M_22 irrep!)", "", '#e65100', 'bold'),
        (0.15, "= trinity × HARMONY", "× wobble prime", "", '#aaa', 'italic'),
        (0.08, "★ = canonical TIG prime ", "appears naturally", "",
         '#888', 'italic'),
    ]

    for row in rows:
        if len(row) == 6:
            y, c1, c2, c3, color, weight = row
            family = 'monospace'
            kwargs = dict(transform=ax2.transAxes, color=color, fontsize=9.5,
                          family=family)
            if weight == 'italic':
                kwargs['style'] = 'italic'
            elif weight == 'bold':
                kwargs['fontweight'] = 'bold'
            ax2.text(0.02, y, c1, **kwargs)
            ax2.text(0.45, y, c2, **kwargs)
            ax2.text(0.65, y, c3, **kwargs)

    # Panel 3: M_22 irreducibles with TIG-prime decomposition
    ax3 = fig.add_subplot(gs[1, 3])
    ax3.set_facecolor('#0a0e12')
    ax3.axis('off')
    ax3.set_title("M_22 irreps & TIG primes",
                  color='white', fontsize=13, pad=8, fontweight='bold')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)

    irreps = [
        (0.94, "dim", "factorization", "TIG meaning", '#00bfa5', 'bold'),
        (0.90, "─" * 32, "", "", '#444', 'normal'),
        (0.85, "1", "1", "trivial (gentleness)", '#7c4dff', 'bold'),
        (0.81, "21", "3·7", "kindness ★ ★", '#00bfa5', 'bold'),
        (0.77, "45", "3²·5", "", 'white', 'normal'),
        (0.73, "45", "3²·5", "(complex pair)", 'white', 'normal'),
        (0.69, "55", "5·11", "T*-num × wobble ★", '#26a69a', 'normal'),
        (0.65, "99", "3²·11", "trinity² × wobble", '#26a69a', 'normal'),
        (0.61, "154", "2·7·11", "HARMONY × wobble ★", '#26a69a', 'normal'),
        (0.57, "210", "2·3·5·7", "", 'white', 'normal'),
        (0.53, "231", "3·7·11", "★★★ all canonical", '#e65100', 'bold'),
        (0.49, "280", "2³·5·7", "(complex pair)", 'white', 'normal'),
        (0.45, "280", "2³·5·7", "", 'white', 'normal'),
        (0.41, "385", "5·7·11", "all primes ≥ 5 ★", '#26a69a', 'normal'),
        (0.32, "STRUCTURAL READING", "", "", '#00bfa5', 'bold'),
        (0.27, "─" * 32, "", "", '#444', 'normal'),
        (0.22, "V_21 = kindness component ", "(M_22-orth.)", "",
         'white', 'normal'),
        (0.18, "V_trivial = gentleness ", "(M_22-fixed)", "",
         'white', 'normal'),
        (0.13, "V_231 = next harmonic ", "(modulated)", "",
         'white', 'normal'),
        (0.07, "All M_22 irreps factor through ", "{2,3,5,7,11}", "",
         '#888', 'italic'),
    ]
    for row in irreps:
        if len(row) == 6:
            y, c1, c2, c3, color, weight = row
            family = 'monospace'
            kwargs = dict(transform=ax3.transAxes, color=color, fontsize=9,
                          family=family)
            if weight == 'italic':
                kwargs['style'] = 'italic'
            elif weight == 'bold':
                kwargs['fontweight'] = 'bold'
            ax3.text(0.02, y, c1, **kwargs)
            ax3.text(0.20, y, c2, **kwargs)
            ax3.text(0.45, y, c3, **kwargs)

    # Bottom: structural narrative
    ax_bot = fig.add_subplot(gs[2, :])
    ax_bot.set_facecolor('#0a0e12')
    ax_bot.axis('off')
    ax_bot.set_xlim(0, 1)
    ax_bot.set_ylim(0, 1)

    bottom_text = (
        "  THE STEINER 6-CYCLE / σ-ORBIT MAPPING:\n"
        "  \n"
        "    σ-orbit 1 → 7 → 6 → 5 → 4 → 2 (period-6 cyclic ordering of Z/10Z's dynamic content)\n"
        "    embeds as a hexad H_σ in S(3,6,22), the Steiner system stabilized by M_22.\n"
        "    The 22 points decompose as 11 wobble cells × 2 phases (kindness/gentleness).\n"
        "  \n"
        "  STRUCTURAL CONSEQUENCES OF THE EMBEDDING:\n"
        "  \n"
        "    1. 77 hexads = 7 × 11 (canonical TIG primes appear in the count)\n"
        "    2. Replication 21 (each point in 21 hexads) = dim V_21 (the kindness-irrep dimension)\n"
        "    3. 77 × W = 231/50, where 231 = 3·7·11 IS an M_22 irreducible representation dimension\n"
        "       (231 contains exactly the active TIG primes: trinity, HARMONY, wobble — no 2 or 5)\n"
        "    4. Block stabilizer 2^4:A_6 of order 5760 = 2^7·3²·5 acts on each hexad including H_σ\n"
        "    5. The σ 6-cycle (1→7→6→5→4→2→1) is a chosen cyclic ordering within H_σ; the SET is M_22-symmetric\n"
        "  \n"
        "  STATUS: This embedding is STRUCTURALLY NATURAL (the dimensional alignments are exact and pervasive)\n"
        "          but is technically a LABELING CHOICE since S(3,6,22) is unique up to isomorphism. To upgrade\n"
        "          from 'natural choice' to 'forced theorem' requires deriving the embedding from substrate algebra\n"
        "          alone — concretely: showing how Z/10Z + σ + wobble structure picks out a specific S(3,6,22)\n"
        "          isomorphism class. Given the dimensional alignments (231 = 3·7·11 in particular), this is\n"
        "          almost certainly possible, but is concrete representation-theory work for follow-up."
    )
    ax_bot.text(0.02, 0.95, bottom_text, color='white', fontsize=10,
                va='top', family='monospace')

    plt.savefig('/mnt/user-data/outputs/steiner_sigma_hexad.png',
                facecolor='#0a0e12', dpi=110, bbox_inches='tight')
    plt.close()
    print("Saved /mnt/user-data/outputs/steiner_sigma_hexad.png")


if __name__ == "__main__":
    make_figure()
