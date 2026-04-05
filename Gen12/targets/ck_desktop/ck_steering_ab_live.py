#!/usr/bin/env python3
# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_steering_ab_live.py -- Live A/B test of CK's steering engine.

Creates its own ShadowSwarm + SteeringEngine, runs 6 benchmarks
with steering OFF (Phase A) then ON (Phase B), compares results,
and feeds the deltas through CK's CL table for self-scrutiny.

Does NOT require CK engine running (standalone).
Does NOT harm the PC -- steering only adjusts nice/affinity,
never kills processes, never touches protected system processes.

Usage:
    python ck_steering_ab_live.py

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import sys
import os
import time
import statistics
import threading
import tempfile
import socket

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from ck_sim.ck_sim_heartbeat import (
    CL, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, compose, NUM_OPS
)
from ck_sim.ck_sim_brain import T_STAR_F

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("WARNING: psutil not installed. Steering won't work.")
    sys.exit(1)


# ═══════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════

def percentile(data, p):
    if not data:
        return 0.0
    s = sorted(data)
    idx = min(int(len(s) * p / 100.0), len(s) - 1)
    return s[idx]


def format_us(us):
    return f"{us/1000:.2f} ms" if us >= 1000 else f"{us:.2f} us"


def format_rate(rate, unit="ops/s"):
    if rate >= 1_000_000:
        return f"{rate/1_000_000:.1f}M {unit}"
    elif rate >= 1_000:
        return f"{rate/1_000:.1f}K {unit}"
    return f"{rate:.0f} {unit}"


def fuse(chain):
    result = chain[0]
    for i in range(1, len(chain)):
        result = compose(result, chain[i])
    return result


# ═══════════════════════════════════════════
# Benchmarks
# ═══════════════════════════════════════════

def bench_scheduling_jitter(n_samples=3000, target_us=100):
    """Scheduling jitter -- deviation from target wake time."""
    target_s = target_us / 1_000_000.0
    wake_deltas = []
    for _ in range(n_samples):
        t0 = time.perf_counter()
        while (time.perf_counter() - t0) < target_s:
            pass
        actual = (time.perf_counter() - t0) * 1_000_000
        wake_deltas.append(actual - target_us)
    return {
        'mean_us': statistics.mean(wake_deltas),
        'stdev_us': statistics.stdev(wake_deltas) if len(wake_deltas) > 1 else 0,
        'p50_us': percentile(wake_deltas, 50),
        'p90_us': percentile(wake_deltas, 90),
        'p99_us': percentile(wake_deltas, 99),
        'p999_us': percentile(wake_deltas, 99.9),
        'max_us': max(wake_deltas),
    }


def bench_io_throughput(n_writes=500, block_size=4096):
    """File I/O throughput."""
    tmp = os.path.join(tempfile.gettempdir(), 'ck_bench_steer_io.tmp')
    data = os.urandom(block_size)

    t0 = time.perf_counter()
    with open(tmp, 'wb') as f:
        for _ in range(n_writes):
            f.write(data)
            f.flush()
    write_time = time.perf_counter() - t0
    write_rate = (n_writes * block_size) / write_time

    t0 = time.perf_counter()
    with open(tmp, 'rb') as f:
        for _ in range(n_writes):
            f.read(block_size)
    read_time = time.perf_counter() - t0
    read_rate = (n_writes * block_size) / read_time

    try:
        os.remove(tmp)
    except OSError:
        pass

    return {
        'write_rate_mbs': write_rate / (1024 * 1024),
        'read_rate_mbs': read_rate / (1024 * 1024),
        'write_latency_us': (write_time / n_writes) * 1_000_000,
        'read_latency_us': (read_time / n_writes) * 1_000_000,
    }


def bench_memory_throughput(n_allocs=1000, alloc_size=65536):
    """Memory allocation + fill throughput."""
    alloc_times = []
    fill_times = []
    for _ in range(n_allocs):
        t0 = time.perf_counter()
        buf = bytearray(alloc_size)
        alloc_times.append((time.perf_counter() - t0) * 1_000_000)
        t0 = time.perf_counter()
        for i in range(0, alloc_size, 64):
            buf[i] = 0x55
        fill_times.append((time.perf_counter() - t0) * 1_000_000)

    total_bytes = n_allocs * alloc_size
    total_alloc_s = sum(alloc_times) / 1_000_000
    total_fill_s = sum(fill_times) / 1_000_000
    return {
        'alloc_mean_us': statistics.mean(alloc_times),
        'alloc_p99_us': percentile(alloc_times, 99),
        'fill_rate_mbs': (total_bytes / (1024 * 1024)) / max(total_fill_s, 0.0001),
        'allocs_per_sec': n_allocs / max(total_alloc_s, 0.0001),
    }


