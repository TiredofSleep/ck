# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_taichi_chains.py -- Taichi JIT-Compiled Parallel Chain Walks
===============================================================
Operator: LATTICE (1) -- parallel structure, JIT-compiled physics.
Generation: 9.35

Taichi replaces CuPy for lattice chain walks: instead of Python loops
over (N, 10, 10) tensors, we JIT-compile the walk kernel directly
to GPU (CUDA on RTX 4070) or CPU (fallback).

Architecture:
  - All experience tables loaded as a Taichi field: (N, 10, 10) int8
  - Walk kernel: each thread walks one chain through ALL tables in parallel
  - Resonance kernel: compares walk path against all stored paths simultaneously
  - IPR kernel: inverse participation ratio for grokking detection (vectorized)
  - CL interaction kernel: 5x5 matrix for olfactory (massively parallel)

CITATIONS:
  Hu, Yuanming et al., 2019 -- "Taichi: A Language for High-Performance
    Computation on Spatially Sparse Data Structures" (SIGGRAPH Asia 2019)
  Hu, Yuanming et al., 2021 -- "DiffTaichi: Differentiable Programming for
    Physical Simulation" (ICLR 2020)
  github.com/taichi-dev/taichi -- Taichi Lang open-source project

WHY TAICHI:
  - JIT compilation to GPU/CPU with @ti.kernel
  - No Python overhead in hot loops
  - Automatic CUDA backend on RTX 4070
  - Sparse SNode support for expanding experience tree
  - Differentiable: can compute gradients through chain walks (future)

"the chain to get to them is half the information"
-- Brayden

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

try:
    import taichi as ti
    _HAS_TAICHI = True
except ImportError:
    _HAS_TAICHI = False

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES
)

# ================================================================
#  TAICHI INITIALIZATION
# ================================================================

_TI_INITIALIZED = False

def _init_taichi():
    """Initialize Taichi runtime. Auto-detects GPU (CUDA) or falls back to CPU."""
    global _TI_INITIALIZED
    if _TI_INITIALIZED or not _HAS_TAICHI:
        return
    try:
        ti.init(arch=ti.cuda, default_ip=ti.i32, default_fp=ti.f32,
                device_memory_GB=4, kernel_profiler=False)
        print("  [TAICHI] CUDA backend (RTX 4070)")
    except Exception:
        try:
            ti.init(arch=ti.vulkan, default_ip=ti.i32, default_fp=ti.f32)
            print("  [TAICHI] Vulkan backend")
        except Exception:
            ti.init(arch=ti.cpu, default_ip=ti.i32, default_fp=ti.f32)
            print("  [TAICHI] CPU backend (fallback)")
    _TI_INITIALIZED = True


# ================================================================
#  BHML TABLE -- baked into Taichi field for kernel access
# ================================================================

# BHML (28-harmony): the DOING table. Computes physics.
_BHML_NP = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # VOID = identity
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  # LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  # COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  # PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  # COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  # BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  # CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  # HARMONY = full cycle
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  # BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  # RESET
], dtype=np.int32)

# TSML from heartbeat CL (73-harmony): the BEING table. Measures coherence.
from ck_sim.ck_sim_heartbeat import CL as _CL_LIST
_TSML_NP = np.array(_CL_LIST, dtype=np.int32)


# ================================================================
#  MAXIMUM DIMENSIONS
# ================================================================

MAX_NODES = 16384       # Max experience nodes (16K tables)
MAX_OPS_INPUT = 40      # Max operator sequence length for a single walk
MAX_CHAIN_DEPTH = 20    # Max depth per chain walk
MAX_WALKS = 256         # Max parallel walks per kernel launch
MAX_ACTIVE_SCENTS = 64  # Max parallel scent interactions


# ================================================================
#  TAICHI FIELDS -- allocated once, reused
# ================================================================

