"""
ck_sinc_demo.py -- 30-Second Sinc2 Pre-Echo Demo
=================================================
Brayden Ross Sanders / 7Site LLC
DOI: 10.5281/zenodo.18852047

Plots the harmonic pre-echo resonance field R(k, f) for several semiprimes,
showing convergence to sinc2(k/f) as f -> infinity and the forced null at k=p.

Run:  python ck_sinc_demo.py
Requires: matplotlib (pip install matplotlib)
"""

import math
import sys

PI = math.pi


def sinc2(t):
    if abs(t) < 1e-15:
        return 1.0
    v = math.sin(PI * t) / (PI * t)
    return v * v


def R(k, f):
    """Harmonic pre-echo resonance R(k, f) = sin2(pi*k/f) / (k2 * sin2(pi/f))."""
    if k == 0:
        return 1.0
    num = math.sin(PI * k / f) ** 2
    den = (k ** 2) * (math.sin(PI / f) ** 2)
    if den == 0:
        return 0.0
    return num / den


def next_prime(n):
    def is_prime(x):
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        i = 3
        while i * i <= x:
            if x % i == 0:
                return False
            i += 2
        return True
    k = n + 1
    while not is_prime(k):
        k += 1
    return k


try:
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def demo_text():
    """Text-mode fallback: print the key values."""
    print("\nSinc2 Pre-Echo Demo (text mode -- install matplotlib for plot)")
    print("=" * 60)

    MONTGOMERY = sinc2(0.5)
    print(f"\nUniversal Sidelobe Amplitude: sinc2(1/2) = 4/pi2 = {MONTGOMERY:.8f}")
    print(f"Scale-free pre-echo floor:    sinc2(0.1)        = {sinc2(0.1):.8f}")
    print(f"Montgomery partition:         R(x) + R2(x) = {MONTGOMERY + (1-MONTGOMERY):.15f}")

    cases = [
        (15, 3, 5),
        (35, 5, 7),
        (437, 19, 23),
        (9703, 97, 100+3),
    ]

    for b, p, q in cases:
        q = next_prime(p)
        print(f"\n  b={p*q} = {p}x{q}  (p={p})")
        print(f"  {'k':>5}  {'R(k,p)':>10}  {'sinc2(k/p)':>12}  {'error':>10}")
        for k in range(1, min(p + 3, 20)):
            rv = R(k, p)
            sv = sinc2(k / p)
            marker = " <- First-G NULL" if k == p else ""
            print(f"  {k:>5}  {rv:>10.6f}  {sv:>12.6f}  {abs(rv-sv):>10.2e}{marker}")


