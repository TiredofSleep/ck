"""
r16_extended_algebra.py
=======================
Extended finite algebra survey — three new territories beyond semiprimes:

  1. PRIME POWERS  (b = p^n, n=2..5)
     G_k = multiples of p — single arithmetic progression, perfect dispersion 1/p.
     Rich structure: how does gate difficulty change as the exponent grows?

  2. THREE-FACTOR NUMBERS  (b = p*q*r, three distinct primes)
     G_k = three interleaved arithmetic progressions.
     Inclusion-exclusion creates richer cancellation patterns.
     Dispersion is a three-frequency beat — maximum complexity.

  3. TRANSITION CORRIDORS  (neighborhood of k = p, the First-G event)
     For each semiprime/prime-power b, sweep k = max(2, p-3) .. min(b-1, 3p).
     Measures how sharply gate difficulty rises after first G appearance.
     Tests C.A. Luther's dispersion conjecture: corridor shape = f(dispersion).

All invariants computed exactly. No sampling for algebra; gate rates via
greedy descent (n_steps=200, n_trials=300) — fast, directional signal.

Usage:
    python r16_extended_algebra.py                    # all three surveys
    python r16_extended_algebra.py --prime_powers     # prime powers only
    python r16_extended_algebra.py --three_factor     # 3-factor only
    python r16_extended_algebra.py --corridors        # transition corridors only
    python r16_extended_algebra.py --b_max 200        # up to b=200

Author: Brayden Sanders / 7Site LLC | Dispersion insight: C.A. Luther
Date: March 2026 | DOI: 10.5281/zenodo.18852047
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

import argparse
import json
import os
import random as _random
import time
from math import gcd
from collections import defaultdict

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


# ═══════════════════════════════════════════════════════════════════════════════
#  NUMBER THEORY UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def sieve(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n+1, i):
                is_p[j] = False
    return [i for i in range(2, n+1) if is_p[i]]


def factorize(b, primes):
    """Full prime factorization: returns {p: exp, ...}."""
    factors = {}
    for p in primes:
        if p * p > b:
            break
        while b % p == 0:
            factors[p] = factors.get(p, 0) + 1
            b //= p
    if b > 1:
        factors[b] = factors.get(b, 0) + 1
    return factors


def is_prime_power(b, primes):
    """Return (True, p, n) if b = p^n, else (False, 0, 0)."""
    factors = factorize(b, primes)
    if len(factors) == 1:
        p, n = list(factors.items())[0]
        if n >= 2:
            return True, p, n
    return False, 0, 0


def is_three_factor(b, primes):
    """Return (True, p, q, r) if b = p*q*r distinct primes, else (False,...)."""
    factors = factorize(b, primes)
    if len(factors) == 3 and all(e == 1 for e in factors.values()):
        ps = sorted(factors.keys())
        return True, ps[0], ps[1], ps[2]
    return False, 0, 0, 0


def euler_totient(b, factors):
    """phi(b) from factorization."""
    result = b
    for p in factors:
        result = result * (p - 1) // p
    return result


# ═══════════════════════════════════════════════════════════════════════════════
#  ALGEBRAIC INVARIANTS  (exact, no sampling)
# ═══════════════════════════════════════════════════════════════════════════════

def compute_invariants(b, k, factors, label):
    """Full exact invariants for alphabet {1..k} mod b."""
    C = [x for x in range(1, k+1) if gcd(x, b) == 1]
    G = [x for x in range(1, k+1) if gcd(x, b) > 1]
    nC, nG = len(C), len(G)

    # Multiplication table
    T = np.array([[(i*j) % b for j in range(1, k+1)]
                  for i in range(1, k+1)], dtype=np.int32)

    n_unit = n_zero = n_mid = 0
    for v in T.flat:
        v = int(v)
        if v == 0: n_zero += 1
        elif gcd(v, b) == 1: n_unit += 1
        else: n_mid += 1
    total = k * k

    # Interleave / dispersion
    seq = [1 if gcd(x, b) == 1 else 0 for x in range(1, k+1)]
    transitions = sum(1 for i in range(len(seq)-1) if seq[i] != seq[i+1])
    min_cg = min(nC, nG) if nC > 0 and nG > 0 else 1
    interleave = transitions / (2 * min_cg) if (nC > 0 and nG > 0) else 0.0

    # Dispersion: average gap between consecutive G elements
    g_positions = [i for i, x in enumerate(range(1, k+1)) if gcd(x, b) > 1]
    if len(g_positions) >= 2:
        gaps = [g_positions[i+1] - g_positions[i] for i in range(len(g_positions)-1)]
        dispersion_gap = sum(gaps) / len(gaps)
        dispersion_spread = max(gaps) - min(gaps)  # 0 = perfectly regular
    elif len(g_positions) == 1:
        dispersion_gap = k  # only one G element
        dispersion_spread = 0.0
    else:
        dispersion_gap = float('inf')
        dispersion_spread = 0.0

    phi_b = euler_totient(b, factors)
    smallest_prime = min(factors.keys())

    return {
        "b": b, "k": k, "label": label,
        "factors": {str(p): e for p, e in factors.items()},
        "phi_b": phi_b, "smallest_prime": smallest_prime,
        "nC": nC, "nG": nG,
        "unit_frac": nC / k,
        "unit_density":    n_unit / total,
        "zero_density":    n_zero / total,
        "nonunit_density": n_mid  / total,
        "interleave": round(interleave, 4),
        "dispersion_gap": round(dispersion_gap, 3) if dispersion_gap != float('inf') else None,
        "dispersion_spread": round(dispersion_spread, 3),
        "dispersion_regular": dispersion_spread == 0.0 and nG > 0,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  GATE RATE (fast, single-threaded, directional signal only)
# ═══════════════════════════════════════════════════════════════════════════════

def _obj(T, k, b):
    gate = har = gstay = 0
    for i in range(k):
        for j in range(k):
            v = int(T[i, j])
            if gcd(v, b) == 1:
                gate += 1
                if v == T[i, i]: har += 1
        if int(T[i, i]) != 0 and gcd(int(T[i, i]), b) > 1:
            gstay += 1
    n = k * k
    return 0.50*gate/n + 0.25*har/n + 0.25*(1 - gstay/k)


def gate_rate(b, k, n_trials=300, n_steps=200, seed=0):
    """Fast directional gate rate estimate."""
    if k >= b:
        return None
    G = [x for x in range(1, k+1) if gcd(x, b) > 1]
    if not G:
        return 1.0  # trivially gated — no obstruction

    wins = 0
    rng = _random.Random(seed)
    for trial in range(n_trials):
        perm = rng.sample(list(range(1, k+1)), k)
        T = np.array([[(perm[i]*perm[j]) % b for j in range(k)]
                      for i in range(k)], dtype=np.int32)
        score = _obj(T, k, b)
        for _ in range(n_steps):
            a, bb = rng.randrange(k), rng.randrange(k)
            T2 = T.copy()
            T2[[a, bb]] = T2[[bb, a]]
            T2[:, [a, bb]] = T2[:, [bb, a]]
            s2 = _obj(T2, k, b)
            if s2 >= score:
                T, score = T2, s2
        if score >= 0.85:
            wins += 1
    return wins / n_trials


# ═══════════════════════════════════════════════════════════════════════════════
#  1. PRIME POWERS
# ═══════════════════════════════════════════════════════════════════════════════

def survey_prime_powers(b_max, n_trials, n_steps, save_dir):
    print("\n" + "="*60)
    print("PRIME POWERS: b = p^n, n=2..5")
    print("="*60)

    primes = sieve(b_max)
    results = []

    for p in primes:
        for n in range(2, 6):
            b = p ** n
            if b > b_max:
                break
            factors = {p: n}
            label = f"p{p}^{n}"

            k_values = list(range(2, min(b, 31)))
            print(f"\n  b={b} ({p}^{n})  k=2..{min(b-1,30)}")

            for k in k_values:
                inv = compute_invariants(b, k, factors, label)
                gr = gate_rate(b, k, n_trials, n_steps)
                inv["gate_rate"] = gr
                inv["n_trials"] = n_trials
                inv["n_steps"] = n_steps
                results.append(inv)

                G = [x for x in range(1, k+1) if gcd(x, b) > 1]
                if G:
                    print(f"    k={k:2d} |G|={len(G):2d} interleave={inv['interleave']:.3f} "
                          f"disp_gap={inv['dispersion_gap']} "
                          f"regular={inv['dispersion_regular']} "
                          f"gate={gr:.3f}")

    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "prime_powers_atlas.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {path}  ({len(results)} rows)")

    _analyze_prime_powers(results)
    if HAS_MPL:
        _plot_prime_powers(results, save_dir)
    return results


def _analyze_prime_powers(results):
    print("\n--- PRIME POWER ANALYSIS ---")
    # Compare same p, different n
    by_p = defaultdict(list)
    for r in results:
        if r["nG"] > 0:
            p = r["smallest_prime"]
            by_p[p].append(r)

    print("  Dispersion regularity: prime powers have perfectly regular G spacing?")
    all_regular = all(r["dispersion_regular"] for r in results if r["nG"] >= 2)
    print(f"  All prime powers have regular dispersion: {all_regular}")

    print("\n  Gate rate by exponent (at k=9 where available):")
    by_exp = defaultdict(list)
    for r in results:
        if r["k"] == 9 and r["gate_rate"] is not None:
            n = list(r["factors"].values())[0]
            by_exp[n].append(r)
    for n in sorted(by_exp):
        rows = by_exp[n]
        avg = sum(r["gate_rate"] for r in rows) / len(rows)
        print(f"  n={n}: {len(rows)} worlds  avg_gate_rate={avg:.3f}")


def _plot_prime_powers(results, save_dir):
    # Unit density evolution for each prime base
    by_p = defaultdict(list)
    for r in results:
        p = r["smallest_prime"]
        by_p[p].append(r)

    primes_seen = sorted(by_p.keys())
    n_p = len(primes_seen)
    if n_p == 0:
        return

    fig, axes = plt.subplots(2, n_p, figsize=(4*n_p, 7))
    if n_p == 1:
        axes = axes.reshape(2, 1)

    fig.suptitle("Prime Powers: unit density + gate rate evolution (p fixed, n varies)",
                 fontsize=11, fontweight="bold")

    CMAP_TERNARY = mcolors.LinearSegmentedColormap.from_list(
        "ternary", [(0.0,"#c0392b"),(0.5,"#f5f5f5"),(1.0,"#1a4f7a")])

    for ci, p in enumerate(primes_seen):
        rows = sorted(by_p[p], key=lambda r: (list(r["factors"].values())[0], r["k"]))
        exponents = sorted(set(list(r["factors"].values())[0] for r in rows))
        k_vals = sorted(set(r["k"] for r in rows))

        # Unit density heatmap
        ax_u = axes[0][ci]
        lookup_ud = {(list(r["factors"].values())[0], r["k"]): r["unit_density"]
                     for r in rows}
        data = np.full((len(exponents), len(k_vals)), np.nan)
        for ri, n in enumerate(exponents):
            for ci2, k in enumerate(k_vals):
                v = lookup_ud.get((n, k))
                if v is not None:
                    data[ri, ci2] = v
        im = ax_u.imshow(data, cmap="RdYlGn", vmin=0, vmax=1,
                         aspect="auto", interpolation="nearest")
        ax_u.set_title(f"p={p}: unit density", fontsize=9)
        ax_u.set_xticks(range(len(k_vals)))
        ax_u.set_xticklabels([str(k) for k in k_vals], fontsize=5, rotation=45)
        ax_u.set_yticks(range(len(exponents)))
        ax_u.set_yticklabels([f"p^{n}" for n in exponents], fontsize=7)

        # Gate rate heatmap
        ax_g = axes[1][ci]
        lookup_gr = {(list(r["factors"].values())[0], r["k"]): r["gate_rate"]
                     for r in rows if r["gate_rate"] is not None}
        data_g = np.full((len(exponents), len(k_vals)), np.nan)
        for ri, n in enumerate(exponents):
            for ci2, k in enumerate(k_vals):
                v = lookup_gr.get((n, k))
                if v is not None:
                    data_g[ri, ci2] = v
        ax_g.imshow(data_g, cmap="RdYlGn", vmin=0, vmax=1,
                    aspect="auto", interpolation="nearest")
        ax_g.set_title(f"p={p}: gate rate", fontsize=9)
        ax_g.set_xticks(range(len(k_vals)))
        ax_g.set_xticklabels([str(k) for k in k_vals], fontsize=5, rotation=45)
        ax_g.set_yticks(range(len(exponents)))
        ax_g.set_yticklabels([f"p^{n}" for n in exponents], fontsize=7)

    plt.tight_layout()
    path = os.path.join(save_dir, "prime_powers_atlas.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    print(f"Saved: {path}")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  2. THREE-FACTOR NUMBERS
# ═══════════════════════════════════════════════════════════════════════════════

def survey_three_factor(b_max, n_trials, n_steps, save_dir):
    print("\n" + "="*60)
    print("THREE-FACTOR NUMBERS: b = p*q*r, distinct primes")
    print("="*60)

    primes = sieve(b_max)
    prime_set = set(primes)
    results = []

    three_factors = []
    for b in range(2, b_max + 1):
        ok, p, q, r = is_three_factor(b, primes)
        if ok:
            three_factors.append((b, p, q, r))

    print(f"Found {len(three_factors)} three-factor numbers up to b={b_max}")

    for b, p, q, r in three_factors:
        factors = {p: 1, q: 1, r: 1}
        label = f"{p}x{q}x{r}"
        print(f"\n  b={b} ({label})")

        for k in range(2, min(b, 31)):
            inv = compute_invariants(b, k, factors, label)
            gr = gate_rate(b, k, n_trials, n_steps)
            inv["gate_rate"] = gr
            inv["n_trials"] = n_trials
            inv["n_steps"] = n_steps
            inv["p"] = p
            inv["q"] = q
            inv["r"] = r
            results.append(inv)

            G = [x for x in range(1, k+1) if gcd(x, b) > 1]
            if G and k <= 15:
                print(f"    k={k:2d} |G|={len(G):2d} interleave={inv['interleave']:.3f} "
                      f"disp_gap={inv['dispersion_gap']} "
                      f"gate={gr:.3f}")

    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "three_factor_atlas.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {path}  ({len(results)} rows)")

    _analyze_three_factor(results)
    if HAS_MPL:
        _plot_three_factor(results, save_dir)
    return results


def _analyze_three_factor(results):
    print("\n--- THREE-FACTOR ANALYSIS ---")

    # Compare to semiprimes: does 3-factor give higher/lower interleave?
    with_G = [r for r in results if r["nG"] > 0]
    if with_G:
        avg_il = sum(r["interleave"] for r in with_G) / len(with_G)
        max_il = max(r["interleave"] for r in with_G)
        at_max = sum(1 for r in with_G if r["interleave"] >= 0.95)
        print(f"  3-factor interleave: avg={avg_il:.3f}  max={max_il:.3f}")
        print(f"  Worlds with interleave>=0.95: {at_max}/{len(with_G)}")

    # Dispersion regularity: 3-factor = three arithmetic progressions, less regular
    regular = [r for r in results if r["nG"] >= 2 and r["dispersion_regular"]]
    irregular = [r for r in results if r["nG"] >= 2 and not r["dispersion_regular"]]
    print(f"  Regular dispersion: {len(regular)}  Irregular: {len(irregular)}")
    print(f"  (3-factor expected mostly irregular — three beat frequencies)")

    # Gate rates at k=9
    at_k9 = [r for r in results if r["k"] == 9 and r["gate_rate"] is not None]
    if at_k9:
        avg_gr = sum(r["gate_rate"] for r in at_k9) / len(at_k9)
        print(f"\n  Gate rate at k=9: {len(at_k9)} worlds  avg={avg_gr:.3f}")
        # Compare small vs large p
        small_p = [r for r in at_k9 if r["smallest_prime"] == 2]
        large_p = [r for r in at_k9 if r["smallest_prime"] >= 5]
        if small_p:
            print(f"  spf=2: avg={sum(r['gate_rate'] for r in small_p)/len(small_p):.3f}")
        if large_p:
            print(f"  spf>=5: avg={sum(r['gate_rate'] for r in large_p)/len(large_p):.3f}")


def _plot_three_factor(results, save_dir):
    with_G = [r for r in results if r["nG"] > 0 and r["gate_rate"] is not None]
    if not with_G:
        return

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Three-Factor Numbers: interleave, dispersion, gate rate at k=9",
                 fontsize=11, fontweight="bold")

    # Plot 1: interleave vs |G| at k=9
    ax = axes[0]
    k9 = [r for r in with_G if r["k"] == 9]
    if k9:
        xs = [r["nG"] for r in k9]
        ys = [r["interleave"] for r in k9]
        ax.scatter(xs, ys, c=[r["gate_rate"] for r in k9],
                   cmap="RdYlGn", vmin=0, vmax=1, s=60, alpha=0.8)
        ax.set_xlabel("|G| at k=9"); ax.set_ylabel("Interleave")
        ax.set_title("Interleave vs |G| (color=gate rate)")

    # Plot 2: dispersion gap vs gate rate
    ax = axes[1]
    valid = [r for r in with_G if r["dispersion_gap"] is not None]
    if valid:
        xs = [r["dispersion_gap"] for r in valid]
        ys = [r["gate_rate"] for r in valid]
        cs = [r["interleave"] for r in valid]
        sc = ax.scatter(xs, ys, c=cs, cmap="viridis", vmin=0, vmax=1, s=40, alpha=0.7)
        plt.colorbar(sc, ax=ax, label="interleave")
        ax.set_xlabel("Dispersion gap (avg spacing between G elements)")
        ax.set_ylabel("Gate rate")
        ax.set_title("Dispersion → Gate Rate (C.A. Luther conjecture)")

    # Plot 3: unit density evolution for first few 3-factor b values
    ax = axes[2]
    b_vals = sorted(set(r["b"] for r in results))[:6]
    k_range = list(range(2, 30))
    for b in b_vals:
        b_rows = {r["k"]: r for r in results if r["b"] == b}
        ud = [b_rows[k]["unit_density"] if k in b_rows else np.nan for k in k_range]
        lbl = results[[r["b"] for r in results].index(b)]["label"]
        ax.plot(k_range, ud, label=f"b={b}({lbl})", linewidth=1.5)
    ax.set_xlabel("k"); ax.set_ylabel("Unit density")
    ax.set_title("Unit density evolution"); ax.legend(fontsize=7)
    ax.axhline(0.85, color="red", linestyle="--", linewidth=0.8, label="0.85 threshold")

    plt.tight_layout()
    path = os.path.join(save_dir, "three_factor_atlas.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    print(f"Saved: {path}")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  3. TRANSITION CORRIDORS  (neighborhood of k = p, the First-G event)
# ═══════════════════════════════════════════════════════════════════════════════

def survey_corridors(b_max, n_trials, n_steps, save_dir):
    print("\n" + "="*60)
    print("TRANSITION CORRIDORS: neighborhood of k = p (First-G event)")
    print("C.A. Luther dispersion conjecture: corridor shape = f(dispersion)")
    print("="*60)

    primes = sieve(b_max)
    prime_set = set(primes)
    results = []

    # Collect all semiprimes and prime powers
    worlds = []
    for b in range(4, b_max + 1):
        factors = factorize(b, primes)
        n_distinct = len(factors)
        total_exp = sum(factors.values())

        if n_distinct == 1 and total_exp >= 2:
            # Prime power
            p = list(factors.keys())[0]
            worlds.append((b, p, factors, f"p{p}^{total_exp}"))
        elif n_distinct == 2 and total_exp == 2:
            # Semiprime
            ps = sorted(factors.keys())
            p = ps[0]
            worlds.append((b, p, factors, f"{ps[0]}x{ps[1]}"))

    print(f"Surveying corridors for {len(worlds)} worlds up to b={b_max}")

    for b, p, factors, label in worlds:
        # Sweep k = max(2, p-3) .. min(b-1, 4*p)
        k_lo = max(2, p - 3)
        k_hi = min(b - 1, 4 * p)
        if k_lo >= k_hi:
            continue

        corridor = []
        for k in range(k_lo, k_hi + 1):
            inv = compute_invariants(b, k, factors, label)
            gr = gate_rate(b, k, n_trials, n_steps)
            inv["gate_rate"] = gr
            inv["k_rel"] = k - p    # position relative to First-G event
            inv["b_label"] = label
            corridor.append(inv)

        results.extend(corridor)

        # Print the corridor crossing
        print(f"\n  b={b:3d} ({label})  p={p}  corridor k={k_lo}..{k_hi}")
        for r in corridor:
            marker = " <<< FIRST G" if r["k_rel"] == 0 else ""
            print(f"    k={r['k']:2d} (k-p={r['k_rel']:+d}) "
                  f"|G|={r['nG']:2d} il={r['interleave']:.3f} "
                  f"disp={r['dispersion_gap']} "
                  f"gate={r['gate_rate']:.3f}{marker}")

    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, "corridor_atlas.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {path}  ({len(results)} rows)")

    _analyze_corridors(results)
    if HAS_MPL:
        _plot_corridors(results, save_dir)
    return results


def _analyze_corridors(results):
    print("\n--- CORRIDOR ANALYSIS ---")
    print("  Gate rate by position relative to First-G event (k_rel = k - p):")

    by_rel = defaultdict(list)
    for r in results:
        if r["gate_rate"] is not None:
            by_rel[r["k_rel"]].append(r["gate_rate"])

    for rel in sorted(by_rel.keys()):
        rates = by_rel[rel]
        avg = sum(rates) / len(rates)
        marker = " <<< k=p" if rel == 0 else ""
        print(f"    k_rel={rel:+d}: n={len(rates):3d}  avg_gate={avg:.3f}{marker}")

    # Test C.A. Luther conjecture: does dispersion predict gate rate in corridor?
    print("\n  Dispersion vs gate rate correlation in corridors:")
    valid = [r for r in results
             if r["gate_rate"] is not None
             and r["dispersion_gap"] is not None
             and r["nG"] > 0]
    if len(valid) > 5:
        xs = np.array([r["dispersion_gap"] for r in valid])
        ys = np.array([r["gate_rate"] for r in valid])
        corr = np.corrcoef(xs, ys)[0, 1]
        print(f"    dispersion_gap vs gate_rate: r = {corr:.3f}")
        xs2 = np.array([r["interleave"] for r in valid])
        corr2 = np.corrcoef(xs2, ys)[0, 1]
        print(f"    interleave vs gate_rate:     r = {corr2:.3f}")
        print(f"    (C.A. Luther: gate_rate ~ F(|G| x dispersion))")


def _plot_corridors(results, save_dir):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(
        "Transition Corridors: gate rate around k=p (First-G event)\n"
        "C.A. Luther: gate_rate = F_k(|G| × dispersion)",
        fontsize=11, fontweight="bold"
    )

    # Plot 1: average gate rate by k_rel
    ax = axes[0]
    by_rel = defaultdict(list)
    for r in results:
        if r["gate_rate"] is not None:
            by_rel[r["k_rel"]].append(r["gate_rate"])
    rels = sorted(by_rel.keys())
    avgs = [sum(by_rel[rel])/len(by_rel[rel]) for rel in rels]
    stds = [np.std(by_rel[rel]) for rel in rels]
    ax.errorbar(rels, avgs, yerr=stds, fmt='o-', color="#1a4f7a",
                capsize=4, linewidth=2, markersize=6)
    ax.axvline(0, color="red", linestyle="--", linewidth=1.5, label="k=p (First-G)")
    ax.set_xlabel("k - p  (position relative to First-G event)")
    ax.set_ylabel("Gate rate")
    ax.set_title("Gate rate corridor profile")
    ax.legend()

    # Plot 2: dispersion_gap vs gate_rate
    ax = axes[1]
    valid = [r for r in results
             if r["gate_rate"] is not None and r["dispersion_gap"] is not None
             and r["nG"] > 0]
    if valid:
        xs = [r["dispersion_gap"] for r in valid]
        ys = [r["gate_rate"] for r in valid]
        cs = [r["k_rel"] for r in valid]
        sc = ax.scatter(xs, ys, c=cs, cmap="coolwarm", s=30, alpha=0.7)
        plt.colorbar(sc, ax=ax, label="k_rel (k-p)")
        ax.set_xlabel("Dispersion gap (avg G spacing)")
        ax.set_ylabel("Gate rate")
        ax.set_title("Dispersion → Gate rate\n(C.A. Luther conjecture)")

    # Plot 3: corridor profile for selected worlds
    ax = axes[2]
    b_vals = sorted(set(r["b"] for r in results))[:8]
    for b in b_vals:
        b_rows = sorted([r for r in results if r["b"] == b and r["gate_rate"] is not None],
                        key=lambda r: r["k_rel"])
        if len(b_rows) < 3:
            continue
        rels = [r["k_rel"] for r in b_rows]
        rates = [r["gate_rate"] for r in b_rows]
        lbl = b_rows[0]["b_label"]
        ax.plot(rels, rates, 'o-', label=f"b={b}({lbl})", linewidth=1.5, markersize=4)
    ax.axvline(0, color="red", linestyle="--", linewidth=1, alpha=0.7)
    ax.set_xlabel("k - p"); ax.set_ylabel("Gate rate")
    ax.set_title("Individual corridor profiles")
    ax.legend(fontsize=6)

    plt.tight_layout()
    path = os.path.join(save_dir, "corridor_atlas.png")
    fig.savefig(path, dpi=120, bbox_inches="tight")
    print(f"Saved: {path}")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Extended finite algebra: prime powers, 3-factor, transition corridors")
    parser.add_argument("--b_max",        type=int, default=150)
    parser.add_argument("--n_trials",     type=int, default=300,
                        help="Gate rate trials per world (default 300)")
    parser.add_argument("--n_steps",      type=int, default=200,
                        help="Optimization steps per trial (default 200)")
    parser.add_argument("--save_dir",     type=str, default="results/extended")
    parser.add_argument("--prime_powers", action="store_true")
    parser.add_argument("--three_factor", action="store_true")
    parser.add_argument("--corridors",    action="store_true")
    args = parser.parse_args()

    run_all = not (args.prime_powers or args.three_factor or args.corridors)

    save_dir = args.save_dir
    os.makedirs(save_dir, exist_ok=True)

    print(f"Extended Algebra Survey")
    print(f"  b_max={args.b_max}  n_trials={args.n_trials}  n_steps={args.n_steps}")
    print(f"  Dispersion conjecture: C.A. Luther")

    t0 = time.time()

    if run_all or args.prime_powers:
        survey_prime_powers(args.b_max, args.n_trials, args.n_steps, save_dir)

    if run_all or args.three_factor:
        survey_three_factor(args.b_max, args.n_trials, args.n_steps, save_dir)

    if run_all or args.corridors:
        survey_corridors(args.b_max, args.n_trials, args.n_steps, save_dir)

    print(f"\nTotal time: {time.time()-t0:.1f}s")
    print("Done.")


if __name__ == "__main__":
    main()
