"""
r16_sweep_all.py
=================
Full semiprime atlas sweep — all semiprimes b=6..100.

Runs r16_job1_reduction for every semiprime base, both random and seeded.
33 worlds × 2 runs × ~3.5s = ~4 minutes total on R16.

Usage:
    python r16_sweep_all.py
    python r16_sweep_all.py --n_start 5000 --n_steps 100
    python r16_sweep_all.py --bases 15 22 35 55      (specific subset)
    python r16_sweep_all.py --skip 6 9               (skip degenerate)

Author: Brayden Sanders / 7Site LLC | Sprint 4 (March 2026)
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
import time
from math import gcd

# Import the job module
from r16_job1_reduction import run_atlas_job, compute_world


def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True


def get_all_semiprimes(max_b=100):
    """Return all semiprimes b=6..max_b (p×q, p and q prime, p≤q)."""
    result = []
    for b in range(6, max_b + 1):
        for p in range(2, int(b**0.5) + 1):
            if b % p == 0 and is_prime(p) and is_prime(b // p):
                result.append(b)
                break
    return result


def run_sweep(bases, n_start, n_steps, workers, skip_seeded=False):
    """Run random + seeded jobs for all bases. Return summary table."""
    summary = []

    for b in bases:
        print(f"\n{'█'*65}")
        print(f"  BASE b={b}  ({n_start} trials × {n_steps} steps)")
        print(f"{'█'*65}")

        # Check if world is viable
        try:
            world = compute_world(b)
        except ValueError as e:
            print(f"  SKIP: {e}")
            summary.append({'b': b, 'status': 'degenerate', 'error': str(e)})
            continue

        row = {
            'b': b,
            'p': world['p'], 'q': world['q'],
            'phi': world['phi'],
            'G_size': len(world['G']),
            'HAR': world['HAR'],
            'score': world['score'],
            'grad_score': world['grad_score'],
            'status': 'ok',
        }

        # ── Random run ────────────────────────────────────────────────────
        out_random = f'results/reduction_b{b}_N{n_start}.json'
        if os.path.exists(out_random):
            print(f"  [random] cached → {out_random}")
            with open(out_random) as f:
                rdata = json.load(f)
            row['random_gate_pct']   = rdata['gate_strong_rate'] * 100
            row['random_tsml_pct']   = rdata['tsml_like_rate'] * 100
            row['random_oracle_pct'] = rdata['oracle_rate'] * 100
            row['random_har_max']    = rdata['stats']['HAR_mass']['max']
            row['random_gap_max']    = rdata['stats']['gap']['max']
        else:
            t0 = time.time()
            result = run_atlas_job(b=b, n_trials=n_start, n_steps=n_steps,
                                   seeded=False, n_workers=workers)
            with open(out_random, 'w') as f:
                json.dump(result, f, indent=2)
            row['random_gate_pct']   = result['gate_strong_rate'] * 100
            row['random_tsml_pct']   = result['tsml_like_rate'] * 100
            row['random_oracle_pct'] = result['oracle_rate'] * 100
            row['random_har_max']    = result['stats']['HAR_mass']['max']
            row['random_gap_max']    = result['stats']['gap']['max']

        # ── Seeded run ────────────────────────────────────────────────────
        if not skip_seeded:
            out_seeded = f'results/reduction_b{b}_N{n_start}_seeded.json'
            if os.path.exists(out_seeded):
                print(f"  [seeded] cached → {out_seeded}")
                with open(out_seeded) as f:
                    sdata = json.load(f)
                row['seeded_gate_pct']   = sdata['gate_strong_rate'] * 100
                row['seeded_tsml_pct']   = sdata['tsml_like_rate'] * 100
                row['seeded_har_max']    = sdata['stats']['HAR_mass']['max']
                row['seeded_gstay_mean'] = sdata['stats'].get('G_stay', {}).get('mean', None)
            else:
                result_s = run_atlas_job(b=b, n_trials=n_start, n_steps=n_steps,
                                         seeded=True, n_workers=workers)
                with open(out_seeded, 'w') as f:
                    json.dump(result_s, f, indent=2)
                row['seeded_gate_pct']   = result_s['gate_strong_rate'] * 100
                row['seeded_tsml_pct']   = result_s['tsml_like_rate'] * 100
                row['seeded_har_max']    = result_s['stats']['HAR_mass']['max']
                row['seeded_gstay_mean'] = result_s['stats'].get('G_stay', {}).get('mean', None)

        summary.append(row)

    return summary


def print_summary_table(summary):
    """Print the complete atlas summary table."""
    print(f"\n\n{'='*90}")
    print(f"FULL SEMIPRIME ATLAS — R16 Sweep Results")
    print(f"{'='*90}")
    print(f"{'b':>4} {'p×q':>7} {'φ':>3} {'|G|':>4} {'HAR':>4} "
          f"{'score':>7} {'rnd%gate':>9} {'seed%gate':>10} "
          f"{'HAR_m_best':>11} {'gap_best':>9} {'G_stay_s':>9}")
    print(f"  {'-'*85}")

    for row in sorted(summary, key=lambda r: -r.get('score', 0)):
        if row.get('status') == 'degenerate':
            print(f"  {row['b']:3d}  DEGENERATE — {row.get('error','')}")
            continue
        b = row['b']
        pq = f"{row['p']}×{row['q']}"
        phi = row['phi']
        gs  = row['G_size']
        har = row['HAR']
        sc  = row.get('score', 0)
        rg  = row.get('random_gate_pct', 0)
        sg  = row.get('seeded_gate_pct', 0)
        hm  = row.get('random_har_max', 0)
        gp  = row.get('random_gap_max', 0)
        gst = row.get('seeded_gstay_mean')
        gst_s = f"{gst:.4f}" if gst is not None else "  —  "

        star = ' ★' if b == 15 else ''
        print(f"  {b:3d}  {pq:>7}  {phi:2d}  {gs:3d}  {har:3d}  "
              f"{sc:7.3f}  {rg:7.1f}%   {sg:7.1f}%   {hm:9.4f}  {gp:7.4f}  {gst_s}{star}")

    print(f"{'='*90}")


def save_atlas_json(summary, path='results/atlas_sweep_all.json'):
    """Save full atlas to JSON."""
    with open(path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\n✓ Full atlas saved → {path}")


def main():
    parser = argparse.ArgumentParser(
        description='Full semiprime atlas sweep: all b=6..100')
    parser.add_argument('--n_start', type=int, default=10000)
    parser.add_argument('--n_steps', type=int, default=100)
    parser.add_argument('--workers', type=int, default=None)
    parser.add_argument('--max_b', type=int, default=100)
    parser.add_argument('--bases', type=int, nargs='+', default=None,
                        help='Specific bases to run (default: all semiprimes)')
    parser.add_argument('--skip', type=int, nargs='+', default=[6],
                        help='Bases to skip (default: [6] degenerate)')
    parser.add_argument('--no_seeded', action='store_true',
                        help='Skip seeded runs')
    args = parser.parse_args()

    os.makedirs('results', exist_ok=True)

    if args.bases:
        bases = args.bases
    else:
        bases = [b for b in get_all_semiprimes(args.max_b)
                 if b not in (args.skip or [])]

    print(f"Sweeping {len(bases)} bases: {bases}")
    print(f"N={args.n_start} steps={args.n_steps} seeded={'no' if args.no_seeded else 'yes'}")

    t_total = time.time()
    summary = run_sweep(bases, args.n_start, args.n_steps,
                        args.workers, skip_seeded=args.no_seeded)
    elapsed = time.time() - t_total

    print_summary_table(summary)
    save_atlas_json(summary)
    print(f"\nTotal time: {elapsed:.1f}s for {len(bases)} bases "
          f"({'×2 seeded' if not args.no_seeded else 'random only'})")


if __name__ == '__main__':
    import multiprocessing as mp
    mp.freeze_support()
    main()