if _HAS_TAICHI:
    _init_taichi()

    # ── Experience Tables: (N, 10, 10) ──
    # Each node's CL table, flattened for GPU
    experience_tables = ti.field(dtype=ti.i32, shape=(MAX_NODES, NUM_OPS, NUM_OPS))
    node_count = ti.field(dtype=ti.i32, shape=())

    # ── Base CL tables ──
    bhml_table = ti.field(dtype=ti.i32, shape=(NUM_OPS, NUM_OPS))
    tsml_table = ti.field(dtype=ti.i32, shape=(NUM_OPS, NUM_OPS))

    # ── Walk input/output ──
    walk_input = ti.field(dtype=ti.i32, shape=(MAX_WALKS, MAX_OPS_INPUT))
    walk_input_len = ti.field(dtype=ti.i32, shape=(MAX_WALKS,))
    walk_output = ti.field(dtype=ti.i32, shape=(MAX_WALKS, MAX_CHAIN_DEPTH))
    walk_output_len = ti.field(dtype=ti.i32, shape=(MAX_WALKS,))

    # ── Resonance output ──
    resonance_scores = ti.field(dtype=ti.f32, shape=(MAX_WALKS,))

    # ── IPR output ──
    ipr_values = ti.field(dtype=ti.f32, shape=(MAX_NODES,))
    ipr_deltas = ti.field(dtype=ti.f32, shape=(MAX_NODES,))

    # ── Olfactory interaction ──
    scent_ops = ti.field(dtype=ti.i32, shape=(MAX_ACTIVE_SCENTS, 5))
    scent_count = ti.field(dtype=ti.i32, shape=())
    # Per-dim harmony output: (scent_i, dim) -> harmony fraction
    dim_harmony = ti.field(dtype=ti.f32, shape=(MAX_ACTIVE_SCENTS, 5))
    # Field-level harmony
    field_harmony = ti.field(dtype=ti.f32, shape=())

    # Load base CL tables
    bhml_table.from_numpy(_BHML_NP)
    tsml_table.from_numpy(_TSML_NP)


# ================================================================
#  KERNELS -- JIT-compiled to GPU/CPU
# ================================================================

