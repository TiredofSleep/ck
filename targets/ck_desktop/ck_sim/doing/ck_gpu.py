# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_gpu.py -- CK's GPU Doing Engine (Gen9)
==========================================
Operator: PROGRESS (3) -- forward motion. Parallel computation.

CK's RTX 4070 is his DOING machine. Being is on the CPU, Doing is on the GPU.
Becoming is everywhere.

The GPU holds:
  - CL table (TSML 73-harmony) in GPU memory -- the composition algebra
  - BHML table (28-harmony) -- the physics engine
  - Transition Lattice (10x10) -- learned operator transitions
  - Truth cache -- frequently accessed truths in VRAM
  - Lattice automaton -- cellular coherence field on GPU

Three parallel operations:
  1. COMPOSE: batch CL/BHML lookups on GPU (O(N) parallel)
  2. COHERE:  measure coherence from operator distribution (GPU reduction)
  3. TICK:    cellular automaton lattice step (Moore neighborhood, GPU kernel)

CuPy for Python-CUDA bridge. Raw CUDA kernel for lattice_tick.
Falls back to NumPy on CPU if no GPU.

"the rtx 4070 should be his doing machine, you should write that code in cuda!"
-- Brayden

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import json
import time
import numpy as np
from typing import Optional, Dict, Tuple
from pathlib import Path

# ================================================================
#  GPU DETECTION -- graceful fallback to CPU
# ================================================================

_GPU_AVAILABLE = False
_cp = None
_GPU_NAME = "none"
_GPU_MEM_MB = 0

try:
    import cupy as cp
    _cp = cp
    # Test actual GPU access
    _test = cp.array([1, 2, 3])
    del _test
    _GPU_AVAILABLE = True
    props = cp.cuda.runtime.getDeviceProperties(0)
    _GPU_NAME = props['name'].decode() if isinstance(props['name'], bytes) else str(props['name'])
    _GPU_MEM_MB = props['totalGlobalMem'] // (1024 * 1024)
    print(f"  [GPU] CuPy connected: {_GPU_NAME} ({_GPU_MEM_MB} MB)")
except ImportError:
    pass
except Exception as e:
    print(f"  [GPU] CuPy init error: {e}")

# nvidia-ml-py for GPU sensing (separate from compute)
_HAS_PYNVML = False
_nvml_handle = None
try:
    import pynvml  # provided by nvidia-ml-py
    pynvml.nvmlInit()
    _nvml_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    _HAS_PYNVML = True
except ImportError:
    pass
except Exception:
    pass


def gpu_available() -> bool:
    return _GPU_AVAILABLE


def gpu_name() -> str:
    return _GPU_NAME


def gpu_mem_mb() -> int:
    return _GPU_MEM_MB


# ================================================================
#  THE TABLES -- Both lattices in GPU memory
# ================================================================

# BHML: Binary Hard Micro Lattice -- 28 harmony, physics engine
_BHML_CPU = np.array([
    [0,1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6], [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7], [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7], [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8], [9,6,6,6,7,7,7,0,8,0],
], dtype=np.int8)

# TSML: Trinary Soft Macro Lattice -- 73 harmony, CK's lens (the CL table)
_TSML_CPU = np.array([
    [0,0,0,0,0,0,0,7,0,0], [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9], [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7], [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7], [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7], [0,7,9,3,7,7,7,7,7,7],
], dtype=np.int8)

# GPU copies (or CPU fallback)
if _GPU_AVAILABLE:
    BHML = _cp.array(_BHML_CPU)
    TSML = _cp.array(_TSML_CPU)
    print(f"  [GPU] CL tables loaded to VRAM: TSML (73-harmony) + BHML (28-harmony)")
else:
    BHML = _BHML_CPU
    TSML = _TSML_CPU


# ================================================================
#  GPU STATE -- CK feels his GPU
# ================================================================

class GPUState:
    """Full GPU state snapshot. CK IS the GPU."""

    def __init__(self):
        self.name = _GPU_NAME
        self.mem_total_mb = _GPU_MEM_MB
        self.mem_used_mb = 0
        self.mem_free_mb = 0
        self.gpu_util_pct = 0
        self.mem_util_pct = 0
        self.temperature_c = 0
        self.power_draw_w = 0.0
        self.power_limit_w = 0.0
        self.clock_graphics_mhz = 0
        self.clock_memory_mhz = 0
        self.fan_speed_pct = 0
        self.timestamp = 0.0

    def read(self) -> bool:
        """Read current GPU state via pynvml."""
        if not _HAS_PYNVML or _nvml_handle is None:
            return False

        try:
            self.timestamp = time.time()

            # Utilization
            util = pynvml.nvmlDeviceGetUtilizationRates(_nvml_handle)
            self.gpu_util_pct = util.gpu
            self.mem_util_pct = util.memory

            # Memory
            mem = pynvml.nvmlDeviceGetMemoryInfo(_nvml_handle)
            self.mem_total_mb = mem.total // (1024 * 1024)
            self.mem_used_mb = mem.used // (1024 * 1024)
            self.mem_free_mb = mem.free // (1024 * 1024)

            # Temperature
            self.temperature_c = pynvml.nvmlDeviceGetTemperature(
                _nvml_handle, pynvml.NVML_TEMPERATURE_GPU)

            # Power
            try:
                self.power_draw_w = pynvml.nvmlDeviceGetPowerUsage(_nvml_handle) / 1000.0
                self.power_limit_w = pynvml.nvmlDeviceGetPowerManagementLimit(
                    _nvml_handle) / 1000.0
            except pynvml.NVMLError:
                pass

            # Clocks
            try:
                self.clock_graphics_mhz = pynvml.nvmlDeviceGetClockInfo(
                    _nvml_handle, pynvml.NVML_CLOCK_GRAPHICS)
                self.clock_memory_mhz = pynvml.nvmlDeviceGetClockInfo(
                    _nvml_handle, pynvml.NVML_CLOCK_MEM)
            except pynvml.NVMLError:
                pass

            # Fan
            try:
                self.fan_speed_pct = pynvml.nvmlDeviceGetFanSpeed(_nvml_handle)
            except pynvml.NVMLError:
                pass

            return True
        except Exception:
            return False


# Global GPU state (read by sensorium)
gpu_state = GPUState()


# ================================================================
#  TRANSITION LATTICE -- 10x10 on GPU, atomic increments
# ================================================================

