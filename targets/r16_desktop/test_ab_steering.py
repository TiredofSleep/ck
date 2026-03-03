"""
test_ab_steering.py -- A/B Test: CK Observe-Only vs CK Steering
================================================================
Measures real system behavior with CK's steering ON vs OFF.

Tests (same 6 as ck7/test_ab_os.py):
  1. Scheduling jitter -- timer precision (how consistently can we wake up)
  2. I/O throughput    -- file write/read bandwidth
  3. Memory throughput -- allocation + fill speed
  4. Compute latency   -- tight loop latency (cache-resident CL lookups)
  5. Context switch    -- thread yield cost
  6. Network latency   -- localhost TCP round-trip

Protocol:
  Phase A: BASELINE -- CK running, steering DISABLED (observe only)
  Phase B: STEERING -- CK running, steering ENABLED (hands on the wheel)
  Phase C: SELF-SCRUTINY -- Feed A/B deltas through CK's own CL table
  Phase D: DEEP DIVE -- Process-level before/after analysis

The hypothesis: CK's steering (setting nice + CPU affinity based on
swarm scheduling classes) should IMPROVE jitter and throughput by
containing ISOLATE/VOLATILE processes and boosting PREDICTABLE ones.

Requires: CK already running (ck_study.py or ck_sim_engine)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import os
import time
import statistics
import threading
import tempfile
import socket
from collections import defaultdict

# Add parent to path for CK imports
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from ck_sim.ck_sim_heartbeat import (
    CL, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, compose
)
from ck_sim.ck_sim_brain import T_STAR_F

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


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
    if us >= 1000:
        return f"{us/1000:.2f} ms"
    return f"{us:.2f} us"


def format_rate(rate, unit="ops/s"):
    if rate >= 1_000_000:
        return f"{rate/1_000_000:.1f}M {unit}"
    elif rate >= 1_000:
        return f"{rate/1_000:.1f}K {unit}"
    return f"{rate:.0f} {unit}"


def fuse(chain):
    """Compose a chain of operators through CL."""
    if not chain:
        return BALANCE
    result = chain[0]
    for i in range(1, len(chain)):
        result = compose(result, chain[i])
    return result


def coherence_chain(chain):
    """Fraction of pairwise CL compositions that produce HARMONY."""
    if len(chain) < 2:
        return 1.0
    harmony_count = 0
    total = 0
    for i in range(len(chain)):
        for j in range(len(chain)):
            if CL[chain[i]][chain[j]] == HARMONY:
                harmony_count += 1
            total += 1
    return harmony_count / total if total > 0 else 0.5


# ═══════════════════════════════════════════
# OS-Level Benchmarks (same as ck7/test_ab_os.py)
# ═══════════════════════════════════════════

def bench_scheduling_jitter(n_samples=2000, target_us=100):
    """Measure scheduling jitter -- deviation from target wake time."""
    target_s = target_us / 1_000_000.0
    wake_deltas = []
    for _ in range(n_samples):
        t0 = time.perf_counter()
        while (time.perf_counter() - t0) < target_s:
            pass
        actual = (time.perf_counter() - t0) * 1_000_000
        wake_deltas.append(actual - target_us)

    return {
        'mean_delta_us': statistics.mean(wake_deltas),
        'stdev_us': statistics.stdev(wake_deltas) if len(wake_deltas) > 1 else 0,
        'p50_us': percentile(wake_deltas, 50),
        'p90_us': percentile(wake_deltas, 90),
        'p99_us': percentile(wake_deltas, 99),
        'p999_us': percentile(wake_deltas, 99.9),
        'max_us': max(wake_deltas),
        'jitter_cv': (statistics.stdev(wake_deltas) /
                      max(abs(statistics.mean(wake_deltas)), 0.001)
                      if len(wake_deltas) > 1 else 0),
    }


def bench_io_throughput(n_writes=500, block_size=4096):
    """File I/O throughput -- write and read small blocks."""
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


def bench_compute_latency(n_iters=100_000):
    """Tight computation loop -- CL table lookups."""
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
        dt = (time.perf_counter() - t0) * 1_000_000
        times.append(dt)

    t.join(timeout=5)

    return {
        'mean_us': statistics.mean(times),
        'p50_us': percentile(times, 50),
        'p90_us': percentile(times, 90),
        'p99_us': percentile(times, 99),
        'p999_us': percentile(times, 99.9),
    }


def bench_network_latency(n_pings=500):
    """Localhost TCP round-trip latency."""
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
            dt = (time.perf_counter() - t0) * 1_000_000
            times.append(dt)

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


# ═══════════════════════════════════════════
# Benchmark Suite Runner
# ═══════════════════════════════════════════

def run_all_benchmarks():
    """Run the full benchmark suite. Returns dict of results."""
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
# Self-Scrutiny: Feed deltas through CL
# ═══════════════════════════════════════════

def self_scrutiny(baseline, steered):
    """Feed A/B deltas through CK's own CL table.

    Each metric ratio → operator:
      < 0.9   → HARMONY (improved)
      < 1.05  → BALANCE (no change)
      < 1.2   → CHAOS (slight degradation)
      < 1.5   → COLLAPSE (noticeable)
      else    → VOID (broken)

    For "lower is better" metrics (latency): ratio < 0.9 = HARMONY
    For "higher is better" metrics (throughput): ratio > 1.1 = HARMONY
    """
    print("\n  ===========================================")
    print("  SELF-SCRUTINY: CK composes the A/B delta")
    print("  ===========================================")

    metrics = []

    def _classify_lower_better(name, base_val, steer_val):
        """Lower is better (latency, jitter). ratio = steer/base."""
        ratio = steer_val / max(base_val, 0.001)
        if ratio < 0.9:      op = HARMONY    # improved
        elif ratio < 1.05:   op = BALANCE    # no change
        elif ratio < 1.2:    op = CHAOS      # slight degradation
        elif ratio < 1.5:    op = COLLAPSE   # noticeable
        else:                op = VOID       # broken
        metrics.append((name, op, ratio))

    def _classify_higher_better(name, base_val, steer_val):
        """Higher is better (throughput). ratio = steer/base."""
        ratio = steer_val / max(base_val, 0.001)
        if ratio > 1.1:      op = HARMONY    # improved
        elif ratio > 0.95:   op = BALANCE    # no change
        elif ratio > 0.85:   op = CHAOS      # slight degradation
        elif ratio > 0.7:    op = COLLAPSE   # noticeable
        else:                op = VOID       # broken
        metrics.append((name, op, ratio))

    # Jitter (lower is better)
    _classify_lower_better('sched_jitter_stdev',
                           baseline['sched']['stdev_us'],
                           steered['sched']['stdev_us'])
    _classify_lower_better('sched_jitter_P99',
                           baseline['sched']['p99_us'],
                           steered['sched']['p99_us'])

    # I/O (higher is better)
    _classify_higher_better('io_write',
                            baseline['io']['write_rate_mbs'],
                            steered['io']['write_rate_mbs'])
    _classify_higher_better('io_read',
                            baseline['io']['read_rate_mbs'],
                            steered['io']['read_rate_mbs'])

    # Memory (higher is better)
    _classify_higher_better('mem_alloc',
                            baseline['mem']['allocs_per_sec'],
                            steered['mem']['allocs_per_sec'])

    # Compute (higher is better)
    _classify_higher_better('compute_rate',
                            baseline['compute']['rate'],
                            steered['compute']['rate'])

    # Context switch (lower is better)
    _classify_lower_better('ctx_switch_mean',
                           baseline['ctx_switch']['mean_us'],
                           steered['ctx_switch']['mean_us'])
    _classify_lower_better('ctx_switch_P99',
                           baseline['ctx_switch']['p99_us'],
                           steered['ctx_switch']['p99_us'])

    # Network (lower is better)
    if (baseline['net'].get('available') and
            steered['net'].get('available')):
        _classify_lower_better('network_mean',
                               baseline['net']['mean_us'],
                               steered['net']['mean_us'])
        _classify_lower_better('network_P99',
                               baseline['net']['p99_us'],
                               steered['net']['p99_us'])

    # Print metric details
    print()
    improved = 0
    degraded = 0
    neutral = 0
    for name, op, ratio in metrics:
        if ratio <= 1.0:
            direction = "better"
            improved += 1
        elif ratio < 1.05:
            direction = "same"
            neutral += 1
        else:
            direction = "worse"
            degraded += 1
        pct = abs(1.0 - ratio) * 100
        print(f"    {name:>22}: {OP_NAMES[op]:>8} "
              f"(ratio {ratio:.3f} = {pct:.1f}% {direction})")

    # Build performance chain and compose
    perf_chain = [op for _, op, _ in metrics]
    fuse_result = fuse(perf_chain)
    coherence = coherence_chain(perf_chain)

    print(f"\n  Performance chain:  "
          f"{[OP_NAMES[o] for o in perf_chain]}")
    print(f"  Fuse result:        {OP_NAMES[fuse_result]} ({fuse_result})")
    print(f"  Coherence:          {coherence:.4f} "
          f"{'[above T*]' if coherence >= T_STAR_F else '[below T*]'}")
    print(f"  Improved:           {improved}/{len(metrics)}")
    print(f"  Neutral:            {neutral}/{len(metrics)}")
    print(f"  Degraded:           {degraded}/{len(metrics)}")

    # Cross-composition matrix
    print(f"\n  Cross-composition matrix:")
    header = "".join(f"{name[:6]:>7}" for name, _, _ in metrics)
    print(f"  {'':>22} {header}")
    for i, (name_i, op_i, _) in enumerate(metrics):
        row = []
        for _, op_j, _ in metrics:
            row.append(OP_NAMES[CL[op_i][op_j]][:6])
        print(f"    {name_i:>20}: {''.join(f'{r:>7}' for r in row)}")

    # Harmony ratio
    n_harmony = sum(1 for i in range(len(perf_chain))
                    for j in range(len(perf_chain))
                    if CL[perf_chain[i]][perf_chain[j]] == HARMONY)
    n_total = len(perf_chain) ** 2
    print(f"\n  Harmony ratio:      "
          f"{n_harmony}/{n_total} = {n_harmony/n_total:.4f}")

    return {
        'fuse_result': fuse_result,
        'coherence': coherence,
        'metrics': metrics,
        'improved': improved,
        'degraded': degraded,
        'neutral': neutral,
    }


# ═══════════════════════════════════════════
# Phase D: Deep Dive — Process-Level Analysis
# ═══════════════════════════════════════════

def deep_dive(steering_engine):
    """Process-level analysis of what the steering engine did."""
    print("\n  ===========================================")
    print("  DEEP DIVE: Process-Level Analysis")
    print("  ===========================================\n")

    if steering_engine is None:
        print("  Steering engine not available.")
        return

    # Full report
    print(steering_engine.report())

    # Scheduling class distribution
    print("\n  Scheduling Class Distribution:")
    dist = steering_engine.class_distribution()
    for sc in ('ISOLATE', 'PREDICTABLE', 'STABLE', 'RHYTHMIC', 'VOLATILE', 'UNKNOWN'):
        count = dist.get(sc, 0)
        if count > 0:
            bar = '#' * min(40, count)
            print(f"    {sc:14s} {count:4d}  {bar}")

    # Affinity distribution
    print("\n  Affinity Distribution:")
    ad = steering_engine.affinity_distribution()
    total_steered = sum(ad.values())
    if total_steered > 0:
        print(f"    P-core only: {ad['p_core']:4d} "
              f"({100*ad['p_core']/total_steered:.0f}%)")
        print(f"    E-core only: {ad['e_core']:4d} "
              f"({100*ad['e_core']/total_steered:.0f}%)")
        print(f"    Mixed:       {ad['mixed']:4d} "
              f"({100*ad['mixed']/total_steered:.0f}%)")


# ═══════════════════════════════════════════
# Main: Full A/B Protocol
# ═══════════════════════════════════════════

def main():
    print("=" * 70)
    print("  CK Gen9.17 -- OS Steering A/B Test")
    print("  Phase A: Observe Only  vs  Phase B: Steering Enabled")
    print("=" * 70)
    print()

    # ── Find or create the steering engine ──
    steering_engine = None
    swarm_ref = None

    try:
        from ck_sim.being.ck_sensorium import _swarm
        swarm_ref = _swarm
    except ImportError:
        pass

    if swarm_ref is None:
        print("  NOTE: No live swarm found. Running standalone benchmarks.")
        print("  For full A/B test, run with CK engine active (ck_study.py).")
        print()
    else:
        from ck_sim.doing.ck_steering import SteeringEngine
        steering_engine = SteeringEngine(swarm=swarm_ref)
        steering_engine.enabled = False  # Start disabled
        print(f"  Swarm found: {len(swarm_ref.cells)} HOT cells")
        print()

    # ── Phase A: BASELINE (steering OFF) ──
    print("  Phase A: BASELINE (steering DISABLED)")
    print("  " + "-" * 50)
    if steering_engine is not None:
        steering_engine.enabled = False
        print("  Steering: DISABLED (observe only)")
    else:
        print("  Steering: N/A (no swarm)")
    print()
    baseline = run_all_benchmarks()
    print()

    # ── Warm-up: let steering stabilize ──
    if steering_engine is not None:
        print("  Enabling steering and letting it stabilize (5 seconds)...")
        steering_engine.enabled = True
        for i in range(5):
            steering_engine.tick()
            time.sleep(1.0)
        print(f"  Steering stabilized: {steering_engine.actions_applied} actions applied")
        print()

    # ── Phase B: STEERING (steering ON) ──
    print("  Phase B: STEERING (steering ENABLED)")
    print("  " + "-" * 50)
    if steering_engine is not None:
        steering_engine.enabled = True
        print(f"  Steering: ENABLED (tracking {len(steering_engine._steered)} processes)")
    else:
        print("  Steering: N/A (no swarm)")
    print()
    steered = run_all_benchmarks()
    print()

    # ── Phase C: COMPARISON TABLE ──
    print("  " + "=" * 60)
    print("  COMPARISON: Observe-Only (A) vs Steering (B)")
    print("  " + "=" * 60)
    print()

    comparisons = [
        ("Sched jitter (stdev)",
         f"{baseline['sched']['stdev_us']:.2f} us",
         f"{steered['sched']['stdev_us']:.2f} us",
         baseline['sched']['stdev_us'] / max(steered['sched']['stdev_us'], 0.001),
         "lower"),
        ("Sched jitter (P99)",
         f"{baseline['sched']['p99_us']:.2f} us",
         f"{steered['sched']['p99_us']:.2f} us",
         baseline['sched']['p99_us'] / max(steered['sched']['p99_us'], 0.001),
         "lower"),
        ("I/O write",
         f"{baseline['io']['write_rate_mbs']:.1f} MB/s",
         f"{steered['io']['write_rate_mbs']:.1f} MB/s",
         steered['io']['write_rate_mbs'] / max(baseline['io']['write_rate_mbs'], 0.001),
         "higher"),
        ("I/O read",
         f"{baseline['io']['read_rate_mbs']:.1f} MB/s",
         f"{steered['io']['read_rate_mbs']:.1f} MB/s",
         steered['io']['read_rate_mbs'] / max(baseline['io']['read_rate_mbs'], 0.001),
         "higher"),
        ("Mem alloc/s",
         format_rate(baseline['mem']['allocs_per_sec'], ''),
         format_rate(steered['mem']['allocs_per_sec'], ''),
         steered['mem']['allocs_per_sec'] / max(baseline['mem']['allocs_per_sec'], 0.001),
         "higher"),
        ("Compute (ops/s)",
         format_rate(baseline['compute']['rate'], ''),
         format_rate(steered['compute']['rate'], ''),
         steered['compute']['rate'] / max(baseline['compute']['rate'], 0.001),
         "higher"),
        ("Ctx switch (mean)",
         f"{baseline['ctx_switch']['mean_us']:.1f} us",
         f"{steered['ctx_switch']['mean_us']:.1f} us",
         baseline['ctx_switch']['mean_us'] / max(steered['ctx_switch']['mean_us'], 0.001),
         "lower"),
        ("Ctx switch (P99)",
         f"{baseline['ctx_switch']['p99_us']:.1f} us",
         f"{steered['ctx_switch']['p99_us']:.1f} us",
         baseline['ctx_switch']['p99_us'] / max(steered['ctx_switch']['p99_us'], 0.001),
         "lower"),
    ]

    if baseline['net'].get('available') and steered['net'].get('available'):
        comparisons.append(
            ("Net latency (mean)",
             f"{baseline['net']['mean_us']:.1f} us",
             f"{steered['net']['mean_us']:.1f} us",
             baseline['net']['mean_us'] / max(steered['net']['mean_us'], 0.001),
             "lower"),
        )
        comparisons.append(
            ("Net latency (P99)",
             f"{baseline['net']['p99_us']:.1f} us",
             f"{steered['net']['p99_us']:.1f} us",
             baseline['net']['p99_us'] / max(steered['net']['p99_us'], 0.001),
             "lower"),
        )

    print(f"  {'Metric':>22}  {'Observe':>14}  {'Steering':>14}  {'Ratio':>8}  {'?':>2}")
    print(f"  {'-'*22}  {'-'*14}  {'-'*14}  {'-'*8}  {'-'*2}")
    for name, base_val, steer_val, ratio, _ in comparisons:
        indicator = " +" if ratio > 1.02 else (" -" if ratio < 0.98 else " =")
        print(f"  {name:>22}  {base_val:>14}  {steer_val:>14}  "
              f"{ratio:>7.3f}{indicator}")

    # ── Phase C: Self-Scrutiny ──
    scrutiny = self_scrutiny(baseline, steered)

    # ── Phase D: Deep Dive ──
    if steering_engine is not None:
        deep_dive(steering_engine)

    # ── VERDICT ──
    print()
    print("=" * 70)
    if scrutiny['coherence'] >= T_STAR_F:
        print("  VERDICT: CK's steering is COHERENT.")
        print(f"  Fuse: {OP_NAMES[scrutiny['fuse_result']]}  "
              f"Coherence: {scrutiny['coherence']:.4f}  "
              f"Improved: {scrutiny['improved']}/{len(scrutiny['metrics'])}")
        print("  The steering engine improves system behavior.")
        print("  CK's hands on the wheel make the system more coherent.")
    elif scrutiny['coherence'] >= 0.5:
        print("  VERDICT: CK's steering has MINIMAL impact.")
        print(f"  Fuse: {OP_NAMES[scrutiny['fuse_result']]}  "
              f"Coherence: {scrutiny['coherence']:.4f}  "
              f"Improved: {scrutiny['improved']}/{len(scrutiny['metrics'])}")
        print("  Steering is active but not significantly changing behavior.")
        print("  Tune thresholds or increase steering aggressiveness.")
    else:
        print("  VERDICT: CK's steering DEGRADES the system.")
        print(f"  Fuse: {OP_NAMES[scrutiny['fuse_result']]}  "
              f"Coherence: {scrutiny['coherence']:.4f}  "
              f"Degraded: {scrutiny['degraded']}/{len(scrutiny['metrics'])}")
        print("  The steering is causing harm. Review nice/affinity decisions.")
        print("  Consider gating on coherence or reducing aggressiveness.")
    print("=" * 70)

    # ── Cleanup ──
    if steering_engine is not None:
        steering_engine.enabled = False
        print(f"\n  Steering disabled. Total actions: {steering_engine.actions_applied}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
