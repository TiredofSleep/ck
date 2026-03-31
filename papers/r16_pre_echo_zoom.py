"""
r16_pre_echo_zoom.py — Fine-structure zoom-in pre-echo analysis
Author: Brayden Sanders / 7Site LLC
Insight framing: C.A. Luther harmonic pre-echo hypothesis

Complements r16_pre_echo_deep.py — zooms into the microscopic structure:

  Z1. Last-step anatomy: sub-pixel zoom on k = p-3, p-2, p-1, p, p+1
      What changes in the FINAL steps before First-G?
  Z2. Product distribution anatomy: where do escaped products land relative to p?
      Do they cluster approaching p? Is there a "shadow cone"?
  Z3. Multi-harmonic resonance: R(k) at 1/p, 2/p, 3/p, 4/p simultaneously
      Are higher harmonics of p also echoing?
  Z4. Defect per source: closure_defect broken down by (x mod p, y mod p) classes
      Which residue classes drive the leakage?
  Z5. Resonance asymmetry: measure R just AFTER k=p — does resonance at 1/p
      recover, stay zero, or oscillate?
  Z6. The exact transition: |G|, interleave, R(k,1/p), defect at every k = p-5..p+5
  Z7. Prime gap fingerprint: for fixed p, how does R(k,1/q) in the bridge depend
      on the prime gap q-p vs the ratio q/p?
  Z8. Defect velocity: d(defect)/dk — is it accelerating, constant, or decelerating
      as k approaches p?
"""

import sys, math, json
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
from pathlib import Path
from collections import defaultdict

