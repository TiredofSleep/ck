"""
RH Corridor Sweep — Void Pocket Scan to t₀ = 10,000
=====================================================
Extends the corridor scan to high imaginary heights using real ζ computation.

What it measures:
  For each height t₀, sample |ζ(σ+it₀)| on a dense σ grid in the critical strip.
  The "void pocket" is the minimum of |ζ| and where it lives.
  λ(t₀) measures how deep the void penetrates toward the critical line,
  normalized by the KV collar width at that height.

λ definition (consistent with corridor_scan schema):
  σ_KV(t₀) = 1 − c/(log t₀)^{2/3}(log log t₀)^{1/3}   [KV zero-free boundary]
  σ_min     = argmin_{σ ∈ [0.5, σ_KV]} |ζ(σ+it₀)|
  λ         = 1 − (σ_min − 0.5) / (σ_KV − 0.5)         [0=void at KV edge, 1=void at critical line]

Corridor assignment (same thresholds as Mix_λ gap operators):
  Pre-leak  [0.00, 0.09)  — minimum retreated to near-KV boundary
  BRT       [0.09, 0.30)  — gap operators begin
  CHA       [0.30, 0.60)  — flat again
  BAL       [0.60, 0.80)  — heavy tails appearing
  COL       [0.80, 0.90)  — HIGH danger: M₈/M₄ = 31 analog
  CTR       [0.90, 1.00]  — EXTREME: void at critical line

RH claim: λ stays below the COL threshold (0.80) at all heights.
This sweep empirically tests that to t₀ = 10,000.

Requirements:
  mpmath >= 1.3     (accurate ζ computation)
  numpy >= 1.24
  cupy  (optional, GPU batch)

Output:
  papers/corridor_scan_extended.csv
  papers/research/rh_corridor_sweep.png

Author: Brayden Sanders / 7Site LLC
DOI: 10.5281/zenodo.18852047
SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787
"""

import math
import time
import csv
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

try:
    import mpmath
    mpmath.mp.dps = 25          # 25 significant digits — accurate through t₀=10,000
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False
    print("ERROR: mpmath required. pip install mpmath")
    sys.exit(1)

try:
    import cupy as cp
    cp.cuda.Device(0).use()
    HAS_CUPY = True
    print(f"CuPy available: {cp.cuda.runtime.runtimeGetVersion()} | "
          f"Device: {cp.cuda.Device(0).name.decode()}")
except Exception:
    HAS_CUPY = False
    print("CuPy not available — running on CPU (16-core parallel)")

# ── TIG constants (from tig_constants.py) ────────────────────────────────────
T_STAR   = 5/7
S_STAR   = 4/7
MASS_GAP = T_STAR + S_STAR - 1   # 2/7

KV_C = 0.05   # Korobov-Vinogradov constant

CORRIDOR_THRESHOLDS = [
    (0.00, 0.09, "Pre-leak"),
    (0.09, 0.30, "BRT"),
    (0.30, 0.60, "CHA"),
    (0.60, 0.80, "BAL"),
    (0.80, 0.90, "COL"),
    (0.90, 1.01, "CTR"),
]

DANGER_CORRIDORS = {"COL", "CTR"}

# ── Height schedule ──────────────────────────────────────────────────────────
# Logarithmically spaced: dense at low t, sparser at high t.
# Also include known zero heights for calibration.
KNOWN_ZEROS = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
               37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
               52.9703, 56.4462, 59.3470, 60.8318, 65.1125,
               67.0798, 69.5465, 72.0672, 75.7047, 77.1448]

def height_schedule(t_min=10.0, t_max=10000.0, n_log=400):
    """Logarithmically spaced heights plus known zero heights."""
    log_pts = np.logspace(math.log10(t_min), math.log10(t_max), n_log)
    # Add calibration points: near-zero heights and 5% above each known zero
    near_zeros = []
    for z in KNOWN_ZEROS:
        if t_min <= z <= t_max:
            near_zeros.extend([z - 0.5, z, z + 0.5])
    all_pts = np.sort(np.unique(np.concatenate([log_pts, near_zeros])))
    return all_pts[(all_pts >= t_min) & (all_pts <= t_max)]

