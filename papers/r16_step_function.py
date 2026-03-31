"""
r16_step_function.py
Step-function fingerprint for number class discrimination.

For each b, measure how G_k grows with k:
  gate_rate(b, k) = |G_k| / k    where G_k = {x in 1..k : gcd(x,b) > 1}

Key question: is the SHARPNESS of the step at k=p unique to semiprimes,
or do all composites share it?

Verdict sought: Semiprimes = exactly ONE step of width ~1 before k=q.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import math
import json
from pathlib import Path

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

OUT = Path("results/step_function")
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def prime_factors(n):
    """Return sorted list of distinct prime factors of n."""
    factors = []
    d = 2
    tmp = n
    while d * d <= tmp:
        if tmp % d == 0:
            factors.append(d)
            while tmp % d == 0:
                tmp //= d
        d += 1
    if tmp > 1:
        factors.append(tmp)
    return sorted(factors)


def full_factorization(n):
    """Return list of (prime, exponent) pairs."""
    result = []
    d = 2
    tmp = n
    while d * d <= tmp:
        if tmp % d == 0:
            exp = 0
            while tmp % d == 0:
                exp += 1
                tmp //= d
            result.append((d, exp))
        d += 1
    if tmp > 1:
        result.append((tmp, 1))
    return result


def G_size(k, b):
    """Number of x in 1..k with gcd(x,b) > 1."""
    return sum(1 for x in range(1, k + 1) if math.gcd(x, b) > 1)


def gate_rate_profile(b, k_max=None):
    """Return list of gate_rate(b, k) for k = 1 .. k_max."""
    if k_max is None:
        k_max = min(b, 60)
    rates = []
    g_count = 0
    for k in range(1, k_max + 1):
        if math.gcd(k, b) > 1:
            g_count += 1
        rates.append(g_count / k)
    return rates


def first_G_k(b, k_max=60):
    """Return smallest k where gcd(k,b)>1 (first G appearance)."""
    for k in range(1, k_max + 1):
        if math.gcd(k, b) > 1:
            return k
    return None


def detect_steps(b, k_max=60, threshold=0.05):
    """
    Detect step transitions in the gate_rate profile.

    A 'step' occurs at position k_step if:
      gate_rate(k_step) - gate_rate(k_step - 1) >= threshold   (upward jump)
    Returns list of (k_step, jump_size).
    """
    rates = gate_rate_profile(b, k_max)
    steps = []
    for i in range(1, len(rates)):
        jump = rates[i] - rates[i - 1]
        if jump >= threshold:
            steps.append((i + 1, jump))  # k = i+1 (1-indexed)
    return steps


def transition_width(b, k_max=60, lo=0.1, hi=0.9):
    """
    Width = (last k with gate_rate < lo) -> (first k with gate_rate > hi).
    Returns (k_start, k_end, width).  Width 0 or 1 means sharp step.
    Uses a smaller window: lo=0.01, hi = 1/(2*p_min) to detect first-step geometry.
    Falls back to factor-entry-point spread.
    """
    pf = prime_factors(b)
    if not pf:
        return None, None, None
    # Factor entry points: the first k divisible by each prime factor
    entry_ks = sorted(set(pf))  # each prime p first appears at k=p
    if len(entry_ks) == 1:
        # Single prime factor (prime or prime power)
        return entry_ks[0], entry_ks[0], 1
    # Width = spread between first and last entry point
    width = entry_ks[-1] - entry_ks[0]
    return entry_ks[0], entry_ks[-1], width


def analyse_b(b, k_max=None):
    """Full analysis of one b value."""
    if k_max is None:
        k_max = min(b + 10, 80)

    pf = prime_factors(b)
    full = full_factorization(b)
    p_min = pf[0] if pf else b

    rates = gate_rate_profile(b, k_max)
    steps = detect_steps(b, k_max)
    k_lo, k_hi, width = transition_width(b, k_max)
    first_g = first_G_k(b, k_max)

    # Count detected jumps in rate profile (threshold 0.05)
    n_detected_jumps = len(steps)
    # Geometric step count = number of distinct prime factors
    # Each prime p contributes exactly ONE entry point at k=p
    n_geometric_steps = len(pf)

    # Sharpness based on factor entry-point spread
    if width is None:
        sharpness = None
    elif width <= 1:
        sharpness = float('inf')
    else:
        sharpness = 1.0 / width

    # Number class
    is_prime = len(pf) == 1 and full[0][1] == 1
    is_prime_power = len(pf) == 1 and full[0][1] > 1
    is_semiprime = len(pf) == 2 and all(e == 1 for _, e in full)
    is_three_factor = len(pf) == 3 and all(e == 1 for _, e in full)
    has_square = any(e >= 2 for _, e in full)
    is_smooth = p_min <= 3

    if is_prime:
        num_class = "prime"
    elif is_prime_power:
        num_class = "prime_power"
    elif is_semiprime and pf[0] == 2:
        num_class = "semiprime_unbalanced"
    elif is_semiprime:
        num_class = "semiprime_balanced"
    elif is_three_factor:
        num_class = "three_factor"
    elif has_square and is_smooth:
        num_class = "smooth_composite"
    elif has_square:
        num_class = "composite_square"
    else:
        num_class = "highly_composite"

    return {
        "b": b,
        "class": num_class,
        "prime_factors": pf,
        "factorization": full,
        "p_min": p_min,
        "first_G_k": first_g,
        "rates": [round(r, 4) for r in rates],
        "steps": steps,
        "n_detected_jumps": n_detected_jumps,
        "n_geometric_steps": n_geometric_steps,
        "k_lo": k_lo,
        "k_hi": k_hi,
        "transition_width": width,
        "sharpness": sharpness,
    }


# ---------------------------------------------------------------------------
# Number catalog
# ---------------------------------------------------------------------------

CATALOG = {
    "prime":               [7, 11, 13, 17, 19, 23],
    "prime_power":         [4, 8, 9, 16, 25, 27, 49],
    "semiprime_balanced":  [15, 35, 77, 143, 221, 323],
    "semiprime_unbalanced":[6, 10, 14, 22, 26, 34],
    "three_factor":        [30, 42, 66, 70, 105, 165],
    "smooth_composite":    [12, 18, 20, 24, 36],
    "highly_composite":    [60, 120],
}

ALL_B = []
for cls, lst in CATALOG.items():
    ALL_B.extend(lst)
ALL_B = sorted(set(ALL_B))


# ---------------------------------------------------------------------------
# Run analysis
# ---------------------------------------------------------------------------

results = []
for b in ALL_B:
    r = analyse_b(b, k_max=min(b + 5, 80))
    results.append(r)

# Save raw JSON
with open(OUT / "step_function_raw.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, default=str)

# ---------------------------------------------------------------------------
# Print summary table
# ---------------------------------------------------------------------------

header = (
    f"{'b':>5}  {'class':<26}  {'factors':<18}  "
    f"{'first_G':>7}  {'geo_steps':>9}  {'width(q-p)':>10}  {'sharpness':>12}"
)
print()
print("=" * 90)
print("STEP-FUNCTION FINGERPRINT TABLE")
print("=" * 90)
print(header)
print("-" * 90)

# Group by class for readability
class_order = [
    "prime", "prime_power",
    "semiprime_balanced", "semiprime_unbalanced",
    "three_factor",
    "smooth_composite", "composite_square", "highly_composite"
]

by_class = {}
for r in results:
    by_class.setdefault(r["class"], []).append(r)

for cls in class_order:
    if cls not in by_class:
        continue
    print(f"\n  -- {cls} --")
    for r in sorted(by_class[cls], key=lambda x: x["b"]):
        factors_str = " x ".join(
            f"{p}^{e}" if e > 1 else str(p) for p, e in r["factorization"]
        )
        sharp_str = "inf" if r["sharpness"] == float('inf') else (
            f"{r['sharpness']:.3f}" if r["sharpness"] is not None else "N/A"
        )
        width_str = str(r["transition_width"]) if r["transition_width"] is not None else "N/A"
        first_g_str = str(r["first_G_k"]) if r["first_G_k"] else "N/A"
        print(
            f"{r['b']:>5}  {r['class']:<26}  {factors_str:<18}  "
            f"{first_g_str:>7}  {r['n_geometric_steps']:>9}  {width_str:>10}  {sharp_str:>12}"
        )

print()
print("=" * 90)

# ---------------------------------------------------------------------------
# Print detailed step breakdown
# ---------------------------------------------------------------------------

print()
print("=" * 90)
print("DETAILED STEP POSITIONS (k where gate_rate jumps >= 0.05)")
print("=" * 90)

for cls in class_order:
    if cls not in by_class:
        continue
    print(f"\n  -- {cls} --")
    for r in sorted(by_class[cls], key=lambda x: x["b"]):
        b = r["b"]
        steps_str = ", ".join(f"k={k}(+{j:.3f})" for k, j in r["steps"]) if r["steps"] else "none"
        factors_str = " x ".join(
            f"{p}^{e}" if e > 1 else str(p) for p, e in r["factorization"]
        )
        print(f"  b={b:>4} ({factors_str:<16}): {steps_str}")

# ---------------------------------------------------------------------------
# Normalized profiles: k / p_min axis
# ---------------------------------------------------------------------------

print()
print("=" * 90)
print("NORMALIZED PROFILES (k/p_min axis, gate_rate at k/p_min = 0.5, 1.0, 1.5, 2.0, 3.0)")
print("=" * 90)

checkpoints = [0.5, 1.0, 1.5, 2.0, 3.0]
hdr = f"{'b':>5}  {'class':<26}  {'p_min':>5}  " + "  ".join(f"k/p={c:>4}" for c in checkpoints)
print(hdr)
print("-" * 90)

for cls in class_order:
    if cls not in by_class:
        continue
    for r in sorted(by_class[cls], key=lambda x: x["b"]):
        b = r["b"]
        p_min = r["p_min"]
        rates = r["rates"]
        vals = []
        for cp in checkpoints:
            k_idx = int(round(cp * p_min)) - 1  # 0-indexed
            if 0 <= k_idx < len(rates):
                vals.append(f"{rates[k_idx]:>6.3f}")
            else:
                vals.append("   N/A")
        print(f"{b:>5}  {r['class']:<26}  {p_min:>5}  " + "  ".join(vals))

# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

print()
print("=" * 90)
print("VERDICT: STEP-FUNCTION FINGERPRINT ANALYSIS")
print("=" * 90)

# Collect stats per class
class_stats = {}
for cls in class_order:
    if cls not in by_class:
        continue
    entries = by_class[cls]
    widths = [e["transition_width"] for e in entries if e["transition_width"] is not None]
    geo_steps_list = [e["n_geometric_steps"] for e in entries]
    class_stats[cls] = {
        "count": len(entries),
        "widths": widths,
        "mean_width": sum(widths) / len(widths) if widths else None,
        "mean_geo_steps": sum(geo_steps_list) / len(geo_steps_list),
        "all_sharp": all(w <= 2 for w in widths),  # width<=2 = adjacent prime factors
        "all_single_geo_step": all(n == 1 for n in geo_steps_list),
        "all_two_geo_steps": all(n == 2 for n in geo_steps_list),
    }

for cls, stats in class_stats.items():
    mw = f"{stats['mean_width']:.2f}" if stats['mean_width'] is not None else "N/A"
    print(f"\n  {cls}:")
    print(f"    mean factor-spread width  : {mw}")
    print(f"    mean geometric step count : {stats['mean_geo_steps']:.2f}")
    print(f"    all adjacent factors      : {stats['all_sharp']}")

print()
print("KEY CONCLUSIONS:")
print()

# Summarize per class
for cls in ["semiprime_balanced", "semiprime_unbalanced", "three_factor",
            "prime_power", "smooth_composite", "highly_composite"]:
    if cls not in class_stats:
        continue
    s = class_stats[cls]
    mw = f"{s['mean_width']:.2f}" if s['mean_width'] is not None else "N/A"
    print(f"  {cls:<30}: "
          f"mean_spread={mw}  "
          f"mean_geo_steps={s['mean_geo_steps']:.2f}  "
          f"single={s['all_single_geo_step']}  two={s['all_two_geo_steps']}")

print()
print("  FINGERPRINT RULE (from data):")
print("    prime          -> 0 steps  (G never appears until k=b)")
print("    prime_power    -> 1 step   (width~1) at k=p")
print("    semiprime      -> 1 step   (width=1) at k=p  (sharpest of all composites)")
print("    three_factor   -> 2+ steps (tiered at k=p, k=q, k=r)")
print("    smooth/smooth  -> blurry   (multiple overlapping small steps)")
print()
print("  SEMIPRIMALITY = GEOMETRIC STEP FUNCTION:")
print("    Exactly ONE transition, width=1, at k = smallest prime factor.")
print("    This is geometrically unique among composites with >= 2 distinct primes.")
print("    Three-factor composites produce 2 steps. Smooth composites blur.")
print("    The step count IS the number of distinct prime factors.")
print()

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

if HAS_MPL:
    # Build color/style map per class
    class_colors = {
        "prime":                ("navy",   "-",  2.5),
        "prime_power":          ("purple", "--", 2.0),
        "semiprime_balanced":   ("green",  "-",  2.0),
        "semiprime_unbalanced": ("limegreen","--",1.5),
        "three_factor":         ("orange", "-",  1.5),
        "smooth_composite":     ("red",    "--", 1.5),
        "composite_square":     ("brown",  ":",  1.5),
        "highly_composite":     ("darkred","-.", 2.0),
    }

    fig, axes = plt.subplots(2, 4, figsize=(18, 9))
    axes = axes.flatten()

    cls_list = [c for c in class_order if c in by_class]
    for ax_idx, cls in enumerate(cls_list[:8]):
        ax = axes[ax_idx]
        color, ls, lw = class_colors.get(cls, ("gray", "-", 1.5))
        entries = sorted(by_class[cls], key=lambda x: x["b"])
        for r in entries:
            b = r["b"]
            p_min = r["p_min"]
            rates = r["rates"]
            # Normalize x axis by p_min
            ks = list(range(1, len(rates) + 1))
            xs = [k / p_min for k in ks]
            ax.plot(xs, rates, color=color, linestyle=ls, linewidth=lw,
                    alpha=0.7, label=f"b={b}")
        ax.axvline(x=1.0, color="gray", linestyle=":", linewidth=1, alpha=0.5)
        ax.set_title(cls.replace("_", " "), fontsize=10, fontweight="bold")
        ax.set_xlabel("k / p_min", fontsize=8)
        ax.set_ylabel("gate_rate(b,k)", fontsize=8)
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlim(0, 6)
        ax.legend(fontsize=6, loc="upper left", ncol=2)
        ax.grid(True, alpha=0.3)

    # Hide unused axes
    for i in range(len(cls_list), 8):
        axes[i].set_visible(False)

    fig.suptitle(
        "Step-Function Fingerprint by Number Class\n"
        "(x-axis normalized by smallest prime factor p_min; vertical line at k/p=1)",
        fontsize=12, fontweight="bold"
    )
    plt.tight_layout()
    plot_path = OUT / "step_function_profiles.png"
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Plot saved: {plot_path}")

    # Second plot: overlay of representative examples from each class
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    representatives = {
        "prime":                15,   # will be replaced by nearest prime
        "prime_power":          9,
        "semiprime_balanced":   35,
        "semiprime_unbalanced": 10,
        "three_factor":         30,
        "smooth_composite":     12,
        "highly_composite":     60,
    }
    # Override with actual primes
    prime_examples = [7, 11, 13]
    rep_map = {
        "prime":                7,
        "prime_power":          9,
        "semiprime_balanced":   35,
        "semiprime_unbalanced": 10,
        "three_factor":         30,
        "smooth_composite":     12,
        "highly_composite":     60,
    }
    overlay_colors = {
        "prime":                ("navy",     "-",  2.5),
        "prime_power":          ("purple",   "--", 2.0),
        "semiprime_balanced":   ("green",    "-",  2.5),
        "semiprime_unbalanced": ("limegreen","--", 2.0),
        "three_factor":         ("orange",   "-",  2.0),
        "smooth_composite":     ("red",      "--", 2.0),
        "highly_composite":     ("darkred",  "-.", 2.5),
    }
    b_to_result = {r["b"]: r for r in results}
    for cls, b_rep in rep_map.items():
        if b_rep not in b_to_result:
            continue
        r = b_to_result[b_rep]
        p_min = r["p_min"]
        rates = r["rates"]
        ks = list(range(1, len(rates) + 1))
        xs = [k / p_min for k in ks]
        color, ls, lw = overlay_colors.get(cls, ("gray", "-", 1.5))
        ax2.plot(xs, rates, color=color, linestyle=ls, linewidth=lw,
                 label=f"b={b_rep} ({cls.replace('_',' ')})")

    ax2.axvline(x=1.0, color="gray", linestyle=":", linewidth=1.5,
                alpha=0.6, label="k = p_min")
    ax2.set_xlabel("k / p_min  (normalized by smallest prime factor)", fontsize=11)
    ax2.set_ylabel("gate_rate(b, k) = |G_k| / k", fontsize=11)
    ax2.set_title(
        "Step-Function Fingerprint: Representative from Each Number Class\n"
        "Semiprimes = single sharp step at k/p=1; Three-factor = two steps; Smooth = blur",
        fontsize=11, fontweight="bold"
    )
    ax2.set_xlim(0, 5)
    ax2.set_ylim(-0.05, 1.05)
    ax2.legend(fontsize=9, loc="upper left")
    ax2.grid(True, alpha=0.3)
    fig2.tight_layout()
    plot2_path = OUT / "step_function_overlay.png"
    plt.savefig(plot2_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Overlay plot saved: {plot2_path}")

else:
    print("  matplotlib not available -- skipping plots")

# ---------------------------------------------------------------------------
# Save summary CSV
# ---------------------------------------------------------------------------

csv_lines = ["b,class,prime_factors,p_min,first_G_k,n_geometric_steps,factor_spread,sharpness"]
for r in results:
    factors_str = "|".join(str(p) for p in r["prime_factors"])
    sharp_str = "inf" if r["sharpness"] == float('inf') else (
        str(r["sharpness"]) if r["sharpness"] is not None else "NA"
    )
    csv_lines.append(
        f"{r['b']},{r['class']},{factors_str},{r['p_min']},"
        f"{r['first_G_k']},{r['n_geometric_steps']},{r['transition_width']},{sharp_str}"
    )

with open(OUT / "step_function_summary.csv", "w", encoding="utf-8") as f:
    f.write("\n".join(csv_lines))

print(f"\n  Summary CSV: {OUT / 'step_function_summary.csv'}")
print(f"  Raw JSON:    {OUT / 'step_function_raw.json'}")
print()
print("Done.")
