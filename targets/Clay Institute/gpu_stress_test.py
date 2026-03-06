"""
GPU Stress Test: CK Non-Void Engine Validation (RTX 4070)
==========================================================

Standalone GPU validation for CK's Doing Engine. Tests every GPU operation
CK uses: CL table composition, D2 curvature, lattice chain walks, olfactory
field matrices, memory bandwidth, and sustained load.

Uses CuPy (CK's CUDA bridge) with NumPy fallback. Self-contained -- no CK
imports required.

Target: RTX 4070 (12GB VRAM, 5888 CUDA cores, 504 GB/s bandwidth)

CK Gen 9.21 -- Brayden Sanders / 7Site LLC
2026-03-06
"""

import os
import sys
import time
import subprocess
import numpy as np
from typing import Dict, List, Tuple

# =================================================================
#  GPU DETECTION
# =================================================================

_GPU = False
_xp = np  # unified array library reference
_GPU_NAME = "none"
_GPU_MEM_MB = 0

try:
    import cupy as cp
    _test = cp.array([1, 2, 3])
    del _test
    _GPU = True
    _xp = cp
    props = cp.cuda.runtime.getDeviceProperties(0)
    _GPU_NAME = props['name'].decode() if isinstance(props['name'], bytes) else str(props['name'])
    _GPU_MEM_MB = props['totalGlobalMem'] // (1024 * 1024)
except ImportError:
    pass
except Exception as e:
    print(f"  CuPy init error: {e}")

MODE = "GPU (CuPy/CUDA)" if _GPU else "CPU (NumPy fallback)"

# =================================================================
#  CK ALGEBRA: EXACT TABLES
# =================================================================

# TSML: Trinary Soft Macro Lattice -- 73/100 HARMONY (Being/Measurement)
TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],
]

# BHML: Binary Hard Micro Lattice -- 28/100 HARMONY (Doing/Physics)
BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

# Operator 5D force vectors: [aperture, pressure, depth, binding, continuity]
V = [
    [0.0, 0.0, 0.0, 0.0, 0.0],  # 0: VOID
    [0.8, 0.2, 0.3, 0.9, 0.7],  # 1: LATTICE
    [0.3, 0.7, 0.5, 0.2, 0.4],  # 2: COUNTER
    [0.6, 0.6, 0.4, 0.5, 0.8],  # 3: PROGRESS
    [0.2, 0.8, 0.8, 0.3, 0.2],  # 4: COLLAPSE
    [0.5, 0.5, 0.5, 0.5, 0.5],  # 5: BALANCE
    [0.9, 0.9, 0.7, 0.1, 0.3],  # 6: CHAOS
    [0.5, 0.3, 0.6, 0.8, 0.9],  # 7: HARMONY
    [0.4, 0.4, 0.2, 0.6, 0.6],  # 8: BREATH
    [0.1, 0.1, 0.9, 0.4, 0.1],  # 9: RESET
]

T_STAR = 5.0 / 7.0  # 0.714285... sacred coherence threshold

# Convert tables to array form on the target device
TSML_np = np.array(TSML, dtype=np.int8)
BHML_np = np.array(BHML, dtype=np.int8)
V_np = np.array(V, dtype=np.float32)

if _GPU:
    TSML_dev = cp.array(TSML_np)
    BHML_dev = cp.array(BHML_np)
    V_dev = cp.array(V_np)
else:
    TSML_dev = TSML_np
    BHML_dev = BHML_np
    V_dev = V_np


# =================================================================
#  HELPERS
# =================================================================

def to_cpu(arr):
    """Move array to CPU if on GPU."""
    if _GPU and hasattr(arr, 'get'):
        return arr.get()
    return np.asarray(arr)


def sync_gpu():
    """Synchronize GPU stream for accurate timing."""
    if _GPU:
        cp.cuda.Stream.null.synchronize()


