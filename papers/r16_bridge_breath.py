"""
r16_bridge_breath.py — Bridge Breathing: post-First-G recovery encodes factor distance
Author: Brayden Sanders / 7Site LLC
Insight: C.A. Luther corridor atlas — bridge zone k=p..q-1, unit_frac rises then drops at k=q.
Hypothesis: the RATE of recovery after the First-G crash at k=p encodes the DISTANCE to q.

Sections:
  A. Bridge slope catalog — unit_frac(k) for every k in p..q; slope metrics
  B. RSA geometry — balanced vs unbalanced semiprimes; slope vs (q-p), q/p, log(q/p)
  C. Recoil recovery rate — d(unit_frac)/dk near k=p, predict q-p and q/p
  D. RSA noise floor — bridge slope at RSA scale; why it is undetectable

Output:
  results/bridge_breath/table_bridge_slope.txt
  results/bridge_breath/table_rsa_noise.txt
  results/bridge_breath/plot_slope_vs_qmp.png
  results/bridge_breath/plot_slope_vs_ratio.png
  results/bridge_breath/plot_rsa_noise_floor.png
  results/bridge_breath/bridge_breath_results.json
"""

import sys, math, json
sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict

OUT = Path("results/bridge_breath")
OUT.mkdir(parents=True, exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def primes_up_to(n):
    return [x for x in range(2, n+1) if is_prime(x)]

def next_prime_after(n):
    x = n + 1
    while not is_prime(x):
        x += 1
    return x

def factorize_semiprime(b):
    """Return (p, q) with p <= q such that b = p*q and both prime; None if not semiprime."""
    for d in range(2, int(b**0.5)+1):
        if b % d == 0 and is_prime(d) and is_prime(b // d):
            return (d, b // d)
    return None

def unit_frac(k, b):
    """unit_frac(k) = |C_k| / k = #{x in 1..k : gcd(x,b)=1} / k"""
    count = sum(1 for x in range(1, k+1) if math.gcd(x, b) == 1)
    return count / k

def unit_frac_fast(k, b):
    """Faster: count non-units via prime factors of b."""
    # For semiprime b=p*q: G_k = multiples of p or q in [1..k]
    # |G_k| = floor(k/p) + floor(k/q) - floor(k/pq) [inclusion-exclusion]
    pq = factorize_semiprime(b)
    if pq is None:
        return unit_frac(k, b)
    p, q = pq
    g = k // p + k // q - k // b
    return (k - g) / k

def bridge_profile(b, p, q):
    """Compute unit_frac at every k in p..q. Returns list of (k, uf) pairs."""
    profile = []
    for k in range(p, q+1):
        uf = unit_frac_fast(k, b)
        profile.append((k, uf))
    return profile

# ── Section A: Bridge slope catalog ──────────────────────────────────────────

def analyze_bridge(b, p, q):
    """
    Full bridge analysis for semiprime b=p*q.
    Returns dict with all metrics.
    """
    profile = bridge_profile(b, p, q)
    ks = [x[0] for x in profile]
    ufs = [x[1] for x in profile]
    bridge_len = q - p  # number of interior steps (p to q-1)

    # unit_frac at key points
    uf_at_p = ufs[0]          # just after First-G crash
    uf_at_q_minus_1 = ufs[-2] if len(ufs) >= 2 else ufs[0]
    uf_at_q = ufs[-1]         # sharp drop at q

    # Full bridge slope: avg over interior k=p..q-1
    # slope = (unit_frac(q-1) - unit_frac(p)) / (q - p - 1) if bridge_len > 1
    if bridge_len > 1 and len(ufs) >= 2:
        full_slope = (ufs[-2] - ufs[0]) / (bridge_len - 1)
    elif bridge_len == 1:
        # p and q are consecutive primes; no interior
        full_slope = 0.0
    else:
        full_slope = 0.0

    # Early slope: first 2 steps after p (if available)
    if len(ufs) >= 3:
        early_slope = ufs[2] - ufs[0]   # unit_frac(p+2) - unit_frac(p)
    elif len(ufs) >= 2:
        early_slope = ufs[1] - ufs[0]   # unit_frac(p+1) - unit_frac(p)
    else:
        early_slope = 0.0

    # Recovery rate: d(unit_frac)/dk averaged over k=p..p+3
    recovery_steps = min(4, len(ufs) - 1)  # up to 4 steps
    if recovery_steps > 0:
        recovery_rate = (ufs[recovery_steps] - ufs[0]) / recovery_steps
    else:
        recovery_rate = 0.0

    # Theoretical: at k=p, unit_frac = (p-1)/p. At k=p+1:
    # G_{p+1} = {p} still (next multiple of p is 2p > q for small bridges)
    # So unit_frac(p+1) = p/(p+1). Increment = p/(p+1) - (p-1)/p = 1/(p(p+1))
    theoretical_step = 1.0 / (p * (p + 1))

    # Drop at q: unit_frac(q) - unit_frac(q-1)
    drop_at_q = uf_at_q - uf_at_q_minus_1 if len(ufs) >= 2 else 0.0

    # Predicted q-p from early_slope:
    # Each step adds ~1/(p*k). Over n steps total gain ~ n/(p*p) roughly.
    # Better: at k~p, each step adds ~ 1/(p*(p+step)) ≈ 1/p²
    # So predicted q-p ≈ needed_gain / (1/p²)
    # But what is needed_gain? We need a reference.
    # Simple linear prediction: if full_slope were known at step 1,
    # predicted_q_minus_p = (uf_at_q_minus_1 - uf_at_p) / full_slope
    # Instead use early_slope over 2 steps as proxy for per-step rate:
    per_step = early_slope / 2.0 if early_slope != 0 else None
    if per_step and per_step > 0:
        # Theoretical total bridge gain: integral of 1/(p+t) for t=0..q-p-1
        # ≈ log((q-1)/p) ≈ log(q/p)
        # So predicted q-p from per_step ≈ log(q/p) / per_step
        # But we can also just do a direct estimate:
        predicted_qmp_from_early = (uf_at_q_minus_1 - uf_at_p) / per_step if per_step > 0 else None
    else:
        predicted_qmp_from_early = None

    return {
        'b': b, 'p': p, 'q': q,
        'q_over_p': q / p,
        'q_minus_p': q - p,
        'bridge_len': bridge_len,
        'uf_at_p': uf_at_p,
        'uf_at_q_minus_1': uf_at_q_minus_1,
        'uf_at_q': uf_at_q,
        'full_slope': full_slope,
        'early_slope': early_slope,
        'recovery_rate': recovery_rate,
        'drop_at_q': drop_at_q,
        'theoretical_step': theoretical_step,
        'predicted_qmp_from_early': predicted_qmp_from_early,
        'profile': list(zip(ks, ufs)),
    }


# ── Build semiprime catalog ───────────────────────────────────────────────────

def build_catalog():
    """Build comprehensive catalog of semiprimes."""
    catalog = []

    # Balanced semiprimes (q/p close to 1): twin-prime-like products
    balanced = [
        (17, 19),   # 323
        (29, 31),   # 899
        (41, 43),   # 1763
        (53, 59),   # 3127
        (71, 73),   # 5183
        (101, 103), # 10403
        (137, 139), # 19043
        (149, 151), # 22499
        (179, 181), # 32399
        (191, 193), # 36863
        (197, 199), # 39203
        (227, 229), # 51983
        (239, 241), # 57599
        (269, 271), # 72899
        (281, 283), # 79523
    ]

    # Unbalanced: p=3
    unbalanced_p3 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83]
    unbalanced_p3 = [(3, q) for q in unbalanced_p3]

    # Unbalanced: p=5
    unbalanced_p5 = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    unbalanced_p5 = [(5, q) for q in unbalanced_p5]

    # Unbalanced: p=7
    unbalanced_p7 = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    unbalanced_p7 = [(7, q) for q in unbalanced_p7]

    # Mixed: moderate ratio
    mixed = []
    small_primes = [p for p in primes_up_to(50) if p >= 7]
    for p in small_primes:
        q = p
        for _ in range(6):
            q = next_prime_after(q)
            if q < 500:
                mixed.append((p, q))

    all_pairs = balanced + unbalanced_p3 + unbalanced_p5 + unbalanced_p7 + mixed
    seen = set()
    for p, q in all_pairs:
        b = p * q
        if b not in seen and is_prime(p) and is_prime(q):
            seen.add(b)
            catalog.append(analyze_bridge(b, p, q))

    return catalog


# ── Section B: RSA geometry tables ───────────────────────────────────────────

def rsa_geometry_tables(catalog):
    """Separate balanced vs unbalanced and print tables."""
    balanced = [r for r in catalog if r['q_over_p'] < 1.15]
    unbalanced_p3 = [r for r in catalog if r['p'] == 3]
    unbalanced_p5 = [r for r in catalog if r['p'] == 5]

    lines = []
    lines.append("=" * 90)
    lines.append("SECTION B: RSA GEOMETRY — BALANCED SEMIPRIMES (q/p < 1.15)")
    lines.append("=" * 90)
    hdr = f"{'b':>8}  {'p':>5}  {'q':>5}  {'q/p':>7}  {'q-p':>5}  {'bridge_len':>10}  {'early_slope':>12}  {'full_slope':>11}  {'drop@q':>9}"
    lines.append(hdr)
    lines.append("-" * 90)
    for r in sorted(balanced, key=lambda x: x['b']):
        lines.append(
            f"{r['b']:>8}  {r['p']:>5}  {r['q']:>5}  {r['q_over_p']:>7.4f}  "
            f"{r['q_minus_p']:>5}  {r['bridge_len']:>10}  "
            f"{r['early_slope']:>12.6f}  {r['full_slope']:>11.6f}  {r['drop_at_q']:>9.6f}"
        )

    lines.append("")
    lines.append("=" * 90)
    lines.append("SECTION B: RSA GEOMETRY — UNBALANCED SEMIPRIMES (p=3)")
    lines.append("=" * 90)
    lines.append(hdr)
    lines.append("-" * 90)
    for r in sorted(unbalanced_p3, key=lambda x: x['b']):
        lines.append(
            f"{r['b']:>8}  {r['p']:>5}  {r['q']:>5}  {r['q_over_p']:>7.4f}  "
            f"{r['q_minus_p']:>5}  {r['bridge_len']:>10}  "
            f"{r['early_slope']:>12.6f}  {r['full_slope']:>11.6f}  {r['drop_at_q']:>9.6f}"
        )
    return "\n".join(lines)


# ── Section C: Full slope catalog table ──────────────────────────────────────

def full_slope_table(catalog):
    """Print full bridge slope catalog."""
    lines = []
    lines.append("=" * 110)
    lines.append("SECTION A+C: FULL BRIDGE SLOPE CATALOG")
    lines.append("=" * 110)
    hdr = (f"{'b':>8}  {'p':>5}  {'q':>5}  {'q/p':>7}  {'q-p':>5}  "
           f"{'uf@p':>8}  {'uf@q-1':>8}  {'uf@q':>8}  "
           f"{'early_s':>10}  {'full_s':>10}  {'recov_r':>10}  {'pred_qmp':>10}  {'err_qmp':>9}")
    lines.append(hdr)
    lines.append("-" * 110)
    for r in sorted(catalog, key=lambda x: (x['p'], x['q'])):
        pred = r['predicted_qmp_from_early']
        pred_str = f"{pred:>10.1f}" if pred is not None else f"{'N/A':>10}"
        err = abs(pred - r['q_minus_p']) if pred is not None else None
        err_str = f"{err:>9.1f}" if err is not None else f"{'N/A':>9}"
        lines.append(
            f"{r['b']:>8}  {r['p']:>5}  {r['q']:>5}  {r['q_over_p']:>7.4f}  "
            f"{r['q_minus_p']:>5}  "
            f"{r['uf_at_p']:>8.5f}  {r['uf_at_q_minus_1']:>8.5f}  {r['uf_at_q']:>8.5f}  "
            f"{r['early_slope']:>10.6f}  {r['full_slope']:>10.6f}  "
            f"{r['recovery_rate']:>10.6f}  {pred_str}  {err_str}"
        )
    return "\n".join(lines)


# ── Section D: RSA noise floor ────────────────────────────────────────────────

def rsa_noise_floor():
    """
    Compute bridge slope at RSA scale.
    At k=p (large prime), unit_frac(p) = (p-1)/p.
    unit_frac(p+1) = p/(p+1)   [G_{p+1} still = {p} if next multiple 2p > q]
    Step gain = p/(p+1) - (p-1)/p = 1/(p(p+1)) ≈ 1/p²

    For RSA-1024: p ≈ 2^512. Step gain ≈ 2^{-1024}. Undetectable.
    """
    # Proxy large primes (computationally feasible)
    proxy_primes = [1009, 2003, 5003, 10007, 50021, 100003]

    results = []
    for p in proxy_primes:
        # b = p * q where q is large — we only measure slope near k=p
        # unit_frac(p) = (p-1)/p  (exactly one non-unit: p itself)
        uf_p = (p - 1) / p

        # unit_frac(p+1): G_{p+1} = {p} (since 2p >> p+1 for large p)
        uf_p1 = p / (p + 1)

        # unit_frac(p+2): G_{p+2} = {p}
        uf_p2 = (p + 1) / (p + 2)

        # unit_frac(p+3)
        uf_p3 = (p + 2) / (p + 3)

        step1 = uf_p1 - uf_p
        step2 = uf_p2 - uf_p1
        step3 = uf_p3 - uf_p2
        avg_step = (step1 + step2 + step3) / 3

        # Theoretical: 1/(p*(p+1))
        theoretical = 1.0 / (p * (p + 1))

        # After how many steps does unit_frac recover 1%?
        # Each step ≈ 1/p². Steps to 0.01: 0.01 / (1/p²) = 0.01 * p²
        steps_to_1pct = int(0.01 * p * p)

        # After 3 steps: delta
        delta_3 = 3 * theoretical

        # After 100 steps
        delta_100 = 100 * theoretical

        results.append({
            'p': p,
            'log2_p': math.log2(p),
            'uf_at_p': uf_p,
            'step_gain_measured': step1,
            'theoretical_step': theoretical,
            'delta_3_steps': delta_3,
            'delta_100_steps': delta_100,
            'steps_to_1pct_recovery': steps_to_1pct,
        })

    # RSA-1024 symbolic — avoid float overflow, work in log10 space
    # step ≈ 1/p² = 1/(2^512)² = 2^{-1024}
    log10_step = -1024 * math.log10(2)  # ≈ -308.25

    lines = []
    lines.append("=" * 100)
    lines.append("SECTION D: RSA NOISE FLOOR — BRIDGE SLOPE AT RSA SCALE")
    lines.append("=" * 100)
    hdr = (f"{'p':>10}  {'log2(p)':>8}  {'step_gain':>14}  "
           f"{'theory_step':>14}  {'delta_3':>12}  {'delta_100':>12}  {'steps_to_1pct':>14}")
    lines.append(hdr)
    lines.append("-" * 100)
    for r in results:
        lines.append(
            f"{r['p']:>10}  {r['log2_p']:>8.1f}  "
            f"{r['step_gain_measured']:>14.4e}  {r['theoretical_step']:>14.4e}  "
            f"{r['delta_3_steps']:>12.4e}  {r['delta_100_steps']:>12.4e}  "
            f"{r['steps_to_1pct_recovery']:>14d}"
        )
    lines.append("")
    lines.append(f"RSA-1024 (p ≈ 2^512):")
    lines.append(f"  Step gain ≈ 2^(-1024) ≈ 10^({log10_step:.0f})")
    lines.append(f"  After 3 steps: delta_unit_frac ≈ 3 × 10^({log10_step:.0f})")
    steps_to_1pct_log10 = 1024 * math.log10(2) + math.log10(0.01)  # = log10(0.01 * 2^1024)
    lines.append(f"  Steps to 1% recovery: ≈ 0.01 × 2^1024 ≈ 10^{steps_to_1pct_log10:.0f}  [completely infeasible]")
    lines.append("")
    lines.append("CONCLUSION: RSA security = bridge slope below noise floor.")
    lines.append("  The slope signal is ≈ 1/p² per step. For RSA-1024, this is")
    lines.append(f"  ≈ 10^({log10_step:.0f}) — below any measurable threshold.")
    lines.append("  The only way to read q from the bridge is to walk to k=q itself.")
    lines.append("  This is equivalent to factoring.")
    return "\n".join(lines), results


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot_slope_vs_qmp(catalog):
    """Plot 1: bridge slope vs (q-p)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Bridge Breathing: Slope vs Factor Distance", fontsize=13, fontweight='bold')

    # Group by p
    by_p = defaultdict(list)
    for r in catalog:
        by_p[r['p']].append(r)

    colors = plt.cm.tab10.colors
    p_vals = sorted(by_p.keys())
    color_map = {p: colors[i % 10] for i, p in enumerate(p_vals)}

    ax = axes[0]
    for p, recs in sorted(by_p.items()):
        xs = [r['q_minus_p'] for r in recs]
        ys = [r['full_slope'] for r in recs]
        ax.scatter(xs, ys, color=color_map[p], label=f"p={p}", s=40, alpha=0.8)
    ax.set_xlabel("q - p  (bridge length)", fontsize=11)
    ax.set_ylabel("full_slope  [(uf(q-1)-uf(p))/(q-p-1)]", fontsize=10)
    ax.set_title("Full Bridge Slope vs q-p", fontsize=11)
    ax.legend(fontsize=7, ncol=3, loc='upper right')
    ax.grid(True, alpha=0.3)

    ax2 = axes[1]
    for p, recs in sorted(by_p.items()):
        xs = [r['q_minus_p'] for r in recs]
        ys = [r['early_slope'] for r in recs]
        ax2.scatter(xs, ys, color=color_map[p], label=f"p={p}", s=40, alpha=0.8)
    ax2.set_xlabel("q - p  (bridge length)", fontsize=11)
    ax2.set_ylabel("early_slope  [uf(p+2)-uf(p)]", fontsize=10)
    ax2.set_title("Early Slope (2-step) vs q-p", fontsize=11)
    ax2.legend(fontsize=7, ncol=3, loc='upper right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    out = OUT / "plot_slope_vs_qmp.png"
    plt.savefig(out, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {out}")


def plot_slope_vs_ratio(catalog):
    """Plot 2: bridge slope vs q/p and log(q/p)."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Bridge Breathing: Slope vs Imbalance Ratio", fontsize=13, fontweight='bold')

    by_p = defaultdict(list)
    for r in catalog:
        by_p[r['p']].append(r)

    colors = plt.cm.tab10.colors
    p_vals = sorted(by_p.keys())
    color_map = {p: colors[i % 10] for i, p in enumerate(p_vals)}

    # Plot: full_slope vs q/p
    ax = axes[0]
    for p, recs in sorted(by_p.items()):
        xs = [r['q_over_p'] for r in recs]
        ys = [r['full_slope'] for r in recs]
        ax.scatter(xs, ys, color=color_map[p], label=f"p={p}", s=40, alpha=0.8)
    ax.set_xlabel("q / p", fontsize=11)
    ax.set_ylabel("full_slope", fontsize=11)
    ax.set_title("Full Slope vs q/p", fontsize=11)
    ax.legend(fontsize=7, ncol=3)
    ax.grid(True, alpha=0.3)

    # Plot: full_slope vs log(q/p)
    ax2 = axes[1]
    for p, recs in sorted(by_p.items()):
        xs = [math.log(r['q_over_p']) for r in recs]
        ys = [r['full_slope'] for r in recs]
        ax2.scatter(xs, ys, color=color_map[p], label=f"p={p}", s=40, alpha=0.8)
    ax2.set_xlabel("log(q/p)", fontsize=11)
    ax2.set_ylabel("full_slope", fontsize=11)
    ax2.set_title("Full Slope vs log(q/p)", fontsize=11)
    ax2.legend(fontsize=7, ncol=3)
    ax2.grid(True, alpha=0.3)

    # Plot: recovery_rate vs q-p
    ax3 = axes[2]
    for p, recs in sorted(by_p.items()):
        xs = [r['q_minus_p'] for r in recs]
        ys = [r['recovery_rate'] for r in recs]
        ax3.scatter(xs, ys, color=color_map[p], label=f"p={p}", s=40, alpha=0.8)
    ax3.set_xlabel("q - p", fontsize=11)
    ax3.set_ylabel("recovery_rate  [avg d(uf)/dk over p..p+3]", fontsize=10)
    ax3.set_title("Recovery Rate vs q-p", fontsize=11)
    ax3.legend(fontsize=7, ncol=3)
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    out = OUT / "plot_slope_vs_ratio.png"
    plt.savefig(out, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {out}")


def plot_rsa_noise_floor(noise_results):
    """Plot 3: RSA noise floor — step gain vs log2(p)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("RSA Noise Floor: Bridge Slope Becomes Undetectable", fontsize=13, fontweight='bold')

    ps = [r['p'] for r in noise_results]
    log2_ps = [r['log2_p'] for r in noise_results]
    steps = [r['step_gain_measured'] for r in noise_results]
    steps_to_1pct = [r['steps_to_1pct_recovery'] for r in noise_results]

    ax = axes[0]
    ax.semilogy(log2_ps, steps, 'o-', color='crimson', lw=2, ms=8)
    ax.set_xlabel("log₂(p)  [proxy for RSA key size / 2]", fontsize=11)
    ax.set_ylabel("step gain per unit (log scale)", fontsize=11)
    ax.set_title("Step Gain ≈ 1/p²  →  Undetectable at RSA Scale", fontsize=11)
    # Annotate RSA-1024
    ax.axhline(y=1e-308, color='gray', ls='--', alpha=0.5)
    ax.text(log2_ps[-1] * 0.6, steps[-1] * 0.1,
            "RSA-1024: step ≈ 10⁻³⁰⁸", fontsize=9, color='gray')
    for i, (lp, s) in enumerate(zip(log2_ps, steps)):
        ax.annotate(f"p={ps[i]}", (lp, s), textcoords="offset points",
                    xytext=(5, 3), fontsize=8)
    ax.grid(True, which='both', alpha=0.3)

    ax2 = axes[1]
    ax2.semilogy(log2_ps, steps_to_1pct, 's-', color='navy', lw=2, ms=8)
    ax2.set_xlabel("log₂(p)", fontsize=11)
    ax2.set_ylabel("steps to 1% unit_frac recovery (log scale)", fontsize=11)
    ax2.set_title("Steps to 1% Recovery = 0.01 × p²  →  Infeasible", fontsize=11)
    for i, (lp, s2) in enumerate(zip(log2_ps, steps_to_1pct)):
        ax2.annotate(f"p={ps[i]}", (lp, s2), textcoords="offset points",
                    xytext=(5, 3), fontsize=8)
    ax2.grid(True, which='both', alpha=0.3)

    # Add RSA-1024 annotation symbolically (no float needed)
    ax2.annotate("RSA-1024: 0.01×2^1024 steps\n(heat death of universe × 10^280)",
                 xy=(log2_ps[-1], steps_to_1pct[-1]),
                 xytext=(log2_ps[0] + 1, steps_to_1pct[-1] * 100),
                 fontsize=8, color='darkred',
                 arrowprops=dict(arrowstyle='->', color='darkred', lw=1))

    plt.tight_layout()
    out = OUT / "plot_rsa_noise_floor.png"
    plt.savefig(out, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {out}")


def plot_bridge_profiles(catalog):
    """Plot 4: bridge unit_frac profiles for selected semiprimes."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Bridge Profiles: unit_frac(k) for k=p..q", fontsize=13, fontweight='bold')
    axes = axes.flatten()

    # Select 6 interesting semiprimes
    balanced_ex = [r for r in catalog if r['q_over_p'] < 1.12][:2]
    unbalanced_ex = [r for r in catalog if r['p'] == 3][:3]
    moderate_ex = [r for r in catalog if 1.5 < r['q_over_p'] < 3.0][:1]
    examples = (balanced_ex + unbalanced_ex + moderate_ex)[:6]

    for i, (r, ax) in enumerate(zip(examples, axes)):
        ks = [x[0] for x in r['profile']]
        ufs = [x[1] for x in r['profile']]
        ax.plot(ks, ufs, 'o-', color='steelblue', lw=2, ms=5)
        ax.axvline(x=r['p'], color='red', ls='--', alpha=0.7, label=f"k=p={r['p']}")
        ax.axvline(x=r['q'], color='orange', ls='--', alpha=0.7, label=f"k=q={r['q']}")
        ax.set_title(f"b={r['b']} = {r['p']}×{r['q']}  (q/p={r['q_over_p']:.3f})", fontsize=10)
        ax.set_xlabel("k", fontsize=9)
        ax.set_ylabel("unit_frac(k)", fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        # Annotate slope
        ax.text(0.05, 0.15,
                f"full_slope={r['full_slope']:.4f}\nearly_slope={r['early_slope']:.4f}",
                transform=ax.transAxes, fontsize=8, color='darkgreen',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    out = OUT / "plot_bridge_profiles.png"
    plt.savefig(out, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {out}")


# ── Conclusion analysis ───────────────────────────────────────────────────────

def analyze_predictions(catalog):
    """
    Assess: how well does early_slope predict q-p?
    Compute correlation and typical error.
    """
    valid = [r for r in catalog if r['predicted_qmp_from_early'] is not None and r['q_minus_p'] > 0]
    if not valid:
        return "No valid prediction data."

    actual = np.array([r['q_minus_p'] for r in valid])
    predicted = np.array([r['predicted_qmp_from_early'] for r in valid])
    errors = np.abs(predicted - actual)
    rel_errors = errors / actual

    # Recovery rate vs q-p correlation
    rr = np.array([r['recovery_rate'] for r in valid])
    corr_rr_qmp = np.corrcoef(rr, actual)[0, 1] if len(valid) > 2 else float('nan')

    # Full slope vs q-p correlation
    fs = np.array([r['full_slope'] for r in valid])
    corr_fs_qmp = np.corrcoef(fs, actual)[0, 1] if len(valid) > 2 else float('nan')

    # Full slope vs log(q/p) correlation
    log_ratio = np.array([math.log(r['q_over_p']) for r in valid])
    corr_fs_logratio = np.corrcoef(fs, log_ratio)[0, 1] if len(valid) > 2 else float('nan')

    lines = []
    lines.append("=" * 80)
    lines.append("CONCLUSION ANALYSIS: Can we estimate q from post-First-G recovery slope?")
    lines.append("=" * 80)
    lines.append(f"  Catalog size: {len(catalog)} semiprimes")
    lines.append(f"  Valid predictions: {len(valid)}")
    lines.append(f"")
    lines.append(f"  Prediction quality (early_slope → q-p):")
    lines.append(f"    Mean abs error:     {np.mean(errors):.2f}")
    lines.append(f"    Median abs error:   {np.median(errors):.2f}")
    lines.append(f"    Mean rel error:     {np.mean(rel_errors)*100:.1f}%")
    lines.append(f"    Median rel error:   {np.median(rel_errors)*100:.1f}%")
    lines.append(f"")
    lines.append(f"  Correlation coefficients:")
    lines.append(f"    recovery_rate vs q-p:     r = {corr_rr_qmp:.4f}")
    lines.append(f"    full_slope vs q-p:        r = {corr_fs_qmp:.4f}")
    lines.append(f"    full_slope vs log(q/p):   r = {corr_fs_logratio:.4f}")
    lines.append(f"")
    lines.append(f"  KEY INSIGHT — what early_slope encodes:")
    lines.append(f"    At k=p, unit_frac(p) = (p-1)/p.")
    lines.append(f"    Each step adds ~1/(p*(p+k)) ≈ 1/p² (for small k relative to p).")
    lines.append(f"    The step gain is INDEPENDENT of q — it is determined by p alone.")
    lines.append(f"    early_slope encodes p (via step size 1/p²), not (q-p).")
    lines.append(f"    full_slope encodes the AVERAGE gain over the bridge, which also")
    lines.append(f"    depends on p more than on (q-p). q is only detectable as the")
    lines.append(f"    sharp DROP at k=q — which requires walking to k=q.")
    lines.append(f"")
    lines.append(f"  CONCLUSION:")
    lines.append(f"    The post-First-G recovery slope does NOT reliably predict q-p")
    lines.append(f"    or q/p. The slope is dominated by 1/p² and is nearly uniform")
    lines.append(f"    across all semiprimes with the same p regardless of q.")
    lines.append(f"    q's signal is ONLY in the DROP at k=q — which requires reaching k=q.")
    lines.append(f"    This is why RSA is hard: q leaves no pre-echo in the slope.")
    lines.append(f"    The bridge breath is deep and uniform; the gasp only arrives at q.")

    return "\n".join(lines), {
        'n_catalog': len(catalog),
        'n_valid': len(valid),
        'mean_abs_error': float(np.mean(errors)),
        'median_abs_error': float(np.median(errors)),
        'mean_rel_error': float(np.mean(rel_errors)),
        'corr_recovery_rate_vs_qmp': float(corr_rr_qmp),
        'corr_full_slope_vs_qmp': float(corr_fs_qmp),
        'corr_full_slope_vs_log_ratio': float(corr_fs_logratio),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("r16_bridge_breath.py — Bridge Breathing: post-First-G recovery")
    print("=" * 70)

    print("\n[A] Building semiprime catalog...")
    catalog = build_catalog()
    print(f"    {len(catalog)} semiprimes analyzed.")

    print("\n[B] RSA geometry tables...")
    rsa_text = rsa_geometry_tables(catalog)

    print("\n[C] Full slope catalog...")
    slope_text = full_slope_table(catalog)

    print("\n[D] RSA noise floor...")
    noise_text, noise_results = rsa_noise_floor()

    print("\n[E] Conclusion analysis...")
    conclusion_result = analyze_predictions(catalog)
    if isinstance(conclusion_result, tuple):
        conclusion_text, conclusion_data = conclusion_result
    else:
        conclusion_text = conclusion_result
        conclusion_data = {}

    # ── Save text tables ──────────────────────────────────────────────────────
    table_path = OUT / "table_bridge_slope.txt"
    with open(table_path, 'w', encoding='utf-8') as f:
        f.write(slope_text)
        f.write("\n\n")
        f.write(rsa_text)
        f.write("\n\n")
        f.write(conclusion_text)
    print(f"\n  Saved: {table_path}")

    noise_path = OUT / "table_rsa_noise.txt"
    with open(noise_path, 'w', encoding='utf-8') as f:
        f.write(noise_text)
    print(f"  Saved: {noise_path}")

    # ── Plots ─────────────────────────────────────────────────────────────────
    print("\n[F] Generating plots...")
    plot_slope_vs_qmp(catalog)
    plot_slope_vs_ratio(catalog)
    plot_rsa_noise_floor(noise_results)
    plot_bridge_profiles(catalog)

    # ── JSON output ───────────────────────────────────────────────────────────
    json_out = {
        'catalog': [
            {k: v for k, v in r.items() if k != 'profile'}
            for r in catalog
        ],
        'noise_floor': noise_results,
        'conclusion': conclusion_data,
    }
    json_path = OUT / "bridge_breath_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_out, f, indent=2)
    print(f"  Saved: {json_path}")

    # ── Print summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(slope_text[:3000])
    print("\n...")
    print(rsa_text[:2000])
    print("\n...")
    print(noise_text[:2000])
    print("\n...")
    print(conclusion_text)

    print("\n" + "=" * 70)
    print(f"All output saved to: {OUT.resolve()}")
    print("=" * 70)


if __name__ == '__main__':
    main()