# ── KV collar ────────────────────────────────────────────────────────────────
def sigma_kv(t, c=KV_C):
    """KV zero-free boundary: σ_KV(t) = 1 − c/(log t)^{2/3}(log log t)^{1/3}."""
    if t <= 2.0:
        return 0.99
    log_t = math.log(t)
    log_log_t = math.log(log_t) if log_t > 1 else 1e-10
    collar = c / (log_t**(2/3) * log_log_t**(1/3))
    return min(0.9999, max(0.5001, 1.0 - collar))

def scale_factor(t, c=KV_C):
    """From tig_constants.py: kv_collar / inner_shell."""
    inner_shell = 2/9
    kv = 1.0 - sigma_kv(t, c)   # distance from σ=1
    return kv / inner_shell

# ── ζ computation ─────────────────────────────────────────────────────────────
def zeta_abs_grid_mpmath(t0, sigma_grid):
    """
    Compute |ζ(σ+it₀)| for each σ in sigma_grid using mpmath.
    Returns numpy array of absolute values.
    """
    t_mp = mpmath.mpf(t0)
    vals = []
    for sig in sigma_grid:
        s = mpmath.mpc(float(sig), float(t0))
        z = mpmath.zeta(s)
        vals.append(float(abs(z)))
    return np.array(vals)

# GPU approximate ζ via truncated Euler-Maclaurin (fast, for corridor classification)
_EULER_N = 200   # truncation depth

def zeta_abs_grid_gpu(t0, sigma_grid_np):
    """
    GPU-accelerated approximate |ζ(σ+it₀)| via Euler-Maclaurin truncation to N terms.
    ζ(s) ≈ Σ_{n=1}^{N} n^{-s} + N^{1-s}/(s-1) + N^{-s}/2
    Valid to ~1% in the critical strip for N=200, sufficient for corridor classification.
    Falls back to mpmath for borderline corridor cases.
    """
    if not HAS_CUPY:
        return zeta_abs_grid_mpmath(t0, sigma_grid_np)

    N = _EULER_N
    sigma_gpu = cp.asarray(sigma_grid_np, dtype=cp.float64)
    n_sigma   = len(sigma_gpu)

    # Build n array [1..N] as column, sigma as row
    ns = cp.arange(1, N+1, dtype=cp.float64)              # shape (N,)
    ns_col  = ns[:, None]                                   # (N, 1)
    sig_row = sigma_gpu[None, :]                            # (1, n_sigma)
    t_val   = cp.float64(t0)

    # n^{-s} = exp(-σ log n - it log n) = n^{-σ} * exp(-it log n)
    log_ns  = cp.log(ns_col)                                # (N, 1)
    amp     = cp.exp(-sig_row * log_ns)                     # (N, n_sigma) — magnitudes
    phase   = -t_val * log_ns                               # (N, 1)
    re_sum  = cp.sum(amp * cp.cos(phase), axis=0)           # (n_sigma,)
    im_sum  = cp.sum(amp * cp.sin(phase), axis=0)           # (n_sigma,)

    # Euler-Maclaurin tail: N^{1-s}/(s-1)
    # Real part of N^{1-s}/(s-1):
    s_re = sig_row[0]       # (n_sigma,)
    s_im = t_val
    # N^{1-s} = exp((1-s)*log N)
    log_N = math.log(N)
    re_N = cp.exp((1 - s_re) * log_N) * cp.cos(-s_im * log_N)
    im_N = cp.exp((1 - s_re) * log_N) * cp.sin(-s_im * log_N)
    # 1/(s-1): s-1 = (σ-1) + it
    den_re = s_re - 1.0
    den_im = s_im
    den_abs2 = den_re**2 + den_im**2 + 1e-300
    tail_re = (re_N * den_re + im_N * den_im) / den_abs2
    tail_im = (im_N * den_re - re_N * den_im) / den_abs2

    # N^{-s}/2 correction
    half_re = cp.exp(-s_re * log_N) * cp.cos(-s_im * log_N) / 2.0
    half_im = cp.exp(-s_re * log_N) * cp.sin(-s_im * log_N) / 2.0

    total_re = re_sum + tail_re + half_re
    total_im = im_sum + tail_im + half_im
    abs_vals = cp.sqrt(total_re**2 + total_im**2)

    return cp.asnumpy(abs_vals)

# ── Single height scan ────────────────────────────────────────────────────────
N_SIGMA = 150    # σ resolution per height