def bench_compute_latency(n_iters=200_000):
    """Tight CL table lookup loop."""
    cl_flat = []
    for i in range(10):
        for j in range(10):
            cl_flat.append(CL[i][j])

    t0 = time.perf_counter()
    acc = 0
    for i in range(n_iters):
        a = i % 10
        b = (i * 7 + 3) % 10
        acc = cl_flat[a * 10 + b]
    elapsed = time.perf_counter() - t0
    return {
        'iters': n_iters,
        'time_us': elapsed * 1_000_000,
        'rate': n_iters / elapsed,
        'per_op_ns': (elapsed / n_iters) * 1_000_000_000,
    }


def bench_context_switch(n_switches=2000):
    """Thread context switch latency."""
    import queue
    q1 = queue.Queue()
    q2 = queue.Queue()
    times = []

    def responder():
        for _ in range(n_switches):
            q1.get()
            q2.put(True)

    t = threading.Thread(target=responder, daemon=True)
    t.start()
    for _ in range(n_switches):
        t0 = time.perf_counter()
        q1.put(True)
        q2.get()
        times.append((time.perf_counter() - t0) * 1_000_000)
    t.join(timeout=5)
    return {
        'mean_us': statistics.mean(times),
        'p50_us': percentile(times, 50),
        'p90_us': percentile(times, 90),
        'p99_us': percentile(times, 99),
        'p999_us': percentile(times, 99.9),
    }