def demo_plot():
    """Full matplotlib plot."""
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor('#0f0f1a')
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.42, wspace=0.35)

    dark_bg = '#0f0f1a'
    panel_bg = '#161625'
    text_color = '#e8e8f0'
    grid_color = '#2a2a40'

    # Color scheme per semiprime
    colors = ['#4fc3f7', '#81c784', '#ffb74d', '#f06292', '#b39ddb', '#80cbc4']

    # ------------------------------------------------------------------ #
    # Panel 1: b=15 (p=3, q=5) -- the simplest case
    ax1 = fig.add_subplot(gs[0, 0])
    p, q = 3, 5
    ks = list(range(1, q + 2))
    rv = [R(k, p) for k in ks]
    t_cont = [i * 0.01 for i in range(1, int(q / p * 100) + 10)]
    sv = [sinc2(t * p / p) for t in t_cont]
    # Continuum sinc2 on same k axis
    k_cont = [t for t in [i * 0.05 for i in range(1, 150)]]
    sv_cont = [sinc2(k / p) for k in k_cont]

    ax1.set_facecolor(panel_bg)
    ax1.bar(ks, rv, color=colors[0], alpha=0.75, width=0.5, label='R(k, p)', zorder=3)
    ax1.plot(k_cont, sv_cont, color='white', alpha=0.5, linewidth=1.2,
             linestyle='--', label='sinc2(k/p)', zorder=2)
    ax1.axvline(p, color='#ff5252', linewidth=2.0, linestyle='-', alpha=0.9,
                label=f'k = p = {p} (null)', zorder=4)
    ax1.set_title(f'b = {p*q} = {p}×{q}  (p={p})', color=text_color, fontsize=10, pad=8)
    ax1.set_xlabel('k', color=text_color, fontsize=9)
    ax1.set_ylabel('R(k, p)', color=text_color, fontsize=9)
    ax1.tick_params(colors=text_color, labelsize=8)
    ax1.spines[:].set_color(grid_color)
    ax1.yaxis.grid(True, color=grid_color, alpha=0.5, zorder=0)
    ax1.legend(fontsize=7, facecolor=dark_bg, labelcolor=text_color, framealpha=0.7)
    ax1.set_xlim(0.3, q + 1.5)
    ax1.set_ylim(-0.05, 1.15)

    # ------------------------------------------------------------------ #
    # Panel 2: b=35 (p=5, q=7) -- the T*=5/7 world
    ax2 = fig.add_subplot(gs[0, 1])
    p, q = 5, 7
    ks = list(range(1, q + 2))
    rv = [R(k, p) for k in ks]
    k_cont = [i * 0.05 for i in range(1, int((q + 2) / 0.05))]
    sv_cont = [sinc2(k / p) for k in k_cont]

    ax2.set_facecolor(panel_bg)
    ax2.bar(ks, rv, color=colors[1], alpha=0.75, width=0.5, label='R(k, p)', zorder=3)
    ax2.plot(k_cont, sv_cont, color='white', alpha=0.5, linewidth=1.2,
             linestyle='--', label='sinc2(k/p)', zorder=2)
    ax2.axvline(p, color='#ff5252', linewidth=2.0, linestyle='-', alpha=0.9,
                label=f'k = p = {p} (null)', zorder=4)
    # T* marker
    t_star = 5 / 7
    ax2.axhline(t_star, color='#ffd54f', linewidth=1.3, linestyle=':', alpha=0.8,
                label=f'T* = 5/7 = {t_star:.4f}', zorder=3)
    ax2.set_title(f'b = {p*q} = {p}×{q}  (T* = 5/7)', color=text_color, fontsize=10, pad=8)
    ax2.set_xlabel('k', color=text_color, fontsize=9)
    ax2.tick_params(colors=text_color, labelsize=8)
    ax2.spines[:].set_color(grid_color)
    ax2.yaxis.grid(True, color=grid_color, alpha=0.5, zorder=0)
    ax2.legend(fontsize=7, facecolor=dark_bg, labelcolor=text_color, framealpha=0.7)
    ax2.set_xlim(0.3, q + 1.5)
    ax2.set_ylim(-0.05, 1.15)

    # ------------------------------------------------------------------ #
    # Panel 3: Convergence -- R(floor(t*p), p) -> sinc2(t) as p grows
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor(panel_bg)

    MONTGOMERY = sinc2(0.5)
    primes = [5, 11, 23, 53, 97, 199, 997]
    t_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    t_colors = ['#ef9a9a', '#ffcc80', '#a5d6a7', '#80deea', '#b39ddb']

    for t, tc in zip(t_values, t_colors):
        target = sinc2(t)
        errors = []
        for p in primes:
            k = max(1, round(t * p))
            val = R(k, p)
            errors.append(abs(val - target))
        ax3.semilogy(primes, errors, 'o-', color=tc, alpha=0.85,
                     linewidth=1.4, markersize=4, label=f't={t}')

    # 1/p reference line
    ref = [1.0 / p for p in primes]
    ax3.semilogy(primes, ref, 'w--', alpha=0.3, linewidth=1.0, label='O(1/p)')

    ax3.set_title('Convergence R(tp, p) → sinc²(t)', color=text_color, fontsize=10, pad=8)
    ax3.set_xlabel('Prime p', color=text_color, fontsize=9)
    ax3.set_ylabel('|R − sinc²(t)|', color=text_color, fontsize=9)
    ax3.tick_params(colors=text_color, labelsize=8)
    ax3.spines[:].set_color(grid_color)
    ax3.yaxis.grid(True, color=grid_color, alpha=0.3, zorder=0)
    ax3.legend(fontsize=7, facecolor=dark_bg, labelcolor=text_color, framealpha=0.7,
               ncol=2)

    # ------------------------------------------------------------------ #
    # Panel 4: Full sinc2 curve with Montgomery bridge
    ax4 = fig.add_subplot(gs[1, 0:2])
    ax4.set_facecolor(panel_bg)

    t_vals = [i * 0.005 for i in range(1, 401)]
    r_vals = [sinc2(t) for t in t_vals]
    r2_vals = [1.0 - sinc2(t) for t in t_vals]

    ax4.fill_between(t_vals, r_vals, alpha=0.25, color='#4fc3f7', label='R(x) = sinc²(x)  [TIG field]')
    ax4.fill_between(t_vals, r2_vals, alpha=0.25, color='#f06292', label='R₂(x) = 1 − sinc²(x)  [Montgomery pair correlation]')
    ax4.plot(t_vals, r_vals, color='#4fc3f7', linewidth=2.0)
    ax4.plot(t_vals, r2_vals, color='#f06292', linewidth=2.0)

    # Mark 4/pi2 at t=0.5
    ax4.axvline(0.5, color='#ffd54f', linewidth=1.3, linestyle='--', alpha=0.8)
    ax4.axhline(MONTGOMERY, color='#ffd54f', linewidth=1.0, linestyle=':', alpha=0.6)
    ax4.annotate(f'4/π² = {MONTGOMERY:.4f}', xy=(0.5, MONTGOMERY),
                 xytext=(0.62, MONTGOMERY + 0.07),
                 color='#ffd54f', fontsize=8.5,
                 arrowprops=dict(arrowstyle='->', color='#ffd54f', lw=1.0))

    # R + R2 = 1 annotation
    ax4.text(0.5, 1.03, 'R(x) + R₂(x) = 1   (spectral partition of unity)',
             ha='center', va='bottom', color=text_color, fontsize=9,
             transform=ax4.get_xaxis_transform())

    ax4.set_title('Montgomery Bridge: sinc²(x) [TIG] and 1 − sinc²(x) [Montgomery 1973] are spectral duals',
                  color=text_color, fontsize=10, pad=8)
    ax4.set_xlabel('x  (t = k/p, or normalized zero spacing u)', color=text_color, fontsize=9)
    ax4.set_ylabel('Amplitude', color=text_color, fontsize=9)
    ax4.tick_params(colors=text_color, labelsize=8)
    ax4.spines[:].set_color(grid_color)
    ax4.yaxis.grid(True, color=grid_color, alpha=0.4, zorder=0)
    ax4.legend(fontsize=8.5, facecolor=dark_bg, labelcolor=text_color, framealpha=0.7,
               loc='upper right')
    ax4.set_xlim(0, 2.0)
    ax4.set_ylim(-0.05, 1.15)

    # ------------------------------------------------------------------ #
    # Panel 5: D1 sign flip at k=p
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.set_facecolor(panel_bg)

    p, q = 19, 23
    b = p * q
    ks_d1 = list(range(1, q + 1))
    d1_vals = [R(k + 1, p) - R(k, p) for k in ks_d1]
    bar_colors = ['#ef5350' if v < 0 else '#66bb6a' for v in d1_vals]

    ax5.bar(ks_d1, d1_vals, color=bar_colors, alpha=0.8, width=0.6, zorder=3)
    ax5.axvline(p, color='#ffd54f', linewidth=2.0, linestyle='-', alpha=0.9,
                label=f'k = p = {p}  (sign flip)', zorder=4)
    ax5.axhline(0, color='white', linewidth=0.7, alpha=0.4)

    ax5.set_title(f'D1 = R(k+1)−R(k)  [b={b}, p={p}]\nRed < 0 (approach), Green > 0 (recovery)',
                  color=text_color, fontsize=9, pad=6)
    ax5.set_xlabel('k', color=text_color, fontsize=9)
    ax5.set_ylabel('D1(k)', color=text_color, fontsize=9)
    ax5.tick_params(colors=text_color, labelsize=8)
    ax5.spines[:].set_color(grid_color)
    ax5.yaxis.grid(True, color=grid_color, alpha=0.4, zorder=0)
    ax5.legend(fontsize=8, facecolor=dark_bg, labelcolor=text_color, framealpha=0.7)

    # ------------------------------------------------------------------ #
    # Title
    fig.suptitle(
        'CK — Sinc² Spectral Field in Prime Arithmetic\n'
        'R(k, f) → sinc²(k/f)  as f → ∞   |   R(x) + R₂(x) = 1  (Montgomery Bridge)\n'
        'DOI: 10.5281/zenodo.18852047  |  github.com/TiredofSleep/ck',
        color=text_color, fontsize=11, y=0.98, va='top',
        fontweight='bold'
    )

    plt.savefig('sinc2_demo.png', dpi=150, bbox_inches='tight',
                facecolor=dark_bg, edgecolor='none')
    print("Saved: sinc2_demo.png")
    plt.show()


if __name__ == '__main__':
    if HAS_MPL:
        demo_plot()
    else:
        print("matplotlib not found. Running text demo.\n"
              "Install with: pip install matplotlib")
        demo_text()

    # Always print the key constants
    MONTGOMERY = sinc2(0.5)
    print(f"\nKey constants:")
    print(f"  4/pi2 = sinc2(1/2) = {MONTGOMERY:.10f}")
    print(f"  sinc2(0.1)         = {sinc2(0.1):.10f}")
    print(f"  T* = 5/7           = {5/7:.10f}")
    print(f"  R + R2 = 1:        = {MONTGOMERY + (1.0 - MONTGOMERY):.15f}")
