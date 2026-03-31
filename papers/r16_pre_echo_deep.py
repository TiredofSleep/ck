"""
r16_pre_echo_deep.py — Fractal recursive pre-echo atlas (wide)
Author: Brayden Sanders / 7Site LLC
Insight framing: C.A. Luther harmonic pre-echo hypothesis

Sections (zoom out → zoom in → zoom out → zoom in):
  A. Macro sweep: 150+ semiprimes — defect + resonance landscape
  B. Spectral fingerprint matrix: R(k, f) for ALL prime frequencies simultaneously
  C. Bridge pre-echo: resonance of q *within* the p→q bridge zone
  D. Three-factor nested cascade: p-echo → q-echo → r-echo (triple ghost gates)
  E. Fixed-p scaling law: hold p=7, vary q — what is q-independent vs q-dependent?
  F. Cross-ω: same first prime p, same k, different omega(b) — ring vs geometry split
  G. Resonance closed form: R(k,f) = sin²(πk/f) / (k² sin²(π/f)) — verify exactly
"""

import sys, math, json
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
from pathlib import Path
from collections import defaultdict

OUT = Path("results/deep_pre_echo")
OUT.mkdir(parents=True, exist_ok=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def primes_up_to(n):
    return [x for x in range(2, n+1) if is_prime(x)]

def next_prime(n):
    x = n + 1
    while not is_prime(x):
        x += 1
    return x

def prime_factors(b):
    factors = []
    d, n = 2, b
    while d*d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: factors.append(n)
    return sorted(factors)

def omega(b):
    return len(prime_factors(b))

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
    """R(k,f) = |Σ_{x=1}^{k} exp(2πix/f)|² / k²"""
    if k == 0: return 1.0
    s = sum(complex(math.cos(2*math.pi*x/f), math.sin(2*math.pi*x/f))
            for x in range(1, k+1))
    return (abs(s)**2) / (k*k)

def harmonic_resonance_exact(k, f):
    """Closed form: sin²(πk/f) / (k² sin²(π/f))"""
    denom_sin = math.sin(math.pi / f)
    if abs(denom_sin) < 1e-15: return 0.0
    num = math.sin(math.pi * k / f)
    return (num * num) / (k * k * denom_sin * denom_sin)


# ── Section A: Macro sweep ─────────────────────────────────────────────────────
print("\n" + "="*70)
print("SECTION A: Macro sweep — 150+ semiprimes")
print("="*70)

macro_results = []
small_primes = [p for p in range(3, 60) if is_prime(p)]

for p in small_primes:
    q = next_prime(p)
    while q <= 3*p:
        b = p * q
        if p < 2:
            q = next_prime(q); continue

        def_pm1 = closure_defect(p-1, b) if p > 2 else 0.0
        def_pm2 = closure_defect(p-2, b) if p > 3 else 0.0
        R_pm1   = harmonic_resonance(p-1, p) if p > 2 else 1.0
        R_pred  = 1.0/(p-1)**2 if p > 2 else 1.0
        err     = abs(R_pm1 - R_pred)

        macro_results.append({
            "b": b, "p": p, "q": q, "q_over_p": q/p,
            "defect_pm1": def_pm1, "defect_pm2": def_pm2,
            "R_pm1": R_pm1, "R_predicted": R_pred, "R_error": err,
        })
        print(f"  b={b:5d} p={p:3d} q={q:3d}  R(p-1)={R_pm1:.6f}  pred={R_pred:.6f}  "
              f"err={err:.2e}  defect(p-1)={def_pm1:.4f}")
        q = next_prime(q)

max_err = max(r["R_error"] for r in macro_results)
print(f"\n  Total: {len(macro_results)} semiprimes  |  Max R error: {max_err:.2e}")
with open(OUT / "A_macro_sweep.json", "w") as f:
    json.dump(macro_results, f, indent=2)


# ── Section B: Spectral fingerprint matrix ─────────────────────────────────────
print("\n" + "="*70)
print("SECTION B: Spectral fingerprint — R(k, f) for all prime f simultaneously")
print("="*70)

SPECTRAL_WORLDS = [(15,3,5),(35,5,7),(77,7,11),(143,11,13),(323,17,19),(667,23,29)]
spectral_results = []

for b, p, q in SPECTRAL_WORLDS:
    freqs = primes_up_to(q + 8)
    k_range = list(range(1, q + 4))
    print(f"\n  b={b} (p={p}, q={q})  k=1..{max(k_range)}  freqs={freqs}")
    print(f"  {'k':>4}  {'dominant_f':>11}  {'R_dom':>7}  {'R(p)':>7}  {'R(q)':>7}  {'defect':>8}")
    rows = {}
    for k in k_range:
        row = {f: harmonic_resonance(k, f) for f in freqs}
        rows[k] = row
        f_dom = max(row, key=row.get)
        def_ = closure_defect(k, b)
        print(f"  {k:>4}  {f_dom:>11}  {row[f_dom]:>7.4f}  "
              f"{row.get(p,0):>7.4f}  {row.get(q,0):>7.4f}  {def_:>8.4f}")
    spectral_results.append({
        "b": b, "p": p, "q": q, "freqs": freqs,
        "matrix": {str(k): {str(f): v for f,v in row.items()} for k,row in rows.items()}
    })

with open(OUT / "B_spectral_matrix.json", "w") as f:
    json.dump(spectral_results, f, indent=2)


# ── Section C: Bridge pre-echo ─────────────────────────────────────────────────
print("\n" + "="*70)
print("SECTION C: Bridge pre-echo — R(k, 1/q) within bridge k=p..q-1")
print("="*70)

BRIDGE_TARGETS = [
    (15,3,5),(21,3,7),(35,5,7),(55,5,11),(77,7,11),
    (91,7,13),(143,11,13),(187,11,17),(221,13,17),(323,17,19),
    (667,23,29),(1073,29,37),(2021,43,47),(3127,53,59),
]
bridge_results = []

for b, p, q in BRIDGE_TARGETS:
    print(f"\n  b={b} ({p}×{q})  bridge k={p}..{q-1}  pre-echo of q:")
    print(f"  {'k':>4}  {'k/q':>6}  {'R(k,1/q)':>10}  {'|G|':>5}  {'defect':>8}")
    bridge_data = []
    for k in range(p, q):
        R_q = harmonic_resonance(k, q)
        G   = G_elements(k, b)
        def_ = closure_defect(k, b) if k <= 20 else None  # skip heavy defect for large b
        def_str = f"{def_:.4f}" if def_ is not None else "  skip"
        print(f"  {k:>4}  {k/q:>6.3f}  {R_q:>10.6f}  {len(G):>5}  {def_str:>8}")
        bridge_data.append({"k": k, "k_over_q": k/q, "R_at_q": R_q, "|G|": len(G)})

    R_qm1 = harmonic_resonance(q-1, q)
    R_pred = 1.0/(q-1)**2
    match = abs(R_qm1 - R_pred) < 1e-10
    print(f"  → R(q-1,1/q)={R_qm1:.8f}  1/(q-1)²={R_pred:.8f}  exact match: {match}")
    bridge_results.append({
        "b": b, "p": p, "q": q, "bridge": bridge_data,
        "R_at_qm1": R_qm1, "R_pred": R_pred, "exact_match": match
    })

with open(OUT / "C_bridge_pre_echo.json", "w") as f:
    json.dump(bridge_results, f, indent=2)


# ── Section D: Three-factor nested cascade ─────────────────────────────────────
print("\n" + "="*70)
print("SECTION D: Three-factor nested cascade — triple ghost gates")
print("="*70)

THREE_FACTOR = [
    (30,  2, 3, 5),  (42,  2, 3, 7),  (66,  2, 3, 11), (70,  2, 5, 7),
    (105, 3, 5, 7),  (165, 3, 5, 11), (231, 3, 7, 11),  (385, 5, 7, 11),
    (1001,7,11,13),  (2431,11,13,17),
]
cascade_results = []

for b, p, q, r in THREE_FACTOR:
    print(f"\n  b={b} ({p}×{q}×{r})  three ghost gates at k={p},{q},{r}")

    # Zone 1: pre-echo of p (and already q, r are casting shadows)
    print(f"  Zone 1 k=1..{p-1}: before p={p}")
    z1 = []
    for k in range(1, p):
        Rp = harmonic_resonance(k, p)
        Rq = harmonic_resonance(k, q)
        Rr = harmonic_resonance(k, r)
        def_ = closure_defect(k, b) if k <= 12 else None
        print(f"    k={k}: R(p)={Rp:.4f} R(q)={Rq:.4f} R(r)={Rr:.4f}" +
              (f" def={def_:.4f}" if def_ is not None else ""))
        z1.append({"k": k, "Rp": Rp, "Rq": Rq, "Rr": Rr})

    # Zone 2: bridge p..q-1 — pre-echo of q and r simultaneously
    print(f"  Zone 2 k={p}..{q-1}: bridge p→q, pre-echo of q={q} and r={r}")
    z2 = []
    for k in range(p, q):
        Rq = harmonic_resonance(k, q)
        Rr = harmonic_resonance(k, r)
        G  = G_elements(k, b)
        print(f"    k={k}: |G|={len(G)} R(q)={Rq:.4f} R(r)={Rr:.4f}")
        z2.append({"k": k, "|G|": len(G), "Rq": Rq, "Rr": Rr})

    # Zone 3: bridge q..r-1 — pre-echo of r only
    print(f"  Zone 3 k={q}..{r-1}: bridge q→r, pre-echo of r={r}")
    z3 = []
    for k in range(q, r):
        Rr = harmonic_resonance(k, r)
        G  = G_elements(k, b)
        print(f"    k={k}: |G|={len(G)} R(r)={Rr:.4f}")
        z3.append({"k": k, "|G|": len(G), "Rr": Rr})

    # Verify 1/(n-1)^2 law at ALL three gates
    Rpm1 = harmonic_resonance(p-1, p) if p > 2 else 1.0
    Rqm1 = harmonic_resonance(q-1, q)
    Rrm1 = harmonic_resonance(r-1, r)
    print(f"  Gate laws: R(p-1,p)={Rpm1:.6f}=1/{(p-1)**2}?{1/(p-1)**2:.6f}  "
          f"R(q-1,q)={Rqm1:.6f}=1/{(q-1)**2}?{1/(q-1)**2:.6f}  "
          f"R(r-1,r)={Rrm1:.6f}=1/{(r-1)**2}?{1/(r-1)**2:.6f}")

    cascade_results.append({
        "b": b, "p": p, "q": q, "r": r,
        "zone1": z1, "zone2": z2, "zone3": z3,
        "gate_laws": {
            "Rpm1": Rpm1, "pred_p": 1/(p-1)**2,
            "Rqm1": Rqm1, "pred_q": 1/(q-1)**2,
            "Rrm1": Rrm1, "pred_r": 1/(r-1)**2,
        }
    })

with open(OUT / "D_cascade.json", "w") as f:
    json.dump(cascade_results, f, indent=2)


# ── Section E: Fixed-p scaling law ────────────────────────────────────────────
print("\n" + "="*70)
print("SECTION E: Fixed-p scaling — p=7 fixed, q varies 11..71")
print("="*70)

FIXED_P = 7
q_vals = [q for q in range(FIXED_P+2, 80) if is_prime(q)]
scaling_results = []

print(f"  {'q':>4}  {'b':>6}  {'br_len':>6}  "
      f"{'R(p-1,1/p)':>12}  {'R(q-1,1/q)':>12}  "
      f"{'def(p-1)':>10}  {'def(q-1)':>10}")
for q in q_vals:
    b = FIXED_P * q
    Rpm1_p = harmonic_resonance(FIXED_P-1, FIXED_P)   # constant — p=7 only
    Rqm1_q = harmonic_resonance(q-1, q)                # 1/(q-1)^2
    def_pm1 = closure_defect(FIXED_P-1, b)             # varies with b!
    def_qm1 = closure_defect(q-1, b) if q <= 30 else None
    bridge = q - FIXED_P
    def_q_str = f"{def_qm1:.6f}" if def_qm1 is not None else "    skip"
    print(f"  {q:>4}  {b:>6}  {bridge:>6}  "
          f"{Rpm1_p:>12.6f}  {Rqm1_q:>12.6f}  "
          f"{def_pm1:>10.6f}  {def_q_str:>10}")
    scaling_results.append({
        "q": q, "b": b, "bridge_len": bridge,
        "R_pm1_p": Rpm1_p, "R_qm1_q": Rqm1_q,
        "def_pm1": def_pm1, "def_qm1": def_qm1,
        "R_pred_q": 1/(q-1)**2,
    })

print(f"\n  Note: R(p-1,1/p) is CONSTANT across all q — resonance is p-only signal")
print(f"  Note: closure defect at k=p-1 VARIES with q — ring signal depends on b")
with open(OUT / "E_fixed_p_scaling.json", "w") as f:
    json.dump(scaling_results, f, indent=2)


# ── Section F: Cross-ω comparison ─────────────────────────────────────────────
print("\n" + "="*70)
print("SECTION F: Cross-ω — same first prime p, different ring structure")
print("="*70)

CROSS_OMEGA = [
    # b,    omega, p,  q,    r     (p=7 everywhere or p=5)
    (49,    1,     7,  None, None),  # 7^2
    (343,   1,     7,  None, None),  # 7^3
    (77,    2,     7,  11,   None),  # 7×11
    (91,    2,     7,  13,   None),  # 7×13
    (119,   2,     7,  17,   None),  # 7×17
    (1001,  3,     7,  11,   13),    # 7×11×13
    (1463,  3,     7,  11,   19),    # 7×11×19
    # Also p=5 series
    (25,    1,     5,  None, None),  # 5^2
    (35,    2,     5,  7,    None),  # 5×7
    (55,    2,     5,  11,   None),  # 5×11
    (385,   3,     5,  7,    11),    # 5×7×11
]
cross_results = []

prev_p = None
for b, om, p, q, r in CROSS_OMEGA:
    if p != prev_p:
        print(f"\n  --- p={p} series ---")
        print(f"  {'b':>6}  {'ω':>3}  {'k':>3}  "
              f"{'R(k,1/p)':>10}  {'defect':>8}  {'|G|':>5}  note")
        prev_p = p
    world_data = []
    for k in range(1, p+1):
        Rp   = harmonic_resonance(k, p)
        def_ = closure_defect(k, b)
        G    = G_elements(k, b)
        note = "← First-G" if k == p else ""
        print(f"  {b:>6}  {om:>3}  {k:>3}  {Rp:>10.6f}  {def_:>8.4f}  {len(G):>5}  {note}")
        world_data.append({"k": k, "R_p": Rp, "defect": def_, "|G|": len(G)})
    cross_results.append({"b": b, "omega": om, "p": p, "data": world_data})

print("\n  Key finding: R(k,1/p) is IDENTICAL for all b with same p — it is purely")
print("  a function of k and p. Only closure defect varies with omega(b).")
with open(OUT / "F_cross_omega.json", "w") as f:
    json.dump(cross_results, f, indent=2)


# ── Section G: Closed-form resonance verification ─────────────────────────────
print("\n" + "="*70)
print("SECTION G: Closed-form verification — R(k,f) = sin²(πk/f)/(k² sin²(π/f))")
print("="*70)

print("\n  Checking against numerical sum for primes p=3..23, k=1..p:")
print(f"  {'p':>4}  {'k':>4}  {'R_sum':>12}  {'R_closed':>12}  {'error':>12}")
max_cf_err = 0.0
cf_results = []
for p in [3,5,7,11,13,17,19,23,29,37,47]:
    for k in range(1, p+2):
        R_sum    = harmonic_resonance(k, p)
        R_closed = harmonic_resonance_exact(k, p)
        err = abs(R_sum - R_closed)
        if err > max_cf_err: max_cf_err = err
        print(f"  {p:>4}  {k:>4}  {R_sum:>12.8f}  {R_closed:>12.8f}  {err:>12.2e}")
        cf_results.append({"p": p, "k": k, "R_sum": R_sum, "R_closed": R_closed, "error": err})
print(f"\n  Max closed-form error: {max_cf_err:.2e}  (should be floating-point noise only)")

# Also derive and print the law at k=f-1 analytically
print("\n  Analytical proof of R(f-1, f) = 1/(f-1)²:")
print("    Σ_{x=1}^{f-1} exp(2πix/f) = [full period sum] - [x=0 term] = 0 - 1 = -1")
print("    |Σ|² = 1,  so R = 1/(f-1)²  ■")
print("\n  Analytical proof of R(f, f) = 0:")
print("    Σ_{x=1}^{f} exp(2πix/f) = Σ_{x=0}^{f-1} exp(2πix/f) = 0  (roots of unity)")
print("    R = 0  ■")

with open(OUT / "G_closed_form.json", "w") as f:
    json.dump(cf_results, f, indent=2)


# ── Plots ──────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("GENERATING PLOTS")
print("="*70)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # ── Fig 1: Macro sweep dashboard ──
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "Pre-Echo Deep Atlas — Macro Survey (150+ semiprimes)\n"
        "Insight: C.A. Luther  |  Verification: B. Sanders / 7Site LLC",
        fontsize=11)

    ax = axes[0,0]
    ps_unique = sorted(set(r["p"] for r in macro_results))
    colors = plt.cm.plasma(np.linspace(0, 1, len(ps_unique)))
    for p_val, col in zip(ps_unique, colors):
        rows = [r for r in macro_results if r["p"] == p_val]
        qs_r = [r["q_over_p"] for r in rows]
        Rvals = [r["R_pm1"] for r in rows]
        ax.scatter(qs_r, Rvals, s=30, color=col, alpha=0.7, label=f"p={p_val}")
    ax.set_xlabel("q/p"); ax.set_ylabel("R(p-1, 1/p)")
    ax.set_title("R(p-1,1/p) vs q/p: q-independence confirmed\n"
                 "Each horizontal band = one prime p")
    ax.legend(fontsize=6, ncol=3); ax.grid(True, alpha=0.3)

    ax = axes[0,1]
    ps_arr  = np.array([r["p"] for r in macro_results])
    def_arr = np.array([r["defect_pm1"] for r in macro_results])
    R_arr   = np.array([r["R_pm1"] for r in macro_results])
    sc = ax.scatter(ps_arr, def_arr, c=[r["q_over_p"] for r in macro_results],
                    cmap='viridis', s=20, alpha=0.7)
    plt.colorbar(sc, ax=ax, label='q/p')
    ax.set_xlabel("p"); ax.set_ylabel("Closure defect at k=p-1")
    ax.set_title("Pre-Echo Defect vs p (colored by q/p)\n"
                 "Defect depends on BOTH p and q")
    ax.grid(True, alpha=0.3)

    ax = axes[1,0]
    for p_val, col in zip([5,7,11,13,17,19,23], plt.cm.tab10(np.linspace(0,1,7))):
        ks_norm = np.linspace(0.1, 1.0, 100)
        Rs = [harmonic_resonance_exact(max(1, int(t*(p_val-1)+0.5)), p_val) for t in ks_norm]
        ax.plot(ks_norm, Rs, color=col, lw=1.5, label=f"p={p_val}")
    ax.axvline(1.0, color='red', lw=1.5, linestyle='--', label='k=p-1 boundary')
    ax.set_xlabel("k/(p-1)"); ax.set_ylabel("R(k, 1/p)")
    ax.set_title("Harmonic Resonance Decay Curves\n"
                 "sin²(πk/p) / (k² sin²(π/p)) — closed form")
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    ax = axes[1,1]
    errs = [r["R_error"] for r in macro_results]
    ax.semilogy(range(len(errs)), errs, '.', alpha=0.5, markersize=3)
    ax.axhline(1e-10, color='red', linestyle='--', label='1e-10 (float noise)')
    ax.set_xlabel("semiprime index"); ax.set_ylabel("R error vs 1/(p-1)²")
    ax.set_title("Residual error: R(p-1,1/p) - 1/(p-1)²\n"
                 "All errors are floating-point noise only")
    ax.legend(); ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUT / "fig1_macro.png", dpi=120, bbox_inches='tight')
    print("Saved: fig1_macro.png")
    plt.close()

    # ── Fig 2: Spectral fingerprint heat maps ──
    n_worlds = len(SPECTRAL_WORLDS)
    fig, axes = plt.subplots(1, n_worlds, figsize=(4*n_worlds, 7))
    fig.suptitle(
        "Spectral Fingerprint: R(k, f) — which prime frequencies resonate at each k?\n"
        "Insight: C.A. Luther  |  Verification: B. Sanders / 7Site LLC",
        fontsize=11)

    for ax, entry in zip(axes, spectral_results):
        b, p, q = entry["b"], entry["p"], entry["q"]
        freqs = entry["freqs"]
        ks_plot = sorted(int(k) for k in entry["matrix"].keys())
        Z = np.array([[entry["matrix"][str(k)].get(str(f), 0)
                       for f in freqs] for k in ks_plot])
        im = ax.imshow(Z.T, aspect='auto', origin='lower',
                       extent=[min(ks_plot)-0.5, max(ks_plot)+0.5, -0.5, len(freqs)-0.5],
                       cmap='inferno', vmin=0, vmax=1)
        ax.set_yticks(range(len(freqs)))
        ax.set_yticklabels([str(f) for f in freqs], fontsize=7)
        ax.axvline(p, color='cyan', lw=2, linestyle='--')
        ax.axvline(q, color='lime', lw=2, linestyle='--')
        p_idx = freqs.index(p) if p in freqs else -1
        q_idx = freqs.index(q) if q in freqs else -1
        if p_idx >= 0: ax.axhline(p_idx, color='cyan', lw=1.5, alpha=0.6)
        if q_idx >= 0: ax.axhline(q_idx, color='lime', lw=1.5, alpha=0.6)
        ax.set_title(f"b={b} ({p}×{q})\ncyan=k=p, lime=k=q", fontsize=9)
        ax.set_xlabel("k")
        if ax is axes[0]: ax.set_ylabel("prime freq f")

    plt.colorbar(im, ax=axes[-1], label='R(k,f)', shrink=0.8)
    plt.tight_layout()
    plt.savefig(OUT / "fig2_spectral.png", dpi=120, bbox_inches='tight')
    print("Saved: fig2_spectral.png")
    plt.close()

    # ── Fig 3: Bridge pre-echo ──
    fig, axes = plt.subplots(2, 4, figsize=(18, 10))
    fig.suptitle(
        "Bridge Pre-Echo: R(k, 1/q) in Bridge Zone k=p..q-1\n"
        "C.A. Luther | B. Sanders / 7Site LLC",
        fontsize=11)
    for ax, entry in zip(axes.flat, bridge_results[:8]):
        b, p, q = entry["b"], entry["p"], entry["q"]
        ks_n = [d["k_over_q"] for d in entry["bridge"]]
        Rs_q = [d["R_at_q"] for d in entry["bridge"]]
        ax.plot(ks_n, Rs_q, 'o-', color='purple', markersize=6, linewidth=2)
        # Theoretical endpoint
        ax.axhline(1/(q-1)**2, color='red', linestyle='--',
                   label=f"1/(q-1)²={1/(q-1)**2:.4f}")
        ax.axvline(1.0, color='lime', linestyle=':', lw=1.5, label=f"k=q={q}")
        ax.set_xlabel("k/q"); ax.set_ylabel("R(k, 1/q)")
        ax.set_title(f"b={b} ({p}×{q})\nbridge len={q-p}", fontsize=9)
        ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "fig3_bridge.png", dpi=120, bbox_inches='tight')
    print("Saved: fig3_bridge.png")
    plt.close()

    # ── Fig 4: Three-factor cascade ──
    fig, axes = plt.subplots(2, 5, figsize=(22, 9))
    fig.suptitle(
        "Triple Ghost Gates: p-echo → q-echo → r-echo in Three-Factor Numbers\n"
        "C.A. Luther | B. Sanders / 7Site LLC",
        fontsize=11)
    for ax, entry in zip(axes.flat, cascade_results[:10]):
        b, p, q, r = entry["b"], entry["p"], entry["q"], entry["r"]
        all_k, Rp_all, Rq_all, Rr_all = [], [], [], []
        for row in entry["zone1"]:
            all_k.append(row["k"]); Rp_all.append(row["Rp"])
            Rq_all.append(row["Rq"]); Rr_all.append(row["Rr"])
        for row in entry["zone2"]:
            all_k.append(row["k"]); Rp_all.append(0.0)
            Rq_all.append(row["Rq"]); Rr_all.append(row["Rr"])
        for row in entry["zone3"]:
            all_k.append(row["k"]); Rp_all.append(0.0)
            Rq_all.append(0.0);     Rr_all.append(row["Rr"])
        ax.plot(all_k, Rp_all, 'b-o', ms=4, lw=1.5, label=f"R(1/p={p})")
        ax.plot(all_k, Rq_all, 'g-s', ms=4, lw=1.5, label=f"R(1/q={q})")
        ax.plot(all_k, Rr_all, 'r-^', ms=4, lw=1.5, label=f"R(1/r={r})")
        ax.axvline(p, color='blue',  lw=1, linestyle=':', alpha=0.8)
        ax.axvline(q, color='green', lw=1, linestyle=':', alpha=0.8)
        ax.axvline(r, color='red',   lw=1, linestyle=':', alpha=0.8)
        ax.set_title(f"b={b} ({p}×{q}×{r})", fontsize=9)
        ax.set_xlabel("k"); ax.legend(fontsize=7); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "fig4_cascade.png", dpi=120, bbox_inches='tight')
    print("Saved: fig4_cascade.png")
    plt.close()

    # ── Fig 5: Fixed-p scaling ──
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(
        f"Fixed-p Scaling: p={FIXED_P}, q varies — what's q-independent vs q-dependent?\n"
        "C.A. Luther | B. Sanders / 7Site LLC",
        fontsize=11)
    qs_sc   = [r["q"] for r in scaling_results]
    Rp_all  = [r["R_pm1_p"] for r in scaling_results]
    Rq_all  = [r["R_qm1_q"] for r in scaling_results]
    def_all = [r["def_pm1"] for r in scaling_results]
    pred_q  = [r["R_pred_q"] for r in scaling_results]

    axes[0].plot(qs_sc, Rp_all, 'b-o', ms=5, label=f"R(p-1=6, 1/p=7)")
    axes[0].axhline(1/(FIXED_P-1)**2, color='red', linestyle='--',
                    label=f"1/(p-1)²={1/(FIXED_P-1)**2:.4f}")
    axes[0].set_xlabel("q"); axes[0].set_ylabel("R(p-1, 1/p)")
    axes[0].set_title(f"R(p-1,1/p) is CONSTANT\n(independent of q — pure p signal)")
    axes[0].legend(fontsize=8); axes[0].grid(True, alpha=0.3)

    axes[1].plot(qs_sc, Rq_all, 'g-o', ms=5, label="R(q-1, 1/q) measured")
    axes[1].plot(qs_sc, pred_q, 'r--', lw=2, label="1/(q-1)²")
    axes[1].set_xlabel("q"); axes[1].set_ylabel("R(q-1, 1/q)")
    axes[1].set_title("R(q-1,1/q) = 1/(q-1)² exactly\n(countdown clock to second gate)")
    axes[1].legend(fontsize=8); axes[1].grid(True, alpha=0.3)

    axes[2].plot(qs_sc, def_all, 'darkorange', marker='o', ms=5)
    axes[2].set_xlabel("q"); axes[2].set_ylabel("Closure defect at k=p-1")
    axes[2].set_title("Defect at end of pre-echo zone\nVARIES with q (ring-theoretic signal)")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUT / "fig5_scaling.png", dpi=120, bbox_inches='tight')
    print("Saved: fig5_scaling.png")
    plt.close()

    print("\nAll plots complete.")

except Exception as e:
    import traceback
    print(f"Plot error: {e}")
    traceback.print_exc()

print("\n" + "="*70)
print("DEEP PRE-ECHO ATLAS COMPLETE")
print(f"Results: {OUT}")
print("="*70)