OUT = Path("results/zoom_pre_echo")
OUT.mkdir(parents=True, exist_ok=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def next_prime(n):
    x = n + 1
    while not is_prime(x): x += 1
    return x

def G_elements(k, b):
    return [x for x in range(1, k+1) if math.gcd(x, b) > 1]

def closure_defect(k, b):
    total = k * k
    outside = sum(
        1 for x in range(1, k+1) for y in range(1, k+1)
        if (x * y) % b not in range(1, k+1)
    )
    return outside / total

def harmonic_resonance(k, f):
    if k == 0: return 1.0
    s = sum(complex(math.cos(2*math.pi*x/f), math.sin(2*math.pi*x/f))
            for x in range(1, k+1))
    return (abs(s)**2) / (k*k)

def harmonic_resonance_exact(k, f):
    """sin²(πk/f) / (k² sin²(π/f))"""
    denom = math.sin(math.pi / f)
    if abs(denom) < 1e-15: return 0.0
    return math.sin(math.pi * k / f)**2 / (k * k * denom * denom)

def interleave_score(k, b):
    G = G_elements(k, b)
    if not G: return 0.0
    C = [x for x in range(1, k+1) if math.gcd(x, b) == 1]
    if not C: return 1.0
    switches = sum(1 for i in range(1, k) if
                   (math.gcd(i, b) > 1) != (math.gcd(i+1, b) > 1))
    return switches / (2 * len(G))


# ── Z1: Last-step anatomy ──────────────────────────────────────────────────────
print("\n" + "="*70)
print("Z1: Last-step anatomy — final 7 steps before First-G")
print("="*70)

FLAGSHIP = [(35,5,7),(77,7,11),(143,11,13),(221,13,17),(323,17,19),(667,23,29),(1073,29,37)]
z1_results = []

for b, p, q in FLAGSHIP:
    print(f"\n  b={b} ({p}×{q}): transition k={max(1,p-5)}..{p+3}")
    print(f"  {'k':>4}  {'zone':>10}  {'|G|':>4}  {'interleave':>10}  "
          f"{'defect':>8}  {'R(k,1/p)':>10}  {'dD/dk':>8}")
    rows = []
    prev_def = None
    for k in range(max(1,p-5), p+4):
        G   = G_elements(k, b)
        IL  = interleave_score(k, b)
        def_ = closure_defect(k, b)
        Rp   = harmonic_resonance_exact(k, p) if k < p else harmonic_resonance(k, p)
        dD   = (def_ - prev_def) if prev_def is not None else 0.0
        zone = "PRE-ECHO" if k < p else ("FIRST-G" if k == p else "POST-G")
        print(f"  {k:>4}  {zone:>10}  {len(G):>4}  {IL:>10.4f}  "
              f"{def_:>8.4f}  {Rp:>10.6f}  {dD:>+8.4f}")
        rows.append({"k": k, "zone": zone, "|G|": len(G), "interleave": IL,
                     "defect": def_, "R_p": Rp, "dD_dk": dD})
        prev_def = def_
    z1_results.append({"b": b, "p": p, "q": q, "transition": rows})

with open(OUT / "Z1_last_step.json", "w") as f:
    json.dump(z1_results, f, indent=2)


# ── Z2: Product distribution anatomy ──────────────────────────────────────────
print("\n" + "="*70)
print("Z2: Product landing anatomy — where do escaped products land?")
print("="*70)

ANATOMY_WORLDS = [(35,5,7),(77,7,11),(143,11,13)]
z2_results = []

for b, p, q in ANATOMY_WORLDS:
    print(f"\n  b={b} ({p}×{q}): product residue distribution mod p, k=1..{p+1}")
    print(f"  {'k':>4} | " + "  ".join(f"≡{r}(p)" for r in range(p)))
    world_rows = []
    for k in range(1, p+2):
        counts = defaultdict(int)
        total = k*k
        for x in range(1, k+1):
            for y in range(1, k+1):
                r = (x * y) % b
                counts[r % p] += 1
        row_strs = []
        row_data = {}
        for rem in range(p):
            frac = counts[rem] / total
            row_strs.append(f"{frac:.3f}")
            row_data[rem] = frac
        print(f"  {k:>4} | " + "  ".join(row_strs))
        G = G_elements(k, b)
        world_rows.append({"k": k, "|G|": len(G), "distribution": row_data})
    z2_results.append({"b": b, "p": p, "q": q, "rows": world_rows})
    # Key: at k=p, residue 0 fraction = fraction hitting a multiple of p

with open(OUT / "Z2_product_anatomy.json", "w") as f:
    json.dump(z2_results, f, indent=2)


# ── Z3: Multi-harmonic resonance ──────────────────────────────────────────────
print("\n" + "="*70)
print("Z3: Multi-harmonic — R(k) at 1/p, 2/p, 3/p, 4/p simultaneously")
print("="*70)

HARMONIC_WORLDS = [(77,7,11),(143,11,13),(323,17,19)]
z3_results = []

for b, p, q in HARMONIC_WORLDS:
    print(f"\n  b={b} (p={p}): harmonics 1..4 of p, k=1..{p+2}")
    harmonics = [p, p//2 if p//2 >= 2 else p, p//3 if p//3 >= 2 else p, 2, 3]
    # Better: use fractional period fractions — freq denominators f such that k/f = 1, 1/2, 1/3, 1/4
    # That means f = k, 2k, 3k, 4k — but we want FIXED freq, varying k
    # Multi-harmonic: R at f=p (fundamental), f=p/2≈, f=p/3≈ (if integer)
    harm_freqs_label = ["1/p", "2/p (f=p/2)", "3/p (f=p/3)", "4/p (f=p/4)"]
    # Use actual integer denominators closest to p/n
    freq_dens = [p, max(2, p//2), max(2, p//3), max(2, p//4)]
    freq_dens = list(dict.fromkeys(freq_dens))  # deduplicate

    print(f"  freq denominators: {freq_dens}")
    print(f"  {'k':>4} | " + " | ".join(f"R(f={fd})" for fd in freq_dens))
    rows = []
    for k in range(1, p+3):
        Rs = [harmonic_resonance_exact(k, fd) for fd in freq_dens]
        G  = G_elements(k, b)
        zone = "pre" if k < p else ("F-G" if k == p else "post")
        r_strs = "  ".join(f"{R:.4f}" for R in Rs)
        print(f"  {k:>4} [{zone}] | {r_strs}  |G|={len(G)}")
        rows.append({"k": k, "zone": zone, "|G|": len(G),
                     "Rs": {str(fd): R for fd, R in zip(freq_dens, Rs)}})
    z3_results.append({"b": b, "p": p, "q": q, "freq_dens": freq_dens, "rows": rows})

with open(OUT / "Z3_multi_harmonic.json", "w") as f:
    json.dump(z3_results, f, indent=2)


# ── Z4: Defect by residue class ────────────────────────────────────────────────
print("\n" + "="*70)
print("Z4: Defect by residue class — which (x mod p, y mod p) pairs escape?")
print("="*70)

DEFECT_WORLDS = [(35,5,7),(77,7,11)]
z4_results = []

for b, p, q in DEFECT_WORLDS:
    print(f"\n  b={b} ({p}×{q}): escape rate by residue class at k={p-1} (pre-echo peak)")
    k = p - 1
    # For each (rx, ry) = (x mod p, y mod p), what fraction of products escape?
    class_escape = defaultdict(lambda: [0, 0])  # [escaped, total]
    for x in range(1, k+1):
        for y in range(1, k+1):
            r = (x * y) % b
            rx, ry = x % p, y % p
            class_escape[(rx, ry)][1] += 1
            if r not in range(1, k+1):
                class_escape[(rx, ry)][0] += 1

    print(f"  k={k}: escape rates by (x mod p, y mod p):")
    print(f"  {'(rx,ry)':>12}  {'escaped':>8}  {'total':>6}  {'rate':>8}")
    rows = []
    for (rx, ry), (esc, tot) in sorted(class_escape.items()):
        rate = esc/tot if tot > 0 else 0
        print(f"  ({rx:2d},{ry:2d})      {esc:>8}  {tot:>6}  {rate:>8.4f}")
        rows.append({"rx": rx, "ry": ry, "escaped": esc, "total": tot, "rate": rate})
    z4_results.append({"b": b, "p": p, "k": k, "classes": rows})

with open(OUT / "Z4_defect_classes.json", "w") as f:
    json.dump(z4_results, f, indent=2)


# ── Z5: Post-G resonance ───────────────────────────────────────────────────────
print("\n" + "="*70)
print("Z5: Post-G resonance — does R(k,1/p) recover after First-G?")
print("="*70)

z5_results = []
for b, p, q in [(77,7,11),(143,11,13),(323,17,19)]:
    print(f"\n  b={b} ({p}×{q}): R(k,1/p) extended k=p-3..q+3")
    print(f"  {'k':>4}  {'zone':>10}  {'R(k,1/p)':>10}  {'closed':>10}  {'|G|':>5}")
    rows = []
    for k in range(max(1,p-3), min(b-1, q+4)):
        G = G_elements(k, b)
        Rp_num = harmonic_resonance(k, p)
        Rp_cf  = harmonic_resonance_exact(k, p)
        zone = "pre" if k < p else ("bridge" if p <= k < q else ("2nd-G" if k == q else "post"))
        print(f"  {k:>4}  {zone:>10}  {Rp_num:>10.6f}  {Rp_cf:>10.6f}  {len(G):>5}")
        rows.append({"k": k, "zone": zone, "|G|": len(G), "R_p": Rp_num})
    z5_results.append({"b": b, "p": p, "q": q, "rows": rows})

with open(OUT / "Z5_post_G_resonance.json", "w") as f:
    json.dump(z5_results, f, indent=2)


# ── Z6: Exact transition snapshot ─────────────────────────────────────────────
print("\n" + "="*70)
print("Z6: Exact transition snapshot — every signal at k=p-5..p+5")
print("="*70)

SNAPSHOT_WORLDS = [
    (35,5,7),(55,5,11),(77,7,11),(91,7,13),
    (143,11,13),(187,11,17),(221,13,17),(323,17,19)
]
z6_results = []

for b, p, q in SNAPSHOT_WORLDS:
    print(f"\n  b={b} ({p}×{q}):")
    print(f"  {'k':>4}  {'Δk':>4}  {'|G|':>4}  {'IL':>6}  "
          f"{'defect':>8}  {'dD/dk':>8}  {'R(1/p)':>8}  {'dR/dk':>8}")
    rows = []
    prev_def, prev_R = None, None
    for k in range(max(1,p-5), min(b-1, p+6)):
        G    = G_elements(k, b)
        IL   = interleave_score(k, b)
        def_ = closure_defect(k, b)
        Rp   = harmonic_resonance_exact(k, p)
        dD   = (def_ - prev_def) if prev_def is not None else None
        dR   = (Rp - prev_R)    if prev_R   is not None else None
        dD_s = f"{dD:+.4f}" if dD is not None else "   N/A"
        dR_s = f"{dR:+.6f}" if dR is not None else "      N/A"
        print(f"  {k:>4}  {k-p:>+4}  {len(G):>4}  {IL:>6.3f}  "
              f"{def_:>8.4f}  {dD_s:>8}  {Rp:>8.5f}  {dR_s:>8}")
        rows.append({"k": k, "dk": k-p, "|G|": len(G), "interleave": IL,
                     "defect": def_, "dD": dD, "R_p": Rp, "dR": dR})
        prev_def, prev_R = def_, Rp
    z6_results.append({"b": b, "p": p, "q": q, "snapshot": rows})

with open(OUT / "Z6_transition_snapshot.json", "w") as f:
    json.dump(z6_results, f, indent=2)


# ── Z7: Prime gap fingerprint ──────────────────────────────────────────────────
print("\n" + "="*70)
print("Z7: Prime gap fingerprint — R(k,1/q) in bridge vs prime gap and ratio")
print("="*70)

FIXED_P_Z7 = 7
q_list = [q for q in range(FIXED_P_Z7+2, 120) if is_prime(q)]
z7_results = []

print(f"  p={FIXED_P_Z7} fixed.  For each q: final R(q-1,1/q), bridge midpoint R, gap vs ratio")
print(f"  {'q':>4}  {'gap=q-p':>7}  {'ratio=q/p':>9}  {'R(q-1)':>8}  "
      f"{'R_mid':>8}  {'R_slope':>9}")
for q in q_list:
    b = FIXED_P_Z7 * q
    gap   = q - FIXED_P_Z7
    ratio = q / FIXED_P_Z7
    R_end = harmonic_resonance_exact(q-1, q)   # = 1/(q-1)^2
    # Bridge midpoint
    k_mid = (FIXED_P_Z7 + q) // 2
    R_mid = harmonic_resonance_exact(k_mid, q) if k_mid < q else 0.0
    # Slope: (R_end - R_start) / bridge_len
    R_start = harmonic_resonance_exact(FIXED_P_Z7, q)  # at k=p
    R_slope = (R_end - R_start) / gap if gap > 0 else 0.0
    print(f"  {q:>4}  {gap:>7}  {ratio:>9.3f}  {R_end:>8.5f}  "
          f"{R_mid:>8.5f}  {R_slope:>9.6f}")
    z7_results.append({"q": q, "b": b, "gap": gap, "ratio": ratio,
                       "R_end": R_end, "R_mid": R_mid, "R_slope": R_slope,
                       "R_start": R_start})

with open(OUT / "Z7_prime_gap.json", "w") as f:
    json.dump(z7_results, f, indent=2)


# ── Z8: Defect velocity ────────────────────────────────────────────────────────
print("\n" + "="*70)
print("Z8: Defect velocity — d(defect)/dk shape approaching First-G")
print("="*70)

VELOCITY_WORLDS = [(35,5,7),(77,7,11),(143,11,13),(323,17,19),(667,23,29),(1073,29,37)]
z8_results = []

for b, p, q in VELOCITY_WORLDS:
    print(f"\n  b={b} ({p}×{q}): defect velocity k=1..p")
    print(f"  {'k':>4}  {'k/p':>6}  {'defect':>8}  {'dD/dk':>8}  {'d2D/dk2':>10}  trend")
    defects = [0.0] + [closure_defect(k, b) for k in range(1, p+1)]
    rows = []
    for k in range(1, p+1):
        d   = defects[k]
        dD  = defects[k] - defects[k-1]
        d2D = (defects[k] - 2*defects[k-1] + defects[k-2]) if k >= 2 else 0.0
        trend = "ACCEL" if d2D > 1e-6 else ("DECEL" if d2D < -1e-6 else "LINEAR")
        print(f"  {k:>4}  {k/p:>6.3f}  {d:>8.4f}  {dD:>+8.4f}  {d2D:>+10.6f}  {trend}")
        rows.append({"k": k, "k_over_p": k/p, "defect": d, "dD": dD, "d2D": d2D})
    z8_results.append({"b": b, "p": p, "q": q, "velocity": rows})

with open(OUT / "Z8_defect_velocity.json", "w") as f:
    json.dump(z8_results, f, indent=2)


# ── Plots ──────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("GENERATING ZOOM PLOTS")
print("="*70)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # ── Fig Z1: Transition telescope ──
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle(
        "Transition Telescope: Every Signal at k = p±5\n"
        "C.A. Luther | B. Sanders / 7Site LLC", fontsize=11)
    for ax, entry in zip(axes.flat, z6_results[:8]):
        b, p, q = entry["b"], entry["p"], entry["q"]
        rows = entry["snapshot"]
        dks  = [r["dk"] for r in rows]
        defs = [r["defect"] for r in rows]
        Rs   = [r["R_p"] for r in rows]
        ILs  = [r["interleave"] for r in rows]
        ax2  = ax.twinx()
        ax.plot(dks, defs, 'b-o', ms=5, lw=2, label="defect")
        ax.plot(dks, ILs,  'g-s', ms=5, lw=2, label="interleave")
        ax2.plot(dks, Rs,  'r-^', ms=5, lw=2, label="R(1/p)", alpha=0.7)
        ax.axvline(0, color='black', lw=2, linestyle='--', label='k=p')
        ax.set_xlabel("k - p"); ax.set_ylabel("defect / interleave", color='b')
        ax2.set_ylabel("R(k,1/p)", color='r')
        ax.set_title(f"b={b} ({p}×{q})", fontsize=9)
        lines1, labs1 = ax.get_legend_handles_labels()
        lines2, labs2 = ax2.get_legend_handles_labels()
        ax.legend(lines1+lines2, labs1+labs2, fontsize=7)
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "figZ1_transition.png", dpi=120, bbox_inches='tight')
    print("Saved: figZ1_transition.png")
    plt.close()

    # ── Fig Z2: Defect velocity ──
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(
        "Defect Velocity: d(defect)/dk and d²(defect)/dk² approaching First-G\n"
        "C.A. Luther | B. Sanders / 7Site LLC", fontsize=11)
    for ax, entry in zip(axes.flat, z8_results):
        b, p, q = entry["b"], entry["p"], entry["q"]
        rows = entry["velocity"]
        ks_n = [r["k_over_p"] for r in rows]
        defs = [r["defect"] for r in rows]
        dDs  = [r["dD"] for r in rows]
        d2Ds = [r["d2D"] for r in rows]
        ax2 = ax.twinx()
        ax.fill_between(ks_n, defs, alpha=0.3, color='steelblue')
        ax.plot(ks_n, defs, 'b-', lw=2, label="defect")
        ax2.plot(ks_n, dDs, 'g-o', ms=4, lw=1.5, label="dD/dk", alpha=0.8)
        ax2.plot(ks_n, d2Ds,'r--s', ms=4, lw=1.5, label="d²D/dk²", alpha=0.8)
        ax2.axhline(0, color='gray', lw=0.8)
        ax.axvline(1.0, color='black', lw=1.5, linestyle='--')
        ax.set_xlabel("k/p"); ax.set_ylabel("closure defect", color='b')
        ax2.set_ylabel("velocity / acceleration", color='g')
        ax.set_title(f"b={b} ({p}×{q})\np={p}", fontsize=9)
        lines1, labs1 = ax.get_legend_handles_labels()
        lines2, labs2 = ax2.get_legend_handles_labels()
        ax.legend(lines1+lines2, labs1+labs2, fontsize=7)
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "figZ2_velocity.png", dpi=120, bbox_inches='tight')
    print("Saved: figZ2_velocity.png")
    plt.close()

    # ── Fig Z3: Post-G resonance recovery ──
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(
        "Post-G Resonance: Does R(k,1/p) recover after First-G?\n"
        "C.A. Luther | B. Sanders / 7Site LLC", fontsize=11)
    for ax, entry in zip(axes, z5_results):
        b, p, q = entry["b"], entry["p"], entry["q"]
        rows = entry["rows"]
        ks = [r["k"] for r in rows]
        Rs = [r["R_p"] for r in rows]
        zones = [r["zone"] for r in rows]
        colors_z = {'pre': 'steelblue', 'bridge': 'orange', '2nd-G': 'red', 'post': 'purple'}
        for i in range(len(ks)-1):
            col = colors_z.get(zones[i], 'gray')
            ax.plot(ks[i:i+2], Rs[i:i+2], '-', color=col, lw=2)
        ax.scatter(ks, Rs, c=[colors_z.get(z,'gray') for z in zones], s=30, zorder=5)
        ax.axvline(p, color='blue',  lw=1.5, linestyle='--', label=f'k=p={p}')
        ax.axvline(q, color='green', lw=1.5, linestyle='--', label=f'k=q={q}')
        ax.set_xlabel("k"); ax.set_ylabel("R(k, 1/p)")
        ax.set_title(f"b={b} ({p}×{q})\nblue=pre, orange=bridge, red/purple=post")
        ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "figZ3_recovery.png", dpi=120, bbox_inches='tight')
    print("Saved: figZ3_recovery.png")
    plt.close()

    # ── Fig Z4: Prime gap fingerprint ──
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(
        f"Prime Gap Fingerprint (p={FIXED_P_Z7} fixed): Bridge Pre-Echo vs Gap vs Ratio\n"
        "C.A. Luther | B. Sanders / 7Site LLC", fontsize=11)
    qs_z7    = [r["q"] for r in z7_results]
    gaps_z7  = [r["gap"] for r in z7_results]
    ratios_z7= [r["ratio"] for r in z7_results]
    R_ends   = [r["R_end"] for r in z7_results]
    R_slopes = [r["R_slope"] for r in z7_results]

    axes[0].scatter(gaps_z7, R_ends, c=ratios_z7, cmap='viridis', s=40)
    axes[0].plot(gaps_z7, [1/(q-1)**2 for q in qs_z7], 'r--', lw=2, label="1/(q-1)²")
    axes[0].set_xlabel("prime gap q-p"); axes[0].set_ylabel("R(q-1,1/q)")
    axes[0].set_title("R at end of bridge vs gap\n(monotone decreasing with q)")
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    axes[1].scatter(ratios_z7, R_slopes, c=gaps_z7, cmap='plasma', s=40)
    axes[1].set_xlabel("q/p ratio"); axes[1].set_ylabel("R slope in bridge")
    axes[1].set_title("R(k,1/q) decay slope vs q/p ratio")
    axes[1].grid(True, alpha=0.3)

    axes[2].scatter(gaps_z7, R_slopes, c=ratios_z7, cmap='viridis', s=40)
    axes[2].set_xlabel("prime gap q-p"); axes[2].set_ylabel("R slope in bridge")
    axes[2].set_title("R slope vs prime gap\n(wider gap → slower decay)")
    axes[2].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "figZ4_gap.png", dpi=120, bbox_inches='tight')
    print("Saved: figZ4_gap.png")
    plt.close()

    print("\nAll zoom plots complete.")

except Exception as e:
    import traceback
    print(f"Plot error: {e}")
    traceback.print_exc()

print("\n" + "="*70)
print("ZOOM PRE-ECHO ATLAS COMPLETE")
print(f"Results: {OUT}")
print("="*70)