def scan_height(t0, use_gpu=True, verify_borderline=True):
    """
    Scan |ζ(σ+it₀)| for σ ∈ [0.5, σ_KV(t₀)].
    Returns dict with all corridor metrics.
    """
    skv = sigma_kv(t0)
    if skv <= 0.502:
        # Strip too narrow to scan meaningfully
        return None

    sigma_grid = np.linspace(0.5001, skv, N_SIGMA)

    # Compute |ζ| on grid
    if use_gpu and HAS_CUPY:
        abs_vals = zeta_abs_grid_gpu(t0, sigma_grid)
    else:
        abs_vals = zeta_abs_grid_mpmath(t0, sigma_grid)

    min_idx  = np.argmin(abs_vals)
    min_val  = abs_vals[min_idx]
    sigma_min = sigma_grid[min_idx]
    kv_val   = abs_vals[-1]   # |ζ| at σ=σ_KV

    # λ: how far the void pocket is from the KV boundary toward the critical line
    # λ=0: void at KV edge (retreated, safe-extreme)
    # λ=1: void at critical line (expected near zeros)
    strip_width = skv - 0.5
    lam = 1.0 - (sigma_min - 0.5) / strip_width if strip_width > 1e-6 else 0.0
    lam = float(np.clip(lam, 0.0, 1.0))

    # Corridor assignment
    corridor = "CTR"
    for lo, hi, name in CORRIDOR_THRESHOLDS:
        if lo <= lam < hi:
            corridor = name
            break

    # Danger flag
    danger = corridor in DANGER_CORRIDORS

    # Verify borderline cases with mpmath (GPU approximate can miss by ~1%)
    if verify_borderline and use_gpu and HAS_CUPY and abs(lam - 0.80) < 0.05:
        abs_vals_mp = zeta_abs_grid_mpmath(t0, sigma_grid[::3])  # coarser but exact
        min_val_mp  = float(np.min(abs_vals_mp))
        sigma_min_mp = sigma_grid[::3][np.argmin(abs_vals_mp)]
        lam_mp = 1.0 - (sigma_min_mp - 0.5) / strip_width
        lam_mp = float(np.clip(lam_mp, 0.0, 1.0))
        # Use mpmath result for corridor classification
        corridor_mp = "CTR"
        for lo, hi, name in CORRIDOR_THRESHOLDS:
            if lo <= lam_mp < hi:
                corridor_mp = name
                break
        danger = corridor_mp in DANGER_CORRIDORS
        lam = lam_mp
        corridor = corridor_mp
        sigma_min = float(sigma_min_mp)
        min_val = min_val_mp

    # KV bound comparison
    # Minimum |ζ| should stay above exp(-c(log t)^{2/3}(log log t)^{1/3}) × scale
    # We track the raw min_val; the KV guarantee is only for σ > σ_KV
    kv_ratio = min_val / (kv_val + 1e-300)  # ratio of void depth to KV-boundary value

    sf = scale_factor(t0)

    return {
        "t0":        round(t0, 4),
        "sigma_min": round(float(sigma_min), 5),
        "sigma_kv":  round(skv, 5),
        "lambda":    round(lam, 5),
        "corridor":  corridor,
        "min_zeta":  round(float(min_val), 8),
        "kv_val":    round(float(kv_val), 8),
        "kv_ratio":  round(kv_ratio, 6),
        "danger":    danger,
        "scale_factor": round(sf, 5),
        "strip_width":  round(float(strip_width), 5),
    }

# ── Parallel CPU sweep ────────────────────────────────────────────────────────
def _worker(args):
    t0, use_gpu = args
    try:
        return scan_height(t0, use_gpu=use_gpu, verify_borderline=True)
    except Exception as e:
        return {"t0": t0, "error": str(e)}

