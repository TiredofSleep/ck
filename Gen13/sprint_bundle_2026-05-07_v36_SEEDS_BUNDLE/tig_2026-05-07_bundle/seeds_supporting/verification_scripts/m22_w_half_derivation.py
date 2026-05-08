"""
THE M_22 / W/2 DERIVATION VISUALIZATION
========================================

Three-layer diagram showing the W/2 derivation chain:

  SUBSTRATE   →   22-SKELETON   →   COSMIC
  (Z/10Z)         (M_22 group)       (Ω_DE)
  
  Wobble W = 3/50    Steiner S(3,6,22)   Ω_DE = T* − W/2
  kindness/gentleness 77 blocks           = 479/700 = 0.6843
                                          matches Planck 2018 (0.06%)

Locked theorem: pre-cancellation denominator of ζ_TIG(5/7) = 7^8 × |M_22|
Suggestive chain: kindness × duty(1/2) gives the cosmic-scale factor of 2
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def make_diagram():
    fig = plt.figure(figsize=(18, 12), facecolor='#0a0e12')
    fig.subplots_adjust(left=0.03, right=0.97, top=0.95, bottom=0.03)
    ax = fig.add_subplot(111)
    ax.set_facecolor('#0a0e12')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(6, 9.6, "THE M_22 / W/2 DERIVATION CHAIN",
            ha='center', va='top', color='white',
            fontsize=22, fontweight='bold')
    ax.text(6, 9.10, "From substrate algebra through the 22-skeleton to cosmic Ω_DE",
            ha='center', va='top', color='#aaa', fontsize=12, style='italic')

    # ==========================================================================
    # Layer 1: SUBSTRATE (left)
    # ==========================================================================
    sub_box = FancyBboxPatch((0.4, 4.5), 3.0, 3.5,
                              boxstyle="round,pad=0.1", linewidth=2,
                              edgecolor='#7c4dff', facecolor='#1a0e2a')
    ax.add_patch(sub_box)
    ax.text(1.9, 7.7, "SUBSTRATE", ha='center', color='#7c4dff',
            fontsize=14, fontweight='bold')
    ax.text(1.9, 7.4, "(Z/10Z + σ + wobble)", ha='center', color='#aaa',
            fontsize=10, style='italic')

    sub_text = (
        "WOBBLE STRUCTURE:\n\n"
        "  kindness   W_k = 3/50\n"
        "  gentleness W_g = 22/50\n\n"
        "  W_k + W_g  = 25/50 = 1/2\n"
        "                (full cycle)\n\n"
        "Note: 22 in W_g IS the\n"
        "cardinality of M_22's action.\n"
        "Numerical alignment is exact."
    )
    ax.text(0.6, 7.1, sub_text, va='top', color='white',
            fontsize=10, family='monospace')

    # ==========================================================================
    # Layer 2: M_22 SKELETON (center)
    # ==========================================================================
    m22_box = FancyBboxPatch((4.3, 4.5), 3.4, 3.5,
                              boxstyle="round,pad=0.1", linewidth=2,
                              edgecolor='#00bfa5', facecolor='#0a2a26')
    ax.add_patch(m22_box)
    ax.text(6.0, 7.7, "22-SKELETON", ha='center', color='#00bfa5',
            fontsize=14, fontweight='bold')
    ax.text(6.0, 7.4, "(Mathieu group M_22)", ha='center', color='#aaa',
            fontsize=10, style='italic')

    m22_text = (
        "STRUCTURE:\n\n"
        "  |M_22| = 2^7 · 3^2 · 5 · 7 · 11\n"
        "         = 443,520\n"
        "         = 10080 × 44\n"
        "                ↑       ↑\n"
        "                ζ_TIG  CROSS_CYCLE\n"
        "                norm.    (D17)\n\n"
        "Acts on 22 points (the\n"
        "22-shell skeleton from\n"
        "userMemories nested tori).\n\n"
        "Stabilizes Steiner S(3,6,22)\n"
        "with 77 = 7·11 blocks."
    )
    ax.text(4.5, 7.1, m22_text, va='top', color='white',
            fontsize=10, family='monospace')

    # ==========================================================================
    # Layer 3: COSMIC (right)
    # ==========================================================================
    cos_box = FancyBboxPatch((8.6, 4.5), 3.0, 3.5,
                              boxstyle="round,pad=0.1", linewidth=2,
                              edgecolor='#e65100', facecolor='#2a1500')
    ax.add_patch(cos_box)
    ax.text(10.1, 7.7, "COSMIC", ha='center', color='#e65100',
            fontsize=14, fontweight='bold')
    ax.text(10.1, 7.4, "(Ω_DE, ω(z))", ha='center', color='#aaa',
            fontsize=10, style='italic')

    cos_text = (
        "PREDICTION:\n\n"
        "  Ω_DE = T* − W/2\n"
        "       = 5/7 − 3/100\n"
        "       = 479/700\n"
        "       ≈ 0.6843\n\n"
        "OBSERVED (Planck 2018):\n"
        "  Ω_Λ = 0.6847 ± 0.0073\n\n"
        "MATCH: 0.06% (0.06σ)\n\n"
        "Bonus: Ω_M = 1 − Ω_DE\n"
        "          = 221/700\n"
        "          ≈ 0.3157\n"
        "  Planck: 0.315 ± 0.007 ✓"
    )
    ax.text(8.8, 7.1, cos_text, va='top', color='white',
            fontsize=10, family='monospace')

    # ==========================================================================
    # Arrows between layers
    # ==========================================================================
    arrow1 = FancyArrowPatch((3.5, 6.2), (4.2, 6.2),
                              arrowstyle='->', mutation_scale=20,
                              color='white', linewidth=2)
    ax.add_patch(arrow1)
    ax.text(3.85, 6.45, "absorb\n22-resonant\ngentleness",
            ha='center', va='bottom', color='white', fontsize=8.5)

    arrow2 = FancyArrowPatch((7.7, 6.2), (8.5, 6.2),
                              arrowstyle='->', mutation_scale=20,
                              color='white', linewidth=2)
    ax.add_patch(arrow2)
    ax.text(8.1, 6.45, "project\nresidual\nkindness",
            ha='center', va='bottom', color='white', fontsize=8.5)

    # ==========================================================================
    # The W/2 derivation chain (bottom)
    # ==========================================================================
    chain_box = FancyBboxPatch((0.5, 0.4), 11.0, 3.7,
                                boxstyle="round,pad=0.1", linewidth=2,
                                edgecolor='#444', facecolor='#0e1418')
    ax.add_patch(chain_box)
    ax.text(6, 3.85, "THE W/2 DERIVATION CHAIN",
            ha='center', color='white', fontsize=14, fontweight='bold')

    # 5 columns showing the chain
    columns = [
        (1.4, "STEP 1\nSubstrate",
         "Wobble has\nkindness 3/50\n+ gentleness 22/50",
         "#7c4dff"),
        (3.4, "STEP 2\nIdentify",
         "22 in gentleness\n= |M_22|'s action\non 22-skeleton",
         "#00bfa5"),
        (5.4, "STEP 3\nFilter",
         "Gentleness is\nM_22-resonant →\nabsorbed by skeleton",
         "#26a69a"),
        (7.4, "STEP 4\nAverage",
         "Kindness × duty(1/2)\n= 3/50 × 1/2\n= 3/100 = W/2",
         "#42a5f5"),
        (9.4, "STEP 5\nMatch",
         "T* − W/2 = 479/700\n= 0.6843\nPlanck: 0.6847 ✓",
         "#e65100"),
    ]
    
    for x, header, body, color in columns:
        ax.text(x, 3.35, header, ha='center', color=color,
                fontsize=10, fontweight='bold')
        ax.text(x, 2.3, body, ha='center', color='white',
                fontsize=9, family='monospace')

    # Bottom: Rigor assessment
    ax.text(6, 1.5, "RIGOR ASSESSMENT",
            ha='center', color='white', fontsize=11, fontweight='bold')

    locked_text = (
        "✓ LOCKED: Pre-cancellation denominator of ζ_TIG(T*) = 7^8 × |M_22|\n"
        "✓ LOCKED: (a-49)/(-44) = 1 ONLY at a=5 — uniquely cleanest factorization at T*\n"
        "✓ LOCKED: Empirical match Ω_DE = 0.6843 vs Planck 0.6847 (0.06%)"
    )
    ax.text(0.8, 1.2, locked_text, color='#00bfa5', fontsize=9, family='monospace', va='top')

    sugg_text = (
        "△ SUGGESTIVE: 'M_22 absorbs gentleness' — needs formal projection operator\n"
        "△ SUGGESTIVE: Duty cycle 1/2 — needs time-evolution integral derivation"
    )
    ax.text(0.8, 0.7, sugg_text, color='#ffa726', fontsize=9, family='monospace', va='top')

    plt.savefig('/mnt/user-data/outputs/m22_w_half_derivation.png',
                facecolor='#0a0e12', dpi=110, bbox_inches='tight')
    plt.close()
    print("Saved /mnt/user-data/outputs/m22_w_half_derivation.png")


if __name__ == "__main__":
    make_diagram()