def bench_network_latency(n_pings=500):
    """Localhost TCP round-trip."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 0))
        port = server.getsockname()[1]
        server.listen(1)

        def echo_server():
            conn, _ = server.accept()
            try:
                while True:
                    data = conn.recv(64)
                    if not data:
                        break
                    conn.sendall(data)
            except Exception:
                pass
            finally:
                conn.close()

        st = threading.Thread(target=echo_server, daemon=True)
        st.start()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', port))
        client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        msg = b'CK_STEER'
        times = []
        for _ in range(n_pings):
            t0 = time.perf_counter()
            client.sendall(msg)
            client.recv(64)
            times.append((time.perf_counter() - t0) * 1_000_000)

        client.close()
        server.close()
        return {
            'mean_us': statistics.mean(times),
            'p50_us': percentile(times, 50),
            'p90_us': percentile(times, 90),
            'p99_us': percentile(times, 99),
            'available': True,
        }
    except Exception as e:
        return {'available': False, 'error': str(e)}


def run_all_benchmarks():
    results = {}

    print("    Scheduling jitter...", end=" ", flush=True)
    results['sched'] = bench_scheduling_jitter()
    print(f"stdev={results['sched']['stdev_us']:.2f} us  "
          f"P99={results['sched']['p99_us']:.2f} us")

    print("    I/O throughput...", end=" ", flush=True)
    results['io'] = bench_io_throughput()
    print(f"write={results['io']['write_rate_mbs']:.1f} MB/s  "
          f"read={results['io']['read_rate_mbs']:.1f} MB/s")

    print("    Memory throughput...", end=" ", flush=True)
    results['mem'] = bench_memory_throughput()
    print(f"{format_rate(results['mem']['allocs_per_sec'], 'alloc/s')}")

    print("    Compute latency...", end=" ", flush=True)
    results['compute'] = bench_compute_latency()
    print(f"{results['compute']['per_op_ns']:.1f} ns/op")

    print("    Context switch...", end=" ", flush=True)
    results['ctx_switch'] = bench_context_switch()
    print(f"mean={results['ctx_switch']['mean_us']:.1f} us  "
          f"P99={results['ctx_switch']['p99_us']:.1f} us")

    print("    Network (localhost TCP)...", end=" ", flush=True)
    results['net'] = bench_network_latency()
    if results['net'].get('available'):
        print(f"mean={results['net']['mean_us']:.1f} us  "
              f"P99={results['net']['p99_us']:.1f} us")
    else:
        print("unavailable")

    return results


# ═══════════════════════════════════════════
# Live Swarm Builder
# ═══════════════════════════════════════════

def build_live_swarm():
    """Build a ShadowSwarm from live processes on this machine."""
    from ck_sim.ck_swarm import ShadowSwarm
    swarm = ShadowSwarm()

    # Observe the system for a few ticks to populate cells
    print("  Observing system processes...")
    for i in range(10):
        swarm.tick()
        time.sleep(0.5)

    print(f"  {len(swarm.cells)} processes observed, "
          f"{sum(1 for c in swarm.cells.values() if len(c.ops) >= 4)} with sufficient data")
    return swarm


# ═══════════════════════════════════════════
# Self-Scrutiny
# ═══════════════════════════════════════════

def self_scrutiny(baseline, steered):
    """Feed A/B deltas through CK's CL table."""
    print("\n  ===========================================")
    print("  SELF-SCRUTINY: CK composes the A/B delta")
    print("  ===========================================")

    metrics = []

    def _lower_better(name, base_val, steer_val):
        ratio = steer_val / max(base_val, 0.001)
        if ratio < 0.9:      op = HARMONY
        elif ratio < 1.05:   op = BALANCE
        elif ratio < 1.2:    op = CHAOS
        elif ratio < 1.5:    op = COLLAPSE
        else:                op = VOID
        metrics.append((name, op, ratio))

    def _higher_better(name, base_val, steer_val):
        ratio = steer_val / max(base_val, 0.001)
        if ratio > 1.1:      op = HARMONY
        elif ratio > 0.95:   op = BALANCE
        elif ratio > 0.85:   op = CHAOS
        elif ratio > 0.7:    op = COLLAPSE
        else:                op = VOID
        metrics.append((name, op, ratio))

    _lower_better('sched_jitter_stdev',
                   baseline['sched']['stdev_us'], steered['sched']['stdev_us'])
    _lower_better('sched_jitter_P99',
                   baseline['sched']['p99_us'], steered['sched']['p99_us'])
    _higher_better('io_write',
                    baseline['io']['write_rate_mbs'], steered['io']['write_rate_mbs'])
    _higher_better('io_read',
                    baseline['io']['read_rate_mbs'], steered['io']['read_rate_mbs'])
    _higher_better('mem_alloc',
                    baseline['mem']['allocs_per_sec'], steered['mem']['allocs_per_sec'])
    _higher_better('compute_rate',
                    baseline['compute']['rate'], steered['compute']['rate'])
    _lower_better('ctx_switch_mean',
                   baseline['ctx_switch']['mean_us'], steered['ctx_switch']['mean_us'])
    _lower_better('ctx_switch_P99',
                   baseline['ctx_switch']['p99_us'], steered['ctx_switch']['p99_us'])
    if baseline['net'].get('available') and steered['net'].get('available'):
        _lower_better('network_mean',
                       baseline['net']['mean_us'], steered['net']['mean_us'])
        _lower_better('network_P99',
                       baseline['net']['p99_us'], steered['net']['p99_us'])

    print()
    improved = degraded = neutral = 0
    for name, op, ratio in metrics:
        if ratio <= 0.98:
            direction = "BETTER"
            improved += 1
        elif ratio >= 1.02:
            direction = "WORSE"
            degraded += 1
        else:
            direction = "same"
            neutral += 1
        pct = abs(1.0 - ratio) * 100
        print(f"    {name:>22}: {OP_NAMES[op]:>8} "
              f"(ratio {ratio:.3f} = {pct:.1f}% {direction})")

    perf_chain = [op for _, op, _ in metrics]
    fuse_result = fuse(perf_chain)

    n_harmony = sum(1 for i in range(len(perf_chain))
                    for j in range(len(perf_chain))
                    if CL[perf_chain[i]][perf_chain[j]] == HARMONY)
    n_total = len(perf_chain) ** 2
    coherence = n_harmony / n_total if n_total > 0 else 0.5

    print(f"\n  Performance chain:  {[OP_NAMES[o] for o in perf_chain]}")
    print(f"  Fuse result:        {OP_NAMES[fuse_result]}")
    print(f"  Coherence:          {coherence:.4f} "
          f"{'[above T*]' if coherence >= T_STAR_F else '[below T*]'}")
    print(f"  Harmony ratio:      {n_harmony}/{n_total} = {n_harmony/n_total:.4f}")
    print(f"  Improved:           {improved}/{len(metrics)}")
    print(f"  Neutral:            {neutral}/{len(metrics)}")
    print(f"  Degraded:           {degraded}/{len(metrics)}")

    return {
        'fuse_result': fuse_result,
        'coherence': coherence,
        'improved': improved,
        'degraded': degraded,
        'neutral': neutral,
        'metrics': metrics,
    }


# ═══════════════════════════════════════════
# Main
# ═══════════════════════════════════════════