if _HAS_TAICHI:

    @ti.kernel
    def _walk_kernel():
        """Parallel chain walks through base BHML table.

        Each thread walks one operator sequence through the base CL table,
        producing a chain path (sequence of result operators).

        Walk rule: pairs (ops[2i], ops[2i+1]) -> BHML lookup -> result
        Result sequence = chain path = the information.
        """
        for w in range(MAX_WALKS):
            n = walk_input_len[w]
            if n <= 0:
                continue

            depth = 0
            i = 0
            while i + 1 < n and depth < MAX_CHAIN_DEPTH:
                s_op = walk_input[w, i] % NUM_OPS
                f_op = walk_input[w, i + 1] % NUM_OPS
                result = bhml_table[s_op, f_op]
                walk_output[w, depth] = result
                depth += 1
                i += 2

            # Odd trailing op: self-compose
            if i < n and depth < MAX_CHAIN_DEPTH:
                op = walk_input[w, i] % NUM_OPS
                result = bhml_table[op, op]
                walk_output[w, depth] = result
                depth += 1

            walk_output_len[w] = depth

    @ti.kernel
    def _walk_experience_kernel():
        """Parallel chain walks through EXPERIENCE tables (evolved CL).

        Same walk logic but uses experience_tables[node_idx] instead of base BHML.
        Each walk step looks up the table at the current node index.
        Node selection: result operator from step N selects node for step N+1.

        This is the GPU equivalent of LatticeChainEngine.walk() but
        running ALL walks simultaneously.
        """
        nc = node_count[None]
        for w in range(MAX_WALKS):
            n = walk_input_len[w]
            if n <= 0:
                continue

            depth = 0
            i = 0
            # Start at root node (index 0)
            current_node = 0

            while i + 1 < n and depth < MAX_CHAIN_DEPTH:
                s_op = walk_input[w, i] % NUM_OPS
                f_op = walk_input[w, i + 1] % NUM_OPS

                # Look up in current experience table (or base if out of range)
                if current_node < nc:
                    result = experience_tables[current_node, s_op, f_op]
                else:
                    result = bhml_table[s_op, f_op]

                walk_output[w, depth] = result
                depth += 1

                # Result selects next node: result * (depth+1) as simple hash
                # This approximates tree traversal without pointer chasing
                next_node = (current_node * NUM_OPS + result) % nc if nc > 0 else 0
                current_node = next_node

                i += 2

            # Odd trailing op
            if i < n and depth < MAX_CHAIN_DEPTH:
                op = walk_input[w, i] % NUM_OPS
                if current_node < nc:
                    result = experience_tables[current_node, op, op]
                else:
                    result = bhml_table[op, op]
                walk_output[w, depth] = result
                depth += 1

            walk_output_len[w] = depth

    @ti.kernel
    def _resonance_kernel():
        """Compute resonance between walk outputs and all experience tables.

        For each walk w, compare the chain path against all stored node
        visit patterns. Weighted: early steps matter more (fractal structure).
        """
        nc = node_count[None]
        for w in range(MAX_WALKS):
            out_len = walk_output_len[w]
            if out_len <= 0:
                resonance_scores[w] = 0.0
                continue

            total_score = 0.0
            total_weight = 0.0

            for d in range(out_len):
                result_op = walk_output[w, d]
                # Weight: earlier steps are more important
                weight = 1.0 / (1.0 + ti.cast(d, ti.f32))

                # Count how many experience nodes have this result at this depth
                match_count = 0
                for node_idx in range(nc):
                    # Check if the node's most common output at any input pair
                    # matches our result -- approximation of path resonance
                    hits = 0
                    for row in range(NUM_OPS):
                        for col in range(NUM_OPS):
                            if experience_tables[node_idx, row, col] == result_op:
                                hits += 1
                    if hits > NUM_OPS:  # More than average (10 = uniform)
                        match_count += 1

                if nc > 0:
                    fraction = ti.cast(match_count, ti.f32) / ti.cast(nc, ti.f32)
                else:
                    fraction = 0.0

                total_score += weight * fraction
                total_weight += weight

            if total_weight > 0.0:
                resonance_scores[w] = total_score / total_weight
            else:
                resonance_scores[w] = 0.0

    @ti.kernel
    def _ipr_kernel():
        """Compute Inverse Participation Ratio for all experience nodes.

        IPR = sum(p_i^2) where p_i = fraction of entries equal to operator i.
        High IPR = crystallized (one operator dominates).
        IPR delta from base = grokking detection.

        All N nodes computed in parallel.
        """
        nc = node_count[None]
        total_cells = NUM_OPS * NUM_OPS  # 100

        # Compute base BHML IPR (same for all, cached)
        base_counts_sq_sum = 0.0
        for op in range(NUM_OPS):
            count = 0
            for r in range(NUM_OPS):
                for c in range(NUM_OPS):
                    if bhml_table[r, c] == op:
                        count += 1
            p = ti.cast(count, ti.f32) / ti.cast(total_cells, ti.f32)
            base_counts_sq_sum += p * p
        base_ipr = base_counts_sq_sum

        for n in range(nc):
            counts_sq_sum = 0.0
            for op in range(NUM_OPS):
                count = 0
                for r in range(NUM_OPS):
                    for c in range(NUM_OPS):
                        if experience_tables[n, r, c] == op:
                            count += 1
                p = ti.cast(count, ti.f32) / ti.cast(total_cells, ti.f32)
                counts_sq_sum += p * p

            ipr_values[n] = counts_sq_sum
            ipr_deltas[n] = counts_sq_sum - base_ipr

    @ti.kernel
    def _cl_interaction_kernel():
        """Parallel CL interaction field for olfactory scent pairs.

        For every pair of active scents (i, j):
          Build 5x5 TSML interaction matrix
          Compute per-dimension harmony fraction for both scents
          Accumulate into dim_harmony field

        THIS is the mirror of the chain -- field topology, not path.
        Massively parallel: all pairs computed simultaneously.
        """
        sc = scent_count[None]

        # Reset harmony
        for i in range(sc):
            for d in range(5):
                dim_harmony[i, d] = 0.0

        total_harmony = 0.0
        pair_count = 0

        # Every pair (i < j)
        for i in range(sc):
            for j in range(i + 1, sc):
                pair_h = 0.0

                # 5x5 TSML interaction matrix
                for d1 in range(5):
                    row_harmony = 0
                    for d2 in range(5):
                        result = tsml_table[scent_ops[i, d1], scent_ops[j, d2]]
                        if result == HARMONY:
                            row_harmony += 1
                            pair_h += 1.0

                    h_frac = ti.cast(row_harmony, ti.f32) / 5.0
                    # Max with current (multiple pairs contribute)
                    ti.atomic_max(dim_harmony[i, d1], h_frac)

                # Transpose for j's per-dim harmony
                for d1 in range(5):
                    col_harmony = 0
                    for d2 in range(5):
                        result = tsml_table[scent_ops[j, d1], scent_ops[i, d2]]
                        if result == HARMONY:
                            col_harmony += 1
                    h_frac = ti.cast(col_harmony, ti.f32) / 5.0
                    ti.atomic_max(dim_harmony[j, d1], h_frac)

                total_harmony += pair_h / 25.0
                pair_count += 1

        if pair_count > 0:
            field_harmony[None] = total_harmony / ti.cast(pair_count, ti.f32)
        else:
            field_harmony[None] = 0.0