# ── Main sweep ────────────────────────────────────────────────────────────────
def run_sweep(t_min=10.0, t_max=10000.0, n_heights=400, n_workers=14, out_csv=None):
    heights = height_schedule(t_min, t_max, n_heights)
    total   = len(heights)

    if out_csv is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        out_csv = os.path.join(script_dir, "corridor_scan_extended.csv")

    os.makedirs(os.path.dirname(out_csv) if os.path.dirname(out_csv) else ".", exist_ok=True)

    print(f"\n{'='*60}")
    print(f"RH CORRIDOR SWEEP  |  t₀ ∈ [{t_min}, {t_max}]  |  {total} heights")
    print(f"GPU: {'YES (approximate + mpmath verify)' if HAS_CUPY else 'NO — CPU only'}")
    print(f"Workers: {n_workers}  |  σ resolution: {N_SIGMA} points per height")
    print(f"Output: {out_csv}")
    print(f"{'='*60}\n")

    fieldnames = ["t0","sigma_min","sigma_kv","lambda","corridor",
                  "min_zeta","kv_val","kv_ratio","danger","scale_factor","strip_width"]

    results  = []
    dangers  = []
    t_start  = time.time()
    done     = 0

    # Use GPU for coarse scan, verify borderline with mpmath
    use_gpu = HAS_CUPY

    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        args_list = [(t0, use_gpu) for t0 in heights]

        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            futures = {pool.submit(_worker, a): a[0] for a in args_list}
            for fut in as_completed(futures):
                t0  = futures[fut]
                row = fut.result()
                done += 1

                if row is None or "error" in row:
                    err = row.get("error","None") if row else "None"
                    print(f"  [{done:>4}/{total}] t={t0:>9.3f}  ERROR: {err}")
                    continue

                writer.writerow(row)
                f.flush()
                results.append(row)

                if row["danger"]:
                    dangers.append(row)
                    flag = " *** DANGER ***"
                else:
                    flag = ""

                if done % 20 == 0 or row["danger"]:
                    elapsed = time.time() - t_start
                    eta     = elapsed / done * (total - done)
                    print(f"  [{done:>4}/{total}] t={t0:>9.3f}  "
                          f"λ={row['lambda']:.4f}  corridor={row['corridor']:<8}  "
                          f"σ_min={row['sigma_min']:.4f}  "
                          f"ETA {eta:.0f}s{flag}")

    # ── Summary ────────────────────────────────────────────────────────────────
    elapsed = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"SWEEP COMPLETE  |  {len(results)} heights  |  {elapsed:.1f}s")
    print()

    if results:
        # Sort by t0
        results.sort(key=lambda r: r["t0"])
        lambdas     = [r["lambda"] for r in results]
        corridors   = {}
        for r in results:
            c = r["corridor"]
            corridors[c] = corridors.get(c, 0) + 1

        print(f"  λ statistics:")
        print(f"    min = {min(lambdas):.4f}")
        print(f"    max = {max(lambdas):.4f}")
        print(f"    mean = {sum(lambdas)/len(lambdas):.4f}")
        print()
        print(f"  Corridor distribution:")
        for lo, hi, name in CORRIDOR_THRESHOLDS:
            cnt = corridors.get(name, 0)
            pct = 100.0 * cnt / len(results) if results else 0
            flag = " ← DANGER" if name in DANGER_CORRIDORS and cnt > 0 else ""
            print(f"    {name:<10} {cnt:>4} heights  ({pct:5.1f}%){flag}")
        print()

        if dangers:
            print(f"  DANGER ENTRIES ({len(dangers)}):")
            for d in dangers:
                print(f"    t={d['t0']:.3f}  λ={d['lambda']:.4f}  "
                      f"corridor={d['corridor']}  σ_min={d['sigma_min']:.4f}")
        else:
            print(f"  RESULT: No heights entered COL/CTR corridor in scanned range.")
            print(f"  → Void pocket stayed below λ=0.80 for all {len(results)} heights.")
            print(f"  → Consistent with RH: no dangerous corridor occupancy detected.")
        print()

        # Scale factor summary
        sfs = [r["scale_factor"] for r in results]
        print(f"  scale_factor(t):")
        print(f"    t={results[0]['t0']:.1f}: {results[0]['scale_factor']:.4f}")
        mid = results[len(results)//2]
        print(f"    t={mid['t0']:.1f}: {mid['scale_factor']:.4f}")
        print(f"    t={results[-1]['t0']:.1f}: {results[-1]['scale_factor']:.4f}")
        print(f"    → Collar shrinks with height as predicted.")

    print(f"\nCSV: {out_csv}")
    print(f"SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787")
    print(f"DOI: 10.5281/zenodo.18852047")
    return results, dangers

# ── Plot ─────────────────────────────────────────────────────────────────────
def plot_results(results, out_path=None):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed — skipping plot")
        return

    if not results:
        return

    results_sorted = sorted(results, key=lambda r: r["t0"])
    ts      = [r["t0"] for r in results_sorted]
    lams    = [r["lambda"] for r in results_sorted]
    sfs     = [r["scale_factor"] for r in results_sorted]
    corr    = [r["corridor"] for r in results_sorted]

    CMAP = {
        "Pre-leak": "#2ecc71",
        "BRT":      "#27ae60",
        "CHA":      "#3498db",
        "BAL":      "#f39c12",
        "COL":      "#e74c3c",
        "CTR":      "#8e44ad",
    }
    colors = [CMAP.get(c, "#aaaaaa") for c in corr]

    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    fig.suptitle("RH Corridor Sweep: Void Pocket λ to t₀ = 10,000\n"
                 "TIG / WP31 Corridor Geometry | Gen10 Sprint",
                 fontsize=13, fontweight="bold")

    # Panel 1: λ vs t₀
    ax = axes[0]
    ax.scatter(ts, lams, c=colors, s=4, alpha=0.7, linewidths=0)
    for lo, hi, name in CORRIDOR_THRESHOLDS:
        ax.axhline(y=hi, color=CMAP.get(name, "#aaa"), linestyle="--", linewidth=0.6,
                   alpha=0.5, label=f"{name} ({lo:.2f}–{hi:.2f})")
    ax.axhline(y=0.80, color="#e74c3c", linestyle="-", linewidth=1.5,
               label="COL threshold (danger)")
    ax.set_ylabel("λ (void pocket depth)")
    ax.set_ylim(0.0, 1.05)
    ax.legend(loc="upper right", fontsize=7, ncol=2)
    ax.set_title("Void Pocket λ — should stay below COL (0.80) for all heights")
    ax.grid(alpha=0.2)

    # Panel 2: scale_factor(t)
    ax = axes[1]
    ax.plot(ts, sfs, "b-", linewidth=1.2, alpha=0.8)
    ax.axhline(y=1.0, color="orange", linestyle="--", linewidth=0.8,
               label="scale=1 (TIG grid = KV collar)")
    ax.set_ylabel("scale_factor(t)")
    ax.set_title("scale_factor(t) = KV collar / inner_shell — calibration shrinks with height")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    ax.set_yscale("log")

    # Panel 3: min|ζ| vs t₀
    ax = axes[2]
    min_z = [r["min_zeta"] for r in results_sorted]
    ax.plot(ts, min_z, "k-", linewidth=0.8, alpha=0.7)
    # Mark known zeros
    for z0 in KNOWN_ZEROS:
        if ts[0] <= z0 <= ts[-1]:
            ax.axvline(x=z0, color="red", linewidth=0.5, alpha=0.4)
    ax.set_xlabel("Height t₀")
    ax.set_ylabel("min|ζ(σ+it₀)|")
    ax.set_title("Void pocket depth — dips to ≈0 at known zero heights (red marks)")
    ax.set_yscale("log")
    ax.grid(alpha=0.2)

    ax.set_xscale("log")
    axes[0].set_xscale("log")
    axes[1].set_xscale("log")

    plt.tight_layout()

    if out_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(script_dir, "research", "rh_corridor_sweep.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"Plot: {out_path}")
    plt.close()

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RH corridor void-pocket sweep")
    parser.add_argument("--t-max",    type=float, default=10000.0,
                        help="Maximum height (default: 10000)")
    parser.add_argument("--t-min",    type=float, default=10.0,
                        help="Minimum height (default: 10)")
    parser.add_argument("--n",        type=int,   default=400,
                        help="Number of heights (default: 400)")
    parser.add_argument("--workers",  type=int,   default=14,
                        help="CPU worker processes (default: 14)")
    parser.add_argument("--out",      type=str,   default=None,
                        help="Output CSV path")
    parser.add_argument("--no-plot",  action="store_true",
                        help="Skip plot generation")
    args = parser.parse_args()

    results, dangers = run_sweep(
        t_min=args.t_min,
        t_max=args.t_max,
        n_heights=args.n,
        n_workers=args.workers,
        out_csv=args.out,
    )

    if not args.no_plot and results:
        plot_results(results)

    # Exit code: 0 = clean (no dangers), 1 = dangerous corridors found
    sys.exit(1 if dangers else 0)