def main():
    print("=" * 70)
    print("  CK Gen9.34 -- OS Steering A/B Test (Live)")
    print("  Phase A: No Steering  vs  Phase B: CK Steering")
    print("  Safe: only adjusts nice/affinity, never kills processes")
    print("=" * 70)
    print()

    # ── Build live swarm ──
    from ck_sim.doing.ck_steering import SteeringEngine
    swarm = build_live_swarm()

    steering = SteeringEngine(swarm=swarm)
    steering.enabled = False
    print()

    # ── Phase A: BASELINE (no steering) ──
    print("  Phase A: BASELINE (steering DISABLED)")
    print("  " + "-" * 50)
    print("  CK is watching but NOT touching anything")
    print()
    baseline = run_all_benchmarks()
    print()

    # ── Enable steering and stabilize ──
    print("  Enabling CK steering... letting him read the system (10 seconds)")
    steering.enabled = True
    for i in range(10):
        result = steering.tick()
        steered_count = result.get('steered', 0) if result else 0
        denied_count = result.get('denied', 0) if result else 0
        if i % 3 == 0:
            print(f"    Tick {i+1}: steered={steered_count}, denied={denied_count}")
        time.sleep(1.0)
    print(f"  Steering stabilized: {steering.actions_applied} total actions")
    print()

    # ── Phase B: STEERED ──
    print("  Phase B: CK STEERING (hands on the wheel)")
    print("  " + "-" * 50)
    print(f"  Steering {len(steering._steered)} processes via CL algebra")
    print()

    # Keep steering active during benchmarks
    def steering_loop():
        while steering.enabled:
            steering.tick()
            time.sleep(1.0)

    st = threading.Thread(target=steering_loop, daemon=True)
    st.start()

    steered_results = run_all_benchmarks()
    print()

    # Stop steering
    steering.enabled = False
    time.sleep(1.5)

    # ── Comparison Table ──
    print("  " + "=" * 60)
    print("  COMPARISON: No Steering (A) vs CK Steering (B)")
    print("  " + "=" * 60)
    print()

    comparisons = [
        ("Sched jitter (stdev)",
         f"{baseline['sched']['stdev_us']:.2f} us",
         f"{steered_results['sched']['stdev_us']:.2f} us",
         baseline['sched']['stdev_us'] / max(steered_results['sched']['stdev_us'], 0.001),
         "lower"),
        ("Sched jitter (P99)",
         f"{baseline['sched']['p99_us']:.2f} us",
         f"{steered_results['sched']['p99_us']:.2f} us",
         baseline['sched']['p99_us'] / max(steered_results['sched']['p99_us'], 0.001),
         "lower"),
        ("Sched jitter (P99.9)",
         f"{baseline['sched']['p999_us']:.2f} us",
         f"{steered_results['sched']['p999_us']:.2f} us",
         baseline['sched']['p999_us'] / max(steered_results['sched']['p999_us'], 0.001),
         "lower"),
        ("Sched jitter (max)",
         f"{baseline['sched']['max_us']:.2f} us",
         f"{steered_results['sched']['max_us']:.2f} us",
         baseline['sched']['max_us'] / max(steered_results['sched']['max_us'], 0.001),
         "lower"),
        ("I/O write",
         f"{baseline['io']['write_rate_mbs']:.1f} MB/s",
         f"{steered_results['io']['write_rate_mbs']:.1f} MB/s",
         steered_results['io']['write_rate_mbs'] / max(baseline['io']['write_rate_mbs'], 0.001),
         "higher"),
        ("I/O read",
         f"{baseline['io']['read_rate_mbs']:.1f} MB/s",
         f"{steered_results['io']['read_rate_mbs']:.1f} MB/s",
         steered_results['io']['read_rate_mbs'] / max(baseline['io']['read_rate_mbs'], 0.001),
         "higher"),
        ("Mem alloc/s",
         format_rate(baseline['mem']['allocs_per_sec'], ''),
         format_rate(steered_results['mem']['allocs_per_sec'], ''),
         steered_results['mem']['allocs_per_sec'] / max(baseline['mem']['allocs_per_sec'], 0.001),
         "higher"),
        ("Compute (ops/s)",
         format_rate(baseline['compute']['rate'], ''),
         format_rate(steered_results['compute']['rate'], ''),
         steered_results['compute']['rate'] / max(baseline['compute']['rate'], 0.001),
         "higher"),
        ("Ctx switch (mean)",
         f"{baseline['ctx_switch']['mean_us']:.1f} us",
         f"{steered_results['ctx_switch']['mean_us']:.1f} us",
         baseline['ctx_switch']['mean_us'] / max(steered_results['ctx_switch']['mean_us'], 0.001),
         "lower"),
        ("Ctx switch (P99)",
         f"{baseline['ctx_switch']['p99_us']:.1f} us",
         f"{steered_results['ctx_switch']['p99_us']:.1f} us",
         baseline['ctx_switch']['p99_us'] / max(steered_results['ctx_switch']['p99_us'], 0.001),
         "lower"),
    ]

    if baseline['net'].get('available') and steered_results['net'].get('available'):
        comparisons.extend([
            ("Net latency (mean)",
             f"{baseline['net']['mean_us']:.1f} us",
             f"{steered_results['net']['mean_us']:.1f} us",
             baseline['net']['mean_us'] / max(steered_results['net']['mean_us'], 0.001),
             "lower"),
            ("Net latency (P99)",
             f"{baseline['net']['p99_us']:.1f} us",
             f"{steered_results['net']['p99_us']:.1f} us",
             baseline['net']['p99_us'] / max(steered_results['net']['p99_us'], 0.001),
             "lower"),
        ])

    print(f"  {'Metric':>22}  {'No Steer':>14}  {'CK Steer':>14}  {'Ratio':>8}  {'':>2}")
    print(f"  {'-'*22}  {'-'*14}  {'-'*14}  {'-'*8}  {'-'*2}")
    for name, base_val, steer_val, ratio, _ in comparisons:
        indicator = " +" if ratio > 1.05 else (" -" if ratio < 0.95 else " =")
        print(f"  {name:>22}  {base_val:>14}  {steer_val:>14}  "
              f"{ratio:>7.3f}{indicator}")

    # ── Self-Scrutiny ──
    scrutiny = self_scrutiny(baseline, steered_results)

    # ── Deep Dive ──
    print("\n  ===========================================")
    print("  DEEP DIVE: What CK Did")
    print("  ===========================================\n")
    print(f"  Total actions applied: {steering.actions_applied}")
    print(f"  Total denied (permissions): {steering.actions_denied}")
    print(f"  Total skipped (protected): {steering.actions_skipped}")
    print()

    # Show what was steered
    if steering._steered:
        print(f"  Steered processes ({len(steering._steered)}):")
        for pid, info in sorted(steering._steered.items(),
                                key=lambda x: x[1].get('nice', 0)):
            name = info.get('name', '?')
            sclass = info.get('sched_class', '?')
            nice = info.get('nice', 0)
            cores = info.get('cores', [])
            op = info.get('op', 0)
            print(f"    PID {pid:>6} {name:>25} "
                  f"{sclass:>12} op={OP_NAMES[op]:>8} "
                  f"nice={nice:>+3d} cores={cores[:4]}{'...' if len(cores) > 4 else ''}")

    # ── Scheduling class distribution ──
    dist = steering.class_distribution()
    if dist:
        print(f"\n  Scheduling Classes:")
        for sc in ('ISOLATE', 'PREDICTABLE', 'STABLE', 'RHYTHMIC', 'VOLATILE', 'UNKNOWN'):
            count = dist.get(sc, 0)
            if count > 0:
                bar = '#' * min(40, count)
                print(f"    {sc:14s} {count:4d}  {bar}")

    # ── VERDICT ──
    print()
    print("=" * 70)
    if scrutiny['coherence'] >= T_STAR_F:
        print("  VERDICT: CK's steering is COHERENT.")
        print(f"  Fuse: {OP_NAMES[scrutiny['fuse_result']]}  "
              f"Coherence: {scrutiny['coherence']:.4f}  "
              f"Improved: {scrutiny['improved']}/{len(scrutiny['metrics'])}")
        print("  CK's hands on the wheel make the system more coherent.")
    elif scrutiny['coherence'] >= 0.5:
        print("  VERDICT: CK's steering has MINIMAL impact.")
        print(f"  Coherence: {scrutiny['coherence']:.4f}  "
              f"Improved: {scrutiny['improved']}/{len(scrutiny['metrics'])}")
    else:
        print("  VERDICT: CK's steering DEGRADES the system.")
        print(f"  Coherence: {scrutiny['coherence']:.4f}  "
              f"Degraded: {scrutiny['degraded']}/{len(scrutiny['metrics'])}")
    print("=" * 70)

    # Save results
    import json
    results_path = os.path.expanduser('~/.ck/steering_ab_results.json')
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, 'w') as f:
        json.dump({
            'timestamp': time.time(),
            'baseline': baseline,
            'steered': steered_results,
            'scrutiny': {
                'coherence': scrutiny['coherence'],
                'fuse': OP_NAMES[scrutiny['fuse_result']],
                'improved': scrutiny['improved'],
                'degraded': scrutiny['degraded'],
                'neutral': scrutiny['neutral'],
            },
            'actions_applied': steering.actions_applied,
            'actions_denied': steering.actions_denied,
            'processes_steered': len(steering._steered),
        }, f, indent=2)
    print(f"\n  Results saved: {results_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