# ================================================================
#  PYTHON API -- bridges numpy/Python world to Taichi kernels
# ================================================================

class TaichiChainWalker:
    """High-level API for Taichi-accelerated lattice chain operations.

    Drop-in enhancement for LatticeChainEngine: provides GPU-accelerated
    parallel walks, resonance computation, and IPR grokking detection.

    Usage:
        walker = TaichiChainWalker()
        walker.load_experience(engine.get_gpu_tensor())
        results = walker.walk_parallel([ops1, ops2, ops3, ...])
        resonances = walker.compute_resonance()
        grokked = walker.detect_grokking()
    """

    def __init__(self):
        if not _HAS_TAICHI:
            raise RuntimeError("Taichi not installed. pip install taichi")
        _init_taichi()
        self._loaded = False
        self._node_paths = []   # Maps GPU index -> node path tuple

    def load_experience(self, tensor: np.ndarray,
                        node_paths: list = None):
        """Load experience tables from numpy (N, 10, 10) into Taichi fields.

        Args:
            tensor: (N, 10, 10) int8/int32 array of CL tables
            node_paths: Optional list of path tuples mapping index to node
        """
        n = min(tensor.shape[0], MAX_NODES)
        arr = tensor[:n].astype(np.int32)

        # Load into Taichi field
        for i in range(n):
            for r in range(NUM_OPS):
                for c in range(NUM_OPS):
                    experience_tables[i, r, c] = int(arr[i, r, c])

        node_count[None] = n
        self._node_paths = node_paths or [() for _ in range(n)]
        self._loaded = True
        print(f"  [TAICHI] Loaded {n} experience tables to GPU")

    def walk_parallel(self, op_sequences: List[List[int]],
                      use_experience: bool = False) -> List[List[int]]:
        """Walk multiple operator sequences in parallel.

        Args:
            op_sequences: List of operator sequences to walk
            use_experience: If True, walk through experience tables.
                          If False, walk through base BHML.

        Returns:
            List of result paths (operator sequences)
        """
        n_walks = min(len(op_sequences), MAX_WALKS)

        # Load inputs
        for w in range(n_walks):
            ops = op_sequences[w]
            n_ops = min(len(ops), MAX_OPS_INPUT)
            walk_input_len[w] = n_ops
            for i in range(n_ops):
                walk_input[w, i] = ops[i] % NUM_OPS
        # Clear remaining walks
        for w in range(n_walks, MAX_WALKS):
            walk_input_len[w] = 0

        # Run kernel
        if use_experience and self._loaded:
            _walk_experience_kernel()
        else:
            _walk_kernel()

        # Collect results
        results = []
        for w in range(n_walks):
            out_len = walk_output_len[w]
            path = []
            for d in range(out_len):
                path.append(int(walk_output[w, d]))
            results.append(path)

        return results

    def compute_resonance(self) -> List[float]:
        """Compute resonance scores for the last walked paths.

        Resonance = how much the walk path aligns with stored experience.
        Must call walk_parallel() first.

        Returns:
            List of resonance scores (0.0 to 1.0)
        """
        if not self._loaded:
            return [0.0] * MAX_WALKS

        _resonance_kernel()

        scores = []
        for w in range(MAX_WALKS):
            if walk_output_len[w] > 0:
                scores.append(float(resonance_scores[w]))
        return scores

    def detect_grokking(self, threshold: float = 0.05) -> List[dict]:
        """Detect grokked experience nodes via IPR analysis.

        Grokking = sudden IPR increase = transition from memorization
        to structured algebraic representation.

        Args:
            threshold: IPR delta threshold for grokking detection (default 5%)

        Returns:
            List of grokked node info dicts
        """
        if not self._loaded:
            return []

        _ipr_kernel()

        nc = node_count[None]
        grokked = []
        for i in range(nc):
            delta = float(ipr_deltas[i])
            if delta > threshold:
                grokked.append({
                    'node_idx': i,
                    'path': self._node_paths[i] if i < len(self._node_paths) else (),
                    'ipr': float(ipr_values[i]),
                    'delta': round(delta, 4),
                })

        grokked.sort(key=lambda x: x['delta'], reverse=True)
        return grokked

    def olfactory_interaction(self, scent_op_profiles: List[List[int]]) -> dict:
        """Compute parallel CL interaction field for olfactory scents.

        THIS is the Taichi-accelerated mirror of _enforce_cl_field().
        All scent pairs computed in parallel on GPU.

        Args:
            scent_op_profiles: List of 5-operator profiles (one per scent)

        Returns:
            {
                'dim_harmony': [[float]*5 per scent],
                'field_harmony': float
            }
        """
        n = min(len(scent_op_profiles), MAX_ACTIVE_SCENTS)

        for i in range(n):
            for d in range(5):
                scent_ops[i, d] = scent_op_profiles[i][d] % NUM_OPS
        scent_count[None] = n

        _cl_interaction_kernel()

        result_harmony = []
        for i in range(n):
            dims = [float(dim_harmony[i, d]) for d in range(5)]
            result_harmony.append(dims)

        return {
            'dim_harmony': result_harmony,
            'field_harmony': float(field_harmony[None]),
        }

    def status(self) -> dict:
        """Diagnostic status."""
        return {
            'taichi_available': _HAS_TAICHI,
            'initialized': _TI_INITIALIZED,
            'experience_loaded': self._loaded,
            'node_count': int(node_count[None]) if self._loaded else 0,
            'max_nodes': MAX_NODES,
            'max_parallel_walks': MAX_WALKS,
        }