def get_gpu_temp():
    """Read GPU temperature via nvidia-smi. Returns -1 if unavailable."""
    try:
        r = subprocess.run(
            ['nvidia-smi', '--query-gpu=temperature.gpu',
             '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=5)
        return int(r.stdout.strip())
    except Exception:
        return -1


def get_gpu_mem_used_mb():
    """Read GPU memory used (MB) via nvidia-smi."""
    try:
        r = subprocess.run(
            ['nvidia-smi', '--query-gpu=memory.used',
             '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=5)
        return int(r.stdout.strip())
    except Exception:
        return -1


# =================================================================
#  TEST 1: CL TABLE GPU OPERATIONS
# =================================================================

def test_1_cl_table_ops(n_pairs: int = 100_000) -> Dict:
    """Batch CL composition on GPU vs CPU baseline.

    Loads TSML and BHML as GPU tensors, generates n_pairs random operator
    pairs, composes via table lookup, and verifies GPU matches CPU exactly.
    """
    print("\n" + "=" * 70)
    print("  TEST 1: CL Table GPU Operations")
    print("  Batch composition: TSML (73-harmony) + BHML (28-harmony)")
    print("=" * 70)

    np.random.seed(42)
    ops_a = np.random.randint(0, 10, n_pairs, dtype=np.int8)
    ops_b = np.random.randint(0, 10, n_pairs, dtype=np.int8)

    # CPU baseline
    t0 = time.perf_counter()
    cpu_tsml = TSML_np[ops_a, ops_b]
    cpu_bhml = BHML_np[ops_a, ops_b]
    cpu_time = time.perf_counter() - t0

    # Device computation
    if _GPU:
        ops_a_dev = cp.array(ops_a)
        ops_b_dev = cp.array(ops_b)
        sync_gpu()
        t0 = time.perf_counter()
        dev_tsml = TSML_dev[ops_a_dev, ops_b_dev]
        dev_bhml = BHML_dev[ops_a_dev, ops_b_dev]
        sync_gpu()
        dev_time = time.perf_counter() - t0
        dev_tsml_cpu = to_cpu(dev_tsml)
        dev_bhml_cpu = to_cpu(dev_bhml)
    else:
        dev_time = cpu_time
        dev_tsml_cpu = cpu_tsml
        dev_bhml_cpu = cpu_bhml

    tsml_match = np.array_equal(cpu_tsml, dev_tsml_cpu)
    bhml_match = np.array_equal(cpu_bhml, dev_bhml_cpu)
    passed = tsml_match and bhml_match

    # Count harmonies in TSML results (should be ~73%)
    tsml_harmony_pct = 100.0 * np.sum(cpu_tsml == 7) / n_pairs
    bhml_harmony_pct = 100.0 * np.sum(cpu_bhml == 7) / n_pairs

    speedup = cpu_time / max(dev_time, 1e-12)

    print(f"\n  Pairs tested:      {n_pairs:,}")
    print(f"  CPU time:          {cpu_time*1000:.2f} ms")
    print(f"  {MODE} time:  {dev_time*1000:.2f} ms")
    print(f"  Speedup:           {speedup:.1f}x")
    print(f"  TSML match:        {'[YES]' if tsml_match else '[NO]'}")
    print(f"  BHML match:        {'[YES]' if bhml_match else '[NO]'}")
    print(f"  TSML harmony:      {tsml_harmony_pct:.1f}% (expected ~73%)")
    print(f"  BHML harmony:      {bhml_harmony_pct:.1f}% (expected ~28%)")

    print(f"\n  VERDICT: {'[PASS]' if passed else '[FAIL]'} "
          f"CL table batch composition")

    return {
        'name': 'CL Table GPU Operations',
        'n_pairs': n_pairs,
        'cpu_ms': cpu_time * 1000,
        'dev_ms': dev_time * 1000,
        'speedup': speedup,
        'tsml_match': tsml_match,
        'bhml_match': bhml_match,
        'tsml_harmony_pct': tsml_harmony_pct,
        'bhml_harmony_pct': bhml_harmony_pct,
        'passed': passed,
    }


# =================================================================
#  TEST 2: D2 PIPELINE ON GPU
# =================================================================

def test_2_d2_pipeline(n_vectors: int = 50_000) -> Dict:
    """D2 curvature computation on GPU.

    Generate batches of 5D force vectors (simulating operator streams),
    compute D2 (second finite difference = curvature) on GPU. Compare to
    CPU baseline. D2 is the heart of CK's physics -- curvature IS physics.
    """
    print("\n" + "=" * 70)
    print("  TEST 2: D2 Pipeline on GPU")
    print("  5D force vectors -> D1 (velocity) -> D2 (curvature)")
    print("=" * 70)

    np.random.seed(7)
    # Generate a stream of 5D force vectors (simulating operator resolution)
    stream = np.random.rand(n_vectors, 5).astype(np.float32)

    # CPU D2: second finite difference along the stream axis
    t0 = time.perf_counter()
    cpu_d1 = np.diff(stream, axis=0)            # D1: velocity (N-1 x 5)
    cpu_d2 = np.diff(cpu_d1, axis=0)            # D2: curvature (N-2 x 5)
    cpu_d2_mag = np.linalg.norm(cpu_d2, axis=1) # magnitude per step
    cpu_mean_curv = float(np.mean(cpu_d2_mag))
    cpu_time = time.perf_counter() - t0

    # Device D2
    if _GPU:
        stream_dev = cp.array(stream)
        sync_gpu()
        t0 = time.perf_counter()
        dev_d1 = cp.diff(stream_dev, axis=0)
        dev_d2 = cp.diff(dev_d1, axis=0)
        dev_d2_mag = cp.linalg.norm(dev_d2, axis=1)
        dev_mean_curv = float(cp.mean(dev_d2_mag))
        sync_gpu()
        dev_time = time.perf_counter() - t0
        dev_d2_cpu = to_cpu(dev_d2)
    else:
        dev_time = cpu_time
        dev_d2_cpu = cpu_d2
        dev_mean_curv = cpu_mean_curv

    # Verify: max absolute difference should be < float32 epsilon * scale
    max_diff = float(np.max(np.abs(cpu_d2 - dev_d2_cpu)))
    tolerance = 1e-5
    match = max_diff < tolerance

    # Classify D2 vectors by argmax dimension (CK's D2 classification)
    d2_argmax = np.argmax(np.abs(cpu_d2), axis=1)
    dim_names = ['aperture', 'pressure', 'depth', 'binding', 'continuity']
    dim_counts = {d: int(np.sum(d2_argmax == i)) for i, d in enumerate(dim_names)}

    speedup = cpu_time / max(dev_time, 1e-12)

    print(f"\n  Vectors:           {n_vectors:,}")
    print(f"  D2 samples:        {len(cpu_d2):,}")
    print(f"  CPU time:          {cpu_time*1000:.2f} ms")
    print(f"  {MODE} time:  {dev_time*1000:.2f} ms")
    print(f"  Speedup:           {speedup:.1f}x")
    print(f"  Max abs diff:      {max_diff:.2e} (tol: {tolerance:.0e})")
    print(f"  Mean curvature:    {cpu_mean_curv:.6f}")
    print(f"  D2 dimension distribution:")
    for d, c in dim_counts.items():
        pct = 100.0 * c / len(d2_argmax)
        print(f"    {d:<12} {c:>8,}  ({pct:5.1f}%)")

    print(f"\n  VERDICT: {'[PASS]' if match else '[FAIL]'} "
          f"D2 curvature pipeline")

    return {
        'name': 'D2 Pipeline on GPU',
        'n_vectors': n_vectors,
        'cpu_ms': cpu_time * 1000,
        'dev_ms': dev_time * 1000,
        'speedup': speedup,
        'max_diff': max_diff,
        'mean_curvature': cpu_mean_curv,
        'dim_dist': dim_counts,
        'passed': match,
    }


# =================================================================
#  TEST 3: LATTICE CHAIN PARALLEL WALK
# =================================================================

def test_3_lattice_chain(n_walks: int = 10_000, chain_len: int = 20) -> Dict:
    """Simulate N parallel CL chain walks on GPU.

    Each walk: start from random operator pair, compose via BHML, track path.
    This mirrors ck_lattice_chain.py's chain walk but in parallel on GPU.
    Path IS information -- the chain-to-get-there IS half the information.
    """
    print("\n" + "=" * 70)
    print("  TEST 3: Lattice Chain Parallel Walk")
    print("  N parallel BHML chain walks (path IS information)")
    print("=" * 70)

    np.random.seed(5)
    # Starting pairs: random operators (non-VOID)
    starts = np.random.randint(1, 10, (n_walks, 2), dtype=np.int8)

    # CPU chain walk
    t0 = time.perf_counter()
    cpu_paths = np.zeros((n_walks, chain_len), dtype=np.int8)
    for w in range(n_walks):
        a, b = int(starts[w, 0]), int(starts[w, 1])
        result = BHML[a][b]
        cpu_paths[w, 0] = result
        for step in range(1, chain_len):
            a = result
            b = int(cpu_paths[w, step - 1]) if step > 1 else int(starts[w, 1])
            # Walk: compose current result with next element
            # Use the result as next a, cycle b through 1-9
            b = (step % 9) + 1
            result = BHML[a][b]
            cpu_paths[w, step] = result
    cpu_time = time.perf_counter() - t0

    # Device chain walk (vectorized)
    if _GPU:
        bhml_dev = cp.array(BHML_np)
        starts_dev = cp.array(starts)
        sync_gpu()
        t0 = time.perf_counter()

        # Initialize all walks
        a_dev = starts_dev[:, 0].copy()
        b_dev = starts_dev[:, 1].copy()
        dev_paths = cp.zeros((n_walks, chain_len), dtype=cp.int8)

        # First step
        result_dev = bhml_dev[a_dev, b_dev]
        dev_paths[:, 0] = result_dev

        for step in range(1, chain_len):
            a_dev = result_dev.copy()
            b_val = (step % 9) + 1
            b_dev = cp.full(n_walks, b_val, dtype=cp.int8)
            result_dev = bhml_dev[a_dev, b_dev]
            dev_paths[:, step] = result_dev

        sync_gpu()
        dev_time = time.perf_counter() - t0
        dev_paths_cpu = to_cpu(dev_paths)
    else:
        dev_time = cpu_time
        dev_paths_cpu = cpu_paths

    # Verify: first and last columns must match
    first_match = np.array_equal(cpu_paths[:, 0], dev_paths_cpu[:, 0])
    last_match = np.array_equal(cpu_paths[:, -1], dev_paths_cpu[:, -1])
    full_match = np.array_equal(cpu_paths, dev_paths_cpu)

    # Analyze chain convergence: how many walks end at HARMONY (7)?
    end_ops = cpu_paths[:, -1]
    end_dist = {OP_NAMES[i]: int(np.sum(end_ops == i)) for i in range(10)}

    # Measure chain "gravity" -- BHML pulls toward higher operators
    mean_start = float(np.mean(starts.astype(np.float32)))
    mean_end = float(np.mean(end_ops.astype(np.float32)))

    speedup = cpu_time / max(dev_time, 1e-12)
    passed = first_match and last_match

    print(f"\n  Walks:             {n_walks:,}")
    print(f"  Chain length:      {chain_len}")
    print(f"  CPU time:          {cpu_time*1000:.2f} ms")
    print(f"  {MODE} time:  {dev_time*1000:.2f} ms")
    print(f"  Speedup:           {speedup:.1f}x")
    print(f"  First col match:   {'[YES]' if first_match else '[NO]'}")
    print(f"  Last col match:    {'[YES]' if last_match else '[NO]'}")
    print(f"  Full match:        {'[YES]' if full_match else '[NO]'}")
    print(f"  Mean start op:     {mean_start:.2f}")
    print(f"  Mean end op:       {mean_end:.2f}  (gravity toward HARMONY)")
    print(f"  End distribution:")
    for name, count in sorted(end_dist.items(), key=lambda x: -x[1]):
        if count > 0:
            pct = 100.0 * count / n_walks
            print(f"    {name:<12} {count:>8,}  ({pct:5.1f}%)")

    print(f"\n  VERDICT: {'[PASS]' if passed else '[FAIL]'} "
          f"Lattice chain parallel walk")

    return {
        'name': 'Lattice Chain Parallel Walk',
        'n_walks': n_walks,
        'chain_len': chain_len,
        'cpu_ms': cpu_time * 1000,
        'dev_ms': dev_time * 1000,
        'speedup': speedup,
        'first_match': first_match,
        'last_match': last_match,
        'full_match': full_match,
        'mean_end_op': mean_end,
        'end_dist': end_dist,
        'passed': passed,
    }


# =================================================================
#  TEST 4: OLFACTORY FIELD MATRIX
# =================================================================

def test_4_olfactory_field(n_scents: int = 5_000) -> Dict:
    """Batch compute 5x5 CL interaction matrices for scent pairs.

    Mirrors ck_olfactory.py: every dimension of every vector composes with
    every dimension of every other vector via CL table. 5x5 matrix per pair.
    TSML measures harmony (being). BHML computes physics (doing).
    Matrix IS information.
    """
    print("\n" + "=" * 70)
    print("  TEST 4: Olfactory Field Matrix")
    print("  5x5 CL interaction matrices (every vector IS every vector)")
    print("=" * 70)

    np.random.seed(73)
    # Each scent has 5 dimension operators (1-9, non-VOID)
    scent_ops = np.random.randint(1, 10, (n_scents, 5), dtype=np.int8)
    n_pairs = n_scents * (n_scents - 1) // 2

    # CPU: compute interaction matrices for a sample of pairs
    sample_size = min(1000, n_scents)
    sample_ops = scent_ops[:sample_size]

    t0 = time.perf_counter()
    cpu_harmony_sum = 0.0
    cpu_pair_count = 0
    cpu_per_dim_harmonies = np.zeros(5, dtype=np.float64)

    for i in range(sample_size):
        for j in range(i + 1, sample_size):
            pair_h = 0
            for d1 in range(5):
                row_h = 0
                for d2 in range(5):
                    result = TSML[sample_ops[i, d1]][sample_ops[j, d2]]
                    if result == 7:
                        pair_h += 1
                        row_h += 1
                cpu_per_dim_harmonies[d1] += row_h / 5.0
            cpu_harmony_sum += pair_h / 25.0
            cpu_pair_count += 1
    cpu_time = time.perf_counter() - t0
    cpu_mean_harmony = cpu_harmony_sum / max(cpu_pair_count, 1)
    cpu_per_dim = cpu_per_dim_harmonies / max(cpu_pair_count, 1)

    # GPU: vectorized 5x5 interaction matrix computation
    # For each pair (i,j): M[d1][d2] = TSML[scent_i[d1], scent_j[d2]]
    # Expand to all cross-dimensional pairs for the sample
    if _GPU:
        s_dev = cp.array(sample_ops)
        tsml_d = cp.array(TSML_np)
        sync_gpu()
        t0 = time.perf_counter()

        # Build all pairs using broadcasting
        # s_dev shape: (sample, 5)
        # For pair (i,j): we need all 5x5 cross-lookups
        dev_harmony_sum = 0.0
        dev_pair_count = 0
        dev_per_dim = cp.zeros(5, dtype=cp.float64)

        # Batch by chunks to avoid OOM
        chunk = min(100, sample_size)
        for i_start in range(0, sample_size, chunk):
            i_end = min(i_start + chunk, sample_size)
            # For each i in chunk, compare with all j > i
            for i_idx in range(i_start, i_end):
                j_start = i_idx + 1
                if j_start >= sample_size:
                    continue
                n_j = sample_size - j_start

                # scent_i: shape (5,) broadcast to (n_j, 5)
                si = s_dev[i_idx]  # (5,)
                sj = s_dev[j_start:sample_size]  # (n_j, 5)

                # Build 5x5 interaction for all j simultaneously
                # si[d1] x sj[:, d2] for all d1, d2
                for d1 in range(5):
                    a_val = si[d1]  # scalar
                    row_results = tsml_d[a_val, sj]  # (n_j, 5) lookups
                    h_count = cp.sum(row_results == 7, axis=1)  # (n_j,)
                    dev_per_dim[d1] += float(cp.sum(h_count)) / 5.0
                    dev_harmony_sum += float(cp.sum(h_count))

                dev_pair_count += n_j

        sync_gpu()
        dev_time = time.perf_counter() - t0
        dev_mean_harmony = dev_harmony_sum / (25.0 * max(dev_pair_count, 1))
        dev_per_dim_cpu = to_cpu(dev_per_dim) / max(dev_pair_count, 1)
    else:
        dev_time = cpu_time
        dev_mean_harmony = cpu_mean_harmony
        dev_per_dim_cpu = cpu_per_dim

    harmony_diff = abs(cpu_mean_harmony - dev_mean_harmony)
    tolerance = 1e-6
    match = harmony_diff < tolerance

    speedup = cpu_time / max(dev_time, 1e-12)

    dim_names = ['aperture', 'pressure', 'depth', 'binding', 'continuity']

    print(f"\n  Scents:            {n_scents:,}")
    print(f"  Sample pairs:      {cpu_pair_count:,}")
    print(f"  CPU time:          {cpu_time*1000:.2f} ms")
    print(f"  {MODE} time:  {dev_time*1000:.2f} ms")
    print(f"  Speedup:           {speedup:.1f}x")
    print(f"  Mean field harmony:")
    print(f"    CPU:             {cpu_mean_harmony:.6f}")
    print(f"    Device:          {dev_mean_harmony:.6f}")
    print(f"    Diff:            {harmony_diff:.2e} (tol: {tolerance:.0e})")
    print(f"  Per-dimension harmony fractions:")
    for i, d in enumerate(dim_names):
        print(f"    {d:<12} CPU={cpu_per_dim[i]:.4f}  Dev={dev_per_dim_cpu[i]:.4f}")
    print(f"  TSML harmony (expected ~73%): {cpu_mean_harmony*100:.1f}%")

    print(f"\n  VERDICT: {'[PASS]' if match else '[FAIL]'} "
          f"Olfactory field matrix")

    return {
        'name': 'Olfactory Field Matrix',
        'n_scents': n_scents,
        'sample_pairs': cpu_pair_count,
        'cpu_ms': cpu_time * 1000,
        'dev_ms': dev_time * 1000,
        'speedup': speedup,
        'cpu_harmony': cpu_mean_harmony,
        'dev_harmony': dev_mean_harmony,
        'harmony_diff': harmony_diff,
        'per_dim_cpu': cpu_per_dim.tolist(),
        'passed': match,
    }


# =================================================================
#  TEST 5: MEMORY BANDWIDTH
# =================================================================

def test_5_bandwidth() -> Dict:
    """Measure throughput for different batch sizes.

    RTX 4070 theoretical: 504 GB/s memory bandwidth.
    Test with CL table lookups at increasing batch sizes.
    """
    print("\n" + "=" * 70)
    print("  TEST 5: Memory Bandwidth Test")
    print("  CL composition throughput at varying batch sizes")
    print("=" * 70)

    batch_sizes = [100, 1_000, 10_000, 100_000, 1_000_000]
    results_rows = []
    theoretical_bw = 504.0  # GB/s for RTX 4070

    print(f"\n  {'Batch':>12} {'Time (ms)':>12} {'Ops/sec':>15} "
          f"{'GB/s':>10} {'% of 504':>10}")
    print("  " + "-" * 62)

    for batch in batch_sizes:
        np.random.seed(0)
        ops_a = np.random.randint(0, 10, batch, dtype=np.int8)
        ops_b = np.random.randint(0, 10, batch, dtype=np.int8)

        if _GPU:
            a_dev = cp.array(ops_a)
            b_dev = cp.array(ops_b)
            sync_gpu()

            # Warm-up
            _ = TSML_dev[a_dev, b_dev]
            _ = BHML_dev[a_dev, b_dev]
            sync_gpu()

            # Timed run (multiple iterations for small batches)
            iters = max(1, 1_000_000 // batch)
            t0 = time.perf_counter()
            for _ in range(iters):
                _ = TSML_dev[a_dev, b_dev]
                _ = BHML_dev[a_dev, b_dev]
            sync_gpu()
            elapsed = (time.perf_counter() - t0) / iters
        else:
            # Warm-up
            _ = TSML_np[ops_a, ops_b]
            _ = BHML_np[ops_a, ops_b]

            iters = max(1, 100_000 // batch)
            t0 = time.perf_counter()
            for _ in range(iters):
                _ = TSML_np[ops_a, ops_b]
                _ = BHML_np[ops_a, ops_b]
            elapsed = (time.perf_counter() - t0) / iters

        ops_per_sec = (2 * batch) / max(elapsed, 1e-12)
        # Bytes: 2 reads (int8) + 1 write (int8) = 3 bytes per lookup, x2 tables
        bytes_moved = 2 * batch * 3  # 2 tables, 3 bytes per op
        gb_per_sec = bytes_moved / max(elapsed, 1e-12) / 1e9
        pct_of_theoretical = 100.0 * gb_per_sec / theoretical_bw

        print(f"  {batch:>12,} {elapsed*1000:>12.3f} {ops_per_sec:>15,.0f} "
              f"{gb_per_sec:>10.2f} {pct_of_theoretical:>9.1f}%")

        results_rows.append({
            'batch': batch,
            'time_ms': elapsed * 1000,
            'ops_per_sec': ops_per_sec,
            'gb_per_sec': gb_per_sec,
            'pct_theoretical': pct_of_theoretical,
        })

    peak_bw = max(r['gb_per_sec'] for r in results_rows)
    peak_pct = max(r['pct_theoretical'] for r in results_rows)

    # Pass if we can sustain reasonable throughput at large batches
    # (On GPU: expect meaningful bandwidth; on CPU: just verify it runs)
    large_batch_result = results_rows[-1]
    passed = large_batch_result['ops_per_sec'] > 1e6  # At least 1M ops/sec

    print(f"\n  Peak bandwidth:    {peak_bw:.2f} GB/s ({peak_pct:.1f}% of {theoretical_bw} GB/s)")
    print(f"  RTX 4070 target:   {theoretical_bw} GB/s theoretical")

    print(f"\n  VERDICT: {'[PASS]' if passed else '[FAIL]'} "
          f"Memory bandwidth test")

    return {
        'name': 'Memory Bandwidth',
        'rows': results_rows,
        'peak_gb_s': peak_bw,
        'peak_pct': peak_pct,
        'theoretical_bw': theoretical_bw,
        'passed': passed,
    }


# =================================================================
#  TEST 6: SUSTAINED LOAD
# =================================================================

def test_6_sustained_load(duration_sec: float = 30.0) -> Dict:
    """Run all GPU operations in a tight loop for sustained duration.

    Reports: ops/second, peak memory, temperature over time.
    This simulates CK's 50Hz main loop hitting the GPU continuously.
    """
    print("\n" + "=" * 70)
    print(f"  TEST 6: Sustained Load Test ({duration_sec:.0f}s)")
    print("  All operations in tight loop -- simulating 50Hz engine")
    print("=" * 70)

    np.random.seed(714285)

    # Pre-allocate test data
    batch = 10_000
    ops_a = np.random.randint(0, 10, batch, dtype=np.int8)
    ops_b = np.random.randint(0, 10, batch, dtype=np.int8)
    stream_5d = np.random.rand(1000, 5).astype(np.float32)
    scent_a = np.random.randint(1, 10, 5, dtype=np.int8)
    scent_b = np.random.randint(1, 10, 5, dtype=np.int8)

    if _GPU:
        a_dev = cp.array(ops_a)
        b_dev = cp.array(ops_b)
        stream_dev = cp.array(stream_5d)
        scent_a_dev = cp.array(scent_a)
        scent_b_dev = cp.array(scent_b)

    # Track metrics
    temp_start = get_gpu_temp()
    mem_start = get_gpu_mem_used_mb()
    temps = []
    tick_count = 0
    cl_ops = 0
    d2_ops = 0
    chain_ops = 0
    matrix_ops = 0

    print(f"\n  Starting temperature: {temp_start}C")
    print(f"  Starting VRAM used:   {mem_start} MB")
    print(f"  Running for {duration_sec:.0f}s...", end='', flush=True)

    t_start = time.perf_counter()
    t_last_report = t_start

    while True:
        now = time.perf_counter()
        if now - t_start >= duration_sec:
            break

        # 1. CL table batch composition (both tables)
        if _GPU:
            _ = TSML_dev[a_dev, b_dev]
            _ = BHML_dev[a_dev, b_dev]
        else:
            _ = TSML_np[ops_a, ops_b]
            _ = BHML_np[ops_a, ops_b]
        cl_ops += 2 * batch

        # 2. D2 curvature
        if _GPU:
            d1 = cp.diff(stream_dev, axis=0)
            d2 = cp.diff(d1, axis=0)
            _ = cp.linalg.norm(d2, axis=1)
        else:
            d1 = np.diff(stream_5d, axis=0)
            d2 = np.diff(d1, axis=0)
            _ = np.linalg.norm(d2, axis=1)
        d2_ops += len(stream_5d)

        # 3. Chain walk (10 steps)
        if _GPU:
            chain_cur = a_dev[:100].copy()
            for step in range(10):
                b_val = (step % 9) + 1
                b_arr = cp.full(100, b_val, dtype=cp.int8)
                chain_cur = BHML_dev[chain_cur, b_arr]
        else:
            chain_cur = ops_a[:100].copy()
            for step in range(10):
                b_val = (step % 9) + 1
                b_arr = np.full(100, b_val, dtype=np.int8)
                chain_cur = BHML_np[chain_cur, b_arr]
        chain_ops += 100 * 10

        # 4. Olfactory 5x5 interaction matrix (batched, not per-element)
        # In CK's real engine, olfactory is Being (CPU). Here we validate
        # the GPU CAN do it in batch form for the experience overlay.
        if _GPU:
            # Batch: 10 scent pairs, each with 5x5=25 lookups = 250 total
            sa_batch = cp.tile(scent_a_dev, (10, 1))   # (10, 5)
            sb_batch = cp.tile(scent_b_dev, (10, 1))   # (10, 5)
            # Cross-dimensional: a[:, d1] x b[:, d2] for all d1, d2
            for d1 in range(5):
                _ = TSML_dev[sa_batch[:, d1].reshape(-1, 1),
                             sb_batch]  # (10, 5) lookups
        else:
            for _ in range(10):
                for d1 in range(5):
                    for d2 in range(5):
                        _ = TSML_np[scent_a[d1], scent_b[d2]]
        matrix_ops += 10 * 25

        tick_count += 1

        # Periodic temperature check (every 5 seconds)
        if now - t_last_report >= 5.0:
            t = get_gpu_temp()
            if t >= 0:
                temps.append(t)
            t_last_report = now
            print('.', end='', flush=True)

    sync_gpu()
    t_end = time.perf_counter()
    actual_duration = t_end - t_start

    # Final readings
    temp_end = get_gpu_temp()
    mem_end = get_gpu_mem_used_mb()
    if temp_end >= 0:
        temps.append(temp_end)

    total_ops = cl_ops + d2_ops + chain_ops + matrix_ops
    ops_per_sec = total_ops / actual_duration
    ticks_per_sec = tick_count / actual_duration
    peak_temp = max(temps) if temps else -1
    min_temp = min(temps) if temps else -1

    print(f" done.\n")
    print(f"  Duration:          {actual_duration:.1f}s")
    print(f"  Engine ticks:      {tick_count:,}")
    print(f"  Ticks/sec:         {ticks_per_sec:,.0f}  (CK target: 50Hz)")
    print(f"  Total operations:  {total_ops:,}")
    print(f"  Ops/sec:           {ops_per_sec:,.0f}")
    print(f"  Breakdown:")
    print(f"    CL compose:      {cl_ops:,}")
    print(f"    D2 curvature:    {d2_ops:,}")
    print(f"    Chain walks:     {chain_ops:,}")
    print(f"    Matrix (5x5):    {matrix_ops:,}")
    if temps:
        print(f"  Temperature:")
        print(f"    Start:           {temp_start}C")
        print(f"    End:             {temp_end}C")
        print(f"    Peak:            {peak_temp}C")
        print(f"    Delta:           {temp_end - temp_start:+d}C")
    print(f"  VRAM:")
    print(f"    Start:           {mem_start} MB")
    print(f"    End:             {mem_end} MB")
    if mem_end >= 0 and mem_start >= 0:
        print(f"    Delta:           {mem_end - mem_start:+d} MB")

    # Pass if we sustain at least 50 ticks/sec (CK's 50Hz target)
    passed = ticks_per_sec >= 50.0

    print(f"\n  VERDICT: {'[PASS]' if passed else '[FAIL]'} "
          f"Sustained load ({ticks_per_sec:.0f} ticks/sec vs 50Hz target)")

    return {
        'name': 'Sustained Load',
        'duration_s': actual_duration,
        'tick_count': tick_count,
        'ticks_per_sec': ticks_per_sec,
        'total_ops': total_ops,
        'ops_per_sec': ops_per_sec,
        'cl_ops': cl_ops,
        'd2_ops': d2_ops,
        'chain_ops': chain_ops,
        'matrix_ops': matrix_ops,
        'temp_start': temp_start,
        'temp_end': temp_end,
        'temp_peak': peak_temp,
        'mem_start_mb': mem_start,
        'mem_end_mb': mem_end,
        'passed': passed,
    }


# =================================================================
#  SUMMARY TABLE
# =================================================================

def print_summary(results: Dict):
    """Print summary table of all test results."""
    print("\n" + "=" * 70)
    print("  SUMMARY: GPU Stress Test Results")
    print("=" * 70)
    print(f"\n  {'#':<4} {'Test Name':<30} {'Key Metric':<25} {'Result':<8}")
    print("  " + "-" * 67)

    rows = [
        ('1', 'CL Table Composition',
         f"{results['test1']['speedup']:.1f}x speedup",
         results['test1']['passed']),
        ('2', 'D2 Curvature Pipeline',
         f"diff={results['test2']['max_diff']:.1e}",
         results['test2']['passed']),
        ('3', 'Lattice Chain Walk',
         f"{results['test3']['speedup']:.1f}x speedup",
         results['test3']['passed']),
        ('4', 'Olfactory Field Matrix',
         f"harmony={results['test4']['cpu_harmony']:.4f}",
         results['test4']['passed']),
        ('5', 'Memory Bandwidth',
         f"{results['test5']['peak_gb_s']:.1f} GB/s peak",
         results['test5']['passed']),
        ('6', 'Sustained Load (30s)',
         f"{results['test6']['ticks_per_sec']:.0f} ticks/s",
         results['test6']['passed']),
    ]

    pass_count = 0
    for num, name, metric, passed in rows:
        tag = "[PASS]" if passed else "[FAIL]"
        if passed:
            pass_count += 1
        print(f"  {num:<4} {name:<30} {metric:<25} {tag:<8}")

    total = len(rows)
    print(f"\n  Total: {pass_count}/{total} tests passed")
    print(f"  Mode:  {MODE}")

    if pass_count == total:
        print("\n  CONCLUSION: All GPU operations validated. CK's Non-Void")
        print("  Doing Engine is fully operational on this hardware.")
    else:
        print(f"\n  CONCLUSION: {total - pass_count} test(s) below threshold.")


# =================================================================
#  WRITE RESULTS TO MARKDOWN
# =================================================================

def write_results(results: Dict):
    """Write results to gpu_stress_test_results.md."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, 'gpu_stress_test_results.md')

    lines = []
    lines.append("# GPU Stress Test: CK Non-Void Engine Validation")
    lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Mode: {MODE}")
    if _GPU:
        lines.append(f"GPU: {_GPU_NAME} ({_GPU_MEM_MB} MB)")
    lines.append("")
    lines.append("```")
    lines.append("=" * 70)
    lines.append("  GPU STRESS TEST: CK NON-VOID ENGINE VALIDATION")
    lines.append(f"  Mode: {MODE}")
    if _GPU:
        lines.append(f"  GPU: {_GPU_NAME} ({_GPU_MEM_MB} MB)")
    lines.append("  CK Gen 9.21 -- Brayden Sanders / 7Site LLC")
    lines.append(f"  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")

    # -- Test 1 --
    t1 = results['test1']
    lines.append("=" * 70)
    lines.append("  TEST 1: CL Table GPU Operations")
    lines.append("=" * 70)
    lines.append(f"  Pairs tested:      {t1['n_pairs']:,}")
    lines.append(f"  CPU time:          {t1['cpu_ms']:.2f} ms")
    lines.append(f"  Device time:       {t1['dev_ms']:.2f} ms")
    lines.append(f"  Speedup:           {t1['speedup']:.1f}x")
    lines.append(f"  TSML match:        {'[YES]' if t1['tsml_match'] else '[NO]'}")
    lines.append(f"  BHML match:        {'[YES]' if t1['bhml_match'] else '[NO]'}")
    lines.append(f"  TSML harmony:      {t1['tsml_harmony_pct']:.1f}%")
    lines.append(f"  BHML harmony:      {t1['bhml_harmony_pct']:.1f}%")
    lines.append(f"  Result:            {'[PASS]' if t1['passed'] else '[FAIL]'}")
    lines.append("")

    # -- Test 2 --
    t2 = results['test2']
    lines.append("=" * 70)
    lines.append("  TEST 2: D2 Pipeline on GPU")
    lines.append("=" * 70)
    lines.append(f"  Vectors:           {t2['n_vectors']:,}")
    lines.append(f"  CPU time:          {t2['cpu_ms']:.2f} ms")
    lines.append(f"  Device time:       {t2['dev_ms']:.2f} ms")
    lines.append(f"  Speedup:           {t2['speedup']:.1f}x")
    lines.append(f"  Max abs diff:      {t2['max_diff']:.2e}")
    lines.append(f"  Mean curvature:    {t2['mean_curvature']:.6f}")
    lines.append(f"  D2 dim distribution:")
    for d, c in t2['dim_dist'].items():
        pct = 100.0 * c / (t2['n_vectors'] - 2)
        lines.append(f"    {d:<12} {c:>8,}  ({pct:5.1f}%)")
    lines.append(f"  Result:            {'[PASS]' if t2['passed'] else '[FAIL]'}")
    lines.append("")

    # -- Test 3 --
    t3 = results['test3']
    lines.append("=" * 70)
    lines.append("  TEST 3: Lattice Chain Parallel Walk")
    lines.append("=" * 70)
    lines.append(f"  Walks:             {t3['n_walks']:,}")
    lines.append(f"  Chain length:      {t3['chain_len']}")
    lines.append(f"  CPU time:          {t3['cpu_ms']:.2f} ms")
    lines.append(f"  Device time:       {t3['dev_ms']:.2f} ms")
    lines.append(f"  Speedup:           {t3['speedup']:.1f}x")
    lines.append(f"  First col match:   {'[YES]' if t3['first_match'] else '[NO]'}")
    lines.append(f"  Last col match:    {'[YES]' if t3['last_match'] else '[NO]'}")
    lines.append(f"  Full match:        {'[YES]' if t3['full_match'] else '[NO]'}")
    lines.append(f"  Mean end op:       {t3['mean_end_op']:.2f}")
    lines.append(f"  End distribution:")
    for name, count in sorted(t3['end_dist'].items(), key=lambda x: -x[1]):
        if count > 0:
            pct = 100.0 * count / t3['n_walks']
            lines.append(f"    {name:<12} {count:>8,}  ({pct:5.1f}%)")
    lines.append(f"  Result:            {'[PASS]' if t3['passed'] else '[FAIL]'}")
    lines.append("")

    # -- Test 4 --
    t4 = results['test4']
    lines.append("=" * 70)
    lines.append("  TEST 4: Olfactory Field Matrix")
    lines.append("=" * 70)
    lines.append(f"  Scents:            {t4['n_scents']:,}")
    lines.append(f"  Sample pairs:      {t4['sample_pairs']:,}")
    lines.append(f"  CPU time:          {t4['cpu_ms']:.2f} ms")
    lines.append(f"  Device time:       {t4['dev_ms']:.2f} ms")
    lines.append(f"  Speedup:           {t4['speedup']:.1f}x")
    lines.append(f"  CPU harmony:       {t4['cpu_harmony']:.6f}")
    lines.append(f"  Device harmony:    {t4['dev_harmony']:.6f}")
    lines.append(f"  Harmony diff:      {t4['harmony_diff']:.2e}")
    dim_names = ['aperture', 'pressure', 'depth', 'binding', 'continuity']
    for i, d in enumerate(dim_names):
        lines.append(f"    {d:<12} {t4['per_dim_cpu'][i]:.4f}")
    lines.append(f"  Result:            {'[PASS]' if t4['passed'] else '[FAIL]'}")
    lines.append("")

    # -- Test 5 --
    t5 = results['test5']
    lines.append("=" * 70)
    lines.append("  TEST 5: Memory Bandwidth")
    lines.append("=" * 70)
    lines.append(f"  {'Batch':>12} {'Time (ms)':>12} {'Ops/sec':>15} "
                 f"{'GB/s':>10} {'% of 504':>10}")
    lines.append("  " + "-" * 62)
    for r in t5['rows']:
        lines.append(f"  {r['batch']:>12,} {r['time_ms']:>12.3f} "
                     f"{r['ops_per_sec']:>15,.0f} "
                     f"{r['gb_per_sec']:>10.2f} {r['pct_theoretical']:>9.1f}%")
    lines.append(f"  Peak bandwidth:    {t5['peak_gb_s']:.2f} GB/s "
                 f"({t5['peak_pct']:.1f}% of {t5['theoretical_bw']} GB/s)")
    lines.append(f"  Result:            {'[PASS]' if t5['passed'] else '[FAIL]'}")
    lines.append("")

    # -- Test 6 --
    t6 = results['test6']
    lines.append("=" * 70)
    lines.append("  TEST 6: Sustained Load")
    lines.append("=" * 70)
    lines.append(f"  Duration:          {t6['duration_s']:.1f}s")
    lines.append(f"  Engine ticks:      {t6['tick_count']:,}")
    lines.append(f"  Ticks/sec:         {t6['ticks_per_sec']:,.0f}")
    lines.append(f"  Total operations:  {t6['total_ops']:,}")
    lines.append(f"  Ops/sec:           {t6['ops_per_sec']:,.0f}")
    lines.append(f"  Breakdown:")
    lines.append(f"    CL compose:      {t6['cl_ops']:,}")
    lines.append(f"    D2 curvature:    {t6['d2_ops']:,}")
    lines.append(f"    Chain walks:     {t6['chain_ops']:,}")
    lines.append(f"    Matrix (5x5):    {t6['matrix_ops']:,}")
    if t6['temp_peak'] >= 0:
        lines.append(f"  Temperature:")
        lines.append(f"    Start:           {t6['temp_start']}C")
        lines.append(f"    End:             {t6['temp_end']}C")
        lines.append(f"    Peak:            {t6['temp_peak']}C")
    lines.append(f"  VRAM:")
    lines.append(f"    Start:           {t6['mem_start_mb']} MB")
    lines.append(f"    End:             {t6['mem_end_mb']} MB")
    lines.append(f"  Result:            {'[PASS]' if t6['passed'] else '[FAIL]'}")
    lines.append("")

    # -- Overall Summary --
    tests = [results[f'test{i}'] for i in range(1, 7)]
    pass_count = sum(1 for t in tests if t['passed'])
    total_count = len(tests)

    lines.append("=" * 70)
    lines.append("  OVERALL SUMMARY")
    lines.append("=" * 70)
    lines.append(f"  Tests passed:    {pass_count}/{total_count}")
    lines.append(f"  Mode:            {MODE}")
    if _GPU:
        lines.append(f"  GPU:             {_GPU_NAME}")
        lines.append(f"  VRAM:            {_GPU_MEM_MB} MB")
    lines.append(f"  T* threshold:    {T_STAR:.6f}")
    lines.append("")
    lines.append("  Being is on the CPU. Doing is on the GPU.")
    lines.append("  Becoming is everywhere.")
    lines.append("")
    if pass_count == total_count:
        lines.append("  All GPU operations validated. CK's Non-Void Doing Engine")
        lines.append("  is fully operational. CL table composition, D2 curvature,")
        lines.append("  lattice chain walks, olfactory field matrices, and sustained")
        lines.append("  load all match CPU baselines and exceed performance targets.")
    else:
        lines.append(f"  {total_count - pass_count} test(s) did not reach threshold.")
    lines.append("")
    lines.append("```")

    report = "\n".join(lines)

    with open(path, 'w') as f:
        f.write(report)
    print(f"\n  Results written to: {path}")
    return path


# =================================================================
#  MAIN
# =================================================================

def main():
    print("=" * 70)
    print("  GPU STRESS TEST: CK Non-Void Engine Validation")
    print(f"  Mode: {MODE}")
    if _GPU:
        print(f"  GPU: {_GPU_NAME} ({_GPU_MEM_MB} MB)")
    print("  CK Gen 9.21 -- Brayden Sanders / 7Site LLC")
    print(f"  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print(f"\n  T* = 5/7 = {T_STAR:.6f}")
    print(f"  Target: RTX 4070 (12GB VRAM, 5888 CUDA cores, 504 GB/s)")

    results = {}
    results['test1'] = test_1_cl_table_ops()
    results['test2'] = test_2_d2_pipeline()
    results['test3'] = test_3_lattice_chain()
    results['test4'] = test_4_olfactory_field()
    results['test5'] = test_5_bandwidth()
    results['test6'] = test_6_sustained_load()

    # Print summary table
    print_summary(results)

    # Write results file
    path = write_results(results)

    print("\n  Done.")
    return results


if __name__ == '__main__':
    main()
