# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
jitter_probe.py -- measure the tick the swarm actually delivers.

Runs a bounded-duration probe at the target Hz and records the full
distribution of inter-tick deltas using time.perf_counter_ns().  Reports
mean / p50 / p99 / max and writes a JSON + markdown summary so we can
look at the number before and after each embodiment step and see if
jitter actually fell.

Usage:
    python jitter_probe.py --seconds 30 --hz 50 --rt
    python jitter_probe.py --seconds 10 --hz 200            # no RT elevation
    python jitter_probe.py --seconds 5 --hz 50 --affinity 0 # pin to core 0

The probe also optionally drives the Hebbian field each tick so the numbers
reflect the real workload, not an empty sleep.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import List, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_BRAIN = os.path.normpath(os.path.join(_HERE, "..", "brain"))
if _BRAIN not in sys.path:
    sys.path.insert(0, _BRAIN)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from rt_priority import elevate, restore_normal, RTStatus  # noqa: E402


def _hi_res_sleep_until(target_ns: int) -> None:
    """Sleep until perf_counter_ns() >= target_ns.

    Uses coarse sleep to get close, then busy-spins the final hundred
    microseconds.  This is what turns a multi-millisecond Python sleep()
    into a near-microsecond wake on Windows / Linux without needing a
    real-time kernel.
    """
    # Coarse: leave ~500us for the busy-spin tail.
    while True:
        now = time.perf_counter_ns()
        remaining = target_ns - now
        if remaining <= 500_000:
            break
        # Sleep in chunks so we stay responsive to signals.
        time.sleep(min(remaining - 500_000, 5_000_000) / 1e9)
    # Busy wait the final window.
    while time.perf_counter_ns() < target_ns:
        pass


def _percentiles(values_ns: List[int], qs: List[float]) -> dict:
    if not values_ns:
        return {f"p{int(q*100)}": 0 for q in qs}
    s = sorted(values_ns)
    out = {}
    for q in qs:
        idx = int(q * (len(s) - 1) + 0.5)
        idx = max(0, min(len(s) - 1, idx))
        out[f"p{int(q*100)}"] = s[idx]
    return out


def run_probe(seconds: float, hz: float, rt: bool, affinity: Optional[List[int]],
              with_hebbian: bool) -> dict:
    """Run the probe.  Returns a dict with the full result."""
    period_ns = int(1e9 / hz)

    rt_status: Optional[RTStatus] = None
    if rt:
        rt_status = elevate(affinity=affinity)

    heb = None
    if with_hebbian:
        try:
            from hebbian_gpu import HebbianGPU
            heb = HebbianGPU()
        except Exception as e:
            print(f"[probe] hebbian_gpu unavailable: {e}; skipping load")

    deltas_ns: List[int] = []
    start_ns = time.perf_counter_ns()
    next_ns = start_ns + period_ns
    last_ns = start_ns
    end_ns = start_ns + int(seconds * 1e9)

    n_ticks = 0
    while True:
        _hi_res_sleep_until(next_ns)
        now = time.perf_counter_ns()
        deltas_ns.append(now - last_ns)
        last_ns = now
        n_ticks += 1

        # Touch a real workload so the measurement isn't an empty loop.
        if heb is not None:
            # A small varied pattern so different cells activate.
            a = [(n_ticks + i) % 10 for i in range(5)]
            b = [(n_ticks * 3 + i) % 10 for i in range(5)]
            heb.update(a, b, lens="tsml")

        next_ns += period_ns
        if now >= end_ns:
            break

    if rt:
        restore_normal()

    # Drop the first delta (warmup).
    measured = deltas_ns[1:] if len(deltas_ns) > 1 else deltas_ns
    mean_ns = sum(measured) / max(1, len(measured))
    pct = _percentiles(measured, [0.50, 0.90, 0.99, 1.00])
    max_ns = max(measured) if measured else 0

    jitter_ns = [abs(d - period_ns) for d in measured]
    jitter_mean = sum(jitter_ns) / max(1, len(jitter_ns))
    jitter_p50 = _percentiles(jitter_ns, [0.50])["p50"]
    jitter_p99 = _percentiles(jitter_ns, [0.99])["p99"]
    jitter_max = max(jitter_ns) if jitter_ns else 0

    result = {
        "target_hz": hz,
        "target_period_us": period_ns / 1e3,
        "seconds_requested": seconds,
        "ticks_completed": n_ticks,
        "with_hebbian": with_hebbian,
        "hebbian_backend": (heb.backend if heb is not None else None),
        "rt_status": rt_status.to_dict() if rt_status else None,
        "delta_us": {
            "mean":  mean_ns / 1e3,
            "p50":   pct["p50"] / 1e3,
            "p90":   pct["p90"] / 1e3,
            "p99":   pct["p99"] / 1e3,
            "max":   max_ns / 1e3,
        },
        "jitter_us": {
            "mean": jitter_mean / 1e3,
            "p50":  jitter_p50 / 1e3,
            "p99":  jitter_p99 / 1e3,
            "max":  jitter_max / 1e3,
        },
    }
    return result