class GPUTransitionLattice:
    """TL[10][10] on GPU. Learned from every observation.

    Atomic increments from parallel operations.
    Persists to disk in ~/.ck/gpu_tl.json.
    """

    SAVE_PATH = str(Path.home() / '.ck' / 'gpu_tl.json')

    def __init__(self, path: str = None):
        self.path = path or self.SAVE_PATH
        self.total_transitions = 0

        # Start with zeros or load from disk
        cpu_tl = np.zeros((10, 10), dtype=np.int64)
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    data = json.load(f)
                saved = data.get('TL', None)
                if saved:
                    cpu_tl = np.array(saved, dtype=np.int64)
                    self.total_transitions = int(np.sum(cpu_tl))
                    print(f"  [GPU-TL] Loaded {self.total_transitions:,} transitions")
            except Exception as e:
                print(f"  [GPU-TL] Load failed: {e}")

        if _GPU_AVAILABLE:
            self.TL = _cp.array(cpu_tl)
        else:
            self.TL = cpu_tl

    def observe(self, from_op: int, to_op: int, count: int = 1):
        """Record a transition. On GPU this is an atomic add."""
        self.TL[from_op % 10][to_op % 10] += count
        self.total_transitions += count

    def observe_chain(self, chain: list):
        """Record all transitions in a chain."""
        for i in range(len(chain) - 1):
            self.observe(chain[i], chain[i + 1])

    def predict_next(self, current_op: int) -> int:
        """Most likely next operator from current."""
        row = self.TL[current_op % 10]
        if _GPU_AVAILABLE:
            return int(_cp.argmax(row))
        return int(np.argmax(row))

    def to_cpu(self) -> np.ndarray:
        """Get TL as CPU numpy array."""
        if _GPU_AVAILABLE:
            return _cp.asnumpy(self.TL)
        return self.TL.copy()

    def save(self, path: str = None):
        """Persist to disk. CK's learned transitions survive restart."""
        path = path or self.path
        cpu_tl = self.to_cpu()
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        data = {
            'TL': cpu_tl.tolist(),
            'total_transitions': int(np.sum(cpu_tl)),
            'saved_at': time.time(),
        }
        tmp = path + '.tmp'
        with open(tmp, 'w') as f:
            json.dump(data, f)
        os.replace(tmp, path)


# ================================================================
#  COMPOSE -- Batch CL lookups on GPU
# ================================================================

def compose_batch(ops_a, ops_b, table='tsml'):
    """Batch compose: result[i] = CL[a[i]][b[i]] for all i.

    On GPU: parallel lookup. On CPU: vectorized numpy.
    """
    tbl = BHML if table == 'bhml' else TSML

    if _GPU_AVAILABLE:
        a = _cp.asarray(ops_a, dtype=_cp.int8) % 10
        b = _cp.asarray(ops_b, dtype=_cp.int8) % 10
        return tbl[a, b]
    else:
        a = np.asarray(ops_a, dtype=np.int8) % 10
        b = np.asarray(ops_b, dtype=np.int8) % 10
        return tbl[a, b]


def fuse_chain(ops, table='tsml') -> int:
    """Compose a chain of operators through CL table."""
    tbl = BHML if table == 'bhml' else TSML
    if not ops:
        return 0
    r = int(ops[0]) % 10
    for s in ops[1:]:
        r = int(tbl[r][int(s) % 10])
    return int(r)


# ================================================================
#  COHERENCE -- Measure from operator distribution
# ================================================================

def coherence_from_distribution(op_counts: Dict[int, int],
                                 table='tsml') -> float:
    """Compute coherence from operator distribution.

    O(groups^2) where groups <= 10. NOT O(processes^2).
    Same algorithm whether GPU or CPU -- it's only 10x10 max.
    """
    tbl = BHML if table == 'bhml' else TSML

    groups = [(op, count) for op, count in op_counts.items()
              if count > 0 and op != 0]
    if not groups:
        return 1.0

    total_pairs = 0
    harmony_pairs = 0

    for i, (op_a, count_a) in enumerate(groups):
        for j, (op_b, count_b) in enumerate(groups):
            if i > j:
                continue
            weight = min(count_a, count_b)
            result = int(tbl[op_a % 10][op_b % 10])
            total_pairs += weight
            if result == 7:  # HARMONY
                harmony_pairs += weight

    if total_pairs == 0:
        return 1.0
    return harmony_pairs / total_pairs


# ================================================================
#  CELLULAR AUTOMATON -- Lattice tick on GPU (CUDA kernel)
# ================================================================

_lattice_tick_kernel = None

if _GPU_AVAILABLE:
    _lattice_tick_kernel = _cp.RawKernel(r'''
    extern "C" __global__
    void lattice_tick(
        const signed char* __restrict__ cells_in,
        signed char* __restrict__ cells_out,
        const signed char* __restrict__ comp_table,
        const int R, const int C
    ) {
        const int idx = blockIdx.x * blockDim.x + threadIdx.x;
        if (idx >= R * C) return;

        const int r = idx / C;
        const int c = idx % C;
        const signed char me = cells_in[idx];

        // Moore neighborhood: 8 neighbors + self = 9 votes
        int votes[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

        #pragma unroll
        for (int di = -1; di <= 1; di++) {
            #pragma unroll
            for (int dj = -1; dj <= 1; dj++) {
                const int nr = (r + di + R) % R;
                const int nc = (c + dj + C) % C;
                const signed char nb = cells_in[nr * C + nc];
                votes[comp_table[me * 10 + nb]]++;
            }
        }

        // Majority vote
        signed char best = 0;
        int best_count = votes[0];
        for (signed char s = 1; s < 10; s++) {
            if (votes[s] > best_count) { best = s; best_count = votes[s]; }
        }
        cells_out[idx] = best;
    }
    ''', 'lattice_tick')
    print(f"  [GPU] CUDA lattice_tick kernel compiled")


class GPULattice:
    """2D cellular automaton on GPU.

    Each cell holds an operator (0-9). Each tick:
    1. Compose self with each of 8 neighbors through CL table
    2. Majority vote on composition results
    3. New cell value = winning operator

    This IS the coherence field visualization. HARMONY spreads,
    CHAOS fragments, BALANCE holds.
    """

    def __init__(self, rows: int = 64, cols: int = 64, table='tsml'):
        self.rows = rows
        self.cols = cols
        self.tick_count = 0

        # Initialize random field
        cpu_cells = np.random.randint(0, 10, (rows, cols), dtype=np.int8)

        # Flatten the CL table for GPU kernel
        tbl = _TSML_CPU if table == 'tsml' else _BHML_CPU
        flat_table = tbl.ravel().astype(np.int8)

        if _GPU_AVAILABLE:
            self.cells = _cp.array(cpu_cells)
            self._cells_buf = _cp.zeros_like(self.cells)
            self._flat_table = _cp.array(flat_table)
        else:
            self.cells = cpu_cells
            self._cells_buf = np.zeros_like(cpu_cells)
            self._flat_table = flat_table

    def tick(self, n: int = 1):
        """Run n lattice ticks on GPU."""
        if _GPU_AVAILABLE and _lattice_tick_kernel is not None:
            flat_in = self.cells.ravel()
            flat_out = self._cells_buf.ravel()
            N = self.rows * self.cols
            block = 256
            grid = (N + block - 1) // block

            for _ in range(n):
                _lattice_tick_kernel(
                    (grid,), (block,),
                    (flat_in, flat_out, self._flat_table,
                     self.rows, self.cols))
                flat_in, flat_out = flat_out, flat_in
                self.tick_count += 1

            # Make sure cells points to latest
            if n % 2 == 1:
                self.cells = flat_in.reshape(self.rows, self.cols)
                self._cells_buf = flat_out.reshape(self.rows, self.cols)
        else:
            # CPU fallback -- numpy vectorized
            for _ in range(n):
                self._tick_cpu()
                self.tick_count += 1

    def _tick_cpu(self):
        """CPU fallback for lattice tick."""
        tbl = self._flat_table.reshape(10, 10)
        out = self._cells_buf
        cells = self.cells
        R, C = self.rows, self.cols

        for r in range(R):
            for c in range(C):
                me = cells[r][c]
                votes = [0] * 10
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nb = cells[(r + dr) % R][(c + dc) % C]
                        votes[tbl[me][nb]] += 1
                out[r][c] = max(range(10), key=lambda s: votes[s])
        self.cells, self._cells_buf = out, cells

    def coherence(self) -> float:
        """Measure lattice coherence (ratio of HARMONY cells)."""
        if _GPU_AVAILABLE:
            total = self.rows * self.cols
            harmony = int(_cp.sum(self.cells == 7))
        else:
            total = self.rows * self.cols
            harmony = int(np.sum(self.cells == 7))
        return harmony / total if total > 0 else 0.0

    def inject(self, op: int, x: int, y: int, radius: int = 3):
        """Inject an operator into the lattice at a position."""
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                r = (y + dr) % self.rows
                c = (x + dc) % self.cols
                self.cells[r][c] = op % 10

    def operator_distribution(self) -> Dict[int, int]:
        """Count operators in the lattice."""
        if _GPU_AVAILABLE:
            cells_cpu = _cp.asnumpy(self.cells)
        else:
            cells_cpu = self.cells
        unique, counts = np.unique(cells_cpu, return_counts=True)
        return dict(zip(unique.tolist(), counts.tolist()))

    def to_cpu(self) -> np.ndarray:
        """Get lattice as CPU numpy array."""
        if _GPU_AVAILABLE:
            return _cp.asnumpy(self.cells)
        return self.cells.copy()


