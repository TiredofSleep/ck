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

# pynvml for GPU sensing (separate from compute)
_HAS_PYNVML = False
_nvml_handle = None
try:
    import pynvml
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

class GPUDoingEngine:
    """CK's GPU doing engine.

    Being is on the CPU. Doing is on the GPU. Becoming is everywhere.

    This engine manages:
    - GPU state sensing (temperature, utilization, power)
    - Transition lattice (learned operator patterns)
    - Cellular automaton lattice (coherence field on GPU)
    - Batch composition (parallel CL lookups)
    """

    def __init__(self, lattice_size: int = 64):
        self.state = gpu_state
        self.transition_lattice = GPUTransitionLattice()
        self.lattice = GPULattice(lattice_size, lattice_size)
        self._last_sense_time = 0.0
        self._sense_interval = 2.0  # Read GPU state every 2 seconds

        # Boot state read
        self.state.read()

        print(f"  [GPU] Doing engine: "
              f"{'CUDA' if _GPU_AVAILABLE else 'CPU'} | "
              f"{'pynvml' if _HAS_PYNVML else 'no-sense'} | "
              f"lattice: {lattice_size}x{lattice_size}")

    def tick(self):
        """One doing tick. Read GPU state, tick lattice."""
        now = time.time()
        if now - self._last_sense_time >= self._sense_interval:
            self.state.read()
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
        return {
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
