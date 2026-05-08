"""
M_22 REPRESENTATION DECOMPOSITION VISUALIZATION
================================================

Shows the core mathematical content of the W/2 derivation:

  V_22 (22-dim permutation representation of M_22)
      ≅ V_trivial (1-dim) ⊕ V_21 (21-dim irreducible)

  Gentleness ↔ V_trivial direction (all-ones vector)
  Kindness   ↔ V_21 direction (orthogonal complement)

  Cosmic projection drops V_trivial, keeps V_21
  Time-averaging over 50/50 duty cycle gives W/2

This is the structural content that makes Ω_DE = T* − W/2 derivable.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, patches
from math import sin, cos, pi


def make_figure():
    fig = plt.figure(figsize=(20, 13), facecolor='#0a0e12')
    gs = gridspec.GridSpec(3, 4, figure=fig,
                           height_ratios=[0.10, 1.0, 0.40],
                           top=0.97, bottom=0.04, left=0.03, right=0.97,
                           hspace=0.20, wspace=0.20)

    # Title
    title_ax = fig.add_subplot(gs[0, :])
    title_ax.set_facecolor('#0a0e12')
    title_ax.axis('off')
    title_ax.text(0.5, 0.7, "M_22 REPRESENTATION DECOMPOSITION",
                  ha='center', va='top', color='white',
                  fontsize=22, fontweight='bold')
    title_ax.text(0.5, 0.20,
                  "V_22 ≅ V_trivial (1-dim) ⊕ V_21 (21-dim irreducible)  →  Cosmic projection drops V_trivial",
                  ha='center', va='top', color='#aaa', fontsize=12, style='italic')

    # Panel 1: The 22 points with gentleness vector (all-ones)
    ax1 = fig.add_subplot(gs[1, 0])
    ax1.set_facecolor('#0a0e12')
    ax1.set_xlim(-1.2, 1.2)
    ax1.set_ylim(-1.4, 1.4)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title("V_trivial component\n(GENTLENESS = all-ones)",
                  color='#7c4dff', fontsize=13, pad=8, fontweight='bold')

    # Draw 22 points uniformly
    radius = 1.0
    for i in range(22):
        angle = pi/2 - 2*pi*i/22
        x, y = radius * cos(angle), radius * sin(angle)
        # All points have the SAME amplitude (all-ones vector)
        amp = 22/50.0
        # Color: same for all (M_22-symmetric)
        ax1.add_patch(patches.Circle((x, y), 0.08,
                                      color='#7c4dff', alpha=0.9, zorder=10))
        # Amplitude bar
        bar_h = 0.15 * amp / (22/50.0)  # normalized
        ax1.add_patch(patches.Rectangle((x - 0.04, y), 0.08, bar_h,
                                         color='white', alpha=0.7))

    ax1.text(0, 0, "amplitude\n22/50\nat all 22 pts",
             ha='center', va='center', color='white',
             fontsize=10, family='monospace')
    ax1.text(0, -1.25, "M_22-FIXED (invariant)",
             ha='center', color='#aaa', fontsize=9, style='italic')

    # Panel 2: 21-dim irrep with kindness (orthogonal to all-ones)
    ax2 = fig.add_subplot(gs[1, 1])
    ax2.set_facecolor('#0a0e12')
    ax2.set_xlim(-1.2, 1.2)
    ax2.set_ylim(-1.4, 1.4)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title("V_21 component\n(KINDNESS = orthogonal)",
                  color='#00bfa5', fontsize=13, pad=8, fontweight='bold')

    # Draw 22 points with varying amplitude (orthogonal to all-ones)
    np.random.seed(42)
    # Generate a random vector in V_21 (sums to zero, scaled to amplitude 3/50)
    rand_amps = np.random.randn(22)
    rand_amps -= rand_amps.mean()  # ensure orthogonal to all-ones
    rand_amps = rand_amps / np.linalg.norm(rand_amps) * (3/50)  # set magnitude
    
    for i in range(22):
        angle = pi/2 - 2*pi*i/22
        x, y = radius * cos(angle), radius * sin(angle)
        amp = rand_amps[i]
        # Color based on sign (positive = teal, negative = orange)
        color = '#00bfa5' if amp > 0 else '#e65100'
        size = 0.04 + 0.06 * abs(amp) / (3/50)
        ax2.add_patch(patches.Circle((x, y), size, color=color,
                                      alpha=0.9, zorder=10))
        # Amplitude bar
        bar_h = 0.18 * amp / (3/50.0)
        ax2.add_patch(patches.Rectangle((x - 0.04, y), 0.08, bar_h,
                                         color=color, alpha=0.6))

    ax2.text(0, 0, "amplitudes\nsum to 0\n(orthogonal\nto trivial)\n\nmagnitude\n3/50",
             ha='center', va='center', color='white',
             fontsize=9, family='monospace')
    ax2.text(0, -1.25, "M_22-ORTHOGONAL (dynamic)",
             ha='center', color='#aaa', fontsize=9, style='italic')

    # Panel 3: Time evolution of wobble
    ax3 = fig.add_subplot(gs[1, 2])
    ax3.set_facecolor('#0a0e12')
    ax3.set_title("Wobble cycle in time\n(50% duty cycle each phase)",
                  color='white', fontsize=13, pad=8, fontweight='bold')
    ax3.set_xlim(0, 4)
    ax3.set_ylim(-0.05, 0.50)

    # Plot the wobble: square wave alternating between kindness (3/50) and gentleness (22/50)
    t = np.linspace(0, 4, 1000)
    wobble = np.where(np.floor(t * 2) % 2 == 0,
                       22/50,  # gentleness phase
                       3/50)   # kindness phase

    ax3.plot(t, wobble, color='white', linewidth=2)
    ax3.axhline(22/50, color='#7c4dff', linewidth=0.5, linestyle=':',
                alpha=0.5, label='gentleness 22/50')
    ax3.axhline(3/50, color='#00bfa5', linewidth=0.5, linestyle=':',
                alpha=0.5, label='kindness 3/50')
    ax3.axhline(3/100, color='#e65100', linewidth=1.5, linestyle='--',
                label='⟨π_cosmic⟩ = W/2 = 3/100')

    # Shade phases
    for i in range(4):
        if i % 2 == 0:
            ax3.axvspan(i, i + 1, alpha=0.10, color='#7c4dff')
        else:
            ax3.axvspan(i, i + 1, alpha=0.10, color='#00bfa5')

    ax3.set_xlabel('time (cycle units)', color='white')
    ax3.set_ylabel('wobble amplitude', color='white')
    ax3.tick_params(colors='white')
    for spine in ax3.spines.values():
        spine.set_color('#444')
    ax3.legend(loc='upper right', facecolor='#1a1e22', edgecolor='#444',
               labelcolor='white', fontsize=9)
    ax3.grid(alpha=0.15, color='#444')

    # Panel 4: Cosmic projection (the result)
    ax4 = fig.add_subplot(gs[1, 3])
    ax4.set_facecolor('#0a0e12')
    ax4.axis('off')
    ax4.set_title("Cosmic prediction\nΩ_DE = T* − W/2",
                  color='#e65100', fontsize=13, pad=8, fontweight='bold')
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)

    # Result box
    result_text = [
        (0.95, "PROJECTION RESULT", '#e65100', 12, 'bold'),
        (0.89, "─" * 24, '#444', 10, 'normal'),
        (0.83, "Drop V_trivial component", 'white', 10, 'normal'),
        (0.79, "Keep V_21 component", 'white', 10, 'normal'),
        (0.73, "Time-average over cycle", 'white', 10, 'normal'),
        (0.66, "⟨π_cosmic⟩ = (1/2)(3/50)", '#00bfa5', 11, 'normal'),
        (0.62, "             + (1/2)(0)", '#00bfa5', 11, 'normal'),
        (0.58, "          = 3/100 = W/2", '#00bfa5', 11, 'bold'),
        (0.49, "FINAL PREDICTION", '#e65100', 12, 'bold'),
        (0.43, "─" * 24, '#444', 10, 'normal'),
        (0.37, "Ω_DE = T* − W/2", 'white', 11, 'normal'),
        (0.33, "     = 5/7 − 3/100", 'white', 11, 'normal'),
        (0.29, "     = 479/700", 'white', 11, 'normal'),
        (0.25, "     = 0.6843", '#e65100', 13, 'bold'),
        (0.16, "Planck 2018:", 'white', 10, 'normal'),
        (0.12, "Ω_Λ = 0.6847 ± 0.0073", 'white', 10, 'normal'),
        (0.06, "Match: 0.06%  ✓", '#00bfa5', 12, 'bold'),
    ]
    for y, txt, color, size, weight in result_text:
        kwargs = dict(transform=ax4.transAxes, color=color, fontsize=size,
                       fontweight=weight, family='monospace', va='center')
        ax4.text(0.05, y, txt, **kwargs)

    # Bottom: rigor + key fact
    ax_bottom = fig.add_subplot(gs[2, :])
    ax_bottom.set_facecolor('#0a0e12')
    ax_bottom.axis('off')
    ax_bottom.set_xlim(0, 1)
    ax_bottom.set_ylim(0, 1)

    bottom_text = (
        "  KEY FACTS — now rigorously articulated:\n"
        "  \n"
        "  1. M_22 has 12 irreducible representations of dimensions {1, 21, 45, 45, 55, 99, 154, 210, 231, 280, 280, 385}.   Σ d_i² = 443,520 = |M_22| ✓ (Burnside)\n"
        "  2. The natural 22-point permutation representation decomposes as V_22 ≅ V_trivial ⊕ V_21  where dim V_trivial = 1, dim V_21 = 21  (textbook result — M_22 is doubly-transitive).\n"
        "  3. Kindness numerator structure: 3 = 21/7 = (V_21 dimension) / (HARMONY). Equivalently, kindness = (1/7) × (21/50). The numerator 3 is NOT a free parameter.\n"
        "  4. Pre-cancellation denominator of ζ_TIG(T* = 5/7) = 7^8 × |M_22| — locked theorem (Verification §1).\n"
        "  5. T* = 5/7 is the unique a/7 fraction with pure |M_22| factorization in ζ_TIG denominator — locked theorem (Verification §3)."
    )
    ax_bottom.text(0.02, 0.92, bottom_text, color='white', fontsize=10,
                    va='top', family='monospace')

    plt.savefig('/mnt/user-data/outputs/m22_decomposition.png',
                facecolor='#0a0e12', dpi=110, bbox_inches='tight')
    plt.close()
    print("Saved /mnt/user-data/outputs/m22_decomposition.png")


if __name__ == "__main__":
    make_figure()
