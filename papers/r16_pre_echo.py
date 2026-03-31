"""
Pre-echo survey: geometric friction before prime obstruction
Author: Brayden Sanders / 7Site LLC
Insight framing: C.A. Luther dispersion conjecture + harmonic pre-echo hypothesis

Measures:
  1. Closure defect(k): fraction of products escaping {1..k} before G appears
  2. Shadow distance(k): min distance from any product to nearest future G element
  3. Harmonic resonance R(k): spectral power at prime frequency in the pre-G alphabet
  4. Corridor difficulty + skew around k=p
  5. Saturation gradient: slope + jump in k=p..q bridge
"""

import math, json
import numpy as np
from pathlib import Path

OUT = Path("results/pre_echo")
OUT.mkdir(parents=True, exist_ok=True)


def closure_defect(k, b):
    """Fraction of products in {1..k}^2 that land outside {1..k} mod b."""
    total = k * k
    outside = sum(
        1 for x in range(1, k+1) for y in range(1, k+1)
        if (x * y) % b not in range(1, k+1)
    )
    return outside / total


def shadow_min_distance(k, b, p):
    """Min residual distance from any product x*y mod b to nearest multiple of p."""
    min_dist = p
    for x in range(1, k+1):
        for y in range(1, k+1):
            r = (x * y) % b
            dist = min(r % p, p - (r % p))
            if dist < min_dist:
                min_dist = dist
    return min_dist


def harmonic_resonance(k, p):
    """Spectral power at frequency 1/p: |sum exp(2pi*i*x/p)|^2 / k^2"""
    if k == 0:
        return 1.0
    s = sum(complex(math.cos(2 * math.pi * x / p), math.sin(2 * math.pi * x / p)) for x in range(1, k+1))
    return (abs(s) ** 2) / (k * k)


def G_elements(k, b):
    return [x for x in range(1, k+1) if math.gcd(x, b) > 1]


def best_score_k(b, k, n_trials=400, n_steps=250, seed=0):
    """Optimization score for (b,k). Returns None if G empty."""
    G = set(G_elements(k, b))
    C = [x for x in range(1, k+1) if x not in G]
    if not G or not C:
        return None
    rng = np.random.default_rng(seed)
    operators = list(range(1, k+1))
    best = 0.0
    for _ in range(n_trials):
        state = int(rng.choice(C))
        hit_G = stay_G = 0
        for _ in range(n_steps):
            op = int(rng.choice(operators))
            nxt = (state * op) % b
            if nxt == 0 or nxt > k:
                nxt = state
            if nxt in G:
                hit_G += 1
                stay_G += 1
            state = nxt
        score = 0.5 * (hit_G / n_steps) + 0.5 * (1 - stay_G / n_steps)
        if score > best:
            best = score
    return best


# ── Survey targets ─────────────────────────────────────────────────────────────
TARGETS = [
    (15,  "3x5",   3,  5),
    (21,  "3x7",   3,  7),
    (35,  "5x7",   5,  7),
    (55,  "5x11",  5, 11),
    (77,  "7x11",  7, 11),
    (91,  "7x13",  7, 13),
    (143, "11x13", 11, 13),
    (187, "11x17", 11, 17),
    (221, "13x17", 13, 17),
    (323, "17x19", 17, 19),
]

print("Pre-Echo Survey: Geometric Friction Before Prime Obstruction")
print("=" * 70)

results = []