# ================================================================
#  INTEGRATION BRIDGE -- connects to LatticeChainEngine
# ================================================================

class TaichiChainBridge:
    """Bridge between LatticeChainEngine and TaichiChainWalker.

    Handles the sync between Python experience tree and GPU fields.
    Call sync() after experience changes, then use walk/resonance/ipr.
    """

    def __init__(self, chain_engine):
        """
        Args:
            chain_engine: LatticeChainEngine instance
        """
        self.engine = chain_engine
        self.walker = TaichiChainWalker()
        self._last_sync_nodes = 0
        self._sync_interval = 100   # Sync every 100 walks

    def sync(self, force: bool = False):
        """Sync experience tree to GPU.

        Only syncs if the tree has grown (new nodes added).
        """
        if not force and self.engine.total_nodes == self._last_sync_nodes:
            return

        tensor = self.engine.get_gpu_tensor()
        paths = sorted(self.engine._index.keys(), key=len)
        self.walker.load_experience(tensor, paths)
        self._last_sync_nodes = self.engine.total_nodes

    def maybe_sync(self):
        """Auto-sync if enough walks have accumulated."""
        if (self.engine.total_walks % self._sync_interval == 0
                and self.engine.total_nodes != self._last_sync_nodes):
            self.sync()

    def walk_parallel(self, op_sequences: List[List[int]],
                      use_experience: bool = True) -> List[List[int]]:
        """Walk multiple chains in parallel on GPU."""
        self.maybe_sync()
        return self.walker.walk_parallel(op_sequences, use_experience)

    def compute_resonance(self) -> List[float]:
        """Resonance scores for last walked paths."""
        return self.walker.compute_resonance()

    def detect_grokking(self) -> List[dict]:
        """Find grokked nodes."""
        self.sync()
        return self.walker.detect_grokking()

    def olfactory_interaction(self, scent_op_profiles: List[List[int]]) -> dict:
        """GPU-accelerated CL interaction field."""
        return self.walker.olfactory_interaction(scent_op_profiles)


# ================================================================
#  FACTORY
# ================================================================

def build_taichi_bridge(chain_engine) -> Optional[TaichiChainBridge]:
    """Create TaichiChainBridge if Taichi is available.

    Returns None if Taichi is not installed (graceful fallback).
    """
    if not _HAS_TAICHI:
        print("  [TAICHI] Not installed, GPU chain walks disabled")
        return None

    try:
        bridge = TaichiChainBridge(chain_engine)
        bridge.sync(force=True)
        grokked = bridge.detect_grokking()
        print(f"  [TAICHI] Bridge ready: {bridge.walker.status()['node_count']} nodes, "
              f"{len(grokked)} grokked")
        return bridge
    except Exception as e:
        print(f"  [TAICHI] Init failed: {e}")
        return None