def _fmt_md(r: dict) -> str:
    rt = r.get("rt_status") or {}
    rt_line = (f"process={rt.get('process_class', 'NORMAL')} "
               f"thread={rt.get('thread_priority', 'NORMAL')} "
               f"affinity={rt.get('cpu_affinity')} "
               f"admin={rt.get('admin', False)}") if rt else "none"
    return (
        f"# jitter_probe\n\n"
        f"- target: **{r['target_hz']} Hz** ({r['target_period_us']:.1f} µs period)\n"
        f"- ticks: {r['ticks_completed']}\n"
        f"- workload: {'hebbian ' + str(r.get('hebbian_backend')) if r['with_hebbian'] else 'empty'}\n"
        f"- rt: {rt_line}\n\n"
        f"## inter-tick delta (µs)\n"
        f"| mean | p50 | p90 | p99 | max |\n"
        f"|---|---|---|---|---|\n"
        f"| {r['delta_us']['mean']:.1f} | {r['delta_us']['p50']:.1f} | "
        f"{r['delta_us']['p90']:.1f} | {r['delta_us']['p99']:.1f} | "
        f"{r['delta_us']['max']:.1f} |\n\n"
        f"## jitter |delta - period| (µs)\n"
        f"| mean | p50 | p99 | max |\n"
        f"|---|---|---|---|\n"
        f"| {r['jitter_us']['mean']:.1f} | {r['jitter_us']['p50']:.1f} | "
        f"{r['jitter_us']['p99']:.1f} | {r['jitter_us']['max']:.1f} |\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seconds", type=float, default=5.0)
    ap.add_argument("--hz", type=float, default=50.0)
    ap.add_argument("--rt", action="store_true",
                    help="elevate thread priority + pin affinity")
    ap.add_argument("--affinity", type=int, nargs="*",
                    help="list of cpu indices to pin to (requires --rt)")
    ap.add_argument("--no-hebbian", action="store_true",
                    help="don't drive the Hebbian field during probe")
    ap.add_argument("--out", type=str, default=None,
                    help="path prefix for JSON + markdown output")
    args = ap.parse_args()

    print(f"[probe] {args.seconds}s at {args.hz} Hz, "
          f"rt={args.rt}, affinity={args.affinity}, "
          f"hebbian={not args.no_hebbian}")

    r = run_probe(
        seconds=args.seconds,
        hz=args.hz,
        rt=args.rt,
        affinity=args.affinity,
        with_hebbian=not args.no_hebbian,
    )

    print("\n" + _fmt_md(r))

    if args.out:
        with open(args.out + ".json", "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2)
        with open(args.out + ".md", "w", encoding="utf-8") as f:
            f.write(_fmt_md(r))
        print(f"[probe] wrote {args.out}.json + {args.out}.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