for b, label, p, q in TARGETS:
    print(f"\nb={b} ({label})  p={p} q={q}  q/p={q/p:.2f}")
    print(f"  Pre-echo zone k=1..{p-1}  First-G at k={p}  Bridge k={p}..{q-1}  Second-G at k={q}")

    world = {"b": b, "label": label, "p": p, "q": q, "pre_echo": [], "corridor": []}

    # ── Pre-echo zone (k < p) ───────────────────────────────────────────────────
    print(f"  {'k':>4}  {'defect':>8}  {'shadow':>8}  {'R(k)':>8}")
    for k in range(1, p):
        defect = closure_defect(k, b)
        shadow = shadow_min_distance(k, b, p)
        R = harmonic_resonance(k, p)
        print(f"  {k:>4}  {defect:>8.4f}  {shadow:>8}  {R:>8.4f}")
        world["pre_echo"].append({
            "k": k, "defect": defect, "shadow": int(shadow), "resonance": R
        })

    # ── Corridor: k = max(1,p-2) .. min(b-1, q+3) ─────────────────────────────
    k_start = max(1, p - 2)
    k_end = min(b - 1, q + 3)
    print(f"  Corridor k={k_start}..{k_end}:")
    print(f"  {'k':>4}  {'|G|':>4}  {'defect':>8}  {'shadow':>8}  {'R(k)':>8}  {'score':>8}  {'diff':>8}")
    for k in range(k_start, k_end + 1):
        defect = closure_defect(k, b)
        shadow = shadow_min_distance(k, b, p)
        R = harmonic_resonance(k, p)
        G = G_elements(k, b)
        score = best_score_k(b, k)
        diff = (1 - score) if score is not None else None
        score_str = f"{score:.4f}" if score is not None else "   N/A"
        diff_str  = f"{diff:.4f}"  if diff  is not None else "   N/A"
        print(f"  {k:>4}  {len(G):>4}  {defect:>8.4f}  {shadow:>8}  {R:>8.4f}  {score_str:>8}  {diff_str:>8}")
        world["corridor"].append({
            "k": k, "G_size": len(G), "defect": defect,
            "shadow": int(shadow), "resonance": R,
            "score": score, "difficulty": diff
        })

    # ── Corridor skew around k=p ────────────────────────────────────────────────
    corr = world["corridor"]
    get = lambda kv: next((c for c in corr if c["k"] == kv), None)
    at_p   = get(p)
    at_pp1 = get(p + 1)
    at_pp2 = get(p + 2)
    pre_defect = next((e["defect"] for e in world["pre_echo"] if e["k"] == p-1), None)
    pre_defect_start = next((e["defect"] for e in world["pre_echo"] if e["k"] == 1), None)

    if at_p and at_pp1 and at_p["difficulty"] and at_pp1["difficulty"]:
        rise_1 = at_pp1["difficulty"] - at_p["difficulty"]
        rise_2 = (at_pp2["difficulty"] - at_p["difficulty"]) if at_pp2 and at_pp2["difficulty"] else None
        approach_slope = None
        if p > 2 and pre_defect is not None and pre_defect_start is not None:
            approach_slope = (pre_defect - pre_defect_start) / (p - 2)
        rise_2_str = f"{rise_2:+.4f}" if rise_2 is not None else "?"
        slope_str  = f"{approach_slope:.4f}" if approach_slope is not None else "N/A"
        print(f"  Skew: diff(p)={at_p['difficulty']:.4f}  +1={rise_1:+.4f}  "
              f"+2={rise_2_str}  approach_slope={slope_str}")
        world["skew"] = {
            "diff_at_p": at_p["difficulty"],
            "rise_1": rise_1, "rise_2": rise_2,
            "approach_slope": approach_slope
        }

    # ── Saturation gradient ─────────────────────────────────────────────────────
    bridge = [c for c in corr if p <= c["k"] < q and c["difficulty"] is not None]
    at_q = get(q)
    if len(bridge) >= 2:
        slope = (bridge[-1]["difficulty"] - bridge[0]["difficulty"]) / (bridge[-1]["k"] - bridge[0]["k"])
        jump = (at_q["difficulty"] - bridge[-1]["difficulty"]) if at_q and at_q["difficulty"] else None
        jump_str = f"{jump:+.4f}" if jump is not None else "N/A"
        print(f"  Bridge slope={slope:.4f}/step  jump_at_q={jump_str}")
        world["saturation"] = {"bridge_slope": slope, "jump_at_q": jump}

    results.append(world)

# ── Save JSON ─────────────────────────────────────────────────────────────────
with open(OUT / "pre_echo_atlas.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved: {OUT}/pre_echo_atlas.json")

# ── Summary table ─────────────────────────────────────────────────────────────
print("\n=== SUMMARY ===")
print(f"{'b':>6}  {'label':>8}  {'p':>3}  {'q':>3}  "
      f"{'max_defect':>10}  {'min_shadow':>10}  "
      f"{'diff@p':>8}  {'rise+1':>7}  {'bridge_slp':>10}")