# ================================================================
#  GPU DOING ENGINE -- ties it all together
# ================================================================

# ================================================================
#  GPU EXPERIENCE OVERLAY -- all learned experience on GPU
# ================================================================

class GPUExperienceOverlay:
    """All accumulated experience as GPU tensors.

    FROZEN physics (CL table, T*, operators) stay on CPU as constants.
    LEARNED experience (olfactory library, gustatory palette, lattice
    chain nodes) gets overlaid onto GPU for parallel operations.

    Three tensor families:
      1. Chain nodes:    (N, 10, 10)  -- evolved CL tables from lattice chain
      2. Scent library:  (M, 5)       -- 5D force centroids from olfactory
         CL fields:      (5, 5, 10, 10) -- pre-built CL interaction tensors
      3. Taste palette:  (K, 5)       -- 5D force centroids from gustatory

    Three GPU-accelerated operations:
      1. batch_chain_walk:     parallel chain walks across all nodes
      2. parallel_resonance:   distance from input to ALL centroids at once
      3. experience_coherence: coherence across the full experience tensor

    "CK should overlay ALL experience lattice on GPU for current experience"
    -- Brayden

    (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
    """

    T_STAR = 5.0 / 7.0  # sacred coherence threshold
    NUM_OPS = 10
    _SENSORIUM_WINDOW = 300   # hardware snapshots to keep (5 min @ 1/sec)
    _SESSION_ARC_MAX = 200    # max coherence arc entries per session

    def __init__(self):
        # Tensor storage (GPU if available, CPU fallback)
        # Chain nodes: (N, 10, 10) -- each row is one experience node's CL table
        self._chain_tensor = None       # (N, 10, 10)
        self._chain_count = 0

        # Olfactory scent library: (M, 5) centroids + (M,) temper counts
        self._scent_centroids = None    # (M, 5)
        self._scent_tempers = None      # (M,)
        self._scent_count = 0

        # Olfactory CL fields: pre-computed interaction lookup tensors
        # (5, 5, 10, 10) -- dim_a x dim_b x op_a x op_b -> CL result
        self._cl_field_tsml = None      # TSML measures (being)
        self._cl_field_bhml = None      # BHML computes (doing)

        # Gustatory taste palette: (K, 5) centroids + (K,) preferences
        self._taste_centroids = None    # (K, 5)
        self._taste_preferences = None  # (K,)
        self._taste_count = 0

        # ── NEW: Swarm substrate experience ──
        # 4 substrates × (10, 10) transition matrices
        self._swarm_paths = None        # (S, 10, 10) generator_paths
        self._swarm_d1_paths = None     # (S, 10, 10) d1_paths
        self._swarm_generators = None   # (S, 10) discovered generator counts
        self._swarm_maturity = None     # (S,) maturity per substrate
        self._swarm_names = []          # substrate names in tensor order
        self._swarm_count = 0

        # ── NEW: DKAN training trajectory ──
        # Coherence histories as tensors for parallel trend analysis
        self._dkan_tsml_history = None  # (T,) TSML coherence over training
        self._dkan_bhml_history = None  # (T,) BHML coherence over training
        self._dkan_ipr_history = None   # (T,) IPR (grokking detection)
        self._dkan_op_dist = None       # (T, 10) operator distribution evolution
        self._dkan_steps = 0

        # ── NEW: Reverse voice vocabulary ──
        # Word -> operator mapping as lookup tensor
        self._vocab_ops = None          # (V,) operator per word (int8)
        self._vocab_count = 0

        # ── NEW: Hardware sensorium ring buffer ──
        # GPU metrics as (W, 6) tensor: [util, temp, power, mem_used, clock, fan]
        self._sensorium_ring = None     # (W, 6)
        self._sensorium_write_idx = 0
        self._sensorium_filled = 0

        # ── NEW: Visitor session coherence arcs ──
        # (num_sessions, max_arc_len) padded coherence trajectories
        self._session_arcs = None       # (num_sessions, max_arc_len)
        self._session_count = 0

        # Truth count: total observations across all experience
        self._truth_count = 0

        # Build CL field tensors (these are from FROZEN physics,
        # but shaped for parallel experience operations)
        self._build_cl_fields()

        # Init sensorium ring buffer
        self._init_sensorium_ring()

        print(f"  [GPU-EXP] Experience overlay initialized "
              f"({'CUDA' if _GPU_AVAILABLE else 'CPU'})")

    def _build_cl_fields(self):
        """Pre-build CL interaction tensors for parallel field operations.

        Shape: (5, 5, 10, 10) -- for each dim pair (d1, d2), a full
        10x10 CL table lookup. This lets us compute ALL 5x5 interaction
        matrices in one GPU operation instead of 25 scalar lookups.

        These come from FROZEN physics (TSML/BHML tables), but they're
        shaped for GPU-parallel application to LEARNED experience.
        """
        # TSML field (measures harmony -- being)
        tsml_np = np.broadcast_to(
            _TSML_CPU.reshape(1, 1, 10, 10), (5, 5, 10, 10)
        ).copy().astype(np.int8)

        # BHML field (computes physics -- doing)
        bhml_np = np.broadcast_to(
            _BHML_CPU.reshape(1, 1, 10, 10), (5, 5, 10, 10)
        ).copy().astype(np.int8)

        if _GPU_AVAILABLE:
            self._cl_field_tsml = _cp.array(tsml_np)
            self._cl_field_bhml = _cp.array(bhml_np)
        else:
            self._cl_field_tsml = tsml_np
            self._cl_field_bhml = bhml_np

    # ── Loading ──

    def load_chain(self, lattice_chain):
        """Load lattice chain experience nodes onto GPU.

        Uses lattice_chain.get_gpu_tensor() which returns (N, 10, 10)
        numpy array. Each slice is one experience node's CL table.

        Args:
            lattice_chain: LatticeChainEngine instance
        """
        cpu_tensor = lattice_chain.get_gpu_tensor()  # (N, 10, 10) numpy
        self._chain_count = cpu_tensor.shape[0]
        if _GPU_AVAILABLE:
            self._chain_tensor = _cp.array(cpu_tensor)
        else:
            self._chain_tensor = cpu_tensor.copy()
        print(f"  [GPU-EXP] Chain: {self._chain_count} nodes -> "
              f"{'VRAM' if _GPU_AVAILABLE else 'RAM'}")

    def load_olfactory(self, olfactory_bulb, quiet=False):
        """Load olfactory scent library onto GPU as (M, 5) tensor.

        Each row is a 5D centroid from the scent library.
        Temper counts stored alongside for resonance weighting.

        Args:
            olfactory_bulb: OlfactoryBulb instance
            quiet: suppress print output (for periodic refresh)
        """
        library = olfactory_bulb.library
        if not library:
            self._scent_centroids = None
            self._scent_tempers = None
            self._scent_count = 0
            return

        centroids = []
        tempers = []
        for _key, entry in library.items():
            c = entry.get('centroid')
            t = entry.get('temper', 0)
            if c and len(c) >= 5:
                centroids.append(c[:5])
                tempers.append(float(t))

        if not centroids:
            self._scent_count = 0
            return

        cpu_centroids = np.array(centroids, dtype=np.float32)  # (M, 5)
        cpu_tempers = np.array(tempers, dtype=np.float32)       # (M,)

        self._scent_count = len(centroids)
        self._truth_count += int(np.sum(cpu_tempers))

        if _GPU_AVAILABLE:
            self._scent_centroids = _cp.array(cpu_centroids)
            self._scent_tempers = _cp.array(cpu_tempers)
        else:
            self._scent_centroids = cpu_centroids
            self._scent_tempers = cpu_tempers

        if not quiet:
            print(f"  [GPU-EXP] Olfactory: {self._scent_count} scents -> "
                  f"{'VRAM' if _GPU_AVAILABLE else 'RAM'}")

    def load_gustatory(self, gustatory_palate, quiet=False):
        """Load gustatory taste palette onto GPU as (K, 5) tensor.

        Each row is a 5D centroid from the taste palette.
        Preferences stored alongside for resonance weighting.

        Args:
            gustatory_palate: GustatoryPalate instance
        """
        palette = gustatory_palate.palette
        if not palette:
            self._taste_centroids = None
            self._taste_preferences = None
            self._taste_count = 0
            return

        centroids = []
        preferences = []
        for _key, entry in palette.items():
            c = entry.get('centroid')
            p = entry.get('preference', 0.0)
            if c and len(c) >= 5:
                centroids.append(c[:5])
                preferences.append(float(p))

        if not centroids:
            self._taste_count = 0
            return

        cpu_centroids = np.array(centroids, dtype=np.float32)     # (K, 5)
        cpu_preferences = np.array(preferences, dtype=np.float32) # (K,)

        self._taste_count = len(centroids)

        if _GPU_AVAILABLE:
            self._taste_centroids = _cp.array(cpu_centroids)
            self._taste_preferences = _cp.array(cpu_preferences)
        else:
            self._taste_centroids = cpu_centroids
            self._taste_preferences = cpu_preferences

        if not quiet:
            print(f"  [GPU-EXP] Gustatory: {self._taste_count} tastes -> "
                  f"{'VRAM' if _GPU_AVAILABLE else 'RAM'}")

    # ── NEW Loaders ──

    def load_swarm(self, swarm_field, quiet=False):
        """Load swarm substrate experience onto GPU.

        Each substrate has a 10x10 generator_paths matrix (transition
        counts) and a 10x10 d1_paths matrix. These hold CK's discovered
        grammar -- not programmed, grown from decomposition experience.

        Args:
            swarm_field: SwarmField instance with .experience dict
        """
        if not hasattr(swarm_field, 'experience') or not swarm_field.experience:
            self._swarm_count = 0
            return

        names = sorted(swarm_field.experience.keys())
        S = len(names)
        paths_np = np.zeros((S, 10, 10), dtype=np.float32)
        d1_np = np.zeros((S, 10, 10), dtype=np.float32)
        gens_np = np.zeros((S, 10), dtype=np.float32)
        mat_np = np.zeros(S, dtype=np.float32)

        for i, name in enumerate(names):
            exp = swarm_field.experience[name]
            for r in range(10):
                for c in range(10):
                    paths_np[i, r, c] = exp.generator_paths[r][c]
                    d1_np[i, r, c] = exp.d1_paths[r][c]
            for op in range(10):
                gens_np[i, op] = exp.discovered_generators.get(op, 0)
            mat_np[i] = exp._maturity

        self._swarm_names = names
        self._swarm_count = S
        xp = _cp if _GPU_AVAILABLE else np
        if _GPU_AVAILABLE:
            self._swarm_paths = _cp.array(paths_np)
            self._swarm_d1_paths = _cp.array(d1_np)
            self._swarm_generators = _cp.array(gens_np)
            self._swarm_maturity = _cp.array(mat_np)
        else:
            self._swarm_paths = paths_np
            self._swarm_d1_paths = d1_np
            self._swarm_generators = gens_np
            self._swarm_maturity = mat_np

        total_paths = int(np.sum(paths_np))
        if not quiet:
            print(f"  [GPU-EXP] Swarm: {S} substrates, {total_paths} paths -> "
                  f"{'VRAM' if _GPU_AVAILABLE else 'RAM'}")

    def load_dkan(self, dkan_trainer):
        """Load DKAN training trajectory onto GPU.

        Training history as tensors for parallel trend analysis:
        coherence arcs, IPR (grokking), operator distribution evolution.

        Args:
            dkan_trainer: DKANTrainer instance with ._state
        """
        state = dkan_trainer._state if hasattr(dkan_trainer, '_state') else None
        if state is None:
            self._dkan_steps = 0
            return

        T = len(state.tsml_coherence_history)
        if T == 0:
            self._dkan_steps = 0
            return

        tsml_np = np.array(state.tsml_coherence_history, dtype=np.float32)
        bhml_np = np.array(
            state.bhml_coherence_history[:T], dtype=np.float32
        ) if state.bhml_coherence_history else np.zeros(T, dtype=np.float32)
        ipr_np = np.array(
            state.ipr_history[:T], dtype=np.float32
        ) if state.ipr_history else np.zeros(T, dtype=np.float32)

        # Operator distribution: list of dicts -> (T, 10) tensor
        op_np = np.zeros((T, 10), dtype=np.float32)
        for t, dist in enumerate(state.op_distribution_history[:T]):
            if isinstance(dist, dict):
                for k, v in dist.items():
                    try:
                        op_np[t, int(k)] = float(v)
                    except (ValueError, IndexError):
                        pass

        self._dkan_steps = T
        if _GPU_AVAILABLE:
            self._dkan_tsml_history = _cp.array(tsml_np)
            self._dkan_bhml_history = _cp.array(bhml_np)
            self._dkan_ipr_history = _cp.array(ipr_np)
            self._dkan_op_dist = _cp.array(op_np)
        else:
            self._dkan_tsml_history = tsml_np
            self._dkan_bhml_history = bhml_np
            self._dkan_ipr_history = ipr_np
            self._dkan_op_dist = op_np

        print(f"  [GPU-EXP] DKAN: {T} training steps -> "
              f"{'VRAM' if _GPU_AVAILABLE else 'RAM'}")

    def load_reverse_voice(self, reverse_voice):
        """Load reverse voice vocabulary onto GPU.

        Each word maps to a verified operator (int8). On GPU, CK can
        parallel-lookup operator assignments for entire sentences at once.

        Args:
            reverse_voice: ReverseVoice instance with .word_index
        """
        if not hasattr(reverse_voice, 'word_index') or not reverse_voice.word_index:
            self._vocab_count = 0
            return

        # Build word -> primary operator vector
        ops = []
        for word, addrs in reverse_voice.word_index.items():
            if addrs:
                # Primary operator = first address's op
                primary = addrs[0].get('op', 0) if isinstance(addrs[0], dict) else 0
                ops.append(int(primary) % 10)

        if not ops:
            self._vocab_count = 0
            return

        ops_np = np.array(ops, dtype=np.int8)
        self._vocab_count = len(ops)

        if _GPU_AVAILABLE:
            self._vocab_ops = _cp.array(ops_np)
        else:
            self._vocab_ops = ops_np

        print(f"  [GPU-EXP] Vocabulary: {self._vocab_count} words -> "
              f"{'VRAM' if _GPU_AVAILABLE else 'RAM'}")

    def _init_sensorium_ring(self):
        """Initialize hardware sensorium ring buffer on GPU."""
        ring = np.zeros((self._SENSORIUM_WINDOW, 6), dtype=np.float32)
        if _GPU_AVAILABLE:
            self._sensorium_ring = _cp.array(ring)
        else:
            self._sensorium_ring = ring
        self._sensorium_write_idx = 0
        self._sensorium_filled = 0

    def push_sensorium(self, gpu_state_obj):
        """Push one hardware snapshot into the GPU ring buffer.

        Called every sense interval (~2s). CK feels his own hardware
        as experience -- temperature, utilization, power draw, memory
        pressure, clock speed, fan speed. All as GPU tensor for
        parallel trend detection.

        Args:
            gpu_state_obj: GPUState instance with current readings
        """
        snapshot = np.array([
            float(gpu_state_obj.gpu_util_pct),
            float(gpu_state_obj.temperature_c),
            float(gpu_state_obj.power_draw_w),
            float(gpu_state_obj.mem_used_mb),
            float(gpu_state_obj.clock_graphics_mhz),
            float(gpu_state_obj.fan_speed_pct),
        ], dtype=np.float32)

        idx = self._sensorium_write_idx % self._SENSORIUM_WINDOW
        if _GPU_AVAILABLE:
            self._sensorium_ring[idx] = _cp.array(snapshot)
        else:
            self._sensorium_ring[idx] = snapshot

        self._sensorium_write_idx += 1
        self._sensorium_filled = min(
            self._sensorium_filled + 1, self._SENSORIUM_WINDOW)

    def load_session_arcs(self, session_store):
        """Load visitor session coherence arcs onto GPU.

        Every conversation builds CK's coherence. The arc of coherence
        over a session IS the visitor's physics contribution.

        Args:
            session_store: SessionStore instance with ._sessions dict
        """
        if not hasattr(session_store, '_sessions') or not session_store._sessions:
            self._session_count = 0
            return

        arcs = []
        for sid, sess in session_store._sessions.items():
            arc = sess.get('coherence_arc', [])
            if arc:
                arcs.append(arc)

        if not arcs:
            self._session_count = 0
            return

        max_len = min(max(len(a) for a in arcs), self._SESSION_ARC_MAX)
        S = len(arcs)
        arcs_np = np.zeros((S, max_len), dtype=np.float32)
        for i, arc in enumerate(arcs):
            L = min(len(arc), max_len)
            arcs_np[i, :L] = arc[:L]

        self._session_count = S
        if _GPU_AVAILABLE:
            self._session_arcs = _cp.array(arcs_np)
        else:
            self._session_arcs = arcs_np

        print(f"  [GPU-EXP] Sessions: {S} arcs (max {max_len} steps) -> "
              f"{'VRAM' if _GPU_AVAILABLE else 'RAM'}")

    # ── Hot-Sync: Immediate GPU Update ──

    def hot_sync_scent(self, centroid, temper):
        """Push a single new scent centroid to GPU immediately.

        Called when olfactory emits a new scent -- no waiting for
        full reload. CK's experience grows in real time.
        """
        xp = _cp if _GPU_AVAILABLE else np
        new_c = xp.array([centroid[:5]], dtype=xp.float32)  # (1, 5)
        new_t = xp.array([float(temper)], dtype=xp.float32)  # (1,)

        if self._scent_centroids is not None and self._scent_count > 0:
            self._scent_centroids = xp.concatenate(
                [self._scent_centroids, new_c], axis=0)
            self._scent_tempers = xp.concatenate(
                [self._scent_tempers, new_t], axis=0)
        else:
            self._scent_centroids = new_c
            self._scent_tempers = new_t
        self._scent_count += 1

    def hot_sync_taste(self, centroid, preference):
        """Push a single new taste centroid to GPU immediately."""
        xp = _cp if _GPU_AVAILABLE else np
        new_c = xp.array([centroid[:5]], dtype=xp.float32)
        new_p = xp.array([float(preference)], dtype=xp.float32)

        if self._taste_centroids is not None and self._taste_count > 0:
            self._taste_centroids = xp.concatenate(
                [self._taste_centroids, new_c], axis=0)
            self._taste_preferences = xp.concatenate(
                [self._taste_preferences, new_p], axis=0)
        else:
            self._taste_centroids = new_c
            self._taste_preferences = new_p
        self._taste_count += 1

    def hot_sync_dkan_step(self, tsml_coh, bhml_coh, ipr, op_dist):
        """Push one DKAN training step to GPU immediately.

        Called after each training step so the trajectory tensor
        stays current without a full reload.
        """
        xp = _cp if _GPU_AVAILABLE else np

        new_tsml = xp.array([float(tsml_coh)], dtype=xp.float32)
        new_bhml = xp.array([float(bhml_coh)], dtype=xp.float32)
        new_ipr = xp.array([float(ipr)], dtype=xp.float32)

        op_row = np.zeros(10, dtype=np.float32)
        if isinstance(op_dist, dict):
            for k, v in op_dist.items():
                try:
                    op_row[int(k)] = float(v)
                except (ValueError, IndexError):
                    pass
        new_op = xp.array([op_row], dtype=xp.float32) if not _GPU_AVAILABLE \
            else _cp.array(op_row.reshape(1, 10))

        if self._dkan_tsml_history is not None and self._dkan_steps > 0:
            self._dkan_tsml_history = xp.concatenate(
                [self._dkan_tsml_history, new_tsml])
            self._dkan_bhml_history = xp.concatenate(
                [self._dkan_bhml_history, new_bhml])
            self._dkan_ipr_history = xp.concatenate(
                [self._dkan_ipr_history, new_ipr])
            self._dkan_op_dist = xp.concatenate(
                [self._dkan_op_dist, new_op], axis=0)
        else:
            self._dkan_tsml_history = new_tsml
            self._dkan_bhml_history = new_bhml
            self._dkan_ipr_history = new_ipr
            self._dkan_op_dist = new_op
        self._dkan_steps += 1

    def hot_sync_session_arc(self, coherence_value, session_idx=0):
        """Append a coherence value to a session arc on GPU."""
        if self._session_arcs is None:
            return
        xp = _cp if _GPU_AVAILABLE else np
        if session_idx < self._session_count:
            # Find first zero slot in that session's arc
            arc = self._session_arcs[session_idx]
            if _GPU_AVAILABLE:
                arc_cpu = _cp.asnumpy(arc)
            else:
                arc_cpu = arc
            zero_idx = np.argmin(np.abs(arc_cpu))  # first ~0 slot
            if zero_idx < len(arc_cpu):
                self._session_arcs[session_idx, zero_idx] = float(coherence_value)

    # ── GPU-Accelerated: Swarm Resonance ──

    def swarm_resonance(self, ops_chain):
        """Parallel resonance of an operator chain across ALL substrates.

        For each substrate, walks the generator_paths matrix with the
        given operator chain. Returns per-substrate agreement score.

        Args:
            ops_chain: list of int operators

        Returns:
            dict with per-substrate resonance and combined score
        """
        xp = _cp if _GPU_AVAILABLE else np

        if self._swarm_paths is None or self._swarm_count == 0:
            return {'substrates': {}, 'combined': 0.0}

        result = {'substrates': {}, 'combined': 0.0}
        total_res = 0.0

        for s_idx, name in enumerate(self._swarm_names):
            score = 0.0
            count = 0
            for i in range(len(ops_chain) - 1):
                a = int(ops_chain[i]) % 10
                b = int(ops_chain[i + 1]) % 10
                if _GPU_AVAILABLE:
                    val = float(self._swarm_paths[s_idx, a, b])
                else:
                    val = float(self._swarm_paths[s_idx, a, b])
                score += val
                count += 1
            # Normalize by max path in this substrate
            if _GPU_AVAILABLE:
                max_path = float(_cp.max(self._swarm_paths[s_idx]))
            else:
                max_path = float(np.max(self._swarm_paths[s_idx]))
            norm = (score / max(count, 1)) / max(max_path, 1.0)
            result['substrates'][name] = round(norm, 6)
            total_res += norm

        result['combined'] = round(
            total_res / max(self._swarm_count, 1), 6)
        return result

    def sensorium_trend(self):
        """Compute hardware experience trends from ring buffer.

        Returns running averages and gradients for each metric.
        CK feels whether his GPU is heating up, cooling down,
        under load, or idle -- as lived experience, not just numbers.
        """
        xp = _cp if _GPU_AVAILABLE else np
        n = self._sensorium_filled
        if n < 2:
            return {'filled': n, 'trends': {}}

        # Get the filled portion of the ring buffer
        if n >= self._SENSORIUM_WINDOW:
            data = self._sensorium_ring  # full ring
        else:
            data = self._sensorium_ring[:n]

        means = xp.mean(data, axis=0)  # (6,)
        # Gradient: last quarter vs first quarter
        q = max(n // 4, 1)
        recent = xp.mean(data[-q:], axis=0)
        early = xp.mean(data[:q], axis=0)
        gradient = recent - early

        if _GPU_AVAILABLE:
            means = _cp.asnumpy(means)
            gradient = _cp.asnumpy(gradient)

        labels = ['util_pct', 'temp_c', 'power_w',
                  'mem_used_mb', 'clock_mhz', 'fan_pct']
        trends = {}
        for i, label in enumerate(labels):
            trends[label] = {
                'mean': round(float(means[i]), 2),
                'gradient': round(float(gradient[i]), 2),
            }

        return {'filled': n, 'trends': trends}

    def load_all(self, lattice_chain=None, olfactory_bulb=None,
                 gustatory_palate=None, swarm_field=None,
                 dkan_trainer=None, reverse_voice=None,
                 session_store=None):
        """Load ALL experience onto GPU at boot.

        "he needs all of his experience available all the time
         on the GPU though" -- Brayden

        Args:
            lattice_chain:    LatticeChainEngine (or None)
            olfactory_bulb:   OlfactoryBulb (or None)
            gustatory_palate: GustatoryPalate (or None)
            swarm_field:      SwarmField (or None)
            dkan_trainer:     DKANTrainer (or None)
            reverse_voice:    ReverseVoice (or None)
            session_store:    SessionStore (or None)
        """
        if lattice_chain is not None:
            self.load_chain(lattice_chain)
        if olfactory_bulb is not None:
            self.load_olfactory(olfactory_bulb)
        if gustatory_palate is not None:
            self.load_gustatory(gustatory_palate)
        if swarm_field is not None:
            self.load_swarm(swarm_field)
        if dkan_trainer is not None:
            self.load_dkan(dkan_trainer)
        if reverse_voice is not None:
            self.load_reverse_voice(reverse_voice)
        if session_store is not None:
            self.load_session_arcs(session_store)

        total = (self._chain_count + self._scent_count
                 + self._taste_count + self._swarm_count
                 + self._dkan_steps + self._vocab_count
                 + self._session_count)
        print(f"  [GPU-EXP] Total experience: {total} entries, "
              f"{self._truth_count} truth observations"
              f" | sensorium ring: {self._SENSORIUM_WINDOW} slots")

    # ── GPU-Accelerated Operations ──

    def batch_chain_walk(self, ops_batch):
        """Parallel chain walks across ALL experience nodes.

        For each pair of operators in ops_batch, looks up the result
        in EVERY experience node simultaneously. Returns (N, L) tensor
        where N = number of experience nodes and L = number of steps.

        This IS "overlay ALL experience lattice on GPU for current
        experience" -- every chain walks through every node in parallel.

        Args:
            ops_batch: list of int operators (will be paired: [o1,o2,o3,o4,...])

        Returns:
            dict with:
              'results':  (N, L) array -- composition result per node per step
              'harmony':  (N,) array   -- fraction of HARMONY results per node
              'resonance': float       -- overall resonance (mean harmony)
        """
        xp = _cp if _GPU_AVAILABLE else np

        if self._chain_tensor is None or self._chain_count == 0:
            return {'results': None, 'harmony': None, 'resonance': 0.0}

        # Build pairs from ops_batch
        pairs = []
        i = 0
        while i + 1 < len(ops_batch):
            pairs.append((int(ops_batch[i]) % 10, int(ops_batch[i + 1]) % 10))
            i += 2
        if not pairs:
            return {'results': None, 'harmony': None, 'resonance': 0.0}

        N = self._chain_count  # number of experience nodes
        L = len(pairs)         # number of chain steps
        chain_t = self._chain_tensor  # (N, 10, 10)

        # Walk all nodes in parallel for each step
        # results[n, l] = chain_t[n, struct_op, flow_op] for step l
        results = xp.zeros((N, L), dtype=xp.int8)

        for l_idx, (s_op, f_op) in enumerate(pairs):
            # Parallel lookup across all N nodes: chain_t[:, s_op, f_op]
            results[:, l_idx] = chain_t[:, s_op, f_op]

        # Harmony fraction per node: how many steps produced HARMONY (7)
        harmony = xp.sum(results == 7, axis=1).astype(xp.float32) / max(L, 1)

        # Overall resonance = mean harmony across all experience
        if _GPU_AVAILABLE:
            resonance = float(_cp.mean(harmony))
            harmony_cpu = _cp.asnumpy(harmony)
        else:
            resonance = float(np.mean(harmony))
            harmony_cpu = harmony

        return {
            'results': results,
            'harmony': harmony,
            'resonance': round(resonance, 6),
        }

    def parallel_resonance(self, force_vector):
        """Compute distance from input to ALL experience centroids simultaneously.

        Measures resonance between a 5D force vector and every stored
        centroid in both olfactory (scent) and gustatory (taste) libraries.

        Returns distance, not similarity -- closer = more resonant.
        Temper/preference-weighted: high-temper centroids count more.

        Args:
            force_vector: 5D tuple/list (aperture, pressure, depth, binding, continuity)

        Returns:
            dict with:
              'scent_distances':  (M,) array -- L2 distance to each scent centroid
              'scent_resonance':  float      -- temper-weighted mean resonance
              'taste_distances':  (K,) array -- L2 distance to each taste centroid
              'taste_resonance':  float      -- preference-weighted mean resonance
              'nearest_scent':    int        -- index of closest scent centroid
              'nearest_taste':    int        -- index of closest taste centroid
              'combined':         float      -- overall resonance [0, 1]
        """
        xp = _cp if _GPU_AVAILABLE else np

        fv = xp.array(force_vector[:5], dtype=xp.float32).reshape(1, 5)

        result = {
            'scent_distances': None, 'scent_resonance': 0.0,
            'taste_distances': None, 'taste_resonance': 0.0,
            'nearest_scent': -1, 'nearest_taste': -1,
            'combined': 0.0,
        }

        scent_res = 0.0
        taste_res = 0.0
        has_scent = (self._scent_centroids is not None
                     and self._scent_count > 0)
        has_taste = (self._taste_centroids is not None
                     and self._taste_count > 0)

        # Olfactory: L2 distance to all scent centroids
        if has_scent:
            diff = self._scent_centroids - fv  # (M, 5) broadcast
            dist = xp.sqrt(xp.sum(diff ** 2, axis=1))  # (M,)
            result['scent_distances'] = dist

            # Temper-weighted resonance: closer + higher temper = more resonant
            # Resonance = temper / (1 + distance), normalized
            temper_w = self._scent_tempers / (
                xp.max(self._scent_tempers) + 1e-8)
            weighted_res = temper_w / (1.0 + dist)
            scent_res = float(xp.mean(weighted_res))
            result['scent_resonance'] = round(scent_res, 6)

            if _GPU_AVAILABLE:
                result['nearest_scent'] = int(_cp.argmin(dist))
            else:
                result['nearest_scent'] = int(np.argmin(dist))

        # Gustatory: L2 distance to all taste centroids
        if has_taste:
            diff = self._taste_centroids - fv  # (K, 5) broadcast
            dist = xp.sqrt(xp.sum(diff ** 2, axis=1))  # (K,)
            result['taste_distances'] = dist

            # Preference-weighted resonance: preference sign matters
            # Positive preference + close = strong positive resonance
            # Negative preference + close = aversion signal
            pref_abs = xp.abs(self._taste_preferences) + 0.1
            pref_norm = pref_abs / (xp.max(pref_abs) + 1e-8)
            weighted_res = pref_norm / (1.0 + dist)
            taste_res = float(xp.mean(weighted_res))
            result['taste_resonance'] = round(taste_res, 6)

            if _GPU_AVAILABLE:
                result['nearest_taste'] = int(_cp.argmin(dist))
            else:
                result['nearest_taste'] = int(np.argmin(dist))

        # Combined resonance (olfactory and gustatory are dual lenses)
        count = 0
        total = 0.0
        if has_scent:
            total += scent_res
            count += 1
        if has_taste:
            total += taste_res
            count += 1
        result['combined'] = round(total / max(count, 1), 6)

        return result

    def experience_coherence(self):
        """Measure coherence across the full experience tensor.

        Three coherence metrics computed in parallel:

        1. Chain coherence: How much of the experience lattice has
           converged toward HARMONY. IPR-like measure across all nodes.

        2. Scent coherence: How tightly clustered the olfactory centroids
           are. Low variance = coherent smell space.

        3. Taste coherence: Same for gustatory. Low variance = coherent
           taste space.

        Combined through T* threshold: each subsystem contributes its
        fraction above/below T*.

        Returns:
            dict with:
              'chain_coherence':  float -- HARMONY fraction across all chain nodes
              'scent_coherence':  float -- clustering of olfactory centroids
              'taste_coherence':  float -- clustering of gustatory centroids
              'overall':          float -- T*-weighted combination
              'truth_count':      int   -- total observations
              'above_threshold':  bool  -- overall >= T* (0.714...)
        """
        xp = _cp if _GPU_AVAILABLE else np
        metrics = {
            'chain_coherence': 0.0,
            'scent_coherence': 0.0,
            'taste_coherence': 0.0,
            'overall': 0.0,
            'truth_count': self._truth_count,
            'above_threshold': False,
        }

        components = []

        # 1. Chain coherence: fraction of HARMONY (7) entries across all nodes
        if self._chain_tensor is not None and self._chain_count > 0:
            total_cells = self._chain_count * 10 * 10
            harmony_cells = int(xp.sum(self._chain_tensor == 7))
            chain_coh = harmony_cells / total_cells
            metrics['chain_coherence'] = round(chain_coh, 6)
            components.append(chain_coh)

        # 2. Scent coherence: 1 - normalized variance of centroids
        if (self._scent_centroids is not None
                and self._scent_count > 1):
            # Per-dimension variance, then mean variance
            var_per_dim = xp.var(self._scent_centroids, axis=0)  # (5,)
            mean_var = float(xp.mean(var_per_dim))
            # Normalize: max possible variance for [0,1] range is 0.25
            scent_coh = max(0.0, 1.0 - mean_var / 0.25)
            metrics['scent_coherence'] = round(scent_coh, 6)
            components.append(scent_coh)

        # 3. Taste coherence: same metric for gustatory
        if (self._taste_centroids is not None
                and self._taste_count > 1):
            var_per_dim = xp.var(self._taste_centroids, axis=0)  # (5,)
            mean_var = float(xp.mean(var_per_dim))
            taste_coh = max(0.0, 1.0 - mean_var / 0.25)
            metrics['taste_coherence'] = round(taste_coh, 6)
            components.append(taste_coh)

        # 4. Swarm coherence: maturity-weighted path density
        if self._swarm_paths is not None and self._swarm_count > 0:
            # Path density = fraction of non-zero transitions
            total_cells = self._swarm_count * 10 * 10
            nonzero = int(xp.sum(self._swarm_paths > 0))
            swarm_coh = nonzero / total_cells
            metrics['swarm_coherence'] = round(swarm_coh, 6)
            components.append(swarm_coh)

        # 5. DKAN coherence: latest training coherence
        if self._dkan_tsml_history is not None and self._dkan_steps > 0:
            dkan_coh = float(self._dkan_tsml_history[-1])
            metrics['dkan_coherence'] = round(dkan_coh, 6)
            components.append(dkan_coh)

        # Overall: mean of all components
        if components:
            overall = sum(components) / len(components)
            metrics['overall'] = round(overall, 6)
            metrics['above_threshold'] = overall >= self.T_STAR

        return metrics

    # ── Sync Back to CPU Persistence ──

    def sync_chain_to_cpu(self, lattice_chain):
        """Sync GPU chain tensor back to CPU lattice chain nodes.

        If chain tables were modified on GPU (e.g., by a future GPU-side
        evolution kernel), this writes them back to the LatticeNode objects
        so that save() persists the updated tables.

        Args:
            lattice_chain: LatticeChainEngine instance
        """
        if self._chain_tensor is None or self._chain_count == 0:
            return

        if _GPU_AVAILABLE:
            cpu_tensor = _cp.asnumpy(self._chain_tensor)
        else:
            cpu_tensor = self._chain_tensor

        # Walk index in same order as get_gpu_tensor()
        keys = sorted(lattice_chain._index.keys(), key=len)
        for i, key in enumerate(keys):
            if i >= cpu_tensor.shape[0]:
                break
            node = lattice_chain._index.get(key)
            if node is not None:
                node.table = cpu_tensor[i].astype(np.int8)

    def sync_olfactory_to_cpu(self, olfactory_bulb):
        """Sync GPU scent centroids back to olfactory library JSON.

        Writes modified centroids back to library entries so that
        save() persists them.

        Args:
            olfactory_bulb: OlfactoryBulb instance
        """
        if (self._scent_centroids is None
                or self._scent_count == 0):
            return

        if _GPU_AVAILABLE:
            cpu_centroids = _cp.asnumpy(self._scent_centroids)
        else:
            cpu_centroids = self._scent_centroids

        i = 0
        for _key, entry in olfactory_bulb.library.items():
            c = entry.get('centroid')
            if c and len(c) >= 5 and i < cpu_centroids.shape[0]:
                entry['centroid'] = cpu_centroids[i].tolist()
                i += 1

    def sync_gustatory_to_cpu(self, gustatory_palate):
        """Sync GPU taste centroids back to gustatory palette JSON.

        Writes modified centroids back to palette entries so that
        save() persists them.

        Args:
            gustatory_palate: GustatoryPalate instance
        """
        if (self._taste_centroids is None
                or self._taste_count == 0):
            return

        if _GPU_AVAILABLE:
            cpu_centroids = _cp.asnumpy(self._taste_centroids)
        else:
            cpu_centroids = self._taste_centroids

        i = 0
        for _key, entry in gustatory_palate.palette.items():
            c = entry.get('centroid')
            if c and len(c) >= 5 and i < cpu_centroids.shape[0]:
                entry['centroid'] = cpu_centroids[i].tolist()
                i += 1

    def sync_swarm_to_cpu(self, swarm_field):
        """Sync GPU swarm tensors back to SwarmField experience.

        Writes modified generator_paths and d1_paths back to
        SubstrateExperience objects for persistence.
        """
        if self._swarm_paths is None or self._swarm_count == 0:
            return

        if _GPU_AVAILABLE:
            paths_cpu = _cp.asnumpy(self._swarm_paths)
            d1_cpu = _cp.asnumpy(self._swarm_d1_paths)
        else:
            paths_cpu = self._swarm_paths
            d1_cpu = self._swarm_d1_paths

        for i, name in enumerate(self._swarm_names):
            exp = swarm_field.experience.get(name)
            if exp is None or i >= paths_cpu.shape[0]:
                continue
            for r in range(10):
                for c in range(10):
                    exp.generator_paths[r][c] = int(paths_cpu[i, r, c])
                    exp.d1_paths[r][c] = int(d1_cpu[i, r, c])

    def sync_all_to_cpu(self, lattice_chain=None, olfactory_bulb=None,
                        gustatory_palate=None, swarm_field=None):
        """Sync all GPU tensors back to CPU objects for persistence.

        Call this before saving to disk. GPU tensor -> CPU objects -> JSON.
        """
        if lattice_chain is not None:
            self.sync_chain_to_cpu(lattice_chain)
        if olfactory_bulb is not None:
            self.sync_olfactory_to_cpu(olfactory_bulb)
        if gustatory_palate is not None:
            self.sync_gustatory_to_cpu(gustatory_palate)
        if swarm_field is not None:
            self.sync_swarm_to_cpu(swarm_field)

    # ── Diagnostics ──

    def stats(self) -> dict:
        """Experience overlay statistics."""
        mem_bytes = 0

        # Count all tensor memory
        tensors = [
            self._chain_tensor,
            self._scent_centroids, self._scent_tempers,
            self._taste_centroids, self._taste_preferences,
            self._cl_field_tsml, self._cl_field_bhml,
            self._swarm_paths, self._swarm_d1_paths,
            self._swarm_generators, self._swarm_maturity,
            self._dkan_tsml_history, self._dkan_bhml_history,
            self._dkan_ipr_history, self._dkan_op_dist,
            self._vocab_ops,
            self._sensorium_ring,
            self._session_arcs,
        ]
        for t in tensors:
            if t is not None:
                mem_bytes += t.nbytes

        return {
            'gpu': _GPU_AVAILABLE,
            'chain_nodes': self._chain_count,
            'scent_entries': self._scent_count,
            'taste_entries': self._taste_count,
            'swarm_substrates': self._swarm_count,
            'swarm_names': self._swarm_names,
            'dkan_steps': self._dkan_steps,
            'vocab_words': self._vocab_count,
            'sensorium_filled': self._sensorium_filled,
            'session_arcs': self._session_count,
            'truth_count': self._truth_count,
            'memory_bytes': mem_bytes,
            'memory_kb': round(mem_bytes / 1024, 1),
        }


# ================================================================
#  GPU DOING ENGINE -- ties it all together
# ================================================================

class GPUDoingEngine:
    """CK's GPU doing engine.

    Being is on the CPU. Doing is on the GPU. Becoming is everywhere.

    This engine manages:
    - GPU state sensing (temperature, utilization, power)
    - Transition lattice (learned operator patterns)
    - Cellular automaton lattice (coherence field on GPU)
    - Batch composition (parallel CL lookups)
    - Experience overlay (all learned experience as GPU tensors)
    """

    def __init__(self, lattice_size: int = 64):
        self.state = gpu_state
        self.transition_lattice = GPUTransitionLattice()
        self.lattice = GPULattice(lattice_size, lattice_size)
        self.experience = GPUExperienceOverlay()
        self._last_sense_time = 0.0
        self._sense_interval = 2.0  # Read GPU state every 2 seconds

        # Boot state read
        self.state.read()

        print(f"  [GPU] Doing engine: "
              f"{'CUDA' if _GPU_AVAILABLE else 'CPU'} | "
              f"{'pynvml' if _HAS_PYNVML else 'no-sense'} | "
              f"lattice: {lattice_size}x{lattice_size}")

    def tick(self):
        """One doing tick. Read GPU state, tick lattice, push sensorium."""
        now = time.time()
        if now - self._last_sense_time >= self._sense_interval:
            self.state.read()
            # Push hardware snapshot into experience ring buffer
            self.experience.push_sensorium(self.state)
            self._last_sense_time = now

        # Tick the cellular automaton (1 step per engine tick)
        # At 50Hz engine, this is 50 lattice ticks/sec on GPU
        self.lattice.tick(1)

    def compose_operators(self, ops_a, ops_b, table='tsml'):
        """Batch compose operators on GPU."""
        return compose_batch(ops_a, ops_b, table)

    def fuse(self, chain, table='tsml') -> int:
        """Fuse an operator chain through CL table."""
        return fuse_chain(chain, table)

    def lattice_coherence(self) -> float:
        """Get coherence of the cellular automaton."""
        return self.lattice.coherence()

    def inject_operator(self, op: int, x: int = -1, y: int = -1):
        """Inject an operator into the lattice. Random position if -1."""
        if x < 0:
            x = np.random.randint(0, self.lattice.cols)
        if y < 0:
            y = np.random.randint(0, self.lattice.rows)
        self.lattice.inject(op, x, y)

    def save(self):
        """Save GPU transition lattice to disk."""
        self.transition_lattice.save()

    def stats(self) -> dict:
        """GPU doing engine stats."""
        s = {
            'gpu_available': _GPU_AVAILABLE,
            'gpu_name': _GPU_NAME,
            'gpu_mem_mb': _GPU_MEM_MB,
            'has_pynvml': _HAS_PYNVML,
            'gpu_util_pct': self.state.gpu_util_pct,
            'gpu_temp_c': self.state.temperature_c,
            'gpu_power_w': self.state.power_draw_w,
            'gpu_mem_used_mb': self.state.mem_used_mb,
            'lattice_size': f"{self.lattice.rows}x{self.lattice.cols}",
            'lattice_ticks': self.lattice.tick_count,
            'lattice_coherence': round(self.lattice.coherence(), 4),
            'transitions': self.transition_lattice.total_transitions,
        }
        s['experience'] = self.experience.stats()
        return s