for w in results:
    max_defect = max((e["defect"] for e in w["pre_echo"]), default=0)
    min_shadow = min((e["shadow"] for e in w["pre_echo"]), default=0)
    skew = w.get("skew", {})
    sat  = w.get("saturation", {})
    rise = skew.get("rise_1") or 0
    slp  = sat.get("bridge_slope") or 0
    print(f"{w['b']:>6}  {w['label']:>8}  {w['p']:>3}  {w['q']:>3}  "
          f"{max_defect:>10.4f}  {min_shadow:>10}  "
          f"{skew.get('diff_at_p', 0):>8.4f}  {rise:>7.4f}  {slp:>10.4f}")

# ── Plots ─────────────────────────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "Pre-Echo Survey: Geometric Friction Before Prime Obstruction\n"
        "Insight: C.A. Luther | Verification: B. Sanders / 7Site LLC",
        fontsize=11)
    colors = plt.cm.tab10(np.linspace(0, 1, len(results)))

    # Panel 1: Closure defect in pre-echo zone (normalized k/p)
    ax = axes[0, 0]
    for w, col in zip(results, colors):
        if w["pre_echo"]:
            ks = [e["k"] / w["p"] for e in w["pre_echo"]]
            ds = [e["defect"] for e in w["pre_echo"]]
            ax.plot(ks, ds, 'o-', color=col, label=f"b={w['b']}", markersize=4)
    ax.axvline(1.0, color='red', lw=1.5, linestyle='--', label='k=p (First-G)')
    ax.set_xlabel("k / p  (normalized)")
    ax.set_ylabel("Closure defect")
    ax.set_title("Ghost Gate: Products escaping {1..k}")
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

    # Panel 2: Harmonic resonance R(k)
    ax = axes[0, 1]
    for w, col in zip(results, colors):
        if w["pre_echo"]:
            ks = [e["k"] / w["p"] for e in w["pre_echo"]]
            Rs = [e["resonance"] for e in w["pre_echo"]]
            ax.plot(ks, Rs, 's-', color=col, label=f"b={w['b']}", markersize=4)
    ax.axvline(1.0, color='red', lw=1.5, linestyle='--')
    ax.set_xlabel("k / p")
    ax.set_ylabel("R(k)")
    ax.set_title("Unit-Alphabet Resonance at Prime Frequency 1/p")
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

    # Panel 3: Shadow distance
    ax = axes[1, 0]
    for w, col in zip(results, colors):
        if w["pre_echo"]:
            ks = [e["k"] / w["p"] for e in w["pre_echo"]]
            sh = [e["shadow"] for e in w["pre_echo"]]
            ax.plot(ks, sh, '^-', color=col, label=f"b={w['b']}", markersize=4)
    ax.axvline(1.0, color='red', lw=1.5, linestyle='--')
    ax.set_xlabel("k / p")
    ax.set_ylabel("Min product distance to multiple of p")
    ax.set_title("Product Shadow: Approach to Obstruction")
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

    # Panel 4: Full corridor — defect (dashed) + difficulty (solid)
    ax = axes[1, 1]
    for w, col in zip(results[:6], colors[:6]):
        ks_d = [e["k"]/w["p"] for e in w["corridor"] if e["difficulty"] is not None]
        ds_d = [e["difficulty"] for e in w["corridor"] if e["difficulty"] is not None]
        if ks_d:
            ax.plot(ks_d, ds_d, 'o-', color=col, label=f"b={w['b']}", markersize=4)
        ks_c = [e["k"]/w["p"] for e in w["corridor"]]
        def_c = [e["defect"] for e in w["corridor"]]
        ax.plot(ks_c, def_c, '--', color=col, alpha=0.45, lw=1)
    ax.axvline(1.0, color='red', lw=1.5, linestyle='--', label='k=p')
    ax.set_xlabel("k / p")
    ax.set_ylabel("Difficulty / Closure defect")
    ax.set_title("Corridor: Defect (dashed) vs Difficulty (solid)")
    ax.legend(fontsize=7, ncol=2)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUT / "pre_echo_atlas.png", dpi=120, bbox_inches='tight')
    print(f"Saved: {OUT}/pre_echo_atlas.png")
except Exception as e:
    print(f"Plot error: {e}")
